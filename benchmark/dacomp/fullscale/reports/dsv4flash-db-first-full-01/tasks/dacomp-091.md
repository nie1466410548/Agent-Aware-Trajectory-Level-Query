# dacomp-091

From the `quickbooks__vendor_performance` table, identify 'high-quality, shrinking-spend' …

运行：服务中断。官方未评分。全部 SQL 尝试/成功 34/32；数据 SQL 32/30；Python 3 次。

完整原题：

From the `quickbooks__vendor_performance` table, identify 'high-quality, shrinking-spend' vendors where `annual_spend_growth_pct` is negative but the `overall_performance_score` is 7 or higher. For these vendors, calculate the spend volatility coefficient (`spend_volatility` / `total_lifetime_spend`) and a composite risk score (`payment_completion_rate` * 0.4 + `business_value_score`/10 * 0.6). Using the corresponding transaction records for each `vendor_id` from the `quickbooks__general_ledger` table, calculate the spend change rate for the last 12 months versus the prior 12 months for each vendor, categorized by `account_type`. Also, calculate the transaction frequency density (number of transactions / active days) for each account type. Based on the `quickbooks__cashflow_forecast` data, build a cash flow impact model assuming a 30% reduction in collaboration with these vendors, and calculate the adjusted monthly outflow forecast and the change in the liquidity risk index.

| 表 | 行数 | 列数 |
| --- | --- | --- |
| quickbooks__cashflow_forecast | 18 | 19 |
| quickbooks__general_ledger | 54545 | 30 |
| quickbooks__vendor_performance | 1443 | 49 |


实际路线（分析者依据 SQL/源码概括，不代表 Agent 自述）：SQL 筛选高质缩支供应商、比较账目并构建预测调整 → Python 汇总与图表 → 服务错误中断。

数据库大小：20,451,328 字节。

## 数据 SQL

| SQL | 状态 | 基础表 | Join 输入/类型 | GROUP BY | 聚合表达式 | 结果行数 | 数据库 ms |
| --- | --- | --- | --- | --- | --- | --- | --- |
| [S3/Q1](#s3) | success | ["quickbooks__vendor_performance"] | 0 / {} | [] | ["COUNT(*)"] | 1 | 0.887 |
| [S4/Q2](#s4) | success | ["quickbooks__general_ledger"] | 0 / {} | [] | ["COUNT(*)"] | 1 | 6.521 |
| [S5/Q3](#s5) | success | ["quickbooks__cashflow_forecast"] | 0 / {} | [] | ["COUNT(*)", "MIN(forecast_month)", "MAX(forecast_month)"] | 1 | 0.364 |
| [S6/Q4](#s6) | success | ["quickbooks__vendor_performance"] | 0 / {} | [] | [] | 342 | 1.758 |
| [S7/Q5](#s7) | success | ["quickbooks__vendor_performance"] | 0 / {} | [] | ["COUNT(*)", "AVG(spend_volatility / NULLIF(total_lifetime_spend, 0))", "MIN(spend_volatility / NULLIF(total_lifetime_spend, 0))", "MAX(spend_volatility / NULLIF(total_lifetime_spend, 0))", "AVG(payment_completion_rate * 0.4 + business_value_score / 10.0 * 0.6)", "MIN(payment_completion_rate * 0.4 + business_value_score / 10.0 * 0.6)", "MAX(payment_completion_rate * 0.4 + business_value_score / 10.0 * 0.6)", "SUM(total_lifetime_spend)", "SUM(spend_volatility)", "SUM(total_outstanding)"] | 1 | 1.084 |
| [S8/Q6](#s8) | success | ["quickbooks__vendor_performance"] | 0 / {} | [] | [] | 342 | 1.189 |
| [S9/Q7](#s9) | success | ["quickbooks__general_ledger", "quickbooks__vendor_performance"] | 0 / {} | [] | ["MIN(transaction_date)", "MAX(transaction_date)", "COUNT(DISTINCT transaction_date)", "COUNT(DISTINCT account_type)"] | 1 | 28.008 |
| [S10/Q8](#s10) | success | ["quickbooks__general_ledger", "quickbooks__vendor_performance"] | 0 / {} | ["account_type"] | ["COUNT(*)", "MIN(transaction_date)", "MAX(transaction_date)", "SUM(amount)"] | 4 | 28.495 |
| [S11/Q9](#s11) | success | ["quickbooks__general_ledger", "quickbooks__vendor_performance"] | 0 / {} | [] | ["COUNT(DISTINCT vendor_id)"] | 1 | 24.389 |
| [S12/Q10](#s12) | success | ["quickbooks__general_ledger", "quickbooks__vendor_performance"] | 0 / {} | ["vendor_id", "account_type"] | ["COUNT(*)", "COUNT(DISTINCT transaction_date)", "SUM(CASE WHEN transaction_date >= '2024-10-15' THEN amount ELSE 0 END)", "SUM(CASE WHEN transaction_date < '2024-10-15' THEN amount ELSE 0 END)"] | 1368 | 37.896 |
| [S13/Q11](#s13) | success | ["quickbooks__general_ledger", "quickbooks__vendor_performance"] | 0 / {} | ["vendor_id", "account_type"] | ["SUM(CASE WHEN transaction_date >= '2024-10-15' THEN amount ELSE 0 END)", "SUM(CASE WHEN transaction_date < '2024-10-15' THEN amount ELSE 0 END)", "COUNT(*)", "COUNT(DISTINCT transaction_date)"] | 1368 | 39.262 |
| [S14/Q12](#s14) | success | ["quickbooks__general_ledger", "quickbooks__vendor_performance"] | 0 / {} | ["vendor_id", "account_type", "account_type"] | ["SUM(CASE WHEN transaction_date >= '2024-10-15' THEN amount ELSE 0 END)", "SUM(CASE WHEN transaction_date < '2024-10-15' THEN amount ELSE 0 END)", "COUNT(*)", "COUNT(DISTINCT transaction_date)", "SUM(CASE WHEN transaction_date < '2024-10-15' THEN amount ELSE 0 END)", "SUM(CASE WHEN transaction_date < '2024-10-15' THEN amount ELSE 0 END)", "SUM(CASE WHEN transaction_date >= '2024-10-15' THEN amount ELSE 0 END)", "SUM(CASE WHEN transaction_date < '2024-10-15' THEN amount ELSE 0 END)", "COUNT(*)", "AVG(spend_change_rate_pct)", "MIN(spend_change_rate_pct)", "MAX(spend_change_rate_pct)", "AVG(tx_frequency_density)", "SUM(spend_last12)", "SUM(spend_prior12)"] | 4 | 48.485 |
| [S15/Q13](#s15) | success | ["quickbooks__vendor_performance"] | 0 / {} | [] | [] | 342 | 2.018 |
| [S16/Q14](#s16) | success | ["quickbooks__cashflow_forecast"] | 0 / {} | [] | [] | 18 | 0.454 |
| [S17/Q15](#s17) | success | ["quickbooks__cashflow_forecast"] | 0 / {} | [] | [] | 6 | 0.41 |
| [S18/Q16](#s18) | success | ["quickbooks__vendor_performance"] | 0 / {} | [] | ["SUM(avg_monthly_spend)", "SUM(avg_transaction_size)", "AVG(avg_monthly_spend)"] | 1 | 0.879 |
| [S19/Q17](#s19) | success | ["quickbooks__general_ledger", "quickbooks__vendor_performance"] | 0 / {} | [] | ["SUM(CASE WHEN amount < 0 THEN amount ELSE 0 END)", "SUM(CASE WHEN amount < 0 AND vendor_id IN (SELECT vendor_id FROM quickbooks__vendor_performance WHERE annual_spend_growth_pct < 0 AND overall_performance_score >= 7) THEN amount ELSE 0 END)", "SUM(CASE WHEN amount > 0 THEN amount ELSE 0 END)", "SUM(CASE WHEN amount < 0 THEN amount ELSE 0 END)", "SUM(CASE WHEN amount < 0 AND vendor_id IN (SELECT vendor_id FROM quickbooks__vendor_performance WHERE annual_spend_growth_pct < 0 AND overall_performance_score >= 7) THEN amount ELSE 0 END)"] | 1 | 35.087 |
| [S20/Q18](#s20) | success | ["quickbooks__general_ledger"] | 0 / {} | ["account_type"] | ["SUM(amount)", "SUM(CASE WHEN amount < 0 THEN amount ELSE 0 END)", "SUM(CASE WHEN amount > 0 THEN amount ELSE 0 END)"] | 4 | 37.99 |
| [S21/Q19](#s21) | success | ["quickbooks__general_ledger", "quickbooks__vendor_performance"] | 0 / {} | ["account_type"] | ["COUNT(*)", "SUM(amount)", "SUM(CASE WHEN amount < 0 THEN amount ELSE 0 END)", "SUM(CASE WHEN amount > 0 THEN amount ELSE 0 END)"] | 4 | 27.697 |
| [S22/Q20](#s22) | success | ["quickbooks__vendor_performance"] | 0 / {} | [] | ["COUNT(*)", "SUM(avg_monthly_spend)", "SUM(CASE WHEN annual_spend_growth_pct < 0 AND overall_performance_score >= 7 THEN avg_monthly_spend ELSE 0 END)", "SUM(total_lifetime_spend)", "SUM(CASE WHEN annual_spend_growth_pct < 0 AND overall_performance_score >= 7 THEN total_lifetime_spend ELSE 0 END)"] | 1 | 1.181 |
| [S23/Q21](#s23) | success | ["quickbooks__cashflow_forecast"] | 0 / {} | [] | ["AVG(forecasted_outflows)", "AVG(forecasted_inflows)", "AVG(forecasted_net_cash_flow)", "SUM(forecasted_outflows)", "SUM(forecasted_inflows)", "SUM(forecasted_net_cash_flow)"] | 1 | 0.408 |
| [S24/Q22](#s24) | failed | ["quickbooks__general_ledger", "quickbooks__vendor_performance"] | 2 / {'CROSS': 1} | [] | ["SUM(CASE WHEN annual_spend_growth_pct < 0 AND overall_performance_score >= 7 THEN avg_monthly_spend ELSE 0 END)", "SUM(CASE WHEN amount < 0 AND vendor_id IN (SELECT vendor_id FROM quickbooks__vendor_performance WHERE annual_spend_growth_pct < 0 AND overall_performance_score >= 7) THEN amount ELSE 0 END)", "SUM(avg_monthly_spend)", "SUM(CASE WHEN amount < 0 THEN amount ELSE 0 END)"] | unknown | 未取得；调用总时长 0.209 ms |
| [S25/Q23](#s25) | success | ["quickbooks__general_ledger", "quickbooks__vendor_performance"] | 0 / {} | [] | ["SUM(CASE WHEN amount < 0 THEN amount ELSE 0 END)", "SUM(CASE WHEN amount < 0 THEN amount ELSE 0 END)"] | 1 | 34.444 |
| [S26/Q24](#s26) | success | ["quickbooks__vendor_performance"] | 0 / {} | [] | ["SUM(avg_monthly_spend)", "SUM(avg_monthly_spend)"] | 1 | 1.246 |
| [S27/Q25](#s27) | success | ["quickbooks__cashflow_forecast"] | 2 / {'CROSS': 1} | [] | [] | 18 | 0.648 |
| [S28/Q26](#s28) | success | ["quickbooks__cashflow_forecast"] | 2 / {'CROSS': 1} | [] | ["SUM(forecasted_outflows)", "SUM(adjusted_outflow)", "SUM(vendor_reduction)", "AVG(baseline_lri)", "AVG(adjusted_lri)", "SUM(forecasted_outflows)", "SUM(forecasted_inflows)", "SUM(forecasted_outflows)", "SUM(forecasted_inflows)", "SUM(adjusted_outflow)", "AVG(baseline_lri)", "AVG(adjusted_lri)", "SUM(vendor_reduction)"] | 1 | 0.541 |
| [S29/Q27](#s29) | success | ["quickbooks__vendor_performance"] | 0 / {} | [] | [] | 342 | 1.675 |
| [S30/Q28](#s30) | success | ["quickbooks__vendor_performance"] | 0 / {} | [] | [] | 3 | 0.333 |
| [S31/Q29](#s31) | success | ["quickbooks__vendor_performance"] | 0 / {} | [] | [] | 342 | 1.544 |
| [S32/Q30](#s32) | success | ["quickbooks__general_ledger", "quickbooks__vendor_performance"] | 0 / {} | ["vendor_id", "account_type", "account_type"] | ["SUM(CASE WHEN transaction_date >= '2024-10-15' THEN amount ELSE 0 END)", "SUM(CASE WHEN transaction_date < '2024-10-15' THEN amount ELSE 0 END)", "COUNT(*)", "COUNT(DISTINCT transaction_date)", "SUM(CASE WHEN transaction_date < '2024-10-15' THEN amount ELSE 0 END)", "SUM(CASE WHEN transaction_date < '2024-10-15' THEN amount ELSE 0 END)", "SUM(CASE WHEN transaction_date >= '2024-10-15' THEN amount ELSE 0 END)", "SUM(CASE WHEN transaction_date < '2024-10-15' THEN amount ELSE 0 END)", "AVG(spend_change_rate_pct)", "AVG(tx_frequency_density)", "SUM(spend_last12)", "SUM(spend_prior12)"] | 4 | 35.965 |
| [S33/Q31](#s33) | success | ["quickbooks__cashflow_forecast"] | 2 / {'CROSS': 1} | [] | [] | 18 | 0.385 |
| [S34/Q32](#s34) | failed | ["quickbooks__general_ledger", "quickbooks__vendor_performance"] | 0 / {} | ["vendor_id", "account_type", "account_type"] | ["SUM(ABS(amount))", "SUM(ABS(CASE WHEN transaction_date < '2024-10-15' THEN amount ELSE 0 END))", "COUNT(*)", "COUNT(DISTINCT transaction_date)", "SUM(ABS(CASE WHEN transaction_date < '2024-10-15' THEN amount ELSE 0 END))", "SUM(CASE WHEN transaction_date < '2024-10-15' THEN ABS(amount) ELSE 0 END)", "SUM(CASE WHEN transaction_date >= '2024-10-15' THEN ABS(amount) ELSE 0 END)", "SUM(CASE WHEN transaction_date < '2024-10-15' THEN ABS(amount) ELSE 0 END)", "COUNT(*)", "AVG(spend_change_rate_pct)", "PERCENTILE_CONT(spend_change_rate_pct, 0.5)", "MIN(spend_change_rate_pct)", "MAX(spend_change_rate_pct)", "AVG(tx_frequency_density)", "PERCENTILE_CONT(tx_frequency_density, 0.5)", "SUM(spend_last12)", "SUM(spend_prior12)"] | unknown | 未取得；调用总时长 0.262 ms |


## 元数据和设置

| SQL | 类别 | 状态 | 内容 |
| --- | --- | --- | --- |
| S1 | connection_setup | success | PRAGMA query_only=ON |
| S2 | metadata | success | SELECT name,sql FROM sqlite_master WHERE type='table' ORDER BY name |


## Python 与执行位置

人工源码审查：**database_first_violation**。这是服务错误停止前的部分轨迹。SQL 已做供应商筛选与主要预测调整，Python 仍求和终身支出、月支出及预测流出，并计算风险指数均值差；这些可在 SQL 完成。绘图单独保留。 [证据](../reviews/dacomp-091.json)。

P1：Creating visualizations for the report: vendor metrics distribution, account-type spend change rates, and cash flow impact model. These require matplotlib which is unavailable in SQL.

[源码](../../../runs/dsv4flash-db-first-full-01/dacomp-091/attempt-01/python/P1.py)；[输出](../../../runs/dsv4flash-db-first-full-01/dacomp-091/attempt-01/python/P1.stdout)；[错误](../../../runs/dsv4flash-db-first-full-01/dacomp-091/attempt-01/python/P1.stderr)。检出需人工核验的 SQL 可实现操作：.query(；不能仅凭理由判为合规。

P2：Testing the db.frame helper to load query results into a pandas DataFrame for visualization; needed because db.rows returns positional rows.

[源码](../../../runs/dsv4flash-db-first-full-01/dacomp-091/attempt-01/python/P2.py)；[输出](../../../runs/dsv4flash-db-first-full-01/dacomp-091/attempt-01/python/P2.stdout)；[错误](../../../runs/dsv4flash-db-first-full-01/dacomp-091/attempt-01/python/P2.stderr)。检出需人工核验的 SQL 可实现操作：.query(；不能仅凭理由判为合规。

P3：Compute all derived metrics and create the three report figures (vendor metrics, account-type spend analysis, cash flow impact model) using matplotlib/pandas; the visualization and statistics aggregation beyond simple SQL GROUP BY require Python.

[源码](../../../runs/dsv4flash-db-first-full-01/dacomp-091/attempt-01/python/P3.py)；[输出](../../../runs/dsv4flash-db-first-full-01/dacomp-091/attempt-01/python/P3.stdout)；[错误](../../../runs/dsv4flash-db-first-full-01/dacomp-091/attempt-01/python/P3.stderr)。检出需人工核验的 SQL 可实现操作：.query(；不能仅凭理由判为合规。

## 优化机会

已验证候选。筛选限于精确 SQL、相同自包含 CTE、相同单表完整过滤、可分解单表聚合；未覆盖任意 Join 等价和一般谓词蕴含。全部候选都是 offline，未测在线预测。

| 候选 | 类型 | 已有结果 | 覆盖 SQL | 后续次数 | 中间行数 | 验证 | 成本 |
| --- | --- | --- | --- | --- | --- | --- | --- |
| C1 | aggregate MV | False | ["S3", "S22"] | 1 | 1 | verified | Not benchmarked; correctness alone does not establish net speedup. |
| C2 | aggregate MV | False | ["S4", "S20"] | 1 | 4 | verified | Not benchmarked; correctness alone does not establish net speedup. |
| C3 | aggregate MV | False | ["S5", "S23"] | 1 | unknown | not_verified_cap | Not tested |
| C4 | common filtered view | False | ["S6", "S7", "S8", "S15", "S18", "S29", "S30", "S31"] | 7 | 342 | verified | Not benchmarked; correctness alone does not establish net speedup. |
| C5 | aggregate MV | False | ["S7", "S18"] | 1 | unknown | not_verified_cap | Not tested |


已验证覆盖（含触发查询、候选并集去重）：12/30 条成功数据 SQL。正确性仅针对当前数据库快照；未测性能的候选不能声称已加速。

[完整 build/rewrite 与比较证据](dacomp-091.analysis.json)。

### C4：common filtered view

Same single source and complete filter; original filter retained.

原查询 [S6](#s6), [S7](#s7), [S8](#s8), [S15](#s15), [S18](#s18), [S29](#s29), [S30](#s30), [S31](#s31) → 新增共享状态 C4 → 后续 7 次可复用。该构建点为事后假设，不代表 Agent 当时预知后续。

构建定义：

```sql
SELECT * FROM "quickbooks__vendor_performance" WHERE annual_spend_growth_pct < 0 AND overall_performance_score >= 7
```

受益查询 S6 的改写示例：

```sql
SELECT vendor_id, vendor_name, vendor_company_name, vendor_display_name, total_lifetime_spend, annual_spend_growth_pct, overall_performance_score, spend_volatility, payment_completion_rate, business_value_score FROM temp.reuse_candidate AS quickbooks__vendor_performance WHERE annual_spend_growth_pct < 0 AND overall_performance_score >= 7 ORDER BY annual_spend_growth_pct
```

| 原 SQL | 列名一致 | 结果一致 | 比较方法 |
| --- | --- | --- | --- |
| S6 | True | True | ordered_numeric_tolerance |
| S7 | True | True | exact_multiset |
| S8 | True | True | exact_multiset |
| S15 | True | True | ordered_numeric_tolerance |
| S18 | True | True | exact_multiset |
| S29 | True | True | exact_multiset |
| S30 | True | True | exact_multiset |
| S31 | True | True | exact_multiset |


验证状态：verified；成本结论：Not benchmarked; correctness alone does not establish net speedup.

### C1：aggregate MV

Union of grouping keys; decomposable aggregate states; AVG uses SUM and non-NULL COUNT.

原查询 [S3](#s3), [S22](#s22) → 新增共享状态 C1 → 后续 1 次可复用。该构建点为事后假设，不代表 Agent 当时预知后续。

构建定义：

```sql
SELECT COUNT(*) AS __a0, SUM(avg_monthly_spend) AS __a1, SUM(CASE WHEN annual_spend_growth_pct < 0 AND overall_performance_score >= 7 THEN avg_monthly_spend ELSE 0 END) AS __a2, SUM(total_lifetime_spend) AS __a3, SUM(CASE WHEN annual_spend_growth_pct < 0 AND overall_performance_score >= 7 THEN total_lifetime_spend ELSE 0 END) AS __a4 FROM "quickbooks__vendor_performance" 
```

受益查询 S3 的改写示例：

```sql
SELECT SUM(__a0) AS n FROM temp.reuse_candidate
```

| 原 SQL | 列名一致 | 结果一致 | 比较方法 |
| --- | --- | --- | --- |
| S3 | True | True | exact_multiset |
| S22 | True | True | exact_multiset |


验证状态：verified；成本结论：Not benchmarked; correctness alone does not establish net speedup.

### C2：aggregate MV

Union of grouping keys; decomposable aggregate states; AVG uses SUM and non-NULL COUNT.

原查询 [S4](#s4), [S20](#s20) → 新增共享状态 C2 → 后续 1 次可复用。该构建点为事后假设，不代表 Agent 当时预知后续。

构建定义：

```sql
SELECT account_type AS __g0, COUNT(*) AS __a0, SUM(amount) AS __a1, SUM(CASE WHEN amount < 0 THEN amount ELSE 0 END) AS __a2, SUM(CASE WHEN amount > 0 THEN amount ELSE 0 END) AS __a3 FROM "quickbooks__general_ledger"  GROUP BY account_type
```

受益查询 S4 的改写示例：

```sql
SELECT SUM(__a0) AS n FROM temp.reuse_candidate
```

| 原 SQL | 列名一致 | 结果一致 | 比较方法 |
| --- | --- | --- | --- |
| S4 | True | True | exact_multiset |
| S20 | True | True | ordered_numeric_tolerance |


验证状态：verified；成本结论：Not benchmarked; correctness alone does not establish net speedup.

结果依赖：自动记录 SQL→Python 的接口父调用，以及源码中引用归档文件的消费者；字面值相同不认定因果。模型方向选择需要人工读取消息，尚未做全面因果标注。

[统一消息](../../../runs/dsv4flash-db-first-full-01/dacomp-091/attempt-01/messages.jsonl)；[原始 OpenCode 事件](../../../runs/dsv4flash-db-first-full-01/dacomp-091/attempt-01/opencode.jsonl)；[SQL 引擎日志](../../../runs/dsv4flash-db-first-full-01/dacomp-091/attempt-01/sql_journal.jsonl)。

## S1

类别 `connection_setup`；来源 `connection`；调用 `f8e9d733b917452f8ca489c433549866`；状态 `success`。

```sql
PRAGMA query_only=ON
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-091/attempt-01/sql/S1.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-091/attempt-01/sql/S1.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-091/attempt-01/results/S1.rows.jsonl)；完整：True；SHA256：`e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`。

## S2

类别 `metadata`；来源 `list_db`；调用 `f8e9d733b917452f8ca489c433549866`；状态 `success`。

```sql
SELECT name,sql FROM sqlite_master WHERE type='table' ORDER BY name
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-091/attempt-01/sql/S2.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-091/attempt-01/sql/S2.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-091/attempt-01/results/S2.rows.jsonl)；完整：True；SHA256：`dafa2dbf884329b8ebce24d9cd1840d9506372b0849975bed0864725295c9eae`。

## S3

类别 `data`；来源 `query_db`；调用 `c26640a8779245df8c2cd0ce04042816`；状态 `success`。

```sql
SELECT COUNT(*) AS n FROM quickbooks__vendor_performance
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-091/attempt-01/sql/S3.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-091/attempt-01/sql/S3.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-091/attempt-01/results/S3.rows.jsonl)；完整：True；SHA256：`de22f07b11c4d8d8591e63996161f58a895e6fb3b4697e6d2d3e26511fadbb73`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "quickbooks__vendor_performance", "kind": "base", "block": null, "base_tables": ["quickbooks__vendor_performance"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |


## S4

类别 `data`；来源 `query_db`；调用 `1db8340366d74ef8bb8c1dc4ae7f87fb`；状态 `success`。

```sql
SELECT COUNT(*) AS n FROM quickbooks__general_ledger
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-091/attempt-01/sql/S4.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-091/attempt-01/sql/S4.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-091/attempt-01/results/S4.rows.jsonl)；完整：True；SHA256：`6c82b23f59aaeaba283ca9e2c48d9fdba626ddb8c4e9364e80be7455c56cd5d1`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "quickbooks__general_ledger", "kind": "base", "block": null, "base_tables": ["quickbooks__general_ledger"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |


## S5

类别 `data`；来源 `query_db`；调用 `60f39372f99b471698939aa4fc15b204`；状态 `success`。

```sql
SELECT COUNT(*) AS n, MIN(forecast_month) AS min_m, MAX(forecast_month) AS max_m FROM quickbooks__cashflow_forecast
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-091/attempt-01/sql/S5.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-091/attempt-01/sql/S5.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-091/attempt-01/results/S5.rows.jsonl)；完整：True；SHA256：`65494d78d285bc46edaa42643361744a79b163353e00d58cdfd6c8727f784d2c`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "quickbooks__cashflow_forecast", "kind": "base", "block": null, "base_tables": ["quickbooks__cashflow_forecast"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |
| B1 | MIN(forecast_month) | [{"table": "quickbooks__cashflow_forecast", "column": "forecast_month"}] | [] | False |
| B1 | MAX(forecast_month) | [{"table": "quickbooks__cashflow_forecast", "column": "forecast_month"}] | [] | False |


## S6

类别 `data`；来源 `query_db`；调用 `468ef8f8e28849b78709563a88423366`；状态 `success`。

```sql
SELECT vendor_id, vendor_name, vendor_company_name, vendor_display_name, total_lifetime_spend, annual_spend_growth_pct, overall_performance_score, spend_volatility, payment_completion_rate, business_value_score
FROM quickbooks__vendor_performance
WHERE annual_spend_growth_pct < 0 AND overall_performance_score >= 7
ORDER BY annual_spend_growth_pct
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-091/attempt-01/sql/S6.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-091/attempt-01/sql/S6.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-091/attempt-01/results/S6.rows.jsonl)；完整：True；SHA256：`051f01614c00e8ed5f5f9b13c7fcc07f69bb03cac0424dfbe93946ce1e34e14a`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "quickbooks__vendor_performance", "kind": "base", "block": null, "base_tables": ["quickbooks__vendor_performance"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |


## S7

类别 `data`；来源 `query_db`；调用 `64ee1948732e458bab90d31781b3c5e8`；状态 `success`。

```sql
SELECT
  COUNT(*) AS n_vendors,
  ROUND(AVG(spend_volatility / NULLIF(total_lifetime_spend,0)),6) AS avg_spend_vol_coef,
  ROUND(MIN(spend_volatility / NULLIF(total_lifetime_spend,0)),6) AS min_spend_vol_coef,
  ROUND(MAX(spend_volatility / NULLIF(total_lifetime_spend,0)),6) AS max_spend_vol_coef,
  ROUND(AVG(payment_completion_rate*0.4 + business_value_score/10.0*0.6),6) AS avg_composite_risk,
  ROUND(MIN(payment_completion_rate*0.4 + business_value_score/10.0*0.6),6) AS min_composite_risk,
  ROUND(MAX(payment_completion_rate*0.4 + business_value_score/10.0*0.6),6) AS max_composite_risk,
  ROUND(SUM(total_lifetime_spend),2) AS total_lifetime_spend_sum,
  ROUND(SUM(spend_volatility),2) AS total_spend_volatility,
  ROUND(SUM(total_outstanding),2) AS total_outstanding
FROM quickbooks__vendor_performance
WHERE annual_spend_growth_pct < 0 AND overall_performance_score >= 7
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-091/attempt-01/sql/S7.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-091/attempt-01/sql/S7.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-091/attempt-01/results/S7.rows.jsonl)；完整：True；SHA256：`897715a509e9cb9ec961a735bb13d39f102d8ccb09b8779e7220d6562a1fd626`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "quickbooks__vendor_performance", "kind": "base", "block": null, "base_tables": ["quickbooks__vendor_performance"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |
| B1 | AVG(spend_volatility / NULLIF(total_lifetime_spend, 0)) | [{"table": "quickbooks__vendor_performance", "column": "spend_volatility"}, {"table": "quickbooks__vendor_performance", "column": "total_lifetime_spend"}] | [] | False |
| B1 | MIN(spend_volatility / NULLIF(total_lifetime_spend, 0)) | [{"table": "quickbooks__vendor_performance", "column": "spend_volatility"}, {"table": "quickbooks__vendor_performance", "column": "total_lifetime_spend"}] | [] | False |
| B1 | MAX(spend_volatility / NULLIF(total_lifetime_spend, 0)) | [{"table": "quickbooks__vendor_performance", "column": "spend_volatility"}, {"table": "quickbooks__vendor_performance", "column": "total_lifetime_spend"}] | [] | False |
| B1 | AVG(payment_completion_rate * 0.4 + business_value_score / 10.0 * 0.6) | [{"table": "quickbooks__vendor_performance", "column": "payment_completion_rate"}, {"table": "quickbooks__vendor_performance", "column": "business_value_score"}] | [] | False |
| B1 | MIN(payment_completion_rate * 0.4 + business_value_score / 10.0 * 0.6) | [{"table": "quickbooks__vendor_performance", "column": "payment_completion_rate"}, {"table": "quickbooks__vendor_performance", "column": "business_value_score"}] | [] | False |
| B1 | MAX(payment_completion_rate * 0.4 + business_value_score / 10.0 * 0.6) | [{"table": "quickbooks__vendor_performance", "column": "payment_completion_rate"}, {"table": "quickbooks__vendor_performance", "column": "business_value_score"}] | [] | False |
| B1 | SUM(total_lifetime_spend) | [{"table": "quickbooks__vendor_performance", "column": "total_lifetime_spend"}] | [] | False |
| B1 | SUM(spend_volatility) | [{"table": "quickbooks__vendor_performance", "column": "spend_volatility"}] | [] | False |
| B1 | SUM(total_outstanding) | [{"table": "quickbooks__vendor_performance", "column": "total_outstanding"}] | [] | False |


## S8

类别 `data`；来源 `query_db`；调用 `4893c7574f404a1d9f993693ce653766`；状态 `success`。

```sql
SELECT annual_spend_growth_pct, overall_performance_score, spend_volatility, total_lifetime_spend, payment_completion_rate, business_value_score
FROM quickbooks__vendor_performance
WHERE annual_spend_growth_pct < 0 AND overall_performance_score >= 7
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-091/attempt-01/sql/S8.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-091/attempt-01/sql/S8.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-091/attempt-01/results/S8.rows.jsonl)；完整：True；SHA256：`02f75434f376266f1fa533261b909a78e10a53e932cdf45c69942a8e51411443`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "quickbooks__vendor_performance", "kind": "base", "block": null, "base_tables": ["quickbooks__vendor_performance"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |


## S9

类别 `data`；来源 `query_db`；调用 `a3f612e38cb841719b797965113c4f63`；状态 `success`。

```sql
SELECT MIN(transaction_date) AS min_date, MAX(transaction_date) AS max_date,
  COUNT(DISTINCT transaction_date) AS n_dates,
  COUNT(DISTINCT account_type) AS n_account_types
FROM quickbooks__general_ledger
WHERE vendor_id IN (SELECT vendor_id FROM quickbooks__vendor_performance WHERE annual_spend_growth_pct < 0 AND overall_performance_score >= 7)
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-091/attempt-01/sql/S9.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-091/attempt-01/sql/S9.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-091/attempt-01/results/S9.rows.jsonl)；完整：True；SHA256：`b39bb4ae35c07c937504db9722972009c3acca17c4025828cd90a7c5ff7717cf`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "quickbooks__vendor_performance", "kind": "base", "block": null, "base_tables": ["quickbooks__vendor_performance"]}] | [] | [] |
| B2 | [{"alias": "quickbooks__general_ledger", "kind": "base", "block": null, "base_tables": ["quickbooks__general_ledger"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B2 | MIN(transaction_date) | [{"table": "quickbooks__general_ledger", "column": "transaction_date"}] | [] | False |
| B2 | MAX(transaction_date) | [{"table": "quickbooks__general_ledger", "column": "transaction_date"}] | [] | False |
| B2 | COUNT(DISTINCT transaction_date) | [{"table": "quickbooks__general_ledger", "column": "transaction_date"}] | [] | False |
| B2 | COUNT(DISTINCT account_type) | [{"table": "quickbooks__general_ledger", "column": "account_type"}] | [] | False |


未解析列血缘：[{"block": "B2", "column": "annual_spend_growth_pct", "reason": "ambiguous_or_missing_source"}, {"block": "B2", "column": "overall_performance_score", "reason": "ambiguous_or_missing_source"}]

## S10

类别 `data`；来源 `query_db`；调用 `6daf9888405c4ac5b29eac85be0e3cc7`；状态 `success`。

```sql
SELECT account_type, COUNT(*) AS n_tx, ROUND(SUM(amount),2) AS total_amt, MIN(transaction_date) AS min_d, MAX(transaction_date) AS max_d
FROM quickbooks__general_ledger
WHERE vendor_id IN (SELECT vendor_id FROM quickbooks__vendor_performance WHERE annual_spend_growth_pct < 0 AND overall_performance_score >= 7)
GROUP BY account_type
ORDER BY total_amt DESC
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-091/attempt-01/sql/S10.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-091/attempt-01/sql/S10.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-091/attempt-01/results/S10.rows.jsonl)；完整：True；SHA256：`25aec37acf3c95bc6b5f5b5e73b86fa29335363796bb3bea7feb51e72ae26934`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "quickbooks__vendor_performance", "kind": "base", "block": null, "base_tables": ["quickbooks__vendor_performance"]}] | [] | [] |
| B2 | [{"alias": "quickbooks__general_ledger", "kind": "base", "block": null, "base_tables": ["quickbooks__general_ledger"]}] | [] | ["account_type"] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B2 | COUNT(*) | [] | [] | True |
| B2 | MIN(transaction_date) | [{"table": "quickbooks__general_ledger", "column": "transaction_date"}] | [] | False |
| B2 | MAX(transaction_date) | [{"table": "quickbooks__general_ledger", "column": "transaction_date"}] | [] | False |
| B2 | SUM(amount) | [{"table": "quickbooks__general_ledger", "column": "amount"}] | [] | False |


未解析列血缘：[{"block": "B2", "column": "annual_spend_growth_pct", "reason": "ambiguous_or_missing_source"}, {"block": "B2", "column": "overall_performance_score", "reason": "ambiguous_or_missing_source"}]

## S11

类别 `data`；来源 `query_db`；调用 `151cf752b21047e4a619f27fdec255f4`；状态 `success`。

```sql
SELECT COUNT(DISTINCT vendor_id) AS vendors_with_gl FROM quickbooks__general_ledger
WHERE vendor_id IN (SELECT vendor_id FROM quickbooks__vendor_performance WHERE annual_spend_growth_pct < 0 AND overall_performance_score >= 7)
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-091/attempt-01/sql/S11.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-091/attempt-01/sql/S11.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-091/attempt-01/results/S11.rows.jsonl)；完整：True；SHA256：`25e589b97fd5838c45891ad685c9729748a85db8f893020e3b90271cb6ce740f`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "quickbooks__vendor_performance", "kind": "base", "block": null, "base_tables": ["quickbooks__vendor_performance"]}] | [] | [] |
| B2 | [{"alias": "quickbooks__general_ledger", "kind": "base", "block": null, "base_tables": ["quickbooks__general_ledger"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B2 | COUNT(DISTINCT vendor_id) | [{"table": "quickbooks__general_ledger", "column": "vendor_id"}] | [] | False |


未解析列血缘：[{"block": "B2", "column": "annual_spend_growth_pct", "reason": "ambiguous_or_missing_source"}, {"block": "B2", "column": "overall_performance_score", "reason": "ambiguous_or_missing_source"}]

## S12

类别 `data`；来源 `query_db`；调用 `025b9dd0cc214fb2927df8e39f33ee2b`；状态 `success`。

```sql
SELECT vendor_id, account_type,
  ROUND(SUM(CASE WHEN transaction_date >= '2024-10-15' THEN amount ELSE 0 END),2) AS spend_last12,
  ROUND(SUM(CASE WHEN transaction_date < '2024-10-15' THEN amount ELSE 0 END),2) AS spend_prior12,
  COUNT(*) AS n_tx,
  COUNT(DISTINCT transaction_date) AS n_active_days
FROM quickbooks__general_ledger
WHERE vendor_id IN (SELECT vendor_id FROM quickbooks__vendor_performance WHERE annual_spend_growth_pct < 0 AND overall_performance_score >= 7)
GROUP BY vendor_id, account_type
ORDER BY vendor_id, account_type
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-091/attempt-01/sql/S12.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-091/attempt-01/sql/S12.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-091/attempt-01/results/S12.rows.jsonl)；完整：True；SHA256：`82115ea2945952daae34896eb3d4056b739849137fd89a7baa76072bf16a3700`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "quickbooks__vendor_performance", "kind": "base", "block": null, "base_tables": ["quickbooks__vendor_performance"]}] | [] | [] |
| B2 | [{"alias": "quickbooks__general_ledger", "kind": "base", "block": null, "base_tables": ["quickbooks__general_ledger"]}] | [] | ["vendor_id", "account_type"] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B2 | COUNT(*) | [] | [] | True |
| B2 | COUNT(DISTINCT transaction_date) | [{"table": "quickbooks__general_ledger", "column": "transaction_date"}] | [] | False |
| B2 | SUM(CASE WHEN transaction_date >= '2024-10-15' THEN amount ELSE 0 END) | [{"table": "quickbooks__general_ledger", "column": "amount"}] | [{"table": "quickbooks__general_ledger", "column": "transaction_date"}] | False |
| B2 | SUM(CASE WHEN transaction_date < '2024-10-15' THEN amount ELSE 0 END) | [{"table": "quickbooks__general_ledger", "column": "amount"}] | [{"table": "quickbooks__general_ledger", "column": "transaction_date"}] | False |


未解析列血缘：[{"block": "B2", "column": "annual_spend_growth_pct", "reason": "ambiguous_or_missing_source"}, {"block": "B2", "column": "overall_performance_score", "reason": "ambiguous_or_missing_source"}]

## S13

类别 `data`；来源 `query_db`；调用 `59687f5b2d424b6fbeb54f071393f0ea`；状态 `success`。

```sql
SELECT
  vendor_id,
  account_type,
  ROUND(spend_last12,2) AS spend_last12,
  ROUND(spend_prior12,2) AS spend_prior12,
  ROUND(CASE WHEN ABS(spend_prior12) > 0 THEN (spend_last12 - spend_prior12) / ABS(spend_prior12) * 100 ELSE NULL END, 4) AS spend_change_rate_pct,
  n_tx,
  n_active_days,
  ROUND(n_tx * 1.0 / NULLIF(n_active_days, 0), 4) AS tx_frequency_density
FROM (
  SELECT vendor_id, account_type,
    SUM(CASE WHEN transaction_date >= '2024-10-15' THEN amount ELSE 0 END) AS spend_last12,
    SUM(CASE WHEN transaction_date < '2024-10-15' THEN amount ELSE 0 END) AS spend_prior12,
    COUNT(*) AS n_tx,
    COUNT(DISTINCT transaction_date) AS n_active_days
  FROM quickbooks__general_ledger
  WHERE vendor_id IN (SELECT vendor_id FROM quickbooks__vendor_performance WHERE annual_spend_growth_pct < 0 AND overall_performance_score >= 7)
  GROUP BY vendor_id, account_type
) t
ORDER BY vendor_id, account_type
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-091/attempt-01/sql/S13.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-091/attempt-01/sql/S13.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-091/attempt-01/results/S13.rows.jsonl)；完整：True；SHA256：`4c65b3a7da39c27fc8e7a12597960e50c4e066573499f6fd4191b983fc8f54b7`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "quickbooks__vendor_performance", "kind": "base", "block": null, "base_tables": ["quickbooks__vendor_performance"]}] | [] | [] |
| B2 | [{"alias": "quickbooks__general_ledger", "kind": "base", "block": null, "base_tables": ["quickbooks__general_ledger"]}] | [] | ["vendor_id", "account_type"] |
| B3 | [{"alias": "t", "kind": "derived", "block": "B2", "base_tables": ["quickbooks__general_ledger"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B2 | SUM(CASE WHEN transaction_date >= '2024-10-15' THEN amount ELSE 0 END) | [{"table": "quickbooks__general_ledger", "column": "amount"}] | [{"table": "quickbooks__general_ledger", "column": "transaction_date"}] | False |
| B2 | SUM(CASE WHEN transaction_date < '2024-10-15' THEN amount ELSE 0 END) | [{"table": "quickbooks__general_ledger", "column": "amount"}] | [{"table": "quickbooks__general_ledger", "column": "transaction_date"}] | False |
| B2 | COUNT(*) | [] | [] | True |
| B2 | COUNT(DISTINCT transaction_date) | [{"table": "quickbooks__general_ledger", "column": "transaction_date"}] | [] | False |


未解析列血缘：[{"block": "B3", "column": "annual_spend_growth_pct", "reason": "ambiguous_or_missing_source"}, {"block": "B3", "column": "overall_performance_score", "reason": "ambiguous_or_missing_source"}]

## S14

类别 `data`；来源 `query_db`；调用 `6f356f7c35fe4dabba451bc4f77e1613`；状态 `success`。

```sql
SELECT
  account_type,
  COUNT(*) AS n_pairs,
  ROUND(AVG(spend_change_rate_pct),4) AS avg_change_rate_pct,
  ROUND(MIN(spend_change_rate_pct),4) AS min_change_rate_pct,
  ROUND(MAX(spend_change_rate_pct),4) AS max_change_rate_pct,
  ROUND(AVG(tx_frequency_density),4) AS avg_tx_freq_density,
  ROUND(SUM(spend_last12),2) AS total_spend_last12,
  ROUND(SUM(spend_prior12),2) AS total_spend_prior12
FROM (
  SELECT vendor_id, account_type,
    SUM(CASE WHEN transaction_date >= '2024-10-15' THEN amount ELSE 0 END) AS spend_last12,
    SUM(CASE WHEN transaction_date < '2024-10-15' THEN amount ELSE 0 END) AS spend_prior12,
    ROUND(CASE WHEN ABS(SUM(CASE WHEN transaction_date < '2024-10-15' THEN amount ELSE 0 END)) > 0
      THEN (SUM(CASE WHEN transaction_date >= '2024-10-15' THEN amount ELSE 0 END) - SUM(CASE WHEN transaction_date < '2024-10-15' THEN amount ELSE 0 END))
           / ABS(SUM(CASE WHEN transaction_date < '2024-10-15' THEN amount ELSE 0 END)) * 100
      ELSE NULL END, 4) AS spend_change_rate_pct,
    COUNT(*) * 1.0 / NULLIF(COUNT(DISTINCT transaction_date), 0) AS tx_frequency_density
  FROM quickbooks__general_ledger
  WHERE vendor_id IN (SELECT vendor_id FROM quickbooks__vendor_performance WHERE annual_spend_growth_pct < 0 AND overall_performance_score >= 7)
  GROUP BY vendor_id, account_type
) t
GROUP BY account_type
ORDER BY account_type
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-091/attempt-01/sql/S14.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-091/attempt-01/sql/S14.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-091/attempt-01/results/S14.rows.jsonl)；完整：True；SHA256：`c2cf684ea70a381fe6730c64acce17a1f2d38bd9c945b33626c9ad665782a789`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "quickbooks__vendor_performance", "kind": "base", "block": null, "base_tables": ["quickbooks__vendor_performance"]}] | [] | [] |
| B2 | [{"alias": "quickbooks__general_ledger", "kind": "base", "block": null, "base_tables": ["quickbooks__general_ledger"]}] | [] | ["vendor_id", "account_type"] |
| B3 | [{"alias": "t", "kind": "derived", "block": "B2", "base_tables": ["quickbooks__general_ledger"]}] | [] | ["account_type"] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B2 | SUM(CASE WHEN transaction_date >= '2024-10-15' THEN amount ELSE 0 END) | [{"table": "quickbooks__general_ledger", "column": "amount"}] | [{"table": "quickbooks__general_ledger", "column": "transaction_date"}] | False |
| B2 | SUM(CASE WHEN transaction_date < '2024-10-15' THEN amount ELSE 0 END) | [{"table": "quickbooks__general_ledger", "column": "amount"}] | [{"table": "quickbooks__general_ledger", "column": "transaction_date"}] | False |
| B2 | COUNT(*) | [] | [] | True |
| B2 | COUNT(DISTINCT transaction_date) | [{"table": "quickbooks__general_ledger", "column": "transaction_date"}] | [] | False |
| B2 | SUM(CASE WHEN transaction_date < '2024-10-15' THEN amount ELSE 0 END) | [{"table": "quickbooks__general_ledger", "column": "amount"}] | [{"table": "quickbooks__general_ledger", "column": "transaction_date"}] | False |
| B2 | SUM(CASE WHEN transaction_date < '2024-10-15' THEN amount ELSE 0 END) | [{"table": "quickbooks__general_ledger", "column": "amount"}] | [{"table": "quickbooks__general_ledger", "column": "transaction_date"}] | False |
| B2 | SUM(CASE WHEN transaction_date >= '2024-10-15' THEN amount ELSE 0 END) | [{"table": "quickbooks__general_ledger", "column": "amount"}] | [{"table": "quickbooks__general_ledger", "column": "transaction_date"}] | False |
| B2 | SUM(CASE WHEN transaction_date < '2024-10-15' THEN amount ELSE 0 END) | [{"table": "quickbooks__general_ledger", "column": "amount"}] | [{"table": "quickbooks__general_ledger", "column": "transaction_date"}] | False |
| B3 | COUNT(*) | [] | [] | True |
| B3 | AVG(spend_change_rate_pct) | [{"table": "quickbooks__general_ledger", "column": "amount"}, {"table": "quickbooks__general_ledger", "column": "transaction_date"}, {"table": "quickbooks__general_ledger", "column": "amount"}, {"table": "quickbooks__general_ledger", "column": "amount"}, {"table": "quickbooks__general_ledger", "column": "amount"}, {"table": "quickbooks__general_ledger", "column": "transaction_date"}, {"table": "quickbooks__general_ledger", "column": "transaction_date"}, {"table": "quickbooks__general_ledger", "column": "transaction_date"}] | [] | False |
| B3 | MIN(spend_change_rate_pct) | [{"table": "quickbooks__general_ledger", "column": "amount"}, {"table": "quickbooks__general_ledger", "column": "transaction_date"}, {"table": "quickbooks__general_ledger", "column": "amount"}, {"table": "quickbooks__general_ledger", "column": "amount"}, {"table": "quickbooks__general_ledger", "column": "amount"}, {"table": "quickbooks__general_ledger", "column": "transaction_date"}, {"table": "quickbooks__general_ledger", "column": "transaction_date"}, {"table": "quickbooks__general_ledger", "column": "transaction_date"}] | [] | False |
| B3 | MAX(spend_change_rate_pct) | [{"table": "quickbooks__general_ledger", "column": "amount"}, {"table": "quickbooks__general_ledger", "column": "transaction_date"}, {"table": "quickbooks__general_ledger", "column": "amount"}, {"table": "quickbooks__general_ledger", "column": "amount"}, {"table": "quickbooks__general_ledger", "column": "amount"}, {"table": "quickbooks__general_ledger", "column": "transaction_date"}, {"table": "quickbooks__general_ledger", "column": "transaction_date"}, {"table": "quickbooks__general_ledger", "column": "transaction_date"}] | [] | False |
| B3 | AVG(tx_frequency_density) | [{"table": "quickbooks__general_ledger", "column": "transaction_date"}] | [] | False |
| B3 | SUM(spend_last12) | [{"table": "quickbooks__general_ledger", "column": "amount"}, {"table": "quickbooks__general_ledger", "column": "transaction_date"}] | [] | False |
| B3 | SUM(spend_prior12) | [{"table": "quickbooks__general_ledger", "column": "amount"}, {"table": "quickbooks__general_ledger", "column": "transaction_date"}] | [] | False |


未解析列血缘：[{"block": "B3", "column": "annual_spend_growth_pct", "reason": "ambiguous_or_missing_source"}, {"block": "B3", "column": "overall_performance_score", "reason": "ambiguous_or_missing_source"}]

## S15

类别 `data`；来源 `query_db`；调用 `d71192655b684e7e8b1cf3e770edeed6`；状态 `success`。

```sql
SELECT vendor_id,
  ROUND(spend_volatility / NULLIF(total_lifetime_spend,0), 6) AS spend_vol_coef,
  ROUND(payment_completion_rate*0.4 + business_value_score/10.0*0.6, 6) AS composite_risk_score,
  annual_spend_growth_pct, overall_performance_score, total_lifetime_spend,
  ROUND(spend_current_year,2) AS spend_current_year, ROUND(spend_prev_year,2) AS spend_prev_year
FROM quickbooks__vendor_performance
WHERE annual_spend_growth_pct < 0 AND overall_performance_score >= 7
ORDER BY composite_risk_score DESC
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-091/attempt-01/sql/S15.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-091/attempt-01/sql/S15.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-091/attempt-01/results/S15.rows.jsonl)；完整：True；SHA256：`e7bd47e8288d00aba5e3ecb0a68efbb895924f6d631ab9c6363254cb9bab2cb2`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "quickbooks__vendor_performance", "kind": "base", "block": null, "base_tables": ["quickbooks__vendor_performance"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |


## S16

类别 `data`；来源 `query_db`；调用 `fe40a9a5d8334e8baf0a71a464d0576b`；状态 `success`。

```sql
SELECT * FROM quickbooks__cashflow_forecast ORDER BY forecast_month
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-091/attempt-01/sql/S16.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-091/attempt-01/sql/S16.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-091/attempt-01/results/S16.rows.jsonl)；完整：True；SHA256：`2056d70bd057e3ce4be8754685384262b2625efc4dd89ad7a42e4cc431d23533`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "quickbooks__cashflow_forecast", "kind": "base", "block": null, "base_tables": ["quickbooks__cashflow_forecast"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |


## S17

类别 `data`；来源 `query_db`；调用 `cce3cc6093034865a2f1b5b03719f0f6`；状态 `success`。

```sql
SELECT * FROM quickbooks__cashflow_forecast ORDER BY forecast_month LIMIT 18 OFFSET 12
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-091/attempt-01/sql/S17.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-091/attempt-01/sql/S17.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-091/attempt-01/results/S17.rows.jsonl)；完整：True；SHA256：`e25fdddac81d4c7216cade772d08fd92145d476daee397ff0ca4261495b926bd`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "quickbooks__cashflow_forecast", "kind": "base", "block": null, "base_tables": ["quickbooks__cashflow_forecast"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |


## S18

类别 `data`；来源 `query_db`；调用 `c1a36b06026043788dc4e8085a6f5cf6`；状态 `success`。

```sql
SELECT
  ROUND(SUM(avg_monthly_spend),2) AS sum_avg_monthly_spend_selected,
  ROUND(SUM(avg_transaction_size),2) AS sum_avg_tx_size,
  ROUND(AVG(avg_monthly_spend),2) AS avg_monthly_spend_per_vendor
FROM quickbooks__vendor_performance
WHERE annual_spend_growth_pct < 0 AND overall_performance_score >= 7
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-091/attempt-01/sql/S18.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-091/attempt-01/sql/S18.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-091/attempt-01/results/S18.rows.jsonl)；完整：True；SHA256：`0615cd1afce78f389aab5ff46d00d5d4e4c71c67d848bc89bdcb128766a517e5`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "quickbooks__vendor_performance", "kind": "base", "block": null, "base_tables": ["quickbooks__vendor_performance"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | SUM(avg_monthly_spend) | [{"table": "quickbooks__vendor_performance", "column": "avg_monthly_spend"}] | [] | False |
| B1 | SUM(avg_transaction_size) | [{"table": "quickbooks__vendor_performance", "column": "avg_transaction_size"}] | [] | False |
| B1 | AVG(avg_monthly_spend) | [{"table": "quickbooks__vendor_performance", "column": "avg_monthly_spend"}] | [] | False |


## S19

类别 `data`；来源 `query_db`；调用 `bdf7f113c4d7431889058e74346b9ab8`；状态 `success`。

```sql
SELECT
  ROUND(SUM(CASE WHEN amount < 0 THEN amount ELSE 0 END),2) AS total_outflow_all,
  ROUND(SUM(CASE WHEN amount < 0 THEN amount ELSE 0 END)/24.0,2) AS avg_monthly_outflow_all_gl,
  ROUND(SUM(CASE WHEN amount < 0 AND vendor_id IN (SELECT vendor_id FROM quickbooks__vendor_performance WHERE annual_spend_growth_pct < 0 AND overall_performance_score >= 7) THEN amount ELSE 0 END),2) AS total_outflow_selected,
  ROUND(SUM(CASE WHEN amount < 0 AND vendor_id IN (SELECT vendor_id FROM quickbooks__vendor_performance WHERE annual_spend_growth_pct < 0 AND overall_performance_score >= 7) THEN amount ELSE 0 END)/24.0,2) AS avg_monthly_outflow_selected_gl,
  ROUND(SUM(CASE WHEN amount > 0 THEN amount ELSE 0 END),2) AS total_inflow_all
FROM quickbooks__general_ledger
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-091/attempt-01/sql/S19.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-091/attempt-01/sql/S19.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-091/attempt-01/results/S19.rows.jsonl)；完整：True；SHA256：`dbd78dd0f12a121fa06bb277a46f2e8c46f586bfe931e09208b0289266175357`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "quickbooks__vendor_performance", "kind": "base", "block": null, "base_tables": ["quickbooks__vendor_performance"]}] | [] | [] |
| B2 | [{"alias": "quickbooks__vendor_performance", "kind": "base", "block": null, "base_tables": ["quickbooks__vendor_performance"]}] | [] | [] |
| B3 | [{"alias": "quickbooks__general_ledger", "kind": "base", "block": null, "base_tables": ["quickbooks__general_ledger"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B3 | SUM(CASE WHEN amount < 0 THEN amount ELSE 0 END) | [{"table": "quickbooks__general_ledger", "column": "amount"}] | [{"table": "quickbooks__general_ledger", "column": "amount"}] | False |
| B3 | SUM(CASE WHEN amount < 0 AND vendor_id IN (SELECT vendor_id FROM quickbooks__vendor_performance WHERE annual_spend_growth_pct < 0 AND overall_performance_score >= 7) THEN amount ELSE 0 END) | [{"table": "quickbooks__general_ledger", "column": "amount"}] | [{"table": "quickbooks__general_ledger", "column": "amount"}, {"table": "quickbooks__general_ledger", "column": "vendor_id"}, {"table": "quickbooks__vendor_performance", "column": "vendor_id"}, {"table": "quickbooks__vendor_performance", "column": "annual_spend_growth_pct"}, {"table": "quickbooks__vendor_performance", "column": "overall_performance_score"}] | False |
| B3 | SUM(CASE WHEN amount > 0 THEN amount ELSE 0 END) | [{"table": "quickbooks__general_ledger", "column": "amount"}] | [{"table": "quickbooks__general_ledger", "column": "amount"}] | False |
| B3 | SUM(CASE WHEN amount < 0 THEN amount ELSE 0 END) | [{"table": "quickbooks__general_ledger", "column": "amount"}] | [{"table": "quickbooks__general_ledger", "column": "amount"}] | False |
| B3 | SUM(CASE WHEN amount < 0 AND vendor_id IN (SELECT vendor_id FROM quickbooks__vendor_performance WHERE annual_spend_growth_pct < 0 AND overall_performance_score >= 7) THEN amount ELSE 0 END) | [{"table": "quickbooks__general_ledger", "column": "amount"}] | [{"table": "quickbooks__general_ledger", "column": "amount"}, {"table": "quickbooks__general_ledger", "column": "vendor_id"}, {"table": "quickbooks__vendor_performance", "column": "vendor_id"}, {"table": "quickbooks__vendor_performance", "column": "annual_spend_growth_pct"}, {"table": "quickbooks__vendor_performance", "column": "overall_performance_score"}] | False |


未解析列血缘：[{"block": "B3", "column": "annual_spend_growth_pct", "reason": "ambiguous_or_missing_source"}, {"block": "B3", "column": "overall_performance_score", "reason": "ambiguous_or_missing_source"}, {"block": "B3", "column": "annual_spend_growth_pct", "reason": "ambiguous_or_missing_source"}, {"block": "B3", "column": "overall_performance_score", "reason": "ambiguous_or_missing_source"}]

## S20

类别 `data`；来源 `query_db`；调用 `401ce431cd534a16bed50c93260d813c`；状态 `success`。

```sql
SELECT account_type,
  ROUND(SUM(amount),2) AS total_all,
  ROUND(SUM(CASE WHEN amount<0 THEN amount ELSE 0 END),2) AS outflow_all,
  ROUND(SUM(CASE WHEN amount>0 THEN amount ELSE 0 END),2) AS inflow_all
FROM quickbooks__general_ledger
GROUP BY account_type ORDER BY account_type
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-091/attempt-01/sql/S20.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-091/attempt-01/sql/S20.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-091/attempt-01/results/S20.rows.jsonl)；完整：True；SHA256：`6498dde182073077e234f5520a74de742cb16995f354b867d1765a5dd187fca8`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "quickbooks__general_ledger", "kind": "base", "block": null, "base_tables": ["quickbooks__general_ledger"]}] | [] | ["account_type"] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | SUM(amount) | [{"table": "quickbooks__general_ledger", "column": "amount"}] | [] | False |
| B1 | SUM(CASE WHEN amount < 0 THEN amount ELSE 0 END) | [{"table": "quickbooks__general_ledger", "column": "amount"}] | [{"table": "quickbooks__general_ledger", "column": "amount"}] | False |
| B1 | SUM(CASE WHEN amount > 0 THEN amount ELSE 0 END) | [{"table": "quickbooks__general_ledger", "column": "amount"}] | [{"table": "quickbooks__general_ledger", "column": "amount"}] | False |


## S21

类别 `data`；来源 `query_db`；调用 `2e07195e7d5f4d4fa6582c952da3e25c`；状态 `success`。

```sql
SELECT account_type,
  ROUND(SUM(amount),2) AS total_selected,
  ROUND(SUM(CASE WHEN amount<0 THEN amount ELSE 0 END),2) AS outflow_selected,
  ROUND(SUM(CASE WHEN amount>0 THEN amount ELSE 0 END),2) AS inflow_selected,
  COUNT(*) AS n_tx
FROM quickbooks__general_ledger
WHERE vendor_id IN (SELECT vendor_id FROM quickbooks__vendor_performance WHERE annual_spend_growth_pct < 0 AND overall_performance_score >= 7)
GROUP BY account_type ORDER BY account_type
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-091/attempt-01/sql/S21.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-091/attempt-01/sql/S21.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-091/attempt-01/results/S21.rows.jsonl)；完整：True；SHA256：`6008a785df03ce38f44f4f8663a154c633e683726339fbd9a58f341a742e5efd`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "quickbooks__vendor_performance", "kind": "base", "block": null, "base_tables": ["quickbooks__vendor_performance"]}] | [] | [] |
| B2 | [{"alias": "quickbooks__general_ledger", "kind": "base", "block": null, "base_tables": ["quickbooks__general_ledger"]}] | [] | ["account_type"] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B2 | COUNT(*) | [] | [] | True |
| B2 | SUM(amount) | [{"table": "quickbooks__general_ledger", "column": "amount"}] | [] | False |
| B2 | SUM(CASE WHEN amount < 0 THEN amount ELSE 0 END) | [{"table": "quickbooks__general_ledger", "column": "amount"}] | [{"table": "quickbooks__general_ledger", "column": "amount"}] | False |
| B2 | SUM(CASE WHEN amount > 0 THEN amount ELSE 0 END) | [{"table": "quickbooks__general_ledger", "column": "amount"}] | [{"table": "quickbooks__general_ledger", "column": "amount"}] | False |


未解析列血缘：[{"block": "B2", "column": "annual_spend_growth_pct", "reason": "ambiguous_or_missing_source"}, {"block": "B2", "column": "overall_performance_score", "reason": "ambiguous_or_missing_source"}]

## S22

类别 `data`；来源 `query_db`；调用 `54383d67132c49839c6f78daf47c36e3`；状态 `success`。

```sql
SELECT
  ROUND(SUM(avg_monthly_spend),2) AS all_vendor_monthly_spend,
  ROUND(SUM(CASE WHEN annual_spend_growth_pct < 0 AND overall_performance_score >= 7 THEN avg_monthly_spend ELSE 0 END),2) AS selected_vendor_monthly_spend,
  ROUND(SUM(total_lifetime_spend),2) AS all_lifetime_spend,
  ROUND(SUM(CASE WHEN annual_spend_growth_pct < 0 AND overall_performance_score >= 7 THEN total_lifetime_spend ELSE 0 END),2) AS selected_lifetime_spend,
  COUNT(*) AS n_all
FROM quickbooks__vendor_performance
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-091/attempt-01/sql/S22.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-091/attempt-01/sql/S22.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-091/attempt-01/results/S22.rows.jsonl)；完整：True；SHA256：`dc1a71959b2577e8e2a03687f4df4ce6f12ea41ba3d8b5d9ef87ea3d35b0ff8a`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "quickbooks__vendor_performance", "kind": "base", "block": null, "base_tables": ["quickbooks__vendor_performance"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |
| B1 | SUM(avg_monthly_spend) | [{"table": "quickbooks__vendor_performance", "column": "avg_monthly_spend"}] | [] | False |
| B1 | SUM(CASE WHEN annual_spend_growth_pct < 0 AND overall_performance_score >= 7 THEN avg_monthly_spend ELSE 0 END) | [{"table": "quickbooks__vendor_performance", "column": "avg_monthly_spend"}] | [{"table": "quickbooks__vendor_performance", "column": "annual_spend_growth_pct"}, {"table": "quickbooks__vendor_performance", "column": "overall_performance_score"}] | False |
| B1 | SUM(total_lifetime_spend) | [{"table": "quickbooks__vendor_performance", "column": "total_lifetime_spend"}] | [] | False |
| B1 | SUM(CASE WHEN annual_spend_growth_pct < 0 AND overall_performance_score >= 7 THEN total_lifetime_spend ELSE 0 END) | [{"table": "quickbooks__vendor_performance", "column": "total_lifetime_spend"}] | [{"table": "quickbooks__vendor_performance", "column": "annual_spend_growth_pct"}, {"table": "quickbooks__vendor_performance", "column": "overall_performance_score"}] | False |


## S23

类别 `data`；来源 `query_db`；调用 `b2fb3eb508294010b703734435b0e83d`；状态 `success`。

```sql
SELECT
  ROUND(AVG(forecasted_outflows),2) AS avg_fc_outflow,
  ROUND(AVG(forecasted_inflows),2) AS avg_fc_inflow,
  ROUND(AVG(forecasted_net_cash_flow),2) AS avg_fc_net,
  ROUND(SUM(forecasted_outflows),2) AS sum_fc_outflow,
  ROUND(SUM(forecasted_inflows),2) AS sum_fc_inflow,
  ROUND(SUM(forecasted_net_cash_flow),2) AS sum_fc_net
FROM quickbooks__cashflow_forecast
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-091/attempt-01/sql/S23.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-091/attempt-01/sql/S23.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-091/attempt-01/results/S23.rows.jsonl)；完整：True；SHA256：`c909be853a018cf1c9a3b68f3c6bbd09db6afa95f66114e21b1a5eb47e768137`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "quickbooks__cashflow_forecast", "kind": "base", "block": null, "base_tables": ["quickbooks__cashflow_forecast"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | AVG(forecasted_outflows) | [{"table": "quickbooks__cashflow_forecast", "column": "forecasted_outflows"}] | [] | False |
| B1 | AVG(forecasted_inflows) | [{"table": "quickbooks__cashflow_forecast", "column": "forecasted_inflows"}] | [] | False |
| B1 | AVG(forecasted_net_cash_flow) | [{"table": "quickbooks__cashflow_forecast", "column": "forecasted_net_cash_flow"}] | [] | False |
| B1 | SUM(forecasted_outflows) | [{"table": "quickbooks__cashflow_forecast", "column": "forecasted_outflows"}] | [] | False |
| B1 | SUM(forecasted_inflows) | [{"table": "quickbooks__cashflow_forecast", "column": "forecasted_inflows"}] | [] | False |
| B1 | SUM(forecasted_net_cash_flow) | [{"table": "quickbooks__cashflow_forecast", "column": "forecasted_net_cash_flow"}] | [] | False |


## S24

类别 `data`；来源 `query_db`；调用 `568152f2b74544ce92c23b05d12532ac`；状态 `failed`。

```sql
SELECT
  -- GL-based outflow share
  ROUND(ABS(SUM(CASE WHEN amount < 0 AND vendor_id IN (SELECT vendor_id FROM quickbooks__vendor_performance WHERE annual_spend_growth_pct < 0 AND overall_performance_score >= 7) THEN amount ELSE 0 END))
   / NULLIF(ABS(SUM(CASE WHEN amount < 0 THEN amount ELSE 0 END)), 0) * 100, 2) AS gl_outflow_share_pct,
  -- Vendor performance based spend share
  ROUND(SUM(CASE WHEN annual_spend_growth_pct < 0 AND overall_performance_score >= 7 THEN avg_monthly_spend ELSE 0 END)
   / NULLIF(SUM(avg_monthly_spend), 0) * 100, 2) AS vp_spend_share_pct
FROM quickbooks__general_ledger, quickbooks__vendor_performance
LIMIT 1
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-091/attempt-01/sql/S24.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-091/attempt-01/sql/S24.parameters.json)。

错误：`OperationalError('ambiguous column name: vendor_id')`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "quickbooks__vendor_performance", "kind": "base", "block": null, "base_tables": ["quickbooks__vendor_performance"]}] | [] | [] |
| B2 | [{"alias": "quickbooks__general_ledger", "kind": "base", "block": null, "base_tables": ["quickbooks__general_ledger"]}, {"alias": "quickbooks__vendor_performance", "kind": "base", "block": null, "base_tables": ["quickbooks__vendor_performance"]}] | [{"type": "CROSS", "right": "quickbooks__vendor_performance", "on": null, "using": []}] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B2 | SUM(CASE WHEN annual_spend_growth_pct < 0 AND overall_performance_score >= 7 THEN avg_monthly_spend ELSE 0 END) | [{"table": "quickbooks__vendor_performance", "column": "avg_monthly_spend"}] | [{"table": "quickbooks__vendor_performance", "column": "annual_spend_growth_pct"}, {"table": "quickbooks__vendor_performance", "column": "overall_performance_score"}] | False |
| B2 | SUM(CASE WHEN amount < 0 AND vendor_id IN (SELECT vendor_id FROM quickbooks__vendor_performance WHERE annual_spend_growth_pct < 0 AND overall_performance_score >= 7) THEN amount ELSE 0 END) | [{"table": "quickbooks__general_ledger", "column": "amount"}] | [{"table": "quickbooks__general_ledger", "column": "amount"}, {"unknown": "vendor_id"}, {"table": "quickbooks__vendor_performance", "column": "vendor_id"}, {"table": "quickbooks__vendor_performance", "column": "annual_spend_growth_pct"}, {"table": "quickbooks__vendor_performance", "column": "overall_performance_score"}] | False |
| B2 | SUM(avg_monthly_spend) | [{"table": "quickbooks__vendor_performance", "column": "avg_monthly_spend"}] | [] | False |
| B2 | SUM(CASE WHEN amount < 0 THEN amount ELSE 0 END) | [{"table": "quickbooks__general_ledger", "column": "amount"}] | [{"table": "quickbooks__general_ledger", "column": "amount"}] | False |


未解析列血缘：[{"block": "B2", "column": "vendor_id", "reason": "ambiguous_or_missing_source"}, {"block": "B2", "column": "vendor_id", "reason": "ambiguous_or_missing_source"}, {"block": "B2", "column": "vendor_id", "reason": "ambiguous_or_missing_source"}, {"block": "B2", "column": "vendor_id", "reason": "ambiguous_or_missing_source"}]

## S25

类别 `data`；来源 `query_db`；调用 `bb2b54dd6dd94afa9fac1329e7961bb7`；状态 `success`。

```sql
SELECT
  ROUND(100.0 * (
    SELECT ABS(SUM(CASE WHEN amount < 0 THEN amount ELSE 0 END)) FROM quickbooks__general_ledger
    WHERE vendor_id IN (SELECT vendor_id FROM quickbooks__vendor_performance WHERE annual_spend_growth_pct < 0 AND overall_performance_score >= 7)
  ) / NULLIF(ABS(SUM(CASE WHEN amount < 0 THEN amount ELSE 0 END)), 0), 2) AS gl_outflow_share_pct
FROM quickbooks__general_ledger
LIMIT 1
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-091/attempt-01/sql/S25.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-091/attempt-01/sql/S25.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-091/attempt-01/results/S25.rows.jsonl)；完整：True；SHA256：`519c476e6d061e5a6d127a27623a88d74ae89ee650b0067e4565021eb9ad68d9`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "quickbooks__vendor_performance", "kind": "base", "block": null, "base_tables": ["quickbooks__vendor_performance"]}] | [] | [] |
| B2 | [{"alias": "quickbooks__general_ledger", "kind": "base", "block": null, "base_tables": ["quickbooks__general_ledger"]}] | [] | [] |
| B3 | [{"alias": "quickbooks__general_ledger", "kind": "base", "block": null, "base_tables": ["quickbooks__general_ledger"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B2 | SUM(CASE WHEN amount < 0 THEN amount ELSE 0 END) | [{"table": "quickbooks__general_ledger", "column": "amount"}] | [{"table": "quickbooks__general_ledger", "column": "amount"}] | False |
| B3 | SUM(CASE WHEN amount < 0 THEN amount ELSE 0 END) | [{"table": "quickbooks__general_ledger", "column": "amount"}] | [{"table": "quickbooks__general_ledger", "column": "amount"}] | False |


未解析列血缘：[{"block": "B3", "column": "annual_spend_growth_pct", "reason": "ambiguous_or_missing_source"}, {"block": "B3", "column": "overall_performance_score", "reason": "ambiguous_or_missing_source"}, {"block": "B3", "column": "annual_spend_growth_pct", "reason": "ambiguous_or_missing_source"}, {"block": "B3", "column": "overall_performance_score", "reason": "ambiguous_or_missing_source"}]

## S26

类别 `data`；来源 `query_db`；调用 `5cd5aed8d2ef4aafa59936f43792fc2b`；状态 `success`。

```sql
SELECT
  ROUND(100.0 * (
    SELECT SUM(avg_monthly_spend) FROM quickbooks__vendor_performance
    WHERE annual_spend_growth_pct < 0 AND overall_performance_score >= 7
  ) / NULLIF(SUM(avg_monthly_spend), 0), 2) AS vp_spend_share_pct
FROM quickbooks__vendor_performance
LIMIT 1
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-091/attempt-01/sql/S26.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-091/attempt-01/sql/S26.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-091/attempt-01/results/S26.rows.jsonl)；完整：True；SHA256：`ce23c766283fde0d0ec05bcf723cc77b154ab1beb06056d534b1e9ac47495393`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "quickbooks__vendor_performance", "kind": "base", "block": null, "base_tables": ["quickbooks__vendor_performance"]}] | [] | [] |
| B2 | [{"alias": "quickbooks__vendor_performance", "kind": "base", "block": null, "base_tables": ["quickbooks__vendor_performance"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | SUM(avg_monthly_spend) | [{"table": "quickbooks__vendor_performance", "column": "avg_monthly_spend"}] | [] | False |
| B2 | SUM(avg_monthly_spend) | [{"table": "quickbooks__vendor_performance", "column": "avg_monthly_spend"}] | [] | False |


## S27

类别 `data`；来源 `query_db`；调用 `5c2d068a7f754bef91251f44087a83dc`；状态 `success`。

```sql
WITH vendor_share AS (
  SELECT 0.2318 AS outflow_share
),
baseline AS (
  SELECT
    forecast_month,
    forecast_year,
    forecast_month_num,
    forecasted_inflows,
    forecasted_outflows,
    forecasted_net_cash_flow,
    cumulative_forecast_cash_flow,
    cash_flow_health_score,
    liquidity_risk_level,
    -- Vendor portion of outflow
    forecasted_outflows * outflow_share AS vendor_outflow,
    -- 30% reduction on vendor portion
    forecasted_outflows * outflow_share * 0.30 AS vendor_reduction,
    -- Adjusted outflow
    forecasted_outflows - forecasted_outflows * outflow_share * 0.30 AS adjusted_outflow,
    -- Adjusted net cash flow
    forecasted_inflows - (forecasted_outflows - forecasted_outflows * outflow_share * 0.30) AS adjusted_net_cash_flow,
    -- Monthly deficit ratio (baseline)
    CASE WHEN forecasted_net_cash_flow < 0 THEN -forecasted_net_cash_flow / NULLIF(forecasted_inflows, 0) ELSE 0 END AS baseline_lri,
    -- Monthly deficit ratio (adjusted)
    CASE WHEN forecasted_inflows - (forecasted_outflows - forecasted_outflows * outflow_share * 0.30) < 0
      THEN -(forecasted_inflows - (forecasted_outflows - forecasted_outflows * outflow_share * 0.30)) / NULLIF(forecasted_inflows, 0)
      ELSE 0 END AS adjusted_lri
  FROM quickbooks__cashflow_forecast, vendor_share
)
SELECT
  forecast_month,
  forecast_year,
  forecast_month_num,
  ROUND(forecasted_inflows,2) AS forecasted_inflows,
  ROUND(forecasted_outflows,2) AS forecasted_outflows,
  ROUND(vendor_outflow,2) AS vendor_outflow,
  ROUND(vendor_reduction,2) AS vendor_reduction_30pct,
  ROUND(adjusted_outflow,2) AS adjusted_outflow,
  ROUND(forecasted_net_cash_flow,2) AS baseline_net,
  ROUND(adjusted_net_cash_flow,2) AS adjusted_net,
  ROUND(baseline_lri,6) AS baseline_lri_monthly,
  ROUND(adjusted_lri,6) AS adjusted_lri_monthly,
  liquidity_risk_level,
  cash_flow_health_score
FROM baseline
ORDER BY forecast_month
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-091/attempt-01/sql/S27.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-091/attempt-01/sql/S27.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-091/attempt-01/results/S27.rows.jsonl)；完整：True；SHA256：`c3b29b4c2a2d7003633f1e04f45c22df30fe062329c1256c76214adc8c9736cf`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [] | [] | [] |
| B2 | [{"alias": "vendor_share", "kind": "derived", "block": "B1", "base_tables": []}, {"alias": "quickbooks__cashflow_forecast", "kind": "base", "block": null, "base_tables": ["quickbooks__cashflow_forecast"]}] | [{"type": "CROSS", "right": "vendor_share", "on": null, "using": []}] | [] |
| B3 | [{"alias": "baseline", "kind": "derived", "block": "B2", "base_tables": ["quickbooks__cashflow_forecast"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |


## S28

类别 `data`；来源 `query_db`；调用 `1cd6a290173c4eacbc7ddf8158c735e0`；状态 `success`。

```sql
WITH vendor_share AS (SELECT 0.2318 AS outflow_share),
m AS (
  SELECT
    forecasted_inflows,
    forecasted_outflows,
    forecasted_net_cash_flow,
    cumulative_forecast_cash_flow,
    forecasted_outflows * outflow_share * 0.30 AS vendor_reduction,
    forecasted_outflows - forecasted_outflows * outflow_share * 0.30 AS adjusted_outflow,
    CASE WHEN forecasted_net_cash_flow < 0 THEN -forecasted_net_cash_flow / NULLIF(forecasted_inflows,0) ELSE 0 END AS baseline_lri,
    CASE WHEN forecasted_inflows - (forecasted_outflows - forecasted_outflows * outflow_share * 0.30) < 0
      THEN -(forecasted_inflows - (forecasted_outflows - forecasted_outflows * outflow_share * 0.30)) / NULLIF(forecasted_inflows,0) ELSE 0 END AS adjusted_lri
  FROM quickbooks__cashflow_forecast, vendor_share
)
SELECT
  ROUND(SUM(forecasted_outflows),2) AS total_baseline_outflow,
  ROUND(SUM(adjusted_outflow),2) AS total_adjusted_outflow,
  ROUND(SUM(vendor_reduction),2) AS total_vendor_reduction,
  ROUND(100.0*SUM(vendor_reduction)/SUM(forecasted_outflows),2) AS pct_outflow_reduction,
  ROUND(SUM(forecasted_inflows) - SUM(forecasted_outflows),2) AS baseline_net_18m,
  ROUND(SUM(forecasted_inflows) - SUM(adjusted_outflow),2) AS adjusted_net_18m,
  ROUND(AVG(baseline_lri),6) AS baseline_lri_avg,
  ROUND(AVG(adjusted_lri),6) AS adjusted_lri_avg,
  ROUND(AVG(baseline_lri)-AVG(adjusted_lri),6) AS lri_change
FROM m
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-091/attempt-01/sql/S28.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-091/attempt-01/sql/S28.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-091/attempt-01/results/S28.rows.jsonl)；完整：True；SHA256：`f37549a89656dcd5cfb9bb2ba0bd9a71042bf8f870b1dbab6bba9dc9895200b3`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [] | [] | [] |
| B2 | [{"alias": "vendor_share", "kind": "derived", "block": "B1", "base_tables": []}, {"alias": "quickbooks__cashflow_forecast", "kind": "base", "block": null, "base_tables": ["quickbooks__cashflow_forecast"]}] | [{"type": "CROSS", "right": "vendor_share", "on": null, "using": []}] | [] |
| B3 | [{"alias": "m", "kind": "derived", "block": "B2", "base_tables": ["quickbooks__cashflow_forecast"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B3 | SUM(forecasted_outflows) | [{"table": "quickbooks__cashflow_forecast", "column": "forecasted_outflows"}] | [] | False |
| B3 | SUM(adjusted_outflow) | [{"table": "quickbooks__cashflow_forecast", "column": "forecasted_outflows"}, {"table": "quickbooks__cashflow_forecast", "column": "forecasted_outflows"}] | [] | False |
| B3 | SUM(vendor_reduction) | [{"table": "quickbooks__cashflow_forecast", "column": "forecasted_outflows"}] | [] | False |
| B3 | AVG(baseline_lri) | [{"table": "quickbooks__cashflow_forecast", "column": "forecasted_net_cash_flow"}, {"table": "quickbooks__cashflow_forecast", "column": "forecasted_net_cash_flow"}, {"table": "quickbooks__cashflow_forecast", "column": "forecasted_inflows"}] | [] | False |
| B3 | AVG(adjusted_lri) | [{"table": "quickbooks__cashflow_forecast", "column": "forecasted_inflows"}, {"table": "quickbooks__cashflow_forecast", "column": "forecasted_inflows"}, {"table": "quickbooks__cashflow_forecast", "column": "forecasted_outflows"}, {"table": "quickbooks__cashflow_forecast", "column": "forecasted_inflows"}, {"table": "quickbooks__cashflow_forecast", "column": "forecasted_outflows"}, {"table": "quickbooks__cashflow_forecast", "column": "forecasted_outflows"}, {"table": "quickbooks__cashflow_forecast", "column": "forecasted_outflows"}] | [] | False |
| B3 | SUM(forecasted_outflows) | [{"table": "quickbooks__cashflow_forecast", "column": "forecasted_outflows"}] | [] | False |
| B3 | SUM(forecasted_inflows) | [{"table": "quickbooks__cashflow_forecast", "column": "forecasted_inflows"}] | [] | False |
| B3 | SUM(forecasted_outflows) | [{"table": "quickbooks__cashflow_forecast", "column": "forecasted_outflows"}] | [] | False |
| B3 | SUM(forecasted_inflows) | [{"table": "quickbooks__cashflow_forecast", "column": "forecasted_inflows"}] | [] | False |
| B3 | SUM(adjusted_outflow) | [{"table": "quickbooks__cashflow_forecast", "column": "forecasted_outflows"}, {"table": "quickbooks__cashflow_forecast", "column": "forecasted_outflows"}] | [] | False |
| B3 | AVG(baseline_lri) | [{"table": "quickbooks__cashflow_forecast", "column": "forecasted_net_cash_flow"}, {"table": "quickbooks__cashflow_forecast", "column": "forecasted_net_cash_flow"}, {"table": "quickbooks__cashflow_forecast", "column": "forecasted_inflows"}] | [] | False |
| B3 | AVG(adjusted_lri) | [{"table": "quickbooks__cashflow_forecast", "column": "forecasted_inflows"}, {"table": "quickbooks__cashflow_forecast", "column": "forecasted_inflows"}, {"table": "quickbooks__cashflow_forecast", "column": "forecasted_outflows"}, {"table": "quickbooks__cashflow_forecast", "column": "forecasted_inflows"}, {"table": "quickbooks__cashflow_forecast", "column": "forecasted_outflows"}, {"table": "quickbooks__cashflow_forecast", "column": "forecasted_outflows"}, {"table": "quickbooks__cashflow_forecast", "column": "forecasted_outflows"}] | [] | False |
| B3 | SUM(vendor_reduction) | [{"table": "quickbooks__cashflow_forecast", "column": "forecasted_outflows"}] | [] | False |


## S29

类别 `data`；来源 `python`；调用 `fd903bce5101464fab693ca04f02f242`；状态 `success`。

```sql
SELECT vendor_id, annual_spend_growth_pct, overall_performance_score, spend_volatility, total_lifetime_spend, payment_completion_rate, business_value_score, avg_monthly_spend, spend_current_year, spend_prev_year, vendor_display_name FROM quickbooks__vendor_performance WHERE annual_spend_growth_pct < 0 AND overall_performance_score >= 7
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-091/attempt-01/sql/S29.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-091/attempt-01/sql/S29.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-091/attempt-01/results/S29.rows.jsonl)；完整：True；SHA256：`525e5b3ff21312a7f22abc7a7b356c4b3ca0ca6e7c091ca96327a551956b7541`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "quickbooks__vendor_performance", "kind": "base", "block": null, "base_tables": ["quickbooks__vendor_performance"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |


## S30

类别 `data`；来源 `python`；调用 `32fb623ad6024029b2b027243df96bc0`；状态 `success`。

```sql
SELECT vendor_id, annual_spend_growth_pct FROM quickbooks__vendor_performance WHERE annual_spend_growth_pct < 0 AND overall_performance_score >= 7 LIMIT 3
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-091/attempt-01/sql/S30.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-091/attempt-01/sql/S30.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-091/attempt-01/results/S30.rows.jsonl)；完整：True；SHA256：`d65c8ff0b03cb003b072c6f85d29ff254d97a22b555e2a86cb07c825ac3d316d`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "quickbooks__vendor_performance", "kind": "base", "block": null, "base_tables": ["quickbooks__vendor_performance"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |


## S31

类别 `data`；来源 `python`；调用 `54072b3c858f4b2eb1484a411bd4f546`；状态 `success`。

```sql

  SELECT vendor_id, vendor_display_name, annual_spend_growth_pct, overall_performance_score,
         spend_volatility, total_lifetime_spend, payment_completion_rate, business_value_score,
         avg_monthly_spend
  FROM quickbooks__vendor_performance
  WHERE annual_spend_growth_pct < 0 AND overall_performance_score >= 7

```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-091/attempt-01/sql/S31.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-091/attempt-01/sql/S31.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-091/attempt-01/results/S31.rows.jsonl)；完整：True；SHA256：`ac4d3b5ee4b29e8a1ff9e859cd05fbd603e8b35310440fd66e2d87a95ed21c4f`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "quickbooks__vendor_performance", "kind": "base", "block": null, "base_tables": ["quickbooks__vendor_performance"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |


## S32

类别 `data`；来源 `python`；调用 `54072b3c858f4b2eb1484a411bd4f546`；状态 `success`。

```sql

  SELECT account_type,
    AVG(spend_change_rate_pct) as avg_change,
    AVG(tx_frequency_density) as avg_freq,
    SUM(spend_last12) as total_last12,
    SUM(spend_prior12) as total_prior12
  FROM (
    SELECT vendor_id, account_type,
      SUM(CASE WHEN transaction_date >= '2024-10-15' THEN amount ELSE 0 END) AS spend_last12,
      SUM(CASE WHEN transaction_date < '2024-10-15' THEN amount ELSE 0 END) AS spend_prior12,
      CASE WHEN ABS(SUM(CASE WHEN transaction_date < '2024-10-15' THEN amount ELSE 0 END)) > 0
        THEN (SUM(CASE WHEN transaction_date >= '2024-10-15' THEN amount ELSE 0 END) - SUM(CASE WHEN transaction_date < '2024-10-15' THEN amount ELSE 0 END))
             / ABS(SUM(CASE WHEN transaction_date < '2024-10-15' THEN amount ELSE 0 END)) * 100
        ELSE NULL END AS spend_change_rate_pct,
      COUNT(*) * 1.0 / NULLIF(COUNT(DISTINCT transaction_date), 0) AS tx_frequency_density
    FROM quickbooks__general_ledger
    WHERE vendor_id IN (SELECT vendor_id FROM quickbooks__vendor_performance WHERE annual_spend_growth_pct < 0 AND overall_performance_score >= 7)
    GROUP BY vendor_id, account_type
  ) t
  GROUP BY account_type
  ORDER BY account_type

```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-091/attempt-01/sql/S32.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-091/attempt-01/sql/S32.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-091/attempt-01/results/S32.rows.jsonl)；完整：True；SHA256：`a9052ba8c6520cf03708c69086d14934030a48a433d55dee7c25099aca5a3ae3`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "quickbooks__vendor_performance", "kind": "base", "block": null, "base_tables": ["quickbooks__vendor_performance"]}] | [] | [] |
| B2 | [{"alias": "quickbooks__general_ledger", "kind": "base", "block": null, "base_tables": ["quickbooks__general_ledger"]}] | [] | ["vendor_id", "account_type"] |
| B3 | [{"alias": "t", "kind": "derived", "block": "B2", "base_tables": ["quickbooks__general_ledger"]}] | [] | ["account_type"] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B2 | SUM(CASE WHEN transaction_date >= '2024-10-15' THEN amount ELSE 0 END) | [{"table": "quickbooks__general_ledger", "column": "amount"}] | [{"table": "quickbooks__general_ledger", "column": "transaction_date"}] | False |
| B2 | SUM(CASE WHEN transaction_date < '2024-10-15' THEN amount ELSE 0 END) | [{"table": "quickbooks__general_ledger", "column": "amount"}] | [{"table": "quickbooks__general_ledger", "column": "transaction_date"}] | False |
| B2 | COUNT(*) | [] | [] | True |
| B2 | COUNT(DISTINCT transaction_date) | [{"table": "quickbooks__general_ledger", "column": "transaction_date"}] | [] | False |
| B2 | SUM(CASE WHEN transaction_date < '2024-10-15' THEN amount ELSE 0 END) | [{"table": "quickbooks__general_ledger", "column": "amount"}] | [{"table": "quickbooks__general_ledger", "column": "transaction_date"}] | False |
| B2 | SUM(CASE WHEN transaction_date < '2024-10-15' THEN amount ELSE 0 END) | [{"table": "quickbooks__general_ledger", "column": "amount"}] | [{"table": "quickbooks__general_ledger", "column": "transaction_date"}] | False |
| B2 | SUM(CASE WHEN transaction_date >= '2024-10-15' THEN amount ELSE 0 END) | [{"table": "quickbooks__general_ledger", "column": "amount"}] | [{"table": "quickbooks__general_ledger", "column": "transaction_date"}] | False |
| B2 | SUM(CASE WHEN transaction_date < '2024-10-15' THEN amount ELSE 0 END) | [{"table": "quickbooks__general_ledger", "column": "amount"}] | [{"table": "quickbooks__general_ledger", "column": "transaction_date"}] | False |
| B3 | AVG(spend_change_rate_pct) | [{"table": "quickbooks__general_ledger", "column": "amount"}, {"table": "quickbooks__general_ledger", "column": "transaction_date"}, {"table": "quickbooks__general_ledger", "column": "amount"}, {"table": "quickbooks__general_ledger", "column": "amount"}, {"table": "quickbooks__general_ledger", "column": "amount"}, {"table": "quickbooks__general_ledger", "column": "transaction_date"}, {"table": "quickbooks__general_ledger", "column": "transaction_date"}, {"table": "quickbooks__general_ledger", "column": "transaction_date"}] | [] | False |
| B3 | AVG(tx_frequency_density) | [{"table": "quickbooks__general_ledger", "column": "transaction_date"}] | [] | False |
| B3 | SUM(spend_last12) | [{"table": "quickbooks__general_ledger", "column": "amount"}, {"table": "quickbooks__general_ledger", "column": "transaction_date"}] | [] | False |
| B3 | SUM(spend_prior12) | [{"table": "quickbooks__general_ledger", "column": "amount"}, {"table": "quickbooks__general_ledger", "column": "transaction_date"}] | [] | False |


未解析列血缘：[{"block": "B3", "column": "annual_spend_growth_pct", "reason": "ambiguous_or_missing_source"}, {"block": "B3", "column": "overall_performance_score", "reason": "ambiguous_or_missing_source"}]

## S33

类别 `data`；来源 `python`；调用 `54072b3c858f4b2eb1484a411bd4f546`；状态 `success`。

```sql

  WITH vendor_share AS (SELECT 0.2318 AS outflow_share)
  SELECT
    forecast_month,
    forecasted_inflows,
    forecasted_outflows,
    forecasted_net_cash_flow,
    cumulative_forecast_cash_flow,
    forecasted_outflows * outflow_share * 0.30 AS vendor_reduction,
    forecasted_outflows - forecasted_outflows * outflow_share * 0.30 AS adjusted_outflow,
    forecasted_inflows - (forecasted_outflows - forecasted_outflows * outflow_share * 0.30) AS adjusted_net,
    cash_flow_health_score,
    liquidity_risk_level
  FROM quickbooks__cashflow_forecast, vendor_share
  ORDER BY forecast_month

```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-091/attempt-01/sql/S33.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-091/attempt-01/sql/S33.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-091/attempt-01/results/S33.rows.jsonl)；完整：True；SHA256：`674867d2d321f19dfa2b5add0368d40667e8203aee5fe85b12da66f292a7f271`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [] | [] | [] |
| B2 | [{"alias": "vendor_share", "kind": "derived", "block": "B1", "base_tables": []}, {"alias": "quickbooks__cashflow_forecast", "kind": "base", "block": null, "base_tables": ["quickbooks__cashflow_forecast"]}] | [{"type": "CROSS", "right": "vendor_share", "on": null, "using": []}] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |


## S34

类别 `data`；来源 `query_db`；调用 `ddc0c88e77384f20af013e7920fa95aa`；状态 `failed`。

```sql
SELECT
  account_type,
  COUNT(*) AS n_pairs,
  ROUND(AVG(spend_change_rate_pct),4) AS avg_change_pct,
  ROUND(MEDIAN(spend_change_rate_pct),4) AS median_change_pct,
  ROUND(MIN(spend_change_rate_pct),4) AS min_change_pct,
  ROUND(MAX(spend_change_rate_pct),4) AS max_change_pct,
  ROUND(AVG(tx_frequency_density),4) AS avg_tx_freq_density,
  ROUND(MEDIAN(tx_frequency_density),4) AS median_tx_freq_density,
  ROUND(SUM(spend_last12),2) AS total_vol_last12,
  ROUND(SUM(spend_prior12),2) AS total_vol_prior12
FROM (
  SELECT vendor_id, account_type,
    SUM(ABS(amount)) AS spend_last12,
    SUM(ABS(CASE WHEN transaction_date < '2024-10-15' THEN amount ELSE 0 END)) AS spend_prior12,
    CASE WHEN SUM(ABS(CASE WHEN transaction_date < '2024-10-15' THEN amount ELSE 0 END)) > 0
      THEN (SUM(CASE WHEN transaction_date >= '2024-10-15' THEN ABS(amount) ELSE 0 END)
           - SUM(CASE WHEN transaction_date < '2024-10-15' THEN ABS(amount) ELSE 0 END))
           / SUM(CASE WHEN transaction_date < '2024-10-15' THEN ABS(amount) ELSE 0 END) * 100
      ELSE NULL END AS spend_change_rate_pct,
    COUNT(*) * 1.0 / NULLIF(COUNT(DISTINCT transaction_date), 0) AS tx_frequency_density
  FROM quickbooks__general_ledger
  WHERE vendor_id IN (SELECT vendor_id FROM quickbooks__vendor_performance WHERE annual_spend_growth_pct < 0 AND overall_performance_score >= 7)
  GROUP BY vendor_id, account_type
) t
GROUP BY account_type
ORDER BY account_type
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-091/attempt-01/sql/S34.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-091/attempt-01/sql/S34.parameters.json)。

错误：`OperationalError('no such function: MEDIAN')`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "quickbooks__vendor_performance", "kind": "base", "block": null, "base_tables": ["quickbooks__vendor_performance"]}] | [] | [] |
| B2 | [{"alias": "quickbooks__general_ledger", "kind": "base", "block": null, "base_tables": ["quickbooks__general_ledger"]}] | [] | ["vendor_id", "account_type"] |
| B3 | [{"alias": "t", "kind": "derived", "block": "B2", "base_tables": ["quickbooks__general_ledger"]}] | [] | ["account_type"] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B2 | SUM(ABS(amount)) | [{"table": "quickbooks__general_ledger", "column": "amount"}] | [] | False |
| B2 | SUM(ABS(CASE WHEN transaction_date < '2024-10-15' THEN amount ELSE 0 END)) | [{"table": "quickbooks__general_ledger", "column": "amount"}] | [{"table": "quickbooks__general_ledger", "column": "transaction_date"}] | False |
| B2 | COUNT(*) | [] | [] | True |
| B2 | COUNT(DISTINCT transaction_date) | [{"table": "quickbooks__general_ledger", "column": "transaction_date"}] | [] | False |
| B2 | SUM(ABS(CASE WHEN transaction_date < '2024-10-15' THEN amount ELSE 0 END)) | [{"table": "quickbooks__general_ledger", "column": "amount"}] | [{"table": "quickbooks__general_ledger", "column": "transaction_date"}] | False |
| B2 | SUM(CASE WHEN transaction_date < '2024-10-15' THEN ABS(amount) ELSE 0 END) | [{"table": "quickbooks__general_ledger", "column": "amount"}] | [{"table": "quickbooks__general_ledger", "column": "transaction_date"}] | False |
| B2 | SUM(CASE WHEN transaction_date >= '2024-10-15' THEN ABS(amount) ELSE 0 END) | [{"table": "quickbooks__general_ledger", "column": "amount"}] | [{"table": "quickbooks__general_ledger", "column": "transaction_date"}] | False |
| B2 | SUM(CASE WHEN transaction_date < '2024-10-15' THEN ABS(amount) ELSE 0 END) | [{"table": "quickbooks__general_ledger", "column": "amount"}] | [{"table": "quickbooks__general_ledger", "column": "transaction_date"}] | False |
| B3 | COUNT(*) | [] | [] | True |
| B3 | AVG(spend_change_rate_pct) | [{"table": "quickbooks__general_ledger", "column": "amount"}, {"table": "quickbooks__general_ledger", "column": "transaction_date"}, {"table": "quickbooks__general_ledger", "column": "transaction_date"}, {"table": "quickbooks__general_ledger", "column": "amount"}, {"table": "quickbooks__general_ledger", "column": "transaction_date"}, {"table": "quickbooks__general_ledger", "column": "amount"}, {"table": "quickbooks__general_ledger", "column": "transaction_date"}, {"table": "quickbooks__general_ledger", "column": "amount"}] | [] | False |
| B3 | PERCENTILE_CONT(spend_change_rate_pct, 0.5) | [{"table": "quickbooks__general_ledger", "column": "amount"}, {"table": "quickbooks__general_ledger", "column": "transaction_date"}, {"table": "quickbooks__general_ledger", "column": "transaction_date"}, {"table": "quickbooks__general_ledger", "column": "amount"}, {"table": "quickbooks__general_ledger", "column": "transaction_date"}, {"table": "quickbooks__general_ledger", "column": "amount"}, {"table": "quickbooks__general_ledger", "column": "transaction_date"}, {"table": "quickbooks__general_ledger", "column": "amount"}] | [] | False |
| B3 | MIN(spend_change_rate_pct) | [{"table": "quickbooks__general_ledger", "column": "amount"}, {"table": "quickbooks__general_ledger", "column": "transaction_date"}, {"table": "quickbooks__general_ledger", "column": "transaction_date"}, {"table": "quickbooks__general_ledger", "column": "amount"}, {"table": "quickbooks__general_ledger", "column": "transaction_date"}, {"table": "quickbooks__general_ledger", "column": "amount"}, {"table": "quickbooks__general_ledger", "column": "transaction_date"}, {"table": "quickbooks__general_ledger", "column": "amount"}] | [] | False |
| B3 | MAX(spend_change_rate_pct) | [{"table": "quickbooks__general_ledger", "column": "amount"}, {"table": "quickbooks__general_ledger", "column": "transaction_date"}, {"table": "quickbooks__general_ledger", "column": "transaction_date"}, {"table": "quickbooks__general_ledger", "column": "amount"}, {"table": "quickbooks__general_ledger", "column": "transaction_date"}, {"table": "quickbooks__general_ledger", "column": "amount"}, {"table": "quickbooks__general_ledger", "column": "transaction_date"}, {"table": "quickbooks__general_ledger", "column": "amount"}] | [] | False |
| B3 | AVG(tx_frequency_density) | [{"table": "quickbooks__general_ledger", "column": "transaction_date"}] | [] | False |
| B3 | PERCENTILE_CONT(tx_frequency_density, 0.5) | [{"table": "quickbooks__general_ledger", "column": "transaction_date"}] | [] | False |
| B3 | SUM(spend_last12) | [{"table": "quickbooks__general_ledger", "column": "amount"}] | [] | False |
| B3 | SUM(spend_prior12) | [{"table": "quickbooks__general_ledger", "column": "amount"}, {"table": "quickbooks__general_ledger", "column": "transaction_date"}] | [] | False |


未解析列血缘：[{"block": "B3", "column": "annual_spend_growth_pct", "reason": "ambiguous_or_missing_source"}, {"block": "B3", "column": "overall_performance_score", "reason": "ambiguous_or_missing_source"}]
