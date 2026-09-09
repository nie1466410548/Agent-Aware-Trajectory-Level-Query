# dacomp-005

Orders whose `Profit Margin` in `sheet1` is lower than 50% of the dataset average are defi…

运行：已提交。官方未评分。全部 SQL 尝试/成功 38/38；数据 SQL 36/36；Python 5 次。

完整原题：

Orders whose `Profit Margin` in `sheet1` is lower than 50% of the dataset average are defined as low-margin orders. Analyze the salient characteristics that distinguish these orders from the broader population (e.g., by `Sales Quantity`, `Total Logistics Revenue`, discount behavior, cost components such as `Freight Cost`, `Warehousing Cost`, `Other Operating Costs`, geographic distribution in `Destination`, time trends in `Date`, customer segments based on `Customer Age`, `Age Range`, `Customer Gender`, and product composition by `Consigned Product`), and then propose concrete, data-backed remedies that cover both cost-control (beating down expense) and revenue/profit uplift (improving efficiency and effectiveness). Keep every description precise, reference the English column names from the authoritative schema, and ensure thresholds or quantifiable insights stay aligned with the provided dataset.

| 表 | 行数 | 列数 |
| --- | --- | --- |
| sheet1 | 18250 | 21 |


实际路线（分析者依据 SQL/源码概括，不代表 Agent 自述）：S3：sheet1 查询 → S10：sheet1 分组聚合 → S17：sheet1 分组聚合 → S24：sheet1 分组聚合 → S31：sheet1 分组聚合 → S38：sheet1 查询（等距列出六个结构节点，全部步骤见下表）

数据库大小：7,507,968 字节。

## 数据 SQL

| SQL | 状态 | 基础表 | Join 输入/类型 | GROUP BY | 聚合表达式 | 结果行数 | 数据库 ms |
| --- | --- | --- | --- | --- | --- | --- | --- |
| [S3/Q1](#s3) | success | ["sheet1"] | 0 / {} | [] | ["COUNT(*)"] | 1 | 2.721 |
| [S4/Q2](#s4) | success | ["sheet1"] | 0 / {} | [] | ["AVG(\"Profit Margin\")", "MIN(\"Profit Margin\")", "MAX(\"Profit Margin\")"] | 1 | 4.682 |
| [S5/Q3](#s5) | success | ["sheet1"] | 0 / {} | [] | [] | 5 | 0.386 |
| [S6/Q4](#s6) | success | ["sheet1"] | 0 / {} | [] | ["AVG(\"Profit Margin\")"] | 1 | 3.526 |
| [S7/Q5](#s7) | success | ["sheet1"] | 0 / {} | [] | ["AVG(\"Profit Margin\")", "AVG(\"Profit Margin\")", "COUNT(*)", "COUNT(CASE WHEN \"Profit Margin\" < 0.5 * (SELECT AVG(\"Profit Margin\") FROM sheet1) THEN 1 END)", "COUNT(*)", "COUNT(CASE WHEN \"Profit Margin\" < 0.5 * (SELECT AVG(\"Profit Margin\") FROM sheet1) THEN 1 END)"] | 1 | 11.065 |
| [S8/Q6](#s8) | success | ["sheet1"] | 0 / {} | ["is_low"] | ["AVG(\"Profit Margin\")", "COUNT(*)", "AVG(\"Sales Quantity\")", "AVG(\"Logistics Unit Price\")", "AVG(\"List Price Revenue\")", "AVG(\"Logistics Value-Added Service Revenue\")", "AVG(\"Discount Amount\")", "AVG(\"Total Logistics Revenue\")", "AVG(\"Freight Cost\")", "AVG(\"Warehousing Cost\")", "AVG(\"Other Operating Costs\")", "AVG(\"Total Logistics Cost\")", "AVG(\"Profit\")", "AVG(\"Profit Margin\")", "AVG(\"Discount Amount\")", "AVG(\"List Price Revenue\")"] | 2 | 32.352 |
| [S9/Q7](#s9) | success | ["sheet1"] | 0 / {} | ["is_low"] | ["AVG(\"Profit Margin\")", "AVG(\"Total Logistics Revenue\")", "AVG(\"Total Logistics Cost\")", "AVG(\"Freight Cost\")", "AVG(\"Warehousing Cost\")", "AVG(\"Other Operating Costs\")", "AVG(\"Total Logistics Cost\")", "AVG(\"Sales Quantity\")", "AVG(\"Sales Quantity\")", "AVG(\"Total Logistics Revenue\")", "AVG(\"Total Logistics Revenue\")", "AVG(\"Total Logistics Revenue\")", "AVG(\"Total Logistics Revenue\")"] | 2 | 20.018 |
| [S10/Q8](#s10) | success | ["sheet1"] | 0 / {} | ["\"Destination\""] | ["AVG(\"Profit Margin\")", "SUM(CASE WHEN is_low = 1 THEN 1 ELSE 0 END)", "SUM(CASE WHEN is_low = 0 THEN 1 ELSE 0 END)", "AVG(CASE WHEN is_low = 1 THEN \"Freight Cost\" END)", "AVG(CASE WHEN is_low = 0 THEN \"Freight Cost\" END)", "SUM(CASE WHEN is_low = 1 THEN 1 ELSE 0 END)", "SUM(CASE WHEN is_low = 1 THEN 1 ELSE 0 END)", "SUM(CASE WHEN is_low = 0 THEN 1 ELSE 0 END)"] | 20 | 44.194 |
| [S11/Q9](#s11) | success | ["sheet1"] | 0 / {} | ["\"Consigned Product\""] | ["AVG(\"Profit Margin\")", "SUM(CASE WHEN is_low = 1 THEN 1 ELSE 0 END)", "SUM(CASE WHEN is_low = 0 THEN 1 ELSE 0 END)", "AVG(CASE WHEN is_low = 1 THEN \"Sales Quantity\" END)", "AVG(CASE WHEN is_low = 0 THEN \"Sales Quantity\" END)", "SUM(CASE WHEN is_low = 1 THEN 1 ELSE 0 END)", "SUM(CASE WHEN is_low = 1 THEN 1 ELSE 0 END)", "SUM(CASE WHEN is_low = 0 THEN 1 ELSE 0 END)"] | 8 | 41.889 |
| [S12/Q10](#s12) | success | ["sheet1"] | 0 / {} | ["\"Customer Gender\""] | ["AVG(\"Profit Margin\")", "SUM(CASE WHEN is_low = 1 THEN 1 ELSE 0 END)", "SUM(CASE WHEN is_low = 0 THEN 1 ELSE 0 END)", "SUM(CASE WHEN is_low = 1 THEN 1 ELSE 0 END)", "SUM(CASE WHEN is_low = 1 THEN 1 ELSE 0 END)", "SUM(CASE WHEN is_low = 0 THEN 1 ELSE 0 END)"] | 2 | 27.969 |
| [S13/Q11](#s13) | success | ["sheet1"] | 0 / {} | ["\"Age Range\""] | ["AVG(\"Profit Margin\")", "SUM(CASE WHEN is_low = 1 THEN 1 ELSE 0 END)", "SUM(CASE WHEN is_low = 0 THEN 1 ELSE 0 END)", "AVG(CASE WHEN is_low = 1 THEN \"Customer Age\" END)", "AVG(CASE WHEN is_low = 0 THEN \"Customer Age\" END)", "SUM(CASE WHEN is_low = 1 THEN 1 ELSE 0 END)", "SUM(CASE WHEN is_low = 1 THEN 1 ELSE 0 END)", "SUM(CASE WHEN is_low = 0 THEN 1 ELSE 0 END)"] | 5 | 37.046 |
| [S14/Q12](#s14) | success | ["sheet1"] | 0 / {} | ["STRFTIME('%Y-%m', \"Date\")"] | ["AVG(\"Profit Margin\")", "SUM(CASE WHEN is_low = 1 THEN 1 ELSE 0 END)", "SUM(CASE WHEN is_low = 0 THEN 1 ELSE 0 END)", "SUM(CASE WHEN is_low = 1 THEN 1 ELSE 0 END)", "SUM(CASE WHEN is_low = 1 THEN 1 ELSE 0 END)", "SUM(CASE WHEN is_low = 0 THEN 1 ELSE 0 END)"] | 12 | 32.955 |
| [S15/Q13](#s15) | success | ["sheet1"] | 0 / {} | ["is_low"] | ["AVG(\"Profit Margin\")", "COUNT(CASE WHEN \"Discount Amount\" > 0 THEN 1 END)", "AVG(\"Discount Amount\")", "AVG(\"Discount Amount\" / NULLIF(\"List Price Revenue\", 0) * 100)", "COUNT(*)", "COUNT(CASE WHEN \"Discount Amount\" > 0 THEN 1 END)"] | 2 | 17.197 |
| [S16/Q14](#s16) | success | ["sheet1"] | 0 / {} | ["\"Sales Quantity\"", "is_low"] | ["AVG(\"Profit Margin\")", "COUNT(*)", "AVG(\"Total Logistics Revenue\")", "AVG(\"Total Logistics Cost\")", "AVG(\"Profit\")", "AVG(\"Profit Margin\")"] | 30 | 20.786 |
| [S17/Q15](#s17) | success | ["sheet1"] | 0 / {} | ["CASE WHEN \"Sales Quantity\" <= 5 THEN 'Qty<=5' WHEN \"Sales Quantity\" <= 10 THEN '6-10' WHEN \"Sales Quantity\" <= 20 THEN '11-20' WHEN \"Sales Quantity\" <= 40 THEN '21-40' ELSE '41+' END", "is_low"] | ["AVG(\"Profit Margin\")", "COUNT(*)", "AVG(\"Discount Amount\" / NULLIF(\"List Price Revenue\", 0) * 100)", "AVG(\"Total Logistics Revenue\")", "AVG(\"Total Logistics Cost\")", "AVG(\"Freight Cost\")", "AVG(\"Warehousing Cost\")", "AVG(\"Other Operating Costs\")", "AVG(\"Profit\")"] | 9 | 31.764 |
| [S18/Q16](#s18) | success | ["sheet1"] | 0 / {} | ["is_low"] | ["AVG(\"Profit Margin\")", "MIN(\"Sales Quantity\")", "MAX(\"Sales Quantity\")", "COUNT(CASE WHEN \"Sales Quantity\" <= 6 THEN 1 END)", "AVG(\"Sales Quantity\")", "COUNT(*)", "COUNT(CASE WHEN \"Sales Quantity\" <= 6 THEN 1 END)"] | 2 | 15.174 |
| [S19/Q17](#s19) | success | ["sheet1"] | 0 / {} | ["\"Destination\""] | ["AVG(\"Profit Margin\")", "COUNT(*)", "SUM(CASE WHEN is_low = 1 THEN 1 ELSE 0 END)", "AVG(\"Sales Quantity\")", "AVG(\"Discount Amount\" / NULLIF(\"List Price Revenue\", 0) * 100)", "COUNT(*)", "SUM(CASE WHEN is_low = 1 THEN 1 ELSE 0 END)"] | 20 | 27.529 |
| [S20/Q18](#s20) | success | ["sheet1"] | 0 / {} | ["SUBSTRING(\"Destination\", 1, INSTR(\"Destination\", '-') - 1)"] | ["AVG(\"Profit Margin\")", "SUM(CASE WHEN is_low = 1 THEN 1 ELSE 0 END)", "SUM(CASE WHEN is_low = 0 THEN 1 ELSE 0 END)", "AVG(CASE WHEN is_low = 1 THEN \"Freight Cost\" END)", "AVG(CASE WHEN is_low = 0 THEN \"Freight Cost\" END)", "COUNT(*)", "SUM(CASE WHEN is_low = 1 THEN 1 ELSE 0 END)"] | 6 | 37.492 |
| [S21/Q19](#s21) | success | ["sheet1"] | 0 / {} | ["is_low"] | ["AVG(\"Profit Margin\")", "AVG(\"Freight Cost\" / NULLIF(\"Sales Quantity\", 0))", "AVG(\"Warehousing Cost\" / NULLIF(\"Sales Quantity\", 0))", "AVG(\"Other Operating Costs\" / NULLIF(\"Sales Quantity\", 0))", "AVG(\"Total Logistics Cost\" / NULLIF(\"Sales Quantity\", 0))", "AVG(\"Total Logistics Revenue\" / NULLIF(\"Sales Quantity\", 0))", "AVG(\"Logistics Unit Price\")"] | 2 | 23.378 |
| [S22/Q20](#s22) | success | ["sheet1"] | 0 / {} | [] | ["AVG(\"Profit Margin\")", "AVG(\"Freight Cost\")", "AVG(\"Warehousing Cost\")", "AVG(\"Other Operating Costs\")", "AVG(\"Logistics Unit Price\")", "AVG(\"Logistics Value-Added Service Revenue\")"] | 1 | 7.023 |
| [S23/Q21](#s23) | success | ["sheet1"] | 0 / {} | ["\"Logistics Unit Price\"", "is_low"] | ["AVG(\"Profit Margin\")", "COUNT(*)", "AVG(\"Total Logistics Revenue\")", "AVG(\"Freight Cost\")", "AVG(\"Discount Amount\" / NULLIF(\"List Price Revenue\", 0) * 100)"] | 40 | 29.489 |
| [S24/Q22](#s24) | success | ["sheet1"] | 0 / {} | ["ROUND(\"Freight Cost\", -1)", "is_low"] | ["AVG(\"Profit Margin\")", "COUNT(*)", "AVG(\"Sales Quantity\")", "AVG(\"Total Logistics Revenue\")", "AVG(\"Profit\")"] | 30 | 25.298 |
| [S25/Q23](#s25) | success | ["sheet1"] | 0 / {} | [] | ["AVG(\"Profit Margin\")"] | 10 | 6.749 |
| [S26/Q24](#s26) | success | ["sheet1"] | 0 / {} | ["is_low"] | ["AVG(\"Profit Margin\")", "AVG(\"Discount Amount\" / NULLIF(\"List Price Revenue\", 0) * 100)", "AVG(\"List Price Revenue\")", "AVG(\"Total Logistics Revenue\")", "AVG(\"List Price Revenue\" - \"Total Logistics Revenue\")", "AVG(\"List Price Revenue\" - \"Total Logistics Revenue\")", "AVG(\"List Price Revenue\")"] | 2 | 18.098 |
| [S27/Q25](#s27) | success | ["sheet1"] | 0 / {} | ["SUBSTRING(\"Destination\", 1, INSTR(\"Destination\", '-') - 1)", "SUBSTRING(\"Destination\", INSTR(\"Destination\", '-') + 1, INSTR(SUBSTRING(\"Destination\", INSTR(\"Destination\", '-') + 1), '-') - 1)"] | ["AVG(\"Profit Margin\")", "COUNT(*)", "AVG(\"Freight Cost\")", "AVG(\"Sales Quantity\")", "AVG(\"Freight Cost\" / NULLIF(\"Sales Quantity\", 0))"] | 15 | 11.419 |
| [S28/Q26](#s28) | success | ["sheet1"] | 0 / {} | ["CASE WHEN \"Discount Amount\" = 0 THEN '0%' WHEN \"Discount Amount\" / NULLIF(\"List Price Revenue\", 0) < 0.05 THEN '0-5%' WHEN \"Discount Amount\" / NULLIF(\"List Price Revenue\", 0) < 0.10 THEN '5-10%' WHEN \"Discount Amount\" / NULLIF(\"List Price Revenue\", 0) < 0.20 THEN '10-20%' WHEN \"Discount Amount\" / NULLIF(\"List Price Revenue\", 0) < 0.30 THEN '20-30%' ELSE '30%+' END"] | ["AVG(\"Profit Margin\")", "COUNT(*)", "SUM(CASE WHEN is_low = 1 THEN 1 ELSE 0 END)", "SUM(CASE WHEN is_low = 1 THEN 1 ELSE 0 END)", "COUNT(*)", "SUM(CASE WHEN is_low = 1 THEN 1 ELSE 0 END)"] | 6 | 23.364 |
| [S29/Q27](#s29) | success | ["sheet1"] | 0 / {} | ["\"Logistics Value-Added Service Revenue\"", "is_low"] | ["AVG(\"Profit Margin\")", "COUNT(*)", "AVG(\"Total Logistics Revenue\")", "AVG(\"Profit\")"] | 30 | 26.2 |
| [S30/Q28](#s30) | success | ["sheet1"] | 0 / {} | ["is_low"] | ["AVG(\"Profit Margin\")", "COUNT(CASE WHEN \"Logistics Value-Added Service Revenue\" > 0 THEN 1 END)", "AVG(\"Logistics Value-Added Service Revenue\")", "COUNT(*)", "AVG(\"Logistics Value-Added Service Revenue\")", "COUNT(CASE WHEN \"Logistics Value-Added Service Revenue\" > 0 THEN 1 END)", "AVG(\"Total Logistics Revenue\")"] | 2 | 15.851 |
| [S31/Q29](#s31) | success | ["sheet1"] | 0 / {} | ["\"Consigned Product\""] | ["AVG(\"Profit Margin\")", "AVG(CASE WHEN is_low = 1 THEN \"Freight Cost\" / NULLIF(\"Sales Quantity\", 0) END)", "AVG(CASE WHEN is_low = 0 THEN \"Freight Cost\" / NULLIF(\"Sales Quantity\", 0) END)", "AVG(CASE WHEN is_low = 1 THEN \"Total Logistics Cost\" / NULLIF(\"Sales Quantity\", 0) END)", "AVG(CASE WHEN is_low = 0 THEN \"Total Logistics Cost\" / NULLIF(\"Sales Quantity\", 0) END)", "AVG(CASE WHEN is_low = 1 THEN \"Total Logistics Revenue\" / NULLIF(\"Sales Quantity\", 0) END)", "AVG(CASE WHEN is_low = 0 THEN \"Total Logistics Revenue\" / NULLIF(\"Sales Quantity\", 0) END)"] | 8 | 42.218 |
| [S32/Q30](#s32) | success | ["sheet1"] | 0 / {} | [] | ["AVG(\"Profit Margin\")"] | 18250 | 80.787 |
| [S33/Q31](#s33) | success | ["sheet1"] | 0 / {} | [] | ["AVG(\"Profit Margin\")"] | 18250 | 78.162 |
| [S34/Q32](#s34) | success | ["sheet1"] | 0 / {} | [] | ["AVG(\"Profit Margin\")"] | 18250 | 78.309 |
| [S35/Q33](#s35) | success | ["sheet1"] | 0 / {} | ["\"Sales Quantity\""] | ["AVG(\"Profit Margin\")", "AVG(\"Profit Margin\")", "COUNT(*)", "AVG(\"Discount Amount\" / NULLIF(\"List Price Revenue\", 0) * 100)", "AVG(\"Total Logistics Revenue\")", "AVG(\"Total Logistics Cost\")", "AVG(\"Freight Cost\")", "AVG(\"Warehousing Cost\")", "AVG(\"Profit\")", "SUM(\"Profit\")"] | 35 | 7.896 |
| [S36/Q34](#s36) | success | ["sheet1"] | 0 / {} | ["\"Destination\""] | ["AVG(\"Profit Margin\")", "AVG(\"Profit Margin\")", "COUNT(*)", "AVG(\"Freight Cost\" / NULLIF(\"Sales Quantity\", 0))", "AVG(\"Total Logistics Cost\" / NULLIF(\"Sales Quantity\", 0))", "AVG(\"Total Logistics Revenue\" / NULLIF(\"Sales Quantity\", 0))", "SUM(\"Profit\")"] | 10 | 7.904 |
| [S37/Q35](#s37) | success | ["sheet1"] | 0 / {} | ["\"Consigned Product\"", "\"Sales Quantity\""] | ["AVG(\"Profit Margin\")", "AVG(\"Profit Margin\")", "COUNT(*)", "AVG(\"Discount Amount\" / NULLIF(\"List Price Revenue\", 0) * 100)", "AVG(\"Total Logistics Cost\" / NULLIF(\"Sales Quantity\", 0))", "AVG(\"Total Logistics Revenue\" / NULLIF(\"Sales Quantity\", 0))", "AVG(\"Profit\")"] | 77 | 7.979 |
| [S38/Q36](#s38) | success | ["sheet1"] | 0 / {} | [] | ["AVG(\"Profit Margin\")"] | 18250 | 77.147 |


## 元数据和设置

| SQL | 类别 | 状态 | 内容 |
| --- | --- | --- | --- |
| S1 | connection_setup | success | PRAGMA query_only=ON |
| S2 | metadata | success | SELECT name,sql FROM sqlite_master WHERE type='table' ORDER BY name |


## Python 与执行位置

人工源码审查：**database_first_violation**。Python visualization calls export the whole table and reproduce SQL-capable groupby aggregations. Rendering itself is allowed; this preprocessing violates database_first_v1. Preserve the primary attempt without rerun. [证据](../reviews/dacomp-005.json)。

P1：Visualize the key differences between low-margin and normal orders: cost structure, discount behavior, and quantity distribution. Matplotlib/seaborn visualization is needed since SQLite cannot produce plots.

[源码](../../../runs/dsv4flash-db-first-full-01/dacomp-005/attempt-01/python/P1.py)；[输出](../../../runs/dsv4flash-db-first-full-01/dacomp-005/attempt-01/python/P1.stdout)；[错误](../../../runs/dsv4flash-db-first-full-01/dacomp-005/attempt-01/python/P1.stderr)。检出需人工核验的 SQL 可实现操作：groupby(, .query(；不能仅凭理由判为合规。

P2：Visualize time trends and geographic/demographic patterns of low-margin orders. SQLite cannot produce plots.

[源码](../../../runs/dsv4flash-db-first-full-01/dacomp-005/attempt-01/python/P2.py)；[输出](../../../runs/dsv4flash-db-first-full-01/dacomp-005/attempt-01/python/P2.stdout)；[错误](../../../runs/dsv4flash-db-first-full-01/dacomp-005/attempt-01/python/P2.stderr)。检出需人工核验的 SQL 可实现操作：groupby(, .query(, sort_values(；不能仅凭理由判为合规。

P3：Statistical analysis of the key drivers of low-margin orders: correlation between quantity, discount rate, and cost components. SQLite cannot compute correlation matrices or statistical tests.

[源码](../../../runs/dsv4flash-db-first-full-01/dacomp-005/attempt-01/python/P3.py)；[输出](../../../runs/dsv4flash-db-first-full-01/dacomp-005/attempt-01/python/P3.stdout)；[错误](../../../runs/dsv4flash-db-first-full-01/dacomp-005/attempt-01/python/P3.stderr)。检出需人工核验的 SQL 可实现操作：groupby(, .query(, sort_values(；不能仅凭理由判为合规。

P4：Scenario analysis to quantify the impact of potential remedies: reducing per-unit costs to normal levels and/or moderating discounts. This requires arithmetic scenario calculations over retrieved data, which is clearer to do in Python with full data for scenario modeling.

[源码](../../../runs/dsv4flash-db-first-full-01/dacomp-005/attempt-01/python/P4.py)；[输出](../../../runs/dsv4flash-db-first-full-01/dacomp-005/attempt-01/python/P4.stdout)；[错误](../../../runs/dsv4flash-db-first-full-01/dacomp-005/attempt-01/python/P4.stderr)。检出需人工核验的 SQL 可实现操作：groupby(, .query(；不能仅凭理由判为合规。

P5：Create a visual summary of the scenario analysis - potential profit improvements from different remedy strategies. This requires a bar chart, which SQLite cannot produce.

[源码](../../../runs/dsv4flash-db-first-full-01/dacomp-005/attempt-01/python/P5.py)；[输出](../../../runs/dsv4flash-db-first-full-01/dacomp-005/attempt-01/python/P5.stdout)；[错误](../../../runs/dsv4flash-db-first-full-01/dacomp-005/attempt-01/python/P5.stderr)。自动源码筛查未检出预设迁出信号；这不是全面语义合规证明。

## 优化机会

已验证候选。筛选限于精确 SQL、相同自包含 CTE、相同单表完整过滤、可分解单表聚合；未覆盖任意 Join 等价和一般谓词蕴含。全部候选都是 offline，未测在线预测。

| 候选 | 类型 | 已有结果 | 覆盖 SQL | 后续次数 | 中间行数 | 验证 | 成本 |
| --- | --- | --- | --- | --- | --- | --- | --- |
| C1 | exact-result reuse | True | ["S32", "S33"] | 1 | unknown | not_verified_cap | Not tested |
| C2 | exact-result reuse | True | ["S34", "S38"] | 1 | unknown | not_verified_cap | Not tested |
| C3 | common subexpression | False | ["S8", "S9", "S10", "S11", "S12", "S13", "S14", "S15", "S16", "S17", "S18", "S19", "S20", "S21", "S22", "S23", "S24", "S26", "S27", "S28", "S29", "S30", "S31"] | 22 | 18250 | verified | Not benchmarked; correctness alone does not establish net speedup. |
| C4 | common subexpression | False | ["S35", "S36", "S37"] | 2 | 1243 | verified | Not benchmarked; correctness alone does not establish net speedup. |
| C5 | aggregate MV | False | ["S3", "S4", "S6"] | 2 | 1 | verified | Not benchmarked; correctness alone does not establish net speedup. |


已验证覆盖（含触发查询、候选并集去重）：29/36 条成功数据 SQL。正确性仅针对当前数据库快照；未测性能的候选不能声称已加速。

[完整 build/rewrite 与比较证据](dacomp-005.analysis.json)。

### C3：common subexpression

Identical self-contained CTE body across queries.

原查询 [S8](#s8), [S9](#s9), [S10](#s10), [S11](#s11), [S12](#s12), [S13](#s13), [S14](#s14), [S15](#s15), [S16](#s16), [S17](#s17), [S18](#s18), [S19](#s19), [S20](#s20), [S21](#s21), [S22](#s22), [S23](#s23), [S24](#s24), [S26](#s26), [S27](#s27), [S28](#s28), [S29](#s29), [S30](#s30), [S31](#s31) → 新增共享状态 C3 → 后续 22 次可复用。该构建点为事后假设，不代表 Agent 当时预知后续。

构建定义：

```sql
SELECT *, CASE WHEN "Profit Margin" < 0.5 * (SELECT AVG("Profit Margin") FROM sheet1) THEN 1 ELSE 0 END AS is_low FROM sheet1
```

受益查询 S8 的改写示例：

```sql
WITH lm AS (SELECT * FROM temp.reuse_candidate) SELECT is_low, COUNT(*) AS n, ROUND(AVG("Sales Quantity"), 2) AS avg_sales_qty, ROUND(AVG("Logistics Unit Price"), 2) AS avg_unit_price, ROUND(AVG("List Price Revenue"), 2) AS avg_list_price_rev, ROUND(AVG("Logistics Value-Added Service Revenue"), 2) AS avg_vas_rev, ROUND(AVG("Discount Amount"), 2) AS avg_discount, ROUND(AVG("Discount Amount") / AVG("List Price Revenue") * 100, 2) AS discount_pct_of_list, ROUND(AVG("Total Logistics Revenue"), 2) AS avg_total_rev, ROUND(AVG("Freight Cost"), 2) AS avg_freight, ROUND(AVG("Warehousing Cost"), 2) AS avg_warehousing, ROUND(AVG("Other Operating Costs"), 2) AS avg_other_op, ROUND(AVG("Total Logistics Cost"), 2) AS avg_total_cost, ROUND(AVG("Profit"), 2) AS avg_profit, ROUND(AVG("Profit Margin"), 4) AS avg_profit_margin FROM lm GROUP BY is_low
```

| 原 SQL | 列名一致 | 结果一致 | 比较方法 |
| --- | --- | --- | --- |
| S8 | True | True | exact_multiset |
| S9 | True | True | exact_multiset |
| S10 | True | True | ordered_numeric_tolerance |
| S11 | True | True | ordered_numeric_tolerance |
| S12 | True | True | exact_multiset |
| S13 | True | True | ordered_numeric_tolerance |
| S14 | True | True | ordered_numeric_tolerance |
| S15 | True | True | exact_multiset |
| S16 | True | True | ordered_numeric_tolerance |
| S17 | True | True | ordered_numeric_tolerance |
| S18 | True | True | exact_multiset |
| S19 | True | True | ordered_numeric_tolerance |
| S20 | True | True | ordered_numeric_tolerance |
| S21 | True | True | exact_multiset |
| S22 | True | True | exact_multiset |
| S23 | True | True | ordered_numeric_tolerance |
| S24 | True | True | ordered_numeric_tolerance |
| S26 | True | True | exact_multiset |
| S27 | True | True | ordered_numeric_tolerance |
| S28 | True | True | ordered_numeric_tolerance |
| S29 | True | True | ordered_numeric_tolerance |
| S30 | True | True | exact_multiset |
| S31 | True | True | ordered_numeric_tolerance |


验证状态：verified；成本结论：Not benchmarked; correctness alone does not establish net speedup.

### C4：common subexpression

Identical self-contained CTE body across queries.

原查询 [S35](#s35), [S36](#s36), [S37](#s37) → 新增共享状态 C4 → 后续 2 次可复用。该构建点为事后假设，不代表 Agent 当时预知后续。

构建定义：

```sql
SELECT *, CASE WHEN "Profit Margin" < 0.5 * (SELECT AVG("Profit Margin") FROM sheet1) THEN 1 ELSE 0 END AS is_low FROM sheet1 WHERE "Profit Margin" < 0.5 * (SELECT AVG("Profit Margin") FROM sheet1)
```

受益查询 S35 的改写示例：

```sql
WITH lm AS (SELECT * FROM temp.reuse_candidate) SELECT "Sales Quantity", COUNT(*) AS n, ROUND(AVG("Discount Amount" / NULLIF("List Price Revenue", 0) * 100), 2) AS avg_disc_rate, ROUND(AVG("Total Logistics Revenue"), 2) AS avg_rev, ROUND(AVG("Total Logistics Cost"), 2) AS avg_cost, ROUND(AVG("Freight Cost"), 2) AS avg_freight, ROUND(AVG("Warehousing Cost"), 2) AS avg_wh, ROUND(AVG("Profit"), 2) AS avg_profit, ROUND(SUM("Profit"), 2) AS total_profit FROM lm GROUP BY "Sales Quantity" ORDER BY "Sales Quantity"
```

| 原 SQL | 列名一致 | 结果一致 | 比较方法 |
| --- | --- | --- | --- |
| S35 | True | True | ordered_numeric_tolerance |
| S36 | True | True | ordered_numeric_tolerance |
| S37 | True | True | ordered_numeric_tolerance |


验证状态：verified；成本结论：Not benchmarked; correctness alone does not establish net speedup.

### C5：aggregate MV

Union of grouping keys; decomposable aggregate states; AVG uses SUM and non-NULL COUNT.

原查询 [S3](#s3), [S4](#s4), [S6](#s6) → 新增共享状态 C5 → 后续 2 次可复用。该构建点为事后假设，不代表 Agent 当时预知后续。

构建定义：

```sql
SELECT COUNT(*) AS __a0, SUM("Profit Margin") AS __a1_sum, COUNT("Profit Margin") AS __a1_n, MIN("Profit Margin") AS __a2, MAX("Profit Margin") AS __a3 FROM "sheet1" 
```

受益查询 S3 的改写示例：

```sql
SELECT SUM(__a0) AS total_rows FROM temp.reuse_candidate
```

| 原 SQL | 列名一致 | 结果一致 | 比较方法 |
| --- | --- | --- | --- |
| S3 | True | True | exact_multiset |
| S4 | True | True | exact_multiset |
| S6 | True | True | exact_multiset |


验证状态：verified；成本结论：Not benchmarked; correctness alone does not establish net speedup.

结果依赖：自动记录 SQL→Python 的接口父调用，以及源码中引用归档文件的消费者；字面值相同不认定因果。模型方向选择需要人工读取消息，尚未做全面因果标注。

[原始报告](../../../runs/dsv4flash-db-first-full-01/dacomp-005/attempt-01/answer.md)；[统一消息](../../../runs/dsv4flash-db-first-full-01/dacomp-005/attempt-01/messages.jsonl)；[原始 OpenCode 事件](../../../runs/dsv4flash-db-first-full-01/dacomp-005/attempt-01/opencode.jsonl)；[SQL 引擎日志](../../../runs/dsv4flash-db-first-full-01/dacomp-005/attempt-01/sql_journal.jsonl)。

[可读报告（本地图片链接规范化）](../answers/dacomp-005.md)。原始回答保留，分析结论未改写。

## S1

类别 `connection_setup`；来源 `connection`；调用 `529afc35effb460e9a3d529b811c75ae`；状态 `success`。

```sql
PRAGMA query_only=ON
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-005/attempt-01/sql/S1.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-005/attempt-01/sql/S1.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-005/attempt-01/results/S1.rows.jsonl)；完整：True；SHA256：`e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`。

## S2

类别 `metadata`；来源 `list_db`；调用 `529afc35effb460e9a3d529b811c75ae`；状态 `success`。

```sql
SELECT name,sql FROM sqlite_master WHERE type='table' ORDER BY name
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-005/attempt-01/sql/S2.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-005/attempt-01/sql/S2.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-005/attempt-01/results/S2.rows.jsonl)；完整：True；SHA256：`1da017ce066480cdde506c4bb99c9f5b07b8f8aa62b3d1442b5e2f6036b9ea14`。

## S3

类别 `data`；来源 `query_db`；调用 `285e5013caf940e8824c3dcfee0089c8`；状态 `success`。

```sql
SELECT COUNT(*) AS total_rows FROM sheet1
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-005/attempt-01/sql/S3.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-005/attempt-01/sql/S3.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-005/attempt-01/results/S3.rows.jsonl)；完整：True；SHA256：`757423e79e7b64c831fee8f4a2af142e23c2edbbfcf88b09b8a276f8433335a2`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "sheet1", "kind": "base", "block": null, "base_tables": ["sheet1"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |


## S4

类别 `data`；来源 `query_db`；调用 `371ae5fe920541ce87b73ef79fcd7d85`；状态 `success`。

```sql
SELECT 
  AVG("Profit Margin") AS avg_profit_margin,
  MIN("Profit Margin") AS min_profit_margin,
  MAX("Profit Margin") AS max_profit_margin
FROM sheet1
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-005/attempt-01/sql/S4.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-005/attempt-01/sql/S4.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-005/attempt-01/results/S4.rows.jsonl)；完整：True；SHA256：`46c8f3910e629d5d3e7d32e9084b8aa2ebad3b4e43ace5b1b11db6c7413cfbc0`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "sheet1", "kind": "base", "block": null, "base_tables": ["sheet1"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | AVG("Profit Margin") | [{"table": "sheet1", "column": "Profit Margin"}] | [] | False |
| B1 | MIN("Profit Margin") | [{"table": "sheet1", "column": "Profit Margin"}] | [] | False |
| B1 | MAX("Profit Margin") | [{"table": "sheet1", "column": "Profit Margin"}] | [] | False |


## S5

类别 `data`；来源 `query_db`；调用 `b5d09e80be4f4707b25cdcd753a69f59`；状态 `success`。

```sql
SELECT * FROM sheet1 LIMIT 5
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-005/attempt-01/sql/S5.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-005/attempt-01/sql/S5.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-005/attempt-01/results/S5.rows.jsonl)；完整：True；SHA256：`2d64fd9916cae9558db4667c53a0fbb8d03d11816934abe508e5b0a4b0b4736f`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "sheet1", "kind": "base", "block": null, "base_tables": ["sheet1"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |


## S6

类别 `data`；来源 `query_db`；调用 `e6ae076f1e2942ec81c60bd645dab629`；状态 `success`。

```sql
SELECT 0.5 * AVG("Profit Margin") AS low_margin_threshold FROM sheet1
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-005/attempt-01/sql/S6.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-005/attempt-01/sql/S6.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-005/attempt-01/results/S6.rows.jsonl)；完整：True；SHA256：`34e25e45d186798bb7862304b78dae63b3680939cced2795c5a072731816b2b3`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "sheet1", "kind": "base", "block": null, "base_tables": ["sheet1"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | AVG("Profit Margin") | [{"table": "sheet1", "column": "Profit Margin"}] | [] | False |


## S7

类别 `data`；来源 `query_db`；调用 `fb92f792b54a42008165317efda0f394`；状态 `success`。

```sql
SELECT 
  COUNT(*) AS total_orders,
  COUNT(CASE WHEN "Profit Margin" < 0.5 * (SELECT AVG("Profit Margin") FROM sheet1) THEN 1 END) AS low_margin_orders,
  ROUND(100.0 * COUNT(CASE WHEN "Profit Margin" < 0.5 * (SELECT AVG("Profit Margin") FROM sheet1) THEN 1 END) / COUNT(*), 2) AS low_margin_pct
FROM sheet1
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-005/attempt-01/sql/S7.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-005/attempt-01/sql/S7.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-005/attempt-01/results/S7.rows.jsonl)；完整：True；SHA256：`596fe3ed47b7db066cb38de526a6788be0cdf6060a3f5941f864089832b7551e`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "sheet1", "kind": "base", "block": null, "base_tables": ["sheet1"]}] | [] | [] |
| B2 | [{"alias": "sheet1", "kind": "base", "block": null, "base_tables": ["sheet1"]}] | [] | [] |
| B3 | [{"alias": "sheet1", "kind": "base", "block": null, "base_tables": ["sheet1"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | AVG("Profit Margin") | [{"table": "sheet1", "column": "Profit Margin"}] | [] | False |
| B2 | AVG("Profit Margin") | [{"table": "sheet1", "column": "Profit Margin"}] | [] | False |
| B3 | COUNT(*) | [] | [] | True |
| B3 | COUNT(CASE WHEN "Profit Margin" < 0.5 * (SELECT AVG("Profit Margin") FROM sheet1) THEN 1 END) | [] | [{"table": "sheet1", "column": "Profit Margin"}, {"table": "sheet1", "column": "Profit Margin"}] | False |
| B3 | COUNT(*) | [] | [] | True |
| B3 | COUNT(CASE WHEN "Profit Margin" < 0.5 * (SELECT AVG("Profit Margin") FROM sheet1) THEN 1 END) | [] | [{"table": "sheet1", "column": "Profit Margin"}, {"table": "sheet1", "column": "Profit Margin"}] | False |


## S8

类别 `data`；来源 `query_db`；调用 `b6ce414e649d4d49813ce54fd27dc32c`；状态 `success`。

```sql
WITH lm AS (
  SELECT *, CASE WHEN "Profit Margin" < 0.5 * (SELECT AVG("Profit Margin") FROM sheet1) THEN 1 ELSE 0 END AS is_low
  FROM sheet1
)
SELECT 
  is_low,
  COUNT(*) AS n,
  ROUND(AVG("Sales Quantity"),2) AS avg_sales_qty,
  ROUND(AVG("Logistics Unit Price"),2) AS avg_unit_price,
  ROUND(AVG("List Price Revenue"),2) AS avg_list_price_rev,
  ROUND(AVG("Logistics Value-Added Service Revenue"),2) AS avg_vas_rev,
  ROUND(AVG("Discount Amount"),2) AS avg_discount,
  ROUND(AVG("Discount Amount") / AVG("List Price Revenue") * 100,2) AS discount_pct_of_list,
  ROUND(AVG("Total Logistics Revenue"),2) AS avg_total_rev,
  ROUND(AVG("Freight Cost"),2) AS avg_freight,
  ROUND(AVG("Warehousing Cost"),2) AS avg_warehousing,
  ROUND(AVG("Other Operating Costs"),2) AS avg_other_op,
  ROUND(AVG("Total Logistics Cost"),2) AS avg_total_cost,
  ROUND(AVG("Profit"),2) AS avg_profit,
  ROUND(AVG("Profit Margin"),4) AS avg_profit_margin
FROM lm
GROUP BY is_low
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-005/attempt-01/sql/S8.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-005/attempt-01/sql/S8.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-005/attempt-01/results/S8.rows.jsonl)；完整：True；SHA256：`72fe1c6d80a5b52979416e254ccd45cb4cf801d59a8dc424df2cc169e054a975`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "sheet1", "kind": "base", "block": null, "base_tables": ["sheet1"]}] | [] | [] |
| B2 | [{"alias": "sheet1", "kind": "base", "block": null, "base_tables": ["sheet1"]}] | [] | [] |
| B3 | [{"alias": "lm", "kind": "derived", "block": "B2", "base_tables": ["sheet1"]}] | [] | ["is_low"] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | AVG("Profit Margin") | [{"table": "sheet1", "column": "Profit Margin"}] | [] | False |
| B3 | COUNT(*) | [] | [] | True |
| B3 | AVG("Sales Quantity") | [{"table": "sheet1", "column": "Sales Quantity"}] | [] | False |
| B3 | AVG("Logistics Unit Price") | [{"table": "sheet1", "column": "Logistics Unit Price"}] | [] | False |
| B3 | AVG("List Price Revenue") | [{"table": "sheet1", "column": "List Price Revenue"}] | [] | False |
| B3 | AVG("Logistics Value-Added Service Revenue") | [{"table": "sheet1", "column": "Logistics Value-Added Service Revenue"}] | [] | False |
| B3 | AVG("Discount Amount") | [{"table": "sheet1", "column": "Discount Amount"}] | [] | False |
| B3 | AVG("Total Logistics Revenue") | [{"table": "sheet1", "column": "Total Logistics Revenue"}] | [] | False |
| B3 | AVG("Freight Cost") | [{"table": "sheet1", "column": "Freight Cost"}] | [] | False |
| B3 | AVG("Warehousing Cost") | [{"table": "sheet1", "column": "Warehousing Cost"}] | [] | False |
| B3 | AVG("Other Operating Costs") | [{"table": "sheet1", "column": "Other Operating Costs"}] | [] | False |
| B3 | AVG("Total Logistics Cost") | [{"table": "sheet1", "column": "Total Logistics Cost"}] | [] | False |
| B3 | AVG("Profit") | [{"table": "sheet1", "column": "Profit"}] | [] | False |
| B3 | AVG("Profit Margin") | [{"table": "sheet1", "column": "Profit Margin"}] | [] | False |
| B3 | AVG("Discount Amount") | [{"table": "sheet1", "column": "Discount Amount"}] | [] | False |
| B3 | AVG("List Price Revenue") | [{"table": "sheet1", "column": "List Price Revenue"}] | [] | False |


## S9

类别 `data`；来源 `query_db`；调用 `38f5350471c8479181d084e40f631a33`；状态 `success`。

```sql
WITH lm AS (
  SELECT *, CASE WHEN "Profit Margin" < 0.5 * (SELECT AVG("Profit Margin") FROM sheet1) THEN 1 ELSE 0 END AS is_low
  FROM sheet1
)
SELECT 
  is_low,
  ROUND(AVG("Freight Cost") / NULLIF(AVG("Total Logistics Revenue"),0) * 100, 2) AS freight_pct_of_rev,
  ROUND(AVG("Warehousing Cost") / NULLIF(AVG("Total Logistics Revenue"),0) * 100, 2) AS warehousing_pct_of_rev,
  ROUND(AVG("Other Operating Costs") / NULLIF(AVG("Total Logistics Revenue"),0) * 100, 2) AS other_op_pct_of_rev,
  ROUND(AVG("Total Logistics Cost") / NULLIF(AVG("Total Logistics Revenue"),0) * 100, 2) AS cost_pct_of_rev,
  ROUND(AVG("Total Logistics Revenue") / NULLIF(AVG("Sales Quantity"),0), 2) AS revenue_per_unit,
  ROUND(AVG("Total Logistics Cost") / NULLIF(AVG("Sales Quantity"),0), 2) AS cost_per_unit
FROM lm
GROUP BY is_low
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-005/attempt-01/sql/S9.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-005/attempt-01/sql/S9.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-005/attempt-01/results/S9.rows.jsonl)；完整：True；SHA256：`cd504ebb2a2dec64c342a5cbf7a9b7334ab3be77580b87c0034fe53279080e79`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "sheet1", "kind": "base", "block": null, "base_tables": ["sheet1"]}] | [] | [] |
| B2 | [{"alias": "sheet1", "kind": "base", "block": null, "base_tables": ["sheet1"]}] | [] | [] |
| B3 | [{"alias": "lm", "kind": "derived", "block": "B2", "base_tables": ["sheet1"]}] | [] | ["is_low"] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | AVG("Profit Margin") | [{"table": "sheet1", "column": "Profit Margin"}] | [] | False |
| B3 | AVG("Total Logistics Revenue") | [{"table": "sheet1", "column": "Total Logistics Revenue"}] | [] | False |
| B3 | AVG("Total Logistics Cost") | [{"table": "sheet1", "column": "Total Logistics Cost"}] | [] | False |
| B3 | AVG("Freight Cost") | [{"table": "sheet1", "column": "Freight Cost"}] | [] | False |
| B3 | AVG("Warehousing Cost") | [{"table": "sheet1", "column": "Warehousing Cost"}] | [] | False |
| B3 | AVG("Other Operating Costs") | [{"table": "sheet1", "column": "Other Operating Costs"}] | [] | False |
| B3 | AVG("Total Logistics Cost") | [{"table": "sheet1", "column": "Total Logistics Cost"}] | [] | False |
| B3 | AVG("Sales Quantity") | [{"table": "sheet1", "column": "Sales Quantity"}] | [] | False |
| B3 | AVG("Sales Quantity") | [{"table": "sheet1", "column": "Sales Quantity"}] | [] | False |
| B3 | AVG("Total Logistics Revenue") | [{"table": "sheet1", "column": "Total Logistics Revenue"}] | [] | False |
| B3 | AVG("Total Logistics Revenue") | [{"table": "sheet1", "column": "Total Logistics Revenue"}] | [] | False |
| B3 | AVG("Total Logistics Revenue") | [{"table": "sheet1", "column": "Total Logistics Revenue"}] | [] | False |
| B3 | AVG("Total Logistics Revenue") | [{"table": "sheet1", "column": "Total Logistics Revenue"}] | [] | False |


## S10

类别 `data`；来源 `query_db`；调用 `c34e35232b894dcdb15e51d629631b27`；状态 `success`。

```sql
WITH lm AS (
  SELECT *, CASE WHEN "Profit Margin" < 0.5 * (SELECT AVG("Profit Margin") FROM sheet1) THEN 1 ELSE 0 END AS is_low
  FROM sheet1
)
SELECT 
  "Destination",
  SUM(CASE WHEN is_low = 1 THEN 1 ELSE 0 END) AS low_margin_count,
  SUM(CASE WHEN is_low = 0 THEN 1 ELSE 0 END) AS normal_count,
  ROUND(100.0 * SUM(CASE WHEN is_low = 1 THEN 1 ELSE 0 END) / NULLIF(SUM(CASE WHEN is_low = 1 THEN 1 ELSE 0 END) + SUM(CASE WHEN is_low = 0 THEN 1 ELSE 0 END), 0), 2) AS low_margin_pct,
  ROUND(AVG(CASE WHEN is_low = 1 THEN "Freight Cost" END), 2) AS lm_avg_freight,
  ROUND(AVG(CASE WHEN is_low = 0 THEN "Freight Cost" END), 2) AS normal_avg_freight
FROM lm
GROUP BY "Destination"
ORDER BY low_margin_count DESC
LIMIT 20
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-005/attempt-01/sql/S10.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-005/attempt-01/sql/S10.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-005/attempt-01/results/S10.rows.jsonl)；完整：True；SHA256：`04b656737f046cea2d3f10ad30d1cc3ac42dea636f1e5b6cf8ea1741c84a4905`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "sheet1", "kind": "base", "block": null, "base_tables": ["sheet1"]}] | [] | [] |
| B2 | [{"alias": "sheet1", "kind": "base", "block": null, "base_tables": ["sheet1"]}] | [] | [] |
| B3 | [{"alias": "lm", "kind": "derived", "block": "B2", "base_tables": ["sheet1"]}] | [] | ["\"Destination\""] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | AVG("Profit Margin") | [{"table": "sheet1", "column": "Profit Margin"}] | [] | False |
| B3 | SUM(CASE WHEN is_low = 1 THEN 1 ELSE 0 END) | [] | [{"table": "sheet1", "column": "Profit Margin"}, {"table": "sheet1", "column": "Profit Margin"}] | False |
| B3 | SUM(CASE WHEN is_low = 0 THEN 1 ELSE 0 END) | [] | [{"table": "sheet1", "column": "Profit Margin"}, {"table": "sheet1", "column": "Profit Margin"}] | False |
| B3 | AVG(CASE WHEN is_low = 1 THEN "Freight Cost" END) | [{"table": "sheet1", "column": "Freight Cost"}] | [{"table": "sheet1", "column": "Profit Margin"}, {"table": "sheet1", "column": "Profit Margin"}] | False |
| B3 | AVG(CASE WHEN is_low = 0 THEN "Freight Cost" END) | [{"table": "sheet1", "column": "Freight Cost"}] | [{"table": "sheet1", "column": "Profit Margin"}, {"table": "sheet1", "column": "Profit Margin"}] | False |
| B3 | SUM(CASE WHEN is_low = 1 THEN 1 ELSE 0 END) | [] | [{"table": "sheet1", "column": "Profit Margin"}, {"table": "sheet1", "column": "Profit Margin"}] | False |
| B3 | SUM(CASE WHEN is_low = 1 THEN 1 ELSE 0 END) | [] | [{"table": "sheet1", "column": "Profit Margin"}, {"table": "sheet1", "column": "Profit Margin"}] | False |
| B3 | SUM(CASE WHEN is_low = 0 THEN 1 ELSE 0 END) | [] | [{"table": "sheet1", "column": "Profit Margin"}, {"table": "sheet1", "column": "Profit Margin"}] | False |


## S11

类别 `data`；来源 `query_db`；调用 `247de9067a774841bbac6d9ebf8ba600`；状态 `success`。

```sql
WITH lm AS (
  SELECT *, CASE WHEN "Profit Margin" < 0.5 * (SELECT AVG("Profit Margin") FROM sheet1) THEN 1 ELSE 0 END AS is_low
  FROM sheet1
)
SELECT 
  "Consigned Product",
  SUM(CASE WHEN is_low = 1 THEN 1 ELSE 0 END) AS low_margin_count,
  SUM(CASE WHEN is_low = 0 THEN 1 ELSE 0 END) AS normal_count,
  ROUND(100.0 * SUM(CASE WHEN is_low = 1 THEN 1 ELSE 0 END) / NULLIF(SUM(CASE WHEN is_low = 1 THEN 1 ELSE 0 END) + SUM(CASE WHEN is_low = 0 THEN 1 ELSE 0 END), 0), 2) AS low_margin_pct,
  ROUND(AVG(CASE WHEN is_low = 1 THEN "Sales Quantity" END), 2) AS lm_avg_qty,
  ROUND(AVG(CASE WHEN is_low = 0 THEN "Sales Quantity" END), 2) AS normal_avg_qty
FROM lm
GROUP BY "Consigned Product"
ORDER BY low_margin_count DESC
LIMIT 20
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-005/attempt-01/sql/S11.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-005/attempt-01/sql/S11.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-005/attempt-01/results/S11.rows.jsonl)；完整：True；SHA256：`339ffba6ab3c8c2d4e005dd4bb89a5ace40aea8e0f11b5a551601365909326ea`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "sheet1", "kind": "base", "block": null, "base_tables": ["sheet1"]}] | [] | [] |
| B2 | [{"alias": "sheet1", "kind": "base", "block": null, "base_tables": ["sheet1"]}] | [] | [] |
| B3 | [{"alias": "lm", "kind": "derived", "block": "B2", "base_tables": ["sheet1"]}] | [] | ["\"Consigned Product\""] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | AVG("Profit Margin") | [{"table": "sheet1", "column": "Profit Margin"}] | [] | False |
| B3 | SUM(CASE WHEN is_low = 1 THEN 1 ELSE 0 END) | [] | [{"table": "sheet1", "column": "Profit Margin"}, {"table": "sheet1", "column": "Profit Margin"}] | False |
| B3 | SUM(CASE WHEN is_low = 0 THEN 1 ELSE 0 END) | [] | [{"table": "sheet1", "column": "Profit Margin"}, {"table": "sheet1", "column": "Profit Margin"}] | False |
| B3 | AVG(CASE WHEN is_low = 1 THEN "Sales Quantity" END) | [{"table": "sheet1", "column": "Sales Quantity"}] | [{"table": "sheet1", "column": "Profit Margin"}, {"table": "sheet1", "column": "Profit Margin"}] | False |
| B3 | AVG(CASE WHEN is_low = 0 THEN "Sales Quantity" END) | [{"table": "sheet1", "column": "Sales Quantity"}] | [{"table": "sheet1", "column": "Profit Margin"}, {"table": "sheet1", "column": "Profit Margin"}] | False |
| B3 | SUM(CASE WHEN is_low = 1 THEN 1 ELSE 0 END) | [] | [{"table": "sheet1", "column": "Profit Margin"}, {"table": "sheet1", "column": "Profit Margin"}] | False |
| B3 | SUM(CASE WHEN is_low = 1 THEN 1 ELSE 0 END) | [] | [{"table": "sheet1", "column": "Profit Margin"}, {"table": "sheet1", "column": "Profit Margin"}] | False |
| B3 | SUM(CASE WHEN is_low = 0 THEN 1 ELSE 0 END) | [] | [{"table": "sheet1", "column": "Profit Margin"}, {"table": "sheet1", "column": "Profit Margin"}] | False |


## S12

类别 `data`；来源 `query_db`；调用 `b83cd558000040338e682c171deb9e90`；状态 `success`。

```sql
WITH lm AS (
  SELECT *, CASE WHEN "Profit Margin" < 0.5 * (SELECT AVG("Profit Margin") FROM sheet1) THEN 1 ELSE 0 END AS is_low
  FROM sheet1
)
SELECT 
  "Customer Gender",
  SUM(CASE WHEN is_low = 1 THEN 1 ELSE 0 END) AS low_margin_count,
  SUM(CASE WHEN is_low = 0 THEN 1 ELSE 0 END) AS normal_count,
  ROUND(100.0 * SUM(CASE WHEN is_low = 1 THEN 1 ELSE 0 END) / NULLIF(SUM(CASE WHEN is_low = 1 THEN 1 ELSE 0 END) + SUM(CASE WHEN is_low = 0 THEN 1 ELSE 0 END), 0), 2) AS low_margin_pct
FROM lm
GROUP BY "Customer Gender"
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-005/attempt-01/sql/S12.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-005/attempt-01/sql/S12.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-005/attempt-01/results/S12.rows.jsonl)；完整：True；SHA256：`9c33c7b637c8b2c656e46a9727ca48ed52d1174a0307169d335f98cab230aa4d`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "sheet1", "kind": "base", "block": null, "base_tables": ["sheet1"]}] | [] | [] |
| B2 | [{"alias": "sheet1", "kind": "base", "block": null, "base_tables": ["sheet1"]}] | [] | [] |
| B3 | [{"alias": "lm", "kind": "derived", "block": "B2", "base_tables": ["sheet1"]}] | [] | ["\"Customer Gender\""] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | AVG("Profit Margin") | [{"table": "sheet1", "column": "Profit Margin"}] | [] | False |
| B3 | SUM(CASE WHEN is_low = 1 THEN 1 ELSE 0 END) | [] | [{"table": "sheet1", "column": "Profit Margin"}, {"table": "sheet1", "column": "Profit Margin"}] | False |
| B3 | SUM(CASE WHEN is_low = 0 THEN 1 ELSE 0 END) | [] | [{"table": "sheet1", "column": "Profit Margin"}, {"table": "sheet1", "column": "Profit Margin"}] | False |
| B3 | SUM(CASE WHEN is_low = 1 THEN 1 ELSE 0 END) | [] | [{"table": "sheet1", "column": "Profit Margin"}, {"table": "sheet1", "column": "Profit Margin"}] | False |
| B3 | SUM(CASE WHEN is_low = 1 THEN 1 ELSE 0 END) | [] | [{"table": "sheet1", "column": "Profit Margin"}, {"table": "sheet1", "column": "Profit Margin"}] | False |
| B3 | SUM(CASE WHEN is_low = 0 THEN 1 ELSE 0 END) | [] | [{"table": "sheet1", "column": "Profit Margin"}, {"table": "sheet1", "column": "Profit Margin"}] | False |


## S13

类别 `data`；来源 `query_db`；调用 `c800e67b69ee45e4ae9e4877a019d923`；状态 `success`。

```sql
WITH lm AS (
  SELECT *, CASE WHEN "Profit Margin" < 0.5 * (SELECT AVG("Profit Margin") FROM sheet1) THEN 1 ELSE 0 END AS is_low
  FROM sheet1
)
SELECT 
  "Age Range",
  SUM(CASE WHEN is_low = 1 THEN 1 ELSE 0 END) AS low_margin_count,
  SUM(CASE WHEN is_low = 0 THEN 1 ELSE 0 END) AS normal_count,
  ROUND(100.0 * SUM(CASE WHEN is_low = 1 THEN 1 ELSE 0 END) / NULLIF(SUM(CASE WHEN is_low = 1 THEN 1 ELSE 0 END) + SUM(CASE WHEN is_low = 0 THEN 1 ELSE 0 END), 0), 2) AS low_margin_pct,
  ROUND(AVG(CASE WHEN is_low = 1 THEN "Customer Age" END), 1) AS lm_avg_age,
  ROUND(AVG(CASE WHEN is_low = 0 THEN "Customer Age" END), 1) AS normal_avg_age
FROM lm
GROUP BY "Age Range"
ORDER BY "Age Range"
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-005/attempt-01/sql/S13.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-005/attempt-01/sql/S13.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-005/attempt-01/results/S13.rows.jsonl)；完整：True；SHA256：`ae53be966241f8ba13a2c23e2cf3e06a77f2f430816cf8e73f3c35c209561591`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "sheet1", "kind": "base", "block": null, "base_tables": ["sheet1"]}] | [] | [] |
| B2 | [{"alias": "sheet1", "kind": "base", "block": null, "base_tables": ["sheet1"]}] | [] | [] |
| B3 | [{"alias": "lm", "kind": "derived", "block": "B2", "base_tables": ["sheet1"]}] | [] | ["\"Age Range\""] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | AVG("Profit Margin") | [{"table": "sheet1", "column": "Profit Margin"}] | [] | False |
| B3 | SUM(CASE WHEN is_low = 1 THEN 1 ELSE 0 END) | [] | [{"table": "sheet1", "column": "Profit Margin"}, {"table": "sheet1", "column": "Profit Margin"}] | False |
| B3 | SUM(CASE WHEN is_low = 0 THEN 1 ELSE 0 END) | [] | [{"table": "sheet1", "column": "Profit Margin"}, {"table": "sheet1", "column": "Profit Margin"}] | False |
| B3 | AVG(CASE WHEN is_low = 1 THEN "Customer Age" END) | [{"table": "sheet1", "column": "Customer Age"}] | [{"table": "sheet1", "column": "Profit Margin"}, {"table": "sheet1", "column": "Profit Margin"}] | False |
| B3 | AVG(CASE WHEN is_low = 0 THEN "Customer Age" END) | [{"table": "sheet1", "column": "Customer Age"}] | [{"table": "sheet1", "column": "Profit Margin"}, {"table": "sheet1", "column": "Profit Margin"}] | False |
| B3 | SUM(CASE WHEN is_low = 1 THEN 1 ELSE 0 END) | [] | [{"table": "sheet1", "column": "Profit Margin"}, {"table": "sheet1", "column": "Profit Margin"}] | False |
| B3 | SUM(CASE WHEN is_low = 1 THEN 1 ELSE 0 END) | [] | [{"table": "sheet1", "column": "Profit Margin"}, {"table": "sheet1", "column": "Profit Margin"}] | False |
| B3 | SUM(CASE WHEN is_low = 0 THEN 1 ELSE 0 END) | [] | [{"table": "sheet1", "column": "Profit Margin"}, {"table": "sheet1", "column": "Profit Margin"}] | False |


## S14

类别 `data`；来源 `query_db`；调用 `83094e8947634da19dd9f57167e30fd2`；状态 `success`。

```sql
WITH lm AS (
  SELECT *, CASE WHEN "Profit Margin" < 0.5 * (SELECT AVG("Profit Margin") FROM sheet1) THEN 1 ELSE 0 END AS is_low
  FROM sheet1
)
SELECT 
  strftime('%Y-%m', "Date") AS month,
  SUM(CASE WHEN is_low = 1 THEN 1 ELSE 0 END) AS low_margin_count,
  SUM(CASE WHEN is_low = 0 THEN 1 ELSE 0 END) AS normal_count,
  ROUND(100.0 * SUM(CASE WHEN is_low = 1 THEN 1 ELSE 0 END) / NULLIF(SUM(CASE WHEN is_low = 1 THEN 1 ELSE 0 END) + SUM(CASE WHEN is_low = 0 THEN 1 ELSE 0 END), 0), 2) AS low_margin_pct
FROM lm
GROUP BY month
ORDER BY month
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-005/attempt-01/sql/S14.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-005/attempt-01/sql/S14.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-005/attempt-01/results/S14.rows.jsonl)；完整：True；SHA256：`15a15bf4a4d0af390002d0858056392cb0c59b5ef0b81d434fd032ae22eefc1f`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "sheet1", "kind": "base", "block": null, "base_tables": ["sheet1"]}] | [] | [] |
| B2 | [{"alias": "sheet1", "kind": "base", "block": null, "base_tables": ["sheet1"]}] | [] | [] |
| B3 | [{"alias": "lm", "kind": "derived", "block": "B2", "base_tables": ["sheet1"]}] | [] | ["STRFTIME('%Y-%m', \"Date\")"] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | AVG("Profit Margin") | [{"table": "sheet1", "column": "Profit Margin"}] | [] | False |
| B3 | SUM(CASE WHEN is_low = 1 THEN 1 ELSE 0 END) | [] | [{"table": "sheet1", "column": "Profit Margin"}, {"table": "sheet1", "column": "Profit Margin"}] | False |
| B3 | SUM(CASE WHEN is_low = 0 THEN 1 ELSE 0 END) | [] | [{"table": "sheet1", "column": "Profit Margin"}, {"table": "sheet1", "column": "Profit Margin"}] | False |
| B3 | SUM(CASE WHEN is_low = 1 THEN 1 ELSE 0 END) | [] | [{"table": "sheet1", "column": "Profit Margin"}, {"table": "sheet1", "column": "Profit Margin"}] | False |
| B3 | SUM(CASE WHEN is_low = 1 THEN 1 ELSE 0 END) | [] | [{"table": "sheet1", "column": "Profit Margin"}, {"table": "sheet1", "column": "Profit Margin"}] | False |
| B3 | SUM(CASE WHEN is_low = 0 THEN 1 ELSE 0 END) | [] | [{"table": "sheet1", "column": "Profit Margin"}, {"table": "sheet1", "column": "Profit Margin"}] | False |


## S15

类别 `data`；来源 `query_db`；调用 `8bc2f5407a5549be84564f909b05162c`；状态 `success`。

```sql
WITH lm AS (
  SELECT *, CASE WHEN "Profit Margin" < 0.5 * (SELECT AVG("Profit Margin") FROM sheet1) THEN 1 ELSE 0 END AS is_low
  FROM sheet1
)
SELECT 
  is_low,
  ROUND(AVG("Discount Amount"), 2) AS avg_discount_abs,
  ROUND(AVG("Discount Amount" / NULLIF("List Price Revenue", 0) * 100), 2) AS avg_discount_rate_pct,
  COUNT(CASE WHEN "Discount Amount" > 0 THEN 1 END) AS orders_with_discount,
  ROUND(100.0 * COUNT(CASE WHEN "Discount Amount" > 0 THEN 1 END) / COUNT(*), 2) AS pct_with_discount
FROM lm
GROUP BY is_low
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-005/attempt-01/sql/S15.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-005/attempt-01/sql/S15.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-005/attempt-01/results/S15.rows.jsonl)；完整：True；SHA256：`03f1685176118339d5d871259b9b0ba4ab65783f51638f6c9830ae2582207b7e`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "sheet1", "kind": "base", "block": null, "base_tables": ["sheet1"]}] | [] | [] |
| B2 | [{"alias": "sheet1", "kind": "base", "block": null, "base_tables": ["sheet1"]}] | [] | [] |
| B3 | [{"alias": "lm", "kind": "derived", "block": "B2", "base_tables": ["sheet1"]}] | [] | ["is_low"] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | AVG("Profit Margin") | [{"table": "sheet1", "column": "Profit Margin"}] | [] | False |
| B3 | COUNT(CASE WHEN "Discount Amount" > 0 THEN 1 END) | [] | [{"table": "sheet1", "column": "Discount Amount"}] | False |
| B3 | AVG("Discount Amount") | [{"table": "sheet1", "column": "Discount Amount"}] | [] | False |
| B3 | AVG("Discount Amount" / NULLIF("List Price Revenue", 0) * 100) | [{"table": "sheet1", "column": "Discount Amount"}, {"table": "sheet1", "column": "List Price Revenue"}] | [] | False |
| B3 | COUNT(*) | [] | [] | True |
| B3 | COUNT(CASE WHEN "Discount Amount" > 0 THEN 1 END) | [] | [{"table": "sheet1", "column": "Discount Amount"}] | False |


## S16

类别 `data`；来源 `query_db`；调用 `d8812bdfd8364c6ba337417c645be5fc`；状态 `success`。

```sql
WITH lm AS (
  SELECT *, CASE WHEN "Profit Margin" < 0.5 * (SELECT AVG("Profit Margin") FROM sheet1) THEN 1 ELSE 0 END AS is_low
  FROM sheet1
)
SELECT 
  "Sales Quantity",
  is_low,
  COUNT(*) AS n,
  ROUND(AVG("Total Logistics Revenue"), 2) AS avg_rev,
  ROUND(AVG("Total Logistics Cost"), 2) AS avg_cost,
  ROUND(AVG("Profit"), 2) AS avg_profit,
  ROUND(AVG("Profit Margin"), 4) AS avg_pm
FROM lm
GROUP BY "Sales Quantity", is_low
ORDER BY "Sales Quantity", is_low
LIMIT 30
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-005/attempt-01/sql/S16.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-005/attempt-01/sql/S16.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-005/attempt-01/results/S16.rows.jsonl)；完整：True；SHA256：`743de52f92b286a36e0607b8e0bfd541dc7cd0f08ae294d19ee6ad6df0b00c42`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "sheet1", "kind": "base", "block": null, "base_tables": ["sheet1"]}] | [] | [] |
| B2 | [{"alias": "sheet1", "kind": "base", "block": null, "base_tables": ["sheet1"]}] | [] | [] |
| B3 | [{"alias": "lm", "kind": "derived", "block": "B2", "base_tables": ["sheet1"]}] | [] | ["\"Sales Quantity\"", "is_low"] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | AVG("Profit Margin") | [{"table": "sheet1", "column": "Profit Margin"}] | [] | False |
| B3 | COUNT(*) | [] | [] | True |
| B3 | AVG("Total Logistics Revenue") | [{"table": "sheet1", "column": "Total Logistics Revenue"}] | [] | False |
| B3 | AVG("Total Logistics Cost") | [{"table": "sheet1", "column": "Total Logistics Cost"}] | [] | False |
| B3 | AVG("Profit") | [{"table": "sheet1", "column": "Profit"}] | [] | False |
| B3 | AVG("Profit Margin") | [{"table": "sheet1", "column": "Profit Margin"}] | [] | False |


## S17

类别 `data`；来源 `query_db`；调用 `e9ecc6129694435b9d7f24e6fc030dcc`；状态 `success`。

```sql
WITH lm AS (
  SELECT *, CASE WHEN "Profit Margin" < 0.5 * (SELECT AVG("Profit Margin") FROM sheet1) THEN 1 ELSE 0 END AS is_low
  FROM sheet1
)
SELECT 
  CASE WHEN "Sales Quantity" <= 5 THEN 'Qty<=5' 
       WHEN "Sales Quantity" <= 10 THEN '6-10'
       WHEN "Sales Quantity" <= 20 THEN '11-20'
       WHEN "Sales Quantity" <= 40 THEN '21-40'
       ELSE '41+' END AS qty_band,
  is_low,
  COUNT(*) AS n,
  ROUND(AVG("Discount Amount" / NULLIF("List Price Revenue",0) * 100),2) AS avg_disc_rate,
  ROUND(AVG("Total Logistics Revenue"),2) AS avg_rev,
  ROUND(AVG("Total Logistics Cost"),2) AS avg_cost,
  ROUND(AVG("Freight Cost"),2) AS avg_freight,
  ROUND(AVG("Warehousing Cost"),2) AS avg_wh,
  ROUND(AVG("Other Operating Costs"),2) AS avg_other,
  ROUND(AVG("Profit"),2) AS avg_profit
FROM lm
GROUP BY qty_band, is_low
ORDER BY qty_band, is_low
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-005/attempt-01/sql/S17.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-005/attempt-01/sql/S17.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-005/attempt-01/results/S17.rows.jsonl)；完整：True；SHA256：`04fb50f38691d95940d03de6ef785752119af454e61c756bbe3d38d755588115`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "sheet1", "kind": "base", "block": null, "base_tables": ["sheet1"]}] | [] | [] |
| B2 | [{"alias": "sheet1", "kind": "base", "block": null, "base_tables": ["sheet1"]}] | [] | [] |
| B3 | [{"alias": "lm", "kind": "derived", "block": "B2", "base_tables": ["sheet1"]}] | [] | ["CASE WHEN \"Sales Quantity\" <= 5 THEN 'Qty<=5' WHEN \"Sales Quantity\" <= 10 THEN '6-10' WHEN \"Sales Quantity\" <= 20 THEN '11-20' WHEN \"Sales Quantity\" <= 40 THEN '21-40' ELSE '41+' END", "is_low"] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | AVG("Profit Margin") | [{"table": "sheet1", "column": "Profit Margin"}] | [] | False |
| B3 | COUNT(*) | [] | [] | True |
| B3 | AVG("Discount Amount" / NULLIF("List Price Revenue", 0) * 100) | [{"table": "sheet1", "column": "Discount Amount"}, {"table": "sheet1", "column": "List Price Revenue"}] | [] | False |
| B3 | AVG("Total Logistics Revenue") | [{"table": "sheet1", "column": "Total Logistics Revenue"}] | [] | False |
| B3 | AVG("Total Logistics Cost") | [{"table": "sheet1", "column": "Total Logistics Cost"}] | [] | False |
| B3 | AVG("Freight Cost") | [{"table": "sheet1", "column": "Freight Cost"}] | [] | False |
| B3 | AVG("Warehousing Cost") | [{"table": "sheet1", "column": "Warehousing Cost"}] | [] | False |
| B3 | AVG("Other Operating Costs") | [{"table": "sheet1", "column": "Other Operating Costs"}] | [] | False |
| B3 | AVG("Profit") | [{"table": "sheet1", "column": "Profit"}] | [] | False |


## S18

类别 `data`；来源 `query_db`；调用 `3558455d9b4b4b68ab6be286e8e4758f`；状态 `success`。

```sql
WITH lm AS (
  SELECT *, CASE WHEN "Profit Margin" < 0.5 * (SELECT AVG("Profit Margin") FROM sheet1) THEN 1 ELSE 0 END AS is_low
  FROM sheet1
)
SELECT 
  is_low,
  MIN("Sales Quantity") AS min_qty,
  ROUND(AVG("Sales Quantity"),2) AS avg_qty,
  MAX("Sales Quantity") AS max_qty,
  COUNT(CASE WHEN "Sales Quantity" <= 6 THEN 1 END) AS qty_le_6,
  ROUND(100.0 * COUNT(CASE WHEN "Sales Quantity" <= 6 THEN 1 END) / COUNT(*), 2) AS pct_qty_le_6
FROM lm
GROUP BY is_low
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-005/attempt-01/sql/S18.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-005/attempt-01/sql/S18.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-005/attempt-01/results/S18.rows.jsonl)；完整：True；SHA256：`89d56570a1e917b215fed7aa931b1a276e67e4d166d84fc92927eb21e680b060`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "sheet1", "kind": "base", "block": null, "base_tables": ["sheet1"]}] | [] | [] |
| B2 | [{"alias": "sheet1", "kind": "base", "block": null, "base_tables": ["sheet1"]}] | [] | [] |
| B3 | [{"alias": "lm", "kind": "derived", "block": "B2", "base_tables": ["sheet1"]}] | [] | ["is_low"] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | AVG("Profit Margin") | [{"table": "sheet1", "column": "Profit Margin"}] | [] | False |
| B3 | MIN("Sales Quantity") | [{"table": "sheet1", "column": "Sales Quantity"}] | [] | False |
| B3 | MAX("Sales Quantity") | [{"table": "sheet1", "column": "Sales Quantity"}] | [] | False |
| B3 | COUNT(CASE WHEN "Sales Quantity" <= 6 THEN 1 END) | [] | [{"table": "sheet1", "column": "Sales Quantity"}] | False |
| B3 | AVG("Sales Quantity") | [{"table": "sheet1", "column": "Sales Quantity"}] | [] | False |
| B3 | COUNT(*) | [] | [] | True |
| B3 | COUNT(CASE WHEN "Sales Quantity" <= 6 THEN 1 END) | [] | [{"table": "sheet1", "column": "Sales Quantity"}] | False |


## S19

类别 `data`；来源 `query_db`；调用 `2699ea6963544deb865cb091bc18f208`；状态 `success`。

```sql
WITH lm AS (
  SELECT *, CASE WHEN "Profit Margin" < 0.5 * (SELECT AVG("Profit Margin") FROM sheet1) THEN 1 ELSE 0 END AS is_low
  FROM sheet1
)
SELECT 
  "Destination",
  COUNT(*) AS total,
  SUM(CASE WHEN is_low = 1 THEN 1 ELSE 0 END) AS low_cnt,
  ROUND(100.0 * SUM(CASE WHEN is_low = 1 THEN 1 ELSE 0 END) / COUNT(*), 2) AS low_pct,
  ROUND(AVG("Sales Quantity"), 2) AS avg_qty,
  ROUND(AVG("Discount Amount" / NULLIF("List Price Revenue",0) * 100), 2) AS avg_disc_rate
FROM lm
GROUP BY "Destination"
HAVING total >= 30
ORDER BY low_pct DESC
LIMIT 20
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-005/attempt-01/sql/S19.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-005/attempt-01/sql/S19.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-005/attempt-01/results/S19.rows.jsonl)；完整：True；SHA256：`b60e2e89906c0918bae97fc24846acbb439782fd6f05111cd214e80b39094cdc`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "sheet1", "kind": "base", "block": null, "base_tables": ["sheet1"]}] | [] | [] |
| B2 | [{"alias": "sheet1", "kind": "base", "block": null, "base_tables": ["sheet1"]}] | [] | [] |
| B3 | [{"alias": "lm", "kind": "derived", "block": "B2", "base_tables": ["sheet1"]}] | [] | ["\"Destination\""] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | AVG("Profit Margin") | [{"table": "sheet1", "column": "Profit Margin"}] | [] | False |
| B3 | COUNT(*) | [] | [] | True |
| B3 | SUM(CASE WHEN is_low = 1 THEN 1 ELSE 0 END) | [] | [{"table": "sheet1", "column": "Profit Margin"}, {"table": "sheet1", "column": "Profit Margin"}] | False |
| B3 | AVG("Sales Quantity") | [{"table": "sheet1", "column": "Sales Quantity"}] | [] | False |
| B3 | AVG("Discount Amount" / NULLIF("List Price Revenue", 0) * 100) | [{"table": "sheet1", "column": "Discount Amount"}, {"table": "sheet1", "column": "List Price Revenue"}] | [] | False |
| B3 | COUNT(*) | [] | [] | True |
| B3 | SUM(CASE WHEN is_low = 1 THEN 1 ELSE 0 END) | [] | [{"table": "sheet1", "column": "Profit Margin"}, {"table": "sheet1", "column": "Profit Margin"}] | False |


## S20

类别 `data`；来源 `query_db`；调用 `119afd9159984851a49bda1c373df8f0`；状态 `success`。

```sql
WITH lm AS (
  SELECT *, CASE WHEN "Profit Margin" < 0.5 * (SELECT AVG("Profit Margin") FROM sheet1) THEN 1 ELSE 0 END AS is_low
  FROM sheet1
)
SELECT 
  SUBSTR("Destination", 1, INSTR("Destination", '-') - 1) AS region,
  SUM(CASE WHEN is_low = 1 THEN 1 ELSE 0 END) AS low_cnt,
  SUM(CASE WHEN is_low = 0 THEN 1 ELSE 0 END) AS normal_cnt,
  ROUND(100.0 * SUM(CASE WHEN is_low = 1 THEN 1 ELSE 0 END) / COUNT(*), 2) AS low_pct,
  ROUND(AVG(CASE WHEN is_low = 1 THEN "Freight Cost" END), 2) AS lm_avg_freight,
  ROUND(AVG(CASE WHEN is_low = 0 THEN "Freight Cost" END), 2) AS normal_avg_freight
FROM lm
GROUP BY region
ORDER BY low_pct DESC
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-005/attempt-01/sql/S20.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-005/attempt-01/sql/S20.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-005/attempt-01/results/S20.rows.jsonl)；完整：True；SHA256：`8fe1e27d8bfe52441e0e52234e79f63289e997633b9aeba6606372246f51b8ab`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "sheet1", "kind": "base", "block": null, "base_tables": ["sheet1"]}] | [] | [] |
| B2 | [{"alias": "sheet1", "kind": "base", "block": null, "base_tables": ["sheet1"]}] | [] | [] |
| B3 | [{"alias": "lm", "kind": "derived", "block": "B2", "base_tables": ["sheet1"]}] | [] | ["SUBSTRING(\"Destination\", 1, INSTR(\"Destination\", '-') - 1)"] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | AVG("Profit Margin") | [{"table": "sheet1", "column": "Profit Margin"}] | [] | False |
| B3 | SUM(CASE WHEN is_low = 1 THEN 1 ELSE 0 END) | [] | [{"table": "sheet1", "column": "Profit Margin"}, {"table": "sheet1", "column": "Profit Margin"}] | False |
| B3 | SUM(CASE WHEN is_low = 0 THEN 1 ELSE 0 END) | [] | [{"table": "sheet1", "column": "Profit Margin"}, {"table": "sheet1", "column": "Profit Margin"}] | False |
| B3 | AVG(CASE WHEN is_low = 1 THEN "Freight Cost" END) | [{"table": "sheet1", "column": "Freight Cost"}] | [{"table": "sheet1", "column": "Profit Margin"}, {"table": "sheet1", "column": "Profit Margin"}] | False |
| B3 | AVG(CASE WHEN is_low = 0 THEN "Freight Cost" END) | [{"table": "sheet1", "column": "Freight Cost"}] | [{"table": "sheet1", "column": "Profit Margin"}, {"table": "sheet1", "column": "Profit Margin"}] | False |
| B3 | COUNT(*) | [] | [] | True |
| B3 | SUM(CASE WHEN is_low = 1 THEN 1 ELSE 0 END) | [] | [{"table": "sheet1", "column": "Profit Margin"}, {"table": "sheet1", "column": "Profit Margin"}] | False |


## S21

类别 `data`；来源 `query_db`；调用 `c4e11ca6fa4b49f7b5c4908dedc3d8d1`；状态 `success`。

```sql
WITH lm AS (
  SELECT *, CASE WHEN "Profit Margin" < 0.5 * (SELECT AVG("Profit Margin") FROM sheet1) THEN 1 ELSE 0 END AS is_low
  FROM sheet1
)
SELECT 
  is_low,
  ROUND(AVG("Freight Cost" / NULLIF("Sales Quantity",0)), 3) AS freight_per_unit,
  ROUND(AVG("Warehousing Cost" / NULLIF("Sales Quantity",0)), 3) AS warehousing_per_unit,
  ROUND(AVG("Other Operating Costs" / NULLIF("Sales Quantity",0)), 3) AS other_per_unit,
  ROUND(AVG("Total Logistics Cost" / NULLIF("Sales Quantity",0)), 3) AS total_cost_per_unit,
  ROUND(AVG("Total Logistics Revenue" / NULLIF("Sales Quantity",0)), 3) AS rev_per_unit,
  ROUND(AVG("Logistics Unit Price"), 3) AS unit_price
FROM lm
GROUP BY is_low
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-005/attempt-01/sql/S21.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-005/attempt-01/sql/S21.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-005/attempt-01/results/S21.rows.jsonl)；完整：True；SHA256：`9cc4df6cc0f7433dbaf25fe0188f47b6a7ed76350cd4930a6bae19abe740ae6d`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "sheet1", "kind": "base", "block": null, "base_tables": ["sheet1"]}] | [] | [] |
| B2 | [{"alias": "sheet1", "kind": "base", "block": null, "base_tables": ["sheet1"]}] | [] | [] |
| B3 | [{"alias": "lm", "kind": "derived", "block": "B2", "base_tables": ["sheet1"]}] | [] | ["is_low"] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | AVG("Profit Margin") | [{"table": "sheet1", "column": "Profit Margin"}] | [] | False |
| B3 | AVG("Freight Cost" / NULLIF("Sales Quantity", 0)) | [{"table": "sheet1", "column": "Freight Cost"}, {"table": "sheet1", "column": "Sales Quantity"}] | [] | False |
| B3 | AVG("Warehousing Cost" / NULLIF("Sales Quantity", 0)) | [{"table": "sheet1", "column": "Warehousing Cost"}, {"table": "sheet1", "column": "Sales Quantity"}] | [] | False |
| B3 | AVG("Other Operating Costs" / NULLIF("Sales Quantity", 0)) | [{"table": "sheet1", "column": "Other Operating Costs"}, {"table": "sheet1", "column": "Sales Quantity"}] | [] | False |
| B3 | AVG("Total Logistics Cost" / NULLIF("Sales Quantity", 0)) | [{"table": "sheet1", "column": "Total Logistics Cost"}, {"table": "sheet1", "column": "Sales Quantity"}] | [] | False |
| B3 | AVG("Total Logistics Revenue" / NULLIF("Sales Quantity", 0)) | [{"table": "sheet1", "column": "Total Logistics Revenue"}, {"table": "sheet1", "column": "Sales Quantity"}] | [] | False |
| B3 | AVG("Logistics Unit Price") | [{"table": "sheet1", "column": "Logistics Unit Price"}] | [] | False |


## S22

类别 `data`；来源 `query_db`；调用 `5269c288e1dd4470abb75a8f0b310b25`；状态 `success`。

```sql
WITH lm AS (
  SELECT *, CASE WHEN "Profit Margin" < 0.5 * (SELECT AVG("Profit Margin") FROM sheet1) THEN 1 ELSE 0 END AS is_low
  FROM sheet1
)
SELECT 
  ROUND(AVG("Freight Cost"), 2) AS lm_freight,
  ROUND(AVG("Warehousing Cost"), 2) AS lm_warehousing,
  ROUND(AVG("Other Operating Costs"), 2) AS lm_other,
  ROUND(AVG("Logistics Unit Price"), 2) AS lm_unit_price,
  ROUND(AVG("Logistics Value-Added Service Revenue"), 2) AS lm_vas
FROM lm
WHERE is_low = 1
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-005/attempt-01/sql/S22.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-005/attempt-01/sql/S22.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-005/attempt-01/results/S22.rows.jsonl)；完整：True；SHA256：`b152c62c6734e5356b81d0cfb29248f40f8905b274cc46a19e61e8489f9d43c0`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "sheet1", "kind": "base", "block": null, "base_tables": ["sheet1"]}] | [] | [] |
| B2 | [{"alias": "sheet1", "kind": "base", "block": null, "base_tables": ["sheet1"]}] | [] | [] |
| B3 | [{"alias": "lm", "kind": "derived", "block": "B2", "base_tables": ["sheet1"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | AVG("Profit Margin") | [{"table": "sheet1", "column": "Profit Margin"}] | [] | False |
| B3 | AVG("Freight Cost") | [{"table": "sheet1", "column": "Freight Cost"}] | [] | False |
| B3 | AVG("Warehousing Cost") | [{"table": "sheet1", "column": "Warehousing Cost"}] | [] | False |
| B3 | AVG("Other Operating Costs") | [{"table": "sheet1", "column": "Other Operating Costs"}] | [] | False |
| B3 | AVG("Logistics Unit Price") | [{"table": "sheet1", "column": "Logistics Unit Price"}] | [] | False |
| B3 | AVG("Logistics Value-Added Service Revenue") | [{"table": "sheet1", "column": "Logistics Value-Added Service Revenue"}] | [] | False |


## S23

类别 `data`；来源 `query_db`；调用 `9f7b78e290ea4802bc8c83bab176a336`；状态 `success`。

```sql
WITH lm AS (
  SELECT *, CASE WHEN "Profit Margin" < 0.5 * (SELECT AVG("Profit Margin") FROM sheet1) THEN 1 ELSE 0 END AS is_low
  FROM sheet1
)
SELECT 
  "Logistics Unit Price",
  is_low,
  COUNT(*) AS n,
  ROUND(AVG("Total Logistics Revenue"), 2) AS avg_rev,
  ROUND(AVG("Freight Cost"), 2) AS avg_freight,
  ROUND(AVG("Discount Amount" / NULLIF("List Price Revenue",0) * 100), 2) AS avg_disc
FROM lm
GROUP BY "Logistics Unit Price", is_low
ORDER BY "Logistics Unit Price", is_low
LIMIT 40
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-005/attempt-01/sql/S23.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-005/attempt-01/sql/S23.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-005/attempt-01/results/S23.rows.jsonl)；完整：True；SHA256：`1c7c16cd5868f65f2e84bb3031e53ef093dca637684db207cb81aadb3224f19c`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "sheet1", "kind": "base", "block": null, "base_tables": ["sheet1"]}] | [] | [] |
| B2 | [{"alias": "sheet1", "kind": "base", "block": null, "base_tables": ["sheet1"]}] | [] | [] |
| B3 | [{"alias": "lm", "kind": "derived", "block": "B2", "base_tables": ["sheet1"]}] | [] | ["\"Logistics Unit Price\"", "is_low"] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | AVG("Profit Margin") | [{"table": "sheet1", "column": "Profit Margin"}] | [] | False |
| B3 | COUNT(*) | [] | [] | True |
| B3 | AVG("Total Logistics Revenue") | [{"table": "sheet1", "column": "Total Logistics Revenue"}] | [] | False |
| B3 | AVG("Freight Cost") | [{"table": "sheet1", "column": "Freight Cost"}] | [] | False |
| B3 | AVG("Discount Amount" / NULLIF("List Price Revenue", 0) * 100) | [{"table": "sheet1", "column": "Discount Amount"}, {"table": "sheet1", "column": "List Price Revenue"}] | [] | False |


## S24

类别 `data`；来源 `query_db`；调用 `1a9e4db2fc8a49c8916417d76a04a47d`；状态 `success`。

```sql
WITH lm AS (
  SELECT *, CASE WHEN "Profit Margin" < 0.5 * (SELECT AVG("Profit Margin") FROM sheet1) THEN 1 ELSE 0 END AS is_low
  FROM sheet1
)
SELECT 
  ROUND("Freight Cost", -1) AS freight_bucket,
  is_low,
  COUNT(*) AS n,
  ROUND(AVG("Sales Quantity"), 2) AS avg_qty,
  ROUND(AVG("Total Logistics Revenue"), 2) AS avg_rev,
  ROUND(AVG("Profit"), 2) AS avg_profit
FROM lm
GROUP BY freight_bucket, is_low
ORDER BY freight_bucket, is_low
LIMIT 30
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-005/attempt-01/sql/S24.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-005/attempt-01/sql/S24.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-005/attempt-01/results/S24.rows.jsonl)；完整：True；SHA256：`a4cfa17783f668797cb3735a1e31094784d0dd40929072850c1928107cb5d62d`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "sheet1", "kind": "base", "block": null, "base_tables": ["sheet1"]}] | [] | [] |
| B2 | [{"alias": "sheet1", "kind": "base", "block": null, "base_tables": ["sheet1"]}] | [] | [] |
| B3 | [{"alias": "lm", "kind": "derived", "block": "B2", "base_tables": ["sheet1"]}] | [] | ["ROUND(\"Freight Cost\", -1)", "is_low"] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | AVG("Profit Margin") | [{"table": "sheet1", "column": "Profit Margin"}] | [] | False |
| B3 | COUNT(*) | [] | [] | True |
| B3 | AVG("Sales Quantity") | [{"table": "sheet1", "column": "Sales Quantity"}] | [] | False |
| B3 | AVG("Total Logistics Revenue") | [{"table": "sheet1", "column": "Total Logistics Revenue"}] | [] | False |
| B3 | AVG("Profit") | [{"table": "sheet1", "column": "Profit"}] | [] | False |


## S25

类别 `data`；来源 `query_db`；调用 `ccadd7fe20b0488bb1002eee7eb9f2d8`；状态 `success`。

```sql
SELECT 
  "Date",
  "Sales Quantity",
  "Total Logistics Revenue",
  "Freight Cost",
  "Warehousing Cost",
  "Other Operating Costs",
  "Total Logistics Cost",
  "Discount Amount",
  "Profit",
  "Profit Margin",
  "Destination",
  "Consigned Product"
FROM sheet1 
WHERE "Profit Margin" < 0.5 * (SELECT AVG("Profit Margin") FROM sheet1)
ORDER BY "Profit Margin" ASC
LIMIT 10
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-005/attempt-01/sql/S25.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-005/attempt-01/sql/S25.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-005/attempt-01/results/S25.rows.jsonl)；完整：True；SHA256：`212be66388a49dd954c43822ea09021e6229a3c291d8ffce9e2ecab1a35244c4`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "sheet1", "kind": "base", "block": null, "base_tables": ["sheet1"]}] | [] | [] |
| B2 | [{"alias": "sheet1", "kind": "base", "block": null, "base_tables": ["sheet1"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | AVG("Profit Margin") | [{"table": "sheet1", "column": "Profit Margin"}] | [] | False |


## S26

类别 `data`；来源 `query_db`；调用 `a752be8fdf3f46ae8a05e99b13d896be`；状态 `success`。

```sql
WITH lm AS (
  SELECT *, CASE WHEN "Profit Margin" < 0.5 * (SELECT AVG("Profit Margin") FROM sheet1) THEN 1 ELSE 0 END AS is_low
  FROM sheet1
)
SELECT 
  is_low,
  ROUND(AVG("Discount Amount" / NULLIF("List Price Revenue", 0) * 100), 2) AS avg_discount_rate,
  ROUND(AVG("List Price Revenue"), 2) AS avg_list_price,
  ROUND(AVG("Total Logistics Revenue"), 2) AS avg_logistics_rev,
  ROUND(AVG("List Price Revenue" - "Total Logistics Revenue"), 2) AS avg_revenue_leakage,
  ROUND(100.0 * AVG("List Price Revenue" - "Total Logistics Revenue") / NULLIF(AVG("List Price Revenue"), 0), 2) AS pct_revenue_leakage
FROM lm
GROUP BY is_low
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-005/attempt-01/sql/S26.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-005/attempt-01/sql/S26.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-005/attempt-01/results/S26.rows.jsonl)；完整：True；SHA256：`229aaab51713f17491dca01910df797281ea2f354738c7b500368eab4826f99b`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "sheet1", "kind": "base", "block": null, "base_tables": ["sheet1"]}] | [] | [] |
| B2 | [{"alias": "sheet1", "kind": "base", "block": null, "base_tables": ["sheet1"]}] | [] | [] |
| B3 | [{"alias": "lm", "kind": "derived", "block": "B2", "base_tables": ["sheet1"]}] | [] | ["is_low"] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | AVG("Profit Margin") | [{"table": "sheet1", "column": "Profit Margin"}] | [] | False |
| B3 | AVG("Discount Amount" / NULLIF("List Price Revenue", 0) * 100) | [{"table": "sheet1", "column": "Discount Amount"}, {"table": "sheet1", "column": "List Price Revenue"}] | [] | False |
| B3 | AVG("List Price Revenue") | [{"table": "sheet1", "column": "List Price Revenue"}] | [] | False |
| B3 | AVG("Total Logistics Revenue") | [{"table": "sheet1", "column": "Total Logistics Revenue"}] | [] | False |
| B3 | AVG("List Price Revenue" - "Total Logistics Revenue") | [{"table": "sheet1", "column": "List Price Revenue"}, {"table": "sheet1", "column": "Total Logistics Revenue"}] | [] | False |
| B3 | AVG("List Price Revenue" - "Total Logistics Revenue") | [{"table": "sheet1", "column": "List Price Revenue"}, {"table": "sheet1", "column": "Total Logistics Revenue"}] | [] | False |
| B3 | AVG("List Price Revenue") | [{"table": "sheet1", "column": "List Price Revenue"}] | [] | False |


## S27

类别 `data`；来源 `query_db`；调用 `1051fe56afa9424cbf7d3b069d39c698`；状态 `success`。

```sql
WITH lm AS (
  SELECT *, CASE WHEN "Profit Margin" < 0.5 * (SELECT AVG("Profit Margin") FROM sheet1) THEN 1 ELSE 0 END AS is_low
  FROM sheet1
)
SELECT 
  SUBSTR("Destination", 1, INSTR("Destination", '-') - 1) AS region,
  SUBSTR("Destination", INSTR("Destination", '-') + 1, INSTR(SUBSTR("Destination", INSTR("Destination", '-') + 1), '-') - 1) AS province,
  is_low,
  COUNT(*) AS n,
  ROUND(AVG("Freight Cost"), 2) AS avg_freight,
  ROUND(AVG("Sales Quantity"), 2) AS avg_qty,
  ROUND(AVG("Freight Cost" / NULLIF("Sales Quantity", 0)), 2) AS freight_per_unit
FROM lm
WHERE is_low = 1
GROUP BY region, province
ORDER BY avg_freight DESC
LIMIT 15
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-005/attempt-01/sql/S27.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-005/attempt-01/sql/S27.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-005/attempt-01/results/S27.rows.jsonl)；完整：True；SHA256：`e484cf8fd65ef5a71d9e5931f890b49443dadfbcec8a2d1e4f99a2a284be5086`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "sheet1", "kind": "base", "block": null, "base_tables": ["sheet1"]}] | [] | [] |
| B2 | [{"alias": "sheet1", "kind": "base", "block": null, "base_tables": ["sheet1"]}] | [] | [] |
| B3 | [{"alias": "lm", "kind": "derived", "block": "B2", "base_tables": ["sheet1"]}] | [] | ["SUBSTRING(\"Destination\", 1, INSTR(\"Destination\", '-') - 1)", "SUBSTRING(\"Destination\", INSTR(\"Destination\", '-') + 1, INSTR(SUBSTRING(\"Destination\", INSTR(\"Destination\", '-') + 1), '-') - 1)"] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | AVG("Profit Margin") | [{"table": "sheet1", "column": "Profit Margin"}] | [] | False |
| B3 | COUNT(*) | [] | [] | True |
| B3 | AVG("Freight Cost") | [{"table": "sheet1", "column": "Freight Cost"}] | [] | False |
| B3 | AVG("Sales Quantity") | [{"table": "sheet1", "column": "Sales Quantity"}] | [] | False |
| B3 | AVG("Freight Cost" / NULLIF("Sales Quantity", 0)) | [{"table": "sheet1", "column": "Freight Cost"}, {"table": "sheet1", "column": "Sales Quantity"}] | [] | False |


## S28

类别 `data`；来源 `query_db`；调用 `3ab4878350d04f1689a88be3a45fbcea`；状态 `success`。

```sql
WITH lm AS (
  SELECT *, CASE WHEN "Profit Margin" < 0.5 * (SELECT AVG("Profit Margin") FROM sheet1) THEN 1 ELSE 0 END AS is_low
  FROM sheet1
)
SELECT 
  CASE 
    WHEN "Discount Amount" = 0 THEN '0%'
    WHEN "Discount Amount" / NULLIF("List Price Revenue", 0) < 0.05 THEN '0-5%'
    WHEN "Discount Amount" / NULLIF("List Price Revenue", 0) < 0.10 THEN '5-10%'
    WHEN "Discount Amount" / NULLIF("List Price Revenue", 0) < 0.20 THEN '10-20%'
    WHEN "Discount Amount" / NULLIF("List Price Revenue", 0) < 0.30 THEN '20-30%'
    ELSE '30%+'
  END AS discount_band,
  COUNT(*) AS total,
  SUM(CASE WHEN is_low = 1 THEN 1 ELSE 0 END) AS low_cnt,
  ROUND(100.0 * SUM(CASE WHEN is_low = 1 THEN 1 ELSE 0 END) / NULLIF(COUNT(*), 0), 2) AS low_pct_in_band,
  ROUND(100.0 * SUM(CASE WHEN is_low = 1 THEN 1 ELSE 0 END) / 1243, 2) AS pct_of_all_low
FROM lm
GROUP BY discount_band
ORDER BY discount_band
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-005/attempt-01/sql/S28.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-005/attempt-01/sql/S28.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-005/attempt-01/results/S28.rows.jsonl)；完整：True；SHA256：`9ca9ee27ffc0b07eea0b3dd76e1ac5df2081cf9b3b35075da5d03292b2aafd03`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "sheet1", "kind": "base", "block": null, "base_tables": ["sheet1"]}] | [] | [] |
| B2 | [{"alias": "sheet1", "kind": "base", "block": null, "base_tables": ["sheet1"]}] | [] | [] |
| B3 | [{"alias": "lm", "kind": "derived", "block": "B2", "base_tables": ["sheet1"]}] | [] | ["CASE WHEN \"Discount Amount\" = 0 THEN '0%' WHEN \"Discount Amount\" / NULLIF(\"List Price Revenue\", 0) < 0.05 THEN '0-5%' WHEN \"Discount Amount\" / NULLIF(\"List Price Revenue\", 0) < 0.10 THEN '5-10%' WHEN \"Discount Amount\" / NULLIF(\"List Price Revenue\", 0) < 0.20 THEN '10-20%' WHEN \"Discount Amount\" / NULLIF(\"List Price Revenue\", 0) < 0.30 THEN '20-30%' ELSE '30%+' END"] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | AVG("Profit Margin") | [{"table": "sheet1", "column": "Profit Margin"}] | [] | False |
| B3 | COUNT(*) | [] | [] | True |
| B3 | SUM(CASE WHEN is_low = 1 THEN 1 ELSE 0 END) | [] | [{"table": "sheet1", "column": "Profit Margin"}, {"table": "sheet1", "column": "Profit Margin"}] | False |
| B3 | SUM(CASE WHEN is_low = 1 THEN 1 ELSE 0 END) | [] | [{"table": "sheet1", "column": "Profit Margin"}, {"table": "sheet1", "column": "Profit Margin"}] | False |
| B3 | COUNT(*) | [] | [] | True |
| B3 | SUM(CASE WHEN is_low = 1 THEN 1 ELSE 0 END) | [] | [{"table": "sheet1", "column": "Profit Margin"}, {"table": "sheet1", "column": "Profit Margin"}] | False |


## S29

类别 `data`；来源 `query_db`；调用 `3c5c3a65255a407d82b2bf054a436f04`；状态 `success`。

```sql
WITH lm AS (
  SELECT *, CASE WHEN "Profit Margin" < 0.5 * (SELECT AVG("Profit Margin") FROM sheet1) THEN 1 ELSE 0 END AS is_low
  FROM sheet1
)
SELECT 
  "Logistics Value-Added Service Revenue",
  is_low,
  COUNT(*) AS n,
  ROUND(AVG("Total Logistics Revenue"), 2) AS avg_rev,
  ROUND(AVG("Profit"), 2) AS avg_profit
FROM lm
GROUP BY "Logistics Value-Added Service Revenue", is_low
ORDER BY "Logistics Value-Added Service Revenue", is_low
LIMIT 30
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-005/attempt-01/sql/S29.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-005/attempt-01/sql/S29.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-005/attempt-01/results/S29.rows.jsonl)；完整：True；SHA256：`8ad114537480c67426c74ed13b2419b05bffb3c2b1d83f6c16284e0b8f0ae8c6`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "sheet1", "kind": "base", "block": null, "base_tables": ["sheet1"]}] | [] | [] |
| B2 | [{"alias": "sheet1", "kind": "base", "block": null, "base_tables": ["sheet1"]}] | [] | [] |
| B3 | [{"alias": "lm", "kind": "derived", "block": "B2", "base_tables": ["sheet1"]}] | [] | ["\"Logistics Value-Added Service Revenue\"", "is_low"] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | AVG("Profit Margin") | [{"table": "sheet1", "column": "Profit Margin"}] | [] | False |
| B3 | COUNT(*) | [] | [] | True |
| B3 | AVG("Total Logistics Revenue") | [{"table": "sheet1", "column": "Total Logistics Revenue"}] | [] | False |
| B3 | AVG("Profit") | [{"table": "sheet1", "column": "Profit"}] | [] | False |


## S30

类别 `data`；来源 `query_db`；调用 `9b58d64fabe54eb0bbc7b5438da06043`；状态 `success`。

```sql
WITH lm AS (
  SELECT *, CASE WHEN "Profit Margin" < 0.5 * (SELECT AVG("Profit Margin") FROM sheet1) THEN 1 ELSE 0 END AS is_low
  FROM sheet1
)
SELECT 
  is_low,
  ROUND(AVG("Logistics Value-Added Service Revenue"), 2) AS avg_vas,
  ROUND(AVG("Logistics Value-Added Service Revenue") / NULLIF(AVG("Total Logistics Revenue"), 0) * 100, 2) AS vas_pct_of_rev,
  COUNT(CASE WHEN "Logistics Value-Added Service Revenue" > 0 THEN 1 END) AS vas_orders,
  ROUND(100.0 * COUNT(CASE WHEN "Logistics Value-Added Service Revenue" > 0 THEN 1 END) / COUNT(*), 2) AS pct_vas_orders
FROM lm
GROUP BY is_low
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-005/attempt-01/sql/S30.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-005/attempt-01/sql/S30.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-005/attempt-01/results/S30.rows.jsonl)；完整：True；SHA256：`f7c45350742c739af830e8db2898faf94b1e2cbb9498bf1c6e1f4e36bc1c63bd`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "sheet1", "kind": "base", "block": null, "base_tables": ["sheet1"]}] | [] | [] |
| B2 | [{"alias": "sheet1", "kind": "base", "block": null, "base_tables": ["sheet1"]}] | [] | [] |
| B3 | [{"alias": "lm", "kind": "derived", "block": "B2", "base_tables": ["sheet1"]}] | [] | ["is_low"] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | AVG("Profit Margin") | [{"table": "sheet1", "column": "Profit Margin"}] | [] | False |
| B3 | COUNT(CASE WHEN "Logistics Value-Added Service Revenue" > 0 THEN 1 END) | [] | [{"table": "sheet1", "column": "Logistics Value-Added Service Revenue"}] | False |
| B3 | AVG("Logistics Value-Added Service Revenue") | [{"table": "sheet1", "column": "Logistics Value-Added Service Revenue"}] | [] | False |
| B3 | COUNT(*) | [] | [] | True |
| B3 | AVG("Logistics Value-Added Service Revenue") | [{"table": "sheet1", "column": "Logistics Value-Added Service Revenue"}] | [] | False |
| B3 | COUNT(CASE WHEN "Logistics Value-Added Service Revenue" > 0 THEN 1 END) | [] | [{"table": "sheet1", "column": "Logistics Value-Added Service Revenue"}] | False |
| B3 | AVG("Total Logistics Revenue") | [{"table": "sheet1", "column": "Total Logistics Revenue"}] | [] | False |


## S31

类别 `data`；来源 `query_db`；调用 `72bb2071c4044fc092eb6718bc67c2fc`；状态 `success`。

```sql
WITH lm AS (
  SELECT *, CASE WHEN "Profit Margin" < 0.5 * (SELECT AVG("Profit Margin") FROM sheet1) THEN 1 ELSE 0 END AS is_low
  FROM sheet1
)
SELECT 
  "Consigned Product",
  ROUND(AVG(CASE WHEN is_low = 1 THEN "Freight Cost" / NULLIF("Sales Quantity", 0) END), 2) AS lm_freight_per_unit,
  ROUND(AVG(CASE WHEN is_low = 0 THEN "Freight Cost" / NULLIF("Sales Quantity", 0) END), 2) AS normal_freight_per_unit,
  ROUND(AVG(CASE WHEN is_low = 1 THEN "Total Logistics Cost" / NULLIF("Sales Quantity", 0) END), 2) AS lm_cost_per_unit,
  ROUND(AVG(CASE WHEN is_low = 0 THEN "Total Logistics Cost" / NULLIF("Sales Quantity", 0) END), 2) AS normal_cost_per_unit,
  ROUND(AVG(CASE WHEN is_low = 1 THEN "Total Logistics Revenue" / NULLIF("Sales Quantity", 0) END), 2) AS lm_rev_per_unit,
  ROUND(AVG(CASE WHEN is_low = 0 THEN "Total Logistics Revenue" / NULLIF("Sales Quantity", 0) END), 2) AS normal_rev_per_unit
FROM lm
GROUP BY "Consigned Product"
ORDER BY lm_cost_per_unit DESC
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-005/attempt-01/sql/S31.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-005/attempt-01/sql/S31.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-005/attempt-01/results/S31.rows.jsonl)；完整：True；SHA256：`896cd094d901058384561500f8bc1a4c3d5ec3b3b9f8a451103b082aa5cad2fb`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "sheet1", "kind": "base", "block": null, "base_tables": ["sheet1"]}] | [] | [] |
| B2 | [{"alias": "sheet1", "kind": "base", "block": null, "base_tables": ["sheet1"]}] | [] | [] |
| B3 | [{"alias": "lm", "kind": "derived", "block": "B2", "base_tables": ["sheet1"]}] | [] | ["\"Consigned Product\""] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | AVG("Profit Margin") | [{"table": "sheet1", "column": "Profit Margin"}] | [] | False |
| B3 | AVG(CASE WHEN is_low = 1 THEN "Freight Cost" / NULLIF("Sales Quantity", 0) END) | [{"table": "sheet1", "column": "Freight Cost"}, {"table": "sheet1", "column": "Sales Quantity"}] | [{"table": "sheet1", "column": "Profit Margin"}, {"table": "sheet1", "column": "Profit Margin"}] | False |
| B3 | AVG(CASE WHEN is_low = 0 THEN "Freight Cost" / NULLIF("Sales Quantity", 0) END) | [{"table": "sheet1", "column": "Freight Cost"}, {"table": "sheet1", "column": "Sales Quantity"}] | [{"table": "sheet1", "column": "Profit Margin"}, {"table": "sheet1", "column": "Profit Margin"}] | False |
| B3 | AVG(CASE WHEN is_low = 1 THEN "Total Logistics Cost" / NULLIF("Sales Quantity", 0) END) | [{"table": "sheet1", "column": "Total Logistics Cost"}, {"table": "sheet1", "column": "Sales Quantity"}] | [{"table": "sheet1", "column": "Profit Margin"}, {"table": "sheet1", "column": "Profit Margin"}] | False |
| B3 | AVG(CASE WHEN is_low = 0 THEN "Total Logistics Cost" / NULLIF("Sales Quantity", 0) END) | [{"table": "sheet1", "column": "Total Logistics Cost"}, {"table": "sheet1", "column": "Sales Quantity"}] | [{"table": "sheet1", "column": "Profit Margin"}, {"table": "sheet1", "column": "Profit Margin"}] | False |
| B3 | AVG(CASE WHEN is_low = 1 THEN "Total Logistics Revenue" / NULLIF("Sales Quantity", 0) END) | [{"table": "sheet1", "column": "Total Logistics Revenue"}, {"table": "sheet1", "column": "Sales Quantity"}] | [{"table": "sheet1", "column": "Profit Margin"}, {"table": "sheet1", "column": "Profit Margin"}] | False |
| B3 | AVG(CASE WHEN is_low = 0 THEN "Total Logistics Revenue" / NULLIF("Sales Quantity", 0) END) | [{"table": "sheet1", "column": "Total Logistics Revenue"}, {"table": "sheet1", "column": "Sales Quantity"}] | [{"table": "sheet1", "column": "Profit Margin"}, {"table": "sheet1", "column": "Profit Margin"}] | False |


## S32

类别 `data`；来源 `python`；调用 `69c70f70f0184c208152e8405180c93d`；状态 `success`。

```sql

  SELECT *, CASE WHEN "Profit Margin" < 0.5 * (SELECT AVG("Profit Margin") FROM sheet1) THEN 'Low-Margin' ELSE 'Normal' END AS order_type
  FROM sheet1

```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-005/attempt-01/sql/S32.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-005/attempt-01/sql/S32.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-005/attempt-01/results/S32.rows.jsonl)；完整：True；SHA256：`752f91d328e6ca988ecdf0187db1d648d19f5c352b047008e76004d71cabc7ec`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "sheet1", "kind": "base", "block": null, "base_tables": ["sheet1"]}] | [] | [] |
| B2 | [{"alias": "sheet1", "kind": "base", "block": null, "base_tables": ["sheet1"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | AVG("Profit Margin") | [{"table": "sheet1", "column": "Profit Margin"}] | [] | False |


## S33

类别 `data`；来源 `python`；调用 `5009d9e070484578b833a6898a9e467d`；状态 `success`。

```sql

  SELECT *, CASE WHEN "Profit Margin" < 0.5 * (SELECT AVG("Profit Margin") FROM sheet1) THEN 'Low-Margin' ELSE 'Normal' END AS order_type
  FROM sheet1

```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-005/attempt-01/sql/S33.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-005/attempt-01/sql/S33.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-005/attempt-01/results/S33.rows.jsonl)；完整：True；SHA256：`752f91d328e6ca988ecdf0187db1d648d19f5c352b047008e76004d71cabc7ec`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "sheet1", "kind": "base", "block": null, "base_tables": ["sheet1"]}] | [] | [] |
| B2 | [{"alias": "sheet1", "kind": "base", "block": null, "base_tables": ["sheet1"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | AVG("Profit Margin") | [{"table": "sheet1", "column": "Profit Margin"}] | [] | False |


## S34

类别 `data`；来源 `python`；调用 `1d457e75824142d4ae48f7d74f22a566`；状态 `success`。

```sql

  SELECT *, CASE WHEN "Profit Margin" < 0.5 * (SELECT AVG("Profit Margin") FROM sheet1) THEN 1 ELSE 0 END AS is_low
  FROM sheet1

```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-005/attempt-01/sql/S34.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-005/attempt-01/sql/S34.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-005/attempt-01/results/S34.rows.jsonl)；完整：True；SHA256：`7e88f90bb2267267e1791746970fc780e1c53427195ee9e0b9faffc95f5fe852`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "sheet1", "kind": "base", "block": null, "base_tables": ["sheet1"]}] | [] | [] |
| B2 | [{"alias": "sheet1", "kind": "base", "block": null, "base_tables": ["sheet1"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | AVG("Profit Margin") | [{"table": "sheet1", "column": "Profit Margin"}] | [] | False |


## S35

类别 `data`；来源 `query_db`；调用 `9628e1b1b3cb4e4ea7d526144aa51c36`；状态 `success`。

```sql
WITH lm AS (
  SELECT *, CASE WHEN "Profit Margin" < 0.5 * (SELECT AVG("Profit Margin") FROM sheet1) THEN 1 ELSE 0 END AS is_low
  FROM sheet1
  WHERE "Profit Margin" < 0.5 * (SELECT AVG("Profit Margin") FROM sheet1)
)
SELECT 
  "Sales Quantity",
  COUNT(*) AS n,
  ROUND(AVG("Discount Amount" / NULLIF("List Price Revenue",0) * 100), 2) AS avg_disc_rate,
  ROUND(AVG("Total Logistics Revenue"), 2) AS avg_rev,
  ROUND(AVG("Total Logistics Cost"), 2) AS avg_cost,
  ROUND(AVG("Freight Cost"), 2) AS avg_freight,
  ROUND(AVG("Warehousing Cost"), 2) AS avg_wh,
  ROUND(AVG("Profit"), 2) AS avg_profit,
  ROUND(SUM("Profit"), 2) AS total_profit
FROM lm
GROUP BY "Sales Quantity"
ORDER BY "Sales Quantity"
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-005/attempt-01/sql/S35.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-005/attempt-01/sql/S35.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-005/attempt-01/results/S35.rows.jsonl)；完整：True；SHA256：`1f8a420a1c9c138fabff9ee1b30907a60b31eaf5ef517623821f08b37d47c5f2`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "sheet1", "kind": "base", "block": null, "base_tables": ["sheet1"]}] | [] | [] |
| B2 | [{"alias": "sheet1", "kind": "base", "block": null, "base_tables": ["sheet1"]}] | [] | [] |
| B3 | [{"alias": "sheet1", "kind": "base", "block": null, "base_tables": ["sheet1"]}] | [] | [] |
| B4 | [{"alias": "lm", "kind": "derived", "block": "B3", "base_tables": ["sheet1"]}] | [] | ["\"Sales Quantity\""] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | AVG("Profit Margin") | [{"table": "sheet1", "column": "Profit Margin"}] | [] | False |
| B2 | AVG("Profit Margin") | [{"table": "sheet1", "column": "Profit Margin"}] | [] | False |
| B4 | COUNT(*) | [] | [] | True |
| B4 | AVG("Discount Amount" / NULLIF("List Price Revenue", 0) * 100) | [{"table": "sheet1", "column": "Discount Amount"}, {"table": "sheet1", "column": "List Price Revenue"}] | [] | False |
| B4 | AVG("Total Logistics Revenue") | [{"table": "sheet1", "column": "Total Logistics Revenue"}] | [] | False |
| B4 | AVG("Total Logistics Cost") | [{"table": "sheet1", "column": "Total Logistics Cost"}] | [] | False |
| B4 | AVG("Freight Cost") | [{"table": "sheet1", "column": "Freight Cost"}] | [] | False |
| B4 | AVG("Warehousing Cost") | [{"table": "sheet1", "column": "Warehousing Cost"}] | [] | False |
| B4 | AVG("Profit") | [{"table": "sheet1", "column": "Profit"}] | [] | False |
| B4 | SUM("Profit") | [{"table": "sheet1", "column": "Profit"}] | [] | False |


## S36

类别 `data`；来源 `query_db`；调用 `5135c9bed5754e28ba72d81514873e68`；状态 `success`。

```sql
WITH lm AS (
  SELECT *, CASE WHEN "Profit Margin" < 0.5 * (SELECT AVG("Profit Margin") FROM sheet1) THEN 1 ELSE 0 END AS is_low
  FROM sheet1
  WHERE "Profit Margin" < 0.5 * (SELECT AVG("Profit Margin") FROM sheet1)
)
SELECT 
  "Destination",
  COUNT(*) AS n,
  ROUND(AVG("Freight Cost" / NULLIF("Sales Quantity",0)), 2) AS avg_freight_per_unit,
  ROUND(AVG("Total Logistics Cost" / NULLIF("Sales Quantity",0)), 2) AS avg_cost_per_unit,
  ROUND(AVG("Total Logistics Revenue" / NULLIF("Sales Quantity",0)), 2) AS avg_rev_per_unit,
  ROUND(SUM("Profit"), 2) AS total_profit_loss
FROM lm
GROUP BY "Destination"
ORDER BY total_profit_loss ASC
LIMIT 10
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-005/attempt-01/sql/S36.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-005/attempt-01/sql/S36.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-005/attempt-01/results/S36.rows.jsonl)；完整：True；SHA256：`5167cca0ff9d400708f40817810dbf2e006110b87e8a14546540a740e1ac693d`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "sheet1", "kind": "base", "block": null, "base_tables": ["sheet1"]}] | [] | [] |
| B2 | [{"alias": "sheet1", "kind": "base", "block": null, "base_tables": ["sheet1"]}] | [] | [] |
| B3 | [{"alias": "sheet1", "kind": "base", "block": null, "base_tables": ["sheet1"]}] | [] | [] |
| B4 | [{"alias": "lm", "kind": "derived", "block": "B3", "base_tables": ["sheet1"]}] | [] | ["\"Destination\""] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | AVG("Profit Margin") | [{"table": "sheet1", "column": "Profit Margin"}] | [] | False |
| B2 | AVG("Profit Margin") | [{"table": "sheet1", "column": "Profit Margin"}] | [] | False |
| B4 | COUNT(*) | [] | [] | True |
| B4 | AVG("Freight Cost" / NULLIF("Sales Quantity", 0)) | [{"table": "sheet1", "column": "Freight Cost"}, {"table": "sheet1", "column": "Sales Quantity"}] | [] | False |
| B4 | AVG("Total Logistics Cost" / NULLIF("Sales Quantity", 0)) | [{"table": "sheet1", "column": "Total Logistics Cost"}, {"table": "sheet1", "column": "Sales Quantity"}] | [] | False |
| B4 | AVG("Total Logistics Revenue" / NULLIF("Sales Quantity", 0)) | [{"table": "sheet1", "column": "Total Logistics Revenue"}, {"table": "sheet1", "column": "Sales Quantity"}] | [] | False |
| B4 | SUM("Profit") | [{"table": "sheet1", "column": "Profit"}] | [] | False |


## S37

类别 `data`；来源 `query_db`；调用 `b7b37ef0a0d3417fb2b1c18704cc1195`；状态 `success`。

```sql
WITH lm AS (
  SELECT *, CASE WHEN "Profit Margin" < 0.5 * (SELECT AVG("Profit Margin") FROM sheet1) THEN 1 ELSE 0 END AS is_low
  FROM sheet1
  WHERE "Profit Margin" < 0.5 * (SELECT AVG("Profit Margin") FROM sheet1)
)
SELECT 
  "Consigned Product",
  "Sales Quantity",
  COUNT(*) AS n,
  ROUND(AVG("Discount Amount" / NULLIF("List Price Revenue",0) * 100), 2) AS avg_disc_rate,
  ROUND(AVG("Total Logistics Cost" / NULLIF("Sales Quantity",0)), 2) AS avg_cost_per_unit,
  ROUND(AVG("Total Logistics Revenue" / NULLIF("Sales Quantity",0)), 2) AS avg_rev_per_unit,
  ROUND(AVG("Profit"), 2) AS avg_profit
FROM lm
GROUP BY "Consigned Product", "Sales Quantity"
HAVING n >= 5
ORDER BY "Consigned Product", "Sales Quantity"
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-005/attempt-01/sql/S37.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-005/attempt-01/sql/S37.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-005/attempt-01/results/S37.rows.jsonl)；完整：True；SHA256：`d64ec7e1866060c217202fc041c939dcf7af4c56c55b69f85eb560809862ba0e`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "sheet1", "kind": "base", "block": null, "base_tables": ["sheet1"]}] | [] | [] |
| B2 | [{"alias": "sheet1", "kind": "base", "block": null, "base_tables": ["sheet1"]}] | [] | [] |
| B3 | [{"alias": "sheet1", "kind": "base", "block": null, "base_tables": ["sheet1"]}] | [] | [] |
| B4 | [{"alias": "lm", "kind": "derived", "block": "B3", "base_tables": ["sheet1"]}] | [] | ["\"Consigned Product\"", "\"Sales Quantity\""] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | AVG("Profit Margin") | [{"table": "sheet1", "column": "Profit Margin"}] | [] | False |
| B2 | AVG("Profit Margin") | [{"table": "sheet1", "column": "Profit Margin"}] | [] | False |
| B4 | COUNT(*) | [] | [] | True |
| B4 | AVG("Discount Amount" / NULLIF("List Price Revenue", 0) * 100) | [{"table": "sheet1", "column": "Discount Amount"}, {"table": "sheet1", "column": "List Price Revenue"}] | [] | False |
| B4 | AVG("Total Logistics Cost" / NULLIF("Sales Quantity", 0)) | [{"table": "sheet1", "column": "Total Logistics Cost"}, {"table": "sheet1", "column": "Sales Quantity"}] | [] | False |
| B4 | AVG("Total Logistics Revenue" / NULLIF("Sales Quantity", 0)) | [{"table": "sheet1", "column": "Total Logistics Revenue"}, {"table": "sheet1", "column": "Sales Quantity"}] | [] | False |
| B4 | AVG("Profit") | [{"table": "sheet1", "column": "Profit"}] | [] | False |


## S38

类别 `data`；来源 `python`；调用 `9b006be533d54ab28f5535c90371b067`；状态 `success`。

```sql

  SELECT *, CASE WHEN "Profit Margin" < 0.5 * (SELECT AVG("Profit Margin") FROM sheet1) THEN 1 ELSE 0 END AS is_low
  FROM sheet1

```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-005/attempt-01/sql/S38.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-005/attempt-01/sql/S38.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-005/attempt-01/results/S38.rows.jsonl)；完整：True；SHA256：`7e88f90bb2267267e1791746970fc780e1c53427195ee9e0b9faffc95f5fe852`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "sheet1", "kind": "base", "block": null, "base_tables": ["sheet1"]}] | [] | [] |
| B2 | [{"alias": "sheet1", "kind": "base", "block": null, "base_tables": ["sheet1"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | AVG("Profit Margin") | [{"table": "sheet1", "column": "Profit Margin"}] | [] | False |

