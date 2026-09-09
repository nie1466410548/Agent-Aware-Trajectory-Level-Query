# dacomp-084

The company is redesigning its organizational structure, and I want you to identify the op…

运行：已提交。官方未评分。全部 SQL 尝试/成功 36/34；数据 SQL 34/32；Python 9 次。

完整原题：

The company is redesigning its organizational structure, and I want you to identify the optimal organizational size and management configuration model from a data perspective. Please segment all organizations into four tiers based on `current_active_employees`: Small (under 30), Medium (30-120), Large (120-300), and Extra Large (over 300). Then, for each tier, calculate the distribution characteristics of `organization_health_score` and the composition ratio of `performance_category`. Focus on analyzing the optimal range for `management_ratio` across different organization sizes by comparing key indicators such as `avg_employee_performance_score`, `position_fill_rate`, and `annual_turnover_rate`. Identify the common characteristics of the top 10% performing organizations in each size tier. Finally, based on these findings, provide quantitative management configuration recommendations for organizations of different sizes, including specific values for optimal management ratios, staffing density, and other metrics.

| 表 | 行数 | 列数 |
| --- | --- | --- |
| workday__organization_overview | 118 | 64 |
| workday__organization_performance | 118 | 66 |


实际路线（分析者依据 SQL/源码概括，不代表 Agent 自述）：SQL 提取组织规模、健康与绩效 → Python 合并、分箱排名和前十分位比较 → 管理配置建议。

数据库大小：114,688 字节。

## 数据 SQL

| SQL | 状态 | 基础表 | Join 输入/类型 | GROUP BY | 聚合表达式 | 结果行数 | 数据库 ms |
| --- | --- | --- | --- | --- | --- | --- | --- |
| [S3/Q1](#s3) | success | ["workday__organization_overview"] | 0 / {} | [] | ["COUNT(*)"] | 1 | 0.337 |
| [S4/Q2](#s4) | success | ["workday__organization_performance"] | 0 / {} | [] | ["COUNT(*)"] | 1 | 0.322 |
| [S5/Q3](#s5) | success | ["workday__organization_overview"] | 0 / {} | [] | [] | 5 | 0.551 |
| [S6/Q4](#s6) | success | ["workday__organization_performance"] | 0 / {} | [] | [] | 5 | 0.514 |
| [S7/Q5](#s7) | success | ["workday__organization_overview"] | 0 / {} | ["data_quality_flag"] | ["COUNT(*)"] | 1 | 0.367 |
| [S8/Q6](#s8) | success | ["workday__organization_overview"] | 0 / {} | ["performance_category"] | ["COUNT(*)", "AVG(organization_health_score)", "MIN(organization_health_score)", "MAX(organization_health_score)"] | 4 | 0.488 |
| [S9/Q7](#s9) | success | ["workday__organization_overview"] | 0 / {} | ["organization_size_category"] | ["COUNT(*)"] | 4 | 0.392 |
| [S10/Q8](#s10) | success | ["workday__organization_overview"] | 0 / {} | [] | [] | 20 | 0.425 |
| [S11/Q9](#s11) | success | ["workday__organization_overview"] | 0 / {} | [] | [] | 18 | 0.378 |
| [S12/Q10](#s12) | success | ["workday__organization_overview"] | 0 / {} | [] | [] | 0 | 0.383 |
| [S13/Q11](#s13) | success | ["workday__organization_overview"] | 0 / {} | ["CASE WHEN current_active_employees < 30 THEN 'Small (<30)' WHEN current_active_employees BETWEEN 30 AND 120 THEN 'Medium (30-120)' WHEN current_active_employees BETWEEN 121 AND 300 THEN 'Large (120-300)' ELSE 'Extra Large (>300)' END", "organization_size_category"] | ["COUNT(*)"] | 4 | 0.454 |
| [S14/Q12](#s14) | success | ["workday__organization_overview"] | 0 / {} | ["organization_size_category"] | ["COUNT(*)", "AVG(organization_health_score)", "MIN(organization_health_score)", "MAX(organization_health_score)", "AVG(management_ratio)", "MIN(management_ratio)", "MAX(management_ratio)", "AVG(avg_employee_performance_score)", "AVG(position_fill_rate)", "AVG(annual_turnover_rate)", "AVG(current_active_employees)"] | 4 | 0.544 |
| [S15/Q13](#s15) | success | ["workday__organization_overview"] | 0 / {} | ["organization_size_category", "performance_category"] | ["COUNT(*)", "COUNT(*)", "COUNT(*)"] | 16 | 0.61 |
| [S16/Q14](#s16) | success | ["workday__organization_performance"] | 0 / {} | [] | ["COUNT(*)", "SUM(CASE WHEN NOT span_of_control IS NULL THEN 1 ELSE 0 END)", "SUM(CASE WHEN NOT talent_density_ratio IS NULL THEN 1 ELSE 0 END)", "SUM(CASE WHEN NOT high_value_retention_rate IS NULL THEN 1 ELSE 0 END)", "SUM(CASE WHEN NOT talent_flight_risk_rate IS NULL THEN 1 ELSE 0 END)", "SUM(CASE WHEN NOT high_achiever_percentage IS NULL THEN 1 ELSE 0 END)", "SUM(CASE WHEN NOT avg_employee_satisfaction_proxy IS NULL THEN 1 ELSE 0 END)"] | 1 | 0.462 |
| [S17/Q15](#s17) | failed | ["workday__organization_overview"] | 0 / {} | ["organization_size_category"] | ["MIN(organization_health_score)", "MAX(organization_health_score)", "AVG(organization_health_score)", "PERCENTILE_CONT(organization_health_score, 0.5)", "STDDEV(organization_health_score)"] | unknown | 未取得；调用总时长 0.178 ms |
| [S18/Q16](#s18) | success | ["workday__organization_overview"] | 0 / {} | ["organization_size_category"] | ["MIN(organization_health_score)", "AVG(organization_health_score)", "MIN(organization_health_score)", "MAX(organization_health_score)", "AVG(CASE WHEN organization_health_score <= (SELECT MIN(organization_health_score) FROM workday__organization_overview AS o2 WHERE o2.organization_size_category = t.organization_size_category) THEN organization_health_score END)"] | 4 | 3.154 |
| [S19/Q17](#s19) | failed | ["workday__organization_overview"] | 0 / {} | ["organization_size_category"] | ["AVG(organization_health_score)", "AVG(CASE WHEN rn * 1.0 / n <= 0.25 THEN organization_health_score END)", "AVG(CASE WHEN rn * 1.0 / n <= 0.5 AND rn * 1.0 / n > 0.25 THEN organization_health_score END)", "AVG(CASE WHEN rn * 1.0 / n <= 0.75 AND rn * 1.0 / n > 0.5 THEN organization_health_score END)", "STDDEV(organization_health_score)"] | unknown | 未取得；调用总时长 0.216 ms |
| [S20/Q18](#s20) | success | ["workday__organization_overview"] | 0 / {} | ["organization_size_category"] | ["MIN(management_ratio)", "MAX(management_ratio)", "AVG(management_ratio)"] | 4 | 0.587 |
| [S21/Q19](#s21) | success | ["workday__organization_overview"] | 0 / {} | ["CASE WHEN management_ratio < 0.15 THEN 'A: <0.15' WHEN management_ratio < 0.18 THEN 'B: 0.15-0.18' WHEN management_ratio < 0.21 THEN 'C: 0.18-0.21' WHEN management_ratio < 0.25 THEN 'D: 0.21-0.25' ELSE 'E: >=0.25' END"] | ["COUNT(*)", "AVG(organization_health_score)", "AVG(avg_employee_performance_score)", "AVG(position_fill_rate)", "AVG(annual_turnover_rate)"] | 5 | 0.527 |
| [S22/Q20](#s22) | success | ["workday__organization_overview"] | 0 / {} | ["organization_size_category", "CASE WHEN management_ratio < 0.15 THEN 'A: <0.15' WHEN management_ratio < 0.18 THEN 'B: 0.15-0.18' WHEN management_ratio < 0.21 THEN 'C: 0.18-0.21' WHEN management_ratio < 0.25 THEN 'D: 0.21-0.25' ELSE 'E: >=0.25' END"] | ["COUNT(*)", "AVG(organization_health_score)", "AVG(avg_employee_performance_score)", "AVG(position_fill_rate)", "AVG(annual_turnover_rate)"] | 13 | 0.616 |
| [S23/Q21](#s23) | success | ["workday__organization_overview"] | 0 / {} | [] | [] | 14 | 1.254 |
| [S24/Q22](#s24) | success | ["workday__organization_overview"] | 0 / {} | ["organization_size_category", "CASE WHEN rn <= CEIL(n * 0.1) THEN 'Top10%' ELSE 'Rest' END"] | ["COUNT(*)", "AVG(organization_health_score)", "AVG(management_ratio)", "AVG(avg_employee_performance_score)", "AVG(position_fill_rate)", "AVG(annual_turnover_rate)", "AVG(avg_career_development_score)", "AVG(avg_retention_stability_score)", "AVG(avg_current_tenure_years)", "AVG(organization_age_years)"] | 8 | 2.948 |
| [S25/Q23](#s25) | success | ["workday__organization_overview"] | 0 / {} | [] | ["SUM(CASE WHEN avg_career_development_score > 0 THEN 1 ELSE 0 END)", "SUM(CASE WHEN avg_retention_stability_score > 0 THEN 1 ELSE 0 END)", "SUM(CASE WHEN avg_current_tenure_years > 0 THEN 1 ELSE 0 END)", "SUM(CASE WHEN high_value_stable_employees > 0 THEN 1 ELSE 0 END)", "SUM(CASE WHEN management_role_employees > 0 THEN 1 ELSE 0 END)", "SUM(CASE WHEN high_risk_employee_percentage > 0 THEN 1 ELSE 0 END)", "SUM(CASE WHEN total_promotions_in_organization > 0 THEN 1 ELSE 0 END)", "SUM(CASE WHEN avg_employee_age > 0 THEN 1 ELSE 0 END)"] | 1 | 0.472 |
| [S26/Q24](#s26) | success | ["workday__organization_overview"] | 0 / {} | [] | [] | 14 | 2.764 |
| [S27/Q25](#s27) | success | ["workday__organization_overview"] | 0 / {} | [] | [] | 118 | 0.735 |
| [S28/Q26](#s28) | success | ["workday__organization_performance"] | 0 / {} | [] | [] | 118 | 0.437 |
| [S29/Q27](#s29) | success | ["workday__organization_overview"] | 0 / {} | [] | [] | 118 | 0.65 |
| [S30/Q28](#s30) | success | ["workday__organization_performance"] | 0 / {} | [] | [] | 118 | 0.421 |
| [S31/Q29](#s31) | success | ["workday__organization_overview"] | 0 / {} | [] | [] | 118 | 0.641 |
| [S32/Q30](#s32) | success | ["workday__organization_overview"] | 0 / {} | [] | [] | 118 | 0.635 |
| [S33/Q31](#s33) | success | ["workday__organization_overview"] | 0 / {} | [] | [] | 118 | 0.747 |
| [S34/Q32](#s34) | success | ["workday__organization_overview"] | 0 / {} | [] | [] | 118 | 0.542 |
| [S35/Q33](#s35) | success | ["workday__organization_overview"] | 0 / {} | [] | [] | 118 | 0.545 |
| [S36/Q34](#s36) | success | ["workday__organization_overview"] | 0 / {} | [] | [] | 118 | 0.59 |


## 元数据和设置

| SQL | 类别 | 状态 | 内容 |
| --- | --- | --- | --- |
| S1 | connection_setup | success | PRAGMA query_only=ON |
| S2 | metadata | success | SELECT name,sql FROM sqlite_master WHERE type='table' ORDER BY name |


## Python 与执行位置

人工源码审查：**database_first_violation**。Python 合并组织绩效数据，按规模与管理比例分箱计算均值和数量，并用组内排名/计数识别前 10%。这些 SQL 可支持的连接、聚合和窗口操作迁出数据库；相关分析与绘图另行评价。 [证据](../reviews/dacomp-084.json)。

P1：Computing detailed distribution statistics (percentiles, std) for health scores per tier, which SQLite does not support natively (no STDDEV, MEDIAN, PERCENTILE). Also computing management_ratio bin optimization and creating visualizations.

[源码](../../../runs/dsv4flash-db-first-full-01/dacomp-084/attempt-01/python/P1.py)；[输出](../../../runs/dsv4flash-db-first-full-01/dacomp-084/attempt-01/python/P1.stdout)；[错误](../../../runs/dsv4flash-db-first-full-01/dacomp-084/attempt-01/python/P1.stderr)。检出需人工核验的 SQL 可实现操作：.merge(, .query(；不能仅凭理由判为合规。

P2：Computing distribution statistics (percentiles, std) for health scores per tier, performance category composition ratios, and management ratio stats - statistical summaries that require percentile/std calculations better handled in Python.

[源码](../../../runs/dsv4flash-db-first-full-01/dacomp-084/attempt-01/python/P2.py)；[输出](../../../runs/dsv4flash-db-first-full-01/dacomp-084/attempt-01/python/P2.stdout)；[错误](../../../runs/dsv4flash-db-first-full-01/dacomp-084/attempt-01/python/P2.stderr)。检出需人工核验的 SQL 可实现操作：groupby(；不能仅凭理由判为合规。

P3：Python is used for distribution statistics (percentiles/std), stacked-bar composition chart, and boxplot visualization which are statistical/visualization procedures not supported by SQLite.

[源码](../../../runs/dsv4flash-db-first-full-01/dacomp-084/attempt-01/python/P3.py)；[输出](../../../runs/dsv4flash-db-first-full-01/dacomp-084/attempt-01/python/P3.stdout)；[错误](../../../runs/dsv4flash-db-first-full-01/dacomp-084/attempt-01/python/P3.stderr)。检出需人工核验的 SQL 可实现操作：groupby(, .merge(, .query(；不能仅凭理由判为合规。

P4：Complex multi-dimensional grouping by tier-specific management_ratio bins, aggregating multiple metrics, and creating bar chart dashboard - all statistical/visualization procedures best done in Python.

[源码](../../../runs/dsv4flash-db-first-full-01/dacomp-084/attempt-01/python/P4.py)；[输出](../../../runs/dsv4flash-db-first-full-01/dacomp-084/attempt-01/python/P4.stdout)；[错误](../../../runs/dsv4flash-db-first-full-01/dacomp-084/attempt-01/python/P4.stderr)。检出需人工核验的 SQL 可实现操作：groupby(, .query(；不能仅凭理由判为合规。

P5：Statistical grouping and comparison of top 10% vs rest, including bar chart visualization - these are statistical/visualization procedures not supported by SQLite.

[源码](../../../runs/dsv4flash-db-first-full-01/dacomp-084/attempt-01/python/P5.py)；[输出](../../../runs/dsv4flash-db-first-full-01/dacomp-084/attempt-01/python/P5.stdout)；[错误](../../../runs/dsv4flash-db-first-full-01/dacomp-084/attempt-01/python/P5.stderr)。检出需人工核验的 SQL 可实现操作：groupby(, .query(, sort_values(；不能仅凭理由判为合规。

P6：Extracting the detailed top-10% organization list with proper columns and summarizing their common characteristics for the report.

[源码](../../../runs/dsv4flash-db-first-full-01/dacomp-084/attempt-01/python/P6.py)；[输出](../../../runs/dsv4flash-db-first-full-01/dacomp-084/attempt-01/python/P6.stdout)；[错误](../../../runs/dsv4flash-db-first-full-01/dacomp-084/attempt-01/python/P6.stderr)。检出需人工核验的 SQL 可实现操作：groupby(, .query(, sort_values(；不能仅凭理由判为合规。

P7：Creating a comprehensive multi-panel analysis figure with scatter plots and histograms, and computing optimal management ratio recommendations using binning - statistical/visualization procedures not supported by SQLite.

[源码](../../../runs/dsv4flash-db-first-full-01/dacomp-084/attempt-01/python/P7.py)；[输出](../../../runs/dsv4flash-db-first-full-01/dacomp-084/attempt-01/python/P7.stdout)；[错误](../../../runs/dsv4flash-db-first-full-01/dacomp-084/attempt-01/python/P7.stderr)。检出需人工核验的 SQL 可实现操作：groupby(, .query(；不能仅凭理由判为合规。

P8：Constructing the final recommendation summary table and visualization, plus validating fill-rate/turnover thresholds for top performers vs rest using descriptive statistics in Python.

[源码](../../../runs/dsv4flash-db-first-full-01/dacomp-084/attempt-01/python/P8.py)；[输出](../../../runs/dsv4flash-db-first-full-01/dacomp-084/attempt-01/python/P8.stdout)；[错误](../../../runs/dsv4flash-db-first-full-01/dacomp-084/attempt-01/python/P8.stderr)。检出需人工核验的 SQL 可实现操作：groupby(, .query(；不能仅凭理由判为合规。

P9：Computing Pearson correlations between management ratio, fill rate, turnover, performance score and health score - a statistical procedure that requires scipy and is outside SQLite's capabilities.

[源码](../../../runs/dsv4flash-db-first-full-01/dacomp-084/attempt-01/python/P9.py)；[输出](../../../runs/dsv4flash-db-first-full-01/dacomp-084/attempt-01/python/P9.stdout)；[错误](../../../runs/dsv4flash-db-first-full-01/dacomp-084/attempt-01/python/P9.stderr)。检出需人工核验的 SQL 可实现操作：.query(；不能仅凭理由判为合规。

## 优化机会

已验证候选。筛选限于精确 SQL、相同自包含 CTE、相同单表完整过滤、可分解单表聚合；未覆盖任意 Join 等价和一般谓词蕴含。全部候选都是 offline，未测在线预测。

| 候选 | 类型 | 已有结果 | 覆盖 SQL | 后续次数 | 中间行数 | 验证 | 成本 |
| --- | --- | --- | --- | --- | --- | --- | --- |
| C1 | exact-result reuse | True | ["S27", "S29", "S32"] | 2 | 118 | verified | Not benchmarked; correctness alone does not establish net speedup. |
| C2 | exact-result reuse | True | ["S31", "S34", "S36"] | 2 | 118 | verified | Not benchmarked; correctness alone does not establish net speedup. |
| C3 | common subexpression | False | ["S24", "S26"] | 1 | unknown | not_verified_cap | Not tested |
| C4 | aggregate MV | False | ["S3", "S7", "S8", "S9", "S13", "S14", "S20", "S21", "S22", "S25"] | 9 | 45 | verified | Not benchmarked; correctness alone does not establish net speedup. |
| C5 | aggregate MV | False | ["S4", "S16"] | 1 | unknown | not_verified_cap | Not tested |


已验证覆盖（含触发查询、候选并集去重）：16/32 条成功数据 SQL。正确性仅针对当前数据库快照；未测性能的候选不能声称已加速。

[完整 build/rewrite 与比较证据](dacomp-084.analysis.json)。

### C4：aggregate MV

Union of grouping keys; decomposable aggregate states; AVG uses SUM and non-NULL COUNT.

原查询 [S3](#s3), [S7](#s7), [S8](#s8), [S9](#s9), [S13](#s13), [S14](#s14), [S20](#s20), [S21](#s21), [S22](#s22), [S25](#s25) → 新增共享状态 C4 → 后续 9 次可复用。该构建点为事后假设，不代表 Agent 当时预知后续。

构建定义：

```sql
SELECT data_quality_flag AS __g0, performance_category AS __g1, organization_size_category AS __g2, CASE WHEN current_active_employees < 30 THEN 'Small (<30)' WHEN current_active_employees BETWEEN 30 AND 120 THEN 'Medium (30-120)' WHEN current_active_employees BETWEEN 121 AND 300 THEN 'Large (120-300)' ELSE 'Extra Large (>300)' END AS __g3, CASE WHEN management_ratio < 0.15 THEN 'A: <0.15' WHEN management_ratio < 0.18 THEN 'B: 0.15-0.18' WHEN management_ratio < 0.21 THEN 'C: 0.18-0.21' WHEN management_ratio < 0.25 THEN 'D: 0.21-0.25' ELSE 'E: >=0.25' END AS __g4, COUNT(*) AS __a0, SUM(organization_health_score) AS __a1_sum, COUNT(organization_health_score) AS __a1_n, MIN(organization_health_score) AS __a2, MAX(organization_health_score) AS __a3, SUM(management_ratio) AS __a4_sum, COUNT(management_ratio) AS __a4_n, MIN(management_ratio) AS __a5, MAX(management_ratio) AS __a6, SUM(avg_employee_performance_score) AS __a7_sum, COUNT(avg_employee_performance_score) AS __a7_n, SUM(position_fill_rate) AS __a8_sum, COUNT(position_fill_rate) AS __a8_n, SUM(annual_turnover_rate) AS __a9_sum, COUNT(annual_turnover_rate) AS __a9_n, SUM(current_active_employees) AS __a10_sum, COUNT(current_active_employees) AS __a10_n, SUM(CASE WHEN avg_career_development_score > 0 THEN 1 ELSE 0 END) AS __a11, SUM(CASE WHEN avg_retention_stability_score > 0 THEN 1 ELSE 0 END) AS __a12, SUM(CASE WHEN avg_current_tenure_years > 0 THEN 1 ELSE 0 END) AS __a13, SUM(CASE WHEN high_value_stable_employees > 0 THEN 1 ELSE 0 END) AS __a14, SUM(CASE WHEN management_role_employees > 0 THEN 1 ELSE 0 END) AS __a15, SUM(CASE WHEN high_risk_employee_percentage > 0 THEN 1 ELSE 0 END) AS __a16, SUM(CASE WHEN total_promotions_in_organization > 0 THEN 1 ELSE 0 END) AS __a17, SUM(CASE WHEN avg_employee_age > 0 THEN 1 ELSE 0 END) AS __a18 FROM "workday__organization_overview"  GROUP BY data_quality_flag, performance_category, organization_size_category, CASE WHEN current_active_employees < 30 THEN 'Small (<30)' WHEN current_active_employees BETWEEN 30 AND 120 THEN 'Medium (30-120)' WHEN current_active_employees BETWEEN 121 AND 300 THEN 'Large (120-300)' ELSE 'Extra Large (>300)' END, CASE WHEN management_ratio < 0.15 THEN 'A: <0.15' WHEN management_ratio < 0.18 THEN 'B: 0.15-0.18' WHEN management_ratio < 0.21 THEN 'C: 0.18-0.21' WHEN management_ratio < 0.25 THEN 'D: 0.21-0.25' ELSE 'E: >=0.25' END
```

受益查询 S3 的改写示例：

```sql
SELECT SUM(__a0) AS n_overview FROM temp.reuse_candidate
```

| 原 SQL | 列名一致 | 结果一致 | 比较方法 |
| --- | --- | --- | --- |
| S3 | True | True | exact_multiset |
| S7 | True | True | exact_multiset |
| S8 | True | True | ordered_numeric_tolerance |
| S9 | True | True | exact_multiset |
| S13 | True | True | ordered_numeric_tolerance |
| S14 | True | True | ordered_numeric_tolerance |
| S20 | True | True | exact_multiset |
| S21 | True | True | ordered_numeric_tolerance |
| S22 | True | True | ordered_numeric_tolerance |
| S25 | True | True | exact_multiset |


验证状态：verified；成本结论：Not benchmarked; correctness alone does not establish net speedup.

### C1：exact-result reuse

Identical normalized SQL and parameters; archive equality checked.

原查询 [S27](#s27), [S29](#s29), [S32](#s32) → 保留前序结果 S27 → 后续 2 次可复用。该构建点为事后假设，不代表 Agent 当时预知后续。

| 原 SQL | 列名一致 | 结果一致 | 比较方法 |
| --- | --- | --- | --- |
| S29 | True | True | exact_multiset |
| S32 | True | True | exact_multiset |


验证状态：verified；成本结论：Not benchmarked; correctness alone does not establish net speedup.

### C2：exact-result reuse

Identical normalized SQL and parameters; archive equality checked.

原查询 [S31](#s31), [S34](#s34), [S36](#s36) → 保留前序结果 S31 → 后续 2 次可复用。该构建点为事后假设，不代表 Agent 当时预知后续。

| 原 SQL | 列名一致 | 结果一致 | 比较方法 |
| --- | --- | --- | --- |
| S34 | True | True | exact_multiset |
| S36 | True | True | exact_multiset |


验证状态：verified；成本结论：Not benchmarked; correctness alone does not establish net speedup.

结果依赖：自动记录 SQL→Python 的接口父调用，以及源码中引用归档文件的消费者；字面值相同不认定因果。模型方向选择需要人工读取消息，尚未做全面因果标注。

[原始报告](../../../runs/dsv4flash-db-first-full-01/dacomp-084/attempt-01/answer.md)；[统一消息](../../../runs/dsv4flash-db-first-full-01/dacomp-084/attempt-01/messages.jsonl)；[原始 OpenCode 事件](../../../runs/dsv4flash-db-first-full-01/dacomp-084/attempt-01/opencode.jsonl)；[SQL 引擎日志](../../../runs/dsv4flash-db-first-full-01/dacomp-084/attempt-01/sql_journal.jsonl)。

[可读报告（本地图片链接规范化）](../answers/dacomp-084.md)。原始回答保留，分析结论未改写。

## S1

类别 `connection_setup`；来源 `connection`；调用 `22c838b580f7497096553ca7936d8679`；状态 `success`。

```sql
PRAGMA query_only=ON
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-084/attempt-01/sql/S1.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-084/attempt-01/sql/S1.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-084/attempt-01/results/S1.rows.jsonl)；完整：True；SHA256：`e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`。

## S2

类别 `metadata`；来源 `list_db`；调用 `22c838b580f7497096553ca7936d8679`；状态 `success`。

```sql
SELECT name,sql FROM sqlite_master WHERE type='table' ORDER BY name
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-084/attempt-01/sql/S2.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-084/attempt-01/sql/S2.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-084/attempt-01/results/S2.rows.jsonl)；完整：True；SHA256：`3a706420f1ed17ef79f108b417a1244b54d4c231672d31b225b96565e4223a0e`。

## S3

类别 `data`；来源 `query_db`；调用 `054c06cba56045698e89babf368a89ba`；状态 `success`。

```sql
SELECT COUNT(*) AS n_overview FROM workday__organization_overview
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-084/attempt-01/sql/S3.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-084/attempt-01/sql/S3.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-084/attempt-01/results/S3.rows.jsonl)；完整：True；SHA256：`0093c59ae19ff353e64345cc1a7e6b5d32ba2e7a8bcd5ddd9863d208f4e46142`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "workday__organization_overview", "kind": "base", "block": null, "base_tables": ["workday__organization_overview"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |


## S4

类别 `data`；来源 `query_db`；调用 `ce035a6db1c84f5ebfb985b110f38944`；状态 `success`。

```sql
SELECT COUNT(*) AS n_perf FROM workday__organization_performance
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-084/attempt-01/sql/S4.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-084/attempt-01/sql/S4.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-084/attempt-01/results/S4.rows.jsonl)；完整：True；SHA256：`0093c59ae19ff353e64345cc1a7e6b5d32ba2e7a8bcd5ddd9863d208f4e46142`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "workday__organization_performance", "kind": "base", "block": null, "base_tables": ["workday__organization_performance"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |


## S5

类别 `data`；来源 `query_db`；调用 `7d8a5afea883495cac3daf604bf81e5f`；状态 `success`。

```sql
SELECT * FROM workday__organization_overview LIMIT 5
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-084/attempt-01/sql/S5.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-084/attempt-01/sql/S5.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-084/attempt-01/results/S5.rows.jsonl)；完整：True；SHA256：`99d65a208f4e71ba292a06b1189c5e2490e85c4243eb9d755b31e865328f2434`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "workday__organization_overview", "kind": "base", "block": null, "base_tables": ["workday__organization_overview"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |


## S6

类别 `data`；来源 `query_db`；调用 `edf0a48e1d424ab5a72f5654defd5bf7`；状态 `success`。

```sql
SELECT * FROM workday__organization_performance LIMIT 5
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-084/attempt-01/sql/S6.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-084/attempt-01/sql/S6.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-084/attempt-01/results/S6.rows.jsonl)；完整：True；SHA256：`fa6b04b34ab39d9578fc7fc4f8eb2d97848114a7c477ea4dd021147756cba360`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "workday__organization_performance", "kind": "base", "block": null, "base_tables": ["workday__organization_performance"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |


## S7

类别 `data`；来源 `query_db`；调用 `9739b58ebac549a8843b26aaedc9f4a3`；状态 `success`。

```sql
SELECT data_quality_flag, COUNT(*) n FROM workday__organization_overview GROUP BY data_quality_flag
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-084/attempt-01/sql/S7.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-084/attempt-01/sql/S7.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-084/attempt-01/results/S7.rows.jsonl)；完整：True；SHA256：`082725fe92ef75e2977b8ab532c9a1ad7c77e0772ce31fd7c618ef0d12010733`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "workday__organization_overview", "kind": "base", "block": null, "base_tables": ["workday__organization_overview"]}] | [] | ["data_quality_flag"] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |


## S8

类别 `data`；来源 `query_db`；调用 `8a65edceffbc45e0a7da88546ae7b753`；状态 `success`。

```sql
SELECT performance_category, COUNT(*) n, AVG(organization_health_score) avg_health, MIN(organization_health_score) min_h, MAX(organization_health_score) max_h FROM workday__organization_overview GROUP BY performance_category ORDER BY n DESC
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-084/attempt-01/sql/S8.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-084/attempt-01/sql/S8.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-084/attempt-01/results/S8.rows.jsonl)；完整：True；SHA256：`bdba6955ce7be4a3d60ed4fa867ca739ca56645b0dc04aaa9f8c2f36a09f28c4`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "workday__organization_overview", "kind": "base", "block": null, "base_tables": ["workday__organization_overview"]}] | [] | ["performance_category"] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |
| B1 | AVG(organization_health_score) | [{"table": "workday__organization_overview", "column": "organization_health_score"}] | [] | False |
| B1 | MIN(organization_health_score) | [{"table": "workday__organization_overview", "column": "organization_health_score"}] | [] | False |
| B1 | MAX(organization_health_score) | [{"table": "workday__organization_overview", "column": "organization_health_score"}] | [] | False |


## S9

类别 `data`；来源 `query_db`；调用 `a96deeaaa0cc48e681d47a1486d71005`；状态 `success`。

```sql
SELECT organization_size_category, COUNT(*) n FROM workday__organization_overview GROUP BY organization_size_category
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-084/attempt-01/sql/S9.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-084/attempt-01/sql/S9.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-084/attempt-01/results/S9.rows.jsonl)；完整：True；SHA256：`c428952e4325a44f4dc6d40ec5a113b3f4a4fb72a80fdd7fb422d89a2179b2a1`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "workday__organization_overview", "kind": "base", "block": null, "base_tables": ["workday__organization_overview"]}] | [] | ["organization_size_category"] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |


## S10

类别 `data`；来源 `query_db`；调用 `a64dcb32bb31452fb8d1f398ab62d1ba`；状态 `success`。

```sql
SELECT current_active_employees, organization_size_category FROM workday__organization_overview ORDER BY current_active_employees LIMIT 20
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-084/attempt-01/sql/S10.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-084/attempt-01/sql/S10.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-084/attempt-01/results/S10.rows.jsonl)；完整：True；SHA256：`379eb5b4dbecb4869cb9e274285e504f22251298f742cb155ffb981070227b74`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "workday__organization_overview", "kind": "base", "block": null, "base_tables": ["workday__organization_overview"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |


## S11

类别 `data`；来源 `query_db`；调用 `1255035eca2b4927844fc9fba61c4857`；状态 `success`。

```sql
SELECT current_active_employees, organization_size_category FROM workday__organization_overview WHERE current_active_employees BETWEEN 25 AND 35 ORDER BY current_active_employees
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-084/attempt-01/sql/S11.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-084/attempt-01/sql/S11.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-084/attempt-01/results/S11.rows.jsonl)；完整：True；SHA256：`5adf04804d2cc2b9c5823d7ab680a015cfb6116a42d445370bf4670b564cc60f`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "workday__organization_overview", "kind": "base", "block": null, "base_tables": ["workday__organization_overview"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |


## S12

类别 `data`；来源 `query_db`；调用 `1bd1b5d303744e748d94c701528ebbea`；状态 `success`。

```sql
SELECT current_active_employees, organization_size_category FROM workday__organization_overview WHERE current_active_employees IN (30, 120, 121, 299, 300, 301) ORDER BY current_active_employees
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-084/attempt-01/sql/S12.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-084/attempt-01/sql/S12.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-084/attempt-01/results/S12.rows.jsonl)；完整：True；SHA256：`e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "workday__organization_overview", "kind": "base", "block": null, "base_tables": ["workday__organization_overview"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |


## S13

类别 `data`；来源 `query_db`；调用 `790d466d4a1d4d37a974fe01f3b8ea36`；状态 `success`。

```sql
SELECT 
  CASE WHEN current_active_employees < 30 THEN 'Small (<30)'
       WHEN current_active_employees BETWEEN 30 AND 120 THEN 'Medium (30-120)'
       WHEN current_active_employees BETWEEN 121 AND 300 THEN 'Large (120-300)'
       ELSE 'Extra Large (>300)' END AS my_tier,
  organization_size_category AS existing_tier,
  COUNT(*) n
FROM workday__organization_overview
GROUP BY my_tier, existing_tier
ORDER BY my_tier
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-084/attempt-01/sql/S13.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-084/attempt-01/sql/S13.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-084/attempt-01/results/S13.rows.jsonl)；完整：True；SHA256：`da99d6565b9e7780d8c392d3f3ef90c65ed67d2597b71a7d673f194716038b1b`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "workday__organization_overview", "kind": "base", "block": null, "base_tables": ["workday__organization_overview"]}] | [] | ["CASE WHEN current_active_employees < 30 THEN 'Small (<30)' WHEN current_active_employees BETWEEN 30 AND 120 THEN 'Medium (30-120)' WHEN current_active_employees BETWEEN 121 AND 300 THEN 'Large (120-300)' ELSE 'Extra Large (>300)' END", "organization_size_category"] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |


## S14

类别 `data`；来源 `query_db`；调用 `d0393c30733544898c5fe75187a75376`；状态 `success`。

```sql
SELECT 
  organization_size_category,
  COUNT(*) n_orgs,
  AVG(organization_health_score) avg_health,
  MIN(organization_health_score) min_health,
  MAX(organization_health_score) max_health,
  AVG(management_ratio) avg_mgmt_ratio,
  MIN(management_ratio) min_mgmt_ratio,
  MAX(management_ratio) max_mgmt_ratio,
  AVG(avg_employee_performance_score) avg_perf_score,
  AVG(position_fill_rate) avg_fill_rate,
  AVG(annual_turnover_rate) avg_turnover,
  AVG(current_active_employees) avg_emp_count
FROM workday__organization_overview
GROUP BY organization_size_category
ORDER BY 
  CASE organization_size_category
    WHEN 'Small (0-30)' THEN 1
    WHEN 'Medium (30-120)' THEN 2
    WHEN 'Large (120-300)' THEN 3
    WHEN 'Extra Large (300+)' THEN 4
  END
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-084/attempt-01/sql/S14.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-084/attempt-01/sql/S14.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-084/attempt-01/results/S14.rows.jsonl)；完整：True；SHA256：`0fd383d78065034eb2fc561a2292668661f2ef1b94e1a04cd40aed550ebe5268`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "workday__organization_overview", "kind": "base", "block": null, "base_tables": ["workday__organization_overview"]}] | [] | ["organization_size_category"] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |
| B1 | AVG(organization_health_score) | [{"table": "workday__organization_overview", "column": "organization_health_score"}] | [] | False |
| B1 | MIN(organization_health_score) | [{"table": "workday__organization_overview", "column": "organization_health_score"}] | [] | False |
| B1 | MAX(organization_health_score) | [{"table": "workday__organization_overview", "column": "organization_health_score"}] | [] | False |
| B1 | AVG(management_ratio) | [{"table": "workday__organization_overview", "column": "management_ratio"}] | [] | False |
| B1 | MIN(management_ratio) | [{"table": "workday__organization_overview", "column": "management_ratio"}] | [] | False |
| B1 | MAX(management_ratio) | [{"table": "workday__organization_overview", "column": "management_ratio"}] | [] | False |
| B1 | AVG(avg_employee_performance_score) | [{"table": "workday__organization_overview", "column": "avg_employee_performance_score"}] | [] | False |
| B1 | AVG(position_fill_rate) | [{"table": "workday__organization_overview", "column": "position_fill_rate"}] | [] | False |
| B1 | AVG(annual_turnover_rate) | [{"table": "workday__organization_overview", "column": "annual_turnover_rate"}] | [] | False |
| B1 | AVG(current_active_employees) | [{"table": "workday__organization_overview", "column": "current_active_employees"}] | [] | False |


## S15

类别 `data`；来源 `query_db`；调用 `e228fe5551d049a5b35a5f05049c9b26`；状态 `success`。

```sql
SELECT 
  organization_size_category,
  performance_category,
  COUNT(*) n,
  ROUND(100.0 * COUNT(*) / SUM(COUNT(*)) OVER (PARTITION BY organization_size_category), 1) AS pct
FROM workday__organization_overview
GROUP BY organization_size_category, performance_category
ORDER BY organization_size_category, performance_category
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-084/attempt-01/sql/S15.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-084/attempt-01/sql/S15.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-084/attempt-01/results/S15.rows.jsonl)；完整：True；SHA256：`e15259d85fbee019f08f7cc5c79cbeb71bc74a0ee2aaee5405d5a792edfa5dc0`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "workday__organization_overview", "kind": "base", "block": null, "base_tables": ["workday__organization_overview"]}] | [] | ["organization_size_category", "performance_category"] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |
| B1 | COUNT(*) | [] | [] | True |
| B1 | COUNT(*) | [] | [] | True |


## S16

类别 `data`；来源 `query_db`；调用 `651c39c911894c088435059348fde70a`；状态 `success`。

```sql
SELECT 
  COUNT(*) total,
  SUM(CASE WHEN span_of_control IS NOT NULL THEN 1 ELSE 0 END) n_span,
  SUM(CASE WHEN talent_density_ratio IS NOT NULL THEN 1 ELSE 0 END) n_tdr,
  SUM(CASE WHEN high_value_retention_rate IS NOT NULL THEN 1 ELSE 0 END) n_hvrr,
  SUM(CASE WHEN talent_flight_risk_rate IS NOT NULL THEN 1 ELSE 0 END) n_tfrr,
  SUM(CASE WHEN high_achiever_percentage IS NOT NULL THEN 1 ELSE 0 END) n_hap,
  SUM(CASE WHEN avg_employee_satisfaction_proxy IS NOT NULL THEN 1 ELSE 0 END) n_sat
FROM workday__organization_performance
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-084/attempt-01/sql/S16.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-084/attempt-01/sql/S16.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-084/attempt-01/results/S16.rows.jsonl)；完整：True；SHA256：`6852eb89073b896b4ee4118934ce310b0f74bdfa6170b5e47d35a3feeb3306fb`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "workday__organization_performance", "kind": "base", "block": null, "base_tables": ["workday__organization_performance"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |
| B1 | SUM(CASE WHEN NOT span_of_control IS NULL THEN 1 ELSE 0 END) | [] | [{"table": "workday__organization_performance", "column": "span_of_control"}] | False |
| B1 | SUM(CASE WHEN NOT talent_density_ratio IS NULL THEN 1 ELSE 0 END) | [] | [{"table": "workday__organization_performance", "column": "talent_density_ratio"}] | False |
| B1 | SUM(CASE WHEN NOT high_value_retention_rate IS NULL THEN 1 ELSE 0 END) | [] | [{"table": "workday__organization_performance", "column": "high_value_retention_rate"}] | False |
| B1 | SUM(CASE WHEN NOT talent_flight_risk_rate IS NULL THEN 1 ELSE 0 END) | [] | [{"table": "workday__organization_performance", "column": "talent_flight_risk_rate"}] | False |
| B1 | SUM(CASE WHEN NOT high_achiever_percentage IS NULL THEN 1 ELSE 0 END) | [] | [{"table": "workday__organization_performance", "column": "high_achiever_percentage"}] | False |
| B1 | SUM(CASE WHEN NOT avg_employee_satisfaction_proxy IS NULL THEN 1 ELSE 0 END) | [] | [{"table": "workday__organization_performance", "column": "avg_employee_satisfaction_proxy"}] | False |


## S17

类别 `data`；来源 `query_db`；调用 `a5259ac16f6e48a38fe3077bf3833cab`；状态 `failed`。

```sql
SELECT organization_size_category,
  ROUND(MIN(organization_health_score),1) min_h,
  ROUND(MAX(organization_health_score),1) max_h,
  ROUND(AVG(organization_health_score),1) mean_h,
  ROUND(MEDIAN(organization_health_score),1) median_h,
  ROUND(STDDEV(organization_health_score),1) sd_h
FROM workday__organization_overview
GROUP BY organization_size_category
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-084/attempt-01/sql/S17.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-084/attempt-01/sql/S17.parameters.json)。

错误：`OperationalError('no such function: MEDIAN')`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "workday__organization_overview", "kind": "base", "block": null, "base_tables": ["workday__organization_overview"]}] | [] | ["organization_size_category"] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | MIN(organization_health_score) | [{"table": "workday__organization_overview", "column": "organization_health_score"}] | [] | False |
| B1 | MAX(organization_health_score) | [{"table": "workday__organization_overview", "column": "organization_health_score"}] | [] | False |
| B1 | AVG(organization_health_score) | [{"table": "workday__organization_overview", "column": "organization_health_score"}] | [] | False |
| B1 | PERCENTILE_CONT(organization_health_score, 0.5) | [{"table": "workday__organization_overview", "column": "organization_health_score"}] | [] | False |
| B1 | STDDEV(organization_health_score) | [{"table": "workday__organization_overview", "column": "organization_health_score"}] | [] | False |


## S18

类别 `data`；来源 `query_db`；调用 `d153f25938a6420da5d092d60a187dbc`；状态 `success`。

```sql
WITH t AS (
  SELECT organization_id, organization_size_category, organization_health_score,
    COUNT(*) OVER (PARTITION BY organization_size_category) AS tier_n
  FROM workday__organization_overview
)
SELECT organization_size_category, tier_n,
  ROUND(AVG(organization_health_score),1) mean_h,
  ROUND(MIN(organization_health_score),1) min_h,
  ROUND(MAX(organization_health_score),1) max_h,
  ROUND(AVG(CASE WHEN organization_health_score <= (SELECT MIN(organization_health_score) FROM workday__organization_overview o2 WHERE o2.organization_size_category=t.organization_size_category) THEN organization_health_score END),1) dummy,
  ROUND(AVG(organization_health_score) OVER (),1) overall
FROM t
GROUP BY organization_size_category
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-084/attempt-01/sql/S18.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-084/attempt-01/sql/S18.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-084/attempt-01/results/S18.rows.jsonl)；完整：True；SHA256：`01cbaa4a5d17e2f9980c992ae8dcc4aee8ce65acefa81acc8578060d5dc29365`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "workday__organization_overview", "kind": "base", "block": null, "base_tables": ["workday__organization_overview"]}] | [] | [] |
| B2 | [{"alias": "o2", "kind": "base", "block": null, "base_tables": ["workday__organization_overview"]}] | [] | [] |
| B3 | [{"alias": "t", "kind": "derived", "block": "B1", "base_tables": ["workday__organization_overview"]}] | [] | ["organization_size_category"] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B2 | MIN(organization_health_score) | [{"table": "workday__organization_overview", "column": "organization_health_score"}] | [] | False |
| B3 | AVG(organization_health_score) | [{"table": "workday__organization_overview", "column": "organization_health_score"}] | [] | False |
| B3 | MIN(organization_health_score) | [{"table": "workday__organization_overview", "column": "organization_health_score"}] | [] | False |
| B3 | MAX(organization_health_score) | [{"table": "workday__organization_overview", "column": "organization_health_score"}] | [] | False |
| B3 | AVG(CASE WHEN organization_health_score <= (SELECT MIN(organization_health_score) FROM workday__organization_overview AS o2 WHERE o2.organization_size_category = t.organization_size_category) THEN organization_health_score END) | [{"table": "workday__organization_overview", "column": "organization_health_score"}] | [{"table": "workday__organization_overview", "column": "organization_health_score"}, {"table": "workday__organization_overview", "column": "organization_health_score"}, {"table": "workday__organization_overview", "column": "organization_size_category"}, {"table": "workday__organization_overview", "column": "organization_size_category"}] | False |


## S19

类别 `data`；来源 `query_db`；调用 `0c12e743a5f44150b1a5f031279dbfc0`；状态 `failed`。

```sql
WITH ranked AS (
  SELECT organization_id, organization_size_category, organization_health_score,
    ROW_NUMBER() OVER (PARTITION BY organization_size_category ORDER BY organization_health_score) rn,
    COUNT(*) OVER (PARTITION BY organization_size_category) n
  FROM workday__organization_overview
)
SELECT organization_size_category,
  ROUND(AVG(organization_health_score),2) AS mean,
  ROUND(AVG(CASE WHEN rn*1.0/n <= 0.25 THEN organization_health_score END),2) AS p25,
  ROUND(AVG(CASE WHEN rn*1.0/n <= 0.5 AND rn*1.0/n > 0.25 THEN organization_health_score END),2) AS p50_approx,
  ROUND(AVG(CASE WHEN rn*1.0/n <= 0.75 AND rn*1.0/n > 0.5 THEN organization_health_score END),2) AS p75_approx,
  ROUND(STDDEV(organization_health_score),2) AS sd
FROM ranked
GROUP BY organization_size_category
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-084/attempt-01/sql/S19.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-084/attempt-01/sql/S19.parameters.json)。

错误：`OperationalError('no such function: STDDEV')`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "workday__organization_overview", "kind": "base", "block": null, "base_tables": ["workday__organization_overview"]}] | [] | [] |
| B2 | [{"alias": "ranked", "kind": "derived", "block": "B1", "base_tables": ["workday__organization_overview"]}] | [] | ["organization_size_category"] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B2 | AVG(organization_health_score) | [{"table": "workday__organization_overview", "column": "organization_health_score"}] | [] | False |
| B2 | AVG(CASE WHEN rn * 1.0 / n <= 0.25 THEN organization_health_score END) | [{"table": "workday__organization_overview", "column": "organization_health_score"}] | [{"table": "workday__organization_overview", "column": "organization_size_category"}, {"table": "workday__organization_overview", "column": "organization_size_category"}, {"table": "workday__organization_overview", "column": "organization_health_score"}] | False |
| B2 | AVG(CASE WHEN rn * 1.0 / n <= 0.5 AND rn * 1.0 / n > 0.25 THEN organization_health_score END) | [{"table": "workday__organization_overview", "column": "organization_health_score"}] | [{"table": "workday__organization_overview", "column": "organization_size_category"}, {"table": "workday__organization_overview", "column": "organization_size_category"}, {"table": "workday__organization_overview", "column": "organization_size_category"}, {"table": "workday__organization_overview", "column": "organization_health_score"}, {"table": "workday__organization_overview", "column": "organization_size_category"}, {"table": "workday__organization_overview", "column": "organization_health_score"}] | False |
| B2 | AVG(CASE WHEN rn * 1.0 / n <= 0.75 AND rn * 1.0 / n > 0.5 THEN organization_health_score END) | [{"table": "workday__organization_overview", "column": "organization_health_score"}] | [{"table": "workday__organization_overview", "column": "organization_size_category"}, {"table": "workday__organization_overview", "column": "organization_size_category"}, {"table": "workday__organization_overview", "column": "organization_size_category"}, {"table": "workday__organization_overview", "column": "organization_health_score"}, {"table": "workday__organization_overview", "column": "organization_size_category"}, {"table": "workday__organization_overview", "column": "organization_health_score"}] | False |
| B2 | STDDEV(organization_health_score) | [{"table": "workday__organization_overview", "column": "organization_health_score"}] | [] | False |


## S20

类别 `data`；来源 `query_db`；调用 `100b118dbabd462caa99e90fe5b32ff1`；状态 `success`。

```sql
SELECT organization_size_category, MIN(management_ratio) mn, MAX(management_ratio) mx,
  ROUND(AVG(management_ratio),3) avg_mr
FROM workday__organization_overview
GROUP BY organization_size_category
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-084/attempt-01/sql/S20.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-084/attempt-01/sql/S20.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-084/attempt-01/results/S20.rows.jsonl)；完整：True；SHA256：`245817afaaecb39005a1ada9e9e0037ed7a5987d2401d542bbf0f6e1919734f3`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "workday__organization_overview", "kind": "base", "block": null, "base_tables": ["workday__organization_overview"]}] | [] | ["organization_size_category"] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | MIN(management_ratio) | [{"table": "workday__organization_overview", "column": "management_ratio"}] | [] | False |
| B1 | MAX(management_ratio) | [{"table": "workday__organization_overview", "column": "management_ratio"}] | [] | False |
| B1 | AVG(management_ratio) | [{"table": "workday__organization_overview", "column": "management_ratio"}] | [] | False |


## S21

类别 `data`；来源 `query_db`；调用 `83f9b5c441f74760b4f17e3ebe4ed485`；状态 `success`。

```sql
SELECT 
  CASE WHEN management_ratio < 0.15 THEN 'A: <0.15'
       WHEN management_ratio < 0.18 THEN 'B: 0.15-0.18'
       WHEN management_ratio < 0.21 THEN 'C: 0.18-0.21'
       WHEN management_ratio < 0.25 THEN 'D: 0.21-0.25'
       ELSE 'E: >=0.25' END AS mr_bin,
  COUNT(*) n,
  ROUND(AVG(organization_health_score),2) avg_health,
  ROUND(AVG(avg_employee_performance_score),3) avg_perf,
  ROUND(AVG(position_fill_rate),3) avg_fill,
  ROUND(AVG(annual_turnover_rate),3) avg_turnover
FROM workday__organization_overview
GROUP BY mr_bin
ORDER BY mr_bin
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-084/attempt-01/sql/S21.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-084/attempt-01/sql/S21.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-084/attempt-01/results/S21.rows.jsonl)；完整：True；SHA256：`e7eb1452762336c7e86788d68ae9d5dd50105be9077fb70d15f6211e92828be2`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "workday__organization_overview", "kind": "base", "block": null, "base_tables": ["workday__organization_overview"]}] | [] | ["CASE WHEN management_ratio < 0.15 THEN 'A: <0.15' WHEN management_ratio < 0.18 THEN 'B: 0.15-0.18' WHEN management_ratio < 0.21 THEN 'C: 0.18-0.21' WHEN management_ratio < 0.25 THEN 'D: 0.21-0.25' ELSE 'E: >=0.25' END"] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |
| B1 | AVG(organization_health_score) | [{"table": "workday__organization_overview", "column": "organization_health_score"}] | [] | False |
| B1 | AVG(avg_employee_performance_score) | [{"table": "workday__organization_overview", "column": "avg_employee_performance_score"}] | [] | False |
| B1 | AVG(position_fill_rate) | [{"table": "workday__organization_overview", "column": "position_fill_rate"}] | [] | False |
| B1 | AVG(annual_turnover_rate) | [{"table": "workday__organization_overview", "column": "annual_turnover_rate"}] | [] | False |


## S22

类别 `data`；来源 `query_db`；调用 `580179a20c064eacbbd637b338cb5483`；状态 `success`。

```sql
SELECT 
  organization_size_category,
  CASE WHEN management_ratio < 0.15 THEN 'A: <0.15'
       WHEN management_ratio < 0.18 THEN 'B: 0.15-0.18'
       WHEN management_ratio < 0.21 THEN 'C: 0.18-0.21'
       WHEN management_ratio < 0.25 THEN 'D: 0.21-0.25'
       ELSE 'E: >=0.25' END AS mr_bin,
  COUNT(*) n,
  ROUND(AVG(organization_health_score),2) avg_health,
  ROUND(AVG(avg_employee_performance_score),3) avg_perf,
  ROUND(AVG(position_fill_rate),3) avg_fill,
  ROUND(AVG(annual_turnover_rate),3) avg_turnover
FROM workday__organization_overview
GROUP BY organization_size_category, mr_bin
ORDER BY organization_size_category, mr_bin
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-084/attempt-01/sql/S22.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-084/attempt-01/sql/S22.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-084/attempt-01/results/S22.rows.jsonl)；完整：True；SHA256：`b6f01d3b01d781ab53cb110e674a1a0e5283ab5b8726c1f452513a3e0a375926`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "workday__organization_overview", "kind": "base", "block": null, "base_tables": ["workday__organization_overview"]}] | [] | ["organization_size_category", "CASE WHEN management_ratio < 0.15 THEN 'A: <0.15' WHEN management_ratio < 0.18 THEN 'B: 0.15-0.18' WHEN management_ratio < 0.21 THEN 'C: 0.18-0.21' WHEN management_ratio < 0.25 THEN 'D: 0.21-0.25' ELSE 'E: >=0.25' END"] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |
| B1 | AVG(organization_health_score) | [{"table": "workday__organization_overview", "column": "organization_health_score"}] | [] | False |
| B1 | AVG(avg_employee_performance_score) | [{"table": "workday__organization_overview", "column": "avg_employee_performance_score"}] | [] | False |
| B1 | AVG(position_fill_rate) | [{"table": "workday__organization_overview", "column": "position_fill_rate"}] | [] | False |
| B1 | AVG(annual_turnover_rate) | [{"table": "workday__organization_overview", "column": "annual_turnover_rate"}] | [] | False |


## S23

类别 `data`；来源 `query_db`；调用 `66cb7b79a90b4e19bb1296a8c5eac379`；状态 `success`。

```sql
WITH ranked AS (
  SELECT organization_id, organization_name, organization_size_category,
    current_active_employees, organization_health_score, performance_category,
    management_ratio, avg_employee_performance_score, position_fill_rate, annual_turnover_rate,
    avg_career_development_score, avg_retention_stability_score,
    ROW_NUMBER() OVER (PARTITION BY organization_size_category ORDER BY organization_health_score DESC) rn,
    COUNT(*) OVER (PARTITION BY organization_size_category) n
  FROM workday__organization_overview
)
SELECT organization_size_category, n AS tier_n, CEIL(n*0.1) AS top_k, rn,
  organization_id, organization_name, current_active_employees, organization_health_score,
  performance_category, management_ratio, avg_employee_performance_score, position_fill_rate, annual_turnover_rate
FROM ranked
WHERE rn <= CEIL(n*0.1)
ORDER BY organization_size_category, rn
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-084/attempt-01/sql/S23.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-084/attempt-01/sql/S23.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-084/attempt-01/results/S23.rows.jsonl)；完整：True；SHA256：`dfbf94ae4ce175a2f31bb93c3b4f9e15288edc5946af039cff72dbec641fcf24`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "workday__organization_overview", "kind": "base", "block": null, "base_tables": ["workday__organization_overview"]}] | [] | [] |
| B2 | [{"alias": "ranked", "kind": "derived", "block": "B1", "base_tables": ["workday__organization_overview"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |


## S24

类别 `data`；来源 `query_db`；调用 `e881ade6eae94211b3759f4f0c8c00e4`；状态 `success`。

```sql
WITH ranked AS (
  SELECT *, ROW_NUMBER() OVER (PARTITION BY organization_size_category ORDER BY organization_health_score DESC) rn,
    COUNT(*) OVER (PARTITION BY organization_size_category) n
  FROM workday__organization_overview
)
SELECT organization_size_category, 
  CASE WHEN rn <= CEIL(n*0.1) THEN 'Top10%' ELSE 'Rest' END AS grp,
  COUNT(*) n,
  ROUND(AVG(organization_health_score),1) avg_health,
  ROUND(AVG(management_ratio),3) avg_mr,
  ROUND(AVG(avg_employee_performance_score),3) avg_perf,
  ROUND(AVG(position_fill_rate),3) avg_fill,
  ROUND(AVG(annual_turnover_rate),3) avg_turnover,
  ROUND(AVG(avg_career_development_score),3) avg_dev,
  ROUND(AVG(avg_retention_stability_score),3) avg_ret,
  ROUND(AVG(avg_current_tenure_years),2) avg_tenure,
  ROUND(AVG(organization_age_years),2) avg_age
FROM ranked
GROUP BY organization_size_category, grp
ORDER BY organization_size_category, grp
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-084/attempt-01/sql/S24.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-084/attempt-01/sql/S24.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-084/attempt-01/results/S24.rows.jsonl)；完整：True；SHA256：`6bb79c29ea156262a72dbb3e58996c332f71d2b7a4177616bb8510d2f1a01ebd`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "workday__organization_overview", "kind": "base", "block": null, "base_tables": ["workday__organization_overview"]}] | [] | [] |
| B2 | [{"alias": "ranked", "kind": "derived", "block": "B1", "base_tables": ["workday__organization_overview"]}] | [] | ["organization_size_category", "CASE WHEN rn <= CEIL(n * 0.1) THEN 'Top10%' ELSE 'Rest' END"] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B2 | COUNT(*) | [] | [] | True |
| B2 | AVG(organization_health_score) | [{"table": "workday__organization_overview", "column": "organization_health_score"}] | [] | False |
| B2 | AVG(management_ratio) | [{"table": "workday__organization_overview", "column": "management_ratio"}] | [] | False |
| B2 | AVG(avg_employee_performance_score) | [{"table": "workday__organization_overview", "column": "avg_employee_performance_score"}] | [] | False |
| B2 | AVG(position_fill_rate) | [{"table": "workday__organization_overview", "column": "position_fill_rate"}] | [] | False |
| B2 | AVG(annual_turnover_rate) | [{"table": "workday__organization_overview", "column": "annual_turnover_rate"}] | [] | False |
| B2 | AVG(avg_career_development_score) | [{"table": "workday__organization_overview", "column": "avg_career_development_score"}] | [] | False |
| B2 | AVG(avg_retention_stability_score) | [{"table": "workday__organization_overview", "column": "avg_retention_stability_score"}] | [] | False |
| B2 | AVG(avg_current_tenure_years) | [{"table": "workday__organization_overview", "column": "avg_current_tenure_years"}] | [] | False |
| B2 | AVG(organization_age_years) | [{"table": "workday__organization_overview", "column": "organization_age_years"}] | [] | False |


## S25

类别 `data`；来源 `query_db`；调用 `ff217c2523f34ff9bc0ba4a2abda14bc`；状态 `success`。

```sql
SELECT 
  SUM(CASE WHEN avg_career_development_score > 0 THEN 1 ELSE 0 END) n_dev,
  SUM(CASE WHEN avg_retention_stability_score > 0 THEN 1 ELSE 0 END) n_ret,
  SUM(CASE WHEN avg_current_tenure_years > 0 THEN 1 ELSE 0 END) n_tenure,
  SUM(CASE WHEN high_value_stable_employees > 0 THEN 1 ELSE 0 END) n_hvs,
  SUM(CASE WHEN management_role_employees > 0 THEN 1 ELSE 0 END) n_mgmt,
  SUM(CASE WHEN high_risk_employee_percentage > 0 THEN 1 ELSE 0 END) n_hrp,
  SUM(CASE WHEN total_promotions_in_organization > 0 THEN 1 ELSE 0 END) n_prom,
  SUM(CASE WHEN avg_employee_age > 0 THEN 1 ELSE 0 END) n_age
FROM workday__organization_overview
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-084/attempt-01/sql/S25.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-084/attempt-01/sql/S25.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-084/attempt-01/results/S25.rows.jsonl)；完整：True；SHA256：`7604640d16826af23c822d02ba16dc713101d1852eb92eead17f07f63c7171b6`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "workday__organization_overview", "kind": "base", "block": null, "base_tables": ["workday__organization_overview"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | SUM(CASE WHEN avg_career_development_score > 0 THEN 1 ELSE 0 END) | [] | [{"table": "workday__organization_overview", "column": "avg_career_development_score"}] | False |
| B1 | SUM(CASE WHEN avg_retention_stability_score > 0 THEN 1 ELSE 0 END) | [] | [{"table": "workday__organization_overview", "column": "avg_retention_stability_score"}] | False |
| B1 | SUM(CASE WHEN avg_current_tenure_years > 0 THEN 1 ELSE 0 END) | [] | [{"table": "workday__organization_overview", "column": "avg_current_tenure_years"}] | False |
| B1 | SUM(CASE WHEN high_value_stable_employees > 0 THEN 1 ELSE 0 END) | [] | [{"table": "workday__organization_overview", "column": "high_value_stable_employees"}] | False |
| B1 | SUM(CASE WHEN management_role_employees > 0 THEN 1 ELSE 0 END) | [] | [{"table": "workday__organization_overview", "column": "management_role_employees"}] | False |
| B1 | SUM(CASE WHEN high_risk_employee_percentage > 0 THEN 1 ELSE 0 END) | [] | [{"table": "workday__organization_overview", "column": "high_risk_employee_percentage"}] | False |
| B1 | SUM(CASE WHEN total_promotions_in_organization > 0 THEN 1 ELSE 0 END) | [] | [{"table": "workday__organization_overview", "column": "total_promotions_in_organization"}] | False |
| B1 | SUM(CASE WHEN avg_employee_age > 0 THEN 1 ELSE 0 END) | [] | [{"table": "workday__organization_overview", "column": "avg_employee_age"}] | False |


## S26

类别 `data`；来源 `query_db`；调用 `c17f5fae60bb4577b301d8ae4410da31`；状态 `success`。

```sql
WITH ranked AS (
  SELECT *, ROW_NUMBER() OVER (PARTITION BY organization_size_category ORDER BY organization_health_score DESC) rn,
    COUNT(*) OVER (PARTITION BY organization_size_category) n
  FROM workday__organization_overview
)
SELECT organization_size_category, organization_id, organization_name, current_active_employees,
  organization_health_score, performance_category, management_ratio, avg_employee_performance_score,
  position_fill_rate, annual_turnover_rate, organization_type, staffing_model, organization_maturity_level,
  unique_organization_roles, total_promotions_in_organization
FROM ranked
WHERE rn <= CEIL(n*0.1)
ORDER BY organization_size_category, rn
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-084/attempt-01/sql/S26.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-084/attempt-01/sql/S26.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-084/attempt-01/results/S26.rows.jsonl)；完整：True；SHA256：`c0e43e82ceeb525f3ddf704a759036f97dfe3d0cca2b818ebfac79e54017d09d`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "workday__organization_overview", "kind": "base", "block": null, "base_tables": ["workday__organization_overview"]}] | [] | [] |
| B2 | [{"alias": "ranked", "kind": "derived", "block": "B1", "base_tables": ["workday__organization_overview"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |


## S27

类别 `data`；来源 `python`；调用 `12e7713978a14ff8ba94f0e89ac41520`；状态 `success`。

```sql

SELECT organization_id, organization_size_category, current_active_employees,
       organization_health_score, performance_category, management_ratio,
       avg_employee_performance_score, position_fill_rate, annual_turnover_rate,
       organization_type, staffing_model, organization_maturity_level
FROM workday__organization_overview

```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-084/attempt-01/sql/S27.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-084/attempt-01/sql/S27.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-084/attempt-01/results/S27.rows.jsonl)；完整：True；SHA256：`5344397ad3441c241dc8c107ee0e777eb111f410a69519f5ce6586c576fefdb9`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "workday__organization_overview", "kind": "base", "block": null, "base_tables": ["workday__organization_overview"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |


## S28

类别 `data`；来源 `python`；调用 `12e7713978a14ff8ba94f0e89ac41520`；状态 `success`。

```sql

SELECT organization_id, organization_size_category, current_employee_count,
       avg_employee_satisfaction_proxy, high_achiever_percentage, avg_weekly_hours_per_employee
FROM workday__organization_performance

```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-084/attempt-01/sql/S28.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-084/attempt-01/sql/S28.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-084/attempt-01/results/S28.rows.jsonl)；完整：True；SHA256：`968154d607c8432ef2c436c1ae8ad3e0dffe1fcbf132c47e339ec94c18d3cbf0`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "workday__organization_performance", "kind": "base", "block": null, "base_tables": ["workday__organization_performance"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |


## S29

类别 `data`；来源 `python`；调用 `ba0a6ba85722418f8a99cf1e254d74b8`；状态 `success`。

```sql

SELECT organization_id, organization_size_category, current_active_employees,
       organization_health_score, performance_category, management_ratio,
       avg_employee_performance_score, position_fill_rate, annual_turnover_rate,
       organization_type, staffing_model, organization_maturity_level
FROM workday__organization_overview

```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-084/attempt-01/sql/S29.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-084/attempt-01/sql/S29.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-084/attempt-01/results/S29.rows.jsonl)；完整：True；SHA256：`5344397ad3441c241dc8c107ee0e777eb111f410a69519f5ce6586c576fefdb9`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "workday__organization_overview", "kind": "base", "block": null, "base_tables": ["workday__organization_overview"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |


## S30

类别 `data`；来源 `python`；调用 `ba0a6ba85722418f8a99cf1e254d74b8`；状态 `success`。

```sql

SELECT organization_id, avg_employee_satisfaction_proxy, high_achiever_percentage,
       avg_weekly_hours_per_employee
FROM workday__organization_performance

```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-084/attempt-01/sql/S30.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-084/attempt-01/sql/S30.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-084/attempt-01/results/S30.rows.jsonl)；完整：True；SHA256：`eb7780b21f7979fccafafd61311180f1ffd6cb0a858f9c8becf36f81d4ce6004`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "workday__organization_performance", "kind": "base", "block": null, "base_tables": ["workday__organization_performance"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |


## S31

类别 `data`；来源 `python`；调用 `f3c2a0c687254c6da903eae52f1b1e4e`；状态 `success`。

```sql

SELECT organization_id, organization_size_category, current_active_employees,
       organization_health_score, performance_category, management_ratio,
       avg_employee_performance_score, position_fill_rate, annual_turnover_rate
FROM workday__organization_overview

```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-084/attempt-01/sql/S31.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-084/attempt-01/sql/S31.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-084/attempt-01/results/S31.rows.jsonl)；完整：True；SHA256：`5d99de515736a1c245ea3b35b299a00531ec87f3e2153419db92121b67349ca9`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "workday__organization_overview", "kind": "base", "block": null, "base_tables": ["workday__organization_overview"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |


## S32

类别 `data`；来源 `python`；调用 `d391e6f6525f4d299230469f89678af8`；状态 `success`。

```sql

SELECT organization_id, organization_size_category, current_active_employees,
       organization_health_score, performance_category, management_ratio,
       avg_employee_performance_score, position_fill_rate, annual_turnover_rate,
       organization_type, staffing_model, organization_maturity_level
FROM workday__organization_overview

```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-084/attempt-01/sql/S32.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-084/attempt-01/sql/S32.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-084/attempt-01/results/S32.rows.jsonl)；完整：True；SHA256：`5344397ad3441c241dc8c107ee0e777eb111f410a69519f5ce6586c576fefdb9`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "workday__organization_overview", "kind": "base", "block": null, "base_tables": ["workday__organization_overview"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |


## S33

类别 `data`；来源 `python`；调用 `0443c1a0c01549d8b50c9459b0f424ff`；状态 `success`。

```sql

SELECT organization_id, organization_name, organization_size_category, current_active_employees,
       organization_health_score, performance_category, management_ratio,
       avg_employee_performance_score, position_fill_rate, annual_turnover_rate,
       organization_type, staffing_model, organization_maturity_level
FROM workday__organization_overview

```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-084/attempt-01/sql/S33.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-084/attempt-01/sql/S33.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-084/attempt-01/results/S33.rows.jsonl)；完整：True；SHA256：`d70d7a81f10348206425d45119b660acc31b3183d8c99581ff907acd554c5845`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "workday__organization_overview", "kind": "base", "block": null, "base_tables": ["workday__organization_overview"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |


## S34

类别 `data`；来源 `python`；调用 `6af2b9beb0954a979cef8e0e7259dbb5`；状态 `success`。

```sql

SELECT organization_id, organization_size_category, current_active_employees,
       organization_health_score, performance_category, management_ratio,
       avg_employee_performance_score, position_fill_rate, annual_turnover_rate
FROM workday__organization_overview

```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-084/attempt-01/sql/S34.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-084/attempt-01/sql/S34.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-084/attempt-01/results/S34.rows.jsonl)；完整：True；SHA256：`5d99de515736a1c245ea3b35b299a00531ec87f3e2153419db92121b67349ca9`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "workday__organization_overview", "kind": "base", "block": null, "base_tables": ["workday__organization_overview"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |


## S35

类别 `data`；来源 `python`；调用 `092fe3d49fce44c6a5db04db70df53e2`；状态 `success`。

```sql

SELECT organization_id, organization_size_category, organization_health_score,
       position_fill_rate, annual_turnover_rate, avg_employee_performance_score
FROM workday__organization_overview

```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-084/attempt-01/sql/S35.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-084/attempt-01/sql/S35.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-084/attempt-01/results/S35.rows.jsonl)；完整：True；SHA256：`d55a7dba0b69b212bc1b200ac5226bd7d162a3c10df2428b5cd35afaf7735ad7`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "workday__organization_overview", "kind": "base", "block": null, "base_tables": ["workday__organization_overview"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |


## S36

类别 `data`；来源 `python`；调用 `7425544da45b47b9a3bc6c221c87dea5`；状态 `success`。

```sql

SELECT organization_id, organization_size_category, current_active_employees,
       organization_health_score, performance_category, management_ratio,
       avg_employee_performance_score, position_fill_rate, annual_turnover_rate
FROM workday__organization_overview

```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-084/attempt-01/sql/S36.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-084/attempt-01/sql/S36.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-084/attempt-01/results/S36.rows.jsonl)；完整：True；SHA256：`5d99de515736a1c245ea3b35b299a00531ec87f3e2153419db92121b67349ca9`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "workday__organization_overview", "kind": "base", "block": null, "base_tables": ["workday__organization_overview"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |

