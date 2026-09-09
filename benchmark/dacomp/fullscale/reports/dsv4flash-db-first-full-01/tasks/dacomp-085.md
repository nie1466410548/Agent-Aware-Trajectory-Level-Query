# dacomp-085

In light of business adjustments, we need to re-evaluate the true value of each job profil…

运行：已提交。官方未评分。全部 SQL 尝试/成功 17/17；数据 SQL 15/15；Python 11 次。

完整原题：

In light of business adjustments, we need to re-evaluate the true value of each job profile and the rationality of talent allocation. Please start with job profiles where job_value_tier is "Tier 1" or "Tier 2", and calculate the talent allocation saturation (current_employees_count/active_positions_count) and the talent quality index (high_performer_percentage * career_growth_potential_percentage) for each job profile. Then, for cases where talent_competition_level is "High" or "Very High", analyze which job profiles exhibit a mismatch between their actual output (measured by job_health_score and avg_career_development_score) and their market competition level. Further explore the differential patterns of these job profiles in terms of work characteristics such as avg_weekly_hours, is_work_shift_required, and retention_difficulty_level, and identify those job profiles with an imbalanced 'input-to-output ratio'. Finally, deliver a job value re-evaluation report that includes a specific list of job profiles recommended for optimization, suggestions for personnel redeployment, and a priority ranking for resource reallocation.

| 表 | 行数 | 列数 |
| --- | --- | --- |
| workday__employee_overview | 156205 | 79 |
| workday__job_overview | 900 | 60 |
| workday__organization_overview | 118 | 64 |


实际路线（分析者依据 SQL/源码概括，不代表 Agent 自述）：SQL 提取高价值高竞争岗位指标 → Python 评分、错配判定与分组统计 → 岗位优化优先级。

数据库大小：92,041,216 字节。

## 数据 SQL

| SQL | 状态 | 基础表 | Join 输入/类型 | GROUP BY | 聚合表达式 | 结果行数 | 数据库 ms |
| --- | --- | --- | --- | --- | --- | --- | --- |
| [S3/Q1](#s3) | success | ["workday__job_overview"] | 0 / {} | [] | ["COUNT(*)"] | 1 | 0.541 |
| [S4/Q2](#s4) | success | ["workday__job_overview"] | 0 / {} | ["job_value_tier"] | ["COUNT(*)"] | 2 | 0.721 |
| [S5/Q3](#s5) | success | ["workday__job_overview"] | 0 / {} | ["talent_competition_level"] | ["COUNT(*)"] | 3 | 0.733 |
| [S6/Q4](#s6) | success | ["workday__job_overview"] | 0 / {} | [] | [] | 4 | 0.726 |
| [S7/Q5](#s7) | success | ["workday__job_overview"] | 0 / {} | [] | ["COUNT(*)", "SUM(CASE WHEN active_positions_count IS NULL OR active_positions_count = 0 THEN 1 ELSE 0 END)", "SUM(CASE WHEN current_employees_count IS NULL THEN 1 ELSE 0 END)", "SUM(CASE WHEN high_performer_percentage IS NULL THEN 1 ELSE 0 END)", "SUM(CASE WHEN career_growth_potential_percentage IS NULL THEN 1 ELSE 0 END)", "SUM(CASE WHEN job_health_score IS NULL THEN 1 ELSE 0 END)", "SUM(CASE WHEN avg_career_development_score IS NULL THEN 1 ELSE 0 END)", "MIN(active_positions_count)", "MAX(active_positions_count)"] | 1 | 0.996 |
| [S8/Q6](#s8) | success | ["workday__job_overview"] | 0 / {} | ["job_value_tier", "talent_competition_level"] | ["COUNT(*)"] | 4 | 0.917 |
| [S9/Q7](#s9) | success | ["workday__job_overview"] | 0 / {} | [] | ["MIN(high_performer_percentage)", "MAX(high_performer_percentage)", "AVG(high_performer_percentage)", "MIN(career_growth_potential_percentage)", "MAX(career_growth_potential_percentage)", "AVG(career_growth_potential_percentage)", "MIN(job_health_score)", "MAX(job_health_score)", "AVG(job_health_score)", "MIN(avg_career_development_score)", "MAX(avg_career_development_score)", "AVG(avg_career_development_score)", "MIN(current_employees_count)", "MAX(current_employees_count)", "MIN(avg_weekly_hours)", "MAX(avg_weekly_hours)"] | 1 | 1.085 |
| [S10/Q8](#s10) | success | ["workday__job_overview"] | 0 / {} | ["job_value_tier"] | ["AVG(job_health_score)", "AVG(avg_career_development_score)", "AVG(high_performer_percentage)", "AVG(career_growth_potential_percentage)", "AVG(current_employees_count * 1.0 / active_positions_count)"] | 2 | 1.041 |
| [S11/Q9](#s11) | success | ["workday__job_overview"] | 0 / {} | [] | [] | 20 | 1.169 |
| [S12/Q10](#s12) | success | ["workday__job_overview"] | 0 / {} | ["talent_competition_level"] | ["COUNT(*)", "AVG(talent_saturation)", "AVG(talent_quality_index)", "AVG(job_health_score)", "AVG(avg_career_development_score)", "AVG(avg_weekly_hours)"] | 2 | 1.56 |
| [S13/Q11](#s13) | success | ["workday__job_overview"] | 0 / {} | [] | ["MIN(job_health_score)", "MAX(job_health_score)", "MIN(avg_career_development_score)", "MAX(avg_career_development_score)", "AVG(job_health_score)", "AVG(avg_career_development_score)", "AVG(talent_saturation)", "AVG(talent_quality_index)"] | 1 | 1.345 |
| [S14/Q12](#s14) | success | ["workday__job_overview"] | 0 / {} | [] | ["MIN(job_health_score)", "AVG(CASE WHEN rn_h <= cnt * 0.25 THEN job_health_score END)", "AVG(CASE WHEN rn_h <= cnt * 0.50 THEN job_health_score END)", "AVG(CASE WHEN rn_h <= cnt * 0.75 THEN job_health_score END)", "MAX(job_health_score)", "MIN(avg_career_development_score)", "AVG(CASE WHEN rn_d <= cnt * 0.25 THEN avg_career_development_score END)", "AVG(CASE WHEN rn_d <= cnt * 0.50 THEN avg_career_development_score END)", "AVG(CASE WHEN rn_d <= cnt * 0.75 THEN avg_career_development_score END)", "MAX(avg_career_development_score)"] | 2 | 3.554 |
| [S15/Q13](#s15) | success | ["workday__job_overview"] | 0 / {} | [] | [] | 660 | 3.337 |
| [S16/Q14](#s16) | success | ["workday__job_overview"] | 0 / {} | [] | [] | 30 | 1.32 |
| [S17/Q15](#s17) | success | ["workday__job_overview"] | 0 / {} | ["retention_difficulty_level"] | ["COUNT(*)", "AVG(job_health_score)", "AVG(avg_career_development_score)", "AVG(high_performer_percentage * career_growth_potential_percentage)", "AVG(current_employees_count * 1.0 / active_positions_count)", "AVG(avg_weekly_hours)", "COUNT(*)", "SUM(is_work_shift_required)"] | 3 | 1.331 |


## 元数据和设置

| SQL | 类别 | 状态 | 内容 |
| --- | --- | --- | --- |
| S1 | connection_setup | success | PRAGMA query_only=ON |
| S2 | metadata | success | SELECT name,sql FROM sqlite_master WHERE type='table' ORDER BY name |


## Python 与执行位置

人工源码审查：**database_first_violation**。Python 构造常规投入产出评分、最小最大归一化和比率，计算错配组均值、轮班及层级条件计数。这些 SQL 可支持的算术和聚合迁出数据库。分位数、t/卡方检验与图形渲染另行保留。 [证据](../reviews/dacomp-085.json)。

P1：Compute percentiles and composite output/input indices for the 660 High/Very High competition profiles. SQLite lacks percentile and normalized composite-index functions; this is statistical analysis best done in Python.

[源码](../../../runs/dsv4flash-db-first-full-01/dacomp-085/attempt-01/python/P1.py)；[输出](../../../runs/dsv4flash-db-first-full-01/dacomp-085/attempt-01/python/P1.stdout)；[错误](../../../runs/dsv4flash-db-first-full-01/dacomp-085/attempt-01/python/P1.stderr)。自动源码筛查未检出预设迁出信号；这不是全面语义合规证明。

P2：Inspect the archive file format for the S15 result so the data can be loaded correctly for percentile/composite-index analysis.

[源码](../../../runs/dsv4flash-db-first-full-01/dacomp-085/attempt-01/python/P2.py)；[输出](../../../runs/dsv4flash-db-first-full-01/dacomp-085/attempt-01/python/P2.stdout)；[错误](../../../runs/dsv4flash-db-first-full-01/dacomp-085/attempt-01/python/P2.stderr)。自动源码筛查未检出预设迁出信号；这不是全面语义合规证明。

P3：Loading the JSONL file line by line, each line is a JSON array. This is needed to get the data into a usable DataFrame.

[源码](../../../runs/dsv4flash-db-first-full-01/dacomp-085/attempt-01/python/P3.py)；[输出](../../../runs/dsv4flash-db-first-full-01/dacomp-085/attempt-01/python/P3.stdout)；[错误](../../../runs/dsv4flash-db-first-full-01/dacomp-085/attempt-01/python/P3.stderr)。自动源码筛查未检出预设迁出信号；这不是全面语义合规证明。

P4：Compute percentiles, composite output/input indices, define mismatch and imbalanced input-to-output ratio thresholds. SQLite lacks percentile, normalization, and composite-index functions; this is statistical analysis.

[源码](../../../runs/dsv4flash-db-first-full-01/dacomp-085/attempt-01/python/P4.py)；[输出](../../../runs/dsv4flash-db-first-full-01/dacomp-085/attempt-01/python/P4.stdout)；[错误](../../../runs/dsv4flash-db-first-full-01/dacomp-085/attempt-01/python/P4.stderr)。自动源码筛查未检出预设迁出信号；这不是全面语义合规证明。

P5：Analyze differential patterns of work characteristics (retention difficulty, shift requirement, weekly hours) between mismatch and non-mismatch groups. Cross-tabulation and descriptive statistics are better in Python than SQL.

[源码](../../../runs/dsv4flash-db-first-full-01/dacomp-085/attempt-01/python/P5.py)；[输出](../../../runs/dsv4flash-db-first-full-01/dacomp-085/attempt-01/python/P5.stdout)；[错误](../../../runs/dsv4flash-db-first-full-01/dacomp-085/attempt-01/python/P5.stderr)。自动源码筛查未检出预设迁出信号；这不是全面语义合规证明。

P6：Create visualizations and extract the final list of critical profiles. Matplotlib is needed for figures; the composite index computation and threshold-based filtering are also statistical procedures not supported by SQLite.

[源码](../../../runs/dsv4flash-db-first-full-01/dacomp-085/attempt-01/python/P6.py)；[输出](../../../runs/dsv4flash-db-first-full-01/dacomp-085/attempt-01/python/P6.stdout)；[错误](../../../runs/dsv4flash-db-first-full-01/dacomp-085/attempt-01/python/P6.stderr)。检出需人工核验的 SQL 可实现操作：sort_values(；不能仅凭理由判为合规。

P7：Run statistical tests (t-test, chi-square) and correlations on the mismatch groups, and build a weighted priority ranking for resource reallocation. These are statistical procedures requiring scipy, not supported by SQLite.

[源码](../../../runs/dsv4flash-db-first-full-01/dacomp-085/attempt-01/python/P7.py)；[输出](../../../runs/dsv4flash-db-first-full-01/dacomp-085/attempt-01/python/P7.stdout)；[错误](../../../runs/dsv4flash-db-first-full-01/dacomp-085/attempt-01/python/P7.stderr)。检出需人工核验的 SQL 可实现操作：sort_values(；不能仅凭理由判为合规。

P8：Generate summary statistics for the report. This is post-analysis summarization using Python for formatting.

[源码](../../../runs/dsv4flash-db-first-full-01/dacomp-085/attempt-01/python/P8.py)；[输出](../../../runs/dsv4flash-db-first-full-01/dacomp-085/attempt-01/python/P8.stdout)；[错误](../../../runs/dsv4flash-db-first-full-01/dacomp-085/attempt-01/python/P8.stderr)。自动源码筛查未检出预设迁出信号；这不是全面语义合规证明。

P9：Print the full ranked list of 79 critical profiles for inclusion in the report appendix.

[源码](../../../runs/dsv4flash-db-first-full-01/dacomp-085/attempt-01/python/P9.py)；[输出](../../../runs/dsv4flash-db-first-full-01/dacomp-085/attempt-01/python/P9.stdout)；[错误](../../../runs/dsv4flash-db-first-full-01/dacomp-085/attempt-01/python/P9.stderr)。检出需人工核验的 SQL 可实现操作：sort_values(；不能仅凭理由判为合规。

P10：Print the tail end of the ranked critical profiles list that was truncated in the previous output.

[源码](../../../runs/dsv4flash-db-first-full-01/dacomp-085/attempt-01/python/P10.py)；[输出](../../../runs/dsv4flash-db-first-full-01/dacomp-085/attempt-01/python/P10.stdout)；[错误](../../../runs/dsv4flash-db-first-full-01/dacomp-085/attempt-01/python/P10.stderr)。检出需人工核验的 SQL 可实现操作：sort_values(；不能仅凭理由判为合规。

P11：Summarize key characteristics of the 79 critical profiles for the report's recommendations section.

[源码](../../../runs/dsv4flash-db-first-full-01/dacomp-085/attempt-01/python/P11.py)；[输出](../../../runs/dsv4flash-db-first-full-01/dacomp-085/attempt-01/python/P11.stdout)；[错误](../../../runs/dsv4flash-db-first-full-01/dacomp-085/attempt-01/python/P11.stderr)。自动源码筛查未检出预设迁出信号；这不是全面语义合规证明。

## 优化机会

已验证候选。筛选限于精确 SQL、相同自包含 CTE、相同单表完整过滤、可分解单表聚合；未覆盖任意 Join 等价和一般谓词蕴含。全部候选都是 offline，未测在线预测。

| 候选 | 类型 | 已有结果 | 覆盖 SQL | 后续次数 | 中间行数 | 验证 | 成本 |
| --- | --- | --- | --- | --- | --- | --- | --- |
| C1 | common subexpression | False | ["S13", "S15"] | 1 | 660 | verified | Not benchmarked; correctness alone does not establish net speedup. |
| C2 | aggregate MV | False | ["S3", "S4", "S5", "S7", "S8", "S9", "S10"] | 6 | 4 | rejected_result_mismatch | Not benchmarked; correctness alone does not establish net speedup. |


已验证覆盖（含触发查询、候选并集去重）：2/15 条成功数据 SQL。正确性仅针对当前数据库快照；未测性能的候选不能声称已加速。

[完整 build/rewrite 与比较证据](dacomp-085.analysis.json)。

### C1：common subexpression

Identical self-contained CTE body across queries.

原查询 [S13](#s13), [S15](#s15) → 新增共享状态 C1 → 后续 1 次可复用。该构建点为事后假设，不代表 Agent 当时预知后续。

构建定义：

```sql
SELECT job_profile_id, job_title, job_value_tier, talent_competition_level, job_health_score, avg_career_development_score, retention_difficulty_level, is_work_shift_required, avg_weekly_hours, current_employees_count, active_positions_count, ROUND(current_employees_count * 1.0 / active_positions_count, 4) AS talent_saturation, ROUND(high_performer_percentage * career_growth_potential_percentage, 6) AS talent_quality_index FROM workday__job_overview WHERE job_value_tier IN ('Tier 1', 'Tier 2') AND talent_competition_level IN ('High', 'Very High')
```

受益查询 S13 的改写示例：

```sql
WITH subset AS (SELECT * FROM temp.reuse_candidate) SELECT ROUND(AVG(job_health_score), 2) AS mean_health, MIN(job_health_score) AS min_health, MAX(job_health_score) AS max_health, ROUND(AVG(avg_career_development_score), 2) AS mean_dev, MIN(avg_career_development_score) AS min_dev, MAX(avg_career_development_score) AS max_dev, ROUND(AVG(talent_saturation), 3) AS mean_sat, ROUND(AVG(talent_quality_index), 5) AS mean_quality FROM subset
```

| 原 SQL | 列名一致 | 结果一致 | 比较方法 |
| --- | --- | --- | --- |
| S13 | True | True | exact_multiset |
| S15 | True | True | ordered_numeric_tolerance |


验证状态：verified；成本结论：Not benchmarked; correctness alone does not establish net speedup.

### C2：aggregate MV

Union of grouping keys; decomposable aggregate states; AVG uses SUM and non-NULL COUNT.

原查询 [S3](#s3), [S4](#s4), [S5](#s5), [S7](#s7), [S8](#s8), [S9](#s9), [S10](#s10) → 新增共享状态 C2 → 后续 6 次可复用。该构建点为事后假设，不代表 Agent 当时预知后续。

构建定义：

```sql
SELECT job_value_tier AS __g0, talent_competition_level AS __g1, COUNT(*) AS __a0, SUM(CASE WHEN active_positions_count IS NULL OR active_positions_count = 0 THEN 1 ELSE 0 END) AS __a1, SUM(CASE WHEN current_employees_count IS NULL THEN 1 ELSE 0 END) AS __a2, SUM(CASE WHEN high_performer_percentage IS NULL THEN 1 ELSE 0 END) AS __a3, SUM(CASE WHEN career_growth_potential_percentage IS NULL THEN 1 ELSE 0 END) AS __a4, SUM(CASE WHEN job_health_score IS NULL THEN 1 ELSE 0 END) AS __a5, SUM(CASE WHEN avg_career_development_score IS NULL THEN 1 ELSE 0 END) AS __a6, MIN(active_positions_count) AS __a7, MAX(active_positions_count) AS __a8, MIN(high_performer_percentage) AS __a9, MAX(high_performer_percentage) AS __a10, SUM(high_performer_percentage) AS __a11_sum, COUNT(high_performer_percentage) AS __a11_n, MIN(career_growth_potential_percentage) AS __a12, MAX(career_growth_potential_percentage) AS __a13, SUM(career_growth_potential_percentage) AS __a14_sum, COUNT(career_growth_potential_percentage) AS __a14_n, MIN(job_health_score) AS __a15, MAX(job_health_score) AS __a16, SUM(job_health_score) AS __a17_sum, COUNT(job_health_score) AS __a17_n, MIN(avg_career_development_score) AS __a18, MAX(avg_career_development_score) AS __a19, SUM(avg_career_development_score) AS __a20_sum, COUNT(avg_career_development_score) AS __a20_n, MIN(current_employees_count) AS __a21, MAX(current_employees_count) AS __a22, MIN(avg_weekly_hours) AS __a23, MAX(avg_weekly_hours) AS __a24, SUM(current_employees_count * 1.0 / active_positions_count) AS __a25_sum, COUNT(current_employees_count * 1.0 / active_positions_count) AS __a25_n FROM "workday__job_overview"  GROUP BY job_value_tier, talent_competition_level
```

受益查询 S3 的改写示例：

```sql
SELECT SUM(__a0) AS total_rows FROM temp.reuse_candidate
```

| 原 SQL | 列名一致 | 结果一致 | 比较方法 |
| --- | --- | --- | --- |
| S3 | True | True | exact_multiset |
| S4 | True | True | ordered_numeric_tolerance |
| S5 | True | True | ordered_numeric_tolerance |
| S7 | True | True | exact_multiset |
| S8 | True | True | ordered_numeric_tolerance |
| S9 | True | False | exact_multiset |
| S10 | True | False | exact_multiset |


验证状态：rejected_result_mismatch；成本结论：Not benchmarked; correctness alone does not establish net speedup.

结果依赖：自动记录 SQL→Python 的接口父调用，以及源码中引用归档文件的消费者；字面值相同不认定因果。模型方向选择需要人工读取消息，尚未做全面因果标注。

[原始报告](../../../runs/dsv4flash-db-first-full-01/dacomp-085/attempt-01/answer.md)；[统一消息](../../../runs/dsv4flash-db-first-full-01/dacomp-085/attempt-01/messages.jsonl)；[原始 OpenCode 事件](../../../runs/dsv4flash-db-first-full-01/dacomp-085/attempt-01/opencode.jsonl)；[SQL 引擎日志](../../../runs/dsv4flash-db-first-full-01/dacomp-085/attempt-01/sql_journal.jsonl)。

[可读报告（本地图片链接规范化）](../answers/dacomp-085.md)。原始回答保留，分析结论未改写。

## S1

类别 `connection_setup`；来源 `connection`；调用 `dd3877e1e93e4730970abdef3e4d035f`；状态 `success`。

```sql
PRAGMA query_only=ON
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-085/attempt-01/sql/S1.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-085/attempt-01/sql/S1.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-085/attempt-01/results/S1.rows.jsonl)；完整：True；SHA256：`e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`。

## S2

类别 `metadata`；来源 `list_db`；调用 `dd3877e1e93e4730970abdef3e4d035f`；状态 `success`。

```sql
SELECT name,sql FROM sqlite_master WHERE type='table' ORDER BY name
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-085/attempt-01/sql/S2.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-085/attempt-01/sql/S2.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-085/attempt-01/results/S2.rows.jsonl)；完整：True；SHA256：`c7a20b97ae48f5c8a99d5709f65e08fb664bf753899525690bcbbd3c4f4b90fc`。

## S3

类别 `data`；来源 `query_db`；调用 `991bf74c39674c76bafce591040416c3`；状态 `success`。

```sql
SELECT COUNT(*) AS total_rows FROM workday__job_overview
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-085/attempt-01/sql/S3.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-085/attempt-01/sql/S3.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-085/attempt-01/results/S3.rows.jsonl)；完整：True；SHA256：`0a963191ffa2ed76b286c1b368b970fe82d31f635a223daa0846ab8c2484f109`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "workday__job_overview", "kind": "base", "block": null, "base_tables": ["workday__job_overview"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |


## S4

类别 `data`；来源 `query_db`；调用 `1a0bbc2b962c48f59e83d373f1c0efcf`；状态 `success`。

```sql
SELECT job_value_tier, COUNT(*) AS cnt FROM workday__job_overview GROUP BY job_value_tier ORDER BY cnt DESC
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-085/attempt-01/sql/S4.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-085/attempt-01/sql/S4.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-085/attempt-01/results/S4.rows.jsonl)；完整：True；SHA256：`d98537471b1f147788498255290f4cd0e01cd463f4e72ccd10c33a9eb96df141`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "workday__job_overview", "kind": "base", "block": null, "base_tables": ["workday__job_overview"]}] | [] | ["job_value_tier"] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |


## S5

类别 `data`；来源 `query_db`；调用 `f3a4504957de485aa8eb7035ad11a8e4`；状态 `success`。

```sql
SELECT talent_competition_level, COUNT(*) AS cnt FROM workday__job_overview GROUP BY talent_competition_level ORDER BY cnt DESC
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-085/attempt-01/sql/S5.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-085/attempt-01/sql/S5.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-085/attempt-01/results/S5.rows.jsonl)；完整：True；SHA256：`1a27103de76435f47c3726cd872079e5934eb7481e906367438876a471a148b4`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "workday__job_overview", "kind": "base", "block": null, "base_tables": ["workday__job_overview"]}] | [] | ["talent_competition_level"] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |


## S6

类别 `data`；来源 `query_db`；调用 `9f1c5be241b941b2917115304185dc9c`；状态 `success`。

```sql
SELECT DISTINCT retention_difficulty_level FROM workday__job_overview
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-085/attempt-01/sql/S6.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-085/attempt-01/sql/S6.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-085/attempt-01/results/S6.rows.jsonl)；完整：True；SHA256：`4c4c0716b60f9c12f421c541675b018dae97006c94cb7b1b03cfb45aaa65dd3b`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "workday__job_overview", "kind": "base", "block": null, "base_tables": ["workday__job_overview"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |


## S7

类别 `data`；来源 `query_db`；调用 `41239cc75071492c8da854f8adb4cf82`；状态 `success`。

```sql
SELECT 
  COUNT(*) AS total,
  SUM(CASE WHEN active_positions_count IS NULL OR active_positions_count = 0 THEN 1 ELSE 0 END) AS zero_active_pos,
  SUM(CASE WHEN current_employees_count IS NULL THEN 1 ELSE 0 END) AS null_curr_emp,
  SUM(CASE WHEN high_performer_percentage IS NULL THEN 1 ELSE 0 END) AS null_hp,
  SUM(CASE WHEN career_growth_potential_percentage IS NULL THEN 1 ELSE 0 END) AS null_cgp,
  SUM(CASE WHEN job_health_score IS NULL THEN 1 ELSE 0 END) AS null_jhs,
  SUM(CASE WHEN avg_career_development_score IS NULL THEN 1 ELSE 0 END) AS null_ads,
  MIN(active_positions_count) AS min_active,
  MAX(active_positions_count) AS max_active
FROM workday__job_overview
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-085/attempt-01/sql/S7.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-085/attempt-01/sql/S7.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-085/attempt-01/results/S7.rows.jsonl)；完整：True；SHA256：`c4d02acf395bdd3b78a343c0dfb01dee31161cf2b5b172c5d113b6691156e614`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "workday__job_overview", "kind": "base", "block": null, "base_tables": ["workday__job_overview"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |
| B1 | SUM(CASE WHEN active_positions_count IS NULL OR active_positions_count = 0 THEN 1 ELSE 0 END) | [] | [{"table": "workday__job_overview", "column": "active_positions_count"}, {"table": "workday__job_overview", "column": "active_positions_count"}] | False |
| B1 | SUM(CASE WHEN current_employees_count IS NULL THEN 1 ELSE 0 END) | [] | [{"table": "workday__job_overview", "column": "current_employees_count"}] | False |
| B1 | SUM(CASE WHEN high_performer_percentage IS NULL THEN 1 ELSE 0 END) | [] | [{"table": "workday__job_overview", "column": "high_performer_percentage"}] | False |
| B1 | SUM(CASE WHEN career_growth_potential_percentage IS NULL THEN 1 ELSE 0 END) | [] | [{"table": "workday__job_overview", "column": "career_growth_potential_percentage"}] | False |
| B1 | SUM(CASE WHEN job_health_score IS NULL THEN 1 ELSE 0 END) | [] | [{"table": "workday__job_overview", "column": "job_health_score"}] | False |
| B1 | SUM(CASE WHEN avg_career_development_score IS NULL THEN 1 ELSE 0 END) | [] | [{"table": "workday__job_overview", "column": "avg_career_development_score"}] | False |
| B1 | MIN(active_positions_count) | [{"table": "workday__job_overview", "column": "active_positions_count"}] | [] | False |
| B1 | MAX(active_positions_count) | [{"table": "workday__job_overview", "column": "active_positions_count"}] | [] | False |


## S8

类别 `data`；来源 `query_db`；调用 `567d0efaab8b4045994cfcafe08334de`；状态 `success`。

```sql
SELECT job_value_tier, talent_competition_level, COUNT(*) AS cnt
FROM workday__job_overview
GROUP BY job_value_tier, talent_competition_level
ORDER BY job_value_tier, cnt DESC
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-085/attempt-01/sql/S8.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-085/attempt-01/sql/S8.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-085/attempt-01/results/S8.rows.jsonl)；完整：True；SHA256：`e84b5a0e4dcbc68d5e759f79915c85b862e518c666f548b0221dad03dd71efc5`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "workday__job_overview", "kind": "base", "block": null, "base_tables": ["workday__job_overview"]}] | [] | ["job_value_tier", "talent_competition_level"] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |


## S9

类别 `data`；来源 `query_db`；调用 `71f79e29cdcd41d089136209b1745c70`；状态 `success`。

```sql
SELECT
  MIN(high_performer_percentage) AS min_hp, MAX(high_performer_percentage) AS max_hp, AVG(high_performer_percentage) AS avg_hp,
  MIN(career_growth_potential_percentage) AS min_cgp, MAX(career_growth_potential_percentage) AS max_cgp, AVG(career_growth_potential_percentage) AS avg_cgp,
  MIN(job_health_score) AS min_jhs, MAX(job_health_score) AS max_jhs, AVG(job_health_score) AS avg_jhs,
  MIN(avg_career_development_score) AS min_ads, MAX(avg_career_development_score) AS max_ads, AVG(avg_career_development_score) AS avg_ads,
  MIN(current_employees_count) AS min_ce, MAX(current_employees_count) AS max_ce,
  MIN(avg_weekly_hours) AS min_wk, MAX(avg_weekly_hours) AS max_wk
FROM workday__job_overview
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-085/attempt-01/sql/S9.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-085/attempt-01/sql/S9.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-085/attempt-01/results/S9.rows.jsonl)；完整：True；SHA256：`a8b5d981e400719b295a3e1ed4b04ac2a92784d729350718152cf83288eaeb9c`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "workday__job_overview", "kind": "base", "block": null, "base_tables": ["workday__job_overview"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | MIN(high_performer_percentage) | [{"table": "workday__job_overview", "column": "high_performer_percentage"}] | [] | False |
| B1 | MAX(high_performer_percentage) | [{"table": "workday__job_overview", "column": "high_performer_percentage"}] | [] | False |
| B1 | AVG(high_performer_percentage) | [{"table": "workday__job_overview", "column": "high_performer_percentage"}] | [] | False |
| B1 | MIN(career_growth_potential_percentage) | [{"table": "workday__job_overview", "column": "career_growth_potential_percentage"}] | [] | False |
| B1 | MAX(career_growth_potential_percentage) | [{"table": "workday__job_overview", "column": "career_growth_potential_percentage"}] | [] | False |
| B1 | AVG(career_growth_potential_percentage) | [{"table": "workday__job_overview", "column": "career_growth_potential_percentage"}] | [] | False |
| B1 | MIN(job_health_score) | [{"table": "workday__job_overview", "column": "job_health_score"}] | [] | False |
| B1 | MAX(job_health_score) | [{"table": "workday__job_overview", "column": "job_health_score"}] | [] | False |
| B1 | AVG(job_health_score) | [{"table": "workday__job_overview", "column": "job_health_score"}] | [] | False |
| B1 | MIN(avg_career_development_score) | [{"table": "workday__job_overview", "column": "avg_career_development_score"}] | [] | False |
| B1 | MAX(avg_career_development_score) | [{"table": "workday__job_overview", "column": "avg_career_development_score"}] | [] | False |
| B1 | AVG(avg_career_development_score) | [{"table": "workday__job_overview", "column": "avg_career_development_score"}] | [] | False |
| B1 | MIN(current_employees_count) | [{"table": "workday__job_overview", "column": "current_employees_count"}] | [] | False |
| B1 | MAX(current_employees_count) | [{"table": "workday__job_overview", "column": "current_employees_count"}] | [] | False |
| B1 | MIN(avg_weekly_hours) | [{"table": "workday__job_overview", "column": "avg_weekly_hours"}] | [] | False |
| B1 | MAX(avg_weekly_hours) | [{"table": "workday__job_overview", "column": "avg_weekly_hours"}] | [] | False |


## S10

类别 `data`；来源 `query_db`；调用 `d57d20a0869146d98e9587fc6a466265`；状态 `success`。

```sql
SELECT job_value_tier, 
  AVG(job_health_score) AS avg_health, AVG(avg_career_development_score) AS avg_dev,
  AVG(high_performer_percentage) AS avg_hp, AVG(career_growth_potential_percentage) AS avg_cgp,
  AVG(current_employees_count*1.0/active_positions_count) AS avg_saturation
FROM workday__job_overview GROUP BY job_value_tier
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-085/attempt-01/sql/S10.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-085/attempt-01/sql/S10.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-085/attempt-01/results/S10.rows.jsonl)；完整：True；SHA256：`47e2b47d2947d324547305df010279cf35d0d0bdab8629606a789ac888e0b566`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "workday__job_overview", "kind": "base", "block": null, "base_tables": ["workday__job_overview"]}] | [] | ["job_value_tier"] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | AVG(job_health_score) | [{"table": "workday__job_overview", "column": "job_health_score"}] | [] | False |
| B1 | AVG(avg_career_development_score) | [{"table": "workday__job_overview", "column": "avg_career_development_score"}] | [] | False |
| B1 | AVG(high_performer_percentage) | [{"table": "workday__job_overview", "column": "high_performer_percentage"}] | [] | False |
| B1 | AVG(career_growth_potential_percentage) | [{"table": "workday__job_overview", "column": "career_growth_potential_percentage"}] | [] | False |
| B1 | AVG(current_employees_count * 1.0 / active_positions_count) | [{"table": "workday__job_overview", "column": "active_positions_count"}, {"table": "workday__job_overview", "column": "current_employees_count"}] | [] | False |


## S11

类别 `data`；来源 `query_db`；调用 `2843f7752ee94c4296932e918129918d`；状态 `success`。

```sql
WITH base_metrics AS (
  SELECT
    job_profile_id, job_title, job_value_tier, talent_competition_level,
    job_health_score, avg_career_development_score,
    retention_difficulty_level, is_work_shift_required, avg_weekly_hours,
    current_employees_count, active_positions_count,
    high_performer_percentage, career_growth_potential_percentage,
    -- Talent allocation saturation
    ROUND(current_employees_count * 1.0 / active_positions_count, 4) AS talent_saturation,
    -- Talent quality index (product of fractions)
    ROUND(high_performer_percentage * career_growth_potential_percentage, 6) AS talent_quality_index
  FROM workday__job_overview
  WHERE job_value_tier IN ('Tier 1', 'Tier 2')
)
SELECT * FROM base_metrics
WHERE talent_competition_level IN ('High', 'Very High')
ORDER BY job_value_tier, talent_competition_level, talent_quality_index DESC
LIMIT 20
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-085/attempt-01/sql/S11.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-085/attempt-01/sql/S11.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-085/attempt-01/results/S11.rows.jsonl)；完整：True；SHA256：`120becea9cdc2be8dfbe5e2cae9026cdd6ea82ae52e4fadd7aa73c11a69c1c83`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "workday__job_overview", "kind": "base", "block": null, "base_tables": ["workday__job_overview"]}] | [] | [] |
| B2 | [{"alias": "base_metrics", "kind": "derived", "block": "B1", "base_tables": ["workday__job_overview"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |


## S12

类别 `data`；来源 `query_db`；调用 `d7ef460388b849498d30c7308d2ef2c7`；状态 `success`。

```sql
WITH base_metrics AS (
  SELECT
    job_profile_id, job_title, job_value_tier, talent_competition_level,
    job_health_score, avg_career_development_score,
    retention_difficulty_level, is_work_shift_required, avg_weekly_hours,
    current_employees_count, active_positions_count,
    high_performer_percentage, career_growth_potential_percentage,
    ROUND(current_employees_count * 1.0 / active_positions_count, 4) AS talent_saturation,
    ROUND(high_performer_percentage * career_growth_potential_percentage, 6) AS talent_quality_index
  FROM workday__job_overview
  WHERE job_value_tier IN ('Tier 1', 'Tier 2')
)
SELECT 
  talent_competition_level,
  COUNT(*) AS cnt,
  ROUND(AVG(talent_saturation), 4) AS avg_saturation,
  ROUND(AVG(talent_quality_index), 6) AS avg_quality,
  ROUND(AVG(job_health_score), 2) AS avg_health,
  ROUND(AVG(avg_career_development_score), 2) AS avg_dev,
  ROUND(AVG(avg_weekly_hours), 2) AS avg_hours
FROM base_metrics
WHERE talent_competition_level IN ('High', 'Very High')
GROUP BY talent_competition_level
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-085/attempt-01/sql/S12.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-085/attempt-01/sql/S12.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-085/attempt-01/results/S12.rows.jsonl)；完整：True；SHA256：`c431efd40e04c5316f6f35685056a07459865a1a9ec646571f11a8bf7f2c02ab`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "workday__job_overview", "kind": "base", "block": null, "base_tables": ["workday__job_overview"]}] | [] | [] |
| B2 | [{"alias": "base_metrics", "kind": "derived", "block": "B1", "base_tables": ["workday__job_overview"]}] | [] | ["talent_competition_level"] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B2 | COUNT(*) | [] | [] | True |
| B2 | AVG(talent_saturation) | [{"table": "workday__job_overview", "column": "active_positions_count"}, {"table": "workday__job_overview", "column": "current_employees_count"}] | [] | False |
| B2 | AVG(talent_quality_index) | [{"table": "workday__job_overview", "column": "high_performer_percentage"}, {"table": "workday__job_overview", "column": "career_growth_potential_percentage"}] | [] | False |
| B2 | AVG(job_health_score) | [{"table": "workday__job_overview", "column": "job_health_score"}] | [] | False |
| B2 | AVG(avg_career_development_score) | [{"table": "workday__job_overview", "column": "avg_career_development_score"}] | [] | False |
| B2 | AVG(avg_weekly_hours) | [{"table": "workday__job_overview", "column": "avg_weekly_hours"}] | [] | False |


## S13

类别 `data`；来源 `query_db`；调用 `e5cf9db5f42844f6ac0d3812fb12e98f`；状态 `success`。

```sql
WITH subset AS (
  SELECT job_profile_id, job_title, job_value_tier, talent_competition_level,
    job_health_score, avg_career_development_score, retention_difficulty_level,
    is_work_shift_required, avg_weekly_hours, current_employees_count, active_positions_count,
    ROUND(current_employees_count*1.0/active_positions_count,4) AS talent_saturation,
    ROUND(high_performer_percentage*career_growth_potential_percentage,6) AS talent_quality_index
  FROM workday__job_overview
  WHERE job_value_tier IN ('Tier 1','Tier 2') AND talent_competition_level IN ('High','Very High')
)
SELECT 
  ROUND(AVG(job_health_score),2) AS mean_health, 
  MIN(job_health_score) AS min_health, MAX(job_health_score) AS max_health,
  ROUND(AVG(avg_career_development_score),2) AS mean_dev,
  MIN(avg_career_development_score) AS min_dev, MAX(avg_career_development_score) AS max_dev,
  ROUND(AVG(talent_saturation),3) AS mean_sat,
  ROUND(AVG(talent_quality_index),5) AS mean_quality
FROM subset
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-085/attempt-01/sql/S13.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-085/attempt-01/sql/S13.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-085/attempt-01/results/S13.rows.jsonl)；完整：True；SHA256：`49689b8cb6ae06510fd99ffeb005d207cb2d3ecd5817bd23088ba7a9ef05ea2b`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "workday__job_overview", "kind": "base", "block": null, "base_tables": ["workday__job_overview"]}] | [] | [] |
| B2 | [{"alias": "subset", "kind": "derived", "block": "B1", "base_tables": ["workday__job_overview"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B2 | MIN(job_health_score) | [{"table": "workday__job_overview", "column": "job_health_score"}] | [] | False |
| B2 | MAX(job_health_score) | [{"table": "workday__job_overview", "column": "job_health_score"}] | [] | False |
| B2 | MIN(avg_career_development_score) | [{"table": "workday__job_overview", "column": "avg_career_development_score"}] | [] | False |
| B2 | MAX(avg_career_development_score) | [{"table": "workday__job_overview", "column": "avg_career_development_score"}] | [] | False |
| B2 | AVG(job_health_score) | [{"table": "workday__job_overview", "column": "job_health_score"}] | [] | False |
| B2 | AVG(avg_career_development_score) | [{"table": "workday__job_overview", "column": "avg_career_development_score"}] | [] | False |
| B2 | AVG(talent_saturation) | [{"table": "workday__job_overview", "column": "active_positions_count"}, {"table": "workday__job_overview", "column": "current_employees_count"}] | [] | False |
| B2 | AVG(talent_quality_index) | [{"table": "workday__job_overview", "column": "high_performer_percentage"}, {"table": "workday__job_overview", "column": "career_growth_potential_percentage"}] | [] | False |


## S14

类别 `data`；来源 `query_db`；调用 `d5a8e60e5556487093353de931d666b9`；状态 `success`。

```sql
WITH subset AS (
  SELECT job_profile_id, job_title, job_value_tier, talent_competition_level,
    job_health_score, avg_career_development_score,
    ROUND(current_employees_count*1.0/active_positions_count,4) AS talent_saturation,
    ROUND(high_performer_percentage*career_growth_potential_percentage,6) AS talent_quality_index
  FROM workday__job_overview
  WHERE job_value_tier IN ('Tier 1','Tier 2') AND talent_competition_level IN ('High','Very High')
)
SELECT 
  'health' AS metric,
  ROUND(MIN(job_health_score),2) AS p0, 
  ROUND(AVG(CASE WHEN rn_h <= cnt*0.25 THEN job_health_score END),2) AS q1,
  ROUND(AVG(CASE WHEN rn_h <= cnt*0.50 THEN job_health_score END),2) AS median,
  ROUND(AVG(CASE WHEN rn_h <= cnt*0.75 THEN job_health_score END),2) AS q3,
  ROUND(MAX(job_health_score),2) AS p100
FROM (
  SELECT job_health_score, ROW_NUMBER() OVER (ORDER BY job_health_score) AS rn_h, COUNT(*) OVER () AS cnt FROM subset
)
UNION ALL
SELECT 'dev',
  ROUND(MIN(avg_career_development_score),2),
  ROUND(AVG(CASE WHEN rn_d <= cnt*0.25 THEN avg_career_development_score END),2),
  ROUND(AVG(CASE WHEN rn_d <= cnt*0.50 THEN avg_career_development_score END),2),
  ROUND(AVG(CASE WHEN rn_d <= cnt*0.75 THEN avg_career_development_score END),2),
  ROUND(MAX(avg_career_development_score),2)
FROM (
  SELECT avg_career_development_score, ROW_NUMBER() OVER (ORDER BY avg_career_development_score) AS rn_d, COUNT(*) OVER () AS cnt FROM subset
)
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-085/attempt-01/sql/S14.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-085/attempt-01/sql/S14.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-085/attempt-01/results/S14.rows.jsonl)；完整：True；SHA256：`607986527603dda0164d29a30a238542a63d29b6711b1ad10860325738e4c6aa`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "workday__job_overview", "kind": "base", "block": null, "base_tables": ["workday__job_overview"]}] | [] | [] |
| B2 | [{"alias": "subset", "kind": "derived", "block": "B1", "base_tables": ["workday__job_overview"]}] | [] | [] |
| B3 | [{"alias": "", "kind": "derived", "block": "B2", "base_tables": ["workday__job_overview"]}] | [] | [] |
| B4 | [{"alias": "subset", "kind": "derived", "block": "B1", "base_tables": ["workday__job_overview"]}] | [] | [] |
| B5 | [{"alias": "", "kind": "derived", "block": "B4", "base_tables": ["workday__job_overview"]}] | [] | [] |
| B6 | [] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B3 | MIN(job_health_score) | [{"table": "workday__job_overview", "column": "job_health_score"}] | [] | False |
| B3 | AVG(CASE WHEN rn_h <= cnt * 0.25 THEN job_health_score END) | [{"table": "workday__job_overview", "column": "job_health_score"}] | [{"table": "workday__job_overview", "column": "job_health_score"}] | False |
| B3 | AVG(CASE WHEN rn_h <= cnt * 0.50 THEN job_health_score END) | [{"table": "workday__job_overview", "column": "job_health_score"}] | [{"table": "workday__job_overview", "column": "job_health_score"}] | False |
| B3 | AVG(CASE WHEN rn_h <= cnt * 0.75 THEN job_health_score END) | [{"table": "workday__job_overview", "column": "job_health_score"}] | [{"table": "workday__job_overview", "column": "job_health_score"}] | False |
| B3 | MAX(job_health_score) | [{"table": "workday__job_overview", "column": "job_health_score"}] | [] | False |
| B5 | MIN(avg_career_development_score) | [{"table": "workday__job_overview", "column": "avg_career_development_score"}] | [] | False |
| B5 | AVG(CASE WHEN rn_d <= cnt * 0.25 THEN avg_career_development_score END) | [{"table": "workday__job_overview", "column": "avg_career_development_score"}] | [{"table": "workday__job_overview", "column": "avg_career_development_score"}] | False |
| B5 | AVG(CASE WHEN rn_d <= cnt * 0.50 THEN avg_career_development_score END) | [{"table": "workday__job_overview", "column": "avg_career_development_score"}] | [{"table": "workday__job_overview", "column": "avg_career_development_score"}] | False |
| B5 | AVG(CASE WHEN rn_d <= cnt * 0.75 THEN avg_career_development_score END) | [{"table": "workday__job_overview", "column": "avg_career_development_score"}] | [{"table": "workday__job_overview", "column": "avg_career_development_score"}] | False |
| B5 | MAX(avg_career_development_score) | [{"table": "workday__job_overview", "column": "avg_career_development_score"}] | [] | False |


## S15

类别 `data`；来源 `query_db`；调用 `06bda4b78cbc454eb8a51603fad57d4b`；状态 `success`。

```sql
WITH subset AS (
  SELECT job_profile_id, job_title, job_value_tier, talent_competition_level,
    job_health_score, avg_career_development_score, retention_difficulty_level,
    is_work_shift_required, avg_weekly_hours, current_employees_count, active_positions_count,
    ROUND(current_employees_count*1.0/active_positions_count,4) AS talent_saturation,
    ROUND(high_performer_percentage*career_growth_potential_percentage,6) AS talent_quality_index
  FROM workday__job_overview
  WHERE job_value_tier IN ('Tier 1','Tier 2') AND talent_competition_level IN ('High','Very High')
)
SELECT * FROM subset ORDER BY job_profile_id
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-085/attempt-01/sql/S15.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-085/attempt-01/sql/S15.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-085/attempt-01/results/S15.rows.jsonl)；完整：True；SHA256：`7c48df6539c4b8eea84b26969f745f20e4c1256e101f4152ac83393a30af34fd`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "workday__job_overview", "kind": "base", "block": null, "base_tables": ["workday__job_overview"]}] | [] | [] |
| B2 | [{"alias": "subset", "kind": "derived", "block": "B1", "base_tables": ["workday__job_overview"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |


## S16

类别 `data`；来源 `query_db`；调用 `5e5b1826d9334ca68f187379f225fde5`；状态 `success`。

```sql
WITH base AS (
  SELECT
    job_profile_id, job_title, job_value_tier, talent_competition_level,
    job_health_score, avg_career_development_score,
    retention_difficulty_level, is_work_shift_required, avg_weekly_hours,
    current_employees_count, active_positions_count, total_positions_count,
    high_performer_percentage, career_growth_potential_percentage,
    ROUND(current_employees_count * 1.0 / NULLIF(active_positions_count, 0), 4) AS talent_saturation,
    ROUND(high_performer_percentage * career_growth_potential_percentage, 6) AS talent_quality_index,
    job_rarity_level, job_maturity_level, talent_management_recommendation
  FROM workday__job_overview
  WHERE job_value_tier IN ('Tier 1', 'Tier 2') AND talent_competition_level IN ('High', 'Very High')
)
SELECT * FROM base
ORDER BY job_health_score ASC, avg_career_development_score ASC
LIMIT 30
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-085/attempt-01/sql/S16.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-085/attempt-01/sql/S16.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-085/attempt-01/results/S16.rows.jsonl)；完整：True；SHA256：`b529f1100dd20325286b49003988ade2401abaf82bede9e4c0b934267910da98`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "workday__job_overview", "kind": "base", "block": null, "base_tables": ["workday__job_overview"]}] | [] | [] |
| B2 | [{"alias": "base", "kind": "derived", "block": "B1", "base_tables": ["workday__job_overview"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |


## S17

类别 `data`；来源 `query_db`；调用 `6b503e94978f40e19d6a6bc766e68572`；状态 `success`。

```sql
SELECT retention_difficulty_level, 
  COUNT(*) AS cnt,
  ROUND(AVG(job_health_score),2) AS avg_health,
  ROUND(AVG(avg_career_development_score),2) AS avg_dev,
  ROUND(AVG(high_performer_percentage*career_growth_potential_percentage),5) AS avg_quality,
  ROUND(AVG(current_employees_count*1.0/active_positions_count),3) AS avg_saturation,
  ROUND(AVG(avg_weekly_hours),2) AS avg_hours,
  ROUND(SUM(is_work_shift_required)*1.0/COUNT(*),3) AS shift_ratio
FROM workday__job_overview
WHERE job_value_tier IN ('Tier 1','Tier 2') AND talent_competition_level IN ('High','Very High')
GROUP BY retention_difficulty_level
ORDER BY cnt DESC
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-085/attempt-01/sql/S17.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-085/attempt-01/sql/S17.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-085/attempt-01/results/S17.rows.jsonl)；完整：True；SHA256：`b217e3a9144899c27ff100aac1463f0d8af3c77acc264fbfc87c00c19929719d`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "workday__job_overview", "kind": "base", "block": null, "base_tables": ["workday__job_overview"]}] | [] | ["retention_difficulty_level"] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |
| B1 | AVG(job_health_score) | [{"table": "workday__job_overview", "column": "job_health_score"}] | [] | False |
| B1 | AVG(avg_career_development_score) | [{"table": "workday__job_overview", "column": "avg_career_development_score"}] | [] | False |
| B1 | AVG(high_performer_percentage * career_growth_potential_percentage) | [{"table": "workday__job_overview", "column": "high_performer_percentage"}, {"table": "workday__job_overview", "column": "career_growth_potential_percentage"}] | [] | False |
| B1 | AVG(current_employees_count * 1.0 / active_positions_count) | [{"table": "workday__job_overview", "column": "active_positions_count"}, {"table": "workday__job_overview", "column": "current_employees_count"}] | [] | False |
| B1 | AVG(avg_weekly_hours) | [{"table": "workday__job_overview", "column": "avg_weekly_hours"}] | [] | False |
| B1 | COUNT(*) | [] | [] | True |
| B1 | SUM(is_work_shift_required) | [{"table": "workday__job_overview", "column": "is_work_shift_required"}] | [] | False |

