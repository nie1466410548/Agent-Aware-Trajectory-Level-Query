# dacomp-072

We want to establish a data-driven performance evaluation system for hiring managers. Plea…

运行：已提交。官方未评分。全部 SQL 尝试/成功 18/18；数据 SQL 16/16；Python 3 次。

完整原题：

We want to establish a data-driven performance evaluation system for hiring managers. Please use the `lever__hiring_manager_scorecard` table to calculate a composite efficiency score for each hiring manager based on the following dimensions:
- Candidate hire rate (30% weight)
- Whether `avg_total_days_to_hire` is less than 45 days (25% weight)
- Whether `avg_candidate_experience_score` is greater than 3.5 (25% weight)
- Whether `feedback_completion_rate_managed` is over 85% (20% weight)

Based on the final score, classify hiring managers into three tiers: Excellent (score ≥ 80), Good (60 ≤ score < 80), and Needs Improvement (score < 60). Only hiring managers who own at least 5 requisitions (`total_requisitions_owned` ≥ 5) should be included in the evaluation.

| 表 | 行数 | 列数 |
| --- | --- | --- |
| lever__hiring_manager_scorecard | 235 | 36 |


实际路线（分析者依据 SQL/源码概括，不代表 Agent 自述）：SQL 筛选经理、计算加权效率分并分层 → Python 层级均值与图表。

数据库大小：122,880 字节。

## 数据 SQL

| SQL | 状态 | 基础表 | Join 输入/类型 | GROUP BY | 聚合表达式 | 结果行数 | 数据库 ms |
| --- | --- | --- | --- | --- | --- | --- | --- |
| [S3/Q1](#s3) | success | ["lever__hiring_manager_scorecard"] | 0 / {} | [] | ["COUNT(*)"] | 1 | 0.368 |
| [S4/Q2](#s4) | success | ["lever__hiring_manager_scorecard"] | 0 / {} | [] | [] | 10 | 0.47 |
| [S5/Q3](#s5) | success | ["lever__hiring_manager_scorecard"] | 0 / {} | [] | ["SUM(CASE WHEN candidate_hire_rate IS NULL THEN 1 ELSE 0 END)", "SUM(CASE WHEN avg_total_days_to_hire IS NULL THEN 1 ELSE 0 END)", "SUM(CASE WHEN avg_candidate_experience_score IS NULL THEN 1 ELSE 0 END)", "SUM(CASE WHEN feedback_completion_rate_managed IS NULL THEN 1 ELSE 0 END)", "SUM(CASE WHEN total_requisitions_owned IS NULL THEN 1 ELSE 0 END)"] | 1 | 0.421 |
| [S6/Q4](#s6) | success | ["lever__hiring_manager_scorecard"] | 0 / {} | [] | ["COUNT(*)", "MIN(candidate_hire_rate)", "MAX(candidate_hire_rate)", "MIN(avg_total_days_to_hire)", "MAX(avg_total_days_to_hire)", "MIN(avg_candidate_experience_score)", "MAX(avg_candidate_experience_score)", "MIN(feedback_completion_rate_managed)", "MAX(feedback_completion_rate_managed)", "MIN(total_requisitions_owned)", "MAX(total_requisitions_owned)"] | 1 | 0.489 |
| [S7/Q5](#s7) | success | ["lever__hiring_manager_scorecard"] | 0 / {} | [] | ["COUNT(*)", "SUM(CASE WHEN total_requisitions_owned < 5 THEN 1 ELSE 0 END)", "SUM(CASE WHEN total_requisitions_owned >= 5 THEN 1 ELSE 0 END)"] | 1 | 0.367 |
| [S8/Q6](#s8) | success | ["lever__hiring_manager_scorecard"] | 0 / {} | [] | [] | 20 | 1.11 |
| [S9/Q7](#s9) | success | ["lever__hiring_manager_scorecard"] | 0 / {} | ["performance_tier"] | ["COUNT(*)", "MIN(composite_score)", "MAX(composite_score)", "AVG(composite_score)"] | 3 | 1.541 |
| [S10/Q8](#s10) | success | ["lever__hiring_manager_scorecard"] | 0 / {} | ["performance_tier"] | ["COUNT(*)", "SUM(CASE WHEN days_score = 100 THEN 1 ELSE 0 END)", "SUM(CASE WHEN experience_score = 100 THEN 1 ELSE 0 END)", "SUM(CASE WHEN feedback_score = 100 THEN 1 ELSE 0 END)", "AVG(hire_rate_score)"] | 3 | 1.175 |
| [S11/Q9](#s11) | success | ["lever__hiring_manager_scorecard"] | 0 / {} | [] | ["COUNT(*)", "MIN(composite_score)", "MAX(composite_score)", "AVG(composite_score)", "AVG(composite_score * composite_score)", "AVG(composite_score)", "AVG(composite_score)"] | 1 | 1.452 |
| [S12/Q10](#s12) | success | ["lever__hiring_manager_scorecard"] | 0 / {} | [] | [] | 235 | 1.489 |
| [S13/Q11](#s13) | success | ["lever__hiring_manager_scorecard"] | 0 / {} | [] | [] | 235 | 1.298 |
| [S14/Q12](#s14) | success | ["lever__hiring_manager_scorecard"] | 0 / {} | [] | [] | 13 | 0.793 |
| [S15/Q13](#s15) | success | ["lever__hiring_manager_scorecard"] | 0 / {} | [] | [] | 5 | 0.748 |
| [S16/Q14](#s16) | success | ["lever__hiring_manager_scorecard"] | 0 / {} | [] | ["COUNT(*)", "SUM(CASE WHEN days_score = 100 THEN 1 ELSE 0 END)", "SUM(CASE WHEN experience_score = 100 THEN 1 ELSE 0 END)", "SUM(CASE WHEN feedback_score = 100 THEN 1 ELSE 0 END)", "SUM(CASE WHEN hire_rate_score >= 50 THEN 1 ELSE 0 END)", "SUM(CASE WHEN days_score = 100 AND experience_score = 100 AND feedback_score = 100 AND hire_rate_score >= 50 THEN 1 ELSE 0 END)", "AVG(hire_rate_score)"] | 1 | 0.727 |
| [S17/Q15](#s17) | success | ["lever__hiring_manager_scorecard"] | 0 / {} | ["CASE WHEN total_requisitions_owned BETWEEN 5 AND 19 THEN '5-19' WHEN total_requisitions_owned BETWEEN 20 AND 39 THEN '20-39' ELSE '40+' END"] | ["COUNT(*)", "AVG(composite_score)", "AVG(hire_rate_score)"] | 3 | 0.863 |
| [S18/Q16](#s18) | success | ["lever__hiring_manager_scorecard"] | 0 / {} | [] | [] | 10 | 0.813 |


## 元数据和设置

| SQL | 类别 | 状态 | 内容 |
| --- | --- | --- | --- |
| S1 | connection_setup | success | PRAGMA query_only=ON |
| S2 | metadata | success | SELECT name,sql FROM sqlite_master WHERE type='table' ORDER BY name |


## Python 与执行位置

人工源码审查：**database_first_violation**。招聘经理资格筛选、评分与分层主要在 SQL 完成，但 Python 为图表按绩效层级再计算四项得分均值，属于可由 SQL 提供的绘图准备，记录为有限范围的分组聚合偏离。 [证据](../reviews/dacomp-072.json)。

P1：Visualization: Creating a histogram of composite scores and a tier breakdown pie chart, plus scatter plot of hire rate vs. composite score. This visualization is done outside SQL because SQLite lacks built-in plotting capabilities.

[源码](../../../runs/dsv4flash-db-first-full-01/dacomp-072/attempt-01/python/P1.py)；[输出](../../../runs/dsv4flash-db-first-full-01/dacomp-072/attempt-01/python/P1.stdout)；[错误](../../../runs/dsv4flash-db-first-full-01/dacomp-072/attempt-01/python/P1.stderr)。检出需人工核验的 SQL 可实现操作：groupby(；不能仅凭理由判为合规。

P2：Loading the full composite scorecard results into pandas for visualization. This reuses the SQL-defined scoring logic and only loads the computed columns needed for plotting; SQLite lacks plotting support, so charting is done in Python.

[源码](../../../runs/dsv4flash-db-first-full-01/dacomp-072/attempt-01/python/P2.py)；[输出](../../../runs/dsv4flash-db-first-full-01/dacomp-072/attempt-01/python/P2.stdout)；[错误](../../../runs/dsv4flash-db-first-full-01/dacomp-072/attempt-01/python/P2.stderr)。检出需人工核验的 SQL 可实现操作：.query(；不能仅凭理由判为合规。

P3：Creating visualizations: histogram of composite scores, pie chart of tier distribution, scatter plot of hire rate vs composite score, and grouped bar chart of component scores by tier. These are all graphical outputs that SQLite cannot produce.

[源码](../../../runs/dsv4flash-db-first-full-01/dacomp-072/attempt-01/python/P3.py)；[输出](../../../runs/dsv4flash-db-first-full-01/dacomp-072/attempt-01/python/P3.stdout)；[错误](../../../runs/dsv4flash-db-first-full-01/dacomp-072/attempt-01/python/P3.stderr)。检出需人工核验的 SQL 可实现操作：groupby(；不能仅凭理由判为合规。

## 优化机会

已验证候选。筛选限于精确 SQL、相同自包含 CTE、相同单表完整过滤、可分解单表聚合；未覆盖任意 Join 等价和一般谓词蕴含。全部候选都是 offline，未测在线预测。

| 候选 | 类型 | 已有结果 | 覆盖 SQL | 后续次数 | 中间行数 | 验证 | 成本 |
| --- | --- | --- | --- | --- | --- | --- | --- |
| C1 | common subexpression | False | ["S9", "S10", "S12", "S13"] | 3 | 235 | verified | Not benchmarked; correctness alone does not establish net speedup. |
| C2 | common subexpression | False | ["S15", "S18"] | 1 | 235 | verified | Not benchmarked; correctness alone does not establish net speedup. |
| C3 | aggregate MV | False | ["S3", "S5", "S7"] | 2 | 1 | verified | Not benchmarked; correctness alone does not establish net speedup. |


已验证覆盖（含触发查询、候选并集去重）：9/16 条成功数据 SQL。正确性仅针对当前数据库快照；未测性能的候选不能声称已加速。

[完整 build/rewrite 与比较证据](dacomp-072.analysis.json)。

### C1：common subexpression

Identical self-contained CTE body across queries.

原查询 [S9](#s9), [S10](#s10), [S12](#s12), [S13](#s13) → 新增共享状态 C1 → 后续 3 次可复用。该构建点为事后假设，不代表 Agent 当时预知后续。

构建定义：

```sql
SELECT hiring_manager_id, hiring_manager_name, total_requisitions_owned, candidate_hire_rate, avg_total_days_to_hire, avg_candidate_experience_score, feedback_completion_rate_managed, ROUND(candidate_hire_rate * 100, 2) AS hire_rate_score, CASE WHEN avg_total_days_to_hire < 45 THEN 100.0 ELSE 0.0 END AS days_score, CASE WHEN avg_candidate_experience_score > 3.5 THEN 100.0 ELSE 0.0 END AS experience_score, CASE WHEN feedback_completion_rate_managed > 85.0 THEN 100.0 ELSE 0.0 END AS feedback_score FROM lever__hiring_manager_scorecard WHERE total_requisitions_owned >= 5
```

受益查询 S9 的改写示例：

```sql
WITH score_components AS (SELECT * FROM temp.reuse_candidate), composite AS (SELECT *, ROUND(0.30 * hire_rate_score + 0.25 * days_score + 0.25 * experience_score + 0.20 * feedback_score, 2) AS composite_score FROM score_components) SELECT performance_tier, COUNT(*) AS manager_count, ROUND(AVG(composite_score), 2) AS avg_score, MIN(composite_score) AS min_score, MAX(composite_score) AS max_score FROM (SELECT *, CASE WHEN composite_score >= 80 THEN 'Excellent' WHEN composite_score >= 60 THEN 'Good' ELSE 'Needs Improvement' END AS performance_tier FROM composite) AS t GROUP BY performance_tier ORDER BY avg_score DESC
```

| 原 SQL | 列名一致 | 结果一致 | 比较方法 |
| --- | --- | --- | --- |
| S9 | True | True | ordered_numeric_tolerance |
| S10 | True | True | ordered_numeric_tolerance |
| S12 | True | True | ordered_numeric_tolerance |
| S13 | True | True | ordered_numeric_tolerance |


验证状态：verified；成本结论：Not benchmarked; correctness alone does not establish net speedup.

### C3：aggregate MV

Union of grouping keys; decomposable aggregate states; AVG uses SUM and non-NULL COUNT.

原查询 [S3](#s3), [S5](#s5), [S7](#s7) → 新增共享状态 C3 → 后续 2 次可复用。该构建点为事后假设，不代表 Agent 当时预知后续。

构建定义：

```sql
SELECT COUNT(*) AS __a0, SUM(CASE WHEN candidate_hire_rate IS NULL THEN 1 ELSE 0 END) AS __a1, SUM(CASE WHEN avg_total_days_to_hire IS NULL THEN 1 ELSE 0 END) AS __a2, SUM(CASE WHEN avg_candidate_experience_score IS NULL THEN 1 ELSE 0 END) AS __a3, SUM(CASE WHEN feedback_completion_rate_managed IS NULL THEN 1 ELSE 0 END) AS __a4, SUM(CASE WHEN total_requisitions_owned IS NULL THEN 1 ELSE 0 END) AS __a5, SUM(CASE WHEN total_requisitions_owned < 5 THEN 1 ELSE 0 END) AS __a6, SUM(CASE WHEN total_requisitions_owned >= 5 THEN 1 ELSE 0 END) AS __a7 FROM "lever__hiring_manager_scorecard" 
```

受益查询 S3 的改写示例：

```sql
SELECT SUM(__a0) AS row_count FROM temp.reuse_candidate
```

| 原 SQL | 列名一致 | 结果一致 | 比较方法 |
| --- | --- | --- | --- |
| S3 | True | True | exact_multiset |
| S5 | True | True | exact_multiset |
| S7 | True | True | exact_multiset |


验证状态：verified；成本结论：Not benchmarked; correctness alone does not establish net speedup.

### C2：common subexpression

Identical self-contained CTE body across queries.

原查询 [S15](#s15), [S18](#s18) → 新增共享状态 C2 → 后续 1 次可复用。该构建点为事后假设，不代表 Agent 当时预知后续。

构建定义：

```sql
SELECT hiring_manager_id, hiring_manager_name, total_requisitions_owned, ROUND(candidate_hire_rate * 100, 2) AS hire_rate_score, CASE WHEN avg_total_days_to_hire < 45 THEN 100.0 ELSE 0.0 END AS days_score, CASE WHEN avg_candidate_experience_score > 3.5 THEN 100.0 ELSE 0.0 END AS experience_score, CASE WHEN feedback_completion_rate_managed > 85.0 THEN 100.0 ELSE 0.0 END AS feedback_score FROM lever__hiring_manager_scorecard WHERE total_requisitions_owned >= 5
```

受益查询 S15 的改写示例：

```sql
WITH score_components AS (SELECT * FROM temp.reuse_candidate), composite AS (SELECT *, ROUND(0.30 * hire_rate_score + 0.25 * days_score + 0.25 * experience_score + 0.20 * feedback_score, 2) AS composite_score FROM score_components) SELECT hiring_manager_id, hiring_manager_name, total_requisitions_owned, hire_rate_score, days_score, experience_score, feedback_score, composite_score FROM composite ORDER BY composite_score ASC LIMIT 5
```

| 原 SQL | 列名一致 | 结果一致 | 比较方法 |
| --- | --- | --- | --- |
| S15 | True | True | ordered_numeric_tolerance |
| S18 | True | True | ordered_numeric_tolerance |


验证状态：verified；成本结论：Not benchmarked; correctness alone does not establish net speedup.

结果依赖：自动记录 SQL→Python 的接口父调用，以及源码中引用归档文件的消费者；字面值相同不认定因果。模型方向选择需要人工读取消息，尚未做全面因果标注。

[原始报告](../../../runs/dsv4flash-db-first-full-01/dacomp-072/attempt-01/answer.md)；[统一消息](../../../runs/dsv4flash-db-first-full-01/dacomp-072/attempt-01/messages.jsonl)；[原始 OpenCode 事件](../../../runs/dsv4flash-db-first-full-01/dacomp-072/attempt-01/opencode.jsonl)；[SQL 引擎日志](../../../runs/dsv4flash-db-first-full-01/dacomp-072/attempt-01/sql_journal.jsonl)。

[可读报告（本地图片链接规范化）](../answers/dacomp-072.md)。原始回答保留，分析结论未改写。

## S1

类别 `connection_setup`；来源 `connection`；调用 `47f2926341c741249d53cc4fe6f8cfb1`；状态 `success`。

```sql
PRAGMA query_only=ON
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-072/attempt-01/sql/S1.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-072/attempt-01/sql/S1.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-072/attempt-01/results/S1.rows.jsonl)；完整：True；SHA256：`e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`。

## S2

类别 `metadata`；来源 `list_db`；调用 `47f2926341c741249d53cc4fe6f8cfb1`；状态 `success`。

```sql
SELECT name,sql FROM sqlite_master WHERE type='table' ORDER BY name
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-072/attempt-01/sql/S2.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-072/attempt-01/sql/S2.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-072/attempt-01/results/S2.rows.jsonl)；完整：True；SHA256：`ca51ff83c8af52ce235e051f3b076bfefd934fda70f9b383c2085584e19be46d`。

## S3

类别 `data`；来源 `query_db`；调用 `b96cd0f6bd7b420a90462a7a26a3b0c9`；状态 `success`。

```sql
SELECT COUNT(*) AS row_count FROM lever__hiring_manager_scorecard
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-072/attempt-01/sql/S3.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-072/attempt-01/sql/S3.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-072/attempt-01/results/S3.rows.jsonl)；完整：True；SHA256：`5bbf39b93dbc91a9b14a963d660dd9a56fb1e69b3acdc295eaa03314799d82f5`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "lever__hiring_manager_scorecard", "kind": "base", "block": null, "base_tables": ["lever__hiring_manager_scorecard"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |


## S4

类别 `data`；来源 `query_db`；调用 `f8d8d3309cc84ff48b2f2d4b3ff54a55`；状态 `success`。

```sql
SELECT hiring_manager_id, hiring_manager_name, total_requisitions_owned, candidate_hire_rate, avg_total_days_to_hire, avg_candidate_experience_score, feedback_completion_rate_managed FROM lever__hiring_manager_scorecard LIMIT 10
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-072/attempt-01/sql/S4.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-072/attempt-01/sql/S4.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-072/attempt-01/results/S4.rows.jsonl)；完整：True；SHA256：`bc81aa3823bf0a8133c4747cfffebc4ab255f02ce95b166523412a6da9a2abba`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "lever__hiring_manager_scorecard", "kind": "base", "block": null, "base_tables": ["lever__hiring_manager_scorecard"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |


## S5

类别 `data`；来源 `query_db`；调用 `0f3a0d7667c64ac1b93379276b858b63`；状态 `success`。

```sql
SELECT 
  SUM(CASE WHEN candidate_hire_rate IS NULL THEN 1 ELSE 0 END) AS null_hire_rate,
  SUM(CASE WHEN avg_total_days_to_hire IS NULL THEN 1 ELSE 0 END) AS null_days,
  SUM(CASE WHEN avg_candidate_experience_score IS NULL THEN 1 ELSE 0 END) AS null_exp,
  SUM(CASE WHEN feedback_completion_rate_managed IS NULL THEN 1 ELSE 0 END) AS null_feedback,
  SUM(CASE WHEN total_requisitions_owned IS NULL THEN 1 ELSE 0 END) AS null_req
FROM lever__hiring_manager_scorecard
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-072/attempt-01/sql/S5.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-072/attempt-01/sql/S5.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-072/attempt-01/results/S5.rows.jsonl)；完整：True；SHA256：`58ac6b25f66c17897ba825e5f41b5b5c2ca9964bd23ec95028409c9b5309e29d`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "lever__hiring_manager_scorecard", "kind": "base", "block": null, "base_tables": ["lever__hiring_manager_scorecard"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | SUM(CASE WHEN candidate_hire_rate IS NULL THEN 1 ELSE 0 END) | [] | [{"table": "lever__hiring_manager_scorecard", "column": "candidate_hire_rate"}] | False |
| B1 | SUM(CASE WHEN avg_total_days_to_hire IS NULL THEN 1 ELSE 0 END) | [] | [{"table": "lever__hiring_manager_scorecard", "column": "avg_total_days_to_hire"}] | False |
| B1 | SUM(CASE WHEN avg_candidate_experience_score IS NULL THEN 1 ELSE 0 END) | [] | [{"table": "lever__hiring_manager_scorecard", "column": "avg_candidate_experience_score"}] | False |
| B1 | SUM(CASE WHEN feedback_completion_rate_managed IS NULL THEN 1 ELSE 0 END) | [] | [{"table": "lever__hiring_manager_scorecard", "column": "feedback_completion_rate_managed"}] | False |
| B1 | SUM(CASE WHEN total_requisitions_owned IS NULL THEN 1 ELSE 0 END) | [] | [{"table": "lever__hiring_manager_scorecard", "column": "total_requisitions_owned"}] | False |


## S6

类别 `data`；来源 `query_db`；调用 `e3f0e23623624384afdea800c939fa66`；状态 `success`。

```sql
SELECT COUNT(*) AS eligible, 
  MIN(candidate_hire_rate) AS min_hr, MAX(candidate_hire_rate) AS max_hr,
  MIN(avg_total_days_to_hire) AS min_days, MAX(avg_total_days_to_hire) AS max_days,
  MIN(avg_candidate_experience_score) AS min_exp, MAX(avg_candidate_experience_score) AS max_exp,
  MIN(feedback_completion_rate_managed) AS min_fb, MAX(feedback_completion_rate_managed) AS max_fb,
  MIN(total_requisitions_owned) AS min_req, MAX(total_requisitions_owned) AS max_req
FROM lever__hiring_manager_scorecard
WHERE total_requisitions_owned >= 5
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-072/attempt-01/sql/S6.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-072/attempt-01/sql/S6.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-072/attempt-01/results/S6.rows.jsonl)；完整：True；SHA256：`a92023d76818448ede4d8acc33bb0ef4bd7be395199b4dd8c3c135810a8676bc`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "lever__hiring_manager_scorecard", "kind": "base", "block": null, "base_tables": ["lever__hiring_manager_scorecard"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |
| B1 | MIN(candidate_hire_rate) | [{"table": "lever__hiring_manager_scorecard", "column": "candidate_hire_rate"}] | [] | False |
| B1 | MAX(candidate_hire_rate) | [{"table": "lever__hiring_manager_scorecard", "column": "candidate_hire_rate"}] | [] | False |
| B1 | MIN(avg_total_days_to_hire) | [{"table": "lever__hiring_manager_scorecard", "column": "avg_total_days_to_hire"}] | [] | False |
| B1 | MAX(avg_total_days_to_hire) | [{"table": "lever__hiring_manager_scorecard", "column": "avg_total_days_to_hire"}] | [] | False |
| B1 | MIN(avg_candidate_experience_score) | [{"table": "lever__hiring_manager_scorecard", "column": "avg_candidate_experience_score"}] | [] | False |
| B1 | MAX(avg_candidate_experience_score) | [{"table": "lever__hiring_manager_scorecard", "column": "avg_candidate_experience_score"}] | [] | False |
| B1 | MIN(feedback_completion_rate_managed) | [{"table": "lever__hiring_manager_scorecard", "column": "feedback_completion_rate_managed"}] | [] | False |
| B1 | MAX(feedback_completion_rate_managed) | [{"table": "lever__hiring_manager_scorecard", "column": "feedback_completion_rate_managed"}] | [] | False |
| B1 | MIN(total_requisitions_owned) | [{"table": "lever__hiring_manager_scorecard", "column": "total_requisitions_owned"}] | [] | False |
| B1 | MAX(total_requisitions_owned) | [{"table": "lever__hiring_manager_scorecard", "column": "total_requisitions_owned"}] | [] | False |


## S7

类别 `data`；来源 `query_db`；调用 `7d26013c28504660a8f73e4164ba5efb`；状态 `success`。

```sql
SELECT COUNT(*) AS total_managers,
  SUM(CASE WHEN total_requisitions_owned < 5 THEN 1 ELSE 0 END) AS excluded_low_req,
  SUM(CASE WHEN total_requisitions_owned >= 5 THEN 1 ELSE 0 END) AS eligible
FROM lever__hiring_manager_scorecard
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-072/attempt-01/sql/S7.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-072/attempt-01/sql/S7.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-072/attempt-01/results/S7.rows.jsonl)；完整：True；SHA256：`07c654729270291af3c814a7fb93e824102bae5036432ec7c6273f0405087ce9`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "lever__hiring_manager_scorecard", "kind": "base", "block": null, "base_tables": ["lever__hiring_manager_scorecard"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |
| B1 | SUM(CASE WHEN total_requisitions_owned < 5 THEN 1 ELSE 0 END) | [] | [{"table": "lever__hiring_manager_scorecard", "column": "total_requisitions_owned"}] | False |
| B1 | SUM(CASE WHEN total_requisitions_owned >= 5 THEN 1 ELSE 0 END) | [] | [{"table": "lever__hiring_manager_scorecard", "column": "total_requisitions_owned"}] | False |


## S8

类别 `data`；来源 `query_db`；调用 `d91aad3c56644d7084c2e0432b59f8ea`；状态 `success`。

```sql
WITH score_components AS (
  SELECT
    hiring_manager_id,
    hiring_manager_name,
    hiring_manager_email,
    total_requisitions_owned,
    candidate_hire_rate,
    avg_total_days_to_hire,
    avg_candidate_experience_score,
    feedback_completion_rate_managed,
    -- Convert hire rate to 0-100 scale
    ROUND(candidate_hire_rate * 100, 2) AS hire_rate_score,
    -- Boolean scores (0 or 100)
    CASE WHEN avg_total_days_to_hire < 45 THEN 100.0 ELSE 0.0 END AS days_score,
    CASE WHEN avg_candidate_experience_score > 3.5 THEN 100.0 ELSE 0.0 END AS experience_score,
    CASE WHEN feedback_completion_rate_managed > 85.0 THEN 100.0 ELSE 0.0 END AS feedback_score
  FROM lever__hiring_manager_scorecard
  WHERE total_requisitions_owned >= 5
),
composite AS (
  SELECT
    *,
    ROUND(
      0.30 * hire_rate_score + 
      0.25 * days_score + 
      0.25 * experience_score + 
      0.20 * feedback_score, 
    2) AS composite_score
  FROM score_components
)
SELECT
  hiring_manager_id,
  hiring_manager_name,
  total_requisitions_owned,
  ROUND(candidate_hire_rate * 100, 2) AS hire_rate_pct,
  avg_total_days_to_hire,
  avg_candidate_experience_score,
  feedback_completion_rate_managed,
  hire_rate_score,
  days_score,
  experience_score,
  feedback_score,
  composite_score,
  CASE 
    WHEN composite_score >= 80 THEN 'Excellent'
    WHEN composite_score >= 60 THEN 'Good'
    ELSE 'Needs Improvement'
  END AS performance_tier
FROM composite
ORDER BY composite_score DESC
LIMIT 20
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-072/attempt-01/sql/S8.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-072/attempt-01/sql/S8.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-072/attempt-01/results/S8.rows.jsonl)；完整：True；SHA256：`afe4b8007671ead94b9a5b3aa178e2bea49cc310c3fa955ab6f106c66c887440`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "lever__hiring_manager_scorecard", "kind": "base", "block": null, "base_tables": ["lever__hiring_manager_scorecard"]}] | [] | [] |
| B2 | [{"alias": "score_components", "kind": "derived", "block": "B1", "base_tables": ["lever__hiring_manager_scorecard"]}] | [] | [] |
| B3 | [{"alias": "composite", "kind": "derived", "block": "B2", "base_tables": ["lever__hiring_manager_scorecard"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |


## S9

类别 `data`；来源 `query_db`；调用 `0a6949670e52486cae755df3fcfd84d5`；状态 `success`。

```sql
WITH score_components AS (
  SELECT
    hiring_manager_id,
    hiring_manager_name,
    total_requisitions_owned,
    candidate_hire_rate,
    avg_total_days_to_hire,
    avg_candidate_experience_score,
    feedback_completion_rate_managed,
    ROUND(candidate_hire_rate * 100, 2) AS hire_rate_score,
    CASE WHEN avg_total_days_to_hire < 45 THEN 100.0 ELSE 0.0 END AS days_score,
    CASE WHEN avg_candidate_experience_score > 3.5 THEN 100.0 ELSE 0.0 END AS experience_score,
    CASE WHEN feedback_completion_rate_managed > 85.0 THEN 100.0 ELSE 0.0 END AS feedback_score
  FROM lever__hiring_manager_scorecard
  WHERE total_requisitions_owned >= 5
),
composite AS (
  SELECT *,
    ROUND(0.30 * hire_rate_score + 0.25 * days_score + 0.25 * experience_score + 0.20 * feedback_score, 2) AS composite_score
  FROM score_components
)
SELECT performance_tier, COUNT(*) AS manager_count, 
  ROUND(AVG(composite_score),2) AS avg_score,
  MIN(composite_score) AS min_score,
  MAX(composite_score) AS max_score
FROM (
  SELECT *,
    CASE WHEN composite_score >= 80 THEN 'Excellent'
         WHEN composite_score >= 60 THEN 'Good'
         ELSE 'Needs Improvement' END AS performance_tier
  FROM composite
) t
GROUP BY performance_tier
ORDER BY avg_score DESC
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-072/attempt-01/sql/S9.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-072/attempt-01/sql/S9.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-072/attempt-01/results/S9.rows.jsonl)；完整：True；SHA256：`cd8d7612bf334b2cb9b33a8b1a1fb810752a5d9db91b6c9e7a4ca84da9216cc4`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "lever__hiring_manager_scorecard", "kind": "base", "block": null, "base_tables": ["lever__hiring_manager_scorecard"]}] | [] | [] |
| B2 | [{"alias": "score_components", "kind": "derived", "block": "B1", "base_tables": ["lever__hiring_manager_scorecard"]}] | [] | [] |
| B3 | [{"alias": "composite", "kind": "derived", "block": "B2", "base_tables": ["lever__hiring_manager_scorecard"]}] | [] | [] |
| B4 | [{"alias": "t", "kind": "derived", "block": "B3", "base_tables": ["lever__hiring_manager_scorecard"]}] | [] | ["performance_tier"] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B4 | COUNT(*) | [] | [] | True |
| B4 | MIN(composite_score) | [{"table": "lever__hiring_manager_scorecard", "column": "feedback_completion_rate_managed"}, {"table": "lever__hiring_manager_scorecard", "column": "avg_candidate_experience_score"}, {"table": "lever__hiring_manager_scorecard", "column": "candidate_hire_rate"}, {"table": "lever__hiring_manager_scorecard", "column": "avg_total_days_to_hire"}] | [] | False |
| B4 | MAX(composite_score) | [{"table": "lever__hiring_manager_scorecard", "column": "feedback_completion_rate_managed"}, {"table": "lever__hiring_manager_scorecard", "column": "avg_candidate_experience_score"}, {"table": "lever__hiring_manager_scorecard", "column": "candidate_hire_rate"}, {"table": "lever__hiring_manager_scorecard", "column": "avg_total_days_to_hire"}] | [] | False |
| B4 | AVG(composite_score) | [{"table": "lever__hiring_manager_scorecard", "column": "feedback_completion_rate_managed"}, {"table": "lever__hiring_manager_scorecard", "column": "avg_candidate_experience_score"}, {"table": "lever__hiring_manager_scorecard", "column": "candidate_hire_rate"}, {"table": "lever__hiring_manager_scorecard", "column": "avg_total_days_to_hire"}] | [] | False |


## S10

类别 `data`；来源 `query_db`；调用 `c5c8bb6b146f46cca67308371abb3f81`；状态 `success`。

```sql
WITH score_components AS (
  SELECT
    hiring_manager_id,
    hiring_manager_name,
    total_requisitions_owned,
    candidate_hire_rate,
    avg_total_days_to_hire,
    avg_candidate_experience_score,
    feedback_completion_rate_managed,
    ROUND(candidate_hire_rate * 100, 2) AS hire_rate_score,
    CASE WHEN avg_total_days_to_hire < 45 THEN 100.0 ELSE 0.0 END AS days_score,
    CASE WHEN avg_candidate_experience_score > 3.5 THEN 100.0 ELSE 0.0 END AS experience_score,
    CASE WHEN feedback_completion_rate_managed > 85.0 THEN 100.0 ELSE 0.0 END AS feedback_score
  FROM lever__hiring_manager_scorecard
  WHERE total_requisitions_owned >= 5
),
composite AS (
  SELECT *,
    ROUND(0.30 * hire_rate_score + 0.25 * days_score + 0.25 * experience_score + 0.20 * feedback_score, 2) AS composite_score
  FROM score_components
)
SELECT performance_tier, COUNT(*) AS n,
  SUM(CASE WHEN days_score = 100 THEN 1 ELSE 0 END) AS days_met,
  SUM(CASE WHEN experience_score = 100 THEN 1 ELSE 0 END) AS exp_met,
  SUM(CASE WHEN feedback_score = 100 THEN 1 ELSE 0 END) AS feedback_met,
  ROUND(AVG(hire_rate_score),2) AS avg_hire_rate_score
FROM (
  SELECT *,
    CASE WHEN composite_score >= 80 THEN 'Excellent'
         WHEN composite_score >= 60 THEN 'Good'
         ELSE 'Needs Improvement' END AS performance_tier
  FROM composite
) t
GROUP BY performance_tier
ORDER BY n DESC
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-072/attempt-01/sql/S10.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-072/attempt-01/sql/S10.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-072/attempt-01/results/S10.rows.jsonl)；完整：True；SHA256：`afb7349dabc6b0bea8033ea3c63102699d540cd8c8e7ba2a82631288b385642b`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "lever__hiring_manager_scorecard", "kind": "base", "block": null, "base_tables": ["lever__hiring_manager_scorecard"]}] | [] | [] |
| B2 | [{"alias": "score_components", "kind": "derived", "block": "B1", "base_tables": ["lever__hiring_manager_scorecard"]}] | [] | [] |
| B3 | [{"alias": "composite", "kind": "derived", "block": "B2", "base_tables": ["lever__hiring_manager_scorecard"]}] | [] | [] |
| B4 | [{"alias": "t", "kind": "derived", "block": "B3", "base_tables": ["lever__hiring_manager_scorecard"]}] | [] | ["performance_tier"] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B4 | COUNT(*) | [] | [] | True |
| B4 | SUM(CASE WHEN days_score = 100 THEN 1 ELSE 0 END) | [] | [{"table": "lever__hiring_manager_scorecard", "column": "avg_total_days_to_hire"}] | False |
| B4 | SUM(CASE WHEN experience_score = 100 THEN 1 ELSE 0 END) | [] | [{"table": "lever__hiring_manager_scorecard", "column": "avg_candidate_experience_score"}] | False |
| B4 | SUM(CASE WHEN feedback_score = 100 THEN 1 ELSE 0 END) | [] | [{"table": "lever__hiring_manager_scorecard", "column": "feedback_completion_rate_managed"}] | False |
| B4 | AVG(hire_rate_score) | [{"table": "lever__hiring_manager_scorecard", "column": "candidate_hire_rate"}] | [] | False |


## S11

类别 `data`；来源 `query_db`；调用 `9d0b188d380f4d3c998b724c5ab8ef9e`；状态 `success`。

```sql
WITH score_components AS (
  SELECT
    hiring_manager_id,
    hiring_manager_name,
    hiring_manager_email,
    total_requisitions_owned,
    candidate_hire_rate,
    avg_total_days_to_hire,
    avg_candidate_experience_score,
    feedback_completion_rate_managed,
    ROUND(candidate_hire_rate * 100, 2) AS hire_rate_score,
    CASE WHEN avg_total_days_to_hire < 45 THEN 100.0 ELSE 0.0 END AS days_score,
    CASE WHEN avg_candidate_experience_score > 3.5 THEN 100.0 ELSE 0.0 END AS experience_score,
    CASE WHEN feedback_completion_rate_managed > 85.0 THEN 100.0 ELSE 0.0 END AS feedback_score
  FROM lever__hiring_manager_scorecard
  WHERE total_requisitions_owned >= 5
),
composite AS (
  SELECT *,
    ROUND(0.30 * hire_rate_score + 0.25 * days_score + 0.25 * experience_score + 0.20 * feedback_score, 2) AS composite_score
  FROM score_components
)
SELECT ROUND(MIN(composite_score),2) AS min_score,
       ROUND(MAX(composite_score),2) AS max_score,
       ROUND(AVG(composite_score),2) AS mean_score,
       ROUND(AVG(composite_score*composite_score) - AVG(composite_score)*AVG(composite_score), 2) AS variance,
       COUNT(*) AS total_managers
FROM composite
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-072/attempt-01/sql/S11.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-072/attempt-01/sql/S11.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-072/attempt-01/results/S11.rows.jsonl)；完整：True；SHA256：`55b9437995daa4c593f8f4913fd55f4e49b105851288ebc7fd09187653227411`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "lever__hiring_manager_scorecard", "kind": "base", "block": null, "base_tables": ["lever__hiring_manager_scorecard"]}] | [] | [] |
| B2 | [{"alias": "score_components", "kind": "derived", "block": "B1", "base_tables": ["lever__hiring_manager_scorecard"]}] | [] | [] |
| B3 | [{"alias": "composite", "kind": "derived", "block": "B2", "base_tables": ["lever__hiring_manager_scorecard"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B3 | COUNT(*) | [] | [] | True |
| B3 | MIN(composite_score) | [{"table": "lever__hiring_manager_scorecard", "column": "feedback_completion_rate_managed"}, {"table": "lever__hiring_manager_scorecard", "column": "avg_candidate_experience_score"}, {"table": "lever__hiring_manager_scorecard", "column": "candidate_hire_rate"}, {"table": "lever__hiring_manager_scorecard", "column": "avg_total_days_to_hire"}] | [] | False |
| B3 | MAX(composite_score) | [{"table": "lever__hiring_manager_scorecard", "column": "feedback_completion_rate_managed"}, {"table": "lever__hiring_manager_scorecard", "column": "avg_candidate_experience_score"}, {"table": "lever__hiring_manager_scorecard", "column": "candidate_hire_rate"}, {"table": "lever__hiring_manager_scorecard", "column": "avg_total_days_to_hire"}] | [] | False |
| B3 | AVG(composite_score) | [{"table": "lever__hiring_manager_scorecard", "column": "feedback_completion_rate_managed"}, {"table": "lever__hiring_manager_scorecard", "column": "avg_candidate_experience_score"}, {"table": "lever__hiring_manager_scorecard", "column": "candidate_hire_rate"}, {"table": "lever__hiring_manager_scorecard", "column": "avg_total_days_to_hire"}] | [] | False |
| B3 | AVG(composite_score * composite_score) | [{"table": "lever__hiring_manager_scorecard", "column": "feedback_completion_rate_managed"}, {"table": "lever__hiring_manager_scorecard", "column": "avg_candidate_experience_score"}, {"table": "lever__hiring_manager_scorecard", "column": "candidate_hire_rate"}, {"table": "lever__hiring_manager_scorecard", "column": "avg_total_days_to_hire"}, {"table": "lever__hiring_manager_scorecard", "column": "feedback_completion_rate_managed"}, {"table": "lever__hiring_manager_scorecard", "column": "avg_candidate_experience_score"}, {"table": "lever__hiring_manager_scorecard", "column": "candidate_hire_rate"}, {"table": "lever__hiring_manager_scorecard", "column": "avg_total_days_to_hire"}] | [] | False |
| B3 | AVG(composite_score) | [{"table": "lever__hiring_manager_scorecard", "column": "feedback_completion_rate_managed"}, {"table": "lever__hiring_manager_scorecard", "column": "avg_candidate_experience_score"}, {"table": "lever__hiring_manager_scorecard", "column": "candidate_hire_rate"}, {"table": "lever__hiring_manager_scorecard", "column": "avg_total_days_to_hire"}] | [] | False |
| B3 | AVG(composite_score) | [{"table": "lever__hiring_manager_scorecard", "column": "feedback_completion_rate_managed"}, {"table": "lever__hiring_manager_scorecard", "column": "avg_candidate_experience_score"}, {"table": "lever__hiring_manager_scorecard", "column": "candidate_hire_rate"}, {"table": "lever__hiring_manager_scorecard", "column": "avg_total_days_to_hire"}] | [] | False |


## S12

类别 `data`；来源 `query_db`；调用 `d763ea99ccf146ab907a5d420a274941`；状态 `success`。

```sql
WITH score_components AS (
  SELECT
    hiring_manager_id,
    hiring_manager_name,
    total_requisitions_owned,
    candidate_hire_rate,
    avg_total_days_to_hire,
    avg_candidate_experience_score,
    feedback_completion_rate_managed,
    ROUND(candidate_hire_rate * 100, 2) AS hire_rate_score,
    CASE WHEN avg_total_days_to_hire < 45 THEN 100.0 ELSE 0.0 END AS days_score,
    CASE WHEN avg_candidate_experience_score > 3.5 THEN 100.0 ELSE 0.0 END AS experience_score,
    CASE WHEN feedback_completion_rate_managed > 85.0 THEN 100.0 ELSE 0.0 END AS feedback_score
  FROM lever__hiring_manager_scorecard
  WHERE total_requisitions_owned >= 5
),
composite AS (
  SELECT *,
    ROUND(0.30 * hire_rate_score + 0.25 * days_score + 0.25 * experience_score + 0.20 * feedback_score, 2) AS composite_score
  FROM score_components
)
SELECT * FROM composite
ORDER BY composite_score DESC
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-072/attempt-01/sql/S12.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-072/attempt-01/sql/S12.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-072/attempt-01/results/S12.rows.jsonl)；完整：True；SHA256：`307b1907523b2e33448407fec0553f0921fd9d601562de083c370c6e973ae15d`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "lever__hiring_manager_scorecard", "kind": "base", "block": null, "base_tables": ["lever__hiring_manager_scorecard"]}] | [] | [] |
| B2 | [{"alias": "score_components", "kind": "derived", "block": "B1", "base_tables": ["lever__hiring_manager_scorecard"]}] | [] | [] |
| B3 | [{"alias": "composite", "kind": "derived", "block": "B2", "base_tables": ["lever__hiring_manager_scorecard"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |


## S13

类别 `data`；来源 `python`；调用 `8f557fada09245c09e395dd60c4a5865`；状态 `success`。

```sql

WITH score_components AS (
  SELECT
    hiring_manager_id,
    hiring_manager_name,
    total_requisitions_owned,
    candidate_hire_rate,
    avg_total_days_to_hire,
    avg_candidate_experience_score,
    feedback_completion_rate_managed,
    ROUND(candidate_hire_rate * 100, 2) AS hire_rate_score,
    CASE WHEN avg_total_days_to_hire < 45 THEN 100.0 ELSE 0.0 END AS days_score,
    CASE WHEN avg_candidate_experience_score > 3.5 THEN 100.0 ELSE 0.0 END AS experience_score,
    CASE WHEN feedback_completion_rate_managed > 85.0 THEN 100.0 ELSE 0.0 END AS feedback_score
  FROM lever__hiring_manager_scorecard
  WHERE total_requisitions_owned >= 5
),
composite AS (
  SELECT *,
    ROUND(0.30 * hire_rate_score + 0.25 * days_score + 0.25 * experience_score + 0.20 * feedback_score, 2) AS composite_score
  FROM score_components
)
SELECT hiring_manager_id, hiring_manager_name, total_requisitions_owned,
       hire_rate_score, days_score, experience_score, feedback_score, composite_score
FROM composite
ORDER BY composite_score DESC

```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-072/attempt-01/sql/S13.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-072/attempt-01/sql/S13.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-072/attempt-01/results/S13.rows.jsonl)；完整：True；SHA256：`9587229b64ff721d2224b95c2fc2a7b8c51531deac16f608c07885fc627def76`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "lever__hiring_manager_scorecard", "kind": "base", "block": null, "base_tables": ["lever__hiring_manager_scorecard"]}] | [] | [] |
| B2 | [{"alias": "score_components", "kind": "derived", "block": "B1", "base_tables": ["lever__hiring_manager_scorecard"]}] | [] | [] |
| B3 | [{"alias": "composite", "kind": "derived", "block": "B2", "base_tables": ["lever__hiring_manager_scorecard"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |


## S14

类别 `data`；来源 `query_db`；调用 `87128932bb1a4f23ad49e0adb8935c07`；状态 `success`。

```sql
WITH score_components AS (
  SELECT
    hiring_manager_id,
    hiring_manager_name,
    total_requisitions_owned,
    ROUND(candidate_hire_rate * 100, 2) AS hire_rate_score,
    CASE WHEN avg_total_days_to_hire < 45 THEN 100.0 ELSE 0.0 END AS days_score,
    CASE WHEN avg_candidate_experience_score > 3.5 THEN 100.0 ELSE 0.0 END AS experience_score,
    CASE WHEN feedback_completion_rate_managed > 85.0 THEN 100.0 ELSE 0.0 END AS feedback_score,
    candidate_hire_rate, avg_total_days_to_hire, avg_candidate_experience_score, feedback_completion_rate_managed
  FROM lever__hiring_manager_scorecard
  WHERE total_requisitions_owned >= 5
),
composite AS (
  SELECT *,
    ROUND(0.30 * hire_rate_score + 0.25 * days_score + 0.25 * experience_score + 0.20 * feedback_score, 2) AS composite_score
  FROM score_components
)
SELECT hiring_manager_id, hiring_manager_name, total_requisitions_owned,
       hire_rate_score, days_score, experience_score, feedback_score, composite_score
FROM composite
ORDER BY composite_score DESC
LIMIT 13
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-072/attempt-01/sql/S14.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-072/attempt-01/sql/S14.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-072/attempt-01/results/S14.rows.jsonl)；完整：True；SHA256：`7d96cdd1a92ff1b71f46773d83870ec3a54608871407759dcfa84a6ecb6cec33`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "lever__hiring_manager_scorecard", "kind": "base", "block": null, "base_tables": ["lever__hiring_manager_scorecard"]}] | [] | [] |
| B2 | [{"alias": "score_components", "kind": "derived", "block": "B1", "base_tables": ["lever__hiring_manager_scorecard"]}] | [] | [] |
| B3 | [{"alias": "composite", "kind": "derived", "block": "B2", "base_tables": ["lever__hiring_manager_scorecard"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |


## S15

类别 `data`；来源 `query_db`；调用 `7fe1d50a7d6a4521bbaec5a0ced9a25a`；状态 `success`。

```sql
WITH score_components AS (
  SELECT
    hiring_manager_id,
    hiring_manager_name,
    total_requisitions_owned,
    ROUND(candidate_hire_rate * 100, 2) AS hire_rate_score,
    CASE WHEN avg_total_days_to_hire < 45 THEN 100.0 ELSE 0.0 END AS days_score,
    CASE WHEN avg_candidate_experience_score > 3.5 THEN 100.0 ELSE 0.0 END AS experience_score,
    CASE WHEN feedback_completion_rate_managed > 85.0 THEN 100.0 ELSE 0.0 END AS feedback_score
  FROM lever__hiring_manager_scorecard
  WHERE total_requisitions_owned >= 5
),
composite AS (
  SELECT *,
    ROUND(0.30 * hire_rate_score + 0.25 * days_score + 0.25 * experience_score + 0.20 * feedback_score, 2) AS composite_score
  FROM score_components
)
SELECT hiring_manager_id, hiring_manager_name, total_requisitions_owned,
       hire_rate_score, days_score, experience_score, feedback_score, composite_score
FROM composite
ORDER BY composite_score ASC
LIMIT 5
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-072/attempt-01/sql/S15.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-072/attempt-01/sql/S15.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-072/attempt-01/results/S15.rows.jsonl)；完整：True；SHA256：`4d05a993ea1a752c5cbedb1c0f4ed77a4bf85df773ebfc074694d57015ac1170`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "lever__hiring_manager_scorecard", "kind": "base", "block": null, "base_tables": ["lever__hiring_manager_scorecard"]}] | [] | [] |
| B2 | [{"alias": "score_components", "kind": "derived", "block": "B1", "base_tables": ["lever__hiring_manager_scorecard"]}] | [] | [] |
| B3 | [{"alias": "composite", "kind": "derived", "block": "B2", "base_tables": ["lever__hiring_manager_scorecard"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |


## S16

类别 `data`；来源 `query_db`；调用 `73ea6be42a2b4f3eb32ae8cec8418c52`；状态 `success`。

```sql
WITH score_components AS (
  SELECT
    hiring_manager_id,
    ROUND(candidate_hire_rate * 100, 2) AS hire_rate_score,
    CASE WHEN avg_total_days_to_hire < 45 THEN 100.0 ELSE 0.0 END AS days_score,
    CASE WHEN avg_candidate_experience_score > 3.5 THEN 100.0 ELSE 0.0 END AS experience_score,
    CASE WHEN feedback_completion_rate_managed > 85.0 THEN 100.0 ELSE 0.0 END AS feedback_score
  FROM lever__hiring_manager_scorecard
  WHERE total_requisitions_owned >= 5
)
SELECT 
  COUNT(*) AS total,
  SUM(CASE WHEN days_score = 100 THEN 1 ELSE 0 END) AS days_met,
  SUM(CASE WHEN experience_score = 100 THEN 1 ELSE 0 END) AS exp_met,
  SUM(CASE WHEN feedback_score = 100 THEN 1 ELSE 0 END) AS feedback_met,
  SUM(CASE WHEN hire_rate_score >= 50 THEN 1 ELSE 0 END) AS hire_rate_ge50,
  SUM(CASE WHEN days_score = 100 AND experience_score = 100 AND feedback_score = 100 AND hire_rate_score >= 50 THEN 1 ELSE 0 END) AS all_four_strong,
  ROUND(AVG(hire_rate_score), 2) AS avg_hire_rate_score
FROM score_components
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-072/attempt-01/sql/S16.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-072/attempt-01/sql/S16.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-072/attempt-01/results/S16.rows.jsonl)；完整：True；SHA256：`aa6f988e6ef7ec59c48d8dcd4fac4a2b940681bf0358043266ba3152f31a3ee1`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "lever__hiring_manager_scorecard", "kind": "base", "block": null, "base_tables": ["lever__hiring_manager_scorecard"]}] | [] | [] |
| B2 | [{"alias": "score_components", "kind": "derived", "block": "B1", "base_tables": ["lever__hiring_manager_scorecard"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B2 | COUNT(*) | [] | [] | True |
| B2 | SUM(CASE WHEN days_score = 100 THEN 1 ELSE 0 END) | [] | [{"table": "lever__hiring_manager_scorecard", "column": "avg_total_days_to_hire"}] | False |
| B2 | SUM(CASE WHEN experience_score = 100 THEN 1 ELSE 0 END) | [] | [{"table": "lever__hiring_manager_scorecard", "column": "avg_candidate_experience_score"}] | False |
| B2 | SUM(CASE WHEN feedback_score = 100 THEN 1 ELSE 0 END) | [] | [{"table": "lever__hiring_manager_scorecard", "column": "feedback_completion_rate_managed"}] | False |
| B2 | SUM(CASE WHEN hire_rate_score >= 50 THEN 1 ELSE 0 END) | [] | [{"table": "lever__hiring_manager_scorecard", "column": "candidate_hire_rate"}] | False |
| B2 | SUM(CASE WHEN days_score = 100 AND experience_score = 100 AND feedback_score = 100 AND hire_rate_score >= 50 THEN 1 ELSE 0 END) | [] | [{"table": "lever__hiring_manager_scorecard", "column": "candidate_hire_rate"}, {"table": "lever__hiring_manager_scorecard", "column": "feedback_completion_rate_managed"}, {"table": "lever__hiring_manager_scorecard", "column": "avg_total_days_to_hire"}, {"table": "lever__hiring_manager_scorecard", "column": "avg_candidate_experience_score"}] | False |
| B2 | AVG(hire_rate_score) | [{"table": "lever__hiring_manager_scorecard", "column": "candidate_hire_rate"}] | [] | False |


## S17

类别 `data`；来源 `query_db`；调用 `8be6ebcdf3594b8b86d0c32c390af283`；状态 `success`。

```sql
WITH score_components AS (
  SELECT
    hiring_manager_id,
    total_requisitions_owned,
    ROUND(candidate_hire_rate * 100, 2) AS hire_rate_score,
    CASE WHEN avg_total_days_to_hire < 45 THEN 100.0 ELSE 0.0 END AS days_score,
    CASE WHEN avg_candidate_experience_score > 3.5 THEN 100.0 ELSE 0.0 END AS experience_score,
    CASE WHEN feedback_completion_rate_managed > 85.0 THEN 100.0 ELSE 0.0 END AS feedback_score
  FROM lever__hiring_manager_scorecard
  WHERE total_requisitions_owned >= 5
),
composite AS (
  SELECT *,
    ROUND(0.30 * hire_rate_score + 0.25 * days_score + 0.25 * experience_score + 0.20 * feedback_score, 2) AS composite_score
  FROM score_components
)
SELECT 
  CASE WHEN total_requisitions_owned BETWEEN 5 AND 19 THEN '5-19'
       WHEN total_requisitions_owned BETWEEN 20 AND 39 THEN '20-39'
       ELSE '40+' END AS req_bucket,
  COUNT(*) AS n,
  ROUND(AVG(composite_score), 2) AS avg_score,
  ROUND(AVG(hire_rate_score), 2) AS avg_hire_rate
FROM composite
GROUP BY req_bucket
ORDER BY req_bucket
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-072/attempt-01/sql/S17.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-072/attempt-01/sql/S17.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-072/attempt-01/results/S17.rows.jsonl)；完整：True；SHA256：`3c61b16c69095a4f1725f61556858a92fe750d48a0177f78738c60b375b0a79f`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "lever__hiring_manager_scorecard", "kind": "base", "block": null, "base_tables": ["lever__hiring_manager_scorecard"]}] | [] | [] |
| B2 | [{"alias": "score_components", "kind": "derived", "block": "B1", "base_tables": ["lever__hiring_manager_scorecard"]}] | [] | [] |
| B3 | [{"alias": "composite", "kind": "derived", "block": "B2", "base_tables": ["lever__hiring_manager_scorecard"]}] | [] | ["CASE WHEN total_requisitions_owned BETWEEN 5 AND 19 THEN '5-19' WHEN total_requisitions_owned BETWEEN 20 AND 39 THEN '20-39' ELSE '40+' END"] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B3 | COUNT(*) | [] | [] | True |
| B3 | AVG(composite_score) | [{"table": "lever__hiring_manager_scorecard", "column": "feedback_completion_rate_managed"}, {"table": "lever__hiring_manager_scorecard", "column": "avg_candidate_experience_score"}, {"table": "lever__hiring_manager_scorecard", "column": "candidate_hire_rate"}, {"table": "lever__hiring_manager_scorecard", "column": "avg_total_days_to_hire"}] | [] | False |
| B3 | AVG(hire_rate_score) | [{"table": "lever__hiring_manager_scorecard", "column": "candidate_hire_rate"}] | [] | False |


## S18

类别 `data`；来源 `query_db`；调用 `fefa0f5daec34986aa11dd84ee9d0c10`；状态 `success`。

```sql
WITH score_components AS (
  SELECT
    hiring_manager_id,
    hiring_manager_name,
    total_requisitions_owned,
    ROUND(candidate_hire_rate * 100, 2) AS hire_rate_score,
    CASE WHEN avg_total_days_to_hire < 45 THEN 100.0 ELSE 0.0 END AS days_score,
    CASE WHEN avg_candidate_experience_score > 3.5 THEN 100.0 ELSE 0.0 END AS experience_score,
    CASE WHEN feedback_completion_rate_managed > 85.0 THEN 100.0 ELSE 0.0 END AS feedback_score
  FROM lever__hiring_manager_scorecard
  WHERE total_requisitions_owned >= 5
),
composite AS (
  SELECT *,
    ROUND(0.30 * hire_rate_score + 0.25 * days_score + 0.25 * experience_score + 0.20 * feedback_score, 2) AS composite_score
  FROM score_components
)
SELECT hiring_manager_name, total_requisitions_owned, hire_rate_score, 
       days_score, experience_score, feedback_score, composite_score
FROM composite
WHERE composite_score >= 60 AND composite_score < 80
ORDER BY composite_score DESC
LIMIT 10
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-072/attempt-01/sql/S18.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-072/attempt-01/sql/S18.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-072/attempt-01/results/S18.rows.jsonl)；完整：True；SHA256：`fea82d3e55bce53d9c496552a50f65ec98500e65da5068cd2a158f62a0cc1446`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "lever__hiring_manager_scorecard", "kind": "base", "block": null, "base_tables": ["lever__hiring_manager_scorecard"]}] | [] | [] |
| B2 | [{"alias": "score_components", "kind": "derived", "block": "B1", "base_tables": ["lever__hiring_manager_scorecard"]}] | [] | [] |
| B3 | [{"alias": "composite", "kind": "derived", "block": "B2", "base_tables": ["lever__hiring_manager_scorecard"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |

