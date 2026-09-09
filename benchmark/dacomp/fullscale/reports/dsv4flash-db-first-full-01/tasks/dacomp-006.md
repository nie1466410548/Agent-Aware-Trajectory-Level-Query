# dacomp-006

The monthly total profit in South China is very unstable. Which aspects are causing the in…

运行：已提交。官方未评分。全部 SQL 尝试/成功 54/51；数据 SQL 52/49；Python 4 次。

完整原题：

The monthly total profit in South China is very unstable. Which aspects are causing the instability?

| 表 | 行数 | 列数 |
| --- | --- | --- |
| sheet1 | 18250 | 21 |


实际路线（分析者依据 SQL/源码概括，不代表 Agent 自述）：S3：sheet1 查询 → S13：sheet1 分组聚合 → S23：sheet1 分组聚合 → S34：sheet1 分组聚合 → S44：sheet1 分组聚合 → S54：sheet1 分组聚合（等距列出六个结构节点，全部步骤见下表）

数据库大小：7,507,968 字节。

## 数据 SQL

| SQL | 状态 | 基础表 | Join 输入/类型 | GROUP BY | 聚合表达式 | 结果行数 | 数据库 ms |
| --- | --- | --- | --- | --- | --- | --- | --- |
| [S3/Q1](#s3) | success | ["sheet1"] | 0 / {} | [] | [] | 10 | 0.326 |
| [S4/Q2](#s4) | success | ["sheet1"] | 0 / {} | [] | [] | 73 | 6.677 |
| [S5/Q3](#s5) | success | ["sheet1"] | 0 / {} | [] | ["MIN(\"Date\")", "MAX(\"Date\")"] | 1 | 3.575 |
| [S6/Q4](#s6) | success | ["sheet1"] | 0 / {} | ["STRFTIME('%Y-%m', \"Date\")"] | ["COUNT(*)", "SUM(\"Profit\")", "SUM(\"Total Logistics Revenue\")", "SUM(\"Total Logistics Cost\")", "AVG(\"Profit Margin\")"] | 12 | 9.538 |
| [S7/Q5](#s7) | success | ["sheet1"] | 0 / {} | [] | [] | 8 | 7.598 |
| [S8/Q6](#s8) | success | ["sheet1"] | 0 / {} | ["\"Consigned Product\"", "STRFTIME('%Y-%m', \"Date\")"] | ["SUM(\"Profit\")", "COUNT(*)", "SUM(\"Sales Quantity\")", "SUM(\"Total Logistics Revenue\")", "SUM(\"Total Logistics Cost\")"] | 96 | 10.538 |
| [S9/Q7](#s9) | success | ["sheet1"] | 0 / {} | ["\"Destination\"", "STRFTIME('%Y-%m', \"Date\")"] | ["SUM(\"Profit\")", "COUNT(*)", "SUM(\"Sales Quantity\")"] | 837 | 11.274 |
| [S10/Q8](#s10) | failed | ["sheet1"] | 0 / {} | ["STRFTIME('%Y-%m', \"Date\")"] | ["SUM(\"Profit\")", "SUM(\"Total Logistics Revenue\")", "SUM(\"Total Logistics Cost\")", "SUM(\"Freight Cost\")", "SUM(\"Warehousing Cost\")", "SUM(\"Other Operating Costs\")", "SUM(\"Logistics Value-Added Service Revenue\")", "SUM(\"Discount Amount\")", "SUM(\"Sales Quantity\")", "COUNT(*)", "AVG(total_profit)", "MIN(total_profit)", "MAX(total_profit)", "AVG(total_profit)", "STDDEV(total_profit)", "AVG(total_profit)", "STDDEV(total_rev)", "AVG(total_rev)", "STDDEV(total_cost)", "AVG(total_cost)", "STDDEV(qty)", "AVG(qty)", "STDDEV(orders)", "AVG(orders)", "STDDEV(freight)", "AVG(freight)", "STDDEV(warehousing)", "AVG(warehousing)", "STDDEV(other_cost)", "AVG(other_cost)", "STDDEV(vas)", "AVG(vas)", "STDDEV(discount)", "AVG(discount)", "MAX(total_profit)", "MIN(total_profit)"] | unknown | 未取得；调用总时长 0.285 ms |
| [S11/Q9](#s11) | failed | ["sheet1"] | 0 / {} | ["\"Consigned Product\"", "STRFTIME('%Y-%m', \"Date\")", "dim"] | ["SUM(\"Profit\")", "SUM(\"Sales Quantity\")", "SUM(\"Profit\")", "AVG(total_profit)", "STDDEV(total_profit)", "SUM(total_profit)", "STDDEV(total_profit)", "AVG(total_profit)", "SUM(total_profit)"] | unknown | 未取得；调用总时长 0.242 ms |
| [S12/Q10](#s12) | success | ["sheet1"] | 0 / {} | ["STRFTIME('%Y-%m', \"Date\")"] | ["SUM(\"Profit\")", "SUM(\"Total Logistics Revenue\")", "SUM(\"Total Logistics Cost\")", "SUM(\"Freight Cost\")", "SUM(\"Warehousing Cost\")", "SUM(\"Other Operating Costs\")", "SUM(\"Logistics Value-Added Service Revenue\")", "SUM(\"Discount Amount\")", "SUM(\"Sales Quantity\")", "COUNT(*)", "AVG(total_profit)", "MIN(total_profit)", "MAX(total_profit)", "AVG(total_profit)", "AVG(total_profit)", "AVG(total_rev)", "AVG(total_cost)", "AVG(qty)", "AVG(orders)", "AVG(freight)", "AVG(warehousing)", "AVG(other_cost)", "AVG(vas)", "AVG(discount)", "MAX(total_profit)", "MIN(total_profit)", "AVG(total_profit * total_profit)", "AVG(total_rev * total_rev)", "AVG(total_cost * total_cost)", "AVG(qty * qty)", "AVG(orders * orders)", "AVG(freight * freight)", "AVG(warehousing * warehousing)", "AVG(other_cost * other_cost)", "AVG(vas * vas)", "AVG(discount * discount)", "AVG(total_profit)", "AVG(total_profit)", "AVG(total_rev)", "AVG(total_rev)", "AVG(total_cost)", "AVG(total_cost)", "AVG(qty)", "AVG(qty)", "AVG(orders)", "AVG(orders)", "AVG(freight)", "AVG(freight)", "AVG(warehousing)", "AVG(warehousing)", "AVG(other_cost)", "AVG(other_cost)", "AVG(vas)", "AVG(vas)", "AVG(discount)", "AVG(discount)"] | 1 | 11.18 |
| [S13/Q11](#s13) | success | ["sheet1"] | 0 / {} | ["\"Consigned Product\"", "STRFTIME('%Y-%m', \"Date\")", "dim"] | ["SUM(\"Profit\")", "SUM(\"Sales Quantity\")", "SUM(\"Profit\")", "AVG(total_profit)", "SUM(total_profit)", "AVG(total_profit * total_profit)", "AVG(total_profit)", "SUM(total_profit)", "AVG(total_profit)", "AVG(total_profit)", "AVG(total_profit * total_profit)", "AVG(total_profit)", "AVG(total_profit)"] | 8 | 13.054 |
| [S14/Q12](#s14) | success | ["sheet1"] | 0 / {} | ["\"Destination\"", "STRFTIME('%Y-%m', \"Date\")", "dim"] | ["SUM(\"Profit\")", "SUM(\"Sales Quantity\")", "SUM(\"Profit\")", "AVG(total_profit)", "SUM(total_profit)", "AVG(total_profit * total_profit)", "AVG(total_profit)", "SUM(total_profit)", "AVG(total_profit)", "AVG(total_profit)", "AVG(total_profit * total_profit)", "AVG(total_profit)", "AVG(total_profit)"] | 73 | 14.411 |
| [S15/Q13](#s15) | success | ["sheet1"] | 0 / {} | ["\"Customer Gender\"", "STRFTIME('%Y-%m', \"Date\")", "dim"] | ["SUM(\"Profit\")", "SUM(\"Sales Quantity\")", "SUM(\"Profit\")", "AVG(total_profit)", "SUM(total_profit)", "AVG(total_profit * total_profit)", "AVG(total_profit)", "SUM(total_profit)", "AVG(total_profit)", "AVG(total_profit)", "AVG(total_profit * total_profit)", "AVG(total_profit)", "AVG(total_profit)"] | 2 | 12.792 |
| [S16/Q14](#s16) | success | ["sheet1"] | 0 / {} | ["\"Age Range\"", "STRFTIME('%Y-%m', \"Date\")", "dim"] | ["SUM(\"Profit\")", "SUM(\"Sales Quantity\")", "SUM(\"Profit\")", "AVG(total_profit)", "SUM(total_profit)", "AVG(total_profit * total_profit)", "AVG(total_profit)", "SUM(total_profit)", "AVG(total_profit)", "AVG(total_profit)", "AVG(total_profit * total_profit)", "AVG(total_profit)", "AVG(total_profit)"] | 5 | 12.875 |
| [S17/Q15](#s17) | failed | ["sheet1"] | 0 / {} | ["SUBSTRING(\"Destination\", 13, IIF(INSTR(SUBSTRING(\"Destination\", 13), '-') = 0, 0, INSTR(SUBSTRING(\"Destination\", 13), '-') + 13 - 1) - 13)"] | ["COUNT(*)", "SUM(\"Profit\")"] | unknown | 未取得；调用总时长 0.171 ms |
| [S18/Q16](#s18) | success | ["sheet1"] | 0 / {} | ["\"Destination\""] | [] | 73 | 5.512 |
| [S19/Q17](#s19) | success | ["sheet1"] | 0 / {} | ["SUBSTRING(\"Destination\", 13, INSTR(SUBSTRING(\"Destination\", 13), '-') - 1)"] | ["COUNT(*)", "SUM(\"Profit\")"] | 6 | 8.063 |
| [S20/Q18](#s20) | success | ["sheet1"] | 0 / {} | ["SUBSTRING(\"Destination\", 13, INSTR(SUBSTRING(\"Destination\", 13), '-') - 1)", "STRFTIME('%Y-%m', \"Date\")", "province"] | ["SUM(\"Profit\")", "SUM(\"Sales Quantity\")", "COUNT(*)", "COUNT(*)", "AVG(total_profit)", "MIN(total_profit)", "MAX(total_profit)", "SUM(total_profit)", "AVG(total_profit * total_profit)", "AVG(total_profit)", "AVG(total_profit)", "AVG(total_profit)", "AVG(total_profit * total_profit)", "AVG(total_profit)", "AVG(total_profit)"] | 6 | 12.121 |
| [S21/Q19](#s21) | success | ["sheet1"] | 2 / {'INNER': 1} | ["\"Consigned Product\"", "STRFTIME('%Y-%m', \"Date\")", "STRFTIME('%Y-%m', \"Date\")", "dim"] | ["SUM(\"Profit\")", "SUM(\"Profit\")", "AVG(p)", "AVG(t)", "AVG(t)", "AVG(t)", "SUM((t - (SELECT AVG(t) FROM tot_month)) * (t - (SELECT AVG(t) FROM tot_month)))", "SUM((p - (SELECT AVG(p) FROM prod_month AS p2 WHERE p2.dim = prod_month.dim)) * (t - (SELECT AVG(t) FROM tot_month)))"] | 8 | 21.939 |
| [S22/Q20](#s22) | success | ["sheet1"] | 2 / {'INNER': 1} | ["SUBSTRING(\"Destination\", 13, INSTR(SUBSTRING(\"Destination\", 13), '-') - 1)", "STRFTIME('%Y-%m', \"Date\")", "STRFTIME('%Y-%m', \"Date\")", "dim"] | ["SUM(\"Profit\")", "SUM(\"Profit\")", "AVG(p)", "AVG(t)", "AVG(t)", "AVG(t)", "SUM((t - (SELECT AVG(t) FROM tot_month)) * (t - (SELECT AVG(t) FROM tot_month)))", "SUM((p - (SELECT AVG(p) FROM prov_month AS p2 WHERE p2.dim = prov_month.dim)) * (t - (SELECT AVG(t) FROM tot_month)))"] | 6 | 25.328 |
| [S23/Q21](#s23) | success | ["sheet1"] | 2 / {'INNER': 1} | ["\"Age Range\"", "STRFTIME('%Y-%m', \"Date\")", "STRFTIME('%Y-%m', \"Date\")", "dim"] | ["SUM(\"Profit\")", "SUM(\"Profit\")", "AVG(p)", "AVG(t)", "AVG(t)", "AVG(t)", "SUM((t - (SELECT AVG(t) FROM tot_month)) * (t - (SELECT AVG(t) FROM tot_month)))", "SUM((p - (SELECT AVG(p) FROM age_month AS p2 WHERE p2.dim = age_month.dim)) * (t - (SELECT AVG(t) FROM tot_month)))"] | 5 | 16.904 |
| [S24/Q22](#s24) | success | ["sheet1"] | 2 / {'INNER': 1} | ["\"Customer Gender\"", "STRFTIME('%Y-%m', \"Date\")", "STRFTIME('%Y-%m', \"Date\")", "dim"] | ["SUM(\"Profit\")", "SUM(\"Profit\")", "AVG(p)", "AVG(t)", "AVG(t)", "AVG(t)", "SUM((t - (SELECT AVG(t) FROM tot_month)) * (t - (SELECT AVG(t) FROM tot_month)))", "SUM((p - (SELECT AVG(p) FROM g_month AS p2 WHERE p2.dim = g_month.dim)) * (t - (SELECT AVG(t) FROM tot_month)))"] | 2 | 16.115 |
| [S25/Q23](#s25) | success | ["sheet1"] | 0 / {} | ["STRFTIME('%Y-%m', \"Date\")"] | ["SUM(\"Total Logistics Revenue\")", "SUM(\"List Price Revenue\")", "SUM(\"Logistics Value-Added Service Revenue\")", "SUM(\"Discount Amount\")", "SUM(\"Total Logistics Cost\")", "SUM(\"Freight Cost\")", "SUM(\"Warehousing Cost\")", "SUM(\"Other Operating Costs\")", "SUM(\"Profit\")"] | 12 | 10.965 |
| [S26/Q24](#s26) | success | ["sheet1"] | 2 / {'LEFT': 1} | ["STRFTIME('%Y-%m', \"Date\")"] | ["SUM(\"Profit\")", "MAX(month)"] | 12 | 7.87 |
| [S27/Q25](#s27) | success | ["sheet1"] | 0 / {} | ["STRFTIME('%Y-%m', \"Date\")"] | ["SUM(\"Profit\")"] | 12 | 7.73 |
| [S28/Q26](#s28) | success | ["sheet1"] | 0 / {} | ["\"Consigned Product\"", "STRFTIME('%Y-%m', \"Date\")"] | ["SUM(\"Profit\")"] | 96 | 9.62 |
| [S29/Q27](#s29) | success | ["sheet1"] | 0 / {} | ["SUBSTRING(\"Destination\", 13, INSTR(SUBSTRING(\"Destination\", 13), '-') - 1)", "STRFTIME('%Y-%m', \"Date\")"] | ["SUM(\"Profit\")"] | 72 | 11.972 |
| [S30/Q28](#s30) | success | ["sheet1"] | 0 / {} | [] | ["SUM(CASE WHEN \"Profit Margin\" > 1 THEN 1 ELSE 0 END)", "SUM(CASE WHEN \"Total Logistics Revenue\" <= 0 THEN 1 ELSE 0 END)", "SUM(CASE WHEN \"Discount Amount\" < 0 THEN 1 ELSE 0 END)", "SUM(CASE WHEN \"Total Logistics Cost\" <= 0 THEN 1 ELSE 0 END)", "COUNT(*)"] | 1 | 5.003 |
| [S31/Q29](#s31) | success | ["sheet1"] | 0 / {} | ["STRFTIME('%Y-%m', \"Date\")"] | ["COUNT(*)", "AVG(\"Profit Margin\")", "MIN(\"Profit Margin\")", "MAX(\"Profit Margin\")"] | 12 | 8.272 |
| [S32/Q30](#s32) | success | ["sheet1"] | 0 / {} | [] | [] | 2 | 3.9 |
| [S33/Q31](#s33) | success | ["sheet1"] | 0 / {} | ["STRFTIME('%Y-%m', \"Date\")"] | ["COUNT(*)", "SUM(\"Profit\")", "AVG(\"Profit\")", "AVG(\"Sales Quantity\")", "AVG(\"Profit Margin\")", "AVG(\"Logistics Unit Price\")"] | 12 | 9.008 |
| [S34/Q32](#s34) | success | ["sheet1"] | 0 / {} | ["pct"] | ["SUM(\"Profit\")", "COUNT(*)", "SUM(\"Profit\")", "SUM(\"Profit\")"] | 12 | 16.703 |
| [S35/Q33](#s35) | success | ["sheet1"] | 0 / {} | [] | [] | 15 | 4.176 |
| [S36/Q34](#s36) | success | ["sheet1"] | 0 / {} | ["STRFTIME('%Y-%m', \"Date\")"] | ["SUM(\"Profit\")", "SUM(\"Total Logistics Revenue\")", "SUM(\"Total Logistics Cost\")", "SUM(\"Sales Quantity\")", "COUNT(*)", "AVG(\"Profit Margin\")", "AVG(\"Logistics Unit Price\")"] | 12 | 10.07 |
| [S37/Q35](#s37) | success | ["sheet1"] | 0 / {} | ["\"Consigned Product\"", "STRFTIME('%Y-%m', \"Date\")"] | ["SUM(\"Profit\")"] | 96 | 9.135 |
| [S38/Q36](#s38) | success | ["sheet1"] | 0 / {} | ["SUBSTRING(\"Destination\", 13, INSTR(SUBSTRING(\"Destination\", 13), '-') - 1)", "STRFTIME('%Y-%m', \"Date\")"] | ["SUM(\"Profit\")"] | 72 | 11.132 |
| [S39/Q37](#s39) | success | ["sheet1"] | 0 / {} | ["STRFTIME('%Y-%m', \"Date\")"] | ["SUM(\"Profit\")", "SUM(\"Total Logistics Revenue\")", "SUM(\"Total Logistics Cost\")", "SUM(\"Sales Quantity\")", "COUNT(*)", "AVG(\"Profit Margin\")", "AVG(\"Logistics Unit Price\")"] | 12 | 9.833 |
| [S40/Q38](#s40) | success | ["sheet1"] | 0 / {} | ["\"Consigned Product\"", "STRFTIME('%Y-%m', \"Date\")"] | ["SUM(\"Profit\")"] | 96 | 8.9 |
| [S41/Q39](#s41) | success | ["sheet1"] | 0 / {} | ["SUBSTRING(\"Destination\", 13, INSTR(SUBSTRING(\"Destination\", 13), '-') - 1)", "STRFTIME('%Y-%m', \"Date\")"] | ["SUM(\"Profit\")"] | 72 | 10.946 |
| [S42/Q40](#s42) | success | ["sheet1"] | 0 / {} | ["STRFTIME('%Y-%m', \"Date\")"] | ["SUM(\"Profit\")", "SUM(\"Total Logistics Revenue\")", "SUM(\"Total Logistics Cost\")", "SUM(\"Sales Quantity\")", "COUNT(*)", "AVG(\"Profit Margin\")", "AVG(\"Logistics Unit Price\")"] | 12 | 10.412 |
| [S43/Q41](#s43) | success | ["sheet1"] | 0 / {} | ["\"Consigned Product\"", "STRFTIME('%Y-%m', \"Date\")"] | ["SUM(\"Profit\")"] | 96 | 9.153 |
| [S44/Q42](#s44) | success | ["sheet1"] | 0 / {} | ["SUBSTRING(\"Destination\", 13, INSTR(SUBSTRING(\"Destination\", 13), '-') - 1)", "STRFTIME('%Y-%m', \"Date\")"] | ["SUM(\"Profit\")"] | 72 | 11.165 |
| [S45/Q43](#s45) | success | ["sheet1"] | 0 / {} | ["STRFTIME('%Y-%m', \"Date\")"] | ["SUM(\"List Price Revenue\")", "SUM(\"Logistics Value-Added Service Revenue\")", "SUM(\"Discount Amount\")"] | 12 | 9.01 |
| [S46/Q44](#s46) | success | ["sheet1"] | 0 / {} | ["STRFTIME('%Y-%m', \"Date\")"] | ["SUM(\"Freight Cost\")", "SUM(\"Warehousing Cost\")", "SUM(\"Other Operating Costs\")"] | 12 | 8.288 |
| [S47/Q45](#s47) | success | ["sheet1"] | 0 / {} | ["\"Consigned Product\""] | ["SUM(CASE WHEN STRFTIME('%m', \"Date\") = '01' THEN \"Profit\" ELSE 0 END)", "SUM(CASE WHEN STRFTIME('%m', \"Date\") = '02' THEN \"Profit\" ELSE 0 END)", "AVG(\"Profit\")", "SUM(CASE WHEN STRFTIME('%m', \"Date\") = '02' THEN \"Profit\" ELSE 0 END)", "SUM(CASE WHEN STRFTIME('%m', \"Date\") = '01' THEN \"Profit\" ELSE 0 END)"] | 8 | 10.225 |
| [S48/Q46](#s48) | success | ["sheet1"] | 0 / {} | ["\"Consigned Product\"", "STRFTIME('%Y-%m', \"Date\")"] | ["SUM(\"Profit\")"] | 12 | 4.724 |
| [S49/Q47](#s49) | success | ["sheet1"] | 0 / {} | ["\"Consigned Product\"", "STRFTIME('%Y-%m', \"Date\")", "dim"] | ["SUM(\"Profit\")", "AVG(p)", "MIN(p)", "MAX(p)", "AVG(p)", "AVG(p * p)", "AVG(p)", "AVG(p)", "AVG(p)", "MAX(p)", "MIN(p)", "AVG(p * p)", "AVG(p)", "AVG(p)"] | 8 | 9.619 |
| [S50/Q48](#s50) | success | ["sheet1"] | 0 / {} | ["STRFTIME('%Y-%m', \"Date\")"] | ["SUM(\"List Price Revenue\")", "SUM(\"Logistics Value-Added Service Revenue\")", "SUM(\"Discount Amount\")", "SUM(\"Total Logistics Revenue\")"] | 12 | 9.574 |
| [S51/Q49](#s51) | success | ["sheet1"] | 0 / {} | ["STRFTIME('%m', \"Date\")"] | ["COUNT(*)", "SUM(\"Sales Quantity\")", "AVG(\"Logistics Unit Price\")", "SUM(\"Discount Amount\")", "SUM(\"Profit\")", "AVG(\"Profit Margin\")", "SUM(\"Profit\")", "SUM(\"Sales Quantity\")"] | 12 | 5.251 |
| [S52/Q50](#s52) | success | ["sheet1"] | 0 / {} | ["STRFTIME('%Y-%m', \"Date\")"] | ["COUNT(*)", "SUM(\"Profit\")", "AVG(\"Profit\")"] | 12 | 8.406 |
| [S53/Q51](#s53) | success | ["sheet1"] | 0 / {} | ["STRFTIME('%Y-%m', \"Date\")"] | ["SUM(\"Sales Quantity\")", "SUM(\"Total Logistics Revenue\")", "SUM(\"Profit\")"] | 12 | 8.356 |
| [S54/Q52](#s54) | success | ["sheet1"] | 0 / {} | ["\"Age Range\"", "\"Customer Gender\"", "STRFTIME('%Y-%m', \"Date\")"] | ["SUM(\"Profit\")"] | 120 | 11.419 |


## 元数据和设置

| SQL | 类别 | 状态 | 内容 |
| --- | --- | --- | --- |
| S1 | connection_setup | success | PRAGMA query_only=ON |
| S2 | metadata | success | SELECT name,sql FROM sqlite_master WHERE type='table' ORDER BY name |


## Python 与执行位置

人工源码审查：**database_first_partial_violation**。SQL performs most monthly/product/province aggregates and several window calculations. Python joins those aggregates, computes group means and covariance contributions, and repeats month-level sums. These arithmetic/grouping preparations can be expressed with SQLite joins/window aggregates; their placement outside SQL is a protocol exception/violation. Rendering is allowed. [证据](../reviews/dacomp-006.json)。

P1：Compute correlation and variance decomposition analysis for South China monthly profit. SQLite lacks STDDEV and correlation functions, so Python is needed for the statistical analysis and visualization of key drivers of instability.

[源码](../../../runs/dsv4flash-db-first-full-01/dacomp-006/attempt-01/python/P1.py)；[输出](../../../runs/dsv4flash-db-first-full-01/dacomp-006/attempt-01/python/P1.stdout)；[错误](../../../runs/dsv4flash-db-first-full-01/dacomp-006/attempt-01/python/P1.stderr)。检出需人工核验的 SQL 可实现操作：groupby(, .merge(, .query(, sort_values(；不能仅凭理由判为合规。

P2：Fix the variance decomposition and correlation analysis. The previous merge had a column name collision. Re-running with corrected column references.

[源码](../../../runs/dsv4flash-db-first-full-01/dacomp-006/attempt-01/python/P2.py)；[输出](../../../runs/dsv4flash-db-first-full-01/dacomp-006/attempt-01/python/P2.stdout)；[错误](../../../runs/dsv4flash-db-first-full-01/dacomp-006/attempt-01/python/P2.stderr)。检出需人工核验的 SQL 可实现操作：groupby(, .merge(, .query(, sort_values(；不能仅凭理由判为合规。

P3：Fix the pie chart to handle negative values (Hunan has negative covariance share). Use bar charts instead and save remaining figures.

[源码](../../../runs/dsv4flash-db-first-full-01/dacomp-006/attempt-01/python/P3.py)；[输出](../../../runs/dsv4flash-db-first-full-01/dacomp-006/attempt-01/python/P3.stdout)；[错误](../../../runs/dsv4flash-db-first-full-01/dacomp-006/attempt-01/python/P3.stderr)。检出需人工核验的 SQL 可实现操作：groupby(, .merge(, .query(, sort_values(；不能仅凭理由判为合规。

P4：Quantify volume-vs-margin decomposition of the largest monthly swings and produce a final summary figure for age/gender segments. These statistical decompositions require Python.

[源码](../../../runs/dsv4flash-db-first-full-01/dacomp-006/attempt-01/python/P4.py)；[输出](../../../runs/dsv4flash-db-first-full-01/dacomp-006/attempt-01/python/P4.stdout)；[错误](../../../runs/dsv4flash-db-first-full-01/dacomp-006/attempt-01/python/P4.stderr)。检出需人工核验的 SQL 可实现操作：groupby(, .query(；不能仅凭理由判为合规。

## 优化机会

已验证候选。筛选限于精确 SQL、相同自包含 CTE、相同单表完整过滤、可分解单表聚合；未覆盖任意 Join 等价和一般谓词蕴含。全部候选都是 offline，未测在线预测。

| 候选 | 类型 | 已有结果 | 覆盖 SQL | 后续次数 | 中间行数 | 验证 | 成本 |
| --- | --- | --- | --- | --- | --- | --- | --- |
| C1 | exact-result reuse | True | ["S36", "S39", "S42"] | 2 | unknown | not_verified_cap | Not tested |
| C2 | exact-result reuse | True | ["S37", "S40", "S43"] | 2 | unknown | not_verified_cap | Not tested |
| C3 | exact-result reuse | True | ["S38", "S41", "S44"] | 2 | unknown | not_verified_cap | Not tested |
| C4 | common subexpression | False | ["S21", "S28", "S48", "S49"] | 3 | unknown | not_verified_cap | Not tested |
| C5 | common subexpression | False | ["S21", "S22", "S23", "S24"] | 3 | unknown | not_verified_cap | Not tested |
| C6 | common subexpression | False | ["S22", "S29"] | 1 | unknown | not_verified_cap | Not tested |
| C7 | common subexpression | False | ["S26", "S27"] | 1 | unknown | not_verified_cap | Not tested |
| C8 | common filtered view | False | ["S4", "S6", "S8", "S9", "S18", "S19", "S30", "S31", "S33", "S35", "S47"] | 10 | 6785 | verified | Not benchmarked; correctness alone does not establish net speedup. |
| C9 | aggregate MV | False | ["S6", "S8", "S9", "S19", "S30", "S31", "S33", "S47"] | 7 | unknown | not_verified_cap | Not tested |
| C10 | common filtered view | False | ["S36", "S37", "S38", "S39", "S40", "S41", "S42", "S43", "S44", "S45", "S46", "S52", "S53", "S54"] | 13 | 6785 | verified | Not benchmarked; correctness alone does not establish net speedup. |
| C11 | aggregate MV | False | ["S36", "S37", "S38", "S39", "S40", "S41", "S42", "S43", "S44", "S45", "S46", "S52", "S53", "S54"] | 13 | 2921 | verified | Not benchmarked; correctness alone does not establish net speedup. |


已验证覆盖（含触发查询、候选并集去重）：25/49 条成功数据 SQL。正确性仅针对当前数据库快照；未测性能的候选不能声称已加速。

[完整 build/rewrite 与比较证据](dacomp-006.analysis.json)。

### C10：common filtered view

Same single source and complete filter; original filter retained.

原查询 [S36](#s36), [S37](#s37), [S38](#s38), [S39](#s39), [S40](#s40), [S41](#s41), [S42](#s42), [S43](#s43), [S44](#s44), [S45](#s45), [S46](#s46), [S52](#s52), [S53](#s53), [S54](#s54) → 新增共享状态 C10 → 后续 13 次可复用。该构建点为事后假设，不代表 Agent 当时预知后续。

构建定义：

```sql
SELECT * FROM "sheet1" WHERE "Destination" LIKE 'South China%%'
```

受益查询 S36 的改写示例：

```sql
SELECT STRFTIME('%Y-%m', "Date") AS month, SUM("Profit") AS profit, SUM("Total Logistics Revenue") AS rev, SUM("Total Logistics Cost") AS cost, SUM("Sales Quantity") AS qty, COUNT(*) AS orders, AVG("Profit Margin") AS avg_margin, AVG("Logistics Unit Price") AS avg_price FROM temp.reuse_candidate AS sheet1 WHERE "Destination" LIKE 'South China%%' GROUP BY month ORDER BY month
```

| 原 SQL | 列名一致 | 结果一致 | 比较方法 |
| --- | --- | --- | --- |
| S36 | True | True | ordered_numeric_tolerance |
| S37 | True | True | ordered_numeric_tolerance |
| S38 | True | True | ordered_numeric_tolerance |
| S39 | True | True | ordered_numeric_tolerance |
| S40 | True | True | ordered_numeric_tolerance |
| S41 | True | True | ordered_numeric_tolerance |
| S42 | True | True | ordered_numeric_tolerance |
| S43 | True | True | ordered_numeric_tolerance |
| S44 | True | True | ordered_numeric_tolerance |
| S45 | True | True | ordered_numeric_tolerance |
| S46 | True | True | ordered_numeric_tolerance |
| S52 | True | True | ordered_numeric_tolerance |
| S53 | True | True | ordered_numeric_tolerance |
| S54 | True | True | ordered_numeric_tolerance |


验证状态：verified；成本结论：Not benchmarked; correctness alone does not establish net speedup.

### C11：aggregate MV

Union of grouping keys; decomposable aggregate states; AVG uses SUM and non-NULL COUNT.

原查询 [S36](#s36), [S37](#s37), [S38](#s38), [S39](#s39), [S40](#s40), [S41](#s41), [S42](#s42), [S43](#s43), [S44](#s44), [S45](#s45), [S46](#s46), [S52](#s52), [S53](#s53), [S54](#s54) → 新增共享状态 C11 → 后续 13 次可复用。该构建点为事后假设，不代表 Agent 当时预知后续。

构建定义：

```sql
SELECT STRFTIME('%Y-%m', "Date") AS __g0, "Consigned Product" AS __g1, SUBSTRING("Destination", 13, INSTR(SUBSTRING("Destination", 13), '-') - 1) AS __g2, "Age Range" AS __g3, "Customer Gender" AS __g4, SUM("Profit") AS __a0, SUM("Total Logistics Revenue") AS __a1, SUM("Total Logistics Cost") AS __a2, SUM("Sales Quantity") AS __a3, COUNT(*) AS __a4, SUM("Profit Margin") AS __a5_sum, COUNT("Profit Margin") AS __a5_n, SUM("Logistics Unit Price") AS __a6_sum, COUNT("Logistics Unit Price") AS __a6_n, SUM("List Price Revenue") AS __a7, SUM("Logistics Value-Added Service Revenue") AS __a8, SUM("Discount Amount") AS __a9, SUM("Freight Cost") AS __a10, SUM("Warehousing Cost") AS __a11, SUM("Other Operating Costs") AS __a12, SUM("Profit") AS __a13_sum, COUNT("Profit") AS __a13_n FROM "sheet1" WHERE "Destination" LIKE 'South China%%' GROUP BY STRFTIME('%Y-%m', "Date"), "Consigned Product", SUBSTRING("Destination", 13, INSTR(SUBSTRING("Destination", 13), '-') - 1), "Age Range", "Customer Gender"
```

受益查询 S36 的改写示例：

```sql
SELECT __g0 AS month, SUM(__a0) AS profit, SUM(__a1) AS rev, SUM(__a2) AS cost, SUM(__a3) AS qty, SUM(__a4) AS orders, (1.0 * SUM(__a5_sum) / NULLIF(SUM(__a5_n), 0)) AS avg_margin, (1.0 * SUM(__a6_sum) / NULLIF(SUM(__a6_n), 0)) AS avg_price FROM temp.reuse_candidate GROUP BY __g0 ORDER BY month
```

| 原 SQL | 列名一致 | 结果一致 | 比较方法 |
| --- | --- | --- | --- |
| S36 | True | True | ordered_numeric_tolerance |
| S37 | True | True | ordered_numeric_tolerance |
| S38 | True | True | ordered_numeric_tolerance |
| S39 | True | True | ordered_numeric_tolerance |
| S40 | True | True | ordered_numeric_tolerance |
| S41 | True | True | ordered_numeric_tolerance |
| S42 | True | True | ordered_numeric_tolerance |
| S43 | True | True | ordered_numeric_tolerance |
| S44 | True | True | ordered_numeric_tolerance |
| S45 | True | True | ordered_numeric_tolerance |
| S46 | True | True | ordered_numeric_tolerance |
| S52 | True | True | ordered_numeric_tolerance |
| S53 | True | True | ordered_numeric_tolerance |
| S54 | True | True | ordered_numeric_tolerance |


验证状态：verified；成本结论：Not benchmarked; correctness alone does not establish net speedup.

### C8：common filtered view

Same single source and complete filter; original filter retained.

原查询 [S4](#s4), [S6](#s6), [S8](#s8), [S9](#s9), [S18](#s18), [S19](#s19), [S30](#s30), [S31](#s31), [S33](#s33), [S35](#s35), [S47](#s47) → 新增共享状态 C8 → 后续 10 次可复用。该构建点为事后假设，不代表 Agent 当时预知后续。

构建定义：

```sql
SELECT * FROM "sheet1" WHERE "Destination" LIKE 'South China%'
```

受益查询 S4 的改写示例：

```sql
SELECT DISTINCT "Destination" FROM temp.reuse_candidate AS sheet1 WHERE "Destination" LIKE 'South China%' ORDER BY "Destination"
```

| 原 SQL | 列名一致 | 结果一致 | 比较方法 |
| --- | --- | --- | --- |
| S4 | True | True | ordered_numeric_tolerance |
| S6 | True | True | ordered_numeric_tolerance |
| S8 | True | True | ordered_numeric_tolerance |
| S9 | True | True | ordered_numeric_tolerance |
| S18 | True | True | ordered_numeric_tolerance |
| S19 | True | True | ordered_numeric_tolerance |
| S30 | True | True | exact_multiset |
| S31 | True | True | ordered_numeric_tolerance |
| S33 | True | True | ordered_numeric_tolerance |
| S35 | True | True | ordered_numeric_tolerance |
| S47 | True | True | ordered_numeric_tolerance |


验证状态：verified；成本结论：Not benchmarked; correctness alone does not establish net speedup.

结果依赖：自动记录 SQL→Python 的接口父调用，以及源码中引用归档文件的消费者；字面值相同不认定因果。模型方向选择需要人工读取消息，尚未做全面因果标注。

[原始报告](../../../runs/dsv4flash-db-first-full-01/dacomp-006/attempt-01/answer.md)；[统一消息](../../../runs/dsv4flash-db-first-full-01/dacomp-006/attempt-01/messages.jsonl)；[原始 OpenCode 事件](../../../runs/dsv4flash-db-first-full-01/dacomp-006/attempt-01/opencode.jsonl)；[SQL 引擎日志](../../../runs/dsv4flash-db-first-full-01/dacomp-006/attempt-01/sql_journal.jsonl)。

[可读报告（本地图片链接规范化）](../answers/dacomp-006.md)。原始回答保留，分析结论未改写。

## S1

类别 `connection_setup`；来源 `connection`；调用 `78a806e54bac4a298d31937cbb26167f`；状态 `success`。

```sql
PRAGMA query_only=ON
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-006/attempt-01/sql/S1.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-006/attempt-01/sql/S1.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-006/attempt-01/results/S1.rows.jsonl)；完整：True；SHA256：`e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`。

## S2

类别 `metadata`；来源 `list_db`；调用 `78a806e54bac4a298d31937cbb26167f`；状态 `success`。

```sql
SELECT name,sql FROM sqlite_master WHERE type='table' ORDER BY name
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-006/attempt-01/sql/S2.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-006/attempt-01/sql/S2.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-006/attempt-01/results/S2.rows.jsonl)；完整：True；SHA256：`1da017ce066480cdde506c4bb99c9f5b07b8f8aa62b3d1442b5e2f6036b9ea14`。

## S3

类别 `data`；来源 `query_db`；调用 `e31bf815b90048cbabb0004af93f5e54`；状态 `success`。

```sql
SELECT * FROM sheet1 LIMIT 10
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-006/attempt-01/sql/S3.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-006/attempt-01/sql/S3.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-006/attempt-01/results/S3.rows.jsonl)；完整：True；SHA256：`b5d856226a804d07fee61ae583e1864fd5a6e817217a9c2cd6988e9ec418941e`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "sheet1", "kind": "base", "block": null, "base_tables": ["sheet1"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |


## S4

类别 `data`；来源 `query_db`；调用 `5655348b718444deb34b64d65af73dec`；状态 `success`。

```sql
SELECT DISTINCT "Destination" FROM sheet1 WHERE "Destination" LIKE 'South China%' ORDER BY "Destination"
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-006/attempt-01/sql/S4.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-006/attempt-01/sql/S4.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-006/attempt-01/results/S4.rows.jsonl)；完整：True；SHA256：`d54f191beb2c5dcd4985430fa50c44458206feacbbd482d7d16d8db0c30b0ccd`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "sheet1", "kind": "base", "block": null, "base_tables": ["sheet1"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |


## S5

类别 `data`；来源 `query_db`；调用 `61bba370f0504803a9494f0a37bcfa84`；状态 `success`。

```sql
SELECT MIN("Date"), MAX("Date") FROM sheet1
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-006/attempt-01/sql/S5.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-006/attempt-01/sql/S5.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-006/attempt-01/results/S5.rows.jsonl)；完整：True；SHA256：`30bc785455b0ec6f6faef4d873749868127e8de17c46b23b89fc255acfc7912e`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "sheet1", "kind": "base", "block": null, "base_tables": ["sheet1"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | MIN("Date") | [{"table": "sheet1", "column": "Date"}] | [] | False |
| B1 | MAX("Date") | [{"table": "sheet1", "column": "Date"}] | [] | False |


## S6

类别 `data`；来源 `query_db`；调用 `11c42b2eab244c1891ed7a83c638ef36`；状态 `success`。

```sql
SELECT 
  strftime('%Y-%m', "Date") AS month,
  COUNT(*) AS order_count,
  SUM("Profit") AS total_profit,
  SUM("Total Logistics Revenue") AS total_revenue,
  SUM("Total Logistics Cost") AS total_cost,
  AVG("Profit Margin") AS avg_profit_margin
FROM sheet1
WHERE "Destination" LIKE 'South China%'
GROUP BY month
ORDER BY month
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-006/attempt-01/sql/S6.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-006/attempt-01/sql/S6.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-006/attempt-01/results/S6.rows.jsonl)；完整：True；SHA256：`adb664ea257a1a6c1a099c50b0dcc7803adc90c0731a63658389aa325d938e08`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "sheet1", "kind": "base", "block": null, "base_tables": ["sheet1"]}] | [] | ["STRFTIME('%Y-%m', \"Date\")"] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |
| B1 | SUM("Profit") | [{"table": "sheet1", "column": "Profit"}] | [] | False |
| B1 | SUM("Total Logistics Revenue") | [{"table": "sheet1", "column": "Total Logistics Revenue"}] | [] | False |
| B1 | SUM("Total Logistics Cost") | [{"table": "sheet1", "column": "Total Logistics Cost"}] | [] | False |
| B1 | AVG("Profit Margin") | [{"table": "sheet1", "column": "Profit Margin"}] | [] | False |


## S7

类别 `data`；来源 `query_db`；调用 `0f722604c41a4f2c8ea0e13e4194750d`；状态 `success`。

```sql
SELECT DISTINCT "Consigned Product" FROM sheet1 ORDER BY "Consigned Product"
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-006/attempt-01/sql/S7.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-006/attempt-01/sql/S7.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-006/attempt-01/results/S7.rows.jsonl)；完整：True；SHA256：`e1b0a0605c919c88e94c8fe19d6af5b0c7d71d25aaaf6a171a6515e0f7da0de9`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "sheet1", "kind": "base", "block": null, "base_tables": ["sheet1"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |


## S8

类别 `data`；来源 `query_db`；调用 `e9b87cf612d1474eb36949c96a2cfdd4`；状态 `success`。

```sql
SELECT 
  "Consigned Product",
  strftime('%Y-%m', "Date") AS month,
  SUM("Profit") AS total_profit,
  COUNT(*) AS order_count,
  SUM("Sales Quantity") AS total_qty,
  SUM("Total Logistics Revenue") AS total_revenue,
  SUM("Total Logistics Cost") AS total_cost
FROM sheet1
WHERE "Destination" LIKE 'South China%'
GROUP BY "Consigned Product", month
ORDER BY "Consigned Product", month
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-006/attempt-01/sql/S8.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-006/attempt-01/sql/S8.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-006/attempt-01/results/S8.rows.jsonl)；完整：True；SHA256：`f08e05d0fa4bae145623b025d74594b1be1346305731a64fc6a55b7c71440105`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "sheet1", "kind": "base", "block": null, "base_tables": ["sheet1"]}] | [] | ["\"Consigned Product\"", "STRFTIME('%Y-%m', \"Date\")"] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | SUM("Profit") | [{"table": "sheet1", "column": "Profit"}] | [] | False |
| B1 | COUNT(*) | [] | [] | True |
| B1 | SUM("Sales Quantity") | [{"table": "sheet1", "column": "Sales Quantity"}] | [] | False |
| B1 | SUM("Total Logistics Revenue") | [{"table": "sheet1", "column": "Total Logistics Revenue"}] | [] | False |
| B1 | SUM("Total Logistics Cost") | [{"table": "sheet1", "column": "Total Logistics Cost"}] | [] | False |


## S9

类别 `data`；来源 `query_db`；调用 `9a50c61a3829428595a9b6b7660e8b20`；状态 `success`。

```sql
SELECT 
  "Destination",
  strftime('%Y-%m', "Date") AS month,
  SUM("Profit") AS total_profit,
  COUNT(*) AS order_count,
  SUM("Sales Quantity") AS total_qty
FROM sheet1
WHERE "Destination" LIKE 'South China%'
GROUP BY "Destination", month
ORDER BY "Destination", month
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-006/attempt-01/sql/S9.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-006/attempt-01/sql/S9.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-006/attempt-01/results/S9.rows.jsonl)；完整：True；SHA256：`eb7acc5ad27c0d6338231d4df138cfcf5550d9d7858faebfe6a366f256c271c5`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "sheet1", "kind": "base", "block": null, "base_tables": ["sheet1"]}] | [] | ["\"Destination\"", "STRFTIME('%Y-%m', \"Date\")"] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | SUM("Profit") | [{"table": "sheet1", "column": "Profit"}] | [] | False |
| B1 | COUNT(*) | [] | [] | True |
| B1 | SUM("Sales Quantity") | [{"table": "sheet1", "column": "Sales Quantity"}] | [] | False |


## S10

类别 `data`；来源 `query_db`；调用 `ed9ddac6f86848398b57e88581bbe4f9`；状态 `failed`。

```sql
WITH monthly AS (
  SELECT 
    strftime('%Y-%m', "Date") AS month,
    SUM("Profit") AS total_profit,
    SUM("Total Logistics Revenue") AS total_rev,
    SUM("Total Logistics Cost") AS total_cost,
    SUM("Freight Cost") AS freight,
    SUM("Warehousing Cost") AS warehousing,
    SUM("Other Operating Costs") AS other_cost,
    SUM("Logistics Value-Added Service Revenue") AS vas,
    SUM("Discount Amount") AS discount,
    SUM("Sales Quantity") AS qty,
    COUNT(*) AS orders
  FROM sheet1
  WHERE "Destination" LIKE 'South China%'
  GROUP BY month
)
SELECT 
  ROUND(AVG(total_profit),0) AS mean_profit,
  ROUND(MIN(total_profit),0) AS min_profit,
  ROUND(MAX(total_profit),0) AS max_profit,
  ROUND((MAX(total_profit)-MIN(total_profit))/AVG(total_profit)*100,1) AS range_pct_of_mean,
  ROUND(STDDEV(total_profit)/AVG(total_profit)*100,1) AS cv_profit_pct,
  ROUND(STDDEV(total_rev)/AVG(total_rev)*100,1) AS cv_rev_pct,
  ROUND(STDDEV(total_cost)/AVG(total_cost)*100,1) AS cv_cost_pct,
  ROUND(STDDEV(qty)/AVG(qty)*100,1) AS cv_qty_pct,
  ROUND(STDDEV(orders)/AVG(orders)*100,1) AS cv_orders_pct,
  ROUND(STDDEV(freight)/AVG(freight)*100,1) AS cv_freight_pct,
  ROUND(STDDEV(warehousing)/AVG(warehousing)*100,1) AS cv_warehousing_pct,
  ROUND(STDDEV(other_cost)/AVG(other_cost)*100,1) AS cv_othercost_pct,
  ROUND(STDDEV(vas)/AVG(vas)*100,1) AS cv_vas_pct,
  ROUND(STDDEV(discount)/AVG(discount)*100,1) AS cv_discount_pct
FROM monthly
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-006/attempt-01/sql/S10.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-006/attempt-01/sql/S10.parameters.json)。

错误：`OperationalError('no such function: STDDEV')`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "sheet1", "kind": "base", "block": null, "base_tables": ["sheet1"]}] | [] | ["STRFTIME('%Y-%m', \"Date\")"] |
| B2 | [{"alias": "monthly", "kind": "derived", "block": "B1", "base_tables": ["sheet1"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | SUM("Profit") | [{"table": "sheet1", "column": "Profit"}] | [] | False |
| B1 | SUM("Total Logistics Revenue") | [{"table": "sheet1", "column": "Total Logistics Revenue"}] | [] | False |
| B1 | SUM("Total Logistics Cost") | [{"table": "sheet1", "column": "Total Logistics Cost"}] | [] | False |
| B1 | SUM("Freight Cost") | [{"table": "sheet1", "column": "Freight Cost"}] | [] | False |
| B1 | SUM("Warehousing Cost") | [{"table": "sheet1", "column": "Warehousing Cost"}] | [] | False |
| B1 | SUM("Other Operating Costs") | [{"table": "sheet1", "column": "Other Operating Costs"}] | [] | False |
| B1 | SUM("Logistics Value-Added Service Revenue") | [{"table": "sheet1", "column": "Logistics Value-Added Service Revenue"}] | [] | False |
| B1 | SUM("Discount Amount") | [{"table": "sheet1", "column": "Discount Amount"}] | [] | False |
| B1 | SUM("Sales Quantity") | [{"table": "sheet1", "column": "Sales Quantity"}] | [] | False |
| B1 | COUNT(*) | [] | [] | True |
| B2 | AVG(total_profit) | [{"table": "sheet1", "column": "Profit"}] | [] | False |
| B2 | MIN(total_profit) | [{"table": "sheet1", "column": "Profit"}] | [] | False |
| B2 | MAX(total_profit) | [{"table": "sheet1", "column": "Profit"}] | [] | False |
| B2 | AVG(total_profit) | [{"table": "sheet1", "column": "Profit"}] | [] | False |
| B2 | STDDEV(total_profit) | [{"table": "sheet1", "column": "Profit"}] | [] | False |
| B2 | AVG(total_profit) | [{"table": "sheet1", "column": "Profit"}] | [] | False |
| B2 | STDDEV(total_rev) | [{"table": "sheet1", "column": "Total Logistics Revenue"}] | [] | False |
| B2 | AVG(total_rev) | [{"table": "sheet1", "column": "Total Logistics Revenue"}] | [] | False |
| B2 | STDDEV(total_cost) | [{"table": "sheet1", "column": "Total Logistics Cost"}] | [] | False |
| B2 | AVG(total_cost) | [{"table": "sheet1", "column": "Total Logistics Cost"}] | [] | False |
| B2 | STDDEV(qty) | [{"table": "sheet1", "column": "Sales Quantity"}] | [] | False |
| B2 | AVG(qty) | [{"table": "sheet1", "column": "Sales Quantity"}] | [] | False |
| B2 | STDDEV(orders) | [] | [] | False |
| B2 | AVG(orders) | [] | [] | False |
| B2 | STDDEV(freight) | [{"table": "sheet1", "column": "Freight Cost"}] | [] | False |
| B2 | AVG(freight) | [{"table": "sheet1", "column": "Freight Cost"}] | [] | False |
| B2 | STDDEV(warehousing) | [{"table": "sheet1", "column": "Warehousing Cost"}] | [] | False |
| B2 | AVG(warehousing) | [{"table": "sheet1", "column": "Warehousing Cost"}] | [] | False |
| B2 | STDDEV(other_cost) | [{"table": "sheet1", "column": "Other Operating Costs"}] | [] | False |
| B2 | AVG(other_cost) | [{"table": "sheet1", "column": "Other Operating Costs"}] | [] | False |
| B2 | STDDEV(vas) | [{"table": "sheet1", "column": "Logistics Value-Added Service Revenue"}] | [] | False |
| B2 | AVG(vas) | [{"table": "sheet1", "column": "Logistics Value-Added Service Revenue"}] | [] | False |
| B2 | STDDEV(discount) | [{"table": "sheet1", "column": "Discount Amount"}] | [] | False |
| B2 | AVG(discount) | [{"table": "sheet1", "column": "Discount Amount"}] | [] | False |
| B2 | MAX(total_profit) | [{"table": "sheet1", "column": "Profit"}] | [] | False |
| B2 | MIN(total_profit) | [{"table": "sheet1", "column": "Profit"}] | [] | False |


## S11

类别 `data`；来源 `query_db`；调用 `3cb110d249fa493cb8e82ba78aaca18d`；状态 `failed`。

```sql
WITH monthly AS (
  SELECT 
    "Consigned Product" AS dim,
    strftime('%Y-%m', "Date") AS month,
    SUM("Profit") AS total_profit,
    SUM("Sales Quantity") AS qty
  FROM sheet1
  WHERE "Destination" LIKE 'South China%'
  GROUP BY "Consigned Product", month
),
stats AS (
  SELECT dim,
    ROUND(AVG(total_profit),0) AS mean_profit,
    ROUND(STDDEV(total_profit),0) AS sd_profit,
    ROUND(STDDEV(total_profit)/AVG(total_profit)*100,1) AS cv_pct,
    ROUND(SUM(total_profit),0) AS annual_profit,
    ROUND(SUM(total_profit) * 100.0 / (SELECT SUM("Profit") FROM sheet1 WHERE "Destination" LIKE 'South China%'),1) AS pct_of_total
  FROM monthly
  GROUP BY dim
)
SELECT * FROM stats ORDER BY cv_pct DESC
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-006/attempt-01/sql/S11.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-006/attempt-01/sql/S11.parameters.json)。

错误：`OperationalError('no such function: STDDEV')`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "sheet1", "kind": "base", "block": null, "base_tables": ["sheet1"]}] | [] | ["\"Consigned Product\"", "STRFTIME('%Y-%m', \"Date\")"] |
| B2 | [{"alias": "sheet1", "kind": "base", "block": null, "base_tables": ["sheet1"]}] | [] | [] |
| B3 | [{"alias": "monthly", "kind": "derived", "block": "B1", "base_tables": ["sheet1"]}] | [] | ["dim"] |
| B4 | [{"alias": "stats", "kind": "derived", "block": "B3", "base_tables": ["sheet1"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | SUM("Profit") | [{"table": "sheet1", "column": "Profit"}] | [] | False |
| B1 | SUM("Sales Quantity") | [{"table": "sheet1", "column": "Sales Quantity"}] | [] | False |
| B2 | SUM("Profit") | [{"table": "sheet1", "column": "Profit"}] | [] | False |
| B3 | AVG(total_profit) | [{"table": "sheet1", "column": "Profit"}] | [] | False |
| B3 | STDDEV(total_profit) | [{"table": "sheet1", "column": "Profit"}] | [] | False |
| B3 | SUM(total_profit) | [{"table": "sheet1", "column": "Profit"}] | [] | False |
| B3 | STDDEV(total_profit) | [{"table": "sheet1", "column": "Profit"}] | [] | False |
| B3 | AVG(total_profit) | [{"table": "sheet1", "column": "Profit"}] | [] | False |
| B3 | SUM(total_profit) | [{"table": "sheet1", "column": "Profit"}] | [] | False |


未解析列血缘：[{"block": "B4", "column": "\"Profit\"", "reason": "ambiguous_or_missing_source"}, {"block": "B4", "column": "\"Destination\"", "reason": "ambiguous_or_missing_source"}]

## S12

类别 `data`；来源 `query_db`；调用 `35d72ad5b1fe4188be1ecbcdaaf21961`；状态 `success`。

```sql
WITH monthly AS (
  SELECT 
    strftime('%Y-%m', "Date") AS month,
    SUM("Profit") AS total_profit,
    SUM("Total Logistics Revenue") AS total_rev,
    SUM("Total Logistics Cost") AS total_cost,
    SUM("Freight Cost") AS freight,
    SUM("Warehousing Cost") AS warehousing,
    SUM("Other Operating Costs") AS other_cost,
    SUM("Logistics Value-Added Service Revenue") AS vas,
    SUM("Discount Amount") AS discount,
    SUM("Sales Quantity") AS qty,
    COUNT(*) AS orders
  FROM sheet1
  WHERE "Destination" LIKE 'South China%'
  GROUP BY month
)
SELECT 
  ROUND(AVG(total_profit),0) AS mean_profit,
  ROUND(MIN(total_profit),0) AS min_profit,
  ROUND(MAX(total_profit),0) AS max_profit,
  ROUND((MAX(total_profit)-MIN(total_profit))/AVG(total_profit)*100,1) AS range_pct_of_mean,
  ROUND(SQRT(AVG(total_profit*total_profit)-AVG(total_profit)*AVG(total_profit))/AVG(total_profit)*100,1) AS cv_profit_pct,
  ROUND(SQRT(AVG(total_rev*total_rev)-AVG(total_rev)*AVG(total_rev))/AVG(total_rev)*100,1) AS cv_rev_pct,
  ROUND(SQRT(AVG(total_cost*total_cost)-AVG(total_cost)*AVG(total_cost))/AVG(total_cost)*100,1) AS cv_cost_pct,
  ROUND(SQRT(AVG(qty*qty)-AVG(qty)*AVG(qty))/AVG(qty)*100,1) AS cv_qty_pct,
  ROUND(SQRT(AVG(orders*orders)-AVG(orders)*AVG(orders))/AVG(orders)*100,1) AS cv_orders_pct,
  ROUND(SQRT(AVG(freight*freight)-AVG(freight)*AVG(freight))/AVG(freight)*100,1) AS cv_freight_pct,
  ROUND(SQRT(AVG(warehousing*warehousing)-AVG(warehousing)*AVG(warehousing))/AVG(warehousing)*100,1) AS cv_warehousing_pct,
  ROUND(SQRT(AVG(other_cost*other_cost)-AVG(other_cost)*AVG(other_cost))/AVG(other_cost)*100,1) AS cv_othercost_pct,
  ROUND(SQRT(AVG(vas*vas)-AVG(vas)*AVG(vas))/AVG(vas)*100,1) AS cv_vas_pct,
  ROUND(SQRT(AVG(discount*discount)-AVG(discount)*AVG(discount))/AVG(discount)*100,1) AS cv_discount_pct
FROM monthly
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-006/attempt-01/sql/S12.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-006/attempt-01/sql/S12.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-006/attempt-01/results/S12.rows.jsonl)；完整：True；SHA256：`6d3b72ba93a57f59caa5b75e69776a9584d757d6f93836735c98c1b6032f759e`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "sheet1", "kind": "base", "block": null, "base_tables": ["sheet1"]}] | [] | ["STRFTIME('%Y-%m', \"Date\")"] |
| B2 | [{"alias": "monthly", "kind": "derived", "block": "B1", "base_tables": ["sheet1"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | SUM("Profit") | [{"table": "sheet1", "column": "Profit"}] | [] | False |
| B1 | SUM("Total Logistics Revenue") | [{"table": "sheet1", "column": "Total Logistics Revenue"}] | [] | False |
| B1 | SUM("Total Logistics Cost") | [{"table": "sheet1", "column": "Total Logistics Cost"}] | [] | False |
| B1 | SUM("Freight Cost") | [{"table": "sheet1", "column": "Freight Cost"}] | [] | False |
| B1 | SUM("Warehousing Cost") | [{"table": "sheet1", "column": "Warehousing Cost"}] | [] | False |
| B1 | SUM("Other Operating Costs") | [{"table": "sheet1", "column": "Other Operating Costs"}] | [] | False |
| B1 | SUM("Logistics Value-Added Service Revenue") | [{"table": "sheet1", "column": "Logistics Value-Added Service Revenue"}] | [] | False |
| B1 | SUM("Discount Amount") | [{"table": "sheet1", "column": "Discount Amount"}] | [] | False |
| B1 | SUM("Sales Quantity") | [{"table": "sheet1", "column": "Sales Quantity"}] | [] | False |
| B1 | COUNT(*) | [] | [] | True |
| B2 | AVG(total_profit) | [{"table": "sheet1", "column": "Profit"}] | [] | False |
| B2 | MIN(total_profit) | [{"table": "sheet1", "column": "Profit"}] | [] | False |
| B2 | MAX(total_profit) | [{"table": "sheet1", "column": "Profit"}] | [] | False |
| B2 | AVG(total_profit) | [{"table": "sheet1", "column": "Profit"}] | [] | False |
| B2 | AVG(total_profit) | [{"table": "sheet1", "column": "Profit"}] | [] | False |
| B2 | AVG(total_rev) | [{"table": "sheet1", "column": "Total Logistics Revenue"}] | [] | False |
| B2 | AVG(total_cost) | [{"table": "sheet1", "column": "Total Logistics Cost"}] | [] | False |
| B2 | AVG(qty) | [{"table": "sheet1", "column": "Sales Quantity"}] | [] | False |
| B2 | AVG(orders) | [] | [] | False |
| B2 | AVG(freight) | [{"table": "sheet1", "column": "Freight Cost"}] | [] | False |
| B2 | AVG(warehousing) | [{"table": "sheet1", "column": "Warehousing Cost"}] | [] | False |
| B2 | AVG(other_cost) | [{"table": "sheet1", "column": "Other Operating Costs"}] | [] | False |
| B2 | AVG(vas) | [{"table": "sheet1", "column": "Logistics Value-Added Service Revenue"}] | [] | False |
| B2 | AVG(discount) | [{"table": "sheet1", "column": "Discount Amount"}] | [] | False |
| B2 | MAX(total_profit) | [{"table": "sheet1", "column": "Profit"}] | [] | False |
| B2 | MIN(total_profit) | [{"table": "sheet1", "column": "Profit"}] | [] | False |
| B2 | AVG(total_profit * total_profit) | [{"table": "sheet1", "column": "Profit"}, {"table": "sheet1", "column": "Profit"}] | [] | False |
| B2 | AVG(total_rev * total_rev) | [{"table": "sheet1", "column": "Total Logistics Revenue"}, {"table": "sheet1", "column": "Total Logistics Revenue"}] | [] | False |
| B2 | AVG(total_cost * total_cost) | [{"table": "sheet1", "column": "Total Logistics Cost"}, {"table": "sheet1", "column": "Total Logistics Cost"}] | [] | False |
| B2 | AVG(qty * qty) | [{"table": "sheet1", "column": "Sales Quantity"}, {"table": "sheet1", "column": "Sales Quantity"}] | [] | False |
| B2 | AVG(orders * orders) | [] | [] | False |
| B2 | AVG(freight * freight) | [{"table": "sheet1", "column": "Freight Cost"}, {"table": "sheet1", "column": "Freight Cost"}] | [] | False |
| B2 | AVG(warehousing * warehousing) | [{"table": "sheet1", "column": "Warehousing Cost"}, {"table": "sheet1", "column": "Warehousing Cost"}] | [] | False |
| B2 | AVG(other_cost * other_cost) | [{"table": "sheet1", "column": "Other Operating Costs"}, {"table": "sheet1", "column": "Other Operating Costs"}] | [] | False |
| B2 | AVG(vas * vas) | [{"table": "sheet1", "column": "Logistics Value-Added Service Revenue"}, {"table": "sheet1", "column": "Logistics Value-Added Service Revenue"}] | [] | False |
| B2 | AVG(discount * discount) | [{"table": "sheet1", "column": "Discount Amount"}, {"table": "sheet1", "column": "Discount Amount"}] | [] | False |
| B2 | AVG(total_profit) | [{"table": "sheet1", "column": "Profit"}] | [] | False |
| B2 | AVG(total_profit) | [{"table": "sheet1", "column": "Profit"}] | [] | False |
| B2 | AVG(total_rev) | [{"table": "sheet1", "column": "Total Logistics Revenue"}] | [] | False |
| B2 | AVG(total_rev) | [{"table": "sheet1", "column": "Total Logistics Revenue"}] | [] | False |
| B2 | AVG(total_cost) | [{"table": "sheet1", "column": "Total Logistics Cost"}] | [] | False |
| B2 | AVG(total_cost) | [{"table": "sheet1", "column": "Total Logistics Cost"}] | [] | False |
| B2 | AVG(qty) | [{"table": "sheet1", "column": "Sales Quantity"}] | [] | False |
| B2 | AVG(qty) | [{"table": "sheet1", "column": "Sales Quantity"}] | [] | False |
| B2 | AVG(orders) | [] | [] | False |
| B2 | AVG(orders) | [] | [] | False |
| B2 | AVG(freight) | [{"table": "sheet1", "column": "Freight Cost"}] | [] | False |
| B2 | AVG(freight) | [{"table": "sheet1", "column": "Freight Cost"}] | [] | False |
| B2 | AVG(warehousing) | [{"table": "sheet1", "column": "Warehousing Cost"}] | [] | False |
| B2 | AVG(warehousing) | [{"table": "sheet1", "column": "Warehousing Cost"}] | [] | False |
| B2 | AVG(other_cost) | [{"table": "sheet1", "column": "Other Operating Costs"}] | [] | False |
| B2 | AVG(other_cost) | [{"table": "sheet1", "column": "Other Operating Costs"}] | [] | False |
| B2 | AVG(vas) | [{"table": "sheet1", "column": "Logistics Value-Added Service Revenue"}] | [] | False |
| B2 | AVG(vas) | [{"table": "sheet1", "column": "Logistics Value-Added Service Revenue"}] | [] | False |
| B2 | AVG(discount) | [{"table": "sheet1", "column": "Discount Amount"}] | [] | False |
| B2 | AVG(discount) | [{"table": "sheet1", "column": "Discount Amount"}] | [] | False |


## S13

类别 `data`；来源 `query_db`；调用 `0333c362d48449f58c58bd83a8558241`；状态 `success`。

```sql
WITH monthly AS (
  SELECT 
    "Consigned Product" AS dim,
    strftime('%Y-%m', "Date") AS month,
    SUM("Profit") AS total_profit,
    SUM("Sales Quantity") AS qty
  FROM sheet1
  WHERE "Destination" LIKE 'South China%'
  GROUP BY "Consigned Product", month
),
stats AS (
  SELECT dim,
    ROUND(AVG(total_profit),0) AS mean_profit,
    ROUND(SQRT(AVG(total_profit*total_profit)-AVG(total_profit)*AVG(total_profit)),0) AS sd_profit,
    ROUND(SQRT(AVG(total_profit*total_profit)-AVG(total_profit)*AVG(total_profit))/AVG(total_profit)*100,1) AS cv_pct,
    ROUND(SUM(total_profit),0) AS annual_profit,
    ROUND(SUM(total_profit) * 100.0 / (SELECT SUM("Profit") FROM sheet1 WHERE "Destination" LIKE 'South China%'),1) AS pct_of_total
  FROM monthly
  GROUP BY dim
)
SELECT * FROM stats ORDER BY cv_pct DESC
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-006/attempt-01/sql/S13.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-006/attempt-01/sql/S13.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-006/attempt-01/results/S13.rows.jsonl)；完整：True；SHA256：`57571d204f7095121a38864da16c62de6eb6969c374ca4f09f20c1c11d107beb`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "sheet1", "kind": "base", "block": null, "base_tables": ["sheet1"]}] | [] | ["\"Consigned Product\"", "STRFTIME('%Y-%m', \"Date\")"] |
| B2 | [{"alias": "sheet1", "kind": "base", "block": null, "base_tables": ["sheet1"]}] | [] | [] |
| B3 | [{"alias": "monthly", "kind": "derived", "block": "B1", "base_tables": ["sheet1"]}] | [] | ["dim"] |
| B4 | [{"alias": "stats", "kind": "derived", "block": "B3", "base_tables": ["sheet1"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | SUM("Profit") | [{"table": "sheet1", "column": "Profit"}] | [] | False |
| B1 | SUM("Sales Quantity") | [{"table": "sheet1", "column": "Sales Quantity"}] | [] | False |
| B2 | SUM("Profit") | [{"table": "sheet1", "column": "Profit"}] | [] | False |
| B3 | AVG(total_profit) | [{"table": "sheet1", "column": "Profit"}] | [] | False |
| B3 | SUM(total_profit) | [{"table": "sheet1", "column": "Profit"}] | [] | False |
| B3 | AVG(total_profit * total_profit) | [{"table": "sheet1", "column": "Profit"}, {"table": "sheet1", "column": "Profit"}] | [] | False |
| B3 | AVG(total_profit) | [{"table": "sheet1", "column": "Profit"}] | [] | False |
| B3 | SUM(total_profit) | [{"table": "sheet1", "column": "Profit"}] | [] | False |
| B3 | AVG(total_profit) | [{"table": "sheet1", "column": "Profit"}] | [] | False |
| B3 | AVG(total_profit) | [{"table": "sheet1", "column": "Profit"}] | [] | False |
| B3 | AVG(total_profit * total_profit) | [{"table": "sheet1", "column": "Profit"}, {"table": "sheet1", "column": "Profit"}] | [] | False |
| B3 | AVG(total_profit) | [{"table": "sheet1", "column": "Profit"}] | [] | False |
| B3 | AVG(total_profit) | [{"table": "sheet1", "column": "Profit"}] | [] | False |


未解析列血缘：[{"block": "B4", "column": "\"Profit\"", "reason": "ambiguous_or_missing_source"}, {"block": "B4", "column": "\"Destination\"", "reason": "ambiguous_or_missing_source"}]

## S14

类别 `data`；来源 `query_db`；调用 `fab0e1a7f6174394b880ffe50fa8a978`；状态 `success`。

```sql
WITH monthly AS (
  SELECT 
    "Destination" AS dim,
    strftime('%Y-%m', "Date") AS month,
    SUM("Profit") AS total_profit,
    SUM("Sales Quantity") AS qty
  FROM sheet1
  WHERE "Destination" LIKE 'South China%'
  GROUP BY "Destination", month
),
stats AS (
  SELECT dim,
    ROUND(AVG(total_profit),0) AS mean_profit,
    ROUND(SQRT(AVG(total_profit*total_profit)-AVG(total_profit)*AVG(total_profit)),0) AS sd_profit,
    ROUND(SQRT(AVG(total_profit*total_profit)-AVG(total_profit)*AVG(total_profit))/AVG(total_profit)*100,1) AS cv_pct,
    ROUND(SUM(total_profit),0) AS annual_profit,
    ROUND(SUM(total_profit) * 100.0 / (SELECT SUM("Profit") FROM sheet1 WHERE "Destination" LIKE 'South China%'),1) AS pct_of_total
  FROM monthly
  GROUP BY dim
)
SELECT * FROM stats ORDER BY cv_pct DESC
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-006/attempt-01/sql/S14.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-006/attempt-01/sql/S14.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-006/attempt-01/results/S14.rows.jsonl)；完整：True；SHA256：`12f5b43aa80605d5829dc9ff4e22dabceb67e09879bb0594df733e66a679fabc`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "sheet1", "kind": "base", "block": null, "base_tables": ["sheet1"]}] | [] | ["\"Destination\"", "STRFTIME('%Y-%m', \"Date\")"] |
| B2 | [{"alias": "sheet1", "kind": "base", "block": null, "base_tables": ["sheet1"]}] | [] | [] |
| B3 | [{"alias": "monthly", "kind": "derived", "block": "B1", "base_tables": ["sheet1"]}] | [] | ["dim"] |
| B4 | [{"alias": "stats", "kind": "derived", "block": "B3", "base_tables": ["sheet1"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | SUM("Profit") | [{"table": "sheet1", "column": "Profit"}] | [] | False |
| B1 | SUM("Sales Quantity") | [{"table": "sheet1", "column": "Sales Quantity"}] | [] | False |
| B2 | SUM("Profit") | [{"table": "sheet1", "column": "Profit"}] | [] | False |
| B3 | AVG(total_profit) | [{"table": "sheet1", "column": "Profit"}] | [] | False |
| B3 | SUM(total_profit) | [{"table": "sheet1", "column": "Profit"}] | [] | False |
| B3 | AVG(total_profit * total_profit) | [{"table": "sheet1", "column": "Profit"}, {"table": "sheet1", "column": "Profit"}] | [] | False |
| B3 | AVG(total_profit) | [{"table": "sheet1", "column": "Profit"}] | [] | False |
| B3 | SUM(total_profit) | [{"table": "sheet1", "column": "Profit"}] | [] | False |
| B3 | AVG(total_profit) | [{"table": "sheet1", "column": "Profit"}] | [] | False |
| B3 | AVG(total_profit) | [{"table": "sheet1", "column": "Profit"}] | [] | False |
| B3 | AVG(total_profit * total_profit) | [{"table": "sheet1", "column": "Profit"}, {"table": "sheet1", "column": "Profit"}] | [] | False |
| B3 | AVG(total_profit) | [{"table": "sheet1", "column": "Profit"}] | [] | False |
| B3 | AVG(total_profit) | [{"table": "sheet1", "column": "Profit"}] | [] | False |


未解析列血缘：[{"block": "B4", "column": "\"Profit\"", "reason": "ambiguous_or_missing_source"}, {"block": "B4", "column": "\"Destination\"", "reason": "ambiguous_or_missing_source"}]

## S15

类别 `data`；来源 `query_db`；调用 `77979e4aa16b40739853cc87398327e7`；状态 `success`。

```sql
WITH monthly AS (
  SELECT 
    "Customer Gender" AS dim,
    strftime('%Y-%m', "Date") AS month,
    SUM("Profit") AS total_profit,
    SUM("Sales Quantity") AS qty
  FROM sheet1
  WHERE "Destination" LIKE 'South China%'
  GROUP BY "Customer Gender", month
),
stats AS (
  SELECT dim,
    ROUND(AVG(total_profit),0) AS mean_profit,
    ROUND(SQRT(AVG(total_profit*total_profit)-AVG(total_profit)*AVG(total_profit)),0) AS sd_profit,
    ROUND(SQRT(AVG(total_profit*total_profit)-AVG(total_profit)*AVG(total_profit))/AVG(total_profit)*100,1) AS cv_pct,
    ROUND(SUM(total_profit),0) AS annual_profit,
    ROUND(SUM(total_profit) * 100.0 / (SELECT SUM("Profit") FROM sheet1 WHERE "Destination" LIKE 'South China%'),1) AS pct_of_total
  FROM monthly
  GROUP BY dim
)
SELECT * FROM stats ORDER BY cv_pct DESC
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-006/attempt-01/sql/S15.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-006/attempt-01/sql/S15.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-006/attempt-01/results/S15.rows.jsonl)；完整：True；SHA256：`1734db74c3cb0d8137f3d3003962da8b6b1332cb6dedb5c05d69f604e29ad699`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "sheet1", "kind": "base", "block": null, "base_tables": ["sheet1"]}] | [] | ["\"Customer Gender\"", "STRFTIME('%Y-%m', \"Date\")"] |
| B2 | [{"alias": "sheet1", "kind": "base", "block": null, "base_tables": ["sheet1"]}] | [] | [] |
| B3 | [{"alias": "monthly", "kind": "derived", "block": "B1", "base_tables": ["sheet1"]}] | [] | ["dim"] |
| B4 | [{"alias": "stats", "kind": "derived", "block": "B3", "base_tables": ["sheet1"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | SUM("Profit") | [{"table": "sheet1", "column": "Profit"}] | [] | False |
| B1 | SUM("Sales Quantity") | [{"table": "sheet1", "column": "Sales Quantity"}] | [] | False |
| B2 | SUM("Profit") | [{"table": "sheet1", "column": "Profit"}] | [] | False |
| B3 | AVG(total_profit) | [{"table": "sheet1", "column": "Profit"}] | [] | False |
| B3 | SUM(total_profit) | [{"table": "sheet1", "column": "Profit"}] | [] | False |
| B3 | AVG(total_profit * total_profit) | [{"table": "sheet1", "column": "Profit"}, {"table": "sheet1", "column": "Profit"}] | [] | False |
| B3 | AVG(total_profit) | [{"table": "sheet1", "column": "Profit"}] | [] | False |
| B3 | SUM(total_profit) | [{"table": "sheet1", "column": "Profit"}] | [] | False |
| B3 | AVG(total_profit) | [{"table": "sheet1", "column": "Profit"}] | [] | False |
| B3 | AVG(total_profit) | [{"table": "sheet1", "column": "Profit"}] | [] | False |
| B3 | AVG(total_profit * total_profit) | [{"table": "sheet1", "column": "Profit"}, {"table": "sheet1", "column": "Profit"}] | [] | False |
| B3 | AVG(total_profit) | [{"table": "sheet1", "column": "Profit"}] | [] | False |
| B3 | AVG(total_profit) | [{"table": "sheet1", "column": "Profit"}] | [] | False |


未解析列血缘：[{"block": "B4", "column": "\"Profit\"", "reason": "ambiguous_or_missing_source"}, {"block": "B4", "column": "\"Destination\"", "reason": "ambiguous_or_missing_source"}]

## S16

类别 `data`；来源 `query_db`；调用 `a2881c7a0b3049e1b33a871d1663953c`；状态 `success`。

```sql
WITH monthly AS (
  SELECT 
    "Age Range" AS dim,
    strftime('%Y-%m', "Date") AS month,
    SUM("Profit") AS total_profit,
    SUM("Sales Quantity") AS qty
  FROM sheet1
  WHERE "Destination" LIKE 'South China%'
  GROUP BY "Age Range", month
),
stats AS (
  SELECT dim,
    ROUND(AVG(total_profit),0) AS mean_profit,
    ROUND(SQRT(AVG(total_profit*total_profit)-AVG(total_profit)*AVG(total_profit)),0) AS sd_profit,
    ROUND(SQRT(AVG(total_profit*total_profit)-AVG(total_profit)*AVG(total_profit))/AVG(total_profit)*100,1) AS cv_pct,
    ROUND(SUM(total_profit),0) AS annual_profit,
    ROUND(SUM(total_profit) * 100.0 / (SELECT SUM("Profit") FROM sheet1 WHERE "Destination" LIKE 'South China%'),1) AS pct_of_total
  FROM monthly
  GROUP BY dim
)
SELECT * FROM stats ORDER BY cv_pct DESC
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-006/attempt-01/sql/S16.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-006/attempt-01/sql/S16.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-006/attempt-01/results/S16.rows.jsonl)；完整：True；SHA256：`54b67e4a147fdb9508c1d155183979a173bbd3eb1d57a37eda9638adce23c070`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "sheet1", "kind": "base", "block": null, "base_tables": ["sheet1"]}] | [] | ["\"Age Range\"", "STRFTIME('%Y-%m', \"Date\")"] |
| B2 | [{"alias": "sheet1", "kind": "base", "block": null, "base_tables": ["sheet1"]}] | [] | [] |
| B3 | [{"alias": "monthly", "kind": "derived", "block": "B1", "base_tables": ["sheet1"]}] | [] | ["dim"] |
| B4 | [{"alias": "stats", "kind": "derived", "block": "B3", "base_tables": ["sheet1"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | SUM("Profit") | [{"table": "sheet1", "column": "Profit"}] | [] | False |
| B1 | SUM("Sales Quantity") | [{"table": "sheet1", "column": "Sales Quantity"}] | [] | False |
| B2 | SUM("Profit") | [{"table": "sheet1", "column": "Profit"}] | [] | False |
| B3 | AVG(total_profit) | [{"table": "sheet1", "column": "Profit"}] | [] | False |
| B3 | SUM(total_profit) | [{"table": "sheet1", "column": "Profit"}] | [] | False |
| B3 | AVG(total_profit * total_profit) | [{"table": "sheet1", "column": "Profit"}, {"table": "sheet1", "column": "Profit"}] | [] | False |
| B3 | AVG(total_profit) | [{"table": "sheet1", "column": "Profit"}] | [] | False |
| B3 | SUM(total_profit) | [{"table": "sheet1", "column": "Profit"}] | [] | False |
| B3 | AVG(total_profit) | [{"table": "sheet1", "column": "Profit"}] | [] | False |
| B3 | AVG(total_profit) | [{"table": "sheet1", "column": "Profit"}] | [] | False |
| B3 | AVG(total_profit * total_profit) | [{"table": "sheet1", "column": "Profit"}, {"table": "sheet1", "column": "Profit"}] | [] | False |
| B3 | AVG(total_profit) | [{"table": "sheet1", "column": "Profit"}] | [] | False |
| B3 | AVG(total_profit) | [{"table": "sheet1", "column": "Profit"}] | [] | False |


未解析列血缘：[{"block": "B4", "column": "\"Profit\"", "reason": "ambiguous_or_missing_source"}, {"block": "B4", "column": "\"Destination\"", "reason": "ambiguous_or_missing_source"}]

## S17

类别 `data`；来源 `query_db`；调用 `9975c8ec5df64705af5ef74add9eb0d7`；状态 `failed`。

```sql
SELECT 
  substr("Destination", 13, instr("Destination", '-', 13) - 13) AS province,
  COUNT(*) AS n,
  SUM("Profit") AS profit
FROM sheet1
WHERE "Destination" LIKE 'South China%'
GROUP BY province
ORDER BY profit DESC
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-006/attempt-01/sql/S17.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-006/attempt-01/sql/S17.parameters.json)。

错误：`OperationalError('wrong number of arguments to function instr()')`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "sheet1", "kind": "base", "block": null, "base_tables": ["sheet1"]}] | [] | ["SUBSTRING(\"Destination\", 13, IIF(INSTR(SUBSTRING(\"Destination\", 13), '-') = 0, 0, INSTR(SUBSTRING(\"Destination\", 13), '-') + 13 - 1) - 13)"] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |
| B1 | SUM("Profit") | [{"table": "sheet1", "column": "Profit"}] | [] | False |


## S18

类别 `data`；来源 `query_db`；调用 `5c5345f7d4d740709aabfcad5b01dedc`；状态 `success`。

```sql
SELECT "Destination" FROM sheet1 WHERE "Destination" LIKE 'South China%' GROUP BY "Destination" ORDER BY "Destination"
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-006/attempt-01/sql/S18.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-006/attempt-01/sql/S18.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-006/attempt-01/results/S18.rows.jsonl)；完整：True；SHA256：`d54f191beb2c5dcd4985430fa50c44458206feacbbd482d7d16d8db0c30b0ccd`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "sheet1", "kind": "base", "block": null, "base_tables": ["sheet1"]}] | [] | ["\"Destination\""] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |


## S19

类别 `data`；来源 `query_db`；调用 `86c68b5448f34d1390100a31e114a252`；状态 `success`。

```sql
SELECT 
  substr("Destination", 13, instr(substr("Destination", 13), '-') - 1) AS province,
  COUNT(*) AS n,
  ROUND(SUM("Profit"),0) AS profit
FROM sheet1
WHERE "Destination" LIKE 'South China%'
GROUP BY province
ORDER BY profit DESC
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-006/attempt-01/sql/S19.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-006/attempt-01/sql/S19.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-006/attempt-01/results/S19.rows.jsonl)；完整：True；SHA256：`57df72ff1bd01d3377ecf8374610acf288783cd6d60ff59d9396ec9144d06db1`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "sheet1", "kind": "base", "block": null, "base_tables": ["sheet1"]}] | [] | ["SUBSTRING(\"Destination\", 13, INSTR(SUBSTRING(\"Destination\", 13), '-') - 1)"] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |
| B1 | SUM("Profit") | [{"table": "sheet1", "column": "Profit"}] | [] | False |


## S20

类别 `data`；来源 `query_db`；调用 `e7b4d6ef841f4e02a5d99f85fac0209e`；状态 `success`。

```sql
WITH monthly AS (
  SELECT 
    substr("Destination", 13, instr(substr("Destination", 13), '-') - 1) AS province,
    strftime('%Y-%m', "Date") AS month,
    SUM("Profit") AS total_profit,
    SUM("Sales Quantity") AS qty,
    COUNT(*) AS orders
  FROM sheet1
  WHERE "Destination" LIKE 'South China%'
  GROUP BY province, month
)
SELECT province,
  COUNT(*) AS months,
  ROUND(AVG(total_profit),0) AS mean_profit,
  ROUND(MIN(total_profit),0) AS min_profit,
  ROUND(MAX(total_profit),0) AS max_profit,
  ROUND(SQRT(AVG(total_profit*total_profit)-AVG(total_profit)*AVG(total_profit)),0) AS sd_profit,
  ROUND(SQRT(AVG(total_profit*total_profit)-AVG(total_profit)*AVG(total_profit))/AVG(total_profit)*100,1) AS cv_pct,
  ROUND(SUM(total_profit),0) AS annual_profit
FROM monthly
GROUP BY province
ORDER BY cv_pct DESC
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-006/attempt-01/sql/S20.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-006/attempt-01/sql/S20.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-006/attempt-01/results/S20.rows.jsonl)；完整：True；SHA256：`367bf41fdd2d11ca9f8b1776b2773348b358a78c87730bd5d56fc53a0145d7d6`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "sheet1", "kind": "base", "block": null, "base_tables": ["sheet1"]}] | [] | ["SUBSTRING(\"Destination\", 13, INSTR(SUBSTRING(\"Destination\", 13), '-') - 1)", "STRFTIME('%Y-%m', \"Date\")"] |
| B2 | [{"alias": "monthly", "kind": "derived", "block": "B1", "base_tables": ["sheet1"]}] | [] | ["province"] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | SUM("Profit") | [{"table": "sheet1", "column": "Profit"}] | [] | False |
| B1 | SUM("Sales Quantity") | [{"table": "sheet1", "column": "Sales Quantity"}] | [] | False |
| B1 | COUNT(*) | [] | [] | True |
| B2 | COUNT(*) | [] | [] | True |
| B2 | AVG(total_profit) | [{"table": "sheet1", "column": "Profit"}] | [] | False |
| B2 | MIN(total_profit) | [{"table": "sheet1", "column": "Profit"}] | [] | False |
| B2 | MAX(total_profit) | [{"table": "sheet1", "column": "Profit"}] | [] | False |
| B2 | SUM(total_profit) | [{"table": "sheet1", "column": "Profit"}] | [] | False |
| B2 | AVG(total_profit * total_profit) | [{"table": "sheet1", "column": "Profit"}, {"table": "sheet1", "column": "Profit"}] | [] | False |
| B2 | AVG(total_profit) | [{"table": "sheet1", "column": "Profit"}] | [] | False |
| B2 | AVG(total_profit) | [{"table": "sheet1", "column": "Profit"}] | [] | False |
| B2 | AVG(total_profit) | [{"table": "sheet1", "column": "Profit"}] | [] | False |
| B2 | AVG(total_profit * total_profit) | [{"table": "sheet1", "column": "Profit"}, {"table": "sheet1", "column": "Profit"}] | [] | False |
| B2 | AVG(total_profit) | [{"table": "sheet1", "column": "Profit"}] | [] | False |
| B2 | AVG(total_profit) | [{"table": "sheet1", "column": "Profit"}] | [] | False |


## S21

类别 `data`；来源 `query_db`；调用 `4ea6b643ee25476b99c15d612ae4534a`；状态 `success`。

```sql
WITH prod_month AS (
  SELECT "Consigned Product" AS dim, strftime('%Y-%m',"Date") AS month, SUM("Profit") AS p
  FROM sheet1 WHERE "Destination" LIKE 'South China%' GROUP BY 1,2
),
tot_month AS (
  SELECT strftime('%Y-%m',"Date") AS month, SUM("Profit") AS t
  FROM sheet1 WHERE "Destination" LIKE 'South China%' GROUP BY 1
),
cov AS (
  SELECT dim,
    SUM((p - (SELECT AVG(p) FROM prod_month p2 WHERE p2.dim=prod_month.dim)) * (t - (SELECT AVG(t) FROM tot_month))) / 12.0 AS cov_p_t,
    (SELECT SUM((t - (SELECT AVG(t) FROM tot_month))*(t - (SELECT AVG(t) FROM tot_month))) / 12.0 FROM tot_month) AS var_t
  FROM prod_month JOIN tot_month USING(month)
  GROUP BY dim
)
SELECT dim, ROUND(cov_p_t/var_t*100,1) AS variance_share_pct FROM cov ORDER BY variance_share_pct DESC
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-006/attempt-01/sql/S21.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-006/attempt-01/sql/S21.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-006/attempt-01/results/S21.rows.jsonl)；完整：True；SHA256：`71d61717e5654af267ab98f845c81e0c432bffbcafe953fbb89a81b845afa858`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "sheet1", "kind": "base", "block": null, "base_tables": ["sheet1"]}] | [] | ["\"Consigned Product\"", "STRFTIME('%Y-%m', \"Date\")"] |
| B2 | [{"alias": "sheet1", "kind": "base", "block": null, "base_tables": ["sheet1"]}] | [] | ["STRFTIME('%Y-%m', \"Date\")"] |
| B3 | [{"alias": "p2", "kind": "derived", "block": "B1", "base_tables": ["sheet1"]}] | [] | [] |
| B4 | [{"alias": "tot_month", "kind": "derived", "block": "B2", "base_tables": ["sheet1"]}] | [] | [] |
| B5 | [{"alias": "tot_month", "kind": "derived", "block": "B2", "base_tables": ["sheet1"]}] | [] | [] |
| B6 | [{"alias": "tot_month", "kind": "derived", "block": "B2", "base_tables": ["sheet1"]}] | [] | [] |
| B7 | [{"alias": "tot_month", "kind": "derived", "block": "B2", "base_tables": ["sheet1"]}] | [] | [] |
| B8 | [{"alias": "prod_month", "kind": "derived", "block": "B1", "base_tables": ["sheet1"]}, {"alias": "tot_month", "kind": "derived", "block": "B2", "base_tables": ["sheet1"]}] | [{"type": "INNER", "right": "tot_month", "on": null, "using": ["month"]}] | ["dim"] |
| B9 | [{"alias": "cov", "kind": "derived", "block": "B8", "base_tables": ["sheet1"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | SUM("Profit") | [{"table": "sheet1", "column": "Profit"}] | [] | False |
| B2 | SUM("Profit") | [{"table": "sheet1", "column": "Profit"}] | [] | False |
| B3 | AVG(p) | [{"table": "sheet1", "column": "Profit"}] | [] | False |
| B4 | AVG(t) | [{"table": "sheet1", "column": "Profit"}] | [] | False |
| B5 | AVG(t) | [{"table": "sheet1", "column": "Profit"}] | [] | False |
| B6 | AVG(t) | [{"table": "sheet1", "column": "Profit"}] | [] | False |
| B7 | SUM((t - (SELECT AVG(t) FROM tot_month)) * (t - (SELECT AVG(t) FROM tot_month))) | [{"table": "sheet1", "column": "Profit"}, {"table": "sheet1", "column": "Profit"}, {"table": "sheet1", "column": "Profit"}, {"table": "sheet1", "column": "Profit"}] | [] | False |
| B8 | SUM((p - (SELECT AVG(p) FROM prod_month AS p2 WHERE p2.dim = prod_month.dim)) * (t - (SELECT AVG(t) FROM tot_month))) | [{"table": "sheet1", "column": "Profit"}, {"table": "sheet1", "column": "Profit"}, {"table": "sheet1", "column": "Profit"}, {"table": "sheet1", "column": "Profit"}, {"table": "sheet1", "column": "Consigned Product"}, {"table": "sheet1", "column": "Consigned Product"}] | [] | False |


## S22

类别 `data`；来源 `query_db`；调用 `402a0ffbf648403a986486f8dffcf90d`；状态 `success`。

```sql
WITH prov_month AS (
  SELECT substr("Destination", 13, instr(substr("Destination", 13), '-') - 1) AS dim, strftime('%Y-%m',"Date") AS month, SUM("Profit") AS p
  FROM sheet1 WHERE "Destination" LIKE 'South China%' GROUP BY 1,2
),
tot_month AS (
  SELECT strftime('%Y-%m',"Date") AS month, SUM("Profit") AS t
  FROM sheet1 WHERE "Destination" LIKE 'South China%' GROUP BY 1
)
SELECT dim,
  ROUND(SUM((p - (SELECT AVG(p) FROM prov_month p2 WHERE p2.dim=prov_month.dim)) * (t - (SELECT AVG(t) FROM tot_month))) / 12.0
    / (SELECT SUM((t - (SELECT AVG(t) FROM tot_month))*(t - (SELECT AVG(t) FROM tot_month))) / 12.0 FROM tot_month) * 100, 1) AS variance_share_pct
FROM prov_month JOIN tot_month USING(month)
GROUP BY dim ORDER BY variance_share_pct DESC
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-006/attempt-01/sql/S22.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-006/attempt-01/sql/S22.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-006/attempt-01/results/S22.rows.jsonl)；完整：True；SHA256：`64c450f9b51d36587d922a11959ca6875719d728732341733e6988d083bf9c07`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "sheet1", "kind": "base", "block": null, "base_tables": ["sheet1"]}] | [] | ["SUBSTRING(\"Destination\", 13, INSTR(SUBSTRING(\"Destination\", 13), '-') - 1)", "STRFTIME('%Y-%m', \"Date\")"] |
| B2 | [{"alias": "sheet1", "kind": "base", "block": null, "base_tables": ["sheet1"]}] | [] | ["STRFTIME('%Y-%m', \"Date\")"] |
| B3 | [{"alias": "p2", "kind": "derived", "block": "B1", "base_tables": ["sheet1"]}] | [] | [] |
| B4 | [{"alias": "tot_month", "kind": "derived", "block": "B2", "base_tables": ["sheet1"]}] | [] | [] |
| B5 | [{"alias": "tot_month", "kind": "derived", "block": "B2", "base_tables": ["sheet1"]}] | [] | [] |
| B6 | [{"alias": "tot_month", "kind": "derived", "block": "B2", "base_tables": ["sheet1"]}] | [] | [] |
| B7 | [{"alias": "tot_month", "kind": "derived", "block": "B2", "base_tables": ["sheet1"]}] | [] | [] |
| B8 | [{"alias": "prov_month", "kind": "derived", "block": "B1", "base_tables": ["sheet1"]}, {"alias": "tot_month", "kind": "derived", "block": "B2", "base_tables": ["sheet1"]}] | [{"type": "INNER", "right": "tot_month", "on": null, "using": ["month"]}] | ["dim"] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | SUM("Profit") | [{"table": "sheet1", "column": "Profit"}] | [] | False |
| B2 | SUM("Profit") | [{"table": "sheet1", "column": "Profit"}] | [] | False |
| B3 | AVG(p) | [{"table": "sheet1", "column": "Profit"}] | [] | False |
| B4 | AVG(t) | [{"table": "sheet1", "column": "Profit"}] | [] | False |
| B5 | AVG(t) | [{"table": "sheet1", "column": "Profit"}] | [] | False |
| B6 | AVG(t) | [{"table": "sheet1", "column": "Profit"}] | [] | False |
| B7 | SUM((t - (SELECT AVG(t) FROM tot_month)) * (t - (SELECT AVG(t) FROM tot_month))) | [{"table": "sheet1", "column": "Profit"}, {"table": "sheet1", "column": "Profit"}, {"table": "sheet1", "column": "Profit"}, {"table": "sheet1", "column": "Profit"}] | [] | False |
| B8 | SUM((p - (SELECT AVG(p) FROM prov_month AS p2 WHERE p2.dim = prov_month.dim)) * (t - (SELECT AVG(t) FROM tot_month))) | [{"table": "sheet1", "column": "Profit"}, {"table": "sheet1", "column": "Profit"}, {"table": "sheet1", "column": "Profit"}, {"table": "sheet1", "column": "Profit"}, {"table": "sheet1", "column": "Destination"}, {"table": "sheet1", "column": "Destination"}, {"table": "sheet1", "column": "Destination"}, {"table": "sheet1", "column": "Destination"}] | [] | False |


## S23

类别 `data`；来源 `query_db`；调用 `965b7acae41d44a3b291abce37ebe200`；状态 `success`。

```sql
WITH age_month AS (
  SELECT "Age Range" AS dim, strftime('%Y-%m',"Date") AS month, SUM("Profit") AS p
  FROM sheet1 WHERE "Destination" LIKE 'South China%' GROUP BY 1,2
),
tot_month AS (
  SELECT strftime('%Y-%m',"Date") AS month, SUM("Profit") AS t
  FROM sheet1 WHERE "Destination" LIKE 'South China%' GROUP BY 1
)
SELECT dim,
  ROUND(SUM((p - (SELECT AVG(p) FROM age_month p2 WHERE p2.dim=age_month.dim)) * (t - (SELECT AVG(t) FROM tot_month))) / 12.0
    / (SELECT SUM((t - (SELECT AVG(t) FROM tot_month))*(t - (SELECT AVG(t) FROM tot_month))) / 12.0 FROM tot_month) * 100, 1) AS variance_share_pct
FROM age_month JOIN tot_month USING(month)
GROUP BY dim ORDER BY variance_share_pct DESC
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-006/attempt-01/sql/S23.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-006/attempt-01/sql/S23.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-006/attempt-01/results/S23.rows.jsonl)；完整：True；SHA256：`e434295c5afb06d94987f9d9536f05c7098c6607194059305cf5933085f7c5fc`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "sheet1", "kind": "base", "block": null, "base_tables": ["sheet1"]}] | [] | ["\"Age Range\"", "STRFTIME('%Y-%m', \"Date\")"] |
| B2 | [{"alias": "sheet1", "kind": "base", "block": null, "base_tables": ["sheet1"]}] | [] | ["STRFTIME('%Y-%m', \"Date\")"] |
| B3 | [{"alias": "p2", "kind": "derived", "block": "B1", "base_tables": ["sheet1"]}] | [] | [] |
| B4 | [{"alias": "tot_month", "kind": "derived", "block": "B2", "base_tables": ["sheet1"]}] | [] | [] |
| B5 | [{"alias": "tot_month", "kind": "derived", "block": "B2", "base_tables": ["sheet1"]}] | [] | [] |
| B6 | [{"alias": "tot_month", "kind": "derived", "block": "B2", "base_tables": ["sheet1"]}] | [] | [] |
| B7 | [{"alias": "tot_month", "kind": "derived", "block": "B2", "base_tables": ["sheet1"]}] | [] | [] |
| B8 | [{"alias": "age_month", "kind": "derived", "block": "B1", "base_tables": ["sheet1"]}, {"alias": "tot_month", "kind": "derived", "block": "B2", "base_tables": ["sheet1"]}] | [{"type": "INNER", "right": "tot_month", "on": null, "using": ["month"]}] | ["dim"] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | SUM("Profit") | [{"table": "sheet1", "column": "Profit"}] | [] | False |
| B2 | SUM("Profit") | [{"table": "sheet1", "column": "Profit"}] | [] | False |
| B3 | AVG(p) | [{"table": "sheet1", "column": "Profit"}] | [] | False |
| B4 | AVG(t) | [{"table": "sheet1", "column": "Profit"}] | [] | False |
| B5 | AVG(t) | [{"table": "sheet1", "column": "Profit"}] | [] | False |
| B6 | AVG(t) | [{"table": "sheet1", "column": "Profit"}] | [] | False |
| B7 | SUM((t - (SELECT AVG(t) FROM tot_month)) * (t - (SELECT AVG(t) FROM tot_month))) | [{"table": "sheet1", "column": "Profit"}, {"table": "sheet1", "column": "Profit"}, {"table": "sheet1", "column": "Profit"}, {"table": "sheet1", "column": "Profit"}] | [] | False |
| B8 | SUM((p - (SELECT AVG(p) FROM age_month AS p2 WHERE p2.dim = age_month.dim)) * (t - (SELECT AVG(t) FROM tot_month))) | [{"table": "sheet1", "column": "Profit"}, {"table": "sheet1", "column": "Profit"}, {"table": "sheet1", "column": "Profit"}, {"table": "sheet1", "column": "Profit"}, {"table": "sheet1", "column": "Age Range"}, {"table": "sheet1", "column": "Age Range"}] | [] | False |


## S24

类别 `data`；来源 `query_db`；调用 `8904e316bf924f50ba1c2cd6532c0c03`；状态 `success`。

```sql
WITH g_month AS (
  SELECT "Customer Gender" AS dim, strftime('%Y-%m',"Date") AS month, SUM("Profit") AS p
  FROM sheet1 WHERE "Destination" LIKE 'South China%' GROUP BY 1,2
),
tot_month AS (
  SELECT strftime('%Y-%m',"Date") AS month, SUM("Profit") AS t
  FROM sheet1 WHERE "Destination" LIKE 'South China%' GROUP BY 1
)
SELECT dim,
  ROUND(SUM((p - (SELECT AVG(p) FROM g_month p2 WHERE p2.dim=g_month.dim)) * (t - (SELECT AVG(t) FROM tot_month))) / 12.0
    / (SELECT SUM((t - (SELECT AVG(t) FROM tot_month))*(t - (SELECT AVG(t) FROM tot_month))) / 12.0 FROM tot_month) * 100, 1) AS variance_share_pct
FROM g_month JOIN tot_month USING(month)
GROUP BY dim ORDER BY variance_share_pct DESC
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-006/attempt-01/sql/S24.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-006/attempt-01/sql/S24.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-006/attempt-01/results/S24.rows.jsonl)；完整：True；SHA256：`0a7c8128c8beb8aee50cb2dbf63c3055939c1c8b82afb51ee57faf370f98915f`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "sheet1", "kind": "base", "block": null, "base_tables": ["sheet1"]}] | [] | ["\"Customer Gender\"", "STRFTIME('%Y-%m', \"Date\")"] |
| B2 | [{"alias": "sheet1", "kind": "base", "block": null, "base_tables": ["sheet1"]}] | [] | ["STRFTIME('%Y-%m', \"Date\")"] |
| B3 | [{"alias": "p2", "kind": "derived", "block": "B1", "base_tables": ["sheet1"]}] | [] | [] |
| B4 | [{"alias": "tot_month", "kind": "derived", "block": "B2", "base_tables": ["sheet1"]}] | [] | [] |
| B5 | [{"alias": "tot_month", "kind": "derived", "block": "B2", "base_tables": ["sheet1"]}] | [] | [] |
| B6 | [{"alias": "tot_month", "kind": "derived", "block": "B2", "base_tables": ["sheet1"]}] | [] | [] |
| B7 | [{"alias": "tot_month", "kind": "derived", "block": "B2", "base_tables": ["sheet1"]}] | [] | [] |
| B8 | [{"alias": "g_month", "kind": "derived", "block": "B1", "base_tables": ["sheet1"]}, {"alias": "tot_month", "kind": "derived", "block": "B2", "base_tables": ["sheet1"]}] | [{"type": "INNER", "right": "tot_month", "on": null, "using": ["month"]}] | ["dim"] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | SUM("Profit") | [{"table": "sheet1", "column": "Profit"}] | [] | False |
| B2 | SUM("Profit") | [{"table": "sheet1", "column": "Profit"}] | [] | False |
| B3 | AVG(p) | [{"table": "sheet1", "column": "Profit"}] | [] | False |
| B4 | AVG(t) | [{"table": "sheet1", "column": "Profit"}] | [] | False |
| B5 | AVG(t) | [{"table": "sheet1", "column": "Profit"}] | [] | False |
| B6 | AVG(t) | [{"table": "sheet1", "column": "Profit"}] | [] | False |
| B7 | SUM((t - (SELECT AVG(t) FROM tot_month)) * (t - (SELECT AVG(t) FROM tot_month))) | [{"table": "sheet1", "column": "Profit"}, {"table": "sheet1", "column": "Profit"}, {"table": "sheet1", "column": "Profit"}, {"table": "sheet1", "column": "Profit"}] | [] | False |
| B8 | SUM((p - (SELECT AVG(p) FROM g_month AS p2 WHERE p2.dim = g_month.dim)) * (t - (SELECT AVG(t) FROM tot_month))) | [{"table": "sheet1", "column": "Profit"}, {"table": "sheet1", "column": "Profit"}, {"table": "sheet1", "column": "Profit"}, {"table": "sheet1", "column": "Profit"}, {"table": "sheet1", "column": "Customer Gender"}, {"table": "sheet1", "column": "Customer Gender"}] | [] | False |


## S25

类别 `data`；来源 `query_db`；调用 `2951f4ee71b14b748c511b32c4b78b98`；状态 `success`。

```sql
WITH rev_month AS (
  SELECT strftime('%Y-%m',"Date") AS month,
    SUM("Total Logistics Revenue") AS rev,
    SUM("List Price Revenue") AS list_price,
    SUM("Logistics Value-Added Service Revenue") AS vas,
    SUM("Discount Amount") AS discount,
    SUM("Total Logistics Cost") AS cost,
    SUM("Freight Cost") AS freight,
    SUM("Warehousing Cost") AS warehousing,
    SUM("Other Operating Costs") AS other_cost,
    SUM("Profit") AS profit
  FROM sheet1 WHERE "Destination" LIKE 'South China%'
  GROUP BY 1
)
SELECT month, ROUND(rev,0) AS rev, ROUND(profit,0) AS profit, ROUND(cost,0) AS cost,
  ROUND(discount,0) AS discount, ROUND(freight,0) AS freight, ROUND(warehousing,0) AS warehousing,
  ROUND(other_cost,0) AS other_cost, ROUND(vas,0) AS vas
FROM rev_month ORDER BY month
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-006/attempt-01/sql/S25.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-006/attempt-01/sql/S25.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-006/attempt-01/results/S25.rows.jsonl)；完整：True；SHA256：`c425769d9dad1b399e871b535b19034da34a35938d6703fd414ae49ef621d52e`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "sheet1", "kind": "base", "block": null, "base_tables": ["sheet1"]}] | [] | ["STRFTIME('%Y-%m', \"Date\")"] |
| B2 | [{"alias": "rev_month", "kind": "derived", "block": "B1", "base_tables": ["sheet1"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | SUM("Total Logistics Revenue") | [{"table": "sheet1", "column": "Total Logistics Revenue"}] | [] | False |
| B1 | SUM("List Price Revenue") | [{"table": "sheet1", "column": "List Price Revenue"}] | [] | False |
| B1 | SUM("Logistics Value-Added Service Revenue") | [{"table": "sheet1", "column": "Logistics Value-Added Service Revenue"}] | [] | False |
| B1 | SUM("Discount Amount") | [{"table": "sheet1", "column": "Discount Amount"}] | [] | False |
| B1 | SUM("Total Logistics Cost") | [{"table": "sheet1", "column": "Total Logistics Cost"}] | [] | False |
| B1 | SUM("Freight Cost") | [{"table": "sheet1", "column": "Freight Cost"}] | [] | False |
| B1 | SUM("Warehousing Cost") | [{"table": "sheet1", "column": "Warehousing Cost"}] | [] | False |
| B1 | SUM("Other Operating Costs") | [{"table": "sheet1", "column": "Other Operating Costs"}] | [] | False |
| B1 | SUM("Profit") | [{"table": "sheet1", "column": "Profit"}] | [] | False |


## S26

类别 `data`；来源 `query_db`；调用 `17c027a01cc24d279558dfedfaefb8c4`；状态 `success`。

```sql
WITH monthly AS (
  SELECT strftime('%Y-%m', "Date") AS month, SUM("Profit") AS total_profit
  FROM sheet1 WHERE "Destination" LIKE 'South China%'
  GROUP BY month
)
SELECT a.month, ROUND(a.total_profit,0) AS profit, 
  ROUND(a.total_profit - b.total_profit,0) AS change_from_prev,
  ROUND((a.total_profit - b.total_profit)/b.total_profit*100,1) AS pct_change
FROM monthly a
LEFT JOIN monthly b ON a.month = (SELECT MAX(month) FROM monthly m2 WHERE m2.month < a.month)
ORDER BY a.month
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-006/attempt-01/sql/S26.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-006/attempt-01/sql/S26.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-006/attempt-01/results/S26.rows.jsonl)；完整：True；SHA256：`3c2168c11f68ee4f349c829ca91a60848851acbb688bca0ada1fedbb53cab71d`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "sheet1", "kind": "base", "block": null, "base_tables": ["sheet1"]}] | [] | ["STRFTIME('%Y-%m', \"Date\")"] |
| B2 | [{"alias": "m2", "kind": "derived", "block": "B1", "base_tables": ["sheet1"]}] | [] | [] |
| B3 | [{"alias": "a", "kind": "derived", "block": "B1", "base_tables": ["sheet1"]}, {"alias": "b", "kind": "derived", "block": "B1", "base_tables": ["sheet1"]}] | [{"type": "LEFT", "right": "monthly AS b", "on": "a.month = (SELECT MAX(month) FROM monthly AS m2 WHERE m2.month < a.month)", "using": []}] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | SUM("Profit") | [{"table": "sheet1", "column": "Profit"}] | [] | False |
| B2 | MAX(month) | [{"table": "sheet1", "column": "Date"}] | [] | False |


未解析列血缘：[{"block": "B3", "column": "month", "reason": "ambiguous_or_missing_source"}]

## S27

类别 `data`；来源 `query_db`；调用 `d4bbb57661564554b53e1dffd6297085`；状态 `success`。

```sql
WITH monthly AS (
  SELECT strftime('%Y-%m', "Date") AS month, SUM("Profit") AS total_profit
  FROM sheet1 WHERE "Destination" LIKE 'South China%'
  GROUP BY month
)
SELECT month, ROUND(total_profit,0) AS profit,
  ROUND(total_profit - LAG(total_profit) OVER (ORDER BY month),0) AS change_from_prev,
  ROUND((total_profit - LAG(total_profit) OVER (ORDER BY month))/LAG(total_profit) OVER (ORDER BY month)*100,1) AS pct_change
FROM monthly ORDER BY month
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-006/attempt-01/sql/S27.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-006/attempt-01/sql/S27.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-006/attempt-01/results/S27.rows.jsonl)；完整：True；SHA256：`b20884d08d922d4f1829fc32483a4327dee8db8daef27f60c51493a763f73388`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "sheet1", "kind": "base", "block": null, "base_tables": ["sheet1"]}] | [] | ["STRFTIME('%Y-%m', \"Date\")"] |
| B2 | [{"alias": "monthly", "kind": "derived", "block": "B1", "base_tables": ["sheet1"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | SUM("Profit") | [{"table": "sheet1", "column": "Profit"}] | [] | False |


## S28

类别 `data`；来源 `query_db`；调用 `e990eb36924947e18e6357499fbae108`；状态 `success`。

```sql
WITH pm AS (
  SELECT "Consigned Product" AS dim, strftime('%Y-%m',"Date") AS month, SUM("Profit") AS p
  FROM sheet1 WHERE "Destination" LIKE 'South China%' GROUP BY 1,2
)
SELECT dim, month, ROUND(p,0) AS profit, 
  ROUND(p - LAG(p) OVER (PARTITION BY dim ORDER BY month),0) AS chg
FROM pm ORDER BY dim, month
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-006/attempt-01/sql/S28.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-006/attempt-01/sql/S28.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-006/attempt-01/results/S28.rows.jsonl)；完整：True；SHA256：`54ec38e0e9c0819ff42176bb86f06e94fad10dba76f3a51281c9fc0659d5ffe4`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "sheet1", "kind": "base", "block": null, "base_tables": ["sheet1"]}] | [] | ["\"Consigned Product\"", "STRFTIME('%Y-%m', \"Date\")"] |
| B2 | [{"alias": "pm", "kind": "derived", "block": "B1", "base_tables": ["sheet1"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | SUM("Profit") | [{"table": "sheet1", "column": "Profit"}] | [] | False |


## S29

类别 `data`；来源 `query_db`；调用 `d47f65c38a174bbf9f5411f652fe7448`；状态 `success`。

```sql
WITH pm AS (
  SELECT substr("Destination", 13, instr(substr("Destination", 13), '-') - 1) AS dim, strftime('%Y-%m',"Date") AS month, SUM("Profit") AS p
  FROM sheet1 WHERE "Destination" LIKE 'South China%' GROUP BY 1,2
)
SELECT dim, month, ROUND(p,0) AS profit,
  ROUND(p - LAG(p) OVER (PARTITION BY dim ORDER BY month),0) AS chg
FROM pm ORDER BY dim, month
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-006/attempt-01/sql/S29.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-006/attempt-01/sql/S29.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-006/attempt-01/results/S29.rows.jsonl)；完整：True；SHA256：`5bd108c530f6f3b2a20eeb824250f7b13a019a7f75fe16143ab5faa9526bb796`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "sheet1", "kind": "base", "block": null, "base_tables": ["sheet1"]}] | [] | ["SUBSTRING(\"Destination\", 13, INSTR(SUBSTRING(\"Destination\", 13), '-') - 1)", "STRFTIME('%Y-%m', \"Date\")"] |
| B2 | [{"alias": "pm", "kind": "derived", "block": "B1", "base_tables": ["sheet1"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | SUM("Profit") | [{"table": "sheet1", "column": "Profit"}] | [] | False |


## S30

类别 `data`；来源 `query_db`；调用 `6634f0e94a124476a4ced0d5ce2054cb`；状态 `success`。

```sql
SELECT 
  SUM(CASE WHEN "Profit Margin" > 1 THEN 1 ELSE 0 END) AS rows_margin_gt1,
  SUM(CASE WHEN "Total Logistics Revenue" <= 0 THEN 1 ELSE 0 END) AS rows_rev_le0,
  SUM(CASE WHEN "Discount Amount" < 0 THEN 1 ELSE 0 END) AS rows_discount_neg,
  SUM(CASE WHEN "Total Logistics Cost" <= 0 THEN 1 ELSE 0 END) AS rows_cost_le0,
  COUNT(*) AS n
FROM sheet1 WHERE "Destination" LIKE 'South China%'
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-006/attempt-01/sql/S30.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-006/attempt-01/sql/S30.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-006/attempt-01/results/S30.rows.jsonl)；完整：True；SHA256：`4170ab7d6d65050afc2d99cd1e99e5c67f9e5c9567f12e042ed23563c25500ef`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "sheet1", "kind": "base", "block": null, "base_tables": ["sheet1"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | SUM(CASE WHEN "Profit Margin" > 1 THEN 1 ELSE 0 END) | [] | [{"table": "sheet1", "column": "Profit Margin"}] | False |
| B1 | SUM(CASE WHEN "Total Logistics Revenue" <= 0 THEN 1 ELSE 0 END) | [] | [{"table": "sheet1", "column": "Total Logistics Revenue"}] | False |
| B1 | SUM(CASE WHEN "Discount Amount" < 0 THEN 1 ELSE 0 END) | [] | [{"table": "sheet1", "column": "Discount Amount"}] | False |
| B1 | SUM(CASE WHEN "Total Logistics Cost" <= 0 THEN 1 ELSE 0 END) | [] | [{"table": "sheet1", "column": "Total Logistics Cost"}] | False |
| B1 | COUNT(*) | [] | [] | True |


## S31

类别 `data`；来源 `query_db`；调用 `9cdc2dd7247146858cd8386d0bcae5b9`；状态 `success`。

```sql
SELECT strftime('%Y-%m', "Date") AS month, COUNT(*) AS n,
  ROUND(AVG("Profit Margin"),3) AS avg_margin,
  ROUND(MIN("Profit Margin"),3) AS min_margin,
  ROUND(MAX("Profit Margin"),3) AS max_margin
FROM sheet1 WHERE "Destination" LIKE 'South China%'
GROUP BY month ORDER BY month
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-006/attempt-01/sql/S31.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-006/attempt-01/sql/S31.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-006/attempt-01/results/S31.rows.jsonl)；完整：True；SHA256：`fe7a34906353045988e29b0d3a89d25b84e6ceb3d197e88b12d57f922a4a3bae`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "sheet1", "kind": "base", "block": null, "base_tables": ["sheet1"]}] | [] | ["STRFTIME('%Y-%m', \"Date\")"] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |
| B1 | AVG("Profit Margin") | [{"table": "sheet1", "column": "Profit Margin"}] | [] | False |
| B1 | MIN("Profit Margin") | [{"table": "sheet1", "column": "Profit Margin"}] | [] | False |
| B1 | MAX("Profit Margin") | [{"table": "sheet1", "column": "Profit Margin"}] | [] | False |


## S32

类别 `data`；来源 `query_db`；调用 `be0504df370e49e785a4f3d078263b4b`；状态 `success`。

```sql
SELECT "Profit Margin", "Total Logistics Revenue", "Profit", "Total Logistics Cost"
FROM sheet1 WHERE "Destination" LIKE 'South China%' AND "Profit Margin" > 1
ORDER BY "Profit Margin" DESC LIMIT 20
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-006/attempt-01/sql/S32.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-006/attempt-01/sql/S32.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-006/attempt-01/results/S32.rows.jsonl)；完整：True；SHA256：`414a8dba8e4fd376923beca4c5f63265ad942f91e84799698b0e850b167b3034`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "sheet1", "kind": "base", "block": null, "base_tables": ["sheet1"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |


## S33

类别 `data`；来源 `query_db`；调用 `258727c3425b462aa5f8cabb95361fd2`；状态 `success`。

```sql
SELECT strftime('%Y-%m', "Date") AS month,
  COUNT(*) AS orders,
  ROUND(SUM("Profit"),0) AS profit,
  ROUND(AVG("Profit"),0) AS avg_profit_per_order,
  ROUND(AVG("Sales Quantity"),1) AS avg_qty,
  ROUND(AVG("Profit Margin"),3) AS avg_margin,
  ROUND(AVG("Logistics Unit Price"),2) AS avg_unit_price
FROM sheet1 WHERE "Destination" LIKE 'South China%'
GROUP BY month ORDER BY month
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-006/attempt-01/sql/S33.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-006/attempt-01/sql/S33.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-006/attempt-01/results/S33.rows.jsonl)；完整：True；SHA256：`ed44bba21d20c44c80abd11c1aee9b3a625af2fee72fe998f19284f218098ece`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "sheet1", "kind": "base", "block": null, "base_tables": ["sheet1"]}] | [] | ["STRFTIME('%Y-%m', \"Date\")"] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |
| B1 | SUM("Profit") | [{"table": "sheet1", "column": "Profit"}] | [] | False |
| B1 | AVG("Profit") | [{"table": "sheet1", "column": "Profit"}] | [] | False |
| B1 | AVG("Sales Quantity") | [{"table": "sheet1", "column": "Sales Quantity"}] | [] | False |
| B1 | AVG("Profit Margin") | [{"table": "sheet1", "column": "Profit Margin"}] | [] | False |
| B1 | AVG("Logistics Unit Price") | [{"table": "sheet1", "column": "Logistics Unit Price"}] | [] | False |


## S34

类别 `data`；来源 `query_db`；调用 `6d3909bec97540f1bf6bda0ec9234593`；状态 `success`。

```sql
WITH sc AS (SELECT * FROM sheet1 WHERE "Destination" LIKE 'South China%'),
ranked AS (
  SELECT "Profit", NTILE(100) OVER (ORDER BY "Profit") AS pct
  FROM sc
),
tot AS (SELECT SUM("Profit") AS t FROM sc)
SELECT pct, ROUND(SUM("Profit"),0) AS profit, ROUND(100.0*SUM("Profit")/(SELECT t FROM tot),2) AS pct_of_total, COUNT(*) AS n
FROM ranked
GROUP BY pct
HAVING pct IN (1,2,5,10,20,50,80,90,95,98,99,100)
ORDER BY pct
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-006/attempt-01/sql/S34.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-006/attempt-01/sql/S34.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-006/attempt-01/results/S34.rows.jsonl)；完整：True；SHA256：`23b973924e107c27b7b929527079287cf006df65c64a749f1a6152da244f9242`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "sheet1", "kind": "base", "block": null, "base_tables": ["sheet1"]}] | [] | [] |
| B2 | [{"alias": "sc", "kind": "derived", "block": "B1", "base_tables": ["sheet1"]}] | [] | [] |
| B3 | [{"alias": "sc", "kind": "derived", "block": "B1", "base_tables": ["sheet1"]}] | [] | [] |
| B4 | [{"alias": "tot", "kind": "derived", "block": "B3", "base_tables": ["sheet1"]}] | [] | [] |
| B5 | [{"alias": "ranked", "kind": "derived", "block": "B2", "base_tables": ["sheet1"]}] | [] | ["pct"] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B3 | SUM("Profit") | [{"table": "sheet1", "column": "Profit"}] | [] | False |
| B5 | COUNT(*) | [] | [] | True |
| B5 | SUM("Profit") | [{"table": "sheet1", "column": "Profit"}] | [] | False |
| B5 | SUM("Profit") | [{"table": "sheet1", "column": "Profit"}] | [] | False |


未解析列血缘：[{"block": "B5", "column": "t", "reason": "ambiguous_or_missing_source"}]

## S35

类别 `data`；来源 `query_db`；调用 `5443950e698942fbb93b566fb4a3fd96`；状态 `success`。

```sql
SELECT "Waybill Number", "Date", "Destination", "Consigned Product", "Sales Quantity", 
  "Total Logistics Revenue", "Total Logistics Cost", "Profit", "Profit Margin"
FROM sheet1 WHERE "Destination" LIKE 'South China%'
ORDER BY "Profit" DESC LIMIT 15
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-006/attempt-01/sql/S35.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-006/attempt-01/sql/S35.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-006/attempt-01/results/S35.rows.jsonl)；完整：True；SHA256：`08ac02abf4297be51eada8069b6a1034d38f259821f70685bb3ab1a36a06bbe4`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "sheet1", "kind": "base", "block": null, "base_tables": ["sheet1"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |


## S36

类别 `data`；来源 `python`；调用 `0e52258e01ab43719ba41da9e7241d1b`；状态 `success`。

```sql
SELECT strftime('%Y-%m', "Date") AS month, SUM("Profit") AS profit, SUM("Total Logistics Revenue") AS rev, SUM("Total Logistics Cost") AS cost, SUM("Sales Quantity") AS qty, COUNT(*) AS orders, AVG("Profit Margin") AS avg_margin, AVG("Logistics Unit Price") AS avg_price FROM sheet1 WHERE "Destination" LIKE 'South China%%' GROUP BY month ORDER BY month
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-006/attempt-01/sql/S36.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-006/attempt-01/sql/S36.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-006/attempt-01/results/S36.rows.jsonl)；完整：True；SHA256：`aac5a38746887bb998a2ec342748af211e1fbe2a39c4178c03914de701875d52`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "sheet1", "kind": "base", "block": null, "base_tables": ["sheet1"]}] | [] | ["STRFTIME('%Y-%m', \"Date\")"] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | SUM("Profit") | [{"table": "sheet1", "column": "Profit"}] | [] | False |
| B1 | SUM("Total Logistics Revenue") | [{"table": "sheet1", "column": "Total Logistics Revenue"}] | [] | False |
| B1 | SUM("Total Logistics Cost") | [{"table": "sheet1", "column": "Total Logistics Cost"}] | [] | False |
| B1 | SUM("Sales Quantity") | [{"table": "sheet1", "column": "Sales Quantity"}] | [] | False |
| B1 | COUNT(*) | [] | [] | True |
| B1 | AVG("Profit Margin") | [{"table": "sheet1", "column": "Profit Margin"}] | [] | False |
| B1 | AVG("Logistics Unit Price") | [{"table": "sheet1", "column": "Logistics Unit Price"}] | [] | False |


## S37

类别 `data`；来源 `python`；调用 `0e52258e01ab43719ba41da9e7241d1b`；状态 `success`。

```sql
SELECT "Consigned Product" AS dim, strftime('%Y-%m', "Date") AS month, SUM("Profit") AS p FROM sheet1 WHERE "Destination" LIKE 'South China%%' GROUP BY dim, month ORDER BY dim, month
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-006/attempt-01/sql/S37.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-006/attempt-01/sql/S37.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-006/attempt-01/results/S37.rows.jsonl)；完整：True；SHA256：`abce1542c2da2ef8fce074b017087ea9f8ab1917a4a3bbf717ae202a62e76a3f`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "sheet1", "kind": "base", "block": null, "base_tables": ["sheet1"]}] | [] | ["\"Consigned Product\"", "STRFTIME('%Y-%m', \"Date\")"] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | SUM("Profit") | [{"table": "sheet1", "column": "Profit"}] | [] | False |


## S38

类别 `data`；来源 `python`；调用 `0e52258e01ab43719ba41da9e7241d1b`；状态 `success`。

```sql
SELECT substr("Destination", 13, instr(substr("Destination", 13), '-') - 1) AS province, strftime('%Y-%m', "Date") AS month, SUM("Profit") AS p FROM sheet1 WHERE "Destination" LIKE 'South China%%' GROUP BY province, month ORDER BY province, month
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-006/attempt-01/sql/S38.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-006/attempt-01/sql/S38.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-006/attempt-01/results/S38.rows.jsonl)；完整：True；SHA256：`8962cce94383488f5131d71752f7444b73a24be08c550ab3a81d0388b940a4e0`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "sheet1", "kind": "base", "block": null, "base_tables": ["sheet1"]}] | [] | ["SUBSTRING(\"Destination\", 13, INSTR(SUBSTRING(\"Destination\", 13), '-') - 1)", "STRFTIME('%Y-%m', \"Date\")"] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | SUM("Profit") | [{"table": "sheet1", "column": "Profit"}] | [] | False |


## S39

类别 `data`；来源 `python`；调用 `e29f2a8a7dba432da0fe74e3adcb3a66`；状态 `success`。

```sql
SELECT strftime('%Y-%m', "Date") AS month, SUM("Profit") AS profit, SUM("Total Logistics Revenue") AS rev, SUM("Total Logistics Cost") AS cost, SUM("Sales Quantity") AS qty, COUNT(*) AS orders, AVG("Profit Margin") AS avg_margin, AVG("Logistics Unit Price") AS avg_price FROM sheet1 WHERE "Destination" LIKE 'South China%%' GROUP BY month ORDER BY month
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-006/attempt-01/sql/S39.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-006/attempt-01/sql/S39.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-006/attempt-01/results/S39.rows.jsonl)；完整：True；SHA256：`aac5a38746887bb998a2ec342748af211e1fbe2a39c4178c03914de701875d52`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "sheet1", "kind": "base", "block": null, "base_tables": ["sheet1"]}] | [] | ["STRFTIME('%Y-%m', \"Date\")"] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | SUM("Profit") | [{"table": "sheet1", "column": "Profit"}] | [] | False |
| B1 | SUM("Total Logistics Revenue") | [{"table": "sheet1", "column": "Total Logistics Revenue"}] | [] | False |
| B1 | SUM("Total Logistics Cost") | [{"table": "sheet1", "column": "Total Logistics Cost"}] | [] | False |
| B1 | SUM("Sales Quantity") | [{"table": "sheet1", "column": "Sales Quantity"}] | [] | False |
| B1 | COUNT(*) | [] | [] | True |
| B1 | AVG("Profit Margin") | [{"table": "sheet1", "column": "Profit Margin"}] | [] | False |
| B1 | AVG("Logistics Unit Price") | [{"table": "sheet1", "column": "Logistics Unit Price"}] | [] | False |


## S40

类别 `data`；来源 `python`；调用 `e29f2a8a7dba432da0fe74e3adcb3a66`；状态 `success`。

```sql
SELECT "Consigned Product" AS dim, strftime('%Y-%m', "Date") AS month, SUM("Profit") AS p FROM sheet1 WHERE "Destination" LIKE 'South China%%' GROUP BY dim, month ORDER BY dim, month
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-006/attempt-01/sql/S40.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-006/attempt-01/sql/S40.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-006/attempt-01/results/S40.rows.jsonl)；完整：True；SHA256：`abce1542c2da2ef8fce074b017087ea9f8ab1917a4a3bbf717ae202a62e76a3f`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "sheet1", "kind": "base", "block": null, "base_tables": ["sheet1"]}] | [] | ["\"Consigned Product\"", "STRFTIME('%Y-%m', \"Date\")"] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | SUM("Profit") | [{"table": "sheet1", "column": "Profit"}] | [] | False |


## S41

类别 `data`；来源 `python`；调用 `e29f2a8a7dba432da0fe74e3adcb3a66`；状态 `success`。

```sql
SELECT substr("Destination", 13, instr(substr("Destination", 13), '-') - 1) AS province, strftime('%Y-%m', "Date") AS month, SUM("Profit") AS p FROM sheet1 WHERE "Destination" LIKE 'South China%%' GROUP BY province, month ORDER BY province, month
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-006/attempt-01/sql/S41.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-006/attempt-01/sql/S41.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-006/attempt-01/results/S41.rows.jsonl)；完整：True；SHA256：`8962cce94383488f5131d71752f7444b73a24be08c550ab3a81d0388b940a4e0`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "sheet1", "kind": "base", "block": null, "base_tables": ["sheet1"]}] | [] | ["SUBSTRING(\"Destination\", 13, INSTR(SUBSTRING(\"Destination\", 13), '-') - 1)", "STRFTIME('%Y-%m', \"Date\")"] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | SUM("Profit") | [{"table": "sheet1", "column": "Profit"}] | [] | False |


## S42

类别 `data`；来源 `python`；调用 `a42f1fbab90142bcb5a47fef675f30d9`；状态 `success`。

```sql
SELECT strftime('%Y-%m', "Date") AS month, SUM("Profit") AS profit, SUM("Total Logistics Revenue") AS rev, SUM("Total Logistics Cost") AS cost, SUM("Sales Quantity") AS qty, COUNT(*) AS orders, AVG("Profit Margin") AS avg_margin, AVG("Logistics Unit Price") AS avg_price FROM sheet1 WHERE "Destination" LIKE 'South China%%' GROUP BY month ORDER BY month
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-006/attempt-01/sql/S42.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-006/attempt-01/sql/S42.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-006/attempt-01/results/S42.rows.jsonl)；完整：True；SHA256：`aac5a38746887bb998a2ec342748af211e1fbe2a39c4178c03914de701875d52`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "sheet1", "kind": "base", "block": null, "base_tables": ["sheet1"]}] | [] | ["STRFTIME('%Y-%m', \"Date\")"] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | SUM("Profit") | [{"table": "sheet1", "column": "Profit"}] | [] | False |
| B1 | SUM("Total Logistics Revenue") | [{"table": "sheet1", "column": "Total Logistics Revenue"}] | [] | False |
| B1 | SUM("Total Logistics Cost") | [{"table": "sheet1", "column": "Total Logistics Cost"}] | [] | False |
| B1 | SUM("Sales Quantity") | [{"table": "sheet1", "column": "Sales Quantity"}] | [] | False |
| B1 | COUNT(*) | [] | [] | True |
| B1 | AVG("Profit Margin") | [{"table": "sheet1", "column": "Profit Margin"}] | [] | False |
| B1 | AVG("Logistics Unit Price") | [{"table": "sheet1", "column": "Logistics Unit Price"}] | [] | False |


## S43

类别 `data`；来源 `python`；调用 `a42f1fbab90142bcb5a47fef675f30d9`；状态 `success`。

```sql
SELECT "Consigned Product" AS dim, strftime('%Y-%m', "Date") AS month, SUM("Profit") AS p FROM sheet1 WHERE "Destination" LIKE 'South China%%' GROUP BY dim, month ORDER BY dim, month
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-006/attempt-01/sql/S43.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-006/attempt-01/sql/S43.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-006/attempt-01/results/S43.rows.jsonl)；完整：True；SHA256：`abce1542c2da2ef8fce074b017087ea9f8ab1917a4a3bbf717ae202a62e76a3f`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "sheet1", "kind": "base", "block": null, "base_tables": ["sheet1"]}] | [] | ["\"Consigned Product\"", "STRFTIME('%Y-%m', \"Date\")"] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | SUM("Profit") | [{"table": "sheet1", "column": "Profit"}] | [] | False |


## S44

类别 `data`；来源 `python`；调用 `a42f1fbab90142bcb5a47fef675f30d9`；状态 `success`。

```sql
SELECT substr("Destination", 13, instr(substr("Destination", 13), '-') - 1) AS province, strftime('%Y-%m', "Date") AS month, SUM("Profit") AS p FROM sheet1 WHERE "Destination" LIKE 'South China%%' GROUP BY province, month ORDER BY province, month
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-006/attempt-01/sql/S44.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-006/attempt-01/sql/S44.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-006/attempt-01/results/S44.rows.jsonl)；完整：True；SHA256：`8962cce94383488f5131d71752f7444b73a24be08c550ab3a81d0388b940a4e0`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "sheet1", "kind": "base", "block": null, "base_tables": ["sheet1"]}] | [] | ["SUBSTRING(\"Destination\", 13, INSTR(SUBSTRING(\"Destination\", 13), '-') - 1)", "STRFTIME('%Y-%m', \"Date\")"] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | SUM("Profit") | [{"table": "sheet1", "column": "Profit"}] | [] | False |


## S45

类别 `data`；来源 `python`；调用 `a42f1fbab90142bcb5a47fef675f30d9`；状态 `success`。

```sql
SELECT strftime('%Y-%m', "Date") AS month, SUM("List Price Revenue") AS list_price, SUM("Logistics Value-Added Service Revenue") AS vas, SUM("Discount Amount") AS discount FROM sheet1 WHERE "Destination" LIKE 'South China%%' GROUP BY month ORDER BY month
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-006/attempt-01/sql/S45.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-006/attempt-01/sql/S45.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-006/attempt-01/results/S45.rows.jsonl)；完整：True；SHA256：`dd8e40bfbd343a394d9dc3891cb0b5b9d6b278720bca321a355efa47fbb34928`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "sheet1", "kind": "base", "block": null, "base_tables": ["sheet1"]}] | [] | ["STRFTIME('%Y-%m', \"Date\")"] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | SUM("List Price Revenue") | [{"table": "sheet1", "column": "List Price Revenue"}] | [] | False |
| B1 | SUM("Logistics Value-Added Service Revenue") | [{"table": "sheet1", "column": "Logistics Value-Added Service Revenue"}] | [] | False |
| B1 | SUM("Discount Amount") | [{"table": "sheet1", "column": "Discount Amount"}] | [] | False |


## S46

类别 `data`；来源 `python`；调用 `a42f1fbab90142bcb5a47fef675f30d9`；状态 `success`。

```sql
SELECT strftime('%Y-%m', "Date") AS month, SUM("Freight Cost") AS freight, SUM("Warehousing Cost") AS warehousing, SUM("Other Operating Costs") AS other FROM sheet1 WHERE "Destination" LIKE 'South China%%' GROUP BY month ORDER BY month
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-006/attempt-01/sql/S46.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-006/attempt-01/sql/S46.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-006/attempt-01/results/S46.rows.jsonl)；完整：True；SHA256：`2339ea7b732a6eb68d642c5e785854d090df76640f54d121c508c17372f0e01e`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "sheet1", "kind": "base", "block": null, "base_tables": ["sheet1"]}] | [] | ["STRFTIME('%Y-%m', \"Date\")"] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | SUM("Freight Cost") | [{"table": "sheet1", "column": "Freight Cost"}] | [] | False |
| B1 | SUM("Warehousing Cost") | [{"table": "sheet1", "column": "Warehousing Cost"}] | [] | False |
| B1 | SUM("Other Operating Costs") | [{"table": "sheet1", "column": "Other Operating Costs"}] | [] | False |


## S47

类别 `data`；来源 `query_db`；调用 `bbb06206d357410aa4fcd32f5964bb60`；状态 `success`。

```sql
SELECT 
  "Consigned Product" AS dim,
  ROUND(SUM(CASE WHEN strftime('%m',"Date")='01' THEN "Profit" ELSE 0 END),0) AS jan,
  ROUND(SUM(CASE WHEN strftime('%m',"Date")='02' THEN "Profit" ELSE 0 END),0) AS feb,
  ROUND(SUM(CASE WHEN strftime('%m',"Date")='02' THEN "Profit" ELSE 0 END) - SUM(CASE WHEN strftime('%m',"Date")='01' THEN "Profit" ELSE 0 END),0) AS change,
  ROUND(AVG("Profit"),0) AS avg_monthly
FROM sheet1 WHERE "Destination" LIKE 'South China%'
GROUP BY dim
ORDER BY ABS(change) DESC
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-006/attempt-01/sql/S47.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-006/attempt-01/sql/S47.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-006/attempt-01/results/S47.rows.jsonl)；完整：True；SHA256：`2620920d6651faea7a13d6faf0ed5502eda980ccd4b2872e7541c1460558910e`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "sheet1", "kind": "base", "block": null, "base_tables": ["sheet1"]}] | [] | ["\"Consigned Product\""] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | SUM(CASE WHEN STRFTIME('%m', "Date") = '01' THEN "Profit" ELSE 0 END) | [{"table": "sheet1", "column": "Profit"}] | [{"table": "sheet1", "column": "Date"}] | False |
| B1 | SUM(CASE WHEN STRFTIME('%m', "Date") = '02' THEN "Profit" ELSE 0 END) | [{"table": "sheet1", "column": "Profit"}] | [{"table": "sheet1", "column": "Date"}] | False |
| B1 | AVG("Profit") | [{"table": "sheet1", "column": "Profit"}] | [] | False |
| B1 | SUM(CASE WHEN STRFTIME('%m', "Date") = '02' THEN "Profit" ELSE 0 END) | [{"table": "sheet1", "column": "Profit"}] | [{"table": "sheet1", "column": "Date"}] | False |
| B1 | SUM(CASE WHEN STRFTIME('%m', "Date") = '01' THEN "Profit" ELSE 0 END) | [{"table": "sheet1", "column": "Profit"}] | [{"table": "sheet1", "column": "Date"}] | False |


## S48

类别 `data`；来源 `query_db`；调用 `fe90eda40b5a4befb69ef378cdc9747a`；状态 `success`。

```sql
WITH prod_month AS (
  SELECT "Consigned Product" AS dim, strftime('%Y-%m',"Date") AS month, SUM("Profit") AS p
  FROM sheet1 WHERE "Destination" LIKE 'South China%' GROUP BY 1,2
)
SELECT month, 
  ROUND(p,0) AS kitchen_appl_profit,
  ROUND(p - AVG(p) OVER (PARTITION BY dim),0) AS deviation_from_mean
FROM prod_month
WHERE dim = 'Kitchen Appliances'
ORDER BY month
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-006/attempt-01/sql/S48.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-006/attempt-01/sql/S48.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-006/attempt-01/results/S48.rows.jsonl)；完整：True；SHA256：`4cd345efc5e1155a76be2d6497155784ce08e9f9c2f6dd9227f7f201b71a8f61`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "sheet1", "kind": "base", "block": null, "base_tables": ["sheet1"]}] | [] | ["\"Consigned Product\"", "STRFTIME('%Y-%m', \"Date\")"] |
| B2 | [{"alias": "prod_month", "kind": "derived", "block": "B1", "base_tables": ["sheet1"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | SUM("Profit") | [{"table": "sheet1", "column": "Profit"}] | [] | False |


## S49

类别 `data`；来源 `query_db`；调用 `e6051520faf74826ab3276efeb4dfea4`；状态 `success`。

```sql
WITH pm AS (
  SELECT "Consigned Product" AS dim, strftime('%Y-%m',"Date") AS month, SUM("Profit") AS p
  FROM sheet1 WHERE "Destination" LIKE 'South China%' GROUP BY 1,2
)
SELECT dim, 
  ROUND(AVG(p),0) AS mean_p,
  ROUND(MIN(p),0) AS min_p,
  ROUND(MAX(p),0) AS max_p,
  ROUND((MAX(p)-MIN(p))/AVG(p)*100,1) AS range_pct,
  ROUND(SQRT(AVG(p*p)-AVG(p)*AVG(p)),0) AS std_p,
  ROUND(SQRT(AVG(p*p)-AVG(p)*AVG(p))/AVG(p)*100,1) AS cv_pct
FROM pm GROUP BY dim ORDER BY cv_pct DESC
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-006/attempt-01/sql/S49.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-006/attempt-01/sql/S49.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-006/attempt-01/results/S49.rows.jsonl)；完整：True；SHA256：`94f62d73d7992fc7c881d0292ed8678f24b46bf636fdbfff0fb85e7ad03a78b6`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "sheet1", "kind": "base", "block": null, "base_tables": ["sheet1"]}] | [] | ["\"Consigned Product\"", "STRFTIME('%Y-%m', \"Date\")"] |
| B2 | [{"alias": "pm", "kind": "derived", "block": "B1", "base_tables": ["sheet1"]}] | [] | ["dim"] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | SUM("Profit") | [{"table": "sheet1", "column": "Profit"}] | [] | False |
| B2 | AVG(p) | [{"table": "sheet1", "column": "Profit"}] | [] | False |
| B2 | MIN(p) | [{"table": "sheet1", "column": "Profit"}] | [] | False |
| B2 | MAX(p) | [{"table": "sheet1", "column": "Profit"}] | [] | False |
| B2 | AVG(p) | [{"table": "sheet1", "column": "Profit"}] | [] | False |
| B2 | AVG(p * p) | [{"table": "sheet1", "column": "Profit"}, {"table": "sheet1", "column": "Profit"}] | [] | False |
| B2 | AVG(p) | [{"table": "sheet1", "column": "Profit"}] | [] | False |
| B2 | AVG(p) | [{"table": "sheet1", "column": "Profit"}] | [] | False |
| B2 | AVG(p) | [{"table": "sheet1", "column": "Profit"}] | [] | False |
| B2 | MAX(p) | [{"table": "sheet1", "column": "Profit"}] | [] | False |
| B2 | MIN(p) | [{"table": "sheet1", "column": "Profit"}] | [] | False |
| B2 | AVG(p * p) | [{"table": "sheet1", "column": "Profit"}, {"table": "sheet1", "column": "Profit"}] | [] | False |
| B2 | AVG(p) | [{"table": "sheet1", "column": "Profit"}] | [] | False |
| B2 | AVG(p) | [{"table": "sheet1", "column": "Profit"}] | [] | False |


## S50

类别 `data`；来源 `query_db`；调用 `6feb45fbd8844f0e9987dd27166f0149`；状态 `success`。

```sql
WITH comp_month AS (
  SELECT strftime('%Y-%m',"Date") AS month,
    SUM("List Price Revenue") AS list_price,
    SUM("Logistics Value-Added Service Revenue") AS vas,
    SUM("Discount Amount") AS discount,
    SUM("Total Logistics Revenue") AS rev
  FROM sheet1 WHERE "Destination" LIKE 'South China%' GROUP BY 1
)
SELECT month, ROUND(list_price,0) AS list_price, ROUND(vas,0) AS vas, ROUND(discount,0) AS discount,
  ROUND(list_price+vas-discount,0) AS calc_rev, ROUND(rev,0) AS actual_rev,
  ROUND(discount/(list_price+vas)*100,1) AS discount_rate_pct,
  ROUND(vas/(list_price+vas)*100,1) AS vas_share_pct
FROM comp_month ORDER BY month
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-006/attempt-01/sql/S50.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-006/attempt-01/sql/S50.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-006/attempt-01/results/S50.rows.jsonl)；完整：True；SHA256：`43c5f6de2a792f2022bae3429013cf4c0e7eaccfbde29fb4c27606eae00064dc`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "sheet1", "kind": "base", "block": null, "base_tables": ["sheet1"]}] | [] | ["STRFTIME('%Y-%m', \"Date\")"] |
| B2 | [{"alias": "comp_month", "kind": "derived", "block": "B1", "base_tables": ["sheet1"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | SUM("List Price Revenue") | [{"table": "sheet1", "column": "List Price Revenue"}] | [] | False |
| B1 | SUM("Logistics Value-Added Service Revenue") | [{"table": "sheet1", "column": "Logistics Value-Added Service Revenue"}] | [] | False |
| B1 | SUM("Discount Amount") | [{"table": "sheet1", "column": "Discount Amount"}] | [] | False |
| B1 | SUM("Total Logistics Revenue") | [{"table": "sheet1", "column": "Total Logistics Revenue"}] | [] | False |


## S51

类别 `data`；来源 `query_db`；调用 `8ae948529d5e4de3b8eda2ceccc6a159`；状态 `success`。

```sql
SELECT strftime('%m',"Date") AS month,
  COUNT(*) AS orders,
  SUM("Sales Quantity") AS qty,
  ROUND(AVG("Logistics Unit Price"),2) AS avg_unit_price,
  ROUND(SUM("Discount Amount"),0) AS discount,
  ROUND(SUM("Profit"),0) AS profit,
  ROUND(AVG("Profit Margin"),3) AS avg_margin,
  ROUND(SUM("Profit")/SUM("Sales Quantity"),2) AS profit_per_unit
FROM sheet1 
WHERE "Destination" LIKE 'South China%' AND "Consigned Product" = 'Kitchen Appliances'
GROUP BY month ORDER BY month
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-006/attempt-01/sql/S51.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-006/attempt-01/sql/S51.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-006/attempt-01/results/S51.rows.jsonl)；完整：True；SHA256：`c611033a239b172df059143ba08271bd23f860b06e3d53617f2b358624a7efea`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "sheet1", "kind": "base", "block": null, "base_tables": ["sheet1"]}] | [] | ["STRFTIME('%m', \"Date\")"] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |
| B1 | SUM("Sales Quantity") | [{"table": "sheet1", "column": "Sales Quantity"}] | [] | False |
| B1 | AVG("Logistics Unit Price") | [{"table": "sheet1", "column": "Logistics Unit Price"}] | [] | False |
| B1 | SUM("Discount Amount") | [{"table": "sheet1", "column": "Discount Amount"}] | [] | False |
| B1 | SUM("Profit") | [{"table": "sheet1", "column": "Profit"}] | [] | False |
| B1 | AVG("Profit Margin") | [{"table": "sheet1", "column": "Profit Margin"}] | [] | False |
| B1 | SUM("Profit") | [{"table": "sheet1", "column": "Profit"}] | [] | False |
| B1 | SUM("Sales Quantity") | [{"table": "sheet1", "column": "Sales Quantity"}] | [] | False |


## S52

类别 `data`；来源 `python`；调用 `18cc9ccae160429d9db4e28b5527c852`；状态 `success`。

```sql
SELECT strftime('%Y-%m', "Date") AS month, COUNT(*) AS orders, SUM("Profit") AS profit, AVG("Profit") AS avg_profit FROM sheet1 WHERE "Destination" LIKE 'South China%%' GROUP BY month ORDER BY month
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-006/attempt-01/sql/S52.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-006/attempt-01/sql/S52.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-006/attempt-01/results/S52.rows.jsonl)；完整：True；SHA256：`51886abe381719bf25bd97712794d2956980acb3573fc70a91f79100329b4916`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "sheet1", "kind": "base", "block": null, "base_tables": ["sheet1"]}] | [] | ["STRFTIME('%Y-%m', \"Date\")"] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |
| B1 | SUM("Profit") | [{"table": "sheet1", "column": "Profit"}] | [] | False |
| B1 | AVG("Profit") | [{"table": "sheet1", "column": "Profit"}] | [] | False |


## S53

类别 `data`；来源 `python`；调用 `18cc9ccae160429d9db4e28b5527c852`；状态 `success`。

```sql
SELECT strftime('%Y-%m', "Date") AS month, SUM("Sales Quantity") AS qty, SUM("Total Logistics Revenue") AS rev, SUM("Profit") AS profit FROM sheet1 WHERE "Destination" LIKE 'South China%%' GROUP BY month ORDER BY month
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-006/attempt-01/sql/S53.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-006/attempt-01/sql/S53.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-006/attempt-01/results/S53.rows.jsonl)；完整：True；SHA256：`e929550f23a3c2a0c7b7d7dbd9eaecd79acf61094172b5208547fd9d06122267`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "sheet1", "kind": "base", "block": null, "base_tables": ["sheet1"]}] | [] | ["STRFTIME('%Y-%m', \"Date\")"] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | SUM("Sales Quantity") | [{"table": "sheet1", "column": "Sales Quantity"}] | [] | False |
| B1 | SUM("Total Logistics Revenue") | [{"table": "sheet1", "column": "Total Logistics Revenue"}] | [] | False |
| B1 | SUM("Profit") | [{"table": "sheet1", "column": "Profit"}] | [] | False |


## S54

类别 `data`；来源 `python`；调用 `18cc9ccae160429d9db4e28b5527c852`；状态 `success`。

```sql
SELECT "Age Range" AS age, "Customer Gender" AS gender, strftime('%Y-%m', "Date") AS month, SUM("Profit") AS p FROM sheet1 WHERE "Destination" LIKE 'South China%%' GROUP BY age, gender, month ORDER BY age, gender, month
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-006/attempt-01/sql/S54.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-006/attempt-01/sql/S54.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-006/attempt-01/results/S54.rows.jsonl)；完整：True；SHA256：`6c1e767a8d6ca1370e50e904a3fc11f27602f6a74d274ee92d2afa5ae9993d97`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "sheet1", "kind": "base", "block": null, "base_tables": ["sheet1"]}] | [] | ["\"Age Range\"", "\"Customer Gender\"", "STRFTIME('%Y-%m', \"Date\")"] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | SUM("Profit") | [{"table": "sheet1", "column": "Profit"}] | [] | False |

