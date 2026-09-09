# dacomp-092

First, from the `profitability_analysis` table, identify the high-volatility customer segm…

运行：服务中断。官方未评分。全部 SQL 尝试/成功 40/38；数据 SQL 38/36；Python 0 次。

完整原题：

First, from the `profitability_analysis` table, identify the high-volatility customer segment ranking in the top 25% for `customer_margin_volatility`. Calculate the coefficient of variation (standard deviation / mean) of their `gross_profit` over the past 12 months and the variance of their quarter-over-quarter `invoice_total` growth rate to quantify their profit stability. Using behavioral features from the `customer_analytics` table such as `rfm_segment`, `payment_behavior`, and `revenue_trend_correlation`, explore the relationship between high volatility and customer lifecycle stages and payment patterns. By joining with `financial_dashboard` data, calculate the contribution of these customers to the overall `business_health_score` and the differential impact on `collection_rate_percentage`. Additionally, analyze the risk exposure distribution based on the accounts receivable structure from the `balance_sheet` table. Finally, build a multi-dimensional customer risk rating model that integrates volatility metrics, behavioral characteristics, and financial risks, and propose targeted customer management strategies.

| 表 | 行数 | 列数 |
| --- | --- | --- |
| quickbooks__balance_sheet | 111567 | 17 |
| quickbooks__customer_analytics | 2800 | 67 |
| quickbooks__financial_dashboard | 33 | 41 |
| quickbooks__profitability_analysis | 8000 | 35 |


实际路线（分析者依据 SQL/源码概括，不代表 Agent 自述）：SQL 识别高波动客户、生命周期和财务风险并计算窗口 → R22 遇服务端 401 后停止。

数据库大小：29,724,672 字节。

## 数据 SQL

| SQL | 状态 | 基础表 | Join 输入/类型 | GROUP BY | 聚合表达式 | 结果行数 | 数据库 ms |
| --- | --- | --- | --- | --- | --- | --- | --- |
| [S3/Q1](#s3) | success | ["quickbooks__profitability_analysis"] | 0 / {} | [] | [] | 5 | 0.464 |
| [S4/Q2](#s4) | success | ["quickbooks__customer_analytics"] | 0 / {} | [] | [] | 5 | 0.505 |
| [S5/Q3](#s5) | success | ["quickbooks__financial_dashboard"] | 0 / {} | [] | [] | 5 | 0.438 |
| [S6/Q4](#s6) | success | ["quickbooks__balance_sheet"] | 0 / {} | [] | [] | 5 | 0.279 |
| [S7/Q5](#s7) | success | ["quickbooks__profitability_analysis"] | 0 / {} | [] | ["COUNT(*)"] | 1 | 2.357 |
| [S8/Q6](#s8) | success | ["quickbooks__customer_analytics"] | 0 / {} | [] | ["COUNT(*)"] | 1 | 0.629 |
| [S9/Q7](#s9) | success | ["quickbooks__financial_dashboard"] | 0 / {} | [] | ["COUNT(*)"] | 1 | 0.289 |
| [S10/Q8](#s10) | success | ["quickbooks__balance_sheet"] | 0 / {} | [] | ["COUNT(*)"] | 1 | 7.669 |
| [S11/Q9](#s11) | success | ["quickbooks__profitability_analysis"] | 0 / {} | [] | [] | 20 | 0.501 |
| [S12/Q10](#s12) | success | ["quickbooks__customer_analytics"] | 0 / {} | [] | [] | 20 | 0.375 |
| [S13/Q11](#s13) | success | ["quickbooks__profitability_analysis"] | 0 / {} | [] | ["MIN(transaction_date)", "MAX(transaction_date)"] | 1 | 2.272 |
| [S14/Q12](#s14) | success | ["quickbooks__customer_analytics"] | 0 / {} | [] | [] | 6 | 1.064 |
| [S15/Q13](#s15) | success | ["quickbooks__customer_analytics"] | 0 / {} | [] | [] | 4 | 0.904 |
| [S16/Q14](#s16) | success | ["quickbooks__customer_analytics"] | 0 / {} | [] | [] | 4 | 0.921 |
| [S17/Q15](#s17) | success | ["quickbooks__profitability_analysis"] | 0 / {} | [] | ["COUNT(DISTINCT customer_id)"] | 1 | 5.294 |
| [S18/Q16](#s18) | success | ["quickbooks__profitability_analysis"] | 0 / {} | ["customer_margin_volatility"] | ["COUNT(*)"] | 20 | 4.987 |
| [S19/Q17](#s19) | success | ["quickbooks__profitability_analysis"] | 0 / {} | ["customer_id"] | ["MAX(customer_margin_volatility)", "COUNT(*)", "MIN(vol)", "MAX(vol)", "AVG(vol)"] | 1 | 6.461 |
| [S20/Q18](#s20) | success | ["quickbooks__profitability_analysis"] | 0 / {} | ["customer_id"] | ["COUNT(DISTINCT customer_margin_volatility)", "COUNT(DISTINCT customer_margin_volatility)", "COUNT(DISTINCT customer_margin_volatility)"] | 5 | 4.322 |
| [S21/Q19](#s21) | success | ["quickbooks__profitability_analysis"] | 0 / {} | [] | [] | 2 | 1.85 |
| [S22/Q20](#s22) | success | ["quickbooks__profitability_analysis"] | 0 / {} | ["customer_id"] | ["AVG(customer_margin_volatility)"] | 5 | 11.134 |
| [S23/Q21](#s23) | failed | ["quickbooks__profitability_analysis"] | 0 / {} | ["customer_id"] | ["AVG(customer_margin_volatility)", "PERCENTILE_DISC(0.75)"] | unknown | 未取得；调用总时长 0.137 ms |
| [S24/Q22](#s24) | success | ["quickbooks__profitability_analysis"] | 0 / {} | ["customer_id"] | ["AVG(customer_margin_volatility)"] | 1 | 9.365 |
| [S25/Q23](#s25) | success | ["quickbooks__profitability_analysis"] | 0 / {} | ["customer_id"] | ["AVG(customer_margin_volatility)", "COUNT(*)"] | 1 | 11.215 |
| [S26/Q24](#s26) | success | ["quickbooks__profitability_analysis"] | 0 / {} | [] | ["MIN(transaction_date)", "MAX(transaction_date)"] | 1 | 2.089 |
| [S27/Q25](#s27) | success | ["quickbooks__profitability_analysis"] | 2 / {'INNER': 1} | ["customer_id"] | ["MAX(transaction_date)", "AVG(customer_margin_volatility)"] | 20 | 1509.444 |
| [S28/Q26](#s28) | failed | ["quickbooks__profitability_analysis"] | 2 / {'INNER': 1} | ["customer_id", "h.customer_id", "h.vol"] | ["MAX(transaction_date)", "AVG(customer_margin_volatility)", "AVG(p.gross_profit)", "STDDEV(p.gross_profit)", "COUNT(p.gross_profit)", "STDDEV(p.gross_profit)", "AVG(p.gross_profit)", "AVG(p.gross_profit)"] | unknown | 未取得；调用总时长 0.238 ms |
| [S29/Q27](#s29) | success | ["quickbooks__profitability_analysis"] | 2 / {'INNER': 1} | ["customer_id", "h.customer_id", "h.vol"] | ["MAX(transaction_date)", "AVG(customer_margin_volatility)", "AVG(p.gross_profit)", "COUNT(p.gross_profit)", "AVG(p.gross_profit * p.gross_profit)", "AVG(p.gross_profit)", "AVG(p.gross_profit)"] | 20 | 1215.476 |
| [S30/Q28](#s30) | success | ["quickbooks__profitability_analysis"] | 2 / {'INNER': 1} | ["customer_id", "h.customer_id", "STRFTIME('%Y-%m', p.transaction_date)", "customer_id"] | ["MAX(transaction_date)", "AVG(customer_margin_volatility)", "SUM(p.gross_profit)", "AVG(monthly_gp)", "COUNT(*)", "AVG(monthly_gp * monthly_gp)", "AVG(monthly_gp)", "AVG(monthly_gp)"] | 15 | 1222.127 |
| [S31/Q29](#s31) | success | ["quickbooks__profitability_analysis"] | 2 / {'INNER': 1} | ["customer_id", "h.customer_id", "STRFTIME('%Y-%m', p.transaction_date)"] | ["MAX(transaction_date)", "AVG(customer_margin_volatility)", "SUM(p.gross_profit)", "AVG(monthly_gp)", "COUNT(*)", "COUNT(DISTINCT customer_id)", "AVG(monthly_gp * monthly_gp)", "AVG(monthly_gp)", "AVG(monthly_gp)", "AVG(monthly_gp)", "AVG(monthly_gp * monthly_gp)", "AVG(monthly_gp)", "AVG(monthly_gp)"] | 1 | 1226.476 |
| [S32/Q30](#s32) | success | ["quickbooks__profitability_analysis"] | 0 / {} | ["revenue_year", "revenue_quarter"] | ["COUNT(*)"] | 11 | 3.856 |
| [S33/Q31](#s33) | success | ["quickbooks__profitability_analysis"] | 0 / {} | ["customer_id"] | ["AVG(customer_margin_volatility)", "COUNT(*)"] | 1 | 11.212 |
| [S34/Q32](#s34) | success | ["quickbooks__profitability_analysis"] | 2 / {'INNER': 1} | ["customer_id", "h.customer_id", "STRFTIME('%Y', p.transaction_date)", "CAST((CAST(STRFTIME('%m', p.transaction_date) AS INTEGER) + 2) / 3 AS INTEGER)"] | ["MAX(transaction_date)", "AVG(customer_margin_volatility)", "SUM(p.invoice_total)"] | 30 | 1225.357 |
| [S35/Q33](#s35) | success | ["quickbooks__profitability_analysis"] | 2 / {'INNER': 1} | ["customer_id", "h.customer_id", "STRFTIME('%Y', p.transaction_date)", "CAST((CAST(STRFTIME('%m', p.transaction_date) AS INTEGER) + 2) / 3 AS INTEGER)"] | ["MAX(transaction_date)", "AVG(customer_margin_volatility)", "SUM(p.invoice_total)", "AVG(qoq_growth)", "COUNT(*)", "AVG(qoq_growth * qoq_growth)", "AVG(qoq_growth)", "AVG(qoq_growth)", "AVG(qoq_growth * qoq_growth)", "AVG(qoq_growth)", "AVG(qoq_growth)"] | 1 | 1219.233 |
| [S36/Q34](#s36) | success | ["quickbooks__customer_analytics", "quickbooks__profitability_analysis"] | 2 / {'INNER': 1} | ["customer_id", "s.vol_segment", "a.rfm_segment"] | ["AVG(customer_margin_volatility)", "COUNT(*)"] | 18 | 1122.652 |
| [S37/Q35](#s37) | success | ["quickbooks__customer_analytics", "quickbooks__profitability_analysis"] | 2 / {'INNER': 1} | ["customer_id", "s.vol_segment", "a.payment_behavior"] | ["AVG(customer_margin_volatility)", "COUNT(*)"] | 12 | 1092.178 |
| [S38/Q36](#s38) | success | ["quickbooks__customer_analytics", "quickbooks__profitability_analysis"] | 2 / {'INNER': 1} | ["customer_id", "s.vol_segment", "a.lifecycle_stage"] | ["AVG(customer_margin_volatility)", "COUNT(*)"] | 12 | 1108.684 |
| [S39/Q37](#s39) | success | ["quickbooks__customer_analytics", "quickbooks__profitability_analysis"] | 2 / {'INNER': 1} | ["customer_id", "s.vol_segment"] | ["AVG(customer_margin_volatility)", "COUNT(*)", "AVG(a.revenue_trend_correlation)", "AVG(a.credit_score)", "AVG(a.avg_payment_days_12m)", "AVG(a.overdue_count_12m)", "AVG(a.overall_customer_score)", "AVG(a.revenue_volatility)"] | 3 | 1114.568 |
| [S40/Q38](#s40) | success | ["quickbooks__customer_analytics"] | 0 / {} | [] | ["COUNT(*)", "COUNT(revenue_trend_correlation)", "COUNT(credit_score)", "COUNT(avg_payment_days_12m)", "COUNT(overdue_count_12m)", "COUNT(overall_customer_score)", "COUNT(revenue_volatility)", "COUNT(rfm_segment)", "COUNT(payment_behavior)", "COUNT(lifecycle_stage)", "COUNT(customer_value_segment)", "COUNT(risk_assessment)", "COUNT(credit_grade)", "COUNT(payment_timeliness_score)", "COUNT(business_stability_score)"] | 1 | 2.154 |


## 元数据和设置

| SQL | 类别 | 状态 | 内容 |
| --- | --- | --- | --- |
| S1 | connection_setup | success | PRAGMA query_only=ON |
| S2 | metadata | success | SELECT name,sql FROM sqlite_master WHERE type='table' ORDER BY name |


## Python 与执行位置

人工源码审查：**reviewed_no_python_before_interruption**。服务错误前没有 Python 调用；仅描述已保留的 SQL 轨迹，不能据此认定未完成后续步骤也遵守协议。 [证据](../reviews/dacomp-092.json)。

无 Python 分析调用。

## 优化机会

已验证候选。筛选限于精确 SQL、相同自包含 CTE、相同单表完整过滤、可分解单表聚合；未覆盖任意 Join 等价和一般谓词蕴含。全部候选都是 offline，未测在线预测。

| 候选 | 类型 | 已有结果 | 覆盖 SQL | 后续次数 | 中间行数 | 验证 | 成本 |
| --- | --- | --- | --- | --- | --- | --- | --- |
| C1 | exact-result reuse | True | ["S13", "S26"] | 1 | unknown | not_verified_cap | Not tested |
| C2 | common subexpression | False | ["S22", "S24", "S25", "S27", "S29", "S30", "S31", "S33", "S34", "S35", "S36", "S37", "S38", "S39"] | 13 | 2800 | verified | Warm-cache baseline 11838.925 ms vs build+reuse 144.199 ms, ratio 82.101; five repetitions, see performance evidence. |
| C3 | common subexpression | False | ["S27", "S29", "S30", "S31", "S34", "S35"] | 5 | 1 | verified | Not benchmarked; correctness alone does not establish net speedup. |
| C4 | aggregate MV | False | ["S7", "S32"] | 1 | 11 | verified | Not benchmarked; correctness alone does not establish net speedup. |
| C5 | aggregate MV | False | ["S8", "S40"] | 1 | unknown | not_verified_cap | Not tested |


已验证覆盖（含触发查询、候选并集去重）：16/36 条成功数据 SQL。正确性仅针对当前数据库快照；未测性能的候选不能声称已加速。

[完整 build/rewrite 与比较证据](dacomp-092.analysis.json)。

### C2：common subexpression

Identical self-contained CTE body across queries.

原查询 [S22](#s22), [S24](#s24), [S25](#s25), [S27](#s27), [S29](#s29), [S30](#s30), [S31](#s31), [S33](#s33), [S34](#s34), [S35](#s35), [S36](#s36), [S37](#s37), [S38](#s38), [S39](#s39) → 新增共享状态 C2 → 后续 13 次可复用。该构建点为事后假设，不代表 Agent 当时预知后续。

构建定义：

```sql
SELECT customer_id, AVG(customer_margin_volatility) AS vol FROM quickbooks__profitability_analysis GROUP BY customer_id
```

受益查询 S22 的改写示例：

```sql
WITH cust_vol AS (SELECT * FROM temp.reuse_candidate), ordered AS (SELECT customer_id, vol, ROW_NUMBER() OVER (ORDER BY vol DESC) AS rn, COUNT(*) OVER () AS total FROM cust_vol) SELECT * FROM ordered WHERE rn IN (700, 701, 2100, 2101) OR rn = 2800
```

| 原 SQL | 列名一致 | 结果一致 | 比较方法 |
| --- | --- | --- | --- |
| S22 | True | True | exact_multiset |
| S24 | True | True | exact_multiset |
| S25 | True | True | exact_multiset |
| S27 | True | True | ordered_numeric_tolerance |
| S29 | True | True | ordered_numeric_tolerance |
| S30 | True | True | ordered_numeric_tolerance |
| S31 | True | True | exact_multiset |
| S33 | True | True | exact_multiset |
| S34 | True | True | ordered_numeric_tolerance |
| S35 | True | True | exact_multiset |
| S36 | True | True | ordered_numeric_tolerance |
| S37 | True | True | ordered_numeric_tolerance |
| S38 | True | True | ordered_numeric_tolerance |
| S39 | True | True | ordered_numeric_tolerance |


验证状态：verified；成本结论：Warm-cache baseline 11838.925 ms vs build+reuse 144.199 ms, ratio 82.101; five repetitions, see performance evidence.

### C3：common subexpression

Identical self-contained CTE body across queries.

原查询 [S27](#s27), [S29](#s29), [S30](#s30), [S31](#s31), [S34](#s34), [S35](#s35) → 新增共享状态 C3 → 后续 5 次可复用。该构建点为事后假设，不代表 Agent 当时预知后续。

构建定义：

```sql
SELECT DATE(MAX(transaction_date), '-12 months') AS cutoff_date FROM quickbooks__profitability_analysis
```

受益查询 S27 的改写示例：

```sql
/* Define the past 12 months date range */ WITH date_range AS (SELECT * FROM temp.reuse_candidate), cust_vol /* High volatility customers (top 25%) */ AS (SELECT customer_id, AVG(customer_margin_volatility) AS vol FROM quickbooks__profitability_analysis GROUP BY customer_id), ordered AS (SELECT customer_id, vol, ROW_NUMBER() OVER (ORDER BY vol DESC) AS rn, COUNT(*) OVER () AS total FROM cust_vol), high_vol_cust AS (SELECT customer_id, vol FROM ordered WHERE rn <= total * 0.25) /* Get gross_profit data for past 12 months */ SELECT h.customer_id, h.vol, p.gross_profit, p.transaction_date FROM high_vol_cust AS h JOIN quickbooks__profitability_analysis AS p ON h.customer_id = p.customer_id WHERE p.transaction_date >= (SELECT cutoff_date FROM date_range) ORDER BY h.vol DESC, h.customer_id, p.transaction_date LIMIT 20
```

| 原 SQL | 列名一致 | 结果一致 | 比较方法 |
| --- | --- | --- | --- |
| S27 | True | True | ordered_numeric_tolerance |
| S29 | True | True | ordered_numeric_tolerance |
| S30 | True | True | ordered_numeric_tolerance |
| S31 | True | True | exact_multiset |
| S34 | True | True | ordered_numeric_tolerance |
| S35 | True | True | exact_multiset |


验证状态：verified；成本结论：Not benchmarked; correctness alone does not establish net speedup.

### C4：aggregate MV

Union of grouping keys; decomposable aggregate states; AVG uses SUM and non-NULL COUNT.

原查询 [S7](#s7), [S32](#s32) → 新增共享状态 C4 → 后续 1 次可复用。该构建点为事后假设，不代表 Agent 当时预知后续。

构建定义：

```sql
SELECT revenue_year AS __g0, revenue_quarter AS __g1, COUNT(*) AS __a0 FROM "quickbooks__profitability_analysis"  GROUP BY revenue_year, revenue_quarter
```

受益查询 S7 的改写示例：

```sql
SELECT SUM(__a0) AS cnt FROM temp.reuse_candidate
```

| 原 SQL | 列名一致 | 结果一致 | 比较方法 |
| --- | --- | --- | --- |
| S7 | True | True | exact_multiset |
| S32 | True | True | ordered_numeric_tolerance |


验证状态：verified；成本结论：Not benchmarked; correctness alone does not establish net speedup.

[性能证据 C2](dacomp-092.C2.performance.json)：measured。

结果依赖：自动记录 SQL→Python 的接口父调用，以及源码中引用归档文件的消费者；字面值相同不认定因果。模型方向选择需要人工读取消息，尚未做全面因果标注。

[统一消息](../../../runs/dsv4flash-db-first-full-01/dacomp-092/attempt-01/messages.jsonl)；[原始 OpenCode 事件](../../../runs/dsv4flash-db-first-full-01/dacomp-092/attempt-01/opencode.jsonl)；[SQL 引擎日志](../../../runs/dsv4flash-db-first-full-01/dacomp-092/attempt-01/sql_journal.jsonl)。

## S1

类别 `connection_setup`；来源 `connection`；调用 `506bca2386aa4963a844de9246db49e5`；状态 `success`。

```sql
PRAGMA query_only=ON
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-092/attempt-01/sql/S1.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-092/attempt-01/sql/S1.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-092/attempt-01/results/S1.rows.jsonl)；完整：True；SHA256：`e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`。

## S2

类别 `metadata`；来源 `list_db`；调用 `506bca2386aa4963a844de9246db49e5`；状态 `success`。

```sql
SELECT name,sql FROM sqlite_master WHERE type='table' ORDER BY name
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-092/attempt-01/sql/S2.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-092/attempt-01/sql/S2.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-092/attempt-01/results/S2.rows.jsonl)；完整：True；SHA256：`13b37ef047190e51a0ed33de050139ac8e4a18b2ba28908cfe985a7fecc06ed3`。

## S3

类别 `data`；来源 `query_db`；调用 `de273ce44b084d1f8b7dbc0dc717a87b`；状态 `success`。

```sql
SELECT * FROM quickbooks__profitability_analysis LIMIT 5
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-092/attempt-01/sql/S3.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-092/attempt-01/sql/S3.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-092/attempt-01/results/S3.rows.jsonl)；完整：True；SHA256：`2bc178207d2c020c85674f0420e6358f8d46f4038f454185b88d8a1f1b1ed7d8`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "quickbooks__profitability_analysis", "kind": "base", "block": null, "base_tables": ["quickbooks__profitability_analysis"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |


## S4

类别 `data`；来源 `query_db`；调用 `63fd74b7b1734039afb0dcf2b542c67b`；状态 `success`。

```sql
SELECT * FROM quickbooks__customer_analytics LIMIT 5
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-092/attempt-01/sql/S4.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-092/attempt-01/sql/S4.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-092/attempt-01/results/S4.rows.jsonl)；完整：True；SHA256：`67effb61e8a88a8846e08780be72a610f9dce4ff408c8786fe6c4604a60609d1`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "quickbooks__customer_analytics", "kind": "base", "block": null, "base_tables": ["quickbooks__customer_analytics"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |


## S5

类别 `data`；来源 `query_db`；调用 `a9185b01a1eb4fb59b54e2375d0b96f7`；状态 `success`。

```sql
SELECT * FROM quickbooks__financial_dashboard LIMIT 5
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-092/attempt-01/sql/S5.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-092/attempt-01/sql/S5.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-092/attempt-01/results/S5.rows.jsonl)；完整：True；SHA256：`d435077a9029b37a079800dd5ec5baa989d231f4e69a436881883b6253babdb3`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "quickbooks__financial_dashboard", "kind": "base", "block": null, "base_tables": ["quickbooks__financial_dashboard"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |


## S6

类别 `data`；来源 `query_db`；调用 `675b59cf66e54389a70218521da4213f`；状态 `success`。

```sql
SELECT * FROM quickbooks__balance_sheet LIMIT 5
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-092/attempt-01/sql/S6.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-092/attempt-01/sql/S6.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-092/attempt-01/results/S6.rows.jsonl)；完整：True；SHA256：`4c0fb82b5d1605806b7da8968dad65976775b1f2f6daafa5a7bdfcea0ffe16e4`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "quickbooks__balance_sheet", "kind": "base", "block": null, "base_tables": ["quickbooks__balance_sheet"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |


## S7

类别 `data`；来源 `query_db`；调用 `686431f034374e2796a86d6a895d4b12`；状态 `success`。

```sql
SELECT COUNT(*) as cnt FROM quickbooks__profitability_analysis
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-092/attempt-01/sql/S7.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-092/attempt-01/sql/S7.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-092/attempt-01/results/S7.rows.jsonl)；完整：True；SHA256：`ca5d97f4dab69813055999493cfea8f56e91e334c1465da9867b484a21b0a9bd`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "quickbooks__profitability_analysis", "kind": "base", "block": null, "base_tables": ["quickbooks__profitability_analysis"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |


## S8

类别 `data`；来源 `query_db`；调用 `cd00c464c33e47f989e8308daff6cefd`；状态 `success`。

```sql
SELECT COUNT(*) as cnt FROM quickbooks__customer_analytics
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-092/attempt-01/sql/S8.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-092/attempt-01/sql/S8.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-092/attempt-01/results/S8.rows.jsonl)；完整：True；SHA256：`409ab31294c9429f03e9f17a7e49ebfac259b29f8ad8ca8c4d51de2ef93bb943`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "quickbooks__customer_analytics", "kind": "base", "block": null, "base_tables": ["quickbooks__customer_analytics"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |


## S9

类别 `data`；来源 `query_db`；调用 `dee31b0d667a4099b971b198f961fec8`；状态 `success`。

```sql
SELECT COUNT(*) as cnt FROM quickbooks__financial_dashboard
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-092/attempt-01/sql/S9.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-092/attempt-01/sql/S9.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-092/attempt-01/results/S9.rows.jsonl)；完整：True；SHA256：`1315f0f7efc386feec13fc4575d19a3dcdd07d1b61de1fe595d7dec48df1079a`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "quickbooks__financial_dashboard", "kind": "base", "block": null, "base_tables": ["quickbooks__financial_dashboard"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |


## S10

类别 `data`；来源 `query_db`；调用 `cf2e55437b314605af287184bca15368`；状态 `success`。

```sql
SELECT COUNT(*) as cnt FROM quickbooks__balance_sheet
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-092/attempt-01/sql/S10.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-092/attempt-01/sql/S10.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-092/attempt-01/results/S10.rows.jsonl)；完整：True；SHA256：`8e0a09c905e099b226011a93e1b432e9d9128d7409a5f78e390fc5976485d446`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "quickbooks__balance_sheet", "kind": "base", "block": null, "base_tables": ["quickbooks__balance_sheet"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |


## S11

类别 `data`；来源 `query_db`；调用 `dc35bc69a60b4249866ec08d86d53901`；状态 `success`。

```sql
SELECT DISTINCT customer_id FROM quickbooks__profitability_analysis LIMIT 20
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-092/attempt-01/sql/S11.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-092/attempt-01/sql/S11.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-092/attempt-01/results/S11.rows.jsonl)；完整：True；SHA256：`de0e14140546fa7462638e50c97595b385055371c8042cf5f30564d14996eaaa`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "quickbooks__profitability_analysis", "kind": "base", "block": null, "base_tables": ["quickbooks__profitability_analysis"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |


## S12

类别 `data`；来源 `query_db`；调用 `c2cf3df564444b2b9f9f8f7fcd0f5409`；状态 `success`。

```sql
SELECT DISTINCT customer_id FROM quickbooks__customer_analytics LIMIT 20
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-092/attempt-01/sql/S12.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-092/attempt-01/sql/S12.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-092/attempt-01/results/S12.rows.jsonl)；完整：True；SHA256：`09d57b7d2026c7fb050b4c1be942cd458d37f0e736a298815e30bfa31ce986f1`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "quickbooks__customer_analytics", "kind": "base", "block": null, "base_tables": ["quickbooks__customer_analytics"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |


## S13

类别 `data`；来源 `query_db`；调用 `f3d570ff0c484d0984cfeab91b36477c`；状态 `success`。

```sql
SELECT MIN(transaction_date), MAX(transaction_date) FROM quickbooks__profitability_analysis
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-092/attempt-01/sql/S13.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-092/attempt-01/sql/S13.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-092/attempt-01/results/S13.rows.jsonl)；完整：True；SHA256：`496d0f79c219533c6657a48eff97851cb977b9458e08c9b6bc69e146e7e111b7`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "quickbooks__profitability_analysis", "kind": "base", "block": null, "base_tables": ["quickbooks__profitability_analysis"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | MIN(transaction_date) | [{"table": "quickbooks__profitability_analysis", "column": "transaction_date"}] | [] | False |
| B1 | MAX(transaction_date) | [{"table": "quickbooks__profitability_analysis", "column": "transaction_date"}] | [] | False |


## S14

类别 `data`；来源 `query_db`；调用 `0d6d3835a23b4bed9d63b92d11772f74`；状态 `success`。

```sql
SELECT DISTINCT rfm_segment FROM quickbooks__customer_analytics
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-092/attempt-01/sql/S14.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-092/attempt-01/sql/S14.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-092/attempt-01/results/S14.rows.jsonl)；完整：True；SHA256：`615f915cb24cd628e9143ba343b155902df162a88bbf1b38d11ec5f9d88f563a`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "quickbooks__customer_analytics", "kind": "base", "block": null, "base_tables": ["quickbooks__customer_analytics"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |


## S15

类别 `data`；来源 `query_db`；调用 `07a9f4fa9b9246feba6338d87ee76a1d`；状态 `success`。

```sql
SELECT DISTINCT payment_behavior FROM quickbooks__customer_analytics
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-092/attempt-01/sql/S15.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-092/attempt-01/sql/S15.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-092/attempt-01/results/S15.rows.jsonl)；完整：True；SHA256：`1d4163f1dcd4517c94629ddbe06f7184b780cdf3f8fbe5798f9107c9195c13be`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "quickbooks__customer_analytics", "kind": "base", "block": null, "base_tables": ["quickbooks__customer_analytics"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |


## S16

类别 `data`；来源 `query_db`；调用 `95b6e587e6264d7ba40cf90966e0ac3a`；状态 `success`。

```sql
SELECT DISTINCT lifecycle_stage FROM quickbooks__customer_analytics
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-092/attempt-01/sql/S16.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-092/attempt-01/sql/S16.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-092/attempt-01/results/S16.rows.jsonl)；完整：True；SHA256：`8b4dcf17295ab17a256f2b60eb070046ff3d4e03fb17bc6b244da92bab1be394`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "quickbooks__customer_analytics", "kind": "base", "block": null, "base_tables": ["quickbooks__customer_analytics"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |


## S17

类别 `data`；来源 `query_db`；调用 `e010c249818e41cd86284d0a9b4ad723`；状态 `success`。

```sql
SELECT COUNT(DISTINCT customer_id) as cnt FROM quickbooks__profitability_analysis
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-092/attempt-01/sql/S17.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-092/attempt-01/sql/S17.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-092/attempt-01/results/S17.rows.jsonl)；完整：True；SHA256：`409ab31294c9429f03e9f17a7e49ebfac259b29f8ad8ca8c4d51de2ef93bb943`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "quickbooks__profitability_analysis", "kind": "base", "block": null, "base_tables": ["quickbooks__profitability_analysis"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(DISTINCT customer_id) | [{"table": "quickbooks__profitability_analysis", "column": "customer_id"}] | [] | False |


## S18

类别 `data`；来源 `query_db`；调用 `cc719efc5ae44367ab6dd0817951db1d`；状态 `success`。

```sql
SELECT customer_margin_volatility, COUNT(*) as cnt
FROM quickbooks__profitability_analysis
WHERE customer_margin_volatility IS NOT NULL
GROUP BY customer_margin_volatility
ORDER BY customer_margin_volatility DESC
LIMIT 20
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-092/attempt-01/sql/S18.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-092/attempt-01/sql/S18.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-092/attempt-01/results/S18.rows.jsonl)；完整：True；SHA256：`8caabc44c5d32d3a9d2a256c140a6d004abe7847e8760f321f2c906739495f86`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "quickbooks__profitability_analysis", "kind": "base", "block": null, "base_tables": ["quickbooks__profitability_analysis"]}] | [] | ["customer_margin_volatility"] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |


## S19

类别 `data`；来源 `query_db`；调用 `0525f76aebc241c2b955cdb438a7f66a`；状态 `success`。

```sql
WITH cust_vol AS (
  SELECT customer_id, MAX(customer_margin_volatility) AS vol
  FROM quickbooks__profitability_analysis
  GROUP BY customer_id
)
SELECT 
  COUNT(*) AS n_customers,
  MIN(vol) AS min_vol,
  MAX(vol) AS max_vol,
  AVG(vol) AS mean_vol
FROM cust_vol
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-092/attempt-01/sql/S19.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-092/attempt-01/sql/S19.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-092/attempt-01/results/S19.rows.jsonl)；完整：True；SHA256：`47a506f4d316b1fc609b413bf6375761cc89a2293ff25bfdc09d3150d7e709c4`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "quickbooks__profitability_analysis", "kind": "base", "block": null, "base_tables": ["quickbooks__profitability_analysis"]}] | [] | ["customer_id"] |
| B2 | [{"alias": "cust_vol", "kind": "derived", "block": "B1", "base_tables": ["quickbooks__profitability_analysis"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | MAX(customer_margin_volatility) | [{"table": "quickbooks__profitability_analysis", "column": "customer_margin_volatility"}] | [] | False |
| B2 | COUNT(*) | [] | [] | True |
| B2 | MIN(vol) | [{"table": "quickbooks__profitability_analysis", "column": "customer_margin_volatility"}] | [] | False |
| B2 | MAX(vol) | [{"table": "quickbooks__profitability_analysis", "column": "customer_margin_volatility"}] | [] | False |
| B2 | AVG(vol) | [{"table": "quickbooks__profitability_analysis", "column": "customer_margin_volatility"}] | [] | False |


## S20

类别 `data`；来源 `query_db`；调用 `2e4b4b2b317d4a07a07629cd57964e84`；状态 `success`。

```sql
SELECT customer_id, COUNT(DISTINCT customer_margin_volatility) AS n_distinct_vol, COUNT(DISTINCT customer_margin_volatility) 
FROM quickbooks__profitability_analysis
GROUP BY customer_id
HAVING COUNT(DISTINCT customer_margin_volatility) > 1
LIMIT 5
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-092/attempt-01/sql/S20.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-092/attempt-01/sql/S20.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-092/attempt-01/results/S20.rows.jsonl)；完整：True；SHA256：`ab3798c8ebb03d54671ae0d8e37ecf4b60d2e503396d25a454e1e3e3dbdb50d3`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "quickbooks__profitability_analysis", "kind": "base", "block": null, "base_tables": ["quickbooks__profitability_analysis"]}] | [] | ["customer_id"] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(DISTINCT customer_margin_volatility) | [{"table": "quickbooks__profitability_analysis", "column": "customer_margin_volatility"}] | [] | False |
| B1 | COUNT(DISTINCT customer_margin_volatility) | [{"table": "quickbooks__profitability_analysis", "column": "customer_margin_volatility"}] | [] | False |
| B1 | COUNT(DISTINCT customer_margin_volatility) | [{"table": "quickbooks__profitability_analysis", "column": "customer_margin_volatility"}] | [] | False |


## S21

类别 `data`；来源 `query_db`；调用 `a645b1c164d046f3ad8a6507d9299b94`；状态 `success`。

```sql
SELECT invoice_id, customer_id, transaction_date, revenue_month_start, customer_margin_volatility, invoice_total, gross_profit
FROM quickbooks__profitability_analysis
WHERE customer_id = 'CUS00031796345'
ORDER BY transaction_date
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-092/attempt-01/sql/S21.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-092/attempt-01/sql/S21.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-092/attempt-01/results/S21.rows.jsonl)；完整：True；SHA256：`30328a2af7ba7f605c45e1d6f2fd5c9572a0ffd07696b714b430a32b28fa27aa`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "quickbooks__profitability_analysis", "kind": "base", "block": null, "base_tables": ["quickbooks__profitability_analysis"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |


## S22

类别 `data`；来源 `query_db`；调用 `010891721bbe49339c7b69ae6751fb9a`；状态 `success`。

```sql
WITH cust_vol AS (
  SELECT customer_id, AVG(customer_margin_volatility) AS vol
  FROM quickbooks__profitability_analysis
  GROUP BY customer_id
),
ordered AS (
  SELECT customer_id, vol,
    ROW_NUMBER() OVER (ORDER BY vol DESC) AS rn,
    COUNT(*) OVER () AS total
  FROM cust_vol
)
SELECT * FROM ordered WHERE rn IN (700, 701, 2100, 2101) OR rn = 2800
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-092/attempt-01/sql/S22.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-092/attempt-01/sql/S22.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-092/attempt-01/results/S22.rows.jsonl)；完整：True；SHA256：`c930526e5bd742c7d6133a29d57d3e5a8c8a964952620d3135f2e8104af708cb`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "quickbooks__profitability_analysis", "kind": "base", "block": null, "base_tables": ["quickbooks__profitability_analysis"]}] | [] | ["customer_id"] |
| B2 | [{"alias": "cust_vol", "kind": "derived", "block": "B1", "base_tables": ["quickbooks__profitability_analysis"]}] | [] | [] |
| B3 | [{"alias": "ordered", "kind": "derived", "block": "B2", "base_tables": ["quickbooks__profitability_analysis"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | AVG(customer_margin_volatility) | [{"table": "quickbooks__profitability_analysis", "column": "customer_margin_volatility"}] | [] | False |


## S23

类别 `data`；来源 `query_db`；调用 `632b5fe4bf494055ac31e47ee0a6ba87`；状态 `failed`。

```sql
WITH cust_vol AS (
  SELECT customer_id, AVG(customer_margin_volatility) AS vol
  FROM quickbooks__profitability_analysis
  GROUP BY customer_id
)
SELECT 
  PERCENTILE_DISC(0.75) WITHIN GROUP (ORDER BY vol) AS p75
FROM cust_vol
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-092/attempt-01/sql/S23.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-092/attempt-01/sql/S23.parameters.json)。

错误：`OperationalError('near "(": syntax error')`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "quickbooks__profitability_analysis", "kind": "base", "block": null, "base_tables": ["quickbooks__profitability_analysis"]}] | [] | ["customer_id"] |
| B2 | [{"alias": "cust_vol", "kind": "derived", "block": "B1", "base_tables": ["quickbooks__profitability_analysis"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | AVG(customer_margin_volatility) | [{"table": "quickbooks__profitability_analysis", "column": "customer_margin_volatility"}] | [] | False |
| B2 | PERCENTILE_DISC(0.75) | [] | [] | False |


## S24

类别 `data`；来源 `query_db`；调用 `5eeb35f7eb9948f58ebbe2a81208c327`；状态 `success`。

```sql
WITH cust_vol AS (
  SELECT customer_id, AVG(customer_margin_volatility) AS vol
  FROM quickbooks__profitability_analysis
  GROUP BY customer_id
),
ordered AS (
  SELECT customer_id, vol,
    ROW_NUMBER() OVER (ORDER BY vol DESC) AS rn
  FROM cust_vol
)
SELECT vol AS threshold FROM ordered WHERE rn = 700
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-092/attempt-01/sql/S24.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-092/attempt-01/sql/S24.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-092/attempt-01/results/S24.rows.jsonl)；完整：True；SHA256：`70ceee86b95235f1c4437f6a68405fa4bdc03b5f6e71a6fd6e1c747d2d71cd0d`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "quickbooks__profitability_analysis", "kind": "base", "block": null, "base_tables": ["quickbooks__profitability_analysis"]}] | [] | ["customer_id"] |
| B2 | [{"alias": "cust_vol", "kind": "derived", "block": "B1", "base_tables": ["quickbooks__profitability_analysis"]}] | [] | [] |
| B3 | [{"alias": "ordered", "kind": "derived", "block": "B2", "base_tables": ["quickbooks__profitability_analysis"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | AVG(customer_margin_volatility) | [{"table": "quickbooks__profitability_analysis", "column": "customer_margin_volatility"}] | [] | False |


## S25

类别 `data`；来源 `query_db`；调用 `a0e3bbe7ee644f78a353decbc7e3c1a0`；状态 `success`。

```sql
WITH cust_vol AS (
  SELECT customer_id, AVG(customer_margin_volatility) AS vol
  FROM quickbooks__profitability_analysis
  GROUP BY customer_id
),
ordered AS (
  SELECT customer_id, vol,
    ROW_NUMBER() OVER (ORDER BY vol DESC) AS rn,
    COUNT(*) OVER () AS total
  FROM cust_vol
),
high_vol_cust AS (
  SELECT customer_id, vol
  FROM ordered
  WHERE rn <= total * 0.25
)
SELECT COUNT(*) AS n_high_vol FROM high_vol_cust
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-092/attempt-01/sql/S25.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-092/attempt-01/sql/S25.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-092/attempt-01/results/S25.rows.jsonl)；完整：True；SHA256：`a482ada409c7c0efe39d3f42fd4364938468c884fb29d4e249f74acf895bba32`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "quickbooks__profitability_analysis", "kind": "base", "block": null, "base_tables": ["quickbooks__profitability_analysis"]}] | [] | ["customer_id"] |
| B2 | [{"alias": "cust_vol", "kind": "derived", "block": "B1", "base_tables": ["quickbooks__profitability_analysis"]}] | [] | [] |
| B3 | [{"alias": "ordered", "kind": "derived", "block": "B2", "base_tables": ["quickbooks__profitability_analysis"]}] | [] | [] |
| B4 | [{"alias": "high_vol_cust", "kind": "derived", "block": "B3", "base_tables": ["quickbooks__profitability_analysis"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | AVG(customer_margin_volatility) | [{"table": "quickbooks__profitability_analysis", "column": "customer_margin_volatility"}] | [] | False |
| B4 | COUNT(*) | [] | [] | True |


## S26

类别 `data`；来源 `query_db`；调用 `bd6c136a42884f90bc8ae9bd57a3ce18`；状态 `success`。

```sql
SELECT MIN(transaction_date), MAX(transaction_date) FROM quickbooks__profitability_analysis
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-092/attempt-01/sql/S26.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-092/attempt-01/sql/S26.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-092/attempt-01/results/S26.rows.jsonl)；完整：True；SHA256：`496d0f79c219533c6657a48eff97851cb977b9458e08c9b6bc69e146e7e111b7`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "quickbooks__profitability_analysis", "kind": "base", "block": null, "base_tables": ["quickbooks__profitability_analysis"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | MIN(transaction_date) | [{"table": "quickbooks__profitability_analysis", "column": "transaction_date"}] | [] | False |
| B1 | MAX(transaction_date) | [{"table": "quickbooks__profitability_analysis", "column": "transaction_date"}] | [] | False |


## S27

类别 `data`；来源 `query_db`；调用 `75d00932af2f473793c20f2fb732090f`；状态 `success`。

```sql
-- Define the past 12 months date range
WITH date_range AS (
  SELECT DATE(MAX(transaction_date), '-12 months') AS cutoff_date
  FROM quickbooks__profitability_analysis
),
-- High volatility customers (top 25%)
cust_vol AS (
  SELECT customer_id, AVG(customer_margin_volatility) AS vol
  FROM quickbooks__profitability_analysis
  GROUP BY customer_id
),
ordered AS (
  SELECT customer_id, vol,
    ROW_NUMBER() OVER (ORDER BY vol DESC) AS rn,
    COUNT(*) OVER () AS total
  FROM cust_vol
),
high_vol_cust AS (
  SELECT customer_id, vol
  FROM ordered
  WHERE rn <= total * 0.25
)
-- Get gross_profit data for past 12 months
SELECT h.customer_id, h.vol, p.gross_profit, p.transaction_date
FROM high_vol_cust h
JOIN quickbooks__profitability_analysis p ON h.customer_id = p.customer_id
WHERE p.transaction_date >= (SELECT cutoff_date FROM date_range)
ORDER BY h.vol DESC, h.customer_id, p.transaction_date
LIMIT 20
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-092/attempt-01/sql/S27.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-092/attempt-01/sql/S27.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-092/attempt-01/results/S27.rows.jsonl)；完整：True；SHA256：`5f5cddc66fbb3d01610415469e8e837b958e1788c9537f11c4a2d69a282cc9d1`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "quickbooks__profitability_analysis", "kind": "base", "block": null, "base_tables": ["quickbooks__profitability_analysis"]}] | [] | [] |
| B2 | [{"alias": "quickbooks__profitability_analysis", "kind": "base", "block": null, "base_tables": ["quickbooks__profitability_analysis"]}] | [] | ["customer_id"] |
| B3 | [{"alias": "cust_vol", "kind": "derived", "block": "B2", "base_tables": ["quickbooks__profitability_analysis"]}] | [] | [] |
| B4 | [{"alias": "ordered", "kind": "derived", "block": "B3", "base_tables": ["quickbooks__profitability_analysis"]}] | [] | [] |
| B5 | [{"alias": "date_range", "kind": "derived", "block": "B1", "base_tables": ["quickbooks__profitability_analysis"]}] | [] | [] |
| B6 | [{"alias": "h", "kind": "derived", "block": "B4", "base_tables": ["quickbooks__profitability_analysis"]}, {"alias": "p", "kind": "base", "block": null, "base_tables": ["quickbooks__profitability_analysis"]}] | [{"type": "INNER", "right": "quickbooks__profitability_analysis AS p", "on": "h.customer_id = p.customer_id", "using": []}] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | MAX(transaction_date) | [{"table": "quickbooks__profitability_analysis", "column": "transaction_date"}] | [] | False |
| B2 | AVG(customer_margin_volatility) | [{"table": "quickbooks__profitability_analysis", "column": "customer_margin_volatility"}] | [] | False |


未解析列血缘：[{"block": "B6", "column": "cutoff_date", "reason": "ambiguous_or_missing_source"}]

## S28

类别 `data`；来源 `query_db`；调用 `997f89df12df4c1baec610a02f9445e9`；状态 `failed`。

```sql
-- Compute coefficient of variation of gross_profit for high-vol customers over past 12 months
WITH date_range AS (
  SELECT DATE(MAX(transaction_date), '-12 months') AS cutoff_date
  FROM quickbooks__profitability_analysis
),
cust_vol AS (
  SELECT customer_id, AVG(customer_margin_volatility) AS vol
  FROM quickbooks__profitability_analysis
  GROUP BY customer_id
),
ordered AS (
  SELECT customer_id, vol,
    ROW_NUMBER() OVER (ORDER BY vol DESC) AS rn,
    COUNT(*) OVER () AS total
  FROM cust_vol
),
high_vol_cust AS (
  SELECT customer_id, vol
  FROM ordered
  WHERE rn <= total * 0.25
)
SELECT 
  h.customer_id,
  h.vol,
  AVG(p.gross_profit) AS mean_gross_profit,
  STDEV(p.gross_profit) AS std_gross_profit,
  CASE WHEN AVG(p.gross_profit) = 0 THEN NULL 
       ELSE STDEV(p.gross_profit) / AVG(p.gross_profit) END AS cv_gross_profit,
  COUNT(p.gross_profit) AS n_obs
FROM high_vol_cust h
JOIN quickbooks__profitability_analysis p ON h.customer_id = p.customer_id
  AND p.transaction_date >= (SELECT cutoff_date FROM date_range)
GROUP BY h.customer_id, h.vol
ORDER BY h.vol DESC
LIMIT 20
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-092/attempt-01/sql/S28.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-092/attempt-01/sql/S28.parameters.json)。

错误：`OperationalError('no such function: STDEV')`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "quickbooks__profitability_analysis", "kind": "base", "block": null, "base_tables": ["quickbooks__profitability_analysis"]}] | [] | [] |
| B2 | [{"alias": "quickbooks__profitability_analysis", "kind": "base", "block": null, "base_tables": ["quickbooks__profitability_analysis"]}] | [] | ["customer_id"] |
| B3 | [{"alias": "cust_vol", "kind": "derived", "block": "B2", "base_tables": ["quickbooks__profitability_analysis"]}] | [] | [] |
| B4 | [{"alias": "ordered", "kind": "derived", "block": "B3", "base_tables": ["quickbooks__profitability_analysis"]}] | [] | [] |
| B5 | [{"alias": "date_range", "kind": "derived", "block": "B1", "base_tables": ["quickbooks__profitability_analysis"]}] | [] | [] |
| B6 | [{"alias": "h", "kind": "derived", "block": "B4", "base_tables": ["quickbooks__profitability_analysis"]}, {"alias": "p", "kind": "base", "block": null, "base_tables": ["quickbooks__profitability_analysis"]}] | [{"type": "INNER", "right": "quickbooks__profitability_analysis AS p", "on": "h.customer_id = p.customer_id AND p.transaction_date >= (SELECT cutoff_date FROM date_range)", "using": []}] | ["h.customer_id", "h.vol"] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | MAX(transaction_date) | [{"table": "quickbooks__profitability_analysis", "column": "transaction_date"}] | [] | False |
| B2 | AVG(customer_margin_volatility) | [{"table": "quickbooks__profitability_analysis", "column": "customer_margin_volatility"}] | [] | False |
| B6 | AVG(p.gross_profit) | [{"table": "quickbooks__profitability_analysis", "column": "gross_profit"}] | [] | False |
| B6 | STDDEV(p.gross_profit) | [{"table": "quickbooks__profitability_analysis", "column": "gross_profit"}] | [] | False |
| B6 | COUNT(p.gross_profit) | [{"table": "quickbooks__profitability_analysis", "column": "gross_profit"}] | [] | False |
| B6 | STDDEV(p.gross_profit) | [{"table": "quickbooks__profitability_analysis", "column": "gross_profit"}] | [] | False |
| B6 | AVG(p.gross_profit) | [{"table": "quickbooks__profitability_analysis", "column": "gross_profit"}] | [] | False |
| B6 | AVG(p.gross_profit) | [{"table": "quickbooks__profitability_analysis", "column": "gross_profit"}] | [] | False |


未解析列血缘：[{"block": "B6", "column": "cutoff_date", "reason": "ambiguous_or_missing_source"}]

## S29

类别 `data`；来源 `query_db`；调用 `f615ac5d1c484e78b93ee30fc75a4250`；状态 `success`。

```sql
-- Compute coefficient of variation of gross_profit for high-vol customers over past 12 months
WITH date_range AS (
  SELECT DATE(MAX(transaction_date), '-12 months') AS cutoff_date
  FROM quickbooks__profitability_analysis
),
cust_vol AS (
  SELECT customer_id, AVG(customer_margin_volatility) AS vol
  FROM quickbooks__profitability_analysis
  GROUP BY customer_id
),
ordered AS (
  SELECT customer_id, vol,
    ROW_NUMBER() OVER (ORDER BY vol DESC) AS rn,
    COUNT(*) OVER () AS total
  FROM cust_vol
),
high_vol_cust AS (
  SELECT customer_id, vol
  FROM ordered
  WHERE rn <= total * 0.25
),
stats AS (
  SELECT 
    h.customer_id,
    h.vol,
    AVG(p.gross_profit) AS mean_gp,
    AVG(p.gross_profit * p.gross_profit) - AVG(p.gross_profit) * AVG(p.gross_profit) AS var_gp,
    COUNT(p.gross_profit) AS n_obs
  FROM high_vol_cust h
  JOIN quickbooks__profitability_analysis p ON h.customer_id = p.customer_id
    AND p.transaction_date >= (SELECT cutoff_date FROM date_range)
  GROUP BY h.customer_id, h.vol
)
SELECT 
  customer_id, vol, mean_gp,
  CASE WHEN var_gp < 0 THEN 0 ELSE SQRT(var_gp) END AS std_gp,
  CASE WHEN mean_gp = 0 THEN NULL 
       ELSE CASE WHEN var_gp < 0 THEN 0 ELSE SQRT(var_gp) END / mean_gp END AS cv_gp,
  n_obs
FROM stats
ORDER BY vol DESC
LIMIT 20
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-092/attempt-01/sql/S29.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-092/attempt-01/sql/S29.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-092/attempt-01/results/S29.rows.jsonl)；完整：True；SHA256：`161d41152cb6ef44a47d626c08855312565b47ef0316fb5e92ccf3610e7598b8`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "quickbooks__profitability_analysis", "kind": "base", "block": null, "base_tables": ["quickbooks__profitability_analysis"]}] | [] | [] |
| B2 | [{"alias": "quickbooks__profitability_analysis", "kind": "base", "block": null, "base_tables": ["quickbooks__profitability_analysis"]}] | [] | ["customer_id"] |
| B3 | [{"alias": "cust_vol", "kind": "derived", "block": "B2", "base_tables": ["quickbooks__profitability_analysis"]}] | [] | [] |
| B4 | [{"alias": "ordered", "kind": "derived", "block": "B3", "base_tables": ["quickbooks__profitability_analysis"]}] | [] | [] |
| B5 | [{"alias": "date_range", "kind": "derived", "block": "B1", "base_tables": ["quickbooks__profitability_analysis"]}] | [] | [] |
| B6 | [{"alias": "h", "kind": "derived", "block": "B4", "base_tables": ["quickbooks__profitability_analysis"]}, {"alias": "p", "kind": "base", "block": null, "base_tables": ["quickbooks__profitability_analysis"]}] | [{"type": "INNER", "right": "quickbooks__profitability_analysis AS p", "on": "h.customer_id = p.customer_id AND p.transaction_date >= (SELECT cutoff_date FROM date_range)", "using": []}] | ["h.customer_id", "h.vol"] |
| B7 | [{"alias": "stats", "kind": "derived", "block": "B6", "base_tables": ["quickbooks__profitability_analysis"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | MAX(transaction_date) | [{"table": "quickbooks__profitability_analysis", "column": "transaction_date"}] | [] | False |
| B2 | AVG(customer_margin_volatility) | [{"table": "quickbooks__profitability_analysis", "column": "customer_margin_volatility"}] | [] | False |
| B6 | AVG(p.gross_profit) | [{"table": "quickbooks__profitability_analysis", "column": "gross_profit"}] | [] | False |
| B6 | COUNT(p.gross_profit) | [{"table": "quickbooks__profitability_analysis", "column": "gross_profit"}] | [] | False |
| B6 | AVG(p.gross_profit * p.gross_profit) | [{"table": "quickbooks__profitability_analysis", "column": "gross_profit"}, {"table": "quickbooks__profitability_analysis", "column": "gross_profit"}] | [] | False |
| B6 | AVG(p.gross_profit) | [{"table": "quickbooks__profitability_analysis", "column": "gross_profit"}] | [] | False |
| B6 | AVG(p.gross_profit) | [{"table": "quickbooks__profitability_analysis", "column": "gross_profit"}] | [] | False |


未解析列血缘：[{"block": "B7", "column": "cutoff_date", "reason": "ambiguous_or_missing_source"}]

## S30

类别 `data`；来源 `query_db`；调用 `e3b993fec8f0421baca77fb85d4e7674`；状态 `success`。

```sql
-- Monthly gross profit per high-vol customer over past 12 months, then CV
WITH date_range AS (
  SELECT DATE(MAX(transaction_date), '-12 months') AS cutoff_date
  FROM quickbooks__profitability_analysis
),
cust_vol AS (
  SELECT customer_id, AVG(customer_margin_volatility) AS vol
  FROM quickbooks__profitability_analysis
  GROUP BY customer_id
),
ordered AS (
  SELECT customer_id, vol,
    ROW_NUMBER() OVER (ORDER BY vol DESC) AS rn,
    COUNT(*) OVER () AS total
  FROM cust_vol
),
high_vol_cust AS (
  SELECT customer_id, vol
  FROM ordered
  WHERE rn <= total * 0.25
),
monthly AS (
  SELECT 
    h.customer_id,
    STRFTIME('%Y-%m', p.transaction_date) AS month,
    SUM(p.gross_profit) AS monthly_gp
  FROM high_vol_cust h
  JOIN quickbooks__profitability_analysis p ON h.customer_id = p.customer_id
    AND p.transaction_date >= (SELECT cutoff_date FROM date_range)
  GROUP BY h.customer_id, STRFTIME('%Y-%m', p.transaction_date)
),
stats AS (
  SELECT 
    customer_id,
    AVG(monthly_gp) AS mean_mgp,
    AVG(monthly_gp * monthly_gp) - AVG(monthly_gp) * AVG(monthly_gp) AS var_mgp,
    COUNT(*) AS n_months
  FROM monthly
  GROUP BY customer_id
)
SELECT 
  customer_id,
  mean_mgp,
  CASE WHEN var_mgp < 0 THEN 0 ELSE SQRT(var_mgp) END AS std_mgp,
  CASE WHEN mean_mgp = 0 THEN NULL 
       ELSE CASE WHEN var_mgp < 0 THEN 0 ELSE SQRT(var_mgp) END / ABS(mean_mgp) END AS cv_mgp,
  n_months
FROM stats
ORDER BY cv_mgp DESC NULLS LAST
LIMIT 15
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-092/attempt-01/sql/S30.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-092/attempt-01/sql/S30.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-092/attempt-01/results/S30.rows.jsonl)；完整：True；SHA256：`89e780e4a8e395563250ae14bd47bbab53c990e8bcf8446d189c32ef0c668b79`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "quickbooks__profitability_analysis", "kind": "base", "block": null, "base_tables": ["quickbooks__profitability_analysis"]}] | [] | [] |
| B2 | [{"alias": "quickbooks__profitability_analysis", "kind": "base", "block": null, "base_tables": ["quickbooks__profitability_analysis"]}] | [] | ["customer_id"] |
| B3 | [{"alias": "cust_vol", "kind": "derived", "block": "B2", "base_tables": ["quickbooks__profitability_analysis"]}] | [] | [] |
| B4 | [{"alias": "ordered", "kind": "derived", "block": "B3", "base_tables": ["quickbooks__profitability_analysis"]}] | [] | [] |
| B5 | [{"alias": "date_range", "kind": "derived", "block": "B1", "base_tables": ["quickbooks__profitability_analysis"]}] | [] | [] |
| B6 | [{"alias": "h", "kind": "derived", "block": "B4", "base_tables": ["quickbooks__profitability_analysis"]}, {"alias": "p", "kind": "base", "block": null, "base_tables": ["quickbooks__profitability_analysis"]}] | [{"type": "INNER", "right": "quickbooks__profitability_analysis AS p", "on": "h.customer_id = p.customer_id AND p.transaction_date >= (SELECT cutoff_date FROM date_range)", "using": []}] | ["h.customer_id", "STRFTIME('%Y-%m', p.transaction_date)"] |
| B7 | [{"alias": "monthly", "kind": "derived", "block": "B6", "base_tables": ["quickbooks__profitability_analysis"]}] | [] | ["customer_id"] |
| B8 | [{"alias": "stats", "kind": "derived", "block": "B7", "base_tables": ["quickbooks__profitability_analysis"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | MAX(transaction_date) | [{"table": "quickbooks__profitability_analysis", "column": "transaction_date"}] | [] | False |
| B2 | AVG(customer_margin_volatility) | [{"table": "quickbooks__profitability_analysis", "column": "customer_margin_volatility"}] | [] | False |
| B6 | SUM(p.gross_profit) | [{"table": "quickbooks__profitability_analysis", "column": "gross_profit"}] | [] | False |
| B7 | AVG(monthly_gp) | [{"table": "quickbooks__profitability_analysis", "column": "gross_profit"}] | [] | False |
| B7 | COUNT(*) | [] | [] | True |
| B7 | AVG(monthly_gp * monthly_gp) | [{"table": "quickbooks__profitability_analysis", "column": "gross_profit"}, {"table": "quickbooks__profitability_analysis", "column": "gross_profit"}] | [] | False |
| B7 | AVG(monthly_gp) | [{"table": "quickbooks__profitability_analysis", "column": "gross_profit"}] | [] | False |
| B7 | AVG(monthly_gp) | [{"table": "quickbooks__profitability_analysis", "column": "gross_profit"}] | [] | False |


未解析列血缘：[{"block": "B8", "column": "cutoff_date", "reason": "ambiguous_or_missing_source"}]

## S31

类别 `data`；来源 `query_db`；调用 `f64a07757c884069886f4db659153d0f`；状态 `success`。

```sql
-- Overall CV of monthly gross profit for high-volatility customers
WITH date_range AS (
  SELECT DATE(MAX(transaction_date), '-12 months') AS cutoff_date
  FROM quickbooks__profitability_analysis
),
cust_vol AS (
  SELECT customer_id, AVG(customer_margin_volatility) AS vol
  FROM quickbooks__profitability_analysis
  GROUP BY customer_id
),
ordered AS (
  SELECT customer_id, vol,
    ROW_NUMBER() OVER (ORDER BY vol DESC) AS rn,
    COUNT(*) OVER () AS total
  FROM cust_vol
),
high_vol_cust AS (
  SELECT customer_id, vol
  FROM ordered
  WHERE rn <= total * 0.25
),
monthly AS (
  SELECT 
    h.customer_id,
    STRFTIME('%Y-%m', p.transaction_date) AS month,
    SUM(p.gross_profit) AS monthly_gp
  FROM high_vol_cust h
  JOIN quickbooks__profitability_analysis p ON h.customer_id = p.customer_id
    AND p.transaction_date >= (SELECT cutoff_date FROM date_range)
  GROUP BY h.customer_id, STRFTIME('%Y-%m', p.transaction_date)
)
SELECT 
  AVG(monthly_gp) AS overall_mean_gp,
  SQRT(AVG(monthly_gp * monthly_gp) - AVG(monthly_gp) * AVG(monthly_gp)) AS overall_std_gp,
  SQRT(AVG(monthly_gp * monthly_gp) - AVG(monthly_gp) * AVG(monthly_gp)) / ABS(AVG(monthly_gp)) AS overall_cv_gp,
  COUNT(*) AS total_month_obs,
  COUNT(DISTINCT customer_id) AS n_customers_with_data
FROM monthly
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-092/attempt-01/sql/S31.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-092/attempt-01/sql/S31.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-092/attempt-01/results/S31.rows.jsonl)；完整：True；SHA256：`42b281b74fe87f1d33a965cc434988c0f4e55036aca1e0fdf17c46f736d161b7`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "quickbooks__profitability_analysis", "kind": "base", "block": null, "base_tables": ["quickbooks__profitability_analysis"]}] | [] | [] |
| B2 | [{"alias": "quickbooks__profitability_analysis", "kind": "base", "block": null, "base_tables": ["quickbooks__profitability_analysis"]}] | [] | ["customer_id"] |
| B3 | [{"alias": "cust_vol", "kind": "derived", "block": "B2", "base_tables": ["quickbooks__profitability_analysis"]}] | [] | [] |
| B4 | [{"alias": "ordered", "kind": "derived", "block": "B3", "base_tables": ["quickbooks__profitability_analysis"]}] | [] | [] |
| B5 | [{"alias": "date_range", "kind": "derived", "block": "B1", "base_tables": ["quickbooks__profitability_analysis"]}] | [] | [] |
| B6 | [{"alias": "h", "kind": "derived", "block": "B4", "base_tables": ["quickbooks__profitability_analysis"]}, {"alias": "p", "kind": "base", "block": null, "base_tables": ["quickbooks__profitability_analysis"]}] | [{"type": "INNER", "right": "quickbooks__profitability_analysis AS p", "on": "h.customer_id = p.customer_id AND p.transaction_date >= (SELECT cutoff_date FROM date_range)", "using": []}] | ["h.customer_id", "STRFTIME('%Y-%m', p.transaction_date)"] |
| B7 | [{"alias": "monthly", "kind": "derived", "block": "B6", "base_tables": ["quickbooks__profitability_analysis"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | MAX(transaction_date) | [{"table": "quickbooks__profitability_analysis", "column": "transaction_date"}] | [] | False |
| B2 | AVG(customer_margin_volatility) | [{"table": "quickbooks__profitability_analysis", "column": "customer_margin_volatility"}] | [] | False |
| B6 | SUM(p.gross_profit) | [{"table": "quickbooks__profitability_analysis", "column": "gross_profit"}] | [] | False |
| B7 | AVG(monthly_gp) | [{"table": "quickbooks__profitability_analysis", "column": "gross_profit"}] | [] | False |
| B7 | COUNT(*) | [] | [] | True |
| B7 | COUNT(DISTINCT customer_id) | [{"table": "quickbooks__profitability_analysis", "column": "customer_id"}] | [] | False |
| B7 | AVG(monthly_gp * monthly_gp) | [{"table": "quickbooks__profitability_analysis", "column": "gross_profit"}, {"table": "quickbooks__profitability_analysis", "column": "gross_profit"}] | [] | False |
| B7 | AVG(monthly_gp) | [{"table": "quickbooks__profitability_analysis", "column": "gross_profit"}] | [] | False |
| B7 | AVG(monthly_gp) | [{"table": "quickbooks__profitability_analysis", "column": "gross_profit"}] | [] | False |
| B7 | AVG(monthly_gp) | [{"table": "quickbooks__profitability_analysis", "column": "gross_profit"}] | [] | False |
| B7 | AVG(monthly_gp * monthly_gp) | [{"table": "quickbooks__profitability_analysis", "column": "gross_profit"}, {"table": "quickbooks__profitability_analysis", "column": "gross_profit"}] | [] | False |
| B7 | AVG(monthly_gp) | [{"table": "quickbooks__profitability_analysis", "column": "gross_profit"}] | [] | False |
| B7 | AVG(monthly_gp) | [{"table": "quickbooks__profitability_analysis", "column": "gross_profit"}] | [] | False |


未解析列血缘：[{"block": "B7", "column": "cutoff_date", "reason": "ambiguous_or_missing_source"}]

## S32

类别 `data`；来源 `query_db`；调用 `31c2306673454d5bbc5f1729e41a3300`；状态 `success`。

```sql
SELECT DISTINCT revenue_year, revenue_quarter, COUNT(*) as cnt
FROM quickbooks__profitability_analysis
GROUP BY revenue_year, revenue_quarter
ORDER BY revenue_year, revenue_quarter
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-092/attempt-01/sql/S32.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-092/attempt-01/sql/S32.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-092/attempt-01/results/S32.rows.jsonl)；完整：True；SHA256：`f6a10f3f5c6fffdfe45397533149a4b198e036545476d70beb7644bda5d488fe`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "quickbooks__profitability_analysis", "kind": "base", "block": null, "base_tables": ["quickbooks__profitability_analysis"]}] | [] | ["revenue_year", "revenue_quarter"] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |


## S33

类别 `data`；来源 `query_db`；调用 `17aad498fd314c04949398d1f8c6affb`；状态 `success`。

```sql
-- Compare CV for bottom 25% (low volatility) customers
WITH cust_vol AS (
  SELECT customer_id, AVG(customer_margin_volatility) AS vol
  FROM quickbooks__profitability_analysis
  GROUP BY customer_id
),
ordered AS (
  SELECT customer_id, vol,
    ROW_NUMBER() OVER (ORDER BY vol ASC) AS rn,
    COUNT(*) OVER () AS total
  FROM cust_vol
),
low_vol_cust AS (
  SELECT customer_id, vol
  FROM ordered
  WHERE rn <= total * 0.25
)
SELECT COUNT(*) AS n_low_vol FROM low_vol_cust
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-092/attempt-01/sql/S33.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-092/attempt-01/sql/S33.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-092/attempt-01/results/S33.rows.jsonl)；完整：True；SHA256：`a482ada409c7c0efe39d3f42fd4364938468c884fb29d4e249f74acf895bba32`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "quickbooks__profitability_analysis", "kind": "base", "block": null, "base_tables": ["quickbooks__profitability_analysis"]}] | [] | ["customer_id"] |
| B2 | [{"alias": "cust_vol", "kind": "derived", "block": "B1", "base_tables": ["quickbooks__profitability_analysis"]}] | [] | [] |
| B3 | [{"alias": "ordered", "kind": "derived", "block": "B2", "base_tables": ["quickbooks__profitability_analysis"]}] | [] | [] |
| B4 | [{"alias": "low_vol_cust", "kind": "derived", "block": "B3", "base_tables": ["quickbooks__profitability_analysis"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | AVG(customer_margin_volatility) | [{"table": "quickbooks__profitability_analysis", "column": "customer_margin_volatility"}] | [] | False |
| B4 | COUNT(*) | [] | [] | True |


## S34

类别 `data`；来源 `query_db`；调用 `0f2608de81be404c9e907ba8fc412576`；状态 `success`。

```sql
-- QoQ invoice_total growth rate for high-vol customers (based on transaction_date quarters)
WITH date_range AS (
  SELECT DATE(MAX(transaction_date), '-12 months') AS cutoff_date
  FROM quickbooks__profitability_analysis
),
cust_vol AS (
  SELECT customer_id, AVG(customer_margin_volatility) AS vol
  FROM quickbooks__profitability_analysis
  GROUP BY customer_id
),
ordered AS (
  SELECT customer_id, vol,
    ROW_NUMBER() OVER (ORDER BY vol DESC) AS rn,
    COUNT(*) OVER () AS total
  FROM cust_vol
),
high_vol_cust AS (
  SELECT customer_id, vol
  FROM ordered
  WHERE rn <= total * 0.25
),
quarterly AS (
  SELECT 
    h.customer_id,
    STRFTIME('%Y', p.transaction_date) AS yr,
    CAST((CAST(STRFTIME('%m', p.transaction_date) AS INTEGER) + 2) / 3 AS INTEGER) AS qtr,
    SUM(p.invoice_total) AS qtr_invoice_total
  FROM high_vol_cust h
  JOIN quickbooks__profitability_analysis p ON h.customer_id = p.customer_id
    AND p.transaction_date >= (SELECT cutoff_date FROM date_range)
  GROUP BY h.customer_id, STRFTIME('%Y', p.transaction_date), CAST((CAST(STRFTIME('%m', p.transaction_date) AS INTEGER) + 2) / 3 AS INTEGER)
),
qoqs AS (
  SELECT 
    customer_id, yr, qtr, qtr_invoice_total,
    LAG(qtr_invoice_total) OVER (PARTITION BY customer_id ORDER BY yr, qtr) AS prev_qtr_total
  FROM quarterly
)
SELECT 
  customer_id, yr, qtr, qtr_invoice_total, prev_qtr_total,
  CASE WHEN prev_qtr_total IS NOT NULL AND prev_qtr_total <> 0 
       THEN (qtr_invoice_total - prev_qtr_total) / prev_qtr_total ELSE NULL END AS qoq_growth
FROM qoqs
WHERE prev_qtr_total IS NOT NULL
ORDER BY customer_id, yr, qtr
LIMIT 30
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-092/attempt-01/sql/S34.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-092/attempt-01/sql/S34.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-092/attempt-01/results/S34.rows.jsonl)；完整：True；SHA256：`1fbc84a75c22ab060417fbdd5b0da62ae96646086b90e71326fd7bb3af46aa13`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "quickbooks__profitability_analysis", "kind": "base", "block": null, "base_tables": ["quickbooks__profitability_analysis"]}] | [] | [] |
| B2 | [{"alias": "quickbooks__profitability_analysis", "kind": "base", "block": null, "base_tables": ["quickbooks__profitability_analysis"]}] | [] | ["customer_id"] |
| B3 | [{"alias": "cust_vol", "kind": "derived", "block": "B2", "base_tables": ["quickbooks__profitability_analysis"]}] | [] | [] |
| B4 | [{"alias": "ordered", "kind": "derived", "block": "B3", "base_tables": ["quickbooks__profitability_analysis"]}] | [] | [] |
| B5 | [{"alias": "date_range", "kind": "derived", "block": "B1", "base_tables": ["quickbooks__profitability_analysis"]}] | [] | [] |
| B6 | [{"alias": "h", "kind": "derived", "block": "B4", "base_tables": ["quickbooks__profitability_analysis"]}, {"alias": "p", "kind": "base", "block": null, "base_tables": ["quickbooks__profitability_analysis"]}] | [{"type": "INNER", "right": "quickbooks__profitability_analysis AS p", "on": "h.customer_id = p.customer_id AND p.transaction_date >= (SELECT cutoff_date FROM date_range)", "using": []}] | ["h.customer_id", "STRFTIME('%Y', p.transaction_date)", "CAST((CAST(STRFTIME('%m', p.transaction_date) AS INTEGER) + 2) / 3 AS INTEGER)"] |
| B7 | [{"alias": "quarterly", "kind": "derived", "block": "B6", "base_tables": ["quickbooks__profitability_analysis"]}] | [] | [] |
| B8 | [{"alias": "qoqs", "kind": "derived", "block": "B7", "base_tables": ["quickbooks__profitability_analysis"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | MAX(transaction_date) | [{"table": "quickbooks__profitability_analysis", "column": "transaction_date"}] | [] | False |
| B2 | AVG(customer_margin_volatility) | [{"table": "quickbooks__profitability_analysis", "column": "customer_margin_volatility"}] | [] | False |
| B6 | SUM(p.invoice_total) | [{"table": "quickbooks__profitability_analysis", "column": "invoice_total"}] | [] | False |


未解析列血缘：[{"block": "B8", "column": "cutoff_date", "reason": "ambiguous_or_missing_source"}]

## S35

类别 `data`；来源 `query_db`；调用 `38160a8029474b388f904bf671e6b1f6`；状态 `success`。

```sql
-- Variance of QoQ invoice_total growth rate for high-vol customers
WITH date_range AS (
  SELECT DATE(MAX(transaction_date), '-12 months') AS cutoff_date
  FROM quickbooks__profitability_analysis
),
cust_vol AS (
  SELECT customer_id, AVG(customer_margin_volatility) AS vol
  FROM quickbooks__profitability_analysis
  GROUP BY customer_id
),
ordered AS (
  SELECT customer_id, vol,
    ROW_NUMBER() OVER (ORDER BY vol DESC) AS rn,
    COUNT(*) OVER () AS total
  FROM cust_vol
),
high_vol_cust AS (
  SELECT customer_id, vol
  FROM ordered
  WHERE rn <= total * 0.25
),
quarterly AS (
  SELECT 
    h.customer_id,
    STRFTIME('%Y', p.transaction_date) AS yr,
    CAST((CAST(STRFTIME('%m', p.transaction_date) AS INTEGER) + 2) / 3 AS INTEGER) AS qtr,
    SUM(p.invoice_total) AS qtr_invoice_total
  FROM high_vol_cust h
  JOIN quickbooks__profitability_analysis p ON h.customer_id = p.customer_id
    AND p.transaction_date >= (SELECT cutoff_date FROM date_range)
  GROUP BY h.customer_id, STRFTIME('%Y', p.transaction_date), CAST((CAST(STRFTIME('%m', p.transaction_date) AS INTEGER) + 2) / 3 AS INTEGER)
),
qoqs AS (
  SELECT 
    customer_id, yr, qtr, qtr_invoice_total,
    LAG(qtr_invoice_total) OVER (PARTITION BY customer_id ORDER BY yr, qtr) AS prev_qtr_total
  FROM quarterly
)
SELECT 
  AVG(qoq_growth) AS mean_qoq_growth,
  AVG(qoq_growth * qoq_growth) - AVG(qoq_growth) * AVG(qoq_growth) AS var_qoq_growth,
  SQRT(AVG(qoq_growth * qoq_growth) - AVG(qoq_growth) * AVG(qoq_growth)) AS std_qoq_growth,
  COUNT(*) AS n_obs
FROM (
  SELECT 
    customer_id, yr, qtr, qtr_invoice_total, prev_qtr_total,
    CASE WHEN prev_qtr_total IS NOT NULL AND prev_qtr_total <> 0 
         THEN (qtr_invoice_total - prev_qtr_total) / prev_qtr_total ELSE NULL END AS qoq_growth
  FROM qoqs
  WHERE prev_qtr_total IS NOT NULL
) WHERE qoq_growth IS NOT NULL
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-092/attempt-01/sql/S35.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-092/attempt-01/sql/S35.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-092/attempt-01/results/S35.rows.jsonl)；完整：True；SHA256：`5d1d56f060f510c0b3cb1ecb9b00d95c761c7cf1ab227003a45f70bba65f1a8d`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "quickbooks__profitability_analysis", "kind": "base", "block": null, "base_tables": ["quickbooks__profitability_analysis"]}] | [] | [] |
| B2 | [{"alias": "quickbooks__profitability_analysis", "kind": "base", "block": null, "base_tables": ["quickbooks__profitability_analysis"]}] | [] | ["customer_id"] |
| B3 | [{"alias": "cust_vol", "kind": "derived", "block": "B2", "base_tables": ["quickbooks__profitability_analysis"]}] | [] | [] |
| B4 | [{"alias": "ordered", "kind": "derived", "block": "B3", "base_tables": ["quickbooks__profitability_analysis"]}] | [] | [] |
| B5 | [{"alias": "date_range", "kind": "derived", "block": "B1", "base_tables": ["quickbooks__profitability_analysis"]}] | [] | [] |
| B6 | [{"alias": "h", "kind": "derived", "block": "B4", "base_tables": ["quickbooks__profitability_analysis"]}, {"alias": "p", "kind": "base", "block": null, "base_tables": ["quickbooks__profitability_analysis"]}] | [{"type": "INNER", "right": "quickbooks__profitability_analysis AS p", "on": "h.customer_id = p.customer_id AND p.transaction_date >= (SELECT cutoff_date FROM date_range)", "using": []}] | ["h.customer_id", "STRFTIME('%Y', p.transaction_date)", "CAST((CAST(STRFTIME('%m', p.transaction_date) AS INTEGER) + 2) / 3 AS INTEGER)"] |
| B7 | [{"alias": "quarterly", "kind": "derived", "block": "B6", "base_tables": ["quickbooks__profitability_analysis"]}] | [] | [] |
| B8 | [{"alias": "qoqs", "kind": "derived", "block": "B7", "base_tables": ["quickbooks__profitability_analysis"]}] | [] | [] |
| B9 | [{"alias": "", "kind": "derived", "block": "B8", "base_tables": ["quickbooks__profitability_analysis"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | MAX(transaction_date) | [{"table": "quickbooks__profitability_analysis", "column": "transaction_date"}] | [] | False |
| B2 | AVG(customer_margin_volatility) | [{"table": "quickbooks__profitability_analysis", "column": "customer_margin_volatility"}] | [] | False |
| B6 | SUM(p.invoice_total) | [{"table": "quickbooks__profitability_analysis", "column": "invoice_total"}] | [] | False |
| B9 | AVG(qoq_growth) | [{"table": "quickbooks__profitability_analysis", "column": "customer_id"}, {"table": "quickbooks__profitability_analysis", "column": "invoice_total"}, {"table": "quickbooks__profitability_analysis", "column": "transaction_date"}, {"table": "quickbooks__profitability_analysis", "column": "transaction_date"}, {"table": "quickbooks__profitability_analysis", "column": "customer_id"}, {"table": "quickbooks__profitability_analysis", "column": "invoice_total"}, {"table": "quickbooks__profitability_analysis", "column": "transaction_date"}, {"table": "quickbooks__profitability_analysis", "column": "transaction_date"}, {"table": "quickbooks__profitability_analysis", "column": "customer_id"}, {"table": "quickbooks__profitability_analysis", "column": "invoice_total"}, {"table": "quickbooks__profitability_analysis", "column": "transaction_date"}, {"table": "quickbooks__profitability_analysis", "column": "transaction_date"}, {"table": "quickbooks__profitability_analysis", "column": "invoice_total"}, {"table": "quickbooks__profitability_analysis", "column": "customer_id"}, {"table": "quickbooks__profitability_analysis", "column": "invoice_total"}, {"table": "quickbooks__profitability_analysis", "column": "transaction_date"}, {"table": "quickbooks__profitability_analysis", "column": "transaction_date"}] | [] | False |
| B9 | COUNT(*) | [] | [] | True |
| B9 | AVG(qoq_growth * qoq_growth) | [{"table": "quickbooks__profitability_analysis", "column": "customer_id"}, {"table": "quickbooks__profitability_analysis", "column": "invoice_total"}, {"table": "quickbooks__profitability_analysis", "column": "transaction_date"}, {"table": "quickbooks__profitability_analysis", "column": "transaction_date"}, {"table": "quickbooks__profitability_analysis", "column": "customer_id"}, {"table": "quickbooks__profitability_analysis", "column": "invoice_total"}, {"table": "quickbooks__profitability_analysis", "column": "transaction_date"}, {"table": "quickbooks__profitability_analysis", "column": "transaction_date"}, {"table": "quickbooks__profitability_analysis", "column": "customer_id"}, {"table": "quickbooks__profitability_analysis", "column": "invoice_total"}, {"table": "quickbooks__profitability_analysis", "column": "transaction_date"}, {"table": "quickbooks__profitability_analysis", "column": "transaction_date"}, {"table": "quickbooks__profitability_analysis", "column": "invoice_total"}, {"table": "quickbooks__profitability_analysis", "column": "customer_id"}, {"table": "quickbooks__profitability_analysis", "column": "invoice_total"}, {"table": "quickbooks__profitability_analysis", "column": "transaction_date"}, {"table": "quickbooks__profitability_analysis", "column": "transaction_date"}, {"table": "quickbooks__profitability_analysis", "column": "customer_id"}, {"table": "quickbooks__profitability_analysis", "column": "invoice_total"}, {"table": "quickbooks__profitability_analysis", "column": "transaction_date"}, {"table": "quickbooks__profitability_analysis", "column": "transaction_date"}, {"table": "quickbooks__profitability_analysis", "column": "customer_id"}, {"table": "quickbooks__profitability_analysis", "column": "invoice_total"}, {"table": "quickbooks__profitability_analysis", "column": "transaction_date"}, {"table": "quickbooks__profitability_analysis", "column": "transaction_date"}, {"table": "quickbooks__profitability_analysis", "column": "customer_id"}, {"table": "quickbooks__profitability_analysis", "column": "invoice_total"}, {"table": "quickbooks__profitability_analysis", "column": "transaction_date"}, {"table": "quickbooks__profitability_analysis", "column": "transaction_date"}, {"table": "quickbooks__profitability_analysis", "column": "invoice_total"}, {"table": "quickbooks__profitability_analysis", "column": "customer_id"}, {"table": "quickbooks__profitability_analysis", "column": "invoice_total"}, {"table": "quickbooks__profitability_analysis", "column": "transaction_date"}, {"table": "quickbooks__profitability_analysis", "column": "transaction_date"}] | [] | False |
| B9 | AVG(qoq_growth) | [{"table": "quickbooks__profitability_analysis", "column": "customer_id"}, {"table": "quickbooks__profitability_analysis", "column": "invoice_total"}, {"table": "quickbooks__profitability_analysis", "column": "transaction_date"}, {"table": "quickbooks__profitability_analysis", "column": "transaction_date"}, {"table": "quickbooks__profitability_analysis", "column": "customer_id"}, {"table": "quickbooks__profitability_analysis", "column": "invoice_total"}, {"table": "quickbooks__profitability_analysis", "column": "transaction_date"}, {"table": "quickbooks__profitability_analysis", "column": "transaction_date"}, {"table": "quickbooks__profitability_analysis", "column": "customer_id"}, {"table": "quickbooks__profitability_analysis", "column": "invoice_total"}, {"table": "quickbooks__profitability_analysis", "column": "transaction_date"}, {"table": "quickbooks__profitability_analysis", "column": "transaction_date"}, {"table": "quickbooks__profitability_analysis", "column": "invoice_total"}, {"table": "quickbooks__profitability_analysis", "column": "customer_id"}, {"table": "quickbooks__profitability_analysis", "column": "invoice_total"}, {"table": "quickbooks__profitability_analysis", "column": "transaction_date"}, {"table": "quickbooks__profitability_analysis", "column": "transaction_date"}] | [] | False |
| B9 | AVG(qoq_growth) | [{"table": "quickbooks__profitability_analysis", "column": "customer_id"}, {"table": "quickbooks__profitability_analysis", "column": "invoice_total"}, {"table": "quickbooks__profitability_analysis", "column": "transaction_date"}, {"table": "quickbooks__profitability_analysis", "column": "transaction_date"}, {"table": "quickbooks__profitability_analysis", "column": "customer_id"}, {"table": "quickbooks__profitability_analysis", "column": "invoice_total"}, {"table": "quickbooks__profitability_analysis", "column": "transaction_date"}, {"table": "quickbooks__profitability_analysis", "column": "transaction_date"}, {"table": "quickbooks__profitability_analysis", "column": "customer_id"}, {"table": "quickbooks__profitability_analysis", "column": "invoice_total"}, {"table": "quickbooks__profitability_analysis", "column": "transaction_date"}, {"table": "quickbooks__profitability_analysis", "column": "transaction_date"}, {"table": "quickbooks__profitability_analysis", "column": "invoice_total"}, {"table": "quickbooks__profitability_analysis", "column": "customer_id"}, {"table": "quickbooks__profitability_analysis", "column": "invoice_total"}, {"table": "quickbooks__profitability_analysis", "column": "transaction_date"}, {"table": "quickbooks__profitability_analysis", "column": "transaction_date"}] | [] | False |
| B9 | AVG(qoq_growth * qoq_growth) | [{"table": "quickbooks__profitability_analysis", "column": "customer_id"}, {"table": "quickbooks__profitability_analysis", "column": "invoice_total"}, {"table": "quickbooks__profitability_analysis", "column": "transaction_date"}, {"table": "quickbooks__profitability_analysis", "column": "transaction_date"}, {"table": "quickbooks__profitability_analysis", "column": "customer_id"}, {"table": "quickbooks__profitability_analysis", "column": "invoice_total"}, {"table": "quickbooks__profitability_analysis", "column": "transaction_date"}, {"table": "quickbooks__profitability_analysis", "column": "transaction_date"}, {"table": "quickbooks__profitability_analysis", "column": "customer_id"}, {"table": "quickbooks__profitability_analysis", "column": "invoice_total"}, {"table": "quickbooks__profitability_analysis", "column": "transaction_date"}, {"table": "quickbooks__profitability_analysis", "column": "transaction_date"}, {"table": "quickbooks__profitability_analysis", "column": "invoice_total"}, {"table": "quickbooks__profitability_analysis", "column": "customer_id"}, {"table": "quickbooks__profitability_analysis", "column": "invoice_total"}, {"table": "quickbooks__profitability_analysis", "column": "transaction_date"}, {"table": "quickbooks__profitability_analysis", "column": "transaction_date"}, {"table": "quickbooks__profitability_analysis", "column": "customer_id"}, {"table": "quickbooks__profitability_analysis", "column": "invoice_total"}, {"table": "quickbooks__profitability_analysis", "column": "transaction_date"}, {"table": "quickbooks__profitability_analysis", "column": "transaction_date"}, {"table": "quickbooks__profitability_analysis", "column": "customer_id"}, {"table": "quickbooks__profitability_analysis", "column": "invoice_total"}, {"table": "quickbooks__profitability_analysis", "column": "transaction_date"}, {"table": "quickbooks__profitability_analysis", "column": "transaction_date"}, {"table": "quickbooks__profitability_analysis", "column": "customer_id"}, {"table": "quickbooks__profitability_analysis", "column": "invoice_total"}, {"table": "quickbooks__profitability_analysis", "column": "transaction_date"}, {"table": "quickbooks__profitability_analysis", "column": "transaction_date"}, {"table": "quickbooks__profitability_analysis", "column": "invoice_total"}, {"table": "quickbooks__profitability_analysis", "column": "customer_id"}, {"table": "quickbooks__profitability_analysis", "column": "invoice_total"}, {"table": "quickbooks__profitability_analysis", "column": "transaction_date"}, {"table": "quickbooks__profitability_analysis", "column": "transaction_date"}] | [] | False |
| B9 | AVG(qoq_growth) | [{"table": "quickbooks__profitability_analysis", "column": "customer_id"}, {"table": "quickbooks__profitability_analysis", "column": "invoice_total"}, {"table": "quickbooks__profitability_analysis", "column": "transaction_date"}, {"table": "quickbooks__profitability_analysis", "column": "transaction_date"}, {"table": "quickbooks__profitability_analysis", "column": "customer_id"}, {"table": "quickbooks__profitability_analysis", "column": "invoice_total"}, {"table": "quickbooks__profitability_analysis", "column": "transaction_date"}, {"table": "quickbooks__profitability_analysis", "column": "transaction_date"}, {"table": "quickbooks__profitability_analysis", "column": "customer_id"}, {"table": "quickbooks__profitability_analysis", "column": "invoice_total"}, {"table": "quickbooks__profitability_analysis", "column": "transaction_date"}, {"table": "quickbooks__profitability_analysis", "column": "transaction_date"}, {"table": "quickbooks__profitability_analysis", "column": "invoice_total"}, {"table": "quickbooks__profitability_analysis", "column": "customer_id"}, {"table": "quickbooks__profitability_analysis", "column": "invoice_total"}, {"table": "quickbooks__profitability_analysis", "column": "transaction_date"}, {"table": "quickbooks__profitability_analysis", "column": "transaction_date"}] | [] | False |
| B9 | AVG(qoq_growth) | [{"table": "quickbooks__profitability_analysis", "column": "customer_id"}, {"table": "quickbooks__profitability_analysis", "column": "invoice_total"}, {"table": "quickbooks__profitability_analysis", "column": "transaction_date"}, {"table": "quickbooks__profitability_analysis", "column": "transaction_date"}, {"table": "quickbooks__profitability_analysis", "column": "customer_id"}, {"table": "quickbooks__profitability_analysis", "column": "invoice_total"}, {"table": "quickbooks__profitability_analysis", "column": "transaction_date"}, {"table": "quickbooks__profitability_analysis", "column": "transaction_date"}, {"table": "quickbooks__profitability_analysis", "column": "customer_id"}, {"table": "quickbooks__profitability_analysis", "column": "invoice_total"}, {"table": "quickbooks__profitability_analysis", "column": "transaction_date"}, {"table": "quickbooks__profitability_analysis", "column": "transaction_date"}, {"table": "quickbooks__profitability_analysis", "column": "invoice_total"}, {"table": "quickbooks__profitability_analysis", "column": "customer_id"}, {"table": "quickbooks__profitability_analysis", "column": "invoice_total"}, {"table": "quickbooks__profitability_analysis", "column": "transaction_date"}, {"table": "quickbooks__profitability_analysis", "column": "transaction_date"}] | [] | False |


未解析列血缘：[{"block": "B9", "column": "cutoff_date", "reason": "ambiguous_or_missing_source"}]

## S36

类别 `data`；来源 `query_db`；调用 `285e0944263f471bbe393f7aa690cc22`；状态 `success`。

```sql
-- Behavioral profile of high-vol customers
WITH cust_vol AS (
  SELECT customer_id, AVG(customer_margin_volatility) AS vol
  FROM quickbooks__profitability_analysis
  GROUP BY customer_id
),
ordered AS (
  SELECT customer_id, vol,
    ROW_NUMBER() OVER (ORDER BY vol DESC) AS rn,
    COUNT(*) OVER () AS total
  FROM cust_vol
),
seg AS (
  SELECT customer_id, vol,
    CASE WHEN rn <= total * 0.25 THEN 'HighVol'
         WHEN rn > total * 0.75 THEN 'LowVol'
         ELSE 'MidVol' END AS vol_segment
  FROM ordered
)
SELECT 
  s.vol_segment,
  a.rfm_segment,
  COUNT(*) AS n_customers
FROM seg s
JOIN quickbooks__customer_analytics a ON s.customer_id = a.customer_id
GROUP BY s.vol_segment, a.rfm_segment
ORDER BY s.vol_segment, n_customers DESC
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-092/attempt-01/sql/S36.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-092/attempt-01/sql/S36.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-092/attempt-01/results/S36.rows.jsonl)；完整：True；SHA256：`e8e4c76208041784d76d45ec8883ce004ca9425092c8b5e2e03d5aac83725087`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "quickbooks__profitability_analysis", "kind": "base", "block": null, "base_tables": ["quickbooks__profitability_analysis"]}] | [] | ["customer_id"] |
| B2 | [{"alias": "cust_vol", "kind": "derived", "block": "B1", "base_tables": ["quickbooks__profitability_analysis"]}] | [] | [] |
| B3 | [{"alias": "ordered", "kind": "derived", "block": "B2", "base_tables": ["quickbooks__profitability_analysis"]}] | [] | [] |
| B4 | [{"alias": "s", "kind": "derived", "block": "B3", "base_tables": ["quickbooks__profitability_analysis"]}, {"alias": "a", "kind": "base", "block": null, "base_tables": ["quickbooks__customer_analytics"]}] | [{"type": "INNER", "right": "quickbooks__customer_analytics AS a", "on": "s.customer_id = a.customer_id", "using": []}] | ["s.vol_segment", "a.rfm_segment"] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | AVG(customer_margin_volatility) | [{"table": "quickbooks__profitability_analysis", "column": "customer_margin_volatility"}] | [] | False |
| B4 | COUNT(*) | [] | [] | True |


## S37

类别 `data`；来源 `query_db`；调用 `0a6c09598fad40109c1b69298069166e`；状态 `success`。

```sql
-- Payment behavior profile by volatility segment
WITH cust_vol AS (
  SELECT customer_id, AVG(customer_margin_volatility) AS vol
  FROM quickbooks__profitability_analysis
  GROUP BY customer_id
),
ordered AS (
  SELECT customer_id, vol,
    ROW_NUMBER() OVER (ORDER BY vol DESC) AS rn,
    COUNT(*) OVER () AS total
  FROM cust_vol
),
seg AS (
  SELECT customer_id, vol,
    CASE WHEN rn <= total * 0.25 THEN 'HighVol'
         WHEN rn > total * 0.75 THEN 'LowVol'
         ELSE 'MidVol' END AS vol_segment
  FROM ordered
)
SELECT 
  s.vol_segment,
  a.payment_behavior,
  COUNT(*) AS n_customers
FROM seg s
JOIN quickbooks__customer_analytics a ON s.customer_id = a.customer_id
GROUP BY s.vol_segment, a.payment_behavior
ORDER BY s.vol_segment, n_customers DESC
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-092/attempt-01/sql/S37.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-092/attempt-01/sql/S37.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-092/attempt-01/results/S37.rows.jsonl)；完整：True；SHA256：`18557deccf5300dddef9dc7adf559a63f44b8393b3a0a35267e768db031fded0`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "quickbooks__profitability_analysis", "kind": "base", "block": null, "base_tables": ["quickbooks__profitability_analysis"]}] | [] | ["customer_id"] |
| B2 | [{"alias": "cust_vol", "kind": "derived", "block": "B1", "base_tables": ["quickbooks__profitability_analysis"]}] | [] | [] |
| B3 | [{"alias": "ordered", "kind": "derived", "block": "B2", "base_tables": ["quickbooks__profitability_analysis"]}] | [] | [] |
| B4 | [{"alias": "s", "kind": "derived", "block": "B3", "base_tables": ["quickbooks__profitability_analysis"]}, {"alias": "a", "kind": "base", "block": null, "base_tables": ["quickbooks__customer_analytics"]}] | [{"type": "INNER", "right": "quickbooks__customer_analytics AS a", "on": "s.customer_id = a.customer_id", "using": []}] | ["s.vol_segment", "a.payment_behavior"] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | AVG(customer_margin_volatility) | [{"table": "quickbooks__profitability_analysis", "column": "customer_margin_volatility"}] | [] | False |
| B4 | COUNT(*) | [] | [] | True |


## S38

类别 `data`；来源 `query_db`；调用 `b195db71d87e48a0a5ac4e8513c34e67`；状态 `success`。

```sql
-- Lifecycle stage profile by volatility segment
WITH cust_vol AS (
  SELECT customer_id, AVG(customer_margin_volatility) AS vol
  FROM quickbooks__profitability_analysis
  GROUP BY customer_id
),
ordered AS (
  SELECT customer_id, vol,
    ROW_NUMBER() OVER (ORDER BY vol DESC) AS rn,
    COUNT(*) OVER () AS total
  FROM cust_vol
),
seg AS (
  SELECT customer_id, vol,
    CASE WHEN rn <= total * 0.25 THEN 'HighVol'
         WHEN rn > total * 0.75 THEN 'LowVol'
         ELSE 'MidVol' END AS vol_segment
  FROM ordered
)
SELECT 
  s.vol_segment,
  a.lifecycle_stage,
  COUNT(*) AS n_customers
FROM seg s
JOIN quickbooks__customer_analytics a ON s.customer_id = a.customer_id
GROUP BY s.vol_segment, a.lifecycle_stage
ORDER BY s.vol_segment, n_customers DESC
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-092/attempt-01/sql/S38.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-092/attempt-01/sql/S38.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-092/attempt-01/results/S38.rows.jsonl)；完整：True；SHA256：`55dc89fa52a478d20cacba36963dd25373fa6481aadd647ab016ef9ad46e4104`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "quickbooks__profitability_analysis", "kind": "base", "block": null, "base_tables": ["quickbooks__profitability_analysis"]}] | [] | ["customer_id"] |
| B2 | [{"alias": "cust_vol", "kind": "derived", "block": "B1", "base_tables": ["quickbooks__profitability_analysis"]}] | [] | [] |
| B3 | [{"alias": "ordered", "kind": "derived", "block": "B2", "base_tables": ["quickbooks__profitability_analysis"]}] | [] | [] |
| B4 | [{"alias": "s", "kind": "derived", "block": "B3", "base_tables": ["quickbooks__profitability_analysis"]}, {"alias": "a", "kind": "base", "block": null, "base_tables": ["quickbooks__customer_analytics"]}] | [{"type": "INNER", "right": "quickbooks__customer_analytics AS a", "on": "s.customer_id = a.customer_id", "using": []}] | ["s.vol_segment", "a.lifecycle_stage"] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | AVG(customer_margin_volatility) | [{"table": "quickbooks__profitability_analysis", "column": "customer_margin_volatility"}] | [] | False |
| B4 | COUNT(*) | [] | [] | True |


## S39

类别 `data`；来源 `query_db`；调用 `70836f5648bc4141a07fd8d3b3a1d436`；状态 `success`。

```sql
-- Revenue trend correlation and other continuous behavioral features by segment
WITH cust_vol AS (
  SELECT customer_id, AVG(customer_margin_volatility) AS vol
  FROM quickbooks__profitability_analysis
  GROUP BY customer_id
),
ordered AS (
  SELECT customer_id, vol,
    ROW_NUMBER() OVER (ORDER BY vol DESC) AS rn,
    COUNT(*) OVER () AS total
  FROM cust_vol
),
seg AS (
  SELECT customer_id, vol,
    CASE WHEN rn <= total * 0.25 THEN 'HighVol'
         WHEN rn > total * 0.75 THEN 'LowVol'
         ELSE 'MidVol' END AS vol_segment
  FROM ordered
)
SELECT 
  s.vol_segment,
  COUNT(*) AS n,
  AVG(a.revenue_trend_correlation) AS avg_trend_corr,
  AVG(a.credit_score) AS avg_credit_score,
  AVG(a.avg_payment_days_12m) AS avg_payment_days,
  AVG(a.overdue_count_12m) AS avg_overdue_count,
  AVG(a.overall_customer_score) AS avg_overall_score,
  AVG(a.revenue_volatility) AS avg_rev_volatility
FROM seg s
JOIN quickbooks__customer_analytics a ON s.customer_id = a.customer_id
GROUP BY s.vol_segment
ORDER BY s.vol_segment
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-092/attempt-01/sql/S39.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-092/attempt-01/sql/S39.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-092/attempt-01/results/S39.rows.jsonl)；完整：True；SHA256：`cfc2b5bc69eede81de891616a00f5bfeb6c931277d4184e5613db9c4f014222f`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "quickbooks__profitability_analysis", "kind": "base", "block": null, "base_tables": ["quickbooks__profitability_analysis"]}] | [] | ["customer_id"] |
| B2 | [{"alias": "cust_vol", "kind": "derived", "block": "B1", "base_tables": ["quickbooks__profitability_analysis"]}] | [] | [] |
| B3 | [{"alias": "ordered", "kind": "derived", "block": "B2", "base_tables": ["quickbooks__profitability_analysis"]}] | [] | [] |
| B4 | [{"alias": "s", "kind": "derived", "block": "B3", "base_tables": ["quickbooks__profitability_analysis"]}, {"alias": "a", "kind": "base", "block": null, "base_tables": ["quickbooks__customer_analytics"]}] | [{"type": "INNER", "right": "quickbooks__customer_analytics AS a", "on": "s.customer_id = a.customer_id", "using": []}] | ["s.vol_segment"] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | AVG(customer_margin_volatility) | [{"table": "quickbooks__profitability_analysis", "column": "customer_margin_volatility"}] | [] | False |
| B4 | COUNT(*) | [] | [] | True |
| B4 | AVG(a.revenue_trend_correlation) | [{"table": "quickbooks__customer_analytics", "column": "revenue_trend_correlation"}] | [] | False |
| B4 | AVG(a.credit_score) | [{"table": "quickbooks__customer_analytics", "column": "credit_score"}] | [] | False |
| B4 | AVG(a.avg_payment_days_12m) | [{"table": "quickbooks__customer_analytics", "column": "avg_payment_days_12m"}] | [] | False |
| B4 | AVG(a.overdue_count_12m) | [{"table": "quickbooks__customer_analytics", "column": "overdue_count_12m"}] | [] | False |
| B4 | AVG(a.overall_customer_score) | [{"table": "quickbooks__customer_analytics", "column": "overall_customer_score"}] | [] | False |
| B4 | AVG(a.revenue_volatility) | [{"table": "quickbooks__customer_analytics", "column": "revenue_volatility"}] | [] | False |


## S40

类别 `data`；来源 `query_db`；调用 `bb98c000d5834162a01b25c88aa51434`；状态 `success`。

```sql
SELECT 
  COUNT(*) AS total,
  COUNT(revenue_trend_correlation) AS n_trend_corr,
  COUNT(credit_score) AS n_credit,
  COUNT(avg_payment_days_12m) AS n_pay_days,
  COUNT(overdue_count_12m) AS n_overdue,
  COUNT(overall_customer_score) AS n_overall,
  COUNT(revenue_volatility) AS n_rev_vol,
  COUNT(rfm_segment) AS n_rfm,
  COUNT(payment_behavior) AS n_payment,
  COUNT(lifecycle_stage) AS n_lifecycle,
  COUNT(customer_value_segment) AS n_value_seg,
  COUNT(risk_assessment) AS n_risk,
  COUNT(credit_grade) AS n_credit_grade,
  COUNT(payment_timeliness_score) AS n_pay_timeliness,
  COUNT(business_stability_score) AS n_biz_stab
FROM quickbooks__customer_analytics
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-092/attempt-01/sql/S40.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-092/attempt-01/sql/S40.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-092/attempt-01/results/S40.rows.jsonl)；完整：True；SHA256：`495e8b96083f4867d42564fa55e51954c3984b2bbb65c725702592867990213b`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "quickbooks__customer_analytics", "kind": "base", "block": null, "base_tables": ["quickbooks__customer_analytics"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |
| B1 | COUNT(revenue_trend_correlation) | [{"table": "quickbooks__customer_analytics", "column": "revenue_trend_correlation"}] | [] | False |
| B1 | COUNT(credit_score) | [{"table": "quickbooks__customer_analytics", "column": "credit_score"}] | [] | False |
| B1 | COUNT(avg_payment_days_12m) | [{"table": "quickbooks__customer_analytics", "column": "avg_payment_days_12m"}] | [] | False |
| B1 | COUNT(overdue_count_12m) | [{"table": "quickbooks__customer_analytics", "column": "overdue_count_12m"}] | [] | False |
| B1 | COUNT(overall_customer_score) | [{"table": "quickbooks__customer_analytics", "column": "overall_customer_score"}] | [] | False |
| B1 | COUNT(revenue_volatility) | [{"table": "quickbooks__customer_analytics", "column": "revenue_volatility"}] | [] | False |
| B1 | COUNT(rfm_segment) | [{"table": "quickbooks__customer_analytics", "column": "rfm_segment"}] | [] | False |
| B1 | COUNT(payment_behavior) | [{"table": "quickbooks__customer_analytics", "column": "payment_behavior"}] | [] | False |
| B1 | COUNT(lifecycle_stage) | [{"table": "quickbooks__customer_analytics", "column": "lifecycle_stage"}] | [] | False |
| B1 | COUNT(customer_value_segment) | [{"table": "quickbooks__customer_analytics", "column": "customer_value_segment"}] | [] | False |
| B1 | COUNT(risk_assessment) | [{"table": "quickbooks__customer_analytics", "column": "risk_assessment"}] | [] | False |
| B1 | COUNT(credit_grade) | [{"table": "quickbooks__customer_analytics", "column": "credit_grade"}] | [] | False |
| B1 | COUNT(payment_timeliness_score) | [{"table": "quickbooks__customer_analytics", "column": "payment_timeliness_score"}] | [] | False |
| B1 | COUNT(business_stability_score) | [{"table": "quickbooks__customer_analytics", "column": "business_stability_score"}] | [] | False |

