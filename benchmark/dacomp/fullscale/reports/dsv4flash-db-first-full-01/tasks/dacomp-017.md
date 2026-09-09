# dacomp-017

Using the metrics in `order_information`, analyze how the annual profit margin for each `P…

运行：已提交。官方未评分。全部 SQL 尝试/成功 71/71；数据 SQL 69/69；Python 13 次。

完整原题：

Using the metrics in `order_information`, analyze how the annual profit margin for each `Product Category` fluctuated from 2022 through 2024 by computing profit ÷ Sales at the category-by-year grain. Identify the category whose profit margin shows the largest swing, investigate the drivers of that volatility through the shipping, SKU, product, pricing, and engagement indicators available in `order_information` and `product_browsing`, and then build an RFM segmentation (Recency/Frequency/Monetary derived from `Order Date`, `Order ID`, and revenue or `profit`) to isolate the category’s core consumers and assess whether they are more sensitive to the identified fluctuation driver.

| 表 | 行数 | 列数 |
| --- | --- | --- |
| customer_information | 51289 | 11 |
| order_information | 51289 | 13 |
| product_browsing | 51289 | 7 |


实际路线（分析者依据 SQL/源码概括，不代表 Agent 自述）：按品类×年份计算利润率 → 针对波动品类检查折扣、数量、商品和浏览互动 → 构造客户 RFM 分层 → 比较分层消费者对波动因素的敏感性，并做数量情景和回归分析。

数据库大小：28,389,376 字节。

## 数据 SQL

| SQL | 状态 | 基础表 | Join 输入/类型 | GROUP BY | 聚合表达式 | 结果行数 | 数据库 ms |
| --- | --- | --- | --- | --- | --- | --- | --- |
| [S3/Q1](#s3) | success | ["order_information"] | 0 / {} | [] | [] | 20 | 0.658 |
| [S4/Q2](#s4) | success | ["product_browsing"] | 0 / {} | [] | [] | 20 | 0.388 |
| [S5/Q3](#s5) | success | ["order_information"] | 0 / {} | [] | ["COUNT(*)"] | 1 | 2.939 |
| [S6/Q4](#s6) | success | ["product_browsing"] | 0 / {} | [] | ["COUNT(*)"] | 1 | 1.226 |
| [S7/Q5](#s7) | success | ["order_information"] | 0 / {} | [] | [] | 4 | 6.688 |
| [S8/Q6](#s8) | success | ["order_information"] | 0 / {} | ["SUBSTRING(\"Order Date\", 1, 4)"] | ["COUNT(*)"] | 3 | 24.773 |
| [S9/Q7](#s9) | success | ["order_information"] | 0 / {} | ["\"Product Category\"", "SUBSTRING(\"Order Date\", 1, 4)"] | ["SUM(profit)", "SUM(Sales)", "SUM(Sales)", "SUM(profit)"] | 12 | 49.215 |
| [S10/Q8](#s10) | success | ["order_information"] | 0 / {} | ["\"Product Category\"", "SUBSTRING(\"Order Date\", 1, 4)"] | ["SUM(Sales)", "SUM(profit)"] | 12 | 48.312 |
| [S11/Q9](#s11) | success | ["order_information"] | 0 / {} | [] | [] | 6 | 17.104 |
| [S12/Q10](#s12) | success | ["order_information"] | 0 / {} | [] | [] | 7 | 27.628 |
| [S13/Q11](#s13) | success | ["order_information"] | 0 / {} | ["\"Product Category\"", "SUBSTRING(\"Order Date\", 1, 4)"] | ["SUM(CASE WHEN \"Discount\" = 'xxx' OR \"Quantity\" = 'abc' OR \"Quantity\" IS NULL THEN 1 ELSE 0 END)", "COUNT(*)"] | 12 | 48.866 |
| [S14/Q12](#s14) | success | ["order_information"] | 0 / {} | ["\"Product Category\"", "SUBSTRING(\"Order Date\", 1, 4)"] | ["SUM(CASE WHEN profit < 0 THEN 1 ELSE 0 END)", "COUNT(*)", "SUM(CASE WHEN profit < 0 THEN profit ELSE 0 END)"] | 12 | 47.62 |
| [S15/Q13](#s15) | success | ["order_information"] | 0 / {} | [] | ["MIN(profit)", "MAX(profit)", "MIN(Sales)", "MAX(Sales)"] | 1 | 11.328 |
| [S16/Q14](#s16) | success | ["order_information"] | 0 / {} | [] | [] | 0 | 6.085 |
| [S17/Q15](#s17) | success | ["order_information"] | 0 / {} | ["\"Discount\""] | ["COUNT(*)", "AVG(profit * 1.0 / Sales)"] | 5 | 9.717 |
| [S18/Q16](#s18) | success | ["order_information"] | 0 / {} | ["\"Shipping Method\""] | ["COUNT(*)", "SUM(profit)", "SUM(Sales)", "SUM(Sales)", "SUM(profit)"] | 1 | 8.875 |
| [S19/Q17](#s19) | success | ["order_information"] | 0 / {} | ["\"Discount\"", "SUBSTRING(\"Order Date\", 1, 4)"] | ["COUNT(*)", "AVG(profit * 1.0 / Sales)", "AVG(profit)", "AVG(Sales)"] | 15 | 14.297 |
| [S20/Q18](#s20) | success | ["order_information"] | 0 / {} | ["SUBSTRING(\"Order Date\", 1, 4)", "\"Discount\""] | ["COUNT(*)", "SUM(profit)", "SUM(Sales)", "SUM(Sales)", "SUM(profit)"] | 15 | 13.858 |
| [S21/Q19](#s21) | success | ["order_information"] | 0 / {} | ["\"Product\""] | ["COUNT(*)", "SUM(Sales)", "SUM(profit)", "SUM(Sales)", "SUM(profit)"] | 10 | 9.518 |
| [S22/Q20](#s22) | success | ["order_information"] | 0 / {} | [] | [] | 10 | 5.944 |
| [S23/Q21](#s23) | success | ["order_information"] | 0 / {} | ["\"Product\"", "SUBSTRING(\"Order Date\", 1, 4)"] | ["COUNT(*)", "SUM(Sales)", "SUM(profit)", "SUM(Sales)", "SUM(profit)"] | 30 | 13.616 |
| [S24/Q22](#s24) | success | ["order_information"] | 0 / {} | ["\"Product\"", "SUBSTRING(\"Order Date\", 1, 4)"] | ["COUNT(*)", "SUM(Sales)", "SUM(profit)", "SUM(Sales)", "SUM(profit)"] | 30 | 13.533 |
| [S25/Q23](#s25) | success | ["order_information"] | 0 / {} | ["yr", "\"Product\"", "\"Discount\""] | ["COUNT(*)", "SUM(Sales)"] | 150 | 16.369 |
| [S26/Q24](#s26) | success | ["order_information"] | 0 / {} | ["\"Product\"", "SUBSTRING(\"Order Date\", 1, 4)"] | ["SUM(Sales)", "SUM(Sales)", "SUM(Sales)"] | 30 | 12.728 |
| [S27/Q25](#s27) | success | ["order_information"] | 0 / {} | [] | [] | 10 | 1.69 |
| [S28/Q26](#s28) | success | ["order_information"] | 0 / {} | [] | [] | 20 | 1.857 |
| [S29/Q27](#s29) | success | ["order_information"] | 0 / {} | ["SUBSTRING(\"Order Date\", 1, 4)", "\"Discount\""] | ["COUNT(*)"] | 15 | 12.795 |
| [S30/Q28](#s30) | success | ["order_information"] | 0 / {} | ["SUBSTRING(\"Order Date\", 1, 4)", "\"Quantity\""] | ["COUNT(*)"] | 15 | 12.093 |
| [S31/Q29](#s31) | success | ["order_information"] | 0 / {} | ["SUBSTRING(\"Order Date\", 1, 4)", "\"Order Priority\""] | ["COUNT(*)"] | 9 | 11.248 |
| [S32/Q30](#s32) | success | ["order_information"] | 0 / {} | ["\"Quantity\"", "\"Discount\""] | ["COUNT(*)", "SUM(Sales)", "SUM(profit)", "SUM(Sales)", "SUM(profit)"] | 25 | 7.047 |
| [S33/Q31](#s33) | success | ["order_information"] | 0 / {} | [] | [] | 1 | 6.061 |
| [S34/Q32](#s34) | success | ["order_information"] | 0 / {} | ["\"Quantity\""] | ["COUNT(*)", "SUM(Sales)", "SUM(profit)", "SUM(Sales)", "SUM(profit)"] | 5 | 6.65 |
| [S35/Q33](#s35) | success | ["order_information"] | 0 / {} | ["SUBSTRING(\"Order Date\", 1, 4)", "\"Quantity\""] | ["COUNT(*)", "SUM(Sales)", "SUM(profit)", "SUM(Sales)", "SUM(profit)"] | 15 | 6.848 |
| [S36/Q34](#s36) | success | ["order_information"] | 0 / {} | [] | [] | 1 | 6.039 |
| [S37/Q35](#s37) | success | ["order_information"] | 0 / {} | ["\"Quantity\""] | ["COUNT(*)", "SUM(profit)", "SUM(Sales)", "SUM(Sales)", "SUM(profit)"] | 5 | 6.553 |
| [S38/Q36](#s38) | success | ["order_information"] | 0 / {} | ["SUBSTRING(\"Order Date\", 1, 4)", "\"Quantity\""] | ["COUNT(*)"] | 15 | 6.697 |
| [S39/Q37](#s39) | success | ["order_information"] | 0 / {} | ["SUBSTRING(\"Order Date\", 1, 4)", "\"Quantity\""] | ["COUNT(*)"] | 15 | 6.669 |
| [S40/Q38](#s40) | success | ["product_browsing"] | 0 / {} | ["pb.\"Product\""] | ["AVG(pb.\"Browsing Time (minutes)\")", "AVG(pb.\"like\")", "AVG(pb.\"share\")", "AVG(pb.\"Add to Cart\")"] | 10 | 9.217 |
| [S41/Q39](#s41) | success | ["product_browsing"] | 0 / {} | ["pb.\"Product\""] | ["COUNT(*)", "SUM(pb.\"like\")", "SUM(pb.\"share\")", "SUM(pb.\"Add to Cart\")"] | 10 | 8.569 |
| [S42/Q40](#s42) | success | ["order_information"] | 0 / {} | [] | ["MAX(\"Order Date\")", "MIN(\"Order Date\")"] | 1 | 7.719 |
| [S43/Q41](#s43) | success | ["order_information"] | 0 / {} | [] | ["COUNT(DISTINCT \"Customer ID\")"] | 1 | 8.952 |
| [S44/Q42](#s44) | success | ["order_information"] | 0 / {} | [] | ["COUNT(DISTINCT \"Order ID\")"] | 1 | 11.953 |
| [S45/Q43](#s45) | success | ["order_information"] | 0 / {} | ["\"Customer ID\""] | ["MAX(\"Order Date\")", "COUNT(DISTINCT \"Order ID\")", "SUM(profit)", "SUM(Sales)", "COUNT(*)", "SUM(\"Quantity\" * 1.0)"] | 15 | 15.712 |
| [S46/Q44](#s46) | success | ["order_information"] | 0 / {} | ["\"Customer ID\""] | ["MAX(\"Order Date\")", "COUNT(DISTINCT \"Order ID\")", "SUM(profit)", "SUM(Sales)", "COUNT(*)", "SUM(CAST(\"Quantity\" AS REAL))"] | 794 | 17.487 |
| [S47/Q45](#s47) | success | ["order_information"] | 0 / {} | ["\"Customer ID\"", "CASE WHEN R + F + M >= 10 THEN 'Top Tier' WHEN R + F + M >= 7 THEN 'Mid Tier' WHEN R + F + M >= 4 THEN 'Low Tier' ELSE 'Bottom Tier' END"] | ["MAX(\"Order Date\")", "COUNT(DISTINCT \"Order ID\")", "SUM(profit)", "COUNT(*)"] | 4 | 17.694 |
| [S48/Q46](#s48) | success | ["order_information"] | 0 / {} | [] | [] | 10309 | 25.74 |
| [S49/Q47](#s49) | success | ["order_information"] | 0 / {} | [] | [] | 51287 | 60.35 |
| [S50/Q48](#s50) | success | ["order_information"] | 0 / {} | [] | [] | 10309 | 19.081 |
| [S51/Q49](#s51) | success | ["order_information"] | 0 / {} | [] | [] | 10309 | 19.545 |
| [S52/Q50](#s52) | success | ["order_information"] | 0 / {} | [] | [] | 10309 | 19.279 |
| [S53/Q51](#s53) | success | ["order_information"] | 0 / {} | [] | [] | 30 | 6.266 |
| [S54/Q52](#s54) | success | ["order_information"] | 0 / {} | [] | [] | 30 | 6.262 |
| [S55/Q53](#s55) | success | ["order_information"] | 0 / {} | [] | [] | 1027 | 7.943 |
| [S56/Q54](#s56) | success | ["order_information"] | 0 / {} | [] | [] | 10309 | 19.687 |
| [S57/Q55](#s57) | success | ["order_information"] | 0 / {} | ["\"Product Category\"", "SUBSTRING(\"Order Date\", 1, 4)"] | ["SUM(Sales)", "SUM(profit)"] | 12 | 47.337 |
| [S58/Q56](#s58) | success | ["order_information"] | 0 / {} | ["\"Product\"", "SUBSTRING(\"Order Date\", 1, 4)"] | ["SUM(Sales)", "SUM(profit)"] | 30 | 13.197 |
| [S59/Q57](#s59) | success | ["order_information"] | 0 / {} | [] | [] | 10309 | 15.771 |
| [S60/Q58](#s60) | success | ["order_information"] | 0 / {} | [] | [] | 5000 | 7.102 |
| [S61/Q59](#s61) | success | ["order_information"] | 0 / {} | ["\"Product\"", "SUBSTRING(\"Order Date\", 1, 4)"] | ["SUM(Sales)"] | 30 | 12.853 |
| [S62/Q60](#s62) | success | ["order_information"] | 0 / {} | [] | [] | 10309 | 17.748 |
| [S63/Q61](#s63) | success | ["order_information"] | 0 / {} | [] | [] | 10309 | 16.869 |
| [S64/Q62](#s64) | success | ["product_browsing"] | 0 / {} | ["pb.\"Customer ID\""] | ["AVG(pb.\"Browsing Time (minutes)\")", "AVG(pb.\"like\")", "AVG(pb.\"share\")", "AVG(pb.\"Add to Cart\")"] | 794 | 12.221 |
| [S65/Q63](#s65) | success | ["order_information"] | 0 / {} | ["SUBSTRING(\"Order Date\", 1, 4)"] | ["AVG(CAST(\"Discount\" AS REAL))", "AVG(CAST(\"Quantity\" AS REAL) * CAST(\"Discount\" AS REAL))"] | 3 | 11.75 |
| [S66/Q64](#s66) | success | ["order_information"] | 0 / {} | ["\"Product\""] | ["AVG(CAST(\"Discount\" AS REAL))", "AVG(CAST(\"Quantity\" AS REAL) * CAST(\"Discount\" AS REAL))"] | 10 | 10.946 |
| [S67/Q65](#s67) | success | ["order_information"] | 0 / {} | [] | [] | 10309 | 17.33 |
| [S68/Q66](#s68) | success | ["order_information"] | 0 / {} | ["\"Product Category\"", "SUBSTRING(\"Order Date\", 1, 4)"] | ["SUM(Sales)", "SUM(profit)"] | 12 | 47.208 |
| [S69/Q67](#s69) | success | ["order_information"] | 0 / {} | ["\"Customer ID\""] | ["SUM(profit)", "SUM(Sales)"] | 794 | 11.215 |
| [S70/Q68](#s70) | success | ["order_information"] | 0 / {} | [] | ["COUNT(*)", "SUM(Sales)", "SUM(profit)"] | 1 | 5.915 |
| [S71/Q69](#s71) | success | ["order_information"] | 0 / {} | [] | ["COUNT(DISTINCT \"Order ID\")", "COUNT(*)"] | 1 | 11.128 |


## 元数据和设置

| SQL | 类别 | 状态 | 内容 |
| --- | --- | --- | --- |
| S1 | connection_setup | success | PRAGMA query_only=ON |
| S2 | metadata | success | SELECT name,sql FROM sqlite_master WHERE type='table' ORDER BY name |


## Python 与执行位置

人工源码审查：**database_first_violation**。SQL computes category-year margins and customer RFM inputs. Python then performs percentile/rank segmentation, year-by-segment aggregation, quantity/product means and arithmetic scenarios over exported results. Those operations are SQL-capable; regression, statistical tests and plotting are separately justified uses. The observed SQL trajectory excludes these actual Python computations; no equivalent SQL is invented. [证据](../reviews/dacomp-017.json)。

P1：RFM segmentation requires quartile binning, scoring, and segment labelling which is more naturally done in Python/pandas. We'll then analyze the top-tier customers' purchasing behavior (quantity per order) to assess sensitivity to the identified margin driver.

[源码](../../../runs/dsv4flash-db-first-full-01/dacomp-017/attempt-01/python/P1.py)；[输出](../../../runs/dsv4flash-db-first-full-01/dacomp-017/attempt-01/python/P1.stdout)；[错误](../../../runs/dsv4flash-db-first-full-01/dacomp-017/attempt-01/python/P1.stderr)。自动源码筛查未检出预设迁出信号；这不是全面语义合规证明。

P2：Check the correct path for the result archive file used by Python, since the relative path attempt failed.

[源码](../../../runs/dsv4flash-db-first-full-01/dacomp-017/attempt-01/python/P2.py)；[输出](../../../runs/dsv4flash-db-first-full-01/dacomp-017/attempt-01/python/P2.stdout)；[错误](../../../runs/dsv4flash-db-first-full-01/dacomp-017/attempt-01/python/P2.stderr)。自动源码筛查未检出预设迁出信号；这不是全面语义合规证明。

P3：RFM segmentation using quartile scoring and customer segment labelling. The full dataset is already fetched via SQL; only the 794 rows needed for RFM scoring are used.

[源码](../../../runs/dsv4flash-db-first-full-01/dacomp-017/attempt-01/python/P3.py)；[输出](../../../runs/dsv4flash-db-first-full-01/dacomp-017/attempt-01/python/P3.stdout)；[错误](../../../runs/dsv4flash-db-first-full-01/dacomp-017/attempt-01/python/P3.stderr)。自动源码筛查未检出预设迁出信号；这不是全面语义合规证明。

P4：Load the top customers list from Python output and query order-level metrics by year and customer segment to assess sensitivity to the quantity driver.

[源码](../../../runs/dsv4flash-db-first-full-01/dacomp-017/attempt-01/python/P4.py)；[输出](../../../runs/dsv4flash-db-first-full-01/dacomp-017/attempt-01/python/P4.stdout)；[错误](../../../runs/dsv4flash-db-first-full-01/dacomp-017/attempt-01/python/P4.stderr)。检出需人工核验的 SQL 可实现操作：groupby(, .query(；不能仅凭理由判为合规。

P5：Order-level analysis of Home & Furniture: compare average quantity per order and per-order margin between Top Tier RFM customers and others across years, using stats not supported by SQL (Welch t-test on quantity distributions).

[源码](../../../runs/dsv4flash-db-first-full-01/dacomp-017/attempt-01/python/P5.py)；[输出](../../../runs/dsv4flash-db-first-full-01/dacomp-017/attempt-01/python/P5.stdout)；[错误](../../../runs/dsv4flash-db-first-full-01/dacomp-017/attempt-01/python/P5.stderr)。检出需人工核验的 SQL 可实现操作：groupby(, .query(；不能仅凭理由判为合规。

P6：Verify the data-generating relationship between profit and Sales/Quantity across all categories (a check outside the SQL aggregation) and decompose the margin change for Home & Furniture into product-mix and within-product components.

[源码](../../../runs/dsv4flash-db-first-full-01/dacomp-017/attempt-01/python/P6.py)；[输出](../../../runs/dsv4flash-db-first-full-01/dacomp-017/attempt-01/python/P6.stdout)；[错误](../../../runs/dsv4flash-db-first-full-01/dacomp-017/attempt-01/python/P6.stderr)。检出需人工核验的 SQL 可实现操作：groupby(, .query(；不能仅凭理由判为合规。

P7：Debug the year column type issue causing NaN in the decomposition analysis.

[源码](../../../runs/dsv4flash-db-first-full-01/dacomp-017/attempt-01/python/P7.py)；[输出](../../../runs/dsv4flash-db-first-full-01/dacomp-017/attempt-01/python/P7.stdout)；[错误](../../../runs/dsv4flash-db-first-full-01/dacomp-017/attempt-01/python/P7.stderr)。检出需人工核验的 SQL 可实现操作：.query(；不能仅凭理由判为合规。

P8：Redo the decomposition with year converted to integer to avoid Arrow-backed string comparison issues, quantifying how much of the Home & Furniture margin decline comes from within-product quantity increases vs product-mix shifts.

[源码](../../../runs/dsv4flash-db-first-full-01/dacomp-017/attempt-01/python/P8.py)；[输出](../../../runs/dsv4flash-db-first-full-01/dacomp-017/attempt-01/python/P8.stdout)；[错误](../../../runs/dsv4flash-db-first-full-01/dacomp-017/attempt-01/python/P8.stderr)。检出需人工核验的 SQL 可实现操作：groupby(, .query(；不能仅凭理由判为合规。

P9：Fit the profit formula from the data (relationship among Sales, Quantity, Discount, profit) using Python regression, since SQLite is not suited to this statistical modeling step.

[源码](../../../runs/dsv4flash-db-first-full-01/dacomp-017/attempt-01/python/P9.py)；[输出](../../../runs/dsv4flash-db-first-full-01/dacomp-017/attempt-01/python/P9.stdout)；[错误](../../../runs/dsv4flash-db-first-full-01/dacomp-017/attempt-01/python/P9.stderr)。检出需人工核验的 SQL 可实现操作：groupby(, .query(；不能仅凭理由判为合规。

P10：Produce visualizations for the report: (1) profit margin by category and year, (2) Home & Furniture product-level margin decomposition, (3) RFM segment analysis of quantity sensitivity. These are graphical outputs not possible in SQL.

[源码](../../../runs/dsv4flash-db-first-full-01/dacomp-017/attempt-01/python/P10.py)；[输出](../../../runs/dsv4flash-db-first-full-01/dacomp-017/attempt-01/python/P10.stdout)；[错误](../../../runs/dsv4flash-db-first-full-01/dacomp-017/attempt-01/python/P10.stderr)。检出需人工核验的 SQL 可实现操作：groupby(, .query(；不能仅凭理由判为合规。

P11：Welch's t-test comparing Top Tier vs Other customer quantity per order across years, to assess statistical significance of the sensitivity difference.

[源码](../../../runs/dsv4flash-db-first-full-01/dacomp-017/attempt-01/python/P11.py)；[输出](../../../runs/dsv4flash-db-first-full-01/dacomp-017/attempt-01/python/P11.stdout)；[错误](../../../runs/dsv4flash-db-first-full-01/dacomp-017/attempt-01/python/P11.stderr)。检出需人工核验的 SQL 可实现操作：groupby(, .query(；不能仅凭理由判为合规。

P12：Final regression to quantify order-level margin sensitivity to Quantity and Discount for Home & Furniture (numpy lstsq, not available in SQL), confirming the driver magnitudes.

[源码](../../../runs/dsv4flash-db-first-full-01/dacomp-017/attempt-01/python/P12.py)；[输出](../../../runs/dsv4flash-db-first-full-01/dacomp-017/attempt-01/python/P12.stdout)；[错误](../../../runs/dsv4flash-db-first-full-01/dacomp-017/attempt-01/python/P12.stderr)。检出需人工核验的 SQL 可实现操作：groupby(, .query(；不能仅凭理由判为合规。

P13：Compile final summary statistics for the report: RFM tier characteristics, profit shares, and margin figures.

[源码](../../../runs/dsv4flash-db-first-full-01/dacomp-017/attempt-01/python/P13.py)；[输出](../../../runs/dsv4flash-db-first-full-01/dacomp-017/attempt-01/python/P13.stdout)；[错误](../../../runs/dsv4flash-db-first-full-01/dacomp-017/attempt-01/python/P13.stderr)。检出需人工核验的 SQL 可实现操作：groupby(, .query(；不能仅凭理由判为合规。

## 优化机会

已验证候选。筛选限于精确 SQL、相同自包含 CTE、相同单表完整过滤、可分解单表聚合；未覆盖任意 Join 等价和一般谓词蕴含。全部候选都是 offline，未测在线预测。

| 候选 | 类型 | 已有结果 | 覆盖 SQL | 后续次数 | 中间行数 | 验证 | 成本 |
| --- | --- | --- | --- | --- | --- | --- | --- |
| C1 | exact-result reuse | True | ["S50", "S51", "S52"] | 2 | unknown | not_verified_cap | Not tested |
| C2 | exact-result reuse | True | ["S59", "S62"] | 1 | unknown | not_verified_cap | Not tested |
| C3 | aggregate MV | False | ["S5", "S8", "S9", "S10", "S13", "S14", "S42", "S57", "S68"] | 8 | 12 | verified | Not benchmarked; correctness alone does not establish net speedup. |
| C4 | common filtered view | False | ["S17", "S18", "S19", "S20", "S21", "S22", "S23", "S28", "S29", "S30", "S31", "S43", "S44", "S58", "S61", "S63", "S69", "S70", "S71"] | 18 | 10309 | verified | Not benchmarked; correctness alone does not establish net speedup. |
| C5 | aggregate MV | False | ["S17", "S18", "S19", "S20", "S21", "S23", "S29", "S30", "S31", "S58", "S61", "S69", "S70"] | 12 | 10259 | rejected_result_mismatch | Not benchmarked; correctness alone does not establish net speedup. |
| C6 | common filtered view | False | ["S27", "S32", "S33", "S34", "S35", "S38"] | 5 | unknown | not_verified_cap | Not tested |
| C7 | aggregate MV | False | ["S32", "S34", "S35", "S38"] | 3 | unknown | not_verified_cap | Not tested |
| C8 | common filtered view | False | ["S36", "S37", "S39"] | 2 | unknown | not_verified_cap | Not tested |
| C9 | aggregate MV | False | ["S37", "S39"] | 1 | unknown | not_verified_cap | Not tested |
| C10 | common filtered view | False | ["S40", "S41", "S64"] | 2 | unknown | not_verified_cap | Not tested |
| C11 | common filtered view | False | ["S48", "S50", "S51", "S52", "S59", "S62"] | 5 | unknown | not_verified_cap | Not tested |
| C12 | common filtered view | False | ["S53", "S55"] | 1 | unknown | not_verified_cap | Not tested |
| C13 | common filtered view | False | ["S56", "S60", "S67"] | 2 | unknown | not_verified_cap | Not tested |
| C14 | common filtered view | False | ["S65", "S66"] | 1 | unknown | not_verified_cap | Not tested |
| C15 | aggregate MV | False | ["S65", "S66"] | 1 | unknown | not_verified_cap | Not tested |


已验证覆盖（含触发查询、候选并集去重）：28/69 条成功数据 SQL。正确性仅针对当前数据库快照；未测性能的候选不能声称已加速。

[完整 build/rewrite 与比较证据](dacomp-017.analysis.json)。

### C4：common filtered view

Same single source and complete filter; original filter retained.

原查询 [S17](#s17), [S18](#s18), [S19](#s19), [S20](#s20), [S21](#s21), [S22](#s22), [S23](#s23), [S28](#s28), [S29](#s29), [S30](#s30), [S31](#s31), [S43](#s43), [S44](#s44), [S58](#s58), [S61](#s61), [S63](#s63), [S69](#s69), [S70](#s70), [S71](#s71) → 新增共享状态 C4 → 后续 18 次可复用。该构建点为事后假设，不代表 Agent 当时预知后续。

构建定义：

```sql
SELECT * FROM "order_information" WHERE "Product Category" = 'Home & Furniture'
```

受益查询 S17 的改写示例：

```sql
SELECT "Discount", COUNT(*) AS n, ROUND(AVG(profit * 1.0 / Sales), 4) AS avg_margin FROM temp.reuse_candidate AS order_information WHERE "Product Category" = 'Home & Furniture' GROUP BY "Discount" ORDER BY "Discount"
```

| 原 SQL | 列名一致 | 结果一致 | 比较方法 |
| --- | --- | --- | --- |
| S17 | True | True | ordered_numeric_tolerance |
| S18 | True | True | ordered_numeric_tolerance |
| S19 | True | True | ordered_numeric_tolerance |
| S20 | True | True | ordered_numeric_tolerance |
| S21 | True | True | ordered_numeric_tolerance |
| S22 | True | True | exact_multiset |
| S23 | True | True | ordered_numeric_tolerance |
| S28 | True | True | exact_multiset |
| S29 | True | True | ordered_numeric_tolerance |
| S30 | True | True | ordered_numeric_tolerance |
| S31 | True | True | ordered_numeric_tolerance |
| S43 | True | True | exact_multiset |
| S44 | True | True | exact_multiset |
| S58 | True | True | ordered_numeric_tolerance |
| S61 | True | True | ordered_numeric_tolerance |
| S63 | True | True | exact_multiset |
| S69 | True | True | exact_multiset |
| S70 | True | True | exact_multiset |
| S71 | True | True | exact_multiset |


验证状态：verified；成本结论：Not benchmarked; correctness alone does not establish net speedup.

### C3：aggregate MV

Union of grouping keys; decomposable aggregate states; AVG uses SUM and non-NULL COUNT.

原查询 [S5](#s5), [S8](#s8), [S9](#s9), [S10](#s10), [S13](#s13), [S14](#s14), [S42](#s42), [S57](#s57), [S68](#s68) → 新增共享状态 C3 → 后续 8 次可复用。该构建点为事后假设，不代表 Agent 当时预知后续。

构建定义：

```sql
SELECT SUBSTRING("Order Date", 1, 4) AS __g0, "Product Category" AS __g1, COUNT(*) AS __a0, SUM(profit) AS __a1, SUM(sales) AS __a2, SUM(CASE WHEN "Discount" = 'xxx' OR "Quantity" = 'abc' OR "Quantity" IS NULL THEN 1 ELSE 0 END) AS __a3, SUM(CASE WHEN profit < 0 THEN 1 ELSE 0 END) AS __a4, SUM(CASE WHEN profit < 0 THEN profit ELSE 0 END) AS __a5, MAX("Order Date") AS __a6, MIN("Order Date") AS __a7 FROM "order_information"  GROUP BY SUBSTRING("Order Date", 1, 4), "Product Category"
```

受益查询 S5 的改写示例：

```sql
SELECT SUM(__a0) AS n FROM temp.reuse_candidate
```

| 原 SQL | 列名一致 | 结果一致 | 比较方法 |
| --- | --- | --- | --- |
| S5 | True | True | exact_multiset |
| S8 | True | True | exact_multiset |
| S9 | True | True | ordered_numeric_tolerance |
| S10 | True | True | ordered_numeric_tolerance |
| S13 | True | True | ordered_numeric_tolerance |
| S14 | True | True | ordered_numeric_tolerance |
| S42 | True | True | exact_multiset |
| S57 | True | True | ordered_numeric_tolerance |
| S68 | True | True | ordered_numeric_tolerance |


验证状态：verified；成本结论：Not benchmarked; correctness alone does not establish net speedup.

### C5：aggregate MV

Union of grouping keys; decomposable aggregate states; AVG uses SUM and non-NULL COUNT.

原查询 [S17](#s17), [S18](#s18), [S19](#s19), [S20](#s20), [S21](#s21), [S23](#s23), [S29](#s29), [S30](#s30), [S31](#s31), [S58](#s58), [S61](#s61), [S69](#s69), [S70](#s70) → 新增共享状态 C5 → 后续 12 次可复用。该构建点为事后假设，不代表 Agent 当时预知后续。

构建定义：

```sql
SELECT "Discount" AS __g0, "Shipping Method" AS __g1, SUBSTRING("Order Date", 1, 4) AS __g2, "Product" AS __g3, "Quantity" AS __g4, "Order Priority" AS __g5, "Customer ID" AS __g6, COUNT(*) AS __a0, SUM(profit * 1.0 / sales) AS __a1_sum, COUNT(profit * 1.0 / sales) AS __a1_n, SUM(profit) AS __a2, SUM(sales) AS __a3, SUM(profit) AS __a4_sum, COUNT(profit) AS __a4_n, SUM(sales) AS __a5_sum, COUNT(sales) AS __a5_n FROM "order_information" WHERE "Product Category" = 'Home & Furniture' GROUP BY "Discount", "Shipping Method", SUBSTRING("Order Date", 1, 4), "Product", "Quantity", "Order Priority", "Customer ID"
```

受益查询 S17 的改写示例：

```sql
SELECT __g0 AS "Discount", SUM(__a0) AS n, ROUND((1.0 * SUM(__a1_sum) / NULLIF(SUM(__a1_n), 0)), 4) AS avg_margin FROM temp.reuse_candidate GROUP BY __g0 ORDER BY __g0
```

| 原 SQL | 列名一致 | 结果一致 | 比较方法 |
| --- | --- | --- | --- |
| S17 | True | True | ordered_numeric_tolerance |
| S18 | True | True | ordered_numeric_tolerance |
| S19 | True | True | ordered_numeric_tolerance |
| S20 | True | True | ordered_numeric_tolerance |
| S21 | True | True | ordered_numeric_tolerance |
| S23 | True | True | ordered_numeric_tolerance |
| S29 | True | True | ordered_numeric_tolerance |
| S30 | True | True | ordered_numeric_tolerance |
| S31 | True | True | ordered_numeric_tolerance |
| S58 | True | True | ordered_numeric_tolerance |
| S61 | True | True | ordered_numeric_tolerance |
| S69 | True | False | exact_multiset |
| S70 | True | False | exact_multiset |


验证状态：rejected_result_mismatch；成本结论：Not benchmarked; correctness alone does not establish net speedup.

结果依赖：自动记录 SQL→Python 的接口父调用，以及源码中引用归档文件的消费者；字面值相同不认定因果。模型方向选择需要人工读取消息，尚未做全面因果标注。

[原始报告](../../../runs/dsv4flash-db-first-full-01/dacomp-017/attempt-01/answer.md)；[统一消息](../../../runs/dsv4flash-db-first-full-01/dacomp-017/attempt-01/messages.jsonl)；[原始 OpenCode 事件](../../../runs/dsv4flash-db-first-full-01/dacomp-017/attempt-01/opencode.jsonl)；[SQL 引擎日志](../../../runs/dsv4flash-db-first-full-01/dacomp-017/attempt-01/sql_journal.jsonl)。

[可读报告（本地图片链接规范化）](../answers/dacomp-017.md)。原始回答保留，分析结论未改写。

## S1

类别 `connection_setup`；来源 `connection`；调用 `13bf0b44e55c41488d2b1115e5cbd98d`；状态 `success`。

```sql
PRAGMA query_only=ON
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-017/attempt-01/sql/S1.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-017/attempt-01/sql/S1.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-017/attempt-01/results/S1.rows.jsonl)；完整：True；SHA256：`e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`。

## S2

类别 `metadata`；来源 `list_db`；调用 `13bf0b44e55c41488d2b1115e5cbd98d`；状态 `success`。

```sql
SELECT name,sql FROM sqlite_master WHERE type='table' ORDER BY name
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-017/attempt-01/sql/S2.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-017/attempt-01/sql/S2.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-017/attempt-01/results/S2.rows.jsonl)；完整：True；SHA256：`65468faae86d39a48f884b13bd510f5ebed47a911d291b1e25fa15a19f7da006`。

## S3

类别 `data`；来源 `query_db`；调用 `2feb1494c20a48b79049f2e5ff384a49`；状态 `success`。

```sql
SELECT * FROM order_information LIMIT 20
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-017/attempt-01/sql/S3.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-017/attempt-01/sql/S3.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-017/attempt-01/results/S3.rows.jsonl)；完整：True；SHA256：`a97703d84648201563002cde99bf290858354ae750e05ec3977594ab1226b052`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "order_information", "kind": "base", "block": null, "base_tables": ["order_information"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |


## S4

类别 `data`；来源 `query_db`；调用 `61da895c1b47436ba5b7aeff37a00f95`；状态 `success`。

```sql
SELECT * FROM product_browsing LIMIT 20
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-017/attempt-01/sql/S4.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-017/attempt-01/sql/S4.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-017/attempt-01/results/S4.rows.jsonl)；完整：True；SHA256：`4e52c2392a6a43ee6ff0d2fede2fbee6d7ab68d6a31d3f0c07a7f993c0ec6054`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "product_browsing", "kind": "base", "block": null, "base_tables": ["product_browsing"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |


## S5

类别 `data`；来源 `query_db`；调用 `9093521141f048d393642b1a5fa87dc6`；状态 `success`。

```sql
SELECT COUNT(*) AS n FROM order_information
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-017/attempt-01/sql/S5.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-017/attempt-01/sql/S5.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-017/attempt-01/results/S5.rows.jsonl)；完整：True；SHA256：`eb6e48656c821597ccb27738e3c2488ee9df4a315c5100bfa7cd031a317aef4e`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "order_information", "kind": "base", "block": null, "base_tables": ["order_information"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |


## S6

类别 `data`；来源 `query_db`；调用 `88f237e10e8d4c7a91dc29cb93f7d815`；状态 `success`。

```sql
SELECT COUNT(*) AS n FROM product_browsing
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-017/attempt-01/sql/S6.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-017/attempt-01/sql/S6.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-017/attempt-01/results/S6.rows.jsonl)；完整：True；SHA256：`eb6e48656c821597ccb27738e3c2488ee9df4a315c5100bfa7cd031a317aef4e`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "product_browsing", "kind": "base", "block": null, "base_tables": ["product_browsing"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |


## S7

类别 `data`；来源 `query_db`；调用 `7a182abe5a944f10b6bd8b8a81ae1ddc`；状态 `success`。

```sql
SELECT DISTINCT "Product Category" FROM order_information
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-017/attempt-01/sql/S7.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-017/attempt-01/sql/S7.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-017/attempt-01/results/S7.rows.jsonl)；完整：True；SHA256：`3c96a6f1661d37195d683029d224d1f99e4381aea1c6a4aa5cf98a7a97e2dd30`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "order_information", "kind": "base", "block": null, "base_tables": ["order_information"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |


## S8

类别 `data`；来源 `query_db`；调用 `e91e9f2fca3542998a44cb5fe8ff40f5`；状态 `success`。

```sql
SELECT substr("Order Date",1,4) AS yr, COUNT(*) AS n FROM order_information GROUP BY yr
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-017/attempt-01/sql/S8.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-017/attempt-01/sql/S8.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-017/attempt-01/results/S8.rows.jsonl)；完整：True；SHA256：`f970e8eb9c847074105bd39b935167705aa0d862db6e54837578755d41bc95d4`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "order_information", "kind": "base", "block": null, "base_tables": ["order_information"]}] | [] | ["SUBSTRING(\"Order Date\", 1, 4)"] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |


## S9

类别 `data`；来源 `query_db`；调用 `910032c7ea254663a20f0792fe7c5b61`；状态 `success`。

```sql
SELECT "Product Category", 
       substr("Order Date",1,4) AS yr,
       SUM(profit) AS total_profit,
       SUM(Sales) AS total_sales,
       ROUND(SUM(profit)*1.0/SUM(Sales), 4) AS profit_margin
FROM order_information
GROUP BY "Product Category", yr
ORDER BY "Product Category", yr
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-017/attempt-01/sql/S9.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-017/attempt-01/sql/S9.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-017/attempt-01/results/S9.rows.jsonl)；完整：True；SHA256：`d6f362fde6773d106037e7da31c4a1854d92b80cd1f22115a508d61ec66aeaff`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "order_information", "kind": "base", "block": null, "base_tables": ["order_information"]}] | [] | ["\"Product Category\"", "SUBSTRING(\"Order Date\", 1, 4)"] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | SUM(profit) | [{"table": "order_information", "column": "profit"}] | [] | False |
| B1 | SUM(Sales) | [{"table": "order_information", "column": "Sales"}] | [] | False |
| B1 | SUM(Sales) | [{"table": "order_information", "column": "Sales"}] | [] | False |
| B1 | SUM(profit) | [{"table": "order_information", "column": "profit"}] | [] | False |


## S10

类别 `data`；来源 `query_db`；调用 `d2eaccfa7ad048fca1b700d992b01b15`；状态 `success`。

```sql
SELECT "Product Category",
       substr("Order Date",1,4) AS yr,
       ROUND(SUM(profit)*1.0/SUM(Sales),6) AS pm
FROM order_information
GROUP BY "Product Category", yr
ORDER BY "Product Category", yr
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-017/attempt-01/sql/S10.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-017/attempt-01/sql/S10.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-017/attempt-01/results/S10.rows.jsonl)；完整：True；SHA256：`df554bd020ed00f0fc83398863d9ddeac950b82b4d73f5e89687a4b775c24a80`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "order_information", "kind": "base", "block": null, "base_tables": ["order_information"]}] | [] | ["\"Product Category\"", "SUBSTRING(\"Order Date\", 1, 4)"] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | SUM(Sales) | [{"table": "order_information", "column": "Sales"}] | [] | False |
| B1 | SUM(profit) | [{"table": "order_information", "column": "profit"}] | [] | False |


## S11

类别 `data`；来源 `query_db`；调用 `78dfce7a304741adab84723cd9a56533`；状态 `success`。

```sql
SELECT DISTINCT "Discount" FROM order_information ORDER BY "Discount"
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-017/attempt-01/sql/S11.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-017/attempt-01/sql/S11.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-017/attempt-01/results/S11.rows.jsonl)；完整：True；SHA256：`b76c8256d8455a7b418e6373ccc3ccc84d78a020cbc754806cd4d2119a55286b`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "order_information", "kind": "base", "block": null, "base_tables": ["order_information"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |


## S12

类别 `data`；来源 `query_db`；调用 `3ea6291bdd8942f69bfecc79fba91f5a`；状态 `success`。

```sql
SELECT DISTINCT "Quantity" FROM order_information ORDER BY "Quantity"
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-017/attempt-01/sql/S12.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-017/attempt-01/sql/S12.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-017/attempt-01/results/S12.rows.jsonl)；完整：True；SHA256：`d3099d3e26fef591d3c4efae08055026c9559481ed18f5bf2ca64e103b3abb7a`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "order_information", "kind": "base", "block": null, "base_tables": ["order_information"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |


## S13

类别 `data`；来源 `query_db`；调用 `3df10cf47adc43fca9cbec216e4cddff`；状态 `success`。

```sql
SELECT "Product Category", substr("Order Date",1,4) AS yr,
  SUM(CASE WHEN "Discount"='xxx' OR "Quantity"='abc' OR "Quantity" IS NULL THEN 1 ELSE 0 END) AS bad_rows,
  COUNT(*) AS n
FROM order_information GROUP BY "Product Category", yr
ORDER BY "Product Category", yr
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-017/attempt-01/sql/S13.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-017/attempt-01/sql/S13.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-017/attempt-01/results/S13.rows.jsonl)；完整：True；SHA256：`6c991266530d2354b4000772827af170dd435a3ca191bcec0f3a26ae4832ca22`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "order_information", "kind": "base", "block": null, "base_tables": ["order_information"]}] | [] | ["\"Product Category\"", "SUBSTRING(\"Order Date\", 1, 4)"] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | SUM(CASE WHEN "Discount" = 'xxx' OR "Quantity" = 'abc' OR "Quantity" IS NULL THEN 1 ELSE 0 END) | [] | [{"table": "order_information", "column": "Quantity"}, {"table": "order_information", "column": "Discount"}, {"table": "order_information", "column": "Quantity"}] | False |
| B1 | COUNT(*) | [] | [] | True |


## S14

类别 `data`；来源 `query_db`；调用 `1206bb7d11bd40cd9993b047247e5e95`；状态 `success`。

```sql
SELECT "Product Category", substr("Order Date",1,4) AS yr,
  SUM(CASE WHEN profit<0 THEN 1 ELSE 0 END) AS neg_rows,
  COUNT(*) AS n,
  SUM(CASE WHEN profit<0 THEN profit ELSE 0 END) AS neg_profit
FROM order_information GROUP BY "Product Category", yr
ORDER BY "Product Category", yr
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-017/attempt-01/sql/S14.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-017/attempt-01/sql/S14.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-017/attempt-01/results/S14.rows.jsonl)；完整：True；SHA256：`d6872fcdedde701e4af0e4e241793c56e88e42e5b4c2133aa721b5802d4ce05c`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "order_information", "kind": "base", "block": null, "base_tables": ["order_information"]}] | [] | ["\"Product Category\"", "SUBSTRING(\"Order Date\", 1, 4)"] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | SUM(CASE WHEN profit < 0 THEN 1 ELSE 0 END) | [] | [{"table": "order_information", "column": "profit"}] | False |
| B1 | COUNT(*) | [] | [] | True |
| B1 | SUM(CASE WHEN profit < 0 THEN profit ELSE 0 END) | [{"table": "order_information", "column": "profit"}] | [{"table": "order_information", "column": "profit"}] | False |


## S15

类别 `data`；来源 `query_db`；调用 `064df375169e4a5787b49ad5b3df449a`；状态 `success`。

```sql
SELECT MIN(profit), MAX(profit), MIN(Sales), MAX(Sales) FROM order_information
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-017/attempt-01/sql/S15.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-017/attempt-01/sql/S15.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-017/attempt-01/results/S15.rows.jsonl)；完整：True；SHA256：`ebdf8bb10640bdd78927fa41f80154c77ac002d3dfef3d6278f41a62cb9b6a47`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "order_information", "kind": "base", "block": null, "base_tables": ["order_information"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | MIN(profit) | [{"table": "order_information", "column": "profit"}] | [] | False |
| B1 | MAX(profit) | [{"table": "order_information", "column": "profit"}] | [] | False |
| B1 | MIN(Sales) | [{"table": "order_information", "column": "Sales"}] | [] | False |
| B1 | MAX(Sales) | [{"table": "order_information", "column": "Sales"}] | [] | False |


## S16

类别 `data`；来源 `query_db`；调用 `18ff209546a644c68bc4ad0f62453136`；状态 `success`。

```sql
SELECT "Order ID", "Product Category", "Product", Sales, "Discount", profit, profit*1.0/Sales AS order_margin
FROM order_information
WHERE "Product Category" = 'Home & Furniture' AND "Discount" = 'xxx'
LIMIT 20
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-017/attempt-01/sql/S16.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-017/attempt-01/sql/S16.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-017/attempt-01/results/S16.rows.jsonl)；完整：True；SHA256：`e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "order_information", "kind": "base", "block": null, "base_tables": ["order_information"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |


## S17

类别 `data`；来源 `query_db`；调用 `2f646351171649538c9b0fdef948cabb`；状态 `success`。

```sql
SELECT "Discount", COUNT(*) AS n, ROUND(AVG(profit*1.0/Sales),4) AS avg_margin
FROM order_information
WHERE "Product Category" = 'Home & Furniture'
GROUP BY "Discount"
ORDER BY "Discount"
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-017/attempt-01/sql/S17.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-017/attempt-01/sql/S17.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-017/attempt-01/results/S17.rows.jsonl)；完整：True；SHA256：`361c067891e829a67682d137b25cfae6b6bd2d7fd0cad397a0d98f4ab5d4a1a6`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "order_information", "kind": "base", "block": null, "base_tables": ["order_information"]}] | [] | ["\"Discount\""] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |
| B1 | AVG(profit * 1.0 / Sales) | [{"table": "order_information", "column": "Sales"}, {"table": "order_information", "column": "profit"}] | [] | False |


## S18

类别 `data`；来源 `query_db`；调用 `51624a06c61d4fe693b3bc485dab0a3b`；状态 `success`。

```sql
SELECT "Shipping Method", COUNT(*) AS n, 
       SUM(profit) AS total_profit, SUM(Sales) AS total_sales,
       ROUND(SUM(profit)*1.0/SUM(Sales),4) AS margin
FROM order_information
WHERE "Product Category" = 'Home & Furniture'
GROUP BY "Shipping Method"
ORDER BY "Shipping Method"
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-017/attempt-01/sql/S18.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-017/attempt-01/sql/S18.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-017/attempt-01/results/S18.rows.jsonl)；完整：True；SHA256：`78d3b04f80c039b5195548ce2b00f6853e9e517a7d278e10954f294b1ce74634`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "order_information", "kind": "base", "block": null, "base_tables": ["order_information"]}] | [] | ["\"Shipping Method\""] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |
| B1 | SUM(profit) | [{"table": "order_information", "column": "profit"}] | [] | False |
| B1 | SUM(Sales) | [{"table": "order_information", "column": "Sales"}] | [] | False |
| B1 | SUM(Sales) | [{"table": "order_information", "column": "Sales"}] | [] | False |
| B1 | SUM(profit) | [{"table": "order_information", "column": "profit"}] | [] | False |


## S19

类别 `data`；来源 `query_db`；调用 `20b5e50be7f748b3a625fc1efba253d2`；状态 `success`。

```sql
SELECT "Discount", 
       substr("Order Date",1,4) AS yr,
       COUNT(*) AS n,
       AVG(profit*1.0/Sales) AS avg_margin,
       AVG(profit) AS avg_profit,
       AVG(Sales) AS avg_sales
FROM order_information
WHERE "Product Category" = 'Home & Furniture'
GROUP BY "Discount", yr
ORDER BY "Discount", yr
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-017/attempt-01/sql/S19.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-017/attempt-01/sql/S19.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-017/attempt-01/results/S19.rows.jsonl)；完整：True；SHA256：`6a8318d96f1898acad3bf51b836262506a88a4db85a065c32be92020492f83d5`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "order_information", "kind": "base", "block": null, "base_tables": ["order_information"]}] | [] | ["\"Discount\"", "SUBSTRING(\"Order Date\", 1, 4)"] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |
| B1 | AVG(profit * 1.0 / Sales) | [{"table": "order_information", "column": "Sales"}, {"table": "order_information", "column": "profit"}] | [] | False |
| B1 | AVG(profit) | [{"table": "order_information", "column": "profit"}] | [] | False |
| B1 | AVG(Sales) | [{"table": "order_information", "column": "Sales"}] | [] | False |


## S20

类别 `data`；来源 `query_db`；调用 `39f3810c0d7d4662a90230e5b23a8104`；状态 `success`。

```sql
SELECT substr("Order Date",1,4) AS yr,
       "Discount",
       COUNT(*) AS n,
       ROUND(SUM(profit),1) AS total_profit,
       ROUND(SUM(Sales),1) AS total_sales,
       ROUND(SUM(profit)*1.0/SUM(Sales),6) AS margin
FROM order_information
WHERE "Product Category" = 'Home & Furniture'
GROUP BY yr, "Discount"
ORDER BY yr, "Discount"
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-017/attempt-01/sql/S20.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-017/attempt-01/sql/S20.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-017/attempt-01/results/S20.rows.jsonl)；完整：True；SHA256：`29486a56ed9afe335bad5caf426e7f1831e85fef9ed018b77252d573d1f174c3`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "order_information", "kind": "base", "block": null, "base_tables": ["order_information"]}] | [] | ["SUBSTRING(\"Order Date\", 1, 4)", "\"Discount\""] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |
| B1 | SUM(profit) | [{"table": "order_information", "column": "profit"}] | [] | False |
| B1 | SUM(Sales) | [{"table": "order_information", "column": "Sales"}] | [] | False |
| B1 | SUM(Sales) | [{"table": "order_information", "column": "Sales"}] | [] | False |
| B1 | SUM(profit) | [{"table": "order_information", "column": "profit"}] | [] | False |


## S21

类别 `data`；来源 `query_db`；调用 `d3b98d8e51034fd6bb24a80792963206`；状态 `success`。

```sql
SELECT "Product", COUNT(*) AS n, SUM(Sales) AS total_sales, SUM(profit) AS total_profit,
       ROUND(SUM(profit)*1.0/SUM(Sales),6) AS margin
FROM order_information
WHERE "Product Category" = 'Home & Furniture'
GROUP BY "Product"
ORDER BY margin
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-017/attempt-01/sql/S21.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-017/attempt-01/sql/S21.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-017/attempt-01/results/S21.rows.jsonl)；完整：True；SHA256：`bbc31f90177070a13fa786133913ec826cdddef77c9483f4e87c8c28478bfc4f`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "order_information", "kind": "base", "block": null, "base_tables": ["order_information"]}] | [] | ["\"Product\""] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |
| B1 | SUM(Sales) | [{"table": "order_information", "column": "Sales"}] | [] | False |
| B1 | SUM(profit) | [{"table": "order_information", "column": "profit"}] | [] | False |
| B1 | SUM(Sales) | [{"table": "order_information", "column": "Sales"}] | [] | False |
| B1 | SUM(profit) | [{"table": "order_information", "column": "profit"}] | [] | False |


## S22

类别 `data`；来源 `query_db`；调用 `c735d5bef8604b259a4e7ee560ea51e8`；状态 `success`。

```sql
SELECT DISTINCT "Product" FROM order_information WHERE "Product Category" = 'Home & Furniture'
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-017/attempt-01/sql/S22.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-017/attempt-01/sql/S22.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-017/attempt-01/results/S22.rows.jsonl)；完整：True；SHA256：`b76252fa8e08c1f775cb82ae1e9f85e8d92748318715ddb0ab10c7c270fb746a`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "order_information", "kind": "base", "block": null, "base_tables": ["order_information"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |


## S23

类别 `data`；来源 `query_db`；调用 `c42010abadb74b76805b49590112d1d5`；状态 `success`。

```sql
SELECT "Product", substr("Order Date",1,4) AS yr,
       COUNT(*) AS n,
       ROUND(SUM(Sales),0) AS total_sales,
       ROUND(SUM(profit),1) AS total_profit,
       ROUND(SUM(profit)*1.0/SUM(Sales),4) AS margin
FROM order_information
WHERE "Product Category" = 'Home & Furniture'
GROUP BY "Product", yr
ORDER BY "Product", yr
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-017/attempt-01/sql/S23.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-017/attempt-01/sql/S23.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-017/attempt-01/results/S23.rows.jsonl)；完整：True；SHA256：`4bf879bf2375ac32b4dbd6ae1e7dc8f4758bef0b29ca84d9c69d45e51c3a533b`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "order_information", "kind": "base", "block": null, "base_tables": ["order_information"]}] | [] | ["\"Product\"", "SUBSTRING(\"Order Date\", 1, 4)"] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |
| B1 | SUM(Sales) | [{"table": "order_information", "column": "Sales"}] | [] | False |
| B1 | SUM(profit) | [{"table": "order_information", "column": "profit"}] | [] | False |
| B1 | SUM(Sales) | [{"table": "order_information", "column": "Sales"}] | [] | False |
| B1 | SUM(profit) | [{"table": "order_information", "column": "profit"}] | [] | False |


## S24

类别 `data`；来源 `query_db`；调用 `9e5445d3612e4139bac9c0d8cd8f470a`；状态 `success`。

```sql
SELECT * FROM (
  SELECT "Product", substr("Order Date",1,4) AS yr,
         COUNT(*) AS n,
         ROUND(SUM(Sales),0) AS total_sales,
         ROUND(SUM(profit),1) AS total_profit,
         ROUND(SUM(profit)*1.0/SUM(Sales),6) AS margin
  FROM order_information
  WHERE "Product Category" = 'Home & Furniture'
  GROUP BY "Product", yr
  ORDER BY "Product", yr
) AS sub
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-017/attempt-01/sql/S24.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-017/attempt-01/sql/S24.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-017/attempt-01/results/S24.rows.jsonl)；完整：True；SHA256：`a2b25d0948f6ca1e220313c910f2fa133b4f225318168bc00541a6b7edd8d9f0`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "order_information", "kind": "base", "block": null, "base_tables": ["order_information"]}] | [] | ["\"Product\"", "SUBSTRING(\"Order Date\", 1, 4)"] |
| B2 | [{"alias": "sub", "kind": "derived", "block": "B1", "base_tables": ["order_information"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |
| B1 | SUM(Sales) | [{"table": "order_information", "column": "Sales"}] | [] | False |
| B1 | SUM(profit) | [{"table": "order_information", "column": "profit"}] | [] | False |
| B1 | SUM(Sales) | [{"table": "order_information", "column": "Sales"}] | [] | False |
| B1 | SUM(profit) | [{"table": "order_information", "column": "profit"}] | [] | False |


## S25

类别 `data`；来源 `query_db`；调用 `1d8ff3d3b56f4847829beca71e354444`；状态 `success`。

```sql
SELECT yr, "Product", "Discount", COUNT(*) AS n, SUM(Sales) AS sales
FROM (
  SELECT substr("Order Date",1,4) AS yr, "Product", "Discount", Sales
  FROM order_information
  WHERE "Product Category" = 'Home & Furniture'
) t
GROUP BY yr, "Product", "Discount"
ORDER BY yr, "Product", "Discount"
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-017/attempt-01/sql/S25.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-017/attempt-01/sql/S25.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-017/attempt-01/results/S25.rows.jsonl)；完整：True；SHA256：`e265fb8b85b43d13bd38e43ff1dbd4935b473bcb6a2c04cde941d28886bbb692`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "order_information", "kind": "base", "block": null, "base_tables": ["order_information"]}] | [] | [] |
| B2 | [{"alias": "t", "kind": "derived", "block": "B1", "base_tables": ["order_information"]}] | [] | ["yr", "\"Product\"", "\"Discount\""] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B2 | COUNT(*) | [] | [] | True |
| B2 | SUM(Sales) | [{"table": "order_information", "column": "Sales"}] | [] | False |


## S26

类别 `data`；来源 `query_db`；调用 `539ba6c7595a4b23ad5d0030e7f406f5`；状态 `success`。

```sql
SELECT "Product", substr("Order Date",1,4) AS yr,
       SUM(Sales) AS sales,
       SUM(Sales)*1.0 / SUM(SUM(Sales)) OVER (PARTITION BY substr("Order Date",1,4)) AS sales_share
FROM order_information
WHERE "Product Category" = 'Home & Furniture'
GROUP BY "Product", yr
ORDER BY yr, sales_share DESC
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-017/attempt-01/sql/S26.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-017/attempt-01/sql/S26.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-017/attempt-01/results/S26.rows.jsonl)；完整：True；SHA256：`5d2b6116c2f24786e47d44bc0809cd60f3777becfc93868137f65b522b95ad48`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "order_information", "kind": "base", "block": null, "base_tables": ["order_information"]}] | [] | ["\"Product\"", "SUBSTRING(\"Order Date\", 1, 4)"] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | SUM(Sales) | [{"table": "order_information", "column": "Sales"}] | [] | False |
| B1 | SUM(Sales) | [{"table": "order_information", "column": "Sales"}] | [] | False |
| B1 | SUM(Sales) | [{"table": "order_information", "column": "Sales"}] | [] | False |


## S27

类别 `data`；来源 `query_db`；调用 `8b6d99ebbb7c438f8a2c799c2ae5779f`；状态 `success`。

```sql
SELECT * FROM order_information WHERE "Product Category" = 'Home & Furniture' AND "Product" = 'Beds' LIMIT 10
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-017/attempt-01/sql/S27.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-017/attempt-01/sql/S27.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-017/attempt-01/results/S27.rows.jsonl)；完整：True；SHA256：`8ed39d0e5bb0bf71efdb1b2f7e84dc1d78e5eed51f6352760f870172063cb11c`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "order_information", "kind": "base", "block": null, "base_tables": ["order_information"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |


## S28

类别 `data`；来源 `query_db`；调用 `0ee83b81c6004f14a89450c3fedc81e1`；状态 `success`。

```sql
SELECT profit, Sales, "Discount", profit*1.0/Sales AS margin,
       Sales - profit AS cost,
       "Quantity", "Shipping Cost"
FROM order_information 
WHERE "Product Category" = 'Home & Furniture' 
LIMIT 20
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-017/attempt-01/sql/S28.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-017/attempt-01/sql/S28.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-017/attempt-01/results/S28.rows.jsonl)；完整：True；SHA256：`c8801f4b11f9dbc73c50eec037dd476ef0618e4e8420ae4be5f9a14d2f5116a7`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "order_information", "kind": "base", "block": null, "base_tables": ["order_information"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |


## S29

类别 `data`；来源 `query_db`；调用 `1cdb31d49b754f60ae190ca2f397e769`；状态 `success`。

```sql
SELECT substr("Order Date",1,4) AS yr, "Discount", COUNT(*) AS n
FROM order_information
WHERE "Product Category" = 'Home & Furniture'
GROUP BY yr, "Discount"
ORDER BY yr, "Discount"
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-017/attempt-01/sql/S29.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-017/attempt-01/sql/S29.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-017/attempt-01/results/S29.rows.jsonl)；完整：True；SHA256：`5567aac7c5fd70f646ad00a0d8352faf84619c37e63ec81e9b60e5959b83bade`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "order_information", "kind": "base", "block": null, "base_tables": ["order_information"]}] | [] | ["SUBSTRING(\"Order Date\", 1, 4)", "\"Discount\""] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |


## S30

类别 `data`；来源 `query_db`；调用 `8dcbd3fa297044118ac80c9910da7979`；状态 `success`。

```sql
SELECT substr("Order Date",1,4) AS yr, "Quantity", COUNT(*) AS n
FROM order_information
WHERE "Product Category" = 'Home & Furniture'
GROUP BY yr, "Quantity"
ORDER BY yr, "Quantity"
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-017/attempt-01/sql/S30.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-017/attempt-01/sql/S30.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-017/attempt-01/results/S30.rows.jsonl)；完整：True；SHA256：`b396c01c218510f46c1642d0a55afd1af39f40a8737ac7097dd335af7ac01391`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "order_information", "kind": "base", "block": null, "base_tables": ["order_information"]}] | [] | ["SUBSTRING(\"Order Date\", 1, 4)", "\"Quantity\""] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |


## S31

类别 `data`；来源 `query_db`；调用 `73af7a519a5d4726bd9a4caad053ea5e`；状态 `success`。

```sql
SELECT substr("Order Date",1,4) AS yr, "Order Priority", COUNT(*) AS n
FROM order_information
WHERE "Product Category" = 'Home & Furniture'
GROUP BY yr, "Order Priority"
ORDER BY yr, "Order Priority"
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-017/attempt-01/sql/S31.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-017/attempt-01/sql/S31.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-017/attempt-01/results/S31.rows.jsonl)；完整：True；SHA256：`6ba62e729730a9411f77d5823d7ac9e7d03ebaf06a6aedbd3c4d0ee93fc59dde`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "order_information", "kind": "base", "block": null, "base_tables": ["order_information"]}] | [] | ["SUBSTRING(\"Order Date\", 1, 4)", "\"Order Priority\""] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |


## S32

类别 `data`；来源 `query_db`；调用 `f70284324cc047f5a31eebce9586ec73`；状态 `success`。

```sql
SELECT "Quantity", "Discount", COUNT(*) AS n, SUM(Sales) AS sales, SUM(profit) AS profit,
       ROUND(SUM(profit)*1.0/SUM(Sales),4) AS margin
FROM order_information
WHERE "Product Category" = 'Home & Furniture' AND "Product" = 'Beds'
GROUP BY "Quantity", "Discount"
ORDER BY "Quantity", "Discount"
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-017/attempt-01/sql/S32.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-017/attempt-01/sql/S32.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-017/attempt-01/results/S32.rows.jsonl)；完整：True；SHA256：`04d920b5e1fec6e4ec500ab01e43fa1b45e1c723ea49b70573c5079784e7b998`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "order_information", "kind": "base", "block": null, "base_tables": ["order_information"]}] | [] | ["\"Quantity\"", "\"Discount\""] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |
| B1 | SUM(Sales) | [{"table": "order_information", "column": "Sales"}] | [] | False |
| B1 | SUM(profit) | [{"table": "order_information", "column": "profit"}] | [] | False |
| B1 | SUM(Sales) | [{"table": "order_information", "column": "Sales"}] | [] | False |
| B1 | SUM(profit) | [{"table": "order_information", "column": "profit"}] | [] | False |


## S33

类别 `data`；来源 `query_db`；调用 `3e449cb88387458791635e2b72882797`；状态 `success`。

```sql
SELECT DISTINCT Sales FROM order_information WHERE "Product Category"='Home & Furniture' AND "Product"='Beds'
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-017/attempt-01/sql/S33.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-017/attempt-01/sql/S33.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-017/attempt-01/results/S33.rows.jsonl)；完整：True；SHA256：`f0f098f97f35b94167e530c7879be572e417707d6ef586289761bc16d5372bfb`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "order_information", "kind": "base", "block": null, "base_tables": ["order_information"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |


## S34

类别 `data`；来源 `query_db`；调用 `35de8790e6604c34a576f3003dc19a92`；状态 `success`。

```sql
SELECT "Quantity", COUNT(*) AS n, SUM(Sales) AS sales, SUM(profit) AS profit,
       ROUND(SUM(profit)*1.0/SUM(Sales),4) AS margin
FROM order_information
WHERE "Product Category" = 'Home & Furniture' AND "Product" = 'Beds'
GROUP BY "Quantity"
ORDER BY "Quantity"
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-017/attempt-01/sql/S34.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-017/attempt-01/sql/S34.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-017/attempt-01/results/S34.rows.jsonl)；完整：True；SHA256：`fd3581bf1b98e90255387cdcf580038cc945e72fbf564c1027ccd490715d76a8`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "order_information", "kind": "base", "block": null, "base_tables": ["order_information"]}] | [] | ["\"Quantity\""] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |
| B1 | SUM(Sales) | [{"table": "order_information", "column": "Sales"}] | [] | False |
| B1 | SUM(profit) | [{"table": "order_information", "column": "profit"}] | [] | False |
| B1 | SUM(Sales) | [{"table": "order_information", "column": "Sales"}] | [] | False |
| B1 | SUM(profit) | [{"table": "order_information", "column": "profit"}] | [] | False |


## S35

类别 `data`；来源 `query_db`；调用 `ff570536b26748e5839e1925a6e3aeff`；状态 `success`。

```sql
SELECT substr("Order Date",1,4) AS yr, "Quantity", COUNT(*) AS n, SUM(Sales) AS sales, SUM(profit) AS profit,
       ROUND(SUM(profit)*1.0/SUM(Sales),4) AS margin
FROM order_information
WHERE "Product Category" = 'Home & Furniture' AND "Product" = 'Beds'
GROUP BY yr, "Quantity"
ORDER BY yr, "Quantity"
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-017/attempt-01/sql/S35.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-017/attempt-01/sql/S35.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-017/attempt-01/results/S35.rows.jsonl)；完整：True；SHA256：`bb2d2fe14f912f9d2c02070485a869a03edd181424c3adf4f623423e971a0f54`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "order_information", "kind": "base", "block": null, "base_tables": ["order_information"]}] | [] | ["SUBSTRING(\"Order Date\", 1, 4)", "\"Quantity\""] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |
| B1 | SUM(Sales) | [{"table": "order_information", "column": "Sales"}] | [] | False |
| B1 | SUM(profit) | [{"table": "order_information", "column": "profit"}] | [] | False |
| B1 | SUM(Sales) | [{"table": "order_information", "column": "Sales"}] | [] | False |
| B1 | SUM(profit) | [{"table": "order_information", "column": "profit"}] | [] | False |


## S36

类别 `data`；来源 `query_db`；调用 `0dd7079018254b37a03f889630cf75bb`；状态 `success`。

```sql
SELECT DISTINCT Sales FROM order_information WHERE "Product Category"='Home & Furniture' AND "Product"='Umbrellas'
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-017/attempt-01/sql/S36.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-017/attempt-01/sql/S36.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-017/attempt-01/results/S36.rows.jsonl)；完整：True；SHA256：`9f8770761f4f50b9c1f847c75cb39595d67fa199f8b2e2b553fe8dbf7fa14425`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "order_information", "kind": "base", "block": null, "base_tables": ["order_information"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |


## S37

类别 `data`；来源 `query_db`；调用 `f1bb617fe0fc4cd0bbd8d2adc01a9596`；状态 `success`。

```sql
SELECT "Quantity", COUNT(*) AS n, SUM(profit) AS profit, SUM(Sales) AS sales,
       ROUND(SUM(profit)*1.0/SUM(Sales),4) AS margin
FROM order_information
WHERE "Product Category" = 'Home & Furniture' AND "Product" = 'Umbrellas'
GROUP BY "Quantity"
ORDER BY "Quantity"
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-017/attempt-01/sql/S37.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-017/attempt-01/sql/S37.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-017/attempt-01/results/S37.rows.jsonl)；完整：True；SHA256：`951093d439b0fdd1999c64904474859ccd2044e4115563b072242c474feafd6f`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "order_information", "kind": "base", "block": null, "base_tables": ["order_information"]}] | [] | ["\"Quantity\""] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |
| B1 | SUM(profit) | [{"table": "order_information", "column": "profit"}] | [] | False |
| B1 | SUM(Sales) | [{"table": "order_information", "column": "Sales"}] | [] | False |
| B1 | SUM(Sales) | [{"table": "order_information", "column": "Sales"}] | [] | False |
| B1 | SUM(profit) | [{"table": "order_information", "column": "profit"}] | [] | False |


## S38

类别 `data`；来源 `query_db`；调用 `08459ed4578a4245b31854ce526fc3af`；状态 `success`。

```sql
SELECT substr("Order Date",1,4) AS yr, "Quantity", COUNT(*) AS n
FROM order_information
WHERE "Product Category" = 'Home & Furniture' AND "Product" = 'Beds'
GROUP BY yr, "Quantity"
ORDER BY yr, "Quantity"
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-017/attempt-01/sql/S38.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-017/attempt-01/sql/S38.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-017/attempt-01/results/S38.rows.jsonl)；完整：True；SHA256：`8527cff650647ea0122e7747017d54eecada3283dc2acd3a5faa4a0e7921cf15`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "order_information", "kind": "base", "block": null, "base_tables": ["order_information"]}] | [] | ["SUBSTRING(\"Order Date\", 1, 4)", "\"Quantity\""] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |


## S39

类别 `data`；来源 `query_db`；调用 `466bc785450a4bc9a03192af101d335f`；状态 `success`。

```sql
SELECT substr("Order Date",1,4) AS yr, "Quantity", COUNT(*) AS n
FROM order_information
WHERE "Product Category" = 'Home & Furniture' AND "Product" = 'Umbrellas'
GROUP BY yr, "Quantity"
ORDER BY yr, "Quantity"
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-017/attempt-01/sql/S39.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-017/attempt-01/sql/S39.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-017/attempt-01/results/S39.rows.jsonl)；完整：True；SHA256：`47fc5f380766c849c4ab706d705ba6276ee7523f4aaad9e840e4e96fc65aa63b`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "order_information", "kind": "base", "block": null, "base_tables": ["order_information"]}] | [] | ["SUBSTRING(\"Order Date\", 1, 4)", "\"Quantity\""] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |


## S40

类别 `data`；来源 `query_db`；调用 `120bab68366f4daaa625399e5066b543`；状态 `success`。

```sql
SELECT pb."Product Category", pb."Product", 
       AVG(pb."Browsing Time (minutes)") AS avg_browsing,
       AVG(pb."like") AS avg_like,
       AVG(pb."share") AS avg_share,
       AVG(pb."Add to Cart") AS avg_add_to_cart
FROM product_browsing pb
WHERE pb."Product Category" = 'Home & Furniture'
GROUP BY pb."Product"
ORDER BY avg_browsing DESC
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-017/attempt-01/sql/S40.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-017/attempt-01/sql/S40.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-017/attempt-01/results/S40.rows.jsonl)；完整：True；SHA256：`3b5efa8b5c64a1df35d29bcedea057ced4530d4346bbd1d4587a45b00b6504c3`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "pb", "kind": "base", "block": null, "base_tables": ["product_browsing"]}] | [] | ["pb.\"Product\""] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | AVG(pb."Browsing Time (minutes)") | [{"table": "product_browsing", "column": "Browsing Time (minutes)"}] | [] | False |
| B1 | AVG(pb."like") | [{"table": "product_browsing", "column": "like"}] | [] | False |
| B1 | AVG(pb."share") | [{"table": "product_browsing", "column": "share"}] | [] | False |
| B1 | AVG(pb."Add to Cart") | [{"table": "product_browsing", "column": "Add to Cart"}] | [] | False |


## S41

类别 `data`；来源 `query_db`；调用 `02ff11aa3844491e86584ee0b0e156b9`；状态 `success`。

```sql
SELECT pb."Product Category", pb."Product",
       COUNT(*) AS n,
       SUM(pb."like") AS total_likes,
       SUM(pb."share") AS total_shares,
       SUM(pb."Add to Cart") AS total_add_to_cart
FROM product_browsing pb
WHERE pb."Product Category" = 'Home & Furniture'
GROUP BY pb."Product"
ORDER BY n DESC
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-017/attempt-01/sql/S41.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-017/attempt-01/sql/S41.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-017/attempt-01/results/S41.rows.jsonl)；完整：True；SHA256：`9b4dbb0a2a4fec102d45a8959c21ad2294258ed42d434be207d5751121e06657`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "pb", "kind": "base", "block": null, "base_tables": ["product_browsing"]}] | [] | ["pb.\"Product\""] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |
| B1 | SUM(pb."like") | [{"table": "product_browsing", "column": "like"}] | [] | False |
| B1 | SUM(pb."share") | [{"table": "product_browsing", "column": "share"}] | [] | False |
| B1 | SUM(pb."Add to Cart") | [{"table": "product_browsing", "column": "Add to Cart"}] | [] | False |


## S42

类别 `data`；来源 `query_db`；调用 `94c046a3208c42d3b682cf9855e4c75d`；状态 `success`。

```sql
SELECT MAX("Order Date") AS max_date, MIN("Order Date") AS min_date FROM order_information
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-017/attempt-01/sql/S42.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-017/attempt-01/sql/S42.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-017/attempt-01/results/S42.rows.jsonl)；完整：True；SHA256：`77d70eddeb5c837e883c0ff27304c1fb8abb039f8684a4eb997cb92f0257c284`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "order_information", "kind": "base", "block": null, "base_tables": ["order_information"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | MAX("Order Date") | [{"table": "order_information", "column": "Order Date"}] | [] | False |
| B1 | MIN("Order Date") | [{"table": "order_information", "column": "Order Date"}] | [] | False |


## S43

类别 `data`；来源 `query_db`；调用 `a271be5b0f6e48bb833d9e67e84592e9`；状态 `success`。

```sql
SELECT COUNT(DISTINCT "Customer ID") AS n_customers FROM order_information WHERE "Product Category" = 'Home & Furniture'
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-017/attempt-01/sql/S43.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-017/attempt-01/sql/S43.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-017/attempt-01/results/S43.rows.jsonl)；完整：True；SHA256：`372c8d8c27f7118c9c8e34bc41619db4d3844d92bd18553d0216232c4c930a60`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "order_information", "kind": "base", "block": null, "base_tables": ["order_information"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(DISTINCT "Customer ID") | [{"table": "order_information", "column": "Customer ID"}] | [] | False |


## S44

类别 `data`；来源 `query_db`；调用 `636f38c3cfa84e34b40c2da0584bb53f`；状态 `success`。

```sql
SELECT COUNT(DISTINCT "Order ID") AS n_orders FROM order_information WHERE "Product Category" = 'Home & Furniture'
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-017/attempt-01/sql/S44.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-017/attempt-01/sql/S44.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-017/attempt-01/results/S44.rows.jsonl)；完整：True；SHA256：`c7e5c37be57865a98e9d20ed736929cbbf1cd3e26bf6f3bf6c7175211726ad03`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "order_information", "kind": "base", "block": null, "base_tables": ["order_information"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(DISTINCT "Order ID") | [{"table": "order_information", "column": "Order ID"}] | [] | False |


## S45

类别 `data`；来源 `query_db`；调用 `e8841038e6384688a45a6aa4f8d3b1dc`；状态 `success`。

```sql
WITH base AS (
  SELECT "Customer ID",
         MAX("Order Date") AS last_order,
         COUNT(DISTINCT "Order ID") AS frequency,
         SUM(profit) AS monetary_profit,
         SUM(Sales) AS monetary_sales,
         COUNT(*) AS n_rows,
         SUM("Quantity" * 1.0) AS total_qty
  FROM order_information
  WHERE "Product Category" = 'Home & Furniture'
  GROUP BY "Customer ID"
)
SELECT "Customer ID", last_order, frequency, ROUND(monetary_profit,1) AS m_profit,
       monetary_sales, n_rows, ROUND(total_qty,1) AS total_qty,
       ROUND((julianday('2024-12-31') - julianday(last_order)),0) AS recency_days
FROM base
ORDER BY recency_days ASC
LIMIT 15
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-017/attempt-01/sql/S45.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-017/attempt-01/sql/S45.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-017/attempt-01/results/S45.rows.jsonl)；完整：True；SHA256：`67c671a9a15d515c72a5d98fc400e72dce25a62c884507149ed120ab75273cba`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "order_information", "kind": "base", "block": null, "base_tables": ["order_information"]}] | [] | ["\"Customer ID\""] |
| B2 | [{"alias": "base", "kind": "derived", "block": "B1", "base_tables": ["order_information"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | MAX("Order Date") | [{"table": "order_information", "column": "Order Date"}] | [] | False |
| B1 | COUNT(DISTINCT "Order ID") | [{"table": "order_information", "column": "Order ID"}] | [] | False |
| B1 | SUM(profit) | [{"table": "order_information", "column": "profit"}] | [] | False |
| B1 | SUM(Sales) | [{"table": "order_information", "column": "Sales"}] | [] | False |
| B1 | COUNT(*) | [] | [] | True |
| B1 | SUM("Quantity" * 1.0) | [{"table": "order_information", "column": "Quantity"}] | [] | False |


## S46

类别 `data`；来源 `query_db`；调用 `5551a7a8c8ec4a7a93571716732e78bc`；状态 `success`。

```sql
WITH base AS (
  SELECT "Customer ID",
         MAX("Order Date") AS last_order,
         COUNT(DISTINCT "Order ID") AS frequency,
         SUM(profit) AS monetary_profit,
         SUM(Sales) AS monetary_sales,
         COUNT(*) AS n_rows,
         SUM(CAST("Quantity" AS REAL)) AS total_qty
  FROM order_information
  WHERE "Product Category" = 'Home & Furniture'
    AND "Quantity" != 'abc'
    AND "Quantity" IS NOT NULL
  GROUP BY "Customer ID"
)
SELECT "Customer ID",
       ROUND((julianday('2024-12-31') - julianday(last_order)),0) AS recency,
       frequency,
       ROUND(monetary_profit, 1) AS monetary,
       ROUND(monetary_sales, 0) AS sales,
       ROUND(total_qty, 1) AS total_qty
FROM base
ORDER BY "Customer ID"
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-017/attempt-01/sql/S46.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-017/attempt-01/sql/S46.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-017/attempt-01/results/S46.rows.jsonl)；完整：True；SHA256：`8d9a88aacd084e701e79d3af234aaf26e5a7f9b3c16908806b09b3cc0b29baeb`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "order_information", "kind": "base", "block": null, "base_tables": ["order_information"]}] | [] | ["\"Customer ID\""] |
| B2 | [{"alias": "base", "kind": "derived", "block": "B1", "base_tables": ["order_information"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | MAX("Order Date") | [{"table": "order_information", "column": "Order Date"}] | [] | False |
| B1 | COUNT(DISTINCT "Order ID") | [{"table": "order_information", "column": "Order ID"}] | [] | False |
| B1 | SUM(profit) | [{"table": "order_information", "column": "profit"}] | [] | False |
| B1 | SUM(Sales) | [{"table": "order_information", "column": "Sales"}] | [] | False |
| B1 | COUNT(*) | [] | [] | True |
| B1 | SUM(CAST("Quantity" AS REAL)) | [{"table": "order_information", "column": "Quantity"}] | [] | False |


## S47

类别 `data`；来源 `query_db`；调用 `8566a18e43da400ebaafafac8b868a50`；状态 `success`。

```sql
WITH rfm AS (
  SELECT "Customer ID",
         MAX("Order Date") AS last_order,
         COUNT(DISTINCT "Order ID") AS frequency,
         SUM(profit) AS monetary
  FROM order_information
  WHERE "Product Category" = 'Home & Furniture'
  GROUP BY "Customer ID"
),
scored AS (
  SELECT "Customer ID",
         NTILE(4) OVER (ORDER BY julianday('2024-12-31') - julianday(last_order) DESC) AS R,
         NTILE(4) OVER (ORDER BY frequency ASC) AS F,
         NTILE(4) OVER (ORDER BY monetary ASC) AS M
  FROM rfm
)
SELECT CASE WHEN R+F+M >= 10 THEN 'Top Tier'
            WHEN R+F+M >= 7 THEN 'Mid Tier'
            WHEN R+F+M >= 4 THEN 'Low Tier'
            ELSE 'Bottom Tier' END AS segment,
       COUNT(*) AS n_customers
FROM scored
GROUP BY segment
ORDER BY n_customers DESC
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-017/attempt-01/sql/S47.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-017/attempt-01/sql/S47.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-017/attempt-01/results/S47.rows.jsonl)；完整：True；SHA256：`ae3722ed8071d67867cea44bb7b83862248785268580d33d140730e891424739`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "order_information", "kind": "base", "block": null, "base_tables": ["order_information"]}] | [] | ["\"Customer ID\""] |
| B2 | [{"alias": "rfm", "kind": "derived", "block": "B1", "base_tables": ["order_information"]}] | [] | [] |
| B3 | [{"alias": "scored", "kind": "derived", "block": "B2", "base_tables": ["order_information"]}] | [] | ["CASE WHEN R + F + M >= 10 THEN 'Top Tier' WHEN R + F + M >= 7 THEN 'Mid Tier' WHEN R + F + M >= 4 THEN 'Low Tier' ELSE 'Bottom Tier' END"] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | MAX("Order Date") | [{"table": "order_information", "column": "Order Date"}] | [] | False |
| B1 | COUNT(DISTINCT "Order ID") | [{"table": "order_information", "column": "Order ID"}] | [] | False |
| B1 | SUM(profit) | [{"table": "order_information", "column": "profit"}] | [] | False |
| B3 | COUNT(*) | [] | [] | True |


## S48

类别 `data`；来源 `python`；调用 `b962e6504dcd433294faec688385ecd8`；状态 `success`。

```sql

SELECT "Customer ID", substr("Order Date",1,4) AS yr, 
       "Order ID", "Quantity", "Product", Sales, profit,
       profit * 1.0 / Sales AS margin
FROM order_information
WHERE "Product Category" = 'Home & Furniture'
  AND "Quantity" != 'abc'
  AND "Quantity" IS NOT NULL

```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-017/attempt-01/sql/S48.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-017/attempt-01/sql/S48.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-017/attempt-01/results/S48.rows.jsonl)；完整：True；SHA256：`ccec19632d4eac5ee5bbe9166393e693cd8d995ef56fe075a277c476c463967c`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "order_information", "kind": "base", "block": null, "base_tables": ["order_information"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |


## S49

类别 `data`；来源 `python`；调用 `b350135883b64d17bc45a4dae050e918`；状态 `success`。

```sql

SELECT "Product Category", "Product", Sales, profit, "Quantity"
FROM order_information
WHERE "Quantity" != 'abc' AND "Quantity" IS NOT NULL

```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-017/attempt-01/sql/S49.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-017/attempt-01/sql/S49.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-017/attempt-01/results/S49.rows.jsonl)；完整：True；SHA256：`7504992d0a62aee7571a5bd84f9d19400ae3a9db4da11d48a409a97f578c6bb7`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "order_information", "kind": "base", "block": null, "base_tables": ["order_information"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |


## S50

类别 `data`；来源 `python`；调用 `b350135883b64d17bc45a4dae050e918`；状态 `success`。

```sql

SELECT substr("Order Date",1,4) AS yr, "Product", "Quantity",
       Sales, profit
FROM order_information
WHERE "Product Category" = 'Home & Furniture' AND "Quantity" != 'abc' AND "Quantity" IS NOT NULL

```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-017/attempt-01/sql/S50.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-017/attempt-01/sql/S50.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-017/attempt-01/results/S50.rows.jsonl)；完整：True；SHA256：`80eaf02cc22807dd482b416c09d71d09ce117fbebaa06ff7c60963d91df0ade1`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "order_information", "kind": "base", "block": null, "base_tables": ["order_information"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |


## S51

类别 `data`；来源 `python`；调用 `33f789a90f424518abc4bd4cfe7623e8`；状态 `success`。

```sql

SELECT substr("Order Date",1,4) AS yr, "Product", "Quantity",
       Sales, profit
FROM order_information
WHERE "Product Category" = 'Home & Furniture' AND "Quantity" != 'abc' AND "Quantity" IS NOT NULL

```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-017/attempt-01/sql/S51.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-017/attempt-01/sql/S51.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-017/attempt-01/results/S51.rows.jsonl)；完整：True；SHA256：`80eaf02cc22807dd482b416c09d71d09ce117fbebaa06ff7c60963d91df0ade1`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "order_information", "kind": "base", "block": null, "base_tables": ["order_information"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |


## S52

类别 `data`；来源 `python`；调用 `8595ea39d27e48469d267761548c58e1`；状态 `success`。

```sql

SELECT substr("Order Date",1,4) AS yr, "Product", "Quantity",
       Sales, profit
FROM order_information
WHERE "Product Category" = 'Home & Furniture' AND "Quantity" != 'abc' AND "Quantity" IS NOT NULL

```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-017/attempt-01/sql/S52.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-017/attempt-01/sql/S52.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-017/attempt-01/results/S52.rows.jsonl)；完整：True；SHA256：`80eaf02cc22807dd482b416c09d71d09ce117fbebaa06ff7c60963d91df0ade1`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "order_information", "kind": "base", "block": null, "base_tables": ["order_information"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |


## S53

类别 `data`；来源 `query_db`；调用 `1edac7a4965e4b179bfd944e72061528`；状态 `success`。

```sql
SELECT "Product", "Quantity", Sales, profit, "Discount", profit*1.0/Sales AS margin
FROM order_information
WHERE "Product Category"='Home & Furniture' AND "Product"='Sofa Covers'
ORDER BY "Quantity", Sales
LIMIT 30
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-017/attempt-01/sql/S53.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-017/attempt-01/sql/S53.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-017/attempt-01/results/S53.rows.jsonl)；完整：True；SHA256：`c147e64e1f1964c3ed1f6a36dd6b85aa84d5b74d33b9be68f2c994c356f20db0`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "order_information", "kind": "base", "block": null, "base_tables": ["order_information"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |


## S54

类别 `data`；来源 `query_db`；调用 `8fb5d9b122504d6885e3ca4d2def7dbd`；状态 `success`。

```sql
SELECT "Product", "Quantity", Sales, profit, profit*1.0/Sales AS margin
FROM order_information
WHERE "Product Category"='Home & Furniture' AND "Product"='Towels'
ORDER BY "Quantity", Sales
LIMIT 30
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-017/attempt-01/sql/S54.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-017/attempt-01/sql/S54.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-017/attempt-01/results/S54.rows.jsonl)；完整：True；SHA256：`672267a9e27bc4ad7df9a55e1b265e123d91c0f4daa6fead2d9d5973b2dca8fb`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "order_information", "kind": "base", "block": null, "base_tables": ["order_information"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |


## S55

类别 `data`；来源 `query_db`；调用 `66f6e50dc6de4957af1d8b834d0e4118`；状态 `success`。

```sql
SELECT "Product", "Quantity", Sales, profit, "Discount", profit*1.0/Sales AS margin
FROM order_information
WHERE "Product Category"='Home & Furniture' AND "Product"='Sofa Covers'
ORDER BY "Quantity", "Discount"
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-017/attempt-01/sql/S55.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-017/attempt-01/sql/S55.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-017/attempt-01/results/S55.rows.jsonl)；完整：True；SHA256：`041179a47f2f7af07caa9800dd295168b5bcf30b140e79da481eb48dbd7e0e8a`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "order_information", "kind": "base", "block": null, "base_tables": ["order_information"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |


## S56

类别 `data`；来源 `python`；调用 `a3cef669665e48cd8c85be0582e07fed`；状态 `success`。

```sql

SELECT "Product", "Quantity", Sales, profit, "Discount", "Shipping Cost"
FROM order_information
WHERE "Product Category" = 'Home & Furniture' AND "Quantity" != 'abc' AND "Quantity" IS NOT NULL AND "Discount" != 'xxx'

```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-017/attempt-01/sql/S56.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-017/attempt-01/sql/S56.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-017/attempt-01/results/S56.rows.jsonl)；完整：True；SHA256：`dce89a759907e2823785876313e11f76caccae33f1f6a1f30a4786d5cc6eab74`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "order_information", "kind": "base", "block": null, "base_tables": ["order_information"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |


## S57

类别 `data`；来源 `python`；调用 `95de76e3694d47bcab6450a1a747d04d`；状态 `success`。

```sql

SELECT "Product Category", substr("Order Date",1,4) AS yr,
       SUM(profit)*1.0/SUM(Sales) AS margin
FROM order_information
GROUP BY "Product Category", yr
ORDER BY "Product Category", yr

```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-017/attempt-01/sql/S57.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-017/attempt-01/sql/S57.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-017/attempt-01/results/S57.rows.jsonl)；完整：True；SHA256：`33b8d8b54c25411240faab6c1d5d67ac18be873b72b4addec18d676993137d61`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "order_information", "kind": "base", "block": null, "base_tables": ["order_information"]}] | [] | ["\"Product Category\"", "SUBSTRING(\"Order Date\", 1, 4)"] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | SUM(Sales) | [{"table": "order_information", "column": "Sales"}] | [] | False |
| B1 | SUM(profit) | [{"table": "order_information", "column": "profit"}] | [] | False |


## S58

类别 `data`；来源 `python`；调用 `95de76e3694d47bcab6450a1a747d04d`；状态 `success`。

```sql

SELECT "Product", substr("Order Date",1,4) AS yr,
       SUM(profit)*1.0/SUM(Sales) AS margin
FROM order_information
WHERE "Product Category" = 'Home & Furniture'
GROUP BY "Product", yr
ORDER BY "Product", yr

```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-017/attempt-01/sql/S58.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-017/attempt-01/sql/S58.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-017/attempt-01/results/S58.rows.jsonl)；完整：True；SHA256：`8cea38746d7fbed1d00029fb4686ea012eb682ee62dec5b70411bd96f5530109`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "order_information", "kind": "base", "block": null, "base_tables": ["order_information"]}] | [] | ["\"Product\"", "SUBSTRING(\"Order Date\", 1, 4)"] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | SUM(Sales) | [{"table": "order_information", "column": "Sales"}] | [] | False |
| B1 | SUM(profit) | [{"table": "order_information", "column": "profit"}] | [] | False |


## S59

类别 `data`；来源 `python`；调用 `95de76e3694d47bcab6450a1a747d04d`；状态 `success`。

```sql

SELECT "Customer ID", substr("Order Date",1,4) AS yr, "Quantity"
FROM order_information
WHERE "Product Category" = 'Home & Furniture' AND "Quantity" != 'abc' AND "Quantity" IS NOT NULL

```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-017/attempt-01/sql/S59.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-017/attempt-01/sql/S59.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-017/attempt-01/results/S59.rows.jsonl)；完整：True；SHA256：`92be1eef908e6302f83bfc85d4f423192655f7bae1f2f6d7cb7e792a888cb382`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "order_information", "kind": "base", "block": null, "base_tables": ["order_information"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |


## S60

类别 `data`；来源 `python`；调用 `95de76e3694d47bcab6450a1a747d04d`；状态 `success`。

```sql

SELECT profit, Sales, "Quantity", "Discount"
FROM order_information
WHERE "Product Category" = 'Home & Furniture' AND "Quantity" != 'abc' AND "Quantity" IS NOT NULL AND "Discount" != 'xxx'
LIMIT 5000

```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-017/attempt-01/sql/S60.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-017/attempt-01/sql/S60.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-017/attempt-01/results/S60.rows.jsonl)；完整：True；SHA256：`d86a46bb087b799631899ea9c6ea3f3a761fbf3f241cc48dd85716db0eb3fd9d`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "order_information", "kind": "base", "block": null, "base_tables": ["order_information"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |


## S61

类别 `data`；来源 `python`；调用 `95de76e3694d47bcab6450a1a747d04d`；状态 `success`。

```sql

SELECT "Product", substr("Order Date",1,4) AS yr,
       SUM(Sales) AS sales
FROM order_information
WHERE "Product Category" = 'Home & Furniture'
GROUP BY "Product", yr
ORDER BY yr, sales DESC

```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-017/attempt-01/sql/S61.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-017/attempt-01/sql/S61.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-017/attempt-01/results/S61.rows.jsonl)；完整：True；SHA256：`5fb4c0f439f16c55aee24bb1a3c0c783d0176ce1d7b4169e48a0fd5eecf24516`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "order_information", "kind": "base", "block": null, "base_tables": ["order_information"]}] | [] | ["\"Product\"", "SUBSTRING(\"Order Date\", 1, 4)"] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | SUM(Sales) | [{"table": "order_information", "column": "Sales"}] | [] | False |


## S62

类别 `data`；来源 `python`；调用 `ab5f52575b9f40269b696f17eb922439`；状态 `success`。

```sql

SELECT "Customer ID", substr("Order Date",1,4) AS yr, "Quantity"
FROM order_information
WHERE "Product Category" = 'Home & Furniture' AND "Quantity" != 'abc' AND "Quantity" IS NOT NULL

```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-017/attempt-01/sql/S62.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-017/attempt-01/sql/S62.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-017/attempt-01/results/S62.rows.jsonl)；完整：True；SHA256：`92be1eef908e6302f83bfc85d4f423192655f7bae1f2f6d7cb7e792a888cb382`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "order_information", "kind": "base", "block": null, "base_tables": ["order_information"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |


## S63

类别 `data`；来源 `python`；调用 `ab5f52575b9f40269b696f17eb922439`；状态 `success`。

```sql

SELECT "Customer ID", substr("Order Date",1,4) AS yr, profit, Sales
FROM order_information
WHERE "Product Category" = 'Home & Furniture'

```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-017/attempt-01/sql/S63.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-017/attempt-01/sql/S63.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-017/attempt-01/results/S63.rows.jsonl)；完整：True；SHA256：`624dba496a5b304e3ca582f096fdd8a6e926878446b246694bdc1d78ed00fe7a`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "order_information", "kind": "base", "block": null, "base_tables": ["order_information"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |


## S64

类别 `data`；来源 `python`；调用 `ab5f52575b9f40269b696f17eb922439`；状态 `success`。

```sql

SELECT pb."Customer ID", pb."Product Category", 
       AVG(pb."Browsing Time (minutes)") AS avg_browsing,
       AVG(pb."like") AS avg_like,
       AVG(pb."share") AS avg_share,
       AVG(pb."Add to Cart") AS avg_add_to_cart
FROM product_browsing pb
WHERE pb."Product Category" = 'Home & Furniture'
GROUP BY pb."Customer ID"

```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-017/attempt-01/sql/S64.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-017/attempt-01/sql/S64.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-017/attempt-01/results/S64.rows.jsonl)；完整：True；SHA256：`68d64900f73b5b9101b57c1bfbe38d685da97efeafbd4b352050ff74ead00f42`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "pb", "kind": "base", "block": null, "base_tables": ["product_browsing"]}] | [] | ["pb.\"Customer ID\""] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | AVG(pb."Browsing Time (minutes)") | [{"table": "product_browsing", "column": "Browsing Time (minutes)"}] | [] | False |
| B1 | AVG(pb."like") | [{"table": "product_browsing", "column": "like"}] | [] | False |
| B1 | AVG(pb."share") | [{"table": "product_browsing", "column": "share"}] | [] | False |
| B1 | AVG(pb."Add to Cart") | [{"table": "product_browsing", "column": "Add to Cart"}] | [] | False |


## S65

类别 `data`；来源 `query_db`；调用 `77a7eac361a94f48b191a996449a6078`；状态 `success`。

```sql
SELECT substr("Order Date",1,4) AS yr,
       AVG(CAST("Discount" AS REAL)) AS avg_discount,
       AVG(CAST("Quantity" AS REAL) * CAST("Discount" AS REAL)) AS avg_qty_discount
FROM order_information
WHERE "Product Category" = 'Home & Furniture' AND "Discount" != 'xxx' AND "Quantity" != 'abc' AND "Quantity" IS NOT NULL
GROUP BY yr
ORDER BY yr
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-017/attempt-01/sql/S65.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-017/attempt-01/sql/S65.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-017/attempt-01/results/S65.rows.jsonl)；完整：True；SHA256：`5b9281c5319f15edd28b5fa9b0e0d281228acf32edb407827dcfc3755f5aa5bc`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "order_information", "kind": "base", "block": null, "base_tables": ["order_information"]}] | [] | ["SUBSTRING(\"Order Date\", 1, 4)"] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | AVG(CAST("Discount" AS REAL)) | [{"table": "order_information", "column": "Discount"}] | [] | False |
| B1 | AVG(CAST("Quantity" AS REAL) * CAST("Discount" AS REAL)) | [{"table": "order_information", "column": "Quantity"}, {"table": "order_information", "column": "Discount"}] | [] | False |


## S66

类别 `data`；来源 `query_db`；调用 `7f849b53e4254e538450a33eeb41cad3`；状态 `success`。

```sql
SELECT "Product", 
       AVG(CAST("Discount" AS REAL)) AS avg_discount,
       AVG(CAST("Quantity" AS REAL) * CAST("Discount" AS REAL)) AS avg_qty_discount
FROM order_information
WHERE "Product Category" = 'Home & Furniture' AND "Discount" != 'xxx' AND "Quantity" != 'abc' AND "Quantity" IS NOT NULL
GROUP BY "Product"
ORDER BY avg_qty_discount DESC
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-017/attempt-01/sql/S66.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-017/attempt-01/sql/S66.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-017/attempt-01/results/S66.rows.jsonl)；完整：True；SHA256：`46e1d685484083be90e847c98976398c70df912202cf4d1e36eab11e5676c5bf`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "order_information", "kind": "base", "block": null, "base_tables": ["order_information"]}] | [] | ["\"Product\""] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | AVG(CAST("Discount" AS REAL)) | [{"table": "order_information", "column": "Discount"}] | [] | False |
| B1 | AVG(CAST("Quantity" AS REAL) * CAST("Discount" AS REAL)) | [{"table": "order_information", "column": "Quantity"}, {"table": "order_information", "column": "Discount"}] | [] | False |


## S67

类别 `data`；来源 `python`；调用 `30389c59ef664abb9b18d5afa22a12ce`；状态 `success`。

```sql

SELECT "Product", "Quantity", "Discount", Sales, profit
FROM order_information
WHERE "Product Category" = 'Home & Furniture' 
  AND "Quantity" != 'abc' AND "Quantity" IS NOT NULL AND "Discount" != 'xxx'

```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-017/attempt-01/sql/S67.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-017/attempt-01/sql/S67.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-017/attempt-01/results/S67.rows.jsonl)；完整：True；SHA256：`f1b3e4e8d846382032a84017e49ecd7ca94005d0940ea645a0d752b0befd71ac`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "order_information", "kind": "base", "block": null, "base_tables": ["order_information"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |


## S68

类别 `data`；来源 `python`；调用 `30389c59ef664abb9b18d5afa22a12ce`；状态 `success`。

```sql

SELECT "Product Category", substr("Order Date",1,4) AS yr,
       ROUND(SUM(profit)*1.0/SUM(Sales),4) AS margin
FROM order_information
GROUP BY "Product Category", yr
ORDER BY "Product Category", yr

```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-017/attempt-01/sql/S68.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-017/attempt-01/sql/S68.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-017/attempt-01/results/S68.rows.jsonl)；完整：True；SHA256：`373848ad024939ccd9082a94fe0f41e9f4b78ab61bec2f49318d9cd3519e2669`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "order_information", "kind": "base", "block": null, "base_tables": ["order_information"]}] | [] | ["\"Product Category\"", "SUBSTRING(\"Order Date\", 1, 4)"] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | SUM(Sales) | [{"table": "order_information", "column": "Sales"}] | [] | False |
| B1 | SUM(profit) | [{"table": "order_information", "column": "profit"}] | [] | False |


## S69

类别 `data`；来源 `python`；调用 `34102af37bc2416fb853b1d16f13dbfa`；状态 `success`。

```sql

SELECT "Customer ID", SUM(profit) AS profit, SUM(Sales) AS sales
FROM order_information
WHERE "Product Category" = 'Home & Furniture'
GROUP BY "Customer ID"

```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-017/attempt-01/sql/S69.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-017/attempt-01/sql/S69.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-017/attempt-01/results/S69.rows.jsonl)；完整：True；SHA256：`8000a0704f7e586f0917a8e4d6ed30ab646d3b138ed7f87ca837e07cdafc1e6a`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "order_information", "kind": "base", "block": null, "base_tables": ["order_information"]}] | [] | ["\"Customer ID\""] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | SUM(profit) | [{"table": "order_information", "column": "profit"}] | [] | False |
| B1 | SUM(Sales) | [{"table": "order_information", "column": "Sales"}] | [] | False |


## S70

类别 `data`；来源 `python`；调用 `34102af37bc2416fb853b1d16f13dbfa`；状态 `success`。

```sql

SELECT COUNT(*) AS n, SUM(Sales) AS sales, SUM(profit) AS profit
FROM order_information WHERE "Product Category" = 'Home & Furniture'

```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-017/attempt-01/sql/S70.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-017/attempt-01/sql/S70.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-017/attempt-01/results/S70.rows.jsonl)；完整：True；SHA256：`c0eb6fcf40898b96ed2c13f9467fdc8a3e169c71c13d4cd838d0f10404b282a5`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "order_information", "kind": "base", "block": null, "base_tables": ["order_information"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |
| B1 | SUM(Sales) | [{"table": "order_information", "column": "Sales"}] | [] | False |
| B1 | SUM(profit) | [{"table": "order_information", "column": "profit"}] | [] | False |


## S71

类别 `data`；来源 `python`；调用 `34102af37bc2416fb853b1d16f13dbfa`；状态 `success`。

```sql

SELECT COUNT(DISTINCT "Order ID") AS distinct_orders, COUNT(*) AS rows_count
FROM order_information WHERE "Product Category" = 'Home & Furniture'

```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-017/attempt-01/sql/S71.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-017/attempt-01/sql/S71.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-017/attempt-01/results/S71.rows.jsonl)；完整：True；SHA256：`6e5de49aa5991ddd0d71c39a867f4006c20cf2cd3eb3b6b34e8f08bd54b93ee6`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "order_information", "kind": "base", "block": null, "base_tables": ["order_information"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(DISTINCT "Order ID") | [{"table": "order_information", "column": "Order ID"}] | [] | False |
| B1 | COUNT(*) | [] | [] | True |

