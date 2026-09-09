# dacomp-004

For each month, determine which product has the highest Sales Amount and provide its corre…

运行：已提交。官方未评分。全部 SQL 尝试/成功 19/19；数据 SQL 17/17；Python 4 次。

完整原题：

For each month, determine which product has the highest Sales Amount and provide its corresponding Product Code. Separately analyze how these products perform across different months, and explore the relationship between their repurchase rate and Sales Amount.

| 表 | 行数 | 列数 |
| --- | --- | --- |
| sheet1 | 42816 | 15 |


实际路线（分析者依据 SQL/源码概括，不代表 Agent 自述）：S3：sheet1 查询 → S6：sheet1 分组聚合 → S9：sheet1 分组聚合 → S13：sheet1 分组聚合 → S16：sheet1 分组聚合 → S19：sheet1 分组聚合（等距列出六个结构节点，全部步骤见下表）

数据库大小：9,310,208 字节。

## 数据 SQL

| SQL | 状态 | 基础表 | Join 输入/类型 | GROUP BY | 聚合表达式 | 结果行数 | 数据库 ms |
| --- | --- | --- | --- | --- | --- | --- | --- |
| [S3/Q1](#s3) | success | ["sheet1"] | 0 / {} | [] | ["COUNT(*)", "COUNT(DISTINCT \"Product Code\")", "COUNT(DISTINCT \"Sales Month\")", "COUNT(DISTINCT \"Customer ID\")", "MIN(\"Sales Month\")", "MAX(\"Sales Month\")", "SUM(\"Sales Amount\")"] | 1 | 37.136 |
| [S4/Q2](#s4) | success | ["sheet1"] | 0 / {} | ["\"Sales Month\""] | ["COUNT(*)", "COUNT(DISTINCT \"Product Code\")", "SUM(\"Sales Amount\")"] | 4 | 38.513 |
| [S5/Q3](#s5) | success | ["sheet1"] | 0 / {} | ["\"Sales Month\"", "\"Product Code\""] | ["SUM(\"Sales Amount\")"] | 12041 | 55.43 |
| [S6/Q4](#s6) | success | ["sheet1"] | 0 / {} | ["\"Sales Month\"", "\"Product Code\""] | ["SUM(\"Sales Amount\")", "SUM(\"Sales Amount\")"] | 4 | 55.396 |
| [S7/Q5](#s7) | success | ["sheet1"] | 0 / {} | ["\"Sales Month\"", "\"Product Code\""] | ["COUNT(*)", "COUNT(DISTINCT \"Customer ID\")", "SUM(\"Sales Amount\")"] | 10 | 9.598 |
| [S8/Q6](#s8) | success | ["sheet1"] | 0 / {} | ["\"Product Code\"", "\"Customer ID\""] | ["COUNT(*)", "SUM(\"Sales Amount\")"] | 367 | 10.156 |
| [S9/Q7](#s9) | success | ["sheet1"] | 0 / {} | ["\"Product Code\"", "\"Customer ID\"", "\"Product Code\""] | ["COUNT(*)", "COUNT(*)", "SUM(CASE WHEN purchase_count > 1 THEN 1 ELSE 0 END)", "SUM(purchase_count)", "COUNT(*)", "SUM(purchase_count)", "SUM(CASE WHEN purchase_count > 1 THEN 1 ELSE 0 END)", "SUM(purchase_count)", "COUNT(*)"] | 4 | 9.857 |
| [S10/Q8](#s10) | success | ["sheet1"] | 0 / {} | ["\"Product Code\""] | ["COUNT(*)", "COUNT(DISTINCT \"Customer ID\")", "SUM(\"Sales Amount\")", "AVG(\"Sales Amount\")"] | 4 | 9.712 |
| [S11/Q9](#s11) | success | ["sheet1"] | 2 / {'INNER': 1} | ["\"Product Code\"", "\"Customer ID\"", "\"Product Code\"", "\"Product Code\""] | ["COUNT(*)", "COUNT(*)", "SUM(CASE WHEN purchase_count > 1 THEN 1 ELSE 0 END)", "SUM(\"Sales Amount\")", "COUNT(*)", "COUNT(DISTINCT \"Customer ID\")"] | 30 | 95.9 |
| [S12/Q10](#s12) | success | ["sheet1"] | 2 / {'INNER': 1} | ["\"Product Code\"", "\"Customer ID\"", "\"Product Code\"", "\"Product Code\""] | ["COUNT(*)", "COUNT(*)", "SUM(CASE WHEN purchase_count > 1 THEN 1 ELSE 0 END)", "SUM(\"Sales Amount\")", "COUNT(*)"] | 1565 | 80.918 |
| [S13/Q11](#s13) | success | ["sheet1"] | 2 / {'INNER': 1} | ["\"Product Code\"", "\"Customer ID\"", "\"Product Code\"", "\"Product Code\""] | ["COUNT(*)", "COUNT(*)", "SUM(CASE WHEN purchase_count > 1 THEN 1 ELSE 0 END)", "SUM(\"Sales Amount\")", "COUNT(*)"] | 1565 | 79.801 |
| [S14/Q12](#s14) | success | ["sheet1"] | 0 / {} | ["\"Sales Month\"", "\"Product Code\""] | ["SUM(\"Sales Amount\")"] | 10 | 9.526 |
| [S15/Q13](#s15) | success | ["sheet1"] | 2 / {'INNER': 1} | ["\"Product Code\"", "\"Customer ID\"", "\"Product Code\"", "\"Product Code\""] | ["COUNT(*)", "COUNT(*)", "SUM(CASE WHEN purchase_count > 1 THEN 1 ELSE 0 END)", "SUM(\"Sales Amount\")"] | 1565 | 79.376 |
| [S16/Q14](#s16) | success | ["sheet1"] | 2 / {'INNER': 1} | ["\"Product Code\"", "\"Customer ID\"", "\"Product Code\"", "\"Product Code\""] | ["COUNT(*)", "COUNT(*)", "SUM(CASE WHEN purchase_count > 1 THEN 1 ELSE 0 END)", "SUM(\"Sales Amount\")"] | 1565 | 79.465 |
| [S17/Q15](#s17) | success | ["sheet1"] | 2 / {'INNER': 1} | ["\"Product Code\"", "\"Customer ID\"", "\"Product Code\"", "\"Product Code\""] | ["COUNT(*)", "COUNT(*)", "SUM(CASE WHEN purchase_count > 1 THEN 1 ELSE 0 END)", "SUM(\"Sales Amount\")", "COUNT(*)"] | 10 | 82.252 |
| [S18/Q16](#s18) | success | ["sheet1"] | 0 / {} | ["\"Product Code\""] | ["MIN(\"Sales Amount\")", "MAX(\"Sales Amount\")", "COUNT(*)", "AVG(\"Sales Amount\")"] | 4 | 9.633 |
| [S19/Q17](#s19) | success | ["sheet1"] | 0 / {} | ["\"Sales Month\"", "\"Product Code\""] | ["COUNT(DISTINCT \"Customer ID\")", "COUNT(*)", "COUNT(*)", "COUNT(*)", "COUNT(DISTINCT \"Customer ID\")"] | 10 | 10.646 |


## 元数据和设置

| SQL | 类别 | 状态 | 内容 |
| --- | --- | --- | --- |
| S1 | connection_setup | success | PRAGMA query_only=ON |
| S2 | metadata | success | SELECT name,sql FROM sqlite_master WHERE type='table' ORDER BY name |


## Python 与执行位置

人工源码审查：**reviewed_with_statistical_plotting_exceptions**。Core filtering, joins, product/customer aggregation and ranking are performed in SQL. Python performs Pearson/Spearman tests, regression, quantiles and plotting. Log transforms and per-series peak annotations are disclosed as statistical/plotting preparation outside SQL; P4 only inspects permitted filesystem locations. No pandas relational groupby/merge pipeline appears in the four scripts. [证据](../reviews/dacomp-004.json)。

P1：Python is used here for statistical correlation analysis (Pearson/Spearman) and visualization (scatter plots, monthly performance charts), which are not supported by SQLite's SQL capabilities. Only pre-aggregated data (product-month totals, per-product sales and repurchase rates) is loaded via the logged db interface.

[源码](../../../runs/dsv4flash-db-first-full-01/dacomp-004/attempt-01/python/P1.py)；[输出](../../../runs/dsv4flash-db-first-full-01/dacomp-004/attempt-01/python/P1.stdout)；[错误](../../../runs/dsv4flash-db-first-full-01/dacomp-004/attempt-01/python/P1.stderr)。检出需人工核验的 SQL 可实现操作：.query(；不能仅凭理由判为合规。

P2：Creating visualizations of the monthly performance of top products (line chart) and the relationship between repurchase rate and sales amount (scatter plot with regression line). These are visual outputs not feasible in SQL.

[源码](../../../runs/dsv4flash-db-first-full-01/dacomp-004/attempt-01/python/P2.py)；[输出](../../../runs/dsv4flash-db-first-full-01/dacomp-004/attempt-01/python/P2.stdout)；[错误](../../../runs/dsv4flash-db-first-full-01/dacomp-004/attempt-01/python/P2.stderr)。检出需人工核验的 SQL 可实现操作：.query(；不能仅凭理由判为合规。

P3：Verifying the output figure files exist in the workspace and getting a final summary of key statistics to support the report.

[源码](../../../runs/dsv4flash-db-first-full-01/dacomp-004/attempt-01/python/P3.py)；[输出](../../../runs/dsv4flash-db-first-full-01/dacomp-004/attempt-01/python/P3.stdout)；[错误](../../../runs/dsv4flash-db-first-full-01/dacomp-004/attempt-01/python/P3.stderr)。检出需人工核验的 SQL 可实现操作：.query(；不能仅凭理由判为合规。

P4：Checking the actual location of saved figure files so they can be referenced correctly in the report.

[源码](../../../runs/dsv4flash-db-first-full-01/dacomp-004/attempt-01/python/P4.py)；[输出](../../../runs/dsv4flash-db-first-full-01/dacomp-004/attempt-01/python/P4.stdout)；[错误](../../../runs/dsv4flash-db-first-full-01/dacomp-004/attempt-01/python/P4.stderr)。自动源码筛查未检出预设迁出信号；这不是全面语义合规证明。

## 优化机会

已验证候选。筛选限于精确 SQL、相同自包含 CTE、相同单表完整过滤、可分解单表聚合；未覆盖任意 Join 等价和一般谓词蕴含。全部候选都是 offline，未测在线预测。

| 候选 | 类型 | 已有结果 | 覆盖 SQL | 后续次数 | 中间行数 | 验证 | 成本 |
| --- | --- | --- | --- | --- | --- | --- | --- |
| C1 | exact-result reuse | True | ["S15", "S16"] | 1 | unknown | not_verified_cap | Not tested |
| C2 | common subexpression | False | ["S11", "S12", "S13", "S15", "S16", "S17"] | 5 | 36858 | verified | Not benchmarked; correctness alone does not establish net speedup. |
| C3 | common subexpression | False | ["S12", "S13", "S17"] | 2 | 6142 | verified | Not benchmarked; correctness alone does not establish net speedup. |
| C4 | common subexpression | False | ["S15", "S16"] | 1 | unknown | not_verified_cap | Not tested |
| C5 | common filtered view | False | ["S7", "S8", "S10", "S14", "S18", "S19"] | 5 | 501 | verified | Not benchmarked; correctness alone does not establish net speedup. |
| C6 | aggregate MV | False | ["S8", "S14"] | 1 | unknown | not_verified_cap | Not tested |


已验证覆盖（含触发查询、候选并集去重）：12/17 条成功数据 SQL。正确性仅针对当前数据库快照；未测性能的候选不能声称已加速。

[完整 build/rewrite 与比较证据](dacomp-004.analysis.json)。

### C2：common subexpression

Identical self-contained CTE body across queries.

原查询 [S11](#s11), [S12](#s12), [S13](#s13), [S15](#s15), [S16](#s16), [S17](#s17) → 新增共享状态 C2 → 后续 5 次可复用。该构建点为事后假设，不代表 Agent 当时预知后续。

构建定义：

```sql
SELECT "Product Code", "Customer ID", COUNT(*) AS purchase_count FROM sheet1 GROUP BY "Product Code", "Customer ID"
```

受益查询 S11 的改写示例：

```sql
WITH cust AS (SELECT * FROM temp.reuse_candidate), prod_stats AS (SELECT "Product Code", COUNT(*) AS n_customers, SUM(CASE WHEN purchase_count > 1 THEN 1 ELSE 0 END) AS repeat_customers FROM cust GROUP BY "Product Code"), sales AS (SELECT "Product Code", SUM("Sales Amount") AS total_sales, COUNT(*) AS n_transactions, COUNT(DISTINCT "Customer ID") AS n_cust_sales FROM sheet1 GROUP BY "Product Code") SELECT s."Product Code", ROUND(s.total_sales, 2) AS total_sales, s.n_transactions, ps.n_customers, ps.repeat_customers, ROUND(1.0 * ps.repeat_customers / ps.n_customers, 4) AS repurchase_rate FROM sales AS s JOIN prod_stats AS ps ON s."Product Code" = ps."Product Code" ORDER BY s.total_sales DESC LIMIT 30
```

| 原 SQL | 列名一致 | 结果一致 | 比较方法 |
| --- | --- | --- | --- |
| S11 | True | True | ordered_numeric_tolerance |
| S12 | True | True | ordered_numeric_tolerance |
| S13 | True | True | exact_multiset |
| S15 | True | True | exact_multiset |
| S16 | True | True | exact_multiset |
| S17 | True | True | ordered_numeric_tolerance |


验证状态：verified；成本结论：Not benchmarked; correctness alone does not establish net speedup.

### C5：common filtered view

Same single source and complete filter; original filter retained.

原查询 [S7](#s7), [S8](#s8), [S10](#s10), [S14](#s14), [S18](#s18), [S19](#s19) → 新增共享状态 C5 → 后续 5 次可复用。该构建点为事后假设，不代表 Agent 当时预知后续。

构建定义：

```sql
SELECT * FROM "sheet1" WHERE "Product Code" IN ('DW-1001040125', 'DW-2316020016', 'DW-1203130446', 'DW-1518040045')
```

受益查询 S7 的改写示例：

```sql
SELECT "Sales Month", "Product Code", ROUND(SUM("Sales Amount"), 2) AS total_amount, COUNT(*) AS transaction_count, COUNT(DISTINCT "Customer ID") AS customer_count FROM temp.reuse_candidate AS sheet1 WHERE "Product Code" IN ('DW-1001040125', 'DW-2316020016', 'DW-1203130446', 'DW-1518040045') GROUP BY "Sales Month", "Product Code" ORDER BY "Product Code", "Sales Month"
```

| 原 SQL | 列名一致 | 结果一致 | 比较方法 |
| --- | --- | --- | --- |
| S7 | True | True | ordered_numeric_tolerance |
| S8 | True | True | ordered_numeric_tolerance |
| S10 | True | True | ordered_numeric_tolerance |
| S14 | True | True | ordered_numeric_tolerance |
| S18 | True | True | exact_multiset |
| S19 | True | True | ordered_numeric_tolerance |


验证状态：verified；成本结论：Not benchmarked; correctness alone does not establish net speedup.

### C3：common subexpression

Identical self-contained CTE body across queries.

原查询 [S12](#s12), [S13](#s13), [S17](#s17) → 新增共享状态 C3 → 后续 2 次可复用。该构建点为事后假设，不代表 Agent 当时预知后续。

构建定义：

```sql
SELECT "Product Code", SUM("Sales Amount") AS total_sales, COUNT(*) AS n_transactions FROM sheet1 GROUP BY "Product Code"
```

受益查询 S12 的改写示例：

```sql
WITH cust AS (SELECT "Product Code", "Customer ID", COUNT(*) AS purchase_count FROM sheet1 GROUP BY "Product Code", "Customer ID"), prod_stats AS (SELECT "Product Code", COUNT(*) AS n_customers, SUM(CASE WHEN purchase_count > 1 THEN 1 ELSE 0 END) AS repeat_customers FROM cust GROUP BY "Product Code"), sales AS (SELECT * FROM temp.reuse_candidate) SELECT s."Product Code", ROUND(s.total_sales, 2) AS total_sales, s.n_transactions, ps.n_customers, ps.repeat_customers, ROUND(1.0 * ps.repeat_customers / NULLIF(ps.n_customers, 0), 4) AS repurchase_rate FROM sales AS s JOIN prod_stats AS ps ON s."Product Code" = ps."Product Code" WHERE ps.n_customers >= 5 ORDER BY s.total_sales DESC
```

| 原 SQL | 列名一致 | 结果一致 | 比较方法 |
| --- | --- | --- | --- |
| S12 | True | True | ordered_numeric_tolerance |
| S13 | True | True | exact_multiset |
| S17 | True | True | ordered_numeric_tolerance |


验证状态：verified；成本结论：Not benchmarked; correctness alone does not establish net speedup.

结果依赖：自动记录 SQL→Python 的接口父调用，以及源码中引用归档文件的消费者；字面值相同不认定因果。模型方向选择需要人工读取消息，尚未做全面因果标注。

[原始报告](../../../runs/dsv4flash-db-first-full-01/dacomp-004/attempt-01/answer.md)；[统一消息](../../../runs/dsv4flash-db-first-full-01/dacomp-004/attempt-01/messages.jsonl)；[原始 OpenCode 事件](../../../runs/dsv4flash-db-first-full-01/dacomp-004/attempt-01/opencode.jsonl)；[SQL 引擎日志](../../../runs/dsv4flash-db-first-full-01/dacomp-004/attempt-01/sql_journal.jsonl)。

[可读报告（本地图片链接规范化）](../answers/dacomp-004.md)。原始回答保留，分析结论未改写。

## S1

类别 `connection_setup`；来源 `connection`；调用 `07eb32888a6144588c68290fa9907bf6`；状态 `success`。

```sql
PRAGMA query_only=ON
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-004/attempt-01/sql/S1.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-004/attempt-01/sql/S1.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-004/attempt-01/results/S1.rows.jsonl)；完整：True；SHA256：`e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`。

## S2

类别 `metadata`；来源 `list_db`；调用 `07eb32888a6144588c68290fa9907bf6`；状态 `success`。

```sql
SELECT name,sql FROM sqlite_master WHERE type='table' ORDER BY name
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-004/attempt-01/sql/S2.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-004/attempt-01/sql/S2.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-004/attempt-01/results/S2.rows.jsonl)；完整：True；SHA256：`1b241f6387dfc8600a326fca3d032eb6662ca78041455a1fa5a3c58b6ac96678`。

## S3

类别 `data`；来源 `query_db`；调用 `13bdcca36ddc407ca815e0c2d6caed7d`；状态 `success`。

```sql
SELECT COUNT(*) AS total_rows, COUNT(DISTINCT "Product Code") AS n_products, COUNT(DISTINCT "Sales Month") AS n_months, COUNT(DISTINCT "Customer ID") AS n_customers, MIN("Sales Month") AS min_month, MAX("Sales Month") AS max_month, SUM("Sales Amount") AS total_sales FROM sheet1
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-004/attempt-01/sql/S3.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-004/attempt-01/sql/S3.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-004/attempt-01/results/S3.rows.jsonl)；完整：True；SHA256：`b19e18ce12b65a975bf483c3e1dc606596dcbd059d1298514d22a1b41280ac30`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "sheet1", "kind": "base", "block": null, "base_tables": ["sheet1"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |
| B1 | COUNT(DISTINCT "Product Code") | [{"table": "sheet1", "column": "Product Code"}] | [] | False |
| B1 | COUNT(DISTINCT "Sales Month") | [{"table": "sheet1", "column": "Sales Month"}] | [] | False |
| B1 | COUNT(DISTINCT "Customer ID") | [{"table": "sheet1", "column": "Customer ID"}] | [] | False |
| B1 | MIN("Sales Month") | [{"table": "sheet1", "column": "Sales Month"}] | [] | False |
| B1 | MAX("Sales Month") | [{"table": "sheet1", "column": "Sales Month"}] | [] | False |
| B1 | SUM("Sales Amount") | [{"table": "sheet1", "column": "Sales Amount"}] | [] | False |


## S4

类别 `data`；来源 `query_db`；调用 `9ec1da998437428d83357a809d1503ec`；状态 `success`。

```sql
SELECT "Sales Month", COUNT(*) AS rows_n, COUNT(DISTINCT "Product Code") AS n_products, SUM("Sales Amount") AS total_amount FROM sheet1 GROUP BY "Sales Month" ORDER BY "Sales Month"
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-004/attempt-01/sql/S4.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-004/attempt-01/sql/S4.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-004/attempt-01/results/S4.rows.jsonl)；完整：True；SHA256：`5b2724a22c92d9b1e0837f5c60f12c8ca896365c54835fdcb3603f5d1516e01b`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "sheet1", "kind": "base", "block": null, "base_tables": ["sheet1"]}] | [] | ["\"Sales Month\""] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |
| B1 | COUNT(DISTINCT "Product Code") | [{"table": "sheet1", "column": "Product Code"}] | [] | False |
| B1 | SUM("Sales Amount") | [{"table": "sheet1", "column": "Sales Amount"}] | [] | False |


## S5

类别 `data`；来源 `query_db`；调用 `b9ee8bd2c1234cad9ab852d32b39b355`；状态 `success`。

```sql
SELECT "Sales Month", "Product Code", SUM("Sales Amount") AS total_amount
FROM sheet1
GROUP BY "Sales Month", "Product Code"
ORDER BY "Sales Month", total_amount DESC
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-004/attempt-01/sql/S5.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-004/attempt-01/sql/S5.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-004/attempt-01/results/S5.rows.jsonl)；完整：True；SHA256：`3c75746490ed014eeb827cbac3dd5e754180e74c4840176c209a520e4abfef51`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "sheet1", "kind": "base", "block": null, "base_tables": ["sheet1"]}] | [] | ["\"Sales Month\"", "\"Product Code\""] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | SUM("Sales Amount") | [{"table": "sheet1", "column": "Sales Amount"}] | [] | False |


## S6

类别 `data`；来源 `query_db`；调用 `de22b6525dba42c185c4b020b3ffbdec`；状态 `success`。

```sql
WITH product_month AS (
  SELECT "Sales Month", "Product Code", SUM("Sales Amount") AS total_amount,
         ROW_NUMBER() OVER (PARTITION BY "Sales Month" ORDER BY SUM("Sales Amount") DESC) AS rn
  FROM sheet1
  GROUP BY "Sales Month", "Product Code"
)
SELECT "Sales Month", "Product Code", ROUND(total_amount, 2) AS total_amount
FROM product_month
WHERE rn = 1
ORDER BY "Sales Month"
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-004/attempt-01/sql/S6.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-004/attempt-01/sql/S6.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-004/attempt-01/results/S6.rows.jsonl)；完整：True；SHA256：`f7fb42bcfc3a35283f14e01c2fb35cf364a05b15ca35ebd3f700318df178ec28`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "sheet1", "kind": "base", "block": null, "base_tables": ["sheet1"]}] | [] | ["\"Sales Month\"", "\"Product Code\""] |
| B2 | [{"alias": "product_month", "kind": "derived", "block": "B1", "base_tables": ["sheet1"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | SUM("Sales Amount") | [{"table": "sheet1", "column": "Sales Amount"}] | [] | False |
| B1 | SUM("Sales Amount") | [{"table": "sheet1", "column": "Sales Amount"}] | [] | False |


## S7

类别 `data`；来源 `query_db`；调用 `54f1db3f4f504dfe9cbfc97720648997`；状态 `success`。

```sql
SELECT "Sales Month", "Product Code", ROUND(SUM("Sales Amount"), 2) AS total_amount, COUNT(*) AS transaction_count, COUNT(DISTINCT "Customer ID") AS customer_count
FROM sheet1
WHERE "Product Code" IN ('DW-1001040125', 'DW-2316020016', 'DW-1203130446', 'DW-1518040045')
GROUP BY "Sales Month", "Product Code"
ORDER BY "Product Code", "Sales Month"
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-004/attempt-01/sql/S7.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-004/attempt-01/sql/S7.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-004/attempt-01/results/S7.rows.jsonl)；完整：True；SHA256：`0ffbfdf8b66560d284249b8ee37c5a7d2d971030ef5460696dca7c8d1a8c2b98`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "sheet1", "kind": "base", "block": null, "base_tables": ["sheet1"]}] | [] | ["\"Sales Month\"", "\"Product Code\""] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |
| B1 | COUNT(DISTINCT "Customer ID") | [{"table": "sheet1", "column": "Customer ID"}] | [] | False |
| B1 | SUM("Sales Amount") | [{"table": "sheet1", "column": "Sales Amount"}] | [] | False |


## S8

类别 `data`；来源 `query_db`；调用 `b91b4a916cf74e51b3ab0a1b2c01e408`；状态 `success`。

```sql
SELECT "Product Code", "Customer ID", COUNT(*) AS purchase_count, SUM("Sales Amount") AS total_spent
FROM sheet1
WHERE "Product Code" IN ('DW-1001040125', 'DW-2316020016', 'DW-1203130446', 'DW-1518040045')
GROUP BY "Product Code", "Customer ID"
ORDER BY "Product Code", purchase_count DESC
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-004/attempt-01/sql/S8.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-004/attempt-01/sql/S8.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-004/attempt-01/results/S8.rows.jsonl)；完整：True；SHA256：`cba3860b8370ca57ae8facca37e89964cb2108fc5452dc990f126bc05b3b3ee9`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "sheet1", "kind": "base", "block": null, "base_tables": ["sheet1"]}] | [] | ["\"Product Code\"", "\"Customer ID\""] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |
| B1 | SUM("Sales Amount") | [{"table": "sheet1", "column": "Sales Amount"}] | [] | False |


## S9

类别 `data`；来源 `query_db`；调用 `54475219a3b244ad90b83cfc5faa8cbc`；状态 `success`。

```sql
WITH cust AS (
  SELECT "Product Code", "Customer ID", COUNT(*) AS purchase_count
  FROM sheet1
  WHERE "Product Code" IN ('DW-1001040125', 'DW-2316020016', 'DW-1203130446', 'DW-1518040045')
  GROUP BY "Product Code", "Customer ID"
)
SELECT "Product Code",
       COUNT(*) AS n_customers,
       SUM(CASE WHEN purchase_count > 1 THEN 1 ELSE 0 END) AS repeat_customers,
       ROUND(1.0 * SUM(CASE WHEN purchase_count > 1 THEN 1 ELSE 0 END) / COUNT(*), 4) AS customer_repurchase_rate,
       SUM(purchase_count) AS n_transactions,
       ROUND(1.0 * (SUM(purchase_count) - COUNT(*)) / SUM(purchase_count), 4) AS transaction_repurchase_share
FROM cust
GROUP BY "Product Code"
ORDER BY "Product Code"
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-004/attempt-01/sql/S9.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-004/attempt-01/sql/S9.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-004/attempt-01/results/S9.rows.jsonl)；完整：True；SHA256：`249bc50989caa31b37cf5998073b887fb420b263ba6becb9407aadc6959f54a9`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "sheet1", "kind": "base", "block": null, "base_tables": ["sheet1"]}] | [] | ["\"Product Code\"", "\"Customer ID\""] |
| B2 | [{"alias": "cust", "kind": "derived", "block": "B1", "base_tables": ["sheet1"]}] | [] | ["\"Product Code\""] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |
| B2 | COUNT(*) | [] | [] | True |
| B2 | SUM(CASE WHEN purchase_count > 1 THEN 1 ELSE 0 END) | [] | [] | False |
| B2 | SUM(purchase_count) | [] | [] | False |
| B2 | COUNT(*) | [] | [] | True |
| B2 | SUM(purchase_count) | [] | [] | False |
| B2 | SUM(CASE WHEN purchase_count > 1 THEN 1 ELSE 0 END) | [] | [] | False |
| B2 | SUM(purchase_count) | [] | [] | False |
| B2 | COUNT(*) | [] | [] | True |


## S10

类别 `data`；来源 `query_db`；调用 `94f5cbbcef0549db89d9ede3e91e9796`；状态 `success`。

```sql
SELECT "Product Code", 
       ROUND(SUM("Sales Amount"), 2) AS total_sales_amount,
       COUNT(*) AS total_transactions,
       COUNT(DISTINCT "Customer ID") AS total_customers,
       ROUND(AVG("Sales Amount"), 2) AS avg_transaction_amount
FROM sheet1
WHERE "Product Code" IN ('DW-1001040125', 'DW-2316020016', 'DW-1203130446', 'DW-1518040045')
GROUP BY "Product Code"
ORDER BY "Product Code"
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-004/attempt-01/sql/S10.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-004/attempt-01/sql/S10.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-004/attempt-01/results/S10.rows.jsonl)；完整：True；SHA256：`bdf899f3363d835f19cc550dc5c1673f16779efdf67e0cd93f3aadc4d0d29946`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "sheet1", "kind": "base", "block": null, "base_tables": ["sheet1"]}] | [] | ["\"Product Code\""] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |
| B1 | COUNT(DISTINCT "Customer ID") | [{"table": "sheet1", "column": "Customer ID"}] | [] | False |
| B1 | SUM("Sales Amount") | [{"table": "sheet1", "column": "Sales Amount"}] | [] | False |
| B1 | AVG("Sales Amount") | [{"table": "sheet1", "column": "Sales Amount"}] | [] | False |


## S11

类别 `data`；来源 `query_db`；调用 `a39e3e53ab1e458fb005c7a2ed982bf8`；状态 `success`。

```sql
WITH cust AS (
  SELECT "Product Code", "Customer ID", COUNT(*) AS purchase_count
  FROM sheet1
  GROUP BY "Product Code", "Customer ID"
),
prod_stats AS (
  SELECT "Product Code",
         COUNT(*) AS n_customers,
         SUM(CASE WHEN purchase_count > 1 THEN 1 ELSE 0 END) AS repeat_customers
  FROM cust
  GROUP BY "Product Code"
),
sales AS (
  SELECT "Product Code", SUM("Sales Amount") AS total_sales, COUNT(*) AS n_transactions, COUNT(DISTINCT "Customer ID") AS n_cust_sales
  FROM sheet1
  GROUP BY "Product Code"
)
SELECT s."Product Code",
       ROUND(s.total_sales, 2) AS total_sales,
       s.n_transactions,
       ps.n_customers,
       ps.repeat_customers,
       ROUND(1.0 * ps.repeat_customers / ps.n_customers, 4) AS repurchase_rate
FROM sales s
JOIN prod_stats ps ON s."Product Code" = ps."Product Code"
ORDER BY s.total_sales DESC
LIMIT 30
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-004/attempt-01/sql/S11.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-004/attempt-01/sql/S11.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-004/attempt-01/results/S11.rows.jsonl)；完整：True；SHA256：`74013d116245346af80cae2d0ec202de8840657a2ddb3c16f26aa4bb32edee25`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "sheet1", "kind": "base", "block": null, "base_tables": ["sheet1"]}] | [] | ["\"Product Code\"", "\"Customer ID\""] |
| B2 | [{"alias": "cust", "kind": "derived", "block": "B1", "base_tables": ["sheet1"]}] | [] | ["\"Product Code\""] |
| B3 | [{"alias": "sheet1", "kind": "base", "block": null, "base_tables": ["sheet1"]}] | [] | ["\"Product Code\""] |
| B4 | [{"alias": "s", "kind": "derived", "block": "B3", "base_tables": ["sheet1"]}, {"alias": "ps", "kind": "derived", "block": "B2", "base_tables": ["sheet1"]}] | [{"type": "INNER", "right": "prod_stats AS ps", "on": "s.\"Product Code\" = ps.\"Product Code\"", "using": []}] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |
| B2 | COUNT(*) | [] | [] | True |
| B2 | SUM(CASE WHEN purchase_count > 1 THEN 1 ELSE 0 END) | [] | [] | False |
| B3 | SUM("Sales Amount") | [{"table": "sheet1", "column": "Sales Amount"}] | [] | False |
| B3 | COUNT(*) | [] | [] | True |
| B3 | COUNT(DISTINCT "Customer ID") | [{"table": "sheet1", "column": "Customer ID"}] | [] | False |


## S12

类别 `data`；来源 `query_db`；调用 `56ed31ce3b9f4d13bcf10830bf25e6ba`；状态 `success`。

```sql
WITH cust AS (
  SELECT "Product Code", "Customer ID", COUNT(*) AS purchase_count
  FROM sheet1
  GROUP BY "Product Code", "Customer ID"
),
prod_stats AS (
  SELECT "Product Code",
         COUNT(*) AS n_customers,
         SUM(CASE WHEN purchase_count > 1 THEN 1 ELSE 0 END) AS repeat_customers
  FROM cust
  GROUP BY "Product Code"
),
sales AS (
  SELECT "Product Code", SUM("Sales Amount") AS total_sales, COUNT(*) AS n_transactions
  FROM sheet1
  GROUP BY "Product Code"
)
SELECT s."Product Code",
       ROUND(s.total_sales, 2) AS total_sales,
       s.n_transactions,
       ps.n_customers,
       ps.repeat_customers,
       ROUND(1.0 * ps.repeat_customers / NULLIF(ps.n_customers, 0), 4) AS repurchase_rate
FROM sales s
JOIN prod_stats ps ON s."Product Code" = ps."Product Code"
WHERE ps.n_customers >= 5
ORDER BY s.total_sales DESC
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-004/attempt-01/sql/S12.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-004/attempt-01/sql/S12.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-004/attempt-01/results/S12.rows.jsonl)；完整：True；SHA256：`3b572fc4d2115b434bca38517e5e843ef1a1011f25bd8e732f14c0d3f88693c5`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "sheet1", "kind": "base", "block": null, "base_tables": ["sheet1"]}] | [] | ["\"Product Code\"", "\"Customer ID\""] |
| B2 | [{"alias": "cust", "kind": "derived", "block": "B1", "base_tables": ["sheet1"]}] | [] | ["\"Product Code\""] |
| B3 | [{"alias": "sheet1", "kind": "base", "block": null, "base_tables": ["sheet1"]}] | [] | ["\"Product Code\""] |
| B4 | [{"alias": "s", "kind": "derived", "block": "B3", "base_tables": ["sheet1"]}, {"alias": "ps", "kind": "derived", "block": "B2", "base_tables": ["sheet1"]}] | [{"type": "INNER", "right": "prod_stats AS ps", "on": "s.\"Product Code\" = ps.\"Product Code\"", "using": []}] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |
| B2 | COUNT(*) | [] | [] | True |
| B2 | SUM(CASE WHEN purchase_count > 1 THEN 1 ELSE 0 END) | [] | [] | False |
| B3 | SUM("Sales Amount") | [{"table": "sheet1", "column": "Sales Amount"}] | [] | False |
| B3 | COUNT(*) | [] | [] | True |


## S13

类别 `data`；来源 `python`；调用 `39548ee7e8aa404e90e304708071fe76`；状态 `success`。

```sql

WITH cust AS (
  SELECT "Product Code", "Customer ID", COUNT(*) AS purchase_count
  FROM sheet1
  GROUP BY "Product Code", "Customer ID"
),
prod_stats AS (
  SELECT "Product Code",
         COUNT(*) AS n_customers,
         SUM(CASE WHEN purchase_count > 1 THEN 1 ELSE 0 END) AS repeat_customers
  FROM cust
  GROUP BY "Product Code"
),
sales AS (
  SELECT "Product Code", SUM("Sales Amount") AS total_sales, COUNT(*) AS n_transactions
  FROM sheet1
  GROUP BY "Product Code"
)
SELECT s."Product Code" AS product, s.total_sales, s.n_transactions,
       ps.n_customers, ps.repeat_customers,
       1.0 * ps.repeat_customers / NULLIF(ps.n_customers,0) AS repurchase_rate
FROM sales s JOIN prod_stats ps ON s."Product Code" = ps."Product Code"
WHERE ps.n_customers >= 5

```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-004/attempt-01/sql/S13.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-004/attempt-01/sql/S13.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-004/attempt-01/results/S13.rows.jsonl)；完整：True；SHA256：`0cf5eacf089779f0f2d7d720bbba2788c22ed909972d505df73e94e6ff68e64b`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "sheet1", "kind": "base", "block": null, "base_tables": ["sheet1"]}] | [] | ["\"Product Code\"", "\"Customer ID\""] |
| B2 | [{"alias": "cust", "kind": "derived", "block": "B1", "base_tables": ["sheet1"]}] | [] | ["\"Product Code\""] |
| B3 | [{"alias": "sheet1", "kind": "base", "block": null, "base_tables": ["sheet1"]}] | [] | ["\"Product Code\""] |
| B4 | [{"alias": "s", "kind": "derived", "block": "B3", "base_tables": ["sheet1"]}, {"alias": "ps", "kind": "derived", "block": "B2", "base_tables": ["sheet1"]}] | [{"type": "INNER", "right": "prod_stats AS ps", "on": "s.\"Product Code\" = ps.\"Product Code\"", "using": []}] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |
| B2 | COUNT(*) | [] | [] | True |
| B2 | SUM(CASE WHEN purchase_count > 1 THEN 1 ELSE 0 END) | [] | [] | False |
| B3 | SUM("Sales Amount") | [{"table": "sheet1", "column": "Sales Amount"}] | [] | False |
| B3 | COUNT(*) | [] | [] | True |


## S14

类别 `data`；来源 `python`；调用 `da9e838927b84cedbdeede53cad5dcba`；状态 `success`。

```sql

SELECT "Sales Month" AS month, "Product Code" AS product, SUM("Sales Amount") AS sales_amount
FROM sheet1
WHERE "Product Code" IN ('DW-1001040125', 'DW-2316020016', 'DW-1203130446', 'DW-1518040045')
GROUP BY "Sales Month", "Product Code"
ORDER BY product, month

```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-004/attempt-01/sql/S14.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-004/attempt-01/sql/S14.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-004/attempt-01/results/S14.rows.jsonl)；完整：True；SHA256：`6381e2b9f380add37faf1e4cb33ad41e5dd6401648397d8873f154a8e82a3bae`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "sheet1", "kind": "base", "block": null, "base_tables": ["sheet1"]}] | [] | ["\"Sales Month\"", "\"Product Code\""] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | SUM("Sales Amount") | [{"table": "sheet1", "column": "Sales Amount"}] | [] | False |


## S15

类别 `data`；来源 `python`；调用 `da9e838927b84cedbdeede53cad5dcba`；状态 `success`。

```sql

WITH cust AS (
  SELECT "Product Code", "Customer ID", COUNT(*) AS purchase_count
  FROM sheet1
  GROUP BY "Product Code", "Customer ID"
),
prod_stats AS (
  SELECT "Product Code",
         COUNT(*) AS n_customers,
         SUM(CASE WHEN purchase_count > 1 THEN 1 ELSE 0 END) AS repeat_customers
  FROM cust
  GROUP BY "Product Code"
),
sales AS (
  SELECT "Product Code", SUM("Sales Amount") AS total_sales
  FROM sheet1
  GROUP BY "Product Code"
)
SELECT s.total_sales, 1.0 * ps.repeat_customers / NULLIF(ps.n_customers, 0) AS repurchase_rate
FROM sales s JOIN prod_stats ps ON s."Product Code" = ps."Product Code"
WHERE ps.n_customers >= 5

```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-004/attempt-01/sql/S15.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-004/attempt-01/sql/S15.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-004/attempt-01/results/S15.rows.jsonl)；完整：True；SHA256：`0bab0adb40277eaab5bbad99cd57765b8002640c542147aba7eccc856ffc4254`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "sheet1", "kind": "base", "block": null, "base_tables": ["sheet1"]}] | [] | ["\"Product Code\"", "\"Customer ID\""] |
| B2 | [{"alias": "cust", "kind": "derived", "block": "B1", "base_tables": ["sheet1"]}] | [] | ["\"Product Code\""] |
| B3 | [{"alias": "sheet1", "kind": "base", "block": null, "base_tables": ["sheet1"]}] | [] | ["\"Product Code\""] |
| B4 | [{"alias": "s", "kind": "derived", "block": "B3", "base_tables": ["sheet1"]}, {"alias": "ps", "kind": "derived", "block": "B2", "base_tables": ["sheet1"]}] | [{"type": "INNER", "right": "prod_stats AS ps", "on": "s.\"Product Code\" = ps.\"Product Code\"", "using": []}] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |
| B2 | COUNT(*) | [] | [] | True |
| B2 | SUM(CASE WHEN purchase_count > 1 THEN 1 ELSE 0 END) | [] | [] | False |
| B3 | SUM("Sales Amount") | [{"table": "sheet1", "column": "Sales Amount"}] | [] | False |


## S16

类别 `data`；来源 `python`；调用 `7f50facdaba14b00a3116ec9d33338de`；状态 `success`。

```sql

WITH cust AS (
  SELECT "Product Code", "Customer ID", COUNT(*) AS purchase_count
  FROM sheet1
  GROUP BY "Product Code", "Customer ID"
),
prod_stats AS (
  SELECT "Product Code",
         COUNT(*) AS n_customers,
         SUM(CASE WHEN purchase_count > 1 THEN 1 ELSE 0 END) AS repeat_customers
  FROM cust
  GROUP BY "Product Code"
),
sales AS (
  SELECT "Product Code", SUM("Sales Amount") AS total_sales
  FROM sheet1
  GROUP BY "Product Code"
)
SELECT s.total_sales, 1.0 * ps.repeat_customers / NULLIF(ps.n_customers, 0) AS repurchase_rate
FROM sales s JOIN prod_stats ps ON s."Product Code" = ps."Product Code"
WHERE ps.n_customers >= 5

```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-004/attempt-01/sql/S16.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-004/attempt-01/sql/S16.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-004/attempt-01/results/S16.rows.jsonl)；完整：True；SHA256：`0bab0adb40277eaab5bbad99cd57765b8002640c542147aba7eccc856ffc4254`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "sheet1", "kind": "base", "block": null, "base_tables": ["sheet1"]}] | [] | ["\"Product Code\"", "\"Customer ID\""] |
| B2 | [{"alias": "cust", "kind": "derived", "block": "B1", "base_tables": ["sheet1"]}] | [] | ["\"Product Code\""] |
| B3 | [{"alias": "sheet1", "kind": "base", "block": null, "base_tables": ["sheet1"]}] | [] | ["\"Product Code\""] |
| B4 | [{"alias": "s", "kind": "derived", "block": "B3", "base_tables": ["sheet1"]}, {"alias": "ps", "kind": "derived", "block": "B2", "base_tables": ["sheet1"]}] | [{"type": "INNER", "right": "prod_stats AS ps", "on": "s.\"Product Code\" = ps.\"Product Code\"", "using": []}] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |
| B2 | COUNT(*) | [] | [] | True |
| B2 | SUM(CASE WHEN purchase_count > 1 THEN 1 ELSE 0 END) | [] | [] | False |
| B3 | SUM("Sales Amount") | [{"table": "sheet1", "column": "Sales Amount"}] | [] | False |


## S17

类别 `data`；来源 `python`；调用 `7f50facdaba14b00a3116ec9d33338de`；状态 `success`。

```sql

WITH cust AS (
  SELECT "Product Code", "Customer ID", COUNT(*) AS purchase_count
  FROM sheet1
  GROUP BY "Product Code", "Customer ID"
),
prod_stats AS (
  SELECT "Product Code",
         COUNT(*) AS n_customers,
         SUM(CASE WHEN purchase_count > 1 THEN 1 ELSE 0 END) AS repeat_customers
  FROM cust
  GROUP BY "Product Code"
),
sales AS (
  SELECT "Product Code", SUM("Sales Amount") AS total_sales, COUNT(*) AS n_transactions
  FROM sheet1
  GROUP BY "Product Code"
)
SELECT s."Product Code" AS product, ROUND(s.total_sales,2) AS total_sales,
       s.n_transactions, ps.n_customers,
       ROUND(1.0 * ps.repeat_customers / NULLIF(ps.n_customers,0), 4) AS repurchase_rate
FROM sales s JOIN prod_stats ps ON s."Product Code" = ps."Product Code"
WHERE ps.n_customers >= 5
ORDER BY s.total_sales DESC
LIMIT 10

```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-004/attempt-01/sql/S17.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-004/attempt-01/sql/S17.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-004/attempt-01/results/S17.rows.jsonl)；完整：True；SHA256：`ee8f3a2ab8918896759975b3e02ab8c4728f4ec002891562454cc9ab6a0608b7`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "sheet1", "kind": "base", "block": null, "base_tables": ["sheet1"]}] | [] | ["\"Product Code\"", "\"Customer ID\""] |
| B2 | [{"alias": "cust", "kind": "derived", "block": "B1", "base_tables": ["sheet1"]}] | [] | ["\"Product Code\""] |
| B3 | [{"alias": "sheet1", "kind": "base", "block": null, "base_tables": ["sheet1"]}] | [] | ["\"Product Code\""] |
| B4 | [{"alias": "s", "kind": "derived", "block": "B3", "base_tables": ["sheet1"]}, {"alias": "ps", "kind": "derived", "block": "B2", "base_tables": ["sheet1"]}] | [{"type": "INNER", "right": "prod_stats AS ps", "on": "s.\"Product Code\" = ps.\"Product Code\"", "using": []}] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |
| B2 | COUNT(*) | [] | [] | True |
| B2 | SUM(CASE WHEN purchase_count > 1 THEN 1 ELSE 0 END) | [] | [] | False |
| B3 | SUM("Sales Amount") | [{"table": "sheet1", "column": "Sales Amount"}] | [] | False |
| B3 | COUNT(*) | [] | [] | True |


## S18

类别 `data`；来源 `query_db`；调用 `77ab96d7da9a469ea617432ddce5dfad`；状态 `success`。

```sql
SELECT "Product Code", "Major Category Name", "Middle Category Name", "Minor Category Name", "Specification/Model", "Product Type", "Unit", MIN("Sales Amount") AS min_amt, MAX("Sales Amount") AS max_amt, ROUND(AVG("Sales Amount"),2) AS avg_amt, COUNT(*) AS n
FROM sheet1
WHERE "Product Code" IN ('DW-1001040125', 'DW-2316020016', 'DW-1203130446', 'DW-1518040045')
GROUP BY "Product Code"
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-004/attempt-01/sql/S18.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-004/attempt-01/sql/S18.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-004/attempt-01/results/S18.rows.jsonl)；完整：True；SHA256：`bc199bc2d8664b1cec585417fbf5feebc42e2ae3dfe82498ec94a25db2e1128e`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "sheet1", "kind": "base", "block": null, "base_tables": ["sheet1"]}] | [] | ["\"Product Code\""] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | MIN("Sales Amount") | [{"table": "sheet1", "column": "Sales Amount"}] | [] | False |
| B1 | MAX("Sales Amount") | [{"table": "sheet1", "column": "Sales Amount"}] | [] | False |
| B1 | COUNT(*) | [] | [] | True |
| B1 | AVG("Sales Amount") | [{"table": "sheet1", "column": "Sales Amount"}] | [] | False |


## S19

类别 `data`；来源 `query_db`；调用 `300b6352239c4cba82bc8f1c3a7bdc49`；状态 `success`。

```sql
SELECT "Sales Month", "Product Code",
       COUNT(DISTINCT "Customer ID") AS cust_n,
       COUNT(*) AS txn_n,
       ROUND(1.0 * (COUNT(*) - COUNT(DISTINCT "Customer ID")) / COUNT(*), 4) AS repeat_txn_share
FROM sheet1
WHERE "Product Code" IN ('DW-1001040125', 'DW-2316020016', 'DW-1203130446', 'DW-1518040045')
GROUP BY "Sales Month", "Product Code"
ORDER BY "Product Code", "Sales Month"
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-004/attempt-01/sql/S19.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-004/attempt-01/sql/S19.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-004/attempt-01/results/S19.rows.jsonl)；完整：True；SHA256：`f0d198fdde75db704a35a4b3ef1ad323a0eab22b0c91ab202787ce808ca1c1f8`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "sheet1", "kind": "base", "block": null, "base_tables": ["sheet1"]}] | [] | ["\"Sales Month\"", "\"Product Code\""] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(DISTINCT "Customer ID") | [{"table": "sheet1", "column": "Customer ID"}] | [] | False |
| B1 | COUNT(*) | [] | [] | True |
| B1 | COUNT(*) | [] | [] | True |
| B1 | COUNT(*) | [] | [] | True |
| B1 | COUNT(DISTINCT "Customer ID") | [{"table": "sheet1", "column": "Customer ID"}] | [] | False |

