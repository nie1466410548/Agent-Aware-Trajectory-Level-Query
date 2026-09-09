# dacomp-023

Analyze the sales trends from 2015 to 2018 for the three categories—Office Supplies, Techn…

运行：已提交。官方未评分。全部 SQL 尝试/成功 37/37；数据 SQL 35/35；Python 5 次。

完整原题：

Analyze the sales trends from 2015 to 2018 for the three categories—Office Supplies, Technology, and Furniture—identify the fastest-growing product category each year, and, combined with regional sales data, assess performance differences among Regional Managers across regions.

| 表 | 行数 | 列数 |
| --- | --- | --- |
| order | 9959 | 20 |
| return | 1163 | 2 |
| salesperson | 6 | 2 |


实际路线（分析者依据 SQL/源码概括，不代表 Agent 自述）：按品类×年份计算销售与增长 → 关联区域经理并比较区域表现 → 绘制品类/区域趋势 → 对订单销售额作区域差异检验。

数据库大小：4,747,264 字节。

## 数据 SQL

| SQL | 状态 | 基础表 | Join 输入/类型 | GROUP BY | 聚合表达式 | 结果行数 | 数据库 ms |
| --- | --- | --- | --- | --- | --- | --- | --- |
| [S3/Q1](#s3) | success | ["salesperson"] | 0 / {} | [] | [] | 6 | 0.375 |
| [S4/Q2](#s4) | success | ["\"order\""] | 0 / {} | [] | ["MIN(\"Order Date\")", "MAX(\"Order Date\")", "COUNT(*)"] | 1 | 3.219 |
| [S5/Q3](#s5) | success | ["\"order\""] | 0 / {} | [] | [] | 3 | 2.529 |
| [S6/Q4](#s6) | success | ["\"order\""] | 0 / {} | [] | [] | 6 | 2.59 |
| [S7/Q5](#s7) | success | ["\"order\""] | 0 / {} | ["Category", "CAST(STRFTIME('%Y', \"Order Date\") AS INTEGER)"] | ["SUM(Sales)", "SUM(Quantity)", "SUM(profit)"] | 12 | 16.264 |
| [S8/Q6](#s8) | success | ["\"order\""] | 0 / {} | ["CAST(STRFTIME('%Y', \"Order Date\") AS INTEGER)"] | ["COUNT(*)", "COUNT(DISTINCT \"Order ID\")"] | 4 | 10.798 |
| [S9/Q7](#s9) | success | ["\"order\""] | 0 / {} | ["Category", "CAST(STRFTIME('%Y', \"Order Date\") AS INTEGER)"] | ["SUM(Sales)"] | 12 | 10.409 |
| [S10/Q8](#s10) | success | ["\"order\"", "salesperson"] | 2 / {'LEFT': 1} | ["o.Region", "sp.\"Regional Manager\"", "CAST(STRFTIME('%Y', o.\"Order Date\") AS INTEGER)"] | ["SUM(o.Sales)", "SUM(o.profit)", "COUNT(DISTINCT o.\"Order ID\")"] | 24 | 17.769 |
| [S11/Q9](#s11) | success | ["\"order\"", "salesperson"] | 2 / {'LEFT': 1} | ["o.Region", "sp.\"Regional Manager\"", "CAST(STRFTIME('%Y', o.\"Order Date\") AS INTEGER)"] | ["SUM(o.Sales)", "SUM(o.profit)", "COUNT(DISTINCT o.\"Order ID\")"] | 24 | 18.697 |
| [S12/Q10](#s12) | success | ["\"order\"", "salesperson"] | 2 / {'LEFT': 1} | ["o.Region", "sp.\"Regional Manager\""] | ["SUM(o.Sales)", "SUM(o.profit)", "COUNT(DISTINCT o.\"Order ID\")", "COUNT(*)", "SUM(o.Sales)", "SUM(o.profit)"] | 6 | 13.294 |
| [S13/Q11](#s13) | success | ["\"order\"", "salesperson"] | 2 / {'LEFT': 1} | ["o.Region", "sp.\"Regional Manager\"", "CAST(STRFTIME('%Y', o.\"Order Date\") AS INTEGER)"] | ["SUM(o.Sales)"] | 12 | 6.946 |
| [S14/Q12](#s14) | success | ["\"order\"", "\"return\"", "salesperson"] | 3 / {'LEFT': 2} | ["o.Region", "sp.\"Regional Manager\"", "r.\"Return\""] | ["COUNT(*)", "COUNT(DISTINCT o.\"Order ID\")"] | 12 | 22.491 |
| [S15/Q13](#s15) | success | ["\"order\"", "\"return\"", "salesperson"] | 3 / {'LEFT': 2} | ["Region", "\"Regional Manager\""] | ["COUNT(DISTINCT \"Order ID\")", "SUM(is_returned)", "COUNT(DISTINCT \"Order ID\")", "SUM(is_returned)"] | 6 | 22.851 |
| [S16/Q14](#s16) | success | ["\"order\"", "salesperson"] | 2 / {'LEFT': 1} | ["o.Region", "sp.\"Regional Manager\"", "o.Category"] | ["SUM(o.Sales)", "SUM(o.Sales)", "SUM(o.Sales)"] | 18 | 11.866 |
| [S17/Q15](#s17) | success | ["\"order\""] | 0 / {} | ["Category", "CAST(STRFTIME('%Y', \"Order Date\") AS INTEGER)"] | ["SUM(Sales)", "SUM(Quantity)", "SUM(profit)"] | 12 | 12.121 |
| [S18/Q16](#s18) | success | ["\"order\""] | 0 / {} | ["Category", "CAST(STRFTIME('%Y', \"Order Date\") AS INTEGER)"] | ["SUM(Sales)"] | 12 | 9.999 |
| [S19/Q17](#s19) | success | ["\"order\"", "salesperson"] | 2 / {'LEFT': 1} | ["o.Region", "sp.\"Regional Manager\"", "CAST(STRFTIME('%Y', o.\"Order Date\") AS INTEGER)"] | ["SUM(o.Sales)", "SUM(o.profit)", "COUNT(DISTINCT o.\"Order ID\")"] | 24 | 17.97 |
| [S20/Q18](#s20) | success | ["\"order\"", "salesperson"] | 2 / {'LEFT': 1} | ["o.Region", "sp.\"Regional Manager\""] | ["SUM(o.Sales)", "SUM(o.profit)", "COUNT(DISTINCT o.\"Order ID\")", "COUNT(*)", "SUM(o.Sales)", "SUM(o.profit)"] | 6 | 12.522 |
| [S21/Q19](#s21) | success | ["\"order\"", "\"return\"", "salesperson"] | 3 / {'LEFT': 2} | ["Region", "\"Regional Manager\""] | ["COUNT(DISTINCT \"Order ID\")", "SUM(is_returned)", "COUNT(DISTINCT \"Order ID\")", "SUM(is_returned)"] | 6 | 22.005 |
| [S22/Q20](#s22) | success | ["\"order\"", "salesperson"] | 2 / {'LEFT': 1} | ["o.Region", "sp.\"Regional Manager\"", "o.Category"] | ["SUM(o.Sales)", "SUM(o.Sales)", "SUM(o.Sales)"] | 18 | 11.885 |
| [S23/Q21](#s23) | success | ["\"order\""] | 0 / {} | ["Category", "CAST(STRFTIME('%Y', \"Order Date\") AS INTEGER)"] | ["SUM(Sales)", "SUM(Quantity)", "SUM(profit)"] | 12 | 11.593 |
| [S24/Q22](#s24) | success | ["\"order\""] | 0 / {} | ["Category", "CAST(STRFTIME('%Y', \"Order Date\") AS INTEGER)"] | ["SUM(Sales)"] | 12 | 9.809 |
| [S25/Q23](#s25) | success | ["\"order\"", "salesperson"] | 2 / {'LEFT': 1} | ["o.Region", "sp.\"Regional Manager\"", "CAST(STRFTIME('%Y', o.\"Order Date\") AS INTEGER)"] | ["SUM(o.Sales)", "SUM(o.profit)", "COUNT(DISTINCT o.\"Order ID\")"] | 24 | 17.028 |
| [S26/Q24](#s26) | success | ["\"order\"", "salesperson"] | 2 / {'LEFT': 1} | ["o.Region", "sp.\"Regional Manager\""] | ["SUM(o.Sales)", "SUM(o.profit)", "COUNT(DISTINCT o.\"Order ID\")", "COUNT(*)", "SUM(o.Sales)", "SUM(o.profit)"] | 6 | 12.264 |
| [S27/Q25](#s27) | success | ["\"order\"", "\"return\"", "salesperson"] | 3 / {'LEFT': 2} | ["Region", "\"Regional Manager\""] | ["COUNT(DISTINCT \"Order ID\")", "SUM(is_returned)", "COUNT(DISTINCT \"Order ID\")", "SUM(is_returned)"] | 6 | 21.502 |
| [S28/Q26](#s28) | success | ["\"order\"", "salesperson"] | 2 / {'LEFT': 1} | ["o.Region", "sp.\"Regional Manager\"", "o.Category"] | ["SUM(o.Sales)", "SUM(o.Sales)", "SUM(o.Sales)"] | 18 | 11.182 |
| [S29/Q27](#s29) | success | ["\"order\""] | 0 / {} | ["Category", "CAST(STRFTIME('%Y', \"Order Date\") AS INTEGER)"] | ["SUM(Sales)"] | 9 | 10.109 |
| [S30/Q28](#s30) | success | ["\"order\""] | 2 / {'INNER': 1} | ["Category", "CAST(STRFTIME('%Y', \"Order Date\") AS INTEGER)"] | ["SUM(Sales)"] | 3 | 10.172 |
| [S31/Q29](#s31) | success | ["\"order\"", "salesperson"] | 2 / {'LEFT': 1} | ["o.Region", "sp.\"Regional Manager\""] | ["COUNT(DISTINCT o.\"Order ID\")", "SUM(o.Sales)", "COUNT(DISTINCT o.\"Order ID\")", "SUM(o.profit)", "COUNT(DISTINCT o.\"Order ID\")", "SUM(o.Sales)", "COUNT(*)", "SUM(o.profit)", "SUM(o.Sales)"] | 6 | 13.099 |
| [S32/Q30](#s32) | success | ["\"order\"", "salesperson"] | 2 / {'LEFT': 1} | ["o.Region", "CAST(STRFTIME('%Y', o.\"Order Date\") AS INTEGER)"] | ["SUM(o.Sales)", "COUNT(DISTINCT o.\"Order ID\")"] | 18 | 12.815 |
| [S33/Q31](#s33) | success | ["\"order\"", "salesperson"] | 2 / {'LEFT': 1} | ["o.Region", "sp.\"Regional Manager\""] | ["SUM(o.Quantity)", "AVG(o.Discount)", "SUM(o.Sales)", "SUM(o.Quantity)"] | 6 | 9.919 |
| [S34/Q32](#s34) | success | ["\"order\""] | 0 / {} | ["CAST(STRFTIME('%Y', \"Order Date\") AS INTEGER)"] | ["SUM(Sales)", "SUM(profit)", "SUM(Sales)", "SUM(profit)"] | 4 | 8.265 |
| [S35/Q33](#s35) | success | ["\"order\""] | 0 / {} | ["Category", "CAST(STRFTIME('%Y', \"Order Date\") AS INTEGER)"] | ["SUM(Sales)"] | 12 | 10.164 |
| [S36/Q34](#s36) | success | ["\"order\"", "salesperson"] | 2 / {'LEFT': 1} | ["o.Region", "o.\"Order ID\""] | ["SUM(o.Sales)"] | 4321 | 17.882 |
| [S37/Q35](#s37) | success | ["\"order\""] | 0 / {} | ["o.Region"] | ["COUNT(DISTINCT o.\"Order ID\")", "SUM(o.Sales)", "SUM(o.profit)"] | 6 | 9.078 |


## 元数据和设置

| SQL | 类别 | 状态 | 内容 |
| --- | --- | --- | --- |
| S1 | connection_setup | success | PRAGMA query_only=ON |
| S2 | metadata | success | SELECT name,sql FROM sqlite_master WHERE type='table' ORDER BY name |


## Python 与执行位置

人工源码审查：**partial_violation**。SQL prepares category-year and region aggregates and growth windows. P3 sums category totals, joins endpoint years and manager labels in pandas for chart preparation; P4 performs ANOVA/Kruskal tests with valid statistical inputs but also grouped count/mean summaries. These relational preparation steps are SQL-capable, whereas rendering and statistical tests are justified exceptions. [证据](../reviews/dacomp-023.json)。

P1：Need to generate visualizations for category sales trends, growth rates, and regional manager performance. These are plots that SQL cannot produce.

[源码](../../../runs/dsv4flash-db-first-full-01/dacomp-023/attempt-01/python/P1.py)；[输出](../../../runs/dsv4flash-db-first-full-01/dacomp-023/attempt-01/python/P1.stdout)；[错误](../../../runs/dsv4flash-db-first-full-01/dacomp-023/attempt-01/python/P1.stderr)。检出需人工核验的 SQL 可实现操作：groupby(, .merge(, sort_values(；不能仅凭理由判为合规。

P2：Need to generate visualizations for category trends, growth rates, and regional manager performance. Using db.query and db.frame to access data.

[源码](../../../runs/dsv4flash-db-first-full-01/dacomp-023/attempt-01/python/P2.py)；[输出](../../../runs/dsv4flash-db-first-full-01/dacomp-023/attempt-01/python/P2.stdout)；[错误](../../../runs/dsv4flash-db-first-full-01/dacomp-023/attempt-01/python/P2.stderr)。检出需人工核验的 SQL 可实现操作：groupby(, .merge(, .query(, sort_values(；不能仅凭理由判为合规。

P3：Need to create the work directory and then generate all visualizations for category trends, growth rates, and regional manager performance.

[源码](../../../runs/dsv4flash-db-first-full-01/dacomp-023/attempt-01/python/P3.py)；[输出](../../../runs/dsv4flash-db-first-full-01/dacomp-023/attempt-01/python/P3.stdout)；[错误](../../../runs/dsv4flash-db-first-full-01/dacomp-023/attempt-01/python/P3.stderr)。检出需人工核验的 SQL 可实现操作：groupby(, .merge(, .query(, sort_values(；不能仅凭理由判为合规。

P4：Build a category share chart and run a one-way ANOVA to test whether average order sales differ across regions/managers — a statistical procedure not supported by SQLite.

[源码](../../../runs/dsv4flash-db-first-full-01/dacomp-023/attempt-01/python/P4.py)；[输出](../../../runs/dsv4flash-db-first-full-01/dacomp-023/attempt-01/python/P4.stdout)；[错误](../../../runs/dsv4flash-db-first-full-01/dacomp-023/attempt-01/python/P4.stderr)。检出需人工核验的 SQL 可实现操作：groupby(, .query(；不能仅凭理由判为合规。

P5：Verify the saved figure files exist.

[源码](../../../runs/dsv4flash-db-first-full-01/dacomp-023/attempt-01/python/P5.py)；[输出](../../../runs/dsv4flash-db-first-full-01/dacomp-023/attempt-01/python/P5.stdout)；[错误](../../../runs/dsv4flash-db-first-full-01/dacomp-023/attempt-01/python/P5.stderr)。自动源码筛查未检出预设迁出信号；这不是全面语义合规证明。

## 优化机会

已验证候选。筛选限于精确 SQL、相同自包含 CTE、相同单表完整过滤、可分解单表聚合；未覆盖任意 Join 等价和一般谓词蕴含。全部候选都是 offline，未测在线预测。

| 候选 | 类型 | 已有结果 | 覆盖 SQL | 后续次数 | 中间行数 | 验证 | 成本 |
| --- | --- | --- | --- | --- | --- | --- | --- |
| C1 | exact-result reuse | True | ["S9", "S18", "S24"] | 2 | unknown | not_verified_cap | Not tested |
| C2 | exact-result reuse | True | ["S10", "S19", "S25"] | 2 | unknown | not_verified_cap | Not tested |
| C3 | exact-result reuse | True | ["S12", "S20", "S26"] | 2 | unknown | not_verified_cap | Not tested |
| C4 | exact-result reuse | True | ["S15", "S21", "S27"] | 2 | 6 | verified | Not benchmarked; correctness alone does not establish net speedup. |
| C5 | exact-result reuse | True | ["S16", "S22", "S28"] | 2 | unknown | not_verified_cap | Not tested |
| C6 | exact-result reuse | True | ["S17", "S23"] | 1 | unknown | not_verified_cap | Not tested |
| C7 | common subexpression | False | ["S9", "S18", "S24", "S29", "S30"] | 4 | 12 | verified | Not benchmarked; correctness alone does not establish net speedup. |
| C8 | common subexpression | False | ["S15", "S21", "S27"] | 2 | unknown | not_verified_cap | Not tested |
| C9 | aggregate MV | False | ["S4", "S17", "S23", "S34", "S35"] | 4 | 12 | verified | Not benchmarked; correctness alone does not establish net speedup. |


已验证覆盖（含触发查询、候选并集去重）：13/35 条成功数据 SQL。正确性仅针对当前数据库快照；未测性能的候选不能声称已加速。

[完整 build/rewrite 与比较证据](dacomp-023.analysis.json)。

### C7：common subexpression

Identical self-contained CTE body across queries.

原查询 [S9](#s9), [S18](#s18), [S24](#s24), [S29](#s29), [S30](#s30) → 新增共享状态 C7 → 后续 4 次可复用。该构建点为事后假设，不代表 Agent 当时预知后续。

构建定义：

```sql
SELECT Category, CAST(STRFTIME('%Y', "Order Date") AS INTEGER) AS yr, SUM(Sales) AS sales FROM "order" GROUP BY Category, yr
```

受益查询 S9 的改写示例：

```sql
WITH yearly AS (SELECT * FROM temp.reuse_candidate) SELECT Category, yr, sales, ROUND(100.0 * (sales - LAG(sales) OVER (PARTITION BY Category ORDER BY yr)) / LAG(sales) OVER (PARTITION BY Category ORDER BY yr), 2) AS yoy_growth_pct FROM yearly ORDER BY Category, yr
```

| 原 SQL | 列名一致 | 结果一致 | 比较方法 |
| --- | --- | --- | --- |
| S9 | True | True | ordered_numeric_tolerance |
| S18 | True | True | ordered_numeric_tolerance |
| S24 | True | True | ordered_numeric_tolerance |
| S29 | True | True | ordered_numeric_tolerance |
| S30 | True | True | ordered_numeric_tolerance |


验证状态：verified；成本结论：Not benchmarked; correctness alone does not establish net speedup.

### C9：aggregate MV

Union of grouping keys; decomposable aggregate states; AVG uses SUM and non-NULL COUNT.

原查询 [S4](#s4), [S17](#s17), [S23](#s23), [S34](#s34), [S35](#s35) → 新增共享状态 C9 → 后续 4 次可复用。该构建点为事后假设，不代表 Agent 当时预知后续。

构建定义：

```sql
SELECT category AS __g0, CAST(STRFTIME('%Y', "Order Date") AS INTEGER) AS __g1, MIN("Order Date") AS __a0, MAX("Order Date") AS __a1, COUNT(*) AS __a2, SUM(sales) AS __a3, SUM(quantity) AS __a4, SUM(profit) AS __a5 FROM "order"  GROUP BY category, CAST(STRFTIME('%Y', "Order Date") AS INTEGER)
```

受益查询 S4 的改写示例：

```sql
SELECT MIN(__a0) AS min_date, MAX(__a1) AS max_date, SUM(__a2) AS n FROM temp.reuse_candidate
```

| 原 SQL | 列名一致 | 结果一致 | 比较方法 |
| --- | --- | --- | --- |
| S4 | True | True | exact_multiset |
| S17 | True | True | ordered_numeric_tolerance |
| S23 | True | True | ordered_numeric_tolerance |
| S34 | True | True | ordered_numeric_tolerance |
| S35 | True | True | ordered_numeric_tolerance |


验证状态：verified；成本结论：Not benchmarked; correctness alone does not establish net speedup.

### C4：exact-result reuse

Identical normalized SQL and parameters; archive equality checked.

原查询 [S15](#s15), [S21](#s21), [S27](#s27) → 保留前序结果 S15 → 后续 2 次可复用。该构建点为事后假设，不代表 Agent 当时预知后续。

| 原 SQL | 列名一致 | 结果一致 | 比较方法 |
| --- | --- | --- | --- |
| S21 | True | True | ordered_numeric_tolerance |
| S27 | True | True | ordered_numeric_tolerance |


验证状态：verified；成本结论：Not benchmarked; correctness alone does not establish net speedup.

结果依赖：自动记录 SQL→Python 的接口父调用，以及源码中引用归档文件的消费者；字面值相同不认定因果。模型方向选择需要人工读取消息，尚未做全面因果标注。

[原始报告](../../../runs/dsv4flash-db-first-full-01/dacomp-023/attempt-01/answer.md)；[统一消息](../../../runs/dsv4flash-db-first-full-01/dacomp-023/attempt-01/messages.jsonl)；[原始 OpenCode 事件](../../../runs/dsv4flash-db-first-full-01/dacomp-023/attempt-01/opencode.jsonl)；[SQL 引擎日志](../../../runs/dsv4flash-db-first-full-01/dacomp-023/attempt-01/sql_journal.jsonl)。

[可读报告（本地图片链接规范化）](../answers/dacomp-023.md)。原始回答保留，分析结论未改写。

## S1

类别 `connection_setup`；来源 `connection`；调用 `5d9fda96177b4f9f832ef00fbb442b4e`；状态 `success`。

```sql
PRAGMA query_only=ON
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-023/attempt-01/sql/S1.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-023/attempt-01/sql/S1.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-023/attempt-01/results/S1.rows.jsonl)；完整：True；SHA256：`e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`。

## S2

类别 `metadata`；来源 `list_db`；调用 `5d9fda96177b4f9f832ef00fbb442b4e`；状态 `success`。

```sql
SELECT name,sql FROM sqlite_master WHERE type='table' ORDER BY name
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-023/attempt-01/sql/S2.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-023/attempt-01/sql/S2.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-023/attempt-01/results/S2.rows.jsonl)；完整：True；SHA256：`044e42f4550272e7e2a4bc853ec9224c0208817a56fcb23d47462a4c4b85e733`。

## S3

类别 `data`；来源 `query_db`；调用 `6cd0a9f8fbdc4d46aa3f079988532ecf`；状态 `success`。

```sql
SELECT * FROM salesperson
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-023/attempt-01/sql/S3.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-023/attempt-01/sql/S3.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-023/attempt-01/results/S3.rows.jsonl)；完整：True；SHA256：`7a8329a6cb23865f24555bece7b21931534530aa94e7745fd996763fe555ccae`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "salesperson", "kind": "base", "block": null, "base_tables": ["salesperson"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |


## S4

类别 `data`；来源 `query_db`；调用 `47fb50ebf34848048e1d6f313ddac6b1`；状态 `success`。

```sql
SELECT MIN("Order Date") AS min_date, MAX("Order Date") AS max_date, COUNT(*) AS n FROM "order"
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-023/attempt-01/sql/S4.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-023/attempt-01/sql/S4.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-023/attempt-01/results/S4.rows.jsonl)；完整：True；SHA256：`74af11074180d3f6458b7d2c47328c66255405ca5c1e1e26be4eb3d66a9244cf`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "order", "kind": "base", "block": null, "base_tables": ["\"order\""]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | MIN("Order Date") | [{"table": "\"order\"", "column": "Order Date"}] | [] | False |
| B1 | MAX("Order Date") | [{"table": "\"order\"", "column": "Order Date"}] | [] | False |
| B1 | COUNT(*) | [] | [] | True |


## S5

类别 `data`；来源 `query_db`；调用 `f3772b0e608f4665b19706b35441c75c`；状态 `success`。

```sql
SELECT DISTINCT Category FROM "order"
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-023/attempt-01/sql/S5.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-023/attempt-01/sql/S5.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-023/attempt-01/results/S5.rows.jsonl)；完整：True；SHA256：`e0a1fbd5bc973e1211c6884610b27c9b80a12eb0967adbc5f1b6f8ebe74bb0d5`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "order", "kind": "base", "block": null, "base_tables": ["\"order\""]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |


## S6

类别 `data`；来源 `query_db`；调用 `2fff779cc39d41cbac52a07e3d40466b`；状态 `success`。

```sql
SELECT DISTINCT Region FROM "order"
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-023/attempt-01/sql/S6.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-023/attempt-01/sql/S6.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-023/attempt-01/results/S6.rows.jsonl)；完整：True；SHA256：`92ef83dc959cfc188bcd88e0ac2b643812963efe360c74f991558c9882982a24`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "order", "kind": "base", "block": null, "base_tables": ["\"order\""]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |


## S7

类别 `data`；来源 `query_db`；调用 `9b047599bc3c489eb222f3e85336588e`；状态 `success`。

```sql
SELECT Category, CAST(strftime('%Y', "Order Date") AS INTEGER) AS yr, SUM(Sales) AS total_sales, SUM(Quantity) AS total_qty, SUM(profit) AS total_profit
FROM "order"
WHERE strftime('%Y', "Order Date") BETWEEN '2015' AND '2018'
GROUP BY Category, yr
ORDER BY Category, yr
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-023/attempt-01/sql/S7.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-023/attempt-01/sql/S7.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-023/attempt-01/results/S7.rows.jsonl)；完整：True；SHA256：`c0680c8598ad4a5181d0808ec4bb05f4c9001542253975294a8cce15b6e8c8b4`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "order", "kind": "base", "block": null, "base_tables": ["\"order\""]}] | [] | ["Category", "CAST(STRFTIME('%Y', \"Order Date\") AS INTEGER)"] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | SUM(Sales) | [{"table": "\"order\"", "column": "Sales"}] | [] | False |
| B1 | SUM(Quantity) | [{"table": "\"order\"", "column": "Quantity"}] | [] | False |
| B1 | SUM(profit) | [{"table": "\"order\"", "column": "profit"}] | [] | False |


## S8

类别 `data`；来源 `query_db`；调用 `038cce01f9ff49059886f321912b7eeb`；状态 `success`。

```sql
SELECT CAST(strftime('%Y', "Order Date") AS INTEGER) AS yr, COUNT(*) AS n_orders, COUNT(DISTINCT "Order ID") AS n_order_ids
FROM "order"
GROUP BY yr
ORDER BY yr
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-023/attempt-01/sql/S8.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-023/attempt-01/sql/S8.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-023/attempt-01/results/S8.rows.jsonl)；完整：True；SHA256：`d495ae177a12d770aceb8a2800b8aa293f2be08aeb76ec609cb9e15a61a264fc`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "order", "kind": "base", "block": null, "base_tables": ["\"order\""]}] | [] | ["CAST(STRFTIME('%Y', \"Order Date\") AS INTEGER)"] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |
| B1 | COUNT(DISTINCT "Order ID") | [{"table": "\"order\"", "column": "Order ID"}] | [] | False |


## S9

类别 `data`；来源 `query_db`；调用 `f2a1516eeab34873a93810ade839ae86`；状态 `success`。

```sql
WITH yearly AS (
  SELECT Category,
         CAST(strftime('%Y', "Order Date") AS INTEGER) AS yr,
         SUM(Sales) AS sales
  FROM "order"
  GROUP BY Category, yr
)
SELECT Category, yr, sales,
       ROUND(100.0 * (sales - LAG(sales) OVER (PARTITION BY Category ORDER BY yr)) / LAG(sales) OVER (PARTITION BY Category ORDER BY yr), 2) AS yoy_growth_pct
FROM yearly
ORDER BY Category, yr
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-023/attempt-01/sql/S9.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-023/attempt-01/sql/S9.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-023/attempt-01/results/S9.rows.jsonl)；完整：True；SHA256：`a468caf501da0d3b091fa0964bd102d7ecc2084431c4bc4924d7bb9caaa9e1db`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "order", "kind": "base", "block": null, "base_tables": ["\"order\""]}] | [] | ["Category", "CAST(STRFTIME('%Y', \"Order Date\") AS INTEGER)"] |
| B2 | [{"alias": "yearly", "kind": "derived", "block": "B1", "base_tables": ["\"order\""]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | SUM(Sales) | [{"table": "\"order\"", "column": "Sales"}] | [] | False |


## S10

类别 `data`；来源 `query_db`；调用 `b9e40ecc4c73449e97f42be1124382a0`；状态 `success`。

```sql
SELECT o.Region, sp."Regional Manager",
       CAST(strftime('%Y', o."Order Date") AS INTEGER) AS yr,
       SUM(o.Sales) AS sales,
       SUM(o.profit) AS profit,
       COUNT(DISTINCT o."Order ID") AS n_orders
FROM "order" o
LEFT JOIN salesperson sp ON o.Region = sp.Region
GROUP BY o.Region, sp."Regional Manager", yr
ORDER BY o.Region, yr
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-023/attempt-01/sql/S10.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-023/attempt-01/sql/S10.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-023/attempt-01/results/S10.rows.jsonl)；完整：True；SHA256：`492092952c88f85fd7c85e207190ef8e5654ab15480ec6041d64720e4d78e038`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "o", "kind": "base", "block": null, "base_tables": ["\"order\""]}, {"alias": "sp", "kind": "base", "block": null, "base_tables": ["salesperson"]}] | [{"type": "LEFT", "right": "salesperson AS sp", "on": "o.Region = sp.Region", "using": []}] | ["o.Region", "sp.\"Regional Manager\"", "CAST(STRFTIME('%Y', o.\"Order Date\") AS INTEGER)"] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | SUM(o.Sales) | [{"table": "\"order\"", "column": "Sales"}] | [] | False |
| B1 | SUM(o.profit) | [{"table": "\"order\"", "column": "profit"}] | [] | False |
| B1 | COUNT(DISTINCT o."Order ID") | [{"table": "\"order\"", "column": "Order ID"}] | [] | False |


## S11

类别 `data`；来源 `query_db`；调用 `67309b06be2b473eaf7e80455bbdb34a`；状态 `success`。

```sql
WITH yearly AS (
  SELECT o.Region, sp."Regional Manager",
         CAST(strftime('%Y', o."Order Date") AS INTEGER) AS yr,
         SUM(o.Sales) AS sales,
         SUM(o.profit) AS profit,
         COUNT(DISTINCT o."Order ID") AS n_orders
  FROM "order" o
  LEFT JOIN salesperson sp ON o.Region = sp.Region
  GROUP BY o.Region, sp."Regional Manager", yr
)
SELECT Region, "Regional Manager", yr, sales, profit, n_orders,
       ROUND(100.0 * (sales - LAG(sales) OVER (PARTITION BY Region ORDER BY yr)) / LAG(sales) OVER (PARTITION BY Region ORDER BY yr), 2) AS yoy_growth_pct
FROM yearly
ORDER BY Region, yr
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-023/attempt-01/sql/S11.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-023/attempt-01/sql/S11.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-023/attempt-01/results/S11.rows.jsonl)；完整：True；SHA256：`e999dd5e24bf408dcd147c1b847d8e5749777c201b5c5ecb307bad7c198d700a`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "o", "kind": "base", "block": null, "base_tables": ["\"order\""]}, {"alias": "sp", "kind": "base", "block": null, "base_tables": ["salesperson"]}] | [{"type": "LEFT", "right": "salesperson AS sp", "on": "o.Region = sp.Region", "using": []}] | ["o.Region", "sp.\"Regional Manager\"", "CAST(STRFTIME('%Y', o.\"Order Date\") AS INTEGER)"] |
| B2 | [{"alias": "yearly", "kind": "derived", "block": "B1", "base_tables": ["\"order\"", "salesperson"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | SUM(o.Sales) | [{"table": "\"order\"", "column": "Sales"}] | [] | False |
| B1 | SUM(o.profit) | [{"table": "\"order\"", "column": "profit"}] | [] | False |
| B1 | COUNT(DISTINCT o."Order ID") | [{"table": "\"order\"", "column": "Order ID"}] | [] | False |


## S12

类别 `data`；来源 `query_db`；调用 `6be2f8c9806b467498bcc003b2a6eafe`；状态 `success`。

```sql
SELECT o.Region, sp."Regional Manager",
       SUM(o.Sales) AS total_sales,
       SUM(o.profit) AS total_profit,
       ROUND(100.0 * SUM(o.profit) / SUM(o.Sales), 2) AS profit_margin_pct,
       COUNT(DISTINCT o."Order ID") AS n_orders,
       COUNT(*) AS n_rows
FROM "order" o
LEFT JOIN salesperson sp ON o.Region = sp.Region
GROUP BY o.Region, sp."Regional Manager"
ORDER BY total_sales DESC
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-023/attempt-01/sql/S12.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-023/attempt-01/sql/S12.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-023/attempt-01/results/S12.rows.jsonl)；完整：True；SHA256：`c68eb665886ad5b9a82bb3df7107f37083a2b5517e89645bb9e43cb41a61a401`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "o", "kind": "base", "block": null, "base_tables": ["\"order\""]}, {"alias": "sp", "kind": "base", "block": null, "base_tables": ["salesperson"]}] | [{"type": "LEFT", "right": "salesperson AS sp", "on": "o.Region = sp.Region", "using": []}] | ["o.Region", "sp.\"Regional Manager\""] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | SUM(o.Sales) | [{"table": "\"order\"", "column": "Sales"}] | [] | False |
| B1 | SUM(o.profit) | [{"table": "\"order\"", "column": "profit"}] | [] | False |
| B1 | COUNT(DISTINCT o."Order ID") | [{"table": "\"order\"", "column": "Order ID"}] | [] | False |
| B1 | COUNT(*) | [] | [] | True |
| B1 | SUM(o.Sales) | [{"table": "\"order\"", "column": "Sales"}] | [] | False |
| B1 | SUM(o.profit) | [{"table": "\"order\"", "column": "profit"}] | [] | False |


## S13

类别 `data`；来源 `query_db`；调用 `09f1e6b8c5a142fa99f4beaa4b340ffe`；状态 `success`。

```sql
WITH yearly AS (
  SELECT o.Region, sp."Regional Manager",
         CAST(strftime('%Y', o."Order Date") AS INTEGER) AS yr,
         SUM(o.Sales) AS sales
  FROM "order" o
  LEFT JOIN salesperson sp ON o.Region = sp.Region
  GROUP BY o.Region, sp."Regional Manager", yr
)
SELECT Region, "Regional Manager", yr, ROUND(sales,2) AS sales,
       ROUND(100.0 * (sales - LAG(sales) OVER (PARTITION BY Region ORDER BY yr)) / LAG(sales) OVER (PARTITION BY Region ORDER BY yr), 2) AS yoy_growth_pct,
       ROUND(100.0 * (sales - FIRST_VALUE(sales) OVER (PARTITION BY Region ORDER BY yr)) / FIRST_VALUE(sales) OVER (PARTITION BY Region ORDER BY yr), 2) AS cum_growth_vs_2015_pct
FROM yearly
WHERE Region IN ('Northeast','Southwest','Northwest')
ORDER BY Region, yr
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-023/attempt-01/sql/S13.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-023/attempt-01/sql/S13.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-023/attempt-01/results/S13.rows.jsonl)；完整：True；SHA256：`b06654b66772a45d370d7bff7757795f78be9245c2e30f3bd9b2c12c4787efce`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "o", "kind": "base", "block": null, "base_tables": ["\"order\""]}, {"alias": "sp", "kind": "base", "block": null, "base_tables": ["salesperson"]}] | [{"type": "LEFT", "right": "salesperson AS sp", "on": "o.Region = sp.Region", "using": []}] | ["o.Region", "sp.\"Regional Manager\"", "CAST(STRFTIME('%Y', o.\"Order Date\") AS INTEGER)"] |
| B2 | [{"alias": "yearly", "kind": "derived", "block": "B1", "base_tables": ["\"order\"", "salesperson"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | SUM(o.Sales) | [{"table": "\"order\"", "column": "Sales"}] | [] | False |


## S14

类别 `data`；来源 `query_db`；调用 `b00593af8eef46c490f05c29d9c88ef6`；状态 `success`。

```sql
SELECT o.Region, sp."Regional Manager",
       r."Return",
       COUNT(*) AS n_lines,
       COUNT(DISTINCT o."Order ID") AS n_orders
FROM "order" o
LEFT JOIN salesperson sp ON o.Region = sp.Region
LEFT JOIN "return" r ON o."Order ID" = r."Order ID"
GROUP BY o.Region, sp."Regional Manager", r."Return"
ORDER BY o.Region, r."Return"
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-023/attempt-01/sql/S14.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-023/attempt-01/sql/S14.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-023/attempt-01/results/S14.rows.jsonl)；完整：True；SHA256：`e0c34f2a7107a87193c071cfd295012415a074c380a925e82db8cd0a1ca549cc`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "o", "kind": "base", "block": null, "base_tables": ["\"order\""]}, {"alias": "sp", "kind": "base", "block": null, "base_tables": ["salesperson"]}, {"alias": "r", "kind": "base", "block": null, "base_tables": ["\"return\""]}] | [{"type": "LEFT", "right": "salesperson AS sp", "on": "o.Region = sp.Region", "using": []}, {"type": "LEFT", "right": "\"return\" AS r", "on": "o.\"Order ID\" = r.\"Order ID\"", "using": []}] | ["o.Region", "sp.\"Regional Manager\"", "r.\"Return\""] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |
| B1 | COUNT(DISTINCT o."Order ID") | [{"table": "\"order\"", "column": "Order ID"}] | [] | False |


## S15

类别 `data`；来源 `query_db`；调用 `8eddd15eb2cd4931b4ee9288912b6a2a`；状态 `success`。

```sql
WITH order_returns AS (
  SELECT DISTINCT o."Order ID", o.Region, sp."Regional Manager",
         CASE WHEN r."Return" = 'Yes' THEN 1 ELSE 0 END AS is_returned
  FROM "order" o
  LEFT JOIN salesperson sp ON o.Region = sp.Region
  LEFT JOIN "return" r ON o."Order ID" = r."Order ID"
)
SELECT Region, "Regional Manager",
       COUNT(DISTINCT "Order ID") AS total_orders,
       SUM(is_returned) AS returned_orders,
       ROUND(100.0 * SUM(is_returned) / COUNT(DISTINCT "Order ID"), 2) AS return_rate_pct
FROM order_returns
GROUP BY Region, "Regional Manager"
ORDER BY return_rate_pct DESC
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-023/attempt-01/sql/S15.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-023/attempt-01/sql/S15.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-023/attempt-01/results/S15.rows.jsonl)；完整：True；SHA256：`069dc52169488f894880b29b923c94b439a25b72a4b10c3d09a2369c3ae1f8ca`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "o", "kind": "base", "block": null, "base_tables": ["\"order\""]}, {"alias": "sp", "kind": "base", "block": null, "base_tables": ["salesperson"]}, {"alias": "r", "kind": "base", "block": null, "base_tables": ["\"return\""]}] | [{"type": "LEFT", "right": "salesperson AS sp", "on": "o.Region = sp.Region", "using": []}, {"type": "LEFT", "right": "\"return\" AS r", "on": "o.\"Order ID\" = r.\"Order ID\"", "using": []}] | [] |
| B2 | [{"alias": "order_returns", "kind": "derived", "block": "B1", "base_tables": ["\"order\"", "\"return\"", "salesperson"]}] | [] | ["Region", "\"Regional Manager\""] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B2 | COUNT(DISTINCT "Order ID") | [{"table": "\"order\"", "column": "Order ID"}] | [] | False |
| B2 | SUM(is_returned) | [{"table": "\"return\"", "column": "Return"}] | [] | False |
| B2 | COUNT(DISTINCT "Order ID") | [{"table": "\"order\"", "column": "Order ID"}] | [] | False |
| B2 | SUM(is_returned) | [{"table": "\"return\"", "column": "Return"}] | [] | False |


## S16

类别 `data`；来源 `query_db`；调用 `c9fcdbb9c7a048c7b04d4d942ced0557`；状态 `success`。

```sql
SELECT o.Region, sp."Regional Manager", o.Category,
       SUM(o.Sales) AS total_sales,
       ROUND(100.0 * SUM(o.Sales) / SUM(SUM(o.Sales)) OVER (PARTITION BY o.Region), 2) AS pct_of_region_sales
FROM "order" o
LEFT JOIN salesperson sp ON o.Region = sp.Region
GROUP BY o.Region, sp."Regional Manager", o.Category
ORDER BY o.Region, total_sales DESC
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-023/attempt-01/sql/S16.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-023/attempt-01/sql/S16.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-023/attempt-01/results/S16.rows.jsonl)；完整：True；SHA256：`fb0db74b3bdcc2361f97f3ae99386f5aa0c247302d972f48e71c49fb14686abe`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "o", "kind": "base", "block": null, "base_tables": ["\"order\""]}, {"alias": "sp", "kind": "base", "block": null, "base_tables": ["salesperson"]}] | [{"type": "LEFT", "right": "salesperson AS sp", "on": "o.Region = sp.Region", "using": []}] | ["o.Region", "sp.\"Regional Manager\"", "o.Category"] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | SUM(o.Sales) | [{"table": "\"order\"", "column": "Sales"}] | [] | False |
| B1 | SUM(o.Sales) | [{"table": "\"order\"", "column": "Sales"}] | [] | False |
| B1 | SUM(o.Sales) | [{"table": "\"order\"", "column": "Sales"}] | [] | False |


## S17

类别 `data`；来源 `python`；调用 `9ed384a5591b4e8c82352a6be534fc8e`；状态 `success`。

```sql
SELECT Category, CAST(strftime('%Y', "Order Date") AS INTEGER) AS yr, SUM(Sales) AS total_sales, SUM(Quantity) AS total_qty, SUM(profit) AS total_profit FROM "order" GROUP BY Category, yr ORDER BY Category, yr
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-023/attempt-01/sql/S17.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-023/attempt-01/sql/S17.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-023/attempt-01/results/S17.rows.jsonl)；完整：True；SHA256：`c0680c8598ad4a5181d0808ec4bb05f4c9001542253975294a8cce15b6e8c8b4`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "order", "kind": "base", "block": null, "base_tables": ["\"order\""]}] | [] | ["Category", "CAST(STRFTIME('%Y', \"Order Date\") AS INTEGER)"] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | SUM(Sales) | [{"table": "\"order\"", "column": "Sales"}] | [] | False |
| B1 | SUM(Quantity) | [{"table": "\"order\"", "column": "Quantity"}] | [] | False |
| B1 | SUM(profit) | [{"table": "\"order\"", "column": "profit"}] | [] | False |


## S18

类别 `data`；来源 `python`；调用 `9ed384a5591b4e8c82352a6be534fc8e`；状态 `success`。

```sql
WITH yearly AS (
  SELECT Category, CAST(strftime('%Y', "Order Date") AS INTEGER) AS yr, SUM(Sales) AS sales
  FROM "order" GROUP BY Category, yr
)
SELECT Category, yr, sales, ROUND(100.0 * (sales - LAG(sales) OVER (PARTITION BY Category ORDER BY yr)) / LAG(sales) OVER (PARTITION BY Category ORDER BY yr), 2) AS yoy_growth_pct
FROM yearly ORDER BY Category, yr
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-023/attempt-01/sql/S18.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-023/attempt-01/sql/S18.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-023/attempt-01/results/S18.rows.jsonl)；完整：True；SHA256：`a468caf501da0d3b091fa0964bd102d7ecc2084431c4bc4924d7bb9caaa9e1db`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "order", "kind": "base", "block": null, "base_tables": ["\"order\""]}] | [] | ["Category", "CAST(STRFTIME('%Y', \"Order Date\") AS INTEGER)"] |
| B2 | [{"alias": "yearly", "kind": "derived", "block": "B1", "base_tables": ["\"order\""]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | SUM(Sales) | [{"table": "\"order\"", "column": "Sales"}] | [] | False |


## S19

类别 `data`；来源 `python`；调用 `9ed384a5591b4e8c82352a6be534fc8e`；状态 `success`。

```sql
SELECT o.Region, sp."Regional Manager", CAST(strftime('%Y', o."Order Date") AS INTEGER) AS yr, SUM(o.Sales) AS sales, SUM(o.profit) AS profit, COUNT(DISTINCT o."Order ID") AS n_orders
FROM "order" o LEFT JOIN salesperson sp ON o.Region = sp.Region GROUP BY o.Region, sp."Regional Manager", yr ORDER BY o.Region, yr
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-023/attempt-01/sql/S19.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-023/attempt-01/sql/S19.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-023/attempt-01/results/S19.rows.jsonl)；完整：True；SHA256：`492092952c88f85fd7c85e207190ef8e5654ab15480ec6041d64720e4d78e038`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "o", "kind": "base", "block": null, "base_tables": ["\"order\""]}, {"alias": "sp", "kind": "base", "block": null, "base_tables": ["salesperson"]}] | [{"type": "LEFT", "right": "salesperson AS sp", "on": "o.Region = sp.Region", "using": []}] | ["o.Region", "sp.\"Regional Manager\"", "CAST(STRFTIME('%Y', o.\"Order Date\") AS INTEGER)"] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | SUM(o.Sales) | [{"table": "\"order\"", "column": "Sales"}] | [] | False |
| B1 | SUM(o.profit) | [{"table": "\"order\"", "column": "profit"}] | [] | False |
| B1 | COUNT(DISTINCT o."Order ID") | [{"table": "\"order\"", "column": "Order ID"}] | [] | False |


## S20

类别 `data`；来源 `python`；调用 `9ed384a5591b4e8c82352a6be534fc8e`；状态 `success`。

```sql
SELECT o.Region, sp."Regional Manager", SUM(o.Sales) AS total_sales, SUM(o.profit) AS total_profit, ROUND(100.0 * SUM(o.profit) / SUM(o.Sales), 2) AS profit_margin_pct, COUNT(DISTINCT o."Order ID") AS n_orders, COUNT(*) AS n_rows
FROM "order" o LEFT JOIN salesperson sp ON o.Region = sp.Region GROUP BY o.Region, sp."Regional Manager" ORDER BY total_sales DESC
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-023/attempt-01/sql/S20.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-023/attempt-01/sql/S20.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-023/attempt-01/results/S20.rows.jsonl)；完整：True；SHA256：`c68eb665886ad5b9a82bb3df7107f37083a2b5517e89645bb9e43cb41a61a401`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "o", "kind": "base", "block": null, "base_tables": ["\"order\""]}, {"alias": "sp", "kind": "base", "block": null, "base_tables": ["salesperson"]}] | [{"type": "LEFT", "right": "salesperson AS sp", "on": "o.Region = sp.Region", "using": []}] | ["o.Region", "sp.\"Regional Manager\""] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | SUM(o.Sales) | [{"table": "\"order\"", "column": "Sales"}] | [] | False |
| B1 | SUM(o.profit) | [{"table": "\"order\"", "column": "profit"}] | [] | False |
| B1 | COUNT(DISTINCT o."Order ID") | [{"table": "\"order\"", "column": "Order ID"}] | [] | False |
| B1 | COUNT(*) | [] | [] | True |
| B1 | SUM(o.Sales) | [{"table": "\"order\"", "column": "Sales"}] | [] | False |
| B1 | SUM(o.profit) | [{"table": "\"order\"", "column": "profit"}] | [] | False |


## S21

类别 `data`；来源 `python`；调用 `9ed384a5591b4e8c82352a6be534fc8e`；状态 `success`。

```sql
WITH order_returns AS (
  SELECT DISTINCT o."Order ID", o.Region, sp."Regional Manager", CASE WHEN r."Return" = 'Yes' THEN 1 ELSE 0 END AS is_returned
  FROM "order" o LEFT JOIN salesperson sp ON o.Region = sp.Region LEFT JOIN "return" r ON o."Order ID" = r."Order ID"
)
SELECT Region, "Regional Manager", COUNT(DISTINCT "Order ID") AS total_orders, SUM(is_returned) AS returned_orders, ROUND(100.0 * SUM(is_returned) / COUNT(DISTINCT "Order ID"), 2) AS return_rate_pct
FROM order_returns GROUP BY Region, "Regional Manager" ORDER BY return_rate_pct DESC
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-023/attempt-01/sql/S21.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-023/attempt-01/sql/S21.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-023/attempt-01/results/S21.rows.jsonl)；完整：True；SHA256：`069dc52169488f894880b29b923c94b439a25b72a4b10c3d09a2369c3ae1f8ca`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "o", "kind": "base", "block": null, "base_tables": ["\"order\""]}, {"alias": "sp", "kind": "base", "block": null, "base_tables": ["salesperson"]}, {"alias": "r", "kind": "base", "block": null, "base_tables": ["\"return\""]}] | [{"type": "LEFT", "right": "salesperson AS sp", "on": "o.Region = sp.Region", "using": []}, {"type": "LEFT", "right": "\"return\" AS r", "on": "o.\"Order ID\" = r.\"Order ID\"", "using": []}] | [] |
| B2 | [{"alias": "order_returns", "kind": "derived", "block": "B1", "base_tables": ["\"order\"", "\"return\"", "salesperson"]}] | [] | ["Region", "\"Regional Manager\""] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B2 | COUNT(DISTINCT "Order ID") | [{"table": "\"order\"", "column": "Order ID"}] | [] | False |
| B2 | SUM(is_returned) | [{"table": "\"return\"", "column": "Return"}] | [] | False |
| B2 | COUNT(DISTINCT "Order ID") | [{"table": "\"order\"", "column": "Order ID"}] | [] | False |
| B2 | SUM(is_returned) | [{"table": "\"return\"", "column": "Return"}] | [] | False |


## S22

类别 `data`；来源 `python`；调用 `9ed384a5591b4e8c82352a6be534fc8e`；状态 `success`。

```sql
SELECT o.Region, sp."Regional Manager", o.Category, SUM(o.Sales) AS total_sales, ROUND(100.0 * SUM(o.Sales) / SUM(SUM(o.Sales)) OVER (PARTITION BY o.Region), 2) AS pct_of_region_sales
FROM "order" o LEFT JOIN salesperson sp ON o.Region = sp.Region GROUP BY o.Region, sp."Regional Manager", o.Category ORDER BY o.Region, total_sales DESC
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-023/attempt-01/sql/S22.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-023/attempt-01/sql/S22.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-023/attempt-01/results/S22.rows.jsonl)；完整：True；SHA256：`fb0db74b3bdcc2361f97f3ae99386f5aa0c247302d972f48e71c49fb14686abe`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "o", "kind": "base", "block": null, "base_tables": ["\"order\""]}, {"alias": "sp", "kind": "base", "block": null, "base_tables": ["salesperson"]}] | [{"type": "LEFT", "right": "salesperson AS sp", "on": "o.Region = sp.Region", "using": []}] | ["o.Region", "sp.\"Regional Manager\"", "o.Category"] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | SUM(o.Sales) | [{"table": "\"order\"", "column": "Sales"}] | [] | False |
| B1 | SUM(o.Sales) | [{"table": "\"order\"", "column": "Sales"}] | [] | False |
| B1 | SUM(o.Sales) | [{"table": "\"order\"", "column": "Sales"}] | [] | False |


## S23

类别 `data`；来源 `python`；调用 `6ec9b090ea6e4682a1007916d463858c`；状态 `success`。

```sql
SELECT Category, CAST(strftime('%Y', "Order Date") AS INTEGER) AS yr, SUM(Sales) AS total_sales, SUM(Quantity) AS total_qty, SUM(profit) AS total_profit FROM "order" GROUP BY Category, yr ORDER BY Category, yr
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-023/attempt-01/sql/S23.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-023/attempt-01/sql/S23.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-023/attempt-01/results/S23.rows.jsonl)；完整：True；SHA256：`c0680c8598ad4a5181d0808ec4bb05f4c9001542253975294a8cce15b6e8c8b4`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "order", "kind": "base", "block": null, "base_tables": ["\"order\""]}] | [] | ["Category", "CAST(STRFTIME('%Y', \"Order Date\") AS INTEGER)"] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | SUM(Sales) | [{"table": "\"order\"", "column": "Sales"}] | [] | False |
| B1 | SUM(Quantity) | [{"table": "\"order\"", "column": "Quantity"}] | [] | False |
| B1 | SUM(profit) | [{"table": "\"order\"", "column": "profit"}] | [] | False |


## S24

类别 `data`；来源 `python`；调用 `6ec9b090ea6e4682a1007916d463858c`；状态 `success`。

```sql
WITH yearly AS (
  SELECT Category, CAST(strftime('%Y', "Order Date") AS INTEGER) AS yr, SUM(Sales) AS sales
  FROM "order" GROUP BY Category, yr
)
SELECT Category, yr, sales, ROUND(100.0 * (sales - LAG(sales) OVER (PARTITION BY Category ORDER BY yr)) / LAG(sales) OVER (PARTITION BY Category ORDER BY yr), 2) AS yoy_growth_pct
FROM yearly ORDER BY Category, yr
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-023/attempt-01/sql/S24.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-023/attempt-01/sql/S24.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-023/attempt-01/results/S24.rows.jsonl)；完整：True；SHA256：`a468caf501da0d3b091fa0964bd102d7ecc2084431c4bc4924d7bb9caaa9e1db`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "order", "kind": "base", "block": null, "base_tables": ["\"order\""]}] | [] | ["Category", "CAST(STRFTIME('%Y', \"Order Date\") AS INTEGER)"] |
| B2 | [{"alias": "yearly", "kind": "derived", "block": "B1", "base_tables": ["\"order\""]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | SUM(Sales) | [{"table": "\"order\"", "column": "Sales"}] | [] | False |


## S25

类别 `data`；来源 `python`；调用 `6ec9b090ea6e4682a1007916d463858c`；状态 `success`。

```sql
SELECT o.Region, sp."Regional Manager", CAST(strftime('%Y', o."Order Date") AS INTEGER) AS yr, SUM(o.Sales) AS sales, SUM(o.profit) AS profit, COUNT(DISTINCT o."Order ID") AS n_orders
FROM "order" o LEFT JOIN salesperson sp ON o.Region = sp.Region GROUP BY o.Region, sp."Regional Manager", yr ORDER BY o.Region, yr
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-023/attempt-01/sql/S25.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-023/attempt-01/sql/S25.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-023/attempt-01/results/S25.rows.jsonl)；完整：True；SHA256：`492092952c88f85fd7c85e207190ef8e5654ab15480ec6041d64720e4d78e038`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "o", "kind": "base", "block": null, "base_tables": ["\"order\""]}, {"alias": "sp", "kind": "base", "block": null, "base_tables": ["salesperson"]}] | [{"type": "LEFT", "right": "salesperson AS sp", "on": "o.Region = sp.Region", "using": []}] | ["o.Region", "sp.\"Regional Manager\"", "CAST(STRFTIME('%Y', o.\"Order Date\") AS INTEGER)"] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | SUM(o.Sales) | [{"table": "\"order\"", "column": "Sales"}] | [] | False |
| B1 | SUM(o.profit) | [{"table": "\"order\"", "column": "profit"}] | [] | False |
| B1 | COUNT(DISTINCT o."Order ID") | [{"table": "\"order\"", "column": "Order ID"}] | [] | False |


## S26

类别 `data`；来源 `python`；调用 `6ec9b090ea6e4682a1007916d463858c`；状态 `success`。

```sql
SELECT o.Region, sp."Regional Manager", SUM(o.Sales) AS total_sales, SUM(o.profit) AS total_profit, ROUND(100.0 * SUM(o.profit) / SUM(o.Sales), 2) AS profit_margin_pct, COUNT(DISTINCT o."Order ID") AS n_orders, COUNT(*) AS n_rows
FROM "order" o LEFT JOIN salesperson sp ON o.Region = sp.Region GROUP BY o.Region, sp."Regional Manager" ORDER BY total_sales DESC
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-023/attempt-01/sql/S26.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-023/attempt-01/sql/S26.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-023/attempt-01/results/S26.rows.jsonl)；完整：True；SHA256：`c68eb665886ad5b9a82bb3df7107f37083a2b5517e89645bb9e43cb41a61a401`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "o", "kind": "base", "block": null, "base_tables": ["\"order\""]}, {"alias": "sp", "kind": "base", "block": null, "base_tables": ["salesperson"]}] | [{"type": "LEFT", "right": "salesperson AS sp", "on": "o.Region = sp.Region", "using": []}] | ["o.Region", "sp.\"Regional Manager\""] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | SUM(o.Sales) | [{"table": "\"order\"", "column": "Sales"}] | [] | False |
| B1 | SUM(o.profit) | [{"table": "\"order\"", "column": "profit"}] | [] | False |
| B1 | COUNT(DISTINCT o."Order ID") | [{"table": "\"order\"", "column": "Order ID"}] | [] | False |
| B1 | COUNT(*) | [] | [] | True |
| B1 | SUM(o.Sales) | [{"table": "\"order\"", "column": "Sales"}] | [] | False |
| B1 | SUM(o.profit) | [{"table": "\"order\"", "column": "profit"}] | [] | False |


## S27

类别 `data`；来源 `python`；调用 `6ec9b090ea6e4682a1007916d463858c`；状态 `success`。

```sql
WITH order_returns AS (
  SELECT DISTINCT o."Order ID", o.Region, sp."Regional Manager", CASE WHEN r."Return" = 'Yes' THEN 1 ELSE 0 END AS is_returned
  FROM "order" o LEFT JOIN salesperson sp ON o.Region = sp.Region LEFT JOIN "return" r ON o."Order ID" = r."Order ID"
)
SELECT Region, "Regional Manager", COUNT(DISTINCT "Order ID") AS total_orders, SUM(is_returned) AS returned_orders, ROUND(100.0 * SUM(is_returned) / COUNT(DISTINCT "Order ID"), 2) AS return_rate_pct
FROM order_returns GROUP BY Region, "Regional Manager" ORDER BY return_rate_pct DESC
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-023/attempt-01/sql/S27.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-023/attempt-01/sql/S27.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-023/attempt-01/results/S27.rows.jsonl)；完整：True；SHA256：`069dc52169488f894880b29b923c94b439a25b72a4b10c3d09a2369c3ae1f8ca`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "o", "kind": "base", "block": null, "base_tables": ["\"order\""]}, {"alias": "sp", "kind": "base", "block": null, "base_tables": ["salesperson"]}, {"alias": "r", "kind": "base", "block": null, "base_tables": ["\"return\""]}] | [{"type": "LEFT", "right": "salesperson AS sp", "on": "o.Region = sp.Region", "using": []}, {"type": "LEFT", "right": "\"return\" AS r", "on": "o.\"Order ID\" = r.\"Order ID\"", "using": []}] | [] |
| B2 | [{"alias": "order_returns", "kind": "derived", "block": "B1", "base_tables": ["\"order\"", "\"return\"", "salesperson"]}] | [] | ["Region", "\"Regional Manager\""] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B2 | COUNT(DISTINCT "Order ID") | [{"table": "\"order\"", "column": "Order ID"}] | [] | False |
| B2 | SUM(is_returned) | [{"table": "\"return\"", "column": "Return"}] | [] | False |
| B2 | COUNT(DISTINCT "Order ID") | [{"table": "\"order\"", "column": "Order ID"}] | [] | False |
| B2 | SUM(is_returned) | [{"table": "\"return\"", "column": "Return"}] | [] | False |


## S28

类别 `data`；来源 `python`；调用 `6ec9b090ea6e4682a1007916d463858c`；状态 `success`。

```sql
SELECT o.Region, sp."Regional Manager", o.Category, SUM(o.Sales) AS total_sales, ROUND(100.0 * SUM(o.Sales) / SUM(SUM(o.Sales)) OVER (PARTITION BY o.Region), 2) AS pct_of_region_sales
FROM "order" o LEFT JOIN salesperson sp ON o.Region = sp.Region GROUP BY o.Region, sp."Regional Manager", o.Category ORDER BY o.Region, total_sales DESC
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-023/attempt-01/sql/S28.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-023/attempt-01/sql/S28.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-023/attempt-01/results/S28.rows.jsonl)；完整：True；SHA256：`fb0db74b3bdcc2361f97f3ae99386f5aa0c247302d972f48e71c49fb14686abe`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "o", "kind": "base", "block": null, "base_tables": ["\"order\""]}, {"alias": "sp", "kind": "base", "block": null, "base_tables": ["salesperson"]}] | [{"type": "LEFT", "right": "salesperson AS sp", "on": "o.Region = sp.Region", "using": []}] | ["o.Region", "sp.\"Regional Manager\"", "o.Category"] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | SUM(o.Sales) | [{"table": "\"order\"", "column": "Sales"}] | [] | False |
| B1 | SUM(o.Sales) | [{"table": "\"order\"", "column": "Sales"}] | [] | False |
| B1 | SUM(o.Sales) | [{"table": "\"order\"", "column": "Sales"}] | [] | False |


## S29

类别 `data`；来源 `query_db`；调用 `9e1d312a29e243e2b47db3f6fc4098f3`；状态 `success`。

```sql
WITH yearly AS (
  SELECT Category, CAST(strftime('%Y', "Order Date") AS INTEGER) AS yr, SUM(Sales) AS sales
  FROM "order" GROUP BY Category, yr
),
growth AS (
  SELECT Category, yr, sales,
         ROUND(100.0 * (sales - LAG(sales) OVER (PARTITION BY Category ORDER BY yr)) / LAG(sales) OVER (PARTITION BY Category ORDER BY yr), 2) AS yoy_growth_pct
  FROM yearly
),
ranked AS (
  SELECT Category, yr, yoy_growth_pct,
         RANK() OVER (PARTITION BY yr ORDER BY yoy_growth_pct DESC) AS rnk
  FROM growth WHERE yr > 2015
)
SELECT yr, Category, yoy_growth_pct, rnk FROM ranked ORDER BY yr, rnk
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-023/attempt-01/sql/S29.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-023/attempt-01/sql/S29.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-023/attempt-01/results/S29.rows.jsonl)；完整：True；SHA256：`4bf2dcb801cd103bef2324844c8d0f025dec2266f1b705c4d1e6fe04e136c384`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "order", "kind": "base", "block": null, "base_tables": ["\"order\""]}] | [] | ["Category", "CAST(STRFTIME('%Y', \"Order Date\") AS INTEGER)"] |
| B2 | [{"alias": "yearly", "kind": "derived", "block": "B1", "base_tables": ["\"order\""]}] | [] | [] |
| B3 | [{"alias": "growth", "kind": "derived", "block": "B2", "base_tables": ["\"order\""]}] | [] | [] |
| B4 | [{"alias": "ranked", "kind": "derived", "block": "B3", "base_tables": ["\"order\""]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | SUM(Sales) | [{"table": "\"order\"", "column": "Sales"}] | [] | False |


## S30

类别 `data`；来源 `query_db`；调用 `0cbb3314655d4b06a4657436e4e7f143`；状态 `success`。

```sql
WITH yearly AS (
  SELECT Category, CAST(strftime('%Y', "Order Date") AS INTEGER) AS yr, SUM(Sales) AS sales
  FROM "order" GROUP BY Category, yr
),
base AS (SELECT Category, sales AS s2015 FROM yearly WHERE yr=2015),
final AS (SELECT Category, sales AS s2018 FROM yearly WHERE yr=2018)
SELECT b.Category,
       ROUND(b.s2015, 2) AS sales_2015,
       ROUND(f.s2018, 2) AS sales_2018,
       ROUND(100.0 * (f.s2018 - b.s2015) / b.s2015, 2) AS total_growth_pct,
       ROUND(100.0 * (POWER(f.s2018 / b.s2015, 1.0/3.0) - 1), 2) AS cagr_pct
FROM base b JOIN final f USING (Category)
ORDER BY cagr_pct DESC
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-023/attempt-01/sql/S30.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-023/attempt-01/sql/S30.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-023/attempt-01/results/S30.rows.jsonl)；完整：True；SHA256：`0ddd3dd066e0af41773bc24ff09504bc6f84eddd3f0e8d948455a89e06947ea9`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "order", "kind": "base", "block": null, "base_tables": ["\"order\""]}] | [] | ["Category", "CAST(STRFTIME('%Y', \"Order Date\") AS INTEGER)"] |
| B2 | [{"alias": "yearly", "kind": "derived", "block": "B1", "base_tables": ["\"order\""]}] | [] | [] |
| B3 | [{"alias": "yearly", "kind": "derived", "block": "B1", "base_tables": ["\"order\""]}] | [] | [] |
| B4 | [{"alias": "b", "kind": "derived", "block": "B2", "base_tables": ["\"order\""]}, {"alias": "f", "kind": "derived", "block": "B3", "base_tables": ["\"order\""]}] | [{"type": "INNER", "right": "final AS f", "on": null, "using": ["Category"]}] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | SUM(Sales) | [{"table": "\"order\"", "column": "Sales"}] | [] | False |


## S31

类别 `data`；来源 `query_db`；调用 `4922929724f24d04bd844a181b004661`；状态 `success`。

```sql
SELECT o.Region, sp."Regional Manager",
       ROUND(SUM(o.Sales) / COUNT(DISTINCT o."Order ID"), 2) AS avg_sales_per_order,
       ROUND(SUM(o.profit) / COUNT(DISTINCT o."Order ID"), 2) AS avg_profit_per_order,
       ROUND(SUM(o.profit) / SUM(o.Sales) * 100, 2) AS profit_margin_pct,
       COUNT(DISTINCT o."Order ID") AS n_orders,
       ROUND(SUM(o.Sales) / COUNT(*), 2) AS avg_sales_per_line
FROM "order" o
LEFT JOIN salesperson sp ON o.Region = sp.Region
GROUP BY o.Region, sp."Regional Manager"
ORDER BY avg_sales_per_order DESC
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-023/attempt-01/sql/S31.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-023/attempt-01/sql/S31.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-023/attempt-01/results/S31.rows.jsonl)；完整：True；SHA256：`802c7b958a9680690aa4c1f3e946ee8c97fdc85f8cba3ca17be7cd1f7866ecf6`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "o", "kind": "base", "block": null, "base_tables": ["\"order\""]}, {"alias": "sp", "kind": "base", "block": null, "base_tables": ["salesperson"]}] | [{"type": "LEFT", "right": "salesperson AS sp", "on": "o.Region = sp.Region", "using": []}] | ["o.Region", "sp.\"Regional Manager\""] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(DISTINCT o."Order ID") | [{"table": "\"order\"", "column": "Order ID"}] | [] | False |
| B1 | SUM(o.Sales) | [{"table": "\"order\"", "column": "Sales"}] | [] | False |
| B1 | COUNT(DISTINCT o."Order ID") | [{"table": "\"order\"", "column": "Order ID"}] | [] | False |
| B1 | SUM(o.profit) | [{"table": "\"order\"", "column": "profit"}] | [] | False |
| B1 | COUNT(DISTINCT o."Order ID") | [{"table": "\"order\"", "column": "Order ID"}] | [] | False |
| B1 | SUM(o.Sales) | [{"table": "\"order\"", "column": "Sales"}] | [] | False |
| B1 | COUNT(*) | [] | [] | True |
| B1 | SUM(o.profit) | [{"table": "\"order\"", "column": "profit"}] | [] | False |
| B1 | SUM(o.Sales) | [{"table": "\"order\"", "column": "Sales"}] | [] | False |


## S32

类别 `data`；来源 `query_db`；调用 `9f963763730a44e090f125d2c6f45766`；状态 `success`。

```sql
WITH yearly AS (
  SELECT o.Region, CAST(strftime('%Y', o."Order Date") AS INTEGER) AS yr,
         SUM(o.Sales) AS sales, COUNT(DISTINCT o."Order ID") AS n_orders
  FROM "order" o GROUP BY o.Region, yr
),
growth AS (
  SELECT Region, yr, sales, n_orders,
         ROUND(100.0 * (sales - LAG(sales) OVER (PARTITION BY Region ORDER BY yr)) / LAG(sales) OVER (PARTITION BY Region ORDER BY yr), 2) AS yoy_sales_growth,
         ROUND(100.0 * (n_orders - LAG(n_orders) OVER (PARTITION BY Region ORDER BY yr)) / LAG(n_orders) OVER (PARTITION BY Region ORDER BY yr), 2) AS yoy_order_growth
  FROM yearly
)
SELECT g.*, sp."Regional Manager"
FROM growth g
LEFT JOIN salesperson sp ON g.Region = sp.Region
WHERE yr > 2015
ORDER BY g.Region, g.yr
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-023/attempt-01/sql/S32.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-023/attempt-01/sql/S32.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-023/attempt-01/results/S32.rows.jsonl)；完整：True；SHA256：`2e4dcbaa1411c0a6feb7168b18d755dce2a7ffab6add479de5dd8c62bbcc53b0`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "o", "kind": "base", "block": null, "base_tables": ["\"order\""]}] | [] | ["o.Region", "CAST(STRFTIME('%Y', o.\"Order Date\") AS INTEGER)"] |
| B2 | [{"alias": "yearly", "kind": "derived", "block": "B1", "base_tables": ["\"order\""]}] | [] | [] |
| B3 | [{"alias": "g", "kind": "derived", "block": "B2", "base_tables": ["\"order\""]}, {"alias": "sp", "kind": "base", "block": null, "base_tables": ["salesperson"]}] | [{"type": "LEFT", "right": "salesperson AS sp", "on": "g.Region = sp.Region", "using": []}] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | SUM(o.Sales) | [{"table": "\"order\"", "column": "Sales"}] | [] | False |
| B1 | COUNT(DISTINCT o."Order ID") | [{"table": "\"order\"", "column": "Order ID"}] | [] | False |


## S33

类别 `data`；来源 `query_db`；调用 `df1b09b031384ab785d0c37908bf2fa6`；状态 `success`。

```sql
SELECT o.Region, sp."Regional Manager",
       ROUND(AVG(o.Discount) * 100, 2) AS avg_discount_pct,
       ROUND(SUM(o.Quantity), 0) AS total_qty,
       ROUND(SUM(o.Sales) / SUM(o.Quantity), 2) AS avg_price_per_unit
FROM "order" o
LEFT JOIN salesperson sp ON o.Region = sp.Region
GROUP BY o.Region, sp."Regional Manager"
ORDER BY avg_discount_pct DESC
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-023/attempt-01/sql/S33.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-023/attempt-01/sql/S33.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-023/attempt-01/results/S33.rows.jsonl)；完整：True；SHA256：`d97a3c872620f3fb0b115abf7461edc5bd8bf11e91525eec2dd77f2d57214119`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "o", "kind": "base", "block": null, "base_tables": ["\"order\""]}, {"alias": "sp", "kind": "base", "block": null, "base_tables": ["salesperson"]}] | [{"type": "LEFT", "right": "salesperson AS sp", "on": "o.Region = sp.Region", "using": []}] | ["o.Region", "sp.\"Regional Manager\""] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | SUM(o.Quantity) | [{"table": "\"order\"", "column": "Quantity"}] | [] | False |
| B1 | AVG(o.Discount) | [{"table": "\"order\"", "column": "Discount"}] | [] | False |
| B1 | SUM(o.Sales) | [{"table": "\"order\"", "column": "Sales"}] | [] | False |
| B1 | SUM(o.Quantity) | [{"table": "\"order\"", "column": "Quantity"}] | [] | False |


## S34

类别 `data`；来源 `query_db`；调用 `db62f6ca933d43d6a4149660f9aa45be`；状态 `success`。

```sql
SELECT CAST(strftime('%Y', "Order Date") AS INTEGER) AS yr,
       SUM(Sales) AS total_sales,
       SUM(profit) AS total_profit,
       ROUND(100.0 * SUM(profit) / SUM(Sales), 2) AS margin_pct
FROM "order"
GROUP BY yr ORDER BY yr
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-023/attempt-01/sql/S34.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-023/attempt-01/sql/S34.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-023/attempt-01/results/S34.rows.jsonl)；完整：True；SHA256：`999e0506ae18787c643c50e5c86f5238f903f88fefe3661999f95d140a1829df`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "order", "kind": "base", "block": null, "base_tables": ["\"order\""]}] | [] | ["CAST(STRFTIME('%Y', \"Order Date\") AS INTEGER)"] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | SUM(Sales) | [{"table": "\"order\"", "column": "Sales"}] | [] | False |
| B1 | SUM(profit) | [{"table": "\"order\"", "column": "profit"}] | [] | False |
| B1 | SUM(Sales) | [{"table": "\"order\"", "column": "Sales"}] | [] | False |
| B1 | SUM(profit) | [{"table": "\"order\"", "column": "profit"}] | [] | False |


## S35

类别 `data`；来源 `python`；调用 `f239367871ed41d48a56921d1bcfac9e`；状态 `success`。

```sql
SELECT Category, CAST(strftime('%Y', "Order Date") AS INTEGER) AS yr, SUM(Sales) AS sales
FROM "order" GROUP BY Category, yr ORDER BY Category, yr
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-023/attempt-01/sql/S35.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-023/attempt-01/sql/S35.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-023/attempt-01/results/S35.rows.jsonl)；完整：True；SHA256：`afcbe126bfe4898e5e6ca2b3876bb59d3770da787de7dd313b853022c23c8a1c`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "order", "kind": "base", "block": null, "base_tables": ["\"order\""]}] | [] | ["Category", "CAST(STRFTIME('%Y', \"Order Date\") AS INTEGER)"] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | SUM(Sales) | [{"table": "\"order\"", "column": "Sales"}] | [] | False |


## S36

类别 `data`；来源 `python`；调用 `f239367871ed41d48a56921d1bcfac9e`；状态 `success`。

```sql
SELECT o.Region, sp."Regional Manager", o."Order ID", SUM(o.Sales) AS order_sales
FROM "order" o LEFT JOIN salesperson sp ON o.Region = sp.Region
GROUP BY o.Region, o."Order ID" ORDER BY o.Region, o."Order ID"
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-023/attempt-01/sql/S36.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-023/attempt-01/sql/S36.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-023/attempt-01/results/S36.rows.jsonl)；完整：True；SHA256：`1c2c3d9c415015ffc918310add75ef1aab6e48f306ec16716babbc323c182455`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "o", "kind": "base", "block": null, "base_tables": ["\"order\""]}, {"alias": "sp", "kind": "base", "block": null, "base_tables": ["salesperson"]}] | [{"type": "LEFT", "right": "salesperson AS sp", "on": "o.Region = sp.Region", "using": []}] | ["o.Region", "o.\"Order ID\""] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | SUM(o.Sales) | [{"table": "\"order\"", "column": "Sales"}] | [] | False |


## S37

类别 `data`；来源 `python`；调用 `f239367871ed41d48a56921d1bcfac9e`；状态 `success`。

```sql
SELECT o.Region,
       ROUND(100.0 * SUM(o.profit) / SUM(o.Sales), 2) AS margin,
       COUNT(DISTINCT o."Order ID") AS total_orders
FROM "order" o GROUP BY o.Region
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-023/attempt-01/sql/S37.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-023/attempt-01/sql/S37.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-023/attempt-01/results/S37.rows.jsonl)；完整：True；SHA256：`f8bfed122007b3a827ded758a561cb28d6759cd62ae507c6bde9b097470f3975`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "o", "kind": "base", "block": null, "base_tables": ["\"order\""]}] | [] | ["o.Region"] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(DISTINCT o."Order ID") | [{"table": "\"order\"", "column": "Order ID"}] | [] | False |
| B1 | SUM(o.Sales) | [{"table": "\"order\"", "column": "Sales"}] | [] | False |
| B1 | SUM(o.profit) | [{"table": "\"order\"", "column": "profit"}] | [] | False |

