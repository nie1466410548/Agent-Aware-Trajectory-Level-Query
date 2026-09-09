# dacomp-013

Develop a fair and reasonable performance evaluation plan for Task Owners across different…

运行：已提交。官方未评分。全部 SQL 尝试/成功 37/37；数据 SQL 35/35；Python 24 次。

完整原题：

Develop a fair and reasonable performance evaluation plan for Task Owners across different Task Types, and classify performance levels according to this plan.
Requirements:
1. Performance levels and proportions: The final performance evaluation results must be distributed according to Excellent (20%), Good (70%), Needs Improvement (10%).
2. Evaluation dimensions: The plan should comprehensively consider the following core dimensions (but is not limited to):
① Task completion status (e.g., completion rate, quality, timeliness)
② Task Priority (the completion of high-priority tasks should be given special consideration)
③ Work hours utilization (input–output efficiency)
Because different Task Types may have significant differences in difficulty, complexity, and required skills, you must fully consider and reasonably balance these differences during plan design and actual evaluation to ensure fairness, comparability, and avoid distortion.

| 表 | 行数 | 列数 |
| --- | --- | --- |
| sheet1 | 799 | 16 |


实际路线（分析者依据 SQL/源码概括，不代表 Agent 自述）：按负责人汇总任务质量、工时和完成指标 → 在任务类型内做百分位评分 → 比较分类方案与收缩参数 → 生成 20/70/10 分类和分类摘要。

数据库大小：233,472 字节。

## 数据 SQL

| SQL | 状态 | 基础表 | Join 输入/类型 | GROUP BY | 聚合表达式 | 结果行数 | 数据库 ms |
| --- | --- | --- | --- | --- | --- | --- | --- |
| [S3/Q1](#s3) | success | ["sheet1"] | 0 / {} | [] | [] | 20 | 0.613 |
| [S4/Q2](#s4) | success | ["sheet1"] | 0 / {} | [] | ["COUNT(*)"] | 1 | 0.393 |
| [S5/Q3](#s5) | success | ["sheet1"] | 0 / {} | ["\"Task Status\""] | ["COUNT(*)"] | 4 | 0.643 |
| [S6/Q4](#s6) | success | ["sheet1"] | 0 / {} | ["\"Priority\""] | ["COUNT(*)"] | 4 | 0.616 |
| [S7/Q5](#s7) | success | ["sheet1"] | 0 / {} | ["\"Task Type\""] | ["COUNT(*)"] | 4 | 0.616 |
| [S8/Q6](#s8) | success | ["sheet1"] | 0 / {} | ["\"Task Owner\""] | ["COUNT(*)"] | 289 | 0.979 |
| [S9/Q7](#s9) | success | ["sheet1"] | 0 / {} | [] | [] | 30 | 0.457 |
| [S10/Q8](#s10) | success | ["sheet1"] | 0 / {} | ["\"Task Type\"", "\"Task Status\""] | ["COUNT(*)"] | 16 | 0.83 |
| [S11/Q9](#s11) | success | ["sheet1"] | 0 / {} | ["\"Task Type\"", "\"Task Status\""] | ["COUNT(*)"] | 16 | 0.762 |
| [S12/Q10](#s12) | success | ["sheet1"] | 0 / {} | [] | ["COUNT(*)", "SUM(CASE WHEN \"Task Status\" = 'Completed' THEN 1 ELSE 0 END)", "SUM(CASE WHEN \"Task Status\" = 'In Progress' THEN 1 ELSE 0 END)", "SUM(CASE WHEN \"Task Status\" = 'Not Started' THEN 1 ELSE 0 END)", "SUM(CASE WHEN \"Task Status\" = 'Paused' THEN 1 ELSE 0 END)"] | 1 | 0.661 |
| [S13/Q11](#s13) | success | ["sheet1"] | 0 / {} | [] | ["MIN(\"Planned Work Hours\")", "MAX(\"Planned Work Hours\")", "AVG(\"Planned Work Hours\")", "SUM(CASE WHEN \"Actual Work Hours\" = '-' OR \"Actual Work Hours\" = '' OR \"Actual Work Hours\" IS NULL THEN 1 ELSE 0 END)", "SUM(CASE WHEN \"Completion Quality Score\" = '-' OR \"Completion Quality Score\" = '' OR \"Completion Quality Score\" IS NULL THEN 1 ELSE 0 END)", "SUM(CASE WHEN \"Rework Count\" = '-' OR \"Rework Count\" = '' OR \"Rework Count\" IS NULL THEN 1 ELSE 0 END)"] | 1 | 0.796 |
| [S14/Q12](#s14) | success | ["sheet1"] | 0 / {} | [] | ["MIN(\"Task Difficulty Coefficient\")", "MAX(\"Task Difficulty Coefficient\")", "AVG(\"Task Difficulty Coefficient\")"] | 1 | 0.525 |
| [S15/Q13](#s15) | success | ["sheet1"] | 0 / {} | ["\"Task Type\""] | ["COUNT(*)", "AVG(CAST(\"Completion Quality Score\" AS REAL))", "AVG(\"Task Difficulty Coefficient\")", "AVG(CAST(\"Actual Work Hours\" AS REAL))", "AVG(\"Planned Work Hours\")", "AVG(CAST(\"Actual Work Hours\" AS REAL) * 1.0 / \"Planned Work Hours\")", "AVG(CAST(\"Rework Count\" AS INTEGER))"] | 4 | 1.052 |
| [S16/Q14](#s16) | success | ["sheet1"] | 0 / {} | ["\"Priority\""] | ["COUNT(*)", "AVG(CAST(\"Completion Quality Score\" AS REAL))", "AVG(\"Task Difficulty Coefficient\")"] | 4 | 0.72 |
| [S17/Q15](#s17) | success | ["sheet1"] | 0 / {} | ["\"Task Owner\"", "\"Task Type\""] | ["COUNT(*)", "SUM(CASE WHEN \"Task Status\" = 'Completed' THEN 1 ELSE 0 END)"] | 290 | 1.331 |
| [S18/Q16](#s18) | success | ["sheet1"] | 0 / {} | [] | [] | 30 | 0.578 |
| [S19/Q17](#s19) | success | ["sheet1"] | 0 / {} | [] | ["MIN(\"Completion Quality Score\")", "MAX(\"Completion Quality Score\")"] | 1 | 0.589 |
| [S20/Q18](#s20) | success | ["sheet1"] | 0 / {} | [] | ["MIN(\"Rework Count\")", "MAX(\"Rework Count\")"] | 1 | 0.507 |
| [S21/Q19](#s21) | success | ["sheet1"] | 0 / {} | ["\"Task Owner\"", "CASE WHEN task_cnt <= 2 THEN '1-2' WHEN task_cnt <= 5 THEN '3-5' WHEN task_cnt <= 10 THEN '6-10' ELSE '11+' END"] | ["COUNT(*)", "COUNT(*)", "MIN(task_cnt)"] | 4 | 0.91 |
| [S22/Q20](#s22) | success | ["sheet1"] | 0 / {} | ["\"Task Owner\"", "CASE WHEN task_cnt <= 2 THEN '1-2' WHEN task_cnt <= 5 THEN '3-5' WHEN task_cnt <= 10 THEN '6-10' ELSE '11+' END"] | ["SUM(CASE WHEN \"Task Status\" = 'Completed' THEN 1 ELSE 0 END)", "COUNT(*)", "MIN(task_cnt)"] | 4 | 1.086 |
| [S23/Q21](#s23) | success | ["sheet1"] | 0 / {} | ["\"Task Owner\""] | ["COUNT(*)", "SUM(CASE WHEN \"Task Status\" = 'Completed' THEN 1 ELSE 0 END)", "SUM(CASE WHEN \"Task Status\" = 'In Progress' THEN 1 ELSE 0 END)", "SUM(CASE WHEN \"Task Status\" = 'Not Started' THEN 1 ELSE 0 END)", "SUM(CASE WHEN \"Task Status\" = 'Paused' THEN 1 ELSE 0 END)"] | 30 | 1.302 |
| [S24/Q22](#s24) | success | ["sheet1"] | 0 / {} | ["\"Task Owner\"", "CASE WHEN completed = 0 THEN '0 completed' WHEN completed = 1 THEN '1 completed' WHEN completed BETWEEN 2 AND 4 THEN '2-4 completed' ELSE '5+ completed' END"] | ["SUM(CASE WHEN \"Task Status\" = 'Completed' THEN 1 ELSE 0 END)", "COUNT(*)", "COUNT(*)", "MIN(completed)"] | 4 | 1.04 |
| [S25/Q23](#s25) | success | ["sheet1"] | 0 / {} | ["\"Task Type\""] | ["COUNT(DISTINCT \"Task Owner\")"] | 4 | 0.777 |
| [S26/Q24](#s26) | success | ["sheet1"] | 0 / {} | ["\"Task Owner\""] | ["COUNT(DISTINCT \"Task Type\")", "COUNT(*)"] | 1 | 1.102 |
| [S27/Q25](#s27) | success | ["sheet1"] | 0 / {} | ["\"Task Type\""] | ["AVG(\"Task Difficulty Coefficient\")", "AVG(\"Planned Work Hours\")", "AVG(CASE WHEN \"Task Status\" = 'Completed' THEN CAST(\"Actual Work Hours\" AS REAL) END)", "AVG(CASE WHEN \"Task Status\" = 'Completed' THEN CAST(\"Completion Quality Score\" AS REAL) END)"] | 4 | 1.095 |
| [S28/Q26](#s28) | success | ["sheet1"] | 0 / {} | ["\"Task Status\""] | ["AVG(\"Task Difficulty Coefficient\")", "AVG(\"Planned Work Hours\")"] | 4 | 0.744 |
| [S29/Q27](#s29) | success | ["sheet1"] | 0 / {} | ["\"Priority\"", "\"Task Status\""] | ["COUNT(*)"] | 16 | 0.779 |
| [S30/Q28](#s30) | success | ["sheet1"] | 0 / {} | ["\"Task Owner\""] | ["MAX(\"Task Type\")", "COUNT(*)", "SUM(completed)", "AVG(quality)", "AVG(eff)", "AVG(CASE WHEN NOT rework IS NULL THEN 1 - rework / 3.0 END)", "AVG(late_days)", "AVG(\"Task Difficulty Coefficient\")", "COUNT(*)", "SUM(completed)", "SUM(on_time)", "SUM(completed)", "SUM(pw * completed)", "SUM(pw)"] | 289 | 4.183 |
| [S31/Q29](#s31) | success | ["sheet1"] | 0 / {} | ["\"Task Owner\""] | ["COUNT(*)", "SUM(completed)", "AVG(quality)", "AVG(eff)", "AVG(CASE WHEN NOT rework IS NULL THEN 1 - rework / 3.0 END)", "COUNT(*)", "SUM(completed)", "SUM(on_time)", "SUM(completed)", "SUM(CASE WHEN \"Priority\" = 'Urgent' THEN 4 WHEN \"Priority\" = 'High' THEN 3 WHEN \"Priority\" = 'Medium' THEN 2 WHEN \"Priority\" = 'Low' THEN 1 END * completed)", "SUM(CASE WHEN \"Priority\" = 'Urgent' THEN 4 WHEN \"Priority\" = 'High' THEN 3 WHEN \"Priority\" = 'Medium' THEN 2 WHEN \"Priority\" = 'Low' THEN 1 END)", "AVG(completion_rate)", "AVG(CASE WHEN completed_tasks > 0 THEN on_time_rate END)", "AVG(CASE WHEN completed_tasks > 0 THEN avg_quality END)", "AVG(priority_weighted_completion)", "AVG(CASE WHEN completed_tasks > 0 THEN hours_efficiency END)", "AVG(CASE WHEN completed_tasks > 0 THEN rework_avoidance END)"] | 1 | 2.412 |
| [S32/Q30](#s32) | success | ["sheet1"] | 0 / {} | ["\"Task Owner\"", "\"Task Type\"", "\"Task Type\""] | ["COUNT(*)", "SUM(CASE WHEN \"Task Status\" = 'Completed' THEN 1 ELSE 0 END)", "SUM(CASE WHEN \"Task Status\" = 'Completed' AND \"Actual Completion Time\" <> '-' AND \"Planned Deadline\" <> '-' AND JULIANDAY(\"Actual Completion Time\") <= JULIANDAY(\"Planned Deadline\") THEN 1 ELSE 0 END)", "SUM(CASE WHEN \"Task Status\" = 'Completed' AND \"Completion Quality Score\" <> '-' THEN CAST(\"Completion Quality Score\" AS REAL) ELSE 0 END)", "AVG(1.0 * completed / total)", "AVG(CASE WHEN completed > 0 THEN on_time / completed END)", "AVG(CASE WHEN completed > 0 THEN quality_sum / completed END)"] | 4 | 1.65 |
| [S33/Q31](#s33) | success | ["sheet1"] | 0 / {} | ["\"Task Owner\""] | ["MAX(\"Task Type\")", "COUNT(*)", "SUM(completed)", "AVG(eff)", "AVG(CASE WHEN NOT rework IS NULL THEN 1 - rework / 3.0 END)", "SUM(CASE WHEN \"Priority\" IN ('Urgent', 'High') THEN 1 ELSE 0 END)", "SUM(CASE WHEN \"Priority\" IN ('Urgent', 'High') AND completed = 1 THEN 1 ELSE 0 END)", "SUM(CASE WHEN \"Priority\" IN ('Urgent', 'High') AND on_time = 1 THEN 1 ELSE 0 END)", "COUNT(*)", "AVG(quality)", "AVG(\"Task Difficulty Coefficient\")", "SUM(completed)", "SUM(on_time)", "SUM(completed)", "SUM(CASE WHEN \"Priority\" = 'Urgent' THEN 4 WHEN \"Priority\" = 'High' THEN 3 WHEN \"Priority\" = 'Medium' THEN 2 WHEN \"Priority\" = 'Low' THEN 1 END * completed)", "SUM(CASE WHEN \"Priority\" = 'Urgent' THEN 4 WHEN \"Priority\" = 'High' THEN 3 WHEN \"Priority\" = 'Medium' THEN 2 WHEN \"Priority\" = 'Low' THEN 1 END)"] | 289 | 3.951 |
| [S34/Q32](#s34) | success | ["sheet1"] | 0 / {} | ["\"Task Owner\""] | ["MAX(\"Task Type\")", "COUNT(*)", "SUM(completed)", "AVG(eff)", "AVG(CASE WHEN NOT rework IS NULL THEN 1 - rework / 3.0 END)", "SUM(CASE WHEN \"Priority\" IN ('Urgent', 'High') THEN 1 ELSE 0 END)", "SUM(CASE WHEN \"Priority\" IN ('Urgent', 'High') AND completed = 1 THEN 1 ELSE 0 END)", "SUM(CASE WHEN \"Priority\" IN ('Urgent', 'High') AND on_time = 1 THEN 1 ELSE 0 END)", "COUNT(*)", "AVG(quality)", "AVG(\"Task Difficulty Coefficient\")", "SUM(completed)", "SUM(on_time)", "SUM(completed)", "SUM(CASE WHEN \"Priority\" = 'Urgent' THEN 4 WHEN \"Priority\" = 'High' THEN 3 WHEN \"Priority\" = 'Medium' THEN 2 WHEN \"Priority\" = 'Low' THEN 1 END * completed)", "SUM(CASE WHEN \"Priority\" = 'Urgent' THEN 4 WHEN \"Priority\" = 'High' THEN 3 WHEN \"Priority\" = 'Medium' THEN 2 WHEN \"Priority\" = 'Low' THEN 1 END)"] | 289 | 3.61 |
| [S35/Q33](#s35) | success | ["sheet1"] | 0 / {} | ["\"Task Owner\""] | ["MAX(\"Task Type\")", "COUNT(*)", "SUM(completed)", "SUM(CASE WHEN \"Task Status\" = 'Completed' AND \"Actual Completion Time\" <> '-' AND \"Planned Deadline\" <> '-' THEN 1 ELSE 0 END)", "SUM(CASE WHEN \"Task Status\" = 'Completed' AND \"Completion Quality Score\" <> '-' THEN 1 ELSE 0 END)", "SUM(CASE WHEN \"Task Status\" = 'Completed' AND \"Actual Work Hours\" <> '-' AND \"Planned Work Hours\" > 0 THEN 1 ELSE 0 END)", "SUM(CASE WHEN \"Task Status\" = 'Completed' AND \"Rework Count\" <> '-' THEN 1 ELSE 0 END)", "AVG(eff)", "AVG(CASE WHEN NOT rework IS NULL THEN 1 - rework / 3.0 END)", "COUNT(*)", "AVG(quality)", "SUM(completed)", "SUM(on_time)", "SUM(completed)", "SUM(CASE WHEN \"Priority\" = 'Urgent' THEN 4 WHEN \"Priority\" = 'High' THEN 3 WHEN \"Priority\" = 'Medium' THEN 2 WHEN \"Priority\" = 'Low' THEN 1 END * completed)", "SUM(CASE WHEN \"Priority\" = 'Urgent' THEN 4 WHEN \"Priority\" = 'High' THEN 3 WHEN \"Priority\" = 'Medium' THEN 2 WHEN \"Priority\" = 'Low' THEN 1 END)"] | 289 | 3.662 |
| [S36/Q34](#s36) | success | ["sheet1"] | 0 / {} | ["\"Task Owner\""] | ["MAX(\"Task Type\")", "COUNT(*)", "SUM(completed)", "SUM(CASE WHEN \"Task Status\" = 'Completed' AND \"Actual Completion Time\" <> '-' AND \"Planned Deadline\" <> '-' THEN 1 ELSE 0 END)", "SUM(CASE WHEN \"Task Status\" = 'Completed' AND \"Completion Quality Score\" <> '-' THEN 1 ELSE 0 END)", "SUM(CASE WHEN \"Task Status\" = 'Completed' AND \"Actual Work Hours\" <> '-' AND \"Planned Work Hours\" > 0 THEN 1 ELSE 0 END)", "SUM(CASE WHEN \"Task Status\" = 'Completed' AND \"Rework Count\" <> '-' THEN 1 ELSE 0 END)", "AVG(eff)", "AVG(CASE WHEN NOT rework IS NULL THEN 1 - rework / 3.0 END)", "SUM(CASE WHEN \"Priority\" IN ('Urgent', 'High') THEN 1 ELSE 0 END)", "SUM(CASE WHEN \"Priority\" IN ('Urgent', 'High') AND completed = 1 THEN 1 ELSE 0 END)", "COUNT(*)", "AVG(quality)", "SUM(completed)", "SUM(on_time)", "SUM(completed)", "SUM(CASE WHEN \"Priority\" = 'Urgent' THEN 4 WHEN \"Priority\" = 'High' THEN 3 WHEN \"Priority\" = 'Medium' THEN 2 WHEN \"Priority\" = 'Low' THEN 1 END * completed)", "SUM(CASE WHEN \"Priority\" = 'Urgent' THEN 4 WHEN \"Priority\" = 'High' THEN 3 WHEN \"Priority\" = 'Medium' THEN 2 WHEN \"Priority\" = 'Low' THEN 1 END)"] | 289 | 3.984 |
| [S37/Q35](#s37) | success | ["sheet1"] | 0 / {} | ["\"Task Owner\""] | ["AVG(\"Task Difficulty Coefficient\")"] | 289 | 1.13 |


## 元数据和设置

| SQL | 类别 | 状态 | 内容 |
| --- | --- | --- | --- |
| S1 | connection_setup | success | PRAGMA query_only=ON |
| S2 | metadata | success | SELECT name,sql FROM sqlite_master WHERE type='table' ORDER BY name |


## Python 与执行位置

人工源码审查：**database_first_violation**。Owner-level metrics are prepared in SQL, but Python builds within-type percentile ranks, weighted scores, shrinkage arithmetic, 20/70/10 classifications and grouped summaries. P19 is a concrete final classification implementation; these calculations can reasonably use SQLite aggregates/windows/CASE. Correlation and figure rendering are separate statistical/visual uses. No task rerun is performed for these deviations. [证据](../reviews/dacomp-013.json)。

P1：Compute within-task-type percentile ranks of each raw performance sub-metric, build a weighted composite score, and apply the exact global 20/70/10 classification cutoffs. This percentile normalization and classification logic is a statistical procedure better done in Python than in SQLite.

[源码](../../../runs/dsv4flash-db-first-full-01/dacomp-013/attempt-01/python/P1.py)；[输出](../../../runs/dsv4flash-db-first-full-01/dacomp-013/attempt-01/python/P1.stdout)；[错误](../../../runs/dsv4flash-db-first-full-01/dacomp-013/attempt-01/python/P1.stderr)。检出需人工核验的 SQL 可实现操作：.query(；不能仅凭理由判为合规。

P2：Build the weighted composite score using within-task-type percentile ranks for each performance sub-metric and inspect its distribution across types.

[源码](../../../runs/dsv4flash-db-first-full-01/dacomp-013/attempt-01/python/P2.py)；[输出](../../../runs/dsv4flash-db-first-full-01/dacomp-013/attempt-01/python/P2.stdout)；[错误](../../../runs/dsv4flash-db-first-full-01/dacomp-013/attempt-01/python/P2.stderr)。检出需人工核验的 SQL 可实现操作：groupby(；不能仅凭理由判为合规。

P3：Compute within-task-type percentile ranks, weighted composite score per owner, inspect distribution, and persist metrics for reuse.

[源码](../../../runs/dsv4flash-db-first-full-01/dacomp-013/attempt-01/python/P3.py)；[输出](../../../runs/dsv4flash-db-first-full-01/dacomp-013/attempt-01/python/P3.stdout)；[错误](../../../runs/dsv4flash-db-first-full-01/dacomp-013/attempt-01/python/P3.stderr)。检出需人工核验的 SQL 可实现操作：groupby(, .query(；不能仅凭理由判为合规。

P4：Apply the 20/70/10 global classification cutoffs on the composite score and examine class characteristics across types and metrics.

[源码](../../../runs/dsv4flash-db-first-full-01/dacomp-013/attempt-01/python/P4.py)；[输出](../../../runs/dsv4flash-db-first-full-01/dacomp-013/attempt-01/python/P4.stdout)；[错误](../../../runs/dsv4flash-db-first-full-01/dacomp-013/attempt-01/python/P4.stderr)。检出需人工核验的 SQL 可实现操作：groupby(, sort_values(；不能仅凭理由判为合规。

P5：Inspect classification boundaries and verify that Needs Improvement class is not unfairly excluding any type.

[源码](../../../runs/dsv4flash-db-first-full-01/dacomp-013/attempt-01/python/P5.py)；[输出](../../../runs/dsv4flash-db-first-full-01/dacomp-013/attempt-01/python/P5.stdout)；[错误](../../../runs/dsv4flash-db-first-full-01/dacomp-013/attempt-01/python/P5.stderr)。检出需人工核验的 SQL 可实现操作：groupby(；不能仅凭理由判为合规。

P6：Inspect the bottom boundary region where Good and Needs Improvement meet, to design a fair tie-breaker.

[源码](../../../runs/dsv4flash-db-first-full-01/dacomp-013/attempt-01/python/P6.py)；[输出](../../../runs/dsv4flash-db-first-full-01/dacomp-013/attempt-01/python/P6.stdout)；[错误](../../../runs/dsv4flash-db-first-full-01/dacomp-013/attempt-01/python/P6.stderr)。检出需人工核验的 SQL 可实现操作：sort_values(；不能仅凭理由判为合规。

P7：Recompute classification with principled tie-breaking: secondary sort by completed_tasks asc, total_tasks desc.

[源码](../../../runs/dsv4flash-db-first-full-01/dacomp-013/attempt-01/python/P7.py)；[输出](../../../runs/dsv4flash-db-first-full-01/dacomp-013/attempt-01/python/P7.stdout)；[错误](../../../runs/dsv4flash-db-first-full-01/dacomp-013/attempt-01/python/P7.stderr)。检出需人工核验的 SQL 可实现操作：groupby(, sort_values(；不能仅凭理由判为合规。

P8：Verify how the tie-breaker resolved boundary ties at composite 0.1133.

[源码](../../../runs/dsv4flash-db-first-full-01/dacomp-013/attempt-01/python/P8.py)；[输出](../../../runs/dsv4flash-db-first-full-01/dacomp-013/attempt-01/python/P8.stdout)；[错误](../../../runs/dsv4flash-db-first-full-01/dacomp-013/attempt-01/python/P8.stderr)。检出需人工核验的 SQL 可实现操作：sort_values(；不能仅凭理由判为合规。

P9：Apply corrected tie-breaker (more incomplete workload = worse) and test whether within-type difficulty correlates with outcomes to validate the normalization approach.

[源码](../../../runs/dsv4flash-db-first-full-01/dacomp-013/attempt-01/python/P9.py)；[输出](../../../runs/dsv4flash-db-first-full-01/dacomp-013/attempt-01/python/P9.stdout)；[错误](../../../runs/dsv4flash-db-first-full-01/dacomp-013/attempt-01/python/P9.stderr)。检出需人工核验的 SQL 可实现操作：groupby(, sort_values(；不能仅凭理由判为合规。

P10：Examine detailed characteristics of each classification class to validate the evaluation plan.

[源码](../../../runs/dsv4flash-db-first-full-01/dacomp-013/attempt-01/python/P10.py)；[输出](../../../runs/dsv4flash-db-first-full-01/dacomp-013/attempt-01/python/P10.stdout)；[错误](../../../runs/dsv4flash-db-first-full-01/dacomp-013/attempt-01/python/P10.stderr)。检出需人工核验的 SQL 可实现操作：groupby(, sort_values(；不能仅凭理由判为合规。

P11：Generate diagnostic visualizations of the evaluation plan: composite score distribution, type balance, class proportions, and radar chart of sub-metrics.

[源码](../../../runs/dsv4flash-db-first-full-01/dacomp-013/attempt-01/python/P11.py)；[输出](../../../runs/dsv4flash-db-first-full-01/dacomp-013/attempt-01/python/P11.stdout)；[错误](../../../runs/dsv4flash-db-first-full-01/dacomp-013/attempt-01/python/P11.stderr)。检出需人工核验的 SQL 可实现操作：groupby(；不能仅凭理由判为合规。

P12：Detailed breakdown of each classification class's characteristics across all metrics.

[源码](../../../runs/dsv4flash-db-first-full-01/dacomp-013/attempt-01/python/P12.py)；[输出](../../../runs/dsv4flash-db-first-full-01/dacomp-013/attempt-01/python/P12.stdout)；[错误](../../../runs/dsv4flash-db-first-full-01/dacomp-013/attempt-01/python/P12.stderr)。检出需人工核验的 SQL 可实现操作：groupby(；不能仅凭理由判为合规。

P13：Check how high-volume owners are classified to assess plan behavior for owners with substantial work history.

[源码](../../../runs/dsv4flash-db-first-full-01/dacomp-013/attempt-01/python/P13.py)；[输出](../../../runs/dsv4flash-db-first-full-01/dacomp-013/attempt-01/python/P13.stdout)；[错误](../../../runs/dsv4flash-db-first-full-01/dacomp-013/attempt-01/python/P13.stderr)。检出需人工核验的 SQL 可实现操作：sort_values(；不能仅凭理由判为合规。

P14：Fetch owner-level metrics with per-metric sample counts needed for credibility (shrinkage) adjustment.

[源码](../../../runs/dsv4flash-db-first-full-01/dacomp-013/attempt-01/python/P14.py)；[输出](../../../runs/dsv4flash-db-first-full-01/dacomp-013/attempt-01/python/P14.stdout)；[错误](../../../runs/dsv4flash-db-first-full-01/dacomp-013/attempt-01/python/P14.stderr)。检出需人工核验的 SQL 可实现操作：.query(；不能仅凭理由判为合规。

P15：Implement credibility-shrinkage adjustment (K=5) on each sub-metric toward type mean, then percentile rank within type and classify, to avoid small-sample distortion.

[源码](../../../runs/dsv4flash-db-first-full-01/dacomp-013/attempt-01/python/P15.py)；[输出](../../../runs/dsv4flash-db-first-full-01/dacomp-013/attempt-01/python/P15.stdout)；[错误](../../../runs/dsv4flash-db-first-full-01/dacomp-013/attempt-01/python/P15.stderr)。检出需人工核验的 SQL 可实现操作：groupby(, sort_values(；不能仅凭理由判为合规。

P16：Compare shrinkage constants K=5,10,15 to choose a plan that balances evidence sufficiency across classes.

[源码](../../../runs/dsv4flash-db-first-full-01/dacomp-013/attempt-01/python/P16.py)；[输出](../../../runs/dsv4flash-db-first-full-01/dacomp-013/attempt-01/python/P16.stdout)；[错误](../../../runs/dsv4flash-db-first-full-01/dacomp-013/attempt-01/python/P16.stderr)。检出需人工核验的 SQL 可实现操作：groupby(, sort_values(；不能仅凭理由判为合规。

P17：Validate the final K=10 classification plan: class characteristics, boundaries, and sample composition.

[源码](../../../runs/dsv4flash-db-first-full-01/dacomp-013/attempt-01/python/P17.py)；[输出](../../../runs/dsv4flash-db-first-full-01/dacomp-013/attempt-01/python/P17.stdout)；[错误](../../../runs/dsv4flash-db-first-full-01/dacomp-013/attempt-01/python/P17.stderr)。检出需人工核验的 SQL 可实现操作：groupby(, sort_values(；不能仅凭理由判为合规。

P18：Fetch full owner metrics including high-priority columns for final classification.

[源码](../../../runs/dsv4flash-db-first-full-01/dacomp-013/attempt-01/python/P18.py)；[输出](../../../runs/dsv4flash-db-first-full-01/dacomp-013/attempt-01/python/P18.stdout)；[错误](../../../runs/dsv4flash-db-first-full-01/dacomp-013/attempt-01/python/P18.stderr)。检出需人工核验的 SQL 可实现操作：.query(；不能仅凭理由判为合规。

P19：Build the final K=10 classification with high-priority metrics and save the definitive results file.

[源码](../../../runs/dsv4flash-db-first-full-01/dacomp-013/attempt-01/python/P19.py)；[输出](../../../runs/dsv4flash-db-first-full-01/dacomp-013/attempt-01/python/P19.stdout)；[错误](../../../runs/dsv4flash-db-first-full-01/dacomp-013/attempt-01/python/P19.stderr)。检出需人工核验的 SQL 可实现操作：groupby(, sort_values(；不能仅凭理由判为合规。

P20：Check high-priority task completion details per class.

[源码](../../../runs/dsv4flash-db-first-full-01/dacomp-013/attempt-01/python/P20.py)；[输出](../../../runs/dsv4flash-db-first-full-01/dacomp-013/attempt-01/python/P20.stdout)；[错误](../../../runs/dsv4flash-db-first-full-01/dacomp-013/attempt-01/python/P20.stderr)。自动源码筛查未检出预设迁出信号；这不是全面语义合规证明。

P21：Create the final report figure set: distribution, type balance, class mix, and radar chart.

[源码](../../../runs/dsv4flash-db-first-full-01/dacomp-013/attempt-01/python/P21.py)；[输出](../../../runs/dsv4flash-db-first-full-01/dacomp-013/attempt-01/python/P21.stdout)；[错误](../../../runs/dsv4flash-db-first-full-01/dacomp-013/attempt-01/python/P21.stderr)。检出需人工核验的 SQL 可实现操作：groupby(；不能仅凭理由判为合规。

P22：Compute final statistics for the report.

[源码](../../../runs/dsv4flash-db-first-full-01/dacomp-013/attempt-01/python/P22.py)；[输出](../../../runs/dsv4flash-db-first-full-01/dacomp-013/attempt-01/python/P22.stdout)；[错误](../../../runs/dsv4flash-db-first-full-01/dacomp-013/attempt-01/python/P22.stderr)。检出需人工核验的 SQL 可实现操作：groupby(；不能仅凭理由判为合规。

P23：Inspect the composition of the Needs Improvement class in the final shrunk plan.

[源码](../../../runs/dsv4flash-db-first-full-01/dacomp-013/attempt-01/python/P23.py)；[输出](../../../runs/dsv4flash-db-first-full-01/dacomp-013/attempt-01/python/P23.stdout)；[错误](../../../runs/dsv4flash-db-first-full-01/dacomp-013/attempt-01/python/P23.stderr)。检出需人工核验的 SQL 可实现操作：sort_values(；不能仅凭理由判为合规。

P24：Compute difficulty coefficients and final summary tables for the report.

[源码](../../../runs/dsv4flash-db-first-full-01/dacomp-013/attempt-01/python/P24.py)；[输出](../../../runs/dsv4flash-db-first-full-01/dacomp-013/attempt-01/python/P24.stdout)；[错误](../../../runs/dsv4flash-db-first-full-01/dacomp-013/attempt-01/python/P24.stderr)。检出需人工核验的 SQL 可实现操作：groupby(, .merge(, .query(；不能仅凭理由判为合规。

## 优化机会

已验证候选。筛选限于精确 SQL、相同自包含 CTE、相同单表完整过滤、可分解单表聚合；未覆盖任意 Join 等价和一般谓词蕴含。全部候选都是 offline，未测在线预测。

| 候选 | 类型 | 已有结果 | 覆盖 SQL | 后续次数 | 中间行数 | 验证 | 成本 |
| --- | --- | --- | --- | --- | --- | --- | --- |
| C1 | exact-result reuse | True | ["S10", "S11"] | 1 | unknown | not_verified_cap | Not tested |
| C2 | exact-result reuse | True | ["S33", "S34"] | 1 | 289 | verified | Not benchmarked; correctness alone does not establish net speedup. |
| C3 | common subexpression | False | ["S31", "S33", "S34"] | 2 | 799 | verified | Not benchmarked; correctness alone does not establish net speedup. |
| C4 | aggregate MV | False | ["S4", "S5", "S6", "S7", "S8", "S10", "S11", "S12", "S13", "S14", "S17", "S27", "S28", "S29", "S37"] | 14 | 596 | rejected_result_mismatch | Not benchmarked; correctness alone does not establish net speedup. |


已验证覆盖（含触发查询、候选并集去重）：3/35 条成功数据 SQL。正确性仅针对当前数据库快照；未测性能的候选不能声称已加速。

[完整 build/rewrite 与比较证据](dacomp-013.analysis.json)。

### C3：common subexpression

Identical self-contained CTE body across queries.

原查询 [S31](#s31), [S33](#s33), [S34](#s34) → 新增共享状态 C3 → 后续 2 次可复用。该构建点为事后假设，不代表 Agent 当时预知后续。

构建定义：

```sql
SELECT "Task Owner", "Task Type", "Task Status", "Priority", CASE WHEN "Task Status" = 'Completed' THEN 1 ELSE 0 END AS completed, CASE WHEN "Task Status" = 'Completed' AND "Actual Completion Time" <> '-' AND "Planned Deadline" <> '-' AND JULIANDAY("Actual Completion Time") <= JULIANDAY("Planned Deadline") THEN 1 ELSE 0 END AS on_time, CASE WHEN "Task Status" = 'Completed' AND "Completion Quality Score" <> '-' THEN CAST("Completion Quality Score" AS REAL) END AS quality, CASE WHEN "Task Status" = 'Completed' AND "Actual Work Hours" <> '-' AND "Planned Work Hours" > 0 THEN MIN(("Planned Work Hours" * 1.0) / CAST("Actual Work Hours" AS REAL), 1.5) END AS eff, CASE WHEN "Task Status" = 'Completed' AND "Rework Count" <> '-' THEN CAST("Rework Count" AS INTEGER) END AS rework, "Task Difficulty Coefficient" FROM sheet1
```

受益查询 S31 的改写示例：

```sql
WITH t AS (SELECT * FROM temp.reuse_candidate) SELECT ROUND(AVG(completion_rate), 3) AS avg_completion_rate, ROUND(AVG(CASE WHEN completed_tasks > 0 THEN on_time_rate END), 3) AS avg_on_time, ROUND(AVG(CASE WHEN completed_tasks > 0 THEN avg_quality END), 3) AS avg_quality, ROUND(AVG(priority_weighted_completion), 3) AS avg_prio_completion, ROUND(AVG(CASE WHEN completed_tasks > 0 THEN hours_efficiency END), 3) AS avg_eff, ROUND(AVG(CASE WHEN completed_tasks > 0 THEN rework_avoidance END), 3) AS avg_rework_avoid FROM (SELECT "Task Owner", COUNT(*) AS total_tasks, SUM(completed) AS completed_tasks, 1.0 * SUM(completed) / COUNT(*) AS completion_rate, 1.0 * SUM(on_time) / NULLIF(SUM(completed), 0) AS on_time_rate, AVG(quality) AS avg_quality, 1.0 * SUM(CASE WHEN "Priority" = 'Urgent' THEN 4 WHEN "Priority" = 'High' THEN 3 WHEN "Priority" = 'Medium' THEN 2 WHEN "Priority" = 'Low' THEN 1 END * completed) / NULLIF(SUM(CASE WHEN "Priority" = 'Urgent' THEN 4 WHEN "Priority" = 'High' THEN 3 WHEN "Priority" = 'Medium' THEN 2 WHEN "Priority" = 'Low' THEN 1 END), 0) AS priority_weighted_completion, AVG(eff) AS hours_efficiency, AVG(CASE WHEN NOT rework IS NULL THEN 1 - rework / 3.0 END) AS rework_avoidance FROM t GROUP BY "Task Owner")
```

| 原 SQL | 列名一致 | 结果一致 | 比较方法 |
| --- | --- | --- | --- |
| S31 | True | True | exact_multiset |
| S33 | True | True | exact_multiset |
| S34 | True | True | exact_multiset |


验证状态：verified；成本结论：Not benchmarked; correctness alone does not establish net speedup.

### C2：exact-result reuse

Identical normalized SQL and parameters; archive equality checked.

原查询 [S33](#s33), [S34](#s34) → 保留前序结果 S33 → 后续 1 次可复用。该构建点为事后假设，不代表 Agent 当时预知后续。

| 原 SQL | 列名一致 | 结果一致 | 比较方法 |
| --- | --- | --- | --- |
| S34 | True | True | exact_multiset |


验证状态：verified；成本结论：Not benchmarked; correctness alone does not establish net speedup.

### C4：aggregate MV

Union of grouping keys; decomposable aggregate states; AVG uses SUM and non-NULL COUNT.

原查询 [S4](#s4), [S5](#s5), [S6](#s6), [S7](#s7), [S8](#s8), [S10](#s10), [S11](#s11), [S12](#s12), [S13](#s13), [S14](#s14), [S17](#s17), [S27](#s27), [S28](#s28), [S29](#s29), [S37](#s37) → 新增共享状态 C4 → 后续 14 次可复用。该构建点为事后假设，不代表 Agent 当时预知后续。

构建定义：

```sql
SELECT "Task Status" AS __g0, "Priority" AS __g1, "Task Type" AS __g2, "Task Owner" AS __g3, COUNT(*) AS __a0, SUM(CASE WHEN "Task Status" = 'Completed' THEN 1 ELSE 0 END) AS __a1, SUM(CASE WHEN "Task Status" = 'In Progress' THEN 1 ELSE 0 END) AS __a2, SUM(CASE WHEN "Task Status" = 'Not Started' THEN 1 ELSE 0 END) AS __a3, SUM(CASE WHEN "Task Status" = 'Paused' THEN 1 ELSE 0 END) AS __a4, MIN("Planned Work Hours") AS __a5, MAX("Planned Work Hours") AS __a6, SUM("Planned Work Hours") AS __a7_sum, COUNT("Planned Work Hours") AS __a7_n, SUM(CASE WHEN "Actual Work Hours" = '-' OR "Actual Work Hours" = '' OR "Actual Work Hours" IS NULL THEN 1 ELSE 0 END) AS __a8, SUM(CASE WHEN "Completion Quality Score" = '-' OR "Completion Quality Score" = '' OR "Completion Quality Score" IS NULL THEN 1 ELSE 0 END) AS __a9, SUM(CASE WHEN "Rework Count" = '-' OR "Rework Count" = '' OR "Rework Count" IS NULL THEN 1 ELSE 0 END) AS __a10, MIN("Task Difficulty Coefficient") AS __a11, MAX("Task Difficulty Coefficient") AS __a12, SUM("Task Difficulty Coefficient") AS __a13_sum, COUNT("Task Difficulty Coefficient") AS __a13_n, SUM(CASE WHEN "Task Status" = 'Completed' THEN CAST("Actual Work Hours" AS REAL) END) AS __a14_sum, COUNT(CASE WHEN "Task Status" = 'Completed' THEN CAST("Actual Work Hours" AS REAL) END) AS __a14_n, SUM(CASE WHEN "Task Status" = 'Completed' THEN CAST("Completion Quality Score" AS REAL) END) AS __a15_sum, COUNT(CASE WHEN "Task Status" = 'Completed' THEN CAST("Completion Quality Score" AS REAL) END) AS __a15_n FROM "sheet1"  GROUP BY "Task Status", "Priority", "Task Type", "Task Owner"
```

受益查询 S4 的改写示例：

```sql
SELECT SUM(__a0) AS total_rows FROM temp.reuse_candidate
```

| 原 SQL | 列名一致 | 结果一致 | 比较方法 |
| --- | --- | --- | --- |
| S4 | True | True | exact_multiset |
| S5 | True | True | exact_multiset |
| S6 | True | True | exact_multiset |
| S7 | True | True | exact_multiset |
| S8 | True | True | ordered_numeric_tolerance |
| S10 | True | True | ordered_numeric_tolerance |
| S11 | True | True | ordered_numeric_tolerance |
| S12 | True | True | exact_multiset |
| S13 | True | True | exact_multiset |
| S14 | True | False | exact_multiset |
| S17 | True | True | ordered_numeric_tolerance |
| S27 | True | True | ordered_numeric_tolerance |
| S28 | True | True | ordered_numeric_tolerance |
| S29 | True | True | ordered_numeric_tolerance |
| S37 | True | True | exact_multiset |


验证状态：rejected_result_mismatch；成本结论：Not benchmarked; correctness alone does not establish net speedup.

结果依赖：自动记录 SQL→Python 的接口父调用，以及源码中引用归档文件的消费者；字面值相同不认定因果。模型方向选择需要人工读取消息，尚未做全面因果标注。

[原始报告](../../../runs/dsv4flash-db-first-full-01/dacomp-013/attempt-01/answer.md)；[统一消息](../../../runs/dsv4flash-db-first-full-01/dacomp-013/attempt-01/messages.jsonl)；[原始 OpenCode 事件](../../../runs/dsv4flash-db-first-full-01/dacomp-013/attempt-01/opencode.jsonl)；[SQL 引擎日志](../../../runs/dsv4flash-db-first-full-01/dacomp-013/attempt-01/sql_journal.jsonl)。

[可读报告（本地图片链接规范化）](../answers/dacomp-013.md)。原始回答保留，分析结论未改写。

## S1

类别 `connection_setup`；来源 `connection`；调用 `4252b3f1dd5545a4843f2572a71e7c22`；状态 `success`。

```sql
PRAGMA query_only=ON
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-013/attempt-01/sql/S1.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-013/attempt-01/sql/S1.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-013/attempt-01/results/S1.rows.jsonl)；完整：True；SHA256：`e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`。

## S2

类别 `metadata`；来源 `list_db`；调用 `4252b3f1dd5545a4843f2572a71e7c22`；状态 `success`。

```sql
SELECT name,sql FROM sqlite_master WHERE type='table' ORDER BY name
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-013/attempt-01/sql/S2.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-013/attempt-01/sql/S2.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-013/attempt-01/results/S2.rows.jsonl)；完整：True；SHA256：`a44f5118597c98205cadbd573edb9fa462d01fd13fde1c4d81c55b5bec43474f`。

## S3

类别 `data`；来源 `query_db`；调用 `81c520d7f502494fa1ae565ffed25bbe`；状态 `success`。

```sql
SELECT * FROM sheet1 LIMIT 20
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-013/attempt-01/sql/S3.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-013/attempt-01/sql/S3.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-013/attempt-01/results/S3.rows.jsonl)；完整：True；SHA256：`5623b59aeec1cdfa93be480494e1f1e78c263f643e46ca9e64b11956fdc6cd7d`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "sheet1", "kind": "base", "block": null, "base_tables": ["sheet1"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |


## S4

类别 `data`；来源 `query_db`；调用 `abeb62f7dad8480ebc444daccfad7f93`；状态 `success`。

```sql
SELECT COUNT(*) AS total_rows FROM sheet1
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-013/attempt-01/sql/S4.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-013/attempt-01/sql/S4.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-013/attempt-01/results/S4.rows.jsonl)；完整：True；SHA256：`8c89b3ce79a0aa2091706f49c78e259b9947d94e941b40e8c04b03c56dac877f`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "sheet1", "kind": "base", "block": null, "base_tables": ["sheet1"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |


## S5

类别 `data`；来源 `query_db`；调用 `273db2b9127942599716f8c66a360e02`；状态 `success`。

```sql
SELECT "Task Status", COUNT(*) AS cnt FROM sheet1 GROUP BY "Task Status"
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-013/attempt-01/sql/S5.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-013/attempt-01/sql/S5.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-013/attempt-01/results/S5.rows.jsonl)；完整：True；SHA256：`7b5e6ce3e6d8771af9f4b829ec68edead8309bcef66a34abeb147e1e9c1c163a`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "sheet1", "kind": "base", "block": null, "base_tables": ["sheet1"]}] | [] | ["\"Task Status\""] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |


## S6

类别 `data`；来源 `query_db`；调用 `43092a345efe4d44b2030c23470f0695`；状态 `success`。

```sql
SELECT "Priority", COUNT(*) AS cnt FROM sheet1 GROUP BY "Priority"
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-013/attempt-01/sql/S6.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-013/attempt-01/sql/S6.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-013/attempt-01/results/S6.rows.jsonl)；完整：True；SHA256：`bba8e1f474712db15dd6dc3598b82e2d101eb2ad616842f66ffb3197d12b1582`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "sheet1", "kind": "base", "block": null, "base_tables": ["sheet1"]}] | [] | ["\"Priority\""] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |


## S7

类别 `data`；来源 `query_db`；调用 `6cbd0bdb5fe0488b84786570d3140f10`；状态 `success`。

```sql
SELECT "Task Type", COUNT(*) AS cnt FROM sheet1 GROUP BY "Task Type"
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-013/attempt-01/sql/S7.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-013/attempt-01/sql/S7.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-013/attempt-01/results/S7.rows.jsonl)；完整：True；SHA256：`6350ac5de6f6a3cd1b2ed9bb7cb5ae17d4047d2a6a053a110e75674ce2e08e20`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "sheet1", "kind": "base", "block": null, "base_tables": ["sheet1"]}] | [] | ["\"Task Type\""] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |


## S8

类别 `data`；来源 `query_db`；调用 `7d23eaa5c6354dd1912d3c63152c1b39`；状态 `success`。

```sql
SELECT "Task Owner", COUNT(*) AS cnt FROM sheet1 GROUP BY "Task Owner" ORDER BY cnt DESC
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-013/attempt-01/sql/S8.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-013/attempt-01/sql/S8.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-013/attempt-01/results/S8.rows.jsonl)；完整：True；SHA256：`7b486e3fbf4b92627e95afd2813efb517aeaf9f9659c45c9078a7ede898b9293`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "sheet1", "kind": "base", "block": null, "base_tables": ["sheet1"]}] | [] | ["\"Task Owner\""] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |


## S9

类别 `data`；来源 `query_db`；调用 `fe39b0a7b2774d27a97addc69f5eaad7`；状态 `success`。

```sql
SELECT * FROM sheet1 LIMIT 30
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-013/attempt-01/sql/S9.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-013/attempt-01/sql/S9.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-013/attempt-01/results/S9.rows.jsonl)；完整：True；SHA256：`e68fa5f27f74e7bc4d429f550110e4db24e6b6ecb3a91fb49c637fc3283f51be`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "sheet1", "kind": "base", "block": null, "base_tables": ["sheet1"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |


## S10

类别 `data`；来源 `query_db`；调用 `9d243dbd3fbc42a1bcd5c84b7e1d268c`；状态 `success`。

```sql
SELECT "Task Type", "Task Status", COUNT(*) AS cnt
FROM sheet1 GROUP BY "Task Type", "Task Status" ORDER BY "Task Type", "Task Status"
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-013/attempt-01/sql/S10.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-013/attempt-01/sql/S10.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-013/attempt-01/results/S10.rows.jsonl)；完整：True；SHA256：`47960fd3f9effdaaa13384a98ea5036e2ccc4660ab0f4103f1c5d49b389cbbba`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "sheet1", "kind": "base", "block": null, "base_tables": ["sheet1"]}] | [] | ["\"Task Type\"", "\"Task Status\""] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |


## S11

类别 `data`；来源 `query_db`；调用 `d425b5888a0a4486a81bba907e877e36`；状态 `success`。

```sql
SELECT "Task Type", "Task Status", COUNT(*) AS cnt
FROM sheet1 GROUP BY "Task Type", "Task Status" ORDER BY "Task Type", "Task Status"
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-013/attempt-01/sql/S11.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-013/attempt-01/sql/S11.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-013/attempt-01/results/S11.rows.jsonl)；完整：True；SHA256：`47960fd3f9effdaaa13384a98ea5036e2ccc4660ab0f4103f1c5d49b389cbbba`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "sheet1", "kind": "base", "block": null, "base_tables": ["sheet1"]}] | [] | ["\"Task Type\"", "\"Task Status\""] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |


## S12

类别 `data`；来源 `query_db`；调用 `41af56e4b8c94f9786d194129d024f10`；状态 `success`。

```sql
SELECT
  COUNT(*) AS total,
  SUM(CASE WHEN "Task Status" = 'Completed' THEN 1 ELSE 0 END) AS completed,
  SUM(CASE WHEN "Task Status" = 'In Progress' THEN 1 ELSE 0 END) AS in_progress,
  SUM(CASE WHEN "Task Status" = 'Not Started' THEN 1 ELSE 0 END) AS not_started,
  SUM(CASE WHEN "Task Status" = 'Paused' THEN 1 ELSE 0 END) AS paused
FROM sheet1
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-013/attempt-01/sql/S12.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-013/attempt-01/sql/S12.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-013/attempt-01/results/S12.rows.jsonl)；完整：True；SHA256：`671d5fc4e57f38347e29aa0104572cb116a1b27d497d8d8e0fa95c7d010cb6b3`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "sheet1", "kind": "base", "block": null, "base_tables": ["sheet1"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |
| B1 | SUM(CASE WHEN "Task Status" = 'Completed' THEN 1 ELSE 0 END) | [] | [{"table": "sheet1", "column": "Task Status"}] | False |
| B1 | SUM(CASE WHEN "Task Status" = 'In Progress' THEN 1 ELSE 0 END) | [] | [{"table": "sheet1", "column": "Task Status"}] | False |
| B1 | SUM(CASE WHEN "Task Status" = 'Not Started' THEN 1 ELSE 0 END) | [] | [{"table": "sheet1", "column": "Task Status"}] | False |
| B1 | SUM(CASE WHEN "Task Status" = 'Paused' THEN 1 ELSE 0 END) | [] | [{"table": "sheet1", "column": "Task Status"}] | False |


## S13

类别 `data`；来源 `query_db`；调用 `890b8a269885469682489d04a2ee177a`；状态 `success`。

```sql
SELECT
  MIN("Planned Work Hours") AS min_planned, MAX("Planned Work Hours") AS max_planned,
  AVG("Planned Work Hours") AS avg_planned,
  SUM(CASE WHEN "Actual Work Hours" = '-' OR "Actual Work Hours" = '' OR "Actual Work Hours" IS NULL THEN 1 ELSE 0 END) AS missing_actual_hours,
  SUM(CASE WHEN "Completion Quality Score" = '-' OR "Completion Quality Score" = '' OR "Completion Quality Score" IS NULL THEN 1 ELSE 0 END) AS missing_quality,
  SUM(CASE WHEN "Rework Count" = '-' OR "Rework Count" = '' OR "Rework Count" IS NULL THEN 1 ELSE 0 END) AS missing_rework
FROM sheet1
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-013/attempt-01/sql/S13.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-013/attempt-01/sql/S13.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-013/attempt-01/results/S13.rows.jsonl)；完整：True；SHA256：`7327ca75bd63606730d6ae1a70a3fc81a7df4c9726689aaa8b006d2191413285`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "sheet1", "kind": "base", "block": null, "base_tables": ["sheet1"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | MIN("Planned Work Hours") | [{"table": "sheet1", "column": "Planned Work Hours"}] | [] | False |
| B1 | MAX("Planned Work Hours") | [{"table": "sheet1", "column": "Planned Work Hours"}] | [] | False |
| B1 | AVG("Planned Work Hours") | [{"table": "sheet1", "column": "Planned Work Hours"}] | [] | False |
| B1 | SUM(CASE WHEN "Actual Work Hours" = '-' OR "Actual Work Hours" = '' OR "Actual Work Hours" IS NULL THEN 1 ELSE 0 END) | [] | [{"table": "sheet1", "column": "Actual Work Hours"}, {"table": "sheet1", "column": "Actual Work Hours"}, {"table": "sheet1", "column": "Actual Work Hours"}] | False |
| B1 | SUM(CASE WHEN "Completion Quality Score" = '-' OR "Completion Quality Score" = '' OR "Completion Quality Score" IS NULL THEN 1 ELSE 0 END) | [] | [{"table": "sheet1", "column": "Completion Quality Score"}, {"table": "sheet1", "column": "Completion Quality Score"}, {"table": "sheet1", "column": "Completion Quality Score"}] | False |
| B1 | SUM(CASE WHEN "Rework Count" = '-' OR "Rework Count" = '' OR "Rework Count" IS NULL THEN 1 ELSE 0 END) | [] | [{"table": "sheet1", "column": "Rework Count"}, {"table": "sheet1", "column": "Rework Count"}, {"table": "sheet1", "column": "Rework Count"}] | False |


## S14

类别 `data`；来源 `query_db`；调用 `d62865b422e24244892a0fcae04955dd`；状态 `success`。

```sql
SELECT MIN("Task Difficulty Coefficient") AS min_diff, MAX("Task Difficulty Coefficient") AS max_diff, AVG("Task Difficulty Coefficient") AS avg_diff
FROM sheet1
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-013/attempt-01/sql/S14.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-013/attempt-01/sql/S14.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-013/attempt-01/results/S14.rows.jsonl)；完整：True；SHA256：`089368509f15e0b05056159af7e5fcbda210fff21b5ae89432bb296d4e30d475`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "sheet1", "kind": "base", "block": null, "base_tables": ["sheet1"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | MIN("Task Difficulty Coefficient") | [{"table": "sheet1", "column": "Task Difficulty Coefficient"}] | [] | False |
| B1 | MAX("Task Difficulty Coefficient") | [{"table": "sheet1", "column": "Task Difficulty Coefficient"}] | [] | False |
| B1 | AVG("Task Difficulty Coefficient") | [{"table": "sheet1", "column": "Task Difficulty Coefficient"}] | [] | False |


## S15

类别 `data`；来源 `query_db`；调用 `f2fde47ef24c4ddd8ca213640d0f1325`；状态 `success`。

```sql
SELECT
  "Task Type",
  COUNT(*) AS cnt,
  AVG(CAST("Completion Quality Score" AS REAL)) AS avg_quality,
  AVG("Task Difficulty Coefficient") AS avg_diff,
  AVG(CAST("Actual Work Hours" AS REAL)) AS avg_actual_hours,
  AVG("Planned Work Hours") AS avg_planned_hours,
  AVG(CAST("Actual Work Hours" AS REAL) * 1.0 / "Planned Work Hours") AS avg_hours_ratio,
  AVG(CAST("Rework Count" AS INTEGER)) AS avg_rework
FROM sheet1
WHERE "Task Status" = 'Completed'
  AND "Completion Quality Score" != '-'
  AND "Actual Work Hours" != '-'
  AND "Rework Count" != '-'
GROUP BY "Task Type"
ORDER BY "Task Type"
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-013/attempt-01/sql/S15.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-013/attempt-01/sql/S15.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-013/attempt-01/results/S15.rows.jsonl)；完整：True；SHA256：`dc95de787a3185e46bd5b0a9d0a960ee31a05bf60a5988dfc86b76f70ccbecb9`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "sheet1", "kind": "base", "block": null, "base_tables": ["sheet1"]}] | [] | ["\"Task Type\""] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |
| B1 | AVG(CAST("Completion Quality Score" AS REAL)) | [{"table": "sheet1", "column": "Completion Quality Score"}] | [] | False |
| B1 | AVG("Task Difficulty Coefficient") | [{"table": "sheet1", "column": "Task Difficulty Coefficient"}] | [] | False |
| B1 | AVG(CAST("Actual Work Hours" AS REAL)) | [{"table": "sheet1", "column": "Actual Work Hours"}] | [] | False |
| B1 | AVG("Planned Work Hours") | [{"table": "sheet1", "column": "Planned Work Hours"}] | [] | False |
| B1 | AVG(CAST("Actual Work Hours" AS REAL) * 1.0 / "Planned Work Hours") | [{"table": "sheet1", "column": "Planned Work Hours"}, {"table": "sheet1", "column": "Actual Work Hours"}] | [] | False |
| B1 | AVG(CAST("Rework Count" AS INTEGER)) | [{"table": "sheet1", "column": "Rework Count"}] | [] | False |


## S16

类别 `data`；来源 `query_db`；调用 `ba010a45f0f247b4a53680bba6de021a`；状态 `success`。

```sql
SELECT
  "Priority",
  COUNT(*) AS cnt,
  AVG(CAST("Completion Quality Score" AS REAL)) AS avg_quality,
  AVG("Task Difficulty Coefficient") AS avg_diff
FROM sheet1
WHERE "Task Status" = 'Completed'
  AND "Completion Quality Score" != '-'
GROUP BY "Priority"
ORDER BY "Priority"
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-013/attempt-01/sql/S16.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-013/attempt-01/sql/S16.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-013/attempt-01/results/S16.rows.jsonl)；完整：True；SHA256：`ac25ea1239e31f60d8abaf44439b8678d897d3f17df0d8033c4ea16f0a408abf`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "sheet1", "kind": "base", "block": null, "base_tables": ["sheet1"]}] | [] | ["\"Priority\""] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |
| B1 | AVG(CAST("Completion Quality Score" AS REAL)) | [{"table": "sheet1", "column": "Completion Quality Score"}] | [] | False |
| B1 | AVG("Task Difficulty Coefficient") | [{"table": "sheet1", "column": "Task Difficulty Coefficient"}] | [] | False |


## S17

类别 `data`；来源 `query_db`；调用 `d3cfd97f0d9840f789110b7786608f1a`；状态 `success`。

```sql
SELECT
  "Task Owner",
  "Task Type",
  COUNT(*) AS total_tasks,
  SUM(CASE WHEN "Task Status" = 'Completed' THEN 1 ELSE 0 END) AS completed_tasks
FROM sheet1
GROUP BY "Task Owner", "Task Type"
ORDER BY "Task Owner", "Task Type"
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-013/attempt-01/sql/S17.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-013/attempt-01/sql/S17.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-013/attempt-01/results/S17.rows.jsonl)；完整：True；SHA256：`a0c5c3dc8292ab7fce255afd0b90824420c591b0fc8e33476ca52600aaf5c436`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "sheet1", "kind": "base", "block": null, "base_tables": ["sheet1"]}] | [] | ["\"Task Owner\"", "\"Task Type\""] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |
| B1 | SUM(CASE WHEN "Task Status" = 'Completed' THEN 1 ELSE 0 END) | [] | [{"table": "sheet1", "column": "Task Status"}] | False |


## S18

类别 `data`；来源 `query_db`；调用 `a9104c4e72a34b51b974e11b87857aab`；状态 `success`。

```sql
SELECT "Task ID", "Planned Deadline", "Actual Completion Time"
FROM sheet1
WHERE "Task Status" = 'Completed'
ORDER BY "Task ID"
LIMIT 30
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-013/attempt-01/sql/S18.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-013/attempt-01/sql/S18.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-013/attempt-01/results/S18.rows.jsonl)；完整：True；SHA256：`d66ffa289f8ae8caaaf527fd61e9122a26aedd1368cc359db047d0841a684631`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "sheet1", "kind": "base", "block": null, "base_tables": ["sheet1"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |


## S19

类别 `data`；来源 `query_db`；调用 `f0042559c30148ed9e72260d7bcb93d2`；状态 `success`。

```sql
SELECT
  MIN("Completion Quality Score") AS min_q,
  MAX("Completion Quality Score") AS max_q
FROM sheet1 WHERE "Completion Quality Score" != '-'
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-013/attempt-01/sql/S19.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-013/attempt-01/sql/S19.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-013/attempt-01/results/S19.rows.jsonl)；完整：True；SHA256：`f42f4f51c6697311571dba2127a73060ed82ef12398e6dffffe69d7af8c2ce81`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "sheet1", "kind": "base", "block": null, "base_tables": ["sheet1"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | MIN("Completion Quality Score") | [{"table": "sheet1", "column": "Completion Quality Score"}] | [] | False |
| B1 | MAX("Completion Quality Score") | [{"table": "sheet1", "column": "Completion Quality Score"}] | [] | False |


## S20

类别 `data`；来源 `query_db`；调用 `b5b1632dea6b4d38b9f9945c1159b0a9`；状态 `success`。

```sql
SELECT MIN("Rework Count") AS min_r, MAX("Rework Count") AS max_r FROM sheet1 WHERE "Rework Count" != '-'
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-013/attempt-01/sql/S20.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-013/attempt-01/sql/S20.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-013/attempt-01/results/S20.rows.jsonl)；完整：True；SHA256：`192826c188cf06bd369ab043d774f061a6a376bda3a0ed93473f5db6ab383c85`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "sheet1", "kind": "base", "block": null, "base_tables": ["sheet1"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | MIN("Rework Count") | [{"table": "sheet1", "column": "Rework Count"}] | [] | False |
| B1 | MAX("Rework Count") | [{"table": "sheet1", "column": "Rework Count"}] | [] | False |


## S21

类别 `data`；来源 `query_db`；调用 `4508bdbc2aa9495ca989e5cb4d252991`；状态 `success`。

```sql
SELECT
  CASE
    WHEN task_cnt <= 2 THEN '1-2'
    WHEN task_cnt <= 5 THEN '3-5'
    WHEN task_cnt <= 10 THEN '6-10'
    ELSE '11+'
  END AS owner_task_bucket,
  COUNT(*) AS owner_count
FROM (
  SELECT "Task Owner", COUNT(*) AS task_cnt
  FROM sheet1
  GROUP BY "Task Owner"
)
GROUP BY owner_task_bucket
ORDER BY MIN(task_cnt)
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-013/attempt-01/sql/S21.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-013/attempt-01/sql/S21.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-013/attempt-01/results/S21.rows.jsonl)；完整：True；SHA256：`7785887ef91224f288382a9050d39f14ac811f884685a3408be4d7970cc536dc`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "sheet1", "kind": "base", "block": null, "base_tables": ["sheet1"]}] | [] | ["\"Task Owner\""] |
| B2 | [{"alias": "", "kind": "derived", "block": "B1", "base_tables": ["sheet1"]}] | [] | ["CASE WHEN task_cnt <= 2 THEN '1-2' WHEN task_cnt <= 5 THEN '3-5' WHEN task_cnt <= 10 THEN '6-10' ELSE '11+' END"] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |
| B2 | COUNT(*) | [] | [] | True |
| B2 | MIN(task_cnt) | [] | [] | False |


## S22

类别 `data`；来源 `query_db`；调用 `4a11692c1fad4e30a1f190812e485f9c`；状态 `success`。

```sql
SELECT
  CASE
    WHEN task_cnt <= 2 THEN '1-2'
    WHEN task_cnt <= 5 THEN '3-5'
    WHEN task_cnt <= 10 THEN '6-10'
    ELSE '11+'
  END AS owner_task_bucket,
  COUNT(*) AS owner_count
FROM (
  SELECT "Task Owner", SUM(CASE WHEN "Task Status" = 'Completed' THEN 1 ELSE 0 END) AS task_cnt
  FROM sheet1
  GROUP BY "Task Owner"
)
GROUP BY owner_task_bucket
ORDER BY MIN(task_cnt)
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-013/attempt-01/sql/S22.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-013/attempt-01/sql/S22.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-013/attempt-01/results/S22.rows.jsonl)；完整：True；SHA256：`5fb68b9ff226dea44a9fa5ffd9f1ee9b15c7f36986e8f59773e05386306c9ad0`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "sheet1", "kind": "base", "block": null, "base_tables": ["sheet1"]}] | [] | ["\"Task Owner\""] |
| B2 | [{"alias": "", "kind": "derived", "block": "B1", "base_tables": ["sheet1"]}] | [] | ["CASE WHEN task_cnt <= 2 THEN '1-2' WHEN task_cnt <= 5 THEN '3-5' WHEN task_cnt <= 10 THEN '6-10' ELSE '11+' END"] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | SUM(CASE WHEN "Task Status" = 'Completed' THEN 1 ELSE 0 END) | [] | [{"table": "sheet1", "column": "Task Status"}] | False |
| B2 | COUNT(*) | [] | [] | True |
| B2 | MIN(task_cnt) | [{"table": "sheet1", "column": "Task Status"}] | [] | False |


## S23

类别 `data`；来源 `query_db`；调用 `efb88cc15583410d9837180d60f8ec47`；状态 `success`。

```sql
SELECT
  "Task Owner",
  COUNT(*) AS total_tasks,
  SUM(CASE WHEN "Task Status" = 'Completed' THEN 1 ELSE 0 END) AS completed_tasks,
  SUM(CASE WHEN "Task Status" = 'In Progress' THEN 1 ELSE 0 END) AS in_progress,
  SUM(CASE WHEN "Task Status" = 'Not Started' THEN 1 ELSE 0 END) AS not_started,
  SUM(CASE WHEN "Task Status" = 'Paused' THEN 1 ELSE 0 END) AS paused
FROM sheet1
GROUP BY "Task Owner"
HAVING total_tasks >= 3
ORDER BY completed_tasks DESC
LIMIT 30
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-013/attempt-01/sql/S23.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-013/attempt-01/sql/S23.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-013/attempt-01/results/S23.rows.jsonl)；完整：True；SHA256：`156b7868face0f092de4042e9d6bcd049a52d99228b6bc9b52a049c4db8f717a`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "sheet1", "kind": "base", "block": null, "base_tables": ["sheet1"]}] | [] | ["\"Task Owner\""] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |
| B1 | SUM(CASE WHEN "Task Status" = 'Completed' THEN 1 ELSE 0 END) | [] | [{"table": "sheet1", "column": "Task Status"}] | False |
| B1 | SUM(CASE WHEN "Task Status" = 'In Progress' THEN 1 ELSE 0 END) | [] | [{"table": "sheet1", "column": "Task Status"}] | False |
| B1 | SUM(CASE WHEN "Task Status" = 'Not Started' THEN 1 ELSE 0 END) | [] | [{"table": "sheet1", "column": "Task Status"}] | False |
| B1 | SUM(CASE WHEN "Task Status" = 'Paused' THEN 1 ELSE 0 END) | [] | [{"table": "sheet1", "column": "Task Status"}] | False |


## S24

类别 `data`；来源 `query_db`；调用 `a59fe2bddabe4070bc14af6f89499838`；状态 `success`。

```sql
SELECT
  CASE
    WHEN completed = 0 THEN '0 completed'
    WHEN completed = 1 THEN '1 completed'
    WHEN completed BETWEEN 2 AND 4 THEN '2-4 completed'
    ELSE '5+ completed'
  END AS bucket,
  COUNT(*) AS owner_count
FROM (
  SELECT "Task Owner",
    SUM(CASE WHEN "Task Status" = 'Completed' THEN 1 ELSE 0 END) AS completed,
    COUNT(*) AS total
  FROM sheet1
  GROUP BY "Task Owner"
)
GROUP BY bucket
ORDER BY MIN(completed)
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-013/attempt-01/sql/S24.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-013/attempt-01/sql/S24.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-013/attempt-01/results/S24.rows.jsonl)；完整：True；SHA256：`8c25cce43245a75de12604300f996bbc9d1602527d8ec77732319ba5ec57c71d`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "sheet1", "kind": "base", "block": null, "base_tables": ["sheet1"]}] | [] | ["\"Task Owner\""] |
| B2 | [{"alias": "", "kind": "derived", "block": "B1", "base_tables": ["sheet1"]}] | [] | ["CASE WHEN completed = 0 THEN '0 completed' WHEN completed = 1 THEN '1 completed' WHEN completed BETWEEN 2 AND 4 THEN '2-4 completed' ELSE '5+ completed' END"] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | SUM(CASE WHEN "Task Status" = 'Completed' THEN 1 ELSE 0 END) | [] | [{"table": "sheet1", "column": "Task Status"}] | False |
| B1 | COUNT(*) | [] | [] | True |
| B2 | COUNT(*) | [] | [] | True |
| B2 | MIN(completed) | [{"table": "sheet1", "column": "Task Status"}] | [] | False |


## S25

类别 `data`；来源 `query_db`；调用 `e5d07e59497d4da693856623fb2bad70`；状态 `success`。

```sql
SELECT "Task Type", COUNT(DISTINCT "Task Owner") AS owner_count
FROM sheet1
GROUP BY "Task Type"
ORDER BY "Task Type"
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-013/attempt-01/sql/S25.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-013/attempt-01/sql/S25.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-013/attempt-01/results/S25.rows.jsonl)；完整：True；SHA256：`f8d29cb14e6115ac2cb7dbe9e39ee224439a31adcc87d21f95d79eaa4034cb40`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "sheet1", "kind": "base", "block": null, "base_tables": ["sheet1"]}] | [] | ["\"Task Type\""] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(DISTINCT "Task Owner") | [{"table": "sheet1", "column": "Task Owner"}] | [] | False |


## S26

类别 `data`；来源 `query_db`；调用 `ea8bdce0c5794c8fa8d8d881246053fb`；状态 `success`。

```sql
SELECT COUNT(*) AS multi_type_owners FROM (
  SELECT "Task Owner" FROM sheet1 GROUP BY "Task Owner" HAVING COUNT(DISTINCT "Task Type") > 1
)
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-013/attempt-01/sql/S26.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-013/attempt-01/sql/S26.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-013/attempt-01/results/S26.rows.jsonl)；完整：True；SHA256：`acc07b62f23f458923737c4cd4a66bd05d1e71eb4f384003baaf2dcc760d6349`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "sheet1", "kind": "base", "block": null, "base_tables": ["sheet1"]}] | [] | ["\"Task Owner\""] |
| B2 | [{"alias": "", "kind": "derived", "block": "B1", "base_tables": ["sheet1"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(DISTINCT "Task Type") | [{"table": "sheet1", "column": "Task Type"}] | [] | False |
| B2 | COUNT(*) | [] | [] | True |


## S27

类别 `data`；来源 `query_db`；调用 `235d37bf9e6c4910a6ea3de272e6cde9`；状态 `success`。

```sql
SELECT
  "Task Type",
  ROUND(AVG("Task Difficulty Coefficient"),3) AS avg_diff,
  ROUND(AVG("Planned Work Hours"),1) AS avg_planned,
  ROUND(AVG(CASE WHEN "Task Status"='Completed' THEN CAST("Actual Work Hours" AS REAL) END),1) AS avg_actual,
  ROUND(AVG(CASE WHEN "Task Status"='Completed' THEN CAST("Completion Quality Score" AS REAL) END),2) AS avg_quality
FROM sheet1
GROUP BY "Task Type"
ORDER BY "Task Type"
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-013/attempt-01/sql/S27.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-013/attempt-01/sql/S27.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-013/attempt-01/results/S27.rows.jsonl)；完整：True；SHA256：`7608e504004c49c3033327cfb4f56feb821e4ccbf7fcb2262baaef1d9487a970`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "sheet1", "kind": "base", "block": null, "base_tables": ["sheet1"]}] | [] | ["\"Task Type\""] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | AVG("Task Difficulty Coefficient") | [{"table": "sheet1", "column": "Task Difficulty Coefficient"}] | [] | False |
| B1 | AVG("Planned Work Hours") | [{"table": "sheet1", "column": "Planned Work Hours"}] | [] | False |
| B1 | AVG(CASE WHEN "Task Status" = 'Completed' THEN CAST("Actual Work Hours" AS REAL) END) | [{"table": "sheet1", "column": "Actual Work Hours"}] | [{"table": "sheet1", "column": "Task Status"}] | False |
| B1 | AVG(CASE WHEN "Task Status" = 'Completed' THEN CAST("Completion Quality Score" AS REAL) END) | [{"table": "sheet1", "column": "Completion Quality Score"}] | [{"table": "sheet1", "column": "Task Status"}] | False |


## S28

类别 `data`；来源 `query_db`；调用 `51de5cd44d9641169219d0090a596809`；状态 `success`。

```sql
SELECT
  "Task Status",
  ROUND(AVG("Task Difficulty Coefficient"),3) AS avg_diff,
  ROUND(AVG("Planned Work Hours"),1) AS avg_planned
FROM sheet1
GROUP BY "Task Status"
ORDER BY "Task Status"
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-013/attempt-01/sql/S28.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-013/attempt-01/sql/S28.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-013/attempt-01/results/S28.rows.jsonl)；完整：True；SHA256：`4f0a98ab274e1d717280626d90200610cb893360173486754a1c9590e2672b25`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "sheet1", "kind": "base", "block": null, "base_tables": ["sheet1"]}] | [] | ["\"Task Status\""] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | AVG("Task Difficulty Coefficient") | [{"table": "sheet1", "column": "Task Difficulty Coefficient"}] | [] | False |
| B1 | AVG("Planned Work Hours") | [{"table": "sheet1", "column": "Planned Work Hours"}] | [] | False |


## S29

类别 `data`；来源 `query_db`；调用 `542d41f2011644568bccc4ff9d707366`；状态 `success`。

```sql
SELECT "Priority", "Task Status", COUNT(*) AS cnt
FROM sheet1 GROUP BY "Priority", "Task Status"
ORDER BY "Priority", "Task Status"
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-013/attempt-01/sql/S29.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-013/attempt-01/sql/S29.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-013/attempt-01/results/S29.rows.jsonl)；完整：True；SHA256：`a3134f6d7111a3ec7527fa24a250a5d1053e6c5e1420752bc6a1333d29ffd904`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "sheet1", "kind": "base", "block": null, "base_tables": ["sheet1"]}] | [] | ["\"Priority\"", "\"Task Status\""] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |


## S30

类别 `data`；来源 `query_db`；调用 `f3e592ffc3544aa3a32acff32445cf23`；状态 `success`。

```sql
WITH t AS (
  SELECT
    "Task Owner",
    "Task Type",
    "Task Status",
    "Priority",
    "Task Difficulty Coefficient",
    CASE WHEN "Task Status" = 'Completed' THEN 1 ELSE 0 END AS completed,
    CASE WHEN "Priority" = 'Urgent' THEN 4 WHEN "Priority" = 'High' THEN 3
         WHEN "Priority" = 'Medium' THEN 2 WHEN "Priority" = 'Low' THEN 1 END AS pw,
    CASE WHEN "Task Status" = 'Completed' AND "Actual Completion Time" != '-'
              AND "Planned Deadline" != '-'
              AND julianday("Actual Completion Time") <= julianday("Planned Deadline")
         THEN 1 ELSE 0 END AS on_time,
    CASE WHEN "Task Status" = 'Completed' AND "Actual Completion Time" != '-'
              AND "Planned Deadline" != '-'
         THEN julianday("Actual Completion Time") - julianday("Planned Deadline") END AS late_days,
    CASE WHEN "Task Status" = 'Completed' AND "Completion Quality Score" != '-'
         THEN CAST("Completion Quality Score" AS REAL) END AS quality,
    CASE WHEN "Task Status" = 'Completed' AND "Actual Work Hours" != '-'
              AND "Planned Work Hours" > 0
         THEN MIN(("Planned Work Hours" * 1.0) / CAST("Actual Work Hours" AS REAL), 1.5) END AS eff,
    CASE WHEN "Task Status" = 'Completed' AND "Rework Count" != '-'
         THEN CAST("Rework Count" AS INTEGER) END AS rework
  FROM sheet1
)
SELECT
  "Task Owner",
  MAX("Task Type") AS task_type,
  COUNT(*) AS total_tasks,
  SUM(completed) AS completed_tasks,
  ROUND(1.0 * SUM(completed) / COUNT(*), 4) AS completion_rate,
  ROUND(1.0 * SUM(on_time) / NULLIF(SUM(completed),0), 4) AS on_time_rate,
  ROUND(AVG(quality), 4) AS avg_quality,
  ROUND(1.0 * SUM(pw * completed) / NULLIF(SUM(pw), 0), 4) AS priority_weighted_completion,
  ROUND(AVG(eff), 4) AS hours_efficiency,
  ROUND(AVG(CASE WHEN rework IS NOT NULL THEN 1 - rework / 3.0 END), 4) AS rework_avoidance,
  ROUND(AVG(late_days), 3) AS avg_late_days,
  ROUND(AVG("Task Difficulty Coefficient"), 3) AS avg_diff
FROM t
GROUP BY "Task Owner"
ORDER BY "Task Owner"
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-013/attempt-01/sql/S30.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-013/attempt-01/sql/S30.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-013/attempt-01/results/S30.rows.jsonl)；完整：True；SHA256：`5dd77b25e5ad7d3761171e9cad8d84cee6e9f423f366c9e43cd9b290825509a2`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "sheet1", "kind": "base", "block": null, "base_tables": ["sheet1"]}] | [] | [] |
| B2 | [{"alias": "t", "kind": "derived", "block": "B1", "base_tables": ["sheet1"]}] | [] | ["\"Task Owner\""] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B2 | MAX("Task Type") | [{"table": "sheet1", "column": "Task Type"}] | [] | False |
| B2 | COUNT(*) | [] | [] | True |
| B2 | SUM(completed) | [{"table": "sheet1", "column": "Task Status"}] | [] | False |
| B2 | AVG(quality) | [{"table": "sheet1", "column": "Completion Quality Score"}, {"table": "sheet1", "column": "Task Status"}, {"table": "sheet1", "column": "Completion Quality Score"}] | [] | False |
| B2 | AVG(eff) | [{"table": "sheet1", "column": "Planned Work Hours"}, {"table": "sheet1", "column": "Task Status"}, {"table": "sheet1", "column": "Actual Work Hours"}, {"table": "sheet1", "column": "Actual Work Hours"}, {"table": "sheet1", "column": "Planned Work Hours"}] | [] | False |
| B2 | AVG(CASE WHEN NOT rework IS NULL THEN 1 - rework / 3.0 END) | [{"table": "sheet1", "column": "Rework Count"}, {"table": "sheet1", "column": "Task Status"}, {"table": "sheet1", "column": "Rework Count"}] | [{"table": "sheet1", "column": "Rework Count"}, {"table": "sheet1", "column": "Task Status"}, {"table": "sheet1", "column": "Rework Count"}] | False |
| B2 | AVG(late_days) | [{"table": "sheet1", "column": "Planned Deadline"}, {"table": "sheet1", "column": "Actual Completion Time"}, {"table": "sheet1", "column": "Planned Deadline"}, {"table": "sheet1", "column": "Task Status"}, {"table": "sheet1", "column": "Actual Completion Time"}] | [] | False |
| B2 | AVG("Task Difficulty Coefficient") | [{"table": "sheet1", "column": "Task Difficulty Coefficient"}] | [] | False |
| B2 | COUNT(*) | [] | [] | True |
| B2 | SUM(completed) | [{"table": "sheet1", "column": "Task Status"}] | [] | False |
| B2 | SUM(on_time) | [{"table": "sheet1", "column": "Planned Deadline"}, {"table": "sheet1", "column": "Actual Completion Time"}, {"table": "sheet1", "column": "Planned Deadline"}, {"table": "sheet1", "column": "Task Status"}, {"table": "sheet1", "column": "Actual Completion Time"}] | [] | False |
| B2 | SUM(completed) | [{"table": "sheet1", "column": "Task Status"}] | [] | False |
| B2 | SUM(pw * completed) | [{"table": "sheet1", "column": "Priority"}, {"table": "sheet1", "column": "Priority"}, {"table": "sheet1", "column": "Priority"}, {"table": "sheet1", "column": "Priority"}, {"table": "sheet1", "column": "Task Status"}] | [] | False |
| B2 | SUM(pw) | [{"table": "sheet1", "column": "Priority"}, {"table": "sheet1", "column": "Priority"}, {"table": "sheet1", "column": "Priority"}, {"table": "sheet1", "column": "Priority"}] | [] | False |


## S31

类别 `data`；来源 `query_db`；调用 `a68db9f686914c56941c1f6fcc51e9ca`；状态 `success`。

```sql
WITH t AS (
  SELECT
    "Task Owner", "Task Type", "Task Status", "Priority",
    CASE WHEN "Task Status" = 'Completed' THEN 1 ELSE 0 END AS completed,
    CASE WHEN "Task Status" = 'Completed' AND "Actual Completion Time" != '-'
              AND "Planned Deadline" != '-'
              AND julianday("Actual Completion Time") <= julianday("Planned Deadline")
         THEN 1 ELSE 0 END AS on_time,
    CASE WHEN "Task Status" = 'Completed' AND "Completion Quality Score" != '-'
         THEN CAST("Completion Quality Score" AS REAL) END AS quality,
    CASE WHEN "Task Status" = 'Completed' AND "Actual Work Hours" != '-'
              AND "Planned Work Hours" > 0
         THEN MIN(("Planned Work Hours" * 1.0) / CAST("Actual Work Hours" AS REAL), 1.5) END AS eff,
    CASE WHEN "Task Status" = 'Completed' AND "Rework Count" != '-'
         THEN CAST("Rework Count" AS INTEGER) END AS rework,
    "Task Difficulty Coefficient"
  FROM sheet1
)
SELECT
  ROUND(AVG(completion_rate),3) AS avg_completion_rate,
  ROUND(AVG(CASE WHEN completed_tasks>0 THEN on_time_rate END),3) AS avg_on_time,
  ROUND(AVG(CASE WHEN completed_tasks>0 THEN avg_quality END),3) AS avg_quality,
  ROUND(AVG(priority_weighted_completion),3) AS avg_prio_completion,
  ROUND(AVG(CASE WHEN completed_tasks>0 THEN hours_efficiency END),3) AS avg_eff,
  ROUND(AVG(CASE WHEN completed_tasks>0 THEN rework_avoidance END),3) AS avg_rework_avoid
FROM (
  SELECT "Task Owner", COUNT(*) AS total_tasks,
    SUM(completed) AS completed_tasks,
    1.0*SUM(completed)/COUNT(*) AS completion_rate,
    1.0*SUM(on_time)/NULLIF(SUM(completed),0) AS on_time_rate,
    AVG(quality) AS avg_quality,
    1.0*SUM(CASE WHEN "Priority"='Urgent' THEN 4 WHEN "Priority"='High' THEN 3
         WHEN "Priority"='Medium' THEN 2 WHEN "Priority"='Low' THEN 1 END * completed)
      /NULLIF(SUM(CASE WHEN "Priority"='Urgent' THEN 4 WHEN "Priority"='High' THEN 3
         WHEN "Priority"='Medium' THEN 2 WHEN "Priority"='Low' THEN 1 END),0) AS priority_weighted_completion,
    AVG(eff) AS hours_efficiency,
    AVG(CASE WHEN rework IS NOT NULL THEN 1 - rework/3.0 END) AS rework_avoidance
  FROM t
  GROUP BY "Task Owner"
)

```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-013/attempt-01/sql/S31.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-013/attempt-01/sql/S31.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-013/attempt-01/results/S31.rows.jsonl)；完整：True；SHA256：`98514f1928acd6a6dda3d167921bf8ed64ddf38038dd88f83bf83e4427427c6b`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "sheet1", "kind": "base", "block": null, "base_tables": ["sheet1"]}] | [] | [] |
| B2 | [{"alias": "t", "kind": "derived", "block": "B1", "base_tables": ["sheet1"]}] | [] | ["\"Task Owner\""] |
| B3 | [{"alias": "", "kind": "derived", "block": "B2", "base_tables": ["sheet1"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B2 | COUNT(*) | [] | [] | True |
| B2 | SUM(completed) | [{"table": "sheet1", "column": "Task Status"}] | [] | False |
| B2 | AVG(quality) | [{"table": "sheet1", "column": "Completion Quality Score"}, {"table": "sheet1", "column": "Task Status"}, {"table": "sheet1", "column": "Completion Quality Score"}] | [] | False |
| B2 | AVG(eff) | [{"table": "sheet1", "column": "Planned Work Hours"}, {"table": "sheet1", "column": "Task Status"}, {"table": "sheet1", "column": "Actual Work Hours"}, {"table": "sheet1", "column": "Actual Work Hours"}, {"table": "sheet1", "column": "Planned Work Hours"}] | [] | False |
| B2 | AVG(CASE WHEN NOT rework IS NULL THEN 1 - rework / 3.0 END) | [{"table": "sheet1", "column": "Rework Count"}, {"table": "sheet1", "column": "Task Status"}, {"table": "sheet1", "column": "Rework Count"}] | [{"table": "sheet1", "column": "Rework Count"}, {"table": "sheet1", "column": "Task Status"}, {"table": "sheet1", "column": "Rework Count"}] | False |
| B2 | COUNT(*) | [] | [] | True |
| B2 | SUM(completed) | [{"table": "sheet1", "column": "Task Status"}] | [] | False |
| B2 | SUM(on_time) | [{"table": "sheet1", "column": "Planned Deadline"}, {"table": "sheet1", "column": "Actual Completion Time"}, {"table": "sheet1", "column": "Planned Deadline"}, {"table": "sheet1", "column": "Task Status"}, {"table": "sheet1", "column": "Actual Completion Time"}] | [] | False |
| B2 | SUM(completed) | [{"table": "sheet1", "column": "Task Status"}] | [] | False |
| B2 | SUM(CASE WHEN "Priority" = 'Urgent' THEN 4 WHEN "Priority" = 'High' THEN 3 WHEN "Priority" = 'Medium' THEN 2 WHEN "Priority" = 'Low' THEN 1 END * completed) | [{"table": "sheet1", "column": "Task Status"}] | [{"table": "sheet1", "column": "Priority"}, {"table": "sheet1", "column": "Priority"}, {"table": "sheet1", "column": "Priority"}, {"table": "sheet1", "column": "Priority"}] | False |
| B2 | SUM(CASE WHEN "Priority" = 'Urgent' THEN 4 WHEN "Priority" = 'High' THEN 3 WHEN "Priority" = 'Medium' THEN 2 WHEN "Priority" = 'Low' THEN 1 END) | [] | [{"table": "sheet1", "column": "Priority"}, {"table": "sheet1", "column": "Priority"}, {"table": "sheet1", "column": "Priority"}, {"table": "sheet1", "column": "Priority"}] | False |
| B3 | AVG(completion_rate) | [{"table": "sheet1", "column": "Task Status"}] | [] | False |
| B3 | AVG(CASE WHEN completed_tasks > 0 THEN on_time_rate END) | [{"table": "sheet1", "column": "Planned Deadline"}, {"table": "sheet1", "column": "Actual Completion Time"}, {"table": "sheet1", "column": "Planned Deadline"}, {"table": "sheet1", "column": "Task Status"}, {"table": "sheet1", "column": "Actual Completion Time"}, {"table": "sheet1", "column": "Task Status"}] | [{"table": "sheet1", "column": "Task Status"}] | False |
| B3 | AVG(CASE WHEN completed_tasks > 0 THEN avg_quality END) | [{"table": "sheet1", "column": "Completion Quality Score"}, {"table": "sheet1", "column": "Task Status"}, {"table": "sheet1", "column": "Completion Quality Score"}] | [{"table": "sheet1", "column": "Task Status"}] | False |
| B3 | AVG(priority_weighted_completion) | [{"table": "sheet1", "column": "Task Status"}, {"table": "sheet1", "column": "Priority"}, {"table": "sheet1", "column": "Priority"}, {"table": "sheet1", "column": "Priority"}, {"table": "sheet1", "column": "Priority"}, {"table": "sheet1", "column": "Priority"}, {"table": "sheet1", "column": "Priority"}, {"table": "sheet1", "column": "Priority"}, {"table": "sheet1", "column": "Priority"}] | [] | False |
| B3 | AVG(CASE WHEN completed_tasks > 0 THEN hours_efficiency END) | [{"table": "sheet1", "column": "Planned Work Hours"}, {"table": "sheet1", "column": "Task Status"}, {"table": "sheet1", "column": "Actual Work Hours"}, {"table": "sheet1", "column": "Actual Work Hours"}, {"table": "sheet1", "column": "Planned Work Hours"}] | [{"table": "sheet1", "column": "Task Status"}] | False |
| B3 | AVG(CASE WHEN completed_tasks > 0 THEN rework_avoidance END) | [{"table": "sheet1", "column": "Rework Count"}, {"table": "sheet1", "column": "Task Status"}, {"table": "sheet1", "column": "Rework Count"}, {"table": "sheet1", "column": "Rework Count"}, {"table": "sheet1", "column": "Task Status"}, {"table": "sheet1", "column": "Rework Count"}] | [{"table": "sheet1", "column": "Task Status"}] | False |


## S32

类别 `data`；来源 `query_db`；调用 `3b9543e18efd4d79a03467b09c6c973b`；状态 `success`。

```sql
SELECT
  "Task Type",
  ROUND(AVG(1.0*completed/total),3) AS avg_completion_rate,
  ROUND(AVG(CASE WHEN completed>0 THEN on_time/completed END),3) AS avg_on_time_rate,
  ROUND(AVG(CASE WHEN completed>0 THEN quality_sum/completed END),3) AS avg_quality
FROM (
  SELECT "Task Owner", "Task Type", COUNT(*) AS total,
    SUM(CASE WHEN "Task Status"='Completed' THEN 1 ELSE 0 END) AS completed,
    SUM(CASE WHEN "Task Status"='Completed' AND "Actual Completion Time" != '-' AND "Planned Deadline" != '-'
              AND julianday("Actual Completion Time") <= julianday("Planned Deadline") THEN 1 ELSE 0 END) AS on_time,
    SUM(CASE WHEN "Task Status"='Completed' AND "Completion Quality Score" != '-'
         THEN CAST("Completion Quality Score" AS REAL) ELSE 0 END) AS quality_sum
  FROM sheet1
  GROUP BY "Task Owner", "Task Type"
)
GROUP BY "Task Type"
ORDER BY "Task Type"
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-013/attempt-01/sql/S32.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-013/attempt-01/sql/S32.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-013/attempt-01/results/S32.rows.jsonl)；完整：True；SHA256：`243019a8f10906321dfec2f2585f80d2a8fd0fdd20b6f847be7c76170f8af46f`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "sheet1", "kind": "base", "block": null, "base_tables": ["sheet1"]}] | [] | ["\"Task Owner\"", "\"Task Type\""] |
| B2 | [{"alias": "", "kind": "derived", "block": "B1", "base_tables": ["sheet1"]}] | [] | ["\"Task Type\""] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |
| B1 | SUM(CASE WHEN "Task Status" = 'Completed' THEN 1 ELSE 0 END) | [] | [{"table": "sheet1", "column": "Task Status"}] | False |
| B1 | SUM(CASE WHEN "Task Status" = 'Completed' AND "Actual Completion Time" <> '-' AND "Planned Deadline" <> '-' AND JULIANDAY("Actual Completion Time") <= JULIANDAY("Planned Deadline") THEN 1 ELSE 0 END) | [] | [{"table": "sheet1", "column": "Planned Deadline"}, {"table": "sheet1", "column": "Actual Completion Time"}, {"table": "sheet1", "column": "Planned Deadline"}, {"table": "sheet1", "column": "Task Status"}, {"table": "sheet1", "column": "Actual Completion Time"}] | False |
| B1 | SUM(CASE WHEN "Task Status" = 'Completed' AND "Completion Quality Score" <> '-' THEN CAST("Completion Quality Score" AS REAL) ELSE 0 END) | [{"table": "sheet1", "column": "Completion Quality Score"}] | [{"table": "sheet1", "column": "Task Status"}, {"table": "sheet1", "column": "Completion Quality Score"}] | False |
| B2 | AVG(1.0 * completed / total) | [{"table": "sheet1", "column": "Task Status"}] | [] | False |
| B2 | AVG(CASE WHEN completed > 0 THEN on_time / completed END) | [{"table": "sheet1", "column": "Planned Deadline"}, {"table": "sheet1", "column": "Actual Completion Time"}, {"table": "sheet1", "column": "Planned Deadline"}, {"table": "sheet1", "column": "Task Status"}, {"table": "sheet1", "column": "Actual Completion Time"}, {"table": "sheet1", "column": "Task Status"}] | [{"table": "sheet1", "column": "Task Status"}] | False |
| B2 | AVG(CASE WHEN completed > 0 THEN quality_sum / completed END) | [{"table": "sheet1", "column": "Completion Quality Score"}, {"table": "sheet1", "column": "Task Status"}, {"table": "sheet1", "column": "Completion Quality Score"}, {"table": "sheet1", "column": "Task Status"}] | [{"table": "sheet1", "column": "Task Status"}] | False |


## S33

类别 `data`；来源 `python`；调用 `a1b4fcbe4a5f4e54991bf25c183f17e2`；状态 `success`。

```sql

WITH t AS (
  SELECT
    "Task Owner", "Task Type", "Task Status", "Priority",
    CASE WHEN "Task Status" = 'Completed' THEN 1 ELSE 0 END AS completed,
    CASE WHEN "Task Status" = 'Completed' AND "Actual Completion Time" != '-'
              AND "Planned Deadline" != '-'
              AND julianday("Actual Completion Time") <= julianday("Planned Deadline")
         THEN 1 ELSE 0 END AS on_time,
    CASE WHEN "Task Status" = 'Completed' AND "Completion Quality Score" != '-'
         THEN CAST("Completion Quality Score" AS REAL) END AS quality,
    CASE WHEN "Task Status" = 'Completed' AND "Actual Work Hours" != '-'
              AND "Planned Work Hours" > 0
         THEN MIN(("Planned Work Hours" * 1.0) / CAST("Actual Work Hours" AS REAL), 1.5) END AS eff,
    CASE WHEN "Task Status" = 'Completed' AND "Rework Count" != '-'
         THEN CAST("Rework Count" AS INTEGER) END AS rework,
    "Task Difficulty Coefficient"
  FROM sheet1
)
SELECT
  "Task Owner",
  MAX("Task Type") AS task_type,
  COUNT(*) AS total_tasks,
  SUM(completed) AS completed_tasks,
  1.0*SUM(completed)/COUNT(*) AS completion_rate,
  1.0*SUM(on_time)/NULLIF(SUM(completed),0) AS on_time_rate,
  AVG(quality)/10.0 AS quality_norm,
  1.0*SUM(CASE WHEN "Priority"='Urgent' THEN 4 WHEN "Priority"='High' THEN 3
         WHEN "Priority"='Medium' THEN 2 WHEN "Priority"='Low' THEN 1 END * completed)
    /NULLIF(SUM(CASE WHEN "Priority"='Urgent' THEN 4 WHEN "Priority"='High' THEN 3
         WHEN "Priority"='Medium' THEN 2 WHEN "Priority"='Low' THEN 1 END),0) AS priority_weighted_completion,
  AVG(eff) AS hours_efficiency,
  AVG(CASE WHEN rework IS NOT NULL THEN 1 - rework/3.0 END) AS rework_avoidance,
  SUM(CASE WHEN "Priority" IN ('Urgent','High') THEN 1 ELSE 0 END) AS hp_total,
  SUM(CASE WHEN "Priority" IN ('Urgent','High') AND completed=1 THEN 1 ELSE 0 END) AS hp_completed,
  SUM(CASE WHEN "Priority" IN ('Urgent','High') AND on_time=1 THEN 1 ELSE 0 END) AS hp_on_time,
  ROUND(AVG("Task Difficulty Coefficient"),3) AS avg_diff
FROM t
GROUP BY "Task Owner"

```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-013/attempt-01/sql/S33.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-013/attempt-01/sql/S33.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-013/attempt-01/results/S33.rows.jsonl)；完整：True；SHA256：`ac0dbaf513f86f31e80ae94c8f42304ebe3b8797eb51baf1fb9940f5cb326f61`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "sheet1", "kind": "base", "block": null, "base_tables": ["sheet1"]}] | [] | [] |
| B2 | [{"alias": "t", "kind": "derived", "block": "B1", "base_tables": ["sheet1"]}] | [] | ["\"Task Owner\""] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B2 | MAX("Task Type") | [{"table": "sheet1", "column": "Task Type"}] | [] | False |
| B2 | COUNT(*) | [] | [] | True |
| B2 | SUM(completed) | [{"table": "sheet1", "column": "Task Status"}] | [] | False |
| B2 | AVG(eff) | [{"table": "sheet1", "column": "Planned Work Hours"}, {"table": "sheet1", "column": "Task Status"}, {"table": "sheet1", "column": "Actual Work Hours"}, {"table": "sheet1", "column": "Actual Work Hours"}, {"table": "sheet1", "column": "Planned Work Hours"}] | [] | False |
| B2 | AVG(CASE WHEN NOT rework IS NULL THEN 1 - rework / 3.0 END) | [{"table": "sheet1", "column": "Rework Count"}, {"table": "sheet1", "column": "Task Status"}, {"table": "sheet1", "column": "Rework Count"}] | [{"table": "sheet1", "column": "Rework Count"}, {"table": "sheet1", "column": "Task Status"}, {"table": "sheet1", "column": "Rework Count"}] | False |
| B2 | SUM(CASE WHEN "Priority" IN ('Urgent', 'High') THEN 1 ELSE 0 END) | [] | [{"table": "sheet1", "column": "Priority"}] | False |
| B2 | SUM(CASE WHEN "Priority" IN ('Urgent', 'High') AND completed = 1 THEN 1 ELSE 0 END) | [] | [{"table": "sheet1", "column": "Priority"}, {"table": "sheet1", "column": "Task Status"}] | False |
| B2 | SUM(CASE WHEN "Priority" IN ('Urgent', 'High') AND on_time = 1 THEN 1 ELSE 0 END) | [] | [{"table": "sheet1", "column": "Priority"}, {"table": "sheet1", "column": "Planned Deadline"}, {"table": "sheet1", "column": "Actual Completion Time"}, {"table": "sheet1", "column": "Planned Deadline"}, {"table": "sheet1", "column": "Task Status"}, {"table": "sheet1", "column": "Actual Completion Time"}] | False |
| B2 | COUNT(*) | [] | [] | True |
| B2 | AVG(quality) | [{"table": "sheet1", "column": "Completion Quality Score"}, {"table": "sheet1", "column": "Task Status"}, {"table": "sheet1", "column": "Completion Quality Score"}] | [] | False |
| B2 | AVG("Task Difficulty Coefficient") | [{"table": "sheet1", "column": "Task Difficulty Coefficient"}] | [] | False |
| B2 | SUM(completed) | [{"table": "sheet1", "column": "Task Status"}] | [] | False |
| B2 | SUM(on_time) | [{"table": "sheet1", "column": "Planned Deadline"}, {"table": "sheet1", "column": "Actual Completion Time"}, {"table": "sheet1", "column": "Planned Deadline"}, {"table": "sheet1", "column": "Task Status"}, {"table": "sheet1", "column": "Actual Completion Time"}] | [] | False |
| B2 | SUM(completed) | [{"table": "sheet1", "column": "Task Status"}] | [] | False |
| B2 | SUM(CASE WHEN "Priority" = 'Urgent' THEN 4 WHEN "Priority" = 'High' THEN 3 WHEN "Priority" = 'Medium' THEN 2 WHEN "Priority" = 'Low' THEN 1 END * completed) | [{"table": "sheet1", "column": "Task Status"}] | [{"table": "sheet1", "column": "Priority"}, {"table": "sheet1", "column": "Priority"}, {"table": "sheet1", "column": "Priority"}, {"table": "sheet1", "column": "Priority"}] | False |
| B2 | SUM(CASE WHEN "Priority" = 'Urgent' THEN 4 WHEN "Priority" = 'High' THEN 3 WHEN "Priority" = 'Medium' THEN 2 WHEN "Priority" = 'Low' THEN 1 END) | [] | [{"table": "sheet1", "column": "Priority"}, {"table": "sheet1", "column": "Priority"}, {"table": "sheet1", "column": "Priority"}, {"table": "sheet1", "column": "Priority"}] | False |


## S34

类别 `data`；来源 `python`；调用 `8c71e40f46444fe9bbf35eee84c40f36`；状态 `success`。

```sql

WITH t AS (
  SELECT
    "Task Owner", "Task Type", "Task Status", "Priority",
    CASE WHEN "Task Status" = 'Completed' THEN 1 ELSE 0 END AS completed,
    CASE WHEN "Task Status" = 'Completed' AND "Actual Completion Time" != '-'
              AND "Planned Deadline" != '-'
              AND julianday("Actual Completion Time") <= julianday("Planned Deadline")
         THEN 1 ELSE 0 END AS on_time,
    CASE WHEN "Task Status" = 'Completed' AND "Completion Quality Score" != '-'
         THEN CAST("Completion Quality Score" AS REAL) END AS quality,
    CASE WHEN "Task Status" = 'Completed' AND "Actual Work Hours" != '-'
              AND "Planned Work Hours" > 0
         THEN MIN(("Planned Work Hours" * 1.0) / CAST("Actual Work Hours" AS REAL), 1.5) END AS eff,
    CASE WHEN "Task Status" = 'Completed' AND "Rework Count" != '-'
         THEN CAST("Rework Count" AS INTEGER) END AS rework,
    "Task Difficulty Coefficient"
  FROM sheet1
)
SELECT
  "Task Owner",
  MAX("Task Type") AS task_type,
  COUNT(*) AS total_tasks,
  SUM(completed) AS completed_tasks,
  1.0*SUM(completed)/COUNT(*) AS completion_rate,
  1.0*SUM(on_time)/NULLIF(SUM(completed),0) AS on_time_rate,
  AVG(quality)/10.0 AS quality_norm,
  1.0*SUM(CASE WHEN "Priority"='Urgent' THEN 4 WHEN "Priority"='High' THEN 3
         WHEN "Priority"='Medium' THEN 2 WHEN "Priority"='Low' THEN 1 END * completed)
    /NULLIF(SUM(CASE WHEN "Priority"='Urgent' THEN 4 WHEN "Priority"='High' THEN 3
         WHEN "Priority"='Medium' THEN 2 WHEN "Priority"='Low' THEN 1 END),0) AS priority_weighted_completion,
  AVG(eff) AS hours_efficiency,
  AVG(CASE WHEN rework IS NOT NULL THEN 1 - rework/3.0 END) AS rework_avoidance,
  SUM(CASE WHEN "Priority" IN ('Urgent','High') THEN 1 ELSE 0 END) AS hp_total,
  SUM(CASE WHEN "Priority" IN ('Urgent','High') AND completed=1 THEN 1 ELSE 0 END) AS hp_completed,
  SUM(CASE WHEN "Priority" IN ('Urgent','High') AND on_time=1 THEN 1 ELSE 0 END) AS hp_on_time,
  ROUND(AVG("Task Difficulty Coefficient"),3) AS avg_diff
FROM t
GROUP BY "Task Owner"

```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-013/attempt-01/sql/S34.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-013/attempt-01/sql/S34.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-013/attempt-01/results/S34.rows.jsonl)；完整：True；SHA256：`ac0dbaf513f86f31e80ae94c8f42304ebe3b8797eb51baf1fb9940f5cb326f61`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "sheet1", "kind": "base", "block": null, "base_tables": ["sheet1"]}] | [] | [] |
| B2 | [{"alias": "t", "kind": "derived", "block": "B1", "base_tables": ["sheet1"]}] | [] | ["\"Task Owner\""] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B2 | MAX("Task Type") | [{"table": "sheet1", "column": "Task Type"}] | [] | False |
| B2 | COUNT(*) | [] | [] | True |
| B2 | SUM(completed) | [{"table": "sheet1", "column": "Task Status"}] | [] | False |
| B2 | AVG(eff) | [{"table": "sheet1", "column": "Planned Work Hours"}, {"table": "sheet1", "column": "Task Status"}, {"table": "sheet1", "column": "Actual Work Hours"}, {"table": "sheet1", "column": "Actual Work Hours"}, {"table": "sheet1", "column": "Planned Work Hours"}] | [] | False |
| B2 | AVG(CASE WHEN NOT rework IS NULL THEN 1 - rework / 3.0 END) | [{"table": "sheet1", "column": "Rework Count"}, {"table": "sheet1", "column": "Task Status"}, {"table": "sheet1", "column": "Rework Count"}] | [{"table": "sheet1", "column": "Rework Count"}, {"table": "sheet1", "column": "Task Status"}, {"table": "sheet1", "column": "Rework Count"}] | False |
| B2 | SUM(CASE WHEN "Priority" IN ('Urgent', 'High') THEN 1 ELSE 0 END) | [] | [{"table": "sheet1", "column": "Priority"}] | False |
| B2 | SUM(CASE WHEN "Priority" IN ('Urgent', 'High') AND completed = 1 THEN 1 ELSE 0 END) | [] | [{"table": "sheet1", "column": "Priority"}, {"table": "sheet1", "column": "Task Status"}] | False |
| B2 | SUM(CASE WHEN "Priority" IN ('Urgent', 'High') AND on_time = 1 THEN 1 ELSE 0 END) | [] | [{"table": "sheet1", "column": "Priority"}, {"table": "sheet1", "column": "Planned Deadline"}, {"table": "sheet1", "column": "Actual Completion Time"}, {"table": "sheet1", "column": "Planned Deadline"}, {"table": "sheet1", "column": "Task Status"}, {"table": "sheet1", "column": "Actual Completion Time"}] | False |
| B2 | COUNT(*) | [] | [] | True |
| B2 | AVG(quality) | [{"table": "sheet1", "column": "Completion Quality Score"}, {"table": "sheet1", "column": "Task Status"}, {"table": "sheet1", "column": "Completion Quality Score"}] | [] | False |
| B2 | AVG("Task Difficulty Coefficient") | [{"table": "sheet1", "column": "Task Difficulty Coefficient"}] | [] | False |
| B2 | SUM(completed) | [{"table": "sheet1", "column": "Task Status"}] | [] | False |
| B2 | SUM(on_time) | [{"table": "sheet1", "column": "Planned Deadline"}, {"table": "sheet1", "column": "Actual Completion Time"}, {"table": "sheet1", "column": "Planned Deadline"}, {"table": "sheet1", "column": "Task Status"}, {"table": "sheet1", "column": "Actual Completion Time"}] | [] | False |
| B2 | SUM(completed) | [{"table": "sheet1", "column": "Task Status"}] | [] | False |
| B2 | SUM(CASE WHEN "Priority" = 'Urgent' THEN 4 WHEN "Priority" = 'High' THEN 3 WHEN "Priority" = 'Medium' THEN 2 WHEN "Priority" = 'Low' THEN 1 END * completed) | [{"table": "sheet1", "column": "Task Status"}] | [{"table": "sheet1", "column": "Priority"}, {"table": "sheet1", "column": "Priority"}, {"table": "sheet1", "column": "Priority"}, {"table": "sheet1", "column": "Priority"}] | False |
| B2 | SUM(CASE WHEN "Priority" = 'Urgent' THEN 4 WHEN "Priority" = 'High' THEN 3 WHEN "Priority" = 'Medium' THEN 2 WHEN "Priority" = 'Low' THEN 1 END) | [] | [{"table": "sheet1", "column": "Priority"}, {"table": "sheet1", "column": "Priority"}, {"table": "sheet1", "column": "Priority"}, {"table": "sheet1", "column": "Priority"}] | False |


## S35

类别 `data`；来源 `python`；调用 `e15f30ee476c43439e593ccedf2e0e8c`；状态 `success`。

```sql

WITH t AS (
  SELECT
    "Task Owner", "Task Type", "Task Status", "Priority",
    CASE WHEN "Task Status" = 'Completed' THEN 1 ELSE 0 END AS completed,
    CASE WHEN "Task Status" = 'Completed' AND "Actual Completion Time" != '-'
              AND "Planned Deadline" != '-'
              AND julianday("Actual Completion Time") <= julianday("Planned Deadline")
         THEN 1 ELSE 0 END AS on_time,
    CASE WHEN "Task Status" = 'Completed' AND "Completion Quality Score" != '-'
         THEN CAST("Completion Quality Score" AS REAL) END AS quality,
    CASE WHEN "Task Status" = 'Completed' AND "Actual Work Hours" != '-'
              AND "Planned Work Hours" > 0
         THEN MIN(("Planned Work Hours" * 1.0) / CAST("Actual Work Hours" AS REAL), 1.5) END AS eff,
    CASE WHEN "Task Status" = 'Completed' AND "Rework Count" != '-'
         THEN CAST("Rework Count" AS INTEGER) END AS rework,
    CASE WHEN "Task Status" = 'Completed' THEN 1 ELSE 0 END AS is_comp
  FROM sheet1
)
SELECT
  "Task Owner", MAX("Task Type") AS task_type,
  COUNT(*) AS total_tasks,
  SUM(completed) AS completed_tasks,
  SUM(CASE WHEN "Task Status" = 'Completed' AND "Actual Completion Time" != '-'
              AND "Planned Deadline" != '-' THEN 1 ELSE 0 END) AS timed_completed,
  SUM(CASE WHEN "Task Status" = 'Completed' AND "Completion Quality Score" != '-' THEN 1 ELSE 0 END) AS scored_completed,
  SUM(CASE WHEN "Task Status" = 'Completed' AND "Actual Work Hours" != '-' AND "Planned Work Hours" > 0 THEN 1 ELSE 0 END) AS eff_completed,
  SUM(CASE WHEN "Task Status" = 'Completed' AND "Rework Count" != '-' THEN 1 ELSE 0 END) AS rework_completed,
  1.0*SUM(completed)/COUNT(*) AS completion_rate,
  1.0*SUM(on_time)/NULLIF(SUM(completed),0) AS on_time_rate,
  AVG(quality)/10.0 AS quality_norm,
  1.0*SUM(CASE WHEN "Priority"='Urgent' THEN 4 WHEN "Priority"='High' THEN 3
         WHEN "Priority"='Medium' THEN 2 WHEN "Priority"='Low' THEN 1 END * completed)
    /NULLIF(SUM(CASE WHEN "Priority"='Urgent' THEN 4 WHEN "Priority"='High' THEN 3
         WHEN "Priority"='Medium' THEN 2 WHEN "Priority"='Low' THEN 1 END),0) AS priority_weighted_completion,
  AVG(eff) AS hours_efficiency,
  AVG(CASE WHEN rework IS NOT NULL THEN 1 - rework/3.0 END) AS rework_avoidance
FROM t
GROUP BY "Task Owner"

```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-013/attempt-01/sql/S35.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-013/attempt-01/sql/S35.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-013/attempt-01/results/S35.rows.jsonl)；完整：True；SHA256：`0e286e4a9d4ac3f414908e256f27a3529478e492cfbd4f5dee2b1f7ee97b0b6c`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "sheet1", "kind": "base", "block": null, "base_tables": ["sheet1"]}] | [] | [] |
| B2 | [{"alias": "t", "kind": "derived", "block": "B1", "base_tables": ["sheet1"]}] | [] | ["\"Task Owner\""] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B2 | MAX("Task Type") | [{"table": "sheet1", "column": "Task Type"}] | [] | False |
| B2 | COUNT(*) | [] | [] | True |
| B2 | SUM(completed) | [{"table": "sheet1", "column": "Task Status"}] | [] | False |
| B2 | SUM(CASE WHEN "Task Status" = 'Completed' AND "Actual Completion Time" <> '-' AND "Planned Deadline" <> '-' THEN 1 ELSE 0 END) | [] | [{"unknown": "\"Planned Deadline\""}, {"table": "sheet1", "column": "Task Status"}, {"unknown": "\"Actual Completion Time\""}] | False |
| B2 | SUM(CASE WHEN "Task Status" = 'Completed' AND "Completion Quality Score" <> '-' THEN 1 ELSE 0 END) | [] | [{"table": "sheet1", "column": "Task Status"}, {"unknown": "\"Completion Quality Score\""}] | False |
| B2 | SUM(CASE WHEN "Task Status" = 'Completed' AND "Actual Work Hours" <> '-' AND "Planned Work Hours" > 0 THEN 1 ELSE 0 END) | [] | [{"unknown": "\"Planned Work Hours\""}, {"table": "sheet1", "column": "Task Status"}, {"unknown": "\"Actual Work Hours\""}] | False |
| B2 | SUM(CASE WHEN "Task Status" = 'Completed' AND "Rework Count" <> '-' THEN 1 ELSE 0 END) | [] | [{"table": "sheet1", "column": "Task Status"}, {"unknown": "\"Rework Count\""}] | False |
| B2 | AVG(eff) | [{"table": "sheet1", "column": "Planned Work Hours"}, {"table": "sheet1", "column": "Task Status"}, {"table": "sheet1", "column": "Actual Work Hours"}, {"table": "sheet1", "column": "Actual Work Hours"}, {"table": "sheet1", "column": "Planned Work Hours"}] | [] | False |
| B2 | AVG(CASE WHEN NOT rework IS NULL THEN 1 - rework / 3.0 END) | [{"table": "sheet1", "column": "Rework Count"}, {"table": "sheet1", "column": "Task Status"}, {"table": "sheet1", "column": "Rework Count"}] | [{"table": "sheet1", "column": "Rework Count"}, {"table": "sheet1", "column": "Task Status"}, {"table": "sheet1", "column": "Rework Count"}] | False |
| B2 | COUNT(*) | [] | [] | True |
| B2 | AVG(quality) | [{"table": "sheet1", "column": "Completion Quality Score"}, {"table": "sheet1", "column": "Task Status"}, {"table": "sheet1", "column": "Completion Quality Score"}] | [] | False |
| B2 | SUM(completed) | [{"table": "sheet1", "column": "Task Status"}] | [] | False |
| B2 | SUM(on_time) | [{"table": "sheet1", "column": "Planned Deadline"}, {"table": "sheet1", "column": "Actual Completion Time"}, {"table": "sheet1", "column": "Planned Deadline"}, {"table": "sheet1", "column": "Task Status"}, {"table": "sheet1", "column": "Actual Completion Time"}] | [] | False |
| B2 | SUM(completed) | [{"table": "sheet1", "column": "Task Status"}] | [] | False |
| B2 | SUM(CASE WHEN "Priority" = 'Urgent' THEN 4 WHEN "Priority" = 'High' THEN 3 WHEN "Priority" = 'Medium' THEN 2 WHEN "Priority" = 'Low' THEN 1 END * completed) | [{"table": "sheet1", "column": "Task Status"}] | [{"table": "sheet1", "column": "Priority"}, {"table": "sheet1", "column": "Priority"}, {"table": "sheet1", "column": "Priority"}, {"table": "sheet1", "column": "Priority"}] | False |
| B2 | SUM(CASE WHEN "Priority" = 'Urgent' THEN 4 WHEN "Priority" = 'High' THEN 3 WHEN "Priority" = 'Medium' THEN 2 WHEN "Priority" = 'Low' THEN 1 END) | [] | [{"table": "sheet1", "column": "Priority"}, {"table": "sheet1", "column": "Priority"}, {"table": "sheet1", "column": "Priority"}, {"table": "sheet1", "column": "Priority"}] | False |


未解析列血缘：[{"block": "B2", "column": "\"Planned Deadline\"", "reason": "ambiguous_or_missing_source"}, {"block": "B2", "column": "\"Actual Completion Time\"", "reason": "ambiguous_or_missing_source"}, {"block": "B2", "column": "\"Completion Quality Score\"", "reason": "ambiguous_or_missing_source"}, {"block": "B2", "column": "\"Planned Work Hours\"", "reason": "ambiguous_or_missing_source"}, {"block": "B2", "column": "\"Actual Work Hours\"", "reason": "ambiguous_or_missing_source"}, {"block": "B2", "column": "\"Rework Count\"", "reason": "ambiguous_or_missing_source"}, {"block": "B2", "column": "\"Planned Deadline\"", "reason": "ambiguous_or_missing_source"}, {"block": "B2", "column": "\"Actual Completion Time\"", "reason": "ambiguous_or_missing_source"}, {"block": "B2", "column": "\"Completion Quality Score\"", "reason": "ambiguous_or_missing_source"}, {"block": "B2", "column": "\"Planned Work Hours\"", "reason": "ambiguous_or_missing_source"}, {"block": "B2", "column": "\"Actual Work Hours\"", "reason": "ambiguous_or_missing_source"}, {"block": "B2", "column": "\"Rework Count\"", "reason": "ambiguous_or_missing_source"}, {"block": "B2", "column": "\"Actual Completion Time\"", "reason": "ambiguous_or_missing_source"}, {"block": "B2", "column": "\"Planned Deadline\"", "reason": "ambiguous_or_missing_source"}, {"block": "B2", "column": "\"Completion Quality Score\"", "reason": "ambiguous_or_missing_source"}, {"block": "B2", "column": "\"Actual Work Hours\"", "reason": "ambiguous_or_missing_source"}, {"block": "B2", "column": "\"Planned Work Hours\"", "reason": "ambiguous_or_missing_source"}, {"block": "B2", "column": "\"Rework Count\"", "reason": "ambiguous_or_missing_source"}]

## S36

类别 `data`；来源 `python`；调用 `cb5a1ae1a7974f8894813aca776c83a9`；状态 `success`。

```sql

WITH t AS (
  SELECT
    "Task Owner", "Task Type", "Task Status", "Priority",
    CASE WHEN "Task Status" = 'Completed' THEN 1 ELSE 0 END AS completed,
    CASE WHEN "Task Status" = 'Completed' AND "Actual Completion Time" != '-'
              AND "Planned Deadline" != '-'
              AND julianday("Actual Completion Time") <= julianday("Planned Deadline")
         THEN 1 ELSE 0 END AS on_time,
    CASE WHEN "Task Status" = 'Completed' AND "Completion Quality Score" != '-'
         THEN CAST("Completion Quality Score" AS REAL) END AS quality,
    CASE WHEN "Task Status" = 'Completed' AND "Actual Work Hours" != '-'
              AND "Planned Work Hours" > 0
         THEN MIN(("Planned Work Hours" * 1.0) / CAST("Actual Work Hours" AS REAL), 1.5) END AS eff,
    CASE WHEN "Task Status" = 'Completed' AND "Rework Count" != '-'
         THEN CAST("Rework Count" AS INTEGER) END AS rework
  FROM sheet1
)
SELECT
  "Task Owner", MAX("Task Type") AS task_type,
  COUNT(*) AS total_tasks,
  SUM(completed) AS completed_tasks,
  SUM(CASE WHEN "Task Status" = 'Completed' AND "Actual Completion Time" != '-'
              AND "Planned Deadline" != '-' THEN 1 ELSE 0 END) AS timed_completed,
  SUM(CASE WHEN "Task Status" = 'Completed' AND "Completion Quality Score" != '-' THEN 1 ELSE 0 END) AS scored_completed,
  SUM(CASE WHEN "Task Status" = 'Completed' AND "Actual Work Hours" != '-' AND "Planned Work Hours" > 0 THEN 1 ELSE 0 END) AS eff_completed,
  SUM(CASE WHEN "Task Status" = 'Completed' AND "Rework Count" != '-' THEN 1 ELSE 0 END) AS rework_completed,
  1.0*SUM(completed)/COUNT(*) AS completion_rate,
  1.0*SUM(on_time)/NULLIF(SUM(completed),0) AS on_time_rate,
  AVG(quality)/10.0 AS quality_norm,
  1.0*SUM(CASE WHEN "Priority"='Urgent' THEN 4 WHEN "Priority"='High' THEN 3
         WHEN "Priority"='Medium' THEN 2 WHEN "Priority"='Low' THEN 1 END * completed)
    /NULLIF(SUM(CASE WHEN "Priority"='Urgent' THEN 4 WHEN "Priority"='High' THEN 3
         WHEN "Priority"='Medium' THEN 2 WHEN "Priority"='Low' THEN 1 END),0) AS priority_weighted_completion,
  AVG(eff) AS hours_efficiency,
  AVG(CASE WHEN rework IS NOT NULL THEN 1 - rework/3.0 END) AS rework_avoidance,
  SUM(CASE WHEN "Priority" IN ('Urgent','High') THEN 1 ELSE 0 END) AS hp_total,
  SUM(CASE WHEN "Priority" IN ('Urgent','High') AND completed=1 THEN 1 ELSE 0 END) AS hp_completed
FROM t
GROUP BY "Task Owner"

```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-013/attempt-01/sql/S36.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-013/attempt-01/sql/S36.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-013/attempt-01/results/S36.rows.jsonl)；完整：True；SHA256：`509c61844fd2e3ede728f09e458fdb3f11bf5edbfc9658149449247f62616d87`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "sheet1", "kind": "base", "block": null, "base_tables": ["sheet1"]}] | [] | [] |
| B2 | [{"alias": "t", "kind": "derived", "block": "B1", "base_tables": ["sheet1"]}] | [] | ["\"Task Owner\""] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B2 | MAX("Task Type") | [{"table": "sheet1", "column": "Task Type"}] | [] | False |
| B2 | COUNT(*) | [] | [] | True |
| B2 | SUM(completed) | [{"table": "sheet1", "column": "Task Status"}] | [] | False |
| B2 | SUM(CASE WHEN "Task Status" = 'Completed' AND "Actual Completion Time" <> '-' AND "Planned Deadline" <> '-' THEN 1 ELSE 0 END) | [] | [{"unknown": "\"Planned Deadline\""}, {"table": "sheet1", "column": "Task Status"}, {"unknown": "\"Actual Completion Time\""}] | False |
| B2 | SUM(CASE WHEN "Task Status" = 'Completed' AND "Completion Quality Score" <> '-' THEN 1 ELSE 0 END) | [] | [{"table": "sheet1", "column": "Task Status"}, {"unknown": "\"Completion Quality Score\""}] | False |
| B2 | SUM(CASE WHEN "Task Status" = 'Completed' AND "Actual Work Hours" <> '-' AND "Planned Work Hours" > 0 THEN 1 ELSE 0 END) | [] | [{"unknown": "\"Planned Work Hours\""}, {"table": "sheet1", "column": "Task Status"}, {"unknown": "\"Actual Work Hours\""}] | False |
| B2 | SUM(CASE WHEN "Task Status" = 'Completed' AND "Rework Count" <> '-' THEN 1 ELSE 0 END) | [] | [{"table": "sheet1", "column": "Task Status"}, {"unknown": "\"Rework Count\""}] | False |
| B2 | AVG(eff) | [{"table": "sheet1", "column": "Planned Work Hours"}, {"table": "sheet1", "column": "Task Status"}, {"table": "sheet1", "column": "Actual Work Hours"}, {"table": "sheet1", "column": "Actual Work Hours"}, {"table": "sheet1", "column": "Planned Work Hours"}] | [] | False |
| B2 | AVG(CASE WHEN NOT rework IS NULL THEN 1 - rework / 3.0 END) | [{"table": "sheet1", "column": "Rework Count"}, {"table": "sheet1", "column": "Task Status"}, {"table": "sheet1", "column": "Rework Count"}] | [{"table": "sheet1", "column": "Rework Count"}, {"table": "sheet1", "column": "Task Status"}, {"table": "sheet1", "column": "Rework Count"}] | False |
| B2 | SUM(CASE WHEN "Priority" IN ('Urgent', 'High') THEN 1 ELSE 0 END) | [] | [{"table": "sheet1", "column": "Priority"}] | False |
| B2 | SUM(CASE WHEN "Priority" IN ('Urgent', 'High') AND completed = 1 THEN 1 ELSE 0 END) | [] | [{"table": "sheet1", "column": "Priority"}, {"table": "sheet1", "column": "Task Status"}] | False |
| B2 | COUNT(*) | [] | [] | True |
| B2 | AVG(quality) | [{"table": "sheet1", "column": "Completion Quality Score"}, {"table": "sheet1", "column": "Task Status"}, {"table": "sheet1", "column": "Completion Quality Score"}] | [] | False |
| B2 | SUM(completed) | [{"table": "sheet1", "column": "Task Status"}] | [] | False |
| B2 | SUM(on_time) | [{"table": "sheet1", "column": "Planned Deadline"}, {"table": "sheet1", "column": "Actual Completion Time"}, {"table": "sheet1", "column": "Planned Deadline"}, {"table": "sheet1", "column": "Task Status"}, {"table": "sheet1", "column": "Actual Completion Time"}] | [] | False |
| B2 | SUM(completed) | [{"table": "sheet1", "column": "Task Status"}] | [] | False |
| B2 | SUM(CASE WHEN "Priority" = 'Urgent' THEN 4 WHEN "Priority" = 'High' THEN 3 WHEN "Priority" = 'Medium' THEN 2 WHEN "Priority" = 'Low' THEN 1 END * completed) | [{"table": "sheet1", "column": "Task Status"}] | [{"table": "sheet1", "column": "Priority"}, {"table": "sheet1", "column": "Priority"}, {"table": "sheet1", "column": "Priority"}, {"table": "sheet1", "column": "Priority"}] | False |
| B2 | SUM(CASE WHEN "Priority" = 'Urgent' THEN 4 WHEN "Priority" = 'High' THEN 3 WHEN "Priority" = 'Medium' THEN 2 WHEN "Priority" = 'Low' THEN 1 END) | [] | [{"table": "sheet1", "column": "Priority"}, {"table": "sheet1", "column": "Priority"}, {"table": "sheet1", "column": "Priority"}, {"table": "sheet1", "column": "Priority"}] | False |


未解析列血缘：[{"block": "B2", "column": "\"Planned Deadline\"", "reason": "ambiguous_or_missing_source"}, {"block": "B2", "column": "\"Actual Completion Time\"", "reason": "ambiguous_or_missing_source"}, {"block": "B2", "column": "\"Completion Quality Score\"", "reason": "ambiguous_or_missing_source"}, {"block": "B2", "column": "\"Planned Work Hours\"", "reason": "ambiguous_or_missing_source"}, {"block": "B2", "column": "\"Actual Work Hours\"", "reason": "ambiguous_or_missing_source"}, {"block": "B2", "column": "\"Rework Count\"", "reason": "ambiguous_or_missing_source"}, {"block": "B2", "column": "\"Planned Deadline\"", "reason": "ambiguous_or_missing_source"}, {"block": "B2", "column": "\"Actual Completion Time\"", "reason": "ambiguous_or_missing_source"}, {"block": "B2", "column": "\"Completion Quality Score\"", "reason": "ambiguous_or_missing_source"}, {"block": "B2", "column": "\"Planned Work Hours\"", "reason": "ambiguous_or_missing_source"}, {"block": "B2", "column": "\"Actual Work Hours\"", "reason": "ambiguous_or_missing_source"}, {"block": "B2", "column": "\"Rework Count\"", "reason": "ambiguous_or_missing_source"}, {"block": "B2", "column": "\"Actual Completion Time\"", "reason": "ambiguous_or_missing_source"}, {"block": "B2", "column": "\"Planned Deadline\"", "reason": "ambiguous_or_missing_source"}, {"block": "B2", "column": "\"Completion Quality Score\"", "reason": "ambiguous_or_missing_source"}, {"block": "B2", "column": "\"Actual Work Hours\"", "reason": "ambiguous_or_missing_source"}, {"block": "B2", "column": "\"Planned Work Hours\"", "reason": "ambiguous_or_missing_source"}, {"block": "B2", "column": "\"Rework Count\"", "reason": "ambiguous_or_missing_source"}]

## S37

类别 `data`；来源 `python`；调用 `53cf06e12c5342d2a87628842021751e`；状态 `success`。

```sql

SELECT "Task Owner", ROUND(AVG("Task Difficulty Coefficient"),3) AS avg_diff
FROM sheet1 GROUP BY "Task Owner"

```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-013/attempt-01/sql/S37.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-013/attempt-01/sql/S37.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-013/attempt-01/results/S37.rows.jsonl)；完整：True；SHA256：`ec5f1a2b1c2d261624b87245c0ad5720b241fbb43e24de03f14b3b34e4c2905b`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "sheet1", "kind": "base", "block": null, "base_tables": ["sheet1"]}] | [] | ["\"Task Owner\""] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | AVG("Task Difficulty Coefficient") | [{"table": "sheet1", "column": "Task Difficulty Coefficient"}] | [] | False |

