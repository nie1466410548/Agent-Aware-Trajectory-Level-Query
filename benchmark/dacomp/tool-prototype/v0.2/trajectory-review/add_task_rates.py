"""Add per-task counts/rates to the one report; preserve underlying experiments."""
import json,re
from pathlib import Path
ROOT=Path(__file__).resolve().parent
OPS=('filters','joins','group_by','aggregations')
def pct(n,d):return f'{n}/{d} = {100*n/d:.1f}%' if d else '没有这种候选'
def summarize(task):
 d=json.loads((ROOT/f'dacomp-{task}-02.json').read_text())
 events=[json.loads(x) for x in (ROOT.parent/'runs'/f'dacomp-{task}-02/events.jsonl').read_text().splitlines()]
 reqs=[x for x in events if x['record']=='request'];results=[]
 for row in d['rows']:
  fs=row['fields'];ops=[f for f in OPS if fs[f]['items']]
  named=[f for f in ('columns',*OPS) if fs[f]['items']]
  hits=set.intersection(*(set(fs[f]['later_queries']) for f in named)) if named else set()
  if 'group_by' in ops and 'aggregations' in ops:
   gs=set(fs['group_by']['items']);ag=set(fs['aggregations']['items'])
   hits={q for q in hits if any((gs==set(s['group_by']) if row['fad']['group_by']['status']=='known' else gs<=set(s['group_by'])) and ag<=set(s['aggregations']) for s in d['sql_features'][str(q)]['scopes'])}
  # Partial = at least one explicitly stated column/op item occurs later, but not the entire bundle.
  some=False
  for q,actual in d['sql_features'].items():
   if int(q)<=row['step']:continue
   for f in ('columns',*OPS):
    values=set().union(*(set(g) for g in actual['group_sets'])) if f=='group_by' else set(actual[f])
    some=some or bool(set(fs[f]['items'])&values)
  label='all_stated_matched' if hits else 'part_matched' if some else 'none_matched'
  results.append({'step':row['step'],'candidate':row['candidate'],'has_operation':bool(ops),'result':label,'evidence_sql':sorted(hits)})
 n=len(results);full=sum(r['result']=='all_stated_matched' for r in results);partial=sum(r['result']=='part_matched' for r in results)
 nonempty=len({r['step'] for r in results});empty=len(reqs)-nonempty
 ops=[r for r in results if r['has_operation']];cols=[r for r in results if not r['has_operation']]
 out={'task':task,'fad_calls':len(reqs),'fad_with_candidates':nonempty,'empty_fad_calls':empty,'candidates':n,
      'all_stated_matched':full,'part_matched':partial,'none_matched':n-full-partial,'candidate_success_rate':full/n,
      'operation_candidates':len(ops),'operation_success':sum(r['result']=='all_stated_matched' for r in ops),
      'columns_only_candidates':len(cols),'columns_only_success':sum(r['result']=='all_stated_matched' for r in cols),'candidate_evidence':results}
 lines=['<!-- task-rates-start -->','### 本题数量与预测成功比例','',
  '**计数单位：一轮SQL附带一份FAD，一份FAD可以包含多个候选。预测成功比例按候选算。**',
  '这里“成功”采用统一的保守标准：候选明确写出的列、过滤条件、连接、分组和聚合，能在某条严格后续成功SQL中一起找到；如果同时写了分组和聚合，它们还需要出现在同一个查询层。只说对其中一部分，单独计为部分对应。没有候选的FAD不进入候选成功率分母。','',
  '| 统计内容 | 本题结果 |','|---|---|',
  f'| 共提交多少份FAD | {len(reqs)}份 |',
  f'| 其中有候选 / 没有候选 | {nonempty}份 / {empty}份 |',
  f'| 共提出多少个候选 | {n}个 |',
  f'| **候选预测成功：已写信息全部对应** | **{full}个，{pct(full,n)}** |',
  f'| 只对应一部分 | {partial}个，{pct(partial,n)} |',
  f'| 已写内容都没找到后续对应 | {n-full-partial}个，{pct(n-full-partial,n)} |',
  f'| 写了具体操作的候选，其已写信息全部对应 | {pct(out["operation_success"],len(ops))} |',
  f'| 只列字段、没写具体操作的候选，其列清单全部对应 | {pct(out["columns_only_success"],len(cols))} |','',
  '**分开看各字段的预测比例：**','',
  '| 预测内容 | 写了多少个候选 | 其中多少个后来对应 | 比例 |','|---|---:|---:|---:|']
 for f,label in [('columns','列清单（包括操作里引用的列）'),('filters','已知过滤条件'),('joins','连接'),('group_by','分组'),('aggregations','聚合')]:
  c=d['counts'][f];total=c.get('stated',0);hit=c.get('later_occurred',0)
  lines.append(f'| {label} | {total} | {hit} | {pct(hit,total)} |')
 lines+=['',
 '分项比例只判断该字段；候选成功率要求这些信息在同一条后续SQL里共同出现，所以通常更低。只列字段的成功不表示预测了查询操作，已在上表单列。none/unknown不作为已写出的操作项计分；因此成功只表示已写信息对应，不表示完整预测了后续SQL全部内容。',
 '同一候选在多轮重复提交会重复计数，多个候选也可能对应同一条后续SQL。复杂表达式与近似方向的人工解释保留在下文；自动过滤匹配仅检查已知条件单项，以上是统一规则下的对应比例，不是完整SQL语义等价率。',
 f'逐候选分类及对应SQL编号保存在[比例复核数据](task-rates.json)的{task}项。','<!-- task-rates-end -->','']
 return out,'\n'.join(lines)
report=(ROOT/'REPORT.md').read_text();report=re.sub(r'<!-- task-rates-start -->.*?<!-- task-rates-end -->\n*','',report,flags=re.S)
allstats=[]
for task in ('003','004','005','006'):
 stats,block=summarize(task);allstats.append(stats)
 start=report.index('## DAComp-'+task+'：');pos=report.index('### 1.',start)
 report=report[:pos]+block+'\n'+report[pos:]
 print(task,'FAD',stats['fad_calls'],'candidates',stats['candidates'],'success',pct(stats['all_stated_matched'],stats['candidates']),'partial',stats['part_matched'])
(ROOT/'REPORT.md').write_text(report)
(ROOT/'task-rates.json').write_text(json.dumps(allstats,ensure_ascii=False,indent=2)+'\n')
