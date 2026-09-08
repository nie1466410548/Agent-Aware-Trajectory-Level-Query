"""Conservative static preparation candidates with exact base input/consumer evidence.

No cost claims. Only supported scopes are analyzed; this is not exhaustive.
"""
import collections,json
from pathlib import Path
import sqlglot
from sqlglot import exp
from sqlglot.optimizer.qualify import qualify
from sqlglot.optimizer.scope import traverse_scope
from overlap_features import SCHEMAS
ROOT=Path(__file__).resolve().parents[1]

def conjuncts(e):
 return conjuncts(e.this)+conjuncts(e.expression) if isinstance(e,exp.And) else [e]
def canonical(e,mapping):
 t=e.copy()
 for c in t.find_all(exp.Column):
  if c.table in mapping:c.set('table',exp.to_identifier(mapping[c.table]))
 for tab in t.find_all(exp.Table):tab.set('alias',None)
 return t.sql(normalize=True,pretty=False)
def extract(q,ds):
 evidence=[]
 for tree in sqlglot.parse(q['sql'],read=q['dialect']):
  if tree is None:continue
  for ident in tree.find_all(exp.Identifier):ident.set('this',ident.this.lower());ident.set('quoted',False)
  tree=qualify(tree,dialect=q['dialect'],schema=SCHEMAS[ds,q['database']],validate_qualify_columns=True)
  for scope in traverse_scope(tree):
   node=scope.expression
   if not isinstance(node,exp.Select):continue
   sources={a:s for a,s in scope.sources.items() if isinstance(s,exp.Table)}
   # CTE names can coexist in scope.sources even when not selected. selected_sources
   # establishes the actual FROM inputs of this scope.
   selected=scope.selected_sources
   if not selected or any(not isinstance(v[1],exp.Table) for v in selected.values()):continue
   sources={a:v[1] for a,v in selected.items()};mapping={a:s.name.lower() for a,s in sources.items()}
   if len(set(mapping.values()))!=len(mapping):continue # self-join role ambiguity
   cols=list(node.find_all(exp.Column))
   local=list(scope.columns)
   def supported(e):
    volatile=(exp.Rand,exp.CurrentDate,exp.CurrentTime,exp.CurrentTimestamp)
    return not e.find(exp.Select) and not any(isinstance(n,volatile) for n in e.walk()) and all(c.table in mapping for c in e.find_all(exp.Column))
   joins=node.args.get('joins') or []
   inner=all(not j.args.get('side') and j.args.get('kind','').upper() in ['','INNER'] and j.args.get('on') is not None and supported(j.args['on']) for j in joins)
   from_=node.args.get('from_')
   if from_ is None:continue
   relation=canonical(from_,mapping)+' '+ ' '.join(canonical(j,mapping) for j in joins)
   relation=relation.strip();tables=sorted(mapping.values())
   where=node.args.get('where')
   if inner and where:
    for atom in conjuncts(where.this):
     if not supported(atom):continue
     refs={mapping[c.table] for c in atom.find_all(exp.Column)}
     if len(refs)==1:
      table=next(iter(refs));predicate=canonical(atom,mapping)
      evidence.append(dict(kind='filter',object=predicate,relation=table,tables=[table],
        preparation='保留满足此共同条件的完整基表行子集及消费者所需列；各查询继续执行其余操作。',
        limits='仅处理基表单输入或纯内连接中的 WHERE 合取项；不是现有 LIMIT 样本的缓存。准备成本和实际选择率未测。'))
   if joins and inner:
    evidence.append(dict(kind='join',object=relation,relation=relation,tables=tables,
      preparation='准备此完整基表内连接的行级结果，保留消费者需要的原始列及重复行；各自筛选、聚合、排序继续执行。',
      limits='只合并完全相同连接类型、键和输入；不合并外连接/自连接/派生输入。全量 Join 可能不如谓词下推便宜。'))
   # Repeated nontrivial pure per-row scalar work on the same base table.
   for scalar in node.walk():
    if not isinstance(scalar,(exp.Substring,exp.Replace,exp.RegexpExtract,exp.StrToTime)):continue
    if not supported(scalar):continue
    refs={mapping[c.table] for c in scalar.find_all(exp.Column)}
    if len(refs)!=1:continue
    table=next(iter(refs))
    evidence.append(dict(kind='derived',object=canonical(scalar,mapping),relation=table,tables=[table],
      preparation='对消费者需要的基表行预计算该标量表达式并保留原始列，供后续查询引用派生列。',
      limits='需维持各查询的求值范围、NULL/异常和数据类型语义；未验证提前求值不会触及原查询不处理的行。不仅凭函数名相同。'))
   # Aggregates count only when the full FROM/WHERE/GROUP input is identical.
   if not inner or (where and not supported(where.this)):continue
   if any(isinstance(n,exp.Select) and n is not node for n in node.walk()):continue
   group=node.args.get('group')
   if group and not supported(group):continue
   input_sig=relation+' '+(canonical(where,mapping) if where else '')+' '+(canonical(group,mapping) if group else '')
   for agg in node.find_all(exp.AggFunc):
    if not isinstance(agg,(exp.Count,exp.Sum,exp.Avg,exp.Min,exp.Max)) or not supported(agg):continue
    if agg.find_ancestor(exp.Window):continue
    # FILTER belongs to the aggregate input, even though it is an AST parent.
    aggregate=agg.parent if isinstance(agg.parent,exp.Filter) else agg
    if not supported(aggregate):continue
    evidence.append(dict(kind='aggregate_state',object=canonical(aggregate,mapping),relation=input_sig.strip(),tables=tables,
      preparation='在完全相同输入与分组上准备此聚合的完整结果/状态，保留全部分组后再施加各自 HAVING、排序和 LIMIT。',
      limits='基表只读且输入/分组表达式完全相同才入选；不将不同表或不同分组的 COUNT 合并。仅一个廉价 COUNT 的价值可能很小。'))
 return evidence

def main():
 data=json.loads((ROOT/'reports/overlap-detail.json').read_text());candidates=[];errors=[]
 for run in data['runs']:
  ds=run['task'].split('/')[0];objects={};byid={q['call_id']:q for q in run['queries']}
  for q in run['queries']:
   try:items=extract(q,ds)
   except Exception as e:errors.append(dict(task=run['task'],group=run['group'],call_id=q['call_id'],error=str(e)));continue
   for obj in items:
    key=(q['database'],obj['kind'],obj['relation'],obj['object'])
    row=objects.setdefault(key,dict(obj,database=q['database'],call_ids=set()))
    row['call_ids'].add(q['call_id'])
  # Merge common expressions of same kind, input and consumer set into one object group.
  merged={}
  for obj in objects.values():
   if len(obj['call_ids'])<2:continue
   ids=tuple(sorted(obj['call_ids'],key=lambda cid:byid[cid]['start_time']))
   key=(obj['database'],obj['kind'],obj['relation'],ids)
   row=merged.setdefault(key,{**obj,'objects':[],'call_ids':ids})
   row['objects'].append(obj['object'])
  for obj in merged.values():
   directory=ROOT/Path(run['analysis_path']).parent
   links=[str(next((directory/'sql').glob('*-'+cid+'.sql')).relative_to(ROOT)) for cid in obj['call_ids']]
   candidates.append({**obj,'task':run['task'],'group':run['group'],'task_passed':run['passed'],
      'consumer_count':len(obj['call_ids']),'later_count':len(obj['call_ids'])-1,'sql_files':links,
      'status':'static_candidate_not_replayed'})
 # Mongo native filters are kept separate from SQL structures.
 for run in data['runs']:
  full=json.loads((ROOT/run['analysis_path']).read_text());groups={}
  for q in full.get('mongo_queries',[]):
   if not q['success'] or q['metadata']:continue
   req=q['mongo_request'];predicate=req.get('filter')
   if req.get('operation')=='aggregate':
    pipeline=req.get('pipeline',[])
    predicate=pipeline[0].get('$match') if pipeline and isinstance(pipeline[0],dict) else None
   if not predicate:continue
   key=(q['database'],req['collection'],json.dumps(predicate,sort_keys=True,ensure_ascii=False))
   groups.setdefault(key,[]).append(q)
  for (db,collection,predicate),qs in groups.items():
   if len(qs)<2:continue
   directory=ROOT/Path(run['analysis_path']).parent
   files=[str(next((directory/'mongo').glob('*-'+q['call_id']+'.json')).relative_to(ROOT)) for q in qs]
   candidates.append(dict(kind='mongo_filter',object=predicate,objects=[predicate],relation=collection,tables=[collection],database=db,
      preparation='准备同一集合上相同原生筛选条件的完整文档子集，继续保留消费者各自的管道、投影和 LIMIT。',
      limits='只匹配非空 find/count/distinct filter 或管道首个 $match，不把任意全集合读取当成机会；未测缓存成本。',
      call_ids=[q['call_id'] for q in qs],task=run['task'],group=run['group'],task_passed=run['passed'],
      consumer_count=len(qs),later_count=len(qs)-1,sql_files=files,status='static_candidate_not_replayed'))
 for n,c in enumerate(candidates,1):c['id']=f'C{n:04d}'
 (ROOT/'reports/opportunities.json').write_text(json.dumps({'method':'conservative exact-input static extraction, not exhaustive or cost-validated; categories can overlap','candidates':candidates,'errors':errors},ensure_ascii=False,indent=2)+'\n')
 print('Candidate groups',len(candidates),'extraction errors',len(errors))
if __name__=='__main__':main()
