# dacomp-052

Noticing that some teams have high project health scores but low actual completion rates, …

运行：已提交。官方未评分。全部 SQL 尝试/成功 27/27；数据 SQL 25/25；Python 2 次。

完整原题：

Noticing that some teams have high project health scores but low actual completion rates, you need to analyze teams from the `asana__team_efficiency_metrics` table where both `collaboration_efficiency_score` and `resource_optimization_score` are 8 or higher, but their `avg_completion_rate` is below 70%. Conduct an in-depth analysis of these teams' characteristics in terms of project size distribution, member workload, and task complexity to identify the underlying reasons for the mismatch between health scores and actual execution performance. Propose targeted team management optimization recommendations based on your findings.

| 表 | 行数 | 列数 |
| --- | --- | --- |
| asana__team_efficiency_metrics | 50 | 53 |


实际路线（分析者依据 SQL/源码概括，不代表 Agent 自述）：SQL 筛选高评分低完成率团队并比较特征 → Python 重新计算组均值与归一化图表 → 团队管理建议。

数据库大小：24,576 字节。

## 数据 SQL

| SQL | 状态 | 基础表 | Join 输入/类型 | GROUP BY | 聚合表达式 | 结果行数 | 数据库 ms |
| --- | --- | --- | --- | --- | --- | --- | --- |
| [S3/Q1](#s3) | success | ["asana__team_efficiency_metrics"] | 0 / {} | [] | ["COUNT(*)", "COUNT(DISTINCT team_id)"] | 1 | 0.405 |
| [S4/Q2](#s4) | success | ["asana__team_efficiency_metrics"] | 0 / {} | [] | ["MIN(avg_completion_rate)", "MAX(avg_completion_rate)", "AVG(avg_completion_rate)", "MIN(collaboration_efficiency_score)", "MAX(collaboration_efficiency_score)", "MIN(resource_optimization_score)", "MAX(resource_optimization_score)"] | 1 | 0.367 |
| [S5/Q3](#s5) | success | ["asana__team_efficiency_metrics"] | 0 / {} | [] | [] | 37 | 0.432 |
| [S6/Q4](#s6) | success | ["asana__team_efficiency_metrics"] | 0 / {} | ["collaboration_efficiency_score"] | ["COUNT(*)"] | 6 | 0.267 |
| [S7/Q5](#s7) | success | ["asana__team_efficiency_metrics"] | 0 / {} | ["resource_optimization_score"] | ["COUNT(*)"] | 4 | 0.268 |
| [S8/Q6](#s8) | success | ["asana__team_efficiency_metrics"] | 0 / {} | [] | [] | 13 | 0.52 |
| [S9/Q7](#s9) | success | ["asana__team_efficiency_metrics"] | 0 / {} | ["grp"] | ["COUNT(*)", "AVG(total_projects)", "AVG(enterprise_projects)", "AVG(large_projects)", "AVG(medium_projects)", "AVG(small_projects)", "AVG(unique_team_members)", "AVG(avg_tasks_per_member)", "AVG(high_workload_members)", "AVG(avg_tasks_per_assignee_across_projects)", "AVG(total_team_tasks)", "AVG(avg_estimated_completion_days)", "AVG(avg_project_velocity)"] | 2 | 0.677 |
| [S10/Q8](#s10) | success | ["asana__team_efficiency_metrics"] | 0 / {} | ["grp"] | ["AVG(avg_project_health)", "AVG(avg_project_performance)", "AVG(avg_completion_rate)", "AVG(avg_quality_rate)", "AVG(avg_risk_percentage)", "AVG(on_schedule_rate_pct)", "AVG(overdue_projects)", "AVG(overdue_team_tasks)", "AVG(active_projects)"] | 2 | 0.62 |
| [S11/Q9](#s11) | success | ["asana__team_efficiency_metrics"] | 0 / {} | ["grp", "team_size_category"] | ["COUNT(*)"] | 5 | 0.576 |
| [S12/Q10](#s12) | success | ["asana__team_efficiency_metrics"] | 0 / {} | ["grp", "workload_balance_status"] | ["COUNT(*)"] | 6 | 0.63 |
| [S13/Q11](#s13) | success | ["asana__team_efficiency_metrics"] | 0 / {} | ["grp", "team_maturity_level"] | ["COUNT(*)"] | 4 | 0.546 |
| [S14/Q12](#s14) | success | ["asana__team_efficiency_metrics"] | 0 / {} | ["grp", "efficiency_grade"] | ["COUNT(*)"] | 8 | 0.571 |
| [S15/Q13](#s15) | success | ["asana__team_efficiency_metrics"] | 0 / {} | ["grp"] | ["AVG(top_performers)", "AVG(high_performers)", "AVG(solid_performers)", "AVG(developing_performers)", "AVG(underperformers)", "AVG(high_risk_members)", "AVG(avg_member_performance)", "AVG(avg_member_completion_rate)", "AVG(avg_member_quality_rate)", "SUM(unique_team_members)", "SUM(unique_team_members)", "SUM(high_workload_members)", "SUM(high_risk_members)"] | 2 | 0.674 |
| [S16/Q14](#s16) | success | ["asana__team_efficiency_metrics"] | 0 / {} | ["grp"] | ["AVG(project_management_score)", "AVG(quality_management_score)", "AVG(collaboration_efficiency_score)", "AVG(resource_optimization_score)", "AVG(overall_team_efficiency_score)"] | 2 | 0.572 |
| [S17/Q15](#s17) | success | ["asana__team_efficiency_metrics"] | 0 / {} | [] | [] | 37 | 0.745 |
| [S18/Q16](#s18) | success | ["asana__team_efficiency_metrics"] | 0 / {} | [] | ["MIN((enterprise_projects + large_projects) * 100.0 / total_projects)", "MAX((enterprise_projects + large_projects) * 100.0 / total_projects)", "MIN(avg_estimated_completion_days)", "MAX(avg_estimated_completion_days)", "AVG((enterprise_projects + large_projects) * 100.0 / total_projects)", "AVG(avg_estimated_completion_days)", "AVG(overdue_team_tasks * 100.0 / total_team_tasks)", "AVG(active_team_tasks * 100.0 / total_team_tasks)", "AVG(completed_team_tasks * 100.0 / total_team_tasks)", "AVG(high_workload_members * 100.0 / unique_team_members)"] | 1 | 0.48 |
| [S19/Q17](#s19) | success | ["asana__team_efficiency_metrics"] | 0 / {} | [] | ["SUM(CASE WHEN (enterprise_projects + large_projects) * 100.0 / total_projects >= 50 THEN 1 ELSE 0 END)", "SUM(CASE WHEN avg_estimated_completion_days >= 75 THEN 1 ELSE 0 END)", "SUM(CASE WHEN high_workload_members * 100.0 / unique_team_members >= 50 THEN 1 ELSE 0 END)", "SUM(CASE WHEN avg_risk_percentage >= 30 THEN 1 ELSE 0 END)", "SUM(CASE WHEN on_schedule_rate_pct < 50 THEN 1 ELSE 0 END)", "COUNT(*)"] | 1 | 0.533 |
| [S20/Q18](#s20) | success | ["asana__team_efficiency_metrics"] | 0 / {} | [] | [] | 37 | 0.743 |
| [S21/Q19](#s21) | success | ["asana__team_efficiency_metrics"] | 0 / {} | ["improvement_recommendations"] | ["COUNT(*)"] | 5 | 0.538 |
| [S22/Q20](#s22) | success | ["asana__team_efficiency_metrics"] | 0 / {} | ["team_strengths"] | ["COUNT(*)"] | 1 | 0.529 |
| [S23/Q21](#s23) | success | ["asana__team_efficiency_metrics"] | 0 / {} | [] | ["AVG(efficiency_rank)", "AVG(performance_rank)", "AVG(schedule_reliability_rank)", "AVG(quality_rank)", "AVG(project_management_score)", "AVG(quality_management_score)", "AVG(avg_member_quality_rate)"] | 1 | 0.72 |
| [S24/Q22](#s24) | success | ["asana__team_efficiency_metrics"] | 0 / {} | [] | [] | 10 | 0.8 |
| [S25/Q23](#s25) | success | ["asana__team_efficiency_metrics"] | 0 / {} | ["grp"] | ["AVG(efficiency_rank)", "AVG(performance_rank)", "AVG(schedule_reliability_rank)", "AVG(quality_rank)", "AVG(project_management_score)", "AVG(quality_management_score)"] | 2 | 0.616 |
| [S26/Q24](#s26) | success | ["asana__team_efficiency_metrics"] | 0 / {} | ["grp"] | ["AVG(overdue_team_tasks * 100.0 / total_team_tasks)", "AVG(active_team_tasks * 100.0 / total_team_tasks)", "AVG(completed_team_tasks * 100.0 / total_team_tasks)", "AVG(overdue_projects * 100.0 / total_projects)"] | 2 | 0.599 |
| [S27/Q25](#s27) | success | ["asana__team_efficiency_metrics"] | 0 / {} | [] | [] | 50 | 1.001 |


## 元数据和设置

| SQL | 类别 | 状态 | 内容 |
| --- | --- | --- | --- |
| S1 | connection_setup | success | PRAGMA query_only=ON |
| S2 | metadata | success | SELECT name,sql FROM sqlite_master WHERE type='table' ORDER BY name |


## Python 与执行位置

人工源码审查：**database_first_violation**。Python 对团队级记录反复计算完成率、规模结构与工作负荷的跨团队均值，并比较目标组与其他团队；这些筛选和聚合可以在 SQL 内执行。绘图的样式和坐标转换单独保留。 [证据](../reviews/dacomp-052.json)。

P1：Compute correlations between completion rate and project-size mix, estimated duration, workload, and schedule metrics among the 37 target teams. Also produce visualizations showing the patterns. SQLite doesn't support correlation functions natively, and matplotlib is needed for figures.

[源码](../../../runs/dsv4flash-db-first-full-01/dacomp-052/attempt-01/python/P1.py)；[输出](../../../runs/dsv4flash-db-first-full-01/dacomp-052/attempt-01/python/P1.stdout)；[错误](../../../runs/dsv4flash-db-first-full-01/dacomp-052/attempt-01/python/P1.stderr)。检出需人工核验的 SQL 可实现操作：.query(；不能仅凭理由判为合规。

P2：Create a final comprehensive visualization comparing target vs. other teams across multiple dimensions (rank profiles, project size, workload, task status) to summarize the mismatch findings.

[源码](../../../runs/dsv4flash-db-first-full-01/dacomp-052/attempt-01/python/P2.py)；[输出](../../../runs/dsv4flash-db-first-full-01/dacomp-052/attempt-01/python/P2.stdout)；[错误](../../../runs/dsv4flash-db-first-full-01/dacomp-052/attempt-01/python/P2.stderr)。检出需人工核验的 SQL 可实现操作：.query(；不能仅凭理由判为合规。

## 优化机会

已验证候选。筛选限于精确 SQL、相同自包含 CTE、相同单表完整过滤、可分解单表聚合；未覆盖任意 Join 等价和一般谓词蕴含。全部候选都是 offline，未测在线预测。

| 候选 | 类型 | 已有结果 | 覆盖 SQL | 后续次数 | 中间行数 | 验证 | 成本 |
| --- | --- | --- | --- | --- | --- | --- | --- |
| C1 | common subexpression | False | ["S9", "S10", "S11", "S12", "S13", "S14", "S15", "S16", "S25", "S26"] | 9 | 50 | verified | Not benchmarked; correctness alone does not establish net speedup. |
| C2 | common subexpression | False | ["S19", "S21", "S22", "S23"] | 3 | 37 | verified | Not benchmarked; correctness alone does not establish net speedup. |
| C3 | aggregate MV | False | ["S4", "S6", "S7"] | 2 | unknown | not_verified_cap | Not tested |
| C4 | common filtered view | False | ["S5", "S17", "S18", "S20"] | 3 | 37 | verified | Not benchmarked; correctness alone does not establish net speedup. |


已验证覆盖（含触发查询、候选并集去重）：18/25 条成功数据 SQL。正确性仅针对当前数据库快照；未测性能的候选不能声称已加速。

[完整 build/rewrite 与比较证据](dacomp-052.analysis.json)。

### C1：common subexpression

Identical self-contained CTE body across queries.

原查询 [S9](#s9), [S10](#s10), [S11](#s11), [S12](#s12), [S13](#s13), [S14](#s14), [S15](#s15), [S16](#s16), [S25](#s25), [S26](#s26) → 新增共享状态 C1 → 后续 9 次可复用。该构建点为事后假设，不代表 Agent 当时预知后续。

构建定义：

```sql
SELECT *, CASE WHEN collaboration_efficiency_score >= 8 AND resource_optimization_score >= 8 AND avg_completion_rate < 70 THEN 'target' ELSE 'other' END AS grp FROM asana__team_efficiency_metrics
```

受益查询 S9 的改写示例：

```sql
WITH grp AS (SELECT * FROM temp.reuse_candidate) SELECT grp, COUNT(*) AS n, ROUND(AVG(total_projects), 2) AS avg_total_projects, ROUND(AVG(enterprise_projects), 2) AS avg_ent_proj, ROUND(AVG(large_projects), 2) AS avg_large_proj, ROUND(AVG(medium_projects), 2) AS avg_med_proj, ROUND(AVG(small_projects), 2) AS avg_small_proj, ROUND(AVG(unique_team_members), 2) AS avg_members, ROUND(AVG(avg_tasks_per_member), 2) AS avg_tasks_per_member, ROUND(AVG(high_workload_members), 2) AS avg_high_wl_members, ROUND(AVG(avg_tasks_per_assignee_across_projects), 2) AS avg_tasks_per_assignee, ROUND(AVG(total_team_tasks), 2) AS avg_total_tasks, ROUND(AVG(avg_estimated_completion_days), 2) AS avg_est_days, ROUND(AVG(avg_project_velocity), 2) AS avg_velocity FROM grp GROUP BY grp
```

| 原 SQL | 列名一致 | 结果一致 | 比较方法 |
| --- | --- | --- | --- |
| S9 | True | True | exact_multiset |
| S10 | True | True | exact_multiset |
| S11 | True | True | ordered_numeric_tolerance |
| S12 | True | True | ordered_numeric_tolerance |
| S13 | True | True | ordered_numeric_tolerance |
| S14 | True | True | ordered_numeric_tolerance |
| S15 | True | True | exact_multiset |
| S16 | True | True | exact_multiset |
| S25 | True | True | exact_multiset |
| S26 | True | True | exact_multiset |


验证状态：verified；成本结论：Not benchmarked; correctness alone does not establish net speedup.

### C2：common subexpression

Identical self-contained CTE body across queries.

原查询 [S19](#s19), [S21](#s21), [S22](#s22), [S23](#s23) → 新增共享状态 C2 → 后续 3 次可复用。该构建点为事后假设，不代表 Agent 当时预知后续。

构建定义：

```sql
SELECT * FROM asana__team_efficiency_metrics WHERE collaboration_efficiency_score >= 8 AND resource_optimization_score >= 8 AND avg_completion_rate < 70
```

受益查询 S19 的改写示例：

```sql
WITH target AS (SELECT * FROM temp.reuse_candidate) SELECT SUM(CASE WHEN (enterprise_projects + large_projects) * 100.0 / total_projects >= 50 THEN 1 ELSE 0 END) AS teams_ge50pct_large, SUM(CASE WHEN avg_estimated_completion_days >= 75 THEN 1 ELSE 0 END) AS teams_ge75_days, SUM(CASE WHEN high_workload_members * 100.0 / unique_team_members >= 50 THEN 1 ELSE 0 END) AS teams_ge50pct_high_wl, SUM(CASE WHEN avg_risk_percentage >= 30 THEN 1 ELSE 0 END) AS teams_ge30_risk, SUM(CASE WHEN on_schedule_rate_pct < 50 THEN 1 ELSE 0 END) AS teams_low_schedule, COUNT(*) AS n FROM target
```

| 原 SQL | 列名一致 | 结果一致 | 比较方法 |
| --- | --- | --- | --- |
| S19 | True | True | exact_multiset |
| S21 | True | True | ordered_numeric_tolerance |
| S22 | True | True | ordered_numeric_tolerance |
| S23 | True | True | exact_multiset |


验证状态：verified；成本结论：Not benchmarked; correctness alone does not establish net speedup.

### C4：common filtered view

Same single source and complete filter; original filter retained.

原查询 [S5](#s5), [S17](#s17), [S18](#s18), [S20](#s20) → 新增共享状态 C4 → 后续 3 次可复用。该构建点为事后假设，不代表 Agent 当时预知后续。

构建定义：

```sql
SELECT * FROM "asana__team_efficiency_metrics" WHERE collaboration_efficiency_score >= 8 AND resource_optimization_score >= 8 AND avg_completion_rate < 70
```

受益查询 S5 的改写示例：

```sql
SELECT team_id, team_name, collaboration_efficiency_score, resource_optimization_score, overall_team_efficiency_score, efficiency_grade, avg_completion_rate FROM temp.reuse_candidate AS asana__team_efficiency_metrics WHERE collaboration_efficiency_score >= 8 AND resource_optimization_score >= 8 AND avg_completion_rate < 70 ORDER BY avg_completion_rate DESC
```

| 原 SQL | 列名一致 | 结果一致 | 比较方法 |
| --- | --- | --- | --- |
| S5 | True | True | ordered_numeric_tolerance |
| S17 | True | True | ordered_numeric_tolerance |
| S18 | True | True | exact_multiset |
| S20 | True | True | exact_multiset |


验证状态：verified；成本结论：Not benchmarked; correctness alone does not establish net speedup.

结果依赖：自动记录 SQL→Python 的接口父调用，以及源码中引用归档文件的消费者；字面值相同不认定因果。模型方向选择需要人工读取消息，尚未做全面因果标注。

[原始报告](../../../runs/dsv4flash-db-first-full-01/dacomp-052/attempt-01/answer.md)；[统一消息](../../../runs/dsv4flash-db-first-full-01/dacomp-052/attempt-01/messages.jsonl)；[原始 OpenCode 事件](../../../runs/dsv4flash-db-first-full-01/dacomp-052/attempt-01/opencode.jsonl)；[SQL 引擎日志](../../../runs/dsv4flash-db-first-full-01/dacomp-052/attempt-01/sql_journal.jsonl)。

[可读报告（本地图片链接规范化）](../answers/dacomp-052.md)。原始回答保留，分析结论未改写。

## S1

类别 `connection_setup`；来源 `connection`；调用 `b3c3f1ae829642218887f90cc4c6b959`；状态 `success`。

```sql
PRAGMA query_only=ON
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-052/attempt-01/sql/S1.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-052/attempt-01/sql/S1.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-052/attempt-01/results/S1.rows.jsonl)；完整：True；SHA256：`e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`。

## S2

类别 `metadata`；来源 `list_db`；调用 `b3c3f1ae829642218887f90cc4c6b959`；状态 `success`。

```sql
SELECT name,sql FROM sqlite_master WHERE type='table' ORDER BY name
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-052/attempt-01/sql/S2.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-052/attempt-01/sql/S2.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-052/attempt-01/results/S2.rows.jsonl)；完整：True；SHA256：`57e4e07d82f453e5b251977f3e27775c9be1babfff750608497d1c6dc89bb97f`。

## S3

类别 `data`；来源 `query_db`；调用 `57a685c56e434f009178949ccef250cf`；状态 `success`。

```sql
SELECT COUNT(*) AS total_rows, COUNT(DISTINCT team_id) AS distinct_teams FROM asana__team_efficiency_metrics
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-052/attempt-01/sql/S3.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-052/attempt-01/sql/S3.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-052/attempt-01/results/S3.rows.jsonl)；完整：True；SHA256：`29fdc9d4c330911408d25240a6ee87bdeaac65594fdde42b3f727db574dc1ac0`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "asana__team_efficiency_metrics", "kind": "base", "block": null, "base_tables": ["asana__team_efficiency_metrics"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |
| B1 | COUNT(DISTINCT team_id) | [{"table": "asana__team_efficiency_metrics", "column": "team_id"}] | [] | False |


## S4

类别 `data`；来源 `query_db`；调用 `c4e87ec7af794b5d89ce5069422952f8`；状态 `success`。

```sql
SELECT MIN(avg_completion_rate) AS min_cr, MAX(avg_completion_rate) AS max_cr, AVG(avg_completion_rate) AS avg_cr, MIN(collaboration_efficiency_score) AS min_ce, MAX(collaboration_efficiency_score) AS max_ce, MIN(resource_optimization_score) AS min_ro, MAX(resource_optimization_score) AS max_ro FROM asana__team_efficiency_metrics
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-052/attempt-01/sql/S4.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-052/attempt-01/sql/S4.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-052/attempt-01/results/S4.rows.jsonl)；完整：True；SHA256：`4ff44e1431e2b47f3ccf0d1637bf11d16d32dd713888ea0dad2d9bfd085e7f4d`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "asana__team_efficiency_metrics", "kind": "base", "block": null, "base_tables": ["asana__team_efficiency_metrics"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | MIN(avg_completion_rate) | [{"table": "asana__team_efficiency_metrics", "column": "avg_completion_rate"}] | [] | False |
| B1 | MAX(avg_completion_rate) | [{"table": "asana__team_efficiency_metrics", "column": "avg_completion_rate"}] | [] | False |
| B1 | AVG(avg_completion_rate) | [{"table": "asana__team_efficiency_metrics", "column": "avg_completion_rate"}] | [] | False |
| B1 | MIN(collaboration_efficiency_score) | [{"table": "asana__team_efficiency_metrics", "column": "collaboration_efficiency_score"}] | [] | False |
| B1 | MAX(collaboration_efficiency_score) | [{"table": "asana__team_efficiency_metrics", "column": "collaboration_efficiency_score"}] | [] | False |
| B1 | MIN(resource_optimization_score) | [{"table": "asana__team_efficiency_metrics", "column": "resource_optimization_score"}] | [] | False |
| B1 | MAX(resource_optimization_score) | [{"table": "asana__team_efficiency_metrics", "column": "resource_optimization_score"}] | [] | False |


## S5

类别 `data`；来源 `query_db`；调用 `dac89e6aed9047d5b8b15d0bcb9d543f`；状态 `success`。

```sql
SELECT team_id, team_name, collaboration_efficiency_score, resource_optimization_score, overall_team_efficiency_score, efficiency_grade, avg_completion_rate FROM asana__team_efficiency_metrics WHERE collaboration_efficiency_score >= 8 AND resource_optimization_score >= 8 AND avg_completion_rate < 70 ORDER BY avg_completion_rate DESC
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-052/attempt-01/sql/S5.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-052/attempt-01/sql/S5.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-052/attempt-01/results/S5.rows.jsonl)；完整：True；SHA256：`bff88be4fdbb199900e0afafdf940ec2dfa5fc932fa45e8e5dcbf25d6d1ca50b`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "asana__team_efficiency_metrics", "kind": "base", "block": null, "base_tables": ["asana__team_efficiency_metrics"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |


## S6

类别 `data`；来源 `query_db`；调用 `8206a050a684407a89f0260c57f44825`；状态 `success`。

```sql
SELECT collaboration_efficiency_score, COUNT(*) AS n FROM asana__team_efficiency_metrics GROUP BY collaboration_efficiency_score ORDER BY collaboration_efficiency_score
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-052/attempt-01/sql/S6.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-052/attempt-01/sql/S6.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-052/attempt-01/results/S6.rows.jsonl)；完整：True；SHA256：`5c1484931609b48dbfbe77319da15ca97b494ea34919129feecb242a846c940e`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "asana__team_efficiency_metrics", "kind": "base", "block": null, "base_tables": ["asana__team_efficiency_metrics"]}] | [] | ["collaboration_efficiency_score"] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |


## S7

类别 `data`；来源 `query_db`；调用 `f2609bcb595644a69fac26ac7e1bb673`；状态 `success`。

```sql
SELECT resource_optimization_score, COUNT(*) AS n FROM asana__team_efficiency_metrics GROUP BY resource_optimization_score ORDER BY resource_optimization_score
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-052/attempt-01/sql/S7.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-052/attempt-01/sql/S7.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-052/attempt-01/results/S7.rows.jsonl)；完整：True；SHA256：`b60952d71b1917e28078891944d08aca0ceddc62aee5ea19011e5954c114747a`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "asana__team_efficiency_metrics", "kind": "base", "block": null, "base_tables": ["asana__team_efficiency_metrics"]}] | [] | ["resource_optimization_score"] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |


## S8

类别 `data`；来源 `query_db`；调用 `7476667b55134ef7b417c5da9f005387`；状态 `success`。

```sql
SELECT team_id, team_name, collaboration_efficiency_score, resource_optimization_score, avg_completion_rate FROM asana__team_efficiency_metrics WHERE NOT (collaboration_efficiency_score >= 8 AND resource_optimization_score >= 8) OR avg_completion_rate >= 70 ORDER BY avg_completion_rate DESC
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-052/attempt-01/sql/S8.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-052/attempt-01/sql/S8.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-052/attempt-01/results/S8.rows.jsonl)；完整：True；SHA256：`8b47c2938c9dd92a9f65d519c9ff71ee1a72f6a6fecf4ff1129bd6e9c5400991`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "asana__team_efficiency_metrics", "kind": "base", "block": null, "base_tables": ["asana__team_efficiency_metrics"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |


## S9

类别 `data`；来源 `query_db`；调用 `aa777939106e43958ba37ce5d5565309`；状态 `success`。

```sql
WITH grp AS (
  SELECT *, CASE WHEN collaboration_efficiency_score >= 8 AND resource_optimization_score >= 8 AND avg_completion_rate < 70 THEN 'target' ELSE 'other' END AS grp
  FROM asana__team_efficiency_metrics
)
SELECT grp, COUNT(*) AS n,
  ROUND(AVG(total_projects),2) AS avg_total_projects,
  ROUND(AVG(enterprise_projects),2) AS avg_ent_proj,
  ROUND(AVG(large_projects),2) AS avg_large_proj,
  ROUND(AVG(medium_projects),2) AS avg_med_proj,
  ROUND(AVG(small_projects),2) AS avg_small_proj,
  ROUND(AVG(unique_team_members),2) AS avg_members,
  ROUND(AVG(avg_tasks_per_member),2) AS avg_tasks_per_member,
  ROUND(AVG(high_workload_members),2) AS avg_high_wl_members,
  ROUND(AVG(avg_tasks_per_assignee_across_projects),2) AS avg_tasks_per_assignee,
  ROUND(AVG(total_team_tasks),2) AS avg_total_tasks,
  ROUND(AVG(avg_estimated_completion_days),2) AS avg_est_days,
  ROUND(AVG(avg_project_velocity),2) AS avg_velocity
FROM grp GROUP BY grp
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-052/attempt-01/sql/S9.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-052/attempt-01/sql/S9.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-052/attempt-01/results/S9.rows.jsonl)；完整：True；SHA256：`4de0421e9002e25687ca75e1e6497fbacf6411df3d364168618c1ac91018bfc5`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "asana__team_efficiency_metrics", "kind": "base", "block": null, "base_tables": ["asana__team_efficiency_metrics"]}] | [] | [] |
| B2 | [{"alias": "grp", "kind": "derived", "block": "B1", "base_tables": ["asana__team_efficiency_metrics"]}] | [] | ["grp"] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B2 | COUNT(*) | [] | [] | True |
| B2 | AVG(total_projects) | [{"table": "asana__team_efficiency_metrics", "column": "total_projects"}] | [] | False |
| B2 | AVG(enterprise_projects) | [{"table": "asana__team_efficiency_metrics", "column": "enterprise_projects"}] | [] | False |
| B2 | AVG(large_projects) | [{"table": "asana__team_efficiency_metrics", "column": "large_projects"}] | [] | False |
| B2 | AVG(medium_projects) | [{"table": "asana__team_efficiency_metrics", "column": "medium_projects"}] | [] | False |
| B2 | AVG(small_projects) | [{"table": "asana__team_efficiency_metrics", "column": "small_projects"}] | [] | False |
| B2 | AVG(unique_team_members) | [{"table": "asana__team_efficiency_metrics", "column": "unique_team_members"}] | [] | False |
| B2 | AVG(avg_tasks_per_member) | [{"table": "asana__team_efficiency_metrics", "column": "avg_tasks_per_member"}] | [] | False |
| B2 | AVG(high_workload_members) | [{"table": "asana__team_efficiency_metrics", "column": "high_workload_members"}] | [] | False |
| B2 | AVG(avg_tasks_per_assignee_across_projects) | [{"table": "asana__team_efficiency_metrics", "column": "avg_tasks_per_assignee_across_projects"}] | [] | False |
| B2 | AVG(total_team_tasks) | [{"table": "asana__team_efficiency_metrics", "column": "total_team_tasks"}] | [] | False |
| B2 | AVG(avg_estimated_completion_days) | [{"table": "asana__team_efficiency_metrics", "column": "avg_estimated_completion_days"}] | [] | False |
| B2 | AVG(avg_project_velocity) | [{"table": "asana__team_efficiency_metrics", "column": "avg_project_velocity"}] | [] | False |


## S10

类别 `data`；来源 `query_db`；调用 `364e34aa65d34593aadcf8403e042f55`；状态 `success`。

```sql
WITH grp AS (
  SELECT *, CASE WHEN collaboration_efficiency_score >= 8 AND resource_optimization_score >= 8 AND avg_completion_rate < 70 THEN 'target' ELSE 'other' END AS grp
  FROM asana__team_efficiency_metrics
)
SELECT grp,
  ROUND(AVG(avg_project_health),2) AS avg_health,
  ROUND(AVG(avg_project_performance),2) AS avg_performance,
  ROUND(AVG(avg_completion_rate),2) AS avg_completion,
  ROUND(AVG(avg_quality_rate),2) AS avg_quality,
  ROUND(AVG(avg_risk_percentage),2) AS avg_risk,
  ROUND(AVG(on_schedule_rate_pct),2) AS avg_on_schedule,
  ROUND(AVG(overdue_projects),2) AS avg_overdue_projects,
  ROUND(AVG(overdue_team_tasks),2) AS avg_overdue_tasks,
  ROUND(AVG(active_projects),2) AS avg_active_projects
FROM grp GROUP BY grp
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-052/attempt-01/sql/S10.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-052/attempt-01/sql/S10.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-052/attempt-01/results/S10.rows.jsonl)；完整：True；SHA256：`fa24f9f70e851459f47d3e9c95df6bef9cbfbdcef99b7b96e1f1026cad8161de`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "asana__team_efficiency_metrics", "kind": "base", "block": null, "base_tables": ["asana__team_efficiency_metrics"]}] | [] | [] |
| B2 | [{"alias": "grp", "kind": "derived", "block": "B1", "base_tables": ["asana__team_efficiency_metrics"]}] | [] | ["grp"] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B2 | AVG(avg_project_health) | [{"table": "asana__team_efficiency_metrics", "column": "avg_project_health"}] | [] | False |
| B2 | AVG(avg_project_performance) | [{"table": "asana__team_efficiency_metrics", "column": "avg_project_performance"}] | [] | False |
| B2 | AVG(avg_completion_rate) | [{"table": "asana__team_efficiency_metrics", "column": "avg_completion_rate"}] | [] | False |
| B2 | AVG(avg_quality_rate) | [{"table": "asana__team_efficiency_metrics", "column": "avg_quality_rate"}] | [] | False |
| B2 | AVG(avg_risk_percentage) | [{"table": "asana__team_efficiency_metrics", "column": "avg_risk_percentage"}] | [] | False |
| B2 | AVG(on_schedule_rate_pct) | [{"table": "asana__team_efficiency_metrics", "column": "on_schedule_rate_pct"}] | [] | False |
| B2 | AVG(overdue_projects) | [{"table": "asana__team_efficiency_metrics", "column": "overdue_projects"}] | [] | False |
| B2 | AVG(overdue_team_tasks) | [{"table": "asana__team_efficiency_metrics", "column": "overdue_team_tasks"}] | [] | False |
| B2 | AVG(active_projects) | [{"table": "asana__team_efficiency_metrics", "column": "active_projects"}] | [] | False |


## S11

类别 `data`；来源 `query_db`；调用 `9dca17daced14b50a5fedad4276b5cdd`；状态 `success`。

```sql
WITH grp AS (
  SELECT *, CASE WHEN collaboration_efficiency_score >= 8 AND resource_optimization_score >= 8 AND avg_completion_rate < 70 THEN 'target' ELSE 'other' END AS grp
  FROM asana__team_efficiency_metrics
)
SELECT grp, team_size_category, COUNT(*) AS n FROM grp GROUP BY grp, team_size_category ORDER BY grp, n DESC
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-052/attempt-01/sql/S11.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-052/attempt-01/sql/S11.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-052/attempt-01/results/S11.rows.jsonl)；完整：True；SHA256：`414884ea354274f8989e97bf6a1dad60dad64641e636ec3b55c8ee644fa9bcbe`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "asana__team_efficiency_metrics", "kind": "base", "block": null, "base_tables": ["asana__team_efficiency_metrics"]}] | [] | [] |
| B2 | [{"alias": "grp", "kind": "derived", "block": "B1", "base_tables": ["asana__team_efficiency_metrics"]}] | [] | ["grp", "team_size_category"] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B2 | COUNT(*) | [] | [] | True |


## S12

类别 `data`；来源 `query_db`；调用 `7dd6ca61bee94417a05b2c9062c3ff7a`；状态 `success`。

```sql
WITH grp AS (
  SELECT *, CASE WHEN collaboration_efficiency_score >= 8 AND resource_optimization_score >= 8 AND avg_completion_rate < 70 THEN 'target' ELSE 'other' END AS grp
  FROM asana__team_efficiency_metrics
)
SELECT grp, workload_balance_status, COUNT(*) AS n FROM grp GROUP BY grp, workload_balance_status ORDER BY grp, n DESC
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-052/attempt-01/sql/S12.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-052/attempt-01/sql/S12.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-052/attempt-01/results/S12.rows.jsonl)；完整：True；SHA256：`b19d8d19fb649ecceb1a534fd1743bc4aec624be95833b4331e19346ae7b9ce5`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "asana__team_efficiency_metrics", "kind": "base", "block": null, "base_tables": ["asana__team_efficiency_metrics"]}] | [] | [] |
| B2 | [{"alias": "grp", "kind": "derived", "block": "B1", "base_tables": ["asana__team_efficiency_metrics"]}] | [] | ["grp", "workload_balance_status"] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B2 | COUNT(*) | [] | [] | True |


## S13

类别 `data`；来源 `query_db`；调用 `491f20a968894f59b19dfaecde13dd7d`；状态 `success`。

```sql
WITH grp AS (
  SELECT *, CASE WHEN collaboration_efficiency_score >= 8 AND resource_optimization_score >= 8 AND avg_completion_rate < 70 THEN 'target' ELSE 'other' END AS grp
  FROM asana__team_efficiency_metrics
)
SELECT grp, team_maturity_level, COUNT(*) AS n FROM grp GROUP BY grp, team_maturity_level ORDER BY grp, n DESC
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-052/attempt-01/sql/S13.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-052/attempt-01/sql/S13.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-052/attempt-01/results/S13.rows.jsonl)；完整：True；SHA256：`b22cdabe5b0f302b5c790b802afee3f4d176f5754406ae8026b050ee78675190`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "asana__team_efficiency_metrics", "kind": "base", "block": null, "base_tables": ["asana__team_efficiency_metrics"]}] | [] | [] |
| B2 | [{"alias": "grp", "kind": "derived", "block": "B1", "base_tables": ["asana__team_efficiency_metrics"]}] | [] | ["grp", "team_maturity_level"] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B2 | COUNT(*) | [] | [] | True |


## S14

类别 `data`；来源 `query_db`；调用 `50bc73ec52334a3c961484a54c0baf4a`；状态 `success`。

```sql
WITH grp AS (
  SELECT *, CASE WHEN collaboration_efficiency_score >= 8 AND resource_optimization_score >= 8 AND avg_completion_rate < 70 THEN 'target' ELSE 'other' END AS grp
  FROM asana__team_efficiency_metrics
)
SELECT grp, efficiency_grade, COUNT(*) AS n FROM grp GROUP BY grp, efficiency_grade ORDER BY grp, n DESC
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-052/attempt-01/sql/S14.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-052/attempt-01/sql/S14.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-052/attempt-01/results/S14.rows.jsonl)；完整：True；SHA256：`d354a8a5fb7e62e885f0a98695e15284c4fe28d5c3bb890c615ff5ead73bbd5d`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "asana__team_efficiency_metrics", "kind": "base", "block": null, "base_tables": ["asana__team_efficiency_metrics"]}] | [] | [] |
| B2 | [{"alias": "grp", "kind": "derived", "block": "B1", "base_tables": ["asana__team_efficiency_metrics"]}] | [] | ["grp", "efficiency_grade"] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B2 | COUNT(*) | [] | [] | True |


## S15

类别 `data`；来源 `query_db`；调用 `7c65f697428448b4a8eb68ba0048a3eb`；状态 `success`。

```sql
WITH grp AS (
  SELECT *, CASE WHEN collaboration_efficiency_score >= 8 AND resource_optimization_score >= 8 AND avg_completion_rate < 70 THEN 'target' ELSE 'other' END AS grp
  FROM asana__team_efficiency_metrics
)
SELECT grp,
  ROUND(AVG(top_performers),2) AS avg_top,
  ROUND(AVG(high_performers),2) AS avg_high,
  ROUND(AVG(solid_performers),2) AS avg_solid,
  ROUND(AVG(developing_performers),2) AS avg_dev,
  ROUND(AVG(underperformers),2) AS avg_under,
  ROUND(AVG(high_risk_members),2) AS avg_high_risk,
  ROUND(AVG(avg_member_performance),2) AS avg_member_perf,
  ROUND(AVG(avg_member_completion_rate),2) AS avg_member_cr,
  ROUND(AVG(avg_member_quality_rate),2) AS avg_member_qr,
  ROUND(SUM(high_workload_members)*100.0/SUM(unique_team_members),2) AS pct_high_wl,
  ROUND(SUM(high_risk_members)*100.0/SUM(unique_team_members),2) AS pct_high_risk
FROM grp GROUP BY grp
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-052/attempt-01/sql/S15.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-052/attempt-01/sql/S15.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-052/attempt-01/results/S15.rows.jsonl)；完整：True；SHA256：`4095459ebe3d1dc359e2066909050f959d8079252919924c3d627b63e4be8b2c`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "asana__team_efficiency_metrics", "kind": "base", "block": null, "base_tables": ["asana__team_efficiency_metrics"]}] | [] | [] |
| B2 | [{"alias": "grp", "kind": "derived", "block": "B1", "base_tables": ["asana__team_efficiency_metrics"]}] | [] | ["grp"] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B2 | AVG(top_performers) | [{"table": "asana__team_efficiency_metrics", "column": "top_performers"}] | [] | False |
| B2 | AVG(high_performers) | [{"table": "asana__team_efficiency_metrics", "column": "high_performers"}] | [] | False |
| B2 | AVG(solid_performers) | [{"table": "asana__team_efficiency_metrics", "column": "solid_performers"}] | [] | False |
| B2 | AVG(developing_performers) | [{"table": "asana__team_efficiency_metrics", "column": "developing_performers"}] | [] | False |
| B2 | AVG(underperformers) | [{"table": "asana__team_efficiency_metrics", "column": "underperformers"}] | [] | False |
| B2 | AVG(high_risk_members) | [{"table": "asana__team_efficiency_metrics", "column": "high_risk_members"}] | [] | False |
| B2 | AVG(avg_member_performance) | [{"table": "asana__team_efficiency_metrics", "column": "avg_member_performance"}] | [] | False |
| B2 | AVG(avg_member_completion_rate) | [{"table": "asana__team_efficiency_metrics", "column": "avg_member_completion_rate"}] | [] | False |
| B2 | AVG(avg_member_quality_rate) | [{"table": "asana__team_efficiency_metrics", "column": "avg_member_quality_rate"}] | [] | False |
| B2 | SUM(unique_team_members) | [{"table": "asana__team_efficiency_metrics", "column": "unique_team_members"}] | [] | False |
| B2 | SUM(unique_team_members) | [{"table": "asana__team_efficiency_metrics", "column": "unique_team_members"}] | [] | False |
| B2 | SUM(high_workload_members) | [{"table": "asana__team_efficiency_metrics", "column": "high_workload_members"}] | [] | False |
| B2 | SUM(high_risk_members) | [{"table": "asana__team_efficiency_metrics", "column": "high_risk_members"}] | [] | False |


## S16

类别 `data`；来源 `query_db`；调用 `a0968e28c49a45638f98ef2b0cd73ea2`；状态 `success`。

```sql
WITH grp AS (
  SELECT *, CASE WHEN collaboration_efficiency_score >= 8 AND resource_optimization_score >= 8 AND avg_completion_rate < 70 THEN 'target' ELSE 'other' END AS grp
  FROM asana__team_efficiency_metrics
)
SELECT grp,
  ROUND(AVG(project_management_score),2) AS avg_pm,
  ROUND(AVG(quality_management_score),2) AS avg_qm,
  ROUND(AVG(collaboration_efficiency_score),2) AS avg_ce,
  ROUND(AVG(resource_optimization_score),2) AS avg_ro,
  ROUND(AVG(overall_team_efficiency_score),2) AS avg_eff
FROM grp GROUP BY grp
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-052/attempt-01/sql/S16.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-052/attempt-01/sql/S16.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-052/attempt-01/results/S16.rows.jsonl)；完整：True；SHA256：`13c0be68ddb1a860c9afd7bbfd2cda56e4903f38a3c41941e903933365a21ee8`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "asana__team_efficiency_metrics", "kind": "base", "block": null, "base_tables": ["asana__team_efficiency_metrics"]}] | [] | [] |
| B2 | [{"alias": "grp", "kind": "derived", "block": "B1", "base_tables": ["asana__team_efficiency_metrics"]}] | [] | ["grp"] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B2 | AVG(project_management_score) | [{"table": "asana__team_efficiency_metrics", "column": "project_management_score"}] | [] | False |
| B2 | AVG(quality_management_score) | [{"table": "asana__team_efficiency_metrics", "column": "quality_management_score"}] | [] | False |
| B2 | AVG(collaboration_efficiency_score) | [{"table": "asana__team_efficiency_metrics", "column": "collaboration_efficiency_score"}] | [] | False |
| B2 | AVG(resource_optimization_score) | [{"table": "asana__team_efficiency_metrics", "column": "resource_optimization_score"}] | [] | False |
| B2 | AVG(overall_team_efficiency_score) | [{"table": "asana__team_efficiency_metrics", "column": "overall_team_efficiency_score"}] | [] | False |


## S17

类别 `data`；来源 `query_db`；调用 `8b8015e79d7644279e357b1b9feeb431`；状态 `success`。

```sql
SELECT team_name, team_size_category, workload_balance_status, team_maturity_level, efficiency_grade,
  total_projects, enterprise_projects, large_projects, medium_projects, small_projects,
  avg_completion_rate, avg_project_health, avg_project_performance, avg_quality_rate,
  unique_team_members, avg_tasks_per_member, high_workload_members, high_risk_members,
  avg_estimated_completion_days, on_schedule_rate_pct, avg_risk_percentage,
  overdue_projects, overdue_team_tasks, total_team_tasks, completed_team_tasks,
  overall_team_efficiency_score, improvement_recommendations, team_strengths
FROM asana__team_efficiency_metrics
WHERE collaboration_efficiency_score >= 8 AND resource_optimization_score >= 8 AND avg_completion_rate < 70
ORDER BY avg_completion_rate DESC
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-052/attempt-01/sql/S17.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-052/attempt-01/sql/S17.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-052/attempt-01/results/S17.rows.jsonl)；完整：True；SHA256：`54e76b4328f31170c315db49b9fb56aa763ea0fb0d76f584156c2e942736abf1`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "asana__team_efficiency_metrics", "kind": "base", "block": null, "base_tables": ["asana__team_efficiency_metrics"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |


## S18

类别 `data`；来源 `query_db`；调用 `36a583bf2876405f8d8a298df538e43b`；状态 `success`。

```sql
SELECT
  ROUND(AVG((enterprise_projects+large_projects)*100.0/total_projects),1) AS avg_pct_large_ent,
  MIN((enterprise_projects+large_projects)*100.0/total_projects) AS min_pct_large_ent,
  MAX((enterprise_projects+large_projects)*100.0/total_projects) AS max_pct_large_ent,
  ROUND(AVG(avg_estimated_completion_days),1) AS avg_est_days_target,
  MIN(avg_estimated_completion_days) AS min_days,
  MAX(avg_estimated_completion_days) AS max_days,
  ROUND(AVG(overdue_team_tasks*100.0/total_team_tasks),1) AS avg_pct_overdue_tasks,
  ROUND(AVG(active_team_tasks*100.0/total_team_tasks),1) AS avg_pct_active_tasks,
  ROUND(AVG(completed_team_tasks*100.0/total_team_tasks),1) AS avg_pct_completed_tasks,
  ROUND(AVG(high_workload_members*100.0/unique_team_members),1) AS avg_pct_high_wl
FROM asana__team_efficiency_metrics
WHERE collaboration_efficiency_score >= 8 AND resource_optimization_score >= 8 AND avg_completion_rate < 70
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-052/attempt-01/sql/S18.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-052/attempt-01/sql/S18.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-052/attempt-01/results/S18.rows.jsonl)；完整：True；SHA256：`4a7bde5a4a9e4c8a89f67643c4f3dffd197474a1b9abfa7ddb1cdf2e5364a2e4`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "asana__team_efficiency_metrics", "kind": "base", "block": null, "base_tables": ["asana__team_efficiency_metrics"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | MIN((enterprise_projects + large_projects) * 100.0 / total_projects) | [{"table": "asana__team_efficiency_metrics", "column": "total_projects"}, {"table": "asana__team_efficiency_metrics", "column": "enterprise_projects"}, {"table": "asana__team_efficiency_metrics", "column": "large_projects"}] | [] | False |
| B1 | MAX((enterprise_projects + large_projects) * 100.0 / total_projects) | [{"table": "asana__team_efficiency_metrics", "column": "total_projects"}, {"table": "asana__team_efficiency_metrics", "column": "enterprise_projects"}, {"table": "asana__team_efficiency_metrics", "column": "large_projects"}] | [] | False |
| B1 | MIN(avg_estimated_completion_days) | [{"table": "asana__team_efficiency_metrics", "column": "avg_estimated_completion_days"}] | [] | False |
| B1 | MAX(avg_estimated_completion_days) | [{"table": "asana__team_efficiency_metrics", "column": "avg_estimated_completion_days"}] | [] | False |
| B1 | AVG((enterprise_projects + large_projects) * 100.0 / total_projects) | [{"table": "asana__team_efficiency_metrics", "column": "total_projects"}, {"table": "asana__team_efficiency_metrics", "column": "enterprise_projects"}, {"table": "asana__team_efficiency_metrics", "column": "large_projects"}] | [] | False |
| B1 | AVG(avg_estimated_completion_days) | [{"table": "asana__team_efficiency_metrics", "column": "avg_estimated_completion_days"}] | [] | False |
| B1 | AVG(overdue_team_tasks * 100.0 / total_team_tasks) | [{"table": "asana__team_efficiency_metrics", "column": "total_team_tasks"}, {"table": "asana__team_efficiency_metrics", "column": "overdue_team_tasks"}] | [] | False |
| B1 | AVG(active_team_tasks * 100.0 / total_team_tasks) | [{"table": "asana__team_efficiency_metrics", "column": "total_team_tasks"}, {"table": "asana__team_efficiency_metrics", "column": "active_team_tasks"}] | [] | False |
| B1 | AVG(completed_team_tasks * 100.0 / total_team_tasks) | [{"table": "asana__team_efficiency_metrics", "column": "total_team_tasks"}, {"table": "asana__team_efficiency_metrics", "column": "completed_team_tasks"}] | [] | False |
| B1 | AVG(high_workload_members * 100.0 / unique_team_members) | [{"table": "asana__team_efficiency_metrics", "column": "unique_team_members"}, {"table": "asana__team_efficiency_metrics", "column": "high_workload_members"}] | [] | False |


## S19

类别 `data`；来源 `query_db`；调用 `bc0e94f9ca1f449bb347cb9f9f125cd9`；状态 `success`。

```sql
WITH target AS (
  SELECT * FROM asana__team_efficiency_metrics
  WHERE collaboration_efficiency_score >= 8 AND resource_optimization_score >= 8 AND avg_completion_rate < 70
)
SELECT
  SUM(CASE WHEN (enterprise_projects+large_projects)*100.0/total_projects >= 50 THEN 1 ELSE 0 END) AS teams_ge50pct_large,
  SUM(CASE WHEN avg_estimated_completion_days >= 75 THEN 1 ELSE 0 END) AS teams_ge75_days,
  SUM(CASE WHEN high_workload_members*100.0/unique_team_members >= 50 THEN 1 ELSE 0 END) AS teams_ge50pct_high_wl,
  SUM(CASE WHEN avg_risk_percentage >= 30 THEN 1 ELSE 0 END) AS teams_ge30_risk,
  SUM(CASE WHEN on_schedule_rate_pct < 50 THEN 1 ELSE 0 END) AS teams_low_schedule,
  COUNT(*) AS n
FROM target
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-052/attempt-01/sql/S19.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-052/attempt-01/sql/S19.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-052/attempt-01/results/S19.rows.jsonl)；完整：True；SHA256：`8712045a986fc2bef50c64e64a0a2dc1e04ee4643ccd7d59e32009b193d1e931`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "asana__team_efficiency_metrics", "kind": "base", "block": null, "base_tables": ["asana__team_efficiency_metrics"]}] | [] | [] |
| B2 | [{"alias": "target", "kind": "derived", "block": "B1", "base_tables": ["asana__team_efficiency_metrics"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B2 | SUM(CASE WHEN (enterprise_projects + large_projects) * 100.0 / total_projects >= 50 THEN 1 ELSE 0 END) | [] | [{"table": "asana__team_efficiency_metrics", "column": "total_projects"}, {"table": "asana__team_efficiency_metrics", "column": "enterprise_projects"}, {"table": "asana__team_efficiency_metrics", "column": "large_projects"}] | False |
| B2 | SUM(CASE WHEN avg_estimated_completion_days >= 75 THEN 1 ELSE 0 END) | [] | [{"table": "asana__team_efficiency_metrics", "column": "avg_estimated_completion_days"}] | False |
| B2 | SUM(CASE WHEN high_workload_members * 100.0 / unique_team_members >= 50 THEN 1 ELSE 0 END) | [] | [{"table": "asana__team_efficiency_metrics", "column": "unique_team_members"}, {"table": "asana__team_efficiency_metrics", "column": "high_workload_members"}] | False |
| B2 | SUM(CASE WHEN avg_risk_percentage >= 30 THEN 1 ELSE 0 END) | [] | [{"table": "asana__team_efficiency_metrics", "column": "avg_risk_percentage"}] | False |
| B2 | SUM(CASE WHEN on_schedule_rate_pct < 50 THEN 1 ELSE 0 END) | [] | [{"table": "asana__team_efficiency_metrics", "column": "on_schedule_rate_pct"}] | False |
| B2 | COUNT(*) | [] | [] | True |


## S20

类别 `data`；来源 `python`；调用 `eb1e24ac108a404596fb5980aff9f7ee`；状态 `success`。

```sql

SELECT team_name, team_size_category, workload_balance_status, team_maturity_level,
  total_projects, enterprise_projects, large_projects, medium_projects, small_projects,
  avg_completion_rate, avg_project_health, avg_project_performance, avg_quality_rate,
  unique_team_members, avg_tasks_per_member, high_workload_members, high_risk_members,
  avg_estimated_completion_days, on_schedule_rate_pct, avg_risk_percentage,
  overdue_projects, overdue_team_tasks, total_team_tasks, completed_team_tasks,
  active_team_tasks, avg_project_velocity, avg_member_completion_rate,
  avg_tasks_per_assignee_across_projects, total_project_assignments,
  top_performers, high_performers, solid_performers, developing_performers, underperformers
FROM asana__team_efficiency_metrics
WHERE collaboration_efficiency_score >= 8 AND resource_optimization_score >= 8 AND avg_completion_rate < 70

```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-052/attempt-01/sql/S20.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-052/attempt-01/sql/S20.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-052/attempt-01/results/S20.rows.jsonl)；完整：True；SHA256：`6d9fae3f17b3bd2910f9a6f5c44cb7b572c9f60269215a3f9c46e2cb757a7d5b`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "asana__team_efficiency_metrics", "kind": "base", "block": null, "base_tables": ["asana__team_efficiency_metrics"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |


## S21

类别 `data`；来源 `query_db`；调用 `3df7d9cf17434964913bd1ea307924c1`；状态 `success`。

```sql
WITH target AS (
  SELECT * FROM asana__team_efficiency_metrics
  WHERE collaboration_efficiency_score >= 8 AND resource_optimization_score >= 8 AND avg_completion_rate < 70
)
SELECT improvement_recommendations, COUNT(*) AS n
FROM target GROUP BY improvement_recommendations ORDER BY n DESC
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-052/attempt-01/sql/S21.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-052/attempt-01/sql/S21.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-052/attempt-01/results/S21.rows.jsonl)；完整：True；SHA256：`0e01b04a21df909056183046ce4f113675faada8717bc11c0ea557e3c7469d9d`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "asana__team_efficiency_metrics", "kind": "base", "block": null, "base_tables": ["asana__team_efficiency_metrics"]}] | [] | [] |
| B2 | [{"alias": "target", "kind": "derived", "block": "B1", "base_tables": ["asana__team_efficiency_metrics"]}] | [] | ["improvement_recommendations"] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B2 | COUNT(*) | [] | [] | True |


## S22

类别 `data`；来源 `query_db`；调用 `4bcfe7793e124aa5a51a74abb5b8dec4`；状态 `success`。

```sql
WITH target AS (
  SELECT * FROM asana__team_efficiency_metrics
  WHERE collaboration_efficiency_score >= 8 AND resource_optimization_score >= 8 AND avg_completion_rate < 70
)
SELECT team_strengths, COUNT(*) AS n
FROM target GROUP BY team_strengths ORDER BY n DESC
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-052/attempt-01/sql/S22.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-052/attempt-01/sql/S22.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-052/attempt-01/results/S22.rows.jsonl)；完整：True；SHA256：`7115165384622ec3781bd29ff2ebdd3f2bbfb23e212a718839449c34755329f0`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "asana__team_efficiency_metrics", "kind": "base", "block": null, "base_tables": ["asana__team_efficiency_metrics"]}] | [] | [] |
| B2 | [{"alias": "target", "kind": "derived", "block": "B1", "base_tables": ["asana__team_efficiency_metrics"]}] | [] | ["team_strengths"] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B2 | COUNT(*) | [] | [] | True |


## S23

类别 `data`；来源 `query_db`；调用 `9320b63e199b47b5adcb375cbd1f823b`；状态 `success`。

```sql
WITH target AS (
  SELECT * FROM asana__team_efficiency_metrics
  WHERE collaboration_efficiency_score >= 8 AND resource_optimization_score >= 8 AND avg_completion_rate < 70
)
SELECT
  ROUND(AVG(efficiency_rank),1) AS avg_eff_rank,
  ROUND(AVG(performance_rank),1) AS avg_perf_rank,
  ROUND(AVG(schedule_reliability_rank),1) AS avg_sched_rank,
  ROUND(AVG(quality_rank),1) AS avg_quality_rank,
  ROUND(AVG(project_management_score),1) AS avg_pm_score,
  ROUND(AVG(quality_management_score),1) AS avg_qm_score,
  ROUND(AVG(avg_member_quality_rate),1) AS avg_member_quality
FROM target
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-052/attempt-01/sql/S23.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-052/attempt-01/sql/S23.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-052/attempt-01/results/S23.rows.jsonl)；完整：True；SHA256：`b3197d72076ad7e5277aaf0ef4753bccff681a73cf28eb3e882473442163da4d`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "asana__team_efficiency_metrics", "kind": "base", "block": null, "base_tables": ["asana__team_efficiency_metrics"]}] | [] | [] |
| B2 | [{"alias": "target", "kind": "derived", "block": "B1", "base_tables": ["asana__team_efficiency_metrics"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B2 | AVG(efficiency_rank) | [{"table": "asana__team_efficiency_metrics", "column": "efficiency_rank"}] | [] | False |
| B2 | AVG(performance_rank) | [{"table": "asana__team_efficiency_metrics", "column": "performance_rank"}] | [] | False |
| B2 | AVG(schedule_reliability_rank) | [{"table": "asana__team_efficiency_metrics", "column": "schedule_reliability_rank"}] | [] | False |
| B2 | AVG(quality_rank) | [{"table": "asana__team_efficiency_metrics", "column": "quality_rank"}] | [] | False |
| B2 | AVG(project_management_score) | [{"table": "asana__team_efficiency_metrics", "column": "project_management_score"}] | [] | False |
| B2 | AVG(quality_management_score) | [{"table": "asana__team_efficiency_metrics", "column": "quality_management_score"}] | [] | False |
| B2 | AVG(avg_member_quality_rate) | [{"table": "asana__team_efficiency_metrics", "column": "avg_member_quality_rate"}] | [] | False |


## S24

类别 `data`；来源 `query_db`；调用 `e8ca3e7849634e26beda51c4fe5068c0`；状态 `success`。

```sql
WITH target AS (
  SELECT team_id, team_name, avg_completion_rate,
    avg_project_health, avg_quality_rate, on_schedule_rate_pct,
    avg_estimated_completion_days, (enterprise_projects+large_projects)*100.0/total_projects AS pct_large_ent,
    high_workload_members*100.0/unique_team_members AS pct_high_wl,
    RANK() OVER (ORDER BY avg_completion_rate ASC) AS low_completion_rank
  FROM asana__team_efficiency_metrics
  WHERE collaboration_efficiency_score >= 8 AND resource_optimization_score >= 8 AND avg_completion_rate < 70
)
SELECT * FROM target ORDER BY avg_completion_rate ASC LIMIT 10
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-052/attempt-01/sql/S24.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-052/attempt-01/sql/S24.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-052/attempt-01/results/S24.rows.jsonl)；完整：True；SHA256：`db8e59727160c071396aa282ab3de2409fbb92aedd73e4b92b3209be5fe95c3c`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "asana__team_efficiency_metrics", "kind": "base", "block": null, "base_tables": ["asana__team_efficiency_metrics"]}] | [] | [] |
| B2 | [{"alias": "target", "kind": "derived", "block": "B1", "base_tables": ["asana__team_efficiency_metrics"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |


## S25

类别 `data`；来源 `query_db`；调用 `0f6738238b8340cf88af96fb5a3bb011`；状态 `success`。

```sql
WITH grp AS (
  SELECT *, CASE WHEN collaboration_efficiency_score >= 8 AND resource_optimization_score >= 8 AND avg_completion_rate < 70 THEN 'target' ELSE 'other' END AS grp
  FROM asana__team_efficiency_metrics
)
SELECT grp,
  ROUND(AVG(efficiency_rank),1) AS avg_eff_rank,
  ROUND(AVG(performance_rank),1) AS avg_perf_rank,
  ROUND(AVG(schedule_reliability_rank),1) AS avg_sched_rank,
  ROUND(AVG(quality_rank),1) AS avg_quality_rank,
  ROUND(AVG(project_management_score),1) AS avg_pm,
  ROUND(AVG(quality_management_score),1) AS avg_qm
FROM grp GROUP BY grp
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-052/attempt-01/sql/S25.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-052/attempt-01/sql/S25.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-052/attempt-01/results/S25.rows.jsonl)；完整：True；SHA256：`108c7c1ee61128cac64540d5cf9e27c726c98e4595e77153cf5ba4f19b6aadff`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "asana__team_efficiency_metrics", "kind": "base", "block": null, "base_tables": ["asana__team_efficiency_metrics"]}] | [] | [] |
| B2 | [{"alias": "grp", "kind": "derived", "block": "B1", "base_tables": ["asana__team_efficiency_metrics"]}] | [] | ["grp"] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B2 | AVG(efficiency_rank) | [{"table": "asana__team_efficiency_metrics", "column": "efficiency_rank"}] | [] | False |
| B2 | AVG(performance_rank) | [{"table": "asana__team_efficiency_metrics", "column": "performance_rank"}] | [] | False |
| B2 | AVG(schedule_reliability_rank) | [{"table": "asana__team_efficiency_metrics", "column": "schedule_reliability_rank"}] | [] | False |
| B2 | AVG(quality_rank) | [{"table": "asana__team_efficiency_metrics", "column": "quality_rank"}] | [] | False |
| B2 | AVG(project_management_score) | [{"table": "asana__team_efficiency_metrics", "column": "project_management_score"}] | [] | False |
| B2 | AVG(quality_management_score) | [{"table": "asana__team_efficiency_metrics", "column": "quality_management_score"}] | [] | False |


## S26

类别 `data`；来源 `query_db`；调用 `bec09a7c9684401d82c98ed2fb0145d4`；状态 `success`。

```sql
WITH grp AS (
  SELECT *, CASE WHEN collaboration_efficiency_score >= 8 AND resource_optimization_score >= 8 AND avg_completion_rate < 70 THEN 'target' ELSE 'other' END AS grp
  FROM asana__team_efficiency_metrics
)
SELECT grp, ROUND(AVG(overdue_team_tasks*100.0/total_team_tasks),1) AS pct_overdue_tasks,
  ROUND(AVG(active_team_tasks*100.0/total_team_tasks),1) AS pct_active_tasks,
  ROUND(AVG(completed_team_tasks*100.0/total_team_tasks),1) AS pct_completed_tasks,
  ROUND(AVG(overdue_projects*100.0/total_projects),1) AS pct_overdue_projects
FROM grp GROUP BY grp
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-052/attempt-01/sql/S26.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-052/attempt-01/sql/S26.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-052/attempt-01/results/S26.rows.jsonl)；完整：True；SHA256：`3f84f930080cd79a858a7123c3d90c5bd42a5e3cee771e05044aa7bf46ef55f3`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "asana__team_efficiency_metrics", "kind": "base", "block": null, "base_tables": ["asana__team_efficiency_metrics"]}] | [] | [] |
| B2 | [{"alias": "grp", "kind": "derived", "block": "B1", "base_tables": ["asana__team_efficiency_metrics"]}] | [] | ["grp"] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B2 | AVG(overdue_team_tasks * 100.0 / total_team_tasks) | [{"table": "asana__team_efficiency_metrics", "column": "total_team_tasks"}, {"table": "asana__team_efficiency_metrics", "column": "overdue_team_tasks"}] | [] | False |
| B2 | AVG(active_team_tasks * 100.0 / total_team_tasks) | [{"table": "asana__team_efficiency_metrics", "column": "total_team_tasks"}, {"table": "asana__team_efficiency_metrics", "column": "active_team_tasks"}] | [] | False |
| B2 | AVG(completed_team_tasks * 100.0 / total_team_tasks) | [{"table": "asana__team_efficiency_metrics", "column": "total_team_tasks"}, {"table": "asana__team_efficiency_metrics", "column": "completed_team_tasks"}] | [] | False |
| B2 | AVG(overdue_projects * 100.0 / total_projects) | [{"table": "asana__team_efficiency_metrics", "column": "total_projects"}, {"table": "asana__team_efficiency_metrics", "column": "overdue_projects"}] | [] | False |


## S27

类别 `data`；来源 `python`；调用 `02ccf5876bda4717b441a43efe0c6ef1`；状态 `success`。

```sql

SELECT *, 
  CASE WHEN collaboration_efficiency_score >= 8 AND resource_optimization_score >= 8 AND avg_completion_rate < 70 THEN 'target' ELSE 'other' END AS grp
FROM asana__team_efficiency_metrics

```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-052/attempt-01/sql/S27.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-052/attempt-01/sql/S27.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-052/attempt-01/results/S27.rows.jsonl)；完整：True；SHA256：`b2593977bd9687ec921b54e541f9744add024a7dcf8e68f40307cf629a1562c5`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "asana__team_efficiency_metrics", "kind": "base", "block": null, "base_tables": ["asana__team_efficiency_metrics"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |

