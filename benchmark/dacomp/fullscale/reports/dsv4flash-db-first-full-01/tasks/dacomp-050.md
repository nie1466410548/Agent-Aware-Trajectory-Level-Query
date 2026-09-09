# dacomp-050

Within the student group, what are the characteristics of those who have had suicidal thou…

运行：已提交。官方未评分。全部 SQL 尝试/成功 32/32；数据 SQL 30/30；Python 16 次。

完整原题：

Within the student group, what are the characteristics of those who have had suicidal thoughts across the economic, academic stress, and diet/sleep dimensions, and how can relapse prevention strategies be devised accordingly?

| 表 | 行数 | 列数 |
| --- | --- | --- |
| sheet1 | 93800 | 19 |


实际路线（分析者依据 SQL/源码概括，不代表 Agent 自述）：SQL 汇总学生压力、饮食与睡眠特征及交叉比例 → Python 拟合逻辑回归并生成图表。

数据库大小：20,639,744 字节。

## 数据 SQL

| SQL | 状态 | 基础表 | Join 输入/类型 | GROUP BY | 聚合表达式 | 结果行数 | 数据库 ms |
| --- | --- | --- | --- | --- | --- | --- | --- |
| [S3/Q1](#s3) | success | ["sheet1"] | 0 / {} | [] | [] | 10 | 0.345 |
| [S4/Q2](#s4) | success | ["sheet1"] | 0 / {} | [] | ["COUNT(*)"] | 1 | 4.222 |
| [S5/Q3](#s5) | success | ["sheet1"] | 0 / {} | ["\"Working professional or student\""] | ["COUNT(*)"] | 3 | 46.409 |
| [S6/Q4](#s6) | success | ["sheet1"] | 0 / {} | ["\"Have you ever had suicidal thoughts?\""] | ["COUNT(*)"] | 3 | 53.784 |
| [S7/Q5](#s7) | success | ["sheet1"] | 0 / {} | ["\"Have you ever had suicidal thoughts?\""] | ["COUNT(*)"] | 2 | 13.63 |
| [S8/Q6](#s8) | success | ["sheet1"] | 0 / {} | ["Gender"] | ["COUNT(*)"] | 2 | 13.068 |
| [S9/Q7](#s9) | success | ["sheet1"] | 0 / {} | [] | [] | 4 | 17.181 |
| [S10/Q8](#s10) | success | ["sheet1"] | 0 / {} | [] | [] | 9 | 11.123 |
| [S11/Q9](#s11) | success | ["sheet1"] | 0 / {} | ["\"Have you ever had suicidal thoughts?\""] | ["COUNT(*)", "AVG(\"Academic stress\")", "AVG(\"Financial stress\")", "AVG(\"Cumulative GPA (CGPA)\")", "AVG(\"Satisfaction with studies\")", "AVG(\"Work/study hours\")", "AVG(Age)"] | 2 | 21.105 |
| [S12/Q10](#s12) | success | ["sheet1"] | 0 / {} | ["\"Have you ever had suicidal thoughts?\"", "\"Sleep duration\""] | ["COUNT(*)"] | 8 | 20.843 |
| [S13/Q11](#s13) | success | ["sheet1"] | 0 / {} | ["\"Have you ever had suicidal thoughts?\"", "\"Dietary habits\""] | ["COUNT(*)"] | 14 | 20.052 |
| [S14/Q12](#s14) | success | ["sheet1"] | 0 / {} | ["\"Sleep duration\""] | ["COUNT(*)", "SUM(CASE WHEN suicidal = 'Yes' THEN 1 ELSE 0 END)", "COUNT(*)", "SUM(CASE WHEN suicidal = 'Yes' THEN 1 ELSE 0 END)"] | 4 | 16.406 |
| [S15/Q13](#s15) | success | ["sheet1"] | 0 / {} | ["CASE WHEN \"Dietary habits\" IN ('Healthy', 'Moderate', 'Unhealthy') THEN \"Dietary habits\" ELSE 'Other/Unknown' END"] | ["COUNT(*)", "SUM(CASE WHEN suicidal = 'Yes' THEN 1 ELSE 0 END)", "COUNT(*)", "SUM(CASE WHEN suicidal = 'Yes' THEN 1 ELSE 0 END)"] | 4 | 18.519 |
| [S16/Q14](#s16) | success | ["sheet1"] | 0 / {} | ["CASE WHEN \"Academic stress\" <= 2 THEN 'Low (1-2)' WHEN \"Academic stress\" = 3 THEN 'Medium (3)' ELSE 'High (4-5)' END"] | ["COUNT(*)", "SUM(CASE WHEN suicidal = 'Yes' THEN 1 ELSE 0 END)", "COUNT(*)", "SUM(CASE WHEN suicidal = 'Yes' THEN 1 ELSE 0 END)"] | 3 | 17.222 |
| [S17/Q15](#s17) | success | ["sheet1"] | 0 / {} | ["CASE WHEN \"Financial stress\" <= 2 THEN 'Low (1-2)' WHEN \"Financial stress\" = 3 THEN 'Medium (3)' ELSE 'High (4-5)' END"] | ["COUNT(*)", "SUM(CASE WHEN suicidal = 'Yes' THEN 1 ELSE 0 END)", "COUNT(*)", "SUM(CASE WHEN suicidal = 'Yes' THEN 1 ELSE 0 END)"] | 3 | 17.003 |
| [S18/Q16](#s18) | success | ["sheet1"] | 0 / {} | ["Gender"] | ["COUNT(*)", "SUM(CASE WHEN suicidal = 'Yes' THEN 1 ELSE 0 END)", "COUNT(*)", "SUM(CASE WHEN suicidal = 'Yes' THEN 1 ELSE 0 END)"] | 2 | 15.459 |
| [S19/Q17](#s19) | success | ["sheet1"] | 0 / {} | ["\"Family history of mental illness\""] | ["COUNT(*)", "SUM(CASE WHEN suicidal = 'Yes' THEN 1 ELSE 0 END)", "COUNT(*)", "SUM(CASE WHEN suicidal = 'Yes' THEN 1 ELSE 0 END)"] | 2 | 15.774 |
| [S20/Q18](#s20) | success | ["sheet1"] | 0 / {} | ["CASE WHEN \"Satisfaction with studies\" <= 2 THEN 'Low (1-2)' WHEN \"Satisfaction with studies\" = 3 THEN 'Medium (3)' ELSE 'High (4-5)' END"] | ["COUNT(*)", "SUM(CASE WHEN suicidal = 'Yes' THEN 1 ELSE 0 END)", "COUNT(*)", "SUM(CASE WHEN suicidal = 'Yes' THEN 1 ELSE 0 END)"] | 3 | 17.169 |
| [S21/Q19](#s21) | success | ["sheet1"] | 0 / {} | ["CASE WHEN \"Work/study hours\" <= 6 THEN '≤6 hrs' WHEN \"Work/study hours\" <= 8 THEN '7-8 hrs' ELSE '9+ hrs' END"] | ["COUNT(*)", "SUM(CASE WHEN suicidal = 'Yes' THEN 1 ELSE 0 END)", "COUNT(*)", "SUM(CASE WHEN suicidal = 'Yes' THEN 1 ELSE 0 END)"] | 3 | 17.401 |
| [S22/Q20](#s22) | success | ["sheet1"] | 0 / {} | ["CASE WHEN \"Cumulative GPA (CGPA)\" < 6 THEN 'CGPA < 6' WHEN \"Cumulative GPA (CGPA)\" < 7.5 THEN 'CGPA 6-7.49' WHEN \"Cumulative GPA (CGPA)\" < 8.5 THEN 'CGPA 7.5-8.49' ELSE 'CGPA ≥ 8.5' END"] | ["COUNT(*)", "SUM(CASE WHEN suicidal = 'Yes' THEN 1 ELSE 0 END)", "COUNT(*)", "SUM(CASE WHEN suicidal = 'Yes' THEN 1 ELSE 0 END)"] | 4 | 17.839 |
| [S23/Q21](#s23) | success | ["sheet1"] | 0 / {} | ["Degree"] | ["COUNT(*)", "SUM(CASE WHEN suicidal = 'Yes' THEN 1 ELSE 0 END)", "COUNT(*)", "SUM(CASE WHEN suicidal = 'Yes' THEN 1 ELSE 0 END)"] | 15 | 20.9 |
| [S24/Q22](#s24) | success | ["sheet1"] | 0 / {} | ["CASE WHEN \"Academic stress\" >= 4 AND \"Financial stress\" >= 4 THEN 'High both' WHEN \"Academic stress\" >= 4 OR \"Financial stress\" >= 4 THEN 'High one' ELSE 'Neither high' END"] | ["COUNT(*)", "SUM(CASE WHEN suicidal = 'Yes' THEN 1 ELSE 0 END)", "COUNT(*)", "SUM(CASE WHEN suicidal = 'Yes' THEN 1 ELSE 0 END)"] | 3 | 18.704 |
| [S25/Q23](#s25) | success | ["sheet1"] | 0 / {} | ["\"Dietary habits\"", "CASE WHEN \"Sleep duration\" = 'Less than 5 hours' THEN 'Sleep<5h' ELSE 'Sleep>=5h' END"] | ["COUNT(*)", "SUM(CASE WHEN suicidal = 'Yes' THEN 1 ELSE 0 END)", "COUNT(*)", "SUM(CASE WHEN suicidal = 'Yes' THEN 1 ELSE 0 END)"] | 6 | 23.746 |
| [S26/Q24](#s26) | success | ["sheet1"] | 0 / {} | ["CASE WHEN Age < 20 THEN '<20' WHEN Age <= 24 THEN '20-24' WHEN Age <= 29 THEN '25-29' ELSE '30+' END"] | ["COUNT(*)", "SUM(CASE WHEN \"Have you ever had suicidal thoughts?\" = 'Yes' THEN 1 ELSE 0 END)", "COUNT(*)", "SUM(CASE WHEN \"Have you ever had suicidal thoughts?\" = 'Yes' THEN 1 ELSE 0 END)"] | 4 | 18.037 |
| [S27/Q25](#s27) | success | ["sheet1"] | 0 / {} | [] | ["MIN(Age)", "MAX(Age)", "AVG(Age)"] | 1 | 10.812 |
| [S28/Q26](#s28) | success | ["sheet1"] | 0 / {} | [] | [] | 18746 | 50.167 |
| [S29/Q27](#s29) | success | ["sheet1"] | 0 / {} | ["n_risk"] | ["COUNT(*)", "SUM(CASE WHEN suicidal = 'Yes' THEN 1 ELSE 0 END)", "COUNT(*)", "SUM(CASE WHEN suicidal = 'Yes' THEN 1 ELSE 0 END)"] | 5 | 23.585 |
| [S30/Q28](#s30) | success | ["sheet1"] | 0 / {} | ["CASE WHEN n_risk >= 3 THEN '3-4 risk factors' WHEN n_risk = 2 THEN '2 risk factors' WHEN n_risk = 1 THEN '1 risk factor' ELSE '0 risk factors' END"] | ["COUNT(*)", "SUM(CASE WHEN suicidal = 'Yes' THEN 1 ELSE 0 END)", "COUNT(*)", "SUM(CASE WHEN suicidal = 'Yes' THEN 1 ELSE 0 END)"] | 4 | 30.103 |
| [S31/Q29](#s31) | success | ["sheet1"] | 0 / {} | [] | ["COUNT(*)", "COUNT(*)", "COUNT(*)", "COUNT(*)", "COUNT(*)", "SUM(CASE WHEN \"Academic stress\" >= 4 THEN 1 ELSE 0 END)", "SUM(CASE WHEN \"Financial stress\" >= 4 THEN 1 ELSE 0 END)", "SUM(CASE WHEN \"Dietary habits\" = 'Unhealthy' THEN 1 ELSE 0 END)", "SUM(CASE WHEN \"Sleep duration\" = 'Less than 5 hours' THEN 1 ELSE 0 END)"] | 1 | 17.16 |
| [S32/Q30](#s32) | success | ["sheet1"] | 0 / {} | [] | ["COUNT(*)", "COUNT(*)", "SUM(CASE WHEN \"Academic stress\" >= 4 AND \"Financial stress\" >= 4 THEN 1 ELSE 0 END)", "SUM(CASE WHEN (\"Academic stress\" >= 4 OR \"Financial stress\" >= 4) AND \"Dietary habits\" = 'Unhealthy' AND \"Sleep duration\" = 'Less than 5 hours' THEN 1 ELSE 0 END)"] | 1 | 15.571 |


## 元数据和设置

| SQL | 类别 | 状态 | 内容 |
| --- | --- | --- | --- |
| S1 | connection_setup | success | PRAGMA query_only=ON |
| S2 | metadata | success | SELECT name,sql FROM sqlite_master WHERE type='table' ORDER BY name |


## Python 与执行位置

人工源码审查：**reviewed_SQL_dominant_with_statistical_model_preprocessing**。描述性计数、分层比例和交叉汇总在 SQL 内完成。Python 主要用于逻辑回归、编码、模型矩阵的有限值筛选、标准化与绘图；均值出现于损失函数或模型预处理，不能据此判为明细聚合迁出。分类编码和有限值筛选也可提前在 SQL 完成，记录为建模预处理边界。 [证据](../reviews/dacomp-050.json)。

P1：Logistic regression is a statistical estimation procedure not supported by SQLite. I use the pre-filtered student rows (S28) to fit a model quantifying independent associations between economic (financial stress), academic stress, diet/sleep factors and suicidal ideation, with standardized effect sizes and predicted probabilities.

[源码](../../../runs/dsv4flash-db-first-full-01/dacomp-050/attempt-01/python/P1.py)；[输出](../../../runs/dsv4flash-db-first-full-01/dacomp-050/attempt-01/python/P1.stdout)；[错误](../../../runs/dsv4flash-db-first-full-01/dacomp-050/attempt-01/python/P1.stderr)。自动源码筛查未检出预设迁出信号；这不是全面语义合规证明。

P2：Logistic regression to quantify independent associations of economic (financial stress), academic stress, diet/sleep with suicidal ideation, controlling for age, gender, family history. SQLite cannot perform this iterative statistical estimation.

[源码](../../../runs/dsv4flash-db-first-full-01/dacomp-050/attempt-01/python/P2.py)；[输出](../../../runs/dsv4flash-db-first-full-01/dacomp-050/attempt-01/python/P2.stdout)；[错误](../../../runs/dsv4flash-db-first-full-01/dacomp-050/attempt-01/python/P2.stderr)。自动源码筛查未检出预设迁出信号；这不是全面语义合规证明。

P3：Logistic regression to quantify independent associations of economic (financial stress), academic stress, diet/sleep with suicidal ideation, controlling for age, gender, family history. SQLite cannot perform this iterative statistical estimation; data was pre-filtered to students via SQL (S28).

[源码](../../../runs/dsv4flash-db-first-full-01/dacomp-050/attempt-01/python/P3.py)；[输出](../../../runs/dsv4flash-db-first-full-01/dacomp-050/attempt-01/python/P3.stdout)；[错误](../../../runs/dsv4flash-db-first-full-01/dacomp-050/attempt-01/python/P3.stderr)。自动源码筛查未检出预设迁出信号；这不是全面语义合规证明。

P4：Inspect the structure of the archived rows to fix column mapping before fitting the logistic regression.

[源码](../../../runs/dsv4flash-db-first-full-01/dacomp-050/attempt-01/python/P4.py)；[输出](../../../runs/dsv4flash-db-first-full-01/dacomp-050/attempt-01/python/P4.stdout)；[错误](../../../runs/dsv4flash-db-first-full-01/dacomp-050/attempt-01/python/P4.stderr)。自动源码筛查未检出预设迁出信号；这不是全面语义合规证明。

P5：Logistic regression fitting with proper column mapping from row arrays. The data was pre-filtered to students via SQL (S28); fitting is a statistical procedure not supported by SQLite.

[源码](../../../runs/dsv4flash-db-first-full-01/dacomp-050/attempt-01/python/P5.py)；[输出](../../../runs/dsv4flash-db-first-full-01/dacomp-050/attempt-01/python/P5.stdout)；[错误](../../../runs/dsv4flash-db-first-full-01/dacomp-050/attempt-01/python/P5.stderr)。自动源码筛查未检出预设迁出信号；这不是全面语义合规证明。

P6：Debugging the logistic regression convergence issue - checking data scale and baseline prevalence.

[源码](../../../runs/dsv4flash-db-first-full-01/dacomp-050/attempt-01/python/P6.py)；[输出](../../../runs/dsv4flash-db-first-full-01/dacomp-050/attempt-01/python/P6.stdout)；[错误](../../../runs/dsv4flash-db-first-full-01/dacomp-050/attempt-01/python/P6.stderr)。自动源码筛查未检出预设迁出信号；这不是全面语义合规证明。

P7：Fixing the logistic regression by dropping rows with any missing values (Satisfaction with studies had 2 NaN), which caused NaN likelihood. SQLite can't fit this model; data already filtered to students via SQL.

[源码](../../../runs/dsv4flash-db-first-full-01/dacomp-050/attempt-01/python/P7.py)；[输出](../../../runs/dsv4flash-db-first-full-01/dacomp-050/attempt-01/python/P7.stdout)；[错误](../../../runs/dsv4flash-db-first-full-01/dacomp-050/attempt-01/python/P7.stderr)。自动源码筛查未检出预设迁出信号；这不是全面语义合规证明。

P8：Refitting logistic regression with analytic gradient/Hessian for numerically correct standard errors and scenario predictions. This is a statistical estimation procedure not supported by SQLite.

[源码](../../../runs/dsv4flash-db-first-full-01/dacomp-050/attempt-01/python/P8.py)；[输出](../../../runs/dsv4flash-db-first-full-01/dacomp-050/attempt-01/python/P8.stdout)；[错误](../../../runs/dsv4flash-db-first-full-01/dacomp-050/attempt-01/python/P8.stderr)。自动源码筛查未检出预设迁出信号；这不是全面语义合规证明。

P9：Diagnosing the unexpectedly large standard errors by examining Hessian conditioning and gradient norm at the optimum; verifying the logistic regression fit is numerically sound.

[源码](../../../runs/dsv4flash-db-first-full-01/dacomp-050/attempt-01/python/P9.py)；[输出](../../../runs/dsv4flash-db-first-full-01/dacomp-050/attempt-01/python/P9.stdout)；[错误](../../../runs/dsv4flash-db-first-full-01/dacomp-050/attempt-01/python/P9.stderr)。检出需人工核验的 SQL 可实现操作：sort_values(；不能仅凭理由判为合规。

P10：Correcting the standard error computation: the observed information matrix must be the sum (not the mean) over observations; SEs were inflated by factor sqrt(n).

[源码](../../../runs/dsv4flash-db-first-full-01/dacomp-050/attempt-01/python/P10.py)；[输出](../../../runs/dsv4flash-db-first-full-01/dacomp-050/attempt-01/python/P10.stdout)；[错误](../../../runs/dsv4flash-db-first-full-01/dacomp-050/attempt-01/python/P10.stderr)。自动源码筛查未检出预设迁出信号；这不是全面语义合规证明。

P11：Creating summary visualizations from the archived SQL aggregate results (S14-S17, S29) — plotting suicidal-ideation prevalence gradients by academic stress, financial stress, diet, sleep, and risk-factor count to support the report.

[源码](../../../runs/dsv4flash-db-first-full-01/dacomp-050/attempt-01/python/P11.py)；[输出](../../../runs/dsv4flash-db-first-full-01/dacomp-050/attempt-01/python/P11.stdout)；[错误](../../../runs/dsv4flash-db-first-full-01/dacomp-050/attempt-01/python/P11.stderr)。自动源码筛查未检出预设迁出信号；这不是全面语义合规证明。

P12：Debugging the plot data preparation - inspecting the diet×sleep cross-tab archived data before re-plotting the summary figures.

[源码](../../../runs/dsv4flash-db-first-full-01/dacomp-050/attempt-01/python/P12.py)；[输出](../../../runs/dsv4flash-db-first-full-01/dacomp-050/attempt-01/python/P12.stdout)；[错误](../../../runs/dsv4flash-db-first-full-01/dacomp-050/attempt-01/python/P12.stderr)。自动源码筛查未检出预设迁出信号；这不是全面语义合规证明。

P13：Creating summary visualizations from archived SQL aggregate results. Plotting is a visualization step done in Python; all grouping/aggregation was performed in SQL and archived.

[源码](../../../runs/dsv4flash-db-first-full-01/dacomp-050/attempt-01/python/P13.py)；[输出](../../../runs/dsv4flash-db-first-full-01/dacomp-050/attempt-01/python/P13.stdout)；[错误](../../../runs/dsv4flash-db-first-full-01/dacomp-050/attempt-01/python/P13.stderr)。自动源码筛查未检出预设迁出信号；这不是全面语义合规证明。

P14：Debugging label matching for the visualization data before plotting the summary figures.

[源码](../../../runs/dsv4flash-db-first-full-01/dacomp-050/attempt-01/python/P14.py)；[输出](../../../runs/dsv4flash-db-first-full-01/dacomp-050/attempt-01/python/P14.stdout)；[错误](../../../runs/dsv4flash-db-first-full-01/dacomp-050/attempt-01/python/P14.stderr)。自动源码筛查未检出预设迁出信号；这不是全面语义合规证明。

P15：Creating the summary visualizations from archived SQL aggregates. The earlier attempt had a slice bug excluding the 'Healthy' diet group; plotting is a Python visualization step over SQL-produced aggregates.

[源码](../../../runs/dsv4flash-db-first-full-01/dacomp-050/attempt-01/python/P15.py)；[输出](../../../runs/dsv4flash-db-first-full-01/dacomp-050/attempt-01/python/P15.stdout)；[错误](../../../runs/dsv4flash-db-first-full-01/dacomp-050/attempt-01/python/P15.stderr)。自动源码筛查未检出预设迁出信号；这不是全面语义合规证明。

P16：Verifying the saved figures are valid image files before referencing them in the report.

[源码](../../../runs/dsv4flash-db-first-full-01/dacomp-050/attempt-01/python/P16.py)；[输出](../../../runs/dsv4flash-db-first-full-01/dacomp-050/attempt-01/python/P16.stdout)；[错误](../../../runs/dsv4flash-db-first-full-01/dacomp-050/attempt-01/python/P16.stderr)。自动源码筛查未检出预设迁出信号；这不是全面语义合规证明。

## 优化机会

已验证候选。筛选限于精确 SQL、相同自包含 CTE、相同单表完整过滤、可分解单表聚合；未覆盖任意 Join 等价和一般谓词蕴含。全部候选都是 offline，未测在线预测。

| 候选 | 类型 | 已有结果 | 覆盖 SQL | 后续次数 | 中间行数 | 验证 | 成本 |
| --- | --- | --- | --- | --- | --- | --- | --- |
| C1 | common subexpression | False | ["S14", "S15", "S16", "S17", "S18", "S19", "S20", "S21", "S22", "S23", "S24"] | 10 | 18762 | verified | Not benchmarked; correctness alone does not establish net speedup. |
| C2 | common subexpression | False | ["S29", "S30"] | 1 | unknown | not_verified_cap | Not tested |
| C3 | common subexpression | False | ["S31", "S32"] | 1 | unknown | not_verified_cap | Not tested |
| C4 | aggregate MV | False | ["S4", "S5", "S6"] | 2 | unknown | not_verified_cap | Not tested |
| C5 | common filtered view | False | ["S7", "S8", "S9", "S10", "S11", "S12", "S13", "S26", "S27"] | 8 | 18762 | verified | Not benchmarked; correctness alone does not establish net speedup. |
| C6 | aggregate MV | False | ["S7", "S8", "S11", "S12", "S13", "S26", "S27"] | 6 | 201 | verified | Not benchmarked; correctness alone does not establish net speedup. |


已验证覆盖（含触发查询、候选并集去重）：20/30 条成功数据 SQL。正确性仅针对当前数据库快照；未测性能的候选不能声称已加速。

[完整 build/rewrite 与比较证据](dacomp-050.analysis.json)。

### C1：common subexpression

Identical self-contained CTE body across queries.

原查询 [S14](#s14), [S15](#s15), [S16](#s16), [S17](#s17), [S18](#s18), [S19](#s19), [S20](#s20), [S21](#s21), [S22](#s22), [S23](#s23), [S24](#s24) → 新增共享状态 C1 → 后续 10 次可复用。该构建点为事后假设，不代表 Agent 当时预知后续。

构建定义：

```sql
SELECT *, "Have you ever had suicidal thoughts?" AS suicidal FROM sheet1 WHERE "Working professional or student" = 'Student'
```

受益查询 S14 的改写示例：

```sql
WITH stu AS (SELECT * FROM temp.reuse_candidate) SELECT "Sleep duration", COUNT(*) AS total, SUM(CASE WHEN suicidal = 'Yes' THEN 1 ELSE 0 END) AS yes_n, ROUND(100.0 * SUM(CASE WHEN suicidal = 'Yes' THEN 1 ELSE 0 END) / COUNT(*), 1) AS yes_pct FROM stu GROUP BY "Sleep duration" ORDER BY yes_pct DESC
```

| 原 SQL | 列名一致 | 结果一致 | 比较方法 |
| --- | --- | --- | --- |
| S14 | True | True | ordered_numeric_tolerance |
| S15 | True | True | ordered_numeric_tolerance |
| S16 | True | True | ordered_numeric_tolerance |
| S17 | True | True | ordered_numeric_tolerance |
| S18 | True | True | ordered_numeric_tolerance |
| S19 | True | True | ordered_numeric_tolerance |
| S20 | True | True | ordered_numeric_tolerance |
| S21 | True | True | ordered_numeric_tolerance |
| S22 | True | True | ordered_numeric_tolerance |
| S23 | True | True | ordered_numeric_tolerance |
| S24 | True | True | ordered_numeric_tolerance |


验证状态：verified；成本结论：Not benchmarked; correctness alone does not establish net speedup.

### C5：common filtered view

Same single source and complete filter; original filter retained.

原查询 [S7](#s7), [S8](#s8), [S9](#s9), [S10](#s10), [S11](#s11), [S12](#s12), [S13](#s13), [S26](#s26), [S27](#s27) → 新增共享状态 C5 → 后续 8 次可复用。该构建点为事后假设，不代表 Agent 当时预知后续。

构建定义：

```sql
SELECT * FROM "sheet1" WHERE "Working professional or student" = 'Student'
```

受益查询 S7 的改写示例：

```sql
SELECT "Have you ever had suicidal thoughts?" AS suicidal, COUNT(*) AS n FROM temp.reuse_candidate AS sheet1 WHERE "Working professional or student" = 'Student' GROUP BY suicidal
```

| 原 SQL | 列名一致 | 结果一致 | 比较方法 |
| --- | --- | --- | --- |
| S7 | True | True | exact_multiset |
| S8 | True | True | exact_multiset |
| S9 | True | True | exact_multiset |
| S10 | True | True | exact_multiset |
| S11 | True | True | exact_multiset |
| S12 | True | True | ordered_numeric_tolerance |
| S13 | True | True | ordered_numeric_tolerance |
| S26 | True | True | ordered_numeric_tolerance |
| S27 | True | True | exact_multiset |


验证状态：verified；成本结论：Not benchmarked; correctness alone does not establish net speedup.

### C6：aggregate MV

Union of grouping keys; decomposable aggregate states; AVG uses SUM and non-NULL COUNT.

原查询 [S7](#s7), [S8](#s8), [S11](#s11), [S12](#s12), [S13](#s13), [S26](#s26), [S27](#s27) → 新增共享状态 C6 → 后续 6 次可复用。该构建点为事后假设，不代表 Agent 当时预知后续。

构建定义：

```sql
SELECT "Have you ever had suicidal thoughts?" AS __g0, gender AS __g1, "Sleep duration" AS __g2, "Dietary habits" AS __g3, CASE WHEN age < 20 THEN '<20' WHEN age <= 24 THEN '20-24' WHEN age <= 29 THEN '25-29' ELSE '30+' END AS __g4, COUNT(*) AS __a0, SUM("Academic stress") AS __a1_sum, COUNT("Academic stress") AS __a1_n, SUM("Financial stress") AS __a2_sum, COUNT("Financial stress") AS __a2_n, SUM("Cumulative GPA (CGPA)") AS __a3_sum, COUNT("Cumulative GPA (CGPA)") AS __a3_n, SUM("Satisfaction with studies") AS __a4_sum, COUNT("Satisfaction with studies") AS __a4_n, SUM("Work/study hours") AS __a5_sum, COUNT("Work/study hours") AS __a5_n, SUM(age) AS __a6_sum, COUNT(age) AS __a6_n, SUM(CASE WHEN "Have you ever had suicidal thoughts?" = 'Yes' THEN 1 ELSE 0 END) AS __a7, MIN(age) AS __a8, MAX(age) AS __a9 FROM "sheet1" WHERE "Working professional or student" = 'Student' GROUP BY "Have you ever had suicidal thoughts?", gender, "Sleep duration", "Dietary habits", CASE WHEN age < 20 THEN '<20' WHEN age <= 24 THEN '20-24' WHEN age <= 29 THEN '25-29' ELSE '30+' END
```

受益查询 S7 的改写示例：

```sql
SELECT __g0 AS suicidal, SUM(__a0) AS n FROM temp.reuse_candidate GROUP BY __g0
```

| 原 SQL | 列名一致 | 结果一致 | 比较方法 |
| --- | --- | --- | --- |
| S7 | True | True | exact_multiset |
| S8 | True | True | exact_multiset |
| S11 | True | True | exact_multiset |
| S12 | True | True | ordered_numeric_tolerance |
| S13 | True | True | ordered_numeric_tolerance |
| S26 | True | True | ordered_numeric_tolerance |
| S27 | True | True | exact_multiset |


验证状态：verified；成本结论：Not benchmarked; correctness alone does not establish net speedup.

结果依赖：自动记录 SQL→Python 的接口父调用，以及源码中引用归档文件的消费者；字面值相同不认定因果。模型方向选择需要人工读取消息，尚未做全面因果标注。

[原始报告](../../../runs/dsv4flash-db-first-full-01/dacomp-050/attempt-01/answer.md)；[统一消息](../../../runs/dsv4flash-db-first-full-01/dacomp-050/attempt-01/messages.jsonl)；[原始 OpenCode 事件](../../../runs/dsv4flash-db-first-full-01/dacomp-050/attempt-01/opencode.jsonl)；[SQL 引擎日志](../../../runs/dsv4flash-db-first-full-01/dacomp-050/attempt-01/sql_journal.jsonl)。

[可读报告（本地图片链接规范化）](../answers/dacomp-050.md)。原始回答保留，分析结论未改写。

## S1

类别 `connection_setup`；来源 `connection`；调用 `5975fd24129b44d59d8a3d4f86c7adb5`；状态 `success`。

```sql
PRAGMA query_only=ON
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-050/attempt-01/sql/S1.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-050/attempt-01/sql/S1.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-050/attempt-01/results/S1.rows.jsonl)；完整：True；SHA256：`e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`。

## S2

类别 `metadata`；来源 `list_db`；调用 `5975fd24129b44d59d8a3d4f86c7adb5`；状态 `success`。

```sql
SELECT name,sql FROM sqlite_master WHERE type='table' ORDER BY name
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-050/attempt-01/sql/S2.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-050/attempt-01/sql/S2.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-050/attempt-01/results/S2.rows.jsonl)；完整：True；SHA256：`e286799e56656c00b1f2aa3ee23fd26935cce617ea29fbed1f1cf3cafc987e01`。

## S3

类别 `data`；来源 `query_db`；调用 `a0f0bf424d20458aa2b1a2bdf70d36e3`；状态 `success`。

```sql
SELECT * FROM sheet1 LIMIT 10
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-050/attempt-01/sql/S3.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-050/attempt-01/sql/S3.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-050/attempt-01/results/S3.rows.jsonl)；完整：True；SHA256：`252b182731409e1d915ca2b6b0b3b4ae307c9bdd4202d70ae73f305fd121133f`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "sheet1", "kind": "base", "block": null, "base_tables": ["sheet1"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |


## S4

类别 `data`；来源 `query_db`；调用 `3fcba429014146c9a254082ba97013a7`；状态 `success`。

```sql
SELECT COUNT(*) AS total_rows FROM sheet1
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-050/attempt-01/sql/S4.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-050/attempt-01/sql/S4.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-050/attempt-01/results/S4.rows.jsonl)；完整：True；SHA256：`f23d25deefa5689b12cf442fe086e4a5fb25b748013fc7c629a27e81eb5c97f1`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "sheet1", "kind": "base", "block": null, "base_tables": ["sheet1"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |


## S5

类别 `data`；来源 `query_db`；调用 `4e14c3410da544c9b26d80bd405e67ba`；状态 `success`。

```sql
SELECT "Working professional or student" AS status, COUNT(*) AS n FROM sheet1 GROUP BY status
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-050/attempt-01/sql/S5.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-050/attempt-01/sql/S5.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-050/attempt-01/results/S5.rows.jsonl)；完整：True；SHA256：`840b1fe8804c2b73d49b6bf67b1eb1b4a02345d540e78899aa0ab0ced3e33d05`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "sheet1", "kind": "base", "block": null, "base_tables": ["sheet1"]}] | [] | ["\"Working professional or student\""] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |


## S6

类别 `data`；来源 `query_db`；调用 `70b277ce4d46445b99210354521183de`；状态 `success`。

```sql
SELECT "Have you ever had suicidal thoughts?" AS suicidal, COUNT(*) AS n FROM sheet1 GROUP BY suicidal
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-050/attempt-01/sql/S6.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-050/attempt-01/sql/S6.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-050/attempt-01/results/S6.rows.jsonl)；完整：True；SHA256：`92e0567a1a893a563eb39eca69355daba6dd9d827e9262bc9f1d20e36c8f714d`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "sheet1", "kind": "base", "block": null, "base_tables": ["sheet1"]}] | [] | ["\"Have you ever had suicidal thoughts?\""] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |


## S7

类别 `data`；来源 `query_db`；调用 `753bb94985cf4d87be868784d79a3d3b`；状态 `success`。

```sql
SELECT "Have you ever had suicidal thoughts?" AS suicidal, COUNT(*) AS n FROM sheet1 WHERE "Working professional or student" = 'Student' GROUP BY suicidal
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-050/attempt-01/sql/S7.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-050/attempt-01/sql/S7.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-050/attempt-01/results/S7.rows.jsonl)；完整：True；SHA256：`ef3e9b0ea71e801c62f9837e7c24046cf885c3716add20ea312750b24ff49ef6`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "sheet1", "kind": "base", "block": null, "base_tables": ["sheet1"]}] | [] | ["\"Have you ever had suicidal thoughts?\""] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |


## S8

类别 `data`；来源 `query_db`；调用 `ac2c99fadbce42d09c1b37be0b26333c`；状态 `success`。

```sql
SELECT Gender, COUNT(*) AS n FROM sheet1 WHERE "Working professional or student" = 'Student' GROUP BY Gender
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-050/attempt-01/sql/S8.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-050/attempt-01/sql/S8.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-050/attempt-01/results/S8.rows.jsonl)；完整：True；SHA256：`1bd5ea181f5269a2f899000d8863e85b1d6244a3195daa750f8c4b68625e7f76`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "sheet1", "kind": "base", "block": null, "base_tables": ["sheet1"]}] | [] | ["Gender"] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |


## S9

类别 `data`；来源 `query_db`；调用 `02c341518e1f4c36971cc1e04732483e`；状态 `success`。

```sql
SELECT DISTINCT "Sleep duration" FROM sheet1 WHERE "Working professional or student" = 'Student'
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-050/attempt-01/sql/S9.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-050/attempt-01/sql/S9.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-050/attempt-01/results/S9.rows.jsonl)；完整：True；SHA256：`242d9da1f69d7ef09ae9a7c11f386ed47b64dff16f77098ab6a5aec4b04f54d8`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "sheet1", "kind": "base", "block": null, "base_tables": ["sheet1"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |


## S10

类别 `data`；来源 `query_db`；调用 `b33a2c20379648c987ba5a8915f25cc5`；状态 `success`。

```sql
SELECT DISTINCT "Dietary habits" FROM sheet1 WHERE "Working professional or student" = 'Student'
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-050/attempt-01/sql/S10.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-050/attempt-01/sql/S10.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-050/attempt-01/results/S10.rows.jsonl)；完整：True；SHA256：`12911fae9eacc0abfc4b7885bbc1621fd77083dca6f6bee8817e388a85525ab4`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "sheet1", "kind": "base", "block": null, "base_tables": ["sheet1"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |


## S11

类别 `data`；来源 `query_db`；调用 `9c0e93d454854628920d491a0317a6c2`；状态 `success`。

```sql
SELECT 
  "Have you ever had suicidal thoughts?" AS suicidal,
  COUNT(*) AS n,
  ROUND(AVG("Academic stress"), 2) AS avg_academic_stress,
  ROUND(AVG("Financial stress"), 2) AS avg_financial_stress,
  ROUND(AVG("Cumulative GPA (CGPA)"), 2) AS avg_cgpa,
  ROUND(AVG("Satisfaction with studies"), 2) AS avg_study_satisfaction,
  ROUND(AVG("Work/study hours"), 2) AS avg_study_hours,
  ROUND(AVG(Age), 2) AS avg_age
FROM sheet1 
WHERE "Working professional or student" = 'Student'
GROUP BY suicidal
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-050/attempt-01/sql/S11.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-050/attempt-01/sql/S11.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-050/attempt-01/results/S11.rows.jsonl)；完整：True；SHA256：`1f575004580dc07debe4b8477e63e2c1a62c943e67683472e71791fe623de8b5`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "sheet1", "kind": "base", "block": null, "base_tables": ["sheet1"]}] | [] | ["\"Have you ever had suicidal thoughts?\""] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |
| B1 | AVG("Academic stress") | [{"table": "sheet1", "column": "Academic stress"}] | [] | False |
| B1 | AVG("Financial stress") | [{"table": "sheet1", "column": "Financial stress"}] | [] | False |
| B1 | AVG("Cumulative GPA (CGPA)") | [{"table": "sheet1", "column": "Cumulative GPA (CGPA)"}] | [] | False |
| B1 | AVG("Satisfaction with studies") | [{"table": "sheet1", "column": "Satisfaction with studies"}] | [] | False |
| B1 | AVG("Work/study hours") | [{"table": "sheet1", "column": "Work/study hours"}] | [] | False |
| B1 | AVG(Age) | [{"table": "sheet1", "column": "Age"}] | [] | False |


## S12

类别 `data`；来源 `query_db`；调用 `4794f2b0d30545028858aefad7fedf79`；状态 `success`。

```sql
SELECT 
  "Have you ever had suicidal thoughts?" AS suicidal,
  "Sleep duration",
  COUNT(*) AS n
FROM sheet1 
WHERE "Working professional or student" = 'Student'
GROUP BY suicidal, "Sleep duration"
ORDER BY suicidal, "Sleep duration"
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-050/attempt-01/sql/S12.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-050/attempt-01/sql/S12.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-050/attempt-01/results/S12.rows.jsonl)；完整：True；SHA256：`b2aa08eea3f4f5dfd1bfd05d96d8f736d784493250c5918118c1cd8e4c37560d`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "sheet1", "kind": "base", "block": null, "base_tables": ["sheet1"]}] | [] | ["\"Have you ever had suicidal thoughts?\"", "\"Sleep duration\""] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |


## S13

类别 `data`；来源 `query_db`；调用 `14c30e695ca4429eb7036a83bbe1ec2f`；状态 `success`。

```sql
SELECT 
  "Have you ever had suicidal thoughts?" AS suicidal,
  "Dietary habits",
  COUNT(*) AS n
FROM sheet1 
WHERE "Working professional or student" = 'Student'
GROUP BY suicidal, "Dietary habits"
ORDER BY suicidal, "Dietary habits"
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-050/attempt-01/sql/S13.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-050/attempt-01/sql/S13.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-050/attempt-01/results/S13.rows.jsonl)；完整：True；SHA256：`43a5be821e202b7078b7bdeea6d45a215618cfe022d9d0cc0f44430a3caf90c2`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "sheet1", "kind": "base", "block": null, "base_tables": ["sheet1"]}] | [] | ["\"Have you ever had suicidal thoughts?\"", "\"Dietary habits\""] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |


## S14

类别 `data`；来源 `query_db`；调用 `3d0af080180944d883a1de0016cfaef5`；状态 `success`。

```sql
WITH stu AS (
  SELECT *, "Have you ever had suicidal thoughts?" AS suicidal FROM sheet1 WHERE "Working professional or student" = 'Student'
)
SELECT 
  "Sleep duration",
  COUNT(*) AS total,
  SUM(CASE WHEN suicidal='Yes' THEN 1 ELSE 0 END) AS yes_n,
  ROUND(100.0*SUM(CASE WHEN suicidal='Yes' THEN 1 ELSE 0 END)/COUNT(*),1) AS yes_pct
FROM stu
GROUP BY "Sleep duration"
ORDER BY yes_pct DESC
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-050/attempt-01/sql/S14.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-050/attempt-01/sql/S14.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-050/attempt-01/results/S14.rows.jsonl)；完整：True；SHA256：`65206ab43f01432caca531b6a979f6fea24e91a1a817666c4b39efe62a1bd118`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "sheet1", "kind": "base", "block": null, "base_tables": ["sheet1"]}] | [] | [] |
| B2 | [{"alias": "stu", "kind": "derived", "block": "B1", "base_tables": ["sheet1"]}] | [] | ["\"Sleep duration\""] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B2 | COUNT(*) | [] | [] | True |
| B2 | SUM(CASE WHEN suicidal = 'Yes' THEN 1 ELSE 0 END) | [] | [{"table": "sheet1", "column": "Have you ever had suicidal thoughts?"}] | False |
| B2 | COUNT(*) | [] | [] | True |
| B2 | SUM(CASE WHEN suicidal = 'Yes' THEN 1 ELSE 0 END) | [] | [{"table": "sheet1", "column": "Have you ever had suicidal thoughts?"}] | False |


## S15

类别 `data`；来源 `query_db`；调用 `b170ddc47b0a47af819ef791649709fb`；状态 `success`。

```sql
WITH stu AS (
  SELECT *, "Have you ever had suicidal thoughts?" AS suicidal FROM sheet1 WHERE "Working professional or student" = 'Student'
)
SELECT 
  CASE WHEN "Dietary habits" IN ('Healthy','Moderate','Unhealthy') THEN "Dietary habits" ELSE 'Other/Unknown' END AS diet_group,
  COUNT(*) AS total,
  SUM(CASE WHEN suicidal='Yes' THEN 1 ELSE 0 END) AS yes_n,
  ROUND(100.0*SUM(CASE WHEN suicidal='Yes' THEN 1 ELSE 0 END)/COUNT(*),1) AS yes_pct
FROM stu
GROUP BY diet_group
ORDER BY yes_pct DESC
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-050/attempt-01/sql/S15.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-050/attempt-01/sql/S15.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-050/attempt-01/results/S15.rows.jsonl)；完整：True；SHA256：`653c71c65ea1cd8fdc647030bdeafb3ed8bc50a565400bd2ea0e80970e819ede`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "sheet1", "kind": "base", "block": null, "base_tables": ["sheet1"]}] | [] | [] |
| B2 | [{"alias": "stu", "kind": "derived", "block": "B1", "base_tables": ["sheet1"]}] | [] | ["CASE WHEN \"Dietary habits\" IN ('Healthy', 'Moderate', 'Unhealthy') THEN \"Dietary habits\" ELSE 'Other/Unknown' END"] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B2 | COUNT(*) | [] | [] | True |
| B2 | SUM(CASE WHEN suicidal = 'Yes' THEN 1 ELSE 0 END) | [] | [{"table": "sheet1", "column": "Have you ever had suicidal thoughts?"}] | False |
| B2 | COUNT(*) | [] | [] | True |
| B2 | SUM(CASE WHEN suicidal = 'Yes' THEN 1 ELSE 0 END) | [] | [{"table": "sheet1", "column": "Have you ever had suicidal thoughts?"}] | False |


## S16

类别 `data`；来源 `query_db`；调用 `5c4d4dd5a46a4e2c8a7f4fd31f297e06`；状态 `success`。

```sql
WITH stu AS (
  SELECT *, "Have you ever had suicidal thoughts?" AS suicidal FROM sheet1 WHERE "Working professional or student" = 'Student'
)
SELECT 
  CASE 
    WHEN "Academic stress" <= 2 THEN 'Low (1-2)'
    WHEN "Academic stress" = 3 THEN 'Medium (3)'
    ELSE 'High (4-5)'
  END AS acad_group,
  COUNT(*) AS total,
  SUM(CASE WHEN suicidal='Yes' THEN 1 ELSE 0 END) AS yes_n,
  ROUND(100.0*SUM(CASE WHEN suicidal='Yes' THEN 1 ELSE 0 END)/COUNT(*),1) AS yes_pct
FROM stu
GROUP BY acad_group
ORDER BY yes_pct DESC
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-050/attempt-01/sql/S16.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-050/attempt-01/sql/S16.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-050/attempt-01/results/S16.rows.jsonl)；完整：True；SHA256：`5f5cc668d00d7b27ebbcff2d655a65f1e14d4761170c0e0b4f067b9021a16857`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "sheet1", "kind": "base", "block": null, "base_tables": ["sheet1"]}] | [] | [] |
| B2 | [{"alias": "stu", "kind": "derived", "block": "B1", "base_tables": ["sheet1"]}] | [] | ["CASE WHEN \"Academic stress\" <= 2 THEN 'Low (1-2)' WHEN \"Academic stress\" = 3 THEN 'Medium (3)' ELSE 'High (4-5)' END"] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B2 | COUNT(*) | [] | [] | True |
| B2 | SUM(CASE WHEN suicidal = 'Yes' THEN 1 ELSE 0 END) | [] | [{"table": "sheet1", "column": "Have you ever had suicidal thoughts?"}] | False |
| B2 | COUNT(*) | [] | [] | True |
| B2 | SUM(CASE WHEN suicidal = 'Yes' THEN 1 ELSE 0 END) | [] | [{"table": "sheet1", "column": "Have you ever had suicidal thoughts?"}] | False |


## S17

类别 `data`；来源 `query_db`；调用 `e0f39472df114c88b7543ecc9762dfbd`；状态 `success`。

```sql
WITH stu AS (
  SELECT *, "Have you ever had suicidal thoughts?" AS suicidal FROM sheet1 WHERE "Working professional or student" = 'Student'
)
SELECT 
  CASE 
    WHEN "Financial stress" <= 2 THEN 'Low (1-2)'
    WHEN "Financial stress" = 3 THEN 'Medium (3)'
    ELSE 'High (4-5)'
  END AS fin_group,
  COUNT(*) AS total,
  SUM(CASE WHEN suicidal='Yes' THEN 1 ELSE 0 END) AS yes_n,
  ROUND(100.0*SUM(CASE WHEN suicidal='Yes' THEN 1 ELSE 0 END)/COUNT(*),1) AS yes_pct
FROM stu
GROUP BY fin_group
ORDER BY yes_pct DESC
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-050/attempt-01/sql/S17.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-050/attempt-01/sql/S17.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-050/attempt-01/results/S17.rows.jsonl)；完整：True；SHA256：`e7c10a1b15f68c0c4a11db11cfa96a757635c9d58787cda0a48b1ef8deb90d3a`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "sheet1", "kind": "base", "block": null, "base_tables": ["sheet1"]}] | [] | [] |
| B2 | [{"alias": "stu", "kind": "derived", "block": "B1", "base_tables": ["sheet1"]}] | [] | ["CASE WHEN \"Financial stress\" <= 2 THEN 'Low (1-2)' WHEN \"Financial stress\" = 3 THEN 'Medium (3)' ELSE 'High (4-5)' END"] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B2 | COUNT(*) | [] | [] | True |
| B2 | SUM(CASE WHEN suicidal = 'Yes' THEN 1 ELSE 0 END) | [] | [{"table": "sheet1", "column": "Have you ever had suicidal thoughts?"}] | False |
| B2 | COUNT(*) | [] | [] | True |
| B2 | SUM(CASE WHEN suicidal = 'Yes' THEN 1 ELSE 0 END) | [] | [{"table": "sheet1", "column": "Have you ever had suicidal thoughts?"}] | False |


## S18

类别 `data`；来源 `query_db`；调用 `a4c59f4ed0ca4172ab62134ccef50940`；状态 `success`。

```sql
WITH stu AS (
  SELECT *, "Have you ever had suicidal thoughts?" AS suicidal FROM sheet1 WHERE "Working professional or student" = 'Student'
)
SELECT 
  Gender,
  COUNT(*) AS total,
  SUM(CASE WHEN suicidal='Yes' THEN 1 ELSE 0 END) AS yes_n,
  ROUND(100.0*SUM(CASE WHEN suicidal='Yes' THEN 1 ELSE 0 END)/COUNT(*),1) AS yes_pct
FROM stu
GROUP BY Gender
ORDER BY yes_pct DESC
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-050/attempt-01/sql/S18.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-050/attempt-01/sql/S18.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-050/attempt-01/results/S18.rows.jsonl)；完整：True；SHA256：`9eb0c11ad675a8806ada0b357e9512d350af87d4a9c4a433231af78cea28e3ee`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "sheet1", "kind": "base", "block": null, "base_tables": ["sheet1"]}] | [] | [] |
| B2 | [{"alias": "stu", "kind": "derived", "block": "B1", "base_tables": ["sheet1"]}] | [] | ["Gender"] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B2 | COUNT(*) | [] | [] | True |
| B2 | SUM(CASE WHEN suicidal = 'Yes' THEN 1 ELSE 0 END) | [] | [{"table": "sheet1", "column": "Have you ever had suicidal thoughts?"}] | False |
| B2 | COUNT(*) | [] | [] | True |
| B2 | SUM(CASE WHEN suicidal = 'Yes' THEN 1 ELSE 0 END) | [] | [{"table": "sheet1", "column": "Have you ever had suicidal thoughts?"}] | False |


## S19

类别 `data`；来源 `query_db`；调用 `8d07a2b4bf594442a1ba14076c69c21f`；状态 `success`。

```sql
WITH stu AS (
  SELECT *, "Have you ever had suicidal thoughts?" AS suicidal FROM sheet1 WHERE "Working professional or student" = 'Student'
)
SELECT 
  "Family history of mental illness",
  COUNT(*) AS total,
  SUM(CASE WHEN suicidal='Yes' THEN 1 ELSE 0 END) AS yes_n,
  ROUND(100.0*SUM(CASE WHEN suicidal='Yes' THEN 1 ELSE 0 END)/COUNT(*),1) AS yes_pct
FROM stu
GROUP BY "Family history of mental illness"
ORDER BY yes_pct DESC
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-050/attempt-01/sql/S19.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-050/attempt-01/sql/S19.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-050/attempt-01/results/S19.rows.jsonl)；完整：True；SHA256：`1d262a81d06936ef6d1e0fa2a73bc7539f1915eb8a11ef96096bf0eced52acdc`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "sheet1", "kind": "base", "block": null, "base_tables": ["sheet1"]}] | [] | [] |
| B2 | [{"alias": "stu", "kind": "derived", "block": "B1", "base_tables": ["sheet1"]}] | [] | ["\"Family history of mental illness\""] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B2 | COUNT(*) | [] | [] | True |
| B2 | SUM(CASE WHEN suicidal = 'Yes' THEN 1 ELSE 0 END) | [] | [{"table": "sheet1", "column": "Have you ever had suicidal thoughts?"}] | False |
| B2 | COUNT(*) | [] | [] | True |
| B2 | SUM(CASE WHEN suicidal = 'Yes' THEN 1 ELSE 0 END) | [] | [{"table": "sheet1", "column": "Have you ever had suicidal thoughts?"}] | False |


## S20

类别 `data`；来源 `query_db`；调用 `90daec5c2b434e66933d8b4173a1e84a`；状态 `success`。

```sql
WITH stu AS (
  SELECT *, "Have you ever had suicidal thoughts?" AS suicidal FROM sheet1 WHERE "Working professional or student" = 'Student'
)
SELECT 
  CASE 
    WHEN "Satisfaction with studies" <= 2 THEN 'Low (1-2)'
    WHEN "Satisfaction with studies" = 3 THEN 'Medium (3)'
    ELSE 'High (4-5)'
  END AS sat_group,
  COUNT(*) AS total,
  SUM(CASE WHEN suicidal='Yes' THEN 1 ELSE 0 END) AS yes_n,
  ROUND(100.0*SUM(CASE WHEN suicidal='Yes' THEN 1 ELSE 0 END)/COUNT(*),1) AS yes_pct
FROM stu
GROUP BY sat_group
ORDER BY yes_pct DESC
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-050/attempt-01/sql/S20.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-050/attempt-01/sql/S20.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-050/attempt-01/results/S20.rows.jsonl)；完整：True；SHA256：`bab2c708a5851eaa2225e591e54abb969c42f43f5623af30e52f552bce88a720`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "sheet1", "kind": "base", "block": null, "base_tables": ["sheet1"]}] | [] | [] |
| B2 | [{"alias": "stu", "kind": "derived", "block": "B1", "base_tables": ["sheet1"]}] | [] | ["CASE WHEN \"Satisfaction with studies\" <= 2 THEN 'Low (1-2)' WHEN \"Satisfaction with studies\" = 3 THEN 'Medium (3)' ELSE 'High (4-5)' END"] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B2 | COUNT(*) | [] | [] | True |
| B2 | SUM(CASE WHEN suicidal = 'Yes' THEN 1 ELSE 0 END) | [] | [{"table": "sheet1", "column": "Have you ever had suicidal thoughts?"}] | False |
| B2 | COUNT(*) | [] | [] | True |
| B2 | SUM(CASE WHEN suicidal = 'Yes' THEN 1 ELSE 0 END) | [] | [{"table": "sheet1", "column": "Have you ever had suicidal thoughts?"}] | False |


## S21

类别 `data`；来源 `query_db`；调用 `569719fe5edc4b6b819dfffbb5d338f0`；状态 `success`。

```sql
WITH stu AS (
  SELECT *, "Have you ever had suicidal thoughts?" AS suicidal FROM sheet1 WHERE "Working professional or student" = 'Student'
)
SELECT 
  CASE 
    WHEN "Work/study hours" <= 6 THEN '≤6 hrs'
    WHEN "Work/study hours" <= 8 THEN '7-8 hrs'
    ELSE '9+ hrs'
  END AS hrs_group,
  COUNT(*) AS total,
  SUM(CASE WHEN suicidal='Yes' THEN 1 ELSE 0 END) AS yes_n,
  ROUND(100.0*SUM(CASE WHEN suicidal='Yes' THEN 1 ELSE 0 END)/COUNT(*),1) AS yes_pct
FROM stu
GROUP BY hrs_group
ORDER BY yes_pct DESC
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-050/attempt-01/sql/S21.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-050/attempt-01/sql/S21.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-050/attempt-01/results/S21.rows.jsonl)；完整：True；SHA256：`873ad5d1bd494048449e474cb056e2be861e2fafe625ac82c268836f99ad3821`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "sheet1", "kind": "base", "block": null, "base_tables": ["sheet1"]}] | [] | [] |
| B2 | [{"alias": "stu", "kind": "derived", "block": "B1", "base_tables": ["sheet1"]}] | [] | ["CASE WHEN \"Work/study hours\" <= 6 THEN '≤6 hrs' WHEN \"Work/study hours\" <= 8 THEN '7-8 hrs' ELSE '9+ hrs' END"] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B2 | COUNT(*) | [] | [] | True |
| B2 | SUM(CASE WHEN suicidal = 'Yes' THEN 1 ELSE 0 END) | [] | [{"table": "sheet1", "column": "Have you ever had suicidal thoughts?"}] | False |
| B2 | COUNT(*) | [] | [] | True |
| B2 | SUM(CASE WHEN suicidal = 'Yes' THEN 1 ELSE 0 END) | [] | [{"table": "sheet1", "column": "Have you ever had suicidal thoughts?"}] | False |


## S22

类别 `data`；来源 `query_db`；调用 `48ae71e7d28846efbe284481fed4bee7`；状态 `success`。

```sql
WITH stu AS (
  SELECT *, "Have you ever had suicidal thoughts?" AS suicidal FROM sheet1 WHERE "Working professional or student" = 'Student'
)
SELECT 
  CASE 
    WHEN "Cumulative GPA (CGPA)" < 6 THEN 'CGPA < 6'
    WHEN "Cumulative GPA (CGPA)" < 7.5 THEN 'CGPA 6-7.49'
    WHEN "Cumulative GPA (CGPA)" < 8.5 THEN 'CGPA 7.5-8.49'
    ELSE 'CGPA ≥ 8.5'
  END AS cgpa_group,
  COUNT(*) AS total,
  SUM(CASE WHEN suicidal='Yes' THEN 1 ELSE 0 END) AS yes_n,
  ROUND(100.0*SUM(CASE WHEN suicidal='Yes' THEN 1 ELSE 0 END)/COUNT(*),1) AS yes_pct
FROM stu
GROUP BY cgpa_group
ORDER BY yes_pct DESC
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-050/attempt-01/sql/S22.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-050/attempt-01/sql/S22.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-050/attempt-01/results/S22.rows.jsonl)；完整：True；SHA256：`00adffacbbe70bbe9e79460d37cae2cfcce46a6c4247eaa413cd44fbafabe799`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "sheet1", "kind": "base", "block": null, "base_tables": ["sheet1"]}] | [] | [] |
| B2 | [{"alias": "stu", "kind": "derived", "block": "B1", "base_tables": ["sheet1"]}] | [] | ["CASE WHEN \"Cumulative GPA (CGPA)\" < 6 THEN 'CGPA < 6' WHEN \"Cumulative GPA (CGPA)\" < 7.5 THEN 'CGPA 6-7.49' WHEN \"Cumulative GPA (CGPA)\" < 8.5 THEN 'CGPA 7.5-8.49' ELSE 'CGPA ≥ 8.5' END"] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B2 | COUNT(*) | [] | [] | True |
| B2 | SUM(CASE WHEN suicidal = 'Yes' THEN 1 ELSE 0 END) | [] | [{"table": "sheet1", "column": "Have you ever had suicidal thoughts?"}] | False |
| B2 | COUNT(*) | [] | [] | True |
| B2 | SUM(CASE WHEN suicidal = 'Yes' THEN 1 ELSE 0 END) | [] | [{"table": "sheet1", "column": "Have you ever had suicidal thoughts?"}] | False |


## S23

类别 `data`；来源 `query_db`；调用 `96b3e0bfbacc41758ce7a4038c0e1d23`；状态 `success`。

```sql
WITH stu AS (
  SELECT *, "Have you ever had suicidal thoughts?" AS suicidal FROM sheet1 WHERE "Working professional or student" = 'Student'
)
SELECT Degree, COUNT(*) AS total,
  SUM(CASE WHEN suicidal='Yes' THEN 1 ELSE 0 END) AS yes_n,
  ROUND(100.0*SUM(CASE WHEN suicidal='Yes' THEN 1 ELSE 0 END)/COUNT(*),1) AS yes_pct
FROM stu
GROUP BY Degree
HAVING total >= 100
ORDER BY yes_pct DESC
LIMIT 15
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-050/attempt-01/sql/S23.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-050/attempt-01/sql/S23.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-050/attempt-01/results/S23.rows.jsonl)；完整：True；SHA256：`3776bf4c824ccea9e262cc480fbc3eb6e4cd585af2ab7d5854d6566d81d004d8`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "sheet1", "kind": "base", "block": null, "base_tables": ["sheet1"]}] | [] | [] |
| B2 | [{"alias": "stu", "kind": "derived", "block": "B1", "base_tables": ["sheet1"]}] | [] | ["Degree"] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B2 | COUNT(*) | [] | [] | True |
| B2 | SUM(CASE WHEN suicidal = 'Yes' THEN 1 ELSE 0 END) | [] | [{"table": "sheet1", "column": "Have you ever had suicidal thoughts?"}] | False |
| B2 | COUNT(*) | [] | [] | True |
| B2 | SUM(CASE WHEN suicidal = 'Yes' THEN 1 ELSE 0 END) | [] | [{"table": "sheet1", "column": "Have you ever had suicidal thoughts?"}] | False |


## S24

类别 `data`；来源 `query_db`；调用 `0b978657f0b042a9ad76b369ff3badc4`；状态 `success`。

```sql
WITH stu AS (
  SELECT *, "Have you ever had suicidal thoughts?" AS suicidal FROM sheet1 WHERE "Working professional or student" = 'Student'
)
SELECT 
  CASE WHEN "Academic stress" >= 4 AND "Financial stress" >= 4 THEN 'High both'
       WHEN "Academic stress" >= 4 OR "Financial stress" >= 4 THEN 'High one'
       ELSE 'Neither high' END AS combo,
  COUNT(*) AS total,
  SUM(CASE WHEN suicidal='Yes' THEN 1 ELSE 0 END) AS yes_n,
  ROUND(100.0*SUM(CASE WHEN suicidal='Yes' THEN 1 ELSE 0 END)/COUNT(*),1) AS yes_pct
FROM stu
GROUP BY combo
ORDER BY yes_pct DESC
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-050/attempt-01/sql/S24.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-050/attempt-01/sql/S24.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-050/attempt-01/results/S24.rows.jsonl)；完整：True；SHA256：`5db0b552dafdc4787e74de39596316298b8889508a728b943d148281b0f8ab72`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "sheet1", "kind": "base", "block": null, "base_tables": ["sheet1"]}] | [] | [] |
| B2 | [{"alias": "stu", "kind": "derived", "block": "B1", "base_tables": ["sheet1"]}] | [] | ["CASE WHEN \"Academic stress\" >= 4 AND \"Financial stress\" >= 4 THEN 'High both' WHEN \"Academic stress\" >= 4 OR \"Financial stress\" >= 4 THEN 'High one' ELSE 'Neither high' END"] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B2 | COUNT(*) | [] | [] | True |
| B2 | SUM(CASE WHEN suicidal = 'Yes' THEN 1 ELSE 0 END) | [] | [{"table": "sheet1", "column": "Have you ever had suicidal thoughts?"}] | False |
| B2 | COUNT(*) | [] | [] | True |
| B2 | SUM(CASE WHEN suicidal = 'Yes' THEN 1 ELSE 0 END) | [] | [{"table": "sheet1", "column": "Have you ever had suicidal thoughts?"}] | False |


## S25

类别 `data`；来源 `query_db`；调用 `93b1aa7c198a49968e9868cf3e209a55`；状态 `success`。

```sql
WITH stu AS (
  SELECT *, "Have you ever had suicidal thoughts?" AS suicidal FROM sheet1 WHERE "Working professional or student" = 'Student'
  AND "Dietary habits" IN ('Healthy','Moderate','Unhealthy')
)
SELECT 
  "Dietary habits",
  CASE WHEN "Sleep duration" = 'Less than 5 hours' THEN 'Sleep<5h' ELSE 'Sleep>=5h' END AS sleep_cat,
  COUNT(*) AS total,
  SUM(CASE WHEN suicidal='Yes' THEN 1 ELSE 0 END) AS yes_n,
  ROUND(100.0*SUM(CASE WHEN suicidal='Yes' THEN 1 ELSE 0 END)/COUNT(*),1) AS yes_pct
FROM stu
GROUP BY "Dietary habits", sleep_cat
ORDER BY yes_pct DESC
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-050/attempt-01/sql/S25.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-050/attempt-01/sql/S25.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-050/attempt-01/results/S25.rows.jsonl)；完整：True；SHA256：`85b1546c823efdb5a34df7fb7e0c8871a4ffd440bd72eb53111394b1611f1cd9`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "sheet1", "kind": "base", "block": null, "base_tables": ["sheet1"]}] | [] | [] |
| B2 | [{"alias": "stu", "kind": "derived", "block": "B1", "base_tables": ["sheet1"]}] | [] | ["\"Dietary habits\"", "CASE WHEN \"Sleep duration\" = 'Less than 5 hours' THEN 'Sleep<5h' ELSE 'Sleep>=5h' END"] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B2 | COUNT(*) | [] | [] | True |
| B2 | SUM(CASE WHEN suicidal = 'Yes' THEN 1 ELSE 0 END) | [] | [{"table": "sheet1", "column": "Have you ever had suicidal thoughts?"}] | False |
| B2 | COUNT(*) | [] | [] | True |
| B2 | SUM(CASE WHEN suicidal = 'Yes' THEN 1 ELSE 0 END) | [] | [{"table": "sheet1", "column": "Have you ever had suicidal thoughts?"}] | False |


## S26

类别 `data`；来源 `query_db`；调用 `3fa9bb7137e742588cacb536ea21e8c9`；状态 `success`。

```sql
SELECT 
  CASE WHEN Age < 20 THEN '<20' WHEN Age <= 24 THEN '20-24' WHEN Age <= 29 THEN '25-29' ELSE '30+' END AS age_group,
  COUNT(*) AS total,
  SUM(CASE WHEN "Have you ever had suicidal thoughts?"='Yes' THEN 1 ELSE 0 END) AS yes_n,
  ROUND(100.0*SUM(CASE WHEN "Have you ever had suicidal thoughts?"='Yes' THEN 1 ELSE 0 END)/COUNT(*),1) AS yes_pct
FROM sheet1 
WHERE "Working professional or student" = 'Student'
GROUP BY age_group
ORDER BY age_group
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-050/attempt-01/sql/S26.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-050/attempt-01/sql/S26.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-050/attempt-01/results/S26.rows.jsonl)；完整：True；SHA256：`c23abaf6c8deca9cea27cccef959cf12ba3b4d714b1b065de33fe55543ebfb60`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "sheet1", "kind": "base", "block": null, "base_tables": ["sheet1"]}] | [] | ["CASE WHEN Age < 20 THEN '<20' WHEN Age <= 24 THEN '20-24' WHEN Age <= 29 THEN '25-29' ELSE '30+' END"] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |
| B1 | SUM(CASE WHEN "Have you ever had suicidal thoughts?" = 'Yes' THEN 1 ELSE 0 END) | [] | [{"table": "sheet1", "column": "Have you ever had suicidal thoughts?"}] | False |
| B1 | COUNT(*) | [] | [] | True |
| B1 | SUM(CASE WHEN "Have you ever had suicidal thoughts?" = 'Yes' THEN 1 ELSE 0 END) | [] | [{"table": "sheet1", "column": "Have you ever had suicidal thoughts?"}] | False |


## S27

类别 `data`；来源 `query_db`；调用 `c1d1268c7caa4d878ff9ba9eaca2d65a`；状态 `success`。

```sql
SELECT ROUND(MIN(Age),1) AS min_age, ROUND(MAX(Age),1) AS max_age, ROUND(AVG(Age),1) AS avg_age FROM sheet1 WHERE "Working professional or student" = 'Student'
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-050/attempt-01/sql/S27.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-050/attempt-01/sql/S27.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-050/attempt-01/results/S27.rows.jsonl)；完整：True；SHA256：`e0d7fde07154d1ee649bb4cd5abfc38c4815ea86863f8b4408525088aecbcd48`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "sheet1", "kind": "base", "block": null, "base_tables": ["sheet1"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | MIN(Age) | [{"table": "sheet1", "column": "Age"}] | [] | False |
| B1 | MAX(Age) | [{"table": "sheet1", "column": "Age"}] | [] | False |
| B1 | AVG(Age) | [{"table": "sheet1", "column": "Age"}] | [] | False |


## S28

类别 `data`；来源 `query_db`；调用 `2a1a214458004fcb80053fcd3f9bd6b2`；状态 `success`。

```sql
SELECT 
  "Have you ever had suicidal thoughts?" AS suicidal,
  Gender, Age, "Academic stress", "Financial stress", "Satisfaction with studies",
  "Work/study hours", "Sleep duration", "Dietary habits", "Family history of mental illness"
FROM sheet1 
WHERE "Working professional or student" = 'Student'
  AND "Dietary habits" IN ('Healthy','Moderate','Unhealthy')
  AND "Sleep duration" IS NOT NULL
  AND "Academic stress" IS NOT NULL
  AND "Financial stress" IS NOT NULL
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-050/attempt-01/sql/S28.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-050/attempt-01/sql/S28.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-050/attempt-01/results/S28.rows.jsonl)；完整：True；SHA256：`adfa954829828326ef7d5b67d03412b38c4c016ba4bdc87fe6e3e68ada77311e`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "sheet1", "kind": "base", "block": null, "base_tables": ["sheet1"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |


## S29

类别 `data`；来源 `query_db`；调用 `eb6883e0594b43a9ac828ec899f31bb0`；状态 `success`。

```sql
WITH stu AS (
  SELECT *, "Have you ever had suicidal thoughts?" AS suicidal FROM sheet1 
  WHERE "Working professional or student" = 'Student'
    AND "Dietary habits" IN ('Healthy','Moderate','Unhealthy')
    AND "Sleep duration" IS NOT NULL
),
risk AS (
  SELECT *,
    (CASE WHEN "Academic stress" >= 4 THEN 1 ELSE 0 END +
     CASE WHEN "Financial stress" >= 4 THEN 1 ELSE 0 END +
     CASE WHEN "Dietary habits" = 'Unhealthy' THEN 1 ELSE 0 END +
     CASE WHEN "Sleep duration" = 'Less than 5 hours' THEN 1 ELSE 0 END) AS n_risk
  FROM stu
)
SELECT n_risk,
  COUNT(*) AS total,
  SUM(CASE WHEN suicidal='Yes' THEN 1 ELSE 0 END) AS yes_n,
  ROUND(100.0*SUM(CASE WHEN suicidal='Yes' THEN 1 ELSE 0 END)/COUNT(*),1) AS yes_pct
FROM risk
GROUP BY n_risk
ORDER BY n_risk
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-050/attempt-01/sql/S29.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-050/attempt-01/sql/S29.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-050/attempt-01/results/S29.rows.jsonl)；完整：True；SHA256：`f271f1532a628c6bfa74ad34eb110f8025a24bba65179ceca7f2017c946c7d49`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "sheet1", "kind": "base", "block": null, "base_tables": ["sheet1"]}] | [] | [] |
| B2 | [{"alias": "stu", "kind": "derived", "block": "B1", "base_tables": ["sheet1"]}] | [] | [] |
| B3 | [{"alias": "risk", "kind": "derived", "block": "B2", "base_tables": ["sheet1"]}] | [] | ["n_risk"] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B3 | COUNT(*) | [] | [] | True |
| B3 | SUM(CASE WHEN suicidal = 'Yes' THEN 1 ELSE 0 END) | [] | [{"table": "sheet1", "column": "Have you ever had suicidal thoughts?"}] | False |
| B3 | COUNT(*) | [] | [] | True |
| B3 | SUM(CASE WHEN suicidal = 'Yes' THEN 1 ELSE 0 END) | [] | [{"table": "sheet1", "column": "Have you ever had suicidal thoughts?"}] | False |


## S30

类别 `data`；来源 `query_db`；调用 `3323a2cf35ed4952b4795571f2d11e61`；状态 `success`。

```sql
WITH stu AS (
  SELECT *, "Have you ever had suicidal thoughts?" AS suicidal FROM sheet1 
  WHERE "Working professional or student" = 'Student'
    AND "Dietary habits" IN ('Healthy','Moderate','Unhealthy')
    AND "Sleep duration" IS NOT NULL
),
risk AS (
  SELECT *,
    (CASE WHEN "Academic stress" >= 4 THEN 1 ELSE 0 END +
     CASE WHEN "Financial stress" >= 4 THEN 1 ELSE 0 END +
     CASE WHEN "Dietary habits" = 'Unhealthy' THEN 1 ELSE 0 END +
     CASE WHEN "Sleep duration" = 'Less than 5 hours' THEN 1 ELSE 0 END) AS n_risk
  FROM stu
)
SELECT 
  CASE WHEN n_risk >= 3 THEN '3-4 risk factors' 
       WHEN n_risk = 2 THEN '2 risk factors'
       WHEN n_risk = 1 THEN '1 risk factor'
       ELSE '0 risk factors' END AS risk_band,
  COUNT(*) AS total,
  SUM(CASE WHEN suicidal='Yes' THEN 1 ELSE 0 END) AS yes_n,
  ROUND(100.0*SUM(CASE WHEN suicidal='Yes' THEN 1 ELSE 0 END)/COUNT(*),1) AS yes_pct
FROM risk
GROUP BY risk_band
ORDER BY yes_pct DESC
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-050/attempt-01/sql/S30.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-050/attempt-01/sql/S30.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-050/attempt-01/results/S30.rows.jsonl)；完整：True；SHA256：`ad96bafc70bc36c154a18577b625738b7cffed7ea7d3f8a6b2eee97e7975e074`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "sheet1", "kind": "base", "block": null, "base_tables": ["sheet1"]}] | [] | [] |
| B2 | [{"alias": "stu", "kind": "derived", "block": "B1", "base_tables": ["sheet1"]}] | [] | [] |
| B3 | [{"alias": "risk", "kind": "derived", "block": "B2", "base_tables": ["sheet1"]}] | [] | ["CASE WHEN n_risk >= 3 THEN '3-4 risk factors' WHEN n_risk = 2 THEN '2 risk factors' WHEN n_risk = 1 THEN '1 risk factor' ELSE '0 risk factors' END"] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B3 | COUNT(*) | [] | [] | True |
| B3 | SUM(CASE WHEN suicidal = 'Yes' THEN 1 ELSE 0 END) | [] | [{"table": "sheet1", "column": "Have you ever had suicidal thoughts?"}] | False |
| B3 | COUNT(*) | [] | [] | True |
| B3 | SUM(CASE WHEN suicidal = 'Yes' THEN 1 ELSE 0 END) | [] | [{"table": "sheet1", "column": "Have you ever had suicidal thoughts?"}] | False |


## S31

类别 `data`；来源 `query_db`；调用 `5f110afa3b354bd08bd9f1572930b79e`；状态 `success`。

```sql
WITH stu AS (
  SELECT * FROM sheet1 WHERE "Working professional or student" = 'Student'
    AND "Dietary habits" IN ('Healthy','Moderate','Unhealthy') AND "Sleep duration" IS NOT NULL
)
SELECT 
  ROUND(100.0*SUM(CASE WHEN "Academic stress" >= 4 THEN 1 ELSE 0 END)/COUNT(*),1) AS pct_high_acad,
  ROUND(100.0*SUM(CASE WHEN "Financial stress" >= 4 THEN 1 ELSE 0 END)/COUNT(*),1) AS pct_high_fin,
  ROUND(100.0*SUM(CASE WHEN "Dietary habits"='Unhealthy' THEN 1 ELSE 0 END)/COUNT(*),1) AS pct_unhealthy_diet,
  ROUND(100.0*SUM(CASE WHEN "Sleep duration"='Less than 5 hours' THEN 1 ELSE 0 END)/COUNT(*),1) AS pct_short_sleep,
  COUNT(*) AS n
FROM stu
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-050/attempt-01/sql/S31.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-050/attempt-01/sql/S31.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-050/attempt-01/results/S31.rows.jsonl)；完整：True；SHA256：`8eab094bb1c3e78e1095f21459994f5a1cf1f77cdb2ec7568262bd0e68183069`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "sheet1", "kind": "base", "block": null, "base_tables": ["sheet1"]}] | [] | [] |
| B2 | [{"alias": "stu", "kind": "derived", "block": "B1", "base_tables": ["sheet1"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B2 | COUNT(*) | [] | [] | True |
| B2 | COUNT(*) | [] | [] | True |
| B2 | COUNT(*) | [] | [] | True |
| B2 | COUNT(*) | [] | [] | True |
| B2 | COUNT(*) | [] | [] | True |
| B2 | SUM(CASE WHEN "Academic stress" >= 4 THEN 1 ELSE 0 END) | [] | [{"table": "sheet1", "column": "Academic stress"}] | False |
| B2 | SUM(CASE WHEN "Financial stress" >= 4 THEN 1 ELSE 0 END) | [] | [{"table": "sheet1", "column": "Financial stress"}] | False |
| B2 | SUM(CASE WHEN "Dietary habits" = 'Unhealthy' THEN 1 ELSE 0 END) | [] | [{"table": "sheet1", "column": "Dietary habits"}] | False |
| B2 | SUM(CASE WHEN "Sleep duration" = 'Less than 5 hours' THEN 1 ELSE 0 END) | [] | [{"table": "sheet1", "column": "Sleep duration"}] | False |


## S32

类别 `data`；来源 `query_db`；调用 `23d1fc5fd1084b22a1ba881d0ab9c721`；状态 `success`。

```sql
WITH stu AS (
  SELECT * FROM sheet1 WHERE "Working professional or student" = 'Student'
    AND "Dietary habits" IN ('Healthy','Moderate','Unhealthy') AND "Sleep duration" IS NOT NULL
)
SELECT 
  ROUND(100.0*SUM(CASE WHEN "Academic stress" >= 4 AND "Financial stress" >= 4 THEN 1 ELSE 0 END)/COUNT(*),1) AS pct_high_both,
  ROUND(100.0*SUM(CASE WHEN ("Academic stress" >= 4 OR "Financial stress" >= 4) AND "Dietary habits"='Unhealthy' AND "Sleep duration"='Less than 5 hours' THEN 1 ELSE 0 END)/COUNT(*),1) AS pct_full_risk
FROM stu
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-050/attempt-01/sql/S32.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-050/attempt-01/sql/S32.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-050/attempt-01/results/S32.rows.jsonl)；完整：True；SHA256：`98f947f77abb02983a428eda4621e710617acf64a5a8495ae6b69f324766cb17`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "sheet1", "kind": "base", "block": null, "base_tables": ["sheet1"]}] | [] | [] |
| B2 | [{"alias": "stu", "kind": "derived", "block": "B1", "base_tables": ["sheet1"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B2 | COUNT(*) | [] | [] | True |
| B2 | COUNT(*) | [] | [] | True |
| B2 | SUM(CASE WHEN "Academic stress" >= 4 AND "Financial stress" >= 4 THEN 1 ELSE 0 END) | [] | [{"table": "sheet1", "column": "Academic stress"}, {"table": "sheet1", "column": "Financial stress"}] | False |
| B2 | SUM(CASE WHEN ("Academic stress" >= 4 OR "Financial stress" >= 4) AND "Dietary habits" = 'Unhealthy' AND "Sleep duration" = 'Less than 5 hours' THEN 1 ELSE 0 END) | [] | [{"table": "sheet1", "column": "Sleep duration"}, {"table": "sheet1", "column": "Dietary habits"}, {"table": "sheet1", "column": "Academic stress"}, {"table": "sheet1", "column": "Financial stress"}] | False |

