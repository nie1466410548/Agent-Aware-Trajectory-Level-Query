# dacomp-069

### Capital Efficiency Issue for a High-Priority Investment Application  The CFO is concer…

运行：已提交。官方未评分。全部 SQL 尝试/成功 46/45；数据 SQL 44/43；Python 5 次。

完整原题：

### Capital Efficiency Issue for a High-Priority Investment Application

The CFO is concerned about the `com.dev.photoeditor` app. Over the past 12 months, a `$2M` `research_budget_usd` was invested, but the `overall_performance_score` has dropped from 85 to 72. Please analyze the performance divergence of this app across different geographical `regions`, focusing specifically on the differences between top markets where a key revenue metric is over $7 and markets where it is under $3.

| 表 | 行数 | 列数 |
| --- | --- | --- |
| google_play__comprehensive_performance_dashboard | 13807 | 38 |
| google_play__finance_report | 10194 | 20 |
| google_play__geo_market_analysis | 14 | 39 |
| google_play__time_series_trends | 18 | 40 |


实际路线（分析者依据 SQL/源码概括，不代表 Agent 自述）：SQL 提取目标应用的地域和财务记录 → Python 按地区、收入层级汇总 → 高低收入市场比较。

数据库大小：3,796,992 字节。

## 数据 SQL

| SQL | 状态 | 基础表 | Join 输入/类型 | GROUP BY | 聚合表达式 | 结果行数 | 数据库 ms |
| --- | --- | --- | --- | --- | --- | --- | --- |
| [S3/Q1](#s3) | success | ["google_play__comprehensive_performance_dashboard"] | 0 / {} | [] | [] | 1 | 3.312 |
| [S4/Q2](#s4) | success | ["google_play__comprehensive_performance_dashboard"] | 0 / {} | [] | [] | 10 | 2.08 |
| [S5/Q3](#s5) | success | ["google_play__geo_market_analysis"] | 0 / {} | [] | [] | 14 | 0.531 |
| [S6/Q4](#s6) | success | ["google_play__geo_market_analysis"] | 0 / {} | [] | [] | 5 | 0.266 |
| [S7/Q5](#s7) | success | ["google_play__finance_report"] | 0 / {} | [] | [] | 10 | 1.635 |
| [S8/Q6](#s8) | success | ["google_play__time_series_trends"] | 0 / {} | [] | ["MIN(revenue_per_active_device)", "MAX(revenue_per_active_device)", "AVG(revenue_per_active_device)"] | 1 | 0.373 |
| [S9/Q7](#s9) | success | ["google_play__geo_market_analysis"] | 0 / {} | [] | ["MIN(avg_transaction_value)", "MAX(avg_transaction_value)", "MIN(average_revenue_per_user)", "MAX(average_revenue_per_user)"] | 1 | 0.337 |
| [S10/Q8](#s10) | success | ["google_play__time_series_trends"] | 0 / {} | [] | [] | 18 | 0.372 |
| [S11/Q9](#s11) | success | ["google_play__geo_market_analysis"] | 0 / {} | [] | [] | 14 | 0.378 |
| [S12/Q10](#s12) | success | ["google_play__geo_market_analysis"] | 0 / {} | ["package_name"] | ["COUNT(*)"] | 1 | 0.353 |
| [S13/Q11](#s13) | success | ["google_play__finance_report"] | 0 / {} | ["country_short"] | ["COUNT(DISTINCT date_day)", "SUM(net_amount)", "SUM(transactions)", "SUM(net_amount)", "SUM(transactions)"] | 6 | 1.666 |
| [S14/Q12](#s14) | success | ["google_play__finance_report"] | 0 / {} | ["sku_id", "product_title"] | ["COUNT(*)", "MIN(net_amount / transactions)", "MAX(net_amount / transactions)"] | 2 | 1.686 |
| [S15/Q13](#s15) | success | ["google_play__finance_report"] | 0 / {} | [] | [] | 8 | 2.016 |
| [S16/Q14](#s16) | success | ["google_play__comprehensive_performance_dashboard"] | 0 / {} | [] | [] | 12 | 1.945 |
| [S17/Q15](#s17) | success | ["google_play__comprehensive_performance_dashboard"] | 0 / {} | [] | ["COUNT(*)", "COUNT(DISTINCT date_day)", "SUM(research_budget_usd)", "MIN(overall_performance_score)", "MAX(overall_performance_score)"] | 1 | 2.006 |
| [S18/Q16](#s18) | success | ["google_play__finance_report"] | 0 / {} | ["country_short", "sku_id"] | ["COUNT(*)", "SUM(net_amount)", "SUM(transactions)", "SUM(net_amount)", "SUM(transactions)"] | 6 | 1.923 |
| [S19/Q17](#s19) | success | ["google_play__finance_report"] | 0 / {} | [] | [] | 25 | 2.059 |
| [S20/Q18](#s20) | success | ["google_play__geo_market_analysis"] | 0 / {} | [] | [] | 14 | 0.47 |
| [S21/Q19](#s21) | success | ["google_play__finance_report"] | 0 / {} | ["package_name", "sku_id", "product_title"] | ["COUNT(*)", "MIN(net_amount / transactions)", "MAX(net_amount / transactions)"] | 26 | 10.792 |
| [S22/Q20](#s22) | success | ["google_play__finance_report"] | 0 / {} | [] | ["COUNT(*)", "COUNT(DISTINCT country_short)", "COUNT(DISTINCT date_day)", "MIN(date_day)", "MAX(date_day)"] | 1 | 2.128 |
| [S23/Q21](#s23) | success | ["google_play__finance_report"] | 0 / {} | [] | [] | 51 | 1.469 |
| [S24/Q22](#s24) | success | ["google_play__geo_market_analysis"] | 0 / {} | [] | [] | 14 | 0.478 |
| [S25/Q23](#s25) | success | ["google_play__geo_market_analysis"] | 0 / {} | ["region"] | ["COUNT(*)", "SUM(avg_daily_revenue)", "AVG(avg_daily_revenue)", "AVG(average_revenue_per_user)", "AVG(avg_transaction_value)", "AVG(app_quality_score)", "AVG(app_crash_rate_per_1k)", "AVG(day_7_retention_rate)", "AVG(day_30_retention_rate)", "AVG(daily_churn_rate)", "AVG(weekly_growth_rate)", "AVG(overall_market_score)"] | 5 | 0.525 |
| [S26/Q24](#s26) | success | ["google_play__geo_market_analysis"] | 0 / {} | ["CASE WHEN average_revenue_per_user > 7 THEN 'High ARPU (>$7)' ELSE 'Low ARPU (<$7)' END"] | ["COUNT(*)", "SUM(avg_daily_revenue)", "AVG(avg_daily_installs)", "AVG(avg_active_devices)", "AVG(average_revenue_per_user)", "AVG(avg_transaction_value)", "AVG(app_quality_score)", "AVG(app_crash_rate_per_1k)", "AVG(day_7_retention_rate)", "AVG(day_30_retention_rate)", "AVG(daily_churn_rate)", "AVG(weekly_growth_rate)", "AVG(overall_market_score)"] | 2 | 0.595 |
| [S27/Q25](#s27) | success | ["google_play__geo_market_analysis"] | 0 / {} | [] | [] | 14 | 0.441 |
| [S28/Q26](#s28) | success | ["google_play__comprehensive_performance_dashboard"] | 0 / {} | [] | [] | 12 | 2.001 |
| [S29/Q27](#s29) | success | ["google_play__finance_report"] | 0 / {} | [] | [] | 51 | 1.85 |
| [S30/Q28](#s30) | failed | ["google_play__time_series_trends"] | 0 / {} | [] | [] | unknown | 未取得；调用总时长 0.186 ms |
| [S31/Q29](#s31) | success | ["google_play__time_series_trends"] | 0 / {} | [] | [] | 18 | 0.521 |
| [S32/Q30](#s32) | success | ["google_play__finance_report"] | 0 / {} | ["country_short", "sku_id", "STRFTIME('%Y-%m', date_day)", "country_short", "sku_id"] | ["SUM(net_amount)", "SUM(transactions)", "MIN(m2.month)", "MAX(m2.month)", "MIN(month)", "MAX(month)", "SUM(CASE WHEN month = (SELECT MIN(m2.month) FROM monthly AS m2 WHERE m2.country_short = monthly.country_short AND m2.sku_id = monthly.sku_id) THEN net END)", "SUM(CASE WHEN month = (SELECT MAX(m2.month) FROM monthly AS m2 WHERE m2.country_short = monthly.country_short AND m2.sku_id = monthly.sku_id) THEN net END)"] | 6 | 2.566 |
| [S33/Q31](#s33) | success | ["google_play__finance_report"] | 0 / {} | ["country_short", "sku_id"] | ["SUM(new_subscriptions)", "SUM(cancelled_subscriptions)", "SUM(total_active_subscriptions)"] | 6 | 1.617 |
| [S34/Q32](#s34) | success | ["google_play__comprehensive_performance_dashboard"] | 0 / {} | [] | [] | 12 | 2.126 |
| [S35/Q33](#s35) | success | ["google_play__geo_market_analysis"] | 0 / {} | [] | [] | 14 | 0.469 |
| [S36/Q34](#s36) | success | ["google_play__finance_report"] | 0 / {} | [] | [] | 51 | 1.505 |
| [S37/Q35](#s37) | success | ["google_play__time_series_trends"] | 0 / {} | [] | [] | 18 | 0.31 |
| [S38/Q36](#s38) | success | ["google_play__comprehensive_performance_dashboard"] | 0 / {} | [] | [] | 12 | 2.318 |
| [S39/Q37](#s39) | success | ["google_play__geo_market_analysis"] | 0 / {} | [] | [] | 14 | 0.349 |
| [S40/Q38](#s40) | success | ["google_play__finance_report"] | 0 / {} | [] | [] | 51 | 1.584 |
| [S41/Q39](#s41) | success | ["google_play__time_series_trends"] | 0 / {} | [] | [] | 18 | 0.287 |
| [S42/Q40](#s42) | success | ["google_play__geo_market_analysis"] | 0 / {} | [] | [] | 14 | 0.413 |
| [S43/Q41](#s43) | success | ["google_play__geo_market_analysis"] | 0 / {} | [] | [] | 14 | 0.415 |
| [S44/Q42](#s44) | success | ["google_play__geo_market_analysis"] | 0 / {} | [] | [] | 14 | 0.507 |
| [S45/Q43](#s45) | success | ["google_play__comprehensive_performance_dashboard"] | 0 / {} | [] | [] | 12 | 2.322 |
| [S46/Q44](#s46) | success | ["google_play__geo_market_analysis"] | 0 / {} | [] | [] | 14 | 0.329 |


## 元数据和设置

| SQL | 类别 | 状态 | 内容 |
| --- | --- | --- | --- |
| S1 | connection_setup | success | PRAGMA query_only=ON |
| S2 | metadata | success | SELECT name,sql FROM sqlite_master WHERE type='table' ORDER BY name |


## Python 与执行位置

人工源码审查：**database_first_violation**。Python 对国家月份交易、地区和收入等级进行求和与均值，并计算收入份额和正负增长数量，属于可在 SQL 内完成的聚合。相关检验和绘图单独保留。 [证据](../reviews/dacomp-069.json)。

P1：Creating visualizations for the analysis: (1) Dashboard performance score decline over time, (2) Regional ARPU and quality comparison, (3) Finance report revenue trends per country, (4) Geo market quality vs ARPU scatter. These use matplotlib which is not supported in SQLite.

[源码](../../../runs/dsv4flash-db-first-full-01/dacomp-069/attempt-01/python/P1.py)；[输出](../../../runs/dsv4flash-db-first-full-01/dacomp-069/attempt-01/python/P1.stdout)；[错误](../../../runs/dsv4flash-db-first-full-01/dacomp-069/attempt-01/python/P1.stderr)。检出需人工核验的 SQL 可实现操作：groupby(, .query(；不能仅凭理由判为合规。

P2：Re-running visualization generation after fixing a variable name bug in the scatter plot size assignment (sizes[tier]). Matplotlib/statistics are not supported in SQLite so Python is required.

[源码](../../../runs/dsv4flash-db-first-full-01/dacomp-069/attempt-01/python/P2.py)；[输出](../../../runs/dsv4flash-db-first-full-01/dacomp-069/attempt-01/python/P2.stdout)；[错误](../../../runs/dsv4flash-db-first-full-01/dacomp-069/attempt-01/python/P2.stderr)。检出需人工核验的 SQL 可实现操作：groupby(, .query(；不能仅凭理由判为合规。

P3：Computing correlation statistics between revenue metrics and quality metrics across geo markets (Pearson/Spearman correlations) — this is a statistical procedure not supported by SQLite.

[源码](../../../runs/dsv4flash-db-first-full-01/dacomp-069/attempt-01/python/P3.py)；[输出](../../../runs/dsv4flash-db-first-full-01/dacomp-069/attempt-01/python/P3.stdout)；[错误](../../../runs/dsv4flash-db-first-full-01/dacomp-069/attempt-01/python/P3.stderr)。检出需人工核验的 SQL 可实现操作：groupby(, .query(, sort_values(；不能仅凭理由判为合规。

P4：Fixing the column name error (revenue_tier not selected in previous query) and computing the Tier 1 vs Tier 3 comparison. This is a statistical summarization better done in Python/pandas than SQL.

[源码](../../../runs/dsv4flash-db-first-full-01/dacomp-069/attempt-01/python/P4.py)；[输出](../../../runs/dsv4flash-db-first-full-01/dacomp-069/attempt-01/python/P4.stdout)；[错误](../../../runs/dsv4flash-db-first-full-01/dacomp-069/attempt-01/python/P4.stderr)。检出需人工核验的 SQL 可实现操作：groupby(, .query(；不能仅凭理由判为合规。

P5：Computing the final summary statistics for the report: revenue shares by market tier, quality differences, retention/churn deltas, and app-level percentage changes. These derived metrics are computed in Python for clarity in reporting.

[源码](../../../runs/dsv4flash-db-first-full-01/dacomp-069/attempt-01/python/P5.py)；[输出](../../../runs/dsv4flash-db-first-full-01/dacomp-069/attempt-01/python/P5.stdout)；[错误](../../../runs/dsv4flash-db-first-full-01/dacomp-069/attempt-01/python/P5.stderr)。检出需人工核验的 SQL 可实现操作：groupby(, .query(；不能仅凭理由判为合规。

## 优化机会

已验证候选。筛选限于精确 SQL、相同自包含 CTE、相同单表完整过滤、可分解单表聚合；未覆盖任意 Join 等价和一般谓词蕴含。全部候选都是 offline，未测在线预测。

| 候选 | 类型 | 已有结果 | 覆盖 SQL | 后续次数 | 中间行数 | 验证 | 成本 |
| --- | --- | --- | --- | --- | --- | --- | --- |
| C1 | common filtered view | False | ["S4", "S16", "S17", "S28", "S34", "S38", "S45"] | 6 | 12 | verified | Not benchmarked; correctness alone does not establish net speedup. |
| C2 | common filtered view | False | ["S5", "S6", "S9", "S11", "S20", "S24", "S25", "S26", "S27", "S35", "S39", "S42", "S43", "S44", "S46"] | 14 | 14 | verified | Not benchmarked; correctness alone does not establish net speedup. |
| C3 | aggregate MV | False | ["S9", "S25", "S26"] | 2 | unknown | not_verified_cap | Not tested |
| C4 | common filtered view | False | ["S7", "S13", "S14", "S18", "S22", "S23", "S29", "S33", "S36", "S40"] | 9 | 51 | verified | Not benchmarked; correctness alone does not establish net speedup. |
| C5 | aggregate MV | False | ["S14", "S18", "S33"] | 2 | unknown | not_verified_cap | Not tested |
| C6 | common filtered view | False | ["S8", "S10", "S31", "S37", "S41"] | 4 | unknown | not_verified_cap | Not tested |


已验证覆盖（含触发查询、候选并集去重）：32/43 条成功数据 SQL。正确性仅针对当前数据库快照；未测性能的候选不能声称已加速。

[完整 build/rewrite 与比较证据](dacomp-069.analysis.json)。

### C2：common filtered view

Same single source and complete filter; original filter retained.

原查询 [S5](#s5), [S6](#s6), [S9](#s9), [S11](#s11), [S20](#s20), [S24](#s24), [S25](#s25), [S26](#s26), [S27](#s27), [S35](#s35), [S39](#s39), [S42](#s42), [S43](#s43), [S44](#s44), [S46](#s46) → 新增共享状态 C2 → 后续 14 次可复用。该构建点为事后假设，不代表 Agent 当时预知后续。

构建定义：

```sql
SELECT * FROM "google_play__geo_market_analysis" WHERE package_name = 'com.dev.photoeditor'
```

受益查询 S5 的改写示例：

```sql
SELECT * FROM temp.reuse_candidate AS google_play__geo_market_analysis WHERE package_name = 'com.dev.photoeditor' ORDER BY avg_daily_revenue DESC
```

| 原 SQL | 列名一致 | 结果一致 | 比较方法 |
| --- | --- | --- | --- |
| S5 | True | True | ordered_numeric_tolerance |
| S6 | True | True | exact_multiset |
| S9 | True | True | exact_multiset |
| S11 | True | True | ordered_numeric_tolerance |
| S20 | True | True | ordered_numeric_tolerance |
| S24 | True | True | ordered_numeric_tolerance |
| S25 | True | True | ordered_numeric_tolerance |
| S26 | True | True | ordered_numeric_tolerance |
| S27 | True | True | ordered_numeric_tolerance |
| S35 | True | True | ordered_numeric_tolerance |
| S39 | True | True | ordered_numeric_tolerance |
| S42 | True | True | exact_multiset |
| S43 | True | True | exact_multiset |
| S44 | True | True | exact_multiset |
| S46 | True | True | exact_multiset |


验证状态：verified；成本结论：Not benchmarked; correctness alone does not establish net speedup.

### C4：common filtered view

Same single source and complete filter; original filter retained.

原查询 [S7](#s7), [S13](#s13), [S14](#s14), [S18](#s18), [S22](#s22), [S23](#s23), [S29](#s29), [S33](#s33), [S36](#s36), [S40](#s40) → 新增共享状态 C4 → 后续 9 次可复用。该构建点为事后假设，不代表 Agent 当时预知后续。

构建定义：

```sql
SELECT * FROM "google_play__finance_report" WHERE package_name = 'com.dev.photoeditor'
```

受益查询 S7 的改写示例：

```sql
SELECT * FROM temp.reuse_candidate AS google_play__finance_report WHERE package_name = 'com.dev.photoeditor' LIMIT 10
```

| 原 SQL | 列名一致 | 结果一致 | 比较方法 |
| --- | --- | --- | --- |
| S7 | True | True | exact_multiset |
| S13 | True | True | ordered_numeric_tolerance |
| S14 | True | True | exact_multiset |
| S18 | True | True | ordered_numeric_tolerance |
| S22 | True | True | exact_multiset |
| S23 | True | True | ordered_numeric_tolerance |
| S29 | True | True | ordered_numeric_tolerance |
| S33 | True | True | ordered_numeric_tolerance |
| S36 | True | True | ordered_numeric_tolerance |
| S40 | True | True | ordered_numeric_tolerance |


验证状态：verified；成本结论：Not benchmarked; correctness alone does not establish net speedup.

### C1：common filtered view

Same single source and complete filter; original filter retained.

原查询 [S4](#s4), [S16](#s16), [S17](#s17), [S28](#s28), [S34](#s34), [S38](#s38), [S45](#s45) → 新增共享状态 C1 → 后续 6 次可复用。该构建点为事后假设，不代表 Agent 当时预知后续。

构建定义：

```sql
SELECT * FROM "google_play__comprehensive_performance_dashboard" WHERE package_name = 'com.dev.photoeditor'
```

受益查询 S4 的改写示例：

```sql
SELECT * FROM temp.reuse_candidate AS google_play__comprehensive_performance_dashboard WHERE package_name = 'com.dev.photoeditor' ORDER BY date_day LIMIT 10
```

| 原 SQL | 列名一致 | 结果一致 | 比较方法 |
| --- | --- | --- | --- |
| S4 | True | True | ordered_numeric_tolerance |
| S16 | True | True | ordered_numeric_tolerance |
| S17 | True | True | exact_multiset |
| S28 | True | True | ordered_numeric_tolerance |
| S34 | True | True | ordered_numeric_tolerance |
| S38 | True | True | ordered_numeric_tolerance |
| S45 | True | True | ordered_numeric_tolerance |


验证状态：verified；成本结论：Not benchmarked; correctness alone does not establish net speedup.

结果依赖：自动记录 SQL→Python 的接口父调用，以及源码中引用归档文件的消费者；字面值相同不认定因果。模型方向选择需要人工读取消息，尚未做全面因果标注。

[原始报告](../../../runs/dsv4flash-db-first-full-01/dacomp-069/attempt-01/answer.md)；[统一消息](../../../runs/dsv4flash-db-first-full-01/dacomp-069/attempt-01/messages.jsonl)；[原始 OpenCode 事件](../../../runs/dsv4flash-db-first-full-01/dacomp-069/attempt-01/opencode.jsonl)；[SQL 引擎日志](../../../runs/dsv4flash-db-first-full-01/dacomp-069/attempt-01/sql_journal.jsonl)。

[可读报告（本地图片链接规范化）](../answers/dacomp-069.md)。原始回答保留，分析结论未改写。

## S1

类别 `connection_setup`；来源 `connection`；调用 `96f77f81b5ad4db18a0255dfef7c5a3c`；状态 `success`。

```sql
PRAGMA query_only=ON
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-069/attempt-01/sql/S1.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-069/attempt-01/sql/S1.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-069/attempt-01/results/S1.rows.jsonl)；完整：True；SHA256：`e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`。

## S2

类别 `metadata`；来源 `list_db`；调用 `96f77f81b5ad4db18a0255dfef7c5a3c`；状态 `success`。

```sql
SELECT name,sql FROM sqlite_master WHERE type='table' ORDER BY name
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-069/attempt-01/sql/S2.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-069/attempt-01/sql/S2.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-069/attempt-01/results/S2.rows.jsonl)；完整：True；SHA256：`b58be70865309bb56ee7bca8c27f5afae4cb6c079957517138e2ccf29170e11c`。

## S3

类别 `data`；来源 `query_db`；调用 `97e192e3b16c4805aceb90ecee1392a5`；状态 `success`。

```sql
SELECT DISTINCT package_name FROM google_play__comprehensive_performance_dashboard WHERE package_name LIKE '%photo%'
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-069/attempt-01/sql/S3.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-069/attempt-01/sql/S3.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-069/attempt-01/results/S3.rows.jsonl)；完整：True；SHA256：`4c72715f289502002b90dcf0ea2a460229cb158a48eeba695e928ca892337ba4`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "google_play__comprehensive_performance_dashboard", "kind": "base", "block": null, "base_tables": ["google_play__comprehensive_performance_dashboard"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |


## S4

类别 `data`；来源 `query_db`；调用 `7acf6465b08c4100b35faa89553b757e`；状态 `success`。

```sql
SELECT * FROM google_play__comprehensive_performance_dashboard WHERE package_name = 'com.dev.photoeditor' ORDER BY date_day LIMIT 10
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-069/attempt-01/sql/S4.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-069/attempt-01/sql/S4.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-069/attempt-01/results/S4.rows.jsonl)；完整：True；SHA256：`22f22f5286008be4a1524a2449699849857a16d780afd9aa64d6c53a7ac68533`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "google_play__comprehensive_performance_dashboard", "kind": "base", "block": null, "base_tables": ["google_play__comprehensive_performance_dashboard"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |


## S5

类别 `data`；来源 `query_db`；调用 `292fcb536c9a49509b68d1541bb9761c`；状态 `success`。

```sql
SELECT * FROM google_play__geo_market_analysis WHERE package_name = 'com.dev.photoeditor' ORDER BY avg_daily_revenue DESC
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-069/attempt-01/sql/S5.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-069/attempt-01/sql/S5.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-069/attempt-01/results/S5.rows.jsonl)；完整：True；SHA256：`9ab0c8c76e866a1aef82450a81072c007b569fa595b9d3b50b932a1bd9ffc4fe`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "google_play__geo_market_analysis", "kind": "base", "block": null, "base_tables": ["google_play__geo_market_analysis"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |


## S6

类别 `data`；来源 `query_db`；调用 `d36d3e73b7984116a2b03c84409bf27f`；状态 `success`。

```sql
SELECT DISTINCT region FROM google_play__geo_market_analysis WHERE package_name = 'com.dev.photoeditor'
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-069/attempt-01/sql/S6.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-069/attempt-01/sql/S6.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-069/attempt-01/results/S6.rows.jsonl)；完整：True；SHA256：`c4ad6b53d877444ed01deb1d6a53db13552f154913ddd363ebf54b80b610a195`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "google_play__geo_market_analysis", "kind": "base", "block": null, "base_tables": ["google_play__geo_market_analysis"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |


## S7

类别 `data`；来源 `query_db`；调用 `ff7be0738b3343e481f362eb2b1a130c`；状态 `success`。

```sql
SELECT * FROM google_play__finance_report WHERE package_name = 'com.dev.photoeditor' LIMIT 10
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-069/attempt-01/sql/S7.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-069/attempt-01/sql/S7.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-069/attempt-01/results/S7.rows.jsonl)；完整：True；SHA256：`92166b25d84883a8026806261776ba1fe78889866dd4a1d300791b001bb395ff`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "google_play__finance_report", "kind": "base", "block": null, "base_tables": ["google_play__finance_report"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |


## S8

类别 `data`；来源 `query_db`；调用 `b332b16dfc084fc68d0b81dbff244c81`；状态 `success`。

```sql
SELECT MIN(revenue_per_active_device) AS min_rpad, MAX(revenue_per_active_device) AS max_rpad, AVG(revenue_per_active_device) AS avg_rpad FROM google_play__time_series_trends WHERE package_name = 'com.dev.photoeditor'
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-069/attempt-01/sql/S8.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-069/attempt-01/sql/S8.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-069/attempt-01/results/S8.rows.jsonl)；完整：True；SHA256：`5347c89d8e36bfa316fe12753c48d020609ab774bac4c04f58e2064f99705997`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "google_play__time_series_trends", "kind": "base", "block": null, "base_tables": ["google_play__time_series_trends"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | MIN(revenue_per_active_device) | [{"table": "google_play__time_series_trends", "column": "revenue_per_active_device"}] | [] | False |
| B1 | MAX(revenue_per_active_device) | [{"table": "google_play__time_series_trends", "column": "revenue_per_active_device"}] | [] | False |
| B1 | AVG(revenue_per_active_device) | [{"table": "google_play__time_series_trends", "column": "revenue_per_active_device"}] | [] | False |


## S9

类别 `data`；来源 `query_db`；调用 `edc145b2441849c8b60d8e0611ddcb41`；状态 `success`。

```sql
SELECT MIN(avg_transaction_value) AS min_atv, MAX(avg_transaction_value) AS max_atv, MIN(average_revenue_per_user) AS min_arpu, MAX(average_revenue_per_user) AS max_arpu FROM google_play__geo_market_analysis WHERE package_name = 'com.dev.photoeditor'
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-069/attempt-01/sql/S9.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-069/attempt-01/sql/S9.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-069/attempt-01/results/S9.rows.jsonl)；完整：True；SHA256：`9cf555c36bfe9adee2dacddfba2d0ae3101908f8afb589afb476d6dc09afb5d1`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "google_play__geo_market_analysis", "kind": "base", "block": null, "base_tables": ["google_play__geo_market_analysis"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | MIN(avg_transaction_value) | [{"table": "google_play__geo_market_analysis", "column": "avg_transaction_value"}] | [] | False |
| B1 | MAX(avg_transaction_value) | [{"table": "google_play__geo_market_analysis", "column": "avg_transaction_value"}] | [] | False |
| B1 | MIN(average_revenue_per_user) | [{"table": "google_play__geo_market_analysis", "column": "average_revenue_per_user"}] | [] | False |
| B1 | MAX(average_revenue_per_user) | [{"table": "google_play__geo_market_analysis", "column": "average_revenue_per_user"}] | [] | False |


## S10

类别 `data`；来源 `query_db`；调用 `fa68106a162f4931b0dbd6954c12bb53`；状态 `success`。

```sql
SELECT date_day, package_name, daily_revenue, daily_transactions, avg_transaction_value, revenue_per_active_device FROM google_play__time_series_trends WHERE package_name = 'com.dev.photoeditor' ORDER BY date_day
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-069/attempt-01/sql/S10.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-069/attempt-01/sql/S10.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-069/attempt-01/results/S10.rows.jsonl)；完整：True；SHA256：`78ba136ab169c2432a1c443daba022a72560da1ee6851aff803ed33bf7a5b34e`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "google_play__time_series_trends", "kind": "base", "block": null, "base_tables": ["google_play__time_series_trends"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |


## S11

类别 `data`；来源 `query_db`；调用 `e7e2409bd7c340c6bb0dcee611f1342b`；状态 `success`。

```sql
SELECT country, country_name, region, avg_daily_revenue, avg_transaction_value, average_revenue_per_user, revenue_last_30_days, revenue_tier FROM google_play__geo_market_analysis WHERE package_name = 'com.dev.photoeditor' ORDER BY average_revenue_per_user DESC
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-069/attempt-01/sql/S11.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-069/attempt-01/sql/S11.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-069/attempt-01/results/S11.rows.jsonl)；完整：True；SHA256：`df20ae6b195e8454f2ccc573c1a97a720833051ce3ed75c795d5f1e736deb4bd`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "google_play__geo_market_analysis", "kind": "base", "block": null, "base_tables": ["google_play__geo_market_analysis"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |


## S12

类别 `data`；来源 `query_db`；调用 `52029df8680e42b8ac9f841ceaa50576`；状态 `success`。

```sql
SELECT package_name, COUNT(*) AS n FROM google_play__geo_market_analysis GROUP BY package_name
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-069/attempt-01/sql/S12.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-069/attempt-01/sql/S12.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-069/attempt-01/results/S12.rows.jsonl)；完整：True；SHA256：`27c68127f3b562bb02245cac43bb99583a49988907f2b6fc35fa7ebe9f934be3`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "google_play__geo_market_analysis", "kind": "base", "block": null, "base_tables": ["google_play__geo_market_analysis"]}] | [] | ["package_name"] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |


## S13

类别 `data`；来源 `query_db`；调用 `576718f631cb4558b3c063b47082fb51`；状态 `success`。

```sql
SELECT country_short, country_long, region, COUNT(DISTINCT date_day) AS days, SUM(net_amount) AS total_net, SUM(transactions) AS total_tx, SUM(net_amount)/SUM(transactions) AS net_per_tx FROM google_play__finance_report WHERE package_name='com.dev.photoeditor' GROUP BY country_short ORDER BY net_per_tx DESC
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-069/attempt-01/sql/S13.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-069/attempt-01/sql/S13.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-069/attempt-01/results/S13.rows.jsonl)；完整：True；SHA256：`d91ee078b91eaeb7eae72bd2852f1a53f47391ef24cc0df2f33a6f4980e5d36f`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "google_play__finance_report", "kind": "base", "block": null, "base_tables": ["google_play__finance_report"]}] | [] | ["country_short"] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(DISTINCT date_day) | [{"table": "google_play__finance_report", "column": "date_day"}] | [] | False |
| B1 | SUM(net_amount) | [{"table": "google_play__finance_report", "column": "net_amount"}] | [] | False |
| B1 | SUM(transactions) | [{"table": "google_play__finance_report", "column": "transactions"}] | [] | False |
| B1 | SUM(net_amount) | [{"table": "google_play__finance_report", "column": "net_amount"}] | [] | False |
| B1 | SUM(transactions) | [{"table": "google_play__finance_report", "column": "transactions"}] | [] | False |


## S14

类别 `data`；来源 `query_db`；调用 `383e4348c47e4b6bb1636a33ea9401f0`；状态 `success`。

```sql
SELECT sku_id, product_title, COUNT(*) AS n, MIN(net_amount/transactions) AS min_net_per_tx, MAX(net_amount/transactions) AS max_net_per_tx FROM google_play__finance_report WHERE package_name='com.dev.photoeditor' GROUP BY sku_id, product_title
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-069/attempt-01/sql/S14.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-069/attempt-01/sql/S14.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-069/attempt-01/results/S14.rows.jsonl)；完整：True；SHA256：`11bcf20ceca953182e4ebcf813e439f02cbd683b62793123ceef30287d430270`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "google_play__finance_report", "kind": "base", "block": null, "base_tables": ["google_play__finance_report"]}] | [] | ["sku_id", "product_title"] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |
| B1 | MIN(net_amount / transactions) | [{"table": "google_play__finance_report", "column": "net_amount"}, {"table": "google_play__finance_report", "column": "transactions"}] | [] | False |
| B1 | MAX(net_amount / transactions) | [{"table": "google_play__finance_report", "column": "net_amount"}, {"table": "google_play__finance_report", "column": "transactions"}] | [] | False |


## S15

类别 `data`；来源 `query_db`；调用 `ce33ca74a47f4d60b4426cce4abee56c`；状态 `success`。

```sql
SELECT DISTINCT package_name FROM google_play__finance_report
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-069/attempt-01/sql/S15.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-069/attempt-01/sql/S15.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-069/attempt-01/results/S15.rows.jsonl)；完整：True；SHA256：`8ee33e5d9e3ccd5e85df056b1510268d50bf1c47fe55392a82bbd74150506b1d`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "google_play__finance_report", "kind": "base", "block": null, "base_tables": ["google_play__finance_report"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |


## S16

类别 `data`；来源 `query_db`；调用 `3d69ca1b329647639963557fdc5ac7c8`；状态 `success`。

```sql
SELECT date_day, overall_performance_score, quality_score, avg_transaction_value, average_revenue_per_user, daily_net_revenue, daily_transactions, research_budget_usd, primary_risk_flag FROM google_play__comprehensive_performance_dashboard WHERE package_name='com.dev.photoeditor' ORDER BY date_day
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-069/attempt-01/sql/S16.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-069/attempt-01/sql/S16.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-069/attempt-01/results/S16.rows.jsonl)；完整：True；SHA256：`e166eab45090658914f211a3b7346d7b24b1c693bf7332ca2821af9866572c08`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "google_play__comprehensive_performance_dashboard", "kind": "base", "block": null, "base_tables": ["google_play__comprehensive_performance_dashboard"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |


## S17

类别 `data`；来源 `query_db`；调用 `a6e38180788b4e68a9dc8482c481c09a`；状态 `success`。

```sql
SELECT COUNT(*) AS n, COUNT(DISTINCT date_day) AS days, SUM(research_budget_usd) AS total_budget, MIN(overall_performance_score) AS min_ops, MAX(overall_performance_score) AS max_ops FROM google_play__comprehensive_performance_dashboard WHERE package_name='com.dev.photoeditor'
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-069/attempt-01/sql/S17.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-069/attempt-01/sql/S17.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-069/attempt-01/results/S17.rows.jsonl)；完整：True；SHA256：`8e6236d61418ad9546ba8d3c47398e980e7f68c8ad9c3a76e7dab782cc89e4c2`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "google_play__comprehensive_performance_dashboard", "kind": "base", "block": null, "base_tables": ["google_play__comprehensive_performance_dashboard"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |
| B1 | COUNT(DISTINCT date_day) | [{"table": "google_play__comprehensive_performance_dashboard", "column": "date_day"}] | [] | False |
| B1 | SUM(research_budget_usd) | [{"table": "google_play__comprehensive_performance_dashboard", "column": "research_budget_usd"}] | [] | False |
| B1 | MIN(overall_performance_score) | [{"table": "google_play__comprehensive_performance_dashboard", "column": "overall_performance_score"}] | [] | False |
| B1 | MAX(overall_performance_score) | [{"table": "google_play__comprehensive_performance_dashboard", "column": "overall_performance_score"}] | [] | False |


## S18

类别 `data`；来源 `query_db`；调用 `98bc422418ce43399ebe5f65607449a4`；状态 `success`。

```sql
SELECT country_short, sku_id, COUNT(*) AS days, SUM(net_amount) AS total_net, SUM(transactions) AS total_tx, SUM(net_amount)/SUM(transactions) AS net_per_tx FROM google_play__finance_report WHERE package_name='com.dev.photoeditor' GROUP BY country_short, sku_id ORDER BY country_short, sku_id
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-069/attempt-01/sql/S18.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-069/attempt-01/sql/S18.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-069/attempt-01/results/S18.rows.jsonl)；完整：True；SHA256：`7d500aa013edc69b9b47389bb6b08abcbbae30ad47386c1efdaa1508f4da9e91`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "google_play__finance_report", "kind": "base", "block": null, "base_tables": ["google_play__finance_report"]}] | [] | ["country_short", "sku_id"] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |
| B1 | SUM(net_amount) | [{"table": "google_play__finance_report", "column": "net_amount"}] | [] | False |
| B1 | SUM(transactions) | [{"table": "google_play__finance_report", "column": "transactions"}] | [] | False |
| B1 | SUM(net_amount) | [{"table": "google_play__finance_report", "column": "net_amount"}] | [] | False |
| B1 | SUM(transactions) | [{"table": "google_play__finance_report", "column": "transactions"}] | [] | False |


## S19

类别 `data`；来源 `query_db`；调用 `e8ead3643ebe444fa15261ee11588856`；状态 `success`。

```sql
SELECT date_day, country_short, sku_id, net_amount, transactions, charge_amount, charge_transactions, new_subscriptions, cancelled_subscriptions, total_active_subscriptions FROM google_play__finance_report WHERE package_name='com.dev.photoeditor' AND sku_id LIKE '%basic%' ORDER BY date_day, country_short LIMIT 30
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-069/attempt-01/sql/S19.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-069/attempt-01/sql/S19.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-069/attempt-01/results/S19.rows.jsonl)；完整：True；SHA256：`cdfcd833be5e995461c4c62aff53df1003fc46b72ef7e26a755af2b56fbc4d3b`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "google_play__finance_report", "kind": "base", "block": null, "base_tables": ["google_play__finance_report"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |


## S20

类别 `data`；来源 `query_db`；调用 `dbfb1b19570a4b769d5ff9d56da45153`；状态 `success`。

```sql
SELECT country, region, avg_daily_installs, avg_active_devices, store_visitors_30d, store_installs_30d, avg_daily_revenue,
  ROUND(avg_daily_revenue/avg_daily_installs,2) AS rev_per_install_day,
  ROUND(revenue_last_30_days/store_installs_30d,2) AS rev_per_install_ltv,
  ROUND(avg_daily_revenue*30/store_visitors_30d,2) AS rev_per_visitor,
  ROUND(avg_daily_revenue/avg_active_devices,2) AS rev_per_active_device
FROM google_play__geo_market_analysis WHERE package_name='com.dev.photoeditor' ORDER BY avg_daily_revenue DESC
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-069/attempt-01/sql/S20.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-069/attempt-01/sql/S20.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-069/attempt-01/results/S20.rows.jsonl)；完整：True；SHA256：`1c55d8177091783f378b24ef309bce0b7a73ea6e0357f4a2839b31a261b4e4aa`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "google_play__geo_market_analysis", "kind": "base", "block": null, "base_tables": ["google_play__geo_market_analysis"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |


## S21

类别 `data`；来源 `query_db`；调用 `e4ad0b49f6284d96b007ade16fafb339`；状态 `success`。

```sql
SELECT package_name, sku_id, product_title, COUNT(*) AS n, MIN(net_amount/transactions) AS min_per_tx, MAX(net_amount/transactions) AS max_per_tx FROM google_play__finance_report GROUP BY package_name, sku_id, product_title ORDER BY package_name, min_per_tx
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-069/attempt-01/sql/S21.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-069/attempt-01/sql/S21.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-069/attempt-01/results/S21.rows.jsonl)；完整：True；SHA256：`5c86eb4ced99fb90af18ea21809fc61461b076a699a1d20e1a81ebe5e25576fd`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "google_play__finance_report", "kind": "base", "block": null, "base_tables": ["google_play__finance_report"]}] | [] | ["package_name", "sku_id", "product_title"] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |
| B1 | MIN(net_amount / transactions) | [{"table": "google_play__finance_report", "column": "net_amount"}, {"table": "google_play__finance_report", "column": "transactions"}] | [] | False |
| B1 | MAX(net_amount / transactions) | [{"table": "google_play__finance_report", "column": "net_amount"}, {"table": "google_play__finance_report", "column": "transactions"}] | [] | False |


## S22

类别 `data`；来源 `query_db`；调用 `32201449cd134f0da185ffc811c2e99a`；状态 `success`。

```sql
SELECT COUNT(*) AS n, COUNT(DISTINCT country_short) AS countries, COUNT(DISTINCT date_day) AS days, MIN(date_day) AS min_date, MAX(date_day) AS max_date FROM google_play__finance_report WHERE package_name='com.dev.photoeditor'
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-069/attempt-01/sql/S22.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-069/attempt-01/sql/S22.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-069/attempt-01/results/S22.rows.jsonl)；完整：True；SHA256：`d57df64415d9049d25acd133de34d6d734b73858658a4fd38cb7afcbfb30c1a6`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "google_play__finance_report", "kind": "base", "block": null, "base_tables": ["google_play__finance_report"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |
| B1 | COUNT(DISTINCT country_short) | [{"table": "google_play__finance_report", "column": "country_short"}] | [] | False |
| B1 | COUNT(DISTINCT date_day) | [{"table": "google_play__finance_report", "column": "date_day"}] | [] | False |
| B1 | MIN(date_day) | [{"table": "google_play__finance_report", "column": "date_day"}] | [] | False |
| B1 | MAX(date_day) | [{"table": "google_play__finance_report", "column": "date_day"}] | [] | False |


## S23

类别 `data`；来源 `query_db`；调用 `3197514125464496a3c1cd25cea1b981`；状态 `success`。

```sql
SELECT date_day, country_short, sku_id, net_amount, transactions, ROUND(net_amount/transactions,2) AS net_per_tx FROM google_play__finance_report WHERE package_name='com.dev.photoeditor' ORDER BY date_day, country_short
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-069/attempt-01/sql/S23.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-069/attempt-01/sql/S23.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-069/attempt-01/results/S23.rows.jsonl)；完整：True；SHA256：`88fef4f9a16bec0c2fd18335919745a174611c8f5ebc841aa38930ad3860c2f2`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "google_play__finance_report", "kind": "base", "block": null, "base_tables": ["google_play__finance_report"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |


## S24

类别 `data`；来源 `query_db`；调用 `e5557557bb00411cbb10076502fa3dab`；状态 `success`。

```sql
SELECT country, region, ROUND(avg_daily_revenue,2) AS daily_rev, ROUND(avg_transaction_value,2) AS atv, ROUND(average_revenue_per_user,2) AS arpu, revenue_tier, market_tier, weekly_growth_rate, ROUND(app_quality_score,1) AS quality, ROUND(app_crash_rate_per_1k,2) AS crash, ROUND(day_30_retention_rate,3) AS d30_ret, ROUND(daily_churn_rate,2) AS churn, overall_market_score, opportunity_type, investment_recommendation FROM google_play__geo_market_analysis WHERE package_name='com.dev.photoeditor' ORDER BY arpu DESC
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-069/attempt-01/sql/S24.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-069/attempt-01/sql/S24.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-069/attempt-01/results/S24.rows.jsonl)；完整：True；SHA256：`4d1235496364047d8e4b298fad4f41334165c029353412bf8862e9e1ac0f2d79`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "google_play__geo_market_analysis", "kind": "base", "block": null, "base_tables": ["google_play__geo_market_analysis"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |


## S25

类别 `data`；来源 `query_db`；调用 `93a05b10b78b4c6e8acafd4cb93509e4`；状态 `success`。

```sql
SELECT region, 
  COUNT(*) AS n_countries,
  ROUND(SUM(avg_daily_revenue),2) AS total_daily_rev,
  ROUND(AVG(avg_daily_revenue),2) AS avg_daily_rev,
  ROUND(AVG(average_revenue_per_user),2) AS avg_arpu,
  ROUND(AVG(avg_transaction_value),2) AS avg_atv,
  ROUND(AVG(app_quality_score),2) AS avg_quality,
  ROUND(AVG(app_crash_rate_per_1k),2) AS avg_crash,
  ROUND(AVG(day_7_retention_rate),3) AS avg_d7_ret,
  ROUND(AVG(day_30_retention_rate),3) AS avg_d30_ret,
  ROUND(AVG(daily_churn_rate),3) AS avg_churn,
  ROUND(AVG(weekly_growth_rate),3) AS avg_growth,
  ROUND(AVG(overall_market_score),2) AS avg_market_score
FROM google_play__geo_market_analysis 
WHERE package_name='com.dev.photoeditor' 
GROUP BY region
ORDER BY total_daily_rev DESC
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-069/attempt-01/sql/S25.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-069/attempt-01/sql/S25.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-069/attempt-01/results/S25.rows.jsonl)；完整：True；SHA256：`3e2630b074c098ea3e4e46cba454a7544d63befeb5639446007ec0804f831a42`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "google_play__geo_market_analysis", "kind": "base", "block": null, "base_tables": ["google_play__geo_market_analysis"]}] | [] | ["region"] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |
| B1 | SUM(avg_daily_revenue) | [{"table": "google_play__geo_market_analysis", "column": "avg_daily_revenue"}] | [] | False |
| B1 | AVG(avg_daily_revenue) | [{"table": "google_play__geo_market_analysis", "column": "avg_daily_revenue"}] | [] | False |
| B1 | AVG(average_revenue_per_user) | [{"table": "google_play__geo_market_analysis", "column": "average_revenue_per_user"}] | [] | False |
| B1 | AVG(avg_transaction_value) | [{"table": "google_play__geo_market_analysis", "column": "avg_transaction_value"}] | [] | False |
| B1 | AVG(app_quality_score) | [{"table": "google_play__geo_market_analysis", "column": "app_quality_score"}] | [] | False |
| B1 | AVG(app_crash_rate_per_1k) | [{"table": "google_play__geo_market_analysis", "column": "app_crash_rate_per_1k"}] | [] | False |
| B1 | AVG(day_7_retention_rate) | [{"table": "google_play__geo_market_analysis", "column": "day_7_retention_rate"}] | [] | False |
| B1 | AVG(day_30_retention_rate) | [{"table": "google_play__geo_market_analysis", "column": "day_30_retention_rate"}] | [] | False |
| B1 | AVG(daily_churn_rate) | [{"table": "google_play__geo_market_analysis", "column": "daily_churn_rate"}] | [] | False |
| B1 | AVG(weekly_growth_rate) | [{"table": "google_play__geo_market_analysis", "column": "weekly_growth_rate"}] | [] | False |
| B1 | AVG(overall_market_score) | [{"table": "google_play__geo_market_analysis", "column": "overall_market_score"}] | [] | False |


## S26

类别 `data`；来源 `query_db`；调用 `8d25f392d2c8416699ee48e3a7ad1847`；状态 `success`。

```sql
SELECT 
  CASE WHEN average_revenue_per_user > 7 THEN 'High ARPU (>$7)' ELSE 'Low ARPU (<$7)' END AS arpu_group,
  COUNT(*) AS n,
  ROUND(SUM(avg_daily_revenue),2) AS total_daily_rev,
  ROUND(AVG(avg_daily_installs),0) AS avg_installs,
  ROUND(AVG(avg_active_devices),0) AS avg_devices,
  ROUND(AVG(average_revenue_per_user),2) AS avg_arpu,
  ROUND(AVG(avg_transaction_value),2) AS avg_atv,
  ROUND(AVG(app_quality_score),2) AS avg_quality,
  ROUND(AVG(app_crash_rate_per_1k),2) AS avg_crash,
  ROUND(AVG(day_7_retention_rate),3) AS avg_d7_ret,
  ROUND(AVG(day_30_retention_rate),3) AS avg_d30_ret,
  ROUND(AVG(daily_churn_rate),3) AS avg_churn,
  ROUND(AVG(weekly_growth_rate),3) AS avg_growth,
  ROUND(AVG(overall_market_score),2) AS avg_market_score
FROM google_play__geo_market_analysis 
WHERE package_name='com.dev.photoeditor'
GROUP BY arpu_group
ORDER BY arpu_group DESC
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-069/attempt-01/sql/S26.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-069/attempt-01/sql/S26.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-069/attempt-01/results/S26.rows.jsonl)；完整：True；SHA256：`e3a8572a3d98ea06c66408e7efc3a1de7a1dcd8093b6961d5f8afb48dfad0bc2`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "google_play__geo_market_analysis", "kind": "base", "block": null, "base_tables": ["google_play__geo_market_analysis"]}] | [] | ["CASE WHEN average_revenue_per_user > 7 THEN 'High ARPU (>$7)' ELSE 'Low ARPU (<$7)' END"] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |
| B1 | SUM(avg_daily_revenue) | [{"table": "google_play__geo_market_analysis", "column": "avg_daily_revenue"}] | [] | False |
| B1 | AVG(avg_daily_installs) | [{"table": "google_play__geo_market_analysis", "column": "avg_daily_installs"}] | [] | False |
| B1 | AVG(avg_active_devices) | [{"table": "google_play__geo_market_analysis", "column": "avg_active_devices"}] | [] | False |
| B1 | AVG(average_revenue_per_user) | [{"table": "google_play__geo_market_analysis", "column": "average_revenue_per_user"}] | [] | False |
| B1 | AVG(avg_transaction_value) | [{"table": "google_play__geo_market_analysis", "column": "avg_transaction_value"}] | [] | False |
| B1 | AVG(app_quality_score) | [{"table": "google_play__geo_market_analysis", "column": "app_quality_score"}] | [] | False |
| B1 | AVG(app_crash_rate_per_1k) | [{"table": "google_play__geo_market_analysis", "column": "app_crash_rate_per_1k"}] | [] | False |
| B1 | AVG(day_7_retention_rate) | [{"table": "google_play__geo_market_analysis", "column": "day_7_retention_rate"}] | [] | False |
| B1 | AVG(day_30_retention_rate) | [{"table": "google_play__geo_market_analysis", "column": "day_30_retention_rate"}] | [] | False |
| B1 | AVG(daily_churn_rate) | [{"table": "google_play__geo_market_analysis", "column": "daily_churn_rate"}] | [] | False |
| B1 | AVG(weekly_growth_rate) | [{"table": "google_play__geo_market_analysis", "column": "weekly_growth_rate"}] | [] | False |
| B1 | AVG(overall_market_score) | [{"table": "google_play__geo_market_analysis", "column": "overall_market_score"}] | [] | False |


## S27

类别 `data`；来源 `query_db`；调用 `041bfdba514e4c3db0878f4dae0de068`；状态 `success`。

```sql
SELECT country, region, average_revenue_per_user, avg_transaction_value, app_quality_score, app_crash_rate_per_1k, day_7_retention_rate, day_30_retention_rate, daily_churn_rate, weekly_growth_rate, overall_market_score, market_tier, revenue_tier, opportunity_type, investment_recommendation, market_insight FROM google_play__geo_market_analysis WHERE package_name='com.dev.photoeditor' ORDER BY average_revenue_per_user DESC
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-069/attempt-01/sql/S27.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-069/attempt-01/sql/S27.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-069/attempt-01/results/S27.rows.jsonl)；完整：True；SHA256：`e209f8a259cfdfa1b4a86a3347bdd2d9d5d6eaa6820d2c938ae6431678e5897c`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "google_play__geo_market_analysis", "kind": "base", "block": null, "base_tables": ["google_play__geo_market_analysis"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |


## S28

类别 `data`；来源 `query_db`；调用 `8f75c7e11a67465ebdd2c0929804dc52`；状态 `success`。

```sql
SELECT date_day, overall_performance_score, quality_score, daily_installs, daily_uninstalls, active_devices, daily_crashes, daily_anrs, crash_rate_per_1k_devices, daily_churn_rate, day_7_retention_rate, day_30_retention_rate, daily_net_revenue, daily_transactions, avg_transaction_value, average_revenue_per_user, revenue_health_score, primary_risk_flag, recommended_action, research_budget_usd FROM google_play__comprehensive_performance_dashboard WHERE package_name='com.dev.photoeditor' ORDER BY date_day
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-069/attempt-01/sql/S28.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-069/attempt-01/sql/S28.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-069/attempt-01/results/S28.rows.jsonl)；完整：True；SHA256：`10ed799ac3410a201bc305788028666d109dc99f99aaae4eb87e08b06514e083`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "google_play__comprehensive_performance_dashboard", "kind": "base", "block": null, "base_tables": ["google_play__comprehensive_performance_dashboard"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |


## S29

类别 `data`；来源 `query_db`；调用 `f483e503e0924487862f2aa88bf2dae4`；状态 `success`。

```sql
SELECT country_short, region, strftime('%Y-%m', date_day) AS month, sku_id, net_amount, transactions, ROUND(net_amount/transactions,2) AS net_per_tx, new_subscriptions, cancelled_subscriptions, total_active_subscriptions FROM google_play__finance_report WHERE package_name='com.dev.photoeditor' ORDER BY country_short, date_day, sku_id
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-069/attempt-01/sql/S29.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-069/attempt-01/sql/S29.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-069/attempt-01/results/S29.rows.jsonl)；完整：True；SHA256：`52b41f9b9480541ce4838263dbf00ed91ba5216b5b6720456cc431277611f8bd`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "google_play__finance_report", "kind": "base", "block": null, "base_tables": ["google_play__finance_report"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |


## S30

类别 `data`；来源 `query_db`；调用 `a4af2ac7b61340969cd394d111f861c1`；状态 `failed`。

```sql
SELECT date_day, daily_revenue, daily_transactions, avg_transaction_value, quality_score, crash_rate_per_1k, anr_rate_per_1k, daily_churn_rate, day_1_retention_rate, active_subscriptions, new_subscriptions, revenue_trend, performance_momentum, anomaly_flag, risk_growth_profile, revenue_per_active_device FROM google_play__time_series_trends WHERE package_name='com.dev.photoeditor' ORDER BY date_day
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-069/attempt-01/sql/S30.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-069/attempt-01/sql/S30.parameters.json)。

错误：`OperationalError('no such column: day_1_retention_rate')`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "google_play__time_series_trends", "kind": "base", "block": null, "base_tables": ["google_play__time_series_trends"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |


未解析列血缘：[{"block": "B1", "column": "day_1_retention_rate", "reason": "ambiguous_or_missing_source"}]

## S31

类别 `data`；来源 `query_db`；调用 `51aa3c0a86f94bc086b686886ccc0506`；状态 `success`。

```sql
SELECT date_day, daily_revenue, daily_transactions, avg_transaction_value, quality_score, crash_rate_per_1k, anr_rate_per_1k, daily_churn_rate, active_subscriptions, new_subscriptions, revenue_trend, performance_momentum, anomaly_flag, risk_growth_profile, revenue_per_active_device FROM google_play__time_series_trends WHERE package_name='com.dev.photoeditor' ORDER BY date_day
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-069/attempt-01/sql/S31.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-069/attempt-01/sql/S31.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-069/attempt-01/results/S31.rows.jsonl)；完整：True；SHA256：`2ca446522cad4aa5885f022ad21e3c4a3cd78563f573f59e5a1df78dfa759ed0`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "google_play__time_series_trends", "kind": "base", "block": null, "base_tables": ["google_play__time_series_trends"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |


## S32

类别 `data`；来源 `query_db`；调用 `07735a7559ba41089322b47fbf67fb59`；状态 `success`。

```sql
WITH monthly AS (
  SELECT country_short, sku_id, strftime('%Y-%m', date_day) AS month,
         SUM(net_amount) AS net, SUM(transactions) AS tx
  FROM google_play__finance_report
  WHERE package_name='com.dev.photoeditor'
  GROUP BY country_short, sku_id, month
),
first_last AS (
  SELECT country_short, sku_id,
    MIN(month) AS first_m, MAX(month) AS last_m,
    SUM(CASE WHEN month = (SELECT MIN(m2.month) FROM monthly m2 WHERE m2.country_short=monthly.country_short AND m2.sku_id=monthly.sku_id) THEN net END) AS first_net,
    SUM(CASE WHEN month = (SELECT MAX(m2.month) FROM monthly m2 WHERE m2.country_short=monthly.country_short AND m2.sku_id=monthly.sku_id) THEN net END) AS last_net
  FROM monthly
  GROUP BY country_short, sku_id
)
SELECT country_short, sku_id, first_m, last_m, ROUND(first_net,2) AS first_net, ROUND(last_net,2) AS last_net,
  ROUND((last_net-first_net)/first_net*100,1) AS pct_change
FROM first_last ORDER BY pct_change
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-069/attempt-01/sql/S32.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-069/attempt-01/sql/S32.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-069/attempt-01/results/S32.rows.jsonl)；完整：True；SHA256：`cae0602698d52a157e68cc57dbebd4fcfc0ea866a14a3b1f388ff147930af6da`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "google_play__finance_report", "kind": "base", "block": null, "base_tables": ["google_play__finance_report"]}] | [] | ["country_short", "sku_id", "STRFTIME('%Y-%m', date_day)"] |
| B2 | [{"alias": "m2", "kind": "derived", "block": "B1", "base_tables": ["google_play__finance_report"]}] | [] | [] |
| B3 | [{"alias": "m2", "kind": "derived", "block": "B1", "base_tables": ["google_play__finance_report"]}] | [] | [] |
| B4 | [{"alias": "monthly", "kind": "derived", "block": "B1", "base_tables": ["google_play__finance_report"]}] | [] | ["country_short", "sku_id"] |
| B5 | [{"alias": "first_last", "kind": "derived", "block": "B4", "base_tables": ["google_play__finance_report"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | SUM(net_amount) | [{"table": "google_play__finance_report", "column": "net_amount"}] | [] | False |
| B1 | SUM(transactions) | [{"table": "google_play__finance_report", "column": "transactions"}] | [] | False |
| B2 | MIN(m2.month) | [{"table": "google_play__finance_report", "column": "date_day"}] | [] | False |
| B3 | MAX(m2.month) | [{"table": "google_play__finance_report", "column": "date_day"}] | [] | False |
| B4 | MIN(month) | [{"table": "google_play__finance_report", "column": "date_day"}] | [] | False |
| B4 | MAX(month) | [{"table": "google_play__finance_report", "column": "date_day"}] | [] | False |
| B4 | SUM(CASE WHEN month = (SELECT MIN(m2.month) FROM monthly AS m2 WHERE m2.country_short = monthly.country_short AND m2.sku_id = monthly.sku_id) THEN net END) | [{"table": "google_play__finance_report", "column": "net_amount"}] | [{"table": "google_play__finance_report", "column": "date_day"}, {"table": "google_play__finance_report", "column": "date_day"}, {"table": "google_play__finance_report", "column": "country_short"}, {"table": "google_play__finance_report", "column": "country_short"}, {"table": "google_play__finance_report", "column": "sku_id"}, {"table": "google_play__finance_report", "column": "sku_id"}] | False |
| B4 | SUM(CASE WHEN month = (SELECT MAX(m2.month) FROM monthly AS m2 WHERE m2.country_short = monthly.country_short AND m2.sku_id = monthly.sku_id) THEN net END) | [{"table": "google_play__finance_report", "column": "net_amount"}] | [{"table": "google_play__finance_report", "column": "date_day"}, {"table": "google_play__finance_report", "column": "date_day"}, {"table": "google_play__finance_report", "column": "country_short"}, {"table": "google_play__finance_report", "column": "country_short"}, {"table": "google_play__finance_report", "column": "sku_id"}, {"table": "google_play__finance_report", "column": "sku_id"}] | False |


## S33

类别 `data`；来源 `query_db`；调用 `106f55c358e842febeb8885dd533294a`；状态 `success`。

```sql
SELECT country_short, sku_id, SUM(new_subscriptions) AS total_new_sub, SUM(cancelled_subscriptions) AS total_cancel, SUM(total_active_subscriptions) AS total_active FROM google_play__finance_report WHERE package_name='com.dev.photoeditor' GROUP BY country_short, sku_id ORDER BY total_active DESC
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-069/attempt-01/sql/S33.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-069/attempt-01/sql/S33.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-069/attempt-01/results/S33.rows.jsonl)；完整：True；SHA256：`e18f4b9595653b4966bafc53cd0303cbcce439343b330a4892399daa2a305ad2`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "google_play__finance_report", "kind": "base", "block": null, "base_tables": ["google_play__finance_report"]}] | [] | ["country_short", "sku_id"] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | SUM(new_subscriptions) | [{"table": "google_play__finance_report", "column": "new_subscriptions"}] | [] | False |
| B1 | SUM(cancelled_subscriptions) | [{"table": "google_play__finance_report", "column": "cancelled_subscriptions"}] | [] | False |
| B1 | SUM(total_active_subscriptions) | [{"table": "google_play__finance_report", "column": "total_active_subscriptions"}] | [] | False |


## S34

类别 `data`；来源 `python`；调用 `43ea3f34979b4986b286896d538e9b1a`；状态 `success`。

```sql
SELECT date_day, overall_performance_score, quality_score, daily_net_revenue, daily_installs, daily_uninstalls, active_devices, daily_crashes, crash_rate_per_1k_devices, day_7_retention_rate, day_30_retention_rate, daily_churn_rate, avg_transaction_value, average_revenue_per_user, revenue_health_score FROM google_play__comprehensive_performance_dashboard WHERE package_name='com.dev.photoeditor' ORDER BY date_day
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-069/attempt-01/sql/S34.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-069/attempt-01/sql/S34.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-069/attempt-01/results/S34.rows.jsonl)；完整：True；SHA256：`0cc3a2dce4c763e00e5f8072f181a789a7e8d75939d702248d7b4afab97c1b3a`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "google_play__comprehensive_performance_dashboard", "kind": "base", "block": null, "base_tables": ["google_play__comprehensive_performance_dashboard"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |


## S35

类别 `data`；来源 `python`；调用 `43ea3f34979b4986b286896d538e9b1a`；状态 `success`。

```sql
SELECT country, region, average_revenue_per_user, avg_transaction_value, app_quality_score, app_crash_rate_per_1k, day_7_retention_rate, day_30_retention_rate, daily_churn_rate, weekly_growth_rate, overall_market_score, market_tier, revenue_tier, avg_daily_revenue, avg_active_devices, avg_daily_installs, store_visitors_30d, store_installs_30d FROM google_play__geo_market_analysis WHERE package_name='com.dev.photoeditor' ORDER BY average_revenue_per_user DESC
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-069/attempt-01/sql/S35.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-069/attempt-01/sql/S35.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-069/attempt-01/results/S35.rows.jsonl)；完整：True；SHA256：`7dea722055983eb7fe619d581f2fc549d6be0777e04c03bc36cc437d7d2e837f`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "google_play__geo_market_analysis", "kind": "base", "block": null, "base_tables": ["google_play__geo_market_analysis"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |


## S36

类别 `data`；来源 `python`；调用 `43ea3f34979b4986b286896d538e9b1a`；状态 `success`。

```sql
SELECT country_short, date_day, sku_id, net_amount, transactions, new_subscriptions, cancelled_subscriptions, total_active_subscriptions FROM google_play__finance_report WHERE package_name='com.dev.photoeditor' ORDER BY country_short, date_day, sku_id
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-069/attempt-01/sql/S36.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-069/attempt-01/sql/S36.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-069/attempt-01/results/S36.rows.jsonl)；完整：True；SHA256：`0c2f95dc27906c13d6ec917757e743b18fb811b1d694b7dd0d1852b89800ca1a`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "google_play__finance_report", "kind": "base", "block": null, "base_tables": ["google_play__finance_report"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |


## S37

类别 `data`；来源 `python`；调用 `43ea3f34979b4986b286896d538e9b1a`；状态 `success`。

```sql
SELECT date_day, daily_revenue, quality_score, crash_rate_per_1k, anr_rate_per_1k, daily_churn_rate, new_subscriptions, active_subscriptions, revenue_per_active_device FROM google_play__time_series_trends WHERE package_name='com.dev.photoeditor' ORDER BY date_day
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-069/attempt-01/sql/S37.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-069/attempt-01/sql/S37.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-069/attempt-01/results/S37.rows.jsonl)；完整：True；SHA256：`a2f3e0446abdc53a15cfe43db2027764883160918406512b48b65c44f3a5e8b9`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "google_play__time_series_trends", "kind": "base", "block": null, "base_tables": ["google_play__time_series_trends"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |


## S38

类别 `data`；来源 `python`；调用 `219a2a2c5cbf491fa3119e280605d60f`；状态 `success`。

```sql
SELECT date_day, overall_performance_score, quality_score, daily_net_revenue, daily_installs, daily_uninstalls, active_devices, daily_crashes, crash_rate_per_1k_devices, day_7_retention_rate, day_30_retention_rate, daily_churn_rate FROM google_play__comprehensive_performance_dashboard WHERE package_name='com.dev.photoeditor' ORDER BY date_day
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-069/attempt-01/sql/S38.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-069/attempt-01/sql/S38.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-069/attempt-01/results/S38.rows.jsonl)；完整：True；SHA256：`6419c755b3b652f3f98f1d54e414569ee22376c9b3c4eb3b1b3f61a96ad5fe03`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "google_play__comprehensive_performance_dashboard", "kind": "base", "block": null, "base_tables": ["google_play__comprehensive_performance_dashboard"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |


## S39

类别 `data`；来源 `python`；调用 `219a2a2c5cbf491fa3119e280605d60f`；状态 `success`。

```sql
SELECT country, region, average_revenue_per_user, avg_transaction_value, app_quality_score, app_crash_rate_per_1k, day_7_retention_rate, day_30_retention_rate, daily_churn_rate, weekly_growth_rate, overall_market_score, market_tier, revenue_tier FROM google_play__geo_market_analysis WHERE package_name='com.dev.photoeditor' ORDER BY average_revenue_per_user DESC
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-069/attempt-01/sql/S39.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-069/attempt-01/sql/S39.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-069/attempt-01/results/S39.rows.jsonl)；完整：True；SHA256：`5cb846e96a041b4457c0135f01596a2523264e83f8bc60b393f24e6c0050ba4c`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "google_play__geo_market_analysis", "kind": "base", "block": null, "base_tables": ["google_play__geo_market_analysis"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |


## S40

类别 `data`；来源 `python`；调用 `219a2a2c5cbf491fa3119e280605d60f`；状态 `success`。

```sql
SELECT country_short, date_day, sku_id, net_amount, transactions FROM google_play__finance_report WHERE package_name='com.dev.photoeditor' ORDER BY country_short, date_day, sku_id
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-069/attempt-01/sql/S40.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-069/attempt-01/sql/S40.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-069/attempt-01/results/S40.rows.jsonl)；完整：True；SHA256：`27c9dd5fbcd01045bb7ce540e1cf1f54d85b0a55e53210c3dc7b7abc3c55d2d7`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "google_play__finance_report", "kind": "base", "block": null, "base_tables": ["google_play__finance_report"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |


## S41

类别 `data`；来源 `python`；调用 `219a2a2c5cbf491fa3119e280605d60f`；状态 `success`。

```sql
SELECT date_day, daily_revenue, quality_score, crash_rate_per_1k, anr_rate_per_1k, daily_churn_rate FROM google_play__time_series_trends WHERE package_name='com.dev.photoeditor' ORDER BY date_day
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-069/attempt-01/sql/S41.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-069/attempt-01/sql/S41.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-069/attempt-01/results/S41.rows.jsonl)；完整：True；SHA256：`c55ed40159a4388ca045f4f4bf3cb6d3d93854460d327971e86be1b6d071ccc9`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "google_play__time_series_trends", "kind": "base", "block": null, "base_tables": ["google_play__time_series_trends"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |


## S42

类别 `data`；来源 `python`；调用 `400fe934462f4c108ebbe76d05a6feb6`；状态 `success`。

```sql
SELECT country, region, average_revenue_per_user, avg_transaction_value, app_quality_score, app_crash_rate_per_1k, day_30_retention_rate, daily_churn_rate, weekly_growth_rate, overall_market_score, avg_daily_revenue, avg_active_devices, avg_daily_installs FROM google_play__geo_market_analysis WHERE package_name='com.dev.photoeditor'
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-069/attempt-01/sql/S42.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-069/attempt-01/sql/S42.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-069/attempt-01/results/S42.rows.jsonl)；完整：True；SHA256：`72e5cc478e35cbd1cad3a7b61478eeca0b423693d9c2e55beba20feb2550c062`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "google_play__geo_market_analysis", "kind": "base", "block": null, "base_tables": ["google_play__geo_market_analysis"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |


## S43

类别 `data`；来源 `python`；调用 `995cbce0e7554419b37a20c638f88325`；状态 `success`。

```sql
SELECT country, region, average_revenue_per_user, avg_transaction_value, app_quality_score, app_crash_rate_per_1k, day_30_retention_rate, daily_churn_rate, weekly_growth_rate, overall_market_score, avg_daily_revenue, avg_active_devices, avg_daily_installs, revenue_tier, market_tier FROM google_play__geo_market_analysis WHERE package_name='com.dev.photoeditor'
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-069/attempt-01/sql/S43.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-069/attempt-01/sql/S43.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-069/attempt-01/results/S43.rows.jsonl)；完整：True；SHA256：`1ef61ec16089ebbfb4abde414ec7160502ebfd6af924f5cd5afcca457968a860`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "google_play__geo_market_analysis", "kind": "base", "block": null, "base_tables": ["google_play__geo_market_analysis"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |


## S44

类别 `data`；来源 `python`；调用 `624d12c2e29043beb2862077ebdbb05e`；状态 `success`。

```sql
SELECT country, region, average_revenue_per_user, avg_transaction_value, app_quality_score, app_crash_rate_per_1k, day_7_retention_rate, day_30_retention_rate, daily_churn_rate, weekly_growth_rate, overall_market_score, avg_daily_revenue, avg_active_devices, avg_daily_installs, revenue_tier, market_tier, opportunity_type, investment_recommendation FROM google_play__geo_market_analysis WHERE package_name='com.dev.photoeditor'
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-069/attempt-01/sql/S44.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-069/attempt-01/sql/S44.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-069/attempt-01/results/S44.rows.jsonl)；完整：True；SHA256：`b80776501bdad711ca70a2167feb1eb52927f7c7bae242134ab48780d2069b8f`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "google_play__geo_market_analysis", "kind": "base", "block": null, "base_tables": ["google_play__geo_market_analysis"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |


## S45

类别 `data`；来源 `python`；调用 `624d12c2e29043beb2862077ebdbb05e`；状态 `success`。

```sql
SELECT date_day, overall_performance_score, quality_score, daily_installs, daily_uninstalls, active_devices, daily_crashes, daily_anrs, crash_rate_per_1k_devices, anr_rate_per_1k_devices, daily_churn_rate, day_1_retention_rate, day_7_retention_rate, day_30_retention_rate, daily_net_revenue, daily_transactions, avg_transaction_value, average_revenue_per_user, revenue_health_score, research_budget_usd FROM google_play__comprehensive_performance_dashboard WHERE package_name='com.dev.photoeditor' ORDER BY date_day
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-069/attempt-01/sql/S45.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-069/attempt-01/sql/S45.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-069/attempt-01/results/S45.rows.jsonl)；完整：True；SHA256：`ce51c999c91f34cc56d17c1ed0e8c34547cc5c09b8947c01a5434a012e41e8f9`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "google_play__comprehensive_performance_dashboard", "kind": "base", "block": null, "base_tables": ["google_play__comprehensive_performance_dashboard"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |


## S46

类别 `data`；来源 `python`；调用 `624d12c2e29043beb2862077ebdbb05e`；状态 `success`。

```sql
SELECT country, revenue_tier, store_conversion_rate, store_visitors_30d, store_installs_30d FROM google_play__geo_market_analysis WHERE package_name='com.dev.photoeditor'
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-069/attempt-01/sql/S46.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-069/attempt-01/sql/S46.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-069/attempt-01/results/S46.rows.jsonl)；完整：True；SHA256：`0179f31c6895df16feadf028665cd8ea9aea93331d4bf1808758aafd5baa5ed5`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "google_play__geo_market_analysis", "kind": "base", "block": null, "base_tables": ["google_play__geo_market_analysis"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |

