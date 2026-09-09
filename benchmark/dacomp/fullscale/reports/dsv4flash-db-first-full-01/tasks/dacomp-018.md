# dacomp-018

I am a merchant in the Fashion category. Based on the e-commerce platform data provided to…

运行：已提交。官方未评分。全部 SQL 尝试/成功 58/57；数据 SQL 56/55；Python 5 次。

完整原题：

I am a merchant in the Fashion category. Based on the e-commerce platform data provided to you, please analyze which user profile I should focus on to operate the Fashion category well on this platform and achieve relatively good profit.

| 表 | 行数 | 列数 |
| --- | --- | --- |
| customer_information | 51289 | 11 |
| order_information | 51289 | 13 |
| product_browsing | 51289 | 7 |


实际路线（分析者依据 SQL/源码概括，不代表 Agent 自述）：按服装品类检查订单与客户资料 → SQL 汇总客户利润并连接浏览行为 → 按性别、客群和商品比较利润 → Python 检验互动关联、计算利润分位和群体摘要 → 绘制月度及商品偏好图。

数据库大小：28,389,376 字节。

## 数据 SQL

| SQL | 状态 | 基础表 | Join 输入/类型 | GROUP BY | 聚合表达式 | 结果行数 | 数据库 ms |
| --- | --- | --- | --- | --- | --- | --- | --- |
| [S3/Q1](#s3) | success | ["order_information"] | 0 / {} | [] | ["COUNT(*)", "COUNT(DISTINCT \"Customer ID\")", "COUNT(DISTINCT \"Product Category\")"] | 1 | 24.373 |
| [S4/Q2](#s4) | success | ["order_information"] | 0 / {} | ["\"Product Category\""] | ["COUNT(*)", "COUNT(DISTINCT \"Customer ID\")", "SUM(Sales)", "SUM(profit)", "AVG(profit)"] | 4 | 46.08 |
| [S5/Q3](#s5) | success | ["customer_information"] | 0 / {} | [] | ["COUNT(*)"] | 1 | 2.022 |
| [S6/Q4](#s6) | success | ["product_browsing"] | 0 / {} | [] | ["COUNT(*)"] | 1 | 1.222 |
| [S7/Q5](#s7) | success | ["customer_information"] | 0 / {} | [] | [] | 5 | 0.373 |
| [S8/Q6](#s8) | success | ["order_information"] | 0 / {} | [] | [] | 5 | 2.459 |
| [S9/Q7](#s9) | success | ["product_browsing"] | 0 / {} | [] | [] | 5 | 1.827 |
| [S10/Q8](#s10) | success | ["customer_information", "order_information"] | 2 / {'INNER': 1} | ["c.\"Customer Segment\""] | ["COUNT(o.\"Order ID\")", "COUNT(DISTINCT o.\"Customer ID\")", "SUM(o.Sales)", "SUM(o.profit)", "AVG(o.profit)", "SUM(o.profit)", "COUNT(DISTINCT o.\"Customer ID\")"] | 3 | 1864.017 |
| [S11/Q9](#s11) | success | ["customer_information", "order_information"] | 2 / {'INNER': 1} | ["c.gender"] | ["COUNT(o.\"Order ID\")", "COUNT(DISTINCT o.\"Customer ID\")", "SUM(o.profit)", "AVG(o.profit)", "SUM(o.profit)", "COUNT(DISTINCT o.\"Customer ID\")"] | 2 | 1770.388 |
| [S12/Q10](#s12) | success | ["order_information"] | 0 / {} | [] | ["COUNT(*)", "COUNT(DISTINCT \"Customer ID\")"] | 1 | 15.167 |
| [S13/Q11](#s13) | success | ["customer_information"] | 0 / {} | [] | ["COUNT(*)"] | 1 | 2.042 |
| [S14/Q12](#s14) | success | ["customer_information"] | 0 / {} | [] | ["COUNT(DISTINCT \"Customer ID\")"] | 1 | 19.16 |
| [S15/Q13](#s15) | success | ["customer_information"] | 0 / {} | ["\"Customer ID\""] | ["COUNT(*)"] | 10 | 22.847 |
| [S16/Q14](#s16) | success | ["customer_information"] | 0 / {} | ["\"Customer Segment\""] | ["COUNT(*)"] | 3 | 20.833 |
| [S17/Q15](#s17) | success | ["customer_information"] | 0 / {} | ["\"Customer ID\""] | ["COUNT(DISTINCT \"Customer Segment\")", "COUNT(*)"] | 1 | 30.389 |
| [S18/Q16](#s18) | success | ["customer_information"] | 0 / {} | ["\"Customer ID\""] | ["COUNT(DISTINCT gender)", "COUNT(*)"] | 1 | 26.062 |
| [S19/Q17](#s19) | success | ["customer_information", "order_information"] | 2 / {'INNER': 1} | ["\"Customer ID\"", "\"Customer ID\"", "c.\"Customer Segment\""] | ["COUNT(*)", "COUNT(DISTINCT \"Order ID\")", "SUM(Sales)", "SUM(profit)", "SUM(CASE WHEN NOT Discount IS NULL AND CAST(Discount AS REAL) > 0 THEN 1 ELSE 0 END)", "COUNT(*)", "SUM(co.orders)", "SUM(co.sales)", "SUM(co.profit)", "AVG(co.profit / co.orders)", "SUM(co.profit)", "COUNT(*)", "SUM(co.orders)", "COUNT(*)"] | 3 | 75.396 |
| [S20/Q18](#s20) | success | ["customer_information", "order_information"] | 2 / {'INNER': 1} | ["\"Customer ID\"", "\"Customer ID\"", "c.gender"] | ["COUNT(*)", "SUM(Sales)", "SUM(profit)", "COUNT(*)", "SUM(co.orders)", "SUM(co.sales)", "SUM(co.profit)", "AVG(co.profit / co.orders)", "SUM(co.profit)", "COUNT(*)", "SUM(co.orders)", "COUNT(*)"] | 2 | 64.426 |
| [S21/Q19](#s21) | success | ["customer_information", "order_information"] | 2 / {'INNER': 1} | ["\"Customer ID\"", "\"Customer ID\"", "b.age_group"] | ["COUNT(*)", "SUM(Sales)", "SUM(profit)", "COUNT(*)", "SUM(co.orders)", "SUM(co.profit)", "AVG(co.profit / co.orders)", "SUM(co.profit)", "COUNT(*)", "SUM(co.orders)", "COUNT(*)"] | 6 | 63.937 |
| [S22/Q20](#s22) | success | ["customer_information", "order_information"] | 2 / {'INNER': 1} | ["\"Customer ID\"", "\"Customer ID\"", "c.\"Education Level\""] | ["COUNT(*)", "SUM(Sales)", "SUM(profit)", "COUNT(*)", "SUM(co.orders)", "SUM(co.profit)", "AVG(co.profit / co.orders)", "SUM(co.profit)", "COUNT(*)", "SUM(co.orders)", "COUNT(*)"] | 5 | 63.953 |
| [S23/Q21](#s23) | success | ["customer_information", "order_information"] | 2 / {'INNER': 1} | ["\"Customer ID\"", "\"Customer ID\"", "c.\"Marital Status\""] | ["COUNT(*)", "SUM(Sales)", "SUM(profit)", "COUNT(*)", "SUM(co.orders)", "SUM(co.profit)", "AVG(co.profit / co.orders)", "SUM(co.profit)", "COUNT(*)", "SUM(co.orders)", "COUNT(*)"] | 2 | 64.035 |
| [S24/Q22](#s24) | success | ["customer_information", "order_information"] | 2 / {'INNER': 1} | ["\"Customer ID\"", "\"Customer ID\"", "c.Region"] | ["COUNT(*)", "SUM(Sales)", "SUM(profit)", "COUNT(*)", "SUM(co.orders)", "SUM(co.profit)", "SUM(co.profit)", "COUNT(*)", "SUM(co.orders)", "COUNT(*)"] | 15 | 64.307 |
| [S25/Q23](#s25) | success | ["customer_information", "order_information"] | 2 / {'INNER': 1} | ["\"Customer ID\"", "\"Customer ID\"", "c.Country"] | ["COUNT(*)", "SUM(Sales)", "SUM(profit)", "COUNT(*)", "SUM(co.orders)", "SUM(co.profit)", "SUM(co.profit)", "COUNT(*)"] | 84 | 54.112 |
| [S26/Q24](#s26) | success | ["order_information"] | 0 / {} | ["\"Product\""] | ["COUNT(*)", "SUM(Sales)", "SUM(profit)", "AVG(profit)"] | 11 | 19.175 |
| [S27/Q25](#s27) | success | ["customer_information", "order_information"] | 2 / {'INNER': 1} | ["\"Customer ID\"", "\"Customer ID\"", "c.gender", "c.\"Customer Segment\""] | ["COUNT(*)", "SUM(Sales)", "SUM(profit)", "COUNT(*)", "SUM(co.orders)", "SUM(co.profit)", "SUM(co.profit)", "COUNT(*)", "SUM(co.orders)", "COUNT(*)"] | 6 | 56.561 |
| [S28/Q26](#s28) | success | ["customer_information", "order_information"] | 2 / {'INNER': 1} | ["\"Customer ID\"", "\"Customer ID\"", "c.gender", "CASE WHEN c.age < 35 THEN 'under35' ELSE '35plus' END"] | ["COUNT(*)", "SUM(Sales)", "SUM(profit)", "COUNT(*)", "SUM(co.profit)", "SUM(co.profit)", "COUNT(*)", "SUM(co.orders)", "COUNT(*)"] | 4 | 53.478 |
| [S29/Q27](#s29) | success | unknown | None / None | [] | [] | 10 | 22.415 |
| [S30/Q28](#s30) | success | ["product_browsing"] | 0 / {} | [] | ["COUNT(*)", "COUNT(DISTINCT \"Customer ID\")"] | 1 | 13.487 |
| [S31/Q29](#s31) | success | unknown | None / None | [] | [] | 11 | 18.27 |
| [S32/Q30](#s32) | success | unknown | None / None | [] | [] | 6 | 79.351 |
| [S33/Q31](#s33) | success | unknown | None / None | [] | [] | 2 | 41.777 |
| [S34/Q32](#s34) | success | ["customer_information", "order_information"] | 2 / {'INNER': 1} | ["\"Customer ID\"", "\"Customer ID\"", "gender", "\"Customer Segment\""] | ["COUNT(*)", "SUM(profit)", "SUM(Sales)", "COUNT(*)", "SUM(profit)", "SUM(profit)", "COUNT(*)"] | 6 | 65.537 |
| [S35/Q33](#s35) | success | ["order_information"] | 0 / {} | ["\"Customer ID\""] | ["COUNT(*)", "SUM(profit)", "SUM(Sales)", "SUM(profit)", "COUNT(*)", "SUM(profit)", "SUM(profit)"] | 1 | 22.463 |
| [S36/Q34](#s36) | success | ["order_information"] | 0 / {} | ["\"Customer ID\"", "quintile"] | ["COUNT(*)", "SUM(profit)", "SUM(profit)", "COUNT(*)", "SUM(profit)", "SUM(profit)"] | 5 | 19.852 |
| [S37/Q35](#s37) | success | ["customer_information", "order_information"] | 2 / {'INNER': 1} | ["\"Customer ID\"", "\"Customer ID\"", "c.gender"] | ["SUM(profit)", "SUM(profit)", "COUNT(*)", "SUM(co.profit)", "SUM(co.profit)", "COUNT(*)", "COUNT(*)", "SUM(co.profit)"] | 2 | 50.672 |
| [S38/Q36](#s38) | success | ["customer_information", "order_information"] | 2 / {'INNER': 1} | ["\"Customer ID\"", "\"Customer ID\"", "o.\"Product\"", "c.gender"] | ["SUM(profit)", "SUM(Sales)", "COUNT(*)", "COUNT(*)", "SUM(o.profit)", "SUM(o.profit)", "COUNT(*)"] | 22 | 67.308 |
| [S39/Q37](#s39) | failed | ["customer_information", "order_information"] | 2 / {'INNER': 1} | ["\"Customer ID\"", "c.gender", "EXTRACT(YEAR FROM o.\"Order Date\")", "month"] | ["COUNT(*)", "SUM(o.profit)"] | unknown | 未取得；调用总时长 0.229 ms |
| [S40/Q38](#s40) | success | ["customer_information", "order_information"] | 2 / {'INNER': 1} | ["c.gender", "o.\"Shipping Method\""] | ["AVG(CAST(o.Discount AS REAL))", "AVG(CAST(o.\"Shipping Cost\" AS REAL))", "COUNT(*)", "COUNT(*)", "SUM(CASE WHEN CAST(o.Discount AS REAL) > 0 THEN 1 ELSE 0 END)"] | 2 | 2202.096 |
| [S41/Q39](#s41) | success | ["order_information"] | 0 / {} | [] | [] | 4 | 5.881 |
| [S42/Q40](#s42) | success | ["customer_information", "order_information"] | 2 / {'INNER': 1} | ["\"Customer ID\"", "c.gender", "o.\"Shipping Method\""] | ["COUNT(*)", "SUM(o.profit)"] | 2 | 60.207 |
| [S43/Q41](#s43) | success | ["customer_information", "order_information"] | 2 / {'INNER': 1} | ["\"Customer ID\"", "c.gender", "STRFTIME('%Y', o.\"Order Date\")", "month"] | ["COUNT(*)", "SUM(o.profit)"] | 72 | 83.25 |
| [S44/Q42](#s44) | success | ["order_information"] | 0 / {} | [] | [] | 36 | 25.47 |
| [S45/Q43](#s45) | success | ["customer_information", "order_information"] | 2 / {'INNER': 1} | ["\"Customer ID\"", "c.gender", "STRFTIME('%Y-%m', o.\"Order Date\")"] | ["COUNT(*)", "SUM(o.profit)"] | 72 | 78.331 |
| [S46/Q44](#s46) | success | ["customer_information", "order_information"] | 2 / {'INNER': 1} | ["\"Customer ID\"", "\"Customer ID\"", "c.gender", "c.\"Customer Segment\"", "c.Region"] | ["COUNT(*)", "SUM(profit)", "SUM(Sales)", "COUNT(*)", "SUM(co.profit)", "SUM(co.profit)", "COUNT(*)"] | 20 | 58.915 |
| [S47/Q45](#s47) | success | ["order_information"] | 0 / {} | ["\"Customer ID\"", "CASE WHEN orders <= 20 THEN '1-20' WHEN orders <= 40 THEN '21-40' WHEN orders <= 60 THEN '41-60' ELSE '60+' END"] | ["COUNT(*)", "SUM(profit)", "SUM(Sales)", "COUNT(*)", "SUM(profit)", "SUM(profit)", "COUNT(*)"] | 4 | 21.612 |
| [S48/Q46](#s48) | success | unknown | None / None | [] | [] | 795 | 77.093 |
| [S49/Q47](#s49) | success | ["customer_information", "order_information"] | 2 / {'INNER': 1} | ["\"Customer ID\"", "c.gender", "STRFTIME('%Y-%m', o.\"Order Date\")"] | ["SUM(o.profit)", "COUNT(*)"] | 72 | 88.257 |
| [S50/Q48](#s50) | success | ["customer_information", "order_information"] | 2 / {'INNER': 1} | ["\"Customer ID\"", "o.\"Product\"", "c.gender"] | ["COUNT(*)", "SUM(o.profit)", "SUM(o.Sales)", "SUM(o.profit)", "COUNT(*)", "SUM(o.Sales)", "COUNT(*)"] | 22 | 66.288 |
| [S51/Q49](#s51) | success | ["customer_information", "order_information"] | 2 / {'INNER': 1} | ["\"Customer ID\"", "c.gender", "o.\"Order Priority\""] | ["COUNT(*)", "SUM(o.profit)", "SUM(o.profit)", "COUNT(*)"] | 6 | 64.216 |
| [S52/Q50](#s52) | success | ["customer_information", "order_information"] | 2 / {'INNER': 1} | ["\"Customer ID\"", "o.\"Product\"", "c.gender"] | ["COUNT(*)", "SUM(o.profit)"] | 22 | 64.747 |
| [S53/Q51](#s53) | success | ["customer_information", "order_information"] | 2 / {'INNER': 1} | ["\"Customer ID\"", "c.gender", "STRFTIME('%m', o.\"Order Date\")", "o.\"Month\""] | ["COUNT(*)", "SUM(o.profit)"] | 288 | 83.345 |
| [S54/Q52](#s54) | success | ["customer_information", "order_information"] | 2 / {'INNER': 1} | ["\"Customer ID\"", "c.gender", "discount"] | ["COUNT(*)", "SUM(o.profit)", "AVG(o.profit)"] | 10 | 72.887 |
| [S55/Q53](#s55) | success | ["customer_information", "order_information"] | 2 / {'INNER': 1} | ["\"Customer ID\"", "c.gender", "STRFTIME('%m', o.\"Order Date\")"] | ["SUM(o.profit)", "COUNT(*)"] | 24 | 78.134 |
| [S56/Q54](#s56) | success | ["customer_information", "order_information"] | 2 / {'INNER': 1} | ["\"Customer ID\"", "\"Customer ID\""] | ["SUM(profit)"] | 795 | 47.275 |
| [S57/Q55](#s57) | success | ["customer_information", "order_information"] | 2 / {'INNER': 1} | ["\"Customer ID\"", "c.gender", "discount"] | ["COUNT(*)", "SUM(o.profit)", "AVG(o.profit)", "SUM(o.Sales)"] | 10 | 67.809 |
| [S58/Q56](#s58) | success | ["customer_information", "order_information"] | 2 / {'INNER': 1} | ["\"Customer ID\"", "\"Customer ID\"", "c.gender", "c.\"Customer Segment\"", "c.Region", "c.\"Marital Status\""] | ["COUNT(*)", "SUM(profit)", "SUM(Sales)", "COUNT(*)", "SUM(co.orders)", "SUM(co.profit)", "SUM(co.profit)", "COUNT(*)", "SUM(co.orders)", "COUNT(*)"] | 15 | 59.605 |


## 元数据和设置

| SQL | 类别 | 状态 | 内容 |
| --- | --- | --- | --- |
| S1 | connection_setup | success | PRAGMA query_only=ON |
| S2 | metadata | success | SELECT name,sql FROM sqlite_master WHERE type='table' ORDER BY name |


## Python 与执行位置

人工源码审查：**partial_violation**。SQL prepares customer aggregates and joins; Python uses Pearson/Mann-Whitney tests and renders figures. P1/P2 also compute per-gender and gender-by-segment counts/means/sums, engagement ratios and profit-quintile summaries; P5 rolls up monthly totals. These SQL-capable operations are execution-location deviations. SQLGlot cannot parse the unquoted schema column like in five successful statements (S29/S31/S32/S33/S48); these remain explicit unknown structures, not zero counts, while original SQL and engine results are preserved. [证据](../reviews/dacomp-018.json)。

P1：Need to compute correlations and run statistical tests (Mann-Whitney U for engagement metrics between genders, Pearson correlation between browsing engagement and profit) which are not reasonably supported by SQLite, and produce visualizations for the report.

[源码](../../../runs/dsv4flash-db-first-full-01/dacomp-018/attempt-01/python/P1.py)；[输出](../../../runs/dsv4flash-db-first-full-01/dacomp-018/attempt-01/python/P1.stdout)；[错误](../../../runs/dsv4flash-db-first-full-01/dacomp-018/attempt-01/python/P1.stderr)。检出需人工核验的 SQL 可实现操作：groupby(, .query(；不能仅凭理由判为合规。

P2：Create summary visualizations from the aggregated customer-level dataset: profit by gender/segment, engagement rate comparison, and profit concentration - figures for the report.

[源码](../../../runs/dsv4flash-db-first-full-01/dacomp-018/attempt-01/python/P2.py)；[输出](../../../runs/dsv4flash-db-first-full-01/dacomp-018/attempt-01/python/P2.stdout)；[错误](../../../runs/dsv4flash-db-first-full-01/dacomp-018/attempt-01/python/P2.stderr)。检出需人工核验的 SQL 可实现操作：groupby(, .query(, sort_values(；不能仅凭理由判为合规。

P3：Create a detailed profile comparison of high-value customers (top 20% by profit) vs the rest, to identify distinguishing characteristics beyond SQL's simple aggregation capabilities.

[源码](../../../runs/dsv4flash-db-first-full-01/dacomp-018/attempt-01/python/P3.py)；[输出](../../../runs/dsv4flash-db-first-full-01/dacomp-018/attempt-01/python/P3.stdout)；[错误](../../../runs/dsv4flash-db-first-full-01/dacomp-018/attempt-01/python/P3.stderr)。自动源码筛查未检出预设迁出信号；这不是全面语义合规证明。

P4：Calculate product preference ratios by gender to identify which products have the highest female-to-male order ratio, helping understand merchandising strategy.

[源码](../../../runs/dsv4flash-db-first-full-01/dacomp-018/attempt-01/python/P4.py)；[输出](../../../runs/dsv4flash-db-first-full-01/dacomp-018/attempt-01/python/P4.stdout)；[错误](../../../runs/dsv4flash-db-first-full-01/dacomp-018/attempt-01/python/P4.stderr)。检出需人工核验的 SQL 可实现操作：.query(, sort_values(；不能仅凭理由判为合规。

P5：Create a seasonality analysis showing monthly profit patterns and identify peak months for Fashion category, using aggregated data from the database.

[源码](../../../runs/dsv4flash-db-first-full-01/dacomp-018/attempt-01/python/P5.py)；[输出](../../../runs/dsv4flash-db-first-full-01/dacomp-018/attempt-01/python/P5.stdout)；[错误](../../../runs/dsv4flash-db-first-full-01/dacomp-018/attempt-01/python/P5.stderr)。检出需人工核验的 SQL 可实现操作：groupby(, .query(, sort_values(；不能仅凭理由判为合规。

## 优化机会

已验证候选。筛选限于精确 SQL、相同自包含 CTE、相同单表完整过滤、可分解单表聚合；未覆盖任意 Join 等价和一般谓词蕴含。全部候选都是 offline，未测在线预测。

| 候选 | 类型 | 已有结果 | 覆盖 SQL | 后续次数 | 中间行数 | 验证 | 成本 |
| --- | --- | --- | --- | --- | --- | --- | --- |
| C1 | common subexpression | False | ["S19", "S20", "S21", "S22", "S23", "S24"] | 5 | 795 | verified | Not benchmarked; correctness alone does not establish net speedup. |
| C2 | common subexpression | False | ["S20", "S21", "S22", "S23", "S24", "S25", "S27", "S28"] | 7 | 795 | verified | Not benchmarked; correctness alone does not establish net speedup. |
| C3 | common subexpression | False | ["S34", "S35", "S46", "S47", "S58"] | 4 | unknown | not_verified_cap | Not tested |
| C4 | common subexpression | False | ["S37", "S38"] | 1 | unknown | not_verified_cap | Not tested |
| C5 | common subexpression | False | ["S37", "S56"] | 1 | unknown | not_verified_cap | Not tested |
| C6 | common subexpression | False | ["S42", "S43", "S45", "S49", "S50", "S51", "S52", "S53", "S54", "S55", "S57"] | 10 | 795 | verified | Not benchmarked; correctness alone does not establish net speedup. |
| C7 | aggregate MV | False | ["S5", "S13", "S15"] | 2 | unknown | not_verified_cap | Not tested |
| C8 | common filtered view | False | ["S8", "S12", "S26", "S44"] | 3 | unknown | not_verified_cap | Not tested |
| C9 | common filtered view | False | ["S9", "S30"] | 1 | unknown | not_verified_cap | Not tested |


已验证覆盖（含触发查询、候选并集去重）：20/55 条成功数据 SQL。正确性仅针对当前数据库快照；未测性能的候选不能声称已加速。

[完整 build/rewrite 与比较证据](dacomp-018.analysis.json)。

### C6：common subexpression

Identical self-contained CTE body across queries.

原查询 [S42](#s42), [S43](#s43), [S45](#s45), [S49](#s49), [S50](#s50), [S51](#s51), [S52](#s52), [S53](#s53), [S54](#s54), [S55](#s55), [S57](#s57) → 新增共享状态 C6 → 后续 10 次可复用。该构建点为事后假设，不代表 Agent 当时预知后续。

构建定义：

```sql
SELECT "Customer ID", gender FROM customer_information GROUP BY "Customer ID"
```

受益查询 S42 的改写示例：

```sql
WITH cust AS (SELECT * FROM temp.reuse_candidate) SELECT c.gender, o."Shipping Method", COUNT(*) AS orders, SUM(o.profit) AS profit FROM order_information AS o JOIN cust AS c ON o."Customer ID" = c."Customer ID" WHERE o."Product Category" = 'Fashion' GROUP BY c.gender, o."Shipping Method" ORDER BY c.gender, orders DESC
```

| 原 SQL | 列名一致 | 结果一致 | 比较方法 |
| --- | --- | --- | --- |
| S42 | True | True | ordered_numeric_tolerance |
| S43 | True | True | ordered_numeric_tolerance |
| S45 | True | True | ordered_numeric_tolerance |
| S49 | True | True | exact_multiset |
| S50 | True | True | ordered_numeric_tolerance |
| S51 | True | True | ordered_numeric_tolerance |
| S52 | True | True | exact_multiset |
| S53 | True | True | ordered_numeric_tolerance |
| S54 | True | True | ordered_numeric_tolerance |
| S55 | True | True | exact_multiset |
| S57 | True | True | ordered_numeric_tolerance |


验证状态：verified；成本结论：Not benchmarked; correctness alone does not establish net speedup.

### C2：common subexpression

Identical self-contained CTE body across queries.

原查询 [S20](#s20), [S21](#s21), [S22](#s22), [S23](#s23), [S24](#s24), [S25](#s25), [S27](#s27), [S28](#s28) → 新增共享状态 C2 → 后续 7 次可复用。该构建点为事后假设，不代表 Agent 当时预知后续。

构建定义：

```sql
SELECT "Customer ID", COUNT(*) AS orders, SUM(Sales) AS sales, SUM(profit) AS profit FROM order_information WHERE "Product Category" = 'Fashion' GROUP BY "Customer ID"
```

受益查询 S20 的改写示例：

```sql
WITH cust AS (SELECT "Customer ID", "Customer Segment", gender, age, "Education Level", "Marital Status", Region, Country, City FROM customer_information GROUP BY "Customer ID"), cust_orders AS (SELECT * FROM temp.reuse_candidate) SELECT c.gender, COUNT(*) AS customers, SUM(co.orders) AS fashion_orders, SUM(co.sales) AS sales, SUM(co.profit) AS profit, SUM(co.profit) / COUNT(*) AS profit_per_customer, SUM(co.orders) / COUNT(*) AS orders_per_customer, AVG(co.profit / co.orders) AS avg_profit_per_order FROM cust AS c JOIN cust_orders AS co ON c."Customer ID" = co."Customer ID" GROUP BY c.gender ORDER BY profit DESC
```

| 原 SQL | 列名一致 | 结果一致 | 比较方法 |
| --- | --- | --- | --- |
| S20 | True | True | ordered_numeric_tolerance |
| S21 | True | True | ordered_numeric_tolerance |
| S22 | True | True | ordered_numeric_tolerance |
| S23 | True | True | ordered_numeric_tolerance |
| S24 | True | True | ordered_numeric_tolerance |
| S25 | True | True | ordered_numeric_tolerance |
| S27 | True | True | ordered_numeric_tolerance |
| S28 | True | True | ordered_numeric_tolerance |


验证状态：verified；成本结论：Not benchmarked; correctness alone does not establish net speedup.

### C1：common subexpression

Identical self-contained CTE body across queries.

原查询 [S19](#s19), [S20](#s20), [S21](#s21), [S22](#s22), [S23](#s23), [S24](#s24) → 新增共享状态 C1 → 后续 5 次可复用。该构建点为事后假设，不代表 Agent 当时预知后续。

构建定义：

```sql
SELECT "Customer ID", "Customer Segment", gender, age, "Education Level", "Marital Status", Region, Country, City FROM customer_information GROUP BY "Customer ID"
```

受益查询 S19 的改写示例：

```sql
WITH cust AS (SELECT * FROM temp.reuse_candidate), cust_orders AS (SELECT "Customer ID", COUNT(*) AS orders, COUNT(DISTINCT "Order ID") AS order_ids, SUM(Sales) AS sales, SUM(profit) AS profit, SUM(CASE WHEN NOT Discount IS NULL AND CAST(Discount AS REAL) > 0 THEN 1 ELSE 0 END) AS discounted_orders FROM order_information WHERE "Product Category" = 'Fashion' GROUP BY "Customer ID") SELECT c."Customer Segment", COUNT(*) AS customers, SUM(co.orders) AS fashion_orders, SUM(co.sales) AS sales, SUM(co.profit) AS profit, SUM(co.profit) / COUNT(*) AS profit_per_customer, SUM(co.orders) / COUNT(*) AS orders_per_customer, AVG(co.profit / co.orders) AS avg_profit_per_order FROM cust AS c JOIN cust_orders AS co ON c."Customer ID" = co."Customer ID" GROUP BY c."Customer Segment" ORDER BY profit DESC
```

| 原 SQL | 列名一致 | 结果一致 | 比较方法 |
| --- | --- | --- | --- |
| S19 | True | True | ordered_numeric_tolerance |
| S20 | True | True | ordered_numeric_tolerance |
| S21 | True | True | ordered_numeric_tolerance |
| S22 | True | True | ordered_numeric_tolerance |
| S23 | True | True | ordered_numeric_tolerance |
| S24 | True | True | ordered_numeric_tolerance |


验证状态：verified；成本结论：Not benchmarked; correctness alone does not establish net speedup.

结果依赖：自动记录 SQL→Python 的接口父调用，以及源码中引用归档文件的消费者；字面值相同不认定因果。模型方向选择需要人工读取消息，尚未做全面因果标注。

[原始报告](../../../runs/dsv4flash-db-first-full-01/dacomp-018/attempt-01/answer.md)；[统一消息](../../../runs/dsv4flash-db-first-full-01/dacomp-018/attempt-01/messages.jsonl)；[原始 OpenCode 事件](../../../runs/dsv4flash-db-first-full-01/dacomp-018/attempt-01/opencode.jsonl)；[SQL 引擎日志](../../../runs/dsv4flash-db-first-full-01/dacomp-018/attempt-01/sql_journal.jsonl)。

[可读报告（本地图片链接规范化）](../answers/dacomp-018.md)。原始回答保留，分析结论未改写。

## S1

类别 `connection_setup`；来源 `connection`；调用 `12a0a575a619441090495be0c8d5fd2a`；状态 `success`。

```sql
PRAGMA query_only=ON
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-018/attempt-01/sql/S1.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-018/attempt-01/sql/S1.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-018/attempt-01/results/S1.rows.jsonl)；完整：True；SHA256：`e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`。

## S2

类别 `metadata`；来源 `list_db`；调用 `12a0a575a619441090495be0c8d5fd2a`；状态 `success`。

```sql
SELECT name,sql FROM sqlite_master WHERE type='table' ORDER BY name
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-018/attempt-01/sql/S2.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-018/attempt-01/sql/S2.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-018/attempt-01/results/S2.rows.jsonl)；完整：True；SHA256：`65468faae86d39a48f884b13bd510f5ebed47a911d291b1e25fa15a19f7da006`。

## S3

类别 `data`；来源 `query_db`；调用 `d1e7d8d21bb642ef92e3856a940b6304`；状态 `success`。

```sql
SELECT COUNT(*) AS total_orders, COUNT(DISTINCT "Customer ID") AS customers, COUNT(DISTINCT "Product Category") AS categories FROM order_information
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-018/attempt-01/sql/S3.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-018/attempt-01/sql/S3.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-018/attempt-01/results/S3.rows.jsonl)；完整：True；SHA256：`54044b4ea20bdec575f78a3f5fe725a0d85a135117ad57b294c885451dbcf0fe`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "order_information", "kind": "base", "block": null, "base_tables": ["order_information"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |
| B1 | COUNT(DISTINCT "Customer ID") | [{"table": "order_information", "column": "Customer ID"}] | [] | False |
| B1 | COUNT(DISTINCT "Product Category") | [{"table": "order_information", "column": "Product Category"}] | [] | False |


## S4

类别 `data`；来源 `query_db`；调用 `ee92519dbf75444898639c19761f907a`；状态 `success`。

```sql
SELECT "Product Category", COUNT(*) AS orders, COUNT(DISTINCT "Customer ID") AS customers, SUM(Sales) AS total_sales, SUM(profit) AS total_profit, AVG(profit) AS avg_profit_per_order FROM order_information GROUP BY "Product Category" ORDER BY total_profit DESC
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-018/attempt-01/sql/S4.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-018/attempt-01/sql/S4.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-018/attempt-01/results/S4.rows.jsonl)；完整：True；SHA256：`409576df46fb02d17e1a5a0c501932b9510d7d00e70fd5fac19f0682b488dfcf`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "order_information", "kind": "base", "block": null, "base_tables": ["order_information"]}] | [] | ["\"Product Category\""] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |
| B1 | COUNT(DISTINCT "Customer ID") | [{"table": "order_information", "column": "Customer ID"}] | [] | False |
| B1 | SUM(Sales) | [{"table": "order_information", "column": "Sales"}] | [] | False |
| B1 | SUM(profit) | [{"table": "order_information", "column": "profit"}] | [] | False |
| B1 | AVG(profit) | [{"table": "order_information", "column": "profit"}] | [] | False |


## S5

类别 `data`；来源 `query_db`；调用 `46d5d51e602445baa88b4cd1e238e802`；状态 `success`。

```sql
SELECT COUNT(*) AS total_customers FROM customer_information
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-018/attempt-01/sql/S5.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-018/attempt-01/sql/S5.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-018/attempt-01/results/S5.rows.jsonl)；完整：True；SHA256：`eb6e48656c821597ccb27738e3c2488ee9df4a315c5100bfa7cd031a317aef4e`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "customer_information", "kind": "base", "block": null, "base_tables": ["customer_information"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |


## S6

类别 `data`；来源 `query_db`；调用 `d1640b9130ab41ae9832a4b3f04370bc`；状态 `success`。

```sql
SELECT COUNT(*) AS total_browsing FROM product_browsing
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-018/attempt-01/sql/S6.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-018/attempt-01/sql/S6.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-018/attempt-01/results/S6.rows.jsonl)；完整：True；SHA256：`eb6e48656c821597ccb27738e3c2488ee9df4a315c5100bfa7cd031a317aef4e`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "product_browsing", "kind": "base", "block": null, "base_tables": ["product_browsing"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |


## S7

类别 `data`；来源 `query_db`；调用 `845a0fce40474a69a2b5bd27dffc860c`；状态 `success`。

```sql
SELECT * FROM customer_information LIMIT 5
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-018/attempt-01/sql/S7.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-018/attempt-01/sql/S7.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-018/attempt-01/results/S7.rows.jsonl)；完整：True；SHA256：`5dd9d8c28dee03606a5c8fa6688ec26092bbf929020ad4574435ffc37b41cdba`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "customer_information", "kind": "base", "block": null, "base_tables": ["customer_information"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |


## S8

类别 `data`；来源 `query_db`；调用 `b65cb8a197944445976eb12c6115d472`；状态 `success`。

```sql
SELECT * FROM order_information WHERE "Product Category" = 'Fashion' LIMIT 5
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-018/attempt-01/sql/S8.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-018/attempt-01/sql/S8.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-018/attempt-01/results/S8.rows.jsonl)；完整：True；SHA256：`053ffd1724142e491c6b3646e4ea571391ed8e871a95ba7ff5de10b571a5e197`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "order_information", "kind": "base", "block": null, "base_tables": ["order_information"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |


## S9

类别 `data`；来源 `query_db`；调用 `8a60405f8c7c49c0b516a2ae45a4cbe0`；状态 `success`。

```sql
SELECT * FROM product_browsing WHERE "Product Category" = 'Fashion' LIMIT 5
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-018/attempt-01/sql/S9.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-018/attempt-01/sql/S9.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-018/attempt-01/results/S9.rows.jsonl)；完整：True；SHA256：`bcd76b4630402184451ce59a5e6bf63a5d94ad49b0afe3122d7d4a0e8a46e502`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "product_browsing", "kind": "base", "block": null, "base_tables": ["product_browsing"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |


## S10

类别 `data`；来源 `query_db`；调用 `23e5ae1a88c14cf4a3a78cc2b71cd61d`；状态 `success`。

```sql
SELECT c."Customer Segment", COUNT(o."Order ID") AS orders, COUNT(DISTINCT o."Customer ID") AS customers, SUM(o.Sales) AS sales, SUM(o.profit) AS profit, AVG(o.profit) AS avg_profit, SUM(o.profit)/COUNT(DISTINCT o."Customer ID") AS profit_per_customer
FROM order_information o JOIN customer_information c ON o."Customer ID" = c."Customer ID"
WHERE o."Product Category" = 'Fashion'
GROUP BY c."Customer Segment" ORDER BY profit DESC
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-018/attempt-01/sql/S10.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-018/attempt-01/sql/S10.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-018/attempt-01/results/S10.rows.jsonl)；完整：True；SHA256：`3e2157297a8b75781dfd30b133707d2c596f6e54a69fd7fe5a7edc1482eb2227`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "o", "kind": "base", "block": null, "base_tables": ["order_information"]}, {"alias": "c", "kind": "base", "block": null, "base_tables": ["customer_information"]}] | [{"type": "INNER", "right": "customer_information AS c", "on": "o.\"Customer ID\" = c.\"Customer ID\"", "using": []}] | ["c.\"Customer Segment\""] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(o."Order ID") | [{"table": "order_information", "column": "Order ID"}] | [] | False |
| B1 | COUNT(DISTINCT o."Customer ID") | [{"table": "order_information", "column": "Customer ID"}] | [] | False |
| B1 | SUM(o.Sales) | [{"table": "order_information", "column": "Sales"}] | [] | False |
| B1 | SUM(o.profit) | [{"table": "order_information", "column": "profit"}] | [] | False |
| B1 | AVG(o.profit) | [{"table": "order_information", "column": "profit"}] | [] | False |
| B1 | SUM(o.profit) | [{"table": "order_information", "column": "profit"}] | [] | False |
| B1 | COUNT(DISTINCT o."Customer ID") | [{"table": "order_information", "column": "Customer ID"}] | [] | False |


## S11

类别 `data`；来源 `query_db`；调用 `bf8869ab71be47ba8c20b31d1a81301f`；状态 `success`。

```sql
SELECT c.gender, COUNT(o."Order ID") AS orders, COUNT(DISTINCT o."Customer ID") AS customers, SUM(o.profit) AS profit, AVG(o.profit) AS avg_profit, SUM(o.profit)/COUNT(DISTINCT o."Customer ID") AS profit_per_customer
FROM order_information o JOIN customer_information c ON o."Customer ID" = c."Customer ID"
WHERE o."Product Category" = 'Fashion'
GROUP BY c.gender ORDER BY profit DESC
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-018/attempt-01/sql/S11.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-018/attempt-01/sql/S11.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-018/attempt-01/results/S11.rows.jsonl)；完整：True；SHA256：`5c726a8b3adc565a1e1e15ca2c2f3d9bdf0bcacc3141507ed50796a60f32e5ee`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "o", "kind": "base", "block": null, "base_tables": ["order_information"]}, {"alias": "c", "kind": "base", "block": null, "base_tables": ["customer_information"]}] | [{"type": "INNER", "right": "customer_information AS c", "on": "o.\"Customer ID\" = c.\"Customer ID\"", "using": []}] | ["c.gender"] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(o."Order ID") | [{"table": "order_information", "column": "Order ID"}] | [] | False |
| B1 | COUNT(DISTINCT o."Customer ID") | [{"table": "order_information", "column": "Customer ID"}] | [] | False |
| B1 | SUM(o.profit) | [{"table": "order_information", "column": "profit"}] | [] | False |
| B1 | AVG(o.profit) | [{"table": "order_information", "column": "profit"}] | [] | False |
| B1 | SUM(o.profit) | [{"table": "order_information", "column": "profit"}] | [] | False |
| B1 | COUNT(DISTINCT o."Customer ID") | [{"table": "order_information", "column": "Customer ID"}] | [] | False |


## S12

类别 `data`；来源 `query_db`；调用 `06432188da1441d985b52a61834b71d9`；状态 `success`。

```sql
SELECT COUNT(*) AS total_fashion_customers, COUNT(DISTINCT "Customer ID") AS distinct_fashion_customers FROM order_information WHERE "Product Category" = 'Fashion'
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-018/attempt-01/sql/S12.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-018/attempt-01/sql/S12.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-018/attempt-01/results/S12.rows.jsonl)；完整：True；SHA256：`81e6249e7f1c0dbd7f7b196fa140ec4b0502f4760114b20c9162f22451710849`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "order_information", "kind": "base", "block": null, "base_tables": ["order_information"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |
| B1 | COUNT(DISTINCT "Customer ID") | [{"table": "order_information", "column": "Customer ID"}] | [] | False |


## S13

类别 `data`；来源 `query_db`；调用 `df95db1aed4f405b86c8d117b139787f`；状态 `success`。

```sql
SELECT COUNT(*) FROM customer_information
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-018/attempt-01/sql/S13.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-018/attempt-01/sql/S13.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-018/attempt-01/results/S13.rows.jsonl)；完整：True；SHA256：`eb6e48656c821597ccb27738e3c2488ee9df4a315c5100bfa7cd031a317aef4e`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "customer_information", "kind": "base", "block": null, "base_tables": ["customer_information"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |


## S14

类别 `data`；来源 `query_db`；调用 `cb44524aef004103b1c53ff189dfb69a`；状态 `success`。

```sql
SELECT COUNT(DISTINCT "Customer ID") FROM customer_information
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-018/attempt-01/sql/S14.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-018/attempt-01/sql/S14.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-018/attempt-01/results/S14.rows.jsonl)；完整：True；SHA256：`0768546a91c4e2e567f996d2cfd5b214a713ed9225e533b75671f7878e75b9a8`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "customer_information", "kind": "base", "block": null, "base_tables": ["customer_information"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(DISTINCT "Customer ID") | [{"table": "customer_information", "column": "Customer ID"}] | [] | False |


## S15

类别 `data`；来源 `query_db`；调用 `c93bb9b360fa4990ba1a9374f2404620`；状态 `success`。

```sql
SELECT "Customer ID", COUNT(*) AS cnt FROM customer_information GROUP BY "Customer ID" ORDER BY cnt DESC LIMIT 10
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-018/attempt-01/sql/S15.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-018/attempt-01/sql/S15.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-018/attempt-01/results/S15.rows.jsonl)；完整：True；SHA256：`96eeac22d95110da001678c2c856476e1bf39c7bc8f7ccda5631ae4063f4cbef`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "customer_information", "kind": "base", "block": null, "base_tables": ["customer_information"]}] | [] | ["\"Customer ID\""] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |


## S16

类别 `data`；来源 `query_db`；调用 `8eb72d732fc249b5a638c490af52a322`；状态 `success`。

```sql
SELECT "Customer Segment", COUNT(*) FROM (SELECT DISTINCT "Customer ID", "Customer Segment" FROM customer_information) GROUP BY "Customer Segment"
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-018/attempt-01/sql/S16.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-018/attempt-01/sql/S16.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-018/attempt-01/results/S16.rows.jsonl)；完整：True；SHA256：`c1cdbb56754cea7fd2bdb19af87e077fe071ca9d9e66c5ba4a9bd70ac3f86663`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "customer_information", "kind": "base", "block": null, "base_tables": ["customer_information"]}] | [] | [] |
| B2 | [{"alias": "", "kind": "derived", "block": "B1", "base_tables": ["customer_information"]}] | [] | ["\"Customer Segment\""] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B2 | COUNT(*) | [] | [] | True |


## S17

类别 `data`；来源 `query_db`；调用 `7f2a89df8069443ba0375ecf9258f395`；状态 `success`。

```sql
SELECT COUNT(*) AS inconsistent_segments FROM (SELECT "Customer ID", COUNT(DISTINCT "Customer Segment") AS seg_cnt FROM customer_information GROUP BY "Customer ID" HAVING seg_cnt > 1)
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-018/attempt-01/sql/S17.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-018/attempt-01/sql/S17.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-018/attempt-01/results/S17.rows.jsonl)；完整：True；SHA256：`c14196f132c1e9be0508ae80ab52fcb3e1d3fc05880415f3dc980971df207c9e`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "customer_information", "kind": "base", "block": null, "base_tables": ["customer_information"]}] | [] | ["\"Customer ID\""] |
| B2 | [{"alias": "", "kind": "derived", "block": "B1", "base_tables": ["customer_information"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(DISTINCT "Customer Segment") | [{"table": "customer_information", "column": "Customer Segment"}] | [] | False |
| B2 | COUNT(*) | [] | [] | True |


## S18

类别 `data`；来源 `query_db`；调用 `8ff36519696a43bfa0070f26f1ac95bd`；状态 `success`。

```sql
SELECT COUNT(*) AS inconsistent_gender FROM (SELECT "Customer ID", COUNT(DISTINCT gender) AS g_cnt FROM customer_information GROUP BY "Customer ID" HAVING g_cnt > 1)
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-018/attempt-01/sql/S18.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-018/attempt-01/sql/S18.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-018/attempt-01/results/S18.rows.jsonl)；完整：True；SHA256：`c14196f132c1e9be0508ae80ab52fcb3e1d3fc05880415f3dc980971df207c9e`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "customer_information", "kind": "base", "block": null, "base_tables": ["customer_information"]}] | [] | ["\"Customer ID\""] |
| B2 | [{"alias": "", "kind": "derived", "block": "B1", "base_tables": ["customer_information"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(DISTINCT gender) | [{"table": "customer_information", "column": "gender"}] | [] | False |
| B2 | COUNT(*) | [] | [] | True |


## S19

类别 `data`；来源 `query_db`；调用 `000b18b2257c45e68d3edca4effa80f9`；状态 `success`。

```sql
WITH cust AS (
  SELECT "Customer ID", "Customer Segment", gender, age, "Education Level", "Marital Status", Region, Country, City
  FROM customer_information GROUP BY "Customer ID"
),
cust_orders AS (
  SELECT "Customer ID", COUNT(*) AS orders, COUNT(DISTINCT "Order ID") AS order_ids, SUM(Sales) AS sales, SUM(profit) AS profit, SUM(CASE WHEN Discount IS NOT NULL AND CAST(Discount AS REAL) > 0 THEN 1 ELSE 0 END) AS discounted_orders
  FROM order_information WHERE "Product Category" = 'Fashion' GROUP BY "Customer ID"
)
SELECT c."Customer Segment", COUNT(*) AS customers, SUM(co.orders) AS fashion_orders, SUM(co.sales) AS sales, SUM(co.profit) AS profit,
  SUM(co.profit)/COUNT(*) AS profit_per_customer, SUM(co.orders)/COUNT(*) AS orders_per_customer, AVG(co.profit/co.orders) AS avg_profit_per_order
FROM cust c JOIN cust_orders co ON c."Customer ID" = co."Customer ID"
GROUP BY c."Customer Segment" ORDER BY profit DESC
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-018/attempt-01/sql/S19.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-018/attempt-01/sql/S19.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-018/attempt-01/results/S19.rows.jsonl)；完整：True；SHA256：`27660671c8fee3343de134e3f7d76e05a7be048ae51db5fe7a7948f5adec7fa0`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "customer_information", "kind": "base", "block": null, "base_tables": ["customer_information"]}] | [] | ["\"Customer ID\""] |
| B2 | [{"alias": "order_information", "kind": "base", "block": null, "base_tables": ["order_information"]}] | [] | ["\"Customer ID\""] |
| B3 | [{"alias": "c", "kind": "derived", "block": "B1", "base_tables": ["customer_information"]}, {"alias": "co", "kind": "derived", "block": "B2", "base_tables": ["order_information"]}] | [{"type": "INNER", "right": "cust_orders AS co", "on": "c.\"Customer ID\" = co.\"Customer ID\"", "using": []}] | ["c.\"Customer Segment\""] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B2 | COUNT(*) | [] | [] | True |
| B2 | COUNT(DISTINCT "Order ID") | [{"table": "order_information", "column": "Order ID"}] | [] | False |
| B2 | SUM(Sales) | [{"table": "order_information", "column": "Sales"}] | [] | False |
| B2 | SUM(profit) | [{"table": "order_information", "column": "profit"}] | [] | False |
| B2 | SUM(CASE WHEN NOT Discount IS NULL AND CAST(Discount AS REAL) > 0 THEN 1 ELSE 0 END) | [] | [{"table": "order_information", "column": "Discount"}, {"table": "order_information", "column": "Discount"}] | False |
| B3 | COUNT(*) | [] | [] | True |
| B3 | SUM(co.orders) | [] | [] | False |
| B3 | SUM(co.sales) | [{"table": "order_information", "column": "Sales"}] | [] | False |
| B3 | SUM(co.profit) | [{"table": "order_information", "column": "profit"}] | [] | False |
| B3 | AVG(co.profit / co.orders) | [{"table": "order_information", "column": "profit"}] | [] | False |
| B3 | SUM(co.profit) | [{"table": "order_information", "column": "profit"}] | [] | False |
| B3 | COUNT(*) | [] | [] | True |
| B3 | SUM(co.orders) | [] | [] | False |
| B3 | COUNT(*) | [] | [] | True |


## S20

类别 `data`；来源 `query_db`；调用 `6eeb76df6de54156a44339afe54c8354`；状态 `success`。

```sql
WITH cust AS (
  SELECT "Customer ID", "Customer Segment", gender, age, "Education Level", "Marital Status", Region, Country, City
  FROM customer_information GROUP BY "Customer ID"
),
cust_orders AS (
  SELECT "Customer ID", COUNT(*) AS orders, SUM(Sales) AS sales, SUM(profit) AS profit
  FROM order_information WHERE "Product Category" = 'Fashion' GROUP BY "Customer ID"
)
SELECT c.gender, COUNT(*) AS customers, SUM(co.orders) AS fashion_orders, SUM(co.sales) AS sales, SUM(co.profit) AS profit,
  SUM(co.profit)/COUNT(*) AS profit_per_customer, SUM(co.orders)/COUNT(*) AS orders_per_customer, AVG(co.profit/co.orders) AS avg_profit_per_order
FROM cust c JOIN cust_orders co ON c."Customer ID" = co."Customer ID"
GROUP BY c.gender ORDER BY profit DESC
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-018/attempt-01/sql/S20.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-018/attempt-01/sql/S20.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-018/attempt-01/results/S20.rows.jsonl)；完整：True；SHA256：`982996f87423de7763fcde76aa897aedcf3c1420fb3f080c7ba51929e4872b57`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "customer_information", "kind": "base", "block": null, "base_tables": ["customer_information"]}] | [] | ["\"Customer ID\""] |
| B2 | [{"alias": "order_information", "kind": "base", "block": null, "base_tables": ["order_information"]}] | [] | ["\"Customer ID\""] |
| B3 | [{"alias": "c", "kind": "derived", "block": "B1", "base_tables": ["customer_information"]}, {"alias": "co", "kind": "derived", "block": "B2", "base_tables": ["order_information"]}] | [{"type": "INNER", "right": "cust_orders AS co", "on": "c.\"Customer ID\" = co.\"Customer ID\"", "using": []}] | ["c.gender"] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B2 | COUNT(*) | [] | [] | True |
| B2 | SUM(Sales) | [{"table": "order_information", "column": "Sales"}] | [] | False |
| B2 | SUM(profit) | [{"table": "order_information", "column": "profit"}] | [] | False |
| B3 | COUNT(*) | [] | [] | True |
| B3 | SUM(co.orders) | [] | [] | False |
| B3 | SUM(co.sales) | [{"table": "order_information", "column": "Sales"}] | [] | False |
| B3 | SUM(co.profit) | [{"table": "order_information", "column": "profit"}] | [] | False |
| B3 | AVG(co.profit / co.orders) | [{"table": "order_information", "column": "profit"}] | [] | False |
| B3 | SUM(co.profit) | [{"table": "order_information", "column": "profit"}] | [] | False |
| B3 | COUNT(*) | [] | [] | True |
| B3 | SUM(co.orders) | [] | [] | False |
| B3 | COUNT(*) | [] | [] | True |


## S21

类别 `data`；来源 `query_db`；调用 `2e72361a0abc404288c6e64eaf765d8c`；状态 `success`。

```sql
WITH cust AS (
  SELECT "Customer ID", "Customer Segment", gender, age, "Education Level", "Marital Status", Region, Country, City
  FROM customer_information GROUP BY "Customer ID"
),
cust_orders AS (
  SELECT "Customer ID", COUNT(*) AS orders, SUM(Sales) AS sales, SUM(profit) AS profit
  FROM order_information WHERE "Product Category" = 'Fashion' GROUP BY "Customer ID"
),
agebuckets AS (
  SELECT "Customer ID", CASE
    WHEN age < 25 THEN '18-24'
    WHEN age < 35 THEN '25-34'
    WHEN age < 45 THEN '35-44'
    WHEN age < 55 THEN '45-54'
    WHEN age < 65 THEN '55-64'
    ELSE '65+' END AS age_group
  FROM cust
)
SELECT b.age_group, COUNT(*) AS customers, SUM(co.orders) AS orders, SUM(co.profit) AS profit,
  SUM(co.profit)/COUNT(*) AS profit_per_customer, SUM(co.orders)/COUNT(*) AS orders_per_customer,
  AVG(co.profit/co.orders) AS avg_profit_per_order
FROM agebuckets b JOIN cust_orders co ON b."Customer ID" = co."Customer ID"
GROUP BY b.age_group ORDER BY profit_per_customer DESC
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-018/attempt-01/sql/S21.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-018/attempt-01/sql/S21.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-018/attempt-01/results/S21.rows.jsonl)；完整：True；SHA256：`88dc358bcfeafc2f3eff76aefcb848fefc7930fb75d67478dcdba7dd12e81a5d`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "customer_information", "kind": "base", "block": null, "base_tables": ["customer_information"]}] | [] | ["\"Customer ID\""] |
| B2 | [{"alias": "order_information", "kind": "base", "block": null, "base_tables": ["order_information"]}] | [] | ["\"Customer ID\""] |
| B3 | [{"alias": "cust", "kind": "derived", "block": "B1", "base_tables": ["customer_information"]}] | [] | [] |
| B4 | [{"alias": "b", "kind": "derived", "block": "B3", "base_tables": ["customer_information"]}, {"alias": "co", "kind": "derived", "block": "B2", "base_tables": ["order_information"]}] | [{"type": "INNER", "right": "cust_orders AS co", "on": "b.\"Customer ID\" = co.\"Customer ID\"", "using": []}] | ["b.age_group"] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B2 | COUNT(*) | [] | [] | True |
| B2 | SUM(Sales) | [{"table": "order_information", "column": "Sales"}] | [] | False |
| B2 | SUM(profit) | [{"table": "order_information", "column": "profit"}] | [] | False |
| B4 | COUNT(*) | [] | [] | True |
| B4 | SUM(co.orders) | [] | [] | False |
| B4 | SUM(co.profit) | [{"table": "order_information", "column": "profit"}] | [] | False |
| B4 | AVG(co.profit / co.orders) | [{"table": "order_information", "column": "profit"}] | [] | False |
| B4 | SUM(co.profit) | [{"table": "order_information", "column": "profit"}] | [] | False |
| B4 | COUNT(*) | [] | [] | True |
| B4 | SUM(co.orders) | [] | [] | False |
| B4 | COUNT(*) | [] | [] | True |


## S22

类别 `data`；来源 `query_db`；调用 `85622e6cdb044f8aa5345c7a9a3c75fb`；状态 `success`。

```sql
WITH cust AS (
  SELECT "Customer ID", "Customer Segment", gender, age, "Education Level", "Marital Status", Region, Country, City
  FROM customer_information GROUP BY "Customer ID"
),
cust_orders AS (
  SELECT "Customer ID", COUNT(*) AS orders, SUM(Sales) AS sales, SUM(profit) AS profit
  FROM order_information WHERE "Product Category" = 'Fashion' GROUP BY "Customer ID"
)
SELECT c."Education Level", COUNT(*) AS customers, SUM(co.orders) AS orders, SUM(co.profit) AS profit,
  SUM(co.profit)/COUNT(*) AS profit_per_customer, SUM(co.orders)/COUNT(*) AS orders_per_customer,
  AVG(co.profit/co.orders) AS avg_profit_per_order
FROM cust c JOIN cust_orders co ON c."Customer ID" = co."Customer ID"
GROUP BY c."Education Level" ORDER BY profit DESC
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-018/attempt-01/sql/S22.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-018/attempt-01/sql/S22.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-018/attempt-01/results/S22.rows.jsonl)；完整：True；SHA256：`30ce09820efb8073f52e9b8c4313092bd46ab1c3306314049de3d6f1d4f5362d`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "customer_information", "kind": "base", "block": null, "base_tables": ["customer_information"]}] | [] | ["\"Customer ID\""] |
| B2 | [{"alias": "order_information", "kind": "base", "block": null, "base_tables": ["order_information"]}] | [] | ["\"Customer ID\""] |
| B3 | [{"alias": "c", "kind": "derived", "block": "B1", "base_tables": ["customer_information"]}, {"alias": "co", "kind": "derived", "block": "B2", "base_tables": ["order_information"]}] | [{"type": "INNER", "right": "cust_orders AS co", "on": "c.\"Customer ID\" = co.\"Customer ID\"", "using": []}] | ["c.\"Education Level\""] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B2 | COUNT(*) | [] | [] | True |
| B2 | SUM(Sales) | [{"table": "order_information", "column": "Sales"}] | [] | False |
| B2 | SUM(profit) | [{"table": "order_information", "column": "profit"}] | [] | False |
| B3 | COUNT(*) | [] | [] | True |
| B3 | SUM(co.orders) | [] | [] | False |
| B3 | SUM(co.profit) | [{"table": "order_information", "column": "profit"}] | [] | False |
| B3 | AVG(co.profit / co.orders) | [{"table": "order_information", "column": "profit"}] | [] | False |
| B3 | SUM(co.profit) | [{"table": "order_information", "column": "profit"}] | [] | False |
| B3 | COUNT(*) | [] | [] | True |
| B3 | SUM(co.orders) | [] | [] | False |
| B3 | COUNT(*) | [] | [] | True |


## S23

类别 `data`；来源 `query_db`；调用 `67bebe5d61a34b0e9e7744d7e7a3f3d9`；状态 `success`。

```sql
WITH cust AS (
  SELECT "Customer ID", "Customer Segment", gender, age, "Education Level", "Marital Status", Region, Country, City
  FROM customer_information GROUP BY "Customer ID"
),
cust_orders AS (
  SELECT "Customer ID", COUNT(*) AS orders, SUM(Sales) AS sales, SUM(profit) AS profit
  FROM order_information WHERE "Product Category" = 'Fashion' GROUP BY "Customer ID"
)
SELECT c."Marital Status", COUNT(*) AS customers, SUM(co.orders) AS orders, SUM(co.profit) AS profit,
  SUM(co.profit)/COUNT(*) AS profit_per_customer, SUM(co.orders)/COUNT(*) AS orders_per_customer,
  AVG(co.profit/co.orders) AS avg_profit_per_order
FROM cust c JOIN cust_orders co ON c."Customer ID" = co."Customer ID"
GROUP BY c."Marital Status" ORDER BY profit DESC
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-018/attempt-01/sql/S23.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-018/attempt-01/sql/S23.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-018/attempt-01/results/S23.rows.jsonl)；完整：True；SHA256：`f654c26affc9684542fb78d1a990086ef4ae0ca9d725816cbd918af2384f081f`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "customer_information", "kind": "base", "block": null, "base_tables": ["customer_information"]}] | [] | ["\"Customer ID\""] |
| B2 | [{"alias": "order_information", "kind": "base", "block": null, "base_tables": ["order_information"]}] | [] | ["\"Customer ID\""] |
| B3 | [{"alias": "c", "kind": "derived", "block": "B1", "base_tables": ["customer_information"]}, {"alias": "co", "kind": "derived", "block": "B2", "base_tables": ["order_information"]}] | [{"type": "INNER", "right": "cust_orders AS co", "on": "c.\"Customer ID\" = co.\"Customer ID\"", "using": []}] | ["c.\"Marital Status\""] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B2 | COUNT(*) | [] | [] | True |
| B2 | SUM(Sales) | [{"table": "order_information", "column": "Sales"}] | [] | False |
| B2 | SUM(profit) | [{"table": "order_information", "column": "profit"}] | [] | False |
| B3 | COUNT(*) | [] | [] | True |
| B3 | SUM(co.orders) | [] | [] | False |
| B3 | SUM(co.profit) | [{"table": "order_information", "column": "profit"}] | [] | False |
| B3 | AVG(co.profit / co.orders) | [{"table": "order_information", "column": "profit"}] | [] | False |
| B3 | SUM(co.profit) | [{"table": "order_information", "column": "profit"}] | [] | False |
| B3 | COUNT(*) | [] | [] | True |
| B3 | SUM(co.orders) | [] | [] | False |
| B3 | COUNT(*) | [] | [] | True |


## S24

类别 `data`；来源 `query_db`；调用 `974e7b9c29814f7388e1e8f990ce64a6`；状态 `success`。

```sql
WITH cust AS (
  SELECT "Customer ID", "Customer Segment", gender, age, "Education Level", "Marital Status", Region, Country, City
  FROM customer_information GROUP BY "Customer ID"
),
cust_orders AS (
  SELECT "Customer ID", COUNT(*) AS orders, SUM(Sales) AS sales, SUM(profit) AS profit
  FROM order_information WHERE "Product Category" = 'Fashion' GROUP BY "Customer ID"
)
SELECT c.Region, COUNT(*) AS customers, SUM(co.orders) AS orders, SUM(co.profit) AS profit,
  SUM(co.profit)/COUNT(*) AS profit_per_customer, SUM(co.orders)/COUNT(*) AS orders_per_customer
FROM cust c JOIN cust_orders co ON c."Customer ID" = co."Customer ID"
GROUP BY c.Region ORDER BY profit DESC
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-018/attempt-01/sql/S24.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-018/attempt-01/sql/S24.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-018/attempt-01/results/S24.rows.jsonl)；完整：True；SHA256：`605707c862b0b4db2cd38ba116498d245c78db0e7145e658fec47d7ffbe3341e`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "customer_information", "kind": "base", "block": null, "base_tables": ["customer_information"]}] | [] | ["\"Customer ID\""] |
| B2 | [{"alias": "order_information", "kind": "base", "block": null, "base_tables": ["order_information"]}] | [] | ["\"Customer ID\""] |
| B3 | [{"alias": "c", "kind": "derived", "block": "B1", "base_tables": ["customer_information"]}, {"alias": "co", "kind": "derived", "block": "B2", "base_tables": ["order_information"]}] | [{"type": "INNER", "right": "cust_orders AS co", "on": "c.\"Customer ID\" = co.\"Customer ID\"", "using": []}] | ["c.Region"] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B2 | COUNT(*) | [] | [] | True |
| B2 | SUM(Sales) | [{"table": "order_information", "column": "Sales"}] | [] | False |
| B2 | SUM(profit) | [{"table": "order_information", "column": "profit"}] | [] | False |
| B3 | COUNT(*) | [] | [] | True |
| B3 | SUM(co.orders) | [] | [] | False |
| B3 | SUM(co.profit) | [{"table": "order_information", "column": "profit"}] | [] | False |
| B3 | SUM(co.profit) | [{"table": "order_information", "column": "profit"}] | [] | False |
| B3 | COUNT(*) | [] | [] | True |
| B3 | SUM(co.orders) | [] | [] | False |
| B3 | COUNT(*) | [] | [] | True |


## S25

类别 `data`；来源 `query_db`；调用 `b656af8689e34b5a8ba0dc55a4a4ae30`；状态 `success`。

```sql
WITH cust AS (
  SELECT "Customer ID", Region, Country, City
  FROM customer_information GROUP BY "Customer ID"
),
cust_orders AS (
  SELECT "Customer ID", COUNT(*) AS orders, SUM(Sales) AS sales, SUM(profit) AS profit
  FROM order_information WHERE "Product Category" = 'Fashion' GROUP BY "Customer ID"
)
SELECT c.Country, COUNT(*) AS customers, SUM(co.orders) AS orders, SUM(co.profit) AS profit,
  SUM(co.profit)/COUNT(*) AS profit_per_customer
FROM cust c JOIN cust_orders co ON c."Customer ID" = co."Customer ID"
GROUP BY c.Country ORDER BY profit DESC
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-018/attempt-01/sql/S25.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-018/attempt-01/sql/S25.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-018/attempt-01/results/S25.rows.jsonl)；完整：True；SHA256：`7bdb677d2643ad8fc2994ed77230a7367a374437a39e5235f86728c19c8b44d3`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "customer_information", "kind": "base", "block": null, "base_tables": ["customer_information"]}] | [] | ["\"Customer ID\""] |
| B2 | [{"alias": "order_information", "kind": "base", "block": null, "base_tables": ["order_information"]}] | [] | ["\"Customer ID\""] |
| B3 | [{"alias": "c", "kind": "derived", "block": "B1", "base_tables": ["customer_information"]}, {"alias": "co", "kind": "derived", "block": "B2", "base_tables": ["order_information"]}] | [{"type": "INNER", "right": "cust_orders AS co", "on": "c.\"Customer ID\" = co.\"Customer ID\"", "using": []}] | ["c.Country"] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B2 | COUNT(*) | [] | [] | True |
| B2 | SUM(Sales) | [{"table": "order_information", "column": "Sales"}] | [] | False |
| B2 | SUM(profit) | [{"table": "order_information", "column": "profit"}] | [] | False |
| B3 | COUNT(*) | [] | [] | True |
| B3 | SUM(co.orders) | [] | [] | False |
| B3 | SUM(co.profit) | [{"table": "order_information", "column": "profit"}] | [] | False |
| B3 | SUM(co.profit) | [{"table": "order_information", "column": "profit"}] | [] | False |
| B3 | COUNT(*) | [] | [] | True |


## S26

类别 `data`；来源 `query_db`；调用 `4eda42980c6842ad87bec4b1bb68dbad`；状态 `success`。

```sql
SELECT "Product", COUNT(*) AS orders, SUM(Sales) AS sales, SUM(profit) AS profit, AVG(profit) AS avg_profit_per_order
FROM order_information WHERE "Product Category" = 'Fashion'
GROUP BY "Product" ORDER BY profit DESC
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-018/attempt-01/sql/S26.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-018/attempt-01/sql/S26.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-018/attempt-01/results/S26.rows.jsonl)；完整：True；SHA256：`ae929c092298f1a9e50700784b9931b522ed39a0e73a695d90225828e4b214f7`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "order_information", "kind": "base", "block": null, "base_tables": ["order_information"]}] | [] | ["\"Product\""] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |
| B1 | SUM(Sales) | [{"table": "order_information", "column": "Sales"}] | [] | False |
| B1 | SUM(profit) | [{"table": "order_information", "column": "profit"}] | [] | False |
| B1 | AVG(profit) | [{"table": "order_information", "column": "profit"}] | [] | False |


## S27

类别 `data`；来源 `query_db`；调用 `cc19844b0da649b3933bf765efaee513`；状态 `success`。

```sql
WITH cust AS (
  SELECT "Customer ID", "Customer Segment", gender, age, Region, Country
  FROM customer_information GROUP BY "Customer ID"
),
cust_orders AS (
  SELECT "Customer ID", COUNT(*) AS orders, SUM(Sales) AS sales, SUM(profit) AS profit
  FROM order_information WHERE "Product Category" = 'Fashion' GROUP BY "Customer ID"
)
SELECT c.gender, c."Customer Segment", COUNT(*) AS customers, SUM(co.orders) AS orders,
  SUM(co.profit) AS profit, SUM(co.profit)/COUNT(*) AS profit_per_customer,
  SUM(co.orders)/COUNT(*) AS orders_per_customer
FROM cust c JOIN cust_orders co ON c."Customer ID" = co."Customer ID"
GROUP BY c.gender, c."Customer Segment" ORDER BY profit_per_customer DESC
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-018/attempt-01/sql/S27.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-018/attempt-01/sql/S27.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-018/attempt-01/results/S27.rows.jsonl)；完整：True；SHA256：`4663df28c757ef61f119bcf3509805f3cd0263866d013948abdbc1dc9ccc02a4`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "customer_information", "kind": "base", "block": null, "base_tables": ["customer_information"]}] | [] | ["\"Customer ID\""] |
| B2 | [{"alias": "order_information", "kind": "base", "block": null, "base_tables": ["order_information"]}] | [] | ["\"Customer ID\""] |
| B3 | [{"alias": "c", "kind": "derived", "block": "B1", "base_tables": ["customer_information"]}, {"alias": "co", "kind": "derived", "block": "B2", "base_tables": ["order_information"]}] | [{"type": "INNER", "right": "cust_orders AS co", "on": "c.\"Customer ID\" = co.\"Customer ID\"", "using": []}] | ["c.gender", "c.\"Customer Segment\""] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B2 | COUNT(*) | [] | [] | True |
| B2 | SUM(Sales) | [{"table": "order_information", "column": "Sales"}] | [] | False |
| B2 | SUM(profit) | [{"table": "order_information", "column": "profit"}] | [] | False |
| B3 | COUNT(*) | [] | [] | True |
| B3 | SUM(co.orders) | [] | [] | False |
| B3 | SUM(co.profit) | [{"table": "order_information", "column": "profit"}] | [] | False |
| B3 | SUM(co.profit) | [{"table": "order_information", "column": "profit"}] | [] | False |
| B3 | COUNT(*) | [] | [] | True |
| B3 | SUM(co.orders) | [] | [] | False |
| B3 | COUNT(*) | [] | [] | True |


## S28

类别 `data`；来源 `query_db`；调用 `d6878689ea1d4c91b29af127d09e98aa`；状态 `success`。

```sql
WITH cust AS (
  SELECT "Customer ID", gender, age, "Customer Segment"
  FROM customer_information GROUP BY "Customer ID"
),
cust_orders AS (
  SELECT "Customer ID", COUNT(*) AS orders, SUM(Sales) AS sales, SUM(profit) AS profit
  FROM order_information WHERE "Product Category" = 'Fashion' GROUP BY "Customer ID"
)
SELECT c.gender,
  CASE WHEN c.age < 35 THEN 'under35' ELSE '35plus' END AS age_group,
  COUNT(*) AS customers, SUM(co.profit) AS profit, SUM(co.profit)/COUNT(*) AS profit_per_customer,
  SUM(co.orders)/COUNT(*) AS orders_per_customer
FROM cust c JOIN cust_orders co ON c."Customer ID" = co."Customer ID"
GROUP BY c.gender, age_group ORDER BY profit_per_customer DESC
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-018/attempt-01/sql/S28.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-018/attempt-01/sql/S28.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-018/attempt-01/results/S28.rows.jsonl)；完整：True；SHA256：`203ae6cb6aae4a8c94334b9b36ef6ff8f5d9699d9a51bb59d847456eb7f9f397`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "customer_information", "kind": "base", "block": null, "base_tables": ["customer_information"]}] | [] | ["\"Customer ID\""] |
| B2 | [{"alias": "order_information", "kind": "base", "block": null, "base_tables": ["order_information"]}] | [] | ["\"Customer ID\""] |
| B3 | [{"alias": "c", "kind": "derived", "block": "B1", "base_tables": ["customer_information"]}, {"alias": "co", "kind": "derived", "block": "B2", "base_tables": ["order_information"]}] | [{"type": "INNER", "right": "cust_orders AS co", "on": "c.\"Customer ID\" = co.\"Customer ID\"", "using": []}] | ["c.gender", "CASE WHEN c.age < 35 THEN 'under35' ELSE '35plus' END"] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B2 | COUNT(*) | [] | [] | True |
| B2 | SUM(Sales) | [{"table": "order_information", "column": "Sales"}] | [] | False |
| B2 | SUM(profit) | [{"table": "order_information", "column": "profit"}] | [] | False |
| B3 | COUNT(*) | [] | [] | True |
| B3 | SUM(co.profit) | [{"table": "order_information", "column": "profit"}] | [] | False |
| B3 | SUM(co.profit) | [{"table": "order_information", "column": "profit"}] | [] | False |
| B3 | COUNT(*) | [] | [] | True |
| B3 | SUM(co.orders) | [] | [] | False |
| B3 | COUNT(*) | [] | [] | True |


## S29

类别 `data`；来源 `query_db`；调用 `8b32a8fa360241038dd42121b2948580`；状态 `success`。

```sql
SELECT "Customer ID", COUNT(*) AS rows_cnt, SUM("Browsing Time (minutes)") AS total_browse, SUM(like) AS likes, SUM(share) AS shares, SUM("Add to Cart") AS carts
FROM product_browsing WHERE "Product Category" = 'Fashion' GROUP BY "Customer ID" ORDER BY rows_cnt DESC LIMIT 10
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-018/attempt-01/sql/S29.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-018/attempt-01/sql/S29.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-018/attempt-01/results/S29.rows.jsonl)；完整：True；SHA256：`5eb0a1209a9e9272237a99678e52e9ee339dd6c2ea592d1192e1d0dd2499a190`。

## S30

类别 `data`；来源 `query_db`；调用 `48ccc20d21de4047aac20cd89d367782`；状态 `success`。

```sql
SELECT COUNT(*) AS rows_cnt, COUNT(DISTINCT "Customer ID") AS customers FROM product_browsing WHERE "Product Category" = 'Fashion'
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-018/attempt-01/sql/S30.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-018/attempt-01/sql/S30.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-018/attempt-01/results/S30.rows.jsonl)；完整：True；SHA256：`81e6249e7f1c0dbd7f7b196fa140ec4b0502f4760114b20c9162f22451710849`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "product_browsing", "kind": "base", "block": null, "base_tables": ["product_browsing"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |
| B1 | COUNT(DISTINCT "Customer ID") | [{"table": "product_browsing", "column": "Customer ID"}] | [] | False |


## S31

类别 `data`；来源 `query_db`；调用 `bd4a32ac3a1b45d08cb7bdcdaf542cb5`；状态 `success`。

```sql
SELECT "Product", COUNT(*) AS browsed, SUM(like) AS likes, SUM(share) AS shares, SUM("Add to Cart") AS carts, AVG("Browsing Time (minutes)") AS avg_browse
FROM product_browsing WHERE "Product Category" = 'Fashion' GROUP BY "Product" ORDER BY browsed DESC
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-018/attempt-01/sql/S31.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-018/attempt-01/sql/S31.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-018/attempt-01/results/S31.rows.jsonl)；完整：True；SHA256：`e3aa056b9b41aa2c237b43640b062d51cc85b76226a85de9b72963197ee74289`。

## S32

类别 `data`；来源 `query_db`；调用 `5676a4768a294a1b9b38bd8444ac8c2e`；状态 `success`。

```sql
WITH cust AS (
  SELECT "Customer ID", "Customer Segment", gender, age
  FROM customer_information GROUP BY "Customer ID"
),
cust_orders AS (
  SELECT "Customer ID", COUNT(*) AS orders, SUM(profit) AS profit, SUM(Sales) AS sales
  FROM order_information WHERE "Product Category" = 'Fashion' GROUP BY "Customer ID"
),
cust_browse AS (
  SELECT "Customer ID", SUM(like) AS likes, SUM(share) AS shares, SUM("Add to Cart") AS carts, SUM("Browsing Time (minutes)") AS browse_time
  FROM product_browsing WHERE "Product Category" = 'Fashion' GROUP BY "Customer ID"
)
SELECT c.gender, c."Customer Segment",
  AVG(b.carts*1.0/o.orders) AS carts_per_order,
  AVG(b.likes*1.0/o.orders) AS likes_per_order,
  AVG(b.shares*1.0/o.orders) AS shares_per_order,
  AVG(b.browse_time/o.orders) AS browse_min_per_order,
  SUM(o.profit)/COUNT(*) AS profit_per_customer
FROM cust c JOIN cust_orders o ON c."Customer ID"=o."Customer ID" JOIN cust_browse b ON c."Customer ID"=b."Customer ID"
GROUP BY c.gender, c."Customer Segment" ORDER BY profit_per_customer DESC
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-018/attempt-01/sql/S32.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-018/attempt-01/sql/S32.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-018/attempt-01/results/S32.rows.jsonl)；完整：True；SHA256：`de47edf7e80e9d4b7a87fdbd7ae3c1f96fc8c7a74a8c60d3117e8e9eb52a3040`。

## S33

类别 `data`；来源 `query_db`；调用 `18580bbeef6448789652e2b2381edd56`；状态 `success`。

```sql
WITH cust_orders AS (
  SELECT "Customer ID", COUNT(*) AS orders, SUM(profit) AS profit
  FROM order_information WHERE "Product Category" = 'Fashion' GROUP BY "Customer ID"
),
cust_browse AS (
  SELECT "Customer ID", SUM(like) AS likes, SUM(share) AS shares, SUM("Add to Cart") AS carts, SUM("Browsing Time (minutes)") AS browse_time
  FROM product_browsing WHERE "Product Category" = 'Fashion' GROUP BY "Customer ID"
)
SELECT CASE WHEN b.carts*1.0/o.orders >= 0.5 THEN 'high_cart_rate' ELSE 'low_cart_rate' END AS cart_rate_group,
  COUNT(*) AS customers, SUM(o.profit) AS profit, SUM(o.profit)/COUNT(*) AS profit_per_customer
FROM cust_orders o JOIN cust_browse b ON o."Customer ID"=b."Customer ID"
GROUP BY cart_rate_group ORDER BY profit_per_customer DESC
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-018/attempt-01/sql/S33.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-018/attempt-01/sql/S33.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-018/attempt-01/results/S33.rows.jsonl)；完整：True；SHA256：`63baa4578f26ef4bd4ab3c836da886886ebfc69fc9fe7e24ba11a708920a4de3`。

## S34

类别 `data`；来源 `query_db`；调用 `87c7a1cdd7074c45a04dcb320dfc6cab`；状态 `success`。

```sql
WITH cust AS (
  SELECT "Customer ID", "Customer Segment", gender, age, "Education Level", "Marital Status", Region, Country
  FROM customer_information GROUP BY "Customer ID"
),
cust_orders AS (
  SELECT "Customer ID", COUNT(*) AS orders, SUM(profit) AS profit, SUM(Sales) AS sales
  FROM order_information WHERE "Product Category" = 'Fashion' GROUP BY "Customer ID"
),
ranked AS (
  SELECT c.*, co.profit, co.orders, co.sales, NTILE(10) OVER (ORDER BY co.profit DESC) AS decile
  FROM cust c JOIN cust_orders co ON c."Customer ID" = co."Customer ID"
)
SELECT gender, "Customer Segment", COUNT(*) AS customers, SUM(profit) AS profit, SUM(profit)/COUNT(*) AS avg_profit
FROM ranked WHERE decile = 1
GROUP BY gender, "Customer Segment" ORDER BY avg_profit DESC
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-018/attempt-01/sql/S34.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-018/attempt-01/sql/S34.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-018/attempt-01/results/S34.rows.jsonl)；完整：True；SHA256：`823e088a857d6baab2cad88110a1ca6843e3943144e63976991141dec8a79e86`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "customer_information", "kind": "base", "block": null, "base_tables": ["customer_information"]}] | [] | ["\"Customer ID\""] |
| B2 | [{"alias": "order_information", "kind": "base", "block": null, "base_tables": ["order_information"]}] | [] | ["\"Customer ID\""] |
| B3 | [{"alias": "c", "kind": "derived", "block": "B1", "base_tables": ["customer_information"]}, {"alias": "co", "kind": "derived", "block": "B2", "base_tables": ["order_information"]}] | [{"type": "INNER", "right": "cust_orders AS co", "on": "c.\"Customer ID\" = co.\"Customer ID\"", "using": []}] | [] |
| B4 | [{"alias": "ranked", "kind": "derived", "block": "B3", "base_tables": ["customer_information", "order_information"]}] | [] | ["gender", "\"Customer Segment\""] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B2 | COUNT(*) | [] | [] | True |
| B2 | SUM(profit) | [{"table": "order_information", "column": "profit"}] | [] | False |
| B2 | SUM(Sales) | [{"table": "order_information", "column": "Sales"}] | [] | False |
| B4 | COUNT(*) | [] | [] | True |
| B4 | SUM(profit) | [{"table": "order_information", "column": "profit"}] | [] | False |
| B4 | SUM(profit) | [{"table": "order_information", "column": "profit"}] | [] | False |
| B4 | COUNT(*) | [] | [] | True |


## S35

类别 `data`；来源 `query_db`；调用 `c34e1c9e850e444cb1e8e64da095331d`；状态 `success`。

```sql
WITH cust_orders AS (
  SELECT "Customer ID", COUNT(*) AS orders, SUM(profit) AS profit, SUM(Sales) AS sales
  FROM order_information WHERE "Product Category" = 'Fashion' GROUP BY "Customer ID"
)
SELECT COUNT(*) AS top10_customers, SUM(profit) AS top10_profit, SUM(profit) * 100.0 / (SELECT SUM(profit) FROM cust_orders) AS pct_of_total_profit
FROM (SELECT "Customer ID", profit FROM cust_orders ORDER BY profit DESC LIMIT 80)
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-018/attempt-01/sql/S35.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-018/attempt-01/sql/S35.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-018/attempt-01/results/S35.rows.jsonl)；完整：True；SHA256：`b5ef3c6056ab9474553fb05177dccec1cc868106cb8e024b36b49eda91c4c4b6`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "order_information", "kind": "base", "block": null, "base_tables": ["order_information"]}] | [] | ["\"Customer ID\""] |
| B2 | [{"alias": "cust_orders", "kind": "derived", "block": "B1", "base_tables": ["order_information"]}] | [] | [] |
| B3 | [{"alias": "cust_orders", "kind": "derived", "block": "B1", "base_tables": ["order_information"]}] | [] | [] |
| B4 | [{"alias": "", "kind": "derived", "block": "B2", "base_tables": ["order_information"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |
| B1 | SUM(profit) | [{"table": "order_information", "column": "profit"}] | [] | False |
| B1 | SUM(Sales) | [{"table": "order_information", "column": "Sales"}] | [] | False |
| B3 | SUM(profit) | [{"table": "order_information", "column": "profit"}] | [] | False |
| B4 | COUNT(*) | [] | [] | True |
| B4 | SUM(profit) | [{"table": "order_information", "column": "profit"}] | [] | False |
| B4 | SUM(profit) | [{"table": "order_information", "column": "profit"}] | [] | False |


## S36

类别 `data`；来源 `query_db`；调用 `bd99779e377b4e9e9eb2da8b6f3df09e`；状态 `success`。

```sql
WITH cust_orders AS (
  SELECT "Customer ID", COUNT(*) AS orders, SUM(profit) AS profit
  FROM order_information WHERE "Product Category" = 'Fashion' GROUP BY "Customer ID"
),
ranked AS (
  SELECT profit, NTILE(5) OVER (ORDER BY profit DESC) AS quintile
  FROM cust_orders
)
SELECT quintile, COUNT(*) AS customers, SUM(profit) AS profit, SUM(profit)*100.0/(SELECT SUM(profit) FROM cust_orders) AS pct_of_profit
FROM ranked GROUP BY quintile ORDER BY quintile
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-018/attempt-01/sql/S36.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-018/attempt-01/sql/S36.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-018/attempt-01/results/S36.rows.jsonl)；完整：True；SHA256：`742acecb1de05a8eaa3b48061964bfd108aaea6610a5397f0503b28e13df9efe`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "order_information", "kind": "base", "block": null, "base_tables": ["order_information"]}] | [] | ["\"Customer ID\""] |
| B2 | [{"alias": "cust_orders", "kind": "derived", "block": "B1", "base_tables": ["order_information"]}] | [] | [] |
| B3 | [{"alias": "cust_orders", "kind": "derived", "block": "B1", "base_tables": ["order_information"]}] | [] | [] |
| B4 | [{"alias": "ranked", "kind": "derived", "block": "B2", "base_tables": ["order_information"]}] | [] | ["quintile"] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |
| B1 | SUM(profit) | [{"table": "order_information", "column": "profit"}] | [] | False |
| B3 | SUM(profit) | [{"table": "order_information", "column": "profit"}] | [] | False |
| B4 | COUNT(*) | [] | [] | True |
| B4 | SUM(profit) | [{"table": "order_information", "column": "profit"}] | [] | False |
| B4 | SUM(profit) | [{"table": "order_information", "column": "profit"}] | [] | False |


## S37

类别 `data`；来源 `query_db`；调用 `96326d89a38647a0af56f2214e7a0e0e`；状态 `success`。

```sql
WITH cust AS (
  SELECT "Customer ID", gender, "Customer Segment"
  FROM customer_information GROUP BY "Customer ID"
),
cust_orders AS (
  SELECT "Customer ID", SUM(profit) AS profit
  FROM order_information WHERE "Product Category" = 'Fashion' GROUP BY "Customer ID"
)
SELECT c.gender, COUNT(*) AS customers, COUNT(*)*100.0/795 AS pct_of_customers,
  SUM(co.profit) AS profit, SUM(co.profit)*100.0/(SELECT SUM(profit) FROM cust_orders) AS pct_of_profit,
  SUM(co.profit)/COUNT(*) AS profit_per_customer
FROM cust c JOIN cust_orders co ON c."Customer ID"=co."Customer ID"
GROUP BY c.gender
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-018/attempt-01/sql/S37.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-018/attempt-01/sql/S37.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-018/attempt-01/results/S37.rows.jsonl)；完整：True；SHA256：`a2983aefb29711464ad9a1ca83e2443103006ada783c418a48433b12a6404524`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "customer_information", "kind": "base", "block": null, "base_tables": ["customer_information"]}] | [] | ["\"Customer ID\""] |
| B2 | [{"alias": "order_information", "kind": "base", "block": null, "base_tables": ["order_information"]}] | [] | ["\"Customer ID\""] |
| B3 | [{"alias": "cust_orders", "kind": "derived", "block": "B2", "base_tables": ["order_information"]}] | [] | [] |
| B4 | [{"alias": "c", "kind": "derived", "block": "B1", "base_tables": ["customer_information"]}, {"alias": "co", "kind": "derived", "block": "B2", "base_tables": ["order_information"]}] | [{"type": "INNER", "right": "cust_orders AS co", "on": "c.\"Customer ID\" = co.\"Customer ID\"", "using": []}] | ["c.gender"] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B2 | SUM(profit) | [{"table": "order_information", "column": "profit"}] | [] | False |
| B3 | SUM(profit) | [{"table": "order_information", "column": "profit"}] | [] | False |
| B4 | COUNT(*) | [] | [] | True |
| B4 | SUM(co.profit) | [{"table": "order_information", "column": "profit"}] | [] | False |
| B4 | SUM(co.profit) | [{"table": "order_information", "column": "profit"}] | [] | False |
| B4 | COUNT(*) | [] | [] | True |
| B4 | COUNT(*) | [] | [] | True |
| B4 | SUM(co.profit) | [{"table": "order_information", "column": "profit"}] | [] | False |


## S38

类别 `data`；来源 `query_db`；调用 `bd00012d426141acac1b885d20f7c29e`；状态 `success`。

```sql
WITH cust AS (
  SELECT "Customer ID", gender, "Customer Segment"
  FROM customer_information GROUP BY "Customer ID"
),
cust_orders AS (
  SELECT "Customer ID", SUM(profit) AS profit, SUM(Sales) AS sales, COUNT(*) AS orders
  FROM order_information WHERE "Product Category" = 'Fashion' GROUP BY "Customer ID"
)
SELECT o."Product", c.gender, COUNT(*) AS orders, SUM(o.profit) AS profit, SUM(o.profit)/COUNT(*) AS profit_per_order
FROM order_information o JOIN cust c ON o."Customer ID"=c."Customer ID"
WHERE o."Product Category" = 'Fashion'
GROUP BY o."Product", c.gender
ORDER BY o."Product", profit DESC
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-018/attempt-01/sql/S38.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-018/attempt-01/sql/S38.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-018/attempt-01/results/S38.rows.jsonl)；完整：True；SHA256：`ae044ab58c53d1efbc06a279711115036ff2f15a85adb2369f28ad5ed1764844`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "customer_information", "kind": "base", "block": null, "base_tables": ["customer_information"]}] | [] | ["\"Customer ID\""] |
| B2 | [{"alias": "order_information", "kind": "base", "block": null, "base_tables": ["order_information"]}] | [] | ["\"Customer ID\""] |
| B3 | [{"alias": "o", "kind": "base", "block": null, "base_tables": ["order_information"]}, {"alias": "c", "kind": "derived", "block": "B1", "base_tables": ["customer_information"]}] | [{"type": "INNER", "right": "cust AS c", "on": "o.\"Customer ID\" = c.\"Customer ID\"", "using": []}] | ["o.\"Product\"", "c.gender"] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B2 | SUM(profit) | [{"table": "order_information", "column": "profit"}] | [] | False |
| B2 | SUM(Sales) | [{"table": "order_information", "column": "Sales"}] | [] | False |
| B2 | COUNT(*) | [] | [] | True |
| B3 | COUNT(*) | [] | [] | True |
| B3 | SUM(o.profit) | [{"table": "order_information", "column": "profit"}] | [] | False |
| B3 | SUM(o.profit) | [{"table": "order_information", "column": "profit"}] | [] | False |
| B3 | COUNT(*) | [] | [] | True |


## S39

类别 `data`；来源 `query_db`；调用 `f0a3f94e227640f783439b3c04d21c3a`；状态 `failed`。

```sql
WITH cust AS (
  SELECT "Customer ID", gender
  FROM customer_information GROUP BY "Customer ID"
)
SELECT c.gender, EXTRACT(YEAR FROM o."Order Date") AS year, EXTRACT(MONTH FROM o."Order Date") AS month,
  COUNT(*) AS orders, SUM(o.profit) AS profit
FROM order_information o JOIN cust c ON o."Customer ID"=c."Customer ID"
WHERE o."Product Category" = 'Fashion'
GROUP BY c.gender, year, month ORDER BY year, month, c.gender
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-018/attempt-01/sql/S39.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-018/attempt-01/sql/S39.parameters.json)。

错误：`OperationalError('near "FROM": syntax error')`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "customer_information", "kind": "base", "block": null, "base_tables": ["customer_information"]}] | [] | ["\"Customer ID\""] |
| B2 | [{"alias": "o", "kind": "base", "block": null, "base_tables": ["order_information"]}, {"alias": "c", "kind": "derived", "block": "B1", "base_tables": ["customer_information"]}] | [{"type": "INNER", "right": "cust AS c", "on": "o.\"Customer ID\" = c.\"Customer ID\"", "using": []}] | ["c.gender", "EXTRACT(YEAR FROM o.\"Order Date\")", "month"] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B2 | COUNT(*) | [] | [] | True |
| B2 | SUM(o.profit) | [{"table": "order_information", "column": "profit"}] | [] | False |


## S40

类别 `data`；来源 `query_db`；调用 `5c38fff3d90e4be4ac3d6c2f4d774278`；状态 `success`。

```sql
SELECT c.gender,
  AVG(CAST(o.Discount AS REAL)) AS avg_discount,
  SUM(CASE WHEN CAST(o.Discount AS REAL) > 0 THEN 1 ELSE 0 END)*100.0/COUNT(*) AS pct_discounted,
  AVG(CAST(o."Shipping Cost" AS REAL)) AS avg_shipping_cost,
  o."Shipping Method", COUNT(*) AS orders
FROM order_information o JOIN customer_information c ON o."Customer ID"=c."Customer ID"
WHERE o."Product Category" = 'Fashion'
GROUP BY c.gender, o."Shipping Method"
ORDER BY c.gender, orders DESC
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-018/attempt-01/sql/S40.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-018/attempt-01/sql/S40.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-018/attempt-01/results/S40.rows.jsonl)；完整：True；SHA256：`7ea753f71ee7a20d27693d3f96c2b3fc825e4b30afa12b3a9c1af28644d1fbc9`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "o", "kind": "base", "block": null, "base_tables": ["order_information"]}, {"alias": "c", "kind": "base", "block": null, "base_tables": ["customer_information"]}] | [{"type": "INNER", "right": "customer_information AS c", "on": "o.\"Customer ID\" = c.\"Customer ID\"", "using": []}] | ["c.gender", "o.\"Shipping Method\""] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | AVG(CAST(o.Discount AS REAL)) | [{"table": "order_information", "column": "Discount"}] | [] | False |
| B1 | AVG(CAST(o."Shipping Cost" AS REAL)) | [{"table": "order_information", "column": "Shipping Cost"}] | [] | False |
| B1 | COUNT(*) | [] | [] | True |
| B1 | COUNT(*) | [] | [] | True |
| B1 | SUM(CASE WHEN CAST(o.Discount AS REAL) > 0 THEN 1 ELSE 0 END) | [] | [{"table": "order_information", "column": "Discount"}] | False |


## S41

类别 `data`；来源 `query_db`；调用 `1fb260d7fec748c0827699fabfdf7264`；状态 `success`。

```sql
SELECT DISTINCT "Shipping Method" FROM order_information
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-018/attempt-01/sql/S41.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-018/attempt-01/sql/S41.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-018/attempt-01/results/S41.rows.jsonl)；完整：True；SHA256：`94f812f2a118d64901ef9866a761157159b4c89670a627e69c5db76f11e1254e`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "order_information", "kind": "base", "block": null, "base_tables": ["order_information"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |


## S42

类别 `data`；来源 `query_db`；调用 `2c2f1896ac3a4548be670a1bef90433d`；状态 `success`。

```sql
WITH cust AS (
  SELECT "Customer ID", gender FROM customer_information GROUP BY "Customer ID"
)
SELECT c.gender, o."Shipping Method", COUNT(*) AS orders, SUM(o.profit) AS profit
FROM order_information o JOIN cust c ON o."Customer ID"=c."Customer ID"
WHERE o."Product Category" = 'Fashion'
GROUP BY c.gender, o."Shipping Method" ORDER BY c.gender, orders DESC
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-018/attempt-01/sql/S42.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-018/attempt-01/sql/S42.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-018/attempt-01/results/S42.rows.jsonl)；完整：True；SHA256：`174b225ac011f61a88d22ef1ff168084371f9a552e97c4d777c143c3a67f3eda`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "customer_information", "kind": "base", "block": null, "base_tables": ["customer_information"]}] | [] | ["\"Customer ID\""] |
| B2 | [{"alias": "o", "kind": "base", "block": null, "base_tables": ["order_information"]}, {"alias": "c", "kind": "derived", "block": "B1", "base_tables": ["customer_information"]}] | [{"type": "INNER", "right": "cust AS c", "on": "o.\"Customer ID\" = c.\"Customer ID\"", "using": []}] | ["c.gender", "o.\"Shipping Method\""] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B2 | COUNT(*) | [] | [] | True |
| B2 | SUM(o.profit) | [{"table": "order_information", "column": "profit"}] | [] | False |


## S43

类别 `data`；来源 `query_db`；调用 `ac5b267d40e84ee58ed486191874e74e`；状态 `success`。

```sql
WITH cust AS (
  SELECT "Customer ID", gender FROM customer_information GROUP BY "Customer ID"
)
SELECT c.gender, strftime('%Y', o."Order Date") AS year, strftime('%m', o."Order Date") AS month,
  COUNT(*) AS orders, SUM(o.profit) AS profit
FROM order_information o JOIN cust c ON o."Customer ID"=c."Customer ID"
WHERE o."Product Category" = 'Fashion'
GROUP BY c.gender, year, month ORDER BY year, month, c.gender
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-018/attempt-01/sql/S43.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-018/attempt-01/sql/S43.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-018/attempt-01/results/S43.rows.jsonl)；完整：True；SHA256：`7f82a8aaa1f7d33eca069bfee508c52be3bdab66df3c2b6b140b3ce5feb0d086`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "customer_information", "kind": "base", "block": null, "base_tables": ["customer_information"]}] | [] | ["\"Customer ID\""] |
| B2 | [{"alias": "o", "kind": "base", "block": null, "base_tables": ["order_information"]}, {"alias": "c", "kind": "derived", "block": "B1", "base_tables": ["customer_information"]}] | [{"type": "INNER", "right": "cust AS c", "on": "o.\"Customer ID\" = c.\"Customer ID\"", "using": []}] | ["c.gender", "STRFTIME('%Y', o.\"Order Date\")", "month"] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B2 | COUNT(*) | [] | [] | True |
| B2 | SUM(o.profit) | [{"table": "order_information", "column": "profit"}] | [] | False |


## S44

类别 `data`；来源 `query_db`；调用 `a0496a1e2e3541fa983ee19b7d5a28fe`；状态 `success`。

```sql
SELECT DISTINCT strftime('%Y-%m', "Order Date") AS ym FROM order_information WHERE "Product Category" = 'Fashion' ORDER BY ym
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-018/attempt-01/sql/S44.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-018/attempt-01/sql/S44.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-018/attempt-01/results/S44.rows.jsonl)；完整：True；SHA256：`c1fbd1910e63454759fe42f5002feeae4d04c71d31227d644168c18b400862c2`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "order_information", "kind": "base", "block": null, "base_tables": ["order_information"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |


## S45

类别 `data`；来源 `query_db`；调用 `8562e5944fe4419ba7a1f0a41c9de355`；状态 `success`。

```sql
WITH cust AS (
  SELECT "Customer ID", gender FROM customer_information GROUP BY "Customer ID"
)
SELECT c.gender, strftime('%Y-%m', o."Order Date") AS ym, COUNT(*) AS orders, SUM(o.profit) AS profit
FROM order_information o JOIN cust c ON o."Customer ID"=c."Customer ID"
WHERE o."Product Category" = 'Fashion'
GROUP BY c.gender, ym ORDER BY ym, c.gender
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-018/attempt-01/sql/S45.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-018/attempt-01/sql/S45.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-018/attempt-01/results/S45.rows.jsonl)；完整：True；SHA256：`31a99498e86453fd407f705af1441b30b0839b898a65ed16b10a540c3457de58`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "customer_information", "kind": "base", "block": null, "base_tables": ["customer_information"]}] | [] | ["\"Customer ID\""] |
| B2 | [{"alias": "o", "kind": "base", "block": null, "base_tables": ["order_information"]}, {"alias": "c", "kind": "derived", "block": "B1", "base_tables": ["customer_information"]}] | [{"type": "INNER", "right": "cust AS c", "on": "o.\"Customer ID\" = c.\"Customer ID\"", "using": []}] | ["c.gender", "STRFTIME('%Y-%m', o.\"Order Date\")"] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B2 | COUNT(*) | [] | [] | True |
| B2 | SUM(o.profit) | [{"table": "order_information", "column": "profit"}] | [] | False |


## S46

类别 `data`；来源 `query_db`；调用 `36f29976daa24711a7f68f764eaaf3b1`；状态 `success`。

```sql
WITH cust AS (
  SELECT "Customer ID", gender, "Customer Segment", age, "Education Level", "Marital Status", Region
  FROM customer_information GROUP BY "Customer ID"
),
cust_orders AS (
  SELECT "Customer ID", COUNT(*) AS orders, SUM(profit) AS profit, SUM(Sales) AS sales
  FROM order_information WHERE "Product Category" = 'Fashion' GROUP BY "Customer ID"
)
SELECT c.gender, c."Customer Segment", c.Region,
  COUNT(*) AS customers, SUM(co.profit) AS profit, SUM(co.profit)/COUNT(*) AS profit_per_customer
FROM cust c JOIN cust_orders co ON c."Customer ID"=co."Customer ID"
GROUP BY c.gender, c."Customer Segment", c.Region
ORDER BY profit_per_customer DESC LIMIT 20
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-018/attempt-01/sql/S46.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-018/attempt-01/sql/S46.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-018/attempt-01/results/S46.rows.jsonl)；完整：True；SHA256：`e5b68ff998bf77a7915a501ae7a4de4601d9cc5a2f5c4abdd7515219a01d3835`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "customer_information", "kind": "base", "block": null, "base_tables": ["customer_information"]}] | [] | ["\"Customer ID\""] |
| B2 | [{"alias": "order_information", "kind": "base", "block": null, "base_tables": ["order_information"]}] | [] | ["\"Customer ID\""] |
| B3 | [{"alias": "c", "kind": "derived", "block": "B1", "base_tables": ["customer_information"]}, {"alias": "co", "kind": "derived", "block": "B2", "base_tables": ["order_information"]}] | [{"type": "INNER", "right": "cust_orders AS co", "on": "c.\"Customer ID\" = co.\"Customer ID\"", "using": []}] | ["c.gender", "c.\"Customer Segment\"", "c.Region"] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B2 | COUNT(*) | [] | [] | True |
| B2 | SUM(profit) | [{"table": "order_information", "column": "profit"}] | [] | False |
| B2 | SUM(Sales) | [{"table": "order_information", "column": "Sales"}] | [] | False |
| B3 | COUNT(*) | [] | [] | True |
| B3 | SUM(co.profit) | [{"table": "order_information", "column": "profit"}] | [] | False |
| B3 | SUM(co.profit) | [{"table": "order_information", "column": "profit"}] | [] | False |
| B3 | COUNT(*) | [] | [] | True |


## S47

类别 `data`；来源 `query_db`；调用 `3bdca5f9c8ec4adf99bb4998ec51f32d`；状态 `success`。

```sql
WITH cust_orders AS (
  SELECT "Customer ID", COUNT(*) AS orders, SUM(profit) AS profit, SUM(Sales) AS sales
  FROM order_information WHERE "Product Category" = 'Fashion' GROUP BY "Customer ID"
)
SELECT
  CASE WHEN orders <= 20 THEN '1-20'
       WHEN orders <= 40 THEN '21-40'
       WHEN orders <= 60 THEN '41-60'
       ELSE '60+' END AS order_freq_group,
  COUNT(*) AS customers, SUM(profit) AS profit, SUM(profit)/COUNT(*) AS profit_per_customer
FROM cust_orders
GROUP BY order_freq_group ORDER BY profit_per_customer DESC
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-018/attempt-01/sql/S47.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-018/attempt-01/sql/S47.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-018/attempt-01/results/S47.rows.jsonl)；完整：True；SHA256：`a5202ea516f797995f97a88ff3c4e268ae1880206d36f0430a7656d329620295`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "order_information", "kind": "base", "block": null, "base_tables": ["order_information"]}] | [] | ["\"Customer ID\""] |
| B2 | [{"alias": "cust_orders", "kind": "derived", "block": "B1", "base_tables": ["order_information"]}] | [] | ["CASE WHEN orders <= 20 THEN '1-20' WHEN orders <= 40 THEN '21-40' WHEN orders <= 60 THEN '41-60' ELSE '60+' END"] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |
| B1 | SUM(profit) | [{"table": "order_information", "column": "profit"}] | [] | False |
| B1 | SUM(Sales) | [{"table": "order_information", "column": "Sales"}] | [] | False |
| B2 | COUNT(*) | [] | [] | True |
| B2 | SUM(profit) | [{"table": "order_information", "column": "profit"}] | [] | False |
| B2 | SUM(profit) | [{"table": "order_information", "column": "profit"}] | [] | False |
| B2 | COUNT(*) | [] | [] | True |


## S48

类别 `data`；来源 `python`；调用 `29cb975d9b5d49379f9d0d8985f8961d`；状态 `success`。

```sql

WITH cust AS (
  SELECT "Customer ID", "Customer Segment" AS segment, gender, age
  FROM customer_information GROUP BY "Customer ID"
),
cust_orders AS (
  SELECT "Customer ID", COUNT(*) AS orders, SUM(profit) AS profit, SUM(Sales) AS sales
  FROM order_information WHERE "Product Category" = 'Fashion' GROUP BY "Customer ID"
),
cust_browse AS (
  SELECT "Customer ID", SUM(like) AS likes, SUM(share) AS shares, SUM("Add to Cart") AS carts,
         SUM("Browsing Time (minutes)") AS browse_time
  FROM product_browsing WHERE "Product Category" = 'Fashion' GROUP BY "Customer ID"
)
SELECT c.gender, c.segment, o.orders, o.profit, o.sales, b.likes, b.shares, b.carts, b.browse_time
FROM cust c JOIN cust_orders o ON c."Customer ID"=o."Customer ID"
JOIN cust_browse b ON c."Customer ID"=b."Customer ID"

```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-018/attempt-01/sql/S48.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-018/attempt-01/sql/S48.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-018/attempt-01/results/S48.rows.jsonl)；完整：True；SHA256：`c79c87d5000a65323fda50a205ee13a153e9387cace8f76cd165d62e8d898453`。

## S49

类别 `data`；来源 `python`；调用 `0a27bd9210824be3921080bf69621db7`；状态 `success`。

```sql

WITH cust AS (SELECT "Customer ID", gender FROM customer_information GROUP BY "Customer ID")
SELECT c.gender, strftime('%Y-%m', o."Order Date") AS ym, SUM(o.profit) AS profit, COUNT(*) AS orders
FROM order_information o JOIN cust c ON o."Customer ID"=c."Customer ID"
WHERE o."Product Category" = 'Fashion'
GROUP BY c.gender, ym

```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-018/attempt-01/sql/S49.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-018/attempt-01/sql/S49.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-018/attempt-01/results/S49.rows.jsonl)；完整：True；SHA256：`34b22f2a0885b4c65531c88c6a7c7ef0a39b24b08708c5753d879db38705ae5d`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "customer_information", "kind": "base", "block": null, "base_tables": ["customer_information"]}] | [] | ["\"Customer ID\""] |
| B2 | [{"alias": "o", "kind": "base", "block": null, "base_tables": ["order_information"]}, {"alias": "c", "kind": "derived", "block": "B1", "base_tables": ["customer_information"]}] | [{"type": "INNER", "right": "cust AS c", "on": "o.\"Customer ID\" = c.\"Customer ID\"", "using": []}] | ["c.gender", "STRFTIME('%Y-%m', o.\"Order Date\")"] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B2 | SUM(o.profit) | [{"table": "order_information", "column": "profit"}] | [] | False |
| B2 | COUNT(*) | [] | [] | True |


## S50

类别 `data`；来源 `query_db`；调用 `1c66ecf3064d4f7ba5e14e818cb22381`；状态 `success`。

```sql
WITH cust AS (
  SELECT "Customer ID", gender FROM customer_information GROUP BY "Customer ID"
)
SELECT o."Product", c.gender, COUNT(*) AS orders, SUM(o.profit) AS profit, SUM(o.Sales) AS sales,
  SUM(o.profit)/COUNT(*) AS profit_per_order, SUM(o.Sales)/COUNT(*) AS sales_per_order
FROM order_information o JOIN cust c ON o."Customer ID"=c."Customer ID"
WHERE o."Product Category" = 'Fashion'
GROUP BY o."Product", c.gender ORDER BY o."Product", c.gender
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-018/attempt-01/sql/S50.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-018/attempt-01/sql/S50.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-018/attempt-01/results/S50.rows.jsonl)；完整：True；SHA256：`0355665a663f7e06a951477495e1c182af312ebda6c4eaa1fe6b0221c6f8a7a4`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "customer_information", "kind": "base", "block": null, "base_tables": ["customer_information"]}] | [] | ["\"Customer ID\""] |
| B2 | [{"alias": "o", "kind": "base", "block": null, "base_tables": ["order_information"]}, {"alias": "c", "kind": "derived", "block": "B1", "base_tables": ["customer_information"]}] | [{"type": "INNER", "right": "cust AS c", "on": "o.\"Customer ID\" = c.\"Customer ID\"", "using": []}] | ["o.\"Product\"", "c.gender"] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B2 | COUNT(*) | [] | [] | True |
| B2 | SUM(o.profit) | [{"table": "order_information", "column": "profit"}] | [] | False |
| B2 | SUM(o.Sales) | [{"table": "order_information", "column": "Sales"}] | [] | False |
| B2 | SUM(o.profit) | [{"table": "order_information", "column": "profit"}] | [] | False |
| B2 | COUNT(*) | [] | [] | True |
| B2 | SUM(o.Sales) | [{"table": "order_information", "column": "Sales"}] | [] | False |
| B2 | COUNT(*) | [] | [] | True |


## S51

类别 `data`；来源 `query_db`；调用 `de61a305ad554afca5d1b7d157bbb14d`；状态 `success`。

```sql
WITH cust AS (
  SELECT "Customer ID", gender FROM customer_information GROUP BY "Customer ID"
)
SELECT c.gender, o."Order Priority", COUNT(*) AS orders, SUM(o.profit) AS profit, SUM(o.profit)/COUNT(*) AS avg_profit_per_order
FROM order_information o JOIN cust c ON o."Customer ID"=c."Customer ID"
WHERE o."Product Category" = 'Fashion'
GROUP BY c.gender, o."Order Priority" ORDER BY c.gender, orders DESC
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-018/attempt-01/sql/S51.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-018/attempt-01/sql/S51.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-018/attempt-01/results/S51.rows.jsonl)；完整：True；SHA256：`2ef4139dd1b1168f6edccd8ea43d6c4276624f751282131746a72c237be41a13`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "customer_information", "kind": "base", "block": null, "base_tables": ["customer_information"]}] | [] | ["\"Customer ID\""] |
| B2 | [{"alias": "o", "kind": "base", "block": null, "base_tables": ["order_information"]}, {"alias": "c", "kind": "derived", "block": "B1", "base_tables": ["customer_information"]}] | [{"type": "INNER", "right": "cust AS c", "on": "o.\"Customer ID\" = c.\"Customer ID\"", "using": []}] | ["c.gender", "o.\"Order Priority\""] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B2 | COUNT(*) | [] | [] | True |
| B2 | SUM(o.profit) | [{"table": "order_information", "column": "profit"}] | [] | False |
| B2 | SUM(o.profit) | [{"table": "order_information", "column": "profit"}] | [] | False |
| B2 | COUNT(*) | [] | [] | True |


## S52

类别 `data`；来源 `python`；调用 `1d6bdaf37b494770a26e925852ade6fd`；状态 `success`。

```sql

WITH cust AS (SELECT "Customer ID", gender FROM customer_information GROUP BY "Customer ID")
SELECT o."Product", c.gender, COUNT(*) AS orders, SUM(o.profit) AS profit
FROM order_information o JOIN cust c ON o."Customer ID"=c."Customer ID"
WHERE o."Product Category" = 'Fashion'
GROUP BY o."Product", c.gender

```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-018/attempt-01/sql/S52.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-018/attempt-01/sql/S52.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-018/attempt-01/results/S52.rows.jsonl)；完整：True；SHA256：`a36b725ae2e75d70be3ddd3bde7940d1dd855283974cba7293a58067acf089a5`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "customer_information", "kind": "base", "block": null, "base_tables": ["customer_information"]}] | [] | ["\"Customer ID\""] |
| B2 | [{"alias": "o", "kind": "base", "block": null, "base_tables": ["order_information"]}, {"alias": "c", "kind": "derived", "block": "B1", "base_tables": ["customer_information"]}] | [{"type": "INNER", "right": "cust AS c", "on": "o.\"Customer ID\" = c.\"Customer ID\"", "using": []}] | ["o.\"Product\"", "c.gender"] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B2 | COUNT(*) | [] | [] | True |
| B2 | SUM(o.profit) | [{"table": "order_information", "column": "profit"}] | [] | False |


## S53

类别 `data`；来源 `query_db`；调用 `80633f76bf244b319b62460f0bac0104`；状态 `success`。

```sql
WITH cust AS (
  SELECT "Customer ID", gender FROM customer_information GROUP BY "Customer ID"
)
SELECT c.gender, strftime('%m', o."Order Date") AS month_num, o."Month" AS month_name,
  COUNT(*) AS orders, SUM(o.profit) AS profit
FROM order_information o JOIN cust c ON o."Customer ID"=c."Customer ID"
WHERE o."Product Category" = 'Fashion'
GROUP BY c.gender, month_num, month_name ORDER BY month_num, c.gender
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-018/attempt-01/sql/S53.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-018/attempt-01/sql/S53.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-018/attempt-01/results/S53.rows.jsonl)；完整：True；SHA256：`ae0d207bb58430654fc8a5a4ec3d4246f4f729f7dd1fb1727158653e53d260ae`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "customer_information", "kind": "base", "block": null, "base_tables": ["customer_information"]}] | [] | ["\"Customer ID\""] |
| B2 | [{"alias": "o", "kind": "base", "block": null, "base_tables": ["order_information"]}, {"alias": "c", "kind": "derived", "block": "B1", "base_tables": ["customer_information"]}] | [{"type": "INNER", "right": "cust AS c", "on": "o.\"Customer ID\" = c.\"Customer ID\"", "using": []}] | ["c.gender", "STRFTIME('%m', o.\"Order Date\")", "o.\"Month\""] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B2 | COUNT(*) | [] | [] | True |
| B2 | SUM(o.profit) | [{"table": "order_information", "column": "profit"}] | [] | False |


## S54

类别 `data`；来源 `query_db`；调用 `14fc8c05f0ef4d58b044fafdc8b375ba`；状态 `success`。

```sql
WITH cust AS (
  SELECT "Customer ID", gender FROM customer_information GROUP BY "Customer ID"
)
SELECT c.gender, CAST(o.Discount AS REAL) AS discount,
  COUNT(*) AS orders, SUM(o.profit) AS profit, AVG(o.profit) AS avg_profit
FROM order_information o JOIN cust c ON o."Customer ID"=c."Customer ID"
WHERE o."Product Category" = 'Fashion'
GROUP BY c.gender, discount ORDER BY c.gender, discount
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-018/attempt-01/sql/S54.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-018/attempt-01/sql/S54.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-018/attempt-01/results/S54.rows.jsonl)；完整：True；SHA256：`760b5091b4b7f25b3261ab8d2d59cf5eb25e92940194abdfc86a5f0c4017704a`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "customer_information", "kind": "base", "block": null, "base_tables": ["customer_information"]}] | [] | ["\"Customer ID\""] |
| B2 | [{"alias": "o", "kind": "base", "block": null, "base_tables": ["order_information"]}, {"alias": "c", "kind": "derived", "block": "B1", "base_tables": ["customer_information"]}] | [{"type": "INNER", "right": "cust AS c", "on": "o.\"Customer ID\" = c.\"Customer ID\"", "using": []}] | ["c.gender", "discount"] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B2 | COUNT(*) | [] | [] | True |
| B2 | SUM(o.profit) | [{"table": "order_information", "column": "profit"}] | [] | False |
| B2 | AVG(o.profit) | [{"table": "order_information", "column": "profit"}] | [] | False |


## S55

类别 `data`；来源 `python`；调用 `25dcbd81b9444dde831534b7a9803d5e`；状态 `success`。

```sql

WITH cust AS (SELECT "Customer ID", gender FROM customer_information GROUP BY "Customer ID")
SELECT c.gender, strftime('%m', o."Order Date") AS mm, SUM(o.profit) AS profit, COUNT(*) AS orders
FROM order_information o JOIN cust c ON o."Customer ID"=c."Customer ID"
WHERE o."Product Category" = 'Fashion'
GROUP BY c.gender, mm

```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-018/attempt-01/sql/S55.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-018/attempt-01/sql/S55.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-018/attempt-01/results/S55.rows.jsonl)；完整：True；SHA256：`dc0429c246795d8e660d9ac9dab73a9236cd7986c84368c143d23af8b2118466`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "customer_information", "kind": "base", "block": null, "base_tables": ["customer_information"]}] | [] | ["\"Customer ID\""] |
| B2 | [{"alias": "o", "kind": "base", "block": null, "base_tables": ["order_information"]}, {"alias": "c", "kind": "derived", "block": "B1", "base_tables": ["customer_information"]}] | [{"type": "INNER", "right": "cust AS c", "on": "o.\"Customer ID\" = c.\"Customer ID\"", "using": []}] | ["c.gender", "STRFTIME('%m', o.\"Order Date\")"] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B2 | SUM(o.profit) | [{"table": "order_information", "column": "profit"}] | [] | False |
| B2 | COUNT(*) | [] | [] | True |


## S56

类别 `data`；来源 `python`；调用 `25dcbd81b9444dde831534b7a9803d5e`；状态 `success`。

```sql

WITH cust AS (SELECT "Customer ID", gender, age FROM customer_information GROUP BY "Customer ID"),
cust_orders AS (SELECT "Customer ID", SUM(profit) AS profit FROM order_information WHERE "Product Category" = 'Fashion' GROUP BY "Customer ID")
SELECT c.gender, c.age, co.profit FROM cust c JOIN cust_orders co ON c."Customer ID"=co."Customer ID"

```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-018/attempt-01/sql/S56.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-018/attempt-01/sql/S56.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-018/attempt-01/results/S56.rows.jsonl)；完整：True；SHA256：`be5f0a6d5ff6132516dc0701eaeaa6e6652d4d009069c0d9f6495b0bd596b151`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "customer_information", "kind": "base", "block": null, "base_tables": ["customer_information"]}] | [] | ["\"Customer ID\""] |
| B2 | [{"alias": "order_information", "kind": "base", "block": null, "base_tables": ["order_information"]}] | [] | ["\"Customer ID\""] |
| B3 | [{"alias": "c", "kind": "derived", "block": "B1", "base_tables": ["customer_information"]}, {"alias": "co", "kind": "derived", "block": "B2", "base_tables": ["order_information"]}] | [{"type": "INNER", "right": "cust_orders AS co", "on": "c.\"Customer ID\" = co.\"Customer ID\"", "using": []}] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B2 | SUM(profit) | [{"table": "order_information", "column": "profit"}] | [] | False |


## S57

类别 `data`；来源 `query_db`；调用 `311c143cb451450caf3b8a7c0eaf6b2b`；状态 `success`。

```sql
WITH cust AS (
  SELECT "Customer ID", gender FROM customer_information GROUP BY "Customer ID"
)
SELECT c.gender, CAST(o.Discount AS REAL) AS discount, COUNT(*) AS orders, SUM(o.profit) AS profit,
  AVG(o.profit) AS avg_profit, SUM(o.Sales) AS sales
FROM order_information o JOIN cust c ON o."Customer ID"=c."Customer ID"
WHERE o."Product Category" = 'Fashion'
GROUP BY c.gender, discount ORDER BY c.gender, discount
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-018/attempt-01/sql/S57.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-018/attempt-01/sql/S57.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-018/attempt-01/results/S57.rows.jsonl)；完整：True；SHA256：`071bf84b93c03aa66ffa2f8ffd79623fab4a60de0193a7555a46f700758de8f6`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "customer_information", "kind": "base", "block": null, "base_tables": ["customer_information"]}] | [] | ["\"Customer ID\""] |
| B2 | [{"alias": "o", "kind": "base", "block": null, "base_tables": ["order_information"]}, {"alias": "c", "kind": "derived", "block": "B1", "base_tables": ["customer_information"]}] | [{"type": "INNER", "right": "cust AS c", "on": "o.\"Customer ID\" = c.\"Customer ID\"", "using": []}] | ["c.gender", "discount"] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B2 | COUNT(*) | [] | [] | True |
| B2 | SUM(o.profit) | [{"table": "order_information", "column": "profit"}] | [] | False |
| B2 | AVG(o.profit) | [{"table": "order_information", "column": "profit"}] | [] | False |
| B2 | SUM(o.Sales) | [{"table": "order_information", "column": "Sales"}] | [] | False |


## S58

类别 `data`；来源 `query_db`；调用 `9fc8cef8f2db4a6a8e6a71d15a16aa23`；状态 `success`。

```sql
WITH cust AS (
  SELECT "Customer ID", "Customer Segment", gender, age, "Education Level", "Marital Status", Region
  FROM customer_information GROUP BY "Customer ID"
),
cust_orders AS (
  SELECT "Customer ID", COUNT(*) AS orders, SUM(profit) AS profit, SUM(Sales) AS sales
  FROM order_information WHERE "Product Category" = 'Fashion' GROUP BY "Customer ID"
)
SELECT c.gender, c."Customer Segment", c.Region, c."Marital Status",
  COUNT(*) AS customers, SUM(co.orders) AS orders, SUM(co.profit) AS profit,
  SUM(co.profit)/COUNT(*) AS profit_per_customer, SUM(co.orders)/COUNT(*) AS orders_per_customer
FROM cust c JOIN cust_orders co ON c."Customer ID"=co."Customer ID"
GROUP BY c.gender, c."Customer Segment", c.Region, c."Marital Status"
ORDER BY profit_per_customer DESC
LIMIT 15
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-018/attempt-01/sql/S58.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-018/attempt-01/sql/S58.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-018/attempt-01/results/S58.rows.jsonl)；完整：True；SHA256：`a72edbbce52f2535aa8f5797141f4dfeb3550448d11f9f1a3093a947c9ee4527`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "customer_information", "kind": "base", "block": null, "base_tables": ["customer_information"]}] | [] | ["\"Customer ID\""] |
| B2 | [{"alias": "order_information", "kind": "base", "block": null, "base_tables": ["order_information"]}] | [] | ["\"Customer ID\""] |
| B3 | [{"alias": "c", "kind": "derived", "block": "B1", "base_tables": ["customer_information"]}, {"alias": "co", "kind": "derived", "block": "B2", "base_tables": ["order_information"]}] | [{"type": "INNER", "right": "cust_orders AS co", "on": "c.\"Customer ID\" = co.\"Customer ID\"", "using": []}] | ["c.gender", "c.\"Customer Segment\"", "c.Region", "c.\"Marital Status\""] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B2 | COUNT(*) | [] | [] | True |
| B2 | SUM(profit) | [{"table": "order_information", "column": "profit"}] | [] | False |
| B2 | SUM(Sales) | [{"table": "order_information", "column": "Sales"}] | [] | False |
| B3 | COUNT(*) | [] | [] | True |
| B3 | SUM(co.orders) | [] | [] | False |
| B3 | SUM(co.profit) | [{"table": "order_information", "column": "profit"}] | [] | False |
| B3 | SUM(co.profit) | [{"table": "order_information", "column": "profit"}] | [] | False |
| B3 | COUNT(*) | [] | [] | True |
| B3 | SUM(co.orders) | [] | [] | False |
| B3 | COUNT(*) | [] | [] | True |

