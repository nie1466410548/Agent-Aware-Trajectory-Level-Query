# dacomp-090

We have observed that the payment behavior of some customers is deteriorating. Please filt…

运行：已提交。官方未评分。全部 SQL 尝试/成功 46/45；数据 SQL 44/43；Python 2 次。

完整原题：

We have observed that the payment behavior of some customers is deteriorating. Please filter the customer group from the `quickbooks__customer_analytics` table with a `payment_rate_percentage` below 75% and an `outstanding_balance` exceeding 15,000. Calculate a composite risk score for these high-risk customers (Formula: Risk Score = (100 - `payment_rate_percentage`) * 0.4 + (850 - `credit_score`) / 850 * 100 * 0.4 + (100 - `business_stability_score`) * 0.2). In conjunction with the `quickbooks__profitability_analysis` table, calculate the proportion of these customers' `gross_profit` to the total profit of all customers. Simultaneously, analyze the month-over-month trend of the `collection_rate_percentage` from the `quickbooks__financial_dashboard` table for the last 12 months, identifying the number of consecutive months of deterioration and the magnitude of the decline. Further analyze the distribution characteristics of these problem customers across dimensions such as `customer_lifespan_days`, `total_invoices`, `avg_invoice_amount`, and `profitability_tier`, exploring their differential patterns compared to normal customers. Finally, using the forecast data from the `quickbooks__cashflow_forecast` table, build a risk warning model to assess the potential loss scale for the next 6 months, and from a business perspective, propose tiered customer management and risk control strategies.

| 表 | 行数 | 列数 |
| --- | --- | --- |
| quickbooks__cashflow_forecast | 6 | 19 |
| quickbooks__customer_analytics | 2800 | 67 |
| quickbooks__financial_dashboard | 33 | 41 |
| quickbooks__profitability_analysis | 8000 | 35 |


实际路线（分析者依据 SQL/源码概括，不代表 Agent 自述）：SQL 识别高风险付款客户、利润及回收趋势 → Python 汇总损失和回收情景 → 现金流风险图表与建议。

数据库大小：4,247,552 字节。

## 数据 SQL

| SQL | 状态 | 基础表 | Join 输入/类型 | GROUP BY | 聚合表达式 | 结果行数 | 数据库 ms |
| --- | --- | --- | --- | --- | --- | --- | --- |
| [S3/Q1](#s3) | success | ["quickbooks__customer_analytics"] | 0 / {} | [] | ["COUNT(*)"] | 1 | 1.457 |
| [S4/Q2](#s4) | success | ["quickbooks__profitability_analysis"] | 0 / {} | [] | ["COUNT(*)"] | 1 | 1.537 |
| [S5/Q3](#s5) | success | ["quickbooks__financial_dashboard"] | 0 / {} | [] | ["COUNT(*)"] | 1 | 0.296 |
| [S6/Q4](#s6) | success | ["quickbooks__cashflow_forecast"] | 0 / {} | [] | ["COUNT(*)"] | 1 | 0.296 |
| [S7/Q5](#s7) | success | ["quickbooks__customer_analytics"] | 0 / {} | [] | [] | 5 | 0.566 |
| [S8/Q6](#s8) | success | ["quickbooks__financial_dashboard"] | 0 / {} | [] | [] | 5 | 0.593 |
| [S9/Q7](#s9) | success | ["quickbooks__cashflow_forecast"] | 0 / {} | [] | [] | 6 | 0.424 |
| [S10/Q8](#s10) | success | ["quickbooks__profitability_analysis"] | 0 / {} | [] | [] | 5 | 0.455 |
| [S11/Q9](#s11) | failed | ["quickbooks__customer_analytics"] | 0 / {} | [] | [] | unknown | 未取得；调用总时长 0.206 ms |
| [S12/Q10](#s12) | success | ["quickbooks__customer_analytics"] | 0 / {} | [] | ["COUNT(*)"] | 1 | 1.105 |
| [S13/Q11](#s13) | success | ["quickbooks__customer_analytics"] | 0 / {} | [] | [] | 399 | 2.737 |
| [S14/Q12](#s14) | success | ["quickbooks__customer_analytics"] | 0 / {} | [] | ["COUNT(*)", "AVG((100 - payment_rate_percentage) * 0.4 + (850 - credit_score) / 850.0 * 100 * 0.4 + (100 - business_stability_score) * 0.2)", "MIN((100 - payment_rate_percentage) * 0.4 + (850 - credit_score) / 850.0 * 100 * 0.4 + (100 - business_stability_score) * 0.2)", "MAX((100 - payment_rate_percentage) * 0.4 + (850 - credit_score) / 850.0 * 100 * 0.4 + (100 - business_stability_score) * 0.2)", "AVG(payment_rate_percentage)", "AVG(outstanding_balance)", "SUM(outstanding_balance)", "AVG(credit_score)", "AVG(business_stability_score)"] | 1 | 1.353 |
| [S15/Q13](#s15) | success | ["quickbooks__customer_analytics"] | 0 / {} | [] | ["COUNT(*)", "AVG(payment_rate_percentage)", "AVG(outstanding_balance)", "SUM(outstanding_balance)"] | 1 | 1.119 |
| [S16/Q14](#s16) | success | ["quickbooks__customer_analytics", "quickbooks__profitability_analysis"] | 2 / {'INNER': 1} | [] | ["COUNT(DISTINCT p.customer_id)", "COUNT(*)", "SUM(p.gross_profit)", "SUM(p.invoice_total)"] | 1 | 11.004 |
| [S17/Q15](#s17) | success | ["quickbooks__profitability_analysis"] | 0 / {} | [] | ["SUM(gross_profit)", "SUM(invoice_total)"] | 1 | 3.223 |
| [S18/Q16](#s18) | success | ["quickbooks__customer_analytics", "quickbooks__profitability_analysis"] | 2 / {'INNER': 1} | ["p.customer_id"] | ["COUNT(*)", "SUM(p.gross_profit)", "SUM(p.invoice_total)"] | 20 | 11.778 |
| [S19/Q17](#s19) | success | ["quickbooks__financial_dashboard"] | 0 / {} | [] | [] | 33 | 0.422 |
| [S20/Q18](#s20) | success | ["quickbooks__financial_dashboard"] | 0 / {} | [] | [] | 13 | 0.61 |
| [S21/Q19](#s21) | success | ["quickbooks__financial_dashboard"] | 0 / {} | [] | [] | 33 | 0.459 |
| [S22/Q20](#s22) | success | ["quickbooks__financial_dashboard"] | 0 / {} | [] | [] | 12 | 0.424 |
| [S23/Q21](#s23) | success | ["quickbooks__customer_analytics"] | 0 / {} | [] | ["COUNT(*)", "AVG(customer_lifespan_days)", "AVG(total_invoices)", "AVG(avg_invoice_amount)", "AVG(credit_score)", "AVG(business_stability_score)", "AVG(outstanding_balance)", "AVG(payment_rate_percentage)", "AVG(active_months)", "AVG(customer_lifespan_days)", "COUNT(*)", "AVG(customer_lifespan_days)", "AVG(total_invoices)", "AVG(avg_invoice_amount)", "AVG(credit_score)", "AVG(business_stability_score)", "AVG(outstanding_balance)", "AVG(payment_rate_percentage)", "AVG(active_months)", "AVG(customer_lifespan_days)"] | 2 | 2.885 |
| [S24/Q22](#s24) | success | ["quickbooks__customer_analytics", "quickbooks__profitability_analysis"] | 2 / {'INNER': 1} | ["c.risk_group", "p.profitability_tier"] | ["COUNT(*)", "SUM(p.gross_profit)"] | 8 | 18.269 |
| [S25/Q23](#s25) | success | ["quickbooks__customer_analytics"] | 0 / {} | ["CASE WHEN payment_rate_percentage < 75 AND outstanding_balance > 15000 THEN 'High-Risk' ELSE 'Normal' END", "lifecycle_stage"] | ["COUNT(*)", "COUNT(*)", "COUNT(*)"] | 14 | 2.946 |
| [S26/Q24](#s26) | success | ["quickbooks__customer_analytics"] | 0 / {} | ["CASE WHEN payment_rate_percentage < 75 AND outstanding_balance > 15000 THEN 'High-Risk' ELSE 'Normal' END", "activity_status"] | ["COUNT(*)", "COUNT(*)", "COUNT(*)"] | 10 | 2.881 |
| [S27/Q25](#s27) | success | ["quickbooks__customer_analytics"] | 0 / {} | ["CASE WHEN payment_rate_percentage < 75 AND outstanding_balance > 15000 THEN 'High-Risk' ELSE 'Normal' END", "customer_value_segment"] | ["COUNT(*)", "COUNT(*)", "COUNT(*)"] | 6 | 2.379 |
| [S28/Q26](#s28) | success | ["quickbooks__customer_analytics"] | 0 / {} | ["CASE WHEN payment_rate_percentage < 75 AND outstanding_balance > 15000 THEN 'High-Risk' ELSE 'Normal' END", "credit_grade"] | ["COUNT(*)", "COUNT(*)", "COUNT(*)"] | 14 | 3.218 |
| [S29/Q27](#s29) | success | ["quickbooks__customer_analytics"] | 0 / {} | ["risk_group"] | ["MIN(customer_lifespan_days)", "MAX(customer_lifespan_days)", "AVG(customer_lifespan_days)", "AVG(total_invoices)", "AVG(avg_invoice_amount)", "MIN(avg_invoice_amount)", "MAX(avg_invoice_amount)", "AVG(overdue_count_12m)", "AVG(avg_payment_days_12m)", "AVG(days_since_last_invoice)", "AVG(revenue_growth_rate_12m)"] | 2 | 3.66 |
| [S30/Q28](#s30) | success | ["quickbooks__customer_analytics"] | 0 / {} | [] | [] | 399 | 2.053 |
| [S31/Q29](#s31) | success | ["quickbooks__cashflow_forecast"] | 0 / {} | [] | [] | 6 | 0.379 |
| [S32/Q30](#s32) | success | ["quickbooks__customer_analytics"] | 0 / {} | ["CASE WHEN risk_score < 40 THEN 'Low (30-40)' WHEN risk_score < 50 THEN 'Medium (40-50)' WHEN risk_score < 60 THEN 'High (50-60)' ELSE 'Critical (60+)' END"] | ["COUNT(*)", "SUM(outstanding_balance)", "MIN(risk_score)"] | 4 | 1.583 |
| [S33/Q31](#s33) | success | ["quickbooks__customer_analytics"] | 0 / {} | [] | ["SUM(outstanding_balance)", "SUM(outstanding_balance * ((100 - payment_rate_percentage) * 0.4 + (850 - credit_score) / 850.0 * 100 * 0.4 + (100 - business_stability_score) * 0.2) / 100.0)", "AVG((100 - payment_rate_percentage) * 0.4 + (850 - credit_score) / 850.0 * 100 * 0.4 + (100 - business_stability_score) * 0.2)"] | 1 | 1.342 |
| [S34/Q32](#s34) | success | ["quickbooks__customer_analytics"] | 0 / {} | ["risk_group"] | ["AVG(total_invoice_amount)", "AVG(monthly_revenue_avg)", "AVG(revenue_current_year)", "AVG(revenue_prev_year)", "AVG(revenue_growth_yoy_pct)", "AVG(total_payments)", "AVG(total_quantity_purchased)", "AVG(unique_products_purchased)", "AVG(payment_timeliness_score)"] | 2 | 3.937 |
| [S35/Q33](#s35) | success | ["quickbooks__customer_analytics"] | 0 / {} | [] | [] | 2800 | 11.671 |
| [S36/Q34](#s36) | success | ["quickbooks__customer_analytics"] | 0 / {} | [] | [] | 399 | 1.328 |
| [S37/Q35](#s37) | success | ["quickbooks__financial_dashboard"] | 0 / {} | [] | [] | 33 | 0.416 |
| [S38/Q36](#s38) | success | ["quickbooks__cashflow_forecast"] | 0 / {} | [] | [] | 6 | 0.448 |
| [S39/Q37](#s39) | success | ["quickbooks__customer_analytics", "quickbooks__profitability_analysis"] | 2 / {'INNER': 1} | ["CASE WHEN c.payment_rate_percentage < 75 AND c.outstanding_balance > 15000 THEN 'High-Risk' ELSE 'Normal' END", "p.profitability_tier"] | ["COUNT(*)", "SUM(p.gross_profit)"] | 8 | 13.814 |
| [S40/Q38](#s40) | success | ["quickbooks__customer_analytics"] | 0 / {} | ["CASE WHEN risk_score < 40 THEN 'Low (30-40)' WHEN risk_score < 50 THEN 'Medium (40-50)' WHEN risk_score < 60 THEN 'High (50-60)' ELSE 'Critical (60+)' END"] | ["COUNT(*)", "SUM(outstanding_balance)", "AVG(risk_score)", "MIN(risk_score)"] | 4 | 1.968 |
| [S41/Q39](#s41) | success | ["quickbooks__customer_analytics", "quickbooks__profitability_analysis"] | 2 / {'INNER': 1} | ["c.risk_group"] | ["COUNT(DISTINCT p.customer_id)", "SUM(p.gross_profit)", "SUM(p.risk_adjusted_profit)"] | 2 | 19.51 |
| [S42/Q40](#s42) | success | ["quickbooks__customer_analytics", "quickbooks__profitability_analysis"] | 2 / {'INNER': 1} | ["c.risk_group", "p.profitability_tier"] | ["COUNT(*)", "SUM(p.gross_profit)", "AVG(p.invoice_gross_margin_pct)", "COUNT(*)", "COUNT(*)"] | 8 | 18.386 |
| [S43/Q41](#s43) | success | ["quickbooks__customer_analytics"] | 0 / {} | [] | [] | 399 | 1.809 |
| [S44/Q42](#s44) | success | ["quickbooks__financial_dashboard"] | 0 / {} | [] | [] | 33 | 0.303 |
| [S45/Q43](#s45) | success | ["quickbooks__cashflow_forecast"] | 0 / {} | [] | [] | 6 | 0.207 |
| [S46/Q44](#s46) | success | ["quickbooks__customer_analytics"] | 0 / {} | ["CASE WHEN risk_score < 40 THEN 'Low (30-40)' WHEN risk_score < 50 THEN 'Medium (40-50)' WHEN risk_score < 60 THEN 'High (50-60)' ELSE 'Critical (60+)' END"] | ["COUNT(*)", "SUM(outstanding_balance)", "AVG(risk_score)", "AVG(avg_payment_days_12m)", "AVG(overdue_count_12m)", "MIN(risk_score)"] | 4 | 1.717 |


## 元数据和设置

| SQL | 类别 | 状态 | 内容 |
| --- | --- | --- | --- |
| S1 | connection_setup | success | PRAGMA query_only=ON |
| S2 | metadata | success | SELECT name,sql FROM sqlite_master WHERE type='table' ORDER BY name |


## Python 与执行位置

人工源码审查：**database_first_violation**。SQL 完成客户筛选、风险分数与趋势的主要计算。Python 仍求和欠款和预计损失、计算最近月份差分均值并构造常规回收率情景；这些 SQL 可支持的算术、窗口和聚合应优先留在数据库，检验及绘图单独评价。 [证据](../reviews/dacomp-090.json)。

P1：Performing statistical comparison (Mann-Whitney U tests) between high-risk and normal customer groups on numerical dimensions like customer_lifespan_days, total_invoices, avg_invoice_amount, credit_score, business_stability_score, etc. This requires distribution-free hypothesis testing which is not supported in SQL. Also creating visualizations for risk score distribution, collection rate trends, and comparative boxplots.

[源码](../../../runs/dsv4flash-db-first-full-01/dacomp-090/attempt-01/python/P1.py)；[输出](../../../runs/dsv4flash-db-first-full-01/dacomp-090/attempt-01/python/P1.stdout)；[错误](../../../runs/dsv4flash-db-first-full-01/dacomp-090/attempt-01/python/P1.stderr)。检出需人工核验的 SQL 可实现操作：.query(, sort_values(；不能仅凭理由判为合规。

P2：Building a risk warning scenario model to assess potential loss scale over the next 6 months. This requires combining multiple data sources (outstanding balance, risk scores, collection rate trends, cashflow forecasts) into a structured scenario analysis with multiple recovery assumptions, which is better done in Python than SQL.

[源码](../../../runs/dsv4flash-db-first-full-01/dacomp-090/attempt-01/python/P2.py)；[输出](../../../runs/dsv4flash-db-first-full-01/dacomp-090/attempt-01/python/P2.stdout)；[错误](../../../runs/dsv4flash-db-first-full-01/dacomp-090/attempt-01/python/P2.stderr)。检出需人工核验的 SQL 可实现操作：.query(；不能仅凭理由判为合规。

## 优化机会

已验证候选。筛选限于精确 SQL、相同自包含 CTE、相同单表完整过滤、可分解单表聚合；未覆盖任意 Join 等价和一般谓词蕴含。全部候选都是 offline，未测在线预测。

| 候选 | 类型 | 已有结果 | 覆盖 SQL | 后续次数 | 中间行数 | 验证 | 成本 |
| --- | --- | --- | --- | --- | --- | --- | --- |
| C1 | exact-result reuse | True | ["S38", "S45"] | 1 | unknown | not_verified_cap | Not tested |
| C2 | aggregate MV | False | ["S3", "S15"] | 1 | unknown | not_verified_cap | Not tested |
| C3 | aggregate MV | False | ["S4", "S17"] | 1 | 1 | verified | Not benchmarked; correctness alone does not establish net speedup. |
| C4 | common filtered view | False | ["S12", "S13", "S14", "S30", "S33", "S36", "S43"] | 6 | 399 | verified | Not benchmarked; correctness alone does not establish net speedup. |
| C5 | aggregate MV | False | ["S12", "S14", "S33"] | 2 | 1 | verified | Not benchmarked; correctness alone does not establish net speedup. |


已验证覆盖（含触发查询、候选并集去重）：9/43 条成功数据 SQL。正确性仅针对当前数据库快照；未测性能的候选不能声称已加速。

[完整 build/rewrite 与比较证据](dacomp-090.analysis.json)。

### C4：common filtered view

Same single source and complete filter; original filter retained.

原查询 [S12](#s12), [S13](#s13), [S14](#s14), [S30](#s30), [S33](#s33), [S36](#s36), [S43](#s43) → 新增共享状态 C4 → 后续 6 次可复用。该构建点为事后假设，不代表 Agent 当时预知后续。

构建定义：

```sql
SELECT * FROM "quickbooks__customer_analytics" WHERE payment_rate_percentage < 75 AND outstanding_balance > 15000
```

受益查询 S12 的改写示例：

```sql
SELECT COUNT(*) AS high_risk_count FROM temp.reuse_candidate AS quickbooks__customer_analytics WHERE payment_rate_percentage < 75 AND outstanding_balance > 15000
```

| 原 SQL | 列名一致 | 结果一致 | 比较方法 |
| --- | --- | --- | --- |
| S12 | True | True | exact_multiset |
| S13 | True | True | ordered_numeric_tolerance |
| S14 | True | True | exact_multiset |
| S30 | True | True | ordered_numeric_tolerance |
| S33 | True | True | exact_multiset |
| S36 | True | True | exact_multiset |
| S43 | True | True | exact_multiset |


验证状态：verified；成本结论：Not benchmarked; correctness alone does not establish net speedup.

### C5：aggregate MV

Union of grouping keys; decomposable aggregate states; AVG uses SUM and non-NULL COUNT.

原查询 [S12](#s12), [S14](#s14), [S33](#s33) → 新增共享状态 C5 → 后续 2 次可复用。该构建点为事后假设，不代表 Agent 当时预知后续。

构建定义：

```sql
SELECT COUNT(*) AS __a0, SUM((100 - payment_rate_percentage) * 0.4 + (850 - credit_score) / 850.0 * 100 * 0.4 + (100 - business_stability_score) * 0.2) AS __a1_sum, COUNT((100 - payment_rate_percentage) * 0.4 + (850 - credit_score) / 850.0 * 100 * 0.4 + (100 - business_stability_score) * 0.2) AS __a1_n, MIN((100 - payment_rate_percentage) * 0.4 + (850 - credit_score) / 850.0 * 100 * 0.4 + (100 - business_stability_score) * 0.2) AS __a2, MAX((100 - payment_rate_percentage) * 0.4 + (850 - credit_score) / 850.0 * 100 * 0.4 + (100 - business_stability_score) * 0.2) AS __a3, SUM(payment_rate_percentage) AS __a4_sum, COUNT(payment_rate_percentage) AS __a4_n, SUM(outstanding_balance) AS __a5_sum, COUNT(outstanding_balance) AS __a5_n, SUM(outstanding_balance) AS __a6, SUM(credit_score) AS __a7_sum, COUNT(credit_score) AS __a7_n, SUM(business_stability_score) AS __a8_sum, COUNT(business_stability_score) AS __a8_n, SUM(outstanding_balance * ((100 - payment_rate_percentage) * 0.4 + (850 - credit_score) / 850.0 * 100 * 0.4 + (100 - business_stability_score) * 0.2) / 100.0) AS __a9 FROM "quickbooks__customer_analytics" WHERE payment_rate_percentage < 75 AND outstanding_balance > 15000
```

受益查询 S12 的改写示例：

```sql
SELECT SUM(__a0) AS high_risk_count FROM temp.reuse_candidate
```

| 原 SQL | 列名一致 | 结果一致 | 比较方法 |
| --- | --- | --- | --- |
| S12 | True | True | exact_multiset |
| S14 | True | True | exact_multiset |
| S33 | True | True | exact_multiset |


验证状态：verified；成本结论：Not benchmarked; correctness alone does not establish net speedup.

### C3：aggregate MV

Union of grouping keys; decomposable aggregate states; AVG uses SUM and non-NULL COUNT.

原查询 [S4](#s4), [S17](#s17) → 新增共享状态 C3 → 后续 1 次可复用。该构建点为事后假设，不代表 Agent 当时预知后续。

构建定义：

```sql
SELECT COUNT(*) AS __a0, SUM(gross_profit) AS __a1, SUM(invoice_total) AS __a2 FROM "quickbooks__profitability_analysis" 
```

受益查询 S4 的改写示例：

```sql
SELECT SUM(__a0) AS n_rows FROM temp.reuse_candidate
```

| 原 SQL | 列名一致 | 结果一致 | 比较方法 |
| --- | --- | --- | --- |
| S4 | True | True | exact_multiset |
| S17 | True | True | exact_multiset |


验证状态：verified；成本结论：Not benchmarked; correctness alone does not establish net speedup.

结果依赖：自动记录 SQL→Python 的接口父调用，以及源码中引用归档文件的消费者；字面值相同不认定因果。模型方向选择需要人工读取消息，尚未做全面因果标注。

[原始报告](../../../runs/dsv4flash-db-first-full-01/dacomp-090/attempt-01/answer.md)；[统一消息](../../../runs/dsv4flash-db-first-full-01/dacomp-090/attempt-01/messages.jsonl)；[原始 OpenCode 事件](../../../runs/dsv4flash-db-first-full-01/dacomp-090/attempt-01/opencode.jsonl)；[SQL 引擎日志](../../../runs/dsv4flash-db-first-full-01/dacomp-090/attempt-01/sql_journal.jsonl)。

[可读报告（本地图片链接规范化）](../answers/dacomp-090.md)。原始回答保留，分析结论未改写。

## S1

类别 `connection_setup`；来源 `connection`；调用 `5f9d3027aa9e40f39b40d28686a25cd1`；状态 `success`。

```sql
PRAGMA query_only=ON
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-090/attempt-01/sql/S1.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-090/attempt-01/sql/S1.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-090/attempt-01/results/S1.rows.jsonl)；完整：True；SHA256：`e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`。

## S2

类别 `metadata`；来源 `list_db`；调用 `5f9d3027aa9e40f39b40d28686a25cd1`；状态 `success`。

```sql
SELECT name,sql FROM sqlite_master WHERE type='table' ORDER BY name
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-090/attempt-01/sql/S2.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-090/attempt-01/sql/S2.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-090/attempt-01/results/S2.rows.jsonl)；完整：True；SHA256：`3861a1bd266e62a63963adb5e5f0f00e4d06d577da7279d4c4131625b87e46cc`。

## S3

类别 `data`；来源 `query_db`；调用 `cb0d729cbe37478d8df8d8947f4ca110`；状态 `success`。

```sql
SELECT COUNT(*) AS n_customers FROM quickbooks__customer_analytics
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-090/attempt-01/sql/S3.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-090/attempt-01/sql/S3.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-090/attempt-01/results/S3.rows.jsonl)；完整：True；SHA256：`409ab31294c9429f03e9f17a7e49ebfac259b29f8ad8ca8c4d51de2ef93bb943`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "quickbooks__customer_analytics", "kind": "base", "block": null, "base_tables": ["quickbooks__customer_analytics"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |


## S4

类别 `data`；来源 `query_db`；调用 `acbad42c1b544519aa8cd5d082a929da`；状态 `success`。

```sql
SELECT COUNT(*) AS n_rows FROM quickbooks__profitability_analysis
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-090/attempt-01/sql/S4.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-090/attempt-01/sql/S4.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-090/attempt-01/results/S4.rows.jsonl)；完整：True；SHA256：`ca5d97f4dab69813055999493cfea8f56e91e334c1465da9867b484a21b0a9bd`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "quickbooks__profitability_analysis", "kind": "base", "block": null, "base_tables": ["quickbooks__profitability_analysis"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |


## S5

类别 `data`；来源 `query_db`；调用 `2d97914243be4ef18c9446bcd5532e23`；状态 `success`。

```sql
SELECT COUNT(*) AS n_rows FROM quickbooks__financial_dashboard
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-090/attempt-01/sql/S5.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-090/attempt-01/sql/S5.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-090/attempt-01/results/S5.rows.jsonl)；完整：True；SHA256：`1315f0f7efc386feec13fc4575d19a3dcdd07d1b61de1fe595d7dec48df1079a`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "quickbooks__financial_dashboard", "kind": "base", "block": null, "base_tables": ["quickbooks__financial_dashboard"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |


## S6

类别 `data`；来源 `query_db`；调用 `2462dfde5bde4344803ac5cf6ed036ee`；状态 `success`。

```sql
SELECT COUNT(*) AS n_rows FROM quickbooks__cashflow_forecast
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-090/attempt-01/sql/S6.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-090/attempt-01/sql/S6.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-090/attempt-01/results/S6.rows.jsonl)；完整：True；SHA256：`c70b148cd0bd4ffd32bea27e9205a15f3b467f06c096d4225b505e077da12af1`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "quickbooks__cashflow_forecast", "kind": "base", "block": null, "base_tables": ["quickbooks__cashflow_forecast"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |


## S7

类别 `data`；来源 `query_db`；调用 `d12d3433dce844c1b258e7182042f2b4`；状态 `success`。

```sql
SELECT * FROM quickbooks__customer_analytics LIMIT 5
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-090/attempt-01/sql/S7.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-090/attempt-01/sql/S7.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-090/attempt-01/results/S7.rows.jsonl)；完整：True；SHA256：`f7b77326f5b74c95f15e2048ead723f477487cbe4e657b0895f56adb89002b18`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "quickbooks__customer_analytics", "kind": "base", "block": null, "base_tables": ["quickbooks__customer_analytics"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |


## S8

类别 `data`；来源 `query_db`；调用 `35369d152c574cefab6547cbe656ff57`；状态 `success`。

```sql
SELECT * FROM quickbooks__financial_dashboard ORDER BY dashboard_month LIMIT 5
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-090/attempt-01/sql/S8.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-090/attempt-01/sql/S8.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-090/attempt-01/results/S8.rows.jsonl)；完整：True；SHA256：`62d82d568253e9e5345aefeffd0aaf0fdf62eb97a0787aa95ba82f3993f77581`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "quickbooks__financial_dashboard", "kind": "base", "block": null, "base_tables": ["quickbooks__financial_dashboard"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |


## S9

类别 `data`；来源 `query_db`；调用 `666d9286106744c3ae7b5394bb240161`；状态 `success`。

```sql
SELECT * FROM quickbooks__cashflow_forecast
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-090/attempt-01/sql/S9.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-090/attempt-01/sql/S9.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-090/attempt-01/results/S9.rows.jsonl)；完整：True；SHA256：`5aa53dba4aede209161c136b82fd246568fc911635de52c62ed05a8121f486f7`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "quickbooks__cashflow_forecast", "kind": "base", "block": null, "base_tables": ["quickbooks__cashflow_forecast"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |


## S10

类别 `data`；来源 `query_db`；调用 `3a0320e856e242c39e270ae9f1de4051`；状态 `success`。

```sql
SELECT * FROM quickbooks__profitability_analysis LIMIT 5
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-090/attempt-01/sql/S10.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-090/attempt-01/sql/S10.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-090/attempt-01/results/S10.rows.jsonl)；完整：True；SHA256：`a512260254e21bd2662447cc55c5cde5ab5fb11541373c646f7182a16fb4f80d`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "quickbooks__profitability_analysis", "kind": "base", "block": null, "base_tables": ["quickbooks__profitability_analysis"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |


## S11

类别 `data`；来源 `query_db`；调用 `7325ba69fc83470fbfbdbfce0c3a7c2c`；状态 `failed`。

```sql
SELECT customer_id, customer_name, company_name, payment_rate_percentage, outstanding_balance, credit_score, business_stability_score, total_invoices, total_invoice_amount, avg_invoice_amount, customer_lifespan_days, profitability_tier 
FROM quickbooks__customer_analytics 
WHERE payment_rate_percentage < 75 AND outstanding_balance > 15000
ORDER BY outstanding_balance DESC
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-090/attempt-01/sql/S11.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-090/attempt-01/sql/S11.parameters.json)。

错误：`OperationalError('no such column: profitability_tier')`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "quickbooks__customer_analytics", "kind": "base", "block": null, "base_tables": ["quickbooks__customer_analytics"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |


未解析列血缘：[{"block": "B1", "column": "profitability_tier", "reason": "ambiguous_or_missing_source"}]

## S12

类别 `data`；来源 `query_db`；调用 `36a7bb873390405199ad4a6234538b65`；状态 `success`。

```sql
SELECT COUNT(*) AS high_risk_count FROM quickbooks__customer_analytics WHERE payment_rate_percentage < 75 AND outstanding_balance > 15000
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-090/attempt-01/sql/S12.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-090/attempt-01/sql/S12.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-090/attempt-01/results/S12.rows.jsonl)；完整：True；SHA256：`9e476dce428e64c9fe542e2591f9c82b335c87be59b04690cd4796fef77127f0`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "quickbooks__customer_analytics", "kind": "base", "block": null, "base_tables": ["quickbooks__customer_analytics"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |


## S13

类别 `data`；来源 `query_db`；调用 `0d8fba1ecc1b4d36bd0a9c28be8f3796`；状态 `success`。

```sql
SELECT customer_id, customer_name, company_name, payment_rate_percentage, outstanding_balance, credit_score, business_stability_score, total_invoices, total_invoice_amount, avg_invoice_amount, customer_lifespan_days, payment_behavior, credit_grade, activity_status, lifecycle_stage, customer_value_segment 
FROM quickbooks__customer_analytics 
WHERE payment_rate_percentage < 75 AND outstanding_balance > 15000
ORDER BY outstanding_balance DESC
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-090/attempt-01/sql/S13.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-090/attempt-01/sql/S13.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-090/attempt-01/results/S13.rows.jsonl)；完整：True；SHA256：`31846a0a4b1233ce1bcbbcf45f5b90243c2124ce168d47295e150163c1954eb5`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "quickbooks__customer_analytics", "kind": "base", "block": null, "base_tables": ["quickbooks__customer_analytics"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |


## S14

类别 `data`；来源 `query_db`；调用 `d30fb838c2bf42c1bbc04cf0f99bdda9`；状态 `success`。

```sql
SELECT 
  COUNT(*) AS n,
  ROUND(AVG((100 - payment_rate_percentage) * 0.4 + (850 - credit_score) / 850.0 * 100 * 0.4 + (100 - business_stability_score) * 0.2), 3) AS avg_risk_score,
  ROUND(MIN((100 - payment_rate_percentage) * 0.4 + (850 - credit_score) / 850.0 * 100 * 0.4 + (100 - business_stability_score) * 0.2), 3) AS min_risk_score,
  ROUND(MAX((100 - payment_rate_percentage) * 0.4 + (850 - credit_score) / 850.0 * 100 * 0.4 + (100 - business_stability_score) * 0.2), 3) AS max_risk_score,
  ROUND(AVG(payment_rate_percentage),2) AS avg_payment_rate,
  ROUND(AVG(outstanding_balance),2) AS avg_outstanding_balance,
  ROUND(SUM(outstanding_balance),2) AS total_outstanding_balance,
  ROUND(AVG(credit_score),2) AS avg_credit_score,
  ROUND(AVG(business_stability_score),2) AS avg_stability_score
FROM quickbooks__customer_analytics 
WHERE payment_rate_percentage < 75 AND outstanding_balance > 15000
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-090/attempt-01/sql/S14.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-090/attempt-01/sql/S14.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-090/attempt-01/results/S14.rows.jsonl)；完整：True；SHA256：`b76519062fbfffd07a8c10cc199ef71d39c07ba6a47259753f055763d9a74a33`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "quickbooks__customer_analytics", "kind": "base", "block": null, "base_tables": ["quickbooks__customer_analytics"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |
| B1 | AVG((100 - payment_rate_percentage) * 0.4 + (850 - credit_score) / 850.0 * 100 * 0.4 + (100 - business_stability_score) * 0.2) | [{"table": "quickbooks__customer_analytics", "column": "business_stability_score"}, {"table": "quickbooks__customer_analytics", "column": "payment_rate_percentage"}, {"table": "quickbooks__customer_analytics", "column": "credit_score"}] | [] | False |
| B1 | MIN((100 - payment_rate_percentage) * 0.4 + (850 - credit_score) / 850.0 * 100 * 0.4 + (100 - business_stability_score) * 0.2) | [{"table": "quickbooks__customer_analytics", "column": "business_stability_score"}, {"table": "quickbooks__customer_analytics", "column": "payment_rate_percentage"}, {"table": "quickbooks__customer_analytics", "column": "credit_score"}] | [] | False |
| B1 | MAX((100 - payment_rate_percentage) * 0.4 + (850 - credit_score) / 850.0 * 100 * 0.4 + (100 - business_stability_score) * 0.2) | [{"table": "quickbooks__customer_analytics", "column": "business_stability_score"}, {"table": "quickbooks__customer_analytics", "column": "payment_rate_percentage"}, {"table": "quickbooks__customer_analytics", "column": "credit_score"}] | [] | False |
| B1 | AVG(payment_rate_percentage) | [{"table": "quickbooks__customer_analytics", "column": "payment_rate_percentage"}] | [] | False |
| B1 | AVG(outstanding_balance) | [{"table": "quickbooks__customer_analytics", "column": "outstanding_balance"}] | [] | False |
| B1 | SUM(outstanding_balance) | [{"table": "quickbooks__customer_analytics", "column": "outstanding_balance"}] | [] | False |
| B1 | AVG(credit_score) | [{"table": "quickbooks__customer_analytics", "column": "credit_score"}] | [] | False |
| B1 | AVG(business_stability_score) | [{"table": "quickbooks__customer_analytics", "column": "business_stability_score"}] | [] | False |


## S15

类别 `data`；来源 `query_db`；调用 `252239c8c7534a53a85f5e6cfb9774f6`；状态 `success`。

```sql
SELECT 
  ROUND(AVG(payment_rate_percentage),2) AS avg_payment_rate_all,
  ROUND(AVG(outstanding_balance),2) AS avg_outstanding_all,
  ROUND(SUM(outstanding_balance),2) AS total_outstanding_all,
  COUNT(*) AS n_all
FROM quickbooks__customer_analytics
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-090/attempt-01/sql/S15.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-090/attempt-01/sql/S15.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-090/attempt-01/results/S15.rows.jsonl)；完整：True；SHA256：`8fbb4069a8b0aac1d755804ee8139a14c54ce1236fe0f5b78250d40eb6ebe92a`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "quickbooks__customer_analytics", "kind": "base", "block": null, "base_tables": ["quickbooks__customer_analytics"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |
| B1 | AVG(payment_rate_percentage) | [{"table": "quickbooks__customer_analytics", "column": "payment_rate_percentage"}] | [] | False |
| B1 | AVG(outstanding_balance) | [{"table": "quickbooks__customer_analytics", "column": "outstanding_balance"}] | [] | False |
| B1 | SUM(outstanding_balance) | [{"table": "quickbooks__customer_analytics", "column": "outstanding_balance"}] | [] | False |


## S16

类别 `data`；来源 `query_db`；调用 `597a4e7a353e40eb9a38ece1db232f63`；状态 `success`。

```sql
SELECT COUNT(DISTINCT p.customer_id) AS customers_in_profit, COUNT(*) AS invoice_count,
  ROUND(SUM(p.gross_profit), 2) AS total_gross_profit_high_risk,
  ROUND(SUM(p.invoice_total), 2) AS total_invoice_high_risk
FROM quickbooks__profitability_analysis p
INNER JOIN (
  SELECT customer_id FROM quickbooks__customer_analytics 
  WHERE payment_rate_percentage < 75 AND outstanding_balance > 15000
) c ON p.customer_id = c.customer_id
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-090/attempt-01/sql/S16.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-090/attempt-01/sql/S16.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-090/attempt-01/results/S16.rows.jsonl)；完整：True；SHA256：`c40f4bb7b2a0a693d18d08c0b27fc6d6e5ca20e91aa48ced9a0e0ef0aa2175b7`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "quickbooks__customer_analytics", "kind": "base", "block": null, "base_tables": ["quickbooks__customer_analytics"]}] | [] | [] |
| B2 | [{"alias": "p", "kind": "base", "block": null, "base_tables": ["quickbooks__profitability_analysis"]}, {"alias": "c", "kind": "derived", "block": "B1", "base_tables": ["quickbooks__customer_analytics"]}] | [{"type": "INNER", "right": "(SELECT customer_id FROM quickbooks__customer_analytics WHERE payment_rate_percentage < 75 AND outstanding_balance > 15000) AS c", "on": "p.customer_id = c.customer_id", "using": []}] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B2 | COUNT(DISTINCT p.customer_id) | [{"table": "quickbooks__profitability_analysis", "column": "customer_id"}] | [] | False |
| B2 | COUNT(*) | [] | [] | True |
| B2 | SUM(p.gross_profit) | [{"table": "quickbooks__profitability_analysis", "column": "gross_profit"}] | [] | False |
| B2 | SUM(p.invoice_total) | [{"table": "quickbooks__profitability_analysis", "column": "invoice_total"}] | [] | False |


## S17

类别 `data`；来源 `query_db`；调用 `ce57f6b5fbda49c3b4487d6f41a6d1c2`；状态 `success`。

```sql
SELECT ROUND(SUM(gross_profit), 2) AS total_gross_profit_all,
  ROUND(SUM(invoice_total), 2) AS total_invoice_all
FROM quickbooks__profitability_analysis
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-090/attempt-01/sql/S17.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-090/attempt-01/sql/S17.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-090/attempt-01/results/S17.rows.jsonl)；完整：True；SHA256：`b55f8ed72b625c7aaa2cfdfd22237e59d63be3e67c3cb08c17bdc53f8da0b15c`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "quickbooks__profitability_analysis", "kind": "base", "block": null, "base_tables": ["quickbooks__profitability_analysis"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | SUM(gross_profit) | [{"table": "quickbooks__profitability_analysis", "column": "gross_profit"}] | [] | False |
| B1 | SUM(invoice_total) | [{"table": "quickbooks__profitability_analysis", "column": "invoice_total"}] | [] | False |


## S18

类别 `data`；来源 `query_db`；调用 `ffc21a5473674ba281537c6466faae4f`；状态 `success`。

```sql
SELECT p.customer_id, c.customer_name,
  ROUND(SUM(p.gross_profit),2) AS gp, ROUND(SUM(p.invoice_total),2) AS inv_total,
  COUNT(*) AS n_inv
FROM quickbooks__profitability_analysis p
INNER JOIN quickbooks__customer_analytics c ON p.customer_id = c.customer_id
WHERE c.payment_rate_percentage < 75 AND c.outstanding_balance > 15000
GROUP BY p.customer_id
ORDER BY gp ASC
LIMIT 20
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-090/attempt-01/sql/S18.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-090/attempt-01/sql/S18.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-090/attempt-01/results/S18.rows.jsonl)；完整：True；SHA256：`a59639bf100767083dd9e1822916d9f365289b74192c64306dea2c2ac2cca1fd`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "p", "kind": "base", "block": null, "base_tables": ["quickbooks__profitability_analysis"]}, {"alias": "c", "kind": "base", "block": null, "base_tables": ["quickbooks__customer_analytics"]}] | [{"type": "INNER", "right": "quickbooks__customer_analytics AS c", "on": "p.customer_id = c.customer_id", "using": []}] | ["p.customer_id"] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |
| B1 | SUM(p.gross_profit) | [{"table": "quickbooks__profitability_analysis", "column": "gross_profit"}] | [] | False |
| B1 | SUM(p.invoice_total) | [{"table": "quickbooks__profitability_analysis", "column": "invoice_total"}] | [] | False |


## S19

类别 `data`；来源 `query_db`；调用 `57aaf3ed05044f5790e3fb7c4f9fa3dc`；状态 `success`。

```sql
SELECT dashboard_month, collection_rate_percentage, outstanding_receivables, overdue_amount, collection_risk_level, gross_profit
FROM quickbooks__financial_dashboard
ORDER BY dashboard_month
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-090/attempt-01/sql/S19.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-090/attempt-01/sql/S19.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-090/attempt-01/results/S19.rows.jsonl)；完整：True；SHA256：`4efd86d933b9fb08798bbfd621614c9f669f61baeb885efcebc2ccc9f43d44e1`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "quickbooks__financial_dashboard", "kind": "base", "block": null, "base_tables": ["quickbooks__financial_dashboard"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |


## S20

类别 `data`；来源 `query_db`；调用 `a8de5a2796864ce582e3f65fc11483f7`；状态 `success`。

```sql
SELECT dashboard_month, collection_rate_percentage,
  collection_rate_percentage - LAG(collection_rate_percentage) OVER (ORDER BY dashboard_month) AS mom_change
FROM quickbooks__financial_dashboard
ORDER BY dashboard_month DESC
LIMIT 13
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-090/attempt-01/sql/S20.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-090/attempt-01/sql/S20.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-090/attempt-01/results/S20.rows.jsonl)；完整：True；SHA256：`ba17395fa0da1e4a35bb74d77a27cad350c4958a0524e53048356f012426a3bb`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "quickbooks__financial_dashboard", "kind": "base", "block": null, "base_tables": ["quickbooks__financial_dashboard"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |


## S21

类别 `data`；来源 `query_db`；调用 `608c83c327c5443b93208c6a00ec674c`；状态 `success`。

```sql
SELECT dashboard_month, collection_rate_percentage,
  LAG(collection_rate_percentage) OVER (ORDER BY dashboard_month) AS prev_rate,
  collection_rate_percentage - LAG(collection_rate_percentage) OVER (ORDER BY dashboard_month) AS mom_change
FROM quickbooks__financial_dashboard
ORDER BY dashboard_month
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-090/attempt-01/sql/S21.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-090/attempt-01/sql/S21.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-090/attempt-01/results/S21.rows.jsonl)；完整：True；SHA256：`8a4efd293fce8a5c0dd4fb477b2ea26a3ed873b881c84063afff892f0d9f2450`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "quickbooks__financial_dashboard", "kind": "base", "block": null, "base_tables": ["quickbooks__financial_dashboard"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |


## S22

类别 `data`；来源 `query_db`；调用 `0553794ec48b4040ad1712c5cdecc145`；状态 `success`。

```sql
SELECT dashboard_month, collection_rate_percentage,
  collection_rate_percentage - LAG(collection_rate_percentage) OVER (ORDER BY dashboard_month) AS mom_change,
  CASE WHEN collection_rate_percentage < LAG(collection_rate_percentage) OVER (ORDER BY dashboard_month) THEN 1 ELSE 0 END AS is_decline
FROM quickbooks__financial_dashboard
WHERE dashboard_month >= '2024-10-01'
ORDER BY dashboard_month
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-090/attempt-01/sql/S22.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-090/attempt-01/sql/S22.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-090/attempt-01/results/S22.rows.jsonl)；完整：True；SHA256：`c68fd31f3dee180a5af01d9a2fcc6550ef763cfc32b9e9a419fd42d2f027e347`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "quickbooks__financial_dashboard", "kind": "base", "block": null, "base_tables": ["quickbooks__financial_dashboard"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |


## S23

类别 `data`；来源 `query_db`；调用 `fd246d07458b4472b2fe00d1593e746d`；状态 `success`。

```sql
SELECT 
  'High-Risk' AS group_name,
  COUNT(*) AS n,
  ROUND(AVG(customer_lifespan_days), 2) AS avg_lifespan_days,
  ROUND(AVG(total_invoices), 2) AS avg_total_invoices,
  ROUND(AVG(avg_invoice_amount), 2) AS avg_invoice_amount,
  ROUND(AVG(credit_score), 2) AS avg_credit_score,
  ROUND(AVG(business_stability_score), 2) AS avg_stability,
  ROUND(AVG(outstanding_balance), 2) AS avg_outstanding,
  ROUND(AVG(payment_rate_percentage), 2) AS avg_payment_rate,
  ROUND(AVG(active_months), 2) AS avg_active_months,
  ROUND(AVG(customer_lifespan_days), 2) AS avg_lifespan
FROM quickbooks__customer_analytics 
WHERE payment_rate_percentage < 75 AND outstanding_balance > 15000
UNION ALL
SELECT 
  'Normal' AS group_name,
  COUNT(*) AS n,
  ROUND(AVG(customer_lifespan_days), 2) AS avg_lifespan_days,
  ROUND(AVG(total_invoices), 2) AS avg_total_invoices,
  ROUND(AVG(avg_invoice_amount), 2) AS avg_invoice_amount,
  ROUND(AVG(credit_score), 2) AS avg_credit_score,
  ROUND(AVG(business_stability_score), 2) AS avg_stability,
  ROUND(AVG(outstanding_balance), 2) AS avg_outstanding,
  ROUND(AVG(payment_rate_percentage), 2) AS avg_payment_rate,
  ROUND(AVG(active_months), 2) AS avg_active_months,
  ROUND(AVG(customer_lifespan_days), 2) AS avg_lifespan
FROM quickbooks__customer_analytics 
WHERE NOT (payment_rate_percentage < 75 AND outstanding_balance > 15000)
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-090/attempt-01/sql/S23.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-090/attempt-01/sql/S23.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-090/attempt-01/results/S23.rows.jsonl)；完整：True；SHA256：`cfe883b08c4caedeab04d7c028c72dd989eb8221061b6d445174c1ce3eebc076`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "quickbooks__customer_analytics", "kind": "base", "block": null, "base_tables": ["quickbooks__customer_analytics"]}] | [] | [] |
| B2 | [{"alias": "quickbooks__customer_analytics", "kind": "base", "block": null, "base_tables": ["quickbooks__customer_analytics"]}] | [] | [] |
| B3 | [] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |
| B1 | AVG(customer_lifespan_days) | [{"table": "quickbooks__customer_analytics", "column": "customer_lifespan_days"}] | [] | False |
| B1 | AVG(total_invoices) | [{"table": "quickbooks__customer_analytics", "column": "total_invoices"}] | [] | False |
| B1 | AVG(avg_invoice_amount) | [{"table": "quickbooks__customer_analytics", "column": "avg_invoice_amount"}] | [] | False |
| B1 | AVG(credit_score) | [{"table": "quickbooks__customer_analytics", "column": "credit_score"}] | [] | False |
| B1 | AVG(business_stability_score) | [{"table": "quickbooks__customer_analytics", "column": "business_stability_score"}] | [] | False |
| B1 | AVG(outstanding_balance) | [{"table": "quickbooks__customer_analytics", "column": "outstanding_balance"}] | [] | False |
| B1 | AVG(payment_rate_percentage) | [{"table": "quickbooks__customer_analytics", "column": "payment_rate_percentage"}] | [] | False |
| B1 | AVG(active_months) | [{"table": "quickbooks__customer_analytics", "column": "active_months"}] | [] | False |
| B1 | AVG(customer_lifespan_days) | [{"table": "quickbooks__customer_analytics", "column": "customer_lifespan_days"}] | [] | False |
| B2 | COUNT(*) | [] | [] | True |
| B2 | AVG(customer_lifespan_days) | [{"table": "quickbooks__customer_analytics", "column": "customer_lifespan_days"}] | [] | False |
| B2 | AVG(total_invoices) | [{"table": "quickbooks__customer_analytics", "column": "total_invoices"}] | [] | False |
| B2 | AVG(avg_invoice_amount) | [{"table": "quickbooks__customer_analytics", "column": "avg_invoice_amount"}] | [] | False |
| B2 | AVG(credit_score) | [{"table": "quickbooks__customer_analytics", "column": "credit_score"}] | [] | False |
| B2 | AVG(business_stability_score) | [{"table": "quickbooks__customer_analytics", "column": "business_stability_score"}] | [] | False |
| B2 | AVG(outstanding_balance) | [{"table": "quickbooks__customer_analytics", "column": "outstanding_balance"}] | [] | False |
| B2 | AVG(payment_rate_percentage) | [{"table": "quickbooks__customer_analytics", "column": "payment_rate_percentage"}] | [] | False |
| B2 | AVG(active_months) | [{"table": "quickbooks__customer_analytics", "column": "active_months"}] | [] | False |
| B2 | AVG(customer_lifespan_days) | [{"table": "quickbooks__customer_analytics", "column": "customer_lifespan_days"}] | [] | False |


## S24

类别 `data`；来源 `query_db`；调用 `92fe117ba52e4e3b83e0ddbfcdf754e2`；状态 `success`。

```sql
SELECT 
  c.risk_group,
  p.profitability_tier,
  COUNT(*) AS n,
  ROUND(SUM(p.gross_profit), 2) AS total_gp
FROM (
  SELECT customer_id, 
    CASE WHEN payment_rate_percentage < 75 AND outstanding_balance > 15000 THEN 'High-Risk' ELSE 'Normal' END AS risk_group
  FROM quickbooks__customer_analytics
) c
INNER JOIN quickbooks__profitability_analysis p ON c.customer_id = p.customer_id
GROUP BY c.risk_group, p.profitability_tier
ORDER BY c.risk_group, p.profitability_tier
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-090/attempt-01/sql/S24.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-090/attempt-01/sql/S24.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-090/attempt-01/results/S24.rows.jsonl)；完整：True；SHA256：`2a492fed30ae4734d2aed4925a664ccf5e962e1f678ac540f276c1885596b8c2`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "quickbooks__customer_analytics", "kind": "base", "block": null, "base_tables": ["quickbooks__customer_analytics"]}] | [] | [] |
| B2 | [{"alias": "c", "kind": "derived", "block": "B1", "base_tables": ["quickbooks__customer_analytics"]}, {"alias": "p", "kind": "base", "block": null, "base_tables": ["quickbooks__profitability_analysis"]}] | [{"type": "INNER", "right": "quickbooks__profitability_analysis AS p", "on": "c.customer_id = p.customer_id", "using": []}] | ["c.risk_group", "p.profitability_tier"] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B2 | COUNT(*) | [] | [] | True |
| B2 | SUM(p.gross_profit) | [{"table": "quickbooks__profitability_analysis", "column": "gross_profit"}] | [] | False |


## S25

类别 `data`；来源 `query_db`；调用 `1e1b298a5eaf43e1afa2603d458b93ce`；状态 `success`。

```sql
SELECT 
  CASE WHEN payment_rate_percentage < 75 AND outstanding_balance > 15000 THEN 'High-Risk' ELSE 'Normal' END AS risk_group,
  lifecycle_stage,
  COUNT(*) AS n,
  ROUND(100.0 * COUNT(*) / SUM(COUNT(*)) OVER (PARTITION BY CASE WHEN payment_rate_percentage < 75 AND outstanding_balance > 15000 THEN 'High-Risk' ELSE 'Normal' END), 2) AS pct
FROM quickbooks__customer_analytics
GROUP BY risk_group, lifecycle_stage
ORDER BY risk_group, n DESC
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-090/attempt-01/sql/S25.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-090/attempt-01/sql/S25.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-090/attempt-01/results/S25.rows.jsonl)；完整：True；SHA256：`349268c585df827b119a14e12d6a6c35fd95d724db0323112626af169c4d7841`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "quickbooks__customer_analytics", "kind": "base", "block": null, "base_tables": ["quickbooks__customer_analytics"]}] | [] | ["CASE WHEN payment_rate_percentage < 75 AND outstanding_balance > 15000 THEN 'High-Risk' ELSE 'Normal' END", "lifecycle_stage"] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |
| B1 | COUNT(*) | [] | [] | True |
| B1 | COUNT(*) | [] | [] | True |


## S26

类别 `data`；来源 `query_db`；调用 `b3f04a395e6a41be9fde0c1c2317bc39`；状态 `success`。

```sql
SELECT 
  CASE WHEN payment_rate_percentage < 75 AND outstanding_balance > 15000 THEN 'High-Risk' ELSE 'Normal' END AS risk_group,
  activity_status,
  COUNT(*) AS n,
  ROUND(100.0 * COUNT(*) / SUM(COUNT(*)) OVER (PARTITION BY CASE WHEN payment_rate_percentage < 75 AND outstanding_balance > 15000 THEN 'High-Risk' ELSE 'Normal' END), 2) AS pct
FROM quickbooks__customer_analytics
GROUP BY risk_group, activity_status
ORDER BY risk_group, n DESC
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-090/attempt-01/sql/S26.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-090/attempt-01/sql/S26.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-090/attempt-01/results/S26.rows.jsonl)；完整：True；SHA256：`d2cbaa6aa40ded249fd4db9fa45d639bcffc8ed9d9b6e1370248f502373fe7c4`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "quickbooks__customer_analytics", "kind": "base", "block": null, "base_tables": ["quickbooks__customer_analytics"]}] | [] | ["CASE WHEN payment_rate_percentage < 75 AND outstanding_balance > 15000 THEN 'High-Risk' ELSE 'Normal' END", "activity_status"] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |
| B1 | COUNT(*) | [] | [] | True |
| B1 | COUNT(*) | [] | [] | True |


## S27

类别 `data`；来源 `query_db`；调用 `9efcd43b83b14590a3682af660a8a908`；状态 `success`。

```sql
SELECT 
  CASE WHEN payment_rate_percentage < 75 AND outstanding_balance > 15000 THEN 'High-Risk' ELSE 'Normal' END AS risk_group,
  customer_value_segment,
  COUNT(*) AS n,
  ROUND(100.0 * COUNT(*) / SUM(COUNT(*)) OVER (PARTITION BY CASE WHEN payment_rate_percentage < 75 AND outstanding_balance > 15000 THEN 'High-Risk' ELSE 'Normal' END), 2) AS pct
FROM quickbooks__customer_analytics
GROUP BY risk_group, customer_value_segment
ORDER BY risk_group, n DESC
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-090/attempt-01/sql/S27.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-090/attempt-01/sql/S27.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-090/attempt-01/results/S27.rows.jsonl)；完整：True；SHA256：`02514d5c2ab69b92dcdd30505dc3ddd38a190f679f56b40442a95b9177cbdc05`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "quickbooks__customer_analytics", "kind": "base", "block": null, "base_tables": ["quickbooks__customer_analytics"]}] | [] | ["CASE WHEN payment_rate_percentage < 75 AND outstanding_balance > 15000 THEN 'High-Risk' ELSE 'Normal' END", "customer_value_segment"] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |
| B1 | COUNT(*) | [] | [] | True |
| B1 | COUNT(*) | [] | [] | True |


## S28

类别 `data`；来源 `query_db`；调用 `6aeb72867aa8469cb0205e9fc0ead277`；状态 `success`。

```sql
SELECT 
  CASE WHEN payment_rate_percentage < 75 AND outstanding_balance > 15000 THEN 'High-Risk' ELSE 'Normal' END AS risk_group,
  credit_grade,
  COUNT(*) AS n,
  ROUND(100.0 * COUNT(*) / SUM(COUNT(*)) OVER (PARTITION BY CASE WHEN payment_rate_percentage < 75 AND outstanding_balance > 15000 THEN 'High-Risk' ELSE 'Normal' END), 2) AS pct
FROM quickbooks__customer_analytics
GROUP BY risk_group, credit_grade
ORDER BY risk_group, credit_grade
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-090/attempt-01/sql/S28.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-090/attempt-01/sql/S28.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-090/attempt-01/results/S28.rows.jsonl)；完整：True；SHA256：`484bad85fff99d01932e89c5e483bc34f5e06488faf5d423d57a3c914c41842a`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "quickbooks__customer_analytics", "kind": "base", "block": null, "base_tables": ["quickbooks__customer_analytics"]}] | [] | ["CASE WHEN payment_rate_percentage < 75 AND outstanding_balance > 15000 THEN 'High-Risk' ELSE 'Normal' END", "credit_grade"] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |
| B1 | COUNT(*) | [] | [] | True |
| B1 | COUNT(*) | [] | [] | True |


## S29

类别 `data`；来源 `query_db`；调用 `0d2d5e6af309438594b3ba4124ec5350`；状态 `success`。

```sql
SELECT risk_group,
  ROUND(MIN(customer_lifespan_days),1) AS min_life, ROUND(MAX(customer_lifespan_days),1) AS max_life,
  ROUND(AVG(customer_lifespan_days),1) AS avg_life,
  ROUND(AVG(total_invoices),2) AS avg_inv_cnt,
  ROUND(AVG(avg_invoice_amount),2) AS avg_inv_amt,
  ROUND(MIN(avg_invoice_amount),2) AS min_inv_amt, ROUND(MAX(avg_invoice_amount),2) AS max_inv_amt,
  ROUND(AVG(overdue_count_12m),2) AS avg_overdue_12m,
  ROUND(AVG(avg_payment_days_12m),2) AS avg_pay_days_12m,
  ROUND(AVG(days_since_last_invoice),1) AS avg_days_since_last,
  ROUND(AVG(revenue_growth_rate_12m),2) AS avg_rev_growth
FROM (
  SELECT customer_id, customer_lifespan_days, total_invoices, avg_invoice_amount, overdue_count_12m, avg_payment_days_12m, days_since_last_invoice, revenue_growth_rate_12m,
    CASE WHEN payment_rate_percentage < 75 AND outstanding_balance > 15000 THEN 'High-Risk' ELSE 'Normal' END AS risk_group
  FROM quickbooks__customer_analytics
)
GROUP BY risk_group
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-090/attempt-01/sql/S29.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-090/attempt-01/sql/S29.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-090/attempt-01/results/S29.rows.jsonl)；完整：True；SHA256：`718f60d64d55b51deeb94dc7a87fc0c624b36b10b439865e6c3638602c525f9f`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "quickbooks__customer_analytics", "kind": "base", "block": null, "base_tables": ["quickbooks__customer_analytics"]}] | [] | [] |
| B2 | [{"alias": "", "kind": "derived", "block": "B1", "base_tables": ["quickbooks__customer_analytics"]}] | [] | ["risk_group"] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B2 | MIN(customer_lifespan_days) | [{"table": "quickbooks__customer_analytics", "column": "customer_lifespan_days"}] | [] | False |
| B2 | MAX(customer_lifespan_days) | [{"table": "quickbooks__customer_analytics", "column": "customer_lifespan_days"}] | [] | False |
| B2 | AVG(customer_lifespan_days) | [{"table": "quickbooks__customer_analytics", "column": "customer_lifespan_days"}] | [] | False |
| B2 | AVG(total_invoices) | [{"table": "quickbooks__customer_analytics", "column": "total_invoices"}] | [] | False |
| B2 | AVG(avg_invoice_amount) | [{"table": "quickbooks__customer_analytics", "column": "avg_invoice_amount"}] | [] | False |
| B2 | MIN(avg_invoice_amount) | [{"table": "quickbooks__customer_analytics", "column": "avg_invoice_amount"}] | [] | False |
| B2 | MAX(avg_invoice_amount) | [{"table": "quickbooks__customer_analytics", "column": "avg_invoice_amount"}] | [] | False |
| B2 | AVG(overdue_count_12m) | [{"table": "quickbooks__customer_analytics", "column": "overdue_count_12m"}] | [] | False |
| B2 | AVG(avg_payment_days_12m) | [{"table": "quickbooks__customer_analytics", "column": "avg_payment_days_12m"}] | [] | False |
| B2 | AVG(days_since_last_invoice) | [{"table": "quickbooks__customer_analytics", "column": "days_since_last_invoice"}] | [] | False |
| B2 | AVG(revenue_growth_rate_12m) | [{"table": "quickbooks__customer_analytics", "column": "revenue_growth_rate_12m"}] | [] | False |


## S30

类别 `data`；来源 `query_db`；调用 `ad19071f0dfb40b79adddd21cd4be7cb`；状态 `success`。

```sql
SELECT customer_id,
  ROUND((100 - payment_rate_percentage) * 0.4 + (850 - credit_score) / 850.0 * 100 * 0.4 + (100 - business_stability_score) * 0.2, 2) AS risk_score,
  payment_rate_percentage, outstanding_balance, credit_score, business_stability_score, overdue_count_12m, avg_payment_days_12m
FROM quickbooks__customer_analytics
WHERE payment_rate_percentage < 75 AND outstanding_balance > 15000
ORDER BY risk_score DESC
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-090/attempt-01/sql/S30.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-090/attempt-01/sql/S30.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-090/attempt-01/results/S30.rows.jsonl)；完整：True；SHA256：`9fe629ddbe454722757e90e5f7504832026eff7abb70125b54f36eea6de400aa`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "quickbooks__customer_analytics", "kind": "base", "block": null, "base_tables": ["quickbooks__customer_analytics"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |


## S31

类别 `data`；来源 `query_db`；调用 `d891a58392f449ffa8e8ae985ff5e04c`；状态 `success`。

```sql
SELECT forecast_month, forecasted_inflows, forecasted_outflows, forecasted_net_cash_flow, risk_adjusted_inflows, blended_forecast, cumulative_forecast_cash_flow, next_3_months_cash_flow, worst_case_3_months, liquidity_status, cash_flow_health_score, liquidity_risk_level, management_recommendation, forecast_reliability
FROM quickbooks__cashflow_forecast
ORDER BY forecast_month
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-090/attempt-01/sql/S31.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-090/attempt-01/sql/S31.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-090/attempt-01/results/S31.rows.jsonl)；完整：True；SHA256：`43c1961cc8e0f4078242e209ba58cebf3e746a22456b0a0e1dcc040f32905183`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "quickbooks__cashflow_forecast", "kind": "base", "block": null, "base_tables": ["quickbooks__cashflow_forecast"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |


## S32

类别 `data`；来源 `query_db`；调用 `a90e1909263e4ad6ac4969bbe26f2b37`；状态 `success`。

```sql
SELECT 
  CASE 
    WHEN risk_score < 40 THEN 'Low (30-40)'
    WHEN risk_score < 50 THEN 'Medium (40-50)'
    WHEN risk_score < 60 THEN 'High (50-60)'
    ELSE 'Critical (60+)'
  END AS risk_tier,
  COUNT(*) AS n_customers,
  ROUND(SUM(outstanding_balance),2) AS total_outstanding
FROM (
  SELECT customer_id, outstanding_balance,
    (100 - payment_rate_percentage) * 0.4 + (850 - credit_score) / 850.0 * 100 * 0.4 + (100 - business_stability_score) * 0.2 AS risk_score
  FROM quickbooks__customer_analytics
  WHERE payment_rate_percentage < 75 AND outstanding_balance > 15000
)
GROUP BY risk_tier
ORDER BY MIN(risk_score)
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-090/attempt-01/sql/S32.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-090/attempt-01/sql/S32.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-090/attempt-01/results/S32.rows.jsonl)；完整：True；SHA256：`8b75f68d4d86eccb2722a969ec27f8dbf7106a3132dfefcb3c98bb838f91cddf`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "quickbooks__customer_analytics", "kind": "base", "block": null, "base_tables": ["quickbooks__customer_analytics"]}] | [] | [] |
| B2 | [{"alias": "", "kind": "derived", "block": "B1", "base_tables": ["quickbooks__customer_analytics"]}] | [] | ["CASE WHEN risk_score < 40 THEN 'Low (30-40)' WHEN risk_score < 50 THEN 'Medium (40-50)' WHEN risk_score < 60 THEN 'High (50-60)' ELSE 'Critical (60+)' END"] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B2 | COUNT(*) | [] | [] | True |
| B2 | SUM(outstanding_balance) | [{"table": "quickbooks__customer_analytics", "column": "outstanding_balance"}] | [] | False |
| B2 | MIN(risk_score) | [{"table": "quickbooks__customer_analytics", "column": "business_stability_score"}, {"table": "quickbooks__customer_analytics", "column": "payment_rate_percentage"}, {"table": "quickbooks__customer_analytics", "column": "credit_score"}] | [] | False |


## S33

类别 `data`；来源 `query_db`；调用 `5cbed46bf93d424590c292be0fcd1ee9`；状态 `success`。

```sql
SELECT 
  ROUND(SUM(outstanding_balance),2) AS total_outstanding,
  ROUND(SUM(outstanding_balance * ((100 - payment_rate_percentage) * 0.4 + (850 - credit_score) / 850.0 * 100 * 0.4 + (100 - business_stability_score) * 0.2) / 100.0),2) AS expected_loss_risk_weighted,
  ROUND(AVG((100 - payment_rate_percentage) * 0.4 + (850 - credit_score) / 850.0 * 100 * 0.4 + (100 - business_stability_score) * 0.2),2) AS avg_risk_score
FROM quickbooks__customer_analytics
WHERE payment_rate_percentage < 75 AND outstanding_balance > 15000
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-090/attempt-01/sql/S33.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-090/attempt-01/sql/S33.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-090/attempt-01/results/S33.rows.jsonl)；完整：True；SHA256：`bfbfc0de3b93ebeb89c3ee8b859200a0ee9c2c0ed8a861769cd5d0bee5c32e37`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "quickbooks__customer_analytics", "kind": "base", "block": null, "base_tables": ["quickbooks__customer_analytics"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | SUM(outstanding_balance) | [{"table": "quickbooks__customer_analytics", "column": "outstanding_balance"}] | [] | False |
| B1 | SUM(outstanding_balance * ((100 - payment_rate_percentage) * 0.4 + (850 - credit_score) / 850.0 * 100 * 0.4 + (100 - business_stability_score) * 0.2) / 100.0) | [{"table": "quickbooks__customer_analytics", "column": "outstanding_balance"}, {"table": "quickbooks__customer_analytics", "column": "business_stability_score"}, {"table": "quickbooks__customer_analytics", "column": "payment_rate_percentage"}, {"table": "quickbooks__customer_analytics", "column": "credit_score"}] | [] | False |
| B1 | AVG((100 - payment_rate_percentage) * 0.4 + (850 - credit_score) / 850.0 * 100 * 0.4 + (100 - business_stability_score) * 0.2) | [{"table": "quickbooks__customer_analytics", "column": "business_stability_score"}, {"table": "quickbooks__customer_analytics", "column": "payment_rate_percentage"}, {"table": "quickbooks__customer_analytics", "column": "credit_score"}] | [] | False |


## S34

类别 `data`；来源 `query_db`；调用 `f4a17a2798e14c5886b3bb74b24d2444`；状态 `success`。

```sql
SELECT 
  risk_group,
  ROUND(AVG(total_invoice_amount),2) AS avg_total_invoice_amt,
  ROUND(AVG(monthly_revenue_avg),2) AS avg_monthly_rev,
  ROUND(AVG(revenue_current_year),2) AS avg_rev_cy,
  ROUND(AVG(revenue_prev_year),2) AS avg_rev_py,
  ROUND(AVG(revenue_growth_yoy_pct),2) AS avg_growth_yoy,
  ROUND(AVG(total_payments),2) AS avg_payments,
  ROUND(AVG(total_quantity_purchased),2) AS avg_qty,
  ROUND(AVG(unique_products_purchased),2) AS avg_products,
  ROUND(AVG(payment_timeliness_score),2) AS avg_timeliness
FROM (
  SELECT *, CASE WHEN payment_rate_percentage < 75 AND outstanding_balance > 15000 THEN 'High-Risk' ELSE 'Normal' END AS risk_group
  FROM quickbooks__customer_analytics
)
GROUP BY risk_group
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-090/attempt-01/sql/S34.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-090/attempt-01/sql/S34.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-090/attempt-01/results/S34.rows.jsonl)；完整：True；SHA256：`72e68d598980e0eafeefc7d1012cb5d588df9b18c84490f889e9a043dc6bcd61`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "quickbooks__customer_analytics", "kind": "base", "block": null, "base_tables": ["quickbooks__customer_analytics"]}] | [] | [] |
| B2 | [{"alias": "", "kind": "derived", "block": "B1", "base_tables": ["quickbooks__customer_analytics"]}] | [] | ["risk_group"] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B2 | AVG(total_invoice_amount) | [{"table": "quickbooks__customer_analytics", "column": "total_invoice_amount"}] | [] | False |
| B2 | AVG(monthly_revenue_avg) | [{"table": "quickbooks__customer_analytics", "column": "monthly_revenue_avg"}] | [] | False |
| B2 | AVG(revenue_current_year) | [{"table": "quickbooks__customer_analytics", "column": "revenue_current_year"}] | [] | False |
| B2 | AVG(revenue_prev_year) | [{"table": "quickbooks__customer_analytics", "column": "revenue_prev_year"}] | [] | False |
| B2 | AVG(revenue_growth_yoy_pct) | [{"table": "quickbooks__customer_analytics", "column": "revenue_growth_yoy_pct"}] | [] | False |
| B2 | AVG(total_payments) | [{"table": "quickbooks__customer_analytics", "column": "total_payments"}] | [] | False |
| B2 | AVG(total_quantity_purchased) | [{"table": "quickbooks__customer_analytics", "column": "total_quantity_purchased"}] | [] | False |
| B2 | AVG(unique_products_purchased) | [{"table": "quickbooks__customer_analytics", "column": "unique_products_purchased"}] | [] | False |
| B2 | AVG(payment_timeliness_score) | [{"table": "quickbooks__customer_analytics", "column": "payment_timeliness_score"}] | [] | False |


## S35

类别 `data`；来源 `python`；调用 `7b8a17b705f8471eaa6c2ef14b0a61e6`；状态 `success`。

```sql

  SELECT customer_id, customer_lifespan_days, total_invoices, avg_invoice_amount,
         credit_score, business_stability_score, outstanding_balance, payment_rate_percentage,
         overdue_count_12m, avg_payment_days_12m, days_since_last_invoice, revenue_growth_rate_12m,
         active_months, total_invoice_amount, monthly_revenue_avg, payment_timeliness_score,
         total_payments, unique_products_purchased, revenue_growth_yoy_pct,
         CASE WHEN payment_rate_percentage < 75 AND outstanding_balance > 15000 THEN 'High-Risk' ELSE 'Normal' END AS risk_group
  FROM quickbooks__customer_analytics

```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-090/attempt-01/sql/S35.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-090/attempt-01/sql/S35.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-090/attempt-01/results/S35.rows.jsonl)；完整：True；SHA256：`8f34f7a13b2c11ad342b9232b58cf2c22da2a5a7f7666773b3c53ff2d7716d32`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "quickbooks__customer_analytics", "kind": "base", "block": null, "base_tables": ["quickbooks__customer_analytics"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |


## S36

类别 `data`；来源 `python`；调用 `7b8a17b705f8471eaa6c2ef14b0a61e6`；状态 `success`。

```sql

  SELECT customer_id, outstanding_balance,
    (100 - payment_rate_percentage) * 0.4 + (850 - credit_score) / 850.0 * 100 * 0.4 + (100 - business_stability_score) * 0.2 AS risk_score
  FROM quickbooks__customer_analytics
  WHERE payment_rate_percentage < 75 AND outstanding_balance > 15000

```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-090/attempt-01/sql/S36.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-090/attempt-01/sql/S36.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-090/attempt-01/results/S36.rows.jsonl)；完整：True；SHA256：`e03249a231c7fc5be1fa0443c0b8a6993ee9b48704fcad5845f02e2fda121eda`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "quickbooks__customer_analytics", "kind": "base", "block": null, "base_tables": ["quickbooks__customer_analytics"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |


## S37

类别 `data`；来源 `python`；调用 `7b8a17b705f8471eaa6c2ef14b0a61e6`；状态 `success`。

```sql

  SELECT dashboard_month, collection_rate_percentage, outstanding_receivables, overdue_amount, gross_profit
  FROM quickbooks__financial_dashboard
  ORDER BY dashboard_month

```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-090/attempt-01/sql/S37.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-090/attempt-01/sql/S37.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-090/attempt-01/results/S37.rows.jsonl)；完整：True；SHA256：`7c33aceb7279dd92e32cef01de5197c7d14c6a6c62c2746a6fac03dc707e0afd`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "quickbooks__financial_dashboard", "kind": "base", "block": null, "base_tables": ["quickbooks__financial_dashboard"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |


## S38

类别 `data`；来源 `python`；调用 `7b8a17b705f8471eaa6c2ef14b0a61e6`；状态 `success`。

```sql

  SELECT forecast_month, forecasted_net_cash_flow, liquidity_status
  FROM quickbooks__cashflow_forecast
  ORDER BY forecast_month

```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-090/attempt-01/sql/S38.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-090/attempt-01/sql/S38.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-090/attempt-01/results/S38.rows.jsonl)；完整：True；SHA256：`c6f6f6e53f64fda23991b679f9238301dcf568f78b045f9ecd8b8804dc95b481`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "quickbooks__cashflow_forecast", "kind": "base", "block": null, "base_tables": ["quickbooks__cashflow_forecast"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |


## S39

类别 `data`；来源 `python`；调用 `7b8a17b705f8471eaa6c2ef14b0a61e6`；状态 `success`。

```sql

  SELECT 
    CASE WHEN c.payment_rate_percentage < 75 AND c.outstanding_balance > 15000 THEN 'High-Risk' ELSE 'Normal' END AS risk_group,
    p.profitability_tier,
    COUNT(*) AS n_invoices,
    ROUND(SUM(p.gross_profit),2) AS total_gp
  FROM quickbooks__profitability_analysis p
  INNER JOIN quickbooks__customer_analytics c ON p.customer_id = c.customer_id
  GROUP BY risk_group, p.profitability_tier
  ORDER BY risk_group, p.profitability_tier

```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-090/attempt-01/sql/S39.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-090/attempt-01/sql/S39.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-090/attempt-01/results/S39.rows.jsonl)；完整：True；SHA256：`2a492fed30ae4734d2aed4925a664ccf5e962e1f678ac540f276c1885596b8c2`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "p", "kind": "base", "block": null, "base_tables": ["quickbooks__profitability_analysis"]}, {"alias": "c", "kind": "base", "block": null, "base_tables": ["quickbooks__customer_analytics"]}] | [{"type": "INNER", "right": "quickbooks__customer_analytics AS c", "on": "p.customer_id = c.customer_id", "using": []}] | ["CASE WHEN c.payment_rate_percentage < 75 AND c.outstanding_balance > 15000 THEN 'High-Risk' ELSE 'Normal' END", "p.profitability_tier"] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |
| B1 | SUM(p.gross_profit) | [{"table": "quickbooks__profitability_analysis", "column": "gross_profit"}] | [] | False |


## S40

类别 `data`；来源 `python`；调用 `7b8a17b705f8471eaa6c2ef14b0a61e6`；状态 `success`。

```sql

  SELECT 
    CASE 
      WHEN risk_score < 40 THEN 'Low (30-40)'
      WHEN risk_score < 50 THEN 'Medium (40-50)'
      WHEN risk_score < 60 THEN 'High (50-60)'
      ELSE 'Critical (60+)'
    END AS risk_tier,
    COUNT(*) AS n_customers,
    ROUND(SUM(outstanding_balance),2) AS total_outstanding,
    ROUND(AVG(risk_score),2) AS avg_risk_score
  FROM (
    SELECT customer_id, outstanding_balance,
      (100 - payment_rate_percentage) * 0.4 + (850 - credit_score) / 850.0 * 100 * 0.4 + (100 - business_stability_score) * 0.2 AS risk_score
    FROM quickbooks__customer_analytics
    WHERE payment_rate_percentage < 75 AND outstanding_balance > 15000
  )
  GROUP BY risk_tier
  ORDER BY MIN(risk_score)

```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-090/attempt-01/sql/S40.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-090/attempt-01/sql/S40.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-090/attempt-01/results/S40.rows.jsonl)；完整：True；SHA256：`e313c3007e0047eddcabac1d2f8b99127840903c161bf41ae5617ca378be01fe`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "quickbooks__customer_analytics", "kind": "base", "block": null, "base_tables": ["quickbooks__customer_analytics"]}] | [] | [] |
| B2 | [{"alias": "", "kind": "derived", "block": "B1", "base_tables": ["quickbooks__customer_analytics"]}] | [] | ["CASE WHEN risk_score < 40 THEN 'Low (30-40)' WHEN risk_score < 50 THEN 'Medium (40-50)' WHEN risk_score < 60 THEN 'High (50-60)' ELSE 'Critical (60+)' END"] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B2 | COUNT(*) | [] | [] | True |
| B2 | SUM(outstanding_balance) | [{"table": "quickbooks__customer_analytics", "column": "outstanding_balance"}] | [] | False |
| B2 | AVG(risk_score) | [{"table": "quickbooks__customer_analytics", "column": "business_stability_score"}, {"table": "quickbooks__customer_analytics", "column": "payment_rate_percentage"}, {"table": "quickbooks__customer_analytics", "column": "credit_score"}] | [] | False |
| B2 | MIN(risk_score) | [{"table": "quickbooks__customer_analytics", "column": "business_stability_score"}, {"table": "quickbooks__customer_analytics", "column": "payment_rate_percentage"}, {"table": "quickbooks__customer_analytics", "column": "credit_score"}] | [] | False |


## S41

类别 `data`；来源 `query_db`；调用 `a90e2bdef9d94025b4010cb49599d917`；状态 `success`。

```sql
SELECT 
  c.risk_group,
  COUNT(DISTINCT p.customer_id) AS n_customers,
  ROUND(SUM(p.gross_profit),2) AS sum_gross_profit,
  ROUND(SUM(p.risk_adjusted_profit),2) AS sum_risk_adj_profit
FROM (
  SELECT customer_id, 
    CASE WHEN payment_rate_percentage < 75 AND outstanding_balance > 15000 THEN 'High-Risk' ELSE 'Normal' END AS risk_group
  FROM quickbooks__customer_analytics
) c
INNER JOIN quickbooks__profitability_analysis p ON c.customer_id = p.customer_id
GROUP BY c.risk_group
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-090/attempt-01/sql/S41.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-090/attempt-01/sql/S41.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-090/attempt-01/results/S41.rows.jsonl)；完整：True；SHA256：`efedb52951a00754a656d783ba900330a9a9b346e80a725086b6e0ddde5d2223`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "quickbooks__customer_analytics", "kind": "base", "block": null, "base_tables": ["quickbooks__customer_analytics"]}] | [] | [] |
| B2 | [{"alias": "c", "kind": "derived", "block": "B1", "base_tables": ["quickbooks__customer_analytics"]}, {"alias": "p", "kind": "base", "block": null, "base_tables": ["quickbooks__profitability_analysis"]}] | [{"type": "INNER", "right": "quickbooks__profitability_analysis AS p", "on": "c.customer_id = p.customer_id", "using": []}] | ["c.risk_group"] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B2 | COUNT(DISTINCT p.customer_id) | [{"table": "quickbooks__profitability_analysis", "column": "customer_id"}] | [] | False |
| B2 | SUM(p.gross_profit) | [{"table": "quickbooks__profitability_analysis", "column": "gross_profit"}] | [] | False |
| B2 | SUM(p.risk_adjusted_profit) | [{"table": "quickbooks__profitability_analysis", "column": "risk_adjusted_profit"}] | [] | False |


## S42

类别 `data`；来源 `query_db`；调用 `ef934e1beae7429fb7fa7b76a0035952`；状态 `success`。

```sql
SELECT 
  c.risk_group,
  p.profitability_tier,
  COUNT(*) AS n_invoices,
  ROUND(100.0 * COUNT(*) / SUM(COUNT(*)) OVER (PARTITION BY c.risk_group), 2) AS pct_invoices,
  ROUND(SUM(p.gross_profit),2) AS total_gp,
  ROUND(AVG(p.invoice_gross_margin_pct),2) AS avg_margin_pct
FROM (
  SELECT customer_id, 
    CASE WHEN payment_rate_percentage < 75 AND outstanding_balance > 15000 THEN 'High-Risk' ELSE 'Normal' END AS risk_group
  FROM quickbooks__customer_analytics
) c
INNER JOIN quickbooks__profitability_analysis p ON c.customer_id = p.customer_id
GROUP BY c.risk_group, p.profitability_tier
ORDER BY c.risk_group, n_invoices DESC
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-090/attempt-01/sql/S42.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-090/attempt-01/sql/S42.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-090/attempt-01/results/S42.rows.jsonl)；完整：True；SHA256：`bdfa42aceeeef3a892c947288a83dac4d4add17e8a654a660e43c1c42f7f655e`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "quickbooks__customer_analytics", "kind": "base", "block": null, "base_tables": ["quickbooks__customer_analytics"]}] | [] | [] |
| B2 | [{"alias": "c", "kind": "derived", "block": "B1", "base_tables": ["quickbooks__customer_analytics"]}, {"alias": "p", "kind": "base", "block": null, "base_tables": ["quickbooks__profitability_analysis"]}] | [{"type": "INNER", "right": "quickbooks__profitability_analysis AS p", "on": "c.customer_id = p.customer_id", "using": []}] | ["c.risk_group", "p.profitability_tier"] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B2 | COUNT(*) | [] | [] | True |
| B2 | SUM(p.gross_profit) | [{"table": "quickbooks__profitability_analysis", "column": "gross_profit"}] | [] | False |
| B2 | AVG(p.invoice_gross_margin_pct) | [{"table": "quickbooks__profitability_analysis", "column": "invoice_gross_margin_pct"}] | [] | False |
| B2 | COUNT(*) | [] | [] | True |
| B2 | COUNT(*) | [] | [] | True |


## S43

类别 `data`；来源 `python`；调用 `3f154921cb5f4c19a6d91d6d56c91cd5`；状态 `success`。

```sql

  SELECT customer_id, outstanding_balance, payment_rate_percentage, credit_score, 
         business_stability_score, overdue_count_12m, avg_payment_days_12m,
         (100 - payment_rate_percentage) * 0.4 + (850 - credit_score) / 850.0 * 100 * 0.4 + (100 - business_stability_score) * 0.2 AS risk_score
  FROM quickbooks__customer_analytics
  WHERE payment_rate_percentage < 75 AND outstanding_balance > 15000

```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-090/attempt-01/sql/S43.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-090/attempt-01/sql/S43.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-090/attempt-01/results/S43.rows.jsonl)；完整：True；SHA256：`67df66d8d32f4e9ca7c758f9f4f105a8310cfd8c6063e766484824790384583f`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "quickbooks__customer_analytics", "kind": "base", "block": null, "base_tables": ["quickbooks__customer_analytics"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |


## S44

类别 `data`；来源 `python`；调用 `3f154921cb5f4c19a6d91d6d56c91cd5`；状态 `success`。

```sql

  SELECT dashboard_month, collection_rate_percentage, outstanding_receivables, overdue_amount
  FROM quickbooks__financial_dashboard
  ORDER BY dashboard_month

```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-090/attempt-01/sql/S44.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-090/attempt-01/sql/S44.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-090/attempt-01/results/S44.rows.jsonl)；完整：True；SHA256：`e06eb9484676b16e9e9f01209c675ce9b6e18c3c7648bed5d01e9da319f7b211`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "quickbooks__financial_dashboard", "kind": "base", "block": null, "base_tables": ["quickbooks__financial_dashboard"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |


## S45

类别 `data`；来源 `python`；调用 `3f154921cb5f4c19a6d91d6d56c91cd5`；状态 `success`。

```sql

  SELECT forecast_month, forecasted_net_cash_flow, liquidity_status
  FROM quickbooks__cashflow_forecast
  ORDER BY forecast_month

```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-090/attempt-01/sql/S45.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-090/attempt-01/sql/S45.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-090/attempt-01/results/S45.rows.jsonl)；完整：True；SHA256：`c6f6f6e53f64fda23991b679f9238301dcf568f78b045f9ecd8b8804dc95b481`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "quickbooks__cashflow_forecast", "kind": "base", "block": null, "base_tables": ["quickbooks__cashflow_forecast"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |


## S46

类别 `data`；来源 `python`；调用 `3f154921cb5f4c19a6d91d6d56c91cd5`；状态 `success`。

```sql

  SELECT 
    CASE 
      WHEN risk_score < 40 THEN 'Low (30-40)'
      WHEN risk_score < 50 THEN 'Medium (40-50)'
      WHEN risk_score < 60 THEN 'High (50-60)'
      ELSE 'Critical (60+)'
    END AS risk_tier,
    COUNT(*) AS n_customers,
    ROUND(SUM(outstanding_balance),2) AS total_outstanding,
    ROUND(AVG(risk_score),2) AS avg_risk_score,
    ROUND(AVG(avg_payment_days_12m),1) AS avg_pay_days,
    ROUND(AVG(overdue_count_12m),2) AS avg_overdue
  FROM (
    SELECT customer_id, outstanding_balance, avg_payment_days_12m, overdue_count_12m,
      (100 - payment_rate_percentage) * 0.4 + (850 - credit_score) / 850.0 * 100 * 0.4 + (100 - business_stability_score) * 0.2 AS risk_score
    FROM quickbooks__customer_analytics
    WHERE payment_rate_percentage < 75 AND outstanding_balance > 15000
  )
  GROUP BY risk_tier
  ORDER BY MIN(risk_score)

```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-090/attempt-01/sql/S46.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-090/attempt-01/sql/S46.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-090/attempt-01/results/S46.rows.jsonl)；完整：True；SHA256：`e25bc826608c7dc37d0123a99fc62a72787dfd41c6068b2ee184d1f7ada45840`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "quickbooks__customer_analytics", "kind": "base", "block": null, "base_tables": ["quickbooks__customer_analytics"]}] | [] | [] |
| B2 | [{"alias": "", "kind": "derived", "block": "B1", "base_tables": ["quickbooks__customer_analytics"]}] | [] | ["CASE WHEN risk_score < 40 THEN 'Low (30-40)' WHEN risk_score < 50 THEN 'Medium (40-50)' WHEN risk_score < 60 THEN 'High (50-60)' ELSE 'Critical (60+)' END"] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B2 | COUNT(*) | [] | [] | True |
| B2 | SUM(outstanding_balance) | [{"table": "quickbooks__customer_analytics", "column": "outstanding_balance"}] | [] | False |
| B2 | AVG(risk_score) | [{"table": "quickbooks__customer_analytics", "column": "business_stability_score"}, {"table": "quickbooks__customer_analytics", "column": "payment_rate_percentage"}, {"table": "quickbooks__customer_analytics", "column": "credit_score"}] | [] | False |
| B2 | AVG(avg_payment_days_12m) | [{"table": "quickbooks__customer_analytics", "column": "avg_payment_days_12m"}] | [] | False |
| B2 | AVG(overdue_count_12m) | [{"table": "quickbooks__customer_analytics", "column": "overdue_count_12m"}] | [] | False |
| B2 | MIN(risk_score) | [{"table": "quickbooks__customer_analytics", "column": "business_stability_score"}, {"table": "quickbooks__customer_analytics", "column": "payment_rate_percentage"}, {"table": "quickbooks__customer_analytics", "column": "credit_score"}] | [] | False |

