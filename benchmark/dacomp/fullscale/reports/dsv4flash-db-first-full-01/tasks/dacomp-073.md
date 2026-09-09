# dacomp-073

Given the rapid business growth, we need to forecast future hiring demand and resource all…

运行：已提交。官方未评分。全部 SQL 尝试/成功 97/94；数据 SQL 95/92；Python 8 次。

完整原题：

Given the rapid business growth, we need to forecast future hiring demand and resource allocation. Based on historical data from the `lever__posting_enhanced` and `lever__requisition_enhanced` tables, analyze the trend in the number of postings and the month-over-month (MoM) growth rate for each team over the past 6 months. Identify high-growth teams with a month-over-month demand growth rate exceeding 15% AND more than 10 current active postings. Calculate their 'Hiring Pressure Index,' defined as: (Number of pending roles / Number of existing hiring managers). Predict which teams are likely to face a resource shortage in the next 2 months, where their pressure index might exceed 8, and calculate how many additional recruiting resources are needed (based on a capacity of one hiring manager handling a maximum of 6 postings simultaneously).

| 表 | 行数 | 列数 |
| --- | --- | --- |
| lever__posting_enhanced | 300 | 29 |
| lever__requisition_enhanced | 200 | 26 |


实际路线（分析者依据 SQL/源码概括，不代表 Agent 自述）：SQL 探查岗位、编制与经理及月趋势 → Python 再聚合部门需求和经理容量 → 招聘压力与资源预测。

数据库大小：618,496 字节。

## 数据 SQL

| SQL | 状态 | 基础表 | Join 输入/类型 | GROUP BY | 聚合表达式 | 结果行数 | 数据库 ms |
| --- | --- | --- | --- | --- | --- | --- | --- |
| [S3/Q1](#s3) | success | ["lever__posting_enhanced"] | 0 / {} | [] | ["MIN(created_at)", "MAX(created_at)", "COUNT(*)"] | 1 | 0.784 |
| [S4/Q2](#s4) | success | ["lever__requisition_enhanced"] | 0 / {} | [] | ["MIN(created_at)", "MAX(created_at)", "COUNT(*)"] | 1 | 0.436 |
| [S5/Q3](#s5) | success | ["lever__posting_enhanced"] | 0 / {} | [] | [] | 4 | 0.471 |
| [S6/Q4](#s6) | success | ["lever__requisition_enhanced"] | 0 / {} | [] | [] | 4 | 0.371 |
| [S7/Q5](#s7) | success | ["lever__posting_enhanced"] | 0 / {} | [] | ["MIN(updated_at)", "MAX(updated_at)"] | 1 | 0.459 |
| [S8/Q6](#s8) | success | ["lever__posting_enhanced"] | 0 / {} | ["state"] | ["COUNT(*)"] | 4 | 0.502 |
| [S9/Q7](#s9) | success | ["lever__requisition_enhanced"] | 0 / {} | ["status"] | ["COUNT(*)"] | 4 | 0.395 |
| [S10/Q8](#s10) | success | ["lever__posting_enhanced"] | 0 / {} | ["categories_team"] | ["COUNT(*)"] | 295 | 0.814 |
| [S11/Q9](#s11) | success | ["lever__requisition_enhanced"] | 0 / {} | ["team"] | ["COUNT(*)"] | 200 | 0.591 |
| [S12/Q10](#s12) | success | ["lever__posting_enhanced"] | 0 / {} | ["categories_department"] | ["COUNT(*)"] | 6 | 0.481 |
| [S13/Q11](#s13) | success | ["lever__posting_enhanced"] | 0 / {} | ["categories_level"] | ["COUNT(*)"] | 6 | 0.472 |
| [S14/Q12](#s14) | success | ["lever__posting_enhanced"] | 0 / {} | ["categories_location"] | ["COUNT(*)"] | 300 | 0.729 |
| [S15/Q13](#s15) | success | ["lever__posting_enhanced"] | 0 / {} | [] | [] | 20 | 0.353 |
| [S16/Q14](#s16) | success | ["lever__requisition_enhanced"] | 0 / {} | [] | [] | 20 | 0.32 |
| [S17/Q15](#s17) | success | ["lever__posting_enhanced"] | 0 / {} | ["state", "categories_department"] | ["COUNT(*)"] | 24 | 0.624 |
| [S18/Q16](#s18) | success | ["lever__posting_enhanced"] | 0 / {} | ["categories_department", "state"] | ["COUNT(*)"] | 24 | 0.604 |
| [S19/Q17](#s19) | success | ["lever__posting_enhanced"] | 0 / {} | ["categories_department"] | ["COUNT(DISTINCT posting_hiring_manager_name)"] | 6 | 0.643 |
| [S20/Q18](#s20) | success | ["lever__posting_enhanced"] | 0 / {} | ["STRFTIME('%Y-%m', created_at)", "categories_department"] | ["COUNT(*)"] | 6 | 0.625 |
| [S21/Q19](#s21) | success | ["lever__posting_enhanced"] | 0 / {} | ["STRFTIME('%Y-%m', created_at)"] | ["COUNT(*)"] | 1 | 0.603 |
| [S22/Q20](#s22) | success | ["lever__posting_enhanced"] | 0 / {} | [] | [] | 10 | 0.323 |
| [S23/Q21](#s23) | success | ["lever__posting_enhanced"] | 0 / {} | [] | [] | 10 | 0.298 |
| [S24/Q22](#s24) | success | ["lever__posting_enhanced"] | 0 / {} | ["SUBSTRING(created_at, 1, 7)", "categories_department"] | ["COUNT(*)"] | 24 | 0.713 |
| [S25/Q23](#s25) | success | ["lever__posting_enhanced"] | 0 / {} | ["SUBSTRING(created_at, 1, 7)"] | ["COUNT(*)"] | 4 | 0.515 |
| [S26/Q24](#s26) | success | ["lever__requisition_enhanced"] | 0 / {} | ["SUBSTRING(created_at, 1, 7)"] | ["COUNT(*)"] | 6 | 0.631 |
| [S27/Q25](#s27) | success | ["lever__requisition_enhanced"] | 0 / {} | ["SUBSTRING(created_at, 1, 7)", "team"] | ["COUNT(*)"] | 200 | 0.814 |
| [S28/Q26](#s28) | success | ["lever__requisition_enhanced"] | 0 / {} | [] | [] | 15 | 0.371 |
| [S29/Q27](#s29) | success | ["lever__posting_enhanced"] | 0 / {} | ["requisition_code"] | ["COUNT(*)"] | 15 | 0.735 |
| [S30/Q28](#s30) | success | ["lever__posting_enhanced"] | 0 / {} | ["has_requisition"] | ["COUNT(*)"] | 1 | 0.478 |
| [S31/Q29](#s31) | success | ["lever__requisition_enhanced"] | 0 / {} | ["has_posting"] | ["COUNT(*)"] | 2 | 0.425 |
| [S32/Q30](#s32) | success | ["lever__posting_enhanced", "lever__requisition_enhanced"] | 2 / {'INNER': 1} | [] | [] | 5 | 0.745 |
| [S33/Q31](#s33) | success | ["lever__posting_enhanced"] | 0 / {} | ["categories_department", "SUBSTRING(created_at, 1, 7)"] | ["COUNT(*)"] | 24 | 0.625 |
| [S34/Q32](#s34) | success | ["lever__posting_enhanced"] | 0 / {} | ["categories_department", "SUBSTRING(created_at, 1, 7)"] | ["COUNT(*)"] | 22 | 0.626 |
| [S35/Q33](#s35) | success | ["lever__posting_enhanced"] | 0 / {} | ["categories_department", "state"] | ["COUNT(*)"] | 24 | 0.611 |
| [S36/Q34](#s36) | success | ["lever__posting_enhanced"] | 0 / {} | ["categories_department", "SUBSTRING(created_at, 1, 7)"] | ["COUNT(*)"] | 24 | 0.874 |
| [S37/Q35](#s37) | success | ["lever__posting_enhanced"] | 0 / {} | ["categories_department", "SUBSTRING(created_at, 1, 7)", "categories_department"] | ["COUNT(*)", "AVG(mom_growth)", "SUM(CASE WHEN ym = '2025-07' THEN cnt ELSE 0 END)"] | 6 | 1.004 |
| [S38/Q36](#s38) | success | ["lever__posting_enhanced"] | 0 / {} | ["categories_department"] | ["COUNT(*)"] | 6 | 0.527 |
| [S39/Q37](#s39) | success | ["lever__requisition_enhanced"] | 0 / {} | ["r.status"] | ["COUNT(*)"] | 4 | 0.418 |
| [S40/Q38](#s40) | success | ["lever__posting_enhanced", "lever__requisition_enhanced"] | 2 / {'LEFT': 1} | ["p.categories_department", "r.status"] | ["COUNT(DISTINCT r.requisition_id)"] | 9 | 0.973 |
| [S41/Q39](#s41) | success | ["lever__requisition_enhanced"] | 0 / {} | [] | [] | 20 | 0.491 |
| [S42/Q40](#s42) | success | ["lever__posting_enhanced", "lever__requisition_enhanced"] | 2 / {'INNER': 1} | [] | [] | 5 | 0.761 |
| [S43/Q41](#s43) | success | ["lever__posting_enhanced"] | 0 / {} | [] | ["COUNT(DISTINCT requisition_code)"] | 1 | 0.526 |
| [S44/Q42](#s44) | success | ["lever__requisition_enhanced"] | 0 / {} | [] | ["COUNT(DISTINCT requisition_code)"] | 1 | 0.426 |
| [S45/Q43](#s45) | success | ["lever__posting_enhanced", "lever__requisition_enhanced"] | 2 / {'INNER': 1} | [] | ["COUNT(DISTINCT p.requisition_code)"] | 1 | 0.694 |
| [S46/Q44](#s46) | success | ["lever__posting_enhanced", "lever__requisition_enhanced"] | 2 / {'INNER': 1} | [] | ["COUNT(DISTINCT r.team)"] | 1 | 0.747 |
| [S47/Q45](#s47) | success | ["lever__posting_enhanced", "lever__requisition_enhanced"] | 0 / {} | [] | ["COUNT(DISTINCT r.team)"] | 1 | 0.703 |
| [S48/Q46](#s48) | failed | ["lever__requisition_enhanced"] | 0 / {} | [] | ["COUNT(DISTINCT r.owner_name)", "COUNT(DISTINCT r.creator_name)"] | unknown | 未取得；调用总时长 0.161 ms |
| [S49/Q47](#s49) | failed | ["lever__posting_enhanced"] | 0 / {} | [] | ["COUNT(DISTINCT p.posting_hiring_manager_name)"] | unknown | 未取得；调用总时长 0.162 ms |
| [S50/Q48](#s50) | success | ["lever__posting_enhanced", "lever__requisition_enhanced"] | 0 / {} | [] | ["COUNT(*)"] | 1 | 0.755 |
| [S51/Q49](#s51) | success | ["lever__requisition_enhanced"] | 0 / {} | [] | [] | 10 | 0.338 |
| [S52/Q50](#s52) | success | ["lever__posting_enhanced"] | 0 / {} | [] | [] | 10 | 0.325 |
| [S53/Q51](#s53) | failed | ["lever__requisition_enhanced"] | 0 / {} | [] | ["COUNT(DISTINCT r.hiring_manager_user_id)"] | unknown | 未取得；调用总时长 0.172 ms |
| [S54/Q52](#s54) | success | ["lever__posting_enhanced", "lever__requisition_enhanced"] | 0 / {} | [] | ["COUNT(DISTINCT r.hiring_manager_user_id)"] | 1 | 0.944 |
| [S55/Q53](#s55) | success | ["lever__posting_enhanced", "lever__requisition_enhanced"] | 0 / {} | [] | ["COUNT(*)"] | 1 | 0.757 |
| [S56/Q54](#s56) | success | ["lever__posting_enhanced", "lever__requisition_enhanced"] | 0 / {} | [] | ["COUNT(*)"] | 1 | 0.64 |
| [S57/Q55](#s57) | success | ["lever__requisition_enhanced"] | 0 / {} | [] | ["COUNT(DISTINCT hiring_manager_user_id)"] | 1 | 0.443 |
| [S58/Q56](#s58) | success | ["lever__posting_enhanced"] | 0 / {} | ["p.categories_department"] | ["COUNT(DISTINCT p.owner_user_id)", "COUNT(DISTINCT p.creator_user_id)"] | 6 | 0.774 |
| [S59/Q57](#s59) | success | ["lever__posting_enhanced"] | 0 / {} | ["user_id"] | ["COUNT(DISTINCT categories_department)"] | 10 | 0.854 |
| [S60/Q58](#s60) | success | ["lever__posting_enhanced"] | 0 / {} | ["posting_hiring_manager_name"] | ["COUNT(DISTINCT categories_department)", "COUNT(*)"] | 15 | 0.794 |
| [S61/Q59](#s61) | success | ["lever__posting_enhanced"] | 0 / {} | ["posting_hiring_manager_name"] | ["COUNT(DISTINCT categories_department)", "COUNT(*)"] | 15 | 0.871 |
| [S62/Q60](#s62) | success | ["lever__posting_enhanced"] | 0 / {} | [] | ["COUNT(*)"] | 1 | 0.542 |
| [S63/Q61](#s63) | success | ["lever__posting_enhanced"] | 0 / {} | ["posting_hiring_manager_name"] | ["COUNT(DISTINCT categories_department)", "COUNT(*)"] | 1 | 0.699 |
| [S64/Q62](#s64) | success | ["lever__requisition_enhanced"] | 0 / {} | ["status"] | ["SUM(headcount_total)", "SUM(headcount_hired)", "SUM(CASE WHEN headcount_infinite = 1 THEN 1 ELSE 0 END)", "COUNT(*)"] | 4 | 0.49 |
| [S65/Q63](#s65) | success | ["lever__requisition_enhanced"] | 0 / {} | [] | [] | 20 | 0.35 |
| [S66/Q64](#s66) | success | ["lever__posting_enhanced"] | 0 / {} | ["posting_hiring_manager_name", "categories_department"] | ["COUNT(*)", "COUNT(*)"] | 20 | 1.343 |
| [S67/Q65](#s67) | success | ["lever__posting_enhanced"] | 0 / {} | ["owner_user_id", "categories_department", "creator_user_id", "categories_department", "user_id", "categories_department", "categories_department"] | ["COUNT(*)", "COUNT(*)", "SUM(cnt)", "SUM(cnt)", "COUNT(DISTINCT user_id)"] | 6 | 2.755 |
| [S68/Q66](#s68) | success | ["lever__posting_enhanced", "lever__requisition_enhanced"] | 2 / {'LEFT': 1} | ["owner_user_id", "categories_department", "creator_user_id", "categories_department", "user_id", "categories_department", "COALESCE(hd.categories_department, 'Unmapped')"] | ["COUNT(*)", "COUNT(*)", "SUM(cnt)", "SUM(cnt)", "COUNT(*)"] | 7 | 4.637 |
| [S69/Q67](#s69) | success | ["lever__posting_enhanced"] | 0 / {} | ["categories_department"] | ["COUNT(DISTINCT posting_hiring_manager_name)", "COUNT(*)"] | 6 | 0.608 |
| [S70/Q68](#s70) | success | ["lever__posting_enhanced"] | 0 / {} | ["categories_department"] | ["COUNT(DISTINCT posting_hiring_manager_name)", "COUNT(*)"] | 6 | 0.606 |
| [S71/Q69](#s71) | success | ["lever__posting_enhanced", "lever__requisition_enhanced"] | 2 / {'LEFT': 1} | ["owner_user_id", "categories_department", "creator_user_id", "categories_department", "user_id", "categories_department", "COALESCE(hd.categories_department, 'Unmapped')"] | ["COUNT(*)", "COUNT(*)", "SUM(cnt)", "SUM(cnt)", "COUNT(*)", "SUM(CASE WHEN r.status = 'open' THEN 1 ELSE 0 END)", "SUM(CASE WHEN r.status = 'on-hold' THEN 1 ELSE 0 END)"] | 7 | 3.273 |
| [S72/Q70](#s72) | success | ["lever__posting_enhanced"] | 0 / {} | ["categories_department"] | ["COUNT(*)", "COUNT(DISTINCT posting_hiring_manager_name)", "COUNT(DISTINCT posting_hiring_manager_name)", "COUNT(*)"] | 6 | 0.618 |
| [S73/Q71](#s73) | success | ["lever__requisition_enhanced"] | 0 / {} | ["status"] | ["SUM(count_postings)", "SUM(count_offers)"] | 4 | 0.479 |
| [S74/Q72](#s74) | success | ["lever__requisition_enhanced"] | 0 / {} | [] | [] | 15 | 0.356 |
| [S75/Q73](#s75) | success | ["lever__posting_enhanced"] | 0 / {} | ["categories_department"] | ["SUM(count_requisitions)", "SUM(count_opportunities)", "SUM(count_open_opportunities)", "SUM(count_interviews)"] | 6 | 0.586 |
| [S76/Q74](#s76) | success | ["lever__requisition_enhanced"] | 0 / {} | ["headcount_total", "headcount_hired", "headcount_infinite"] | ["COUNT(*)"] | 8 | 0.427 |
| [S77/Q75](#s77) | success | ["lever__posting_enhanced"] | 0 / {} | ["posting_hiring_manager_name", "postings_per_hm"] | ["COUNT(*)", "COUNT(*)"] | 4 | 0.758 |
| [S78/Q76](#s78) | success | ["lever__requisition_enhanced"] | 0 / {} | [] | ["SUM(headcount_total)", "SUM(headcount_hired)", "SUM(CASE WHEN headcount_infinite = 1 THEN 1 ELSE 0 END)"] | 1 | 0.401 |
| [S79/Q77](#s79) | success | ["lever__requisition_enhanced"] | 0 / {} | [] | ["SUM(headcount_total)", "SUM(headcount_hired)", "SUM(CASE WHEN headcount_infinite = 1 THEN 1 ELSE 0 END)"] | 1 | 0.404 |
| [S80/Q78](#s80) | success | ["lever__posting_enhanced"] | 0 / {} | ["categories_department", "SUBSTRING(created_at, 1, 7)"] | ["COUNT(*)"] | 24 | 0.624 |
| [S81/Q79](#s81) | success | ["lever__posting_enhanced"] | 0 / {} | ["categories_department", "SUBSTRING(created_at, 1, 7)"] | ["COUNT(*)"] | 24 | 0.628 |
| [S82/Q80](#s82) | success | ["lever__posting_enhanced", "lever__requisition_enhanced"] | 2 / {'LEFT': 1} | ["owner_user_id", "categories_department", "creator_user_id", "categories_department", "user_id", "categories_department", "COALESCE(hd.categories_department, 'Unmapped')"] | ["COUNT(*)", "COUNT(*)", "SUM(cnt)", "SUM(cnt)", "COUNT(*)", "SUM(r.count_postings)", "SUM(r.count_offers)"] | 7 | 4.519 |
| [S83/Q81](#s83) | success | ["lever__posting_enhanced", "lever__requisition_enhanced"] | 2 / {'LEFT': 1} | ["owner_user_id", "categories_department", "creator_user_id", "categories_department", "user_id", "categories_department", "COALESCE(hd.categories_department, 'Unmapped')"] | ["COUNT(*)", "COUNT(*)", "SUM(cnt)", "SUM(cnt)", "COUNT(*)", "SUM(CASE WHEN r.status = 'open' THEN 1 ELSE 0 END)", "SUM(CASE WHEN r.status = 'on-hold' THEN 1 ELSE 0 END)", "SUM(CASE WHEN r.status IN ('open', 'on-hold') THEN r.count_postings ELSE 0 END)"] | 7 | 3.174 |
| [S84/Q82](#s84) | success | ["lever__posting_enhanced"] | 0 / {} | [] | [] | 300 | 2.559 |
| [S85/Q83](#s85) | success | ["lever__requisition_enhanced"] | 0 / {} | [] | [] | 200 | 1.345 |
| [S86/Q84](#s86) | success | ["lever__posting_enhanced"] | 0 / {} | [] | [] | 300 | 2.36 |
| [S87/Q85](#s87) | success | ["lever__posting_enhanced"] | 0 / {} | ["categories_department", "state"] | ["COUNT(*)"] | 4 | 0.579 |
| [S88/Q86](#s88) | success | ["lever__posting_enhanced"] | 0 / {} | ["categories_department", "state"] | ["COUNT(*)"] | 24 | 0.511 |
| [S89/Q87](#s89) | success | ["lever__posting_enhanced"] | 0 / {} | ["categories_department", "state"] | ["COUNT(*)"] | 24 | 0.631 |
| [S90/Q88](#s90) | success | ["lever__posting_enhanced"] | 0 / {} | [] | [] | 300 | 2.338 |
| [S91/Q89](#s91) | success | ["lever__requisition_enhanced"] | 0 / {} | [] | [] | 200 | 1.232 |
| [S92/Q90](#s92) | success | ["lever__posting_enhanced"] | 0 / {} | [] | [] | 300 | 2.349 |
| [S93/Q91](#s93) | success | ["lever__requisition_enhanced"] | 0 / {} | [] | [] | 200 | 1.295 |
| [S94/Q92](#s94) | success | ["lever__posting_enhanced"] | 0 / {} | [] | [] | 300 | 2.333 |
| [S95/Q93](#s95) | success | ["lever__requisition_enhanced"] | 0 / {} | [] | [] | 200 | 1.249 |
| [S96/Q94](#s96) | success | ["lever__posting_enhanced"] | 0 / {} | [] | [] | 300 | 2.519 |
| [S97/Q95](#s97) | success | ["lever__requisition_enhanced"] | 0 / {} | [] | [] | 200 | 1.259 |


## 元数据和设置

| SQL | 类别 | 状态 | 内容 |
| --- | --- | --- | --- |
| S1 | connection_setup | success | PRAGMA query_only=ON |
| S2 | metadata | success | SELECT name,sql FROM sqlite_master WHERE type='table' ORDER BY name |


## Python 与执行位置

人工源码审查：**database_first_violation**。Python 重新按部门和月份计数、统计去重招聘经理、求和未结机会及岗位需求，并整理增长率和压力预测输入。这些筛选、去重和分组聚合可在 SQL 完成，存在明确的数据库优先偏离。 [证据](../reviews/dacomp-073.json)。

P1：Fetching the full monthly posting data per department to analyze trends and compute MoM growth rates

[源码](../../../runs/dsv4flash-db-first-full-01/dacomp-073/attempt-01/python/P1.py)；[输出](../../../runs/dsv4flash-db-first-full-01/dacomp-073/attempt-01/python/P1.stdout)；[错误](../../../runs/dsv4flash-db-first-full-01/dacomp-073/attempt-01/python/P1.stderr)。检出需人工核验的 SQL 可实现操作：.query(；不能仅凭理由判为合规。

P2：Comprehensive data exploration to understand the relationship between posting and requisition tables, and compute all metrics needed for the task

[源码](../../../runs/dsv4flash-db-first-full-01/dacomp-073/attempt-01/python/P2.py)；[输出](../../../runs/dsv4flash-db-first-full-01/dacomp-073/attempt-01/python/P2.stdout)；[错误](../../../runs/dsv4flash-db-first-full-01/dacomp-073/attempt-01/python/P2.stderr)。检出需人工核验的 SQL 可实现操作：groupby(, .query(；不能仅凭理由判为合规。

P3：Exploring the opportunity/application count fields to understand if they can serve as 'pending roles' metrics for the Hiring Pressure Index

[源码](../../../runs/dsv4flash-db-first-full-01/dacomp-073/attempt-01/python/P3.py)；[输出](../../../runs/dsv4flash-db-first-full-01/dacomp-073/attempt-01/python/P3.stdout)；[错误](../../../runs/dsv4flash-db-first-full-01/dacomp-073/attempt-01/python/P3.stderr)。检出需人工核验的 SQL 可实现操作：groupby(, .query(；不能仅凭理由判为合规。

P4：Fetching full state distribution per department to accurately compute pending roles and active postings for the Hiring Pressure Index analysis

[源码](../../../runs/dsv4flash-db-first-full-01/dacomp-073/attempt-01/python/P4.py)；[输出](../../../runs/dsv4flash-db-first-full-01/dacomp-073/attempt-01/python/P4.stdout)；[错误](../../../runs/dsv4flash-db-first-full-01/dacomp-073/attempt-01/python/P4.stderr)。检出需人工核验的 SQL 可实现操作：.query(；不能仅凭理由判为合规。

P5：Building the complete Hiring Demand Forecast analysis. Computing MoM growth rates, identifying high-growth teams, calculating Hiring Pressure Index, and predicting future resource shortages.

[源码](../../../runs/dsv4flash-db-first-full-01/dacomp-073/attempt-01/python/P5.py)；[输出](../../../runs/dsv4flash-db-first-full-01/dacomp-073/attempt-01/python/P5.stdout)；[错误](../../../runs/dsv4flash-db-first-full-01/dacomp-073/attempt-01/python/P5.stderr)。检出需人工核验的 SQL 可实现操作：groupby(, .query(；不能仅凭理由判为合规。

P6：Evaluating alternative mapping of requisitions to departments via owner_name matching posting hiring manager names, to see if open requisitions can serve as 'pending roles' per department

[源码](../../../runs/dsv4flash-db-first-full-01/dacomp-073/attempt-01/python/P6.py)；[输出](../../../runs/dsv4flash-db-first-full-01/dacomp-073/attempt-01/python/P6.stdout)；[错误](../../../runs/dsv4flash-db-first-full-01/dacomp-073/attempt-01/python/P6.stderr)。检出需人工核验的 SQL 可实现操作：groupby(, .query(, sort_values(；不能仅凭理由判为合规。

P7：Exploring requisition monthly trends and alternative definitions of 'pending roles' to find a coherent interpretation where the pressure index can exceed 8 under projected growth

[源码](../../../runs/dsv4flash-db-first-full-01/dacomp-073/attempt-01/python/P7.py)；[输出](../../../runs/dsv4flash-db-first-full-01/dacomp-073/attempt-01/python/P7.stdout)；[错误](../../../runs/dsv4flash-db-first-full-01/dacomp-073/attempt-01/python/P7.stderr)。检出需人工核验的 SQL 可实现操作：groupby(, .query(, sort_values(；不能仅凭理由判为合规。

P8：Building the final comprehensive analysis with all metrics, visualizations, and forecasts. Using count_open_opportunities as the 'pending roles' metric (representing hiring workload/candidates in pipeline per hiring manager) as it's the only interpretation that yields a meaningful pressure index forecast.

[源码](../../../runs/dsv4flash-db-first-full-01/dacomp-073/attempt-01/python/P8.py)；[输出](../../../runs/dsv4flash-db-first-full-01/dacomp-073/attempt-01/python/P8.stdout)；[错误](../../../runs/dsv4flash-db-first-full-01/dacomp-073/attempt-01/python/P8.stderr)。检出需人工核验的 SQL 可实现操作：groupby(, .query(；不能仅凭理由判为合规。

## 优化机会

已验证候选。筛选限于精确 SQL、相同自包含 CTE、相同单表完整过滤、可分解单表聚合；未覆盖任意 Join 等价和一般谓词蕴含。全部候选都是 offline，未测在线预测。

| 候选 | 类型 | 已有结果 | 覆盖 SQL | 后续次数 | 中间行数 | 验证 | 成本 |
| --- | --- | --- | --- | --- | --- | --- | --- |
| C1 | exact-result reuse | True | ["S33", "S80", "S81"] | 2 | unknown | not_verified_cap | Not tested |
| C2 | exact-result reuse | True | ["S35", "S88", "S89"] | 2 | unknown | not_verified_cap | Not tested |
| C3 | exact-result reuse | True | ["S84", "S86", "S90", "S92", "S94", "S96"] | 5 | 300 | verified | Not benchmarked; correctness alone does not establish net speedup. |
| C4 | exact-result reuse | True | ["S85", "S91", "S93", "S95", "S97"] | 4 | unknown | not_verified_cap | Not tested |
| C5 | common subexpression | False | ["S36", "S37"] | 1 | unknown | not_verified_cap | Not tested |
| C6 | common subexpression | False | ["S67", "S68", "S71", "S82", "S83"] | 4 | unknown | not_verified_cap | Not tested |
| C7 | aggregate MV | False | ["S3", "S7", "S8", "S10", "S12", "S13", "S14", "S17", "S18", "S20", "S21", "S24", "S25", "S29", "S30", "S33", "S35", "S75", "S80", "S81", "S88", "S89"] | 21 | 300 | verified | Not benchmarked; correctness alone does not establish net speedup. |
| C8 | aggregate MV | False | ["S4", "S9", "S11", "S26", "S27", "S31", "S39", "S64", "S73", "S78"] | 9 | 200 | verified | Not benchmarked; correctness alone does not establish net speedup. |
| C9 | common filtered view | False | ["S34", "S38", "S69", "S72"] | 3 | unknown | not_verified_cap | Not tested |
| C10 | aggregate MV | False | ["S34", "S38"] | 1 | unknown | not_verified_cap | Not tested |
| C11 | common filtered view | False | ["S65", "S74", "S76", "S79"] | 3 | unknown | not_verified_cap | Not tested |
| C12 | aggregate MV | False | ["S76", "S79"] | 1 | unknown | not_verified_cap | Not tested |


已验证覆盖（含触发查询、候选并集去重）：38/92 条成功数据 SQL。正确性仅针对当前数据库快照；未测性能的候选不能声称已加速。

[完整 build/rewrite 与比较证据](dacomp-073.analysis.json)。

### C7：aggregate MV

Union of grouping keys; decomposable aggregate states; AVG uses SUM and non-NULL COUNT.

原查询 [S3](#s3), [S7](#s7), [S8](#s8), [S10](#s10), [S12](#s12), [S13](#s13), [S14](#s14), [S17](#s17), [S18](#s18), [S20](#s20), [S21](#s21), [S24](#s24), [S25](#s25), [S29](#s29), [S30](#s30), [S33](#s33), [S35](#s35), [S75](#s75), [S80](#s80), [S81](#s81), [S88](#s88), [S89](#s89) → 新增共享状态 C7 → 后续 21 次可复用。该构建点为事后假设，不代表 Agent 当时预知后续。

构建定义：

```sql
SELECT state AS __g0, categories_team AS __g1, categories_department AS __g2, categories_level AS __g3, categories_location AS __g4, STRFTIME('%Y-%m', created_at) AS __g5, SUBSTRING(created_at, 1, 7) AS __g6, requisition_code AS __g7, has_requisition AS __g8, MIN(created_at) AS __a0, MAX(created_at) AS __a1, COUNT(*) AS __a2, MIN(updated_at) AS __a3, MAX(updated_at) AS __a4, SUM(count_requisitions) AS __a5, SUM(count_opportunities) AS __a6, SUM(count_open_opportunities) AS __a7, SUM(count_interviews) AS __a8 FROM "lever__posting_enhanced"  GROUP BY state, categories_team, categories_department, categories_level, categories_location, STRFTIME('%Y-%m', created_at), SUBSTRING(created_at, 1, 7), requisition_code, has_requisition
```

受益查询 S3 的改写示例：

```sql
SELECT MIN(__a0) AS min_date, MAX(__a1) AS max_date, SUM(__a2) AS total_rows FROM temp.reuse_candidate
```

| 原 SQL | 列名一致 | 结果一致 | 比较方法 |
| --- | --- | --- | --- |
| S3 | True | True | exact_multiset |
| S7 | True | True | exact_multiset |
| S8 | True | True | exact_multiset |
| S10 | True | True | ordered_numeric_tolerance |
| S12 | True | True | ordered_numeric_tolerance |
| S13 | True | True | ordered_numeric_tolerance |
| S14 | True | True | ordered_numeric_tolerance |
| S17 | True | True | ordered_numeric_tolerance |
| S18 | True | True | ordered_numeric_tolerance |
| S20 | True | True | ordered_numeric_tolerance |
| S21 | True | True | ordered_numeric_tolerance |
| S24 | True | True | ordered_numeric_tolerance |
| S25 | True | True | ordered_numeric_tolerance |
| S29 | True | True | ordered_numeric_tolerance |
| S30 | True | True | exact_multiset |
| S33 | True | True | ordered_numeric_tolerance |
| S35 | True | True | ordered_numeric_tolerance |
| S75 | True | True | exact_multiset |
| S80 | True | True | ordered_numeric_tolerance |
| S81 | True | True | ordered_numeric_tolerance |
| S88 | True | True | ordered_numeric_tolerance |
| S89 | True | True | ordered_numeric_tolerance |


验证状态：verified；成本结论：Not benchmarked; correctness alone does not establish net speedup.

### C8：aggregate MV

Union of grouping keys; decomposable aggregate states; AVG uses SUM and non-NULL COUNT.

原查询 [S4](#s4), [S9](#s9), [S11](#s11), [S26](#s26), [S27](#s27), [S31](#s31), [S39](#s39), [S64](#s64), [S73](#s73), [S78](#s78) → 新增共享状态 C8 → 后续 9 次可复用。该构建点为事后假设，不代表 Agent 当时预知后续。

构建定义：

```sql
SELECT status AS __g0, team AS __g1, SUBSTRING(created_at, 1, 7) AS __g2, has_posting AS __g3, MIN(created_at) AS __a0, MAX(created_at) AS __a1, COUNT(*) AS __a2, SUM(headcount_total) AS __a3, SUM(headcount_hired) AS __a4, SUM(CASE WHEN headcount_infinite = 1 THEN 1 ELSE 0 END) AS __a5, SUM(count_postings) AS __a6, SUM(count_offers) AS __a7 FROM "lever__requisition_enhanced"  GROUP BY status, team, SUBSTRING(created_at, 1, 7), has_posting
```

受益查询 S4 的改写示例：

```sql
SELECT MIN(__a0) AS min_date, MAX(__a1) AS max_date, SUM(__a2) AS total_rows FROM temp.reuse_candidate
```

| 原 SQL | 列名一致 | 结果一致 | 比较方法 |
| --- | --- | --- | --- |
| S4 | True | True | exact_multiset |
| S9 | True | True | exact_multiset |
| S11 | True | True | ordered_numeric_tolerance |
| S26 | True | True | ordered_numeric_tolerance |
| S27 | True | True | ordered_numeric_tolerance |
| S31 | True | True | exact_multiset |
| S39 | True | True | ordered_numeric_tolerance |
| S64 | True | True | exact_multiset |
| S73 | True | True | exact_multiset |
| S78 | True | True | exact_multiset |


验证状态：verified；成本结论：Not benchmarked; correctness alone does not establish net speedup.

### C3：exact-result reuse

Identical normalized SQL and parameters; archive equality checked.

原查询 [S84](#s84), [S86](#s86), [S90](#s90), [S92](#s92), [S94](#s94), [S96](#s96) → 保留前序结果 S84 → 后续 5 次可复用。该构建点为事后假设，不代表 Agent 当时预知后续。

| 原 SQL | 列名一致 | 结果一致 | 比较方法 |
| --- | --- | --- | --- |
| S86 | True | True | exact_multiset |
| S90 | True | True | exact_multiset |
| S92 | True | True | exact_multiset |
| S94 | True | True | exact_multiset |
| S96 | True | True | exact_multiset |


验证状态：verified；成本结论：Not benchmarked; correctness alone does not establish net speedup.

结果依赖：自动记录 SQL→Python 的接口父调用，以及源码中引用归档文件的消费者；字面值相同不认定因果。模型方向选择需要人工读取消息，尚未做全面因果标注。

[原始报告](../../../runs/dsv4flash-db-first-full-01/dacomp-073/attempt-01/answer.md)；[统一消息](../../../runs/dsv4flash-db-first-full-01/dacomp-073/attempt-01/messages.jsonl)；[原始 OpenCode 事件](../../../runs/dsv4flash-db-first-full-01/dacomp-073/attempt-01/opencode.jsonl)；[SQL 引擎日志](../../../runs/dsv4flash-db-first-full-01/dacomp-073/attempt-01/sql_journal.jsonl)。

[可读报告（本地图片链接规范化）](../answers/dacomp-073.md)。原始回答保留，分析结论未改写。

## S1

类别 `connection_setup`；来源 `connection`；调用 `30e410012e9443ff912ee4ddb4af7c73`；状态 `success`。

```sql
PRAGMA query_only=ON
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-073/attempt-01/sql/S1.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-073/attempt-01/sql/S1.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-073/attempt-01/results/S1.rows.jsonl)；完整：True；SHA256：`e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`。

## S2

类别 `metadata`；来源 `list_db`；调用 `30e410012e9443ff912ee4ddb4af7c73`；状态 `success`。

```sql
SELECT name,sql FROM sqlite_master WHERE type='table' ORDER BY name
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-073/attempt-01/sql/S2.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-073/attempt-01/sql/S2.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-073/attempt-01/results/S2.rows.jsonl)；完整：True；SHA256：`6d65875e0a065f19403ad8e7b06ce0889cb491e294ddbaa0c59bd3c30466cb58`。

## S3

类别 `data`；来源 `query_db`；调用 `b8e3e906c31e4cb798fe95e9338aebeb`；状态 `success`。

```sql
SELECT MIN(created_at) as min_date, MAX(created_at) as max_date, COUNT(*) as total_rows FROM lever__posting_enhanced
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-073/attempt-01/sql/S3.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-073/attempt-01/sql/S3.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-073/attempt-01/results/S3.rows.jsonl)；完整：True；SHA256：`e684799147913d504cf61131be94b528443d6709d0e9c1dfd4affe18a916b2be`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "lever__posting_enhanced", "kind": "base", "block": null, "base_tables": ["lever__posting_enhanced"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | MIN(created_at) | [{"table": "lever__posting_enhanced", "column": "created_at"}] | [] | False |
| B1 | MAX(created_at) | [{"table": "lever__posting_enhanced", "column": "created_at"}] | [] | False |
| B1 | COUNT(*) | [] | [] | True |


## S4

类别 `data`；来源 `query_db`；调用 `f4b3f9bbf59d4c4e825812dd5b2c3e59`；状态 `success`。

```sql
SELECT MIN(created_at) as min_date, MAX(created_at) as max_date, COUNT(*) as total_rows FROM lever__requisition_enhanced
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-073/attempt-01/sql/S4.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-073/attempt-01/sql/S4.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-073/attempt-01/results/S4.rows.jsonl)；完整：True；SHA256：`ffdf346fdf81373a2c5c77b681d34fe56ce0865f6b1afb445289f60f725f0633`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "lever__requisition_enhanced", "kind": "base", "block": null, "base_tables": ["lever__requisition_enhanced"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | MIN(created_at) | [{"table": "lever__requisition_enhanced", "column": "created_at"}] | [] | False |
| B1 | MAX(created_at) | [{"table": "lever__requisition_enhanced", "column": "created_at"}] | [] | False |
| B1 | COUNT(*) | [] | [] | True |


## S5

类别 `data`；来源 `query_db`；调用 `3925b0b0a9a8405dbc37a8edc9ffdbdc`；状态 `success`。

```sql
SELECT DISTINCT state FROM lever__posting_enhanced
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-073/attempt-01/sql/S5.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-073/attempt-01/sql/S5.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-073/attempt-01/results/S5.rows.jsonl)；完整：True；SHA256：`a288fa00be3a90fcc822421f4d5434f894ea9c0c0719028d044628788b696220`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "lever__posting_enhanced", "kind": "base", "block": null, "base_tables": ["lever__posting_enhanced"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |


## S6

类别 `data`；来源 `query_db`；调用 `11eb499783d64268aa0ac3fd6a098cbc`；状态 `success`。

```sql
SELECT DISTINCT status FROM lever__requisition_enhanced
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-073/attempt-01/sql/S6.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-073/attempt-01/sql/S6.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-073/attempt-01/results/S6.rows.jsonl)；完整：True；SHA256：`24e67396eb56af18dce1c40c22838a5416ae0c04aad20a64474dc6b0630b64e0`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "lever__requisition_enhanced", "kind": "base", "block": null, "base_tables": ["lever__requisition_enhanced"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |


## S7

类别 `data`；来源 `query_db`；调用 `ccff3d15c88f4910b0b9c39342e7efd3`；状态 `success`。

```sql
SELECT MIN(updated_at) as min_upd, MAX(updated_at) as max_upd FROM lever__posting_enhanced
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-073/attempt-01/sql/S7.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-073/attempt-01/sql/S7.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-073/attempt-01/results/S7.rows.jsonl)；完整：True；SHA256：`fef7ce373a23ac1e0c54bbc50ed60e4ad9852a9f50375796cdca9c5e830cd3fb`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "lever__posting_enhanced", "kind": "base", "block": null, "base_tables": ["lever__posting_enhanced"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | MIN(updated_at) | [{"table": "lever__posting_enhanced", "column": "updated_at"}] | [] | False |
| B1 | MAX(updated_at) | [{"table": "lever__posting_enhanced", "column": "updated_at"}] | [] | False |


## S8

类别 `data`；来源 `query_db`；调用 `63e37fa002dc44ab8b348f1e6296d559`；状态 `success`。

```sql
SELECT state, COUNT(*) as cnt FROM lever__posting_enhanced GROUP BY state
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-073/attempt-01/sql/S8.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-073/attempt-01/sql/S8.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-073/attempt-01/results/S8.rows.jsonl)；完整：True；SHA256：`1a36bbd12b7f6aca2e58b2fc76d073d3dcae7b8e7b8770aaa78a052f52ae4b1f`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "lever__posting_enhanced", "kind": "base", "block": null, "base_tables": ["lever__posting_enhanced"]}] | [] | ["state"] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |


## S9

类别 `data`；来源 `query_db`；调用 `1358336163ae45f9b4cc7aa886fd9e01`；状态 `success`。

```sql
SELECT status, COUNT(*) as cnt FROM lever__requisition_enhanced GROUP BY status
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-073/attempt-01/sql/S9.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-073/attempt-01/sql/S9.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-073/attempt-01/results/S9.rows.jsonl)；完整：True；SHA256：`2068d3e653192217897b416a1c92ee8fad607419070a42c158e78c1b64caafdf`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "lever__requisition_enhanced", "kind": "base", "block": null, "base_tables": ["lever__requisition_enhanced"]}] | [] | ["status"] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |


## S10

类别 `data`；来源 `query_db`；调用 `9eeec740fc53425282c2403998d5af65`；状态 `success`。

```sql
SELECT categories_team, COUNT(*) as cnt FROM lever__posting_enhanced GROUP BY categories_team ORDER BY cnt DESC
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-073/attempt-01/sql/S10.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-073/attempt-01/sql/S10.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-073/attempt-01/results/S10.rows.jsonl)；完整：True；SHA256：`5602bfafd4c3f58ab59afff3f4f8e2fdfa9a0680491a6c6f6a308e68ac95ffff`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "lever__posting_enhanced", "kind": "base", "block": null, "base_tables": ["lever__posting_enhanced"]}] | [] | ["categories_team"] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |


## S11

类别 `data`；来源 `query_db`；调用 `a4ad48adc4fa4076a60ab69642aa7e4e`；状态 `success`。

```sql
SELECT team, COUNT(*) as cnt FROM lever__requisition_enhanced GROUP BY team ORDER BY cnt DESC
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-073/attempt-01/sql/S11.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-073/attempt-01/sql/S11.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-073/attempt-01/results/S11.rows.jsonl)；完整：True；SHA256：`e7034b6be88e15aeeb31fce2e267386bcf2a411ee8282c6b1f9992dc056c4988`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "lever__requisition_enhanced", "kind": "base", "block": null, "base_tables": ["lever__requisition_enhanced"]}] | [] | ["team"] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |


## S12

类别 `data`；来源 `query_db`；调用 `4a08abca37714f939c940a3b7d9f24ba`；状态 `success`。

```sql
SELECT categories_department, COUNT(*) as cnt FROM lever__posting_enhanced GROUP BY categories_department ORDER BY cnt DESC
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-073/attempt-01/sql/S12.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-073/attempt-01/sql/S12.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-073/attempt-01/results/S12.rows.jsonl)；完整：True；SHA256：`f61ce30c40f5c3453b5056aff39c5416075a73f567396cb5a661b2692bb7c7f3`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "lever__posting_enhanced", "kind": "base", "block": null, "base_tables": ["lever__posting_enhanced"]}] | [] | ["categories_department"] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |


## S13

类别 `data`；来源 `query_db`；调用 `a87979668137433780d847581a0f1629`；状态 `success`。

```sql
SELECT categories_level, COUNT(*) as cnt FROM lever__posting_enhanced GROUP BY categories_level ORDER BY cnt DESC
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-073/attempt-01/sql/S13.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-073/attempt-01/sql/S13.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-073/attempt-01/results/S13.rows.jsonl)；完整：True；SHA256：`ed2f36314d32890c1a32bd121c4f336550b01262b58892e51aa2c1f3ce47b0be`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "lever__posting_enhanced", "kind": "base", "block": null, "base_tables": ["lever__posting_enhanced"]}] | [] | ["categories_level"] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |


## S14

类别 `data`；来源 `query_db`；调用 `ee81fc06a4534096b7666df91e4ed031`；状态 `success`。

```sql
SELECT categories_location, COUNT(*) as cnt FROM lever__posting_enhanced GROUP BY categories_location ORDER BY cnt DESC
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-073/attempt-01/sql/S14.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-073/attempt-01/sql/S14.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-073/attempt-01/results/S14.rows.jsonl)；完整：True；SHA256：`0fc85a2e822f3c9611257f22af95729fbff44886f11e60faf1758031f0b7a6d8`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "lever__posting_enhanced", "kind": "base", "block": null, "base_tables": ["lever__posting_enhanced"]}] | [] | ["categories_location"] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |


## S15

类别 `data`；来源 `query_db`；调用 `6c340cbf5cfd4ee9a5ccbab8f9811db3`；状态 `success`。

```sql
SELECT DISTINCT posting_hiring_manager_name FROM lever__posting_enhanced LIMIT 20
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-073/attempt-01/sql/S15.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-073/attempt-01/sql/S15.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-073/attempt-01/results/S15.rows.jsonl)；完整：True；SHA256：`738023ec1156a5da1173ee7a7ac376b61b19b5b8e91ed2ece552897341f50f36`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "lever__posting_enhanced", "kind": "base", "block": null, "base_tables": ["lever__posting_enhanced"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |


## S16

类别 `data`；来源 `query_db`；调用 `c995b6f6ae0147d8bc046faae68ac5f4`；状态 `success`。

```sql
SELECT DISTINCT hiring_manager_user_id FROM lever__requisition_enhanced LIMIT 20
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-073/attempt-01/sql/S16.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-073/attempt-01/sql/S16.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-073/attempt-01/results/S16.rows.jsonl)；完整：True；SHA256：`4a5bf1a5689f9c3281c459f10cdbebe37e7ccf53241cf71c4677dfb811c38f32`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "lever__requisition_enhanced", "kind": "base", "block": null, "base_tables": ["lever__requisition_enhanced"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |


## S17

类别 `data`；来源 `query_db`；调用 `a9b31cfff1454301bcfe514765b76e13`；状态 `success`。

```sql
SELECT state, categories_department, COUNT(*) as cnt FROM lever__posting_enhanced GROUP BY state, categories_department ORDER BY categories_department, state
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-073/attempt-01/sql/S17.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-073/attempt-01/sql/S17.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-073/attempt-01/results/S17.rows.jsonl)；完整：True；SHA256：`5ee4b1f460fe544736ee457c2bdf59dc35d7b257271133f38b4f2a436735795d`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "lever__posting_enhanced", "kind": "base", "block": null, "base_tables": ["lever__posting_enhanced"]}] | [] | ["state", "categories_department"] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |


## S18

类别 `data`；来源 `query_db`；调用 `1624dd60b3954026973e7c280558e545`；状态 `success`。

```sql
SELECT state, categories_department, COUNT(*) as cnt FROM lever__posting_enhanced GROUP BY categories_department, state ORDER BY categories_department, state
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-073/attempt-01/sql/S18.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-073/attempt-01/sql/S18.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-073/attempt-01/results/S18.rows.jsonl)；完整：True；SHA256：`5ee4b1f460fe544736ee457c2bdf59dc35d7b257271133f38b4f2a436735795d`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "lever__posting_enhanced", "kind": "base", "block": null, "base_tables": ["lever__posting_enhanced"]}] | [] | ["categories_department", "state"] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |


## S19

类别 `data`；来源 `query_db`；调用 `f5906a45fbbf4e5684b25eef408e4a81`；状态 `success`。

```sql
SELECT categories_department, COUNT(DISTINCT posting_hiring_manager_name) as num_hiring_managers FROM lever__posting_enhanced GROUP BY categories_department ORDER BY categories_department
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-073/attempt-01/sql/S19.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-073/attempt-01/sql/S19.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-073/attempt-01/results/S19.rows.jsonl)；完整：True；SHA256：`8c8647a87aa7568ef5a62c9b42cd6f4c6a0ab96e8cf6eac8bcd747933e85632a`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "lever__posting_enhanced", "kind": "base", "block": null, "base_tables": ["lever__posting_enhanced"]}] | [] | ["categories_department"] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(DISTINCT posting_hiring_manager_name) | [{"table": "lever__posting_enhanced", "column": "posting_hiring_manager_name"}] | [] | False |


## S20

类别 `data`；来源 `query_db`；调用 `fa259abc8bdd4e7d950b4979c773fd67`；状态 `success`。

```sql
SELECT strftime('%Y-%m', created_at) as ym, categories_department, COUNT(*) as cnt FROM lever__posting_enhanced GROUP BY ym, categories_department ORDER BY ym, categories_department
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-073/attempt-01/sql/S20.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-073/attempt-01/sql/S20.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-073/attempt-01/results/S20.rows.jsonl)；完整：True；SHA256：`db584952f8fcbf5dca7327409b4f3a0647c81a1d5238f86c8151f0951e43dc95`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "lever__posting_enhanced", "kind": "base", "block": null, "base_tables": ["lever__posting_enhanced"]}] | [] | ["STRFTIME('%Y-%m', created_at)", "categories_department"] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |


## S21

类别 `data`；来源 `query_db`；调用 `91a63aacc7a348de9759df93d7e626be`；状态 `success`。

```sql
SELECT strftime('%Y-%m', created_at) as ym, COUNT(*) as cnt FROM lever__posting_enhanced GROUP BY ym ORDER BY ym
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-073/attempt-01/sql/S21.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-073/attempt-01/sql/S21.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-073/attempt-01/results/S21.rows.jsonl)；完整：True；SHA256：`328b1225a390981a285f45d0d677ded9a3486e062bc9b6ec51989cafc72a4686`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "lever__posting_enhanced", "kind": "base", "block": null, "base_tables": ["lever__posting_enhanced"]}] | [] | ["STRFTIME('%Y-%m', created_at)"] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |


## S22

类别 `data`；来源 `query_db`；调用 `cf1d81ef27774b968f077f84038bf5bc`；状态 `success`。

```sql
SELECT created_at FROM lever__posting_enhanced LIMIT 10
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-073/attempt-01/sql/S22.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-073/attempt-01/sql/S22.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-073/attempt-01/results/S22.rows.jsonl)；完整：True；SHA256：`b7d20475229350f87a6aa428ca8c2a901fd50701213ccb381c6c4d304859bea0`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "lever__posting_enhanced", "kind": "base", "block": null, "base_tables": ["lever__posting_enhanced"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |


## S23

类别 `data`；来源 `query_db`；调用 `fce18d405e2e44ed8a8fe03588c780c2`；状态 `success`。

```sql
SELECT updated_at FROM lever__posting_enhanced LIMIT 10
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-073/attempt-01/sql/S23.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-073/attempt-01/sql/S23.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-073/attempt-01/results/S23.rows.jsonl)；完整：True；SHA256：`6fa322bb47363196840adc6585ac874a6b861928004c12294f1a937153f13f1f`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "lever__posting_enhanced", "kind": "base", "block": null, "base_tables": ["lever__posting_enhanced"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |


## S24

类别 `data`；来源 `query_db`；调用 `5ebc34bd6a6f4c44ae0e4fe820af31a6`；状态 `success`。

```sql
SELECT substr(created_at, 1, 7) as ym, categories_department, COUNT(*) as cnt FROM lever__posting_enhanced GROUP BY ym, categories_department ORDER BY ym, categories_department
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-073/attempt-01/sql/S24.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-073/attempt-01/sql/S24.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-073/attempt-01/results/S24.rows.jsonl)；完整：True；SHA256：`3f97a1c07870c6e34979d95a0b61a6270ac3013d6428bccd2b5e94d80a57fd11`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "lever__posting_enhanced", "kind": "base", "block": null, "base_tables": ["lever__posting_enhanced"]}] | [] | ["SUBSTRING(created_at, 1, 7)", "categories_department"] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |


## S25

类别 `data`；来源 `query_db`；调用 `1a646332d8f745f7a4900b9d5d57fedb`；状态 `success`。

```sql
SELECT substr(created_at, 1, 7) as ym, COUNT(*) as cnt FROM lever__posting_enhanced GROUP BY ym ORDER BY ym
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-073/attempt-01/sql/S25.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-073/attempt-01/sql/S25.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-073/attempt-01/results/S25.rows.jsonl)；完整：True；SHA256：`0870a7b42f6ab83ea11094501cbc8a91bc6780b31602d9997d7542936fe33644`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "lever__posting_enhanced", "kind": "base", "block": null, "base_tables": ["lever__posting_enhanced"]}] | [] | ["SUBSTRING(created_at, 1, 7)"] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |


## S26

类别 `data`；来源 `query_db`；调用 `01e387ce13ba472baa5ebfd4af75f50d`；状态 `success`。

```sql
SELECT substr(created_at, 1, 7) as ym, COUNT(*) as cnt FROM lever__requisition_enhanced GROUP BY ym ORDER BY ym
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-073/attempt-01/sql/S26.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-073/attempt-01/sql/S26.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-073/attempt-01/results/S26.rows.jsonl)；完整：True；SHA256：`846875140a9df08a2701b87723bb7f0da2d15299fc2cb416402f2f20d363d8d1`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "lever__requisition_enhanced", "kind": "base", "block": null, "base_tables": ["lever__requisition_enhanced"]}] | [] | ["SUBSTRING(created_at, 1, 7)"] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |


## S27

类别 `data`；来源 `query_db`；调用 `35e899c034fc420c8dd3d823bb8a2f46`；状态 `success`。

```sql
SELECT substr(created_at, 1, 7) as ym, team, COUNT(*) as cnt FROM lever__requisition_enhanced GROUP BY ym, team ORDER BY ym, team
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-073/attempt-01/sql/S27.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-073/attempt-01/sql/S27.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-073/attempt-01/results/S27.rows.jsonl)；完整：True；SHA256：`a3219deba28227f41609570ecedcb3e9cd83ae75d7c6a458b782aaf74f1f0571`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "lever__requisition_enhanced", "kind": "base", "block": null, "base_tables": ["lever__requisition_enhanced"]}] | [] | ["SUBSTRING(created_at, 1, 7)", "team"] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |


## S28

类别 `data`；来源 `query_db`；调用 `830938594aee4a5ba411e8c0b4b44af9`；状态 `success`。

```sql
SELECT requisition_code, status, headcount_total, headcount_hired, headcount_infinite, team, hiring_manager_user_id FROM lever__requisition_enhanced LIMIT 15
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-073/attempt-01/sql/S28.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-073/attempt-01/sql/S28.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-073/attempt-01/results/S28.rows.jsonl)；完整：True；SHA256：`68ad99715398c7fde4e568f1baeb3a8aaa516ff5d1a5b3ec0c4d04536539b6e4`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "lever__requisition_enhanced", "kind": "base", "block": null, "base_tables": ["lever__requisition_enhanced"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |


## S29

类别 `data`；来源 `query_db`；调用 `eb18e9d59548429ab02f21d8b8e771a4`；状态 `success`。

```sql
SELECT requisition_code, COUNT(*) as cnt FROM lever__posting_enhanced GROUP BY requisition_code ORDER BY cnt DESC LIMIT 15
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-073/attempt-01/sql/S29.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-073/attempt-01/sql/S29.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-073/attempt-01/results/S29.rows.jsonl)；完整：True；SHA256：`49e9c99541765cf42d8a411d573fc4fb46275d688cdcc574c3625076f2ff6bbd`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "lever__posting_enhanced", "kind": "base", "block": null, "base_tables": ["lever__posting_enhanced"]}] | [] | ["requisition_code"] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |


## S30

类别 `data`；来源 `query_db`；调用 `4924f426537c477dbe2ba76c4ab91775`；状态 `success`。

```sql
SELECT has_requisition, COUNT(*) as cnt FROM lever__posting_enhanced GROUP BY has_requisition
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-073/attempt-01/sql/S30.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-073/attempt-01/sql/S30.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-073/attempt-01/results/S30.rows.jsonl)；完整：True；SHA256：`dfde2bb7481f6c92564506147cc69f8382f8f23ac344fde8379f919b2cebed4d`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "lever__posting_enhanced", "kind": "base", "block": null, "base_tables": ["lever__posting_enhanced"]}] | [] | ["has_requisition"] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |


## S31

类别 `data`；来源 `query_db`；调用 `61c5041c88024ae181d9f37b1adb1c6d`；状态 `success`。

```sql
SELECT has_posting, COUNT(*) as cnt FROM lever__requisition_enhanced GROUP BY has_posting
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-073/attempt-01/sql/S31.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-073/attempt-01/sql/S31.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-073/attempt-01/results/S31.rows.jsonl)；完整：True；SHA256：`4014a9b1ee1ec6f04e8d8ff6817eb422463d027965bbc24d2a8b397f63a8f0a2`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "lever__requisition_enhanced", "kind": "base", "block": null, "base_tables": ["lever__requisition_enhanced"]}] | [] | ["has_posting"] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |


## S32

类别 `data`；来源 `query_db`；调用 `6259b3e89c8a413d853f19ab63a37527`；状态 `success`。

```sql
SELECT p.requisition_code, p.categories_department, r.team, r.status, r.headcount_total, r.headcount_hired, r.headcount_infinite
FROM lever__posting_enhanced p
JOIN lever__requisition_enhanced r ON p.requisition_code = r.requisition_code
LIMIT 15
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-073/attempt-01/sql/S32.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-073/attempt-01/sql/S32.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-073/attempt-01/results/S32.rows.jsonl)；完整：True；SHA256：`4883e0ffa2c1026cf940f8ca4873043b12f3a081872d02eb56831510bfa69f30`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "p", "kind": "base", "block": null, "base_tables": ["lever__posting_enhanced"]}, {"alias": "r", "kind": "base", "block": null, "base_tables": ["lever__requisition_enhanced"]}] | [{"type": "INNER", "right": "lever__requisition_enhanced AS r", "on": "p.requisition_code = r.requisition_code", "using": []}] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |


## S33

类别 `data`；来源 `query_db`；调用 `e6434827b5674bf3b4bdf1d7a48dcd86`；状态 `success`。

```sql
SELECT substr(created_at, 1, 7) as ym, categories_department, COUNT(*) as cnt
FROM lever__posting_enhanced
GROUP BY categories_department, substr(created_at, 1, 7)
ORDER BY categories_department, ym
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-073/attempt-01/sql/S33.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-073/attempt-01/sql/S33.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-073/attempt-01/results/S33.rows.jsonl)；完整：True；SHA256：`c76d6786e4bdedf9d3371e35a30eef56065b78a48804f18d3d06e5c74424644e`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "lever__posting_enhanced", "kind": "base", "block": null, "base_tables": ["lever__posting_enhanced"]}] | [] | ["categories_department", "SUBSTRING(created_at, 1, 7)"] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |


## S34

类别 `data`；来源 `query_db`；调用 `eb860e925122495d82f74206c8ee0a34`；状态 `success`。

```sql
SELECT substr(created_at, 1, 7) as ym, categories_department, COUNT(*) as cnt
FROM lever__posting_enhanced
WHERE state IN ('published', 'pending')
GROUP BY categories_department, substr(created_at, 1, 7)
ORDER BY categories_department, ym
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-073/attempt-01/sql/S34.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-073/attempt-01/sql/S34.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-073/attempt-01/results/S34.rows.jsonl)；完整：True；SHA256：`f254c0be156d41197ee0046e1597628c29146cc4ee41446f8f74ef5c2df7b6af`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "lever__posting_enhanced", "kind": "base", "block": null, "base_tables": ["lever__posting_enhanced"]}] | [] | ["categories_department", "SUBSTRING(created_at, 1, 7)"] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |


## S35

类别 `data`；来源 `query_db`；调用 `398e1cd3422d4815b45466a1e45ce94e`；状态 `success`。

```sql
SELECT categories_department, state, COUNT(*) as cnt
FROM lever__posting_enhanced
GROUP BY categories_department, state
ORDER BY categories_department, state
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-073/attempt-01/sql/S35.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-073/attempt-01/sql/S35.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-073/attempt-01/results/S35.rows.jsonl)；完整：True；SHA256：`f8a9437507a1c2291c0c3b5caf95934f3e8b4f1c5e8184e381107b2ee4ce4f5b`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "lever__posting_enhanced", "kind": "base", "block": null, "base_tables": ["lever__posting_enhanced"]}] | [] | ["categories_department", "state"] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |


## S36

类别 `data`；来源 `query_db`；调用 `29bb7a31532b4afe95d90ed5926fa576`；状态 `success`。

```sql
WITH monthly AS (
  SELECT categories_department,
         substr(created_at, 1, 7) as ym,
         COUNT(*) as cnt
  FROM lever__posting_enhanced
  WHERE substr(created_at, 1, 7) IS NOT NULL
  GROUP BY categories_department, substr(created_at, 1, 7)
)
SELECT categories_department, ym, cnt,
       LAG(cnt) OVER (PARTITION BY categories_department ORDER BY ym) as prev_cnt,
       CASE WHEN LAG(cnt) OVER (PARTITION BY categories_department ORDER BY ym) > 0
            THEN 1.0*(cnt - LAG(cnt) OVER (PARTITION BY categories_department ORDER BY ym)) / LAG(cnt) OVER (PARTITION BY categories_department ORDER BY ym)
            ELSE NULL END as mom_growth
FROM monthly
ORDER BY categories_department, ym
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-073/attempt-01/sql/S36.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-073/attempt-01/sql/S36.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-073/attempt-01/results/S36.rows.jsonl)；完整：True；SHA256：`56fd375907db1a1275272f3359efb1712f97f6d753892f3ad8602932d9ffae85`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "lever__posting_enhanced", "kind": "base", "block": null, "base_tables": ["lever__posting_enhanced"]}] | [] | ["categories_department", "SUBSTRING(created_at, 1, 7)"] |
| B2 | [{"alias": "monthly", "kind": "derived", "block": "B1", "base_tables": ["lever__posting_enhanced"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |


## S37

类别 `data`；来源 `query_db`；调用 `132f734c2bba4ff7bbbc093fabe413b2`；状态 `success`。

```sql
WITH monthly AS (
  SELECT categories_department,
         substr(created_at, 1, 7) as ym,
         COUNT(*) as cnt
  FROM lever__posting_enhanced
  WHERE substr(created_at, 1, 7) IS NOT NULL
  GROUP BY categories_department, substr(created_at, 1, 7)
),
mom_growth AS (
  SELECT categories_department, ym, cnt,
         LAG(cnt) OVER (PARTITION BY categories_department ORDER BY ym) as prev_cnt,
         CASE WHEN LAG(cnt) OVER (PARTITION BY categories_department ORDER BY ym) > 0
              THEN 1.0*(cnt - LAG(cnt) OVER (PARTITION BY categories_department ORDER BY ym)) / LAG(cnt) OVER (PARTITION BY categories_department ORDER BY ym)
              ELSE NULL END as mom_growth
  FROM monthly
)
SELECT categories_department,
       AVG(mom_growth) as avg_mom_growth,
       SUM(CASE WHEN ym = '2025-07' THEN cnt ELSE 0 END) as latest_month_cnt
FROM mom_growth
WHERE ym IN ('2025-06', '2025-07')
  AND mom_growth IS NOT NULL
GROUP BY categories_department
ORDER BY categories_department
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-073/attempt-01/sql/S37.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-073/attempt-01/sql/S37.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-073/attempt-01/results/S37.rows.jsonl)；完整：True；SHA256：`2944f3956d20720f3beb71067fa802f746db9dfc12416edb0b6bea717cabf0da`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "lever__posting_enhanced", "kind": "base", "block": null, "base_tables": ["lever__posting_enhanced"]}] | [] | ["categories_department", "SUBSTRING(created_at, 1, 7)"] |
| B2 | [{"alias": "monthly", "kind": "derived", "block": "B1", "base_tables": ["lever__posting_enhanced"]}] | [] | [] |
| B3 | [{"alias": "mom_growth", "kind": "derived", "block": "B2", "base_tables": ["lever__posting_enhanced"]}] | [] | ["categories_department"] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |
| B3 | AVG(mom_growth) | [{"table": "lever__posting_enhanced", "column": "categories_department"}, {"table": "lever__posting_enhanced", "column": "categories_department"}, {"table": "lever__posting_enhanced", "column": "created_at"}, {"table": "lever__posting_enhanced", "column": "created_at"}, {"table": "lever__posting_enhanced", "column": "categories_department"}, {"table": "lever__posting_enhanced", "column": "created_at"}] | [] | False |
| B3 | SUM(CASE WHEN ym = '2025-07' THEN cnt ELSE 0 END) | [] | [{"table": "lever__posting_enhanced", "column": "created_at"}] | False |


## S38

类别 `data`；来源 `query_db`；调用 `b6a10260b9074b0e9ff3def93e715e83`；状态 `success`。

```sql
SELECT categories_department, COUNT(*) as active_postings
FROM lever__posting_enhanced
WHERE state IN ('published', 'pending')
GROUP BY categories_department
ORDER BY categories_department
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-073/attempt-01/sql/S38.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-073/attempt-01/sql/S38.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-073/attempt-01/results/S38.rows.jsonl)；完整：True；SHA256：`7bc9f2534baf3e108871077ed33cc87de2a5c92b40a380b38b3a8410c3cc0e94`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "lever__posting_enhanced", "kind": "base", "block": null, "base_tables": ["lever__posting_enhanced"]}] | [] | ["categories_department"] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |


## S39

类别 `data`；来源 `query_db`；调用 `4fed5a534d81493d8a783e35fa2945d7`；状态 `success`。

```sql
SELECT r.status, COUNT(*) as cnt
FROM lever__requisition_enhanced r
GROUP BY r.status
ORDER BY r.status
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-073/attempt-01/sql/S39.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-073/attempt-01/sql/S39.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-073/attempt-01/results/S39.rows.jsonl)；完整：True；SHA256：`2068d3e653192217897b416a1c92ee8fad607419070a42c158e78c1b64caafdf`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "r", "kind": "base", "block": null, "base_tables": ["lever__requisition_enhanced"]}] | [] | ["r.status"] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |


## S40

类别 `data`；来源 `query_db`；调用 `b233a29c37f44b5a87413582663cc3ce`；状态 `success`。

```sql
SELECT p.categories_department, r.status, COUNT(DISTINCT r.requisition_id) as cnt
FROM lever__requisition_enhanced r
LEFT JOIN lever__posting_enhanced p ON p.requisition_code = r.requisition_code
GROUP BY p.categories_department, r.status
ORDER BY p.categories_department, r.status
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-073/attempt-01/sql/S40.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-073/attempt-01/sql/S40.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-073/attempt-01/results/S40.rows.jsonl)；完整：True；SHA256：`ad7590cdaadf45bc70130d5f3b46ae1276d18fec2651756c36bb2803f8280826`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "r", "kind": "base", "block": null, "base_tables": ["lever__requisition_enhanced"]}, {"alias": "p", "kind": "base", "block": null, "base_tables": ["lever__posting_enhanced"]}] | [{"type": "LEFT", "right": "lever__posting_enhanced AS p", "on": "p.requisition_code = r.requisition_code", "using": []}] | ["p.categories_department", "r.status"] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(DISTINCT r.requisition_id) | [{"table": "lever__requisition_enhanced", "column": "requisition_id"}] | [] | False |


## S41

类别 `data`；来源 `query_db`；调用 `bb9f535713304a3b8507675eadab4b3b`；状态 `success`。

```sql
SELECT r.requisition_code, r.team, r.status, r.headcount_total, r.headcount_hired, r.headcount_infinite
FROM lever__requisition_enhanced r
WHERE r.has_posting = 1
LIMIT 20
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-073/attempt-01/sql/S41.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-073/attempt-01/sql/S41.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-073/attempt-01/results/S41.rows.jsonl)；完整：True；SHA256：`e78fee90192a688820df781a241f26d64a2604b3b628edea17dd4b3f2eb9254f`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "r", "kind": "base", "block": null, "base_tables": ["lever__requisition_enhanced"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |


## S42

类别 `data`；来源 `query_db`；调用 `8c21d615074243e9bde0189b2382b76a`；状态 `success`。

```sql
SELECT r.requisition_code, r.team, r.status, p.categories_department, p.posting_title
FROM lever__requisition_enhanced r
JOIN lever__posting_enhanced p ON r.requisition_code = p.requisition_code
LIMIT 20
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-073/attempt-01/sql/S42.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-073/attempt-01/sql/S42.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-073/attempt-01/results/S42.rows.jsonl)；完整：True；SHA256：`33ff5497c386c7a5e3d98c04667b538f59b8a7a209885ef5a9d6a76268a996c4`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "r", "kind": "base", "block": null, "base_tables": ["lever__requisition_enhanced"]}, {"alias": "p", "kind": "base", "block": null, "base_tables": ["lever__posting_enhanced"]}] | [{"type": "INNER", "right": "lever__posting_enhanced AS p", "on": "r.requisition_code = p.requisition_code", "using": []}] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |


## S43

类别 `data`；来源 `query_db`；调用 `1bb9fc7ac509492aa84e9c645a50e2ea`；状态 `success`。

```sql
SELECT COUNT(DISTINCT requisition_code) as distinct_req_codes_posting FROM lever__posting_enhanced
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-073/attempt-01/sql/S43.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-073/attempt-01/sql/S43.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-073/attempt-01/results/S43.rows.jsonl)；完整：True；SHA256：`0fb06f7da26cf9fd53644fcf9fd972fd78002af5b018c5b7caf2e80803b88bad`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "lever__posting_enhanced", "kind": "base", "block": null, "base_tables": ["lever__posting_enhanced"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(DISTINCT requisition_code) | [{"table": "lever__posting_enhanced", "column": "requisition_code"}] | [] | False |


## S44

类别 `data`；来源 `query_db`；调用 `429957d97fae4e95a08955ca3b187e3d`；状态 `success`。

```sql
SELECT COUNT(DISTINCT requisition_code) as distinct_req_codes_req FROM lever__requisition_enhanced
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-073/attempt-01/sql/S44.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-073/attempt-01/sql/S44.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-073/attempt-01/results/S44.rows.jsonl)；完整：True；SHA256：`914c5efa683150856b3065e4c7e758e0ee6040ca8abc568edf466d879be69fee`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "lever__requisition_enhanced", "kind": "base", "block": null, "base_tables": ["lever__requisition_enhanced"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(DISTINCT requisition_code) | [{"table": "lever__requisition_enhanced", "column": "requisition_code"}] | [] | False |


## S45

类别 `data`；来源 `query_db`；调用 `60a51508d3a046fd97c680a7b05daa56`；状态 `success`。

```sql
SELECT COUNT(DISTINCT p.requisition_code) as matched_codes
FROM lever__posting_enhanced p
JOIN lever__requisition_enhanced r ON p.requisition_code = r.requisition_code
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-073/attempt-01/sql/S45.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-073/attempt-01/sql/S45.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-073/attempt-01/results/S45.rows.jsonl)；完整：True；SHA256：`631e21d653c4403cc79be7266a9ded76c4f00e70e98fc0ef2bb3d0d0d3e0a09e`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "p", "kind": "base", "block": null, "base_tables": ["lever__posting_enhanced"]}, {"alias": "r", "kind": "base", "block": null, "base_tables": ["lever__requisition_enhanced"]}] | [{"type": "INNER", "right": "lever__requisition_enhanced AS r", "on": "p.requisition_code = r.requisition_code", "using": []}] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(DISTINCT p.requisition_code) | [{"table": "lever__posting_enhanced", "column": "requisition_code"}] | [] | False |


## S46

类别 `data`；来源 `query_db`；调用 `c860790acb864a47b7804db0c344a168`；状态 `success`。

```sql
SELECT COUNT(DISTINCT r.team) as req_team_cnt
FROM lever__requisition_enhanced r
JOIN lever__posting_enhanced p ON r.team = p.categories_team
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-073/attempt-01/sql/S46.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-073/attempt-01/sql/S46.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-073/attempt-01/results/S46.rows.jsonl)；完整：True；SHA256：`acc07b62f23f458923737c4cd4a66bd05d1e71eb4f384003baaf2dcc760d6349`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "r", "kind": "base", "block": null, "base_tables": ["lever__requisition_enhanced"]}, {"alias": "p", "kind": "base", "block": null, "base_tables": ["lever__posting_enhanced"]}] | [{"type": "INNER", "right": "lever__posting_enhanced AS p", "on": "r.team = p.categories_team", "using": []}] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(DISTINCT r.team) | [{"table": "lever__requisition_enhanced", "column": "team"}] | [] | False |


## S47

类别 `data`；来源 `query_db`；调用 `1440de2f226846a8a7c97b8ec4dda309`；状态 `success`。

```sql
SELECT COUNT(DISTINCT r.team) as req_team_in_post_team
FROM lever__requisition_enhanced r
WHERE r.team IN (SELECT categories_team FROM lever__posting_enhanced)
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-073/attempt-01/sql/S47.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-073/attempt-01/sql/S47.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-073/attempt-01/results/S47.rows.jsonl)；完整：True；SHA256：`acc07b62f23f458923737c4cd4a66bd05d1e71eb4f384003baaf2dcc760d6349`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "lever__posting_enhanced", "kind": "base", "block": null, "base_tables": ["lever__posting_enhanced"]}] | [] | [] |
| B2 | [{"alias": "r", "kind": "base", "block": null, "base_tables": ["lever__requisition_enhanced"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B2 | COUNT(DISTINCT r.team) | [{"table": "lever__requisition_enhanced", "column": "team"}] | [] | False |


未解析列血缘：[{"block": "B2", "column": "categories_team", "reason": "ambiguous_or_missing_source"}]

## S48

类别 `data`；来源 `query_db`；调用 `db3c3f9dcf6147488067247ccd0e4248`；状态 `failed`。

```sql
SELECT COUNT(DISTINCT r.owner_name) as req_owner_cnt, COUNT(DISTINCT r.creator_name) as req_creator_cnt FROM lever__requisition_enhanced
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-073/attempt-01/sql/S48.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-073/attempt-01/sql/S48.parameters.json)。

错误：`OperationalError('no such column: r.owner_name')`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "lever__requisition_enhanced", "kind": "base", "block": null, "base_tables": ["lever__requisition_enhanced"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(DISTINCT r.owner_name) | [{"unknown": "r.owner_name"}] | [] | False |
| B1 | COUNT(DISTINCT r.creator_name) | [{"unknown": "r.creator_name"}] | [] | False |


未解析列血缘：[{"block": "B1", "column": "r.owner_name", "reason": "ambiguous_or_missing_source"}, {"block": "B1", "column": "r.creator_name", "reason": "ambiguous_or_missing_source"}, {"block": "B1", "column": "r.owner_name", "reason": "ambiguous_or_missing_source"}, {"block": "B1", "column": "r.creator_name", "reason": "ambiguous_or_missing_source"}]

## S49

类别 `data`；来源 `query_db`；调用 `a76f18da95c64fc2b1f62fdac751f20a`；状态 `failed`。

```sql
SELECT COUNT(DISTINCT p.posting_hiring_manager_name) as posting_hm_cnt FROM lever__posting_enhanced
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-073/attempt-01/sql/S49.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-073/attempt-01/sql/S49.parameters.json)。

错误：`OperationalError('no such column: p.posting_hiring_manager_name')`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "lever__posting_enhanced", "kind": "base", "block": null, "base_tables": ["lever__posting_enhanced"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(DISTINCT p.posting_hiring_manager_name) | [{"unknown": "p.posting_hiring_manager_name"}] | [] | False |


未解析列血缘：[{"block": "B1", "column": "p.posting_hiring_manager_name", "reason": "ambiguous_or_missing_source"}, {"block": "B1", "column": "p.posting_hiring_manager_name", "reason": "ambiguous_or_missing_source"}]

## S50

类别 `data`；来源 `query_db`；调用 `9ea9b8cf3e9a4d5882f8db7491d213e5`；状态 `success`。

```sql
SELECT COUNT(*) as overlap
FROM lever__requisition_enhanced r
WHERE r.owner_name IN (SELECT DISTINCT posting_hiring_manager_name FROM lever__posting_enhanced)
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-073/attempt-01/sql/S50.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-073/attempt-01/sql/S50.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-073/attempt-01/results/S50.rows.jsonl)；完整：True；SHA256：`89f4285370482f48a75a18fce754080be4f6764ff48618dad770c42d4dbee8c7`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "lever__posting_enhanced", "kind": "base", "block": null, "base_tables": ["lever__posting_enhanced"]}] | [] | [] |
| B2 | [{"alias": "r", "kind": "base", "block": null, "base_tables": ["lever__requisition_enhanced"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B2 | COUNT(*) | [] | [] | True |


未解析列血缘：[{"block": "B2", "column": "posting_hiring_manager_name", "reason": "ambiguous_or_missing_source"}]

## S51

类别 `data`；来源 `query_db`；调用 `5a74f82b046d498e8e450cb13b655a16`；状态 `success`。

```sql
SELECT r.owner_name, r.creator_name, r.hiring_manager_user_id
FROM lever__requisition_enhanced r
LIMIT 10
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-073/attempt-01/sql/S51.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-073/attempt-01/sql/S51.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-073/attempt-01/results/S51.rows.jsonl)；完整：True；SHA256：`9a6aec0cbe1ed6353c4ee8211ea9019c352f64bec508e0e7e68623ceb61f8b68`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "r", "kind": "base", "block": null, "base_tables": ["lever__requisition_enhanced"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |


## S52

类别 `data`；来源 `query_db`；调用 `4e60d73c14cc4b00bb7ca7a16c4e9fef`；状态 `success`。

```sql
SELECT posting_hiring_manager_name
FROM lever__posting_enhanced p
LIMIT 10
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-073/attempt-01/sql/S52.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-073/attempt-01/sql/S52.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-073/attempt-01/results/S52.rows.jsonl)；完整：True；SHA256：`8e85d48bee8d78cc5a72d83c97114ff9fbf743ff0fa39e43aec1e4dc1a4f8c17`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "p", "kind": "base", "block": null, "base_tables": ["lever__posting_enhanced"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |


## S53

类别 `data`；来源 `query_db`；调用 `b37e3720b8844af2869e39165bfa7782`；状态 `failed`。

```sql
SELECT COUNT(DISTINCT r.hiring_manager_user_id) as hm_cnt FROM lever__requisition_enhanced
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-073/attempt-01/sql/S53.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-073/attempt-01/sql/S53.parameters.json)。

错误：`OperationalError('no such column: r.hiring_manager_user_id')`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "lever__requisition_enhanced", "kind": "base", "block": null, "base_tables": ["lever__requisition_enhanced"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(DISTINCT r.hiring_manager_user_id) | [{"unknown": "r.hiring_manager_user_id"}] | [] | False |


未解析列血缘：[{"block": "B1", "column": "r.hiring_manager_user_id", "reason": "ambiguous_or_missing_source"}, {"block": "B1", "column": "r.hiring_manager_user_id", "reason": "ambiguous_or_missing_source"}]

## S54

类别 `data`；来源 `query_db`；调用 `374424fc5fe146e2be2493554345c252`；状态 `success`。

```sql
SELECT COUNT(DISTINCT r.hiring_manager_user_id) as matched_hm
FROM lever__requisition_enhanced r
WHERE r.hiring_manager_user_id IN (SELECT creator_user_id FROM lever__posting_enhanced)
   OR r.hiring_manager_user_id IN (SELECT owner_user_id FROM lever__posting_enhanced)
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-073/attempt-01/sql/S54.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-073/attempt-01/sql/S54.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-073/attempt-01/results/S54.rows.jsonl)；完整：True；SHA256：`5405bcc9751ace0f9485a2e56d44e0fd486c2d5c3242dfa83762f9b1e8cb1c3c`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "lever__posting_enhanced", "kind": "base", "block": null, "base_tables": ["lever__posting_enhanced"]}] | [] | [] |
| B2 | [{"alias": "lever__posting_enhanced", "kind": "base", "block": null, "base_tables": ["lever__posting_enhanced"]}] | [] | [] |
| B3 | [{"alias": "r", "kind": "base", "block": null, "base_tables": ["lever__requisition_enhanced"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B3 | COUNT(DISTINCT r.hiring_manager_user_id) | [{"table": "lever__requisition_enhanced", "column": "hiring_manager_user_id"}] | [] | False |


## S55

类别 `data`；来源 `query_db`；调用 `d9a0a86aecb444dfa20094d098c3ee40`；状态 `success`。

```sql
SELECT COUNT(*) as cnt
FROM lever__requisition_enhanced r
WHERE r.hiring_manager_user_id IN (SELECT creator_user_id FROM lever__posting_enhanced)
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-073/attempt-01/sql/S55.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-073/attempt-01/sql/S55.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-073/attempt-01/results/S55.rows.jsonl)；完整：True；SHA256：`44bd07ec0b7e5316d8d6caf1b9f3680158bbfbd0742d00b2f17c7434455172fd`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "lever__posting_enhanced", "kind": "base", "block": null, "base_tables": ["lever__posting_enhanced"]}] | [] | [] |
| B2 | [{"alias": "r", "kind": "base", "block": null, "base_tables": ["lever__requisition_enhanced"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B2 | COUNT(*) | [] | [] | True |


## S56

类别 `data`；来源 `query_db`；调用 `fb900d430e8b477bbd5bbd281e080d70`；状态 `success`。

```sql
SELECT COUNT(*) as cnt
FROM lever__requisition_enhanced r
WHERE r.hiring_manager_user_id IN (SELECT owner_user_id FROM lever__posting_enhanced)
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-073/attempt-01/sql/S56.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-073/attempt-01/sql/S56.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-073/attempt-01/results/S56.rows.jsonl)；完整：True；SHA256：`3a9d7406a7d937b1cc1d2a41d94c3d1c0ca1902ec3f690697f99f71305777600`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "lever__posting_enhanced", "kind": "base", "block": null, "base_tables": ["lever__posting_enhanced"]}] | [] | [] |
| B2 | [{"alias": "r", "kind": "base", "block": null, "base_tables": ["lever__requisition_enhanced"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B2 | COUNT(*) | [] | [] | True |


## S57

类别 `data`；来源 `query_db`；调用 `dc64f68c2f53431db1f76518c67136b1`；状态 `success`。

```sql
SELECT COUNT(DISTINCT hiring_manager_user_id) as hm_cnt FROM lever__requisition_enhanced
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-073/attempt-01/sql/S57.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-073/attempt-01/sql/S57.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-073/attempt-01/results/S57.rows.jsonl)；完整：True；SHA256：`ccc12cc4c2d8a3d471a67f40538641c3c569b2184ec6605de15cb91ea80f6043`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "lever__requisition_enhanced", "kind": "base", "block": null, "base_tables": ["lever__requisition_enhanced"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(DISTINCT hiring_manager_user_id) | [{"table": "lever__requisition_enhanced", "column": "hiring_manager_user_id"}] | [] | False |


## S58

类别 `data`；来源 `query_db`；调用 `c5689515a26c46b4b8f4e9bdecfe51ec`；状态 `success`。

```sql
SELECT p.categories_department, COUNT(DISTINCT p.owner_user_id) as owners, COUNT(DISTINCT p.creator_user_id) as creators
FROM lever__posting_enhanced p
GROUP BY p.categories_department
ORDER BY p.categories_department
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-073/attempt-01/sql/S58.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-073/attempt-01/sql/S58.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-073/attempt-01/results/S58.rows.jsonl)；完整：True；SHA256：`8d12af6e24c67d342fd5f9a85278671fb8b7f66dc84052c11226eb3b591e9867`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "p", "kind": "base", "block": null, "base_tables": ["lever__posting_enhanced"]}] | [] | ["p.categories_department"] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(DISTINCT p.owner_user_id) | [{"table": "lever__posting_enhanced", "column": "owner_user_id"}] | [] | False |
| B1 | COUNT(DISTINCT p.creator_user_id) | [{"table": "lever__posting_enhanced", "column": "creator_user_id"}] | [] | False |


## S59

类别 `data`；来源 `query_db`；调用 `32c0bff2f6ea402ea5bfd6d223515c15`；状态 `success`。

```sql
SELECT user_id, COUNT(DISTINCT categories_department) as dept_cnt
FROM (
  SELECT owner_user_id as user_id, categories_department FROM lever__posting_enhanced WHERE owner_user_id IS NOT NULL
  UNION ALL
  SELECT creator_user_id as user_id, categories_department FROM lever__posting_enhanced WHERE creator_user_id IS NOT NULL
)
GROUP BY user_id
HAVING dept_cnt > 1
LIMIT 10
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-073/attempt-01/sql/S59.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-073/attempt-01/sql/S59.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-073/attempt-01/results/S59.rows.jsonl)；完整：True；SHA256：`55e2738aa7205b174e1bee42ef8b7194e5187d3d0bd393f5d468a8dd7a20bf77`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "lever__posting_enhanced", "kind": "base", "block": null, "base_tables": ["lever__posting_enhanced"]}] | [] | [] |
| B2 | [{"alias": "lever__posting_enhanced", "kind": "base", "block": null, "base_tables": ["lever__posting_enhanced"]}] | [] | [] |
| B3 | [] | [] | [] |
| B4 | [{"alias": "", "kind": "derived", "block": "B3", "base_tables": ["lever__posting_enhanced"]}] | [] | ["user_id"] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B4 | COUNT(DISTINCT categories_department) | [{"table": "lever__posting_enhanced", "column": "categories_department"}, {"table": "lever__posting_enhanced", "column": "categories_department"}] | [] | False |


## S60

类别 `data`；来源 `query_db`；调用 `a0cb2d02ee384f398df8afeb4ad4d4da`；状态 `success`。

```sql
SELECT posting_hiring_manager_name, COUNT(DISTINCT categories_department) as dept_cnt, COUNT(*) as posting_cnt
FROM lever__posting_enhanced
GROUP BY posting_hiring_manager_name
HAVING dept_cnt > 1
ORDER BY posting_cnt DESC
LIMIT 15
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-073/attempt-01/sql/S60.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-073/attempt-01/sql/S60.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-073/attempt-01/results/S60.rows.jsonl)；完整：True；SHA256：`edd4ba2c02a474b8f38c394c0ecd47a856697648e87bc0d03dfadddd6f176d8b`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "lever__posting_enhanced", "kind": "base", "block": null, "base_tables": ["lever__posting_enhanced"]}] | [] | ["posting_hiring_manager_name"] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(DISTINCT categories_department) | [{"table": "lever__posting_enhanced", "column": "categories_department"}] | [] | False |
| B1 | COUNT(*) | [] | [] | True |


## S61

类别 `data`；来源 `query_db`；调用 `c5745f38d42e4f90a9eae008aabe57a9`；状态 `success`。

```sql
SELECT posting_hiring_manager_name, COUNT(DISTINCT categories_department) as dept_cnt, COUNT(*) as posting_cnt
FROM lever__posting_enhanced
GROUP BY posting_hiring_manager_name
HAVING dept_cnt = 1
ORDER BY posting_cnt DESC
LIMIT 15
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-073/attempt-01/sql/S61.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-073/attempt-01/sql/S61.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-073/attempt-01/results/S61.rows.jsonl)；完整：True；SHA256：`5266ebe58e5ae55e8b27dd9dae6638a7912c0e7fb8f155f6decf5d64963d1f7c`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "lever__posting_enhanced", "kind": "base", "block": null, "base_tables": ["lever__posting_enhanced"]}] | [] | ["posting_hiring_manager_name"] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(DISTINCT categories_department) | [{"table": "lever__posting_enhanced", "column": "categories_department"}] | [] | False |
| B1 | COUNT(*) | [] | [] | True |


## S62

类别 `data`；来源 `query_db`；调用 `2cf0962dc88b4ecca40e613c47efdde5`；状态 `success`。

```sql
SELECT COUNT(*) as total_hiring_managers
FROM (SELECT DISTINCT posting_hiring_manager_name FROM lever__posting_enhanced)
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-073/attempt-01/sql/S62.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-073/attempt-01/sql/S62.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-073/attempt-01/results/S62.rows.jsonl)；完整：True；SHA256：`b2fc15559ddc0657b7d9de50446cdd1529022e47707935df9b72609c350eda84`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "lever__posting_enhanced", "kind": "base", "block": null, "base_tables": ["lever__posting_enhanced"]}] | [] | [] |
| B2 | [{"alias": "", "kind": "derived", "block": "B1", "base_tables": ["lever__posting_enhanced"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B2 | COUNT(*) | [] | [] | True |


## S63

类别 `data`；来源 `query_db`；调用 `f0ecf216a4864573ae15cbed66b0e982`；状态 `success`。

```sql
SELECT COUNT(*) as single_dept_hms
FROM (
  SELECT posting_hiring_manager_name
  FROM lever__posting_enhanced
  GROUP BY posting_hiring_manager_name
  HAVING COUNT(DISTINCT categories_department) = 1
)
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-073/attempt-01/sql/S63.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-073/attempt-01/sql/S63.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-073/attempt-01/results/S63.rows.jsonl)；完整：True；SHA256：`d07c663d60f259d6d0d926bb43a2d21fbf8e1375d314434579359ab2882d80cc`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "lever__posting_enhanced", "kind": "base", "block": null, "base_tables": ["lever__posting_enhanced"]}] | [] | ["posting_hiring_manager_name"] |
| B2 | [{"alias": "", "kind": "derived", "block": "B1", "base_tables": ["lever__posting_enhanced"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(DISTINCT categories_department) | [{"table": "lever__posting_enhanced", "column": "categories_department"}] | [] | False |
| B2 | COUNT(*) | [] | [] | True |


## S64

类别 `data`；来源 `query_db`；调用 `68eb2e0298df48ecaff3893446cce2d3`；状态 `success`。

```sql
SELECT status,
       SUM(headcount_total) as total_headcount,
       SUM(headcount_hired) as total_hired,
       SUM(CASE WHEN headcount_infinite = 1 THEN 1 ELSE 0 END) as infinite_cnt,
       COUNT(*) as cnt
FROM lever__requisition_enhanced
GROUP BY status
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-073/attempt-01/sql/S64.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-073/attempt-01/sql/S64.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-073/attempt-01/results/S64.rows.jsonl)；完整：True；SHA256：`c578772718af51983f1b6ae80038916df0ae596b447709f4d599cc6aa1f338ee`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "lever__requisition_enhanced", "kind": "base", "block": null, "base_tables": ["lever__requisition_enhanced"]}] | [] | ["status"] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | SUM(headcount_total) | [{"table": "lever__requisition_enhanced", "column": "headcount_total"}] | [] | False |
| B1 | SUM(headcount_hired) | [{"table": "lever__requisition_enhanced", "column": "headcount_hired"}] | [] | False |
| B1 | SUM(CASE WHEN headcount_infinite = 1 THEN 1 ELSE 0 END) | [] | [{"table": "lever__requisition_enhanced", "column": "headcount_infinite"}] | False |
| B1 | COUNT(*) | [] | [] | True |


## S65

类别 `data`；来源 `query_db`；调用 `c5a370e31b1f41a59b7e32c61168948b`；状态 `success`。

```sql
SELECT status, headcount_total, headcount_hired, headcount_infinite
FROM lever__requisition_enhanced
WHERE status = 'open'
LIMIT 20
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-073/attempt-01/sql/S65.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-073/attempt-01/sql/S65.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-073/attempt-01/results/S65.rows.jsonl)；完整：True；SHA256：`d544cfc347aa46c9da3b44aafc496138bcd10170a1c2bc78db2c3a57be54455a`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "lever__requisition_enhanced", "kind": "base", "block": null, "base_tables": ["lever__requisition_enhanced"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |


## S66

类别 `data`；来源 `query_db`；调用 `56a047ec8a8947f59f62d9258f503f8c`；状态 `success`。

```sql
-- Get the most common department for each hiring manager
SELECT pm.hiring_manager_name, pm.categories_department, pm.cnt as dept_posting_cnt
FROM (
  SELECT posting_hiring_manager_name as hiring_manager_name, categories_department, COUNT(*) as cnt,
         ROW_NUMBER() OVER (PARTITION BY posting_hiring_manager_name ORDER BY COUNT(*) DESC) as rn
  FROM lever__posting_enhanced
  GROUP BY posting_hiring_manager_name, categories_department
) pm
WHERE pm.rn = 1
ORDER BY pm.hiring_manager_name
LIMIT 20
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-073/attempt-01/sql/S66.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-073/attempt-01/sql/S66.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-073/attempt-01/results/S66.rows.jsonl)；完整：True；SHA256：`b3fe7c8d12f2ea632008090b77d254607b915de305269cc3bf8569a09990dd49`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "lever__posting_enhanced", "kind": "base", "block": null, "base_tables": ["lever__posting_enhanced"]}] | [] | ["posting_hiring_manager_name", "categories_department"] |
| B2 | [{"alias": "pm", "kind": "derived", "block": "B1", "base_tables": ["lever__posting_enhanced"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |
| B1 | COUNT(*) | [] | [] | True |


## S67

类别 `data`；来源 `query_db`；调用 `1818ceb29d6040e99f464b0eeee85931`；状态 `success`。

```sql
-- Map requisition hiring managers to departments via posting user IDs
WITH user_dept AS (
  SELECT user_id, categories_department, cnt
  FROM (
    SELECT owner_user_id as user_id, categories_department, COUNT(*) as cnt
    FROM lever__posting_enhanced WHERE owner_user_id IS NOT NULL
    GROUP BY owner_user_id, categories_department
    UNION ALL
    SELECT creator_user_id as user_id, categories_department, COUNT(*) as cnt
    FROM lever__posting_enhanced WHERE creator_user_id IS NOT NULL
    GROUP BY creator_user_id, categories_department
  )
),
ranked AS (
  SELECT user_id, categories_department, SUM(cnt) as total_cnt,
         ROW_NUMBER() OVER (PARTITION BY user_id ORDER BY SUM(cnt) DESC) as rn
  FROM user_dept
  GROUP BY user_id, categories_department
)
SELECT categories_department, COUNT(DISTINCT user_id) as mapped_hms
FROM ranked
WHERE rn = 1
GROUP BY categories_department
ORDER BY categories_department
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-073/attempt-01/sql/S67.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-073/attempt-01/sql/S67.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-073/attempt-01/results/S67.rows.jsonl)；完整：True；SHA256：`43b169bb89cfcf0103b6f0e5b788443aa32f71dd96218d4a5611b26d3b39f6f6`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "lever__posting_enhanced", "kind": "base", "block": null, "base_tables": ["lever__posting_enhanced"]}] | [] | ["owner_user_id", "categories_department"] |
| B2 | [{"alias": "lever__posting_enhanced", "kind": "base", "block": null, "base_tables": ["lever__posting_enhanced"]}] | [] | ["creator_user_id", "categories_department"] |
| B3 | [] | [] | [] |
| B4 | [{"alias": "", "kind": "derived", "block": "B3", "base_tables": ["lever__posting_enhanced"]}] | [] | [] |
| B5 | [{"alias": "user_dept", "kind": "derived", "block": "B4", "base_tables": ["lever__posting_enhanced"]}] | [] | ["user_id", "categories_department"] |
| B6 | [{"alias": "ranked", "kind": "derived", "block": "B5", "base_tables": ["lever__posting_enhanced"]}] | [] | ["categories_department"] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |
| B2 | COUNT(*) | [] | [] | True |
| B5 | SUM(cnt) | [] | [] | False |
| B5 | SUM(cnt) | [] | [] | False |
| B6 | COUNT(DISTINCT user_id) | [{"table": "lever__posting_enhanced", "column": "owner_user_id"}, {"table": "lever__posting_enhanced", "column": "creator_user_id"}] | [] | False |


## S68

类别 `data`；来源 `query_db`；调用 `b4b85d5aac6148a49df2a7562a5bf019`；状态 `success`。

```sql
-- Map each requisition's hiring manager to a department
WITH user_dept AS (
  SELECT user_id, categories_department, cnt
  FROM (
    SELECT owner_user_id as user_id, categories_department, COUNT(*) as cnt
    FROM lever__posting_enhanced WHERE owner_user_id IS NOT NULL
    GROUP BY owner_user_id, categories_department
    UNION ALL
    SELECT creator_user_id as user_id, categories_department, COUNT(*) as cnt
    FROM lever__posting_enhanced WHERE creator_user_id IS NOT NULL
    GROUP BY creator_user_id, categories_department
  )
),
ranked AS (
  SELECT user_id, categories_department, SUM(cnt) as total_cnt,
         ROW_NUMBER() OVER (PARTITION BY user_id ORDER BY SUM(cnt) DESC) as rn
  FROM user_dept
  GROUP BY user_id, categories_department
),
hm_dept AS (
  SELECT user_id, categories_department FROM ranked WHERE rn = 1
)
SELECT COALESCE(hd.categories_department, 'Unmapped') as department,
       COUNT(*) as open_requisitions
FROM lever__requisition_enhanced r
LEFT JOIN hm_dept hd ON r.hiring_manager_user_id = hd.user_id
WHERE r.status = 'open'
GROUP BY COALESCE(hd.categories_department, 'Unmapped')
ORDER BY department
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-073/attempt-01/sql/S68.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-073/attempt-01/sql/S68.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-073/attempt-01/results/S68.rows.jsonl)；完整：True；SHA256：`ae5e35d8250918b20e8d03bd5e7ed8cc37aaaee97d7a470d5b2ce732187905d7`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "lever__posting_enhanced", "kind": "base", "block": null, "base_tables": ["lever__posting_enhanced"]}] | [] | ["owner_user_id", "categories_department"] |
| B2 | [{"alias": "lever__posting_enhanced", "kind": "base", "block": null, "base_tables": ["lever__posting_enhanced"]}] | [] | ["creator_user_id", "categories_department"] |
| B3 | [] | [] | [] |
| B4 | [{"alias": "", "kind": "derived", "block": "B3", "base_tables": ["lever__posting_enhanced"]}] | [] | [] |
| B5 | [{"alias": "user_dept", "kind": "derived", "block": "B4", "base_tables": ["lever__posting_enhanced"]}] | [] | ["user_id", "categories_department"] |
| B6 | [{"alias": "ranked", "kind": "derived", "block": "B5", "base_tables": ["lever__posting_enhanced"]}] | [] | [] |
| B7 | [{"alias": "r", "kind": "base", "block": null, "base_tables": ["lever__requisition_enhanced"]}, {"alias": "hd", "kind": "derived", "block": "B6", "base_tables": ["lever__posting_enhanced"]}] | [{"type": "LEFT", "right": "hm_dept AS hd", "on": "r.hiring_manager_user_id = hd.user_id", "using": []}] | ["COALESCE(hd.categories_department, 'Unmapped')"] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |
| B2 | COUNT(*) | [] | [] | True |
| B5 | SUM(cnt) | [] | [] | False |
| B5 | SUM(cnt) | [] | [] | False |
| B7 | COUNT(*) | [] | [] | True |


## S69

类别 `data`；来源 `query_db`；调用 `406fe4f2a18b473987b20e7afc2c5483`；状态 `success`。

```sql
SELECT categories_department,
       COUNT(DISTINCT posting_hiring_manager_name) as active_hms,
       COUNT(*) as active_postings
FROM lever__posting_enhanced
WHERE state IN ('published', 'pending')
GROUP BY categories_department
ORDER BY categories_department
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-073/attempt-01/sql/S69.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-073/attempt-01/sql/S69.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-073/attempt-01/results/S69.rows.jsonl)；完整：True；SHA256：`12cfde94d5c0a8f15eb85d86730d088c3ebfcb75df5bdd964182201060386fd6`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "lever__posting_enhanced", "kind": "base", "block": null, "base_tables": ["lever__posting_enhanced"]}] | [] | ["categories_department"] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(DISTINCT posting_hiring_manager_name) | [{"table": "lever__posting_enhanced", "column": "posting_hiring_manager_name"}] | [] | False |
| B1 | COUNT(*) | [] | [] | True |


## S70

类别 `data`；来源 `query_db`；调用 `8cc04fe4fc324b2f9201629eb284eedf`；状态 `success`。

```sql
SELECT categories_department,
       COUNT(DISTINCT posting_hiring_manager_name) as all_hms,
       COUNT(*) as all_postings
FROM lever__posting_enhanced
GROUP BY categories_department
ORDER BY categories_department
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-073/attempt-01/sql/S70.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-073/attempt-01/sql/S70.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-073/attempt-01/results/S70.rows.jsonl)；完整：True；SHA256：`ce673c2c4c6e9948ceaa355544e221328fe26a1da7768569f15e5c7faf5423f6`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "lever__posting_enhanced", "kind": "base", "block": null, "base_tables": ["lever__posting_enhanced"]}] | [] | ["categories_department"] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(DISTINCT posting_hiring_manager_name) | [{"table": "lever__posting_enhanced", "column": "posting_hiring_manager_name"}] | [] | False |
| B1 | COUNT(*) | [] | [] | True |


## S71

类别 `data`；来源 `query_db`；调用 `428c766e14d849aba52334353c7cb1e7`；状态 `success`。

```sql
-- Map each requisition to a department and count open + on-hold
WITH user_dept AS (
  SELECT user_id, categories_department, cnt
  FROM (
    SELECT owner_user_id as user_id, categories_department, COUNT(*) as cnt
    FROM lever__posting_enhanced WHERE owner_user_id IS NOT NULL
    GROUP BY owner_user_id, categories_department
    UNION ALL
    SELECT creator_user_id as user_id, categories_department, COUNT(*) as cnt
    FROM lever__posting_enhanced WHERE creator_user_id IS NOT NULL
    GROUP BY creator_user_id, categories_department
  )
),
ranked AS (
  SELECT user_id, categories_department, SUM(cnt) as total_cnt,
         ROW_NUMBER() OVER (PARTITION BY user_id ORDER BY SUM(cnt) DESC) as rn
  FROM user_dept
  GROUP BY user_id, categories_department
),
hm_dept AS (
  SELECT user_id, categories_department FROM ranked WHERE rn = 1
)
SELECT COALESCE(hd.categories_department, 'Unmapped') as department,
       COUNT(*) as pending_roles,
       SUM(CASE WHEN r.status = 'open' THEN 1 ELSE 0 END) as open_cnt,
       SUM(CASE WHEN r.status = 'on-hold' THEN 1 ELSE 0 END) as onhold_cnt
FROM lever__requisition_enhanced r
LEFT JOIN hm_dept hd ON r.hiring_manager_user_id = hd.user_id
WHERE r.status IN ('open', 'on-hold')
GROUP BY COALESCE(hd.categories_department, 'Unmapped')
ORDER BY department
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-073/attempt-01/sql/S71.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-073/attempt-01/sql/S71.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-073/attempt-01/results/S71.rows.jsonl)；完整：True；SHA256：`c700e27938ffc062198e04ea2d252ee64f707d6d39f45f499e02304dbc4f0b5c`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "lever__posting_enhanced", "kind": "base", "block": null, "base_tables": ["lever__posting_enhanced"]}] | [] | ["owner_user_id", "categories_department"] |
| B2 | [{"alias": "lever__posting_enhanced", "kind": "base", "block": null, "base_tables": ["lever__posting_enhanced"]}] | [] | ["creator_user_id", "categories_department"] |
| B3 | [] | [] | [] |
| B4 | [{"alias": "", "kind": "derived", "block": "B3", "base_tables": ["lever__posting_enhanced"]}] | [] | [] |
| B5 | [{"alias": "user_dept", "kind": "derived", "block": "B4", "base_tables": ["lever__posting_enhanced"]}] | [] | ["user_id", "categories_department"] |
| B6 | [{"alias": "ranked", "kind": "derived", "block": "B5", "base_tables": ["lever__posting_enhanced"]}] | [] | [] |
| B7 | [{"alias": "r", "kind": "base", "block": null, "base_tables": ["lever__requisition_enhanced"]}, {"alias": "hd", "kind": "derived", "block": "B6", "base_tables": ["lever__posting_enhanced"]}] | [{"type": "LEFT", "right": "hm_dept AS hd", "on": "r.hiring_manager_user_id = hd.user_id", "using": []}] | ["COALESCE(hd.categories_department, 'Unmapped')"] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |
| B2 | COUNT(*) | [] | [] | True |
| B5 | SUM(cnt) | [] | [] | False |
| B5 | SUM(cnt) | [] | [] | False |
| B7 | COUNT(*) | [] | [] | True |
| B7 | SUM(CASE WHEN r.status = 'open' THEN 1 ELSE 0 END) | [] | [{"table": "lever__requisition_enhanced", "column": "status"}] | False |
| B7 | SUM(CASE WHEN r.status = 'on-hold' THEN 1 ELSE 0 END) | [] | [{"table": "lever__requisition_enhanced", "column": "status"}] | False |


## S72

类别 `data`；来源 `query_db`；调用 `a78f21e3c1384b5fa5349e6624f41a44`；状态 `success`。

```sql
SELECT categories_department,
       COUNT(*) as total_postings,
       COUNT(DISTINCT posting_hiring_manager_name) as distinct_hms,
       ROUND(1.0*COUNT(*) / COUNT(DISTINCT posting_hiring_manager_name), 2) as postings_per_hm
FROM lever__posting_enhanced
WHERE state IN ('published', 'pending')
GROUP BY categories_department
ORDER BY categories_department
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-073/attempt-01/sql/S72.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-073/attempt-01/sql/S72.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-073/attempt-01/results/S72.rows.jsonl)；完整：True；SHA256：`c19678cbc4835e203a3f2d8eaa91fb611ad2dc2771dd9df8805122d51d8d388d`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "lever__posting_enhanced", "kind": "base", "block": null, "base_tables": ["lever__posting_enhanced"]}] | [] | ["categories_department"] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |
| B1 | COUNT(DISTINCT posting_hiring_manager_name) | [{"table": "lever__posting_enhanced", "column": "posting_hiring_manager_name"}] | [] | False |
| B1 | COUNT(DISTINCT posting_hiring_manager_name) | [{"table": "lever__posting_enhanced", "column": "posting_hiring_manager_name"}] | [] | False |
| B1 | COUNT(*) | [] | [] | True |


## S73

类别 `data`；来源 `query_db`；调用 `5e9bed76c7f745a2a1881fa1d22a89bc`；状态 `success`。

```sql
SELECT status, 
       SUM(count_postings) as total_postings,
       SUM(count_offers) as total_offers
FROM lever__requisition_enhanced
GROUP BY status
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-073/attempt-01/sql/S73.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-073/attempt-01/sql/S73.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-073/attempt-01/results/S73.rows.jsonl)；完整：True；SHA256：`dafb1228c8f0bc51479b7b9d93308587717c8ef251f1f0853f63365a3d1e613c`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "lever__requisition_enhanced", "kind": "base", "block": null, "base_tables": ["lever__requisition_enhanced"]}] | [] | ["status"] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | SUM(count_postings) | [{"table": "lever__requisition_enhanced", "column": "count_postings"}] | [] | False |
| B1 | SUM(count_offers) | [{"table": "lever__requisition_enhanced", "column": "count_offers"}] | [] | False |


## S74

类别 `data`；来源 `query_db`；调用 `8f747b13bf244c8898fc89f54d9325c5`；状态 `success`。

```sql
SELECT status, count_postings, count_offers, headcount_total, headcount_hired, headcount_infinite
FROM lever__requisition_enhanced
WHERE status = 'open'
LIMIT 15
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-073/attempt-01/sql/S74.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-073/attempt-01/sql/S74.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-073/attempt-01/results/S74.rows.jsonl)；完整：True；SHA256：`5d6c796d71d6b0156f69cc123c8841f887afe2e16f3234679c0fe86cc49a224a`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "lever__requisition_enhanced", "kind": "base", "block": null, "base_tables": ["lever__requisition_enhanced"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |


## S75

类别 `data`；来源 `query_db`；调用 `a94e5dc40fab4b63afe0f8c1f323ceb1`；状态 `success`。

```sql
SELECT categories_department,
       SUM(count_requisitions) as total_requisitions,
       SUM(count_opportunities) as total_opportunities,
       SUM(count_open_opportunities) as total_open_opportunities,
       SUM(count_interviews) as total_interviews
FROM lever__posting_enhanced
GROUP BY categories_department
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-073/attempt-01/sql/S75.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-073/attempt-01/sql/S75.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-073/attempt-01/results/S75.rows.jsonl)；完整：True；SHA256：`651d7ba910a4bd2cbb4287f8e511c6f3de1bfa68a853d952a00c6f46529bff5c`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "lever__posting_enhanced", "kind": "base", "block": null, "base_tables": ["lever__posting_enhanced"]}] | [] | ["categories_department"] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | SUM(count_requisitions) | [{"table": "lever__posting_enhanced", "column": "count_requisitions"}] | [] | False |
| B1 | SUM(count_opportunities) | [{"table": "lever__posting_enhanced", "column": "count_opportunities"}] | [] | False |
| B1 | SUM(count_open_opportunities) | [{"table": "lever__posting_enhanced", "column": "count_open_opportunities"}] | [] | False |
| B1 | SUM(count_interviews) | [{"table": "lever__posting_enhanced", "column": "count_interviews"}] | [] | False |


## S76

类别 `data`；来源 `query_db`；调用 `60bbe3df9237415bb2648f00a358fac3`；状态 `success`。

```sql
SELECT headcount_total, headcount_hired, headcount_infinite, COUNT(*) as cnt
FROM lever__requisition_enhanced
WHERE status = 'open'
GROUP BY headcount_total, headcount_hired, headcount_infinite
ORDER BY cnt DESC
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-073/attempt-01/sql/S76.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-073/attempt-01/sql/S76.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-073/attempt-01/results/S76.rows.jsonl)；完整：True；SHA256：`cfd2f8f114338596ba97b77c9db3a8685bbfb42a5321e0f17fe542ab045cc497`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "lever__requisition_enhanced", "kind": "base", "block": null, "base_tables": ["lever__requisition_enhanced"]}] | [] | ["headcount_total", "headcount_hired", "headcount_infinite"] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |


## S77

类别 `data`；来源 `query_db`；调用 `253f061cf6484b189b00ccbb13c81dd4`；状态 `success`。

```sql
SELECT postings_per_hm, COUNT(*) as num_managers
FROM (
  SELECT posting_hiring_manager_name, COUNT(*) as postings_per_hm
  FROM lever__posting_enhanced
  GROUP BY posting_hiring_manager_name
)
GROUP BY postings_per_hm
ORDER BY postings_per_hm DESC
LIMIT 15
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-073/attempt-01/sql/S77.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-073/attempt-01/sql/S77.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-073/attempt-01/results/S77.rows.jsonl)；完整：True；SHA256：`c8b87911815b6299c31d33121e5f010a099a86bb7142958b982808f194ba7606`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "lever__posting_enhanced", "kind": "base", "block": null, "base_tables": ["lever__posting_enhanced"]}] | [] | ["posting_hiring_manager_name"] |
| B2 | [{"alias": "", "kind": "derived", "block": "B1", "base_tables": ["lever__posting_enhanced"]}] | [] | ["postings_per_hm"] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |
| B2 | COUNT(*) | [] | [] | True |


## S78

类别 `data`；来源 `query_db`；调用 `3f0befb021a54c8588ead2f76eb7c7ea`；状态 `success`。

```sql
SELECT SUM(headcount_total) as sum_total, SUM(headcount_hired) as sum_hired, SUM(CASE WHEN headcount_infinite=1 THEN 1 ELSE 0 END) as inf_cnt FROM lever__requisition_enhanced
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-073/attempt-01/sql/S78.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-073/attempt-01/sql/S78.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-073/attempt-01/results/S78.rows.jsonl)；完整：True；SHA256：`3ee25969c5db40fe781f400190636823b7c6755922de7a03838e3cdb361c0e1f`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "lever__requisition_enhanced", "kind": "base", "block": null, "base_tables": ["lever__requisition_enhanced"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | SUM(headcount_total) | [{"table": "lever__requisition_enhanced", "column": "headcount_total"}] | [] | False |
| B1 | SUM(headcount_hired) | [{"table": "lever__requisition_enhanced", "column": "headcount_hired"}] | [] | False |
| B1 | SUM(CASE WHEN headcount_infinite = 1 THEN 1 ELSE 0 END) | [] | [{"table": "lever__requisition_enhanced", "column": "headcount_infinite"}] | False |


## S79

类别 `data`；来源 `query_db`；调用 `f9776158cd154e388b2ad4581da57236`；状态 `success`。

```sql
SELECT SUM(headcount_total) as sum_total, SUM(headcount_hired) as sum_hired, SUM(CASE WHEN headcount_infinite=1 THEN 1 ELSE 0 END) as inf_cnt FROM lever__requisition_enhanced WHERE status='open'
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-073/attempt-01/sql/S79.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-073/attempt-01/sql/S79.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-073/attempt-01/results/S79.rows.jsonl)；完整：True；SHA256：`632134c6331f6cb89838b374a6a2d09161c8d4e99a716fdba11cb20e556691c0`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "lever__requisition_enhanced", "kind": "base", "block": null, "base_tables": ["lever__requisition_enhanced"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | SUM(headcount_total) | [{"table": "lever__requisition_enhanced", "column": "headcount_total"}] | [] | False |
| B1 | SUM(headcount_hired) | [{"table": "lever__requisition_enhanced", "column": "headcount_hired"}] | [] | False |
| B1 | SUM(CASE WHEN headcount_infinite = 1 THEN 1 ELSE 0 END) | [] | [{"table": "lever__requisition_enhanced", "column": "headcount_infinite"}] | False |


## S80

类别 `data`；来源 `query_db`；调用 `a343606fd97b4e72a92c990ba224c32a`；状态 `success`。

```sql
SELECT substr(created_at, 1, 7) as ym, categories_department, COUNT(*) as cnt
FROM lever__posting_enhanced
GROUP BY categories_department, substr(created_at, 1, 7)
ORDER BY categories_department, ym
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-073/attempt-01/sql/S80.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-073/attempt-01/sql/S80.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-073/attempt-01/results/S80.rows.jsonl)；完整：True；SHA256：`c76d6786e4bdedf9d3371e35a30eef56065b78a48804f18d3d06e5c74424644e`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "lever__posting_enhanced", "kind": "base", "block": null, "base_tables": ["lever__posting_enhanced"]}] | [] | ["categories_department", "SUBSTRING(created_at, 1, 7)"] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |


## S81

类别 `data`；来源 `python`；调用 `59c1d603a7c847adbfec9991361b9817`；状态 `success`。

```sql
SELECT substr(created_at, 1, 7) as ym, categories_department, COUNT(*) as cnt FROM lever__posting_enhanced GROUP BY categories_department, substr(created_at, 1, 7) ORDER BY categories_department, ym
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-073/attempt-01/sql/S81.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-073/attempt-01/sql/S81.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-073/attempt-01/results/S81.rows.jsonl)；完整：True；SHA256：`c76d6786e4bdedf9d3371e35a30eef56065b78a48804f18d3d06e5c74424644e`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "lever__posting_enhanced", "kind": "base", "block": null, "base_tables": ["lever__posting_enhanced"]}] | [] | ["categories_department", "SUBSTRING(created_at, 1, 7)"] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |


## S82

类别 `data`；来源 `query_db`；调用 `abd2f3c33cf94fef858904e84679cc45`；状态 `success`。

```sql
-- Map open requisitions to departments via hiring manager user ID -> posting owner/creator -> dept
WITH user_dept AS (
  SELECT user_id, categories_department, cnt
  FROM (
    SELECT owner_user_id as user_id, categories_department, COUNT(*) as cnt
    FROM lever__posting_enhanced WHERE owner_user_id IS NOT NULL
    GROUP BY owner_user_id, categories_department
    UNION ALL
    SELECT creator_user_id as user_id, categories_department, COUNT(*) as cnt
    FROM lever__posting_enhanced WHERE creator_user_id IS NOT NULL
    GROUP BY creator_user_id, categories_department
  )
),
ranked AS (
  SELECT user_id, categories_department, SUM(cnt) as total_cnt,
         ROW_NUMBER() OVER (PARTITION BY user_id ORDER BY SUM(cnt) DESC) as rn
  FROM user_dept
  GROUP BY user_id, categories_department
),
hm_dept AS (
  SELECT user_id, categories_department FROM ranked WHERE rn = 1
)
SELECT COALESCE(hd.categories_department, 'Unmapped') as department,
       COUNT(*) as open_reqs,
       SUM(r.count_postings) as total_posting_attached,
       SUM(r.count_offers) as total_offers
FROM lever__requisition_enhanced r
LEFT JOIN hm_dept hd ON r.hiring_manager_user_id = hd.user_id
WHERE r.status = 'open'
GROUP BY COALESCE(hd.categories_department, 'Unmapped')
ORDER BY department
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-073/attempt-01/sql/S82.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-073/attempt-01/sql/S82.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-073/attempt-01/results/S82.rows.jsonl)；完整：True；SHA256：`b75d15f126f827ec89ded1eb8e1f3ab50916ce03fc5bbe1d414e22ed26bf44f5`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "lever__posting_enhanced", "kind": "base", "block": null, "base_tables": ["lever__posting_enhanced"]}] | [] | ["owner_user_id", "categories_department"] |
| B2 | [{"alias": "lever__posting_enhanced", "kind": "base", "block": null, "base_tables": ["lever__posting_enhanced"]}] | [] | ["creator_user_id", "categories_department"] |
| B3 | [] | [] | [] |
| B4 | [{"alias": "", "kind": "derived", "block": "B3", "base_tables": ["lever__posting_enhanced"]}] | [] | [] |
| B5 | [{"alias": "user_dept", "kind": "derived", "block": "B4", "base_tables": ["lever__posting_enhanced"]}] | [] | ["user_id", "categories_department"] |
| B6 | [{"alias": "ranked", "kind": "derived", "block": "B5", "base_tables": ["lever__posting_enhanced"]}] | [] | [] |
| B7 | [{"alias": "r", "kind": "base", "block": null, "base_tables": ["lever__requisition_enhanced"]}, {"alias": "hd", "kind": "derived", "block": "B6", "base_tables": ["lever__posting_enhanced"]}] | [{"type": "LEFT", "right": "hm_dept AS hd", "on": "r.hiring_manager_user_id = hd.user_id", "using": []}] | ["COALESCE(hd.categories_department, 'Unmapped')"] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |
| B2 | COUNT(*) | [] | [] | True |
| B5 | SUM(cnt) | [] | [] | False |
| B5 | SUM(cnt) | [] | [] | False |
| B7 | COUNT(*) | [] | [] | True |
| B7 | SUM(r.count_postings) | [{"table": "lever__requisition_enhanced", "column": "count_postings"}] | [] | False |
| B7 | SUM(r.count_offers) | [{"table": "lever__requisition_enhanced", "column": "count_offers"}] | [] | False |


## S83

类别 `data`；来源 `query_db`；调用 `0517cb9353d44239a7888cc7519cda32`；状态 `success`。

```sql
-- Map all requisitions to departments and compute metrics
WITH user_dept AS (
  SELECT user_id, categories_department, cnt
  FROM (
    SELECT owner_user_id as user_id, categories_department, COUNT(*) as cnt
    FROM lever__posting_enhanced WHERE owner_user_id IS NOT NULL
    GROUP BY owner_user_id, categories_department
    UNION ALL
    SELECT creator_user_id as user_id, categories_department, COUNT(*) as cnt
    FROM lever__posting_enhanced WHERE creator_user_id IS NOT NULL
    GROUP BY creator_user_id, categories_department
  )
),
ranked AS (
  SELECT user_id, categories_department, SUM(cnt) as total_cnt,
         ROW_NUMBER() OVER (PARTITION BY user_id ORDER BY SUM(cnt) DESC) as rn
  FROM user_dept
  GROUP BY user_id, categories_department
),
hm_dept AS (
  SELECT user_id, categories_department FROM ranked WHERE rn = 1
)
SELECT COALESCE(hd.categories_department, 'Unmapped') as department,
       COUNT(*) as req_cnt,
       SUM(CASE WHEN r.status = 'open' THEN 1 ELSE 0 END) as open_cnt,
       SUM(CASE WHEN r.status = 'on-hold' THEN 1 ELSE 0 END) as onhold_cnt,
       SUM(CASE WHEN r.status IN ('open', 'on-hold') THEN r.count_postings ELSE 0 END) as total_pending_postings
FROM lever__requisition_enhanced r
LEFT JOIN hm_dept hd ON r.hiring_manager_user_id = hd.user_id
GROUP BY COALESCE(hd.categories_department, 'Unmapped')
ORDER BY department
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-073/attempt-01/sql/S83.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-073/attempt-01/sql/S83.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-073/attempt-01/results/S83.rows.jsonl)；完整：True；SHA256：`d2eca69f52bb5b88b53d1b6413b6fd03921f614c8fc9b3d7a8f0e36e2219ce9b`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "lever__posting_enhanced", "kind": "base", "block": null, "base_tables": ["lever__posting_enhanced"]}] | [] | ["owner_user_id", "categories_department"] |
| B2 | [{"alias": "lever__posting_enhanced", "kind": "base", "block": null, "base_tables": ["lever__posting_enhanced"]}] | [] | ["creator_user_id", "categories_department"] |
| B3 | [] | [] | [] |
| B4 | [{"alias": "", "kind": "derived", "block": "B3", "base_tables": ["lever__posting_enhanced"]}] | [] | [] |
| B5 | [{"alias": "user_dept", "kind": "derived", "block": "B4", "base_tables": ["lever__posting_enhanced"]}] | [] | ["user_id", "categories_department"] |
| B6 | [{"alias": "ranked", "kind": "derived", "block": "B5", "base_tables": ["lever__posting_enhanced"]}] | [] | [] |
| B7 | [{"alias": "r", "kind": "base", "block": null, "base_tables": ["lever__requisition_enhanced"]}, {"alias": "hd", "kind": "derived", "block": "B6", "base_tables": ["lever__posting_enhanced"]}] | [{"type": "LEFT", "right": "hm_dept AS hd", "on": "r.hiring_manager_user_id = hd.user_id", "using": []}] | ["COALESCE(hd.categories_department, 'Unmapped')"] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |
| B2 | COUNT(*) | [] | [] | True |
| B5 | SUM(cnt) | [] | [] | False |
| B5 | SUM(cnt) | [] | [] | False |
| B7 | COUNT(*) | [] | [] | True |
| B7 | SUM(CASE WHEN r.status = 'open' THEN 1 ELSE 0 END) | [] | [{"table": "lever__requisition_enhanced", "column": "status"}] | False |
| B7 | SUM(CASE WHEN r.status = 'on-hold' THEN 1 ELSE 0 END) | [] | [{"table": "lever__requisition_enhanced", "column": "status"}] | False |
| B7 | SUM(CASE WHEN r.status IN ('open', 'on-hold') THEN r.count_postings ELSE 0 END) | [{"table": "lever__requisition_enhanced", "column": "count_postings"}] | [{"table": "lever__requisition_enhanced", "column": "status"}] | False |


## S84

类别 `data`；来源 `python`；调用 `dc97c85ddb1245b6b8ccd88cdf18787f`；状态 `success`。

```sql
SELECT * FROM lever__posting_enhanced
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-073/attempt-01/sql/S84.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-073/attempt-01/sql/S84.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-073/attempt-01/results/S84.rows.jsonl)；完整：True；SHA256：`4e7e7d5e7c201b716eced37d4bcbbc36c3b9095d4c7e911d91536621707183fb`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "lever__posting_enhanced", "kind": "base", "block": null, "base_tables": ["lever__posting_enhanced"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |


## S85

类别 `data`；来源 `python`；调用 `dc97c85ddb1245b6b8ccd88cdf18787f`；状态 `success`。

```sql
SELECT * FROM lever__requisition_enhanced
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-073/attempt-01/sql/S85.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-073/attempt-01/sql/S85.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-073/attempt-01/results/S85.rows.jsonl)；完整：True；SHA256：`039b48c891ae91d46acd4fd2518ab3b96aef985e28ddee656f602c79b133c9bc`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "lever__requisition_enhanced", "kind": "base", "block": null, "base_tables": ["lever__requisition_enhanced"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |


## S86

类别 `data`；来源 `python`；调用 `512f8d3e334e4366ba4fe28d64a04153`；状态 `success`。

```sql
SELECT * FROM lever__posting_enhanced
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-073/attempt-01/sql/S86.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-073/attempt-01/sql/S86.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-073/attempt-01/results/S86.rows.jsonl)；完整：True；SHA256：`4e7e7d5e7c201b716eced37d4bcbbc36c3b9095d4c7e911d91536621707183fb`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "lever__posting_enhanced", "kind": "base", "block": null, "base_tables": ["lever__posting_enhanced"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |


## S87

类别 `data`；来源 `query_db`；调用 `abf2fe974a1b40bd85ffaabf3e38bee4`；状态 `success`。

```sql
SELECT categories_department, state, COUNT(*) as cnt
FROM lever__posting_enhanced
WHERE categories_department = 'Marketing'
GROUP BY categories_department, state
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-073/attempt-01/sql/S87.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-073/attempt-01/sql/S87.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-073/attempt-01/results/S87.rows.jsonl)；完整：True；SHA256：`d55aed3ef59a5517199b5f1326e0f6899c5a84262d739e3827b824ffd22b93b0`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "lever__posting_enhanced", "kind": "base", "block": null, "base_tables": ["lever__posting_enhanced"]}] | [] | ["categories_department", "state"] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |


## S88

类别 `data`；来源 `query_db`；调用 `fd1ecc3f7fc84045a228d9f944cade0b`；状态 `success`。

```sql
SELECT categories_department, state, COUNT(*) as cnt
FROM lever__posting_enhanced
GROUP BY categories_department, state
ORDER BY categories_department, state
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-073/attempt-01/sql/S88.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-073/attempt-01/sql/S88.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-073/attempt-01/results/S88.rows.jsonl)；完整：True；SHA256：`f8a9437507a1c2291c0c3b5caf95934f3e8b4f1c5e8184e381107b2ee4ce4f5b`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "lever__posting_enhanced", "kind": "base", "block": null, "base_tables": ["lever__posting_enhanced"]}] | [] | ["categories_department", "state"] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |


## S89

类别 `data`；来源 `python`；调用 `05b45c65dbb0401db66393f0e4c76ec2`；状态 `success`。

```sql
SELECT categories_department, state, COUNT(*) as cnt FROM lever__posting_enhanced GROUP BY categories_department, state ORDER BY categories_department, state
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-073/attempt-01/sql/S89.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-073/attempt-01/sql/S89.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-073/attempt-01/results/S89.rows.jsonl)；完整：True；SHA256：`f8a9437507a1c2291c0c3b5caf95934f3e8b4f1c5e8184e381107b2ee4ce4f5b`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "lever__posting_enhanced", "kind": "base", "block": null, "base_tables": ["lever__posting_enhanced"]}] | [] | ["categories_department", "state"] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |


## S90

类别 `data`；来源 `python`；调用 `fbef98fb066743118767490d4b1978db`；状态 `success`。

```sql
SELECT * FROM lever__posting_enhanced
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-073/attempt-01/sql/S90.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-073/attempt-01/sql/S90.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-073/attempt-01/results/S90.rows.jsonl)；完整：True；SHA256：`4e7e7d5e7c201b716eced37d4bcbbc36c3b9095d4c7e911d91536621707183fb`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "lever__posting_enhanced", "kind": "base", "block": null, "base_tables": ["lever__posting_enhanced"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |


## S91

类别 `data`；来源 `python`；调用 `fbef98fb066743118767490d4b1978db`；状态 `success`。

```sql
SELECT * FROM lever__requisition_enhanced
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-073/attempt-01/sql/S91.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-073/attempt-01/sql/S91.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-073/attempt-01/results/S91.rows.jsonl)；完整：True；SHA256：`039b48c891ae91d46acd4fd2518ab3b96aef985e28ddee656f602c79b133c9bc`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "lever__requisition_enhanced", "kind": "base", "block": null, "base_tables": ["lever__requisition_enhanced"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |


## S92

类别 `data`；来源 `python`；调用 `e1b1c7c8dbb54cacab27285ad385229c`；状态 `success`。

```sql
SELECT * FROM lever__posting_enhanced
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-073/attempt-01/sql/S92.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-073/attempt-01/sql/S92.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-073/attempt-01/results/S92.rows.jsonl)；完整：True；SHA256：`4e7e7d5e7c201b716eced37d4bcbbc36c3b9095d4c7e911d91536621707183fb`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "lever__posting_enhanced", "kind": "base", "block": null, "base_tables": ["lever__posting_enhanced"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |


## S93

类别 `data`；来源 `python`；调用 `e1b1c7c8dbb54cacab27285ad385229c`；状态 `success`。

```sql
SELECT * FROM lever__requisition_enhanced
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-073/attempt-01/sql/S93.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-073/attempt-01/sql/S93.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-073/attempt-01/results/S93.rows.jsonl)；完整：True；SHA256：`039b48c891ae91d46acd4fd2518ab3b96aef985e28ddee656f602c79b133c9bc`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "lever__requisition_enhanced", "kind": "base", "block": null, "base_tables": ["lever__requisition_enhanced"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |


## S94

类别 `data`；来源 `python`；调用 `6a55cd68a93d456db394e57441a42b28`；状态 `success`。

```sql
SELECT * FROM lever__posting_enhanced
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-073/attempt-01/sql/S94.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-073/attempt-01/sql/S94.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-073/attempt-01/results/S94.rows.jsonl)；完整：True；SHA256：`4e7e7d5e7c201b716eced37d4bcbbc36c3b9095d4c7e911d91536621707183fb`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "lever__posting_enhanced", "kind": "base", "block": null, "base_tables": ["lever__posting_enhanced"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |


## S95

类别 `data`；来源 `python`；调用 `6a55cd68a93d456db394e57441a42b28`；状态 `success`。

```sql
SELECT * FROM lever__requisition_enhanced
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-073/attempt-01/sql/S95.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-073/attempt-01/sql/S95.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-073/attempt-01/results/S95.rows.jsonl)；完整：True；SHA256：`039b48c891ae91d46acd4fd2518ab3b96aef985e28ddee656f602c79b133c9bc`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "lever__requisition_enhanced", "kind": "base", "block": null, "base_tables": ["lever__requisition_enhanced"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |


## S96

类别 `data`；来源 `python`；调用 `8be6c745e0a94997a5fef35740c15e4b`；状态 `success`。

```sql
SELECT * FROM lever__posting_enhanced
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-073/attempt-01/sql/S96.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-073/attempt-01/sql/S96.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-073/attempt-01/results/S96.rows.jsonl)；完整：True；SHA256：`4e7e7d5e7c201b716eced37d4bcbbc36c3b9095d4c7e911d91536621707183fb`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "lever__posting_enhanced", "kind": "base", "block": null, "base_tables": ["lever__posting_enhanced"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |


## S97

类别 `data`；来源 `python`；调用 `8be6c745e0a94997a5fef35740c15e4b`；状态 `success`。

```sql
SELECT * FROM lever__requisition_enhanced
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-073/attempt-01/sql/S97.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-073/attempt-01/sql/S97.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-073/attempt-01/results/S97.rows.jsonl)；完整：True；SHA256：`039b48c891ae91d46acd4fd2518ab3b96aef985e28ddee656f602c79b133c9bc`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "lever__requisition_enhanced", "kind": "base", "block": null, "base_tables": ["lever__requisition_enhanced"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |

