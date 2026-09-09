# dacomp-022

I am a ride-hailing driver. Based on the platform’s 2024 data, please help me take a look …

运行：已提交。官方未评分。全部 SQL 尝试/成功 65/61；数据 SQL 63/59；Python 4 次。

完整原题：

I am a ride-hailing driver. Based on the platform’s 2024 data, please help me take a look at what strategies I can use to achieve better annual earnings (for example, higher per-kilometer ride fare), such as which Vehicle Type to choose and what level of service quality rating to maintain.

| 表 | 行数 | 列数 |
| --- | --- | --- |
| sheet1 | 150000 | 21 |


实际路线（分析者依据 SQL/源码概括，不代表 Agent 自述）：SQL 比较车型、时段、评分与每公里车费 → Python 对完成订单做分组检验与图表汇总 → 细分距离/接驾区域 → 计算工作安排的年度流水情景。

数据库大小：46,215,168 字节。

## 数据 SQL

| SQL | 状态 | 基础表 | Join 输入/类型 | GROUP BY | 聚合表达式 | 结果行数 | 数据库 ms |
| --- | --- | --- | --- | --- | --- | --- | --- |
| [S3/Q1](#s3) | success | ["sheet1"] | 0 / {} | [] | [] | 20 | 0.411 |
| [S4/Q2](#s4) | success | ["sheet1"] | 0 / {} | [] | [] | 7 | 71.14 |
| [S5/Q3](#s5) | success | ["sheet1"] | 0 / {} | [] | [] | 5 | 65.825 |
| [S6/Q4](#s6) | success | ["sheet1"] | 0 / {} | [] | ["COUNT(*)", "COUNT(\"Booking Value\")", "COUNT(\"Ride Distance\")", "COUNT(\"Driver Ratings\")"] | 1 | 30.541 |
| [S7/Q5](#s7) | success | ["sheet1"] | 0 / {} | ["\"Vehicle Type\""] | ["COUNT(*)", "AVG(\"Booking Value\")", "AVG(\"Ride Distance\")", "AVG(\"Booking Value\" / NULLIF(\"Ride Distance\", 0))", "AVG(\"Driver Ratings\")", "SUM(\"Booking Value\")"] | 7 | 85.226 |
| [S8/Q6](#s8) | success | ["sheet1"] | 0 / {} | [] | ["COUNT(*)", "AVG(\"Booking Value\" / NULLIF(\"Ride Distance\", 0))", "AVG(\"Booking Value\")", "AVG(\"Ride Distance\")", "SUM(\"Booking Value\")"] | 1 | 36.135 |
| [S9/Q7](#s9) | success | ["sheet1"] | 0 / {} | ["\"Driver Ratings\""] | ["COUNT(*)", "AVG(\"Booking Value\")", "AVG(\"Booking Value\" / NULLIF(\"Ride Distance\", 0))", "SUM(\"Booking Value\")"] | 21 | 94.879 |
| [S10/Q8](#s10) | success | ["sheet1"] | 0 / {} | [] | ["MIN(\"Driver Ratings\")", "MAX(\"Driver Ratings\")", "MIN(\"Booking Value\")", "MAX(\"Booking Value\")", "MIN(\"Ride Distance\")", "MAX(\"Ride Distance\")", "AVG(\"Driver Ratings\")"] | 1 | 43.893 |
| [S11/Q9](#s11) | success | ["sheet1"] | 0 / {} | ["\"Driver Ratings\""] | ["COUNT(*)", "AVG(\"Booking Value\")", "AVG(\"Booking Value\" / NULLIF(\"Ride Distance\", 0))", "SUM(\"Booking Value\")", "COUNT(*)", "COUNT(*)"] | 21 | 94.88 |
| [S12/Q10](#s12) | success | ["sheet1"] | 0 / {} | ["\"Driver Ratings\""] | ["COUNT(*)", "AVG(\"Booking Value\")", "AVG(\"Booking Value\" / NULLIF(\"Ride Distance\", 0))", "SUM(\"Booking Value\")"] | 9 | 70.125 |
| [S13/Q11](#s13) | success | ["sheet1"] | 0 / {} | ["\"Vehicle Type\""] | ["COUNT(*)", "SUM(CASE WHEN \"Booking Status\" = 'Completed' THEN 1 ELSE 0 END)", "SUM(CASE WHEN \"Booking Status\" = 'Cancelled by Driver' THEN 1 ELSE 0 END)", "SUM(CASE WHEN \"Booking Status\" = 'Cancelled by Customer' THEN 1 ELSE 0 END)", "SUM(CASE WHEN \"Booking Status\" = 'Incomplete' THEN 1 ELSE 0 END)", "SUM(CASE WHEN \"Booking Status\" = 'No Driver Found' THEN 1 ELSE 0 END)", "COUNT(*)", "COUNT(*)", "SUM(CASE WHEN \"Booking Status\" = 'Completed' THEN 1 ELSE 0 END)", "SUM(CASE WHEN \"Booking Status\" = 'Cancelled by Driver' THEN 1 ELSE 0 END)"] | 7 | 113.868 |
| [S14/Q12](#s14) | success | ["sheet1"] | 0 / {} | [] | ["COUNT(*)", "COUNT(*)", "COUNT(*)", "COUNT(*)", "SUM(CASE WHEN \"Booking Status\" = 'Completed' THEN 1 ELSE 0 END)", "SUM(CASE WHEN \"Booking Status\" = 'Cancelled by Driver' THEN 1 ELSE 0 END)", "SUM(CASE WHEN \"Booking Status\" = 'Cancelled by Customer' THEN 1 ELSE 0 END)", "SUM(CASE WHEN \"Booking Status\" IN ('Incomplete', 'No Driver Found') THEN 1 ELSE 0 END)"] | 1 | 49.752 |
| [S15/Q13](#s15) | success | ["sheet1"] | 0 / {} | ["CAST(SUBSTRING(\"Time\", 1, 2) AS INTEGER)"] | ["COUNT(*)", "AVG(\"Booking Value\")", "AVG(\"Booking Value\" / NULLIF(\"Ride Distance\", 0))", "SUM(\"Booking Value\")"] | 24 | 83.571 |
| [S16/Q14](#s16) | success | ["sheet1"] | 0 / {} | ["\"Payment Method\""] | ["COUNT(*)", "AVG(\"Booking Value\")", "AVG(\"Booking Value\" / NULLIF(\"Ride Distance\", 0))"] | 5 | 67.658 |
| [S17/Q15](#s17) | success | ["sheet1"] | 0 / {} | ["CAST(SUBSTRING(\"Time\", 1, 2) AS INTEGER)"] | ["COUNT(*)", "AVG(\"Booking Value\")", "AVG(\"Booking Value\" / NULLIF(\"Ride Distance\", 0))", "SUM(\"Booking Value\")"] | 12 | 65.61 |
| [S18/Q16](#s18) | success | ["sheet1"] | 0 / {} | ["CAST(STRFTIME('%w', \"Date\") AS INTEGER)"] | ["COUNT(*)", "AVG(\"Booking Value\")", "AVG(\"Booking Value\" / NULLIF(\"Ride Distance\", 0))", "SUM(\"Booking Value\")"] | 1 | 77.751 |
| [S19/Q17](#s19) | success | ["sheet1"] | 0 / {} | ["CAST(STRFTIME('%m', \"Date\") AS INTEGER)"] | ["COUNT(*)", "AVG(\"Booking Value\")", "AVG(\"Booking Value\" / NULLIF(\"Ride Distance\", 0))", "SUM(\"Booking Value\")"] | 1 | 76.462 |
| [S20/Q18](#s20) | success | ["sheet1"] | 0 / {} | [] | [] | 20 | 0.408 |
| [S21/Q19](#s21) | failed | ["sheet1"] | 0 / {} | [] | [] | unknown | 未取得；调用总时长 0.185 ms |
| [S22/Q20](#s22) | success | ["sheet1"] | 0 / {} | [] | [] | 20 | 0.421 |
| [S23/Q21](#s23) | success | ["sheet1"] | 0 / {} | [] | [] | 12 | 111.322 |
| [S24/Q22](#s24) | success | ["sheet1"] | 0 / {} | ["CAST(SUBSTRING(\"Date\", 6, INSTR(SUBSTRING(\"Date\", 6), '/') - 1) AS INTEGER)"] | ["COUNT(*)", "AVG(\"Booking Value\")", "AVG(\"Booking Value\" / NULLIF(\"Ride Distance\", 0))", "SUM(\"Booking Value\")"] | 12 | 107.734 |
| [S25/Q23](#s25) | failed | ["sheet1"] | 0 / {} | ["CAST(STRFTIME('%w', SUBSTRING(\"Date\", 1, 4) \|\| '-' \|\| SUBSTRING(\"Date\", 6, INSTR(SUBSTRING(\"Date\", 6), '/') - 1) \|\| '-' \|\| SUBSTRING(\"Date\", IIF(INSTR(SUBSTRING(\"Date\", 6), '/') = 0, 0, INSTR(SUBSTRING(\"Date\", 6), '/') + 6 - 1) + 1)) AS INTEGER)"] | ["COUNT(*)", "SUM(\"Booking Value\")"] | unknown | 未取得；调用总时长 0.172 ms |
| [S26/Q24](#s26) | failed | ["sheet1"] | 0 / {} | [] | [] | unknown | 未取得；调用总时长 0.194 ms |
| [S27/Q25](#s27) | success | ["sheet1"] | 0 / {} | [] | [] | 5 | 0.402 |
| [S28/Q26](#s28) | success | ["sheet1"] | 0 / {} | [] | [] | 8 | 281.594 |
| [S29/Q27](#s29) | success | ["sheet1"] | 0 / {} | ["STRFTIME('%w', SUBSTRING(\"Date\", 1, 4) \|\| '-' \|\| SUBSTRING(\"Date\", 6, INSTR(SUBSTRING(\"Date\", 6), '/') - 1) \|\| '-' \|\| SUBSTRING(\"Date\", INSTR(SUBSTRING(\"Date\", 6), '/') + 6))"] | ["COUNT(*)", "AVG(\"Booking Value\")", "AVG(\"Booking Value\" / NULLIF(\"Ride Distance\", 0))", "SUM(\"Booking Value\")"] | 7 | 178.286 |
| [S30/Q28](#s30) | success | ["sheet1"] | 0 / {} | ["CASE WHEN STRFTIME('%w', SUBSTRING(\"Date\", 1, 4) \|\| '-' \|\| SUBSTRING(\"Date\", 6, INSTR(SUBSTRING(\"Date\", 6), '/') - 1) \|\| '-' \|\| SUBSTRING(\"Date\", INSTR(SUBSTRING(\"Date\", 6), '/') + 6)) IS NULL THEN 'unparsed' ELSE 'parsed' END"] | ["COUNT(*)"] | 2 | 169.532 |
| [S31/Q29](#s31) | success | ["sheet1"] | 0 / {} | ["\"Date\""] | ["COUNT(*)"] | 20 | 165.371 |
| [S32/Q30](#s32) | success | ["sheet1"] | 0 / {} | [] | [] | 1 | 0.527 |
| [S33/Q31](#s33) | success | [] | 0 / {} | [] | [] | 1 | 0.291 |
| [S34/Q32](#s34) | success | ["sheet1"] | 0 / {} | [] | [] | 251 | 20.4 |
| [S35/Q33](#s35) | success | ["sheet1"] | 0 / {} | ["STRFTIME('%w', SUBSTRING(\"Date\", 1, 4) \|\| '-' \|\| PRINTF('%02d', CAST(SUBSTRING(\"Date\", 6, INSTR(SUBSTRING(\"Date\", 6), '/') - 1) AS INTEGER)) \|\| '-' \|\| PRINTF('%02d', CAST(SUBSTRING(\"Date\", INSTR(SUBSTRING(\"Date\", 6), '/') + 6) AS INTEGER)))"] | ["COUNT(*)", "AVG(\"Booking Value\")", "AVG(\"Booking Value\" / NULLIF(\"Ride Distance\", 0))", "SUM(\"Booking Value\")"] | 7 | 261.486 |
| [S36/Q34](#s36) | success | ["sheet1"] | 0 / {} | ["CASE WHEN \"Ride Distance\" <= 5 THEN '0-5 km' WHEN \"Ride Distance\" <= 10 THEN '5-10 km' WHEN \"Ride Distance\" <= 15 THEN '10-15 km' WHEN \"Ride Distance\" <= 20 THEN '15-20 km' WHEN \"Ride Distance\" <= 25 THEN '20-25 km' WHEN \"Ride Distance\" <= 30 THEN '25-30 km' WHEN \"Ride Distance\" <= 40 THEN '30-40 km' ELSE '40+ km' END"] | ["COUNT(*)", "AVG(\"Booking Value\")", "AVG(\"Booking Value\" / NULLIF(\"Ride Distance\", 0))", "MIN(\"Ride Distance\")"] | 8 | 85.051 |
| [S37/Q35](#s37) | success | ["sheet1"] | 0 / {} | ["\"Vehicle Type\""] | ["AVG(\"Booking Value\" / NULLIF(\"Ride Distance\", 0))", "SUM(\"Booking Value\")"] | 7 | 240.304 |
| [S38/Q36](#s38) | failed | ["sheet1"] | 0 / {} | [] | ["CORR(\"Booking Value\", \"Ride Distance\")"] | unknown | 未取得；调用总时长 0.129 ms |
| [S39/Q37](#s39) | success | ["sheet1"] | 0 / {} | [] | ["AVG(\"Booking Value\")", "AVG(\"Ride Distance\")"] | 1 | 21.645 |
| [S40/Q38](#s40) | success | ["sheet1"] | 0 / {} | [] | ["AVG(\"Booking Value\")", "AVG(\"Ride Distance\")"] | 1 | 22.476 |
| [S41/Q39](#s41) | success | ["sheet1"] | 0 / {} | ["CASE WHEN \"Driver Ratings\" < 3.5 THEN '3.0-3.4' WHEN \"Driver Ratings\" < 4.0 THEN '3.5-3.9' WHEN \"Driver Ratings\" < 4.5 THEN '4.0-4.4' ELSE '4.5-5.0' END"] | ["COUNT(*)", "AVG(\"Booking Value\")", "MIN(\"Driver Ratings\")", "COUNT(*)", "COUNT(*)", "COUNT(*)", "COUNT(*)", "COUNT(*)", "SUM(CASE WHEN \"Booking Status\" = 'Completed' THEN 1 ELSE 0 END)", "SUM(CASE WHEN \"Booking Status\" = 'Cancelled by Driver' THEN 1 ELSE 0 END)", "SUM(CASE WHEN \"Booking Status\" = 'Cancelled by Customer' THEN 1 ELSE 0 END)", "SUM(CASE WHEN \"Booking Status\" = 'No Driver Found' THEN 1 ELSE 0 END)", "SUM(CASE WHEN \"Booking Status\" = 'Incomplete' THEN 1 ELSE 0 END)"] | 4 | 93.146 |
| [S42/Q40](#s42) | success | ["sheet1"] | 0 / {} | ["CASE WHEN \"Driver Ratings\" < 3.5 THEN '3.0-3.4' WHEN \"Driver Ratings\" < 4.0 THEN '3.5-3.9' WHEN \"Driver Ratings\" < 4.5 THEN '4.0-4.4' ELSE '4.5-5.0' END"] | ["COUNT(*)", "SUM(\"Booking Value\")", "MIN(\"Driver Ratings\")"] | 4 | 68.853 |
| [S43/Q41](#s43) | success | ["sheet1"] | 0 / {} | ["\"Pickup Location\""] | ["COUNT(*)", "AVG(\"Booking Value\" / NULLIF(\"Ride Distance\", 0))", "SUM(\"Booking Value\")"] | 20 | 77.189 |
| [S44/Q42](#s44) | success | ["sheet1"] | 0 / {} | ["\"Vehicle Type\""] | ["COUNT(*)", "SUM(\"Booking Value\")", "AVG(\"Booking Value\")", "AVG(\"Ride Distance\")", "AVG(\"Booking Value\" / NULLIF(\"Ride Distance\", 0))", "COUNT(*)", "COUNT(*)"] | 7 | 77.669 |
| [S45/Q43](#s45) | success | ["sheet1"] | 0 / {} | ["CASE WHEN \"Voice Talk Average Time\" < 5 THEN '0-5 min' WHEN \"Voice Talk Average Time\" < 10 THEN '5-10 min' WHEN \"Voice Talk Average Time\" < 15 THEN '10-15 min' ELSE '15+ min' END"] | ["COUNT(*)", "AVG(\"Booking Value\")", "AVG(\"Booking Value\" / NULLIF(\"Ride Distance\", 0))", "AVG(\"Driver Ratings\")", "MIN(\"Voice Talk Average Time\")"] | 4 | 86.122 |
| [S46/Q44](#s46) | success | ["sheet1"] | 0 / {} | ["CASE WHEN \"Customer Technical Assistance Time\" < 5 THEN '0-5 min' WHEN \"Customer Technical Assistance Time\" < 10 THEN '5-10 min' WHEN \"Customer Technical Assistance Time\" < 15 THEN '10-15 min' ELSE '15+ min' END"] | ["COUNT(*)", "AVG(\"Booking Value\")", "AVG(\"Booking Value\" / NULLIF(\"Ride Distance\", 0))", "AVG(\"Driver Ratings\")", "MIN(\"Customer Technical Assistance Time\")"] | 1 | 81.766 |
| [S47/Q45](#s47) | success | ["sheet1"] | 0 / {} | [] | ["MIN(\"Customer Technical Assistance Time\")", "MAX(\"Customer Technical Assistance Time\")", "AVG(\"Customer Technical Assistance Time\")"] | 1 | 26.722 |
| [S48/Q46](#s48) | success | ["sheet1"] | 0 / {} | [] | [] | 20 | 60.663 |
| [S49/Q47](#s49) | success | ["sheet1"] | 0 / {} | ["CASE WHEN \"Customer Technical Assistance Time\" < 20 THEN '15-20 min' WHEN \"Customer Technical Assistance Time\" < 25 THEN '20-25 min' WHEN \"Customer Technical Assistance Time\" < 30 THEN '25-30 min' WHEN \"Customer Technical Assistance Time\" < 35 THEN '30-35 min' ELSE '35+ min' END"] | ["COUNT(*)", "AVG(\"Booking Value\")", "AVG(\"Booking Value\" / NULLIF(\"Ride Distance\", 0))", "AVG(\"Driver Ratings\")", "MIN(\"Customer Technical Assistance Time\")"] | 5 | 89.244 |
| [S50/Q48](#s50) | success | ["sheet1"] | 0 / {} | ["\"Vehicle Type\""] | ["COUNT(*)", "COUNT(*)", "COUNT(*)", "SUM(CASE WHEN \"Booking Status\" = 'No Driver Found' THEN 1 ELSE 0 END)", "SUM(CASE WHEN \"Booking Status\" = 'Cancelled by Driver' THEN 1 ELSE 0 END)", "SUM(CASE WHEN \"Booking Status\" = 'Incomplete' THEN 1 ELSE 0 END)"] | 7 | 97.204 |
| [S51/Q49](#s51) | success | ["sheet1"] | 0 / {} | ["\"Driver Cancellation Reason\""] | ["COUNT(*)"] | 4 | 24.562 |
| [S52/Q50](#s52) | success | ["sheet1"] | 0 / {} | ["\"Reason for cancelling by Customer\""] | ["COUNT(*)"] | 5 | 19.885 |
| [S53/Q51](#s53) | success | ["sheet1"] | 0 / {} | [] | [] | 93000 | 336.697 |
| [S54/Q52](#s54) | success | ["sheet1"] | 0 / {} | [] | [] | 93000 | 351.934 |
| [S55/Q53](#s55) | success | ["sheet1"] | 0 / {} | [] | [] | 93000 | 388.638 |
| [S56/Q54](#s56) | success | ["sheet1"] | 0 / {} | [] | ["COUNT(DISTINCT \"Customer ID\")", "COUNT(DISTINCT \"Booking ID\")", "COUNT(DISTINCT \"Date\")"] | 1 | 400.338 |
| [S57/Q55](#s57) | success | ["sheet1"] | 0 / {} | ["CAST(SUBSTRING(\"Time\", 1, 2) AS INTEGER)"] | ["COUNT(*)", "COUNT(*)", "COUNT(*)", "SUM(CASE WHEN \"Booking Status\" = 'No Driver Found' THEN 1 ELSE 0 END)", "SUM(CASE WHEN \"Booking Status\" = 'Completed' THEN 1 ELSE 0 END)"] | 24 | 98.723 |
| [S58/Q56](#s58) | success | ["sheet1"] | 0 / {} | ["\"Vehicle Type\""] | ["COUNT(*)", "AVG(\"Booking Value\")", "AVG(\"Ride Distance\")", "SUM(\"Booking Value\")"] | 7 | 69.287 |
| [S59/Q57](#s59) | success | ["sheet1"] | 0 / {} | ["CAST(SUBSTRING(\"Time\", 1, 2) AS INTEGER)"] | ["COUNT(*)", "COUNT(*)", "COUNT(*)", "COUNT(*)", "SUM(CASE WHEN \"Booking Status\" = 'No Driver Found' THEN 1 ELSE 0 END)", "SUM(CASE WHEN \"Booking Status\" = 'Completed' THEN 1 ELSE 0 END)", "SUM(CASE WHEN \"Booking Status\" = 'Cancelled by Driver' THEN 1 ELSE 0 END)"] | 12 | 84.325 |
| [S60/Q58](#s60) | success | ["sheet1"] | 0 / {} | ["\"Customer ID\"", "ride_count"] | ["COUNT(*)", "COUNT(*)", "COUNT(*)"] | 3 | 117.745 |
| [S61/Q59](#s61) | success | ["sheet1"] | 0 / {} | ["\"Customer ID\""] | ["COUNT(*)", "MIN(ride_count)", "MAX(ride_count)", "AVG(ride_count)"] | 1 | 101.681 |
| [S62/Q60](#s62) | success | ["sheet1"] | 0 / {} | [] | [] | 93000 | 341.05 |
| [S63/Q61](#s63) | success | ["sheet1"] | 0 / {} | ["\"Pickup Location\" \|\| ' → ' \|\| \"Drop Location\""] | ["COUNT(*)", "AVG(\"Booking Value\")", "AVG(\"Booking Value\" / NULLIF(\"Ride Distance\", 0))", "AVG(\"Ride Distance\")"] | 0 | 145.509 |
| [S64/Q62](#s64) | success | ["sheet1"] | 0 / {} | ["\"Drop Location\""] | ["COUNT(*)", "AVG(\"Booking Value\")", "AVG(\"Booking Value\" / NULLIF(\"Ride Distance\", 0))"] | 10 | 77.175 |
| [S65/Q63](#s65) | success | ["sheet1"] | 0 / {} | ["CAST(SUBSTRING(\"Date\", 6, INSTR(SUBSTRING(\"Date\", 6), '/') - 1) AS INTEGER)"] | ["COUNT(*)", "AVG(\"Booking Value\")", "AVG(\"Booking Value\" / NULLIF(\"Ride Distance\", 0))", "SUM(\"Booking Value\")"] | 12 | 106.216 |


## 元数据和设置

| SQL | 类别 | 状态 | 内容 |
| --- | --- | --- | --- |
| S1 | connection_setup | success | PRAGMA query_only=ON |
| S2 | metadata | success | SELECT name,sql FROM sqlite_master WHERE type='table' ORDER BY name |


## Python 与执行位置

人工源码审查：**database_first_violation**。Python performs repeated vehicle/hour/rating/location grouping, binning, counts/means and annual arithmetic scenarios over completed-ride rows. These are SQL-capable preparation and scenario calculations. Kruskal-Wallis/Mann-Whitney tests and plots are separately justified uses. A 93,000-row aggregate candidate has no row-count compression; correctness alone does not imply useful materialization or net speedup. [证据](../reviews/dacomp-022.json)。

P1：I need to compute correlation between Booking Value and Ride Distance, and visualize the distribution of fare per km by vehicle type, day of week, and driver rating. This is better done in Python because SQLite lacks CORR function and I need to create visualizations.

[源码](../../../runs/dsv4flash-db-first-full-01/dacomp-022/attempt-01/python/P1.py)；[输出](../../../runs/dsv4flash-db-first-full-01/dacomp-022/attempt-01/python/P1.stdout)；[错误](../../../runs/dsv4flash-db-first-full-01/dacomp-022/attempt-01/python/P1.stderr)。检出需人工核验的 SQL 可实现操作：groupby(, .query(, sort_values(；不能仅凭理由判为合规。

P2：I need to perform statistical tests (ANOVA/Kruskal-Wallis) to determine if differences in booking value and fare-per-km across vehicle types and rating bands are significant, and to estimate realistic annual earnings scenarios. SQLite lacks these statistical functions.

[源码](../../../runs/dsv4flash-db-first-full-01/dacomp-022/attempt-01/python/P2.py)；[输出](../../../runs/dsv4flash-db-first-full-01/dacomp-022/attempt-01/python/P2.stdout)；[错误](../../../runs/dsv4flash-db-first-full-01/dacomp-022/attempt-01/python/P2.stderr)。检出需人工核验的 SQL 可实现操作：groupby(, .query(, sort_values(；不能仅凭理由判为合规。

P3：I need to analyze whether ride distance differs by vehicle type (to explain per-km fare differences) and identify the most profitable pickup/drop locations and routes. This requires sorting and statistical summary which is clearer to visualize in Python.

[源码](../../../runs/dsv4flash-db-first-full-01/dacomp-022/attempt-01/python/P3.py)；[输出](../../../runs/dsv4flash-db-first-full-01/dacomp-022/attempt-01/python/P3.stdout)；[错误](../../../runs/dsv4flash-db-first-full-01/dacomp-022/attempt-01/python/P3.stderr)。检出需人工核验的 SQL 可实现操作：groupby(, .query(, sort_values(；不能仅凭理由判为合规。

P4：I need to create a final consolidated strategy visualization showing the relative impact of each earnings lever (weekend premium, location premium, per-ride value) and compute the final scenario numbers for the report.

[源码](../../../runs/dsv4flash-db-first-full-01/dacomp-022/attempt-01/python/P4.py)；[输出](../../../runs/dsv4flash-db-first-full-01/dacomp-022/attempt-01/python/P4.stdout)；[错误](../../../runs/dsv4flash-db-first-full-01/dacomp-022/attempt-01/python/P4.stderr)。检出需人工核验的 SQL 可实现操作：groupby(, .query(；不能仅凭理由判为合规。

## 优化机会

已验证候选。筛选限于精确 SQL、相同自包含 CTE、相同单表完整过滤、可分解单表聚合；未覆盖任意 Join 等价和一般谓词蕴含。全部候选都是 offline，未测在线预测。

| 候选 | 类型 | 已有结果 | 覆盖 SQL | 后续次数 | 中间行数 | 验证 | 成本 |
| --- | --- | --- | --- | --- | --- | --- | --- |
| C1 | exact-result reuse | True | ["S53", "S54"] | 1 | unknown | not_verified_cap | Not tested |
| C2 | aggregate MV | False | ["S6", "S13", "S14", "S50", "S57"] | 4 | 168 | verified | Not benchmarked; correctness alone does not establish net speedup. |
| C3 | common filtered view | False | ["S7", "S8", "S9", "S10", "S15", "S16", "S18", "S19", "S24", "S30", "S35", "S36", "S42", "S43", "S45", "S46", "S47", "S48", "S49", "S53", "S54", "S55", "S58", "S62", "S63", "S64", "S65"] | 26 | 93000 | verified | Warm-cache baseline 3700.187 ms vs build+reuse 3612.967 ms, ratio 1.024; five repetitions, see performance evidence. |
| C4 | aggregate MV | False | ["S7", "S8", "S9", "S10", "S15", "S16", "S18", "S19", "S24", "S30", "S35", "S36", "S42", "S43", "S45", "S46", "S47", "S49", "S58", "S64", "S65"] | 20 | 93000 | verified | Not benchmarked; correctness alone does not establish net speedup. |
| C5 | common filtered view | False | ["S32", "S34"] | 1 | unknown | not_verified_cap | Not tested |


已验证覆盖（含触发查询、候选并集去重）：32/59 条成功数据 SQL。正确性仅针对当前数据库快照；未测性能的候选不能声称已加速。

[完整 build/rewrite 与比较证据](dacomp-022.analysis.json)。

### C3：common filtered view

Same single source and complete filter; original filter retained.

原查询 [S7](#s7), [S8](#s8), [S9](#s9), [S10](#s10), [S15](#s15), [S16](#s16), [S18](#s18), [S19](#s19), [S24](#s24), [S30](#s30), [S35](#s35), [S36](#s36), [S42](#s42), [S43](#s43), [S45](#s45), [S46](#s46), [S47](#s47), [S48](#s48), [S49](#s49), [S53](#s53), [S54](#s54), [S55](#s55), [S58](#s58), [S62](#s62), [S63](#s63), [S64](#s64), [S65](#s65) → 新增共享状态 C3 → 后续 26 次可复用。该构建点为事后假设，不代表 Agent 当时预知后续。

构建定义：

```sql
SELECT * FROM "sheet1" WHERE "Booking Status" = 'Completed'
```

受益查询 S7 的改写示例：

```sql
SELECT "Vehicle Type", COUNT(*) AS ride_count, ROUND(AVG("Booking Value"), 2) AS avg_booking_value, ROUND(AVG("Ride Distance"), 2) AS avg_distance, ROUND(AVG("Booking Value" / NULLIF("Ride Distance", 0)), 2) AS avg_fare_per_km, ROUND(AVG("Driver Ratings"), 2) AS avg_driver_rating, ROUND(SUM("Booking Value"), 2) AS total_earnings FROM temp.reuse_candidate AS sheet1 WHERE "Booking Status" = 'Completed' GROUP BY "Vehicle Type" ORDER BY avg_fare_per_km DESC
```

| 原 SQL | 列名一致 | 结果一致 | 比较方法 |
| --- | --- | --- | --- |
| S7 | True | True | ordered_numeric_tolerance |
| S8 | True | True | exact_multiset |
| S9 | True | True | ordered_numeric_tolerance |
| S10 | True | True | exact_multiset |
| S15 | True | True | ordered_numeric_tolerance |
| S16 | True | True | ordered_numeric_tolerance |
| S18 | True | True | ordered_numeric_tolerance |
| S19 | True | True | ordered_numeric_tolerance |
| S24 | True | True | ordered_numeric_tolerance |
| S30 | True | True | exact_multiset |
| S35 | True | True | ordered_numeric_tolerance |
| S36 | True | True | ordered_numeric_tolerance |
| S42 | True | True | ordered_numeric_tolerance |
| S43 | True | True | ordered_numeric_tolerance |
| S45 | True | True | ordered_numeric_tolerance |
| S46 | True | True | ordered_numeric_tolerance |
| S47 | True | True | exact_multiset |
| S48 | True | True | ordered_numeric_tolerance |
| S49 | True | True | ordered_numeric_tolerance |
| S53 | True | True | exact_multiset |
| S54 | True | True | exact_multiset |
| S55 | True | True | exact_multiset |
| S58 | True | True | ordered_numeric_tolerance |
| S62 | True | True | exact_multiset |
| S63 | True | True | ordered_numeric_tolerance |
| S64 | True | True | ordered_numeric_tolerance |
| S65 | True | True | ordered_numeric_tolerance |


验证状态：verified；成本结论：Warm-cache baseline 3700.187 ms vs build+reuse 3612.967 ms, ratio 1.024; five repetitions, see performance evidence.

### C4：aggregate MV

Union of grouping keys; decomposable aggregate states; AVG uses SUM and non-NULL COUNT.

原查询 [S7](#s7), [S8](#s8), [S9](#s9), [S10](#s10), [S15](#s15), [S16](#s16), [S18](#s18), [S19](#s19), [S24](#s24), [S30](#s30), [S35](#s35), [S36](#s36), [S42](#s42), [S43](#s43), [S45](#s45), [S46](#s46), [S47](#s47), [S49](#s49), [S58](#s58), [S64](#s64), [S65](#s65) → 新增共享状态 C4 → 后续 20 次可复用。该构建点为事后假设，不代表 Agent 当时预知后续。

构建定义：

```sql
SELECT "Vehicle Type" AS __g0, "Driver Ratings" AS __g1, CAST(SUBSTRING("Time", 1, 2) AS INTEGER) AS __g2, "Payment Method" AS __g3, CAST(STRFTIME('%w', "Date") AS INTEGER) AS __g4, CAST(STRFTIME('%m', "Date") AS INTEGER) AS __g5, CAST(SUBSTRING("Date", 6, INSTR(SUBSTRING("Date", 6), '/') - 1) AS INTEGER) AS __g6, CASE WHEN STRFTIME('%w', SUBSTRING("Date", 1, 4) || '-' || SUBSTRING("Date", 6, INSTR(SUBSTRING("Date", 6), '/') - 1) || '-' || SUBSTRING("Date", INSTR(SUBSTRING("Date", 6), '/') + 6)) IS NULL THEN 'unparsed' ELSE 'parsed' END AS __g7, STRFTIME('%w', SUBSTRING("Date", 1, 4) || '-' || PRINTF('%02d', CAST(SUBSTRING("Date", 6, INSTR(SUBSTRING("Date", 6), '/') - 1) AS INTEGER)) || '-' || PRINTF('%02d', CAST(SUBSTRING("Date", INSTR(SUBSTRING("Date", 6), '/') + 6) AS INTEGER))) AS __g8, CASE WHEN "Ride Distance" <= 5 THEN '0-5 km' WHEN "Ride Distance" <= 10 THEN '5-10 km' WHEN "Ride Distance" <= 15 THEN '10-15 km' WHEN "Ride Distance" <= 20 THEN '15-20 km' WHEN "Ride Distance" <= 25 THEN '20-25 km' WHEN "Ride Distance" <= 30 THEN '25-30 km' WHEN "Ride Distance" <= 40 THEN '30-40 km' ELSE '40+ km' END AS __g9, CASE WHEN "Driver Ratings" < 3.5 THEN '3.0-3.4' WHEN "Driver Ratings" < 4.0 THEN '3.5-3.9' WHEN "Driver Ratings" < 4.5 THEN '4.0-4.4' ELSE '4.5-5.0' END AS __g10, "Pickup Location" AS __g11, CASE WHEN "Voice Talk Average Time" < 5 THEN '0-5 min' WHEN "Voice Talk Average Time" < 10 THEN '5-10 min' WHEN "Voice Talk Average Time" < 15 THEN '10-15 min' ELSE '15+ min' END AS __g12, CASE WHEN "Customer Technical Assistance Time" < 5 THEN '0-5 min' WHEN "Customer Technical Assistance Time" < 10 THEN '5-10 min' WHEN "Customer Technical Assistance Time" < 15 THEN '10-15 min' ELSE '15+ min' END AS __g13, CASE WHEN "Customer Technical Assistance Time" < 20 THEN '15-20 min' WHEN "Customer Technical Assistance Time" < 25 THEN '20-25 min' WHEN "Customer Technical Assistance Time" < 30 THEN '25-30 min' WHEN "Customer Technical Assistance Time" < 35 THEN '30-35 min' ELSE '35+ min' END AS __g14, "Drop Location" AS __g15, COUNT(*) AS __a0, SUM("Booking Value") AS __a1_sum, COUNT("Booking Value") AS __a1_n, SUM("Ride Distance") AS __a2_sum, COUNT("Ride Distance") AS __a2_n, SUM("Booking Value" / NULLIF("Ride Distance", 0)) AS __a3_sum, COUNT("Booking Value" / NULLIF("Ride Distance", 0)) AS __a3_n, SUM("Driver Ratings") AS __a4_sum, COUNT("Driver Ratings") AS __a4_n, SUM("Booking Value") AS __a5, MIN("Driver Ratings") AS __a6, MAX("Driver Ratings") AS __a7, MIN("Booking Value") AS __a8, MAX("Booking Value") AS __a9, MIN("Ride Distance") AS __a10, MAX("Ride Distance") AS __a11, MIN("Voice Talk Average Time") AS __a12, MIN("Customer Technical Assistance Time") AS __a13, MAX("Customer Technical Assistance Time") AS __a14, SUM("Customer Technical Assistance Time") AS __a15_sum, COUNT("Customer Technical Assistance Time") AS __a15_n FROM "sheet1" WHERE "Booking Status" = 'Completed' GROUP BY "Vehicle Type", "Driver Ratings", CAST(SUBSTRING("Time", 1, 2) AS INTEGER), "Payment Method", CAST(STRFTIME('%w', "Date") AS INTEGER), CAST(STRFTIME('%m', "Date") AS INTEGER), CAST(SUBSTRING("Date", 6, INSTR(SUBSTRING("Date", 6), '/') - 1) AS INTEGER), CASE WHEN STRFTIME('%w', SUBSTRING("Date", 1, 4) || '-' || SUBSTRING("Date", 6, INSTR(SUBSTRING("Date", 6), '/') - 1) || '-' || SUBSTRING("Date", INSTR(SUBSTRING("Date", 6), '/') + 6)) IS NULL THEN 'unparsed' ELSE 'parsed' END, STRFTIME('%w', SUBSTRING("Date", 1, 4) || '-' || PRINTF('%02d', CAST(SUBSTRING("Date", 6, INSTR(SUBSTRING("Date", 6), '/') - 1) AS INTEGER)) || '-' || PRINTF('%02d', CAST(SUBSTRING("Date", INSTR(SUBSTRING("Date", 6), '/') + 6) AS INTEGER))), CASE WHEN "Ride Distance" <= 5 THEN '0-5 km' WHEN "Ride Distance" <= 10 THEN '5-10 km' WHEN "Ride Distance" <= 15 THEN '10-15 km' WHEN "Ride Distance" <= 20 THEN '15-20 km' WHEN "Ride Distance" <= 25 THEN '20-25 km' WHEN "Ride Distance" <= 30 THEN '25-30 km' WHEN "Ride Distance" <= 40 THEN '30-40 km' ELSE '40+ km' END, CASE WHEN "Driver Ratings" < 3.5 THEN '3.0-3.4' WHEN "Driver Ratings" < 4.0 THEN '3.5-3.9' WHEN "Driver Ratings" < 4.5 THEN '4.0-4.4' ELSE '4.5-5.0' END, "Pickup Location", CASE WHEN "Voice Talk Average Time" < 5 THEN '0-5 min' WHEN "Voice Talk Average Time" < 10 THEN '5-10 min' WHEN "Voice Talk Average Time" < 15 THEN '10-15 min' ELSE '15+ min' END, CASE WHEN "Customer Technical Assistance Time" < 5 THEN '0-5 min' WHEN "Customer Technical Assistance Time" < 10 THEN '5-10 min' WHEN "Customer Technical Assistance Time" < 15 THEN '10-15 min' ELSE '15+ min' END, CASE WHEN "Customer Technical Assistance Time" < 20 THEN '15-20 min' WHEN "Customer Technical Assistance Time" < 25 THEN '20-25 min' WHEN "Customer Technical Assistance Time" < 30 THEN '25-30 min' WHEN "Customer Technical Assistance Time" < 35 THEN '30-35 min' ELSE '35+ min' END, "Drop Location"
```

受益查询 S7 的改写示例：

```sql
SELECT __g0 AS "Vehicle Type", SUM(__a0) AS ride_count, ROUND((1.0 * SUM(__a1_sum) / NULLIF(SUM(__a1_n), 0)), 2) AS avg_booking_value, ROUND((1.0 * SUM(__a2_sum) / NULLIF(SUM(__a2_n), 0)), 2) AS avg_distance, ROUND((1.0 * SUM(__a3_sum) / NULLIF(SUM(__a3_n), 0)), 2) AS avg_fare_per_km, ROUND((1.0 * SUM(__a4_sum) / NULLIF(SUM(__a4_n), 0)), 2) AS avg_driver_rating, ROUND(SUM(__a5), 2) AS total_earnings FROM temp.reuse_candidate GROUP BY __g0 ORDER BY avg_fare_per_km DESC
```

| 原 SQL | 列名一致 | 结果一致 | 比较方法 |
| --- | --- | --- | --- |
| S7 | True | True | ordered_numeric_tolerance |
| S8 | True | True | exact_multiset |
| S9 | True | True | ordered_numeric_tolerance |
| S10 | True | True | exact_multiset |
| S15 | True | True | ordered_numeric_tolerance |
| S16 | True | True | ordered_numeric_tolerance |
| S18 | True | True | ordered_numeric_tolerance |
| S19 | True | True | ordered_numeric_tolerance |
| S24 | True | True | ordered_numeric_tolerance |
| S30 | True | True | exact_multiset |
| S35 | True | True | ordered_numeric_tolerance |
| S36 | True | True | ordered_numeric_tolerance |
| S42 | True | True | ordered_numeric_tolerance |
| S43 | True | True | ordered_numeric_tolerance |
| S45 | True | True | ordered_numeric_tolerance |
| S46 | True | True | ordered_numeric_tolerance |
| S47 | True | True | exact_multiset |
| S49 | True | True | ordered_numeric_tolerance |
| S58 | True | True | ordered_numeric_tolerance |
| S64 | True | True | ordered_numeric_tolerance |
| S65 | True | True | ordered_numeric_tolerance |


验证状态：verified；成本结论：Not benchmarked; correctness alone does not establish net speedup.

### C2：aggregate MV

Union of grouping keys; decomposable aggregate states; AVG uses SUM and non-NULL COUNT.

原查询 [S6](#s6), [S13](#s13), [S14](#s14), [S50](#s50), [S57](#s57) → 新增共享状态 C2 → 后续 4 次可复用。该构建点为事后假设，不代表 Agent 当时预知后续。

构建定义：

```sql
SELECT "Vehicle Type" AS __g0, CAST(SUBSTRING("Time", 1, 2) AS INTEGER) AS __g1, COUNT(*) AS __a0, COUNT("Booking Value") AS __a1, COUNT("Ride Distance") AS __a2, COUNT("Driver Ratings") AS __a3, SUM(CASE WHEN "Booking Status" = 'Completed' THEN 1 ELSE 0 END) AS __a4, SUM(CASE WHEN "Booking Status" = 'Cancelled by Driver' THEN 1 ELSE 0 END) AS __a5, SUM(CASE WHEN "Booking Status" = 'Cancelled by Customer' THEN 1 ELSE 0 END) AS __a6, SUM(CASE WHEN "Booking Status" = 'Incomplete' THEN 1 ELSE 0 END) AS __a7, SUM(CASE WHEN "Booking Status" = 'No Driver Found' THEN 1 ELSE 0 END) AS __a8, SUM(CASE WHEN "Booking Status" IN ('Incomplete', 'No Driver Found') THEN 1 ELSE 0 END) AS __a9 FROM "sheet1"  GROUP BY "Vehicle Type", CAST(SUBSTRING("Time", 1, 2) AS INTEGER)
```

受益查询 S6 的改写示例：

```sql
SELECT SUM(__a0) AS total_rows, SUM(__a1) AS has_value, SUM(__a2) AS has_distance, SUM(__a3) AS has_rating FROM temp.reuse_candidate
```

| 原 SQL | 列名一致 | 结果一致 | 比较方法 |
| --- | --- | --- | --- |
| S6 | True | True | exact_multiset |
| S13 | True | True | ordered_numeric_tolerance |
| S14 | True | True | exact_multiset |
| S50 | True | True | ordered_numeric_tolerance |
| S57 | True | True | ordered_numeric_tolerance |


验证状态：verified；成本结论：Not benchmarked; correctness alone does not establish net speedup.

[性能证据 C3](dacomp-022.C3.performance.json)：measured。

结果依赖：自动记录 SQL→Python 的接口父调用，以及源码中引用归档文件的消费者；字面值相同不认定因果。模型方向选择需要人工读取消息，尚未做全面因果标注。

[原始报告](../../../runs/dsv4flash-db-first-full-01/dacomp-022/attempt-01/answer.md)；[统一消息](../../../runs/dsv4flash-db-first-full-01/dacomp-022/attempt-01/messages.jsonl)；[原始 OpenCode 事件](../../../runs/dsv4flash-db-first-full-01/dacomp-022/attempt-01/opencode.jsonl)；[SQL 引擎日志](../../../runs/dsv4flash-db-first-full-01/dacomp-022/attempt-01/sql_journal.jsonl)。

[可读报告（本地图片链接规范化）](../answers/dacomp-022.md)。原始回答保留，分析结论未改写。

## S1

类别 `connection_setup`；来源 `connection`；调用 `db9c7feba38f4f0a992d107dcc100a5d`；状态 `success`。

```sql
PRAGMA query_only=ON
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-022/attempt-01/sql/S1.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-022/attempt-01/sql/S1.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-022/attempt-01/results/S1.rows.jsonl)；完整：True；SHA256：`e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`。

## S2

类别 `metadata`；来源 `list_db`；调用 `db9c7feba38f4f0a992d107dcc100a5d`；状态 `success`。

```sql
SELECT name,sql FROM sqlite_master WHERE type='table' ORDER BY name
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-022/attempt-01/sql/S2.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-022/attempt-01/sql/S2.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-022/attempt-01/results/S2.rows.jsonl)；完整：True；SHA256：`c342ec0fa7df72007bdc6a8a6d4cc9704995ccdcc9eace19d76e76f9a51240ee`。

## S3

类别 `data`；来源 `query_db`；调用 `166345838a584711ac0bbb9390e29d5f`；状态 `success`。

```sql
SELECT * FROM sheet1 LIMIT 20
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-022/attempt-01/sql/S3.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-022/attempt-01/sql/S3.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-022/attempt-01/results/S3.rows.jsonl)；完整：True；SHA256：`d5532a360ab05c28267ef808e3358bf7e8c5cfdd540fa7d8877298efbaba3760`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "sheet1", "kind": "base", "block": null, "base_tables": ["sheet1"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |


## S4

类别 `data`；来源 `query_db`；调用 `14996d93fa1f4ac6ba26016a33f91c1d`；状态 `success`。

```sql
SELECT DISTINCT "Vehicle Type" FROM sheet1 ORDER BY "Vehicle Type"
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-022/attempt-01/sql/S4.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-022/attempt-01/sql/S4.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-022/attempt-01/results/S4.rows.jsonl)；完整：True；SHA256：`d72ee06b1ea945ce6c21fdda518401ca41716f763d199de19fa226844bcea7f1`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "sheet1", "kind": "base", "block": null, "base_tables": ["sheet1"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |


## S5

类别 `data`；来源 `query_db`；调用 `fd857f73a4e246e183e1d0eaeaf2610c`；状态 `success`。

```sql
SELECT DISTINCT "Booking Status" FROM sheet1 ORDER BY "Booking Status"
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-022/attempt-01/sql/S5.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-022/attempt-01/sql/S5.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-022/attempt-01/results/S5.rows.jsonl)；完整：True；SHA256：`aa74e49927b1c97d9fa3c3742b672a1ac6cc5b34630c30590107334e30918ed9`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "sheet1", "kind": "base", "block": null, "base_tables": ["sheet1"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |


## S6

类别 `data`；来源 `query_db`；调用 `7998e5d525054dae9a788f5bc5523bd8`；状态 `success`。

```sql
SELECT COUNT(*) as total_rows, 
       COUNT("Booking Value") as has_value,
       COUNT("Ride Distance") as has_distance,
       COUNT("Driver Ratings") as has_rating
FROM sheet1
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-022/attempt-01/sql/S6.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-022/attempt-01/sql/S6.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-022/attempt-01/results/S6.rows.jsonl)；完整：True；SHA256：`9f536ad9f11043b4ae921458119a94db2ba3fde2964239b7ff86454c809e629f`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "sheet1", "kind": "base", "block": null, "base_tables": ["sheet1"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |
| B1 | COUNT("Booking Value") | [{"table": "sheet1", "column": "Booking Value"}] | [] | False |
| B1 | COUNT("Ride Distance") | [{"table": "sheet1", "column": "Ride Distance"}] | [] | False |
| B1 | COUNT("Driver Ratings") | [{"table": "sheet1", "column": "Driver Ratings"}] | [] | False |


## S7

类别 `data`；来源 `query_db`；调用 `ce87c0af2eac4fcdbfda0351e40d01b6`；状态 `success`。

```sql
SELECT "Vehicle Type",
       COUNT(*) as ride_count,
       ROUND(AVG("Booking Value"), 2) as avg_booking_value,
       ROUND(AVG("Ride Distance"), 2) as avg_distance,
       ROUND(AVG("Booking Value" / NULLIF("Ride Distance", 0)), 2) as avg_fare_per_km,
       ROUND(AVG("Driver Ratings"), 2) as avg_driver_rating,
       ROUND(SUM("Booking Value"), 2) as total_earnings
FROM sheet1
WHERE "Booking Status" = 'Completed'
GROUP BY "Vehicle Type"
ORDER BY avg_fare_per_km DESC
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-022/attempt-01/sql/S7.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-022/attempt-01/sql/S7.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-022/attempt-01/results/S7.rows.jsonl)；完整：True；SHA256：`6f1c8e7953b7bd42bba27853eadf35de69e5a0bbfd0c388eb561e76adf5d1fd2`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "sheet1", "kind": "base", "block": null, "base_tables": ["sheet1"]}] | [] | ["\"Vehicle Type\""] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |
| B1 | AVG("Booking Value") | [{"table": "sheet1", "column": "Booking Value"}] | [] | False |
| B1 | AVG("Ride Distance") | [{"table": "sheet1", "column": "Ride Distance"}] | [] | False |
| B1 | AVG("Booking Value" / NULLIF("Ride Distance", 0)) | [{"table": "sheet1", "column": "Booking Value"}, {"table": "sheet1", "column": "Ride Distance"}] | [] | False |
| B1 | AVG("Driver Ratings") | [{"table": "sheet1", "column": "Driver Ratings"}] | [] | False |
| B1 | SUM("Booking Value") | [{"table": "sheet1", "column": "Booking Value"}] | [] | False |


## S8

类别 `data`；来源 `query_db`；调用 `791b143eb0ba4274badbf30fb8897de9`；状态 `success`。

```sql
SELECT 
       ROUND(AVG("Booking Value" / NULLIF("Ride Distance", 0)), 2) as overall_fare_per_km,
       ROUND(AVG("Booking Value"), 2) as overall_avg_booking,
       ROUND(AVG("Ride Distance"), 2) as overall_avg_distance,
       ROUND(SUM("Booking Value"), 2) as overall_total_earnings,
       COUNT(*) as completed_rides
FROM sheet1
WHERE "Booking Status" = 'Completed'
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-022/attempt-01/sql/S8.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-022/attempt-01/sql/S8.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-022/attempt-01/results/S8.rows.jsonl)；完整：True；SHA256：`b7d224515a7d82bdc7b19e3573a212810298eed74f500635c214866447238383`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "sheet1", "kind": "base", "block": null, "base_tables": ["sheet1"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |
| B1 | AVG("Booking Value" / NULLIF("Ride Distance", 0)) | [{"table": "sheet1", "column": "Booking Value"}, {"table": "sheet1", "column": "Ride Distance"}] | [] | False |
| B1 | AVG("Booking Value") | [{"table": "sheet1", "column": "Booking Value"}] | [] | False |
| B1 | AVG("Ride Distance") | [{"table": "sheet1", "column": "Ride Distance"}] | [] | False |
| B1 | SUM("Booking Value") | [{"table": "sheet1", "column": "Booking Value"}] | [] | False |


## S9

类别 `data`；来源 `query_db`；调用 `93d67c8f1b6a488b965314d1bdff9bbc`；状态 `success`。

```sql
SELECT "Driver Ratings",
       COUNT(*) as ride_count,
       ROUND(AVG("Booking Value"), 2) as avg_booking_value,
       ROUND(AVG("Booking Value" / NULLIF("Ride Distance", 0)), 2) as avg_fare_per_km,
       ROUND(SUM("Booking Value"), 2) as total_earnings
FROM sheet1
WHERE "Booking Status" = 'Completed'
GROUP BY "Driver Ratings"
ORDER BY "Driver Ratings"
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-022/attempt-01/sql/S9.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-022/attempt-01/sql/S9.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-022/attempt-01/results/S9.rows.jsonl)；完整：True；SHA256：`09fcd372c780eda5c2112b16d30f7680a6bd1f0adc6673eeffa5f4e37aae1fa6`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "sheet1", "kind": "base", "block": null, "base_tables": ["sheet1"]}] | [] | ["\"Driver Ratings\""] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |
| B1 | AVG("Booking Value") | [{"table": "sheet1", "column": "Booking Value"}] | [] | False |
| B1 | AVG("Booking Value" / NULLIF("Ride Distance", 0)) | [{"table": "sheet1", "column": "Booking Value"}, {"table": "sheet1", "column": "Ride Distance"}] | [] | False |
| B1 | SUM("Booking Value") | [{"table": "sheet1", "column": "Booking Value"}] | [] | False |


## S10

类别 `data`；来源 `query_db`；调用 `585ea133c8b348b6a86cc212ec83c3bb`；状态 `success`。

```sql
SELECT MIN("Driver Ratings") as min_r, MAX("Driver Ratings") as max_r,
       ROUND(AVG("Driver Ratings"),2) as avg_r,
       MIN("Booking Value") as min_bv, MAX("Booking Value") as max_bv,
       MIN("Ride Distance") as min_d, MAX("Ride Distance") as max_d
FROM sheet1 WHERE "Booking Status" = 'Completed'
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-022/attempt-01/sql/S10.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-022/attempt-01/sql/S10.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-022/attempt-01/results/S10.rows.jsonl)；完整：True；SHA256：`0e3a84ccb7e33ac8e3eddcf72118d74e7f067a038794acf68c08879ad5342d21`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "sheet1", "kind": "base", "block": null, "base_tables": ["sheet1"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | MIN("Driver Ratings") | [{"table": "sheet1", "column": "Driver Ratings"}] | [] | False |
| B1 | MAX("Driver Ratings") | [{"table": "sheet1", "column": "Driver Ratings"}] | [] | False |
| B1 | MIN("Booking Value") | [{"table": "sheet1", "column": "Booking Value"}] | [] | False |
| B1 | MAX("Booking Value") | [{"table": "sheet1", "column": "Booking Value"}] | [] | False |
| B1 | MIN("Ride Distance") | [{"table": "sheet1", "column": "Ride Distance"}] | [] | False |
| B1 | MAX("Ride Distance") | [{"table": "sheet1", "column": "Ride Distance"}] | [] | False |
| B1 | AVG("Driver Ratings") | [{"table": "sheet1", "column": "Driver Ratings"}] | [] | False |


## S11

类别 `data`；来源 `query_db`；调用 `64887400a3f746a3860aebde8d6a21de`；状态 `success`。

```sql
SELECT "Driver Ratings",
       COUNT(*) as ride_count,
       ROUND(AVG("Booking Value"), 2) as avg_booking_value,
       ROUND(AVG("Booking Value" / NULLIF("Ride Distance", 0)), 2) as avg_fare_per_km,
       ROUND(SUM("Booking Value"), 2) as total_earnings,
       ROUND(100.0*COUNT(*)/SUM(COUNT(*)) OVER (), 2) as pct_of_rides
FROM sheet1
WHERE "Booking Status" = 'Completed'
GROUP BY "Driver Ratings"
ORDER BY "Driver Ratings"
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-022/attempt-01/sql/S11.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-022/attempt-01/sql/S11.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-022/attempt-01/results/S11.rows.jsonl)；完整：True；SHA256：`ec8ea4e6028460229a800741bdd675ff413153b2f870807e1b7ccd395bb9ce5f`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "sheet1", "kind": "base", "block": null, "base_tables": ["sheet1"]}] | [] | ["\"Driver Ratings\""] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |
| B1 | AVG("Booking Value") | [{"table": "sheet1", "column": "Booking Value"}] | [] | False |
| B1 | AVG("Booking Value" / NULLIF("Ride Distance", 0)) | [{"table": "sheet1", "column": "Booking Value"}, {"table": "sheet1", "column": "Ride Distance"}] | [] | False |
| B1 | SUM("Booking Value") | [{"table": "sheet1", "column": "Booking Value"}] | [] | False |
| B1 | COUNT(*) | [] | [] | True |
| B1 | COUNT(*) | [] | [] | True |


## S12

类别 `data`；来源 `query_db`；调用 `c356959cfb414a9bb84556000b737bd1`；状态 `success`。

```sql
SELECT "Driver Ratings",
       COUNT(*) as ride_count,
       ROUND(AVG("Booking Value"), 2) as avg_booking_value,
       ROUND(AVG("Booking Value" / NULLIF("Ride Distance", 0)), 2) as avg_fare_per_km,
       ROUND(SUM("Booking Value"), 2) as total_earnings
FROM sheet1
WHERE "Booking Status" = 'Completed' AND "Driver Ratings" >= 4.2
GROUP BY "Driver Ratings"
ORDER BY "Driver Ratings"
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-022/attempt-01/sql/S12.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-022/attempt-01/sql/S12.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-022/attempt-01/results/S12.rows.jsonl)；完整：True；SHA256：`26dd5f858a2229ed4c90319f38c3bb52e88ae7cdbfffe16d09ca82738af42bc9`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "sheet1", "kind": "base", "block": null, "base_tables": ["sheet1"]}] | [] | ["\"Driver Ratings\""] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |
| B1 | AVG("Booking Value") | [{"table": "sheet1", "column": "Booking Value"}] | [] | False |
| B1 | AVG("Booking Value" / NULLIF("Ride Distance", 0)) | [{"table": "sheet1", "column": "Booking Value"}, {"table": "sheet1", "column": "Ride Distance"}] | [] | False |
| B1 | SUM("Booking Value") | [{"table": "sheet1", "column": "Booking Value"}] | [] | False |


## S13

类别 `data`；来源 `query_db`；调用 `f4f9c57d0c2b4a42b84d9a8291199a46`；状态 `success`。

```sql
SELECT "Vehicle Type",
       COUNT(*) as total_bookings,
       SUM(CASE WHEN "Booking Status" = 'Completed' THEN 1 ELSE 0 END) as completed,
       SUM(CASE WHEN "Booking Status" = 'Cancelled by Driver' THEN 1 ELSE 0 END) as cancelled_by_driver,
       SUM(CASE WHEN "Booking Status" = 'Cancelled by Customer' THEN 1 ELSE 0 END) as cancelled_by_customer,
       SUM(CASE WHEN "Booking Status" = 'Incomplete' THEN 1 ELSE 0 END) as incomplete,
       SUM(CASE WHEN "Booking Status" = 'No Driver Found' THEN 1 ELSE 0 END) as no_driver_found,
       ROUND(100.0 * SUM(CASE WHEN "Booking Status" = 'Completed' THEN 1 ELSE 0 END) / COUNT(*), 2) as completion_rate,
       ROUND(100.0 * SUM(CASE WHEN "Booking Status" = 'Cancelled by Driver' THEN 1 ELSE 0 END) / COUNT(*), 2) as driver_cancellation_rate
FROM sheet1
GROUP BY "Vehicle Type"
ORDER BY completion_rate DESC
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-022/attempt-01/sql/S13.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-022/attempt-01/sql/S13.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-022/attempt-01/results/S13.rows.jsonl)；完整：True；SHA256：`e338a46f08ab1b0255d79fc47f21d48658debe71dd175653b4eafc6e009716ee`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "sheet1", "kind": "base", "block": null, "base_tables": ["sheet1"]}] | [] | ["\"Vehicle Type\""] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |
| B1 | SUM(CASE WHEN "Booking Status" = 'Completed' THEN 1 ELSE 0 END) | [] | [{"table": "sheet1", "column": "Booking Status"}] | False |
| B1 | SUM(CASE WHEN "Booking Status" = 'Cancelled by Driver' THEN 1 ELSE 0 END) | [] | [{"table": "sheet1", "column": "Booking Status"}] | False |
| B1 | SUM(CASE WHEN "Booking Status" = 'Cancelled by Customer' THEN 1 ELSE 0 END) | [] | [{"table": "sheet1", "column": "Booking Status"}] | False |
| B1 | SUM(CASE WHEN "Booking Status" = 'Incomplete' THEN 1 ELSE 0 END) | [] | [{"table": "sheet1", "column": "Booking Status"}] | False |
| B1 | SUM(CASE WHEN "Booking Status" = 'No Driver Found' THEN 1 ELSE 0 END) | [] | [{"table": "sheet1", "column": "Booking Status"}] | False |
| B1 | COUNT(*) | [] | [] | True |
| B1 | COUNT(*) | [] | [] | True |
| B1 | SUM(CASE WHEN "Booking Status" = 'Completed' THEN 1 ELSE 0 END) | [] | [{"table": "sheet1", "column": "Booking Status"}] | False |
| B1 | SUM(CASE WHEN "Booking Status" = 'Cancelled by Driver' THEN 1 ELSE 0 END) | [] | [{"table": "sheet1", "column": "Booking Status"}] | False |


## S14

类别 `data`；来源 `query_db`；调用 `c9963b5f6a5d4d44bbb58396e4af1ed1`；状态 `success`。

```sql
SELECT 
       ROUND(100.0 * SUM(CASE WHEN "Booking Status" = 'Completed' THEN 1 ELSE 0 END) / COUNT(*), 2) as overall_completion_rate,
       ROUND(100.0 * SUM(CASE WHEN "Booking Status" = 'Cancelled by Driver' THEN 1 ELSE 0 END) / COUNT(*), 2) as driver_cancel_rate,
       ROUND(100.0 * SUM(CASE WHEN "Booking Status" = 'Cancelled by Customer' THEN 1 ELSE 0 END) / COUNT(*), 2) as customer_cancel_rate,
       ROUND(100.0 * SUM(CASE WHEN "Booking Status" IN ('Incomplete','No Driver Found') THEN 1 ELSE 0 END) / COUNT(*), 2) as other_loss_rate
FROM sheet1
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-022/attempt-01/sql/S14.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-022/attempt-01/sql/S14.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-022/attempt-01/results/S14.rows.jsonl)；完整：True；SHA256：`42df1572c82c362674a199fe39f46d1ab9fe1a8b91a2f4041d5b9d2c860e55c0`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "sheet1", "kind": "base", "block": null, "base_tables": ["sheet1"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |
| B1 | COUNT(*) | [] | [] | True |
| B1 | COUNT(*) | [] | [] | True |
| B1 | COUNT(*) | [] | [] | True |
| B1 | SUM(CASE WHEN "Booking Status" = 'Completed' THEN 1 ELSE 0 END) | [] | [{"table": "sheet1", "column": "Booking Status"}] | False |
| B1 | SUM(CASE WHEN "Booking Status" = 'Cancelled by Driver' THEN 1 ELSE 0 END) | [] | [{"table": "sheet1", "column": "Booking Status"}] | False |
| B1 | SUM(CASE WHEN "Booking Status" = 'Cancelled by Customer' THEN 1 ELSE 0 END) | [] | [{"table": "sheet1", "column": "Booking Status"}] | False |
| B1 | SUM(CASE WHEN "Booking Status" IN ('Incomplete', 'No Driver Found') THEN 1 ELSE 0 END) | [] | [{"table": "sheet1", "column": "Booking Status"}] | False |


## S15

类别 `data`；来源 `query_db`；调用 `f7d45045a81a4bb886a4ed8670fcefd4`；状态 `success`。

```sql
SELECT CAST(SUBSTR("Time", 1, 2) AS INTEGER) as hour_of_day,
       COUNT(*) as ride_count,
       ROUND(AVG("Booking Value"), 2) as avg_booking_value,
       ROUND(AVG("Booking Value" / NULLIF("Ride Distance", 0)), 2) as avg_fare_per_km,
       ROUND(SUM("Booking Value"), 2) as total_earnings
FROM sheet1
WHERE "Booking Status" = 'Completed'
GROUP BY hour_of_day
ORDER BY hour_of_day
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-022/attempt-01/sql/S15.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-022/attempt-01/sql/S15.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-022/attempt-01/results/S15.rows.jsonl)；完整：True；SHA256：`011578875c3d7884995cebda4d2e14f87b751ffc35d4ff1c635148a7f2fe4fe3`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "sheet1", "kind": "base", "block": null, "base_tables": ["sheet1"]}] | [] | ["CAST(SUBSTRING(\"Time\", 1, 2) AS INTEGER)"] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |
| B1 | AVG("Booking Value") | [{"table": "sheet1", "column": "Booking Value"}] | [] | False |
| B1 | AVG("Booking Value" / NULLIF("Ride Distance", 0)) | [{"table": "sheet1", "column": "Booking Value"}, {"table": "sheet1", "column": "Ride Distance"}] | [] | False |
| B1 | SUM("Booking Value") | [{"table": "sheet1", "column": "Booking Value"}] | [] | False |


## S16

类别 `data`；来源 `query_db`；调用 `d5ef64d7e1504046b9c52cd139cf541a`；状态 `success`。

```sql
SELECT "Payment Method",
       COUNT(*) as ride_count,
       ROUND(AVG("Booking Value"), 2) as avg_booking_value,
       ROUND(AVG("Booking Value" / NULLIF("Ride Distance", 0)), 2) as avg_fare_per_km
FROM sheet1
WHERE "Booking Status" = 'Completed'
GROUP BY "Payment Method"
ORDER BY ride_count DESC
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-022/attempt-01/sql/S16.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-022/attempt-01/sql/S16.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-022/attempt-01/results/S16.rows.jsonl)；完整：True；SHA256：`1f5ab231133d0d5c0c91dcd838e71cfcd83e58a82351980a534286fd97248254`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "sheet1", "kind": "base", "block": null, "base_tables": ["sheet1"]}] | [] | ["\"Payment Method\""] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |
| B1 | AVG("Booking Value") | [{"table": "sheet1", "column": "Booking Value"}] | [] | False |
| B1 | AVG("Booking Value" / NULLIF("Ride Distance", 0)) | [{"table": "sheet1", "column": "Booking Value"}, {"table": "sheet1", "column": "Ride Distance"}] | [] | False |


## S17

类别 `data`；来源 `query_db`；调用 `ad2a7418ae7747ecaad58d474cddd0d7`；状态 `success`。

```sql
SELECT CAST(SUBSTR("Time", 1, 2) AS INTEGER) as hour_of_day,
       COUNT(*) as ride_count,
       ROUND(AVG("Booking Value"), 2) as avg_booking_value,
       ROUND(AVG("Booking Value" / NULLIF("Ride Distance", 0)), 2) as avg_fare_per_km,
       ROUND(SUM("Booking Value"), 2) as total_earnings
FROM sheet1
WHERE "Booking Status" = 'Completed' AND CAST(SUBSTR("Time", 1, 2) AS INTEGER) >= 12
GROUP BY hour_of_day
ORDER BY hour_of_day
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-022/attempt-01/sql/S17.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-022/attempt-01/sql/S17.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-022/attempt-01/results/S17.rows.jsonl)；完整：True；SHA256：`3bcd916a982274d6342e52e08944fa1dea71397972412823f1fb848cc768b807`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "sheet1", "kind": "base", "block": null, "base_tables": ["sheet1"]}] | [] | ["CAST(SUBSTRING(\"Time\", 1, 2) AS INTEGER)"] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |
| B1 | AVG("Booking Value") | [{"table": "sheet1", "column": "Booking Value"}] | [] | False |
| B1 | AVG("Booking Value" / NULLIF("Ride Distance", 0)) | [{"table": "sheet1", "column": "Booking Value"}, {"table": "sheet1", "column": "Ride Distance"}] | [] | False |
| B1 | SUM("Booking Value") | [{"table": "sheet1", "column": "Booking Value"}] | [] | False |


## S18

类别 `data`；来源 `query_db`；调用 `bb85f98aa65a414d94cb35ca3f1ba541`；状态 `success`。

```sql
SELECT CAST(STRFTIME('%w', "Date") AS INTEGER) as day_of_week,
       COUNT(*) as ride_count,
       ROUND(AVG("Booking Value"), 2) as avg_booking_value,
       ROUND(AVG("Booking Value" / NULLIF("Ride Distance", 0)), 2) as avg_fare_per_km,
       ROUND(SUM("Booking Value"), 2) as total_earnings
FROM sheet1
WHERE "Booking Status" = 'Completed'
GROUP BY day_of_week
ORDER BY day_of_week
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-022/attempt-01/sql/S18.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-022/attempt-01/sql/S18.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-022/attempt-01/results/S18.rows.jsonl)；完整：True；SHA256：`e3df4808d2e3a3e47a1de98f328e253e2891b2415e1498ebc4c5bfdd48e9c89e`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "sheet1", "kind": "base", "block": null, "base_tables": ["sheet1"]}] | [] | ["CAST(STRFTIME('%w', \"Date\") AS INTEGER)"] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |
| B1 | AVG("Booking Value") | [{"table": "sheet1", "column": "Booking Value"}] | [] | False |
| B1 | AVG("Booking Value" / NULLIF("Ride Distance", 0)) | [{"table": "sheet1", "column": "Booking Value"}, {"table": "sheet1", "column": "Ride Distance"}] | [] | False |
| B1 | SUM("Booking Value") | [{"table": "sheet1", "column": "Booking Value"}] | [] | False |


## S19

类别 `data`；来源 `query_db`；调用 `6b14e88a77f0489da499ae68a6123755`；状态 `success`。

```sql
SELECT CAST(STRFTIME('%m', "Date") AS INTEGER) as month,
       COUNT(*) as ride_count,
       ROUND(AVG("Booking Value"), 2) as avg_booking_value,
       ROUND(AVG("Booking Value" / NULLIF("Ride Distance", 0)), 2) as avg_fare_per_km,
       ROUND(SUM("Booking Value"), 2) as total_earnings
FROM sheet1
WHERE "Booking Status" = 'Completed'
GROUP BY month
ORDER BY month
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-022/attempt-01/sql/S19.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-022/attempt-01/sql/S19.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-022/attempt-01/results/S19.rows.jsonl)；完整：True；SHA256：`e3df4808d2e3a3e47a1de98f328e253e2891b2415e1498ebc4c5bfdd48e9c89e`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "sheet1", "kind": "base", "block": null, "base_tables": ["sheet1"]}] | [] | ["CAST(STRFTIME('%m', \"Date\") AS INTEGER)"] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |
| B1 | AVG("Booking Value") | [{"table": "sheet1", "column": "Booking Value"}] | [] | False |
| B1 | AVG("Booking Value" / NULLIF("Ride Distance", 0)) | [{"table": "sheet1", "column": "Booking Value"}, {"table": "sheet1", "column": "Ride Distance"}] | [] | False |
| B1 | SUM("Booking Value") | [{"table": "sheet1", "column": "Booking Value"}] | [] | False |


## S20

类别 `data`；来源 `query_db`；调用 `5d2f59646df9427ead81c60532d14bfb`；状态 `success`。

```sql
SELECT DISTINCT "Date" FROM sheet1 LIMIT 20
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-022/attempt-01/sql/S20.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-022/attempt-01/sql/S20.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-022/attempt-01/results/S20.rows.jsonl)；完整：True；SHA256：`597effec40c5aa7f4e46b1c52a0d8c697f042d3beed00a931d2b5f4c22daf260`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "sheet1", "kind": "base", "block": null, "base_tables": ["sheet1"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |


## S21

类别 `data`；来源 `query_db`；调用 `900449069aea4161a8e627d4c5330435`；状态 `failed`。

```sql
SELECT DISTINCT CAST(SUBSTR("Date", 6, INSTR("Date", '/', 6) - 6) AS INTEGER) as month
FROM sheet1
ORDER BY month
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-022/attempt-01/sql/S21.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-022/attempt-01/sql/S21.parameters.json)。

错误：`OperationalError('wrong number of arguments to function INSTR()')`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "sheet1", "kind": "base", "block": null, "base_tables": ["sheet1"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |


## S22

类别 `data`；来源 `query_db`；调用 `5ba40bc467d541d7ab1fe8737de7436d`；状态 `success`。

```sql
SELECT DISTINCT SUBSTR("Date", 6) as month_part FROM sheet1 LIMIT 20
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-022/attempt-01/sql/S22.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-022/attempt-01/sql/S22.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-022/attempt-01/results/S22.rows.jsonl)；完整：True；SHA256：`7a2d7ff6f35e348ddf7c94ac53c6745f8fbc298d6fbbc8bd3ac813169c98cf79`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "sheet1", "kind": "base", "block": null, "base_tables": ["sheet1"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |


## S23

类别 `data`；来源 `query_db`；调用 `57e06f270f384596806e54a1edda65f8`；状态 `success`。

```sql
SELECT DISTINCT CAST(SUBSTR("Date", 6, INSTR(SUBSTR("Date", 6), '/') - 1) AS INTEGER) as month
FROM sheet1
ORDER BY month
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-022/attempt-01/sql/S23.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-022/attempt-01/sql/S23.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-022/attempt-01/results/S23.rows.jsonl)；完整：True；SHA256：`5f4c57143c2a2d5e29e8bb123c44bcfde176cbd25eff96fe15368ecf52f0adc8`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "sheet1", "kind": "base", "block": null, "base_tables": ["sheet1"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |


## S24

类别 `data`；来源 `query_db`；调用 `a8acee641c7e48c9a6fc72dda5b02183`；状态 `success`。

```sql
SELECT CAST(SUBSTR("Date", 6, INSTR(SUBSTR("Date", 6), '/') - 1) AS INTEGER) as month,
       COUNT(*) as ride_count,
       ROUND(AVG("Booking Value"), 2) as avg_booking_value,
       ROUND(AVG("Booking Value" / NULLIF("Ride Distance", 0)), 2) as avg_fare_per_km,
       ROUND(SUM("Booking Value"), 2) as total_earnings
FROM sheet1
WHERE "Booking Status" = 'Completed'
GROUP BY month
ORDER BY month
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-022/attempt-01/sql/S24.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-022/attempt-01/sql/S24.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-022/attempt-01/results/S24.rows.jsonl)；完整：True；SHA256：`5aeba3de1e062ba85bdfc5637501e65744e16b001e28b96ba4936204a8deeaba`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "sheet1", "kind": "base", "block": null, "base_tables": ["sheet1"]}] | [] | ["CAST(SUBSTRING(\"Date\", 6, INSTR(SUBSTRING(\"Date\", 6), '/') - 1) AS INTEGER)"] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |
| B1 | AVG("Booking Value") | [{"table": "sheet1", "column": "Booking Value"}] | [] | False |
| B1 | AVG("Booking Value" / NULLIF("Ride Distance", 0)) | [{"table": "sheet1", "column": "Booking Value"}, {"table": "sheet1", "column": "Ride Distance"}] | [] | False |
| B1 | SUM("Booking Value") | [{"table": "sheet1", "column": "Booking Value"}] | [] | False |


## S25

类别 `data`；来源 `query_db`；调用 `11f46cb2befd4ae48c6e65475394224f`；状态 `failed`。

```sql
SELECT CAST(STRFTIME('%w', SUBSTR("Date", 1, 4) || '-' || 
       SUBSTR("Date", 6, INSTR(SUBSTR("Date", 6), '/') - 1) || '-' || 
       SUBSTR("Date", INSTR("Date", '/', 6) + 1)) AS INTEGER) as day_of_week,
       COUNT(*) as ride_count,
       ROUND(SUM("Booking Value"), 2) as total_earnings
FROM sheet1
WHERE "Booking Status" = 'Completed'
GROUP BY day_of_week
ORDER BY day_of_week
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-022/attempt-01/sql/S25.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-022/attempt-01/sql/S25.parameters.json)。

错误：`OperationalError('wrong number of arguments to function INSTR()')`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "sheet1", "kind": "base", "block": null, "base_tables": ["sheet1"]}] | [] | ["CAST(STRFTIME('%w', SUBSTRING(\"Date\", 1, 4) \|\| '-' \|\| SUBSTRING(\"Date\", 6, INSTR(SUBSTRING(\"Date\", 6), '/') - 1) \|\| '-' \|\| SUBSTRING(\"Date\", IIF(INSTR(SUBSTRING(\"Date\", 6), '/') = 0, 0, INSTR(SUBSTRING(\"Date\", 6), '/') + 6 - 1) + 1)) AS INTEGER)"] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |
| B1 | SUM("Booking Value") | [{"table": "sheet1", "column": "Booking Value"}] | [] | False |


## S26

类别 `data`；来源 `query_db`；调用 `90b8e47aabea4a5e8d99b1c7b5c7fc94`；状态 `failed`。

```sql
SELECT 
       CAST(SUBSTR("Date", 1, 4) AS TEXT) || '-' || 
       CAST(SUBSTR("Date", 6, INSTR(SUBSTR("Date", 6), '/') - 1) AS TEXT) || '-' || 
       CAST(SUBSTR("Date", INSTR("Date", '/', 6) + 1) AS TEXT) as formatted_date
FROM sheet1 LIMIT 5
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-022/attempt-01/sql/S26.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-022/attempt-01/sql/S26.parameters.json)。

错误：`OperationalError('wrong number of arguments to function INSTR()')`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "sheet1", "kind": "base", "block": null, "base_tables": ["sheet1"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |


## S27

类别 `data`；来源 `query_db`；调用 `72b862591e384edfb865da938ed1b3df`；状态 `success`。

```sql
SELECT 
       SUBSTR("Date", 1, 4) || '-' || 
       SUBSTR("Date", 6, INSTR(SUBSTR("Date", 6), '/') - 1) || '-' || 
       SUBSTR("Date", INSTR(SUBSTR("Date", 6), '/') + 6) as formatted_date
FROM sheet1 LIMIT 5
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-022/attempt-01/sql/S27.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-022/attempt-01/sql/S27.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-022/attempt-01/results/S27.rows.jsonl)；完整：True；SHA256：`13d57a01a9e8256de90143050c54158cb9199025d2335a7a1367f45fb2574d5a`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "sheet1", "kind": "base", "block": null, "base_tables": ["sheet1"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |


## S28

类别 `data`；来源 `query_db`；调用 `1ad9fcff5a944f51a8eff12480f76027`；状态 `success`。

```sql
SELECT DISTINCT STRFTIME('%w', SUBSTR("Date", 1, 4) || '-' || 
       SUBSTR("Date", 6, INSTR(SUBSTR("Date", 6), '/') - 1) || '-' || 
       SUBSTR("Date", INSTR(SUBSTR("Date", 6), '/') + 6)) as dow
FROM sheet1
ORDER BY dow
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-022/attempt-01/sql/S28.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-022/attempt-01/sql/S28.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-022/attempt-01/results/S28.rows.jsonl)；完整：True；SHA256：`9acdc91fc84c8be75fdda2bcb904d837a9c2842b4fe13bb79773039efeaab083`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "sheet1", "kind": "base", "block": null, "base_tables": ["sheet1"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |


## S29

类别 `data`；来源 `query_db`；调用 `5c97d30e022f439d9a4bdc529fa58d8f`；状态 `success`。

```sql
SELECT STRFTIME('%w', SUBSTR("Date", 1, 4) || '-' || 
       SUBSTR("Date", 6, INSTR(SUBSTR("Date", 6), '/') - 1) || '-' || 
       SUBSTR("Date", INSTR(SUBSTR("Date", 6), '/') + 6)) as day_of_week,
       COUNT(*) as ride_count,
       ROUND(AVG("Booking Value"), 2) as avg_booking_value,
       ROUND(AVG("Booking Value" / NULLIF("Ride Distance", 0)), 2) as avg_fare_per_km,
       ROUND(SUM("Booking Value"), 2) as total_earnings
FROM sheet1
WHERE "Booking Status" = 'Completed' AND 
      STRFTIME('%w', SUBSTR("Date", 1, 4) || '-' || 
       SUBSTR("Date", 6, INSTR(SUBSTR("Date", 6), '/') - 1) || '-' || 
       SUBSTR("Date", INSTR(SUBSTR("Date", 6), '/') + 6)) IS NOT NULL
GROUP BY day_of_week
ORDER BY day_of_week
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-022/attempt-01/sql/S29.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-022/attempt-01/sql/S29.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-022/attempt-01/results/S29.rows.jsonl)；完整：True；SHA256：`116e9ba68dcd221130806d12e533dd8f1e11a6527ff68462ceb842b6f7cc566d`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "sheet1", "kind": "base", "block": null, "base_tables": ["sheet1"]}] | [] | ["STRFTIME('%w', SUBSTRING(\"Date\", 1, 4) \|\| '-' \|\| SUBSTRING(\"Date\", 6, INSTR(SUBSTRING(\"Date\", 6), '/') - 1) \|\| '-' \|\| SUBSTRING(\"Date\", INSTR(SUBSTRING(\"Date\", 6), '/') + 6))"] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |
| B1 | AVG("Booking Value") | [{"table": "sheet1", "column": "Booking Value"}] | [] | False |
| B1 | AVG("Booking Value" / NULLIF("Ride Distance", 0)) | [{"table": "sheet1", "column": "Booking Value"}, {"table": "sheet1", "column": "Ride Distance"}] | [] | False |
| B1 | SUM("Booking Value") | [{"table": "sheet1", "column": "Booking Value"}] | [] | False |


## S30

类别 `data`；来源 `query_db`；调用 `396247a3903d43898e48ecb2b67c64fc`；状态 `success`。

```sql
SELECT 
       CASE WHEN STRFTIME('%w', SUBSTR("Date", 1, 4) || '-' || 
            SUBSTR("Date", 6, INSTR(SUBSTR("Date", 6), '/') - 1) || '-' || 
            SUBSTR("Date", INSTR(SUBSTR("Date", 6), '/') + 6)) IS NULL THEN 'unparsed' ELSE 'parsed' END as parse_status,
       COUNT(*) as cnt
FROM sheet1
WHERE "Booking Status" = 'Completed'
GROUP BY parse_status
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-022/attempt-01/sql/S30.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-022/attempt-01/sql/S30.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-022/attempt-01/results/S30.rows.jsonl)；完整：True；SHA256：`ca428e2debae686c1d2bf9be8f5d4de0dc1e2901e2236bbc8f8bba8a1eb600dc`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "sheet1", "kind": "base", "block": null, "base_tables": ["sheet1"]}] | [] | ["CASE WHEN STRFTIME('%w', SUBSTRING(\"Date\", 1, 4) \|\| '-' \|\| SUBSTRING(\"Date\", 6, INSTR(SUBSTRING(\"Date\", 6), '/') - 1) \|\| '-' \|\| SUBSTRING(\"Date\", INSTR(SUBSTRING(\"Date\", 6), '/') + 6)) IS NULL THEN 'unparsed' ELSE 'parsed' END"] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |


## S31

类别 `data`；来源 `query_db`；调用 `9c407ad75ec14db7bcabb0f210dce789`；状态 `success`。

```sql
SELECT "Date", COUNT(*) as cnt
FROM sheet1
WHERE "Booking Status" = 'Completed'
  AND STRFTIME('%w', SUBSTR("Date", 1, 4) || '-' || 
       SUBSTR("Date", 6, INSTR(SUBSTR("Date", 6), '/') - 1) || '-' || 
       SUBSTR("Date", INSTR(SUBSTR("Date", 6), '/') + 6)) IS NULL
GROUP BY "Date"
LIMIT 20
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-022/attempt-01/sql/S31.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-022/attempt-01/sql/S31.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-022/attempt-01/results/S31.rows.jsonl)；完整：True；SHA256：`c60531f238c5c9cc70279ae0d874684a4d2fe932d77466b5f61b29056ed5f91c`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "sheet1", "kind": "base", "block": null, "base_tables": ["sheet1"]}] | [] | ["\"Date\""] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |


## S32

类别 `data`；来源 `query_db`；调用 `befb4920aae748368d721dcfcb2d7cbb`；状态 `success`。

```sql
SELECT "Date",
       SUBSTR("Date", 1, 4) || '-' || 
       SUBSTR("Date", 6, INSTR(SUBSTR("Date", 6), '/') - 1) || '-' || 
       SUBSTR("Date", INSTR(SUBSTR("Date", 6), '/') + 6) as formatted
FROM sheet1
WHERE "Booking Status" = 'Completed' AND "Date" = '2024/1/1'
LIMIT 1
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-022/attempt-01/sql/S32.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-022/attempt-01/sql/S32.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-022/attempt-01/results/S32.rows.jsonl)；完整：True；SHA256：`a654808d310375d125b87dbee5e22ad47642db8657929656b23b86ab18b4e6ac`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "sheet1", "kind": "base", "block": null, "base_tables": ["sheet1"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |


## S33

类别 `data`；来源 `query_db`；调用 `dca56d573cbd448082110ea3274c8ca5`；状态 `success`。

```sql
SELECT STRFTIME('%w', '2024-1-1') as test1, STRFTIME('%w', '2024-03-23') as test2, STRFTIME('%w', '2024-3-23') as test3
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-022/attempt-01/sql/S33.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-022/attempt-01/sql/S33.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-022/attempt-01/results/S33.rows.jsonl)；完整：True；SHA256：`442f530eaf21dab0f277608ba9e740abaa97a65d4ed383c6b20faf8433b987ff`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |


## S34

类别 `data`；来源 `query_db`；调用 `bcb40c2ea56a4d729b8c4a1aba2dd9f4`；状态 `success`。

```sql
SELECT STRFTIME('%w', SUBSTR("Date", 1, 4) || '-' || 
       PRINTF('%02d', CAST(SUBSTR("Date", 6, INSTR(SUBSTR("Date", 6), '/') - 1) AS INTEGER)) || '-' || 
       PRINTF('%02d', CAST(SUBSTR("Date", INSTR(SUBSTR("Date", 6), '/') + 6) AS INTEGER))) as dow
FROM sheet1
WHERE "Booking Status" = 'Completed' AND "Date" = '2024/1/1'
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-022/attempt-01/sql/S34.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-022/attempt-01/sql/S34.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-022/attempt-01/results/S34.rows.jsonl)；完整：True；SHA256：`6e6350921f3e37b5abff1a9b1b8a59e593d88e42e5502f5e693dfdff39b0db02`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "sheet1", "kind": "base", "block": null, "base_tables": ["sheet1"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |


## S35

类别 `data`；来源 `query_db`；调用 `7d62fa73b8e048f68deb836640b1dab6`；状态 `success`。

```sql
SELECT STRFTIME('%w', SUBSTR("Date", 1, 4) || '-' || 
       PRINTF('%02d', CAST(SUBSTR("Date", 6, INSTR(SUBSTR("Date", 6), '/') - 1) AS INTEGER)) || '-' || 
       PRINTF('%02d', CAST(SUBSTR("Date", INSTR(SUBSTR("Date", 6), '/') + 6) AS INTEGER))) as day_of_week,
       COUNT(*) as ride_count,
       ROUND(AVG("Booking Value"), 2) as avg_booking_value,
       ROUND(AVG("Booking Value" / NULLIF("Ride Distance", 0)), 2) as avg_fare_per_km,
       ROUND(SUM("Booking Value"), 2) as total_earnings
FROM sheet1
WHERE "Booking Status" = 'Completed'
GROUP BY day_of_week
ORDER BY day_of_week
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-022/attempt-01/sql/S35.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-022/attempt-01/sql/S35.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-022/attempt-01/results/S35.rows.jsonl)；完整：True；SHA256：`8955f04e62e3b9622e6fbfeb63b7198dd4ca67ac3fc5f0f4594cdc2a61336746`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "sheet1", "kind": "base", "block": null, "base_tables": ["sheet1"]}] | [] | ["STRFTIME('%w', SUBSTRING(\"Date\", 1, 4) \|\| '-' \|\| PRINTF('%02d', CAST(SUBSTRING(\"Date\", 6, INSTR(SUBSTRING(\"Date\", 6), '/') - 1) AS INTEGER)) \|\| '-' \|\| PRINTF('%02d', CAST(SUBSTRING(\"Date\", INSTR(SUBSTRING(\"Date\", 6), '/') + 6) AS INTEGER)))"] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |
| B1 | AVG("Booking Value") | [{"table": "sheet1", "column": "Booking Value"}] | [] | False |
| B1 | AVG("Booking Value" / NULLIF("Ride Distance", 0)) | [{"table": "sheet1", "column": "Booking Value"}, {"table": "sheet1", "column": "Ride Distance"}] | [] | False |
| B1 | SUM("Booking Value") | [{"table": "sheet1", "column": "Booking Value"}] | [] | False |


## S36

类别 `data`；来源 `query_db`；调用 `f9f722bd1f5e4292b1ec6d09e4959de9`；状态 `success`。

```sql
SELECT 
  CASE WHEN "Ride Distance" <= 5 THEN '0-5 km'
       WHEN "Ride Distance" <= 10 THEN '5-10 km'
       WHEN "Ride Distance" <= 15 THEN '10-15 km'
       WHEN "Ride Distance" <= 20 THEN '15-20 km'
       WHEN "Ride Distance" <= 25 THEN '20-25 km'
       WHEN "Ride Distance" <= 30 THEN '25-30 km'
       WHEN "Ride Distance" <= 40 THEN '30-40 km'
       ELSE '40+ km' END as distance_band,
       COUNT(*) as ride_count,
       ROUND(AVG("Booking Value"), 2) as avg_booking_value,
       ROUND(AVG("Booking Value" / NULLIF("Ride Distance", 0)), 2) as avg_fare_per_km
FROM sheet1
WHERE "Booking Status" = 'Completed'
GROUP BY distance_band
ORDER BY MIN("Ride Distance")
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-022/attempt-01/sql/S36.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-022/attempt-01/sql/S36.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-022/attempt-01/results/S36.rows.jsonl)；完整：True；SHA256：`e22225b3642bcbf3ba0f17aae9587a1ac76ebfa1cfccd8a6b134b4256d4c9829`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "sheet1", "kind": "base", "block": null, "base_tables": ["sheet1"]}] | [] | ["CASE WHEN \"Ride Distance\" <= 5 THEN '0-5 km' WHEN \"Ride Distance\" <= 10 THEN '5-10 km' WHEN \"Ride Distance\" <= 15 THEN '10-15 km' WHEN \"Ride Distance\" <= 20 THEN '15-20 km' WHEN \"Ride Distance\" <= 25 THEN '20-25 km' WHEN \"Ride Distance\" <= 30 THEN '25-30 km' WHEN \"Ride Distance\" <= 40 THEN '30-40 km' ELSE '40+ km' END"] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |
| B1 | AVG("Booking Value") | [{"table": "sheet1", "column": "Booking Value"}] | [] | False |
| B1 | AVG("Booking Value" / NULLIF("Ride Distance", 0)) | [{"table": "sheet1", "column": "Booking Value"}, {"table": "sheet1", "column": "Ride Distance"}] | [] | False |
| B1 | MIN("Ride Distance") | [{"table": "sheet1", "column": "Ride Distance"}] | [] | False |


## S37

类别 `data`；来源 `query_db`；调用 `c20a5cc6c86a4eb491e8f9fe2a247e86`；状态 `success`。

```sql
SELECT "Vehicle Type",
       ROUND(AVG("Booking Value" / NULLIF("Ride Distance", 0)), 2) as fare_per_km_weekday,
       ROUND(SUM("Booking Value"), 2) as earnings_weekday
FROM sheet1
WHERE "Booking Status" = 'Completed' AND 
  STRFTIME('%w', SUBSTR("Date", 1, 4) || '-' || 
       PRINTF('%02d', CAST(SUBSTR("Date", 6, INSTR(SUBSTR("Date", 6), '/') - 1) AS INTEGER)) || '-' || 
       PRINTF('%02d', CAST(SUBSTR("Date", INSTR(SUBSTR("Date", 6), '/') + 6) AS INTEGER))) NOT IN ('0','6')
GROUP BY "Vehicle Type"
ORDER BY fare_per_km_weekday DESC
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-022/attempt-01/sql/S37.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-022/attempt-01/sql/S37.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-022/attempt-01/results/S37.rows.jsonl)；完整：True；SHA256：`c0577190b2cd10f5d10209253eb0ae4daf446c91f642cbb112dcb40b61a46ea3`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "sheet1", "kind": "base", "block": null, "base_tables": ["sheet1"]}] | [] | ["\"Vehicle Type\""] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | AVG("Booking Value" / NULLIF("Ride Distance", 0)) | [{"table": "sheet1", "column": "Booking Value"}, {"table": "sheet1", "column": "Ride Distance"}] | [] | False |
| B1 | SUM("Booking Value") | [{"table": "sheet1", "column": "Booking Value"}] | [] | False |


## S38

类别 `data`；来源 `query_db`；调用 `d11f33c3332146288f196d285453809d`；状态 `failed`。

```sql
SELECT CORR("Booking Value", "Ride Distance") as corr_value_distance
FROM sheet1 WHERE "Booking Status" = 'Completed'
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-022/attempt-01/sql/S38.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-022/attempt-01/sql/S38.parameters.json)。

错误：`OperationalError('no such function: CORR')`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "sheet1", "kind": "base", "block": null, "base_tables": ["sheet1"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | CORR("Booking Value", "Ride Distance") | [{"table": "sheet1", "column": "Booking Value"}, {"table": "sheet1", "column": "Ride Distance"}] | [] | False |


## S39

类别 `data`；来源 `query_db`；调用 `c17d3d13e7d844d0bdd0f325048a42c2`；状态 `success`。

```sql
SELECT ROUND(AVG("Booking Value"),2) as avg_bv, ROUND(AVG("Ride Distance"),2) as avg_dist
FROM sheet1 WHERE "Booking Status" = 'Completed' AND "Ride Distance" <= 5
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-022/attempt-01/sql/S39.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-022/attempt-01/sql/S39.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-022/attempt-01/results/S39.rows.jsonl)；完整：True；SHA256：`da898d8e0480f4080108ee9b7db76af7da2f8b79449dd7bd7f0a37983d8f2a34`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "sheet1", "kind": "base", "block": null, "base_tables": ["sheet1"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | AVG("Booking Value") | [{"table": "sheet1", "column": "Booking Value"}] | [] | False |
| B1 | AVG("Ride Distance") | [{"table": "sheet1", "column": "Ride Distance"}] | [] | False |


## S40

类别 `data`；来源 `query_db`；调用 `16a11c69d6ee46439cf49f065f5df824`；状态 `success`。

```sql
SELECT ROUND(AVG("Booking Value"),2) as avg_bv, ROUND(AVG("Ride Distance"),2) as avg_dist
FROM sheet1 WHERE "Booking Status" = 'Completed' AND "Ride Distance" > 40
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-022/attempt-01/sql/S40.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-022/attempt-01/sql/S40.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-022/attempt-01/results/S40.rows.jsonl)；完整：True；SHA256：`375e77bd6a6ea6dbd23e8073c682448a8d924e055ca68ce640689b823fcd4a7e`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "sheet1", "kind": "base", "block": null, "base_tables": ["sheet1"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | AVG("Booking Value") | [{"table": "sheet1", "column": "Booking Value"}] | [] | False |
| B1 | AVG("Ride Distance") | [{"table": "sheet1", "column": "Ride Distance"}] | [] | False |


## S41

类别 `data`；来源 `query_db`；调用 `3724221e94e94e838127b3f500ded6ac`；状态 `success`。

```sql
SELECT 
  CASE WHEN "Driver Ratings" < 3.5 THEN '3.0-3.4'
       WHEN "Driver Ratings" < 4.0 THEN '3.5-3.9'
       WHEN "Driver Ratings" < 4.5 THEN '4.0-4.4'
       ELSE '4.5-5.0' END as rating_band,
       COUNT(*) as total_bookings,
       ROUND(100.0*SUM(CASE WHEN "Booking Status" = 'Completed' THEN 1 ELSE 0 END)/COUNT(*),1) as completion_rate,
       ROUND(100.0*SUM(CASE WHEN "Booking Status" = 'Cancelled by Driver' THEN 1 ELSE 0 END)/COUNT(*),1) as driver_cancel_rate,
       ROUND(100.0*SUM(CASE WHEN "Booking Status" = 'Cancelled by Customer' THEN 1 ELSE 0 END)/COUNT(*),1) as cust_cancel_rate,
       ROUND(100.0*SUM(CASE WHEN "Booking Status" = 'No Driver Found' THEN 1 ELSE 0 END)/COUNT(*),1) as no_driver_rate,
       ROUND(100.0*SUM(CASE WHEN "Booking Status" = 'Incomplete' THEN 1 ELSE 0 END)/COUNT(*),1) as incomplete_rate,
       ROUND(AVG("Booking Value"),2) as avg_booking_value
FROM sheet1
WHERE "Driver Ratings" IS NOT NULL
GROUP BY rating_band
ORDER BY MIN("Driver Ratings")
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-022/attempt-01/sql/S41.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-022/attempt-01/sql/S41.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-022/attempt-01/results/S41.rows.jsonl)；完整：True；SHA256：`204179c434dd911b3ffae2f66a903a6d03bbd405e21a0c28037de0d1dae0b6bc`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "sheet1", "kind": "base", "block": null, "base_tables": ["sheet1"]}] | [] | ["CASE WHEN \"Driver Ratings\" < 3.5 THEN '3.0-3.4' WHEN \"Driver Ratings\" < 4.0 THEN '3.5-3.9' WHEN \"Driver Ratings\" < 4.5 THEN '4.0-4.4' ELSE '4.5-5.0' END"] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |
| B1 | AVG("Booking Value") | [{"table": "sheet1", "column": "Booking Value"}] | [] | False |
| B1 | MIN("Driver Ratings") | [{"table": "sheet1", "column": "Driver Ratings"}] | [] | False |
| B1 | COUNT(*) | [] | [] | True |
| B1 | COUNT(*) | [] | [] | True |
| B1 | COUNT(*) | [] | [] | True |
| B1 | COUNT(*) | [] | [] | True |
| B1 | COUNT(*) | [] | [] | True |
| B1 | SUM(CASE WHEN "Booking Status" = 'Completed' THEN 1 ELSE 0 END) | [] | [{"table": "sheet1", "column": "Booking Status"}] | False |
| B1 | SUM(CASE WHEN "Booking Status" = 'Cancelled by Driver' THEN 1 ELSE 0 END) | [] | [{"table": "sheet1", "column": "Booking Status"}] | False |
| B1 | SUM(CASE WHEN "Booking Status" = 'Cancelled by Customer' THEN 1 ELSE 0 END) | [] | [{"table": "sheet1", "column": "Booking Status"}] | False |
| B1 | SUM(CASE WHEN "Booking Status" = 'No Driver Found' THEN 1 ELSE 0 END) | [] | [{"table": "sheet1", "column": "Booking Status"}] | False |
| B1 | SUM(CASE WHEN "Booking Status" = 'Incomplete' THEN 1 ELSE 0 END) | [] | [{"table": "sheet1", "column": "Booking Status"}] | False |


## S42

类别 `data`；来源 `query_db`；调用 `91eddcb48c354fe29483460bd40bac29`；状态 `success`。

```sql
SELECT 
  CASE WHEN "Driver Ratings" < 3.5 THEN '3.0-3.4'
       WHEN "Driver Ratings" < 4.0 THEN '3.5-3.9'
       WHEN "Driver Ratings" < 4.5 THEN '4.0-4.4'
       ELSE '4.5-5.0' END as rating_band,
       COUNT(*) as rides,
       ROUND(SUM("Booking Value"),2) as total_earnings
FROM sheet1
WHERE "Booking Status" = 'Completed'
GROUP BY rating_band
ORDER BY MIN("Driver Ratings")
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-022/attempt-01/sql/S42.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-022/attempt-01/sql/S42.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-022/attempt-01/results/S42.rows.jsonl)；完整：True；SHA256：`13aedb2061ba9bf3be80d272f54220f56a64ae234fe4638977c5af4db6ebd575`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "sheet1", "kind": "base", "block": null, "base_tables": ["sheet1"]}] | [] | ["CASE WHEN \"Driver Ratings\" < 3.5 THEN '3.0-3.4' WHEN \"Driver Ratings\" < 4.0 THEN '3.5-3.9' WHEN \"Driver Ratings\" < 4.5 THEN '4.0-4.4' ELSE '4.5-5.0' END"] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |
| B1 | SUM("Booking Value") | [{"table": "sheet1", "column": "Booking Value"}] | [] | False |
| B1 | MIN("Driver Ratings") | [{"table": "sheet1", "column": "Driver Ratings"}] | [] | False |


## S43

类别 `data`；来源 `query_db`；调用 `b07a172fb6e8461ebeda674520e5df26`；状态 `success`。

```sql
SELECT "Pickup Location",
       COUNT(*) as ride_count,
       ROUND(AVG("Booking Value" / NULLIF("Ride Distance", 0)), 2) as avg_fare_per_km,
       ROUND(SUM("Booking Value"), 2) as total_earnings
FROM sheet1
WHERE "Booking Status" = 'Completed'
GROUP BY "Pickup Location"
ORDER BY ride_count DESC
LIMIT 20
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-022/attempt-01/sql/S43.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-022/attempt-01/sql/S43.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-022/attempt-01/results/S43.rows.jsonl)；完整：True；SHA256：`6b77b5eda0811e0e552e77872824022993e3e6187b0b75a1f940882dcfdff812`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "sheet1", "kind": "base", "block": null, "base_tables": ["sheet1"]}] | [] | ["\"Pickup Location\""] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |
| B1 | AVG("Booking Value" / NULLIF("Ride Distance", 0)) | [{"table": "sheet1", "column": "Booking Value"}, {"table": "sheet1", "column": "Ride Distance"}] | [] | False |
| B1 | SUM("Booking Value") | [{"table": "sheet1", "column": "Booking Value"}] | [] | False |


## S44

类别 `data`；来源 `query_db`；调用 `75364a862b0b4f76a718bd0c4a7e8629`；状态 `success`。

```sql
SELECT "Vehicle Type",
       COUNT(*) as completed_rides,
       ROUND(SUM("Booking Value"), 2) as total_earnings,
       ROUND(AVG("Booking Value"), 2) as avg_per_ride,
       ROUND(AVG("Ride Distance"), 2) as avg_distance,
       ROUND(AVG("Booking Value" / NULLIF("Ride Distance", 0)), 2) as avg_fare_per_km,
       ROUND(100.0 * COUNT(*) / SUM(COUNT(*)) OVER (), 2) as pct_of_completed_rides
FROM sheet1
WHERE "Booking Status" = 'Completed'
GROUP BY "Vehicle Type"
ORDER BY avg_fare_per_km DESC
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-022/attempt-01/sql/S44.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-022/attempt-01/sql/S44.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-022/attempt-01/results/S44.rows.jsonl)；完整：True；SHA256：`0a3d32aefb227164ec225db0e39b93e79594da9366113777169b936f83be6f49`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "sheet1", "kind": "base", "block": null, "base_tables": ["sheet1"]}] | [] | ["\"Vehicle Type\""] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |
| B1 | SUM("Booking Value") | [{"table": "sheet1", "column": "Booking Value"}] | [] | False |
| B1 | AVG("Booking Value") | [{"table": "sheet1", "column": "Booking Value"}] | [] | False |
| B1 | AVG("Ride Distance") | [{"table": "sheet1", "column": "Ride Distance"}] | [] | False |
| B1 | AVG("Booking Value" / NULLIF("Ride Distance", 0)) | [{"table": "sheet1", "column": "Booking Value"}, {"table": "sheet1", "column": "Ride Distance"}] | [] | False |
| B1 | COUNT(*) | [] | [] | True |
| B1 | COUNT(*) | [] | [] | True |


## S45

类别 `data`；来源 `query_db`；调用 `a4ba9037dc914b2ab8d1aebf17c49d15`；状态 `success`。

```sql
SELECT 
  CASE WHEN "Voice Talk Average Time" < 5 THEN '0-5 min'
       WHEN "Voice Talk Average Time" < 10 THEN '5-10 min'
       WHEN "Voice Talk Average Time" < 15 THEN '10-15 min'
       ELSE '15+ min' END as voice_band,
       COUNT(*) as rides,
       ROUND(AVG("Booking Value"),2) as avg_booking,
       ROUND(AVG("Booking Value"/NULLIF("Ride Distance",0)),2) as avg_fare_per_km,
       ROUND(AVG("Driver Ratings"),2) as avg_driver_rating
FROM sheet1
WHERE "Booking Status" = 'Completed'
GROUP BY voice_band
ORDER BY MIN("Voice Talk Average Time")
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-022/attempt-01/sql/S45.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-022/attempt-01/sql/S45.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-022/attempt-01/results/S45.rows.jsonl)；完整：True；SHA256：`e6c19b87889c797fbab4dd92d8697a3ebd163cf9825907f0db0c423075d44697`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "sheet1", "kind": "base", "block": null, "base_tables": ["sheet1"]}] | [] | ["CASE WHEN \"Voice Talk Average Time\" < 5 THEN '0-5 min' WHEN \"Voice Talk Average Time\" < 10 THEN '5-10 min' WHEN \"Voice Talk Average Time\" < 15 THEN '10-15 min' ELSE '15+ min' END"] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |
| B1 | AVG("Booking Value") | [{"table": "sheet1", "column": "Booking Value"}] | [] | False |
| B1 | AVG("Booking Value" / NULLIF("Ride Distance", 0)) | [{"table": "sheet1", "column": "Booking Value"}, {"table": "sheet1", "column": "Ride Distance"}] | [] | False |
| B1 | AVG("Driver Ratings") | [{"table": "sheet1", "column": "Driver Ratings"}] | [] | False |
| B1 | MIN("Voice Talk Average Time") | [{"table": "sheet1", "column": "Voice Talk Average Time"}] | [] | False |


## S46

类别 `data`；来源 `query_db`；调用 `4aab73d4c94d48e4a20abe106667f2a0`；状态 `success`。

```sql
SELECT 
  CASE WHEN "Customer Technical Assistance Time" < 5 THEN '0-5 min'
       WHEN "Customer Technical Assistance Time" < 10 THEN '5-10 min'
       WHEN "Customer Technical Assistance Time" < 15 THEN '10-15 min'
       ELSE '15+ min' END as assist_band,
       COUNT(*) as rides,
       ROUND(AVG("Booking Value"),2) as avg_booking,
       ROUND(AVG("Booking Value"/NULLIF("Ride Distance",0)),2) as avg_fare_per_km,
       ROUND(AVG("Driver Ratings"),2) as avg_driver_rating
FROM sheet1
WHERE "Booking Status" = 'Completed'
GROUP BY assist_band
ORDER BY MIN("Customer Technical Assistance Time")
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-022/attempt-01/sql/S46.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-022/attempt-01/sql/S46.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-022/attempt-01/results/S46.rows.jsonl)；完整：True；SHA256：`b9358c0be4cfa377a9619b293eb4fc830a5e48a4eb2116bc75a540f90b1d5041`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "sheet1", "kind": "base", "block": null, "base_tables": ["sheet1"]}] | [] | ["CASE WHEN \"Customer Technical Assistance Time\" < 5 THEN '0-5 min' WHEN \"Customer Technical Assistance Time\" < 10 THEN '5-10 min' WHEN \"Customer Technical Assistance Time\" < 15 THEN '10-15 min' ELSE '15+ min' END"] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |
| B1 | AVG("Booking Value") | [{"table": "sheet1", "column": "Booking Value"}] | [] | False |
| B1 | AVG("Booking Value" / NULLIF("Ride Distance", 0)) | [{"table": "sheet1", "column": "Booking Value"}, {"table": "sheet1", "column": "Ride Distance"}] | [] | False |
| B1 | AVG("Driver Ratings") | [{"table": "sheet1", "column": "Driver Ratings"}] | [] | False |
| B1 | MIN("Customer Technical Assistance Time") | [{"table": "sheet1", "column": "Customer Technical Assistance Time"}] | [] | False |


## S47

类别 `data`；来源 `query_db`；调用 `d19e1c70235a404b944c60ec35db9691`；状态 `success`。

```sql
SELECT MIN("Customer Technical Assistance Time") as min_ctat,
       MAX("Customer Technical Assistance Time") as max_ctat,
       ROUND(AVG("Customer Technical Assistance Time"),2) as avg_ctat
FROM sheet1 WHERE "Booking Status" = 'Completed'
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-022/attempt-01/sql/S47.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-022/attempt-01/sql/S47.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-022/attempt-01/results/S47.rows.jsonl)；完整：True；SHA256：`2abb9787aa71c494ef8ec9168c561d6d9d1e86b1e2aee3bead88e0e54d20b850`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "sheet1", "kind": "base", "block": null, "base_tables": ["sheet1"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | MIN("Customer Technical Assistance Time") | [{"table": "sheet1", "column": "Customer Technical Assistance Time"}] | [] | False |
| B1 | MAX("Customer Technical Assistance Time") | [{"table": "sheet1", "column": "Customer Technical Assistance Time"}] | [] | False |
| B1 | AVG("Customer Technical Assistance Time") | [{"table": "sheet1", "column": "Customer Technical Assistance Time"}] | [] | False |


## S48

类别 `data`；来源 `query_db`；调用 `7a987e4a7363487c956cddd7e8e8667a`；状态 `success`。

```sql
SELECT DISTINCT "Customer Technical Assistance Time"
FROM sheet1 WHERE "Booking Status" = 'Completed'
ORDER BY "Customer Technical Assistance Time"
LIMIT 20
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-022/attempt-01/sql/S48.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-022/attempt-01/sql/S48.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-022/attempt-01/results/S48.rows.jsonl)；完整：True；SHA256：`332447a25d1902abcc43d0823c93ee5e41a06ee5aa5175f7b96e9d40c50ecf96`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "sheet1", "kind": "base", "block": null, "base_tables": ["sheet1"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |


## S49

类别 `data`；来源 `query_db`；调用 `ef39747c46e543048d601ebd3d76bd88`；状态 `success`。

```sql
SELECT 
  CASE WHEN "Customer Technical Assistance Time" < 20 THEN '15-20 min'
       WHEN "Customer Technical Assistance Time" < 25 THEN '20-25 min'
       WHEN "Customer Technical Assistance Time" < 30 THEN '25-30 min'
       WHEN "Customer Technical Assistance Time" < 35 THEN '30-35 min'
       ELSE '35+ min' END as assist_band,
       COUNT(*) as rides,
       ROUND(AVG("Booking Value"),2) as avg_booking,
       ROUND(AVG("Booking Value"/NULLIF("Ride Distance",0)),2) as avg_fare_per_km,
       ROUND(AVG("Driver Ratings"),2) as avg_driver_rating
FROM sheet1
WHERE "Booking Status" = 'Completed'
GROUP BY assist_band
ORDER BY MIN("Customer Technical Assistance Time")
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-022/attempt-01/sql/S49.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-022/attempt-01/sql/S49.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-022/attempt-01/results/S49.rows.jsonl)；完整：True；SHA256：`906da88147a0b9cd72185b029bf7c1fdccd811868bb6ba142f5cf444d0ed0c8f`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "sheet1", "kind": "base", "block": null, "base_tables": ["sheet1"]}] | [] | ["CASE WHEN \"Customer Technical Assistance Time\" < 20 THEN '15-20 min' WHEN \"Customer Technical Assistance Time\" < 25 THEN '20-25 min' WHEN \"Customer Technical Assistance Time\" < 30 THEN '25-30 min' WHEN \"Customer Technical Assistance Time\" < 35 THEN '30-35 min' ELSE '35+ min' END"] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |
| B1 | AVG("Booking Value") | [{"table": "sheet1", "column": "Booking Value"}] | [] | False |
| B1 | AVG("Booking Value" / NULLIF("Ride Distance", 0)) | [{"table": "sheet1", "column": "Booking Value"}, {"table": "sheet1", "column": "Ride Distance"}] | [] | False |
| B1 | AVG("Driver Ratings") | [{"table": "sheet1", "column": "Driver Ratings"}] | [] | False |
| B1 | MIN("Customer Technical Assistance Time") | [{"table": "sheet1", "column": "Customer Technical Assistance Time"}] | [] | False |


## S50

类别 `data`；来源 `query_db`；调用 `ef03e6161730432d869e164df125a274`；状态 `success`。

```sql
SELECT "Vehicle Type",
       ROUND(100.0*SUM(CASE WHEN "Booking Status" = 'No Driver Found' THEN 1 ELSE 0 END)/COUNT(*),2) as no_driver_found_rate,
       ROUND(100.0*SUM(CASE WHEN "Booking Status" = 'Cancelled by Driver' THEN 1 ELSE 0 END)/COUNT(*),2) as driver_cancel_rate,
       ROUND(100.0*SUM(CASE WHEN "Booking Status" = 'Incomplete' THEN 1 ELSE 0 END)/COUNT(*),2) as incomplete_rate
FROM sheet1
GROUP BY "Vehicle Type"
ORDER BY no_driver_found_rate DESC
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-022/attempt-01/sql/S50.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-022/attempt-01/sql/S50.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-022/attempt-01/results/S50.rows.jsonl)；完整：True；SHA256：`71d7fef0e3f618d8967bf9e4e432f3d42c3098660debeee7ae25044c3bb3fb17`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "sheet1", "kind": "base", "block": null, "base_tables": ["sheet1"]}] | [] | ["\"Vehicle Type\""] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |
| B1 | COUNT(*) | [] | [] | True |
| B1 | COUNT(*) | [] | [] | True |
| B1 | SUM(CASE WHEN "Booking Status" = 'No Driver Found' THEN 1 ELSE 0 END) | [] | [{"table": "sheet1", "column": "Booking Status"}] | False |
| B1 | SUM(CASE WHEN "Booking Status" = 'Cancelled by Driver' THEN 1 ELSE 0 END) | [] | [{"table": "sheet1", "column": "Booking Status"}] | False |
| B1 | SUM(CASE WHEN "Booking Status" = 'Incomplete' THEN 1 ELSE 0 END) | [] | [{"table": "sheet1", "column": "Booking Status"}] | False |


## S51

类别 `data`；来源 `query_db`；调用 `3ec6bcec1fe64ad68da52bd5cc61d7a5`；状态 `success`。

```sql
SELECT "Driver Cancellation Reason", COUNT(*) as cnt
FROM sheet1
WHERE "Booking Status" = 'Cancelled by Driver'
GROUP BY "Driver Cancellation Reason"
ORDER BY cnt DESC
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-022/attempt-01/sql/S51.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-022/attempt-01/sql/S51.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-022/attempt-01/results/S51.rows.jsonl)；完整：True；SHA256：`76f27150ff7b7aeabdaec7a8c6136d0b9c75ecd28741d6d14e716ca51aaa518d`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "sheet1", "kind": "base", "block": null, "base_tables": ["sheet1"]}] | [] | ["\"Driver Cancellation Reason\""] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |


## S52

类别 `data`；来源 `query_db`；调用 `cbfb8bce19ac429f8fe922210ce7eaaa`；状态 `success`。

```sql
SELECT "Reason for cancelling by Customer", COUNT(*) as cnt
FROM sheet1
WHERE "Booking Status" = 'Cancelled by Customer'
GROUP BY "Reason for cancelling by Customer"
ORDER BY cnt DESC
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-022/attempt-01/sql/S52.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-022/attempt-01/sql/S52.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-022/attempt-01/results/S52.rows.jsonl)；完整：True；SHA256：`4f212c68cb95af50f671b47d8dea4b8cdcdddf8cf281f7759ebe57fd8fb42e26`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "sheet1", "kind": "base", "block": null, "base_tables": ["sheet1"]}] | [] | ["\"Reason for cancelling by Customer\""] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |


## S53

类别 `data`；来源 `python`；调用 `84740d6c217946628e7ab3dca39b74f7`；状态 `success`。

```sql

SELECT "Vehicle Type", "Booking Value", "Ride Distance", "Driver Ratings",
       "Booking Value" / NULLIF("Ride Distance", 0) as fare_per_km,
       STRFTIME('%w', SUBSTR("Date", 1, 4) || '-' || 
            PRINTF('%02d', CAST(SUBSTR("Date", 6, INSTR(SUBSTR("Date", 6), '/') - 1) AS INTEGER)) || '-' || 
            PRINTF('%02d', CAST(SUBSTR("Date", INSTR(SUBSTR("Date", 6), '/') + 6) AS INTEGER))) as day_of_week,
       CAST(SUBSTR("Time", 1, 2) AS INTEGER) as hour
FROM sheet1
WHERE "Booking Status" = 'Completed'

```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-022/attempt-01/sql/S53.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-022/attempt-01/sql/S53.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-022/attempt-01/results/S53.rows.jsonl)；完整：True；SHA256：`c684578ef14189f1aa1c4fb95cffd55a6e62345cc55fa973d434db1ff1a3b567`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "sheet1", "kind": "base", "block": null, "base_tables": ["sheet1"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |


## S54

类别 `data`；来源 `python`；调用 `a9314689989b4cadab4977e3a196fed1`；状态 `success`。

```sql

SELECT "Vehicle Type", "Booking Value", "Ride Distance", "Driver Ratings",
       "Booking Value" / NULLIF("Ride Distance", 0) as fare_per_km,
       STRFTIME('%w', SUBSTR("Date", 1, 4) || '-' || 
            PRINTF('%02d', CAST(SUBSTR("Date", 6, INSTR(SUBSTR("Date", 6), '/') - 1) AS INTEGER)) || '-' || 
            PRINTF('%02d', CAST(SUBSTR("Date", INSTR(SUBSTR("Date", 6), '/') + 6) AS INTEGER))) as day_of_week,
       CAST(SUBSTR("Time", 1, 2) AS INTEGER) as hour
FROM sheet1
WHERE "Booking Status" = 'Completed'

```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-022/attempt-01/sql/S54.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-022/attempt-01/sql/S54.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-022/attempt-01/results/S54.rows.jsonl)；完整：True；SHA256：`c684578ef14189f1aa1c4fb95cffd55a6e62345cc55fa973d434db1ff1a3b567`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "sheet1", "kind": "base", "block": null, "base_tables": ["sheet1"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |


## S55

类别 `data`；来源 `python`；调用 `91ace5a6780d4a679003eaeffb119c25`；状态 `success`。

```sql

SELECT "Vehicle Type", "Booking Value", "Ride Distance", "Driver Ratings",
       "Pickup Location", "Drop Location",
       "Booking Value" / NULLIF("Ride Distance", 0) as fare_per_km,
       STRFTIME('%w', SUBSTR("Date", 1, 4) || '-' || 
            PRINTF('%02d', CAST(SUBSTR("Date", 6, INSTR(SUBSTR("Date", 6), '/') - 1) AS INTEGER)) || '-' || 
            PRINTF('%02d', CAST(SUBSTR("Date", INSTR(SUBSTR("Date", 6), '/') + 6) AS INTEGER))) as day_of_week,
       CAST(SUBSTR("Time", 1, 2) AS INTEGER) as hour
FROM sheet1
WHERE "Booking Status" = 'Completed'

```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-022/attempt-01/sql/S55.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-022/attempt-01/sql/S55.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-022/attempt-01/results/S55.rows.jsonl)；完整：True；SHA256：`2b555d3cbd7230751d5597f543825cb7bfb68b0d95fb45d03dc29e877cbdfb48`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "sheet1", "kind": "base", "block": null, "base_tables": ["sheet1"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |


## S56

类别 `data`；来源 `query_db`；调用 `7c472f1c92684015b2295660d4bd1cd4`；状态 `success`。

```sql
SELECT COUNT(DISTINCT "Customer ID") as unique_customers,
       COUNT(DISTINCT "Booking ID") as unique_bookings,
       COUNT(DISTINCT "Date") as unique_dates
FROM sheet1
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-022/attempt-01/sql/S56.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-022/attempt-01/sql/S56.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-022/attempt-01/results/S56.rows.jsonl)；完整：True；SHA256：`8a633242f1fcac2f8eeb264248e921ee793663de80e93889884e8adf72139178`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "sheet1", "kind": "base", "block": null, "base_tables": ["sheet1"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(DISTINCT "Customer ID") | [{"table": "sheet1", "column": "Customer ID"}] | [] | False |
| B1 | COUNT(DISTINCT "Booking ID") | [{"table": "sheet1", "column": "Booking ID"}] | [] | False |
| B1 | COUNT(DISTINCT "Date") | [{"table": "sheet1", "column": "Date"}] | [] | False |


## S57

类别 `data`；来源 `query_db`；调用 `fceb17cd36ec4108902ff1ba05fd23fe`；状态 `success`。

```sql
SELECT CAST(SUBSTR("Time", 1, 2) AS INTEGER) as hour,
       COUNT(*) as total_bookings,
       ROUND(100.0*SUM(CASE WHEN "Booking Status" = 'No Driver Found' THEN 1 ELSE 0 END)/COUNT(*),1) as no_driver_rate,
       ROUND(100.0*SUM(CASE WHEN "Booking Status" = 'Completed' THEN 1 ELSE 0 END)/COUNT(*),1) as completion_rate
FROM sheet1
GROUP BY hour
ORDER BY hour
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-022/attempt-01/sql/S57.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-022/attempt-01/sql/S57.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-022/attempt-01/results/S57.rows.jsonl)；完整：True；SHA256：`3d65e386beaa7181406ab6bec4baaac7b39f3719b2a201ce2e74f1f0fcde524b`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "sheet1", "kind": "base", "block": null, "base_tables": ["sheet1"]}] | [] | ["CAST(SUBSTRING(\"Time\", 1, 2) AS INTEGER)"] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |
| B1 | COUNT(*) | [] | [] | True |
| B1 | COUNT(*) | [] | [] | True |
| B1 | SUM(CASE WHEN "Booking Status" = 'No Driver Found' THEN 1 ELSE 0 END) | [] | [{"table": "sheet1", "column": "Booking Status"}] | False |
| B1 | SUM(CASE WHEN "Booking Status" = 'Completed' THEN 1 ELSE 0 END) | [] | [{"table": "sheet1", "column": "Booking Status"}] | False |


## S58

类别 `data`；来源 `query_db`；调用 `d9e55612ed1144efab7bd631e653087b`；状态 `success`。

```sql
SELECT "Vehicle Type",
       ROUND(AVG("Booking Value"),2) as avg_booking,
       ROUND(AVG("Ride Distance"),2) as avg_dist,
       ROUND(SUM("Booking Value"),2) as total_earnings,
       COUNT(*) as completed_rides
FROM sheet1
WHERE "Booking Status" = 'Completed'
GROUP BY "Vehicle Type"
ORDER BY total_earnings DESC
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-022/attempt-01/sql/S58.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-022/attempt-01/sql/S58.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-022/attempt-01/results/S58.rows.jsonl)；完整：True；SHA256：`a8174a2509f1e0c43ee93bdd851d0d0427f4467a4949c3c237eb0f8b2262f3dc`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "sheet1", "kind": "base", "block": null, "base_tables": ["sheet1"]}] | [] | ["\"Vehicle Type\""] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |
| B1 | AVG("Booking Value") | [{"table": "sheet1", "column": "Booking Value"}] | [] | False |
| B1 | AVG("Ride Distance") | [{"table": "sheet1", "column": "Ride Distance"}] | [] | False |
| B1 | SUM("Booking Value") | [{"table": "sheet1", "column": "Booking Value"}] | [] | False |


## S59

类别 `data`；来源 `query_db`；调用 `d1bf324e2d8847149b35670306a23b15`；状态 `success`。

```sql
SELECT CAST(SUBSTR("Time", 1, 2) AS INTEGER) as hour,
       COUNT(*) as total_bookings,
       ROUND(100.0*SUM(CASE WHEN "Booking Status" = 'No Driver Found' THEN 1 ELSE 0 END)/COUNT(*),1) as no_driver_rate,
       ROUND(100.0*SUM(CASE WHEN "Booking Status" = 'Completed' THEN 1 ELSE 0 END)/COUNT(*),1) as completion_rate,
       ROUND(100.0*SUM(CASE WHEN "Booking Status" = 'Cancelled by Driver' THEN 1 ELSE 0 END)/COUNT(*),1) as driver_cancel_rate
FROM sheet1
WHERE CAST(SUBSTR("Time", 1, 2) AS INTEGER) >= 12
GROUP BY hour
ORDER BY hour
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-022/attempt-01/sql/S59.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-022/attempt-01/sql/S59.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-022/attempt-01/results/S59.rows.jsonl)；完整：True；SHA256：`e110c15616900ec5a992f4e33822359fba66d51330209db8df315437830ece53`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "sheet1", "kind": "base", "block": null, "base_tables": ["sheet1"]}] | [] | ["CAST(SUBSTRING(\"Time\", 1, 2) AS INTEGER)"] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |
| B1 | COUNT(*) | [] | [] | True |
| B1 | COUNT(*) | [] | [] | True |
| B1 | COUNT(*) | [] | [] | True |
| B1 | SUM(CASE WHEN "Booking Status" = 'No Driver Found' THEN 1 ELSE 0 END) | [] | [{"table": "sheet1", "column": "Booking Status"}] | False |
| B1 | SUM(CASE WHEN "Booking Status" = 'Completed' THEN 1 ELSE 0 END) | [] | [{"table": "sheet1", "column": "Booking Status"}] | False |
| B1 | SUM(CASE WHEN "Booking Status" = 'Cancelled by Driver' THEN 1 ELSE 0 END) | [] | [{"table": "sheet1", "column": "Booking Status"}] | False |


## S60

类别 `data`；来源 `query_db`；调用 `8a5110942a05454fae924223af9b4378`；状态 `success`。

```sql
SELECT COUNT(*) as rides_per_customer, COUNT(*) as customer_count
FROM (
  SELECT "Customer ID", COUNT(*) as ride_count
  FROM sheet1
  WHERE "Booking Status" = 'Completed'
  GROUP BY "Customer ID"
)
GROUP BY ride_count
ORDER BY ride_count
LIMIT 20
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-022/attempt-01/sql/S60.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-022/attempt-01/sql/S60.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-022/attempt-01/results/S60.rows.jsonl)；完整：True；SHA256：`841158d2b267c38d563060edfc6787294652f61b2a32ac6b26ceef97bccec28c`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "sheet1", "kind": "base", "block": null, "base_tables": ["sheet1"]}] | [] | ["\"Customer ID\""] |
| B2 | [{"alias": "", "kind": "derived", "block": "B1", "base_tables": ["sheet1"]}] | [] | ["ride_count"] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |
| B2 | COUNT(*) | [] | [] | True |
| B2 | COUNT(*) | [] | [] | True |


## S61

类别 `data`；来源 `query_db`；调用 `085698ffb5e7400982740cb4f4333137`；状态 `success`。

```sql
SELECT ROUND(AVG(ride_count),1) as avg_rides_per_customer,
       MIN(ride_count) as min_rides, MAX(ride_count) as max_rides
FROM (
  SELECT "Customer ID", COUNT(*) as ride_count
  FROM sheet1
  WHERE "Booking Status" = 'Completed'
  GROUP BY "Customer ID"
)
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-022/attempt-01/sql/S61.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-022/attempt-01/sql/S61.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-022/attempt-01/results/S61.rows.jsonl)；完整：True；SHA256：`1db82a0410dedbcdf78d72ed13b9e5629c0cb41840ffdd5d22da4668a470122f`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "sheet1", "kind": "base", "block": null, "base_tables": ["sheet1"]}] | [] | ["\"Customer ID\""] |
| B2 | [{"alias": "", "kind": "derived", "block": "B1", "base_tables": ["sheet1"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |
| B2 | MIN(ride_count) | [] | [] | False |
| B2 | MAX(ride_count) | [] | [] | False |
| B2 | AVG(ride_count) | [] | [] | False |


## S62

类别 `data`；来源 `python`；调用 `e25b9ea4cb7741a596cbce19770e2751`；状态 `success`。

```sql

SELECT "Vehicle Type", "Booking Value", "Ride Distance", "Driver Ratings",
       "Pickup Location",
       "Booking Value" / NULLIF("Ride Distance", 0) as fare_per_km,
       STRFTIME('%w', SUBSTR("Date", 1, 4) || '-' || 
            PRINTF('%02d', CAST(SUBSTR("Date", 6, INSTR(SUBSTR("Date", 6), '/') - 1) AS INTEGER)) || '-' || 
            PRINTF('%02d', CAST(SUBSTR("Date", INSTR(SUBSTR("Date", 6), '/') + 6) AS INTEGER))) as day_of_week
FROM sheet1
WHERE "Booking Status" = 'Completed'

```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-022/attempt-01/sql/S62.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-022/attempt-01/sql/S62.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-022/attempt-01/results/S62.rows.jsonl)；完整：True；SHA256：`a7c86b2690a8bee92231142d1596da1c829b313696becb85db9972ec8d24d39b`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "sheet1", "kind": "base", "block": null, "base_tables": ["sheet1"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |


## S63

类别 `data`；来源 `query_db`；调用 `f5a61c2a7fa9461d8df7df1cd2a31e23`；状态 `success`。

```sql
SELECT "Pickup Location" || ' → ' || "Drop Location" as route,
       COUNT(*) as ride_count,
       ROUND(AVG("Booking Value"), 2) as avg_booking,
       ROUND(AVG("Booking Value" / NULLIF("Ride Distance", 0)), 2) as avg_fare_per_km,
       ROUND(AVG("Ride Distance"), 2) as avg_distance
FROM sheet1
WHERE "Booking Status" = 'Completed'
GROUP BY route
HAVING ride_count >= 100
ORDER BY avg_fare_per_km DESC
LIMIT 15
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-022/attempt-01/sql/S63.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-022/attempt-01/sql/S63.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-022/attempt-01/results/S63.rows.jsonl)；完整：True；SHA256：`e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "sheet1", "kind": "base", "block": null, "base_tables": ["sheet1"]}] | [] | ["\"Pickup Location\" \|\| ' → ' \|\| \"Drop Location\""] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |
| B1 | AVG("Booking Value") | [{"table": "sheet1", "column": "Booking Value"}] | [] | False |
| B1 | AVG("Booking Value" / NULLIF("Ride Distance", 0)) | [{"table": "sheet1", "column": "Booking Value"}, {"table": "sheet1", "column": "Ride Distance"}] | [] | False |
| B1 | AVG("Ride Distance") | [{"table": "sheet1", "column": "Ride Distance"}] | [] | False |


## S64

类别 `data`；来源 `query_db`；调用 `3df5446fe52b4f0d8186f6035905c750`；状态 `success`。

```sql
SELECT "Drop Location",
       COUNT(*) as ride_count,
       ROUND(AVG("Booking Value"), 2) as avg_booking,
       ROUND(AVG("Booking Value" / NULLIF("Ride Distance", 0)), 2) as avg_fare_per_km
FROM sheet1
WHERE "Booking Status" = 'Completed'
GROUP BY "Drop Location"
ORDER BY avg_fare_per_km DESC
LIMIT 10
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-022/attempt-01/sql/S64.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-022/attempt-01/sql/S64.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-022/attempt-01/results/S64.rows.jsonl)；完整：True；SHA256：`14c1940b957bc88b89e1355822b8e4e9d79fb677ad5fc1c4562b8dc2a0fb26e1`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "sheet1", "kind": "base", "block": null, "base_tables": ["sheet1"]}] | [] | ["\"Drop Location\""] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |
| B1 | AVG("Booking Value") | [{"table": "sheet1", "column": "Booking Value"}] | [] | False |
| B1 | AVG("Booking Value" / NULLIF("Ride Distance", 0)) | [{"table": "sheet1", "column": "Booking Value"}, {"table": "sheet1", "column": "Ride Distance"}] | [] | False |


## S65

类别 `data`；来源 `query_db`；调用 `b76e8b24607d4e81b0c49ebd30645208`；状态 `success`。

```sql
SELECT CAST(SUBSTR("Date", 6, INSTR(SUBSTR("Date", 6), '/') - 1) AS INTEGER) as month,
       COUNT(*) as rides,
       ROUND(AVG("Booking Value"),2) as avg_booking,
       ROUND(AVG("Booking Value" / NULLIF("Ride Distance", 0)),2) as fare_per_km,
       ROUND(SUM("Booking Value"),0) as total_earnings
FROM sheet1
WHERE "Booking Status" = 'Completed'
GROUP BY month
ORDER BY month
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-022/attempt-01/sql/S65.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-022/attempt-01/sql/S65.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-022/attempt-01/results/S65.rows.jsonl)；完整：True；SHA256：`5aeba3de1e062ba85bdfc5637501e65744e16b001e28b96ba4936204a8deeaba`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "sheet1", "kind": "base", "block": null, "base_tables": ["sheet1"]}] | [] | ["CAST(SUBSTRING(\"Date\", 6, INSTR(SUBSTRING(\"Date\", 6), '/') - 1) AS INTEGER)"] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |
| B1 | AVG("Booking Value") | [{"table": "sheet1", "column": "Booking Value"}] | [] | False |
| B1 | AVG("Booking Value" / NULLIF("Ride Distance", 0)) | [{"table": "sheet1", "column": "Booking Value"}, {"table": "sheet1", "column": "Ride Distance"}] | [] | False |
| B1 | SUM("Booking Value") | [{"table": "sheet1", "column": "Booking Value"}] | [] | False |

