"""Conservative offline candidate enumeration/replay. Not an exhaustive MV search."""
import collections, json, math, sqlite3, time
from pathlib import Path
import sqlglot
from sqlglot import exp
from common import *

def norm(n):
 n=n.copy()
 for c in n.find_all(exp.Column): c.set('table',None)
 return n.sql(dialect='sqlite',normalize=True)
def comparable(rows,ordered):
 return rows if ordered else sorted(rows,key=lambda r:json.dumps(r,ensure_ascii=False,sort_keys=True))
def equal(a,b,ordered):
 # Exact multiset (preserves duplicates) or ordered comparison. Tolerance only
 # applied to aligned ordered rows; unordered numeric differences remain failures.
 if len(a)!=len(b): return False
 a=comparable(a,ordered); b=comparable(b,ordered)
 return all(len(x)==len(y) and all(u==v or ordered and isinstance(u,(int,float)) and isinstance(v,(int,float)) and math.isclose(u,v,rel_tol=1e-12,abs_tol=1e-9) for u,v in zip(x,y)) for x,y in zip(a,b))
def enumerate_candidates(queries):
 candidates=[]; groups=collections.defaultdict(list); ctes=collections.defaultdict(list); exact=collections.defaultdict(list)
 for q in queries:
  if not q.get('profile',{}).get('parsed') or not q.get('result_complete') or q.get('parameters'): continue
  tree=sqlglot.parse_one(q['sql'],read='sqlite'); exact[q['profile']['canonical_sql']].append(q)
  for c in tree.find_all(exp.CTE):
   # Only self-contained SELECT; any CTE dependency or correlated reference is
   # conservatively excluded by demanding one real source without qualifiers.
   body=c.this
   if isinstance(body,exp.Select) and not body.args.get('with_') and len(list(body.find_all(exp.Table)))>=1:
    t=next(body.find_all(exp.Table))
    if all(table.name in {exp.to_table(x).name for x in q['profile']['base_tables']} for table in body.find_all(exp.Table)):
     ctes[body.sql(dialect='sqlite')].append((q,c.alias_or_name))
  if not isinstance(tree,exp.Select) or tree.args.get('with_') or tree.args.get('joins') or list(tree.find_all(exp.Subquery)) or list(tree.find_all(exp.Window)): continue
  ts=list(tree.find_all(exp.Table))
  if len(ts)!=1: continue
  table=ts[0]; where=tree.args.get('where')
  key=(table.name,norm(where) if where else '')
  groups[key].append((q,tree))
 for canonical,qs in exact.items():
  if len(qs)>1: candidates.append({'type':'exact-result reuse','existing_result':True,'producer':qs[0]['sql_id'],'covered':[q['sql_id'] for q in qs],'build_sql':None,'rewrites':{},'status':'pending','reason':'Identical normalized SQL and parameters; archive equality checked.'})
 for body,items in ctes.items():
  qs={q['sql_id']:q for q,name in items}
  if len(qs)<2: continue
  rewrites={}
  for qid,q in qs.items():
   tree=sqlglot.parse_one(q['sql'],read='sqlite')
   for c in tree.find_all(exp.CTE):
    if c.this.sql(dialect='sqlite')==body: c.set('this',sqlglot.parse_one('SELECT * FROM temp.reuse_candidate',read='sqlite'))
   rewrites[qid]=tree.sql(dialect='sqlite')
  candidates.append({'type':'common subexpression','existing_result':False,'build_sql':body,'covered':list(qs),'rewrites':rewrites,'status':'pending','reason':'Identical self-contained CTE body across queries.'})
 for (table,where),items in groups.items():
  if len(items)<2: continue
  if where:
   build=f'SELECT * FROM "{table.replace(chr(34),chr(34)*2)}" '+where
   rewrites={}
   for q,tree in items:
    t=tree.copy(); old=next(t.find_all(exp.Table)); replacement=exp.to_table('temp.reuse_candidate'); replacement.set('alias',old.args.get('alias') or exp.TableAlias(this=exp.to_identifier(old.name))); old.replace(replacement)
    rewrites[q['sql_id']]=t.sql(dialect='sqlite')
   candidates.append({'type':'common filtered view','existing_result':False,'build_sql':build,'covered':[q['sql_id'] for q,t in items],'rewrites':rewrites,'status':'pending','reason':'Same single source and complete filter; original filter retained.'})
  aggitems=[]; dims={}; states={}
  for q,tree in items:
   aggs=[a for a in tree.find_all(exp.AggFunc) if not (isinstance(a,(exp.Min,exp.Max)) and a.expressions)]; group=tree.args.get('group')
   if not aggs or any(not isinstance(a,(exp.Sum,exp.Count,exp.Avg,exp.Min,exp.Max)) or a.find(exp.Distinct) or isinstance(a.parent,exp.Filter) for a in aggs): continue
   if any(isinstance(x,exp.Star) for x in tree.selects): continue
   keys=q['profile']['blocks'][-1]['group_by']; localdims={norm(sqlglot.parse_one(k['expression'],read='sqlite')) for k in keys}
   # Reject SQLite's arbitrary bare columns and HAVING-only columns.
   valid=True
   for node in tree.selects+[tree.args.get('having')] if tree.args.get('having') else tree.selects:
    probe=node.copy()
    for a in list(probe.find_all(exp.AggFunc)): a.replace(exp.Literal.number(0))
    probe=probe.transform(lambda n:exp.Literal.number(0) if norm(n) in localdims else n)
    if list(probe.find_all(exp.Column)): valid=False
   if not valid: continue
   aggitems.append((q,tree,keys))
   for k in keys: dims.setdefault(norm(sqlglot.parse_one(k['expression'],read='sqlite')),f'__g{len(dims)}')
   for a in aggs: states.setdefault(norm(a),(a.copy(),f'__a{len(states)}'))
  if len(aggitems)<2: continue
  selections=[f'{expr} AS {alias}' for expr,alias in dims.items()]; replacement={}
  for expr,(a,alias) in states.items():
   inner=norm(a.this)
   if isinstance(a,exp.Avg):
    selections.extend([f'SUM({inner}) AS {alias}_sum',f'COUNT({inner}) AS {alias}_n']); replacement[expr]=f'(1.0*SUM({alias}_sum)/NULLIF(SUM({alias}_n),0))'
   else:
    selections.append(f'{expr} AS {alias}'); fn='SUM' if isinstance(a,(exp.Sum,exp.Count)) else a.sql_name(); replacement[expr]=f'{fn}({alias})'
  build='SELECT '+', '.join(selections)+' FROM "'+table.replace('"','""')+'" '+where+(' GROUP BY '+', '.join(dims) if dims else '')
  rewrites={}
  for q,tree,keys in aggitems:
   t=tree.copy(); t.set('where',None); t.set('from_',exp.From(this=exp.to_table('temp.reuse_candidate')))
   if keys: t.set('group',exp.Group(expressions=[sqlglot.parse_one(k['expression'],read='sqlite') for k in keys]))
   def replace(n):
    key=norm(n)
    if isinstance(n,exp.AggFunc) and key in replacement: return sqlglot.parse_one(replacement[key],read='sqlite')
    if key in dims: return exp.column(dims[key])
    return n
   t=t.transform(replace)
   # Preserve output names exactly; bare group expressions otherwise change name.
   for original,rewritten in zip(tree.selects,t.selects):
    if not isinstance(rewritten,exp.Alias) and original.output_name: rewritten.replace(exp.alias_(rewritten.copy(),original.output_name,quoted=True))
   rewrites[q['sql_id']]=t.sql(dialect='sqlite')
  candidates.append({'type':'aggregate MV','existing_result':False,'build_sql':build,'covered':[q['sql_id'] for q,t,k in aggitems],'rewrites':rewrites,'status':'pending','reason':'Union of grouping keys; decomposable aggregate states; AVG uses SUM and non-NULL COUNT.'})
 for i,c in enumerate(candidates,1):
  c.update(candidate_id=f'C{i}',offline=True,earliest_build_before=c['covered'][0],later_reuses=len(c['covered'])-1,denominator=len(queries),coverage_includes_trigger=True)
 return candidates

def verify(c,queries,run,dbpath,seconds=120):
 byid={q['sql_id']:q for q in queries}; deadline=time.time()+seconds; checks=[]
 try:
  if c['existing_result']:
   qs=[byid[k] for k in c['covered']]; producer=qs[0]; original=[json.loads(l) for l in (run/producer['result_file']).read_text().splitlines()]
   if producer['result_bytes']>32*1024*1024: raise TimeoutError('Offline result size cap')
   for q in qs[1:]:
    rows=[json.loads(l) for l in (run/q['result_file']).read_text().splitlines()]; ordered=bool(sqlglot.parse_one(q['sql'],read='sqlite').args.get('order'))
    checks.append({'sql_id':q['sql_id'],'columns_equal':q['columns']==producer['columns'],'rows_equal':equal(original,rows,ordered),'comparison':'ordered_numeric_tolerance' if ordered else 'exact_multiset'})
   c['intermediate_rows']=len(original)
  else:
   db=sqlite3.connect(Path(dbpath).resolve().as_uri()+'?mode=ro',uri=True)
   db.set_progress_handler(lambda:int(time.time()>deadline),10000)
   t=time.perf_counter(); db.execute('CREATE TEMP TABLE reuse_candidate AS '+c['build_sql']); c['build_ms']=(time.perf_counter()-t)*1000
   c['intermediate_rows']=db.execute('SELECT COUNT(*) FROM temp.reuse_candidate').fetchone()[0]
   c['intermediate_columns']=[r[1] for r in db.execute('PRAGMA temp.table_info(reuse_candidate)')]
   for sid,rewrite in c['rewrites'].items():
    q=byid[sid]
    if q['result_bytes']>32*1024*1024: raise TimeoutError('Offline result size cap')
    t=time.perf_counter(); cur=db.execute(rewrite); rows=[]
    while chunk:=cur.fetchmany(1000):
     rows.extend([list(r) for r in chunk])
     if len(rows)>1_000_000 or time.time()>deadline: raise TimeoutError('Offline replay cap')
    original=[json.loads(l) for l in (run/q['result_file']).read_text().splitlines()]
    ordered=bool(sqlglot.parse_one(q['sql'],read='sqlite').args.get('order'))
    checks.append({'sql_id':sid,'rewritten_sql':rewrite,'columns_equal':[d[0] for d in cur.description]==q['columns'],'rows_equal':equal(original,rows,ordered),'comparison':'ordered_numeric_tolerance' if ordered else 'exact_multiset','replay_ms':(time.perf_counter()-t)*1000})
   db.close()
  c['status']='verified' if all(x['columns_equal'] and x['rows_equal'] for x in checks) else 'rejected_result_mismatch'
 except Exception as e: c.update(status='verification_limited' if isinstance(e,TimeoutError) or 'interrupted' in str(e) else 'verification_error',error=repr(e))
 c['checks']=checks; c['cost_conclusion']='Not benchmarked; correctness alone does not establish net speedup.'
 return c
