"""User-defined metric: a FAD hits if any explicitly predicted item is used later.
Run with benchmark/dacomp/.venv/bin/python from repo root.
"""
import ast,json,re,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parent
sys.path.insert(0,str(ROOT.parents[4]))
from agent_db_tool.matching import key
from sqlglot import Tokenizer,TokenType
for node in ast.parse((ROOT/'pair_evidence.py').read_text()).body:
 if isinstance(node,ast.FunctionDef) and node.name=='pretty':exec(compile(ast.Module(body=[node],type_ignores=[]),'<display>','exec'))
FIELDS=('columns','group_by','aggregations','filters','joins')
LABEL={'columns':'列','group_by':'分组','aggregations':'聚合','filters':'过滤','joins':'连接'}
def ratio(n,d):return f'{n}/{d} = {100*n/d:.1f}%' if d else '未提供'
def display(f,item):
 if f=='columns':return item
 x=json.loads(item)
 if f=='group_by':return ' ＋ '.join(g[1]+('（按'+{'month':'月','year':'年','day':'日'}[g[2]]+'）' if g[0]=='time_bucket' else '') for g in x)
 if f=='aggregations':return x[0].upper()+'('+x[1]+')'
 if f=='filters':return x[1]+' '+x[2]+' '+json.dumps(x[3],ensure_ascii=False)
 return x[0]+'：'+x[1][0]+' = '+x[1][1]
def actual_items(f,a):
 if f=='joins':return {key((json.loads(j)[0],p)) for j in a['joins'] for p in json.loads(j)[1]}
 return set(a[f])

def compute(task):
 d=json.loads((ROOT/f'dacomp-{task}-02.json').read_text())
 events=[json.loads(x) for x in (ROOT.parent/'runs'/f'dacomp-{task}-02/events.jsonl').read_text().splitlines()]
 reqs=[e for e in events if e['record']=='request'];sql={r['step_id']:r['arguments']['sql'] for r in reqs}
 qs={int(q):a for q,a in d['sql_features'].items()};rounds=[]
 for req in reqs:
  step=req['step_id'];rows=[r for r in d['rows'] if r['step']==step];unique={};candidates=[]
  for row in rows:
   items=[]
   for f in FIELDS:
    predicted=row['fields'][f]['items']
    if f=='group_by':predicted=[key([json.loads(v) for v in sorted(predicted)])] if predicted else []
    elif f=='joins':predicted=sorted({key((json.loads(j)[0],p)) for j in predicted for p in json.loads(j)[1]})
    for item in predicted:
     hits=[]
     for q,a in qs.items():
      if q<=step:continue
      if f=='group_by':yes=any({key(v) for v in json.loads(item)}<=set(g) for g in a['group_sets'])
      else:yes=item in actual_items(f,a)
      if yes:hits.append(q)
     entry={'field':f,'item':item,'description':display(f,item),'queries':sorted(hits)}
     items.append(entry);unique[(f,item)]=entry
   candidates.append({'candidate':row['candidate'],'hit':any(i['queries'] for i in items),'items':items})
  rounds.append({'step':step,'has_prediction':bool(rows),'hit':any(i['queries'] for i in unique.values()),
                 'items':list(unique.values()),'candidates':candidates})
 counts={f:{'predicted':sum(i['field']==f for r in rounds for i in r['items']),
              'hit':sum(i['field']==f and bool(i['queries']) for r in rounds for i in r['items'])} for f in FIELDS}
 nonempty=sum(r['has_prediction'] for r in rounds);hits=sum(r['hit'] for r in rounds)
 out={'task':task,'criterion':'any explicit item used by a later successful SQL; FAD-level',
      'fad_count':len(rounds),'nonempty_fad_count':nonempty,'empty_fad_count':len(rounds)-nonempty,
      'fad_hits':hits,'fad_hit_rate':hits/nonempty if nonempty else None,'all_calls_hit_rate':hits/len(rounds),
      'candidate_count':sum(len(r['candidates']) for r in rounds),
      'candidate_hits':sum(c['hit'] for r in rounds for c in r['candidates']),
      'field_items':counts,'rounds':rounds}
 return out,sql,qs

old=(ROOT/'REPORT.md').read_text()
intro=old.split('<a id="task-003">')[0]
intro=re.sub(r'\n\*\*本次命中口径：.*?\*\*\n*','\n',intro)
# Keep one report, current runs only, task-local presentation.
intro += '\n**本次命中口径：一份FAD中任意一项明确预测被后续成功SQL使用，就算这份FAD命中。不同信息可以在不同SQL中使用。下面已替换旧的“全部信息必须共同出现”口径。**\n\n'
parts=[intro];allstats=[]
for task in ('003','004','005','006'):
 out,sql,qs=compute(task);allstats.append(out)
 section=old.split('## DAComp-'+task+'：')[1].split('\n<a id="task-')[0]
 title=section.splitlines()[0]
 notes=section.split('<!-- task-notes-start -->',1)[1].split('<!-- task-notes-end -->',1)[0] if '<!-- task-notes-start -->' in section else ''
 notes=notes.replace('### 具体操作的差异与遗漏','').replace('下面保留操作细节分析。“某项操作未发生”不等于整份FAD未命中；整份FAD只要其他信息被使用，就已命中。','')
 # Old bundle counts and interpretations no longer define success.
 notes=notes.split('### 本题分组和聚合的数量')[0]
 notes=notes.replace('这条访问预测没有发生。Year被用到，不等于GROUP BY Year被预测正确','Year后来作为地区＋年份联合分组的维度被使用，按本次口径分组项命中；但两项用水SUM没有发生')
 notes=notes.replace('预测没有发生 |','这两项均值未命中，但这份FAD仍可能因列或连接被使用而命中 |')
 lines=[f'<a id="task-{task}"></a>','',f'## DAComp-{task}：{title}','','### 本题命中率','',
  '**一份FAD有任意一项被后续SQL用到，就记为命中。** 没提供预测的FAD单列，不混入“有预测的FAD命中率”；同时给出占全部提交的比例。','',
  '| 统计内容 | 结果 |','|---|---|',
  f'| 共提交FAD | {out["fad_count"]}份 |',f'| 有预测 / 没提供预测 | {out["nonempty_fad_count"]}份 / {out["empty_fad_count"]}份 |',
  f'| **有预测的FAD命中率** | **{ratio(out["fad_hits"],out["nonempty_fad_count"])}** |',
  f'| 命中份数占全部提交 | {ratio(out["fad_hits"],out["fad_count"])} |',
  '', '**候选访问预测的命中情况：** 每个候选中任意一项明确预测被后续SQL使用，该候选就算命中。一份FAD可以有多个候选，所以与上面的FAD份数分别统计。','',
  '| 统计内容 | 结果 |','|---|---|',
  f'| 候选总数 | {out["candidate_count"]}个 |',
  f'| 命中的候选 | {out["candidate_hits"]}个 |',
  f'| 未命中的候选 | {out["candidate_count"]-out["candidate_hits"]}个 |',
  f'| **候选命中率** | **{ratio(out["candidate_hits"],out["candidate_count"])}** |','',
  '**具体预测信息用了多少：** 同一份FAD中重复出现的同类信息只计一次，不同轮次重复预测分别计数。列、聚合、过滤条件、连接等值条件分别逐项数；联合分组作为一项，所列维度需在后续某个分组中一起使用，允许实际增加维度。','',
  '| 信息类别 | 提前写了多少项 | 后来使用了多少项 | 比例 |','|---|---:|---:|---|']
 for f in FIELDS:
  c=out['field_items'][f];lines.append(f'| {LABEL[f]} | {c["predicted"]} | {c["hit"]} | {ratio(c["hit"],c["predicted"])} |')
 lines += ['',
  '命中一列就足以让该份FAD命中，并不意味着其中所有分组、聚合都对。上表用来区分“有用到一点”与“具体信息用了多少”。过滤按已知条件项匹配，连接按类型＋等值条件匹配；复杂表达式无法自动确认的部分保留在具体分析中。','',
  '### 逐轮FAD与后续query','']
 for r in out['rounds']:
  step=r['step'];n=len(r['candidates']);future=sorted(q for q in qs if q>step)
  status='命中' if r['hit'] else '未命中' if r['has_prediction'] else '未提供预测'
  lines += [f'#### Q{step}：{status}（{n}项候选访问预测）','',
    '<details><summary>当前执行的SQL</summary>','','```sql',pretty(sql[step]),'```','','</details>','']
  used=set()
  if not n:
   lines+=['没有提供未来访问预测。'+('之后仍执行了'+ '、'.join('Q'+str(q) for q in future)+'。' if future else '之后没有再查询。'),'']
  for c in r['candidates']:
   lines += [f'##### 候选{c["candidate"]}：'+('命中' if c['hit'] else '未命中'),'','| 预测的信息 | 后续实际使用它的query |','|---|---|']
   for item in c['items']:
    hits=item['queries'];used.update(hits)
    target='、'.join(f'[Q{q}](#t{task}-from{step}-sql{q})' for q in hits) if hits else '未找到'
    lines.append('| '+LABEL[item['field']]+'：'+item['description'].replace('|','&#124;')+' | '+target+' |')
   lines.append('')
  if used:
   lines += ['##### 后续SQL原文','']
   for q in sorted(used):
    lines += [f'<a id="t{task}-from{step}-sql{q}"></a>',f'<details><summary>Q{q}：实际SQL</summary>','','```sql',pretty(sql[q]),'```','','</details>','']
  elif future:
   lines += ['##### 后续SQL原文','']
   for q in future:lines += [f'<details><summary>Q{q}：实际SQL</summary>','','```sql',pretty(sql[q]),'```','','</details>','']
 lines += ['<!-- task-notes-start -->','### 具体操作的差异与遗漏','',
 '下面保留操作细节分析。“某项操作未发生”不等于整份FAD未命中；整份FAD只要其他信息被使用，就已命中。','',notes.strip(),'<!-- task-notes-end -->','',
 f'原始数据：[events.jsonl](../runs/dacomp-{task}-02/events.jsonl)。本次逐项命中记录：[item-hit-rates.json](item-hit-rates.json)。','']
 parts+=lines
 print(task,'FAD',ratio(out['fad_hits'],out['nonempty_fad_count']),'all calls',ratio(out['fad_hits'],out['fad_count']),'items',out['field_items'])
(ROOT/'item-hit-rates.json').write_text(json.dumps(allstats,ensure_ascii=False,indent=2)+'\n')
(ROOT/'REPORT.md').write_text('\n'.join(parts))
