# dacomp-062

I want to understand the effectiveness of our cross-functional collaboration. Please analy…

运行：已提交。官方未评分。全部 SQL 尝试/成功 33/31；数据 SQL 30/28；Python 5 次。

完整原题：

I want to understand the effectiveness of our cross-functional collaboration. Please analyze whether stakeholders with a high number of `direct_network_connections` actually lead to better project outcomes, paying special attention to the performance of the projects they are involved in regarding `complexity_risk_score` and `success_probability`.

| 表 | 行数 | 列数 |
| --- | --- | --- |
| jira__project_risk_assessment | 200 | 31 |
| jira__stakeholder_engagement_insights | 4524 | 23 |


实际路线（分析者依据 SQL/源码概括，不代表 Agent 自述）：SQL 描述利益相关者连接和项目风险 → Python 相关分析及层次聚类 → 项目画像与协作建议。

数据库大小：1,007,616 字节。

## 数据 SQL

| SQL | 状态 | 基础表 | Join 输入/类型 | GROUP BY | 聚合表达式 | 结果行数 | 数据库 ms |
| --- | --- | --- | --- | --- | --- | --- | --- |
| [S3/Q1](#s3) | success | ["jira__project_risk_assessment"] | 0 / {} | [] | [] | 5 | 0.395 |
| [S4/Q2](#s4) | success | ["jira__stakeholder_engagement_insights"] | 0 / {} | [] | [] | 5 | 0.387 |
| [S6/Q3](#s6) | success | ["jira__project_risk_assessment"] | 0 / {} | [] | ["COUNT(*)"] | 1 | 0.371 |
| [S7/Q4](#s7) | success | ["jira__stakeholder_engagement_insights"] | 0 / {} | [] | ["COUNT(*)"] | 1 | 1.081 |
| [S8/Q5](#s8) | failed | ["jira__stakeholder_engagement_insights"] | 0 / {} | [] | ["MIN(direct_network_connections)", "AVG(direct_network_connections)", "MAX(direct_network_connections)", "PERCENTILE_CONT(direct_network_connections, 0.5)", "STDDEV(direct_network_connections)"] | unknown | 未取得；调用总时长 0.168 ms |
| [S9/Q6](#s9) | failed | ["jira__project_risk_assessment"] | 0 / {} | [] | ["MIN(complexity_risk_score)", "AVG(complexity_risk_score)", "MAX(complexity_risk_score)", "PERCENTILE_CONT(complexity_risk_score, 0.5)", "STDDEV(complexity_risk_score)", "MIN(success_probability)", "AVG(success_probability)", "MAX(success_probability)", "PERCENTILE_CONT(success_probability, 0.5)", "STDDEV(success_probability)"] | unknown | 未取得；调用总时长 0.159 ms |
| [S10/Q7](#s10) | success | ["jira__stakeholder_engagement_insights"] | 0 / {} | ["total_projects_involved"] | ["AVG(direct_network_connections)", "COUNT(*)"] | 12 | 2.252 |
| [S11/Q8](#s11) | success | ["jira__stakeholder_engagement_insights"] | 0 / {} | ["influence_level"] | ["COUNT(*)", "AVG(direct_network_connections)", "MIN(direct_network_connections)", "MAX(direct_network_connections)", "AVG(cross_functional_projects)", "AVG(total_engagement_score)"] | 5 | 3.381 |
| [S12/Q9](#s12) | success | ["jira__project_risk_assessment"] | 0 / {} | ["risk_category"] | ["COUNT(*)", "AVG(complexity_risk_score)", "AVG(success_probability)", "AVG(total_risk_score)", "AVG(overall_health_score)"] | 3 | 0.587 |
| [S13/Q10](#s13) | success | ["jira__project_risk_assessment"] | 0 / {} | ["trajectory_status"] | ["COUNT(*)", "AVG(complexity_risk_score)", "AVG(success_probability)", "AVG(delivered_value_points)", "AVG(value_delivery_percentage)"] | 4 | 0.494 |
| [S14/Q11](#s14) | success | ["jira__stakeholder_engagement_insights"] | 0 / {} | ["CASE WHEN direct_network_connections <= 5 THEN '1_low_(<=5)' WHEN direct_network_connections <= 10 THEN '2_mid_low_(6-10)' WHEN direct_network_connections <= 20 THEN '3_mid_(11-20)' WHEN direct_network_connections <= 35 THEN '4_high_(21-35)' ELSE '5_very_high_(>35)' END"] | ["COUNT(*)", "AVG(total_projects_involved)", "AVG(cross_functional_projects)", "AVG(total_engagement_score)", "AVG(total_inbound_influence)", "AVG(total_outbound_influence)"] | 5 | 4.214 |
| [S15/Q12](#s15) | success | ["jira__project_risk_assessment"] | 0 / {} | ["CASE WHEN complexity_risk_score <= 25 THEN 'low_complexity_(<=25)' WHEN complexity_risk_score <= 50 THEN 'medium_complexity_(26-50)' WHEN complexity_risk_score <= 75 THEN 'high_complexity_(51-75)' ELSE 'very_high_complexity_(>75)' END"] | ["COUNT(*)", "AVG(success_probability)", "AVG(overall_health_score)", "AVG(value_delivery_percentage)", "AVG(total_risk_score)", "AVG(team_stability_percentage)"] | 4 | 0.587 |
| [S16/Q13](#s16) | success | ["jira__stakeholder_engagement_insights"] | 0 / {} | ["stakeholder_archetype"] | ["COUNT(*)", "AVG(direct_network_connections)", "AVG(cross_functional_projects)", "AVG(total_engagement_score)", "AVG(engagement_quality_score)", "AVG(engagement_impact_score)"] | 10 | 3.629 |
| [S17/Q14](#s17) | success | ["jira__stakeholder_engagement_insights"] | 0 / {} | ["response_pattern_type"] | ["COUNT(*)", "AVG(direct_network_connections)", "AVG(total_engagement_score)", "AVG(engagement_quality_score)", "AVG(avg_outbound_influence_strength)"] | 4 | 3.315 |
| [S18/Q15](#s18) | success | ["jira__project_risk_assessment"] | 0 / {} | ["primary_risk_factor"] | ["COUNT(*)", "AVG(complexity_risk_score)", "AVG(success_probability)", "AVG(overall_health_score)"] | 6 | 0.503 |
| [S19/Q16](#s19) | success | ["jira__project_risk_assessment"] | 0 / {} | ["primary_risk_driver"] | ["COUNT(*)", "AVG(complexity_risk_score)", "AVG(success_probability)", "AVG(overall_health_score)"] | 8 | 0.517 |
| [S20/Q17](#s20) | success | ["jira__stakeholder_engagement_insights"] | 0 / {} | [] | [] | 4524 | 16.74 |
| [S21/Q18](#s21) | success | ["jira__project_risk_assessment"] | 0 / {} | [] | [] | 200 | 0.862 |
| [S22/Q19](#s22) | success | ["jira__stakeholder_engagement_insights"] | 0 / {} | ["CASE WHEN direct_network_connections <= 5 THEN 'low_(<=5)' WHEN direct_network_connections <= 20 THEN 'mid_(6-20)' ELSE 'high_(>20)' END", "engagement_risk_status"] | ["COUNT(*)", "AVG(total_engagement_score)"] | 7 | 3.858 |
| [S23/Q20](#s23) | success | ["jira__project_risk_assessment"] | 0 / {} | ["success_probability"] | ["COUNT(*)"] | 43 | 0.452 |
| [S24/Q21](#s24) | success | ["jira__project_risk_assessment"] | 0 / {} | ["trajectory_status"] | ["AVG(complexity_risk_score)", "AVG(success_probability)", "AVG(total_risk_score)", "AVG(health_risk_score)", "AVG(schedule_risk_score)", "AVG(resource_risk_score)", "AVG(scope_risk_score)"] | 4 | 0.571 |
| [S25/Q22](#s25) | success | ["jira__stakeholder_engagement_insights"] | 0 / {} | [] | ["SUM(total_projects_involved)", "SUM(cross_functional_projects)", "COUNT(*)", "COUNT(DISTINCT total_projects_involved)"] | 1 | 1.667 |
| [S26/Q23](#s26) | success | ["jira__stakeholder_engagement_insights"] | 0 / {} | [] | ["COUNT(*)", "SUM(CASE WHEN stakeholder_id LIKE '%PRO%' THEN 1 ELSE 0 END)", "SUM(CASE WHEN user_display_name LIKE '%PRO%' THEN 1 ELSE 0 END)", "SUM(CASE WHEN stakeholder_archetype LIKE '%PRO%' THEN 1 ELSE 0 END)", "SUM(CASE WHEN recommended_engagement_strategy LIKE '%PRO%' THEN 1 ELSE 0 END)", "SUM(CASE WHEN development_opportunity LIKE '%PRO%' THEN 1 ELSE 0 END)"] | 1 | 3.214 |
| [S27/Q24](#s27) | success | ["jira__project_risk_assessment"] | 0 / {} | [] | ["COUNT(DISTINCT project_key)", "COUNT(DISTINCT project_name)", "COUNT(DISTINCT project_id)"] | 1 | 0.608 |
| [S28/Q25](#s28) | success | ["jira__project_risk_assessment"] | 0 / {} | ["CASE WHEN team_stability_percentage < 60 THEN 'low_stability_(<60)' WHEN team_stability_percentage < 75 THEN 'medium_stability_(60-75)' ELSE 'high_stability_(>=75)' END"] | ["COUNT(*)", "AVG(complexity_risk_score)", "AVG(success_probability)", "AVG(team_stability_percentage)", "AVG(value_delivery_percentage)", "AVG(total_risk_score)"] | 3 | 0.574 |
| [S29/Q26](#s29) | success | ["jira__project_risk_assessment"] | 0 / {} | ["CASE WHEN sprint_adoption_rate < 0.5 THEN 'low_sprint_adoption' WHEN sprint_adoption_rate < 0.8 THEN 'medium_sprint_adoption' ELSE 'high_sprint_adoption' END"] | ["COUNT(*)", "AVG(complexity_risk_score)", "AVG(success_probability)", "AVG(sprint_adoption_rate)", "AVG(value_delivery_percentage)", "AVG(total_risk_score)"] | 3 | 0.582 |
| [S30/Q27](#s30) | success | ["jira__project_risk_assessment"] | 0 / {} | [] | [] | 200 | 1.305 |
| [S31/Q28](#s31) | success | ["jira__project_risk_assessment"] | 0 / {} | [] | [] | 200 | 1.06 |
| [S32/Q29](#s32) | success | ["jira__project_risk_assessment"] | 0 / {} | [] | [] | 200 | 1.109 |
| [S33/Q30](#s33) | success | ["jira__stakeholder_engagement_insights"] | 0 / {} | [] | [] | 4524 | 10.992 |


## 元数据和设置

| SQL | 类别 | 状态 | 内容 |
| --- | --- | --- | --- |
| S1 | connection_setup | success | PRAGMA query_only=ON |
| S2 | metadata | success | SELECT name,sql FROM sqlite_master WHERE type='table' ORDER BY name |
| S5 | metadata | success | SELECT type, name, sql FROM sqlite_master ORDER BY type, name |


## Python 与执行位置

人工源码审查：**reviewed_SQL_dominant_with_statistical_and_chart_exceptions**。Python 主要用于 Pearson 相关、层次聚类、模型标准化与图表。聚类后组别来自数值算法，其画像均值应与原始 SQL 维度聚合区别处理。仍有可在 SQL 完成的成功率阈值计数、高连接人数计数和分项风险求和，属于明确的执行位置例外，不能称完全遵守。 [证据](../reviews/dacomp-062.json)。

P1：SQLite lacks built-in correlation (CORR/Pearson) and MEDIAN functions. I need to compute Pearson correlations between direct_network_connections and stakeholder engagement/influence metrics, and between complexity_risk_score and success_probability with other project metrics. I'll also compute quantiles for distributions. I'm pulling only the numeric columns needed for these statistical computations.

[源码](../../../runs/dsv4flash-db-first-full-01/dacomp-062/attempt-01/python/P1.py)；[输出](../../../runs/dsv4flash-db-first-full-01/dacomp-062/attempt-01/python/P1.stdout)；[错误](../../../runs/dsv4flash-db-first-full-01/dacomp-062/attempt-01/python/P1.stderr)。检出需人工核验的 SQL 可实现操作：.query(；不能仅凭理由判为合规。

P2：Need to compute the full distribution of project success_probability values (detailed histogram), examine the relationship between all risk sub-scores, and check for any cluster structure in the project data that might relate to complexity_risk_score and success_probability. SQL alone cannot do clustering or produce the necessary visualization.

[源码](../../../runs/dsv4flash-db-first-full-01/dacomp-062/attempt-01/python/P2.py)；[输出](../../../runs/dsv4flash-db-first-full-01/dacomp-062/attempt-01/python/P2.stdout)；[错误](../../../runs/dsv4flash-db-first-full-01/dacomp-062/attempt-01/python/P2.stderr)。检出需人工核验的 SQL 可实现操作：.query(；不能仅凭理由判为合规。

P3：Need to compute hierarchical clustering (scipy linkage), detailed correlation matrices, and combined visualizations for the project risk profiles. SQLite does not support clustering, PCA, or correlation heatmaps. I'm pulling only the numeric columns needed for this analysis.

[源码](../../../runs/dsv4flash-db-first-full-01/dacomp-062/attempt-01/python/P3.py)；[输出](../../../runs/dsv4flash-db-first-full-01/dacomp-062/attempt-01/python/P3.stdout)；[错误](../../../runs/dsv4flash-db-first-full-01/dacomp-062/attempt-01/python/P3.stderr)。检出需人工核验的 SQL 可实现操作：.query(；不能仅凭理由判为合规。

P4：Fixing the matplotlib boxplot API issue and producing the final visualization and statistics. Need scipy for hierarchical clustering (not supported in SQLite) and Pearson correlations (not available in SQLite).

[源码](../../../runs/dsv4flash-db-first-full-01/dacomp-062/attempt-01/python/P4.py)；[输出](../../../runs/dsv4flash-db-first-full-01/dacomp-062/attempt-01/python/P4.stdout)；[错误](../../../runs/dsv4flash-db-first-full-01/dacomp-062/attempt-01/python/P4.stderr)。检出需人工核验的 SQL 可实现操作：.query(；不能仅凭理由判为合规。

P5：Check where the plots were saved to reference them correctly.

[源码](../../../runs/dsv4flash-db-first-full-01/dacomp-062/attempt-01/python/P5.py)；[输出](../../../runs/dsv4flash-db-first-full-01/dacomp-062/attempt-01/python/P5.stdout)；[错误](../../../runs/dsv4flash-db-first-full-01/dacomp-062/attempt-01/python/P5.stderr)。自动源码筛查未检出预设迁出信号；这不是全面语义合规证明。

## 优化机会

已验证候选。筛选限于精确 SQL、相同自包含 CTE、相同单表完整过滤、可分解单表聚合；未覆盖任意 Join 等价和一般谓词蕴含。全部候选都是 offline，未测在线预测。

| 候选 | 类型 | 已有结果 | 覆盖 SQL | 后续次数 | 中间行数 | 验证 | 成本 |
| --- | --- | --- | --- | --- | --- | --- | --- |
| C1 | exact-result reuse | True | ["S30", "S31", "S32"] | 2 | 200 | verified | Not benchmarked; correctness alone does not establish net speedup. |
| C2 | aggregate MV | False | ["S6", "S12", "S13", "S15", "S18", "S19", "S23", "S24", "S28", "S29"] | 9 | 200 | rejected_result_mismatch | Not benchmarked; correctness alone does not establish net speedup. |
| C3 | aggregate MV | False | ["S7", "S10", "S11", "S14", "S16", "S17", "S22", "S26"] | 7 | 1555 | verified | Not benchmarked; correctness alone does not establish net speedup. |


已验证覆盖（含触发查询、候选并集去重）：11/28 条成功数据 SQL。正确性仅针对当前数据库快照；未测性能的候选不能声称已加速。

[完整 build/rewrite 与比较证据](dacomp-062.analysis.json)。

### C3：aggregate MV

Union of grouping keys; decomposable aggregate states; AVG uses SUM and non-NULL COUNT.

原查询 [S7](#s7), [S10](#s10), [S11](#s11), [S14](#s14), [S16](#s16), [S17](#s17), [S22](#s22), [S26](#s26) → 新增共享状态 C3 → 后续 7 次可复用。该构建点为事后假设，不代表 Agent 当时预知后续。

构建定义：

```sql
SELECT total_projects_involved AS __g0, influence_level AS __g1, CASE WHEN direct_network_connections <= 5 THEN '1_low_(<=5)' WHEN direct_network_connections <= 10 THEN '2_mid_low_(6-10)' WHEN direct_network_connections <= 20 THEN '3_mid_(11-20)' WHEN direct_network_connections <= 35 THEN '4_high_(21-35)' ELSE '5_very_high_(>35)' END AS __g2, stakeholder_archetype AS __g3, response_pattern_type AS __g4, CASE WHEN direct_network_connections <= 5 THEN 'low_(<=5)' WHEN direct_network_connections <= 20 THEN 'mid_(6-20)' ELSE 'high_(>20)' END AS __g5, engagement_risk_status AS __g6, COUNT(*) AS __a0, SUM(direct_network_connections) AS __a1_sum, COUNT(direct_network_connections) AS __a1_n, MIN(direct_network_connections) AS __a2, MAX(direct_network_connections) AS __a3, SUM(cross_functional_projects) AS __a4_sum, COUNT(cross_functional_projects) AS __a4_n, SUM(total_engagement_score) AS __a5_sum, COUNT(total_engagement_score) AS __a5_n, SUM(total_projects_involved) AS __a6_sum, COUNT(total_projects_involved) AS __a6_n, SUM(total_inbound_influence) AS __a7_sum, COUNT(total_inbound_influence) AS __a7_n, SUM(total_outbound_influence) AS __a8_sum, COUNT(total_outbound_influence) AS __a8_n, SUM(engagement_quality_score) AS __a9_sum, COUNT(engagement_quality_score) AS __a9_n, SUM(engagement_impact_score) AS __a10_sum, COUNT(engagement_impact_score) AS __a10_n, SUM(avg_outbound_influence_strength) AS __a11_sum, COUNT(avg_outbound_influence_strength) AS __a11_n, SUM(CASE WHEN stakeholder_id LIKE '%PRO%' THEN 1 ELSE 0 END) AS __a12, SUM(CASE WHEN user_display_name LIKE '%PRO%' THEN 1 ELSE 0 END) AS __a13, SUM(CASE WHEN stakeholder_archetype LIKE '%PRO%' THEN 1 ELSE 0 END) AS __a14, SUM(CASE WHEN recommended_engagement_strategy LIKE '%PRO%' THEN 1 ELSE 0 END) AS __a15, SUM(CASE WHEN development_opportunity LIKE '%PRO%' THEN 1 ELSE 0 END) AS __a16 FROM "jira__stakeholder_engagement_insights"  GROUP BY total_projects_involved, influence_level, CASE WHEN direct_network_connections <= 5 THEN '1_low_(<=5)' WHEN direct_network_connections <= 10 THEN '2_mid_low_(6-10)' WHEN direct_network_connections <= 20 THEN '3_mid_(11-20)' WHEN direct_network_connections <= 35 THEN '4_high_(21-35)' ELSE '5_very_high_(>35)' END, stakeholder_archetype, response_pattern_type, CASE WHEN direct_network_connections <= 5 THEN 'low_(<=5)' WHEN direct_network_connections <= 20 THEN 'mid_(6-20)' ELSE 'high_(>20)' END, engagement_risk_status
```

受益查询 S7 的改写示例：

```sql
SELECT SUM(__a0) AS n_stakeholders FROM temp.reuse_candidate
```

| 原 SQL | 列名一致 | 结果一致 | 比较方法 |
| --- | --- | --- | --- |
| S7 | True | True | exact_multiset |
| S10 | True | True | ordered_numeric_tolerance |
| S11 | True | True | ordered_numeric_tolerance |
| S14 | True | True | ordered_numeric_tolerance |
| S16 | True | True | ordered_numeric_tolerance |
| S17 | True | True | ordered_numeric_tolerance |
| S22 | True | True | ordered_numeric_tolerance |
| S26 | True | True | exact_multiset |


验证状态：verified；成本结论：Not benchmarked; correctness alone does not establish net speedup.

### C1：exact-result reuse

Identical normalized SQL and parameters; archive equality checked.

原查询 [S30](#s30), [S31](#s31), [S32](#s32) → 保留前序结果 S30 → 后续 2 次可复用。该构建点为事后假设，不代表 Agent 当时预知后续。

| 原 SQL | 列名一致 | 结果一致 | 比较方法 |
| --- | --- | --- | --- |
| S31 | True | True | exact_multiset |
| S32 | True | True | exact_multiset |


验证状态：verified；成本结论：Not benchmarked; correctness alone does not establish net speedup.

### C2：aggregate MV

Union of grouping keys; decomposable aggregate states; AVG uses SUM and non-NULL COUNT.

原查询 [S6](#s6), [S12](#s12), [S13](#s13), [S15](#s15), [S18](#s18), [S19](#s19), [S23](#s23), [S24](#s24), [S28](#s28), [S29](#s29) → 新增共享状态 C2 → 后续 9 次可复用。该构建点为事后假设，不代表 Agent 当时预知后续。

构建定义：

```sql
SELECT risk_category AS __g0, trajectory_status AS __g1, CASE WHEN complexity_risk_score <= 25 THEN 'low_complexity_(<=25)' WHEN complexity_risk_score <= 50 THEN 'medium_complexity_(26-50)' WHEN complexity_risk_score <= 75 THEN 'high_complexity_(51-75)' ELSE 'very_high_complexity_(>75)' END AS __g2, primary_risk_factor AS __g3, primary_risk_driver AS __g4, success_probability AS __g5, CASE WHEN team_stability_percentage < 60 THEN 'low_stability_(<60)' WHEN team_stability_percentage < 75 THEN 'medium_stability_(60-75)' ELSE 'high_stability_(>=75)' END AS __g6, CASE WHEN sprint_adoption_rate < 0.5 THEN 'low_sprint_adoption' WHEN sprint_adoption_rate < 0.8 THEN 'medium_sprint_adoption' ELSE 'high_sprint_adoption' END AS __g7, COUNT(*) AS __a0, SUM(complexity_risk_score) AS __a1_sum, COUNT(complexity_risk_score) AS __a1_n, SUM(success_probability) AS __a2_sum, COUNT(success_probability) AS __a2_n, SUM(total_risk_score) AS __a3_sum, COUNT(total_risk_score) AS __a3_n, SUM(overall_health_score) AS __a4_sum, COUNT(overall_health_score) AS __a4_n, SUM(delivered_value_points) AS __a5_sum, COUNT(delivered_value_points) AS __a5_n, SUM(value_delivery_percentage) AS __a6_sum, COUNT(value_delivery_percentage) AS __a6_n, SUM(team_stability_percentage) AS __a7_sum, COUNT(team_stability_percentage) AS __a7_n, SUM(health_risk_score) AS __a8_sum, COUNT(health_risk_score) AS __a8_n, SUM(schedule_risk_score) AS __a9_sum, COUNT(schedule_risk_score) AS __a9_n, SUM(resource_risk_score) AS __a10_sum, COUNT(resource_risk_score) AS __a10_n, SUM(scope_risk_score) AS __a11_sum, COUNT(scope_risk_score) AS __a11_n, SUM(sprint_adoption_rate) AS __a12_sum, COUNT(sprint_adoption_rate) AS __a12_n FROM "jira__project_risk_assessment"  GROUP BY risk_category, trajectory_status, CASE WHEN complexity_risk_score <= 25 THEN 'low_complexity_(<=25)' WHEN complexity_risk_score <= 50 THEN 'medium_complexity_(26-50)' WHEN complexity_risk_score <= 75 THEN 'high_complexity_(51-75)' ELSE 'very_high_complexity_(>75)' END, primary_risk_factor, primary_risk_driver, success_probability, CASE WHEN team_stability_percentage < 60 THEN 'low_stability_(<60)' WHEN team_stability_percentage < 75 THEN 'medium_stability_(60-75)' ELSE 'high_stability_(>=75)' END, CASE WHEN sprint_adoption_rate < 0.5 THEN 'low_sprint_adoption' WHEN sprint_adoption_rate < 0.8 THEN 'medium_sprint_adoption' ELSE 'high_sprint_adoption' END
```

受益查询 S6 的改写示例：

```sql
SELECT SUM(__a0) AS n_projects FROM temp.reuse_candidate
```

| 原 SQL | 列名一致 | 结果一致 | 比较方法 |
| --- | --- | --- | --- |
| S6 | True | True | exact_multiset |
| S12 | True | True | ordered_numeric_tolerance |
| S13 | True | True | ordered_numeric_tolerance |
| S15 | True | True | ordered_numeric_tolerance |
| S18 | True | True | ordered_numeric_tolerance |
| S19 | True | True | ordered_numeric_tolerance |
| S23 | True | True | ordered_numeric_tolerance |
| S24 | True | True | ordered_numeric_tolerance |
| S28 | True | False | ordered_numeric_tolerance |
| S29 | True | True | ordered_numeric_tolerance |


验证状态：rejected_result_mismatch；成本结论：Not benchmarked; correctness alone does not establish net speedup.

结果依赖：自动记录 SQL→Python 的接口父调用，以及源码中引用归档文件的消费者；字面值相同不认定因果。模型方向选择需要人工读取消息，尚未做全面因果标注。

[原始报告](../../../runs/dsv4flash-db-first-full-01/dacomp-062/attempt-01/answer.md)；[统一消息](../../../runs/dsv4flash-db-first-full-01/dacomp-062/attempt-01/messages.jsonl)；[原始 OpenCode 事件](../../../runs/dsv4flash-db-first-full-01/dacomp-062/attempt-01/opencode.jsonl)；[SQL 引擎日志](../../../runs/dsv4flash-db-first-full-01/dacomp-062/attempt-01/sql_journal.jsonl)。

[可读报告（本地图片链接规范化）](../answers/dacomp-062.md)。原始回答保留，分析结论未改写。

## S1

类别 `connection_setup`；来源 `connection`；调用 `b200c125c1fb467cab88bf7182cef409`；状态 `success`。

```sql
PRAGMA query_only=ON
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-062/attempt-01/sql/S1.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-062/attempt-01/sql/S1.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-062/attempt-01/results/S1.rows.jsonl)；完整：True；SHA256：`e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`。

## S2

类别 `metadata`；来源 `list_db`；调用 `b200c125c1fb467cab88bf7182cef409`；状态 `success`。

```sql
SELECT name,sql FROM sqlite_master WHERE type='table' ORDER BY name
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-062/attempt-01/sql/S2.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-062/attempt-01/sql/S2.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-062/attempt-01/results/S2.rows.jsonl)；完整：True；SHA256：`c150d692f75ec71f470a8e7cfed7d41d20698c216917cd0ce1258b275fff9b56`。

## S3

类别 `data`；来源 `query_db`；调用 `feef2d3831c7465fa5f3e8183754c4c1`；状态 `success`。

```sql
SELECT * FROM jira__project_risk_assessment LIMIT 5
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-062/attempt-01/sql/S3.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-062/attempt-01/sql/S3.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-062/attempt-01/results/S3.rows.jsonl)；完整：True；SHA256：`8689a83b6e276591023f07da57377d28fe91c9c4892bd4f8b9e679ee358b0dcf`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "jira__project_risk_assessment", "kind": "base", "block": null, "base_tables": ["jira__project_risk_assessment"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |


## S4

类别 `data`；来源 `query_db`；调用 `81bcf1697e7c4b4ba634a499e1badad3`；状态 `success`。

```sql
SELECT * FROM jira__stakeholder_engagement_insights LIMIT 5
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-062/attempt-01/sql/S4.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-062/attempt-01/sql/S4.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-062/attempt-01/results/S4.rows.jsonl)；完整：True；SHA256：`6cc8ddf288790903c2100b5cc97c49bd662a031fcb697613146091ec111783cc`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "jira__stakeholder_engagement_insights", "kind": "base", "block": null, "base_tables": ["jira__stakeholder_engagement_insights"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |


## S5

类别 `metadata`；来源 `query_db`；调用 `5043fcbc07e9450f90287af17891904a`；状态 `success`。

```sql
SELECT type, name, sql FROM sqlite_master ORDER BY type, name
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-062/attempt-01/sql/S5.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-062/attempt-01/sql/S5.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-062/attempt-01/results/S5.rows.jsonl)；完整：True；SHA256：`d7bd787ba6bf76bd09a44ad3ac9e1bbaf0194f542faa1b14c55b6c446b2421bf`。

## S6

类别 `data`；来源 `query_db`；调用 `44356485036c43fd83e2205743c4bbae`；状态 `success`。

```sql
SELECT COUNT(*) AS n_projects FROM jira__project_risk_assessment
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-062/attempt-01/sql/S6.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-062/attempt-01/sql/S6.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-062/attempt-01/results/S6.rows.jsonl)；完整：True；SHA256：`8fe64ac838eb7a89546cb6a98f203e335a9c087776008d203b43095ded53e1b7`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "jira__project_risk_assessment", "kind": "base", "block": null, "base_tables": ["jira__project_risk_assessment"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |


## S7

类别 `data`；来源 `query_db`；调用 `4a2d23764a414d2eb8660caf4955b487`；状态 `success`。

```sql
SELECT COUNT(*) AS n_stakeholders FROM jira__stakeholder_engagement_insights
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-062/attempt-01/sql/S7.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-062/attempt-01/sql/S7.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-062/attempt-01/results/S7.rows.jsonl)；完整：True；SHA256：`d627005cafeb3332957ae72cf9a51f690d805fcb8a5a8212d1ab1e775ae32288`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "jira__stakeholder_engagement_insights", "kind": "base", "block": null, "base_tables": ["jira__stakeholder_engagement_insights"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |


## S8

类别 `data`；来源 `query_db`；调用 `ba4b07c505264cab8f5811ae9c8f2413`；状态 `failed`。

```sql
SELECT 
  MIN(direct_network_connections) AS min_conn,
  AVG(direct_network_connections) AS avg_conn,
  MAX(direct_network_connections) AS max_conn,
  MEDIAN(direct_network_connections) AS median_conn,
  STDEV(direct_network_connections) AS std_conn
FROM jira__stakeholder_engagement_insights
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-062/attempt-01/sql/S8.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-062/attempt-01/sql/S8.parameters.json)。

错误：`OperationalError('no such function: MEDIAN')`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "jira__stakeholder_engagement_insights", "kind": "base", "block": null, "base_tables": ["jira__stakeholder_engagement_insights"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | MIN(direct_network_connections) | [{"table": "jira__stakeholder_engagement_insights", "column": "direct_network_connections"}] | [] | False |
| B1 | AVG(direct_network_connections) | [{"table": "jira__stakeholder_engagement_insights", "column": "direct_network_connections"}] | [] | False |
| B1 | MAX(direct_network_connections) | [{"table": "jira__stakeholder_engagement_insights", "column": "direct_network_connections"}] | [] | False |
| B1 | PERCENTILE_CONT(direct_network_connections, 0.5) | [{"table": "jira__stakeholder_engagement_insights", "column": "direct_network_connections"}] | [] | False |
| B1 | STDDEV(direct_network_connections) | [{"table": "jira__stakeholder_engagement_insights", "column": "direct_network_connections"}] | [] | False |


## S9

类别 `data`；来源 `query_db`；调用 `4b2ce2be73104b39969771bbfe49dc46`；状态 `failed`。

```sql
SELECT 
  MIN(complexity_risk_score) AS min_crs,
  AVG(complexity_risk_score) AS avg_crs,
  MAX(complexity_risk_score) AS max_crs,
  MEDIAN(complexity_risk_score) AS median_crs,
  STDEV(complexity_risk_score) AS std_crs,
  MIN(success_probability) AS min_sp,
  AVG(success_probability) AS avg_sp,
  MAX(success_probability) AS max_sp,
  MEDIAN(success_probability) AS median_sp,
  STDEV(success_probability) AS std_sp
FROM jira__project_risk_assessment
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-062/attempt-01/sql/S9.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-062/attempt-01/sql/S9.parameters.json)。

错误：`OperationalError('no such function: MEDIAN')`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "jira__project_risk_assessment", "kind": "base", "block": null, "base_tables": ["jira__project_risk_assessment"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | MIN(complexity_risk_score) | [{"table": "jira__project_risk_assessment", "column": "complexity_risk_score"}] | [] | False |
| B1 | AVG(complexity_risk_score) | [{"table": "jira__project_risk_assessment", "column": "complexity_risk_score"}] | [] | False |
| B1 | MAX(complexity_risk_score) | [{"table": "jira__project_risk_assessment", "column": "complexity_risk_score"}] | [] | False |
| B1 | PERCENTILE_CONT(complexity_risk_score, 0.5) | [{"table": "jira__project_risk_assessment", "column": "complexity_risk_score"}] | [] | False |
| B1 | STDDEV(complexity_risk_score) | [{"table": "jira__project_risk_assessment", "column": "complexity_risk_score"}] | [] | False |
| B1 | MIN(success_probability) | [{"table": "jira__project_risk_assessment", "column": "success_probability"}] | [] | False |
| B1 | AVG(success_probability) | [{"table": "jira__project_risk_assessment", "column": "success_probability"}] | [] | False |
| B1 | MAX(success_probability) | [{"table": "jira__project_risk_assessment", "column": "success_probability"}] | [] | False |
| B1 | PERCENTILE_CONT(success_probability, 0.5) | [{"table": "jira__project_risk_assessment", "column": "success_probability"}] | [] | False |
| B1 | STDDEV(success_probability) | [{"table": "jira__project_risk_assessment", "column": "success_probability"}] | [] | False |


## S10

类别 `data`；来源 `query_db`；调用 `d82e104b620b43929c6a26e0d8983b15`；状态 `success`。

```sql
SELECT 
  total_projects_involved,
  AVG(direct_network_connections) AS avg_connections,
  COUNT(*) AS n_stakeholders
FROM jira__stakeholder_engagement_insights
GROUP BY total_projects_involved
ORDER BY total_projects_involved
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-062/attempt-01/sql/S10.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-062/attempt-01/sql/S10.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-062/attempt-01/results/S10.rows.jsonl)；完整：True；SHA256：`44b4e923435c3c2730177f1c61057c4986614fccb7c5a11f781327a9aaf110cf`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "jira__stakeholder_engagement_insights", "kind": "base", "block": null, "base_tables": ["jira__stakeholder_engagement_insights"]}] | [] | ["total_projects_involved"] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | AVG(direct_network_connections) | [{"table": "jira__stakeholder_engagement_insights", "column": "direct_network_connections"}] | [] | False |
| B1 | COUNT(*) | [] | [] | True |


## S11

类别 `data`；来源 `query_db`；调用 `bcbdb0ddb2214c1a9b6db6ccc311cd7b`；状态 `success`。

```sql
SELECT 
  influence_level,
  COUNT(*) AS n,
  AVG(direct_network_connections) AS avg_conn,
  MIN(direct_network_connections) AS min_conn,
  MAX(direct_network_connections) AS max_conn,
  AVG(cross_functional_projects) AS avg_cross_func,
  AVG(total_engagement_score) AS avg_engagement
FROM jira__stakeholder_engagement_insights
GROUP BY influence_level
ORDER BY avg_conn DESC
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-062/attempt-01/sql/S11.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-062/attempt-01/sql/S11.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-062/attempt-01/results/S11.rows.jsonl)；完整：True；SHA256：`0e4fa143e2f0c0b06ef0580127e84f93964080367220a62ff7f0255ad265602c`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "jira__stakeholder_engagement_insights", "kind": "base", "block": null, "base_tables": ["jira__stakeholder_engagement_insights"]}] | [] | ["influence_level"] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |
| B1 | AVG(direct_network_connections) | [{"table": "jira__stakeholder_engagement_insights", "column": "direct_network_connections"}] | [] | False |
| B1 | MIN(direct_network_connections) | [{"table": "jira__stakeholder_engagement_insights", "column": "direct_network_connections"}] | [] | False |
| B1 | MAX(direct_network_connections) | [{"table": "jira__stakeholder_engagement_insights", "column": "direct_network_connections"}] | [] | False |
| B1 | AVG(cross_functional_projects) | [{"table": "jira__stakeholder_engagement_insights", "column": "cross_functional_projects"}] | [] | False |
| B1 | AVG(total_engagement_score) | [{"table": "jira__stakeholder_engagement_insights", "column": "total_engagement_score"}] | [] | False |


## S12

类别 `data`；来源 `query_db`；调用 `0c68e4b1518b4d9bbc14908ef7ed90ed`；状态 `success`。

```sql
SELECT 
  risk_category,
  COUNT(*) AS n,
  AVG(complexity_risk_score) AS avg_complexity,
  AVG(success_probability) AS avg_success,
  AVG(total_risk_score) AS avg_total_risk,
  AVG(overall_health_score) AS avg_health
FROM jira__project_risk_assessment
GROUP BY risk_category
ORDER BY avg_success ASC
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-062/attempt-01/sql/S12.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-062/attempt-01/sql/S12.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-062/attempt-01/results/S12.rows.jsonl)；完整：True；SHA256：`617fd7aacf05e148341a6ba317018ad6083a9121dcab52986f30a4e361eb1156`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "jira__project_risk_assessment", "kind": "base", "block": null, "base_tables": ["jira__project_risk_assessment"]}] | [] | ["risk_category"] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |
| B1 | AVG(complexity_risk_score) | [{"table": "jira__project_risk_assessment", "column": "complexity_risk_score"}] | [] | False |
| B1 | AVG(success_probability) | [{"table": "jira__project_risk_assessment", "column": "success_probability"}] | [] | False |
| B1 | AVG(total_risk_score) | [{"table": "jira__project_risk_assessment", "column": "total_risk_score"}] | [] | False |
| B1 | AVG(overall_health_score) | [{"table": "jira__project_risk_assessment", "column": "overall_health_score"}] | [] | False |


## S13

类别 `data`；来源 `query_db`；调用 `0b304649f0834d398dc4c6288ff6772c`；状态 `success`。

```sql
SELECT 
  trajectory_status,
  COUNT(*) AS n,
  AVG(complexity_risk_score) AS avg_complexity,
  AVG(success_probability) AS avg_success,
  AVG(delivered_value_points) AS avg_delivered,
  AVG(value_delivery_percentage) AS avg_vdp
FROM jira__project_risk_assessment
GROUP BY trajectory_status
ORDER BY avg_success ASC
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-062/attempt-01/sql/S13.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-062/attempt-01/sql/S13.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-062/attempt-01/results/S13.rows.jsonl)；完整：True；SHA256：`9b638af86824808df25360e2338b2dfb70ae0c303a4aeb518d4ecedece090f6e`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "jira__project_risk_assessment", "kind": "base", "block": null, "base_tables": ["jira__project_risk_assessment"]}] | [] | ["trajectory_status"] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |
| B1 | AVG(complexity_risk_score) | [{"table": "jira__project_risk_assessment", "column": "complexity_risk_score"}] | [] | False |
| B1 | AVG(success_probability) | [{"table": "jira__project_risk_assessment", "column": "success_probability"}] | [] | False |
| B1 | AVG(delivered_value_points) | [{"table": "jira__project_risk_assessment", "column": "delivered_value_points"}] | [] | False |
| B1 | AVG(value_delivery_percentage) | [{"table": "jira__project_risk_assessment", "column": "value_delivery_percentage"}] | [] | False |


## S14

类别 `data`；来源 `query_db`；调用 `7a4b51483a48419ebe499e0499176add`；状态 `success`。

```sql
SELECT 
  CASE 
    WHEN direct_network_connections <= 5 THEN '1_low_(<=5)'
    WHEN direct_network_connections <= 10 THEN '2_mid_low_(6-10)'
    WHEN direct_network_connections <= 20 THEN '3_mid_(11-20)'
    WHEN direct_network_connections <= 35 THEN '4_high_(21-35)'
    ELSE '5_very_high_(>35)'
  END AS conn_bucket,
  COUNT(*) AS n,
  ROUND(AVG(total_projects_involved),2) AS avg_projects,
  ROUND(AVG(cross_functional_projects),2) AS avg_cross_func,
  ROUND(AVG(total_engagement_score),2) AS avg_engagement,
  ROUND(AVG(total_inbound_influence),2) AS avg_inbound,
  ROUND(AVG(total_outbound_influence),2) AS avg_outbound
FROM jira__stakeholder_engagement_insights
GROUP BY conn_bucket
ORDER BY conn_bucket
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-062/attempt-01/sql/S14.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-062/attempt-01/sql/S14.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-062/attempt-01/results/S14.rows.jsonl)；完整：True；SHA256：`9d94705f4c9e1ad4824e616d076188669fe319ee52eff59fbd47c1916332329a`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "jira__stakeholder_engagement_insights", "kind": "base", "block": null, "base_tables": ["jira__stakeholder_engagement_insights"]}] | [] | ["CASE WHEN direct_network_connections <= 5 THEN '1_low_(<=5)' WHEN direct_network_connections <= 10 THEN '2_mid_low_(6-10)' WHEN direct_network_connections <= 20 THEN '3_mid_(11-20)' WHEN direct_network_connections <= 35 THEN '4_high_(21-35)' ELSE '5_very_high_(>35)' END"] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |
| B1 | AVG(total_projects_involved) | [{"table": "jira__stakeholder_engagement_insights", "column": "total_projects_involved"}] | [] | False |
| B1 | AVG(cross_functional_projects) | [{"table": "jira__stakeholder_engagement_insights", "column": "cross_functional_projects"}] | [] | False |
| B1 | AVG(total_engagement_score) | [{"table": "jira__stakeholder_engagement_insights", "column": "total_engagement_score"}] | [] | False |
| B1 | AVG(total_inbound_influence) | [{"table": "jira__stakeholder_engagement_insights", "column": "total_inbound_influence"}] | [] | False |
| B1 | AVG(total_outbound_influence) | [{"table": "jira__stakeholder_engagement_insights", "column": "total_outbound_influence"}] | [] | False |


## S15

类别 `data`；来源 `query_db`；调用 `529d809381dd472b925320737adda31a`；状态 `success`。

```sql
SELECT 
  CASE 
    WHEN complexity_risk_score <= 25 THEN 'low_complexity_(<=25)'
    WHEN complexity_risk_score <= 50 THEN 'medium_complexity_(26-50)'
    WHEN complexity_risk_score <= 75 THEN 'high_complexity_(51-75)'
    ELSE 'very_high_complexity_(>75)'
  END AS comp_bucket,
  COUNT(*) AS n,
  ROUND(AVG(success_probability),3) AS avg_success,
  ROUND(AVG(overall_health_score),2) AS avg_health,
  ROUND(AVG(value_delivery_percentage),2) AS avg_vdp,
  ROUND(AVG(total_risk_score),2) AS avg_total_risk,
  ROUND(AVG(team_stability_percentage),2) AS avg_team_stability
FROM jira__project_risk_assessment
GROUP BY comp_bucket
ORDER BY comp_bucket
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-062/attempt-01/sql/S15.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-062/attempt-01/sql/S15.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-062/attempt-01/results/S15.rows.jsonl)；完整：True；SHA256：`b6320c41763e1207a9ed6eb1dd185aefb6851b79edf3c5bd4ab35540442c1146`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "jira__project_risk_assessment", "kind": "base", "block": null, "base_tables": ["jira__project_risk_assessment"]}] | [] | ["CASE WHEN complexity_risk_score <= 25 THEN 'low_complexity_(<=25)' WHEN complexity_risk_score <= 50 THEN 'medium_complexity_(26-50)' WHEN complexity_risk_score <= 75 THEN 'high_complexity_(51-75)' ELSE 'very_high_complexity_(>75)' END"] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |
| B1 | AVG(success_probability) | [{"table": "jira__project_risk_assessment", "column": "success_probability"}] | [] | False |
| B1 | AVG(overall_health_score) | [{"table": "jira__project_risk_assessment", "column": "overall_health_score"}] | [] | False |
| B1 | AVG(value_delivery_percentage) | [{"table": "jira__project_risk_assessment", "column": "value_delivery_percentage"}] | [] | False |
| B1 | AVG(total_risk_score) | [{"table": "jira__project_risk_assessment", "column": "total_risk_score"}] | [] | False |
| B1 | AVG(team_stability_percentage) | [{"table": "jira__project_risk_assessment", "column": "team_stability_percentage"}] | [] | False |


## S16

类别 `data`；来源 `query_db`；调用 `7c20f4ec7d2d476eb15773add23bac07`；状态 `success`。

```sql
SELECT 
  stakeholder_archetype,
  COUNT(*) AS n,
  ROUND(AVG(direct_network_connections),2) AS avg_conn,
  ROUND(AVG(cross_functional_projects),2) AS avg_cross_func,
  ROUND(AVG(total_engagement_score),2) AS avg_engagement,
  ROUND(AVG(engagement_quality_score),2) AS avg_quality,
  ROUND(AVG(engagement_impact_score),2) AS avg_impact
FROM jira__stakeholder_engagement_insights
GROUP BY stakeholder_archetype
ORDER BY avg_conn DESC
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-062/attempt-01/sql/S16.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-062/attempt-01/sql/S16.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-062/attempt-01/results/S16.rows.jsonl)；完整：True；SHA256：`8872aa905a96f2c7b3606f5988fe28c72a166269811ef85f2d68368451bb8257`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "jira__stakeholder_engagement_insights", "kind": "base", "block": null, "base_tables": ["jira__stakeholder_engagement_insights"]}] | [] | ["stakeholder_archetype"] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |
| B1 | AVG(direct_network_connections) | [{"table": "jira__stakeholder_engagement_insights", "column": "direct_network_connections"}] | [] | False |
| B1 | AVG(cross_functional_projects) | [{"table": "jira__stakeholder_engagement_insights", "column": "cross_functional_projects"}] | [] | False |
| B1 | AVG(total_engagement_score) | [{"table": "jira__stakeholder_engagement_insights", "column": "total_engagement_score"}] | [] | False |
| B1 | AVG(engagement_quality_score) | [{"table": "jira__stakeholder_engagement_insights", "column": "engagement_quality_score"}] | [] | False |
| B1 | AVG(engagement_impact_score) | [{"table": "jira__stakeholder_engagement_insights", "column": "engagement_impact_score"}] | [] | False |


## S17

类别 `data`；来源 `query_db`；调用 `87b3b8b7ea2d4f2fb607e26fc3971344`；状态 `success`。

```sql
SELECT 
  response_pattern_type,
  COUNT(*) AS n,
  ROUND(AVG(direct_network_connections),2) AS avg_conn,
  ROUND(AVG(total_engagement_score),2) AS avg_engagement,
  ROUND(AVG(engagement_quality_score),2) AS avg_quality,
  ROUND(AVG(avg_outbound_influence_strength),3) AS avg_influence_strength
FROM jira__stakeholder_engagement_insights
GROUP BY response_pattern_type
ORDER BY avg_conn DESC
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-062/attempt-01/sql/S17.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-062/attempt-01/sql/S17.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-062/attempt-01/results/S17.rows.jsonl)；完整：True；SHA256：`238580b58180d8cb67ed9aca9e0758e20c0f5750eb2ae468868ec298dfb26868`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "jira__stakeholder_engagement_insights", "kind": "base", "block": null, "base_tables": ["jira__stakeholder_engagement_insights"]}] | [] | ["response_pattern_type"] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |
| B1 | AVG(direct_network_connections) | [{"table": "jira__stakeholder_engagement_insights", "column": "direct_network_connections"}] | [] | False |
| B1 | AVG(total_engagement_score) | [{"table": "jira__stakeholder_engagement_insights", "column": "total_engagement_score"}] | [] | False |
| B1 | AVG(engagement_quality_score) | [{"table": "jira__stakeholder_engagement_insights", "column": "engagement_quality_score"}] | [] | False |
| B1 | AVG(avg_outbound_influence_strength) | [{"table": "jira__stakeholder_engagement_insights", "column": "avg_outbound_influence_strength"}] | [] | False |


## S18

类别 `data`；来源 `query_db`；调用 `129ed6f802e44d959f3f1d80421e4976`；状态 `success`。

```sql
SELECT 
  primary_risk_factor,
  COUNT(*) AS n,
  ROUND(AVG(complexity_risk_score),2) AS avg_complexity,
  ROUND(AVG(success_probability),3) AS avg_success,
  ROUND(AVG(overall_health_score),2) AS avg_health
FROM jira__project_risk_assessment
GROUP BY primary_risk_factor
ORDER BY avg_success ASC
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-062/attempt-01/sql/S18.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-062/attempt-01/sql/S18.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-062/attempt-01/results/S18.rows.jsonl)；完整：True；SHA256：`fb9ef2690aec352d14c833f921d5ff5a3ca9973e3d94ac041363eceb205153a0`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "jira__project_risk_assessment", "kind": "base", "block": null, "base_tables": ["jira__project_risk_assessment"]}] | [] | ["primary_risk_factor"] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |
| B1 | AVG(complexity_risk_score) | [{"table": "jira__project_risk_assessment", "column": "complexity_risk_score"}] | [] | False |
| B1 | AVG(success_probability) | [{"table": "jira__project_risk_assessment", "column": "success_probability"}] | [] | False |
| B1 | AVG(overall_health_score) | [{"table": "jira__project_risk_assessment", "column": "overall_health_score"}] | [] | False |


## S19

类别 `data`；来源 `query_db`；调用 `cdd45dda6ce949868198ff480d54550f`；状态 `success`。

```sql
SELECT 
  primary_risk_driver,
  COUNT(*) AS n,
  ROUND(AVG(complexity_risk_score),2) AS avg_complexity,
  ROUND(AVG(success_probability),3) AS avg_success,
  ROUND(AVG(overall_health_score),2) AS avg_health
FROM jira__project_risk_assessment
GROUP BY primary_risk_driver
ORDER BY avg_success ASC
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-062/attempt-01/sql/S19.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-062/attempt-01/sql/S19.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-062/attempt-01/results/S19.rows.jsonl)；完整：True；SHA256：`26e89f967b723e614c5f39e568f264d99c2d2eec4e1fbf50d13c1a3e3ad501d0`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "jira__project_risk_assessment", "kind": "base", "block": null, "base_tables": ["jira__project_risk_assessment"]}] | [] | ["primary_risk_driver"] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |
| B1 | AVG(complexity_risk_score) | [{"table": "jira__project_risk_assessment", "column": "complexity_risk_score"}] | [] | False |
| B1 | AVG(success_probability) | [{"table": "jira__project_risk_assessment", "column": "success_probability"}] | [] | False |
| B1 | AVG(overall_health_score) | [{"table": "jira__project_risk_assessment", "column": "overall_health_score"}] | [] | False |


## S20

类别 `data`；来源 `python`；调用 `9fbad0eebdc2492f8b98f403c2b1dbb0`；状态 `success`。

```sql
SELECT direct_network_connections, total_projects_involved, cross_functional_projects, engagement_breadth_score, engagement_depth_score, engagement_quality_score, engagement_impact_score, total_engagement_score, strategic_value_score, total_outbound_influence, total_inbound_influence, avg_outbound_influence_strength FROM jira__stakeholder_engagement_insights
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-062/attempt-01/sql/S20.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-062/attempt-01/sql/S20.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-062/attempt-01/results/S20.rows.jsonl)；完整：True；SHA256：`2309a4de53e555076bf767f6632d156821a8f88bd2f16514aeef6bcc3217f319`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "jira__stakeholder_engagement_insights", "kind": "base", "block": null, "base_tables": ["jira__stakeholder_engagement_insights"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |


## S21

类别 `data`；来源 `python`；调用 `9fbad0eebdc2492f8b98f403c2b1dbb0`；状态 `success`。

```sql
SELECT complexity_risk_score, success_probability, overall_health_score, total_risk_score, health_risk_score, schedule_risk_score, resource_risk_score, scope_risk_score, value_delivery_percentage, team_stability_percentage, total_hours_invested, estimated_project_value_points, delivered_value_points, sprint_adoption_rate, unique_issue_types, unique_components, total_external_links FROM jira__project_risk_assessment
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-062/attempt-01/sql/S21.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-062/attempt-01/sql/S21.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-062/attempt-01/results/S21.rows.jsonl)；完整：True；SHA256：`a76d30abb028337d84e765f17eb7b5bbe6a1a904d5249bae2cfb1d4846e2fa5a`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "jira__project_risk_assessment", "kind": "base", "block": null, "base_tables": ["jira__project_risk_assessment"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |


## S22

类别 `data`；来源 `query_db`；调用 `f5d56ea5001341acba592710799607e5`；状态 `success`。

```sql
SELECT 
  CASE 
    WHEN direct_network_connections <= 5 THEN 'low_(<=5)'
    WHEN direct_network_connections <= 20 THEN 'mid_(6-20)'
    ELSE 'high_(>20)'
  END AS conn_group,
  engagement_risk_status,
  COUNT(*) AS n,
  ROUND(AVG(total_engagement_score),2) AS avg_engagement
FROM jira__stakeholder_engagement_insights
GROUP BY conn_group, engagement_risk_status
ORDER BY conn_group, engagement_risk_status
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-062/attempt-01/sql/S22.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-062/attempt-01/sql/S22.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-062/attempt-01/results/S22.rows.jsonl)；完整：True；SHA256：`45d2d1d8e7854b79bb87ce6ad166ccc8a70b6d2dab1a31bf42c5bfd315dac27b`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "jira__stakeholder_engagement_insights", "kind": "base", "block": null, "base_tables": ["jira__stakeholder_engagement_insights"]}] | [] | ["CASE WHEN direct_network_connections <= 5 THEN 'low_(<=5)' WHEN direct_network_connections <= 20 THEN 'mid_(6-20)' ELSE 'high_(>20)' END", "engagement_risk_status"] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |
| B1 | AVG(total_engagement_score) | [{"table": "jira__stakeholder_engagement_insights", "column": "total_engagement_score"}] | [] | False |


## S23

类别 `data`；来源 `query_db`；调用 `825c64522b9a49cc8d9472946ae3fa4a`；状态 `success`。

```sql
SELECT success_probability, COUNT(*) AS n
FROM jira__project_risk_assessment
GROUP BY success_probability
ORDER BY success_probability
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-062/attempt-01/sql/S23.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-062/attempt-01/sql/S23.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-062/attempt-01/results/S23.rows.jsonl)；完整：True；SHA256：`a6397d90b3a7b81667f676f123ab54fc2a73f9a93c0724a38278b15237b28ecd`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "jira__project_risk_assessment", "kind": "base", "block": null, "base_tables": ["jira__project_risk_assessment"]}] | [] | ["success_probability"] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |


## S24

类别 `data`；来源 `query_db`；调用 `1edd7fdd77b642a8ae5e0773524841a4`；状态 `success`。

```sql
SELECT 
  trajectory_status,
  ROUND(AVG(complexity_risk_score),2) AS avg_complexity,
  ROUND(AVG(success_probability),3) AS avg_success,
  ROUND(AVG(total_risk_score),2) AS avg_total_risk,
  ROUND(AVG(health_risk_score),2) AS avg_health_risk,
  ROUND(AVG(schedule_risk_score),2) AS avg_schedule_risk,
  ROUND(AVG(resource_risk_score),2) AS avg_resource_risk,
  ROUND(AVG(scope_risk_score),2) AS avg_scope_risk
FROM jira__project_risk_assessment
GROUP BY trajectory_status
ORDER BY avg_total_risk DESC
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-062/attempt-01/sql/S24.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-062/attempt-01/sql/S24.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-062/attempt-01/results/S24.rows.jsonl)；完整：True；SHA256：`10ea75af28262627873d0dae6f68dcb7a3551073ccaf8e89062c8130fcfdfbec`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "jira__project_risk_assessment", "kind": "base", "block": null, "base_tables": ["jira__project_risk_assessment"]}] | [] | ["trajectory_status"] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | AVG(complexity_risk_score) | [{"table": "jira__project_risk_assessment", "column": "complexity_risk_score"}] | [] | False |
| B1 | AVG(success_probability) | [{"table": "jira__project_risk_assessment", "column": "success_probability"}] | [] | False |
| B1 | AVG(total_risk_score) | [{"table": "jira__project_risk_assessment", "column": "total_risk_score"}] | [] | False |
| B1 | AVG(health_risk_score) | [{"table": "jira__project_risk_assessment", "column": "health_risk_score"}] | [] | False |
| B1 | AVG(schedule_risk_score) | [{"table": "jira__project_risk_assessment", "column": "schedule_risk_score"}] | [] | False |
| B1 | AVG(resource_risk_score) | [{"table": "jira__project_risk_assessment", "column": "resource_risk_score"}] | [] | False |
| B1 | AVG(scope_risk_score) | [{"table": "jira__project_risk_assessment", "column": "scope_risk_score"}] | [] | False |


## S25

类别 `data`；来源 `query_db`；调用 `967fbc3b52b34f08a958363181da10d4`；状态 `success`。

```sql
SELECT 
  SUM(total_projects_involved) AS total_involvements,
  SUM(cross_functional_projects) AS total_cross_func,
  COUNT(*) AS n_stakeholders,
  COUNT(DISTINCT total_projects_involved) AS distinct_project_counts
FROM jira__stakeholder_engagement_insights
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-062/attempt-01/sql/S25.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-062/attempt-01/sql/S25.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-062/attempt-01/results/S25.rows.jsonl)；完整：True；SHA256：`1ad04d8b6fa49b7334c79d050cdcf06bbb6a3a493059ded80b9ad9172ff00003`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "jira__stakeholder_engagement_insights", "kind": "base", "block": null, "base_tables": ["jira__stakeholder_engagement_insights"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | SUM(total_projects_involved) | [{"table": "jira__stakeholder_engagement_insights", "column": "total_projects_involved"}] | [] | False |
| B1 | SUM(cross_functional_projects) | [{"table": "jira__stakeholder_engagement_insights", "column": "cross_functional_projects"}] | [] | False |
| B1 | COUNT(*) | [] | [] | True |
| B1 | COUNT(DISTINCT total_projects_involved) | [{"table": "jira__stakeholder_engagement_insights", "column": "total_projects_involved"}] | [] | False |


## S26

类别 `data`；来源 `query_db`；调用 `1f75b716b243472396a27157e6443097`；状态 `success`。

```sql
SELECT COUNT(*) AS total,
       SUM(CASE WHEN stakeholder_id LIKE '%PRO%' THEN 1 ELSE 0 END) AS id_has_pro,
       SUM(CASE WHEN user_display_name LIKE '%PRO%' THEN 1 ELSE 0 END) AS name_has_pro,
       SUM(CASE WHEN stakeholder_archetype LIKE '%PRO%' THEN 1 ELSE 0 END) AS archetype_has_pro,
       SUM(CASE WHEN recommended_engagement_strategy LIKE '%PRO%' THEN 1 ELSE 0 END) AS strategy_has_pro,
       SUM(CASE WHEN development_opportunity LIKE '%PRO%' THEN 1 ELSE 0 END) AS dev_has_pro
FROM jira__stakeholder_engagement_insights
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-062/attempt-01/sql/S26.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-062/attempt-01/sql/S26.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-062/attempt-01/results/S26.rows.jsonl)；完整：True；SHA256：`0990f5be173671aaa69d8e76dbd9465a408113f400fb28187bb672c9ae98b03f`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "jira__stakeholder_engagement_insights", "kind": "base", "block": null, "base_tables": ["jira__stakeholder_engagement_insights"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |
| B1 | SUM(CASE WHEN stakeholder_id LIKE '%PRO%' THEN 1 ELSE 0 END) | [] | [{"table": "jira__stakeholder_engagement_insights", "column": "stakeholder_id"}] | False |
| B1 | SUM(CASE WHEN user_display_name LIKE '%PRO%' THEN 1 ELSE 0 END) | [] | [{"table": "jira__stakeholder_engagement_insights", "column": "user_display_name"}] | False |
| B1 | SUM(CASE WHEN stakeholder_archetype LIKE '%PRO%' THEN 1 ELSE 0 END) | [] | [{"table": "jira__stakeholder_engagement_insights", "column": "stakeholder_archetype"}] | False |
| B1 | SUM(CASE WHEN recommended_engagement_strategy LIKE '%PRO%' THEN 1 ELSE 0 END) | [] | [{"table": "jira__stakeholder_engagement_insights", "column": "recommended_engagement_strategy"}] | False |
| B1 | SUM(CASE WHEN development_opportunity LIKE '%PRO%' THEN 1 ELSE 0 END) | [] | [{"table": "jira__stakeholder_engagement_insights", "column": "development_opportunity"}] | False |


## S27

类别 `data`；来源 `query_db`；调用 `aab74522cf6d4c7aa33b110b156fae67`；状态 `success`。

```sql
SELECT COUNT(DISTINCT project_key) AS distinct_keys,
       COUNT(DISTINCT project_name) AS distinct_names,
       COUNT(DISTINCT project_id) AS distinct_ids
FROM jira__project_risk_assessment
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-062/attempt-01/sql/S27.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-062/attempt-01/sql/S27.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-062/attempt-01/results/S27.rows.jsonl)；完整：True；SHA256：`f4cf805718a0c8b4eb0e7f4278c91e137665b406032ea7cf7206123344a2bd83`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "jira__project_risk_assessment", "kind": "base", "block": null, "base_tables": ["jira__project_risk_assessment"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(DISTINCT project_key) | [{"table": "jira__project_risk_assessment", "column": "project_key"}] | [] | False |
| B1 | COUNT(DISTINCT project_name) | [{"table": "jira__project_risk_assessment", "column": "project_name"}] | [] | False |
| B1 | COUNT(DISTINCT project_id) | [{"table": "jira__project_risk_assessment", "column": "project_id"}] | [] | False |


## S28

类别 `data`；来源 `query_db`；调用 `664bda9fb95149f3bafabf1d5804318a`；状态 `success`。

```sql
SELECT 
  CASE 
    WHEN team_stability_percentage < 60 THEN 'low_stability_(<60)'
    WHEN team_stability_percentage < 75 THEN 'medium_stability_(60-75)'
    ELSE 'high_stability_(>=75)'
  END AS stability_bucket,
  COUNT(*) AS n,
  ROUND(AVG(complexity_risk_score),2) AS avg_complexity,
  ROUND(AVG(success_probability),3) AS avg_success,
  ROUND(AVG(team_stability_percentage),2) AS avg_stability,
  ROUND(AVG(value_delivery_percentage),2) AS avg_vdp,
  ROUND(AVG(total_risk_score),2) AS avg_total_risk
FROM jira__project_risk_assessment
GROUP BY stability_bucket
ORDER BY stability_bucket
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-062/attempt-01/sql/S28.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-062/attempt-01/sql/S28.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-062/attempt-01/results/S28.rows.jsonl)；完整：True；SHA256：`e39d251d551221b13cfb5d7f9972c13b5cdcbd20d5555905331dc0baaf316c86`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "jira__project_risk_assessment", "kind": "base", "block": null, "base_tables": ["jira__project_risk_assessment"]}] | [] | ["CASE WHEN team_stability_percentage < 60 THEN 'low_stability_(<60)' WHEN team_stability_percentage < 75 THEN 'medium_stability_(60-75)' ELSE 'high_stability_(>=75)' END"] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |
| B1 | AVG(complexity_risk_score) | [{"table": "jira__project_risk_assessment", "column": "complexity_risk_score"}] | [] | False |
| B1 | AVG(success_probability) | [{"table": "jira__project_risk_assessment", "column": "success_probability"}] | [] | False |
| B1 | AVG(team_stability_percentage) | [{"table": "jira__project_risk_assessment", "column": "team_stability_percentage"}] | [] | False |
| B1 | AVG(value_delivery_percentage) | [{"table": "jira__project_risk_assessment", "column": "value_delivery_percentage"}] | [] | False |
| B1 | AVG(total_risk_score) | [{"table": "jira__project_risk_assessment", "column": "total_risk_score"}] | [] | False |


## S29

类别 `data`；来源 `query_db`；调用 `a7a8eb31508c401c801f1d6c8fdbcc69`；状态 `success`。

```sql
SELECT 
  CASE 
    WHEN sprint_adoption_rate < 0.5 THEN 'low_sprint_adoption'
    WHEN sprint_adoption_rate < 0.8 THEN 'medium_sprint_adoption'
    ELSE 'high_sprint_adoption'
  END AS sprint_bucket,
  COUNT(*) AS n,
  ROUND(AVG(complexity_risk_score),2) AS avg_complexity,
  ROUND(AVG(success_probability),3) AS avg_success,
  ROUND(AVG(sprint_adoption_rate),2) AS avg_sprint,
  ROUND(AVG(value_delivery_percentage),2) AS avg_vdp,
  ROUND(AVG(total_risk_score),2) AS avg_total_risk
FROM jira__project_risk_assessment
GROUP BY sprint_bucket
ORDER BY sprint_bucket
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-062/attempt-01/sql/S29.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-062/attempt-01/sql/S29.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-062/attempt-01/results/S29.rows.jsonl)；完整：True；SHA256：`954b2e0a3b39651d0811d8bcbe45835e5f256818f6cc350989bbb673e2a99cd0`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "jira__project_risk_assessment", "kind": "base", "block": null, "base_tables": ["jira__project_risk_assessment"]}] | [] | ["CASE WHEN sprint_adoption_rate < 0.5 THEN 'low_sprint_adoption' WHEN sprint_adoption_rate < 0.8 THEN 'medium_sprint_adoption' ELSE 'high_sprint_adoption' END"] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |
| B1 | AVG(complexity_risk_score) | [{"table": "jira__project_risk_assessment", "column": "complexity_risk_score"}] | [] | False |
| B1 | AVG(success_probability) | [{"table": "jira__project_risk_assessment", "column": "success_probability"}] | [] | False |
| B1 | AVG(sprint_adoption_rate) | [{"table": "jira__project_risk_assessment", "column": "sprint_adoption_rate"}] | [] | False |
| B1 | AVG(value_delivery_percentage) | [{"table": "jira__project_risk_assessment", "column": "value_delivery_percentage"}] | [] | False |
| B1 | AVG(total_risk_score) | [{"table": "jira__project_risk_assessment", "column": "total_risk_score"}] | [] | False |


## S30

类别 `data`；来源 `python`；调用 `fc3fbe8c726e4363951c8cc144b3e478`；状态 `success`。

```sql
SELECT complexity_risk_score, success_probability, overall_health_score, total_risk_score, health_risk_score, schedule_risk_score, resource_risk_score, scope_risk_score, value_delivery_percentage, team_stability_percentage, total_hours_invested, estimated_project_value_points, delivered_value_points, sprint_adoption_rate, unique_issue_types, unique_components, total_external_links, net_issue_growth_30d, resolution_velocity_change_percent, trajectory_status, risk_category, primary_risk_factor, primary_risk_driver FROM jira__project_risk_assessment
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-062/attempt-01/sql/S30.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-062/attempt-01/sql/S30.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-062/attempt-01/results/S30.rows.jsonl)；完整：True；SHA256：`6baa81673348088194cfe753400c86ae538d7f23e934d2b0464388658e0b3a7f`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "jira__project_risk_assessment", "kind": "base", "block": null, "base_tables": ["jira__project_risk_assessment"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |


## S31

类别 `data`；来源 `python`；调用 `07bec966b2824b00b9bdf10d9bb36a93`；状态 `success`。

```sql
SELECT complexity_risk_score, success_probability, overall_health_score, total_risk_score, health_risk_score, schedule_risk_score, resource_risk_score, scope_risk_score, value_delivery_percentage, team_stability_percentage, total_hours_invested, estimated_project_value_points, delivered_value_points, sprint_adoption_rate, unique_issue_types, unique_components, total_external_links, net_issue_growth_30d, resolution_velocity_change_percent, trajectory_status, risk_category, primary_risk_factor, primary_risk_driver FROM jira__project_risk_assessment
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-062/attempt-01/sql/S31.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-062/attempt-01/sql/S31.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-062/attempt-01/results/S31.rows.jsonl)；完整：True；SHA256：`6baa81673348088194cfe753400c86ae538d7f23e934d2b0464388658e0b3a7f`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "jira__project_risk_assessment", "kind": "base", "block": null, "base_tables": ["jira__project_risk_assessment"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |


## S32

类别 `data`；来源 `python`；调用 `6f1363ccd9594ccdaf6c99c1db73ef1f`；状态 `success`。

```sql
SELECT complexity_risk_score, success_probability, overall_health_score, total_risk_score, health_risk_score, schedule_risk_score, resource_risk_score, scope_risk_score, value_delivery_percentage, team_stability_percentage, total_hours_invested, estimated_project_value_points, delivered_value_points, sprint_adoption_rate, unique_issue_types, unique_components, total_external_links, net_issue_growth_30d, resolution_velocity_change_percent, trajectory_status, risk_category, primary_risk_factor, primary_risk_driver FROM jira__project_risk_assessment
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-062/attempt-01/sql/S32.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-062/attempt-01/sql/S32.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-062/attempt-01/results/S32.rows.jsonl)；完整：True；SHA256：`6baa81673348088194cfe753400c86ae538d7f23e934d2b0464388658e0b3a7f`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "jira__project_risk_assessment", "kind": "base", "block": null, "base_tables": ["jira__project_risk_assessment"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |


## S33

类别 `data`；来源 `python`；调用 `6f1363ccd9594ccdaf6c99c1db73ef1f`；状态 `success`。

```sql
SELECT direct_network_connections, total_projects_involved, cross_functional_projects, engagement_breadth_score, engagement_quality_score, engagement_impact_score, total_engagement_score, strategic_value_score, total_outbound_influence, total_inbound_influence, stakeholder_archetype, influence_level, engagement_risk_status FROM jira__stakeholder_engagement_insights
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-062/attempt-01/sql/S33.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-062/attempt-01/sql/S33.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-062/attempt-01/results/S33.rows.jsonl)；完整：True；SHA256：`413b16fce4c1515715a92184f16f7c622690c9164ae78b6dcffc152375251198`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "jira__stakeholder_engagement_insights", "kind": "base", "block": null, "base_tables": ["jira__stakeholder_engagement_insights"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |

