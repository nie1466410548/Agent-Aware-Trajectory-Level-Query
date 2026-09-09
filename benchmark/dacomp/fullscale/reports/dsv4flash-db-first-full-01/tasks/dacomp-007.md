# dacomp-007

The Research & Development (R&D) department’s employee attrition rate is significantly low…

运行：已提交。官方未评分。全部 SQL 尝试/成功 43/43；数据 SQL 41/41；Python 13 次。

完整原题：

The Research & Development (R&D) department’s employee attrition rate is significantly lower than the other two departments. Please analyze what factors are driving this difference in attrition rates.

| 表 | 行数 | 列数 |
| --- | --- | --- |
| sheet1 | 1480 | 38 |


实际路线（分析者依据 SQL/源码概括，不代表 Agent 自述）：S3：sheet1 分组聚合 → S11：sheet1 分组聚合 → S19：sheet1 分组聚合 → S27：sheet1 分组聚合 → S35：sheet1 查询 → S43：sheet1 分组聚合（等距列出六个结构节点，全部步骤见下表）

数据库大小：503,808 字节。

## 数据 SQL

| SQL | 状态 | 基础表 | Join 输入/类型 | GROUP BY | 聚合表达式 | 结果行数 | 数据库 ms |
| --- | --- | --- | --- | --- | --- | --- | --- |
| [S3/Q1](#s3) | success | ["sheet1"] | 0 / {} | ["Department"] | ["COUNT(*)", "SUM(CASE WHEN Attrition = 'Yes' THEN 1 ELSE 0 END)", "COUNT(*)", "SUM(CASE WHEN Attrition = 'Yes' THEN 1 ELSE 0 END)"] | 3 | 1.079 |
| [S4/Q2](#s4) | success | ["sheet1"] | 0 / {} | [] | ["COUNT(*)", "COUNT(DISTINCT EmpID)", "SUM(CASE WHEN Attrition = 'Yes' THEN 1 ELSE 0 END)"] | 1 | 1.319 |
| [S5/Q3](#s5) | success | ["sheet1"] | 0 / {} | ["Department", "JobRole"] | ["COUNT(*)", "SUM(CASE WHEN Attrition = 'Yes' THEN 1 ELSE 0 END)", "COUNT(*)", "SUM(CASE WHEN Attrition = 'Yes' THEN 1 ELSE 0 END)"] | 11 | 1.449 |
| [S6/Q4](#s6) | success | ["sheet1"] | 0 / {} | ["Department"] | ["AVG(MonthlyIncome)", "AVG(TotalWorkingYears)", "AVG(YearsAtCompany)", "AVG(Age)", "AVG(DistanceFromHome)", "AVG(JobSatisfaction)", "AVG(EnvironmentSatisfaction)", "AVG(JobInvolvement)", "AVG(WorkLifeBalance)", "AVG(RelationshipSatisfaction)", "AVG(PercentSalaryHike)", "AVG(StockOptionLevel)", "AVG(TrainingTimesLastYear)", "AVG(YearsSinceLastPromotion)", "AVG(YearsInCurrentRole)", "AVG(YearsWithCurrManager)"] | 3 | 2.458 |
| [S7/Q5](#s7) | success | ["sheet1"] | 0 / {} | ["Department", "JobRole"] | ["COUNT(*)", "COUNT(*)", "COUNT(*)"] | 11 | 1.548 |
| [S8/Q6](#s8) | success | ["sheet1"] | 0 / {} | ["Department", "JobLevel"] | ["COUNT(*)", "SUM(CASE WHEN Attrition = 'Yes' THEN 1 ELSE 0 END)", "COUNT(*)", "SUM(CASE WHEN Attrition = 'Yes' THEN 1 ELSE 0 END)"] | 15 | 1.286 |
| [S9/Q7](#s9) | success | ["sheet1"] | 0 / {} | ["Department", "JobLevel"] | ["COUNT(*)", "SUM(CASE WHEN Attrition = 'Yes' THEN 1 ELSE 0 END)"] | 5 | 0.786 |
| [S10/Q8](#s10) | success | ["sheet1"] | 0 / {} | ["Department", "JobRole"] | ["AVG(MonthlyIncome)", "AVG(JobLevel)", "AVG(YearsAtCompany)", "AVG(TotalWorkingYears)", "AVG(Age)"] | 11 | 1.731 |
| [S11/Q9](#s11) | success | ["sheet1"] | 0 / {} | ["Department", "OverTime"] | ["COUNT(*)", "SUM(CASE WHEN Attrition = 'Yes' THEN 1 ELSE 0 END)", "COUNT(*)", "SUM(CASE WHEN Attrition = 'Yes' THEN 1 ELSE 0 END)"] | 6 | 1.461 |
| [S12/Q10](#s12) | success | ["sheet1"] | 0 / {} | ["Department", "BusinessTravel"] | ["COUNT(*)", "SUM(CASE WHEN Attrition = 'Yes' THEN 1 ELSE 0 END)", "COUNT(*)", "SUM(CASE WHEN Attrition = 'Yes' THEN 1 ELSE 0 END)"] | 12 | 1.315 |
| [S13/Q11](#s13) | success | ["sheet1"] | 0 / {} | ["Department", "MaritalStatus"] | ["COUNT(*)", "SUM(CASE WHEN Attrition = 'Yes' THEN 1 ELSE 0 END)", "COUNT(*)", "SUM(CASE WHEN Attrition = 'Yes' THEN 1 ELSE 0 END)"] | 9 | 1.426 |
| [S14/Q12](#s14) | success | ["sheet1"] | 0 / {} | ["Department", "StockOptionLevel"] | ["COUNT(*)", "SUM(CASE WHEN Attrition = 'Yes' THEN 1 ELSE 0 END)", "COUNT(*)", "SUM(CASE WHEN Attrition = 'Yes' THEN 1 ELSE 0 END)"] | 12 | 1.337 |
| [S15/Q13](#s15) | success | ["sheet1"] | 0 / {} | ["Department", "SalarySlab"] | ["COUNT(*)", "SUM(CASE WHEN Attrition = 'Yes' THEN 1 ELSE 0 END)", "COUNT(*)", "SUM(CASE WHEN Attrition = 'Yes' THEN 1 ELSE 0 END)"] | 12 | 1.404 |
| [S16/Q14](#s16) | success | ["sheet1"] | 0 / {} | ["Department", "EducationField"] | ["COUNT(*)", "SUM(CASE WHEN Attrition = 'Yes' THEN 1 ELSE 0 END)", "COUNT(*)", "SUM(CASE WHEN Attrition = 'Yes' THEN 1 ELSE 0 END)"] | 14 | 1.459 |
| [S17/Q15](#s17) | success | ["sheet1"] | 0 / {} | ["Department", "SalarySlab"] | ["COUNT(*)", "COUNT(*)", "COUNT(*)"] | 12 | 1.493 |
| [S18/Q16](#s18) | success | ["sheet1"] | 0 / {} | ["Department", "AgeGroup"] | ["COUNT(*)", "SUM(CASE WHEN Attrition = 'Yes' THEN 1 ELSE 0 END)", "COUNT(*)", "SUM(CASE WHEN Attrition = 'Yes' THEN 1 ELSE 0 END)"] | 15 | 1.213 |
| [S19/Q17](#s19) | success | ["sheet1"] | 0 / {} | ["Department", "AgeGroup"] | ["COUNT(*)", "SUM(CASE WHEN Attrition = 'Yes' THEN 1 ELSE 0 END)", "COUNT(*)", "SUM(CASE WHEN Attrition = 'Yes' THEN 1 ELSE 0 END)"] | 5 | 0.788 |
| [S20/Q18](#s20) | success | ["sheet1"] | 0 / {} | ["Department", "JobSatisfaction"] | ["COUNT(*)", "SUM(CASE WHEN Attrition = 'Yes' THEN 1 ELSE 0 END)", "COUNT(*)", "SUM(CASE WHEN Attrition = 'Yes' THEN 1 ELSE 0 END)"] | 12 | 1.329 |
| [S21/Q19](#s21) | success | ["sheet1"] | 0 / {} | ["Department"] | ["COUNT(*)", "COUNT(*)", "COUNT(*)", "COUNT(*)", "COUNT(*)", "COUNT(*)", "SUM(CASE WHEN JobSatisfaction >= 3 THEN 1 ELSE 0 END)", "SUM(CASE WHEN EnvironmentSatisfaction >= 3 THEN 1 ELSE 0 END)", "SUM(CASE WHEN WorkLifeBalance >= 3 THEN 1 ELSE 0 END)", "SUM(CASE WHEN JobInvolvement >= 3 THEN 1 ELSE 0 END)", "SUM(CASE WHEN RelationshipSatisfaction >= 3 THEN 1 ELSE 0 END)", "SUM(CASE WHEN PerformanceRating >= 3 THEN 1 ELSE 0 END)"] | 3 | 1.651 |
| [S22/Q20](#s22) | success | ["sheet1"] | 0 / {} | ["Department", "Gender"] | ["COUNT(*)", "SUM(CASE WHEN Attrition = 'Yes' THEN 1 ELSE 0 END)", "COUNT(*)", "SUM(CASE WHEN Attrition = 'Yes' THEN 1 ELSE 0 END)", "COUNT(*)", "COUNT(*)"] | 6 | 1.359 |
| [S23/Q21](#s23) | success | ["sheet1"] | 0 / {} | ["Department", "CASE WHEN YearsAtCompany <= 2 THEN '0-2y' WHEN YearsAtCompany <= 5 THEN '3-5y' WHEN YearsAtCompany <= 10 THEN '6-10y' ELSE '10y+' END"] | ["COUNT(*)", "SUM(CASE WHEN Attrition = 'Yes' THEN 1 ELSE 0 END)", "COUNT(*)", "SUM(CASE WHEN Attrition = 'Yes' THEN 1 ELSE 0 END)"] | 12 | 1.695 |
| [S24/Q22](#s24) | success | ["sheet1"] | 0 / {} | ["Department", "CASE WHEN TotalWorkingYears <= 2 THEN '0-2y' WHEN TotalWorkingYears <= 5 THEN '3-5y' WHEN TotalWorkingYears <= 10 THEN '6-10y' ELSE '10y+' END"] | ["COUNT(*)", "SUM(CASE WHEN Attrition = 'Yes' THEN 1 ELSE 0 END)", "COUNT(*)", "SUM(CASE WHEN Attrition = 'Yes' THEN 1 ELSE 0 END)"] | 12 | 1.533 |
| [S25/Q23](#s25) | success | ["sheet1"] | 0 / {} | ["Department", "CASE WHEN YearsAtCompany <= 2 THEN '0-2y' WHEN YearsAtCompany <= 5 THEN '3-5y' WHEN YearsAtCompany <= 10 THEN '6-10y' ELSE '10y+' END"] | ["COUNT(*)", "COUNT(*)", "COUNT(*)"] | 12 | 1.534 |
| [S26/Q24](#s26) | success | ["sheet1"] | 0 / {} | ["Department"] | ["AVG(NumCompaniesWorked)", "AVG(TrainingTimesLastYear)", "AVG(YearsSinceLastPromotion)", "AVG(YearsInCurrentRole)", "AVG(YearsWithCurrManager)", "AVG(PercentSalaryHike)", "AVG(Education)"] | 3 | 1.55 |
| [S27/Q25](#s27) | success | ["sheet1"] | 0 / {} | ["Department", "JobLevel"] | ["COUNT(*)", "SUM(CASE WHEN Attrition = 'Yes' THEN 1 ELSE 0 END)", "COUNT(*)", "COUNT(*)", "SUM(CASE WHEN Attrition = 'Yes' THEN 1 ELSE 0 END)", "COUNT(*)"] | 15 | 1.428 |
| [S28/Q26](#s28) | success | ["sheet1"] | 0 / {} | ["Department", "OverTime"] | ["COUNT(*)", "COUNT(*)", "COUNT(*)"] | 6 | 1.336 |
| [S29/Q27](#s29) | success | ["sheet1"] | 0 / {} | ["Department", "JobLevel"] | ["COUNT(*)", "SUM(CASE WHEN Attrition = 'Yes' THEN 1 ELSE 0 END)", "COUNT(*)", "COUNT(*)", "SUM(CASE WHEN Attrition = 'Yes' THEN 1 ELSE 0 END)", "COUNT(*)"] | 5 | 0.893 |
| [S30/Q28](#s30) | success | ["sheet1"] | 0 / {} | [] | [] | 1480 | 10.337 |
| [S31/Q29](#s31) | success | ["sheet1"] | 0 / {} | [] | [] | 1480 | 1.804 |
| [S32/Q30](#s32) | success | ["sheet1"] | 0 / {} | [] | [] | 1480 | 1.698 |
| [S33/Q31](#s33) | success | ["sheet1"] | 0 / {} | [] | [] | 1480 | 9.894 |
| [S34/Q32](#s34) | success | ["sheet1"] | 0 / {} | [] | [] | 1480 | 9.643 |
| [S35/Q33](#s35) | success | ["sheet1"] | 0 / {} | [] | [] | 1480 | 9.81 |
| [S36/Q34](#s36) | success | ["sheet1"] | 0 / {} | ["EmpID"] | ["COUNT(*)"] | 20 | 1.72 |
| [S37/Q35](#s37) | success | ["sheet1"] | 0 / {} | [] | [] | 1480 | 9.454 |
| [S38/Q36](#s38) | success | ["sheet1"] | 0 / {} | [] | [] | 1480 | 10.111 |
| [S39/Q37](#s39) | success | ["sheet1"] | 0 / {} | [] | [] | 1480 | 9.825 |
| [S40/Q38](#s40) | success | ["sheet1"] | 0 / {} | [] | [] | 1480 | 9.803 |
| [S41/Q39](#s41) | success | ["sheet1"] | 0 / {} | [] | [] | 1480 | 9.809 |
| [S42/Q40](#s42) | success | ["sheet1"] | 0 / {} | [] | [] | 1480 | 10.018 |
| [S43/Q41](#s43) | success | ["sheet1"] | 0 / {} | ["Department"] | ["SUM(CASE WHEN Attrition = 'Yes' THEN 1 ELSE 0 END)", "COUNT(*)", "SUM(CASE WHEN Attrition = 'Yes' THEN 1 ELSE 0 END)", "COUNT(*)", "COUNT(*)", "SUM(CASE WHEN Attrition = 'Yes' THEN 1 ELSE 0 END)", "SUM(CASE WHEN Attrition = 'Yes' THEN 1 ELSE 0 END)", "COUNT(*)"] | 3 | 1.346 |


## 元数据和设置

| SQL | 类别 | 状态 | 内容 |
| --- | --- | --- | --- |
| S1 | connection_setup | success | PRAGMA query_only=ON |
| S2 | metadata | success | SELECT name,sql FROM sqlite_master WHERE type='table' ORDER BY name |


## Python 与执行位置

人工源码审查：**database_first_violation**。Python repeatedly calculates departmental/job-level attrition rates, counts, means, ranks and cross-tabs from row-level results. These operations are supported by SQLite grouping/window expressions. The repeated query result is a verified direct-reuse opportunity, but the subsequent relational processing in pandas is a protocol violation. [证据](../reviews/dacomp-007.json)。

P1：Need to compute standardized attrition rates controlling for job level composition to determine if the R&D department's lower attrition is due to its composition or other factors. This requires standardization calculations that are more natural in Python.

[源码](../../../runs/dsv4flash-db-first-full-01/dacomp-007/attempt-01/python/P1.py)；[输出](../../../runs/dsv4flash-db-first-full-01/dacomp-007/attempt-01/python/P1.stdout)；[错误](../../../runs/dsv4flash-db-first-full-01/dacomp-007/attempt-01/python/P1.stderr)。检出需人工核验的 SQL 可实现操作：groupby(, .query(；不能仅凭理由判为合规。

P2：Compute direct standardization of attrition by job level to decompose the Sales vs R&D attrition gap into a composition effect and a within-level rate effect.

[源码](../../../runs/dsv4flash-db-first-full-01/dacomp-007/attempt-01/python/P2.py)；[输出](../../../runs/dsv4flash-db-first-full-01/dacomp-007/attempt-01/python/P2.stdout)；[错误](../../../runs/dsv4flash-db-first-full-01/dacomp-007/attempt-01/python/P2.stderr)。检出需人工核验的 SQL 可实现操作：groupby(, .query(；不能仅凭理由判为合规。

P3：Perform Oaxaca decomposition to separate the Sales vs R&D attrition gap into composition effects (different job level mix) and rate effects (different within-level attrition rates).

[源码](../../../runs/dsv4flash-db-first-full-01/dacomp-007/attempt-01/python/P3.py)；[输出](../../../runs/dsv4flash-db-first-full-01/dacomp-007/attempt-01/python/P3.stdout)；[错误](../../../runs/dsv4flash-db-first-full-01/dacomp-007/attempt-01/python/P3.stderr)。检出需人工核验的 SQL 可实现操作：groupby(, .query(；不能仅凭理由判为合规。

P4：Compare income and other factors between R&D and Sales within the same job level to identify drivers of within-level attrition rate differences.

[源码](../../../runs/dsv4flash-db-first-full-01/dacomp-007/attempt-01/python/P4.py)；[输出](../../../runs/dsv4flash-db-first-full-01/dacomp-007/attempt-01/python/P4.stdout)；[错误](../../../runs/dsv4flash-db-first-full-01/dacomp-007/attempt-01/python/P4.stderr)。检出需人工核验的 SQL 可实现操作：groupby(, .query(；不能仅凭理由判为合规。

P5：Clean tabular comparison of attrition rates by factor within each job level for R&D vs Sales to identify the specific factors where within-level attrition differs most.

[源码](../../../runs/dsv4flash-db-first-full-01/dacomp-007/attempt-01/python/P5.py)；[输出](../../../runs/dsv4flash-db-first-full-01/dacomp-007/attempt-01/python/P5.stdout)；[错误](../../../runs/dsv4flash-db-first-full-01/dacomp-007/attempt-01/python/P5.stderr)。检出需人工核验的 SQL 可实现操作：groupby(, .query(；不能仅凭理由判为合规。

P6：Compile a role-level summary of attrition and its correlates across departments, and check data quality (duplicate EmpIDs).

[源码](../../../runs/dsv4flash-db-first-full-01/dacomp-007/attempt-01/python/P6.py)；[输出](../../../runs/dsv4flash-db-first-full-01/dacomp-007/attempt-01/python/P6.stdout)；[错误](../../../runs/dsv4flash-db-first-full-01/dacomp-007/attempt-01/python/P6.stderr)。检出需人工核验的 SQL 可实现操作：groupby(, .query(, sort_values(；不能仅凭理由判为合规。

P7：Inspect the duplicated EmpID records to determine whether they are exact duplicates or conflicting records that could affect attrition counts.

[源码](../../../runs/dsv4flash-db-first-full-01/dacomp-007/attempt-01/python/P7.py)；[输出](../../../runs/dsv4flash-db-first-full-01/dacomp-007/attempt-01/python/P7.stdout)；[错误](../../../runs/dsv4flash-db-first-full-01/dacomp-007/attempt-01/python/P7.stderr)。检出需人工核验的 SQL 可实现操作：.query(, sort_values(；不能仅凭理由判为合规。

P8：Create comprehensive visualization of attrition patterns across departments broken down by job level, overtime, stock options, and marital status.

[源码](../../../runs/dsv4flash-db-first-full-01/dacomp-007/attempt-01/python/P8.py)；[输出](../../../runs/dsv4flash-db-first-full-01/dacomp-007/attempt-01/python/P8.stdout)；[错误](../../../runs/dsv4flash-db-first-full-01/dacomp-007/attempt-01/python/P8.stderr)。检出需人工核验的 SQL 可实现操作：groupby(, .query(；不能仅凭理由判为合规。

P9：Create visualizations of job role composition and income differences across departments.

[源码](../../../runs/dsv4flash-db-first-full-01/dacomp-007/attempt-01/python/P9.py)；[输出](../../../runs/dsv4flash-db-first-full-01/dacomp-007/attempt-01/python/P9.stdout)；[错误](../../../runs/dsv4flash-db-first-full-01/dacomp-007/attempt-01/python/P9.stderr)。检出需人工核验的 SQL 可实现操作：groupby(, .query(, sort_values(；不能仅凭理由判为合规。

P10：Perform counterfactual analysis to quantify the contribution of specific job roles (especially Sales Representatives) to the department-level attrition differences.

[源码](../../../runs/dsv4flash-db-first-full-01/dacomp-007/attempt-01/python/P10.py)；[输出](../../../runs/dsv4flash-db-first-full-01/dacomp-007/attempt-01/python/P10.stdout)；[错误](../../../runs/dsv4flash-db-first-full-01/dacomp-007/attempt-01/python/P10.stderr)。检出需人工核验的 SQL 可实现操作：groupby(, .query(；不能仅凭理由判为合规。

P11：Examine additional factors (prior employers, commute distance, promotion recency, training) and how they relate to attrition across departments.

[源码](../../../runs/dsv4flash-db-first-full-01/dacomp-007/attempt-01/python/P11.py)；[输出](../../../runs/dsv4flash-db-first-full-01/dacomp-007/attempt-01/python/P11.stdout)；[错误](../../../runs/dsv4flash-db-first-full-01/dacomp-007/attempt-01/python/P11.stderr)。检出需人工核验的 SQL 可实现操作：groupby(, .query(；不能仅凭理由判为合规。

P12：Create a side-by-side bar chart comparing Sales vs R&D attrition rates across all key factors to visualize the pervasive pattern where R&D has lower attrition in every category.

[源码](../../../runs/dsv4flash-db-first-full-01/dacomp-007/attempt-01/python/P12.py)；[输出](../../../runs/dsv4flash-db-first-full-01/dacomp-007/attempt-01/python/P12.stdout)；[错误](../../../runs/dsv4flash-db-first-full-01/dacomp-007/attempt-01/python/P12.stderr)。检出需人工核验的 SQL 可实现操作：groupby(, .query(, sort_values(；不能仅凭理由判为合规。

P13：Create a waterfall decomposition visualization and compile the final summary statistics.

[源码](../../../runs/dsv4flash-db-first-full-01/dacomp-007/attempt-01/python/P13.py)；[输出](../../../runs/dsv4flash-db-first-full-01/dacomp-007/attempt-01/python/P13.stdout)；[错误](../../../runs/dsv4flash-db-first-full-01/dacomp-007/attempt-01/python/P13.stderr)。检出需人工核验的 SQL 可实现操作：.query(；不能仅凭理由判为合规。

## 优化机会

已验证候选。筛选限于精确 SQL、相同自包含 CTE、相同单表完整过滤、可分解单表聚合；未覆盖任意 Join 等价和一般谓词蕴含。全部候选都是 offline，未测在线预测。

| 候选 | 类型 | 已有结果 | 覆盖 SQL | 后续次数 | 中间行数 | 验证 | 成本 |
| --- | --- | --- | --- | --- | --- | --- | --- |
| C1 | exact-result reuse | True | ["S30", "S33", "S34", "S35", "S37", "S38", "S39", "S40", "S41", "S42"] | 9 | 1480 | verified | Not benchmarked; correctness alone does not establish net speedup. |
| C2 | exact-result reuse | True | ["S31", "S32"] | 1 | 1480 | verified | Not benchmarked; correctness alone does not establish net speedup. |
| C3 | aggregate MV | False | ["S3", "S5", "S6", "S8", "S10", "S11", "S12", "S13", "S14", "S15", "S16", "S18", "S20", "S21", "S23", "S24", "S26"] | 16 | 1438 | verified | Not benchmarked; correctness alone does not establish net speedup. |
| C4 | common filtered view | False | ["S9", "S19"] | 1 | unknown | not_verified_cap | Not tested |
| C5 | aggregate MV | False | ["S9", "S19"] | 1 | unknown | not_verified_cap | Not tested |


已验证覆盖（含触发查询、候选并集去重）：29/41 条成功数据 SQL。正确性仅针对当前数据库快照；未测性能的候选不能声称已加速。

[完整 build/rewrite 与比较证据](dacomp-007.analysis.json)。

### C3：aggregate MV

Union of grouping keys; decomposable aggregate states; AVG uses SUM and non-NULL COUNT.

原查询 [S3](#s3), [S5](#s5), [S6](#s6), [S8](#s8), [S10](#s10), [S11](#s11), [S12](#s12), [S13](#s13), [S14](#s14), [S15](#s15), [S16](#s16), [S18](#s18), [S20](#s20), [S21](#s21), [S23](#s23), [S24](#s24), [S26](#s26) → 新增共享状态 C3 → 后续 16 次可复用。该构建点为事后假设，不代表 Agent 当时预知后续。

构建定义：

```sql
SELECT department AS __g0, jobrole AS __g1, joblevel AS __g2, overtime AS __g3, businesstravel AS __g4, maritalstatus AS __g5, stockoptionlevel AS __g6, salaryslab AS __g7, educationfield AS __g8, agegroup AS __g9, jobsatisfaction AS __g10, CASE WHEN yearsatcompany <= 2 THEN '0-2y' WHEN yearsatcompany <= 5 THEN '3-5y' WHEN yearsatcompany <= 10 THEN '6-10y' ELSE '10y+' END AS __g11, CASE WHEN totalworkingyears <= 2 THEN '0-2y' WHEN totalworkingyears <= 5 THEN '3-5y' WHEN totalworkingyears <= 10 THEN '6-10y' ELSE '10y+' END AS __g12, COUNT(*) AS __a0, SUM(CASE WHEN attrition = 'Yes' THEN 1 ELSE 0 END) AS __a1, SUM(monthlyincome) AS __a2_sum, COUNT(monthlyincome) AS __a2_n, SUM(totalworkingyears) AS __a3_sum, COUNT(totalworkingyears) AS __a3_n, SUM(yearsatcompany) AS __a4_sum, COUNT(yearsatcompany) AS __a4_n, SUM(age) AS __a5_sum, COUNT(age) AS __a5_n, SUM(distancefromhome) AS __a6_sum, COUNT(distancefromhome) AS __a6_n, SUM(jobsatisfaction) AS __a7_sum, COUNT(jobsatisfaction) AS __a7_n, SUM(environmentsatisfaction) AS __a8_sum, COUNT(environmentsatisfaction) AS __a8_n, SUM(jobinvolvement) AS __a9_sum, COUNT(jobinvolvement) AS __a9_n, SUM(worklifebalance) AS __a10_sum, COUNT(worklifebalance) AS __a10_n, SUM(relationshipsatisfaction) AS __a11_sum, COUNT(relationshipsatisfaction) AS __a11_n, SUM(percentsalaryhike) AS __a12_sum, COUNT(percentsalaryhike) AS __a12_n, SUM(stockoptionlevel) AS __a13_sum, COUNT(stockoptionlevel) AS __a13_n, SUM(trainingtimeslastyear) AS __a14_sum, COUNT(trainingtimeslastyear) AS __a14_n, SUM(yearssincelastpromotion) AS __a15_sum, COUNT(yearssincelastpromotion) AS __a15_n, SUM(yearsincurrentrole) AS __a16_sum, COUNT(yearsincurrentrole) AS __a16_n, SUM(yearswithcurrmanager) AS __a17_sum, COUNT(yearswithcurrmanager) AS __a17_n, SUM(joblevel) AS __a18_sum, COUNT(joblevel) AS __a18_n, SUM(CASE WHEN jobsatisfaction >= 3 THEN 1 ELSE 0 END) AS __a19, SUM(CASE WHEN environmentsatisfaction >= 3 THEN 1 ELSE 0 END) AS __a20, SUM(CASE WHEN worklifebalance >= 3 THEN 1 ELSE 0 END) AS __a21, SUM(CASE WHEN jobinvolvement >= 3 THEN 1 ELSE 0 END) AS __a22, SUM(CASE WHEN relationshipsatisfaction >= 3 THEN 1 ELSE 0 END) AS __a23, SUM(CASE WHEN performancerating >= 3 THEN 1 ELSE 0 END) AS __a24, SUM(numcompaniesworked) AS __a25_sum, COUNT(numcompaniesworked) AS __a25_n, SUM(education) AS __a26_sum, COUNT(education) AS __a26_n FROM "sheet1"  GROUP BY department, jobrole, joblevel, overtime, businesstravel, maritalstatus, stockoptionlevel, salaryslab, educationfield, agegroup, jobsatisfaction, CASE WHEN yearsatcompany <= 2 THEN '0-2y' WHEN yearsatcompany <= 5 THEN '3-5y' WHEN yearsatcompany <= 10 THEN '6-10y' ELSE '10y+' END, CASE WHEN totalworkingyears <= 2 THEN '0-2y' WHEN totalworkingyears <= 5 THEN '3-5y' WHEN totalworkingyears <= 10 THEN '6-10y' ELSE '10y+' END
```

受益查询 S3 的改写示例：

```sql
SELECT __g0 AS "Department", SUM(__a0) AS total, SUM(__a1) AS attrition_count, ROUND(100.0 * SUM(__a1) / SUM(__a0), 2) AS attrition_rate FROM temp.reuse_candidate GROUP BY __g0 ORDER BY attrition_rate DESC
```

| 原 SQL | 列名一致 | 结果一致 | 比较方法 |
| --- | --- | --- | --- |
| S3 | True | True | ordered_numeric_tolerance |
| S5 | True | True | ordered_numeric_tolerance |
| S6 | True | True | exact_multiset |
| S8 | True | True | ordered_numeric_tolerance |
| S10 | True | True | ordered_numeric_tolerance |
| S11 | True | True | ordered_numeric_tolerance |
| S12 | True | True | ordered_numeric_tolerance |
| S13 | True | True | ordered_numeric_tolerance |
| S14 | True | True | ordered_numeric_tolerance |
| S15 | True | True | ordered_numeric_tolerance |
| S16 | True | True | ordered_numeric_tolerance |
| S18 | True | True | ordered_numeric_tolerance |
| S20 | True | True | ordered_numeric_tolerance |
| S21 | True | True | exact_multiset |
| S23 | True | True | ordered_numeric_tolerance |
| S24 | True | True | ordered_numeric_tolerance |
| S26 | True | True | exact_multiset |


验证状态：verified；成本结论：Not benchmarked; correctness alone does not establish net speedup.

### C1：exact-result reuse

Identical normalized SQL and parameters; archive equality checked.

原查询 [S30](#s30), [S33](#s33), [S34](#s34), [S35](#s35), [S37](#s37), [S38](#s38), [S39](#s39), [S40](#s40), [S41](#s41), [S42](#s42) → 保留前序结果 S30 → 后续 9 次可复用。该构建点为事后假设，不代表 Agent 当时预知后续。

| 原 SQL | 列名一致 | 结果一致 | 比较方法 |
| --- | --- | --- | --- |
| S33 | True | True | exact_multiset |
| S34 | True | True | exact_multiset |
| S35 | True | True | exact_multiset |
| S37 | True | True | exact_multiset |
| S38 | True | True | exact_multiset |
| S39 | True | True | exact_multiset |
| S40 | True | True | exact_multiset |
| S41 | True | True | exact_multiset |
| S42 | True | True | exact_multiset |


验证状态：verified；成本结论：Not benchmarked; correctness alone does not establish net speedup.

### C2：exact-result reuse

Identical normalized SQL and parameters; archive equality checked.

原查询 [S31](#s31), [S32](#s32) → 保留前序结果 S31 → 后续 1 次可复用。该构建点为事后假设，不代表 Agent 当时预知后续。

| 原 SQL | 列名一致 | 结果一致 | 比较方法 |
| --- | --- | --- | --- |
| S32 | True | True | exact_multiset |


验证状态：verified；成本结论：Not benchmarked; correctness alone does not establish net speedup.

结果依赖：自动记录 SQL→Python 的接口父调用，以及源码中引用归档文件的消费者；字面值相同不认定因果。模型方向选择需要人工读取消息，尚未做全面因果标注。

[原始报告](../../../runs/dsv4flash-db-first-full-01/dacomp-007/attempt-01/answer.md)；[统一消息](../../../runs/dsv4flash-db-first-full-01/dacomp-007/attempt-01/messages.jsonl)；[原始 OpenCode 事件](../../../runs/dsv4flash-db-first-full-01/dacomp-007/attempt-01/opencode.jsonl)；[SQL 引擎日志](../../../runs/dsv4flash-db-first-full-01/dacomp-007/attempt-01/sql_journal.jsonl)。

[可读报告（本地图片链接规范化）](../answers/dacomp-007.md)。原始回答保留，分析结论未改写。

## S1

类别 `connection_setup`；来源 `connection`；调用 `1d6a89751fcf4a3187f31f518fbe563e`；状态 `success`。

```sql
PRAGMA query_only=ON
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-007/attempt-01/sql/S1.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-007/attempt-01/sql/S1.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-007/attempt-01/results/S1.rows.jsonl)；完整：True；SHA256：`e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`。

## S2

类别 `metadata`；来源 `list_db`；调用 `1d6a89751fcf4a3187f31f518fbe563e`；状态 `success`。

```sql
SELECT name,sql FROM sqlite_master WHERE type='table' ORDER BY name
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-007/attempt-01/sql/S2.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-007/attempt-01/sql/S2.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-007/attempt-01/results/S2.rows.jsonl)；完整：True；SHA256：`94731284c43bc8e5b144e13abccbd74adbf46917d68d6726705b8596d303b46c`。

## S3

类别 `data`；来源 `query_db`；调用 `ebc26df16e4c4300a322e41a216bb11e`；状态 `success`。

```sql
SELECT Department, COUNT(*) AS total, SUM(CASE WHEN Attrition='Yes' THEN 1 ELSE 0 END) AS attrition_count, ROUND(100.0*SUM(CASE WHEN Attrition='Yes' THEN 1 ELSE 0 END)/COUNT(*),2) AS attrition_rate FROM sheet1 GROUP BY Department ORDER BY attrition_rate DESC;
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-007/attempt-01/sql/S3.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-007/attempt-01/sql/S3.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-007/attempt-01/results/S3.rows.jsonl)；完整：True；SHA256：`1fd28b6a22fc981d5c5d62b044026357beb69bb4a2be9705bdb82f87c34b6d13`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "sheet1", "kind": "base", "block": null, "base_tables": ["sheet1"]}] | [] | ["Department"] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |
| B1 | SUM(CASE WHEN Attrition = 'Yes' THEN 1 ELSE 0 END) | [] | [{"table": "sheet1", "column": "Attrition"}] | False |
| B1 | COUNT(*) | [] | [] | True |
| B1 | SUM(CASE WHEN Attrition = 'Yes' THEN 1 ELSE 0 END) | [] | [{"table": "sheet1", "column": "Attrition"}] | False |


## S4

类别 `data`；来源 `query_db`；调用 `25dbab14f0464073af6f9dc0fa412c54`；状态 `success`。

```sql
SELECT COUNT(*) AS total_rows, COUNT(DISTINCT EmpID) AS unique_emp, SUM(CASE WHEN Attrition='Yes' THEN 1 ELSE 0 END) AS total_attrition FROM sheet1;
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-007/attempt-01/sql/S4.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-007/attempt-01/sql/S4.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-007/attempt-01/results/S4.rows.jsonl)；完整：True；SHA256：`a9d66dfd08ab139d7ac15b909ff328083d7c67572024ca5892fa46fa5b7b3a94`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "sheet1", "kind": "base", "block": null, "base_tables": ["sheet1"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |
| B1 | COUNT(DISTINCT EmpID) | [{"table": "sheet1", "column": "EmpID"}] | [] | False |
| B1 | SUM(CASE WHEN Attrition = 'Yes' THEN 1 ELSE 0 END) | [] | [{"table": "sheet1", "column": "Attrition"}] | False |


## S5

类别 `data`；来源 `query_db`；调用 `9e86d387398f49f2aeff77c387af6377`；状态 `success`。

```sql
SELECT Department, JobRole, COUNT(*) AS total, SUM(CASE WHEN Attrition='Yes' THEN 1 ELSE 0 END) AS attrition_count, ROUND(100.0*SUM(CASE WHEN Attrition='Yes' THEN 1 ELSE 0 END)/COUNT(*),2) AS attrition_rate FROM sheet1 GROUP BY Department, JobRole ORDER BY Department, attrition_rate DESC;
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-007/attempt-01/sql/S5.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-007/attempt-01/sql/S5.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-007/attempt-01/results/S5.rows.jsonl)；完整：True；SHA256：`0037ad211a07b9d7fa4b199811de7b6b74de219b0cf5b36fb1d86b404dfeeca5`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "sheet1", "kind": "base", "block": null, "base_tables": ["sheet1"]}] | [] | ["Department", "JobRole"] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |
| B1 | SUM(CASE WHEN Attrition = 'Yes' THEN 1 ELSE 0 END) | [] | [{"table": "sheet1", "column": "Attrition"}] | False |
| B1 | COUNT(*) | [] | [] | True |
| B1 | SUM(CASE WHEN Attrition = 'Yes' THEN 1 ELSE 0 END) | [] | [{"table": "sheet1", "column": "Attrition"}] | False |


## S6

类别 `data`；来源 `query_db`；调用 `1046000040964b03acdf46abd978563c`；状态 `success`。

```sql
SELECT Department, ROUND(AVG(MonthlyIncome),0) AS avg_income, ROUND(AVG(TotalWorkingYears),2) AS avg_working_years, ROUND(AVG(YearsAtCompany),2) AS avg_tenure, ROUND(AVG(Age),2) AS avg_age, ROUND(AVG(DistanceFromHome),2) AS avg_distance, ROUND(AVG(JobSatisfaction),2) AS avg_job_satisfaction, ROUND(AVG(EnvironmentSatisfaction),2) AS avg_env_satisfaction, ROUND(AVG(JobInvolvement),2) AS avg_job_involvement, ROUND(AVG(WorkLifeBalance),2) AS avg_worklife_balance, ROUND(AVG(RelationshipSatisfaction),2) AS avg_rel_satisfaction, ROUND(AVG(PercentSalaryHike),2) AS avg_salary_hike, ROUND(AVG(StockOptionLevel),2) AS avg_stock_options, ROUND(AVG(TrainingTimesLastYear),2) AS avg_training, ROUND(AVG(YearsSinceLastPromotion),2) AS avg_yrs_since_promo, ROUND(AVG(YearsInCurrentRole),2) AS avg_yrs_in_role, ROUND(AVG(YearsWithCurrManager),2) AS avg_yrs_with_mgr FROM sheet1 GROUP BY Department;
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-007/attempt-01/sql/S6.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-007/attempt-01/sql/S6.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-007/attempt-01/results/S6.rows.jsonl)；完整：True；SHA256：`e6b4e2e8b08ac9ff2f4d4e7526076de77c9d06a62548f3cc6b876c356f94e841`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "sheet1", "kind": "base", "block": null, "base_tables": ["sheet1"]}] | [] | ["Department"] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | AVG(MonthlyIncome) | [{"table": "sheet1", "column": "MonthlyIncome"}] | [] | False |
| B1 | AVG(TotalWorkingYears) | [{"table": "sheet1", "column": "TotalWorkingYears"}] | [] | False |
| B1 | AVG(YearsAtCompany) | [{"table": "sheet1", "column": "YearsAtCompany"}] | [] | False |
| B1 | AVG(Age) | [{"table": "sheet1", "column": "Age"}] | [] | False |
| B1 | AVG(DistanceFromHome) | [{"table": "sheet1", "column": "DistanceFromHome"}] | [] | False |
| B1 | AVG(JobSatisfaction) | [{"table": "sheet1", "column": "JobSatisfaction"}] | [] | False |
| B1 | AVG(EnvironmentSatisfaction) | [{"table": "sheet1", "column": "EnvironmentSatisfaction"}] | [] | False |
| B1 | AVG(JobInvolvement) | [{"table": "sheet1", "column": "JobInvolvement"}] | [] | False |
| B1 | AVG(WorkLifeBalance) | [{"table": "sheet1", "column": "WorkLifeBalance"}] | [] | False |
| B1 | AVG(RelationshipSatisfaction) | [{"table": "sheet1", "column": "RelationshipSatisfaction"}] | [] | False |
| B1 | AVG(PercentSalaryHike) | [{"table": "sheet1", "column": "PercentSalaryHike"}] | [] | False |
| B1 | AVG(StockOptionLevel) | [{"table": "sheet1", "column": "StockOptionLevel"}] | [] | False |
| B1 | AVG(TrainingTimesLastYear) | [{"table": "sheet1", "column": "TrainingTimesLastYear"}] | [] | False |
| B1 | AVG(YearsSinceLastPromotion) | [{"table": "sheet1", "column": "YearsSinceLastPromotion"}] | [] | False |
| B1 | AVG(YearsInCurrentRole) | [{"table": "sheet1", "column": "YearsInCurrentRole"}] | [] | False |
| B1 | AVG(YearsWithCurrManager) | [{"table": "sheet1", "column": "YearsWithCurrManager"}] | [] | False |


## S7

类别 `data`；来源 `query_db`；调用 `b09c357a21ec4a5ba44966aeacec0cdf`；状态 `success`。

```sql
SELECT Department, JobRole, COUNT(*) AS total, ROUND(100.0*COUNT(*)/SUM(COUNT(*)) OVER (PARTITION BY Department),1) AS pct_of_dept FROM sheet1 GROUP BY Department, JobRole ORDER BY Department, pct_of_dept DESC;
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-007/attempt-01/sql/S7.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-007/attempt-01/sql/S7.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-007/attempt-01/results/S7.rows.jsonl)；完整：True；SHA256：`440c0de86f3d9974e1667f3376b67a76abed39b61f5fcf59750cc5b1d36117d0`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "sheet1", "kind": "base", "block": null, "base_tables": ["sheet1"]}] | [] | ["Department", "JobRole"] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |
| B1 | COUNT(*) | [] | [] | True |
| B1 | COUNT(*) | [] | [] | True |


## S8

类别 `data`；来源 `query_db`；调用 `af7799d60c0445e2957676af2e503829`；状态 `success`。

```sql
SELECT Department, JobLevel, COUNT(*) AS total, SUM(CASE WHEN Attrition='Yes' THEN 1 ELSE 0 END) AS att, ROUND(100.0*SUM(CASE WHEN Attrition='Yes' THEN 1 ELSE 0 END)/COUNT(*),2) AS att_rate FROM sheet1 GROUP BY Department, JobLevel ORDER BY Department, JobLevel;
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-007/attempt-01/sql/S8.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-007/attempt-01/sql/S8.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-007/attempt-01/results/S8.rows.jsonl)；完整：True；SHA256：`c469cc226c7ecaa74e47712c10221c1f3e77a52331d5354e41e1a4f9b6936c07`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "sheet1", "kind": "base", "block": null, "base_tables": ["sheet1"]}] | [] | ["Department", "JobLevel"] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |
| B1 | SUM(CASE WHEN Attrition = 'Yes' THEN 1 ELSE 0 END) | [] | [{"table": "sheet1", "column": "Attrition"}] | False |
| B1 | COUNT(*) | [] | [] | True |
| B1 | SUM(CASE WHEN Attrition = 'Yes' THEN 1 ELSE 0 END) | [] | [{"table": "sheet1", "column": "Attrition"}] | False |


## S9

类别 `data`；来源 `query_db`；调用 `e378921f2f6a4870b23acf0144fffe6b`；状态 `success`。

```sql
SELECT Department, JobLevel, COUNT(*) AS total, SUM(CASE WHEN Attrition='Yes' THEN 1 ELSE 0 END) AS att FROM sheet1 WHERE Department='Sales' GROUP BY Department, JobLevel ORDER BY JobLevel;
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-007/attempt-01/sql/S9.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-007/attempt-01/sql/S9.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-007/attempt-01/results/S9.rows.jsonl)；完整：True；SHA256：`62c71fcf81efee7eb5fb1a32179b02b05219c3d00fe214471ee13317203e8508`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "sheet1", "kind": "base", "block": null, "base_tables": ["sheet1"]}] | [] | ["Department", "JobLevel"] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |
| B1 | SUM(CASE WHEN Attrition = 'Yes' THEN 1 ELSE 0 END) | [] | [{"table": "sheet1", "column": "Attrition"}] | False |


## S10

类别 `data`；来源 `query_db`；调用 `9b7ceccd5ef0400ba499f4e20ba82cdd`；状态 `success`。

```sql
SELECT Department, JobRole, AVG(MonthlyIncome) AS avg_income, AVG(JobLevel) AS avg_joblevel, AVG(YearsAtCompany) AS avg_tenure, AVG(TotalWorkingYears) AS avg_twy, AVG(Age) AS avg_age FROM sheet1 GROUP BY Department, JobRole ORDER BY Department, avg_income;
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-007/attempt-01/sql/S10.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-007/attempt-01/sql/S10.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-007/attempt-01/results/S10.rows.jsonl)；完整：True；SHA256：`a84953f5d1a252fb00e202e49d7f38d29b5dcb12de640e121bd9f3031d903d3a`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "sheet1", "kind": "base", "block": null, "base_tables": ["sheet1"]}] | [] | ["Department", "JobRole"] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | AVG(MonthlyIncome) | [{"table": "sheet1", "column": "MonthlyIncome"}] | [] | False |
| B1 | AVG(JobLevel) | [{"table": "sheet1", "column": "JobLevel"}] | [] | False |
| B1 | AVG(YearsAtCompany) | [{"table": "sheet1", "column": "YearsAtCompany"}] | [] | False |
| B1 | AVG(TotalWorkingYears) | [{"table": "sheet1", "column": "TotalWorkingYears"}] | [] | False |
| B1 | AVG(Age) | [{"table": "sheet1", "column": "Age"}] | [] | False |


## S11

类别 `data`；来源 `query_db`；调用 `fc623876521243f3ba0dbd9258d39ec7`；状态 `success`。

```sql
SELECT Department, OverTime, COUNT(*) AS total, SUM(CASE WHEN Attrition='Yes' THEN 1 ELSE 0 END) AS att, ROUND(100.0*SUM(CASE WHEN Attrition='Yes' THEN 1 ELSE 0 END)/COUNT(*),2) AS att_rate FROM sheet1 GROUP BY Department, OverTime ORDER BY Department, OverTime;
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-007/attempt-01/sql/S11.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-007/attempt-01/sql/S11.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-007/attempt-01/results/S11.rows.jsonl)；完整：True；SHA256：`08a359e3fa71e2bdbc605f2c0aa20375e39ecd7f5fefc1c3b872524ec95ceb59`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "sheet1", "kind": "base", "block": null, "base_tables": ["sheet1"]}] | [] | ["Department", "OverTime"] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |
| B1 | SUM(CASE WHEN Attrition = 'Yes' THEN 1 ELSE 0 END) | [] | [{"table": "sheet1", "column": "Attrition"}] | False |
| B1 | COUNT(*) | [] | [] | True |
| B1 | SUM(CASE WHEN Attrition = 'Yes' THEN 1 ELSE 0 END) | [] | [{"table": "sheet1", "column": "Attrition"}] | False |


## S12

类别 `data`；来源 `query_db`；调用 `9c2b1108ac464098a37423ba2ab1ede5`；状态 `success`。

```sql
SELECT Department, BusinessTravel, COUNT(*) AS total, SUM(CASE WHEN Attrition='Yes' THEN 1 ELSE 0 END) AS att, ROUND(100.0*SUM(CASE WHEN Attrition='Yes' THEN 1 ELSE 0 END)/COUNT(*),2) AS att_rate FROM sheet1 GROUP BY Department, BusinessTravel ORDER BY Department, BusinessTravel;
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-007/attempt-01/sql/S12.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-007/attempt-01/sql/S12.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-007/attempt-01/results/S12.rows.jsonl)；完整：True；SHA256：`770a9e27742fd1e01e46280b169e81cbd1ba3d5886d8058b4db369d86ff31294`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "sheet1", "kind": "base", "block": null, "base_tables": ["sheet1"]}] | [] | ["Department", "BusinessTravel"] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |
| B1 | SUM(CASE WHEN Attrition = 'Yes' THEN 1 ELSE 0 END) | [] | [{"table": "sheet1", "column": "Attrition"}] | False |
| B1 | COUNT(*) | [] | [] | True |
| B1 | SUM(CASE WHEN Attrition = 'Yes' THEN 1 ELSE 0 END) | [] | [{"table": "sheet1", "column": "Attrition"}] | False |


## S13

类别 `data`；来源 `query_db`；调用 `78c15c46421b4676ae87035bbe408eea`；状态 `success`。

```sql
SELECT Department, MaritalStatus, COUNT(*) AS total, SUM(CASE WHEN Attrition='Yes' THEN 1 ELSE 0 END) AS att, ROUND(100.0*SUM(CASE WHEN Attrition='Yes' THEN 1 ELSE 0 END)/COUNT(*),2) AS att_rate FROM sheet1 GROUP BY Department, MaritalStatus ORDER BY Department, MaritalStatus;
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-007/attempt-01/sql/S13.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-007/attempt-01/sql/S13.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-007/attempt-01/results/S13.rows.jsonl)；完整：True；SHA256：`3009510c727aac5c715549228ba4b70d9a509b8f255bd9f9e56a1f23e7381b1b`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "sheet1", "kind": "base", "block": null, "base_tables": ["sheet1"]}] | [] | ["Department", "MaritalStatus"] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |
| B1 | SUM(CASE WHEN Attrition = 'Yes' THEN 1 ELSE 0 END) | [] | [{"table": "sheet1", "column": "Attrition"}] | False |
| B1 | COUNT(*) | [] | [] | True |
| B1 | SUM(CASE WHEN Attrition = 'Yes' THEN 1 ELSE 0 END) | [] | [{"table": "sheet1", "column": "Attrition"}] | False |


## S14

类别 `data`；来源 `query_db`；调用 `f50cfb1eeb20424681ba21dde182e7ce`；状态 `success`。

```sql
SELECT Department, StockOptionLevel, COUNT(*) AS total, SUM(CASE WHEN Attrition='Yes' THEN 1 ELSE 0 END) AS att, ROUND(100.0*SUM(CASE WHEN Attrition='Yes' THEN 1 ELSE 0 END)/COUNT(*),2) AS att_rate FROM sheet1 GROUP BY Department, StockOptionLevel ORDER BY Department, StockOptionLevel;
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-007/attempt-01/sql/S14.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-007/attempt-01/sql/S14.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-007/attempt-01/results/S14.rows.jsonl)；完整：True；SHA256：`0176cc8344a903b9ec55ae013948bbcca364e947c108c75061aa4a51d327cc34`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "sheet1", "kind": "base", "block": null, "base_tables": ["sheet1"]}] | [] | ["Department", "StockOptionLevel"] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |
| B1 | SUM(CASE WHEN Attrition = 'Yes' THEN 1 ELSE 0 END) | [] | [{"table": "sheet1", "column": "Attrition"}] | False |
| B1 | COUNT(*) | [] | [] | True |
| B1 | SUM(CASE WHEN Attrition = 'Yes' THEN 1 ELSE 0 END) | [] | [{"table": "sheet1", "column": "Attrition"}] | False |


## S15

类别 `data`；来源 `query_db`；调用 `ed7260a99abc417c8c4a50d739d492d6`；状态 `success`。

```sql
SELECT Department, SalarySlab, COUNT(*) AS total, SUM(CASE WHEN Attrition='Yes' THEN 1 ELSE 0 END) AS att, ROUND(100.0*SUM(CASE WHEN Attrition='Yes' THEN 1 ELSE 0 END)/COUNT(*),2) AS att_rate FROM sheet1 GROUP BY Department, SalarySlab ORDER BY Department, SalarySlab;
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-007/attempt-01/sql/S15.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-007/attempt-01/sql/S15.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-007/attempt-01/results/S15.rows.jsonl)；完整：True；SHA256：`9515a7ff5a6f55e5a65dd0096b179ddc8b0a7023a9f30fa43a9d35ec799f119f`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "sheet1", "kind": "base", "block": null, "base_tables": ["sheet1"]}] | [] | ["Department", "SalarySlab"] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |
| B1 | SUM(CASE WHEN Attrition = 'Yes' THEN 1 ELSE 0 END) | [] | [{"table": "sheet1", "column": "Attrition"}] | False |
| B1 | COUNT(*) | [] | [] | True |
| B1 | SUM(CASE WHEN Attrition = 'Yes' THEN 1 ELSE 0 END) | [] | [{"table": "sheet1", "column": "Attrition"}] | False |


## S16

类别 `data`；来源 `query_db`；调用 `ee3ad3a1da6b4b8f962d38a53b8e39e6`；状态 `success`。

```sql
SELECT Department, EducationField, COUNT(*) AS total, SUM(CASE WHEN Attrition='Yes' THEN 1 ELSE 0 END) AS att, ROUND(100.0*SUM(CASE WHEN Attrition='Yes' THEN 1 ELSE 0 END)/COUNT(*),2) AS att_rate FROM sheet1 GROUP BY Department, EducationField ORDER BY Department, EducationField;
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-007/attempt-01/sql/S16.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-007/attempt-01/sql/S16.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-007/attempt-01/results/S16.rows.jsonl)；完整：True；SHA256：`6466d7ba17e49de9e2a0c00ea503f826ebe6113d66e2e0bf311a6dc3d3c0de78`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "sheet1", "kind": "base", "block": null, "base_tables": ["sheet1"]}] | [] | ["Department", "EducationField"] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |
| B1 | SUM(CASE WHEN Attrition = 'Yes' THEN 1 ELSE 0 END) | [] | [{"table": "sheet1", "column": "Attrition"}] | False |
| B1 | COUNT(*) | [] | [] | True |
| B1 | SUM(CASE WHEN Attrition = 'Yes' THEN 1 ELSE 0 END) | [] | [{"table": "sheet1", "column": "Attrition"}] | False |


## S17

类别 `data`；来源 `query_db`；调用 `695d74dc35d4471cbf474a03d0b98d74`；状态 `success`。

```sql
SELECT Department, SalarySlab, COUNT(*) AS total, ROUND(100.0*COUNT(*)/SUM(COUNT(*)) OVER (PARTITION BY Department),1) AS pct_of_dept FROM sheet1 GROUP BY Department, SalarySlab ORDER BY Department, SalarySlab;
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-007/attempt-01/sql/S17.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-007/attempt-01/sql/S17.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-007/attempt-01/results/S17.rows.jsonl)；完整：True；SHA256：`e414c26bcb143dc58741e039dbebe482875ddf516c2b6cc612d3dd02e9d40f33`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "sheet1", "kind": "base", "block": null, "base_tables": ["sheet1"]}] | [] | ["Department", "SalarySlab"] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |
| B1 | COUNT(*) | [] | [] | True |
| B1 | COUNT(*) | [] | [] | True |


## S18

类别 `data`；来源 `query_db`；调用 `d001d589b48d445898e73f2fb364c286`；状态 `success`。

```sql
SELECT Department, AgeGroup, COUNT(*) AS total, SUM(CASE WHEN Attrition='Yes' THEN 1 ELSE 0 END) AS att, ROUND(100.0*SUM(CASE WHEN Attrition='Yes' THEN 1 ELSE 0 END)/COUNT(*),2) AS att_rate FROM sheet1 GROUP BY Department, AgeGroup ORDER BY Department, AgeGroup;
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-007/attempt-01/sql/S18.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-007/attempt-01/sql/S18.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-007/attempt-01/results/S18.rows.jsonl)；完整：True；SHA256：`32ecc2ed7552ecdb309b79c493fef00506f0154458286fa55d73d1cf8e17e738`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "sheet1", "kind": "base", "block": null, "base_tables": ["sheet1"]}] | [] | ["Department", "AgeGroup"] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |
| B1 | SUM(CASE WHEN Attrition = 'Yes' THEN 1 ELSE 0 END) | [] | [{"table": "sheet1", "column": "Attrition"}] | False |
| B1 | COUNT(*) | [] | [] | True |
| B1 | SUM(CASE WHEN Attrition = 'Yes' THEN 1 ELSE 0 END) | [] | [{"table": "sheet1", "column": "Attrition"}] | False |


## S19

类别 `data`；来源 `query_db`；调用 `a27d9093eec44cff8355cf8557eb59e0`；状态 `success`。

```sql
SELECT Department, AgeGroup, COUNT(*) AS total, SUM(CASE WHEN Attrition='Yes' THEN 1 ELSE 0 END) AS att, ROUND(100.0*SUM(CASE WHEN Attrition='Yes' THEN 1 ELSE 0 END)/COUNT(*),2) AS att_rate FROM sheet1 WHERE Department='Sales' GROUP BY Department, AgeGroup ORDER BY AgeGroup;
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-007/attempt-01/sql/S19.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-007/attempt-01/sql/S19.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-007/attempt-01/results/S19.rows.jsonl)；完整：True；SHA256：`969131f2da78d3811ec90123b7f4dc96cd7489e1d5917fb565f14e9e02f27090`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "sheet1", "kind": "base", "block": null, "base_tables": ["sheet1"]}] | [] | ["Department", "AgeGroup"] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |
| B1 | SUM(CASE WHEN Attrition = 'Yes' THEN 1 ELSE 0 END) | [] | [{"table": "sheet1", "column": "Attrition"}] | False |
| B1 | COUNT(*) | [] | [] | True |
| B1 | SUM(CASE WHEN Attrition = 'Yes' THEN 1 ELSE 0 END) | [] | [{"table": "sheet1", "column": "Attrition"}] | False |


## S20

类别 `data`；来源 `query_db`；调用 `cfb1b3c1509742abb1d849ac956b1a8c`；状态 `success`。

```sql
SELECT Department, JobSatisfaction, COUNT(*) AS total, SUM(CASE WHEN Attrition='Yes' THEN 1 ELSE 0 END) AS att, ROUND(100.0*SUM(CASE WHEN Attrition='Yes' THEN 1 ELSE 0 END)/COUNT(*),2) AS att_rate FROM sheet1 GROUP BY Department, JobSatisfaction ORDER BY Department, JobSatisfaction;
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-007/attempt-01/sql/S20.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-007/attempt-01/sql/S20.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-007/attempt-01/results/S20.rows.jsonl)；完整：True；SHA256：`c449e0664e0ba727d53a0c64aa380ff8162d011bb6f0ca20708bddd18baec5dc`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "sheet1", "kind": "base", "block": null, "base_tables": ["sheet1"]}] | [] | ["Department", "JobSatisfaction"] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |
| B1 | SUM(CASE WHEN Attrition = 'Yes' THEN 1 ELSE 0 END) | [] | [{"table": "sheet1", "column": "Attrition"}] | False |
| B1 | COUNT(*) | [] | [] | True |
| B1 | SUM(CASE WHEN Attrition = 'Yes' THEN 1 ELSE 0 END) | [] | [{"table": "sheet1", "column": "Attrition"}] | False |


## S21

类别 `data`；来源 `query_db`；调用 `a4c820f2fe6648f3802a1c0d5c99aad4`；状态 `success`。

```sql
SELECT Department, ROUND(100.0*SUM(CASE WHEN JobSatisfaction>=3 THEN 1 ELSE 0 END)/COUNT(*),1) AS pct_high_job_sat, ROUND(100.0*SUM(CASE WHEN EnvironmentSatisfaction>=3 THEN 1 ELSE 0 END)/COUNT(*),1) AS pct_high_env_sat, ROUND(100.0*SUM(CASE WHEN WorkLifeBalance>=3 THEN 1 ELSE 0 END)/COUNT(*),1) AS pct_good_wlb, ROUND(100.0*SUM(CASE WHEN JobInvolvement>=3 THEN 1 ELSE 0 END)/COUNT(*),1) AS pct_high_involvement, ROUND(100.0*SUM(CASE WHEN RelationshipSatisfaction>=3 THEN 1 ELSE 0 END)/COUNT(*),1) AS pct_high_rel_sat, ROUND(100.0*SUM(CASE WHEN PerformanceRating>=3 THEN 1 ELSE 0 END)/COUNT(*),1) AS pct_high_perf FROM sheet1 GROUP BY Department;
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-007/attempt-01/sql/S21.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-007/attempt-01/sql/S21.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-007/attempt-01/results/S21.rows.jsonl)；完整：True；SHA256：`552889c866d783b554ba903d4946d2d9ec5efc43bf4404e3bfcb1276c745f00e`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "sheet1", "kind": "base", "block": null, "base_tables": ["sheet1"]}] | [] | ["Department"] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |
| B1 | COUNT(*) | [] | [] | True |
| B1 | COUNT(*) | [] | [] | True |
| B1 | COUNT(*) | [] | [] | True |
| B1 | COUNT(*) | [] | [] | True |
| B1 | COUNT(*) | [] | [] | True |
| B1 | SUM(CASE WHEN JobSatisfaction >= 3 THEN 1 ELSE 0 END) | [] | [{"table": "sheet1", "column": "JobSatisfaction"}] | False |
| B1 | SUM(CASE WHEN EnvironmentSatisfaction >= 3 THEN 1 ELSE 0 END) | [] | [{"table": "sheet1", "column": "EnvironmentSatisfaction"}] | False |
| B1 | SUM(CASE WHEN WorkLifeBalance >= 3 THEN 1 ELSE 0 END) | [] | [{"table": "sheet1", "column": "WorkLifeBalance"}] | False |
| B1 | SUM(CASE WHEN JobInvolvement >= 3 THEN 1 ELSE 0 END) | [] | [{"table": "sheet1", "column": "JobInvolvement"}] | False |
| B1 | SUM(CASE WHEN RelationshipSatisfaction >= 3 THEN 1 ELSE 0 END) | [] | [{"table": "sheet1", "column": "RelationshipSatisfaction"}] | False |
| B1 | SUM(CASE WHEN PerformanceRating >= 3 THEN 1 ELSE 0 END) | [] | [{"table": "sheet1", "column": "PerformanceRating"}] | False |


## S22

类别 `data`；来源 `query_db`；调用 `668571042318499cac4e34ef50579a2f`；状态 `success`。

```sql
SELECT Department, Gender, COUNT(*) AS total, SUM(CASE WHEN Attrition='Yes' THEN 1 ELSE 0 END) AS att, ROUND(100.0*SUM(CASE WHEN Attrition='Yes' THEN 1 ELSE 0 END)/COUNT(*),2) AS att_rate, ROUND(100.0*COUNT(*)/SUM(COUNT(*)) OVER (PARTITION BY Department),1) AS gender_pct FROM sheet1 GROUP BY Department, Gender ORDER BY Department, Gender;
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-007/attempt-01/sql/S22.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-007/attempt-01/sql/S22.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-007/attempt-01/results/S22.rows.jsonl)；完整：True；SHA256：`e3aa7d52f45488f33e921deb5e7dd74e80f36ac88d0624c07e70f3053dfde630`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "sheet1", "kind": "base", "block": null, "base_tables": ["sheet1"]}] | [] | ["Department", "Gender"] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |
| B1 | SUM(CASE WHEN Attrition = 'Yes' THEN 1 ELSE 0 END) | [] | [{"table": "sheet1", "column": "Attrition"}] | False |
| B1 | COUNT(*) | [] | [] | True |
| B1 | SUM(CASE WHEN Attrition = 'Yes' THEN 1 ELSE 0 END) | [] | [{"table": "sheet1", "column": "Attrition"}] | False |
| B1 | COUNT(*) | [] | [] | True |
| B1 | COUNT(*) | [] | [] | True |


## S23

类别 `data`；来源 `query_db`；调用 `db6b5773ee474d709ae013e0a47a2214`；状态 `success`。

```sql
SELECT Department, CASE WHEN YearsAtCompany<=2 THEN '0-2y' WHEN YearsAtCompany<=5 THEN '3-5y' WHEN YearsAtCompany<=10 THEN '6-10y' ELSE '10y+' END AS tenure_bucket, COUNT(*) AS total, SUM(CASE WHEN Attrition='Yes' THEN 1 ELSE 0 END) AS att, ROUND(100.0*SUM(CASE WHEN Attrition='Yes' THEN 1 ELSE 0 END)/COUNT(*),2) AS att_rate FROM sheet1 GROUP BY Department, tenure_bucket ORDER BY Department, tenure_bucket;
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-007/attempt-01/sql/S23.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-007/attempt-01/sql/S23.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-007/attempt-01/results/S23.rows.jsonl)；完整：True；SHA256：`905c14fb023b2b2203df418d4857fafaed35ee77b0eccb64cbc3d0ec4d62058c`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "sheet1", "kind": "base", "block": null, "base_tables": ["sheet1"]}] | [] | ["Department", "CASE WHEN YearsAtCompany <= 2 THEN '0-2y' WHEN YearsAtCompany <= 5 THEN '3-5y' WHEN YearsAtCompany <= 10 THEN '6-10y' ELSE '10y+' END"] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |
| B1 | SUM(CASE WHEN Attrition = 'Yes' THEN 1 ELSE 0 END) | [] | [{"table": "sheet1", "column": "Attrition"}] | False |
| B1 | COUNT(*) | [] | [] | True |
| B1 | SUM(CASE WHEN Attrition = 'Yes' THEN 1 ELSE 0 END) | [] | [{"table": "sheet1", "column": "Attrition"}] | False |


## S24

类别 `data`；来源 `query_db`；调用 `858497318520466eb0941ce796cc0b22`；状态 `success`。

```sql
SELECT Department, CASE WHEN TotalWorkingYears<=2 THEN '0-2y' WHEN TotalWorkingYears<=5 THEN '3-5y' WHEN TotalWorkingYears<=10 THEN '6-10y' ELSE '10y+' END AS workexp_bucket, COUNT(*) AS total, SUM(CASE WHEN Attrition='Yes' THEN 1 ELSE 0 END) AS att, ROUND(100.0*SUM(CASE WHEN Attrition='Yes' THEN 1 ELSE 0 END)/COUNT(*),2) AS att_rate FROM sheet1 GROUP BY Department, workexp_bucket ORDER BY Department, workexp_bucket;
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-007/attempt-01/sql/S24.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-007/attempt-01/sql/S24.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-007/attempt-01/results/S24.rows.jsonl)；完整：True；SHA256：`6198698d67d3fdc823fe9f1f1d2fe5680a3d8e8d424300a460c7a48e66a0c5b2`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "sheet1", "kind": "base", "block": null, "base_tables": ["sheet1"]}] | [] | ["Department", "CASE WHEN TotalWorkingYears <= 2 THEN '0-2y' WHEN TotalWorkingYears <= 5 THEN '3-5y' WHEN TotalWorkingYears <= 10 THEN '6-10y' ELSE '10y+' END"] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |
| B1 | SUM(CASE WHEN Attrition = 'Yes' THEN 1 ELSE 0 END) | [] | [{"table": "sheet1", "column": "Attrition"}] | False |
| B1 | COUNT(*) | [] | [] | True |
| B1 | SUM(CASE WHEN Attrition = 'Yes' THEN 1 ELSE 0 END) | [] | [{"table": "sheet1", "column": "Attrition"}] | False |


## S25

类别 `data`；来源 `query_db`；调用 `6458364c4bfb4af48b79ba30ff892d69`；状态 `success`。

```sql
SELECT Department, CASE WHEN YearsAtCompany<=2 THEN '0-2y' WHEN YearsAtCompany<=5 THEN '3-5y' WHEN YearsAtCompany<=10 THEN '6-10y' ELSE '10y+' END AS tenure_bucket, COUNT(*) AS total, ROUND(100.0*COUNT(*)/SUM(COUNT(*)) OVER (PARTITION BY Department),1) AS pct_of_dept FROM sheet1 GROUP BY Department, tenure_bucket ORDER BY Department, tenure_bucket;
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-007/attempt-01/sql/S25.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-007/attempt-01/sql/S25.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-007/attempt-01/results/S25.rows.jsonl)；完整：True；SHA256：`89cfe6f9c9625d326573cec952c7e5103fa5440eb8e2f4bfc3ed9e1399e30096`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "sheet1", "kind": "base", "block": null, "base_tables": ["sheet1"]}] | [] | ["Department", "CASE WHEN YearsAtCompany <= 2 THEN '0-2y' WHEN YearsAtCompany <= 5 THEN '3-5y' WHEN YearsAtCompany <= 10 THEN '6-10y' ELSE '10y+' END"] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |
| B1 | COUNT(*) | [] | [] | True |
| B1 | COUNT(*) | [] | [] | True |


## S26

类别 `data`；来源 `query_db`；调用 `65349d5b9b04491da94bc72970bcc45e`；状态 `success`。

```sql
SELECT Department, ROUND(AVG(NumCompaniesWorked),2) AS avg_companies, ROUND(AVG(TrainingTimesLastYear),2) AS avg_training, ROUND(AVG(YearsSinceLastPromotion),2) AS avg_yrs_since_promo, ROUND(AVG(YearsInCurrentRole),2) AS avg_yrs_in_role, ROUND(AVG(YearsWithCurrManager),2) AS avg_yrs_mgr, ROUND(AVG(PercentSalaryHike),2) AS avg_hike, ROUND(AVG(Education),2) AS avg_education FROM sheet1 GROUP BY Department;
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-007/attempt-01/sql/S26.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-007/attempt-01/sql/S26.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-007/attempt-01/results/S26.rows.jsonl)；完整：True；SHA256：`473799c34b70807ce85180813bb45b85d9bae9d0d6c2907554945e8cead4cca9`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "sheet1", "kind": "base", "block": null, "base_tables": ["sheet1"]}] | [] | ["Department"] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | AVG(NumCompaniesWorked) | [{"table": "sheet1", "column": "NumCompaniesWorked"}] | [] | False |
| B1 | AVG(TrainingTimesLastYear) | [{"table": "sheet1", "column": "TrainingTimesLastYear"}] | [] | False |
| B1 | AVG(YearsSinceLastPromotion) | [{"table": "sheet1", "column": "YearsSinceLastPromotion"}] | [] | False |
| B1 | AVG(YearsInCurrentRole) | [{"table": "sheet1", "column": "YearsInCurrentRole"}] | [] | False |
| B1 | AVG(YearsWithCurrManager) | [{"table": "sheet1", "column": "YearsWithCurrManager"}] | [] | False |
| B1 | AVG(PercentSalaryHike) | [{"table": "sheet1", "column": "PercentSalaryHike"}] | [] | False |
| B1 | AVG(Education) | [{"table": "sheet1", "column": "Education"}] | [] | False |


## S27

类别 `data`；来源 `query_db`；调用 `030fa1fbfc0f4e5fbdd369e7d1b6984d`；状态 `success`。

```sql
SELECT Department, JobLevel, COUNT(*) AS total, ROUND(100.0*COUNT(*)/SUM(COUNT(*)) OVER (PARTITION BY Department),1) AS pct_of_dept, SUM(CASE WHEN Attrition='Yes' THEN 1 ELSE 0 END) AS att, ROUND(100.0*SUM(CASE WHEN Attrition='Yes' THEN 1 ELSE 0 END)/COUNT(*),2) AS att_rate FROM sheet1 GROUP BY Department, JobLevel ORDER BY Department, JobLevel;
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-007/attempt-01/sql/S27.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-007/attempt-01/sql/S27.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-007/attempt-01/results/S27.rows.jsonl)；完整：True；SHA256：`3fb1851be340e91dfeddb345791e87c4f596fe4eaa898cbff1b4190ca2729423`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "sheet1", "kind": "base", "block": null, "base_tables": ["sheet1"]}] | [] | ["Department", "JobLevel"] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |
| B1 | SUM(CASE WHEN Attrition = 'Yes' THEN 1 ELSE 0 END) | [] | [{"table": "sheet1", "column": "Attrition"}] | False |
| B1 | COUNT(*) | [] | [] | True |
| B1 | COUNT(*) | [] | [] | True |
| B1 | SUM(CASE WHEN Attrition = 'Yes' THEN 1 ELSE 0 END) | [] | [{"table": "sheet1", "column": "Attrition"}] | False |
| B1 | COUNT(*) | [] | [] | True |


## S28

类别 `data`；来源 `query_db`；调用 `dbdca29e1c124cf1878832b5a1bea55b`；状态 `success`。

```sql
SELECT Department, OverTime, COUNT(*) AS total, ROUND(100.0*COUNT(*)/SUM(COUNT(*)) OVER (PARTITION BY Department),1) AS pct_of_dept FROM sheet1 GROUP BY Department, OverTime ORDER BY Department, OverTime;
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-007/attempt-01/sql/S28.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-007/attempt-01/sql/S28.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-007/attempt-01/results/S28.rows.jsonl)；完整：True；SHA256：`0a1ce51ab3661fd6a48ee38e7be94009d7d31f102af83d5c95b373d1ae9cb251`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "sheet1", "kind": "base", "block": null, "base_tables": ["sheet1"]}] | [] | ["Department", "OverTime"] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |
| B1 | COUNT(*) | [] | [] | True |
| B1 | COUNT(*) | [] | [] | True |


## S29

类别 `data`；来源 `query_db`；调用 `28abe901932b4da5bc3a01fc0a0a0f04`；状态 `success`。

```sql
SELECT Department, JobLevel, COUNT(*) AS total, ROUND(100.0*COUNT(*)/SUM(COUNT(*)) OVER (PARTITION BY Department),1) AS pct_of_dept, SUM(CASE WHEN Attrition='Yes' THEN 1 ELSE 0 END) AS att, ROUND(100.0*SUM(CASE WHEN Attrition='Yes' THEN 1 ELSE 0 END)/COUNT(*),2) AS att_rate FROM sheet1 WHERE Department='Sales' GROUP BY Department, JobLevel ORDER BY JobLevel;
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-007/attempt-01/sql/S29.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-007/attempt-01/sql/S29.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-007/attempt-01/results/S29.rows.jsonl)；完整：True；SHA256：`880371e0940671927713390bf2b4262d2e84edbb702774a6218c2765fd548657`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "sheet1", "kind": "base", "block": null, "base_tables": ["sheet1"]}] | [] | ["Department", "JobLevel"] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |
| B1 | SUM(CASE WHEN Attrition = 'Yes' THEN 1 ELSE 0 END) | [] | [{"table": "sheet1", "column": "Attrition"}] | False |
| B1 | COUNT(*) | [] | [] | True |
| B1 | COUNT(*) | [] | [] | True |
| B1 | SUM(CASE WHEN Attrition = 'Yes' THEN 1 ELSE 0 END) | [] | [{"table": "sheet1", "column": "Attrition"}] | False |
| B1 | COUNT(*) | [] | [] | True |


## S30

类别 `data`；来源 `python`；调用 `8b6a6f23373a4792869dca3b275e613a`；状态 `success`。

```sql
SELECT * FROM sheet1
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-007/attempt-01/sql/S30.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-007/attempt-01/sql/S30.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-007/attempt-01/results/S30.rows.jsonl)；完整：True；SHA256：`aba219d46dbbe89f7055fb2639026d34755044efd37a5391982bd306d44d2d8f`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "sheet1", "kind": "base", "block": null, "base_tables": ["sheet1"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |


## S31

类别 `data`；来源 `python`；调用 `ea4823a8ab4345a496df589c2c912a68`；状态 `success`。

```sql
SELECT Department, JobLevel, Attrition FROM sheet1
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-007/attempt-01/sql/S31.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-007/attempt-01/sql/S31.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-007/attempt-01/results/S31.rows.jsonl)；完整：True；SHA256：`b9374e78897701fad648247169d8dd5f7df7717603cc8a4dae51ff6ae48c32a8`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "sheet1", "kind": "base", "block": null, "base_tables": ["sheet1"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |


## S32

类别 `data`；来源 `python`；调用 `f55744d60c9f42b6b7ebe4410e5060c7`；状态 `success`。

```sql
SELECT Department, JobLevel, Attrition FROM sheet1
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-007/attempt-01/sql/S32.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-007/attempt-01/sql/S32.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-007/attempt-01/results/S32.rows.jsonl)；完整：True；SHA256：`b9374e78897701fad648247169d8dd5f7df7717603cc8a4dae51ff6ae48c32a8`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "sheet1", "kind": "base", "block": null, "base_tables": ["sheet1"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |


## S33

类别 `data`；来源 `python`；调用 `3681f4874e92427486ee1faaf4ba1270`；状态 `success`。

```sql
SELECT * FROM sheet1
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-007/attempt-01/sql/S33.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-007/attempt-01/sql/S33.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-007/attempt-01/results/S33.rows.jsonl)；完整：True；SHA256：`aba219d46dbbe89f7055fb2639026d34755044efd37a5391982bd306d44d2d8f`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "sheet1", "kind": "base", "block": null, "base_tables": ["sheet1"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |


## S34

类别 `data`；来源 `python`；调用 `3bd0ca8d66b040258e4fba2c3748357c`；状态 `success`。

```sql
SELECT * FROM sheet1
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-007/attempt-01/sql/S34.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-007/attempt-01/sql/S34.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-007/attempt-01/results/S34.rows.jsonl)；完整：True；SHA256：`aba219d46dbbe89f7055fb2639026d34755044efd37a5391982bd306d44d2d8f`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "sheet1", "kind": "base", "block": null, "base_tables": ["sheet1"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |


## S35

类别 `data`；来源 `python`；调用 `5bdfa7ecf3764c1f9bcb102075fb1aa6`；状态 `success`。

```sql
SELECT * FROM sheet1
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-007/attempt-01/sql/S35.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-007/attempt-01/sql/S35.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-007/attempt-01/results/S35.rows.jsonl)；完整：True；SHA256：`aba219d46dbbe89f7055fb2639026d34755044efd37a5391982bd306d44d2d8f`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "sheet1", "kind": "base", "block": null, "base_tables": ["sheet1"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |


## S36

类别 `data`；来源 `python`；调用 `6b3aab329cc242eab6942678e06f75e4`；状态 `success`。

```sql
SELECT * FROM sheet1 WHERE EmpID IN (SELECT EmpID FROM sheet1 GROUP BY EmpID HAVING COUNT(*)>1) ORDER BY EmpID
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-007/attempt-01/sql/S36.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-007/attempt-01/sql/S36.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-007/attempt-01/results/S36.rows.jsonl)；完整：True；SHA256：`0c0216107f30b8cd174d38d2e4bf62815a932c7267f45fdfe8a2e8b7b3f5d43c`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "sheet1", "kind": "base", "block": null, "base_tables": ["sheet1"]}] | [] | ["EmpID"] |
| B2 | [{"alias": "sheet1", "kind": "base", "block": null, "base_tables": ["sheet1"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |


## S37

类别 `data`；来源 `python`；调用 `36b04481e11c452ebd205f7665d6cdbf`；状态 `success`。

```sql
SELECT * FROM sheet1
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-007/attempt-01/sql/S37.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-007/attempt-01/sql/S37.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-007/attempt-01/results/S37.rows.jsonl)；完整：True；SHA256：`aba219d46dbbe89f7055fb2639026d34755044efd37a5391982bd306d44d2d8f`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "sheet1", "kind": "base", "block": null, "base_tables": ["sheet1"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |


## S38

类别 `data`；来源 `python`；调用 `1c52b8079c5a42feab63dcca614657d6`；状态 `success`。

```sql
SELECT * FROM sheet1
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-007/attempt-01/sql/S38.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-007/attempt-01/sql/S38.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-007/attempt-01/results/S38.rows.jsonl)；完整：True；SHA256：`aba219d46dbbe89f7055fb2639026d34755044efd37a5391982bd306d44d2d8f`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "sheet1", "kind": "base", "block": null, "base_tables": ["sheet1"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |


## S39

类别 `data`；来源 `python`；调用 `b82885be88d34bd0909b6790e52130e1`；状态 `success`。

```sql
SELECT * FROM sheet1
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-007/attempt-01/sql/S39.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-007/attempt-01/sql/S39.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-007/attempt-01/results/S39.rows.jsonl)；完整：True；SHA256：`aba219d46dbbe89f7055fb2639026d34755044efd37a5391982bd306d44d2d8f`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "sheet1", "kind": "base", "block": null, "base_tables": ["sheet1"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |


## S40

类别 `data`；来源 `python`；调用 `0eefa70bb85b4e7da4f52d7881c418fc`；状态 `success`。

```sql
SELECT * FROM sheet1
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-007/attempt-01/sql/S40.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-007/attempt-01/sql/S40.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-007/attempt-01/results/S40.rows.jsonl)；完整：True；SHA256：`aba219d46dbbe89f7055fb2639026d34755044efd37a5391982bd306d44d2d8f`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "sheet1", "kind": "base", "block": null, "base_tables": ["sheet1"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |


## S41

类别 `data`；来源 `python`；调用 `7f12debf21204b489b45ddf90ef26a91`；状态 `success`。

```sql
SELECT * FROM sheet1
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-007/attempt-01/sql/S41.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-007/attempt-01/sql/S41.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-007/attempt-01/results/S41.rows.jsonl)；完整：True；SHA256：`aba219d46dbbe89f7055fb2639026d34755044efd37a5391982bd306d44d2d8f`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "sheet1", "kind": "base", "block": null, "base_tables": ["sheet1"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |


## S42

类别 `data`；来源 `python`；调用 `48c9aad045d94a09965d3d85c42afdf7`；状态 `success`。

```sql
SELECT * FROM sheet1
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-007/attempt-01/sql/S42.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-007/attempt-01/sql/S42.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-007/attempt-01/results/S42.rows.jsonl)；完整：True；SHA256：`aba219d46dbbe89f7055fb2639026d34755044efd37a5391982bd306d44d2d8f`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "sheet1", "kind": "base", "block": null, "base_tables": ["sheet1"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |


## S43

类别 `data`；来源 `query_db`；调用 `1fb4f08956394590aba34c1b4354d8d4`；状态 `success`。

```sql
SELECT Department, COUNT(*) AS total, ROUND(100.0*COUNT(*)/SUM(COUNT(*)) OVER (),1) AS pct_of_total, SUM(CASE WHEN Attrition='Yes' THEN 1 ELSE 0 END) AS att, ROUND(100.0*SUM(CASE WHEN Attrition='Yes' THEN 1 ELSE 0 END)/COUNT(*),2) AS att_rate, ROUND(100.0*SUM(CASE WHEN Attrition='Yes' THEN 1 ELSE 0 END)/ (SELECT SUM(CASE WHEN Attrition='Yes' THEN 1 ELSE 0 END) FROM sheet1),1) AS pct_of_all_attrition FROM sheet1 GROUP BY Department ORDER BY att_rate DESC;
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-007/attempt-01/sql/S43.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-007/attempt-01/sql/S43.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-007/attempt-01/results/S43.rows.jsonl)；完整：True；SHA256：`36e3f7e58fbb344896d20133a47f872d0550133aaec70e2c670202c6336a09df`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "sheet1", "kind": "base", "block": null, "base_tables": ["sheet1"]}] | [] | [] |
| B2 | [{"alias": "sheet1", "kind": "base", "block": null, "base_tables": ["sheet1"]}] | [] | ["Department"] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | SUM(CASE WHEN Attrition = 'Yes' THEN 1 ELSE 0 END) | [] | [{"table": "sheet1", "column": "Attrition"}] | False |
| B2 | COUNT(*) | [] | [] | True |
| B2 | SUM(CASE WHEN Attrition = 'Yes' THEN 1 ELSE 0 END) | [] | [{"table": "sheet1", "column": "Attrition"}] | False |
| B2 | COUNT(*) | [] | [] | True |
| B2 | COUNT(*) | [] | [] | True |
| B2 | SUM(CASE WHEN Attrition = 'Yes' THEN 1 ELSE 0 END) | [] | [{"table": "sheet1", "column": "Attrition"}] | False |
| B2 | SUM(CASE WHEN Attrition = 'Yes' THEN 1 ELSE 0 END) | [] | [{"table": "sheet1", "column": "Attrition"}] | False |
| B2 | COUNT(*) | [] | [] | True |

