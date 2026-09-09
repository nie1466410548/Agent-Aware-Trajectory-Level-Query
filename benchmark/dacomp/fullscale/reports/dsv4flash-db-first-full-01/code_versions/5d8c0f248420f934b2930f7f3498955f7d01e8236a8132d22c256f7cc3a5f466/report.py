"""Regenerate 100-task readable reports and machine tables from primary evidence."""
import collections, csv, json, statistics, time, os, re, hashlib
from common import *
from profile import features
from engine import category as logged_category
from opportunities import enumerate_candidates,verify
from audit import audit_task
from render_answers import render_answer
LABEL={'pending':'未开始','submitted':'已提交','running':'运行中','quota_interrupted':'额度中断','service_error':'服务中断','timeout':'超时','no_submission':'未提交','process_failed':'进程失败','not_prepared':'未准备','preparation_failed':'准备失败','orchestration_failed':'运行器失败'}
def table(headers,rows):
 def cell(x):
  if isinstance(x,(list,dict)): x=json.dumps(x,ensure_ascii=False)
  return str(x if x is not None else 'unknown').replace('|','\\|').replace('\n','<br>')
 return '\n| '+' | '.join(headers)+' |\n| '+' | '.join(['---']*len(headers))+' |\n'+''.join('| '+' | '.join(cell(x) for x in row)+' |\n' for row in rows)+'\n'
def csvout(name,rows,fields=None):
 with (REPORT/name).open('w') as f:
  fields=fields or sorted(set(k for r in rows for k in r));w=csv.DictWriter(f,fieldnames=fields);w.writeheader()
  for r in rows: w.writerow({k:json.dumps(v,ensure_ascii=False) if isinstance(v,(list,dict)) else v for k,v in r.items()})
def relative(path,base): return os.path.relpath(path,base)
def elapsed(q):
 if q.get('execute_return_ms') is None and q['status']!='success': return '未取得；调用总时长 '+str(round(q['wall_ms'],3) if q.get('wall_ms') is not None else 'unknown')+' ms'
 return round(q['execute_fetch_ms'],3)
def analysis_status(qs,cs):
 if any(c['status']=='verified' for c in cs): return '已验证候选'
 if cs: return '有候选待验证/受限或已拒绝'
 if not qs or not all(q['profile'].get('parsed') for q in qs): return '轨迹/解析不足无法判断'
 return '分析覆盖内未发现候选'
def main():
 REPORT.mkdir(parents=True,exist_ok=True);(REPORT/'tasks').mkdir(exist_ok=True)
 source_files=[ROOT/'tools'/name for name in ['report.py','profile.py','opportunities.py','common.py','audit.py','render_answers.py']]
 analysis_hash=hashlib.sha256(''.join(sha(p) for p in source_files).encode()).hexdigest()
 version_dir=REPORT/'code_versions'/analysis_hash
 if not version_dir.exists():
  version_dir.mkdir(parents=True)
  for source in source_files:(version_dir/source.name).write_bytes(source.read_bytes())
  dump(version_dir/'manifest.json',{'phase':'offline_analysis','version':analysis_hash,'files':{p.name:sha(p) for p in source_files}})
 profile_version=sha(ROOT/'tools/profile.py');(REPORT/'profile_cache').mkdir(exist_ok=True)
 entries=records(ROOT/'manifests/tasks.jsonl'); queue=json.loads((ROOT/'state/queue.json').read_text()) if (ROOT/'state/queue.json').exists() else {'tasks':{}}
 taskrows=[];sqlrows=[];profiles=[];structures=[];opps=[];verification=[];overview=[];stra=[];strb=[];audit=[]
 performance=json.loads((REPORT/'performance.json').read_text()) if (REPORT/'performance.json').exists() else []
 performance_map={(r.get('task_id'),r.get('candidate_id')):r for r in performance}
 for entry in entries:
  tid=entry['task_id'];run=ROOT/'runs'/BATCH/tid/'attempt-01';status=queue['tasks'].get(tid,{}).get('status',entry['status']);summary=json.loads((run/'run_summary.json').read_text()) if (run/'run_summary.json').exists() else {}
  active_run=status=='running'
  events=[] if active_run else records(run/'sql_events.jsonl');calls=[] if active_run else records(run/'tool_calls.jsonl');qs=[]
  profile_cache_path=REPORT/'profile_cache'/f'{tid}.json';event_hash=sha(run/'sql_events.jsonl') if events else None
  profile_cache=json.loads(profile_cache_path.read_text()) if profile_cache_path.exists() else {}
  cached_profiles=profile_cache.get('profiles',{}) if profile_cache.get('event_hash')==event_hash and profile_cache.get('profile_version')==profile_version else {}
  fresh_profiles={}
  for q in events:
   q['recorded_category']=q['category']
   without_prefix=re.sub(r'^(?:\s|--[^\n]*(?:\n|$)|/\*[\s\S]*?\*/)*','',q['sql'])
   q['category']=logged_category(without_prefix) if q['category']=='unknown' else q['category']
   q['profile']=(cached_profiles.get(q['sql_id']) or features(q['sql'],entry.get('tables',[]))) if q['category']=='data' else {}
   fresh_profiles[q['sql_id']]=q['profile']
   if q['category']=='data': q['query_id']=f'Q{len(qs)+1}';qs.append(q)
   profiles.append({'task_id':tid,**q})
   f=q['profile'];row={'task_id':tid,'sql_id':q['sql_id'],'query_id':q.get('query_id'),'source':q['source'],'category':q['category'],'status':q['status'],
       'base_tables':f.get('base_tables'),'table_references':f.get('table_references'),'join_inputs':f.get('max_join_inputs'),'join_types':f.get('join_types'),
       'group_by':[g['expression'] for b in f.get('blocks',[]) for g in b['group_by']],'aggregates':[a['expression'] for a in f.get('aggregate_expressions',[])],
       'row_count':q['row_count'],'execute_fetch_ms':q['execute_fetch_ms'] if q.get('execute_return_ms') is not None or q['status']=='success' else None,'call_wall_ms':q.get('wall_ms'),'result_complete':q['result_complete'],'sql':q['sql'],'parameters':q['parameters']};sqlrows.append(row)
  if events and not cached_profiles: dump(profile_cache_path,{'event_hash':event_hash,'profile_version':profile_version,'profiles':fresh_profiles})
  if summary:
   normalized_attempts=len(qs);normalized_success=sum(q['status']=='success' for q in qs)
   if normalized_attempts!=summary['data_sql_attempts'] or normalized_success!=summary['data_sql_success']:
    summary.setdefault('provisional_data_counts_before_comment_normalization',{'attempts':summary['data_sql_attempts'],'success':summary['data_sql_success']})
    summary.update(data_sql_attempts=normalized_attempts,data_sql_success=normalized_success,sql_category_policy='leading SQL comments ignored; raw sql_events unchanged')
    dump(run/'run_summary.json',summary)
  success=[q for q in qs if q['status']=='success'];parsed=[q for q in success if q['profile'].get('parsed')]
  candidates=[]
  if success:
   cache=REPORT/'tasks'/f'{tid}.analysis.json';fingerprint=sha(run/'sql_events.jsonl')
   old=json.loads(cache.read_text()) if cache.exists() else {}
   if old.get('fingerprint')==fingerprint: candidates=old['candidates']
   else:
    candidates=enumerate_candidates(success)
    ranked=sorted(candidates,key=lambda c:(c['later_reuses'],sum(q['execute_fetch_ms'] for q in success if q['sql_id'] in c['covered']),c['type']=='aggregate MV'),reverse=True)
    for c in ranked[:3]: verify(c,success,run,entry['database_path'])
    for c in ranked[3:]: c['status']='not_verified_cap';c['cost_conclusion']='Not tested'
    dump(cache,{'fingerprint':fingerprint,'analysis_source_version':analysis_hash,'method':'exact SQL, identical CTE, identical single-table filter, decomposable single-table aggregate; maximum three correctness checks','candidates':candidates})
  for c in candidates:
   perf=performance_map.get((tid,c['candidate_id']))
   if perf and perf.get('status')=='measured': c['cost_conclusion']=f"Warm-cache baseline {perf['baseline_median_ms']:.3f} ms vs build+reuse {perf['candidate_median_ms']:.3f} ms, ratio {perf['ratio_baseline_over_candidate']:.3f}; five repetitions, see performance evidence."
  astat=analysis_status(success,candidates)
  for c in candidates: opps.append({'task_id':tid,**{k:v for k,v in c.items() if k not in ['checks','rewrites']}}); verification.append({'task_id':tid,**c})
  scounter=collections.Counter(q['category'] for q in events);py=[c for c in calls if c['tool']=='python']
  row={'task_id':tid,'instruction':entry['task']['instruction'],'database_tables':len(entry.get('tables',[])),'database_bytes':entry.get('database_bytes'),'status':status,
       'all_sql_attempts':len(events),'all_sql_success':sum(q['status']=='success' for q in events),'data_sql_attempts':len(qs),'data_sql_success':len(success),
       'failed_sql':sum(q['status']=='failed' for q in events),'metadata_sql':scounter['metadata'],'connection_setup_sql':scounter['connection_setup'],'maintenance_sql':scounter['maintenance'],'unknown_category_sql':scounter['unknown'],
       'python_calls':len(py),'python_success':sum(c.get('result',{}).get('returncode')==0 for c in py),'query_rejections':len(records(run/'sql_rejections.jsonl')),'cancelled_sql':sum(q['status']=='cancelled' for q in events),'limited_sql':sum(q['status']=='limited' for q in events),'duration_s':summary.get('duration_s'),'analysis_status':astat,'parsed_data_sql':len(parsed),'table_lineage_complete_sql':sum(q['profile'].get('table_lineage_coverage',False) for q in parsed),
       'column_lineage_complete_sql':sum(q['profile'].get('column_lineage_coverage',False) for q in parsed),'official_evaluation':'not_run'}
  review_path=REPORT/'reviews'/f'{tid}.json'; review=json.loads(review_path.read_text()) if review_path.exists() else {}
  row['trajectory_truncated']=status in ['timeout','quota_interrupted','service_error','interrupted'] or row['query_rejections']>0
  row['python_protocol_status']=review.get('status','not_applicable' if not py else 'not_fully_reviewed')
  taskrows.append(row)
  fns=collections.Counter(a for q in parsed for a in q['profile']['aggregate_functions'])
  structure={'task_id':tid,'success_data_sql':len(success),'unknown_sql':len(success)-len(parsed),'table_buckets':dict(collections.Counter(str(min(len(q['profile']['base_tables']),4)) for q in parsed)),
       'join_buckets':dict(collections.Counter(str(min(q['profile']['max_join_inputs'],4)) for q in parsed)), 'group_buckets':dict(collections.Counter(str(min(q['profile']['max_group_dimensions'],4)) for q in parsed)),
       'group_vectors':[q['profile']['group_dimensions'] for q in parsed],'aggregate_function_sql_counts':dict(fns),'aggregate_expression_counts':dict(sum((collections.Counter(q['profile']['aggregate_functions']) for q in parsed),collections.Counter())),
       'with_join':sum(q['profile']['max_join_inputs']>0 for q in parsed),'with_group_by':sum(q['profile']['max_group_dimensions']>0 for q in parsed),
       'with_aggregate':sum(bool(q['profile']['aggregate_functions']) for q in parsed),'with_window':sum(q['profile']['window_count']>0 for q in parsed)}
  structure['aggregate_metric_columns']=sorted({json.dumps(col,ensure_ascii=False,sort_keys=True) for q in parsed for a in q['profile']['aggregate_expressions'] for col in a['metric_columns']})
  structure['aggregate_condition_columns']=sorted({json.dumps(col,ensure_ascii=False,sort_keys=True) for q in parsed for a in q['profile']['aggregate_expressions'] for col in a['condition_columns']})
  structure['aggregate_metric_columns']=[json.loads(v) for v in structure['aggregate_metric_columns']]
  structure['aggregate_condition_columns']=[json.loads(v) for v in structure['aggregate_condition_columns']]
  structure['distinct_metric_column_count']=len(structure['aggregate_metric_columns'])
  structure['join_type_occurrences']=dict(sum((collections.Counter(q['profile']['join_types']) for q in parsed),collections.Counter()))
  structures.append(structure)
  link=f'[{tid}](tasks/{tid}.md)';short=entry['task']['instruction'].strip().replace('\n',' ')[:90]+'…'
  status_label='已提交（截断）' if status=='submitted' and row['trajectory_truncated'] else LABEL.get(status,status)
  overview.append([link,short,f"{row['database_tables']} / {round((row['database_bytes'] or 0)/1024**2,2)} MiB",status_label,f"{len(events)}/{row['all_sql_success']}",f"{len(qs)}/{len(success)}",len(py),round(summary.get('duration_s',0)/60,2),astat])
  stra.append([link,len(success),structure['table_buckets'].get('1',0),sum(len(q['profile']['base_tables'])>1 for q in parsed),structure['with_join'],*[structure['join_buckets'].get(str(i),0) for i in [2,3,4]],structure['unknown_sql']])
  strb.append([link,structure['with_group_by'],*[structure['group_buckets'].get(str(i),0) for i in [1,2,3,4]],structure['with_aggregate'],dict(fns),structure['with_window']])
  detail=REPORT/'tasks'/f'{tid}.md';base=detail.parent
  readable=render_answer(run,REPORT/'answers'/f'{tid}.md') if not active_run else None
  text=f'# {tid}\n\n{short}\n\n运行：{status_label}。官方未评分。全部 SQL 尝试/成功 {len(events)}/{row["all_sql_success"]}；数据 SQL {len(qs)}/{len(success)}；Python {len(py)} 次。\n'
  if active_run: text+='\n本题运行中，统计暂不读取正在写入的日志；结束后补全。\n'
  text+='\n完整原题：\n\n'+entry['task']['instruction']+'\n'
  text+=table(['表','行数','列数'],[[t['name'],t['rows'],len(t['columns'])] for t in entry.get('tables',[])])
  route=review.get('route')
  if not route:
   landmarks=qs if len(qs)<=6 else [qs[i] for i in sorted({round(j*(len(qs)-1)/5) for j in range(6)})]
   route=(' → '.join(f"{q['sql_id']}："+('/'.join(q['profile'].get('base_tables') or ['unknown']))+(' 分组聚合' if q['profile'].get('max_group_dimensions') else ' 查询') for q in landmarks) if qs else '没有可用数据查询。')
   if len(qs)>6: route+='（等距列出六个结构节点，全部步骤见下表）'
  text+='\n实际路线（分析者依据 SQL/源码概括，不代表 Agent 自述）：'+route+'\n'
  text+=f'\n数据库大小：{entry.get("database_bytes",0):,} 字节。\n'
  text+='\n## 数据 SQL\n'+table(['SQL','状态','基础表','Join 输入/类型','GROUP BY','聚合表达式','结果行数','数据库 ms'],[[f'[{q["sql_id"]}/{q["query_id"]}](#{q["sql_id"].lower()})',q['status'],q['profile'].get('base_tables'),str(q['profile'].get('max_join_inputs'))+' / '+str(q['profile'].get('join_types')),[g['expression'] for b in q['profile'].get('blocks',[]) for g in b['group_by']],[a['expression'] for a in q['profile'].get('aggregate_expressions',[])],q['row_count'],elapsed(q)] for q in qs])
  text+='\n## 元数据和设置\n'+table(['SQL','类别','状态','内容'],[[q['sql_id'],q['category'],q['status'],q['sql']] for q in events if q['category']!='data'])
  text+='\n## Python 与执行位置\n'
  if review: text+='\n人工源码审查：**'+review['status']+'**。'+review['conclusion']+f' [证据](../reviews/{tid}.json)。\n'
  if not py: text+='\n无 Python 分析调用。\n'
  for i,c in enumerate(py,1):
   code=c['arguments'].get('code',''); signal_terms=[term for term in ['groupby(','.merge(','.query(','.resample(','sort_values('] if term in code]
   text+=f'\nP{i}：{c["arguments"].get("reason","未提供理由")}\n\n[源码]({relative(run/"python"/f"P{i}.py",base)})；[输出]({relative(run/"python"/f"P{i}.stdout",base)})；[错误]({relative(run/"python"/f"P{i}.stderr",base)})。'+('检出需人工核验的 SQL 可实现操作：'+', '.join(signal_terms)+'；不能仅凭理由判为合规。' if signal_terms else '自动源码筛查未检出预设迁出信号；这不是全面语义合规证明。')+'\n'
  text+='\n## 优化机会\n\n'+astat+'。筛选限于精确 SQL、相同自包含 CTE、相同单表完整过滤、可分解单表聚合；未覆盖任意 Join 等价和一般谓词蕴含。全部候选都是 offline，未测在线预测。\n'
  text+=table(['候选','类型','已有结果','覆盖 SQL','后续次数','中间行数','验证','成本'],[[c['candidate_id'],c['type'],c['existing_result'],c['covered'],c['later_reuses'],c.get('intermediate_rows'),c['status'],c.get('cost_conclusion','未验证')] for c in candidates])
  covered=set(qid for c in candidates if c['status']=='verified' for qid in c['covered'])
  text+=f'\n已验证覆盖（含触发查询、候选并集去重）：{len(covered)}/{len(success)} 条成功数据 SQL。'+('没有发现本方法可验证的候选，不等于不存在优化。' if not candidates else '正确性仅针对当前数据库快照；未测性能的候选不能声称已加速。')+'\n'
  if candidates: text+=f'\n[完整 build/rewrite 与比较证据]({tid}.analysis.json)。\n'
  representative=sorted(candidates,key=lambda c:(c['status']!='verified',-len(c['covered'])))[:3]
  for c in representative:
   text+=f'\n### {c["candidate_id"]}：{c["type"]}\n\n'+c.get('reason','')+'\n\n原查询 '+', '.join(f'[{sid}](#{sid.lower()})' for sid in c['covered'])+' → '+('保留前序结果 '+c.get('producer','') if c['existing_result'] else '新增共享状态 '+c['candidate_id'])+' → 后续 '+str(c['later_reuses'])+' 次可复用。该构建点为事后假设，不代表 Agent 当时预知后续。\n'
   if c.get('build_sql'): text+='\n构建定义：\n\n```sql\n'+c['build_sql']+'\n```\n'
   if c.get('rewrites'):
    sid=next(iter(c['rewrites']));rewritten=c['rewrites'][sid]
    text+=f'\n受益查询 {sid} 的改写示例'+('（截取前 1600 字符，完整版本见证据 JSON）' if len(rewritten)>1600 else '')+'：\n\n```sql\n'+rewritten[:1600]+'\n```\n'
   if c.get('checks'): text+=table(['原 SQL','列名一致','结果一致','比较方法'],[[x['sql_id'],x['columns_equal'],x['rows_equal'],x['comparison']] for x in c['checks']])
   text+='\n验证状态：'+c['status']+'；成本结论：'+c.get('cost_conclusion','未验证')+'\n'

  for c in candidates:
   perf=performance_map.get((tid,c['candidate_id']))
   if perf: text+=f'\n[性能证据 {c["candidate_id"]}]({tid}.{c["candidate_id"]}.performance.json)：'+perf.get('status','unknown')+'。\n'
  text+='\n结果依赖：自动记录 SQL→Python 的接口父调用，以及源码中引用归档文件的消费者；字面值相同不认定因果。模型方向选择需要人工读取消息，尚未做全面因果标注。\n'
  if run.exists(): text+='\n'+'；'.join(f'[{label}]({relative(run/path,base)})' for label,path in [('原始报告','answer.md'),('统一消息','messages.jsonl'),('原始 OpenCode 事件','opencode.jsonl'),('SQL 引擎日志','sql_journal.jsonl')] if (run/path).exists())+'。\n'
  if readable: text+=f'\n[可读报告（本地图片链接规范化）](../answers/{tid}.md)。原始回答保留，分析结论未改写。\n'
  for q in events:
   text+=f'\n## {q["sql_id"]}\n\n类别 `{q["category"]}`；来源 `{q["source"]}`；调用 `{q["call_id"]}`；状态 `{q["status"]}`。\n\n```sql\n{q["sql"]}\n```\n'
   text+=f'\n[SQL]({relative(run/"sql"/(q["sql_id"]+".sql"),base)})；[绑定参数]({relative(run/"sql"/(q["sql_id"]+".parameters.json"),base)})。\n'
   if q.get('result_file'): text+=f'\n[原始行数组]({relative(run/q["result_file"],base)})；完整：{q["result_complete"]}；SHA256：`{q["result_sha256"]}`。\n'
   if q.get('error'): text+='\n错误：`'+q['error']+'`。\n'
   f=q.get('profile',{})
   if f.get('parsed'):
    text+=table(['查询块','来源实例与基础表','Join 条件','分组维度'],[[b['id'],b['sources'],b['joins'],[g['expression'] for g in b['group_by']]] for b in f['blocks']])
    text+=table(['块','聚合表达式','指标列血缘','条件列血缘','行计数'],[[b['id'],a['expression'],a['metric_columns'],a['condition_columns'],a['row_count']] for b in f['blocks'] for a in b['aggregates']])
    if f.get('unknowns'): text+='\n未解析列血缘：'+json.dumps(f['unknowns'],ensure_ascii=False)+'\n'

  detail.write_text(text)
  journal=[] if active_run else records(run/'sql_journal.jsonl');req=[j for j in journal if j.get('record')=='request'];traces=[j for j in journal if j.get('record')=='engine_trace']
  if summary and not active_run and not (run/'audit.json').exists():
   checked=audit_task(tid,entry)
   if checked['issues'] and not queue.get('stop_reason'):
    queue['stop_reason']={'kind':'recording_audit_gap','task_id':tid,'issues':checked['issues']};dump(ROOT/'state/queue.json',queue)
  completed_audit=json.loads((run/'audit.json').read_text()) if (run/'audit.json').exists() else None
  audit.append({'task_id':tid,'status':status,'sql_requests':len(req),'sql_completions':len(events),'counts_closed':len(req)==len(events),'engine_trace_events':len(traces),'unattributed_traces':sum(j.get('sql_id') is None for j in traces),'archive_hashes_ok':all(not issue.startswith('Archive hash mismatch') for issue in completed_audit['issues']) if completed_audit else None,'hash_validation_source':'per-run audit.json; final audit rechecks all files'})
 csvout('tasks.csv',taskrows);csvout('sql_profile.csv',sqlrows,fields=None if sqlrows else ['task_id','sql_id']);csvout('trajectory_structure.csv',structures);csvout('opportunities.csv',opps,fields=None if opps else ['task_id','candidate_id','status'])
 (REPORT/'sql_profile.jsonl').write_text(''.join(json.dumps(q,ensure_ascii=False)+'\n' for q in profiles));(REPORT/'verification.jsonl').write_text(''.join(json.dumps(c,ensure_ascii=False)+'\n' for c in verification));dump(REPORT/'audit.json',{'planned':100,'registered':len(entries),'status_counts':dict(collections.Counter(r['status'] for r in taskrows)),'tasks':audit})
 counts=collections.Counter(r['status'] for r in taskrows);started=sum(r['status'] not in ['pending','not_prepared','preparation_failed'] for r in taskrows)
 text=f'# DAComp-DA：数据库内优先协议下的 Agent 轨迹\n\n计划 100 题，登记 {len(entries)} 题，已开始 {started} 题，已提交 {counts["submitted"]} 题（其中未截断 {sum(r["status"]=="submitted" and not r["trajectory_truncated"] for r in taskrows)} 题、截断提交 {sum(r["status"]=="submitted" and r["trajectory_truncated"] for r in taskrows)} 题）。模型 `{MODEL}`，OpenCode 1.18.29；全部官方未评分；旧四题独立保留。\n'
 sizes=[r.get('database_bytes',0) for r in entries if r.get('status')=='ready']
 if sizes: text+=f'\n数据固定 revision `{REVISION}`；数据库合计 {sum(sizes):,} 字节，中位数 {statistics.median(sizes):,.0f} 字节，最大 {max(sizes):,} 字节。逐表实际行数见各题详情与 [数据清单](../../manifests/databases.csv)。\n'
 text+=table(['状态','任务数'],[[LABEL.get(k,k),v] for k,v in sorted(counts.items())])
 text+='\n并发调度：'+str(queue.get('concurrency',1))+' 个任务槽；运行中的轨迹暂不计数，结束后统一审计。串行/并发边界见 state/version_boundaries.jsonl，原始查询耗时可能受并发资源竞争影响。\n'
 text+='\n本批次状态持续由记录生成；提交不等于答案正确。无 FAD 组、无官方模型裁判、无成功率重跑、无金额预算。\n'
 if queue.get('stop_reason'): text+='\n**已停止派发：** '+json.dumps(queue['stop_reason'],ensure_ascii=False)+'\n\n[检查点](../../state/queue.json)；恢复操作见 [恢复说明](../../RECOVERY.md)。\n'
 text+='\n## 轨迹有多长\n\n表中 SQL 为尝试/成功，时长为分钟；元数据和连接设置纳入全部 SQL。\n'+table(['任务','题意节选','表数/大小','状态','全 SQL','数据 SQL','Python','时长','分析状态'],overview)
 for label,rs in [('已提交且未截断',[r for r in taskrows if r['status']=='submitted' and not r['trajectory_truncated']]),('已结束但截断/失败',[r for r in taskrows if r['trajectory_truncated'] or r['status'] not in ['submitted','pending','running','not_prepared','preparation_failed']])]:
  values=sorted(r['data_sql_success'] for r in rs)
  if values:
   def pct(p):
    x=(len(values)-1)*p;a=int(x);b=min(a+1,len(values)-1);return values[a]+(values[b]-values[a])*(x-a)
   text+=f'\n{label}：n={len(values)}；成功数据 SQL 均值 {statistics.mean(values):.2f}，中位数 {statistics.median(values)}，P25/P75/P90 {pct(.25):.2f}/{pct(.75):.2f}/{pct(.9):.2f}，范围 {min(values)}–{max(values)}。\n'
 total_sql=sum(r['all_sql_attempts'] for r in taskrows);total_data=sum(r['data_sql_attempts'] for r in taskrows);total_py=sum(r['python_calls'] for r in taskrows)
 text+=f'\n全批次当前记录：SQL 尝试 {total_sql}，其中数据 {total_data}、元数据 {sum(r["metadata_sql"] for r in taskrows)}、连接设置 {sum(r["connection_setup_sql"] for r in taskrows)}、维护 {sum(r["maintenance_sql"] for r in taskrows)}、未知类别 {sum(r["unknown_category_sql"] for r in taskrows)}；SQL 成功 {sum(r["all_sql_success"] for r in taskrows)}、失败 {sum(r["failed_sql"] for r in taskrows)}、取消 {sum(r["cancelled_sql"] for r in taskrows)}、结果受限 {sum(r["limited_sql"] for r in taskrows)}。Python {total_py} 次，其中 {sum(r["python_success"] for r in taskrows)} 次成功；使用 Python 的已开始任务 {sum(r["python_calls"]>0 for r in taskrows)}/{started}。\n'
 review_counts=collections.Counter(r['python_protocol_status'] for r in taskrows if r['status'] not in ['pending','running','not_prepared','preparation_failed'])
 text+='\n执行位置审查按已结束任务列出；含违例的轨迹继续保留，不能混称严格符合数据库内优先协议。\n'+table(['Python 执行位置审查状态','任务数'],sorted(review_counts.items()))
 text+='\n## SQL 具体在做什么\n\n以下以成功数据 SQL 为分母；解析失败单列，不能把多表访问自动当成 Join。\n'+table(['任务','数据 SQL','单表','多表','含 Join','2 输入','3 输入','≥4 输入','未解析'],stra)+table(['任务','含 GROUP BY','1 维','2 维','3 维','≥4 维','含聚合','函数 SQL 数','含窗口'],strb)
 text+='\n## 哪些工作能共享\n\n精确结果复用与新增物化分别记录；结构相似只用于候选筛选，每题最多验证 3 个代表性候选。\n'+table(['任务','分析状态','已验证已有结果候选','已验证新增物化候选','去重覆盖/成功数据 SQL'],[[f'[{r["task_id"]}](tasks/{r["task_id"]}.md)',r['analysis_status'],sum(c['task_id']==r['task_id'] and c['status']=='verified' and c['existing_result'] for c in verification),sum(c['task_id']==r['task_id'] and c['status']=='verified' and not c['existing_result'] for c in verification),str(len({sid for c in verification if c['task_id']==r['task_id'] and c['status']=='verified' for sid in c['covered']}))+'/'+str(r['data_sql_success'])] for r in taskrows])
 if performance:
  text+='\n暖缓存代表性性能验证（物化路径含每次构建，五次交替重复）：\n'+table(['任务/候选','状态','基线中位 ms','构建+复用中位 ms','基线/候选'],[[str(r.get('task_id'))+'/'+str(r.get('candidate_id')),r['status'],r.get('baseline_median_ms'),r.get('candidate_median_ms'),r.get('ratio_baseline_over_candidate')] for r in performance])
 text+='\n## 结论边界\n\n本报告描述当前已记录轨迹。未开始任务不参与轨迹长度分布。不能把协议或模型变化解释为受控因果效果；候选基于已知完整轨迹离线选择，不证明在线可预测性或净收益。Python 源码筛查不能代替完整语义人工审查；无法解析的列血缘明确保留 unknown。\n\n[指标口径](METRICS.md)；[机器任务表](tasks.csv)；[逐 SQL 结构](sql_profile.jsonl)；[候选比较](verification.jsonl)；[审计](audit.json)。\n'
 (REPORT/'REPORT.md').write_text(text)
 print(json.dumps({'registered':len(entries),'states':dict(counts),'all_sql':len(profiles),'candidates':len(verification)},ensure_ascii=False),flush=True)
 if queue.get('stop_reason',{}).get('kind')=='recording_audit_gap': raise SystemExit('Recording audit gap; dispatch stopped, see state/queue.json')
if __name__=='__main__':
 main()
 # One-time authorized scheduler handover, only after a completed report and
 # only for the named serial parent. No OpenCode process is interrupted.
 handover=ROOT/'state/parallel-handover.json'
 if handover.exists():
  h=json.loads(handover.read_text())
  if h.get('status')=='requested' and h.get('serial_pid')==os.getppid():
   import signal
   h.update(status='ready',ready_at=time.time());dump(handover,h)
   os.kill(os.getppid(),signal.SIGTERM)

