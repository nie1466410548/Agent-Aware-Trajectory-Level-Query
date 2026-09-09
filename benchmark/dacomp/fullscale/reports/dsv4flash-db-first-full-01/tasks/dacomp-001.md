# dacomp-001

Below are our bank’s collected credit and operating data for small, micro, and medium ente…

运行：已提交。官方未评分。全部 SQL 尝试/成功 28/28；数据 SQL 26/26；Python 8 次。

完整原题：

Below are our bank’s collected credit and operating data for small, micro, and medium enterprises. Using existing Credit Ratings, revenue capacity, profit stability, and upstream/downstream dependency, perform a quantitative analysis of the credit risk of enterprises with credit histories.
Assume our bank’s annual total credit is RMB 100 million. Incorporating churn rates, design an allocation plan for credit limits and interest rates, and explain in detail the rules by which the limits and rates vary with risk levels.

| 表 | 行数 | 列数 |
| --- | --- | --- |
| annual_rate_&_churn | 29 | 4 |
| ch___company_info | 123 | 4 |
| ch___input_invoices | 210947 | 8 |
| ch___sales_invoices | 162484 | 8 |
| nch___company_info | 302 | 2 |
| nch___input_invoices | 395175 | 8 |
| nch___sales_invoices | 330835 | 8 |


实际路线（分析者依据 SQL/源码概括，不代表 Agent 自述）：S3："annual_rate_&_churn" 查询 → S8：ch___sales_invoices 查询 → S13：ch___company_info/ch___sales_invoices 分组聚合 → S18：ch___company_info/ch___input_invoices/ch___sales_invoices 分组聚合 → S23："annual_rate_&_churn" 查询 → S28："annual_rate_&_churn" 查询（等距列出六个结构节点，全部步骤见下表）

数据库大小：164,876,288 字节。

## 数据 SQL

| SQL | 状态 | 基础表 | Join 输入/类型 | GROUP BY | 聚合表达式 | 结果行数 | 数据库 ms |
| --- | --- | --- | --- | --- | --- | --- | --- |
| [S3/Q1](#s3) | success | ["\"annual_rate_&_churn\""] | 0 / {} | [] | [] | 29 | 0.744 |
| [S4/Q2](#s4) | success | ["ch___company_info"] | 0 / {} | [] | [] | 123 | 0.585 |
| [S5/Q3](#s5) | success | ["nch___company_info"] | 0 / {} | [] | [] | 302 | 0.533 |
| [S6/Q4](#s6) | success | ["\"annual_rate_&_churn\""] | 0 / {} | [] | [] | 29 | 0.51 |
| [S7/Q5](#s7) | success | ["ch___company_info"] | 0 / {} | ["\"Credit Rating\""] | ["COUNT(*)", "SUM(CASE WHEN \"Defaulted\" = 'Yes' THEN 1 ELSE 0 END)"] | 4 | 0.393 |
| [S8/Q6](#s8) | success | ["ch___sales_invoices"] | 0 / {} | [] | ["COUNT(*)", "MIN(\"Invoice Date\")", "MAX(\"Invoice Date\")"] | 1 | 24.299 |
| [S9/Q7](#s9) | success | ["ch___input_invoices"] | 0 / {} | [] | ["COUNT(*)", "MIN(\"Invoice Date\")", "MAX(\"Invoice Date\")"] | 1 | 39.614 |
| [S10/Q8](#s10) | success | ["ch___sales_invoices"] | 0 / {} | ["\"Invoice Status\""] | ["COUNT(*)"] | 3 | 81.478 |
| [S11/Q9](#s11) | success | ["ch___input_invoices"] | 0 / {} | ["\"Invoice Status\""] | ["COUNT(*)"] | 2 | 78.157 |
| [S12/Q10](#s12) | success | ["nch___sales_invoices"] | 0 / {} | ["\"Invoice Status\""] | ["COUNT(*)"] | 3 | 117.782 |
| [S13/Q11](#s13) | success | ["ch___company_info", "ch___sales_invoices"] | 2 / {'LEFT': 1} | ["ci.\"Enterprise Code\""] | ["SUM(s.\"Amount Including Tax\")"] | 123 | 280.03 |
| [S14/Q12](#s14) | success | ["ch___company_info", "ch___input_invoices"] | 2 / {'LEFT': 1} | ["ci.\"Enterprise Code\""] | ["SUM(i.\"Amount Including Tax\")"] | 123 | 394.506 |
| [S15/Q13](#s15) | success | ["ch___company_info", "ch___sales_invoices"] | 2 / {'INNER': 1} | ["ci.\"Enterprise Code\"", "STRFTIME('%Y', s.\"Invoice Date\")"] | ["SUM(s.\"Amount Including Tax\")"] | 434 | 191.253 |
| [S16/Q14](#s16) | success | ["ch___sales_invoices"] | 2 / {'INNER': 1} | ["s.\"Enterprise Code\"", "s.\"Buyer organization code\"", "\"Enterprise Code\"", "c.code"] | ["SUM(s.\"Amount Including Tax\")", "SUM(\"Amount Including Tax\")", "COUNT(c.partner)", "MAX(c.amt)"] | 123 | 220.285 |
| [S17/Q15](#s17) | success | ["ch___input_invoices"] | 2 / {'INNER': 1} | ["i.\"Enterprise Code\"", "i.\"Seller Organization Code\"", "\"Enterprise Code\"", "s.code"] | ["SUM(i.\"Amount Including Tax\")", "SUM(\"Amount Including Tax\")", "COUNT(s.partner)", "MAX(s.amt)"] | 123 | 288.924 |
| [S18/Q16](#s18) | success | ["ch___company_info", "ch___input_invoices", "ch___sales_invoices"] | 5 / {'INNER': 2, 'LEFT': 4} | ["\"Enterprise Code\"", "\"Enterprise Code\"", "s.\"Enterprise Code\"", "s.\"Buyer organization code\"", "\"Enterprise Code\"", "c.code", "i.\"Enterprise Code\"", "i.\"Seller Organization Code\"", "\"Enterprise Code\"", "s.code"] | ["SUM(\"Amount Including Tax\")", "SUM(\"Amount Including Tax\")", "SUM(s.\"Amount Including Tax\")", "SUM(\"Amount Including Tax\")", "MAX(c.amt)", "SUM(i.\"Amount Including Tax\")", "SUM(\"Amount Including Tax\")", "MAX(s.amt)"] | 123 | 652.726 |
| [S19/Q17](#s19) | success | ["ch___company_info", "ch___input_invoices", "ch___sales_invoices"] | 3 / {'LEFT': 2} | ["\"Enterprise Code\"", "\"Enterprise Code\"", "ci.\"Credit Rating\""] | ["SUM(\"Amount Including Tax\")", "SUM(\"Amount Including Tax\")", "COUNT(*)", "SUM(CASE WHEN ci.\"Defaulted\" = 'Yes' THEN 1 ELSE 0 END)", "AVG(rev.total_revenue)", "AVG(CASE WHEN rev.total_revenue > 0 THEN (rev.total_revenue - COALESCE(inp.total_input, 0)) / rev.total_revenue ELSE NULL END)", "MIN(rev.total_revenue)", "MAX(rev.total_revenue)"] | 4 | 148.727 |
| [S20/Q18](#s20) | success | ["ch___company_info", "ch___input_invoices", "ch___sales_invoices"] | 5 / {'INNER': 2, 'LEFT': 4} | ["\"Enterprise Code\"", "\"Enterprise Code\"", "s.\"Enterprise Code\"", "s.\"Buyer organization code\"", "\"Enterprise Code\"", "c.code", "i.\"Enterprise Code\"", "i.\"Seller Organization Code\"", "\"Enterprise Code\"", "s.code"] | ["SUM(\"Amount Including Tax\")", "SUM(\"Amount Including Tax\")", "SUM(s.\"Amount Including Tax\")", "SUM(\"Amount Including Tax\")", "MAX(c.amt)", "SUM(i.\"Amount Including Tax\")", "SUM(\"Amount Including Tax\")", "MAX(s.amt)"] | 123 | 645.301 |
| [S21/Q19](#s21) | success | ["ch___sales_invoices"] | 0 / {} | ["\"Enterprise Code\"", "STRFTIME('%Y', \"Invoice Date\")"] | ["SUM(\"Amount Including Tax\")"] | 434 | 133.633 |
| [S22/Q20](#s22) | success | ["\"annual_rate_&_churn\""] | 0 / {} | [] | [] | 29 | 0.318 |
| [S23/Q21](#s23) | success | ["\"annual_rate_&_churn\""] | 0 / {} | [] | [] | 29 | 0.376 |
| [S24/Q22](#s24) | success | ["\"annual_rate_&_churn\""] | 0 / {} | [] | [] | 29 | 0.306 |
| [S25/Q23](#s25) | success | ["\"annual_rate_&_churn\""] | 0 / {} | [] | [] | 29 | 0.314 |
| [S26/Q24](#s26) | success | ["ch___input_invoices", "nch___company_info"] | 0 / {} | [] | ["COUNT(DISTINCT i.\"Seller Organization Code\")"] | 1 | 56.621 |
| [S27/Q25](#s27) | success | ["ch___sales_invoices", "nch___company_info"] | 0 / {} | [] | ["COUNT(DISTINCT s.\"Buyer organization code\")"] | 1 | 45.095 |
| [S28/Q26](#s28) | success | ["\"annual_rate_&_churn\""] | 0 / {} | [] | [] | 29 | 0.317 |


## 元数据和设置

| SQL | 类别 | 状态 | 内容 |
| --- | --- | --- | --- |
| S1 | connection_setup | success | PRAGMA query_only=ON |
| S2 | metadata | success | SELECT name,sql FROM sqlite_master WHERE type='table' ORDER BY name |


## Python 与执行位置

人工源码审查：**database_first_violation**。Python performs joins/groupby, weighted scoring, conditional allocation and element-wise portfolio arithmetic supported by SQLite. Reasons cite verbosity or convenience rather than unavailable SQL functionality. Plot rendering is allowed, but these preprocessing/scenario steps violate database_first_v1. Failed Python fixes belong to this same primary attempt, not whole-task reruns. [证据](../reviews/dacomp-001.json)。

P1：Building the analysis dataset in Python: combining company metrics (revenue, input, margins, concentration) with yearly revenue data to compute profit stability (coefficient of variation). SQL can't easily compute per-company CV across years without verbose pivoting, and we need a single in-memory dataset for statistical modeling and visualization.

[源码](../../../runs/dsv4flash-db-first-full-01/dacomp-001/attempt-01/python/P1.py)；[输出](../../../runs/dsv4flash-db-first-full-01/dacomp-001/attempt-01/python/P1.stdout)；[错误](../../../runs/dsv4flash-db-first-full-01/dacomp-001/attempt-01/python/P1.stderr)。检出需人工核验的 SQL 可实现操作：groupby(, .merge(, .query(；不能仅凭理由判为合规。

P2：Computing the risk score model and credit allocation plan outside SQL because we need to combine multiple metrics into a weighted risk score, perform statistical analysis, and simulate credit allocation under the total 100M budget constraint, which involves iterative calculations better suited to Python.

[源码](../../../runs/dsv4flash-db-first-full-01/dacomp-001/attempt-01/python/P2.py)；[输出](../../../runs/dsv4flash-db-first-full-01/dacomp-001/attempt-01/python/P2.stdout)；[错误](../../../runs/dsv4flash-db-first-full-01/dacomp-001/attempt-01/python/P2.stderr)。检出需人工核验的 SQL 可实现操作：groupby(, .query(；不能仅凭理由判为合规。

P3：Fixing the earlier error: categorical dtype cannot be used in arithmetic operations. Will convert risk_tier to string before mapping adjustments, and re-run the complete credit allocation and interest rate design.

[源码](../../../runs/dsv4flash-db-first-full-01/dacomp-001/attempt-01/python/P3.py)；[输出](../../../runs/dsv4flash-db-first-full-01/dacomp-001/attempt-01/python/P3.stdout)；[错误](../../../runs/dsv4flash-db-first-full-01/dacomp-001/attempt-01/python/P3.stderr)。检出需人工核验的 SQL 可实现操作：groupby(, .query(；不能仅凭理由判为合规。

P4：Computing portfolio-level expected income and churn-adjusted expected return to validate the economic viability of the allocation plan, as this requires element-wise multiplication and summation across all companies.

[源码](../../../runs/dsv4flash-db-first-full-01/dacomp-001/attempt-01/python/P4.py)；[输出](../../../runs/dsv4flash-db-first-full-01/dacomp-001/attempt-01/python/P4.stdout)；[错误](../../../runs/dsv4flash-db-first-full-01/dacomp-001/attempt-01/python/P4.stderr)。检出需人工核验的 SQL 可实现操作：.query(；不能仅凭理由判为合规。

P5：Refining the allocation: D-rated companies all defaulted (100% default rate), so lending to them guarantees losses. Compute a revised plan that denies new credit to D-rated (defaulted) firms and re-allocates the 100M budget across A/B/C rated firms, with portfolio expected return validation.

[源码](../../../runs/dsv4flash-db-first-full-01/dacomp-001/attempt-01/python/P5.py)；[输出](../../../runs/dsv4flash-db-first-full-01/dacomp-001/attempt-01/python/P5.stdout)；[错误](../../../runs/dsv4flash-db-first-full-01/dacomp-001/attempt-01/python/P5.stderr)。检出需人工核验的 SQL 可实现操作：groupby(, .query(；不能仅凭理由判为合规。

P6：Visualizing the optimal interest rate selection more clearly, showing the trade-off between rate and churn, and computing the detailed expected return curves for each rating.

[源码](../../../runs/dsv4flash-db-first-full-01/dacomp-001/attempt-01/python/P6.py)；[输出](../../../runs/dsv4flash-db-first-full-01/dacomp-001/attempt-01/python/P6.stdout)；[错误](../../../runs/dsv4flash-db-first-full-01/dacomp-001/attempt-01/python/P6.stderr)。检出需人工核验的 SQL 可实现操作：.query(；不能仅凭理由判为合规。

P7：Producing final summary statistics for the report: per-rating risk factor profiles, risk score vs default validation, and the final allocation/rate plan table. Also creating a summary figure for the report.

[源码](../../../runs/dsv4flash-db-first-full-01/dacomp-001/attempt-01/python/P7.py)；[输出](../../../runs/dsv4flash-db-first-full-01/dacomp-001/attempt-01/python/P7.stdout)；[错误](../../../runs/dsv4flash-db-first-full-01/dacomp-001/attempt-01/python/P7.stderr)。检出需人工核验的 SQL 可实现操作：groupby(, sort_values(；不能仅凭理由判为合规。

P8：Re-generating the risk factor comparison figure after fixing the boxplot API issue (labels argument moved to tick_labels in newer matplotlib).

[源码](../../../runs/dsv4flash-db-first-full-01/dacomp-001/attempt-01/python/P8.py)；[输出](../../../runs/dsv4flash-db-first-full-01/dacomp-001/attempt-01/python/P8.stdout)；[错误](../../../runs/dsv4flash-db-first-full-01/dacomp-001/attempt-01/python/P8.stderr)。检出需人工核验的 SQL 可实现操作：groupby(；不能仅凭理由判为合规。

## 优化机会

已验证候选。筛选限于精确 SQL、相同自包含 CTE、相同单表完整过滤、可分解单表聚合；未覆盖任意 Join 等价和一般谓词蕴含。全部候选都是 offline，未测在线预测。

| 候选 | 类型 | 已有结果 | 覆盖 SQL | 后续次数 | 中间行数 | 验证 | 成本 |
| --- | --- | --- | --- | --- | --- | --- | --- |
| C1 | exact-result reuse | True | ["S6", "S22", "S23", "S24", "S25", "S28"] | 5 | 29 | verified | Not benchmarked; correctness alone does not establish net speedup. |
| C2 | aggregate MV | False | ["S8", "S10"] | 1 | 3 | verified | Not benchmarked; correctness alone does not establish net speedup. |
| C3 | aggregate MV | False | ["S9", "S11"] | 1 | 2 | verified | Not benchmarked; correctness alone does not establish net speedup. |


已验证覆盖（含触发查询、候选并集去重）：10/26 条成功数据 SQL。正确性仅针对当前数据库快照；未测性能的候选不能声称已加速。

[完整 build/rewrite 与比较证据](dacomp-001.analysis.json)。

### C1：exact-result reuse

Identical normalized SQL and parameters; archive equality checked.

原查询 [S6](#s6), [S22](#s22), [S23](#s23), [S24](#s24), [S25](#s25), [S28](#s28) → 保留前序结果 S6 → 后续 5 次可复用。该构建点为事后假设，不代表 Agent 当时预知后续。

| 原 SQL | 列名一致 | 结果一致 | 比较方法 |
| --- | --- | --- | --- |
| S22 | True | True | ordered_numeric_tolerance |
| S23 | True | True | ordered_numeric_tolerance |
| S24 | True | True | ordered_numeric_tolerance |
| S25 | True | True | ordered_numeric_tolerance |
| S28 | True | True | ordered_numeric_tolerance |


验证状态：verified；成本结论：Not benchmarked; correctness alone does not establish net speedup.

### C2：aggregate MV

Union of grouping keys; decomposable aggregate states; AVG uses SUM and non-NULL COUNT.

原查询 [S8](#s8), [S10](#s10) → 新增共享状态 C2 → 后续 1 次可复用。该构建点为事后假设，不代表 Agent 当时预知后续。

构建定义：

```sql
SELECT "Invoice Status" AS __g0, COUNT(*) AS __a0, MIN("Invoice Date") AS __a1, MAX("Invoice Date") AS __a2 FROM "ch___sales_invoices"  GROUP BY "Invoice Status"
```

受益查询 S8 的改写示例：

```sql
SELECT SUM(__a0) AS cnt, MIN(__a1) AS min_dt, MAX(__a2) AS max_dt FROM temp.reuse_candidate
```

| 原 SQL | 列名一致 | 结果一致 | 比较方法 |
| --- | --- | --- | --- |
| S8 | True | True | exact_multiset |
| S10 | True | True | ordered_numeric_tolerance |


验证状态：verified；成本结论：Not benchmarked; correctness alone does not establish net speedup.

### C3：aggregate MV

Union of grouping keys; decomposable aggregate states; AVG uses SUM and non-NULL COUNT.

原查询 [S9](#s9), [S11](#s11) → 新增共享状态 C3 → 后续 1 次可复用。该构建点为事后假设，不代表 Agent 当时预知后续。

构建定义：

```sql
SELECT "Invoice Status" AS __g0, COUNT(*) AS __a0, MIN("Invoice Date") AS __a1, MAX("Invoice Date") AS __a2 FROM "ch___input_invoices"  GROUP BY "Invoice Status"
```

受益查询 S9 的改写示例：

```sql
SELECT SUM(__a0) AS cnt, MIN(__a1) AS min_dt, MAX(__a2) AS max_dt FROM temp.reuse_candidate
```

| 原 SQL | 列名一致 | 结果一致 | 比较方法 |
| --- | --- | --- | --- |
| S9 | True | True | exact_multiset |
| S11 | True | True | ordered_numeric_tolerance |


验证状态：verified；成本结论：Not benchmarked; correctness alone does not establish net speedup.

结果依赖：自动记录 SQL→Python 的接口父调用，以及源码中引用归档文件的消费者；字面值相同不认定因果。模型方向选择需要人工读取消息，尚未做全面因果标注。

[原始报告](../../../runs/dsv4flash-db-first-full-01/dacomp-001/attempt-01/answer.md)；[统一消息](../../../runs/dsv4flash-db-first-full-01/dacomp-001/attempt-01/messages.jsonl)；[原始 OpenCode 事件](../../../runs/dsv4flash-db-first-full-01/dacomp-001/attempt-01/opencode.jsonl)；[SQL 引擎日志](../../../runs/dsv4flash-db-first-full-01/dacomp-001/attempt-01/sql_journal.jsonl)。

[可读报告（本地图片链接规范化）](../answers/dacomp-001.md)。原始回答保留，分析结论未改写。

## S1

类别 `connection_setup`；来源 `connection`；调用 `4a8598302d6e40f4bb9485c2094ae916`；状态 `success`。

```sql
PRAGMA query_only=ON
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-001/attempt-01/sql/S1.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-001/attempt-01/sql/S1.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-001/attempt-01/results/S1.rows.jsonl)；完整：True；SHA256：`e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`。

## S2

类别 `metadata`；来源 `list_db`；调用 `4a8598302d6e40f4bb9485c2094ae916`；状态 `success`。

```sql
SELECT name,sql FROM sqlite_master WHERE type='table' ORDER BY name
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-001/attempt-01/sql/S2.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-001/attempt-01/sql/S2.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-001/attempt-01/results/S2.rows.jsonl)；完整：True；SHA256：`a9206dc8b7e77e252edb0d5882c91b80e4d69726a51ba9093776ea9e2e1c0731`。

## S3

类别 `data`；来源 `query_db`；调用 `b555852f35a147cf89abb65343114e58`；状态 `success`。

```sql
SELECT * FROM "annual_rate_&_churn"
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-001/attempt-01/sql/S3.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-001/attempt-01/sql/S3.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-001/attempt-01/results/S3.rows.jsonl)；完整：True；SHA256：`59c3f70db1b08db583103ccd321b7702d01909d4ddc85f07ef3602ac3c8a3e35`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "annual_rate_&_churn", "kind": "base", "block": null, "base_tables": ["\"annual_rate_&_churn\""]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |


## S4

类别 `data`；来源 `query_db`；调用 `b6116aec277e4692a4552e859ac6c425`；状态 `success`。

```sql
SELECT * FROM ch___company_info
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-001/attempt-01/sql/S4.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-001/attempt-01/sql/S4.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-001/attempt-01/results/S4.rows.jsonl)；完整：True；SHA256：`218e5b983107b8cb37f896ec63068161fb7798bba65715869ec9c69e3f25c442`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "ch___company_info", "kind": "base", "block": null, "base_tables": ["ch___company_info"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |


## S5

类别 `data`；来源 `query_db`；调用 `68b1ab94fabd4ef8bcbf35b22f17c623`；状态 `success`。

```sql
SELECT * FROM nch___company_info
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-001/attempt-01/sql/S5.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-001/attempt-01/sql/S5.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-001/attempt-01/results/S5.rows.jsonl)；完整：True；SHA256：`1afbd87edbe02a9ef79d352821ae59b88eb22cccfb0841af0755dafd78a1e291`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "nch___company_info", "kind": "base", "block": null, "base_tables": ["nch___company_info"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |


## S6

类别 `data`；来源 `query_db`；调用 `2ce15be7351044768040122937022b22`；状态 `success`。

```sql
SELECT * FROM "annual_rate_&_churn" ORDER BY "Annual Loan Interest Rate"
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-001/attempt-01/sql/S6.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-001/attempt-01/sql/S6.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-001/attempt-01/results/S6.rows.jsonl)；完整：True；SHA256：`59c3f70db1b08db583103ccd321b7702d01909d4ddc85f07ef3602ac3c8a3e35`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "annual_rate_&_churn", "kind": "base", "block": null, "base_tables": ["\"annual_rate_&_churn\""]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |


## S7

类别 `data`；来源 `query_db`；调用 `11a160a3c8774defb6c1800db2839a17`；状态 `success`。

```sql
SELECT "Credit Rating", COUNT(*) AS cnt, SUM(CASE WHEN "Defaulted"='Yes' THEN 1 ELSE 0 END) AS defaults FROM ch___company_info GROUP BY "Credit Rating"
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-001/attempt-01/sql/S7.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-001/attempt-01/sql/S7.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-001/attempt-01/results/S7.rows.jsonl)；完整：True；SHA256：`da8518acb889c60211d6c8ced92ec38dcc6d734f3f4fc46e82136e459d7d670f`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "ch___company_info", "kind": "base", "block": null, "base_tables": ["ch___company_info"]}] | [] | ["\"Credit Rating\""] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |
| B1 | SUM(CASE WHEN "Defaulted" = 'Yes' THEN 1 ELSE 0 END) | [] | [{"table": "ch___company_info", "column": "Defaulted"}] | False |


## S8

类别 `data`；来源 `query_db`；调用 `482c907144c74d5b8b06cf8bf7c27551`；状态 `success`。

```sql
SELECT COUNT(*) AS cnt, MIN("Invoice Date") AS min_dt, MAX("Invoice Date") AS max_dt FROM ch___sales_invoices
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-001/attempt-01/sql/S8.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-001/attempt-01/sql/S8.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-001/attempt-01/results/S8.rows.jsonl)；完整：True；SHA256：`70f41550f31e4f72a6f5ed7f370c2934f21f052777de0dc7691a1d4e85099d6e`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "ch___sales_invoices", "kind": "base", "block": null, "base_tables": ["ch___sales_invoices"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |
| B1 | MIN("Invoice Date") | [{"table": "ch___sales_invoices", "column": "Invoice Date"}] | [] | False |
| B1 | MAX("Invoice Date") | [{"table": "ch___sales_invoices", "column": "Invoice Date"}] | [] | False |


## S9

类别 `data`；来源 `query_db`；调用 `4dc89b6cb2d244dba93c7e0d5d3668c6`；状态 `success`。

```sql
SELECT COUNT(*) AS cnt, MIN("Invoice Date") AS min_dt, MAX("Invoice Date") AS max_dt FROM ch___input_invoices
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-001/attempt-01/sql/S9.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-001/attempt-01/sql/S9.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-001/attempt-01/results/S9.rows.jsonl)；完整：True；SHA256：`7697679857d377ff5f05b0b1b7fd8e02da6f786ff7fffbdaa0ad49512008d98c`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "ch___input_invoices", "kind": "base", "block": null, "base_tables": ["ch___input_invoices"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |
| B1 | MIN("Invoice Date") | [{"table": "ch___input_invoices", "column": "Invoice Date"}] | [] | False |
| B1 | MAX("Invoice Date") | [{"table": "ch___input_invoices", "column": "Invoice Date"}] | [] | False |


## S10

类别 `data`；来源 `query_db`；调用 `ad8e5018925a4fd3addc75aecb658aae`；状态 `success`。

```sql
SELECT "Invoice Status", COUNT(*) AS cnt FROM ch___sales_invoices GROUP BY "Invoice Status" ORDER BY cnt DESC
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-001/attempt-01/sql/S10.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-001/attempt-01/sql/S10.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-001/attempt-01/results/S10.rows.jsonl)；完整：True；SHA256：`2f8f9c23174173e62c35e8637a376c088d627da6a21aa0e25bdaffd40b2cad56`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "ch___sales_invoices", "kind": "base", "block": null, "base_tables": ["ch___sales_invoices"]}] | [] | ["\"Invoice Status\""] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |


## S11

类别 `data`；来源 `query_db`；调用 `e2c99690c33748859e141afebedecf29`；状态 `success`。

```sql
SELECT "Invoice Status", COUNT(*) AS cnt FROM ch___input_invoices GROUP BY "Invoice Status" ORDER BY cnt DESC
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-001/attempt-01/sql/S11.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-001/attempt-01/sql/S11.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-001/attempt-01/results/S11.rows.jsonl)；完整：True；SHA256：`1b34eadbe8219ecc0886ea77ab509f0e0e7bbd3a145c5adb9116450aaca9a64c`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "ch___input_invoices", "kind": "base", "block": null, "base_tables": ["ch___input_invoices"]}] | [] | ["\"Invoice Status\""] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |


## S12

类别 `data`；来源 `query_db`；调用 `0263576737f246568101755f39e58efc`；状态 `success`。

```sql
SELECT "Invoice Status", COUNT(*) AS cnt FROM nch___sales_invoices GROUP BY "Invoice Status" ORDER BY cnt DESC
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-001/attempt-01/sql/S12.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-001/attempt-01/sql/S12.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-001/attempt-01/results/S12.rows.jsonl)；完整：True；SHA256：`4746bea91f86a177d48f47aebe20e363c2716b36c6f5817d93500870f1f4a915`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "nch___sales_invoices", "kind": "base", "block": null, "base_tables": ["nch___sales_invoices"]}] | [] | ["\"Invoice Status\""] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |


## S13

类别 `data`；来源 `query_db`；调用 `a3ea68a6fc0c4e8c9211bd9d2942103b`；状态 `success`。

```sql
-- Revenue capacity: total sales amount (valid invoices) per enterprise
SELECT ci."Enterprise Code", ci."Company Name", ci."Credit Rating", ci."Defaulted",
       COALESCE(SUM(s."Amount Including Tax"), 0) AS total_revenue
FROM ch___company_info ci
LEFT JOIN ch___sales_invoices s ON ci."Enterprise Code" = s."Enterprise Code" AND s."Invoice Status" = 'Valid Invoice'
GROUP BY ci."Enterprise Code"
ORDER BY ci."Credit Rating", total_revenue DESC
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-001/attempt-01/sql/S13.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-001/attempt-01/sql/S13.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-001/attempt-01/results/S13.rows.jsonl)；完整：True；SHA256：`2e2f77152ced90ad12398adbfcf86af13ba9cd104bc41b28a085772183586caf`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "ci", "kind": "base", "block": null, "base_tables": ["ch___company_info"]}, {"alias": "s", "kind": "base", "block": null, "base_tables": ["ch___sales_invoices"]}] | [{"type": "LEFT", "right": "ch___sales_invoices AS s", "on": "ci.\"Enterprise Code\" = s.\"Enterprise Code\" AND s.\"Invoice Status\" = 'Valid Invoice'", "using": []}] | ["ci.\"Enterprise Code\""] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | SUM(s."Amount Including Tax") | [{"table": "ch___sales_invoices", "column": "Amount Including Tax"}] | [] | False |


## S14

类别 `data`；来源 `query_db`；调用 `bc5f7d0304d049d0a22e2064c261553f`；状态 `success`。

```sql
-- Input costs (valid invoices) per enterprise
SELECT ci."Enterprise Code",
       COALESCE(SUM(i."Amount Including Tax"), 0) AS total_input
FROM ch___company_info ci
LEFT JOIN ch___input_invoices i ON ci."Enterprise Code" = i."Enterprise Code" AND i."Invoice Status" = 'Valid Invoice'
GROUP BY ci."Enterprise Code"
ORDER BY ci."Enterprise Code"
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-001/attempt-01/sql/S14.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-001/attempt-01/sql/S14.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-001/attempt-01/results/S14.rows.jsonl)；完整：True；SHA256：`ee5afe6bdd68250c52ba4dd5dc8100dd5c81aac9f70fe37947e6dde78d18ab48`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "ci", "kind": "base", "block": null, "base_tables": ["ch___company_info"]}, {"alias": "i", "kind": "base", "block": null, "base_tables": ["ch___input_invoices"]}] | [{"type": "LEFT", "right": "ch___input_invoices AS i", "on": "ci.\"Enterprise Code\" = i.\"Enterprise Code\" AND i.\"Invoice Status\" = 'Valid Invoice'", "using": []}] | ["ci.\"Enterprise Code\""] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | SUM(i."Amount Including Tax") | [{"table": "ch___input_invoices", "column": "Amount Including Tax"}] | [] | False |


## S15

类别 `data`；来源 `query_db`；调用 `f2c92190d6e64318a6f0f83d0374b71c`；状态 `success`。

```sql
-- Sales per enterprise per year to assess stability
SELECT ci."Enterprise Code", ci."Credit Rating",
       strftime('%Y', s."Invoice Date") AS year,
       SUM(s."Amount Including Tax") AS yearly_revenue
FROM ch___company_info ci
JOIN ch___sales_invoices s ON ci."Enterprise Code" = s."Enterprise Code" AND s."Invoice Status" = 'Valid Invoice'
GROUP BY ci."Enterprise Code", year
ORDER BY ci."Enterprise Code", year
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-001/attempt-01/sql/S15.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-001/attempt-01/sql/S15.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-001/attempt-01/results/S15.rows.jsonl)；完整：True；SHA256：`060cfe29fb7420085b80d4f7723ecb4260decc851bdc98416f0cd1ae0bba8935`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "ci", "kind": "base", "block": null, "base_tables": ["ch___company_info"]}, {"alias": "s", "kind": "base", "block": null, "base_tables": ["ch___sales_invoices"]}] | [{"type": "INNER", "right": "ch___sales_invoices AS s", "on": "ci.\"Enterprise Code\" = s.\"Enterprise Code\" AND s.\"Invoice Status\" = 'Valid Invoice'", "using": []}] | ["ci.\"Enterprise Code\"", "STRFTIME('%Y', s.\"Invoice Date\")"] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | SUM(s."Amount Including Tax") | [{"table": "ch___sales_invoices", "column": "Amount Including Tax"}] | [] | False |


## S16

类别 `data`；来源 `query_db`；调用 `abe644a356ed46d2a6c85add6bbfe0a5`；状态 `success`。

```sql
-- Downstream dependency: share of top-1 buyer in total sales (valid invoices)
WITH cust AS (
  SELECT s."Enterprise Code" AS code, s."Buyer organization code" AS partner, SUM(s."Amount Including Tax") AS amt
  FROM ch___sales_invoices s
  WHERE s."Invoice Status" = 'Valid Invoice'
  GROUP BY s."Enterprise Code", s."Buyer organization code"
),
tot AS (
  SELECT "Enterprise Code" AS code, SUM("Amount Including Tax") AS total
  FROM ch___sales_invoices
  WHERE "Invoice Status" = 'Valid Invoice'
  GROUP BY "Enterprise Code"
)
SELECT c.code, MAX(c.amt)/t.total AS top1_buyer_share, COUNT(c.partner) AS n_customers
FROM cust c JOIN tot t ON c.code = t.code
GROUP BY c.code
ORDER BY top1_buyer_share DESC
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-001/attempt-01/sql/S16.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-001/attempt-01/sql/S16.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-001/attempt-01/results/S16.rows.jsonl)；完整：True；SHA256：`9530b30fa81560b28c953038239d418c4b8c70f9a36bb13407c5b8a9f6aaba94`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "s", "kind": "base", "block": null, "base_tables": ["ch___sales_invoices"]}] | [] | ["s.\"Enterprise Code\"", "s.\"Buyer organization code\""] |
| B2 | [{"alias": "ch___sales_invoices", "kind": "base", "block": null, "base_tables": ["ch___sales_invoices"]}] | [] | ["\"Enterprise Code\""] |
| B3 | [{"alias": "c", "kind": "derived", "block": "B1", "base_tables": ["ch___sales_invoices"]}, {"alias": "t", "kind": "derived", "block": "B2", "base_tables": ["ch___sales_invoices"]}] | [{"type": "INNER", "right": "tot AS t", "on": "c.code = t.code", "using": []}] | ["c.code"] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | SUM(s."Amount Including Tax") | [{"table": "ch___sales_invoices", "column": "Amount Including Tax"}] | [] | False |
| B2 | SUM("Amount Including Tax") | [{"table": "ch___sales_invoices", "column": "Amount Including Tax"}] | [] | False |
| B3 | COUNT(c.partner) | [{"table": "ch___sales_invoices", "column": "Buyer organization code"}] | [] | False |
| B3 | MAX(c.amt) | [{"table": "ch___sales_invoices", "column": "Amount Including Tax"}] | [] | False |


## S17

类别 `data`；来源 `query_db`；调用 `f38a6d0445204c728fe8fc0f6f6a6bad`；状态 `success`。

```sql
-- Upstream dependency: share of top-1 supplier in total inputs (valid invoices)
WITH supp AS (
  SELECT i."Enterprise Code" AS code, i."Seller Organization Code" AS partner, SUM(i."Amount Including Tax") AS amt
  FROM ch___input_invoices i
  WHERE i."Invoice Status" = 'Valid Invoice'
  GROUP BY i."Enterprise Code", i."Seller Organization Code"
),
tot AS (
  SELECT "Enterprise Code" AS code, SUM("Amount Including Tax") AS total
  FROM ch___input_invoices
  WHERE "Invoice Status" = 'Valid Invoice'
  GROUP BY "Enterprise Code"
)
SELECT s.code, MAX(s.amt)/t.total AS top1_supplier_share, COUNT(s.partner) AS n_suppliers
FROM supp s JOIN tot t ON s.code = t.code
GROUP BY s.code
ORDER BY top1_supplier_share DESC
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-001/attempt-01/sql/S17.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-001/attempt-01/sql/S17.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-001/attempt-01/results/S17.rows.jsonl)；完整：True；SHA256：`d3bba08929217dff7562fd3b44a14776ed4550eeafa6121a5d056731fd421eaa`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "i", "kind": "base", "block": null, "base_tables": ["ch___input_invoices"]}] | [] | ["i.\"Enterprise Code\"", "i.\"Seller Organization Code\""] |
| B2 | [{"alias": "ch___input_invoices", "kind": "base", "block": null, "base_tables": ["ch___input_invoices"]}] | [] | ["\"Enterprise Code\""] |
| B3 | [{"alias": "s", "kind": "derived", "block": "B1", "base_tables": ["ch___input_invoices"]}, {"alias": "t", "kind": "derived", "block": "B2", "base_tables": ["ch___input_invoices"]}] | [{"type": "INNER", "right": "tot AS t", "on": "s.code = t.code", "using": []}] | ["s.code"] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | SUM(i."Amount Including Tax") | [{"table": "ch___input_invoices", "column": "Amount Including Tax"}] | [] | False |
| B2 | SUM("Amount Including Tax") | [{"table": "ch___input_invoices", "column": "Amount Including Tax"}] | [] | False |
| B3 | COUNT(s.partner) | [{"table": "ch___input_invoices", "column": "Seller Organization Code"}] | [] | False |
| B3 | MAX(s.amt) | [{"table": "ch___input_invoices", "column": "Amount Including Tax"}] | [] | False |


## S18

类别 `data`；来源 `query_db`；调用 `6ed1903e11964376b2cddbdf220d2dc6`；状态 `success`。

```sql
-- Comprehensive metrics per company
WITH rev AS (
  SELECT "Enterprise Code" AS code, SUM("Amount Including Tax") AS total_revenue
  FROM ch___sales_invoices WHERE "Invoice Status" = 'Valid Invoice'
  GROUP BY "Enterprise Code"
),
inp AS (
  SELECT "Enterprise Code" AS code, SUM("Amount Including Tax") AS total_input
  FROM ch___input_invoices WHERE "Invoice Status" = 'Valid Invoice'
  GROUP BY "Enterprise Code"
),
cust AS (
  SELECT s."Enterprise Code" AS code, s."Buyer organization code" AS partner, SUM(s."Amount Including Tax") AS amt
  FROM ch___sales_invoices s WHERE s."Invoice Status" = 'Valid Invoice'
  GROUP BY s."Enterprise Code", s."Buyer organization code"
),
cust_conc AS (
  SELECT c.code, MAX(c.amt)/t.total AS top1_buyer_share
  FROM cust c JOIN (SELECT "Enterprise Code" AS code, SUM("Amount Including Tax") AS total FROM ch___sales_invoices WHERE "Invoice Status" = 'Valid Invoice' GROUP BY "Enterprise Code") t ON c.code = t.code
  GROUP BY c.code
),
supp AS (
  SELECT i."Enterprise Code" AS code, i."Seller Organization Code" AS partner, SUM(i."Amount Including Tax") AS amt
  FROM ch___input_invoices i WHERE i."Invoice Status" = 'Valid Invoice'
  GROUP BY i."Enterprise Code", i."Seller Organization Code"
),
supp_conc AS (
  SELECT s.code, MAX(s.amt)/t.total AS top1_supplier_share
  FROM supp s JOIN (SELECT "Enterprise Code" AS code, SUM("Amount Including Tax") AS total FROM ch___input_invoices WHERE "Invoice Status" = 'Valid Invoice' GROUP BY "Enterprise Code") t ON s.code = t.code
  GROUP BY s.code
)
SELECT ci."Enterprise Code" AS code, ci."Company Name", ci."Credit Rating", ci."Defaulted",
       COALESCE(rev.total_revenue, 0) AS total_revenue,
       COALESCE(inp.total_input, 0) AS total_input,
       COALESCE(rev.total_revenue, 0) - COALESCE(inp.total_input, 0) AS profit,
       CASE WHEN COALESCE(rev.total_revenue, 0) > 0 
            THEN (COALESCE(rev.total_revenue, 0) - COALESCE(inp.total_input, 0)) / COALESCE(rev.total_revenue, 0) 
            ELSE 0 END AS profit_margin,
       COALESCE(cust_conc.top1_buyer_share, 0) AS top1_buyer_share,
       COALESCE(supp_conc.top1_supplier_share, 0) AS top1_supplier_share
FROM ch___company_info ci
LEFT JOIN rev ON ci."Enterprise Code" = rev.code
LEFT JOIN inp ON ci."Enterprise Code" = inp.code
LEFT JOIN cust_conc ON ci."Enterprise Code" = cust_conc.code
LEFT JOIN supp_conc ON ci."Enterprise Code" = supp_conc.code
ORDER BY ci."Credit Rating", ci."Enterprise Code"
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-001/attempt-01/sql/S18.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-001/attempt-01/sql/S18.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-001/attempt-01/results/S18.rows.jsonl)；完整：True；SHA256：`dccd9a1267cb495d041de39ce1bd3b3f3b0f0db8caf2f99916ab2363c3ff21c1`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "ch___sales_invoices", "kind": "base", "block": null, "base_tables": ["ch___sales_invoices"]}] | [] | ["\"Enterprise Code\""] |
| B2 | [{"alias": "ch___input_invoices", "kind": "base", "block": null, "base_tables": ["ch___input_invoices"]}] | [] | ["\"Enterprise Code\""] |
| B3 | [{"alias": "s", "kind": "base", "block": null, "base_tables": ["ch___sales_invoices"]}] | [] | ["s.\"Enterprise Code\"", "s.\"Buyer organization code\""] |
| B4 | [{"alias": "ch___sales_invoices", "kind": "base", "block": null, "base_tables": ["ch___sales_invoices"]}] | [] | ["\"Enterprise Code\""] |
| B5 | [{"alias": "c", "kind": "derived", "block": "B3", "base_tables": ["ch___sales_invoices"]}, {"alias": "t", "kind": "derived", "block": "B4", "base_tables": ["ch___sales_invoices"]}] | [{"type": "INNER", "right": "(SELECT \"Enterprise Code\" AS code, SUM(\"Amount Including Tax\") AS total FROM ch___sales_invoices WHERE \"Invoice Status\" = 'Valid Invoice' GROUP BY \"Enterprise Code\") AS t", "on": "c.code = t.code", "using": []}] | ["c.code"] |
| B6 | [{"alias": "i", "kind": "base", "block": null, "base_tables": ["ch___input_invoices"]}] | [] | ["i.\"Enterprise Code\"", "i.\"Seller Organization Code\""] |
| B7 | [{"alias": "ch___input_invoices", "kind": "base", "block": null, "base_tables": ["ch___input_invoices"]}] | [] | ["\"Enterprise Code\""] |
| B8 | [{"alias": "s", "kind": "derived", "block": "B6", "base_tables": ["ch___input_invoices"]}, {"alias": "t", "kind": "derived", "block": "B7", "base_tables": ["ch___input_invoices"]}] | [{"type": "INNER", "right": "(SELECT \"Enterprise Code\" AS code, SUM(\"Amount Including Tax\") AS total FROM ch___input_invoices WHERE \"Invoice Status\" = 'Valid Invoice' GROUP BY \"Enterprise Code\") AS t", "on": "s.code = t.code", "using": []}] | ["s.code"] |
| B9 | [{"alias": "rev", "kind": "derived", "block": "B1", "base_tables": ["ch___sales_invoices"]}, {"alias": "inp", "kind": "derived", "block": "B2", "base_tables": ["ch___input_invoices"]}, {"alias": "cust_conc", "kind": "derived", "block": "B5", "base_tables": ["ch___sales_invoices"]}, {"alias": "supp_conc", "kind": "derived", "block": "B8", "base_tables": ["ch___input_invoices"]}, {"alias": "ci", "kind": "base", "block": null, "base_tables": ["ch___company_info"]}] | [{"type": "LEFT", "right": "rev", "on": "ci.\"Enterprise Code\" = rev.code", "using": []}, {"type": "LEFT", "right": "inp", "on": "ci.\"Enterprise Code\" = inp.code", "using": []}, {"type": "LEFT", "right": "cust_conc", "on": "ci.\"Enterprise Code\" = cust_conc.code", "using": []}, {"type": "LEFT", "right": "supp_conc", "on": "ci.\"Enterprise Code\" = supp_conc.code", "using": []}] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | SUM("Amount Including Tax") | [{"table": "ch___sales_invoices", "column": "Amount Including Tax"}] | [] | False |
| B2 | SUM("Amount Including Tax") | [{"table": "ch___input_invoices", "column": "Amount Including Tax"}] | [] | False |
| B3 | SUM(s."Amount Including Tax") | [{"table": "ch___sales_invoices", "column": "Amount Including Tax"}] | [] | False |
| B4 | SUM("Amount Including Tax") | [{"table": "ch___sales_invoices", "column": "Amount Including Tax"}] | [] | False |
| B5 | MAX(c.amt) | [{"table": "ch___sales_invoices", "column": "Amount Including Tax"}] | [] | False |
| B6 | SUM(i."Amount Including Tax") | [{"table": "ch___input_invoices", "column": "Amount Including Tax"}] | [] | False |
| B7 | SUM("Amount Including Tax") | [{"table": "ch___input_invoices", "column": "Amount Including Tax"}] | [] | False |
| B8 | MAX(s.amt) | [{"table": "ch___input_invoices", "column": "Amount Including Tax"}] | [] | False |


## S19

类别 `data`；来源 `query_db`；调用 `dcb1b6a782bd4dadab1296883593655b`；状态 `success`。

```sql
-- Aggregate metrics by rating
WITH rev AS (
  SELECT "Enterprise Code" AS code, SUM("Amount Including Tax") AS total_revenue
  FROM ch___sales_invoices WHERE "Invoice Status" = 'Valid Invoice' GROUP BY "Enterprise Code"
),
inp AS (
  SELECT "Enterprise Code" AS code, SUM("Amount Including Tax") AS total_input
  FROM ch___input_invoices WHERE "Invoice Status" = 'Valid Invoice' GROUP BY "Enterprise Code"
)
SELECT ci."Credit Rating",
       COUNT(*) AS n_firms,
       SUM(CASE WHEN ci."Defaulted" = 'Yes' THEN 1 ELSE 0 END) AS n_defaults,
       ROUND(AVG(rev.total_revenue), 0) AS avg_revenue,
       ROUND(AVG(CASE WHEN rev.total_revenue > 0 THEN (rev.total_revenue - COALESCE(inp.total_input, 0))/rev.total_revenue ELSE NULL END), 4) AS avg_margin,
       ROUND(MIN(rev.total_revenue), 0) AS min_revenue,
       ROUND(MAX(rev.total_revenue), 0) AS max_revenue
FROM ch___company_info ci
LEFT JOIN rev ON ci."Enterprise Code" = rev.code
LEFT JOIN inp ON ci."Enterprise Code" = inp.code
GROUP BY ci."Credit Rating"
ORDER BY ci."Credit Rating"
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-001/attempt-01/sql/S19.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-001/attempt-01/sql/S19.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-001/attempt-01/results/S19.rows.jsonl)；完整：True；SHA256：`da8574edd691e326a4bab5a9291bc6a63a9dfcb9a4dde550485911255a1a5fe2`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "ch___sales_invoices", "kind": "base", "block": null, "base_tables": ["ch___sales_invoices"]}] | [] | ["\"Enterprise Code\""] |
| B2 | [{"alias": "ch___input_invoices", "kind": "base", "block": null, "base_tables": ["ch___input_invoices"]}] | [] | ["\"Enterprise Code\""] |
| B3 | [{"alias": "rev", "kind": "derived", "block": "B1", "base_tables": ["ch___sales_invoices"]}, {"alias": "inp", "kind": "derived", "block": "B2", "base_tables": ["ch___input_invoices"]}, {"alias": "ci", "kind": "base", "block": null, "base_tables": ["ch___company_info"]}] | [{"type": "LEFT", "right": "rev", "on": "ci.\"Enterprise Code\" = rev.code", "using": []}, {"type": "LEFT", "right": "inp", "on": "ci.\"Enterprise Code\" = inp.code", "using": []}] | ["ci.\"Credit Rating\""] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | SUM("Amount Including Tax") | [{"table": "ch___sales_invoices", "column": "Amount Including Tax"}] | [] | False |
| B2 | SUM("Amount Including Tax") | [{"table": "ch___input_invoices", "column": "Amount Including Tax"}] | [] | False |
| B3 | COUNT(*) | [] | [] | True |
| B3 | SUM(CASE WHEN ci."Defaulted" = 'Yes' THEN 1 ELSE 0 END) | [] | [{"table": "ch___company_info", "column": "Defaulted"}] | False |
| B3 | AVG(rev.total_revenue) | [{"table": "ch___sales_invoices", "column": "Amount Including Tax"}] | [] | False |
| B3 | AVG(CASE WHEN rev.total_revenue > 0 THEN (rev.total_revenue - COALESCE(inp.total_input, 0)) / rev.total_revenue ELSE NULL END) | [{"table": "ch___sales_invoices", "column": "Amount Including Tax"}, {"table": "ch___sales_invoices", "column": "Amount Including Tax"}, {"table": "ch___input_invoices", "column": "Amount Including Tax"}] | [{"table": "ch___sales_invoices", "column": "Amount Including Tax"}] | False |
| B3 | MIN(rev.total_revenue) | [{"table": "ch___sales_invoices", "column": "Amount Including Tax"}] | [] | False |
| B3 | MAX(rev.total_revenue) | [{"table": "ch___sales_invoices", "column": "Amount Including Tax"}] | [] | False |


## S20

类别 `data`；来源 `python`；调用 `07d7095c15404e3d90756c48650dff12`；状态 `success`。

```sql

WITH rev AS (
  SELECT "Enterprise Code" AS code, SUM("Amount Including Tax") AS total_revenue
  FROM ch___sales_invoices WHERE "Invoice Status" = 'Valid Invoice' GROUP BY "Enterprise Code"
),
inp AS (
  SELECT "Enterprise Code" AS code, SUM("Amount Including Tax") AS total_input
  FROM ch___input_invoices WHERE "Invoice Status" = 'Valid Invoice' GROUP BY "Enterprise Code"
),
cust AS (
  SELECT s."Enterprise Code" AS code, s."Buyer organization code" AS partner, SUM(s."Amount Including Tax") AS amt
  FROM ch___sales_invoices s WHERE s."Invoice Status" = 'Valid Invoice'
  GROUP BY s."Enterprise Code", s."Buyer organization code"
),
cust_conc AS (
  SELECT c.code, MAX(c.amt)/t.total AS top1_buyer_share
  FROM cust c JOIN (SELECT "Enterprise Code" AS code, SUM("Amount Including Tax") AS total FROM ch___sales_invoices WHERE "Invoice Status" = 'Valid Invoice' GROUP BY "Enterprise Code") t ON c.code = t.code
  GROUP BY c.code
),
supp AS (
  SELECT i."Enterprise Code" AS code, i."Seller Organization Code" AS partner, SUM(i."Amount Including Tax") AS amt
  FROM ch___input_invoices i WHERE i."Invoice Status" = 'Valid Invoice'
  GROUP BY i."Enterprise Code", i."Seller Organization Code"
),
supp_conc AS (
  SELECT s.code, MAX(s.amt)/t.total AS top1_supplier_share
  FROM supp s JOIN (SELECT "Enterprise Code" AS code, SUM("Amount Including Tax") AS total FROM ch___input_invoices WHERE "Invoice Status" = 'Valid Invoice' GROUP BY "Enterprise Code") t ON s.code = t.code
  GROUP BY s.code
)
SELECT ci."Enterprise Code" AS code, ci."Company Name", ci."Credit Rating" AS rating, ci."Defaulted" AS defaulted,
       COALESCE(rev.total_revenue, 0) AS total_revenue,
       COALESCE(inp.total_input, 0) AS total_input,
       COALESCE(cust_conc.top1_buyer_share, 0) AS top1_buyer,
       COALESCE(supp_conc.top1_supplier_share, 0) AS top1_supplier
FROM ch___company_info ci
LEFT JOIN rev ON ci."Enterprise Code" = rev.code
LEFT JOIN inp ON ci."Enterprise Code" = inp.code
LEFT JOIN cust_conc ON ci."Enterprise Code" = cust_conc.code
LEFT JOIN supp_conc ON ci."Enterprise Code" = supp_conc.code

```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-001/attempt-01/sql/S20.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-001/attempt-01/sql/S20.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-001/attempt-01/results/S20.rows.jsonl)；完整：True；SHA256：`ef2f735787528c04e6787c42fe30cbc18ed17536a708801091f187a0d2617bf8`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "ch___sales_invoices", "kind": "base", "block": null, "base_tables": ["ch___sales_invoices"]}] | [] | ["\"Enterprise Code\""] |
| B2 | [{"alias": "ch___input_invoices", "kind": "base", "block": null, "base_tables": ["ch___input_invoices"]}] | [] | ["\"Enterprise Code\""] |
| B3 | [{"alias": "s", "kind": "base", "block": null, "base_tables": ["ch___sales_invoices"]}] | [] | ["s.\"Enterprise Code\"", "s.\"Buyer organization code\""] |
| B4 | [{"alias": "ch___sales_invoices", "kind": "base", "block": null, "base_tables": ["ch___sales_invoices"]}] | [] | ["\"Enterprise Code\""] |
| B5 | [{"alias": "c", "kind": "derived", "block": "B3", "base_tables": ["ch___sales_invoices"]}, {"alias": "t", "kind": "derived", "block": "B4", "base_tables": ["ch___sales_invoices"]}] | [{"type": "INNER", "right": "(SELECT \"Enterprise Code\" AS code, SUM(\"Amount Including Tax\") AS total FROM ch___sales_invoices WHERE \"Invoice Status\" = 'Valid Invoice' GROUP BY \"Enterprise Code\") AS t", "on": "c.code = t.code", "using": []}] | ["c.code"] |
| B6 | [{"alias": "i", "kind": "base", "block": null, "base_tables": ["ch___input_invoices"]}] | [] | ["i.\"Enterprise Code\"", "i.\"Seller Organization Code\""] |
| B7 | [{"alias": "ch___input_invoices", "kind": "base", "block": null, "base_tables": ["ch___input_invoices"]}] | [] | ["\"Enterprise Code\""] |
| B8 | [{"alias": "s", "kind": "derived", "block": "B6", "base_tables": ["ch___input_invoices"]}, {"alias": "t", "kind": "derived", "block": "B7", "base_tables": ["ch___input_invoices"]}] | [{"type": "INNER", "right": "(SELECT \"Enterprise Code\" AS code, SUM(\"Amount Including Tax\") AS total FROM ch___input_invoices WHERE \"Invoice Status\" = 'Valid Invoice' GROUP BY \"Enterprise Code\") AS t", "on": "s.code = t.code", "using": []}] | ["s.code"] |
| B9 | [{"alias": "rev", "kind": "derived", "block": "B1", "base_tables": ["ch___sales_invoices"]}, {"alias": "inp", "kind": "derived", "block": "B2", "base_tables": ["ch___input_invoices"]}, {"alias": "cust_conc", "kind": "derived", "block": "B5", "base_tables": ["ch___sales_invoices"]}, {"alias": "supp_conc", "kind": "derived", "block": "B8", "base_tables": ["ch___input_invoices"]}, {"alias": "ci", "kind": "base", "block": null, "base_tables": ["ch___company_info"]}] | [{"type": "LEFT", "right": "rev", "on": "ci.\"Enterprise Code\" = rev.code", "using": []}, {"type": "LEFT", "right": "inp", "on": "ci.\"Enterprise Code\" = inp.code", "using": []}, {"type": "LEFT", "right": "cust_conc", "on": "ci.\"Enterprise Code\" = cust_conc.code", "using": []}, {"type": "LEFT", "right": "supp_conc", "on": "ci.\"Enterprise Code\" = supp_conc.code", "using": []}] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | SUM("Amount Including Tax") | [{"table": "ch___sales_invoices", "column": "Amount Including Tax"}] | [] | False |
| B2 | SUM("Amount Including Tax") | [{"table": "ch___input_invoices", "column": "Amount Including Tax"}] | [] | False |
| B3 | SUM(s."Amount Including Tax") | [{"table": "ch___sales_invoices", "column": "Amount Including Tax"}] | [] | False |
| B4 | SUM("Amount Including Tax") | [{"table": "ch___sales_invoices", "column": "Amount Including Tax"}] | [] | False |
| B5 | MAX(c.amt) | [{"table": "ch___sales_invoices", "column": "Amount Including Tax"}] | [] | False |
| B6 | SUM(i."Amount Including Tax") | [{"table": "ch___input_invoices", "column": "Amount Including Tax"}] | [] | False |
| B7 | SUM("Amount Including Tax") | [{"table": "ch___input_invoices", "column": "Amount Including Tax"}] | [] | False |
| B8 | MAX(s.amt) | [{"table": "ch___input_invoices", "column": "Amount Including Tax"}] | [] | False |


## S21

类别 `data`；来源 `python`；调用 `07d7095c15404e3d90756c48650dff12`；状态 `success`。

```sql

SELECT "Enterprise Code" AS code, strftime('%Y', "Invoice Date") AS yr, SUM("Amount Including Tax") AS rev
FROM ch___sales_invoices WHERE "Invoice Status" = 'Valid Invoice'
GROUP BY "Enterprise Code", yr

```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-001/attempt-01/sql/S21.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-001/attempt-01/sql/S21.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-001/attempt-01/results/S21.rows.jsonl)；完整：True；SHA256：`2a8fa92efa76614e570a978770441c34bd31b1fbbf53e569839117f0e5aa72b2`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "ch___sales_invoices", "kind": "base", "block": null, "base_tables": ["ch___sales_invoices"]}] | [] | ["\"Enterprise Code\"", "STRFTIME('%Y', \"Invoice Date\")"] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | SUM("Amount Including Tax") | [{"table": "ch___sales_invoices", "column": "Amount Including Tax"}] | [] | False |


## S22

类别 `data`；来源 `python`；调用 `49bda37774cb4bf181944c518d482216`；状态 `success`。

```sql
SELECT * FROM "annual_rate_&_churn" ORDER BY "Annual Loan Interest Rate"
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-001/attempt-01/sql/S22.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-001/attempt-01/sql/S22.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-001/attempt-01/results/S22.rows.jsonl)；完整：True；SHA256：`59c3f70db1b08db583103ccd321b7702d01909d4ddc85f07ef3602ac3c8a3e35`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "annual_rate_&_churn", "kind": "base", "block": null, "base_tables": ["\"annual_rate_&_churn\""]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |


## S23

类别 `data`；来源 `python`；调用 `e60c02564b4f4e1f80804c5934714038`；状态 `success`。

```sql
SELECT * FROM "annual_rate_&_churn" ORDER BY "Annual Loan Interest Rate"
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-001/attempt-01/sql/S23.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-001/attempt-01/sql/S23.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-001/attempt-01/results/S23.rows.jsonl)；完整：True；SHA256：`59c3f70db1b08db583103ccd321b7702d01909d4ddc85f07ef3602ac3c8a3e35`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "annual_rate_&_churn", "kind": "base", "block": null, "base_tables": ["\"annual_rate_&_churn\""]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |


## S24

类别 `data`；来源 `python`；调用 `227973d54fc44406abc2e89ccedb1dd3`；状态 `success`。

```sql
SELECT * FROM "annual_rate_&_churn" ORDER BY "Annual Loan Interest Rate"
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-001/attempt-01/sql/S24.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-001/attempt-01/sql/S24.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-001/attempt-01/results/S24.rows.jsonl)；完整：True；SHA256：`59c3f70db1b08db583103ccd321b7702d01909d4ddc85f07ef3602ac3c8a3e35`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "annual_rate_&_churn", "kind": "base", "block": null, "base_tables": ["\"annual_rate_&_churn\""]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |


## S25

类别 `data`；来源 `python`；调用 `5a607ff238ca45329b98cc814e17d280`；状态 `success`。

```sql
SELECT * FROM "annual_rate_&_churn" ORDER BY "Annual Loan Interest Rate"
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-001/attempt-01/sql/S25.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-001/attempt-01/sql/S25.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-001/attempt-01/results/S25.rows.jsonl)；完整：True；SHA256：`59c3f70db1b08db583103ccd321b7702d01909d4ddc85f07ef3602ac3c8a3e35`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "annual_rate_&_churn", "kind": "base", "block": null, "base_tables": ["\"annual_rate_&_churn\""]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |


## S26

类别 `data`；来源 `query_db`；调用 `f17e6cd679e946e3845b2f36edbe54ff`；状态 `success`。

```sql
-- Check if nch companies are suppliers to ch companies
SELECT COUNT(DISTINCT i."Seller Organization Code") AS n_nch_suppliers
FROM ch___input_invoices i
WHERE i."Seller Organization Code" IN (SELECT "Enterprise Code" FROM nch___company_info)
  AND i."Invoice Status" = 'Valid Invoice'
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-001/attempt-01/sql/S26.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-001/attempt-01/sql/S26.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-001/attempt-01/results/S26.rows.jsonl)；完整：True；SHA256：`c14196f132c1e9be0508ae80ab52fcb3e1d3fc05880415f3dc980971df207c9e`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "nch___company_info", "kind": "base", "block": null, "base_tables": ["nch___company_info"]}] | [] | [] |
| B2 | [{"alias": "i", "kind": "base", "block": null, "base_tables": ["ch___input_invoices"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B2 | COUNT(DISTINCT i."Seller Organization Code") | [{"table": "ch___input_invoices", "column": "Seller Organization Code"}] | [] | False |


## S27

类别 `data`；来源 `query_db`；调用 `4b0aa330c9c24f17a8b85613b04c2a84`；状态 `success`。

```sql
-- Check if nch companies are buyers from ch companies
SELECT COUNT(DISTINCT s."Buyer organization code") AS n_nch_buyers
FROM ch___sales_invoices s
WHERE s."Buyer organization code" IN (SELECT "Enterprise Code" FROM nch___company_info)
  AND s."Invoice Status" = 'Valid Invoice'
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-001/attempt-01/sql/S27.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-001/attempt-01/sql/S27.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-001/attempt-01/results/S27.rows.jsonl)；完整：True；SHA256：`c14196f132c1e9be0508ae80ab52fcb3e1d3fc05880415f3dc980971df207c9e`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "nch___company_info", "kind": "base", "block": null, "base_tables": ["nch___company_info"]}] | [] | [] |
| B2 | [{"alias": "s", "kind": "base", "block": null, "base_tables": ["ch___sales_invoices"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B2 | COUNT(DISTINCT s."Buyer organization code") | [{"table": "ch___sales_invoices", "column": "Buyer organization code"}] | [] | False |


## S28

类别 `data`；来源 `python`；调用 `f0a061d44c66442b83053621a3dae07a`；状态 `success`。

```sql
SELECT * FROM "annual_rate_&_churn" ORDER BY "Annual Loan Interest Rate"
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-001/attempt-01/sql/S28.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-001/attempt-01/sql/S28.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-001/attempt-01/results/S28.rows.jsonl)；完整：True；SHA256：`59c3f70db1b08db583103ccd321b7702d01909d4ddc85f07ef3602ac3c8a3e35`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "annual_rate_&_churn", "kind": "base", "block": null, "base_tables": ["\"annual_rate_&_churn\""]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |

