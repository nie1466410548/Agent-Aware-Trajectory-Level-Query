# dacomp-051

The company needs to analyze the reasons behind the decline in project delivery efficiency…

运行：已提交。官方未评分。全部 SQL 尝试/成功 53/53；数据 SQL 51/51；Python 9 次。

完整原题：

The company needs to analyze the reasons behind the decline in project delivery efficiency. Based on the existing data: first compute each user’s average task completion time (asana__user.avg_close_time_assigned_days), identify the user cohort whose completion time exceeds 1.5× the overall average, then analyze the distribution characteristics of the tasks handled by these users across complexity_score, urgency_score, and project_health_score. Meanwhile, compute each team’s task completion rate (completed_tasks/total_tasks) and average project health score, and identify underperforming teams. On this basis, dig deeper into the root causes of inefficiency, analyze the fit between individual capability and task assignment, explore opportunities to improve team collaboration models, and, combined with time trends, identify key influencing factors. Finally, produce concrete recommendations to improve efficiency.

| 表 | 行数 | 列数 |
| --- | --- | --- |
| asana__task_lifecycle_analysis | 3995 | 43 |
| asana__user | 1000 | 7 |


实际路线（分析者依据 SQL/源码概括，不代表 Agent 自述）：SQL 识别慢完成用户和低效团队 → Python 检验、回归及再次分组比较 → 交付效率建议。

数据库大小：1,871,872 字节。

## 数据 SQL

| SQL | 状态 | 基础表 | Join 输入/类型 | GROUP BY | 聚合表达式 | 结果行数 | 数据库 ms |
| --- | --- | --- | --- | --- | --- | --- | --- |
| [S3/Q1](#s3) | success | ["asana__user"] | 0 / {} | [] | [] | 1000 | 2.836 |
| [S4/Q2](#s4) | success | ["asana__task_lifecycle_analysis"] | 0 / {} | [] | ["COUNT(*)", "COUNT(DISTINCT team_id)", "COUNT(DISTINCT assignee_user_id)"] | 1 | 4.05 |
| [S5/Q3](#s5) | success | ["asana__user"] | 0 / {} | [] | ["COUNT(*)", "MIN(avg_close_time_assigned_days)", "MAX(avg_close_time_assigned_days)", "AVG(avg_close_time_assigned_days)", "AVG(avg_close_time_assigned_days)"] | 1 | 0.787 |
| [S6/Q4](#s6) | success | ["asana__task_lifecycle_analysis"] | 0 / {} | ["team_id"] | ["COUNT(*)", "COUNT(DISTINCT assignee_user_id)", "COUNT(*) FILTER(WHERE is_completed = 1)"] | 20 | 3.266 |
| [S7/Q5](#s7) | success | ["asana__user"] | 0 / {} | [] | ["AVG(avg_close_time_assigned_days)", "COUNT(*)"] | 1 | 0.543 |
| [S8/Q6](#s8) | success | ["asana__user"] | 0 / {} | [] | ["AVG(avg_close_time_assigned_days)"] | 30 | 0.688 |
| [S9/Q7](#s9) | success | ["asana__task_lifecycle_analysis", "asana__user"] | 2 / {'INNER': 1} | [] | ["COUNT(*)"] | 1 | 3.357 |
| [S10/Q8](#s10) | success | ["asana__task_lifecycle_analysis", "asana__user"] | 2 / {'LEFT': 1} | [] | ["COUNT(*)", "COUNT(DISTINCT assignee_user_id)"] | 1 | 4.335 |
| [S11/Q9](#s11) | success | ["asana__task_lifecycle_analysis", "asana__user"] | 2 / {'INNER': 1} | [] | ["AVG(avg_close_time_assigned_days)", "COUNT(*)", "SUM(CASE WHEN is_completed = 1 THEN 1 ELSE 0 END)", "AVG(complexity_score)", "AVG(urgency_score)", "AVG(project_health_score)", "AVG(hours_assigned_to_completion)", "AVG(avg_daily_activity_rate)"] | 1 | 3.832 |
| [S12/Q10](#s12) | success | ["asana__task_lifecycle_analysis", "asana__user"] | 2 / {'INNER': 1} | [] | ["AVG(avg_close_time_assigned_days)", "COUNT(*)", "SUM(CASE WHEN is_completed = 1 THEN 1 ELSE 0 END)", "AVG(complexity_score)", "AVG(urgency_score)", "AVG(project_health_score)", "AVG(hours_assigned_to_completion)", "AVG(avg_daily_activity_rate)"] | 1 | 4.188 |
| [S13/Q11](#s13) | success | ["asana__task_lifecycle_analysis", "asana__user"] | 2 / {'INNER': 1} | ["complexity_score"] | ["AVG(avg_close_time_assigned_days)", "COUNT(*)", "COUNT(*)", "COUNT(*)"] | 5 | 5.003 |
| [S14/Q12](#s14) | success | ["asana__task_lifecycle_analysis", "asana__user"] | 2 / {'INNER': 1} | ["urgency_score"] | ["AVG(avg_close_time_assigned_days)", "COUNT(*)", "COUNT(*)", "COUNT(*)"] | 5 | 4.067 |
| [S15/Q13](#s15) | success | ["asana__task_lifecycle_analysis", "asana__user"] | 2 / {'INNER': 1} | ["project_health_score"] | ["AVG(avg_close_time_assigned_days)", "COUNT(*)", "COUNT(*)", "COUNT(*)"] | 80 | 3.973 |
| [S16/Q14](#s16) | success | ["asana__task_lifecycle_analysis"] | 0 / {} | ["team_id"] | ["COUNT(*)", "SUM(CASE WHEN is_completed = 1 THEN 1 ELSE 0 END)", "COUNT(DISTINCT assignee_user_id)", "AVG(project_health_score)", "AVG(complexity_score)", "AVG(urgency_score)", "AVG(hours_assigned_to_completion)", "COUNT(*)", "SUM(CASE WHEN is_completed = 1 THEN 1 ELSE 0 END)"] | 50 | 4.449 |
| [S17/Q15](#s17) | success | ["asana__task_lifecycle_analysis"] | 0 / {} | [] | ["AVG(project_health_score)", "AVG(complexity_score)", "AVG(urgency_score)", "COUNT(*)", "SUM(CASE WHEN is_completed = 1 THEN 1 ELSE 0 END)"] | 1 | 1.694 |
| [S18/Q16](#s18) | success | ["asana__task_lifecycle_analysis"] | 0 / {} | ["team_id"] | ["COUNT(*)", "SUM(CASE WHEN is_completed = 1 THEN 1 ELSE 0 END)", "COUNT(DISTINCT assignee_user_id)", "AVG(project_health_score)", "AVG(hours_assigned_to_completion)", "COUNT(*)", "SUM(CASE WHEN is_completed = 1 THEN 1 ELSE 0 END)"] | 50 | 3.918 |
| [S19/Q17](#s19) | success | ["asana__task_lifecycle_analysis", "asana__user"] | 2 / {'LEFT': 1} | ["t.team_id"] | ["AVG(avg_close_time_assigned_days)", "AVG(avg_close_time_assigned_days)", "COUNT(*)", "SUM(CASE WHEN t.is_completed = 1 THEN 1 ELSE 0 END)", "COUNT(DISTINCT t.assignee_user_id)", "COUNT(DISTINCT CASE WHEN u.avg_close_time_assigned_days > (SELECT 1.5 * AVG(avg_close_time_assigned_days) FROM asana__user) THEN t.assignee_user_id END)", "AVG(t.project_health_score)", "AVG(t.hours_assigned_to_completion)", "COUNT(*)", "SUM(CASE WHEN t.is_completed = 1 THEN 1 ELSE 0 END)", "COUNT(DISTINCT CASE WHEN u.avg_close_time_assigned_days > (SELECT 1.5 * AVG(avg_close_time_assigned_days) FROM asana__user) THEN t.assignee_user_id END)", "COUNT(DISTINCT t.assignee_user_id)"] | 50 | 8.156 |
| [S20/Q18](#s20) | success | ["asana__task_lifecycle_analysis", "asana__user"] | 2 / {'INNER': 1} | ["CASE WHEN u.avg_close_time_assigned_days > (SELECT 1.5 * AVG(avg_close_time_assigned_days) FROM asana__user) THEN 'SLOW' ELSE 'FAST' END"] | ["AVG(avg_close_time_assigned_days)", "COUNT(*)", "AVG(t.hours_to_assignment)", "AVG(t.hours_assigned_to_completion)", "AVG(t.total_lifecycle_hours)", "AVG(t.total_story_events)", "AVG(t.unique_action_types)", "AVG(t.days_with_activity)", "AVG(t.avg_daily_activity_rate)", "AVG(t.delay_days)", "AVG(t.response_time_days)"] | 2 | 5.836 |
| [S21/Q19](#s21) | success | ["asana__task_lifecycle_analysis", "asana__user"] | 2 / {'INNER': 1} | ["CASE WHEN u.avg_close_time_assigned_days > (SELECT 1.5 * AVG(avg_close_time_assigned_days) FROM asana__user) THEN 'SLOW' ELSE 'FAST' END", "t.task_status_category"] | ["AVG(avg_close_time_assigned_days)", "COUNT(*)"] | 6 | 5.151 |
| [S22/Q20](#s22) | success | ["asana__task_lifecycle_analysis", "asana__user"] | 2 / {'INNER': 1} | ["CASE WHEN u.avg_close_time_assigned_days > (SELECT 1.5 * AVG(avg_close_time_assigned_days) FROM asana__user) THEN 'SLOW' ELSE 'FAST' END", "t.assignee_performance_grade"] | ["AVG(avg_close_time_assigned_days)", "COUNT(*)"] | 5 | 5.101 |
| [S23/Q21](#s23) | success | ["asana__task_lifecycle_analysis", "asana__user"] | 2 / {'INNER': 1} | ["CASE WHEN u.avg_close_time_assigned_days > (SELECT 1.5 * AVG(avg_close_time_assigned_days) FROM asana__user) THEN 'SLOW' ELSE 'FAST' END", "t.complexity_execution_match"] | ["AVG(avg_close_time_assigned_days)", "COUNT(*)"] | 14 | 5.34 |
| [S24/Q22](#s24) | success | ["asana__task_lifecycle_analysis", "asana__user"] | 2 / {'INNER': 1} | ["CASE WHEN u.avg_close_time_assigned_days > (SELECT 1.5 * AVG(avg_close_time_assigned_days) FROM asana__user) THEN 'SLOW' ELSE 'FAST' END", "t.relative_performance_vs_project"] | ["AVG(avg_close_time_assigned_days)", "COUNT(*)"] | 12 | 5.415 |
| [S25/Q23](#s25) | success | ["asana__task_lifecycle_analysis", "asana__user"] | 2 / {'INNER': 1} | ["CASE WHEN u.avg_close_time_assigned_days > (SELECT 1.5 * AVG(avg_close_time_assigned_days) FROM asana__user) THEN 'SLOW' ELSE 'FAST' END", "t.lifecycle_efficiency_category"] | ["AVG(avg_close_time_assigned_days)", "COUNT(*)"] | 12 | 5.331 |
| [S26/Q24](#s26) | success | ["asana__task_lifecycle_analysis", "asana__user"] | 2 / {'INNER': 1} | ["CASE WHEN u.avg_close_time_assigned_days > (SELECT 1.5 * AVG(avg_close_time_assigned_days) FROM asana__user) THEN 'SLOW' ELSE 'FAST' END", "t.activity_level"] | ["AVG(avg_close_time_assigned_days)", "COUNT(*)"] | 12 | 5.331 |
| [S27/Q25](#s27) | success | ["asana__task_lifecycle_analysis", "asana__user"] | 2 / {'INNER': 1} | ["CASE WHEN u.avg_close_time_assigned_days > (SELECT 1.5 * AVG(avg_close_time_assigned_days) FROM asana__user) THEN 'SLOW' ELSE 'FAST' END", "t.anomaly_patterns"] | ["AVG(avg_close_time_assigned_days)", "COUNT(*)"] | 6 | 5.059 |
| [S28/Q26](#s28) | success | ["asana__user"] | 2 / {'LEFT': 1} | ["CASE WHEN NOT s.user_id IS NULL THEN 'SLOW' ELSE 'FAST' END"] | ["AVG(avg_close_time_assigned_days)", "COUNT(*)", "AVG(u.number_of_open_tasks)", "AVG(u.number_of_tasks_completed)", "AVG(u.avg_close_time_assigned_days)"] | 2 | 2.416 |
| [S29/Q27](#s29) | success | ["asana__task_lifecycle_analysis"] | 0 / {} | ["STRFTIME('%Y-%m', created_at)"] | ["COUNT(*)", "SUM(CASE WHEN is_completed = 1 THEN 1 ELSE 0 END)", "AVG(complexity_score)", "AVG(project_health_score)", "COUNT(*)", "SUM(CASE WHEN is_completed = 1 THEN 1 ELSE 0 END)"] | 7 | 4.515 |
| [S30/Q28](#s30) | success | ["asana__task_lifecycle_analysis", "asana__user"] | 2 / {'INNER': 1} | ["CASE WHEN u.avg_close_time_assigned_days > (SELECT 1.5 * AVG(avg_close_time_assigned_days) FROM asana__user) THEN 'SLOW' ELSE 'FAST' END", "t.complexity_execution_match"] | ["AVG(avg_close_time_assigned_days)", "AVG(avg_close_time_assigned_days)", "COUNT(*)", "COUNT(*)", "COUNT(*)"] | 14 | 6.294 |
| [S31/Q29](#s31) | success | ["asana__task_lifecycle_analysis", "asana__user"] | 2 / {'INNER': 1} | ["CASE WHEN u.avg_close_time_assigned_days > (SELECT 1.5 * AVG(avg_close_time_assigned_days) FROM asana__user) THEN 'SLOW' ELSE 'FAST' END", "t.improvement_opportunities"] | ["AVG(avg_close_time_assigned_days)", "AVG(avg_close_time_assigned_days)", "COUNT(*)", "COUNT(*)", "COUNT(*)"] | 20 | 6.206 |
| [S32/Q30](#s32) | success | ["asana__task_lifecycle_analysis", "asana__user"] | 2 / {'INNER': 1} | ["t.improvement_opportunities"] | ["AVG(avg_close_time_assigned_days)", "COUNT(*)"] | 10 | 4.299 |
| [S33/Q31](#s33) | success | ["asana__task_lifecycle_analysis", "asana__user"] | 2 / {'INNER': 1} | ["t.complexity_execution_match"] | ["AVG(avg_close_time_assigned_days)", "COUNT(*)"] | 7 | 4.277 |
| [S34/Q32](#s34) | success | ["asana__task_lifecycle_analysis", "asana__user"] | 2 / {'INNER': 1} | ["assignee_user_id", "CASE WHEN u.avg_close_time_assigned_days > (SELECT 1.5 * AVG(avg_close_time_assigned_days) FROM asana__user) THEN 'SLOW' ELSE 'FAST' END"] | ["COUNT(*)", "SUM(CASE WHEN is_completed = 1 THEN 1 ELSE 0 END)", "AVG(complexity_score)", "AVG(urgency_score)", "AVG(project_health_score)", "AVG(avg_close_time_assigned_days)", "COUNT(*)", "AVG(ts.n_tasks)", "AVG(ts.avg_task_complexity)", "AVG(ts.avg_task_urgency)", "AVG(ts.avg_project_health)"] | 2 | 8.801 |
| [S35/Q33](#s35) | success | ["asana__task_lifecycle_analysis", "asana__user"] | 2 / {'LEFT': 1} | ["t.team_id"] | ["AVG(avg_close_time_assigned_days)", "COUNT(*)", "COUNT(DISTINCT CAST(t.assignee_user_id AS TEXT))", "COUNT(DISTINCT CASE WHEN u.avg_close_time_assigned_days > (SELECT 1.5 * AVG(avg_close_time_assigned_days) FROM asana__user) THEN CAST(t.assignee_user_id AS TEXT) END)", "COUNT(*) FILTER(WHERE is_completed = 1)", "AVG(t.hours_assigned_to_completion)", "COUNT(*)", "COUNT(*) FILTER(WHERE is_completed = 1)"] | 15 | 7.94 |
| [S36/Q34](#s36) | success | ["asana__task_lifecycle_analysis", "asana__user"] | 2 / {'INNER': 1} | [] | ["AVG(avg_close_time_assigned_days)"] | 2298 | 22.368 |
| [S37/Q35](#s37) | success | ["asana__task_lifecycle_analysis", "asana__user"] | 2 / {'LEFT': 1} | ["t.team_id"] | ["AVG(avg_close_time_assigned_days)", "AVG(avg_close_time_assigned_days)", "COUNT(*)", "SUM(CASE WHEN t.is_completed = 1 THEN 1 ELSE 0 END)", "COUNT(DISTINCT t.assignee_user_id)", "COUNT(DISTINCT CASE WHEN u.avg_close_time_assigned_days > (SELECT 1.5 * AVG(avg_close_time_assigned_days) FROM asana__user) THEN t.assignee_user_id END)", "AVG(t.project_health_score)", "AVG(t.hours_assigned_to_completion)", "AVG(t.complexity_score)", "AVG(t.urgency_score)", "COUNT(*)", "SUM(CASE WHEN t.is_completed = 1 THEN 1 ELSE 0 END)", "COUNT(DISTINCT CASE WHEN u.avg_close_time_assigned_days > (SELECT 1.5 * AVG(avg_close_time_assigned_days) FROM asana__user) THEN t.assignee_user_id END)", "COUNT(DISTINCT t.assignee_user_id)"] | 50 | 9.194 |
| [S38/Q36](#s38) | success | ["asana__task_lifecycle_analysis", "asana__user"] | 2 / {'INNER': 1} | ["STRFTIME('%Y-%m', t.created_at)", "CASE WHEN u.avg_close_time_assigned_days > (SELECT 1.5 * AVG(avg_close_time_assigned_days) FROM asana__user) THEN 'SLOW' ELSE 'FAST' END"] | ["AVG(avg_close_time_assigned_days)", "COUNT(*)", "SUM(CASE WHEN t.is_completed = 1 THEN 1 ELSE 0 END)", "AVG(t.hours_assigned_to_completion)", "AVG(t.avg_daily_activity_rate)"] | 14 | 6.962 |
| [S39/Q37](#s39) | success | ["asana__task_lifecycle_analysis"] | 0 / {} | ["STRFTIME('%Y-%m', created_at)"] | ["COUNT(*)", "SUM(CASE WHEN is_completed = 1 THEN 1 ELSE 0 END)", "COUNT(*)", "SUM(CASE WHEN is_completed = 1 THEN 1 ELSE 0 END)"] | 7 | 4.135 |
| [S40/Q38](#s40) | success | ["asana__task_lifecycle_analysis", "asana__user"] | 2 / {'LEFT': 1} | ["assignee_user_id"] | ["COUNT(*)", "SUM(CASE WHEN is_completed = 1 THEN 1 ELSE 0 END)"] | 1000 | 7.082 |
| [S41/Q39](#s41) | success | ["asana__task_lifecycle_analysis", "asana__user"] | 2 / {'INNER': 1} | [] | ["AVG(avg_close_time_assigned_days)"] | 2298 | 22.278 |
| [S42/Q40](#s42) | success | ["asana__task_lifecycle_analysis", "asana__user"] | 2 / {'INNER': 1} | ["t.assignee_user_id"] | ["COUNT(*)", "SUM(CASE WHEN t.is_completed = 1 THEN 1 ELSE 0 END)", "SUM(CASE WHEN t.delay_days > 0 THEN 1 ELSE 0 END)", "AVG(t.complexity_score)", "AVG(t.urgency_score)", "AVG(t.hours_assigned_to_completion)", "AVG(t.avg_daily_activity_rate)"] | 640 | 9.01 |
| [S43/Q41](#s43) | success | ["asana__task_lifecycle_analysis", "asana__user"] | 2 / {'LEFT': 1} | ["t.team_id"] | ["AVG(avg_close_time_assigned_days)", "COUNT(*)", "COUNT(DISTINCT CASE WHEN u.avg_close_time_assigned_days > (SELECT 1.5 * AVG(avg_close_time_assigned_days) FROM asana__user) THEN t.assignee_user_id END)", "COUNT(*)", "SUM(CASE WHEN t.is_completed = 1 THEN 1 ELSE 0 END)"] | 50 | 6.065 |
| [S44/Q42](#s44) | success | ["asana__task_lifecycle_analysis", "asana__user"] | 2 / {'INNER': 1} | ["t.success_patterns"] | ["AVG(avg_close_time_assigned_days)", "COUNT(*)", "COUNT(*)", "COUNT(*)"] | 10 | 4.78 |
| [S45/Q43](#s45) | success | ["asana__task_lifecycle_analysis", "asana__user"] | 2 / {'INNER': 1} | ["t.anomaly_patterns"] | ["AVG(avg_close_time_assigned_days)", "COUNT(*)", "COUNT(*)", "COUNT(*)"] | 3 | 5.714 |
| [S46/Q44](#s46) | success | ["asana__task_lifecycle_analysis", "asana__user"] | 2 / {'INNER': 1} | ["t.success_patterns"] | ["AVG(avg_close_time_assigned_days)", "COUNT(*)", "COUNT(*)", "COUNT(*)"] | 10 | 4.931 |
| [S47/Q45](#s47) | success | ["asana__task_lifecycle_analysis", "asana__user"] | 2 / {'LEFT': 1} | ["t.project_name"] | ["AVG(avg_close_time_assigned_days)", "COUNT(*)", "COUNT(DISTINCT CASE WHEN u.avg_close_time_assigned_days > (SELECT 1.5 * AVG(avg_close_time_assigned_days) FROM asana__user) THEN t.assignee_user_id END)", "AVG(t.project_health_score)", "AVG(t.complexity_score)", "COUNT(*)", "SUM(CASE WHEN t.is_completed = 1 THEN 1 ELSE 0 END)"] | 15 | 7.432 |
| [S48/Q46](#s48) | success | ["asana__task_lifecycle_analysis"] | 0 / {} | [] | ["COUNT(*)", "SUM(CASE WHEN NOT parent_task_id IS NULL AND parent_task_id <> task_id THEN 1 ELSE 0 END)", "SUM(CASE WHEN is_completed = 1 THEN 1 ELSE 0 END)"] | 1 | 1.64 |
| [S49/Q47](#s49) | success | ["asana__task_lifecycle_analysis", "asana__user"] | 2 / {'INNER': 1} | [] | ["AVG(avg_close_time_assigned_days)"] | 2298 | 21.108 |
| [S50/Q48](#s50) | success | ["asana__task_lifecycle_analysis", "asana__user"] | 2 / {'INNER': 1} | [] | ["AVG(avg_close_time_assigned_days)"] | 2298 | 21.124 |
| [S51/Q49](#s51) | success | ["asana__task_lifecycle_analysis", "asana__user"] | 2 / {'INNER': 1} | [] | ["AVG(avg_close_time_assigned_days)"] | 2298 | 38.648 |
| [S52/Q50](#s52) | success | ["asana__task_lifecycle_analysis", "asana__user"] | 2 / {'INNER': 1} | [] | ["AVG(avg_close_time_assigned_days)"] | 2298 | 21.652 |
| [S53/Q51](#s53) | success | ["asana__task_lifecycle_analysis"] | 0 / {} | ["team_id"] | ["COUNT(*)", "SUM(CASE WHEN is_completed = 1 THEN 1 ELSE 0 END)", "AVG(project_health_score)", "AVG(hours_assigned_to_completion)", "COUNT(*)", "SUM(CASE WHEN is_completed = 1 THEN 1 ELSE 0 END)"] | 10 | 2.958 |


## 元数据和设置

| SQL | 类别 | 状态 | 内容 |
| --- | --- | --- | --- |
| S1 | connection_setup | success | PRAGMA query_only=ON |
| S2 | metadata | success | SELECT name,sql FROM sqlite_master WHERE type='table' ORDER BY name |


## Python 与执行位置

人工源码审查：**database_first_violation**。虽然 SQL 已完成大量连接与分层汇总，Python 仍按成功模式、完成状态及活动水平计算计数、均值和完成率，属于可推入数据库的计算。t 检验、效应量与回归本身是合理统计补充。 [证据](../reviews/dacomp-051.json)。

P1：Need to run statistical analysis (chi-square, t-tests) and create visualizations comparing slow vs fast cohorts across multiple dimensions. This is outside SQL's reasonable capability.

[源码](../../../runs/dsv4flash-db-first-full-01/dacomp-051/attempt-01/python/P1.py)；[输出](../../../runs/dsv4flash-db-first-full-01/dacomp-051/attempt-01/python/P1.stdout)；[错误](../../../runs/dsv4flash-db-first-full-01/dacomp-051/attempt-01/python/P1.stderr)。检出需人工核验的 SQL 可实现操作：.query(；不能仅凭理由判为合规。

P2：Team-level analysis requires correlation and scatter plot visualization which is better done in Python than SQL. Also need to analyze time trends and individual capability fit.

[源码](../../../runs/dsv4flash-db-first-full-01/dacomp-051/attempt-01/python/P2.py)；[输出](../../../runs/dsv4flash-db-first-full-01/dacomp-051/attempt-01/python/P2.stdout)；[错误](../../../runs/dsv4flash-db-first-full-01/dacomp-051/attempt-01/python/P2.stderr)。检出需人工核验的 SQL 可实现操作：.query(；不能仅凭理由判为合规。

P3：Time trend analysis and workload vs speed correlation are best done in Python for visualization and statistical testing.

[源码](../../../runs/dsv4flash-db-first-full-01/dacomp-051/attempt-01/python/P3.py)；[输出](../../../runs/dsv4flash-db-first-full-01/dacomp-051/attempt-01/python/P3.stdout)；[错误](../../../runs/dsv4flash-db-first-full-01/dacomp-051/attempt-01/python/P3.stderr)。检出需人工核验的 SQL 可实现操作：.query(；不能仅凭理由判为合规。

P4：Need to compare categorical lifecycle/pattern features between cohorts and create visualizations, including stacked bar charts, which is easier in Python.

[源码](../../../runs/dsv4flash-db-first-full-01/dacomp-051/attempt-01/python/P4.py)；[输出](../../../runs/dsv4flash-db-first-full-01/dacomp-051/attempt-01/python/P4.stdout)；[错误](../../../runs/dsv4flash-db-first-full-01/dacomp-051/attempt-01/python/P4.stderr)。检出需人工核验的 SQL 可实现操作：groupby(, .query(；不能仅凭理由判为合规。

P5：Individual capability-fit analysis requires per-user aggregation and correlation/segmentation, which is more naturally handled in Python.

[源码](../../../runs/dsv4flash-db-first-full-01/dacomp-051/attempt-01/python/P5.py)；[输出](../../../runs/dsv4flash-db-first-full-01/dacomp-051/attempt-01/python/P5.stdout)；[错误](../../../runs/dsv4flash-db-first-full-01/dacomp-051/attempt-01/python/P5.stderr)。检出需人工核验的 SQL 可实现操作：.query(；不能仅凭理由判为合规。

P6：Need regression analysis to identify key drivers of task completion time and compare completed vs open tasks, which is a statistical modeling task better handled in Python.

[源码](../../../runs/dsv4flash-db-first-full-01/dacomp-051/attempt-01/python/P6.py)；[输出](../../../runs/dsv4flash-db-first-full-01/dacomp-051/attempt-01/python/P6.stdout)；[错误](../../../runs/dsv4flash-db-first-full-01/dacomp-051/attempt-01/python/P6.stderr)。检出需人工核验的 SQL 可实现操作：groupby(, .query(, sort_values(；不能仅凭理由判为合规。

P7：Statsmodels is not available, so I'll use sklearn/stats for regression analysis. Also need to complete the analysis of completion patterns and collaboration effects.

[源码](../../../runs/dsv4flash-db-first-full-01/dacomp-051/attempt-01/python/P7.py)；[输出](../../../runs/dsv4flash-db-first-full-01/dacomp-051/attempt-01/python/P7.stdout)；[错误](../../../runs/dsv4flash-db-first-full-01/dacomp-051/attempt-01/python/P7.stderr)。检出需人工核验的 SQL 可实现操作：groupby(, .query(, sort_values(；不能仅凭理由判为合规。

P8：Neither statsmodels nor sklearn are available, so I'll implement OLS regression with numpy and complete the driver analysis and remaining group comparisons.

[源码](../../../runs/dsv4flash-db-first-full-01/dacomp-051/attempt-01/python/P8.py)；[输出](../../../runs/dsv4flash-db-first-full-01/dacomp-051/attempt-01/python/P8.stdout)；[错误](../../../runs/dsv4flash-db-first-full-01/dacomp-051/attempt-01/python/P8.stderr)。检出需人工核验的 SQL 可实现操作：groupby(, .query(, sort_values(；不能仅凭理由判为合规。

P9：Need to create a comprehensive summary visualization showing the key drivers of inefficiency for the final report.

[源码](../../../runs/dsv4flash-db-first-full-01/dacomp-051/attempt-01/python/P9.py)；[输出](../../../runs/dsv4flash-db-first-full-01/dacomp-051/attempt-01/python/P9.stdout)；[错误](../../../runs/dsv4flash-db-first-full-01/dacomp-051/attempt-01/python/P9.stderr)。检出需人工核验的 SQL 可实现操作：groupby(, .query(, sort_values(；不能仅凭理由判为合规。

## 优化机会

已验证候选。筛选限于精确 SQL、相同自包含 CTE、相同单表完整过滤、可分解单表聚合；未覆盖任意 Join 等价和一般谓词蕴含。全部候选都是 offline，未测在线预测。

| 候选 | 类型 | 已有结果 | 覆盖 SQL | 后续次数 | 中间行数 | 验证 | 成本 |
| --- | --- | --- | --- | --- | --- | --- | --- |
| C1 | exact-result reuse | True | ["S36", "S41", "S49", "S50", "S51", "S52"] | 5 | 2298 | verified | Not benchmarked; correctness alone does not establish net speedup. |
| C2 | common filtered view | False | ["S4", "S16", "S17", "S29", "S48", "S53"] | 5 | 3995 | verified | Not benchmarked; correctness alone does not establish net speedup. |
| C3 | aggregate MV | False | ["S17", "S29", "S48"] | 2 | 7 | verified | Not benchmarked; correctness alone does not establish net speedup. |


已验证覆盖（含触发查询、候选并集去重）：12/51 条成功数据 SQL。正确性仅针对当前数据库快照；未测性能的候选不能声称已加速。

[完整 build/rewrite 与比较证据](dacomp-051.analysis.json)。

### C1：exact-result reuse

Identical normalized SQL and parameters; archive equality checked.

原查询 [S36](#s36), [S41](#s41), [S49](#s49), [S50](#s50), [S51](#s51), [S52](#s52) → 保留前序结果 S36 → 后续 5 次可复用。该构建点为事后假设，不代表 Agent 当时预知后续。

| 原 SQL | 列名一致 | 结果一致 | 比较方法 |
| --- | --- | --- | --- |
| S41 | True | True | exact_multiset |
| S49 | True | True | exact_multiset |
| S50 | True | True | exact_multiset |
| S51 | True | True | exact_multiset |
| S52 | True | True | exact_multiset |


验证状态：verified；成本结论：Not benchmarked; correctness alone does not establish net speedup.

### C2：common filtered view

Same single source and complete filter; original filter retained.

原查询 [S4](#s4), [S16](#s16), [S17](#s17), [S29](#s29), [S48](#s48), [S53](#s53) → 新增共享状态 C2 → 后续 5 次可复用。该构建点为事后假设，不代表 Agent 当时预知后续。

构建定义：

```sql
SELECT * FROM "asana__task_lifecycle_analysis" WHERE is_valid_record = 1
```

受益查询 S4 的改写示例：

```sql
SELECT COUNT(*) AS total_tasks, COUNT(DISTINCT team_id) AS teams, COUNT(DISTINCT assignee_user_id) AS users FROM temp.reuse_candidate AS asana__task_lifecycle_analysis WHERE is_valid_record = 1
```

| 原 SQL | 列名一致 | 结果一致 | 比较方法 |
| --- | --- | --- | --- |
| S4 | True | True | exact_multiset |
| S16 | True | True | ordered_numeric_tolerance |
| S17 | True | True | exact_multiset |
| S29 | True | True | ordered_numeric_tolerance |
| S48 | True | True | exact_multiset |
| S53 | True | True | ordered_numeric_tolerance |


验证状态：verified；成本结论：Not benchmarked; correctness alone does not establish net speedup.

### C3：aggregate MV

Union of grouping keys; decomposable aggregate states; AVG uses SUM and non-NULL COUNT.

原查询 [S17](#s17), [S29](#s29), [S48](#s48) → 新增共享状态 C3 → 后续 2 次可复用。该构建点为事后假设，不代表 Agent 当时预知后续。

构建定义：

```sql
SELECT STRFTIME('%Y-%m', created_at) AS __g0, SUM(project_health_score) AS __a0_sum, COUNT(project_health_score) AS __a0_n, SUM(complexity_score) AS __a1_sum, COUNT(complexity_score) AS __a1_n, SUM(urgency_score) AS __a2_sum, COUNT(urgency_score) AS __a2_n, COUNT(*) AS __a3, SUM(CASE WHEN is_completed = 1 THEN 1 ELSE 0 END) AS __a4, SUM(CASE WHEN NOT parent_task_id IS NULL AND parent_task_id <> task_id THEN 1 ELSE 0 END) AS __a5 FROM "asana__task_lifecycle_analysis" WHERE is_valid_record = 1 GROUP BY STRFTIME('%Y-%m', created_at)
```

受益查询 S17 的改写示例：

```sql
SELECT ROUND(100.0 * SUM(__a4) / SUM(__a3), 2) AS overall_completion_rate, ROUND((1.0 * SUM(__a0_sum) / NULLIF(SUM(__a0_n), 0)), 2) AS overall_avg_health, ROUND((1.0 * SUM(__a1_sum) / NULLIF(SUM(__a1_n), 0)), 2) AS overall_avg_complexity, ROUND((1.0 * SUM(__a2_sum) / NULLIF(SUM(__a2_n), 0)), 2) AS overall_avg_urgency FROM temp.reuse_candidate
```

| 原 SQL | 列名一致 | 结果一致 | 比较方法 |
| --- | --- | --- | --- |
| S17 | True | True | exact_multiset |
| S29 | True | True | ordered_numeric_tolerance |
| S48 | True | True | exact_multiset |


验证状态：verified；成本结论：Not benchmarked; correctness alone does not establish net speedup.

结果依赖：自动记录 SQL→Python 的接口父调用，以及源码中引用归档文件的消费者；字面值相同不认定因果。模型方向选择需要人工读取消息，尚未做全面因果标注。

[原始报告](../../../runs/dsv4flash-db-first-full-01/dacomp-051/attempt-01/answer.md)；[统一消息](../../../runs/dsv4flash-db-first-full-01/dacomp-051/attempt-01/messages.jsonl)；[原始 OpenCode 事件](../../../runs/dsv4flash-db-first-full-01/dacomp-051/attempt-01/opencode.jsonl)；[SQL 引擎日志](../../../runs/dsv4flash-db-first-full-01/dacomp-051/attempt-01/sql_journal.jsonl)。

[可读报告（本地图片链接规范化）](../answers/dacomp-051.md)。原始回答保留，分析结论未改写。

## S1

类别 `connection_setup`；来源 `connection`；调用 `85a8a08bc624489180c0af2040a4744e`；状态 `success`。

```sql
PRAGMA query_only=ON
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-051/attempt-01/sql/S1.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-051/attempt-01/sql/S1.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-051/attempt-01/results/S1.rows.jsonl)；完整：True；SHA256：`e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`。

## S2

类别 `metadata`；来源 `list_db`；调用 `85a8a08bc624489180c0af2040a4744e`；状态 `success`。

```sql
SELECT name,sql FROM sqlite_master WHERE type='table' ORDER BY name
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-051/attempt-01/sql/S2.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-051/attempt-01/sql/S2.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-051/attempt-01/results/S2.rows.jsonl)；完整：True；SHA256：`e020a560957c536c1faa4bfdaf98378baea00de228129d272a45f8ad69f47243`。

## S3

类别 `data`；来源 `query_db`；调用 `e468f3c46c3949d8bbb744d365d3a8a3`；状态 `success`。

```sql
SELECT * FROM asana__user ORDER BY avg_close_time_assigned_days DESC
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-051/attempt-01/sql/S3.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-051/attempt-01/sql/S3.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-051/attempt-01/results/S3.rows.jsonl)；完整：True；SHA256：`87ceac06ca5ec51867318f9c6869f6d692dc9c72f852ad339c86ba6f331b9ee3`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "asana__user", "kind": "base", "block": null, "base_tables": ["asana__user"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |


## S4

类别 `data`；来源 `query_db`；调用 `15dbc3a3ecd74ca7bd59cb149f0e563f`；状态 `success`。

```sql
SELECT COUNT(*) as total_tasks, COUNT(DISTINCT team_id) as teams, COUNT(DISTINCT assignee_user_id) as users FROM asana__task_lifecycle_analysis WHERE is_valid_record = 1
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-051/attempt-01/sql/S4.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-051/attempt-01/sql/S4.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-051/attempt-01/results/S4.rows.jsonl)；完整：True；SHA256：`383bf2b493cf4cf8e894ca0f596bf62a1040257037b764e0fde79a7b37811e99`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "asana__task_lifecycle_analysis", "kind": "base", "block": null, "base_tables": ["asana__task_lifecycle_analysis"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |
| B1 | COUNT(DISTINCT team_id) | [{"table": "asana__task_lifecycle_analysis", "column": "team_id"}] | [] | False |
| B1 | COUNT(DISTINCT assignee_user_id) | [{"table": "asana__task_lifecycle_analysis", "column": "assignee_user_id"}] | [] | False |


## S5

类别 `data`；来源 `query_db`；调用 `fb065e41ea27490588ff58772047bb3e`；状态 `success`。

```sql
SELECT COUNT(*) AS user_count, ROUND(AVG(avg_close_time_assigned_days),4) AS overall_avg,
ROUND(1.5*AVG(avg_close_time_assigned_days),4) AS threshold_15x,
MIN(avg_close_time_assigned_days) AS min_val, MAX(avg_close_time_assigned_days) AS max_val
FROM asana__user
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-051/attempt-01/sql/S5.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-051/attempt-01/sql/S5.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-051/attempt-01/results/S5.rows.jsonl)；完整：True；SHA256：`82820f8a0bd02e1acf230a70fb0afd3f4d819a1a03b85edb1f4bed389e4f44d4`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "asana__user", "kind": "base", "block": null, "base_tables": ["asana__user"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |
| B1 | MIN(avg_close_time_assigned_days) | [{"table": "asana__user", "column": "avg_close_time_assigned_days"}] | [] | False |
| B1 | MAX(avg_close_time_assigned_days) | [{"table": "asana__user", "column": "avg_close_time_assigned_days"}] | [] | False |
| B1 | AVG(avg_close_time_assigned_days) | [{"table": "asana__user", "column": "avg_close_time_assigned_days"}] | [] | False |
| B1 | AVG(avg_close_time_assigned_days) | [{"table": "asana__user", "column": "avg_close_time_assigned_days"}] | [] | False |


## S6

类别 `data`；来源 `query_db`；调用 `811380530f154f82b7b451750dabb4b4`；状态 `success`。

```sql
SELECT team_id, COUNT(*) AS task_cnt, COUNT(DISTINCT assignee_user_id) AS users_cnt,
COUNT(*) FILTER (WHERE is_completed=1) AS completed_cnt FROM asana__task_lifecycle_analysis
GROUP BY team_id ORDER BY task_cnt DESC LIMIT 20
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-051/attempt-01/sql/S6.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-051/attempt-01/sql/S6.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-051/attempt-01/results/S6.rows.jsonl)；完整：True；SHA256：`5ed2dff61fe0767ece3cef753f9f59176ae0d7947a5b62dcdbcdc23e60e4549f`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "asana__task_lifecycle_analysis", "kind": "base", "block": null, "base_tables": ["asana__task_lifecycle_analysis"]}] | [] | ["team_id"] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |
| B1 | COUNT(DISTINCT assignee_user_id) | [{"table": "asana__task_lifecycle_analysis", "column": "assignee_user_id"}] | [] | False |
| B1 | COUNT(*) FILTER(WHERE is_completed = 1) | [] | [{"table": "asana__task_lifecycle_analysis", "column": "is_completed"}] | True |


## S7

类别 `data`；来源 `query_db`；调用 `58b0697c58864906936601cf14ba23cd`；状态 `success`。

```sql
SELECT COUNT(*) AS slow_user_count FROM asana__user
WHERE avg_close_time_assigned_days > (SELECT 1.5*AVG(avg_close_time_assigned_days) FROM asana__user)
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-051/attempt-01/sql/S7.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-051/attempt-01/sql/S7.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-051/attempt-01/results/S7.rows.jsonl)；完整：True；SHA256：`2a754072b022df556c621f749199d09e057cbc139ceb3a4723cda565dc5c2916`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "asana__user", "kind": "base", "block": null, "base_tables": ["asana__user"]}] | [] | [] |
| B2 | [{"alias": "asana__user", "kind": "base", "block": null, "base_tables": ["asana__user"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | AVG(avg_close_time_assigned_days) | [{"table": "asana__user", "column": "avg_close_time_assigned_days"}] | [] | False |
| B2 | COUNT(*) | [] | [] | True |


## S8

类别 `data`；来源 `query_db`；调用 `d5dc52d1c0f042fea8cdcd5be0890d78`；状态 `success`。

```sql
SELECT u.user_id, u.user_name, u.avg_close_time_assigned_days,
u.number_of_open_tasks, u.number_of_tasks_completed
FROM asana__user u
WHERE u.avg_close_time_assigned_days > (SELECT 1.5*AVG(avg_close_time_assigned_days) FROM asana__user)
ORDER BY u.avg_close_time_assigned_days DESC
LIMIT 30
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-051/attempt-01/sql/S8.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-051/attempt-01/sql/S8.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-051/attempt-01/results/S8.rows.jsonl)；完整：True；SHA256：`df2be3f5810c241a64a721da5f0244287c705d289160a1c14f4adef58656e7c1`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "asana__user", "kind": "base", "block": null, "base_tables": ["asana__user"]}] | [] | [] |
| B2 | [{"alias": "u", "kind": "base", "block": null, "base_tables": ["asana__user"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | AVG(avg_close_time_assigned_days) | [{"table": "asana__user", "column": "avg_close_time_assigned_days"}] | [] | False |


## S9

类别 `data`；来源 `query_db`；调用 `5e105c43d06b43ffabc4b07ce7ce101a`；状态 `success`。

```sql
SELECT COUNT(*) AS matched FROM asana__task_lifecycle_analysis t JOIN asana__user u ON CAST(t.assignee_user_id AS TEXT) = u.user_id
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-051/attempt-01/sql/S9.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-051/attempt-01/sql/S9.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-051/attempt-01/results/S9.rows.jsonl)；完整：True；SHA256：`74ce3ada7c3b847c4a73a7224c18d4fd751609fda6bba0cf2119197e18aeee72`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "t", "kind": "base", "block": null, "base_tables": ["asana__task_lifecycle_analysis"]}, {"alias": "u", "kind": "base", "block": null, "base_tables": ["asana__user"]}] | [{"type": "INNER", "right": "asana__user AS u", "on": "CAST(t.assignee_user_id AS TEXT) = u.user_id", "using": []}] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |


## S10

类别 `data`；来源 `query_db`；调用 `c98656748da74f40a4e89a50b7154b55`；状态 `success`。

```sql
SELECT COUNT(*) AS unmatched, COUNT(DISTINCT assignee_user_id) AS uniq_unmatched
FROM asana__task_lifecycle_analysis t LEFT JOIN asana__user u ON CAST(t.assignee_user_id AS TEXT) = u.user_id
WHERE u.user_id IS NULL
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-051/attempt-01/sql/S10.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-051/attempt-01/sql/S10.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-051/attempt-01/results/S10.rows.jsonl)；完整：True；SHA256：`84a4ed820012fd28ec81afc11ae8d5967df878e8089c62a1b8becffaf9421310`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "t", "kind": "base", "block": null, "base_tables": ["asana__task_lifecycle_analysis"]}, {"alias": "u", "kind": "base", "block": null, "base_tables": ["asana__user"]}] | [{"type": "LEFT", "right": "asana__user AS u", "on": "CAST(t.assignee_user_id AS TEXT) = u.user_id", "using": []}] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |
| B1 | COUNT(DISTINCT assignee_user_id) | [{"table": "asana__task_lifecycle_analysis", "column": "assignee_user_id"}] | [] | False |


## S11

类别 `data`；来源 `query_db`；调用 `7eb3274b1ce84dcd80ee0af3959e6573`；状态 `success`。

```sql
SELECT
  COUNT(*) AS slow_tasks,
  SUM(CASE WHEN is_completed=1 THEN 1 ELSE 0 END) AS slow_completed,
  ROUND(AVG(complexity_score),3) AS avg_complexity,
  ROUND(AVG(urgency_score),3) AS avg_urgency,
  ROUND(AVG(project_health_score),3) AS avg_project_health,
  ROUND(AVG(hours_assigned_to_completion),2) AS avg_hours_atc,
  ROUND(AVG(avg_daily_activity_rate),4) AS avg_daily_activity
FROM asana__task_lifecycle_analysis t
JOIN asana__user u ON CAST(t.assignee_user_id AS TEXT) = u.user_id
WHERE u.avg_close_time_assigned_days > (SELECT 1.5*AVG(avg_close_time_assigned_days) FROM asana__user)
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-051/attempt-01/sql/S11.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-051/attempt-01/sql/S11.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-051/attempt-01/results/S11.rows.jsonl)；完整：True；SHA256：`472ab64ff39c427ad15001cc8375b07ed9cfdc277d0555438b8e690f280a16bc`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "asana__user", "kind": "base", "block": null, "base_tables": ["asana__user"]}] | [] | [] |
| B2 | [{"alias": "t", "kind": "base", "block": null, "base_tables": ["asana__task_lifecycle_analysis"]}, {"alias": "u", "kind": "base", "block": null, "base_tables": ["asana__user"]}] | [{"type": "INNER", "right": "asana__user AS u", "on": "CAST(t.assignee_user_id AS TEXT) = u.user_id", "using": []}] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | AVG(avg_close_time_assigned_days) | [{"table": "asana__user", "column": "avg_close_time_assigned_days"}] | [] | False |
| B2 | COUNT(*) | [] | [] | True |
| B2 | SUM(CASE WHEN is_completed = 1 THEN 1 ELSE 0 END) | [] | [{"table": "asana__task_lifecycle_analysis", "column": "is_completed"}] | False |
| B2 | AVG(complexity_score) | [{"table": "asana__task_lifecycle_analysis", "column": "complexity_score"}] | [] | False |
| B2 | AVG(urgency_score) | [{"table": "asana__task_lifecycle_analysis", "column": "urgency_score"}] | [] | False |
| B2 | AVG(project_health_score) | [{"table": "asana__task_lifecycle_analysis", "column": "project_health_score"}] | [] | False |
| B2 | AVG(hours_assigned_to_completion) | [{"table": "asana__task_lifecycle_analysis", "column": "hours_assigned_to_completion"}] | [] | False |
| B2 | AVG(avg_daily_activity_rate) | [{"table": "asana__task_lifecycle_analysis", "column": "avg_daily_activity_rate"}] | [] | False |


## S12

类别 `data`；来源 `query_db`；调用 `ee5be455cf59424ab6922eaf0ef23c6e`；状态 `success`。

```sql
SELECT
  COUNT(*) AS fast_tasks,
  SUM(CASE WHEN is_completed=1 THEN 1 ELSE 0 END) AS fast_completed,
  ROUND(AVG(complexity_score),3) AS avg_complexity,
  ROUND(AVG(urgency_score),3) AS avg_urgency,
  ROUND(AVG(project_health_score),3) AS avg_project_health,
  ROUND(AVG(hours_assigned_to_completion),2) AS avg_hours_atc,
  ROUND(AVG(avg_daily_activity_rate),4) AS avg_daily_activity
FROM asana__task_lifecycle_analysis t
JOIN asana__user u ON CAST(t.assignee_user_id AS TEXT) = u.user_id
WHERE u.avg_close_time_assigned_days <= (SELECT 1.5*AVG(avg_close_time_assigned_days) FROM asana__user)
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-051/attempt-01/sql/S12.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-051/attempt-01/sql/S12.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-051/attempt-01/results/S12.rows.jsonl)；完整：True；SHA256：`341c0b1de1a66a5c11b7bd0634604d8b122b17b0d04855962d9e372a6fb0f149`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "asana__user", "kind": "base", "block": null, "base_tables": ["asana__user"]}] | [] | [] |
| B2 | [{"alias": "t", "kind": "base", "block": null, "base_tables": ["asana__task_lifecycle_analysis"]}, {"alias": "u", "kind": "base", "block": null, "base_tables": ["asana__user"]}] | [{"type": "INNER", "right": "asana__user AS u", "on": "CAST(t.assignee_user_id AS TEXT) = u.user_id", "using": []}] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | AVG(avg_close_time_assigned_days) | [{"table": "asana__user", "column": "avg_close_time_assigned_days"}] | [] | False |
| B2 | COUNT(*) | [] | [] | True |
| B2 | SUM(CASE WHEN is_completed = 1 THEN 1 ELSE 0 END) | [] | [{"table": "asana__task_lifecycle_analysis", "column": "is_completed"}] | False |
| B2 | AVG(complexity_score) | [{"table": "asana__task_lifecycle_analysis", "column": "complexity_score"}] | [] | False |
| B2 | AVG(urgency_score) | [{"table": "asana__task_lifecycle_analysis", "column": "urgency_score"}] | [] | False |
| B2 | AVG(project_health_score) | [{"table": "asana__task_lifecycle_analysis", "column": "project_health_score"}] | [] | False |
| B2 | AVG(hours_assigned_to_completion) | [{"table": "asana__task_lifecycle_analysis", "column": "hours_assigned_to_completion"}] | [] | False |
| B2 | AVG(avg_daily_activity_rate) | [{"table": "asana__task_lifecycle_analysis", "column": "avg_daily_activity_rate"}] | [] | False |


## S13

类别 `data`；来源 `query_db`；调用 `76785a06db3e4a659ace9b601023cf2b`；状态 `success`。

```sql
SELECT complexity_score, COUNT(*) AS cnt,
ROUND(100.0*COUNT(*)/SUM(COUNT(*)) OVER(),2) AS pct
FROM asana__task_lifecycle_analysis t
JOIN asana__user u ON CAST(t.assignee_user_id AS TEXT) = u.user_id
WHERE u.avg_close_time_assigned_days > (SELECT 1.5*AVG(avg_close_time_assigned_days) FROM asana__user)
GROUP BY complexity_score ORDER BY complexity_score
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-051/attempt-01/sql/S13.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-051/attempt-01/sql/S13.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-051/attempt-01/results/S13.rows.jsonl)；完整：True；SHA256：`86bfb89d7ce454c4f8e501459bfe7b9a66b503ef1ea7db3019b631159de4edc2`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "asana__user", "kind": "base", "block": null, "base_tables": ["asana__user"]}] | [] | [] |
| B2 | [{"alias": "t", "kind": "base", "block": null, "base_tables": ["asana__task_lifecycle_analysis"]}, {"alias": "u", "kind": "base", "block": null, "base_tables": ["asana__user"]}] | [{"type": "INNER", "right": "asana__user AS u", "on": "CAST(t.assignee_user_id AS TEXT) = u.user_id", "using": []}] | ["complexity_score"] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | AVG(avg_close_time_assigned_days) | [{"table": "asana__user", "column": "avg_close_time_assigned_days"}] | [] | False |
| B2 | COUNT(*) | [] | [] | True |
| B2 | COUNT(*) | [] | [] | True |
| B2 | COUNT(*) | [] | [] | True |


## S14

类别 `data`；来源 `query_db`；调用 `1661ea9f81a040c6bc0d9efb0b499b80`；状态 `success`。

```sql
SELECT urgency_score, COUNT(*) AS cnt,
ROUND(100.0*COUNT(*)/SUM(COUNT(*)) OVER(),2) AS pct
FROM asana__task_lifecycle_analysis t
JOIN asana__user u ON CAST(t.assignee_user_id AS TEXT) = u.user_id
WHERE u.avg_close_time_assigned_days > (SELECT 1.5*AVG(avg_close_time_assigned_days) FROM asana__user)
GROUP BY urgency_score ORDER BY urgency_score
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-051/attempt-01/sql/S14.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-051/attempt-01/sql/S14.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-051/attempt-01/results/S14.rows.jsonl)；完整：True；SHA256：`55862b33b0f707afa1a71eb4f430423ada784f873be381ce180aa62744849300`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "asana__user", "kind": "base", "block": null, "base_tables": ["asana__user"]}] | [] | [] |
| B2 | [{"alias": "t", "kind": "base", "block": null, "base_tables": ["asana__task_lifecycle_analysis"]}, {"alias": "u", "kind": "base", "block": null, "base_tables": ["asana__user"]}] | [{"type": "INNER", "right": "asana__user AS u", "on": "CAST(t.assignee_user_id AS TEXT) = u.user_id", "using": []}] | ["urgency_score"] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | AVG(avg_close_time_assigned_days) | [{"table": "asana__user", "column": "avg_close_time_assigned_days"}] | [] | False |
| B2 | COUNT(*) | [] | [] | True |
| B2 | COUNT(*) | [] | [] | True |
| B2 | COUNT(*) | [] | [] | True |


## S15

类别 `data`；来源 `query_db`；调用 `70447af463f9496dabf28ba42b11f89b`；状态 `success`。

```sql
SELECT project_health_score, COUNT(*) AS cnt,
ROUND(100.0*COUNT(*)/SUM(COUNT(*)) OVER(),2) AS pct
FROM asana__task_lifecycle_analysis t
JOIN asana__user u ON CAST(t.assignee_user_id AS TEXT) = u.user_id
WHERE u.avg_close_time_assigned_days > (SELECT 1.5*AVG(avg_close_time_assigned_days) FROM asana__user)
GROUP BY project_health_score ORDER BY project_health_score
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-051/attempt-01/sql/S15.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-051/attempt-01/sql/S15.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-051/attempt-01/results/S15.rows.jsonl)；完整：True；SHA256：`0c3bfd0d371cf56875433d372636be98bbad6c082837f28d6c8c69623b25c63b`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "asana__user", "kind": "base", "block": null, "base_tables": ["asana__user"]}] | [] | [] |
| B2 | [{"alias": "t", "kind": "base", "block": null, "base_tables": ["asana__task_lifecycle_analysis"]}, {"alias": "u", "kind": "base", "block": null, "base_tables": ["asana__user"]}] | [{"type": "INNER", "right": "asana__user AS u", "on": "CAST(t.assignee_user_id AS TEXT) = u.user_id", "using": []}] | ["project_health_score"] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | AVG(avg_close_time_assigned_days) | [{"table": "asana__user", "column": "avg_close_time_assigned_days"}] | [] | False |
| B2 | COUNT(*) | [] | [] | True |
| B2 | COUNT(*) | [] | [] | True |
| B2 | COUNT(*) | [] | [] | True |


## S16

类别 `data`；来源 `query_db`；调用 `029c6f44b3bd4654b90f0ee4281bed83`；状态 `success`。

```sql
SELECT team_id, COUNT(*) AS total_tasks,
SUM(CASE WHEN is_completed=1 THEN 1 ELSE 0 END) AS completed_tasks,
ROUND(100.0*SUM(CASE WHEN is_completed=1 THEN 1 ELSE 0 END)/COUNT(*),2) AS completion_rate,
ROUND(AVG(project_health_score),2) AS avg_project_health,
ROUND(AVG(complexity_score),2) AS avg_complexity,
ROUND(AVG(urgency_score),2) AS avg_urgency,
ROUND(AVG(hours_assigned_to_completion),1) AS avg_hours_atc,
COUNT(DISTINCT assignee_user_id) AS n_users
FROM asana__task_lifecycle_analysis
WHERE is_valid_record=1
GROUP BY team_id
ORDER BY completion_rate ASC
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-051/attempt-01/sql/S16.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-051/attempt-01/sql/S16.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-051/attempt-01/results/S16.rows.jsonl)；完整：True；SHA256：`9468a6d917890053e315591f939f04e932fc4fb015bcb9e21f744475bd0c7383`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "asana__task_lifecycle_analysis", "kind": "base", "block": null, "base_tables": ["asana__task_lifecycle_analysis"]}] | [] | ["team_id"] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |
| B1 | SUM(CASE WHEN is_completed = 1 THEN 1 ELSE 0 END) | [] | [{"table": "asana__task_lifecycle_analysis", "column": "is_completed"}] | False |
| B1 | COUNT(DISTINCT assignee_user_id) | [{"table": "asana__task_lifecycle_analysis", "column": "assignee_user_id"}] | [] | False |
| B1 | AVG(project_health_score) | [{"table": "asana__task_lifecycle_analysis", "column": "project_health_score"}] | [] | False |
| B1 | AVG(complexity_score) | [{"table": "asana__task_lifecycle_analysis", "column": "complexity_score"}] | [] | False |
| B1 | AVG(urgency_score) | [{"table": "asana__task_lifecycle_analysis", "column": "urgency_score"}] | [] | False |
| B1 | AVG(hours_assigned_to_completion) | [{"table": "asana__task_lifecycle_analysis", "column": "hours_assigned_to_completion"}] | [] | False |
| B1 | COUNT(*) | [] | [] | True |
| B1 | SUM(CASE WHEN is_completed = 1 THEN 1 ELSE 0 END) | [] | [{"table": "asana__task_lifecycle_analysis", "column": "is_completed"}] | False |


## S17

类别 `data`；来源 `query_db`；调用 `1c1240aee2da455ca9d3428837bd5144`；状态 `success`。

```sql
SELECT ROUND(100.0*SUM(CASE WHEN is_completed=1 THEN 1 ELSE 0 END)/COUNT(*),2) AS overall_completion_rate,
ROUND(AVG(project_health_score),2) AS overall_avg_health,
ROUND(AVG(complexity_score),2) AS overall_avg_complexity,
ROUND(AVG(urgency_score),2) AS overall_avg_urgency
FROM asana__task_lifecycle_analysis WHERE is_valid_record=1
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-051/attempt-01/sql/S17.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-051/attempt-01/sql/S17.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-051/attempt-01/results/S17.rows.jsonl)；完整：True；SHA256：`16f90faeea0a6216a6f96ecabeba7b80edf5c17d3ead2aa9c7ac0942dc5e872e`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "asana__task_lifecycle_analysis", "kind": "base", "block": null, "base_tables": ["asana__task_lifecycle_analysis"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | AVG(project_health_score) | [{"table": "asana__task_lifecycle_analysis", "column": "project_health_score"}] | [] | False |
| B1 | AVG(complexity_score) | [{"table": "asana__task_lifecycle_analysis", "column": "complexity_score"}] | [] | False |
| B1 | AVG(urgency_score) | [{"table": "asana__task_lifecycle_analysis", "column": "urgency_score"}] | [] | False |
| B1 | COUNT(*) | [] | [] | True |
| B1 | SUM(CASE WHEN is_completed = 1 THEN 1 ELSE 0 END) | [] | [{"table": "asana__task_lifecycle_analysis", "column": "is_completed"}] | False |


## S18

类别 `data`；来源 `query_db`；调用 `42560669b0b441b5827b09ac7f0eb220`；状态 `success`。

```sql
SELECT team_id, total_tasks, completed_tasks, completion_rate, avg_project_health,
avg_hours_atc, n_users
FROM (
  SELECT team_id, COUNT(*) AS total_tasks,
  SUM(CASE WHEN is_completed=1 THEN 1 ELSE 0 END) AS completed_tasks,
  ROUND(100.0*SUM(CASE WHEN is_completed=1 THEN 1 ELSE 0 END)/COUNT(*),2) AS completion_rate,
  ROUND(AVG(project_health_score),2) AS avg_project_health,
  ROUND(AVG(hours_assigned_to_completion),1) AS avg_hours_atc,
  COUNT(DISTINCT assignee_user_id) AS n_users
  FROM asana__task_lifecycle_analysis
  WHERE is_valid_record=1
  GROUP BY team_id
)
ORDER BY completion_rate DESC
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-051/attempt-01/sql/S18.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-051/attempt-01/sql/S18.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-051/attempt-01/results/S18.rows.jsonl)；完整：True；SHA256：`fc96a6a467838e61468be0713533f7b7e72a1fa3dfc1ac7a23af9a1cbe158145`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "asana__task_lifecycle_analysis", "kind": "base", "block": null, "base_tables": ["asana__task_lifecycle_analysis"]}] | [] | ["team_id"] |
| B2 | [{"alias": "", "kind": "derived", "block": "B1", "base_tables": ["asana__task_lifecycle_analysis"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |
| B1 | SUM(CASE WHEN is_completed = 1 THEN 1 ELSE 0 END) | [] | [{"table": "asana__task_lifecycle_analysis", "column": "is_completed"}] | False |
| B1 | COUNT(DISTINCT assignee_user_id) | [{"table": "asana__task_lifecycle_analysis", "column": "assignee_user_id"}] | [] | False |
| B1 | AVG(project_health_score) | [{"table": "asana__task_lifecycle_analysis", "column": "project_health_score"}] | [] | False |
| B1 | AVG(hours_assigned_to_completion) | [{"table": "asana__task_lifecycle_analysis", "column": "hours_assigned_to_completion"}] | [] | False |
| B1 | COUNT(*) | [] | [] | True |
| B1 | SUM(CASE WHEN is_completed = 1 THEN 1 ELSE 0 END) | [] | [{"table": "asana__task_lifecycle_analysis", "column": "is_completed"}] | False |


## S19

类别 `data`；来源 `query_db`；调用 `5f0ce7d47de94c3f85505a030f331b58`；状态 `success`。

```sql
SELECT t.team_id, COUNT(*) AS total_tasks,
SUM(CASE WHEN t.is_completed=1 THEN 1 ELSE 0 END) AS completed_tasks,
ROUND(100.0*SUM(CASE WHEN t.is_completed=1 THEN 1 ELSE 0 END)/COUNT(*),2) AS completion_rate,
ROUND(AVG(t.project_health_score),2) AS avg_project_health,
ROUND(AVG(t.hours_assigned_to_completion),1) AS avg_hours_atc,
COUNT(DISTINCT t.assignee_user_id) AS n_users,
COUNT(DISTINCT CASE WHEN u.avg_close_time_assigned_days > (SELECT 1.5*AVG(avg_close_time_assigned_days) FROM asana__user) THEN t.assignee_user_id END) AS slow_users_cnt,
ROUND(100.0*COUNT(DISTINCT CASE WHEN u.avg_close_time_assigned_days > (SELECT 1.5*AVG(avg_close_time_assigned_days) FROM asana__user) THEN t.assignee_user_id END)/NULLIF(COUNT(DISTINCT t.assignee_user_id),0),2) AS slow_user_pct
FROM asana__task_lifecycle_analysis t
LEFT JOIN asana__user u ON CAST(t.assignee_user_id AS TEXT) = u.user_id
WHERE t.is_valid_record=1
GROUP BY t.team_id
ORDER BY completion_rate ASC
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-051/attempt-01/sql/S19.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-051/attempt-01/sql/S19.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-051/attempt-01/results/S19.rows.jsonl)；完整：True；SHA256：`4d01df33910326a89d99a7c7d7693e5d26087c8ade9ddf62f55610fc4e3016e8`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "asana__user", "kind": "base", "block": null, "base_tables": ["asana__user"]}] | [] | [] |
| B2 | [{"alias": "asana__user", "kind": "base", "block": null, "base_tables": ["asana__user"]}] | [] | [] |
| B3 | [{"alias": "t", "kind": "base", "block": null, "base_tables": ["asana__task_lifecycle_analysis"]}, {"alias": "u", "kind": "base", "block": null, "base_tables": ["asana__user"]}] | [{"type": "LEFT", "right": "asana__user AS u", "on": "CAST(t.assignee_user_id AS TEXT) = u.user_id", "using": []}] | ["t.team_id"] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | AVG(avg_close_time_assigned_days) | [{"table": "asana__user", "column": "avg_close_time_assigned_days"}] | [] | False |
| B2 | AVG(avg_close_time_assigned_days) | [{"table": "asana__user", "column": "avg_close_time_assigned_days"}] | [] | False |
| B3 | COUNT(*) | [] | [] | True |
| B3 | SUM(CASE WHEN t.is_completed = 1 THEN 1 ELSE 0 END) | [] | [{"table": "asana__task_lifecycle_analysis", "column": "is_completed"}] | False |
| B3 | COUNT(DISTINCT t.assignee_user_id) | [{"table": "asana__task_lifecycle_analysis", "column": "assignee_user_id"}] | [] | False |
| B3 | COUNT(DISTINCT CASE WHEN u.avg_close_time_assigned_days > (SELECT 1.5 * AVG(avg_close_time_assigned_days) FROM asana__user) THEN t.assignee_user_id END) | [{"table": "asana__task_lifecycle_analysis", "column": "assignee_user_id"}] | [{"table": "asana__user", "column": "avg_close_time_assigned_days"}, {"table": "asana__user", "column": "avg_close_time_assigned_days"}] | False |
| B3 | AVG(t.project_health_score) | [{"table": "asana__task_lifecycle_analysis", "column": "project_health_score"}] | [] | False |
| B3 | AVG(t.hours_assigned_to_completion) | [{"table": "asana__task_lifecycle_analysis", "column": "hours_assigned_to_completion"}] | [] | False |
| B3 | COUNT(*) | [] | [] | True |
| B3 | SUM(CASE WHEN t.is_completed = 1 THEN 1 ELSE 0 END) | [] | [{"table": "asana__task_lifecycle_analysis", "column": "is_completed"}] | False |
| B3 | COUNT(DISTINCT CASE WHEN u.avg_close_time_assigned_days > (SELECT 1.5 * AVG(avg_close_time_assigned_days) FROM asana__user) THEN t.assignee_user_id END) | [{"table": "asana__task_lifecycle_analysis", "column": "assignee_user_id"}] | [{"table": "asana__user", "column": "avg_close_time_assigned_days"}, {"table": "asana__user", "column": "avg_close_time_assigned_days"}] | False |
| B3 | COUNT(DISTINCT t.assignee_user_id) | [{"table": "asana__task_lifecycle_analysis", "column": "assignee_user_id"}] | [] | False |


## S20

类别 `data`；来源 `query_db`；调用 `fb32bb71f9034206856b03a2b5a70462`；状态 `success`。

```sql
SELECT
  CASE WHEN u.avg_close_time_assigned_days > (SELECT 1.5*AVG(avg_close_time_assigned_days) FROM asana__user) THEN 'SLOW' ELSE 'FAST' END AS cohort,
  COUNT(*) AS tasks,
  ROUND(AVG(t.hours_to_assignment),2) AS avg_hours_to_assign,
  ROUND(AVG(t.hours_assigned_to_completion),2) AS avg_hours_atc,
  ROUND(AVG(t.total_lifecycle_hours),2) AS avg_lifecycle_hours,
  ROUND(AVG(t.total_story_events),2) AS avg_story_events,
  ROUND(AVG(t.unique_action_types),2) AS avg_action_types,
  ROUND(AVG(t.days_with_activity),2) AS avg_activity_days,
  ROUND(AVG(t.avg_daily_activity_rate),3) AS avg_daily_activity_rate,
  ROUND(AVG(t.delay_days),2) AS avg_delay_days,
  ROUND(AVG(t.response_time_days),2) AS avg_response_days
FROM asana__task_lifecycle_analysis t
JOIN asana__user u ON CAST(t.assignee_user_id AS TEXT) = u.user_id
WHERE t.is_valid_record=1
GROUP BY cohort
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-051/attempt-01/sql/S20.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-051/attempt-01/sql/S20.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-051/attempt-01/results/S20.rows.jsonl)；完整：True；SHA256：`d8490d67768b6e2272bedeb25aa69154efffb0a41ce06ef42f20cf1fec862b5b`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "asana__user", "kind": "base", "block": null, "base_tables": ["asana__user"]}] | [] | [] |
| B2 | [{"alias": "t", "kind": "base", "block": null, "base_tables": ["asana__task_lifecycle_analysis"]}, {"alias": "u", "kind": "base", "block": null, "base_tables": ["asana__user"]}] | [{"type": "INNER", "right": "asana__user AS u", "on": "CAST(t.assignee_user_id AS TEXT) = u.user_id", "using": []}] | ["CASE WHEN u.avg_close_time_assigned_days > (SELECT 1.5 * AVG(avg_close_time_assigned_days) FROM asana__user) THEN 'SLOW' ELSE 'FAST' END"] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | AVG(avg_close_time_assigned_days) | [{"table": "asana__user", "column": "avg_close_time_assigned_days"}] | [] | False |
| B2 | COUNT(*) | [] | [] | True |
| B2 | AVG(t.hours_to_assignment) | [{"table": "asana__task_lifecycle_analysis", "column": "hours_to_assignment"}] | [] | False |
| B2 | AVG(t.hours_assigned_to_completion) | [{"table": "asana__task_lifecycle_analysis", "column": "hours_assigned_to_completion"}] | [] | False |
| B2 | AVG(t.total_lifecycle_hours) | [{"table": "asana__task_lifecycle_analysis", "column": "total_lifecycle_hours"}] | [] | False |
| B2 | AVG(t.total_story_events) | [{"table": "asana__task_lifecycle_analysis", "column": "total_story_events"}] | [] | False |
| B2 | AVG(t.unique_action_types) | [{"table": "asana__task_lifecycle_analysis", "column": "unique_action_types"}] | [] | False |
| B2 | AVG(t.days_with_activity) | [{"table": "asana__task_lifecycle_analysis", "column": "days_with_activity"}] | [] | False |
| B2 | AVG(t.avg_daily_activity_rate) | [{"table": "asana__task_lifecycle_analysis", "column": "avg_daily_activity_rate"}] | [] | False |
| B2 | AVG(t.delay_days) | [{"table": "asana__task_lifecycle_analysis", "column": "delay_days"}] | [] | False |
| B2 | AVG(t.response_time_days) | [{"table": "asana__task_lifecycle_analysis", "column": "response_time_days"}] | [] | False |


## S21

类别 `data`；来源 `query_db`；调用 `9a5d9bb51df44c7f90eb935f5a6520e2`；状态 `success`。

```sql
SELECT
  CASE WHEN u.avg_close_time_assigned_days > (SELECT 1.5*AVG(avg_close_time_assigned_days) FROM asana__user) THEN 'SLOW' ELSE 'FAST' END AS cohort,
  t.task_status_category, COUNT(*) AS cnt
FROM asana__task_lifecycle_analysis t
JOIN asana__user u ON CAST(t.assignee_user_id AS TEXT) = u.user_id
WHERE t.is_valid_record=1
GROUP BY cohort, t.task_status_category
ORDER BY cohort, cnt DESC
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-051/attempt-01/sql/S21.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-051/attempt-01/sql/S21.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-051/attempt-01/results/S21.rows.jsonl)；完整：True；SHA256：`c47a6431a6de541126985f2b034b8a8fae8968658b66499b08d9e54deffeebf1`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "asana__user", "kind": "base", "block": null, "base_tables": ["asana__user"]}] | [] | [] |
| B2 | [{"alias": "t", "kind": "base", "block": null, "base_tables": ["asana__task_lifecycle_analysis"]}, {"alias": "u", "kind": "base", "block": null, "base_tables": ["asana__user"]}] | [{"type": "INNER", "right": "asana__user AS u", "on": "CAST(t.assignee_user_id AS TEXT) = u.user_id", "using": []}] | ["CASE WHEN u.avg_close_time_assigned_days > (SELECT 1.5 * AVG(avg_close_time_assigned_days) FROM asana__user) THEN 'SLOW' ELSE 'FAST' END", "t.task_status_category"] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | AVG(avg_close_time_assigned_days) | [{"table": "asana__user", "column": "avg_close_time_assigned_days"}] | [] | False |
| B2 | COUNT(*) | [] | [] | True |


## S22

类别 `data`；来源 `query_db`；调用 `31f1525624c0421bbb048901af5a2f16`；状态 `success`。

```sql
SELECT
  CASE WHEN u.avg_close_time_assigned_days > (SELECT 1.5*AVG(avg_close_time_assigned_days) FROM asana__user) THEN 'SLOW' ELSE 'FAST' END AS cohort,
  t.assignee_performance_grade, COUNT(*) AS cnt
FROM asana__task_lifecycle_analysis t
JOIN asana__user u ON CAST(t.assignee_user_id AS TEXT) = u.user_id
WHERE t.is_valid_record=1
GROUP BY cohort, t.assignee_performance_grade
ORDER BY cohort, cnt DESC
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-051/attempt-01/sql/S22.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-051/attempt-01/sql/S22.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-051/attempt-01/results/S22.rows.jsonl)；完整：True；SHA256：`136d5ed1c670f2be4ffea45b7d30aa9d060363626b694d59a610bc50ac5fd2fe`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "asana__user", "kind": "base", "block": null, "base_tables": ["asana__user"]}] | [] | [] |
| B2 | [{"alias": "t", "kind": "base", "block": null, "base_tables": ["asana__task_lifecycle_analysis"]}, {"alias": "u", "kind": "base", "block": null, "base_tables": ["asana__user"]}] | [{"type": "INNER", "right": "asana__user AS u", "on": "CAST(t.assignee_user_id AS TEXT) = u.user_id", "using": []}] | ["CASE WHEN u.avg_close_time_assigned_days > (SELECT 1.5 * AVG(avg_close_time_assigned_days) FROM asana__user) THEN 'SLOW' ELSE 'FAST' END", "t.assignee_performance_grade"] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | AVG(avg_close_time_assigned_days) | [{"table": "asana__user", "column": "avg_close_time_assigned_days"}] | [] | False |
| B2 | COUNT(*) | [] | [] | True |


## S23

类别 `data`；来源 `query_db`；调用 `e574fd405bbd4708a81834b73767cc41`；状态 `success`。

```sql
SELECT
  CASE WHEN u.avg_close_time_assigned_days > (SELECT 1.5*AVG(avg_close_time_assigned_days) FROM asana__user) THEN 'SLOW' ELSE 'FAST' END AS cohort,
  t.complexity_execution_match, COUNT(*) AS cnt
FROM asana__task_lifecycle_analysis t
JOIN asana__user u ON CAST(t.assignee_user_id AS TEXT) = u.user_id
WHERE t.is_valid_record=1
GROUP BY cohort, t.complexity_execution_match
ORDER BY cohort, cnt DESC
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-051/attempt-01/sql/S23.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-051/attempt-01/sql/S23.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-051/attempt-01/results/S23.rows.jsonl)；完整：True；SHA256：`499d2dadb35cd37a13f3ecd2fd0f44f41c79647f38dae471a7fc0ac427da6188`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "asana__user", "kind": "base", "block": null, "base_tables": ["asana__user"]}] | [] | [] |
| B2 | [{"alias": "t", "kind": "base", "block": null, "base_tables": ["asana__task_lifecycle_analysis"]}, {"alias": "u", "kind": "base", "block": null, "base_tables": ["asana__user"]}] | [{"type": "INNER", "right": "asana__user AS u", "on": "CAST(t.assignee_user_id AS TEXT) = u.user_id", "using": []}] | ["CASE WHEN u.avg_close_time_assigned_days > (SELECT 1.5 * AVG(avg_close_time_assigned_days) FROM asana__user) THEN 'SLOW' ELSE 'FAST' END", "t.complexity_execution_match"] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | AVG(avg_close_time_assigned_days) | [{"table": "asana__user", "column": "avg_close_time_assigned_days"}] | [] | False |
| B2 | COUNT(*) | [] | [] | True |


## S24

类别 `data`；来源 `query_db`；调用 `53f2ee80c51f49ae95af679e98cc5cb5`；状态 `success`。

```sql
SELECT
  CASE WHEN u.avg_close_time_assigned_days > (SELECT 1.5*AVG(avg_close_time_assigned_days) FROM asana__user) THEN 'SLOW' ELSE 'FAST' END AS cohort,
  t.relative_performance_vs_project, COUNT(*) AS cnt
FROM asana__task_lifecycle_analysis t
JOIN asana__user u ON CAST(t.assignee_user_id AS TEXT) = u.user_id
WHERE t.is_valid_record=1
GROUP BY cohort, t.relative_performance_vs_project
ORDER BY cohort, cnt DESC
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-051/attempt-01/sql/S24.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-051/attempt-01/sql/S24.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-051/attempt-01/results/S24.rows.jsonl)；完整：True；SHA256：`72202cd328fb6e270a261b24b210e175cdaffe5c013dee35a4825a2705bc2a6c`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "asana__user", "kind": "base", "block": null, "base_tables": ["asana__user"]}] | [] | [] |
| B2 | [{"alias": "t", "kind": "base", "block": null, "base_tables": ["asana__task_lifecycle_analysis"]}, {"alias": "u", "kind": "base", "block": null, "base_tables": ["asana__user"]}] | [{"type": "INNER", "right": "asana__user AS u", "on": "CAST(t.assignee_user_id AS TEXT) = u.user_id", "using": []}] | ["CASE WHEN u.avg_close_time_assigned_days > (SELECT 1.5 * AVG(avg_close_time_assigned_days) FROM asana__user) THEN 'SLOW' ELSE 'FAST' END", "t.relative_performance_vs_project"] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | AVG(avg_close_time_assigned_days) | [{"table": "asana__user", "column": "avg_close_time_assigned_days"}] | [] | False |
| B2 | COUNT(*) | [] | [] | True |


## S25

类别 `data`；来源 `query_db`；调用 `49fb7fe2ddf946788c0a52b990c6a047`；状态 `success`。

```sql
SELECT
  CASE WHEN u.avg_close_time_assigned_days > (SELECT 1.5*AVG(avg_close_time_assigned_days) FROM asana__user) THEN 'SLOW' ELSE 'FAST' END AS cohort,
  t.lifecycle_efficiency_category, COUNT(*) AS cnt
FROM asana__task_lifecycle_analysis t
JOIN asana__user u ON CAST(t.assignee_user_id AS TEXT) = u.user_id
WHERE t.is_valid_record=1
GROUP BY cohort, t.lifecycle_efficiency_category
ORDER BY cohort, cnt DESC
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-051/attempt-01/sql/S25.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-051/attempt-01/sql/S25.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-051/attempt-01/results/S25.rows.jsonl)；完整：True；SHA256：`5eef7d332de2284eef790ff5b65086648ec515a8d6119feeb5fed5a20d8af754`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "asana__user", "kind": "base", "block": null, "base_tables": ["asana__user"]}] | [] | [] |
| B2 | [{"alias": "t", "kind": "base", "block": null, "base_tables": ["asana__task_lifecycle_analysis"]}, {"alias": "u", "kind": "base", "block": null, "base_tables": ["asana__user"]}] | [{"type": "INNER", "right": "asana__user AS u", "on": "CAST(t.assignee_user_id AS TEXT) = u.user_id", "using": []}] | ["CASE WHEN u.avg_close_time_assigned_days > (SELECT 1.5 * AVG(avg_close_time_assigned_days) FROM asana__user) THEN 'SLOW' ELSE 'FAST' END", "t.lifecycle_efficiency_category"] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | AVG(avg_close_time_assigned_days) | [{"table": "asana__user", "column": "avg_close_time_assigned_days"}] | [] | False |
| B2 | COUNT(*) | [] | [] | True |


## S26

类别 `data`；来源 `query_db`；调用 `85cd0e05f3df47fea72ca9218774074f`；状态 `success`。

```sql
SELECT
  CASE WHEN u.avg_close_time_assigned_days > (SELECT 1.5*AVG(avg_close_time_assigned_days) FROM asana__user) THEN 'SLOW' ELSE 'FAST' END AS cohort,
  t.activity_level, COUNT(*) AS cnt
FROM asana__task_lifecycle_analysis t
JOIN asana__user u ON CAST(t.assignee_user_id AS TEXT) = u.user_id
WHERE t.is_valid_record=1
GROUP BY cohort, t.activity_level
ORDER BY cohort, cnt DESC
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-051/attempt-01/sql/S26.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-051/attempt-01/sql/S26.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-051/attempt-01/results/S26.rows.jsonl)；完整：True；SHA256：`5bf1559f45d990adfff113d2105c1ee108f413c24c7f35aaf58d11162423a278`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "asana__user", "kind": "base", "block": null, "base_tables": ["asana__user"]}] | [] | [] |
| B2 | [{"alias": "t", "kind": "base", "block": null, "base_tables": ["asana__task_lifecycle_analysis"]}, {"alias": "u", "kind": "base", "block": null, "base_tables": ["asana__user"]}] | [{"type": "INNER", "right": "asana__user AS u", "on": "CAST(t.assignee_user_id AS TEXT) = u.user_id", "using": []}] | ["CASE WHEN u.avg_close_time_assigned_days > (SELECT 1.5 * AVG(avg_close_time_assigned_days) FROM asana__user) THEN 'SLOW' ELSE 'FAST' END", "t.activity_level"] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | AVG(avg_close_time_assigned_days) | [{"table": "asana__user", "column": "avg_close_time_assigned_days"}] | [] | False |
| B2 | COUNT(*) | [] | [] | True |


## S27

类别 `data`；来源 `query_db`；调用 `72814969bdea4655b5589c2b49500642`；状态 `success`。

```sql
SELECT
  CASE WHEN u.avg_close_time_assigned_days > (SELECT 1.5*AVG(avg_close_time_assigned_days) FROM asana__user) THEN 'SLOW' ELSE 'FAST' END AS cohort,
  t.anomaly_patterns, COUNT(*) AS cnt
FROM asana__task_lifecycle_analysis t
JOIN asana__user u ON CAST(t.assignee_user_id AS TEXT) = u.user_id
WHERE t.is_valid_record=1
GROUP BY cohort, t.anomaly_patterns
ORDER BY cohort, cnt DESC
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-051/attempt-01/sql/S27.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-051/attempt-01/sql/S27.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-051/attempt-01/results/S27.rows.jsonl)；完整：True；SHA256：`36b61cb45ce6e94941923e5758eb5084957ec8cb925f12458192198a6109c839`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "asana__user", "kind": "base", "block": null, "base_tables": ["asana__user"]}] | [] | [] |
| B2 | [{"alias": "t", "kind": "base", "block": null, "base_tables": ["asana__task_lifecycle_analysis"]}, {"alias": "u", "kind": "base", "block": null, "base_tables": ["asana__user"]}] | [{"type": "INNER", "right": "asana__user AS u", "on": "CAST(t.assignee_user_id AS TEXT) = u.user_id", "using": []}] | ["CASE WHEN u.avg_close_time_assigned_days > (SELECT 1.5 * AVG(avg_close_time_assigned_days) FROM asana__user) THEN 'SLOW' ELSE 'FAST' END", "t.anomaly_patterns"] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | AVG(avg_close_time_assigned_days) | [{"table": "asana__user", "column": "avg_close_time_assigned_days"}] | [] | False |
| B2 | COUNT(*) | [] | [] | True |


## S28

类别 `data`；来源 `query_db`；调用 `c22c092ddf884b3a9c39e221a55dabac`；状态 `success`。

```sql
WITH slow_users AS (
  SELECT user_id FROM asana__user
  WHERE avg_close_time_assigned_days > (SELECT 1.5*AVG(avg_close_time_assigned_days) FROM asana__user)
)
SELECT
  CASE WHEN s.user_id IS NOT NULL THEN 'SLOW' ELSE 'FAST' END AS cohort,
  COUNT(*) AS n_users,
  ROUND(AVG(u.number_of_open_tasks),2) AS avg_open_tasks,
  ROUND(AVG(u.number_of_tasks_completed),2) AS avg_completed_tasks,
  ROUND(AVG(u.avg_close_time_assigned_days),2) AS avg_close_time_assigned
FROM asana__user u
LEFT JOIN slow_users s ON u.user_id = s.user_id
GROUP BY cohort
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-051/attempt-01/sql/S28.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-051/attempt-01/sql/S28.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-051/attempt-01/results/S28.rows.jsonl)；完整：True；SHA256：`e7897d0e4ee0eadb3d7cc3e380cdae016171af74e1be39f0711b1b5b56dc03eb`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "asana__user", "kind": "base", "block": null, "base_tables": ["asana__user"]}] | [] | [] |
| B2 | [{"alias": "asana__user", "kind": "base", "block": null, "base_tables": ["asana__user"]}] | [] | [] |
| B3 | [{"alias": "u", "kind": "base", "block": null, "base_tables": ["asana__user"]}, {"alias": "s", "kind": "derived", "block": "B2", "base_tables": ["asana__user"]}] | [{"type": "LEFT", "right": "slow_users AS s", "on": "u.user_id = s.user_id", "using": []}] | ["CASE WHEN NOT s.user_id IS NULL THEN 'SLOW' ELSE 'FAST' END"] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | AVG(avg_close_time_assigned_days) | [{"table": "asana__user", "column": "avg_close_time_assigned_days"}] | [] | False |
| B3 | COUNT(*) | [] | [] | True |
| B3 | AVG(u.number_of_open_tasks) | [{"table": "asana__user", "column": "number_of_open_tasks"}] | [] | False |
| B3 | AVG(u.number_of_tasks_completed) | [{"table": "asana__user", "column": "number_of_tasks_completed"}] | [] | False |
| B3 | AVG(u.avg_close_time_assigned_days) | [{"table": "asana__user", "column": "avg_close_time_assigned_days"}] | [] | False |


## S29

类别 `data`；来源 `query_db`；调用 `77b139bfb05948869679e13c74211754`；状态 `success`。

```sql
SELECT strftime('%Y-%m', created_at) AS month, COUNT(*) AS tasks_created,
SUM(CASE WHEN is_completed=1 THEN 1 ELSE 0 END) AS completed,
ROUND(100.0*SUM(CASE WHEN is_completed=1 THEN 1 ELSE 0 END)/COUNT(*),1) AS completion_rate,
ROUND(AVG(complexity_score),2) AS avg_complexity,
ROUND(AVG(project_health_score),2) AS avg_health
FROM asana__task_lifecycle_analysis
WHERE is_valid_record=1
GROUP BY month ORDER BY month
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-051/attempt-01/sql/S29.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-051/attempt-01/sql/S29.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-051/attempt-01/results/S29.rows.jsonl)；完整：True；SHA256：`d799e1dd16cc2126d98115a0e05cfd45418a556c91357e2c806bd499a2e3a19c`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "asana__task_lifecycle_analysis", "kind": "base", "block": null, "base_tables": ["asana__task_lifecycle_analysis"]}] | [] | ["STRFTIME('%Y-%m', created_at)"] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |
| B1 | SUM(CASE WHEN is_completed = 1 THEN 1 ELSE 0 END) | [] | [{"table": "asana__task_lifecycle_analysis", "column": "is_completed"}] | False |
| B1 | AVG(complexity_score) | [{"table": "asana__task_lifecycle_analysis", "column": "complexity_score"}] | [] | False |
| B1 | AVG(project_health_score) | [{"table": "asana__task_lifecycle_analysis", "column": "project_health_score"}] | [] | False |
| B1 | COUNT(*) | [] | [] | True |
| B1 | SUM(CASE WHEN is_completed = 1 THEN 1 ELSE 0 END) | [] | [{"table": "asana__task_lifecycle_analysis", "column": "is_completed"}] | False |


## S30

类别 `data`；来源 `query_db`；调用 `43a6e7997c054279ab1f721abe9cf018`；状态 `success`。

```sql
SELECT
  CASE WHEN u.avg_close_time_assigned_days > (SELECT 1.5*AVG(avg_close_time_assigned_days) FROM asana__user) THEN 'SLOW' ELSE 'FAST' END AS cohort,
  t.complexity_execution_match, COUNT(*) AS cnt,
  ROUND(100.0*COUNT(*)/SUM(COUNT(*)) OVER(PARTITION BY (CASE WHEN u.avg_close_time_assigned_days > (SELECT 1.5*AVG(avg_close_time_assigned_days) FROM asana__user) THEN 'SLOW' ELSE 'FAST' END)),1) AS pct
FROM asana__task_lifecycle_analysis t
JOIN asana__user u ON CAST(t.assignee_user_id AS TEXT) = u.user_id
WHERE t.is_valid_record=1
GROUP BY cohort, t.complexity_execution_match
ORDER BY cohort, pct DESC
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-051/attempt-01/sql/S30.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-051/attempt-01/sql/S30.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-051/attempt-01/results/S30.rows.jsonl)；完整：True；SHA256：`7a2e53ce0337a701fb1ac4c4f91e533812f23e42b31e0e143141edd41bceadf1`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "asana__user", "kind": "base", "block": null, "base_tables": ["asana__user"]}] | [] | [] |
| B2 | [{"alias": "asana__user", "kind": "base", "block": null, "base_tables": ["asana__user"]}] | [] | [] |
| B3 | [{"alias": "t", "kind": "base", "block": null, "base_tables": ["asana__task_lifecycle_analysis"]}, {"alias": "u", "kind": "base", "block": null, "base_tables": ["asana__user"]}] | [{"type": "INNER", "right": "asana__user AS u", "on": "CAST(t.assignee_user_id AS TEXT) = u.user_id", "using": []}] | ["CASE WHEN u.avg_close_time_assigned_days > (SELECT 1.5 * AVG(avg_close_time_assigned_days) FROM asana__user) THEN 'SLOW' ELSE 'FAST' END", "t.complexity_execution_match"] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | AVG(avg_close_time_assigned_days) | [{"table": "asana__user", "column": "avg_close_time_assigned_days"}] | [] | False |
| B2 | AVG(avg_close_time_assigned_days) | [{"table": "asana__user", "column": "avg_close_time_assigned_days"}] | [] | False |
| B3 | COUNT(*) | [] | [] | True |
| B3 | COUNT(*) | [] | [] | True |
| B3 | COUNT(*) | [] | [] | True |


## S31

类别 `data`；来源 `query_db`；调用 `39ce00df4c1144c2b28cf82e2cd5b44d`；状态 `success`。

```sql
SELECT
  CASE WHEN u.avg_close_time_assigned_days > (SELECT 1.5*AVG(avg_close_time_assigned_days) FROM asana__user) THEN 'SLOW' ELSE 'FAST' END AS cohort,
  t.improvement_opportunities, COUNT(*) AS cnt,
  ROUND(100.0*COUNT(*)/SUM(COUNT(*)) OVER(PARTITION BY (CASE WHEN u.avg_close_time_assigned_days > (SELECT 1.5*AVG(avg_close_time_assigned_days) FROM asana__user) THEN 'SLOW' ELSE 'FAST' END)),1) AS pct
FROM asana__task_lifecycle_analysis t
JOIN asana__user u ON CAST(t.assignee_user_id AS TEXT) = u.user_id
WHERE t.is_valid_record=1
GROUP BY cohort, t.improvement_opportunities
ORDER BY cohort, pct DESC
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-051/attempt-01/sql/S31.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-051/attempt-01/sql/S31.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-051/attempt-01/results/S31.rows.jsonl)；完整：True；SHA256：`2c10799ada25894b5305588222f3c507a44bc50320eb6f1dab6a915e1eec1387`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "asana__user", "kind": "base", "block": null, "base_tables": ["asana__user"]}] | [] | [] |
| B2 | [{"alias": "asana__user", "kind": "base", "block": null, "base_tables": ["asana__user"]}] | [] | [] |
| B3 | [{"alias": "t", "kind": "base", "block": null, "base_tables": ["asana__task_lifecycle_analysis"]}, {"alias": "u", "kind": "base", "block": null, "base_tables": ["asana__user"]}] | [{"type": "INNER", "right": "asana__user AS u", "on": "CAST(t.assignee_user_id AS TEXT) = u.user_id", "using": []}] | ["CASE WHEN u.avg_close_time_assigned_days > (SELECT 1.5 * AVG(avg_close_time_assigned_days) FROM asana__user) THEN 'SLOW' ELSE 'FAST' END", "t.improvement_opportunities"] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | AVG(avg_close_time_assigned_days) | [{"table": "asana__user", "column": "avg_close_time_assigned_days"}] | [] | False |
| B2 | AVG(avg_close_time_assigned_days) | [{"table": "asana__user", "column": "avg_close_time_assigned_days"}] | [] | False |
| B3 | COUNT(*) | [] | [] | True |
| B3 | COUNT(*) | [] | [] | True |
| B3 | COUNT(*) | [] | [] | True |


## S32

类别 `data`；来源 `query_db`；调用 `37b3c4a7ffb64acc8a8d588783feea65`；状态 `success`。

```sql
SELECT t.improvement_opportunities, COUNT(*) AS cnt
FROM asana__task_lifecycle_analysis t
JOIN asana__user u ON CAST(t.assignee_user_id AS TEXT) = u.user_id
WHERE t.is_valid_record=1
AND u.avg_close_time_assigned_days > (SELECT 1.5*AVG(avg_close_time_assigned_days) FROM asana__user)
GROUP BY t.improvement_opportunities
ORDER BY cnt DESC
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-051/attempt-01/sql/S32.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-051/attempt-01/sql/S32.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-051/attempt-01/results/S32.rows.jsonl)；完整：True；SHA256：`8248c03b8f56a644498c9fbebf7e268d5a5a2f47571938defe7feb453bf984f7`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "asana__user", "kind": "base", "block": null, "base_tables": ["asana__user"]}] | [] | [] |
| B2 | [{"alias": "t", "kind": "base", "block": null, "base_tables": ["asana__task_lifecycle_analysis"]}, {"alias": "u", "kind": "base", "block": null, "base_tables": ["asana__user"]}] | [{"type": "INNER", "right": "asana__user AS u", "on": "CAST(t.assignee_user_id AS TEXT) = u.user_id", "using": []}] | ["t.improvement_opportunities"] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | AVG(avg_close_time_assigned_days) | [{"table": "asana__user", "column": "avg_close_time_assigned_days"}] | [] | False |
| B2 | COUNT(*) | [] | [] | True |


## S33

类别 `data`；来源 `query_db`；调用 `3e27efe0beac48298dc13085d7759a95`；状态 `success`。

```sql
SELECT t.complexity_execution_match, COUNT(*) AS cnt
FROM asana__task_lifecycle_analysis t
JOIN asana__user u ON CAST(t.assignee_user_id AS TEXT) = u.user_id
WHERE t.is_valid_record=1
AND u.avg_close_time_assigned_days > (SELECT 1.5*AVG(avg_close_time_assigned_days) FROM asana__user)
GROUP BY t.complexity_execution_match
ORDER BY cnt DESC
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-051/attempt-01/sql/S33.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-051/attempt-01/sql/S33.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-051/attempt-01/results/S33.rows.jsonl)；完整：True；SHA256：`0a2684916b5eb3a41cd62a1261bcf6104ee1fbfdd7c0e2eb14e4505352ea8aa5`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "asana__user", "kind": "base", "block": null, "base_tables": ["asana__user"]}] | [] | [] |
| B2 | [{"alias": "t", "kind": "base", "block": null, "base_tables": ["asana__task_lifecycle_analysis"]}, {"alias": "u", "kind": "base", "block": null, "base_tables": ["asana__user"]}] | [{"type": "INNER", "right": "asana__user AS u", "on": "CAST(t.assignee_user_id AS TEXT) = u.user_id", "using": []}] | ["t.complexity_execution_match"] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | AVG(avg_close_time_assigned_days) | [{"table": "asana__user", "column": "avg_close_time_assigned_days"}] | [] | False |
| B2 | COUNT(*) | [] | [] | True |


## S34

类别 `data`；来源 `query_db`；调用 `f504605b680f4f1d97b1f99428367bfe`；状态 `success`。

```sql
WITH user_task_stats AS (
  SELECT CAST(assignee_user_id AS TEXT) AS user_id,
    COUNT(*) AS n_tasks,
    SUM(CASE WHEN is_completed=1 THEN 1 ELSE 0 END) AS n_completed,
    ROUND(AVG(complexity_score),2) AS avg_task_complexity,
    ROUND(AVG(urgency_score),2) AS avg_task_urgency,
    ROUND(AVG(project_health_score),2) AS avg_project_health
  FROM asana__task_lifecycle_analysis
  WHERE is_valid_record=1 AND assignee_user_id IS NOT NULL
  GROUP BY assignee_user_id
)
SELECT
  CASE WHEN u.avg_close_time_assigned_days > (SELECT 1.5*AVG(avg_close_time_assigned_days) FROM asana__user) THEN 'SLOW' ELSE 'FAST' END AS cohort,
  COUNT(*) AS n_matched_users,
  ROUND(AVG(ts.n_tasks),2) AS avg_tasks_per_user,
  ROUND(AVG(ts.avg_task_complexity),2) AS avg_task_complexity,
  ROUND(AVG(ts.avg_task_urgency),2) AS avg_task_urgency,
  ROUND(AVG(ts.avg_project_health),2) AS avg_proj_health
FROM asana__user u
JOIN user_task_stats ts ON u.user_id = ts.user_id
GROUP BY cohort
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-051/attempt-01/sql/S34.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-051/attempt-01/sql/S34.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-051/attempt-01/results/S34.rows.jsonl)；完整：True；SHA256：`8ecf8e387f72924392e4c5e9d8c9a2d48ba658297a83139d614b70e7f27be034`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "asana__task_lifecycle_analysis", "kind": "base", "block": null, "base_tables": ["asana__task_lifecycle_analysis"]}] | [] | ["assignee_user_id"] |
| B2 | [{"alias": "asana__user", "kind": "base", "block": null, "base_tables": ["asana__user"]}] | [] | [] |
| B3 | [{"alias": "u", "kind": "base", "block": null, "base_tables": ["asana__user"]}, {"alias": "ts", "kind": "derived", "block": "B1", "base_tables": ["asana__task_lifecycle_analysis"]}] | [{"type": "INNER", "right": "user_task_stats AS ts", "on": "u.user_id = ts.user_id", "using": []}] | ["CASE WHEN u.avg_close_time_assigned_days > (SELECT 1.5 * AVG(avg_close_time_assigned_days) FROM asana__user) THEN 'SLOW' ELSE 'FAST' END"] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |
| B1 | SUM(CASE WHEN is_completed = 1 THEN 1 ELSE 0 END) | [] | [{"table": "asana__task_lifecycle_analysis", "column": "is_completed"}] | False |
| B1 | AVG(complexity_score) | [{"table": "asana__task_lifecycle_analysis", "column": "complexity_score"}] | [] | False |
| B1 | AVG(urgency_score) | [{"table": "asana__task_lifecycle_analysis", "column": "urgency_score"}] | [] | False |
| B1 | AVG(project_health_score) | [{"table": "asana__task_lifecycle_analysis", "column": "project_health_score"}] | [] | False |
| B2 | AVG(avg_close_time_assigned_days) | [{"table": "asana__user", "column": "avg_close_time_assigned_days"}] | [] | False |
| B3 | COUNT(*) | [] | [] | True |
| B3 | AVG(ts.n_tasks) | [] | [] | False |
| B3 | AVG(ts.avg_task_complexity) | [{"table": "asana__task_lifecycle_analysis", "column": "complexity_score"}] | [] | False |
| B3 | AVG(ts.avg_task_urgency) | [{"table": "asana__task_lifecycle_analysis", "column": "urgency_score"}] | [] | False |
| B3 | AVG(ts.avg_project_health) | [{"table": "asana__task_lifecycle_analysis", "column": "project_health_score"}] | [] | False |


## S35

类别 `data`；来源 `query_db`；调用 `917409c3be4c4febb5e9741bb5ed23c9`；状态 `success`。

```sql
SELECT t.team_id,
  COUNT(*) FILTER (WHERE is_completed=1) AS completed_cnt,
  COUNT(*) AS total_cnt,
  ROUND(100.0*COUNT(*) FILTER (WHERE is_completed=1)/COUNT(*),1) AS completion_rate,
  COUNT(DISTINCT CAST(t.assignee_user_id AS TEXT)) AS n_users,
  COUNT(DISTINCT CASE WHEN u.avg_close_time_assigned_days > (SELECT 1.5*AVG(avg_close_time_assigned_days) FROM asana__user) THEN CAST(t.assignee_user_id AS TEXT) END) AS n_slow_users,
  ROUND(AVG(t.hours_assigned_to_completion),1) AS avg_atc_hours
FROM asana__task_lifecycle_analysis t
LEFT JOIN asana__user u ON CAST(t.assignee_user_id AS TEXT)=u.user_id
WHERE t.is_valid_record=1
GROUP BY t.team_id
HAVING total_cnt >= 50
ORDER BY completion_rate ASC
LIMIT 15
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-051/attempt-01/sql/S35.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-051/attempt-01/sql/S35.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-051/attempt-01/results/S35.rows.jsonl)；完整：True；SHA256：`80232acefc23ddfb6f55ae8abad8d32b818779079770f7942f70ed3564c25a5e`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "asana__user", "kind": "base", "block": null, "base_tables": ["asana__user"]}] | [] | [] |
| B2 | [{"alias": "t", "kind": "base", "block": null, "base_tables": ["asana__task_lifecycle_analysis"]}, {"alias": "u", "kind": "base", "block": null, "base_tables": ["asana__user"]}] | [{"type": "LEFT", "right": "asana__user AS u", "on": "CAST(t.assignee_user_id AS TEXT) = u.user_id", "using": []}] | ["t.team_id"] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | AVG(avg_close_time_assigned_days) | [{"table": "asana__user", "column": "avg_close_time_assigned_days"}] | [] | False |
| B2 | COUNT(*) | [] | [] | True |
| B2 | COUNT(DISTINCT CAST(t.assignee_user_id AS TEXT)) | [{"table": "asana__task_lifecycle_analysis", "column": "assignee_user_id"}] | [] | False |
| B2 | COUNT(DISTINCT CASE WHEN u.avg_close_time_assigned_days > (SELECT 1.5 * AVG(avg_close_time_assigned_days) FROM asana__user) THEN CAST(t.assignee_user_id AS TEXT) END) | [{"table": "asana__task_lifecycle_analysis", "column": "assignee_user_id"}] | [{"table": "asana__user", "column": "avg_close_time_assigned_days"}, {"table": "asana__user", "column": "avg_close_time_assigned_days"}] | False |
| B2 | COUNT(*) FILTER(WHERE is_completed = 1) | [] | [{"table": "asana__task_lifecycle_analysis", "column": "is_completed"}] | True |
| B2 | AVG(t.hours_assigned_to_completion) | [{"table": "asana__task_lifecycle_analysis", "column": "hours_assigned_to_completion"}] | [] | False |
| B2 | COUNT(*) | [] | [] | True |
| B2 | COUNT(*) FILTER(WHERE is_completed = 1) | [] | [{"table": "asana__task_lifecycle_analysis", "column": "is_completed"}] | True |


## S36

类别 `data`；来源 `python`；调用 `f175a1ee55cf4cbc856e5400bd4e44ad`；状态 `success`。

```sql

SELECT t.*,
  CASE WHEN u.avg_close_time_assigned_days > (SELECT 1.5*AVG(avg_close_time_assigned_days) FROM asana__user) THEN 'SLOW' ELSE 'FAST' END AS cohort
FROM asana__task_lifecycle_analysis t
JOIN asana__user u ON CAST(t.assignee_user_id AS TEXT) = u.user_id
WHERE t.is_valid_record=1

```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-051/attempt-01/sql/S36.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-051/attempt-01/sql/S36.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-051/attempt-01/results/S36.rows.jsonl)；完整：True；SHA256：`ee1be45e96c3ef8380052e312356c93e4448d994aceccde13c18e873e0ddeff9`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "asana__user", "kind": "base", "block": null, "base_tables": ["asana__user"]}] | [] | [] |
| B2 | [{"alias": "t", "kind": "base", "block": null, "base_tables": ["asana__task_lifecycle_analysis"]}, {"alias": "u", "kind": "base", "block": null, "base_tables": ["asana__user"]}] | [{"type": "INNER", "right": "asana__user AS u", "on": "CAST(t.assignee_user_id AS TEXT) = u.user_id", "using": []}] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | AVG(avg_close_time_assigned_days) | [{"table": "asana__user", "column": "avg_close_time_assigned_days"}] | [] | False |


## S37

类别 `data`；来源 `python`；调用 `b6004d5044fb4a08871b00f01a718a85`；状态 `success`。

```sql

SELECT t.team_id,
  COUNT(*) AS total_tasks,
  SUM(CASE WHEN t.is_completed=1 THEN 1 ELSE 0 END) AS completed_tasks,
  ROUND(100.0*SUM(CASE WHEN t.is_completed=1 THEN 1 ELSE 0 END)/COUNT(*),2) AS completion_rate,
  ROUND(AVG(t.project_health_score),2) AS avg_project_health,
  ROUND(AVG(t.hours_assigned_to_completion),1) AS avg_hours_atc,
  ROUND(AVG(t.complexity_score),2) AS avg_complexity,
  ROUND(AVG(t.urgency_score),2) AS avg_urgency,
  COUNT(DISTINCT t.assignee_user_id) AS n_users,
  COUNT(DISTINCT CASE WHEN u.avg_close_time_assigned_days > (SELECT 1.5*AVG(avg_close_time_assigned_days) FROM asana__user) THEN t.assignee_user_id END) AS n_slow_users,
  ROUND(100.0*COUNT(DISTINCT CASE WHEN u.avg_close_time_assigned_days > (SELECT 1.5*AVG(avg_close_time_assigned_days) FROM asana__user) THEN t.assignee_user_id END)/NULLIF(COUNT(DISTINCT t.assignee_user_id),0),2) AS slow_user_pct
FROM asana__task_lifecycle_analysis t
LEFT JOIN asana__user u ON CAST(t.assignee_user_id AS TEXT)=u.user_id
WHERE t.is_valid_record=1
GROUP BY t.team_id
ORDER BY completion_rate ASC

```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-051/attempt-01/sql/S37.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-051/attempt-01/sql/S37.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-051/attempt-01/results/S37.rows.jsonl)；完整：True；SHA256：`a56f628bee093ffeeaaaa3837ca429c7294d392e6ff850aa19ca422eb1385e6c`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "asana__user", "kind": "base", "block": null, "base_tables": ["asana__user"]}] | [] | [] |
| B2 | [{"alias": "asana__user", "kind": "base", "block": null, "base_tables": ["asana__user"]}] | [] | [] |
| B3 | [{"alias": "t", "kind": "base", "block": null, "base_tables": ["asana__task_lifecycle_analysis"]}, {"alias": "u", "kind": "base", "block": null, "base_tables": ["asana__user"]}] | [{"type": "LEFT", "right": "asana__user AS u", "on": "CAST(t.assignee_user_id AS TEXT) = u.user_id", "using": []}] | ["t.team_id"] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | AVG(avg_close_time_assigned_days) | [{"table": "asana__user", "column": "avg_close_time_assigned_days"}] | [] | False |
| B2 | AVG(avg_close_time_assigned_days) | [{"table": "asana__user", "column": "avg_close_time_assigned_days"}] | [] | False |
| B3 | COUNT(*) | [] | [] | True |
| B3 | SUM(CASE WHEN t.is_completed = 1 THEN 1 ELSE 0 END) | [] | [{"table": "asana__task_lifecycle_analysis", "column": "is_completed"}] | False |
| B3 | COUNT(DISTINCT t.assignee_user_id) | [{"table": "asana__task_lifecycle_analysis", "column": "assignee_user_id"}] | [] | False |
| B3 | COUNT(DISTINCT CASE WHEN u.avg_close_time_assigned_days > (SELECT 1.5 * AVG(avg_close_time_assigned_days) FROM asana__user) THEN t.assignee_user_id END) | [{"table": "asana__task_lifecycle_analysis", "column": "assignee_user_id"}] | [{"table": "asana__user", "column": "avg_close_time_assigned_days"}, {"table": "asana__user", "column": "avg_close_time_assigned_days"}] | False |
| B3 | AVG(t.project_health_score) | [{"table": "asana__task_lifecycle_analysis", "column": "project_health_score"}] | [] | False |
| B3 | AVG(t.hours_assigned_to_completion) | [{"table": "asana__task_lifecycle_analysis", "column": "hours_assigned_to_completion"}] | [] | False |
| B3 | AVG(t.complexity_score) | [{"table": "asana__task_lifecycle_analysis", "column": "complexity_score"}] | [] | False |
| B3 | AVG(t.urgency_score) | [{"table": "asana__task_lifecycle_analysis", "column": "urgency_score"}] | [] | False |
| B3 | COUNT(*) | [] | [] | True |
| B3 | SUM(CASE WHEN t.is_completed = 1 THEN 1 ELSE 0 END) | [] | [{"table": "asana__task_lifecycle_analysis", "column": "is_completed"}] | False |
| B3 | COUNT(DISTINCT CASE WHEN u.avg_close_time_assigned_days > (SELECT 1.5 * AVG(avg_close_time_assigned_days) FROM asana__user) THEN t.assignee_user_id END) | [{"table": "asana__task_lifecycle_analysis", "column": "assignee_user_id"}] | [{"table": "asana__user", "column": "avg_close_time_assigned_days"}, {"table": "asana__user", "column": "avg_close_time_assigned_days"}] | False |
| B3 | COUNT(DISTINCT t.assignee_user_id) | [{"table": "asana__task_lifecycle_analysis", "column": "assignee_user_id"}] | [] | False |


## S38

类别 `data`；来源 `python`；调用 `7f8750b01b3d4ee1added66010e611bb`；状态 `success`。

```sql

SELECT strftime('%Y-%m', t.created_at) AS month,
  CASE WHEN u.avg_close_time_assigned_days > (SELECT 1.5*AVG(avg_close_time_assigned_days) FROM asana__user) THEN 'SLOW' ELSE 'FAST' END AS cohort,
  COUNT(*) AS n_tasks,
  SUM(CASE WHEN t.is_completed=1 THEN 1 ELSE 0 END) AS n_completed,
  ROUND(AVG(t.hours_assigned_to_completion),1) AS avg_atc,
  ROUND(AVG(t.avg_daily_activity_rate),3) AS avg_daily_activity
FROM asana__task_lifecycle_analysis t
JOIN asana__user u ON CAST(t.assignee_user_id AS TEXT) = u.user_id
WHERE t.is_valid_record=1 AND t.created_at IS NOT NULL
GROUP BY month, cohort
ORDER BY month

```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-051/attempt-01/sql/S38.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-051/attempt-01/sql/S38.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-051/attempt-01/results/S38.rows.jsonl)；完整：True；SHA256：`2194ecf0121c4b19ab2ae6fde03302720ad52ab932586d9a41c9c9ff14856c82`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "asana__user", "kind": "base", "block": null, "base_tables": ["asana__user"]}] | [] | [] |
| B2 | [{"alias": "t", "kind": "base", "block": null, "base_tables": ["asana__task_lifecycle_analysis"]}, {"alias": "u", "kind": "base", "block": null, "base_tables": ["asana__user"]}] | [{"type": "INNER", "right": "asana__user AS u", "on": "CAST(t.assignee_user_id AS TEXT) = u.user_id", "using": []}] | ["STRFTIME('%Y-%m', t.created_at)", "CASE WHEN u.avg_close_time_assigned_days > (SELECT 1.5 * AVG(avg_close_time_assigned_days) FROM asana__user) THEN 'SLOW' ELSE 'FAST' END"] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | AVG(avg_close_time_assigned_days) | [{"table": "asana__user", "column": "avg_close_time_assigned_days"}] | [] | False |
| B2 | COUNT(*) | [] | [] | True |
| B2 | SUM(CASE WHEN t.is_completed = 1 THEN 1 ELSE 0 END) | [] | [{"table": "asana__task_lifecycle_analysis", "column": "is_completed"}] | False |
| B2 | AVG(t.hours_assigned_to_completion) | [{"table": "asana__task_lifecycle_analysis", "column": "hours_assigned_to_completion"}] | [] | False |
| B2 | AVG(t.avg_daily_activity_rate) | [{"table": "asana__task_lifecycle_analysis", "column": "avg_daily_activity_rate"}] | [] | False |


## S39

类别 `data`；来源 `python`；调用 `7f8750b01b3d4ee1added66010e611bb`；状态 `success`。

```sql

SELECT strftime('%Y-%m', created_at) AS month, COUNT(*) AS n_tasks,
SUM(CASE WHEN is_completed=1 THEN 1 ELSE 0 END) AS n_completed,
ROUND(100.0*SUM(CASE WHEN is_completed=1 THEN 1 ELSE 0 END)/COUNT(*),1) AS comp_rate
FROM asana__task_lifecycle_analysis
WHERE is_valid_record=1 AND created_at IS NOT NULL
GROUP BY month ORDER BY month

```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-051/attempt-01/sql/S39.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-051/attempt-01/sql/S39.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-051/attempt-01/results/S39.rows.jsonl)；完整：True；SHA256：`754f21b67f9cc7a1b4be1b254796b49cdad76a4b42b3a5d6bce93bd812385384`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "asana__task_lifecycle_analysis", "kind": "base", "block": null, "base_tables": ["asana__task_lifecycle_analysis"]}] | [] | ["STRFTIME('%Y-%m', created_at)"] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |
| B1 | SUM(CASE WHEN is_completed = 1 THEN 1 ELSE 0 END) | [] | [{"table": "asana__task_lifecycle_analysis", "column": "is_completed"}] | False |
| B1 | COUNT(*) | [] | [] | True |
| B1 | SUM(CASE WHEN is_completed = 1 THEN 1 ELSE 0 END) | [] | [{"table": "asana__task_lifecycle_analysis", "column": "is_completed"}] | False |


## S40

类别 `data`；来源 `python`；调用 `7f8750b01b3d4ee1added66010e611bb`；状态 `success`。

```sql

SELECT u.user_id, u.user_name, u.avg_close_time_assigned_days,
  u.number_of_open_tasks, u.number_of_tasks_completed,
  ts.n_tasks AS tasks_in_table,
  ts.n_completed AS completed_in_table
FROM asana__user u
LEFT JOIN (
  SELECT CAST(assignee_user_id AS TEXT) AS user_id, COUNT(*) AS n_tasks,
    SUM(CASE WHEN is_completed=1 THEN 1 ELSE 0 END) AS n_completed
  FROM asana__task_lifecycle_analysis
  WHERE is_valid_record=1
  GROUP BY assignee_user_id
) ts ON u.user_id = ts.user_id

```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-051/attempt-01/sql/S40.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-051/attempt-01/sql/S40.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-051/attempt-01/results/S40.rows.jsonl)；完整：True；SHA256：`57e974db0c887276f8a1f51ff6c498fbf135f74b26e1faafbe862fcb15072282`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "asana__task_lifecycle_analysis", "kind": "base", "block": null, "base_tables": ["asana__task_lifecycle_analysis"]}] | [] | ["assignee_user_id"] |
| B2 | [{"alias": "u", "kind": "base", "block": null, "base_tables": ["asana__user"]}, {"alias": "ts", "kind": "derived", "block": "B1", "base_tables": ["asana__task_lifecycle_analysis"]}] | [{"type": "LEFT", "right": "(SELECT CAST(assignee_user_id AS TEXT) AS user_id, COUNT(*) AS n_tasks, SUM(CASE WHEN is_completed = 1 THEN 1 ELSE 0 END) AS n_completed FROM asana__task_lifecycle_analysis WHERE is_valid_record = 1 GROUP BY assignee_user_id) AS ts", "on": "u.user_id = ts.user_id", "using": []}] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |
| B1 | SUM(CASE WHEN is_completed = 1 THEN 1 ELSE 0 END) | [] | [{"table": "asana__task_lifecycle_analysis", "column": "is_completed"}] | False |


## S41

类别 `data`；来源 `python`；调用 `8cf7b259cfea48f3b7f0e2e05db08a5b`；状态 `success`。

```sql

SELECT t.*,
  CASE WHEN u.avg_close_time_assigned_days > (SELECT 1.5*AVG(avg_close_time_assigned_days) FROM asana__user) THEN 'SLOW' ELSE 'FAST' END AS cohort
FROM asana__task_lifecycle_analysis t
JOIN asana__user u ON CAST(t.assignee_user_id AS TEXT) = u.user_id
WHERE t.is_valid_record=1

```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-051/attempt-01/sql/S41.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-051/attempt-01/sql/S41.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-051/attempt-01/results/S41.rows.jsonl)；完整：True；SHA256：`ee1be45e96c3ef8380052e312356c93e4448d994aceccde13c18e873e0ddeff9`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "asana__user", "kind": "base", "block": null, "base_tables": ["asana__user"]}] | [] | [] |
| B2 | [{"alias": "t", "kind": "base", "block": null, "base_tables": ["asana__task_lifecycle_analysis"]}, {"alias": "u", "kind": "base", "block": null, "base_tables": ["asana__user"]}] | [{"type": "INNER", "right": "asana__user AS u", "on": "CAST(t.assignee_user_id AS TEXT) = u.user_id", "using": []}] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | AVG(avg_close_time_assigned_days) | [{"table": "asana__user", "column": "avg_close_time_assigned_days"}] | [] | False |


## S42

类别 `data`；来源 `python`；调用 `843503c091724a5e9b7ccf8df43327f7`；状态 `success`。

```sql

SELECT CAST(t.assignee_user_id AS TEXT) AS user_id, u.user_name,
  u.avg_close_time_assigned_days,
  u.number_of_open_tasks,
  u.number_of_tasks_completed,
  COUNT(*) AS n_tasks,
  SUM(CASE WHEN t.is_completed=1 THEN 1 ELSE 0 END) AS n_completed,
  ROUND(AVG(t.complexity_score),2) AS avg_complexity,
  ROUND(AVG(t.urgency_score),2) AS avg_urgency,
  ROUND(AVG(t.hours_assigned_to_completion),1) AS avg_atc,
  ROUND(AVG(t.avg_daily_activity_rate),3) AS avg_activity_rate,
  SUM(CASE WHEN t.delay_days>0 THEN 1 ELSE 0 END) AS n_delayed
FROM asana__task_lifecycle_analysis t
JOIN asana__user u ON CAST(t.assignee_user_id AS TEXT)=u.user_id
WHERE t.is_valid_record=1
GROUP BY t.assignee_user_id

```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-051/attempt-01/sql/S42.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-051/attempt-01/sql/S42.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-051/attempt-01/results/S42.rows.jsonl)；完整：True；SHA256：`6f2bc966cc198ceb6f9054627de6df2724b1973e075c2d004edf516adc85017c`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "t", "kind": "base", "block": null, "base_tables": ["asana__task_lifecycle_analysis"]}, {"alias": "u", "kind": "base", "block": null, "base_tables": ["asana__user"]}] | [{"type": "INNER", "right": "asana__user AS u", "on": "CAST(t.assignee_user_id AS TEXT) = u.user_id", "using": []}] | ["t.assignee_user_id"] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |
| B1 | SUM(CASE WHEN t.is_completed = 1 THEN 1 ELSE 0 END) | [] | [{"table": "asana__task_lifecycle_analysis", "column": "is_completed"}] | False |
| B1 | SUM(CASE WHEN t.delay_days > 0 THEN 1 ELSE 0 END) | [] | [{"table": "asana__task_lifecycle_analysis", "column": "delay_days"}] | False |
| B1 | AVG(t.complexity_score) | [{"table": "asana__task_lifecycle_analysis", "column": "complexity_score"}] | [] | False |
| B1 | AVG(t.urgency_score) | [{"table": "asana__task_lifecycle_analysis", "column": "urgency_score"}] | [] | False |
| B1 | AVG(t.hours_assigned_to_completion) | [{"table": "asana__task_lifecycle_analysis", "column": "hours_assigned_to_completion"}] | [] | False |
| B1 | AVG(t.avg_daily_activity_rate) | [{"table": "asana__task_lifecycle_analysis", "column": "avg_daily_activity_rate"}] | [] | False |


## S43

类别 `data`；来源 `python`；调用 `843503c091724a5e9b7ccf8df43327f7`；状态 `success`。

```sql

SELECT t.team_id,
  COUNT(*) AS total_tasks,
  ROUND(100.0*SUM(CASE WHEN t.is_completed=1 THEN 1 ELSE 0 END)/COUNT(*),2) AS completion_rate,
  COUNT(DISTINCT CASE WHEN u.avg_close_time_assigned_days > (SELECT 1.5*AVG(avg_close_time_assigned_days) FROM asana__user) THEN t.assignee_user_id END) AS n_slow_users
FROM asana__task_lifecycle_analysis t
LEFT JOIN asana__user u ON CAST(t.assignee_user_id AS TEXT)=u.user_id
WHERE t.is_valid_record=1
GROUP BY t.team_id

```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-051/attempt-01/sql/S43.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-051/attempt-01/sql/S43.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-051/attempt-01/results/S43.rows.jsonl)；完整：True；SHA256：`38ffa2c6184e68d2ab58a496308ec2fc391fa368eca9ec75bbef2b0934423524`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "asana__user", "kind": "base", "block": null, "base_tables": ["asana__user"]}] | [] | [] |
| B2 | [{"alias": "t", "kind": "base", "block": null, "base_tables": ["asana__task_lifecycle_analysis"]}, {"alias": "u", "kind": "base", "block": null, "base_tables": ["asana__user"]}] | [{"type": "LEFT", "right": "asana__user AS u", "on": "CAST(t.assignee_user_id AS TEXT) = u.user_id", "using": []}] | ["t.team_id"] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | AVG(avg_close_time_assigned_days) | [{"table": "asana__user", "column": "avg_close_time_assigned_days"}] | [] | False |
| B2 | COUNT(*) | [] | [] | True |
| B2 | COUNT(DISTINCT CASE WHEN u.avg_close_time_assigned_days > (SELECT 1.5 * AVG(avg_close_time_assigned_days) FROM asana__user) THEN t.assignee_user_id END) | [{"table": "asana__task_lifecycle_analysis", "column": "assignee_user_id"}] | [{"table": "asana__user", "column": "avg_close_time_assigned_days"}, {"table": "asana__user", "column": "avg_close_time_assigned_days"}] | False |
| B2 | COUNT(*) | [] | [] | True |
| B2 | SUM(CASE WHEN t.is_completed = 1 THEN 1 ELSE 0 END) | [] | [{"table": "asana__task_lifecycle_analysis", "column": "is_completed"}] | False |


## S44

类别 `data`；来源 `query_db`；调用 `0490cf78c537469fa4615adcf1d13ed7`；状态 `success`。

```sql
SELECT t.success_patterns, COUNT(*) AS cnt,
ROUND(100.0*COUNT(*)/SUM(COUNT(*)) OVER(),1) AS pct
FROM asana__task_lifecycle_analysis t
JOIN asana__user u ON CAST(t.assignee_user_id AS TEXT) = u.user_id
WHERE t.is_valid_record=1
AND u.avg_close_time_assigned_days > (SELECT 1.5*AVG(avg_close_time_assigned_days) FROM asana__user)
GROUP BY t.success_patterns
ORDER BY cnt DESC
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-051/attempt-01/sql/S44.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-051/attempt-01/sql/S44.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-051/attempt-01/results/S44.rows.jsonl)；完整：True；SHA256：`af2374501a9cf50ef8244d15df4daf296bec1fd0341cef2d9cabf32f7769d314`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "asana__user", "kind": "base", "block": null, "base_tables": ["asana__user"]}] | [] | [] |
| B2 | [{"alias": "t", "kind": "base", "block": null, "base_tables": ["asana__task_lifecycle_analysis"]}, {"alias": "u", "kind": "base", "block": null, "base_tables": ["asana__user"]}] | [{"type": "INNER", "right": "asana__user AS u", "on": "CAST(t.assignee_user_id AS TEXT) = u.user_id", "using": []}] | ["t.success_patterns"] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | AVG(avg_close_time_assigned_days) | [{"table": "asana__user", "column": "avg_close_time_assigned_days"}] | [] | False |
| B2 | COUNT(*) | [] | [] | True |
| B2 | COUNT(*) | [] | [] | True |
| B2 | COUNT(*) | [] | [] | True |


## S45

类别 `data`；来源 `query_db`；调用 `7bd2ec69de7c4e96b718c5f1e4349bb6`；状态 `success`。

```sql
SELECT t.anomaly_patterns, COUNT(*) AS cnt,
ROUND(100.0*COUNT(*)/SUM(COUNT(*)) OVER(),1) AS pct
FROM asana__task_lifecycle_analysis t
JOIN asana__user u ON CAST(t.assignee_user_id AS TEXT) = u.user_id
WHERE t.is_valid_record=1
AND u.avg_close_time_assigned_days > (SELECT 1.5*AVG(avg_close_time_assigned_days) FROM asana__user)
GROUP BY t.anomaly_patterns
ORDER BY cnt DESC
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-051/attempt-01/sql/S45.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-051/attempt-01/sql/S45.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-051/attempt-01/results/S45.rows.jsonl)；完整：True；SHA256：`094806816f8b05c36cadfd6c76d1ab71aef40ca60a90cb677618917988245ed5`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "asana__user", "kind": "base", "block": null, "base_tables": ["asana__user"]}] | [] | [] |
| B2 | [{"alias": "t", "kind": "base", "block": null, "base_tables": ["asana__task_lifecycle_analysis"]}, {"alias": "u", "kind": "base", "block": null, "base_tables": ["asana__user"]}] | [{"type": "INNER", "right": "asana__user AS u", "on": "CAST(t.assignee_user_id AS TEXT) = u.user_id", "using": []}] | ["t.anomaly_patterns"] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | AVG(avg_close_time_assigned_days) | [{"table": "asana__user", "column": "avg_close_time_assigned_days"}] | [] | False |
| B2 | COUNT(*) | [] | [] | True |
| B2 | COUNT(*) | [] | [] | True |
| B2 | COUNT(*) | [] | [] | True |


## S46

类别 `data`；来源 `query_db`；调用 `9c052f63cc6e477db02f74da276c8eff`；状态 `success`。

```sql
SELECT t.success_patterns, COUNT(*) AS cnt,
ROUND(100.0*COUNT(*)/SUM(COUNT(*)) OVER(),1) AS pct
FROM asana__task_lifecycle_analysis t
JOIN asana__user u ON CAST(t.assignee_user_id AS TEXT) = u.user_id
WHERE t.is_valid_record=1
AND u.avg_close_time_assigned_days <= (SELECT 1.5*AVG(avg_close_time_assigned_days) FROM asana__user)
GROUP BY t.success_patterns
ORDER BY cnt DESC
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-051/attempt-01/sql/S46.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-051/attempt-01/sql/S46.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-051/attempt-01/results/S46.rows.jsonl)；完整：True；SHA256：`1bda01c0044d0b02ff2616177fd582c668ef916b7cbd8a41de58c65b7f3735c3`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "asana__user", "kind": "base", "block": null, "base_tables": ["asana__user"]}] | [] | [] |
| B2 | [{"alias": "t", "kind": "base", "block": null, "base_tables": ["asana__task_lifecycle_analysis"]}, {"alias": "u", "kind": "base", "block": null, "base_tables": ["asana__user"]}] | [{"type": "INNER", "right": "asana__user AS u", "on": "CAST(t.assignee_user_id AS TEXT) = u.user_id", "using": []}] | ["t.success_patterns"] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | AVG(avg_close_time_assigned_days) | [{"table": "asana__user", "column": "avg_close_time_assigned_days"}] | [] | False |
| B2 | COUNT(*) | [] | [] | True |
| B2 | COUNT(*) | [] | [] | True |
| B2 | COUNT(*) | [] | [] | True |


## S47

类别 `data`；来源 `query_db`；调用 `c7f1a82aa3ba467a8082e746fe7fbf48`；状态 `success`。

```sql
SELECT t.project_name,
  COUNT(*) AS n_tasks,
  ROUND(100.0*SUM(CASE WHEN t.is_completed=1 THEN 1 ELSE 0 END)/COUNT(*),1) AS completion_rate,
  ROUND(AVG(t.project_health_score),1) AS avg_project_health,
  ROUND(AVG(t.complexity_score),2) AS avg_complexity,
  COUNT(DISTINCT CASE WHEN u.avg_close_time_assigned_days > (SELECT 1.5*AVG(avg_close_time_assigned_days) FROM asana__user) THEN t.assignee_user_id END) AS n_slow_users
FROM asana__task_lifecycle_analysis t
LEFT JOIN asana__user u ON CAST(t.assignee_user_id AS TEXT)=u.user_id
WHERE t.is_valid_record=1
GROUP BY t.project_name
ORDER BY n_tasks DESC
LIMIT 15
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-051/attempt-01/sql/S47.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-051/attempt-01/sql/S47.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-051/attempt-01/results/S47.rows.jsonl)；完整：True；SHA256：`686da2588ec68fc1e2895618ffaf2daeef14ba615d8bce7d9289aba1062c1ecd`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "asana__user", "kind": "base", "block": null, "base_tables": ["asana__user"]}] | [] | [] |
| B2 | [{"alias": "t", "kind": "base", "block": null, "base_tables": ["asana__task_lifecycle_analysis"]}, {"alias": "u", "kind": "base", "block": null, "base_tables": ["asana__user"]}] | [{"type": "LEFT", "right": "asana__user AS u", "on": "CAST(t.assignee_user_id AS TEXT) = u.user_id", "using": []}] | ["t.project_name"] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | AVG(avg_close_time_assigned_days) | [{"table": "asana__user", "column": "avg_close_time_assigned_days"}] | [] | False |
| B2 | COUNT(*) | [] | [] | True |
| B2 | COUNT(DISTINCT CASE WHEN u.avg_close_time_assigned_days > (SELECT 1.5 * AVG(avg_close_time_assigned_days) FROM asana__user) THEN t.assignee_user_id END) | [{"table": "asana__task_lifecycle_analysis", "column": "assignee_user_id"}] | [{"table": "asana__user", "column": "avg_close_time_assigned_days"}, {"table": "asana__user", "column": "avg_close_time_assigned_days"}] | False |
| B2 | AVG(t.project_health_score) | [{"table": "asana__task_lifecycle_analysis", "column": "project_health_score"}] | [] | False |
| B2 | AVG(t.complexity_score) | [{"table": "asana__task_lifecycle_analysis", "column": "complexity_score"}] | [] | False |
| B2 | COUNT(*) | [] | [] | True |
| B2 | SUM(CASE WHEN t.is_completed = 1 THEN 1 ELSE 0 END) | [] | [{"table": "asana__task_lifecycle_analysis", "column": "is_completed"}] | False |


## S48

类别 `data`；来源 `query_db`；调用 `ead660ba9b9f4c1a992d2de56ca38551`；状态 `success`。

```sql
SELECT COUNT(*) AS total, SUM(CASE WHEN parent_task_id IS NOT NULL AND parent_task_id != task_id THEN 1 ELSE 0 END) AS has_parent,
SUM(CASE WHEN is_completed=1 THEN 1 ELSE 0 END) AS completed
FROM asana__task_lifecycle_analysis WHERE is_valid_record=1
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-051/attempt-01/sql/S48.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-051/attempt-01/sql/S48.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-051/attempt-01/results/S48.rows.jsonl)；完整：True；SHA256：`5b35a59a7f98c7461e573954acb9b2cafa64470cb8bb480f78f1f87e01b568f4`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "asana__task_lifecycle_analysis", "kind": "base", "block": null, "base_tables": ["asana__task_lifecycle_analysis"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |
| B1 | SUM(CASE WHEN NOT parent_task_id IS NULL AND parent_task_id <> task_id THEN 1 ELSE 0 END) | [] | [{"table": "asana__task_lifecycle_analysis", "column": "parent_task_id"}, {"table": "asana__task_lifecycle_analysis", "column": "task_id"}, {"table": "asana__task_lifecycle_analysis", "column": "parent_task_id"}] | False |
| B1 | SUM(CASE WHEN is_completed = 1 THEN 1 ELSE 0 END) | [] | [{"table": "asana__task_lifecycle_analysis", "column": "is_completed"}] | False |


## S49

类别 `data`；来源 `python`；调用 `75032d797d524d85861f2d32f98ab52a`；状态 `success`。

```sql

SELECT t.*,
  CASE WHEN u.avg_close_time_assigned_days > (SELECT 1.5*AVG(avg_close_time_assigned_days) FROM asana__user) THEN 'SLOW' ELSE 'FAST' END AS cohort
FROM asana__task_lifecycle_analysis t
JOIN asana__user u ON CAST(t.assignee_user_id AS TEXT) = u.user_id
WHERE t.is_valid_record=1

```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-051/attempt-01/sql/S49.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-051/attempt-01/sql/S49.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-051/attempt-01/results/S49.rows.jsonl)；完整：True；SHA256：`ee1be45e96c3ef8380052e312356c93e4448d994aceccde13c18e873e0ddeff9`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "asana__user", "kind": "base", "block": null, "base_tables": ["asana__user"]}] | [] | [] |
| B2 | [{"alias": "t", "kind": "base", "block": null, "base_tables": ["asana__task_lifecycle_analysis"]}, {"alias": "u", "kind": "base", "block": null, "base_tables": ["asana__user"]}] | [{"type": "INNER", "right": "asana__user AS u", "on": "CAST(t.assignee_user_id AS TEXT) = u.user_id", "using": []}] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | AVG(avg_close_time_assigned_days) | [{"table": "asana__user", "column": "avg_close_time_assigned_days"}] | [] | False |


## S50

类别 `data`；来源 `python`；调用 `1fc72bfb03fc4c0eaaab6f8256dacbe4`；状态 `success`。

```sql

SELECT t.*,
  CASE WHEN u.avg_close_time_assigned_days > (SELECT 1.5*AVG(avg_close_time_assigned_days) FROM asana__user) THEN 'SLOW' ELSE 'FAST' END AS cohort
FROM asana__task_lifecycle_analysis t
JOIN asana__user u ON CAST(t.assignee_user_id AS TEXT) = u.user_id
WHERE t.is_valid_record=1

```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-051/attempt-01/sql/S50.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-051/attempt-01/sql/S50.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-051/attempt-01/results/S50.rows.jsonl)；完整：True；SHA256：`ee1be45e96c3ef8380052e312356c93e4448d994aceccde13c18e873e0ddeff9`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "asana__user", "kind": "base", "block": null, "base_tables": ["asana__user"]}] | [] | [] |
| B2 | [{"alias": "t", "kind": "base", "block": null, "base_tables": ["asana__task_lifecycle_analysis"]}, {"alias": "u", "kind": "base", "block": null, "base_tables": ["asana__user"]}] | [{"type": "INNER", "right": "asana__user AS u", "on": "CAST(t.assignee_user_id AS TEXT) = u.user_id", "using": []}] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | AVG(avg_close_time_assigned_days) | [{"table": "asana__user", "column": "avg_close_time_assigned_days"}] | [] | False |


## S51

类别 `data`；来源 `python`；调用 `c4dd86bed2dc4567a115ecb6b099633b`；状态 `success`。

```sql

SELECT t.*,
  CASE WHEN u.avg_close_time_assigned_days > (SELECT 1.5*AVG(avg_close_time_assigned_days) FROM asana__user) THEN 'SLOW' ELSE 'FAST' END AS cohort
FROM asana__task_lifecycle_analysis t
JOIN asana__user u ON CAST(t.assignee_user_id AS TEXT) = u.user_id
WHERE t.is_valid_record=1

```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-051/attempt-01/sql/S51.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-051/attempt-01/sql/S51.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-051/attempt-01/results/S51.rows.jsonl)；完整：True；SHA256：`ee1be45e96c3ef8380052e312356c93e4448d994aceccde13c18e873e0ddeff9`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "asana__user", "kind": "base", "block": null, "base_tables": ["asana__user"]}] | [] | [] |
| B2 | [{"alias": "t", "kind": "base", "block": null, "base_tables": ["asana__task_lifecycle_analysis"]}, {"alias": "u", "kind": "base", "block": null, "base_tables": ["asana__user"]}] | [{"type": "INNER", "right": "asana__user AS u", "on": "CAST(t.assignee_user_id AS TEXT) = u.user_id", "using": []}] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | AVG(avg_close_time_assigned_days) | [{"table": "asana__user", "column": "avg_close_time_assigned_days"}] | [] | False |


## S52

类别 `data`；来源 `python`；调用 `412117c59e3c4ac1a73d920d52f4fe7e`；状态 `success`。

```sql

SELECT t.*,
  CASE WHEN u.avg_close_time_assigned_days > (SELECT 1.5*AVG(avg_close_time_assigned_days) FROM asana__user) THEN 'SLOW' ELSE 'FAST' END AS cohort
FROM asana__task_lifecycle_analysis t
JOIN asana__user u ON CAST(t.assignee_user_id AS TEXT) = u.user_id
WHERE t.is_valid_record=1

```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-051/attempt-01/sql/S52.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-051/attempt-01/sql/S52.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-051/attempt-01/results/S52.rows.jsonl)；完整：True；SHA256：`ee1be45e96c3ef8380052e312356c93e4448d994aceccde13c18e873e0ddeff9`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "asana__user", "kind": "base", "block": null, "base_tables": ["asana__user"]}] | [] | [] |
| B2 | [{"alias": "t", "kind": "base", "block": null, "base_tables": ["asana__task_lifecycle_analysis"]}, {"alias": "u", "kind": "base", "block": null, "base_tables": ["asana__user"]}] | [{"type": "INNER", "right": "asana__user AS u", "on": "CAST(t.assignee_user_id AS TEXT) = u.user_id", "using": []}] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | AVG(avg_close_time_assigned_days) | [{"table": "asana__user", "column": "avg_close_time_assigned_days"}] | [] | False |


## S53

类别 `data`；来源 `python`；调用 `412117c59e3c4ac1a73d920d52f4fe7e`；状态 `success`。

```sql

SELECT team_id, COUNT(*) AS total_tasks,
SUM(CASE WHEN is_completed=1 THEN 1 ELSE 0 END) AS completed_tasks,
ROUND(100.0*SUM(CASE WHEN is_completed=1 THEN 1 ELSE 0 END)/COUNT(*),2) AS completion_rate,
ROUND(AVG(project_health_score),2) AS avg_project_health,
ROUND(AVG(hours_assigned_to_completion),1) AS avg_hours_atc
FROM asana__task_lifecycle_analysis
WHERE is_valid_record=1
GROUP BY team_id
HAVING total_tasks >= 50
ORDER BY completion_rate ASC
LIMIT 10

```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-051/attempt-01/sql/S53.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-051/attempt-01/sql/S53.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-051/attempt-01/results/S53.rows.jsonl)；完整：True；SHA256：`0cc31cd8cd34d4add40c669622d1316073ad61e6b980ca36d48a5b3b75d2ceea`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "asana__task_lifecycle_analysis", "kind": "base", "block": null, "base_tables": ["asana__task_lifecycle_analysis"]}] | [] | ["team_id"] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |
| B1 | SUM(CASE WHEN is_completed = 1 THEN 1 ELSE 0 END) | [] | [{"table": "asana__task_lifecycle_analysis", "column": "is_completed"}] | False |
| B1 | AVG(project_health_score) | [{"table": "asana__task_lifecycle_analysis", "column": "project_health_score"}] | [] | False |
| B1 | AVG(hours_assigned_to_completion) | [{"table": "asana__task_lifecycle_analysis", "column": "hours_assigned_to_completion"}] | [] | False |
| B1 | COUNT(*) | [] | [] | True |
| B1 | SUM(CASE WHEN is_completed = 1 THEN 1 ELSE 0 END) | [] | [{"table": "asana__task_lifecycle_analysis", "column": "is_completed"}] | False |

