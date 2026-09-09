# dacomp-074

The CFO wants to build a more accurate cash flow forecasting model. Analyze the historical…

运行：已提交。官方未评分。全部 SQL 尝试/成功 26/26；数据 SQL 24/24；Python 9 次。

完整原题：

The CFO wants to build a more accurate cash flow forecasting model. Analyze the historical cash flow trajectories of subsidiaries marked with a 'High' `cash_flow_risk_level`, focusing on the changes in their key financial indicators during the 6 months prior to them entering this risk state. The specific dimensions of analysis include: revenue recognition (frequency of monthly revenue fluctuations exceeding 20%), accounts receivable management (the proportion of time `weighted_average_days_outstanding` exceeds 45 days, and instances where `overdue_percentage` rises for 3 consecutive months), and expense control (the degree of divergence between the growth rate of 'expense' account type expenditures and the revenue growth rate). By comparing the indicator trajectories of these high-risk subsidiaries with those of financially healthy subsidiaries over the same time dimensions, identify a combination of key indicators and threshold settings that can provide a 2-3 month early warning for cash flow crises.

| 表 | 行数 | 列数 |
| --- | --- | --- |
| netsuite2_financial_dashboard | 180 | 40 |
| netsuite2_income_statement | 1800 | 27 |


实际路线（分析者依据 SQL/源码概括，不代表 Agent 自述）：SQL 提取高风险子公司及历史指标 → Python 连接、构建风险前窗口和环比阈值 → 现金流预警比较。

数据库大小：307,200 字节。

## 数据 SQL

| SQL | 状态 | 基础表 | Join 输入/类型 | GROUP BY | 聚合表达式 | 结果行数 | 数据库 ms |
| --- | --- | --- | --- | --- | --- | --- | --- |
| [S3/Q1](#s3) | success | ["netsuite2_financial_dashboard"] | 0 / {} | [] | ["COUNT(*)", "COUNT(DISTINCT subsidiary_id)", "COUNT(DISTINCT accounting_period_id)", "MIN(dashboard_date)", "MAX(dashboard_date)"] | 1 | 0.52 |
| [S4/Q2](#s4) | success | ["netsuite2_financial_dashboard"] | 0 / {} | ["cash_flow_risk_level"] | ["COUNT(*)"] | 3 | 0.389 |
| [S5/Q3](#s5) | success | ["netsuite2_income_statement"] | 0 / {} | [] | ["COUNT(*)", "COUNT(DISTINCT subsidiary_id)", "COUNT(DISTINCT account_type_name)"] | 1 | 0.898 |
| [S6/Q4](#s6) | success | ["netsuite2_financial_dashboard"] | 0 / {} | [] | [] | 25 | 0.457 |
| [S7/Q5](#s7) | success | ["netsuite2_income_statement"] | 0 / {} | ["account_type_name"] | ["COUNT(*)", "SUM(converted_amount)"] | 3 | 1.036 |
| [S8/Q6](#s8) | success | ["netsuite2_income_statement"] | 0 / {} | ["subsidiary_id"] | ["COUNT(*)"] | 10 | 0.953 |
| [S9/Q7](#s9) | success | ["netsuite2_financial_dashboard"] | 0 / {} | ["subsidiary_id"] | ["COUNT(*)", "MIN(dashboard_date)", "MAX(dashboard_date)"] | 10 | 0.453 |
| [S10/Q8](#s10) | success | ["netsuite2_financial_dashboard"] | 0 / {} | ["dashboard_date"] | ["COUNT(*)"] | 18 | 0.302 |
| [S11/Q9](#s11) | success | ["netsuite2_financial_dashboard"] | 0 / {} | [] | [] | 18 | 0.294 |
| [S12/Q10](#s12) | success | ["netsuite2_financial_dashboard"] | 0 / {} | [] | [] | 18 | 0.375 |
| [S13/Q11](#s13) | success | ["netsuite2_financial_dashboard"] | 0 / {} | [] | [] | 180 | 0.553 |
| [S14/Q12](#s14) | success | ["netsuite2_financial_dashboard"] | 0 / {} | [] | [] | 18 | 0.309 |
| [S15/Q13](#s15) | success | ["netsuite2_financial_dashboard"] | 0 / {} | [] | [] | 180 | 0.46 |
| [S16/Q14](#s16) | success | ["netsuite2_income_statement"] | 0 / {} | ["accounting_period_id", "accounting_period_name", "account_type_name"] | ["COUNT(*)", "COUNT(DISTINCT account_name)"] | 30 | 2.178 |
| [S17/Q15](#s17) | success | ["netsuite2_income_statement"] | 0 / {} | [] | [] | 10 | 0.797 |
| [S18/Q16](#s18) | success | ["netsuite2_financial_dashboard"] | 0 / {} | ["financial_health_grade"] | ["COUNT(*)"] | 4 | 0.403 |
| [S19/Q17](#s19) | success | ["netsuite2_financial_dashboard"] | 0 / {} | ["cash_flow_health"] | ["COUNT(*)"] | 2 | 0.296 |
| [S20/Q18](#s20) | success | ["netsuite2_income_statement"] | 0 / {} | [] | [] | 18 | 0.77 |
| [S21/Q19](#s21) | success | ["netsuite2_income_statement"] | 0 / {} | ["account_type_name", "account_name"] | ["COUNT(*)"] | 10 | 1.374 |
| [S22/Q20](#s22) | success | ["netsuite2_financial_dashboard"] | 0 / {} | ["subsidiary_id"] | ["MIN(dashboard_date)"] | 10 | 0.447 |
| [S23/Q21](#s23) | success | ["netsuite2_financial_dashboard"] | 0 / {} | [] | [] | 180 | 1.084 |
| [S24/Q22](#s24) | success | ["netsuite2_income_statement"] | 0 / {} | ["subsidiary_id", "accounting_period_ending", "account_type_name"] | ["SUM(converted_amount)"] | 540 | 2.495 |
| [S25/Q23](#s25) | success | ["netsuite2_financial_dashboard", "netsuite2_income_statement"] | 3 / {'LEFT': 2} | ["subsidiary_id", "accounting_period_ending", "subsidiary_id", "accounting_period_ending"] | ["SUM(converted_amount)", "SUM(converted_amount)"] | 180 | 3.805 |
| [S26/Q24](#s26) | success | ["netsuite2_income_statement"] | 0 / {} | ["subsidiary_id", "accounting_period_ending", "account_name"] | ["SUM(converted_amount)"] | 720 | 2.372 |


## 元数据和设置

| SQL | 类别 | 状态 | 内容 |
| --- | --- | --- | --- |
| S1 | connection_setup | success | PRAGMA query_only=ON |
| S2 | metadata | success | SELECT name,sql FROM sqlite_master WHERE type='table' ORDER BY name |


## Python 与执行位置

人工源码审查：**database_first_violation**。Python 连接风险首日、财务指标与费用，按子公司计算滞后值和环比，按风险前窗口计算均值、阈值频率和预警敏感度/特异度。这里的常规窗口与条件聚合可由 SQLite 完成，属于明确的执行位置偏离。 [证据](../reviews/dacomp-074.json)。

P1：Load the archived per-period metric dataset (S25) plus the first-High-date mapping (S22) into pandas, compute derived metrics (revenue MoM fluctuation flags, AR flags, expense-revenue growth divergence), define each subsidiary's pre-High 6-month window and healthy (Low-risk) comparison periods, and produce comparison statistics. This is statistical aggregation/visualization beyond what a single SQL query should assemble.

[源码](../../../runs/dsv4flash-db-first-full-01/dacomp-074/attempt-01/python/P1.py)；[输出](../../../runs/dsv4flash-db-first-full-01/dacomp-074/attempt-01/python/P1.stdout)；[错误](../../../runs/dsv4flash-db-first-full-01/dacomp-074/attempt-01/python/P1.stderr)。检出需人工核验的 SQL 可实现操作：groupby(, .merge(；不能仅凭理由判为合规。

P2：Compute the three key dimension metrics (revenue fluctuation frequency, AR days outstanding & overdue rise, expense-revenue divergence) comparing pre-High 6-month windows vs. healthy (Low-risk) periods, and produce summary tables and visualization.

[源码](../../../runs/dsv4flash-db-first-full-01/dacomp-074/attempt-01/python/P2.py)；[输出](../../../runs/dsv4flash-db-first-full-01/dacomp-074/attempt-01/python/P2.stdout)；[错误](../../../runs/dsv4flash-db-first-full-01/dacomp-074/attempt-01/python/P2.stderr)。检出需人工核验的 SQL 可实现操作：groupby(, sort_values(；不能仅凭理由判为合规。

P3：Investigate the trajectory of AR metrics (DSO, overdue%) and revenue/expense around the High-risk transition, re-examine the pre-High window definition including the transition month, and build a clean pre-High vs healthy comparison. This is trajectory-level statistical analysis requiring Python.

[源码](../../../runs/dsv4flash-db-first-full-01/dacomp-074/attempt-01/python/P3.py)；[输出](../../../runs/dsv4flash-db-first-full-01/dacomp-074/attempt-01/python/P3.stdout)；[错误](../../../runs/dsv4flash-db-first-full-01/dacomp-074/attempt-01/python/P3.stderr)。检出需人工核验的 SQL 可实现操作：groupby(, sort_values(；不能仅凭理由判为合规。

P4：Refine the early warning threshold analysis: examine DSO rate of change, test alternative thresholds (DSO > 35, > 40), and identify the best combination of indicators that discriminate pre-High periods from healthy periods 2-3 months in advance. This requires iterative threshold testing and visualization beyond SQL.

[源码](../../../runs/dsv4flash-db-first-full-01/dacomp-074/attempt-01/python/P4.py)；[输出](../../../runs/dsv4flash-db-first-full-01/dacomp-074/attempt-01/python/P4.stdout)；[错误](../../../runs/dsv4flash-db-first-full-01/dacomp-074/attempt-01/python/P4.stderr)。检出需人工核验的 SQL 可实现操作：groupby(, sort_values(；不能仅凭理由判为合规。

P5：Analyze expense sub-category growth in the pre-High window vs healthy periods to identify which expense types drive the divergence, and compute a final consolidated early-warning scorecard. This is a statistical breakdown not supported by SQL alone.

[源码](../../../runs/dsv4flash-db-first-full-01/dacomp-074/attempt-01/python/P5.py)；[输出](../../../runs/dsv4flash-db-first-full-01/dacomp-074/attempt-01/python/P5.stdout)；[错误](../../../runs/dsv4flash-db-first-full-01/dacomp-074/attempt-01/python/P5.stderr)。检出需人工核验的 SQL 可实现操作：groupby(, .merge(；不能仅凭理由判为合规。

P6：Re-do expense category analysis with correct JSONL loading, and generate final early-warning scorecard and boxplots.

[源码](../../../runs/dsv4flash-db-first-full-01/dacomp-074/attempt-01/python/P6.py)；[输出](../../../runs/dsv4flash-db-first-full-01/dacomp-074/attempt-01/python/P6.stdout)；[错误](../../../runs/dsv4flash-db-first-full-01/dacomp-074/attempt-01/python/P6.stderr)。检出需人工核验的 SQL 可实现操作：groupby(, .merge(；不能仅凭理由判为合规。

P7：Determine the lead time: when DSO first crosses 35 and when revenue fluctuation signals first appear relative to each subsidiary's High transition, and compare net cash flow trends in pre-High vs healthy periods. This timing analysis supports the 2-3 month early warning recommendation and requires per-subsidiary trajectory computation in Python.

[源码](../../../runs/dsv4flash-db-first-full-01/dacomp-074/attempt-01/python/P7.py)；[输出](../../../runs/dsv4flash-db-first-full-01/dacomp-074/attempt-01/python/P7.stdout)；[错误](../../../runs/dsv4flash-db-first-full-01/dacomp-074/attempt-01/python/P7.stderr)。检出需人工核验的 SQL 可实现操作：groupby(, .merge(, sort_values(；不能仅凭理由判为合规。

P8：Compute sensitivity/specificity specifically for the 2-3 months before High (the target early-warning window) for each candidate signal and combination, and generate the final summary figure. This is the definitive threshold recommendation step.

[源码](../../../runs/dsv4flash-db-first-full-01/dacomp-074/attempt-01/python/P8.py)；[输出](../../../runs/dsv4flash-db-first-full-01/dacomp-074/attempt-01/python/P8.stdout)；[错误](../../../runs/dsv4flash-db-first-full-01/dacomp-074/attempt-01/python/P8.stderr)。检出需人工核验的 SQL 可实现操作：groupby(, sort_values(；不能仅凭理由判为合规。

P9：Fix the combination evaluation function call and complete the 2-3 month early-warning window analysis and final framework figure.

[源码](../../../runs/dsv4flash-db-first-full-01/dacomp-074/attempt-01/python/P9.py)；[输出](../../../runs/dsv4flash-db-first-full-01/dacomp-074/attempt-01/python/P9.stdout)；[错误](../../../runs/dsv4flash-db-first-full-01/dacomp-074/attempt-01/python/P9.stderr)。检出需人工核验的 SQL 可实现操作：groupby(, sort_values(；不能仅凭理由判为合规。

## 优化机会

已验证候选。筛选限于精确 SQL、相同自包含 CTE、相同单表完整过滤、可分解单表聚合；未覆盖任意 Join 等价和一般谓词蕴含。全部候选都是 offline，未测在线预测。

| 候选 | 类型 | 已有结果 | 覆盖 SQL | 后续次数 | 中间行数 | 验证 | 成本 |
| --- | --- | --- | --- | --- | --- | --- | --- |
| C1 | exact-result reuse | True | ["S12", "S14"] | 1 | unknown | not_verified_cap | Not tested |
| C2 | exact-result reuse | True | ["S13", "S15"] | 1 | 180 | verified | Not benchmarked; correctness alone does not establish net speedup. |
| C3 | aggregate MV | False | ["S4", "S9", "S10", "S18", "S19"] | 4 | 180 | verified | Not benchmarked; correctness alone does not establish net speedup. |
| C4 | aggregate MV | False | ["S7", "S21", "S24"] | 2 | 1800 | rejected_result_mismatch | Not benchmarked; correctness alone does not establish net speedup. |


已验证覆盖（含触发查询、候选并集去重）：7/24 条成功数据 SQL。正确性仅针对当前数据库快照；未测性能的候选不能声称已加速。

[完整 build/rewrite 与比较证据](dacomp-074.analysis.json)。

### C3：aggregate MV

Union of grouping keys; decomposable aggregate states; AVG uses SUM and non-NULL COUNT.

原查询 [S4](#s4), [S9](#s9), [S10](#s10), [S18](#s18), [S19](#s19) → 新增共享状态 C3 → 后续 4 次可复用。该构建点为事后假设，不代表 Agent 当时预知后续。

构建定义：

```sql
SELECT cash_flow_risk_level AS __g0, subsidiary_id AS __g1, dashboard_date AS __g2, financial_health_grade AS __g3, cash_flow_health AS __g4, COUNT(*) AS __a0, MIN(dashboard_date) AS __a1, MAX(dashboard_date) AS __a2 FROM "netsuite2_financial_dashboard"  GROUP BY cash_flow_risk_level, subsidiary_id, dashboard_date, financial_health_grade, cash_flow_health
```

受益查询 S4 的改写示例：

```sql
SELECT __g0 AS "cash_flow_risk_level", SUM(__a0) AS n FROM temp.reuse_candidate GROUP BY __g0 ORDER BY n DESC
```

| 原 SQL | 列名一致 | 结果一致 | 比较方法 |
| --- | --- | --- | --- |
| S4 | True | True | ordered_numeric_tolerance |
| S9 | True | True | exact_multiset |
| S10 | True | True | ordered_numeric_tolerance |
| S18 | True | True | ordered_numeric_tolerance |
| S19 | True | True | ordered_numeric_tolerance |


验证状态：verified；成本结论：Not benchmarked; correctness alone does not establish net speedup.

### C2：exact-result reuse

Identical normalized SQL and parameters; archive equality checked.

原查询 [S13](#s13), [S15](#s15) → 保留前序结果 S13 → 后续 1 次可复用。该构建点为事后假设，不代表 Agent 当时预知后续。

| 原 SQL | 列名一致 | 结果一致 | 比较方法 |
| --- | --- | --- | --- |
| S15 | True | True | ordered_numeric_tolerance |


验证状态：verified；成本结论：Not benchmarked; correctness alone does not establish net speedup.

### C4：aggregate MV

Union of grouping keys; decomposable aggregate states; AVG uses SUM and non-NULL COUNT.

原查询 [S7](#s7), [S21](#s21), [S24](#s24) → 新增共享状态 C4 → 后续 2 次可复用。该构建点为事后假设，不代表 Agent 当时预知后续。

构建定义：

```sql
SELECT account_type_name AS __g0, account_name AS __g1, subsidiary_id AS __g2, accounting_period_ending AS __g3, COUNT(*) AS __a0, SUM(converted_amount) AS __a1 FROM "netsuite2_income_statement"  GROUP BY account_type_name, account_name, subsidiary_id, accounting_period_ending
```

受益查询 S7 的改写示例：

```sql
SELECT __g0 AS "account_type_name", SUM(__a0) AS n, SUM(__a1) AS total FROM temp.reuse_candidate GROUP BY __g0
```

| 原 SQL | 列名一致 | 结果一致 | 比较方法 |
| --- | --- | --- | --- |
| S7 | True | False | exact_multiset |
| S21 | True | True | ordered_numeric_tolerance |
| S24 | True | True | ordered_numeric_tolerance |


验证状态：rejected_result_mismatch；成本结论：Not benchmarked; correctness alone does not establish net speedup.

结果依赖：自动记录 SQL→Python 的接口父调用，以及源码中引用归档文件的消费者；字面值相同不认定因果。模型方向选择需要人工读取消息，尚未做全面因果标注。

[原始报告](../../../runs/dsv4flash-db-first-full-01/dacomp-074/attempt-01/answer.md)；[统一消息](../../../runs/dsv4flash-db-first-full-01/dacomp-074/attempt-01/messages.jsonl)；[原始 OpenCode 事件](../../../runs/dsv4flash-db-first-full-01/dacomp-074/attempt-01/opencode.jsonl)；[SQL 引擎日志](../../../runs/dsv4flash-db-first-full-01/dacomp-074/attempt-01/sql_journal.jsonl)。

[可读报告（本地图片链接规范化）](../answers/dacomp-074.md)。原始回答保留，分析结论未改写。

## S1

类别 `connection_setup`；来源 `connection`；调用 `873a030f761342a7ba2e63cf25801a99`；状态 `success`。

```sql
PRAGMA query_only=ON
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-074/attempt-01/sql/S1.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-074/attempt-01/sql/S1.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-074/attempt-01/results/S1.rows.jsonl)；完整：True；SHA256：`e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`。

## S2

类别 `metadata`；来源 `list_db`；调用 `873a030f761342a7ba2e63cf25801a99`；状态 `success`。

```sql
SELECT name,sql FROM sqlite_master WHERE type='table' ORDER BY name
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-074/attempt-01/sql/S2.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-074/attempt-01/sql/S2.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-074/attempt-01/results/S2.rows.jsonl)；完整：True；SHA256：`1fadf8195b5c7a158614b29f60e446964dd0cb558b6ac062f94b00509388baf5`。

## S3

类别 `data`；来源 `query_db`；调用 `e3c4277e692e445b9a355ed282476f1a`；状态 `success`。

```sql
SELECT COUNT(*) AS n_rows, COUNT(DISTINCT subsidiary_id) AS n_subs, COUNT(DISTINCT accounting_period_id) AS n_periods, MIN(dashboard_date) AS min_date, MAX(dashboard_date) AS max_date FROM netsuite2_financial_dashboard
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-074/attempt-01/sql/S3.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-074/attempt-01/sql/S3.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-074/attempt-01/results/S3.rows.jsonl)；完整：True；SHA256：`575159e9eac6c9fdd437705345f9ae1192f18e9ff1413c774ea935eaddff5255`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "netsuite2_financial_dashboard", "kind": "base", "block": null, "base_tables": ["netsuite2_financial_dashboard"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |
| B1 | COUNT(DISTINCT subsidiary_id) | [{"table": "netsuite2_financial_dashboard", "column": "subsidiary_id"}] | [] | False |
| B1 | COUNT(DISTINCT accounting_period_id) | [{"table": "netsuite2_financial_dashboard", "column": "accounting_period_id"}] | [] | False |
| B1 | MIN(dashboard_date) | [{"table": "netsuite2_financial_dashboard", "column": "dashboard_date"}] | [] | False |
| B1 | MAX(dashboard_date) | [{"table": "netsuite2_financial_dashboard", "column": "dashboard_date"}] | [] | False |


## S4

类别 `data`；来源 `query_db`；调用 `3993b929bf7147b98e1c5a524c28a8ec`；状态 `success`。

```sql
SELECT cash_flow_risk_level, COUNT(*) AS n FROM netsuite2_financial_dashboard GROUP BY cash_flow_risk_level ORDER BY n DESC
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-074/attempt-01/sql/S4.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-074/attempt-01/sql/S4.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-074/attempt-01/results/S4.rows.jsonl)；完整：True；SHA256：`91fa519637b6db995a217ad314a2b603912c14f513fef3e6b38376ffd3b843db`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "netsuite2_financial_dashboard", "kind": "base", "block": null, "base_tables": ["netsuite2_financial_dashboard"]}] | [] | ["cash_flow_risk_level"] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |


## S5

类别 `data`；来源 `query_db`；调用 `54e63f2191724df98ac56da4326f433e`；状态 `success`。

```sql
SELECT COUNT(*) AS n_rows, COUNT(DISTINCT subsidiary_id) AS n_subs, COUNT(DISTINCT account_type_name) AS n_types FROM netsuite2_income_statement
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-074/attempt-01/sql/S5.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-074/attempt-01/sql/S5.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-074/attempt-01/results/S5.rows.jsonl)；完整：True；SHA256：`379089365c83dc49a39470bd009c54c9d5797e284950e62f95056e4db66a02d1`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "netsuite2_income_statement", "kind": "base", "block": null, "base_tables": ["netsuite2_income_statement"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |
| B1 | COUNT(DISTINCT subsidiary_id) | [{"table": "netsuite2_income_statement", "column": "subsidiary_id"}] | [] | False |
| B1 | COUNT(DISTINCT account_type_name) | [{"table": "netsuite2_income_statement", "column": "account_type_name"}] | [] | False |


## S6

类别 `data`；来源 `query_db`；调用 `ed631e80410f443990e83485fd814cea`；状态 `success`。

```sql
SELECT accounting_period_id, dashboard_date, subsidiary_id, cash_flow_risk_level FROM netsuite2_financial_dashboard ORDER BY dashboard_date LIMIT 25
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-074/attempt-01/sql/S6.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-074/attempt-01/sql/S6.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-074/attempt-01/results/S6.rows.jsonl)；完整：True；SHA256：`9237e19c0bed1683dfc7ba9a331addc113e6ae45770af946955863e595656468`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "netsuite2_financial_dashboard", "kind": "base", "block": null, "base_tables": ["netsuite2_financial_dashboard"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |


## S7

类别 `data`；来源 `query_db`；调用 `793d5537e56d440881b3a1c4916a907e`；状态 `success`。

```sql
SELECT account_type_name, COUNT(*) AS n, SUM(converted_amount) AS total FROM netsuite2_income_statement GROUP BY account_type_name
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-074/attempt-01/sql/S7.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-074/attempt-01/sql/S7.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-074/attempt-01/results/S7.rows.jsonl)；完整：True；SHA256：`009c0effb6751feec6ac703bb09493d6cbb778b1bf2ff3671c0893ace1756d5c`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "netsuite2_income_statement", "kind": "base", "block": null, "base_tables": ["netsuite2_income_statement"]}] | [] | ["account_type_name"] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |
| B1 | SUM(converted_amount) | [{"table": "netsuite2_income_statement", "column": "converted_amount"}] | [] | False |


## S8

类别 `data`；来源 `query_db`；调用 `aecd6e7203e44c7f9dc212aa926d1eca`；状态 `success`。

```sql
SELECT subsidiary_id, subsidiary_name, COUNT(*) AS n FROM netsuite2_income_statement GROUP BY subsidiary_id ORDER BY subsidiary_id LIMIT 20
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-074/attempt-01/sql/S8.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-074/attempt-01/sql/S8.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-074/attempt-01/results/S8.rows.jsonl)；完整：True；SHA256：`44ceffc108c928c58b0d84d208cb63ad7bb110bf15eedb86a876c97dc8d6a6dd`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "netsuite2_income_statement", "kind": "base", "block": null, "base_tables": ["netsuite2_income_statement"]}] | [] | ["subsidiary_id"] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |


## S9

类别 `data`；来源 `query_db`；调用 `b4402143a9e84e91be8913acd72cb4d7`；状态 `success`。

```sql
SELECT subsidiary_id, COUNT(*) AS n, MIN(dashboard_date) AS min_d, MAX(dashboard_date) AS max_d FROM netsuite2_financial_dashboard GROUP BY subsidiary_id
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-074/attempt-01/sql/S9.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-074/attempt-01/sql/S9.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-074/attempt-01/results/S9.rows.jsonl)；完整：True；SHA256：`ea2698d4811846c55d4a63df481fed8a72833fdf40dfc37d5d608d4402e481c4`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "netsuite2_financial_dashboard", "kind": "base", "block": null, "base_tables": ["netsuite2_financial_dashboard"]}] | [] | ["subsidiary_id"] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |
| B1 | MIN(dashboard_date) | [{"table": "netsuite2_financial_dashboard", "column": "dashboard_date"}] | [] | False |
| B1 | MAX(dashboard_date) | [{"table": "netsuite2_financial_dashboard", "column": "dashboard_date"}] | [] | False |


## S10

类别 `data`；来源 `query_db`；调用 `7bae7dc3c55b4f76b39c441f2f3482e6`；状态 `success`。

```sql
SELECT dashboard_date, COUNT(*) AS n FROM netsuite2_financial_dashboard GROUP BY dashboard_date ORDER BY dashboard_date
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-074/attempt-01/sql/S10.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-074/attempt-01/sql/S10.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-074/attempt-01/results/S10.rows.jsonl)；完整：True；SHA256：`96acdb4257ddf8d1f43959076bdb09438cf3f45deb75d4f4f9065000409ddf6b`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "netsuite2_financial_dashboard", "kind": "base", "block": null, "base_tables": ["netsuite2_financial_dashboard"]}] | [] | ["dashboard_date"] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |


## S11

类别 `data`；来源 `query_db`；调用 `b3c6f15c3aac46f681ce56688dac4d1f`；状态 `success`。

```sql
SELECT subsidiary_id, dashboard_date, cash_flow_risk_level, cash_flow_health, total_risk_score, overall_financial_health_score FROM netsuite2_financial_dashboard WHERE subsidiary_id='NET18925086954' ORDER BY dashboard_date
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-074/attempt-01/sql/S11.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-074/attempt-01/sql/S11.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-074/attempt-01/results/S11.rows.jsonl)；完整：True；SHA256：`6d339568743843179452eb2d064bafcd4a279688c6ad4e8d907667086da6f76d`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "netsuite2_financial_dashboard", "kind": "base", "block": null, "base_tables": ["netsuite2_financial_dashboard"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |


## S12

类别 `data`；来源 `query_db`；调用 `6e3255acddf14efe985177e99dfffe5e`；状态 `success`。

```sql
SELECT DISTINCT dashboard_date FROM netsuite2_financial_dashboard ORDER BY dashboard_date
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-074/attempt-01/sql/S12.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-074/attempt-01/sql/S12.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-074/attempt-01/results/S12.rows.jsonl)；完整：True；SHA256：`61e75f28321815ab169e6f1d6e04a08b8d5a10919a2981bc77c72e306efbaa0a`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "netsuite2_financial_dashboard", "kind": "base", "block": null, "base_tables": ["netsuite2_financial_dashboard"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |


## S13

类别 `data`；来源 `query_db`；调用 `a387adf622de4726a67cc0842d22df27`；状态 `success`。

```sql
SELECT subsidiary_id, dashboard_date, cash_flow_risk_level FROM netsuite2_financial_dashboard ORDER BY subsidiary_id, dashboard_date
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-074/attempt-01/sql/S13.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-074/attempt-01/sql/S13.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-074/attempt-01/results/S13.rows.jsonl)；完整：True；SHA256：`6ee33ec8895352e676ff587f5f33b137375edea8223b9d2875d82f2c1a81167e`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "netsuite2_financial_dashboard", "kind": "base", "block": null, "base_tables": ["netsuite2_financial_dashboard"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |


## S14

类别 `data`；来源 `query_db`；调用 `911338a0e42d4011979a244d1f56e9ca`；状态 `success`。

```sql
SELECT DISTINCT dashboard_date FROM netsuite2_financial_dashboard ORDER BY dashboard_date
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-074/attempt-01/sql/S14.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-074/attempt-01/sql/S14.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-074/attempt-01/results/S14.rows.jsonl)；完整：True；SHA256：`61e75f28321815ab169e6f1d6e04a08b8d5a10919a2981bc77c72e306efbaa0a`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "netsuite2_financial_dashboard", "kind": "base", "block": null, "base_tables": ["netsuite2_financial_dashboard"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |


## S15

类别 `data`；来源 `query_db`；调用 `de2b847ee21448029de0c6ea98375fdf`；状态 `success`。

```sql
SELECT subsidiary_id, dashboard_date, cash_flow_risk_level FROM netsuite2_financial_dashboard ORDER BY subsidiary_id, dashboard_date
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-074/attempt-01/sql/S15.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-074/attempt-01/sql/S15.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-074/attempt-01/results/S15.rows.jsonl)；完整：True；SHA256：`6ee33ec8895352e676ff587f5f33b137375edea8223b9d2875d82f2c1a81167e`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "netsuite2_financial_dashboard", "kind": "base", "block": null, "base_tables": ["netsuite2_financial_dashboard"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |


## S16

类别 `data`；来源 `query_db`；调用 `f529b8ab07c24d7da2df8bc82bd0906a`；状态 `success`。

```sql
SELECT accounting_period_id, accounting_period_name, accounting_period_ending, account_type_name, COUNT(*) AS n, COUNT(DISTINCT account_name) AS n_acc FROM netsuite2_income_statement GROUP BY accounting_period_id, accounting_period_name, account_type_name ORDER BY accounting_period_ending LIMIT 30
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-074/attempt-01/sql/S16.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-074/attempt-01/sql/S16.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-074/attempt-01/results/S16.rows.jsonl)；完整：True；SHA256：`b8a1af7e83ddee7e1a055b636d6196b204bf64859645686fdf83aa48b66dbfe3`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "netsuite2_income_statement", "kind": "base", "block": null, "base_tables": ["netsuite2_income_statement"]}] | [] | ["accounting_period_id", "accounting_period_name", "account_type_name"] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |
| B1 | COUNT(DISTINCT account_name) | [{"table": "netsuite2_income_statement", "column": "account_name"}] | [] | False |


## S17

类别 `data`；来源 `query_db`；调用 `0cd7a45b907b45f4993bf60f88ef5cfa`；状态 `success`。

```sql
SELECT * FROM netsuite2_income_statement WHERE subsidiary_id='NET03901813602' AND account_type_name='Revenue' ORDER BY accounting_period_ending LIMIT 10
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-074/attempt-01/sql/S17.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-074/attempt-01/sql/S17.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-074/attempt-01/results/S17.rows.jsonl)；完整：True；SHA256：`c930188a2b2248ea67d05344b171856631ed9cf2e5d9ff7a9ba4315ca9cbc370`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "netsuite2_income_statement", "kind": "base", "block": null, "base_tables": ["netsuite2_income_statement"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |


## S18

类别 `data`；来源 `query_db`；调用 `943123d6ca9f419684f4ea715e6a3fef`；状态 `success`。

```sql
SELECT financial_health_grade, COUNT(*) n FROM netsuite2_financial_dashboard GROUP BY financial_health_grade ORDER BY n DESC
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-074/attempt-01/sql/S18.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-074/attempt-01/sql/S18.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-074/attempt-01/results/S18.rows.jsonl)；完整：True；SHA256：`0959797e05a4ab90531a26473c608927d735f2be52cf9680f32a15822e04ffe5`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "netsuite2_financial_dashboard", "kind": "base", "block": null, "base_tables": ["netsuite2_financial_dashboard"]}] | [] | ["financial_health_grade"] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |


## S19

类别 `data`；来源 `query_db`；调用 `3d6d059161c045459e7c5b4646af4277`；状态 `success`。

```sql
SELECT cash_flow_health, COUNT(*) n FROM netsuite2_financial_dashboard GROUP BY cash_flow_health ORDER BY n DESC
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-074/attempt-01/sql/S19.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-074/attempt-01/sql/S19.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-074/attempt-01/results/S19.rows.jsonl)；完整：True；SHA256：`21e4d587035e6bc3b57a576b1b1b26d5c2f826196027ff63c44e496930d7961a`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "netsuite2_financial_dashboard", "kind": "base", "block": null, "base_tables": ["netsuite2_financial_dashboard"]}] | [] | ["cash_flow_health"] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |


## S20

类别 `data`；来源 `query_db`；调用 `67e536d98ed04bfa9d00deb7a9bc5500`；状态 `success`。

```sql
SELECT DISTINCT accounting_period_ending, accounting_period_name FROM netsuite2_income_statement ORDER BY accounting_period_ending
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-074/attempt-01/sql/S20.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-074/attempt-01/sql/S20.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-074/attempt-01/results/S20.rows.jsonl)；完整：True；SHA256：`5d549fd7429e712c8b832eb1a02c29759a07eb3268d6246913631c1650c36636`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "netsuite2_income_statement", "kind": "base", "block": null, "base_tables": ["netsuite2_income_statement"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |


## S21

类别 `data`；来源 `query_db`；调用 `b92bae9f7ea548ad8fbb90aa0c103040`；状态 `success`。

```sql
SELECT account_type_name, account_name, COUNT(*) AS n FROM netsuite2_income_statement GROUP BY account_type_name, account_name ORDER BY account_type_name, n DESC
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-074/attempt-01/sql/S21.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-074/attempt-01/sql/S21.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-074/attempt-01/results/S21.rows.jsonl)；完整：True；SHA256：`162587c8359df9fb467a2c96cc0923c66972756b122d225f3947d12520cc5c8c`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "netsuite2_income_statement", "kind": "base", "block": null, "base_tables": ["netsuite2_income_statement"]}] | [] | ["account_type_name", "account_name"] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |


## S22

类别 `data`；来源 `query_db`；调用 `f10351c4af0c414bb1fb0bd329e16df7`；状态 `success`。

```sql
SELECT subsidiary_id, MIN(dashboard_date) AS first_high_date FROM netsuite2_financial_dashboard WHERE cash_flow_risk_level = 'High' GROUP BY subsidiary_id ORDER BY first_high_date
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-074/attempt-01/sql/S22.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-074/attempt-01/sql/S22.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-074/attempt-01/results/S22.rows.jsonl)；完整：True；SHA256：`126de611410b75ef0c9b280730e15c6a398f36883b78f03f44dfc9bd147ca645`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "netsuite2_financial_dashboard", "kind": "base", "block": null, "base_tables": ["netsuite2_financial_dashboard"]}] | [] | ["subsidiary_id"] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | MIN(dashboard_date) | [{"table": "netsuite2_financial_dashboard", "column": "dashboard_date"}] | [] | False |


## S23

类别 `data`；来源 `query_db`；调用 `7d4aa77f34dc4b5489491a75c8552b18`；状态 `success`。

```sql
SELECT subsidiary_id, dashboard_date, cash_flow_risk_level, cash_flow_health, overall_financial_health_score, financial_health_grade, operating_cash_flow, net_cash_flow, overdue_percentage, weighted_average_days_outstanding, total_ar_amount, overdue_amount, total_risk_score, current_ratio, quick_ratio, net_profit_margin, gross_margin_ratio, return_on_equity FROM netsuite2_financial_dashboard ORDER BY subsidiary_id, dashboard_date
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-074/attempt-01/sql/S23.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-074/attempt-01/sql/S23.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-074/attempt-01/results/S23.rows.jsonl)；完整：True；SHA256：`03642a3901399a4733e9c0233f839ff045eb0082deaf91575eebbc9e374a1ae4`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "netsuite2_financial_dashboard", "kind": "base", "block": null, "base_tables": ["netsuite2_financial_dashboard"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |


## S24

类别 `data`；来源 `query_db`；调用 `29c0c0b41c2c42fc894c524a7aa200d6`；状态 `success`。

```sql
SELECT subsidiary_id, accounting_period_ending, account_type_name, SUM(converted_amount) AS total_amount FROM netsuite2_income_statement GROUP BY subsidiary_id, accounting_period_ending, account_type_name ORDER BY subsidiary_id, accounting_period_ending, account_type_name
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-074/attempt-01/sql/S24.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-074/attempt-01/sql/S24.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-074/attempt-01/results/S24.rows.jsonl)；完整：True；SHA256：`175a8bb7442795d7d65e044ce77dd3c82af84d610e2f37482bdbfc37e17fa065`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "netsuite2_income_statement", "kind": "base", "block": null, "base_tables": ["netsuite2_income_statement"]}] | [] | ["subsidiary_id", "accounting_period_ending", "account_type_name"] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | SUM(converted_amount) | [{"table": "netsuite2_income_statement", "column": "converted_amount"}] | [] | False |


## S25

类别 `data`；来源 `query_db`；调用 `30abe3d75b4143d99904b9736ccfe8d1`；状态 `success`。

```sql

WITH per_sub AS (
  SELECT subsidiary_id, dashboard_date,
         ROW_NUMBER() OVER (PARTITION BY subsidiary_id ORDER BY dashboard_date) AS period_idx,
         cash_flow_risk_level, weighted_average_days_outstanding, overdue_percentage
  FROM netsuite2_financial_dashboard
),
rev AS (
  SELECT subsidiary_id, accounting_period_ending, SUM(converted_amount) AS revenue
  FROM netsuite2_income_statement WHERE account_type_name='Revenue' GROUP BY 1,2
),
exp AS (
  SELECT subsidiary_id, accounting_period_ending, SUM(converted_amount) AS expense
  FROM netsuite2_income_statement WHERE account_type_name='Expense' GROUP BY 1,2
),
joined AS (
  SELECT d.subsidiary_id, d.dashboard_date, d.period_idx, d.cash_flow_risk_level,
         d.weighted_average_days_outstanding, d.overdue_percentage,
         r.revenue, e.expense
  FROM per_sub d
  LEFT JOIN rev r ON r.subsidiary_id=d.subsidiary_id AND r.accounting_period_ending=d.dashboard_date
  LEFT JOIN exp e ON e.subsidiary_id=d.subsidiary_id AND e.accounting_period_ending=d.dashboard_date
)
SELECT subsidiary_id, dashboard_date, period_idx, cash_flow_risk_level,
       weighted_average_days_outstanding, overdue_percentage, revenue, expense,
       LAG(revenue) OVER w AS prev_revenue,
       LAG(expense) OVER w AS prev_expense,
       LAG(overdue_percentage) OVER w AS prev_overdue,
       LAG(overdue_percentage,2) OVER w AS prev2_overdue
FROM joined
WINDOW w AS (PARTITION BY subsidiary_id ORDER BY dashboard_date)
ORDER BY subsidiary_id, period_idx

```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-074/attempt-01/sql/S25.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-074/attempt-01/sql/S25.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-074/attempt-01/results/S25.rows.jsonl)；完整：True；SHA256：`fb6cc5858709701afef57850e766b24ba9679084a0d4477e74784f0c886a2f4c`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "netsuite2_financial_dashboard", "kind": "base", "block": null, "base_tables": ["netsuite2_financial_dashboard"]}] | [] | [] |
| B2 | [{"alias": "netsuite2_income_statement", "kind": "base", "block": null, "base_tables": ["netsuite2_income_statement"]}] | [] | ["subsidiary_id", "accounting_period_ending"] |
| B3 | [{"alias": "netsuite2_income_statement", "kind": "base", "block": null, "base_tables": ["netsuite2_income_statement"]}] | [] | ["subsidiary_id", "accounting_period_ending"] |
| B4 | [{"alias": "d", "kind": "derived", "block": "B1", "base_tables": ["netsuite2_financial_dashboard"]}, {"alias": "r", "kind": "derived", "block": "B2", "base_tables": ["netsuite2_income_statement"]}, {"alias": "e", "kind": "derived", "block": "B3", "base_tables": ["netsuite2_income_statement"]}] | [{"type": "LEFT", "right": "rev AS r", "on": "r.subsidiary_id = d.subsidiary_id AND r.accounting_period_ending = d.dashboard_date", "using": []}, {"type": "LEFT", "right": "exp AS e", "on": "e.subsidiary_id = d.subsidiary_id AND e.accounting_period_ending = d.dashboard_date", "using": []}] | [] |
| B5 | [{"alias": "joined", "kind": "derived", "block": "B4", "base_tables": ["netsuite2_financial_dashboard", "netsuite2_income_statement"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B2 | SUM(converted_amount) | [{"table": "netsuite2_income_statement", "column": "converted_amount"}] | [] | False |
| B3 | SUM(converted_amount) | [{"table": "netsuite2_income_statement", "column": "converted_amount"}] | [] | False |


## S26

类别 `data`；来源 `query_db`；调用 `b7a6166091b64d5b9fa1826204d14452`；状态 `success`。

```sql
SELECT subsidiary_id, accounting_period_ending, account_name, SUM(converted_amount) AS amount FROM netsuite2_income_statement WHERE account_type_name='Expense' GROUP BY subsidiary_id, accounting_period_ending, account_name ORDER BY subsidiary_id, accounting_period_ending, account_name
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-074/attempt-01/sql/S26.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-074/attempt-01/sql/S26.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-074/attempt-01/results/S26.rows.jsonl)；完整：True；SHA256：`b6d2685e60cc9dc90e4e9cde788412ebc05fdb3669c5cf800a48cb4f83c46c80`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "netsuite2_income_statement", "kind": "base", "block": null, "base_tables": ["netsuite2_income_statement"]}] | [] | ["subsidiary_id", "accounting_period_ending", "account_name"] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | SUM(converted_amount) | [{"table": "netsuite2_income_statement", "column": "converted_amount"}] | [] | False |

