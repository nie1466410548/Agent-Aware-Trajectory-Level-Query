# dacomp-041

Please, for Exhibition Halls with an average Daily Visitor Count exceeding 900, conduct a …

运行：已提交。官方未评分。全部 SQL 尝试/成功 37/33；数据 SQL 35/31；Python 23 次。

完整原题：

Please, for Exhibition Halls with an average Daily Visitor Count exceeding 900, conduct a comprehensive analysis of air quality, temperature and humidity, and light and radiation data, and, combined with the exhibited cultural relics’ ratings and condition, evaluate the core preservation risks faced by cultural relics in these high-traffic environments, and accordingly propose specific, prioritized conservation and maintenance measures.

| 表 | 行数 | 列数 |
| --- | --- | --- |
| air_quality_readings | 951 | 12 |
| artifact_conservation_and_maint | 951 | 20 |
| artifact_rating | 951 | 12 |
| artifact_security_and_access | 951 | 13 |
| basic_artifact_information | 951 | 6 |
| condition_assessment | 951 | 7 |
| display_case_information | 951 | 17 |
| environmental_monitoring_data | 951 | 9 |
| gallery_information | 951 | 9 |
| light_and_radiation_readings | 951 | 6 |
| risk_assessment | 951 | 8 |
| sensitivity_data | 951 | 13 |
| surface_and_physical_readings | 951 | 27 |
| usage_records | 951 | 26 |


实际路线（分析者依据 SQL/源码概括，不代表 Agent 自述）：SQL 筛选高客流展厅并提取环境与文物信息 → 宽表计数查询超时 → Python 合并、阈值计数和风险比较 → 绘图。

数据库大小：3,514,368 字节。

## 数据 SQL

| SQL | 状态 | 基础表 | Join 输入/类型 | GROUP BY | 聚合表达式 | 结果行数 | 数据库 ms |
| --- | --- | --- | --- | --- | --- | --- | --- |
| [S3/Q1](#s3) | success | ["gallery_information"] | 0 / {} | [] | [] | 951 | 1.609 |
| [S4/Q2](#s4) | success | ["gallery_information"] | 0 / {} | [] | [] | 104 | 0.588 |
| [S5/Q3](#s5) | success | ["gallery_information"] | 0 / {} | [] | ["COUNT(*)", "AVG(\"Daily Visitor Count\")", "MAX(\"Daily Visitor Count\")", "MIN(\"Daily Visitor Count\")"] | 1 | 0.57 |
| [S6/Q4](#s6) | success | ["display_case_information"] | 0 / {} | [] | [] | 20 | 0.419 |
| [S7/Q5](#s7) | success | ["environmental_monitoring_data"] | 0 / {} | [] | [] | 20 | 0.356 |
| [S8/Q6](#s8) | success | ["artifact_conservation_and_maint"] | 0 / {} | [] | [] | 20 | 0.375 |
| [S9/Q7](#s9) | success | ["display_case_information"] | 0 / {} | [] | ["COUNT(*)", "COUNT(DISTINCT \"Display case ID\")", "COUNT(DISTINCT \"Gallery reference\")"] | 1 | 1.585 |
| [S10/Q8](#s10) | success | ["display_case_information", "environmental_monitoring_data"] | 2 / {'LEFT': 1} | [] | [] | 0 | 180.441 |
| [S11/Q9](#s11) | success | ["environmental_monitoring_data"] | 0 / {} | [] | ["COUNT(*)", "COUNT(DISTINCT \"Environmental Reading ID\")", "COUNT(DISTINCT \"Display Case Reference\")"] | 1 | 1.092 |
| [S12/Q10](#s12) | success | ["air_quality_readings", "environmental_monitoring_data"] | 2 / {'LEFT': 1} | [] | [] | 0 | 0.936 |
| [S13/Q11](#s13) | success | ["air_quality_readings"] | 0 / {} | [] | ["COUNT(*)", "COUNT(DISTINCT \"Environmental monitoring reference\")"] | 1 | 0.514 |
| [S14/Q12](#s14) | success | ["artifact_conservation_and_maint"] | 0 / {} | [] | ["COUNT(*)", "COUNT(DISTINCT \"Preserve Cultural Relic Reference\")", "COUNT(DISTINCT \"Gallery Reference\")"] | 1 | 1.566 |
| [S15/Q13](#s15) | success | ["artifact_rating"] | 0 / {} | [] | ["COUNT(*)", "COUNT(DISTINCT \"Cultural Relic Reference Number\")"] | 1 | 0.891 |
| [S16/Q14](#s16) | success | ["basic_artifact_information"] | 0 / {} | [] | ["COUNT(*)", "COUNT(DISTINCT \"Cultural Relic Registration Number\")"] | 1 | 0.951 |
| [S17/Q15](#s17) | success | ["sensitivity_data"] | 0 / {} | [] | ["COUNT(*)", "COUNT(DISTINCT \"Cultural Relic Reference Number\")"] | 1 | 0.938 |
| [S18/Q16](#s18) | success | ["condition_assessment"] | 0 / {} | [] | ["COUNT(*)", "COUNT(DISTINCT \"Inspected Cultural Relic Reference\")", "COUNT(DISTINCT \"Inspected Display Case Reference\")"] | 1 | 1.38 |
| [S19/Q17](#s19) | success | ["display_case_information", "gallery_information"] | 2 / {'LEFT': 1} | [] | [] | 0 | 128.779 |
| [S20/Q18](#s20) | success | ["artifact_conservation_and_maint", "artifact_rating"] | 2 / {'LEFT': 1} | [] | [] | 0 | 157.012 |
| [S21/Q19](#s21) | cancelled | ["air_quality_readings", "artifact_conservation_and_maint", "artifact_rating", "basic_artifact_information", "condition_assessment", "display_case_information", "environmental_monitoring_data", "gallery_information", "light_and_radiation_readings", "sensitivity_data", "surface_and_physical_readings"] | 11 / {'INNER': 10} | [] | ["COUNT(*)"] | unknown | 未取得；调用总时长 300000.436 ms |
| [S22/Q20](#s22) | success | ["gallery_information"] | 0 / {} | [] | [] | 104 | 0.509 |
| [S23/Q21](#s23) | failed | ["air_quality_readings", "display_case_information", "environmental_monitoring_data", "gallery_information", "light_and_radiation_readings", "surface_and_physical_readings"] | 6 / {'INNER': 5} | [] | [] | unknown | 未取得；调用总时长 0.225 ms |
| [S24/Q22](#s24) | success | ["light_and_radiation_readings"] | 0 / {} | [] | [] | 1 | 0.323 |
| [S25/Q23](#s25) | success | ["surface_and_physical_readings"] | 0 / {} | [] | [] | 1 | 0.367 |
| [S26/Q24](#s26) | failed | ["air_quality_readings", "display_case_information", "environmental_monitoring_data", "gallery_information", "light_and_radiation_readings", "surface_and_physical_readings"] | 6 / {'INNER': 5} | [] | [] | unknown | 未取得；调用总时长 0.228 ms |
| [S27/Q25](#s27) | failed | unknown | None / None | [] | [] | unknown | 未取得；调用总时长 0.127 ms |
| [S28/Q26](#s28) | success | ["light_and_radiation_readings"] | 0 / {} | [] | [] | 1 | 0.241 |
| [S29/Q27](#s29) | success | ["surface_and_physical_readings"] | 0 / {} | [] | [] | 1 | 0.218 |
| [S30/Q28](#s30) | success | ["air_quality_readings", "display_case_information", "environmental_monitoring_data", "gallery_information", "light_and_radiation_readings", "surface_and_physical_readings"] | 6 / {'INNER': 5} | [] | [] | 104 | 37.795 |
| [S31/Q29](#s31) | success | ["artifact_conservation_and_maint", "artifact_rating", "artifact_security_and_access", "basic_artifact_information", "condition_assessment", "gallery_information", "sensitivity_data"] | 7 / {'INNER': 6} | [] | [] | 104 | 96.915 |
| [S32/Q30](#s32) | success | ["display_case_information", "gallery_information"] | 2 / {'INNER': 1} | [] | [] | 104 | 15.335 |
| [S33/Q31](#s33) | success | ["display_case_information", "environmental_monitoring_data", "gallery_information"] | 3 / {'INNER': 2} | [] | [] | 951 | 309.795 |
| [S34/Q32](#s34) | success | ["air_quality_readings", "display_case_information", "environmental_monitoring_data", "gallery_information", "light_and_radiation_readings", "surface_and_physical_readings"] | 6 / {'INNER': 5} | [] | [] | 951 | 323.201 |
| [S35/Q33](#s35) | success | ["artifact_conservation_and_maint", "artifact_rating", "artifact_security_and_access", "basic_artifact_information", "condition_assessment", "gallery_information", "sensitivity_data"] | 7 / {'INNER': 6} | [] | [] | 951 | 880.489 |
| [S36/Q34](#s36) | success | ["gallery_information", "risk_assessment"] | 2 / {'INNER': 1} | [] | [] | 104 | 14.775 |
| [S37/Q35](#s37) | success | ["artifact_conservation_and_maint", "gallery_information", "usage_records"] | 3 / {'INNER': 2} | [] | [] | 104 | 16054.461 |


## 元数据和设置

| SQL | 类别 | 状态 | 内容 |
| --- | --- | --- | --- |
| S1 | connection_setup | success | PRAGMA query_only=ON |
| S2 | metadata | success | SELECT name,sql FROM sqlite_master WHERE type='table' ORDER BY name |


## Python 与执行位置

人工源码审查：**database_first_violation**。Python 多次合并展厅环境、文物、展柜及风险明细，并计算条件计数、分组均值和风险指标，属于可在数据库内完成的工作。绘图及额外统计应单独评价。 [证据](../reviews/dacomp-041.json)。

P1：Use Python to inspect the actual column names of light_and_radiation_readings and surface_and_physical_readings tables, since they contain special characters (non-breaking spaces) that make SQL querying difficult.

[源码](../../../runs/dsv4flash-db-first-full-01/dacomp-041/attempt-01/python/P1.py)；[输出](../../../runs/dsv4flash-db-first-full-01/dacomp-041/attempt-01/python/P1.stdout)；[错误](../../../runs/dsv4flash-db-first-full-01/dacomp-041/attempt-01/python/P1.stderr)。检出需人工核验的 SQL 可实现操作：.query(；不能仅凭理由判为合规。

P2：Build the master environmental dataset for high-traffic halls (>900 visitors/day) via SQL join across gallery, display case, environmental monitoring, air quality, light/radiation and surface/physical readings. Using Python to embed the exact non-breaking-space column names from light and surface tables which are difficult to type directly in the SQL tool.

[源码](../../../runs/dsv4flash-db-first-full-01/dacomp-041/attempt-01/python/P2.py)；[输出](../../../runs/dsv4flash-db-first-full-01/dacomp-041/attempt-01/python/P2.stdout)；[错误](../../../runs/dsv4flash-db-first-full-01/dacomp-041/attempt-01/python/P2.stderr)。检出需人工核验的 SQL 可实现操作：.query(；不能仅凭理由判为合规。

P3：Retrieve artifact rating, condition, sensitivity, and conservation data for relics in high-traffic halls (>900 visitors/day) via SQL joins. This artifact data is needed to evaluate preservation risks alongside environmental data.

[源码](../../../runs/dsv4flash-db-first-full-01/dacomp-041/attempt-01/python/P3.py)；[输出](../../../runs/dsv4flash-db-first-full-01/dacomp-041/attempt-01/python/P3.stdout)；[错误](../../../runs/dsv4flash-db-first-full-01/dacomp-041/attempt-01/python/P3.stderr)。检出需人工核验的 SQL 可实现操作：.query(；不能仅凭理由判为合规。

P4：Retrieve display case and gallery management data for high-traffic halls and confirm overall population row counts for comparative statistics.

[源码](../../../runs/dsv4flash-db-first-full-01/dacomp-041/attempt-01/python/P4.py)；[输出](../../../runs/dsv4flash-db-first-full-01/dacomp-041/attempt-01/python/P4.stdout)；[错误](../../../runs/dsv4flash-db-first-full-01/dacomp-041/attempt-01/python/P4.stderr)。检出需人工核验的 SQL 可实现操作：.query(；不能仅凭理由判为合规。

P5：Retrieve full population dataset (all 951 halls) for comparative statistics between high-traffic and low-traffic environments.

[源码](../../../runs/dsv4flash-db-first-full-01/dacomp-041/attempt-01/python/P5.py)；[输出](../../../runs/dsv4flash-db-first-full-01/dacomp-041/attempt-01/python/P5.stdout)；[错误](../../../runs/dsv4flash-db-first-full-01/dacomp-041/attempt-01/python/P5.stderr)。检出需人工核验的 SQL 可实现操作：.query(；不能仅凭理由判为合规。

P6：Compute comparative statistics between high-traffic and low-traffic halls for all environmental parameters, to identify which factors are most affected by high visitor traffic.

[源码](../../../runs/dsv4flash-db-first-full-01/dacomp-041/attempt-01/python/P6.py)；[输出](../../../runs/dsv4flash-db-first-full-01/dacomp-041/attempt-01/python/P6.stdout)；[错误](../../../runs/dsv4flash-db-first-full-01/dacomp-041/attempt-01/python/P6.stderr)。检出需人工核验的 SQL 可实现操作：.merge(；不能仅凭理由判为合规。

P7：Analyze artifact ratings, material types, preservation status, conservation difficulty, sensitivity, and treatment data to compare high-traffic vs low-traffic environments.

[源码](../../../runs/dsv4flash-db-first-full-01/dacomp-041/attempt-01/python/P7.py)；[输出](../../../runs/dsv4flash-db-first-full-01/dacomp-041/attempt-01/python/P7.stdout)；[错误](../../../runs/dsv4flash-db-first-full-01/dacomp-041/attempt-01/python/P7.stderr)。自动源码筛查未检出预设迁出信号；这不是全面语义合规证明。

P8：Merge all high-traffic data and analyze threshold exceedances and correlations between visitor count and environmental parameters to identify the specific preservation risks.

[源码](../../../runs/dsv4flash-db-first-full-01/dacomp-041/attempt-01/python/P8.py)；[输出](../../../runs/dsv4flash-db-first-full-01/dacomp-041/attempt-01/python/P8.stdout)；[错误](../../../runs/dsv4flash-db-first-full-01/dacomp-041/attempt-01/python/P8.stderr)。检出需人工核验的 SQL 可实现操作：.merge(；不能仅凭理由判为合规。

P9：Analyze display case conditions, compare threshold exceedances between high and low traffic, and cross-reference artifact material types with sensitivities and environmental conditions.

[源码](../../../runs/dsv4flash-db-first-full-01/dacomp-041/attempt-01/python/P9.py)；[输出](../../../runs/dsv4flash-db-first-full-01/dacomp-041/attempt-01/python/P9.stdout)；[错误](../../../runs/dsv4flash-db-first-full-01/dacomp-041/attempt-01/python/P9.stderr)。自动源码筛查未检出预设迁出信号；这不是全面语义合规证明。

P10：Analyze display case conditions, threshold exceedance comparisons, artifact sensitivities, and cross-reference material types with deterioration rates and conservation priorities.

[源码](../../../runs/dsv4flash-db-first-full-01/dacomp-041/attempt-01/python/P10.py)；[输出](../../../runs/dsv4flash-db-first-full-01/dacomp-041/attempt-01/python/P10.stdout)；[错误](../../../runs/dsv4flash-db-first-full-01/dacomp-041/attempt-01/python/P10.stderr)。自动源码筛查未检出预设迁出信号；这不是全面语义合规证明。

P11：Check merged dataframe column names to find the correct treatment priority column.

[源码](../../../runs/dsv4flash-db-first-full-01/dacomp-041/attempt-01/python/P11.py)；[输出](../../../runs/dsv4flash-db-first-full-01/dacomp-041/attempt-01/python/P11.stdout)；[错误](../../../runs/dsv4flash-db-first-full-01/dacomp-041/attempt-01/python/P11.stderr)。自动源码筛查未检出预设迁出信号；这不是全面语义合规证明。

P12：Inspect treatment priority and material type values in merged data to verify the cross-tabulation.

[源码](../../../runs/dsv4flash-db-first-full-01/dacomp-041/attempt-01/python/P12.py)；[输出](../../../runs/dsv4flash-db-first-full-01/dacomp-041/attempt-01/python/P12.stdout)；[错误](../../../runs/dsv4flash-db-first-full-01/dacomp-041/attempt-01/python/P12.stderr)。自动源码筛查未检出预设迁出信号；这不是全面语义合规证明。

P13：Create visualizations for the comprehensive analysis: environmental parameter comparison, correlation heatmap, condition assessment, material type treatment priority, and display case status.

[源码](../../../runs/dsv4flash-db-first-full-01/dacomp-041/attempt-01/python/P13.py)；[输出](../../../runs/dsv4flash-db-first-full-01/dacomp-041/attempt-01/python/P13.stdout)；[错误](../../../runs/dsv4flash-db-first-full-01/dacomp-041/attempt-01/python/P13.stderr)。自动源码筛查未检出预设迁出信号；这不是全面语义合规证明。

P14：Retrieve and analyze risk assessment data for high-traffic halls, usage records, and compile a comprehensive summary of all risk indicators.

[源码](../../../runs/dsv4flash-db-first-full-01/dacomp-041/attempt-01/python/P14.py)；[输出](../../../runs/dsv4flash-db-first-full-01/dacomp-041/attempt-01/python/P14.stdout)；[错误](../../../runs/dsv4flash-db-first-full-01/dacomp-041/attempt-01/python/P14.stderr)。检出需人工核验的 SQL 可实现操作：.query(；不能仅凭理由判为合规。

P15：Compile the comprehensive summary of all risk indicators for the high-traffic halls and identify the top-risk relics combining condition and treatment priority.

[源码](../../../runs/dsv4flash-db-first-full-01/dacomp-041/attempt-01/python/P15.py)；[输出](../../../runs/dsv4flash-db-first-full-01/dacomp-041/attempt-01/python/P15.stdout)；[错误](../../../runs/dsv4flash-db-first-full-01/dacomp-041/attempt-01/python/P15.stderr)。自动源码筛查未检出预设迁出信号；这不是全面语义合规证明。

P16：Debug the data type and whitespace issues in sensitivity and treatment priority columns.

[源码](../../../runs/dsv4flash-db-first-full-01/dacomp-041/attempt-01/python/P16.py)；[输出](../../../runs/dsv4flash-db-first-full-01/dacomp-041/attempt-01/python/P16.stdout)；[错误](../../../runs/dsv4flash-db-first-full-01/dacomp-041/attempt-01/python/P16.stderr)。自动源码筛查未检出预设迁出信号；这不是全面语义合规证明。

P17：Re-analyze with whitespace-trimmed string columns to get correct counts for risk indicators.

[源码](../../../runs/dsv4flash-db-first-full-01/dacomp-041/attempt-01/python/P17.py)；[输出](../../../runs/dsv4flash-db-first-full-01/dacomp-041/attempt-01/python/P17.stdout)；[错误](../../../runs/dsv4flash-db-first-full-01/dacomp-041/attempt-01/python/P17.stderr)。自动源码筛查未检出预设迁出信号；这不是全面语义合规证明。

P18：Debug the whitespace stripping issue to understand why str.strip() didn't work and fix it properly.

[源码](../../../runs/dsv4flash-db-first-full-01/dacomp-041/attempt-01/python/P18.py)；[输出](../../../runs/dsv4flash-db-first-full-01/dacomp-041/attempt-01/python/P18.stdout)；[错误](../../../runs/dsv4flash-db-first-full-01/dacomp-041/attempt-01/python/P18.stderr)。自动源码筛查未检出预设迁出信号；这不是全面语义合规证明。

P19：Perform the final comprehensive analysis with properly cleaned data, covering all environmental, artifact, display case, and risk assessment dimensions.

[源码](../../../runs/dsv4flash-db-first-full-01/dacomp-041/attempt-01/python/P19.py)；[输出](../../../runs/dsv4flash-db-first-full-01/dacomp-041/attempt-01/python/P19.stdout)；[错误](../../../runs/dsv4flash-db-first-full-01/dacomp-041/attempt-01/python/P19.stderr)。自动源码筛查未检出预设迁出信号；这不是全面语义合规证明。

P20：Check raw string values in display case columns to understand exact padding and verify correct counts.

[源码](../../../runs/dsv4flash-db-first-full-01/dacomp-041/attempt-01/python/P20.py)；[输出](../../../runs/dsv4flash-db-first-full-01/dacomp-041/attempt-01/python/P20.stdout)；[错误](../../../runs/dsv4flash-db-first-full-01/dacomp-041/attempt-01/python/P20.stderr)。自动源码筛查未检出预设迁出信号；这不是全面语义合规证明。

P21：Identify specific top-risk relics and cross-reference formal risk assessment levels with environmental exposures and condition ratings.

[源码](../../../runs/dsv4flash-db-first-full-01/dacomp-041/attempt-01/python/P21.py)；[输出](../../../runs/dsv4flash-db-first-full-01/dacomp-041/attempt-01/python/P21.stdout)；[错误](../../../runs/dsv4flash-db-first-full-01/dacomp-041/attempt-01/python/P21.stderr)。检出需人工核验的 SQL 可实现操作：groupby(, .merge(；不能仅凭理由判为合规。

P22：Debug the persistent whitespace issue in the merged CSV Treatment Priority column.

[源码](../../../runs/dsv4flash-db-first-full-01/dacomp-041/attempt-01/python/P22.py)；[输出](../../../runs/dsv4flash-db-first-full-01/dacomp-041/attempt-01/python/P22.stdout)；[错误](../../../runs/dsv4flash-db-first-full-01/dacomp-041/attempt-01/python/P22.stderr)。自动源码筛查未检出预设迁出信号；这不是全面语义合规证明。

P23：Build the final clean merged dataset with properly stripped values and identify top-risk relics with cross-referenced risk levels.

[源码](../../../runs/dsv4flash-db-first-full-01/dacomp-041/attempt-01/python/P23.py)；[输出](../../../runs/dsv4flash-db-first-full-01/dacomp-041/attempt-01/python/P23.stdout)；[错误](../../../runs/dsv4flash-db-first-full-01/dacomp-041/attempt-01/python/P23.stderr)。检出需人工核验的 SQL 可实现操作：groupby(, .merge(；不能仅凭理由判为合规。

## 优化机会

已验证候选。筛选限于精确 SQL、相同自包含 CTE、相同单表完整过滤、可分解单表聚合；未覆盖任意 Join 等价和一般谓词蕴含。全部候选都是 offline，未测在线预测。

| 候选 | 类型 | 已有结果 | 覆盖 SQL | 后续次数 | 中间行数 | 验证 | 成本 |
| --- | --- | --- | --- | --- | --- | --- | --- |
| C1 | exact-result reuse | True | ["S24", "S28"] | 1 | 1 | verified | Not benchmarked; correctness alone does not establish net speedup. |
| C2 | exact-result reuse | True | ["S25", "S29"] | 1 | 1 | verified | Not benchmarked; correctness alone does not establish net speedup. |
| C3 | common filtered view | False | ["S4", "S22"] | 1 | 104 | verified | Not benchmarked; correctness alone does not establish net speedup. |


已验证覆盖（含触发查询、候选并集去重）：6/31 条成功数据 SQL。正确性仅针对当前数据库快照；未测性能的候选不能声称已加速。

[完整 build/rewrite 与比较证据](dacomp-041.analysis.json)。

### C1：exact-result reuse

Identical normalized SQL and parameters; archive equality checked.

原查询 [S24](#s24), [S28](#s28) → 保留前序结果 S24 → 后续 1 次可复用。该构建点为事后假设，不代表 Agent 当时预知后续。

| 原 SQL | 列名一致 | 结果一致 | 比较方法 |
| --- | --- | --- | --- |
| S28 | True | True | exact_multiset |


验证状态：verified；成本结论：Not benchmarked; correctness alone does not establish net speedup.

### C2：exact-result reuse

Identical normalized SQL and parameters; archive equality checked.

原查询 [S25](#s25), [S29](#s29) → 保留前序结果 S25 → 后续 1 次可复用。该构建点为事后假设，不代表 Agent 当时预知后续。

| 原 SQL | 列名一致 | 结果一致 | 比较方法 |
| --- | --- | --- | --- |
| S29 | True | True | exact_multiset |


验证状态：verified；成本结论：Not benchmarked; correctness alone does not establish net speedup.

### C3：common filtered view

Same single source and complete filter; original filter retained.

原查询 [S4](#s4), [S22](#s22) → 新增共享状态 C3 → 后续 1 次可复用。该构建点为事后假设，不代表 Agent 当时预知后续。

构建定义：

```sql
SELECT * FROM "gallery_information" WHERE "Daily Visitor Count" > 900
```

受益查询 S4 的改写示例：

```sql
SELECT "Exhibition Hall Record ID", "Daily Visitor Count" FROM temp.reuse_candidate AS gallery_information WHERE "Daily Visitor Count" > 900 ORDER BY "Daily Visitor Count" DESC
```

| 原 SQL | 列名一致 | 结果一致 | 比较方法 |
| --- | --- | --- | --- |
| S4 | True | True | ordered_numeric_tolerance |
| S22 | True | True | ordered_numeric_tolerance |


验证状态：verified；成本结论：Not benchmarked; correctness alone does not establish net speedup.

结果依赖：自动记录 SQL→Python 的接口父调用，以及源码中引用归档文件的消费者；字面值相同不认定因果。模型方向选择需要人工读取消息，尚未做全面因果标注。

[原始报告](../../../runs/dsv4flash-db-first-full-01/dacomp-041/attempt-01/answer.md)；[统一消息](../../../runs/dsv4flash-db-first-full-01/dacomp-041/attempt-01/messages.jsonl)；[原始 OpenCode 事件](../../../runs/dsv4flash-db-first-full-01/dacomp-041/attempt-01/opencode.jsonl)；[SQL 引擎日志](../../../runs/dsv4flash-db-first-full-01/dacomp-041/attempt-01/sql_journal.jsonl)。

[可读报告（本地图片链接规范化）](../answers/dacomp-041.md)。原始回答保留，分析结论未改写。

## S1

类别 `connection_setup`；来源 `connection`；调用 `d539c57c2628444996a9feceed48fc3c`；状态 `success`。

```sql
PRAGMA query_only=ON
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-041/attempt-01/sql/S1.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-041/attempt-01/sql/S1.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-041/attempt-01/results/S1.rows.jsonl)；完整：True；SHA256：`e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`。

## S2

类别 `metadata`；来源 `list_db`；调用 `d539c57c2628444996a9feceed48fc3c`；状态 `success`。

```sql
SELECT name,sql FROM sqlite_master WHERE type='table' ORDER BY name
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-041/attempt-01/sql/S2.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-041/attempt-01/sql/S2.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-041/attempt-01/results/S2.rows.jsonl)；完整：True；SHA256：`ea259bdbd674b5b1dbbe05cf95a94f7846bc5728a77db35dd2d527619e7384b4`。

## S3

类别 `data`；来源 `query_db`；调用 `bc27783445ad42a08aad96acc026a728`；状态 `success`。

```sql
SELECT "Exhibition Hall Record ID", "Daily Visitor Count" FROM gallery_information ORDER BY "Daily Visitor Count" DESC
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-041/attempt-01/sql/S3.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-041/attempt-01/sql/S3.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-041/attempt-01/results/S3.rows.jsonl)；完整：True；SHA256：`d2a6bce975d1f7eac61a7bc5d2edf89802e0c6ae4277d578f6ca849175d44eaf`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "gallery_information", "kind": "base", "block": null, "base_tables": ["gallery_information"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |


## S4

类别 `data`；来源 `query_db`；调用 `093271e188ec4b1c90694d209b137859`；状态 `success`。

```sql
SELECT "Exhibition Hall Record ID", "Daily Visitor Count" FROM gallery_information WHERE "Daily Visitor Count" > 900 ORDER BY "Daily Visitor Count" DESC
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-041/attempt-01/sql/S4.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-041/attempt-01/sql/S4.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-041/attempt-01/results/S4.rows.jsonl)；完整：True；SHA256：`ddd0b8d145ea21f45b3889cfa89e61320414630dc51939379a308660dd97b77d`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "gallery_information", "kind": "base", "block": null, "base_tables": ["gallery_information"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |


## S5

类别 `data`；来源 `query_db`；调用 `f887ba0b24014b6d94a89d8bc49bb179`；状态 `success`。

```sql
SELECT COUNT(*) as total_halls, 
       AVG("Daily Visitor Count") as avg_visitor, 
       MAX("Daily Visitor Count") as max_visitor, 
       MIN("Daily Visitor Count") as min_visitor
FROM gallery_information
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-041/attempt-01/sql/S5.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-041/attempt-01/sql/S5.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-041/attempt-01/results/S5.rows.jsonl)；完整：True；SHA256：`a38c126f6443d1f6a362ce0fce853f745058dae4dcc4d782e8e4caa686063960`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "gallery_information", "kind": "base", "block": null, "base_tables": ["gallery_information"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |
| B1 | AVG("Daily Visitor Count") | [{"table": "gallery_information", "column": "Daily Visitor Count"}] | [] | False |
| B1 | MAX("Daily Visitor Count") | [{"table": "gallery_information", "column": "Daily Visitor Count"}] | [] | False |
| B1 | MIN("Daily Visitor Count") | [{"table": "gallery_information", "column": "Daily Visitor Count"}] | [] | False |


## S6

类别 `data`；来源 `query_db`；调用 `c9c2e6d2486e491eb0219e873bee8385`；状态 `success`。

```sql
SELECT DISTINCT "Gallery reference" FROM display_case_information LIMIT 20
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-041/attempt-01/sql/S6.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-041/attempt-01/sql/S6.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-041/attempt-01/results/S6.rows.jsonl)；完整：True；SHA256：`2b2f1e96b89fc1a12438e7bdca75493624f55c517d9c17df5d97e13878935cc1`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "display_case_information", "kind": "base", "block": null, "base_tables": ["display_case_information"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |


## S7

类别 `data`；来源 `query_db`；调用 `b2a9767b374f4cb29fe911ea325b4395`；状态 `success`。

```sql
SELECT DISTINCT "Display Case Reference" FROM environmental_monitoring_data LIMIT 20
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-041/attempt-01/sql/S7.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-041/attempt-01/sql/S7.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-041/attempt-01/results/S7.rows.jsonl)；完整：True；SHA256：`6a9556dd232c56075ea3ab72cf7788a85ef1c2daef49b6af05b20c47fef2e321`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "environmental_monitoring_data", "kind": "base", "block": null, "base_tables": ["environmental_monitoring_data"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |


## S8

类别 `data`；来源 `query_db`；调用 `fb15728512184fbd881f2d9ac1af6918`；状态 `success`。

```sql
SELECT DISTINCT "Gallery Reference" FROM artifact_conservation_and_maint LIMIT 20
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-041/attempt-01/sql/S8.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-041/attempt-01/sql/S8.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-041/attempt-01/results/S8.rows.jsonl)；完整：True；SHA256：`2b2f1e96b89fc1a12438e7bdca75493624f55c517d9c17df5d97e13878935cc1`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "artifact_conservation_and_maint", "kind": "base", "block": null, "base_tables": ["artifact_conservation_and_maint"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |


## S9

类别 `data`；来源 `query_db`；调用 `8d73573e2c384bc8aa08d5c10ff196d8`；状态 `success`。

```sql
SELECT COUNT(*) as total_cases, COUNT(DISTINCT "Display case ID") as distinct_cases, COUNT(DISTINCT "Gallery reference") as distinct_galleries FROM display_case_information
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-041/attempt-01/sql/S9.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-041/attempt-01/sql/S9.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-041/attempt-01/results/S9.rows.jsonl)；完整：True；SHA256：`536d1696b274dd097c73c02797b9f675e5f2ee53cafc722b137b0511e953342c`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "display_case_information", "kind": "base", "block": null, "base_tables": ["display_case_information"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |
| B1 | COUNT(DISTINCT "Display case ID") | [{"table": "display_case_information", "column": "Display case ID"}] | [] | False |
| B1 | COUNT(DISTINCT "Gallery reference") | [{"table": "display_case_information", "column": "Gallery reference"}] | [] | False |


## S10

类别 `data`；来源 `query_db`；调用 `93cd6cf849014d398cba3a27d18fdfd6`；状态 `success`。

```sql
SELECT emd."Display Case Reference", dci."Display case ID", dci."Gallery reference"
FROM environmental_monitoring_data emd
LEFT JOIN display_case_information dci ON TRIM(emd."Display Case Reference") = TRIM(dci."Display case ID")
WHERE dci."Display case ID" IS NULL
LIMIT 10
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-041/attempt-01/sql/S10.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-041/attempt-01/sql/S10.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-041/attempt-01/results/S10.rows.jsonl)；完整：True；SHA256：`e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "emd", "kind": "base", "block": null, "base_tables": ["environmental_monitoring_data"]}, {"alias": "dci", "kind": "base", "block": null, "base_tables": ["display_case_information"]}] | [{"type": "LEFT", "right": "display_case_information AS dci", "on": "TRIM(emd.\"Display Case Reference\") = TRIM(dci.\"Display case ID\")", "using": []}] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |


## S11

类别 `data`；来源 `query_db`；调用 `e41b50b446ed4d96a29c38f2cb05cb3b`；状态 `success`。

```sql
SELECT COUNT(*) as total_readings, COUNT(DISTINCT "Environmental Reading ID") as distinct_readings,
       COUNT(DISTINCT "Display Case Reference") as distinct_cases
FROM environmental_monitoring_data
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-041/attempt-01/sql/S11.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-041/attempt-01/sql/S11.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-041/attempt-01/results/S11.rows.jsonl)；完整：True；SHA256：`536d1696b274dd097c73c02797b9f675e5f2ee53cafc722b137b0511e953342c`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "environmental_monitoring_data", "kind": "base", "block": null, "base_tables": ["environmental_monitoring_data"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |
| B1 | COUNT(DISTINCT "Environmental Reading ID") | [{"table": "environmental_monitoring_data", "column": "Environmental Reading ID"}] | [] | False |
| B1 | COUNT(DISTINCT "Display Case Reference") | [{"table": "environmental_monitoring_data", "column": "Display Case Reference"}] | [] | False |


## S12

类别 `data`；来源 `query_db`；调用 `1536fde48eac419c9eb2d811857eb5f9`；状态 `success`。

```sql
SELECT aqr."Environmental monitoring reference", emd."Environmental Reading ID"
FROM air_quality_readings aqr
LEFT JOIN environmental_monitoring_data emd ON aqr."Environmental monitoring reference" = emd."Environmental Reading ID"
WHERE emd."Environmental Reading ID" IS NULL
LIMIT 5
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-041/attempt-01/sql/S12.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-041/attempt-01/sql/S12.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-041/attempt-01/results/S12.rows.jsonl)；完整：True；SHA256：`e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "aqr", "kind": "base", "block": null, "base_tables": ["air_quality_readings"]}, {"alias": "emd", "kind": "base", "block": null, "base_tables": ["environmental_monitoring_data"]}] | [{"type": "LEFT", "right": "environmental_monitoring_data AS emd", "on": "aqr.\"Environmental monitoring reference\" = emd.\"Environmental Reading ID\"", "using": []}] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |


## S13

类别 `data`；来源 `query_db`；调用 `950d40492d0e4eb7b8e823dfa4224de8`；状态 `success`。

```sql
SELECT COUNT(*) as aq_count, COUNT(DISTINCT "Environmental monitoring reference") as distinct_refs FROM air_quality_readings
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-041/attempt-01/sql/S13.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-041/attempt-01/sql/S13.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-041/attempt-01/results/S13.rows.jsonl)；完整：True；SHA256：`26850e0dbf257a45354c91ef69c0800d155ae09d6d5f9ae6a563cbf3a5cb66c5`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "air_quality_readings", "kind": "base", "block": null, "base_tables": ["air_quality_readings"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |
| B1 | COUNT(DISTINCT "Environmental monitoring reference") | [{"table": "air_quality_readings", "column": "Environmental monitoring reference"}] | [] | False |


## S14

类别 `data`；来源 `query_db`；调用 `7325ba7cc96f4404904756bc923760b9`；状态 `success`。

```sql
SELECT COUNT(*) as cons_count, COUNT(DISTINCT "Preserve Cultural Relic Reference") as distinct_relics, COUNT(DISTINCT "Gallery Reference") as distinct_galleries FROM artifact_conservation_and_maint
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-041/attempt-01/sql/S14.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-041/attempt-01/sql/S14.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-041/attempt-01/results/S14.rows.jsonl)；完整：True；SHA256：`536d1696b274dd097c73c02797b9f675e5f2ee53cafc722b137b0511e953342c`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "artifact_conservation_and_maint", "kind": "base", "block": null, "base_tables": ["artifact_conservation_and_maint"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |
| B1 | COUNT(DISTINCT "Preserve Cultural Relic Reference") | [{"table": "artifact_conservation_and_maint", "column": "Preserve Cultural Relic Reference"}] | [] | False |
| B1 | COUNT(DISTINCT "Gallery Reference") | [{"table": "artifact_conservation_and_maint", "column": "Gallery Reference"}] | [] | False |


## S15

类别 `data`；来源 `query_db`；调用 `e78d83baa13146f38ddee1635ef236e5`；状态 `success`。

```sql
SELECT COUNT(*) as rating_count, COUNT(DISTINCT "Cultural Relic Reference Number") as distinct_relics FROM artifact_rating
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-041/attempt-01/sql/S15.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-041/attempt-01/sql/S15.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-041/attempt-01/results/S15.rows.jsonl)；完整：True；SHA256：`26850e0dbf257a45354c91ef69c0800d155ae09d6d5f9ae6a563cbf3a5cb66c5`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "artifact_rating", "kind": "base", "block": null, "base_tables": ["artifact_rating"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |
| B1 | COUNT(DISTINCT "Cultural Relic Reference Number") | [{"table": "artifact_rating", "column": "Cultural Relic Reference Number"}] | [] | False |


## S16

类别 `data`；来源 `query_db`；调用 `450a4246a8064d4f83ecedbf23b196af`；状态 `success`。

```sql
SELECT COUNT(*) as basic_count, COUNT(DISTINCT "Cultural Relic Registration Number") as distinct_relics FROM basic_artifact_information
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-041/attempt-01/sql/S16.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-041/attempt-01/sql/S16.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-041/attempt-01/results/S16.rows.jsonl)；完整：True；SHA256：`26850e0dbf257a45354c91ef69c0800d155ae09d6d5f9ae6a563cbf3a5cb66c5`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "basic_artifact_information", "kind": "base", "block": null, "base_tables": ["basic_artifact_information"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |
| B1 | COUNT(DISTINCT "Cultural Relic Registration Number") | [{"table": "basic_artifact_information", "column": "Cultural Relic Registration Number"}] | [] | False |


## S17

类别 `data`；来源 `query_db`；调用 `030dd36a4f9243748ac6b81288aada46`；状态 `success`。

```sql
SELECT COUNT(*) as sens_count, COUNT(DISTINCT "Cultural Relic Reference Number") as distinct_relics FROM sensitivity_data
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-041/attempt-01/sql/S17.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-041/attempt-01/sql/S17.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-041/attempt-01/results/S17.rows.jsonl)；完整：True；SHA256：`26850e0dbf257a45354c91ef69c0800d155ae09d6d5f9ae6a563cbf3a5cb66c5`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "sensitivity_data", "kind": "base", "block": null, "base_tables": ["sensitivity_data"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |
| B1 | COUNT(DISTINCT "Cultural Relic Reference Number") | [{"table": "sensitivity_data", "column": "Cultural Relic Reference Number"}] | [] | False |


## S18

类别 `data`；来源 `query_db`；调用 `e7ffe9363bf44f9c8ae4a268ec9daed7`；状态 `success`。

```sql
SELECT COUNT(*) as cond_count, COUNT(DISTINCT "Inspected Cultural Relic Reference") as distinct_relics, COUNT(DISTINCT "Inspected Display Case Reference") as distinct_cases FROM condition_assessment
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-041/attempt-01/sql/S18.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-041/attempt-01/sql/S18.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-041/attempt-01/results/S18.rows.jsonl)；完整：True；SHA256：`536d1696b274dd097c73c02797b9f675e5f2ee53cafc722b137b0511e953342c`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "condition_assessment", "kind": "base", "block": null, "base_tables": ["condition_assessment"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |
| B1 | COUNT(DISTINCT "Inspected Cultural Relic Reference") | [{"table": "condition_assessment", "column": "Inspected Cultural Relic Reference"}] | [] | False |
| B1 | COUNT(DISTINCT "Inspected Display Case Reference") | [{"table": "condition_assessment", "column": "Inspected Display Case Reference"}] | [] | False |


## S19

类别 `data`；来源 `query_db`；调用 `85e574cba37b4574b885ebbcc03ec05b`；状态 `success`。

```sql
SELECT gi."Exhibition Hall Record ID", dci."Gallery reference"
FROM gallery_information gi
LEFT JOIN display_case_information dci ON TRIM(gi."Exhibition Hall Record ID") = TRIM(dci."Gallery reference")
WHERE dci."Gallery reference" IS NULL
LIMIT 5
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-041/attempt-01/sql/S19.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-041/attempt-01/sql/S19.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-041/attempt-01/results/S19.rows.jsonl)；完整：True；SHA256：`e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "gi", "kind": "base", "block": null, "base_tables": ["gallery_information"]}, {"alias": "dci", "kind": "base", "block": null, "base_tables": ["display_case_information"]}] | [{"type": "LEFT", "right": "display_case_information AS dci", "on": "TRIM(gi.\"Exhibition Hall Record ID\") = TRIM(dci.\"Gallery reference\")", "using": []}] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |


## S20

类别 `data`；来源 `query_db`；调用 `df7b8a2bf5844eeeace1eb46b72668de`；状态 `success`。

```sql
SELECT acm."Preserve Cultural Relic Reference", ar."Cultural Relic Reference Number"
FROM artifact_conservation_and_maint acm
LEFT JOIN artifact_rating ar ON TRIM(acm."Preserve Cultural Relic Reference") = TRIM(ar."Cultural Relic Reference Number")
WHERE ar."Cultural Relic Reference Number" IS NULL
LIMIT 5
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-041/attempt-01/sql/S20.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-041/attempt-01/sql/S20.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-041/attempt-01/results/S20.rows.jsonl)；完整：True；SHA256：`e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "acm", "kind": "base", "block": null, "base_tables": ["artifact_conservation_and_maint"]}, {"alias": "ar", "kind": "base", "block": null, "base_tables": ["artifact_rating"]}] | [{"type": "LEFT", "right": "artifact_rating AS ar", "on": "TRIM(acm.\"Preserve Cultural Relic Reference\") = TRIM(ar.\"Cultural Relic Reference Number\")", "using": []}] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |


## S21

类别 `data`；来源 `query_db`；调用 `c667970ef17845008ff979243375c7b0`；状态 `cancelled`。

```sql
SELECT COUNT(*) as count
FROM gallery_information gi
JOIN display_case_information dci ON TRIM(gi."Exhibition Hall Record ID") = TRIM(dci."Gallery reference")
JOIN environmental_monitoring_data emd ON TRIM(emd."Display Case Reference") = TRIM(dci."Display case ID")
JOIN air_quality_readings aqr ON aqr."Environmental monitoring reference" = emd."Environmental Reading ID"
JOIN light_and_radiation_readings lrr ON lrr."Environmental monitoring reference" = emd."Environmental Reading ID"
JOIN surface_and_physical_readings spr ON spr."Environmental Monitoring Reference" = emd."Environmental Reading ID"
JOIN artifact_conservation_and_maint acm ON TRIM(acm."Gallery Reference") = TRIM(gi."Exhibition Hall Record ID")
JOIN artifact_rating ar ON TRIM(ar."Cultural Relic Reference Number") = TRIM(acm."Preserve Cultural Relic Reference")
JOIN basic_artifact_information bai ON TRIM(bai."Cultural Relic Registration Number") = TRIM(ar."Cultural Relic Reference Number")
JOIN sensitivity_data sd ON TRIM(sd."Cultural Relic Reference Number") = TRIM(ar."Cultural Relic Reference Number")
JOIN condition_assessment ca ON TRIM(ca."Inspected Cultural Relic Reference") = TRIM(ar."Cultural Relic Reference Number")
WHERE gi."Daily Visitor Count" > 900
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-041/attempt-01/sql/S21.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-041/attempt-01/sql/S21.parameters.json)。

错误：`OperationalError('interrupted')`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "gi", "kind": "base", "block": null, "base_tables": ["gallery_information"]}, {"alias": "dci", "kind": "base", "block": null, "base_tables": ["display_case_information"]}, {"alias": "emd", "kind": "base", "block": null, "base_tables": ["environmental_monitoring_data"]}, {"alias": "aqr", "kind": "base", "block": null, "base_tables": ["air_quality_readings"]}, {"alias": "lrr", "kind": "base", "block": null, "base_tables": ["light_and_radiation_readings"]}, {"alias": "spr", "kind": "base", "block": null, "base_tables": ["surface_and_physical_readings"]}, {"alias": "acm", "kind": "base", "block": null, "base_tables": ["artifact_conservation_and_maint"]}, {"alias": "ar", "kind": "base", "block": null, "base_tables": ["artifact_rating"]}, {"alias": "bai", "kind": "base", "block": null, "base_tables": ["basic_artifact_information"]}, {"alias": "sd", "kind": "base", "block": null, "base_tables": ["sensitivity_data"]}, {"alias": "ca", "kind": "base", "block": null, "base_tables": ["condition_assessment"]}] | [{"type": "INNER", "right": "display_case_information AS dci", "on": "TRIM(gi.\"Exhibition Hall Record ID\") = TRIM(dci.\"Gallery reference\")", "using": []}, {"type": "INNER", "right": "environmental_monitoring_data AS emd", "on": "TRIM(emd.\"Display Case Reference\") = TRIM(dci.\"Display case ID\")", "using": []}, {"type": "INNER", "right": "air_quality_readings AS aqr", "on": "aqr.\"Environmental monitoring reference\" = emd.\"Environmental Reading ID\"", "using": []}, {"type": "INNER", "right": "light_and_radiation_readings AS lrr", "on": "lrr.\"Environmental monitoring reference\" = emd.\"Environmental Reading ID\"", "using": []}, {"type": "INNER", "right": "surface_and_physical_readings AS spr", "on": "spr.\"Environmental Monitoring Reference\" = emd.\"Environmental Reading ID\"", "using": []}, {"type": "INNER", "right": "artifact_conservation_and_maint AS acm", "on": "TRIM(acm.\"Gallery Reference\") = TRIM(gi.\"Exhibition Hall Record ID\")", "using": []}, {"type": "INNER", "right": "artifact_rating AS ar", "on": "TRIM(ar.\"Cultural Relic Reference Number\") = TRIM(acm.\"Preserve Cultural Relic Reference\")", "using": []}, {"type": "INNER", "right": "basic_artifact_information AS bai", "on": "TRIM(bai.\"Cultural Relic Registration Number\") = TRIM(ar.\"Cultural Relic Reference Number\")", "using": []}, {"type": "INNER", "right": "sensitivity_data AS sd", "on": "TRIM(sd.\"Cultural Relic Reference Number\") = TRIM(ar.\"Cultural Relic Reference Number\")", "using": []}, {"type": "INNER", "right": "condition_assessment AS ca", "on": "TRIM(ca.\"Inspected Cultural Relic Reference\") = TRIM(ar.\"Cultural Relic Reference Number\")", "using": []}] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |


## S22

类别 `data`；来源 `query_db`；调用 `5f7e835fb30243b79e9de971fd6cc414`；状态 `success`。

```sql
SELECT TRIM(gi."Exhibition Hall Record ID") as hall_id, gi."Daily Visitor Count"
FROM gallery_information gi
WHERE gi."Daily Visitor Count" > 900
ORDER BY gi."Daily Visitor Count" DESC
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-041/attempt-01/sql/S22.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-041/attempt-01/sql/S22.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-041/attempt-01/results/S22.rows.jsonl)；完整：True；SHA256：`74e67e7225b91d9395a3c735fbcf925b83aa16bdc31ec7059371edd2e6cda391`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "gi", "kind": "base", "block": null, "base_tables": ["gallery_information"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |


## S23

类别 `data`；来源 `query_db`；调用 `7f343bfd467c46dcbe21a92c67ba26ad`；状态 `failed`。

```sql
SELECT gi."Exhibition Hall Record ID" as hall_id, gi."Daily Visitor Count",
       emd."Temperature (°C)", emd."24-hour Temperature Change", emd."Relative Humidity (%)", emd."24-hour Humidity Change",
       aqr."Carbon dioxide concentration (ppm)", aqr."Total volatile organic compounds concentration (ppb)",
       aqr."Ozone concentration (ppb)", aqr."Sulfur dioxide concentration (ppb)", aqr."Nitrogen dioxide concentration (ppb)",
       aqr."PM2.5 concentration", aqr."PM10 concentration", aqr."Formaldehyde concentration",
       aqr."Air exchange rate", aqr."Airflow velocity (m/s)",
       lrr."Illuminance (Lux)", lrr."UV Irradiance (μW/cm²)", lrr."IR Irradiance (W/m²)", lrr."Visible Light Exposure (Lx·h)",
       spr."Vibration Level (mm/s²)", spr."Noise Level (dB)", spr."Dust Accumulation (mg/m²)",
       spr."Microbial Count (CFU)", spr."Mold Risk Index", spr."Pest Activity Level",
       spr."Metal Corrosion Rate", spr."Organic Degradation Index", spr."Color Change (ΔE)",
       spr."Surface Temperature (°C)", spr."Surface Relative Humidity (%)", spr."Condensation Risk",
       spr."Oxygen Concentration", spr."Nitrogen Concentration"
FROM gallery_information gi
JOIN display_case_information dci ON TRIM(gi."Exhibition Hall Record ID") = TRIM(dci."Gallery reference")
JOIN environmental_monitoring_data emd ON TRIM(emd."Display Case Reference") = TRIM(dci."Display case ID")
JOIN air_quality_readings aqr ON aqr."Environmental monitoring reference" = emd."Environmental Reading ID"
JOIN light_and_radiation_readings lrr ON lrr."Environmental monitoring reference" = emd."Environmental Reading ID"
JOIN surface_and_physical_readings spr ON spr."Environmental Monitoring Reference" = emd."Environmental Reading ID"
WHERE gi."Daily Visitor Count" > 900
ORDER BY gi."Daily Visitor Count" DESC
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-041/attempt-01/sql/S23.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-041/attempt-01/sql/S23.parameters.json)。

错误：`OperationalError('no such column: lrr.Illuminance (Lux)')`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "gi", "kind": "base", "block": null, "base_tables": ["gallery_information"]}, {"alias": "dci", "kind": "base", "block": null, "base_tables": ["display_case_information"]}, {"alias": "emd", "kind": "base", "block": null, "base_tables": ["environmental_monitoring_data"]}, {"alias": "aqr", "kind": "base", "block": null, "base_tables": ["air_quality_readings"]}, {"alias": "lrr", "kind": "base", "block": null, "base_tables": ["light_and_radiation_readings"]}, {"alias": "spr", "kind": "base", "block": null, "base_tables": ["surface_and_physical_readings"]}] | [{"type": "INNER", "right": "display_case_information AS dci", "on": "TRIM(gi.\"Exhibition Hall Record ID\") = TRIM(dci.\"Gallery reference\")", "using": []}, {"type": "INNER", "right": "environmental_monitoring_data AS emd", "on": "TRIM(emd.\"Display Case Reference\") = TRIM(dci.\"Display case ID\")", "using": []}, {"type": "INNER", "right": "air_quality_readings AS aqr", "on": "aqr.\"Environmental monitoring reference\" = emd.\"Environmental Reading ID\"", "using": []}, {"type": "INNER", "right": "light_and_radiation_readings AS lrr", "on": "lrr.\"Environmental monitoring reference\" = emd.\"Environmental Reading ID\"", "using": []}, {"type": "INNER", "right": "surface_and_physical_readings AS spr", "on": "spr.\"Environmental Monitoring Reference\" = emd.\"Environmental Reading ID\"", "using": []}] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |


## S24

类别 `data`；来源 `query_db`；调用 `d6e0b646fdb64a0a9490e6339fb5c2cf`；状态 `success`。

```sql
SELECT * FROM light_and_radiation_readings LIMIT 1
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-041/attempt-01/sql/S24.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-041/attempt-01/sql/S24.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-041/attempt-01/results/S24.rows.jsonl)；完整：True；SHA256：`7f2cb4488583c25c3e55a8053bc92f395b3bacaaf77bd49e5280ee93555ad722`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "light_and_radiation_readings", "kind": "base", "block": null, "base_tables": ["light_and_radiation_readings"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |


## S25

类别 `data`；来源 `query_db`；调用 `a7a9f9ed4f384599a0ad624eefd092c2`；状态 `success`。

```sql
SELECT * FROM surface_and_physical_readings LIMIT 1
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-041/attempt-01/sql/S25.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-041/attempt-01/sql/S25.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-041/attempt-01/results/S25.rows.jsonl)；完整：True；SHA256：`924f8c1fb02f85b3e3c0ff663638c7064aef4bc25576e292569328812079690d`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "surface_and_physical_readings", "kind": "base", "block": null, "base_tables": ["surface_and_physical_readings"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |


## S26

类别 `data`；来源 `query_db`；调用 `0d6d8916f495478099a3a47cd0ea9434`；状态 `failed`。

```sql
SELECT gi."Exhibition Hall Record ID" as hall_id, gi."Daily Visitor Count",
       emd."Temperature (°C)", emd."24-hour Temperature Change", emd."Relative Humidity (%)", emd."24-hour Humidity Change",
       aqr."Carbon dioxide concentration (ppm)", aqr."Total volatile organic compounds concentration (ppb)",
       aqr."Ozone concentration (ppb)", aqr."Sulfur dioxide concentration (ppb)", aqr."Nitrogen dioxide concentration (ppb)",
       aqr."PM2.5 concentration", aqr."PM10 concentration", aqr."Formaldehyde concentration",
       aqr."Air exchange rate", aqr."Airflow velocity (m/s)",
       lrr."Illuminance (Lux)", lrr."UV Irradiance (μW/cm²)", lrr."IR Irradiance (W/m²)", lrr."Visible Light Exposure (Lx·h)",
       spr."Vibration Level (mm/s²)", spr."Noise Level (dB)", spr."Dust Accumulation (mg/m²)",
       spr."Microbial Count (CFU)", spr."Mold Risk Index", spr."Pest Activity Level",
       spr."Metal Corrosion Rate", spr."Organic Degradation Index", spr."Color Change (ΔE)",
       spr."Surface Temperature (°C)", spr."Surface Relative Humidity (%)", spr."Condensation Risk",
       spr."Oxygen Concentration", spr."Nitrogen Concentration"
FROM gallery_information gi
JOIN display_case_information dci ON TRIM(gi."Exhibition Hall Record ID") = TRIM(dci."Gallery reference")
JOIN environmental_monitoring_data emd ON TRIM(emd."Display Case Reference") = TRIM(dci."Display case ID")
JOIN air_quality_readings aqr ON aqr."Environmental monitoring reference" = emd."Environmental Reading ID"
JOIN light_and_radiation_readings lrr ON lrr."Environmental monitoring reference" = emd."Environmental Reading ID"
JOIN surface_and_physical_readings spr ON spr."Environmental Monitoring Reference" = emd."Environmental Reading ID"
WHERE gi."Daily Visitor Count" > 900
ORDER BY gi."Daily Visitor Count" DESC
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-041/attempt-01/sql/S26.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-041/attempt-01/sql/S26.parameters.json)。

错误：`OperationalError('no such column: lrr.Illuminance (Lux)')`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "gi", "kind": "base", "block": null, "base_tables": ["gallery_information"]}, {"alias": "dci", "kind": "base", "block": null, "base_tables": ["display_case_information"]}, {"alias": "emd", "kind": "base", "block": null, "base_tables": ["environmental_monitoring_data"]}, {"alias": "aqr", "kind": "base", "block": null, "base_tables": ["air_quality_readings"]}, {"alias": "lrr", "kind": "base", "block": null, "base_tables": ["light_and_radiation_readings"]}, {"alias": "spr", "kind": "base", "block": null, "base_tables": ["surface_and_physical_readings"]}] | [{"type": "INNER", "right": "display_case_information AS dci", "on": "TRIM(gi.\"Exhibition Hall Record ID\") = TRIM(dci.\"Gallery reference\")", "using": []}, {"type": "INNER", "right": "environmental_monitoring_data AS emd", "on": "TRIM(emd.\"Display Case Reference\") = TRIM(dci.\"Display case ID\")", "using": []}, {"type": "INNER", "right": "air_quality_readings AS aqr", "on": "aqr.\"Environmental monitoring reference\" = emd.\"Environmental Reading ID\"", "using": []}, {"type": "INNER", "right": "light_and_radiation_readings AS lrr", "on": "lrr.\"Environmental monitoring reference\" = emd.\"Environmental Reading ID\"", "using": []}, {"type": "INNER", "right": "surface_and_physical_readings AS spr", "on": "spr.\"Environmental Monitoring Reference\" = emd.\"Environmental Reading ID\"", "using": []}] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |


## S27

类别 `data`；来源 `query_db`；调用 `eb11a95a50a146359f099d98b831206b`；状态 `failed`。

```sql
SELECT "Light & Radiation Record ID", "Environmental monitoring reference", "\" Illuminance (Lux)\"" FROM light_and_radiation_readings LIMIT 1
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-041/attempt-01/sql/S27.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-041/attempt-01/sql/S27.parameters.json)。

错误：`OperationalError('near "(": syntax error')`。

## S28

类别 `data`；来源 `python`；调用 `3586879de61149d6b54304f22a2dd85f`；状态 `success`。

```sql
SELECT * FROM light_and_radiation_readings LIMIT 1
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-041/attempt-01/sql/S28.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-041/attempt-01/sql/S28.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-041/attempt-01/results/S28.rows.jsonl)；完整：True；SHA256：`7f2cb4488583c25c3e55a8053bc92f395b3bacaaf77bd49e5280ee93555ad722`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "light_and_radiation_readings", "kind": "base", "block": null, "base_tables": ["light_and_radiation_readings"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |


## S29

类别 `data`；来源 `python`；调用 `3586879de61149d6b54304f22a2dd85f`；状态 `success`。

```sql
SELECT * FROM surface_and_physical_readings LIMIT 1
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-041/attempt-01/sql/S29.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-041/attempt-01/sql/S29.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-041/attempt-01/results/S29.rows.jsonl)；完整：True；SHA256：`924f8c1fb02f85b3e3c0ff663638c7064aef4bc25576e292569328812079690d`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "surface_and_physical_readings", "kind": "base", "block": null, "base_tables": ["surface_and_physical_readings"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |


## S30

类别 `data`；来源 `python`；调用 `a8930cc7804d452b98218d1744134b81`；状态 `success`。

```sql

SELECT TRIM(gi."Exhibition Hall Record ID") as hall_id, gi."Daily Visitor Count",
       emd."Temperature (°C)", emd."24-hour Temperature Change", emd."Relative Humidity (%)", emd."24-hour Humidity Change",
       emd."Atmospheric Pressure (hPa)",
       aqr."Carbon dioxide concentration (ppm)", aqr."Total volatile organic compounds concentration (ppb)",
       aqr."Ozone concentration (ppb)", aqr."Sulfur dioxide concentration (ppb)", aqr."Nitrogen dioxide concentration (ppb)",
       aqr."PM2.5 concentration", aqr."PM10 concentration", aqr."Formaldehyde concentration",
       aqr."Air exchange rate", aqr."Airflow velocity (m/s)",
       lrr." Illuminance (Lux)", lrr."UV Irradiance (μW/cm²)", lrr." IR Irradiance (W/m²)", lrr."Visible Light Exposure (Lx·h)",
       spr." Vibration Level (mm/s²)", spr." Noise Level (dB)", spr."Dust Accumulation (mg/m²)",
       spr." Microbial Count (CFU)", spr." Mold Risk Index", spr." Pest Activity Level",
       spr."Metal Corrosion Rate", spr."Organic Degradation Index", spr." Color Change (ΔE)",
       spr."Surface Temperature (°C)", spr."Surface Relative Humidity (%)", spr." Condensation Risk",
       spr."Oxygen Concentration", spr." Nitrogen Concentration"
FROM gallery_information gi
JOIN display_case_information dci ON TRIM(gi."Exhibition Hall Record ID") = TRIM(dci."Gallery reference")
JOIN environmental_monitoring_data emd ON TRIM(emd."Display Case Reference") = TRIM(dci."Display case ID")
JOIN air_quality_readings aqr ON aqr."Environmental monitoring reference" = emd."Environmental Reading ID"
JOIN light_and_radiation_readings lrr ON lrr."Environmental monitoring reference" = emd."Environmental Reading ID"
JOIN surface_and_physical_readings spr ON spr."Environmental Monitoring Reference" = emd."Environmental Reading ID"
WHERE gi."Daily Visitor Count" > 900
ORDER BY gi."Daily Visitor Count" DESC

```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-041/attempt-01/sql/S30.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-041/attempt-01/sql/S30.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-041/attempt-01/results/S30.rows.jsonl)；完整：True；SHA256：`6d0c5d21b04096338033ebcf01391dd46c9231449321aecd42dd9faae897c8ae`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "gi", "kind": "base", "block": null, "base_tables": ["gallery_information"]}, {"alias": "dci", "kind": "base", "block": null, "base_tables": ["display_case_information"]}, {"alias": "emd", "kind": "base", "block": null, "base_tables": ["environmental_monitoring_data"]}, {"alias": "aqr", "kind": "base", "block": null, "base_tables": ["air_quality_readings"]}, {"alias": "lrr", "kind": "base", "block": null, "base_tables": ["light_and_radiation_readings"]}, {"alias": "spr", "kind": "base", "block": null, "base_tables": ["surface_and_physical_readings"]}] | [{"type": "INNER", "right": "display_case_information AS dci", "on": "TRIM(gi.\"Exhibition Hall Record ID\") = TRIM(dci.\"Gallery reference\")", "using": []}, {"type": "INNER", "right": "environmental_monitoring_data AS emd", "on": "TRIM(emd.\"Display Case Reference\") = TRIM(dci.\"Display case ID\")", "using": []}, {"type": "INNER", "right": "air_quality_readings AS aqr", "on": "aqr.\"Environmental monitoring reference\" = emd.\"Environmental Reading ID\"", "using": []}, {"type": "INNER", "right": "light_and_radiation_readings AS lrr", "on": "lrr.\"Environmental monitoring reference\" = emd.\"Environmental Reading ID\"", "using": []}, {"type": "INNER", "right": "surface_and_physical_readings AS spr", "on": "spr.\"Environmental Monitoring Reference\" = emd.\"Environmental Reading ID\"", "using": []}] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |


## S31

类别 `data`；来源 `python`；调用 `485ff39fa1c44384b9f318a5a1f7590b`；状态 `success`。

```sql

SELECT TRIM(gi."Exhibition Hall Record ID") as hall_id, gi."Daily Visitor Count",
       TRIM(acm."Preserve Cultural Relic Reference") as relic_ref,
       bai."Cultural Relic Name", bai."Dynasty", bai."Date (Year)", bai."Material Type", bai."Preservation Status",
       ar."Historical Significance Rating", ar."Research Value Rating", ar."Exhibition Value Rating",
       ar."Cultural Value Score", ar."Public Accessibility Rating", ar."Educational Value Rating",
       ar."Conservation Difficulty", ar."Treatment Complexity", ar."Material Stability", ar."Deterioration Rate",
       sd."Environmental Sensitivity", sd."Light Sensitivity", sd."Temperature Sensitivity", sd."Humidity Sensitivity",
       sd."Vibration Sensitivity", sd."Contamination Sensitivity",
       ca."Condition Assessment Rating",
       acm."Treatment Status", acm."Treatment Priority", acm."Treatment Effectiveness", acm."Reversibility Potential",
       sas." Security Level", sas."Insurance Value (USD)"
FROM gallery_information gi
JOIN artifact_conservation_and_maint acm ON TRIM(gi."Exhibition Hall Record ID") = TRIM(acm."Gallery Reference")
JOIN artifact_rating ar ON TRIM(ar."Cultural Relic Reference Number") = TRIM(acm."Preserve Cultural Relic Reference")
JOIN basic_artifact_information bai ON TRIM(bai."Cultural Relic Registration Number") = TRIM(ar."Cultural Relic Reference Number")
JOIN sensitivity_data sd ON TRIM(sd."Cultural Relic Reference Number") = TRIM(ar."Cultural Relic Reference Number")
JOIN condition_assessment ca ON TRIM(ca."Inspected Cultural Relic Reference") = TRIM(ar."Cultural Relic Reference Number")
JOIN artifact_security_and_access sas ON TRIM(sas."Cultural Relic Reference Number") = TRIM(ar."Cultural Relic Reference Number")
WHERE gi."Daily Visitor Count" > 900
ORDER BY gi."Daily Visitor Count" DESC

```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-041/attempt-01/sql/S31.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-041/attempt-01/sql/S31.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-041/attempt-01/results/S31.rows.jsonl)；完整：True；SHA256：`ed6f66b00508874482a4744a6486f18579a3630de926ef71e6d05d43d9037389`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "gi", "kind": "base", "block": null, "base_tables": ["gallery_information"]}, {"alias": "acm", "kind": "base", "block": null, "base_tables": ["artifact_conservation_and_maint"]}, {"alias": "ar", "kind": "base", "block": null, "base_tables": ["artifact_rating"]}, {"alias": "bai", "kind": "base", "block": null, "base_tables": ["basic_artifact_information"]}, {"alias": "sd", "kind": "base", "block": null, "base_tables": ["sensitivity_data"]}, {"alias": "ca", "kind": "base", "block": null, "base_tables": ["condition_assessment"]}, {"alias": "sas", "kind": "base", "block": null, "base_tables": ["artifact_security_and_access"]}] | [{"type": "INNER", "right": "artifact_conservation_and_maint AS acm", "on": "TRIM(gi.\"Exhibition Hall Record ID\") = TRIM(acm.\"Gallery Reference\")", "using": []}, {"type": "INNER", "right": "artifact_rating AS ar", "on": "TRIM(ar.\"Cultural Relic Reference Number\") = TRIM(acm.\"Preserve Cultural Relic Reference\")", "using": []}, {"type": "INNER", "right": "basic_artifact_information AS bai", "on": "TRIM(bai.\"Cultural Relic Registration Number\") = TRIM(ar.\"Cultural Relic Reference Number\")", "using": []}, {"type": "INNER", "right": "sensitivity_data AS sd", "on": "TRIM(sd.\"Cultural Relic Reference Number\") = TRIM(ar.\"Cultural Relic Reference Number\")", "using": []}, {"type": "INNER", "right": "condition_assessment AS ca", "on": "TRIM(ca.\"Inspected Cultural Relic Reference\") = TRIM(ar.\"Cultural Relic Reference Number\")", "using": []}, {"type": "INNER", "right": "artifact_security_and_access AS sas", "on": "TRIM(sas.\"Cultural Relic Reference Number\") = TRIM(ar.\"Cultural Relic Reference Number\")", "using": []}] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |


## S32

类别 `data`；来源 `python`；调用 `dd7a3ed6f54246f8828b586af5031a39`；状态 `success`。

```sql

SELECT TRIM(gi."Exhibition Hall Record ID") as hall_id, gi."Daily Visitor Count", gi."Visitor Traffic",
       gi."Average Dwell Time (minutes)", gi."Surveillance Coverage Status", gi."Motion Detection Status",
       gi."Alarm System Status", gi."Access Control Status",
       dci."Airtightness", dci."Display case material", dci."Seal status", dci."Maintenance Status",
       dci."Filter status", dci."Silica gel status", dci."Humidity buffering capacity",
       dci."Pollutant absorption capacity", dci."Leak rate", dci."Pressure (Pa)",
       dci."Inert gas system status", dci."Fire suppression system status", dci."Power status", dci."Backup system status"
FROM gallery_information gi
JOIN display_case_information dci ON TRIM(gi."Exhibition Hall Record ID") = TRIM(dci."Gallery reference")
WHERE gi."Daily Visitor Count" > 900
ORDER BY gi."Daily Visitor Count" DESC

```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-041/attempt-01/sql/S32.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-041/attempt-01/sql/S32.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-041/attempt-01/results/S32.rows.jsonl)；完整：True；SHA256：`a4e30ecb5355d90dc5362254a3e05b9bfb63152936d9985948fbb251f69891aa`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "gi", "kind": "base", "block": null, "base_tables": ["gallery_information"]}, {"alias": "dci", "kind": "base", "block": null, "base_tables": ["display_case_information"]}] | [{"type": "INNER", "right": "display_case_information AS dci", "on": "TRIM(gi.\"Exhibition Hall Record ID\") = TRIM(dci.\"Gallery reference\")", "using": []}] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |


## S33

类别 `data`；来源 `python`；调用 `dd7a3ed6f54246f8828b586af5031a39`；状态 `success`。

```sql

SELECT gi."Daily Visitor Count" as dv,
       emd."Temperature (°C)" as temp, emd."Relative Humidity (%)" as rh
FROM gallery_information gi
JOIN display_case_information dci ON TRIM(gi."Exhibition Hall Record ID") = TRIM(dci."Gallery reference")
JOIN environmental_monitoring_data emd ON TRIM(emd."Display Case Reference") = TRIM(dci."Display case ID")

```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-041/attempt-01/sql/S33.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-041/attempt-01/sql/S33.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-041/attempt-01/results/S33.rows.jsonl)；完整：True；SHA256：`de3cdb337c107b4f92699160f4a5794646efe624cdea69865f10048a8f7b5d17`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "gi", "kind": "base", "block": null, "base_tables": ["gallery_information"]}, {"alias": "dci", "kind": "base", "block": null, "base_tables": ["display_case_information"]}, {"alias": "emd", "kind": "base", "block": null, "base_tables": ["environmental_monitoring_data"]}] | [{"type": "INNER", "right": "display_case_information AS dci", "on": "TRIM(gi.\"Exhibition Hall Record ID\") = TRIM(dci.\"Gallery reference\")", "using": []}, {"type": "INNER", "right": "environmental_monitoring_data AS emd", "on": "TRIM(emd.\"Display Case Reference\") = TRIM(dci.\"Display case ID\")", "using": []}] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |


## S34

类别 `data`；来源 `python`；调用 `2f44d356b4564bf983bd981d345b5271`；状态 `success`。

```sql

SELECT TRIM(gi."Exhibition Hall Record ID") as hall_id, gi."Daily Visitor Count",
       emd."Temperature (°C)", emd."24-hour Temperature Change", emd."Relative Humidity (%)", emd."24-hour Humidity Change",
       emd."Atmospheric Pressure (hPa)",
       aqr."Carbon dioxide concentration (ppm)", aqr."Total volatile organic compounds concentration (ppb)",
       aqr."Ozone concentration (ppb)", aqr."Sulfur dioxide concentration (ppb)", aqr."Nitrogen dioxide concentration (ppb)",
       aqr."PM2.5 concentration", aqr."PM10 concentration", aqr."Formaldehyde concentration",
       aqr."Air exchange rate", aqr."Airflow velocity (m/s)",
       lrr." Illuminance (Lux)", lrr."UV Irradiance (μW/cm²)", lrr." IR Irradiance (W/m²)", lrr."Visible Light Exposure (Lx·h)",
       spr." Vibration Level (mm/s²)", spr." Noise Level (dB)", spr."Dust Accumulation (mg/m²)",
       spr." Microbial Count (CFU)", spr." Mold Risk Index", spr." Pest Activity Level",
       spr."Metal Corrosion Rate", spr."Organic Degradation Index", spr." Color Change (ΔE)",
       spr."Surface Temperature (°C)", spr."Surface Relative Humidity (%)", spr." Condensation Risk",
       spr."Oxygen Concentration", spr." Nitrogen Concentration"
FROM gallery_information gi
JOIN display_case_information dci ON TRIM(gi."Exhibition Hall Record ID") = TRIM(dci."Gallery reference")
JOIN environmental_monitoring_data emd ON TRIM(emd."Display Case Reference") = TRIM(dci."Display case ID")
JOIN air_quality_readings aqr ON aqr."Environmental monitoring reference" = emd."Environmental Reading ID"
JOIN light_and_radiation_readings lrr ON lrr."Environmental monitoring reference" = emd."Environmental Reading ID"
JOIN surface_and_physical_readings spr ON spr."Environmental Monitoring Reference" = emd."Environmental Reading ID"
ORDER BY gi."Daily Visitor Count" DESC

```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-041/attempt-01/sql/S34.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-041/attempt-01/sql/S34.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-041/attempt-01/results/S34.rows.jsonl)；完整：True；SHA256：`ac8184de3fc2fb822b6e01b1c16579d5082b05f2f411fb0efee259db3932c5eb`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "gi", "kind": "base", "block": null, "base_tables": ["gallery_information"]}, {"alias": "dci", "kind": "base", "block": null, "base_tables": ["display_case_information"]}, {"alias": "emd", "kind": "base", "block": null, "base_tables": ["environmental_monitoring_data"]}, {"alias": "aqr", "kind": "base", "block": null, "base_tables": ["air_quality_readings"]}, {"alias": "lrr", "kind": "base", "block": null, "base_tables": ["light_and_radiation_readings"]}, {"alias": "spr", "kind": "base", "block": null, "base_tables": ["surface_and_physical_readings"]}] | [{"type": "INNER", "right": "display_case_information AS dci", "on": "TRIM(gi.\"Exhibition Hall Record ID\") = TRIM(dci.\"Gallery reference\")", "using": []}, {"type": "INNER", "right": "environmental_monitoring_data AS emd", "on": "TRIM(emd.\"Display Case Reference\") = TRIM(dci.\"Display case ID\")", "using": []}, {"type": "INNER", "right": "air_quality_readings AS aqr", "on": "aqr.\"Environmental monitoring reference\" = emd.\"Environmental Reading ID\"", "using": []}, {"type": "INNER", "right": "light_and_radiation_readings AS lrr", "on": "lrr.\"Environmental monitoring reference\" = emd.\"Environmental Reading ID\"", "using": []}, {"type": "INNER", "right": "surface_and_physical_readings AS spr", "on": "spr.\"Environmental Monitoring Reference\" = emd.\"Environmental Reading ID\"", "using": []}] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |


## S35

类别 `data`；来源 `python`；调用 `2f44d356b4564bf983bd981d345b5271`；状态 `success`。

```sql

SELECT TRIM(gi."Exhibition Hall Record ID") as hall_id, gi."Daily Visitor Count",
       TRIM(acm."Preserve Cultural Relic Reference") as relic_ref,
       bai."Cultural Relic Name", bai."Dynasty", bai."Date (Year)", bai."Material Type", bai."Preservation Status",
       ar."Historical Significance Rating", ar."Research Value Rating", ar."Exhibition Value Rating",
       ar."Cultural Value Score", ar."Public Accessibility Rating", ar."Educational Value Rating",
       ar."Conservation Difficulty", ar."Treatment Complexity", ar."Material Stability", ar."Deterioration Rate",
       sd."Environmental Sensitivity", sd."Light Sensitivity", sd."Temperature Sensitivity", sd."Humidity Sensitivity",
       sd."Vibration Sensitivity", sd."Contamination Sensitivity",
       ca."Condition Assessment Rating",
       acm."Treatment Status", acm."Treatment Priority", acm."Treatment Effectiveness", acm."Reversibility Potential",
       sas." Security Level", sas."Insurance Value (USD)"
FROM gallery_information gi
JOIN artifact_conservation_and_maint acm ON TRIM(gi."Exhibition Hall Record ID") = TRIM(acm."Gallery Reference")
JOIN artifact_rating ar ON TRIM(ar."Cultural Relic Reference Number") = TRIM(acm."Preserve Cultural Relic Reference")
JOIN basic_artifact_information bai ON TRIM(bai."Cultural Relic Registration Number") = TRIM(ar."Cultural Relic Reference Number")
JOIN sensitivity_data sd ON TRIM(sd."Cultural Relic Reference Number") = TRIM(ar."Cultural Relic Reference Number")
JOIN condition_assessment ca ON TRIM(ca."Inspected Cultural Relic Reference") = TRIM(ar."Cultural Relic Reference Number")
JOIN artifact_security_and_access sas ON TRIM(sas."Cultural Relic Reference Number") = TRIM(ar."Cultural Relic Reference Number")
ORDER BY gi."Daily Visitor Count" DESC

```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-041/attempt-01/sql/S35.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-041/attempt-01/sql/S35.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-041/attempt-01/results/S35.rows.jsonl)；完整：True；SHA256：`dedfdacb744b04d5131317a42cf3bddd4a1872107941ed9d88254b7dcb61c4cc`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "gi", "kind": "base", "block": null, "base_tables": ["gallery_information"]}, {"alias": "acm", "kind": "base", "block": null, "base_tables": ["artifact_conservation_and_maint"]}, {"alias": "ar", "kind": "base", "block": null, "base_tables": ["artifact_rating"]}, {"alias": "bai", "kind": "base", "block": null, "base_tables": ["basic_artifact_information"]}, {"alias": "sd", "kind": "base", "block": null, "base_tables": ["sensitivity_data"]}, {"alias": "ca", "kind": "base", "block": null, "base_tables": ["condition_assessment"]}, {"alias": "sas", "kind": "base", "block": null, "base_tables": ["artifact_security_and_access"]}] | [{"type": "INNER", "right": "artifact_conservation_and_maint AS acm", "on": "TRIM(gi.\"Exhibition Hall Record ID\") = TRIM(acm.\"Gallery Reference\")", "using": []}, {"type": "INNER", "right": "artifact_rating AS ar", "on": "TRIM(ar.\"Cultural Relic Reference Number\") = TRIM(acm.\"Preserve Cultural Relic Reference\")", "using": []}, {"type": "INNER", "right": "basic_artifact_information AS bai", "on": "TRIM(bai.\"Cultural Relic Registration Number\") = TRIM(ar.\"Cultural Relic Reference Number\")", "using": []}, {"type": "INNER", "right": "sensitivity_data AS sd", "on": "TRIM(sd.\"Cultural Relic Reference Number\") = TRIM(ar.\"Cultural Relic Reference Number\")", "using": []}, {"type": "INNER", "right": "condition_assessment AS ca", "on": "TRIM(ca.\"Inspected Cultural Relic Reference\") = TRIM(ar.\"Cultural Relic Reference Number\")", "using": []}, {"type": "INNER", "right": "artifact_security_and_access AS sas", "on": "TRIM(sas.\"Cultural Relic Reference Number\") = TRIM(ar.\"Cultural Relic Reference Number\")", "using": []}] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |


## S36

类别 `data`；来源 `python`；调用 `64b7a219e205421690dbd42666e6997d`；状态 `success`。

```sql

SELECT ra.* FROM risk_assessment ra
JOIN gallery_information gi ON TRIM(gi."Exhibition Hall Record ID") = TRIM(ra."Related Gallery References")
WHERE gi."Daily Visitor Count" > 900

```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-041/attempt-01/sql/S36.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-041/attempt-01/sql/S36.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-041/attempt-01/results/S36.rows.jsonl)；完整：True；SHA256：`c7e033458d295a025d0794885e531a3ec33c6496866415a603b6e3020216fc1e`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "ra", "kind": "base", "block": null, "base_tables": ["risk_assessment"]}, {"alias": "gi", "kind": "base", "block": null, "base_tables": ["gallery_information"]}] | [{"type": "INNER", "right": "gallery_information AS gi", "on": "TRIM(gi.\"Exhibition Hall Record ID\") = TRIM(ra.\"Related Gallery References\")", "using": []}] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |


## S37

类别 `data`；来源 `python`；调用 `64b7a219e205421690dbd42666e6997d`；状态 `success`。

```sql

SELECT ur.* FROM usage_records ur
JOIN artifact_conservation_and_maint acm ON TRIM(acm."Preserve Cultural Relic Reference") = TRIM(ur."Cultural Relic Reference Number")
JOIN gallery_information gi ON TRIM(gi."Exhibition Hall Record ID") = TRIM(acm."Gallery Reference")
WHERE gi."Daily Visitor Count" > 900

```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-041/attempt-01/sql/S37.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-041/attempt-01/sql/S37.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-041/attempt-01/results/S37.rows.jsonl)；完整：True；SHA256：`fada8b1888f3bb18d2790275ec0227685ee4361d07e907f4d1191d9b13bfa654`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "ur", "kind": "base", "block": null, "base_tables": ["usage_records"]}, {"alias": "acm", "kind": "base", "block": null, "base_tables": ["artifact_conservation_and_maint"]}, {"alias": "gi", "kind": "base", "block": null, "base_tables": ["gallery_information"]}] | [{"type": "INNER", "right": "artifact_conservation_and_maint AS acm", "on": "TRIM(acm.\"Preserve Cultural Relic Reference\") = TRIM(ur.\"Cultural Relic Reference Number\")", "using": []}, {"type": "INNER", "right": "gallery_information AS gi", "on": "TRIM(gi.\"Exhibition Hall Record ID\") = TRIM(acm.\"Gallery Reference\")", "using": []}] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |

