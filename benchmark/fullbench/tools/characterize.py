"""Five-RQ offline characterization. No agent calls or database execution."""
import collections,csv,hashlib,itertools,json,statistics
from pathlib import Path
import sqlglot,sqlparse
from sqlglot import exp
from sqlglot.optimizer.qualify import qualify
from sqlglot.optimizer.scope import traverse_scope
from overlap_features import SCHEMAS
from discover import canonical,conjuncts

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'reports/characterization'

def dump(name,obj):
 (OUT/name).write_text(json.dumps(obj,ensure_ascii=False,indent=2)+'\n')
def csvfile(name,rows):
 if not rows:return
 with (OUT/name).open('w') as f:
  w=csv.DictWriter(f,fieldnames=list(rows[0]));w.writeheader();w.writerows(rows)
def avg(xs):return statistics.mean(xs) if xs else None
def ratio(a,b):return a/b if b else None
def fmt(x):return '—' if x is None else f'{x:.2f}'
def pct(a,b):return '—' if not b else f'{a/b:.1%}'
def jac(a,b):return ratio(len(a&b),len(a|b))
def valuekey(v):
 if isinstance(v,bool) or v is None or isinstance(v,(dict,list)):return None
 if isinstance(v,(int,float)):return ('number',str(v))
 return ('string',str(v))
def literals(sql,dialect):
 """Only direct column-literal EQ/IN predicates, not arbitrary constant matches."""
 found=[]
 try:trees=sqlglot.parse(sql,read=dialect)
 except sqlglot.errors.ParseError:return found
 for tree in trees:
  if tree is None:continue
  for where in tree.find_all(exp.Where):
   for node in where.walk():
    pairs=[]
    if isinstance(node,exp.EQ):
     pairs=[(node.this,node.expression),(node.expression,node.this)]
    elif isinstance(node,exp.In) and not node.args.get('query'):
     pairs=[(node.this,x) for x in node.expressions]
    for col,val in pairs:
     if isinstance(col,exp.Column) and isinstance(val,exp.Literal):
      key=('string' if val.is_string else 'number',val.this)
      found.append({'column':col.sql(),'value':val.this,'value_type':key[0],'key':key,'predicate':node.sql()})
 return found

def scoped(q,ds):
 """Base-input grouped scopes. Derived/CTE inputs and outer/self joins excluded."""
 result=[]
 for tree in sqlglot.parse(q['sql'],read=q['dialect']):
  if tree is None:continue
  for ident in tree.find_all(exp.Identifier):ident.set('this',ident.this.lower());ident.set('quoted',False)
  tree=qualify(tree,dialect=q['dialect'],schema=SCHEMAS[ds,q['database']],validate_qualify_columns=True)
  for scope in traverse_scope(tree):
   node=scope.expression
   if not isinstance(node,exp.Select):continue
   group=node.args.get('group')
   if not group:continue
   sources=scope.selected_sources
   if not sources or any(not isinstance(v[1],exp.Table) for v in sources.values()):continue
   mapping={alias:source[1].name.lower() for alias,source in sources.items()}
   if len(set(mapping.values()))!=len(mapping):continue
   if any(group.args.get(k) for k in ['grouping_sets','cube','rollup','all']):continue
   joins=node.args.get('joins') or []
   if any(j.args.get('side') or j.args.get('kind','').upper() not in ('','INNER') or not j.args.get('on') for j in joins):continue
   def safe(e):
    return not any(isinstance(n,(exp.Select,exp.Window,exp.Rand,exp.CurrentDate,exp.CurrentTime,exp.CurrentTimestamp)) for n in e.walk()) and all(c.table in mapping for c in e.find_all(exp.Column))
   if not safe(group):continue
   where=node.args.get('where')
   if where and not safe(where):continue
   relation=(canonical(node.args['from_'],mapping)+' '+' '.join(canonical(j,mapping) for j in joins)).strip()
   predicates=sorted(canonical(x,mapping) for x in conjuncts(where.this)) if where else []
   aggregates=[];unsupported=[]
   for agg in node.find_all(exp.AggFunc):
    if agg.find_ancestor(exp.Select) is not node:continue
    whole=agg.parent if isinstance(agg.parent,exp.Filter) else agg
    if not safe(whole):unsupported.append(whole.sql());continue
    if not isinstance(agg,(exp.Count,exp.Sum,exp.Min,exp.Max,exp.Avg)) or agg.find(exp.Distinct):unsupported.append(whole.sql());continue
    aggregates.append(canonical(whole,mapping))
   result.append({'relation':relation,'where_atoms':predicates,'keys':sorted(set(canonical(x,mapping) for x in group.expressions)),
     'aggregates':sorted(set(aggregates)),'unsupported_aggregates':sorted(set(unsupported)),
     'input':relation+' WHERE '+ ' AND '.join(predicates)})
 return result

def main():
 OUT.mkdir(exist_ok=True)
 structural=json.loads((ROOT/'reports/overlap-detail.json').read_text())
 bound={(r['task'],r['group']):{q['call_id']:q for q in r['queries']} for r in structural['runs']}
 existing=json.loads((ROOT/'reports/opportunities.json').read_text())['candidates']
 runs=[];adjacent=[];evolution=[];dependencies=[];candidates=[];issues=[];allscopes=[]
 for path in sorted((ROOT/'runs').glob('*/*/*/full-01/analysis.json')):
  a=json.loads(path.read_text());s=a['summary'];task=s['task_id'];g=s['group'];ds=task.split('/')[0];run=path.parent
  identity={'task':task,'group':g};bs=bound[task,g]
  events=[json.loads(x) for x in (run/'tool_calls.jsonl').read_text().splitlines()] if (run/'tool_calls.jsonl').exists() else []
  eventmap={x['call_id']:x for x in events};sqls=a['queries'];byid={q['call_id']:q for q in sqls}
  qs=[q for q in sqls if not q['metadata']];success=[q for q in qs if q['success']]
  paths={q['call_id']:str(next((run/'sql').glob('*-'+q['call_id']+'.sql')).relative_to(ROOT)) for q in sqls}
  ns=0;groups=0;scope_queries=0;scopes=[]
  for q in qs:
   ns+=len(sqlparse.split(q['sql']))
   try:trees=[t for t in sqlglot.parse(q['sql'],read=q['dialect']) if t is not None]
   except Exception as e:issues.append({**identity,'call_id':q['call_id'],'stage':'syntax','error':str(e)});continue
   if not q['success']:continue
   groups+=any(t.find(exp.Group) for t in trees)
   try:found=scoped(q,ds)
   except Exception as e:issues.append({**identity,'call_id':q['call_id'],'stage':'group_binding','error':str(e)});continue
   scope_queries+=bool(found)
   for n,x in enumerate(found):scopes.append({**identity,**x,'call_id':q['call_id'],'scope':n,'database':q['database'],'sql_file':paths[q['call_id']],'start_time':q['start_time']})
  allscopes+=scopes
  # Consecutive data requests: a failed SQL or Mongo request breaks SQL adjacency.
  native={q['call_id']:q for q in a.get('mongo_queries',[])}
  requests=[byid.get(e['call_id'],native.get(e['call_id'])) for e in events if e['tool']=='query-db']
  requests=[q for q in requests if q and not q['metadata']]
  adj=[]
  for p,q in zip(requests,requests[1:]):
   if not p['success'] or not q['success'] or not isinstance(p.get('sql'),str) or not isinstance(q.get('sql'),str):continue
   row={**identity,'producer':p['call_id'],'consumer':q['call_id'],'producer_sql':paths[p['call_id']],'consumer_sql':paths[q['call_id']],
        'same_database':p['database']==q['database'],'binding_complete':p['call_id'] in bs and q['call_id'] in bs}
   for name,field in [('relation','tables'),('predicate','filter_atoms'),('join','bound_joins')]:
    if field!='tables' and not row['binding_complete']:row[name+'_jaccard']=None;row[name+'_hit']=None;continue
    left=bs.get(p['call_id'],p);right=bs.get(q['call_id'],q)
    u={(p['database'],x) for x in left[field]};v={(q['database'],x) for x in right[field]}
    row[name+'_jaccard']=jac(u,v);row[name+'_hit']=bool(u&v)
   adj.append(row)
  adjacent+=adj
  # Group evolution is scope-based, all later calls; query-pair counts deduplicate scopes.
  ev=[]
  for p,q in itertools.combinations(scopes,2):
   if p['call_id']==q['call_id'] or p['database']!=q['database'] or p['relation']!=q['relation']:continue
   x,y=set(p['keys']),set(q['keys'])
   kind='same_keys' if x==y else 'refinement' if x<y else 'coarsening' if y<x else 'sibling'
   ev.append({**identity,'producer':p['call_id'],'consumer':q['call_id'],'producer_scope':p['scope'],'consumer_scope':q['scope'],
     'producer_sql':p['sql_file'],'consumer_sql':q['sql_file'],'kind':kind,'same_predicates':p['where_atoms']==q['where_atoms'],
     'before_keys':p['keys'],'after_keys':q['keys'],'before_aggregates':p['aggregates'],'after_aggregates':q['aggregates'],
     'producer_input':p['input'],'consumer_input':q['input']})
  evolution+=ev
  # Same-input aggregate preparation can combine keys and different aggregate metrics.
  buckets=collections.defaultdict(list)
  for x in scopes:
   if x['aggregates']:buckets[x['database'],x['input']].append(x)
  for (db,inp),ss in buckets.items():
   ids=list(dict.fromkeys(x['call_id'] for x in ss))
   if len(ids)<2:continue
   keys=sorted({k for x in ss for k in x['keys']});aggs=sorted({k for x in ss for k in x['aggregates']})
   candidates.append({**identity,'kind':'aggregate_mv_extended','database':db,'input':inp,'group_keys':keys,'aggregates':aggs,'call_ids':ids,
    'sql_files':[paths[c] for c in ids],'consumer_count':len(ids),'expected_reuse':len(ids)-1,'build_ms':None,'reuse_ms':None,
    'different_group_keys':len({tuple(x['keys']) for x in ss})>1,'different_metrics':len({tuple(x['aggregates']) for x in ss})>1,
    'eligibility':'partial_aggregate_component_static_candidate','limitations':'Union grouping keys; SUM/COUNT/MIN/MAX merge, AVG needs SUM and non-NULL COUNT. Preserve complete groups and per-consumer HAVING/LIMIT, absent/empty groups, FILTER and NULL/type semantics. Unsupported aggregates still require base computation. Fine grouping may approach base cardinality. No rewrite/cost validation.'})
  for c in existing:
   if c['task']!=task or c['group']!=g or c['kind'] not in ('filter','join','derived','aggregate_state'):continue
   candidates.append({**identity,'kind':c['kind'],'database':c['database'],'input':c['relation'],'objects':c['objects'],'call_ids':c['call_ids'],
    'sql_files':c['sql_files'],'consumer_count':c['consumer_count'],'expected_reuse':c['later_count'],'build_ms':None,'reuse_ms':None,
    'eligibility':'partial_component_static_candidate','limitations':c['limits']})
  # Match next-query predicate literals against complete saved result rows.
  deps=[]
  literal_cache={old['call_id']:literals(old['sql'],old['dialect']) for old in qs}
  for p,q in zip(requests,requests[1:]):
   if not p['success'] or not q['success'] or not isinstance(p.get('sql'),str) or not isinstance(q.get('sql'),str):continue
   if len(sqlglot.parse(p['sql'],read=p['dialect']))!=1:continue
   wanted=literal_cache[q['call_id']]
   if not wanted:continue
   e=eventmap[p['call_id']];result_path=Path(e.get('result_file',run/'results'/f"{p['call_id']}.json"))
   rows=json.loads(result_path.read_text());keys={tuple(x['key']) for x in wanted};matched={}
   for row_index,row in enumerate(rows):
    if not isinstance(row,dict):continue
    for col,v in row.items():
     key=valuekey(v)
     if key in keys:matched.setdefault(key,{'row_index':row_index,'result_column':col})
   before={tuple(x['key']) for old in qs if old['start_time']<q['start_time'] for x in literal_cache[old['call_id']]}
   prompt=(run/'prompt.txt').read_text()
   for x in wanted:
    key=tuple(x['key'])
    if key not in matched:continue
    deps.append({**identity,'producer':p['call_id'],'consumer':q['call_id'],'producer_sql':paths[p['call_id']],'consumer_sql':paths[q['call_id']],
      'predicate_column':x['column'],'predicate':x['predicate'],'value':x['value'],'value_type':x['value_type'],**matched[key],
      'new_in_sql_predicates':key not in before,'literal_text_in_prompt':str(x['value']) in prompt,
      'result_file':str(result_path.relative_to(ROOT)),'evidence_level':'value_match_not_causal_proof'})
  dependencies+=deps
  runs.append({**identity,'validated':s['validator_passed'],'sql_attempt_calls':len(qs),'sql_statement_count':ns,'successful_sql':len(success),
   'metadata_sql':len(sqls)-len(qs),'mongo_data_requests':sum(not q['metadata'] for q in native.values()),'python_calls':s['python_calls'],
   'assistant_turns':s['assistant_turns'],'group_by_calls':groups,'group_base_scope_calls':scope_queries,'adjacent_pairs':len(adj),
   'relation_overlap_pairs':sum(x['relation_hit'] is True for x in adj),'predicate_overlap_pairs':sum(x['predicate_hit'] is True for x in adj),
   'join_overlap_pairs':sum(x['join_hit'] is True for x in adj),'binding_complete_pairs':sum(x['binding_complete'] for x in adj),
   'same_keys_pairs':len({(x['producer'],x['consumer']) for x in ev if x['kind']=='same_keys'}),
   'refinement_pairs':len({(x['producer'],x['consumer']) for x in ev if x['kind']=='refinement'}),
   'coarsening_pairs':len({(x['producer'],x['consumer']) for x in ev if x['kind']=='coarsening'}),
   'sibling_pairs':len({(x['producer'],x['consumer']) for x in ev if x['kind']=='sibling'}),
   'predicate_change_pairs':len({(x['producer'],x['consumer']) for x in ev if not x['same_predicates']}),
   'result_match_pairs':len({(x['producer'],x['consumer']) for x in deps}),
   'new_result_match_pairs':len({(x['producer'],x['consumer']) for x in deps if x['new_in_sql_predicates'] and not x['literal_text_in_prompt']})})
 # Candidate timing is a whole-query baseline, never an estimated aggregate cost.
 for n,c in enumerate(candidates,1):
  c['id']=f'ME{n:04d}'
  run=ROOT/'runs'/c['group']/c['task']/'full-01';events={x['call_id']:x for x in map(json.loads,(run/'tool_calls.jsonl').read_text().splitlines())}
  c['consumer_execute_fetch_ms']=[events[cid].get('execute_fetch_ms') for cid in c['call_ids']]
  c['later_baseline_execute_fetch_ms']=sum(x for x in c['consumer_execute_fetch_ms'][1:] if x is not None)
  c['timing_complete']=all(x is not None for x in c['consumer_execute_fetch_ms'])
  c['optimistic_incremental_build_budget_ms']=c['later_baseline_execute_fetch_ms'] if c['timing_complete'] else None
 for r in runs:
  cs=[c for c in candidates if c['task']==r['task'] and c['group']==r['group']]
  r.update(candidate_groups=len(cs),mv_covered_calls=len({cid for c in cs for cid in c['call_ids']}),later_covered_calls=len({cid for c in cs for cid in c['call_ids'][1:]}),
   reuse_ge2_candidates=sum(c['expected_reuse']>=2 for c in cs))
 dump('runs.json',runs);dump('adjacent-pairs.json',adjacent);dump('group-evolution.json',evolution);dump('group-scopes.json',allscopes)
 dump('result-dependencies.json',dependencies);dump('materialization-candidates.json',candidates);dump('analysis-issues.json',issues);csvfile('task-characterization.csv',runs)
 render(runs,adjacent,evolution,dependencies,candidates,issues)
 print('Characterized',len(runs),'runs;',len(adjacent),'adjacent pairs;',len(evolution),'group scope transitions;',len(dependencies),'literal matches;',len(candidates),'candidate groups;',len(issues),'issues')

def render(runs,adj,ev,deps,cs,issues):
 lines=['# Characterizing SQL Trajectories of Data Analysis Agents','',
 '54 个任务 × 自然/FAD 两组，共 108 条轨迹；仅使用 full-01 全量实验。所有比较限定同一任务、同一组、同一次运行。答案验证失败的完整轨迹保留；额度中断尝试不混入。此次仅离线分析，没有调用 Agent、重跑数据库或测物化收益。','',
 '计数单位以 SQL 工具调用为主，多语句调用另列语句数。SQL 轨迹不等于整个 Agent 轨迹：元数据 SQL、Python、MongoDB 请求和 assistant 轮数分别保留。相邻指实际连续的数据 query-db 请求；过滤掉元数据，但失败或 Mongo 请求会中断有效 SQL 对，不跨过它们拼接。', '',
 '## RQ1 — Trajectory Structure','',
 '| 组 | 任务数 | SQL 尝试总数 | 平均 N_SQL | 中位数 | P90 | 范围 | 成功 SQL | 平均 assistant 轮数 |',
 '|---|---:|---:|---:|---:|---:|---|---:|---:|']
 for g in ['natural','fad']:
  rs=[r for r in runs if r['group']==g];ns=sorted(r['sql_attempt_calls'] for r in rs)
  lines.append(f"| {g} | {len(rs)} | {sum(ns)} | {avg(ns):.2f} | {statistics.median(ns)} | {ns[int(.9*(len(ns)-1))]} | {min(ns)}–{max(ns)} | {sum(r['successful_sql'] for r in rs)} | {avg([r['assistant_turns'] for r in rs]):.2f} |")
 lines += ['', '这里 Length(T_SQL)=N_SQL（含失败数据 SQL 尝试），不是模型轮数或 SQL 语句数。详表同时记录三者；不能把结束轮数称为成功收敛轮数。', '',
 '**本节结论：** 当前 workload 以较短的 SQL 轨迹为主，单任务平均约产生 5–6 次数据 SQL 调用。任务内存在跨查询优化的时间窗口，但可供摊销准备成本的后续查询数量有限，因此优化方案需要能在较少的复用次数内收回成本。FAD 组 SQL 较少、assistant 轮数较多只是本次观测，不能据此认定协议提高了效率。', '',
 '## RQ2 — Cross-query Similarity','',
 'RelationOverlap、PredicateOverlap、JoinOverlap 均为对应特征集合的 Jaccard。表名包含逻辑数据库身份；谓词按归一 AST 的 WHERE 合取项严格匹配（基表别名归一，复杂派生列不保证完整血缘）；Join 是归一语法片段，尚非完整 Join 输入等价证明。空并集的 Jaccard 未定义，不算 1；未解析特征也不当作 0。','',
 '| 组 | 有效相邻 SQL 对 | Relation 命中 | 平均 Jaccard / n | Predicate 命中 / 可分析对 | 平均 Jaccard / n | Join 命中 / 可分析对 | 平均 Jaccard / n |',
 '|---|---:|---:|---|---|---|---|---|']
 for g in ['natural','fad']:
  ps=[x for x in adj if x['group']==g];cells=[]
  for kind in ['relation','predicate','join']:
   good=[x for x in ps if x[kind+'_hit'] is not None];vals=[x[kind+'_jaccard'] for x in ps if x[kind+'_jaccard'] is not None]
   cells.extend([f"{sum(x[kind+'_hit'] for x in good)}/{len(good)}",f'{fmt(avg(vals))} / {len(vals)}'])
  lines.append('| '+g+' | '+str(len(ps))+' | '+' | '.join(cells)+' |')
 lines += ['', '**本节结论：** 两组约四到五成的有效相邻 SQL 对访问了相同基表，说明任务内存在较明显的访问局部性；相同 WHERE 合取项和 Join 片段的命中则少得多。现有证据支持继续寻找共同扫描或共享子计算，但“访问同表”本身不能证明前序结果可复用，也不能直接作为物化收益。', '',
 '## RQ3 — Analytical Evolution','',
 '先统计 GROUP BY 使用量，再在相同完整基表 FROM/INNER JOIN 输入的前后分组作用域中比较键集合。细化 A⊂B，粗化 B⊂A，sibling 为双方互不包含；相同键单列。分组表达式先解析别名和 GROUP BY 位置引用。两条 SQL 的多个作用域可使其进入不同类别，类别不可直接相加。', '',
 '| 组 | 含 GROUP BY 的调用 | 涉及任务 | 支持基表输入演化分析的调用 | 同键查询对 | 细化对 | 粗化对 | Sibling 对 | 上述对中筛选发生变化 |',
 '|---|---:|---:|---:|---:|---:|---:|---:|---:|']
 for g in ['natural','fad']:
  rs=[r for r in runs if r['group']==g]
  lines.append(f"| {g} | {sum(r['group_by_calls'] for r in rs)} | {sum(r['group_by_calls']>0 for r in rs)}/54 | {sum(r['group_base_scope_calls'] for r in rs)} | "+' | '.join(str(sum(r[k] for r in rs)) for k in ['same_keys_pairs','refinement_pairs','coarsening_pairs','sibling_pairs','predicate_change_pairs'])+' |')
 lines += ['', '演化不自动等于可复用：筛选不同、Join 不同、DISTINCT/不可合并聚合、Top-K 截断均会改变条件。细粒度到粗粒度需保存足够状态；反方向不能仅从已有粗粒度结果恢复细节。任意两个基表集合相同的查询不算相同输入。CTE/派生输入、外连接、自连接及复杂分组暂未做完整血缘演化识别；因此下表是支持范围内的计数，不能据零断言不存在。', '',
 '**本节结论：** GROUP BY 在任务中并不少见，但在已覆盖的基表输入范围内，尚未观察到分组键严格包含的细化或粗化；已识别的变化包括同分组键下改变筛选条件，以及少量 sibling exploration。因此目前不支持“Agent 普遍逐级细化分组”的判断。聚合优化仍可围绕同键共享状态、多条件聚合和 sibling 的共同准备展开，但需验证输入语义及成本，且不能将当前零计数推广到未覆盖的复杂输入。', '',
 '## RQ4 — Result Dependency','',
 '在相邻成功 SQL 对中，将后序 WHERE 的直接 column=literal、column IN(literals) 与前序保存的完整结果单元格匹配，保持类型及值；记录结果行号、列名、SQL 文件。仅字符串或数值常量，暂不推导范围谓词、函数转换、Python 派生值、Mongo→SQL、跨多个请求的依赖。多语句生产者排除。', '',
 '| 组 | 相邻对分母 | 至少一项结果值匹配的对 | 涉及任务 | 新值匹配对* |', '|---|---:|---:|---:|---:|']
 for g in ['natural','fad']:
  ps=[x for x in adj if x['group']==g];ds=[x for x in deps if x['group']==g];pairs={(x['task'],x['producer'],x['consumer']) for x in ds};new={(x['task'],x['producer'],x['consumer']) for x in ds if x['new_in_sql_predicates'] and not x['literal_text_in_prompt']}
  lines.append(f"| {g} | {len(ps)} | {len(pairs)} | {len({x['task'] for x in ds})} | {len(new)} |")
 lines += ['', '*新值仅指：此前 SQL 的同类谓词中未出现，且任务 prompt 未包含该值文本；不是世界知识新颖性或因果依赖证明。0/1、年份、常见类别等可以偶合；值匹配不证明模型读取并使用了结果。该实验也不能据此证明 future SQL 在 Q1 前不可能知道，或证明方案 novelty。需要结合轨迹人工核对，再用隐藏/扰动结果的对照实验建立更强依赖证据。', '',
 '人工核对实例：agnews/query2 的 FAD 轨迹先[按 Amy Jones 查作者 ID](../../runs/fad/agnews/query2/full-01/sql/003-fc15464eda3949649d0d46f4187aa5ad.sql)，[结果](../../runs/fad/agnews/query2/full-01/results/fc15464eda3949649d0d46f4187aa5ad.json)为 `author_id=218`，随后[按 author_id=218 查文章](../../runs/fad/agnews/query2/full-01/sql/004-38cd4fc28cc34d239cf6fb5cbc0a4094.sql)。这是明确的“姓名→数据 ID→下一条查询筛选”的轨迹证据；仍不等于反事实意义上证明模型提前无法知道 ID。', '',
 '**本节结论：** 两组均发现了前序结果值进入后序谓词的匹配，并有“姓名→作者 ID→文章筛选”的具体轨迹实例，支持“部分后续 SQL 参数随查询结果逐步确定”的研究假设。不过，自动值匹配可能包含巧合，尚不能仅凭该统计证明完整 future SQL 提前不可知或证明方案 novelty；更强结论需要逐例核对及结果隐藏／扰动实验。', '',
 '## RQ5 — Cross-query Optimization Opportunity','',
 'ME 在此定义为 materialization candidate（共同准备对象候选）。保留公共筛选、完整公共内连接、标量子表达式、同输入聚合状态；新增同输入但分组键/指标不同的聚合 MV 候选：按分组键并集准备可合并状态，再服务各消费者。计入“可共享的子计算”，不宣称 MV 单独回答完整 SQL。','',
 '| 组 | 候选对象组 | 涉及任务 | MV Coverage：调用/成功 SQL | 后续调用覆盖 | Expected Reuse 中位数 | 后续可用≥2 次的对象组 |', '|---|---:|---:|---|---:|---:|---:|']
 for g in ['natural','fad']:
  xs=[c for c in cs if c['group']==g];rs=[r for r in runs if r['group']==g];covered={(c['task'],cid) for c in xs for cid in c['call_ids']};later={(c['task'],cid) for c in xs for cid in c['call_ids'][1:]};den=sum(r['successful_sql'] for r in rs)
  lines.append(f"| {g} | {len(xs)} | {len({c['task'] for c in xs})} | {len(covered)}/{den} ({pct(len(covered),den)}) | {len(later)} | {statistics.median([c['expected_reuse'] for c in xs]) if xs else '—'} | {sum(c['expected_reuse']>=2 for c in xs)} |")
 lines += ['', '| Build-vs-Reuse 筛查 | 有完整时延记录的候选 | 乐观增量构建预算上界中位数（ms） | 上界不足 100ms 的候选 |', '|---|---:|---:|---:|']
 for g in ['natural','fad']:
  xs=[c for c in cs if c['group']==g and c['timing_complete']];vs=[c['optimistic_incremental_build_budget_ms'] for c in xs]
  lines.append(f"| {g} | {len(xs)} | {fmt(statistics.median(vs) if vs else None)} | {sum(v<100 for v in vs)} |")
 lines += ['', '上界采用各候选后续消费者的原始 execute+fetch 耗时之和，假设后续全部计算成本均可消除、MV 查询零成本。这是非常乐观的筛查上界，不是实际构建成本或预期收益；只覆盖已记录的数据库执行与取数计时，受并发/cache 状态影响，不含 JSON 序列化等环节。不同候选重叠，预算不可相加。', '',
 'Expected Reuse = 已观察轨迹中首次使用后的可用调用数（不是概率期望），不要求连续；同一消费者内多个作用域只算一次。MV Coverage 在任务内去重，再相加；不同候选可能重叠或互为替代，候选组数不能相加解释为独立优化数。', '',
 '**Build-vs-Reuse：尚无实测净收益。** 每个候选保存消费者已记录的 execute+fetch 时间作为原查询基线，build_ms/reuse_ms 留空。判断式为 `增量构建成本 + 维护/存储成本 < Σ后续查询(原成本 − 使用MV后的成本)`；若构建替代首次查询，应扣除被替代部分。不能把 SQL 总耗时当作可消除的聚合耗时，也不能把 Agent 思考时间算数据库收益。当前缺少 MV 构建及改写查询实测，不能报告加速比或盈亏平衡点。', '',
 '聚合 MV 须保存完整分组：SUM/COUNT 可再求和，MIN/MAX 可再归并，AVG 保留 SUM 与非 NULL COUNT；不直接平均平均数。不自动支持 COUNT DISTINCT。细粒度并集可能接近基表大小，FILTER/空分组/NULL/类型及每个消费者的 HAVING/LIMIT 必须在改写验证中处理。', '',
 '**本节结论：** 静态共享计算候选覆盖了两组约四分之一至三成的成功 SQL 调用，但覆盖仅表示其中存在潜在共享子计算。候选首次后的可用次数中位数为 1，乐观增量构建预算上界的中位数也仅为几十毫秒，因此“有机会”尚不足以说明“值得物化”。后续应优先验证原计算较贵、后续复用较多的任务内候选，通过实际构建和查询改写测量净收益。', '',
 '## 逐任务总表','', '所有数字均来自本任务本组。R/P/J 是相邻对命中数；演化是全部前后调用对；依赖是相邻值匹配对；这几种分母不可混用。','',
 '| 任务 | 组 | 验证 | SQL尝试/成功 | GROUP BY调用 | 相邻对 | R/P/J命中 | 同键/细化/粗化/sibling | 结果匹配对 | MV覆盖调用 |', '|---|---|---|---|---:|---:|---|---|---:|---:|']
 for r in sorted(runs,key=lambda r:(r['task'],r['group'])):
  lines.append(f"| {r['task']} | {r['group']} | {'✓' if r['validated'] else '✗'} | {r['sql_attempt_calls']}/{r['successful_sql']} | {r['group_by_calls']} | {r['adjacent_pairs']} | {r['relation_overlap_pairs']}/{r['predicate_overlap_pairs']}/{r['join_overlap_pairs']} | {r['same_keys_pairs']}/{r['refinement_pairs']}/{r['coarsening_pairs']}/{r['sibling_pairs']} | {r['result_match_pairs']} | {r['mv_covered_calls']} |")
 lines+=['',f'分析异常记录 {len(issues)} 条，详见 [analysis-issues.json](analysis-issues.json)。不完整结构绑定不影响原始 SQL 执行成功的计数。', '',
 '[逐任务 CSV](task-characterization.csv) · [相邻对](adjacent-pairs.json) · [分组演化](group-evolution.json) · [结果值依赖证据](result-dependencies.json) · [物化候选](materialization-candidates.json) · [可读实例与原始 SQL](EVIDENCE.md)']
 (OUT/'REPORT.md').write_text('\n'.join(lines)+'\n')
 evidence=['# 逐项证据','', '下列证据均在各自任务、组内部。候选和数值匹配尚非语义改写或因果验证。','', '## 分组演化','']
 for x in ev:
  evidence += [f"- {x['task']} / {x['group']} / {x['kind']} / 同筛选={x['same_predicates']}：`{x['before_keys']}` → `{x['after_keys']}`；[前序](../../{x['producer_sql']}) → [后序](../../{x['consumer_sql']})"]
 evidence+=['','## 结果值匹配（每个查询对最多展示 3 个值，JSON 保留全部）','']
 counts=collections.Counter()
 for x in deps:
  key=(x['task'],x['group'],x['producer'],x['consumer']);counts[key]+=1
  if counts[key]>3:continue
  evidence.append(f"- {x['task']} / {x['group']}：结果列 `{x['result_column']}` 第 {x['row_index']} 行值 `{x['value']}` 匹配后序 `{x['predicate_column']}`；[前序](../../{x['producer_sql']}) → [后序](../../{x['consumer_sql']})。新谓词值={x['new_in_sql_predicates']}，prompt含值={x['literal_text_in_prompt']}。")
 evidence+=['','## 共同准备候选','']
 for c in cs:
  evidence += [f"### {c['id']} · {c['task']} · {c['group']} · {c['kind']}",'',f"使用 {c['consumer_count']} 次，首次后 {c['expected_reuse']} 次；仅共享子计算候选。",'','```',c['input'],'\n'.join(c.get('group_keys',[])),'\n'.join(c.get('aggregates',c.get('objects',[]))),'```','',
   ' → '.join(f'[{Path(p).name.split("-")[0]}](../../{p})' for p in c['sql_files']),'',c['limitations'],'']
 (OUT/'EVIDENCE.md').write_text('\n'.join(evidence)+'\n')

if __name__=='__main__':main()
