# dacomp-083

I need you to build a comprehensive employee value and risk assessment system to support t…

运行：已提交。官方未评分。全部 SQL 尝试/成功 65/64；数据 SQL 63/62；Python 2 次。

完整原题：

I need you to build a comprehensive employee value and risk assessment system to support the optimization of human resources decisions. First, define "core employees" as those with an `overall_employee_score` greater than 75 and a `career_development_score` exceeding the median. Then, conduct a deep-dive profile analysis of these core employees based on multi-dimensional features such as `age`, `tenure_years`, `marital_status`, `ethnicity_codes`, `total_positions_held`, `total_promotions`, `lateral_moves`, and `management_positions_held`. Next, perform a cross-group analysis by `career_phase` (Early/Mid/Senior Career) and `employee_maturity_segment` (New Hire/Developing/Established/Veteran) to analyze the distribution pattern of high `employee_risk_level` in each combination. Further explore the associated characteristics of these high-risk core employees across organizational environmental factors like `compensation_tier`, `work_conditions_score`, `dept_turnover_rate`, `dept_management_ratio`, `dept_health_score`, and `organization_type`. Additionally, you need to identify "high-value attrition risk employees," defined as those with a `retention_stability_score` below 60 but an `overall_employee_score` above 80. Analyze their `employee_value_segment` distribution and work condition features like `is_work_shift_required` and `is_union_eligible`. Finally, construct an integrated, tiered employee management recommendation system. Based on combinations of `highest_management_level_reached`, `dept_performance_category`, and `organization_sub_type`, provide targeted retention strategies and development path suggestions for different types of core employees, and evaluate the implementation priority and expected effectiveness of these strategies in various departments.

| 表 | 行数 | 列数 |
| --- | --- | --- |
| workday__employee_overview | 156205 | 79 |


实际路线（分析者依据 SQL/源码概括，不代表 Agent 自述）：SQL 去重员工、识别核心及流失风险并交叉汇总 → Python 描述统计、优先级分箱与图表 → 分层管理建议。

数据库大小：91,701,248 字节。

## 数据 SQL

| SQL | 状态 | 基础表 | Join 输入/类型 | GROUP BY | 聚合表达式 | 结果行数 | 数据库 ms |
| --- | --- | --- | --- | --- | --- | --- | --- |
| [S3/Q1](#s3) | success | ["workday__employee_overview"] | 0 / {} | [] | ["COUNT(*)"] | 1 | 30.641 |
| [S4/Q2](#s4) | success | ["workday__employee_overview"] | 0 / {} | [] | [] | 5 | 0.604 |
| [S5/Q3](#s5) | success | ["workday__employee_overview"] | 0 / {} | [] | ["COUNT(DISTINCT employee_id)", "COUNT(DISTINCT worker_id)", "COUNT(*)"] | 1 | 125.045 |
| [S6/Q4](#s6) | success | ["workday__employee_overview"] | 0 / {} | ["event_type"] | ["COUNT(*)"] | 5 | 93.223 |
| [S7/Q5](#s7) | success | ["workday__employee_overview"] | 0 / {} | ["employee_id"] | ["COUNT(*)", "COUNT(*)", "COUNT(*)", "COUNT(DISTINCT employee_id)"] | 1 | 102.417 |
| [S8/Q6](#s8) | success | ["workday__employee_overview"] | 0 / {} | ["employee_id", "rows_per_emp"] | ["COUNT(*)", "COUNT(*)"] | 7 | 102.845 |
| [S9/Q7](#s9) | success | ["workday__employee_overview"] | 0 / {} | [] | ["MIN(worker_id)", "MAX(worker_id)", "MIN(age)", "MAX(age)", "COUNT(*) FILTER(WHERE age IS NULL)"] | 1 | 64.044 |
| [S10/Q8](#s10) | success | ["workday__employee_overview"] | 0 / {} | ["worker_id"] | ["COUNT(DISTINCT employee_id)", "COUNT(DISTINCT employee_id)"] | 5 | 69.207 |
| [S11/Q9](#s11) | success | ["workday__employee_overview"] | 0 / {} | ["employee_id"] | ["COUNT(DISTINCT overall_employee_score)", "COUNT(DISTINCT career_development_score)", "COUNT(DISTINCT age)", "COUNT(DISTINCT tenure_years)", "COUNT(DISTINCT employee_risk_level)", "COUNT(DISTINCT employee_maturity_segment)", "COUNT(DISTINCT overall_employee_score)", "COUNT(DISTINCT employee_risk_level)"] | 10 | 227.945 |
| [S12/Q10](#s12) | success | ["workday__employee_overview"] | 0 / {} | [] | [] | 8 | 38.122 |
| [S13/Q11](#s13) | success | ["workday__employee_overview"] | 0 / {} | [] | [] | 1 | 58.398 |
| [S14/Q12](#s14) | success | ["workday__employee_overview"] | 0 / {} | [] | [] | 15 | 38.44 |
| [S15/Q13](#s15) | success | ["workday__employee_overview"] | 0 / {} | [] | ["COUNT(*)"] | 1 | 96.536 |
| [S16/Q14](#s16) | success | ["workday__employee_overview"] | 0 / {} | [] | [] | 3 | 59.204 |
| [S17/Q15](#s17) | success | ["workday__employee_overview"] | 0 / {} | [] | [] | 4 | 53.963 |
| [S18/Q16](#s18) | success | ["workday__employee_overview"] | 0 / {} | [] | [] | 3 | 58.769 |
| [S19/Q17](#s19) | success | ["workday__employee_overview"] | 0 / {} | [] | ["COUNT(*)", "AVG(career_development_score)", "MIN(career_development_score)", "MAX(career_development_score)", "AVG(overall_employee_score)", "MIN(overall_employee_score)", "MAX(overall_employee_score)"] | 1 | 1838.026 |
| [S20/Q18](#s20) | success | ["workday__employee_overview"] | 0 / {} | [] | ["COUNT(*)"] | 1 | 2138.118 |
| [S21/Q19](#s21) | success | ["workday__employee_overview"] | 0 / {} | [] | [] | 1 | 1846.413 |
| [S22/Q20](#s22) | success | ["workday__employee_overview"] | 0 / {} | [] | ["SUM(CASE WHEN overall_employee_score > 75 AND career_development_score > 78.57581219355939 THEN 1 ELSE 0 END)", "COUNT(*)"] | 1 | 1828.677 |
| [S23/Q21](#s23) | failed | ["workday__employee_overview"] | 0 / {} | [] | ["MIN(age)", "MAX(age)", "AVG(age)", "AVG(age)", "STDDEV(age)", "AVG(age)", "STDDEV(age)", "AVG(tenure_years)", "MIN(tenure_years)", "MAX(tenure_years)", "AVG(tenure_years)", "STDDEV(tenure_years)", "AVG(tenure_years)", "STDDEV(tenure_years)", "MIN(total_positions_held)", "MAX(total_positions_held)", "AVG(total_positions_held)", "AVG(total_positions_held)", "STDDEV(total_positions_held)", "AVG(total_positions_held)", "STDDEV(total_positions_held)", "MIN(total_promotions)", "MAX(total_promotions)", "AVG(total_promotions)", "AVG(total_promotions)", "STDDEV(total_promotions)", "AVG(total_promotions)", "STDDEV(total_promotions)", "MIN(lateral_moves)", "MAX(lateral_moves)", "AVG(lateral_moves)", "AVG(lateral_moves)", "STDDEV(lateral_moves)", "AVG(lateral_moves)", "STDDEV(lateral_moves)", "MIN(management_positions_held)", "MAX(management_positions_held)", "AVG(management_positions_held)", "AVG(management_positions_held)", "STDDEV(management_positions_held)", "AVG(management_positions_held)", "STDDEV(management_positions_held)"] | unknown | 未取得；调用总时长 1.228 ms |
| [S24/Q22](#s24) | success | ["workday__employee_overview"] | 0 / {} | ["marital_status"] | ["COUNT(*)", "COUNT(*)", "COUNT(*)"] | 4 | 2137.458 |
| [S25/Q23](#s25) | success | ["workday__employee_overview"] | 0 / {} | ["ethnicity_codes"] | ["COUNT(*)", "COUNT(*)", "COUNT(*)"] | 6 | 2105.137 |
| [S26/Q24](#s26) | success | ["workday__employee_overview"] | 0 / {} | [] | ["MIN(age)", "MAX(age)", "AVG(age)", "AVG(tenure_years)", "MIN(tenure_years)", "MAX(tenure_years)", "MIN(total_positions_held)", "MAX(total_positions_held)", "AVG(total_positions_held)", "MIN(total_promotions)", "MAX(total_promotions)", "AVG(total_promotions)", "MIN(lateral_moves)", "MAX(lateral_moves)", "AVG(lateral_moves)", "MIN(management_positions_held)", "MAX(management_positions_held)", "AVG(management_positions_held)"] | 6 | 2307.679 |
| [S27/Q25](#s27) | success | ["workday__employee_overview"] | 0 / {} | ["career_phase", "employee_maturity_segment"] | ["COUNT(*)", "SUM(CASE WHEN employee_risk_level = 'High' THEN 1 ELSE 0 END)", "SUM(CASE WHEN employee_risk_level = 'Medium' THEN 1 ELSE 0 END)", "SUM(CASE WHEN employee_risk_level = 'Low' THEN 1 ELSE 0 END)", "COUNT(*)", "COUNT(*)", "COUNT(*)", "SUM(CASE WHEN employee_risk_level = 'High' THEN 1 ELSE 0 END)", "SUM(CASE WHEN employee_risk_level = 'Medium' THEN 1 ELSE 0 END)", "SUM(CASE WHEN employee_risk_level = 'Low' THEN 1 ELSE 0 END)"] | 7 | 1831.883 |
| [S28/Q26](#s28) | success | ["workday__employee_overview"] | 0 / {} | ["compensation_tier"] | ["COUNT(*)", "SUM(CASE WHEN employee_risk_level = 'High' THEN 1 ELSE 0 END)", "AVG(work_conditions_score)", "AVG(dept_turnover_rate)", "AVG(dept_management_ratio)", "AVG(dept_health_score)", "COUNT(*)", "SUM(CASE WHEN employee_risk_level = 'High' THEN 1 ELSE 0 END)"] | 5 | 1892.794 |
| [S29/Q27](#s29) | success | ["workday__employee_overview"] | 0 / {} | ["organization_type"] | ["COUNT(*)", "SUM(CASE WHEN employee_risk_level = 'High' THEN 1 ELSE 0 END)", "AVG(dept_turnover_rate)", "AVG(dept_health_score)", "COUNT(*)", "SUM(CASE WHEN employee_risk_level = 'High' THEN 1 ELSE 0 END)"] | 3 | 1939.358 |
| [S30/Q28](#s30) | success | ["workday__employee_overview"] | 0 / {} | ["employee_risk_level"] | ["COUNT(*)", "COUNT(*)", "COUNT(*)"] | 3 | 2175.937 |
| [S31/Q29](#s31) | success | ["workday__employee_overview"] | 0 / {} | ["employee_risk_level"] | ["AVG(work_conditions_score)", "AVG(dept_turnover_rate)", "AVG(dept_management_ratio)", "AVG(dept_health_score)", "AVG(compensation_tier)"] | 3 | 1836.806 |
| [S32/Q30](#s32) | success | ["workday__employee_overview"] | 0 / {} | [] | ["COUNT(*)", "SUM(CASE WHEN retention_stability_score < 60 AND overall_employee_score > 80 THEN 1 ELSE 0 END)"] | 1 | 1883.813 |
| [S33/Q31](#s33) | success | ["workday__employee_overview"] | 0 / {} | ["employee_value_segment"] | ["COUNT(*)", "COUNT(*)", "COUNT(*)"] | 6 | 2117.554 |
| [S34/Q32](#s34) | success | ["workday__employee_overview"] | 0 / {} | [] | ["SUM(is_work_shift_required)", "SUM(is_union_eligible)", "COUNT(*)", "COUNT(*)", "SUM(is_work_shift_required)", "SUM(is_union_eligible)"] | 1 | 1833.258 |
| [S35/Q33](#s35) | success | ["workday__employee_overview"] | 0 / {} | [] | ["COUNT(*)", "AVG(retention_stability_score)", "AVG(overall_employee_score)", "COUNT(*)", "COUNT(*)", "SUM(is_work_shift_required)", "SUM(is_union_eligible)", "COUNT(*)", "AVG(retention_stability_score)", "AVG(overall_employee_score)", "COUNT(*)", "COUNT(*)", "SUM(is_work_shift_required)", "SUM(is_union_eligible)"] | 2 | 2162.963 |
| [S36/Q34](#s36) | success | ["workday__employee_overview"] | 0 / {} | [] | [] | 6 | 1864.838 |
| [S37/Q35](#s37) | success | ["workday__employee_overview"] | 0 / {} | [] | [] | 6 | 1901.947 |
| [S38/Q36](#s38) | success | ["workday__employee_overview"] | 0 / {} | [] | [] | 3 | 1839.373 |
| [S39/Q37](#s39) | success | ["workday__employee_overview"] | 0 / {} | [] | [] | 15 | 1841.371 |
| [S40/Q38](#s40) | success | ["workday__employee_overview"] | 0 / {} | ["organization_sub_type"] | ["COUNT(*)"] | 15 | 1831.4 |
| [S41/Q39](#s41) | success | ["workday__employee_overview"] | 0 / {} | ["highest_management_level_reached", "dept_performance_category"] | ["COUNT(*)", "SUM(CASE WHEN employee_risk_level IN ('High', 'Medium') THEN 1 ELSE 0 END)", "SUM(CASE WHEN retention_stability_score < 60 THEN 1 ELSE 0 END)", "AVG(overall_employee_score)", "AVG(career_development_score)", "COUNT(*)", "COUNT(*)", "SUM(CASE WHEN employee_risk_level IN ('High', 'Medium') THEN 1 ELSE 0 END)", "SUM(CASE WHEN retention_stability_score < 60 THEN 1 ELSE 0 END)"] | 17 | 1850.537 |
| [S42/Q40](#s42) | success | ["workday__employee_overview"] | 0 / {} | ["organization_sub_type", "dept_performance_category"] | ["COUNT(*)", "SUM(CASE WHEN employee_risk_level IN ('High', 'Medium') THEN 1 ELSE 0 END)", "SUM(CASE WHEN retention_stability_score < 60 THEN 1 ELSE 0 END)", "AVG(overall_employee_score)", "AVG(career_development_score)", "SUM(CASE WHEN employee_risk_level IN ('High', 'Medium') THEN 1 ELSE 0 END)", "COUNT(*)"] | 44 | 1853.451 |
| [S43/Q41](#s43) | success | ["workday__employee_overview"] | 0 / {} | ["CASE WHEN age < 45 THEN '<45' WHEN age BETWEEN 45 AND 50 THEN '45-50' WHEN age BETWEEN 51 AND 55 THEN '51-55' WHEN age BETWEEN 56 AND 60 THEN '56-60' ELSE '60+' END"] | ["COUNT(*)", "COUNT(*)", "MIN(age)", "COUNT(*)"] | 5 | 2136.389 |
| [S44/Q42](#s44) | success | ["workday__employee_overview"] | 0 / {} | [] | [] | 19 | 1824.465 |
| [S45/Q43](#s45) | success | ["workday__employee_overview"] | 0 / {} | ["tenure_group"] | ["COUNT(*)", "COUNT(*)", "COUNT(*)"] | 2 | 2111.499 |
| [S46/Q44](#s46) | success | ["workday__employee_overview"] | 0 / {} | ["career_phase"] | ["COUNT(*)", "COUNT(*)", "COUNT(*)"] | 3 | 2124.262 |
| [S47/Q45](#s47) | success | ["workday__employee_overview"] | 0 / {} | ["employee_maturity_segment"] | ["COUNT(*)", "COUNT(*)", "COUNT(*)"] | 4 | 2129.698 |
| [S48/Q46](#s48) | success | ["workday__employee_overview"] | 0 / {} | [] | ["COUNT(*)", "AVG(age)", "AVG(tenure_years)", "AVG(overall_employee_score)", "AVG(career_development_score)", "AVG(retention_stability_score)", "AVG(total_positions_held)", "AVG(total_promotions)", "AVG(lateral_moves)", "AVG(management_positions_held)", "COUNT(*)", "AVG(age)", "AVG(tenure_years)", "AVG(overall_employee_score)", "AVG(career_development_score)", "AVG(retention_stability_score)", "AVG(total_positions_held)", "AVG(total_promotions)", "AVG(lateral_moves)", "AVG(management_positions_held)"] | 2 | 2129.229 |
| [S49/Q47](#s49) | success | ["workday__employee_overview"] | 0 / {} | [] | ["SUM(CASE WHEN retention_stability_score < 60 AND overall_employee_score > 80 THEN 1 ELSE 0 END)", "COUNT(*)", "COUNT(*)", "COUNT(*)", "SUM(CASE WHEN employee_risk_level = 'High' THEN 1 ELSE 0 END)", "SUM(CASE WHEN employee_risk_level = 'Medium' THEN 1 ELSE 0 END)", "SUM(CASE WHEN employee_risk_level = 'Low' THEN 1 ELSE 0 END)", "SUM(CASE WHEN retention_stability_score < 60 AND overall_employee_score > 80 THEN 1 ELSE 0 END)", "COUNT(*)", "COUNT(*)", "COUNT(*)", "SUM(CASE WHEN employee_risk_level = 'High' THEN 1 ELSE 0 END)", "SUM(CASE WHEN employee_risk_level = 'Medium' THEN 1 ELSE 0 END)", "SUM(CASE WHEN employee_risk_level = 'Low' THEN 1 ELSE 0 END)"] | 2 | 2144.904 |
| [S50/Q48](#s50) | success | ["workday__employee_overview"] | 0 / {} | [] | [] | 2114 | 1888.239 |
| [S51/Q49](#s51) | success | ["workday__employee_overview"] | 0 / {} | [] | [] | 10317 | 1869.566 |
| [S52/Q50](#s52) | success | ["workday__employee_overview"] | 0 / {} | ["career_phase", "employee_maturity_segment"] | ["COUNT(*)", "SUM(CASE WHEN employee_risk_level = 'High' THEN 1 ELSE 0 END)", "SUM(CASE WHEN employee_risk_level = 'Medium' THEN 1 ELSE 0 END)", "SUM(CASE WHEN employee_risk_level = 'Low' THEN 1 ELSE 0 END)"] | 7 | 1852.927 |
| [S53/Q51](#s53) | success | ["workday__employee_overview"] | 0 / {} | ["employee_value_segment"] | ["COUNT(*)"] | 6 | 1843.887 |
| [S54/Q52](#s54) | success | ["workday__employee_overview"] | 0 / {} | ["employee_risk_level"] | ["AVG(work_conditions_score)", "AVG(dept_turnover_rate)", "AVG(dept_health_score)"] | 3 | 1836.368 |
| [S55/Q53](#s55) | success | ["workday__employee_overview"] | 0 / {} | ["compensation_tier"] | ["COUNT(*)"] | 5 | 1854.831 |
| [S56/Q54](#s56) | success | ["workday__employee_overview"] | 0 / {} | ["highest_management_level_reached", "dept_performance_category"] | ["COUNT(*)", "SUM(CASE WHEN employee_risk_level IN ('High', 'Medium') THEN 1 ELSE 0 END)", "SUM(CASE WHEN retention_stability_score < 60 THEN 1 ELSE 0 END)"] | 17 | 1843.643 |
| [S57/Q55](#s57) | success | ["workday__employee_overview"] | 0 / {} | ["organization_type", "organization_sub_type"] | ["COUNT(*)", "AVG(highest_management_level_reached)", "AVG(retention_stability_score)", "AVG(overall_employee_score)", "COUNT(*)", "COUNT(*)", "SUM(CASE WHEN employee_risk_level IN ('High', 'Medium') THEN 1 ELSE 0 END)"] | 15 | 1872.338 |
| [S58/Q56](#s58) | success | ["workday__employee_overview"] | 0 / {} | ["ethnicity_codes"] | ["COUNT(*)", "SUM(CASE WHEN overall_employee_score > 75 AND career_development_score > 78.57581219355939 THEN 1 ELSE 0 END)", "COUNT(*)", "SUM(CASE WHEN overall_employee_score > 75 AND career_development_score > 78.57581219355939 THEN 1 ELSE 0 END)"] | 6 | 1887.097 |
| [S59/Q57](#s59) | success | ["workday__employee_overview"] | 0 / {} | ["compensation_tier"] | ["COUNT(*)", "SUM(CASE WHEN retention_stability_score < 60 AND overall_employee_score > 80 THEN 1 ELSE 0 END)", "COUNT(*)", "SUM(CASE WHEN retention_stability_score < 60 AND overall_employee_score > 80 THEN 1 ELSE 0 END)"] | 5 | 1914.008 |
| [S60/Q58](#s60) | success | ["workday__employee_overview"] | 0 / {} | ["dept_performance_category"] | ["COUNT(*)", "SUM(CASE WHEN retention_stability_score < 60 AND overall_employee_score > 80 THEN 1 ELSE 0 END)", "AVG(dept_turnover_rate)", "COUNT(*)", "SUM(CASE WHEN retention_stability_score < 60 AND overall_employee_score > 80 THEN 1 ELSE 0 END)"] | 3 | 1869.581 |
| [S61/Q59](#s61) | success | ["workday__employee_overview"] | 0 / {} | ["organization_sub_type"] | ["COUNT(*)", "SUM(CASE WHEN retention_stability_score < 60 AND overall_employee_score > 80 THEN 1 ELSE 0 END)", "COUNT(*)", "SUM(CASE WHEN retention_stability_score < 60 AND overall_employee_score > 80 THEN 1 ELSE 0 END)", "COUNT(*)"] | 10 | 1873.725 |
| [S62/Q60](#s62) | success | ["workday__employee_overview"] | 0 / {} | ["organization_type", "dept_performance_category"] | ["COUNT(*)", "SUM(CASE WHEN employee_risk_level IN ('High', 'Medium') THEN 1 ELSE 0 END)", "AVG(overall_employee_score)", "AVG(career_development_score)", "AVG(retention_stability_score)", "COUNT(*)", "SUM(CASE WHEN employee_risk_level IN ('High', 'Medium') THEN 1 ELSE 0 END)"] | 9 | 1859.85 |
| [S63/Q61](#s63) | success | ["workday__employee_overview"] | 0 / {} | ["CASE WHEN highest_management_level_reached = 0 THEN 'Individual Contributor (L0)' WHEN highest_management_level_reached = 1 THEN 'Team Lead (L1)' WHEN highest_management_level_reached = 2 THEN 'Manager (L2)' ELSE 'Senior Management (L3+)' END", "dept_performance_category"] | ["COUNT(*)", "SUM(CASE WHEN employee_risk_level IN ('High', 'Medium') THEN 1 ELSE 0 END)", "SUM(CASE WHEN retention_stability_score < 60 THEN 1 ELSE 0 END)", "AVG(overall_employee_score)", "AVG(career_development_score)", "AVG(retention_stability_score)", "COUNT(*)", "SUM(CASE WHEN employee_risk_level IN ('High', 'Medium') THEN 1 ELSE 0 END)"] | 12 | 1854.862 |
| [S64/Q62](#s64) | success | ["workday__employee_overview"] | 0 / {} | ["CASE WHEN highest_management_level_reached = 0 THEN 'IC (L0)' WHEN highest_management_level_reached = 1 THEN 'Team Lead (L1)' WHEN highest_management_level_reached = 2 THEN 'Manager (L2)' ELSE 'Sr Mgmt (L3+)' END", "dept_performance_category"] | ["COUNT(*)", "SUM(CASE WHEN employee_risk_level IN ('High', 'Medium') THEN 1 ELSE 0 END)", "COUNT(*)", "SUM(CASE WHEN employee_risk_level IN ('High', 'Medium') THEN 1 ELSE 0 END)"] | 12 | 1848.596 |
| [S65/Q63](#s65) | success | ["workday__employee_overview"] | 0 / {} | ["organization_sub_type"] | ["COUNT(*)", "SUM(CASE WHEN retention_stability_score < 60 AND overall_employee_score > 80 THEN 1 ELSE 0 END)", "COUNT(*)", "COUNT(*)", "SUM(CASE WHEN retention_stability_score < 60 AND overall_employee_score > 80 THEN 1 ELSE 0 END)"] | 15 | 1846.769 |


## 元数据和设置

| SQL | 类别 | 状态 | 内容 |
| --- | --- | --- | --- |
| S1 | connection_setup | success | PRAGMA query_only=ON |
| S2 | metadata | success | SELECT name,sql FROM sqlite_master WHERE type='table' ORDER BY name |


## Python 与执行位置

人工源码审查：**database_first_violation**。SQL 完成主要去重窗口、核心员工筛选与交叉汇总。Python 仍用 describe 重算均值/极值，并在已聚合结果上计算优先级和分箱；这些统计与常规评分可在 SQL 提供，记录为有限范围的执行位置偏离。绘图及标准差单独评价。 [证据](../reviews/dacomp-083.json)。

P1：Compute standard deviations and detailed statistics for core employees that SQLite can't calculate (STDDEV not available), and generate visualizations for the report.

[源码](../../../runs/dsv4flash-db-first-full-01/dacomp-083/attempt-01/python/P1.py)；[输出](../../../runs/dsv4flash-db-first-full-01/dacomp-083/attempt-01/python/P1.stdout)；[错误](../../../runs/dsv4flash-db-first-full-01/dacomp-083/attempt-01/python/P1.stderr)。检出需人工核验的 SQL 可实现操作：.query(；不能仅凭理由判为合规。

P2：Build the integrated priority scoring for the tiered recommendation system and generate the priority matrix and attrition-by-org visualizations, which require priority score computation beyond simple SQL aggregation.

[源码](../../../runs/dsv4flash-db-first-full-01/dacomp-083/attempt-01/python/P2.py)；[输出](../../../runs/dsv4flash-db-first-full-01/dacomp-083/attempt-01/python/P2.stdout)；[错误](../../../runs/dsv4flash-db-first-full-01/dacomp-083/attempt-01/python/P2.stderr)。检出需人工核验的 SQL 可实现操作：.query(, sort_values(；不能仅凭理由判为合规。

## 优化机会

已验证候选。筛选限于精确 SQL、相同自包含 CTE、相同单表完整过滤、可分解单表聚合；未覆盖任意 Join 等价和一般谓词蕴含。全部候选都是 offline，未测在线预测。

| 候选 | 类型 | 已有结果 | 覆盖 SQL | 后续次数 | 中间行数 | 验证 | 成本 |
| --- | --- | --- | --- | --- | --- | --- | --- |
| C1 | common subexpression | False | ["S19", "S20", "S21", "S22", "S24", "S25", "S26", "S27", "S28", "S29", "S30", "S31", "S32", "S33", "S34", "S35", "S36", "S37", "S38", "S39", "S40", "S41", "S42", "S43", "S44", "S45", "S46", "S47", "S48", "S49", "S50", "S51", "S52", "S53", "S54", "S55", "S56", "S57", "S58", "S59", "S60", "S61", "S62", "S63", "S64", "S65"] | 45 | 156205 | verified | Not benchmarked; correctness alone does not establish net speedup. |
| C2 | aggregate MV | False | ["S3", "S6"] | 1 | 5 | verified | Not benchmarked; correctness alone does not establish net speedup. |


已验证覆盖（含触发查询、候选并集去重）：48/62 条成功数据 SQL。正确性仅针对当前数据库快照；未测性能的候选不能声称已加速。

[完整 build/rewrite 与比较证据](dacomp-083.analysis.json)。

### C1：common subexpression

Identical self-contained CTE body across queries.

原查询 [S19](#s19), [S20](#s20), [S21](#s21), [S22](#s22), [S24](#s24), [S25](#s25), [S26](#s26), [S27](#s27), [S28](#s28), [S29](#s29), [S30](#s30), [S31](#s31), [S32](#s32), [S33](#s33), [S34](#s34), [S35](#s35), [S36](#s36), [S37](#s37), [S38](#s38), [S39](#s39), [S40](#s40), [S41](#s41), [S42](#s42), [S43](#s43), [S44](#s44), [S45](#s45), [S46](#s46), [S47](#s47), [S48](#s48), [S49](#s49), [S50](#s50), [S51](#s51), [S52](#s52), [S53](#s53), [S54](#s54), [S55](#s55), [S56](#s56), [S57](#s57), [S58](#s58), [S59](#s59), [S60](#s60), [S61](#s61), [S62](#s62), [S63](#s63), [S64](#s64), [S65](#s65) → 新增共享状态 C1 → 后续 45 次可复用。该构建点为事后假设，不代表 Agent 当时预知后续。

构建定义：

```sql
SELECT *, ROW_NUMBER() OVER (PARTITION BY employee_id ORDER BY position_start_date DESC, overall_employee_score DESC, career_development_score DESC, total_promotions DESC) AS rn FROM workday__employee_overview
```

受益查询 S19 的改写示例：

```sql
WITH ranked AS (SELECT * FROM temp.reuse_candidate) SELECT COUNT(*) AS n, AVG(career_development_score) AS avg_career, MIN(career_development_score) AS min_career, MAX(career_development_score) AS max_career, AVG(overall_employee_score) AS avg_overall, MIN(overall_employee_score) AS min_overall, MAX(overall_employee_score) AS max_overall FROM ranked WHERE rn = 1
```

| 原 SQL | 列名一致 | 结果一致 | 比较方法 |
| --- | --- | --- | --- |
| S19 | True | True | exact_multiset |
| S20 | True | True | ordered_numeric_tolerance |
| S21 | True | True | exact_multiset |
| S22 | True | True | exact_multiset |
| S24 | True | True | ordered_numeric_tolerance |
| S25 | True | True | ordered_numeric_tolerance |
| S26 | True | True | exact_multiset |
| S27 | True | True | ordered_numeric_tolerance |
| S28 | True | True | ordered_numeric_tolerance |
| S29 | True | True | ordered_numeric_tolerance |
| S30 | True | True | ordered_numeric_tolerance |
| S31 | True | True | exact_multiset |
| S32 | True | True | exact_multiset |
| S33 | True | True | ordered_numeric_tolerance |
| S34 | True | True | exact_multiset |
| S35 | True | True | exact_multiset |
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
| S47 | True | True | ordered_numeric_tolerance |
| S48 | True | True | exact_multiset |
| S49 | True | True | exact_multiset |
| S50 | True | True | exact_multiset |
| S51 | True | True | exact_multiset |
| S52 | True | True | ordered_numeric_tolerance |
| S53 | True | True | ordered_numeric_tolerance |
| S54 | True | True | ordered_numeric_tolerance |
| S55 | True | True | ordered_numeric_tolerance |
| S56 | True | True | ordered_numeric_tolerance |
| S57 | True | True | ordered_numeric_tolerance |
| S58 | True | True | ordered_numeric_tolerance |
| S59 | True | True | ordered_numeric_tolerance |
| S60 | True | True | ordered_numeric_tolerance |
| S61 | True | True | ordered_numeric_tolerance |
| S62 | True | True | ordered_numeric_tolerance |
| S63 | True | True | ordered_numeric_tolerance |
| S64 | True | True | exact_multiset |
| S65 | True | True | ordered_numeric_tolerance |


验证状态：verified；成本结论：Not benchmarked; correctness alone does not establish net speedup.

### C2：aggregate MV

Union of grouping keys; decomposable aggregate states; AVG uses SUM and non-NULL COUNT.

原查询 [S3](#s3), [S6](#s6) → 新增共享状态 C2 → 后续 1 次可复用。该构建点为事后假设，不代表 Agent 当时预知后续。

构建定义：

```sql
SELECT event_type AS __g0, COUNT(*) AS __a0 FROM "workday__employee_overview"  GROUP BY event_type
```

受益查询 S3 的改写示例：

```sql
SELECT SUM(__a0) AS total FROM temp.reuse_candidate
```

| 原 SQL | 列名一致 | 结果一致 | 比较方法 |
| --- | --- | --- | --- |
| S3 | True | True | exact_multiset |
| S6 | True | True | ordered_numeric_tolerance |


验证状态：verified；成本结论：Not benchmarked; correctness alone does not establish net speedup.

[性能证据 C1](dacomp-083.C1.performance.json)：limited_or_failed。

结果依赖：自动记录 SQL→Python 的接口父调用，以及源码中引用归档文件的消费者；字面值相同不认定因果。模型方向选择需要人工读取消息，尚未做全面因果标注。

[原始报告](../../../runs/dsv4flash-db-first-full-01/dacomp-083/attempt-01/answer.md)；[统一消息](../../../runs/dsv4flash-db-first-full-01/dacomp-083/attempt-01/messages.jsonl)；[原始 OpenCode 事件](../../../runs/dsv4flash-db-first-full-01/dacomp-083/attempt-01/opencode.jsonl)；[SQL 引擎日志](../../../runs/dsv4flash-db-first-full-01/dacomp-083/attempt-01/sql_journal.jsonl)。

[可读报告（本地图片链接规范化）](../answers/dacomp-083.md)。原始回答保留，分析结论未改写。

## S1

类别 `connection_setup`；来源 `connection`；调用 `438d59d4ebf9428cb7959288cf164bca`；状态 `success`。

```sql
PRAGMA query_only=ON
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-083/attempt-01/sql/S1.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-083/attempt-01/sql/S1.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-083/attempt-01/results/S1.rows.jsonl)；完整：True；SHA256：`e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`。

## S2

类别 `metadata`；来源 `list_db`；调用 `438d59d4ebf9428cb7959288cf164bca`；状态 `success`。

```sql
SELECT name,sql FROM sqlite_master WHERE type='table' ORDER BY name
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-083/attempt-01/sql/S2.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-083/attempt-01/sql/S2.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-083/attempt-01/results/S2.rows.jsonl)；完整：True；SHA256：`ba78d234bb5d277df49bd3b90b6054580308ab6bcd040e6244d892858295cee0`。

## S3

类别 `data`；来源 `query_db`；调用 `52c346b28d25483abec948b3f9301029`；状态 `success`。

```sql
SELECT COUNT(*) as total FROM workday__employee_overview
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-083/attempt-01/sql/S3.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-083/attempt-01/sql/S3.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-083/attempt-01/results/S3.rows.jsonl)；完整：True；SHA256：`fd1308e8ceaf6a95e55f3c12d903facc806e1451f92ca66e6a45ee02e1fc46db`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "workday__employee_overview", "kind": "base", "block": null, "base_tables": ["workday__employee_overview"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |


## S4

类别 `data`；来源 `query_db`；调用 `644eb26a48b74b8692eeba349bcb14aa`；状态 `success`。

```sql
SELECT * FROM workday__employee_overview LIMIT 5
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-083/attempt-01/sql/S4.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-083/attempt-01/sql/S4.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-083/attempt-01/results/S4.rows.jsonl)；完整：True；SHA256：`e56d263419f0da05edf99ed04deb125afeb2f787c8e8b4cfe0c00fcd3990a1d7`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "workday__employee_overview", "kind": "base", "block": null, "base_tables": ["workday__employee_overview"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |


## S5

类别 `data`；来源 `query_db`；调用 `f8d25c60037a4294adec089c9ba89054`；状态 `success`。

```sql
SELECT COUNT(DISTINCT employee_id) as distinct_emp, COUNT(DISTINCT worker_id) as distinct_worker, COUNT(*) as total_rows FROM workday__employee_overview
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-083/attempt-01/sql/S5.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-083/attempt-01/sql/S5.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-083/attempt-01/results/S5.rows.jsonl)；完整：True；SHA256：`440a5e16f0b78da39b1b5d16e6ada5874324b07f6d86980c14f24110b55ae0d9`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "workday__employee_overview", "kind": "base", "block": null, "base_tables": ["workday__employee_overview"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(DISTINCT employee_id) | [{"table": "workday__employee_overview", "column": "employee_id"}] | [] | False |
| B1 | COUNT(DISTINCT worker_id) | [{"table": "workday__employee_overview", "column": "worker_id"}] | [] | False |
| B1 | COUNT(*) | [] | [] | True |


## S6

类别 `data`；来源 `query_db`；调用 `70f01118c64e428c981c4355d4cadaf0`；状态 `success`。

```sql
SELECT event_type, COUNT(*) as cnt FROM workday__employee_overview GROUP BY event_type ORDER BY cnt DESC
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-083/attempt-01/sql/S6.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-083/attempt-01/sql/S6.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-083/attempt-01/results/S6.rows.jsonl)；完整：True；SHA256：`4e00e857d0a0cb07426966c559dbe675a77fcd8600739c5c2a772693e9ee8670`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "workday__employee_overview", "kind": "base", "block": null, "base_tables": ["workday__employee_overview"]}] | [] | ["event_type"] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |


## S7

类别 `data`；来源 `query_db`；调用 `c50ca2e640fa4ff0a5500efdf1e2d2f9`；状态 `success`。

```sql
SELECT COUNT(*) as cnt, COUNT(DISTINCT employee_id) as emp FROM (SELECT employee_id, COUNT(*) as c FROM workday__employee_overview GROUP BY employee_id HAVING COUNT(*)=1)
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-083/attempt-01/sql/S7.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-083/attempt-01/sql/S7.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-083/attempt-01/results/S7.rows.jsonl)；完整：True；SHA256：`373253885dda63c1c985b81cfd4111d84e675b96e42b8f0b3a09eab658e51293`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "workday__employee_overview", "kind": "base", "block": null, "base_tables": ["workday__employee_overview"]}] | [] | ["employee_id"] |
| B2 | [{"alias": "", "kind": "derived", "block": "B1", "base_tables": ["workday__employee_overview"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |
| B1 | COUNT(*) | [] | [] | True |
| B2 | COUNT(*) | [] | [] | True |
| B2 | COUNT(DISTINCT employee_id) | [{"table": "workday__employee_overview", "column": "employee_id"}] | [] | False |


## S8

类别 `data`；来源 `query_db`；调用 `1377af35b2304429989416fc896d879b`；状态 `success`。

```sql
SELECT rows_per_emp, COUNT(*) as num_emp FROM (SELECT employee_id, COUNT(*) as rows_per_emp FROM workday__employee_overview GROUP BY employee_id) GROUP BY rows_per_emp ORDER BY rows_per_emp
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-083/attempt-01/sql/S8.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-083/attempt-01/sql/S8.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-083/attempt-01/results/S8.rows.jsonl)；完整：True；SHA256：`c9d8569b21f24c200a29bdf1b3270551e17667cbb588130e1ebe3b117a24a992`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "workday__employee_overview", "kind": "base", "block": null, "base_tables": ["workday__employee_overview"]}] | [] | ["employee_id"] |
| B2 | [{"alias": "", "kind": "derived", "block": "B1", "base_tables": ["workday__employee_overview"]}] | [] | ["rows_per_emp"] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |
| B2 | COUNT(*) | [] | [] | True |


## S9

类别 `data`；来源 `query_db`；调用 `19671594d39544f3a3d82b5e2e29f062`；状态 `success`。

```sql
SELECT MIN(worker_id) as min_w, MAX(worker_id) as max_w, MIN(age) as min_age, MAX(age) as max_age, COUNT(*) FILTER (WHERE age IS NULL) as null_age FROM workday__employee_overview
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-083/attempt-01/sql/S9.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-083/attempt-01/sql/S9.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-083/attempt-01/results/S9.rows.jsonl)；完整：True；SHA256：`680ae73fa423a92589283bf06c8d69ebfbf6e938dafe9651fe44385d0d0f9b02`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "workday__employee_overview", "kind": "base", "block": null, "base_tables": ["workday__employee_overview"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | MIN(worker_id) | [{"table": "workday__employee_overview", "column": "worker_id"}] | [] | False |
| B1 | MAX(worker_id) | [{"table": "workday__employee_overview", "column": "worker_id"}] | [] | False |
| B1 | MIN(age) | [{"table": "workday__employee_overview", "column": "age"}] | [] | False |
| B1 | MAX(age) | [{"table": "workday__employee_overview", "column": "age"}] | [] | False |
| B1 | COUNT(*) FILTER(WHERE age IS NULL) | [] | [{"table": "workday__employee_overview", "column": "age"}] | True |


## S10

类别 `data`；来源 `query_db`；调用 `6c8861a441d342879237f172cc5211d7`；状态 `success`。

```sql
SELECT worker_id, COUNT(DISTINCT employee_id) as num_emp_ids FROM workday__employee_overview GROUP BY worker_id HAVING COUNT(DISTINCT employee_id) > 1 LIMIT 5
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-083/attempt-01/sql/S10.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-083/attempt-01/sql/S10.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-083/attempt-01/results/S10.rows.jsonl)；完整：True；SHA256：`d7bbfbfdc38c0f07293720a668c5beac1cc58ee128548d248ab03862d4e9c644`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "workday__employee_overview", "kind": "base", "block": null, "base_tables": ["workday__employee_overview"]}] | [] | ["worker_id"] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(DISTINCT employee_id) | [{"table": "workday__employee_overview", "column": "employee_id"}] | [] | False |
| B1 | COUNT(DISTINCT employee_id) | [{"table": "workday__employee_overview", "column": "employee_id"}] | [] | False |


## S11

类别 `data`；来源 `query_db`；调用 `38976a57ede74753a308797516689238`；状态 `success`。

```sql
SELECT employee_id, COUNT(DISTINCT overall_employee_score) as distinct_score, COUNT(DISTINCT career_development_score) as distinct_career, COUNT(DISTINCT age) as distinct_age, COUNT(DISTINCT tenure_years) as distinct_tenure, COUNT(DISTINCT employee_risk_level) as distinct_risk, COUNT(DISTINCT employee_maturity_segment) as distinct_mat FROM workday__employee_overview GROUP BY employee_id HAVING COUNT(DISTINCT overall_employee_score)>1 OR COUNT(DISTINCT employee_risk_level)>1 ORDER BY distinct_score DESC LIMIT 10
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-083/attempt-01/sql/S11.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-083/attempt-01/sql/S11.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-083/attempt-01/results/S11.rows.jsonl)；完整：True；SHA256：`7eceb7225d9ae7e156851339c5dd628f6b5c8cf865aa9edfd48227b52b582af6`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "workday__employee_overview", "kind": "base", "block": null, "base_tables": ["workday__employee_overview"]}] | [] | ["employee_id"] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(DISTINCT overall_employee_score) | [{"table": "workday__employee_overview", "column": "overall_employee_score"}] | [] | False |
| B1 | COUNT(DISTINCT career_development_score) | [{"table": "workday__employee_overview", "column": "career_development_score"}] | [] | False |
| B1 | COUNT(DISTINCT age) | [{"table": "workday__employee_overview", "column": "age"}] | [] | False |
| B1 | COUNT(DISTINCT tenure_years) | [{"table": "workday__employee_overview", "column": "tenure_years"}] | [] | False |
| B1 | COUNT(DISTINCT employee_risk_level) | [{"table": "workday__employee_overview", "column": "employee_risk_level"}] | [] | False |
| B1 | COUNT(DISTINCT employee_maturity_segment) | [{"table": "workday__employee_overview", "column": "employee_maturity_segment"}] | [] | False |
| B1 | COUNT(DISTINCT overall_employee_score) | [{"table": "workday__employee_overview", "column": "overall_employee_score"}] | [] | False |
| B1 | COUNT(DISTINCT employee_risk_level) | [{"table": "workday__employee_overview", "column": "employee_risk_level"}] | [] | False |


## S12

类别 `data`；来源 `query_db`；调用 `285946c8d7cc4f95aead125617abb65b`；状态 `success`。

```sql
SELECT employee_id, event_type, position_start_date, analysis_timestamp, overall_employee_score, career_development_score, employee_risk_level, employee_maturity_segment FROM workday__employee_overview WHERE employee_id = '138c4f2e4ad951d86bb2c7c7e13a500a' ORDER BY analysis_timestamp DESC
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-083/attempt-01/sql/S12.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-083/attempt-01/sql/S12.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-083/attempt-01/results/S12.rows.jsonl)；完整：True；SHA256：`4c44e793053f2caeb93312fd2acce336795fc1614de005cb40b7179c6b7a7b76`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "workday__employee_overview", "kind": "base", "block": null, "base_tables": ["workday__employee_overview"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |


## S13

类别 `data`；来源 `query_db`；调用 `6c80f8826f2346d4beb7ec0a018e5b57`；状态 `success`。

```sql
SELECT DISTINCT analysis_timestamp FROM workday__employee_overview LIMIT 5
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-083/attempt-01/sql/S13.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-083/attempt-01/sql/S13.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-083/attempt-01/results/S13.rows.jsonl)；完整：True；SHA256：`7fca117e01489c6263a4b7f8e9566233eb6180b1b6ed650c60e48dfb42b1dc76`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "workday__employee_overview", "kind": "base", "block": null, "base_tables": ["workday__employee_overview"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |


## S14

类别 `data`；来源 `query_db`；调用 `a5a2e59b03564de4be4abd541e18228c`；状态 `success`。

```sql
SELECT employee_id, position_start_date, event_type, overall_employee_score, career_development_score, tenure_years, age, employee_risk_level FROM workday__employee_overview WHERE employee_id = '8eecfd5b558a6fc53ff34603b903a523' ORDER BY position_start_date DESC LIMIT 15
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-083/attempt-01/sql/S14.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-083/attempt-01/sql/S14.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-083/attempt-01/results/S14.rows.jsonl)；完整：True；SHA256：`7ecd497dcd671e6b95ec9c7dc0f4c823ca881205420681a1a0f679833d23afd1`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "workday__employee_overview", "kind": "base", "block": null, "base_tables": ["workday__employee_overview"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |


## S15

类别 `data`；来源 `query_db`；调用 `d42e0e460d2d4a97a056d205d52f9c57`；状态 `success`。

```sql
SELECT COUNT(*) as total_emp FROM (SELECT DISTINCT employee_id FROM workday__employee_overview)
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-083/attempt-01/sql/S15.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-083/attempt-01/sql/S15.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-083/attempt-01/results/S15.rows.jsonl)；完整：True；SHA256：`8d2ad92171c612d2c5d7c3c5ec6fdb3e3cb42be1412f72324029618a6c8be8ce`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "workday__employee_overview", "kind": "base", "block": null, "base_tables": ["workday__employee_overview"]}] | [] | [] |
| B2 | [{"alias": "", "kind": "derived", "block": "B1", "base_tables": ["workday__employee_overview"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B2 | COUNT(*) | [] | [] | True |


## S16

类别 `data`；来源 `query_db`；调用 `e8f75c399d9c49b5a5c5a93c03b3305e`；状态 `success`。

```sql
SELECT DISTINCT employee_risk_level FROM workday__employee_overview
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-083/attempt-01/sql/S16.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-083/attempt-01/sql/S16.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-083/attempt-01/results/S16.rows.jsonl)；完整：True；SHA256：`3ba0841c9b51b922d3519947c7a178ecd7296c470aa2afd99a50e3bfcdef2aa3`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "workday__employee_overview", "kind": "base", "block": null, "base_tables": ["workday__employee_overview"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |


## S17

类别 `data`；来源 `query_db`；调用 `03773f85309248fdbe184432fc553f17`；状态 `success`。

```sql
SELECT DISTINCT employee_maturity_segment FROM workday__employee_overview
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-083/attempt-01/sql/S17.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-083/attempt-01/sql/S17.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-083/attempt-01/results/S17.rows.jsonl)；完整：True；SHA256：`e4f2f58beff73fdce7da8c0b5d0015c6c0aaf002fc4cb8f283c670bf12884e48`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "workday__employee_overview", "kind": "base", "block": null, "base_tables": ["workday__employee_overview"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |


## S18

类别 `data`；来源 `query_db`；调用 `ebfb209fddb84b0db3449e544108ffb3`；状态 `success`。

```sql
SELECT DISTINCT career_phase FROM workday__employee_overview
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-083/attempt-01/sql/S18.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-083/attempt-01/sql/S18.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-083/attempt-01/results/S18.rows.jsonl)；完整：True；SHA256：`487358eae7dd65b11445598fa5cd3f37a6b1952409b3f5761c06975f2f535ed5`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "workday__employee_overview", "kind": "base", "block": null, "base_tables": ["workday__employee_overview"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |


## S19

类别 `data`；来源 `query_db`；调用 `e96901e168fc461e91942ae7e7538e2a`；状态 `success`。

```sql
WITH ranked AS (
  SELECT *, ROW_NUMBER() OVER (PARTITION BY employee_id ORDER BY position_start_date DESC, overall_employee_score DESC, career_development_score DESC, total_promotions DESC) as rn
  FROM workday__employee_overview
)
SELECT 
  COUNT(*) as n,
  AVG(career_development_score) as avg_career,
  MIN(career_development_score) as min_career,
  MAX(career_development_score) as max_career,
  AVG(overall_employee_score) as avg_overall,
  MIN(overall_employee_score) as min_overall,
  MAX(overall_employee_score) as max_overall
FROM ranked WHERE rn = 1
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-083/attempt-01/sql/S19.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-083/attempt-01/sql/S19.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-083/attempt-01/results/S19.rows.jsonl)；完整：True；SHA256：`c06ef6e849944d20fc06e241cd7b27979043884fad41ae14f47b5bb2e3930daa`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "workday__employee_overview", "kind": "base", "block": null, "base_tables": ["workday__employee_overview"]}] | [] | [] |
| B2 | [{"alias": "ranked", "kind": "derived", "block": "B1", "base_tables": ["workday__employee_overview"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B2 | COUNT(*) | [] | [] | True |
| B2 | AVG(career_development_score) | [{"table": "workday__employee_overview", "column": "career_development_score"}] | [] | False |
| B2 | MIN(career_development_score) | [{"table": "workday__employee_overview", "column": "career_development_score"}] | [] | False |
| B2 | MAX(career_development_score) | [{"table": "workday__employee_overview", "column": "career_development_score"}] | [] | False |
| B2 | AVG(overall_employee_score) | [{"table": "workday__employee_overview", "column": "overall_employee_score"}] | [] | False |
| B2 | MIN(overall_employee_score) | [{"table": "workday__employee_overview", "column": "overall_employee_score"}] | [] | False |
| B2 | MAX(overall_employee_score) | [{"table": "workday__employee_overview", "column": "overall_employee_score"}] | [] | False |


## S20

类别 `data`；来源 `query_db`；调用 `38f22e9587584f5cb44e535832749d0d`；状态 `success`。

```sql
WITH ranked AS (
  SELECT *, ROW_NUMBER() OVER (PARTITION BY employee_id ORDER BY position_start_date DESC, overall_employee_score DESC, career_development_score DESC, total_promotions DESC) as rn
  FROM workday__employee_overview
)
SELECT career_development_score FROM ranked WHERE rn = 1 ORDER BY career_development_score LIMIT 1 OFFSET (SELECT COUNT(*)/2 FROM ranked WHERE rn = 1)
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-083/attempt-01/sql/S20.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-083/attempt-01/sql/S20.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-083/attempt-01/results/S20.rows.jsonl)；完整：True；SHA256：`6e1b44b2c22a004cbf691844c22ec53c8c1da9405bb981df1566ce1dd4c7edb2`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "workday__employee_overview", "kind": "base", "block": null, "base_tables": ["workday__employee_overview"]}] | [] | [] |
| B2 | [{"alias": "ranked", "kind": "derived", "block": "B1", "base_tables": ["workday__employee_overview"]}] | [] | [] |
| B3 | [{"alias": "ranked", "kind": "derived", "block": "B1", "base_tables": ["workday__employee_overview"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B2 | COUNT(*) | [] | [] | True |


## S21

类别 `data`；来源 `query_db`；调用 `8343a421f2534a2da22da89c2be22821`；状态 `success`。

```sql
WITH ranked AS (
  SELECT *, ROW_NUMBER() OVER (PARTITION BY employee_id ORDER BY position_start_date DESC, overall_employee_score DESC, career_development_score DESC, total_promotions DESC) as rn
  FROM workday__employee_overview
),
emp AS (SELECT * FROM ranked WHERE rn = 1),
ordered AS (
  SELECT career_development_score, ROW_NUMBER() OVER (ORDER BY career_development_score) as rn, COUNT(*) OVER () as total
  FROM emp
)
SELECT career_development_score as median_career FROM ordered WHERE rn = (total + 1) / 2
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-083/attempt-01/sql/S21.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-083/attempt-01/sql/S21.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-083/attempt-01/results/S21.rows.jsonl)；完整：True；SHA256：`6e1b44b2c22a004cbf691844c22ec53c8c1da9405bb981df1566ce1dd4c7edb2`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "workday__employee_overview", "kind": "base", "block": null, "base_tables": ["workday__employee_overview"]}] | [] | [] |
| B2 | [{"alias": "ranked", "kind": "derived", "block": "B1", "base_tables": ["workday__employee_overview"]}] | [] | [] |
| B3 | [{"alias": "emp", "kind": "derived", "block": "B2", "base_tables": ["workday__employee_overview"]}] | [] | [] |
| B4 | [{"alias": "ordered", "kind": "derived", "block": "B3", "base_tables": ["workday__employee_overview"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |


## S22

类别 `data`；来源 `query_db`；调用 `21911e4a41e64b138a7c4c9e2a4c264a`；状态 `success`。

```sql
WITH ranked AS (
  SELECT *, ROW_NUMBER() OVER (PARTITION BY employee_id ORDER BY position_start_date DESC, overall_employee_score DESC, career_development_score DESC, total_promotions DESC) as rn
  FROM workday__employee_overview
),
emp AS (SELECT * FROM ranked WHERE rn = 1)
SELECT 
  SUM(CASE WHEN overall_employee_score > 75 AND career_development_score > 78.57581219355939 THEN 1 ELSE 0 END) as core_emp,
  COUNT(*) as total_emp
FROM emp
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-083/attempt-01/sql/S22.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-083/attempt-01/sql/S22.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-083/attempt-01/results/S22.rows.jsonl)；完整：True；SHA256：`42b7b29b159f82b094e1cc8c0c33cce1be6f3d77b807835a683b6be8bc9fe40e`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "workday__employee_overview", "kind": "base", "block": null, "base_tables": ["workday__employee_overview"]}] | [] | [] |
| B2 | [{"alias": "ranked", "kind": "derived", "block": "B1", "base_tables": ["workday__employee_overview"]}] | [] | [] |
| B3 | [{"alias": "emp", "kind": "derived", "block": "B2", "base_tables": ["workday__employee_overview"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B3 | SUM(CASE WHEN overall_employee_score > 75 AND career_development_score > 78.57581219355939 THEN 1 ELSE 0 END) | [] | [{"table": "workday__employee_overview", "column": "overall_employee_score"}, {"table": "workday__employee_overview", "column": "career_development_score"}] | False |
| B3 | COUNT(*) | [] | [] | True |


## S23

类别 `data`；来源 `query_db`；调用 `c272160dde8c42e59636011aeedf14ef`；状态 `failed`。

```sql
WITH ranked AS (
  SELECT *, ROW_NUMBER() OVER (PARTITION BY employee_id ORDER BY position_start_date DESC, overall_employee_score DESC, career_development_score DESC, total_promotions DESC) as rn
  FROM workday__employee_overview
),
emp AS (SELECT * FROM ranked WHERE rn = 1),
core AS (
  SELECT * FROM emp 
  WHERE overall_employee_score > 75 AND career_development_score > 78.57581219355939
)
SELECT 
  'Age' as feature,
  ROUND(AVG(age), 1) as avg_val,
  MIN(age) as min_val,
  MAX(age) as max_val,
  ROUND(AVG(age) - STDDEV(age), 1) as low_std,
  ROUND(AVG(age) + STDDEV(age), 1) as high_std
FROM core
UNION ALL
SELECT 
  'Tenure_years' as feature,
  ROUND(AVG(tenure_years), 2) as avg_val,
  ROUND(MIN(tenure_years), 2) as min_val,
  ROUND(MAX(tenure_years), 2) as max_val,
  ROUND(AVG(tenure_years) - STDDEV(tenure_years), 2) as low_std,
  ROUND(AVG(tenure_years) + STDDEV(tenure_years), 2) as high_std
FROM core
UNION ALL
SELECT 
  'Total_positions_held' as feature,
  ROUND(AVG(total_positions_held), 2) as avg_val,
  MIN(total_positions_held) as min_val,
  MAX(total_positions_held) as max_val,
  ROUND(AVG(total_positions_held) - STDDEV(total_positions_held), 2) as low_std,
  ROUND(AVG(total_positions_held) + STDDEV(total_positions_held), 2) as high_std
FROM core
UNION ALL
SELECT 
  'Total_promotions' as feature,
  ROUND(AVG(total_promotions), 2) as avg_val,
  MIN(total_promotions) as min_val,
  MAX(total_promotions) as max_val,
  ROUND(AVG(total_promotions) - STDDEV(total_promotions), 2) as low_std,
  ROUND(AVG(total_promotions) + STDDEV(total_promotions), 2) as high_std
FROM core
UNION ALL
SELECT 
  'Lateral_moves' as feature,
  ROUND(AVG(lateral_moves), 2) as avg_val,
  MIN(lateral_moves) as min_val,
  MAX(lateral_moves) as max_val,
  ROUND(AVG(lateral_moves) - STDDEV(lateral_moves), 2) as low_std,
  ROUND(AVG(lateral_moves) + STDDEV(lateral_moves), 2) as high_std
FROM core
UNION ALL
SELECT 
  'Management_positions_held' as feature,
  ROUND(AVG(management_positions_held), 2) as avg_val,
  MIN(management_positions_held) as min_val,
  MAX(management_positions_held) as max_val,
  ROUND(AVG(management_positions_held) - STDDEV(management_positions_held), 2) as low_std,
  ROUND(AVG(management_positions_held) + STDDEV(management_positions_held), 2) as high_std
FROM core
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-083/attempt-01/sql/S23.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-083/attempt-01/sql/S23.parameters.json)。

错误：`OperationalError('no such function: STDDEV')`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "workday__employee_overview", "kind": "base", "block": null, "base_tables": ["workday__employee_overview"]}] | [] | [] |
| B2 | [{"alias": "ranked", "kind": "derived", "block": "B1", "base_tables": ["workday__employee_overview"]}] | [] | [] |
| B3 | [{"alias": "emp", "kind": "derived", "block": "B2", "base_tables": ["workday__employee_overview"]}] | [] | [] |
| B4 | [{"alias": "core", "kind": "derived", "block": "B3", "base_tables": ["workday__employee_overview"]}] | [] | [] |
| B5 | [{"alias": "core", "kind": "derived", "block": "B3", "base_tables": ["workday__employee_overview"]}] | [] | [] |
| B6 | [] | [] | [] |
| B7 | [{"alias": "core", "kind": "derived", "block": "B3", "base_tables": ["workday__employee_overview"]}] | [] | [] |
| B8 | [] | [] | [] |
| B9 | [{"alias": "core", "kind": "derived", "block": "B3", "base_tables": ["workday__employee_overview"]}] | [] | [] |
| B10 | [] | [] | [] |
| B11 | [{"alias": "core", "kind": "derived", "block": "B3", "base_tables": ["workday__employee_overview"]}] | [] | [] |
| B12 | [] | [] | [] |
| B13 | [{"alias": "core", "kind": "derived", "block": "B3", "base_tables": ["workday__employee_overview"]}] | [] | [] |
| B14 | [] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B4 | MIN(age) | [{"table": "workday__employee_overview", "column": "age"}] | [] | False |
| B4 | MAX(age) | [{"table": "workday__employee_overview", "column": "age"}] | [] | False |
| B4 | AVG(age) | [{"table": "workday__employee_overview", "column": "age"}] | [] | False |
| B4 | AVG(age) | [{"table": "workday__employee_overview", "column": "age"}] | [] | False |
| B4 | STDDEV(age) | [{"table": "workday__employee_overview", "column": "age"}] | [] | False |
| B4 | AVG(age) | [{"table": "workday__employee_overview", "column": "age"}] | [] | False |
| B4 | STDDEV(age) | [{"table": "workday__employee_overview", "column": "age"}] | [] | False |
| B5 | AVG(tenure_years) | [{"table": "workday__employee_overview", "column": "tenure_years"}] | [] | False |
| B5 | MIN(tenure_years) | [{"table": "workday__employee_overview", "column": "tenure_years"}] | [] | False |
| B5 | MAX(tenure_years) | [{"table": "workday__employee_overview", "column": "tenure_years"}] | [] | False |
| B5 | AVG(tenure_years) | [{"table": "workday__employee_overview", "column": "tenure_years"}] | [] | False |
| B5 | STDDEV(tenure_years) | [{"table": "workday__employee_overview", "column": "tenure_years"}] | [] | False |
| B5 | AVG(tenure_years) | [{"table": "workday__employee_overview", "column": "tenure_years"}] | [] | False |
| B5 | STDDEV(tenure_years) | [{"table": "workday__employee_overview", "column": "tenure_years"}] | [] | False |
| B7 | MIN(total_positions_held) | [{"table": "workday__employee_overview", "column": "total_positions_held"}] | [] | False |
| B7 | MAX(total_positions_held) | [{"table": "workday__employee_overview", "column": "total_positions_held"}] | [] | False |
| B7 | AVG(total_positions_held) | [{"table": "workday__employee_overview", "column": "total_positions_held"}] | [] | False |
| B7 | AVG(total_positions_held) | [{"table": "workday__employee_overview", "column": "total_positions_held"}] | [] | False |
| B7 | STDDEV(total_positions_held) | [{"table": "workday__employee_overview", "column": "total_positions_held"}] | [] | False |
| B7 | AVG(total_positions_held) | [{"table": "workday__employee_overview", "column": "total_positions_held"}] | [] | False |
| B7 | STDDEV(total_positions_held) | [{"table": "workday__employee_overview", "column": "total_positions_held"}] | [] | False |
| B9 | MIN(total_promotions) | [{"table": "workday__employee_overview", "column": "total_promotions"}] | [] | False |
| B9 | MAX(total_promotions) | [{"table": "workday__employee_overview", "column": "total_promotions"}] | [] | False |
| B9 | AVG(total_promotions) | [{"table": "workday__employee_overview", "column": "total_promotions"}] | [] | False |
| B9 | AVG(total_promotions) | [{"table": "workday__employee_overview", "column": "total_promotions"}] | [] | False |
| B9 | STDDEV(total_promotions) | [{"table": "workday__employee_overview", "column": "total_promotions"}] | [] | False |
| B9 | AVG(total_promotions) | [{"table": "workday__employee_overview", "column": "total_promotions"}] | [] | False |
| B9 | STDDEV(total_promotions) | [{"table": "workday__employee_overview", "column": "total_promotions"}] | [] | False |
| B11 | MIN(lateral_moves) | [{"table": "workday__employee_overview", "column": "lateral_moves"}] | [] | False |
| B11 | MAX(lateral_moves) | [{"table": "workday__employee_overview", "column": "lateral_moves"}] | [] | False |
| B11 | AVG(lateral_moves) | [{"table": "workday__employee_overview", "column": "lateral_moves"}] | [] | False |
| B11 | AVG(lateral_moves) | [{"table": "workday__employee_overview", "column": "lateral_moves"}] | [] | False |
| B11 | STDDEV(lateral_moves) | [{"table": "workday__employee_overview", "column": "lateral_moves"}] | [] | False |
| B11 | AVG(lateral_moves) | [{"table": "workday__employee_overview", "column": "lateral_moves"}] | [] | False |
| B11 | STDDEV(lateral_moves) | [{"table": "workday__employee_overview", "column": "lateral_moves"}] | [] | False |
| B13 | MIN(management_positions_held) | [{"table": "workday__employee_overview", "column": "management_positions_held"}] | [] | False |
| B13 | MAX(management_positions_held) | [{"table": "workday__employee_overview", "column": "management_positions_held"}] | [] | False |
| B13 | AVG(management_positions_held) | [{"table": "workday__employee_overview", "column": "management_positions_held"}] | [] | False |
| B13 | AVG(management_positions_held) | [{"table": "workday__employee_overview", "column": "management_positions_held"}] | [] | False |
| B13 | STDDEV(management_positions_held) | [{"table": "workday__employee_overview", "column": "management_positions_held"}] | [] | False |
| B13 | AVG(management_positions_held) | [{"table": "workday__employee_overview", "column": "management_positions_held"}] | [] | False |
| B13 | STDDEV(management_positions_held) | [{"table": "workday__employee_overview", "column": "management_positions_held"}] | [] | False |


## S24

类别 `data`；来源 `query_db`；调用 `400cf74b542e4399a736857d3a764caf`；状态 `success`。

```sql
WITH ranked AS (
  SELECT *, ROW_NUMBER() OVER (PARTITION BY employee_id ORDER BY position_start_date DESC, overall_employee_score DESC, career_development_score DESC, total_promotions DESC) as rn
  FROM workday__employee_overview
),
emp AS (SELECT * FROM ranked WHERE rn = 1),
core AS (
  SELECT * FROM emp 
  WHERE overall_employee_score > 75 AND career_development_score > 78.57581219355939
)
SELECT marital_status, COUNT(*) as cnt, ROUND(100.0 * COUNT(*) / (SELECT COUNT(*) FROM core), 1) as pct
FROM core
GROUP BY marital_status
ORDER BY cnt DESC
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-083/attempt-01/sql/S24.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-083/attempt-01/sql/S24.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-083/attempt-01/results/S24.rows.jsonl)；完整：True；SHA256：`40d0da01efee0db69851814022b0890826f4c1f0cc38de10bc8bd8d81cf8546c`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "workday__employee_overview", "kind": "base", "block": null, "base_tables": ["workday__employee_overview"]}] | [] | [] |
| B2 | [{"alias": "ranked", "kind": "derived", "block": "B1", "base_tables": ["workday__employee_overview"]}] | [] | [] |
| B3 | [{"alias": "emp", "kind": "derived", "block": "B2", "base_tables": ["workday__employee_overview"]}] | [] | [] |
| B4 | [{"alias": "core", "kind": "derived", "block": "B3", "base_tables": ["workday__employee_overview"]}] | [] | [] |
| B5 | [{"alias": "core", "kind": "derived", "block": "B3", "base_tables": ["workday__employee_overview"]}] | [] | ["marital_status"] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B4 | COUNT(*) | [] | [] | True |
| B5 | COUNT(*) | [] | [] | True |
| B5 | COUNT(*) | [] | [] | True |


## S25

类别 `data`；来源 `query_db`；调用 `161a5dcfefd74e20b07613fa24573e2b`；状态 `success`。

```sql
WITH ranked AS (
  SELECT *, ROW_NUMBER() OVER (PARTITION BY employee_id ORDER BY position_start_date DESC, overall_employee_score DESC, career_development_score DESC, total_promotions DESC) as rn
  FROM workday__employee_overview
),
emp AS (SELECT * FROM ranked WHERE rn = 1),
core AS (
  SELECT * FROM emp 
  WHERE overall_employee_score > 75 AND career_development_score > 78.57581219355939
)
SELECT ethnicity_codes, COUNT(*) as cnt, ROUND(100.0 * COUNT(*) / (SELECT COUNT(*) FROM core), 1) as pct
FROM core
GROUP BY ethnicity_codes
ORDER BY cnt DESC
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-083/attempt-01/sql/S25.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-083/attempt-01/sql/S25.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-083/attempt-01/results/S25.rows.jsonl)；完整：True；SHA256：`dea4af73e7bd7fdc0dc0ea411db3b5c693985736b450de5c410eacfc0053d43a`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "workday__employee_overview", "kind": "base", "block": null, "base_tables": ["workday__employee_overview"]}] | [] | [] |
| B2 | [{"alias": "ranked", "kind": "derived", "block": "B1", "base_tables": ["workday__employee_overview"]}] | [] | [] |
| B3 | [{"alias": "emp", "kind": "derived", "block": "B2", "base_tables": ["workday__employee_overview"]}] | [] | [] |
| B4 | [{"alias": "core", "kind": "derived", "block": "B3", "base_tables": ["workday__employee_overview"]}] | [] | [] |
| B5 | [{"alias": "core", "kind": "derived", "block": "B3", "base_tables": ["workday__employee_overview"]}] | [] | ["ethnicity_codes"] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B4 | COUNT(*) | [] | [] | True |
| B5 | COUNT(*) | [] | [] | True |
| B5 | COUNT(*) | [] | [] | True |


## S26

类别 `data`；来源 `query_db`；调用 `829e2b586b924b8dad186ae664230e0c`；状态 `success`。

```sql
WITH ranked AS (
  SELECT *, ROW_NUMBER() OVER (PARTITION BY employee_id ORDER BY position_start_date DESC, overall_employee_score DESC, career_development_score DESC, total_promotions DESC) as rn
  FROM workday__employee_overview
),
emp AS (SELECT * FROM ranked WHERE rn = 1),
core AS (
  SELECT * FROM emp 
  WHERE overall_employee_score > 75 AND career_development_score > 78.57581219355939
)
SELECT 
  'Age' as feature,
  ROUND(AVG(age), 1) as avg_val,
  MIN(age) as min_val,
  MAX(age) as max_val
FROM core
UNION ALL
SELECT 
  'Tenure_years',
  ROUND(AVG(tenure_years), 2),
  ROUND(MIN(tenure_years), 2),
  ROUND(MAX(tenure_years), 2)
FROM core
UNION ALL
SELECT 
  'Total_positions_held',
  ROUND(AVG(total_positions_held), 2),
  MIN(total_positions_held),
  MAX(total_positions_held)
FROM core
UNION ALL
SELECT 
  'Total_promotions',
  ROUND(AVG(total_promotions), 2),
  MIN(total_promotions),
  MAX(total_promotions)
FROM core
UNION ALL
SELECT 
  'Lateral_moves',
  ROUND(AVG(lateral_moves), 2),
  MIN(lateral_moves),
  MAX(lateral_moves)
FROM core
UNION ALL
SELECT 
  'Management_positions_held',
  ROUND(AVG(management_positions_held), 2),
  MIN(management_positions_held),
  MAX(management_positions_held)
FROM core
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-083/attempt-01/sql/S26.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-083/attempt-01/sql/S26.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-083/attempt-01/results/S26.rows.jsonl)；完整：True；SHA256：`5b092bedc39667790cf5bf22ece00842de07dcc0acbcfb3a3c7a56d4a9a93c00`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "workday__employee_overview", "kind": "base", "block": null, "base_tables": ["workday__employee_overview"]}] | [] | [] |
| B2 | [{"alias": "ranked", "kind": "derived", "block": "B1", "base_tables": ["workday__employee_overview"]}] | [] | [] |
| B3 | [{"alias": "emp", "kind": "derived", "block": "B2", "base_tables": ["workday__employee_overview"]}] | [] | [] |
| B4 | [{"alias": "core", "kind": "derived", "block": "B3", "base_tables": ["workday__employee_overview"]}] | [] | [] |
| B5 | [{"alias": "core", "kind": "derived", "block": "B3", "base_tables": ["workday__employee_overview"]}] | [] | [] |
| B6 | [] | [] | [] |
| B7 | [{"alias": "core", "kind": "derived", "block": "B3", "base_tables": ["workday__employee_overview"]}] | [] | [] |
| B8 | [] | [] | [] |
| B9 | [{"alias": "core", "kind": "derived", "block": "B3", "base_tables": ["workday__employee_overview"]}] | [] | [] |
| B10 | [] | [] | [] |
| B11 | [{"alias": "core", "kind": "derived", "block": "B3", "base_tables": ["workday__employee_overview"]}] | [] | [] |
| B12 | [] | [] | [] |
| B13 | [{"alias": "core", "kind": "derived", "block": "B3", "base_tables": ["workday__employee_overview"]}] | [] | [] |
| B14 | [] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B4 | MIN(age) | [{"table": "workday__employee_overview", "column": "age"}] | [] | False |
| B4 | MAX(age) | [{"table": "workday__employee_overview", "column": "age"}] | [] | False |
| B4 | AVG(age) | [{"table": "workday__employee_overview", "column": "age"}] | [] | False |
| B5 | AVG(tenure_years) | [{"table": "workday__employee_overview", "column": "tenure_years"}] | [] | False |
| B5 | MIN(tenure_years) | [{"table": "workday__employee_overview", "column": "tenure_years"}] | [] | False |
| B5 | MAX(tenure_years) | [{"table": "workday__employee_overview", "column": "tenure_years"}] | [] | False |
| B7 | MIN(total_positions_held) | [{"table": "workday__employee_overview", "column": "total_positions_held"}] | [] | False |
| B7 | MAX(total_positions_held) | [{"table": "workday__employee_overview", "column": "total_positions_held"}] | [] | False |
| B7 | AVG(total_positions_held) | [{"table": "workday__employee_overview", "column": "total_positions_held"}] | [] | False |
| B9 | MIN(total_promotions) | [{"table": "workday__employee_overview", "column": "total_promotions"}] | [] | False |
| B9 | MAX(total_promotions) | [{"table": "workday__employee_overview", "column": "total_promotions"}] | [] | False |
| B9 | AVG(total_promotions) | [{"table": "workday__employee_overview", "column": "total_promotions"}] | [] | False |
| B11 | MIN(lateral_moves) | [{"table": "workday__employee_overview", "column": "lateral_moves"}] | [] | False |
| B11 | MAX(lateral_moves) | [{"table": "workday__employee_overview", "column": "lateral_moves"}] | [] | False |
| B11 | AVG(lateral_moves) | [{"table": "workday__employee_overview", "column": "lateral_moves"}] | [] | False |
| B13 | MIN(management_positions_held) | [{"table": "workday__employee_overview", "column": "management_positions_held"}] | [] | False |
| B13 | MAX(management_positions_held) | [{"table": "workday__employee_overview", "column": "management_positions_held"}] | [] | False |
| B13 | AVG(management_positions_held) | [{"table": "workday__employee_overview", "column": "management_positions_held"}] | [] | False |


## S27

类别 `data`；来源 `query_db`；调用 `a63bbb14bec341839ad7a29ba292ba23`；状态 `success`。

```sql
WITH ranked AS (
  SELECT *, ROW_NUMBER() OVER (PARTITION BY employee_id ORDER BY position_start_date DESC, overall_employee_score DESC, career_development_score DESC, total_promotions DESC) as rn
  FROM workday__employee_overview
),
emp AS (SELECT * FROM ranked WHERE rn = 1),
core AS (
  SELECT * FROM emp 
  WHERE overall_employee_score > 75 AND career_development_score > 78.57581219355939
)
SELECT 
  career_phase,
  employee_maturity_segment,
  COUNT(*) as total_core,
  SUM(CASE WHEN employee_risk_level = 'High' THEN 1 ELSE 0 END) as high_risk,
  ROUND(100.0 * SUM(CASE WHEN employee_risk_level = 'High' THEN 1 ELSE 0 END) / COUNT(*), 1) as high_risk_pct,
  SUM(CASE WHEN employee_risk_level = 'Medium' THEN 1 ELSE 0 END) as medium_risk,
  ROUND(100.0 * SUM(CASE WHEN employee_risk_level = 'Medium' THEN 1 ELSE 0 END) / COUNT(*), 1) as medium_risk_pct,
  SUM(CASE WHEN employee_risk_level = 'Low' THEN 1 ELSE 0 END) as low_risk,
  ROUND(100.0 * SUM(CASE WHEN employee_risk_level = 'Low' THEN 1 ELSE 0 END) / COUNT(*), 1) as low_risk_pct
FROM core
GROUP BY career_phase, employee_maturity_segment
ORDER BY career_phase, employee_maturity_segment
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-083/attempt-01/sql/S27.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-083/attempt-01/sql/S27.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-083/attempt-01/results/S27.rows.jsonl)；完整：True；SHA256：`0e2a3f447e6fbbd4580b6ad8ee609caf6cc9c0992a5bd05af987039094fce279`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "workday__employee_overview", "kind": "base", "block": null, "base_tables": ["workday__employee_overview"]}] | [] | [] |
| B2 | [{"alias": "ranked", "kind": "derived", "block": "B1", "base_tables": ["workday__employee_overview"]}] | [] | [] |
| B3 | [{"alias": "emp", "kind": "derived", "block": "B2", "base_tables": ["workday__employee_overview"]}] | [] | [] |
| B4 | [{"alias": "core", "kind": "derived", "block": "B3", "base_tables": ["workday__employee_overview"]}] | [] | ["career_phase", "employee_maturity_segment"] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B4 | COUNT(*) | [] | [] | True |
| B4 | SUM(CASE WHEN employee_risk_level = 'High' THEN 1 ELSE 0 END) | [] | [{"table": "workday__employee_overview", "column": "employee_risk_level"}] | False |
| B4 | SUM(CASE WHEN employee_risk_level = 'Medium' THEN 1 ELSE 0 END) | [] | [{"table": "workday__employee_overview", "column": "employee_risk_level"}] | False |
| B4 | SUM(CASE WHEN employee_risk_level = 'Low' THEN 1 ELSE 0 END) | [] | [{"table": "workday__employee_overview", "column": "employee_risk_level"}] | False |
| B4 | COUNT(*) | [] | [] | True |
| B4 | COUNT(*) | [] | [] | True |
| B4 | COUNT(*) | [] | [] | True |
| B4 | SUM(CASE WHEN employee_risk_level = 'High' THEN 1 ELSE 0 END) | [] | [{"table": "workday__employee_overview", "column": "employee_risk_level"}] | False |
| B4 | SUM(CASE WHEN employee_risk_level = 'Medium' THEN 1 ELSE 0 END) | [] | [{"table": "workday__employee_overview", "column": "employee_risk_level"}] | False |
| B4 | SUM(CASE WHEN employee_risk_level = 'Low' THEN 1 ELSE 0 END) | [] | [{"table": "workday__employee_overview", "column": "employee_risk_level"}] | False |


## S28

类别 `data`；来源 `query_db`；调用 `c3ad2696ae7c49db9c4755918ca4007f`；状态 `success`。

```sql
WITH ranked AS (
  SELECT *, ROW_NUMBER() OVER (PARTITION BY employee_id ORDER BY position_start_date DESC, overall_employee_score DESC, career_development_score DESC, total_promotions DESC) as rn
  FROM workday__employee_overview
),
emp AS (SELECT * FROM ranked WHERE rn = 1),
core AS (
  SELECT * FROM emp 
  WHERE overall_employee_score > 75 AND career_development_score > 78.57581219355939
)
SELECT 
  compensation_tier,
  COUNT(*) as total_core,
  SUM(CASE WHEN employee_risk_level = 'High' THEN 1 ELSE 0 END) as high_risk,
  ROUND(100.0 * SUM(CASE WHEN employee_risk_level = 'High' THEN 1 ELSE 0 END) / COUNT(*), 1) as high_risk_pct,
  ROUND(AVG(work_conditions_score), 1) as avg_work_cond,
  ROUND(AVG(dept_turnover_rate), 3) as avg_turnover,
  ROUND(AVG(dept_management_ratio), 3) as avg_mgmt_ratio,
  ROUND(AVG(dept_health_score), 1) as avg_dept_health
FROM core
GROUP BY compensation_tier
ORDER BY high_risk_pct DESC
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-083/attempt-01/sql/S28.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-083/attempt-01/sql/S28.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-083/attempt-01/results/S28.rows.jsonl)；完整：True；SHA256：`77598d4ac40f378ecb8bb0b5c65d502e2273151f5c98c4e43e6e78136b075451`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "workday__employee_overview", "kind": "base", "block": null, "base_tables": ["workday__employee_overview"]}] | [] | [] |
| B2 | [{"alias": "ranked", "kind": "derived", "block": "B1", "base_tables": ["workday__employee_overview"]}] | [] | [] |
| B3 | [{"alias": "emp", "kind": "derived", "block": "B2", "base_tables": ["workday__employee_overview"]}] | [] | [] |
| B4 | [{"alias": "core", "kind": "derived", "block": "B3", "base_tables": ["workday__employee_overview"]}] | [] | ["compensation_tier"] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B4 | COUNT(*) | [] | [] | True |
| B4 | SUM(CASE WHEN employee_risk_level = 'High' THEN 1 ELSE 0 END) | [] | [{"table": "workday__employee_overview", "column": "employee_risk_level"}] | False |
| B4 | AVG(work_conditions_score) | [{"table": "workday__employee_overview", "column": "work_conditions_score"}] | [] | False |
| B4 | AVG(dept_turnover_rate) | [{"table": "workday__employee_overview", "column": "dept_turnover_rate"}] | [] | False |
| B4 | AVG(dept_management_ratio) | [{"table": "workday__employee_overview", "column": "dept_management_ratio"}] | [] | False |
| B4 | AVG(dept_health_score) | [{"table": "workday__employee_overview", "column": "dept_health_score"}] | [] | False |
| B4 | COUNT(*) | [] | [] | True |
| B4 | SUM(CASE WHEN employee_risk_level = 'High' THEN 1 ELSE 0 END) | [] | [{"table": "workday__employee_overview", "column": "employee_risk_level"}] | False |


## S29

类别 `data`；来源 `query_db`；调用 `f24bac3d2f0d4e78b7547c8288cf1339`；状态 `success`。

```sql
WITH ranked AS (
  SELECT *, ROW_NUMBER() OVER (PARTITION BY employee_id ORDER BY position_start_date DESC, overall_employee_score DESC, career_development_score DESC, total_promotions DESC) as rn
  FROM workday__employee_overview
),
emp AS (SELECT * FROM ranked WHERE rn = 1),
core AS (
  SELECT * FROM emp 
  WHERE overall_employee_score > 75 AND career_development_score > 78.57581219355939
)
SELECT 
  organization_type,
  COUNT(*) as total_core,
  SUM(CASE WHEN employee_risk_level = 'High' THEN 1 ELSE 0 END) as high_risk,
  ROUND(100.0 * SUM(CASE WHEN employee_risk_level = 'High' THEN 1 ELSE 0 END) / COUNT(*), 1) as high_risk_pct,
  ROUND(AVG(dept_turnover_rate), 3) as avg_turnover,
  ROUND(AVG(dept_health_score), 1) as avg_dept_health
FROM core
GROUP BY organization_type
ORDER BY high_risk_pct DESC
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-083/attempt-01/sql/S29.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-083/attempt-01/sql/S29.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-083/attempt-01/results/S29.rows.jsonl)；完整：True；SHA256：`b64bf55a8a39cf8b3de1f55a971dd16d28f6f8f5e3cc9c713c91ba38f526bdab`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "workday__employee_overview", "kind": "base", "block": null, "base_tables": ["workday__employee_overview"]}] | [] | [] |
| B2 | [{"alias": "ranked", "kind": "derived", "block": "B1", "base_tables": ["workday__employee_overview"]}] | [] | [] |
| B3 | [{"alias": "emp", "kind": "derived", "block": "B2", "base_tables": ["workday__employee_overview"]}] | [] | [] |
| B4 | [{"alias": "core", "kind": "derived", "block": "B3", "base_tables": ["workday__employee_overview"]}] | [] | ["organization_type"] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B4 | COUNT(*) | [] | [] | True |
| B4 | SUM(CASE WHEN employee_risk_level = 'High' THEN 1 ELSE 0 END) | [] | [{"table": "workday__employee_overview", "column": "employee_risk_level"}] | False |
| B4 | AVG(dept_turnover_rate) | [{"table": "workday__employee_overview", "column": "dept_turnover_rate"}] | [] | False |
| B4 | AVG(dept_health_score) | [{"table": "workday__employee_overview", "column": "dept_health_score"}] | [] | False |
| B4 | COUNT(*) | [] | [] | True |
| B4 | SUM(CASE WHEN employee_risk_level = 'High' THEN 1 ELSE 0 END) | [] | [{"table": "workday__employee_overview", "column": "employee_risk_level"}] | False |


## S30

类别 `data`；来源 `query_db`；调用 `c72ec2fc7c084d94baf7bb093ce4eb7f`；状态 `success`。

```sql
WITH ranked AS (
  SELECT *, ROW_NUMBER() OVER (PARTITION BY employee_id ORDER BY position_start_date DESC, overall_employee_score DESC, career_development_score DESC, total_promotions DESC) as rn
  FROM workday__employee_overview
),
emp AS (SELECT * FROM ranked WHERE rn = 1),
core AS (
  SELECT * FROM emp 
  WHERE overall_employee_score > 75 AND career_development_score > 78.57581219355939
)
SELECT employee_risk_level, COUNT(*) as cnt, ROUND(100.0 * COUNT(*) / (SELECT COUNT(*) FROM core), 1) as pct
FROM core
GROUP BY employee_risk_level
ORDER BY cnt DESC
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-083/attempt-01/sql/S30.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-083/attempt-01/sql/S30.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-083/attempt-01/results/S30.rows.jsonl)；完整：True；SHA256：`d2b57cc9ab205f65395f3a8e5c677e094bc6e69a396f660fae9f5456c8a1998b`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "workday__employee_overview", "kind": "base", "block": null, "base_tables": ["workday__employee_overview"]}] | [] | [] |
| B2 | [{"alias": "ranked", "kind": "derived", "block": "B1", "base_tables": ["workday__employee_overview"]}] | [] | [] |
| B3 | [{"alias": "emp", "kind": "derived", "block": "B2", "base_tables": ["workday__employee_overview"]}] | [] | [] |
| B4 | [{"alias": "core", "kind": "derived", "block": "B3", "base_tables": ["workday__employee_overview"]}] | [] | [] |
| B5 | [{"alias": "core", "kind": "derived", "block": "B3", "base_tables": ["workday__employee_overview"]}] | [] | ["employee_risk_level"] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B4 | COUNT(*) | [] | [] | True |
| B5 | COUNT(*) | [] | [] | True |
| B5 | COUNT(*) | [] | [] | True |


## S31

类别 `data`；来源 `query_db`；调用 `16dd8d95d2bf42f8b9029ef9ff82d0c6`；状态 `success`。

```sql
WITH ranked AS (
  SELECT *, ROW_NUMBER() OVER (PARTITION BY employee_id ORDER BY position_start_date DESC, overall_employee_score DESC, career_development_score DESC, total_promotions DESC) as rn
  FROM workday__employee_overview
),
emp AS (SELECT * FROM ranked WHERE rn = 1),
core AS (
  SELECT * FROM emp 
  WHERE overall_employee_score > 75 AND career_development_score > 78.57581219355939
)
SELECT 
  employee_risk_level,
  ROUND(AVG(work_conditions_score), 1) as avg_work_cond,
  ROUND(AVG(dept_turnover_rate), 3) as avg_turnover,
  ROUND(AVG(dept_management_ratio), 3) as avg_mgmt_ratio,
  ROUND(AVG(dept_health_score), 1) as avg_dept_health,
  ROUND(AVG(compensation_tier), 1) as avg_comp
FROM core
GROUP BY employee_risk_level
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-083/attempt-01/sql/S31.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-083/attempt-01/sql/S31.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-083/attempt-01/results/S31.rows.jsonl)；完整：True；SHA256：`cc8b51702cb23097e186a5361facb325f48894b3b0866238cd39268241fa6d44`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "workday__employee_overview", "kind": "base", "block": null, "base_tables": ["workday__employee_overview"]}] | [] | [] |
| B2 | [{"alias": "ranked", "kind": "derived", "block": "B1", "base_tables": ["workday__employee_overview"]}] | [] | [] |
| B3 | [{"alias": "emp", "kind": "derived", "block": "B2", "base_tables": ["workday__employee_overview"]}] | [] | [] |
| B4 | [{"alias": "core", "kind": "derived", "block": "B3", "base_tables": ["workday__employee_overview"]}] | [] | ["employee_risk_level"] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B4 | AVG(work_conditions_score) | [{"table": "workday__employee_overview", "column": "work_conditions_score"}] | [] | False |
| B4 | AVG(dept_turnover_rate) | [{"table": "workday__employee_overview", "column": "dept_turnover_rate"}] | [] | False |
| B4 | AVG(dept_management_ratio) | [{"table": "workday__employee_overview", "column": "dept_management_ratio"}] | [] | False |
| B4 | AVG(dept_health_score) | [{"table": "workday__employee_overview", "column": "dept_health_score"}] | [] | False |
| B4 | AVG(compensation_tier) | [{"table": "workday__employee_overview", "column": "compensation_tier"}] | [] | False |


## S32

类别 `data`；来源 `query_db`；调用 `38f90bc79ead43499b0f9c8767e080f9`；状态 `success`。

```sql
WITH ranked AS (
  SELECT *, ROW_NUMBER() OVER (PARTITION BY employee_id ORDER BY position_start_date DESC, overall_employee_score DESC, career_development_score DESC, total_promotions DESC) as rn
  FROM workday__employee_overview
),
emp AS (SELECT * FROM ranked WHERE rn = 1)
SELECT 
  COUNT(*) as total_emp,
  SUM(CASE WHEN retention_stability_score < 60 AND overall_employee_score > 80 THEN 1 ELSE 0 END) as high_value_attrition_risk
FROM emp
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-083/attempt-01/sql/S32.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-083/attempt-01/sql/S32.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-083/attempt-01/results/S32.rows.jsonl)；完整：True；SHA256：`0fb96b2f917588109dc72791d0e3c7c3b446de45df11e1201dada868025cf701`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "workday__employee_overview", "kind": "base", "block": null, "base_tables": ["workday__employee_overview"]}] | [] | [] |
| B2 | [{"alias": "ranked", "kind": "derived", "block": "B1", "base_tables": ["workday__employee_overview"]}] | [] | [] |
| B3 | [{"alias": "emp", "kind": "derived", "block": "B2", "base_tables": ["workday__employee_overview"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B3 | COUNT(*) | [] | [] | True |
| B3 | SUM(CASE WHEN retention_stability_score < 60 AND overall_employee_score > 80 THEN 1 ELSE 0 END) | [] | [{"table": "workday__employee_overview", "column": "retention_stability_score"}, {"table": "workday__employee_overview", "column": "overall_employee_score"}] | False |


## S33

类别 `data`；来源 `query_db`；调用 `9a83831f7cc84f31a8cd1e43676bbaa4`；状态 `success`。

```sql
WITH ranked AS (
  SELECT *, ROW_NUMBER() OVER (PARTITION BY employee_id ORDER BY position_start_date DESC, overall_employee_score DESC, career_development_score DESC, total_promotions DESC) as rn
  FROM workday__employee_overview
),
emp AS (SELECT * FROM ranked WHERE rn = 1)
SELECT 
  employee_value_segment,
  COUNT(*) as cnt,
  ROUND(100.0 * COUNT(*) / (SELECT COUNT(*) FROM emp WHERE retention_stability_score < 60 AND overall_employee_score > 80), 1) as pct
FROM emp
WHERE retention_stability_score < 60 AND overall_employee_score > 80
GROUP BY employee_value_segment
ORDER BY cnt DESC
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-083/attempt-01/sql/S33.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-083/attempt-01/sql/S33.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-083/attempt-01/results/S33.rows.jsonl)；完整：True；SHA256：`a5991fefade1d45cc12d32d9c198f6677a0b9a5985d63b20799a739be4be533f`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "workday__employee_overview", "kind": "base", "block": null, "base_tables": ["workday__employee_overview"]}] | [] | [] |
| B2 | [{"alias": "ranked", "kind": "derived", "block": "B1", "base_tables": ["workday__employee_overview"]}] | [] | [] |
| B3 | [{"alias": "emp", "kind": "derived", "block": "B2", "base_tables": ["workday__employee_overview"]}] | [] | [] |
| B4 | [{"alias": "emp", "kind": "derived", "block": "B2", "base_tables": ["workday__employee_overview"]}] | [] | ["employee_value_segment"] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B3 | COUNT(*) | [] | [] | True |
| B4 | COUNT(*) | [] | [] | True |
| B4 | COUNT(*) | [] | [] | True |


## S34

类别 `data`；来源 `query_db`；调用 `8e9f4036a40e46a39ddfb99da4d2e06f`；状态 `success`。

```sql
WITH ranked AS (
  SELECT *, ROW_NUMBER() OVER (PARTITION BY employee_id ORDER BY position_start_date DESC, overall_employee_score DESC, career_development_score DESC, total_promotions DESC) as rn
  FROM workday__employee_overview
),
emp AS (SELECT * FROM ranked WHERE rn = 1)
SELECT 
  SUM(is_work_shift_required) as shift_required,
  SUM(is_union_eligible) as union_eligible,
  ROUND(100.0 * SUM(is_work_shift_required) / COUNT(*), 1) as shift_required_pct,
  ROUND(100.0 * SUM(is_union_eligible) / COUNT(*), 1) as union_eligible_pct
FROM emp
WHERE retention_stability_score < 60 AND overall_employee_score > 80
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-083/attempt-01/sql/S34.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-083/attempt-01/sql/S34.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-083/attempt-01/results/S34.rows.jsonl)；完整：True；SHA256：`4e29dce81242a892e5640c5a013cff393bb129e52b4899a8ec844e8eef6c6ae9`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "workday__employee_overview", "kind": "base", "block": null, "base_tables": ["workday__employee_overview"]}] | [] | [] |
| B2 | [{"alias": "ranked", "kind": "derived", "block": "B1", "base_tables": ["workday__employee_overview"]}] | [] | [] |
| B3 | [{"alias": "emp", "kind": "derived", "block": "B2", "base_tables": ["workday__employee_overview"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B3 | SUM(is_work_shift_required) | [{"table": "workday__employee_overview", "column": "is_work_shift_required"}] | [] | False |
| B3 | SUM(is_union_eligible) | [{"table": "workday__employee_overview", "column": "is_union_eligible"}] | [] | False |
| B3 | COUNT(*) | [] | [] | True |
| B3 | COUNT(*) | [] | [] | True |
| B3 | SUM(is_work_shift_required) | [{"table": "workday__employee_overview", "column": "is_work_shift_required"}] | [] | False |
| B3 | SUM(is_union_eligible) | [{"table": "workday__employee_overview", "column": "is_union_eligible"}] | [] | False |


## S35

类别 `data`；来源 `query_db`；调用 `7707cc13eae04a4b98255825746413e6`；状态 `success`。

```sql
WITH ranked AS (
  SELECT *, ROW_NUMBER() OVER (PARTITION BY employee_id ORDER BY position_start_date DESC, overall_employee_score DESC, career_development_score DESC, total_promotions DESC) as rn
  FROM workday__employee_overview
),
emp AS (SELECT * FROM ranked WHERE rn = 1)
SELECT 
  'All employees' as grp,
  COUNT(*) as n,
  ROUND(100.0 * SUM(is_work_shift_required) / COUNT(*), 1) as shift_pct,
  ROUND(100.0 * SUM(is_union_eligible) / COUNT(*), 1) as union_pct,
  ROUND(AVG(retention_stability_score), 1) as avg_retention,
  ROUND(AVG(overall_employee_score), 1) as avg_overall
FROM emp
UNION ALL
SELECT 
  'High-value attrition risk',
  COUNT(*),
  ROUND(100.0 * SUM(is_work_shift_required) / COUNT(*), 1),
  ROUND(100.0 * SUM(is_union_eligible) / COUNT(*), 1),
  ROUND(AVG(retention_stability_score), 1),
  ROUND(AVG(overall_employee_score), 1)
FROM emp
WHERE retention_stability_score < 60 AND overall_employee_score > 80
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-083/attempt-01/sql/S35.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-083/attempt-01/sql/S35.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-083/attempt-01/results/S35.rows.jsonl)；完整：True；SHA256：`bd9b15a8ce9616cda49f7a0afe319ddccad9ab998f840442cd1078a209a0d559`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "workday__employee_overview", "kind": "base", "block": null, "base_tables": ["workday__employee_overview"]}] | [] | [] |
| B2 | [{"alias": "ranked", "kind": "derived", "block": "B1", "base_tables": ["workday__employee_overview"]}] | [] | [] |
| B3 | [{"alias": "emp", "kind": "derived", "block": "B2", "base_tables": ["workday__employee_overview"]}] | [] | [] |
| B4 | [{"alias": "emp", "kind": "derived", "block": "B2", "base_tables": ["workday__employee_overview"]}] | [] | [] |
| B5 | [] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B3 | COUNT(*) | [] | [] | True |
| B3 | AVG(retention_stability_score) | [{"table": "workday__employee_overview", "column": "retention_stability_score"}] | [] | False |
| B3 | AVG(overall_employee_score) | [{"table": "workday__employee_overview", "column": "overall_employee_score"}] | [] | False |
| B3 | COUNT(*) | [] | [] | True |
| B3 | COUNT(*) | [] | [] | True |
| B3 | SUM(is_work_shift_required) | [{"table": "workday__employee_overview", "column": "is_work_shift_required"}] | [] | False |
| B3 | SUM(is_union_eligible) | [{"table": "workday__employee_overview", "column": "is_union_eligible"}] | [] | False |
| B4 | COUNT(*) | [] | [] | True |
| B4 | AVG(retention_stability_score) | [{"table": "workday__employee_overview", "column": "retention_stability_score"}] | [] | False |
| B4 | AVG(overall_employee_score) | [{"table": "workday__employee_overview", "column": "overall_employee_score"}] | [] | False |
| B4 | COUNT(*) | [] | [] | True |
| B4 | COUNT(*) | [] | [] | True |
| B4 | SUM(is_work_shift_required) | [{"table": "workday__employee_overview", "column": "is_work_shift_required"}] | [] | False |
| B4 | SUM(is_union_eligible) | [{"table": "workday__employee_overview", "column": "is_union_eligible"}] | [] | False |


## S36

类别 `data`；来源 `query_db`；调用 `bc1ef2e4fbfa4e5eacb7f93e44b22388`；状态 `success`。

```sql
WITH ranked AS (
  SELECT *, ROW_NUMBER() OVER (PARTITION BY employee_id ORDER BY position_start_date DESC, overall_employee_score DESC, career_development_score DESC, total_promotions DESC) as rn
  FROM workday__employee_overview
),
emp AS (SELECT * FROM ranked WHERE rn = 1)
SELECT DISTINCT employee_value_segment FROM emp ORDER BY employee_value_segment
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-083/attempt-01/sql/S36.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-083/attempt-01/sql/S36.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-083/attempt-01/results/S36.rows.jsonl)；完整：True；SHA256：`5360b64ce34a540f688d709eeccf9a6c019091e1531399b0a47b71ec1099bff8`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "workday__employee_overview", "kind": "base", "block": null, "base_tables": ["workday__employee_overview"]}] | [] | [] |
| B2 | [{"alias": "ranked", "kind": "derived", "block": "B1", "base_tables": ["workday__employee_overview"]}] | [] | [] |
| B3 | [{"alias": "emp", "kind": "derived", "block": "B2", "base_tables": ["workday__employee_overview"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |


## S37

类别 `data`；来源 `query_db`；调用 `f964774d1f43403884383a5cd947ae84`；状态 `success`。

```sql
WITH ranked AS (
  SELECT *, ROW_NUMBER() OVER (PARTITION BY employee_id ORDER BY position_start_date DESC, overall_employee_score DESC, career_development_score DESC, total_promotions DESC) as rn
  FROM workday__employee_overview
),
emp AS (SELECT * FROM ranked WHERE rn = 1)
SELECT DISTINCT highest_management_level_reached FROM emp ORDER BY highest_management_level_reached
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-083/attempt-01/sql/S37.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-083/attempt-01/sql/S37.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-083/attempt-01/results/S37.rows.jsonl)；完整：True；SHA256：`d64de5f980a4023eddd9abca403c4aa44fd99f38c2b24220be97b13195f4cf22`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "workday__employee_overview", "kind": "base", "block": null, "base_tables": ["workday__employee_overview"]}] | [] | [] |
| B2 | [{"alias": "ranked", "kind": "derived", "block": "B1", "base_tables": ["workday__employee_overview"]}] | [] | [] |
| B3 | [{"alias": "emp", "kind": "derived", "block": "B2", "base_tables": ["workday__employee_overview"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |


## S38

类别 `data`；来源 `query_db`；调用 `1c493accaf3244e1bb3b60ca4149c0b8`；状态 `success`。

```sql
WITH ranked AS (
  SELECT *, ROW_NUMBER() OVER (PARTITION BY employee_id ORDER BY position_start_date DESC, overall_employee_score DESC, career_development_score DESC, total_promotions DESC) as rn
  FROM workday__employee_overview
),
emp AS (SELECT * FROM ranked WHERE rn = 1)
SELECT DISTINCT dept_performance_category FROM emp ORDER BY dept_performance_category
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-083/attempt-01/sql/S38.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-083/attempt-01/sql/S38.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-083/attempt-01/results/S38.rows.jsonl)；完整：True；SHA256：`bcc004293e3f50caa36e77b90e7d30995882e99f5ad651db249a0d103be8402f`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "workday__employee_overview", "kind": "base", "block": null, "base_tables": ["workday__employee_overview"]}] | [] | [] |
| B2 | [{"alias": "ranked", "kind": "derived", "block": "B1", "base_tables": ["workday__employee_overview"]}] | [] | [] |
| B3 | [{"alias": "emp", "kind": "derived", "block": "B2", "base_tables": ["workday__employee_overview"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |


## S39

类别 `data`；来源 `query_db`；调用 `bea2b18dc18744cb9548dce671ac1a0d`；状态 `success`。

```sql
WITH ranked AS (
  SELECT *, ROW_NUMBER() OVER (PARTITION BY employee_id ORDER BY position_start_date DESC, overall_employee_score DESC, career_development_score DESC, total_promotions DESC) as rn
  FROM workday__employee_overview
),
emp AS (SELECT * FROM ranked WHERE rn = 1)
SELECT DISTINCT organization_sub_type FROM emp ORDER BY organization_sub_type
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-083/attempt-01/sql/S39.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-083/attempt-01/sql/S39.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-083/attempt-01/results/S39.rows.jsonl)；完整：True；SHA256：`b326b7481498cde6eab663169b904dad3526da0b66a900b1511a9c7bce8b9278`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "workday__employee_overview", "kind": "base", "block": null, "base_tables": ["workday__employee_overview"]}] | [] | [] |
| B2 | [{"alias": "ranked", "kind": "derived", "block": "B1", "base_tables": ["workday__employee_overview"]}] | [] | [] |
| B3 | [{"alias": "emp", "kind": "derived", "block": "B2", "base_tables": ["workday__employee_overview"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |


## S40

类别 `data`；来源 `query_db`；调用 `77f05d0cf57644ff933550a36d302bd7`；状态 `success`。

```sql
WITH ranked AS (
  SELECT *, ROW_NUMBER() OVER (PARTITION BY employee_id ORDER BY position_start_date DESC, overall_employee_score DESC, career_development_score DESC, total_promotions DESC) as rn
  FROM workday__employee_overview
),
emp AS (SELECT * FROM ranked WHERE rn = 1)
SELECT organization_sub_type, COUNT(*) as cnt FROM emp GROUP BY organization_sub_type ORDER BY cnt DESC
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-083/attempt-01/sql/S40.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-083/attempt-01/sql/S40.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-083/attempt-01/results/S40.rows.jsonl)；完整：True；SHA256：`32cc20a6416bfde5a855a494d6c43d1e641bbddc6882f879747e862268b0e94a`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "workday__employee_overview", "kind": "base", "block": null, "base_tables": ["workday__employee_overview"]}] | [] | [] |
| B2 | [{"alias": "ranked", "kind": "derived", "block": "B1", "base_tables": ["workday__employee_overview"]}] | [] | [] |
| B3 | [{"alias": "emp", "kind": "derived", "block": "B2", "base_tables": ["workday__employee_overview"]}] | [] | ["organization_sub_type"] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B3 | COUNT(*) | [] | [] | True |


## S41

类别 `data`；来源 `query_db`；调用 `539823daf6c54c4faf561a89283599c6`；状态 `success`。

```sql
WITH ranked AS (
  SELECT *, ROW_NUMBER() OVER (PARTITION BY employee_id ORDER BY position_start_date DESC, overall_employee_score DESC, career_development_score DESC, total_promotions DESC) as rn
  FROM workday__employee_overview
),
emp AS (SELECT * FROM ranked WHERE rn = 1),
core AS (
  SELECT * FROM emp 
  WHERE overall_employee_score > 75 AND career_development_score > 78.57581219355939
)
SELECT 
  highest_management_level_reached,
  dept_performance_category,
  COUNT(*) as total_core,
  SUM(CASE WHEN employee_risk_level IN ('High','Medium') THEN 1 ELSE 0 END) as risk_core,
  ROUND(100.0 * SUM(CASE WHEN employee_risk_level IN ('High','Medium') THEN 1 ELSE 0 END) / COUNT(*), 1) as risk_pct,
  SUM(CASE WHEN retention_stability_score < 60 THEN 1 ELSE 0 END) as low_retention,
  ROUND(100.0 * SUM(CASE WHEN retention_stability_score < 60 THEN 1 ELSE 0 END) / COUNT(*), 1) as low_retention_pct,
  ROUND(AVG(overall_employee_score), 1) as avg_overall,
  ROUND(AVG(career_development_score), 1) as avg_career
FROM core
GROUP BY highest_management_level_reached, dept_performance_category
ORDER BY highest_management_level_reached, dept_performance_category
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-083/attempt-01/sql/S41.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-083/attempt-01/sql/S41.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-083/attempt-01/results/S41.rows.jsonl)；完整：True；SHA256：`d575e6c74fefe4cb32cbb073e20cd416faf83d0544e0a3d7e68834cc4a49b023`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "workday__employee_overview", "kind": "base", "block": null, "base_tables": ["workday__employee_overview"]}] | [] | [] |
| B2 | [{"alias": "ranked", "kind": "derived", "block": "B1", "base_tables": ["workday__employee_overview"]}] | [] | [] |
| B3 | [{"alias": "emp", "kind": "derived", "block": "B2", "base_tables": ["workday__employee_overview"]}] | [] | [] |
| B4 | [{"alias": "core", "kind": "derived", "block": "B3", "base_tables": ["workday__employee_overview"]}] | [] | ["highest_management_level_reached", "dept_performance_category"] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B4 | COUNT(*) | [] | [] | True |
| B4 | SUM(CASE WHEN employee_risk_level IN ('High', 'Medium') THEN 1 ELSE 0 END) | [] | [{"table": "workday__employee_overview", "column": "employee_risk_level"}] | False |
| B4 | SUM(CASE WHEN retention_stability_score < 60 THEN 1 ELSE 0 END) | [] | [{"table": "workday__employee_overview", "column": "retention_stability_score"}] | False |
| B4 | AVG(overall_employee_score) | [{"table": "workday__employee_overview", "column": "overall_employee_score"}] | [] | False |
| B4 | AVG(career_development_score) | [{"table": "workday__employee_overview", "column": "career_development_score"}] | [] | False |
| B4 | COUNT(*) | [] | [] | True |
| B4 | COUNT(*) | [] | [] | True |
| B4 | SUM(CASE WHEN employee_risk_level IN ('High', 'Medium') THEN 1 ELSE 0 END) | [] | [{"table": "workday__employee_overview", "column": "employee_risk_level"}] | False |
| B4 | SUM(CASE WHEN retention_stability_score < 60 THEN 1 ELSE 0 END) | [] | [{"table": "workday__employee_overview", "column": "retention_stability_score"}] | False |


## S42

类别 `data`；来源 `query_db`；调用 `3ea715af747049819cbbbabb84f30667`；状态 `success`。

```sql
WITH ranked AS (
  SELECT *, ROW_NUMBER() OVER (PARTITION BY employee_id ORDER BY position_start_date DESC, overall_employee_score DESC, career_development_score DESC, total_promotions DESC) as rn
  FROM workday__employee_overview
),
emp AS (SELECT * FROM ranked WHERE rn = 1),
core AS (
  SELECT * FROM emp 
  WHERE overall_employee_score > 75 AND career_development_score > 78.57581219355939
)
SELECT 
  organization_sub_type,
  dept_performance_category,
  COUNT(*) as total_core,
  SUM(CASE WHEN employee_risk_level IN ('High','Medium') THEN 1 ELSE 0 END) as risk_core,
  ROUND(100.0 * SUM(CASE WHEN employee_risk_level IN ('High','Medium') THEN 1 ELSE 0 END) / NULLIF(COUNT(*), 0), 1) as risk_pct,
  SUM(CASE WHEN retention_stability_score < 60 THEN 1 ELSE 0 END) as low_retention,
  ROUND(AVG(overall_employee_score), 1) as avg_overall,
  ROUND(AVG(career_development_score), 1) as avg_career
FROM core
GROUP BY organization_sub_type, dept_performance_category
ORDER BY total_core DESC
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-083/attempt-01/sql/S42.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-083/attempt-01/sql/S42.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-083/attempt-01/results/S42.rows.jsonl)；完整：True；SHA256：`e9bbc60947366a3f0c9248c98f73e13d22be4492a6dc00565f21c98a1bf8d9ca`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "workday__employee_overview", "kind": "base", "block": null, "base_tables": ["workday__employee_overview"]}] | [] | [] |
| B2 | [{"alias": "ranked", "kind": "derived", "block": "B1", "base_tables": ["workday__employee_overview"]}] | [] | [] |
| B3 | [{"alias": "emp", "kind": "derived", "block": "B2", "base_tables": ["workday__employee_overview"]}] | [] | [] |
| B4 | [{"alias": "core", "kind": "derived", "block": "B3", "base_tables": ["workday__employee_overview"]}] | [] | ["organization_sub_type", "dept_performance_category"] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B4 | COUNT(*) | [] | [] | True |
| B4 | SUM(CASE WHEN employee_risk_level IN ('High', 'Medium') THEN 1 ELSE 0 END) | [] | [{"table": "workday__employee_overview", "column": "employee_risk_level"}] | False |
| B4 | SUM(CASE WHEN retention_stability_score < 60 THEN 1 ELSE 0 END) | [] | [{"table": "workday__employee_overview", "column": "retention_stability_score"}] | False |
| B4 | AVG(overall_employee_score) | [{"table": "workday__employee_overview", "column": "overall_employee_score"}] | [] | False |
| B4 | AVG(career_development_score) | [{"table": "workday__employee_overview", "column": "career_development_score"}] | [] | False |
| B4 | SUM(CASE WHEN employee_risk_level IN ('High', 'Medium') THEN 1 ELSE 0 END) | [] | [{"table": "workday__employee_overview", "column": "employee_risk_level"}] | False |
| B4 | COUNT(*) | [] | [] | True |


## S43

类别 `data`；来源 `query_db`；调用 `53dde45b5e2344d793de39950b072596`；状态 `success`。

```sql
WITH ranked AS (
  SELECT *, ROW_NUMBER() OVER (PARTITION BY employee_id ORDER BY position_start_date DESC, overall_employee_score DESC, career_development_score DESC, total_promotions DESC) as rn
  FROM workday__employee_overview
),
emp AS (SELECT * FROM ranked WHERE rn = 1),
core AS (
  SELECT * FROM emp 
  WHERE overall_employee_score > 75 AND career_development_score > 78.57581219355939
)
SELECT 
  CASE WHEN age < 45 THEN '<45' WHEN age BETWEEN 45 AND 50 THEN '45-50' WHEN age BETWEEN 51 AND 55 THEN '51-55' WHEN age BETWEEN 56 AND 60 THEN '56-60' ELSE '60+' END as age_band,
  COUNT(*) as cnt,
  ROUND(100.0 * COUNT(*) / (SELECT COUNT(*) FROM core), 1) as pct
FROM core
GROUP BY age_band
ORDER BY MIN(age)
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-083/attempt-01/sql/S43.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-083/attempt-01/sql/S43.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-083/attempt-01/results/S43.rows.jsonl)；完整：True；SHA256：`ce31d0e03fcb50f57a8465c5ae1d855115c6cad50e1a001de93a5385bc27c698`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "workday__employee_overview", "kind": "base", "block": null, "base_tables": ["workday__employee_overview"]}] | [] | [] |
| B2 | [{"alias": "ranked", "kind": "derived", "block": "B1", "base_tables": ["workday__employee_overview"]}] | [] | [] |
| B3 | [{"alias": "emp", "kind": "derived", "block": "B2", "base_tables": ["workday__employee_overview"]}] | [] | [] |
| B4 | [{"alias": "core", "kind": "derived", "block": "B3", "base_tables": ["workday__employee_overview"]}] | [] | [] |
| B5 | [{"alias": "core", "kind": "derived", "block": "B3", "base_tables": ["workday__employee_overview"]}] | [] | ["CASE WHEN age < 45 THEN '<45' WHEN age BETWEEN 45 AND 50 THEN '45-50' WHEN age BETWEEN 51 AND 55 THEN '51-55' WHEN age BETWEEN 56 AND 60 THEN '56-60' ELSE '60+' END"] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B4 | COUNT(*) | [] | [] | True |
| B5 | COUNT(*) | [] | [] | True |
| B5 | MIN(age) | [{"table": "workday__employee_overview", "column": "age"}] | [] | False |
| B5 | COUNT(*) | [] | [] | True |


## S44

类别 `data`；来源 `query_db`；调用 `e9d587359c8a4d59b544f683d3c023bc`；状态 `success`。

```sql
WITH ranked AS (
  SELECT *, ROW_NUMBER() OVER (PARTITION BY employee_id ORDER BY position_start_date DESC, overall_employee_score DESC, career_development_score DESC, total_promotions DESC) as rn
  FROM workday__employee_overview
),
emp AS (SELECT * FROM ranked WHERE rn = 1),
core AS (
  SELECT * FROM emp 
  WHERE overall_employee_score > 75 AND career_development_score > 78.57581219355939
)
SELECT employee_id, age, tenure_years, marital_status, ethnicity_codes, total_positions_held, total_promotions, lateral_moves, management_positions_held, career_phase, employee_maturity_segment, compensation_tier, work_conditions_score, dept_turnover_rate, dept_health_score, organization_type, organization_sub_type, retention_stability_score, overall_employee_score, career_development_score
FROM core
WHERE employee_risk_level = 'High'
ORDER BY retention_stability_score
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-083/attempt-01/sql/S44.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-083/attempt-01/sql/S44.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-083/attempt-01/results/S44.rows.jsonl)；完整：True；SHA256：`a2ff8063a0b6c079c763d68a90f779bb840663a1ed59b4c5c8c60da19f6fa45f`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "workday__employee_overview", "kind": "base", "block": null, "base_tables": ["workday__employee_overview"]}] | [] | [] |
| B2 | [{"alias": "ranked", "kind": "derived", "block": "B1", "base_tables": ["workday__employee_overview"]}] | [] | [] |
| B3 | [{"alias": "emp", "kind": "derived", "block": "B2", "base_tables": ["workday__employee_overview"]}] | [] | [] |
| B4 | [{"alias": "core", "kind": "derived", "block": "B3", "base_tables": ["workday__employee_overview"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |


## S45

类别 `data`；来源 `query_db`；调用 `8b3c47da66414babba9a85e28ac1bc44`；状态 `success`。

```sql
WITH ranked AS (
  SELECT *, ROW_NUMBER() OVER (PARTITION BY employee_id ORDER BY position_start_date DESC, overall_employee_score DESC, career_development_score DESC, total_promotions DESC) as rn
  FROM workday__employee_overview
),
emp AS (SELECT * FROM ranked WHERE rn = 1),
core AS (
  SELECT * FROM emp 
  WHERE overall_employee_score > 75 AND career_development_score > 78.57581219355939
)
SELECT 
  tenure_group,
  COUNT(*) as cnt,
  ROUND(100.0 * COUNT(*) / (SELECT COUNT(*) FROM core), 1) as pct
FROM core
GROUP BY tenure_group
ORDER BY cnt DESC
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-083/attempt-01/sql/S45.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-083/attempt-01/sql/S45.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-083/attempt-01/results/S45.rows.jsonl)；完整：True；SHA256：`a748d744857438d412ba9ecfd5c069604c884e386ab9536dad0bc983bb31563e`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "workday__employee_overview", "kind": "base", "block": null, "base_tables": ["workday__employee_overview"]}] | [] | [] |
| B2 | [{"alias": "ranked", "kind": "derived", "block": "B1", "base_tables": ["workday__employee_overview"]}] | [] | [] |
| B3 | [{"alias": "emp", "kind": "derived", "block": "B2", "base_tables": ["workday__employee_overview"]}] | [] | [] |
| B4 | [{"alias": "core", "kind": "derived", "block": "B3", "base_tables": ["workday__employee_overview"]}] | [] | [] |
| B5 | [{"alias": "core", "kind": "derived", "block": "B3", "base_tables": ["workday__employee_overview"]}] | [] | ["tenure_group"] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B4 | COUNT(*) | [] | [] | True |
| B5 | COUNT(*) | [] | [] | True |
| B5 | COUNT(*) | [] | [] | True |


## S46

类别 `data`；来源 `query_db`；调用 `d52eab066e25422d9fd02eb4a0a632f8`；状态 `success`。

```sql
WITH ranked AS (
  SELECT *, ROW_NUMBER() OVER (PARTITION BY employee_id ORDER BY position_start_date DESC, overall_employee_score DESC, career_development_score DESC, total_promotions DESC) as rn
  FROM workday__employee_overview
),
emp AS (SELECT * FROM ranked WHERE rn = 1),
core AS (
  SELECT * FROM emp 
  WHERE overall_employee_score > 75 AND career_development_score > 78.57581219355939
)
SELECT 
  career_phase,
  COUNT(*) as cnt,
  ROUND(100.0 * COUNT(*) / (SELECT COUNT(*) FROM core), 1) as pct
FROM core
GROUP BY career_phase
ORDER BY cnt DESC
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-083/attempt-01/sql/S46.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-083/attempt-01/sql/S46.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-083/attempt-01/results/S46.rows.jsonl)；完整：True；SHA256：`d4f0d1a2d5eef37d7155abafa51b805ab05940c59744c9fd49bcd1debe60fe69`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "workday__employee_overview", "kind": "base", "block": null, "base_tables": ["workday__employee_overview"]}] | [] | [] |
| B2 | [{"alias": "ranked", "kind": "derived", "block": "B1", "base_tables": ["workday__employee_overview"]}] | [] | [] |
| B3 | [{"alias": "emp", "kind": "derived", "block": "B2", "base_tables": ["workday__employee_overview"]}] | [] | [] |
| B4 | [{"alias": "core", "kind": "derived", "block": "B3", "base_tables": ["workday__employee_overview"]}] | [] | [] |
| B5 | [{"alias": "core", "kind": "derived", "block": "B3", "base_tables": ["workday__employee_overview"]}] | [] | ["career_phase"] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B4 | COUNT(*) | [] | [] | True |
| B5 | COUNT(*) | [] | [] | True |
| B5 | COUNT(*) | [] | [] | True |


## S47

类别 `data`；来源 `query_db`；调用 `6361cf7459594a3ab95a0d065e2122f3`；状态 `success`。

```sql
WITH ranked AS (
  SELECT *, ROW_NUMBER() OVER (PARTITION BY employee_id ORDER BY position_start_date DESC, overall_employee_score DESC, career_development_score DESC, total_promotions DESC) as rn
  FROM workday__employee_overview
),
emp AS (SELECT * FROM ranked WHERE rn = 1),
core AS (
  SELECT * FROM emp 
  WHERE overall_employee_score > 75 AND career_development_score > 78.57581219355939
)
SELECT 
  employee_maturity_segment,
  COUNT(*) as cnt,
  ROUND(100.0 * COUNT(*) / (SELECT COUNT(*) FROM core), 1) as pct
FROM core
GROUP BY employee_maturity_segment
ORDER BY cnt DESC
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-083/attempt-01/sql/S47.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-083/attempt-01/sql/S47.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-083/attempt-01/results/S47.rows.jsonl)；完整：True；SHA256：`d24e3dabdadd8cce2f9abb9ca167172e3b66fb02a0bb7f5780d87b2c3952c894`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "workday__employee_overview", "kind": "base", "block": null, "base_tables": ["workday__employee_overview"]}] | [] | [] |
| B2 | [{"alias": "ranked", "kind": "derived", "block": "B1", "base_tables": ["workday__employee_overview"]}] | [] | [] |
| B3 | [{"alias": "emp", "kind": "derived", "block": "B2", "base_tables": ["workday__employee_overview"]}] | [] | [] |
| B4 | [{"alias": "core", "kind": "derived", "block": "B3", "base_tables": ["workday__employee_overview"]}] | [] | [] |
| B5 | [{"alias": "core", "kind": "derived", "block": "B3", "base_tables": ["workday__employee_overview"]}] | [] | ["employee_maturity_segment"] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B4 | COUNT(*) | [] | [] | True |
| B5 | COUNT(*) | [] | [] | True |
| B5 | COUNT(*) | [] | [] | True |


## S48

类别 `data`；来源 `query_db`；调用 `e9f1eb8f41bd4f668385c49c40810a2e`；状态 `success`。

```sql
WITH ranked AS (
  SELECT *, ROW_NUMBER() OVER (PARTITION BY employee_id ORDER BY position_start_date DESC, overall_employee_score DESC, career_development_score DESC, total_promotions DESC) as rn
  FROM workday__employee_overview
),
emp AS (SELECT * FROM ranked WHERE rn = 1)
SELECT 
  'All Employees' as grp,
  COUNT(*) as n,
  ROUND(AVG(age), 1) as avg_age,
  ROUND(AVG(tenure_years), 2) as avg_tenure,
  ROUND(AVG(overall_employee_score), 1) as avg_overall,
  ROUND(AVG(career_development_score), 1) as avg_career,
  ROUND(AVG(retention_stability_score), 1) as avg_retention,
  ROUND(AVG(total_positions_held), 2) as avg_positions,
  ROUND(AVG(total_promotions), 2) as avg_promotions,
  ROUND(AVG(lateral_moves), 2) as avg_lateral,
  ROUND(AVG(management_positions_held), 2) as avg_mgmt
FROM emp
UNION ALL
SELECT 
  'Core Employees',
  COUNT(*),
  ROUND(AVG(age), 1),
  ROUND(AVG(tenure_years), 2),
  ROUND(AVG(overall_employee_score), 1),
  ROUND(AVG(career_development_score), 1),
  ROUND(AVG(retention_stability_score), 1),
  ROUND(AVG(total_positions_held), 2),
  ROUND(AVG(total_promotions), 2),
  ROUND(AVG(lateral_moves), 2),
  ROUND(AVG(management_positions_held), 2)
FROM emp
WHERE overall_employee_score > 75 AND career_development_score > 78.57581219355939
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-083/attempt-01/sql/S48.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-083/attempt-01/sql/S48.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-083/attempt-01/results/S48.rows.jsonl)；完整：True；SHA256：`4045c76e0f6474db5298b275c1b2f84d6833c49b4db23952934ef04f7c038412`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "workday__employee_overview", "kind": "base", "block": null, "base_tables": ["workday__employee_overview"]}] | [] | [] |
| B2 | [{"alias": "ranked", "kind": "derived", "block": "B1", "base_tables": ["workday__employee_overview"]}] | [] | [] |
| B3 | [{"alias": "emp", "kind": "derived", "block": "B2", "base_tables": ["workday__employee_overview"]}] | [] | [] |
| B4 | [{"alias": "emp", "kind": "derived", "block": "B2", "base_tables": ["workday__employee_overview"]}] | [] | [] |
| B5 | [] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B3 | COUNT(*) | [] | [] | True |
| B3 | AVG(age) | [{"table": "workday__employee_overview", "column": "age"}] | [] | False |
| B3 | AVG(tenure_years) | [{"table": "workday__employee_overview", "column": "tenure_years"}] | [] | False |
| B3 | AVG(overall_employee_score) | [{"table": "workday__employee_overview", "column": "overall_employee_score"}] | [] | False |
| B3 | AVG(career_development_score) | [{"table": "workday__employee_overview", "column": "career_development_score"}] | [] | False |
| B3 | AVG(retention_stability_score) | [{"table": "workday__employee_overview", "column": "retention_stability_score"}] | [] | False |
| B3 | AVG(total_positions_held) | [{"table": "workday__employee_overview", "column": "total_positions_held"}] | [] | False |
| B3 | AVG(total_promotions) | [{"table": "workday__employee_overview", "column": "total_promotions"}] | [] | False |
| B3 | AVG(lateral_moves) | [{"table": "workday__employee_overview", "column": "lateral_moves"}] | [] | False |
| B3 | AVG(management_positions_held) | [{"table": "workday__employee_overview", "column": "management_positions_held"}] | [] | False |
| B4 | COUNT(*) | [] | [] | True |
| B4 | AVG(age) | [{"table": "workday__employee_overview", "column": "age"}] | [] | False |
| B4 | AVG(tenure_years) | [{"table": "workday__employee_overview", "column": "tenure_years"}] | [] | False |
| B4 | AVG(overall_employee_score) | [{"table": "workday__employee_overview", "column": "overall_employee_score"}] | [] | False |
| B4 | AVG(career_development_score) | [{"table": "workday__employee_overview", "column": "career_development_score"}] | [] | False |
| B4 | AVG(retention_stability_score) | [{"table": "workday__employee_overview", "column": "retention_stability_score"}] | [] | False |
| B4 | AVG(total_positions_held) | [{"table": "workday__employee_overview", "column": "total_positions_held"}] | [] | False |
| B4 | AVG(total_promotions) | [{"table": "workday__employee_overview", "column": "total_promotions"}] | [] | False |
| B4 | AVG(lateral_moves) | [{"table": "workday__employee_overview", "column": "lateral_moves"}] | [] | False |
| B4 | AVG(management_positions_held) | [{"table": "workday__employee_overview", "column": "management_positions_held"}] | [] | False |


## S49

类别 `data`；来源 `query_db`；调用 `3a6cf485583b438c800b4b9973c03501`；状态 `success`。

```sql
WITH ranked AS (
  SELECT *, ROW_NUMBER() OVER (PARTITION BY employee_id ORDER BY position_start_date DESC, overall_employee_score DESC, career_development_score DESC, total_promotions DESC) as rn
  FROM workday__employee_overview
),
emp AS (SELECT * FROM ranked WHERE rn = 1)
SELECT 
  'All Employees' as grp,
  ROUND(100.0 * SUM(CASE WHEN employee_risk_level = 'High' THEN 1 ELSE 0 END) / COUNT(*), 1) as high_risk_pct,
  ROUND(100.0 * SUM(CASE WHEN employee_risk_level = 'Medium' THEN 1 ELSE 0 END) / COUNT(*), 1) as med_risk_pct,
  ROUND(100.0 * SUM(CASE WHEN employee_risk_level = 'Low' THEN 1 ELSE 0 END) / COUNT(*), 1) as low_risk_pct,
  SUM(CASE WHEN retention_stability_score < 60 AND overall_employee_score > 80 THEN 1 ELSE 0 END) as high_value_attrition_risk
FROM emp
UNION ALL
SELECT 
  'Core Employees',
  ROUND(100.0 * SUM(CASE WHEN employee_risk_level = 'High' THEN 1 ELSE 0 END) / COUNT(*), 1),
  ROUND(100.0 * SUM(CASE WHEN employee_risk_level = 'Medium' THEN 1 ELSE 0 END) / COUNT(*), 1),
  ROUND(100.0 * SUM(CASE WHEN employee_risk_level = 'Low' THEN 1 ELSE 0 END) / COUNT(*), 1),
  SUM(CASE WHEN retention_stability_score < 60 AND overall_employee_score > 80 THEN 1 ELSE 0 END)
FROM emp
WHERE overall_employee_score > 75 AND career_development_score > 78.57581219355939
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-083/attempt-01/sql/S49.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-083/attempt-01/sql/S49.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-083/attempt-01/results/S49.rows.jsonl)；完整：True；SHA256：`6beaf3969f88e2ba48f343a03c4978df66b64d9b5281ff16c39dd3ab78f0c6c5`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "workday__employee_overview", "kind": "base", "block": null, "base_tables": ["workday__employee_overview"]}] | [] | [] |
| B2 | [{"alias": "ranked", "kind": "derived", "block": "B1", "base_tables": ["workday__employee_overview"]}] | [] | [] |
| B3 | [{"alias": "emp", "kind": "derived", "block": "B2", "base_tables": ["workday__employee_overview"]}] | [] | [] |
| B4 | [{"alias": "emp", "kind": "derived", "block": "B2", "base_tables": ["workday__employee_overview"]}] | [] | [] |
| B5 | [] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B3 | SUM(CASE WHEN retention_stability_score < 60 AND overall_employee_score > 80 THEN 1 ELSE 0 END) | [] | [{"table": "workday__employee_overview", "column": "retention_stability_score"}, {"table": "workday__employee_overview", "column": "overall_employee_score"}] | False |
| B3 | COUNT(*) | [] | [] | True |
| B3 | COUNT(*) | [] | [] | True |
| B3 | COUNT(*) | [] | [] | True |
| B3 | SUM(CASE WHEN employee_risk_level = 'High' THEN 1 ELSE 0 END) | [] | [{"table": "workday__employee_overview", "column": "employee_risk_level"}] | False |
| B3 | SUM(CASE WHEN employee_risk_level = 'Medium' THEN 1 ELSE 0 END) | [] | [{"table": "workday__employee_overview", "column": "employee_risk_level"}] | False |
| B3 | SUM(CASE WHEN employee_risk_level = 'Low' THEN 1 ELSE 0 END) | [] | [{"table": "workday__employee_overview", "column": "employee_risk_level"}] | False |
| B4 | SUM(CASE WHEN retention_stability_score < 60 AND overall_employee_score > 80 THEN 1 ELSE 0 END) | [] | [{"table": "workday__employee_overview", "column": "retention_stability_score"}, {"table": "workday__employee_overview", "column": "overall_employee_score"}] | False |
| B4 | COUNT(*) | [] | [] | True |
| B4 | COUNT(*) | [] | [] | True |
| B4 | COUNT(*) | [] | [] | True |
| B4 | SUM(CASE WHEN employee_risk_level = 'High' THEN 1 ELSE 0 END) | [] | [{"table": "workday__employee_overview", "column": "employee_risk_level"}] | False |
| B4 | SUM(CASE WHEN employee_risk_level = 'Medium' THEN 1 ELSE 0 END) | [] | [{"table": "workday__employee_overview", "column": "employee_risk_level"}] | False |
| B4 | SUM(CASE WHEN employee_risk_level = 'Low' THEN 1 ELSE 0 END) | [] | [{"table": "workday__employee_overview", "column": "employee_risk_level"}] | False |


## S50

类别 `data`；来源 `python`；调用 `5ccaa9b01ecd48a6881b0366e8baeb1c`；状态 `success`。

```sql

WITH ranked AS (
  SELECT *, ROW_NUMBER() OVER (PARTITION BY employee_id ORDER BY position_start_date DESC, overall_employee_score DESC, career_development_score DESC, total_promotions DESC) as rn
  FROM workday__employee_overview
),
emp AS (SELECT * FROM ranked WHERE rn = 1),
core AS (
  SELECT * FROM emp 
  WHERE overall_employee_score > 75 AND career_development_score > 78.57581219355939
)
SELECT age, tenure_years, total_positions_held, total_promotions, lateral_moves, management_positions_held, 
       overall_employee_score, career_development_score, retention_stability_score,
       marital_status, ethnicity_codes, career_phase, employee_maturity_segment,
       employee_risk_level, compensation_tier, work_conditions_score, dept_turnover_rate,
       dept_health_score, dept_management_ratio, organization_type, organization_sub_type,
       dept_performance_category, highest_management_level_reached,
       is_work_shift_required, is_union_eligible, employee_value_segment
FROM core

```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-083/attempt-01/sql/S50.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-083/attempt-01/sql/S50.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-083/attempt-01/results/S50.rows.jsonl)；完整：True；SHA256：`25848ac13a0ea569c52ba5fd9d938d665298b6263b83d0f02de70456b213b8f5`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "workday__employee_overview", "kind": "base", "block": null, "base_tables": ["workday__employee_overview"]}] | [] | [] |
| B2 | [{"alias": "ranked", "kind": "derived", "block": "B1", "base_tables": ["workday__employee_overview"]}] | [] | [] |
| B3 | [{"alias": "emp", "kind": "derived", "block": "B2", "base_tables": ["workday__employee_overview"]}] | [] | [] |
| B4 | [{"alias": "core", "kind": "derived", "block": "B3", "base_tables": ["workday__employee_overview"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |


## S51

类别 `data`；来源 `python`；调用 `5ccaa9b01ecd48a6881b0366e8baeb1c`；状态 `success`。

```sql

WITH ranked AS (
  SELECT *, ROW_NUMBER() OVER (PARTITION BY employee_id ORDER BY position_start_date DESC, overall_employee_score DESC, career_development_score DESC, total_promotions DESC) as rn
  FROM workday__employee_overview
),
emp AS (SELECT * FROM ranked WHERE rn = 1)
SELECT age, tenure_years, overall_employee_score, career_development_score, retention_stability_score,
       employee_risk_level, total_positions_held, total_promotions, lateral_moves, management_positions_held
FROM emp

```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-083/attempt-01/sql/S51.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-083/attempt-01/sql/S51.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-083/attempt-01/results/S51.rows.jsonl)；完整：True；SHA256：`8389c6d486444b59340fabc97637d7b0c8a970d2ee3debe535fc13cb5e0129b2`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "workday__employee_overview", "kind": "base", "block": null, "base_tables": ["workday__employee_overview"]}] | [] | [] |
| B2 | [{"alias": "ranked", "kind": "derived", "block": "B1", "base_tables": ["workday__employee_overview"]}] | [] | [] |
| B3 | [{"alias": "emp", "kind": "derived", "block": "B2", "base_tables": ["workday__employee_overview"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |


## S52

类别 `data`；来源 `python`；调用 `5ccaa9b01ecd48a6881b0366e8baeb1c`；状态 `success`。

```sql

WITH ranked AS (
  SELECT *, ROW_NUMBER() OVER (PARTITION BY employee_id ORDER BY position_start_date DESC, overall_employee_score DESC, career_development_score DESC, total_promotions DESC) as rn
  FROM workday__employee_overview
),
emp AS (SELECT * FROM ranked WHERE rn = 1),
core AS (
  SELECT * FROM emp 
  WHERE overall_employee_score > 75 AND career_development_score > 78.57581219355939
)
SELECT career_phase, employee_maturity_segment, 
       COUNT(*) as total,
       SUM(CASE WHEN employee_risk_level = 'High' THEN 1 ELSE 0 END) as high_risk,
       SUM(CASE WHEN employee_risk_level = 'Medium' THEN 1 ELSE 0 END) as med_risk,
       SUM(CASE WHEN employee_risk_level = 'Low' THEN 1 ELSE 0 END) as low_risk
FROM core
GROUP BY career_phase, employee_maturity_segment
ORDER BY career_phase, employee_maturity_segment

```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-083/attempt-01/sql/S52.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-083/attempt-01/sql/S52.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-083/attempt-01/results/S52.rows.jsonl)；完整：True；SHA256：`0187e9e8b74fad434a35e2bc1d30faea292f3ffe1f4d37859a060f61c6f44856`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "workday__employee_overview", "kind": "base", "block": null, "base_tables": ["workday__employee_overview"]}] | [] | [] |
| B2 | [{"alias": "ranked", "kind": "derived", "block": "B1", "base_tables": ["workday__employee_overview"]}] | [] | [] |
| B3 | [{"alias": "emp", "kind": "derived", "block": "B2", "base_tables": ["workday__employee_overview"]}] | [] | [] |
| B4 | [{"alias": "core", "kind": "derived", "block": "B3", "base_tables": ["workday__employee_overview"]}] | [] | ["career_phase", "employee_maturity_segment"] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B4 | COUNT(*) | [] | [] | True |
| B4 | SUM(CASE WHEN employee_risk_level = 'High' THEN 1 ELSE 0 END) | [] | [{"table": "workday__employee_overview", "column": "employee_risk_level"}] | False |
| B4 | SUM(CASE WHEN employee_risk_level = 'Medium' THEN 1 ELSE 0 END) | [] | [{"table": "workday__employee_overview", "column": "employee_risk_level"}] | False |
| B4 | SUM(CASE WHEN employee_risk_level = 'Low' THEN 1 ELSE 0 END) | [] | [{"table": "workday__employee_overview", "column": "employee_risk_level"}] | False |


## S53

类别 `data`；来源 `python`；调用 `5ccaa9b01ecd48a6881b0366e8baeb1c`；状态 `success`。

```sql

WITH ranked AS (
  SELECT *, ROW_NUMBER() OVER (PARTITION BY employee_id ORDER BY position_start_date DESC, overall_employee_score DESC, career_development_score DESC, total_promotions DESC) as rn
  FROM workday__employee_overview
),
emp AS (SELECT * FROM ranked WHERE rn = 1)
SELECT employee_value_segment, COUNT(*) as cnt
FROM emp
WHERE retention_stability_score < 60 AND overall_employee_score > 80
GROUP BY employee_value_segment
ORDER BY cnt DESC

```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-083/attempt-01/sql/S53.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-083/attempt-01/sql/S53.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-083/attempt-01/results/S53.rows.jsonl)；完整：True；SHA256：`493f22a82ce379a5e5f715cabc9ec7e31c3f6bab470be1898d9c6f79ee1f6301`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "workday__employee_overview", "kind": "base", "block": null, "base_tables": ["workday__employee_overview"]}] | [] | [] |
| B2 | [{"alias": "ranked", "kind": "derived", "block": "B1", "base_tables": ["workday__employee_overview"]}] | [] | [] |
| B3 | [{"alias": "emp", "kind": "derived", "block": "B2", "base_tables": ["workday__employee_overview"]}] | [] | ["employee_value_segment"] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B3 | COUNT(*) | [] | [] | True |


## S54

类别 `data`；来源 `python`；调用 `5ccaa9b01ecd48a6881b0366e8baeb1c`；状态 `success`。

```sql

WITH ranked AS (
  SELECT *, ROW_NUMBER() OVER (PARTITION BY employee_id ORDER BY position_start_date DESC, overall_employee_score DESC, career_development_score DESC, total_promotions DESC) as rn
  FROM workday__employee_overview
),
emp AS (SELECT * FROM ranked WHERE rn = 1),
core AS (
  SELECT * FROM emp 
  WHERE overall_employee_score > 75 AND career_development_score > 78.57581219355939
)
SELECT employee_risk_level, 
       AVG(work_conditions_score) as avg_work_cond,
       AVG(dept_turnover_rate) as avg_turnover,
       AVG(dept_health_score) as avg_dept_health
FROM core
GROUP BY employee_risk_level
ORDER BY employee_risk_level

```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-083/attempt-01/sql/S54.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-083/attempt-01/sql/S54.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-083/attempt-01/results/S54.rows.jsonl)；完整：True；SHA256：`bff7a521b559fbd7a4659e8d83940de3165b2ea3ee55162ba7c41ee02a333967`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "workday__employee_overview", "kind": "base", "block": null, "base_tables": ["workday__employee_overview"]}] | [] | [] |
| B2 | [{"alias": "ranked", "kind": "derived", "block": "B1", "base_tables": ["workday__employee_overview"]}] | [] | [] |
| B3 | [{"alias": "emp", "kind": "derived", "block": "B2", "base_tables": ["workday__employee_overview"]}] | [] | [] |
| B4 | [{"alias": "core", "kind": "derived", "block": "B3", "base_tables": ["workday__employee_overview"]}] | [] | ["employee_risk_level"] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B4 | AVG(work_conditions_score) | [{"table": "workday__employee_overview", "column": "work_conditions_score"}] | [] | False |
| B4 | AVG(dept_turnover_rate) | [{"table": "workday__employee_overview", "column": "dept_turnover_rate"}] | [] | False |
| B4 | AVG(dept_health_score) | [{"table": "workday__employee_overview", "column": "dept_health_score"}] | [] | False |


## S55

类别 `data`；来源 `python`；调用 `5ccaa9b01ecd48a6881b0366e8baeb1c`；状态 `success`。

```sql

WITH ranked AS (
  SELECT *, ROW_NUMBER() OVER (PARTITION BY employee_id ORDER BY position_start_date DESC, overall_employee_score DESC, career_development_score DESC, total_promotions DESC) as rn
  FROM workday__employee_overview
),
emp AS (SELECT * FROM ranked WHERE rn = 1),
core AS (
  SELECT * FROM emp 
  WHERE overall_employee_score > 75 AND career_development_score > 78.57581219355939
)
SELECT compensation_tier, COUNT(*) as cnt
FROM core
GROUP BY compensation_tier
ORDER BY cnt DESC

```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-083/attempt-01/sql/S55.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-083/attempt-01/sql/S55.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-083/attempt-01/results/S55.rows.jsonl)；完整：True；SHA256：`491d5c3738f378a33993cd558d4915aa8e98278eb433f12fe9a59f01570844cf`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "workday__employee_overview", "kind": "base", "block": null, "base_tables": ["workday__employee_overview"]}] | [] | [] |
| B2 | [{"alias": "ranked", "kind": "derived", "block": "B1", "base_tables": ["workday__employee_overview"]}] | [] | [] |
| B3 | [{"alias": "emp", "kind": "derived", "block": "B2", "base_tables": ["workday__employee_overview"]}] | [] | [] |
| B4 | [{"alias": "core", "kind": "derived", "block": "B3", "base_tables": ["workday__employee_overview"]}] | [] | ["compensation_tier"] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B4 | COUNT(*) | [] | [] | True |


## S56

类别 `data`；来源 `python`；调用 `5ccaa9b01ecd48a6881b0366e8baeb1c`；状态 `success`。

```sql

WITH ranked AS (
  SELECT *, ROW_NUMBER() OVER (PARTITION BY employee_id ORDER BY position_start_date DESC, overall_employee_score DESC, career_development_score DESC, total_promotions DESC) as rn
  FROM workday__employee_overview
),
emp AS (SELECT * FROM ranked WHERE rn = 1),
core AS (
  SELECT * FROM emp 
  WHERE overall_employee_score > 75 AND career_development_score > 78.57581219355939
)
SELECT highest_management_level_reached, dept_performance_category, 
       COUNT(*) as total,
       SUM(CASE WHEN employee_risk_level IN ('High','Medium') THEN 1 ELSE 0 END) as at_risk,
       SUM(CASE WHEN retention_stability_score < 60 THEN 1 ELSE 0 END) as low_retention
FROM core
GROUP BY highest_management_level_reached, dept_performance_category
ORDER BY highest_management_level_reached, dept_performance_category

```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-083/attempt-01/sql/S56.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-083/attempt-01/sql/S56.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-083/attempt-01/results/S56.rows.jsonl)；完整：True；SHA256：`2ab3aa4984fe856a83e130ffbad534c999e0149d7bdb9eeef8c11dcd5f96d7ef`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "workday__employee_overview", "kind": "base", "block": null, "base_tables": ["workday__employee_overview"]}] | [] | [] |
| B2 | [{"alias": "ranked", "kind": "derived", "block": "B1", "base_tables": ["workday__employee_overview"]}] | [] | [] |
| B3 | [{"alias": "emp", "kind": "derived", "block": "B2", "base_tables": ["workday__employee_overview"]}] | [] | [] |
| B4 | [{"alias": "core", "kind": "derived", "block": "B3", "base_tables": ["workday__employee_overview"]}] | [] | ["highest_management_level_reached", "dept_performance_category"] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B4 | COUNT(*) | [] | [] | True |
| B4 | SUM(CASE WHEN employee_risk_level IN ('High', 'Medium') THEN 1 ELSE 0 END) | [] | [{"table": "workday__employee_overview", "column": "employee_risk_level"}] | False |
| B4 | SUM(CASE WHEN retention_stability_score < 60 THEN 1 ELSE 0 END) | [] | [{"table": "workday__employee_overview", "column": "retention_stability_score"}] | False |


## S57

类别 `data`；来源 `query_db`；调用 `c619a3a2dbd946ce80e776a51ba1249a`；状态 `success`。

```sql
WITH ranked AS (
  SELECT *, ROW_NUMBER() OVER (PARTITION BY employee_id ORDER BY position_start_date DESC, overall_employee_score DESC, career_development_score DESC, total_promotions DESC) as rn
  FROM workday__employee_overview
),
emp AS (SELECT * FROM ranked WHERE rn = 1),
core AS (
  SELECT * FROM emp 
  WHERE overall_employee_score > 75 AND career_development_score > 78.57581219355939
)
SELECT 
  organization_type,
  organization_sub_type,
  COUNT(*) as total_core,
  ROUND(100.0 * SUM(CASE WHEN employee_risk_level IN ('High','Medium') THEN 1 ELSE 0 END) / COUNT(*), 1) as risk_pct,
  ROUND(AVG(highest_management_level_reached), 2) as avg_mgmt_level,
  ROUND(AVG(retention_stability_score), 1) as avg_retention,
  ROUND(AVG(overall_employee_score), 1) as avg_overall
FROM core
GROUP BY organization_type, organization_sub_type
HAVING COUNT(*) >= 20
ORDER BY risk_pct DESC
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-083/attempt-01/sql/S57.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-083/attempt-01/sql/S57.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-083/attempt-01/results/S57.rows.jsonl)；完整：True；SHA256：`4fe588b45381d3e316cf463f31d54b88a5335d8036b72d97976eac973131af97`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "workday__employee_overview", "kind": "base", "block": null, "base_tables": ["workday__employee_overview"]}] | [] | [] |
| B2 | [{"alias": "ranked", "kind": "derived", "block": "B1", "base_tables": ["workday__employee_overview"]}] | [] | [] |
| B3 | [{"alias": "emp", "kind": "derived", "block": "B2", "base_tables": ["workday__employee_overview"]}] | [] | [] |
| B4 | [{"alias": "core", "kind": "derived", "block": "B3", "base_tables": ["workday__employee_overview"]}] | [] | ["organization_type", "organization_sub_type"] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B4 | COUNT(*) | [] | [] | True |
| B4 | AVG(highest_management_level_reached) | [{"table": "workday__employee_overview", "column": "highest_management_level_reached"}] | [] | False |
| B4 | AVG(retention_stability_score) | [{"table": "workday__employee_overview", "column": "retention_stability_score"}] | [] | False |
| B4 | AVG(overall_employee_score) | [{"table": "workday__employee_overview", "column": "overall_employee_score"}] | [] | False |
| B4 | COUNT(*) | [] | [] | True |
| B4 | COUNT(*) | [] | [] | True |
| B4 | SUM(CASE WHEN employee_risk_level IN ('High', 'Medium') THEN 1 ELSE 0 END) | [] | [{"table": "workday__employee_overview", "column": "employee_risk_level"}] | False |


## S58

类别 `data`；来源 `query_db`；调用 `a84aadce1d1a4ecbb1305e5c44aab9f5`；状态 `success`。

```sql
WITH ranked AS (
  SELECT *, ROW_NUMBER() OVER (PARTITION BY employee_id ORDER BY position_start_date DESC, overall_employee_score DESC, career_development_score DESC, total_promotions DESC) as rn
  FROM workday__employee_overview
),
emp AS (SELECT * FROM ranked WHERE rn = 1)
SELECT 
  ethnicity_codes,
  COUNT(*) as total,
  SUM(CASE WHEN overall_employee_score > 75 AND career_development_score > 78.57581219355939 THEN 1 ELSE 0 END) as core,
  ROUND(100.0 * SUM(CASE WHEN overall_employee_score > 75 AND career_development_score > 78.57581219355939 THEN 1 ELSE 0 END) / COUNT(*), 1) as core_rate_pct
FROM emp
GROUP BY ethnicity_codes
ORDER BY core_rate_pct DESC
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-083/attempt-01/sql/S58.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-083/attempt-01/sql/S58.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-083/attempt-01/results/S58.rows.jsonl)；完整：True；SHA256：`492824e7b9b809792226bd16979043c16cccd4d542ba2244c9f042b158f6ba49`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "workday__employee_overview", "kind": "base", "block": null, "base_tables": ["workday__employee_overview"]}] | [] | [] |
| B2 | [{"alias": "ranked", "kind": "derived", "block": "B1", "base_tables": ["workday__employee_overview"]}] | [] | [] |
| B3 | [{"alias": "emp", "kind": "derived", "block": "B2", "base_tables": ["workday__employee_overview"]}] | [] | ["ethnicity_codes"] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B3 | COUNT(*) | [] | [] | True |
| B3 | SUM(CASE WHEN overall_employee_score > 75 AND career_development_score > 78.57581219355939 THEN 1 ELSE 0 END) | [] | [{"table": "workday__employee_overview", "column": "overall_employee_score"}, {"table": "workday__employee_overview", "column": "career_development_score"}] | False |
| B3 | COUNT(*) | [] | [] | True |
| B3 | SUM(CASE WHEN overall_employee_score > 75 AND career_development_score > 78.57581219355939 THEN 1 ELSE 0 END) | [] | [{"table": "workday__employee_overview", "column": "overall_employee_score"}, {"table": "workday__employee_overview", "column": "career_development_score"}] | False |


## S59

类别 `data`；来源 `query_db`；调用 `b6a420e78e234eb69ef9fff7dad0ad14`；状态 `success`。

```sql
WITH ranked AS (
  SELECT *, ROW_NUMBER() OVER (PARTITION BY employee_id ORDER BY position_start_date DESC, overall_employee_score DESC, career_development_score DESC, total_promotions DESC) as rn
  FROM workday__employee_overview
),
emp AS (SELECT * FROM ranked WHERE rn = 1)
SELECT 
  compensation_tier,
  COUNT(*) as total,
  SUM(CASE WHEN retention_stability_score < 60 AND overall_employee_score > 80 THEN 1 ELSE 0 END) as attrition_risk,
  ROUND(100.0 * SUM(CASE WHEN retention_stability_score < 60 AND overall_employee_score > 80 THEN 1 ELSE 0 END) / COUNT(*), 1) as attrition_pct
FROM emp
GROUP BY compensation_tier
ORDER BY attrition_pct DESC
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-083/attempt-01/sql/S59.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-083/attempt-01/sql/S59.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-083/attempt-01/results/S59.rows.jsonl)；完整：True；SHA256：`0e316aef2907e896f501fef5641fd112595f9e5e7fa325a63f4b3481a7a360e0`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "workday__employee_overview", "kind": "base", "block": null, "base_tables": ["workday__employee_overview"]}] | [] | [] |
| B2 | [{"alias": "ranked", "kind": "derived", "block": "B1", "base_tables": ["workday__employee_overview"]}] | [] | [] |
| B3 | [{"alias": "emp", "kind": "derived", "block": "B2", "base_tables": ["workday__employee_overview"]}] | [] | ["compensation_tier"] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B3 | COUNT(*) | [] | [] | True |
| B3 | SUM(CASE WHEN retention_stability_score < 60 AND overall_employee_score > 80 THEN 1 ELSE 0 END) | [] | [{"table": "workday__employee_overview", "column": "retention_stability_score"}, {"table": "workday__employee_overview", "column": "overall_employee_score"}] | False |
| B3 | COUNT(*) | [] | [] | True |
| B3 | SUM(CASE WHEN retention_stability_score < 60 AND overall_employee_score > 80 THEN 1 ELSE 0 END) | [] | [{"table": "workday__employee_overview", "column": "retention_stability_score"}, {"table": "workday__employee_overview", "column": "overall_employee_score"}] | False |


## S60

类别 `data`；来源 `query_db`；调用 `59f719ff2f084f62b71e8ba4596e79c9`；状态 `success`。

```sql
WITH ranked AS (
  SELECT *, ROW_NUMBER() OVER (PARTITION BY employee_id ORDER BY position_start_date DESC, overall_employee_score DESC, career_development_score DESC, total_promotions DESC) as rn
  FROM workday__employee_overview
),
emp AS (SELECT * FROM ranked WHERE rn = 1)
SELECT 
  dept_performance_category,
  COUNT(*) as total,
  SUM(CASE WHEN retention_stability_score < 60 AND overall_employee_score > 80 THEN 1 ELSE 0 END) as attrition_risk,
  ROUND(100.0 * SUM(CASE WHEN retention_stability_score < 60 AND overall_employee_score > 80 THEN 1 ELSE 0 END) / COUNT(*), 1) as attrition_pct,
  ROUND(AVG(dept_turnover_rate), 3) as avg_turnover
FROM emp
GROUP BY dept_performance_category
ORDER BY attrition_pct DESC
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-083/attempt-01/sql/S60.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-083/attempt-01/sql/S60.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-083/attempt-01/results/S60.rows.jsonl)；完整：True；SHA256：`370879b10a36ca3f65cc6c0782f654a76322f0a537ad670b9d7ef008a0a93fc5`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "workday__employee_overview", "kind": "base", "block": null, "base_tables": ["workday__employee_overview"]}] | [] | [] |
| B2 | [{"alias": "ranked", "kind": "derived", "block": "B1", "base_tables": ["workday__employee_overview"]}] | [] | [] |
| B3 | [{"alias": "emp", "kind": "derived", "block": "B2", "base_tables": ["workday__employee_overview"]}] | [] | ["dept_performance_category"] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B3 | COUNT(*) | [] | [] | True |
| B3 | SUM(CASE WHEN retention_stability_score < 60 AND overall_employee_score > 80 THEN 1 ELSE 0 END) | [] | [{"table": "workday__employee_overview", "column": "retention_stability_score"}, {"table": "workday__employee_overview", "column": "overall_employee_score"}] | False |
| B3 | AVG(dept_turnover_rate) | [{"table": "workday__employee_overview", "column": "dept_turnover_rate"}] | [] | False |
| B3 | COUNT(*) | [] | [] | True |
| B3 | SUM(CASE WHEN retention_stability_score < 60 AND overall_employee_score > 80 THEN 1 ELSE 0 END) | [] | [{"table": "workday__employee_overview", "column": "retention_stability_score"}, {"table": "workday__employee_overview", "column": "overall_employee_score"}] | False |


## S61

类别 `data`；来源 `query_db`；调用 `cc16894874fe4c4a8d747a89133f1125`；状态 `success`。

```sql
WITH ranked AS (
  SELECT *, ROW_NUMBER() OVER (PARTITION BY employee_id ORDER BY position_start_date DESC, overall_employee_score DESC, career_development_score DESC, total_promotions DESC) as rn
  FROM workday__employee_overview
),
emp AS (SELECT * FROM ranked WHERE rn = 1)
SELECT 
  organization_sub_type,
  COUNT(*) as total,
  SUM(CASE WHEN retention_stability_score < 60 AND overall_employee_score > 80 THEN 1 ELSE 0 END) as attrition_risk,
  ROUND(100.0 * SUM(CASE WHEN retention_stability_score < 60 AND overall_employee_score > 80 THEN 1 ELSE 0 END) / NULLIF(COUNT(*), 0), 1) as attrition_pct
FROM emp
GROUP BY organization_sub_type
HAVING COUNT(*) >= 20
ORDER BY attrition_pct DESC
LIMIT 10
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-083/attempt-01/sql/S61.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-083/attempt-01/sql/S61.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-083/attempt-01/results/S61.rows.jsonl)；完整：True；SHA256：`d5e514f15e9706f18eea699c43aa3295e56b1dd422e6dfb409114296991b63d0`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "workday__employee_overview", "kind": "base", "block": null, "base_tables": ["workday__employee_overview"]}] | [] | [] |
| B2 | [{"alias": "ranked", "kind": "derived", "block": "B1", "base_tables": ["workday__employee_overview"]}] | [] | [] |
| B3 | [{"alias": "emp", "kind": "derived", "block": "B2", "base_tables": ["workday__employee_overview"]}] | [] | ["organization_sub_type"] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B3 | COUNT(*) | [] | [] | True |
| B3 | SUM(CASE WHEN retention_stability_score < 60 AND overall_employee_score > 80 THEN 1 ELSE 0 END) | [] | [{"table": "workday__employee_overview", "column": "retention_stability_score"}, {"table": "workday__employee_overview", "column": "overall_employee_score"}] | False |
| B3 | COUNT(*) | [] | [] | True |
| B3 | SUM(CASE WHEN retention_stability_score < 60 AND overall_employee_score > 80 THEN 1 ELSE 0 END) | [] | [{"table": "workday__employee_overview", "column": "retention_stability_score"}, {"table": "workday__employee_overview", "column": "overall_employee_score"}] | False |
| B3 | COUNT(*) | [] | [] | True |


## S62

类别 `data`；来源 `query_db`；调用 `2bf2ad4d1f994376b0dcd06eaa63bab7`；状态 `success`。

```sql
WITH ranked AS (
  SELECT *, ROW_NUMBER() OVER (PARTITION BY employee_id ORDER BY position_start_date DESC, overall_employee_score DESC, career_development_score DESC, total_promotions DESC) as rn
  FROM workday__employee_overview
),
emp AS (SELECT * FROM ranked WHERE rn = 1),
core AS (
  SELECT * FROM emp 
  WHERE overall_employee_score > 75 AND career_development_score > 78.57581219355939
)
SELECT 
  organization_type,
  dept_performance_category,
  COUNT(*) as total_core,
  SUM(CASE WHEN employee_risk_level IN ('High','Medium') THEN 1 ELSE 0 END) as risk_core,
  ROUND(100.0 * SUM(CASE WHEN employee_risk_level IN ('High','Medium') THEN 1 ELSE 0 END) / COUNT(*), 1) as risk_pct,
  ROUND(AVG(overall_employee_score), 1) as avg_overall,
  ROUND(AVG(career_development_score), 1) as avg_career,
  ROUND(AVG(retention_stability_score), 1) as avg_retention
FROM core
GROUP BY organization_type, dept_performance_category
ORDER BY risk_pct DESC
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-083/attempt-01/sql/S62.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-083/attempt-01/sql/S62.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-083/attempt-01/results/S62.rows.jsonl)；完整：True；SHA256：`3a9e1f701ad7712d558b8a727fcf7ad460f40e2732714e53011128c3db7b073d`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "workday__employee_overview", "kind": "base", "block": null, "base_tables": ["workday__employee_overview"]}] | [] | [] |
| B2 | [{"alias": "ranked", "kind": "derived", "block": "B1", "base_tables": ["workday__employee_overview"]}] | [] | [] |
| B3 | [{"alias": "emp", "kind": "derived", "block": "B2", "base_tables": ["workday__employee_overview"]}] | [] | [] |
| B4 | [{"alias": "core", "kind": "derived", "block": "B3", "base_tables": ["workday__employee_overview"]}] | [] | ["organization_type", "dept_performance_category"] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B4 | COUNT(*) | [] | [] | True |
| B4 | SUM(CASE WHEN employee_risk_level IN ('High', 'Medium') THEN 1 ELSE 0 END) | [] | [{"table": "workday__employee_overview", "column": "employee_risk_level"}] | False |
| B4 | AVG(overall_employee_score) | [{"table": "workday__employee_overview", "column": "overall_employee_score"}] | [] | False |
| B4 | AVG(career_development_score) | [{"table": "workday__employee_overview", "column": "career_development_score"}] | [] | False |
| B4 | AVG(retention_stability_score) | [{"table": "workday__employee_overview", "column": "retention_stability_score"}] | [] | False |
| B4 | COUNT(*) | [] | [] | True |
| B4 | SUM(CASE WHEN employee_risk_level IN ('High', 'Medium') THEN 1 ELSE 0 END) | [] | [{"table": "workday__employee_overview", "column": "employee_risk_level"}] | False |


## S63

类别 `data`；来源 `query_db`；调用 `594a7cbda3b44167acee0f8705b23318`；状态 `success`。

```sql
WITH ranked AS (
  SELECT *, ROW_NUMBER() OVER (PARTITION BY employee_id ORDER BY position_start_date DESC, overall_employee_score DESC, career_development_score DESC, total_promotions DESC) as rn
  FROM workday__employee_overview
),
emp AS (SELECT * FROM ranked WHERE rn = 1),
core AS (
  SELECT * FROM emp 
  WHERE overall_employee_score > 75 AND career_development_score > 78.57581219355939
),
tiers AS (
  SELECT 
    CASE WHEN highest_management_level_reached = 0 THEN 'Individual Contributor (L0)'
         WHEN highest_management_level_reached = 1 THEN 'Team Lead (L1)'
         WHEN highest_management_level_reached = 2 THEN 'Manager (L2)'
         ELSE 'Senior Management (L3+)' END as mgmt_tier,
    dept_performance_category,
    COUNT(*) as n_core,
    SUM(CASE WHEN employee_risk_level IN ('High','Medium') THEN 1 ELSE 0 END) as n_at_risk,
    SUM(CASE WHEN retention_stability_score < 60 THEN 1 ELSE 0 END) as n_low_retention,
    ROUND(100.0 * SUM(CASE WHEN employee_risk_level IN ('High','Medium') THEN 1 ELSE 0 END) / COUNT(*), 1) as at_risk_pct,
    ROUND(AVG(overall_employee_score), 1) as avg_overall,
    ROUND(AVG(career_development_score), 1) as avg_career,
    ROUND(AVG(retention_stability_score), 1) as avg_retention
  FROM core
  GROUP BY mgmt_tier, dept_performance_category
)
SELECT * FROM tiers
ORDER BY at_risk_pct DESC, n_core DESC
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-083/attempt-01/sql/S63.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-083/attempt-01/sql/S63.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-083/attempt-01/results/S63.rows.jsonl)；完整：True；SHA256：`266efb541dcebbb8ee564ad3b2259e41f2cae47003607f37bb6797977a669c89`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "workday__employee_overview", "kind": "base", "block": null, "base_tables": ["workday__employee_overview"]}] | [] | [] |
| B2 | [{"alias": "ranked", "kind": "derived", "block": "B1", "base_tables": ["workday__employee_overview"]}] | [] | [] |
| B3 | [{"alias": "emp", "kind": "derived", "block": "B2", "base_tables": ["workday__employee_overview"]}] | [] | [] |
| B4 | [{"alias": "core", "kind": "derived", "block": "B3", "base_tables": ["workday__employee_overview"]}] | [] | ["CASE WHEN highest_management_level_reached = 0 THEN 'Individual Contributor (L0)' WHEN highest_management_level_reached = 1 THEN 'Team Lead (L1)' WHEN highest_management_level_reached = 2 THEN 'Manager (L2)' ELSE 'Senior Management (L3+)' END", "dept_performance_category"] |
| B5 | [{"alias": "tiers", "kind": "derived", "block": "B4", "base_tables": ["workday__employee_overview"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B4 | COUNT(*) | [] | [] | True |
| B4 | SUM(CASE WHEN employee_risk_level IN ('High', 'Medium') THEN 1 ELSE 0 END) | [] | [{"table": "workday__employee_overview", "column": "employee_risk_level"}] | False |
| B4 | SUM(CASE WHEN retention_stability_score < 60 THEN 1 ELSE 0 END) | [] | [{"table": "workday__employee_overview", "column": "retention_stability_score"}] | False |
| B4 | AVG(overall_employee_score) | [{"table": "workday__employee_overview", "column": "overall_employee_score"}] | [] | False |
| B4 | AVG(career_development_score) | [{"table": "workday__employee_overview", "column": "career_development_score"}] | [] | False |
| B4 | AVG(retention_stability_score) | [{"table": "workday__employee_overview", "column": "retention_stability_score"}] | [] | False |
| B4 | COUNT(*) | [] | [] | True |
| B4 | SUM(CASE WHEN employee_risk_level IN ('High', 'Medium') THEN 1 ELSE 0 END) | [] | [{"table": "workday__employee_overview", "column": "employee_risk_level"}] | False |


## S64

类别 `data`；来源 `python`；调用 `2fbc47a89f5c419ead938cfddd319f4d`；状态 `success`。

```sql

WITH ranked AS (
  SELECT *, ROW_NUMBER() OVER (PARTITION BY employee_id ORDER BY position_start_date DESC, overall_employee_score DESC, career_development_score DESC, total_promotions DESC) as rn
  FROM workday__employee_overview
),
emp AS (SELECT * FROM ranked WHERE rn = 1),
core AS (
  SELECT * FROM emp 
  WHERE overall_employee_score > 75 AND career_development_score > 78.57581219355939
)
SELECT 
  CASE WHEN highest_management_level_reached = 0 THEN 'IC (L0)'
       WHEN highest_management_level_reached = 1 THEN 'Team Lead (L1)'
       WHEN highest_management_level_reached = 2 THEN 'Manager (L2)'
       ELSE 'Sr Mgmt (L3+)' END as mgmt_tier,
  dept_performance_category,
  COUNT(*) as n_core,
  SUM(CASE WHEN employee_risk_level IN ('High','Medium') THEN 1 ELSE 0 END) as n_at_risk,
  ROUND(100.0 * SUM(CASE WHEN employee_risk_level IN ('High','Medium') THEN 1 ELSE 0 END) / COUNT(*), 1) as at_risk_pct
FROM core
GROUP BY mgmt_tier, dept_performance_category

```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-083/attempt-01/sql/S64.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-083/attempt-01/sql/S64.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-083/attempt-01/results/S64.rows.jsonl)；完整：True；SHA256：`bba09aeecf254f09ba098a8dee830b76dbf0266f2048f53038c5cb8bf19e074a`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "workday__employee_overview", "kind": "base", "block": null, "base_tables": ["workday__employee_overview"]}] | [] | [] |
| B2 | [{"alias": "ranked", "kind": "derived", "block": "B1", "base_tables": ["workday__employee_overview"]}] | [] | [] |
| B3 | [{"alias": "emp", "kind": "derived", "block": "B2", "base_tables": ["workday__employee_overview"]}] | [] | [] |
| B4 | [{"alias": "core", "kind": "derived", "block": "B3", "base_tables": ["workday__employee_overview"]}] | [] | ["CASE WHEN highest_management_level_reached = 0 THEN 'IC (L0)' WHEN highest_management_level_reached = 1 THEN 'Team Lead (L1)' WHEN highest_management_level_reached = 2 THEN 'Manager (L2)' ELSE 'Sr Mgmt (L3+)' END", "dept_performance_category"] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B4 | COUNT(*) | [] | [] | True |
| B4 | SUM(CASE WHEN employee_risk_level IN ('High', 'Medium') THEN 1 ELSE 0 END) | [] | [{"table": "workday__employee_overview", "column": "employee_risk_level"}] | False |
| B4 | COUNT(*) | [] | [] | True |
| B4 | SUM(CASE WHEN employee_risk_level IN ('High', 'Medium') THEN 1 ELSE 0 END) | [] | [{"table": "workday__employee_overview", "column": "employee_risk_level"}] | False |


## S65

类别 `data`；来源 `python`；调用 `2fbc47a89f5c419ead938cfddd319f4d`；状态 `success`。

```sql

WITH ranked AS (
  SELECT *, ROW_NUMBER() OVER (PARTITION BY employee_id ORDER BY position_start_date DESC, overall_employee_score DESC, career_development_score DESC, total_promotions DESC) as rn
  FROM workday__employee_overview
),
emp AS (SELECT * FROM ranked WHERE rn = 1)
SELECT organization_sub_type, COUNT(*) as total,
       SUM(CASE WHEN retention_stability_score < 60 AND overall_employee_score > 80 THEN 1 ELSE 0 END) as attrition_risk,
       ROUND(100.0 * SUM(CASE WHEN retention_stability_score < 60 AND overall_employee_score > 80 THEN 1 ELSE 0 END) / COUNT(*), 1) as attrition_pct
FROM emp
GROUP BY organization_sub_type
HAVING COUNT(*) >= 20
ORDER BY attrition_pct DESC

```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-083/attempt-01/sql/S65.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-083/attempt-01/sql/S65.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-083/attempt-01/results/S65.rows.jsonl)；完整：True；SHA256：`10ef16d57b5c17d0dc294b763995954d00070a7a8dbaa787d8ba455b199c096a`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "workday__employee_overview", "kind": "base", "block": null, "base_tables": ["workday__employee_overview"]}] | [] | [] |
| B2 | [{"alias": "ranked", "kind": "derived", "block": "B1", "base_tables": ["workday__employee_overview"]}] | [] | [] |
| B3 | [{"alias": "emp", "kind": "derived", "block": "B2", "base_tables": ["workday__employee_overview"]}] | [] | ["organization_sub_type"] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B3 | COUNT(*) | [] | [] | True |
| B3 | SUM(CASE WHEN retention_stability_score < 60 AND overall_employee_score > 80 THEN 1 ELSE 0 END) | [] | [{"table": "workday__employee_overview", "column": "retention_stability_score"}, {"table": "workday__employee_overview", "column": "overall_employee_score"}] | False |
| B3 | COUNT(*) | [] | [] | True |
| B3 | COUNT(*) | [] | [] | True |
| B3 | SUM(CASE WHEN retention_stability_score < 60 AND overall_employee_score > 80 THEN 1 ELSE 0 END) | [] | [{"table": "workday__employee_overview", "column": "retention_stability_score"}, {"table": "workday__employee_overview", "column": "overall_employee_score"}] | False |

