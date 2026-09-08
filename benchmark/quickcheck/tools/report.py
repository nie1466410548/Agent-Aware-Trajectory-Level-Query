"""Render the final descriptive tables; qualitative conclusions live in FINDINGS.md."""
import csv
import json
from pathlib import Path
import statistics
ROOT=Path(__file__).resolve().parents[1]
data=json.loads((ROOT/'reports/analysis.json').read_text())
rows=data['runs']
def pct(v):return '—' if v is None else f'{v*100:.1f}%'
lines=['> 本页的结构计数不是优化机会数量，当前候选见 [OVERLAP.md](OVERLAP.md)。', '', '# 九题快速验证：数据表','',
       '配置：Kimi CLI 0.41.0 / kimi-code/k3；自然组与 FAD 组各一次；不使用 hints；3 个并发运行进程。',
       '任务按描述预先选取，非随机总体样本。通过指原始 benchmark 验证器通过。', '',
       '| 任务 | 组别 | 验证 | 数据 SQL | 元数据 SQL | 失败数据 SQL | 空结果 | 重访表的后续 SQL | 复用语法候选 | FAD | 时长/秒 |',
       '|---|---|---|---:|---:|---:|---:|---:|---:|---:|---:|']
for r in sorted(rows,key=lambda r:(r['task_id'],r['group'])):
    path=f'../runs/{r["group"]}/{r["task_id"]}/{r["run_id"]}/analysis.json'
    status='通过' if r.get('validator_passed') else ('超时' if r.get('timed_out') else '未通过')
    lines.append(f'| [{r["task_id"]}]({path}) | {r["group"]} | {status} | {r["data_queries"]} | {r["metadata_queries"]} | {r["failed_data_queries"]} | {r["empty_successful_data_queries"]} | {r["later_queries_sharing_tables"]} | {r["later_queries_with_reuse_witness"]} | {r["fad_submissions"]} | {r.get("duration_s",0):.1f} |')
lines+=['','## 分组汇总','', '| 指标 | natural | fad |','|---|---:|---:|']
labels={'runs':'运行数','passed':'通过数','data_queries':'数据查询数（含失败）','metadata_queries':'元数据查询数',
 'failed_data_queries':'失败数据查询','empty_successful_data_queries':'执行成功但空结果',
 'later_queries_sharing_tables':'与前序成功查询共享表的后续查询数','later_queries_sharing_table_columns':'共享表且共享列的后续查询数',
 'shared_filter_consumers':'存在相同 WHERE 文本的后续查询数','shared_join_consumers':'存在相同 Join 片段的后续查询数',
 'shared_aggregate_consumers':'存在相同聚合表达式的后续查询数','exact_repeat_consumers':'规范化 SQL 完全相同的后续查询数',
 'later_queries_with_reuse_witness':'满足保守结果复用语法条件的后续查询数','fad_submissions':'成功提交 FAD 数','python_calls':'适配器 Python 调用数',
 'assistant_turns':'可见 assistant 消息数'}
for k,label in labels.items():lines.append(f'| {label} | {data["groups"]["natural"][k]} | {data["groups"]["fad"][k]} |')
lines+=['','注意：不同结构指标可以重叠，不能相加。同表/同 Join 片段均为候选，不表示已验证物理复用或净收益。','',
 '## FAD 预测统计','',
 '以下为各前瞻点的宏平均；分母 n 为有定义的前瞻点数。元数据目标已分离；针对已发出 SQL 的结构评分包含失败 SQL。', '',
 '| 指标 | 平均值 | n |','|---|---:|---:|']
fg=data['groups']['fad']
for k,label in [('table_precision_1','整个 frontier 对下一条 SQL 的表精度'),('table_recall_1','下一条 SQL 的表覆盖率'),
 ('immediate_table_precision','仅 horizon=1 条目的下一条表精度'),('immediate_table_recall','仅 horizon=1 条目的下一条表覆盖率'),
 ('table_precision_3','整个 frontier 对后续最多三条 SQL 的表精度'),('table_recall_3','后续最多三条 SQL 的表覆盖率'),
 ('column_precision_1','下一条 SQL 的列精度'),('column_recall_1','下一条 SQL 的列覆盖率'),
 ('operation_precision_1','下一条 SQL 的操作精度'),('operation_recall_1','下一条 SQL 的操作覆盖率'),
 ('filter_exact_precision_1','过滤条件精确合取项匹配精度'),('filter_exact_recall_1','过滤条件精确合取项匹配覆盖率'),
 ('later_table_precision','horizon 2/3 条目对第 2/3 条 SQL 的表精度'),('later_table_recall','horizon 2/3 条目对第 2/3 条 SQL 的表覆盖率'),
 ('last_query_table_recall_1','弱基线：上一条查询表集合覆盖下一条')]:
    v=fg[k];lines.append(f'| {label} | {pct(v["mean"])} | {v["n"]} |')
lines+=['',f'- 数据目标 FAD：{fg["scored_data_frontiers"]}；元数据目标：{fg["metadata_frontiers"]}；之后无查询：{fg["frontiers_without_next_query"]}。',
 f'- 明确包含 horizon 2/3 预测的数据 frontier：{fg["frontiers_with_later_predictions"]}。',
 f'- 下一条查询失败的数据 frontier：{fg["frontiers_followed_by_failed_query"]}。',
 f'- SQL 独立后续 assistant turn 时序检查：{fg["fad_separate_turn_passed"]}/{fg["fad_order_checked"]}；提前出现相同 SQL 的检查标记：{fg["sql_early_emission_flags"]}。',
 f'- FAD 完成到 SQL 提交的时间差：中位数 {fg["lead_s_median"]:.2f} 秒，范围 {fg["lead_s_min"]:.2f}–{fg["lead_s_max"]:.2f} 秒。',
 '- 时间差包括模型生成与工具开销，不能等同于可隐藏的物化时间或实测加速。',
 '- frontier 内含多个候选时，下一条表精度较低可以是正常分支/远期预测，不能全部解释为错误。第 2/3 条的独立指标更接近 rolling 能力。',
 '- 过滤指标是严格文本结构匹配，SQL 等价条件可能被判未匹配；未测概率校准。','',
 '## FAD 按任务分布','', '| 任务 | 数据 frontier 数 | horizon=1 表覆盖 | 第 2/3 条表精度 | 有远期预测的 frontier 数 |','|---|---:|---:|---:|---:|']
for r in sorted((r for r in rows if r['group']=='fad'),key=lambda r:r['task_id']):
    p=ROOT/'runs'/r['group']/r['task_id']/r['run_id']/'analysis.json'
    if not p.exists():continue
    fs=[f for f in json.loads(p.read_text())['fads'] if f['has_next_query'] and not f['targets_metadata']]
    def avg(k):
        vs=[f[k] for f in fs if f.get(k) is not None]
        return statistics.mean(vs) if vs else None
    lines.append(f'| {r["task_id"]} | {len(fs)} | {pct(avg("immediate_table_recall"))} | {pct(avg("later_table_precision"))} | {sum(bool(f["later_prediction_atoms"]) for f in fs)} |')
lines+=['',
 '## 两组运行变化','', '| 任务 | natural 秒 | fad 秒 | 数据 SQL natural → fad | 验证 natural → fad |','|---|---:|---:|---|---|']
for task in sorted({r['task_id'] for r in rows}):
    rr={r['group']:r for r in rows if r['task_id']==task}
    if set(rr)!={'natural','fad'}:continue
    a,b=rr['natural'],rr['fad']
    lines.append(f'| {task} | {a.get("duration_s",0):.1f} | {b.get("duration_s",0):.1f} | {a["data_queries"]} → {b["data_queries"]} | {a.get("validator_passed")} → {b.get("validator_passed")} |')
lines+=['','同题两组是不同的随机轨迹，样本各一次，运行时长受共享资源与服务波动影响。这里仅描述变化，不估计 FAD 的因果开销或收益。', '',
 '详细方法、约束及复跑方法见 [README](../README.md)。结论与案例见 [FINDINGS](FINDINGS.md)。']
(ROOT/'reports/TABLES.md').write_text('\n'.join(lines)+'\n')
keys=sorted(set().union(*(r.keys() for r in rows)))
with (ROOT/'reports/runs.csv').open('w') as f:
    w=csv.DictWriter(f,fieldnames=keys);w.writeheader();w.writerows(rows)
print('Wrote TABLES.md and runs.csv')
