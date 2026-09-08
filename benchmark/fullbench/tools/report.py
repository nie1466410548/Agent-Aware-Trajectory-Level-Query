"""Render the agreed task-first tables; incomplete episodes are never shown as zero."""
import collections,csv,json,statistics,hashlib
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
LABELS={'filter':'公共筛选','join':'公共内连接','derived':'派生计算','aggregate_state':'同输入同分组聚合状态','mongo_filter':'Mongo 公共筛选'}
RULES=[('验证','结束后原始 benchmark 验证器是否通过；未通过不等于 SQL 执行失败。'),
('成功 SQL','成功执行的数据查询调用数，排除元数据和失败尝试；多语句仍计一次。'),
('同表','与本任务同组同库的至少一个前序成功查询共享基表。'),
('同表列','共享具体 (基表,列)，按 schema 展开 SELECT *，包含过滤/连接等列；COUNT(*) 不视为所有列。'),
('WHERE 合取项','将 WHERE 按 AND 拆分、绑定基表并归一表达式后匹配相同项，保留常量。'),
('Join 片段','基表别名归一后相同 Join 节点；不保证左输入、完整中间结果或可复用性。'),
('聚合表达式','相同基表集合中有相同聚合表达式；不要求分组、过滤或输入行相同，不是聚合复用次数。'),
('GROUP BY','相同基表集合中有相同完整 GROUP BY 结构；不是含分组的调用总数。'),
('相同结果行','同库共享表、输出列名相同时，实际 JSON 行值集合有交集；忽略行序/重复次数，多语句调用排除。')]
def pct(x):return '—' if x is None else f'{x:.1%}'
def mean(v):return statistics.mean(v) if v else None

def main():
 tasks=json.loads((ROOT/'tasks.json').read_text())['tasks'];expected=2*sum(map(len,tasks.values()))
 raw=json.loads((ROOT/'reports/overlap-detail.json').read_text());rs={(r['task'],r['group']):r for r in raw['runs']}
 a=json.loads((ROOT/'reports/analysis.json').read_text());op=json.loads((ROOT/'reports/opportunities.json').read_text());cs=op['candidates']
 reviews=json.loads((ROOT/'reports/trace-review.json').read_text()) if (ROOT/'reports/trace-review.json').exists() else {}
 status=f"**进度：{len(rs)}/{expected} 次运行已结束。{'全量运行已结束。' if len(rs)==expected else '这是阶段性报告，尚未完成的调用不计入统计。'}**"
 lines=['# 全量任务：查询重叠与潜在共同优化机会','',status,'',
 '正式清单为 12 个数据集、54 个任务，每题自然/FAD 各一次。任务与数据均固定版本，旧 9 题试跑不混入本组。','',
 '## 统计规则','',
 '依据原始 SQL、执行状态、schema 和保存结果离线比较。只在同一任务、同一组、同一库内比较前后成功数据调用。不使用性能数据证明复用。', '',
 '| 列 | 具体规则 |','|---|---|']
 lines += ['| '+k+' | '+v+' |' for k,v in RULES]
 quota_file=ROOT/'reports/quota-interruption.json'
 if quota_file.exists():
  quota=json.loads(quota_file.read_text())
  lines += ['', f"运行记录：Kimi 曾返回 5 小时用量额度限制；首批 {len(quota['affected'])} 次受影响尝试已单独归档并排除主统计，额度恢复后补跑。正常答题失败仍保留，不因验证结果重跑。详见 [额度中断记录](quota-interruption.json)。", '']
 lines += ['', '**从“同表”到“相同结果行”均按后续调用去重，列之间不可相加。** 同一后续调用与多个前序匹配也只算一次。若存在无法完整绑定的 SQL，对应任务计数标为 ≥（仅已解析部分），并列出覆盖数。Mongo 原生查询另表记录，不当作 SQL。','',
 '## 1. 逐任务查询统计','']
 keys=['table_any','column_bound','filter_atom','join_bound','aggregate_bound','group','result_row']
 flat=[]
 for ds,ids in tasks.items():
  lines += [f'### {ds}','', '| 任务 | 组 | 验证 | 成功 SQL | 同表 | 同表列 | WHERE 合取项 | Join 片段 | 聚合表达式 | GROUP BY | 相同结果行 | 分析覆盖 |',
    '|---|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---|']
  for i in ids:
   task=f'{ds}/query{i}'
   for g in ['natural','fad']:
    r=rs.get((task,g));name='自然' if g=='natural' else 'FAD'
    if not r:lines.append(f'| query{i} | {name} | 未完成 | — | — | — | — | — | — | — | — | — |');continue
    vals={k:len({p['consumer'] for p in r['pairs'] if k in p['metrics']}) for k in keys}
    prefix='≥' if r['errors'] else ''
    counts=' | '.join(prefix+str(vals[k]) for k in keys)
    lines.append(f"| [query{i}](../{r['analysis_path']}) | {name} | {'✓' if r['passed'] else '✗'} | {r['successful']} | {counts} | {r['analyzed_queries']}/{r['successful']} |")
    flat.append({'task':task,'group':g,'passed':r['passed'],'successful_sql':r['successful'],'analyzed_sql':r['analyzed_queries'],**vals})
  lines+=['']
 lines += ['## 2. 可提出具体准备方案的候选','',
 '自动候选采用比上表更严格的规则：同一基表上的相同筛选；完全相同基表输入/键/类型的内连接；同一基表列的相同非平凡派生表达式；或 FROM、WHERE、GROUP BY 全部相同的聚合状态。不同输入/分组的 COUNT 不算聚合复用。Mongo 仅识别相同集合的非空原生筛选。', '',
 '以下数的是候选对象组，同一种对象、相同输入和相同消费者集合中的多个表达式合并。不同种类可能是同一优化的替代方案，**不能把各类之和当成互不重复的优化数量**。覆盖调用按任务去重，可仅有部分子计算受益。尚未测加速、改写等价和 FAD 当时是否能提前给出信息。', '',
 '| 任务 | 组 | 公共筛选 | 公共内连接 | 派生计算 | 同输入聚合状态 | Mongo 筛选 | 涉及调用（去重） | 首次后仍有至少 2 次使用的对象组 | 证据 |',
 '|---|---|---:|---:|---:|---:|---:|---:|---:|---|']
 for (task,g),r in sorted(rs.items()):
  selected=[c for c in cs if c['task']==task and c['group']==g]
  count=collections.Counter(c['kind'] for c in selected);coverage=len({cid for c in selected for cid in c['call_ids']})
  counts=' | '.join(str(count[k]) for k in LABELS)
  links=' '.join(f"[{c['id']}](OPPORTUNITY_CASES.md#{c['id'].lower()})" for c in selected) or '未识别'
  lines.append(f"| {task} | {'自然' if g=='natural' else 'FAD'} | {counts} | {coverage} | {sum(c['later_count']>=2 for c in selected)} | {links} |")
 lines += ['', '候选只是在支持的 SQL 作用域内保守提取，不是所有优化机会的穷尽枚举；外连接、自连接、复杂派生输入等未自动合并。泛化全表缓存、任意索引建议和单纯同名函数不计入。', '',
 '[运行轮数及耗时](RUNS.md) · [MongoDB 调用](MONGO.md) · [FAD 统计](FAD.md) · [数据位置与规模](DATA.md) · [错误及解析覆盖](ERRORS.md) · [机器可读结构明细](overlap-detail.json) · [候选原文](opportunities.json)']
 (ROOT/'reports/OVERLAP.md').write_text('\n'.join(lines)+'\n')
 with (ROOT/'reports/task-overlap.csv').open('w') as f:
  if flat:w=csv.DictWriter(f,fieldnames=list(flat[0]));w.writeheader();w.writerows(flat)
 cases=['# 共同准备候选及原始请求','',status,'', '所有条目均为静态候选，未进行性能或改写验证。不同对象组可以重叠，不代表独立收益。','']
 for c in cs:
  cases += [f'<a id="{c["id"].lower()}"></a>',f"## {c['id']} · {c['task']} · {c['group']} · {LABELS[c['kind']]}",'',
    f"数据库：`{c['database']}`；任务验证：{'通过' if c['task_passed'] else '未通过'}；涉及 {c['consumer_count']} 次调用，首次之后 {c['later_count']} 次。",'',
    '共同输入：','```sql',c['relation'],'```','共同表达式/条件：','```', '\n'.join(c['objects']),'```','',
    '准备方式：'+c['preparation'],'','边界：'+c['limits'],'',
    '消费者：'+'、'.join(f"[{Path(p).name.split('-')[0]}](../{p})" for p in c['sql_files']),'']
 (ROOT/'reports/OPPORTUNITY_CASES.md').write_text('\n'.join(cases)+'\n')
 runlines=['# 运行、轮数和耗时','',status,'','轮数为可见 assistant 消息数（可在一轮内调用多个工具），不是成功收敛次数。验证失败也保留结束轮数。并发和服务波动影响耗时，不能用组间差异推断因果收益。','',
 '| 任务 | 组 | 验证 | assistant 轮数 | 数据 SQL 尝试 | 失败数据 SQL | 元数据 SQL | Mongo 数据请求 | FAD 提交 | 总秒数 | 超时 |','|---|---|---|---:|---:|---:|---:|---:|---:|---:|---|']
 for s in a['runs']:
  runlines.append(f"| {s['task_id']} | {s['group']} | {'✓' if s['validator_passed'] else '✗'} | {s['assistant_turns']} | {s['data_queries']} | {s['failed_data_queries']} | {s['metadata_queries']} | {s.get('mongo_queries',0)} | {s['fad_submissions']} | {s['duration_s']:.1f} | {s['timed_out']} |")
 (ROOT/'reports/RUNS.md').write_text('\n'.join(runlines)+'\n')
 native=['# MongoDB 原生查询','',status,'','Mongo 请求独立记录，不计入 SQL 表。集合重访按同任务同库此前成功原生数据请求去重；集合名相同不代表计算可复用。','',
 '| 任务 | 组 | 成功数据请求 | 失败数据请求 | 集合元数据请求 | 重访集合的后续请求 | 原始日志 |','|---|---|---:|---:|---:|---:|---|']
 errors=['# 失败、解析覆盖和审计','',status,'','验证失败是原始验证器结果，保留错误轨迹，不以重新作答提高通过率。未完成任务不等同失败。','']
 fadrows=[];order_checks=[]
 for r in raw['runs']:
  full=json.loads((ROOT/r['analysis_path']).read_text());mq=full.get('mongo_queries',[]);seen=set();revisit=0
  for q in mq:
   if q['metadata'] or not q['success']:continue
   atoms={(q['database'],t) for t in q['tables']}
   revisit+=bool(atoms&seen);seen|=atoms
  if mq:
   native.append(f"| {r['task']} | {r['group']} | {sum(q['success'] and not q['metadata'] for q in mq)} | {sum(not q['success'] and not q['metadata'] for q in mq)} | {sum(q['metadata'] for q in mq)} | {revisit} | [日志](../{Path(r['analysis_path']).parent}/tool_calls.jsonl) |")
  if r['errors']:errors += [f"## 结构解析：{r['task']} / {r['group']}",'','```json',json.dumps(r['errors'],ensure_ascii=False,indent=2),'```','']
  if not r['passed']:errors += [f"- {r['task']} / {r['group']}：{r['summary']['validator_reason']}"]
  flags=full['audit']['review_flags']
  for flag in flags:
   key=f"{r['group']}|{r['task']}|{flag['index']}";review=reviews.get(key)
   if review and review['command_sha256']==hashlib.sha256(flag['command'].encode()).hexdigest():
    errors += [f"- 已核对 {r['task']} / {r['group']} / 消息 {flag['index']}：{review['review']} [代码](../{review['script']})"]
   else:errors += [f"\n审计待核对 {r['task']} / {r['group']}：",'```json',json.dumps(flag,ensure_ascii=False,indent=2),'```']
  fadrows += [dict(f,task=r['task']) for f in full['fads'] if f['has_next_query'] and not f['targets_metadata']]
  order_checks += list(full['audit']['sql_order_checks'].values())
 if op['errors']:errors+=['','候选提取异常：','```json',json.dumps(op['errors'],ensure_ascii=False,indent=2),'```']
 provenance=ROOT/'reports/provenance-review.json'
 if provenance.exists():
  pv=json.loads(provenance.read_text());decisions=json.loads((ROOT/'reports/provenance-decisions.json').read_text()) if (ROOT/'reports/provenance-decisions.json').exists() else {}
  errors += ['', '## 扩展工具参数检查', '', f"检查 {pv['completed_reports_checked']} 次已结束运行的 {pv['assistant_messages_checked']} 条 assistant 消息及 {pv['saved_scripts_checked']} 个 Python 脚本。匹配路径/库名只是待核对线索，不是泄漏证明。", '', '[全部线索](provenance-review.json) · [人工核对记录](provenance-decisions.json)']
  for flag in pv['flags']:
   decision=decisions.get(flag['text_sha256'])
   errors.append(f"- {flag['task']} / {flag['group']} / 消息 {flag['index']}："+(decision['review'] if decision else '待人工核对：'+', '.join(flag['reasons'])))
 for path in sorted((ROOT/'reports/incidents').glob('*.json')):
  incident=json.loads(path.read_text())
  errors += ['',f"## 记录故障：{path.stem}", '',
      '异常尝试已排除主统计并归档；'+('等待记录修复后的单独恢复运行。' if incident.get('recovery_required') else '恢复运行已结束，主报告引用恢复轨迹。'),
      f"[事件记录]({path.relative_to(ROOT/'reports')})", '',
      'v2 适配器将记录目录及任务身份绑定到启动环境，防止改变当前目录后日志错位；早期 v1 运行保留，版本差异需与结果一同解释。']
 (ROOT/'reports/MONGO.md').write_text('\n'.join(native)+'\n');(ROOT/'reports/ERRORS.md').write_text('\n'.join(errors)+'\n')
 fl=['# FAD 预测和可见时序','',status,'',
 '这是协作协议干预，可能改变 Agent 的查询选择；不代表自然 Agent 的被动可预测性。预测在每次 query-db 前提交，list-db 豁免。horizon 2/3 匹配后续第 2/3 个请求的集合，不要求精确命中指定位置。Mongo 与 SQL 混合时，未来窗口按实际 query-db 顺序。','',
 '| 目标 | 数据前瞻点数 | 下一步表/集合精度 | 下一步表/集合覆盖 | 远期表/集合精度 | 远期有效分母 | 提交间隔中位秒 |','|---|---:|---:|---:|---:|---:|---:|']
 for mongo,label in [(False,'SQL'),(True,'Mongo')]:
  fs=[f for f in fadrows if f['targets_mongo']==mongo]
  def vals(k):return [f[k] for f in fs if f.get(k) is not None]
  fl.append(f"| {label} | {len(fs)} | {pct(mean(vals('immediate_table_precision')))} | {pct(mean(vals('immediate_table_recall')))} | {pct(mean(vals('later_table_precision')))} | {len(vals('later_table_precision'))} | {statistics.median(vals('lead_s')) if vals('lead_s') else '—'} |")
 fl += ['', f"可见新 assistant turn 检查：{sum(x['separate_assistant_turn'] for x in order_checks)}/{len(order_checks)}。SQL 文本子串提前出现标记：{sum(x['exact_sql_seen_before_fad_response'] for x in order_checks)}（启发式，须人工核对，不等于完整 SQL 提前生成）。Mongo 未进行原始请求内容的提前出现检查。",'',
 '间隔包含协议、模型和工具开销，不是免费可隐藏的物化时间。时间顺序不证明模型内部未提前构思 SQL。Mongo 原生列/过滤语义尚未做精确评分；各点明细保留在各运行 analysis.json。']
 order_review=ROOT/'reports/fad-order-review.json'
 if order_review.exists():
  fl += ['', '### 时序标记人工核对', '', '| 任务 | 调用 ID | 核对结果 |', '|---|---|---|']
  for review in json.loads(order_review.read_text()):
   run=ROOT/'runs'/review['group']/review['task']/'full-01'
   if not (run/'analysis.json').exists():continue
   query=next((q for q in json.loads((run/'analysis.json').read_text())['queries'] if q['call_id']==review['call_id']),None)
   if query and hashlib.sha256(query['sql'].encode()).hexdigest()==review['sql_sha256']:
    fl.append(f"| {review['task']} | {review['call_id']} | {review['review']} |")
  fl += ['', '[人工核对记录](fad-order-review.json)。保留原始标记，不将其直接作为违反协议的次数。']
 fl += ['', '## SQL 描述匹配细项', '', '按前瞻点宏平均，n 为指标有定义的点数；空分母不当作 0。列指标在相关库/表的预测条目中匹配列名，不是完整列血缘等价证明。过滤指标为严格合取项文本结构匹配，等价写法可能未命中；操作按 scan/filter/join/aggregate/sort/limit 分类。包含指向失败 SQL 的前瞻点，详见逐点记录。', '',
  '| 指标 | 平均值 | n |','|---|---:|---:|']
 sqlfs=[f for f in fadrows if not f['targets_mongo']]
 for key,label in [('immediate_table_precision','下一步表精度'),('immediate_table_recall','下一步表覆盖率'),('column_precision_1','下一步列名精度'),('column_recall_1','下一步列名覆盖率'),('operation_precision_1','下一步操作精度'),('operation_recall_1','下一步操作覆盖率'),('filter_exact_precision_1','过滤合取项精确匹配精度'),('filter_exact_recall_1','过滤合取项精确匹配覆盖率'),('later_table_precision','第 2/3 个请求的表集合精度'),('later_table_recall','第 2/3 个请求的表集合覆盖率')]:
  vs=[f[key] for f in sqlfs if f.get(key) is not None]
  fl.append(f"| {label} | {pct(mean(vs))} | {len(vs)} |")
 fl += ['', '## 按任务的前瞻表现', '', '仅统计 FAD 组在其实际请求序列上的预测；SQL 与 Mongo 目标数量分列，下面精度按两类的表/集合原子匹配合并。远期 n 仅包含显式给出远期预测且可计算精度的点。', '',
  '| 任务 | SQL 目标数 | Mongo 目标数 | 下一步表/集合精度 | 下一步覆盖率 | 远期精度 | 远期 n |','|---|---:|---:|---:|---:|---:|---:|']
 for task in sorted({f['task'] for f in fadrows}):
  fs=[f for f in fadrows if f['task']==task]
  def metric(key):return [f[key] for f in fs if f.get(key) is not None]
  fl.append(f"| {task} | {sum(not f['targets_mongo'] for f in fs)} | {sum(f['targets_mongo'] for f in fs)} | {pct(mean(metric('immediate_table_precision')))} | {pct(mean(metric('immediate_table_recall')))} | {pct(mean(metric('later_table_precision')))} | {len(metric('later_table_precision'))} |")
 (ROOT/'reports/FAD.md').write_text('\n'.join(fl)+'\n')
 inventory=json.loads((ROOT/'reports/data-inventory.json').read_text());dl=['# 数据位置和规模','', '| 数据集 | 逻辑库 | 引擎 | 表/集合数 | 精确总行/文档数 | 大小 MiB | 位置 |','|---|---|---|---:|---:|---:|---|']
 with (ROOT/'reports/tables.csv').open('w') as f:
  w=csv.DictWriter(f,fieldnames=['dataset','database','engine','table','rows','columns']);w.writeheader()
  for db in inventory:
   dl.append(f"| {db['dataset']} | {db['database']} | {db['engine']} | {len(db['tables'])} | {sum(t['rows'] for t in db['tables']):,} | {db['bytes']/1024**2:.2f} | `{db['location']}` |")
   for t in db['tables']:w.writerow(dict(dataset=db['dataset'],database=db['database'],engine=db['engine'],table=t['table'],rows=t['rows'],columns=json.dumps(t['columns'],ensure_ascii=False)))
 dl+=['','文件大小与 PostgreSQL/Mongo 存储大小口径不同，详见 JSON 的 size_kind。Mongo 字段名来自最多 100 个文档抽样，不是完整 schema。','',
 '[所有表/集合行数与字段 CSV](tables.csv) · [完整数据清单 JSON](data-inventory.json) · [源文件校验](source-integrity.json) · [环境版本](environment.json)','',
 '```bash','benchmark/bookreview/.venv/bin/python benchmark/fullbench/tools/inspect_data.py DATASET DATABASE --sql \'SELECT * FROM "TABLE" LIMIT 5\'','```','',
 '查看工具独立于实验轨迹，SQL 数据库只读连接；Mongo 在此工具中仅列清单。']
 (ROOT/'reports/DATA.md').write_text('\n'.join(dl)+'\n')
 print('Reports rendered',len(rs),'/',expected)
if __name__=='__main__':main()
