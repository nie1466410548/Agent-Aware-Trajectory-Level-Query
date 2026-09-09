# dacomp-063

The Project Management Committee has observed a perplexing phenomenon: certain projects ex…

运行：已提交。官方未评分。全部 SQL 尝试/成功 77/76；数据 SQL 74/73；Python 6 次。

完整原题：

The Project Management Committee has observed a perplexing phenomenon: certain projects exhibit an excellent `overall_health_score` and team performance (health score > 75, team performance score > 80), yet on the stakeholder engagement level, they show an `engagement_risk_status` of "High Risk". Simultaneously, issue intelligence analytics for these projects indicate high `high_complexity_risk` and `intervention_urgency`. What is more concerning is that upon deeper analysis, these "superficially healthy" projects show an anomalous `lifecycle_deviation_ratio`, a high assignee `assignment_risk_score`, and a mismatch between their cross-functional collaboration model (`cross_functional_projects`) and actual delivery outcomes. Please construct a comprehensive analytical framework to:

1) Identify and quantify the distribution characteristics of projects exhibiting this multi-dimensional contradictory phenomenon;
2) Based on multiple dimensions such as the team performance dashboard, stakeholder engagement patterns, and issue lifecycle analytics, design your own comprehensive risk assessment model to re-evaluate the true health status of these projects;
3) Conduct a deep-dive analysis into the root causes of this "false prosperity," paying special attention to hidden factors such as staffing efficiency, the quality of the communication and collaboration network, and workflow deviations.

| 表 | 行数 | 列数 |
| --- | --- | --- |
| jira__project_risk_assessment | 200 | 31 |
| jira__stakeholder_engagement_insights | 4524 | 23 |
| jira__team_performance_dashboard | 4374 | 33 |


实际路线（分析者依据 SQL/源码概括，不代表 Agent 自述）：SQL 探查项目健康、团队和参与风险 → Python 连接与风险重评分、分组比较 → 虚假繁荣诊断与检验。

数据库大小：1,855,488 字节。

## 数据 SQL

| SQL | 状态 | 基础表 | Join 输入/类型 | GROUP BY | 聚合表达式 | 结果行数 | 数据库 ms |
| --- | --- | --- | --- | --- | --- | --- | --- |
| [S4/Q1](#s4) | success | ["jira__project_risk_assessment"] | 0 / {} | [] | [] | 5 | 0.411 |
| [S5/Q2](#s5) | success | ["jira__stakeholder_engagement_insights"] | 0 / {} | [] | [] | 5 | 0.295 |
| [S6/Q3](#s6) | success | ["jira__team_performance_dashboard"] | 0 / {} | [] | [] | 5 | 0.433 |
| [S7/Q4](#s7) | success | ["jira__project_risk_assessment"] | 0 / {} | [] | ["COUNT(*)"] | 1 | 0.339 |
| [S8/Q5](#s8) | success | ["jira__stakeholder_engagement_insights"] | 0 / {} | [] | ["COUNT(*)"] | 1 | 0.916 |
| [S9/Q6](#s9) | success | ["jira__team_performance_dashboard"] | 0 / {} | [] | ["COUNT(*)"] | 1 | 1.107 |
| [S10/Q7](#s10) | success | ["jira__stakeholder_engagement_insights"] | 0 / {} | [] | [] | 2 | 1.125 |
| [S11/Q8](#s11) | success | ["jira__project_risk_assessment"] | 0 / {} | [] | [] | 3 | 0.43 |
| [S12/Q9](#s12) | success | ["jira__project_risk_assessment"] | 0 / {} | [] | [] | 4 | 0.367 |
| [S13/Q10](#s13) | success | ["jira__project_risk_assessment"] | 0 / {} | [] | [] | 7 | 0.381 |
| [S14/Q11](#s14) | success | ["jira__project_risk_assessment"] | 0 / {} | [] | ["MIN(overall_health_score)", "AVG(overall_health_score)", "MAX(overall_health_score)"] | 1 | 0.359 |
| [S15/Q12](#s15) | success | ["jira__team_performance_dashboard"] | 0 / {} | [] | ["MIN(overall_performance_score)", "AVG(overall_performance_score)", "MAX(overall_performance_score)"] | 1 | 1.271 |
| [S16/Q13](#s16) | success | ["jira__team_performance_dashboard"] | 0 / {} | [] | [] | 5 | 1.301 |
| [S17/Q14](#s17) | success | ["jira__project_risk_assessment"] | 0 / {} | [] | [] | 10 | 0.375 |
| [S18/Q15](#s18) | success | ["jira__team_performance_dashboard"] | 0 / {} | [] | [] | 1 | 1.602 |
| [S19/Q16](#s19) | success | ["jira__stakeholder_engagement_insights"] | 0 / {} | [] | [] | 6 | 1.056 |
| [S20/Q17](#s20) | success | ["jira__project_risk_assessment"] | 0 / {} | [] | [] | 20 | 0.544 |
| [S21/Q18](#s21) | success | ["jira__stakeholder_engagement_insights"] | 0 / {} | ["engagement_risk_status"] | ["COUNT(*)"] | 2 | 1.653 |
| [S22/Q19](#s22) | success | ["jira__project_risk_assessment"] | 0 / {} | [] | [] | 42 | 0.526 |
| [S23/Q20](#s23) | success | ["jira__project_risk_assessment"] | 0 / {} | ["risk_category"] | ["COUNT(*)", "AVG(overall_health_score)", "AVG(total_risk_score)", "AVG(complexity_risk_score)"] | 3 | 0.496 |
| [S24/Q21](#s24) | success | ["jira__project_risk_assessment"] | 0 / {} | ["recommended_intervention"] | ["COUNT(*)", "AVG(overall_health_score)"] | 4 | 0.516 |
| [S25/Q22](#s25) | success | ["jira__project_risk_assessment"] | 0 / {} | ["trajectory_status"] | ["COUNT(*)", "AVG(overall_health_score)", "AVG(health_risk_score)"] | 7 | 0.458 |
| [S26/Q23](#s26) | success | ["jira__stakeholder_engagement_insights"] | 0 / {} | [] | ["COUNT(DISTINCT user_display_name)"] | 1 | 2.275 |
| [S27/Q24](#s27) | success | ["jira__team_performance_dashboard"] | 0 / {} | [] | ["COUNT(DISTINCT user_display_name)"] | 1 | 1.242 |
| [S28/Q25](#s28) | failed | ["jira__stakeholder_engagement_insights"] | 0 / {} | [] | ["COUNT(DISTINCT user_id)"] | unknown | 未取得；调用总时长 0.193 ms |
| [S29/Q26](#s29) | success | ["jira__team_performance_dashboard"] | 0 / {} | [] | ["COUNT(DISTINCT user_id)"] | 1 | 3.725 |
| [S30/Q27](#s30) | success | ["jira__stakeholder_engagement_insights", "jira__team_performance_dashboard"] | 0 / {} | [] | ["COUNT(*)"] | 1 | 3.569 |
| [S31/Q28](#s31) | success | ["jira__stakeholder_engagement_insights"] | 0 / {} | ["user_display_name"] | ["COUNT(*)"] | 5 | 2.153 |
| [S32/Q29](#s32) | success | ["jira__team_performance_dashboard"] | 0 / {} | ["user_display_name"] | ["COUNT(*)"] | 5 | 1.54 |
| [S33/Q30](#s33) | success | ["jira__team_performance_dashboard"] | 0 / {} | [] | [] | 5 | 1.187 |
| [S34/Q31](#s34) | success | ["jira__team_performance_dashboard"] | 0 / {} | [] | [] | 6 | 1.22 |
| [S35/Q32](#s35) | success | ["jira__team_performance_dashboard"] | 0 / {} | [] | [] | 5 | 1.161 |
| [S36/Q33](#s36) | success | ["jira__stakeholder_engagement_insights"] | 0 / {} | [] | [] | 7 | 1.26 |
| [S37/Q34](#s37) | success | ["jira__stakeholder_engagement_insights"] | 0 / {} | [] | [] | 5 | 1.227 |
| [S38/Q35](#s38) | success | ["jira__project_risk_assessment"] | 0 / {} | ["CASE WHEN overall_health_score > 75 THEN 'health>75' ELSE 'health<=75' END", "risk_category"] | ["COUNT(*)", "AVG(overall_health_score)", "AVG(total_risk_score)", "AVG(complexity_risk_score)", "AVG(success_probability)"] | 6 | 0.591 |
| [S39/Q36](#s39) | success | ["jira__project_risk_assessment"] | 0 / {} | ["primary_risk_factor"] | ["COUNT(*)", "AVG(overall_health_score)"] | 5 | 0.431 |
| [S40/Q37](#s40) | success | ["jira__team_performance_dashboard"] | 0 / {} | ["CASE WHEN overall_performance_score > 80 THEN 'perf>80' ELSE 'perf<=80' END"] | ["COUNT(*)", "AVG(overall_performance_score)", "AVG(avg_resolution_days)", "AVG(estimate_accuracy_percentage)", "AVG(consistency_percentage)"] | 2 | 3.12 |
| [S41/Q38](#s41) | success | ["jira__team_performance_dashboard"] | 0 / {} | ["performance_tier"] | ["COUNT(*)", "AVG(overall_performance_score)", "AVG(resolution_rate_percentage)"] | 5 | 2.508 |
| [S42/Q39](#s42) | success | ["jira__stakeholder_engagement_insights", "jira__team_performance_dashboard"] | 0 / {} | [] | ["COUNT(*)"] | 1 | 8.966 |
| [S43/Q40](#s43) | success | ["jira__stakeholder_engagement_insights", "jira__team_performance_dashboard"] | 0 / {} | [] | ["COUNT(*)"] | 1 | 8.872 |
| [S44/Q41](#s44) | success | ["jira__stakeholder_engagement_insights"] | 0 / {} | [] | [] | 8 | 0.325 |
| [S45/Q42](#s45) | success | ["jira__project_risk_assessment"] | 0 / {} | ["CASE WHEN overall_health_score > 75 THEN 'High Health' ELSE 'Low Health' END", "CASE WHEN risk_category IN ('Critical Risk', 'High Risk') AND complexity_risk_score > 30 THEN 'High Risk Cluster' ELSE 'Normal Risk' END"] | ["COUNT(*)", "AVG(overall_health_score)", "AVG(total_risk_score)", "AVG(complexity_risk_score)", "AVG(value_delivery_percentage)", "AVG(team_stability_percentage)", "AVG(success_probability)", "AVG(resolution_velocity_change_percent)", "AVG(health_risk_score)", "AVG(schedule_risk_score)", "AVG(resource_risk_score)"] | 4 | 0.878 |
| [S46/Q43](#s46) | success | ["jira__project_risk_assessment"] | 0 / {} | [] | [] | 19 | 0.545 |
| [S47/Q44](#s47) | success | ["jira__stakeholder_engagement_insights", "jira__team_performance_dashboard"] | 2 / {'INNER': 1} | ["t.overall_performance_score > 80", "s.engagement_risk_status"] | ["COUNT(*)"] | 4 | 8.719 |
| [S48/Q45](#s48) | success | ["jira__stakeholder_engagement_insights", "jira__team_performance_dashboard"] | 2 / {'INNER': 1} | ["s.engagement_risk_status", "CASE WHEN t.overall_performance_score > 80 THEN 'High Perf' ELSE 'Low Perf' END"] | ["COUNT(*)", "AVG(t.resolution_rate_percentage)", "AVG(t.avg_resolution_days)", "AVG(t.estimate_accuracy_percentage)", "AVG(t.consistency_percentage)", "AVG(t.unique_collaborators_on_issues)", "AVG(t.at_churn_risk)", "AVG(t.poor_estimation)", "AVG(t.inactive_recently)"] | 4 | 10.701 |
| [S49/Q46](#s49) | success | ["jira__stakeholder_engagement_insights"] | 0 / {} | ["engagement_risk_status"] | ["COUNT(*)", "AVG(total_engagement_score)", "AVG(engagement_breadth_score)", "AVG(engagement_depth_score)", "AVG(engagement_quality_score)", "AVG(engagement_impact_score)", "AVG(cross_functional_projects)", "AVG(direct_network_connections)", "AVG(total_outbound_influence)", "AVG(total_inbound_influence)", "AVG(strategic_value_score)", "AVG(total_comments_authored)", "AVG(issues_assigned)", "AVG(issues_reported)"] | 2 | 5.665 |
| [S50/Q47](#s50) | success | ["jira__project_risk_assessment"] | 0 / {} | ["CASE WHEN overall_health_score > 75 AND risk_category IN ('Critical Risk', 'High Risk') AND complexity_risk_score > 30 THEN 'FalseProsperity' ELSE 'Other' END"] | ["COUNT(*)", "AVG(overall_health_score)", "AVG(total_risk_score)", "AVG(health_risk_score)", "AVG(schedule_risk_score)", "AVG(resource_risk_score)", "AVG(complexity_risk_score)", "AVG(scope_risk_score)", "AVG(success_probability)", "AVG(value_delivery_percentage)", "AVG(team_stability_percentage)", "AVG(resolution_velocity_change_percent)", "AVG(net_issue_growth_30d)", "AVG(high_delay_cost_issues)", "AVG(total_hours_invested)", "AVG(estimated_project_value_points)", "AVG(delivered_value_points)", "AVG(sprint_adoption_rate)"] | 2 | 0.835 |
| [S51/Q48](#s51) | success | ["jira__project_risk_assessment"] | 0 / {} | [] | [] | 200 | 1.625 |
| [S52/Q49](#s52) | success | ["jira__stakeholder_engagement_insights"] | 0 / {} | [] | [] | 4524 | 19.133 |
| [S53/Q50](#s53) | success | ["jira__team_performance_dashboard"] | 0 / {} | [] | [] | 4374 | 26.008 |
| [S54/Q51](#s54) | success | ["jira__project_risk_assessment"] | 0 / {} | [] | [] | 200 | 1.56 |
| [S55/Q52](#s55) | success | ["jira__stakeholder_engagement_insights"] | 0 / {} | [] | [] | 4524 | 18.303 |
| [S56/Q53](#s56) | success | ["jira__team_performance_dashboard"] | 0 / {} | [] | [] | 4374 | 24.183 |
| [S57/Q54](#s57) | success | ["jira__project_risk_assessment"] | 0 / {} | [] | [] | 200 | 1.439 |
| [S58/Q55](#s58) | success | ["jira__stakeholder_engagement_insights"] | 0 / {} | [] | [] | 4524 | 18.309 |
| [S59/Q56](#s59) | success | ["jira__team_performance_dashboard"] | 0 / {} | [] | [] | 4374 | 24.033 |
| [S60/Q57](#s60) | success | ["jira__project_risk_assessment"] | 0 / {} | [] | [] | 200 | 1.543 |
| [S61/Q58](#s61) | success | ["jira__stakeholder_engagement_insights"] | 0 / {} | [] | [] | 4524 | 18.926 |
| [S62/Q59](#s62) | success | ["jira__team_performance_dashboard"] | 0 / {} | [] | [] | 4374 | 27.059 |
| [S63/Q60](#s63) | success | ["jira__project_risk_assessment"] | 0 / {} | [] | [] | 200 | 1.609 |
| [S64/Q61](#s64) | success | ["jira__stakeholder_engagement_insights"] | 0 / {} | [] | [] | 4524 | 19.036 |
| [S65/Q62](#s65) | success | ["jira__team_performance_dashboard"] | 0 / {} | [] | [] | 4374 | 24.371 |
| [S66/Q63](#s66) | success | ["jira__project_risk_assessment"] | 0 / {} | [] | [] | 200 | 1.552 |
| [S67/Q64](#s67) | success | ["jira__stakeholder_engagement_insights"] | 0 / {} | [] | [] | 4524 | 18.389 |
| [S68/Q65](#s68) | success | ["jira__team_performance_dashboard"] | 0 / {} | [] | [] | 4374 | 24.431 |
| [S69/Q66](#s69) | success | ["jira__project_risk_assessment"] | 0 / {} | ["primary_risk_driver"] | ["COUNT(*)"] | 3 | 0.528 |
| [S70/Q67](#s70) | success | ["jira__project_risk_assessment"] | 0 / {} | ["strategic_priority_recommendation"] | ["COUNT(*)"] | 2 | 0.805 |
| [S71/Q68](#s71) | success | ["jira__stakeholder_engagement_insights", "jira__team_performance_dashboard"] | 2 / {'INNER': 1} | ["t.performance_tier", "s.engagement_risk_status"] | ["COUNT(*)"] | 10 | 8.943 |
| [S72/Q69](#s72) | success | ["jira__project_risk_assessment"] | 0 / {} | [] | [] | 95 | 0.694 |
| [S73/Q70](#s73) | success | ["jira__project_risk_assessment"] | 0 / {} | [] | ["COUNT(*)"] | 1 | 0.385 |
| [S74/Q71](#s74) | success | ["jira__project_risk_assessment"] | 0 / {} | ["strategic_priority_recommendation"] | ["COUNT(*)"] | 2 | 0.455 |
| [S75/Q72](#s75) | success | ["jira__project_risk_assessment"] | 0 / {} | ["CASE WHEN overall_health_score > 75 THEN 'health>75' ELSE 'health<=75' END", "strategic_priority_recommendation"] | ["COUNT(*)"] | 6 | 0.535 |
| [S76/Q73](#s76) | success | ["jira__project_risk_assessment"] | 0 / {} | [] | [] | 15 | 0.536 |
| [S77/Q74](#s77) | success | ["jira__project_risk_assessment"] | 0 / {} | [] | ["COUNT(*)", "SUM(CASE WHEN risk_category = 'Critical Risk' THEN 1 ELSE 0 END)", "SUM(CASE WHEN trajectory_status IN ('Declining', 'Deteriorating', 'At Risk', 'Volatile') THEN 1 ELSE 0 END)", "SUM(CASE WHEN value_delivery_percentage < 60 THEN 1 ELSE 0 END)", "SUM(CASE WHEN success_probability < 0.4 THEN 1 ELSE 0 END)", "SUM(CASE WHEN resolution_velocity_change_percent < 0 THEN 1 ELSE 0 END)", "SUM(CASE WHEN net_issue_growth_30d > 0 THEN 1 ELSE 0 END)", "AVG(overall_health_score)", "AVG(total_risk_score)", "AVG(complexity_risk_score)", "AVG(value_delivery_percentage)", "AVG(success_probability)"] | 1 | 0.579 |


## 元数据和设置

| SQL | 类别 | 状态 | 内容 |
| --- | --- | --- | --- |
| S1 | connection_setup | success | PRAGMA query_only=ON |
| S2 | metadata | success | SELECT name,sql FROM sqlite_master WHERE type='table' ORDER BY name |
| S3 | metadata | success | SELECT name FROM sqlite_master WHERE type='table' ORDER BY name |


## Python 与执行位置

人工源码审查：**database_first_violation**。Python 连接团队与利益相关者表，按风险级别和原型计数，构造风险评分并比较分组均值。这些 SQL 可支持的关系运算和算术迁出数据库；t 检验和绘图独立保留。 [证据](../reviews/dacomp-063.json)。

P1：Need to compute comprehensive analysis combining project, team, and stakeholder data. Building a composite risk model and creating visualizations. This is outside SQL because it requires multi-dimensional scaling, correlation analysis, and visualization that SQLite cannot do.

[源码](../../../runs/dsv4flash-db-first-full-01/dacomp-063/attempt-01/python/P1.py)；[输出](../../../runs/dsv4flash-db-first-full-01/dacomp-063/attempt-01/python/P1.stdout)；[错误](../../../runs/dsv4flash-db-first-full-01/dacomp-063/attempt-01/python/P1.stderr)。检出需人工核验的 SQL 可实现操作：groupby(, .merge(, .query(, sort_values(；不能仅凭理由判为合规。

P2：Need to fix the data loading to use db.frame() instead of db.rows() since db.rows returns tuples, not dicts/DataFrames.

[源码](../../../runs/dsv4flash-db-first-full-01/dacomp-063/attempt-01/python/P2.py)；[输出](../../../runs/dsv4flash-db-first-full-01/dacomp-063/attempt-01/python/P2.stdout)；[错误](../../../runs/dsv4flash-db-first-full-01/dacomp-063/attempt-01/python/P2.stderr)。检出需人工核验的 SQL 可实现操作：groupby(, .merge(, .query(；不能仅凭理由判为合规。

P3：Fix matplotlib boxplot API (labels -> tick_labels) and generate remaining figures for team performance and stakeholder engagement patterns.

[源码](../../../runs/dsv4flash-db-first-full-01/dacomp-063/attempt-01/python/P3.py)；[输出](../../../runs/dsv4flash-db-first-full-01/dacomp-063/attempt-01/python/P3.stdout)；[错误](../../../runs/dsv4flash-db-first-full-01/dacomp-063/attempt-01/python/P3.stderr)。检出需人工核验的 SQL 可实现操作：groupby(, .merge(, .query(, sort_values(；不能仅凭理由判为合规。

P4：Fix the model computation - ensure health_gap column is accessible. The error was caused by trying to access health_gap on fp subset before it was computed. Also need to fix the describe call syntax.

[源码](../../../runs/dsv4flash-db-first-full-01/dacomp-063/attempt-01/python/P4.py)；[输出](../../../runs/dsv4flash-db-first-full-01/dacomp-063/attempt-01/python/P4.stdout)；[错误](../../../runs/dsv4flash-db-first-full-01/dacomp-063/attempt-01/python/P4.stderr)。检出需人工核验的 SQL 可实现操作：.merge(, .query(, sort_values(；不能仅凭理由判为合规。

P5：Need one more analysis to compute lifecycle_deviation_ratio and assignment_risk_score, and to examine the cross-functional projects mismatch. These are derived metrics that need Python computation.

[源码](../../../runs/dsv4flash-db-first-full-01/dacomp-063/attempt-01/python/P5.py)；[输出](../../../runs/dsv4flash-db-first-full-01/dacomp-063/attempt-01/python/P5.stdout)；[错误](../../../runs/dsv4flash-db-first-full-01/dacomp-063/attempt-01/python/P5.stderr)。检出需人工核验的 SQL 可实现操作：.query(；不能仅凭理由判为合规。

P6：Fix ordering: fp subset must be recomputed after adding derived columns. Compute lifecycle deviation, assignment risk, and cross-functional mismatch, then create figure 8.

[源码](../../../runs/dsv4flash-db-first-full-01/dacomp-063/attempt-01/python/P6.py)；[输出](../../../runs/dsv4flash-db-first-full-01/dacomp-063/attempt-01/python/P6.stdout)；[错误](../../../runs/dsv4flash-db-first-full-01/dacomp-063/attempt-01/python/P6.stderr)。检出需人工核验的 SQL 可实现操作：.query(；不能仅凭理由判为合规。

## 优化机会

已验证候选。筛选限于精确 SQL、相同自包含 CTE、相同单表完整过滤、可分解单表聚合；未覆盖任意 Join 等价和一般谓词蕴含。全部候选都是 offline，未测在线预测。

| 候选 | 类型 | 已有结果 | 覆盖 SQL | 后续次数 | 中间行数 | 验证 | 成本 |
| --- | --- | --- | --- | --- | --- | --- | --- |
| C1 | exact-result reuse | True | ["S51", "S54", "S57", "S60", "S63", "S66"] | 5 | unknown | not_verified_cap | Not tested |
| C2 | exact-result reuse | True | ["S52", "S55", "S58", "S61", "S64", "S67"] | 5 | 4524 | verified | Not benchmarked; correctness alone does not establish net speedup. |
| C3 | exact-result reuse | True | ["S53", "S56", "S59", "S62", "S65", "S68"] | 5 | 4374 | verified | Not benchmarked; correctness alone does not establish net speedup. |
| C4 | aggregate MV | False | ["S7", "S23", "S24", "S25", "S38", "S39", "S50", "S75"] | 7 | 125 | rejected_result_mismatch | Not benchmarked; correctness alone does not establish net speedup. |
| C5 | aggregate MV | False | ["S8", "S21", "S49"] | 2 | unknown | not_verified_cap | Not tested |
| C6 | aggregate MV | False | ["S9", "S40", "S41"] | 2 | unknown | not_verified_cap | Not tested |
| C7 | common filtered view | False | ["S20", "S22"] | 1 | unknown | not_verified_cap | Not tested |
| C8 | common filtered view | False | ["S46", "S69", "S70", "S74"] | 3 | unknown | not_verified_cap | Not tested |
| C9 | aggregate MV | False | ["S69", "S70", "S74"] | 2 | unknown | not_verified_cap | Not tested |


已验证覆盖（含触发查询、候选并集去重）：12/73 条成功数据 SQL。正确性仅针对当前数据库快照；未测性能的候选不能声称已加速。

[完整 build/rewrite 与比较证据](dacomp-063.analysis.json)。

### C2：exact-result reuse

Identical normalized SQL and parameters; archive equality checked.

原查询 [S52](#s52), [S55](#s55), [S58](#s58), [S61](#s61), [S64](#s64), [S67](#s67) → 保留前序结果 S52 → 后续 5 次可复用。该构建点为事后假设，不代表 Agent 当时预知后续。

| 原 SQL | 列名一致 | 结果一致 | 比较方法 |
| --- | --- | --- | --- |
| S55 | True | True | exact_multiset |
| S58 | True | True | exact_multiset |
| S61 | True | True | exact_multiset |
| S64 | True | True | exact_multiset |
| S67 | True | True | exact_multiset |


验证状态：verified；成本结论：Not benchmarked; correctness alone does not establish net speedup.

### C3：exact-result reuse

Identical normalized SQL and parameters; archive equality checked.

原查询 [S53](#s53), [S56](#s56), [S59](#s59), [S62](#s62), [S65](#s65), [S68](#s68) → 保留前序结果 S53 → 后续 5 次可复用。该构建点为事后假设，不代表 Agent 当时预知后续。

| 原 SQL | 列名一致 | 结果一致 | 比较方法 |
| --- | --- | --- | --- |
| S56 | True | True | exact_multiset |
| S59 | True | True | exact_multiset |
| S62 | True | True | exact_multiset |
| S65 | True | True | exact_multiset |
| S68 | True | True | exact_multiset |


验证状态：verified；成本结论：Not benchmarked; correctness alone does not establish net speedup.

### C4：aggregate MV

Union of grouping keys; decomposable aggregate states; AVG uses SUM and non-NULL COUNT.

原查询 [S7](#s7), [S23](#s23), [S24](#s24), [S25](#s25), [S38](#s38), [S39](#s39), [S50](#s50), [S75](#s75) → 新增共享状态 C4 → 后续 7 次可复用。该构建点为事后假设，不代表 Agent 当时预知后续。

构建定义：

```sql
SELECT risk_category AS __g0, recommended_intervention AS __g1, trajectory_status AS __g2, CASE WHEN overall_health_score > 75 THEN 'health>75' ELSE 'health<=75' END AS __g3, primary_risk_factor AS __g4, CASE WHEN overall_health_score > 75 AND risk_category IN ('Critical Risk', 'High Risk') AND complexity_risk_score > 30 THEN 'FalseProsperity' ELSE 'Other' END AS __g5, strategic_priority_recommendation AS __g6, COUNT(*) AS __a0, SUM(overall_health_score) AS __a1_sum, COUNT(overall_health_score) AS __a1_n, SUM(total_risk_score) AS __a2_sum, COUNT(total_risk_score) AS __a2_n, SUM(complexity_risk_score) AS __a3_sum, COUNT(complexity_risk_score) AS __a3_n, SUM(health_risk_score) AS __a4_sum, COUNT(health_risk_score) AS __a4_n, SUM(success_probability) AS __a5_sum, COUNT(success_probability) AS __a5_n, SUM(schedule_risk_score) AS __a6_sum, COUNT(schedule_risk_score) AS __a6_n, SUM(resource_risk_score) AS __a7_sum, COUNT(resource_risk_score) AS __a7_n, SUM(scope_risk_score) AS __a8_sum, COUNT(scope_risk_score) AS __a8_n, SUM(value_delivery_percentage) AS __a9_sum, COUNT(value_delivery_percentage) AS __a9_n, SUM(team_stability_percentage) AS __a10_sum, COUNT(team_stability_percentage) AS __a10_n, SUM(resolution_velocity_change_percent) AS __a11_sum, COUNT(resolution_velocity_change_percent) AS __a11_n, SUM(net_issue_growth_30d) AS __a12_sum, COUNT(net_issue_growth_30d) AS __a12_n, SUM(high_delay_cost_issues) AS __a13_sum, COUNT(high_delay_cost_issues) AS __a13_n, SUM(total_hours_invested) AS __a14_sum, COUNT(total_hours_invested) AS __a14_n, SUM(estimated_project_value_points) AS __a15_sum, COUNT(estimated_project_value_points) AS __a15_n, SUM(delivered_value_points) AS __a16_sum, COUNT(delivered_value_points) AS __a16_n, SUM(sprint_adoption_rate) AS __a17_sum, COUNT(sprint_adoption_rate) AS __a17_n FROM "jira__project_risk_assessment"  GROUP BY risk_category, recommended_intervention, trajectory_status, CASE WHEN overall_health_score > 75 THEN 'health>75' ELSE 'health<=75' END, primary_risk_factor, CASE WHEN overall_health_score > 75 AND risk_category IN ('Critical Risk', 'High Risk') AND complexity_risk_score > 30 THEN 'FalseProsperity' ELSE 'Other' END, strategic_priority_recommendation
```

受益查询 S7 的改写示例：

```sql
SELECT SUM(__a0) AS cnt FROM temp.reuse_candidate
```

| 原 SQL | 列名一致 | 结果一致 | 比较方法 |
| --- | --- | --- | --- |
| S7 | True | True | exact_multiset |
| S23 | True | False | exact_multiset |
| S24 | True | False | exact_multiset |
| S25 | True | False | exact_multiset |
| S38 | True | True | ordered_numeric_tolerance |
| S39 | True | True | ordered_numeric_tolerance |
| S50 | True | True | exact_multiset |
| S75 | True | True | ordered_numeric_tolerance |


验证状态：rejected_result_mismatch；成本结论：Not benchmarked; correctness alone does not establish net speedup.

结果依赖：自动记录 SQL→Python 的接口父调用，以及源码中引用归档文件的消费者；字面值相同不认定因果。模型方向选择需要人工读取消息，尚未做全面因果标注。

[原始报告](../../../runs/dsv4flash-db-first-full-01/dacomp-063/attempt-01/answer.md)；[统一消息](../../../runs/dsv4flash-db-first-full-01/dacomp-063/attempt-01/messages.jsonl)；[原始 OpenCode 事件](../../../runs/dsv4flash-db-first-full-01/dacomp-063/attempt-01/opencode.jsonl)；[SQL 引擎日志](../../../runs/dsv4flash-db-first-full-01/dacomp-063/attempt-01/sql_journal.jsonl)。

[可读报告（本地图片链接规范化）](../answers/dacomp-063.md)。原始回答保留，分析结论未改写。

## S1

类别 `connection_setup`；来源 `connection`；调用 `952b09f67140445896e73bb57175f9cd`；状态 `success`。

```sql
PRAGMA query_only=ON
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-063/attempt-01/sql/S1.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-063/attempt-01/sql/S1.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-063/attempt-01/results/S1.rows.jsonl)；完整：True；SHA256：`e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`。

## S2

类别 `metadata`；来源 `list_db`；调用 `952b09f67140445896e73bb57175f9cd`；状态 `success`。

```sql
SELECT name,sql FROM sqlite_master WHERE type='table' ORDER BY name
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-063/attempt-01/sql/S2.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-063/attempt-01/sql/S2.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-063/attempt-01/results/S2.rows.jsonl)；完整：True；SHA256：`6c9900ff8ea869d59270a3a52898da003b3225e1ca5262ed9107876ac6e64171`。

## S3

类别 `metadata`；来源 `query_db`；调用 `ab24b51ecc8e4588a421a62f593f9f5b`；状态 `success`。

```sql
SELECT name FROM sqlite_master WHERE type='table' ORDER BY name
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-063/attempt-01/sql/S3.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-063/attempt-01/sql/S3.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-063/attempt-01/results/S3.rows.jsonl)；完整：True；SHA256：`2590497397bbeb83c4a327e6149b8d10013ebeb8584ee414597e3fc0179b9141`。

## S4

类别 `data`；来源 `query_db`；调用 `1681239313574e988737ee53d025e43a`；状态 `success`。

```sql
SELECT * FROM jira__project_risk_assessment LIMIT 5
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-063/attempt-01/sql/S4.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-063/attempt-01/sql/S4.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-063/attempt-01/results/S4.rows.jsonl)；完整：True；SHA256：`ea332c7d7e7eb55816838ef74e119d520c80bcb7fdb4583a1471db834d0e470f`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "jira__project_risk_assessment", "kind": "base", "block": null, "base_tables": ["jira__project_risk_assessment"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |


## S5

类别 `data`；来源 `query_db`；调用 `a06a0244e7824a2a8f3534038bec502e`；状态 `success`。

```sql
SELECT * FROM jira__stakeholder_engagement_insights LIMIT 5
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-063/attempt-01/sql/S5.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-063/attempt-01/sql/S5.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-063/attempt-01/results/S5.rows.jsonl)；完整：True；SHA256：`cc994386a469495880c01961435877d1a58ec921ca25625617f546f912432395`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "jira__stakeholder_engagement_insights", "kind": "base", "block": null, "base_tables": ["jira__stakeholder_engagement_insights"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |


## S6

类别 `data`；来源 `query_db`；调用 `fb0e6f5ad265451d83f553297ce2d643`；状态 `success`。

```sql
SELECT * FROM jira__team_performance_dashboard LIMIT 5
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-063/attempt-01/sql/S6.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-063/attempt-01/sql/S6.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-063/attempt-01/results/S6.rows.jsonl)；完整：True；SHA256：`135592b0ba4716a77eabc67213879d487646600c1e3fc887d0eef0cb965e2f14`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "jira__team_performance_dashboard", "kind": "base", "block": null, "base_tables": ["jira__team_performance_dashboard"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |


## S7

类别 `data`；来源 `query_db`；调用 `fc048bd9857b46eb86abfb747ceb2f06`；状态 `success`。

```sql
SELECT COUNT(*) as cnt FROM jira__project_risk_assessment
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-063/attempt-01/sql/S7.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-063/attempt-01/sql/S7.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-063/attempt-01/results/S7.rows.jsonl)；完整：True；SHA256：`8fe64ac838eb7a89546cb6a98f203e335a9c087776008d203b43095ded53e1b7`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "jira__project_risk_assessment", "kind": "base", "block": null, "base_tables": ["jira__project_risk_assessment"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |


## S8

类别 `data`；来源 `query_db`；调用 `bf8b5e46317947bd8f20019836045b0f`；状态 `success`。

```sql
SELECT COUNT(*) as cnt FROM jira__stakeholder_engagement_insights
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-063/attempt-01/sql/S8.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-063/attempt-01/sql/S8.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-063/attempt-01/results/S8.rows.jsonl)；完整：True；SHA256：`d627005cafeb3332957ae72cf9a51f690d805fcb8a5a8212d1ab1e775ae32288`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "jira__stakeholder_engagement_insights", "kind": "base", "block": null, "base_tables": ["jira__stakeholder_engagement_insights"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |


## S9

类别 `data`；来源 `query_db`；调用 `c0d2e9a7812b471dad57afd3c1da5326`；状态 `success`。

```sql
SELECT COUNT(*) as cnt FROM jira__team_performance_dashboard
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-063/attempt-01/sql/S9.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-063/attempt-01/sql/S9.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-063/attempt-01/results/S9.rows.jsonl)；完整：True；SHA256：`7f55456fc3429b0a7398d6571deb2b08fded1545c23079431f0a75a6bfdb0055`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "jira__team_performance_dashboard", "kind": "base", "block": null, "base_tables": ["jira__team_performance_dashboard"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |


## S10

类别 `data`；来源 `query_db`；调用 `17d58b0cb9254147be846115e7b556b0`；状态 `success`。

```sql
SELECT DISTINCT engagement_risk_status FROM jira__stakeholder_engagement_insights
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-063/attempt-01/sql/S10.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-063/attempt-01/sql/S10.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-063/attempt-01/results/S10.rows.jsonl)；完整：True；SHA256：`6c10baea536ee45ba2e432faef81b05e2b120e855c2fb2e3918a3dc085d0f68a`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "jira__stakeholder_engagement_insights", "kind": "base", "block": null, "base_tables": ["jira__stakeholder_engagement_insights"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |


## S11

类别 `data`；来源 `query_db`；调用 `323cf391f88441099c2cf9c380caa6b1`；状态 `success`。

```sql
SELECT DISTINCT risk_category FROM jira__project_risk_assessment
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-063/attempt-01/sql/S11.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-063/attempt-01/sql/S11.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-063/attempt-01/results/S11.rows.jsonl)；完整：True；SHA256：`770f72b161c614ff7ee1d8c5ad3800490221971c7d92aa648705b7fb4241b018`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "jira__project_risk_assessment", "kind": "base", "block": null, "base_tables": ["jira__project_risk_assessment"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |


## S12

类别 `data`；来源 `query_db`；调用 `177f19294ff14177baa0ddb920a6d9aa`；状态 `success`。

```sql
SELECT DISTINCT recommended_intervention FROM jira__project_risk_assessment
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-063/attempt-01/sql/S12.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-063/attempt-01/sql/S12.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-063/attempt-01/results/S12.rows.jsonl)；完整：True；SHA256：`27f04ec27e736475307b8aa4bb8041e905f86836b693338b946b3d6b454ee597`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "jira__project_risk_assessment", "kind": "base", "block": null, "base_tables": ["jira__project_risk_assessment"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |


## S13

类别 `data`；来源 `query_db`；调用 `10df71fccd5d4a688ac8d7f056de6567`；状态 `success`。

```sql
SELECT DISTINCT trajectory_status FROM jira__project_risk_assessment
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-063/attempt-01/sql/S13.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-063/attempt-01/sql/S13.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-063/attempt-01/results/S13.rows.jsonl)；完整：True；SHA256：`9e8dc62b6a3553e98f86a8c98a1f181fa41135cb0304ef6f283233825bf85a8d`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "jira__project_risk_assessment", "kind": "base", "block": null, "base_tables": ["jira__project_risk_assessment"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |


## S14

类别 `data`；来源 `query_db`；调用 `04b241a04ae743db987ca7cf70c7ec0c`；状态 `success`。

```sql
SELECT MIN(overall_health_score), AVG(overall_health_score), MAX(overall_health_score) FROM jira__project_risk_assessment
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-063/attempt-01/sql/S14.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-063/attempt-01/sql/S14.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-063/attempt-01/results/S14.rows.jsonl)；完整：True；SHA256：`a6c39b96cc1bdad30d218aba2070c3c9ffa8c3fc9b3f9c993747ec3bd21cf767`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "jira__project_risk_assessment", "kind": "base", "block": null, "base_tables": ["jira__project_risk_assessment"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | MIN(overall_health_score) | [{"table": "jira__project_risk_assessment", "column": "overall_health_score"}] | [] | False |
| B1 | AVG(overall_health_score) | [{"table": "jira__project_risk_assessment", "column": "overall_health_score"}] | [] | False |
| B1 | MAX(overall_health_score) | [{"table": "jira__project_risk_assessment", "column": "overall_health_score"}] | [] | False |


## S15

类别 `data`；来源 `query_db`；调用 `69fd883848444c3b854537a8ea09c755`；状态 `success`。

```sql
SELECT MIN(overall_performance_score), AVG(overall_performance_score), MAX(overall_performance_score) FROM jira__team_performance_dashboard
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-063/attempt-01/sql/S15.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-063/attempt-01/sql/S15.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-063/attempt-01/results/S15.rows.jsonl)；完整：True；SHA256：`45f2e37852364d27640d7f55e7e989f9d4b413bb173d22bbd556c6b1e11b7b68`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "jira__team_performance_dashboard", "kind": "base", "block": null, "base_tables": ["jira__team_performance_dashboard"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | MIN(overall_performance_score) | [{"table": "jira__team_performance_dashboard", "column": "overall_performance_score"}] | [] | False |
| B1 | AVG(overall_performance_score) | [{"table": "jira__team_performance_dashboard", "column": "overall_performance_score"}] | [] | False |
| B1 | MAX(overall_performance_score) | [{"table": "jira__team_performance_dashboard", "column": "overall_performance_score"}] | [] | False |


## S16

类别 `data`；来源 `query_db`；调用 `097fc86f292a42f29bfffbcd196bbb43`；状态 `success`。

```sql
SELECT DISTINCT performance_tier FROM jira__team_performance_dashboard
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-063/attempt-01/sql/S16.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-063/attempt-01/sql/S16.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-063/attempt-01/results/S16.rows.jsonl)；完整：True；SHA256：`1636091820668face103ad22a5e49f3580e926540f9e5cc87cd35d6aff62b906`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "jira__team_performance_dashboard", "kind": "base", "block": null, "base_tables": ["jira__team_performance_dashboard"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |


## S17

类别 `data`；来源 `query_db`；调用 `7a6d423e33f14002b157d49b5620099c`；状态 `success`。

```sql
SELECT DISTINCT project_id FROM jira__project_risk_assessment ORDER BY project_id LIMIT 10
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-063/attempt-01/sql/S17.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-063/attempt-01/sql/S17.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-063/attempt-01/results/S17.rows.jsonl)；完整：True；SHA256：`7a82f6e2a00101a6c580c617c3308f2e5930c6083330736cc7bce0b4b57a28d1`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "jira__project_risk_assessment", "kind": "base", "block": null, "base_tables": ["jira__project_risk_assessment"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |


## S18

类别 `data`；来源 `query_db`；调用 `c48fde200c5a4bc8af3129a19853f837`；状态 `success`。

```sql
SELECT DISTINCT project_id FROM jira__team_performance_dashboard ORDER BY project_id LIMIT 10
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-063/attempt-01/sql/S18.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-063/attempt-01/sql/S18.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-063/attempt-01/results/S18.rows.jsonl)；完整：True；SHA256：`c75d6d9f1a22031a98c0cefe1e003cccb2cf4b08377bda762553d958a4162cc6`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "jira__team_performance_dashboard", "kind": "base", "block": null, "base_tables": ["jira__team_performance_dashboard"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |


## S19

类别 `data`；来源 `query_db`；调用 `8d7319da279e483fb3de923a00be43a2`；状态 `success`。

```sql
SELECT DISTINCT total_projects_involved FROM jira__stakeholder_engagement_insights ORDER BY total_projects_involved DESC LIMIT 10
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-063/attempt-01/sql/S19.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-063/attempt-01/sql/S19.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-063/attempt-01/results/S19.rows.jsonl)；完整：True；SHA256：`3d914f085ccf50b84d5c091b2930b055cdfba0433607bec4aca27c45c5d3c73e`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "jira__stakeholder_engagement_insights", "kind": "base", "block": null, "base_tables": ["jira__stakeholder_engagement_insights"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |


## S20

类别 `data`；来源 `query_db`；调用 `15fa77c9686f4e7b95574d6ad5757d8e`；状态 `success`。

```sql
SELECT project_id, project_key, project_name, overall_health_score, complexity_risk_score, total_risk_score, risk_category, primary_risk_factor, recommended_intervention, trajectory_status
FROM jira__project_risk_assessment 
WHERE overall_health_score > 75
ORDER BY overall_health_score DESC
LIMIT 20
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-063/attempt-01/sql/S20.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-063/attempt-01/sql/S20.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-063/attempt-01/results/S20.rows.jsonl)；完整：True；SHA256：`7c29da15054a9cde23a589afa9f8e895a1fae561ac7759c6fdb4accef4ada79a`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "jira__project_risk_assessment", "kind": "base", "block": null, "base_tables": ["jira__project_risk_assessment"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |


## S21

类别 `data`；来源 `query_db`；调用 `f156113162d34fa5b578b8e3cd7d5b8e`；状态 `success`。

```sql
SELECT engagement_risk_status, COUNT(*) as cnt
FROM jira__stakeholder_engagement_insights
GROUP BY engagement_risk_status
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-063/attempt-01/sql/S21.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-063/attempt-01/sql/S21.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-063/attempt-01/results/S21.rows.jsonl)；完整：True；SHA256：`fe33bfead5dc7126a51b6b017062e80c3813eb219ae38b512f9cf601c232a1bb`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "jira__stakeholder_engagement_insights", "kind": "base", "block": null, "base_tables": ["jira__stakeholder_engagement_insights"]}] | [] | ["engagement_risk_status"] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |


## S22

类别 `data`；来源 `query_db`；调用 `eda510c2e0b74a3292a58787c21aeecb`；状态 `success`。

```sql
SELECT project_id, overall_health_score, complexity_risk_score, total_risk_score, risk_category, recommended_intervention, trajectory_status, value_delivery_percentage, team_stability_percentage, resolution_velocity_change_percent, net_issue_growth_30d, high_delay_cost_issues
FROM jira__project_risk_assessment
WHERE overall_health_score > 75
ORDER BY overall_health_score DESC
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-063/attempt-01/sql/S22.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-063/attempt-01/sql/S22.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-063/attempt-01/results/S22.rows.jsonl)；完整：True；SHA256：`326651a52d46c4e246c28e4174e3bf86b90b94ba92619846185c912c5653ec54`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "jira__project_risk_assessment", "kind": "base", "block": null, "base_tables": ["jira__project_risk_assessment"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |


## S23

类别 `data`；来源 `query_db`；调用 `94150eff756542c48406eb3dee6da65b`；状态 `success`。

```sql
SELECT risk_category, COUNT(*) as cnt, AVG(overall_health_score) as avg_health, AVG(total_risk_score) as avg_risk, AVG(complexity_risk_score) as avg_complexity
FROM jira__project_risk_assessment
GROUP BY risk_category
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-063/attempt-01/sql/S23.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-063/attempt-01/sql/S23.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-063/attempt-01/results/S23.rows.jsonl)；完整：True；SHA256：`e14bfaae959cf9f0bfdafb11bcb2b7f72e0081455ea316cf7a393f4d68392310`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "jira__project_risk_assessment", "kind": "base", "block": null, "base_tables": ["jira__project_risk_assessment"]}] | [] | ["risk_category"] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |
| B1 | AVG(overall_health_score) | [{"table": "jira__project_risk_assessment", "column": "overall_health_score"}] | [] | False |
| B1 | AVG(total_risk_score) | [{"table": "jira__project_risk_assessment", "column": "total_risk_score"}] | [] | False |
| B1 | AVG(complexity_risk_score) | [{"table": "jira__project_risk_assessment", "column": "complexity_risk_score"}] | [] | False |


## S24

类别 `data`；来源 `query_db`；调用 `273fc8dea3004153ab01f33750d54939`；状态 `success`。

```sql
SELECT recommended_intervention, COUNT(*) as cnt, AVG(overall_health_score) as avg_health
FROM jira__project_risk_assessment
GROUP BY recommended_intervention
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-063/attempt-01/sql/S24.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-063/attempt-01/sql/S24.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-063/attempt-01/results/S24.rows.jsonl)；完整：True；SHA256：`e7a02bb5bb9b277fd30c0c59d92d930dd8375ce82346baf84240af96e88ffe5d`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "jira__project_risk_assessment", "kind": "base", "block": null, "base_tables": ["jira__project_risk_assessment"]}] | [] | ["recommended_intervention"] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |
| B1 | AVG(overall_health_score) | [{"table": "jira__project_risk_assessment", "column": "overall_health_score"}] | [] | False |


## S25

类别 `data`；来源 `query_db`；调用 `cb610a6b3ee1449aa2e7eb8d8436d8b2`；状态 `success`。

```sql
SELECT trajectory_status, COUNT(*) as cnt, AVG(overall_health_score) as avg_health, AVG(health_risk_score) as avg_health_risk
FROM jira__project_risk_assessment
GROUP BY trajectory_status
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-063/attempt-01/sql/S25.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-063/attempt-01/sql/S25.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-063/attempt-01/results/S25.rows.jsonl)；完整：True；SHA256：`307ea1d5d6fd64c592c251cdff25bf66c9693dbfb9c75d6f51b200379022ac6d`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "jira__project_risk_assessment", "kind": "base", "block": null, "base_tables": ["jira__project_risk_assessment"]}] | [] | ["trajectory_status"] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |
| B1 | AVG(overall_health_score) | [{"table": "jira__project_risk_assessment", "column": "overall_health_score"}] | [] | False |
| B1 | AVG(health_risk_score) | [{"table": "jira__project_risk_assessment", "column": "health_risk_score"}] | [] | False |


## S26

类别 `data`；来源 `query_db`；调用 `38ee7f10ca7f40fcb135fb23e828197e`；状态 `success`。

```sql
SELECT COUNT(DISTINCT user_display_name) FROM jira__stakeholder_engagement_insights
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-063/attempt-01/sql/S26.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-063/attempt-01/sql/S26.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-063/attempt-01/results/S26.rows.jsonl)；完整：True；SHA256：`1f401dcea8166bb67574bf1b38efbffe97c53f87f3cc03a17777a80dae86b48a`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "jira__stakeholder_engagement_insights", "kind": "base", "block": null, "base_tables": ["jira__stakeholder_engagement_insights"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(DISTINCT user_display_name) | [{"table": "jira__stakeholder_engagement_insights", "column": "user_display_name"}] | [] | False |


## S27

类别 `data`；来源 `query_db`；调用 `33726708225948bf9bb7459e373cd2ea`；状态 `success`。

```sql
SELECT COUNT(DISTINCT user_display_name) FROM jira__team_performance_dashboard
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-063/attempt-01/sql/S27.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-063/attempt-01/sql/S27.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-063/attempt-01/results/S27.rows.jsonl)；完整：True；SHA256：`1f401dcea8166bb67574bf1b38efbffe97c53f87f3cc03a17777a80dae86b48a`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "jira__team_performance_dashboard", "kind": "base", "block": null, "base_tables": ["jira__team_performance_dashboard"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(DISTINCT user_display_name) | [{"table": "jira__team_performance_dashboard", "column": "user_display_name"}] | [] | False |


## S28

类别 `data`；来源 `query_db`；调用 `47866b81971f4ae4b0dd47f78b922101`；状态 `failed`。

```sql
SELECT COUNT(DISTINCT user_id) FROM jira__stakeholder_engagement_insights
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-063/attempt-01/sql/S28.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-063/attempt-01/sql/S28.parameters.json)。

错误：`OperationalError('no such column: user_id')`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "jira__stakeholder_engagement_insights", "kind": "base", "block": null, "base_tables": ["jira__stakeholder_engagement_insights"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(DISTINCT user_id) | [{"unknown": "user_id"}] | [] | False |


未解析列血缘：[{"block": "B1", "column": "user_id", "reason": "ambiguous_or_missing_source"}, {"block": "B1", "column": "user_id", "reason": "ambiguous_or_missing_source"}]

## S29

类别 `data`；来源 `query_db`；调用 `3f18ff14f3fc4eea862b7f8853be480d`；状态 `success`。

```sql
SELECT COUNT(DISTINCT user_id) FROM jira__team_performance_dashboard
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-063/attempt-01/sql/S29.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-063/attempt-01/sql/S29.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-063/attempt-01/results/S29.rows.jsonl)；完整：True；SHA256：`7f55456fc3429b0a7398d6571deb2b08fded1545c23079431f0a75a6bfdb0055`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "jira__team_performance_dashboard", "kind": "base", "block": null, "base_tables": ["jira__team_performance_dashboard"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(DISTINCT user_id) | [{"table": "jira__team_performance_dashboard", "column": "user_id"}] | [] | False |


## S30

类别 `data`；来源 `query_db`；调用 `939e78b0b60e4dbd903514f782c27093`；状态 `success`。

```sql
SELECT COUNT(*) as matching_names FROM (
  SELECT DISTINCT user_display_name FROM jira__stakeholder_engagement_insights
  INTERSECT
  SELECT DISTINCT user_display_name FROM jira__team_performance_dashboard
)
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-063/attempt-01/sql/S30.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-063/attempt-01/sql/S30.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-063/attempt-01/results/S30.rows.jsonl)；完整：True；SHA256：`1f401dcea8166bb67574bf1b38efbffe97c53f87f3cc03a17777a80dae86b48a`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "jira__stakeholder_engagement_insights", "kind": "base", "block": null, "base_tables": ["jira__stakeholder_engagement_insights"]}] | [] | [] |
| B2 | [{"alias": "jira__team_performance_dashboard", "kind": "base", "block": null, "base_tables": ["jira__team_performance_dashboard"]}] | [] | [] |
| B3 | [] | [] | [] |
| B4 | [{"alias": "", "kind": "derived", "block": "B3", "base_tables": ["jira__stakeholder_engagement_insights", "jira__team_performance_dashboard"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B4 | COUNT(*) | [] | [] | True |


## S31

类别 `data`；来源 `query_db`；调用 `106f1b1ac49746dc81cdc57447eaac2c`；状态 `success`。

```sql
SELECT user_display_name, COUNT(*) as cnt FROM jira__stakeholder_engagement_insights GROUP BY user_display_name HAVING cnt > 1 LIMIT 5
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-063/attempt-01/sql/S31.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-063/attempt-01/sql/S31.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-063/attempt-01/results/S31.rows.jsonl)；完整：True；SHA256：`82d78581d423264b2672c7511322224c550fe9236036b082f029c09da9690530`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "jira__stakeholder_engagement_insights", "kind": "base", "block": null, "base_tables": ["jira__stakeholder_engagement_insights"]}] | [] | ["user_display_name"] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |


## S32

类别 `data`；来源 `query_db`；调用 `fab180145bd64201aab179032ce7e582`；状态 `success`。

```sql
SELECT user_display_name, COUNT(*) as cnt FROM jira__team_performance_dashboard GROUP BY user_display_name HAVING cnt > 1 LIMIT 5
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-063/attempt-01/sql/S32.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-063/attempt-01/sql/S32.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-063/attempt-01/results/S32.rows.jsonl)；完整：True；SHA256：`bd78be20589cb88ad4e441bd792c8c4f7063df14e832b5197d39adf0d35c7605`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "jira__team_performance_dashboard", "kind": "base", "block": null, "base_tables": ["jira__team_performance_dashboard"]}] | [] | ["user_display_name"] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |


## S33

类别 `data`；来源 `query_db`；调用 `f206026c3d834f568ff37d2c24146c7f`；状态 `success`。

```sql
SELECT DISTINCT current_lifecycle_stage FROM jira__team_performance_dashboard
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-063/attempt-01/sql/S33.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-063/attempt-01/sql/S33.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-063/attempt-01/results/S33.rows.jsonl)；完整：True；SHA256：`f4299467d79f48cbfe5e35a230343ccd72feacfb1e6751f2db2523c869b5a921`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "jira__team_performance_dashboard", "kind": "base", "block": null, "base_tables": ["jira__team_performance_dashboard"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |


## S34

类别 `data`；来源 `query_db`；调用 `d6c9173d5f57422aba28cb717b4e19a8`；状态 `success`。

```sql
SELECT DISTINCT current_pattern_type FROM jira__team_performance_dashboard
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-063/attempt-01/sql/S34.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-063/attempt-01/sql/S34.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-063/attempt-01/results/S34.rows.jsonl)；完整：True；SHA256：`8e4298a24ee8185ede57b7b5a35619e77c858bc051c648a636fad1f45becea81`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "jira__team_performance_dashboard", "kind": "base", "block": null, "base_tables": ["jira__team_performance_dashboard"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |


## S35

类别 `data`；来源 `query_db`；调用 `f786716f35ec4a03a4ae6063007c6e69`；状态 `success`。

```sql
SELECT DISTINCT current_engagement_tier FROM jira__team_performance_dashboard
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-063/attempt-01/sql/S35.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-063/attempt-01/sql/S35.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-063/attempt-01/results/S35.rows.jsonl)；完整：True；SHA256：`19e3524e8545e41ecc9eac969ad96c7b5a17c63cbb45453abfcf9227cae3a7ca`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "jira__team_performance_dashboard", "kind": "base", "block": null, "base_tables": ["jira__team_performance_dashboard"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |


## S36

类别 `data`；来源 `query_db`；调用 `bf703bd60726470db96af6c1b244b760`；状态 `success`。

```sql
SELECT DISTINCT stakeholder_archetype FROM jira__stakeholder_engagement_insights
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-063/attempt-01/sql/S36.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-063/attempt-01/sql/S36.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-063/attempt-01/results/S36.rows.jsonl)；完整：True；SHA256：`c0b8659a0f44aa322c3698f343a5d2b301b187cc830efef2a73bb2fc132b5e4d`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "jira__stakeholder_engagement_insights", "kind": "base", "block": null, "base_tables": ["jira__stakeholder_engagement_insights"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |


## S37

类别 `data`；来源 `query_db`；调用 `8e88680567d347bc9e9e54c437860b0a`；状态 `success`。

```sql
SELECT DISTINCT influence_level FROM jira__stakeholder_engagement_insights
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-063/attempt-01/sql/S37.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-063/attempt-01/sql/S37.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-063/attempt-01/results/S37.rows.jsonl)；完整：True；SHA256：`0c02e90dd31a97af5cbf4cde2d9792a60ec6e1fa2ba989843fa89c6d7e1ceca4`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "jira__stakeholder_engagement_insights", "kind": "base", "block": null, "base_tables": ["jira__stakeholder_engagement_insights"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |


## S38

类别 `data`；来源 `query_db`；调用 `dbca90d1ffa74bab9740be2e8529f608`；状态 `success`。

```sql
SELECT 
  CASE WHEN overall_health_score > 75 THEN 'health>75' ELSE 'health<=75' END as health_band,
  risk_category,
  COUNT(*) as cnt,
  AVG(overall_health_score) as avg_health,
  AVG(total_risk_score) as avg_total_risk,
  AVG(complexity_risk_score) as avg_complexity,
  AVG(success_probability) as avg_success
FROM jira__project_risk_assessment
GROUP BY health_band, risk_category
ORDER BY health_band, cnt DESC
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-063/attempt-01/sql/S38.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-063/attempt-01/sql/S38.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-063/attempt-01/results/S38.rows.jsonl)；完整：True；SHA256：`feb6b5c493273a5f5049e240dbd6225aaa0192339562e1f0ee0955caf421606e`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "jira__project_risk_assessment", "kind": "base", "block": null, "base_tables": ["jira__project_risk_assessment"]}] | [] | ["CASE WHEN overall_health_score > 75 THEN 'health>75' ELSE 'health<=75' END", "risk_category"] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |
| B1 | AVG(overall_health_score) | [{"table": "jira__project_risk_assessment", "column": "overall_health_score"}] | [] | False |
| B1 | AVG(total_risk_score) | [{"table": "jira__project_risk_assessment", "column": "total_risk_score"}] | [] | False |
| B1 | AVG(complexity_risk_score) | [{"table": "jira__project_risk_assessment", "column": "complexity_risk_score"}] | [] | False |
| B1 | AVG(success_probability) | [{"table": "jira__project_risk_assessment", "column": "success_probability"}] | [] | False |


## S39

类别 `data`；来源 `query_db`；调用 `f6c41ea693b440bcb4c1378b0947d446`；状态 `success`。

```sql
SELECT primary_risk_factor, COUNT(*) as cnt, AVG(overall_health_score) as avg_health
FROM jira__project_risk_assessment
GROUP BY primary_risk_factor
ORDER BY cnt DESC
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-063/attempt-01/sql/S39.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-063/attempt-01/sql/S39.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-063/attempt-01/results/S39.rows.jsonl)；完整：True；SHA256：`421a40e7210143b85a6fab0df9b9f1a2b824c82da8ce9620446dbd32b6592e73`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "jira__project_risk_assessment", "kind": "base", "block": null, "base_tables": ["jira__project_risk_assessment"]}] | [] | ["primary_risk_factor"] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |
| B1 | AVG(overall_health_score) | [{"table": "jira__project_risk_assessment", "column": "overall_health_score"}] | [] | False |


## S40

类别 `data`；来源 `query_db`；调用 `16c2cb91d900427c934a608cc9e97c08`；状态 `success`。

```sql
SELECT 
  CASE WHEN overall_performance_score > 80 THEN 'perf>80' ELSE 'perf<=80' END as perf_band,
  COUNT(*) as cnt,
  AVG(overall_performance_score) as avg_perf,
  AVG(avg_resolution_days) as avg_res_days,
  AVG(estimate_accuracy_percentage) as avg_est_acc,
  AVG(consistency_percentage) as avg_consistency
FROM jira__team_performance_dashboard
GROUP BY perf_band
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-063/attempt-01/sql/S40.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-063/attempt-01/sql/S40.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-063/attempt-01/results/S40.rows.jsonl)；完整：True；SHA256：`dde04eb4b2051832c9944995939c8c9f93c55f990a97152e21ae20d0737ed419`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "jira__team_performance_dashboard", "kind": "base", "block": null, "base_tables": ["jira__team_performance_dashboard"]}] | [] | ["CASE WHEN overall_performance_score > 80 THEN 'perf>80' ELSE 'perf<=80' END"] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |
| B1 | AVG(overall_performance_score) | [{"table": "jira__team_performance_dashboard", "column": "overall_performance_score"}] | [] | False |
| B1 | AVG(avg_resolution_days) | [{"table": "jira__team_performance_dashboard", "column": "avg_resolution_days"}] | [] | False |
| B1 | AVG(estimate_accuracy_percentage) | [{"table": "jira__team_performance_dashboard", "column": "estimate_accuracy_percentage"}] | [] | False |
| B1 | AVG(consistency_percentage) | [{"table": "jira__team_performance_dashboard", "column": "consistency_percentage"}] | [] | False |


## S41

类别 `data`；来源 `query_db`；调用 `c4b9b849bac94768a58d74a333e18175`；状态 `success`。

```sql
SELECT performance_tier, COUNT(*) as cnt, AVG(overall_performance_score) as avg_perf, AVG(resolution_rate_percentage) as avg_res_rate
FROM jira__team_performance_dashboard
GROUP BY performance_tier
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-063/attempt-01/sql/S41.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-063/attempt-01/sql/S41.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-063/attempt-01/results/S41.rows.jsonl)；完整：True；SHA256：`487805bd65f30aa56ace7f8771a9a5ce001513f6164a47bea2fd9b72562fc9d8`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "jira__team_performance_dashboard", "kind": "base", "block": null, "base_tables": ["jira__team_performance_dashboard"]}] | [] | ["performance_tier"] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |
| B1 | AVG(overall_performance_score) | [{"table": "jira__team_performance_dashboard", "column": "overall_performance_score"}] | [] | False |
| B1 | AVG(resolution_rate_percentage) | [{"table": "jira__team_performance_dashboard", "column": "resolution_rate_percentage"}] | [] | False |


## S42

类别 `data`；来源 `query_db`；调用 `c56ebd29392f4f959ccf80d984b59a6a`；状态 `success`。

```sql
SELECT COUNT(*) as overlap FROM (
  SELECT DISTINCT stakeholder_id FROM jira__stakeholder_engagement_insights
  INTERSECT
  SELECT DISTINCT user_id FROM jira__team_performance_dashboard
)
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-063/attempt-01/sql/S42.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-063/attempt-01/sql/S42.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-063/attempt-01/results/S42.rows.jsonl)；完整：True；SHA256：`a81c1f1f0b1ab19539cdc200b797bee0a994b8032a058c100f96c763bd05f1f6`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "jira__stakeholder_engagement_insights", "kind": "base", "block": null, "base_tables": ["jira__stakeholder_engagement_insights"]}] | [] | [] |
| B2 | [{"alias": "jira__team_performance_dashboard", "kind": "base", "block": null, "base_tables": ["jira__team_performance_dashboard"]}] | [] | [] |
| B3 | [] | [] | [] |
| B4 | [{"alias": "", "kind": "derived", "block": "B3", "base_tables": ["jira__stakeholder_engagement_insights", "jira__team_performance_dashboard"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B4 | COUNT(*) | [] | [] | True |


## S43

类别 `data`；来源 `query_db`；调用 `39b4d9c020594034a52f718094264099`；状态 `success`。

```sql
SELECT COUNT(*) as overlap2 FROM (
  SELECT DISTINCT user_id FROM jira__team_performance_dashboard
  INTERSECT
  SELECT DISTINCT stakeholder_id FROM jira__stakeholder_engagement_insights
)
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-063/attempt-01/sql/S43.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-063/attempt-01/sql/S43.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-063/attempt-01/results/S43.rows.jsonl)；完整：True；SHA256：`a81c1f1f0b1ab19539cdc200b797bee0a994b8032a058c100f96c763bd05f1f6`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "jira__team_performance_dashboard", "kind": "base", "block": null, "base_tables": ["jira__team_performance_dashboard"]}] | [] | [] |
| B2 | [{"alias": "jira__stakeholder_engagement_insights", "kind": "base", "block": null, "base_tables": ["jira__stakeholder_engagement_insights"]}] | [] | [] |
| B3 | [] | [] | [] |
| B4 | [{"alias": "", "kind": "derived", "block": "B3", "base_tables": ["jira__stakeholder_engagement_insights", "jira__team_performance_dashboard"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B4 | COUNT(*) | [] | [] | True |


## S44

类别 `data`；来源 `query_db`；调用 `ea9821f55b6d4715bf77e8a63e740ad3`；状态 `success`。

```sql
SELECT stakeholder_id, user_display_name FROM jira__stakeholder_engagement_insights LIMIT 8
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-063/attempt-01/sql/S44.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-063/attempt-01/sql/S44.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-063/attempt-01/results/S44.rows.jsonl)；完整：True；SHA256：`7f5fabb9f8c59aaae0d1e582e9a64aec32f8c121a2c47b9d6e4d05304564d66a`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "jira__stakeholder_engagement_insights", "kind": "base", "block": null, "base_tables": ["jira__stakeholder_engagement_insights"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |


## S45

类别 `data`；来源 `query_db`；调用 `2aa18adff6aa4ff3aacf9bb309a14eaf`；状态 `success`。

```sql
-- Comprehensive analysis of false prosperity projects
WITH health_groups AS (
  SELECT 
    CASE WHEN overall_health_score > 75 THEN 'High Health' ELSE 'Low Health' END as health_group,
    CASE WHEN risk_category IN ('Critical Risk', 'High Risk') AND complexity_risk_score > 30 THEN 'High Risk Cluster' ELSE 'Normal Risk' END as risk_cluster,
    COUNT(*) as cnt,
    AVG(overall_health_score) as avg_health,
    AVG(total_risk_score) as avg_total_risk,
    AVG(complexity_risk_score) as avg_complexity,
    AVG(value_delivery_percentage) as avg_delivery_pct,
    AVG(team_stability_percentage) as avg_stability,
    AVG(success_probability) as avg_success_prob,
    AVG(resolution_velocity_change_percent) as avg_vel_change,
    AVG(health_risk_score) as avg_health_risk,
    AVG(schedule_risk_score) as avg_schedule_risk,
    AVG(resource_risk_score) as avg_resource_risk
  FROM jira__project_risk_assessment
  GROUP BY health_group, risk_cluster
)
SELECT * FROM health_groups ORDER BY health_group, risk_cluster
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-063/attempt-01/sql/S45.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-063/attempt-01/sql/S45.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-063/attempt-01/results/S45.rows.jsonl)；完整：True；SHA256：`8eef093fff59b27bb3dd5039d17b06bcca094637fbf1808701b3d7b5b345844e`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "jira__project_risk_assessment", "kind": "base", "block": null, "base_tables": ["jira__project_risk_assessment"]}] | [] | ["CASE WHEN overall_health_score > 75 THEN 'High Health' ELSE 'Low Health' END", "CASE WHEN risk_category IN ('Critical Risk', 'High Risk') AND complexity_risk_score > 30 THEN 'High Risk Cluster' ELSE 'Normal Risk' END"] |
| B2 | [{"alias": "health_groups", "kind": "derived", "block": "B1", "base_tables": ["jira__project_risk_assessment"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |
| B1 | AVG(overall_health_score) | [{"table": "jira__project_risk_assessment", "column": "overall_health_score"}] | [] | False |
| B1 | AVG(total_risk_score) | [{"table": "jira__project_risk_assessment", "column": "total_risk_score"}] | [] | False |
| B1 | AVG(complexity_risk_score) | [{"table": "jira__project_risk_assessment", "column": "complexity_risk_score"}] | [] | False |
| B1 | AVG(value_delivery_percentage) | [{"table": "jira__project_risk_assessment", "column": "value_delivery_percentage"}] | [] | False |
| B1 | AVG(team_stability_percentage) | [{"table": "jira__project_risk_assessment", "column": "team_stability_percentage"}] | [] | False |
| B1 | AVG(success_probability) | [{"table": "jira__project_risk_assessment", "column": "success_probability"}] | [] | False |
| B1 | AVG(resolution_velocity_change_percent) | [{"table": "jira__project_risk_assessment", "column": "resolution_velocity_change_percent"}] | [] | False |
| B1 | AVG(health_risk_score) | [{"table": "jira__project_risk_assessment", "column": "health_risk_score"}] | [] | False |
| B1 | AVG(schedule_risk_score) | [{"table": "jira__project_risk_assessment", "column": "schedule_risk_score"}] | [] | False |
| B1 | AVG(resource_risk_score) | [{"table": "jira__project_risk_assessment", "column": "resource_risk_score"}] | [] | False |


## S46

类别 `data`；来源 `query_db`；调用 `05fe7625f8b9487997d3b3d2a22e89e7`；状态 `success`。

```sql
SELECT project_id, project_key, project_name, overall_health_score, total_risk_score, complexity_risk_score, health_risk_score, schedule_risk_score, resource_risk_score, scope_risk_score, value_delivery_percentage, team_stability_percentage, resolution_velocity_change_percent, net_issue_growth_30d, high_delay_cost_issues, success_probability, trajectory_status, risk_category, primary_risk_driver, recommended_intervention
FROM jira__project_risk_assessment
WHERE overall_health_score > 75 AND risk_category IN ('Critical Risk', 'High Risk') AND complexity_risk_score > 30
ORDER BY overall_health_score DESC
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-063/attempt-01/sql/S46.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-063/attempt-01/sql/S46.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-063/attempt-01/results/S46.rows.jsonl)；完整：True；SHA256：`1ca8d105ba4b4a816c9c4b818d2a9b6702b087789dcb08d262929a58ab105a69`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "jira__project_risk_assessment", "kind": "base", "block": null, "base_tables": ["jira__project_risk_assessment"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |


## S47

类别 `data`；来源 `query_db`；调用 `88d0c563c251412fab2c0aa368b722e3`；状态 `success`。

```sql
-- Join team performance and stakeholder data on user ID
SELECT 
  t.overall_performance_score > 80 as high_performer,
  s.engagement_risk_status,
  COUNT(*) as cnt
FROM jira__team_performance_dashboard t
JOIN jira__stakeholder_engagement_insights s ON t.user_id = s.stakeholder_id
GROUP BY high_performer, s.engagement_risk_status
ORDER BY high_performer, s.engagement_risk_status
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-063/attempt-01/sql/S47.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-063/attempt-01/sql/S47.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-063/attempt-01/results/S47.rows.jsonl)；完整：True；SHA256：`45556fbe45fee2458c3adc922b773e984abd5684d90d43106be8c95346a820ab`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "t", "kind": "base", "block": null, "base_tables": ["jira__team_performance_dashboard"]}, {"alias": "s", "kind": "base", "block": null, "base_tables": ["jira__stakeholder_engagement_insights"]}] | [{"type": "INNER", "right": "jira__stakeholder_engagement_insights AS s", "on": "t.user_id = s.stakeholder_id", "using": []}] | ["t.overall_performance_score > 80", "s.engagement_risk_status"] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |


## S48

类别 `data`；来源 `query_db`；调用 `c48ea2f6290d40b9adc443eea400c188`；状态 `success`。

```sql
-- Team performance patterns for high performers
SELECT 
  s.engagement_risk_status,
  CASE WHEN t.overall_performance_score > 80 THEN 'High Perf' ELSE 'Low Perf' END as perf_group,
  COUNT(*) as cnt,
  AVG(t.resolution_rate_percentage) as avg_res_rate,
  AVG(t.avg_resolution_days) as avg_res_days,
  AVG(t.estimate_accuracy_percentage) as avg_est_acc,
  AVG(t.consistency_percentage) as avg_consistency,
  AVG(t.unique_collaborators_on_issues) as avg_collaborators,
  AVG(t.at_churn_risk) as avg_churn,
  AVG(t.poor_estimation) as avg_poor_est,
  AVG(t.inactive_recently) as avg_inactive
FROM jira__team_performance_dashboard t
JOIN jira__stakeholder_engagement_insights s ON t.user_id = s.stakeholder_id
GROUP BY s.engagement_risk_status, perf_group
ORDER BY s.engagement_risk_status, perf_group
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-063/attempt-01/sql/S48.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-063/attempt-01/sql/S48.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-063/attempt-01/results/S48.rows.jsonl)；完整：True；SHA256：`d55e6df741f47ed21ddea95efbb37b3f4e501d3a70f2cc783867af49a06b04fd`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "t", "kind": "base", "block": null, "base_tables": ["jira__team_performance_dashboard"]}, {"alias": "s", "kind": "base", "block": null, "base_tables": ["jira__stakeholder_engagement_insights"]}] | [{"type": "INNER", "right": "jira__stakeholder_engagement_insights AS s", "on": "t.user_id = s.stakeholder_id", "using": []}] | ["s.engagement_risk_status", "CASE WHEN t.overall_performance_score > 80 THEN 'High Perf' ELSE 'Low Perf' END"] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |
| B1 | AVG(t.resolution_rate_percentage) | [{"table": "jira__team_performance_dashboard", "column": "resolution_rate_percentage"}] | [] | False |
| B1 | AVG(t.avg_resolution_days) | [{"table": "jira__team_performance_dashboard", "column": "avg_resolution_days"}] | [] | False |
| B1 | AVG(t.estimate_accuracy_percentage) | [{"table": "jira__team_performance_dashboard", "column": "estimate_accuracy_percentage"}] | [] | False |
| B1 | AVG(t.consistency_percentage) | [{"table": "jira__team_performance_dashboard", "column": "consistency_percentage"}] | [] | False |
| B1 | AVG(t.unique_collaborators_on_issues) | [{"table": "jira__team_performance_dashboard", "column": "unique_collaborators_on_issues"}] | [] | False |
| B1 | AVG(t.at_churn_risk) | [{"table": "jira__team_performance_dashboard", "column": "at_churn_risk"}] | [] | False |
| B1 | AVG(t.poor_estimation) | [{"table": "jira__team_performance_dashboard", "column": "poor_estimation"}] | [] | False |
| B1 | AVG(t.inactive_recently) | [{"table": "jira__team_performance_dashboard", "column": "inactive_recently"}] | [] | False |


## S49

类别 `data`；来源 `query_db`；调用 `12dec6e933fd4d828034105804e6ff64`；状态 `success`。

```sql
-- Stakeholder characteristics by engagement risk status
SELECT 
  engagement_risk_status,
  COUNT(*) as cnt,
  AVG(total_engagement_score) as avg_engagement,
  AVG(engagement_breadth_score) as avg_breadth,
  AVG(engagement_depth_score) as avg_depth,
  AVG(engagement_quality_score) as avg_quality,
  AVG(engagement_impact_score) as avg_impact,
  AVG(cross_functional_projects) as avg_cross_func,
  AVG(direct_network_connections) as avg_network,
  AVG(total_outbound_influence) as avg_outbound,
  AVG(total_inbound_influence) as avg_inbound,
  AVG(strategic_value_score) as avg_strategic,
  AVG(total_comments_authored) as avg_comments,
  AVG(issues_assigned) as avg_assigned,
  AVG(issues_reported) as avg_reported
FROM jira__stakeholder_engagement_insights
GROUP BY engagement_risk_status
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-063/attempt-01/sql/S49.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-063/attempt-01/sql/S49.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-063/attempt-01/results/S49.rows.jsonl)；完整：True；SHA256：`06d6e74f15a7519a168340af018d7bde5513da0e536902edbeb662f5392b8353`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "jira__stakeholder_engagement_insights", "kind": "base", "block": null, "base_tables": ["jira__stakeholder_engagement_insights"]}] | [] | ["engagement_risk_status"] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |
| B1 | AVG(total_engagement_score) | [{"table": "jira__stakeholder_engagement_insights", "column": "total_engagement_score"}] | [] | False |
| B1 | AVG(engagement_breadth_score) | [{"table": "jira__stakeholder_engagement_insights", "column": "engagement_breadth_score"}] | [] | False |
| B1 | AVG(engagement_depth_score) | [{"table": "jira__stakeholder_engagement_insights", "column": "engagement_depth_score"}] | [] | False |
| B1 | AVG(engagement_quality_score) | [{"table": "jira__stakeholder_engagement_insights", "column": "engagement_quality_score"}] | [] | False |
| B1 | AVG(engagement_impact_score) | [{"table": "jira__stakeholder_engagement_insights", "column": "engagement_impact_score"}] | [] | False |
| B1 | AVG(cross_functional_projects) | [{"table": "jira__stakeholder_engagement_insights", "column": "cross_functional_projects"}] | [] | False |
| B1 | AVG(direct_network_connections) | [{"table": "jira__stakeholder_engagement_insights", "column": "direct_network_connections"}] | [] | False |
| B1 | AVG(total_outbound_influence) | [{"table": "jira__stakeholder_engagement_insights", "column": "total_outbound_influence"}] | [] | False |
| B1 | AVG(total_inbound_influence) | [{"table": "jira__stakeholder_engagement_insights", "column": "total_inbound_influence"}] | [] | False |
| B1 | AVG(strategic_value_score) | [{"table": "jira__stakeholder_engagement_insights", "column": "strategic_value_score"}] | [] | False |
| B1 | AVG(total_comments_authored) | [{"table": "jira__stakeholder_engagement_insights", "column": "total_comments_authored"}] | [] | False |
| B1 | AVG(issues_assigned) | [{"table": "jira__stakeholder_engagement_insights", "column": "issues_assigned"}] | [] | False |
| B1 | AVG(issues_reported) | [{"table": "jira__stakeholder_engagement_insights", "column": "issues_reported"}] | [] | False |


## S50

类别 `data`；来源 `query_db`；调用 `d4abf0680ca642b0b61760da555273e0`；状态 `success`。

```sql
-- Project metrics: False prosperity vs others
SELECT 
  CASE WHEN overall_health_score > 75 AND risk_category IN ('Critical Risk','High Risk') AND complexity_risk_score > 30 THEN 'FalseProsperity' ELSE 'Other' END as group_label,
  COUNT(*) as cnt,
  ROUND(AVG(overall_health_score),2) as avg_health,
  ROUND(AVG(total_risk_score),2) as avg_total_risk,
  ROUND(AVG(health_risk_score),2) as avg_health_risk,
  ROUND(AVG(schedule_risk_score),2) as avg_schedule_risk,
  ROUND(AVG(resource_risk_score),2) as avg_resource_risk,
  ROUND(AVG(complexity_risk_score),2) as avg_complexity_risk,
  ROUND(AVG(scope_risk_score),2) as avg_scope_risk,
  ROUND(AVG(success_probability),3) as avg_success_prob,
  ROUND(AVG(value_delivery_percentage),2) as avg_delivery_pct,
  ROUND(AVG(team_stability_percentage),2) as avg_stability,
  ROUND(AVG(resolution_velocity_change_percent),2) as avg_vel_change,
  ROUND(AVG(net_issue_growth_30d),2) as avg_issue_growth,
  ROUND(AVG(high_delay_cost_issues),2) as avg_delay_issues,
  ROUND(AVG(total_hours_invested),2) as avg_hours,
  ROUND(AVG(estimated_project_value_points),2) as avg_est_value,
  ROUND(AVG(delivered_value_points),2) as avg_delivered_value,
  ROUND(AVG(sprint_adoption_rate),2) as avg_sprint_adopt
FROM jira__project_risk_assessment
GROUP BY group_label
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-063/attempt-01/sql/S50.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-063/attempt-01/sql/S50.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-063/attempt-01/results/S50.rows.jsonl)；完整：True；SHA256：`1a2e0561585714f9dabfadaccbc77e3f5602b084c7ae85a74d224fc03eed9396`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "jira__project_risk_assessment", "kind": "base", "block": null, "base_tables": ["jira__project_risk_assessment"]}] | [] | ["CASE WHEN overall_health_score > 75 AND risk_category IN ('Critical Risk', 'High Risk') AND complexity_risk_score > 30 THEN 'FalseProsperity' ELSE 'Other' END"] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |
| B1 | AVG(overall_health_score) | [{"table": "jira__project_risk_assessment", "column": "overall_health_score"}] | [] | False |
| B1 | AVG(total_risk_score) | [{"table": "jira__project_risk_assessment", "column": "total_risk_score"}] | [] | False |
| B1 | AVG(health_risk_score) | [{"table": "jira__project_risk_assessment", "column": "health_risk_score"}] | [] | False |
| B1 | AVG(schedule_risk_score) | [{"table": "jira__project_risk_assessment", "column": "schedule_risk_score"}] | [] | False |
| B1 | AVG(resource_risk_score) | [{"table": "jira__project_risk_assessment", "column": "resource_risk_score"}] | [] | False |
| B1 | AVG(complexity_risk_score) | [{"table": "jira__project_risk_assessment", "column": "complexity_risk_score"}] | [] | False |
| B1 | AVG(scope_risk_score) | [{"table": "jira__project_risk_assessment", "column": "scope_risk_score"}] | [] | False |
| B1 | AVG(success_probability) | [{"table": "jira__project_risk_assessment", "column": "success_probability"}] | [] | False |
| B1 | AVG(value_delivery_percentage) | [{"table": "jira__project_risk_assessment", "column": "value_delivery_percentage"}] | [] | False |
| B1 | AVG(team_stability_percentage) | [{"table": "jira__project_risk_assessment", "column": "team_stability_percentage"}] | [] | False |
| B1 | AVG(resolution_velocity_change_percent) | [{"table": "jira__project_risk_assessment", "column": "resolution_velocity_change_percent"}] | [] | False |
| B1 | AVG(net_issue_growth_30d) | [{"table": "jira__project_risk_assessment", "column": "net_issue_growth_30d"}] | [] | False |
| B1 | AVG(high_delay_cost_issues) | [{"table": "jira__project_risk_assessment", "column": "high_delay_cost_issues"}] | [] | False |
| B1 | AVG(total_hours_invested) | [{"table": "jira__project_risk_assessment", "column": "total_hours_invested"}] | [] | False |
| B1 | AVG(estimated_project_value_points) | [{"table": "jira__project_risk_assessment", "column": "estimated_project_value_points"}] | [] | False |
| B1 | AVG(delivered_value_points) | [{"table": "jira__project_risk_assessment", "column": "delivered_value_points"}] | [] | False |
| B1 | AVG(sprint_adoption_rate) | [{"table": "jira__project_risk_assessment", "column": "sprint_adoption_rate"}] | [] | False |


## S51

类别 `data`；来源 `python`；调用 `19069280b997468e9c42bf0b18328acc`；状态 `success`。

```sql
SELECT * FROM jira__project_risk_assessment
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-063/attempt-01/sql/S51.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-063/attempt-01/sql/S51.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-063/attempt-01/results/S51.rows.jsonl)；完整：True；SHA256：`c71bf71f4d1d59352557a5c253a467ce127e6980655f906ed16dec42b33428f0`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "jira__project_risk_assessment", "kind": "base", "block": null, "base_tables": ["jira__project_risk_assessment"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |


## S52

类别 `data`；来源 `python`；调用 `19069280b997468e9c42bf0b18328acc`；状态 `success`。

```sql
SELECT * FROM jira__stakeholder_engagement_insights
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-063/attempt-01/sql/S52.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-063/attempt-01/sql/S52.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-063/attempt-01/results/S52.rows.jsonl)；完整：True；SHA256：`d0d6a16e67027655ab8eed61328494c11c418b1d936b7306da2c844c2d0e870a`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "jira__stakeholder_engagement_insights", "kind": "base", "block": null, "base_tables": ["jira__stakeholder_engagement_insights"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |


## S53

类别 `data`；来源 `python`；调用 `19069280b997468e9c42bf0b18328acc`；状态 `success`。

```sql
SELECT * FROM jira__team_performance_dashboard
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-063/attempt-01/sql/S53.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-063/attempt-01/sql/S53.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-063/attempt-01/results/S53.rows.jsonl)；完整：True；SHA256：`d27f57954de59236fc8226941690940774c5ece1a0e05529f7865256604d557b`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "jira__team_performance_dashboard", "kind": "base", "block": null, "base_tables": ["jira__team_performance_dashboard"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |


## S54

类别 `data`；来源 `python`；调用 `7cb75b145f4d4ebcabf9d6ab46c723a4`；状态 `success`。

```sql
SELECT * FROM jira__project_risk_assessment
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-063/attempt-01/sql/S54.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-063/attempt-01/sql/S54.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-063/attempt-01/results/S54.rows.jsonl)；完整：True；SHA256：`c71bf71f4d1d59352557a5c253a467ce127e6980655f906ed16dec42b33428f0`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "jira__project_risk_assessment", "kind": "base", "block": null, "base_tables": ["jira__project_risk_assessment"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |


## S55

类别 `data`；来源 `python`；调用 `7cb75b145f4d4ebcabf9d6ab46c723a4`；状态 `success`。

```sql
SELECT * FROM jira__stakeholder_engagement_insights
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-063/attempt-01/sql/S55.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-063/attempt-01/sql/S55.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-063/attempt-01/results/S55.rows.jsonl)；完整：True；SHA256：`d0d6a16e67027655ab8eed61328494c11c418b1d936b7306da2c844c2d0e870a`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "jira__stakeholder_engagement_insights", "kind": "base", "block": null, "base_tables": ["jira__stakeholder_engagement_insights"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |


## S56

类别 `data`；来源 `python`；调用 `7cb75b145f4d4ebcabf9d6ab46c723a4`；状态 `success`。

```sql
SELECT * FROM jira__team_performance_dashboard
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-063/attempt-01/sql/S56.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-063/attempt-01/sql/S56.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-063/attempt-01/results/S56.rows.jsonl)；完整：True；SHA256：`d27f57954de59236fc8226941690940774c5ece1a0e05529f7865256604d557b`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "jira__team_performance_dashboard", "kind": "base", "block": null, "base_tables": ["jira__team_performance_dashboard"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |


## S57

类别 `data`；来源 `python`；调用 `77bf63eb72f549138d96f1a63ddd60a7`；状态 `success`。

```sql
SELECT * FROM jira__project_risk_assessment
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-063/attempt-01/sql/S57.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-063/attempt-01/sql/S57.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-063/attempt-01/results/S57.rows.jsonl)；完整：True；SHA256：`c71bf71f4d1d59352557a5c253a467ce127e6980655f906ed16dec42b33428f0`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "jira__project_risk_assessment", "kind": "base", "block": null, "base_tables": ["jira__project_risk_assessment"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |


## S58

类别 `data`；来源 `python`；调用 `77bf63eb72f549138d96f1a63ddd60a7`；状态 `success`。

```sql
SELECT * FROM jira__stakeholder_engagement_insights
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-063/attempt-01/sql/S58.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-063/attempt-01/sql/S58.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-063/attempt-01/results/S58.rows.jsonl)；完整：True；SHA256：`d0d6a16e67027655ab8eed61328494c11c418b1d936b7306da2c844c2d0e870a`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "jira__stakeholder_engagement_insights", "kind": "base", "block": null, "base_tables": ["jira__stakeholder_engagement_insights"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |


## S59

类别 `data`；来源 `python`；调用 `77bf63eb72f549138d96f1a63ddd60a7`；状态 `success`。

```sql
SELECT * FROM jira__team_performance_dashboard
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-063/attempt-01/sql/S59.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-063/attempt-01/sql/S59.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-063/attempt-01/results/S59.rows.jsonl)；完整：True；SHA256：`d27f57954de59236fc8226941690940774c5ece1a0e05529f7865256604d557b`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "jira__team_performance_dashboard", "kind": "base", "block": null, "base_tables": ["jira__team_performance_dashboard"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |


## S60

类别 `data`；来源 `python`；调用 `874d5fe2316240929e805025b2767f10`；状态 `success`。

```sql
SELECT * FROM jira__project_risk_assessment
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-063/attempt-01/sql/S60.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-063/attempt-01/sql/S60.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-063/attempt-01/results/S60.rows.jsonl)；完整：True；SHA256：`c71bf71f4d1d59352557a5c253a467ce127e6980655f906ed16dec42b33428f0`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "jira__project_risk_assessment", "kind": "base", "block": null, "base_tables": ["jira__project_risk_assessment"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |


## S61

类别 `data`；来源 `python`；调用 `874d5fe2316240929e805025b2767f10`；状态 `success`。

```sql
SELECT * FROM jira__stakeholder_engagement_insights
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-063/attempt-01/sql/S61.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-063/attempt-01/sql/S61.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-063/attempt-01/results/S61.rows.jsonl)；完整：True；SHA256：`d0d6a16e67027655ab8eed61328494c11c418b1d936b7306da2c844c2d0e870a`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "jira__stakeholder_engagement_insights", "kind": "base", "block": null, "base_tables": ["jira__stakeholder_engagement_insights"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |


## S62

类别 `data`；来源 `python`；调用 `874d5fe2316240929e805025b2767f10`；状态 `success`。

```sql
SELECT * FROM jira__team_performance_dashboard
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-063/attempt-01/sql/S62.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-063/attempt-01/sql/S62.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-063/attempt-01/results/S62.rows.jsonl)；完整：True；SHA256：`d27f57954de59236fc8226941690940774c5ece1a0e05529f7865256604d557b`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "jira__team_performance_dashboard", "kind": "base", "block": null, "base_tables": ["jira__team_performance_dashboard"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |


## S63

类别 `data`；来源 `python`；调用 `321e7ffdf5e1470cbfb6fe69370d11bd`；状态 `success`。

```sql
SELECT * FROM jira__project_risk_assessment
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-063/attempt-01/sql/S63.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-063/attempt-01/sql/S63.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-063/attempt-01/results/S63.rows.jsonl)；完整：True；SHA256：`c71bf71f4d1d59352557a5c253a467ce127e6980655f906ed16dec42b33428f0`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "jira__project_risk_assessment", "kind": "base", "block": null, "base_tables": ["jira__project_risk_assessment"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |


## S64

类别 `data`；来源 `python`；调用 `321e7ffdf5e1470cbfb6fe69370d11bd`；状态 `success`。

```sql
SELECT * FROM jira__stakeholder_engagement_insights
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-063/attempt-01/sql/S64.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-063/attempt-01/sql/S64.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-063/attempt-01/results/S64.rows.jsonl)；完整：True；SHA256：`d0d6a16e67027655ab8eed61328494c11c418b1d936b7306da2c844c2d0e870a`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "jira__stakeholder_engagement_insights", "kind": "base", "block": null, "base_tables": ["jira__stakeholder_engagement_insights"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |


## S65

类别 `data`；来源 `python`；调用 `321e7ffdf5e1470cbfb6fe69370d11bd`；状态 `success`。

```sql
SELECT * FROM jira__team_performance_dashboard
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-063/attempt-01/sql/S65.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-063/attempt-01/sql/S65.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-063/attempt-01/results/S65.rows.jsonl)；完整：True；SHA256：`d27f57954de59236fc8226941690940774c5ece1a0e05529f7865256604d557b`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "jira__team_performance_dashboard", "kind": "base", "block": null, "base_tables": ["jira__team_performance_dashboard"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |


## S66

类别 `data`；来源 `python`；调用 `b85723389f3d4edab428a075344be7e8`；状态 `success`。

```sql
SELECT * FROM jira__project_risk_assessment
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-063/attempt-01/sql/S66.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-063/attempt-01/sql/S66.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-063/attempt-01/results/S66.rows.jsonl)；完整：True；SHA256：`c71bf71f4d1d59352557a5c253a467ce127e6980655f906ed16dec42b33428f0`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "jira__project_risk_assessment", "kind": "base", "block": null, "base_tables": ["jira__project_risk_assessment"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |


## S67

类别 `data`；来源 `python`；调用 `b85723389f3d4edab428a075344be7e8`；状态 `success`。

```sql
SELECT * FROM jira__stakeholder_engagement_insights
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-063/attempt-01/sql/S67.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-063/attempt-01/sql/S67.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-063/attempt-01/results/S67.rows.jsonl)；完整：True；SHA256：`d0d6a16e67027655ab8eed61328494c11c418b1d936b7306da2c844c2d0e870a`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "jira__stakeholder_engagement_insights", "kind": "base", "block": null, "base_tables": ["jira__stakeholder_engagement_insights"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |


## S68

类别 `data`；来源 `python`；调用 `b85723389f3d4edab428a075344be7e8`；状态 `success`。

```sql
SELECT * FROM jira__team_performance_dashboard
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-063/attempt-01/sql/S68.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-063/attempt-01/sql/S68.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-063/attempt-01/results/S68.rows.jsonl)；完整：True；SHA256：`d27f57954de59236fc8226941690940774c5ece1a0e05529f7865256604d557b`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "jira__team_performance_dashboard", "kind": "base", "block": null, "base_tables": ["jira__team_performance_dashboard"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |


## S69

类别 `data`；来源 `query_db`；调用 `5c7551cc1d644a4e94fc966bc3a50240`；状态 `success`。

```sql
-- Primary risk drivers among false prosperity projects
SELECT primary_risk_driver, COUNT(*) as cnt
FROM jira__project_risk_assessment
WHERE overall_health_score > 75 AND risk_category IN ('Critical Risk','High Risk') AND complexity_risk_score > 30
GROUP BY primary_risk_driver
ORDER BY cnt DESC
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-063/attempt-01/sql/S69.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-063/attempt-01/sql/S69.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-063/attempt-01/results/S69.rows.jsonl)；完整：True；SHA256：`43b91c518f67a29c781d9d4eb3524644bef29107dd25d9b435e0dc26ab6d8ad3`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "jira__project_risk_assessment", "kind": "base", "block": null, "base_tables": ["jira__project_risk_assessment"]}] | [] | ["primary_risk_driver"] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |


## S70

类别 `data`；来源 `query_db`；调用 `06c34a79b40d48eda7d46306c1ce429e`；状态 `success`。

```sql
-- Strategic priority recommendations
SELECT strategic_priority_recommendation, COUNT(*) as cnt
FROM jira__project_risk_assessment
WHERE overall_health_score > 75 AND risk_category IN ('Critical Risk','High Risk') AND complexity_risk_score > 30
GROUP BY strategic_priority_recommendation
ORDER BY cnt DESC
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-063/attempt-01/sql/S70.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-063/attempt-01/sql/S70.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-063/attempt-01/results/S70.rows.jsonl)；完整：True；SHA256：`3178d90c205f7b99ff3e5e457c5ac920972f3d929cc28f8dfdbfdf8d84d4f24e`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "jira__project_risk_assessment", "kind": "base", "block": null, "base_tables": ["jira__project_risk_assessment"]}] | [] | ["strategic_priority_recommendation"] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |


## S71

类别 `data`；来源 `query_db`；调用 `0b62b675b1954b3ca5f2bcfb3d1e3838`；状态 `success`。

```sql
-- Engagement risk status by performance tier
SELECT t.performance_tier, s.engagement_risk_status, COUNT(*) as cnt
FROM jira__team_performance_dashboard t
JOIN jira__stakeholder_engagement_insights s ON t.user_id = s.stakeholder_id
GROUP BY t.performance_tier, s.engagement_risk_status
ORDER BY t.performance_tier, s.engagement_risk_status
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-063/attempt-01/sql/S71.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-063/attempt-01/sql/S71.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-063/attempt-01/results/S71.rows.jsonl)；完整：True；SHA256：`a49cd624f8056564a6d98b75c65445dcf3a8c30be51290afea0bdd6881268644`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "t", "kind": "base", "block": null, "base_tables": ["jira__team_performance_dashboard"]}, {"alias": "s", "kind": "base", "block": null, "base_tables": ["jira__stakeholder_engagement_insights"]}] | [{"type": "INNER", "right": "jira__stakeholder_engagement_insights AS s", "on": "t.user_id = s.stakeholder_id", "using": []}] | ["t.performance_tier", "s.engagement_risk_status"] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |


## S72

类别 `data`；来源 `query_db`；调用 `4433e9f04f4143d8ba96225624e62279`；状态 `success`。

```sql
-- Detailed breakdown of the 6 "Critical Priority - Investigate Contradictions" projects
SELECT project_id, project_key, project_name, overall_health_score, total_risk_score, complexity_risk_score, trajectory_status, value_delivery_percentage, success_probability, resolution_velocity_change_percent, net_issue_growth_30d, primary_risk_driver
FROM jira__project_risk_assessment
WHERE strategic_priority_recommendation = 'Critical Priority - Investigate Contradictions'
ORDER BY overall_health_score DESC
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-063/attempt-01/sql/S72.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-063/attempt-01/sql/S72.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-063/attempt-01/results/S72.rows.jsonl)；完整：True；SHA256：`92e1aa04325c09e0ecbf03c5629786461d6f26a78930649bc68d9d94200d4536`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "jira__project_risk_assessment", "kind": "base", "block": null, "base_tables": ["jira__project_risk_assessment"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |


## S73

类别 `data`；来源 `query_db`；调用 `c13af8e42b434c7ea6ad5282e433a0dd`；状态 `success`。

```sql
-- Count of projects with health > 75 and "Monitor Hidden Risks" recommendation
SELECT COUNT(*) FROM jira__project_risk_assessment
WHERE overall_health_score > 75 AND strategic_priority_recommendation = 'High Priority - Monitor Hidden Risks'
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-063/attempt-01/sql/S73.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-063/attempt-01/sql/S73.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-063/attempt-01/results/S73.rows.jsonl)；完整：True；SHA256：`fd8d7c613715406a208b525486f17f83b89cd219dbfe3230c9c146d374099fee`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "jira__project_risk_assessment", "kind": "base", "block": null, "base_tables": ["jira__project_risk_assessment"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |


## S74

类别 `data`；来源 `query_db`；调用 `7d07612d3f5044ffb360c3ef74c3d96d`；状态 `success`。

```sql
-- Intersection of false prosperity and strategic recommendations
SELECT strategic_priority_recommendation, COUNT(*) as cnt
FROM jira__project_risk_assessment
WHERE overall_health_score > 75 AND risk_category IN ('Critical Risk','High Risk') AND complexity_risk_score > 30
GROUP BY strategic_priority_recommendation
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-063/attempt-01/sql/S74.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-063/attempt-01/sql/S74.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-063/attempt-01/results/S74.rows.jsonl)；完整：True；SHA256：`d1a5b8be16d23b33cf2456439ececed827b447b9c5126f377a1978c3d8ea20db`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "jira__project_risk_assessment", "kind": "base", "block": null, "base_tables": ["jira__project_risk_assessment"]}] | [] | ["strategic_priority_recommendation"] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |


## S75

类别 `data`；来源 `query_db`；调用 `a155f5e2b550488b91c0da106d22ff7f`；状态 `success`。

```sql
-- How many with health > 75 are "Critical Priority - Investigate Contradictions"?
SELECT 
  CASE WHEN overall_health_score > 75 THEN 'health>75' ELSE 'health<=75' END as health_band,
  strategic_priority_recommendation,
  COUNT(*) as cnt
FROM jira__project_risk_assessment
GROUP BY health_band, strategic_priority_recommendation
ORDER BY health_band, cnt DESC
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-063/attempt-01/sql/S75.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-063/attempt-01/sql/S75.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-063/attempt-01/results/S75.rows.jsonl)；完整：True；SHA256：`33436bb70fd10e41d6ef11014486371143caadd1de597eb130d996dbe47b1d72`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "jira__project_risk_assessment", "kind": "base", "block": null, "base_tables": ["jira__project_risk_assessment"]}] | [] | ["CASE WHEN overall_health_score > 75 THEN 'health>75' ELSE 'health<=75' END", "strategic_priority_recommendation"] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |


## S76

类别 `data`；来源 `query_db`；调用 `c6f79684fbd449e9ac45fa66ece9fff5`；状态 `success`。

```sql
-- All 15 projects with health>75 and "Investigate Contradictions"
SELECT project_id, project_key, overall_health_score, total_risk_score, complexity_risk_score, risk_category, trajectory_status, value_delivery_percentage, success_probability, resolution_velocity_change_percent, net_issue_growth_30d, primary_risk_driver, recommended_intervention
FROM jira__project_risk_assessment
WHERE overall_health_score > 75 AND strategic_priority_recommendation = 'Critical Priority - Investigate Contradictions'
ORDER BY overall_health_score DESC
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-063/attempt-01/sql/S76.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-063/attempt-01/sql/S76.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-063/attempt-01/results/S76.rows.jsonl)；完整：True；SHA256：`768369cac62a8160692ca45a16bcfa841f02e71f5bed80e37cd8b7e623d280e1`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "jira__project_risk_assessment", "kind": "base", "block": null, "base_tables": ["jira__project_risk_assessment"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |


## S77

类别 `data`；来源 `query_db`；调用 `c74be2441cef4998b300d584c0ac207b`；状态 `success`。

```sql
-- Final profile: the extreme contradictory cohort (health>75, critical/high risk, high complexity, immediate executive review)
SELECT 
  COUNT(*) as total,
  SUM(CASE WHEN risk_category='Critical Risk' THEN 1 ELSE 0 END) as critical_cnt,
  SUM(CASE WHEN trajectory_status IN ('Declining','Deteriorating','At Risk','Volatile') THEN 1 ELSE 0 END) as adverse_trajectory,
  SUM(CASE WHEN value_delivery_percentage < 60 THEN 1 ELSE 0 END) as low_value_delivery,
  SUM(CASE WHEN success_probability < 0.4 THEN 1 ELSE 0 END) as low_success,
  SUM(CASE WHEN resolution_velocity_change_percent < 0 THEN 1 ELSE 0 END) as negative_velocity,
  SUM(CASE WHEN net_issue_growth_30d > 0 THEN 1 ELSE 0 END) as growing_backlog,
  AVG(overall_health_score) as avg_health,
  AVG(total_risk_score) as avg_total_risk,
  AVG(complexity_risk_score) as avg_complexity,
  AVG(value_delivery_percentage) as avg_delivery,
  AVG(success_probability) as avg_success_prob
FROM jira__project_risk_assessment
WHERE overall_health_score > 75 AND risk_category IN ('Critical Risk','High Risk') AND complexity_risk_score > 30
  AND recommended_intervention = 'Immediate Executive Review Required'
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-063/attempt-01/sql/S77.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-063/attempt-01/sql/S77.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-063/attempt-01/results/S77.rows.jsonl)；完整：True；SHA256：`9191022d2d25640578f94e161d42fbcd400ef57d1e46405df584e92dae200367`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "jira__project_risk_assessment", "kind": "base", "block": null, "base_tables": ["jira__project_risk_assessment"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |
| B1 | SUM(CASE WHEN risk_category = 'Critical Risk' THEN 1 ELSE 0 END) | [] | [{"table": "jira__project_risk_assessment", "column": "risk_category"}] | False |
| B1 | SUM(CASE WHEN trajectory_status IN ('Declining', 'Deteriorating', 'At Risk', 'Volatile') THEN 1 ELSE 0 END) | [] | [{"table": "jira__project_risk_assessment", "column": "trajectory_status"}] | False |
| B1 | SUM(CASE WHEN value_delivery_percentage < 60 THEN 1 ELSE 0 END) | [] | [{"table": "jira__project_risk_assessment", "column": "value_delivery_percentage"}] | False |
| B1 | SUM(CASE WHEN success_probability < 0.4 THEN 1 ELSE 0 END) | [] | [{"table": "jira__project_risk_assessment", "column": "success_probability"}] | False |
| B1 | SUM(CASE WHEN resolution_velocity_change_percent < 0 THEN 1 ELSE 0 END) | [] | [{"table": "jira__project_risk_assessment", "column": "resolution_velocity_change_percent"}] | False |
| B1 | SUM(CASE WHEN net_issue_growth_30d > 0 THEN 1 ELSE 0 END) | [] | [{"table": "jira__project_risk_assessment", "column": "net_issue_growth_30d"}] | False |
| B1 | AVG(overall_health_score) | [{"table": "jira__project_risk_assessment", "column": "overall_health_score"}] | [] | False |
| B1 | AVG(total_risk_score) | [{"table": "jira__project_risk_assessment", "column": "total_risk_score"}] | [] | False |
| B1 | AVG(complexity_risk_score) | [{"table": "jira__project_risk_assessment", "column": "complexity_risk_score"}] | [] | False |
| B1 | AVG(value_delivery_percentage) | [{"table": "jira__project_risk_assessment", "column": "value_delivery_percentage"}] | [] | False |
| B1 | AVG(success_probability) | [{"table": "jira__project_risk_assessment", "column": "success_probability"}] | [] | False |

