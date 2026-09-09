# dacomp-064

In the project delivery cycle of the last 6 months, we have observed that certain key stak…

运行：已提交。官方未评分。全部 SQL 尝试/成功 67/66；数据 SQL 65/64；Python 8 次。

完整原题：

In the project delivery cycle of the last 6 months, we have observed that certain key stakeholders with high technical influence (`engagement_impact_score` ≥ 3) and frequent cross-functional collaboration (`cross_functional_projects` ≥ 3) have shown a phenomenon of decreasing engagement depth while their influence breadth continues to expand. Simultaneously, their problem-solving efficiency (based on the ratio of `issues_assigned` to `issues_reported` and `avg_close_time`) and influence propagation patterns (the dynamic balance between `total_outbound_influence` vs. `total_inbound_influence`) have exhibited abnormal fluctuations. Please conduct an in-depth analysis of the root causes behind this contradictory phenomenon of 'expanding influence but declining participation efficiency'. Identify which factors (such as changes in `response_pattern_type`, growth patterns of `network_connections`, distribution of project types, and the alignment between `strategic_value_score` and actual contributions) are driving this trend. Additionally, evaluate the potential impact of this pattern on overall project success rates and team collaboration efficiency, and propose data-driven strategies for personnel capability reallocation and collaboration model optimization.

| 表 | 行数 | 列数 |
| --- | --- | --- |
| jira__daily_issue_field_history | 50000 | 12 |
| jira__issue_enhanced | 8000 | 66 |
| jira__project_enhanced | 200 | 30 |
| jira__stakeholder_engagement_insights | 4524 | 23 |
| jira__user_enhanced | 6000 | 18 |


实际路线（分析者依据 SQL/源码概括，不代表 Agent 自述）：SQL 识别高影响跨职能利益相关者并连接问题记录 → Python 月趋势及响应模式分组比较 → 影响失衡与协作建议。

数据库大小：14,692,352 字节。

## 数据 SQL

| SQL | 状态 | 基础表 | Join 输入/类型 | GROUP BY | 聚合表达式 | 结果行数 | 数据库 ms |
| --- | --- | --- | --- | --- | --- | --- | --- |
| [S3/Q1](#s3) | success | ["jira__stakeholder_engagement_insights"] | 0 / {} | [] | ["COUNT(*)"] | 1 | 1.092 |
| [S4/Q2](#s4) | success | ["jira__issue_enhanced"] | 0 / {} | [] | ["COUNT(*)"] | 1 | 3.012 |
| [S5/Q3](#s5) | success | ["jira__daily_issue_field_history"] | 0 / {} | [] | ["COUNT(*)"] | 1 | 2.24 |
| [S6/Q4](#s6) | success | ["jira__project_enhanced"] | 0 / {} | [] | ["COUNT(*)"] | 1 | 0.288 |
| [S7/Q5](#s7) | success | ["jira__daily_issue_field_history"] | 0 / {} | [] | ["MIN(date_day)", "MAX(date_day)"] | 1 | 7.055 |
| [S8/Q6](#s8) | success | ["jira__stakeholder_engagement_insights"] | 0 / {} | [] | ["SUM(CASE WHEN engagement_impact_score >= 3 AND cross_functional_projects >= 3 THEN 1 ELSE 0 END)", "SUM(CASE WHEN engagement_impact_score >= 3 THEN 1 ELSE 0 END)", "SUM(CASE WHEN cross_functional_projects >= 3 THEN 1 ELSE 0 END)", "COUNT(*)"] | 1 | 1.625 |
| [S9/Q7](#s9) | success | ["jira__stakeholder_engagement_insights"] | 0 / {} | ["engagement_impact_score"] | ["COUNT(*)"] | 6 | 1.781 |
| [S10/Q8](#s10) | success | ["jira__stakeholder_engagement_insights"] | 0 / {} | ["response_pattern_type"] | ["COUNT(*)"] | 10 | 2.13 |
| [S11/Q9](#s11) | success | ["jira__stakeholder_engagement_insights"] | 0 / {} | ["influence_level"] | ["COUNT(*)"] | 6 | 2.074 |
| [S12/Q10](#s12) | success | ["jira__stakeholder_engagement_insights"] | 0 / {} | ["stakeholder_archetype"] | ["COUNT(*)"] | 20 | 2.108 |
| [S13/Q11](#s13) | success | ["jira__stakeholder_engagement_insights"] | 0 / {} | ["engagement_risk_status"] | ["COUNT(*)"] | 5 | 2.054 |
| [S14/Q12](#s14) | success | ["jira__stakeholder_engagement_insights"] | 0 / {} | [] | ["AVG(engagement_depth_score)", "AVG(engagement_breadth_score)", "AVG(issues_reported)", "AVG(issues_assigned)", "AVG(total_outbound_influence)", "AVG(total_inbound_influence)", "AVG(strategic_value_score)", "AVG(direct_network_connections)", "AVG(total_engagement_score)"] | 1 | 2.116 |
| [S15/Q13](#s15) | success | ["jira__stakeholder_engagement_insights"] | 0 / {} | [] | ["AVG(engagement_depth_score)", "AVG(engagement_breadth_score)", "AVG(issues_reported)", "AVG(issues_assigned)", "AVG(total_outbound_influence)", "AVG(total_inbound_influence)", "AVG(strategic_value_score)", "AVG(direct_network_connections)", "AVG(total_engagement_score)"] | 1 | 2.836 |
| [S16/Q14](#s16) | failed | ["jira__user_enhanced"] | 0 / {} | [] | ["MIN(engagement_depth_score)", "MAX(engagement_depth_score)", "MIN(engagement_breadth_score)", "MAX(engagement_breadth_score)", "MIN(strategic_value_score)", "MAX(strategic_value_score)", "MIN(avg_close_time_days)", "MAX(avg_close_time_days)"] | unknown | 未取得；调用总时长 0.168 ms |
| [S17/Q15](#s17) | success | ["jira__stakeholder_engagement_insights"] | 0 / {} | [] | ["MIN(engagement_depth_score)", "MAX(engagement_depth_score)", "MIN(engagement_breadth_score)", "MAX(engagement_breadth_score)", "MIN(strategic_value_score)", "MAX(strategic_value_score)", "MIN(engagement_quality_score)", "MAX(engagement_quality_score)", "MIN(total_engagement_score)", "MAX(total_engagement_score)"] | 1 | 2.364 |
| [S18/Q16](#s18) | success | ["jira__stakeholder_engagement_insights"] | 0 / {} | ["response_pattern_type"] | ["COUNT(*)", "AVG(engagement_depth_score)", "AVG(engagement_breadth_score)", "AVG(total_outbound_influence)", "AVG(total_inbound_influence)", "AVG(issues_assigned * 1.0 / NULLIF(issues_reported, 0))"] | 10 | 2.05 |
| [S19/Q17](#s19) | success | ["jira__stakeholder_engagement_insights"] | 0 / {} | ["engagement_risk_status"] | ["COUNT(*)", "AVG(engagement_depth_score)", "AVG(engagement_breadth_score)", "AVG(total_outbound_influence)", "AVG(total_inbound_influence)"] | 3 | 1.746 |
| [S20/Q18](#s20) | success | ["jira__stakeholder_engagement_insights"] | 0 / {} | [] | [] | 5 | 0.301 |
| [S21/Q19](#s21) | success | ["jira__issue_enhanced"] | 0 / {} | ["assignee_user_id", "assignee_name"] | ["COUNT(*)"] | 5 | 9.328 |
| [S22/Q20](#s22) | success | ["jira__user_enhanced"] | 0 / {} | [] | [] | 5 | 0.389 |
| [S23/Q21](#s23) | success | ["jira__issue_enhanced"] | 0 / {} | [] | ["MIN(created_at)", "MAX(created_at)", "MIN(resolved_at)", "MAX(resolved_at)"] | 1 | 4.152 |
| [S24/Q22](#s24) | success | ["jira__issue_enhanced", "jira__stakeholder_engagement_insights"] | 2 / {'INNER': 1} | [] | [] | 10 | 11.007 |
| [S25/Q23](#s25) | success | ["jira__stakeholder_engagement_insights", "jira__user_enhanced"] | 2 / {'LEFT': 1} | [] | [] | 10 | 6.126 |
| [S26/Q24](#s26) | success | ["jira__issue_enhanced", "jira__stakeholder_engagement_insights"] | 2 / {'INNER': 1} | [] | ["COUNT(DISTINCT s.stakeholder_id)"] | 1 | 13.904 |
| [S27/Q25](#s27) | success | ["jira__issue_enhanced"] | 0 / {} | ["assignee_name"] | ["COUNT(DISTINCT assignee_user_id)", "COUNT(*)"] | 10 | 5.713 |
| [S28/Q26](#s28) | success | ["jira__issue_enhanced"] | 0 / {} | [] | ["COUNT(*)"] | 1 | 3.443 |
| [S29/Q27](#s29) | success | ["jira__stakeholder_engagement_insights"] | 0 / {} | [] | [] | 20 | 1.468 |
| [S30/Q28](#s30) | success | ["jira__daily_issue_field_history"] | 0 / {} | ["date_day", "date_week", "status", "issue_type"] | ["COUNT(*)"] | 10 | 57.364 |
| [S31/Q29](#s31) | success | ["jira__daily_issue_field_history"] | 0 / {} | [] | ["COUNT(DISTINCT issue_id)", "COUNT(DISTINCT date_day)", "COUNT(DISTINCT assignee)", "COUNT(DISTINCT reporter)"] | 1 | 50.249 |
| [S32/Q30](#s32) | success | ["jira__daily_issue_field_history"] | 0 / {} | [] | [] | 10 | 0.254 |
| [S33/Q31](#s33) | success | ["jira__daily_issue_field_history", "jira__stakeholder_engagement_insights"] | 2 / {'LEFT': 1} | [] | ["COUNT(DISTINCT d.assignee)", "COUNT(DISTINCT CASE WHEN NOT s.stakeholder_id IS NULL THEN d.assignee END)"] | 1 | 21.37 |
| [S34/Q32](#s34) | success | ["jira__issue_enhanced", "jira__stakeholder_engagement_insights"] | 2 / {'LEFT': 1} | [] | ["COUNT(DISTINCT i.assignee_user_id)", "COUNT(DISTINCT CASE WHEN NOT s.stakeholder_id IS NULL THEN i.assignee_user_id END)"] | 1 | 18.786 |
| [S35/Q33](#s35) | success | ["jira__daily_issue_field_history", "jira__stakeholder_engagement_insights"] | 2 / {'LEFT': 1} | [] | ["COUNT(DISTINCT d.reporter)", "COUNT(DISTINCT CASE WHEN NOT s.stakeholder_id IS NULL THEN d.reporter END)"] | 1 | 21.197 |
| [S36/Q34](#s36) | success | ["jira__stakeholder_engagement_insights"] | 0 / {} | [] | [] | 1502 | 9.409 |
| [S37/Q35](#s37) | success | ["jira__issue_enhanced", "jira__stakeholder_engagement_insights"] | 2 / {'INNER': 1} | ["STRFTIME('%Y-%m', i.created_at)"] | ["COUNT(*)", "COUNT(DISTINCT i.assignee_user_id)", "AVG(i.open_duration_seconds / 86400.0)", "AVG(i.any_assignment_duration_seconds / 86400.0)", "AVG(i.work_ratio)"] | 7 | 18.029 |
| [S38/Q36](#s38) | success | ["jira__issue_enhanced", "jira__stakeholder_engagement_insights"] | 2 / {'INNER': 1} | ["STRFTIME('%Y-%m', i.resolved_at)"] | ["COUNT(*)", "AVG((JULIANDAY(i.resolved_at) - JULIANDAY(i.created_at)) * 1.0)"] | 8 | 12.161 |
| [S39/Q37](#s39) | success | ["jira__issue_enhanced", "jira__stakeholder_engagement_insights"] | 2 / {'INNER': 1} | ["i.project_name", "i.issue_type"] | ["COUNT(*)", "AVG(i.open_duration_seconds / 86400.0)", "AVG(CASE WHEN NOT i.resolved_at IS NULL THEN (JULIANDAY(i.resolved_at) - JULIANDAY(i.created_at)) END)"] | 30 | 18.734 |
| [S40/Q38](#s40) | success | ["jira__project_enhanced"] | 0 / {} | ["project_category_id"] | ["COUNT(*)"] | 6 | 0.446 |
| [S41/Q39](#s41) | success | ["jira__issue_enhanced", "jira__project_enhanced", "jira__stakeholder_engagement_insights"] | 3 / {'INNER': 2} | ["p.project_category_id"] | ["COUNT(*)", "COUNT(DISTINCT i.assignee_user_id)", "AVG(CASE WHEN NOT i.resolved_at IS NULL THEN (JULIANDAY(i.resolved_at) - JULIANDAY(i.created_at)) END)", "AVG(i.open_duration_seconds / 86400.0)", "AVG(i.work_ratio)"] | 6 | 19.87 |
| [S42/Q40](#s42) | success | ["jira__issue_enhanced", "jira__stakeholder_engagement_insights"] | 2 / {'INNER': 1} | ["i.issue_type"] | ["COUNT(*)", "AVG(CASE WHEN NOT i.resolved_at IS NULL THEN (JULIANDAY(i.resolved_at) - JULIANDAY(i.created_at)) END)", "AVG(i.work_ratio)"] | 7 | 16.589 |
| [S43/Q41](#s43) | success | ["jira__issue_enhanced", "jira__stakeholder_engagement_insights"] | 2 / {'INNER': 1} | ["s.stakeholder_id"] | ["COUNT(i.issue_id)", "SUM(CASE WHEN NOT i.resolved_at IS NULL THEN 1 ELSE 0 END)", "COUNT(DISTINCT i.project_id)", "COUNT(DISTINCT i.issue_type)", "AVG(CASE WHEN NOT i.resolved_at IS NULL THEN (JULIANDAY(i.resolved_at) - JULIANDAY(i.created_at)) END)", "AVG(i.work_ratio)", "AVG(i.open_duration_seconds / 86400.0)", "SUM(i.time_spent_seconds)"] | 1252 | 26.846 |
| [S44/Q42](#s44) | success | ["jira__issue_enhanced", "jira__stakeholder_engagement_insights"] | 2 / {'INNER': 1} | ["s.stakeholder_id"] | ["COUNT(i.issue_id)", "SUM(CASE WHEN NOT i.resolved_at IS NULL THEN 1 ELSE 0 END)", "COUNT(DISTINCT i.project_id)", "AVG(CASE WHEN NOT i.resolved_at IS NULL THEN (JULIANDAY(i.resolved_at) - JULIANDAY(i.created_at)) END)", "AVG(i.work_ratio)", "AVG(i.open_duration_seconds / 86400.0)", "SUM(i.time_spent_seconds)"] | 2499 | 32.437 |
| [S45/Q43](#s45) | success | ["jira__stakeholder_engagement_insights"] | 0 / {} | [] | ["AVG(engagement_depth_score)", "AVG(engagement_breadth_score)", "AVG(engagement_quality_score)", "AVG(issues_assigned)", "AVG(issues_reported)", "AVG(total_outbound_influence)", "AVG(total_inbound_influence)", "AVG(direct_network_connections)", "AVG(strategic_value_score)", "AVG(total_engagement_score)"] | 1 | 2.068 |
| [S46/Q44](#s46) | success | ["jira__stakeholder_engagement_insights"] | 0 / {} | ["response_pattern_type"] | ["COUNT(*)", "SUM(CASE WHEN engagement_risk_status = 'At Risk' OR engagement_risk_status = 'Disengaged' THEN 1 ELSE 0 END)", "AVG(engagement_depth_score)", "AVG(engagement_breadth_score)", "AVG(total_outbound_influence - total_inbound_influence)", "AVG(issues_assigned * 1.0 / NULLIF(issues_reported, 0))", "AVG(direct_network_connections)", "AVG(strategic_value_score)", "AVG(total_engagement_score)"] | 10 | 2.879 |
| [S47/Q45](#s47) | success | ["jira__stakeholder_engagement_insights"] | 0 / {} | ["CASE WHEN strategic_value_score >= 80 AND engagement_depth_score < 20 THEN 'High Strategic, Low Depth' WHEN strategic_value_score >= 80 AND engagement_depth_score >= 20 THEN 'High Strategic, High Depth' WHEN strategic_value_score < 80 AND engagement_depth_score < 20 THEN 'Low Strategic, Low Depth' ELSE 'Low Strategic, High Depth' END"] | ["COUNT(*)", "AVG(engagement_breadth_score)", "AVG(total_outbound_influence - total_inbound_influence)", "AVG(issues_assigned * 1.0 / NULLIF(issues_reported, 0))", "AVG(total_engagement_score)"] | 4 | 2.198 |
| [S48/Q46](#s48) | success | ["jira__stakeholder_engagement_insights"] | 0 / {} | [] | [] | 1502 | 7.212 |
| [S49/Q47](#s49) | success | ["jira__stakeholder_engagement_insights"] | 0 / {} | [] | [] | 1502 | 6.957 |
| [S50/Q48](#s50) | success | ["jira__stakeholder_engagement_insights"] | 0 / {} | [] | [] | 4524 | 20.101 |
| [S51/Q49](#s51) | success | ["jira__issue_enhanced", "jira__stakeholder_engagement_insights"] | 2 / {'INNER': 1} | [] | [] | 1855 | 14.8 |
| [S52/Q50](#s52) | success | ["jira__issue_enhanced", "jira__stakeholder_engagement_insights"] | 2 / {'INNER': 1} | [] | [] | 3692 | 13.911 |
| [S53/Q51](#s53) | success | ["jira__daily_issue_field_history", "jira__stakeholder_engagement_insights"] | 2 / {'INNER': 1} | ["d.date_week", "d.status"] | ["COUNT(DISTINCT d.issue_id)"] | 141 | 80.117 |
| [S54/Q52](#s54) | success | ["jira__stakeholder_engagement_insights"] | 0 / {} | [] | [] | 1502 | 6.978 |
| [S55/Q53](#s55) | success | ["jira__daily_issue_field_history", "jira__stakeholder_engagement_insights"] | 2 / {'INNER': 1} | ["d.date_week", "d.status"] | ["COUNT(DISTINCT d.issue_id)"] | 141 | 86.68 |
| [S56/Q54](#s56) | success | ["jira__stakeholder_engagement_insights"] | 0 / {} | [] | [] | 1502 | 7.952 |
| [S57/Q55](#s57) | success | ["jira__issue_enhanced", "jira__project_enhanced", "jira__stakeholder_engagement_insights"] | 3 / {'INNER': 2} | [] | [] | 1841 | 14.519 |
| [S58/Q56](#s58) | success | ["jira__stakeholder_engagement_insights"] | 0 / {} | [] | [] | 1502 | 7.136 |
| [S59/Q57](#s59) | success | ["jira__issue_enhanced", "jira__project_enhanced", "jira__stakeholder_engagement_insights"] | 3 / {'INNER': 2} | [] | [] | 1841 | 11.411 |
| [S60/Q58](#s60) | success | ["jira__daily_issue_field_history", "jira__stakeholder_engagement_insights"] | 2 / {'INNER': 1} | ["d.date_week", "d.status"] | ["COUNT(DISTINCT d.issue_id)"] | 141 | 80.14 |
| [S61/Q59](#s61) | success | ["jira__stakeholder_engagement_insights"] | 0 / {} | [] | [] | 1502 | 6.968 |
| [S62/Q60](#s62) | success | ["jira__stakeholder_engagement_insights"] | 0 / {} | ["response_pattern_type"] | ["COUNT(*)", "SUM(CASE WHEN engagement_breadth_score >= 40 THEN 1 ELSE 0 END)", "AVG(engagement_breadth_score)", "COUNT(*)", "SUM(CASE WHEN engagement_breadth_score >= 40 THEN 1 ELSE 0 END)"] | 10 | 1.597 |
| [S63/Q61](#s63) | success | ["jira__stakeholder_engagement_insights"] | 0 / {} | ["recommended_engagement_strategy"] | ["COUNT(*)", "AVG(engagement_depth_score)", "AVG(engagement_breadth_score)"] | 12 | 1.657 |
| [S64/Q62](#s64) | success | ["jira__stakeholder_engagement_insights"] | 0 / {} | ["development_opportunity"] | ["COUNT(*)"] | 12 | 1.552 |
| [S65/Q63](#s65) | success | ["jira__stakeholder_engagement_insights"] | 0 / {} | ["development_opportunity"] | ["COUNT(*)"] | 12 | 1.004 |
| [S66/Q64](#s66) | success | ["jira__stakeholder_engagement_insights"] | 0 / {} | ["recommended_engagement_strategy"] | ["COUNT(*)"] | 12 | 0.995 |
| [S67/Q65](#s67) | success | ["jira__stakeholder_engagement_insights", "jira__user_enhanced"] | 2 / {'INNER': 1} | ["CASE WHEN s.engagement_impact_score >= 3 AND s.cross_functional_projects >= 3 THEN 'Target' ELSE 'Other' END"] | ["COUNT(DISTINCT u.user_id)", "AVG(u.avg_close_time_days)", "AVG(u.median_close_time_days)", "AVG(u.avg_age_currently_open_days)"] | 2 | 13.348 |


## 元数据和设置

| SQL | 类别 | 状态 | 内容 |
| --- | --- | --- | --- |
| S1 | connection_setup | success | PRAGMA query_only=ON |
| S2 | metadata | success | SELECT name,sql FROM sqlite_master WHERE type='table' ORDER BY name |


## Python 与执行位置

人工源码审查：**database_first_violation**。Python 按月份、问题类型、响应模式和连接分组计算数量、均值及风险比例，还执行阈值计数。这些可在 SQL 完成。Mann–Whitney、Spearman 检验和绘图是独立的统计补充。 [证据](../reviews/dacomp-064.json)。

P1：Statistical correlation and visualization for the target cohort. SQLite supports the joins/aggregations but correlation matrices, group comparisons (t-tests), and multi-panel figures are statistical/visual procedures better handled in Python.

[源码](../../../runs/dsv4flash-db-first-full-01/dacomp-064/attempt-01/python/P1.py)；[输出](../../../runs/dsv4flash-db-first-full-01/dacomp-064/attempt-01/python/P1.stdout)；[错误](../../../runs/dsv4flash-db-first-full-01/dacomp-064/attempt-01/python/P1.stderr)。检出需人工核验的 SQL 可实现操作：.query(；不能仅凭理由判为合规。

P2：Correlation matrix and scatter plots for the target cohort to identify which factors drive the depth-breadth inverse relationship. Python's matplotlib/seaborn provide better visualization than SQL.

[源码](../../../runs/dsv4flash-db-first-full-01/dacomp-064/attempt-01/python/P2.py)；[输出](../../../runs/dsv4flash-db-first-full-01/dacomp-064/attempt-01/python/P2.stdout)；[错误](../../../runs/dsv4flash-db-first-full-01/dacomp-064/attempt-01/python/P2.stderr)。检出需人工核验的 SQL 可实现操作：.query(；不能仅凭理由判为合规。

P3：Statistical comparison (t-tests / Mann-Whitney) between the target cohort and the rest, plus analysis of strategic-value misalignment. These inferential statistics are not reasonably supported by SQLite.

[源码](../../../runs/dsv4flash-db-first-full-01/dacomp-064/attempt-01/python/P3.py)；[输出](../../../runs/dsv4flash-db-first-full-01/dacomp-064/attempt-01/python/P3.stdout)；[错误](../../../runs/dsv4flash-db-first-full-01/dacomp-064/attempt-01/python/P3.stderr)。检出需人工核验的 SQL 可实现操作：groupby(, .query(, sort_values(；不能仅凭理由判为合规。

P4：Monthly close time trend analysis and comparison between target and non-target groups. This shows temporal changes in problem-solving efficiency which SQLite aggregation alone cannot visualize.

[源码](../../../runs/dsv4flash-db-first-full-01/dacomp-064/attempt-01/python/P4.py)；[输出](../../../runs/dsv4flash-db-first-full-01/dacomp-064/attempt-01/python/P4.stdout)；[错误](../../../runs/dsv4flash-db-first-full-01/dacomp-064/attempt-01/python/P4.stderr)。检出需人工核验的 SQL 可实现操作：groupby(, .query(；不能仅凭理由判为合规。

P5：Deeper analysis of the root causes: (1) weekly issue volume trend from daily history, (2) influence propagation vs network size, (3) strategic value vs contribution gap analysis. Python needed for statistical tests, data transformations, and multiple panel plots.

[源码](../../../runs/dsv4flash-db-first-full-01/dacomp-064/attempt-01/python/P5.py)；[输出](../../../runs/dsv4flash-db-first-full-01/dacomp-064/attempt-01/python/P5.stdout)；[错误](../../../runs/dsv4flash-db-first-full-01/dacomp-064/attempt-01/python/P5.stderr)。检出需人工核验的 SQL 可实现操作：groupby(, .query(, sort_values(；不能仅凭理由判为合规。

P6：Analyze the Testing bottleneck, influence propagation topology, and build the final diagnostic visualization. Python needed for multi-panel figure and statistical tests that SQLite cannot perform.

[源码](../../../runs/dsv4flash-db-first-full-01/dacomp-064/attempt-01/python/P6.py)；[输出](../../../runs/dsv4flash-db-first-full-01/dacomp-064/attempt-01/python/P6.stdout)；[错误](../../../runs/dsv4flash-db-first-full-01/dacomp-064/attempt-01/python/P6.stderr)。检出需人工核验的 SQL 可实现操作：groupby(, .query(, sort_values(；不能仅凭理由判为合规。

P7：Redo the final multi-panel diagnostic visualization after fixing the variable initialization error; the prior analysis outputs were still valid but the figure generation failed.

[源码](../../../runs/dsv4flash-db-first-full-01/dacomp-064/attempt-01/python/P7.py)；[输出](../../../runs/dsv4flash-db-first-full-01/dacomp-064/attempt-01/python/P7.stdout)；[错误](../../../runs/dsv4flash-db-first-full-01/dacomp-064/attempt-01/python/P7.stderr)。检出需人工核验的 SQL 可实现操作：groupby(, .query(；不能仅凭理由判为合规。

P8：Identify high-risk sub-cohort within the target group and profile the stakeholders showing the strongest 'expanding influence but declining depth' signature; also test whether network growth variables predict the pattern via regression. This requires inferential statistics not in SQLite.

[源码](../../../runs/dsv4flash-db-first-full-01/dacomp-064/attempt-01/python/P8.py)；[输出](../../../runs/dsv4flash-db-first-full-01/dacomp-064/attempt-01/python/P8.stdout)；[错误](../../../runs/dsv4flash-db-first-full-01/dacomp-064/attempt-01/python/P8.stderr)。检出需人工核验的 SQL 可实现操作：.query(, sort_values(；不能仅凭理由判为合规。

## 优化机会

已验证候选。筛选限于精确 SQL、相同自包含 CTE、相同单表完整过滤、可分解单表聚合；未覆盖任意 Join 等价和一般谓词蕴含。全部候选都是 offline，未测在线预测。

| 候选 | 类型 | 已有结果 | 覆盖 SQL | 后续次数 | 中间行数 | 验证 | 成本 |
| --- | --- | --- | --- | --- | --- | --- | --- |
| C1 | exact-result reuse | True | ["S48", "S49", "S54", "S56", "S58", "S61"] | 5 | unknown | not_verified_cap | Not tested |
| C2 | exact-result reuse | True | ["S53", "S55", "S60"] | 2 | unknown | not_verified_cap | Not tested |
| C3 | aggregate MV | False | ["S3", "S8", "S9", "S10", "S11", "S12", "S13", "S17"] | 7 | 3575 | verified | Not benchmarked; correctness alone does not establish net speedup. |
| C4 | aggregate MV | False | ["S4", "S21", "S23"] | 2 | unknown | not_verified_cap | Not tested |
| C5 | aggregate MV | False | ["S5", "S7", "S30"] | 2 | unknown | not_verified_cap | Not tested |
| C6 | aggregate MV | False | ["S6", "S40"] | 1 | unknown | not_verified_cap | Not tested |
| C7 | common filtered view | False | ["S14", "S18", "S19", "S29", "S36", "S46", "S47", "S48", "S49", "S54", "S56", "S58", "S61", "S62", "S63", "S64"] | 15 | 1502 | verified | Not benchmarked; correctness alone does not establish net speedup. |
| C8 | aggregate MV | False | ["S14", "S18", "S19", "S46", "S47", "S62", "S63", "S64"] | 7 | 1442 | rejected_result_mismatch | Not benchmarked; correctness alone does not establish net speedup. |
| C9 | common filtered view | False | ["S15", "S45"] | 1 | unknown | not_verified_cap | Not tested |
| C10 | aggregate MV | False | ["S15", "S45"] | 1 | unknown | not_verified_cap | Not tested |
| C11 | common filtered view | False | ["S65", "S66"] | 1 | unknown | not_verified_cap | Not tested |
| C12 | aggregate MV | False | ["S65", "S66"] | 1 | unknown | not_verified_cap | Not tested |


已验证覆盖（含触发查询、候选并集去重）：24/64 条成功数据 SQL。正确性仅针对当前数据库快照；未测性能的候选不能声称已加速。

[完整 build/rewrite 与比较证据](dacomp-064.analysis.json)。

### C7：common filtered view

Same single source and complete filter; original filter retained.

原查询 [S14](#s14), [S18](#s18), [S19](#s19), [S29](#s29), [S36](#s36), [S46](#s46), [S47](#s47), [S48](#s48), [S49](#s49), [S54](#s54), [S56](#s56), [S58](#s58), [S61](#s61), [S62](#s62), [S63](#s63), [S64](#s64) → 新增共享状态 C7 → 后续 15 次可复用。该构建点为事后假设，不代表 Agent 当时预知后续。

构建定义：

```sql
SELECT * FROM "jira__stakeholder_engagement_insights" WHERE engagement_impact_score >= 3 AND cross_functional_projects >= 3
```

受益查询 S14 的改写示例：

```sql
SELECT AVG(engagement_depth_score) AS avg_depth, AVG(engagement_breadth_score) AS avg_breadth, AVG(issues_reported) AS avg_reported, AVG(issues_assigned) AS avg_assigned, AVG(total_outbound_influence) AS avg_outbound, AVG(total_inbound_influence) AS avg_inbound, AVG(strategic_value_score) AS avg_strategic, AVG(direct_network_connections) AS avg_connections, AVG(total_engagement_score) AS avg_total_score FROM temp.reuse_candidate AS jira__stakeholder_engagement_insights WHERE engagement_impact_score >= 3 AND cross_functional_projects >= 3
```

| 原 SQL | 列名一致 | 结果一致 | 比较方法 |
| --- | --- | --- | --- |
| S14 | True | True | exact_multiset |
| S18 | True | True | ordered_numeric_tolerance |
| S19 | True | True | ordered_numeric_tolerance |
| S29 | True | True | ordered_numeric_tolerance |
| S36 | True | True | ordered_numeric_tolerance |
| S46 | True | True | ordered_numeric_tolerance |
| S47 | True | True | ordered_numeric_tolerance |
| S48 | True | True | exact_multiset |
| S49 | True | True | exact_multiset |
| S54 | True | True | exact_multiset |
| S56 | True | True | exact_multiset |
| S58 | True | True | exact_multiset |
| S61 | True | True | exact_multiset |
| S62 | True | True | ordered_numeric_tolerance |
| S63 | True | True | ordered_numeric_tolerance |
| S64 | True | True | ordered_numeric_tolerance |


验证状态：verified；成本结论：Not benchmarked; correctness alone does not establish net speedup.

### C3：aggregate MV

Union of grouping keys; decomposable aggregate states; AVG uses SUM and non-NULL COUNT.

原查询 [S3](#s3), [S8](#s8), [S9](#s9), [S10](#s10), [S11](#s11), [S12](#s12), [S13](#s13), [S17](#s17) → 新增共享状态 C3 → 后续 7 次可复用。该构建点为事后假设，不代表 Agent 当时预知后续。

构建定义：

```sql
SELECT engagement_impact_score AS __g0, response_pattern_type AS __g1, influence_level AS __g2, stakeholder_archetype AS __g3, engagement_risk_status AS __g4, COUNT(*) AS __a0, SUM(CASE WHEN engagement_impact_score >= 3 AND cross_functional_projects >= 3 THEN 1 ELSE 0 END) AS __a1, SUM(CASE WHEN engagement_impact_score >= 3 THEN 1 ELSE 0 END) AS __a2, SUM(CASE WHEN cross_functional_projects >= 3 THEN 1 ELSE 0 END) AS __a3, MIN(engagement_depth_score) AS __a4, MAX(engagement_depth_score) AS __a5, MIN(engagement_breadth_score) AS __a6, MAX(engagement_breadth_score) AS __a7, MIN(strategic_value_score) AS __a8, MAX(strategic_value_score) AS __a9, MIN(engagement_quality_score) AS __a10, MAX(engagement_quality_score) AS __a11, MIN(total_engagement_score) AS __a12, MAX(total_engagement_score) AS __a13 FROM "jira__stakeholder_engagement_insights"  GROUP BY engagement_impact_score, response_pattern_type, influence_level, stakeholder_archetype, engagement_risk_status
```

受益查询 S3 的改写示例：

```sql
SELECT SUM(__a0) AS n_stakeholders FROM temp.reuse_candidate
```

| 原 SQL | 列名一致 | 结果一致 | 比较方法 |
| --- | --- | --- | --- |
| S3 | True | True | exact_multiset |
| S8 | True | True | exact_multiset |
| S9 | True | True | ordered_numeric_tolerance |
| S10 | True | True | ordered_numeric_tolerance |
| S11 | True | True | ordered_numeric_tolerance |
| S12 | True | True | ordered_numeric_tolerance |
| S13 | True | True | ordered_numeric_tolerance |
| S17 | True | True | exact_multiset |


验证状态：verified；成本结论：Not benchmarked; correctness alone does not establish net speedup.

### C8：aggregate MV

Union of grouping keys; decomposable aggregate states; AVG uses SUM and non-NULL COUNT.

原查询 [S14](#s14), [S18](#s18), [S19](#s19), [S46](#s46), [S47](#s47), [S62](#s62), [S63](#s63), [S64](#s64) → 新增共享状态 C8 → 后续 7 次可复用。该构建点为事后假设，不代表 Agent 当时预知后续。

构建定义：

```sql
SELECT response_pattern_type AS __g0, engagement_risk_status AS __g1, CASE WHEN strategic_value_score >= 80 AND engagement_depth_score < 20 THEN 'High Strategic, Low Depth' WHEN strategic_value_score >= 80 AND engagement_depth_score >= 20 THEN 'High Strategic, High Depth' WHEN strategic_value_score < 80 AND engagement_depth_score < 20 THEN 'Low Strategic, Low Depth' ELSE 'Low Strategic, High Depth' END AS __g2, recommended_engagement_strategy AS __g3, development_opportunity AS __g4, SUM(engagement_depth_score) AS __a0_sum, COUNT(engagement_depth_score) AS __a0_n, SUM(engagement_breadth_score) AS __a1_sum, COUNT(engagement_breadth_score) AS __a1_n, SUM(issues_reported) AS __a2_sum, COUNT(issues_reported) AS __a2_n, SUM(issues_assigned) AS __a3_sum, COUNT(issues_assigned) AS __a3_n, SUM(total_outbound_influence) AS __a4_sum, COUNT(total_outbound_influence) AS __a4_n, SUM(total_inbound_influence) AS __a5_sum, COUNT(total_inbound_influence) AS __a5_n, SUM(strategic_value_score) AS __a6_sum, COUNT(strategic_value_score) AS __a6_n, SUM(direct_network_connections) AS __a7_sum, COUNT(direct_network_connections) AS __a7_n, SUM(total_engagement_score) AS __a8_sum, COUNT(total_engagement_score) AS __a8_n, COUNT(*) AS __a9, SUM(issues_assigned * 1.0 / NULLIF(issues_reported, 0)) AS __a10_sum, COUNT(issues_assigned * 1.0 / NULLIF(issues_reported, 0)) AS __a10_n, SUM(CASE WHEN engagement_risk_status = 'At Risk' OR engagement_risk_status = 'Disengaged' THEN 1 ELSE 0 END) AS __a11, SUM(total_outbound_influence - total_inbound_influence) AS __a12_sum, COUNT(total_outbound_influence - total_inbound_influence) AS __a12_n, SUM(CASE WHEN engagement_breadth_score >= 40 THEN 1 ELSE 0 END) AS __a13 FROM "jira__stakeholder_engagement_insights" WHERE engagement_impact_score >= 3 AND cross_functional_projects >= 3 GROUP BY response_pattern_type, engagement_risk_status, CASE WHEN strategic_value_score >= 80 AND engagement_depth_score < 20 THEN 'High Strategic, Low Depth' WHEN strategic_value_score >= 80 AND engagement_depth_score >= 20 THEN 'High Strategic, High Depth' WHEN strategic_value_score < 80 AND engagement_depth_score < 20 THEN 'Low Strategic, Low Depth' ELSE 'Low Strategic, High Depth' END, recommended_engagement_strategy, development_opportunity
```

受益查询 S14 的改写示例：

```sql
SELECT (1.0 * SUM(__a0_sum) / NULLIF(SUM(__a0_n), 0)) AS avg_depth, (1.0 * SUM(__a1_sum) / NULLIF(SUM(__a1_n), 0)) AS avg_breadth, (1.0 * SUM(__a2_sum) / NULLIF(SUM(__a2_n), 0)) AS avg_reported, (1.0 * SUM(__a3_sum) / NULLIF(SUM(__a3_n), 0)) AS avg_assigned, (1.0 * SUM(__a4_sum) / NULLIF(SUM(__a4_n), 0)) AS avg_outbound, (1.0 * SUM(__a5_sum) / NULLIF(SUM(__a5_n), 0)) AS avg_inbound, (1.0 * SUM(__a6_sum) / NULLIF(SUM(__a6_n), 0)) AS avg_strategic, (1.0 * SUM(__a7_sum) / NULLIF(SUM(__a7_n), 0)) AS avg_connections, (1.0 * SUM(__a8_sum) / NULLIF(SUM(__a8_n), 0)) AS avg_total_score FROM temp.reuse_candidate
```

| 原 SQL | 列名一致 | 结果一致 | 比较方法 |
| --- | --- | --- | --- |
| S14 | True | False | exact_multiset |
| S18 | True | True | ordered_numeric_tolerance |
| S19 | True | True | ordered_numeric_tolerance |
| S46 | True | True | ordered_numeric_tolerance |
| S47 | True | True | ordered_numeric_tolerance |
| S62 | True | True | ordered_numeric_tolerance |
| S63 | True | True | ordered_numeric_tolerance |
| S64 | True | True | ordered_numeric_tolerance |


验证状态：rejected_result_mismatch；成本结论：Not benchmarked; correctness alone does not establish net speedup.

结果依赖：自动记录 SQL→Python 的接口父调用，以及源码中引用归档文件的消费者；字面值相同不认定因果。模型方向选择需要人工读取消息，尚未做全面因果标注。

[原始报告](../../../runs/dsv4flash-db-first-full-01/dacomp-064/attempt-01/answer.md)；[统一消息](../../../runs/dsv4flash-db-first-full-01/dacomp-064/attempt-01/messages.jsonl)；[原始 OpenCode 事件](../../../runs/dsv4flash-db-first-full-01/dacomp-064/attempt-01/opencode.jsonl)；[SQL 引擎日志](../../../runs/dsv4flash-db-first-full-01/dacomp-064/attempt-01/sql_journal.jsonl)。

[可读报告（本地图片链接规范化）](../answers/dacomp-064.md)。原始回答保留，分析结论未改写。

## S1

类别 `connection_setup`；来源 `connection`；调用 `0ebc7d055b3742139e50ac89ac61c539`；状态 `success`。

```sql
PRAGMA query_only=ON
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-064/attempt-01/sql/S1.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-064/attempt-01/sql/S1.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-064/attempt-01/results/S1.rows.jsonl)；完整：True；SHA256：`e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`。

## S2

类别 `metadata`；来源 `list_db`；调用 `0ebc7d055b3742139e50ac89ac61c539`；状态 `success`。

```sql
SELECT name,sql FROM sqlite_master WHERE type='table' ORDER BY name
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-064/attempt-01/sql/S2.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-064/attempt-01/sql/S2.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-064/attempt-01/results/S2.rows.jsonl)；完整：True；SHA256：`615fd3a28f2fc7dede6fa23fc55afe65b912fd11f48b70edb694a897025d6b8b`。

## S3

类别 `data`；来源 `query_db`；调用 `b36350d088684cec98cbb90797c331a7`；状态 `success`。

```sql
SELECT COUNT(*) AS n_stakeholders FROM jira__stakeholder_engagement_insights
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-064/attempt-01/sql/S3.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-064/attempt-01/sql/S3.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-064/attempt-01/results/S3.rows.jsonl)；完整：True；SHA256：`d627005cafeb3332957ae72cf9a51f690d805fcb8a5a8212d1ab1e775ae32288`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "jira__stakeholder_engagement_insights", "kind": "base", "block": null, "base_tables": ["jira__stakeholder_engagement_insights"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |


## S4

类别 `data`；来源 `query_db`；调用 `52ae8b77b8634683bc7ae1a87723de27`；状态 `success`。

```sql
SELECT COUNT(*) AS n_issues FROM jira__issue_enhanced
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-064/attempt-01/sql/S4.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-064/attempt-01/sql/S4.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-064/attempt-01/results/S4.rows.jsonl)；完整：True；SHA256：`ca5d97f4dab69813055999493cfea8f56e91e334c1465da9867b484a21b0a9bd`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "jira__issue_enhanced", "kind": "base", "block": null, "base_tables": ["jira__issue_enhanced"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |


## S5

类别 `data`；来源 `query_db`；调用 `ae8910ae553e4eb3a3ad9e79784a3e2b`；状态 `success`。

```sql
SELECT COUNT(*) AS n_daily FROM jira__daily_issue_field_history
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-064/attempt-01/sql/S5.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-064/attempt-01/sql/S5.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-064/attempt-01/results/S5.rows.jsonl)；完整：True；SHA256：`84aba7031949574a4378f726bcb64e067b6186ed127ea06b26c2cbdf2f4187ed`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "jira__daily_issue_field_history", "kind": "base", "block": null, "base_tables": ["jira__daily_issue_field_history"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |


## S6

类别 `data`；来源 `query_db`；调用 `993055bfabfe4429ac31bf2b5cede487`；状态 `success`。

```sql
SELECT COUNT(*) AS n_projects FROM jira__project_enhanced
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-064/attempt-01/sql/S6.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-064/attempt-01/sql/S6.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-064/attempt-01/results/S6.rows.jsonl)；完整：True；SHA256：`8fe64ac838eb7a89546cb6a98f203e335a9c087776008d203b43095ded53e1b7`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "jira__project_enhanced", "kind": "base", "block": null, "base_tables": ["jira__project_enhanced"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |


## S7

类别 `data`；来源 `query_db`；调用 `2ae1f6142e2e4e83892a2b10410636f3`；状态 `success`。

```sql
SELECT MIN(date_day) AS min_day, MAX(date_day) AS max_day FROM jira__daily_issue_field_history
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-064/attempt-01/sql/S7.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-064/attempt-01/sql/S7.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-064/attempt-01/results/S7.rows.jsonl)；完整：True；SHA256：`1576e59d88e0fd6377d98cfdd41a08f3a9759a7b887073ef14fd0ac4887d964b`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "jira__daily_issue_field_history", "kind": "base", "block": null, "base_tables": ["jira__daily_issue_field_history"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | MIN(date_day) | [{"table": "jira__daily_issue_field_history", "column": "date_day"}] | [] | False |
| B1 | MAX(date_day) | [{"table": "jira__daily_issue_field_history", "column": "date_day"}] | [] | False |


## S8

类别 `data`；来源 `query_db`；调用 `55ffe8c2ad5649ecbf6fd58ae92d72df`；状态 `success`。

```sql
SELECT 
  SUM(CASE WHEN engagement_impact_score >= 3 AND cross_functional_projects >= 3 THEN 1 ELSE 0 END) AS n_target,
  SUM(CASE WHEN engagement_impact_score >= 3 THEN 1 ELSE 0 END) AS n_high_impact,
  SUM(CASE WHEN cross_functional_projects >= 3 THEN 1 ELSE 0 END) AS n_cross_func,
  COUNT(*) AS n_total
FROM jira__stakeholder_engagement_insights
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-064/attempt-01/sql/S8.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-064/attempt-01/sql/S8.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-064/attempt-01/results/S8.rows.jsonl)；完整：True；SHA256：`5c952ac3d2b79fcd6613779ed2f9b46f0c5cad2fb74c014e97f3ecb40ae48958`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "jira__stakeholder_engagement_insights", "kind": "base", "block": null, "base_tables": ["jira__stakeholder_engagement_insights"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | SUM(CASE WHEN engagement_impact_score >= 3 AND cross_functional_projects >= 3 THEN 1 ELSE 0 END) | [] | [{"table": "jira__stakeholder_engagement_insights", "column": "engagement_impact_score"}, {"table": "jira__stakeholder_engagement_insights", "column": "cross_functional_projects"}] | False |
| B1 | SUM(CASE WHEN engagement_impact_score >= 3 THEN 1 ELSE 0 END) | [] | [{"table": "jira__stakeholder_engagement_insights", "column": "engagement_impact_score"}] | False |
| B1 | SUM(CASE WHEN cross_functional_projects >= 3 THEN 1 ELSE 0 END) | [] | [{"table": "jira__stakeholder_engagement_insights", "column": "cross_functional_projects"}] | False |
| B1 | COUNT(*) | [] | [] | True |


## S9

类别 `data`；来源 `query_db`；调用 `dad42943cb1b42c98ae0b26239d83ee0`；状态 `success`。

```sql
SELECT engagement_impact_score, COUNT(*) AS n FROM jira__stakeholder_engagement_insights GROUP BY engagement_impact_score ORDER BY engagement_impact_score
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-064/attempt-01/sql/S9.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-064/attempt-01/sql/S9.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-064/attempt-01/results/S9.rows.jsonl)；完整：True；SHA256：`1189697ccea3081f498e90cfb9e525bac432e95e7afdcc077c2e100581cf8cce`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "jira__stakeholder_engagement_insights", "kind": "base", "block": null, "base_tables": ["jira__stakeholder_engagement_insights"]}] | [] | ["engagement_impact_score"] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |


## S10

类别 `data`；来源 `query_db`；调用 `fcecaafba8ec4c42baff84cc9afd5bd6`；状态 `success`。

```sql
SELECT response_pattern_type, COUNT(*) AS n FROM jira__stakeholder_engagement_insights GROUP BY response_pattern_type ORDER BY n DESC
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-064/attempt-01/sql/S10.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-064/attempt-01/sql/S10.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-064/attempt-01/results/S10.rows.jsonl)；完整：True；SHA256：`0e3ee42589da54f765373b8dd74effe958a1ff5668114c6f8b69aff40d19cb45`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "jira__stakeholder_engagement_insights", "kind": "base", "block": null, "base_tables": ["jira__stakeholder_engagement_insights"]}] | [] | ["response_pattern_type"] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |


## S11

类别 `data`；来源 `query_db`；调用 `90f44b68fea04c1f8a6799828faf58ca`；状态 `success`。

```sql
SELECT influence_level, COUNT(*) AS n FROM jira__stakeholder_engagement_insights GROUP BY influence_level ORDER BY n DESC
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-064/attempt-01/sql/S11.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-064/attempt-01/sql/S11.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-064/attempt-01/results/S11.rows.jsonl)；完整：True；SHA256：`e552985cd2fd02db8f53f951a0fc2dcfaa6034850d4cec5118bd8faa267b7133`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "jira__stakeholder_engagement_insights", "kind": "base", "block": null, "base_tables": ["jira__stakeholder_engagement_insights"]}] | [] | ["influence_level"] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |


## S12

类别 `data`；来源 `query_db`；调用 `3aa39ae014924281a83ae1f94a32a73e`；状态 `success`。

```sql
SELECT stakeholder_archetype, COUNT(*) AS n FROM jira__stakeholder_engagement_insights GROUP BY stakeholder_archetype ORDER BY n DESC
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-064/attempt-01/sql/S12.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-064/attempt-01/sql/S12.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-064/attempt-01/results/S12.rows.jsonl)；完整：True；SHA256：`57299b4ed175f4492fd4ff7d566d0155118a196d3b0443984134d4e7962b069a`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "jira__stakeholder_engagement_insights", "kind": "base", "block": null, "base_tables": ["jira__stakeholder_engagement_insights"]}] | [] | ["stakeholder_archetype"] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |


## S13

类别 `data`；来源 `query_db`；调用 `a0d5b7b92dd5490ebb02e4cd829b3d9c`；状态 `success`。

```sql
SELECT engagement_risk_status, COUNT(*) AS n FROM jira__stakeholder_engagement_insights GROUP BY engagement_risk_status ORDER BY n DESC
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-064/attempt-01/sql/S13.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-064/attempt-01/sql/S13.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-064/attempt-01/results/S13.rows.jsonl)；完整：True；SHA256：`54a2fd397d7a72899fc966de1a705efb41c7229ef09303516ba1d0b46d8fbcc8`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "jira__stakeholder_engagement_insights", "kind": "base", "block": null, "base_tables": ["jira__stakeholder_engagement_insights"]}] | [] | ["engagement_risk_status"] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |


## S14

类别 `data`；来源 `query_db`；调用 `962ef0d1e9284a659398e90c07275ac8`；状态 `success`。

```sql
SELECT 
  AVG(engagement_depth_score) AS avg_depth,
  AVG(engagement_breadth_score) AS avg_breadth,
  AVG(issues_reported) AS avg_reported,
  AVG(issues_assigned) AS avg_assigned,
  AVG(total_outbound_influence) AS avg_outbound,
  AVG(total_inbound_influence) AS avg_inbound,
  AVG(strategic_value_score) AS avg_strategic,
  AVG(direct_network_connections) AS avg_connections,
  AVG(total_engagement_score) AS avg_total_score
FROM jira__stakeholder_engagement_insights
WHERE engagement_impact_score >= 3 AND cross_functional_projects >= 3
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-064/attempt-01/sql/S14.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-064/attempt-01/sql/S14.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-064/attempt-01/results/S14.rows.jsonl)；完整：True；SHA256：`43e8b997a98858d8852bfffcae76481d203c78b888f1712a08d9d2452231b826`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "jira__stakeholder_engagement_insights", "kind": "base", "block": null, "base_tables": ["jira__stakeholder_engagement_insights"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | AVG(engagement_depth_score) | [{"table": "jira__stakeholder_engagement_insights", "column": "engagement_depth_score"}] | [] | False |
| B1 | AVG(engagement_breadth_score) | [{"table": "jira__stakeholder_engagement_insights", "column": "engagement_breadth_score"}] | [] | False |
| B1 | AVG(issues_reported) | [{"table": "jira__stakeholder_engagement_insights", "column": "issues_reported"}] | [] | False |
| B1 | AVG(issues_assigned) | [{"table": "jira__stakeholder_engagement_insights", "column": "issues_assigned"}] | [] | False |
| B1 | AVG(total_outbound_influence) | [{"table": "jira__stakeholder_engagement_insights", "column": "total_outbound_influence"}] | [] | False |
| B1 | AVG(total_inbound_influence) | [{"table": "jira__stakeholder_engagement_insights", "column": "total_inbound_influence"}] | [] | False |
| B1 | AVG(strategic_value_score) | [{"table": "jira__stakeholder_engagement_insights", "column": "strategic_value_score"}] | [] | False |
| B1 | AVG(direct_network_connections) | [{"table": "jira__stakeholder_engagement_insights", "column": "direct_network_connections"}] | [] | False |
| B1 | AVG(total_engagement_score) | [{"table": "jira__stakeholder_engagement_insights", "column": "total_engagement_score"}] | [] | False |


## S15

类别 `data`；来源 `query_db`；调用 `e2db5dd751a14cd78467b086cc45bff1`；状态 `success`。

```sql
SELECT 
  AVG(engagement_depth_score) AS avg_depth,
  AVG(engagement_breadth_score) AS avg_breadth,
  AVG(issues_reported) AS avg_reported,
  AVG(issues_assigned) AS avg_assigned,
  AVG(total_outbound_influence) AS avg_outbound,
  AVG(total_inbound_influence) AS avg_inbound,
  AVG(strategic_value_score) AS avg_strategic,
  AVG(direct_network_connections) AS avg_connections,
  AVG(total_engagement_score) AS avg_total_score
FROM jira__stakeholder_engagement_insights
WHERE NOT (engagement_impact_score >= 3 AND cross_functional_projects >= 3)
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-064/attempt-01/sql/S15.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-064/attempt-01/sql/S15.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-064/attempt-01/results/S15.rows.jsonl)；完整：True；SHA256：`4236be1e321fb298e7cfbada31fb72701441b4557c30fdc4d15352bfc68a236b`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "jira__stakeholder_engagement_insights", "kind": "base", "block": null, "base_tables": ["jira__stakeholder_engagement_insights"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | AVG(engagement_depth_score) | [{"table": "jira__stakeholder_engagement_insights", "column": "engagement_depth_score"}] | [] | False |
| B1 | AVG(engagement_breadth_score) | [{"table": "jira__stakeholder_engagement_insights", "column": "engagement_breadth_score"}] | [] | False |
| B1 | AVG(issues_reported) | [{"table": "jira__stakeholder_engagement_insights", "column": "issues_reported"}] | [] | False |
| B1 | AVG(issues_assigned) | [{"table": "jira__stakeholder_engagement_insights", "column": "issues_assigned"}] | [] | False |
| B1 | AVG(total_outbound_influence) | [{"table": "jira__stakeholder_engagement_insights", "column": "total_outbound_influence"}] | [] | False |
| B1 | AVG(total_inbound_influence) | [{"table": "jira__stakeholder_engagement_insights", "column": "total_inbound_influence"}] | [] | False |
| B1 | AVG(strategic_value_score) | [{"table": "jira__stakeholder_engagement_insights", "column": "strategic_value_score"}] | [] | False |
| B1 | AVG(direct_network_connections) | [{"table": "jira__stakeholder_engagement_insights", "column": "direct_network_connections"}] | [] | False |
| B1 | AVG(total_engagement_score) | [{"table": "jira__stakeholder_engagement_insights", "column": "total_engagement_score"}] | [] | False |


## S16

类别 `data`；来源 `query_db`；调用 `fa36789f30a14f2eba0a1d2237b6d64e`；状态 `failed`。

```sql
SELECT 
  MIN(engagement_depth_score) AS min_depth, MAX(engagement_depth_score) AS max_depth,
  MIN(engagement_breadth_score) AS min_breadth, MAX(engagement_breadth_score) AS max_breadth,
  MIN(strategic_value_score) AS min_strat, MAX(strategic_value_score) AS max_strat,
  MIN(avg_close_time_days) AS min_close, MAX(avg_close_time_days) AS max_close
FROM jira__user_enhanced
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-064/attempt-01/sql/S16.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-064/attempt-01/sql/S16.parameters.json)。

错误：`OperationalError('no such column: engagement_depth_score')`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "jira__user_enhanced", "kind": "base", "block": null, "base_tables": ["jira__user_enhanced"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | MIN(engagement_depth_score) | [{"unknown": "engagement_depth_score"}] | [] | False |
| B1 | MAX(engagement_depth_score) | [{"unknown": "engagement_depth_score"}] | [] | False |
| B1 | MIN(engagement_breadth_score) | [{"unknown": "engagement_breadth_score"}] | [] | False |
| B1 | MAX(engagement_breadth_score) | [{"unknown": "engagement_breadth_score"}] | [] | False |
| B1 | MIN(strategic_value_score) | [{"unknown": "strategic_value_score"}] | [] | False |
| B1 | MAX(strategic_value_score) | [{"unknown": "strategic_value_score"}] | [] | False |
| B1 | MIN(avg_close_time_days) | [{"table": "jira__user_enhanced", "column": "avg_close_time_days"}] | [] | False |
| B1 | MAX(avg_close_time_days) | [{"table": "jira__user_enhanced", "column": "avg_close_time_days"}] | [] | False |


未解析列血缘：[{"block": "B1", "column": "engagement_depth_score", "reason": "ambiguous_or_missing_source"}, {"block": "B1", "column": "engagement_depth_score", "reason": "ambiguous_or_missing_source"}, {"block": "B1", "column": "engagement_breadth_score", "reason": "ambiguous_or_missing_source"}, {"block": "B1", "column": "engagement_breadth_score", "reason": "ambiguous_or_missing_source"}, {"block": "B1", "column": "strategic_value_score", "reason": "ambiguous_or_missing_source"}, {"block": "B1", "column": "strategic_value_score", "reason": "ambiguous_or_missing_source"}, {"block": "B1", "column": "engagement_depth_score", "reason": "ambiguous_or_missing_source"}, {"block": "B1", "column": "engagement_depth_score", "reason": "ambiguous_or_missing_source"}, {"block": "B1", "column": "engagement_breadth_score", "reason": "ambiguous_or_missing_source"}, {"block": "B1", "column": "engagement_breadth_score", "reason": "ambiguous_or_missing_source"}, {"block": "B1", "column": "strategic_value_score", "reason": "ambiguous_or_missing_source"}, {"block": "B1", "column": "strategic_value_score", "reason": "ambiguous_or_missing_source"}]

## S17

类别 `data`；来源 `query_db`；调用 `5ebe3cb686414341ab619dd3ee81324b`；状态 `success`。

```sql
SELECT 
  MIN(engagement_depth_score) AS min_depth, MAX(engagement_depth_score) AS max_depth,
  MIN(engagement_breadth_score) AS min_breadth, MAX(engagement_breadth_score) AS max_breadth,
  MIN(strategic_value_score) AS min_strat, MAX(strategic_value_score) AS max_strat,
  MIN(engagement_quality_score) AS min_qual, MAX(engagement_quality_score) AS max_qual,
  MIN(total_engagement_score) AS min_tot, MAX(total_engagement_score) AS max_tot
FROM jira__stakeholder_engagement_insights
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-064/attempt-01/sql/S17.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-064/attempt-01/sql/S17.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-064/attempt-01/results/S17.rows.jsonl)；完整：True；SHA256：`3a75dc45de9d64b2d36caf74be705e9adbffc00ed3a70270ace805b3fed96e6c`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "jira__stakeholder_engagement_insights", "kind": "base", "block": null, "base_tables": ["jira__stakeholder_engagement_insights"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | MIN(engagement_depth_score) | [{"table": "jira__stakeholder_engagement_insights", "column": "engagement_depth_score"}] | [] | False |
| B1 | MAX(engagement_depth_score) | [{"table": "jira__stakeholder_engagement_insights", "column": "engagement_depth_score"}] | [] | False |
| B1 | MIN(engagement_breadth_score) | [{"table": "jira__stakeholder_engagement_insights", "column": "engagement_breadth_score"}] | [] | False |
| B1 | MAX(engagement_breadth_score) | [{"table": "jira__stakeholder_engagement_insights", "column": "engagement_breadth_score"}] | [] | False |
| B1 | MIN(strategic_value_score) | [{"table": "jira__stakeholder_engagement_insights", "column": "strategic_value_score"}] | [] | False |
| B1 | MAX(strategic_value_score) | [{"table": "jira__stakeholder_engagement_insights", "column": "strategic_value_score"}] | [] | False |
| B1 | MIN(engagement_quality_score) | [{"table": "jira__stakeholder_engagement_insights", "column": "engagement_quality_score"}] | [] | False |
| B1 | MAX(engagement_quality_score) | [{"table": "jira__stakeholder_engagement_insights", "column": "engagement_quality_score"}] | [] | False |
| B1 | MIN(total_engagement_score) | [{"table": "jira__stakeholder_engagement_insights", "column": "total_engagement_score"}] | [] | False |
| B1 | MAX(total_engagement_score) | [{"table": "jira__stakeholder_engagement_insights", "column": "total_engagement_score"}] | [] | False |


## S18

类别 `data`；来源 `query_db`；调用 `b8536682119047b882d06a05ebf41ff0`；状态 `success`。

```sql
SELECT response_pattern_type, COUNT(*) AS n, 
  ROUND(AVG(engagement_depth_score),2) AS avg_depth,
  ROUND(AVG(engagement_breadth_score),2) AS avg_breadth,
  ROUND(AVG(total_outbound_influence),2) AS avg_out,
  ROUND(AVG(total_inbound_influence),2) AS avg_in,
  ROUND(AVG(issues_assigned*1.0/NULLIF(issues_reported,0)),2) AS assign_report_ratio
FROM jira__stakeholder_engagement_insights
WHERE engagement_impact_score >= 3 AND cross_functional_projects >= 3
GROUP BY response_pattern_type
ORDER BY n DESC
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-064/attempt-01/sql/S18.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-064/attempt-01/sql/S18.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-064/attempt-01/results/S18.rows.jsonl)；完整：True；SHA256：`ac94887eb5755400498bfbf48fe185dd2ce18ddae3618a1a730fa23b1fa398d5`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "jira__stakeholder_engagement_insights", "kind": "base", "block": null, "base_tables": ["jira__stakeholder_engagement_insights"]}] | [] | ["response_pattern_type"] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |
| B1 | AVG(engagement_depth_score) | [{"table": "jira__stakeholder_engagement_insights", "column": "engagement_depth_score"}] | [] | False |
| B1 | AVG(engagement_breadth_score) | [{"table": "jira__stakeholder_engagement_insights", "column": "engagement_breadth_score"}] | [] | False |
| B1 | AVG(total_outbound_influence) | [{"table": "jira__stakeholder_engagement_insights", "column": "total_outbound_influence"}] | [] | False |
| B1 | AVG(total_inbound_influence) | [{"table": "jira__stakeholder_engagement_insights", "column": "total_inbound_influence"}] | [] | False |
| B1 | AVG(issues_assigned * 1.0 / NULLIF(issues_reported, 0)) | [{"table": "jira__stakeholder_engagement_insights", "column": "issues_assigned"}, {"table": "jira__stakeholder_engagement_insights", "column": "issues_reported"}] | [] | False |


## S19

类别 `data`；来源 `query_db`；调用 `567cf01f19384925907c4b1d19144f1a`；状态 `success`。

```sql
SELECT engagement_risk_status, COUNT(*) AS n,
  ROUND(AVG(engagement_depth_score),2) AS avg_depth,
  ROUND(AVG(engagement_breadth_score),2) AS avg_breadth,
  ROUND(AVG(total_outbound_influence),2) AS avg_out,
  ROUND(AVG(total_inbound_influence),2) AS avg_in
FROM jira__stakeholder_engagement_insights
WHERE engagement_impact_score >= 3 AND cross_functional_projects >= 3
GROUP BY engagement_risk_status
ORDER BY n DESC
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-064/attempt-01/sql/S19.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-064/attempt-01/sql/S19.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-064/attempt-01/results/S19.rows.jsonl)；完整：True；SHA256：`efe7a9a523a6bd1bdf2435f8306276e3a175787e5d00e6ab35894b1e5901d79a`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "jira__stakeholder_engagement_insights", "kind": "base", "block": null, "base_tables": ["jira__stakeholder_engagement_insights"]}] | [] | ["engagement_risk_status"] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |
| B1 | AVG(engagement_depth_score) | [{"table": "jira__stakeholder_engagement_insights", "column": "engagement_depth_score"}] | [] | False |
| B1 | AVG(engagement_breadth_score) | [{"table": "jira__stakeholder_engagement_insights", "column": "engagement_breadth_score"}] | [] | False |
| B1 | AVG(total_outbound_influence) | [{"table": "jira__stakeholder_engagement_insights", "column": "total_outbound_influence"}] | [] | False |
| B1 | AVG(total_inbound_influence) | [{"table": "jira__stakeholder_engagement_insights", "column": "total_inbound_influence"}] | [] | False |


## S20

类别 `data`；来源 `query_db`；调用 `928031925d0f4acb8ed653196b65fbec`；状态 `success`。

```sql
SELECT stakeholder_id, user_display_name FROM jira__stakeholder_engagement_insights LIMIT 5
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-064/attempt-01/sql/S20.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-064/attempt-01/sql/S20.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-064/attempt-01/results/S20.rows.jsonl)；完整：True；SHA256：`fd1cbb1b266cc90f2d15b8f28b7883ccec7380e8906125081faa5fe30a7efb2f`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "jira__stakeholder_engagement_insights", "kind": "base", "block": null, "base_tables": ["jira__stakeholder_engagement_insights"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |


## S21

类别 `data`；来源 `query_db`；调用 `fdfc89d16dfc4521b33fe3182bd205e2`；状态 `success`。

```sql
SELECT assignee_user_id, assignee_name, COUNT(*) n FROM jira__issue_enhanced GROUP BY assignee_user_id, assignee_name ORDER BY n DESC LIMIT 5
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-064/attempt-01/sql/S21.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-064/attempt-01/sql/S21.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-064/attempt-01/results/S21.rows.jsonl)；完整：True；SHA256：`27ea552c730e64f9057200fefed06e776cfeb9d1b9ea6e09cc7848d3f52f6cac`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "jira__issue_enhanced", "kind": "base", "block": null, "base_tables": ["jira__issue_enhanced"]}] | [] | ["assignee_user_id", "assignee_name"] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |


## S22

类别 `data`；来源 `query_db`；调用 `a1fbf05effa743d3960098c85ba84df4`；状态 `success`。

```sql
SELECT user_id, user_display_name FROM jira__user_enhanced LIMIT 5
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-064/attempt-01/sql/S22.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-064/attempt-01/sql/S22.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-064/attempt-01/results/S22.rows.jsonl)；完整：True；SHA256：`03ef026869cbb5d433dd4102ee84d3651b5d7931e81191b862477debac59abc7`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "jira__user_enhanced", "kind": "base", "block": null, "base_tables": ["jira__user_enhanced"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |


## S23

类别 `data`；来源 `query_db`；调用 `bd2e911bb4be4912bd422256f599e6a2`；状态 `success`。

```sql
SELECT MIN(created_at) min_c, MAX(created_at) max_c, MIN(resolved_at) min_r, MAX(resolved_at) max_r FROM jira__issue_enhanced
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-064/attempt-01/sql/S23.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-064/attempt-01/sql/S23.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-064/attempt-01/results/S23.rows.jsonl)；完整：True；SHA256：`4fc6b726b44cc6b1df7cbd64fe8d36dfbda44f169fc158abf42de8ef3b40c0fb`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "jira__issue_enhanced", "kind": "base", "block": null, "base_tables": ["jira__issue_enhanced"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | MIN(created_at) | [{"table": "jira__issue_enhanced", "column": "created_at"}] | [] | False |
| B1 | MAX(created_at) | [{"table": "jira__issue_enhanced", "column": "created_at"}] | [] | False |
| B1 | MIN(resolved_at) | [{"table": "jira__issue_enhanced", "column": "resolved_at"}] | [] | False |
| B1 | MAX(resolved_at) | [{"table": "jira__issue_enhanced", "column": "resolved_at"}] | [] | False |


## S24

类别 `data`；来源 `query_db`；调用 `07077c12d56c4908b05e0ca649cae3c0`；状态 `success`。

```sql
-- Check if stakeholder user_display_names match assignee_name
SELECT s.user_display_name, s.stakeholder_id, i.assignee_name, i.assignee_user_id
FROM jira__stakeholder_engagement_insights s
JOIN jira__issue_enhanced i ON s.user_display_name = i.assignee_name
LIMIT 10
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-064/attempt-01/sql/S24.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-064/attempt-01/sql/S24.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-064/attempt-01/results/S24.rows.jsonl)；完整：True；SHA256：`dfbafbc51d39bc11c40a47948f3f65e81fe64ea7c695aeca023bece486f55919`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "s", "kind": "base", "block": null, "base_tables": ["jira__stakeholder_engagement_insights"]}, {"alias": "i", "kind": "base", "block": null, "base_tables": ["jira__issue_enhanced"]}] | [{"type": "INNER", "right": "jira__issue_enhanced AS i", "on": "s.user_display_name = i.assignee_name", "using": []}] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |


## S25

类别 `data`；来源 `query_db`；调用 `3d45ff59c69844abbff2cbcd5cd86854`；状态 `success`。

```sql
-- Check if stakeholder_id matches user_id
SELECT s.stakeholder_id, u.user_id, s.user_display_name, u.user_display_name
FROM jira__stakeholder_engagement_insights s
LEFT JOIN jira__user_enhanced u ON s.stakeholder_id = u.user_id
LIMIT 10
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-064/attempt-01/sql/S25.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-064/attempt-01/sql/S25.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-064/attempt-01/results/S25.rows.jsonl)；完整：True；SHA256：`104e138dd479bb211d111d4a75b41b93d9f4a6cf0fca8930ab5ba54e5297935c`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "s", "kind": "base", "block": null, "base_tables": ["jira__stakeholder_engagement_insights"]}, {"alias": "u", "kind": "base", "block": null, "base_tables": ["jira__user_enhanced"]}] | [{"type": "LEFT", "right": "jira__user_enhanced AS u", "on": "s.stakeholder_id = u.user_id", "using": []}] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |


## S26

类别 `data`；来源 `query_db`；调用 `7991685b319d430f9c120b575dfbbfa3`；状态 `success`。

```sql
-- How many distinct names in issues match stakeholder names
SELECT COUNT(DISTINCT s.stakeholder_id) AS stakeholders_with_issues_as_assignee
FROM jira__stakeholder_engagement_insights s
JOIN jira__issue_enhanced i ON s.user_display_name = i.assignee_name
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-064/attempt-01/sql/S26.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-064/attempt-01/sql/S26.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-064/attempt-01/results/S26.rows.jsonl)；完整：True；SHA256：`0cd82efbf0e0bf2d5d8a678bd070ec92be183ca294485f68fe6d66c3cd38af3c`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "s", "kind": "base", "block": null, "base_tables": ["jira__stakeholder_engagement_insights"]}, {"alias": "i", "kind": "base", "block": null, "base_tables": ["jira__issue_enhanced"]}] | [{"type": "INNER", "right": "jira__issue_enhanced AS i", "on": "s.user_display_name = i.assignee_name", "using": []}] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(DISTINCT s.stakeholder_id) | [{"table": "jira__stakeholder_engagement_insights", "column": "stakeholder_id"}] | [] | False |


## S27

类别 `data`；来源 `query_db`；调用 `71ab916374c5426385241bde5b17e3be`；状态 `success`。

```sql
-- Distinct assignee_user_id per assignee_name sample
SELECT assignee_name, COUNT(DISTINCT assignee_user_id) AS n_ids, COUNT(*) AS n_issues
FROM jira__issue_enhanced
GROUP BY assignee_name
HAVING n_ids > 1
LIMIT 10
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-064/attempt-01/sql/S27.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-064/attempt-01/sql/S27.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-064/attempt-01/results/S27.rows.jsonl)；完整：True；SHA256：`d34932be579bd5c6cbc06bdf0d31e061421149154179e5f5b78a7da4c90a5f71`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "jira__issue_enhanced", "kind": "base", "block": null, "base_tables": ["jira__issue_enhanced"]}] | [] | ["assignee_name"] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(DISTINCT assignee_user_id) | [{"table": "jira__issue_enhanced", "column": "assignee_user_id"}] | [] | False |
| B1 | COUNT(*) | [] | [] | True |


## S28

类别 `data`；来源 `query_db`；调用 `13db47f096bd48bf802ec4bbf0be6c64`；状态 `success`。

```sql
SELECT COUNT(*) AS total_issues_assigned FROM jira__issue_enhanced WHERE assignee_name IS NOT NULL
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-064/attempt-01/sql/S28.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-064/attempt-01/sql/S28.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-064/attempt-01/results/S28.rows.jsonl)；完整：True；SHA256：`ca5d97f4dab69813055999493cfea8f56e91e334c1465da9867b484a21b0a9bd`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "jira__issue_enhanced", "kind": "base", "block": null, "base_tables": ["jira__issue_enhanced"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |


## S29

类别 `data`；来源 `query_db`；调用 `c31f0230118448bd9e997a12c820cec3`；状态 `success`。

```sql
-- Target stakeholders' issue counts and closest times
SELECT 
  s.stakeholder_id,
  s.user_display_name,
  s.engagement_depth_score,
  s.engagement_breadth_score,
  s.total_outbound_influence,
  s.total_inbound_influence,
  s.issues_assigned,
  s.issues_reported,
  s.engagement_impact_score,
  s.cross_functional_projects,
  s.strategic_value_score,
  s.direct_network_connections,
  s.response_pattern_type,
  s.engagement_risk_status
FROM jira__stakeholder_engagement_insights s
WHERE s.engagement_impact_score >= 3 AND s.cross_functional_projects >= 3
ORDER BY s.total_engagement_score DESC
LIMIT 20
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-064/attempt-01/sql/S29.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-064/attempt-01/sql/S29.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-064/attempt-01/results/S29.rows.jsonl)；完整：True；SHA256：`dab9cf687d4f02a99ef496d34fddf35d94bdfd247b5c4518d7bf3d7538df4b8e`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "s", "kind": "base", "block": null, "base_tables": ["jira__stakeholder_engagement_insights"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |


## S30

类别 `data`；来源 `query_db`；调用 `fc3d1180810740028851cdaba31535f9`；状态 `success`。

```sql
SELECT date_day, date_week, status, issue_type, COUNT(*) n
FROM jira__daily_issue_field_history
GROUP BY date_day, date_week, status, issue_type
ORDER BY date_day
LIMIT 10
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-064/attempt-01/sql/S30.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-064/attempt-01/sql/S30.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-064/attempt-01/results/S30.rows.jsonl)；完整：True；SHA256：`62e90bf3984a0b47d01bb383f8dc18cd15217fed20021bbc94e322a177778548`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "jira__daily_issue_field_history", "kind": "base", "block": null, "base_tables": ["jira__daily_issue_field_history"]}] | [] | ["date_day", "date_week", "status", "issue_type"] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |


## S31

类别 `data`；来源 `query_db`；调用 `636d0a524d854fd394eadd7fe594e8bf`；状态 `success`。

```sql
SELECT COUNT(DISTINCT issue_id) AS n_issues, COUNT(DISTINCT date_day) AS n_days, COUNT(DISTINCT assignee) AS n_assignees, COUNT(DISTINCT reporter) AS n_reporters
FROM jira__daily_issue_field_history
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-064/attempt-01/sql/S31.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-064/attempt-01/sql/S31.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-064/attempt-01/results/S31.rows.jsonl)；完整：True；SHA256：`597936f304da12d4eeb8fa32ab73f7ffd792b8e1c1f4f8dd9e677ddfea42d282`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "jira__daily_issue_field_history", "kind": "base", "block": null, "base_tables": ["jira__daily_issue_field_history"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(DISTINCT issue_id) | [{"table": "jira__daily_issue_field_history", "column": "issue_id"}] | [] | False |
| B1 | COUNT(DISTINCT date_day) | [{"table": "jira__daily_issue_field_history", "column": "date_day"}] | [] | False |
| B1 | COUNT(DISTINCT assignee) | [{"table": "jira__daily_issue_field_history", "column": "assignee"}] | [] | False |
| B1 | COUNT(DISTINCT reporter) | [{"table": "jira__daily_issue_field_history", "column": "reporter"}] | [] | False |


## S32

类别 `data`；来源 `query_db`；调用 `aaa150ff5bff4e329d359883ea43fc99`；状态 `success`。

```sql
SELECT assignee, reporter FROM jira__daily_issue_field_history LIMIT 10
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-064/attempt-01/sql/S32.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-064/attempt-01/sql/S32.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-064/attempt-01/results/S32.rows.jsonl)；完整：True；SHA256：`aaf6ed7679f18724ad2779a9713952b12b285b959663586a61c23297396fba9a`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "jira__daily_issue_field_history", "kind": "base", "block": null, "base_tables": ["jira__daily_issue_field_history"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |


## S33

类别 `data`；来源 `query_db`；调用 `b2fb2ba9e1fd4410b4c7c08e6cba2999`；状态 `success`。

```sql
-- Check if daily assignee IDs match stakeholder IDs
SELECT COUNT(DISTINCT d.assignee) AS daily_assignee_ids,
       COUNT(DISTINCT CASE WHEN s.stakeholder_id IS NOT NULL THEN d.assignee END) AS matched_to_stakeholders
FROM (SELECT DISTINCT assignee FROM jira__daily_issue_field_history) d
LEFT JOIN jira__stakeholder_engagement_insights s ON d.assignee = s.stakeholder_id
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-064/attempt-01/sql/S33.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-064/attempt-01/sql/S33.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-064/attempt-01/results/S33.rows.jsonl)；完整：True；SHA256：`b382ab9f15b199d4e1d07738b3b0409ceecd89973c366f50cb967b61e45145cb`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "jira__daily_issue_field_history", "kind": "base", "block": null, "base_tables": ["jira__daily_issue_field_history"]}] | [] | [] |
| B2 | [{"alias": "d", "kind": "derived", "block": "B1", "base_tables": ["jira__daily_issue_field_history"]}, {"alias": "s", "kind": "base", "block": null, "base_tables": ["jira__stakeholder_engagement_insights"]}] | [{"type": "LEFT", "right": "jira__stakeholder_engagement_insights AS s", "on": "d.assignee = s.stakeholder_id", "using": []}] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B2 | COUNT(DISTINCT d.assignee) | [{"table": "jira__daily_issue_field_history", "column": "assignee"}] | [] | False |
| B2 | COUNT(DISTINCT CASE WHEN NOT s.stakeholder_id IS NULL THEN d.assignee END) | [{"table": "jira__daily_issue_field_history", "column": "assignee"}] | [{"table": "jira__stakeholder_engagement_insights", "column": "stakeholder_id"}] | False |


## S34

类别 `data`；来源 `query_db`；调用 `06b50c778aff4b4fb6b75dd35b21fb58`；状态 `success`。

```sql
-- Check if issue assignee_user_id matches stakeholder IDs
SELECT COUNT(DISTINCT i.assignee_user_id) AS issue_assignee_ids,
       COUNT(DISTINCT CASE WHEN s.stakeholder_id IS NOT NULL THEN i.assignee_user_id END) AS matched_to_stakeholders
FROM (SELECT DISTINCT assignee_user_id FROM jira__issue_enhanced) i
LEFT JOIN jira__stakeholder_engagement_insights s ON i.assignee_user_id = s.stakeholder_id
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-064/attempt-01/sql/S34.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-064/attempt-01/sql/S34.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-064/attempt-01/results/S34.rows.jsonl)；完整：True；SHA256：`4fa4aa2a7fc46eb7e9fe936eced901a1ad0f24b6c107ffc50fb3652694da6bd3`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "jira__issue_enhanced", "kind": "base", "block": null, "base_tables": ["jira__issue_enhanced"]}] | [] | [] |
| B2 | [{"alias": "i", "kind": "derived", "block": "B1", "base_tables": ["jira__issue_enhanced"]}, {"alias": "s", "kind": "base", "block": null, "base_tables": ["jira__stakeholder_engagement_insights"]}] | [{"type": "LEFT", "right": "jira__stakeholder_engagement_insights AS s", "on": "i.assignee_user_id = s.stakeholder_id", "using": []}] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B2 | COUNT(DISTINCT i.assignee_user_id) | [{"table": "jira__issue_enhanced", "column": "assignee_user_id"}] | [] | False |
| B2 | COUNT(DISTINCT CASE WHEN NOT s.stakeholder_id IS NULL THEN i.assignee_user_id END) | [{"table": "jira__issue_enhanced", "column": "assignee_user_id"}] | [{"table": "jira__stakeholder_engagement_insights", "column": "stakeholder_id"}] | False |


## S35

类别 `data`；来源 `query_db`；调用 `c6256eda46074ed6869211247dd4b283`；状态 `success`。

```sql
-- Match daily reporter IDs to stakeholders
SELECT COUNT(DISTINCT d.reporter) AS daily_reporter_ids,
       COUNT(DISTINCT CASE WHEN s.stakeholder_id IS NOT NULL THEN d.reporter END) AS matched
FROM (SELECT DISTINCT reporter FROM jira__daily_issue_field_history) d
LEFT JOIN jira__stakeholder_engagement_insights s ON d.reporter = s.stakeholder_id
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-064/attempt-01/sql/S35.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-064/attempt-01/sql/S35.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-064/attempt-01/results/S35.rows.jsonl)；完整：True；SHA256：`0abddb7303cb8e1539a74b95de16edcafe643024ff7a6de5cf0142fef0249459`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "jira__daily_issue_field_history", "kind": "base", "block": null, "base_tables": ["jira__daily_issue_field_history"]}] | [] | [] |
| B2 | [{"alias": "d", "kind": "derived", "block": "B1", "base_tables": ["jira__daily_issue_field_history"]}, {"alias": "s", "kind": "base", "block": null, "base_tables": ["jira__stakeholder_engagement_insights"]}] | [{"type": "LEFT", "right": "jira__stakeholder_engagement_insights AS s", "on": "d.reporter = s.stakeholder_id", "using": []}] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B2 | COUNT(DISTINCT d.reporter) | [{"table": "jira__daily_issue_field_history", "column": "reporter"}] | [] | False |
| B2 | COUNT(DISTINCT CASE WHEN NOT s.stakeholder_id IS NULL THEN d.reporter END) | [{"table": "jira__daily_issue_field_history", "column": "reporter"}] | [{"table": "jira__stakeholder_engagement_insights", "column": "stakeholder_id"}] | False |


## S36

类别 `data`；来源 `query_db`；调用 `f6fc14709c31467ea94fe0853b401f40`；状态 `success`。

```sql
-- Get all target stakeholders with their metrics
SELECT s.stakeholder_id, s.user_display_name, s.engagement_depth_score, s.engagement_breadth_score,
       s.engagement_quality_score, s.engagement_impact_score, s.total_engagement_score,
       s.issues_reported, s.issues_assigned, s.total_comments_authored,
       s.total_projects_involved, s.direct_network_connections,
       s.total_outbound_influence, s.total_inbound_influence,
       s.cross_functional_projects, s.strategic_value_score,
       s.response_pattern_type, s.stakeholder_archetype, s.influence_level,
       s.engagement_risk_status, s.recommended_engagement_strategy,
       s.development_opportunity,
       CASE WHEN s.issues_reported > 0 THEN s.issues_assigned * 1.0 / s.issues_reported ELSE NULL END AS assign_report_ratio,
       s.total_outbound_influence - s.total_inbound_influence AS influence_imbalance
FROM jira__stakeholder_engagement_insights s
WHERE s.engagement_impact_score >= 3 AND s.cross_functional_projects >= 3
ORDER BY s.total_engagement_score DESC
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-064/attempt-01/sql/S36.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-064/attempt-01/sql/S36.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-064/attempt-01/results/S36.rows.jsonl)；完整：True；SHA256：`101b2da6dddb7ff3859fc5752171462ac56d6dac00f01dc076ebe1627f7f0c14`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "s", "kind": "base", "block": null, "base_tables": ["jira__stakeholder_engagement_insights"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |


## S37

类别 `data`；来源 `query_db`；调用 `0aab6401fc8243e593af5f52b9414691`；状态 `success`。

```sql
-- Monthly workload trend for target stakeholders (assignee side)
SELECT 
  strftime('%Y-%m', i.created_at) AS month,
  COUNT(*) AS n_created,
  ROUND(AVG(i.open_duration_seconds/86400.0),2) AS avg_open_days,
  ROUND(AVG(i.any_assignment_duration_seconds/86400.0),2) AS avg_assignment_days,
  ROUND(AVG(i.work_ratio),3) AS avg_work_ratio,
  COUNT(DISTINCT i.assignee_user_id) AS n_distinct_assignees
FROM jira__issue_enhanced i
JOIN jira__stakeholder_engagement_insights s ON i.assignee_user_id = s.stakeholder_id
WHERE s.engagement_impact_score >= 3 AND s.cross_functional_projects >= 3
GROUP BY strftime('%Y-%m', i.created_at)
ORDER BY month
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-064/attempt-01/sql/S37.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-064/attempt-01/sql/S37.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-064/attempt-01/results/S37.rows.jsonl)；完整：True；SHA256：`4bd9ed8d35ee95f1222be158f7df3cc6166759675ecccdec92025d060fc12ce6`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "i", "kind": "base", "block": null, "base_tables": ["jira__issue_enhanced"]}, {"alias": "s", "kind": "base", "block": null, "base_tables": ["jira__stakeholder_engagement_insights"]}] | [{"type": "INNER", "right": "jira__stakeholder_engagement_insights AS s", "on": "i.assignee_user_id = s.stakeholder_id", "using": []}] | ["STRFTIME('%Y-%m', i.created_at)"] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |
| B1 | COUNT(DISTINCT i.assignee_user_id) | [{"table": "jira__issue_enhanced", "column": "assignee_user_id"}] | [] | False |
| B1 | AVG(i.open_duration_seconds / 86400.0) | [{"table": "jira__issue_enhanced", "column": "open_duration_seconds"}] | [] | False |
| B1 | AVG(i.any_assignment_duration_seconds / 86400.0) | [{"table": "jira__issue_enhanced", "column": "any_assignment_duration_seconds"}] | [] | False |
| B1 | AVG(i.work_ratio) | [{"table": "jira__issue_enhanced", "column": "work_ratio"}] | [] | False |


## S38

类别 `data`；来源 `query_db`；调用 `5222004769f947ca80c3b7c57d8a3a70`；状态 `success`。

```sql
-- Monthly resolution trend for target stakeholders
SELECT 
  strftime('%Y-%m', i.resolved_at) AS month,
  COUNT(*) AS n_resolved,
  ROUND(AVG((julianday(i.resolved_at) - julianday(i.created_at))*1.0),2) AS avg_close_days
FROM jira__issue_enhanced i
JOIN jira__stakeholder_engagement_insights s ON i.assignee_user_id = s.stakeholder_id
WHERE s.engagement_impact_score >= 3 AND s.cross_functional_projects >= 3
  AND i.resolved_at IS NOT NULL
GROUP BY strftime('%Y-%m', i.resolved_at)
ORDER BY month
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-064/attempt-01/sql/S38.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-064/attempt-01/sql/S38.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-064/attempt-01/results/S38.rows.jsonl)；完整：True；SHA256：`514170275cd0bb2179be47ef0958d7b0d63c68fb9d9184071214648dfe6fe041`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "i", "kind": "base", "block": null, "base_tables": ["jira__issue_enhanced"]}, {"alias": "s", "kind": "base", "block": null, "base_tables": ["jira__stakeholder_engagement_insights"]}] | [{"type": "INNER", "right": "jira__stakeholder_engagement_insights AS s", "on": "i.assignee_user_id = s.stakeholder_id", "using": []}] | ["STRFTIME('%Y-%m', i.resolved_at)"] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |
| B1 | AVG((JULIANDAY(i.resolved_at) - JULIANDAY(i.created_at)) * 1.0) | [{"table": "jira__issue_enhanced", "column": "resolved_at"}, {"table": "jira__issue_enhanced", "column": "created_at"}] | [] | False |


## S39

类别 `data`；来源 `query_db`；调用 `7d7ecc37c99a4fff89afc0d2911bff63`；状态 `success`。

```sql
-- Project type distribution for target stakeholders
SELECT i.project_name, i.issue_type, COUNT(*) AS n_issues,
       ROUND(AVG(i.open_duration_seconds/86400.0),1) AS avg_open_days,
       ROUND(AVG(CASE WHEN i.resolved_at IS NOT NULL THEN (julianday(i.resolved_at)-julianday(i.created_at)) END),2) AS avg_close_days
FROM jira__issue_enhanced i
JOIN jira__stakeholder_engagement_insights s ON i.assignee_user_id = s.stakeholder_id
WHERE s.engagement_impact_score >= 3 AND s.cross_functional_projects >= 3
GROUP BY i.project_name, i.issue_type
ORDER BY n_issues DESC
LIMIT 30
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-064/attempt-01/sql/S39.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-064/attempt-01/sql/S39.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-064/attempt-01/results/S39.rows.jsonl)；完整：True；SHA256：`890cb428ca4ade8e597fe8460e3f5ef589c63b9798d87a9005bfe84c0f6a3ac0`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "i", "kind": "base", "block": null, "base_tables": ["jira__issue_enhanced"]}, {"alias": "s", "kind": "base", "block": null, "base_tables": ["jira__stakeholder_engagement_insights"]}] | [{"type": "INNER", "right": "jira__stakeholder_engagement_insights AS s", "on": "i.assignee_user_id = s.stakeholder_id", "using": []}] | ["i.project_name", "i.issue_type"] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |
| B1 | AVG(i.open_duration_seconds / 86400.0) | [{"table": "jira__issue_enhanced", "column": "open_duration_seconds"}] | [] | False |
| B1 | AVG(CASE WHEN NOT i.resolved_at IS NULL THEN (JULIANDAY(i.resolved_at) - JULIANDAY(i.created_at)) END) | [{"table": "jira__issue_enhanced", "column": "resolved_at"}, {"table": "jira__issue_enhanced", "column": "created_at"}] | [{"table": "jira__issue_enhanced", "column": "resolved_at"}] | False |


## S40

类别 `data`；来源 `query_db`；调用 `d9e2c9d9d5dd40a7a07c5ddb5d7b7e09`；状态 `success`。

```sql
-- Check project categories
SELECT project_category_id, COUNT(*) n FROM jira__project_enhanced GROUP BY project_category_id ORDER BY n DESC
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-064/attempt-01/sql/S40.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-064/attempt-01/sql/S40.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-064/attempt-01/results/S40.rows.jsonl)；完整：True；SHA256：`a55fca6bb0de74dfd7bd780845043f12f01c3dc5abdac1b6ca071816033289cb`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "jira__project_enhanced", "kind": "base", "block": null, "base_tables": ["jira__project_enhanced"]}] | [] | ["project_category_id"] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |


## S41

类别 `data`；来源 `query_db`；调用 `bf1a65e685344da9999cc655a2095f2b`；状态 `success`。

```sql
-- Project category distribution for target stakeholders' issues
SELECT 
  p.project_category_id,
  COUNT(*) AS n_issues,
  COUNT(DISTINCT i.assignee_user_id) AS n_stakeholders,
  ROUND(AVG(CASE WHEN i.resolved_at IS NOT NULL THEN (julianday(i.resolved_at)-julianday(i.created_at)) END),2) AS avg_close_days,
  ROUND(AVG(i.open_duration_seconds/86400.0),1) AS avg_open_days,
  ROUND(AVG(i.work_ratio),3) AS avg_work_ratio
FROM jira__issue_enhanced i
JOIN jira__stakeholder_engagement_insights s ON i.assignee_user_id = s.stakeholder_id
JOIN jira__project_enhanced p ON i.project_id = p.project_id
WHERE s.engagement_impact_score >= 3 AND s.cross_functional_projects >= 3
GROUP BY p.project_category_id
ORDER BY n_issues DESC
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-064/attempt-01/sql/S41.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-064/attempt-01/sql/S41.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-064/attempt-01/results/S41.rows.jsonl)；完整：True；SHA256：`dacc3bef1dca3caa5257963fc367584cc731e5110a830b13e5137238adcf618a`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "i", "kind": "base", "block": null, "base_tables": ["jira__issue_enhanced"]}, {"alias": "s", "kind": "base", "block": null, "base_tables": ["jira__stakeholder_engagement_insights"]}, {"alias": "p", "kind": "base", "block": null, "base_tables": ["jira__project_enhanced"]}] | [{"type": "INNER", "right": "jira__stakeholder_engagement_insights AS s", "on": "i.assignee_user_id = s.stakeholder_id", "using": []}, {"type": "INNER", "right": "jira__project_enhanced AS p", "on": "i.project_id = p.project_id", "using": []}] | ["p.project_category_id"] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |
| B1 | COUNT(DISTINCT i.assignee_user_id) | [{"table": "jira__issue_enhanced", "column": "assignee_user_id"}] | [] | False |
| B1 | AVG(CASE WHEN NOT i.resolved_at IS NULL THEN (JULIANDAY(i.resolved_at) - JULIANDAY(i.created_at)) END) | [{"table": "jira__issue_enhanced", "column": "resolved_at"}, {"table": "jira__issue_enhanced", "column": "created_at"}] | [{"table": "jira__issue_enhanced", "column": "resolved_at"}] | False |
| B1 | AVG(i.open_duration_seconds / 86400.0) | [{"table": "jira__issue_enhanced", "column": "open_duration_seconds"}] | [] | False |
| B1 | AVG(i.work_ratio) | [{"table": "jira__issue_enhanced", "column": "work_ratio"}] | [] | False |


## S42

类别 `data`；来源 `query_db`；调用 `3fb3aefe4077458d95bff40be668643d`；状态 `success`。

```sql
-- Issue type distribution for target stakeholders
SELECT 
  i.issue_type,
  COUNT(*) AS n_issues,
  ROUND(AVG(CASE WHEN i.resolved_at IS NOT NULL THEN (julianday(i.resolved_at)-julianday(i.created_at)) END),2) AS avg_close_days,
  ROUND(AVG(i.work_ratio),3) AS avg_work_ratio
FROM jira__issue_enhanced i
JOIN jira__stakeholder_engagement_insights s ON i.assignee_user_id = s.stakeholder_id
WHERE s.engagement_impact_score >= 3 AND s.cross_functional_projects >= 3
GROUP BY i.issue_type
ORDER BY n_issues DESC
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-064/attempt-01/sql/S42.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-064/attempt-01/sql/S42.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-064/attempt-01/results/S42.rows.jsonl)；完整：True；SHA256：`d9d403cdd42f31aa2ee80ba6240668e0b11d5e17dd4361f12589629ded3cda3e`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "i", "kind": "base", "block": null, "base_tables": ["jira__issue_enhanced"]}, {"alias": "s", "kind": "base", "block": null, "base_tables": ["jira__stakeholder_engagement_insights"]}] | [{"type": "INNER", "right": "jira__stakeholder_engagement_insights AS s", "on": "i.assignee_user_id = s.stakeholder_id", "using": []}] | ["i.issue_type"] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |
| B1 | AVG(CASE WHEN NOT i.resolved_at IS NULL THEN (JULIANDAY(i.resolved_at) - JULIANDAY(i.created_at)) END) | [{"table": "jira__issue_enhanced", "column": "resolved_at"}, {"table": "jira__issue_enhanced", "column": "created_at"}] | [{"table": "jira__issue_enhanced", "column": "resolved_at"}] | False |
| B1 | AVG(i.work_ratio) | [{"table": "jira__issue_enhanced", "column": "work_ratio"}] | [] | False |


## S43

类别 `data`；来源 `query_db`；调用 `7d30b7ab59c34371be084582f4d07f20`；状态 `success`。

```sql
-- Per-target-stakeholder issue-level performance metrics
SELECT 
  s.stakeholder_id,
  COUNT(i.issue_id) AS n_issues_handled,
  SUM(CASE WHEN i.resolved_at IS NOT NULL THEN 1 ELSE 0 END) AS n_resolved,
  ROUND(AVG(CASE WHEN i.resolved_at IS NOT NULL THEN (julianday(i.resolved_at)-julianday(i.created_at)) END),2) AS avg_close_days,
  ROUND(AVG(i.work_ratio),3) AS avg_work_ratio,
  ROUND(SUM(i.time_spent_seconds)/3600.0,1) AS total_hours_spent,
  ROUND(AVG(i.open_duration_seconds/86400.0),1) AS avg_open_days,
  COUNT(DISTINCT i.project_id) AS n_projects_worked,
  COUNT(DISTINCT i.issue_type) AS n_issue_types
FROM jira__issue_enhanced i
JOIN jira__stakeholder_engagement_insights s ON i.assignee_user_id = s.stakeholder_id
WHERE s.engagement_impact_score >= 3 AND s.cross_functional_projects >= 3
GROUP BY s.stakeholder_id
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-064/attempt-01/sql/S43.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-064/attempt-01/sql/S43.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-064/attempt-01/results/S43.rows.jsonl)；完整：True；SHA256：`49e5f545efb347b900dcedfdf81eea9ac2a13ddfc608d23fd8a67d71ff7629f2`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "i", "kind": "base", "block": null, "base_tables": ["jira__issue_enhanced"]}, {"alias": "s", "kind": "base", "block": null, "base_tables": ["jira__stakeholder_engagement_insights"]}] | [{"type": "INNER", "right": "jira__stakeholder_engagement_insights AS s", "on": "i.assignee_user_id = s.stakeholder_id", "using": []}] | ["s.stakeholder_id"] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(i.issue_id) | [{"table": "jira__issue_enhanced", "column": "issue_id"}] | [] | False |
| B1 | SUM(CASE WHEN NOT i.resolved_at IS NULL THEN 1 ELSE 0 END) | [] | [{"table": "jira__issue_enhanced", "column": "resolved_at"}] | False |
| B1 | COUNT(DISTINCT i.project_id) | [{"table": "jira__issue_enhanced", "column": "project_id"}] | [] | False |
| B1 | COUNT(DISTINCT i.issue_type) | [{"table": "jira__issue_enhanced", "column": "issue_type"}] | [] | False |
| B1 | AVG(CASE WHEN NOT i.resolved_at IS NULL THEN (JULIANDAY(i.resolved_at) - JULIANDAY(i.created_at)) END) | [{"table": "jira__issue_enhanced", "column": "resolved_at"}, {"table": "jira__issue_enhanced", "column": "created_at"}] | [{"table": "jira__issue_enhanced", "column": "resolved_at"}] | False |
| B1 | AVG(i.work_ratio) | [{"table": "jira__issue_enhanced", "column": "work_ratio"}] | [] | False |
| B1 | AVG(i.open_duration_seconds / 86400.0) | [{"table": "jira__issue_enhanced", "column": "open_duration_seconds"}] | [] | False |
| B1 | SUM(i.time_spent_seconds) | [{"table": "jira__issue_enhanced", "column": "time_spent_seconds"}] | [] | False |


## S44

类别 `data`；来源 `query_db`；调用 `a16c249ad75343799036376953ba789f`；状态 `success`。

```sql
-- Per-stakeholder issue metrics for NON-target group
SELECT 
  s.stakeholder_id,
  COUNT(i.issue_id) AS n_issues_handled,
  SUM(CASE WHEN i.resolved_at IS NOT NULL THEN 1 ELSE 0 END) AS n_resolved,
  ROUND(AVG(CASE WHEN i.resolved_at IS NOT NULL THEN (julianday(i.resolved_at)-julianday(i.created_at)) END),2) AS avg_close_days,
  ROUND(AVG(i.work_ratio),3) AS avg_work_ratio,
  ROUND(SUM(i.time_spent_seconds)/3600.0,1) AS total_hours_spent,
  ROUND(AVG(i.open_duration_seconds/86400.0),1) AS avg_open_days,
  COUNT(DISTINCT i.project_id) AS n_projects_worked
FROM jira__issue_enhanced i
JOIN jira__stakeholder_engagement_insights s ON i.assignee_user_id = s.stakeholder_id
WHERE NOT (s.engagement_impact_score >= 3 AND s.cross_functional_projects >= 3)
GROUP BY s.stakeholder_id
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-064/attempt-01/sql/S44.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-064/attempt-01/sql/S44.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-064/attempt-01/results/S44.rows.jsonl)；完整：True；SHA256：`30f422cad29c20e29d445bff3805104d320445342136f3bc94035614c4cface3`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "i", "kind": "base", "block": null, "base_tables": ["jira__issue_enhanced"]}, {"alias": "s", "kind": "base", "block": null, "base_tables": ["jira__stakeholder_engagement_insights"]}] | [{"type": "INNER", "right": "jira__stakeholder_engagement_insights AS s", "on": "i.assignee_user_id = s.stakeholder_id", "using": []}] | ["s.stakeholder_id"] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(i.issue_id) | [{"table": "jira__issue_enhanced", "column": "issue_id"}] | [] | False |
| B1 | SUM(CASE WHEN NOT i.resolved_at IS NULL THEN 1 ELSE 0 END) | [] | [{"table": "jira__issue_enhanced", "column": "resolved_at"}] | False |
| B1 | COUNT(DISTINCT i.project_id) | [{"table": "jira__issue_enhanced", "column": "project_id"}] | [] | False |
| B1 | AVG(CASE WHEN NOT i.resolved_at IS NULL THEN (JULIANDAY(i.resolved_at) - JULIANDAY(i.created_at)) END) | [{"table": "jira__issue_enhanced", "column": "resolved_at"}, {"table": "jira__issue_enhanced", "column": "created_at"}] | [{"table": "jira__issue_enhanced", "column": "resolved_at"}] | False |
| B1 | AVG(i.work_ratio) | [{"table": "jira__issue_enhanced", "column": "work_ratio"}] | [] | False |
| B1 | AVG(i.open_duration_seconds / 86400.0) | [{"table": "jira__issue_enhanced", "column": "open_duration_seconds"}] | [] | False |
| B1 | SUM(i.time_spent_seconds) | [{"table": "jira__issue_enhanced", "column": "time_spent_seconds"}] | [] | False |


## S45

类别 `data`；来源 `query_db`；调用 `6ba9524ad949407b8637c3e848c86e14`；状态 `success`。

```sql
-- Full profile for NON-target group (aggregated for comparison)
SELECT 
  ROUND(AVG(engagement_depth_score),2) AS avg_depth,
  ROUND(AVG(engagement_breadth_score),2) AS avg_breadth,
  ROUND(AVG(engagement_quality_score),2) AS avg_quality,
  ROUND(AVG(issues_assigned),2) AS avg_assigned,
  ROUND(AVG(issues_reported),2) AS avg_reported,
  ROUND(AVG(total_outbound_influence),2) AS avg_out,
  ROUND(AVG(total_inbound_influence),2) AS avg_in,
  ROUND(AVG(direct_network_connections),2) AS avg_conn,
  ROUND(AVG(strategic_value_score),2) AS avg_strat,
  ROUND(AVG(total_engagement_score),2) AS avg_total
FROM jira__stakeholder_engagement_insights
WHERE NOT (engagement_impact_score >= 3 AND cross_functional_projects >= 3)
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-064/attempt-01/sql/S45.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-064/attempt-01/sql/S45.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-064/attempt-01/results/S45.rows.jsonl)；完整：True；SHA256：`1c4441411d3d5046de74ac8a3bcbae8a5814d8d460aba0da14ec97cf33552c9e`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "jira__stakeholder_engagement_insights", "kind": "base", "block": null, "base_tables": ["jira__stakeholder_engagement_insights"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | AVG(engagement_depth_score) | [{"table": "jira__stakeholder_engagement_insights", "column": "engagement_depth_score"}] | [] | False |
| B1 | AVG(engagement_breadth_score) | [{"table": "jira__stakeholder_engagement_insights", "column": "engagement_breadth_score"}] | [] | False |
| B1 | AVG(engagement_quality_score) | [{"table": "jira__stakeholder_engagement_insights", "column": "engagement_quality_score"}] | [] | False |
| B1 | AVG(issues_assigned) | [{"table": "jira__stakeholder_engagement_insights", "column": "issues_assigned"}] | [] | False |
| B1 | AVG(issues_reported) | [{"table": "jira__stakeholder_engagement_insights", "column": "issues_reported"}] | [] | False |
| B1 | AVG(total_outbound_influence) | [{"table": "jira__stakeholder_engagement_insights", "column": "total_outbound_influence"}] | [] | False |
| B1 | AVG(total_inbound_influence) | [{"table": "jira__stakeholder_engagement_insights", "column": "total_inbound_influence"}] | [] | False |
| B1 | AVG(direct_network_connections) | [{"table": "jira__stakeholder_engagement_insights", "column": "direct_network_connections"}] | [] | False |
| B1 | AVG(strategic_value_score) | [{"table": "jira__stakeholder_engagement_insights", "column": "strategic_value_score"}] | [] | False |
| B1 | AVG(total_engagement_score) | [{"table": "jira__stakeholder_engagement_insights", "column": "total_engagement_score"}] | [] | False |


## S46

类别 `data`；来源 `query_db`；调用 `222930cec704485bace1c82edeb47e8d`；状态 `success`。

```sql
-- Target stakeholders by response_pattern_type with full metrics
SELECT 
  response_pattern_type,
  COUNT(*) AS n_stakeholders,
  ROUND(AVG(engagement_depth_score),2) AS avg_depth,
  ROUND(AVG(engagement_breadth_score),2) AS avg_breadth,
  ROUND(AVG(total_outbound_influence - total_inbound_influence),2) AS avg_influence_imbalance,
  ROUND(AVG(issues_assigned*1.0/NULLIF(issues_reported,0)),2) AS avg_assign_report_ratio,
  ROUND(AVG(direct_network_connections),2) AS avg_connections,
  ROUND(AVG(strategic_value_score),2) AS avg_strategic,
  ROUND(AVG(total_engagement_score),2) AS avg_total_score,
  SUM(CASE WHEN engagement_risk_status = 'At Risk' OR engagement_risk_status = 'Disengaged' THEN 1 ELSE 0 END) AS n_at_risk
FROM jira__stakeholder_engagement_insights
WHERE engagement_impact_score >= 3 AND cross_functional_projects >= 3
GROUP BY response_pattern_type
ORDER BY n_stakeholders DESC
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-064/attempt-01/sql/S46.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-064/attempt-01/sql/S46.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-064/attempt-01/results/S46.rows.jsonl)；完整：True；SHA256：`8c68b463fee51926e4696c8b94e5f6351e2451da1399757709acbd88ce766ac7`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "jira__stakeholder_engagement_insights", "kind": "base", "block": null, "base_tables": ["jira__stakeholder_engagement_insights"]}] | [] | ["response_pattern_type"] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |
| B1 | SUM(CASE WHEN engagement_risk_status = 'At Risk' OR engagement_risk_status = 'Disengaged' THEN 1 ELSE 0 END) | [] | [{"table": "jira__stakeholder_engagement_insights", "column": "engagement_risk_status"}, {"table": "jira__stakeholder_engagement_insights", "column": "engagement_risk_status"}] | False |
| B1 | AVG(engagement_depth_score) | [{"table": "jira__stakeholder_engagement_insights", "column": "engagement_depth_score"}] | [] | False |
| B1 | AVG(engagement_breadth_score) | [{"table": "jira__stakeholder_engagement_insights", "column": "engagement_breadth_score"}] | [] | False |
| B1 | AVG(total_outbound_influence - total_inbound_influence) | [{"table": "jira__stakeholder_engagement_insights", "column": "total_outbound_influence"}, {"table": "jira__stakeholder_engagement_insights", "column": "total_inbound_influence"}] | [] | False |
| B1 | AVG(issues_assigned * 1.0 / NULLIF(issues_reported, 0)) | [{"table": "jira__stakeholder_engagement_insights", "column": "issues_assigned"}, {"table": "jira__stakeholder_engagement_insights", "column": "issues_reported"}] | [] | False |
| B1 | AVG(direct_network_connections) | [{"table": "jira__stakeholder_engagement_insights", "column": "direct_network_connections"}] | [] | False |
| B1 | AVG(strategic_value_score) | [{"table": "jira__stakeholder_engagement_insights", "column": "strategic_value_score"}] | [] | False |
| B1 | AVG(total_engagement_score) | [{"table": "jira__stakeholder_engagement_insights", "column": "total_engagement_score"}] | [] | False |


## S47

类别 `data`；来源 `query_db`；调用 `1f0c438f40164114a0c385b0b185e9d9`；状态 `success`。

```sql
-- Strategic value vs depth/breadth mismatch patterns
SELECT 
  CASE 
    WHEN strategic_value_score >= 80 AND engagement_depth_score < 20 THEN 'High Strategic, Low Depth'
    WHEN strategic_value_score >= 80 AND engagement_depth_score >= 20 THEN 'High Strategic, High Depth'
    WHEN strategic_value_score < 80 AND engagement_depth_score < 20 THEN 'Low Strategic, Low Depth'
    ELSE 'Low Strategic, High Depth'
  END AS strategic_depth_bucket,
  COUNT(*) AS n,
  ROUND(AVG(engagement_breadth_score),1) AS avg_breadth,
  ROUND(AVG(total_outbound_influence - total_inbound_influence),2) AS avg_influence_imbalance,
  ROUND(AVG(issues_assigned*1.0/NULLIF(issues_reported,0)),2) AS avg_assign_report_ratio,
  ROUND(AVG(total_engagement_score),2) AS avg_total_score
FROM jira__stakeholder_engagement_insights
WHERE engagement_impact_score >= 3 AND cross_functional_projects >= 3
GROUP BY strategic_depth_bucket
ORDER BY n DESC
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-064/attempt-01/sql/S47.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-064/attempt-01/sql/S47.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-064/attempt-01/results/S47.rows.jsonl)；完整：True；SHA256：`984671a5f5ea81854da6a188fd27a5e86b878bb2361498ebaf03fbacc1a40cbc`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "jira__stakeholder_engagement_insights", "kind": "base", "block": null, "base_tables": ["jira__stakeholder_engagement_insights"]}] | [] | ["CASE WHEN strategic_value_score >= 80 AND engagement_depth_score < 20 THEN 'High Strategic, Low Depth' WHEN strategic_value_score >= 80 AND engagement_depth_score >= 20 THEN 'High Strategic, High Depth' WHEN strategic_value_score < 80 AND engagement_depth_score < 20 THEN 'Low Strategic, Low Depth' ELSE 'Low Strategic, High Depth' END"] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |
| B1 | AVG(engagement_breadth_score) | [{"table": "jira__stakeholder_engagement_insights", "column": "engagement_breadth_score"}] | [] | False |
| B1 | AVG(total_outbound_influence - total_inbound_influence) | [{"table": "jira__stakeholder_engagement_insights", "column": "total_outbound_influence"}, {"table": "jira__stakeholder_engagement_insights", "column": "total_inbound_influence"}] | [] | False |
| B1 | AVG(issues_assigned * 1.0 / NULLIF(issues_reported, 0)) | [{"table": "jira__stakeholder_engagement_insights", "column": "issues_assigned"}, {"table": "jira__stakeholder_engagement_insights", "column": "issues_reported"}] | [] | False |
| B1 | AVG(total_engagement_score) | [{"table": "jira__stakeholder_engagement_insights", "column": "total_engagement_score"}] | [] | False |


## S48

类别 `data`；来源 `python`；调用 `a2b37cb801c44bf4b86df67745a6435c`；状态 `success`。

```sql

SELECT * FROM jira__stakeholder_engagement_insights
WHERE engagement_impact_score >= 3 AND cross_functional_projects >= 3

```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-064/attempt-01/sql/S48.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-064/attempt-01/sql/S48.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-064/attempt-01/results/S48.rows.jsonl)；完整：True；SHA256：`2a01f02fc6461a17fe5717302ceeb7036fa3fab7670994fbd7217c60e7472af1`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "jira__stakeholder_engagement_insights", "kind": "base", "block": null, "base_tables": ["jira__stakeholder_engagement_insights"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |


## S49

类别 `data`；来源 `python`；调用 `dbd4bd81860a4bdb8317ec0854ead4d0`；状态 `success`。

```sql

SELECT * FROM jira__stakeholder_engagement_insights
WHERE engagement_impact_score >= 3 AND cross_functional_projects >= 3

```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-064/attempt-01/sql/S49.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-064/attempt-01/sql/S49.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-064/attempt-01/results/S49.rows.jsonl)；完整：True；SHA256：`2a01f02fc6461a17fe5717302ceeb7036fa3fab7670994fbd7217c60e7472af1`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "jira__stakeholder_engagement_insights", "kind": "base", "block": null, "base_tables": ["jira__stakeholder_engagement_insights"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |


## S50

类别 `data`；来源 `python`；调用 `514a7448f1144d4494f8b8a0aef12c78`；状态 `success`。

```sql

SELECT *, 
  CASE WHEN engagement_impact_score >= 3 AND cross_functional_projects >= 3 THEN 1 ELSE 0 END AS is_target
FROM jira__stakeholder_engagement_insights

```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-064/attempt-01/sql/S50.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-064/attempt-01/sql/S50.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-064/attempt-01/results/S50.rows.jsonl)；完整：True；SHA256：`04f8dc5b029d6f487cd264278152435c2cc4f19f5ef431564ce96342e889e297`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "jira__stakeholder_engagement_insights", "kind": "base", "block": null, "base_tables": ["jira__stakeholder_engagement_insights"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |


## S51

类别 `data`；来源 `python`；调用 `46689e37fc6746bfb1636df0ee6981a5`；状态 `success`。

```sql

SELECT 
  strftime('%Y-%m', i.resolved_at) AS month,
  (julianday(i.resolved_at)-julianday(i.created_at)) AS close_days,
  i.work_ratio,
  i.issue_type
FROM jira__issue_enhanced i
JOIN jira__stakeholder_engagement_insights s ON i.assignee_user_id = s.stakeholder_id
WHERE s.engagement_impact_score >= 3 AND s.cross_functional_projects >= 3
  AND i.resolved_at IS NOT NULL

```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-064/attempt-01/sql/S51.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-064/attempt-01/sql/S51.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-064/attempt-01/results/S51.rows.jsonl)；完整：True；SHA256：`1d85e3c11c2b59061b36c035fdf783c078528e3cef286f4a5174705d7c6b17f2`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "i", "kind": "base", "block": null, "base_tables": ["jira__issue_enhanced"]}, {"alias": "s", "kind": "base", "block": null, "base_tables": ["jira__stakeholder_engagement_insights"]}] | [{"type": "INNER", "right": "jira__stakeholder_engagement_insights AS s", "on": "i.assignee_user_id = s.stakeholder_id", "using": []}] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |


## S52

类别 `data`；来源 `python`；调用 `46689e37fc6746bfb1636df0ee6981a5`；状态 `success`。

```sql

SELECT 
  strftime('%Y-%m', i.resolved_at) AS month,
  (julianday(i.resolved_at)-julianday(i.created_at)) AS close_days,
  i.work_ratio
FROM jira__issue_enhanced i
JOIN jira__stakeholder_engagement_insights s ON i.assignee_user_id = s.stakeholder_id
WHERE NOT (s.engagement_impact_score >= 3 AND s.cross_functional_projects >= 3)
  AND i.resolved_at IS NOT NULL

```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-064/attempt-01/sql/S52.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-064/attempt-01/sql/S52.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-064/attempt-01/results/S52.rows.jsonl)；完整：True；SHA256：`5cb94926b399789297042cd8d74066127dc465e717fc74b1c493d516070e20d7`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "i", "kind": "base", "block": null, "base_tables": ["jira__issue_enhanced"]}, {"alias": "s", "kind": "base", "block": null, "base_tables": ["jira__stakeholder_engagement_insights"]}] | [{"type": "INNER", "right": "jira__stakeholder_engagement_insights AS s", "on": "i.assignee_user_id = s.stakeholder_id", "using": []}] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |


## S53

类别 `data`；来源 `python`；调用 `eb732d04e1c44b57acc4bb67014f46fd`；状态 `success`。

```sql

SELECT d.date_week, d.status, COUNT(DISTINCT d.issue_id) AS n_issues
FROM jira__daily_issue_field_history d
JOIN jira__stakeholder_engagement_insights s ON d.assignee = s.stakeholder_id
WHERE s.engagement_impact_score >= 3 AND s.cross_functional_projects >= 3
GROUP BY d.date_week, d.status
ORDER BY d.date_week

```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-064/attempt-01/sql/S53.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-064/attempt-01/sql/S53.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-064/attempt-01/results/S53.rows.jsonl)；完整：True；SHA256：`5556a0be4b2da84b9d0575476c7a06bd3ec0845c24e4078ef8f525584f8ef1b2`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "d", "kind": "base", "block": null, "base_tables": ["jira__daily_issue_field_history"]}, {"alias": "s", "kind": "base", "block": null, "base_tables": ["jira__stakeholder_engagement_insights"]}] | [{"type": "INNER", "right": "jira__stakeholder_engagement_insights AS s", "on": "d.assignee = s.stakeholder_id", "using": []}] | ["d.date_week", "d.status"] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(DISTINCT d.issue_id) | [{"table": "jira__daily_issue_field_history", "column": "issue_id"}] | [] | False |


## S54

类别 `data`；来源 `python`；调用 `eb732d04e1c44b57acc4bb67014f46fd`；状态 `success`。

```sql

SELECT * FROM jira__stakeholder_engagement_insights
WHERE engagement_impact_score >= 3 AND cross_functional_projects >= 3

```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-064/attempt-01/sql/S54.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-064/attempt-01/sql/S54.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-064/attempt-01/results/S54.rows.jsonl)；完整：True；SHA256：`2a01f02fc6461a17fe5717302ceeb7036fa3fab7670994fbd7217c60e7472af1`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "jira__stakeholder_engagement_insights", "kind": "base", "block": null, "base_tables": ["jira__stakeholder_engagement_insights"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |


## S55

类别 `data`；来源 `python`；调用 `80310753a7d94f8f8753808267cf20f1`；状态 `success`。

```sql

SELECT d.date_week, d.status, COUNT(DISTINCT d.issue_id) AS n_issues
FROM jira__daily_issue_field_history d
JOIN jira__stakeholder_engagement_insights s ON d.assignee = s.stakeholder_id
WHERE s.engagement_impact_score >= 3 AND s.cross_functional_projects >= 3
GROUP BY d.date_week, d.status
ORDER BY d.date_week

```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-064/attempt-01/sql/S55.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-064/attempt-01/sql/S55.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-064/attempt-01/results/S55.rows.jsonl)；完整：True；SHA256：`5556a0be4b2da84b9d0575476c7a06bd3ec0845c24e4078ef8f525584f8ef1b2`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "d", "kind": "base", "block": null, "base_tables": ["jira__daily_issue_field_history"]}, {"alias": "s", "kind": "base", "block": null, "base_tables": ["jira__stakeholder_engagement_insights"]}] | [{"type": "INNER", "right": "jira__stakeholder_engagement_insights AS s", "on": "d.assignee = s.stakeholder_id", "using": []}] | ["d.date_week", "d.status"] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(DISTINCT d.issue_id) | [{"table": "jira__daily_issue_field_history", "column": "issue_id"}] | [] | False |


## S56

类别 `data`；来源 `python`；调用 `80310753a7d94f8f8753808267cf20f1`；状态 `success`。

```sql

SELECT * FROM jira__stakeholder_engagement_insights
WHERE engagement_impact_score >= 3 AND cross_functional_projects >= 3

```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-064/attempt-01/sql/S56.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-064/attempt-01/sql/S56.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-064/attempt-01/results/S56.rows.jsonl)；完整：True；SHA256：`2a01f02fc6461a17fe5717302ceeb7036fa3fab7670994fbd7217c60e7472af1`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "jira__stakeholder_engagement_insights", "kind": "base", "block": null, "base_tables": ["jira__stakeholder_engagement_insights"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |


## S57

类别 `data`；来源 `python`；调用 `80310753a7d94f8f8753808267cf20f1`；状态 `success`。

```sql

SELECT p.project_category_id, 
  (julianday(i.resolved_at)-julianday(i.created_at)) AS close_days,
  i.issue_type, strftime('%Y-%m', i.resolved_at) AS month
FROM jira__issue_enhanced i
JOIN jira__stakeholder_engagement_insights s ON i.assignee_user_id = s.stakeholder_id
JOIN jira__project_enhanced p ON i.project_id = p.project_id
WHERE s.engagement_impact_score >= 3 AND s.cross_functional_projects >= 3
  AND i.resolved_at IS NOT NULL
  AND i.resolved_at < '2025-11-01'

```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-064/attempt-01/sql/S57.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-064/attempt-01/sql/S57.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-064/attempt-01/results/S57.rows.jsonl)；完整：True；SHA256：`85ad473bb39813908a046707b3bb4e18c8b2be58b54c8064e1af1c80abedeb89`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "i", "kind": "base", "block": null, "base_tables": ["jira__issue_enhanced"]}, {"alias": "s", "kind": "base", "block": null, "base_tables": ["jira__stakeholder_engagement_insights"]}, {"alias": "p", "kind": "base", "block": null, "base_tables": ["jira__project_enhanced"]}] | [{"type": "INNER", "right": "jira__stakeholder_engagement_insights AS s", "on": "i.assignee_user_id = s.stakeholder_id", "using": []}, {"type": "INNER", "right": "jira__project_enhanced AS p", "on": "i.project_id = p.project_id", "using": []}] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |


## S58

类别 `data`；来源 `python`；调用 `bb6ef7d4e7f846eb8a16bf7220325fce`；状态 `success`。

```sql

SELECT * FROM jira__stakeholder_engagement_insights
WHERE engagement_impact_score >= 3 AND cross_functional_projects >= 3

```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-064/attempt-01/sql/S58.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-064/attempt-01/sql/S58.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-064/attempt-01/results/S58.rows.jsonl)；完整：True；SHA256：`2a01f02fc6461a17fe5717302ceeb7036fa3fab7670994fbd7217c60e7472af1`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "jira__stakeholder_engagement_insights", "kind": "base", "block": null, "base_tables": ["jira__stakeholder_engagement_insights"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |


## S59

类别 `data`；来源 `python`；调用 `bb6ef7d4e7f846eb8a16bf7220325fce`；状态 `success`。

```sql

SELECT p.project_category_id, 
  (julianday(i.resolved_at)-julianday(i.created_at)) AS close_days,
  strftime('%Y-%m', i.resolved_at) AS month
FROM jira__issue_enhanced i
JOIN jira__stakeholder_engagement_insights s ON i.assignee_user_id = s.stakeholder_id
JOIN jira__project_enhanced p ON i.project_id = p.project_id
WHERE s.engagement_impact_score >= 3 AND s.cross_functional_projects >= 3
  AND i.resolved_at IS NOT NULL AND i.resolved_at < '2025-11-01'

```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-064/attempt-01/sql/S59.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-064/attempt-01/sql/S59.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-064/attempt-01/results/S59.rows.jsonl)；完整：True；SHA256：`5069d438bc246c2b8e773c29a94dbc7445af1bddbc0e27bf4594dda12efcadcd`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "i", "kind": "base", "block": null, "base_tables": ["jira__issue_enhanced"]}, {"alias": "s", "kind": "base", "block": null, "base_tables": ["jira__stakeholder_engagement_insights"]}, {"alias": "p", "kind": "base", "block": null, "base_tables": ["jira__project_enhanced"]}] | [{"type": "INNER", "right": "jira__stakeholder_engagement_insights AS s", "on": "i.assignee_user_id = s.stakeholder_id", "using": []}, {"type": "INNER", "right": "jira__project_enhanced AS p", "on": "i.project_id = p.project_id", "using": []}] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |


## S60

类别 `data`；来源 `python`；调用 `bb6ef7d4e7f846eb8a16bf7220325fce`；状态 `success`。

```sql

SELECT d.date_week, d.status, COUNT(DISTINCT d.issue_id) AS n_issues
FROM jira__daily_issue_field_history d
JOIN jira__stakeholder_engagement_insights s ON d.assignee = s.stakeholder_id
WHERE s.engagement_impact_score >= 3 AND s.cross_functional_projects >= 3
GROUP BY d.date_week, d.status ORDER BY d.date_week

```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-064/attempt-01/sql/S60.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-064/attempt-01/sql/S60.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-064/attempt-01/results/S60.rows.jsonl)；完整：True；SHA256：`5556a0be4b2da84b9d0575476c7a06bd3ec0845c24e4078ef8f525584f8ef1b2`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "d", "kind": "base", "block": null, "base_tables": ["jira__daily_issue_field_history"]}, {"alias": "s", "kind": "base", "block": null, "base_tables": ["jira__stakeholder_engagement_insights"]}] | [{"type": "INNER", "right": "jira__stakeholder_engagement_insights AS s", "on": "d.assignee = s.stakeholder_id", "using": []}] | ["d.date_week", "d.status"] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(DISTINCT d.issue_id) | [{"table": "jira__daily_issue_field_history", "column": "issue_id"}] | [] | False |


## S61

类别 `data`；来源 `python`；调用 `1df2b82f9fdf461e9f1e7b30c4384cf3`；状态 `success`。

```sql

SELECT * FROM jira__stakeholder_engagement_insights
WHERE engagement_impact_score >= 3 AND cross_functional_projects >= 3

```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-064/attempt-01/sql/S61.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-064/attempt-01/sql/S61.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-064/attempt-01/results/S61.rows.jsonl)；完整：True；SHA256：`2a01f02fc6461a17fe5717302ceeb7036fa3fab7670994fbd7217c60e7472af1`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "jira__stakeholder_engagement_insights", "kind": "base", "block": null, "base_tables": ["jira__stakeholder_engagement_insights"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |


## S62

类别 `data`；来源 `query_db`；调用 `714ac62e027f4b5992dbfcf18b15543e`；状态 `success`。

```sql
-- Response patterns and breadth distribution in target cohort
SELECT response_pattern_type,
  COUNT(*) AS n,
  SUM(CASE WHEN engagement_breadth_score >= 40 THEN 1 ELSE 0 END) AS n_breadth40,
  ROUND(100.0*SUM(CASE WHEN engagement_breadth_score >= 40 THEN 1 ELSE 0 END)/COUNT(*),1) AS pct_breadth40,
  ROUND(AVG(engagement_breadth_score),1) AS avg_breadth
FROM jira__stakeholder_engagement_insights
WHERE engagement_impact_score >= 3 AND cross_functional_projects >= 3
GROUP BY response_pattern_type
ORDER BY pct_breadth40 DESC
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-064/attempt-01/sql/S62.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-064/attempt-01/sql/S62.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-064/attempt-01/results/S62.rows.jsonl)；完整：True；SHA256：`576bcb12d2cd1d4a10f3d398727a91576e7179cb18df772156bea3ece90d4c02`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "jira__stakeholder_engagement_insights", "kind": "base", "block": null, "base_tables": ["jira__stakeholder_engagement_insights"]}] | [] | ["response_pattern_type"] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |
| B1 | SUM(CASE WHEN engagement_breadth_score >= 40 THEN 1 ELSE 0 END) | [] | [{"table": "jira__stakeholder_engagement_insights", "column": "engagement_breadth_score"}] | False |
| B1 | AVG(engagement_breadth_score) | [{"table": "jira__stakeholder_engagement_insights", "column": "engagement_breadth_score"}] | [] | False |
| B1 | COUNT(*) | [] | [] | True |
| B1 | SUM(CASE WHEN engagement_breadth_score >= 40 THEN 1 ELSE 0 END) | [] | [{"table": "jira__stakeholder_engagement_insights", "column": "engagement_breadth_score"}] | False |


## S63

类别 `data`；来源 `query_db`；调用 `21350dfc1af9449a97dad147caacdd6c`；状态 `success`。

```sql
-- Recommended strategies for target cohort
SELECT recommended_engagement_strategy, COUNT(*) n,
  ROUND(AVG(engagement_depth_score),2) avg_depth,
  ROUND(AVG(engagement_breadth_score),2) avg_breadth
FROM jira__stakeholder_engagement_insights
WHERE engagement_impact_score >= 3 AND cross_functional_projects >= 3
GROUP BY recommended_engagement_strategy
ORDER BY n DESC
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-064/attempt-01/sql/S63.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-064/attempt-01/sql/S63.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-064/attempt-01/results/S63.rows.jsonl)；完整：True；SHA256：`1da127b0596adb6fd6b095c48f842f69e07cfa6f6a0d5d875be051adcd05bb2d`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "jira__stakeholder_engagement_insights", "kind": "base", "block": null, "base_tables": ["jira__stakeholder_engagement_insights"]}] | [] | ["recommended_engagement_strategy"] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |
| B1 | AVG(engagement_depth_score) | [{"table": "jira__stakeholder_engagement_insights", "column": "engagement_depth_score"}] | [] | False |
| B1 | AVG(engagement_breadth_score) | [{"table": "jira__stakeholder_engagement_insights", "column": "engagement_breadth_score"}] | [] | False |


## S64

类别 `data`；来源 `query_db`；调用 `9ed35cb81fb5464da6dd3f384b5760de`；状态 `success`。

```sql
-- Development opportunities distribution for target cohort
SELECT development_opportunity, COUNT(*) n
FROM jira__stakeholder_engagement_insights
WHERE engagement_impact_score >= 3 AND cross_functional_projects >= 3
GROUP BY development_opportunity
ORDER BY n DESC
LIMIT 20
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-064/attempt-01/sql/S64.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-064/attempt-01/sql/S64.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-064/attempt-01/results/S64.rows.jsonl)；完整：True；SHA256：`1148c270aba5fb1736a6b4349e6435592c2794ebb63da7cbfa4b749cdfe72349`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "jira__stakeholder_engagement_insights", "kind": "base", "block": null, "base_tables": ["jira__stakeholder_engagement_insights"]}] | [] | ["development_opportunity"] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |


## S65

类别 `data`；来源 `query_db`；调用 `e9b7d90f8b1744e9922c43557360f608`；状态 `success`。

```sql
-- At-risk high-impact stakeholders: development opportunities
SELECT development_opportunity, COUNT(*) AS n
FROM jira__stakeholder_engagement_insights
WHERE engagement_impact_score = 5 AND engagement_risk_status IN ('At Risk','Disengaged')
  AND cross_functional_projects >= 3
GROUP BY development_opportunity
ORDER BY n DESC
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-064/attempt-01/sql/S65.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-064/attempt-01/sql/S65.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-064/attempt-01/results/S65.rows.jsonl)；完整：True；SHA256：`84bba38187ea2eafdfc87b7208806b2823a4f58ba69158b25d791fe2226e27e3`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "jira__stakeholder_engagement_insights", "kind": "base", "block": null, "base_tables": ["jira__stakeholder_engagement_insights"]}] | [] | ["development_opportunity"] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |


## S66

类别 `data`；来源 `query_db`；调用 `6dce605810cf4f0dbd5d670f906e0e34`；状态 `success`。

```sql
-- At-risk high-impact stakeholders: recommended strategies
SELECT recommended_engagement_strategy, COUNT(*) AS n
FROM jira__stakeholder_engagement_insights
WHERE engagement_impact_score = 5 AND engagement_risk_status IN ('At Risk','Disengaged')
  AND cross_functional_projects >= 3
GROUP BY recommended_engagement_strategy
ORDER BY n DESC
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-064/attempt-01/sql/S66.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-064/attempt-01/sql/S66.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-064/attempt-01/results/S66.rows.jsonl)；完整：True；SHA256：`30f2cc3d56f9939c5cefb5a2feeac225c1426808249c4c18ca7d9f511508cf54`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "jira__stakeholder_engagement_insights", "kind": "base", "block": null, "base_tables": ["jira__stakeholder_engagement_insights"]}] | [] | ["recommended_engagement_strategy"] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |


## S67

类别 `data`；来源 `query_db`；调用 `492e6aa01db14b7a8a985c163dc89f2c`；状态 `success`。

```sql
-- Avg close time from user_enhanced for target stakeholders (by joining on stakeholder_id = user_id)
SELECT 
  CASE WHEN s.engagement_impact_score >= 3 AND s.cross_functional_projects >= 3 THEN 'Target' ELSE 'Other' END AS group_type,
  COUNT(DISTINCT u.user_id) AS n_users,
  ROUND(AVG(u.avg_close_time_days),2) AS avg_close_time_days,
  ROUND(AVG(u.median_close_time_days),2) AS median_close_time_days,
  ROUND(AVG(u.avg_age_currently_open_days),1) AS avg_open_age_days
FROM jira__user_enhanced u
JOIN jira__stakeholder_engagement_insights s ON u.user_id = s.stakeholder_id
GROUP BY group_type
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-064/attempt-01/sql/S67.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-064/attempt-01/sql/S67.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-064/attempt-01/results/S67.rows.jsonl)；完整：True；SHA256：`1d03515f0cb3c14e33d5e992cf5ca907c48d02de235e29a170b961e59b91cd57`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "u", "kind": "base", "block": null, "base_tables": ["jira__user_enhanced"]}, {"alias": "s", "kind": "base", "block": null, "base_tables": ["jira__stakeholder_engagement_insights"]}] | [{"type": "INNER", "right": "jira__stakeholder_engagement_insights AS s", "on": "u.user_id = s.stakeholder_id", "using": []}] | ["CASE WHEN s.engagement_impact_score >= 3 AND s.cross_functional_projects >= 3 THEN 'Target' ELSE 'Other' END"] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(DISTINCT u.user_id) | [{"table": "jira__user_enhanced", "column": "user_id"}] | [] | False |
| B1 | AVG(u.avg_close_time_days) | [{"table": "jira__user_enhanced", "column": "avg_close_time_days"}] | [] | False |
| B1 | AVG(u.median_close_time_days) | [{"table": "jira__user_enhanced", "column": "median_close_time_days"}] | [] | False |
| B1 | AVG(u.avg_age_currently_open_days) | [{"table": "jira__user_enhanced", "column": "avg_age_currently_open_days"}] | [] | False |

