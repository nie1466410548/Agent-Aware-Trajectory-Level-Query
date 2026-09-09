# dacomp-024

Compare the business performance of the four regions (Central, East, South, West), analyze…

运行：已提交。官方未评分。全部 SQL 尝试/成功 25/24；数据 SQL 23/22；Python 3 次。

完整原题：

Compare the business performance of the four regions (Central, East, South, West), analyze the differences in penetration and profitability across 2015, 2016, and 2017 for each region in the three segments—Consumer, Corporate, and Home Office—identify the best-performing region–segment combinations, and provide expansion recommendations.

| 表 | 行数 | 列数 |
| --- | --- | --- |
| sheet1 | 9994 | 12 |
| sheet2 | 9994 | 9 |


实际路线（分析者依据 SQL/源码概括，不代表 Agent 自述）：SQL 汇总区域×客群×年份销售、利润和客户数 → Python 计算渗透份额、同比和更粗粒度汇总 → 比较区域客群组合并绘图。

数据库大小：5,042,176 字节。

## 数据 SQL

| SQL | 状态 | 基础表 | Join 输入/类型 | GROUP BY | 聚合表达式 | 结果行数 | 数据库 ms |
| --- | --- | --- | --- | --- | --- | --- | --- |
| [S3/Q1](#s3) | success | ["sheet1"] | 0 / {} | [] | [] | 4 | 5.468 |
| [S4/Q2](#s4) | success | ["sheet1"] | 0 / {} | [] | [] | 4 | 3.459 |
| [S5/Q3](#s5) | success | ["sheet1"] | 0 / {} | [] | [] | 3 | 3.355 |
| [S6/Q4](#s6) | success | ["sheet1", "sheet2"] | 2 / {'INNER': 1} | ["s1.Region", "s1.Segment", "SUBSTRING(s1.\"Order Date\", -4, 4)"] | ["COUNT(DISTINCT s1.\"Order ID\")", "COUNT(DISTINCT s1.\"Customer ID\")", "SUM(s2.Quantity)", "SUM(s2.Quantity * s2.\"Sales per Unit\")", "SUM(s2.Quantity * s2.\"Profit per Unit\")", "AVG(s2.Discount)", "SUM(s2.Quantity * (s2.\"Sales per Unit\" - s2.\"Profit per Unit\"))"] | 36 | 64.314 |
| [S7/Q5](#s7) | success | ["sheet1", "sheet2"] | 2 / {'INNER': 1} | ["Region", "Segment"] | ["COUNT(DISTINCT \"Order ID\")", "COUNT(DISTINCT \"Customer ID\")", "SUM(sales)", "SUM(profit)"] | 12 | 47.108 |
| [S8/Q6](#s8) | failed | ["sheet1", "sheet2"] | 2 / {'INNER': 1} | ["Region"] | ["COUNT(DISTINCT \"Order ID\")", "COUNT(DISTINCT \"Customer ID\")", "SUM(s2.Quantity)", "SUM(s2.Quantity * s2.\"Sales per Unit\")", "SUM(s2.Quantity * s2.\"Profit per Unit\")"] | unknown | 未取得；调用总时长 0.178 ms |
| [S9/Q7](#s9) | success | ["sheet1", "sheet2"] | 2 / {'INNER': 1} | ["s1.Region"] | ["COUNT(DISTINCT s1.\"Order ID\")", "COUNT(DISTINCT s1.\"Customer ID\")", "SUM(s2.Quantity)", "SUM(s2.Quantity * s2.\"Sales per Unit\")", "SUM(s2.Quantity * s2.\"Profit per Unit\")", "SUM(s2.Quantity * s2.\"Sales per Unit\")", "SUM(s2.Quantity * s2.\"Profit per Unit\")"] | 4 | 42.187 |
| [S10/Q8](#s10) | success | ["sheet1", "sheet2"] | 2 / {'INNER': 1} | ["s1.Segment"] | ["COUNT(DISTINCT s1.\"Order ID\")", "COUNT(DISTINCT s1.\"Customer ID\")", "SUM(s2.Quantity)", "SUM(s2.Quantity * s2.\"Sales per Unit\")", "SUM(s2.Quantity * s2.\"Profit per Unit\")", "SUM(s2.Quantity * s2.\"Sales per Unit\")", "SUM(s2.Quantity * s2.\"Profit per Unit\")"] | 3 | 41.461 |
| [S11/Q9](#s11) | success | ["sheet1", "sheet2"] | 2 / {'INNER': 1} | ["Region", "Segment", "year"] | ["SUM(sales)", "SUM(profit)", "SUM(sales)", "SUM(profit)"] | 36 | 44.295 |
| [S12/Q10](#s12) | success | ["sheet1", "sheet2"] | 2 / {'INNER': 1} | ["Region", "Segment", "year"] | ["COUNT(DISTINCT \"Order ID\")", "COUNT(DISTINCT \"Customer ID\")", "SUM(sales)", "SUM(profit)", "SUM(sales)", "SUM(profit)"] | 36 | 60.704 |
| [S13/Q11](#s13) | success | ["sheet1", "sheet2"] | 2 / {'INNER': 1} | ["Region", "Segment", "year"] | ["SUM(sales)", "SUM(profit)", "COUNT(DISTINCT \"Customer ID\")"] | 36 | 44.303 |
| [S14/Q12](#s14) | success | ["sheet1", "sheet2"] | 2 / {'INNER': 1} | ["Region", "Segment", "year"] | ["SUM(sales)", "SUM(profit)", "COUNT(DISTINCT cid)"] | 36 | 47.497 |
| [S15/Q13](#s15) | success | ["sheet1", "sheet2"] | 2 / {'INNER': 1} | ["Region", "Segment", "year"] | ["SUM(sales)", "SUM(profit)", "COUNT(DISTINCT cid)", "COUNT(DISTINCT oid)"] | 36 | 55.749 |
| [S16/Q14](#s16) | success | ["sheet1", "sheet2"] | 2 / {'INNER': 1} | ["Region", "Category"] | ["SUM(sales)", "SUM(profit)", "SUM(sales)", "SUM(profit)"] | 12 | 39.925 |
| [S17/Q15](#s17) | success | ["sheet1", "sheet2"] | 2 / {'INNER': 1} | ["Region", "Segment", "year"] | ["SUM(sales)", "SUM(profit)", "COUNT(DISTINCT cid)", "COUNT(DISTINCT oid)"] | 36 | 56.311 |
| [S18/Q16](#s18) | success | ["sheet1", "sheet2"] | 2 / {'INNER': 1} | ["Region", "Segment", "year"] | ["SUM(sales)", "SUM(profit)", "COUNT(DISTINCT cid)", "COUNT(DISTINCT oid)"] | 36 | 56.548 |
| [S19/Q17](#s19) | success | ["sheet1", "sheet2"] | 2 / {'INNER': 1} | ["Subcategory", "Region"] | ["SUM(sales)", "SUM(profit)", "SUM(sales)", "SUM(profit)"] | 68 | 38.393 |
| [S20/Q18](#s20) | success | ["sheet1"] | 0 / {} | ["Segment", "year"] | ["COUNT(DISTINCT cid)", "COUNT(DISTINCT cid)", "COUNT(DISTINCT cid)"] | 9 | 9.598 |
| [S21/Q19](#s21) | success | ["sheet1", "sheet2"] | 2 / {'INNER': 1} | ["Region", "Segment", "year"] | ["SUM(sales)", "SUM(profit)"] | 36 | 43.891 |
| [S22/Q20](#s22) | success | ["sheet1", "sheet2"] | 2 / {'INNER': 1} | ["Region", "Category"] | ["SUM(sales)", "SUM(profit)"] | 12 | 39.905 |
| [S23/Q21](#s23) | success | ["sheet1", "sheet2"] | 2 / {'INNER': 1} | ["Region", "Segment", "year"] | ["SUM(sales)", "SUM(profit)", "COUNT(DISTINCT cid)"] | 36 | 53.392 |
| [S24/Q22](#s24) | success | ["sheet1"] | 0 / {} | ["Region", "year"] | ["COUNT(DISTINCT cid)", "COUNT(DISTINCT cid)", "COUNT(DISTINCT cid)"] | 12 | 9.667 |
| [S25/Q23](#s25) | success | ["sheet1"] | 0 / {} | ["Region"] | ["COUNT(DISTINCT State)", "COUNT(DISTINCT City)", "COUNT(DISTINCT \"Customer ID\")"] | 4 | 10.0 |


## 元数据和设置

| SQL | 类别 | 状态 | 内容 |
| --- | --- | --- | --- |
| S1 | connection_setup | success | PRAGMA query_only=ON |
| S2 | metadata | success | SELECT name,sql FROM sqlite_master WHERE type='table' ORDER BY name |


## Python 与执行位置

人工源码审查：**database_first_violation**。SQL supplies the region-segment-year aggregate. P2 performs grouped rollups, merges yearly totals, computes penetration ratios and within-region/segment percentage changes in pandas before plotting. These are SQL-capable operations over a small aggregated result, not an unlogged database access. Rendering is allowed; the preparation is explicitly marked as a protocol deviation. [证据](../reviews/dacomp-024.json)。

P1：Creating summary figures for the report: region performance over years, region-segment-year sales/profit/margin trends, penetration shares, and a category view. These visualizations require matplotlib which SQLite cannot produce.

[源码](../../../runs/dsv4flash-db-first-full-01/dacomp-024/attempt-01/python/P1.py)；[输出](../../../runs/dsv4flash-db-first-full-01/dacomp-024/attempt-01/python/P1.stdout)；[错误](../../../runs/dsv4flash-db-first-full-01/dacomp-024/attempt-01/python/P1.stderr)。检出需人工核验的 SQL 可实现操作：.query(；不能仅凭理由判为合规。

P2：Computing derived metrics: profit margin, penetration shares, YoY growth, and creating all visualizations for the report. SQLite cannot produce plots.

[源码](../../../runs/dsv4flash-db-first-full-01/dacomp-024/attempt-01/python/P2.py)；[输出](../../../runs/dsv4flash-db-first-full-01/dacomp-024/attempt-01/python/P2.stdout)；[错误](../../../runs/dsv4flash-db-first-full-01/dacomp-024/attempt-01/python/P2.stderr)。检出需人工核验的 SQL 可实现操作：groupby(, .merge(, .query(, sort_values(；不能仅凭理由判为合规。

P3：Creating two additional figures for the report: (1) a heatmap of profit margin across region-segment-year to visualize differences, and (2) category profit by region for expansion recommendations. Matplotlib is required for these visualizations.

[源码](../../../runs/dsv4flash-db-first-full-01/dacomp-024/attempt-01/python/P3.py)；[输出](../../../runs/dsv4flash-db-first-full-01/dacomp-024/attempt-01/python/P3.stdout)；[错误](../../../runs/dsv4flash-db-first-full-01/dacomp-024/attempt-01/python/P3.stderr)。检出需人工核验的 SQL 可实现操作：.query(；不能仅凭理由判为合规。

## 优化机会

已验证候选。筛选限于精确 SQL、相同自包含 CTE、相同单表完整过滤、可分解单表聚合；未覆盖任意 Join 等价和一般谓词蕴含。全部候选都是 offline，未测在线预测。

| 候选 | 类型 | 已有结果 | 覆盖 SQL | 后续次数 | 中间行数 | 验证 | 成本 |
| --- | --- | --- | --- | --- | --- | --- | --- |
| C1 | exact-result reuse | True | ["S17", "S18"] | 1 | 36 | verified | Not benchmarked; correctness alone does not establish net speedup. |
| C2 | common subexpression | False | ["S7", "S12"] | 1 | 23897 | verified | Not benchmarked; correctness alone does not establish net speedup. |
| C3 | common subexpression | False | ["S11", "S13"] | 1 | unknown | not_verified_cap | Not tested |
| C4 | common subexpression | False | ["S15", "S17", "S18", "S23"] | 3 | 23897 | verified | Not benchmarked; correctness alone does not establish net speedup. |
| C5 | common subexpression | False | ["S20", "S24"] | 1 | unknown | not_verified_cap | Not tested |


已验证覆盖（含触发查询、候选并集去重）：6/22 条成功数据 SQL。正确性仅针对当前数据库快照；未测性能的候选不能声称已加速。

[完整 build/rewrite 与比较证据](dacomp-024.analysis.json)。

### C4：common subexpression

Identical self-contained CTE body across queries.

原查询 [S15](#s15), [S17](#s17), [S18](#s18), [S23](#s23) → 新增共享状态 C4 → 后续 3 次可复用。该构建点为事后假设，不代表 Agent 当时预知后续。

构建定义：

```sql
SELECT s1.Region, s1.Segment, SUBSTRING(s1."Order Date", -4, 4) AS year, s1."Customer ID" AS cid, s1."Order ID" AS oid, s2.Quantity * s2."Sales per Unit" AS sales, s2.Quantity * s2."Profit per Unit" AS profit FROM sheet1 AS s1 JOIN sheet2 AS s2 ON s1."Order ID" = s2."Order ID" WHERE SUBSTRING(s1."Order Date", -4, 4) IN ('2015', '2016', '2017')
```

受益查询 S15 的改写示例：

```sql
WITH base AS (SELECT * FROM temp.reuse_candidate), agg AS (SELECT Region, Segment, year, SUM(sales) AS sales, SUM(profit) AS profit, COUNT(DISTINCT cid) AS customers, COUNT(DISTINCT oid) AS orders FROM base GROUP BY Region, Segment, year) SELECT Region, Segment, year, ROUND(sales, 0) AS sales, ROUND(profit, 0) AS profit, customers, orders, ROUND(100.0 * sales / SUM(sales) OVER (PARTITION BY year), 1) AS pct_of_year_sales, ROUND(100.0 * customers / SUM(customers) OVER (PARTITION BY year), 1) AS pct_of_year_customers, ROUND(100.0 * profit / sales, 2) AS margin_pct, ROUND(profit / customers, 2) AS profit_per_customer, ROUND(sales / orders, 2) AS avg_order_value FROM agg ORDER BY year, sales DESC
```

| 原 SQL | 列名一致 | 结果一致 | 比较方法 |
| --- | --- | --- | --- |
| S15 | True | True | ordered_numeric_tolerance |
| S17 | True | True | ordered_numeric_tolerance |
| S18 | True | True | ordered_numeric_tolerance |
| S23 | True | True | exact_multiset |


验证状态：verified；成本结论：Not benchmarked; correctness alone does not establish net speedup.

### C1：exact-result reuse

Identical normalized SQL and parameters; archive equality checked.

原查询 [S17](#s17), [S18](#s18) → 保留前序结果 S17 → 后续 1 次可复用。该构建点为事后假设，不代表 Agent 当时预知后续。

| 原 SQL | 列名一致 | 结果一致 | 比较方法 |
| --- | --- | --- | --- |
| S18 | True | True | ordered_numeric_tolerance |


验证状态：verified；成本结论：Not benchmarked; correctness alone does not establish net speedup.

### C2：common subexpression

Identical self-contained CTE body across queries.

原查询 [S7](#s7), [S12](#s12) → 新增共享状态 C2 → 后续 1 次可复用。该构建点为事后假设，不代表 Agent 当时预知后续。

构建定义：

```sql
SELECT s1.Region, s1.Segment, SUBSTRING(s1."Order Date", -4, 4) AS year, s1."Order ID", s1."Customer ID", s2.Quantity, s2.Quantity * s2."Sales per Unit" AS sales, s2.Quantity * s2."Profit per Unit" AS profit FROM sheet1 AS s1 JOIN sheet2 AS s2 ON s1."Order ID" = s2."Order ID" WHERE SUBSTRING(s1."Order Date", -4, 4) IN ('2015', '2016', '2017')
```

受益查询 S7 的改写示例：

```sql
WITH base AS (SELECT * FROM temp.reuse_candidate), agg AS (SELECT Region, Segment, COUNT(DISTINCT "Order ID") AS orders, COUNT(DISTINCT "Customer ID") AS customers, SUM(sales) AS sales, SUM(profit) AS profit FROM base GROUP BY Region, Segment) SELECT Region, Segment, orders, customers, ROUND(sales, 0) AS sales, ROUND(profit, 0) AS profit, ROUND(100.0 * profit / sales, 2) AS profit_margin_pct, ROUND(100.0 * sales / SUM(sales) OVER (), 2) AS sales_share_pct, ROUND(100.0 * customers / SUM(customers) OVER (), 2) AS customer_share_pct, ROUND(sales / orders, 2) AS avg_order_value FROM agg ORDER BY sales DESC
```

| 原 SQL | 列名一致 | 结果一致 | 比较方法 |
| --- | --- | --- | --- |
| S7 | True | True | ordered_numeric_tolerance |
| S12 | True | True | ordered_numeric_tolerance |


验证状态：verified；成本结论：Not benchmarked; correctness alone does not establish net speedup.

结果依赖：自动记录 SQL→Python 的接口父调用，以及源码中引用归档文件的消费者；字面值相同不认定因果。模型方向选择需要人工读取消息，尚未做全面因果标注。

[原始报告](../../../runs/dsv4flash-db-first-full-01/dacomp-024/attempt-01/answer.md)；[统一消息](../../../runs/dsv4flash-db-first-full-01/dacomp-024/attempt-01/messages.jsonl)；[原始 OpenCode 事件](../../../runs/dsv4flash-db-first-full-01/dacomp-024/attempt-01/opencode.jsonl)；[SQL 引擎日志](../../../runs/dsv4flash-db-first-full-01/dacomp-024/attempt-01/sql_journal.jsonl)。

[可读报告（本地图片链接规范化）](../answers/dacomp-024.md)。原始回答保留，分析结论未改写。

## S1

类别 `connection_setup`；来源 `connection`；调用 `fa54f785307e4ad99a6f86c4b2a7af6d`；状态 `success`。

```sql
PRAGMA query_only=ON
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-024/attempt-01/sql/S1.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-024/attempt-01/sql/S1.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-024/attempt-01/results/S1.rows.jsonl)；完整：True；SHA256：`e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`。

## S2

类别 `metadata`；来源 `list_db`；调用 `fa54f785307e4ad99a6f86c4b2a7af6d`；状态 `success`。

```sql
SELECT name,sql FROM sqlite_master WHERE type='table' ORDER BY name
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-024/attempt-01/sql/S2.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-024/attempt-01/sql/S2.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-024/attempt-01/results/S2.rows.jsonl)；完整：True；SHA256：`692391a3c348b95402278c1c20b378172a20896412e209b248bcfd92604393d2`。

## S3

类别 `data`；来源 `query_db`；调用 `5711cc4318484ef39cc97dbe1bf1df23`；状态 `success`。

```sql
SELECT DISTINCT substr("Order Date", -4, 4) AS year FROM sheet1 ORDER BY year
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-024/attempt-01/sql/S3.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-024/attempt-01/sql/S3.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-024/attempt-01/results/S3.rows.jsonl)；完整：True；SHA256：`7dae251ddf361a6f65f9ed5514b0a12350476221252a38eedf5651575c9a3eca`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "sheet1", "kind": "base", "block": null, "base_tables": ["sheet1"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |


## S4

类别 `data`；来源 `query_db`；调用 `7eaa4f0d348643759b2840fc75bb1429`；状态 `success`。

```sql
SELECT DISTINCT Region FROM sheet1 ORDER BY Region
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-024/attempt-01/sql/S4.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-024/attempt-01/sql/S4.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-024/attempt-01/results/S4.rows.jsonl)；完整：True；SHA256：`59d481f9485790134e5906b7612b69829e6cab5a919ed6d95a242bb50491b3fb`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "sheet1", "kind": "base", "block": null, "base_tables": ["sheet1"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |


## S5

类别 `data`；来源 `query_db`；调用 `9d4af1b9785f4d089b68aeed5dd94789`；状态 `success`。

```sql
SELECT DISTINCT Segment FROM sheet1 ORDER BY Segment
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-024/attempt-01/sql/S5.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-024/attempt-01/sql/S5.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-024/attempt-01/results/S5.rows.jsonl)；完整：True；SHA256：`3e7df8f5639ae6b43e6cfe4a2fcfd421dad08749383ded52c443493c8bf806fc`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "sheet1", "kind": "base", "block": null, "base_tables": ["sheet1"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |


## S6

类别 `data`；来源 `query_db`；调用 `a7d4ffc4d22c46ebadfe523ab6520317`；状态 `success`。

```sql
SELECT s1.Region, s1.Segment, substr(s1."Order Date", -4, 4) AS year,
       COUNT(DISTINCT s1."Order ID") AS order_count,
       COUNT(DISTINCT s1."Customer ID") AS customer_count,
       SUM(s2.Quantity) AS total_quantity,
       SUM(s2.Quantity * s2."Sales per Unit") AS total_sales,
       SUM(s2.Quantity * s2."Profit per Unit") AS total_profit,
       AVG(s2.Discount) AS avg_discount,
       SUM(s2.Quantity * (s2."Sales per Unit" - s2."Profit per Unit")) AS total_cost
FROM sheet1 s1
JOIN sheet2 s2 ON s1."Order ID" = s2."Order ID"
WHERE substr(s1."Order Date", -4, 4) IN ('2015', '2016', '2017')
GROUP BY s1.Region, s1.Segment, year
ORDER BY Region, Segment, year
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-024/attempt-01/sql/S6.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-024/attempt-01/sql/S6.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-024/attempt-01/results/S6.rows.jsonl)；完整：True；SHA256：`f59fda3f9c7f02051af8807d33db675a3d6defe47804175a215c258959f95d1e`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "s1", "kind": "base", "block": null, "base_tables": ["sheet1"]}, {"alias": "s2", "kind": "base", "block": null, "base_tables": ["sheet2"]}] | [{"type": "INNER", "right": "sheet2 AS s2", "on": "s1.\"Order ID\" = s2.\"Order ID\"", "using": []}] | ["s1.Region", "s1.Segment", "SUBSTRING(s1.\"Order Date\", -4, 4)"] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(DISTINCT s1."Order ID") | [{"table": "sheet1", "column": "Order ID"}] | [] | False |
| B1 | COUNT(DISTINCT s1."Customer ID") | [{"table": "sheet1", "column": "Customer ID"}] | [] | False |
| B1 | SUM(s2.Quantity) | [{"table": "sheet2", "column": "Quantity"}] | [] | False |
| B1 | SUM(s2.Quantity * s2."Sales per Unit") | [{"table": "sheet2", "column": "Quantity"}, {"table": "sheet2", "column": "Sales per Unit"}] | [] | False |
| B1 | SUM(s2.Quantity * s2."Profit per Unit") | [{"table": "sheet2", "column": "Quantity"}, {"table": "sheet2", "column": "Profit per Unit"}] | [] | False |
| B1 | AVG(s2.Discount) | [{"table": "sheet2", "column": "Discount"}] | [] | False |
| B1 | SUM(s2.Quantity * (s2."Sales per Unit" - s2."Profit per Unit")) | [{"table": "sheet2", "column": "Quantity"}, {"table": "sheet2", "column": "Sales per Unit"}, {"table": "sheet2", "column": "Profit per Unit"}] | [] | False |


## S7

类别 `data`；来源 `query_db`；调用 `b1c25478cd6f4a2797bf184c9be10173`；状态 `success`。

```sql
WITH base AS (
  SELECT s1.Region, s1.Segment, substr(s1."Order Date", -4, 4) AS year,
         s1."Order ID", s1."Customer ID",
         s2.Quantity, s2.Quantity*s2."Sales per Unit" AS sales, s2.Quantity*s2."Profit per Unit" AS profit
  FROM sheet1 s1 JOIN sheet2 s2 ON s1."Order ID" = s2."Order ID"
  WHERE substr(s1."Order Date", -4, 4) IN ('2015','2016','2017')
),
agg AS (
  SELECT Region, Segment, COUNT(DISTINCT "Order ID") AS orders, COUNT(DISTINCT "Customer ID") AS customers,
         SUM(sales) AS sales, SUM(profit) AS profit
  FROM base GROUP BY Region, Segment
)
SELECT Region, Segment, orders, customers, ROUND(sales,0) AS sales, ROUND(profit,0) AS profit,
       ROUND(100.0*profit/sales,2) AS profit_margin_pct,
       ROUND(100.0*sales/SUM(sales) OVER (),2) AS sales_share_pct,
       ROUND(100.0*customers/SUM(customers) OVER (),2) AS customer_share_pct,
       ROUND(sales/orders,2) AS avg_order_value
FROM agg
ORDER BY sales DESC
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-024/attempt-01/sql/S7.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-024/attempt-01/sql/S7.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-024/attempt-01/results/S7.rows.jsonl)；完整：True；SHA256：`8ea9c236f06e69737ae3473dd667bced7b29e06fa61a4f6c418f5e1d1dda8316`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "s1", "kind": "base", "block": null, "base_tables": ["sheet1"]}, {"alias": "s2", "kind": "base", "block": null, "base_tables": ["sheet2"]}] | [{"type": "INNER", "right": "sheet2 AS s2", "on": "s1.\"Order ID\" = s2.\"Order ID\"", "using": []}] | [] |
| B2 | [{"alias": "base", "kind": "derived", "block": "B1", "base_tables": ["sheet1", "sheet2"]}] | [] | ["Region", "Segment"] |
| B3 | [{"alias": "agg", "kind": "derived", "block": "B2", "base_tables": ["sheet1", "sheet2"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B2 | COUNT(DISTINCT "Order ID") | [{"table": "sheet1", "column": "Order ID"}] | [] | False |
| B2 | COUNT(DISTINCT "Customer ID") | [{"table": "sheet1", "column": "Customer ID"}] | [] | False |
| B2 | SUM(sales) | [{"table": "sheet2", "column": "Quantity"}, {"table": "sheet2", "column": "Sales per Unit"}] | [] | False |
| B2 | SUM(profit) | [{"table": "sheet2", "column": "Quantity"}, {"table": "sheet2", "column": "Profit per Unit"}] | [] | False |


## S8

类别 `data`；来源 `query_db`；调用 `9845cfb8dd434ce19527aed71a5a05f6`；状态 `failed`。

```sql
SELECT Region,
       COUNT(DISTINCT "Order ID") AS orders,
       COUNT(DISTINCT "Customer ID") AS customers,
       SUM(s2.Quantity) AS qty,
       SUM(s2.Quantity*s2."Sales per Unit") AS sales,
       SUM(s2.Quantity*s2."Profit per Unit") AS profit
FROM sheet1 s1 JOIN sheet2 s2 ON s1."Order ID"=s2."Order ID"
WHERE substr(s1."Order Date",-4,4) IN ('2015','2016','2017')
GROUP BY Region ORDER BY sales DESC
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-024/attempt-01/sql/S8.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-024/attempt-01/sql/S8.parameters.json)。

错误：`OperationalError('ambiguous column name: Order ID')`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "s1", "kind": "base", "block": null, "base_tables": ["sheet1"]}, {"alias": "s2", "kind": "base", "block": null, "base_tables": ["sheet2"]}] | [{"type": "INNER", "right": "sheet2 AS s2", "on": "s1.\"Order ID\" = s2.\"Order ID\"", "using": []}] | ["Region"] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(DISTINCT "Order ID") | [{"unknown": "\"Order ID\""}] | [] | False |
| B1 | COUNT(DISTINCT "Customer ID") | [{"table": "sheet1", "column": "Customer ID"}] | [] | False |
| B1 | SUM(s2.Quantity) | [{"table": "sheet2", "column": "Quantity"}] | [] | False |
| B1 | SUM(s2.Quantity * s2."Sales per Unit") | [{"table": "sheet2", "column": "Quantity"}, {"table": "sheet2", "column": "Sales per Unit"}] | [] | False |
| B1 | SUM(s2.Quantity * s2."Profit per Unit") | [{"table": "sheet2", "column": "Quantity"}, {"table": "sheet2", "column": "Profit per Unit"}] | [] | False |


未解析列血缘：[{"block": "B1", "column": "\"Order ID\"", "reason": "ambiguous_or_missing_source"}, {"block": "B1", "column": "\"Order ID\"", "reason": "ambiguous_or_missing_source"}]

## S9

类别 `data`；来源 `query_db`；调用 `2049ee1ecdd44ba7a622ff7c20279c40`；状态 `success`。

```sql
SELECT s1.Region,
       COUNT(DISTINCT s1."Order ID") AS orders,
       COUNT(DISTINCT s1."Customer ID") AS customers,
       SUM(s2.Quantity) AS qty,
       SUM(s2.Quantity*s2."Sales per Unit") AS sales,
       SUM(s2.Quantity*s2."Profit per Unit") AS profit,
       ROUND(100.0*SUM(s2.Quantity*s2."Profit per Unit")/SUM(s2.Quantity*s2."Sales per Unit"),2) AS margin_pct
FROM sheet1 s1 JOIN sheet2 s2 ON s1."Order ID"=s2."Order ID"
WHERE substr(s1."Order Date",-4,4) IN ('2015','2016','2017')
GROUP BY s1.Region ORDER BY sales DESC
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-024/attempt-01/sql/S9.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-024/attempt-01/sql/S9.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-024/attempt-01/results/S9.rows.jsonl)；完整：True；SHA256：`69947031c86915c7248fd8e244c252f58d577d18caf22dc7915163ded21d344b`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "s1", "kind": "base", "block": null, "base_tables": ["sheet1"]}, {"alias": "s2", "kind": "base", "block": null, "base_tables": ["sheet2"]}] | [{"type": "INNER", "right": "sheet2 AS s2", "on": "s1.\"Order ID\" = s2.\"Order ID\"", "using": []}] | ["s1.Region"] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(DISTINCT s1."Order ID") | [{"table": "sheet1", "column": "Order ID"}] | [] | False |
| B1 | COUNT(DISTINCT s1."Customer ID") | [{"table": "sheet1", "column": "Customer ID"}] | [] | False |
| B1 | SUM(s2.Quantity) | [{"table": "sheet2", "column": "Quantity"}] | [] | False |
| B1 | SUM(s2.Quantity * s2."Sales per Unit") | [{"table": "sheet2", "column": "Quantity"}, {"table": "sheet2", "column": "Sales per Unit"}] | [] | False |
| B1 | SUM(s2.Quantity * s2."Profit per Unit") | [{"table": "sheet2", "column": "Quantity"}, {"table": "sheet2", "column": "Profit per Unit"}] | [] | False |
| B1 | SUM(s2.Quantity * s2."Sales per Unit") | [{"table": "sheet2", "column": "Quantity"}, {"table": "sheet2", "column": "Sales per Unit"}] | [] | False |
| B1 | SUM(s2.Quantity * s2."Profit per Unit") | [{"table": "sheet2", "column": "Quantity"}, {"table": "sheet2", "column": "Profit per Unit"}] | [] | False |


## S10

类别 `data`；来源 `query_db`；调用 `c45fe800e3f949adbd9b37d7a94f42fa`；状态 `success`。

```sql
SELECT s1.Segment,
       COUNT(DISTINCT s1."Order ID") AS orders,
       COUNT(DISTINCT s1."Customer ID") AS customers,
       SUM(s2.Quantity) AS qty,
       SUM(s2.Quantity*s2."Sales per Unit") AS sales,
       SUM(s2.Quantity*s2."Profit per Unit") AS profit,
       ROUND(100.0*SUM(s2.Quantity*s2."Profit per Unit")/SUM(s2.Quantity*s2."Sales per Unit"),2) AS margin_pct
FROM sheet1 s1 JOIN sheet2 s2 ON s1."Order ID"=s2."Order ID"
WHERE substr(s1."Order Date",-4,4) IN ('2015','2016','2017')
GROUP BY s1.Segment ORDER BY sales DESC
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-024/attempt-01/sql/S10.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-024/attempt-01/sql/S10.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-024/attempt-01/results/S10.rows.jsonl)；完整：True；SHA256：`d0c2ea58eefda4062e64eaa7471f007a95bd7abf740df033599772d32ce47d25`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "s1", "kind": "base", "block": null, "base_tables": ["sheet1"]}, {"alias": "s2", "kind": "base", "block": null, "base_tables": ["sheet2"]}] | [{"type": "INNER", "right": "sheet2 AS s2", "on": "s1.\"Order ID\" = s2.\"Order ID\"", "using": []}] | ["s1.Segment"] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(DISTINCT s1."Order ID") | [{"table": "sheet1", "column": "Order ID"}] | [] | False |
| B1 | COUNT(DISTINCT s1."Customer ID") | [{"table": "sheet1", "column": "Customer ID"}] | [] | False |
| B1 | SUM(s2.Quantity) | [{"table": "sheet2", "column": "Quantity"}] | [] | False |
| B1 | SUM(s2.Quantity * s2."Sales per Unit") | [{"table": "sheet2", "column": "Quantity"}, {"table": "sheet2", "column": "Sales per Unit"}] | [] | False |
| B1 | SUM(s2.Quantity * s2."Profit per Unit") | [{"table": "sheet2", "column": "Quantity"}, {"table": "sheet2", "column": "Profit per Unit"}] | [] | False |
| B1 | SUM(s2.Quantity * s2."Sales per Unit") | [{"table": "sheet2", "column": "Quantity"}, {"table": "sheet2", "column": "Sales per Unit"}] | [] | False |
| B1 | SUM(s2.Quantity * s2."Profit per Unit") | [{"table": "sheet2", "column": "Quantity"}, {"table": "sheet2", "column": "Profit per Unit"}] | [] | False |


## S11

类别 `data`；来源 `query_db`；调用 `192168b06fc9429680a69cc77c1eb479`；状态 `success`。

```sql
WITH base AS (
  SELECT s1.Region, s1.Segment, substr(s1."Order Date", -4, 4) AS year,
         s2.Quantity, s2.Quantity*s2."Sales per Unit" AS sales, s2.Quantity*s2."Profit per Unit" AS profit
  FROM sheet1 s1 JOIN sheet2 s2 ON s1."Order ID" = s2."Order ID"
  WHERE substr(s1."Order Date", -4, 4) IN ('2015','2016','2017')
)
SELECT Region, Segment, year,
       ROUND(SUM(sales),0) AS sales,
       ROUND(SUM(profit),0) AS profit,
       ROUND(100.0*SUM(profit)/SUM(sales),2) AS margin_pct
FROM base
GROUP BY Region, Segment, year
ORDER BY Region, Segment, year
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-024/attempt-01/sql/S11.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-024/attempt-01/sql/S11.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-024/attempt-01/results/S11.rows.jsonl)；完整：True；SHA256：`7bcc0eebeae80784b6ef45875f86c31bcdeca2fb081fe6940930c6d8dae6ec0b`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "s1", "kind": "base", "block": null, "base_tables": ["sheet1"]}, {"alias": "s2", "kind": "base", "block": null, "base_tables": ["sheet2"]}] | [{"type": "INNER", "right": "sheet2 AS s2", "on": "s1.\"Order ID\" = s2.\"Order ID\"", "using": []}] | [] |
| B2 | [{"alias": "base", "kind": "derived", "block": "B1", "base_tables": ["sheet1", "sheet2"]}] | [] | ["Region", "Segment", "year"] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B2 | SUM(sales) | [{"table": "sheet2", "column": "Quantity"}, {"table": "sheet2", "column": "Sales per Unit"}] | [] | False |
| B2 | SUM(profit) | [{"table": "sheet2", "column": "Quantity"}, {"table": "sheet2", "column": "Profit per Unit"}] | [] | False |
| B2 | SUM(sales) | [{"table": "sheet2", "column": "Quantity"}, {"table": "sheet2", "column": "Sales per Unit"}] | [] | False |
| B2 | SUM(profit) | [{"table": "sheet2", "column": "Quantity"}, {"table": "sheet2", "column": "Profit per Unit"}] | [] | False |


## S12

类别 `data`；来源 `query_db`；调用 `7fe761e7206640948dd5292b554d94e9`；状态 `success`。

```sql
WITH base AS (
  SELECT s1.Region, s1.Segment, substr(s1."Order Date", -4, 4) AS year,
         s1."Order ID", s1."Customer ID",
         s2.Quantity, s2.Quantity*s2."Sales per Unit" AS sales, s2.Quantity*s2."Profit per Unit" AS profit
  FROM sheet1 s1 JOIN sheet2 s2 ON s1."Order ID" = s2."Order ID"
  WHERE substr(s1."Order Date", -4, 4) IN ('2015','2016','2017')
)
SELECT Region, Segment, year,
       COUNT(DISTINCT "Order ID") AS orders,
       COUNT(DISTINCT "Customer ID") AS customers,
       ROUND(SUM(sales),2) AS sales,
       ROUND(SUM(profit),2) AS profit,
       ROUND(100.0*SUM(profit)/SUM(sales),2) AS margin_pct
FROM base
GROUP BY Region, Segment, year
ORDER BY Region, Segment, year
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-024/attempt-01/sql/S12.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-024/attempt-01/sql/S12.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-024/attempt-01/results/S12.rows.jsonl)；完整：True；SHA256：`5efd5c3681f9016401b14e25383ccfa69276c0c945d8cca128e0550a43b30d82`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "s1", "kind": "base", "block": null, "base_tables": ["sheet1"]}, {"alias": "s2", "kind": "base", "block": null, "base_tables": ["sheet2"]}] | [{"type": "INNER", "right": "sheet2 AS s2", "on": "s1.\"Order ID\" = s2.\"Order ID\"", "using": []}] | [] |
| B2 | [{"alias": "base", "kind": "derived", "block": "B1", "base_tables": ["sheet1", "sheet2"]}] | [] | ["Region", "Segment", "year"] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B2 | COUNT(DISTINCT "Order ID") | [{"table": "sheet1", "column": "Order ID"}] | [] | False |
| B2 | COUNT(DISTINCT "Customer ID") | [{"table": "sheet1", "column": "Customer ID"}] | [] | False |
| B2 | SUM(sales) | [{"table": "sheet2", "column": "Quantity"}, {"table": "sheet2", "column": "Sales per Unit"}] | [] | False |
| B2 | SUM(profit) | [{"table": "sheet2", "column": "Quantity"}, {"table": "sheet2", "column": "Profit per Unit"}] | [] | False |
| B2 | SUM(sales) | [{"table": "sheet2", "column": "Quantity"}, {"table": "sheet2", "column": "Sales per Unit"}] | [] | False |
| B2 | SUM(profit) | [{"table": "sheet2", "column": "Quantity"}, {"table": "sheet2", "column": "Profit per Unit"}] | [] | False |


## S13

类别 `data`；来源 `query_db`；调用 `70e5db79c0184dbeaccc454a816d3ac3`；状态 `success`。

```sql
WITH base AS (
  SELECT s1.Region, s1.Segment, substr(s1."Order Date", -4, 4) AS year,
         s2.Quantity, s2.Quantity*s2."Sales per Unit" AS sales, s2.Quantity*s2."Profit per Unit" AS profit
  FROM sheet1 s1 JOIN sheet2 s2 ON s1."Order ID" = s2."Order ID"
  WHERE substr(s1."Order Date", -4, 4) IN ('2015','2016','2017')
),
agg AS (
  SELECT Region, Segment, year, SUM(sales) AS sales, SUM(profit) AS profit,
         COUNT(DISTINCT "Customer ID") AS customers
  FROM base GROUP BY Region, Segment, year
)
SELECT Region, Segment, year, sales, profit, customers,
       ROUND(100.0*(sales - LAG(sales) OVER (PARTITION BY Region, Segment ORDER BY year))/LAG(sales) OVER (PARTITION BY Region, Segment ORDER BY year),1) AS sales_yoy_pct,
       ROUND(100.0*(profit - LAG(profit) OVER (PARTITION BY Region, Segment ORDER BY year))/NULLIF(LAG(profit) OVER (PARTITION BY Region, Segment ORDER BY year),0),1) AS profit_yoy_pct
FROM agg ORDER BY Region, Segment, year
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-024/attempt-01/sql/S13.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-024/attempt-01/sql/S13.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-024/attempt-01/results/S13.rows.jsonl)；完整：True；SHA256：`c6fcc5869b364a267db8e112a78a28c4433c596487a20e139f1538f91d9cbff4`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "s1", "kind": "base", "block": null, "base_tables": ["sheet1"]}, {"alias": "s2", "kind": "base", "block": null, "base_tables": ["sheet2"]}] | [{"type": "INNER", "right": "sheet2 AS s2", "on": "s1.\"Order ID\" = s2.\"Order ID\"", "using": []}] | [] |
| B2 | [{"alias": "base", "kind": "derived", "block": "B1", "base_tables": ["sheet1", "sheet2"]}] | [] | ["Region", "Segment", "year"] |
| B3 | [{"alias": "agg", "kind": "derived", "block": "B2", "base_tables": ["sheet1", "sheet2"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B2 | SUM(sales) | [{"table": "sheet2", "column": "Quantity"}, {"table": "sheet2", "column": "Sales per Unit"}] | [] | False |
| B2 | SUM(profit) | [{"table": "sheet2", "column": "Quantity"}, {"table": "sheet2", "column": "Profit per Unit"}] | [] | False |
| B2 | COUNT(DISTINCT "Customer ID") | [{"unknown": "\"Customer ID\""}] | [] | False |


未解析列血缘：[{"block": "B3", "column": "\"Customer ID\"", "reason": "ambiguous_or_missing_source"}, {"block": "B3", "column": "\"Customer ID\"", "reason": "ambiguous_or_missing_source"}, {"block": "B3", "column": "\"Customer ID\"", "reason": "ambiguous_or_missing_source"}]

## S14

类别 `data`；来源 `query_db`；调用 `2144f729774d4ab398137ffbc600cf11`；状态 `success`。

```sql
WITH base AS (
  SELECT s1.Region, s1.Segment, substr(s1."Order Date", -4, 4) AS year,
         s1."Customer ID" AS cid,
         s2.Quantity, s2.Quantity*s2."Sales per Unit" AS sales, s2.Quantity*s2."Profit per Unit" AS profit
  FROM sheet1 s1 JOIN sheet2 s2 ON s1."Order ID" = s2."Order ID"
  WHERE substr(s1."Order Date", -4, 4) IN ('2015','2016','2017')
),
agg AS (
  SELECT Region, Segment, year, SUM(sales) AS sales, SUM(profit) AS profit,
         COUNT(DISTINCT cid) AS customers
  FROM base GROUP BY Region, Segment, year
)
SELECT Region, Segment, year, ROUND(sales,0) AS sales, ROUND(profit,0) AS profit, customers,
       ROUND(100.0*(sales - LAG(sales) OVER (PARTITION BY Region, Segment ORDER BY year))/LAG(sales) OVER (PARTITION BY Region, Segment ORDER BY year),1) AS sales_yoy_pct,
       ROUND(100.0*(profit - LAG(profit) OVER (PARTITION BY Region, Segment ORDER BY year))/NULLIF(LAG(profit) OVER (PARTITION BY Region, Segment ORDER BY year),0),1) AS profit_yoy_pct
FROM agg ORDER BY Region, Segment, year
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-024/attempt-01/sql/S14.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-024/attempt-01/sql/S14.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-024/attempt-01/results/S14.rows.jsonl)；完整：True；SHA256：`8512144c0cfae0d4fadb7b82416608446cc4eb5afc11a99a33e4cafc8d012a15`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "s1", "kind": "base", "block": null, "base_tables": ["sheet1"]}, {"alias": "s2", "kind": "base", "block": null, "base_tables": ["sheet2"]}] | [{"type": "INNER", "right": "sheet2 AS s2", "on": "s1.\"Order ID\" = s2.\"Order ID\"", "using": []}] | [] |
| B2 | [{"alias": "base", "kind": "derived", "block": "B1", "base_tables": ["sheet1", "sheet2"]}] | [] | ["Region", "Segment", "year"] |
| B3 | [{"alias": "agg", "kind": "derived", "block": "B2", "base_tables": ["sheet1", "sheet2"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B2 | SUM(sales) | [{"table": "sheet2", "column": "Quantity"}, {"table": "sheet2", "column": "Sales per Unit"}] | [] | False |
| B2 | SUM(profit) | [{"table": "sheet2", "column": "Quantity"}, {"table": "sheet2", "column": "Profit per Unit"}] | [] | False |
| B2 | COUNT(DISTINCT cid) | [{"table": "sheet1", "column": "Customer ID"}] | [] | False |


## S15

类别 `data`；来源 `query_db`；调用 `c893f239d38744eeb53c2744b0d9b9e7`；状态 `success`。

```sql
WITH base AS (
  SELECT s1.Region, s1.Segment, substr(s1."Order Date", -4, 4) AS year,
         s1."Customer ID" AS cid, s1."Order ID" AS oid,
         s2.Quantity*s2."Sales per Unit" AS sales, s2.Quantity*s2."Profit per Unit" AS profit
  FROM sheet1 s1 JOIN sheet2 s2 ON s1."Order ID" = s2."Order ID"
  WHERE substr(s1."Order Date", -4, 4) IN ('2015','2016','2017')
),
agg AS (
  SELECT Region, Segment, year, SUM(sales) AS sales, SUM(profit) AS profit,
         COUNT(DISTINCT cid) AS customers, COUNT(DISTINCT oid) AS orders
  FROM base GROUP BY Region, Segment, year
)
SELECT Region, Segment, year, ROUND(sales,0) AS sales, ROUND(profit,0) AS profit,
       customers, orders,
       ROUND(100.0*sales/SUM(sales) OVER (PARTITION BY year),1) AS pct_of_year_sales,
       ROUND(100.0*customers/SUM(customers) OVER (PARTITION BY year),1) AS pct_of_year_customers,
       ROUND(100.0*profit/sales,2) AS margin_pct,
       ROUND(profit/customers,2) AS profit_per_customer,
       ROUND(sales/orders,2) AS avg_order_value
FROM agg
ORDER BY year, sales DESC
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-024/attempt-01/sql/S15.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-024/attempt-01/sql/S15.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-024/attempt-01/results/S15.rows.jsonl)；完整：True；SHA256：`833253eec51822893ced3b20d3782c6a0dee61ad3518e964412b45ecf15f4539`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "s1", "kind": "base", "block": null, "base_tables": ["sheet1"]}, {"alias": "s2", "kind": "base", "block": null, "base_tables": ["sheet2"]}] | [{"type": "INNER", "right": "sheet2 AS s2", "on": "s1.\"Order ID\" = s2.\"Order ID\"", "using": []}] | [] |
| B2 | [{"alias": "base", "kind": "derived", "block": "B1", "base_tables": ["sheet1", "sheet2"]}] | [] | ["Region", "Segment", "year"] |
| B3 | [{"alias": "agg", "kind": "derived", "block": "B2", "base_tables": ["sheet1", "sheet2"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B2 | SUM(sales) | [{"table": "sheet2", "column": "Quantity"}, {"table": "sheet2", "column": "Sales per Unit"}] | [] | False |
| B2 | SUM(profit) | [{"table": "sheet2", "column": "Quantity"}, {"table": "sheet2", "column": "Profit per Unit"}] | [] | False |
| B2 | COUNT(DISTINCT cid) | [{"table": "sheet1", "column": "Customer ID"}] | [] | False |
| B2 | COUNT(DISTINCT oid) | [{"table": "sheet1", "column": "Order ID"}] | [] | False |


## S16

类别 `data`；来源 `query_db`；调用 `3982b8dafab7418ba5ca231be9a6e8ee`；状态 `success`。

```sql
WITH base AS (
  SELECT s1.Region, substr(s1."Order Date", -4, 4) AS year, s2.Category, s2.Subcategory,
         s2.Quantity*s2."Sales per Unit" AS sales, s2.Quantity*s2."Profit per Unit" AS profit
  FROM sheet1 s1 JOIN sheet2 s2 ON s1."Order ID" = s2."Order ID"
  WHERE substr(s1."Order Date", -4, 4) IN ('2015','2016','2017')
)
SELECT Region, Category, ROUND(SUM(sales),0) AS sales, ROUND(SUM(profit),0) AS profit,
       ROUND(100.0*SUM(profit)/SUM(sales),2) AS margin_pct
FROM base GROUP BY Region, Category
ORDER BY Region, sales DESC
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-024/attempt-01/sql/S16.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-024/attempt-01/sql/S16.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-024/attempt-01/results/S16.rows.jsonl)；完整：True；SHA256：`d94d5c46ebe3a69e911875e0c5fc0cb71a42c88cce105c9d642c79e69acdf8a8`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "s1", "kind": "base", "block": null, "base_tables": ["sheet1"]}, {"alias": "s2", "kind": "base", "block": null, "base_tables": ["sheet2"]}] | [{"type": "INNER", "right": "sheet2 AS s2", "on": "s1.\"Order ID\" = s2.\"Order ID\"", "using": []}] | [] |
| B2 | [{"alias": "base", "kind": "derived", "block": "B1", "base_tables": ["sheet1", "sheet2"]}] | [] | ["Region", "Category"] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B2 | SUM(sales) | [{"table": "sheet2", "column": "Quantity"}, {"table": "sheet2", "column": "Sales per Unit"}] | [] | False |
| B2 | SUM(profit) | [{"table": "sheet2", "column": "Quantity"}, {"table": "sheet2", "column": "Profit per Unit"}] | [] | False |
| B2 | SUM(sales) | [{"table": "sheet2", "column": "Quantity"}, {"table": "sheet2", "column": "Sales per Unit"}] | [] | False |
| B2 | SUM(profit) | [{"table": "sheet2", "column": "Quantity"}, {"table": "sheet2", "column": "Profit per Unit"}] | [] | False |


## S17

类别 `data`；来源 `python`；调用 `158bc624564744959a54c634da75bb5a`；状态 `success`。

```sql

WITH base AS (
  SELECT s1.Region, s1.Segment, substr(s1."Order Date", -4, 4) AS year,
         s1."Customer ID" AS cid, s1."Order ID" AS oid,
         s2.Quantity*s2."Sales per Unit" AS sales, s2.Quantity*s2."Profit per Unit" AS profit
  FROM sheet1 s1 JOIN sheet2 s2 ON s1."Order ID" = s2."Order ID"
  WHERE substr(s1."Order Date", -4, 4) IN ('2015','2016','2017')
)
SELECT Region, Segment, year, SUM(sales) AS sales, SUM(profit) AS profit,
       COUNT(DISTINCT cid) AS customers, COUNT(DISTINCT oid) AS orders
FROM base GROUP BY Region, Segment, year
ORDER BY year, Region, Segment

```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-024/attempt-01/sql/S17.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-024/attempt-01/sql/S17.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-024/attempt-01/results/S17.rows.jsonl)；完整：True；SHA256：`f1cb53ffd426702710e8b2bb6c13a5efe25b06894b86ef85420051e6fdba1472`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "s1", "kind": "base", "block": null, "base_tables": ["sheet1"]}, {"alias": "s2", "kind": "base", "block": null, "base_tables": ["sheet2"]}] | [{"type": "INNER", "right": "sheet2 AS s2", "on": "s1.\"Order ID\" = s2.\"Order ID\"", "using": []}] | [] |
| B2 | [{"alias": "base", "kind": "derived", "block": "B1", "base_tables": ["sheet1", "sheet2"]}] | [] | ["Region", "Segment", "year"] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B2 | SUM(sales) | [{"table": "sheet2", "column": "Quantity"}, {"table": "sheet2", "column": "Sales per Unit"}] | [] | False |
| B2 | SUM(profit) | [{"table": "sheet2", "column": "Quantity"}, {"table": "sheet2", "column": "Profit per Unit"}] | [] | False |
| B2 | COUNT(DISTINCT cid) | [{"table": "sheet1", "column": "Customer ID"}] | [] | False |
| B2 | COUNT(DISTINCT oid) | [{"table": "sheet1", "column": "Order ID"}] | [] | False |


## S18

类别 `data`；来源 `python`；调用 `8ccc0f398a344aff9c9960012810adfa`；状态 `success`。

```sql

WITH base AS (
  SELECT s1.Region, s1.Segment, substr(s1."Order Date", -4, 4) AS year,
         s1."Customer ID" AS cid, s1."Order ID" AS oid,
         s2.Quantity*s2."Sales per Unit" AS sales, s2.Quantity*s2."Profit per Unit" AS profit
  FROM sheet1 s1 JOIN sheet2 s2 ON s1."Order ID" = s2."Order ID"
  WHERE substr(s1."Order Date", -4, 4) IN ('2015','2016','2017')
)
SELECT Region, Segment, year, SUM(sales) AS sales, SUM(profit) AS profit,
       COUNT(DISTINCT cid) AS customers, COUNT(DISTINCT oid) AS orders
FROM base GROUP BY Region, Segment, year
ORDER BY year, Region, Segment

```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-024/attempt-01/sql/S18.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-024/attempt-01/sql/S18.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-024/attempt-01/results/S18.rows.jsonl)；完整：True；SHA256：`f1cb53ffd426702710e8b2bb6c13a5efe25b06894b86ef85420051e6fdba1472`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "s1", "kind": "base", "block": null, "base_tables": ["sheet1"]}, {"alias": "s2", "kind": "base", "block": null, "base_tables": ["sheet2"]}] | [{"type": "INNER", "right": "sheet2 AS s2", "on": "s1.\"Order ID\" = s2.\"Order ID\"", "using": []}] | [] |
| B2 | [{"alias": "base", "kind": "derived", "block": "B1", "base_tables": ["sheet1", "sheet2"]}] | [] | ["Region", "Segment", "year"] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B2 | SUM(sales) | [{"table": "sheet2", "column": "Quantity"}, {"table": "sheet2", "column": "Sales per Unit"}] | [] | False |
| B2 | SUM(profit) | [{"table": "sheet2", "column": "Quantity"}, {"table": "sheet2", "column": "Profit per Unit"}] | [] | False |
| B2 | COUNT(DISTINCT cid) | [{"table": "sheet1", "column": "Customer ID"}] | [] | False |
| B2 | COUNT(DISTINCT oid) | [{"table": "sheet1", "column": "Order ID"}] | [] | False |


## S19

类别 `data`；来源 `query_db`；调用 `bdcc531637a741acb070ce7e87697dea`；状态 `success`。

```sql
WITH base AS (
  SELECT s1.Region, substr(s1."Order Date", -4, 4) AS year, s2.Subcategory,
         s2.Quantity*s2."Sales per Unit" AS sales, s2.Quantity*s2."Profit per Unit" AS profit
  FROM sheet1 s1 JOIN sheet2 s2 ON s1."Order ID" = s2."Order ID"
  WHERE substr(s1."Order Date", -4, 4) IN ('2015','2016','2017')
)
SELECT Subcategory, Region, ROUND(SUM(sales),0) AS sales, ROUND(SUM(profit),0) AS profit,
       ROUND(100.0*SUM(profit)/SUM(sales),2) AS margin_pct
FROM base GROUP BY Subcategory, Region
ORDER BY Subcategory, sales DESC
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-024/attempt-01/sql/S19.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-024/attempt-01/sql/S19.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-024/attempt-01/results/S19.rows.jsonl)；完整：True；SHA256：`1b49b6e00f8eea6c9a109da273d06b91463a772d0c6c1d68ee167890762ede45`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "s1", "kind": "base", "block": null, "base_tables": ["sheet1"]}, {"alias": "s2", "kind": "base", "block": null, "base_tables": ["sheet2"]}] | [{"type": "INNER", "right": "sheet2 AS s2", "on": "s1.\"Order ID\" = s2.\"Order ID\"", "using": []}] | [] |
| B2 | [{"alias": "base", "kind": "derived", "block": "B1", "base_tables": ["sheet1", "sheet2"]}] | [] | ["Subcategory", "Region"] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B2 | SUM(sales) | [{"table": "sheet2", "column": "Quantity"}, {"table": "sheet2", "column": "Sales per Unit"}] | [] | False |
| B2 | SUM(profit) | [{"table": "sheet2", "column": "Quantity"}, {"table": "sheet2", "column": "Profit per Unit"}] | [] | False |
| B2 | SUM(sales) | [{"table": "sheet2", "column": "Quantity"}, {"table": "sheet2", "column": "Sales per Unit"}] | [] | False |
| B2 | SUM(profit) | [{"table": "sheet2", "column": "Quantity"}, {"table": "sheet2", "column": "Profit per Unit"}] | [] | False |


## S20

类别 `data`；来源 `query_db`；调用 `8ec68e5517d642398e85614bdee285f6`；状态 `success`。

```sql
WITH base AS (
  SELECT s1.Region, s1.Segment, substr(s1."Order Date", -4, 4) AS year, s1."Customer ID" AS cid
  FROM sheet1 s1
  WHERE substr(s1."Order Date", -4, 4) IN ('2015','2016','2017')
)
SELECT Segment, year, COUNT(DISTINCT cid) AS customers,
       ROUND(100.0*COUNT(DISTINCT cid)/SUM(COUNT(DISTINCT cid)) OVER (PARTITION BY year),1) AS segment_customer_share_pct
FROM base GROUP BY Segment, year
ORDER BY Segment, year
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-024/attempt-01/sql/S20.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-024/attempt-01/sql/S20.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-024/attempt-01/results/S20.rows.jsonl)；完整：True；SHA256：`39c19300830ab8bfebfeff174ec9d03c7946792607a329c44a8eb41704e65916`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "s1", "kind": "base", "block": null, "base_tables": ["sheet1"]}] | [] | [] |
| B2 | [{"alias": "base", "kind": "derived", "block": "B1", "base_tables": ["sheet1"]}] | [] | ["Segment", "year"] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B2 | COUNT(DISTINCT cid) | [{"table": "sheet1", "column": "Customer ID"}] | [] | False |
| B2 | COUNT(DISTINCT cid) | [{"table": "sheet1", "column": "Customer ID"}] | [] | False |
| B2 | COUNT(DISTINCT cid) | [{"table": "sheet1", "column": "Customer ID"}] | [] | False |


## S21

类别 `data`；来源 `python`；调用 `0d3e78be58034a5c9e9bce7f863057a2`；状态 `success`。

```sql

WITH base AS (
  SELECT s1.Region, s1.Segment, substr(s1."Order Date", -4, 4) AS year,
         s2.Quantity*s2."Sales per Unit" AS sales, s2.Quantity*s2."Profit per Unit" AS profit
  FROM sheet1 s1 JOIN sheet2 s2 ON s1."Order ID" = s2."Order ID"
  WHERE substr(s1."Order Date", -4, 4) IN ('2015','2016','2017')
)
SELECT Region, Segment, year, SUM(sales) AS sales, SUM(profit) AS profit
FROM base GROUP BY Region, Segment, year

```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-024/attempt-01/sql/S21.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-024/attempt-01/sql/S21.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-024/attempt-01/results/S21.rows.jsonl)；完整：True；SHA256：`a41b59deb2e5166681a99625b653520d54f0802d7d77ae7195436873b98445db`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "s1", "kind": "base", "block": null, "base_tables": ["sheet1"]}, {"alias": "s2", "kind": "base", "block": null, "base_tables": ["sheet2"]}] | [{"type": "INNER", "right": "sheet2 AS s2", "on": "s1.\"Order ID\" = s2.\"Order ID\"", "using": []}] | [] |
| B2 | [{"alias": "base", "kind": "derived", "block": "B1", "base_tables": ["sheet1", "sheet2"]}] | [] | ["Region", "Segment", "year"] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B2 | SUM(sales) | [{"table": "sheet2", "column": "Quantity"}, {"table": "sheet2", "column": "Sales per Unit"}] | [] | False |
| B2 | SUM(profit) | [{"table": "sheet2", "column": "Quantity"}, {"table": "sheet2", "column": "Profit per Unit"}] | [] | False |


## S22

类别 `data`；来源 `python`；调用 `0d3e78be58034a5c9e9bce7f863057a2`；状态 `success`。

```sql

WITH base AS (
  SELECT s1.Region, s2.Category, s2.Quantity*s2."Sales per Unit" AS sales,
         s2.Quantity*s2."Profit per Unit" AS profit
  FROM sheet1 s1 JOIN sheet2 s2 ON s1."Order ID" = s2."Order ID"
  WHERE substr(s1."Order Date", -4, 4) IN ('2015','2016','2017')
)
SELECT Region, Category, SUM(sales) AS sales, SUM(profit) AS profit FROM base GROUP BY Region, Category

```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-024/attempt-01/sql/S22.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-024/attempt-01/sql/S22.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-024/attempt-01/results/S22.rows.jsonl)；完整：True；SHA256：`1705881df62f4c73515fd9ec5d2a6c3bf38033b00ab108203c20d509c63d16e5`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "s1", "kind": "base", "block": null, "base_tables": ["sheet1"]}, {"alias": "s2", "kind": "base", "block": null, "base_tables": ["sheet2"]}] | [{"type": "INNER", "right": "sheet2 AS s2", "on": "s1.\"Order ID\" = s2.\"Order ID\"", "using": []}] | [] |
| B2 | [{"alias": "base", "kind": "derived", "block": "B1", "base_tables": ["sheet1", "sheet2"]}] | [] | ["Region", "Category"] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B2 | SUM(sales) | [{"table": "sheet2", "column": "Quantity"}, {"table": "sheet2", "column": "Sales per Unit"}] | [] | False |
| B2 | SUM(profit) | [{"table": "sheet2", "column": "Quantity"}, {"table": "sheet2", "column": "Profit per Unit"}] | [] | False |


## S23

类别 `data`；来源 `python`；调用 `0d3e78be58034a5c9e9bce7f863057a2`；状态 `success`。

```sql

WITH base AS (
  SELECT s1.Region, s1.Segment, substr(s1."Order Date", -4, 4) AS year,
         s1."Customer ID" AS cid, s1."Order ID" AS oid,
         s2.Quantity*s2."Sales per Unit" AS sales, s2.Quantity*s2."Profit per Unit" AS profit
  FROM sheet1 s1 JOIN sheet2 s2 ON s1."Order ID" = s2."Order ID"
  WHERE substr(s1."Order Date", -4, 4) IN ('2015','2016','2017')
)
SELECT Region, Segment, year, SUM(sales) AS sales, SUM(profit) AS profit,
       COUNT(DISTINCT cid) AS customers
FROM base GROUP BY Region, Segment, year

```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-024/attempt-01/sql/S23.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-024/attempt-01/sql/S23.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-024/attempt-01/results/S23.rows.jsonl)；完整：True；SHA256：`914b9af1fc5d51e3909852eadaa50feac599b99849aae33d41fd72576ebff8a7`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "s1", "kind": "base", "block": null, "base_tables": ["sheet1"]}, {"alias": "s2", "kind": "base", "block": null, "base_tables": ["sheet2"]}] | [{"type": "INNER", "right": "sheet2 AS s2", "on": "s1.\"Order ID\" = s2.\"Order ID\"", "using": []}] | [] |
| B2 | [{"alias": "base", "kind": "derived", "block": "B1", "base_tables": ["sheet1", "sheet2"]}] | [] | ["Region", "Segment", "year"] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B2 | SUM(sales) | [{"table": "sheet2", "column": "Quantity"}, {"table": "sheet2", "column": "Sales per Unit"}] | [] | False |
| B2 | SUM(profit) | [{"table": "sheet2", "column": "Quantity"}, {"table": "sheet2", "column": "Profit per Unit"}] | [] | False |
| B2 | COUNT(DISTINCT cid) | [{"table": "sheet1", "column": "Customer ID"}] | [] | False |


## S24

类别 `data`；来源 `query_db`；调用 `270e0ff102a2467bb9aaa949c4e5c0d4`；状态 `success`。

```sql
WITH base AS (
  SELECT s1.Region, s1.Segment, substr(s1."Order Date", -4, 4) AS year, s1."Customer ID" AS cid
  FROM sheet1 s1
  WHERE substr(s1."Order Date", -4, 4) IN ('2015','2016','2017')
)
SELECT Region, year, COUNT(DISTINCT cid) AS customers,
       ROUND(100.0*COUNT(DISTINCT cid)/SUM(COUNT(DISTINCT cid)) OVER (PARTITION BY year),1) AS customer_share_pct
FROM base GROUP BY Region, year
ORDER BY year, customers DESC
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-024/attempt-01/sql/S24.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-024/attempt-01/sql/S24.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-024/attempt-01/results/S24.rows.jsonl)；完整：True；SHA256：`75707672927a2c7817e6e5ffba8021740d122f75a63e1669a60e18cffde538fd`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "s1", "kind": "base", "block": null, "base_tables": ["sheet1"]}] | [] | [] |
| B2 | [{"alias": "base", "kind": "derived", "block": "B1", "base_tables": ["sheet1"]}] | [] | ["Region", "year"] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B2 | COUNT(DISTINCT cid) | [{"table": "sheet1", "column": "Customer ID"}] | [] | False |
| B2 | COUNT(DISTINCT cid) | [{"table": "sheet1", "column": "Customer ID"}] | [] | False |
| B2 | COUNT(DISTINCT cid) | [{"table": "sheet1", "column": "Customer ID"}] | [] | False |


## S25

类别 `data`；来源 `query_db`；调用 `752b5b63a09a447f8e3b98f6761cbcf1`；状态 `success`。

```sql
SELECT Region, COUNT(DISTINCT State) AS states, COUNT(DISTINCT City) AS cities,
       COUNT(DISTINCT "Customer ID") AS total_customers_2015_17
FROM sheet1
WHERE substr("Order Date", -4, 4) IN ('2015','2016','2017')
GROUP BY Region ORDER BY total_customers_2015_17 DESC
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-024/attempt-01/sql/S25.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-024/attempt-01/sql/S25.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-024/attempt-01/results/S25.rows.jsonl)；完整：True；SHA256：`7d9b284e7081b6047fcd0da5582c509ecbab0e2fe8b11708db04d7a251c7e20e`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "sheet1", "kind": "base", "block": null, "base_tables": ["sheet1"]}] | [] | ["Region"] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(DISTINCT State) | [{"table": "sheet1", "column": "State"}] | [] | False |
| B1 | COUNT(DISTINCT City) | [{"table": "sheet1", "column": "City"}] | [] | False |
| B1 | COUNT(DISTINCT "Customer ID") | [{"table": "sheet1", "column": "Customer ID"}] | [] | False |

