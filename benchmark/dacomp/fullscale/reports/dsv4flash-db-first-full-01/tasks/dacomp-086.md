# dacomp-086

We need to build a customer health score model to predict churn risk and formulate operati…

运行：已提交。官方未评分。全部 SQL 尝试/成功 18/17；数据 SQL 16/15；Python 11 次。

完整原题：

We need to build a customer health score model to predict churn risk and formulate operational strategies. Please calculate a health score from 0-100 for each account based on dimensions such as last activity time, contact completeness, business value, industry type, and customer size. The weights are as follows: activity accounts for 40% (based on `days_since_last_activity` and `total_activities_30d`), contact quality for 30% (based on the `contacts_with_email`/`total_contacts` ratio), business value for 20% (based on `annual_revenue` and `total_won_amount`), and account scale for 10% (based on `account_size_segment` and `number_of_employees`). The output must include three core analyses: (1) Construct a customer risk warning matrix, cross-analyzing by industry and size, to identify high-risk customer segments with a health score below 50 and analyze their common characteristics; (2) Build a revenue contribution prediction model, based on the health score, historical won amount, and current pipeline value, to predict the potential revenue contribution of each customer over the next 6 months, and tier customers based on this contribution; (3) Design differentiated customer success strategies, proposing specific customer retention, expansion, and recovery action plans for different health score ranges (80+ High Health, 50-79 Medium, <50 Low Health) and different company sizes.

| 表 | 行数 | 列数 |
| --- | --- | --- |
| salesforce__contact_enhanced | 25000 | 55 |
| salesforce__customer_360_view | 10000 | 54 |
| salesforce__daily_activity | 2090 | 12 |
| salesforce__opportunity_enhanced | 20000 | 65 |


实际路线（分析者依据 SQL/源码概括，不代表 Agent 自述）：SQL 提取客户健康与商业字段 → Python 评分、收入情景及分层聚合 → 风险矩阵和客户成功建议。

数据库大小：33,095,680 字节。

## 数据 SQL

| SQL | 状态 | 基础表 | Join 输入/类型 | GROUP BY | 聚合表达式 | 结果行数 | 数据库 ms |
| --- | --- | --- | --- | --- | --- | --- | --- |
| [S3/Q1](#s3) | success | ["salesforce__customer_360_view"] | 0 / {} | [] | ["COUNT(*)"] | 1 | 2.675 |
| [S4/Q2](#s4) | success | ["salesforce__customer_360_view"] | 0 / {} | [] | [] | 5 | 0.483 |
| [S5/Q3](#s5) | success | ["salesforce__customer_360_view"] | 0 / {} | [] | ["COUNT(*)", "MIN(days_since_last_activity)", "MAX(days_since_last_activity)", "MIN(total_activities_30d)", "MAX(total_activities_30d)", "MIN(total_contacts)", "MAX(total_contacts)", "MIN(contacts_with_email)", "MAX(contacts_with_email)", "MIN(annual_revenue)", "MAX(annual_revenue)", "MIN(total_won_amount)", "MAX(total_won_amount)", "MIN(number_of_employees)", "MAX(number_of_employees)", "MIN(current_pipeline_amount)", "MAX(current_pipeline_amount)"] | 1 | 8.408 |
| [S6/Q4](#s6) | success | ["salesforce__customer_360_view"] | 0 / {} | ["industry_normalized"] | ["COUNT(*)"] | 6 | 4.454 |
| [S7/Q5](#s7) | success | ["salesforce__customer_360_view"] | 0 / {} | ["account_size_segment"] | ["COUNT(*)"] | 4 | 4.031 |
| [S8/Q6](#s8) | failed | ["salesforce__customer_360_view"] | 0 / {} | [] | [] | unknown | 未取得；调用总时长 0.166 ms |
| [S9/Q7](#s9) | success | ["salesforce__customer_360_view"] | 0 / {} | [] | [] | 20 | 0.347 |
| [S10/Q8](#s10) | success | ["salesforce__customer_360_view"] | 0 / {} | [] | ["MIN(contacts_with_email * 1.0 / NULLIF(total_contacts, 0))", "MAX(contacts_with_email * 1.0 / NULLIF(total_contacts, 0))", "AVG(contacts_with_email * 1.0 / NULLIF(total_contacts, 0))"] | 1 | 4.984 |
| [S11/Q9](#s11) | success | ["salesforce__customer_360_view"] | 0 / {} | [] | [] | 10000 | 29.707 |
| [S12/Q10](#s12) | success | ["salesforce__customer_360_view"] | 0 / {} | [] | [] | 10000 | 25.963 |
| [S13/Q11](#s13) | success | ["salesforce__customer_360_view"] | 0 / {} | [] | [] | 20 | 0.747 |
| [S14/Q12](#s14) | success | ["salesforce__customer_360_view"] | 0 / {} | [] | [] | 10000 | 70.317 |
| [S15/Q13](#s15) | success | ["salesforce__customer_360_view"] | 0 / {} | [] | [] | 10000 | 73.725 |
| [S16/Q14](#s16) | success | ["salesforce__customer_360_view"] | 0 / {} | [] | [] | 10000 | 70.052 |
| [S17/Q15](#s17) | success | ["salesforce__customer_360_view"] | 0 / {} | [] | [] | 10000 | 69.326 |
| [S18/Q16](#s18) | success | ["salesforce__customer_360_view"] | 0 / {} | ["industry_normalized", "account_size_segment"] | ["COUNT(*)", "AVG(health_score)", "MIN(health_score)", "MAX(health_score)"] | 19 | 67.536 |


## 元数据和设置

| SQL | 类别 | 状态 | 内容 |
| --- | --- | --- | --- |
| S1 | connection_setup | success | PRAGMA query_only=ON |
| S2 | metadata | success | SELECT name,sql FROM sqlite_master WHERE type='table' ORDER BY name |


## Python 与执行位置

人工源码审查：**database_first_violation**。Python 按健康及收入层级计算数量、均值、总收入与贡献份额，并进行健康阈值计数及管道风险求和。这些常规聚合和条件算术可在 SQL 内完成；分位数及图形渲染单独评价。 [证据](../reviews/dacomp-086.json)。

P1：SQLite lacks percentile/quantile functions. Need to compute distributions of key variables for health score normalization.

[源码](../../../runs/dsv4flash-db-first-full-01/dacomp-086/attempt-01/python/P1.py)；[输出](../../../runs/dsv4flash-db-first-full-01/dacomp-086/attempt-01/python/P1.stdout)；[错误](../../../runs/dsv4flash-db-first-full-01/dacomp-086/attempt-01/python/P1.stderr)。检出需人工核验的 SQL 可实现操作：.query(；不能仅凭理由判为合规。

P2：SQLite lacks quantile functions; need these distribution stats to calibrate sensible 0-100 normalization for each health-score dimension.

[源码](../../../runs/dsv4flash-db-first-full-01/dacomp-086/attempt-01/python/P2.py)；[输出](../../../runs/dsv4flash-db-first-full-01/dacomp-086/attempt-01/python/P2.stdout)；[错误](../../../runs/dsv4flash-db-first-full-01/dacomp-086/attempt-01/python/P2.stderr)。检出需人工核验的 SQL 可实现操作：.query(；不能仅凭理由判为合规。

P3：Compute health-score distribution, percentiles, low-health counts, and cross-tabulations. SQLite can't easily do percentiles or crosstabs with formatting.

[源码](../../../runs/dsv4flash-db-first-full-01/dacomp-086/attempt-01/python/P3.py)；[输出](../../../runs/dsv4flash-db-first-full-01/dacomp-086/attempt-01/python/P3.stdout)；[错误](../../../runs/dsv4flash-db-first-full-01/dacomp-086/attempt-01/python/P3.stderr)。检出需人工核验的 SQL 可实现操作：groupby(, .query(；不能仅凭理由判为合规。

P4：Investigate why Education/Retail health scores behave unusually; check industry-size interactions in SQL-computed scores using pandas crosstabs.

[源码](../../../runs/dsv4flash-db-first-full-01/dacomp-086/attempt-01/python/P4.py)；[输出](../../../runs/dsv4flash-db-first-full-01/dacomp-086/attempt-01/python/P4.stdout)；[错误](../../../runs/dsv4flash-db-first-full-01/dacomp-086/attempt-01/python/P4.stderr)。检出需人工核验的 SQL 可实现操作：.query(；不能仅凭理由判为合规。

P5：Compute all three analyses: risk warning matrix, revenue prediction model, differentiated strategies. Use pandas for crosstabs, quantiles, and visualizations not supported by SQLite.

[源码](../../../runs/dsv4flash-db-first-full-01/dacomp-086/attempt-01/python/P5.py)；[输出](../../../runs/dsv4flash-db-first-full-01/dacomp-086/attempt-01/python/P5.stdout)；[错误](../../../runs/dsv4flash-db-first-full-01/dacomp-086/attempt-01/python/P5.stderr)。检出需人工核验的 SQL 可实现操作：groupby(, .query(；不能仅凭理由判为合规。

P6：Full execution of all three analyses with corrected heatmap handling; revenue model and strategy metrics computed in pandas since they involve quantiles, crosstabs, and plotting not supported by SQLite.

[源码](../../../runs/dsv4flash-db-first-full-01/dacomp-086/attempt-01/python/P6.py)；[输出](../../../runs/dsv4flash-db-first-full-01/dacomp-086/attempt-01/python/P6.stdout)；[错误](../../../runs/dsv4flash-db-first-full-01/dacomp-086/attempt-01/python/P6.stderr)。检出需人工核验的 SQL 可实现操作：groupby(, .query(；不能仅凭理由判为合规。

P7：Create strategy matrix figure and compute risk/revenue concentration tables for the report (pandas-only cross-tab formatting).

[源码](../../../runs/dsv4flash-db-first-full-01/dacomp-086/attempt-01/python/P7.py)；[输出](../../../runs/dsv4flash-db-first-full-01/dacomp-086/attempt-01/python/P7.stdout)；[错误](../../../runs/dsv4flash-db-first-full-01/dacomp-086/attempt-01/python/P7.stderr)。检出需人工核验的 SQL 可实现操作：groupby(；不能仅凭理由判为合规。

P8：Resolve the discrepancy between pd.cut category counts and strict <50 counts around boundary values for accurate reporting.

[源码](../../../runs/dsv4flash-db-first-full-01/dacomp-086/attempt-01/python/P8.py)；[输出](../../../runs/dsv4flash-db-first-full-01/dacomp-086/attempt-01/python/P8.stdout)；[错误](../../../runs/dsv4flash-db-first-full-01/dacomp-086/attempt-01/python/P8.stderr)。自动源码筛查未检出预设迁出信号；这不是全面语义合规证明。

P9：Compute revenue tier thresholds, model component decomposition, and top accounts for the report narrative.

[源码](../../../runs/dsv4flash-db-first-full-01/dacomp-086/attempt-01/python/P9.py)；[输出](../../../runs/dsv4flash-db-first-full-01/dacomp-086/attempt-01/python/P9.stdout)；[错误](../../../runs/dsv4flash-db-first-full-01/dacomp-086/attempt-01/python/P9.stderr)。自动源码筛查未检出预设迁出信号；这不是全面语义合规证明。

P10：Complete the revenue model decomposition and risk-concentration numbers that were interrupted by a missing numpy import.

[源码](../../../runs/dsv4flash-db-first-full-01/dacomp-086/attempt-01/python/P10.py)；[输出](../../../runs/dsv4flash-db-first-full-01/dacomp-086/attempt-01/python/P10.stdout)；[错误](../../../runs/dsv4flash-db-first-full-01/dacomp-086/attempt-01/python/P10.stderr)。自动源码筛查未检出预设迁出信号；这不是全面语义合规证明。

P11：Find where the generated figures were saved so they can be referenced correctly in the report.

[源码](../../../runs/dsv4flash-db-first-full-01/dacomp-086/attempt-01/python/P11.py)；[输出](../../../runs/dsv4flash-db-first-full-01/dacomp-086/attempt-01/python/P11.stdout)；[错误](../../../runs/dsv4flash-db-first-full-01/dacomp-086/attempt-01/python/P11.stderr)。自动源码筛查未检出预设迁出信号；这不是全面语义合规证明。

## 优化机会

已验证候选。筛选限于精确 SQL、相同自包含 CTE、相同单表完整过滤、可分解单表聚合；未覆盖任意 Join 等价和一般谓词蕴含。全部候选都是 offline，未测在线预测。

| 候选 | 类型 | 已有结果 | 覆盖 SQL | 后续次数 | 中间行数 | 验证 | 成本 |
| --- | --- | --- | --- | --- | --- | --- | --- |
| C1 | exact-result reuse | True | ["S14", "S15", "S16", "S17"] | 3 | 10000 | verified | Not benchmarked; correctness alone does not establish net speedup. |
| C2 | common subexpression | False | ["S14", "S15", "S16", "S17"] | 3 | 10000 | verified | Not benchmarked; correctness alone does not establish net speedup. |
| C3 | aggregate MV | False | ["S3", "S5", "S6", "S7", "S10"] | 4 | 19 | rejected_result_mismatch | Not benchmarked; correctness alone does not establish net speedup. |


已验证覆盖（含触发查询、候选并集去重）：4/15 条成功数据 SQL。正确性仅针对当前数据库快照；未测性能的候选不能声称已加速。

[完整 build/rewrite 与比较证据](dacomp-086.analysis.json)。

### C1：exact-result reuse

Identical normalized SQL and parameters; archive equality checked.

原查询 [S14](#s14), [S15](#s15), [S16](#s16), [S17](#s17) → 保留前序结果 S14 → 后续 3 次可复用。该构建点为事后假设，不代表 Agent 当时预知后续。

| 原 SQL | 列名一致 | 结果一致 | 比较方法 |
| --- | --- | --- | --- |
| S15 | True | True | exact_multiset |
| S16 | True | True | exact_multiset |
| S17 | True | True | exact_multiset |


验证状态：verified；成本结论：Not benchmarked; correctness alone does not establish net speedup.

### C2：common subexpression

Identical self-contained CTE body across queries.

原查询 [S14](#s14), [S15](#s15), [S16](#s16), [S17](#s17) → 新增共享状态 C2 → 后续 3 次可复用。该构建点为事后假设，不代表 Agent 当时预知后续。

构建定义：

```sql
SELECT account_id, account_name, industry_normalized, account_size_segment, number_of_employees, annual_revenue, total_won_amount, current_pipeline_amount, win_rate_percentage, account_age_days, total_contacts, contacts_with_email, days_since_last_activity, total_activities_30d, ROUND(0.5 * MAX(0, 100 - days_since_last_activity * 1.667) + 0.5 * MIN(100, total_activities_30d * 1.667), 2) AS activity_score, ROUND(contacts_with_email * 100.0 / NULLIF(total_contacts, 0), 2) AS contact_score, ROUND(0.5 * MAX(0, MIN(100, (LOG(10, annual_revenue) - 6) * 25)) + 0.5 * MIN(100, LOG(10, total_won_amount + 1) * 100.0 / 9), 2) AS value_score, ROUND(0.5 * CASE account_size_segment WHEN 'Small Business' THEN 25 WHEN 'Mid-Market' THEN 50 WHEN 'Large' THEN 75 WHEN 'Enterprise' THEN 100 ELSE 50 END + 0.5 * MAX(0, MIN(100, (LOG(10, number_of_employees) - 1.114) * 100.0 / 3.586)), 2) AS scale_score FROM salesforce__customer_360_view
```

受益查询 S14 的改写示例：

```sql
WITH scores AS (SELECT * FROM temp.reuse_candidate) SELECT *, ROUND(0.4 * activity_score + 0.3 * contact_score + 0.2 * value_score + 0.1 * scale_score, 1) AS health_score FROM scores
```

| 原 SQL | 列名一致 | 结果一致 | 比较方法 |
| --- | --- | --- | --- |
| S14 | True | True | exact_multiset |
| S15 | True | True | exact_multiset |
| S16 | True | True | exact_multiset |
| S17 | True | True | exact_multiset |


验证状态：verified；成本结论：Not benchmarked; correctness alone does not establish net speedup.

### C3：aggregate MV

Union of grouping keys; decomposable aggregate states; AVG uses SUM and non-NULL COUNT.

原查询 [S3](#s3), [S5](#s5), [S6](#s6), [S7](#s7), [S10](#s10) → 新增共享状态 C3 → 后续 4 次可复用。该构建点为事后假设，不代表 Agent 当时预知后续。

构建定义：

```sql
SELECT industry_normalized AS __g0, account_size_segment AS __g1, COUNT(*) AS __a0, MIN(days_since_last_activity) AS __a1, MAX(days_since_last_activity) AS __a2, MIN(total_activities_30d) AS __a3, MAX(total_activities_30d) AS __a4, MIN(total_contacts) AS __a5, MAX(total_contacts) AS __a6, MIN(contacts_with_email) AS __a7, MAX(contacts_with_email) AS __a8, MIN(annual_revenue) AS __a9, MAX(annual_revenue) AS __a10, MIN(total_won_amount) AS __a11, MAX(total_won_amount) AS __a12, MIN(number_of_employees) AS __a13, MAX(number_of_employees) AS __a14, MIN(current_pipeline_amount) AS __a15, MAX(current_pipeline_amount) AS __a16, MIN(contacts_with_email * 1.0 / NULLIF(total_contacts, 0)) AS __a17, MAX(contacts_with_email * 1.0 / NULLIF(total_contacts, 0)) AS __a18, SUM(contacts_with_email * 1.0 / NULLIF(total_contacts, 0)) AS __a19_sum, COUNT(contacts_with_email * 1.0 / NULLIF(total_contacts, 0)) AS __a19_n FROM "salesforce__customer_360_view"  GROUP BY industry_normalized, account_size_segment
```

受益查询 S3 的改写示例：

```sql
SELECT SUM(__a0) AS cnt FROM temp.reuse_candidate
```

| 原 SQL | 列名一致 | 结果一致 | 比较方法 |
| --- | --- | --- | --- |
| S3 | True | True | exact_multiset |
| S5 | True | True | exact_multiset |
| S6 | True | True | ordered_numeric_tolerance |
| S7 | True | True | ordered_numeric_tolerance |
| S10 | True | False | exact_multiset |


验证状态：rejected_result_mismatch；成本结论：Not benchmarked; correctness alone does not establish net speedup.

结果依赖：自动记录 SQL→Python 的接口父调用，以及源码中引用归档文件的消费者；字面值相同不认定因果。模型方向选择需要人工读取消息，尚未做全面因果标注。

[原始报告](../../../runs/dsv4flash-db-first-full-01/dacomp-086/attempt-01/answer.md)；[统一消息](../../../runs/dsv4flash-db-first-full-01/dacomp-086/attempt-01/messages.jsonl)；[原始 OpenCode 事件](../../../runs/dsv4flash-db-first-full-01/dacomp-086/attempt-01/opencode.jsonl)；[SQL 引擎日志](../../../runs/dsv4flash-db-first-full-01/dacomp-086/attempt-01/sql_journal.jsonl)。

[可读报告（本地图片链接规范化）](../answers/dacomp-086.md)。原始回答保留，分析结论未改写。

## S1

类别 `connection_setup`；来源 `connection`；调用 `8e85909d2f7d48f794377fabecc9a0a9`；状态 `success`。

```sql
PRAGMA query_only=ON
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-086/attempt-01/sql/S1.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-086/attempt-01/sql/S1.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-086/attempt-01/results/S1.rows.jsonl)；完整：True；SHA256：`e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`。

## S2

类别 `metadata`；来源 `list_db`；调用 `8e85909d2f7d48f794377fabecc9a0a9`；状态 `success`。

```sql
SELECT name,sql FROM sqlite_master WHERE type='table' ORDER BY name
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-086/attempt-01/sql/S2.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-086/attempt-01/sql/S2.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-086/attempt-01/results/S2.rows.jsonl)；完整：True；SHA256：`4a3cb6c16c0d90da1a4611893eb1215097051174af64f382d61391f166b4d4f7`。

## S3

类别 `data`；来源 `query_db`；调用 `2b21a86bb9cc4dd7b779fd92915f221f`；状态 `success`。

```sql
SELECT COUNT(*) AS cnt FROM salesforce__customer_360_view
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-086/attempt-01/sql/S3.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-086/attempt-01/sql/S3.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-086/attempt-01/results/S3.rows.jsonl)；完整：True；SHA256：`aa6d6ae6ca30e188ae245d117135dedb1eec9e98797ddc3dad4f9cec745e2f6d`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "salesforce__customer_360_view", "kind": "base", "block": null, "base_tables": ["salesforce__customer_360_view"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |


## S4

类别 `data`；来源 `query_db`；调用 `3817bac8390646369b1f026c45281d70`；状态 `success`。

```sql
SELECT * FROM salesforce__customer_360_view LIMIT 5
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-086/attempt-01/sql/S4.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-086/attempt-01/sql/S4.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-086/attempt-01/results/S4.rows.jsonl)；完整：True；SHA256：`ff06344123b5b374967ac3059d24d4d01e0ce76c7b2da6184aa286441711c5ac`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "salesforce__customer_360_view", "kind": "base", "block": null, "base_tables": ["salesforce__customer_360_view"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |


## S5

类别 `data`；来源 `query_db`；调用 `0c829d5b2ad04e63b14760ca1918c987`；状态 `success`。

```sql
SELECT 
  COUNT(*) AS n,
  MIN(days_since_last_activity) AS min_days, MAX(days_since_last_activity) AS max_days,
  MIN(total_activities_30d) AS min_act30, MAX(total_activities_30d) AS max_act30,
  MIN(total_contacts) AS min_tc, MAX(total_contacts) AS max_tc,
  MIN(contacts_with_email) AS min_ce, MAX(contacts_with_email) AS max_ce,
  MIN(annual_revenue) AS min_rev, MAX(annual_revenue) AS max_rev,
  MIN(total_won_amount) AS min_won, MAX(total_won_amount) AS max_won,
  MIN(number_of_employees) AS min_emp, MAX(number_of_employees) AS max_emp,
  MIN(current_pipeline_amount) AS min_pipe, MAX(current_pipeline_amount) AS max_pipe
FROM salesforce__customer_360_view
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-086/attempt-01/sql/S5.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-086/attempt-01/sql/S5.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-086/attempt-01/results/S5.rows.jsonl)；完整：True；SHA256：`c779ccff8b11ebeb3b6f376a15cd57a79612f7511f03f8e01b5fd7037c57a595`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "salesforce__customer_360_view", "kind": "base", "block": null, "base_tables": ["salesforce__customer_360_view"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |
| B1 | MIN(days_since_last_activity) | [{"table": "salesforce__customer_360_view", "column": "days_since_last_activity"}] | [] | False |
| B1 | MAX(days_since_last_activity) | [{"table": "salesforce__customer_360_view", "column": "days_since_last_activity"}] | [] | False |
| B1 | MIN(total_activities_30d) | [{"table": "salesforce__customer_360_view", "column": "total_activities_30d"}] | [] | False |
| B1 | MAX(total_activities_30d) | [{"table": "salesforce__customer_360_view", "column": "total_activities_30d"}] | [] | False |
| B1 | MIN(total_contacts) | [{"table": "salesforce__customer_360_view", "column": "total_contacts"}] | [] | False |
| B1 | MAX(total_contacts) | [{"table": "salesforce__customer_360_view", "column": "total_contacts"}] | [] | False |
| B1 | MIN(contacts_with_email) | [{"table": "salesforce__customer_360_view", "column": "contacts_with_email"}] | [] | False |
| B1 | MAX(contacts_with_email) | [{"table": "salesforce__customer_360_view", "column": "contacts_with_email"}] | [] | False |
| B1 | MIN(annual_revenue) | [{"table": "salesforce__customer_360_view", "column": "annual_revenue"}] | [] | False |
| B1 | MAX(annual_revenue) | [{"table": "salesforce__customer_360_view", "column": "annual_revenue"}] | [] | False |
| B1 | MIN(total_won_amount) | [{"table": "salesforce__customer_360_view", "column": "total_won_amount"}] | [] | False |
| B1 | MAX(total_won_amount) | [{"table": "salesforce__customer_360_view", "column": "total_won_amount"}] | [] | False |
| B1 | MIN(number_of_employees) | [{"table": "salesforce__customer_360_view", "column": "number_of_employees"}] | [] | False |
| B1 | MAX(number_of_employees) | [{"table": "salesforce__customer_360_view", "column": "number_of_employees"}] | [] | False |
| B1 | MIN(current_pipeline_amount) | [{"table": "salesforce__customer_360_view", "column": "current_pipeline_amount"}] | [] | False |
| B1 | MAX(current_pipeline_amount) | [{"table": "salesforce__customer_360_view", "column": "current_pipeline_amount"}] | [] | False |


## S6

类别 `data`；来源 `query_db`；调用 `6f680f91020a4e92ab52d6d15007281c`；状态 `success`。

```sql
SELECT industry_normalized, COUNT(*) AS n FROM salesforce__customer_360_view GROUP BY industry_normalized ORDER BY n DESC
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-086/attempt-01/sql/S6.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-086/attempt-01/sql/S6.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-086/attempt-01/results/S6.rows.jsonl)；完整：True；SHA256：`8cea5215004dd1ed1c7e926422312fe0d93cc7f03c60865f8f041b19cd3e0f50`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "salesforce__customer_360_view", "kind": "base", "block": null, "base_tables": ["salesforce__customer_360_view"]}] | [] | ["industry_normalized"] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |


## S7

类别 `data`；来源 `query_db`；调用 `175391973168412baa33405999df0392`；状态 `success`。

```sql
SELECT account_size_segment, COUNT(*) AS n FROM salesforce__customer_360_view GROUP BY account_size_segment ORDER BY n DESC
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-086/attempt-01/sql/S7.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-086/attempt-01/sql/S7.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-086/attempt-01/results/S7.rows.jsonl)；完整：True；SHA256：`aa3171fc13acb4e7e59a0e72a0071d610b433b3786b7d85bd6c7e5b3866c8e22`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "salesforce__customer_360_view", "kind": "base", "block": null, "base_tables": ["salesforce__customer_360_view"]}] | [] | ["account_size_segment"] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |


## S8

类别 `data`；来源 `query_db`；调用 `4d9146ccc335483cb673ac15d8c978ef`；状态 `failed`。

```sql
SELECT 
  PERCENTILE_25(days_since_last_activity) AS p25_days,
  PERCENTILE_50(days_since_last_activity) AS p50_days,
  PERCENTILE_75(days_since_last_activity) AS p75_days,
  PERCENTILE_25(total_activities_30d) AS p25_act,
  PERCENTILE_50(total_activities_30d) AS p50_act,
  PERCENTILE_75(total_activities_30d) AS p75_act,
  PERCENTILE_25(annual_revenue) AS p25_rev,
  PERCENTILE_50(annual_revenue) AS p50_rev,
  PERCENTILE_75(annual_revenue) AS p75_rev,
  PERCENTILE_25(total_won_amount) AS p25_won,
  PERCENTILE_50(total_won_amount) AS p50_won,
  PERCENTILE_75(total_won_amount) AS p75_won
FROM salesforce__customer_360_view
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-086/attempt-01/sql/S8.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-086/attempt-01/sql/S8.parameters.json)。

错误：`OperationalError('no such function: PERCENTILE_25')`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "salesforce__customer_360_view", "kind": "base", "block": null, "base_tables": ["salesforce__customer_360_view"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |


## S9

类别 `data`；来源 `query_db`；调用 `02c72c1d89504366b0794fb8e403d4ee`；状态 `success`。

```sql
SELECT 
  contacts_with_email * 1.0 / NULLIF(total_contacts, 0) AS contact_email_ratio
FROM salesforce__customer_360_view 
LIMIT 20
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-086/attempt-01/sql/S9.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-086/attempt-01/sql/S9.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-086/attempt-01/results/S9.rows.jsonl)；完整：True；SHA256：`4e11b3fe361103483257325e9c0a2e41df87f6e3a2dc1fb2eec6c283f47929c3`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "salesforce__customer_360_view", "kind": "base", "block": null, "base_tables": ["salesforce__customer_360_view"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |


## S10

类别 `data`；来源 `query_db`；调用 `b8732b4958784529878ef5979839e70b`；状态 `success`。

```sql
SELECT 
  MIN(contacts_with_email * 1.0 / NULLIF(total_contacts, 0)) AS min_ratio,
  MAX(contacts_with_email * 1.0 / NULLIF(total_contacts, 0)) AS max_ratio,
  AVG(contacts_with_email * 1.0 / NULLIF(total_contacts, 0)) AS avg_ratio
FROM salesforce__customer_360_view
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-086/attempt-01/sql/S10.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-086/attempt-01/sql/S10.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-086/attempt-01/results/S10.rows.jsonl)；完整：True；SHA256：`4582e433e3541036be20ef1517d0e88843ba6773de902f9bd0cfe8b367a7c413`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "salesforce__customer_360_view", "kind": "base", "block": null, "base_tables": ["salesforce__customer_360_view"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | MIN(contacts_with_email * 1.0 / NULLIF(total_contacts, 0)) | [{"table": "salesforce__customer_360_view", "column": "contacts_with_email"}, {"table": "salesforce__customer_360_view", "column": "total_contacts"}] | [] | False |
| B1 | MAX(contacts_with_email * 1.0 / NULLIF(total_contacts, 0)) | [{"table": "salesforce__customer_360_view", "column": "contacts_with_email"}, {"table": "salesforce__customer_360_view", "column": "total_contacts"}] | [] | False |
| B1 | AVG(contacts_with_email * 1.0 / NULLIF(total_contacts, 0)) | [{"table": "salesforce__customer_360_view", "column": "contacts_with_email"}, {"table": "salesforce__customer_360_view", "column": "total_contacts"}] | [] | False |


## S11

类别 `data`；来源 `python`；调用 `9b10ec55f6d64d4eb6eca6b6198983f5`；状态 `success`。

```sql
SELECT account_id, days_since_last_activity, total_activities_30d, total_contacts, contacts_with_email, annual_revenue, total_won_amount, account_size_segment, number_of_employees, industry_normalized, current_pipeline_amount, customer_health_score, churn_risk_level, account_name, account_type FROM salesforce__customer_360_view
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-086/attempt-01/sql/S11.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-086/attempt-01/sql/S11.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-086/attempt-01/results/S11.rows.jsonl)；完整：True；SHA256：`a8a357399ab0270cac5a00473cbe02a49ca64fb903a73e475027afec63a8e90a`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "salesforce__customer_360_view", "kind": "base", "block": null, "base_tables": ["salesforce__customer_360_view"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |


## S12

类别 `data`；来源 `python`；调用 `99955eb300ae454aabb9f1432a79f86f`；状态 `success`。

```sql
SELECT account_id, days_since_last_activity, total_activities_30d, total_contacts, contacts_with_email, annual_revenue, total_won_amount, account_size_segment, number_of_employees, account_age_days, win_rate_percentage, current_pipeline_amount, industry_normalized FROM salesforce__customer_360_view
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-086/attempt-01/sql/S12.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-086/attempt-01/sql/S12.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-086/attempt-01/results/S12.rows.jsonl)；完整：True；SHA256：`94972e067151c436a39b9f3814f9025e374516b2d93fcc6d3d75204949020e78`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "salesforce__customer_360_view", "kind": "base", "block": null, "base_tables": ["salesforce__customer_360_view"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |


## S13

类别 `data`；来源 `query_db`；调用 `42e7ce7d8dab4a769d4dd45dac041a89`；状态 `success`。

```sql
WITH scores AS (
  SELECT 
    account_id,
    account_name,
    industry_normalized,
    account_size_segment,
    number_of_employees,
    annual_revenue,
    total_won_amount,
    current_pipeline_amount,
    win_rate_percentage,
    account_age_days,
    total_contacts,
    contacts_with_email,
    days_since_last_activity,
    total_activities_30d,
    -- Activity Score (40%): 50% recency + 50% volume
    ROUND(0.5 * MAX(0, 100 - days_since_last_activity * 1.667) + 0.5 * MIN(100, total_activities_30d * 1.667), 2) AS activity_score,
    -- Contact Score (30%): email ratio * 100
    ROUND(contacts_with_email * 100.0 / NULLIF(total_contacts, 0), 2) AS contact_score,
    -- Business Value Score (20%): 50% revenue + 50% won amount
    ROUND(0.5 * MAX(0, MIN(100, (LOG10(annual_revenue) - 6) * 25)) + 0.5 * MIN(100, LOG10(total_won_amount + 1) * 100.0 / 9), 2) AS value_score,
    -- Scale Score (10%): 50% segment + 50% employees
    ROUND(0.5 * CASE account_size_segment
      WHEN 'Small Business' THEN 25
      WHEN 'Mid-Market' THEN 50
      WHEN 'Large' THEN 75
      WHEN 'Enterprise' THEN 100
      ELSE 50
    END + 0.5 * MAX(0, MIN(100, (LOG10(number_of_employees) - 1.114) * 100.0 / 3.586)), 2) AS scale_score
  FROM salesforce__customer_360_view
)
SELECT 
  account_id, account_name, industry_normalized, account_size_segment,
  activity_score, contact_score, value_score, scale_score,
  ROUND(0.4 * activity_score + 0.3 * contact_score + 0.2 * value_score + 0.1 * scale_score, 1) AS health_score
FROM scores
LIMIT 20
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-086/attempt-01/sql/S13.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-086/attempt-01/sql/S13.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-086/attempt-01/results/S13.rows.jsonl)；完整：True；SHA256：`ee3d93b18a8c12a8375efe4b641a232e5f3cc1cb0b29b7a2022bd5f9dbb095aa`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "salesforce__customer_360_view", "kind": "base", "block": null, "base_tables": ["salesforce__customer_360_view"]}] | [] | [] |
| B2 | [{"alias": "scores", "kind": "derived", "block": "B1", "base_tables": ["salesforce__customer_360_view"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |


## S14

类别 `data`；来源 `python`；调用 `16e51c9544db4a788ff0efbc1d12d9d2`；状态 `success`。

```sql

  WITH scores AS (
    SELECT 
      account_id,
      account_name,
      industry_normalized,
      account_size_segment,
      number_of_employees,
      annual_revenue,
      total_won_amount,
      current_pipeline_amount,
      win_rate_percentage,
      account_age_days,
      total_contacts,
      contacts_with_email,
      days_since_last_activity,
      total_activities_30d,
      ROUND(0.5 * MAX(0, 100 - days_since_last_activity * 1.667) + 0.5 * MIN(100, total_activities_30d * 1.667), 2) AS activity_score,
      ROUND(contacts_with_email * 100.0 / NULLIF(total_contacts, 0), 2) AS contact_score,
      ROUND(0.5 * MAX(0, MIN(100, (LOG10(annual_revenue) - 6) * 25)) + 0.5 * MIN(100, LOG10(total_won_amount + 1) * 100.0 / 9), 2) AS value_score,
      ROUND(0.5 * CASE account_size_segment
        WHEN 'Small Business' THEN 25
        WHEN 'Mid-Market' THEN 50
        WHEN 'Large' THEN 75
        WHEN 'Enterprise' THEN 100
        ELSE 50
      END + 0.5 * MAX(0, MIN(100, (LOG10(number_of_employees) - 1.114) * 100.0 / 3.586)), 2) AS scale_score
    FROM salesforce__customer_360_view
  )
  SELECT *,
    ROUND(0.4 * activity_score + 0.3 * contact_score + 0.2 * value_score + 0.1 * scale_score, 1) AS health_score
  FROM scores

```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-086/attempt-01/sql/S14.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-086/attempt-01/sql/S14.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-086/attempt-01/results/S14.rows.jsonl)；完整：True；SHA256：`6dde88be98ed7bf4f862efea44726c902172f959607fd6adff256bc27472d90d`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "salesforce__customer_360_view", "kind": "base", "block": null, "base_tables": ["salesforce__customer_360_view"]}] | [] | [] |
| B2 | [{"alias": "scores", "kind": "derived", "block": "B1", "base_tables": ["salesforce__customer_360_view"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |


## S15

类别 `data`；来源 `python`；调用 `bf4699eb9757420e80f25d908614bdbd`；状态 `success`。

```sql

  WITH scores AS (
    SELECT 
      account_id, account_name, industry_normalized, account_size_segment, number_of_employees,
      annual_revenue, total_won_amount, current_pipeline_amount, win_rate_percentage, account_age_days,
      total_contacts, contacts_with_email, days_since_last_activity, total_activities_30d,
      ROUND(0.5 * MAX(0, 100 - days_since_last_activity * 1.667) + 0.5 * MIN(100, total_activities_30d * 1.667), 2) AS activity_score,
      ROUND(contacts_with_email * 100.0 / NULLIF(total_contacts, 0), 2) AS contact_score,
      ROUND(0.5 * MAX(0, MIN(100, (LOG10(annual_revenue) - 6) * 25)) + 0.5 * MIN(100, LOG10(total_won_amount + 1) * 100.0 / 9), 2) AS value_score,
      ROUND(0.5 * CASE account_size_segment
        WHEN 'Small Business' THEN 25
        WHEN 'Mid-Market' THEN 50
        WHEN 'Large' THEN 75
        WHEN 'Enterprise' THEN 100
        ELSE 50
      END + 0.5 * MAX(0, MIN(100, (LOG10(number_of_employees) - 1.114) * 100.0 / 3.586)), 2) AS scale_score
    FROM salesforce__customer_360_view
  )
  SELECT *,
    ROUND(0.4 * activity_score + 0.3 * contact_score + 0.2 * value_score + 0.1 * scale_score, 1) AS health_score
  FROM scores

```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-086/attempt-01/sql/S15.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-086/attempt-01/sql/S15.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-086/attempt-01/results/S15.rows.jsonl)；完整：True；SHA256：`6dde88be98ed7bf4f862efea44726c902172f959607fd6adff256bc27472d90d`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "salesforce__customer_360_view", "kind": "base", "block": null, "base_tables": ["salesforce__customer_360_view"]}] | [] | [] |
| B2 | [{"alias": "scores", "kind": "derived", "block": "B1", "base_tables": ["salesforce__customer_360_view"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |


## S16

类别 `data`；来源 `python`；调用 `2cc68090933f4d9eb81adec14acedd75`；状态 `success`。

```sql

  WITH scores AS (
    SELECT 
      account_id, account_name, industry_normalized, account_size_segment, number_of_employees,
      annual_revenue, total_won_amount, current_pipeline_amount, win_rate_percentage, account_age_days,
      total_contacts, contacts_with_email, days_since_last_activity, total_activities_30d,
      ROUND(0.5 * MAX(0, 100 - days_since_last_activity * 1.667) + 0.5 * MIN(100, total_activities_30d * 1.667), 2) AS activity_score,
      ROUND(contacts_with_email * 100.0 / NULLIF(total_contacts, 0), 2) AS contact_score,
      ROUND(0.5 * MAX(0, MIN(100, (LOG10(annual_revenue) - 6) * 25)) + 0.5 * MIN(100, LOG10(total_won_amount + 1) * 100.0 / 9), 2) AS value_score,
      ROUND(0.5 * CASE account_size_segment
        WHEN 'Small Business' THEN 25
        WHEN 'Mid-Market' THEN 50
        WHEN 'Large' THEN 75
        WHEN 'Enterprise' THEN 100
        ELSE 50
      END + 0.5 * MAX(0, MIN(100, (LOG10(number_of_employees) - 1.114) * 100.0 / 3.586)), 2) AS scale_score
    FROM salesforce__customer_360_view
  )
  SELECT *,
    ROUND(0.4 * activity_score + 0.3 * contact_score + 0.2 * value_score + 0.1 * scale_score, 1) AS health_score
  FROM scores

```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-086/attempt-01/sql/S16.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-086/attempt-01/sql/S16.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-086/attempt-01/results/S16.rows.jsonl)；完整：True；SHA256：`6dde88be98ed7bf4f862efea44726c902172f959607fd6adff256bc27472d90d`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "salesforce__customer_360_view", "kind": "base", "block": null, "base_tables": ["salesforce__customer_360_view"]}] | [] | [] |
| B2 | [{"alias": "scores", "kind": "derived", "block": "B1", "base_tables": ["salesforce__customer_360_view"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |


## S17

类别 `data`；来源 `python`；调用 `057fb66d05a948e98145aedacf833d19`；状态 `success`。

```sql

  WITH scores AS (
    SELECT 
      account_id, account_name, industry_normalized, account_size_segment, number_of_employees,
      annual_revenue, total_won_amount, current_pipeline_amount, win_rate_percentage, account_age_days,
      total_contacts, contacts_with_email, days_since_last_activity, total_activities_30d,
      ROUND(0.5 * MAX(0, 100 - days_since_last_activity * 1.667) + 0.5 * MIN(100, total_activities_30d * 1.667), 2) AS activity_score,
      ROUND(contacts_with_email * 100.0 / NULLIF(total_contacts, 0), 2) AS contact_score,
      ROUND(0.5 * MAX(0, MIN(100, (LOG10(annual_revenue) - 6) * 25)) + 0.5 * MIN(100, LOG10(total_won_amount + 1) * 100.0 / 9), 2) AS value_score,
      ROUND(0.5 * CASE account_size_segment
        WHEN 'Small Business' THEN 25
        WHEN 'Mid-Market' THEN 50
        WHEN 'Large' THEN 75
        WHEN 'Enterprise' THEN 100
        ELSE 50
      END + 0.5 * MAX(0, MIN(100, (LOG10(number_of_employees) - 1.114) * 100.0 / 3.586)), 2) AS scale_score
    FROM salesforce__customer_360_view
  )
  SELECT *,
    ROUND(0.4 * activity_score + 0.3 * contact_score + 0.2 * value_score + 0.1 * scale_score, 1) AS health_score
  FROM scores

```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-086/attempt-01/sql/S17.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-086/attempt-01/sql/S17.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-086/attempt-01/results/S17.rows.jsonl)；完整：True；SHA256：`6dde88be98ed7bf4f862efea44726c902172f959607fd6adff256bc27472d90d`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "salesforce__customer_360_view", "kind": "base", "block": null, "base_tables": ["salesforce__customer_360_view"]}] | [] | [] |
| B2 | [{"alias": "scores", "kind": "derived", "block": "B1", "base_tables": ["salesforce__customer_360_view"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |


## S18

类别 `data`；来源 `query_db`；调用 `79ad1df9aa1944cebfe259be57b6f544`；状态 `success`。

```sql
SELECT industry_normalized, account_size_segment, 
       COUNT(*) AS n,
       ROUND(AVG(health_score), 1) AS avg_hs,
       ROUND(MIN(health_score), 1) AS min_hs,
       ROUND(MAX(health_score), 1) AS max_hs
FROM (
  WITH scores AS (
    SELECT 
      account_id, industry_normalized, account_size_segment, number_of_employees,
      annual_revenue, total_won_amount, total_contacts, contacts_with_email,
      days_since_last_activity, total_activities_30d,
      ROUND(0.5 * MAX(0, 100 - days_since_last_activity * 1.667) + 0.5 * MIN(100, total_activities_30d * 1.667), 2) AS activity_score,
      ROUND(contacts_with_email * 100.0 / NULLIF(total_contacts, 0), 2) AS contact_score,
      ROUND(0.5 * MAX(0, MIN(100, (LOG10(annual_revenue) - 6) * 25)) + 0.5 * MIN(100, LOG10(total_won_amount + 1) * 100.0 / 9), 2) AS value_score,
      ROUND(0.5 * CASE account_size_segment
        WHEN 'Small Business' THEN 25
        WHEN 'Mid-Market' THEN 50
        WHEN 'Large' THEN 75
        WHEN 'Enterprise' THEN 100
        ELSE 50
      END + 0.5 * MAX(0, MIN(100, (LOG10(number_of_employees) - 1.114) * 100.0 / 3.586)), 2) AS scale_score
    FROM salesforce__customer_360_view
  )
  SELECT *, ROUND(0.4 * activity_score + 0.3 * contact_score + 0.2 * value_score + 0.1 * scale_score, 1) AS health_score
  FROM scores
)
GROUP BY industry_normalized, account_size_segment
ORDER BY industry_normalized, account_size_segment
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-086/attempt-01/sql/S18.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-086/attempt-01/sql/S18.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-086/attempt-01/results/S18.rows.jsonl)；完整：True；SHA256：`0e25d0e127f1962dc5142b80155f5d2d0b2f89b207c8f4dc36a4fc9c8fabd66d`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "salesforce__customer_360_view", "kind": "base", "block": null, "base_tables": ["salesforce__customer_360_view"]}] | [] | [] |
| B2 | [{"alias": "scores", "kind": "derived", "block": "B1", "base_tables": ["salesforce__customer_360_view"]}] | [] | [] |
| B3 | [{"alias": "", "kind": "derived", "block": "B2", "base_tables": ["salesforce__customer_360_view"]}] | [] | ["industry_normalized", "account_size_segment"] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B3 | COUNT(*) | [] | [] | True |
| B3 | AVG(health_score) | [{"table": "salesforce__customer_360_view", "column": "account_size_segment"}, {"table": "salesforce__customer_360_view", "column": "number_of_employees"}, {"table": "salesforce__customer_360_view", "column": "total_won_amount"}, {"table": "salesforce__customer_360_view", "column": "annual_revenue"}, {"table": "salesforce__customer_360_view", "column": "total_activities_30d"}, {"table": "salesforce__customer_360_view", "column": "days_since_last_activity"}, {"table": "salesforce__customer_360_view", "column": "contacts_with_email"}, {"table": "salesforce__customer_360_view", "column": "total_contacts"}] | [] | False |
| B3 | MIN(health_score) | [{"table": "salesforce__customer_360_view", "column": "account_size_segment"}, {"table": "salesforce__customer_360_view", "column": "number_of_employees"}, {"table": "salesforce__customer_360_view", "column": "total_won_amount"}, {"table": "salesforce__customer_360_view", "column": "annual_revenue"}, {"table": "salesforce__customer_360_view", "column": "total_activities_30d"}, {"table": "salesforce__customer_360_view", "column": "days_since_last_activity"}, {"table": "salesforce__customer_360_view", "column": "contacts_with_email"}, {"table": "salesforce__customer_360_view", "column": "total_contacts"}] | [] | False |
| B3 | MAX(health_score) | [{"table": "salesforce__customer_360_view", "column": "account_size_segment"}, {"table": "salesforce__customer_360_view", "column": "number_of_employees"}, {"table": "salesforce__customer_360_view", "column": "total_won_amount"}, {"table": "salesforce__customer_360_view", "column": "annual_revenue"}, {"table": "salesforce__customer_360_view", "column": "total_activities_30d"}, {"table": "salesforce__customer_360_view", "column": "days_since_last_activity"}, {"table": "salesforce__customer_360_view", "column": "contacts_with_email"}, {"table": "salesforce__customer_360_view", "column": "total_contacts"}] | [] | False |

