# dacomp-056

The data team has identified a paradoxical phenomenon among high-value enterprise customer…

运行：已提交。官方未评分。全部 SQL 尝试/成功 35/34；数据 SQL 33/32；Python 13 次。

完整原题：

The data team has identified a paradoxical phenomenon among high-value enterprise customers (those in Gold/Platinum tiers with a `portfolio_contribution_pct` > 5%): their `cross_stage_engagement_consistency` is generally lower than that of SMB customers, yet their `revenue_velocity_monthly` and `estimated_customer_ltv` are significantly higher. By building a composite RFM scoring model (based on `recency_score`, `frequency_score`, and `monetary_score`) and conducting a multi-dimensional customer health analysis (integrating `customer_health_score`, `activity_efficiency`, and `churn_probability`), please thoroughly explain the root cause of this 'low consistency, high value' phenomenon. Based on time-based conversion efficiency (`marketing_to_sales_days`, `sales_to_support_days`), engagement channel preferences, and account lifecycle characteristics, design differentiated operational strategies and resource allocation plans for different customer segments.

| 表 | 行数 | 列数 |
| --- | --- | --- |
| customer360__conversion_funnel_analysis | 0 | 43 |
| customer360__customer_activity_metrics | 0 | 57 |
| customer360__customer_value_analysis | 5001 | 37 |


实际路线（分析者依据 SQL/源码概括，不代表 Agent 自述）：SQL 提取高价值企业客户与 SMB 特征 → Python 构建 RFM 指标并多维分组聚合 → 客户运营建议与图表。

数据库大小：2,109,440 字节。

## 数据 SQL

| SQL | 状态 | 基础表 | Join 输入/类型 | GROUP BY | 聚合表达式 | 结果行数 | 数据库 ms |
| --- | --- | --- | --- | --- | --- | --- | --- |
| [S3/Q1](#s3) | success | ["customer360__conversion_funnel_analysis", "customer360__customer_activity_metrics", "customer360__customer_value_analysis"] | 0 / {} | [] | ["COUNT(*)", "COUNT(*)", "COUNT(*)"] | 3 | 1.977 |
| [S4/Q2](#s4) | success | ["customer360__customer_value_analysis"] | 0 / {} | ["customer_tier", "customer_segment"] | ["COUNT(*)"] | 15 | 3.382 |
| [S5/Q3](#s5) | success | ["customer360__customer_value_analysis"] | 0 / {} | [] | [] | 5 | 0.435 |
| [S6/Q4](#s6) | success | ["customer360__customer_value_analysis"] | 0 / {} | [] | [] | 5 | 2.186 |
| [S7/Q5](#s7) | success | ["customer360__customer_value_analysis"] | 0 / {} | [] | [] | 7 | 2.147 |
| [S8/Q6](#s8) | success | ["customer360__customer_value_analysis"] | 0 / {} | [] | ["COUNT(*)", "COUNT(DISTINCT marketo_lead_id)", "COUNT(DISTINCT primary_email)", "COUNT(DISTINCT stripe_customer_id)", "COUNT(DISTINCT zendesk_user_id)"] | 1 | 11.684 |
| [S9/Q7](#s9) | success | ["customer360__customer_value_analysis"] | 0 / {} | ["marketo_lead_id"] | ["COUNT(*)"] | 20 | 3.37 |
| [S10/Q8](#s10) | success | ["customer360__customer_value_analysis"] | 0 / {} | ["customer_tier"] | ["COUNT(DISTINCT marketo_lead_id)", "AVG(portfolio_contribution_pct)", "AVG(estimated_customer_ltv)", "AVG(customer_health_score)", "AVG(churn_probability)", "AVG(recency_score)", "AVG(frequency_score)", "AVG(monetary_score)"] | 5 | 6.66 |
| [S11/Q9](#s11) | success | ["customer360__customer_value_analysis"] | 0 / {} | [] | [] | 20 | 2.958 |
| [S12/Q10](#s12) | success | ["customer360__conversion_funnel_analysis"] | 0 / {} | [] | ["COUNT(*)"] | 1 | 0.282 |
| [S13/Q11](#s13) | success | ["customer360__customer_activity_metrics"] | 0 / {} | [] | ["COUNT(*)"] | 1 | 0.38 |
| [S14/Q12](#s14) | success | ["customer360__customer_value_analysis"] | 0 / {} | ["customer_tier", "customer_segment"] | ["COUNT(DISTINCT marketo_lead_id)", "AVG(portfolio_contribution_pct)", "AVG(estimated_customer_ltv)", "AVG(recency_score)", "AVG(frequency_score)", "AVG(monetary_score)", "AVG(rfm_avg_score)", "AVG(customer_health_score)", "AVG(churn_probability)", "AVG(account_age_days)"] | 0 | 1.714 |
| [S15/Q13](#s15) | success | ["customer360__customer_value_analysis"] | 0 / {} | ["customer_tier", "customer_segment"] | ["COUNT(DISTINCT marketo_lead_id)", "AVG(portfolio_contribution_pct)", "AVG(estimated_customer_ltv)", "AVG(recency_score)", "AVG(frequency_score)", "AVG(monetary_score)", "AVG(rfm_avg_score)", "AVG(customer_health_score)", "AVG(churn_probability)"] | 0 | 2.113 |
| [S16/Q14](#s16) | failed | ["customer360__customer_value_analysis"] | 0 / {} | [] | ["MIN(portfolio_contribution_pct)", "MAX(portfolio_contribution_pct)", "AVG(portfolio_contribution_pct)"] | unknown | 未取得；调用总时长 0.205 ms |
| [S17/Q15](#s17) | success | ["customer360__customer_value_analysis"] | 0 / {} | [] | ["MIN(portfolio_contribution_pct)", "MAX(portfolio_contribution_pct)", "AVG(portfolio_contribution_pct)"] | 1 | 1.89 |
| [S18/Q16](#s18) | success | ["customer360__customer_value_analysis"] | 0 / {} | ["customer_tier"] | ["COUNT(DISTINCT marketo_lead_id)", "MIN(portfolio_contribution_pct)", "MAX(portfolio_contribution_pct)", "AVG(portfolio_contribution_pct)"] | 5 | 4.924 |
| [S19/Q17](#s19) | success | ["customer360__customer_value_analysis"] | 0 / {} | ["customer_tier", "customer_segment"] | ["COUNT(DISTINCT marketo_lead_id)", "AVG(portfolio_contribution_pct)", "AVG(estimated_customer_ltv)", "AVG(recency_score)", "AVG(frequency_score)", "AVG(monetary_score)", "AVG(rfm_avg_score)", "AVG(customer_health_score)", "AVG(churn_probability)", "AVG(account_age_days)", "AVG(days_since_last_activity)"] | 6 | 1.918 |
| [S20/Q18](#s20) | success | ["customer360__customer_value_analysis"] | 0 / {} | ["customer_tier", "customer_segment"] | ["COUNT(DISTINCT marketo_lead_id)", "AVG(portfolio_contribution_pct)", "AVG(estimated_customer_ltv)", "AVG(recency_score)", "AVG(frequency_score)", "AVG(monetary_score)", "AVG(rfm_avg_score)", "AVG(customer_health_score)", "AVG(churn_probability)"] | 9 | 8.379 |
| [S21/Q19](#s21) | success | ["customer360__customer_value_analysis"] | 0 / {} | [] | [] | 12 | 1.497 |
| [S22/Q20](#s22) | success | ["customer360__customer_value_analysis"] | 0 / {} | ["marketo_lead_id"] | ["COUNT(DISTINCT customer_tier)", "COUNT(DISTINCT customer_segment)", "COUNT(DISTINCT rfm_score)", "SUM(CASE WHEN ntiers > 1 THEN 1 ELSE 0 END)", "SUM(CASE WHEN nsegs > 1 THEN 1 ELSE 0 END)", "SUM(CASE WHEN nrfm > 1 THEN 1 ELSE 0 END)", "COUNT(*)"] | 1 | 8.96 |
| [S23/Q21](#s23) | success | ["customer360__customer_value_analysis"] | 0 / {} | ["rfm_segment"] | ["COUNT(*)"] | 7 | 2.459 |
| [S24/Q22](#s24) | success | ["customer360__customer_value_analysis"] | 0 / {} | [] | [] | 5 | 2.378 |
| [S25/Q23](#s25) | success | ["customer360__customer_value_analysis"] | 0 / {} | [] | [] | 4 | 2.352 |
| [S26/Q24](#s26) | success | ["customer360__customer_value_analysis"] | 0 / {} | [] | [] | 3 | 2.129 |
| [S27/Q25](#s27) | success | ["customer360__customer_value_analysis"] | 0 / {} | [] | [] | 4 | 2.189 |
| [S28/Q26](#s28) | success | ["customer360__customer_value_analysis"] | 0 / {} | [] | [] | 1 | 2.274 |
| [S29/Q27](#s29) | success | ["customer360__customer_value_analysis"] | 0 / {} | [] | [] | 4 | 2.267 |
| [S30/Q28](#s30) | success | ["customer360__customer_value_analysis"] | 0 / {} | [] | [] | 3 | 2.297 |
| [S31/Q29](#s31) | success | ["customer360__customer_value_analysis"] | 0 / {} | [] | [] | 4 | 2.028 |
| [S32/Q30](#s32) | success | ["customer360__customer_value_analysis"] | 0 / {} | [] | [] | 2 | 2.241 |
| [S33/Q31](#s33) | success | ["customer360__customer_value_analysis"] | 0 / {} | [] | [] | 2 | 1.971 |
| [S34/Q32](#s34) | success | ["customer360__customer_value_analysis"] | 0 / {} | [] | [] | 4672 | 76.05 |
| [S35/Q33](#s35) | success | ["customer360__customer_value_analysis"] | 0 / {} | ["customer_group"] | ["COUNT(*)", "AVG(recency_score)", "AVG(frequency_score)", "AVG(monetary_score)", "AVG(rfm_avg_score)", "AVG(estimated_customer_ltv)", "AVG(customer_health_score)", "AVG(churn_probability)", "AVG(account_age_days)", "AVG(days_since_last_activity)", "AVG(portfolio_contribution_pct)", "AVG(investment_priority_score)", "AVG(expected_annual_revenue)"] | 2 | 39.509 |


## 元数据和设置

| SQL | 类别 | 状态 | 内容 |
| --- | --- | --- | --- |
| S1 | connection_setup | success | PRAGMA query_only=ON |
| S2 | metadata | success | SELECT name,sql FROM sqlite_master WHERE type='table' ORDER BY name |


## Python 与执行位置

人工源码审查：**database_first_violation**。Python 对客户群、生命周期、风险与投资建议等维度执行分组求和、均值、数量和常规评分，并计算贡献率。这些计算可在 SQL 完成。相关性、卡方检验与图形渲染是独立的统计补充。 [证据](../reviews/dacomp-056.json)。

P1：I need to compute correlation coefficients, dispersion/consistency metrics across RFM components, hypothesis tests (t-test, chi-square), and distributions that SQLite cannot reasonably calculate. I load only the deduplicated per-lead rows (46 columns is fine since the full dedup result is already archived; I select only the columns needed for analysis).

[源码](../../../runs/dsv4flash-db-first-full-01/dacomp-056/attempt-01/python/P1.py)；[输出](../../../runs/dsv4flash-db-first-full-01/dacomp-056/attempt-01/python/P1.stdout)；[错误](../../../runs/dsv4flash-db-first-full-01/dacomp-056/attempt-01/python/P1.stderr)。检出需人工核验的 SQL 可实现操作：groupby(；不能仅凭理由判为合规。

P2：Check available result files and workspace structure

[源码](../../../runs/dsv4flash-db-first-full-01/dacomp-056/attempt-01/python/P2.py)；[输出](../../../runs/dsv4flash-db-first-full-01/dacomp-056/attempt-01/python/P2.stdout)；[错误](../../../runs/dsv4flash-db-first-full-01/dacomp-056/attempt-01/python/P2.stderr)。自动源码筛查未检出预设迁出信号；这不是全面语义合规证明。

P3：Find the results directory and list available files

[源码](../../../runs/dsv4flash-db-first-full-01/dacomp-056/attempt-01/python/P3.py)；[输出](../../../runs/dsv4flash-db-first-full-01/dacomp-056/attempt-01/python/P3.stdout)；[错误](../../../runs/dsv4flash-db-first-full-01/dacomp-056/attempt-01/python/P3.stderr)。自动源码筛查未检出预设迁出信号；这不是全面语义合规证明。

P4：Load deduplicated data from results directory and compute composite RFM, consistency metrics, and statistical tests that SQLite cannot reasonably compute.

[源码](../../../runs/dsv4flash-db-first-full-01/dacomp-056/attempt-01/python/P4.py)；[输出](../../../runs/dsv4flash-db-first-full-01/dacomp-056/attempt-01/python/P4.stdout)；[错误](../../../runs/dsv4flash-db-first-full-01/dacomp-056/attempt-01/python/P4.stderr)。检出需人工核验的 SQL 可实现操作：groupby(；不能仅凭理由判为合规。

P5：Inspect the JSONL structure to correctly load the archived rows

[源码](../../../runs/dsv4flash-db-first-full-01/dacomp-056/attempt-01/python/P5.py)；[输出](../../../runs/dsv4flash-db-first-full-01/dacomp-056/attempt-01/python/P5.stdout)；[错误](../../../runs/dsv4flash-db-first-full-01/dacomp-056/attempt-01/python/P5.stderr)。自动源码筛查未检出预设迁出信号；这不是全面语义合规证明。

P6：Load the deduped rows with correct column names from the table schema

[源码](../../../runs/dsv4flash-db-first-full-01/dacomp-056/attempt-01/python/P6.py)；[输出](../../../runs/dsv4flash-db-first-full-01/dacomp-056/attempt-01/python/P6.stdout)；[错误](../../../runs/dsv4flash-db-first-full-01/dacomp-056/attempt-01/python/P6.stderr)。检出需人工核验的 SQL 可实现操作：groupby(；不能仅凭理由判为合规。

P7：Create visualizations to illustrate the 'low consistency, high value' paradox: RFM component comparison, M-RF gap, consistency metrics, lifecycle stages, and risk profiles.

[源码](../../../runs/dsv4flash-db-first-full-01/dacomp-056/attempt-01/python/P7.py)；[输出](../../../runs/dsv4flash-db-first-full-01/dacomp-056/attempt-01/python/P7.stdout)；[错误](../../../runs/dsv4flash-db-first-full-01/dacomp-056/attempt-01/python/P7.stderr)。自动源码筛查未检出预设迁出信号；这不是全面语义合规证明。

P8：Analyze HVE sub-segments (tier, segment, lifecycle) and define strategy quadrants using composite RFM and churn/health metrics, plus compute segment-level aggregates to design differentiated operational plans.

[源码](../../../runs/dsv4flash-db-first-full-01/dacomp-056/attempt-01/python/P8.py)；[输出](../../../runs/dsv4flash-db-first-full-01/dacomp-056/attempt-01/python/P8.stdout)；[错误](../../../runs/dsv4flash-db-first-full-01/dacomp-056/attempt-01/python/P8.stderr)。检出需人工核验的 SQL 可实现操作：groupby(；不能仅凭理由判为合规。

P9：Compute time-based efficiency proxies (inactive share of account life), investment metrics, and additional segment details needed for strategy design; also run chi-square tests for categorical differences.

[源码](../../../runs/dsv4flash-db-first-full-01/dacomp-056/attempt-01/python/P9.py)；[输出](../../../runs/dsv4flash-db-first-full-01/dacomp-056/attempt-01/python/P9.stdout)；[错误](../../../runs/dsv4flash-db-first-full-01/dacomp-056/attempt-01/python/P9.stderr)。检出需人工核验的 SQL 可实现操作：groupby(；不能仅凭理由判为合规。

P10：Complete the remaining segment analysis (SMB by tier, HVE at-risk cluster, correlations) for strategy design.

[源码](../../../runs/dsv4flash-db-first-full-01/dacomp-056/attempt-01/python/P10.py)；[输出](../../../runs/dsv4flash-db-first-full-01/dacomp-056/attempt-01/python/P10.stdout)；[错误](../../../runs/dsv4flash-db-first-full-01/dacomp-056/attempt-01/python/P10.stderr)。检出需人工核验的 SQL 可实现操作：groupby(；不能仅凭理由判为合规。

P11：Create a consolidated strategy visualization (heatmap of HVE segment profiles) for the report.

[源码](../../../runs/dsv4flash-db-first-full-01/dacomp-056/attempt-01/python/P11.py)；[输出](../../../runs/dsv4flash-db-first-full-01/dacomp-056/attempt-01/python/P11.stdout)；[错误](../../../runs/dsv4flash-db-first-full-01/dacomp-056/attempt-01/python/P11.stderr)。自动源码筛查未检出预设迁出信号；这不是全面语义合规证明。

P12：Recreate strategy visualization with active_share recomputed from the base data (it wasn't persisted in the pickle).

[源码](../../../runs/dsv4flash-db-first-full-01/dacomp-056/attempt-01/python/P12.py)；[输出](../../../runs/dsv4flash-db-first-full-01/dacomp-056/attempt-01/python/P12.stdout)；[错误](../../../runs/dsv4flash-db-first-full-01/dacomp-056/attempt-01/python/P12.stderr)。自动源码筛查未检出预设迁出信号；这不是全面语义合规证明。

P13：Recreate heatmap without sklearn by doing manual min-max normalization.

[源码](../../../runs/dsv4flash-db-first-full-01/dacomp-056/attempt-01/python/P13.py)；[输出](../../../runs/dsv4flash-db-first-full-01/dacomp-056/attempt-01/python/P13.stdout)；[错误](../../../runs/dsv4flash-db-first-full-01/dacomp-056/attempt-01/python/P13.stderr)。自动源码筛查未检出预设迁出信号；这不是全面语义合规证明。

## 优化机会

已验证候选。筛选限于精确 SQL、相同自包含 CTE、相同单表完整过滤、可分解单表聚合；未覆盖任意 Join 等价和一般谓词蕴含。全部候选都是 offline，未测在线预测。

| 候选 | 类型 | 已有结果 | 覆盖 SQL | 后续次数 | 中间行数 | 验证 | 成本 |
| --- | --- | --- | --- | --- | --- | --- | --- |
| C1 | common subexpression | False | ["S34", "S35"] | 1 | 4837 | verified | Not benchmarked; correctness alone does not establish net speedup. |
| C2 | aggregate MV | False | ["S4", "S23"] | 1 | 48 | verified | Not benchmarked; correctness alone does not establish net speedup. |
| C3 | common filtered view | False | ["S10", "S17", "S18"] | 2 | 4837 | verified | Not benchmarked; correctness alone does not establish net speedup. |


已验证覆盖（含触发查询、候选并集去重）：7/32 条成功数据 SQL。正确性仅针对当前数据库快照；未测性能的候选不能声称已加速。

[完整 build/rewrite 与比较证据](dacomp-056.analysis.json)。

### C3：common filtered view

Same single source and complete filter; original filter retained.

原查询 [S10](#s10), [S17](#s17), [S18](#s18) → 新增共享状态 C3 → 后续 2 次可复用。该构建点为事后假设，不代表 Agent 当时预知后续。

构建定义：

```sql
SELECT * FROM "customer360__customer_value_analysis" WHERE NOT marketo_lead_id IS NULL
```

受益查询 S10 的改写示例：

```sql
SELECT customer_tier, COUNT(DISTINCT marketo_lead_id) AS n, AVG(portfolio_contribution_pct) AS avg_portfolio_contrib, AVG(estimated_customer_ltv) AS avg_ltv, AVG(customer_health_score) AS avg_health, AVG(churn_probability) AS avg_churn, AVG(recency_score) AS avg_recency, AVG(frequency_score) AS avg_frequency, AVG(monetary_score) AS avg_monetary FROM temp.reuse_candidate AS customer360__customer_value_analysis WHERE NOT marketo_lead_id IS NULL GROUP BY customer_tier ORDER BY CASE customer_tier WHEN 'Platinum' THEN 1 WHEN 'Gold' THEN 2 WHEN 'Silver' THEN 3 WHEN 'Bronze' THEN 4 WHEN 'Basic' THEN 5 END
```

| 原 SQL | 列名一致 | 结果一致 | 比较方法 |
| --- | --- | --- | --- |
| S10 | True | True | ordered_numeric_tolerance |
| S17 | True | True | exact_multiset |
| S18 | True | True | exact_multiset |


验证状态：verified；成本结论：Not benchmarked; correctness alone does not establish net speedup.

### C1：common subexpression

Identical self-contained CTE body across queries.

原查询 [S34](#s34), [S35](#s35) → 新增共享状态 C1 → 后续 1 次可复用。该构建点为事后假设，不代表 Agent 当时预知后续。

构建定义：

```sql
SELECT *, ROW_NUMBER() OVER (PARTITION BY marketo_lead_id ORDER BY rfm_avg_score DESC, rfm_score DESC) AS rn FROM customer360__customer_value_analysis WHERE NOT marketo_lead_id IS NULL
```

受益查询 S34 的改写示例：

```sql
/* Deduplicate: keep one row per lead, picking the one with highest rfm_avg_score */ WITH dedup AS (SELECT * FROM temp.reuse_candidate) SELECT * FROM dedup WHERE rn = 1
```

| 原 SQL | 列名一致 | 结果一致 | 比较方法 |
| --- | --- | --- | --- |
| S34 | True | True | exact_multiset |
| S35 | True | True | exact_multiset |


验证状态：verified；成本结论：Not benchmarked; correctness alone does not establish net speedup.

### C2：aggregate MV

Union of grouping keys; decomposable aggregate states; AVG uses SUM and non-NULL COUNT.

原查询 [S4](#s4), [S23](#s23) → 新增共享状态 C2 → 后续 1 次可复用。该构建点为事后假设，不代表 Agent 当时预知后续。

构建定义：

```sql
SELECT customer_tier AS __g0, customer_segment AS __g1, rfm_segment AS __g2, COUNT(*) AS __a0 FROM "customer360__customer_value_analysis"  GROUP BY customer_tier, customer_segment, rfm_segment
```

受益查询 S4 的改写示例：

```sql
SELECT __g0 AS "customer_tier", __g1 AS "customer_segment", SUM(__a0) AS n FROM temp.reuse_candidate GROUP BY __g0, __g1 ORDER BY n DESC
```

| 原 SQL | 列名一致 | 结果一致 | 比较方法 |
| --- | --- | --- | --- |
| S4 | True | True | ordered_numeric_tolerance |
| S23 | True | True | ordered_numeric_tolerance |


验证状态：verified；成本结论：Not benchmarked; correctness alone does not establish net speedup.

结果依赖：自动记录 SQL→Python 的接口父调用，以及源码中引用归档文件的消费者；字面值相同不认定因果。模型方向选择需要人工读取消息，尚未做全面因果标注。

[原始报告](../../../runs/dsv4flash-db-first-full-01/dacomp-056/attempt-01/answer.md)；[统一消息](../../../runs/dsv4flash-db-first-full-01/dacomp-056/attempt-01/messages.jsonl)；[原始 OpenCode 事件](../../../runs/dsv4flash-db-first-full-01/dacomp-056/attempt-01/opencode.jsonl)；[SQL 引擎日志](../../../runs/dsv4flash-db-first-full-01/dacomp-056/attempt-01/sql_journal.jsonl)。

[可读报告（本地图片链接规范化）](../answers/dacomp-056.md)。原始回答保留，分析结论未改写。

## S1

类别 `connection_setup`；来源 `connection`；调用 `eb1cafcc0fb14d70b421435b113f9c40`；状态 `success`。

```sql
PRAGMA query_only=ON
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-056/attempt-01/sql/S1.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-056/attempt-01/sql/S1.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-056/attempt-01/results/S1.rows.jsonl)；完整：True；SHA256：`e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`。

## S2

类别 `metadata`；来源 `list_db`；调用 `eb1cafcc0fb14d70b421435b113f9c40`；状态 `success`。

```sql
SELECT name,sql FROM sqlite_master WHERE type='table' ORDER BY name
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-056/attempt-01/sql/S2.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-056/attempt-01/sql/S2.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-056/attempt-01/results/S2.rows.jsonl)；完整：True；SHA256：`e107363f42e3530dcafbaed159b1ec1f0c8b25ac714bea0adfc1f16c6230be45`。

## S3

类别 `data`；来源 `query_db`；调用 `03901114d13d479cb4db29f30723c1b2`；状态 `success`。

```sql
SELECT 'conversion_funnel' AS tbl, COUNT(*) AS n FROM customer360__conversion_funnel_analysis
UNION ALL SELECT 'activity_metrics', COUNT(*) FROM customer360__customer_activity_metrics
UNION ALL SELECT 'value_analysis', COUNT(*) FROM customer360__customer_value_analysis
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-056/attempt-01/sql/S3.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-056/attempt-01/sql/S3.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-056/attempt-01/results/S3.rows.jsonl)；完整：True；SHA256：`e36ec7a82be30150315d988c2ec5982b3503c9c553e04e0a9751749d91f83b32`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "customer360__conversion_funnel_analysis", "kind": "base", "block": null, "base_tables": ["customer360__conversion_funnel_analysis"]}] | [] | [] |
| B2 | [{"alias": "customer360__customer_activity_metrics", "kind": "base", "block": null, "base_tables": ["customer360__customer_activity_metrics"]}] | [] | [] |
| B3 | [] | [] | [] |
| B4 | [{"alias": "customer360__customer_value_analysis", "kind": "base", "block": null, "base_tables": ["customer360__customer_value_analysis"]}] | [] | [] |
| B5 | [] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |
| B2 | COUNT(*) | [] | [] | True |
| B4 | COUNT(*) | [] | [] | True |


## S4

类别 `data`；来源 `query_db`；调用 `1fec7842890b42e590a131251f0c30e4`；状态 `success`。

```sql
SELECT customer_tier, customer_segment, COUNT(*) AS n FROM customer360__customer_value_analysis GROUP BY customer_tier, customer_segment ORDER BY n DESC
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-056/attempt-01/sql/S4.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-056/attempt-01/sql/S4.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-056/attempt-01/results/S4.rows.jsonl)；完整：True；SHA256：`c13d58163000b4c3f0e6a646fce6157fe6a4f6eaf03ab487dd4b0653e92d6d5c`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "customer360__customer_value_analysis", "kind": "base", "block": null, "base_tables": ["customer360__customer_value_analysis"]}] | [] | ["customer_tier", "customer_segment"] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |


## S5

类别 `data`；来源 `query_db`；调用 `df53a5d7e658472b9f05a60244ff2922`；状态 `success`。

```sql
SELECT * FROM customer360__customer_value_analysis LIMIT 5
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-056/attempt-01/sql/S5.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-056/attempt-01/sql/S5.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-056/attempt-01/results/S5.rows.jsonl)；完整：True；SHA256：`b5f4b08ff4da922cf66060c6075626851cedfde5c552da4afde59b57113745ec`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "customer360__customer_value_analysis", "kind": "base", "block": null, "base_tables": ["customer360__customer_value_analysis"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |


## S6

类别 `data`；来源 `query_db`；调用 `83054a4a6e6a40d98b358cd45ecd1b30`；状态 `success`。

```sql
SELECT DISTINCT customer_tier FROM customer360__customer_value_analysis ORDER BY customer_tier
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-056/attempt-01/sql/S6.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-056/attempt-01/sql/S6.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-056/attempt-01/results/S6.rows.jsonl)；完整：True；SHA256：`0247280cee89907e617e0bf91816fd7b470c0f7c042bae332cbeda2b75c5b59b`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "customer360__customer_value_analysis", "kind": "base", "block": null, "base_tables": ["customer360__customer_value_analysis"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |


## S7

类别 `data`；来源 `query_db`；调用 `52ac0cf255824b58b46b0c9bd3d3d77d`；状态 `success`。

```sql
SELECT DISTINCT customer_segment FROM customer360__customer_value_analysis ORDER BY customer_segment
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-056/attempt-01/sql/S7.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-056/attempt-01/sql/S7.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-056/attempt-01/results/S7.rows.jsonl)；完整：True；SHA256：`365075f9f0af5476970cba35c74d7db82520a18139cd8fa5e4986ebbb7cb9468`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "customer360__customer_value_analysis", "kind": "base", "block": null, "base_tables": ["customer360__customer_value_analysis"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |


## S8

类别 `data`；来源 `query_db`；调用 `cd6154d1c1c244daa669002978b8db7b`；状态 `success`。

```sql
SELECT COUNT(*) AS total_rows, COUNT(DISTINCT marketo_lead_id) AS distinct_leads, COUNT(DISTINCT primary_email) AS distinct_emails, COUNT(DISTINCT stripe_customer_id) AS distinct_stripe, COUNT(DISTINCT zendesk_user_id) AS distinct_zendesk FROM customer360__customer_value_analysis
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-056/attempt-01/sql/S8.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-056/attempt-01/sql/S8.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-056/attempt-01/results/S8.rows.jsonl)；完整：True；SHA256：`349b6bb62a672112a0783c5f9c76162c14e52ce4497d2d91934de9317555af85`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "customer360__customer_value_analysis", "kind": "base", "block": null, "base_tables": ["customer360__customer_value_analysis"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |
| B1 | COUNT(DISTINCT marketo_lead_id) | [{"table": "customer360__customer_value_analysis", "column": "marketo_lead_id"}] | [] | False |
| B1 | COUNT(DISTINCT primary_email) | [{"table": "customer360__customer_value_analysis", "column": "primary_email"}] | [] | False |
| B1 | COUNT(DISTINCT stripe_customer_id) | [{"table": "customer360__customer_value_analysis", "column": "stripe_customer_id"}] | [] | False |
| B1 | COUNT(DISTINCT zendesk_user_id) | [{"table": "customer360__customer_value_analysis", "column": "zendesk_user_id"}] | [] | False |


## S9

类别 `data`；来源 `query_db`；调用 `0610856c0c6a4ce8a4c33c8401183793`；状态 `success`。

```sql
SELECT marketo_lead_id, COUNT(*) AS n FROM customer360__customer_value_analysis GROUP BY marketo_lead_id HAVING n > 1 ORDER BY n DESC LIMIT 20
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-056/attempt-01/sql/S9.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-056/attempt-01/sql/S9.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-056/attempt-01/results/S9.rows.jsonl)；完整：True；SHA256：`737e960d859f5ef616c384d240e064602886a24a24edc25ac7fcc4fdf06b25bd`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "customer360__customer_value_analysis", "kind": "base", "block": null, "base_tables": ["customer360__customer_value_analysis"]}] | [] | ["marketo_lead_id"] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |


## S10

类别 `data`；来源 `query_db`；调用 `ffbaeb985e9a434fa10ddb39e7ffa585`；状态 `success`。

```sql
SELECT customer_tier, COUNT(DISTINCT marketo_lead_id) AS n, 
       AVG(portfolio_contribution_pct) AS avg_portfolio_contrib,
       AVG(estimated_customer_ltv) AS avg_ltv,
       AVG(customer_health_score) AS avg_health,
       AVG(churn_probability) AS avg_churn,
       AVG(recency_score) AS avg_recency,
       AVG(frequency_score) AS avg_frequency,
       AVG(monetary_score) AS avg_monetary
FROM customer360__customer_value_analysis
WHERE marketo_lead_id IS NOT NULL
GROUP BY customer_tier
ORDER BY CASE customer_tier 
  WHEN 'Platinum' THEN 1 WHEN 'Gold' THEN 2 
  WHEN 'Silver' THEN 3 WHEN 'Bronze' THEN 4 WHEN 'Basic' THEN 5 END
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-056/attempt-01/sql/S10.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-056/attempt-01/sql/S10.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-056/attempt-01/results/S10.rows.jsonl)；完整：True；SHA256：`936027ef61c3eea8e7eab4d5f85d35041f845fbd91bf4e1096cd9720f5b523d2`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "customer360__customer_value_analysis", "kind": "base", "block": null, "base_tables": ["customer360__customer_value_analysis"]}] | [] | ["customer_tier"] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(DISTINCT marketo_lead_id) | [{"table": "customer360__customer_value_analysis", "column": "marketo_lead_id"}] | [] | False |
| B1 | AVG(portfolio_contribution_pct) | [{"table": "customer360__customer_value_analysis", "column": "portfolio_contribution_pct"}] | [] | False |
| B1 | AVG(estimated_customer_ltv) | [{"table": "customer360__customer_value_analysis", "column": "estimated_customer_ltv"}] | [] | False |
| B1 | AVG(customer_health_score) | [{"table": "customer360__customer_value_analysis", "column": "customer_health_score"}] | [] | False |
| B1 | AVG(churn_probability) | [{"table": "customer360__customer_value_analysis", "column": "churn_probability"}] | [] | False |
| B1 | AVG(recency_score) | [{"table": "customer360__customer_value_analysis", "column": "recency_score"}] | [] | False |
| B1 | AVG(frequency_score) | [{"table": "customer360__customer_value_analysis", "column": "frequency_score"}] | [] | False |
| B1 | AVG(monetary_score) | [{"table": "customer360__customer_value_analysis", "column": "monetary_score"}] | [] | False |


## S11

类别 `data`；来源 `query_db`；调用 `4115fb7b2f814b1e8c03571072606d73`；状态 `success`。

```sql
SELECT DISTINCT portfolio_contribution_pct FROM customer360__customer_value_analysis ORDER BY portfolio_contribution_pct LIMIT 20
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-056/attempt-01/sql/S11.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-056/attempt-01/sql/S11.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-056/attempt-01/results/S11.rows.jsonl)；完整：True；SHA256：`ae3e32ec7881e23fb762c3b4641deeada18dc577e1c05cf88cedfd367ed0b41f`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "customer360__customer_value_analysis", "kind": "base", "block": null, "base_tables": ["customer360__customer_value_analysis"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |


## S12

类别 `data`；来源 `query_db`；调用 `95f5c78297844d9bb213486d2b9fdb09`；状态 `success`。

```sql
SELECT COUNT(*) FROM customer360__conversion_funnel_analysis
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-056/attempt-01/sql/S12.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-056/attempt-01/sql/S12.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-056/attempt-01/results/S12.rows.jsonl)；完整：True；SHA256：`c14196f132c1e9be0508ae80ab52fcb3e1d3fc05880415f3dc980971df207c9e`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "customer360__conversion_funnel_analysis", "kind": "base", "block": null, "base_tables": ["customer360__conversion_funnel_analysis"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |


## S13

类别 `data`；来源 `query_db`；调用 `1af82e858a284732b9da254621f51a7b`；状态 `success`。

```sql
SELECT COUNT(*) FROM customer360__customer_activity_metrics
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-056/attempt-01/sql/S13.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-056/attempt-01/sql/S13.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-056/attempt-01/results/S13.rows.jsonl)；完整：True；SHA256：`c14196f132c1e9be0508ae80ab52fcb3e1d3fc05880415f3dc980971df207c9e`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "customer360__customer_activity_metrics", "kind": "base", "block": null, "base_tables": ["customer360__customer_activity_metrics"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |


## S14

类别 `data`；来源 `query_db`；调用 `cdf81192f11b44ed8769df4ed184f709`；状态 `success`。

```sql
SELECT customer_tier, customer_segment, COUNT(DISTINCT marketo_lead_id) AS n,
       AVG(portfolio_contribution_pct) AS avg_portfolio,
       AVG(estimated_customer_ltv) AS avg_ltv,
       AVG(recency_score) AS avg_recency,
       AVG(frequency_score) AS avg_frequency,
       AVG(monetary_score) AS avg_monetary,
       AVG(rfm_avg_score) AS avg_rfm,
       AVG(customer_health_score) AS avg_health,
       AVG(churn_probability) AS avg_churn,
       AVG(account_age_days) AS avg_age
FROM customer360__customer_value_analysis
WHERE marketo_lead_id IS NOT NULL
  AND customer_tier IN ('Gold', 'Platinum')
  AND portfolio_contribution_pct > 5.0
GROUP BY customer_tier, customer_segment
ORDER BY customer_tier, n DESC
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-056/attempt-01/sql/S14.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-056/attempt-01/sql/S14.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-056/attempt-01/results/S14.rows.jsonl)；完整：True；SHA256：`e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "customer360__customer_value_analysis", "kind": "base", "block": null, "base_tables": ["customer360__customer_value_analysis"]}] | [] | ["customer_tier", "customer_segment"] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(DISTINCT marketo_lead_id) | [{"table": "customer360__customer_value_analysis", "column": "marketo_lead_id"}] | [] | False |
| B1 | AVG(portfolio_contribution_pct) | [{"table": "customer360__customer_value_analysis", "column": "portfolio_contribution_pct"}] | [] | False |
| B1 | AVG(estimated_customer_ltv) | [{"table": "customer360__customer_value_analysis", "column": "estimated_customer_ltv"}] | [] | False |
| B1 | AVG(recency_score) | [{"table": "customer360__customer_value_analysis", "column": "recency_score"}] | [] | False |
| B1 | AVG(frequency_score) | [{"table": "customer360__customer_value_analysis", "column": "frequency_score"}] | [] | False |
| B1 | AVG(monetary_score) | [{"table": "customer360__customer_value_analysis", "column": "monetary_score"}] | [] | False |
| B1 | AVG(rfm_avg_score) | [{"table": "customer360__customer_value_analysis", "column": "rfm_avg_score"}] | [] | False |
| B1 | AVG(customer_health_score) | [{"table": "customer360__customer_value_analysis", "column": "customer_health_score"}] | [] | False |
| B1 | AVG(churn_probability) | [{"table": "customer360__customer_value_analysis", "column": "churn_probability"}] | [] | False |
| B1 | AVG(account_age_days) | [{"table": "customer360__customer_value_analysis", "column": "account_age_days"}] | [] | False |


## S15

类别 `data`；来源 `query_db`；调用 `34fb9a7a7a3f426092d546907e4ed067`；状态 `success`。

```sql
SELECT customer_tier, customer_segment, COUNT(DISTINCT marketo_lead_id) AS n,
       AVG(portfolio_contribution_pct) AS avg_portfolio,
       AVG(estimated_customer_ltv) AS avg_ltv,
       AVG(recency_score) AS avg_recency,
       AVG(frequency_score) AS avg_frequency,
       AVG(monetary_score) AS avg_monetary,
       AVG(rfm_avg_score) AS avg_rfm,
       AVG(customer_health_score) AS avg_health,
       AVG(churn_probability) AS avg_churn
FROM customer360__customer_value_analysis
WHERE marketo_lead_id IS NOT NULL
  AND customer_tier NOT IN ('Gold', 'Platinum')
  AND portfolio_contribution_pct > 5.0
GROUP BY customer_tier, customer_segment
ORDER BY customer_tier, n DESC
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-056/attempt-01/sql/S15.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-056/attempt-01/sql/S15.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-056/attempt-01/results/S15.rows.jsonl)；完整：True；SHA256：`e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "customer360__customer_value_analysis", "kind": "base", "block": null, "base_tables": ["customer360__customer_value_analysis"]}] | [] | ["customer_tier", "customer_segment"] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(DISTINCT marketo_lead_id) | [{"table": "customer360__customer_value_analysis", "column": "marketo_lead_id"}] | [] | False |
| B1 | AVG(portfolio_contribution_pct) | [{"table": "customer360__customer_value_analysis", "column": "portfolio_contribution_pct"}] | [] | False |
| B1 | AVG(estimated_customer_ltv) | [{"table": "customer360__customer_value_analysis", "column": "estimated_customer_ltv"}] | [] | False |
| B1 | AVG(recency_score) | [{"table": "customer360__customer_value_analysis", "column": "recency_score"}] | [] | False |
| B1 | AVG(frequency_score) | [{"table": "customer360__customer_value_analysis", "column": "frequency_score"}] | [] | False |
| B1 | AVG(monetary_score) | [{"table": "customer360__customer_value_analysis", "column": "monetary_score"}] | [] | False |
| B1 | AVG(rfm_avg_score) | [{"table": "customer360__customer_value_analysis", "column": "rfm_avg_score"}] | [] | False |
| B1 | AVG(customer_health_score) | [{"table": "customer360__customer_value_analysis", "column": "customer_health_score"}] | [] | False |
| B1 | AVG(churn_probability) | [{"table": "customer360__customer_value_analysis", "column": "churn_probability"}] | [] | False |


## S16

类别 `data`；来源 `query_db`；调用 `5a83c1cf61b2485e8932266d1d824481`；状态 `failed`。

```sql
SELECT MIN(portfolio_contribution_pct) AS min_pct,
       MAX(portfolio_contribution_pct) AS max_pct,
       AVG(portfolio_contribution_pct) AS avg_pct,
       PERCENTILE(portfolio_contribution_pct, 0.5) AS median_pct,
       PERCENTILE(portfolio_contribution_pct, 0.75) AS p75,
       PERCENTILE(portfolio_contribution_pct, 0.90) AS p90,
       PERCENTILE(portfolio_contribution_pct, 0.95) AS p95,
       PERCENTILE(portfolio_contribution_pct, 0.99) AS p99
FROM customer360__customer_value_analysis
WHERE marketo_lead_id IS NOT NULL
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-056/attempt-01/sql/S16.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-056/attempt-01/sql/S16.parameters.json)。

错误：`OperationalError('no such function: PERCENTILE')`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "customer360__customer_value_analysis", "kind": "base", "block": null, "base_tables": ["customer360__customer_value_analysis"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | MIN(portfolio_contribution_pct) | [{"table": "customer360__customer_value_analysis", "column": "portfolio_contribution_pct"}] | [] | False |
| B1 | MAX(portfolio_contribution_pct) | [{"table": "customer360__customer_value_analysis", "column": "portfolio_contribution_pct"}] | [] | False |
| B1 | AVG(portfolio_contribution_pct) | [{"table": "customer360__customer_value_analysis", "column": "portfolio_contribution_pct"}] | [] | False |


## S17

类别 `data`；来源 `query_db`；调用 `ea5513cbfe84479190336698b9ecfcb0`；状态 `success`。

```sql
SELECT MIN(portfolio_contribution_pct) AS min_pct,
       MAX(portfolio_contribution_pct) AS max_pct,
       AVG(portfolio_contribution_pct) AS avg_pct
FROM customer360__customer_value_analysis
WHERE marketo_lead_id IS NOT NULL
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-056/attempt-01/sql/S17.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-056/attempt-01/sql/S17.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-056/attempt-01/results/S17.rows.jsonl)；完整：True；SHA256：`6699e8f5de091fce8ebf7f9c47db50a31083e72055577d1e634e9d191ebc1b88`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "customer360__customer_value_analysis", "kind": "base", "block": null, "base_tables": ["customer360__customer_value_analysis"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | MIN(portfolio_contribution_pct) | [{"table": "customer360__customer_value_analysis", "column": "portfolio_contribution_pct"}] | [] | False |
| B1 | MAX(portfolio_contribution_pct) | [{"table": "customer360__customer_value_analysis", "column": "portfolio_contribution_pct"}] | [] | False |
| B1 | AVG(portfolio_contribution_pct) | [{"table": "customer360__customer_value_analysis", "column": "portfolio_contribution_pct"}] | [] | False |


## S18

类别 `data`；来源 `query_db`；调用 `6090d72fef2047d2bdac6c492050efcb`；状态 `success`。

```sql
SELECT customer_tier,
       COUNT(DISTINCT marketo_lead_id) AS n,
       MIN(portfolio_contribution_pct) AS min_pct,
       MAX(portfolio_contribution_pct) AS max_pct,
       AVG(portfolio_contribution_pct) AS avg_pct
FROM customer360__customer_value_analysis
WHERE marketo_lead_id IS NOT NULL
GROUP BY customer_tier
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-056/attempt-01/sql/S18.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-056/attempt-01/sql/S18.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-056/attempt-01/results/S18.rows.jsonl)；完整：True；SHA256：`4e3350c63baf0e04ce322f3af306379a3d38ccfed5bd1dc3b65d44c005a78e8e`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "customer360__customer_value_analysis", "kind": "base", "block": null, "base_tables": ["customer360__customer_value_analysis"]}] | [] | ["customer_tier"] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(DISTINCT marketo_lead_id) | [{"table": "customer360__customer_value_analysis", "column": "marketo_lead_id"}] | [] | False |
| B1 | MIN(portfolio_contribution_pct) | [{"table": "customer360__customer_value_analysis", "column": "portfolio_contribution_pct"}] | [] | False |
| B1 | MAX(portfolio_contribution_pct) | [{"table": "customer360__customer_value_analysis", "column": "portfolio_contribution_pct"}] | [] | False |
| B1 | AVG(portfolio_contribution_pct) | [{"table": "customer360__customer_value_analysis", "column": "portfolio_contribution_pct"}] | [] | False |


## S19

类别 `data`；来源 `query_db`；调用 `be53fb42bb394402a51f46bde4ae258e`；状态 `success`。

```sql
SELECT customer_tier, customer_segment, COUNT(DISTINCT marketo_lead_id) AS n,
       AVG(portfolio_contribution_pct) AS avg_portfolio,
       AVG(estimated_customer_ltv) AS avg_ltv,
       AVG(recency_score) AS avg_recency,
       AVG(frequency_score) AS avg_frequency,
       AVG(monetary_score) AS avg_monetary,
       AVG(rfm_avg_score) AS avg_rfm,
       AVG(customer_health_score) AS avg_health,
       AVG(churn_probability) AS avg_churn,
       AVG(account_age_days) AS avg_age,
       AVG(days_since_last_activity) AS avg_days_inactive
FROM customer360__customer_value_analysis
WHERE marketo_lead_id IS NOT NULL
  AND customer_tier IN ('Gold', 'Platinum')
  AND portfolio_contribution_pct > 0.05
GROUP BY customer_tier, customer_segment
ORDER BY customer_tier, n DESC
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-056/attempt-01/sql/S19.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-056/attempt-01/sql/S19.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-056/attempt-01/results/S19.rows.jsonl)；完整：True；SHA256：`47e284e7887125b7f912696e4ea1d95728f650110310463cc8adb7eb1ba80a4c`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "customer360__customer_value_analysis", "kind": "base", "block": null, "base_tables": ["customer360__customer_value_analysis"]}] | [] | ["customer_tier", "customer_segment"] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(DISTINCT marketo_lead_id) | [{"table": "customer360__customer_value_analysis", "column": "marketo_lead_id"}] | [] | False |
| B1 | AVG(portfolio_contribution_pct) | [{"table": "customer360__customer_value_analysis", "column": "portfolio_contribution_pct"}] | [] | False |
| B1 | AVG(estimated_customer_ltv) | [{"table": "customer360__customer_value_analysis", "column": "estimated_customer_ltv"}] | [] | False |
| B1 | AVG(recency_score) | [{"table": "customer360__customer_value_analysis", "column": "recency_score"}] | [] | False |
| B1 | AVG(frequency_score) | [{"table": "customer360__customer_value_analysis", "column": "frequency_score"}] | [] | False |
| B1 | AVG(monetary_score) | [{"table": "customer360__customer_value_analysis", "column": "monetary_score"}] | [] | False |
| B1 | AVG(rfm_avg_score) | [{"table": "customer360__customer_value_analysis", "column": "rfm_avg_score"}] | [] | False |
| B1 | AVG(customer_health_score) | [{"table": "customer360__customer_value_analysis", "column": "customer_health_score"}] | [] | False |
| B1 | AVG(churn_probability) | [{"table": "customer360__customer_value_analysis", "column": "churn_probability"}] | [] | False |
| B1 | AVG(account_age_days) | [{"table": "customer360__customer_value_analysis", "column": "account_age_days"}] | [] | False |
| B1 | AVG(days_since_last_activity) | [{"table": "customer360__customer_value_analysis", "column": "days_since_last_activity"}] | [] | False |


## S20

类别 `data`；来源 `query_db`；调用 `71110ca92f394b8eb2dc1f90f14c60e3`；状态 `success`。

```sql
SELECT customer_tier, customer_segment, COUNT(DISTINCT marketo_lead_id) AS n,
       AVG(portfolio_contribution_pct) AS avg_portfolio,
       AVG(estimated_customer_ltv) AS avg_ltv,
       AVG(recency_score) AS avg_recency,
       AVG(frequency_score) AS avg_frequency,
       AVG(monetary_score) AS avg_monetary,
       AVG(rfm_avg_score) AS avg_rfm,
       AVG(customer_health_score) AS avg_health,
       AVG(churn_probability) AS avg_churn
FROM customer360__customer_value_analysis
WHERE marketo_lead_id IS NOT NULL
  AND customer_tier NOT IN ('Gold', 'Platinum')
GROUP BY customer_tier, customer_segment
ORDER BY customer_tier, n DESC
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-056/attempt-01/sql/S20.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-056/attempt-01/sql/S20.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-056/attempt-01/results/S20.rows.jsonl)；完整：True；SHA256：`b0ae8d91451d1f6dfb90a81f7e47d3dceb7a1ad3da7e29c746011f99bd87882b`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "customer360__customer_value_analysis", "kind": "base", "block": null, "base_tables": ["customer360__customer_value_analysis"]}] | [] | ["customer_tier", "customer_segment"] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(DISTINCT marketo_lead_id) | [{"table": "customer360__customer_value_analysis", "column": "marketo_lead_id"}] | [] | False |
| B1 | AVG(portfolio_contribution_pct) | [{"table": "customer360__customer_value_analysis", "column": "portfolio_contribution_pct"}] | [] | False |
| B1 | AVG(estimated_customer_ltv) | [{"table": "customer360__customer_value_analysis", "column": "estimated_customer_ltv"}] | [] | False |
| B1 | AVG(recency_score) | [{"table": "customer360__customer_value_analysis", "column": "recency_score"}] | [] | False |
| B1 | AVG(frequency_score) | [{"table": "customer360__customer_value_analysis", "column": "frequency_score"}] | [] | False |
| B1 | AVG(monetary_score) | [{"table": "customer360__customer_value_analysis", "column": "monetary_score"}] | [] | False |
| B1 | AVG(rfm_avg_score) | [{"table": "customer360__customer_value_analysis", "column": "rfm_avg_score"}] | [] | False |
| B1 | AVG(customer_health_score) | [{"table": "customer360__customer_value_analysis", "column": "customer_health_score"}] | [] | False |
| B1 | AVG(churn_probability) | [{"table": "customer360__customer_value_analysis", "column": "churn_probability"}] | [] | False |


## S21

类别 `data`；来源 `query_db`；调用 `e6c1ce24420f41aeb3bdb56fc0e648e5`；状态 `success`。

```sql
SELECT marketo_lead_id, rfm_score, rfm_segment, rfm_avg_score, recency_score, frequency_score, monetary_score, estimated_customer_ltv, customer_health_score, churn_probability, customer_tier, customer_segment
FROM customer360__customer_value_analysis
WHERE marketo_lead_id = 7116
ORDER BY rfm_score
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-056/attempt-01/sql/S21.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-056/attempt-01/sql/S21.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-056/attempt-01/results/S21.rows.jsonl)；完整：True；SHA256：`6df7dcd3bd6b537cfcc383fc98e0e99b6d8330b0343071451027baa8b3570fe2`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "customer360__customer_value_analysis", "kind": "base", "block": null, "base_tables": ["customer360__customer_value_analysis"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |


## S22

类别 `data`；来源 `query_db`；调用 `e7b67aa2d9a342cb900c2639015e37e3`；状态 `success`。

```sql
WITH lead_tiers AS (
  SELECT marketo_lead_id, COUNT(DISTINCT customer_tier) AS ntiers, COUNT(DISTINCT customer_segment) AS nsegs,
         COUNT(DISTINCT rfm_score) AS nrfm
  FROM customer360__customer_value_analysis
  WHERE marketo_lead_id IS NOT NULL
  GROUP BY marketo_lead_id
)
SELECT SUM(CASE WHEN ntiers>1 THEN 1 ELSE 0 END) AS multi_tier_leads,
       SUM(CASE WHEN nsegs>1 THEN 1 ELSE 0 END) AS multi_seg_leads,
       SUM(CASE WHEN nrfm>1 THEN 1 ELSE 0 END) AS multi_rfm_leads,
       COUNT(*) AS total_leads
FROM lead_tiers
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-056/attempt-01/sql/S22.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-056/attempt-01/sql/S22.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-056/attempt-01/results/S22.rows.jsonl)；完整：True；SHA256：`78b8194c1fb9587d665543337c9370bbc8bb83b35fae542d921ce7634e8256a3`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "customer360__customer_value_analysis", "kind": "base", "block": null, "base_tables": ["customer360__customer_value_analysis"]}] | [] | ["marketo_lead_id"] |
| B2 | [{"alias": "lead_tiers", "kind": "derived", "block": "B1", "base_tables": ["customer360__customer_value_analysis"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(DISTINCT customer_tier) | [{"table": "customer360__customer_value_analysis", "column": "customer_tier"}] | [] | False |
| B1 | COUNT(DISTINCT customer_segment) | [{"table": "customer360__customer_value_analysis", "column": "customer_segment"}] | [] | False |
| B1 | COUNT(DISTINCT rfm_score) | [{"table": "customer360__customer_value_analysis", "column": "rfm_score"}] | [] | False |
| B2 | SUM(CASE WHEN ntiers > 1 THEN 1 ELSE 0 END) | [] | [{"table": "customer360__customer_value_analysis", "column": "customer_tier"}] | False |
| B2 | SUM(CASE WHEN nsegs > 1 THEN 1 ELSE 0 END) | [] | [{"table": "customer360__customer_value_analysis", "column": "customer_segment"}] | False |
| B2 | SUM(CASE WHEN nrfm > 1 THEN 1 ELSE 0 END) | [] | [{"table": "customer360__customer_value_analysis", "column": "rfm_score"}] | False |
| B2 | COUNT(*) | [] | [] | True |


## S23

类别 `data`；来源 `query_db`；调用 `3841f9b02d3544939dd02b55c73c1041`；状态 `success`。

```sql
SELECT rfm_segment, COUNT(*) AS n FROM customer360__customer_value_analysis GROUP BY rfm_segment ORDER BY n DESC
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-056/attempt-01/sql/S23.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-056/attempt-01/sql/S23.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-056/attempt-01/results/S23.rows.jsonl)；完整：True；SHA256：`aa312dd69becb0a18b10724dbbdf184af84af0f070eab65776400f88b7975bf7`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "customer360__customer_value_analysis", "kind": "base", "block": null, "base_tables": ["customer360__customer_value_analysis"]}] | [] | ["rfm_segment"] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |


## S24

类别 `data`；来源 `query_db`；调用 `6c34935315d346b1b653e1ce7c03aab8`；状态 `success`。

```sql
SELECT DISTINCT lifecycle_stage FROM customer360__customer_value_analysis ORDER BY 1
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-056/attempt-01/sql/S24.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-056/attempt-01/sql/S24.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-056/attempt-01/results/S24.rows.jsonl)；完整：True；SHA256：`98874ada66948ace887a4a0c46d7db1cd60bc736023ba6521c7e9deb832ad778`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "customer360__customer_value_analysis", "kind": "base", "block": null, "base_tables": ["customer360__customer_value_analysis"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |


## S25

类别 `data`；来源 `query_db`；调用 `9964d9da082844cfa65df09db70df6e9`；状态 `success`。

```sql
SELECT DISTINCT risk_category FROM customer360__customer_value_analysis ORDER BY 1
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-056/attempt-01/sql/S25.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-056/attempt-01/sql/S25.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-056/attempt-01/results/S25.rows.jsonl)；完整：True；SHA256：`00a6662948a99dad6526a79bdd806eebbb252d9fcaefe011ea05d20cd74c3715`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "customer360__customer_value_analysis", "kind": "base", "block": null, "base_tables": ["customer360__customer_value_analysis"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |


## S26

类别 `data`；来源 `query_db`；调用 `9ea7644c58f94005a13c4a68cd5b3cb7`；状态 `success`。

```sql
SELECT DISTINCT value_stability FROM customer360__customer_value_analysis ORDER BY 1
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-056/attempt-01/sql/S26.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-056/attempt-01/sql/S26.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-056/attempt-01/results/S26.rows.jsonl)；完整：True；SHA256：`a5a48158749cabe57d1ceec4f7690e27e2827f7b3f98ab78e0e9894f87625210`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "customer360__customer_value_analysis", "kind": "base", "block": null, "base_tables": ["customer360__customer_value_analysis"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |


## S27

类别 `data`；来源 `query_db`；调用 `e974b684dd0e4e1eb24924429c3290a5`；状态 `success`。

```sql
SELECT DISTINCT strategic_classification FROM customer360__customer_value_analysis ORDER BY 1
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-056/attempt-01/sql/S27.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-056/attempt-01/sql/S27.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-056/attempt-01/results/S27.rows.jsonl)；完整：True；SHA256：`eb3cb27a3759faf6777818bf242b5a06013e8c1e2dbca4477f34949df462bcee`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "customer360__customer_value_analysis", "kind": "base", "block": null, "base_tables": ["customer360__customer_value_analysis"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |


## S28

类别 `data`；来源 `query_db`；调用 `1b1186abe4924e9c8830af087f6a4933`；状态 `success`。

```sql
SELECT DISTINCT concentration_risk FROM customer360__customer_value_analysis ORDER BY 1
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-056/attempt-01/sql/S28.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-056/attempt-01/sql/S28.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-056/attempt-01/results/S28.rows.jsonl)；完整：True；SHA256：`efd0ee506411bb39b64635875af49e24618ee6244cd22885d22166babb646285`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "customer360__customer_value_analysis", "kind": "base", "block": null, "base_tables": ["customer360__customer_value_analysis"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |


## S29

类别 `data`；来源 `query_db`；调用 `d2f145788b3b49899cc2131f254e0d25`；状态 `success`。

```sql
SELECT DISTINCT recommended_engagement_model FROM customer360__customer_value_analysis ORDER BY 1
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-056/attempt-01/sql/S29.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-056/attempt-01/sql/S29.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-056/attempt-01/results/S29.rows.jsonl)；完整：True；SHA256：`398475700e742d6ad4dc7827496a16a92ff9e4594e21077b942e152e76b13452`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "customer360__customer_value_analysis", "kind": "base", "block": null, "base_tables": ["customer360__customer_value_analysis"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |


## S30

类别 `data`；来源 `query_db`；调用 `9d8052e2dccc461c8d282f746e6308b8`；状态 `success`。

```sql
SELECT DISTINCT investment_recommendation FROM customer360__customer_value_analysis ORDER BY 1
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-056/attempt-01/sql/S30.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-056/attempt-01/sql/S30.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-056/attempt-01/results/S30.rows.jsonl)；完整：True；SHA256：`4be30e68355bf236590c0742127c275ee8a0baf0103402be62203481ef213d9b`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "customer360__customer_value_analysis", "kind": "base", "block": null, "base_tables": ["customer360__customer_value_analysis"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |


## S31

类别 `data`；来源 `query_db`；调用 `27fc665975804274ac41751f090ff13e`；状态 `success`。

```sql
SELECT DISTINCT success_target FROM customer360__customer_value_analysis ORDER BY 1
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-056/attempt-01/sql/S31.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-056/attempt-01/sql/S31.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-056/attempt-01/results/S31.rows.jsonl)；完整：True；SHA256：`b00808923051f6b5d2f490157aeb37ae15f001b704aa3de7714c47502a634547`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "customer360__customer_value_analysis", "kind": "base", "block": null, "base_tables": ["customer360__customer_value_analysis"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |


## S32

类别 `data`；来源 `query_db`；调用 `240608619472466e8d59096980de189a`；状态 `success`。

```sql
SELECT DISTINCT development_opportunity FROM customer360__customer_value_analysis ORDER BY 1
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-056/attempt-01/sql/S32.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-056/attempt-01/sql/S32.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-056/attempt-01/results/S32.rows.jsonl)；完整：True；SHA256：`add580a0f41a2c58e5c7d9d66a5f5a6d2ec4f149b9e5522f9676702127d2b3ff`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "customer360__customer_value_analysis", "kind": "base", "block": null, "base_tables": ["customer360__customer_value_analysis"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |


## S33

类别 `data`；来源 `query_db`；调用 `655aa066188e458bb3776b5e6d14e282`；状态 `success`。

```sql
SELECT DISTINCT upsell_potential FROM customer360__customer_value_analysis ORDER BY 1
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-056/attempt-01/sql/S33.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-056/attempt-01/sql/S33.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-056/attempt-01/results/S33.rows.jsonl)；完整：True；SHA256：`b82bfdb807179d77aec9f3dee36eac61581d4f84aebbf3feee063009121a9667`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "customer360__customer_value_analysis", "kind": "base", "block": null, "base_tables": ["customer360__customer_value_analysis"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |


## S34

类别 `data`；来源 `query_db`；调用 `ebf1c8013c77488f8b67b78c837285f7`；状态 `success`。

```sql
-- Deduplicate: keep one row per lead, picking the one with highest rfm_avg_score
WITH dedup AS (
  SELECT *, ROW_NUMBER() OVER (PARTITION BY marketo_lead_id ORDER BY rfm_avg_score DESC, rfm_score DESC) AS rn
  FROM customer360__customer_value_analysis
  WHERE marketo_lead_id IS NOT NULL
)
SELECT * FROM dedup WHERE rn = 1
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-056/attempt-01/sql/S34.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-056/attempt-01/sql/S34.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-056/attempt-01/results/S34.rows.jsonl)；完整：True；SHA256：`4a65228694e74d5eb8e4122d103f4e83362839814abb8ccba40b5b8630a60a36`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "customer360__customer_value_analysis", "kind": "base", "block": null, "base_tables": ["customer360__customer_value_analysis"]}] | [] | [] |
| B2 | [{"alias": "dedup", "kind": "derived", "block": "B1", "base_tables": ["customer360__customer_value_analysis"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |


## S35

类别 `data`；来源 `query_db`；调用 `257329494b544470a2d16e749dfb2eec`；状态 `success`。

```sql
WITH dedup AS (
  SELECT *, ROW_NUMBER() OVER (PARTITION BY marketo_lead_id ORDER BY rfm_avg_score DESC, rfm_score DESC) AS rn
  FROM customer360__customer_value_analysis
  WHERE marketo_lead_id IS NOT NULL
),
groups AS (
  SELECT *,
    CASE WHEN customer_tier IN ('Gold','Platinum') AND portfolio_contribution_pct > 0.05 THEN 'HVE'
         ELSE 'SMB' END AS customer_group
  FROM dedup WHERE rn = 1
)
SELECT customer_group, COUNT(*) AS n,
  AVG(recency_score) AS avg_recency,
  AVG(frequency_score) AS avg_frequency,
  AVG(monetary_score) AS avg_monetary,
  AVG(rfm_avg_score) AS avg_rfm,
  AVG(estimated_customer_ltv) AS avg_ltv,
  AVG(customer_health_score) AS avg_health,
  AVG(churn_probability) AS avg_churn,
  AVG(account_age_days) AS avg_age,
  AVG(days_since_last_activity) AS avg_days_inactive,
  AVG(portfolio_contribution_pct) AS avg_portfolio,
  AVG(investment_priority_score) AS avg_priority,
  AVG(expected_annual_revenue) AS avg_annual_rev
FROM groups
GROUP BY customer_group
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-056/attempt-01/sql/S35.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-056/attempt-01/sql/S35.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-056/attempt-01/results/S35.rows.jsonl)；完整：True；SHA256：`4e0f147a694f66ed3a77b7bdd92e214dff83d8527c7df86c035310e060e10181`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "customer360__customer_value_analysis", "kind": "base", "block": null, "base_tables": ["customer360__customer_value_analysis"]}] | [] | [] |
| B2 | [{"alias": "dedup", "kind": "derived", "block": "B1", "base_tables": ["customer360__customer_value_analysis"]}] | [] | [] |
| B3 | [{"alias": "groups", "kind": "derived", "block": "B2", "base_tables": ["customer360__customer_value_analysis"]}] | [] | ["customer_group"] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B3 | COUNT(*) | [] | [] | True |
| B3 | AVG(recency_score) | [{"table": "customer360__customer_value_analysis", "column": "recency_score"}] | [] | False |
| B3 | AVG(frequency_score) | [{"table": "customer360__customer_value_analysis", "column": "frequency_score"}] | [] | False |
| B3 | AVG(monetary_score) | [{"table": "customer360__customer_value_analysis", "column": "monetary_score"}] | [] | False |
| B3 | AVG(rfm_avg_score) | [{"table": "customer360__customer_value_analysis", "column": "rfm_avg_score"}] | [] | False |
| B3 | AVG(estimated_customer_ltv) | [{"table": "customer360__customer_value_analysis", "column": "estimated_customer_ltv"}] | [] | False |
| B3 | AVG(customer_health_score) | [{"table": "customer360__customer_value_analysis", "column": "customer_health_score"}] | [] | False |
| B3 | AVG(churn_probability) | [{"table": "customer360__customer_value_analysis", "column": "churn_probability"}] | [] | False |
| B3 | AVG(account_age_days) | [{"table": "customer360__customer_value_analysis", "column": "account_age_days"}] | [] | False |
| B3 | AVG(days_since_last_activity) | [{"table": "customer360__customer_value_analysis", "column": "days_since_last_activity"}] | [] | False |
| B3 | AVG(portfolio_contribution_pct) | [{"table": "customer360__customer_value_analysis", "column": "portfolio_contribution_pct"}] | [] | False |
| B3 | AVG(investment_priority_score) | [{"table": "customer360__customer_value_analysis", "column": "investment_priority_score"}] | [] | False |
| B3 | AVG(expected_annual_revenue) | [{"table": "customer360__customer_value_analysis", "column": "expected_annual_revenue"}] | [] | False |

