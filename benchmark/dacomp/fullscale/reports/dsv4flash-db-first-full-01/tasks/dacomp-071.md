# dacomp-071

Management is concerned about our hiring funnel efficiency and wants to know which stages …

运行：已提交。官方未评分。全部 SQL 尝试/成功 38/38；数据 SQL 36/36；Python 19 次。

完整原题：

Management is concerned about our hiring funnel efficiency and wants to know which stages are the biggest bottlenecks. By analyzing the average time candidates spend in each hiring stage and the attrition rate, identify key bottleneck stages where the average time spent exceeds 25 days and the attrition rate is higher than 40%. Additionally, calculate an "efficiency index" for each stage (defined as: pass_rate / avg_days * 100), find stages with an efficiency index below 1.5, and provide improvement recommendations based on stage data with at least 100 samples.

| 表 | 行数 | 列数 |
| --- | --- | --- |
| lever__opportunity_enhanced | 5861 | 43 |
| lever__opportunity_stage_history | 8019 | 13 |


实际路线（分析者依据 SQL/源码概括，不代表 Agent 自述）：SQL 提取招聘阶段与归档信息 → Python 重建阶段推进、终止状态及流失率 → 瓶颈与效率指数建议。

数据库大小：6,479,872 字节。

## 数据 SQL

| SQL | 状态 | 基础表 | Join 输入/类型 | GROUP BY | 聚合表达式 | 结果行数 | 数据库 ms |
| --- | --- | --- | --- | --- | --- | --- | --- |
| [S3/Q1](#s3) | success | ["lever__opportunity_stage_history"] | 0 / {} | [] | [] | 20 | 0.582 |
| [S4/Q2](#s4) | success | ["lever__opportunity_stage_history"] | 0 / {} | [] | [] | 10 | 3.948 |
| [S5/Q3](#s5) | success | ["lever__opportunity_stage_history"] | 0 / {} | [] | ["COUNT(*)"] | 1 | 0.301 |
| [S6/Q4](#s6) | success | ["lever__opportunity_stage_history"] | 0 / {} | ["archive_reason"] | ["COUNT(*)"] | 21 | 3.569 |
| [S7/Q5](#s7) | success | ["lever__opportunity_stage_history"] | 0 / {} | ["stage_id", "stage"] | ["COUNT(*)"] | 10 | 4.234 |
| [S8/Q6](#s8) | success | ["lever__opportunity_stage_history"] | 0 / {} | [] | [] | 21 | 3.424 |
| [S9/Q7](#s9) | success | ["lever__opportunity_stage_history"] | 0 / {} | ["archive_reason"] | ["COUNT(*)"] | 21 | 3.476 |
| [S10/Q8](#s10) | success | ["lever__opportunity_stage_history"] | 0 / {} | ["archive_reason"] | ["COUNT(*)"] | 21 | 3.385 |
| [S11/Q9](#s11) | success | ["lever__opportunity_stage_history"] | 0 / {} | ["stage_id", "stage", "archive_reason"] | ["COUNT(*)"] | 112 | 8.126 |
| [S12/Q10](#s12) | success | ["lever__opportunity_stage_history"] | 0 / {} | [] | [] | 8019 | 18.396 |
| [S13/Q11](#s13) | success | ["lever__opportunity_stage_history"] | 0 / {} | [] | [] | 8019 | 17.547 |
| [S14/Q12](#s14) | success | ["lever__opportunity_stage_history"] | 0 / {} | [] | [] | 8019 | 15.872 |
| [S15/Q13](#s15) | success | ["lever__opportunity_stage_history"] | 0 / {} | [] | [] | 8019 | 10.611 |
| [S16/Q14](#s16) | success | ["lever__opportunity_stage_history"] | 0 / {} | [] | [] | 8019 | 10.916 |
| [S17/Q15](#s17) | success | ["lever__opportunity_stage_history"] | 2 / {'LEFT': 1} | ["opportunity_id", "e.stage_id", "e.stage"] | ["MAX(CAST(SUBSTRING(stage_id, 8) AS INTEGER))", "COUNT(DISTINCT e.opportunity_id)", "COUNT(DISTINCT CASE WHEN o.max_stage_num > CAST(SUBSTRING(e.stage_id, 8) AS INTEGER) THEN e.opportunity_id END)", "COUNT(DISTINCT CASE WHEN o.max_stage_num = CAST(SUBSTRING(e.stage_id, 8) AS INTEGER) AND NOT e.archive_reason IN ('Advanced to next stage', 'Qualified', 'Proceeding', 'Hired') THEN e.opportunity_id END)", "COUNT(DISTINCT CASE WHEN o.max_stage_num = CAST(SUBSTRING(e.stage_id, 8) AS INTEGER) AND e.archive_reason = 'Proceeding' THEN e.opportunity_id END)", "COUNT(DISTINCT CASE WHEN o.max_stage_num = CAST(SUBSTRING(e.stage_id, 8) AS INTEGER) AND e.archive_reason = 'Hired' THEN e.opportunity_id END)", "AVG(e.days_in_stage)"] | 10 | 31.036 |
| [S18/Q16](#s18) | success | ["lever__opportunity_stage_history"] | 0 / {} | [] | [] | 8019 | 10.546 |
| [S19/Q17](#s19) | success | ["lever__opportunity_stage_history"] | 0 / {} | [] | [] | 10 | 0.612 |
| [S20/Q18](#s20) | success | ["lever__opportunity_stage_history"] | 0 / {} | ["archive_reason"] | ["COUNT(*)"] | 1 | 1.834 |
| [S21/Q19](#s21) | success | ["lever__opportunity_stage_history"] | 0 / {} | [] | [] | 8019 | 10.681 |
| [S22/Q20](#s22) | success | ["lever__opportunity_stage_history"] | 0 / {} | [] | [] | 8019 | 10.573 |
| [S23/Q21](#s23) | success | ["lever__opportunity_stage_history"] | 0 / {} | [] | [] | 8019 | 10.513 |
| [S24/Q22](#s24) | success | ["lever__opportunity_enhanced"] | 0 / {} | ["current_stage"] | ["COUNT(*)"] | 10 | 5.366 |
| [S25/Q23](#s25) | success | ["lever__opportunity_enhanced"] | 0 / {} | ["archive_reason"] | ["COUNT(*)"] | 14 | 4.814 |
| [S26/Q24](#s26) | success | ["lever__opportunity_enhanced"] | 0 / {} | [] | ["COUNT(*)"] | 1 | 2.363 |
| [S27/Q25](#s27) | success | ["lever__opportunity_enhanced"] | 0 / {} | [] | ["COUNT(DISTINCT opportunity_id)"] | 1 | 5.499 |
| [S28/Q26](#s28) | success | ["lever__opportunity_stage_history"] | 0 / {} | ["stage_id", "stage"] | ["MIN(days_in_stage)", "MAX(days_in_stage)", "COUNT(*)", "AVG(days_in_stage)"] | 10 | 5.709 |
| [S29/Q27](#s29) | success | ["lever__opportunity_stage_history"] | 0 / {} | [] | [] | 8019 | 10.74 |
| [S30/Q28](#s30) | success | ["lever__opportunity_stage_history"] | 0 / {} | [] | [] | 8019 | 10.943 |
| [S31/Q29](#s31) | success | ["lever__opportunity_stage_history"] | 0 / {} | ["stage", "archive_reason"] | ["COUNT(*)"] | 19 | 3.701 |
| [S32/Q30](#s32) | success | ["lever__opportunity_stage_history"] | 0 / {} | ["stage", "job_team"] | ["COUNT(*)", "AVG(days_in_stage)"] | 14 | 2.649 |
| [S33/Q31](#s33) | success | ["lever__opportunity_stage_history"] | 0 / {} | [] | [] | 8019 | 10.258 |
| [S34/Q32](#s34) | success | ["lever__opportunity_stage_history"] | 0 / {} | [] | [] | 8019 | 10.46 |
| [S35/Q33](#s35) | success | ["lever__opportunity_stage_history"] | 0 / {} | [] | [] | 1566 | 4.738 |
| [S36/Q34](#s36) | success | ["lever__opportunity_stage_history"] | 0 / {} | [] | [] | 8019 | 15.13 |
| [S37/Q35](#s37) | success | ["lever__opportunity_stage_history"] | 0 / {} | [] | [] | 8019 | 10.303 |
| [S38/Q36](#s38) | success | ["lever__opportunity_stage_history"] | 0 / {} | [] | [] | 8019 | 13.438 |


## 元数据和设置

| SQL | 类别 | 状态 | 内容 |
| --- | --- | --- | --- |
| S1 | connection_setup | success | PRAGMA query_only=ON |
| S2 | metadata | success | SELECT name,sql FROM sqlite_master WHERE type='table' ORDER BY name |


## Python 与执行位置

人工源码审查：**database_first_violation**。Python 在招聘阶段明细上执行分组行号、组总数和最大阶段，并连接回原表，反复计算通过/流失数量、平均时长与团队流失率。SQLite 的窗口、连接及条件聚合能够完成这些工作，属于明确的数据库优先偏离。 [证据](../reviews/dacomp-071.json)。

P1：Retrieve the full archive_reason value list and stage x archive_reason cross-tabulation, which the SQL preview truncated. This is just reading full query results into a frame for inspection; no SQL-capable computation is being moved to Python.

[源码](../../../runs/dsv4flash-db-first-full-01/dacomp-071/attempt-01/python/P1.py)；[输出](../../../runs/dsv4flash-db-first-full-01/dacomp-071/attempt-01/python/P1.stdout)；[错误](../../../runs/dsv4flash-db-first-full-01/dacomp-071/attempt-01/python/P1.stderr)。检出需人工核验的 SQL 可实现操作：groupby(, .query(, sort_values(；不能仅凭理由判为合规。

P2：Check whether archive_reason is opportunity-level (same reason on all rows of an opportunity) or stage-level, and whether there are multiple records per stage. This determines how pass/attrition should be computed; it is data-structure inspection that is clearer in Python.

[源码](../../../runs/dsv4flash-db-first-full-01/dacomp-071/attempt-01/python/P2.py)；[输出](../../../runs/dsv4flash-db-first-full-01/dacomp-071/attempt-01/python/P2.stdout)；[错误](../../../runs/dsv4flash-db-first-full-01/dacomp-071/attempt-01/python/P2.stderr)。检出需人工核验的 SQL 可实现操作：groupby(, .query(；不能仅凭理由判为合规。

P3：Evaluate consistency between two definitions of pass/attrition (presence of a later stage record vs. archive_reason classification) to decide the most defensible definition for pass_rate and attrition_rate. This consistency check is easier in Python on the small set of needed columns.

[源码](../../../runs/dsv4flash-db-first-full-01/dacomp-071/attempt-01/python/P3.py)；[输出](../../../runs/dsv4flash-db-first-full-01/dacomp-071/attempt-01/python/P3.stdout)；[错误](../../../runs/dsv4flash-db-first-full-01/dacomp-071/attempt-01/python/P3.stderr)。检出需人工核验的 SQL 可实现操作：groupby(, .query(, sort_values(；不能仅凭理由判为合规。

P4：Inspect concrete multi-stage opportunity examples to understand whether archive_reason is per-stage outcome or an opportunity-level final reason, which determines the pass/attrition definition.

[源码](../../../runs/dsv4flash-db-first-full-01/dacomp-071/attempt-01/python/P4.py)；[输出](../../../runs/dsv4flash-db-first-full-01/dacomp-071/attempt-01/python/P4.stdout)；[错误](../../../runs/dsv4flash-db-first-full-01/dacomp-071/attempt-01/python/P4.stderr)。检出需人工核验的 SQL 可实现操作：groupby(, .query(；不能仅凭理由判为合规。

P5：Recompute pass/attrition consistency using the funnel order defined by stage_id (STAGE_01..STAGE_10), since valid_from timestamps appear not to be chronological in this dataset. This determines the correct per-stage pass/attrition definition.

[源码](../../../runs/dsv4flash-db-first-full-01/dacomp-071/attempt-01/python/P5.py)；[输出](../../../runs/dsv4flash-db-first-full-01/dacomp-071/attempt-01/python/P5.stdout)；[错误](../../../runs/dsv4flash-db-first-full-01/dacomp-071/attempt-01/python/P5.stderr)。检出需人工核验的 SQL 可实现操作：groupby(, .query(, sort_values(；不能仅凭理由判为合规。

P6：Inspect the 899 inconsistent rows (negative reason yet a later-stage record) to determine whether archive_reason should still be trusted as the per-stage outcome for pass/attrition computation.

[源码](../../../runs/dsv4flash-db-first-full-01/dacomp-071/attempt-01/python/P6.py)；[输出](../../../runs/dsv4flash-db-first-full-01/dacomp-071/attempt-01/python/P6.stdout)；[错误](../../../runs/dsv4flash-db-first-full-01/dacomp-071/attempt-01/python/P6.stderr)。检出需人工核验的 SQL 可实现操作：groupby(, .query(, sort_values(；不能仅凭理由判为合规。

P7：Compute per-stage funnel metrics (avg_days, advanced, attrited, proceeding, pass_rate, attrition_rate, efficiency index) using stage_id ordering since valid_from timestamps are not chronological. The SQL for this was becoming complex; Python with pandas on the small columns needed provides a cleaner, verifiable computation.

[源码](../../../runs/dsv4flash-db-first-full-01/dacomp-071/attempt-01/python/P7.py)；[输出](../../../runs/dsv4flash-db-first-full-01/dacomp-071/attempt-01/python/P7.stdout)；[错误](../../../runs/dsv4flash-db-first-full-01/dacomp-071/attempt-01/python/P7.stderr)。检出需人工核验的 SQL 可实现操作：groupby(, .merge(, .query(, sort_values(；不能仅凭理由判为合规。

P8：Debug why Hired stage shows hired=0 in the previous computation by checking the max_stage_num and archive_reason values for Hired stage opportunities.

[源码](../../../runs/dsv4flash-db-first-full-01/dacomp-071/attempt-01/python/P8.py)；[输出](../../../runs/dsv4flash-db-first-full-01/dacomp-071/attempt-01/python/P8.stdout)；[错误](../../../runs/dsv4flash-db-first-full-01/dacomp-071/attempt-01/python/P8.stderr)。检出需人工核验的 SQL 可实现操作：groupby(, .merge(, .query(；不能仅凭理由判为合规。

P9：Understand the 'Proceeding' status - how many are terminal (in-progress at their furthest stage) vs. intermediate, to correctly handle in-progress candidates in attrition/pass calculations.

[源码](../../../runs/dsv4flash-db-first-full-01/dacomp-071/attempt-01/python/P9.py)；[输出](../../../runs/dsv4flash-db-first-full-01/dacomp-071/attempt-01/python/P9.stdout)；[错误](../../../runs/dsv4flash-db-first-full-01/dacomp-071/attempt-01/python/P9.stderr)。检出需人工核验的 SQL 可实现操作：groupby(, .query(, sort_values(；不能仅凭理由判为合规。

P10：Compare two candidate definitions of pass/attrition (progression-based vs archive_reason-based) to assess robustness of the bottleneck conclusions before finalizing the methodology.

[源码](../../../runs/dsv4flash-db-first-full-01/dacomp-071/attempt-01/python/P10.py)；[输出](../../../runs/dsv4flash-db-first-full-01/dacomp-071/attempt-01/python/P10.stdout)；[错误](../../../runs/dsv4flash-db-first-full-01/dacomp-071/attempt-01/python/P10.stderr)。检出需人工核验的 SQL 可实现操作：groupby(, .query(, sort_values(；不能仅凭理由判为合规。

P11：Compute final per-stage metrics including avg_days, pass_rate, attrition_rate, efficiency index, and identify bottleneck stages and low-efficiency stages. This is the main analysis performed in Python for clarity and to produce the visualizations below.

[源码](../../../runs/dsv4flash-db-first-full-01/dacomp-071/attempt-01/python/P11.py)；[输出](../../../runs/dsv4flash-db-first-full-01/dacomp-071/attempt-01/python/P11.stdout)；[错误](../../../runs/dsv4flash-db-first-full-01/dacomp-071/attempt-01/python/P11.stderr)。检出需人工核验的 SQL 可实现操作：groupby(, .query(, sort_values(；不能仅凭理由判为合规。

P12：Compute final per-stage metrics (avg_days, pass_rate, attrition_rate, efficiency index), identify bottleneck stages (avg_days>25 & attrition>40%) and low-efficiency stages (eff_index<1.5). This is the core analysis, done in Python for clear computation and to feed visualizations.

[源码](../../../runs/dsv4flash-db-first-full-01/dacomp-071/attempt-01/python/P12.py)；[输出](../../../runs/dsv4flash-db-first-full-01/dacomp-071/attempt-01/python/P12.stdout)；[错误](../../../runs/dsv4flash-db-first-full-01/dacomp-071/attempt-01/python/P12.stderr)。检出需人工核验的 SQL 可实现操作：groupby(, .query(, sort_values(；不能仅凭理由判为合规。

P13：Create a combined visualization (avg days, attrition rate, efficiency index per stage with threshold lines) to support the report. Python/matplotlib is used because this is a visualization task not supported by SQLite.

[源码](../../../runs/dsv4flash-db-first-full-01/dacomp-071/attempt-01/python/P13.py)；[输出](../../../runs/dsv4flash-db-first-full-01/dacomp-071/attempt-01/python/P13.stdout)；[错误](../../../runs/dsv4flash-db-first-full-01/dacomp-071/attempt-01/python/P13.stderr)。检出需人工核验的 SQL 可实现操作：groupby(, .query(, sort_values(；不能仅凭理由判为合规。

P14：Check the working directory structure to determine the correct relative path for saving figures.

[源码](../../../runs/dsv4flash-db-first-full-01/dacomp-071/attempt-01/python/P14.py)；[输出](../../../runs/dsv4flash-db-first-full-01/dacomp-071/attempt-01/python/P14.stdout)；[错误](../../../runs/dsv4flash-db-first-full-01/dacomp-071/attempt-01/python/P14.stderr)。自动源码筛查未检出预设迁出信号；这不是全面语义合规证明。

P15：Create the combined bottleneck visualization (avg days, attrition rate, efficiency index per stage) and save it as a relative-path figure in /work. This is a matplotlib visualization task, not supported by SQLite.

[源码](../../../runs/dsv4flash-db-first-full-01/dacomp-071/attempt-01/python/P15.py)；[输出](../../../runs/dsv4flash-db-first-full-01/dacomp-071/attempt-01/python/P15.stdout)；[错误](../../../runs/dsv4flash-db-first-full-01/dacomp-071/attempt-01/python/P15.stderr)。检出需人工核验的 SQL 可实现操作：groupby(, .query(, sort_values(；不能仅凭理由判为合规。

P16：Deep dive into the two bottleneck stages (Technical Assessment and Final Interview) to understand attrition reasons, team distributions, and time patterns. This informs data-driven improvement recommendations.

[源码](../../../runs/dsv4flash-db-first-full-01/dacomp-071/attempt-01/python/P16.py)；[输出](../../../runs/dsv4flash-db-first-full-01/dacomp-071/attempt-01/python/P16.stdout)；[错误](../../../runs/dsv4flash-db-first-full-01/dacomp-071/attempt-01/python/P16.stderr)。检出需人工核验的 SQL 可实现操作：groupby(, .query(, sort_values(；不能仅凭理由判为合规。

P17：Recompute the deep-dive statistics for Technical Assessment and Final Interview bottleneck stages using the full dataset (not filtered subset) to ensure correct has_next computation. This is needed for accurate improvement recommendations.

[源码](../../../runs/dsv4flash-db-first-full-01/dacomp-071/attempt-01/python/P17.py)；[输出](../../../runs/dsv4flash-db-first-full-01/dacomp-071/attempt-01/python/P17.stdout)；[错误](../../../runs/dsv4flash-db-first-full-01/dacomp-071/attempt-01/python/P17.stderr)。检出需人工核验的 SQL 可实现操作：groupby(, .query(, sort_values(；不能仅凭理由判为合规。

P18：Create a funnel visualization showing the candidate count per stage to visually identify bottlenecks, and prepare the final metrics table for the report. Matplotlib is needed for visualization.

[源码](../../../runs/dsv4flash-db-first-full-01/dacomp-071/attempt-01/python/P18.py)；[输出](../../../runs/dsv4flash-db-first-full-01/dacomp-071/attempt-01/python/P18.stdout)；[错误](../../../runs/dsv4flash-db-first-full-01/dacomp-071/attempt-01/python/P18.stderr)。检出需人工核验的 SQL 可实现操作：groupby(, .query(, sort_values(；不能仅凭理由判为合规。

P19：Quantify the data-quality inconsistency (negative reasons among candidates who advanced) and produce attrition-reason breakdowns with percentages for the bottleneck stages to support recommendations. These are simple aggregations over the needed columns, computed in Python for formatting.

[源码](../../../runs/dsv4flash-db-first-full-01/dacomp-071/attempt-01/python/P19.py)；[输出](../../../runs/dsv4flash-db-first-full-01/dacomp-071/attempt-01/python/P19.stdout)；[错误](../../../runs/dsv4flash-db-first-full-01/dacomp-071/attempt-01/python/P19.stderr)。检出需人工核验的 SQL 可实现操作：groupby(, .query(, sort_values(；不能仅凭理由判为合规。

## 优化机会

已验证候选。筛选限于精确 SQL、相同自包含 CTE、相同单表完整过滤、可分解单表聚合；未覆盖任意 Join 等价和一般谓词蕴含。全部候选都是 offline，未测在线预测。

| 候选 | 类型 | 已有结果 | 覆盖 SQL | 后续次数 | 中间行数 | 验证 | 成本 |
| --- | --- | --- | --- | --- | --- | --- | --- |
| C1 | exact-result reuse | True | ["S9", "S10"] | 1 | unknown | not_verified_cap | Not tested |
| C2 | exact-result reuse | True | ["S12", "S13"] | 1 | unknown | not_verified_cap | Not tested |
| C3 | exact-result reuse | True | ["S15", "S16", "S18", "S21", "S22", "S23", "S29", "S30", "S33", "S34", "S37"] | 10 | 8019 | verified | Not benchmarked; correctness alone does not establish net speedup. |
| C4 | aggregate MV | False | ["S5", "S6", "S7", "S9", "S10", "S11", "S28"] | 6 | 112 | verified | Not benchmarked; correctness alone does not establish net speedup. |
| C5 | common filtered view | False | ["S19", "S20"] | 1 | unknown | not_verified_cap | Not tested |
| C6 | aggregate MV | False | ["S24", "S25", "S26"] | 2 | 100 | verified | Not benchmarked; correctness alone does not establish net speedup. |
| C7 | common filtered view | False | ["S31", "S32", "S35"] | 2 | unknown | not_verified_cap | Not tested |
| C8 | aggregate MV | False | ["S31", "S32"] | 1 | unknown | not_verified_cap | Not tested |


已验证覆盖（含触发查询、候选并集去重）：21/36 条成功数据 SQL。正确性仅针对当前数据库快照；未测性能的候选不能声称已加速。

[完整 build/rewrite 与比较证据](dacomp-071.analysis.json)。

### C3：exact-result reuse

Identical normalized SQL and parameters; archive equality checked.

原查询 [S15](#s15), [S16](#s16), [S18](#s18), [S21](#s21), [S22](#s22), [S23](#s23), [S29](#s29), [S30](#s30), [S33](#s33), [S34](#s34), [S37](#s37) → 保留前序结果 S15 → 后续 10 次可复用。该构建点为事后假设，不代表 Agent 当时预知后续。

| 原 SQL | 列名一致 | 结果一致 | 比较方法 |
| --- | --- | --- | --- |
| S16 | True | True | exact_multiset |
| S18 | True | True | exact_multiset |
| S21 | True | True | exact_multiset |
| S22 | True | True | exact_multiset |
| S23 | True | True | exact_multiset |
| S29 | True | True | exact_multiset |
| S30 | True | True | exact_multiset |
| S33 | True | True | exact_multiset |
| S34 | True | True | exact_multiset |
| S37 | True | True | exact_multiset |


验证状态：verified；成本结论：Not benchmarked; correctness alone does not establish net speedup.

### C4：aggregate MV

Union of grouping keys; decomposable aggregate states; AVG uses SUM and non-NULL COUNT.

原查询 [S5](#s5), [S6](#s6), [S7](#s7), [S9](#s9), [S10](#s10), [S11](#s11), [S28](#s28) → 新增共享状态 C4 → 后续 6 次可复用。该构建点为事后假设，不代表 Agent 当时预知后续。

构建定义：

```sql
SELECT archive_reason AS __g0, stage_id AS __g1, stage AS __g2, COUNT(*) AS __a0, MIN(days_in_stage) AS __a1, MAX(days_in_stage) AS __a2, SUM(days_in_stage) AS __a3_sum, COUNT(days_in_stage) AS __a3_n FROM "lever__opportunity_stage_history"  GROUP BY archive_reason, stage_id, stage
```

受益查询 S5 的改写示例：

```sql
SELECT SUM(__a0) AS total_rows FROM temp.reuse_candidate
```

| 原 SQL | 列名一致 | 结果一致 | 比较方法 |
| --- | --- | --- | --- |
| S5 | True | True | exact_multiset |
| S6 | True | True | ordered_numeric_tolerance |
| S7 | True | True | ordered_numeric_tolerance |
| S9 | True | True | ordered_numeric_tolerance |
| S10 | True | True | ordered_numeric_tolerance |
| S11 | True | True | ordered_numeric_tolerance |
| S28 | True | True | ordered_numeric_tolerance |


验证状态：verified；成本结论：Not benchmarked; correctness alone does not establish net speedup.

### C6：aggregate MV

Union of grouping keys; decomposable aggregate states; AVG uses SUM and non-NULL COUNT.

原查询 [S24](#s24), [S25](#s25), [S26](#s26) → 新增共享状态 C6 → 后续 2 次可复用。该构建点为事后假设，不代表 Agent 当时预知后续。

构建定义：

```sql
SELECT current_stage AS __g0, archive_reason AS __g1, COUNT(*) AS __a0 FROM "lever__opportunity_enhanced"  GROUP BY current_stage, archive_reason
```

受益查询 S24 的改写示例：

```sql
SELECT __g0 AS "current_stage", SUM(__a0) AS cnt FROM temp.reuse_candidate GROUP BY __g0 ORDER BY cnt DESC
```

| 原 SQL | 列名一致 | 结果一致 | 比较方法 |
| --- | --- | --- | --- |
| S24 | True | True | ordered_numeric_tolerance |
| S25 | True | True | ordered_numeric_tolerance |
| S26 | True | True | exact_multiset |


验证状态：verified；成本结论：Not benchmarked; correctness alone does not establish net speedup.

结果依赖：自动记录 SQL→Python 的接口父调用，以及源码中引用归档文件的消费者；字面值相同不认定因果。模型方向选择需要人工读取消息，尚未做全面因果标注。

[原始报告](../../../runs/dsv4flash-db-first-full-01/dacomp-071/attempt-01/answer.md)；[统一消息](../../../runs/dsv4flash-db-first-full-01/dacomp-071/attempt-01/messages.jsonl)；[原始 OpenCode 事件](../../../runs/dsv4flash-db-first-full-01/dacomp-071/attempt-01/opencode.jsonl)；[SQL 引擎日志](../../../runs/dsv4flash-db-first-full-01/dacomp-071/attempt-01/sql_journal.jsonl)。

[可读报告（本地图片链接规范化）](../answers/dacomp-071.md)。原始回答保留，分析结论未改写。

## S1

类别 `connection_setup`；来源 `connection`；调用 `fe200afcff9740ed9378f156c47764be`；状态 `success`。

```sql
PRAGMA query_only=ON
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-071/attempt-01/sql/S1.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-071/attempt-01/sql/S1.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-071/attempt-01/results/S1.rows.jsonl)；完整：True；SHA256：`e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`。

## S2

类别 `metadata`；来源 `list_db`；调用 `fe200afcff9740ed9378f156c47764be`；状态 `success`。

```sql
SELECT name,sql FROM sqlite_master WHERE type='table' ORDER BY name
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-071/attempt-01/sql/S2.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-071/attempt-01/sql/S2.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-071/attempt-01/results/S2.rows.jsonl)；完整：True；SHA256：`61039a6d5a9bc991895f7fdf4144422e15cda951e5d236bd93e355262389002a`。

## S3

类别 `data`；来源 `query_db`；调用 `6626a9d3346d42789e5411a60af1e61d`；状态 `success`。

```sql
SELECT * FROM lever__opportunity_stage_history LIMIT 20
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-071/attempt-01/sql/S3.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-071/attempt-01/sql/S3.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-071/attempt-01/results/S3.rows.jsonl)；完整：True；SHA256：`297b6fe1b4d2687320cae994f98f3bc53137f9b2e583ee00d53b70015477013a`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "lever__opportunity_stage_history", "kind": "base", "block": null, "base_tables": ["lever__opportunity_stage_history"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |


## S4

类别 `data`；来源 `query_db`；调用 `1929bbd7ab9d40e7a77d4a9224c8f2f0`；状态 `success`。

```sql
SELECT DISTINCT stage FROM lever__opportunity_stage_history ORDER BY stage
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-071/attempt-01/sql/S4.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-071/attempt-01/sql/S4.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-071/attempt-01/results/S4.rows.jsonl)；完整：True；SHA256：`620aa3377e7b51ea4298c925578cf7f932d2651ad5a7e1e70d6d1edbba7fcc00`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "lever__opportunity_stage_history", "kind": "base", "block": null, "base_tables": ["lever__opportunity_stage_history"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |


## S5

类别 `data`；来源 `query_db`；调用 `8d5d5af9147e444a9c5184cc8e865606`；状态 `success`。

```sql
SELECT COUNT(*) as total_rows FROM lever__opportunity_stage_history
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-071/attempt-01/sql/S5.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-071/attempt-01/sql/S5.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-071/attempt-01/results/S5.rows.jsonl)；完整：True；SHA256：`4d5040c525180f324f1a2d356f55b71c885f238c37f55c9d4c6e24b1c62da04e`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "lever__opportunity_stage_history", "kind": "base", "block": null, "base_tables": ["lever__opportunity_stage_history"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |


## S6

类别 `data`；来源 `query_db`；调用 `de8cdc4d0d9d47abb2439e3ad2b6414f`；状态 `success`。

```sql
SELECT archive_reason, COUNT(*) as cnt FROM lever__opportunity_stage_history GROUP BY archive_reason ORDER BY cnt DESC
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-071/attempt-01/sql/S6.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-071/attempt-01/sql/S6.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-071/attempt-01/results/S6.rows.jsonl)；完整：True；SHA256：`caef439f4183b4b89436b30c435e505c29c81bab9e9a167224ea559d48edde77`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "lever__opportunity_stage_history", "kind": "base", "block": null, "base_tables": ["lever__opportunity_stage_history"]}] | [] | ["archive_reason"] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |


## S7

类别 `data`；来源 `query_db`；调用 `0217bdaf31264511816d2b44dc125cdb`；状态 `success`。

```sql
SELECT stage_id, stage, COUNT(*) as cnt FROM lever__opportunity_stage_history GROUP BY stage_id, stage ORDER BY stage_id
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-071/attempt-01/sql/S7.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-071/attempt-01/sql/S7.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-071/attempt-01/results/S7.rows.jsonl)；完整：True；SHA256：`83c6339c439dfa7af86acc9e21a78dc8df18befc682993a931a3e8399c7dd38c`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "lever__opportunity_stage_history", "kind": "base", "block": null, "base_tables": ["lever__opportunity_stage_history"]}] | [] | ["stage_id", "stage"] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |


## S8

类别 `data`；来源 `query_db`；调用 `b9799008d7264341b08301804bf00651`；状态 `success`。

```sql
SELECT DISTINCT archive_reason FROM lever__opportunity_stage_history ORDER BY archive_reason
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-071/attempt-01/sql/S8.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-071/attempt-01/sql/S8.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-071/attempt-01/results/S8.rows.jsonl)；完整：True；SHA256：`81a0ddb733ab165a660f8fc9f764ee49e445125612ad9481c6212cd1b791b811`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "lever__opportunity_stage_history", "kind": "base", "block": null, "base_tables": ["lever__opportunity_stage_history"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |


## S9

类别 `data`；来源 `query_db`；调用 `5a067571391946398fdf42a11ec58ac2`；状态 `success`。

```sql
SELECT archive_reason, COUNT(*) as cnt FROM lever__opportunity_stage_history GROUP BY archive_reason ORDER BY archive_reason
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-071/attempt-01/sql/S9.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-071/attempt-01/sql/S9.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-071/attempt-01/results/S9.rows.jsonl)；完整：True；SHA256：`14799e1fdd13c9123bba2a6daf0ab8864cd686e5f54f56e601fe7f0222886852`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "lever__opportunity_stage_history", "kind": "base", "block": null, "base_tables": ["lever__opportunity_stage_history"]}] | [] | ["archive_reason"] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |


## S10

类别 `data`；来源 `query_db`；调用 `241ec22d8f0a42329be869a9e4858a0d`；状态 `success`。

```sql
SELECT archive_reason, COUNT(*) as cnt FROM lever__opportunity_stage_history GROUP BY archive_reason ORDER BY archive_reason
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-071/attempt-01/sql/S10.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-071/attempt-01/sql/S10.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-071/attempt-01/results/S10.rows.jsonl)；完整：True；SHA256：`14799e1fdd13c9123bba2a6daf0ab8864cd686e5f54f56e601fe7f0222886852`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "lever__opportunity_stage_history", "kind": "base", "block": null, "base_tables": ["lever__opportunity_stage_history"]}] | [] | ["archive_reason"] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |


## S11

类别 `data`；来源 `python`；调用 `39607196e39749b689a5f03b547935c3`；状态 `success`。

```sql

SELECT stage_id, stage, archive_reason, COUNT(*) as cnt
FROM lever__opportunity_stage_history
GROUP BY stage_id, stage, archive_reason
ORDER BY stage_id, cnt DESC

```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-071/attempt-01/sql/S11.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-071/attempt-01/sql/S11.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-071/attempt-01/results/S11.rows.jsonl)；完整：True；SHA256：`f3804ff85082902f092cc67edab0a1856eefee1742dc0ed234d4841aa9231c00`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "lever__opportunity_stage_history", "kind": "base", "block": null, "base_tables": ["lever__opportunity_stage_history"]}] | [] | ["stage_id", "stage", "archive_reason"] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |


## S12

类别 `data`；来源 `python`；调用 `4cbba8ab3fdc4894aed44cef2abe0db4`；状态 `success`。

```sql

SELECT opportunity_id, stage_id, stage, valid_from, valid_ending_at, archive_reason, days_in_stage
FROM lever__opportunity_stage_history
ORDER BY opportunity_id, valid_from

```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-071/attempt-01/sql/S12.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-071/attempt-01/sql/S12.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-071/attempt-01/results/S12.rows.jsonl)；完整：True；SHA256：`f50f3a8451d963f28e9fbf1ce442ef3529e26d6ff11c92e24b979c3b54403f90`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "lever__opportunity_stage_history", "kind": "base", "block": null, "base_tables": ["lever__opportunity_stage_history"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |


## S13

类别 `data`；来源 `python`；调用 `83ffa11b6ef34331b246fb7c09e5ea02`；状态 `success`。

```sql

SELECT opportunity_id, stage_id, stage, valid_from, valid_ending_at, archive_reason, days_in_stage
FROM lever__opportunity_stage_history
ORDER BY opportunity_id, valid_from

```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-071/attempt-01/sql/S13.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-071/attempt-01/sql/S13.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-071/attempt-01/results/S13.rows.jsonl)；完整：True；SHA256：`f50f3a8451d963f28e9fbf1ce442ef3529e26d6ff11c92e24b979c3b54403f90`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "lever__opportunity_stage_history", "kind": "base", "block": null, "base_tables": ["lever__opportunity_stage_history"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |


## S14

类别 `data`；来源 `python`；调用 `4b1b299172754f85855bc4ed8f69425d`；状态 `success`。

```sql

SELECT opportunity_id, stage_id, stage, valid_from, archive_reason, days_in_stage
FROM lever__opportunity_stage_history
ORDER BY opportunity_id, valid_from

```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-071/attempt-01/sql/S14.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-071/attempt-01/sql/S14.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-071/attempt-01/results/S14.rows.jsonl)；完整：True；SHA256：`8738ca73cbf18536d3a537b06af1caa9c4cb99703afbd130f0602284ab95856c`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "lever__opportunity_stage_history", "kind": "base", "block": null, "base_tables": ["lever__opportunity_stage_history"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |


## S15

类别 `data`；来源 `python`；调用 `34599c487a60431495c637af5aeaecf2`；状态 `success`。

```sql

SELECT opportunity_id, stage_id, stage, archive_reason, days_in_stage
FROM lever__opportunity_stage_history

```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-071/attempt-01/sql/S15.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-071/attempt-01/sql/S15.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-071/attempt-01/results/S15.rows.jsonl)；完整：True；SHA256：`e4a4aae70f8f453db5252a05e93106ed67fe096b219d95946e2471298a449d0b`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "lever__opportunity_stage_history", "kind": "base", "block": null, "base_tables": ["lever__opportunity_stage_history"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |


## S16

类别 `data`；来源 `python`；调用 `cf229284330d4f64a25fe994e7b6135c`；状态 `success`。

```sql

SELECT opportunity_id, stage_id, stage, archive_reason, days_in_stage
FROM lever__opportunity_stage_history

```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-071/attempt-01/sql/S16.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-071/attempt-01/sql/S16.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-071/attempt-01/results/S16.rows.jsonl)；完整：True；SHA256：`e4a4aae70f8f453db5252a05e93106ed67fe096b219d95946e2471298a449d0b`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "lever__opportunity_stage_history", "kind": "base", "block": null, "base_tables": ["lever__opportunity_stage_history"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |


## S17

类别 `data`；来源 `query_db`；调用 `7930e67a62484a06bc83942ddcb58721`；状态 `success`。

```sql
WITH stage_order AS (
    SELECT DISTINCT stage_id, stage,
           CAST(SUBSTR(stage_id, 8) AS INTEGER) AS stage_num
    FROM lever__opportunity_stage_history
),
stage_entries AS (
    SELECT stage_id, stage, opportunity_id, archive_reason, days_in_stage
    FROM lever__opportunity_stage_history
),
-- For each opportunity, find the max stage_num they reached
opp_max_stage AS (
    SELECT opportunity_id, MAX(CAST(SUBSTR(stage_id, 8) AS INTEGER)) AS max_stage_num
    FROM lever__opportunity_stage_history
    GROUP BY opportunity_id
),
-- Per stage: count entries, advanced, attrited, proceeding
stage_stats AS (
    SELECT 
        e.stage_id,
        e.stage,
        CAST(SUBSTR(e.stage_id, 8) AS INTEGER) AS stage_num,
        COUNT(DISTINCT e.opportunity_id) AS total_entries,
        ROUND(AVG(e.days_in_stage), 1) AS avg_days,
        -- Count candidates who advanced (have a later stage)
        COUNT(DISTINCT CASE WHEN o.max_stage_num > CAST(SUBSTR(e.stage_id, 8) AS INTEGER) THEN e.opportunity_id END) AS advanced,
        -- Count candidates who are at their terminal stage with a negative reason (attrition)
        COUNT(DISTINCT CASE WHEN o.max_stage_num = CAST(SUBSTR(e.stage_id, 8) AS INTEGER) 
                             AND e.archive_reason NOT IN ('Advanced to next stage','Qualified','Proceeding','Hired')
                        THEN e.opportunity_id END) AS attrited,
        -- Count candidates still proceeding
        COUNT(DISTINCT CASE WHEN o.max_stage_num = CAST(SUBSTR(e.stage_id, 8) AS INTEGER) 
                             AND e.archive_reason = 'Proceeding'
                        THEN e.opportunity_id END) AS proceeding,
        -- Count candidates hired at this stage
        COUNT(DISTINCT CASE WHEN o.max_stage_num = CAST(SUBSTR(e.stage_id, 8) AS INTEGER) 
                             AND e.archive_reason = 'Hired'
                        THEN e.opportunity_id END) AS hired
    FROM stage_entries e
    LEFT JOIN opp_max_stage o ON e.opportunity_id = o.opportunity_id
    GROUP BY e.stage_id, e.stage
)
SELECT 
    stage_id,
    stage,
    total_entries,
    avg_days,
    advanced,
    attrited,
    proceeding,
    hired,
    ROUND(CAST(advanced AS REAL) / total_entries * 100, 1) AS pass_rate_pct,
    ROUND(CAST(attrited AS REAL) / total_entries * 100, 1) AS attrition_rate_pct,
    ROUND(CAST(advanced AS REAL) / NULLIF(total_entries - proceeding, 0) * 100, 1) AS resolved_pass_rate_pct,
    ROUND(CAST(attrited AS REAL) / NULLIF(total_entries - proceeding, 0) * 100, 1) AS resolved_attrition_rate_pct
FROM stage_stats
ORDER BY stage_num
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-071/attempt-01/sql/S17.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-071/attempt-01/sql/S17.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-071/attempt-01/results/S17.rows.jsonl)；完整：True；SHA256：`b27d06d83684af1b8d7c1721568854b83ebfb7d7bcc0ca86a00a1f050397eec7`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "lever__opportunity_stage_history", "kind": "base", "block": null, "base_tables": ["lever__opportunity_stage_history"]}] | [] | [] |
| B2 | [{"alias": "lever__opportunity_stage_history", "kind": "base", "block": null, "base_tables": ["lever__opportunity_stage_history"]}] | [] | [] |
| B3 | [{"alias": "lever__opportunity_stage_history", "kind": "base", "block": null, "base_tables": ["lever__opportunity_stage_history"]}] | [] | ["opportunity_id"] |
| B4 | [{"alias": "e", "kind": "derived", "block": "B2", "base_tables": ["lever__opportunity_stage_history"]}, {"alias": "o", "kind": "derived", "block": "B3", "base_tables": ["lever__opportunity_stage_history"]}] | [{"type": "LEFT", "right": "opp_max_stage AS o", "on": "e.opportunity_id = o.opportunity_id", "using": []}] | ["e.stage_id", "e.stage"] |
| B5 | [{"alias": "stage_stats", "kind": "derived", "block": "B4", "base_tables": ["lever__opportunity_stage_history"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B3 | MAX(CAST(SUBSTRING(stage_id, 8) AS INTEGER)) | [{"table": "lever__opportunity_stage_history", "column": "stage_id"}] | [] | False |
| B4 | COUNT(DISTINCT e.opportunity_id) | [{"table": "lever__opportunity_stage_history", "column": "opportunity_id"}] | [] | False |
| B4 | COUNT(DISTINCT CASE WHEN o.max_stage_num > CAST(SUBSTRING(e.stage_id, 8) AS INTEGER) THEN e.opportunity_id END) | [{"table": "lever__opportunity_stage_history", "column": "opportunity_id"}] | [{"table": "lever__opportunity_stage_history", "column": "stage_id"}, {"table": "lever__opportunity_stage_history", "column": "stage_id"}] | False |
| B4 | COUNT(DISTINCT CASE WHEN o.max_stage_num = CAST(SUBSTRING(e.stage_id, 8) AS INTEGER) AND NOT e.archive_reason IN ('Advanced to next stage', 'Qualified', 'Proceeding', 'Hired') THEN e.opportunity_id END) | [{"table": "lever__opportunity_stage_history", "column": "opportunity_id"}] | [{"table": "lever__opportunity_stage_history", "column": "stage_id"}, {"table": "lever__opportunity_stage_history", "column": "archive_reason"}, {"table": "lever__opportunity_stage_history", "column": "stage_id"}] | False |
| B4 | COUNT(DISTINCT CASE WHEN o.max_stage_num = CAST(SUBSTRING(e.stage_id, 8) AS INTEGER) AND e.archive_reason = 'Proceeding' THEN e.opportunity_id END) | [{"table": "lever__opportunity_stage_history", "column": "opportunity_id"}] | [{"table": "lever__opportunity_stage_history", "column": "stage_id"}, {"table": "lever__opportunity_stage_history", "column": "archive_reason"}, {"table": "lever__opportunity_stage_history", "column": "stage_id"}] | False |
| B4 | COUNT(DISTINCT CASE WHEN o.max_stage_num = CAST(SUBSTRING(e.stage_id, 8) AS INTEGER) AND e.archive_reason = 'Hired' THEN e.opportunity_id END) | [{"table": "lever__opportunity_stage_history", "column": "opportunity_id"}] | [{"table": "lever__opportunity_stage_history", "column": "stage_id"}, {"table": "lever__opportunity_stage_history", "column": "archive_reason"}, {"table": "lever__opportunity_stage_history", "column": "stage_id"}] | False |
| B4 | AVG(e.days_in_stage) | [{"table": "lever__opportunity_stage_history", "column": "days_in_stage"}] | [] | False |


## S18

类别 `data`；来源 `python`；调用 `d34d775ea29d48cdbe7364917152554d`；状态 `success`。

```sql

SELECT opportunity_id, stage_id, stage, archive_reason, days_in_stage
FROM lever__opportunity_stage_history

```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-071/attempt-01/sql/S18.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-071/attempt-01/sql/S18.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-071/attempt-01/results/S18.rows.jsonl)；完整：True；SHA256：`e4a4aae70f8f453db5252a05e93106ed67fe096b219d95946e2471298a449d0b`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "lever__opportunity_stage_history", "kind": "base", "block": null, "base_tables": ["lever__opportunity_stage_history"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |


## S19

类别 `data`；来源 `query_db`；调用 `b48452a0712649abbcb4ceae8cb04c27`；状态 `success`。

```sql
SELECT * FROM lever__opportunity_stage_history WHERE stage = 'Hired' LIMIT 10
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-071/attempt-01/sql/S19.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-071/attempt-01/sql/S19.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-071/attempt-01/results/S19.rows.jsonl)；完整：True；SHA256：`de5be3acbfeacc91a4968083496b8b9780905a24d85bacdef3dc406ed6344a01`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "lever__opportunity_stage_history", "kind": "base", "block": null, "base_tables": ["lever__opportunity_stage_history"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |


## S20

类别 `data`；来源 `query_db`；调用 `046d0190f74944f39f472bc39d19a28d`；状态 `success`。

```sql
SELECT stage, archive_reason, COUNT(*) as cnt FROM lever__opportunity_stage_history WHERE stage = 'Hired' GROUP BY archive_reason
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-071/attempt-01/sql/S20.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-071/attempt-01/sql/S20.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-071/attempt-01/results/S20.rows.jsonl)；完整：True；SHA256：`114ae32b97715644571ec60186b848564ab315adb434898a360c2aad84f5fc3e`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "lever__opportunity_stage_history", "kind": "base", "block": null, "base_tables": ["lever__opportunity_stage_history"]}] | [] | ["archive_reason"] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |


## S21

类别 `data`；来源 `python`；调用 `4eaf532f73e5478592aa037f3681adee`；状态 `success`。

```sql

SELECT opportunity_id, stage_id, stage, archive_reason, days_in_stage
FROM lever__opportunity_stage_history

```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-071/attempt-01/sql/S21.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-071/attempt-01/sql/S21.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-071/attempt-01/results/S21.rows.jsonl)；完整：True；SHA256：`e4a4aae70f8f453db5252a05e93106ed67fe096b219d95946e2471298a449d0b`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "lever__opportunity_stage_history", "kind": "base", "block": null, "base_tables": ["lever__opportunity_stage_history"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |


## S22

类别 `data`；来源 `python`；调用 `ea20657a0cd24395909a3a57a976eb05`；状态 `success`。

```sql

SELECT opportunity_id, stage_id, stage, archive_reason, days_in_stage
FROM lever__opportunity_stage_history

```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-071/attempt-01/sql/S22.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-071/attempt-01/sql/S22.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-071/attempt-01/results/S22.rows.jsonl)；完整：True；SHA256：`e4a4aae70f8f453db5252a05e93106ed67fe096b219d95946e2471298a449d0b`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "lever__opportunity_stage_history", "kind": "base", "block": null, "base_tables": ["lever__opportunity_stage_history"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |


## S23

类别 `data`；来源 `python`；调用 `dd87c34c15894ed5ba76e2a8a5e522d5`；状态 `success`。

```sql

SELECT opportunity_id, stage_id, stage, archive_reason, days_in_stage
FROM lever__opportunity_stage_history

```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-071/attempt-01/sql/S23.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-071/attempt-01/sql/S23.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-071/attempt-01/results/S23.rows.jsonl)；完整：True；SHA256：`e4a4aae70f8f453db5252a05e93106ed67fe096b219d95946e2471298a449d0b`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "lever__opportunity_stage_history", "kind": "base", "block": null, "base_tables": ["lever__opportunity_stage_history"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |


## S24

类别 `data`；来源 `query_db`；调用 `80a1b321e381459ea627c9d170a932a9`；状态 `success`。

```sql
SELECT current_stage, COUNT(*) as cnt FROM lever__opportunity_enhanced GROUP BY current_stage ORDER BY cnt DESC
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-071/attempt-01/sql/S24.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-071/attempt-01/sql/S24.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-071/attempt-01/results/S24.rows.jsonl)；完整：True；SHA256：`5fdf329b6df73320f58ebf02ba89afaddeb873122843b9be3bcd0cdd3721b457`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "lever__opportunity_enhanced", "kind": "base", "block": null, "base_tables": ["lever__opportunity_enhanced"]}] | [] | ["current_stage"] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |


## S25

类别 `data`；来源 `query_db`；调用 `6ad3f1ec4c284a4a92c1fe38e878871e`；状态 `success`。

```sql
SELECT archive_reason, COUNT(*) as cnt FROM lever__opportunity_enhanced GROUP BY archive_reason ORDER BY cnt DESC
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-071/attempt-01/sql/S25.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-071/attempt-01/sql/S25.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-071/attempt-01/results/S25.rows.jsonl)；完整：True；SHA256：`a1b9b57ea9c37b6058b417b53bdfd52982b3b58ce159994efa409f33b76fa0ee`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "lever__opportunity_enhanced", "kind": "base", "block": null, "base_tables": ["lever__opportunity_enhanced"]}] | [] | ["archive_reason"] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |


## S26

类别 `data`；来源 `query_db`；调用 `7277d64207f64a0bb9f87dfa6eef7cc7`；状态 `success`。

```sql
SELECT COUNT(*) as total FROM lever__opportunity_enhanced
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-071/attempt-01/sql/S26.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-071/attempt-01/sql/S26.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-071/attempt-01/results/S26.rows.jsonl)；完整：True；SHA256：`0fe9e3fb635450e627702c4f9f2499b6184ce004c9e8e92651363e971b5d7ceb`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "lever__opportunity_enhanced", "kind": "base", "block": null, "base_tables": ["lever__opportunity_enhanced"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |


## S27

类别 `data`；来源 `query_db`；调用 `b4f7d81d6e1b477a867bd5436c1e7cfc`；状态 `success`。

```sql
SELECT COUNT(DISTINCT opportunity_id) as distinct_opps FROM lever__opportunity_enhanced
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-071/attempt-01/sql/S27.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-071/attempt-01/sql/S27.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-071/attempt-01/results/S27.rows.jsonl)；完整：True；SHA256：`dff8c3b6940b56c6f7d42c9a7dd52bffb7f8a05d2f40cf73df9db0c66e956be9`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "lever__opportunity_enhanced", "kind": "base", "block": null, "base_tables": ["lever__opportunity_enhanced"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(DISTINCT opportunity_id) | [{"table": "lever__opportunity_enhanced", "column": "opportunity_id"}] | [] | False |


## S28

类别 `data`；来源 `query_db`；调用 `61a4c3b12f174658a1556d46ea5d2c5e`；状态 `success`。

```sql
SELECT stage_id, stage, MIN(days_in_stage) as min_d, MAX(days_in_stage) as max_d, ROUND(AVG(days_in_stage),2) as avg_d, COUNT(*) as n
FROM lever__opportunity_stage_history
GROUP BY stage_id, stage ORDER BY stage_id
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-071/attempt-01/sql/S28.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-071/attempt-01/sql/S28.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-071/attempt-01/results/S28.rows.jsonl)；完整：True；SHA256：`24b635d462968138f21ea70483a0d501b266354d0e29f7e92a1a58b5a8a82b37`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "lever__opportunity_stage_history", "kind": "base", "block": null, "base_tables": ["lever__opportunity_stage_history"]}] | [] | ["stage_id", "stage"] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | MIN(days_in_stage) | [{"table": "lever__opportunity_stage_history", "column": "days_in_stage"}] | [] | False |
| B1 | MAX(days_in_stage) | [{"table": "lever__opportunity_stage_history", "column": "days_in_stage"}] | [] | False |
| B1 | COUNT(*) | [] | [] | True |
| B1 | AVG(days_in_stage) | [{"table": "lever__opportunity_stage_history", "column": "days_in_stage"}] | [] | False |


## S29

类别 `data`；来源 `python`；调用 `8d6e28aab2b844bcb38afa593b5a1217`；状态 `success`。

```sql

SELECT opportunity_id, stage_id, stage, archive_reason, days_in_stage
FROM lever__opportunity_stage_history

```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-071/attempt-01/sql/S29.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-071/attempt-01/sql/S29.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-071/attempt-01/results/S29.rows.jsonl)；完整：True；SHA256：`e4a4aae70f8f453db5252a05e93106ed67fe096b219d95946e2471298a449d0b`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "lever__opportunity_stage_history", "kind": "base", "block": null, "base_tables": ["lever__opportunity_stage_history"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |


## S30

类别 `data`；来源 `python`；调用 `2504c0c866df44fea45b0b2c7ed1d8c3`；状态 `success`。

```sql

SELECT opportunity_id, stage_id, stage, archive_reason, days_in_stage
FROM lever__opportunity_stage_history

```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-071/attempt-01/sql/S30.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-071/attempt-01/sql/S30.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-071/attempt-01/results/S30.rows.jsonl)；完整：True；SHA256：`e4a4aae70f8f453db5252a05e93106ed67fe096b219d95946e2471298a449d0b`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "lever__opportunity_stage_history", "kind": "base", "block": null, "base_tables": ["lever__opportunity_stage_history"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |


## S31

类别 `data`；来源 `query_db`；调用 `ab9431963b424916a01d11b8df10939a`；状态 `success`。

```sql
SELECT stage, archive_reason, COUNT(*) as cnt
FROM lever__opportunity_stage_history
WHERE stage IN ('Technical Assessment','Final Interview')
GROUP BY stage, archive_reason
ORDER BY stage, cnt DESC
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-071/attempt-01/sql/S31.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-071/attempt-01/sql/S31.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-071/attempt-01/results/S31.rows.jsonl)；完整：True；SHA256：`112370dcc4b89aca97e9122e8215b7e16a5c35a33ba621fe0960b9a3c7711300`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "lever__opportunity_stage_history", "kind": "base", "block": null, "base_tables": ["lever__opportunity_stage_history"]}] | [] | ["stage", "archive_reason"] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |


## S32

类别 `data`；来源 `query_db`；调用 `5b72665b7ed945dda0a2c247bdd49ec2`；状态 `success`。

```sql
SELECT stage, job_team, COUNT(*) as cnt, ROUND(AVG(days_in_stage),1) as avg_days
FROM lever__opportunity_stage_history
WHERE stage IN ('Technical Assessment','Final Interview')
GROUP BY stage, job_team
ORDER BY stage, cnt DESC
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-071/attempt-01/sql/S32.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-071/attempt-01/sql/S32.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-071/attempt-01/results/S32.rows.jsonl)；完整：True；SHA256：`b98a89e7500ae8954d84c4bf96f882842f4b9d23339afd2d5c934a28f3ce801c`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "lever__opportunity_stage_history", "kind": "base", "block": null, "base_tables": ["lever__opportunity_stage_history"]}] | [] | ["stage", "job_team"] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |
| B1 | AVG(days_in_stage) | [{"table": "lever__opportunity_stage_history", "column": "days_in_stage"}] | [] | False |


## S33

类别 `data`；来源 `python`；调用 `bfd3c9fe904a4938b731a56cad7edefa`；状态 `success`。

```sql

SELECT opportunity_id, stage_id, stage, archive_reason, days_in_stage
FROM lever__opportunity_stage_history

```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-071/attempt-01/sql/S33.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-071/attempt-01/sql/S33.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-071/attempt-01/results/S33.rows.jsonl)；完整：True；SHA256：`e4a4aae70f8f453db5252a05e93106ed67fe096b219d95946e2471298a449d0b`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "lever__opportunity_stage_history", "kind": "base", "block": null, "base_tables": ["lever__opportunity_stage_history"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |


## S34

类别 `data`；来源 `python`；调用 `f873948580c541ad9973edf1cf583651`；状态 `success`。

```sql

SELECT opportunity_id, stage_id, stage, archive_reason, days_in_stage
FROM lever__opportunity_stage_history

```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-071/attempt-01/sql/S34.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-071/attempt-01/sql/S34.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-071/attempt-01/results/S34.rows.jsonl)；完整：True；SHA256：`e4a4aae70f8f453db5252a05e93106ed67fe096b219d95946e2471298a449d0b`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "lever__opportunity_stage_history", "kind": "base", "block": null, "base_tables": ["lever__opportunity_stage_history"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |


## S35

类别 `data`；来源 `python`；调用 `e6c62e9affeb41919f2f9cad576fda0a`；状态 `success`。

```sql

SELECT opportunity_id, stage_id, stage, archive_reason, days_in_stage, job_team, job_title, application_sources
FROM lever__opportunity_stage_history
WHERE stage IN ('Technical Assessment', 'Final Interview')

```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-071/attempt-01/sql/S35.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-071/attempt-01/sql/S35.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-071/attempt-01/results/S35.rows.jsonl)；完整：True；SHA256：`4a266bd53b00f325ac1a97b1755080222a3c426bd27cc3bc21ba0caccfbac8f6`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "lever__opportunity_stage_history", "kind": "base", "block": null, "base_tables": ["lever__opportunity_stage_history"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |


## S36

类别 `data`；来源 `python`；调用 `971de71ffbe9411f9d49a96812cde4f5`；状态 `success`。

```sql

SELECT opportunity_id, stage_id, stage, archive_reason, days_in_stage, job_team, job_title, application_sources
FROM lever__opportunity_stage_history

```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-071/attempt-01/sql/S36.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-071/attempt-01/sql/S36.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-071/attempt-01/results/S36.rows.jsonl)；完整：True；SHA256：`7bd9df5f1bb104532c5ee4972adcff390543413682d7f49e44a7ef2f2d18bec1`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "lever__opportunity_stage_history", "kind": "base", "block": null, "base_tables": ["lever__opportunity_stage_history"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |


## S37

类别 `data`；来源 `python`；调用 `36fecbd96ae140aab1eb4c421f424352`；状态 `success`。

```sql

SELECT opportunity_id, stage_id, stage, archive_reason, days_in_stage
FROM lever__opportunity_stage_history

```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-071/attempt-01/sql/S37.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-071/attempt-01/sql/S37.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-071/attempt-01/results/S37.rows.jsonl)；完整：True；SHA256：`e4a4aae70f8f453db5252a05e93106ed67fe096b219d95946e2471298a449d0b`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "lever__opportunity_stage_history", "kind": "base", "block": null, "base_tables": ["lever__opportunity_stage_history"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |


## S38

类别 `data`；来源 `python`；调用 `03a56917e3e04df9a75cbe13474f9dba`；状态 `success`。

```sql

SELECT opportunity_id, stage_id, stage, archive_reason, days_in_stage, job_team, application_sources
FROM lever__opportunity_stage_history

```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-071/attempt-01/sql/S38.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-071/attempt-01/sql/S38.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-071/attempt-01/results/S38.rows.jsonl)；完整：True；SHA256：`2ba5ded052fac4d8ea24d589f12b8a0c1929685c69d68d7fba700eafe7823e03`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "lever__opportunity_stage_history", "kind": "base", "block": null, "base_tables": ["lever__opportunity_stage_history"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |

