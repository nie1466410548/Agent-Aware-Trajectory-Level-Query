"""One report, task by task, every FAD round and all matching future queries."""
import json,re,ast
from pathlib import Path
from sqlglot import Tokenizer,TokenType
ROOT=Path(__file__).resolve().parent
OPS=('filters','joins','group_by','aggregations')
LABEL={'columns':'列清单','filters':'过滤','joins':'连接','group_by':'分组','aggregations':'聚合'}
# Reuse display-only helpers, without executing the old example-based generator.
tree=ast.parse((ROOT/'pair_evidence.py').read_text())
for node in tree.body:
 if isinstance(node,ast.FunctionDef) and node.name in ('pretty','format_fad','evidence'):
  exec(compile(ast.Module(body=[node],type_ignores=[]),'<display-helper>','exec'))
report=(ROOT/'REPORT.md').read_text()
rates={x['task']:x for x in json.loads((ROOT/'task-rates.json').read_text())}
new=[report.split('<a id="task-003">')[0].rstrip(),'']
for task in ('003','004','005','006'):
 start=report.index('## DAComp-'+task+'：');end=report.find('\n<a id="task-',start)
 section=report[start:end if end>=0 else len(report)]
 first=section.find('### 1.')
 if first<0:first=section.index('### 逐轮FAD与后续query核对')
 prefix=section[:first].rstrip()
 if '### 2.' in section:
  notes=section[section.index('### 2.'):section.index('### 7.')]
 else:
  marker='<!-- task-notes-start -->'
  notes=section.split(marker,1)[1].split('<!-- task-notes-end -->',1)[0] if marker in section else ''
 notes=re.sub(r'^### \d+\. ', '### ',notes,flags=re.M).replace('第2节','本题补充分析')
 d=json.loads((ROOT/f'dacomp-{task}-02.json').read_text())
 es=[json.loads(x) for x in (ROOT.parent/'runs'/f'dacomp-{task}-02/events.jsonl').read_text().splitlines()]
 reqs=[x for x in es if x['record']=='request'];sqls={x['step_id']:x['arguments']['sql'] for x in reqs}
 qs={int(q):s for q,s in d['sql_features'].items()}
 statuses={(r['step'],r['candidate']):r for r in rates[task]['candidate_evidence']}
 lines=[f'<a id="task-{task}"></a>','',prefix,'','### 逐轮FAD与后续query核对','',
 '从Q1开始逐轮列出全部候选；不是选例子。每个候选列出所有完整对应的后续query，部分对应按字段单独列出。本轮涉及的后续SQL原文紧接在候选后面，同一条SQL在本轮内只展示一次。SQL可展开查看。','']
 for req in reqs:
  step=req['step_id'];rows=[r for r in d['rows'] if r['step']==step];future=sorted(q for q in qs if q>step)
  lines += [f'#### Q{step}：本轮FAD（{len(rows)}个候选）','',
   '<details><summary>当前执行的SQL</summary>','','```sql',pretty(sqls[step]),'```','','</details>','']
  evidence_queries=set()
  if not rows:
   raw=req['arguments']['future_access'];h=json.loads(raw) if isinstance(raw,str) else raw
   lines += ['**本轮FAD：** `'+json.dumps(h,ensure_ascii=False)+'`','']
   if future:
    lines += ['**判断：没有提供后续访问候选，但之后仍执行了'+ '、'.join('Q'+str(q) for q in future)+'。**','']
    evidence_queries.update(future)
   else:lines += ['**判断：之后没有再执行SQL，与结束判断一致。**','']
  for r in rows:
   stat=statuses[(step,r['candidate'])];full=stat['evidence_sql'];fields=r['fields']
   label={'all_stated_matched':'已写信息全部对应','part_matched':'部分对应，整个候选未命中','none_matched':'没有找到对应内容'}[stat['result']]
   lines += [f'##### 候选{r["candidate"]}：{label}','','**对后续查询的预测：**','',format_fad(r['fad']),'',
    '**整个候选对应的后续query：** '+('、'.join('Q'+str(q) for q in full) if full else '无')+'。','',
    '| FAD中的信息 | 后续哪些query对应了这一整项 |','|---|---|']
   evidence_queries.update(full)
   for f in ('columns',*OPS):
    v=fields[f];hits=v['later_queries']
    if not v['items']:message='未提供具体项，不算预测成功'
    elif hits:message='、'.join(f'[Q{q}](#t{task}-from{step}-sql{q})' for q in hits);evidence_queries.update(hits)
    else:message='没有；后续SQL未完整包含这一项所述内容'
    lines.append('| '+LABEL[f]+' | '+message+' |')
   if not full and stat['result']=='part_matched':
    # Include partial item overlaps even when no entire field bundle matches.
    overlaps=[]
    for q in future:
     common=sorted(set(fields['columns']['items'])&set(qs[q]['columns']))
     if common:overlaps.append((q,common));evidence_queries.add(q)
    lines += ['','**部分对应的具体列：** 下面只表示这些列确实被访问，不代表分组、聚合或整个候选成功。','',
              '| 后续query | 与本候选相同的已写列 |','|---|---|']
    for q,cols in overlaps:lines.append(f'| [Q{q}](#t{task}-from{step}-sql{q}) | '+', '.join(cols)+' |')
   lines.append('')
  if evidence_queries:
   lines += ['##### 本轮FAD对应的后续SQL原文','',
    '对应关系见上面各候选的表格；以下既包含完整命中的证据，也包含部分字段对应的证据，不能仅凭SQL出现在这里就算整个候选命中。','']
   for q in sorted(evidence_queries):
    assert q>step
    lines += [f'<a id="t{task}-from{step}-sql{q}"></a>',f'<details><summary>后续Q{q}：实际SQL</summary>','',
              '```sql',pretty(sqls[q]),'```','','</details>','']
  elif future:
   lines += ['**未找到匹配。剩余实际query为：** '+ '、'.join('Q'+str(q) for q in future)+'。','']
   for q in future:lines += [f'<details><summary>未匹配的后续Q{q}：实际SQL</summary>','','```sql',pretty(sqls[q]),'```','','</details>','']
 lines += ['<!-- task-notes-start -->',notes.strip(),'<!-- task-notes-end -->','',
  f'原始记录：[events.jsonl](../runs/dacomp-{task}-02/events.jsonl)；本题复核数据：[JSON](dacomp-{task}-02.json)。','']
 new += lines
(ROOT/'REPORT.md').write_text('\n'.join(new))
print('Saved one report with every round, every candidate, and all corresponding later queries.')
