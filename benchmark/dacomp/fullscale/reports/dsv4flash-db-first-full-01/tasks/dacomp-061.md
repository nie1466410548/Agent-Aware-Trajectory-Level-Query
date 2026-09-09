# dacomp-061

A peculiar phenomenon has been observed recently: some projects have a very short `avg_clo…

运行：已提交。官方未评分。全部 SQL 尝试/成功 53/53；数据 SQL 51/51；Python 5 次。

完整原题：

A peculiar phenomenon has been observed recently: some projects have a very short `avg_close_time_days` (less than 15 days), but their `team_stability_percentage` is low (this metric needs to be redefined, as the current data shows it as 100%). Are these projects, characterized by rapid delivery but high turnover, truly healthy?

Please conduct an in-depth analysis of the quality indicators (including indirect metrics like bug rate, rework frequency, and code quality) and long-term sustainability of such projects to explore the true relationship between speed and stability and its impact on long-term project success.

| 表 | 行数 | 列数 |
| --- | --- | --- |
| jira__issue_intelligence_analytics | 13799108 | 34 |
| jira__project_enhanced | 200 | 30 |
| jira__team_performance_dashboard | 4374 | 33 |


实际路线（分析者依据 SQL/源码概括，不代表 Agent 自述）：S3：jira__project_enhanced 查询 → S13：jira__issue_intelligence_analytics 分组聚合 → S23：jira__project_enhanced 分组聚合 → S33：jira__issue_intelligence_analytics 查询 → S43：jira__issue_intelligence_analytics 分组聚合 → S53：jira__issue_intelligence_analytics/jira__project_enhanced 分组聚合（等距列出六个结构节点，全部步骤见下表）

数据库大小：3,524,939,776 字节。

## 数据 SQL

| SQL | 状态 | 基础表 | Join 输入/类型 | GROUP BY | 聚合表达式 | 结果行数 | 数据库 ms |
| --- | --- | --- | --- | --- | --- | --- | --- |
| [S3/Q1](#s3) | success | ["jira__project_enhanced"] | 0 / {} | [] | [] | 20 | 0.886 |
| [S4/Q2](#s4) | success | ["jira__project_enhanced"] | 0 / {} | [] | ["COUNT(*)", "AVG(avg_close_time_days)", "MIN(avg_close_time_days)", "MAX(avg_close_time_days)"] | 1 | 0.497 |
| [S5/Q3](#s5) | success | ["jira__project_enhanced"] | 0 / {} | [] | [] | 5 | 0.479 |
| [S6/Q4](#s6) | success | ["jira__team_performance_dashboard"] | 0 / {} | [] | [] | 5 | 1.771 |
| [S7/Q5](#s7) | success | ["jira__project_enhanced"] | 0 / {} | ["project_name"] | ["COUNT(*)", "AVG(avg_close_time_days)"] | 70 | 0.609 |
| [S8/Q6](#s8) | success | ["jira__team_performance_dashboard"] | 0 / {} | ["project_name"] | ["COUNT(*)", "SUM(at_churn_risk)", "SUM(inactive_recently)", "AVG(consistency_percentage)", "AVG(resolution_rate_percentage)", "AVG(overall_performance_score)"] | 5 | 3.127 |
| [S9/Q7](#s9) | success | ["jira__issue_intelligence_analytics"] | 0 / {} | ["project_name"] | ["COUNT(*)"] | 70 | 8629.064 |
| [S10/Q8](#s10) | success | ["jira__issue_intelligence_analytics"] | 0 / {} | ["issue_type"] | ["COUNT(*)"] | 7 | 7094.313 |
| [S11/Q9](#s11) | success | ["jira__project_enhanced"] | 0 / {} | ["project_name"] | ["AVG(avg_close_time_days)", "COUNT(*)"] | 2 | 0.418 |
| [S12/Q10](#s12) | success | ["jira__issue_intelligence_analytics"] | 0 / {} | ["health_status"] | ["COUNT(*)"] | 1 | 6769.199 |
| [S13/Q11](#s13) | success | ["jira__issue_intelligence_analytics"] | 0 / {} | ["current_status"] | ["COUNT(*)"] | 6 | 7173.482 |
| [S14/Q12](#s14) | success | ["jira__issue_intelligence_analytics"] | 0 / {} | ["lifecycle_outlier_status"] | ["COUNT(*)"] | 4 | 7138.712 |
| [S15/Q13](#s15) | success | ["jira__issue_intelligence_analytics"] | 0 / {} | ["lifecycle_pattern"] | ["COUNT(*)"] | 1 | 6347.348 |
| [S16/Q14](#s16) | success | ["jira__issue_intelligence_analytics"] | 0 / {} | ["intervention_urgency"] | ["COUNT(*)"] | 1 | 6774.592 |
| [S17/Q15](#s17) | success | ["jira__team_performance_dashboard"] | 0 / {} | [] | [] | 12 | 1.12 |
| [S18/Q16](#s18) | success | ["jira__team_performance_dashboard"] | 0 / {} | [] | [] | 15 | 0.97 |
| [S19/Q17](#s19) | success | ["jira__team_performance_dashboard"] | 0 / {} | [] | [] | 3 | 1.055 |
| [S20/Q18](#s20) | success | ["jira__team_performance_dashboard"] | 0 / {} | ["project_name"] | ["COUNT(*)", "SUM(at_churn_risk)", "SUM(inactive_recently)", "AVG(consistency_percentage)", "AVG(resolution_rate_percentage)", "AVG(overall_performance_score)", "AVG(avg_sprint_completion_rate)", "AVG(days_since_first_issue)"] | 2 | 1.03 |
| [S21/Q19](#s21) | success | ["jira__issue_intelligence_analytics"] | 0 / {} | [] | ["MIN(lifecycle_quality_score)", "MAX(lifecycle_quality_score)", "AVG(lifecycle_quality_score)", "MIN(regression_ratio)", "MAX(regression_ratio)", "AVG(regression_ratio)", "MIN(lifecycle_deviation_ratio)", "MAX(lifecycle_deviation_ratio)", "AVG(lifecycle_deviation_ratio)", "MIN(completion_probability)", "MAX(completion_probability)", "AVG(completion_probability)", "MIN(total_risk_score)", "MAX(total_risk_score)", "AVG(total_risk_score)", "MIN(intelligence_score)", "MAX(intelligence_score)", "AVG(intelligence_score)"] | 1 | 10099.204 |
| [S22/Q20](#s22) | success | ["jira__issue_intelligence_analytics"] | 0 / {} | ["project_name"] | ["COUNT(*)", "SUM(CASE WHEN issue_type = 'Bug' THEN 1 ELSE 0 END)", "AVG(regression_ratio)", "AVG(lifecycle_quality_score)", "AVG(total_risk_score)", "AVG(intelligence_score)", "SUM(CASE WHEN lifecycle_outlier_status = 'Unusually Fast' THEN 1 ELSE 0 END)", "SUM(CASE WHEN lifecycle_outlier_status = 'Statistical Outlier' THEN 1 ELSE 0 END)", "SUM(CASE WHEN lifecycle_outlier_status = 'Above Normal Range' THEN 1 ELSE 0 END)", "AVG(completion_probability)"] | 2 | 2898.113 |
| [S23/Q21](#s23) | success | ["jira__project_enhanced"] | 0 / {} | ["project_name"] | ["COUNT(*)", "AVG(avg_close_time_days)", "MIN(avg_close_time_days)", "MAX(avg_close_time_days)", "SUM(count_closed_issues)", "SUM(count_open_issues)"] | 70 | 0.7 |
| [S24/Q22](#s24) | success | ["jira__issue_intelligence_analytics"] | 0 / {} | ["project_name"] | ["COUNT(*)", "AVG(regression_ratio)", "AVG(lifecycle_quality_score)", "AVG(lifecycle_deviation_ratio)", "AVG(total_risk_score)", "AVG(completion_probability)", "AVG(intelligence_score)", "COUNT(DISTINCT assignee_name)", "COUNT(*)", "COUNT(*)", "COUNT(*)", "COUNT(*)", "COUNT(*)", "COUNT(*)", "COUNT(*)", "COUNT(*)", "COUNT(*)", "COUNT(*)", "COUNT(*)", "COUNT(*)", "COUNT(*)", "SUM(CASE WHEN issue_type = 'Bug' THEN 1 ELSE 0 END)", "SUM(CASE WHEN lifecycle_outlier_status = 'Unusually Fast' THEN 1 ELSE 0 END)", "SUM(CASE WHEN lifecycle_outlier_status = 'Statistical Outlier' THEN 1 ELSE 0 END)", "SUM(CASE WHEN lifecycle_outlier_status = 'Above Normal Range' THEN 1 ELSE 0 END)", "SUM(CASE WHEN current_status = 'Blocked' THEN 1 ELSE 0 END)", "SUM(CASE WHEN high_complexity_risk = 1 THEN 1 ELSE 0 END)", "SUM(CASE WHEN is_active_sprint = 1 THEN 1 ELSE 0 END)", "SUM(CASE WHEN assignment_risk_score > 0 THEN 1 ELSE 0 END)", "SUM(CASE WHEN engagement_risk_score > 0 THEN 1 ELSE 0 END)", "SUM(CASE WHEN age_risk_score > 0 THEN 1 ELSE 0 END)", "SUM(CASE WHEN process_risk_score > 0 THEN 1 ELSE 0 END)", "SUM(CASE WHEN deviation_risk_score > 0 THEN 1 ELSE 0 END)", "SUM(CASE WHEN complexity_risk_score > 0 THEN 1 ELSE 0 END)"] | 70 | 35123.37 |
| [S25/Q23](#s25) | success | ["jira__project_enhanced"] | 0 / {} | ["project_name"] | ["AVG(avg_close_time_days)", "MIN(avg_close_time_days)", "MAX(avg_close_time_days)", "SUM(count_closed_issues)", "SUM(count_open_issues)", "AVG(avg_age_currently_open_days)", "AVG(median_close_time_days)"] | 70 | 0.781 |
| [S26/Q24](#s26) | success | ["jira__team_performance_dashboard"] | 0 / {} | ["project_name"] | ["COUNT(*)", "SUM(at_churn_risk)", "SUM(inactive_recently)", "AVG(consistency_percentage)", "AVG(resolution_rate_percentage)", "AVG(overall_performance_score)", "AVG(avg_sprint_completion_rate)", "AVG(days_since_first_issue)", "AVG(estimate_accuracy_percentage)"] | 5 | 4.017 |
| [S27/Q25](#s27) | success | ["jira__issue_intelligence_analytics"] | 0 / {} | ["project_name"] | ["COUNT(*)", "AVG(regression_ratio)", "AVG(lifecycle_quality_score)", "AVG(lifecycle_deviation_ratio)", "AVG(total_risk_score)", "AVG(completion_probability)", "AVG(intelligence_score)", "COUNT(DISTINCT assignee_name)", "COUNT(*)", "COUNT(*)", "COUNT(*)", "COUNT(*)", "COUNT(*)", "COUNT(*)", "COUNT(*)", "COUNT(*)", "COUNT(*)", "COUNT(*)", "COUNT(*)", "COUNT(*)", "SUM(CASE WHEN issue_type = 'Bug' THEN 1 ELSE 0 END)", "SUM(CASE WHEN lifecycle_outlier_status = 'Unusually Fast' THEN 1 ELSE 0 END)", "SUM(CASE WHEN lifecycle_outlier_status = 'Statistical Outlier' THEN 1 ELSE 0 END)", "SUM(CASE WHEN lifecycle_outlier_status = 'Above Normal Range' THEN 1 ELSE 0 END)", "SUM(CASE WHEN current_status = 'Blocked' THEN 1 ELSE 0 END)", "SUM(CASE WHEN high_complexity_risk = 1 THEN 1 ELSE 0 END)", "SUM(CASE WHEN assignment_risk_score > 0 THEN 1 ELSE 0 END)", "SUM(CASE WHEN engagement_risk_score > 0 THEN 1 ELSE 0 END)", "SUM(CASE WHEN age_risk_score > 0 THEN 1 ELSE 0 END)", "SUM(CASE WHEN process_risk_score > 0 THEN 1 ELSE 0 END)", "SUM(CASE WHEN deviation_risk_score > 0 THEN 1 ELSE 0 END)", "SUM(CASE WHEN complexity_risk_score > 0 THEN 1 ELSE 0 END)"] | 70 | 34336.968 |
| [S28/Q26](#s28) | success | ["jira__project_enhanced"] | 0 / {} | ["project_name"] | ["AVG(avg_close_time_days)", "MIN(avg_close_time_days)", "MAX(avg_close_time_days)", "SUM(count_closed_issues)", "SUM(count_open_issues)", "AVG(avg_age_currently_open_days)", "AVG(median_close_time_days)"] | 70 | 0.763 |
| [S29/Q27](#s29) | success | ["jira__team_performance_dashboard"] | 0 / {} | ["project_name"] | ["COUNT(*)", "SUM(at_churn_risk)", "SUM(inactive_recently)", "AVG(consistency_percentage)", "AVG(resolution_rate_percentage)", "AVG(overall_performance_score)", "AVG(avg_sprint_completion_rate)", "AVG(days_since_first_issue)", "AVG(estimate_accuracy_percentage)"] | 5 | 3.829 |
| [S30/Q28](#s30) | success | ["jira__project_enhanced"] | 0 / {} | [] | [] | 5 | 0.457 |
| [S31/Q29](#s31) | success | ["jira__issue_intelligence_analytics"] | 0 / {} | ["issue_type"] | ["COUNT(*)", "AVG(regression_ratio)", "AVG(lifecycle_quality_score)", "AVG(total_lifecycle_days)", "AVG(lifecycle_deviation_ratio)", "AVG(total_risk_score)", "COUNT(*)", "COUNT(*)", "COUNT(*)", "COUNT(*)", "SUM(CASE WHEN lifecycle_outlier_status = 'Unusually Fast' THEN 1 ELSE 0 END)", "SUM(CASE WHEN lifecycle_outlier_status = 'Statistical Outlier' THEN 1 ELSE 0 END)", "SUM(CASE WHEN lifecycle_outlier_status = 'Above Normal Range' THEN 1 ELSE 0 END)", "SUM(CASE WHEN current_status = 'Blocked' THEN 1 ELSE 0 END)"] | 7 | 2182.048 |
| [S32/Q30](#s32) | success | ["jira__issue_intelligence_analytics"] | 0 / {} | ["issue_type"] | ["COUNT(*)", "AVG(regression_ratio)", "AVG(lifecycle_quality_score)", "AVG(total_lifecycle_days)", "AVG(lifecycle_deviation_ratio)", "AVG(total_risk_score)", "COUNT(*)", "COUNT(*)", "COUNT(*)", "COUNT(*)", "SUM(CASE WHEN lifecycle_outlier_status = 'Unusually Fast' THEN 1 ELSE 0 END)", "SUM(CASE WHEN lifecycle_outlier_status = 'Statistical Outlier' THEN 1 ELSE 0 END)", "SUM(CASE WHEN lifecycle_outlier_status = 'Above Normal Range' THEN 1 ELSE 0 END)", "SUM(CASE WHEN current_status = 'Blocked' THEN 1 ELSE 0 END)"] | 7 | 2212.219 |
| [S33/Q31](#s33) | success | ["jira__issue_intelligence_analytics"] | 0 / {} | [] | ["AVG(regression_ratio)", "AVG(lifecycle_quality_score)", "AVG(lifecycle_deviation_ratio)", "AVG(total_risk_score)", "AVG(intelligence_score)", "AVG(completion_probability)"] | 1 | 4447.286 |
| [S34/Q32](#s34) | success | ["jira__issue_intelligence_analytics"] | 0 / {} | ["project_name"] | ["AVG(regression_ratio)", "AVG(lifecycle_quality_score)", "AVG(lifecycle_deviation_ratio)", "AVG(total_risk_score)", "AVG(intelligence_score)", "AVG(completion_probability)", "COUNT(*)", "COUNT(*)", "COUNT(*)", "COUNT(*)", "COUNT(*)", "SUM(CASE WHEN lifecycle_outlier_status = 'Unusually Fast' THEN 1 ELSE 0 END)", "SUM(CASE WHEN lifecycle_outlier_status = 'Statistical Outlier' THEN 1 ELSE 0 END)", "SUM(CASE WHEN lifecycle_outlier_status = 'Above Normal Range' THEN 1 ELSE 0 END)", "SUM(CASE WHEN current_status = 'Blocked' THEN 1 ELSE 0 END)", "SUM(CASE WHEN issue_type = 'Bug' THEN 1 ELSE 0 END)"] | 70 | 20557.787 |
| [S35/Q33](#s35) | success | ["jira__project_enhanced"] | 0 / {} | ["project_name"] | ["AVG(avg_close_time_days)", "MIN(avg_close_time_days)"] | 70 | 0.573 |
| [S36/Q34](#s36) | success | ["jira__team_performance_dashboard"] | 0 / {} | ["project_name"] | ["COUNT(*)", "SUM(at_churn_risk)", "AVG(consistency_percentage)", "AVG(avg_sprint_completion_rate)", "AVG(days_since_first_issue)", "AVG(estimate_accuracy_percentage)", "AVG(overall_performance_score)"] | 5 | 3.189 |
| [S37/Q35](#s37) | success | ["jira__project_enhanced"] | 0 / {} | [] | [] | 8 | 0.424 |
| [S38/Q36](#s38) | success | ["jira__issue_intelligence_analytics"] | 0 / {} | ["regression_ratio"] | ["COUNT(*)"] | 3 | 11057.345 |
| [S39/Q37](#s39) | success | ["jira__issue_intelligence_analytics"] | 0 / {} | ["regression_ratio"] | ["COUNT(*)"] | 2 | 2460.267 |
| [S40/Q38](#s40) | success | ["jira__issue_intelligence_analytics"] | 0 / {} | ["regression_ratio"] | ["COUNT(*)"] | 3 | 11318.764 |
| [S41/Q39](#s41) | success | ["jira__issue_intelligence_analytics"] | 0 / {} | ["regression_ratio"] | ["COUNT(*)"] | 2 | 2467.163 |
| [S42/Q40](#s42) | success | ["jira__issue_intelligence_analytics"] | 0 / {} | ["regression_ratio"] | ["COUNT(*)"] | 3 | 11411.66 |
| [S43/Q41](#s43) | success | ["jira__issue_intelligence_analytics"] | 0 / {} | ["CASE WHEN project_name IN ('Data Analytics Delta', 'Mobile App Delta') THEN 'Fast Projects' ELSE 'Other Projects' END"] | ["AVG(age_risk_score)", "AVG(process_risk_score)", "AVG(complexity_risk_score)", "AVG(engagement_risk_score)", "AVG(assignment_risk_score)", "AVG(deviation_risk_score)", "AVG(total_risk_score)", "AVG(total_opportunity_score)"] | 2 | 15489.516 |
| [S44/Q42](#s44) | success | ["jira__issue_intelligence_analytics"] | 0 / {} | ["lifecycle_quality_score"] | ["COUNT(*)"] | 71 | 12604.189 |
| [S45/Q43](#s45) | success | ["jira__issue_intelligence_analytics"] | 0 / {} | ["CASE WHEN project_name IN ('Data Analytics Delta', 'Mobile App Delta') THEN 'Fast Projects' ELSE 'Other Projects' END", "lifecycle_quality_score"] | ["COUNT(*)"] | 142 | 18573.92 |
| [S46/Q44](#s46) | success | ["jira__issue_intelligence_analytics"] | 0 / {} | ["project_name"] | ["AVG(age_risk_score)", "AVG(process_risk_score)", "AVG(engagement_risk_score)", "AVG(assignment_risk_score)", "AVG(deviation_risk_score)", "AVG(complexity_risk_score)", "AVG(total_risk_score)", "AVG(total_opportunity_score)", "AVG(intelligence_score)", "AVG(collaboration_opportunity_score)", "AVG(efficiency_opportunity_score)", "AVG(process_opportunity_score)"] | 2 | 3199.452 |
| [S47/Q45](#s47) | success | ["jira__issue_intelligence_analytics"] | 0 / {} | [] | ["AVG(age_risk_score)", "AVG(process_risk_score)", "AVG(engagement_risk_score)", "AVG(assignment_risk_score)", "AVG(deviation_risk_score)", "AVG(complexity_risk_score)", "AVG(total_risk_score)", "AVG(total_opportunity_score)", "AVG(collaboration_opportunity_score)", "AVG(efficiency_opportunity_score)", "AVG(process_opportunity_score)"] | 1 | 7500.918 |
| [S48/Q46](#s48) | success | ["jira__team_performance_dashboard"] | 0 / {} | [] | [] | 12 | 1.068 |
| [S49/Q47](#s49) | success | ["jira__team_performance_dashboard"] | 0 / {} | [] | [] | 15 | 0.726 |
| [S50/Q48](#s50) | success | ["jira__team_performance_dashboard"] | 0 / {} | [] | [] | 10 | 0.596 |
| [S51/Q49](#s51) | success | ["jira__team_performance_dashboard"] | 0 / {} | [] | [] | 8 | 0.585 |
| [S52/Q50](#s52) | success | ["jira__team_performance_dashboard"] | 0 / {} | [] | [] | 4329 | 2.697 |
| [S53/Q51](#s53) | success | ["jira__issue_intelligence_analytics", "jira__project_enhanced"] | 2 / {'INNER': 1} | ["project_name", "project_name"] | ["AVG(avg_close_time_days)", "AVG(regression_ratio)", "AVG(lifecycle_quality_score)"] | 70 | 11327.558 |


## 元数据和设置

| SQL | 类别 | 状态 | 内容 |
| --- | --- | --- | --- |
| S1 | connection_setup | success | PRAGMA query_only=ON |
| S2 | metadata | success | SELECT name,sql FROM sqlite_master WHERE type='table' ORDER BY name |


## Python 与执行位置

人工源码审查：**database_first_violation**。Most large-table preparation is in SQL. Python performs statistical comparisons and rendering, which are allowed, but also merges SQL-derived project/issue/team aggregates using pandas. Those joins are supported in SQLite and no engine limitation is shown; these portions violate database_first_v1. Preserve this primary attempt. [证据](../reviews/dacomp-061.json)。

P1：I need to combine the three datasets (issue aggregate, project enhanced aggregate, team performance) and perform statistical comparisons between fast projects (avg_close_time_days < 15) and slower projects. This requires correlation analysis and visualization which is better suited for Python.

[源码](../../../runs/dsv4flash-db-first-full-01/dacomp-061/attempt-01/python/P1.py)；[输出](../../../runs/dsv4flash-db-first-full-01/dacomp-061/attempt-01/python/P1.stdout)；[错误](../../../runs/dsv4flash-db-first-full-01/dacomp-061/attempt-01/python/P1.stderr)。检出需人工核验的 SQL 可实现操作：.merge(, .query(；不能仅凭理由判为合规。

P2：I need to analyze the individual project instances with avg_close_time < 15 days, and compute more detailed metrics including the specific issue-level characteristics to understand the quality trade-offs. Also need to compute weighted stability combining churn risk and consistency.

[源码](../../../runs/dsv4flash-db-first-full-01/dacomp-061/attempt-01/python/P2.py)；[输出](../../../runs/dsv4flash-db-first-full-01/dacomp-061/attempt-01/python/P2.stdout)；[错误](../../../runs/dsv4flash-db-first-full-01/dacomp-061/attempt-01/python/P2.stderr)。检出需人工核验的 SQL 可实现操作：.merge(, .query(；不能仅凭理由判为合规。

P3：I need to examine the distribution of regression_ratio across fast vs slow projects to understand the quality difference, and also compute the redefined team stability metric comprehensively. This requires Python for statistical analysis and visualization.

[源码](../../../runs/dsv4flash-db-first-full-01/dacomp-061/attempt-01/python/P3.py)；[输出](../../../runs/dsv4flash-db-first-full-01/dacomp-061/attempt-01/python/P3.stdout)；[错误](../../../runs/dsv4flash-db-first-full-01/dacomp-061/attempt-01/python/P3.stderr)。检出需人工核验的 SQL 可实现操作：.query(；不能仅凭理由判为合规。

P4：Fix the regression distribution analysis code that had an indexing error. The fast projects have no regression_ratio=0.0 rows, so the pie chart code needs to handle this.

[源码](../../../runs/dsv4flash-db-first-full-01/dacomp-061/attempt-01/python/P4.py)；[输出](../../../runs/dsv4flash-db-first-full-01/dacomp-061/attempt-01/python/P4.stdout)；[错误](../../../runs/dsv4flash-db-first-full-01/dacomp-061/attempt-01/python/P4.stderr)。检出需人工核验的 SQL 可实现操作：.query(；不能仅凭理由判为合规。

P5：I need to quantify workload concentration on churn-risk members for the fast project teams, and compute long-term sustainability indicators. This requires combining team-level flags with issue workload and is best done in Python for visualization and final summary metrics.

[源码](../../../runs/dsv4flash-db-first-full-01/dacomp-061/attempt-01/python/P5.py)；[输出](../../../runs/dsv4flash-db-first-full-01/dacomp-061/attempt-01/python/P5.stdout)；[错误](../../../runs/dsv4flash-db-first-full-01/dacomp-061/attempt-01/python/P5.stderr)。检出需人工核验的 SQL 可实现操作：.query(；不能仅凭理由判为合规。

## 优化机会

已验证候选。筛选限于精确 SQL、相同自包含 CTE、相同单表完整过滤、可分解单表聚合；未覆盖任意 Join 等价和一般谓词蕴含。全部候选都是 offline，未测在线预测。

| 候选 | 类型 | 已有结果 | 覆盖 SQL | 后续次数 | 中间行数 | 验证 | 成本 |
| --- | --- | --- | --- | --- | --- | --- | --- |
| C1 | exact-result reuse | True | ["S25", "S28"] | 1 | unknown | not_verified_cap | Not tested |
| C2 | exact-result reuse | True | ["S26", "S29"] | 1 | unknown | not_verified_cap | Not tested |
| C3 | aggregate MV | False | ["S4", "S7", "S23", "S25", "S28", "S35"] | 5 | 70 | verified | Not benchmarked; correctness alone does not establish net speedup. |
| C4 | common filtered view | False | ["S5", "S11", "S30"] | 2 | unknown | not_verified_cap | Not tested |
| C5 | aggregate MV | False | ["S8", "S26", "S29", "S36"] | 3 | unknown | not_verified_cap | Not tested |
| C6 | aggregate MV | False | ["S9", "S10", "S12", "S13", "S14", "S15", "S16", "S21", "S33", "S34", "S38", "S43", "S44", "S45"] | 13 | 293205 | rejected_result_mismatch | Not benchmarked; correctness alone does not establish net speedup. |
| C7 | common filtered view | False | ["S17", "S48"] | 1 | unknown | not_verified_cap | Not tested |
| C8 | common filtered view | False | ["S18", "S49"] | 1 | unknown | not_verified_cap | Not tested |
| C9 | common filtered view | False | ["S22", "S39", "S41", "S46"] | 3 | unknown | not_verified_cap | Not tested |
| C10 | aggregate MV | False | ["S22", "S39", "S41", "S46"] | 3 | 4 | rejected_result_mismatch | Not benchmarked; correctness alone does not establish net speedup. |
| C11 | common filtered view | False | ["S40", "S42", "S47"] | 2 | unknown | not_verified_cap | Not tested |
| C12 | aggregate MV | False | ["S40", "S42", "S47"] | 2 | unknown | not_verified_cap | Not tested |


已验证覆盖（含触发查询、候选并集去重）：6/51 条成功数据 SQL。正确性仅针对当前数据库快照；未测性能的候选不能声称已加速。

[完整 build/rewrite 与比较证据](dacomp-061.analysis.json)。

### C3：aggregate MV

Union of grouping keys; decomposable aggregate states; AVG uses SUM and non-NULL COUNT.

原查询 [S4](#s4), [S7](#s7), [S23](#s23), [S25](#s25), [S28](#s28), [S35](#s35) → 新增共享状态 C3 → 后续 5 次可复用。该构建点为事后假设，不代表 Agent 当时预知后续。

构建定义：

```sql
SELECT project_name AS __g0, COUNT(*) AS __a0, SUM(avg_close_time_days) AS __a1_sum, COUNT(avg_close_time_days) AS __a1_n, MIN(avg_close_time_days) AS __a2, MAX(avg_close_time_days) AS __a3, SUM(count_closed_issues) AS __a4, SUM(count_open_issues) AS __a5, SUM(avg_age_currently_open_days) AS __a6_sum, COUNT(avg_age_currently_open_days) AS __a6_n, SUM(median_close_time_days) AS __a7_sum, COUNT(median_close_time_days) AS __a7_n FROM "jira__project_enhanced"  GROUP BY project_name
```

受益查询 S4 的改写示例：

```sql
SELECT SUM(__a0) AS cnt, (1.0 * SUM(__a1_sum) / NULLIF(SUM(__a1_n), 0)) AS avg_close, MIN(__a2) AS min_close, MAX(__a3) AS max_close FROM temp.reuse_candidate
```

| 原 SQL | 列名一致 | 结果一致 | 比较方法 |
| --- | --- | --- | --- |
| S4 | True | True | exact_multiset |
| S7 | True | True | ordered_numeric_tolerance |
| S23 | True | True | exact_multiset |
| S25 | True | True | exact_multiset |
| S28 | True | True | exact_multiset |
| S35 | True | True | exact_multiset |


验证状态：verified；成本结论：Not benchmarked; correctness alone does not establish net speedup.

### C6：aggregate MV

Union of grouping keys; decomposable aggregate states; AVG uses SUM and non-NULL COUNT.

原查询 [S9](#s9), [S10](#s10), [S12](#s12), [S13](#s13), [S14](#s14), [S15](#s15), [S16](#s16), [S21](#s21), [S33](#s33), [S34](#s34), [S38](#s38), [S43](#s43), [S44](#s44), [S45](#s45) → 新增共享状态 C6 → 后续 13 次可复用。该构建点为事后假设，不代表 Agent 当时预知后续。

构建定义：

```sql
SELECT project_name AS __g0, issue_type AS __g1, health_status AS __g2, current_status AS __g3, lifecycle_outlier_status AS __g4, lifecycle_pattern AS __g5, intervention_urgency AS __g6, regression_ratio AS __g7, CASE WHEN project_name IN ('Data Analytics Delta', 'Mobile App Delta') THEN 'Fast Projects' ELSE 'Other Projects' END AS __g8, lifecycle_quality_score AS __g9, COUNT(*) AS __a0, MIN(lifecycle_quality_score) AS __a1, MAX(lifecycle_quality_score) AS __a2, SUM(lifecycle_quality_score) AS __a3_sum, COUNT(lifecycle_quality_score) AS __a3_n, MIN(regression_ratio) AS __a4, MAX(regression_ratio) AS __a5, SUM(regression_ratio) AS __a6_sum, COUNT(regression_ratio) AS __a6_n, MIN(lifecycle_deviation_ratio) AS __a7, MAX(lifecycle_deviation_ratio) AS __a8, SUM(lifecycle_deviation_ratio) AS __a9_sum, COUNT(lifecycle_deviation_ratio) AS __a9_n, MIN(completion_probability) AS __a10, MAX(completion_probability) AS __a11, SUM(completion_probability) AS __a12_sum, COUNT(completion_probability) AS __a12_n, MIN(total_risk_score) AS __a13, MAX(total_risk_score) AS __a14, SUM(total_risk_score) AS __a15_sum, COUNT(total_risk_score) AS __a15_n, MIN(intelligence_score) AS __a16, MAX(intelligence_score) AS __a17, SUM(intelligence_score) AS __a18_sum, COUNT(intelligence_score) AS __a18_n, SUM(CASE WHEN lifecycle_outlier_status = 'Unusually Fast' THEN 1 ELSE 0 END) AS __a19, SUM(CASE WHEN lifecycle_outlier_status = 'Statistical Outlier' THEN 1 ELSE 0 END) AS __a20, SUM(CASE WHEN lifecycle_outlier_status = 'Above Normal Range' THEN 1 ELSE 0 END) AS __a21, SUM(CASE WHEN current_status = 'Blocked' THEN 1 ELSE 0 END) AS __a22, SUM(CASE WHEN issue_type = 'Bug' THEN 1 ELSE 0 END) AS __a23, SUM(age_risk_score) AS __a24_sum, COUNT(age_risk_score) AS __a24_n, SUM(process_risk_score) AS __a25_sum, COUNT(process_risk_score) AS __a25_n, SUM(complexity_risk_score) AS __a26_sum, COUNT(complexity_risk_score) AS __a26_n, SUM(engagement_risk_score) AS __a27_sum, COUNT(engagement_risk_score) AS __a27_n, SUM(assignment_risk_score) AS __a28_sum, COUNT(assignment_risk_score) AS __a28_n, SUM(deviation_risk_score) AS __a29_sum, COUNT(deviation_risk_score) AS __a29_n, SUM(total_opportunity_score) AS __a30_sum, COUNT(total_opportunity_score) AS __a30_n FROM "jira__issue_intelligence_analytics"  GROUP BY project_name, issue_type, health_status, current_status, lifecycle_outlier_status, lifecycle_pattern, intervention_urgency, regression_ratio, CASE WHEN project_name IN ('Data Analytics Delta', 'Mobile App Delta') THEN 'Fast Projects' ELSE 'Other Projects' END, lifecycle_quality_score
```

受益查询 S9 的改写示例：

```sql
SELECT __g0 AS "project_name", SUM(__a0) AS cnt FROM temp.reuse_candidate GROUP BY __g0 ORDER BY cnt DESC
```

| 原 SQL | 列名一致 | 结果一致 | 比较方法 |
| --- | --- | --- | --- |
| S9 | True | True | ordered_numeric_tolerance |
| S10 | True | True | ordered_numeric_tolerance |
| S12 | True | True | exact_multiset |
| S13 | True | True | exact_multiset |
| S14 | True | True | exact_multiset |
| S15 | True | True | exact_multiset |
| S16 | True | True | exact_multiset |
| S21 | True | False | exact_multiset |
| S33 | True | False | exact_multiset |
| S34 | True | False | exact_multiset |
| S38 | True | True | ordered_numeric_tolerance |
| S43 | True | True | exact_multiset |
| S44 | True | True | ordered_numeric_tolerance |
| S45 | True | True | ordered_numeric_tolerance |


验证状态：rejected_result_mismatch；成本结论：Not benchmarked; correctness alone does not establish net speedup.

### C5：aggregate MV

Union of grouping keys; decomposable aggregate states; AVG uses SUM and non-NULL COUNT.

原查询 [S8](#s8), [S26](#s26), [S29](#s29), [S36](#s36) → 新增共享状态 C5 → 后续 3 次可复用。该构建点为事后假设，不代表 Agent 当时预知后续。

构建定义：

```sql
SELECT project_name AS __g0, COUNT(*) AS __a0, SUM(at_churn_risk) AS __a1, SUM(inactive_recently) AS __a2, SUM(consistency_percentage) AS __a3_sum, COUNT(consistency_percentage) AS __a3_n, SUM(resolution_rate_percentage) AS __a4_sum, COUNT(resolution_rate_percentage) AS __a4_n, SUM(overall_performance_score) AS __a5_sum, COUNT(overall_performance_score) AS __a5_n, SUM(avg_sprint_completion_rate) AS __a6_sum, COUNT(avg_sprint_completion_rate) AS __a6_n, SUM(days_since_first_issue) AS __a7_sum, COUNT(days_since_first_issue) AS __a7_n, SUM(estimate_accuracy_percentage) AS __a8_sum, COUNT(estimate_accuracy_percentage) AS __a8_n FROM "jira__team_performance_dashboard"  GROUP BY project_name
```

受益查询 S8 的改写示例：

```sql
SELECT __g0 AS "project_name", SUM(__a0) AS members, SUM(__a1) AS churn_risk, SUM(__a2) AS inactive, (1.0 * SUM(__a3_sum) / NULLIF(SUM(__a3_n), 0)) AS avg_consistency, (1.0 * SUM(__a4_sum) / NULLIF(SUM(__a4_n), 0)) AS avg_res_rate, (1.0 * SUM(__a5_sum) / NULLIF(SUM(__a5_n), 0)) AS avg_perf FROM temp.reuse_candidate GROUP BY __g0
```

验证状态：not_verified_cap；成本结论：Not tested

结果依赖：自动记录 SQL→Python 的接口父调用，以及源码中引用归档文件的消费者；字面值相同不认定因果。模型方向选择需要人工读取消息，尚未做全面因果标注。

[原始报告](../../../runs/dsv4flash-db-first-full-01/dacomp-061/attempt-01/answer.md)；[统一消息](../../../runs/dsv4flash-db-first-full-01/dacomp-061/attempt-01/messages.jsonl)；[原始 OpenCode 事件](../../../runs/dsv4flash-db-first-full-01/dacomp-061/attempt-01/opencode.jsonl)；[SQL 引擎日志](../../../runs/dsv4flash-db-first-full-01/dacomp-061/attempt-01/sql_journal.jsonl)。

[可读报告（本地图片链接规范化）](../answers/dacomp-061.md)。原始回答保留，分析结论未改写。

## S1

类别 `connection_setup`；来源 `connection`；调用 `38cf868058734ba69429968772c0ac40`；状态 `success`。

```sql
PRAGMA query_only=ON
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-061/attempt-01/sql/S1.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-061/attempt-01/sql/S1.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-061/attempt-01/results/S1.rows.jsonl)；完整：True；SHA256：`e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`。

## S2

类别 `metadata`；来源 `list_db`；调用 `38cf868058734ba69429968772c0ac40`；状态 `success`。

```sql
SELECT name,sql FROM sqlite_master WHERE type='table' ORDER BY name
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-061/attempt-01/sql/S2.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-061/attempt-01/sql/S2.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-061/attempt-01/results/S2.rows.jsonl)；完整：True；SHA256：`e6884123ed22ef6d3886369977f8a453af06725910977f932f01ba8b7a788ef3`。

## S3

类别 `data`；来源 `query_db`；调用 `fad115fd2cfe424ab95e6d55b4cdbbee`；状态 `success`。

```sql
SELECT * FROM jira__project_enhanced ORDER BY avg_close_time_days ASC LIMIT 20
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-061/attempt-01/sql/S3.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-061/attempt-01/sql/S3.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-061/attempt-01/results/S3.rows.jsonl)；完整：True；SHA256：`f2f970710d4f02617f003ef0079cd02ca03dabffa67f97c9da336f4375fb2eb4`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "jira__project_enhanced", "kind": "base", "block": null, "base_tables": ["jira__project_enhanced"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |


## S4

类别 `data`；来源 `query_db`；调用 `31601172d2ea4cc2b487a0fdcc9c92e7`；状态 `success`。

```sql
SELECT COUNT(*) as cnt, AVG(avg_close_time_days) as avg_close, MIN(avg_close_time_days) as min_close, MAX(avg_close_time_days) as max_close FROM jira__project_enhanced
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-061/attempt-01/sql/S4.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-061/attempt-01/sql/S4.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-061/attempt-01/results/S4.rows.jsonl)；完整：True；SHA256：`e3c286bf46a31338ab3dca5c0d867b317554b0ea4ddf109fc67793be41d852d8`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "jira__project_enhanced", "kind": "base", "block": null, "base_tables": ["jira__project_enhanced"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |
| B1 | AVG(avg_close_time_days) | [{"table": "jira__project_enhanced", "column": "avg_close_time_days"}] | [] | False |
| B1 | MIN(avg_close_time_days) | [{"table": "jira__project_enhanced", "column": "avg_close_time_days"}] | [] | False |
| B1 | MAX(avg_close_time_days) | [{"table": "jira__project_enhanced", "column": "avg_close_time_days"}] | [] | False |


## S5

类别 `data`；来源 `query_db`；调用 `c8821678755f4891b18162009da60e68`；状态 `success`。

```sql
SELECT * FROM jira__project_enhanced WHERE avg_close_time_days < 15 ORDER BY avg_close_time_days ASC
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-061/attempt-01/sql/S5.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-061/attempt-01/sql/S5.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-061/attempt-01/results/S5.rows.jsonl)；完整：True；SHA256：`942cad1518ae2fc7cf644b35489bd911fa0693b36d197f7aff3582f4994809f1`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "jira__project_enhanced", "kind": "base", "block": null, "base_tables": ["jira__project_enhanced"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |


## S6

类别 `data`；来源 `query_db`；调用 `04ca3d0ab3c24b85b66bf1683a24f7d4`；状态 `success`。

```sql
SELECT DISTINCT project_name, project_id FROM jira__team_performance_dashboard ORDER BY project_name
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-061/attempt-01/sql/S6.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-061/attempt-01/sql/S6.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-061/attempt-01/results/S6.rows.jsonl)；完整：True；SHA256：`7f394d8af7687a8e2076e46273d89e01e53fd9e85cca14a20509f270e10ce3e6`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "jira__team_performance_dashboard", "kind": "base", "block": null, "base_tables": ["jira__team_performance_dashboard"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |


## S7

类别 `data`；来源 `query_db`；调用 `93fb8874872440ebbf54e8b53f5858d7`；状态 `success`。

```sql
SELECT project_name, COUNT(*) as cnt, AVG(avg_close_time_days) as avg_close FROM jira__project_enhanced GROUP BY project_name ORDER BY project_name
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-061/attempt-01/sql/S7.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-061/attempt-01/sql/S7.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-061/attempt-01/results/S7.rows.jsonl)；完整：True；SHA256：`6e4195eaf1789dec5b4dd602a0fec30314dab79f3a1d549e2fc2ce1c42714e07`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "jira__project_enhanced", "kind": "base", "block": null, "base_tables": ["jira__project_enhanced"]}] | [] | ["project_name"] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |
| B1 | AVG(avg_close_time_days) | [{"table": "jira__project_enhanced", "column": "avg_close_time_days"}] | [] | False |


## S8

类别 `data`；来源 `query_db`；调用 `5c1feb004f3f437faa0743d3f608ac88`；状态 `success`。

```sql
SELECT project_name, COUNT(*) as members, SUM(at_churn_risk) as churn_risk, SUM(inactive_recently) as inactive, AVG(consistency_percentage) as avg_consistency, AVG(resolution_rate_percentage) as avg_res_rate, AVG(overall_performance_score) as avg_perf FROM jira__team_performance_dashboard GROUP BY project_name
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-061/attempt-01/sql/S8.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-061/attempt-01/sql/S8.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-061/attempt-01/results/S8.rows.jsonl)；完整：True；SHA256：`9159f548e3d592259cd7881c4f266e969a813911f1c72dd1583205ca7f1f4482`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "jira__team_performance_dashboard", "kind": "base", "block": null, "base_tables": ["jira__team_performance_dashboard"]}] | [] | ["project_name"] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |
| B1 | SUM(at_churn_risk) | [{"table": "jira__team_performance_dashboard", "column": "at_churn_risk"}] | [] | False |
| B1 | SUM(inactive_recently) | [{"table": "jira__team_performance_dashboard", "column": "inactive_recently"}] | [] | False |
| B1 | AVG(consistency_percentage) | [{"table": "jira__team_performance_dashboard", "column": "consistency_percentage"}] | [] | False |
| B1 | AVG(resolution_rate_percentage) | [{"table": "jira__team_performance_dashboard", "column": "resolution_rate_percentage"}] | [] | False |
| B1 | AVG(overall_performance_score) | [{"table": "jira__team_performance_dashboard", "column": "overall_performance_score"}] | [] | False |


## S9

类别 `data`；来源 `query_db`；调用 `0e90260b5b7441d3983dd7675021988d`；状态 `success`。

```sql
SELECT project_name, COUNT(*) as cnt FROM jira__issue_intelligence_analytics GROUP BY project_name ORDER BY cnt DESC
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-061/attempt-01/sql/S9.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-061/attempt-01/sql/S9.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-061/attempt-01/results/S9.rows.jsonl)；完整：True；SHA256：`431b4ea69e04ec766fe854ea9c0046be44f5c5dbd0ab22a9841d07e480cf6b1d`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "jira__issue_intelligence_analytics", "kind": "base", "block": null, "base_tables": ["jira__issue_intelligence_analytics"]}] | [] | ["project_name"] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |


## S10

类别 `data`；来源 `query_db`；调用 `8ffbaf043ec44de2bd6f066b6b846d16`；状态 `success`。

```sql
SELECT issue_type, COUNT(*) as cnt FROM jira__issue_intelligence_analytics GROUP BY issue_type ORDER BY cnt DESC
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-061/attempt-01/sql/S10.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-061/attempt-01/sql/S10.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-061/attempt-01/results/S10.rows.jsonl)；完整：True；SHA256：`d8cf3abb3e0bfaa7b81bbb7efea56a2c64333f53e18fab61a82ab113b6e67162`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "jira__issue_intelligence_analytics", "kind": "base", "block": null, "base_tables": ["jira__issue_intelligence_analytics"]}] | [] | ["issue_type"] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |


## S11

类别 `data`；来源 `query_db`；调用 `7328759d61d1467c9822b4da1153a7c8`；状态 `success`。

```sql
SELECT project_name, AVG(avg_close_time_days) as avg_close, COUNT(*) as instances FROM jira__project_enhanced WHERE avg_close_time_days < 15 GROUP BY project_name
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-061/attempt-01/sql/S11.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-061/attempt-01/sql/S11.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-061/attempt-01/results/S11.rows.jsonl)；完整：True；SHA256：`25ee4cbd3b2a8c01fa54c974695113c0997a05a3928672f588bc63233c826a6c`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "jira__project_enhanced", "kind": "base", "block": null, "base_tables": ["jira__project_enhanced"]}] | [] | ["project_name"] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | AVG(avg_close_time_days) | [{"table": "jira__project_enhanced", "column": "avg_close_time_days"}] | [] | False |
| B1 | COUNT(*) | [] | [] | True |


## S12

类别 `data`；来源 `query_db`；调用 `2e8dfce4bddb43e39805e26177fc6255`；状态 `success`。

```sql
SELECT health_status, COUNT(*) as cnt FROM jira__issue_intelligence_analytics GROUP BY health_status
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-061/attempt-01/sql/S12.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-061/attempt-01/sql/S12.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-061/attempt-01/results/S12.rows.jsonl)；完整：True；SHA256：`1c2e2701324c624927a3cf4182415a4b1886fd44e02d4ca962f300f97c197613`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "jira__issue_intelligence_analytics", "kind": "base", "block": null, "base_tables": ["jira__issue_intelligence_analytics"]}] | [] | ["health_status"] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |


## S13

类别 `data`；来源 `query_db`；调用 `8f46cc6e29674c3b87e711d43419e44c`；状态 `success`。

```sql
SELECT current_status, COUNT(*) as cnt FROM jira__issue_intelligence_analytics GROUP BY current_status
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-061/attempt-01/sql/S13.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-061/attempt-01/sql/S13.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-061/attempt-01/results/S13.rows.jsonl)；完整：True；SHA256：`53c9b85b71b4e070bfc9741c1aa752073d8b28684f43e9a5475a338b76ae3d12`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "jira__issue_intelligence_analytics", "kind": "base", "block": null, "base_tables": ["jira__issue_intelligence_analytics"]}] | [] | ["current_status"] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |


## S14

类别 `data`；来源 `query_db`；调用 `9b759618ed1e426b832b9638b8ef5593`；状态 `success`。

```sql
SELECT lifecycle_outlier_status, COUNT(*) as cnt FROM jira__issue_intelligence_analytics GROUP BY lifecycle_outlier_status
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-061/attempt-01/sql/S14.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-061/attempt-01/sql/S14.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-061/attempt-01/results/S14.rows.jsonl)；完整：True；SHA256：`9de136fcbdf23d23d74dbc6cf0d80b0e8ab7564384793d59d2be71f122983329`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "jira__issue_intelligence_analytics", "kind": "base", "block": null, "base_tables": ["jira__issue_intelligence_analytics"]}] | [] | ["lifecycle_outlier_status"] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |


## S15

类别 `data`；来源 `query_db`；调用 `26ac7025be6a4d1aa90fae1da4d5032f`；状态 `success`。

```sql
SELECT lifecycle_pattern, COUNT(*) as cnt FROM jira__issue_intelligence_analytics GROUP BY lifecycle_pattern
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-061/attempt-01/sql/S15.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-061/attempt-01/sql/S15.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-061/attempt-01/results/S15.rows.jsonl)；完整：True；SHA256：`74012a59597f99510be9344fe6d76b4f0a875ffa219aa99d71ea8ba437076fb7`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "jira__issue_intelligence_analytics", "kind": "base", "block": null, "base_tables": ["jira__issue_intelligence_analytics"]}] | [] | ["lifecycle_pattern"] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |


## S16

类别 `data`；来源 `query_db`；调用 `f69f77ff7b61496a8fbae6f4aebaa639`；状态 `success`。

```sql
SELECT intervention_urgency, COUNT(*) as cnt FROM jira__issue_intelligence_analytics GROUP BY intervention_urgency
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-061/attempt-01/sql/S16.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-061/attempt-01/sql/S16.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-061/attempt-01/results/S16.rows.jsonl)；完整：True；SHA256：`b204812123aa656241155faf2f82d24894a61d038077b975756c1efad9da6d8f`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "jira__issue_intelligence_analytics", "kind": "base", "block": null, "base_tables": ["jira__issue_intelligence_analytics"]}] | [] | ["intervention_urgency"] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |


## S17

类别 `data`；来源 `query_db`；调用 `a82b252eea484e4197a9ee1eb8a137fe`；状态 `success`。

```sql
SELECT user_display_name, current_engagement_tier, current_pattern_type, current_lifecycle_stage, avg_daily_activity_score, avg_weekly_activity_score, consistency_percentage, total_assigned_issues, resolved_issues, resolution_rate_percentage, avg_resolution_days, bug_issues, estimate_accuracy_percentage, unique_collaborators_on_issues, sprint_count, avg_sprint_completion_rate, days_since_first_issue, at_churn_risk, inactive_recently, poor_estimation, overall_performance_score, performance_tier FROM jira__team_performance_dashboard WHERE project_name = 'Data Analytics Delta' ORDER BY at_churn_risk DESC, overall_performance_score DESC
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-061/attempt-01/sql/S17.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-061/attempt-01/sql/S17.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-061/attempt-01/results/S17.rows.jsonl)；完整：True；SHA256：`d9d4d59d2121fbed53fa4cdd7f14a9b98a2336a2980809c21da5ae9605586838`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "jira__team_performance_dashboard", "kind": "base", "block": null, "base_tables": ["jira__team_performance_dashboard"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |


## S18

类别 `data`；来源 `query_db`；调用 `d8f7a9f8471d4841b7ffead3b53c18a9`；状态 `success`。

```sql
SELECT user_display_name, current_engagement_tier, current_pattern_type, current_lifecycle_stage, consistency_percentage, total_assigned_issues, resolved_issues, resolution_rate_percentage, bug_issues, sprint_count, avg_sprint_completion_rate, days_since_first_issue, at_churn_risk, inactive_recently, poor_estimation, overall_performance_score, performance_tier FROM jira__team_performance_dashboard WHERE project_name = 'Mobile App Delta' ORDER BY at_churn_risk DESC, overall_performance_score DESC
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-061/attempt-01/sql/S18.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-061/attempt-01/sql/S18.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-061/attempt-01/results/S18.rows.jsonl)；完整：True；SHA256：`260fd10a6d0abde4bbebc4a9e10f058f557d580a35f8282f3419352556754c11`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "jira__team_performance_dashboard", "kind": "base", "block": null, "base_tables": ["jira__team_performance_dashboard"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |


## S19

类别 `data`；来源 `query_db`；调用 `4ce23e8ae155402a8c83c0dedabfa03a`；状态 `success`。

```sql
SELECT user_display_name, consistency_percentage, total_assigned_issues, bug_issues, sprint_count, avg_sprint_completion_rate, days_since_first_issue, at_churn_risk, overall_performance_score FROM jira__team_performance_dashboard WHERE project_name = 'Mobile App Delta' AND user_display_name NOT IN ('Robert Martinez', 'Robert Thomas', 'William Johnson', 'Anna Smith', 'Michelle Martin', 'Anna Moore', 'Maria Rodriguez', 'Thomas Hernandez', 'Anna Brown', 'Chris Moore', 'James Miller', 'Thomas Taylor') ORDER BY at_churn_risk DESC, overall_performance_score DESC
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-061/attempt-01/sql/S19.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-061/attempt-01/sql/S19.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-061/attempt-01/results/S19.rows.jsonl)；完整：True；SHA256：`050f899b210df9c5363e86bab5561ffef25592d2a24b57a423bde7a0a336608f`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "jira__team_performance_dashboard", "kind": "base", "block": null, "base_tables": ["jira__team_performance_dashboard"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |


## S20

类别 `data`；来源 `query_db`；调用 `085043a729094502ae15ebb917a359f1`；状态 `success`。

```sql
SELECT project_name, COUNT(*) as members, SUM(at_churn_risk) as churn_risk, SUM(inactive_recently) as inactive, AVG(consistency_percentage) as avg_consistency, AVG(resolution_rate_percentage) as avg_res_rate, AVG(overall_performance_score) as avg_perf, AVG(avg_sprint_completion_rate) as avg_sprint_completion, AVG(days_since_first_issue) as avg_tenure FROM jira__team_performance_dashboard WHERE project_name IN ('Data Analytics Delta', 'Mobile App Delta') GROUP BY project_name
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-061/attempt-01/sql/S20.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-061/attempt-01/sql/S20.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-061/attempt-01/results/S20.rows.jsonl)；完整：True；SHA256：`2830f11f2b5b07d60261962693238efea9695ce6cb84fed71b8de02c9420d617`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "jira__team_performance_dashboard", "kind": "base", "block": null, "base_tables": ["jira__team_performance_dashboard"]}] | [] | ["project_name"] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |
| B1 | SUM(at_churn_risk) | [{"table": "jira__team_performance_dashboard", "column": "at_churn_risk"}] | [] | False |
| B1 | SUM(inactive_recently) | [{"table": "jira__team_performance_dashboard", "column": "inactive_recently"}] | [] | False |
| B1 | AVG(consistency_percentage) | [{"table": "jira__team_performance_dashboard", "column": "consistency_percentage"}] | [] | False |
| B1 | AVG(resolution_rate_percentage) | [{"table": "jira__team_performance_dashboard", "column": "resolution_rate_percentage"}] | [] | False |
| B1 | AVG(overall_performance_score) | [{"table": "jira__team_performance_dashboard", "column": "overall_performance_score"}] | [] | False |
| B1 | AVG(avg_sprint_completion_rate) | [{"table": "jira__team_performance_dashboard", "column": "avg_sprint_completion_rate"}] | [] | False |
| B1 | AVG(days_since_first_issue) | [{"table": "jira__team_performance_dashboard", "column": "days_since_first_issue"}] | [] | False |


## S21

类别 `data`；来源 `query_db`；调用 `b2c0b1c66cca46569ee68977b5774351`；状态 `success`。

```sql
SELECT MIN(lifecycle_quality_score) as min_lqs, MAX(lifecycle_quality_score) as max_lqs, AVG(lifecycle_quality_score) as avg_lqs, MIN(regression_ratio) as min_rr, MAX(regression_ratio) as max_rr, AVG(regression_ratio) as avg_rr, MIN(lifecycle_deviation_ratio) as min_ldr, MAX(lifecycle_deviation_ratio) as max_ldr, AVG(lifecycle_deviation_ratio) as avg_ldr, MIN(completion_probability) as min_cp, MAX(completion_probability) as max_cp, AVG(completion_probability) as avg_cp, MIN(total_risk_score) as min_trs, MAX(total_risk_score) as max_trs, AVG(total_risk_score) as avg_trs, MIN(intelligence_score) as min_is, MAX(intelligence_score) as max_is, AVG(intelligence_score) as avg_is FROM jira__issue_intelligence_analytics
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-061/attempt-01/sql/S21.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-061/attempt-01/sql/S21.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-061/attempt-01/results/S21.rows.jsonl)；完整：True；SHA256：`4a5796854bf47ea1e5d4aed6f6bf4262f67b75c9e90b42fde6151026ba53b9b5`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "jira__issue_intelligence_analytics", "kind": "base", "block": null, "base_tables": ["jira__issue_intelligence_analytics"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | MIN(lifecycle_quality_score) | [{"table": "jira__issue_intelligence_analytics", "column": "lifecycle_quality_score"}] | [] | False |
| B1 | MAX(lifecycle_quality_score) | [{"table": "jira__issue_intelligence_analytics", "column": "lifecycle_quality_score"}] | [] | False |
| B1 | AVG(lifecycle_quality_score) | [{"table": "jira__issue_intelligence_analytics", "column": "lifecycle_quality_score"}] | [] | False |
| B1 | MIN(regression_ratio) | [{"table": "jira__issue_intelligence_analytics", "column": "regression_ratio"}] | [] | False |
| B1 | MAX(regression_ratio) | [{"table": "jira__issue_intelligence_analytics", "column": "regression_ratio"}] | [] | False |
| B1 | AVG(regression_ratio) | [{"table": "jira__issue_intelligence_analytics", "column": "regression_ratio"}] | [] | False |
| B1 | MIN(lifecycle_deviation_ratio) | [{"table": "jira__issue_intelligence_analytics", "column": "lifecycle_deviation_ratio"}] | [] | False |
| B1 | MAX(lifecycle_deviation_ratio) | [{"table": "jira__issue_intelligence_analytics", "column": "lifecycle_deviation_ratio"}] | [] | False |
| B1 | AVG(lifecycle_deviation_ratio) | [{"table": "jira__issue_intelligence_analytics", "column": "lifecycle_deviation_ratio"}] | [] | False |
| B1 | MIN(completion_probability) | [{"table": "jira__issue_intelligence_analytics", "column": "completion_probability"}] | [] | False |
| B1 | MAX(completion_probability) | [{"table": "jira__issue_intelligence_analytics", "column": "completion_probability"}] | [] | False |
| B1 | AVG(completion_probability) | [{"table": "jira__issue_intelligence_analytics", "column": "completion_probability"}] | [] | False |
| B1 | MIN(total_risk_score) | [{"table": "jira__issue_intelligence_analytics", "column": "total_risk_score"}] | [] | False |
| B1 | MAX(total_risk_score) | [{"table": "jira__issue_intelligence_analytics", "column": "total_risk_score"}] | [] | False |
| B1 | AVG(total_risk_score) | [{"table": "jira__issue_intelligence_analytics", "column": "total_risk_score"}] | [] | False |
| B1 | MIN(intelligence_score) | [{"table": "jira__issue_intelligence_analytics", "column": "intelligence_score"}] | [] | False |
| B1 | MAX(intelligence_score) | [{"table": "jira__issue_intelligence_analytics", "column": "intelligence_score"}] | [] | False |
| B1 | AVG(intelligence_score) | [{"table": "jira__issue_intelligence_analytics", "column": "intelligence_score"}] | [] | False |


## S22

类别 `data`；来源 `query_db`；调用 `5c7e144e49ab458fa8d496eea76be117`；状态 `success`。

```sql
SELECT project_name, COUNT(*) as total_issues, SUM(CASE WHEN issue_type='Bug' THEN 1 ELSE 0 END) as bugs, AVG(regression_ratio) as avg_regression, AVG(lifecycle_quality_score) as avg_lqs, AVG(total_risk_score) as avg_risk, AVG(intelligence_score) as avg_intel, SUM(CASE WHEN lifecycle_outlier_status='Unusually Fast' THEN 1 ELSE 0 END) as unusually_fast, SUM(CASE WHEN lifecycle_outlier_status='Statistical Outlier' THEN 1 ELSE 0 END) as stat_outliers, SUM(CASE WHEN lifecycle_outlier_status='Above Normal Range' THEN 1 ELSE 0 END) as above_normal, AVG(completion_probability) as avg_cp FROM jira__issue_intelligence_analytics WHERE project_name IN ('Data Analytics Delta', 'Mobile App Delta') GROUP BY project_name
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-061/attempt-01/sql/S22.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-061/attempt-01/sql/S22.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-061/attempt-01/results/S22.rows.jsonl)；完整：True；SHA256：`21a5b2537394e53a82a7ad61c57603c2dab59234654f088b08b33c98b0587aeb`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "jira__issue_intelligence_analytics", "kind": "base", "block": null, "base_tables": ["jira__issue_intelligence_analytics"]}] | [] | ["project_name"] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |
| B1 | SUM(CASE WHEN issue_type = 'Bug' THEN 1 ELSE 0 END) | [] | [{"table": "jira__issue_intelligence_analytics", "column": "issue_type"}] | False |
| B1 | AVG(regression_ratio) | [{"table": "jira__issue_intelligence_analytics", "column": "regression_ratio"}] | [] | False |
| B1 | AVG(lifecycle_quality_score) | [{"table": "jira__issue_intelligence_analytics", "column": "lifecycle_quality_score"}] | [] | False |
| B1 | AVG(total_risk_score) | [{"table": "jira__issue_intelligence_analytics", "column": "total_risk_score"}] | [] | False |
| B1 | AVG(intelligence_score) | [{"table": "jira__issue_intelligence_analytics", "column": "intelligence_score"}] | [] | False |
| B1 | SUM(CASE WHEN lifecycle_outlier_status = 'Unusually Fast' THEN 1 ELSE 0 END) | [] | [{"table": "jira__issue_intelligence_analytics", "column": "lifecycle_outlier_status"}] | False |
| B1 | SUM(CASE WHEN lifecycle_outlier_status = 'Statistical Outlier' THEN 1 ELSE 0 END) | [] | [{"table": "jira__issue_intelligence_analytics", "column": "lifecycle_outlier_status"}] | False |
| B1 | SUM(CASE WHEN lifecycle_outlier_status = 'Above Normal Range' THEN 1 ELSE 0 END) | [] | [{"table": "jira__issue_intelligence_analytics", "column": "lifecycle_outlier_status"}] | False |
| B1 | AVG(completion_probability) | [{"table": "jira__issue_intelligence_analytics", "column": "completion_probability"}] | [] | False |


## S23

类别 `data`；来源 `query_db`；调用 `85aa0181149945da9e07c3455c9306e7`；状态 `success`。

```sql
SELECT project_name, COUNT(*) as num_instances, AVG(avg_close_time_days) as avg_close_time, MIN(avg_close_time_days) as min_close, MAX(avg_close_time_days) as max_close, SUM(count_closed_issues) as total_closed, SUM(count_open_issues) as total_open FROM jira__project_enhanced GROUP BY project_name
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-061/attempt-01/sql/S23.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-061/attempt-01/sql/S23.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-061/attempt-01/results/S23.rows.jsonl)；完整：True；SHA256：`ef243b7b76ebb3d95e227a276dd68cbb0e804d0db5b0aba11b4204c479b833b2`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "jira__project_enhanced", "kind": "base", "block": null, "base_tables": ["jira__project_enhanced"]}] | [] | ["project_name"] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |
| B1 | AVG(avg_close_time_days) | [{"table": "jira__project_enhanced", "column": "avg_close_time_days"}] | [] | False |
| B1 | MIN(avg_close_time_days) | [{"table": "jira__project_enhanced", "column": "avg_close_time_days"}] | [] | False |
| B1 | MAX(avg_close_time_days) | [{"table": "jira__project_enhanced", "column": "avg_close_time_days"}] | [] | False |
| B1 | SUM(count_closed_issues) | [{"table": "jira__project_enhanced", "column": "count_closed_issues"}] | [] | False |
| B1 | SUM(count_open_issues) | [{"table": "jira__project_enhanced", "column": "count_open_issues"}] | [] | False |


## S24

类别 `data`；来源 `query_db`；调用 `faeff045e9d647f9945fdec043171e83`；状态 `success`。

```sql
SELECT project_name,
  COUNT(*) as total_issues,
  SUM(CASE WHEN issue_type='Bug' THEN 1 ELSE 0 END)*1.0/COUNT(*) as bug_rate,
  AVG(regression_ratio) as avg_regression_ratio,
  AVG(lifecycle_quality_score) as avg_lifecycle_quality,
  AVG(lifecycle_deviation_ratio) as avg_deviation_ratio,
  AVG(total_risk_score) as avg_risk_score,
  AVG(completion_probability) as avg_completion_prob,
  AVG(intelligence_score) as avg_intelligence,
  SUM(CASE WHEN lifecycle_outlier_status='Unusually Fast' THEN 1 ELSE 0 END)*1.0/COUNT(*) as unusually_fast_rate,
  SUM(CASE WHEN lifecycle_outlier_status='Statistical Outlier' THEN 1 ELSE 0 END)*1.0/COUNT(*) as stat_outlier_rate,
  SUM(CASE WHEN lifecycle_outlier_status='Above Normal Range' THEN 1 ELSE 0 END)*1.0/COUNT(*) as above_normal_rate,
  SUM(CASE WHEN current_status='Blocked' THEN 1 ELSE 0 END)*1.0/COUNT(*) as blocked_rate,
  SUM(CASE WHEN high_complexity_risk=1 THEN 1 ELSE 0 END)*1.0/COUNT(*) as high_complexity_rate,
  SUM(CASE WHEN is_active_sprint=1 THEN 1 ELSE 0 END)*1.0/COUNT(*) as active_sprint_rate,
  COUNT(DISTINCT assignee_name) as distinct_assignees,
  SUM(CASE WHEN assignment_risk_score > 0 THEN 1 ELSE 0 END)*1.0/COUNT(*) as assignment_risk_rate,
  SUM(CASE WHEN engagement_risk_score > 0 THEN 1 ELSE 0 END)*1.0/COUNT(*) as engagement_risk_rate,
  SUM(CASE WHEN age_risk_score > 0 THEN 1 ELSE 0 END)*1.0/COUNT(*) as age_risk_rate,
  SUM(CASE WHEN process_risk_score > 0 THEN 1 ELSE 0 END)*1.0/COUNT(*) as process_risk_rate,
  SUM(CASE WHEN deviation_risk_score > 0 THEN 1 ELSE 0 END)*1.0/COUNT(*) as deviation_risk_rate,
  SUM(CASE WHEN complexity_risk_score > 0 THEN 1 ELSE 0 END)*1.0/COUNT(*) as complexity_risk_rate
FROM jira__issue_intelligence_analytics
GROUP BY project_name
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-061/attempt-01/sql/S24.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-061/attempt-01/sql/S24.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-061/attempt-01/results/S24.rows.jsonl)；完整：True；SHA256：`8a0e34f9e70ec5cb1a36602c00cb0f7a8aefbbdb83a1bbf6a1171fcea7c6f924`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "jira__issue_intelligence_analytics", "kind": "base", "block": null, "base_tables": ["jira__issue_intelligence_analytics"]}] | [] | ["project_name"] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |
| B1 | AVG(regression_ratio) | [{"table": "jira__issue_intelligence_analytics", "column": "regression_ratio"}] | [] | False |
| B1 | AVG(lifecycle_quality_score) | [{"table": "jira__issue_intelligence_analytics", "column": "lifecycle_quality_score"}] | [] | False |
| B1 | AVG(lifecycle_deviation_ratio) | [{"table": "jira__issue_intelligence_analytics", "column": "lifecycle_deviation_ratio"}] | [] | False |
| B1 | AVG(total_risk_score) | [{"table": "jira__issue_intelligence_analytics", "column": "total_risk_score"}] | [] | False |
| B1 | AVG(completion_probability) | [{"table": "jira__issue_intelligence_analytics", "column": "completion_probability"}] | [] | False |
| B1 | AVG(intelligence_score) | [{"table": "jira__issue_intelligence_analytics", "column": "intelligence_score"}] | [] | False |
| B1 | COUNT(DISTINCT assignee_name) | [{"table": "jira__issue_intelligence_analytics", "column": "assignee_name"}] | [] | False |
| B1 | COUNT(*) | [] | [] | True |
| B1 | COUNT(*) | [] | [] | True |
| B1 | COUNT(*) | [] | [] | True |
| B1 | COUNT(*) | [] | [] | True |
| B1 | COUNT(*) | [] | [] | True |
| B1 | COUNT(*) | [] | [] | True |
| B1 | COUNT(*) | [] | [] | True |
| B1 | COUNT(*) | [] | [] | True |
| B1 | COUNT(*) | [] | [] | True |
| B1 | COUNT(*) | [] | [] | True |
| B1 | COUNT(*) | [] | [] | True |
| B1 | COUNT(*) | [] | [] | True |
| B1 | COUNT(*) | [] | [] | True |
| B1 | SUM(CASE WHEN issue_type = 'Bug' THEN 1 ELSE 0 END) | [] | [{"table": "jira__issue_intelligence_analytics", "column": "issue_type"}] | False |
| B1 | SUM(CASE WHEN lifecycle_outlier_status = 'Unusually Fast' THEN 1 ELSE 0 END) | [] | [{"table": "jira__issue_intelligence_analytics", "column": "lifecycle_outlier_status"}] | False |
| B1 | SUM(CASE WHEN lifecycle_outlier_status = 'Statistical Outlier' THEN 1 ELSE 0 END) | [] | [{"table": "jira__issue_intelligence_analytics", "column": "lifecycle_outlier_status"}] | False |
| B1 | SUM(CASE WHEN lifecycle_outlier_status = 'Above Normal Range' THEN 1 ELSE 0 END) | [] | [{"table": "jira__issue_intelligence_analytics", "column": "lifecycle_outlier_status"}] | False |
| B1 | SUM(CASE WHEN current_status = 'Blocked' THEN 1 ELSE 0 END) | [] | [{"table": "jira__issue_intelligence_analytics", "column": "current_status"}] | False |
| B1 | SUM(CASE WHEN high_complexity_risk = 1 THEN 1 ELSE 0 END) | [] | [{"table": "jira__issue_intelligence_analytics", "column": "high_complexity_risk"}] | False |
| B1 | SUM(CASE WHEN is_active_sprint = 1 THEN 1 ELSE 0 END) | [] | [{"table": "jira__issue_intelligence_analytics", "column": "is_active_sprint"}] | False |
| B1 | SUM(CASE WHEN assignment_risk_score > 0 THEN 1 ELSE 0 END) | [] | [{"table": "jira__issue_intelligence_analytics", "column": "assignment_risk_score"}] | False |
| B1 | SUM(CASE WHEN engagement_risk_score > 0 THEN 1 ELSE 0 END) | [] | [{"table": "jira__issue_intelligence_analytics", "column": "engagement_risk_score"}] | False |
| B1 | SUM(CASE WHEN age_risk_score > 0 THEN 1 ELSE 0 END) | [] | [{"table": "jira__issue_intelligence_analytics", "column": "age_risk_score"}] | False |
| B1 | SUM(CASE WHEN process_risk_score > 0 THEN 1 ELSE 0 END) | [] | [{"table": "jira__issue_intelligence_analytics", "column": "process_risk_score"}] | False |
| B1 | SUM(CASE WHEN deviation_risk_score > 0 THEN 1 ELSE 0 END) | [] | [{"table": "jira__issue_intelligence_analytics", "column": "deviation_risk_score"}] | False |
| B1 | SUM(CASE WHEN complexity_risk_score > 0 THEN 1 ELSE 0 END) | [] | [{"table": "jira__issue_intelligence_analytics", "column": "complexity_risk_score"}] | False |


## S25

类别 `data`；来源 `query_db`；调用 `3438ef11ca3a487c83f88c5279f266c8`；状态 `success`。

```sql
SELECT project_name,
  AVG(avg_close_time_days) as avg_close_time,
  MIN(avg_close_time_days) as min_close_time,
  MAX(avg_close_time_days) as max_close_time,
  SUM(count_closed_issues) as total_closed_issues,
  SUM(count_open_issues) as total_open_issues,
  AVG(avg_age_currently_open_days) as avg_age_open,
  AVG(median_close_time_days) as avg_median_close
FROM jira__project_enhanced
GROUP BY project_name
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-061/attempt-01/sql/S25.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-061/attempt-01/sql/S25.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-061/attempt-01/results/S25.rows.jsonl)；完整：True；SHA256：`7a21079b17b04c7132912aa35592be5cda96488f096b6f470a1019f140bea8a7`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "jira__project_enhanced", "kind": "base", "block": null, "base_tables": ["jira__project_enhanced"]}] | [] | ["project_name"] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | AVG(avg_close_time_days) | [{"table": "jira__project_enhanced", "column": "avg_close_time_days"}] | [] | False |
| B1 | MIN(avg_close_time_days) | [{"table": "jira__project_enhanced", "column": "avg_close_time_days"}] | [] | False |
| B1 | MAX(avg_close_time_days) | [{"table": "jira__project_enhanced", "column": "avg_close_time_days"}] | [] | False |
| B1 | SUM(count_closed_issues) | [{"table": "jira__project_enhanced", "column": "count_closed_issues"}] | [] | False |
| B1 | SUM(count_open_issues) | [{"table": "jira__project_enhanced", "column": "count_open_issues"}] | [] | False |
| B1 | AVG(avg_age_currently_open_days) | [{"table": "jira__project_enhanced", "column": "avg_age_currently_open_days"}] | [] | False |
| B1 | AVG(median_close_time_days) | [{"table": "jira__project_enhanced", "column": "median_close_time_days"}] | [] | False |


## S26

类别 `data`；来源 `query_db`；调用 `8c99e76336fe44a3ad1da9601839984c`；状态 `success`。

```sql
SELECT project_name,
  COUNT(*) as team_size,
  SUM(at_churn_risk) as churn_risk_count,
  SUM(inactive_recently) as inactive_count,
  AVG(consistency_percentage) as avg_consistency,
  AVG(resolution_rate_percentage) as avg_resolution_rate,
  AVG(overall_performance_score) as avg_performance,
  AVG(avg_sprint_completion_rate) as avg_sprint_completion,
  AVG(days_since_first_issue) as avg_tenure_days,
  AVG(estimate_accuracy_percentage) as avg_estimate_accuracy
FROM jira__team_performance_dashboard
GROUP BY project_name
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-061/attempt-01/sql/S26.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-061/attempt-01/sql/S26.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-061/attempt-01/results/S26.rows.jsonl)；完整：True；SHA256：`c4711bb8232922eb077d4f9ddeb6a361a63d7461c7118c71cf389ddc3091bb14`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "jira__team_performance_dashboard", "kind": "base", "block": null, "base_tables": ["jira__team_performance_dashboard"]}] | [] | ["project_name"] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |
| B1 | SUM(at_churn_risk) | [{"table": "jira__team_performance_dashboard", "column": "at_churn_risk"}] | [] | False |
| B1 | SUM(inactive_recently) | [{"table": "jira__team_performance_dashboard", "column": "inactive_recently"}] | [] | False |
| B1 | AVG(consistency_percentage) | [{"table": "jira__team_performance_dashboard", "column": "consistency_percentage"}] | [] | False |
| B1 | AVG(resolution_rate_percentage) | [{"table": "jira__team_performance_dashboard", "column": "resolution_rate_percentage"}] | [] | False |
| B1 | AVG(overall_performance_score) | [{"table": "jira__team_performance_dashboard", "column": "overall_performance_score"}] | [] | False |
| B1 | AVG(avg_sprint_completion_rate) | [{"table": "jira__team_performance_dashboard", "column": "avg_sprint_completion_rate"}] | [] | False |
| B1 | AVG(days_since_first_issue) | [{"table": "jira__team_performance_dashboard", "column": "days_since_first_issue"}] | [] | False |
| B1 | AVG(estimate_accuracy_percentage) | [{"table": "jira__team_performance_dashboard", "column": "estimate_accuracy_percentage"}] | [] | False |


## S27

类别 `data`；来源 `python`；调用 `cc68bd904fb544c2abcfd3baf5897734`；状态 `success`。

```sql
SELECT project_name, COUNT(*) as total_issues, SUM(CASE WHEN issue_type='Bug' THEN 1 ELSE 0 END)*1.0/COUNT(*) as bug_rate, AVG(regression_ratio) as avg_regression_ratio, AVG(lifecycle_quality_score) as avg_lifecycle_quality, AVG(lifecycle_deviation_ratio) as avg_deviation_ratio, AVG(total_risk_score) as avg_risk_score, AVG(completion_probability) as avg_completion_prob, AVG(intelligence_score) as avg_intelligence, SUM(CASE WHEN lifecycle_outlier_status='Unusually Fast' THEN 1 ELSE 0 END)*1.0/COUNT(*) as unusually_fast_rate, SUM(CASE WHEN lifecycle_outlier_status='Statistical Outlier' THEN 1 ELSE 0 END)*1.0/COUNT(*) as stat_outlier_rate, SUM(CASE WHEN lifecycle_outlier_status='Above Normal Range' THEN 1 ELSE 0 END)*1.0/COUNT(*) as above_normal_rate, SUM(CASE WHEN current_status='Blocked' THEN 1 ELSE 0 END)*1.0/COUNT(*) as blocked_rate, SUM(CASE WHEN high_complexity_risk=1 THEN 1 ELSE 0 END)*1.0/COUNT(*) as high_complexity_rate, COUNT(DISTINCT assignee_name) as distinct_assignees, SUM(CASE WHEN assignment_risk_score > 0 THEN 1 ELSE 0 END)*1.0/COUNT(*) as assignment_risk_rate, SUM(CASE WHEN engagement_risk_score > 0 THEN 1 ELSE 0 END)*1.0/COUNT(*) as engagement_risk_rate, SUM(CASE WHEN age_risk_score > 0 THEN 1 ELSE 0 END)*1.0/COUNT(*) as age_risk_rate, SUM(CASE WHEN process_risk_score > 0 THEN 1 ELSE 0 END)*1.0/COUNT(*) as process_risk_rate, SUM(CASE WHEN deviation_risk_score > 0 THEN 1 ELSE 0 END)*1.0/COUNT(*) as deviation_risk_rate, SUM(CASE WHEN complexity_risk_score > 0 THEN 1 ELSE 0 END)*1.0/COUNT(*) as complexity_risk_rate FROM jira__issue_intelligence_analytics GROUP BY project_name
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-061/attempt-01/sql/S27.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-061/attempt-01/sql/S27.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-061/attempt-01/results/S27.rows.jsonl)；完整：True；SHA256：`a342dfa8bd18fc3625a82444b2e3e7b9e38c9ea32eefdd918f7e92a906fc2aec`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "jira__issue_intelligence_analytics", "kind": "base", "block": null, "base_tables": ["jira__issue_intelligence_analytics"]}] | [] | ["project_name"] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |
| B1 | AVG(regression_ratio) | [{"table": "jira__issue_intelligence_analytics", "column": "regression_ratio"}] | [] | False |
| B1 | AVG(lifecycle_quality_score) | [{"table": "jira__issue_intelligence_analytics", "column": "lifecycle_quality_score"}] | [] | False |
| B1 | AVG(lifecycle_deviation_ratio) | [{"table": "jira__issue_intelligence_analytics", "column": "lifecycle_deviation_ratio"}] | [] | False |
| B1 | AVG(total_risk_score) | [{"table": "jira__issue_intelligence_analytics", "column": "total_risk_score"}] | [] | False |
| B1 | AVG(completion_probability) | [{"table": "jira__issue_intelligence_analytics", "column": "completion_probability"}] | [] | False |
| B1 | AVG(intelligence_score) | [{"table": "jira__issue_intelligence_analytics", "column": "intelligence_score"}] | [] | False |
| B1 | COUNT(DISTINCT assignee_name) | [{"table": "jira__issue_intelligence_analytics", "column": "assignee_name"}] | [] | False |
| B1 | COUNT(*) | [] | [] | True |
| B1 | COUNT(*) | [] | [] | True |
| B1 | COUNT(*) | [] | [] | True |
| B1 | COUNT(*) | [] | [] | True |
| B1 | COUNT(*) | [] | [] | True |
| B1 | COUNT(*) | [] | [] | True |
| B1 | COUNT(*) | [] | [] | True |
| B1 | COUNT(*) | [] | [] | True |
| B1 | COUNT(*) | [] | [] | True |
| B1 | COUNT(*) | [] | [] | True |
| B1 | COUNT(*) | [] | [] | True |
| B1 | COUNT(*) | [] | [] | True |
| B1 | SUM(CASE WHEN issue_type = 'Bug' THEN 1 ELSE 0 END) | [] | [{"table": "jira__issue_intelligence_analytics", "column": "issue_type"}] | False |
| B1 | SUM(CASE WHEN lifecycle_outlier_status = 'Unusually Fast' THEN 1 ELSE 0 END) | [] | [{"table": "jira__issue_intelligence_analytics", "column": "lifecycle_outlier_status"}] | False |
| B1 | SUM(CASE WHEN lifecycle_outlier_status = 'Statistical Outlier' THEN 1 ELSE 0 END) | [] | [{"table": "jira__issue_intelligence_analytics", "column": "lifecycle_outlier_status"}] | False |
| B1 | SUM(CASE WHEN lifecycle_outlier_status = 'Above Normal Range' THEN 1 ELSE 0 END) | [] | [{"table": "jira__issue_intelligence_analytics", "column": "lifecycle_outlier_status"}] | False |
| B1 | SUM(CASE WHEN current_status = 'Blocked' THEN 1 ELSE 0 END) | [] | [{"table": "jira__issue_intelligence_analytics", "column": "current_status"}] | False |
| B1 | SUM(CASE WHEN high_complexity_risk = 1 THEN 1 ELSE 0 END) | [] | [{"table": "jira__issue_intelligence_analytics", "column": "high_complexity_risk"}] | False |
| B1 | SUM(CASE WHEN assignment_risk_score > 0 THEN 1 ELSE 0 END) | [] | [{"table": "jira__issue_intelligence_analytics", "column": "assignment_risk_score"}] | False |
| B1 | SUM(CASE WHEN engagement_risk_score > 0 THEN 1 ELSE 0 END) | [] | [{"table": "jira__issue_intelligence_analytics", "column": "engagement_risk_score"}] | False |
| B1 | SUM(CASE WHEN age_risk_score > 0 THEN 1 ELSE 0 END) | [] | [{"table": "jira__issue_intelligence_analytics", "column": "age_risk_score"}] | False |
| B1 | SUM(CASE WHEN process_risk_score > 0 THEN 1 ELSE 0 END) | [] | [{"table": "jira__issue_intelligence_analytics", "column": "process_risk_score"}] | False |
| B1 | SUM(CASE WHEN deviation_risk_score > 0 THEN 1 ELSE 0 END) | [] | [{"table": "jira__issue_intelligence_analytics", "column": "deviation_risk_score"}] | False |
| B1 | SUM(CASE WHEN complexity_risk_score > 0 THEN 1 ELSE 0 END) | [] | [{"table": "jira__issue_intelligence_analytics", "column": "complexity_risk_score"}] | False |


## S28

类别 `data`；来源 `python`；调用 `cc68bd904fb544c2abcfd3baf5897734`；状态 `success`。

```sql
SELECT project_name, AVG(avg_close_time_days) as avg_close_time, MIN(avg_close_time_days) as min_close_time, MAX(avg_close_time_days) as max_close_time, SUM(count_closed_issues) as total_closed_issues, SUM(count_open_issues) as total_open_issues, AVG(avg_age_currently_open_days) as avg_age_open, AVG(median_close_time_days) as avg_median_close FROM jira__project_enhanced GROUP BY project_name
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-061/attempt-01/sql/S28.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-061/attempt-01/sql/S28.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-061/attempt-01/results/S28.rows.jsonl)；完整：True；SHA256：`7a21079b17b04c7132912aa35592be5cda96488f096b6f470a1019f140bea8a7`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "jira__project_enhanced", "kind": "base", "block": null, "base_tables": ["jira__project_enhanced"]}] | [] | ["project_name"] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | AVG(avg_close_time_days) | [{"table": "jira__project_enhanced", "column": "avg_close_time_days"}] | [] | False |
| B1 | MIN(avg_close_time_days) | [{"table": "jira__project_enhanced", "column": "avg_close_time_days"}] | [] | False |
| B1 | MAX(avg_close_time_days) | [{"table": "jira__project_enhanced", "column": "avg_close_time_days"}] | [] | False |
| B1 | SUM(count_closed_issues) | [{"table": "jira__project_enhanced", "column": "count_closed_issues"}] | [] | False |
| B1 | SUM(count_open_issues) | [{"table": "jira__project_enhanced", "column": "count_open_issues"}] | [] | False |
| B1 | AVG(avg_age_currently_open_days) | [{"table": "jira__project_enhanced", "column": "avg_age_currently_open_days"}] | [] | False |
| B1 | AVG(median_close_time_days) | [{"table": "jira__project_enhanced", "column": "median_close_time_days"}] | [] | False |


## S29

类别 `data`；来源 `python`；调用 `cc68bd904fb544c2abcfd3baf5897734`；状态 `success`。

```sql
SELECT project_name, COUNT(*) as team_size, SUM(at_churn_risk) as churn_risk_count, SUM(inactive_recently) as inactive_count, AVG(consistency_percentage) as avg_consistency, AVG(resolution_rate_percentage) as avg_resolution_rate, AVG(overall_performance_score) as avg_performance, AVG(avg_sprint_completion_rate) as avg_sprint_completion, AVG(days_since_first_issue) as avg_tenure_days, AVG(estimate_accuracy_percentage) as avg_estimate_accuracy FROM jira__team_performance_dashboard GROUP BY project_name
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-061/attempt-01/sql/S29.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-061/attempt-01/sql/S29.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-061/attempt-01/results/S29.rows.jsonl)；完整：True；SHA256：`c4711bb8232922eb077d4f9ddeb6a361a63d7461c7118c71cf389ddc3091bb14`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "jira__team_performance_dashboard", "kind": "base", "block": null, "base_tables": ["jira__team_performance_dashboard"]}] | [] | ["project_name"] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |
| B1 | SUM(at_churn_risk) | [{"table": "jira__team_performance_dashboard", "column": "at_churn_risk"}] | [] | False |
| B1 | SUM(inactive_recently) | [{"table": "jira__team_performance_dashboard", "column": "inactive_recently"}] | [] | False |
| B1 | AVG(consistency_percentage) | [{"table": "jira__team_performance_dashboard", "column": "consistency_percentage"}] | [] | False |
| B1 | AVG(resolution_rate_percentage) | [{"table": "jira__team_performance_dashboard", "column": "resolution_rate_percentage"}] | [] | False |
| B1 | AVG(overall_performance_score) | [{"table": "jira__team_performance_dashboard", "column": "overall_performance_score"}] | [] | False |
| B1 | AVG(avg_sprint_completion_rate) | [{"table": "jira__team_performance_dashboard", "column": "avg_sprint_completion_rate"}] | [] | False |
| B1 | AVG(days_since_first_issue) | [{"table": "jira__team_performance_dashboard", "column": "days_since_first_issue"}] | [] | False |
| B1 | AVG(estimate_accuracy_percentage) | [{"table": "jira__team_performance_dashboard", "column": "estimate_accuracy_percentage"}] | [] | False |


## S30

类别 `data`；来源 `python`；调用 `6ed0fd9d07fd42f48e94e27f8b475e6f`；状态 `success`。

```sql

    SELECT project_id, project_name, project_key, project_lead_user_name, 
           avg_close_time_days, median_close_time_days, count_closed_issues, count_open_issues,
           avg_age_currently_open_days, avg_assigned_close_time_days
    FROM jira__project_enhanced 
    WHERE avg_close_time_days < 15
    ORDER BY avg_close_time_days

```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-061/attempt-01/sql/S30.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-061/attempt-01/sql/S30.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-061/attempt-01/results/S30.rows.jsonl)；完整：True；SHA256：`16c980ba870c1ba9378300bf0b02ee7a9ae149c027fb4513aa154b4bb69c4a6a`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "jira__project_enhanced", "kind": "base", "block": null, "base_tables": ["jira__project_enhanced"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |


## S31

类别 `data`；来源 `python`；调用 `6ed0fd9d07fd42f48e94e27f8b475e6f`；状态 `success`。

```sql

    SELECT 
        issue_type,
        COUNT(*) as cnt,
        AVG(regression_ratio) as avg_regression,
        AVG(lifecycle_quality_score) as avg_lqs,
        AVG(total_lifecycle_days) as avg_lifecycle_days,
        AVG(lifecycle_deviation_ratio) as avg_deviation,
        SUM(CASE WHEN lifecycle_outlier_status='Unusually Fast' THEN 1 ELSE 0 END)*1.0/COUNT(*) as unusually_fast_rate,
        SUM(CASE WHEN lifecycle_outlier_status='Statistical Outlier' THEN 1 ELSE 0 END)*1.0/COUNT(*) as stat_outlier_rate,
        SUM(CASE WHEN lifecycle_outlier_status='Above Normal Range' THEN 1 ELSE 0 END)*1.0/COUNT(*) as above_normal_rate,
        SUM(CASE WHEN current_status='Blocked' THEN 1 ELSE 0 END)*1.0/COUNT(*) as blocked_rate,
        AVG(total_risk_score) as avg_risk
    FROM jira__issue_intelligence_analytics 
    WHERE project_name = 'Data Analytics Delta'
    GROUP BY issue_type
    ORDER BY cnt DESC

```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-061/attempt-01/sql/S31.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-061/attempt-01/sql/S31.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-061/attempt-01/results/S31.rows.jsonl)；完整：True；SHA256：`20d609acabc137aa6531e247161f1082ed8f3c7bd53d313ea575620a5287a1d2`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "jira__issue_intelligence_analytics", "kind": "base", "block": null, "base_tables": ["jira__issue_intelligence_analytics"]}] | [] | ["issue_type"] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |
| B1 | AVG(regression_ratio) | [{"table": "jira__issue_intelligence_analytics", "column": "regression_ratio"}] | [] | False |
| B1 | AVG(lifecycle_quality_score) | [{"table": "jira__issue_intelligence_analytics", "column": "lifecycle_quality_score"}] | [] | False |
| B1 | AVG(total_lifecycle_days) | [{"table": "jira__issue_intelligence_analytics", "column": "total_lifecycle_days"}] | [] | False |
| B1 | AVG(lifecycle_deviation_ratio) | [{"table": "jira__issue_intelligence_analytics", "column": "lifecycle_deviation_ratio"}] | [] | False |
| B1 | AVG(total_risk_score) | [{"table": "jira__issue_intelligence_analytics", "column": "total_risk_score"}] | [] | False |
| B1 | COUNT(*) | [] | [] | True |
| B1 | COUNT(*) | [] | [] | True |
| B1 | COUNT(*) | [] | [] | True |
| B1 | COUNT(*) | [] | [] | True |
| B1 | SUM(CASE WHEN lifecycle_outlier_status = 'Unusually Fast' THEN 1 ELSE 0 END) | [] | [{"table": "jira__issue_intelligence_analytics", "column": "lifecycle_outlier_status"}] | False |
| B1 | SUM(CASE WHEN lifecycle_outlier_status = 'Statistical Outlier' THEN 1 ELSE 0 END) | [] | [{"table": "jira__issue_intelligence_analytics", "column": "lifecycle_outlier_status"}] | False |
| B1 | SUM(CASE WHEN lifecycle_outlier_status = 'Above Normal Range' THEN 1 ELSE 0 END) | [] | [{"table": "jira__issue_intelligence_analytics", "column": "lifecycle_outlier_status"}] | False |
| B1 | SUM(CASE WHEN current_status = 'Blocked' THEN 1 ELSE 0 END) | [] | [{"table": "jira__issue_intelligence_analytics", "column": "current_status"}] | False |


## S32

类别 `data`；来源 `python`；调用 `6ed0fd9d07fd42f48e94e27f8b475e6f`；状态 `success`。

```sql

    SELECT 
        issue_type,
        COUNT(*) as cnt,
        AVG(regression_ratio) as avg_regression,
        AVG(lifecycle_quality_score) as avg_lqs,
        AVG(total_lifecycle_days) as avg_lifecycle_days,
        AVG(lifecycle_deviation_ratio) as avg_deviation,
        SUM(CASE WHEN lifecycle_outlier_status='Unusually Fast' THEN 1 ELSE 0 END)*1.0/COUNT(*) as unusually_fast_rate,
        SUM(CASE WHEN lifecycle_outlier_status='Statistical Outlier' THEN 1 ELSE 0 END)*1.0/COUNT(*) as stat_outlier_rate,
        SUM(CASE WHEN lifecycle_outlier_status='Above Normal Range' THEN 1 ELSE 0 END)*1.0/COUNT(*) as above_normal_rate,
        SUM(CASE WHEN current_status='Blocked' THEN 1 ELSE 0 END)*1.0/COUNT(*) as blocked_rate,
        AVG(total_risk_score) as avg_risk
    FROM jira__issue_intelligence_analytics 
    WHERE project_name = 'Mobile App Delta'
    GROUP BY issue_type
    ORDER BY cnt DESC

```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-061/attempt-01/sql/S32.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-061/attempt-01/sql/S32.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-061/attempt-01/results/S32.rows.jsonl)；完整：True；SHA256：`a5ca59ea6e39201ce14718439ae39f49d3bcf4c6f228808f13fa1d6428d54edf`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "jira__issue_intelligence_analytics", "kind": "base", "block": null, "base_tables": ["jira__issue_intelligence_analytics"]}] | [] | ["issue_type"] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |
| B1 | AVG(regression_ratio) | [{"table": "jira__issue_intelligence_analytics", "column": "regression_ratio"}] | [] | False |
| B1 | AVG(lifecycle_quality_score) | [{"table": "jira__issue_intelligence_analytics", "column": "lifecycle_quality_score"}] | [] | False |
| B1 | AVG(total_lifecycle_days) | [{"table": "jira__issue_intelligence_analytics", "column": "total_lifecycle_days"}] | [] | False |
| B1 | AVG(lifecycle_deviation_ratio) | [{"table": "jira__issue_intelligence_analytics", "column": "lifecycle_deviation_ratio"}] | [] | False |
| B1 | AVG(total_risk_score) | [{"table": "jira__issue_intelligence_analytics", "column": "total_risk_score"}] | [] | False |
| B1 | COUNT(*) | [] | [] | True |
| B1 | COUNT(*) | [] | [] | True |
| B1 | COUNT(*) | [] | [] | True |
| B1 | COUNT(*) | [] | [] | True |
| B1 | SUM(CASE WHEN lifecycle_outlier_status = 'Unusually Fast' THEN 1 ELSE 0 END) | [] | [{"table": "jira__issue_intelligence_analytics", "column": "lifecycle_outlier_status"}] | False |
| B1 | SUM(CASE WHEN lifecycle_outlier_status = 'Statistical Outlier' THEN 1 ELSE 0 END) | [] | [{"table": "jira__issue_intelligence_analytics", "column": "lifecycle_outlier_status"}] | False |
| B1 | SUM(CASE WHEN lifecycle_outlier_status = 'Above Normal Range' THEN 1 ELSE 0 END) | [] | [{"table": "jira__issue_intelligence_analytics", "column": "lifecycle_outlier_status"}] | False |
| B1 | SUM(CASE WHEN current_status = 'Blocked' THEN 1 ELSE 0 END) | [] | [{"table": "jira__issue_intelligence_analytics", "column": "current_status"}] | False |


## S33

类别 `data`；来源 `python`；调用 `6ed0fd9d07fd42f48e94e27f8b475e6f`；状态 `success`。

```sql

    SELECT 
        AVG(regression_ratio) as avg_regression,
        AVG(lifecycle_quality_score) as avg_lqs,
        AVG(lifecycle_deviation_ratio) as avg_deviation,
        AVG(total_risk_score) as avg_risk,
        AVG(intelligence_score) as avg_intel,
        AVG(completion_probability) as avg_cp
    FROM jira__issue_intelligence_analytics

```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-061/attempt-01/sql/S33.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-061/attempt-01/sql/S33.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-061/attempt-01/results/S33.rows.jsonl)；完整：True；SHA256：`ae92b0d176008834db5285f287ac3cd45cec5c95a960326d108d87c9e19203bc`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "jira__issue_intelligence_analytics", "kind": "base", "block": null, "base_tables": ["jira__issue_intelligence_analytics"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | AVG(regression_ratio) | [{"table": "jira__issue_intelligence_analytics", "column": "regression_ratio"}] | [] | False |
| B1 | AVG(lifecycle_quality_score) | [{"table": "jira__issue_intelligence_analytics", "column": "lifecycle_quality_score"}] | [] | False |
| B1 | AVG(lifecycle_deviation_ratio) | [{"table": "jira__issue_intelligence_analytics", "column": "lifecycle_deviation_ratio"}] | [] | False |
| B1 | AVG(total_risk_score) | [{"table": "jira__issue_intelligence_analytics", "column": "total_risk_score"}] | [] | False |
| B1 | AVG(intelligence_score) | [{"table": "jira__issue_intelligence_analytics", "column": "intelligence_score"}] | [] | False |
| B1 | AVG(completion_probability) | [{"table": "jira__issue_intelligence_analytics", "column": "completion_probability"}] | [] | False |


## S34

类别 `data`；来源 `python`；调用 `6ed0fd9d07fd42f48e94e27f8b475e6f`；状态 `success`。

```sql

    SELECT project_name,
        AVG(regression_ratio) as avg_regression,
        AVG(lifecycle_quality_score) as avg_lqs,
        AVG(lifecycle_deviation_ratio) as avg_deviation,
        AVG(total_risk_score) as avg_risk,
        AVG(intelligence_score) as avg_intel,
        AVG(completion_probability) as avg_cp,
        SUM(CASE WHEN lifecycle_outlier_status='Unusually Fast' THEN 1 ELSE 0 END)*1.0/COUNT(*) as unusually_fast_rate,
        SUM(CASE WHEN lifecycle_outlier_status='Statistical Outlier' THEN 1 ELSE 0 END)*1.0/COUNT(*) as stat_outlier_rate,
        SUM(CASE WHEN lifecycle_outlier_status='Above Normal Range' THEN 1 ELSE 0 END)*1.0/COUNT(*) as above_normal_rate,
        SUM(CASE WHEN current_status='Blocked' THEN 1 ELSE 0 END)*1.0/COUNT(*) as blocked_rate,
        SUM(CASE WHEN issue_type='Bug' THEN 1 ELSE 0 END)*1.0/COUNT(*) as bug_rate
    FROM jira__issue_intelligence_analytics
    GROUP BY project_name

```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-061/attempt-01/sql/S34.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-061/attempt-01/sql/S34.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-061/attempt-01/results/S34.rows.jsonl)；完整：True；SHA256：`4aef329a18437af0f90d789c5de2a708e882cfba02e81162f19743a771650f26`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "jira__issue_intelligence_analytics", "kind": "base", "block": null, "base_tables": ["jira__issue_intelligence_analytics"]}] | [] | ["project_name"] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | AVG(regression_ratio) | [{"table": "jira__issue_intelligence_analytics", "column": "regression_ratio"}] | [] | False |
| B1 | AVG(lifecycle_quality_score) | [{"table": "jira__issue_intelligence_analytics", "column": "lifecycle_quality_score"}] | [] | False |
| B1 | AVG(lifecycle_deviation_ratio) | [{"table": "jira__issue_intelligence_analytics", "column": "lifecycle_deviation_ratio"}] | [] | False |
| B1 | AVG(total_risk_score) | [{"table": "jira__issue_intelligence_analytics", "column": "total_risk_score"}] | [] | False |
| B1 | AVG(intelligence_score) | [{"table": "jira__issue_intelligence_analytics", "column": "intelligence_score"}] | [] | False |
| B1 | AVG(completion_probability) | [{"table": "jira__issue_intelligence_analytics", "column": "completion_probability"}] | [] | False |
| B1 | COUNT(*) | [] | [] | True |
| B1 | COUNT(*) | [] | [] | True |
| B1 | COUNT(*) | [] | [] | True |
| B1 | COUNT(*) | [] | [] | True |
| B1 | COUNT(*) | [] | [] | True |
| B1 | SUM(CASE WHEN lifecycle_outlier_status = 'Unusually Fast' THEN 1 ELSE 0 END) | [] | [{"table": "jira__issue_intelligence_analytics", "column": "lifecycle_outlier_status"}] | False |
| B1 | SUM(CASE WHEN lifecycle_outlier_status = 'Statistical Outlier' THEN 1 ELSE 0 END) | [] | [{"table": "jira__issue_intelligence_analytics", "column": "lifecycle_outlier_status"}] | False |
| B1 | SUM(CASE WHEN lifecycle_outlier_status = 'Above Normal Range' THEN 1 ELSE 0 END) | [] | [{"table": "jira__issue_intelligence_analytics", "column": "lifecycle_outlier_status"}] | False |
| B1 | SUM(CASE WHEN current_status = 'Blocked' THEN 1 ELSE 0 END) | [] | [{"table": "jira__issue_intelligence_analytics", "column": "current_status"}] | False |
| B1 | SUM(CASE WHEN issue_type = 'Bug' THEN 1 ELSE 0 END) | [] | [{"table": "jira__issue_intelligence_analytics", "column": "issue_type"}] | False |


## S35

类别 `data`；来源 `python`；调用 `6ed0fd9d07fd42f48e94e27f8b475e6f`；状态 `success`。

```sql

    SELECT project_name, AVG(avg_close_time_days) as avg_close, MIN(avg_close_time_days) as min_close
    FROM jira__project_enhanced
    GROUP BY project_name

```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-061/attempt-01/sql/S35.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-061/attempt-01/sql/S35.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-061/attempt-01/results/S35.rows.jsonl)；完整：True；SHA256：`1f6c74edd07b7cfbf9c3e6eb1dead6d39a1752a85121e667b3815ec5fc945867`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "jira__project_enhanced", "kind": "base", "block": null, "base_tables": ["jira__project_enhanced"]}] | [] | ["project_name"] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | AVG(avg_close_time_days) | [{"table": "jira__project_enhanced", "column": "avg_close_time_days"}] | [] | False |
| B1 | MIN(avg_close_time_days) | [{"table": "jira__project_enhanced", "column": "avg_close_time_days"}] | [] | False |


## S36

类别 `data`；来源 `python`；调用 `6ed0fd9d07fd42f48e94e27f8b475e6f`；状态 `success`。

```sql

    SELECT project_name, 
        COUNT(*) as team_size,
        SUM(at_churn_risk) as churn_risk,
        AVG(consistency_percentage) as avg_consistency,
        AVG(avg_sprint_completion_rate) as avg_sprint_completion,
        AVG(days_since_first_issue) as avg_tenure,
        AVG(estimate_accuracy_percentage) as avg_estimate_accuracy,
        AVG(overall_performance_score) as avg_performance
    FROM jira__team_performance_dashboard
    GROUP BY project_name

```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-061/attempt-01/sql/S36.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-061/attempt-01/sql/S36.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-061/attempt-01/results/S36.rows.jsonl)；完整：True；SHA256：`38bdea07adbd3ec4d52eed62e99a605695e0b681193b814e37b213fbfdaf51d9`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "jira__team_performance_dashboard", "kind": "base", "block": null, "base_tables": ["jira__team_performance_dashboard"]}] | [] | ["project_name"] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |
| B1 | SUM(at_churn_risk) | [{"table": "jira__team_performance_dashboard", "column": "at_churn_risk"}] | [] | False |
| B1 | AVG(consistency_percentage) | [{"table": "jira__team_performance_dashboard", "column": "consistency_percentage"}] | [] | False |
| B1 | AVG(avg_sprint_completion_rate) | [{"table": "jira__team_performance_dashboard", "column": "avg_sprint_completion_rate"}] | [] | False |
| B1 | AVG(days_since_first_issue) | [{"table": "jira__team_performance_dashboard", "column": "days_since_first_issue"}] | [] | False |
| B1 | AVG(estimate_accuracy_percentage) | [{"table": "jira__team_performance_dashboard", "column": "estimate_accuracy_percentage"}] | [] | False |
| B1 | AVG(overall_performance_score) | [{"table": "jira__team_performance_dashboard", "column": "overall_performance_score"}] | [] | False |


## S37

类别 `data`；来源 `query_db`；调用 `8328fbdc01554a949c6f569a23a7e93d`；状态 `success`。

```sql
SELECT project_id, project_name, avg_close_time_days, median_close_time_days, count_closed_issues, count_open_issues FROM jira__project_enhanced WHERE project_name IN ('Data Analytics Delta', 'Mobile App Delta') ORDER BY project_name, avg_close_time_days
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-061/attempt-01/sql/S37.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-061/attempt-01/sql/S37.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-061/attempt-01/results/S37.rows.jsonl)；完整：True；SHA256：`f71d20c6e49af20ff3d776d540d8864e6d54ddb117eee3e6ac227e50aacc1d6b`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "jira__project_enhanced", "kind": "base", "block": null, "base_tables": ["jira__project_enhanced"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |


## S38

类别 `data`；来源 `query_db`；调用 `f95dba20948b4e02b4ac82e17367791b`；状态 `success`。

```sql
SELECT regression_ratio, COUNT(*) as cnt FROM jira__issue_intelligence_analytics GROUP BY regression_ratio ORDER BY regression_ratio
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-061/attempt-01/sql/S38.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-061/attempt-01/sql/S38.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-061/attempt-01/results/S38.rows.jsonl)；完整：True；SHA256：`8942396f115615e22b499dea790b174794513712caa7b507f82153682284557a`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "jira__issue_intelligence_analytics", "kind": "base", "block": null, "base_tables": ["jira__issue_intelligence_analytics"]}] | [] | ["regression_ratio"] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |


## S39

类别 `data`；来源 `python`；调用 `db1c0f4e0dce423aa46e4b005ac7c55c`；状态 `success`。

```sql

    SELECT 
        CASE WHEN regression_ratio = 0.0 THEN 'No Regression'
             WHEN regression_ratio = 0.1 THEN 'Some Regression'
             ELSE 'High Regression'
        END as regression_level,
        COUNT(*) as cnt
    FROM jira__issue_intelligence_analytics 
    WHERE project_name IN ('Data Analytics Delta', 'Mobile App Delta')
    GROUP BY regression_ratio
    ORDER BY regression_ratio

```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-061/attempt-01/sql/S39.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-061/attempt-01/sql/S39.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-061/attempt-01/results/S39.rows.jsonl)；完整：True；SHA256：`a4213b9cf55a052a298f5d84a016d17167e1462348d59aef70d886c13c802d27`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "jira__issue_intelligence_analytics", "kind": "base", "block": null, "base_tables": ["jira__issue_intelligence_analytics"]}] | [] | ["regression_ratio"] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |


## S40

类别 `data`；来源 `python`；调用 `db1c0f4e0dce423aa46e4b005ac7c55c`；状态 `success`。

```sql

    SELECT 
        CASE WHEN regression_ratio = 0.0 THEN 'No Regression'
             WHEN regression_ratio = 0.1 THEN 'Some Regression'
             ELSE 'High Regression'
        END as regression_level,
        COUNT(*) as cnt
    FROM jira__issue_intelligence_analytics 
    WHERE project_name NOT IN ('Data Analytics Delta', 'Mobile App Delta')
    GROUP BY regression_ratio
    ORDER BY regression_ratio

```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-061/attempt-01/sql/S40.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-061/attempt-01/sql/S40.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-061/attempt-01/results/S40.rows.jsonl)；完整：True；SHA256：`9f2d6529c9bf5aff7a055296f67768cf0332b6c6372b36c3b6c2646402526666`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "jira__issue_intelligence_analytics", "kind": "base", "block": null, "base_tables": ["jira__issue_intelligence_analytics"]}] | [] | ["regression_ratio"] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |


## S41

类别 `data`；来源 `python`；调用 `b357b635b7b14b1586a4550069ba7b38`；状态 `success`。

```sql

    SELECT 
        regression_ratio,
        COUNT(*) as cnt
    FROM jira__issue_intelligence_analytics 
    WHERE project_name IN ('Data Analytics Delta', 'Mobile App Delta')
    GROUP BY regression_ratio
    ORDER BY regression_ratio

```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-061/attempt-01/sql/S41.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-061/attempt-01/sql/S41.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-061/attempt-01/results/S41.rows.jsonl)；完整：True；SHA256：`f3407517ad0c7214fee3077887803937de98b0b2aeed2bab5f7cff6a87f86993`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "jira__issue_intelligence_analytics", "kind": "base", "block": null, "base_tables": ["jira__issue_intelligence_analytics"]}] | [] | ["regression_ratio"] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |


## S42

类别 `data`；来源 `python`；调用 `b357b635b7b14b1586a4550069ba7b38`；状态 `success`。

```sql

    SELECT 
        regression_ratio,
        COUNT(*) as cnt
    FROM jira__issue_intelligence_analytics 
    WHERE project_name NOT IN ('Data Analytics Delta', 'Mobile App Delta')
    GROUP BY regression_ratio
    ORDER BY regression_ratio

```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-061/attempt-01/sql/S42.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-061/attempt-01/sql/S42.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-061/attempt-01/results/S42.rows.jsonl)；完整：True；SHA256：`145aec15b2e41a4f7473abd6bf78817802785e5ee8b9e30494035155c47a59fe`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "jira__issue_intelligence_analytics", "kind": "base", "block": null, "base_tables": ["jira__issue_intelligence_analytics"]}] | [] | ["regression_ratio"] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |


## S43

类别 `data`；来源 `python`；调用 `b357b635b7b14b1586a4550069ba7b38`；状态 `success`。

```sql

    SELECT 
        CASE WHEN project_name IN ('Data Analytics Delta', 'Mobile App Delta') THEN 'Fast Projects' ELSE 'Other Projects' END as project_group,
        AVG(age_risk_score) as avg_age_risk,
        AVG(process_risk_score) as avg_process_risk,
        AVG(complexity_risk_score) as avg_complexity_risk,
        AVG(engagement_risk_score) as avg_engagement_risk,
        AVG(assignment_risk_score) as avg_assignment_risk,
        AVG(deviation_risk_score) as avg_deviation_risk,
        AVG(total_risk_score) as avg_total_risk,
        AVG(total_opportunity_score) as avg_opportunity
    FROM jira__issue_intelligence_analytics
    GROUP BY project_group

```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-061/attempt-01/sql/S43.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-061/attempt-01/sql/S43.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-061/attempt-01/results/S43.rows.jsonl)；完整：True；SHA256：`643a974e3b38095fe9c22af68ddd77dc7996db6f618f0ae4ddfa6468fc09e47c`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "jira__issue_intelligence_analytics", "kind": "base", "block": null, "base_tables": ["jira__issue_intelligence_analytics"]}] | [] | ["CASE WHEN project_name IN ('Data Analytics Delta', 'Mobile App Delta') THEN 'Fast Projects' ELSE 'Other Projects' END"] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | AVG(age_risk_score) | [{"table": "jira__issue_intelligence_analytics", "column": "age_risk_score"}] | [] | False |
| B1 | AVG(process_risk_score) | [{"table": "jira__issue_intelligence_analytics", "column": "process_risk_score"}] | [] | False |
| B1 | AVG(complexity_risk_score) | [{"table": "jira__issue_intelligence_analytics", "column": "complexity_risk_score"}] | [] | False |
| B1 | AVG(engagement_risk_score) | [{"table": "jira__issue_intelligence_analytics", "column": "engagement_risk_score"}] | [] | False |
| B1 | AVG(assignment_risk_score) | [{"table": "jira__issue_intelligence_analytics", "column": "assignment_risk_score"}] | [] | False |
| B1 | AVG(deviation_risk_score) | [{"table": "jira__issue_intelligence_analytics", "column": "deviation_risk_score"}] | [] | False |
| B1 | AVG(total_risk_score) | [{"table": "jira__issue_intelligence_analytics", "column": "total_risk_score"}] | [] | False |
| B1 | AVG(total_opportunity_score) | [{"table": "jira__issue_intelligence_analytics", "column": "total_opportunity_score"}] | [] | False |


## S44

类别 `data`；来源 `python`；调用 `b357b635b7b14b1586a4550069ba7b38`；状态 `success`。

```sql

    SELECT lifecycle_quality_score, COUNT(*) as cnt
    FROM jira__issue_intelligence_analytics
    GROUP BY lifecycle_quality_score
    ORDER BY lifecycle_quality_score

```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-061/attempt-01/sql/S44.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-061/attempt-01/sql/S44.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-061/attempt-01/results/S44.rows.jsonl)；完整：True；SHA256：`2d6b1f876663d12795da8f87469cfa1d3657507bd4ccff288f3a97512cf75e71`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "jira__issue_intelligence_analytics", "kind": "base", "block": null, "base_tables": ["jira__issue_intelligence_analytics"]}] | [] | ["lifecycle_quality_score"] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |


## S45

类别 `data`；来源 `python`；调用 `b357b635b7b14b1586a4550069ba7b38`；状态 `success`。

```sql

    SELECT 
        CASE WHEN project_name IN ('Data Analytics Delta', 'Mobile App Delta') THEN 'Fast Projects' ELSE 'Other Projects' END as project_group,
        lifecycle_quality_score,
        COUNT(*) as cnt
    FROM jira__issue_intelligence_analytics
    GROUP BY project_group, lifecycle_quality_score
    ORDER BY project_group, lifecycle_quality_score

```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-061/attempt-01/sql/S45.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-061/attempt-01/sql/S45.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-061/attempt-01/results/S45.rows.jsonl)；完整：True；SHA256：`29c764fa790f857f7c8067a42e2b902d8b8293695be0ac119bbf53f47193342d`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "jira__issue_intelligence_analytics", "kind": "base", "block": null, "base_tables": ["jira__issue_intelligence_analytics"]}] | [] | ["CASE WHEN project_name IN ('Data Analytics Delta', 'Mobile App Delta') THEN 'Fast Projects' ELSE 'Other Projects' END", "lifecycle_quality_score"] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |


## S46

类别 `data`；来源 `python`；调用 `b357b635b7b14b1586a4550069ba7b38`；状态 `success`。

```sql

    SELECT 
        project_name,
        AVG(age_risk_score) as avg_age_risk,
        AVG(process_risk_score) as avg_process_risk,
        AVG(engagement_risk_score) as avg_engagement_risk,
        AVG(assignment_risk_score) as avg_assignment_risk,
        AVG(deviation_risk_score) as avg_deviation_risk,
        AVG(complexity_risk_score) as avg_complexity_risk,
        AVG(total_risk_score) as avg_total_risk,
        AVG(total_opportunity_score) as avg_opportunity,
        AVG(intelligence_score) as avg_intel,
        AVG(collaboration_opportunity_score) as avg_collab,
        AVG(efficiency_opportunity_score) as avg_efficiency,
        AVG(process_opportunity_score) as avg_process_opp
    FROM jira__issue_intelligence_analytics
    WHERE project_name IN ('Data Analytics Delta', 'Mobile App Delta')
    GROUP BY project_name

```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-061/attempt-01/sql/S46.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-061/attempt-01/sql/S46.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-061/attempt-01/results/S46.rows.jsonl)；完整：True；SHA256：`cd0719a3f4301a2fbc3807dc6d48a4d68f67b02663eecd4c6f779b67e80868d3`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "jira__issue_intelligence_analytics", "kind": "base", "block": null, "base_tables": ["jira__issue_intelligence_analytics"]}] | [] | ["project_name"] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | AVG(age_risk_score) | [{"table": "jira__issue_intelligence_analytics", "column": "age_risk_score"}] | [] | False |
| B1 | AVG(process_risk_score) | [{"table": "jira__issue_intelligence_analytics", "column": "process_risk_score"}] | [] | False |
| B1 | AVG(engagement_risk_score) | [{"table": "jira__issue_intelligence_analytics", "column": "engagement_risk_score"}] | [] | False |
| B1 | AVG(assignment_risk_score) | [{"table": "jira__issue_intelligence_analytics", "column": "assignment_risk_score"}] | [] | False |
| B1 | AVG(deviation_risk_score) | [{"table": "jira__issue_intelligence_analytics", "column": "deviation_risk_score"}] | [] | False |
| B1 | AVG(complexity_risk_score) | [{"table": "jira__issue_intelligence_analytics", "column": "complexity_risk_score"}] | [] | False |
| B1 | AVG(total_risk_score) | [{"table": "jira__issue_intelligence_analytics", "column": "total_risk_score"}] | [] | False |
| B1 | AVG(total_opportunity_score) | [{"table": "jira__issue_intelligence_analytics", "column": "total_opportunity_score"}] | [] | False |
| B1 | AVG(intelligence_score) | [{"table": "jira__issue_intelligence_analytics", "column": "intelligence_score"}] | [] | False |
| B1 | AVG(collaboration_opportunity_score) | [{"table": "jira__issue_intelligence_analytics", "column": "collaboration_opportunity_score"}] | [] | False |
| B1 | AVG(efficiency_opportunity_score) | [{"table": "jira__issue_intelligence_analytics", "column": "efficiency_opportunity_score"}] | [] | False |
| B1 | AVG(process_opportunity_score) | [{"table": "jira__issue_intelligence_analytics", "column": "process_opportunity_score"}] | [] | False |


## S47

类别 `data`；来源 `python`；调用 `b357b635b7b14b1586a4550069ba7b38`；状态 `success`。

```sql

    SELECT 
        AVG(age_risk_score) as avg_age_risk,
        AVG(process_risk_score) as avg_process_risk,
        AVG(engagement_risk_score) as avg_engagement_risk,
        AVG(assignment_risk_score) as avg_assignment_risk,
        AVG(deviation_risk_score) as avg_deviation_risk,
        AVG(complexity_risk_score) as avg_complexity_risk,
        AVG(total_risk_score) as avg_total_risk,
        AVG(total_opportunity_score) as avg_opportunity,
        AVG(collaboration_opportunity_score) as avg_collab,
        AVG(efficiency_opportunity_score) as avg_efficiency,
        AVG(process_opportunity_score) as avg_process_opp
    FROM jira__issue_intelligence_analytics
    WHERE project_name NOT IN ('Data Analytics Delta', 'Mobile App Delta')

```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-061/attempt-01/sql/S47.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-061/attempt-01/sql/S47.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-061/attempt-01/results/S47.rows.jsonl)；完整：True；SHA256：`248f4cc6f67e982a177a18678040ffd9c92ad816678bba058c4bcfaa78af75a3`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "jira__issue_intelligence_analytics", "kind": "base", "block": null, "base_tables": ["jira__issue_intelligence_analytics"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | AVG(age_risk_score) | [{"table": "jira__issue_intelligence_analytics", "column": "age_risk_score"}] | [] | False |
| B1 | AVG(process_risk_score) | [{"table": "jira__issue_intelligence_analytics", "column": "process_risk_score"}] | [] | False |
| B1 | AVG(engagement_risk_score) | [{"table": "jira__issue_intelligence_analytics", "column": "engagement_risk_score"}] | [] | False |
| B1 | AVG(assignment_risk_score) | [{"table": "jira__issue_intelligence_analytics", "column": "assignment_risk_score"}] | [] | False |
| B1 | AVG(deviation_risk_score) | [{"table": "jira__issue_intelligence_analytics", "column": "deviation_risk_score"}] | [] | False |
| B1 | AVG(complexity_risk_score) | [{"table": "jira__issue_intelligence_analytics", "column": "complexity_risk_score"}] | [] | False |
| B1 | AVG(total_risk_score) | [{"table": "jira__issue_intelligence_analytics", "column": "total_risk_score"}] | [] | False |
| B1 | AVG(total_opportunity_score) | [{"table": "jira__issue_intelligence_analytics", "column": "total_opportunity_score"}] | [] | False |
| B1 | AVG(collaboration_opportunity_score) | [{"table": "jira__issue_intelligence_analytics", "column": "collaboration_opportunity_score"}] | [] | False |
| B1 | AVG(efficiency_opportunity_score) | [{"table": "jira__issue_intelligence_analytics", "column": "efficiency_opportunity_score"}] | [] | False |
| B1 | AVG(process_opportunity_score) | [{"table": "jira__issue_intelligence_analytics", "column": "process_opportunity_score"}] | [] | False |


## S48

类别 `data`；来源 `python`；调用 `91971f8f7e084f49b00ff2ec5dc0ec57`；状态 `success`。

```sql

    SELECT user_display_name, total_assigned_issues, resolved_issues, at_churn_risk,
           consistency_percentage, avg_resolution_days, bug_issues, overall_performance_score,
           estimate_accuracy_percentage
    FROM jira__team_performance_dashboard
    WHERE project_name = 'Data Analytics Delta'
    ORDER BY at_churn_risk DESC

```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-061/attempt-01/sql/S48.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-061/attempt-01/sql/S48.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-061/attempt-01/results/S48.rows.jsonl)；完整：True；SHA256：`a1a9b4416130ab3358c1704492d7bd5a2d6dbccfa53d24baffa56212f5920813`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "jira__team_performance_dashboard", "kind": "base", "block": null, "base_tables": ["jira__team_performance_dashboard"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |


## S49

类别 `data`；来源 `python`；调用 `91971f8f7e084f49b00ff2ec5dc0ec57`；状态 `success`。

```sql

    SELECT user_display_name, total_assigned_issues, resolved_issues, at_churn_risk,
           consistency_percentage, avg_resolution_days, bug_issues, overall_performance_score,
           estimate_accuracy_percentage
    FROM jira__team_performance_dashboard
    WHERE project_name = 'Mobile App Delta'
    ORDER BY at_churn_risk DESC

```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-061/attempt-01/sql/S49.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-061/attempt-01/sql/S49.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-061/attempt-01/results/S49.rows.jsonl)；完整：True；SHA256：`df8c17a35a2c9017a3ba69fb258c1f1c00e880779a2b76ed694c2e94657e259f`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "jira__team_performance_dashboard", "kind": "base", "block": null, "base_tables": ["jira__team_performance_dashboard"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |


## S50

类别 `data`；来源 `python`；调用 `91971f8f7e084f49b00ff2ec5dc0ec57`；状态 `success`。

```sql

        SELECT total_assigned_issues, at_churn_risk
        FROM jira__team_performance_dashboard
        WHERE project_name = 'API Gateway V3'
    
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-061/attempt-01/sql/S50.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-061/attempt-01/sql/S50.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-061/attempt-01/results/S50.rows.jsonl)；完整：True；SHA256：`b3c972c887e7defa58c2ed0ea96e4adc5a7f3dde34df272af5b1cdeb0668b533`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "jira__team_performance_dashboard", "kind": "base", "block": null, "base_tables": ["jira__team_performance_dashboard"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |


## S51

类别 `data`；来源 `python`；调用 `91971f8f7e084f49b00ff2ec5dc0ec57`；状态 `success`。

```sql

        SELECT total_assigned_issues, at_churn_risk
        FROM jira__team_performance_dashboard
        WHERE project_name = 'Mobile App Gamma'
    
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-061/attempt-01/sql/S51.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-061/attempt-01/sql/S51.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-061/attempt-01/results/S51.rows.jsonl)；完整：True；SHA256：`a973679d332bc231d455dc89bbebe363cb045180050e9431feb03eafd431ea62`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "jira__team_performance_dashboard", "kind": "base", "block": null, "base_tables": ["jira__team_performance_dashboard"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |


## S52

类别 `data`；来源 `python`；调用 `91971f8f7e084f49b00ff2ec5dc0ec57`；状态 `success`。

```sql

        SELECT total_assigned_issues, at_churn_risk
        FROM jira__team_performance_dashboard
        WHERE project_name = 'User Management V3'
    
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-061/attempt-01/sql/S52.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-061/attempt-01/sql/S52.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-061/attempt-01/results/S52.rows.jsonl)；完整：True；SHA256：`2bf982d58f582685011d6d948cbf57ff5847d02e0fb9c6c3864598df9f021578`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "jira__team_performance_dashboard", "kind": "base", "block": null, "base_tables": ["jira__team_performance_dashboard"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |


## S53

类别 `data`；来源 `python`；调用 `91971f8f7e084f49b00ff2ec5dc0ec57`；状态 `success`。

```sql

    SELECT p.project_name, p.avg_close_time, i.avg_regression, i.avg_lqs
    FROM (SELECT project_name, AVG(avg_close_time_days) as avg_close_time FROM jira__project_enhanced GROUP BY project_name) p
    JOIN (SELECT project_name, AVG(regression_ratio) as avg_regression, AVG(lifecycle_quality_score) as avg_lqs FROM jira__issue_intelligence_analytics GROUP BY project_name) i
    ON p.project_name = i.project_name

```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-061/attempt-01/sql/S53.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-061/attempt-01/sql/S53.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-061/attempt-01/results/S53.rows.jsonl)；完整：True；SHA256：`6aa4b95dd1219b948b91465d6e64fc38a8ca9ab48fdff3ba955a37cc9fce7001`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "jira__project_enhanced", "kind": "base", "block": null, "base_tables": ["jira__project_enhanced"]}] | [] | ["project_name"] |
| B2 | [{"alias": "jira__issue_intelligence_analytics", "kind": "base", "block": null, "base_tables": ["jira__issue_intelligence_analytics"]}] | [] | ["project_name"] |
| B3 | [{"alias": "p", "kind": "derived", "block": "B1", "base_tables": ["jira__project_enhanced"]}, {"alias": "i", "kind": "derived", "block": "B2", "base_tables": ["jira__issue_intelligence_analytics"]}] | [{"type": "INNER", "right": "(SELECT project_name, AVG(regression_ratio) AS avg_regression, AVG(lifecycle_quality_score) AS avg_lqs FROM jira__issue_intelligence_analytics GROUP BY project_name) AS i", "on": "p.project_name = i.project_name", "using": []}] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | AVG(avg_close_time_days) | [{"table": "jira__project_enhanced", "column": "avg_close_time_days"}] | [] | False |
| B2 | AVG(regression_ratio) | [{"table": "jira__issue_intelligence_analytics", "column": "regression_ratio"}] | [] | False |
| B2 | AVG(lifecycle_quality_score) | [{"table": "jira__issue_intelligence_analytics", "column": "lifecycle_quality_score"}] | [] | False |

