# dacomp-053

We've observed a peculiar phenomenon in our company's project management: some seemingly h…

运行：已提交。官方未评分。全部 SQL 尝试/成功 50/50；数据 SQL 48/48；Python 5 次。

完整原题：

We've observed a peculiar phenomenon in our company's project management: some seemingly healthy projects (overall_health_score > 80) end up with unsatisfactory ROI, while other projects with lower health scores generate significant business value. Based on the `asana__project_analytics` table, please conduct an in-depth analysis of this "health-value inversion" phenomenon.

Requirements:
1.  Calculate the average `roi_efficiency_ratio`, average `completion_percentage`, and the proportion of projects that exceed their `planned_duration_days` by more than 20% for each health grade (A/B/C/D/F).
2.  Independently explore key factor dimensions influencing this inversion (e.g., team size, project complexity, management priority, collaboration efficiency). Identify which combinations of project characteristics tend to produce abnormal situations like "High Health, Low Value" (HHLV) or "Low Health, High Value" (LHHV).
3.  Based on your data insights, propose recommendations for optimizing the project evaluation system.

| 表 | 行数 | 列数 |
| --- | --- | --- |
| asana__project_analytics | 500 | 45 |


实际路线（分析者依据 SQL/源码概括，不代表 Agent 自述）：SQL 计算健康等级、ROI 与延期特征 → Python 按倒挂组再次汇总、条件计数并绘图 → 评价体系建议。

数据库大小：262,144 字节。

## 数据 SQL

| SQL | 状态 | 基础表 | Join 输入/类型 | GROUP BY | 聚合表达式 | 结果行数 | 数据库 ms |
| --- | --- | --- | --- | --- | --- | --- | --- |
| [S3/Q1](#s3) | success | ["asana__project_analytics"] | 0 / {} | [] | ["COUNT(*)"] | 1 | 0.491 |
| [S4/Q2](#s4) | success | ["asana__project_analytics"] | 0 / {} | [] | [] | 5 | 0.435 |
| [S5/Q3](#s5) | success | ["asana__project_analytics"] | 0 / {} | [] | ["MIN(overall_health_score)", "MAX(overall_health_score)", "AVG(overall_health_score)"] | 1 | 0.394 |
| [S6/Q4](#s6) | success | ["asana__project_analytics"] | 0 / {} | [] | ["MIN(roi_efficiency_ratio)", "MAX(roi_efficiency_ratio)", "AVG(roi_efficiency_ratio)"] | 1 | 0.479 |
| [S7/Q5](#s7) | success | ["asana__project_analytics"] | 0 / {} | ["health_grade"] | ["COUNT(*)", "AVG(roi_efficiency_ratio)", "AVG(completion_percentage)", "COUNT(*)", "SUM(CASE WHEN elapsed_days > planned_duration_days * 1.2 THEN 1 ELSE 0 END)"] | 5 | 0.831 |
| [S8/Q6](#s8) | success | ["asana__project_analytics"] | 0 / {} | ["health_grade"] | ["COUNT(*)", "AVG(overall_health_score)", "AVG(roi_efficiency_ratio)", "AVG(completion_percentage)"] | 5 | 0.724 |
| [S9/Q7](#s9) | success | ["asana__project_analytics"] | 0 / {} | [] | ["COUNT(*)"] | 1 | 0.54 |
| [S10/Q8](#s10) | success | ["asana__project_analytics"] | 0 / {} | [] | ["COUNT(*)"] | 1 | 0.455 |
| [S11/Q9](#s11) | success | ["asana__project_analytics"] | 0 / {} | [] | ["COUNT(*)"] | 1 | 0.504 |
| [S12/Q10](#s12) | success | ["asana__project_analytics"] | 0 / {} | ["health_grade"] | ["AVG(team_size_category)", "AVG(complexity_factor)", "AVG(collaboration_score)", "AVG(management_priority)"] | 5 | 0.871 |
| [S13/Q11](#s13) | success | ["asana__project_analytics"] | 0 / {} | [] | [] | 3 | 0.545 |
| [S14/Q12](#s14) | success | ["asana__project_analytics"] | 0 / {} | [] | [] | 3 | 0.506 |
| [S15/Q13](#s15) | success | ["asana__project_analytics"] | 0 / {} | [] | [] | 3 | 0.53 |
| [S16/Q14](#s16) | success | ["asana__project_analytics"] | 0 / {} | [] | [] | 4 | 0.584 |
| [S17/Q15](#s17) | success | ["asana__project_analytics"] | 0 / {} | [] | [] | 3 | 0.498 |
| [S18/Q16](#s18) | success | ["asana__project_analytics"] | 0 / {} | [] | [] | 2 | 0.536 |
| [S19/Q17](#s19) | success | ["asana__project_analytics"] | 0 / {} | ["health_grade"] | ["COUNT(*)", "AVG(roi_efficiency_ratio)", "MIN(roi_efficiency_ratio)", "MAX(roi_efficiency_ratio)", "AVG(overall_health_score)", "AVG(comprehensive_project_score)", "AVG(efficiency_score)", "AVG(collaboration_score)", "AVG(time_management_score)"] | 5 | 0.902 |
| [S20/Q18](#s20) | success | ["asana__project_analytics"] | 0 / {} | ["CASE WHEN overall_health_score > 80 AND roi_efficiency_ratio < 0.3 THEN 'HHLV' WHEN overall_health_score <= 60 AND roi_efficiency_ratio > 0.5 THEN 'LHHV' ELSE 'Other' END"] | ["COUNT(*)"] | 1 | 0.666 |
| [S21/Q19](#s21) | success | ["asana__project_analytics"] | 0 / {} | ["health_grade"] | ["MIN(overall_health_score)", "MAX(overall_health_score)", "AVG(overall_health_score)"] | 5 | 0.678 |
| [S22/Q20](#s22) | success | ["asana__project_analytics"] | 0 / {} | ["health_grade"] | ["SUM(CASE WHEN roi_efficiency_ratio >= 0.5 THEN 1 ELSE 0 END)", "SUM(CASE WHEN roi_efficiency_ratio >= 0.8 THEN 1 ELSE 0 END)", "SUM(CASE WHEN roi_efficiency_ratio >= 1.0 THEN 1 ELSE 0 END)"] | 5 | 0.749 |
| [S23/Q21](#s23) | success | ["asana__project_analytics"] | 0 / {} | [] | [] | 30 | 0.597 |
| [S24/Q22](#s24) | success | ["asana__project_analytics"] | 0 / {} | ["health_grade"] | ["AVG(roi_efficiency_ratio)", "AVG(completion_percentage)", "COUNT(*)", "SUM(CASE WHEN elapsed_days > planned_duration_days * 1.2 THEN 1 ELSE 0 END)"] | 5 | 0.802 |
| [S25/Q23](#s25) | success | ["asana__project_analytics"] | 0 / {} | [] | [] | 5 | 0.62 |
| [S26/Q24](#s26) | success | ["asana__project_analytics"] | 0 / {} | [] | [] | 6 | 0.598 |
| [S27/Q25](#s27) | success | ["asana__project_analytics"] | 0 / {} | ["schedule_forecast", "health_grade"] | ["COUNT(*)", "AVG(roi_efficiency_ratio)"] | 15 | 0.83 |
| [S28/Q26](#s28) | success | ["asana__project_analytics"] | 0 / {} | [] | ["SUM(CASE WHEN roi_efficiency_ratio < 0.1 THEN 1 ELSE 0 END)", "SUM(CASE WHEN roi_efficiency_ratio < 0.3 THEN 1 ELSE 0 END)", "SUM(CASE WHEN roi_efficiency_ratio < 0.5 THEN 1 ELSE 0 END)", "SUM(CASE WHEN roi_efficiency_ratio > 0.8 THEN 1 ELSE 0 END)", "SUM(CASE WHEN roi_efficiency_ratio > 1.0 THEN 1 ELSE 0 END)"] | 1 | 0.721 |
| [S29/Q27](#s29) | success | ["asana__project_analytics"] | 0 / {} | ["health_grade"] | ["AVG(roi_efficiency_ratio)", "AVG(completion_percentage)", "AVG(complexity_factor)", "AVG(collaboration_score)", "AVG(efficiency_score)", "AVG(time_management_score)"] | 5 | 0.612 |
| [S30/Q28](#s30) | success | ["asana__project_analytics"] | 0 / {} | ["CASE WHEN overall_health_score > 75 AND roi_efficiency_ratio < 0.5 THEN 'HHLV' WHEN overall_health_score <= 64 AND roi_efficiency_ratio > 0.5 THEN 'LHHV' ELSE 'Normal' END"] | ["COUNT(*)"] | 3 | 0.635 |
| [S31/Q29](#s31) | success | ["asana__project_analytics"] | 0 / {} | ["CASE WHEN overall_health_score > 75 AND roi_efficiency_ratio < 0.5 THEN 'HHLV' WHEN overall_health_score <= 64 AND roi_efficiency_ratio > 0.3 THEN 'LHHV' ELSE 'Normal' END"] | ["COUNT(*)"] | 3 | 0.645 |
| [S32/Q30](#s32) | success | ["asana__project_analytics"] | 0 / {} | ["CASE WHEN health_grade IN ('A', 'B') AND roi_efficiency_ratio < 0.5 THEN 'HHLV' WHEN health_grade IN ('A', 'B') AND roi_efficiency_ratio >= 0.5 THEN 'HH_HV' WHEN health_grade IN ('D', 'F') AND roi_efficiency_ratio > 0.5 THEN 'LHHV' WHEN health_grade IN ('D', 'F') AND roi_efficiency_ratio < 0.1 THEN 'LH_LV' ELSE 'Other' END"] | ["COUNT(*)"] | 5 | 0.916 |
| [S33/Q31](#s33) | success | ["asana__project_analytics"] | 0 / {} | ["CASE WHEN health_grade IN ('A', 'B') AND roi_efficiency_ratio < 0.5 THEN 'HHLV' WHEN health_grade IN ('A', 'B') AND roi_efficiency_ratio >= 0.5 THEN 'HH_HV' WHEN health_grade IN ('D', 'F') AND roi_efficiency_ratio > 0.3 THEN 'LHHV' WHEN health_grade IN ('D', 'F') AND roi_efficiency_ratio < 0.1 THEN 'LH_LV' ELSE 'Other' END"] | ["COUNT(*)"] | 5 | 0.776 |
| [S34/Q32](#s34) | success | ["asana__project_analytics"] | 0 / {} | ["grp"] | ["COUNT(*)", "AVG(overall_health_score)", "AVG(roi_efficiency_ratio)", "AVG(completion_percentage)", "AVG(efficiency_score)", "AVG(time_management_score)", "AVG(collaboration_score)", "AVG(complexity_factor)", "AVG(elapsed_days * 1.0 / planned_duration_days)", "COUNT(*)", "COUNT(*)", "COUNT(*)", "COUNT(*)", "SUM(CASE WHEN schedule_forecast = 'ahead_of_schedule' THEN 1 ELSE 0 END)", "SUM(CASE WHEN schedule_forecast = 'behind_schedule' THEN 1 ELSE 0 END)", "SUM(CASE WHEN management_priority = 'low' THEN 1 ELSE 0 END)", "SUM(CASE WHEN risk_level = 'minimal_risk' THEN 1 ELSE 0 END)"] | 5 | 1.648 |
| [S35/Q33](#s35) | success | ["asana__project_analytics"] | 0 / {} | ["grp"] | ["COUNT(*)", "COUNT(*)", "COUNT(*)", "COUNT(*)", "COUNT(*)", "COUNT(*)", "COUNT(*)", "COUNT(*)", "COUNT(*)", "COUNT(*)", "COUNT(*)", "COUNT(*)", "COUNT(*)", "COUNT(*)", "COUNT(*)", "SUM(CASE WHEN team_size_category = 'small_team' THEN 1 ELSE 0 END)", "SUM(CASE WHEN team_size_category = 'medium_team' THEN 1 ELSE 0 END)", "SUM(CASE WHEN team_size_category = 'large_team' THEN 1 ELSE 0 END)", "SUM(CASE WHEN project_size_category = 'small' THEN 1 ELSE 0 END)", "SUM(CASE WHEN project_size_category = 'medium' THEN 1 ELSE 0 END)", "SUM(CASE WHEN project_size_category = 'large' THEN 1 ELSE 0 END)", "SUM(CASE WHEN management_priority = 'high' THEN 1 ELSE 0 END)", "SUM(CASE WHEN management_priority = 'medium' THEN 1 ELSE 0 END)", "SUM(CASE WHEN management_priority = 'low' THEN 1 ELSE 0 END)", "SUM(CASE WHEN project_maturity_phase = 'execution' THEN 1 ELSE 0 END)", "SUM(CASE WHEN risk_level = 'minimal_risk' THEN 1 ELSE 0 END)", "SUM(CASE WHEN risk_level = 'low_risk' THEN 1 ELSE 0 END)", "SUM(CASE WHEN risk_level = 'medium_risk' THEN 1 ELSE 0 END)", "SUM(CASE WHEN risk_level = 'high_risk' THEN 1 ELSE 0 END)"] | 5 | 1.663 |
| [S36/Q34](#s36) | success | ["asana__project_analytics"] | 0 / {} | [] | ["AVG(completion_percentage)", "AVG(quality_percentage)", "AVG(risk_percentage)", "AVG(efficiency_score)", "AVG(time_management_score)", "AVG(collaboration_score)", "AVG(completion_percentage)", "AVG(quality_percentage)", "AVG(risk_percentage)", "AVG(efficiency_score)", "AVG(time_management_score)", "AVG(collaboration_score)", "AVG(completion_percentage)", "AVG(quality_percentage)", "AVG(risk_percentage)", "AVG(efficiency_score)", "AVG(time_management_score)", "AVG(collaboration_score)", "AVG(completion_percentage)", "AVG(quality_percentage)", "AVG(risk_percentage)", "AVG(efficiency_score)", "AVG(time_management_score)", "AVG(collaboration_score)", "AVG(completion_percentage)", "AVG(quality_percentage)", "AVG(risk_percentage)", "AVG(efficiency_score)", "AVG(time_management_score)", "AVG(collaboration_score)"] | 5 | 1.022 |
| [S37/Q35](#s37) | success | ["asana__project_analytics"] | 0 / {} | ["schedule_forecast"] | ["AVG(roi_efficiency_ratio)", "AVG(overall_health_score)", "AVG(completion_percentage)", "AVG(efficiency_score)", "AVG(time_management_score)", "AVG(collaboration_score)", "AVG(complexity_factor)", "AVG(elapsed_days * 1.0 / planned_duration_days)"] | 3 | 1.512 |
| [S38/Q36](#s38) | success | ["asana__project_analytics"] | 0 / {} | [] | [] | 500 | 1.626 |
| [S39/Q37](#s39) | success | ["asana__project_analytics"] | 0 / {} | [] | [] | 500 | 5.156 |
| [S40/Q38](#s40) | success | ["asana__project_analytics"] | 0 / {} | [] | [] | 500 | 5.103 |
| [S41/Q39](#s41) | success | ["asana__project_analytics"] | 0 / {} | ["inv_group", "team_size_category"] | ["COUNT(*)"] | 12 | 1.106 |
| [S42/Q40](#s42) | success | ["asana__project_analytics"] | 0 / {} | ["inv_group", "management_priority"] | ["COUNT(*)"] | 5 | 1.017 |
| [S43/Q41](#s43) | success | ["asana__project_analytics"] | 0 / {} | ["management_priority", "health_grade"] | ["COUNT(*)", "AVG(roi_efficiency_ratio)"] | 9 | 0.737 |
| [S44/Q42](#s44) | success | ["asana__project_analytics"] | 0 / {} | ["management_priority"] | ["COUNT(*)", "AVG(overall_health_score)", "AVG(roi_efficiency_ratio)", "AVG(completion_percentage)", "AVG(elapsed_days * 1.0 / planned_duration_days)", "AVG(complexity_factor)", "AVG(time_management_score)"] | 3 | 0.874 |
| [S45/Q43](#s45) | success | ["asana__project_analytics"] | 0 / {} | ["team_size_category"] | ["COUNT(*)", "AVG(overall_health_score)", "AVG(roi_efficiency_ratio)", "AVG(completion_percentage)", "AVG(efficiency_score)", "AVG(time_management_score)", "AVG(collaboration_score)", "AVG(complexity_factor)", "AVG(elapsed_days * 1.0 / planned_duration_days)", "COUNT(*)", "SUM(CASE WHEN schedule_forecast = 'behind_schedule' THEN 1 ELSE 0 END)"] | 3 | 1.063 |
| [S46/Q44](#s46) | success | ["asana__project_analytics"] | 0 / {} | ["project_size_category"] | ["COUNT(*)", "AVG(overall_health_score)", "AVG(roi_efficiency_ratio)", "AVG(completion_percentage)", "AVG(efficiency_score)", "AVG(time_management_score)", "AVG(complexity_factor)", "AVG(elapsed_days * 1.0 / planned_duration_days)"] | 3 | 0.915 |
| [S47/Q45](#s47) | success | ["asana__project_analytics"] | 0 / {} | [] | [] | 11 | 0.636 |
| [S48/Q46](#s48) | success | ["asana__project_analytics"] | 0 / {} | [] | [] | 5 | 0.589 |
| [S49/Q47](#s49) | success | ["asana__project_analytics"] | 0 / {} | [] | ["AVG(completion_percentage)", "AVG(quality_percentage)", "AVG(risk_percentage)", "AVG(efficiency_score)", "AVG(time_management_score)", "AVG(collaboration_score)", "AVG(completion_percentage)", "AVG(quality_percentage)", "AVG(risk_percentage)", "AVG(efficiency_score)", "AVG(time_management_score)", "AVG(collaboration_score)", "AVG(completion_percentage)", "AVG(quality_percentage)", "AVG(risk_percentage)", "AVG(efficiency_score)", "AVG(time_management_score)", "AVG(collaboration_score)", "AVG(completion_percentage)", "AVG(quality_percentage)", "AVG(risk_percentage)", "AVG(efficiency_score)", "AVG(time_management_score)", "AVG(collaboration_score)", "AVG(completion_percentage)", "AVG(quality_percentage)", "AVG(risk_percentage)", "AVG(efficiency_score)", "AVG(time_management_score)", "AVG(collaboration_score)"] | 5 | 0.905 |
| [S50/Q48](#s50) | success | ["asana__project_analytics"] | 0 / {} | [] | [] | 500 | 4.86 |


## 元数据和设置

| SQL | 类别 | 状态 | 内容 |
| --- | --- | --- | --- |
| S1 | connection_setup | success | PRAGMA query_only=ON |
| S2 | metadata | success | SELECT name,sql FROM sqlite_master WHERE type='table' ORDER BY name |


## Python 与执行位置

人工源码审查：**database_first_violation**。Python 为健康度与价值倒挂的组别计算指标均值、进度类别占比及条件比例，并排序。这些数据准备可以在 SQL 内完成，绘图用途不消除执行位置偏离。 [证据](../reviews/dacomp-053.json)。

P1：SQLite has no built-in Pearson correlation function; computing correlations between ROI/health and their constituent factors requires Python statistics. Also creating diagnostic visualizations of the inversion phenomenon.

[源码](../../../runs/dsv4flash-db-first-full-01/dacomp-053/attempt-01/python/P1.py)；[输出](../../../runs/dsv4flash-db-first-full-01/dacomp-053/attempt-01/python/P1.stdout)；[错误](../../../runs/dsv4flash-db-first-full-01/dacomp-053/attempt-01/python/P1.stderr)。检出需人工核验的 SQL 可实现操作：.query(；不能仅凭理由判为合规。

P2：Creating visualizations to illustrate the health-value inversion phenomenon: scatter plots, group comparisons, and factor heatmaps.

[源码](../../../runs/dsv4flash-db-first-full-01/dacomp-053/attempt-01/python/P2.py)；[输出](../../../runs/dsv4flash-db-first-full-01/dacomp-053/attempt-01/python/P2.stdout)；[错误](../../../runs/dsv4flash-db-first-full-01/dacomp-053/attempt-01/python/P2.stderr)。检出需人工核验的 SQL 可实现操作：groupby(, .query(；不能仅凭理由判为合规。

P3：Checking current working directory and creating the work directory for saving figures.

[源码](../../../runs/dsv4flash-db-first-full-01/dacomp-053/attempt-01/python/P3.py)；[输出](../../../runs/dsv4flash-db-first-full-01/dacomp-053/attempt-01/python/P3.stdout)；[错误](../../../runs/dsv4flash-db-first-full-01/dacomp-053/attempt-01/python/P3.stderr)。自动源码筛查未检出预设迁出信号；这不是全面语义合规证明。

P4：Creating visualizations (scatter, bar comparisons, correlation heatmap) and group profiles in Python for the inversion analysis.

[源码](../../../runs/dsv4flash-db-first-full-01/dacomp-053/attempt-01/python/P4.py)；[输出](../../../runs/dsv4flash-db-first-full-01/dacomp-053/attempt-01/python/P4.stdout)；[错误](../../../runs/dsv4flash-db-first-full-01/dacomp-053/attempt-01/python/P4.stderr)。检出需人工核验的 SQL 可实现操作：groupby(, .query(；不能仅凭理由判为合规。

P5：Creating the final summary figure and running non-parametric significance tests (Mann-Whitney U) between inversion groups - statistical hypothesis testing is not supported by SQLite and must be done in Python.

[源码](../../../runs/dsv4flash-db-first-full-01/dacomp-053/attempt-01/python/P5.py)；[输出](../../../runs/dsv4flash-db-first-full-01/dacomp-053/attempt-01/python/P5.stdout)；[错误](../../../runs/dsv4flash-db-first-full-01/dacomp-053/attempt-01/python/P5.stderr)。检出需人工核验的 SQL 可实现操作：groupby(, .query(, sort_values(；不能仅凭理由判为合规。

## 优化机会

已验证候选。筛选限于精确 SQL、相同自包含 CTE、相同单表完整过滤、可分解单表聚合；未覆盖任意 Join 等价和一般谓词蕴含。全部候选都是 offline，未测在线预测。

| 候选 | 类型 | 已有结果 | 覆盖 SQL | 后续次数 | 中间行数 | 验证 | 成本 |
| --- | --- | --- | --- | --- | --- | --- | --- |
| C1 | exact-result reuse | True | ["S36", "S49"] | 1 | unknown | not_verified_cap | Not tested |
| C2 | exact-result reuse | True | ["S39", "S40", "S50"] | 2 | 500 | verified | Not benchmarked; correctness alone does not establish net speedup. |
| C3 | common subexpression | False | ["S34", "S35"] | 1 | 500 | verified | Not benchmarked; correctness alone does not establish net speedup. |
| C4 | aggregate MV | False | ["S3", "S7", "S8", "S12", "S19", "S20", "S21", "S22", "S24", "S27", "S28", "S30", "S31", "S32", "S33", "S37", "S43", "S44", "S45", "S46"] | 19 | 132 | verified | Not benchmarked; correctness alone does not establish net speedup. |


已验证覆盖（含触发查询、候选并集去重）：25/48 条成功数据 SQL。正确性仅针对当前数据库快照；未测性能的候选不能声称已加速。

[完整 build/rewrite 与比较证据](dacomp-053.analysis.json)。

### C4：aggregate MV

Union of grouping keys; decomposable aggregate states; AVG uses SUM and non-NULL COUNT.

原查询 [S3](#s3), [S7](#s7), [S8](#s8), [S12](#s12), [S19](#s19), [S20](#s20), [S21](#s21), [S22](#s22), [S24](#s24), [S27](#s27), [S28](#s28), [S30](#s30), [S31](#s31), [S32](#s32), [S33](#s33), [S37](#s37), [S43](#s43), [S44](#s44), [S45](#s45), [S46](#s46) → 新增共享状态 C4 → 后续 19 次可复用。该构建点为事后假设，不代表 Agent 当时预知后续。

构建定义：

```sql
SELECT health_grade AS __g0, CASE WHEN overall_health_score > 80 AND roi_efficiency_ratio < 0.3 THEN 'HHLV' WHEN overall_health_score <= 60 AND roi_efficiency_ratio > 0.5 THEN 'LHHV' ELSE 'Other' END AS __g1, schedule_forecast AS __g2, CASE WHEN overall_health_score > 75 AND roi_efficiency_ratio < 0.5 THEN 'HHLV' WHEN overall_health_score <= 64 AND roi_efficiency_ratio > 0.5 THEN 'LHHV' ELSE 'Normal' END AS __g3, CASE WHEN overall_health_score > 75 AND roi_efficiency_ratio < 0.5 THEN 'HHLV' WHEN overall_health_score <= 64 AND roi_efficiency_ratio > 0.3 THEN 'LHHV' ELSE 'Normal' END AS __g4, CASE WHEN health_grade IN ('A', 'B') AND roi_efficiency_ratio < 0.5 THEN 'HHLV' WHEN health_grade IN ('A', 'B') AND roi_efficiency_ratio >= 0.5 THEN 'HH_HV' WHEN health_grade IN ('D', 'F') AND roi_efficiency_ratio > 0.5 THEN 'LHHV' WHEN health_grade IN ('D', 'F') AND roi_efficiency_ratio < 0.1 THEN 'LH_LV' ELSE 'Other' END AS __g5, CASE WHEN health_grade IN ('A', 'B') AND roi_efficiency_ratio < 0.5 THEN 'HHLV' WHEN health_grade IN ('A', 'B') AND roi_efficiency_ratio >= 0.5 THEN 'HH_HV' WHEN health_grade IN ('D', 'F') AND roi_efficiency_ratio > 0.3 THEN 'LHHV' WHEN health_grade IN ('D', 'F') AND roi_efficiency_ratio < 0.1 THEN 'LH_LV' ELSE 'Other' END AS __g6, management_priority AS __g7, team_size_category AS __g8, project_size_category AS __g9, COUNT(*) AS __a0, SUM(roi_efficiency_ratio) AS __a1_sum, COUNT(roi_efficiency_ratio) AS __a1_n, SUM(completion_percentage) AS __a2_sum, COUNT(completion_percentage) AS __a2_n, SUM(CASE WHEN elapsed_days > planned_duration_days * 1.2 THEN 1 ELSE 0 END) AS __a3, SUM(overall_health_score) AS __a4_sum, COUNT(overall_health_score) AS __a4_n, SUM(team_size_category) AS __a5_sum, COUNT(team_size_category) AS __a5_n, SUM(complexity_factor) AS __a6_sum, COUNT(complexity_factor) AS __a6_n, SUM(collaboration_score) AS __a7_sum, COUNT(collaboration_score) AS __a7_n, SUM(management_priority) AS __a8_sum, COUNT(management_priority) AS __a8_n, MIN(roi_efficiency_ratio) AS __a9, MAX(roi_efficiency_ratio) AS __a10, SUM(comprehensive_project_score) AS __a11_sum, COUNT(comprehensive_project_score) AS __a11_n, SUM(efficiency_score) AS __a12_sum, COUNT(efficiency_score) AS __a12_n, SUM(time_management_score) AS __a13_sum, COUNT(time_management_score) AS __a13_n, MIN(overall_health_score) AS __a14, MAX(overall_health_score) AS __a15, SUM(CASE WHEN roi_efficiency_ratio >= 0.5 THEN 1 ELSE 0 END) AS __a16, SUM(CASE WHEN roi_efficiency_ratio >= 0.8 THEN 1 ELSE 0 END) AS __a17, SUM(CASE WHEN roi_efficiency_ratio >= 1.0 THEN 1 ELSE 0 END) AS __a18, SUM(CASE WHEN roi_efficiency_ratio < 0.1 THEN 1 ELSE 0 END) AS __a19, SUM(CASE WHEN roi_efficiency_ratio < 0.3 THEN 1 ELSE 0 END) AS __a20, SUM(CASE WHEN roi_efficiency_ratio < 0.5 THEN 1 ELSE 0 END) AS __a21, SUM(CASE WHEN roi_efficiency_ratio > 0.8 THEN 1 ELSE 0 END) AS __a22, SUM(CASE WHEN roi_efficiency_ratio > 1.0 THEN 1 ELSE 0 END) AS __a23, SUM(elapsed_days * 1.0 / planned_duration_days) AS __a24_sum, COUNT(elapsed_days * 1.0 / planned_duration_days) AS __a24_n, SUM(CASE WHEN schedule_forecast = 'behind_schedule' THEN 1 ELSE 0 END) AS __a25 FROM "asana__project_analytics"  GROUP BY health_grade, CASE WHEN overall_health_score > 80 AND roi_efficiency_ratio < 0.3 THEN 'HHLV' WHEN overall_health_score <= 60 AND roi_efficiency_ratio > 0.5 THEN 'LHHV' ELSE 'Other' END, schedule_forecast, CASE WHEN overall_health_score > 75 AND roi_efficiency_ratio < 0.5 THEN 'HHLV' WHEN overall_health_score <= 64 AND roi_efficiency_ratio > 0.5 THEN 'LHHV' ELSE 'Normal' END, CASE WHEN overall_health_score > 75 AND roi_efficiency_ratio < 0.5 THEN 'HHLV' WHEN overall_health_score <= 64 AND roi_efficiency_ratio > 0.3 THEN 'LHHV' ELSE 'Normal' END, CASE WHEN health_grade IN ('A', 'B') AND roi_efficiency_ratio < 0.5 THEN 'HHLV' WHEN health_grade IN ('A', 'B') AND roi_efficiency_ratio >= 0.5 THEN 'HH_HV' WHEN health_grade IN ('D', 'F') AND roi_efficiency_ratio > 0.5 THEN 'LHHV' WHEN health_grade IN ('D', 'F') AND roi_efficiency_ratio < 0.1 THEN 'LH_LV' ELSE 'Other' END, CASE WHEN health_grade IN ('A', 'B') AND roi_efficiency_ratio < 0.5 THEN 'HHLV' WHEN health_grade IN ('A', 'B') AND roi_efficiency_ratio >= 0.5 THEN 'HH_HV' WHEN health_grade IN ('D', 'F') AND roi_efficiency_ratio > 0.3 THEN 'LHHV' WHEN health_grade IN ('D', 'F') AND roi_efficiency_ratio < 0.1 THEN 'LH_LV' ELSE 'Other' END, management_priority, team_size_category, project_size_category
```

受益查询 S3 的改写示例：

```sql
SELECT SUM(__a0) AS total_rows FROM temp.reuse_candidate
```

| 原 SQL | 列名一致 | 结果一致 | 比较方法 |
| --- | --- | --- | --- |
| S3 | True | True | exact_multiset |
| S7 | True | True | ordered_numeric_tolerance |
| S8 | True | True | ordered_numeric_tolerance |
| S12 | True | True | ordered_numeric_tolerance |
| S19 | True | True | ordered_numeric_tolerance |
| S20 | True | True | exact_multiset |
| S21 | True | True | ordered_numeric_tolerance |
| S22 | True | True | ordered_numeric_tolerance |
| S24 | True | True | ordered_numeric_tolerance |
| S27 | True | True | ordered_numeric_tolerance |
| S28 | True | True | exact_multiset |
| S30 | True | True | exact_multiset |
| S31 | True | True | exact_multiset |
| S32 | True | True | exact_multiset |
| S33 | True | True | exact_multiset |
| S37 | True | True | ordered_numeric_tolerance |
| S43 | True | True | ordered_numeric_tolerance |
| S44 | True | True | ordered_numeric_tolerance |
| S45 | True | True | ordered_numeric_tolerance |
| S46 | True | True | ordered_numeric_tolerance |


验证状态：verified；成本结论：Not benchmarked; correctness alone does not establish net speedup.

### C2：exact-result reuse

Identical normalized SQL and parameters; archive equality checked.

原查询 [S39](#s39), [S40](#s40), [S50](#s50) → 保留前序结果 S39 → 后续 2 次可复用。该构建点为事后假设，不代表 Agent 当时预知后续。

| 原 SQL | 列名一致 | 结果一致 | 比较方法 |
| --- | --- | --- | --- |
| S40 | True | True | exact_multiset |
| S50 | True | True | exact_multiset |


验证状态：verified；成本结论：Not benchmarked; correctness alone does not establish net speedup.

### C3：common subexpression

Identical self-contained CTE body across queries.

原查询 [S34](#s34), [S35](#s35) → 新增共享状态 C3 → 后续 1 次可复用。该构建点为事后假设，不代表 Agent 当时预知后续。

构建定义：

```sql
SELECT *, CASE WHEN health_grade IN ('A', 'B') AND roi_efficiency_ratio < 0.5 THEN 'HHLV' WHEN health_grade IN ('A', 'B') AND roi_efficiency_ratio >= 0.5 THEN 'HH_HV' WHEN health_grade IN ('D', 'F') AND roi_efficiency_ratio > 0.3 THEN 'LHHV' WHEN health_grade IN ('D', 'F') AND roi_efficiency_ratio < 0.1 THEN 'LH_LV' ELSE 'Other' END AS grp FROM asana__project_analytics
```

受益查询 S34 的改写示例：

```sql
WITH grp AS (SELECT * FROM temp.reuse_candidate) SELECT grp, COUNT(*) AS n, ROUND(AVG(overall_health_score), 1) AS avg_health, ROUND(AVG(roi_efficiency_ratio), 4) AS avg_roi, ROUND(AVG(completion_percentage), 1) AS avg_comp, ROUND(AVG(efficiency_score), 1) AS avg_eff, ROUND(AVG(time_management_score), 1) AS avg_time, ROUND(AVG(collaboration_score), 1) AS avg_collab, ROUND(AVG(complexity_factor), 2) AS avg_complexity, ROUND(AVG(elapsed_days * 1.0 / planned_duration_days), 2) AS avg_elapsed_ratio, ROUND(100.0 * SUM(CASE WHEN schedule_forecast = 'ahead_of_schedule' THEN 1 ELSE 0 END) / COUNT(*), 1) AS pct_ahead, ROUND(100.0 * SUM(CASE WHEN schedule_forecast = 'behind_schedule' THEN 1 ELSE 0 END) / COUNT(*), 1) AS pct_behind, ROUND(100.0 * SUM(CASE WHEN management_priority = 'low' THEN 1 ELSE 0 END) / COUNT(*), 1) AS pct_low_priority, ROUND(100.0 * SUM(CASE WHEN risk_level = 'minimal_risk' THEN 1 ELSE 0 END) / COUNT(*), 1) AS pct_minimal_risk FROM grp GROUP BY grp ORDER BY grp
```

| 原 SQL | 列名一致 | 结果一致 | 比较方法 |
| --- | --- | --- | --- |
| S34 | True | True | ordered_numeric_tolerance |
| S35 | True | True | ordered_numeric_tolerance |


验证状态：verified；成本结论：Not benchmarked; correctness alone does not establish net speedup.

结果依赖：自动记录 SQL→Python 的接口父调用，以及源码中引用归档文件的消费者；字面值相同不认定因果。模型方向选择需要人工读取消息，尚未做全面因果标注。

[原始报告](../../../runs/dsv4flash-db-first-full-01/dacomp-053/attempt-01/answer.md)；[统一消息](../../../runs/dsv4flash-db-first-full-01/dacomp-053/attempt-01/messages.jsonl)；[原始 OpenCode 事件](../../../runs/dsv4flash-db-first-full-01/dacomp-053/attempt-01/opencode.jsonl)；[SQL 引擎日志](../../../runs/dsv4flash-db-first-full-01/dacomp-053/attempt-01/sql_journal.jsonl)。

[可读报告（本地图片链接规范化）](../answers/dacomp-053.md)。原始回答保留，分析结论未改写。

## S1

类别 `connection_setup`；来源 `connection`；调用 `32bdbf1e16bc4464a7b5694e7669f3fd`；状态 `success`。

```sql
PRAGMA query_only=ON
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-053/attempt-01/sql/S1.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-053/attempt-01/sql/S1.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-053/attempt-01/results/S1.rows.jsonl)；完整：True；SHA256：`e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`。

## S2

类别 `metadata`；来源 `list_db`；调用 `32bdbf1e16bc4464a7b5694e7669f3fd`；状态 `success`。

```sql
SELECT name,sql FROM sqlite_master WHERE type='table' ORDER BY name
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-053/attempt-01/sql/S2.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-053/attempt-01/sql/S2.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-053/attempt-01/results/S2.rows.jsonl)；完整：True；SHA256：`a6cc8281f8fc441b2dcddf665a7f7743fd6a56d6130e5b0febcfa0f51baf2917`。

## S3

类别 `data`；来源 `query_db`；调用 `a80ff04f9d2c4d3b92bdb21cec4b68be`；状态 `success`。

```sql
SELECT COUNT(*) as total_rows FROM asana__project_analytics
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-053/attempt-01/sql/S3.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-053/attempt-01/sql/S3.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-053/attempt-01/results/S3.rows.jsonl)；完整：True；SHA256：`b698036da49b1445965981015dfc2182edc1fd3d70d70852bff41b56f1ade4e5`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "asana__project_analytics", "kind": "base", "block": null, "base_tables": ["asana__project_analytics"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |


## S4

类别 `data`；来源 `query_db`；调用 `e073fa2b462b43d58370c4bc488a1069`；状态 `success`。

```sql
SELECT DISTINCT health_grade FROM asana__project_analytics ORDER BY health_grade
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-053/attempt-01/sql/S4.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-053/attempt-01/sql/S4.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-053/attempt-01/results/S4.rows.jsonl)；完整：True；SHA256：`b3d8346a87c313bb15faa3ac0b25076ee3b39388397c3986803749b797d752f4`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "asana__project_analytics", "kind": "base", "block": null, "base_tables": ["asana__project_analytics"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |


## S5

类别 `data`；来源 `query_db`；调用 `16c9deb2e459478681b299fba9e9a4c1`；状态 `success`。

```sql
SELECT MIN(overall_health_score), MAX(overall_health_score), AVG(overall_health_score) FROM asana__project_analytics
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-053/attempt-01/sql/S5.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-053/attempt-01/sql/S5.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-053/attempt-01/results/S5.rows.jsonl)；完整：True；SHA256：`16c019275c9570ef872a6b3c757d3ee354b8792ec3f0dc4c7a0d7b39d8a7e733`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "asana__project_analytics", "kind": "base", "block": null, "base_tables": ["asana__project_analytics"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | MIN(overall_health_score) | [{"table": "asana__project_analytics", "column": "overall_health_score"}] | [] | False |
| B1 | MAX(overall_health_score) | [{"table": "asana__project_analytics", "column": "overall_health_score"}] | [] | False |
| B1 | AVG(overall_health_score) | [{"table": "asana__project_analytics", "column": "overall_health_score"}] | [] | False |


## S6

类别 `data`；来源 `query_db`；调用 `395a5d3284d348d59ac64e37e493d4ed`；状态 `success`。

```sql
SELECT MIN(roi_efficiency_ratio), MAX(roi_efficiency_ratio), AVG(roi_efficiency_ratio) FROM asana__project_analytics
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-053/attempt-01/sql/S6.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-053/attempt-01/sql/S6.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-053/attempt-01/results/S6.rows.jsonl)；完整：True；SHA256：`10c0b70cee1cd75fd14450ca7d9d5d0f8f5bf9f091278bf96efa68bd2a3f461b`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "asana__project_analytics", "kind": "base", "block": null, "base_tables": ["asana__project_analytics"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | MIN(roi_efficiency_ratio) | [{"table": "asana__project_analytics", "column": "roi_efficiency_ratio"}] | [] | False |
| B1 | MAX(roi_efficiency_ratio) | [{"table": "asana__project_analytics", "column": "roi_efficiency_ratio"}] | [] | False |
| B1 | AVG(roi_efficiency_ratio) | [{"table": "asana__project_analytics", "column": "roi_efficiency_ratio"}] | [] | False |


## S7

类别 `data`；来源 `query_db`；调用 `38e3842e571546eba700cc9d6fd98643`；状态 `success`。

```sql
SELECT health_grade,
       COUNT(*) AS n_projects,
       ROUND(AVG(roi_efficiency_ratio),4) AS avg_roi,
       ROUND(AVG(completion_percentage),2) AS avg_completion,
       ROUND(100.0*SUM(CASE WHEN elapsed_days > planned_duration_days*1.2 THEN 1 ELSE 0 END)/COUNT(*),2) AS pct_exceed_duration_20pct
FROM asana__project_analytics
GROUP BY health_grade
ORDER BY health_grade
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-053/attempt-01/sql/S7.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-053/attempt-01/sql/S7.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-053/attempt-01/results/S7.rows.jsonl)；完整：True；SHA256：`fafcae020e0191b66d3549192d654c09c35d06781cc6c6fb8e7630edca110908`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "asana__project_analytics", "kind": "base", "block": null, "base_tables": ["asana__project_analytics"]}] | [] | ["health_grade"] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |
| B1 | AVG(roi_efficiency_ratio) | [{"table": "asana__project_analytics", "column": "roi_efficiency_ratio"}] | [] | False |
| B1 | AVG(completion_percentage) | [{"table": "asana__project_analytics", "column": "completion_percentage"}] | [] | False |
| B1 | COUNT(*) | [] | [] | True |
| B1 | SUM(CASE WHEN elapsed_days > planned_duration_days * 1.2 THEN 1 ELSE 0 END) | [] | [{"table": "asana__project_analytics", "column": "elapsed_days"}, {"table": "asana__project_analytics", "column": "planned_duration_days"}] | False |


## S8

类别 `data`；来源 `query_db`；调用 `db735cde06cb43c78b202f8cd2d023e3`；状态 `success`。

```sql
SELECT health_grade, COUNT(*) n, 
       ROUND(AVG(overall_health_score),1) avg_health,
       ROUND(AVG(roi_efficiency_ratio),4) avg_roi,
       ROUND(AVG(completion_percentage),1) avg_comp
FROM asana__project_analytics
GROUP BY health_grade ORDER BY health_grade
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-053/attempt-01/sql/S8.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-053/attempt-01/sql/S8.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-053/attempt-01/results/S8.rows.jsonl)；完整：True；SHA256：`e941a8eb723f843ff72a6de28bb5d7c6bd261e6c3313fa290036a6e34e033c96`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "asana__project_analytics", "kind": "base", "block": null, "base_tables": ["asana__project_analytics"]}] | [] | ["health_grade"] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |
| B1 | AVG(overall_health_score) | [{"table": "asana__project_analytics", "column": "overall_health_score"}] | [] | False |
| B1 | AVG(roi_efficiency_ratio) | [{"table": "asana__project_analytics", "column": "roi_efficiency_ratio"}] | [] | False |
| B1 | AVG(completion_percentage) | [{"table": "asana__project_analytics", "column": "completion_percentage"}] | [] | False |


## S9

类别 `data`；来源 `query_db`；调用 `176ad11a123c442cb20f201d7cd79cd6`；状态 `success`。

```sql
SELECT COUNT(*) FROM asana__project_analytics WHERE overall_health_score > 80
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-053/attempt-01/sql/S9.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-053/attempt-01/sql/S9.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-053/attempt-01/results/S9.rows.jsonl)；完整：True；SHA256：`9a3d37009d547ca8d9e5e079e7f7b08a02f7b958e2cf8d1d8d856415cc4124bc`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "asana__project_analytics", "kind": "base", "block": null, "base_tables": ["asana__project_analytics"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |


## S10

类别 `data`；来源 `query_db`；调用 `92b818aa648e4e8c8da895139f8d8760`；状态 `success`。

```sql
SELECT COUNT(*) FROM asana__project_analytics WHERE overall_health_score > 80 AND roi_efficiency_ratio < 0.5
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-053/attempt-01/sql/S10.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-053/attempt-01/sql/S10.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-053/attempt-01/results/S10.rows.jsonl)；完整：True；SHA256：`acc07b62f23f458923737c4cd4a66bd05d1e71eb4f384003baaf2dcc760d6349`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "asana__project_analytics", "kind": "base", "block": null, "base_tables": ["asana__project_analytics"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |


## S11

类别 `data`；来源 `query_db`；调用 `b611b0fd5a18455789028574a4415707`；状态 `success`。

```sql
SELECT COUNT(*) FROM asana__project_analytics WHERE overall_health_score <= 60 AND roi_efficiency_ratio > 0.5
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-053/attempt-01/sql/S11.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-053/attempt-01/sql/S11.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-053/attempt-01/results/S11.rows.jsonl)；完整：True；SHA256：`c14196f132c1e9be0508ae80ab52fcb3e1d3fc05880415f3dc980971df207c9e`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "asana__project_analytics", "kind": "base", "block": null, "base_tables": ["asana__project_analytics"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |


## S12

类别 `data`；来源 `query_db`；调用 `afecdd677a104d6daf1fca665729e5a2`；状态 `success`。

```sql
SELECT health_grade, 
       ROUND(AVG(team_size_category),2) as avg_team_size,
       ROUND(AVG(complexity_factor),4) as avg_complexity,
       ROUND(AVG(collaboration_score),2) as avg_collab,
       ROUND(AVG(management_priority),2) as avg_priority
FROM asana__project_analytics
GROUP BY health_grade ORDER BY health_grade
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-053/attempt-01/sql/S12.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-053/attempt-01/sql/S12.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-053/attempt-01/results/S12.rows.jsonl)；完整：True；SHA256：`fdaf8e1bd9192afbda39929ffba19188853427719083036f828e2d68807e3e03`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "asana__project_analytics", "kind": "base", "block": null, "base_tables": ["asana__project_analytics"]}] | [] | ["health_grade"] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | AVG(team_size_category) | [{"table": "asana__project_analytics", "column": "team_size_category"}] | [] | False |
| B1 | AVG(complexity_factor) | [{"table": "asana__project_analytics", "column": "complexity_factor"}] | [] | False |
| B1 | AVG(collaboration_score) | [{"table": "asana__project_analytics", "column": "collaboration_score"}] | [] | False |
| B1 | AVG(management_priority) | [{"table": "asana__project_analytics", "column": "management_priority"}] | [] | False |


## S13

类别 `data`；来源 `query_db`；调用 `f402e677d3fb42c2b13fcd96d1051e0a`；状态 `success`。

```sql
SELECT DISTINCT team_size_category FROM asana__project_analytics
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-053/attempt-01/sql/S13.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-053/attempt-01/sql/S13.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-053/attempt-01/results/S13.rows.jsonl)；完整：True；SHA256：`09209b1f5579dae0dceee5323065602bc6df43b30f96ab693b371aa0f1b14031`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "asana__project_analytics", "kind": "base", "block": null, "base_tables": ["asana__project_analytics"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |


## S14

类别 `data`；来源 `query_db`；调用 `58403322e5704d0b9be80fe5093373ad`；状态 `success`。

```sql
SELECT DISTINCT management_priority FROM asana__project_analytics
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-053/attempt-01/sql/S14.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-053/attempt-01/sql/S14.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-053/attempt-01/results/S14.rows.jsonl)；完整：True；SHA256：`10da2d8605ddeb73038739d55d24a22195e94289bdcf2905993eadff3a7e3418`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "asana__project_analytics", "kind": "base", "block": null, "base_tables": ["asana__project_analytics"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |


## S15

类别 `data`；来源 `query_db`；调用 `99e78545b01c496286af461f9bdbf010`；状态 `success`。

```sql
SELECT DISTINCT project_size_category FROM asana__project_analytics
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-053/attempt-01/sql/S15.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-053/attempt-01/sql/S15.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-053/attempt-01/results/S15.rows.jsonl)；完整：True；SHA256：`175170dd007ad396abda87d429d468caf983b5049010a80e4651ae83f688fef2`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "asana__project_analytics", "kind": "base", "block": null, "base_tables": ["asana__project_analytics"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |


## S16

类别 `data`；来源 `query_db`；调用 `b0b2bbdf6e994448842aa2f51fd74d3e`；状态 `success`。

```sql
SELECT DISTINCT risk_level FROM asana__project_analytics
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-053/attempt-01/sql/S16.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-053/attempt-01/sql/S16.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-053/attempt-01/results/S16.rows.jsonl)；完整：True；SHA256：`a01928622b5893a69226cd325877b241677a90ed030fd1059bb98c8b4a68f5ef`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "asana__project_analytics", "kind": "base", "block": null, "base_tables": ["asana__project_analytics"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |


## S17

类别 `data`；来源 `query_db`；调用 `c1839e2c837e4cdf9508865b3cac5d44`；状态 `success`。

```sql
SELECT DISTINCT schedule_forecast FROM asana__project_analytics
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-053/attempt-01/sql/S17.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-053/attempt-01/sql/S17.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-053/attempt-01/results/S17.rows.jsonl)；完整：True；SHA256：`c18ce3936f2664a14645c54088963d96547844424f64841ebb95e6d123415352`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "asana__project_analytics", "kind": "base", "block": null, "base_tables": ["asana__project_analytics"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |


## S18

类别 `data`；来源 `query_db`；调用 `975940b74b004f82b9447954cc039c1b`；状态 `success`。

```sql
SELECT DISTINCT project_maturity_phase FROM asana__project_analytics
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-053/attempt-01/sql/S18.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-053/attempt-01/sql/S18.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-053/attempt-01/results/S18.rows.jsonl)；完整：True；SHA256：`7b1c07643377286aaaa0d9adad33ee319ef993cbac3d54506de094276b750322`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "asana__project_analytics", "kind": "base", "block": null, "base_tables": ["asana__project_analytics"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |


## S19

类别 `data`；来源 `query_db`；调用 `21fbc14ebb0b47d18e7b4de765fb9126`；状态 `success`。

```sql
SELECT health_grade,
       COUNT(*) n,
       ROUND(AVG(roi_efficiency_ratio),4) avg_roi,
       ROUND(MIN(roi_efficiency_ratio),4) min_roi,
       ROUND(MAX(roi_efficiency_ratio),4) max_roi,
       ROUND(AVG(overall_health_score),1) avg_health,
       ROUND(AVG(comprehensive_project_score),2) avg_cps,
       ROUND(AVG(efficiency_score),1) avg_eff,
       ROUND(AVG(collaboration_score),1) avg_collab,
       ROUND(AVG(time_management_score),1) avg_time
FROM asana__project_analytics
GROUP BY health_grade ORDER BY health_grade
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-053/attempt-01/sql/S19.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-053/attempt-01/sql/S19.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-053/attempt-01/results/S19.rows.jsonl)；完整：True；SHA256：`6a0b45dc815d52c580a5c7275e8a8dbcfcc96c18ac846724386081d61a037579`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "asana__project_analytics", "kind": "base", "block": null, "base_tables": ["asana__project_analytics"]}] | [] | ["health_grade"] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |
| B1 | AVG(roi_efficiency_ratio) | [{"table": "asana__project_analytics", "column": "roi_efficiency_ratio"}] | [] | False |
| B1 | MIN(roi_efficiency_ratio) | [{"table": "asana__project_analytics", "column": "roi_efficiency_ratio"}] | [] | False |
| B1 | MAX(roi_efficiency_ratio) | [{"table": "asana__project_analytics", "column": "roi_efficiency_ratio"}] | [] | False |
| B1 | AVG(overall_health_score) | [{"table": "asana__project_analytics", "column": "overall_health_score"}] | [] | False |
| B1 | AVG(comprehensive_project_score) | [{"table": "asana__project_analytics", "column": "comprehensive_project_score"}] | [] | False |
| B1 | AVG(efficiency_score) | [{"table": "asana__project_analytics", "column": "efficiency_score"}] | [] | False |
| B1 | AVG(collaboration_score) | [{"table": "asana__project_analytics", "column": "collaboration_score"}] | [] | False |
| B1 | AVG(time_management_score) | [{"table": "asana__project_analytics", "column": "time_management_score"}] | [] | False |


## S20

类别 `data`；来源 `query_db`；调用 `4d164c4ffc9243bfb3e3a6653177c270`；状态 `success`。

```sql
SELECT 
  CASE WHEN overall_health_score > 80 AND roi_efficiency_ratio < 0.3 THEN 'HHLV'
       WHEN overall_health_score <= 60 AND roi_efficiency_ratio > 0.5 THEN 'LHHV'
       ELSE 'Other'
  END AS inversion_type,
  COUNT(*) AS n
FROM asana__project_analytics
GROUP BY inversion_type
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-053/attempt-01/sql/S20.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-053/attempt-01/sql/S20.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-053/attempt-01/results/S20.rows.jsonl)；完整：True；SHA256：`0af56612e405513d33c0ae60bb47f8da106afa0c6ac8bd0a871c315360e28791`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "asana__project_analytics", "kind": "base", "block": null, "base_tables": ["asana__project_analytics"]}] | [] | ["CASE WHEN overall_health_score > 80 AND roi_efficiency_ratio < 0.3 THEN 'HHLV' WHEN overall_health_score <= 60 AND roi_efficiency_ratio > 0.5 THEN 'LHHV' ELSE 'Other' END"] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |


## S21

类别 `data`；来源 `query_db`；调用 `738d1b2daaf24ae886640d1e475cd8f7`；状态 `success`。

```sql
SELECT health_grade,
       ROUND(MIN(overall_health_score),0) min_h, ROUND(MAX(overall_health_score),0) max_h,
       ROUND(AVG(overall_health_score),1) avg_h
FROM asana__project_analytics GROUP BY health_grade ORDER BY health_grade
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-053/attempt-01/sql/S21.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-053/attempt-01/sql/S21.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-053/attempt-01/results/S21.rows.jsonl)；完整：True；SHA256：`6a36f1207012c254481b5755b5ba4638ecb6b38010d2d076ec8c1750dac108cf`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "asana__project_analytics", "kind": "base", "block": null, "base_tables": ["asana__project_analytics"]}] | [] | ["health_grade"] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | MIN(overall_health_score) | [{"table": "asana__project_analytics", "column": "overall_health_score"}] | [] | False |
| B1 | MAX(overall_health_score) | [{"table": "asana__project_analytics", "column": "overall_health_score"}] | [] | False |
| B1 | AVG(overall_health_score) | [{"table": "asana__project_analytics", "column": "overall_health_score"}] | [] | False |


## S22

类别 `data`；来源 `query_db`；调用 `99b9a0feb5544b3f9b3249b4b82dff62`；状态 `success`。

```sql
SELECT health_grade,
       SUM(CASE WHEN roi_efficiency_ratio >= 0.5 THEN 1 ELSE 0 END) AS roi_ge_05,
       SUM(CASE WHEN roi_efficiency_ratio >= 0.8 THEN 1 ELSE 0 END) AS roi_ge_08,
       SUM(CASE WHEN roi_efficiency_ratio >= 1.0 THEN 1 ELSE 0 END) AS roi_ge_10
FROM asana__project_analytics GROUP BY health_grade ORDER BY health_grade
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-053/attempt-01/sql/S22.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-053/attempt-01/sql/S22.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-053/attempt-01/results/S22.rows.jsonl)；完整：True；SHA256：`716d1d873e6b3e63557fe199498d44f6b22d8e670c5bb4f068e23f44b154b307`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "asana__project_analytics", "kind": "base", "block": null, "base_tables": ["asana__project_analytics"]}] | [] | ["health_grade"] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | SUM(CASE WHEN roi_efficiency_ratio >= 0.5 THEN 1 ELSE 0 END) | [] | [{"table": "asana__project_analytics", "column": "roi_efficiency_ratio"}] | False |
| B1 | SUM(CASE WHEN roi_efficiency_ratio >= 0.8 THEN 1 ELSE 0 END) | [] | [{"table": "asana__project_analytics", "column": "roi_efficiency_ratio"}] | False |
| B1 | SUM(CASE WHEN roi_efficiency_ratio >= 1.0 THEN 1 ELSE 0 END) | [] | [{"table": "asana__project_analytics", "column": "roi_efficiency_ratio"}] | False |


## S23

类别 `data`；来源 `query_db`；调用 `2d7f6ceca72c412a87d3d828a9d6f34d`；状态 `success`。

```sql
SELECT project_id, overall_health_score, health_grade, roi_efficiency_ratio, completion_percentage, planned_duration_days, elapsed_days
FROM asana__project_analytics
WHERE roi_efficiency_ratio >= 0.8
ORDER BY roi_efficiency_ratio DESC
LIMIT 30
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-053/attempt-01/sql/S23.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-053/attempt-01/sql/S23.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-053/attempt-01/results/S23.rows.jsonl)；完整：True；SHA256：`55aa8d7ad94edac7c7ece7ae20dca52872e49d4bb26fc20d2ce1abdee6bec191`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "asana__project_analytics", "kind": "base", "block": null, "base_tables": ["asana__project_analytics"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |


## S24

类别 `data`；来源 `query_db`；调用 `9b1e896074ce480e92da2f112bd35a51`；状态 `success`。

```sql
SELECT health_grade,
       ROUND(AVG(roi_efficiency_ratio),4) AS avg_roi,
       ROUND(AVG(completion_percentage),2) AS avg_completion,
       ROUND(100.0*SUM(CASE WHEN elapsed_days > planned_duration_days*1.2 THEN 1 ELSE 0 END)/COUNT(*),2) AS pct_exceed_duration_20pct
FROM asana__project_analytics
GROUP BY health_grade
ORDER BY health_grade
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-053/attempt-01/sql/S24.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-053/attempt-01/sql/S24.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-053/attempt-01/results/S24.rows.jsonl)；完整：True；SHA256：`2caebabee4a1ce1f52b8df29d0faeea381cd9f7bfc4115a04859df17322579c9`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "asana__project_analytics", "kind": "base", "block": null, "base_tables": ["asana__project_analytics"]}] | [] | ["health_grade"] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | AVG(roi_efficiency_ratio) | [{"table": "asana__project_analytics", "column": "roi_efficiency_ratio"}] | [] | False |
| B1 | AVG(completion_percentage) | [{"table": "asana__project_analytics", "column": "completion_percentage"}] | [] | False |
| B1 | COUNT(*) | [] | [] | True |
| B1 | SUM(CASE WHEN elapsed_days > planned_duration_days * 1.2 THEN 1 ELSE 0 END) | [] | [{"table": "asana__project_analytics", "column": "elapsed_days"}, {"table": "asana__project_analytics", "column": "planned_duration_days"}] | False |


## S25

类别 `data`；来源 `query_db`；调用 `74ef1e97e9654610a92d73809f1d4553`；状态 `success`。

```sql
-- Find projects with abnormally high roi for their health (LHHV candidates)
SELECT project_id, overall_health_score, health_grade, roi_efficiency_ratio,
       team_size_category, project_size_category, complexity_factor,
       collaboration_score, management_priority, efficiency_score,
       schedule_forecast, risk_level, project_maturity_phase,
       completion_percentage, elapsed_days, planned_duration_days,
       time_management_score
FROM asana__project_analytics
WHERE (health_grade IN ('D','F') AND roi_efficiency_ratio > 0.5)
   OR (health_grade = 'D' AND roi_efficiency_ratio > 0.3)
ORDER BY roi_efficiency_ratio DESC
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-053/attempt-01/sql/S25.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-053/attempt-01/sql/S25.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-053/attempt-01/results/S25.rows.jsonl)；完整：True；SHA256：`1247fddf7c4333633aa27cbbfdbf3f6345194f1f7aa5c120b4b32a700cd58d75`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "asana__project_analytics", "kind": "base", "block": null, "base_tables": ["asana__project_analytics"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |


## S26

类别 `data`；来源 `query_db`；调用 `80e911687f8a46e59d2fb1253ee561ae`；状态 `success`。

```sql
-- HHLV candidates: health A/B but roi below median (0.5?)
SELECT project_id, overall_health_score, health_grade, roi_efficiency_ratio,
       team_size_category, project_size_category, complexity_factor,
       collaboration_score, management_priority, efficiency_score,
       schedule_forecast, risk_level, project_maturity_phase,
       completion_percentage, elapsed_days, planned_duration_days,
       time_management_score
FROM asana__project_analytics
WHERE health_grade IN ('A','B') AND roi_efficiency_ratio < 0.4
ORDER BY roi_efficiency_ratio ASC
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-053/attempt-01/sql/S26.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-053/attempt-01/sql/S26.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-053/attempt-01/results/S26.rows.jsonl)；完整：True；SHA256：`97a20c49c8759cc8fbf871d2fe5e17143ccf6667775649c7dd5b14c9497e568c`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "asana__project_analytics", "kind": "base", "block": null, "base_tables": ["asana__project_analytics"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |


## S27

类别 `data`；来源 `query_db`；调用 `f8045c08989947318824734c499b935c`；状态 `success`。

```sql
SELECT schedule_forecast, health_grade, COUNT(*) n, ROUND(AVG(roi_efficiency_ratio),4) avg_roi
FROM asana__project_analytics
GROUP BY schedule_forecast, health_grade
ORDER BY schedule_forecast, health_grade
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-053/attempt-01/sql/S27.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-053/attempt-01/sql/S27.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-053/attempt-01/results/S27.rows.jsonl)；完整：True；SHA256：`3ae86ba2766a872c0d2636c102919b3df8f912802bc2351f89e599f5a00011b8`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "asana__project_analytics", "kind": "base", "block": null, "base_tables": ["asana__project_analytics"]}] | [] | ["schedule_forecast", "health_grade"] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |
| B1 | AVG(roi_efficiency_ratio) | [{"table": "asana__project_analytics", "column": "roi_efficiency_ratio"}] | [] | False |


## S28

类别 `data`；来源 `query_db`；调用 `493a93190bf3413c932d0c1c882a69e7`；状态 `success`。

```sql
SELECT 
  ROUND(SUM(CASE WHEN roi_efficiency_ratio < 0.1 THEN 1 ELSE 0 END)*100.0/500,1) pct_lt_01,
  ROUND(SUM(CASE WHEN roi_efficiency_ratio < 0.3 THEN 1 ELSE 0 END)*100.0/500,1) pct_lt_03,
  ROUND(SUM(CASE WHEN roi_efficiency_ratio < 0.5 THEN 1 ELSE 0 END)*100.0/500,1) pct_lt_05,
  ROUND(SUM(CASE WHEN roi_efficiency_ratio > 0.8 THEN 1 ELSE 0 END)*100.0/500,1) pct_gt_08,
  ROUND(SUM(CASE WHEN roi_efficiency_ratio > 1.0 THEN 1 ELSE 0 END)*100.0/500,1) pct_gt_10
FROM asana__project_analytics
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-053/attempt-01/sql/S28.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-053/attempt-01/sql/S28.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-053/attempt-01/results/S28.rows.jsonl)；完整：True；SHA256：`5555c8091fa42aaa8c1919158ba5ae8308f5cbe8db64fa29cdf525d3c6d1e9d2`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "asana__project_analytics", "kind": "base", "block": null, "base_tables": ["asana__project_analytics"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | SUM(CASE WHEN roi_efficiency_ratio < 0.1 THEN 1 ELSE 0 END) | [] | [{"table": "asana__project_analytics", "column": "roi_efficiency_ratio"}] | False |
| B1 | SUM(CASE WHEN roi_efficiency_ratio < 0.3 THEN 1 ELSE 0 END) | [] | [{"table": "asana__project_analytics", "column": "roi_efficiency_ratio"}] | False |
| B1 | SUM(CASE WHEN roi_efficiency_ratio < 0.5 THEN 1 ELSE 0 END) | [] | [{"table": "asana__project_analytics", "column": "roi_efficiency_ratio"}] | False |
| B1 | SUM(CASE WHEN roi_efficiency_ratio > 0.8 THEN 1 ELSE 0 END) | [] | [{"table": "asana__project_analytics", "column": "roi_efficiency_ratio"}] | False |
| B1 | SUM(CASE WHEN roi_efficiency_ratio > 1.0 THEN 1 ELSE 0 END) | [] | [{"table": "asana__project_analytics", "column": "roi_efficiency_ratio"}] | False |


## S29

类别 `data`；来源 `query_db`；调用 `0b03884b36a84f0590446e767cc0d686`；状态 `success`。

```sql
-- Compare ahead-of-schedule projects by health grade: ROI vs key factors
SELECT health_grade, 
       ROUND(AVG(roi_efficiency_ratio),4) avg_roi,
       ROUND(AVG(completion_percentage),1) avg_comp,
       ROUND(AVG(complexity_factor),2) avg_complexity,
       ROUND(AVG(collaboration_score),1) avg_collab,
       ROUND(AVG(efficiency_score),1) avg_eff,
       ROUND(AVG(time_management_score),1) avg_time
FROM asana__project_analytics
WHERE schedule_forecast = 'ahead_of_schedule'
GROUP BY health_grade ORDER BY health_grade
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-053/attempt-01/sql/S29.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-053/attempt-01/sql/S29.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-053/attempt-01/results/S29.rows.jsonl)；完整：True；SHA256：`71e3db768eec72f7e36d91fc4c6d6631b3c2f6c55192a98ad7c3aed626880b45`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "asana__project_analytics", "kind": "base", "block": null, "base_tables": ["asana__project_analytics"]}] | [] | ["health_grade"] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | AVG(roi_efficiency_ratio) | [{"table": "asana__project_analytics", "column": "roi_efficiency_ratio"}] | [] | False |
| B1 | AVG(completion_percentage) | [{"table": "asana__project_analytics", "column": "completion_percentage"}] | [] | False |
| B1 | AVG(complexity_factor) | [{"table": "asana__project_analytics", "column": "complexity_factor"}] | [] | False |
| B1 | AVG(collaboration_score) | [{"table": "asana__project_analytics", "column": "collaboration_score"}] | [] | False |
| B1 | AVG(efficiency_score) | [{"table": "asana__project_analytics", "column": "efficiency_score"}] | [] | False |
| B1 | AVG(time_management_score) | [{"table": "asana__project_analytics", "column": "time_management_score"}] | [] | False |


## S30

类别 `data`；来源 `query_db`；调用 `53c0aec49b5a41dbb765473679e797ea`；状态 `success`。

```sql
SELECT 
  CASE WHEN overall_health_score > 75 AND roi_efficiency_ratio < 0.5 THEN 'HHLV'
       WHEN overall_health_score <= 64 AND roi_efficiency_ratio > 0.5 THEN 'LHHV'
       ELSE 'Normal'
  END AS group_label,
  COUNT(*) AS n
FROM asana__project_analytics
GROUP BY group_label
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-053/attempt-01/sql/S30.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-053/attempt-01/sql/S30.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-053/attempt-01/results/S30.rows.jsonl)；完整：True；SHA256：`e563f3ca32b896da12e43701e8ba9a2794bd15247df79ebe2a5dbf4849f197b3`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "asana__project_analytics", "kind": "base", "block": null, "base_tables": ["asana__project_analytics"]}] | [] | ["CASE WHEN overall_health_score > 75 AND roi_efficiency_ratio < 0.5 THEN 'HHLV' WHEN overall_health_score <= 64 AND roi_efficiency_ratio > 0.5 THEN 'LHHV' ELSE 'Normal' END"] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |


## S31

类别 `data`；来源 `query_db`；调用 `c406a7293c8d4db69a24817eb905156c`；状态 `success`。

```sql
SELECT 
  CASE WHEN overall_health_score > 75 AND roi_efficiency_ratio < 0.5 THEN 'HHLV'
       WHEN overall_health_score <= 64 AND roi_efficiency_ratio > 0.3 THEN 'LHHV'
       ELSE 'Normal'
  END AS group_label,
  COUNT(*) AS n
FROM asana__project_analytics
GROUP BY group_label
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-053/attempt-01/sql/S31.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-053/attempt-01/sql/S31.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-053/attempt-01/results/S31.rows.jsonl)；完整：True；SHA256：`8e453f723612cf2ff73aa37564e5c8df9c3044bfa28847000f5078f8202e9dc7`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "asana__project_analytics", "kind": "base", "block": null, "base_tables": ["asana__project_analytics"]}] | [] | ["CASE WHEN overall_health_score > 75 AND roi_efficiency_ratio < 0.5 THEN 'HHLV' WHEN overall_health_score <= 64 AND roi_efficiency_ratio > 0.3 THEN 'LHHV' ELSE 'Normal' END"] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |


## S32

类别 `data`；来源 `query_db`；调用 `7d78d7806ce94a52b21b65ba19c5cec2`；状态 `success`。

```sql
SELECT 
  CASE WHEN health_grade IN ('A','B') AND roi_efficiency_ratio < 0.5 THEN 'HHLV'
       WHEN health_grade IN ('A','B') AND roi_efficiency_ratio >= 0.5 THEN 'HH_HV'
       WHEN health_grade IN ('D','F') AND roi_efficiency_ratio > 0.5 THEN 'LHHV'
       WHEN health_grade IN ('D','F') AND roi_efficiency_ratio < 0.1 THEN 'LH_LV'
       ELSE 'Other'
  END AS grp,
  COUNT(*) n
FROM asana__project_analytics
GROUP BY grp
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-053/attempt-01/sql/S32.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-053/attempt-01/sql/S32.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-053/attempt-01/results/S32.rows.jsonl)；完整：True；SHA256：`22fbb56083e26e44cdcb4a1028582b36448f4883bfd03d87725bcd85250cedb6`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "asana__project_analytics", "kind": "base", "block": null, "base_tables": ["asana__project_analytics"]}] | [] | ["CASE WHEN health_grade IN ('A', 'B') AND roi_efficiency_ratio < 0.5 THEN 'HHLV' WHEN health_grade IN ('A', 'B') AND roi_efficiency_ratio >= 0.5 THEN 'HH_HV' WHEN health_grade IN ('D', 'F') AND roi_efficiency_ratio > 0.5 THEN 'LHHV' WHEN health_grade IN ('D', 'F') AND roi_efficiency_ratio < 0.1 THEN 'LH_LV' ELSE 'Other' END"] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |


## S33

类别 `data`；来源 `query_db`；调用 `d9fd258870bc4561980cfc418a59f4be`；状态 `success`。

```sql
SELECT 
  CASE WHEN health_grade IN ('A','B') AND roi_efficiency_ratio < 0.5 THEN 'HHLV'
       WHEN health_grade IN ('A','B') AND roi_efficiency_ratio >= 0.5 THEN 'HH_HV'
       WHEN health_grade IN ('D','F') AND roi_efficiency_ratio > 0.3 THEN 'LHHV'
       WHEN health_grade IN ('D','F') AND roi_efficiency_ratio < 0.1 THEN 'LH_LV'
       ELSE 'Other'
  END AS grp,
  COUNT(*) n
FROM asana__project_analytics
GROUP BY grp
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-053/attempt-01/sql/S33.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-053/attempt-01/sql/S33.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-053/attempt-01/results/S33.rows.jsonl)；完整：True；SHA256：`ef188e5fafd76ceefa8db7c57379daae0d4a4343496ee806624e26f87da5aec6`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "asana__project_analytics", "kind": "base", "block": null, "base_tables": ["asana__project_analytics"]}] | [] | ["CASE WHEN health_grade IN ('A', 'B') AND roi_efficiency_ratio < 0.5 THEN 'HHLV' WHEN health_grade IN ('A', 'B') AND roi_efficiency_ratio >= 0.5 THEN 'HH_HV' WHEN health_grade IN ('D', 'F') AND roi_efficiency_ratio > 0.3 THEN 'LHHV' WHEN health_grade IN ('D', 'F') AND roi_efficiency_ratio < 0.1 THEN 'LH_LV' ELSE 'Other' END"] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |


## S34

类别 `data`；来源 `query_db`；调用 `4037a4cfaa8c4c7a98bd760729a3379c`；状态 `success`。

```sql
WITH grp AS (
  SELECT *,
    CASE WHEN health_grade IN ('A','B') AND roi_efficiency_ratio < 0.5 THEN 'HHLV'
         WHEN health_grade IN ('A','B') AND roi_efficiency_ratio >= 0.5 THEN 'HH_HV'
         WHEN health_grade IN ('D','F') AND roi_efficiency_ratio > 0.3 THEN 'LHHV'
         WHEN health_grade IN ('D','F') AND roi_efficiency_ratio < 0.1 THEN 'LH_LV'
         ELSE 'Other' END AS grp
  FROM asana__project_analytics
)
SELECT grp, COUNT(*) n,
  ROUND(AVG(overall_health_score),1) avg_health,
  ROUND(AVG(roi_efficiency_ratio),4) avg_roi,
  ROUND(AVG(completion_percentage),1) avg_comp,
  ROUND(AVG(efficiency_score),1) avg_eff,
  ROUND(AVG(time_management_score),1) avg_time,
  ROUND(AVG(collaboration_score),1) avg_collab,
  ROUND(AVG(complexity_factor),2) avg_complexity,
  ROUND(AVG(elapsed_days*1.0/planned_duration_days),2) avg_elapsed_ratio,
  ROUND(100.0*SUM(CASE WHEN schedule_forecast='ahead_of_schedule' THEN 1 ELSE 0 END)/COUNT(*),1) pct_ahead,
  ROUND(100.0*SUM(CASE WHEN schedule_forecast='behind_schedule' THEN 1 ELSE 0 END)/COUNT(*),1) pct_behind,
  ROUND(100.0*SUM(CASE WHEN management_priority='low' THEN 1 ELSE 0 END)/COUNT(*),1) pct_low_priority,
  ROUND(100.0*SUM(CASE WHEN risk_level='minimal_risk' THEN 1 ELSE 0 END)/COUNT(*),1) pct_minimal_risk
FROM grp
GROUP BY grp ORDER BY grp
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-053/attempt-01/sql/S34.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-053/attempt-01/sql/S34.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-053/attempt-01/results/S34.rows.jsonl)；完整：True；SHA256：`72d0ae25a484fb781352cb48c9ad4a3cccdfdd93ed8c448e7547b237d256dded`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "asana__project_analytics", "kind": "base", "block": null, "base_tables": ["asana__project_analytics"]}] | [] | [] |
| B2 | [{"alias": "grp", "kind": "derived", "block": "B1", "base_tables": ["asana__project_analytics"]}] | [] | ["grp"] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B2 | COUNT(*) | [] | [] | True |
| B2 | AVG(overall_health_score) | [{"table": "asana__project_analytics", "column": "overall_health_score"}] | [] | False |
| B2 | AVG(roi_efficiency_ratio) | [{"table": "asana__project_analytics", "column": "roi_efficiency_ratio"}] | [] | False |
| B2 | AVG(completion_percentage) | [{"table": "asana__project_analytics", "column": "completion_percentage"}] | [] | False |
| B2 | AVG(efficiency_score) | [{"table": "asana__project_analytics", "column": "efficiency_score"}] | [] | False |
| B2 | AVG(time_management_score) | [{"table": "asana__project_analytics", "column": "time_management_score"}] | [] | False |
| B2 | AVG(collaboration_score) | [{"table": "asana__project_analytics", "column": "collaboration_score"}] | [] | False |
| B2 | AVG(complexity_factor) | [{"table": "asana__project_analytics", "column": "complexity_factor"}] | [] | False |
| B2 | AVG(elapsed_days * 1.0 / planned_duration_days) | [{"table": "asana__project_analytics", "column": "planned_duration_days"}, {"table": "asana__project_analytics", "column": "elapsed_days"}] | [] | False |
| B2 | COUNT(*) | [] | [] | True |
| B2 | COUNT(*) | [] | [] | True |
| B2 | COUNT(*) | [] | [] | True |
| B2 | COUNT(*) | [] | [] | True |
| B2 | SUM(CASE WHEN schedule_forecast = 'ahead_of_schedule' THEN 1 ELSE 0 END) | [] | [{"table": "asana__project_analytics", "column": "schedule_forecast"}] | False |
| B2 | SUM(CASE WHEN schedule_forecast = 'behind_schedule' THEN 1 ELSE 0 END) | [] | [{"table": "asana__project_analytics", "column": "schedule_forecast"}] | False |
| B2 | SUM(CASE WHEN management_priority = 'low' THEN 1 ELSE 0 END) | [] | [{"table": "asana__project_analytics", "column": "management_priority"}] | False |
| B2 | SUM(CASE WHEN risk_level = 'minimal_risk' THEN 1 ELSE 0 END) | [] | [{"table": "asana__project_analytics", "column": "risk_level"}] | False |


## S35

类别 `data`；来源 `query_db`；调用 `53a6766716614ed8ba567b2616760c2d`；状态 `success`。

```sql
WITH grp AS (
  SELECT *,
    CASE WHEN health_grade IN ('A','B') AND roi_efficiency_ratio < 0.5 THEN 'HHLV'
         WHEN health_grade IN ('A','B') AND roi_efficiency_ratio >= 0.5 THEN 'HH_HV'
         WHEN health_grade IN ('D','F') AND roi_efficiency_ratio > 0.3 THEN 'LHHV'
         WHEN health_grade IN ('D','F') AND roi_efficiency_ratio < 0.1 THEN 'LH_LV'
         ELSE 'Other' END AS grp
  FROM asana__project_analytics
)
SELECT grp, COUNT(*) n,
  ROUND(100.0*SUM(CASE WHEN team_size_category='small_team' THEN 1 ELSE 0 END)/COUNT(*),1) pct_small_team,
  ROUND(100.0*SUM(CASE WHEN team_size_category='medium_team' THEN 1 ELSE 0 END)/COUNT(*),1) pct_medium_team,
  ROUND(100.0*SUM(CASE WHEN team_size_category='large_team' THEN 1 ELSE 0 END)/COUNT(*),1) pct_large_team,
  ROUND(100.0*SUM(CASE WHEN project_size_category='small' THEN 1 ELSE 0 END)/COUNT(*),1) pct_small_proj,
  ROUND(100.0*SUM(CASE WHEN project_size_category='medium' THEN 1 ELSE 0 END)/COUNT(*),1) pct_medium_proj,
  ROUND(100.0*SUM(CASE WHEN project_size_category='large' THEN 1 ELSE 0 END)/COUNT(*),1) pct_large_proj,
  ROUND(100.0*SUM(CASE WHEN management_priority='high' THEN 1 ELSE 0 END)/COUNT(*),1) pct_high_priority,
  ROUND(100.0*SUM(CASE WHEN management_priority='medium' THEN 1 ELSE 0 END)/COUNT(*),1) pct_medium_priority,
  ROUND(100.0*SUM(CASE WHEN management_priority='low' THEN 1 ELSE 0 END)/COUNT(*),1) pct_low_priority,
  ROUND(100.0*SUM(CASE WHEN project_maturity_phase='execution' THEN 1 ELSE 0 END)/COUNT(*),1) pct_execution,
  ROUND(100.0*SUM(CASE WHEN risk_level='minimal_risk' THEN 1 ELSE 0 END)/COUNT(*),1) pct_minimal_risk,
  ROUND(100.0*SUM(CASE WHEN risk_level='low_risk' THEN 1 ELSE 0 END)/COUNT(*),1) pct_low_risk,
  ROUND(100.0*SUM(CASE WHEN risk_level='medium_risk' THEN 1 ELSE 0 END)/COUNT(*),1) pct_medium_risk,
  ROUND(100.0*SUM(CASE WHEN risk_level='high_risk' THEN 1 ELSE 0 END)/COUNT(*),1) pct_high_risk
FROM grp
GROUP BY grp ORDER BY grp
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-053/attempt-01/sql/S35.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-053/attempt-01/sql/S35.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-053/attempt-01/results/S35.rows.jsonl)；完整：True；SHA256：`fe620d82777e2d0fca91aaeb1db0c4bfa00d7f390b64a42f95f2d6a0e2638a61`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "asana__project_analytics", "kind": "base", "block": null, "base_tables": ["asana__project_analytics"]}] | [] | [] |
| B2 | [{"alias": "grp", "kind": "derived", "block": "B1", "base_tables": ["asana__project_analytics"]}] | [] | ["grp"] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B2 | COUNT(*) | [] | [] | True |
| B2 | COUNT(*) | [] | [] | True |
| B2 | COUNT(*) | [] | [] | True |
| B2 | COUNT(*) | [] | [] | True |
| B2 | COUNT(*) | [] | [] | True |
| B2 | COUNT(*) | [] | [] | True |
| B2 | COUNT(*) | [] | [] | True |
| B2 | COUNT(*) | [] | [] | True |
| B2 | COUNT(*) | [] | [] | True |
| B2 | COUNT(*) | [] | [] | True |
| B2 | COUNT(*) | [] | [] | True |
| B2 | COUNT(*) | [] | [] | True |
| B2 | COUNT(*) | [] | [] | True |
| B2 | COUNT(*) | [] | [] | True |
| B2 | COUNT(*) | [] | [] | True |
| B2 | SUM(CASE WHEN team_size_category = 'small_team' THEN 1 ELSE 0 END) | [] | [{"table": "asana__project_analytics", "column": "team_size_category"}] | False |
| B2 | SUM(CASE WHEN team_size_category = 'medium_team' THEN 1 ELSE 0 END) | [] | [{"table": "asana__project_analytics", "column": "team_size_category"}] | False |
| B2 | SUM(CASE WHEN team_size_category = 'large_team' THEN 1 ELSE 0 END) | [] | [{"table": "asana__project_analytics", "column": "team_size_category"}] | False |
| B2 | SUM(CASE WHEN project_size_category = 'small' THEN 1 ELSE 0 END) | [] | [{"table": "asana__project_analytics", "column": "project_size_category"}] | False |
| B2 | SUM(CASE WHEN project_size_category = 'medium' THEN 1 ELSE 0 END) | [] | [{"table": "asana__project_analytics", "column": "project_size_category"}] | False |
| B2 | SUM(CASE WHEN project_size_category = 'large' THEN 1 ELSE 0 END) | [] | [{"table": "asana__project_analytics", "column": "project_size_category"}] | False |
| B2 | SUM(CASE WHEN management_priority = 'high' THEN 1 ELSE 0 END) | [] | [{"table": "asana__project_analytics", "column": "management_priority"}] | False |
| B2 | SUM(CASE WHEN management_priority = 'medium' THEN 1 ELSE 0 END) | [] | [{"table": "asana__project_analytics", "column": "management_priority"}] | False |
| B2 | SUM(CASE WHEN management_priority = 'low' THEN 1 ELSE 0 END) | [] | [{"table": "asana__project_analytics", "column": "management_priority"}] | False |
| B2 | SUM(CASE WHEN project_maturity_phase = 'execution' THEN 1 ELSE 0 END) | [] | [{"table": "asana__project_analytics", "column": "project_maturity_phase"}] | False |
| B2 | SUM(CASE WHEN risk_level = 'minimal_risk' THEN 1 ELSE 0 END) | [] | [{"table": "asana__project_analytics", "column": "risk_level"}] | False |
| B2 | SUM(CASE WHEN risk_level = 'low_risk' THEN 1 ELSE 0 END) | [] | [{"table": "asana__project_analytics", "column": "risk_level"}] | False |
| B2 | SUM(CASE WHEN risk_level = 'medium_risk' THEN 1 ELSE 0 END) | [] | [{"table": "asana__project_analytics", "column": "risk_level"}] | False |
| B2 | SUM(CASE WHEN risk_level = 'high_risk' THEN 1 ELSE 0 END) | [] | [{"table": "asana__project_analytics", "column": "risk_level"}] | False |


## S36

类别 `data`；来源 `query_db`；调用 `b95991b6ac0948f980201cdba62c61de`；状态 `success`。

```sql
SELECT 
  ROUND(AVG(completion_percentage),1) avg_comp,
  ROUND(AVG(quality_percentage),1) avg_quality,
  ROUND(AVG(risk_percentage),1) avg_risk,
  ROUND(AVG(efficiency_score),1) avg_eff,
  ROUND(AVG(time_management_score),1) avg_time,
  ROUND(AVG(collaboration_score),1) avg_collab
FROM asana__project_analytics
WHERE health_grade = 'A'
UNION ALL
SELECT ROUND(AVG(completion_percentage),1), ROUND(AVG(quality_percentage),1), ROUND(AVG(risk_percentage),1), ROUND(AVG(efficiency_score),1), ROUND(AVG(time_management_score),1), ROUND(AVG(collaboration_score),1)
FROM asana__project_analytics WHERE health_grade = 'B'
UNION ALL
SELECT ROUND(AVG(completion_percentage),1), ROUND(AVG(quality_percentage),1), ROUND(AVG(risk_percentage),1), ROUND(AVG(efficiency_score),1), ROUND(AVG(time_management_score),1), ROUND(AVG(collaboration_score),1)
FROM asana__project_analytics WHERE health_grade = 'C'
UNION ALL
SELECT ROUND(AVG(completion_percentage),1), ROUND(AVG(quality_percentage),1), ROUND(AVG(risk_percentage),1), ROUND(AVG(efficiency_score),1), ROUND(AVG(time_management_score),1), ROUND(AVG(collaboration_score),1)
FROM asana__project_analytics WHERE health_grade = 'D'
UNION ALL
SELECT ROUND(AVG(completion_percentage),1), ROUND(AVG(quality_percentage),1), ROUND(AVG(risk_percentage),1), ROUND(AVG(efficiency_score),1), ROUND(AVG(time_management_score),1), ROUND(AVG(collaboration_score),1)
FROM asana__project_analytics WHERE health_grade = 'F'
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-053/attempt-01/sql/S36.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-053/attempt-01/sql/S36.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-053/attempt-01/results/S36.rows.jsonl)；完整：True；SHA256：`c5d0560dd054a46c4372b1a0bf0687805df2a282a4d1269bc76f06cec66b44e3`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "asana__project_analytics", "kind": "base", "block": null, "base_tables": ["asana__project_analytics"]}] | [] | [] |
| B2 | [{"alias": "asana__project_analytics", "kind": "base", "block": null, "base_tables": ["asana__project_analytics"]}] | [] | [] |
| B3 | [] | [] | [] |
| B4 | [{"alias": "asana__project_analytics", "kind": "base", "block": null, "base_tables": ["asana__project_analytics"]}] | [] | [] |
| B5 | [] | [] | [] |
| B6 | [{"alias": "asana__project_analytics", "kind": "base", "block": null, "base_tables": ["asana__project_analytics"]}] | [] | [] |
| B7 | [] | [] | [] |
| B8 | [{"alias": "asana__project_analytics", "kind": "base", "block": null, "base_tables": ["asana__project_analytics"]}] | [] | [] |
| B9 | [] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | AVG(completion_percentage) | [{"table": "asana__project_analytics", "column": "completion_percentage"}] | [] | False |
| B1 | AVG(quality_percentage) | [{"table": "asana__project_analytics", "column": "quality_percentage"}] | [] | False |
| B1 | AVG(risk_percentage) | [{"table": "asana__project_analytics", "column": "risk_percentage"}] | [] | False |
| B1 | AVG(efficiency_score) | [{"table": "asana__project_analytics", "column": "efficiency_score"}] | [] | False |
| B1 | AVG(time_management_score) | [{"table": "asana__project_analytics", "column": "time_management_score"}] | [] | False |
| B1 | AVG(collaboration_score) | [{"table": "asana__project_analytics", "column": "collaboration_score"}] | [] | False |
| B2 | AVG(completion_percentage) | [{"table": "asana__project_analytics", "column": "completion_percentage"}] | [] | False |
| B2 | AVG(quality_percentage) | [{"table": "asana__project_analytics", "column": "quality_percentage"}] | [] | False |
| B2 | AVG(risk_percentage) | [{"table": "asana__project_analytics", "column": "risk_percentage"}] | [] | False |
| B2 | AVG(efficiency_score) | [{"table": "asana__project_analytics", "column": "efficiency_score"}] | [] | False |
| B2 | AVG(time_management_score) | [{"table": "asana__project_analytics", "column": "time_management_score"}] | [] | False |
| B2 | AVG(collaboration_score) | [{"table": "asana__project_analytics", "column": "collaboration_score"}] | [] | False |
| B4 | AVG(completion_percentage) | [{"table": "asana__project_analytics", "column": "completion_percentage"}] | [] | False |
| B4 | AVG(quality_percentage) | [{"table": "asana__project_analytics", "column": "quality_percentage"}] | [] | False |
| B4 | AVG(risk_percentage) | [{"table": "asana__project_analytics", "column": "risk_percentage"}] | [] | False |
| B4 | AVG(efficiency_score) | [{"table": "asana__project_analytics", "column": "efficiency_score"}] | [] | False |
| B4 | AVG(time_management_score) | [{"table": "asana__project_analytics", "column": "time_management_score"}] | [] | False |
| B4 | AVG(collaboration_score) | [{"table": "asana__project_analytics", "column": "collaboration_score"}] | [] | False |
| B6 | AVG(completion_percentage) | [{"table": "asana__project_analytics", "column": "completion_percentage"}] | [] | False |
| B6 | AVG(quality_percentage) | [{"table": "asana__project_analytics", "column": "quality_percentage"}] | [] | False |
| B6 | AVG(risk_percentage) | [{"table": "asana__project_analytics", "column": "risk_percentage"}] | [] | False |
| B6 | AVG(efficiency_score) | [{"table": "asana__project_analytics", "column": "efficiency_score"}] | [] | False |
| B6 | AVG(time_management_score) | [{"table": "asana__project_analytics", "column": "time_management_score"}] | [] | False |
| B6 | AVG(collaboration_score) | [{"table": "asana__project_analytics", "column": "collaboration_score"}] | [] | False |
| B8 | AVG(completion_percentage) | [{"table": "asana__project_analytics", "column": "completion_percentage"}] | [] | False |
| B8 | AVG(quality_percentage) | [{"table": "asana__project_analytics", "column": "quality_percentage"}] | [] | False |
| B8 | AVG(risk_percentage) | [{"table": "asana__project_analytics", "column": "risk_percentage"}] | [] | False |
| B8 | AVG(efficiency_score) | [{"table": "asana__project_analytics", "column": "efficiency_score"}] | [] | False |
| B8 | AVG(time_management_score) | [{"table": "asana__project_analytics", "column": "time_management_score"}] | [] | False |
| B8 | AVG(collaboration_score) | [{"table": "asana__project_analytics", "column": "collaboration_score"}] | [] | False |


## S37

类别 `data`；来源 `query_db`；调用 `98d51145ced54805a84a49d6cf00ba7a`；状态 `success`。

```sql
SELECT 
  schedule_forecast,
  ROUND(AVG(roi_efficiency_ratio),4) avg_roi,
  ROUND(AVG(overall_health_score),1) avg_health,
  ROUND(AVG(completion_percentage),1) avg_comp,
  ROUND(AVG(efficiency_score),1) avg_eff,
  ROUND(AVG(time_management_score),1) avg_time,
  ROUND(AVG(collaboration_score),1) avg_collab,
  ROUND(AVG(complexity_factor),2) avg_complexity,
  ROUND(AVG(elapsed_days*1.0/planned_duration_days),2) avg_elapsed_ratio
FROM asana__project_analytics
GROUP BY schedule_forecast
ORDER BY avg_roi DESC
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-053/attempt-01/sql/S37.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-053/attempt-01/sql/S37.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-053/attempt-01/results/S37.rows.jsonl)；完整：True；SHA256：`12e9265736eec1a838f7bdfd3be5821173ecbae6b9d7445a7767b2eeaad66590`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "asana__project_analytics", "kind": "base", "block": null, "base_tables": ["asana__project_analytics"]}] | [] | ["schedule_forecast"] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | AVG(roi_efficiency_ratio) | [{"table": "asana__project_analytics", "column": "roi_efficiency_ratio"}] | [] | False |
| B1 | AVG(overall_health_score) | [{"table": "asana__project_analytics", "column": "overall_health_score"}] | [] | False |
| B1 | AVG(completion_percentage) | [{"table": "asana__project_analytics", "column": "completion_percentage"}] | [] | False |
| B1 | AVG(efficiency_score) | [{"table": "asana__project_analytics", "column": "efficiency_score"}] | [] | False |
| B1 | AVG(time_management_score) | [{"table": "asana__project_analytics", "column": "time_management_score"}] | [] | False |
| B1 | AVG(collaboration_score) | [{"table": "asana__project_analytics", "column": "collaboration_score"}] | [] | False |
| B1 | AVG(complexity_factor) | [{"table": "asana__project_analytics", "column": "complexity_factor"}] | [] | False |
| B1 | AVG(elapsed_days * 1.0 / planned_duration_days) | [{"table": "asana__project_analytics", "column": "planned_duration_days"}, {"table": "asana__project_analytics", "column": "elapsed_days"}] | [] | False |


## S38

类别 `data`；来源 `python`；调用 `7eacd44671b94a5abedda276d2a7e7a9`；状态 `success`。

```sql

SELECT overall_health_score, roi_efficiency_ratio, completion_percentage, quality_percentage,
       risk_percentage, efficiency_score, time_management_score, collaboration_score,
       complexity_factor, elapsed_days, planned_duration_days, unique_assignees,
       total_tasks, completion_rate_per_day
FROM asana__project_analytics

```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-053/attempt-01/sql/S38.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-053/attempt-01/sql/S38.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-053/attempt-01/results/S38.rows.jsonl)；完整：True；SHA256：`9008d2e860e307325fad05b42dc67a3fb4c284f95d1170adc5019344b3d30bc9`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "asana__project_analytics", "kind": "base", "block": null, "base_tables": ["asana__project_analytics"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |


## S39

类别 `data`；来源 `python`；调用 `4fe0ebaec48449aaafa341dba5899677`；状态 `success`。

```sql

SELECT *, 
  CASE WHEN health_grade IN ('A','B') AND roi_efficiency_ratio < 0.5 THEN 'HHLV'
       WHEN health_grade IN ('A','B') AND roi_efficiency_ratio >= 0.5 THEN 'HH_HV'
       WHEN health_grade IN ('D','F') AND roi_efficiency_ratio > 0.3 THEN 'LHHV'
       WHEN health_grade IN ('D','F') AND roi_efficiency_ratio < 0.1 THEN 'LH_LV'
       ELSE 'Other' END AS inv_group
FROM asana__project_analytics

```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-053/attempt-01/sql/S39.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-053/attempt-01/sql/S39.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-053/attempt-01/results/S39.rows.jsonl)；完整：True；SHA256：`cfa0ca6c3e28b25eb6fb56933c26ded634231016c3eba715d559cae6cf2d657a`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "asana__project_analytics", "kind": "base", "block": null, "base_tables": ["asana__project_analytics"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |


## S40

类别 `data`；来源 `python`；调用 `a367fca5eb0e4544bfca1ad8cd593c12`；状态 `success`。

```sql

SELECT *, 
  CASE WHEN health_grade IN ('A','B') AND roi_efficiency_ratio < 0.5 THEN 'HHLV'
       WHEN health_grade IN ('A','B') AND roi_efficiency_ratio >= 0.5 THEN 'HH_HV'
       WHEN health_grade IN ('D','F') AND roi_efficiency_ratio > 0.3 THEN 'LHHV'
       WHEN health_grade IN ('D','F') AND roi_efficiency_ratio < 0.1 THEN 'LH_LV'
       ELSE 'Other' END AS inv_group
FROM asana__project_analytics

```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-053/attempt-01/sql/S40.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-053/attempt-01/sql/S40.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-053/attempt-01/results/S40.rows.jsonl)；完整：True；SHA256：`cfa0ca6c3e28b25eb6fb56933c26ded634231016c3eba715d559cae6cf2d657a`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "asana__project_analytics", "kind": "base", "block": null, "base_tables": ["asana__project_analytics"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |


## S41

类别 `data`；来源 `query_db`；调用 `242fca85f97c40918b3e424350beb471`；状态 `success`。

```sql
SELECT inv_group, team_size_category, COUNT(*) n
FROM (
  SELECT *,
    CASE WHEN health_grade IN ('A','B') AND roi_efficiency_ratio < 0.5 THEN 'HHLV'
         WHEN health_grade IN ('A','B') AND roi_efficiency_ratio >= 0.5 THEN 'HH_HV'
         WHEN health_grade IN ('D','F') AND roi_efficiency_ratio > 0.3 THEN 'LHHV'
         WHEN health_grade IN ('D','F') AND roi_efficiency_ratio < 0.1 THEN 'LH_LV'
         ELSE 'Other' END AS inv_group
  FROM asana__project_analytics
)
WHERE inv_group IN ('HHLV','HH_HV','LHHV','LH_LV')
GROUP BY inv_group, team_size_category
ORDER BY inv_group, team_size_category
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-053/attempt-01/sql/S41.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-053/attempt-01/sql/S41.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-053/attempt-01/results/S41.rows.jsonl)；完整：True；SHA256：`0a9eb97f9d03516099a6fc27c42910cc73c8911ea4654d2c5913e6c42d371622`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "asana__project_analytics", "kind": "base", "block": null, "base_tables": ["asana__project_analytics"]}] | [] | [] |
| B2 | [{"alias": "", "kind": "derived", "block": "B1", "base_tables": ["asana__project_analytics"]}] | [] | ["inv_group", "team_size_category"] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B2 | COUNT(*) | [] | [] | True |


## S42

类别 `data`；来源 `query_db`；调用 `9d05bb3dcbb741b48c1cbffd107a6ad9`；状态 `success`。

```sql
SELECT inv_group, management_priority, COUNT(*) n
FROM (
  SELECT *,
    CASE WHEN health_grade IN ('A','B') AND roi_efficiency_ratio < 0.5 THEN 'HHLV'
         WHEN health_grade IN ('A','B') AND roi_efficiency_ratio >= 0.5 THEN 'HH_HV'
         WHEN health_grade IN ('D','F') AND roi_efficiency_ratio > 0.3 THEN 'LHHV'
         WHEN health_grade IN ('D','F') AND roi_efficiency_ratio < 0.1 THEN 'LH_LV'
         ELSE 'Other' END AS inv_group
  FROM asana__project_analytics
)
WHERE inv_group IN ('HHLV','HH_HV','LHHV','LH_LV')
GROUP BY inv_group, management_priority
ORDER BY inv_group, management_priority
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-053/attempt-01/sql/S42.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-053/attempt-01/sql/S42.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-053/attempt-01/results/S42.rows.jsonl)；完整：True；SHA256：`651dea5515401eba3d873efd7c834acaa812aaa44402795e201d355b3bec2eae`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "asana__project_analytics", "kind": "base", "block": null, "base_tables": ["asana__project_analytics"]}] | [] | [] |
| B2 | [{"alias": "", "kind": "derived", "block": "B1", "base_tables": ["asana__project_analytics"]}] | [] | ["inv_group", "management_priority"] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B2 | COUNT(*) | [] | [] | True |


## S43

类别 `data`；来源 `query_db`；调用 `d422d52360c8426bbee11306fe66324f`；状态 `success`。

```sql
SELECT management_priority, health_grade, COUNT(*) n, ROUND(AVG(roi_efficiency_ratio),4) avg_roi
FROM asana__project_analytics
GROUP BY management_priority, health_grade
ORDER BY management_priority, health_grade
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-053/attempt-01/sql/S43.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-053/attempt-01/sql/S43.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-053/attempt-01/results/S43.rows.jsonl)；完整：True；SHA256：`2b7d568ac3ec630569c69c271f3d24d4fc530eb882daedc59ca11723936b15f9`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "asana__project_analytics", "kind": "base", "block": null, "base_tables": ["asana__project_analytics"]}] | [] | ["management_priority", "health_grade"] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |
| B1 | AVG(roi_efficiency_ratio) | [{"table": "asana__project_analytics", "column": "roi_efficiency_ratio"}] | [] | False |


## S44

类别 `data`；来源 `query_db`；调用 `b4e5ed578d214a4093af996e8d318e6a`；状态 `success`。

```sql
SELECT management_priority, COUNT(*) n,
       ROUND(AVG(overall_health_score),1) avg_health,
       ROUND(AVG(roi_efficiency_ratio),4) avg_roi,
       ROUND(AVG(completion_percentage),1) avg_comp,
       ROUND(AVG(elapsed_days*1.0/planned_duration_days),2) avg_elapsed_ratio,
       ROUND(AVG(complexity_factor),2) avg_complexity,
       ROUND(AVG(time_management_score),1) avg_time
FROM asana__project_analytics
GROUP BY management_priority ORDER BY management_priority
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-053/attempt-01/sql/S44.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-053/attempt-01/sql/S44.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-053/attempt-01/results/S44.rows.jsonl)；完整：True；SHA256：`54104ab4f7cc0ac2464bd51d6406593bff7ed5d5b1c9a82573b7b9ebadd2e001`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "asana__project_analytics", "kind": "base", "block": null, "base_tables": ["asana__project_analytics"]}] | [] | ["management_priority"] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |
| B1 | AVG(overall_health_score) | [{"table": "asana__project_analytics", "column": "overall_health_score"}] | [] | False |
| B1 | AVG(roi_efficiency_ratio) | [{"table": "asana__project_analytics", "column": "roi_efficiency_ratio"}] | [] | False |
| B1 | AVG(completion_percentage) | [{"table": "asana__project_analytics", "column": "completion_percentage"}] | [] | False |
| B1 | AVG(elapsed_days * 1.0 / planned_duration_days) | [{"table": "asana__project_analytics", "column": "planned_duration_days"}, {"table": "asana__project_analytics", "column": "elapsed_days"}] | [] | False |
| B1 | AVG(complexity_factor) | [{"table": "asana__project_analytics", "column": "complexity_factor"}] | [] | False |
| B1 | AVG(time_management_score) | [{"table": "asana__project_analytics", "column": "time_management_score"}] | [] | False |


## S45

类别 `data`；来源 `query_db`；调用 `ffee6907bf684886a468cfa7aad7e26c`；状态 `success`。

```sql
SELECT team_size_category, COUNT(*) n,
       ROUND(AVG(overall_health_score),1) avg_health,
       ROUND(AVG(roi_efficiency_ratio),4) avg_roi,
       ROUND(AVG(completion_percentage),1) avg_comp,
       ROUND(AVG(efficiency_score),1) avg_eff,
       ROUND(AVG(time_management_score),1) avg_time,
       ROUND(AVG(collaboration_score),1) avg_collab,
       ROUND(AVG(complexity_factor),2) avg_complexity,
       ROUND(AVG(elapsed_days*1.0/planned_duration_days),2) avg_elapsed_ratio,
       ROUND(100.0*SUM(CASE WHEN schedule_forecast='behind_schedule' THEN 1 ELSE 0 END)/COUNT(*),1) pct_behind
FROM asana__project_analytics
GROUP BY team_size_category ORDER BY avg_roi DESC
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-053/attempt-01/sql/S45.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-053/attempt-01/sql/S45.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-053/attempt-01/results/S45.rows.jsonl)；完整：True；SHA256：`aff2b67d41d9b8a00435adf6a51d90e739cf42c723e001acb864392c4c19d627`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "asana__project_analytics", "kind": "base", "block": null, "base_tables": ["asana__project_analytics"]}] | [] | ["team_size_category"] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |
| B1 | AVG(overall_health_score) | [{"table": "asana__project_analytics", "column": "overall_health_score"}] | [] | False |
| B1 | AVG(roi_efficiency_ratio) | [{"table": "asana__project_analytics", "column": "roi_efficiency_ratio"}] | [] | False |
| B1 | AVG(completion_percentage) | [{"table": "asana__project_analytics", "column": "completion_percentage"}] | [] | False |
| B1 | AVG(efficiency_score) | [{"table": "asana__project_analytics", "column": "efficiency_score"}] | [] | False |
| B1 | AVG(time_management_score) | [{"table": "asana__project_analytics", "column": "time_management_score"}] | [] | False |
| B1 | AVG(collaboration_score) | [{"table": "asana__project_analytics", "column": "collaboration_score"}] | [] | False |
| B1 | AVG(complexity_factor) | [{"table": "asana__project_analytics", "column": "complexity_factor"}] | [] | False |
| B1 | AVG(elapsed_days * 1.0 / planned_duration_days) | [{"table": "asana__project_analytics", "column": "planned_duration_days"}, {"table": "asana__project_analytics", "column": "elapsed_days"}] | [] | False |
| B1 | COUNT(*) | [] | [] | True |
| B1 | SUM(CASE WHEN schedule_forecast = 'behind_schedule' THEN 1 ELSE 0 END) | [] | [{"table": "asana__project_analytics", "column": "schedule_forecast"}] | False |


## S46

类别 `data`；来源 `query_db`；调用 `80df049482cc429f8f9da09a59d79646`；状态 `success`。

```sql
SELECT project_size_category, COUNT(*) n,
       ROUND(AVG(overall_health_score),1) avg_health,
       ROUND(AVG(roi_efficiency_ratio),4) avg_roi,
       ROUND(AVG(completion_percentage),1) avg_comp,
       ROUND(AVG(efficiency_score),1) avg_eff,
       ROUND(AVG(time_management_score),1) avg_time,
       ROUND(AVG(complexity_factor),2) avg_complexity,
       ROUND(AVG(elapsed_days*1.0/planned_duration_days),2) avg_elapsed_ratio
FROM asana__project_analytics
GROUP BY project_size_category ORDER BY avg_roi DESC
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-053/attempt-01/sql/S46.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-053/attempt-01/sql/S46.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-053/attempt-01/results/S46.rows.jsonl)；完整：True；SHA256：`feee4e76c75dc1543f68792eab0685ac848f626070b7f20d70ff650b7a1efaca`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "asana__project_analytics", "kind": "base", "block": null, "base_tables": ["asana__project_analytics"]}] | [] | ["project_size_category"] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |
| B1 | AVG(overall_health_score) | [{"table": "asana__project_analytics", "column": "overall_health_score"}] | [] | False |
| B1 | AVG(roi_efficiency_ratio) | [{"table": "asana__project_analytics", "column": "roi_efficiency_ratio"}] | [] | False |
| B1 | AVG(completion_percentage) | [{"table": "asana__project_analytics", "column": "completion_percentage"}] | [] | False |
| B1 | AVG(efficiency_score) | [{"table": "asana__project_analytics", "column": "efficiency_score"}] | [] | False |
| B1 | AVG(time_management_score) | [{"table": "asana__project_analytics", "column": "time_management_score"}] | [] | False |
| B1 | AVG(complexity_factor) | [{"table": "asana__project_analytics", "column": "complexity_factor"}] | [] | False |
| B1 | AVG(elapsed_days * 1.0 / planned_duration_days) | [{"table": "asana__project_analytics", "column": "planned_duration_days"}, {"table": "asana__project_analytics", "column": "elapsed_days"}] | [] | False |


## S47

类别 `data`；来源 `query_db`；调用 `0124e577bde141be97dc0addd99fca00`；状态 `success`。

```sql
SELECT project_id, project_name, health_grade, overall_health_score, roi_efficiency_ratio,
       completion_percentage, efficiency_score, time_management_score, collaboration_score,
       schedule_forecast, risk_level, management_priority, complexity_factor,
       team_size_category, project_size_category, elapsed_days, planned_duration_days,
       focus_areas, success_factors, improvement_opportunities
FROM asana__project_analytics
WHERE (health_grade IN ('A','B') AND roi_efficiency_ratio < 0.5)
ORDER BY roi_efficiency_ratio ASC
LIMIT 11
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-053/attempt-01/sql/S47.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-053/attempt-01/sql/S47.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-053/attempt-01/results/S47.rows.jsonl)；完整：True；SHA256：`044eb737980c590fd2674438490a595aca12f07ae8f47993041fa5fc0900bd08`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "asana__project_analytics", "kind": "base", "block": null, "base_tables": ["asana__project_analytics"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |


## S48

类别 `data`；来源 `query_db`；调用 `244a72856c0045519a70a9f607b12cab`；状态 `success`。

```sql
SELECT project_id, project_name, health_grade, overall_health_score, roi_efficiency_ratio,
       completion_percentage, efficiency_score, time_management_score, collaboration_score,
       schedule_forecast, risk_level, management_priority, complexity_factor,
       team_size_category, project_size_category, elapsed_days, planned_duration_days,
       focus_areas, success_factors, improvement_opportunities
FROM asana__project_analytics
WHERE (health_grade IN ('D','F') AND roi_efficiency_ratio > 0.3)
ORDER BY roi_efficiency_ratio DESC
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-053/attempt-01/sql/S48.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-053/attempt-01/sql/S48.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-053/attempt-01/results/S48.rows.jsonl)；完整：True；SHA256：`83a5bef52d3002182b4b519dbebde4f96c35ee53c81ad43481b7cb977ddf1817`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "asana__project_analytics", "kind": "base", "block": null, "base_tables": ["asana__project_analytics"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |


## S49

类别 `data`；来源 `query_db`；调用 `c08584699a8d48b89ea1f28eb41bc204`；状态 `success`。

```sql
SELECT 
  ROUND(AVG(completion_percentage),1) avg_comp,
  ROUND(AVG(quality_percentage),1) avg_quality,
  ROUND(AVG(risk_percentage),1) avg_risk,
  ROUND(AVG(efficiency_score),1) avg_eff,
  ROUND(AVG(time_management_score),1) avg_time,
  ROUND(AVG(collaboration_score),1) avg_collab
FROM asana__project_analytics
WHERE health_grade = 'A'
UNION ALL
SELECT ROUND(AVG(completion_percentage),1), ROUND(AVG(quality_percentage),1), ROUND(AVG(risk_percentage),1), ROUND(AVG(efficiency_score),1), ROUND(AVG(time_management_score),1), ROUND(AVG(collaboration_score),1)
FROM asana__project_analytics WHERE health_grade = 'B'
UNION ALL
SELECT ROUND(AVG(completion_percentage),1), ROUND(AVG(quality_percentage),1), ROUND(AVG(risk_percentage),1), ROUND(AVG(efficiency_score),1), ROUND(AVG(time_management_score),1), ROUND(AVG(collaboration_score),1)
FROM asana__project_analytics WHERE health_grade = 'C'
UNION ALL
SELECT ROUND(AVG(completion_percentage),1), ROUND(AVG(quality_percentage),1), ROUND(AVG(risk_percentage),1), ROUND(AVG(efficiency_score),1), ROUND(AVG(time_management_score),1), ROUND(AVG(collaboration_score),1)
FROM asana__project_analytics WHERE health_grade = 'D'
UNION ALL
SELECT ROUND(AVG(completion_percentage),1), ROUND(AVG(quality_percentage),1), ROUND(AVG(risk_percentage),1), ROUND(AVG(efficiency_score),1), ROUND(AVG(time_management_score),1), ROUND(AVG(collaboration_score),1)
FROM asana__project_analytics WHERE health_grade = 'F'
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-053/attempt-01/sql/S49.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-053/attempt-01/sql/S49.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-053/attempt-01/results/S49.rows.jsonl)；完整：True；SHA256：`c5d0560dd054a46c4372b1a0bf0687805df2a282a4d1269bc76f06cec66b44e3`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "asana__project_analytics", "kind": "base", "block": null, "base_tables": ["asana__project_analytics"]}] | [] | [] |
| B2 | [{"alias": "asana__project_analytics", "kind": "base", "block": null, "base_tables": ["asana__project_analytics"]}] | [] | [] |
| B3 | [] | [] | [] |
| B4 | [{"alias": "asana__project_analytics", "kind": "base", "block": null, "base_tables": ["asana__project_analytics"]}] | [] | [] |
| B5 | [] | [] | [] |
| B6 | [{"alias": "asana__project_analytics", "kind": "base", "block": null, "base_tables": ["asana__project_analytics"]}] | [] | [] |
| B7 | [] | [] | [] |
| B8 | [{"alias": "asana__project_analytics", "kind": "base", "block": null, "base_tables": ["asana__project_analytics"]}] | [] | [] |
| B9 | [] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | AVG(completion_percentage) | [{"table": "asana__project_analytics", "column": "completion_percentage"}] | [] | False |
| B1 | AVG(quality_percentage) | [{"table": "asana__project_analytics", "column": "quality_percentage"}] | [] | False |
| B1 | AVG(risk_percentage) | [{"table": "asana__project_analytics", "column": "risk_percentage"}] | [] | False |
| B1 | AVG(efficiency_score) | [{"table": "asana__project_analytics", "column": "efficiency_score"}] | [] | False |
| B1 | AVG(time_management_score) | [{"table": "asana__project_analytics", "column": "time_management_score"}] | [] | False |
| B1 | AVG(collaboration_score) | [{"table": "asana__project_analytics", "column": "collaboration_score"}] | [] | False |
| B2 | AVG(completion_percentage) | [{"table": "asana__project_analytics", "column": "completion_percentage"}] | [] | False |
| B2 | AVG(quality_percentage) | [{"table": "asana__project_analytics", "column": "quality_percentage"}] | [] | False |
| B2 | AVG(risk_percentage) | [{"table": "asana__project_analytics", "column": "risk_percentage"}] | [] | False |
| B2 | AVG(efficiency_score) | [{"table": "asana__project_analytics", "column": "efficiency_score"}] | [] | False |
| B2 | AVG(time_management_score) | [{"table": "asana__project_analytics", "column": "time_management_score"}] | [] | False |
| B2 | AVG(collaboration_score) | [{"table": "asana__project_analytics", "column": "collaboration_score"}] | [] | False |
| B4 | AVG(completion_percentage) | [{"table": "asana__project_analytics", "column": "completion_percentage"}] | [] | False |
| B4 | AVG(quality_percentage) | [{"table": "asana__project_analytics", "column": "quality_percentage"}] | [] | False |
| B4 | AVG(risk_percentage) | [{"table": "asana__project_analytics", "column": "risk_percentage"}] | [] | False |
| B4 | AVG(efficiency_score) | [{"table": "asana__project_analytics", "column": "efficiency_score"}] | [] | False |
| B4 | AVG(time_management_score) | [{"table": "asana__project_analytics", "column": "time_management_score"}] | [] | False |
| B4 | AVG(collaboration_score) | [{"table": "asana__project_analytics", "column": "collaboration_score"}] | [] | False |
| B6 | AVG(completion_percentage) | [{"table": "asana__project_analytics", "column": "completion_percentage"}] | [] | False |
| B6 | AVG(quality_percentage) | [{"table": "asana__project_analytics", "column": "quality_percentage"}] | [] | False |
| B6 | AVG(risk_percentage) | [{"table": "asana__project_analytics", "column": "risk_percentage"}] | [] | False |
| B6 | AVG(efficiency_score) | [{"table": "asana__project_analytics", "column": "efficiency_score"}] | [] | False |
| B6 | AVG(time_management_score) | [{"table": "asana__project_analytics", "column": "time_management_score"}] | [] | False |
| B6 | AVG(collaboration_score) | [{"table": "asana__project_analytics", "column": "collaboration_score"}] | [] | False |
| B8 | AVG(completion_percentage) | [{"table": "asana__project_analytics", "column": "completion_percentage"}] | [] | False |
| B8 | AVG(quality_percentage) | [{"table": "asana__project_analytics", "column": "quality_percentage"}] | [] | False |
| B8 | AVG(risk_percentage) | [{"table": "asana__project_analytics", "column": "risk_percentage"}] | [] | False |
| B8 | AVG(efficiency_score) | [{"table": "asana__project_analytics", "column": "efficiency_score"}] | [] | False |
| B8 | AVG(time_management_score) | [{"table": "asana__project_analytics", "column": "time_management_score"}] | [] | False |
| B8 | AVG(collaboration_score) | [{"table": "asana__project_analytics", "column": "collaboration_score"}] | [] | False |


## S50

类别 `data`；来源 `python`；调用 `bf0afe7784a946299ec9e3beaf3dd2b7`；状态 `success`。

```sql

SELECT *, 
  CASE WHEN health_grade IN ('A','B') AND roi_efficiency_ratio < 0.5 THEN 'HHLV'
       WHEN health_grade IN ('A','B') AND roi_efficiency_ratio >= 0.5 THEN 'HH_HV'
       WHEN health_grade IN ('D','F') AND roi_efficiency_ratio > 0.3 THEN 'LHHV'
       WHEN health_grade IN ('D','F') AND roi_efficiency_ratio < 0.1 THEN 'LH_LV'
       ELSE 'Other' END AS inv_group
FROM asana__project_analytics

```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-053/attempt-01/sql/S50.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-053/attempt-01/sql/S50.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-053/attempt-01/results/S50.rows.jsonl)；完整：True；SHA256：`cfa0ca6c3e28b25eb6fb56933c26ded634231016c3eba715d559cae6cf2d657a`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "asana__project_analytics", "kind": "base", "block": null, "base_tables": ["asana__project_analytics"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |

