# dacomp-088

The Marketing Department is questioning the ROI efficiency of our investments in different…

运行：已提交。官方未评分。全部 SQL 尝试/成功 75/75；数据 SQL 73/73；Python 8 次。

完整原题：

The Marketing Department is questioning the ROI efficiency of our investments in different states and has requested a detailed analysis of regional market performance. Please perform calculations based on Salesforce data according to the following definitions:
- Customer Acquisition Cost (CAC) per state = (Total number of sales representatives in the state × 150,000 annual salary) / Number of new customers in the state
- Average Customer Value per state = A comparative analysis of the mean and median of `annual_revenue`
- Market Penetration Rate per state = Our number of customers / (State population / 10,000)
- Sales Efficiency per state = Average won deal amount / Average sales cycle days × Win probability
- Industry Concentration per state = Sum of the customer share from the top 3 industries

Additionally, you are required to:
1.  Design a State Competition Intensity Assessment Model (based on average win probability, average deal size, and sales cycle length).
2.  Construct a State Investment Return Prediction Algorithm (incorporating state GDP, population density, and primary industry types).

Finally, output a ranked list of states by their Investment Efficiency Score and provide a 3-year regional expansion priority recommendation.

| 表 | 行数 | 列数 |
| --- | --- | --- |
| industry_benchmark_data | 18 | 10 |
| salesforce__account_daily_history | 3000 | 17 |
| salesforce__opportunity_enhanced | 20000 | 71 |
| salesforce__sales_performance_dashboard | 1000 | 48 |
| state_economic_data | 50 | 13 |


实际路线（分析者依据 SQL/源码概括，不代表 Agent 自述）：SQL 提取州级客户与机会指标 → Python 多表连接、行业集中度与投资评分 → 州排名及扩张建议。

数据库大小：13,774,848 字节。

## 数据 SQL

| SQL | 状态 | 基础表 | Join 输入/类型 | GROUP BY | 聚合表达式 | 结果行数 | 数据库 ms |
| --- | --- | --- | --- | --- | --- | --- | --- |
| [S3/Q1](#s3) | success | ["state_economic_data"] | 0 / {} | [] | [] | 50 | 0.704 |
| [S4/Q2](#s4) | success | ["industry_benchmark_data"] | 0 / {} | [] | [] | 18 | 0.29 |
| [S5/Q3](#s5) | success | ["salesforce__account_daily_history"] | 0 / {} | [] | [] | 50 | 2.093 |
| [S6/Q4](#s6) | success | ["salesforce__opportunity_enhanced"] | 0 / {} | [] | [] | 49 | 13.054 |
| [S7/Q5](#s7) | success | ["salesforce__account_daily_history"] | 0 / {} | [] | [] | 24 | 1.396 |
| [S8/Q6](#s8) | success | ["salesforce__account_daily_history"] | 0 / {} | [] | ["COUNT(*)", "COUNT(DISTINCT account_id)", "COUNT(DISTINCT snapshot_date)"] | 1 | 1.426 |
| [S9/Q7](#s9) | success | ["salesforce__opportunity_enhanced"] | 0 / {} | [] | ["COUNT(*)", "COUNT(DISTINCT opportunity_id)", "COUNT(DISTINCT account_id)"] | 1 | 25.072 |
| [S10/Q8](#s10) | success | ["salesforce__sales_performance_dashboard"] | 0 / {} | [] | ["COUNT(*)", "COUNT(DISTINCT owner_id)"] | 1 | 1.005 |
| [S11/Q9](#s11) | success | ["salesforce__account_daily_history"] | 0 / {} | [] | [] | 5 | 0.37 |
| [S12/Q10](#s12) | success | ["salesforce__opportunity_enhanced"] | 0 / {} | [] | [] | 3 | 0.478 |
| [S13/Q11](#s13) | success | ["salesforce__account_daily_history"] | 0 / {} | ["billing_state"] | ["COUNT(DISTINCT account_id)", "COUNT(DISTINCT owner_id)"] | 46 | 1.278 |
| [S14/Q12](#s14) | success | ["salesforce__account_daily_history"] | 0 / {} | [] | [] | 6 | 0.745 |
| [S15/Q13](#s15) | success | ["salesforce__opportunity_enhanced"] | 0 / {} | ["opportunity_owner_state"] | ["COUNT(*)", "COUNT(DISTINCT account_id)", "AVG(CASE WHEN is_won = 1 THEN amount END)", "AVG(probability)", "AVG(days_to_close)", "SUM(CASE WHEN is_won = 1 THEN 1 ELSE 0 END)", "COUNT(*)"] | 49 | 23.399 |
| [S16/Q14](#s16) | success | ["salesforce__account_daily_history"] | 0 / {} | ["billing_state", "industry"] | ["COUNT(*)"] | 214 | 1.398 |
| [S17/Q15](#s17) | success | ["salesforce__account_daily_history"] | 0 / {} | [] | [] | 517 | 0.984 |
| [S18/Q16](#s18) | success | ["salesforce__account_daily_history"] | 0 / {} | [] | [] | 2768 | 5.151 |
| [S19/Q17](#s19) | success | ["salesforce__sales_performance_dashboard"] | 0 / {} | [] | [] | 5 | 0.482 |
| [S20/Q18](#s20) | success | ["salesforce__sales_performance_dashboard"] | 0 / {} | [] | [] | 3 | 0.636 |
| [S21/Q19](#s21) | success | ["salesforce__account_daily_history"] | 0 / {} | [] | ["COUNT(DISTINCT owner_id)", "COUNT(DISTINCT billing_state)"] | 1 | 1.255 |
| [S22/Q20](#s22) | success | ["salesforce__account_daily_history"] | 0 / {} | ["owner_id", "billing_state"] | ["COUNT(*)"] | 2768 | 5.988 |
| [S23/Q21](#s23) | success | ["salesforce__account_daily_history"] | 0 / {} | ["owner_id", "billing_state"] | ["COUNT(*)", "COUNT(*)"] | 955 | 7.892 |
| [S24/Q22](#s24) | success | ["salesforce__account_daily_history"] | 0 / {} | ["billing_state"] | ["COUNT(DISTINCT account_id)"] | 46 | 1.106 |
| [S25/Q23](#s25) | success | ["salesforce__opportunity_enhanced"] | 0 / {} | ["fiscal_year"] | ["COUNT(*)", "SUM(is_won)"] | 2 | 10.656 |
| [S26/Q24](#s26) | success | ["salesforce__account_daily_history"] | 0 / {} | [] | ["MIN(snapshot_date)", "MAX(snapshot_date)", "MIN(last_activity_date)", "MAX(last_activity_date)"] | 1 | 1.275 |
| [S27/Q25](#s27) | success | ["salesforce__opportunity_enhanced"] | 0 / {} | [] | ["MIN(created_date)", "MAX(created_date)", "MIN(close_date)", "MAX(close_date)"] | 1 | 8.897 |
| [S28/Q26](#s28) | success | ["salesforce__account_daily_history", "salesforce__opportunity_enhanced"] | 2 / {'INNER': 1} | ["a.billing_state"] | ["COUNT(DISTINCT a.account_id)"] | 49 | 12.073 |
| [S29/Q27](#s29) | success | ["salesforce__account_daily_history", "salesforce__opportunity_enhanced"] | 2 / {'LEFT': 1} | ["a.type"] | ["COUNT(DISTINCT a.account_id)", "COUNT(DISTINCT CASE WHEN o.is_won = 1 THEN a.account_id END)"] | 6 | 36.949 |
| [S30/Q28](#s30) | success | ["salesforce__opportunity_enhanced"] | 0 / {} | ["is_won"] | ["COUNT(*)", "AVG(amount)", "AVG(probability)"] | 2 | 12.848 |
| [S31/Q29](#s31) | success | ["salesforce__account_daily_history"] | 0 / {} | ["owner_id", "billing_state", "primary_state"] | ["COUNT(*)", "COUNT(*)", "COUNT(*)"] | 47 | 7.667 |
| [S32/Q30](#s32) | success | ["state_economic_data"] | 0 / {} | [] | [] | 50 | 0.303 |
| [S33/Q31](#s33) | success | ["salesforce__account_daily_history"] | 0 / {} | ["billing_state"] | ["COUNT(DISTINCT account_id)", "AVG(annual_revenue)", "SUM(annual_revenue)"] | 46 | 1.381 |
| [S34/Q32](#s34) | success | ["salesforce__opportunity_enhanced"] | 0 / {} | ["opportunity_owner_state"] | ["COUNT(*)", "SUM(is_won)", "AVG(CASE WHEN is_won = 1 THEN amount END)", "AVG(CASE WHEN is_won = 1 THEN probability END)", "AVG(CASE WHEN is_won = 1 THEN days_to_close END)", "AVG(probability)", "AVG(days_to_close)"] | 49 | 19.73 |
| [S35/Q33](#s35) | success | ["salesforce__account_daily_history"] | 0 / {} | ["billing_state", "industry"] | ["COUNT(DISTINCT account_id)"] | 214 | 1.718 |
| [S36/Q34](#s36) | success | ["state_economic_data"] | 0 / {} | [] | [] | 50 | 0.654 |
| [S37/Q35](#s37) | success | ["salesforce__account_daily_history"] | 0 / {} | [] | [] | 517 | 1.176 |
| [S38/Q36](#s38) | success | ["salesforce__account_daily_history"] | 0 / {} | ["billing_state"] | ["COUNT(DISTINCT account_id)", "AVG(annual_revenue)", "SUM(annual_revenue)"] | 46 | 1.161 |
| [S39/Q37](#s39) | success | ["salesforce__account_daily_history"] | 0 / {} | ["billing_state", "industry"] | ["COUNT(DISTINCT account_id)"] | 214 | 1.311 |
| [S40/Q38](#s40) | success | ["salesforce__opportunity_enhanced"] | 0 / {} | ["opportunity_owner_state"] | ["COUNT(*)", "SUM(is_won)", "AVG(CASE WHEN is_won = 1 THEN amount END)", "AVG(CASE WHEN is_won = 1 THEN probability END)", "AVG(CASE WHEN is_won = 1 THEN days_to_close END)", "AVG(probability)", "AVG(days_to_close)"] | 49 | 19.349 |
| [S41/Q39](#s41) | success | ["salesforce__account_daily_history"] | 0 / {} | ["owner_id", "billing_state", "primary_state"] | ["COUNT(*)", "COUNT(*)", "COUNT(*)"] | 47 | 7.153 |
| [S42/Q40](#s42) | success | ["state_economic_data"] | 0 / {} | [] | [] | 50 | 0.47 |
| [S43/Q41](#s43) | success | ["salesforce__account_daily_history"] | 0 / {} | [] | [] | 517 | 1.056 |
| [S44/Q42](#s44) | success | ["salesforce__account_daily_history"] | 0 / {} | ["billing_state"] | ["COUNT(DISTINCT account_id)", "AVG(annual_revenue)", "SUM(annual_revenue)"] | 46 | 0.981 |
| [S45/Q43](#s45) | success | ["salesforce__account_daily_history"] | 0 / {} | ["billing_state", "industry"] | ["COUNT(DISTINCT account_id)"] | 214 | 1.14 |
| [S46/Q44](#s46) | success | ["salesforce__opportunity_enhanced"] | 0 / {} | ["opportunity_owner_state"] | ["COUNT(*)", "SUM(is_won)", "AVG(CASE WHEN is_won = 1 THEN amount END)", "AVG(CASE WHEN is_won = 1 THEN probability END)", "AVG(CASE WHEN is_won = 1 THEN days_to_close END)", "AVG(probability)", "AVG(days_to_close)"] | 49 | 18.378 |
| [S47/Q45](#s47) | success | ["salesforce__account_daily_history"] | 0 / {} | ["owner_id", "billing_state", "primary_state"] | ["COUNT(*)", "COUNT(*)", "COUNT(*)"] | 47 | 7.031 |
| [S48/Q46](#s48) | success | ["state_economic_data"] | 0 / {} | [] | [] | 50 | 0.434 |
| [S49/Q47](#s49) | success | ["state_economic_data"] | 0 / {} | [] | [] | 50 | 0.348 |
| [S50/Q48](#s50) | success | ["salesforce__account_daily_history"] | 0 / {} | [] | [] | 517 | 1.055 |
| [S51/Q49](#s51) | success | ["salesforce__account_daily_history"] | 0 / {} | ["billing_state"] | ["COUNT(DISTINCT account_id)", "AVG(annual_revenue)", "SUM(annual_revenue)"] | 46 | 1.167 |
| [S52/Q50](#s52) | success | ["salesforce__account_daily_history"] | 0 / {} | ["billing_state", "industry"] | ["COUNT(DISTINCT account_id)"] | 214 | 1.178 |
| [S53/Q51](#s53) | success | ["salesforce__opportunity_enhanced"] | 0 / {} | ["opportunity_owner_state"] | ["COUNT(*)", "SUM(is_won)", "AVG(CASE WHEN is_won = 1 THEN amount END)", "AVG(CASE WHEN is_won = 1 THEN probability END)", "AVG(CASE WHEN is_won = 1 THEN days_to_close END)", "AVG(probability)", "AVG(days_to_close)"] | 49 | 18.372 |
| [S54/Q52](#s54) | success | ["salesforce__account_daily_history"] | 0 / {} | ["billing_state"] | ["COUNT(DISTINCT owner_id)"] | 50 | 2.372 |
| [S55/Q53](#s55) | success | ["state_economic_data"] | 0 / {} | [] | [] | 50 | 0.357 |
| [S56/Q54](#s56) | success | ["salesforce__opportunity_enhanced"] | 0 / {} | ["type"] | ["COUNT(*)", "SUM(is_won)"] | 4 | 11.845 |
| [S57/Q55](#s57) | success | ["salesforce__account_daily_history"] | 0 / {} | ["account_source"] | ["COUNT(*)"] | 5 | 0.963 |
| [S58/Q56](#s58) | success | ["salesforce__opportunity_enhanced"] | 0 / {} | ["opportunity_owner_state"] | ["COUNT(DISTINCT account_id)"] | 42 | 6.362 |
| [S59/Q57](#s59) | success | ["salesforce__account_daily_history", "salesforce__opportunity_enhanced"] | 2 / {'INNER': 1} | ["a.billing_state"] | ["COUNT(DISTINCT a.account_id)"] | 45 | 8.568 |
| [S60/Q58](#s60) | success | ["salesforce__account_daily_history"] | 0 / {} | [] | [] | 517 | 1.09 |
| [S61/Q59](#s61) | success | ["salesforce__account_daily_history"] | 0 / {} | ["billing_state"] | ["COUNT(DISTINCT account_id)", "AVG(annual_revenue)", "SUM(annual_revenue)"] | 46 | 0.968 |
| [S62/Q60](#s62) | success | ["salesforce__account_daily_history", "salesforce__opportunity_enhanced"] | 2 / {'INNER': 1} | ["a.billing_state"] | ["COUNT(DISTINCT a.account_id)"] | 45 | 8.329 |
| [S63/Q61](#s63) | success | ["salesforce__account_daily_history"] | 0 / {} | ["billing_state", "industry"] | ["COUNT(DISTINCT account_id)"] | 214 | 1.339 |
| [S64/Q62](#s64) | success | ["salesforce__opportunity_enhanced"] | 0 / {} | ["opportunity_owner_state"] | ["COUNT(*)", "SUM(is_won)", "AVG(CASE WHEN is_won = 1 THEN amount END)", "AVG(CASE WHEN is_won = 1 THEN probability END)", "AVG(CASE WHEN is_won = 1 THEN days_to_close END)", "AVG(probability)", "AVG(days_to_close)"] | 49 | 18.185 |
| [S65/Q63](#s65) | success | ["salesforce__account_daily_history"] | 0 / {} | ["billing_state"] | ["COUNT(DISTINCT owner_id)"] | 50 | 2.305 |
| [S66/Q64](#s66) | success | ["state_economic_data"] | 0 / {} | [] | [] | 50 | 0.334 |
| [S67/Q65](#s67) | success | ["salesforce__account_daily_history"] | 0 / {} | [] | [] | 517 | 1.125 |
| [S68/Q66](#s68) | success | ["salesforce__account_daily_history"] | 0 / {} | ["billing_state"] | ["COUNT(DISTINCT account_id)", "AVG(annual_revenue)", "SUM(annual_revenue)"] | 46 | 1.08 |
| [S69/Q67](#s69) | success | ["salesforce__account_daily_history", "salesforce__opportunity_enhanced"] | 2 / {'INNER': 1} | ["a.billing_state"] | ["COUNT(DISTINCT a.account_id)"] | 45 | 8.192 |
| [S70/Q68](#s70) | success | ["salesforce__account_daily_history"] | 0 / {} | ["billing_state", "industry"] | ["COUNT(DISTINCT account_id)"] | 214 | 1.322 |
| [S71/Q69](#s71) | success | ["salesforce__opportunity_enhanced"] | 0 / {} | ["opportunity_owner_state"] | ["COUNT(*)", "SUM(is_won)", "AVG(CASE WHEN is_won = 1 THEN amount END)", "AVG(CASE WHEN is_won = 1 THEN probability END)", "AVG(CASE WHEN is_won = 1 THEN days_to_close END)", "AVG(probability)", "AVG(days_to_close)"] | 49 | 18.949 |
| [S72/Q70](#s72) | success | ["salesforce__account_daily_history"] | 0 / {} | ["billing_state"] | ["COUNT(DISTINCT owner_id)"] | 50 | 2.485 |
| [S73/Q71](#s73) | success | ["state_economic_data"] | 0 / {} | [] | [] | 50 | 0.408 |
| [S74/Q72](#s74) | success | ["salesforce__opportunity_enhanced"] | 0 / {} | ["opportunity_owner_state"] | ["AVG(CASE WHEN is_won = 1 THEN amount END)", "AVG(probability)", "AVG(CASE WHEN is_won = 1 THEN days_to_close END)", "COUNT(*)", "SUM(is_won)"] | 3 | 11.022 |
| [S75/Q73](#s75) | success | ["salesforce__account_daily_history"] | 0 / {} | ["industry"] | ["COUNT(DISTINCT account_id)"] | 8 | 1.227 |


## 元数据和设置

| SQL | 类别 | 状态 | 内容 |
| --- | --- | --- | --- |
| S1 | connection_setup | success | PRAGMA query_only=ON |
| S2 | metadata | success | SELECT name,sql FROM sqlite_master WHERE type='table' ORDER BY name |


## Python 与执行位置

人工源码审查：**database_first_violation**。Python 按州连接客户、销售机会、销售代表和经济指标，并对行业份额求和、排序选前三、汇总扩张层级。这些 SQL 可执行的连接与 Top-K 聚合迁出数据库；收入中位数及绘图单独评价。 [证据](../reviews/dacomp-088.json)。

P1：Compute median revenue, industry concentration, and combine all state-level metrics. Median is not natively supported in SQLite, and the industry concentration plus model scoring is easier as a reproducible pandas pipeline over already-aggregated state-level rows.

[源码](../../../runs/dsv4flash-db-first-full-01/dacomp-088/attempt-01/python/P1.py)；[输出](../../../runs/dsv4flash-db-first-full-01/dacomp-088/attempt-01/python/P1.stdout)；[错误](../../../runs/dsv4flash-db-first-full-01/dacomp-088/attempt-01/python/P1.stderr)。检出需人工核验的 SQL 可实现操作：groupby(, .merge(, .query(, sort_values(；不能仅凭理由判为合规。

P2：Merge all state-level data, compute CAC, Market Penetration, Sales Efficiency, Competition Intensity Model, Investment Return Prediction Algorithm, and final Investment Efficiency Score. This requires custom weighted formulas best done in pandas.

[源码](../../../runs/dsv4flash-db-first-full-01/dacomp-088/attempt-01/python/P2.py)；[输出](../../../runs/dsv4flash-db-first-full-01/dacomp-088/attempt-01/python/P2.stdout)；[错误](../../../runs/dsv4flash-db-first-full-01/dacomp-088/attempt-01/python/P2.stderr)。检出需人工核验的 SQL 可实现操作：.merge(, sort_values(；不能仅凭理由判为合规。

P3：Re-run full analysis in a single script: pull state-level aggregates, compute medians (not supported in SQLite), and build the composite models/scoring pipeline in pandas.

[源码](../../../runs/dsv4flash-db-first-full-01/dacomp-088/attempt-01/python/P3.py)；[输出](../../../runs/dsv4flash-db-first-full-01/dacomp-088/attempt-01/python/P3.stdout)；[错误](../../../runs/dsv4flash-db-first-full-01/dacomp-088/attempt-01/python/P3.stderr)。检出需人工核验的 SQL 可实现操作：groupby(, .merge(, .query(, sort_values(；不能仅凭理由判为合规。

P4：Check coverage: which of the 50 states are missing from customer/opportunity data, and validate intermediate metrics to ensure model robustness before finalizing the report.

[源码](../../../runs/dsv4flash-db-first-full-01/dacomp-088/attempt-01/python/P4.py)；[输出](../../../runs/dsv4flash-db-first-full-01/dacomp-088/attempt-01/python/P4.stdout)；[错误](../../../runs/dsv4flash-db-first-full-01/dacomp-088/attempt-01/python/P4.stderr)。检出需人工核验的 SQL 可实现操作：.query(, sort_values(；不能仅凭理由判为合规。

P5：Refine rep assignment: use distinct owner_ids per state (reps operating in that state) instead of primary state assignment. Also fix CAC divide-by-zero for states with 0 reps. Recompute full model with corrected data.

[源码](../../../runs/dsv4flash-db-first-full-01/dacomp-088/attempt-01/python/P5.py)；[输出](../../../runs/dsv4flash-db-first-full-01/dacomp-088/attempt-01/python/P5.stdout)；[错误](../../../runs/dsv4flash-db-first-full-01/dacomp-088/attempt-01/python/P5.stderr)。检出需人工核验的 SQL 可实现操作：groupby(, .merge(, .query(, sort_values(；不能仅凭理由判为合规。

P6：Final comprehensive analysis: use billing_state-based new customers from New Business won opportunities for CAC. Generate all metrics, visualizations, and final ranking for the report.

[源码](../../../runs/dsv4flash-db-first-full-01/dacomp-088/attempt-01/python/P6.py)；[输出](../../../runs/dsv4flash-db-first-full-01/dacomp-088/attempt-01/python/P6.stdout)；[错误](../../../runs/dsv4flash-db-first-full-01/dacomp-088/attempt-01/python/P6.stderr)。检出需人工核验的 SQL 可实现操作：groupby(, .merge(, .query(, sort_values(；不能仅凭理由判为合规。

P7：Refine sales_efficiency to use state-level average win probability (probability field across all opportunities) instead of probability of won deals only, then recompute the composite score and validate a few metrics against SQL aggregates.

[源码](../../../runs/dsv4flash-db-first-full-01/dacomp-088/attempt-01/python/P7.py)；[输出](../../../runs/dsv4flash-db-first-full-01/dacomp-088/attempt-01/python/P7.stdout)；[错误](../../../runs/dsv4flash-db-first-full-01/dacomp-088/attempt-01/python/P7.stderr)。检出需人工核验的 SQL 可实现操作：groupby(, .merge(, .query(, sort_values(；不能仅凭理由判为合规。

P8：Generate final report figures from the validated v3 dataset: overall ranking chart, key metric comparisons, competition vs return scatter, and CAC vs penetration scatter. Also compute summary statistics for the report.

[源码](../../../runs/dsv4flash-db-first-full-01/dacomp-088/attempt-01/python/P8.py)；[输出](../../../runs/dsv4flash-db-first-full-01/dacomp-088/attempt-01/python/P8.stdout)；[错误](../../../runs/dsv4flash-db-first-full-01/dacomp-088/attempt-01/python/P8.stderr)。检出需人工核验的 SQL 可实现操作：groupby(, .query(；不能仅凭理由判为合规。

## 优化机会

已验证候选。筛选限于精确 SQL、相同自包含 CTE、相同单表完整过滤、可分解单表聚合；未覆盖任意 Join 等价和一般谓词蕴含。全部候选都是 offline，未测在线预测。

| 候选 | 类型 | 已有结果 | 覆盖 SQL | 后续次数 | 中间行数 | 验证 | 成本 |
| --- | --- | --- | --- | --- | --- | --- | --- |
| C1 | exact-result reuse | True | ["S37", "S43", "S50", "S60", "S67"] | 4 | unknown | not_verified_cap | Not tested |
| C2 | exact-result reuse | True | ["S38", "S44", "S51", "S61", "S68"] | 4 | unknown | not_verified_cap | Not tested |
| C3 | exact-result reuse | True | ["S39", "S45", "S52", "S63", "S70"] | 4 | unknown | not_verified_cap | Not tested |
| C4 | exact-result reuse | True | ["S40", "S46", "S53", "S64", "S71"] | 4 | unknown | not_verified_cap | Not tested |
| C5 | exact-result reuse | True | ["S41", "S47"] | 1 | unknown | not_verified_cap | Not tested |
| C6 | exact-result reuse | True | ["S42", "S48", "S55", "S66", "S73"] | 4 | unknown | not_verified_cap | Not tested |
| C7 | exact-result reuse | True | ["S54", "S65", "S72"] | 2 | unknown | not_verified_cap | Not tested |
| C8 | exact-result reuse | True | ["S62", "S69"] | 1 | unknown | not_verified_cap | Not tested |
| C9 | aggregate MV | False | ["S25", "S30", "S56"] | 2 | unknown | not_verified_cap | Not tested |
| C10 | common filtered view | False | ["S13", "S16", "S21", "S57", "S75"] | 4 | unknown | not_verified_cap | Not tested |
| C11 | aggregate MV | False | ["S16", "S57"] | 1 | unknown | not_verified_cap | Not tested |
| C12 | common filtered view | False | ["S15", "S34", "S40", "S46", "S53", "S64", "S71"] | 6 | 20000 | verified | Not benchmarked; correctness alone does not establish net speedup. |
| C13 | aggregate MV | False | ["S34", "S40", "S46", "S53", "S64", "S71"] | 5 | 49 | verified | Not benchmarked; correctness alone does not establish net speedup. |
| C14 | common filtered view | False | ["S17", "S24", "S33", "S35", "S37", "S38", "S39", "S43", "S44", "S45", "S50", "S51", "S52", "S60", "S61", "S63", "S67", "S68", "S70"] | 18 | 517 | verified | Not benchmarked; correctness alone does not establish net speedup. |
| C15 | common filtered view | False | ["S18", "S22", "S54", "S65", "S72"] | 4 | unknown | not_verified_cap | Not tested |


已验证覆盖（含触发查询、候选并集去重）：26/73 条成功数据 SQL。正确性仅针对当前数据库快照；未测性能的候选不能声称已加速。

[完整 build/rewrite 与比较证据](dacomp-088.analysis.json)。

### C14：common filtered view

Same single source and complete filter; original filter retained.

原查询 [S17](#s17), [S24](#s24), [S33](#s33), [S35](#s35), [S37](#s37), [S38](#s38), [S39](#s39), [S43](#s43), [S44](#s44), [S45](#s45), [S50](#s50), [S51](#s51), [S52](#s52), [S60](#s60), [S61](#s61), [S63](#s63), [S67](#s67), [S68](#s68), [S70](#s70) → 新增共享状态 C14 → 后续 18 次可复用。该构建点为事后假设，不代表 Agent 当时预知后续。

构建定义：

```sql
SELECT * FROM "salesforce__account_daily_history" WHERE type = 'Customer' AND NOT billing_state IS NULL
```

受益查询 S17 的改写示例：

```sql
SELECT billing_state, annual_revenue FROM temp.reuse_candidate AS salesforce__account_daily_history WHERE type = 'Customer' AND NOT billing_state IS NULL ORDER BY billing_state
```

| 原 SQL | 列名一致 | 结果一致 | 比较方法 |
| --- | --- | --- | --- |
| S17 | True | True | ordered_numeric_tolerance |
| S24 | True | True | ordered_numeric_tolerance |
| S33 | True | True | exact_multiset |
| S35 | True | True | exact_multiset |
| S37 | True | True | exact_multiset |
| S38 | True | True | exact_multiset |
| S39 | True | True | exact_multiset |
| S43 | True | True | exact_multiset |
| S44 | True | True | exact_multiset |
| S45 | True | True | exact_multiset |
| S50 | True | True | exact_multiset |
| S51 | True | True | exact_multiset |
| S52 | True | True | exact_multiset |
| S60 | True | True | exact_multiset |
| S61 | True | True | exact_multiset |
| S63 | True | True | exact_multiset |
| S67 | True | True | exact_multiset |
| S68 | True | True | exact_multiset |
| S70 | True | True | exact_multiset |


验证状态：verified；成本结论：Not benchmarked; correctness alone does not establish net speedup.

### C12：common filtered view

Same single source and complete filter; original filter retained.

原查询 [S15](#s15), [S34](#s34), [S40](#s40), [S46](#s46), [S53](#s53), [S64](#s64), [S71](#s71) → 新增共享状态 C12 → 后续 6 次可复用。该构建点为事后假设，不代表 Agent 当时预知后续。

构建定义：

```sql
SELECT * FROM "salesforce__opportunity_enhanced" WHERE NOT opportunity_owner_state IS NULL
```

受益查询 S15 的改写示例：

```sql
SELECT opportunity_owner_state, COUNT(*) AS n_opps, COUNT(DISTINCT account_id) AS n_accounts, AVG(CASE WHEN is_won = 1 THEN amount END) AS avg_won_amount, AVG(probability) AS avg_probability, AVG(days_to_close) AS avg_days_to_close, SUM(CASE WHEN is_won = 1 THEN 1 ELSE 0 END) AS won_opps, COUNT(*) AS total_opps FROM temp.reuse_candidate AS salesforce__opportunity_enhanced WHERE NOT opportunity_owner_state IS NULL GROUP BY opportunity_owner_state ORDER BY n_opps DESC
```

| 原 SQL | 列名一致 | 结果一致 | 比较方法 |
| --- | --- | --- | --- |
| S15 | True | True | ordered_numeric_tolerance |
| S34 | True | True | exact_multiset |
| S40 | True | True | exact_multiset |
| S46 | True | True | exact_multiset |
| S53 | True | True | exact_multiset |
| S64 | True | True | exact_multiset |
| S71 | True | True | exact_multiset |


验证状态：verified；成本结论：Not benchmarked; correctness alone does not establish net speedup.

### C13：aggregate MV

Union of grouping keys; decomposable aggregate states; AVG uses SUM and non-NULL COUNT.

原查询 [S34](#s34), [S40](#s40), [S46](#s46), [S53](#s53), [S64](#s64), [S71](#s71) → 新增共享状态 C13 → 后续 5 次可复用。该构建点为事后假设，不代表 Agent 当时预知后续。

构建定义：

```sql
SELECT opportunity_owner_state AS __g0, COUNT(*) AS __a0, SUM(is_won) AS __a1, SUM(CASE WHEN is_won = 1 THEN amount END) AS __a2_sum, COUNT(CASE WHEN is_won = 1 THEN amount END) AS __a2_n, SUM(CASE WHEN is_won = 1 THEN probability END) AS __a3_sum, COUNT(CASE WHEN is_won = 1 THEN probability END) AS __a3_n, SUM(CASE WHEN is_won = 1 THEN days_to_close END) AS __a4_sum, COUNT(CASE WHEN is_won = 1 THEN days_to_close END) AS __a4_n, SUM(probability) AS __a5_sum, COUNT(probability) AS __a5_n, SUM(days_to_close) AS __a6_sum, COUNT(days_to_close) AS __a6_n FROM "salesforce__opportunity_enhanced" WHERE NOT opportunity_owner_state IS NULL GROUP BY opportunity_owner_state
```

受益查询 S34 的改写示例：

```sql
/* Per-state opportunity stats (owner state) */ SELECT __g0 AS state, SUM(__a0) AS n_opps, SUM(__a1) AS won_opps, ROUND((1.0 * SUM(__a2_sum) / NULLIF(SUM(__a2_n), 0)), 2) AS avg_won_amount, ROUND((1.0 * SUM(__a3_sum) / NULLIF(SUM(__a3_n), 0)), 2) AS avg_won_prob, ROUND((1.0 * SUM(__a4_sum) / NULLIF(SUM(__a4_n), 0)), 2) AS avg_won_cycle_days, ROUND((1.0 * SUM(__a5_sum) / NULLIF(SUM(__a5_n), 0)), 2) AS avg_probability, ROUND((1.0 * SUM(__a6_sum) / NULLIF(SUM(__a6_n), 0)), 2) AS avg_cycle_days FROM temp.reuse_candidate GROUP BY __g0
```

| 原 SQL | 列名一致 | 结果一致 | 比较方法 |
| --- | --- | --- | --- |
| S34 | True | True | exact_multiset |
| S40 | True | True | exact_multiset |
| S46 | True | True | exact_multiset |
| S53 | True | True | exact_multiset |
| S64 | True | True | exact_multiset |
| S71 | True | True | exact_multiset |


验证状态：verified；成本结论：Not benchmarked; correctness alone does not establish net speedup.

结果依赖：自动记录 SQL→Python 的接口父调用，以及源码中引用归档文件的消费者；字面值相同不认定因果。模型方向选择需要人工读取消息，尚未做全面因果标注。

[原始报告](../../../runs/dsv4flash-db-first-full-01/dacomp-088/attempt-01/answer.md)；[统一消息](../../../runs/dsv4flash-db-first-full-01/dacomp-088/attempt-01/messages.jsonl)；[原始 OpenCode 事件](../../../runs/dsv4flash-db-first-full-01/dacomp-088/attempt-01/opencode.jsonl)；[SQL 引擎日志](../../../runs/dsv4flash-db-first-full-01/dacomp-088/attempt-01/sql_journal.jsonl)。

[可读报告（本地图片链接规范化）](../answers/dacomp-088.md)。原始回答保留，分析结论未改写。

## S1

类别 `connection_setup`；来源 `connection`；调用 `6cc1e7a54d69432ca9c98819623bf260`；状态 `success`。

```sql
PRAGMA query_only=ON
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-088/attempt-01/sql/S1.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-088/attempt-01/sql/S1.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-088/attempt-01/results/S1.rows.jsonl)；完整：True；SHA256：`e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`。

## S2

类别 `metadata`；来源 `list_db`；调用 `6cc1e7a54d69432ca9c98819623bf260`；状态 `success`。

```sql
SELECT name,sql FROM sqlite_master WHERE type='table' ORDER BY name
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-088/attempt-01/sql/S2.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-088/attempt-01/sql/S2.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-088/attempt-01/results/S2.rows.jsonl)；完整：True；SHA256：`ea74d86184106f0b54302445b0d0256e0e9f2ba90dde3bfca495adf511a00673`。

## S3

类别 `data`；来源 `query_db`；调用 `36e9cfba8994417483444dab55f7d31b`；状态 `success`。

```sql
SELECT * FROM state_economic_data ORDER BY state_name
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-088/attempt-01/sql/S3.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-088/attempt-01/sql/S3.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-088/attempt-01/results/S3.rows.jsonl)；完整：True；SHA256：`f0d207daf9049b6102018ab0bb9ede0c17b4bacb8ed4c0690758c362f0794257`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "state_economic_data", "kind": "base", "block": null, "base_tables": ["state_economic_data"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |


## S4

类别 `data`；来源 `query_db`；调用 `87ba7276f74b433bb700ec0bff4bdce3`；状态 `success`。

```sql
SELECT * FROM industry_benchmark_data ORDER BY industry_name
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-088/attempt-01/sql/S4.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-088/attempt-01/sql/S4.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-088/attempt-01/results/S4.rows.jsonl)；完整：True；SHA256：`aeb75a8ac319a5c1f96c2b9b86256bd9130f9e2ec48d228c2364eeadf822ec02`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "industry_benchmark_data", "kind": "base", "block": null, "base_tables": ["industry_benchmark_data"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |


## S5

类别 `data`；来源 `query_db`；调用 `75015f9f4bcc45eeae33b80923bb178b`；状态 `success`。

```sql
SELECT DISTINCT billing_state FROM salesforce__account_daily_history ORDER BY billing_state
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-088/attempt-01/sql/S5.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-088/attempt-01/sql/S5.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-088/attempt-01/results/S5.rows.jsonl)；完整：True；SHA256：`e26626d8bcd1e3318d942fcf96b80abd997b681fb1ee54dbe6dc9dac02428638`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "salesforce__account_daily_history", "kind": "base", "block": null, "base_tables": ["salesforce__account_daily_history"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |


## S6

类别 `data`；来源 `query_db`；调用 `c77d511f84b648d68f69a2ee0c589b65`；状态 `success`。

```sql
SELECT DISTINCT opportunity_owner_state FROM salesforce__opportunity_enhanced ORDER BY opportunity_owner_state
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-088/attempt-01/sql/S6.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-088/attempt-01/sql/S6.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-088/attempt-01/results/S6.rows.jsonl)；完整：True；SHA256：`52c3bff3a0f953fc7b26776923921061ed90e8bc4550b4b00673bc17a904fdfc`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "salesforce__opportunity_enhanced", "kind": "base", "block": null, "base_tables": ["salesforce__opportunity_enhanced"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |


## S7

类别 `data`；来源 `query_db`；调用 `4151cf783ec24a2cb833721bfa2fdde1`；状态 `success`。

```sql
SELECT DISTINCT industry FROM salesforce__account_daily_history ORDER BY industry
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-088/attempt-01/sql/S7.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-088/attempt-01/sql/S7.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-088/attempt-01/results/S7.rows.jsonl)；完整：True；SHA256：`55f66363f25bf09e3f8d56d7fa686403bb0d1aec833e1222e647dfaad490bd3a`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "salesforce__account_daily_history", "kind": "base", "block": null, "base_tables": ["salesforce__account_daily_history"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |


## S8

类别 `data`；来源 `query_db`；调用 `cc85d31c7d6746b6a23a94c299c32a4e`；状态 `success`。

```sql
SELECT COUNT(*) AS n, COUNT(DISTINCT account_id) AS n_accounts, COUNT(DISTINCT snapshot_date) AS n_snapshots FROM salesforce__account_daily_history
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-088/attempt-01/sql/S8.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-088/attempt-01/sql/S8.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-088/attempt-01/results/S8.rows.jsonl)；完整：True；SHA256：`3363f12ed529ed70dd4d06fc8ed76276947916a2b3cd88574443cce24476e4e3`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "salesforce__account_daily_history", "kind": "base", "block": null, "base_tables": ["salesforce__account_daily_history"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |
| B1 | COUNT(DISTINCT account_id) | [{"table": "salesforce__account_daily_history", "column": "account_id"}] | [] | False |
| B1 | COUNT(DISTINCT snapshot_date) | [{"table": "salesforce__account_daily_history", "column": "snapshot_date"}] | [] | False |


## S9

类别 `data`；来源 `query_db`；调用 `cfd5d26114264c959bad445c52e7ee77`；状态 `success`。

```sql
SELECT COUNT(*) AS n, COUNT(DISTINCT opportunity_id) AS n_opps, COUNT(DISTINCT account_id) AS n_accounts FROM salesforce__opportunity_enhanced
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-088/attempt-01/sql/S9.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-088/attempt-01/sql/S9.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-088/attempt-01/results/S9.rows.jsonl)；完整：True；SHA256：`c4627ff1b69e2ada1aee1ff932e3003f5a0f969fd699ca369fbd0910c17b0121`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "salesforce__opportunity_enhanced", "kind": "base", "block": null, "base_tables": ["salesforce__opportunity_enhanced"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |
| B1 | COUNT(DISTINCT opportunity_id) | [{"table": "salesforce__opportunity_enhanced", "column": "opportunity_id"}] | [] | False |
| B1 | COUNT(DISTINCT account_id) | [{"table": "salesforce__opportunity_enhanced", "column": "account_id"}] | [] | False |


## S10

类别 `data`；来源 `query_db`；调用 `de49acb63554474e86d9cfe389c721af`；状态 `success`。

```sql
SELECT COUNT(*) AS n, COUNT(DISTINCT owner_id) AS n_reps FROM salesforce__sales_performance_dashboard
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-088/attempt-01/sql/S10.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-088/attempt-01/sql/S10.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-088/attempt-01/results/S10.rows.jsonl)；完整：True；SHA256：`a90e15298292a76fb54f4650d13af13b5d1abeebc98778c442822f8d46e28715`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "salesforce__sales_performance_dashboard", "kind": "base", "block": null, "base_tables": ["salesforce__sales_performance_dashboard"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |
| B1 | COUNT(DISTINCT owner_id) | [{"table": "salesforce__sales_performance_dashboard", "column": "owner_id"}] | [] | False |


## S11

类别 `data`；来源 `query_db`；调用 `0e7307786dfa446fb3a9efbc0ca38f90`；状态 `success`。

```sql
SELECT * FROM salesforce__account_daily_history LIMIT 5
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-088/attempt-01/sql/S11.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-088/attempt-01/sql/S11.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-088/attempt-01/results/S11.rows.jsonl)；完整：True；SHA256：`a5a70a0f1bd735cf033a2e3d9d78907284cfb52f1760f521d9adf2e547aa909c`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "salesforce__account_daily_history", "kind": "base", "block": null, "base_tables": ["salesforce__account_daily_history"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |


## S12

类别 `data`；来源 `query_db`；调用 `3b5ff0ccf3614bb9b98ff343ca511ccf`；状态 `success`。

```sql
SELECT * FROM salesforce__opportunity_enhanced LIMIT 3
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-088/attempt-01/sql/S12.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-088/attempt-01/sql/S12.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-088/attempt-01/results/S12.rows.jsonl)；完整：True；SHA256：`08eb90494ba7b6b1e34f71c975569e57feafd2416b96fa3aa4ba47c6e2ece917`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "salesforce__opportunity_enhanced", "kind": "base", "block": null, "base_tables": ["salesforce__opportunity_enhanced"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |


## S13

类别 `data`；来源 `query_db`；调用 `8cd4a976234f4000912b1e446a982a52`；状态 `success`。

```sql
SELECT billing_state, COUNT(DISTINCT account_id) AS n_customers, COUNT(DISTINCT owner_id) AS n_owners
FROM salesforce__account_daily_history
WHERE type = 'Customer'
GROUP BY billing_state
ORDER BY n_customers DESC
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-088/attempt-01/sql/S13.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-088/attempt-01/sql/S13.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-088/attempt-01/results/S13.rows.jsonl)；完整：True；SHA256：`26b9361e25d08caa867d9162f6814ea575347a776f0219658b126101c210d2d9`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "salesforce__account_daily_history", "kind": "base", "block": null, "base_tables": ["salesforce__account_daily_history"]}] | [] | ["billing_state"] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(DISTINCT account_id) | [{"table": "salesforce__account_daily_history", "column": "account_id"}] | [] | False |
| B1 | COUNT(DISTINCT owner_id) | [{"table": "salesforce__account_daily_history", "column": "owner_id"}] | [] | False |


## S14

类别 `data`；来源 `query_db`；调用 `d1a5f9d78a554c58bbb66c105353c225`；状态 `success`。

```sql
SELECT DISTINCT type FROM salesforce__account_daily_history
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-088/attempt-01/sql/S14.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-088/attempt-01/sql/S14.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-088/attempt-01/results/S14.rows.jsonl)；完整：True；SHA256：`806c7fde1056a74b92d296a03a4e355e93bd75e6fcbbfc88d614e8303e69f4cc`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "salesforce__account_daily_history", "kind": "base", "block": null, "base_tables": ["salesforce__account_daily_history"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |


## S15

类别 `data`；来源 `query_db`；调用 `35cb8f7dc5694abeabf149a9ebd96e82`；状态 `success`。

```sql
SELECT opportunity_owner_state, 
       COUNT(*) AS n_opps,
       COUNT(DISTINCT account_id) AS n_accounts,
       AVG(CASE WHEN is_won = 1 THEN amount END) AS avg_won_amount,
       AVG(probability) AS avg_probability,
       AVG(days_to_close) AS avg_days_to_close,
       SUM(CASE WHEN is_won = 1 THEN 1 ELSE 0 END) AS won_opps,
       COUNT(*) AS total_opps
FROM salesforce__opportunity_enhanced
WHERE opportunity_owner_state IS NOT NULL
GROUP BY opportunity_owner_state
ORDER BY n_opps DESC
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-088/attempt-01/sql/S15.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-088/attempt-01/sql/S15.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-088/attempt-01/results/S15.rows.jsonl)；完整：True；SHA256：`678d5ad3736f33b792bcfd1765e72d0f7e8818d3bcda37b8d193f5e1500f91e0`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "salesforce__opportunity_enhanced", "kind": "base", "block": null, "base_tables": ["salesforce__opportunity_enhanced"]}] | [] | ["opportunity_owner_state"] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |
| B1 | COUNT(DISTINCT account_id) | [{"table": "salesforce__opportunity_enhanced", "column": "account_id"}] | [] | False |
| B1 | AVG(CASE WHEN is_won = 1 THEN amount END) | [{"table": "salesforce__opportunity_enhanced", "column": "amount"}] | [{"table": "salesforce__opportunity_enhanced", "column": "is_won"}] | False |
| B1 | AVG(probability) | [{"table": "salesforce__opportunity_enhanced", "column": "probability"}] | [] | False |
| B1 | AVG(days_to_close) | [{"table": "salesforce__opportunity_enhanced", "column": "days_to_close"}] | [] | False |
| B1 | SUM(CASE WHEN is_won = 1 THEN 1 ELSE 0 END) | [] | [{"table": "salesforce__opportunity_enhanced", "column": "is_won"}] | False |
| B1 | COUNT(*) | [] | [] | True |


## S16

类别 `data`；来源 `query_db`；调用 `24fac1dc6b884969a07a99472dce5233`；状态 `success`。

```sql
SELECT billing_state, industry, COUNT(*) AS n_customers
FROM salesforce__account_daily_history
WHERE type = 'Customer'
GROUP BY billing_state, industry
ORDER BY billing_state, n_customers DESC
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-088/attempt-01/sql/S16.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-088/attempt-01/sql/S16.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-088/attempt-01/results/S16.rows.jsonl)；完整：True；SHA256：`d09adffd1c1fe71784331787b519289623b4ca2a9d35ef577f45dd98e7023067`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "salesforce__account_daily_history", "kind": "base", "block": null, "base_tables": ["salesforce__account_daily_history"]}] | [] | ["billing_state", "industry"] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |


## S17

类别 `data`；来源 `query_db`；调用 `74d51f927b8443e7bee9c427c7b99852`；状态 `success`。

```sql
SELECT billing_state, annual_revenue
FROM salesforce__account_daily_history
WHERE type = 'Customer' AND billing_state IS NOT NULL
ORDER BY billing_state
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-088/attempt-01/sql/S17.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-088/attempt-01/sql/S17.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-088/attempt-01/results/S17.rows.jsonl)；完整：True；SHA256：`d92516c89d0a5d4348f9879f4fb9ce20ec1c2199826896df94cb27622e4e6266`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "salesforce__account_daily_history", "kind": "base", "block": null, "base_tables": ["salesforce__account_daily_history"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |


## S18

类别 `data`；来源 `query_db`；调用 `831b46e9d0184d7d88d6d7d8a5c72593`；状态 `success`。

```sql
SELECT DISTINCT owner_id, billing_state
FROM salesforce__account_daily_history
WHERE billing_state IS NOT NULL
ORDER BY owner_id
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-088/attempt-01/sql/S18.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-088/attempt-01/sql/S18.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-088/attempt-01/results/S18.rows.jsonl)；完整：True；SHA256：`60535ea4f936d1ba0764a79079d14afa6fb7c65740d43086c414af37a162bf4c`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "salesforce__account_daily_history", "kind": "base", "block": null, "base_tables": ["salesforce__account_daily_history"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |


## S19

类别 `data`；来源 `query_db`；调用 `abb0ff84047a4e24b3127a9445215230`；状态 `success`。

```sql
SELECT * FROM salesforce__sales_performance_dashboard LIMIT 5
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-088/attempt-01/sql/S19.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-088/attempt-01/sql/S19.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-088/attempt-01/results/S19.rows.jsonl)；完整：True；SHA256：`fdef74f542023796a05cd3bdc1c94cacb7d26487754f4e343e036d920931ba97`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "salesforce__sales_performance_dashboard", "kind": "base", "block": null, "base_tables": ["salesforce__sales_performance_dashboard"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |


## S20

类别 `data`；来源 `query_db`；调用 `79734587185f4bdda04d96935b00b76c`；状态 `success`。

```sql
SELECT DISTINCT territory_coverage FROM salesforce__sales_performance_dashboard
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-088/attempt-01/sql/S20.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-088/attempt-01/sql/S20.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-088/attempt-01/results/S20.rows.jsonl)；完整：True；SHA256：`0cee2ba484a2ee928fbaa49197ec8db7e70227530bd11a35da967d2816e2a9ec`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "salesforce__sales_performance_dashboard", "kind": "base", "block": null, "base_tables": ["salesforce__sales_performance_dashboard"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |


## S21

类别 `data`；来源 `query_db`；调用 `8c55f88710fc43f48f8b7ab704af1021`；状态 `success`。

```sql
SELECT COUNT(DISTINCT owner_id) AS n_reps, COUNT(DISTINCT billing_state) AS n_states FROM salesforce__account_daily_history WHERE type = 'Customer'
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-088/attempt-01/sql/S21.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-088/attempt-01/sql/S21.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-088/attempt-01/results/S21.rows.jsonl)；完整：True；SHA256：`5490f79c9bfe7527692636823ac6447a0b007e53ca5cd83405c87ff46374874d`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "salesforce__account_daily_history", "kind": "base", "block": null, "base_tables": ["salesforce__account_daily_history"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(DISTINCT owner_id) | [{"table": "salesforce__account_daily_history", "column": "owner_id"}] | [] | False |
| B1 | COUNT(DISTINCT billing_state) | [{"table": "salesforce__account_daily_history", "column": "billing_state"}] | [] | False |


## S22

类别 `data`；来源 `query_db`；调用 `d2bb04955bf1435aa8831458c5b1005f`；状态 `success`。

```sql
SELECT owner_id, billing_state, COUNT(*) AS cnt
FROM salesforce__account_daily_history
WHERE billing_state IS NOT NULL
GROUP BY owner_id, billing_state
ORDER BY owner_id, cnt DESC
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-088/attempt-01/sql/S22.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-088/attempt-01/sql/S22.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-088/attempt-01/results/S22.rows.jsonl)；完整：True；SHA256：`4b15661c646674da5c48d2835350a51e4fd5742f9f8e96be82ed8f64982f89e5`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "salesforce__account_daily_history", "kind": "base", "block": null, "base_tables": ["salesforce__account_daily_history"]}] | [] | ["owner_id", "billing_state"] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |


## S23

类别 `data`；来源 `query_db`；调用 `d55682413ab442f7b58355957e3e6ca7`；状态 `success`。

```sql
-- Primary state per owner (most common billing_state)
SELECT owner_id, billing_state AS primary_state
FROM (
  SELECT owner_id, billing_state, COUNT(*) AS cnt,
         ROW_NUMBER() OVER (PARTITION BY owner_id ORDER BY COUNT(*) DESC) AS rn
  FROM salesforce__account_daily_history
  WHERE billing_state IS NOT NULL
  GROUP BY owner_id, billing_state
) t
WHERE rn = 1
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-088/attempt-01/sql/S23.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-088/attempt-01/sql/S23.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-088/attempt-01/results/S23.rows.jsonl)；完整：True；SHA256：`6fb6f9994bd23087f7bcb422ef40408160097a1ae6e6d2b20111a403b49f3fee`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "salesforce__account_daily_history", "kind": "base", "block": null, "base_tables": ["salesforce__account_daily_history"]}] | [] | ["owner_id", "billing_state"] |
| B2 | [{"alias": "t", "kind": "derived", "block": "B1", "base_tables": ["salesforce__account_daily_history"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |
| B1 | COUNT(*) | [] | [] | True |


## S24

类别 `data`；来源 `query_db`；调用 `2e5683944ed1474695168b108dfcd109`；状态 `success`。

```sql
-- Number of new customers per state (accounts with type='Customer')
SELECT billing_state, COUNT(DISTINCT account_id) AS n_customers
FROM salesforce__account_daily_history
WHERE type = 'Customer' AND billing_state IS NOT NULL
GROUP BY billing_state
ORDER BY n_customers DESC
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-088/attempt-01/sql/S24.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-088/attempt-01/sql/S24.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-088/attempt-01/results/S24.rows.jsonl)；完整：True；SHA256：`fe249fab22e79abcf3db9c6596d83841a74933c958bddaa0f636c8bf05849e96`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "salesforce__account_daily_history", "kind": "base", "block": null, "base_tables": ["salesforce__account_daily_history"]}] | [] | ["billing_state"] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(DISTINCT account_id) | [{"table": "salesforce__account_daily_history", "column": "account_id"}] | [] | False |


## S25

类别 `data`；来源 `query_db`；调用 `a09b7711d0fe433094f66dc5d4325591`；状态 `success`。

```sql
SELECT fiscal_year, COUNT(*) AS n, SUM(is_won) AS won
FROM salesforce__opportunity_enhanced
GROUP BY fiscal_year ORDER BY fiscal_year
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-088/attempt-01/sql/S25.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-088/attempt-01/sql/S25.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-088/attempt-01/results/S25.rows.jsonl)；完整：True；SHA256：`ec146edd3549fbeefaee88ade6a7b9f128a015279b89ec0b184b99f9b6fb827b`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "salesforce__opportunity_enhanced", "kind": "base", "block": null, "base_tables": ["salesforce__opportunity_enhanced"]}] | [] | ["fiscal_year"] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |
| B1 | SUM(is_won) | [{"table": "salesforce__opportunity_enhanced", "column": "is_won"}] | [] | False |


## S26

类别 `data`；来源 `query_db`；调用 `d46e30ce8cd844399c14764e7715db60`；状态 `success`。

```sql
SELECT MIN(snapshot_date), MAX(snapshot_date), MIN(last_activity_date), MAX(last_activity_date) FROM salesforce__account_daily_history
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-088/attempt-01/sql/S26.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-088/attempt-01/sql/S26.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-088/attempt-01/results/S26.rows.jsonl)；完整：True；SHA256：`51e0b9f93f616ee629922abcd758908e2f607b99b0e95dc19d60ee2e695aede1`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "salesforce__account_daily_history", "kind": "base", "block": null, "base_tables": ["salesforce__account_daily_history"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | MIN(snapshot_date) | [{"table": "salesforce__account_daily_history", "column": "snapshot_date"}] | [] | False |
| B1 | MAX(snapshot_date) | [{"table": "salesforce__account_daily_history", "column": "snapshot_date"}] | [] | False |
| B1 | MIN(last_activity_date) | [{"table": "salesforce__account_daily_history", "column": "last_activity_date"}] | [] | False |
| B1 | MAX(last_activity_date) | [{"table": "salesforce__account_daily_history", "column": "last_activity_date"}] | [] | False |


## S27

类别 `data`；来源 `query_db`；调用 `9413836e444a4f74bea568e58aa60dac`；状态 `success`。

```sql
SELECT MIN(created_date), MAX(created_date), MIN(close_date), MAX(close_date) FROM salesforce__opportunity_enhanced
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-088/attempt-01/sql/S27.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-088/attempt-01/sql/S27.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-088/attempt-01/results/S27.rows.jsonl)；完整：True；SHA256：`91e5911514a66b376d4510ca44257c469e4e29fc55ba4cb408345db59bfa8ec7`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "salesforce__opportunity_enhanced", "kind": "base", "block": null, "base_tables": ["salesforce__opportunity_enhanced"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | MIN(created_date) | [{"table": "salesforce__opportunity_enhanced", "column": "created_date"}] | [] | False |
| B1 | MAX(created_date) | [{"table": "salesforce__opportunity_enhanced", "column": "created_date"}] | [] | False |
| B1 | MIN(close_date) | [{"table": "salesforce__opportunity_enhanced", "column": "close_date"}] | [] | False |
| B1 | MAX(close_date) | [{"table": "salesforce__opportunity_enhanced", "column": "close_date"}] | [] | False |


## S28

类别 `data`；来源 `query_db`；调用 `660ed17ba1744972a6e5f21935e937b3`；状态 `success`。

```sql
-- Count of won opportunities per account (to identify active customers)
SELECT a.billing_state, COUNT(DISTINCT a.account_id) AS n_customers_with_won_opps
FROM salesforce__account_daily_history a
JOIN salesforce__opportunity_enhanced o ON a.account_id = o.account_id
WHERE o.is_won = 1 AND a.billing_state IS NOT NULL
GROUP BY a.billing_state
ORDER BY n_customers_with_won_opps DESC
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-088/attempt-01/sql/S28.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-088/attempt-01/sql/S28.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-088/attempt-01/results/S28.rows.jsonl)；完整：True；SHA256：`258e841bf398531d5ba3d3b838584d0d893c0222dc8bc59c338db456a78aadbf`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "a", "kind": "base", "block": null, "base_tables": ["salesforce__account_daily_history"]}, {"alias": "o", "kind": "base", "block": null, "base_tables": ["salesforce__opportunity_enhanced"]}] | [{"type": "INNER", "right": "salesforce__opportunity_enhanced AS o", "on": "a.account_id = o.account_id", "using": []}] | ["a.billing_state"] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(DISTINCT a.account_id) | [{"table": "salesforce__account_daily_history", "column": "account_id"}] | [] | False |


## S29

类别 `data`；来源 `query_db`；调用 `5bea850a4ada4715a71f0e8b9a54cc64`；状态 `success`。

```sql
-- Overview of account types and won opp relationships
SELECT a.type,
       COUNT(DISTINCT a.account_id) AS n_accounts,
       COUNT(DISTINCT CASE WHEN o.is_won = 1 THEN a.account_id END) AS n_with_won
FROM salesforce__account_daily_history a
LEFT JOIN salesforce__opportunity_enhanced o ON a.account_id = o.account_id
GROUP BY a.type
ORDER BY n_accounts DESC
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-088/attempt-01/sql/S29.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-088/attempt-01/sql/S29.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-088/attempt-01/results/S29.rows.jsonl)；完整：True；SHA256：`bb2523d81f01b2698710d07a6e9bfc00388e40115df2daeaeb6623fee5a07f87`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "a", "kind": "base", "block": null, "base_tables": ["salesforce__account_daily_history"]}, {"alias": "o", "kind": "base", "block": null, "base_tables": ["salesforce__opportunity_enhanced"]}] | [{"type": "LEFT", "right": "salesforce__opportunity_enhanced AS o", "on": "a.account_id = o.account_id", "using": []}] | ["a.type"] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(DISTINCT a.account_id) | [{"table": "salesforce__account_daily_history", "column": "account_id"}] | [] | False |
| B1 | COUNT(DISTINCT CASE WHEN o.is_won = 1 THEN a.account_id END) | [{"table": "salesforce__account_daily_history", "column": "account_id"}] | [{"table": "salesforce__opportunity_enhanced", "column": "is_won"}] | False |


## S30

类别 `data`；来源 `query_db`；调用 `7a298eca0ac24041a7001002f2a67868`；状态 `success`。

```sql
SELECT is_won, COUNT(*) AS n, AVG(amount) AS avg_amount, AVG(probability) AS avg_prob
FROM salesforce__opportunity_enhanced
GROUP BY is_won
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-088/attempt-01/sql/S30.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-088/attempt-01/sql/S30.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-088/attempt-01/results/S30.rows.jsonl)；完整：True；SHA256：`455bfb462bd2f9c57a67b7b52c6c5be71b4ecc2bffcf8465a947dd4f37b01bdc`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "salesforce__opportunity_enhanced", "kind": "base", "block": null, "base_tables": ["salesforce__opportunity_enhanced"]}] | [] | ["is_won"] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |
| B1 | AVG(amount) | [{"table": "salesforce__opportunity_enhanced", "column": "amount"}] | [] | False |
| B1 | AVG(probability) | [{"table": "salesforce__opportunity_enhanced", "column": "probability"}] | [] | False |


## S31

类别 `data`；来源 `query_db`；调用 `5c69001d45c74fe2ad2cfca13ad2874f`；状态 `success`。

```sql
-- Count reps per state (by primary state)
SELECT primary_state, COUNT(*) AS n_reps
FROM (
  SELECT owner_id, billing_state AS primary_state
  FROM (
    SELECT owner_id, billing_state, COUNT(*) AS cnt,
           ROW_NUMBER() OVER (PARTITION BY owner_id ORDER BY COUNT(*) DESC) AS rn
    FROM salesforce__account_daily_history
    WHERE billing_state IS NOT NULL
    GROUP BY owner_id, billing_state
  ) t
  WHERE rn = 1
) r
GROUP BY primary_state
ORDER BY n_reps DESC
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-088/attempt-01/sql/S31.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-088/attempt-01/sql/S31.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-088/attempt-01/results/S31.rows.jsonl)；完整：True；SHA256：`77377cacb6b58f10357a94d9f1be6f9bfd236e88446c4136350b1401ce27e620`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "salesforce__account_daily_history", "kind": "base", "block": null, "base_tables": ["salesforce__account_daily_history"]}] | [] | ["owner_id", "billing_state"] |
| B2 | [{"alias": "t", "kind": "derived", "block": "B1", "base_tables": ["salesforce__account_daily_history"]}] | [] | [] |
| B3 | [{"alias": "r", "kind": "derived", "block": "B2", "base_tables": ["salesforce__account_daily_history"]}] | [] | ["primary_state"] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |
| B1 | COUNT(*) | [] | [] | True |
| B3 | COUNT(*) | [] | [] | True |


## S32

类别 `data`；来源 `query_db`；调用 `962f918b8ad84369b62fa26d5d774bcd`；状态 `success`。

```sql
-- Also get all states from state_economic_data
SELECT state_name FROM state_economic_data ORDER BY state_name
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-088/attempt-01/sql/S32.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-088/attempt-01/sql/S32.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-088/attempt-01/results/S32.rows.jsonl)；完整：True；SHA256：`e26626d8bcd1e3318d942fcf96b80abd997b681fb1ee54dbe6dc9dac02428638`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "state_economic_data", "kind": "base", "block": null, "base_tables": ["state_economic_data"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |


## S33

类别 `data`；来源 `query_db`；调用 `4674e622937b41e8a3e6bf1172f6357b`；状态 `success`。

```sql
-- Per-state customer stats: count, mean, median revenue
SELECT billing_state AS state,
       COUNT(DISTINCT account_id) AS n_customers,
       ROUND(AVG(annual_revenue),2) AS avg_revenue,
       ROUND(SUM(annual_revenue),2) AS total_revenue
FROM salesforce__account_daily_history
WHERE type = 'Customer' AND billing_state IS NOT NULL
GROUP BY billing_state
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-088/attempt-01/sql/S33.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-088/attempt-01/sql/S33.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-088/attempt-01/results/S33.rows.jsonl)；完整：True；SHA256：`f0fc59bd4009b52dd0d721bf6b82ebed441ada6a8f1cdee2d649227cc2bd08a3`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "salesforce__account_daily_history", "kind": "base", "block": null, "base_tables": ["salesforce__account_daily_history"]}] | [] | ["billing_state"] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(DISTINCT account_id) | [{"table": "salesforce__account_daily_history", "column": "account_id"}] | [] | False |
| B1 | AVG(annual_revenue) | [{"table": "salesforce__account_daily_history", "column": "annual_revenue"}] | [] | False |
| B1 | SUM(annual_revenue) | [{"table": "salesforce__account_daily_history", "column": "annual_revenue"}] | [] | False |


## S34

类别 `data`；来源 `query_db`；调用 `7d94c187e18b44f29348d05768036906`；状态 `success`。

```sql
-- Per-state opportunity stats (owner state)
SELECT opportunity_owner_state AS state,
       COUNT(*) AS n_opps,
       SUM(is_won) AS won_opps,
       ROUND(AVG(CASE WHEN is_won=1 THEN amount END),2) AS avg_won_amount,
       ROUND(AVG(CASE WHEN is_won=1 THEN probability END),2) AS avg_won_prob,
       ROUND(AVG(CASE WHEN is_won=1 THEN days_to_close END),2) AS avg_won_cycle_days,
       ROUND(AVG(probability),2) AS avg_probability,
       ROUND(AVG(days_to_close),2) AS avg_cycle_days
FROM salesforce__opportunity_enhanced
WHERE opportunity_owner_state IS NOT NULL
GROUP BY opportunity_owner_state
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-088/attempt-01/sql/S34.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-088/attempt-01/sql/S34.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-088/attempt-01/results/S34.rows.jsonl)；完整：True；SHA256：`b274585fe653de5ebe6aa37fc50744f635a62da9801fc49605552fac5835a32e`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "salesforce__opportunity_enhanced", "kind": "base", "block": null, "base_tables": ["salesforce__opportunity_enhanced"]}] | [] | ["opportunity_owner_state"] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |
| B1 | SUM(is_won) | [{"table": "salesforce__opportunity_enhanced", "column": "is_won"}] | [] | False |
| B1 | AVG(CASE WHEN is_won = 1 THEN amount END) | [{"table": "salesforce__opportunity_enhanced", "column": "amount"}] | [{"table": "salesforce__opportunity_enhanced", "column": "is_won"}] | False |
| B1 | AVG(CASE WHEN is_won = 1 THEN probability END) | [{"table": "salesforce__opportunity_enhanced", "column": "probability"}] | [{"table": "salesforce__opportunity_enhanced", "column": "is_won"}] | False |
| B1 | AVG(CASE WHEN is_won = 1 THEN days_to_close END) | [{"table": "salesforce__opportunity_enhanced", "column": "days_to_close"}] | [{"table": "salesforce__opportunity_enhanced", "column": "is_won"}] | False |
| B1 | AVG(probability) | [{"table": "salesforce__opportunity_enhanced", "column": "probability"}] | [] | False |
| B1 | AVG(days_to_close) | [{"table": "salesforce__opportunity_enhanced", "column": "days_to_close"}] | [] | False |


## S35

类别 `data`；来源 `query_db`；调用 `e099be61b21d4d949c2190a04bad7990`；状态 `success`。

```sql
-- Industry customer share per state
SELECT billing_state AS state, industry,
       COUNT(DISTINCT account_id) AS n_cust_industry
FROM salesforce__account_daily_history
WHERE type = 'Customer' AND billing_state IS NOT NULL
GROUP BY billing_state, industry
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-088/attempt-01/sql/S35.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-088/attempt-01/sql/S35.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-088/attempt-01/results/S35.rows.jsonl)；完整：True；SHA256：`e96b2fe3b633ae2e7bf5303ccecceeefd94fa1118d3fc278dbb12aa4d7f942e5`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "salesforce__account_daily_history", "kind": "base", "block": null, "base_tables": ["salesforce__account_daily_history"]}] | [] | ["billing_state", "industry"] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(DISTINCT account_id) | [{"table": "salesforce__account_daily_history", "column": "account_id"}] | [] | False |


## S36

类别 `data`；来源 `query_db`；调用 `c3e2a576eca7403ba122625abf0c6401`；状态 `success`。

```sql
SELECT state_name, population, gdp_billion, gdp_per_capita, primary_industry, secondary_industry,
       tertiary_industry, quaternary_industry, market_maturity_score, competition_intensity,
       business_friendly_index, unemployment_rate, corporate_tax_rate
FROM state_economic_data
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-088/attempt-01/sql/S36.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-088/attempt-01/sql/S36.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-088/attempt-01/results/S36.rows.jsonl)；完整：True；SHA256：`45a0b785cdac40ac4d5d510d30cad822c81ddaa6a0ecaecfb19f2af1d2184f0e`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "state_economic_data", "kind": "base", "block": null, "base_tables": ["state_economic_data"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |


## S37

类别 `data`；来源 `python`；调用 `373ca59dd870436981a8325ab300de72`；状态 `success`。

```sql

    SELECT billing_state AS state, annual_revenue
    FROM salesforce__account_daily_history
    WHERE type='Customer' AND billing_state IS NOT NULL

```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-088/attempt-01/sql/S37.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-088/attempt-01/sql/S37.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-088/attempt-01/results/S37.rows.jsonl)；完整：True；SHA256：`6971ff02f488c657a44ddcafdab1fb9adb7454cc8dbf87c193dcab8bd0ba277a`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "salesforce__account_daily_history", "kind": "base", "block": null, "base_tables": ["salesforce__account_daily_history"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |


## S38

类别 `data`；来源 `python`；调用 `373ca59dd870436981a8325ab300de72`；状态 `success`。

```sql

    SELECT billing_state AS state, COUNT(DISTINCT account_id) AS n_customers,
           AVG(annual_revenue) AS avg_revenue, SUM(annual_revenue) AS total_revenue
    FROM salesforce__account_daily_history
    WHERE type='Customer' AND billing_state IS NOT NULL
    GROUP BY billing_state

```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-088/attempt-01/sql/S38.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-088/attempt-01/sql/S38.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-088/attempt-01/results/S38.rows.jsonl)；完整：True；SHA256：`8eeb616f67786fea0fbc379aee8c48cba0bf0304ca1a5462156f265b9c049476`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "salesforce__account_daily_history", "kind": "base", "block": null, "base_tables": ["salesforce__account_daily_history"]}] | [] | ["billing_state"] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(DISTINCT account_id) | [{"table": "salesforce__account_daily_history", "column": "account_id"}] | [] | False |
| B1 | AVG(annual_revenue) | [{"table": "salesforce__account_daily_history", "column": "annual_revenue"}] | [] | False |
| B1 | SUM(annual_revenue) | [{"table": "salesforce__account_daily_history", "column": "annual_revenue"}] | [] | False |


## S39

类别 `data`；来源 `python`；调用 `373ca59dd870436981a8325ab300de72`；状态 `success`。

```sql

    SELECT billing_state AS state, industry, COUNT(DISTINCT account_id) AS n_cust_industry
    FROM salesforce__account_daily_history
    WHERE type='Customer' AND billing_state IS NOT NULL
    GROUP BY billing_state, industry

```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-088/attempt-01/sql/S39.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-088/attempt-01/sql/S39.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-088/attempt-01/results/S39.rows.jsonl)；完整：True；SHA256：`e96b2fe3b633ae2e7bf5303ccecceeefd94fa1118d3fc278dbb12aa4d7f942e5`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "salesforce__account_daily_history", "kind": "base", "block": null, "base_tables": ["salesforce__account_daily_history"]}] | [] | ["billing_state", "industry"] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(DISTINCT account_id) | [{"table": "salesforce__account_daily_history", "column": "account_id"}] | [] | False |


## S40

类别 `data`；来源 `python`；调用 `373ca59dd870436981a8325ab300de72`；状态 `success`。

```sql

    SELECT opportunity_owner_state AS state,
           COUNT(*) AS n_opps, SUM(is_won) AS won_opps,
           AVG(CASE WHEN is_won=1 THEN amount END) AS avg_won_amount,
           AVG(CASE WHEN is_won=1 THEN probability END) AS avg_won_prob,
           AVG(CASE WHEN is_won=1 THEN days_to_close END) AS avg_won_cycle_days,
           AVG(probability) AS avg_probability,
           AVG(days_to_close) AS avg_cycle_days
    FROM salesforce__opportunity_enhanced
    WHERE opportunity_owner_state IS NOT NULL
    GROUP BY opportunity_owner_state

```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-088/attempt-01/sql/S40.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-088/attempt-01/sql/S40.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-088/attempt-01/results/S40.rows.jsonl)；完整：True；SHA256：`0dd48343036e0ba3e05dac1f34760f3b5d9a11a4fdeba42a9ca53c064efe83ab`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "salesforce__opportunity_enhanced", "kind": "base", "block": null, "base_tables": ["salesforce__opportunity_enhanced"]}] | [] | ["opportunity_owner_state"] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |
| B1 | SUM(is_won) | [{"table": "salesforce__opportunity_enhanced", "column": "is_won"}] | [] | False |
| B1 | AVG(CASE WHEN is_won = 1 THEN amount END) | [{"table": "salesforce__opportunity_enhanced", "column": "amount"}] | [{"table": "salesforce__opportunity_enhanced", "column": "is_won"}] | False |
| B1 | AVG(CASE WHEN is_won = 1 THEN probability END) | [{"table": "salesforce__opportunity_enhanced", "column": "probability"}] | [{"table": "salesforce__opportunity_enhanced", "column": "is_won"}] | False |
| B1 | AVG(CASE WHEN is_won = 1 THEN days_to_close END) | [{"table": "salesforce__opportunity_enhanced", "column": "days_to_close"}] | [{"table": "salesforce__opportunity_enhanced", "column": "is_won"}] | False |
| B1 | AVG(probability) | [{"table": "salesforce__opportunity_enhanced", "column": "probability"}] | [] | False |
| B1 | AVG(days_to_close) | [{"table": "salesforce__opportunity_enhanced", "column": "days_to_close"}] | [] | False |


## S41

类别 `data`；来源 `python`；调用 `373ca59dd870436981a8325ab300de72`；状态 `success`。

```sql

    SELECT primary_state AS state, COUNT(*) AS n_reps
    FROM (
      SELECT owner_id, billing_state AS primary_state
      FROM (
        SELECT owner_id, billing_state, COUNT(*) AS cnt,
               ROW_NUMBER() OVER (PARTITION BY owner_id ORDER BY COUNT(*) DESC) AS rn
        FROM salesforce__account_daily_history
        WHERE billing_state IS NOT NULL
        GROUP BY owner_id, billing_state
      ) t
      WHERE rn = 1
    ) r
    GROUP BY primary_state

```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-088/attempt-01/sql/S41.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-088/attempt-01/sql/S41.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-088/attempt-01/results/S41.rows.jsonl)；完整：True；SHA256：`7b394359d6cbf8af366069081eaee534b7f2f9d423db343e7c90b1780aaf3bf5`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "salesforce__account_daily_history", "kind": "base", "block": null, "base_tables": ["salesforce__account_daily_history"]}] | [] | ["owner_id", "billing_state"] |
| B2 | [{"alias": "t", "kind": "derived", "block": "B1", "base_tables": ["salesforce__account_daily_history"]}] | [] | [] |
| B3 | [{"alias": "r", "kind": "derived", "block": "B2", "base_tables": ["salesforce__account_daily_history"]}] | [] | ["primary_state"] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |
| B1 | COUNT(*) | [] | [] | True |
| B3 | COUNT(*) | [] | [] | True |


## S42

类别 `data`；来源 `python`；调用 `373ca59dd870436981a8325ab300de72`；状态 `success`。

```sql

    SELECT state_name AS state, population, gdp_billion, gdp_per_capita,
           primary_industry, secondary_industry, tertiary_industry, quaternary_industry,
           market_maturity_score, competition_intensity, business_friendly_index,
           unemployment_rate, corporate_tax_rate
    FROM state_economic_data

```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-088/attempt-01/sql/S42.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-088/attempt-01/sql/S42.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-088/attempt-01/results/S42.rows.jsonl)；完整：True；SHA256：`45a0b785cdac40ac4d5d510d30cad822c81ddaa6a0ecaecfb19f2af1d2184f0e`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "state_economic_data", "kind": "base", "block": null, "base_tables": ["state_economic_data"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |


## S43

类别 `data`；来源 `python`；调用 `6a2bbd344fb34b5c92cece034e677c77`；状态 `success`。

```sql

    SELECT billing_state AS state, annual_revenue
    FROM salesforce__account_daily_history
    WHERE type='Customer' AND billing_state IS NOT NULL

```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-088/attempt-01/sql/S43.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-088/attempt-01/sql/S43.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-088/attempt-01/results/S43.rows.jsonl)；完整：True；SHA256：`6971ff02f488c657a44ddcafdab1fb9adb7454cc8dbf87c193dcab8bd0ba277a`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "salesforce__account_daily_history", "kind": "base", "block": null, "base_tables": ["salesforce__account_daily_history"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |


## S44

类别 `data`；来源 `python`；调用 `6a2bbd344fb34b5c92cece034e677c77`；状态 `success`。

```sql

    SELECT billing_state AS state, COUNT(DISTINCT account_id) AS n_customers,
           AVG(annual_revenue) AS avg_revenue, SUM(annual_revenue) AS total_revenue
    FROM salesforce__account_daily_history
    WHERE type='Customer' AND billing_state IS NOT NULL
    GROUP BY billing_state

```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-088/attempt-01/sql/S44.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-088/attempt-01/sql/S44.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-088/attempt-01/results/S44.rows.jsonl)；完整：True；SHA256：`8eeb616f67786fea0fbc379aee8c48cba0bf0304ca1a5462156f265b9c049476`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "salesforce__account_daily_history", "kind": "base", "block": null, "base_tables": ["salesforce__account_daily_history"]}] | [] | ["billing_state"] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(DISTINCT account_id) | [{"table": "salesforce__account_daily_history", "column": "account_id"}] | [] | False |
| B1 | AVG(annual_revenue) | [{"table": "salesforce__account_daily_history", "column": "annual_revenue"}] | [] | False |
| B1 | SUM(annual_revenue) | [{"table": "salesforce__account_daily_history", "column": "annual_revenue"}] | [] | False |


## S45

类别 `data`；来源 `python`；调用 `6a2bbd344fb34b5c92cece034e677c77`；状态 `success`。

```sql

    SELECT billing_state AS state, industry, COUNT(DISTINCT account_id) AS n_cust_industry
    FROM salesforce__account_daily_history
    WHERE type='Customer' AND billing_state IS NOT NULL
    GROUP BY billing_state, industry

```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-088/attempt-01/sql/S45.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-088/attempt-01/sql/S45.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-088/attempt-01/results/S45.rows.jsonl)；完整：True；SHA256：`e96b2fe3b633ae2e7bf5303ccecceeefd94fa1118d3fc278dbb12aa4d7f942e5`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "salesforce__account_daily_history", "kind": "base", "block": null, "base_tables": ["salesforce__account_daily_history"]}] | [] | ["billing_state", "industry"] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(DISTINCT account_id) | [{"table": "salesforce__account_daily_history", "column": "account_id"}] | [] | False |


## S46

类别 `data`；来源 `python`；调用 `6a2bbd344fb34b5c92cece034e677c77`；状态 `success`。

```sql

    SELECT opportunity_owner_state AS state,
           COUNT(*) AS n_opps, SUM(is_won) AS won_opps,
           AVG(CASE WHEN is_won=1 THEN amount END) AS avg_won_amount,
           AVG(CASE WHEN is_won=1 THEN probability END) AS avg_won_prob,
           AVG(CASE WHEN is_won=1 THEN days_to_close END) AS avg_won_cycle_days,
           AVG(probability) AS avg_probability,
           AVG(days_to_close) AS avg_cycle_days
    FROM salesforce__opportunity_enhanced
    WHERE opportunity_owner_state IS NOT NULL
    GROUP BY opportunity_owner_state

```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-088/attempt-01/sql/S46.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-088/attempt-01/sql/S46.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-088/attempt-01/results/S46.rows.jsonl)；完整：True；SHA256：`0dd48343036e0ba3e05dac1f34760f3b5d9a11a4fdeba42a9ca53c064efe83ab`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "salesforce__opportunity_enhanced", "kind": "base", "block": null, "base_tables": ["salesforce__opportunity_enhanced"]}] | [] | ["opportunity_owner_state"] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |
| B1 | SUM(is_won) | [{"table": "salesforce__opportunity_enhanced", "column": "is_won"}] | [] | False |
| B1 | AVG(CASE WHEN is_won = 1 THEN amount END) | [{"table": "salesforce__opportunity_enhanced", "column": "amount"}] | [{"table": "salesforce__opportunity_enhanced", "column": "is_won"}] | False |
| B1 | AVG(CASE WHEN is_won = 1 THEN probability END) | [{"table": "salesforce__opportunity_enhanced", "column": "probability"}] | [{"table": "salesforce__opportunity_enhanced", "column": "is_won"}] | False |
| B1 | AVG(CASE WHEN is_won = 1 THEN days_to_close END) | [{"table": "salesforce__opportunity_enhanced", "column": "days_to_close"}] | [{"table": "salesforce__opportunity_enhanced", "column": "is_won"}] | False |
| B1 | AVG(probability) | [{"table": "salesforce__opportunity_enhanced", "column": "probability"}] | [] | False |
| B1 | AVG(days_to_close) | [{"table": "salesforce__opportunity_enhanced", "column": "days_to_close"}] | [] | False |


## S47

类别 `data`；来源 `python`；调用 `6a2bbd344fb34b5c92cece034e677c77`；状态 `success`。

```sql

    SELECT primary_state AS state, COUNT(*) AS n_reps
    FROM (
      SELECT owner_id, billing_state AS primary_state
      FROM (
        SELECT owner_id, billing_state, COUNT(*) AS cnt,
               ROW_NUMBER() OVER (PARTITION BY owner_id ORDER BY COUNT(*) DESC) AS rn
        FROM salesforce__account_daily_history
        WHERE billing_state IS NOT NULL
        GROUP BY owner_id, billing_state
      ) t
      WHERE rn = 1
    ) r
    GROUP BY primary_state

```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-088/attempt-01/sql/S47.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-088/attempt-01/sql/S47.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-088/attempt-01/results/S47.rows.jsonl)；完整：True；SHA256：`7b394359d6cbf8af366069081eaee534b7f2f9d423db343e7c90b1780aaf3bf5`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "salesforce__account_daily_history", "kind": "base", "block": null, "base_tables": ["salesforce__account_daily_history"]}] | [] | ["owner_id", "billing_state"] |
| B2 | [{"alias": "t", "kind": "derived", "block": "B1", "base_tables": ["salesforce__account_daily_history"]}] | [] | [] |
| B3 | [{"alias": "r", "kind": "derived", "block": "B2", "base_tables": ["salesforce__account_daily_history"]}] | [] | ["primary_state"] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |
| B1 | COUNT(*) | [] | [] | True |
| B3 | COUNT(*) | [] | [] | True |


## S48

类别 `data`；来源 `python`；调用 `6a2bbd344fb34b5c92cece034e677c77`；状态 `success`。

```sql

    SELECT state_name AS state, population, gdp_billion, gdp_per_capita,
           primary_industry, secondary_industry, tertiary_industry, quaternary_industry,
           market_maturity_score, competition_intensity, business_friendly_index,
           unemployment_rate, corporate_tax_rate
    FROM state_economic_data

```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-088/attempt-01/sql/S48.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-088/attempt-01/sql/S48.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-088/attempt-01/results/S48.rows.jsonl)；完整：True；SHA256：`45a0b785cdac40ac4d5d510d30cad822c81ddaa6a0ecaecfb19f2af1d2184f0e`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "state_economic_data", "kind": "base", "block": null, "base_tables": ["state_economic_data"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |


## S49

类别 `data`；来源 `python`；调用 `3d3b92cd34ef4f8c823d8fcdf8571c8f`；状态 `success`。

```sql
SELECT state_name AS state FROM state_economic_data
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-088/attempt-01/sql/S49.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-088/attempt-01/sql/S49.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-088/attempt-01/results/S49.rows.jsonl)；完整：True；SHA256：`3edc9e09f024954102c48687d84817b937c4b5e22aea01af0daef78090cc5fb6`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "state_economic_data", "kind": "base", "block": null, "base_tables": ["state_economic_data"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |


## S50

类别 `data`；来源 `python`；调用 `6cd4574adad94a42826732d947a4d244`；状态 `success`。

```sql

    SELECT billing_state AS state, annual_revenue
    FROM salesforce__account_daily_history
    WHERE type='Customer' AND billing_state IS NOT NULL

```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-088/attempt-01/sql/S50.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-088/attempt-01/sql/S50.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-088/attempt-01/results/S50.rows.jsonl)；完整：True；SHA256：`6971ff02f488c657a44ddcafdab1fb9adb7454cc8dbf87c193dcab8bd0ba277a`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "salesforce__account_daily_history", "kind": "base", "block": null, "base_tables": ["salesforce__account_daily_history"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |


## S51

类别 `data`；来源 `python`；调用 `6cd4574adad94a42826732d947a4d244`；状态 `success`。

```sql

    SELECT billing_state AS state, COUNT(DISTINCT account_id) AS n_customers,
           AVG(annual_revenue) AS avg_revenue, SUM(annual_revenue) AS total_revenue
    FROM salesforce__account_daily_history
    WHERE type='Customer' AND billing_state IS NOT NULL
    GROUP BY billing_state

```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-088/attempt-01/sql/S51.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-088/attempt-01/sql/S51.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-088/attempt-01/results/S51.rows.jsonl)；完整：True；SHA256：`8eeb616f67786fea0fbc379aee8c48cba0bf0304ca1a5462156f265b9c049476`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "salesforce__account_daily_history", "kind": "base", "block": null, "base_tables": ["salesforce__account_daily_history"]}] | [] | ["billing_state"] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(DISTINCT account_id) | [{"table": "salesforce__account_daily_history", "column": "account_id"}] | [] | False |
| B1 | AVG(annual_revenue) | [{"table": "salesforce__account_daily_history", "column": "annual_revenue"}] | [] | False |
| B1 | SUM(annual_revenue) | [{"table": "salesforce__account_daily_history", "column": "annual_revenue"}] | [] | False |


## S52

类别 `data`；来源 `python`；调用 `6cd4574adad94a42826732d947a4d244`；状态 `success`。

```sql

    SELECT billing_state AS state, industry, COUNT(DISTINCT account_id) AS n_cust_industry
    FROM salesforce__account_daily_history
    WHERE type='Customer' AND billing_state IS NOT NULL
    GROUP BY billing_state, industry

```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-088/attempt-01/sql/S52.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-088/attempt-01/sql/S52.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-088/attempt-01/results/S52.rows.jsonl)；完整：True；SHA256：`e96b2fe3b633ae2e7bf5303ccecceeefd94fa1118d3fc278dbb12aa4d7f942e5`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "salesforce__account_daily_history", "kind": "base", "block": null, "base_tables": ["salesforce__account_daily_history"]}] | [] | ["billing_state", "industry"] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(DISTINCT account_id) | [{"table": "salesforce__account_daily_history", "column": "account_id"}] | [] | False |


## S53

类别 `data`；来源 `python`；调用 `6cd4574adad94a42826732d947a4d244`；状态 `success`。

```sql

    SELECT opportunity_owner_state AS state,
           COUNT(*) AS n_opps, SUM(is_won) AS won_opps,
           AVG(CASE WHEN is_won=1 THEN amount END) AS avg_won_amount,
           AVG(CASE WHEN is_won=1 THEN probability END) AS avg_won_prob,
           AVG(CASE WHEN is_won=1 THEN days_to_close END) AS avg_won_cycle_days,
           AVG(probability) AS avg_probability,
           AVG(days_to_close) AS avg_cycle_days
    FROM salesforce__opportunity_enhanced
    WHERE opportunity_owner_state IS NOT NULL
    GROUP BY opportunity_owner_state

```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-088/attempt-01/sql/S53.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-088/attempt-01/sql/S53.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-088/attempt-01/results/S53.rows.jsonl)；完整：True；SHA256：`0dd48343036e0ba3e05dac1f34760f3b5d9a11a4fdeba42a9ca53c064efe83ab`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "salesforce__opportunity_enhanced", "kind": "base", "block": null, "base_tables": ["salesforce__opportunity_enhanced"]}] | [] | ["opportunity_owner_state"] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |
| B1 | SUM(is_won) | [{"table": "salesforce__opportunity_enhanced", "column": "is_won"}] | [] | False |
| B1 | AVG(CASE WHEN is_won = 1 THEN amount END) | [{"table": "salesforce__opportunity_enhanced", "column": "amount"}] | [{"table": "salesforce__opportunity_enhanced", "column": "is_won"}] | False |
| B1 | AVG(CASE WHEN is_won = 1 THEN probability END) | [{"table": "salesforce__opportunity_enhanced", "column": "probability"}] | [{"table": "salesforce__opportunity_enhanced", "column": "is_won"}] | False |
| B1 | AVG(CASE WHEN is_won = 1 THEN days_to_close END) | [{"table": "salesforce__opportunity_enhanced", "column": "days_to_close"}] | [{"table": "salesforce__opportunity_enhanced", "column": "is_won"}] | False |
| B1 | AVG(probability) | [{"table": "salesforce__opportunity_enhanced", "column": "probability"}] | [] | False |
| B1 | AVG(days_to_close) | [{"table": "salesforce__opportunity_enhanced", "column": "days_to_close"}] | [] | False |


## S54

类别 `data`；来源 `python`；调用 `6cd4574adad94a42826732d947a4d244`；状态 `success`。

```sql

    SELECT billing_state AS state, COUNT(DISTINCT owner_id) AS n_reps
    FROM salesforce__account_daily_history
    WHERE billing_state IS NOT NULL
    GROUP BY billing_state

```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-088/attempt-01/sql/S54.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-088/attempt-01/sql/S54.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-088/attempt-01/results/S54.rows.jsonl)；完整：True；SHA256：`8e059489197fa2f49e7f6bea9899d2a951ddccf2d0787aced6bdae3a2d514cf2`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "salesforce__account_daily_history", "kind": "base", "block": null, "base_tables": ["salesforce__account_daily_history"]}] | [] | ["billing_state"] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(DISTINCT owner_id) | [{"table": "salesforce__account_daily_history", "column": "owner_id"}] | [] | False |


## S55

类别 `data`；来源 `python`；调用 `6cd4574adad94a42826732d947a4d244`；状态 `success`。

```sql

    SELECT state_name AS state, population, gdp_billion, gdp_per_capita,
           primary_industry, secondary_industry, tertiary_industry, quaternary_industry,
           market_maturity_score, competition_intensity, business_friendly_index,
           unemployment_rate, corporate_tax_rate
    FROM state_economic_data

```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-088/attempt-01/sql/S55.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-088/attempt-01/sql/S55.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-088/attempt-01/results/S55.rows.jsonl)；完整：True；SHA256：`45a0b785cdac40ac4d5d510d30cad822c81ddaa6a0ecaecfb19f2af1d2184f0e`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "state_economic_data", "kind": "base", "block": null, "base_tables": ["state_economic_data"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |


## S56

类别 `data`；来源 `query_db`；调用 `aa673b64973c4adca7dbc0d2cd9d9e86`；状态 `success`。

```sql
SELECT type, COUNT(*) AS n, SUM(is_won) AS won FROM salesforce__opportunity_enhanced GROUP BY type ORDER BY n DESC
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-088/attempt-01/sql/S56.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-088/attempt-01/sql/S56.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-088/attempt-01/results/S56.rows.jsonl)；完整：True；SHA256：`3ab76b4e5e4f0a2d0c9cc8501021518c319a0bc8108e0f00bbd08e9b88fd94ae`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "salesforce__opportunity_enhanced", "kind": "base", "block": null, "base_tables": ["salesforce__opportunity_enhanced"]}] | [] | ["type"] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |
| B1 | SUM(is_won) | [{"table": "salesforce__opportunity_enhanced", "column": "is_won"}] | [] | False |


## S57

类别 `data`；来源 `query_db`；调用 `325407ca1d6b43daa205d196fba39367`；状态 `success`。

```sql
-- Distribution of account_source
SELECT account_source, COUNT(*) AS n FROM salesforce__account_daily_history WHERE type='Customer' GROUP BY account_source ORDER BY n DESC
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-088/attempt-01/sql/S57.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-088/attempt-01/sql/S57.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-088/attempt-01/results/S57.rows.jsonl)；完整：True；SHA256：`5dcf82b124ae618e2e8a4c99fb80b307b77fd9b7eee44fa1ebfca95c2b17b65b`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "salesforce__account_daily_history", "kind": "base", "block": null, "base_tables": ["salesforce__account_daily_history"]}] | [] | ["account_source"] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |


## S58

类别 `data`；来源 `query_db`；调用 `968c5e60749e4943b0923d44a9469037`；状态 `success`。

```sql
-- New Business won opportunities per owner state
SELECT opportunity_owner_state AS state, COUNT(DISTINCT account_id) AS n_new_cust
FROM salesforce__opportunity_enhanced
WHERE is_won = 1 AND type = 'New Business' AND opportunity_owner_state IS NOT NULL
GROUP BY opportunity_owner_state
ORDER BY n_new_cust DESC
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-088/attempt-01/sql/S58.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-088/attempt-01/sql/S58.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-088/attempt-01/results/S58.rows.jsonl)；完整：True；SHA256：`a49b75ea98bf401f8ddbb5005ff5df912878993ab862536469d6e238578b343a`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "salesforce__opportunity_enhanced", "kind": "base", "block": null, "base_tables": ["salesforce__opportunity_enhanced"]}] | [] | ["opportunity_owner_state"] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(DISTINCT account_id) | [{"table": "salesforce__opportunity_enhanced", "column": "account_id"}] | [] | False |


## S59

类别 `data`；来源 `query_db`；调用 `4d270d82c7144f3390a0fddee30c61cd`；状态 `success`。

```sql
-- New Business won opportunities per account billing state
SELECT a.billing_state AS state, COUNT(DISTINCT a.account_id) AS n_new_cust
FROM salesforce__account_daily_history a
JOIN salesforce__opportunity_enhanced o ON a.account_id = o.account_id
WHERE o.is_won = 1 AND o.type = 'New Business' AND a.billing_state IS NOT NULL
GROUP BY a.billing_state
ORDER BY n_new_cust DESC
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-088/attempt-01/sql/S59.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-088/attempt-01/sql/S59.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-088/attempt-01/results/S59.rows.jsonl)；完整：True；SHA256：`c9cc87b59d82331af13d632736194cef209b7458e8f07e847a70a55217c8abba`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "a", "kind": "base", "block": null, "base_tables": ["salesforce__account_daily_history"]}, {"alias": "o", "kind": "base", "block": null, "base_tables": ["salesforce__opportunity_enhanced"]}] | [{"type": "INNER", "right": "salesforce__opportunity_enhanced AS o", "on": "a.account_id = o.account_id", "using": []}] | ["a.billing_state"] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(DISTINCT a.account_id) | [{"table": "salesforce__account_daily_history", "column": "account_id"}] | [] | False |


## S60

类别 `data`；来源 `python`；调用 `11ce5da070fe4dd184669133a4c8f78c`；状态 `success`。

```sql

    SELECT billing_state AS state, annual_revenue
    FROM salesforce__account_daily_history
    WHERE type='Customer' AND billing_state IS NOT NULL

```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-088/attempt-01/sql/S60.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-088/attempt-01/sql/S60.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-088/attempt-01/results/S60.rows.jsonl)；完整：True；SHA256：`6971ff02f488c657a44ddcafdab1fb9adb7454cc8dbf87c193dcab8bd0ba277a`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "salesforce__account_daily_history", "kind": "base", "block": null, "base_tables": ["salesforce__account_daily_history"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |


## S61

类别 `data`；来源 `python`；调用 `11ce5da070fe4dd184669133a4c8f78c`；状态 `success`。

```sql

    SELECT billing_state AS state, COUNT(DISTINCT account_id) AS n_customers,
           AVG(annual_revenue) AS avg_revenue, SUM(annual_revenue) AS total_revenue
    FROM salesforce__account_daily_history
    WHERE type='Customer' AND billing_state IS NOT NULL
    GROUP BY billing_state

```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-088/attempt-01/sql/S61.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-088/attempt-01/sql/S61.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-088/attempt-01/results/S61.rows.jsonl)；完整：True；SHA256：`8eeb616f67786fea0fbc379aee8c48cba0bf0304ca1a5462156f265b9c049476`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "salesforce__account_daily_history", "kind": "base", "block": null, "base_tables": ["salesforce__account_daily_history"]}] | [] | ["billing_state"] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(DISTINCT account_id) | [{"table": "salesforce__account_daily_history", "column": "account_id"}] | [] | False |
| B1 | AVG(annual_revenue) | [{"table": "salesforce__account_daily_history", "column": "annual_revenue"}] | [] | False |
| B1 | SUM(annual_revenue) | [{"table": "salesforce__account_daily_history", "column": "annual_revenue"}] | [] | False |


## S62

类别 `data`；来源 `python`；调用 `11ce5da070fe4dd184669133a4c8f78c`；状态 `success`。

```sql

    SELECT a.billing_state AS state, COUNT(DISTINCT a.account_id) AS n_new_customers
    FROM salesforce__account_daily_history a
    JOIN salesforce__opportunity_enhanced o ON a.account_id = o.account_id
    WHERE o.is_won = 1 AND o.type = 'New Business' AND a.billing_state IS NOT NULL
    GROUP BY a.billing_state

```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-088/attempt-01/sql/S62.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-088/attempt-01/sql/S62.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-088/attempt-01/results/S62.rows.jsonl)；完整：True；SHA256：`ad9932adb612b4191c4faa590981d74b51ff1e169ba81b702a3d47bca9afa53f`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "a", "kind": "base", "block": null, "base_tables": ["salesforce__account_daily_history"]}, {"alias": "o", "kind": "base", "block": null, "base_tables": ["salesforce__opportunity_enhanced"]}] | [{"type": "INNER", "right": "salesforce__opportunity_enhanced AS o", "on": "a.account_id = o.account_id", "using": []}] | ["a.billing_state"] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(DISTINCT a.account_id) | [{"table": "salesforce__account_daily_history", "column": "account_id"}] | [] | False |


## S63

类别 `data`；来源 `python`；调用 `11ce5da070fe4dd184669133a4c8f78c`；状态 `success`。

```sql

    SELECT billing_state AS state, industry, COUNT(DISTINCT account_id) AS n_cust_industry
    FROM salesforce__account_daily_history
    WHERE type='Customer' AND billing_state IS NOT NULL
    GROUP BY billing_state, industry

```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-088/attempt-01/sql/S63.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-088/attempt-01/sql/S63.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-088/attempt-01/results/S63.rows.jsonl)；完整：True；SHA256：`e96b2fe3b633ae2e7bf5303ccecceeefd94fa1118d3fc278dbb12aa4d7f942e5`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "salesforce__account_daily_history", "kind": "base", "block": null, "base_tables": ["salesforce__account_daily_history"]}] | [] | ["billing_state", "industry"] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(DISTINCT account_id) | [{"table": "salesforce__account_daily_history", "column": "account_id"}] | [] | False |


## S64

类别 `data`；来源 `python`；调用 `11ce5da070fe4dd184669133a4c8f78c`；状态 `success`。

```sql

    SELECT opportunity_owner_state AS state,
           COUNT(*) AS n_opps, SUM(is_won) AS won_opps,
           AVG(CASE WHEN is_won=1 THEN amount END) AS avg_won_amount,
           AVG(CASE WHEN is_won=1 THEN probability END) AS avg_won_prob,
           AVG(CASE WHEN is_won=1 THEN days_to_close END) AS avg_won_cycle_days,
           AVG(probability) AS avg_probability,
           AVG(days_to_close) AS avg_cycle_days
    FROM salesforce__opportunity_enhanced
    WHERE opportunity_owner_state IS NOT NULL
    GROUP BY opportunity_owner_state

```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-088/attempt-01/sql/S64.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-088/attempt-01/sql/S64.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-088/attempt-01/results/S64.rows.jsonl)；完整：True；SHA256：`0dd48343036e0ba3e05dac1f34760f3b5d9a11a4fdeba42a9ca53c064efe83ab`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "salesforce__opportunity_enhanced", "kind": "base", "block": null, "base_tables": ["salesforce__opportunity_enhanced"]}] | [] | ["opportunity_owner_state"] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |
| B1 | SUM(is_won) | [{"table": "salesforce__opportunity_enhanced", "column": "is_won"}] | [] | False |
| B1 | AVG(CASE WHEN is_won = 1 THEN amount END) | [{"table": "salesforce__opportunity_enhanced", "column": "amount"}] | [{"table": "salesforce__opportunity_enhanced", "column": "is_won"}] | False |
| B1 | AVG(CASE WHEN is_won = 1 THEN probability END) | [{"table": "salesforce__opportunity_enhanced", "column": "probability"}] | [{"table": "salesforce__opportunity_enhanced", "column": "is_won"}] | False |
| B1 | AVG(CASE WHEN is_won = 1 THEN days_to_close END) | [{"table": "salesforce__opportunity_enhanced", "column": "days_to_close"}] | [{"table": "salesforce__opportunity_enhanced", "column": "is_won"}] | False |
| B1 | AVG(probability) | [{"table": "salesforce__opportunity_enhanced", "column": "probability"}] | [] | False |
| B1 | AVG(days_to_close) | [{"table": "salesforce__opportunity_enhanced", "column": "days_to_close"}] | [] | False |


## S65

类别 `data`；来源 `python`；调用 `11ce5da070fe4dd184669133a4c8f78c`；状态 `success`。

```sql

    SELECT billing_state AS state, COUNT(DISTINCT owner_id) AS n_reps
    FROM salesforce__account_daily_history
    WHERE billing_state IS NOT NULL
    GROUP BY billing_state

```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-088/attempt-01/sql/S65.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-088/attempt-01/sql/S65.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-088/attempt-01/results/S65.rows.jsonl)；完整：True；SHA256：`8e059489197fa2f49e7f6bea9899d2a951ddccf2d0787aced6bdae3a2d514cf2`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "salesforce__account_daily_history", "kind": "base", "block": null, "base_tables": ["salesforce__account_daily_history"]}] | [] | ["billing_state"] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(DISTINCT owner_id) | [{"table": "salesforce__account_daily_history", "column": "owner_id"}] | [] | False |


## S66

类别 `data`；来源 `python`；调用 `11ce5da070fe4dd184669133a4c8f78c`；状态 `success`。

```sql

    SELECT state_name AS state, population, gdp_billion, gdp_per_capita,
           primary_industry, secondary_industry, tertiary_industry, quaternary_industry,
           market_maturity_score, competition_intensity, business_friendly_index,
           unemployment_rate, corporate_tax_rate
    FROM state_economic_data

```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-088/attempt-01/sql/S66.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-088/attempt-01/sql/S66.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-088/attempt-01/results/S66.rows.jsonl)；完整：True；SHA256：`45a0b785cdac40ac4d5d510d30cad822c81ddaa6a0ecaecfb19f2af1d2184f0e`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "state_economic_data", "kind": "base", "block": null, "base_tables": ["state_economic_data"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |


## S67

类别 `data`；来源 `python`；调用 `365ea467277e4d92b004d6772e804de2`；状态 `success`。

```sql
SELECT billing_state AS state, annual_revenue FROM salesforce__account_daily_history WHERE type='Customer' AND billing_state IS NOT NULL
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-088/attempt-01/sql/S67.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-088/attempt-01/sql/S67.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-088/attempt-01/results/S67.rows.jsonl)；完整：True；SHA256：`6971ff02f488c657a44ddcafdab1fb9adb7454cc8dbf87c193dcab8bd0ba277a`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "salesforce__account_daily_history", "kind": "base", "block": null, "base_tables": ["salesforce__account_daily_history"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |


## S68

类别 `data`；来源 `python`；调用 `365ea467277e4d92b004d6772e804de2`；状态 `success`。

```sql
SELECT billing_state AS state, COUNT(DISTINCT account_id) AS n_customers, AVG(annual_revenue) AS avg_revenue, SUM(annual_revenue) AS total_revenue FROM salesforce__account_daily_history WHERE type='Customer' AND billing_state IS NOT NULL GROUP BY billing_state
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-088/attempt-01/sql/S68.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-088/attempt-01/sql/S68.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-088/attempt-01/results/S68.rows.jsonl)；完整：True；SHA256：`8eeb616f67786fea0fbc379aee8c48cba0bf0304ca1a5462156f265b9c049476`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "salesforce__account_daily_history", "kind": "base", "block": null, "base_tables": ["salesforce__account_daily_history"]}] | [] | ["billing_state"] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(DISTINCT account_id) | [{"table": "salesforce__account_daily_history", "column": "account_id"}] | [] | False |
| B1 | AVG(annual_revenue) | [{"table": "salesforce__account_daily_history", "column": "annual_revenue"}] | [] | False |
| B1 | SUM(annual_revenue) | [{"table": "salesforce__account_daily_history", "column": "annual_revenue"}] | [] | False |


## S69

类别 `data`；来源 `python`；调用 `365ea467277e4d92b004d6772e804de2`；状态 `success`。

```sql

    SELECT a.billing_state AS state, COUNT(DISTINCT a.account_id) AS n_new_customers
    FROM salesforce__account_daily_history a JOIN salesforce__opportunity_enhanced o ON a.account_id = o.account_id
    WHERE o.is_won = 1 AND o.type = 'New Business' AND a.billing_state IS NOT NULL
    GROUP BY a.billing_state
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-088/attempt-01/sql/S69.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-088/attempt-01/sql/S69.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-088/attempt-01/results/S69.rows.jsonl)；完整：True；SHA256：`ad9932adb612b4191c4faa590981d74b51ff1e169ba81b702a3d47bca9afa53f`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "a", "kind": "base", "block": null, "base_tables": ["salesforce__account_daily_history"]}, {"alias": "o", "kind": "base", "block": null, "base_tables": ["salesforce__opportunity_enhanced"]}] | [{"type": "INNER", "right": "salesforce__opportunity_enhanced AS o", "on": "a.account_id = o.account_id", "using": []}] | ["a.billing_state"] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(DISTINCT a.account_id) | [{"table": "salesforce__account_daily_history", "column": "account_id"}] | [] | False |


## S70

类别 `data`；来源 `python`；调用 `365ea467277e4d92b004d6772e804de2`；状态 `success`。

```sql
SELECT billing_state AS state, industry, COUNT(DISTINCT account_id) AS n_cust_industry FROM salesforce__account_daily_history WHERE type='Customer' AND billing_state IS NOT NULL GROUP BY billing_state, industry
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-088/attempt-01/sql/S70.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-088/attempt-01/sql/S70.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-088/attempt-01/results/S70.rows.jsonl)；完整：True；SHA256：`e96b2fe3b633ae2e7bf5303ccecceeefd94fa1118d3fc278dbb12aa4d7f942e5`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "salesforce__account_daily_history", "kind": "base", "block": null, "base_tables": ["salesforce__account_daily_history"]}] | [] | ["billing_state", "industry"] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(DISTINCT account_id) | [{"table": "salesforce__account_daily_history", "column": "account_id"}] | [] | False |


## S71

类别 `data`；来源 `python`；调用 `365ea467277e4d92b004d6772e804de2`；状态 `success`。

```sql

    SELECT opportunity_owner_state AS state, COUNT(*) AS n_opps, SUM(is_won) AS won_opps,
           AVG(CASE WHEN is_won=1 THEN amount END) AS avg_won_amount,
           AVG(CASE WHEN is_won=1 THEN probability END) AS avg_won_prob,
           AVG(CASE WHEN is_won=1 THEN days_to_close END) AS avg_won_cycle_days,
           AVG(probability) AS avg_probability, AVG(days_to_close) AS avg_cycle_days
    FROM salesforce__opportunity_enhanced WHERE opportunity_owner_state IS NOT NULL
    GROUP BY opportunity_owner_state
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-088/attempt-01/sql/S71.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-088/attempt-01/sql/S71.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-088/attempt-01/results/S71.rows.jsonl)；完整：True；SHA256：`0dd48343036e0ba3e05dac1f34760f3b5d9a11a4fdeba42a9ca53c064efe83ab`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "salesforce__opportunity_enhanced", "kind": "base", "block": null, "base_tables": ["salesforce__opportunity_enhanced"]}] | [] | ["opportunity_owner_state"] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |
| B1 | SUM(is_won) | [{"table": "salesforce__opportunity_enhanced", "column": "is_won"}] | [] | False |
| B1 | AVG(CASE WHEN is_won = 1 THEN amount END) | [{"table": "salesforce__opportunity_enhanced", "column": "amount"}] | [{"table": "salesforce__opportunity_enhanced", "column": "is_won"}] | False |
| B1 | AVG(CASE WHEN is_won = 1 THEN probability END) | [{"table": "salesforce__opportunity_enhanced", "column": "probability"}] | [{"table": "salesforce__opportunity_enhanced", "column": "is_won"}] | False |
| B1 | AVG(CASE WHEN is_won = 1 THEN days_to_close END) | [{"table": "salesforce__opportunity_enhanced", "column": "days_to_close"}] | [{"table": "salesforce__opportunity_enhanced", "column": "is_won"}] | False |
| B1 | AVG(probability) | [{"table": "salesforce__opportunity_enhanced", "column": "probability"}] | [] | False |
| B1 | AVG(days_to_close) | [{"table": "salesforce__opportunity_enhanced", "column": "days_to_close"}] | [] | False |


## S72

类别 `data`；来源 `python`；调用 `365ea467277e4d92b004d6772e804de2`；状态 `success`。

```sql
SELECT billing_state AS state, COUNT(DISTINCT owner_id) AS n_reps FROM salesforce__account_daily_history WHERE billing_state IS NOT NULL GROUP BY billing_state
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-088/attempt-01/sql/S72.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-088/attempt-01/sql/S72.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-088/attempt-01/results/S72.rows.jsonl)；完整：True；SHA256：`8e059489197fa2f49e7f6bea9899d2a951ddccf2d0787aced6bdae3a2d514cf2`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "salesforce__account_daily_history", "kind": "base", "block": null, "base_tables": ["salesforce__account_daily_history"]}] | [] | ["billing_state"] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(DISTINCT owner_id) | [{"table": "salesforce__account_daily_history", "column": "owner_id"}] | [] | False |


## S73

类别 `data`；来源 `python`；调用 `365ea467277e4d92b004d6772e804de2`；状态 `success`。

```sql
SELECT state_name AS state, population, gdp_billion, gdp_per_capita, primary_industry, secondary_industry, tertiary_industry, quaternary_industry, market_maturity_score, competition_intensity, business_friendly_index, unemployment_rate, corporate_tax_rate FROM state_economic_data
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-088/attempt-01/sql/S73.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-088/attempt-01/sql/S73.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-088/attempt-01/results/S73.rows.jsonl)；完整：True；SHA256：`45a0b785cdac40ac4d5d510d30cad822c81ddaa6a0ecaecfb19f2af1d2184f0e`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "state_economic_data", "kind": "base", "block": null, "base_tables": ["state_economic_data"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |


## S74

类别 `data`；来源 `python`；调用 `365ea467277e4d92b004d6772e804de2`；状态 `success`。

```sql

    SELECT opportunity_owner_state AS state,
           AVG(CASE WHEN is_won=1 THEN amount END) AS avg_won_amount,
           AVG(probability) AS avg_probability,
           AVG(CASE WHEN is_won=1 THEN days_to_close END) AS avg_won_cycle,
           SUM(is_won)*1.0/COUNT(*) AS win_rate
    FROM salesforce__opportunity_enhanced
    WHERE opportunity_owner_state IN ('New York','California','Oregon')
    GROUP BY opportunity_owner_state
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-088/attempt-01/sql/S74.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-088/attempt-01/sql/S74.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-088/attempt-01/results/S74.rows.jsonl)；完整：True；SHA256：`1e1cd2078ca0490c69acde7ecddfd56303045ee222154efbd92f856b9890ac5b`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "salesforce__opportunity_enhanced", "kind": "base", "block": null, "base_tables": ["salesforce__opportunity_enhanced"]}] | [] | ["opportunity_owner_state"] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | AVG(CASE WHEN is_won = 1 THEN amount END) | [{"table": "salesforce__opportunity_enhanced", "column": "amount"}] | [{"table": "salesforce__opportunity_enhanced", "column": "is_won"}] | False |
| B1 | AVG(probability) | [{"table": "salesforce__opportunity_enhanced", "column": "probability"}] | [] | False |
| B1 | AVG(CASE WHEN is_won = 1 THEN days_to_close END) | [{"table": "salesforce__opportunity_enhanced", "column": "days_to_close"}] | [{"table": "salesforce__opportunity_enhanced", "column": "is_won"}] | False |
| B1 | COUNT(*) | [] | [] | True |
| B1 | SUM(is_won) | [{"table": "salesforce__opportunity_enhanced", "column": "is_won"}] | [] | False |


## S75

类别 `data`；来源 `python`；调用 `07ae3897f0d04350b2cd3b1363385567`；状态 `success`。

```sql

    SELECT industry, COUNT(DISTINCT account_id) AS n
    FROM salesforce__account_daily_history WHERE type='Customer'
    GROUP BY industry ORDER BY n DESC LIMIT 8

```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-088/attempt-01/sql/S75.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-088/attempt-01/sql/S75.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-088/attempt-01/results/S75.rows.jsonl)；完整：True；SHA256：`0b080626e9af5aab6a38a5e11868d548e5a9480cfa28737f4598e809ac910c8a`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "salesforce__account_daily_history", "kind": "base", "block": null, "base_tables": ["salesforce__account_daily_history"]}] | [] | ["industry"] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(DISTINCT account_id) | [{"table": "salesforce__account_daily_history", "column": "account_id"}] | [] | False |

