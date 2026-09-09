# dacomp-031

Analyze employees’ current employment status at the company across different working years…

运行：已提交。官方未评分。全部 SQL 尝试/成功 40/39；数据 SQL 38/37；Python 2 次。

完整原题：

Analyze employees’ current employment status at the company across different working years intervals (0–5 years, 6–10 years, 11–15 years, 16–20 years, and 20+ years), and identify the characteristics of long-term retained employees at the company (10 years and above). Based on these data, what specific actions can the company take to increase employee tenure?

| 表 | 行数 | 列数 |
| --- | --- | --- |
| sheet1 | 1480 | 38 |


实际路线（分析者依据 SQL/源码概括，不代表 Agent 自述）：按工龄区间汇总在职/离职 → 比较长期留存员工的收入、加班、股权和晋升特征 → Python 相关分析 → 绘图及额外离职分组摘要。

数据库大小：503,808 字节。

## 数据 SQL

| SQL | 状态 | 基础表 | Join 输入/类型 | GROUP BY | 聚合表达式 | 结果行数 | 数据库 ms |
| --- | --- | --- | --- | --- | --- | --- | --- |
| [S3/Q1](#s3) | success | ["sheet1"] | 0 / {} | [] | ["COUNT(*)", "COUNT(DISTINCT EmpID)"] | 1 | 1.376 |
| [S4/Q2](#s4) | failed | ["sheet1"] | 0 / {} | [] | ["MIN(YearsAtCompany)", "MAX(YearsAtCompany)", "AVG(YearsAtCompany)", "PERCENTILE_CONT(YearsAtCompany, 0.5)"] | unknown | 未取得；调用总时长 0.161 ms |
| [S5/Q3](#s5) | success | ["sheet1"] | 0 / {} | ["Attrition"] | ["COUNT(*)"] | 2 | 0.787 |
| [S6/Q4](#s6) | success | ["sheet1"] | 0 / {} | [] | ["MIN(YearsAtCompany)", "MAX(YearsAtCompany)", "AVG(YearsAtCompany)", "AVG(CASE WHEN Attrition = 'No' THEN YearsAtCompany END)", "AVG(CASE WHEN Attrition = 'Yes' THEN YearsAtCompany END)"] | 1 | 0.888 |
| [S7/Q5](#s7) | success | ["sheet1"] | 0 / {} | ["CASE WHEN YearsAtCompany BETWEEN 0 AND 5 THEN '0-5 years' WHEN YearsAtCompany BETWEEN 6 AND 10 THEN '6-10 years' WHEN YearsAtCompany BETWEEN 11 AND 15 THEN '11-15 years' WHEN YearsAtCompany BETWEEN 16 AND 20 THEN '16-20 years' WHEN YearsAtCompany > 20 THEN '20+ years' END"] | ["COUNT(*)", "SUM(CASE WHEN Attrition = 'Yes' THEN 1 ELSE 0 END)", "SUM(CASE WHEN Attrition = 'No' THEN 1 ELSE 0 END)", "MIN(YearsAtCompany)", "COUNT(*)", "SUM(CASE WHEN Attrition = 'Yes' THEN 1 ELSE 0 END)"] | 5 | 1.318 |
| [S8/Q6](#s8) | success | ["sheet1"] | 0 / {} | ["CASE WHEN YearsAtCompany >= 10 THEN '10+ years (Long-term)' ELSE '<10 years' END"] | ["COUNT(*)", "AVG(Age)", "AVG(MonthlyIncome)", "AVG(PercentSalaryHike)", "AVG(JobSatisfaction)", "AVG(EnvironmentSatisfaction)", "AVG(WorkLifeBalance)", "AVG(JobInvolvement)", "AVG(RelationshipSatisfaction)", "AVG(PerformanceRating)", "AVG(StockOptionLevel)", "AVG(TrainingTimesLastYear)", "AVG(DistanceFromHome)", "AVG(NumCompaniesWorked)", "AVG(YearsSinceLastPromotion)", "AVG(YearsInCurrentRole)", "AVG(YearsWithCurrManager)"] | 2 | 2.567 |
| [S9/Q7](#s9) | success | ["sheet1"] | 0 / {} | ["CASE WHEN YearsAtCompany >= 10 THEN '10+ years' ELSE '<10 years' END", "Department"] | ["COUNT(*)", "COUNT(*)", "COUNT(*)"] | 6 | 1.467 |
| [S10/Q8](#s10) | success | ["sheet1"] | 0 / {} | ["CASE WHEN YearsAtCompany >= 10 THEN '10+ years' ELSE '<10 years' END", "JobRole"] | ["COUNT(*)", "COUNT(*)", "COUNT(*)"] | 18 | 1.566 |
| [S11/Q9](#s11) | success | ["sheet1"] | 0 / {} | ["CASE WHEN YearsAtCompany >= 10 THEN '10+ years' ELSE '<10 years' END", "OverTime"] | ["COUNT(*)", "COUNT(*)", "COUNT(*)"] | 4 | 1.473 |
| [S12/Q10](#s12) | success | ["sheet1"] | 0 / {} | ["CASE WHEN YearsAtCompany >= 10 THEN '10+ years' ELSE '<10 years' END", "MaritalStatus"] | ["COUNT(*)", "COUNT(*)", "COUNT(*)"] | 6 | 1.459 |
| [S13/Q11](#s13) | success | ["sheet1"] | 0 / {} | ["CASE WHEN YearsAtCompany >= 10 THEN '10+ years' ELSE '<10 years' END", "Gender"] | ["COUNT(*)", "COUNT(*)", "COUNT(*)"] | 4 | 1.286 |
| [S14/Q12](#s14) | success | ["sheet1"] | 0 / {} | ["CASE WHEN YearsAtCompany >= 10 THEN '10+ years' ELSE '<10 years' END", "Education"] | ["COUNT(*)", "COUNT(*)", "COUNT(*)"] | 10 | 1.361 |
| [S15/Q13](#s15) | success | ["sheet1"] | 0 / {} | ["CASE WHEN YearsAtCompany >= 10 THEN '10+ years' ELSE '<10 years' END", "BusinessTravel"] | ["COUNT(*)", "COUNT(*)", "COUNT(*)"] | 8 | 1.378 |
| [S16/Q14](#s16) | success | ["sheet1"] | 0 / {} | ["CASE WHEN YearsAtCompany >= 10 THEN '10+ years' ELSE '<10 years' END", "JobSatisfaction"] | ["COUNT(*)", "COUNT(*)", "COUNT(*)"] | 8 | 1.325 |
| [S17/Q15](#s17) | success | ["sheet1"] | 0 / {} | ["CASE WHEN YearsAtCompany >= 10 THEN '10+ years' ELSE '<10 years' END", "WorkLifeBalance"] | ["COUNT(*)", "COUNT(*)", "COUNT(*)"] | 8 | 1.374 |
| [S18/Q16](#s18) | success | ["sheet1"] | 0 / {} | ["CASE WHEN YearsAtCompany >= 10 THEN '10+ years' ELSE '<10 years' END", "SalarySlab"] | ["COUNT(*)", "COUNT(*)", "COUNT(*)"] | 8 | 1.444 |
| [S19/Q17](#s19) | success | ["sheet1"] | 0 / {} | ["YearsAtCompany"] | ["COUNT(*)", "SUM(CASE WHEN Attrition = 'Yes' THEN 1 ELSE 0 END)", "COUNT(*)", "SUM(CASE WHEN Attrition = 'Yes' THEN 1 ELSE 0 END)"] | 37 | 1.044 |
| [S20/Q18](#s20) | success | ["sheet1"] | 0 / {} | ["CASE WHEN YearsAtCompany BETWEEN 6 AND 10 THEN '6-10 years band' ELSE 'other' END"] | ["AVG(CASE WHEN Attrition = 'Yes' THEN MonthlyIncome END)", "AVG(CASE WHEN Attrition = 'No' THEN MonthlyIncome END)", "AVG(CASE WHEN Attrition = 'Yes' THEN YearsSinceLastPromotion END)", "AVG(CASE WHEN Attrition = 'No' THEN YearsSinceLastPromotion END)", "AVG(CASE WHEN Attrition = 'Yes' THEN JobSatisfaction END)", "AVG(CASE WHEN Attrition = 'No' THEN JobSatisfaction END)"] | 1 | 0.969 |
| [S21/Q19](#s21) | success | ["sheet1"] | 0 / {} | ["Attrition"] | ["COUNT(*)", "AVG(MonthlyIncome)", "AVG(YearsSinceLastPromotion)", "AVG(YearsAtCompany)", "AVG(JobSatisfaction)", "AVG(EnvironmentSatisfaction)", "AVG(WorkLifeBalance)", "AVG(TrainingTimesLastYear)", "AVG(OverTime = 'Yes')", "AVG(StockOptionLevel = 0)"] | 2 | 1.734 |
| [S22/Q20](#s22) | success | ["sheet1"] | 0 / {} | ["Attrition"] | ["AVG(CASE WHEN YearsSinceLastPromotion BETWEEN 0 AND 1 THEN 1 ELSE 0 END)", "AVG(CASE WHEN YearsSinceLastPromotion BETWEEN 2 AND 3 THEN 1 ELSE 0 END)", "AVG(CASE WHEN YearsSinceLastPromotion >= 4 THEN 1 ELSE 0 END)"] | 2 | 1.13 |
| [S23/Q21](#s23) | success | ["sheet1"] | 0 / {} | ["CASE WHEN YearsAtCompany >= 10 THEN '10+ years' ELSE '<10 years' END"] | ["AVG(MonthlyIncome)", "AVG(JobLevel)", "AVG(StockOptionLevel)", "AVG(YearsSinceLastPromotion)", "AVG(TotalWorkingYears)", "AVG(YearsInCurrentRole)", "AVG(CASE WHEN StockOptionLevel = 0 THEN 1 ELSE 0 END)"] | 2 | 1.485 |
| [S24/Q22](#s24) | success | ["sheet1"] | 0 / {} | ["YearsSinceLastPromotion"] | ["COUNT(*)", "SUM(CASE WHEN Attrition = 'Yes' THEN 1 ELSE 0 END)", "AVG(MonthlyIncome)", "COUNT(*)", "SUM(CASE WHEN Attrition = 'Yes' THEN 1 ELSE 0 END)"] | 9 | 1.085 |
| [S25/Q23](#s25) | success | ["sheet1"] | 0 / {} | ["CASE WHEN YearsAtCompany BETWEEN 0 AND 5 THEN '0-5 years' WHEN YearsAtCompany BETWEEN 6 AND 10 THEN '6-10 years' WHEN YearsAtCompany BETWEEN 11 AND 15 THEN '11-15 years' WHEN YearsAtCompany BETWEEN 16 AND 20 THEN '16-20 years' ELSE '20+ years' END"] | ["AVG(MonthlyIncome)", "AVG(JobLevel)", "AVG(YearsSinceLastPromotion)", "AVG(YearsInCurrentRole)", "AVG(YearsWithCurrManager)", "AVG(StockOptionLevel)", "AVG(JobSatisfaction)", "MIN(YearsAtCompany)"] | 5 | 1.712 |
| [S26/Q24](#s26) | success | ["sheet1"] | 0 / {} | ["CASE WHEN YearsAtCompany BETWEEN 6 AND 10 THEN '6-10 band' ELSE 'other' END", "OverTime", "Attrition"] | ["COUNT(*)", "COUNT(*)", "COUNT(*)"] | 4 | 1.037 |
| [S27/Q25](#s27) | success | ["sheet1"] | 0 / {} | ["Attrition"] | ["COUNT(*)", "AVG(MonthlyIncome)", "AVG(YearsSinceLastPromotion)", "AVG(JobSatisfaction)", "AVG(EnvironmentSatisfaction)", "AVG(WorkLifeBalance)", "AVG(DistanceFromHome)", "AVG(NumCompaniesWorked)"] | 2 | 0.957 |
| [S28/Q26](#s28) | success | ["sheet1"] | 0 / {} | ["Attrition"] | ["AVG(MonthlyIncome)", "AVG(JobSatisfaction)", "AVG(YearsSinceLastPromotion)", "COUNT(*)", "COUNT(*)", "SUM(CASE WHEN OverTime = 'Yes' THEN 1 ELSE 0 END)", "SUM(CASE WHEN StockOptionLevel = 0 THEN 1 ELSE 0 END)"] | 2 | 0.877 |
| [S29/Q27](#s29) | success | ["sheet1"] | 0 / {} | ["JobRole"] | ["COUNT(*)", "AVG(MonthlyIncome)", "AVG(YearsSinceLastPromotion)", "AVG(JobSatisfaction)", "AVG(YearsAtCompany)", "COUNT(*)", "SUM(CASE WHEN Attrition = 'Yes' THEN 1 ELSE 0 END)"] | 9 | 1.534 |
| [S30/Q28](#s30) | success | ["sheet1"] | 0 / {} | ["EducationField"] | ["COUNT(*)", "AVG(YearsAtCompany)", "COUNT(*)", "SUM(CASE WHEN Attrition = 'Yes' THEN 1 ELSE 0 END)"] | 6 | 1.173 |
| [S31/Q29](#s31) | success | ["sheet1"] | 0 / {} | [] | [] | 1480 | 5.29 |
| [S32/Q30](#s32) | success | ["sheet1"] | 0 / {} | [] | [] | 1480 | 2.698 |
| [S33/Q31](#s33) | success | ["sheet1"] | 0 / {} | ["CASE WHEN YearsAtCompany BETWEEN 0 AND 5 THEN '0-5 years' WHEN YearsAtCompany BETWEEN 6 AND 10 THEN '6-10 years' WHEN YearsAtCompany BETWEEN 11 AND 15 THEN '11-15 years' WHEN YearsAtCompany BETWEEN 16 AND 20 THEN '16-20 years' WHEN YearsAtCompany > 20 THEN '20+ years' END"] | ["COUNT(*)", "SUM(CASE WHEN Attrition = 'Yes' THEN 1 ELSE 0 END)", "MIN(YearsAtCompany)", "COUNT(*)", "SUM(CASE WHEN Attrition = 'Yes' THEN 1 ELSE 0 END)"] | 5 | 1.258 |
| [S34/Q32](#s34) | success | ["sheet1"] | 0 / {} | ["CASE WHEN YearsAtCompany >= 10 THEN '10+ Years' ELSE '<10 Years' END"] | ["COUNT(*)", "AVG(MonthlyIncome)", "AVG(YearsSinceLastPromotion)", "AVG(JobLevel)", "AVG(StockOptionLevel)", "AVG(JobSatisfaction)", "AVG(WorkLifeBalance)", "COUNT(*)", "COUNT(*)", "SUM(CASE WHEN OverTime = 'Yes' THEN 1 ELSE 0 END)", "SUM(CASE WHEN StockOptionLevel = 0 THEN 1 ELSE 0 END)"] | 2 | 1.763 |
| [S35/Q33](#s35) | success | ["sheet1"] | 0 / {} | ["CASE WHEN YearsAtCompany BETWEEN 0 AND 5 THEN '0-5 years' WHEN YearsAtCompany BETWEEN 6 AND 10 THEN '6-10 years' WHEN YearsAtCompany BETWEEN 11 AND 15 THEN '11-15 years' WHEN YearsAtCompany BETWEEN 16 AND 20 THEN '16-20 years' ELSE '20+ years' END"] | ["AVG(MonthlyIncome)", "AVG(JobLevel)", "AVG(YearsSinceLastPromotion)", "AVG(YearsInCurrentRole)", "MIN(YearsAtCompany)"] | 5 | 1.439 |
| [S36/Q34](#s36) | success | ["sheet1"] | 0 / {} | ["OverTime", "StockOptionLevel"] | ["COUNT(*)", "COUNT(*)", "SUM(CASE WHEN Attrition = 'Yes' THEN 1 ELSE 0 END)"] | 8 | 1.316 |
| [S37/Q35](#s37) | success | ["sheet1"] | 0 / {} | ["JobRole"] | ["COUNT(*)", "AVG(MonthlyIncome)", "AVG(YearsAtCompany)", "COUNT(*)", "SUM(CASE WHEN Attrition = 'Yes' THEN 1 ELSE 0 END)"] | 9 | 0.865 |
| [S38/Q36](#s38) | success | ["sheet1"] | 0 / {} | ["CASE WHEN YearsAtCompany >= 10 AND Attrition = 'No' THEN '10+ Stayer' WHEN YearsAtCompany >= 10 AND Attrition = 'Yes' THEN '10+ Leaver' WHEN YearsAtCompany < 10 AND Attrition = 'No' THEN '<10 Stayer' ELSE '<10 Leaver' END"] | ["COUNT(*)", "AVG(MonthlyIncome)", "AVG(JobSatisfaction)", "AVG(EnvironmentSatisfaction)", "AVG(CASE WHEN OverTime = 'Yes' THEN 1 ELSE 0 END)"] | 4 | 1.582 |
| [S39/Q37](#s39) | success | ["sheet1"] | 0 / {} | ["Attrition"] | ["AVG(MonthlyIncome)", "AVG(PercentSalaryHike)", "AVG(JobSatisfaction)", "AVG(TrainingTimesLastYear)", "AVG(CASE WHEN OverTime = 'Yes' THEN 1 ELSE 0 END)", "AVG(CASE WHEN StockOptionLevel = 0 THEN 1 ELSE 0 END)"] | 2 | 0.924 |
| [S40/Q38](#s40) | success | ["sheet1"] | 0 / {} | ["Attrition"] | ["AVG(YearsSinceLastPromotion)", "AVG(YearsInCurrentRole)", "AVG(NumCompaniesWorked)"] | 2 | 0.864 |


## 元数据和设置

| SQL | 类别 | 状态 | 内容 |
| --- | --- | --- | --- |
| S1 | connection_setup | success | PRAGMA query_only=ON |
| S2 | metadata | success | SELECT name,sql FROM sqlite_master WHERE type='table' ORDER BY name |


## Python 与执行位置

人工源码审查：**partial_violation**。SQL handles tenure bands, many attrition aggregates and windows. Python correlation and rendering are reasonable uses, but P1 groups leaver/stayer summaries and P2 rolls up attrition rates by unweighted pandas means. These are SQL-capable preparations, explicitly retained as actual Python operations rather than counted as SQL. This execution-location review is not an official answer-correctness judgment. [证据](../reviews/dacomp-031.json)。

P1：Correlation analysis and statistical testing (Pearson correlations, mean comparisons) are not supported by SQLite SQL, so the relevant numeric columns are retrieved once for this specific statistical step. Visualizations are also created here.

[源码](../../../runs/dsv4flash-db-first-full-01/dacomp-031/attempt-01/python/P1.py)；[输出](../../../runs/dsv4flash-db-first-full-01/dacomp-031/attempt-01/python/P1.stdout)；[错误](../../../runs/dsv4flash-db-first-full-01/dacomp-031/attempt-01/python/P1.stderr)。检出需人工核验的 SQL 可实现操作：groupby(, .query(, sort_values(；不能仅凭理由判为合规。

P2：Creating visualizations for the report: attrition by tenure band, key metric comparisons, income progression, and driver analysis. These are all visualizations (matplotlib/seaborn) which cannot be done in SQL.

[源码](../../../runs/dsv4flash-db-first-full-01/dacomp-031/attempt-01/python/P2.py)；[输出](../../../runs/dsv4flash-db-first-full-01/dacomp-031/attempt-01/python/P2.stdout)；[错误](../../../runs/dsv4flash-db-first-full-01/dacomp-031/attempt-01/python/P2.stderr)。检出需人工核验的 SQL 可实现操作：groupby(, .query(；不能仅凭理由判为合规。

## 优化机会

已验证候选。筛选限于精确 SQL、相同自包含 CTE、相同单表完整过滤、可分解单表聚合；未覆盖任意 Join 等价和一般谓词蕴含。全部候选都是 offline，未测在线预测。

| 候选 | 类型 | 已有结果 | 覆盖 SQL | 后续次数 | 中间行数 | 验证 | 成本 |
| --- | --- | --- | --- | --- | --- | --- | --- |
| C1 | aggregate MV | False | ["S5", "S6", "S7", "S8", "S19", "S21", "S22", "S23", "S25", "S29", "S30", "S33", "S34", "S35", "S36", "S38"] | 15 | 1051 | verified | Not benchmarked; correctness alone does not establish net speedup. |
| C2 | common filtered view | False | ["S20", "S27", "S37", "S39", "S40"] | 4 | 452 | verified | Not benchmarked; correctness alone does not establish net speedup. |
| C3 | aggregate MV | False | ["S20", "S37"] | 1 | 9 | verified | Not benchmarked; correctness alone does not establish net speedup. |


已验证覆盖（含触发查询、候选并集去重）：21/37 条成功数据 SQL。正确性仅针对当前数据库快照；未测性能的候选不能声称已加速。

[完整 build/rewrite 与比较证据](dacomp-031.analysis.json)。

### C1：aggregate MV

Union of grouping keys; decomposable aggregate states; AVG uses SUM and non-NULL COUNT.

原查询 [S5](#s5), [S6](#s6), [S7](#s7), [S8](#s8), [S19](#s19), [S21](#s21), [S22](#s22), [S23](#s23), [S25](#s25), [S29](#s29), [S30](#s30), [S33](#s33), [S34](#s34), [S35](#s35), [S36](#s36), [S38](#s38) → 新增共享状态 C1 → 后续 15 次可复用。该构建点为事后假设，不代表 Agent 当时预知后续。

构建定义：

```sql
SELECT attrition AS __g0, CASE WHEN yearsatcompany BETWEEN 0 AND 5 THEN '0-5 years' WHEN yearsatcompany BETWEEN 6 AND 10 THEN '6-10 years' WHEN yearsatcompany BETWEEN 11 AND 15 THEN '11-15 years' WHEN yearsatcompany BETWEEN 16 AND 20 THEN '16-20 years' WHEN yearsatcompany > 20 THEN '20+ years' END AS __g1, CASE WHEN yearsatcompany >= 10 THEN '10+ years (Long-term)' ELSE '<10 years' END AS __g2, yearsatcompany AS __g3, CASE WHEN yearsatcompany >= 10 THEN '10+ years' ELSE '<10 years' END AS __g4, CASE WHEN yearsatcompany BETWEEN 0 AND 5 THEN '0-5 years' WHEN yearsatcompany BETWEEN 6 AND 10 THEN '6-10 years' WHEN yearsatcompany BETWEEN 11 AND 15 THEN '11-15 years' WHEN yearsatcompany BETWEEN 16 AND 20 THEN '16-20 years' ELSE '20+ years' END AS __g5, jobrole AS __g6, educationfield AS __g7, CASE WHEN yearsatcompany >= 10 THEN '10+ Years' ELSE '<10 Years' END AS __g8, overtime AS __g9, stockoptionlevel AS __g10, CASE WHEN yearsatcompany >= 10 AND attrition = 'No' THEN '10+ Stayer' WHEN yearsatcompany >= 10 AND attrition = 'Yes' THEN '10+ Leaver' WHEN yearsatcompany < 10 AND attrition = 'No' THEN '<10 Stayer' ELSE '<10 Leaver' END AS __g11, COUNT(*) AS __a0, MIN(yearsatcompany) AS __a1, MAX(yearsatcompany) AS __a2, SUM(yearsatcompany) AS __a3_sum, COUNT(yearsatcompany) AS __a3_n, SUM(CASE WHEN attrition = 'No' THEN yearsatcompany END) AS __a4_sum, COUNT(CASE WHEN attrition = 'No' THEN yearsatcompany END) AS __a4_n, SUM(CASE WHEN attrition = 'Yes' THEN yearsatcompany END) AS __a5_sum, COUNT(CASE WHEN attrition = 'Yes' THEN yearsatcompany END) AS __a5_n, SUM(CASE WHEN attrition = 'Yes' THEN 1 ELSE 0 END) AS __a6, SUM(CASE WHEN attrition = 'No' THEN 1 ELSE 0 END) AS __a7, SUM(age) AS __a8_sum, COUNT(age) AS __a8_n, SUM(monthlyincome) AS __a9_sum, COUNT(monthlyincome) AS __a9_n, SUM(percentsalaryhike) AS __a10_sum, COUNT(percentsalaryhike) AS __a10_n, SUM(jobsatisfaction) AS __a11_sum, COUNT(jobsatisfaction) AS __a11_n, SUM(environmentsatisfaction) AS __a12_sum, COUNT(environmentsatisfaction) AS __a12_n, SUM(worklifebalance) AS __a13_sum, COUNT(worklifebalance) AS __a13_n, SUM(jobinvolvement) AS __a14_sum, COUNT(jobinvolvement) AS __a14_n, SUM(relationshipsatisfaction) AS __a15_sum, COUNT(relationshipsatisfaction) AS __a15_n, SUM(performancerating) AS __a16_sum, COUNT(performancerating) AS __a16_n, SUM(stockoptionlevel) AS __a17_sum, COUNT(stockoptionlevel) AS __a17_n, SUM(trainingtimeslastyear) AS __a18_sum, COUNT(trainingtimeslastyear) AS __a18_n, SUM(distancefromhome) AS __a19_sum, COUNT(distancefromhome) AS __a19_n, SUM(numcompaniesworked) AS __a20_sum, COUNT(numcompaniesworked) AS __a20_n, SUM(yearssincelastpromotion) AS __a21_sum, COUNT(yearssincelastpromotion) AS __a21_n, SUM(yearsincurrentrole) AS __a22_sum, COUNT(yearsincurrentrole) AS __a22_n, SUM(yearswithcurrmanager) AS __a23_sum, COUNT(yearswithcurrmanager) AS __a23_n, SUM(overtime = 'Yes') AS __a24_sum, COUNT(overtime = 'Yes') AS __a24_n, SUM(stockoptionlevel = 0) AS __a25_sum, COUNT(stockoptionlevel = 0) AS __a25_n, SUM(CASE WHEN yearssincelastpromotion BETWEEN 0 AND 1 THEN 1 ELSE 0 END) AS __a26_sum, COUNT(CASE WHEN yearssincelastpromotion BETWEEN 0 AND 1 THEN 1 ELSE 0 END) AS __a26_n, SUM(CASE WHEN yearssincelastpromotion BETWEEN 2 AND 3 THEN 1 ELSE 0 END) AS __a27_sum, COUNT(CASE WHEN yearssincelastpromotion BETWEEN 2 AND 3 THEN 1 ELSE 0 END) AS __a27_n, SUM(CASE WHEN yearssincelastpromotion >= 4 THEN 1 ELSE 0 END) AS __a28_sum, COUNT(CASE WHEN yearssincelastpromotion >= 4 THEN 1 ELSE 0 END) AS __a28_n, SUM(joblevel) AS __a29_sum, COUNT(joblevel) AS __a29_n, SUM(totalworkingyears) AS __a30_sum, COUNT(totalworkingyears) AS __a30_n, SUM(CASE WHEN stockoptionlevel = 0 THEN 1 ELSE 0 END) AS __a31_sum, COUNT(CASE WHEN stockoptionlevel = 0 THEN 1 ELSE 0 END) AS __a31_n, SUM(CASE WHEN overtime = 'Yes' THEN 1 ELSE 0 END) AS __a32, SUM(CASE WHEN stockoptionlevel = 0 THEN 1 ELSE 0 END) AS __a33, SUM(CASE WHEN overtime = 'Yes' THEN 1 ELSE 0 END) AS __a34_sum, COUNT(CASE WHEN overtime = 'Yes' THEN 1 ELSE 0 END) AS __a34_n FROM "sheet1"  GROUP BY attrition, CASE WHEN yearsatcompany BETWEEN 0 AND 5 THEN '0-5 years' WHEN yearsatcompany BETWEEN 6 AND 10 THEN '6-10 years' WHEN yearsatcompany BETWEEN 11 AND 15 THEN '11-15 years' WHEN yearsatcompany BETWEEN 16 AND 20 THEN '16-20 years' WHEN yearsatcompany > 20 THEN '20+ years' END, CASE WHEN yearsatcompany >= 10 THEN '10+ years (Long-term)' ELSE '<10 years' END, yearsatcompany, CASE WHEN yearsatcompany >= 10 THEN '10+ years' ELSE '<10 years' END, CASE WHEN yearsatcompany BETWEEN 0 AND 5 THEN '0-5 years' WHEN yearsatcompany BETWEEN 6 AND 10 THEN '6-10 years' WHEN yearsatcompany BETWEEN 11 AND 15 THEN '11-15 years' WHEN yearsatcompany BETWEEN 16 AND 20 THEN '16-20 years' ELSE '20+ years' END, jobrole, educationfield, CASE WHEN yearsatcompany >= 10 THEN '10+ Years' ELSE '<10 Years' END, overtime, stockoptionlevel, CASE WHEN yearsatcompany >= 10 AND attrition = 'No' THEN '10+ Stayer' WHEN yearsatcompany >= 10 AND attrition = 'Yes' THEN '10+ Leaver' WHEN yearsatcompany < 10 AND attrition = 'No' THEN '<10 Stayer' ELSE '<10 Leaver' END
```

受益查询 S5 的改写示例：

```sql
SELECT __g0 AS "Attrition", SUM(__a0) AS cnt FROM temp.reuse_candidate GROUP BY __g0
```

| 原 SQL | 列名一致 | 结果一致 | 比较方法 |
| --- | --- | --- | --- |
| S5 | True | True | exact_multiset |
| S6 | True | True | exact_multiset |
| S7 | True | True | ordered_numeric_tolerance |
| S8 | True | True | exact_multiset |
| S19 | True | True | ordered_numeric_tolerance |
| S21 | True | True | exact_multiset |
| S22 | True | True | exact_multiset |
| S23 | True | True | exact_multiset |
| S25 | True | True | ordered_numeric_tolerance |
| S29 | True | True | ordered_numeric_tolerance |
| S30 | True | True | ordered_numeric_tolerance |
| S33 | True | True | ordered_numeric_tolerance |
| S34 | True | True | ordered_numeric_tolerance |
| S35 | True | True | ordered_numeric_tolerance |
| S36 | True | True | ordered_numeric_tolerance |
| S38 | True | True | ordered_numeric_tolerance |


验证状态：verified；成本结论：Not benchmarked; correctness alone does not establish net speedup.

### C2：common filtered view

Same single source and complete filter; original filter retained.

原查询 [S20](#s20), [S27](#s27), [S37](#s37), [S39](#s39), [S40](#s40) → 新增共享状态 C2 → 后续 4 次可复用。该构建点为事后假设，不代表 Agent 当时预知后续。

构建定义：

```sql
SELECT * FROM "sheet1" WHERE yearsatcompany BETWEEN 6 AND 10
```

受益查询 S20 的改写示例：

```sql
SELECT CASE WHEN YearsAtCompany BETWEEN 6 AND 10 THEN '6-10 years band' ELSE 'other' END AS band, ROUND(AVG(CASE WHEN Attrition = 'Yes' THEN MonthlyIncome END), 2) AS leaver_income, ROUND(AVG(CASE WHEN Attrition = 'No' THEN MonthlyIncome END), 2) AS stayer_income, ROUND(AVG(CASE WHEN Attrition = 'Yes' THEN YearsSinceLastPromotion END), 2) AS leaver_years_since_promo, ROUND(AVG(CASE WHEN Attrition = 'No' THEN YearsSinceLastPromotion END), 2) AS stayer_years_since_promo, ROUND(AVG(CASE WHEN Attrition = 'Yes' THEN JobSatisfaction END), 2) AS leaver_jobsat, ROUND(AVG(CASE WHEN Attrition = 'No' THEN JobSatisfaction END), 2) AS stayer_jobsat FROM temp.reuse_candidate AS sheet1 WHERE YearsAtCompany BETWEEN 6 AND 10 GROUP BY band
```

| 原 SQL | 列名一致 | 结果一致 | 比较方法 |
| --- | --- | --- | --- |
| S20 | True | True | exact_multiset |
| S27 | True | True | exact_multiset |
| S37 | True | True | ordered_numeric_tolerance |
| S39 | True | True | exact_multiset |
| S40 | True | True | exact_multiset |


验证状态：verified；成本结论：Not benchmarked; correctness alone does not establish net speedup.

### C3：aggregate MV

Union of grouping keys; decomposable aggregate states; AVG uses SUM and non-NULL COUNT.

原查询 [S20](#s20), [S37](#s37) → 新增共享状态 C3 → 后续 1 次可复用。该构建点为事后假设，不代表 Agent 当时预知后续。

构建定义：

```sql
SELECT CASE WHEN yearsatcompany BETWEEN 6 AND 10 THEN '6-10 years band' ELSE 'other' END AS __g0, jobrole AS __g1, SUM(CASE WHEN attrition = 'Yes' THEN monthlyincome END) AS __a0_sum, COUNT(CASE WHEN attrition = 'Yes' THEN monthlyincome END) AS __a0_n, SUM(CASE WHEN attrition = 'No' THEN monthlyincome END) AS __a1_sum, COUNT(CASE WHEN attrition = 'No' THEN monthlyincome END) AS __a1_n, SUM(CASE WHEN attrition = 'Yes' THEN yearssincelastpromotion END) AS __a2_sum, COUNT(CASE WHEN attrition = 'Yes' THEN yearssincelastpromotion END) AS __a2_n, SUM(CASE WHEN attrition = 'No' THEN yearssincelastpromotion END) AS __a3_sum, COUNT(CASE WHEN attrition = 'No' THEN yearssincelastpromotion END) AS __a3_n, SUM(CASE WHEN attrition = 'Yes' THEN jobsatisfaction END) AS __a4_sum, COUNT(CASE WHEN attrition = 'Yes' THEN jobsatisfaction END) AS __a4_n, SUM(CASE WHEN attrition = 'No' THEN jobsatisfaction END) AS __a5_sum, COUNT(CASE WHEN attrition = 'No' THEN jobsatisfaction END) AS __a5_n, COUNT(*) AS __a6, SUM(monthlyincome) AS __a7_sum, COUNT(monthlyincome) AS __a7_n, SUM(yearsatcompany) AS __a8_sum, COUNT(yearsatcompany) AS __a8_n, SUM(CASE WHEN attrition = 'Yes' THEN 1 ELSE 0 END) AS __a9 FROM "sheet1" WHERE yearsatcompany BETWEEN 6 AND 10 GROUP BY CASE WHEN yearsatcompany BETWEEN 6 AND 10 THEN '6-10 years band' ELSE 'other' END, jobrole
```

受益查询 S20 的改写示例：

```sql
SELECT __g0 AS band, ROUND((1.0 * SUM(__a0_sum) / NULLIF(SUM(__a0_n), 0)), 2) AS leaver_income, ROUND((1.0 * SUM(__a1_sum) / NULLIF(SUM(__a1_n), 0)), 2) AS stayer_income, ROUND((1.0 * SUM(__a2_sum) / NULLIF(SUM(__a2_n), 0)), 2) AS leaver_years_since_promo, ROUND((1.0 * SUM(__a3_sum) / NULLIF(SUM(__a3_n), 0)), 2) AS stayer_years_since_promo, ROUND((1.0 * SUM(__a4_sum) / NULLIF(SUM(__a4_n), 0)), 2) AS leaver_jobsat, ROUND((1.0 * SUM(__a5_sum) / NULLIF(SUM(__a5_n), 0)), 2) AS stayer_jobsat FROM temp.reuse_candidate GROUP BY __g0
```

| 原 SQL | 列名一致 | 结果一致 | 比较方法 |
| --- | --- | --- | --- |
| S20 | True | True | exact_multiset |
| S37 | True | True | ordered_numeric_tolerance |


验证状态：verified；成本结论：Not benchmarked; correctness alone does not establish net speedup.

结果依赖：自动记录 SQL→Python 的接口父调用，以及源码中引用归档文件的消费者；字面值相同不认定因果。模型方向选择需要人工读取消息，尚未做全面因果标注。

[原始报告](../../../runs/dsv4flash-db-first-full-01/dacomp-031/attempt-01/answer.md)；[统一消息](../../../runs/dsv4flash-db-first-full-01/dacomp-031/attempt-01/messages.jsonl)；[原始 OpenCode 事件](../../../runs/dsv4flash-db-first-full-01/dacomp-031/attempt-01/opencode.jsonl)；[SQL 引擎日志](../../../runs/dsv4flash-db-first-full-01/dacomp-031/attempt-01/sql_journal.jsonl)。

[可读报告（本地图片链接规范化）](../answers/dacomp-031.md)。原始回答保留，分析结论未改写。

## S1

类别 `connection_setup`；来源 `connection`；调用 `6204d2bddeb444ed96a38fcbd4da8234`；状态 `success`。

```sql
PRAGMA query_only=ON
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-031/attempt-01/sql/S1.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-031/attempt-01/sql/S1.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-031/attempt-01/results/S1.rows.jsonl)；完整：True；SHA256：`e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`。

## S2

类别 `metadata`；来源 `list_db`；调用 `6204d2bddeb444ed96a38fcbd4da8234`；状态 `success`。

```sql
SELECT name,sql FROM sqlite_master WHERE type='table' ORDER BY name
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-031/attempt-01/sql/S2.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-031/attempt-01/sql/S2.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-031/attempt-01/results/S2.rows.jsonl)；完整：True；SHA256：`94731284c43bc8e5b144e13abccbd74adbf46917d68d6726705b8596d303b46c`。

## S3

类别 `data`；来源 `query_db`；调用 `a24cf62058424d858153495bbbda48a0`；状态 `success`。

```sql
SELECT COUNT(*) AS total_rows, COUNT(DISTINCT EmpID) AS distinct_emp FROM sheet1
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-031/attempt-01/sql/S3.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-031/attempt-01/sql/S3.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-031/attempt-01/results/S3.rows.jsonl)；完整：True；SHA256：`19ee377565f48c1032ac7b13f087f9a5ab76d976ad47b7eec1d6d12b316e4667`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "sheet1", "kind": "base", "block": null, "base_tables": ["sheet1"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |
| B1 | COUNT(DISTINCT EmpID) | [{"table": "sheet1", "column": "EmpID"}] | [] | False |


## S4

类别 `data`；来源 `query_db`；调用 `e07a8b14b58740939e671c0036dce427`；状态 `failed`。

```sql
SELECT MIN(YearsAtCompany) AS min_years, 
       MAX(YearsAtCompany) AS max_years, 
       AVG(YearsAtCompany) AS avg_years,
       MEDIAN(YearsAtCompany) AS median_years
FROM sheet1
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-031/attempt-01/sql/S4.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-031/attempt-01/sql/S4.parameters.json)。

错误：`OperationalError('no such function: MEDIAN')`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "sheet1", "kind": "base", "block": null, "base_tables": ["sheet1"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | MIN(YearsAtCompany) | [{"table": "sheet1", "column": "YearsAtCompany"}] | [] | False |
| B1 | MAX(YearsAtCompany) | [{"table": "sheet1", "column": "YearsAtCompany"}] | [] | False |
| B1 | AVG(YearsAtCompany) | [{"table": "sheet1", "column": "YearsAtCompany"}] | [] | False |
| B1 | PERCENTILE_CONT(YearsAtCompany, 0.5) | [{"table": "sheet1", "column": "YearsAtCompany"}] | [] | False |


## S5

类别 `data`；来源 `query_db`；调用 `5ba96338b93c4c8abdaa4855a8334a6a`；状态 `success`。

```sql
SELECT Attrition, COUNT(*) AS cnt FROM sheet1 GROUP BY Attrition
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-031/attempt-01/sql/S5.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-031/attempt-01/sql/S5.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-031/attempt-01/results/S5.rows.jsonl)；完整：True；SHA256：`25562d60b37967575f40ec6771a6cec7653380d39ae4c7483db1cf62fae105e2`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "sheet1", "kind": "base", "block": null, "base_tables": ["sheet1"]}] | [] | ["Attrition"] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |


## S6

类别 `data`；来源 `query_db`；调用 `46723d73039c4b548b002bfa79b65feb`；状态 `success`。

```sql
SELECT MIN(YearsAtCompany) AS min_years, 
       MAX(YearsAtCompany) AS max_years, 
       ROUND(AVG(YearsAtCompany),2) AS avg_years,
       ROUND(AVG(CASE WHEN Attrition='No' THEN YearsAtCompany END),2) AS avg_years_stayers,
       ROUND(AVG(CASE WHEN Attrition='Yes' THEN YearsAtCompany END),2) AS avg_years_leavers
FROM sheet1
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-031/attempt-01/sql/S6.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-031/attempt-01/sql/S6.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-031/attempt-01/results/S6.rows.jsonl)；完整：True；SHA256：`bad71da7bb1ebcf61c8e0a8705e94aa65451a51fd9088c0233c97b31811ba2f7`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "sheet1", "kind": "base", "block": null, "base_tables": ["sheet1"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | MIN(YearsAtCompany) | [{"table": "sheet1", "column": "YearsAtCompany"}] | [] | False |
| B1 | MAX(YearsAtCompany) | [{"table": "sheet1", "column": "YearsAtCompany"}] | [] | False |
| B1 | AVG(YearsAtCompany) | [{"table": "sheet1", "column": "YearsAtCompany"}] | [] | False |
| B1 | AVG(CASE WHEN Attrition = 'No' THEN YearsAtCompany END) | [{"table": "sheet1", "column": "YearsAtCompany"}] | [{"table": "sheet1", "column": "Attrition"}] | False |
| B1 | AVG(CASE WHEN Attrition = 'Yes' THEN YearsAtCompany END) | [{"table": "sheet1", "column": "YearsAtCompany"}] | [{"table": "sheet1", "column": "Attrition"}] | False |


## S7

类别 `data`；来源 `query_db`；调用 `0abc5fbf972246eda57fddc6ca11a90c`；状态 `success`。

```sql
SELECT CASE 
         WHEN YearsAtCompany BETWEEN 0 AND 5 THEN '0-5 years'
         WHEN YearsAtCompany BETWEEN 6 AND 10 THEN '6-10 years'
         WHEN YearsAtCompany BETWEEN 11 AND 15 THEN '11-15 years'
         WHEN YearsAtCompany BETWEEN 16 AND 20 THEN '16-20 years'
         WHEN YearsAtCompany > 20 THEN '20+ years'
       END AS tenure_band,
       COUNT(*) AS total_employees,
       SUM(CASE WHEN Attrition='Yes' THEN 1 ELSE 0 END) AS attrition_yes,
       SUM(CASE WHEN Attrition='No' THEN 1 ELSE 0 END) AS attrition_no,
       ROUND(100.0*SUM(CASE WHEN Attrition='Yes' THEN 1 ELSE 0 END)/COUNT(*),2) AS attrition_rate_pct
FROM sheet1
GROUP BY tenure_band
ORDER BY MIN(YearsAtCompany)
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-031/attempt-01/sql/S7.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-031/attempt-01/sql/S7.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-031/attempt-01/results/S7.rows.jsonl)；完整：True；SHA256：`258d4f4f20ab9919d3ae88ad8368d4df5c34b7b585046347fc3966da0b48bd65`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "sheet1", "kind": "base", "block": null, "base_tables": ["sheet1"]}] | [] | ["CASE WHEN YearsAtCompany BETWEEN 0 AND 5 THEN '0-5 years' WHEN YearsAtCompany BETWEEN 6 AND 10 THEN '6-10 years' WHEN YearsAtCompany BETWEEN 11 AND 15 THEN '11-15 years' WHEN YearsAtCompany BETWEEN 16 AND 20 THEN '16-20 years' WHEN YearsAtCompany > 20 THEN '20+ years' END"] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |
| B1 | SUM(CASE WHEN Attrition = 'Yes' THEN 1 ELSE 0 END) | [] | [{"table": "sheet1", "column": "Attrition"}] | False |
| B1 | SUM(CASE WHEN Attrition = 'No' THEN 1 ELSE 0 END) | [] | [{"table": "sheet1", "column": "Attrition"}] | False |
| B1 | MIN(YearsAtCompany) | [{"table": "sheet1", "column": "YearsAtCompany"}] | [] | False |
| B1 | COUNT(*) | [] | [] | True |
| B1 | SUM(CASE WHEN Attrition = 'Yes' THEN 1 ELSE 0 END) | [] | [{"table": "sheet1", "column": "Attrition"}] | False |


## S8

类别 `data`；来源 `query_db`；调用 `e64c0a1d68314726a338431b37973739`；状态 `success`。

```sql
SELECT 
  CASE WHEN YearsAtCompany >= 10 THEN '10+ years (Long-term)' ELSE '<10 years' END AS tenure_group,
  COUNT(*) AS cnt,
  ROUND(AVG(Age),2) AS avg_age,
  ROUND(AVG(MonthlyIncome),2) AS avg_monthly_income,
  ROUND(AVG(PercentSalaryHike),2) AS avg_salary_hike,
  ROUND(AVG(JobSatisfaction),2) AS avg_job_satisfaction,
  ROUND(AVG(EnvironmentSatisfaction),2) AS avg_env_satisfaction,
  ROUND(AVG(WorkLifeBalance),2) AS avg_work_life_balance,
  ROUND(AVG(JobInvolvement),2) AS avg_job_involvement,
  ROUND(AVG(RelationshipSatisfaction),2) AS avg_rel_satisfaction,
  ROUND(AVG(PerformanceRating),2) AS avg_perf_rating,
  ROUND(AVG(StockOptionLevel),2) AS avg_stock_option,
  ROUND(AVG(TrainingTimesLastYear),2) AS avg_training,
  ROUND(AVG(DistanceFromHome),2) AS avg_distance,
  ROUND(AVG(NumCompaniesWorked),2) AS avg_num_companies,
  ROUND(AVG(YearsSinceLastPromotion),2) AS avg_years_since_promo,
  ROUND(AVG(YearsInCurrentRole),2) AS avg_years_in_role,
  ROUND(AVG(YearsWithCurrManager),2) AS avg_years_with_mgr
FROM sheet1
GROUP BY tenure_group
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-031/attempt-01/sql/S8.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-031/attempt-01/sql/S8.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-031/attempt-01/results/S8.rows.jsonl)；完整：True；SHA256：`cf9235079683dfea33da3199a4ae1a98c1d8aaa9252383fb0234d87764f15dd0`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "sheet1", "kind": "base", "block": null, "base_tables": ["sheet1"]}] | [] | ["CASE WHEN YearsAtCompany >= 10 THEN '10+ years (Long-term)' ELSE '<10 years' END"] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |
| B1 | AVG(Age) | [{"table": "sheet1", "column": "Age"}] | [] | False |
| B1 | AVG(MonthlyIncome) | [{"table": "sheet1", "column": "MonthlyIncome"}] | [] | False |
| B1 | AVG(PercentSalaryHike) | [{"table": "sheet1", "column": "PercentSalaryHike"}] | [] | False |
| B1 | AVG(JobSatisfaction) | [{"table": "sheet1", "column": "JobSatisfaction"}] | [] | False |
| B1 | AVG(EnvironmentSatisfaction) | [{"table": "sheet1", "column": "EnvironmentSatisfaction"}] | [] | False |
| B1 | AVG(WorkLifeBalance) | [{"table": "sheet1", "column": "WorkLifeBalance"}] | [] | False |
| B1 | AVG(JobInvolvement) | [{"table": "sheet1", "column": "JobInvolvement"}] | [] | False |
| B1 | AVG(RelationshipSatisfaction) | [{"table": "sheet1", "column": "RelationshipSatisfaction"}] | [] | False |
| B1 | AVG(PerformanceRating) | [{"table": "sheet1", "column": "PerformanceRating"}] | [] | False |
| B1 | AVG(StockOptionLevel) | [{"table": "sheet1", "column": "StockOptionLevel"}] | [] | False |
| B1 | AVG(TrainingTimesLastYear) | [{"table": "sheet1", "column": "TrainingTimesLastYear"}] | [] | False |
| B1 | AVG(DistanceFromHome) | [{"table": "sheet1", "column": "DistanceFromHome"}] | [] | False |
| B1 | AVG(NumCompaniesWorked) | [{"table": "sheet1", "column": "NumCompaniesWorked"}] | [] | False |
| B1 | AVG(YearsSinceLastPromotion) | [{"table": "sheet1", "column": "YearsSinceLastPromotion"}] | [] | False |
| B1 | AVG(YearsInCurrentRole) | [{"table": "sheet1", "column": "YearsInCurrentRole"}] | [] | False |
| B1 | AVG(YearsWithCurrManager) | [{"table": "sheet1", "column": "YearsWithCurrManager"}] | [] | False |


## S9

类别 `data`；来源 `query_db`；调用 `4cf51634a67d42c4be10e1080c365c17`；状态 `success`。

```sql
SELECT 
  CASE WHEN YearsAtCompany >= 10 THEN '10+ years' ELSE '<10 years' END AS tenure_group,
  Department,
  COUNT(*) AS cnt,
  ROUND(100.0*COUNT(*)/SUM(COUNT(*)) OVER (PARTITION BY CASE WHEN YearsAtCompany >= 10 THEN '10+ years' ELSE '<10 years' END), 2) AS pct
FROM sheet1
GROUP BY tenure_group, Department
ORDER BY tenure_group, cnt DESC
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-031/attempt-01/sql/S9.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-031/attempt-01/sql/S9.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-031/attempt-01/results/S9.rows.jsonl)；完整：True；SHA256：`f5f2a00aaa787cd565bc437c84fb81a3c739659080b0b46b1abbcc323913267d`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "sheet1", "kind": "base", "block": null, "base_tables": ["sheet1"]}] | [] | ["CASE WHEN YearsAtCompany >= 10 THEN '10+ years' ELSE '<10 years' END", "Department"] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |
| B1 | COUNT(*) | [] | [] | True |
| B1 | COUNT(*) | [] | [] | True |


## S10

类别 `data`；来源 `query_db`；调用 `9e8b7306991541a6ae741d2ad508601a`；状态 `success`。

```sql
SELECT 
  CASE WHEN YearsAtCompany >= 10 THEN '10+ years' ELSE '<10 years' END AS tenure_group,
  JobRole, COUNT(*) AS cnt,
  ROUND(100.0*COUNT(*)/SUM(COUNT(*)) OVER (PARTITION BY CASE WHEN YearsAtCompany >= 10 THEN '10+ years' ELSE '<10 years' END),2) AS pct_in_group
FROM sheet1
GROUP BY tenure_group, JobRole
ORDER BY tenure_group, cnt DESC
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-031/attempt-01/sql/S10.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-031/attempt-01/sql/S10.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-031/attempt-01/results/S10.rows.jsonl)；完整：True；SHA256：`e5a25e823bfef5285251a5f1aff92523817cf9d0c73ebea1e2bf7bccb9d97f2d`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "sheet1", "kind": "base", "block": null, "base_tables": ["sheet1"]}] | [] | ["CASE WHEN YearsAtCompany >= 10 THEN '10+ years' ELSE '<10 years' END", "JobRole"] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |
| B1 | COUNT(*) | [] | [] | True |
| B1 | COUNT(*) | [] | [] | True |


## S11

类别 `data`；来源 `query_db`；调用 `eb402387b2bc47c6afee10cc75ba0788`；状态 `success`。

```sql
SELECT 
  CASE WHEN YearsAtCompany >= 10 THEN '10+ years' ELSE '<10 years' END AS tenure_group,
  OverTime, COUNT(*) AS cnt,
  ROUND(100.0*COUNT(*)/SUM(COUNT(*)) OVER (PARTITION BY CASE WHEN YearsAtCompany >= 10 THEN '10+ years' ELSE '<10 years' END),2) AS pct_in_group
FROM sheet1
GROUP BY tenure_group, OverTime
ORDER BY tenure_group, OverTime
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-031/attempt-01/sql/S11.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-031/attempt-01/sql/S11.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-031/attempt-01/results/S11.rows.jsonl)；完整：True；SHA256：`58f741a19f5596c982ee2382c69cbd0fa229c7cf80c9f1280ee6de981db9ab95`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "sheet1", "kind": "base", "block": null, "base_tables": ["sheet1"]}] | [] | ["CASE WHEN YearsAtCompany >= 10 THEN '10+ years' ELSE '<10 years' END", "OverTime"] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |
| B1 | COUNT(*) | [] | [] | True |
| B1 | COUNT(*) | [] | [] | True |


## S12

类别 `data`；来源 `query_db`；调用 `0d0a671a21fb455593a9f154944ba007`；状态 `success`。

```sql
SELECT 
  CASE WHEN YearsAtCompany >= 10 THEN '10+ years' ELSE '<10 years' END AS tenure_group,
  MaritalStatus, COUNT(*) AS cnt,
  ROUND(100.0*COUNT(*)/SUM(COUNT(*)) OVER (PARTITION BY CASE WHEN YearsAtCompany >= 10 THEN '10+ years' ELSE '<10 years' END),2) AS pct_in_group
FROM sheet1
GROUP BY tenure_group, MaritalStatus
ORDER BY tenure_group, MaritalStatus
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-031/attempt-01/sql/S12.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-031/attempt-01/sql/S12.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-031/attempt-01/results/S12.rows.jsonl)；完整：True；SHA256：`8edad6ccfe0ae4aa8c3c85fd9f1341c3a85e66e88600b04315ca30e3d84a236e`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "sheet1", "kind": "base", "block": null, "base_tables": ["sheet1"]}] | [] | ["CASE WHEN YearsAtCompany >= 10 THEN '10+ years' ELSE '<10 years' END", "MaritalStatus"] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |
| B1 | COUNT(*) | [] | [] | True |
| B1 | COUNT(*) | [] | [] | True |


## S13

类别 `data`；来源 `query_db`；调用 `f0e9df1f27164d7c966e66f2e9a78479`；状态 `success`。

```sql
SELECT 
  CASE WHEN YearsAtCompany >= 10 THEN '10+ years' ELSE '<10 years' END AS tenure_group,
  Gender, COUNT(*) AS cnt,
  ROUND(100.0*COUNT(*)/SUM(COUNT(*)) OVER (PARTITION BY CASE WHEN YearsAtCompany >= 10 THEN '10+ years' ELSE '<10 years' END),2) AS pct_in_group
FROM sheet1
GROUP BY tenure_group, Gender
ORDER BY tenure_group, Gender
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-031/attempt-01/sql/S13.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-031/attempt-01/sql/S13.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-031/attempt-01/results/S13.rows.jsonl)；完整：True；SHA256：`e10898da5977bdab8edd6dcc2dacffd6bf00b0ee59d046f7c297951c9a93d9f5`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "sheet1", "kind": "base", "block": null, "base_tables": ["sheet1"]}] | [] | ["CASE WHEN YearsAtCompany >= 10 THEN '10+ years' ELSE '<10 years' END", "Gender"] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |
| B1 | COUNT(*) | [] | [] | True |
| B1 | COUNT(*) | [] | [] | True |


## S14

类别 `data`；来源 `query_db`；调用 `147db5603bbc4d3b9435bd07b512d066`；状态 `success`。

```sql
SELECT 
  CASE WHEN YearsAtCompany >= 10 THEN '10+ years' ELSE '<10 years' END AS tenure_group,
  Education, COUNT(*) AS cnt,
  ROUND(100.0*COUNT(*)/SUM(COUNT(*)) OVER (PARTITION BY CASE WHEN YearsAtCompany >= 10 THEN '10+ years' ELSE '<10 years' END),2) AS pct_in_group
FROM sheet1
GROUP BY tenure_group, Education
ORDER BY tenure_group, Education
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-031/attempt-01/sql/S14.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-031/attempt-01/sql/S14.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-031/attempt-01/results/S14.rows.jsonl)；完整：True；SHA256：`db693a8304856bf8d549aeaeebddb6b9fa89988abeebec161a209a8dee85da4b`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "sheet1", "kind": "base", "block": null, "base_tables": ["sheet1"]}] | [] | ["CASE WHEN YearsAtCompany >= 10 THEN '10+ years' ELSE '<10 years' END", "Education"] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |
| B1 | COUNT(*) | [] | [] | True |
| B1 | COUNT(*) | [] | [] | True |


## S15

类别 `data`；来源 `query_db`；调用 `d9bf0d77dbc74f46b4d1dbc4d46e5ab4`；状态 `success`。

```sql
SELECT 
  CASE WHEN YearsAtCompany >= 10 THEN '10+ years' ELSE '<10 years' END AS tenure_group,
  BusinessTravel, COUNT(*) AS cnt,
  ROUND(100.0*COUNT(*)/SUM(COUNT(*)) OVER (PARTITION BY CASE WHEN YearsAtCompany >= 10 THEN '10+ years' ELSE '<10 years' END),2) AS pct_in_group
FROM sheet1
GROUP BY tenure_group, BusinessTravel
ORDER BY tenure_group, BusinessTravel
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-031/attempt-01/sql/S15.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-031/attempt-01/sql/S15.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-031/attempt-01/results/S15.rows.jsonl)；完整：True；SHA256：`f21a2df64d670624743103693f69a04476df041b635bd22b9df0691a5b129d80`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "sheet1", "kind": "base", "block": null, "base_tables": ["sheet1"]}] | [] | ["CASE WHEN YearsAtCompany >= 10 THEN '10+ years' ELSE '<10 years' END", "BusinessTravel"] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |
| B1 | COUNT(*) | [] | [] | True |
| B1 | COUNT(*) | [] | [] | True |


## S16

类别 `data`；来源 `query_db`；调用 `038860741cac44d38ca69b0ff2830b72`；状态 `success`。

```sql
SELECT 
  CASE WHEN YearsAtCompany >= 10 THEN '10+ years' ELSE '<10 years' END AS tenure_group,
  JobSatisfaction,
  COUNT(*) AS cnt,
  ROUND(100.0*COUNT(*)/SUM(COUNT(*)) OVER (PARTITION BY CASE WHEN YearsAtCompany >= 10 THEN '10+ years' ELSE '<10 years' END),2) AS pct_in_group
FROM sheet1
GROUP BY tenure_group, JobSatisfaction
ORDER BY tenure_group, JobSatisfaction
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-031/attempt-01/sql/S16.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-031/attempt-01/sql/S16.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-031/attempt-01/results/S16.rows.jsonl)；完整：True；SHA256：`331d5f2eddbf944e8edd9e74f930dea6250e8656703855c700773d7aec32d6e5`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "sheet1", "kind": "base", "block": null, "base_tables": ["sheet1"]}] | [] | ["CASE WHEN YearsAtCompany >= 10 THEN '10+ years' ELSE '<10 years' END", "JobSatisfaction"] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |
| B1 | COUNT(*) | [] | [] | True |
| B1 | COUNT(*) | [] | [] | True |


## S17

类别 `data`；来源 `query_db`；调用 `4ba789dbc2ab4fbba5ff3338035e8238`；状态 `success`。

```sql
SELECT 
  CASE WHEN YearsAtCompany >= 10 THEN '10+ years' ELSE '<10 years' END AS tenure_group,
  WorkLifeBalance,
  COUNT(*) AS cnt,
  ROUND(100.0*COUNT(*)/SUM(COUNT(*)) OVER (PARTITION BY CASE WHEN YearsAtCompany >= 10 THEN '10+ years' ELSE '<10 years' END),2) AS pct_in_group
FROM sheet1
GROUP BY tenure_group, WorkLifeBalance
ORDER BY tenure_group, WorkLifeBalance
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-031/attempt-01/sql/S17.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-031/attempt-01/sql/S17.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-031/attempt-01/results/S17.rows.jsonl)；完整：True；SHA256：`cb01cf59cc59569215aea73a674f5b3209e1e7f664eaa6b941b681cd5608fbda`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "sheet1", "kind": "base", "block": null, "base_tables": ["sheet1"]}] | [] | ["CASE WHEN YearsAtCompany >= 10 THEN '10+ years' ELSE '<10 years' END", "WorkLifeBalance"] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |
| B1 | COUNT(*) | [] | [] | True |
| B1 | COUNT(*) | [] | [] | True |


## S18

类别 `data`；来源 `query_db`；调用 `81f72fe221e943adba8685af2a4c68cf`；状态 `success`。

```sql
SELECT 
  CASE WHEN YearsAtCompany >= 10 THEN '10+ years' ELSE '<10 years' END AS tenure_group,
  SalarySlab, COUNT(*) AS cnt,
  ROUND(100.0*COUNT(*)/SUM(COUNT(*)) OVER (PARTITION BY CASE WHEN YearsAtCompany >= 10 THEN '10+ years' ELSE '<10 years' END),2) AS pct_in_group
FROM sheet1
GROUP BY tenure_group, SalarySlab
ORDER BY tenure_group, cnt DESC
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-031/attempt-01/sql/S18.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-031/attempt-01/sql/S18.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-031/attempt-01/results/S18.rows.jsonl)；完整：True；SHA256：`cc806c3962002ef5d311eba769b47650d8f1f9a0b11e71691e89d8a9f29d14a4`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "sheet1", "kind": "base", "block": null, "base_tables": ["sheet1"]}] | [] | ["CASE WHEN YearsAtCompany >= 10 THEN '10+ years' ELSE '<10 years' END", "SalarySlab"] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |
| B1 | COUNT(*) | [] | [] | True |
| B1 | COUNT(*) | [] | [] | True |


## S19

类别 `data`；来源 `query_db`；调用 `0977c74003fe43f6a63a2c6cf6e2e0d1`；状态 `success`。

```sql
SELECT YearsAtCompany, COUNT(*) AS cnt,
       SUM(CASE WHEN Attrition='Yes' THEN 1 ELSE 0 END) AS leavers,
       ROUND(100.0*SUM(CASE WHEN Attrition='Yes' THEN 1 ELSE 0 END)/COUNT(*),2) AS attrition_rate_pct
FROM sheet1
GROUP BY YearsAtCompany
ORDER BY YearsAtCompany
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-031/attempt-01/sql/S19.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-031/attempt-01/sql/S19.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-031/attempt-01/results/S19.rows.jsonl)；完整：True；SHA256：`279a7cb8d2f87cfb1b1fc4a8d632b0e083323580517ab7e07b9ed42a192991b9`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "sheet1", "kind": "base", "block": null, "base_tables": ["sheet1"]}] | [] | ["YearsAtCompany"] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |
| B1 | SUM(CASE WHEN Attrition = 'Yes' THEN 1 ELSE 0 END) | [] | [{"table": "sheet1", "column": "Attrition"}] | False |
| B1 | COUNT(*) | [] | [] | True |
| B1 | SUM(CASE WHEN Attrition = 'Yes' THEN 1 ELSE 0 END) | [] | [{"table": "sheet1", "column": "Attrition"}] | False |


## S20

类别 `data`；来源 `query_db`；调用 `174469005fc543289afc74ddd5092772`；状态 `success`。

```sql
SELECT 
  CASE WHEN YearsAtCompany BETWEEN 6 AND 10 THEN '6-10 years band' ELSE 'other' END AS band,
  ROUND(AVG(CASE WHEN Attrition='Yes' THEN MonthlyIncome END),2) AS leaver_income,
  ROUND(AVG(CASE WHEN Attrition='No' THEN MonthlyIncome END),2) AS stayer_income,
  ROUND(AVG(CASE WHEN Attrition='Yes' THEN YearsSinceLastPromotion END),2) AS leaver_years_since_promo,
  ROUND(AVG(CASE WHEN Attrition='No' THEN YearsSinceLastPromotion END),2) AS stayer_years_since_promo,
  ROUND(AVG(CASE WHEN Attrition='Yes' THEN JobSatisfaction END),2) AS leaver_jobsat,
  ROUND(AVG(CASE WHEN Attrition='No' THEN JobSatisfaction END),2) AS stayer_jobsat
FROM sheet1
WHERE YearsAtCompany BETWEEN 6 AND 10
GROUP BY band
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-031/attempt-01/sql/S20.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-031/attempt-01/sql/S20.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-031/attempt-01/results/S20.rows.jsonl)；完整：True；SHA256：`d47be7f7f30f4eda56ea2082c3653f0548d73d294279688e590c7dc319fa505c`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "sheet1", "kind": "base", "block": null, "base_tables": ["sheet1"]}] | [] | ["CASE WHEN YearsAtCompany BETWEEN 6 AND 10 THEN '6-10 years band' ELSE 'other' END"] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | AVG(CASE WHEN Attrition = 'Yes' THEN MonthlyIncome END) | [{"table": "sheet1", "column": "MonthlyIncome"}] | [{"table": "sheet1", "column": "Attrition"}] | False |
| B1 | AVG(CASE WHEN Attrition = 'No' THEN MonthlyIncome END) | [{"table": "sheet1", "column": "MonthlyIncome"}] | [{"table": "sheet1", "column": "Attrition"}] | False |
| B1 | AVG(CASE WHEN Attrition = 'Yes' THEN YearsSinceLastPromotion END) | [{"table": "sheet1", "column": "YearsSinceLastPromotion"}] | [{"table": "sheet1", "column": "Attrition"}] | False |
| B1 | AVG(CASE WHEN Attrition = 'No' THEN YearsSinceLastPromotion END) | [{"table": "sheet1", "column": "YearsSinceLastPromotion"}] | [{"table": "sheet1", "column": "Attrition"}] | False |
| B1 | AVG(CASE WHEN Attrition = 'Yes' THEN JobSatisfaction END) | [{"table": "sheet1", "column": "JobSatisfaction"}] | [{"table": "sheet1", "column": "Attrition"}] | False |
| B1 | AVG(CASE WHEN Attrition = 'No' THEN JobSatisfaction END) | [{"table": "sheet1", "column": "JobSatisfaction"}] | [{"table": "sheet1", "column": "Attrition"}] | False |


## S21

类别 `data`；来源 `query_db`；调用 `dc06a5190043429fae021c180f58c337`；状态 `success`。

```sql
SELECT Attrition, COUNT(*) AS cnt,
  ROUND(AVG(MonthlyIncome),2) AS avg_income,
  ROUND(AVG(YearsSinceLastPromotion),2) AS avg_years_since_promo,
  ROUND(AVG(YearsAtCompany),2) AS avg_years_at_co,
  ROUND(AVG(JobSatisfaction),2) AS avg_jobsat,
  ROUND(AVG(EnvironmentSatisfaction),2) AS avg_envsat,
  ROUND(AVG(WorkLifeBalance),2) AS avg_wlb,
  ROUND(AVG(OverTime='Yes')*100,2) AS pct_overtime,
  ROUND(AVG(StockOptionLevel=0)*100,2) AS pct_no_stock,
  ROUND(AVG(TrainingTimesLastYear),2) AS avg_training
FROM sheet1
GROUP BY Attrition
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-031/attempt-01/sql/S21.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-031/attempt-01/sql/S21.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-031/attempt-01/results/S21.rows.jsonl)；完整：True；SHA256：`b191646fe6fef25c2e6c6bc460de1c2c20cb4feffc77ee41d1bc2ccf6bef26ce`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "sheet1", "kind": "base", "block": null, "base_tables": ["sheet1"]}] | [] | ["Attrition"] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |
| B1 | AVG(MonthlyIncome) | [{"table": "sheet1", "column": "MonthlyIncome"}] | [] | False |
| B1 | AVG(YearsSinceLastPromotion) | [{"table": "sheet1", "column": "YearsSinceLastPromotion"}] | [] | False |
| B1 | AVG(YearsAtCompany) | [{"table": "sheet1", "column": "YearsAtCompany"}] | [] | False |
| B1 | AVG(JobSatisfaction) | [{"table": "sheet1", "column": "JobSatisfaction"}] | [] | False |
| B1 | AVG(EnvironmentSatisfaction) | [{"table": "sheet1", "column": "EnvironmentSatisfaction"}] | [] | False |
| B1 | AVG(WorkLifeBalance) | [{"table": "sheet1", "column": "WorkLifeBalance"}] | [] | False |
| B1 | AVG(TrainingTimesLastYear) | [{"table": "sheet1", "column": "TrainingTimesLastYear"}] | [] | False |
| B1 | AVG(OverTime = 'Yes') | [{"table": "sheet1", "column": "OverTime"}] | [] | False |
| B1 | AVG(StockOptionLevel = 0) | [{"table": "sheet1", "column": "StockOptionLevel"}] | [] | False |


## S22

类别 `data`；来源 `query_db`；调用 `1964f7c8612941fd8dba6468cc0b97cf`；状态 `success`。

```sql
SELECT Attrition,
  ROUND(AVG(CASE WHEN YearsSinceLastPromotion BETWEEN 0 AND 1 THEN 1 ELSE 0 END)*100,2) AS pct_promo_0_1yr,
  ROUND(AVG(CASE WHEN YearsSinceLastPromotion BETWEEN 2 AND 3 THEN 1 ELSE 0 END)*100,2) AS pct_promo_2_3yr,
  ROUND(AVG(CASE WHEN YearsSinceLastPromotion >= 4 THEN 1 ELSE 0 END)*100,2) AS pct_promo_4plus_yr
FROM sheet1
GROUP BY Attrition
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-031/attempt-01/sql/S22.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-031/attempt-01/sql/S22.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-031/attempt-01/results/S22.rows.jsonl)；完整：True；SHA256：`018f699958d107856db74554d0521352b724d7f23232a9a3db77600686ae3e27`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "sheet1", "kind": "base", "block": null, "base_tables": ["sheet1"]}] | [] | ["Attrition"] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | AVG(CASE WHEN YearsSinceLastPromotion BETWEEN 0 AND 1 THEN 1 ELSE 0 END) | [] | [{"table": "sheet1", "column": "YearsSinceLastPromotion"}] | False |
| B1 | AVG(CASE WHEN YearsSinceLastPromotion BETWEEN 2 AND 3 THEN 1 ELSE 0 END) | [] | [{"table": "sheet1", "column": "YearsSinceLastPromotion"}] | False |
| B1 | AVG(CASE WHEN YearsSinceLastPromotion >= 4 THEN 1 ELSE 0 END) | [] | [{"table": "sheet1", "column": "YearsSinceLastPromotion"}] | False |


## S23

类别 `data`；来源 `query_db`；调用 `f341424b2b854ecab57fd290ced85308`；状态 `success`。

```sql
SELECT 
  CASE WHEN YearsAtCompany >= 10 THEN '10+ years' ELSE '<10 years' END AS tenure_group,
  ROUND(AVG(MonthlyIncome),0) AS avg_income,
  ROUND(AVG(JobLevel),2) AS avg_job_level,
  ROUND(AVG(StockOptionLevel),2) AS avg_stock_level,
  ROUND(AVG(CASE WHEN StockOptionLevel=0 THEN 1 ELSE 0 END)*100,2) AS pct_no_stock,
  ROUND(AVG(YearsSinceLastPromotion),2) AS avg_years_since_promo,
  ROUND(AVG(TotalWorkingYears),2) AS avg_total_work_years,
  ROUND(AVG(YearsInCurrentRole),2) AS avg_years_in_role
FROM sheet1
GROUP BY tenure_group
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-031/attempt-01/sql/S23.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-031/attempt-01/sql/S23.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-031/attempt-01/results/S23.rows.jsonl)；完整：True；SHA256：`987e933a586e0334e3f758fb245ab8d6bdf0e0fc1dabdf2ac3108da0ceb65bd3`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "sheet1", "kind": "base", "block": null, "base_tables": ["sheet1"]}] | [] | ["CASE WHEN YearsAtCompany >= 10 THEN '10+ years' ELSE '<10 years' END"] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | AVG(MonthlyIncome) | [{"table": "sheet1", "column": "MonthlyIncome"}] | [] | False |
| B1 | AVG(JobLevel) | [{"table": "sheet1", "column": "JobLevel"}] | [] | False |
| B1 | AVG(StockOptionLevel) | [{"table": "sheet1", "column": "StockOptionLevel"}] | [] | False |
| B1 | AVG(YearsSinceLastPromotion) | [{"table": "sheet1", "column": "YearsSinceLastPromotion"}] | [] | False |
| B1 | AVG(TotalWorkingYears) | [{"table": "sheet1", "column": "TotalWorkingYears"}] | [] | False |
| B1 | AVG(YearsInCurrentRole) | [{"table": "sheet1", "column": "YearsInCurrentRole"}] | [] | False |
| B1 | AVG(CASE WHEN StockOptionLevel = 0 THEN 1 ELSE 0 END) | [] | [{"table": "sheet1", "column": "StockOptionLevel"}] | False |


## S24

类别 `data`；来源 `query_db`；调用 `84386dd66d8f4f1099e8bdb09fabb11d`；状态 `success`。

```sql
SELECT YearsSinceLastPromotion, 
       COUNT(*) AS cnt,
       SUM(CASE WHEN Attrition='Yes' THEN 1 ELSE 0 END) AS leavers,
       ROUND(100.0*SUM(CASE WHEN Attrition='Yes' THEN 1 ELSE 0 END)/COUNT(*),2) AS attrition_rate_pct,
       ROUND(AVG(MonthlyIncome),0) AS avg_income
FROM sheet1
GROUP BY YearsSinceLastPromotion
HAVING cnt >= 20
ORDER BY YearsSinceLastPromotion
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-031/attempt-01/sql/S24.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-031/attempt-01/sql/S24.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-031/attempt-01/results/S24.rows.jsonl)；完整：True；SHA256：`a9c727a34e53b281eff6749ccf98cd32c244a317394f2516c6c628b149dbe2d0`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "sheet1", "kind": "base", "block": null, "base_tables": ["sheet1"]}] | [] | ["YearsSinceLastPromotion"] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |
| B1 | SUM(CASE WHEN Attrition = 'Yes' THEN 1 ELSE 0 END) | [] | [{"table": "sheet1", "column": "Attrition"}] | False |
| B1 | AVG(MonthlyIncome) | [{"table": "sheet1", "column": "MonthlyIncome"}] | [] | False |
| B1 | COUNT(*) | [] | [] | True |
| B1 | SUM(CASE WHEN Attrition = 'Yes' THEN 1 ELSE 0 END) | [] | [{"table": "sheet1", "column": "Attrition"}] | False |


## S25

类别 `data`；来源 `query_db`；调用 `0e30b52063614ab5b90e8af3416bdd0a`；状态 `success`。

```sql
SELECT 
  CASE 
    WHEN YearsAtCompany BETWEEN 0 AND 5 THEN '0-5 years'
    WHEN YearsAtCompany BETWEEN 6 AND 10 THEN '6-10 years'
    WHEN YearsAtCompany BETWEEN 11 AND 15 THEN '11-15 years'
    WHEN YearsAtCompany BETWEEN 16 AND 20 THEN '16-20 years'
    ELSE '20+ years'
  END AS tenure_band,
  ROUND(AVG(MonthlyIncome),0) AS avg_income,
  ROUND(AVG(JobLevel),2) AS avg_job_level,
  ROUND(AVG(YearsSinceLastPromotion),2) AS avg_years_since_promo,
  ROUND(AVG(YearsInCurrentRole),2) AS avg_years_in_role,
  ROUND(AVG(YearsWithCurrManager),2) AS avg_years_with_mgr,
  ROUND(AVG(StockOptionLevel),2) AS avg_stock,
  ROUND(AVG(JobSatisfaction),2) AS avg_jobsat
FROM sheet1
GROUP BY tenure_band
ORDER BY MIN(YearsAtCompany)
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-031/attempt-01/sql/S25.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-031/attempt-01/sql/S25.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-031/attempt-01/results/S25.rows.jsonl)；完整：True；SHA256：`1edab1295d2f910c16fe08f8b5b91530153eca5c361c75545fc93f03eb972042`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "sheet1", "kind": "base", "block": null, "base_tables": ["sheet1"]}] | [] | ["CASE WHEN YearsAtCompany BETWEEN 0 AND 5 THEN '0-5 years' WHEN YearsAtCompany BETWEEN 6 AND 10 THEN '6-10 years' WHEN YearsAtCompany BETWEEN 11 AND 15 THEN '11-15 years' WHEN YearsAtCompany BETWEEN 16 AND 20 THEN '16-20 years' ELSE '20+ years' END"] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | AVG(MonthlyIncome) | [{"table": "sheet1", "column": "MonthlyIncome"}] | [] | False |
| B1 | AVG(JobLevel) | [{"table": "sheet1", "column": "JobLevel"}] | [] | False |
| B1 | AVG(YearsSinceLastPromotion) | [{"table": "sheet1", "column": "YearsSinceLastPromotion"}] | [] | False |
| B1 | AVG(YearsInCurrentRole) | [{"table": "sheet1", "column": "YearsInCurrentRole"}] | [] | False |
| B1 | AVG(YearsWithCurrManager) | [{"table": "sheet1", "column": "YearsWithCurrManager"}] | [] | False |
| B1 | AVG(StockOptionLevel) | [{"table": "sheet1", "column": "StockOptionLevel"}] | [] | False |
| B1 | AVG(JobSatisfaction) | [{"table": "sheet1", "column": "JobSatisfaction"}] | [] | False |
| B1 | MIN(YearsAtCompany) | [{"table": "sheet1", "column": "YearsAtCompany"}] | [] | False |


## S26

类别 `data`；来源 `query_db`；调用 `47cf910a04cc4c83812dd9fc6f2e5a02`；状态 `success`。

```sql
SELECT 
  CASE WHEN YearsAtCompany BETWEEN 6 AND 10 THEN '6-10 band' ELSE 'other' END AS band,
  OverTime, Attrition, COUNT(*) AS cnt,
  ROUND(100.0*COUNT(*)/SUM(COUNT(*)) OVER (PARTITION BY CASE WHEN YearsAtCompany BETWEEN 6 AND 10 THEN '6-10 band' ELSE 'other' END),2) AS pct
FROM sheet1
WHERE YearsAtCompany BETWEEN 6 AND 10
GROUP BY band, OverTime, Attrition
ORDER BY OverTime, Attrition
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-031/attempt-01/sql/S26.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-031/attempt-01/sql/S26.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-031/attempt-01/results/S26.rows.jsonl)；完整：True；SHA256：`356f15e185c6b06bc1f775f7101f9d73b35e2511225e3df1fbe13544c5e80cd2`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "sheet1", "kind": "base", "block": null, "base_tables": ["sheet1"]}] | [] | ["CASE WHEN YearsAtCompany BETWEEN 6 AND 10 THEN '6-10 band' ELSE 'other' END", "OverTime", "Attrition"] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |
| B1 | COUNT(*) | [] | [] | True |
| B1 | COUNT(*) | [] | [] | True |


## S27

类别 `data`；来源 `query_db`；调用 `12e75bc02f8b4a50a69c03ae7f3ef30a`；状态 `success`。

```sql
SELECT 
  CASE WHEN YearsAtCompany BETWEEN 6 AND 10 THEN '6-10 band' ELSE 'other' END AS band,
  Attrition, 
  COUNT(*) AS cnt,
  ROUND(AVG(MonthlyIncome),0) AS avg_income,
  ROUND(AVG(YearsSinceLastPromotion),2) AS avg_years_since_promo,
  ROUND(AVG(JobSatisfaction),2) AS avg_jobsat,
  ROUND(AVG(EnvironmentSatisfaction),2) AS avg_envsat,
  ROUND(AVG(WorkLifeBalance),2) AS avg_wlb,
  ROUND(AVG(DistanceFromHome),2) AS avg_distance,
  ROUND(AVG(NumCompaniesWorked),2) AS avg_num_companies
FROM sheet1
WHERE YearsAtCompany BETWEEN 6 AND 10
GROUP BY Attrition
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-031/attempt-01/sql/S27.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-031/attempt-01/sql/S27.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-031/attempt-01/results/S27.rows.jsonl)；完整：True；SHA256：`cc672c7e57183fde2b2aa712b95f74959885a246e27c554d7d31587b9fa429c4`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "sheet1", "kind": "base", "block": null, "base_tables": ["sheet1"]}] | [] | ["Attrition"] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |
| B1 | AVG(MonthlyIncome) | [{"table": "sheet1", "column": "MonthlyIncome"}] | [] | False |
| B1 | AVG(YearsSinceLastPromotion) | [{"table": "sheet1", "column": "YearsSinceLastPromotion"}] | [] | False |
| B1 | AVG(JobSatisfaction) | [{"table": "sheet1", "column": "JobSatisfaction"}] | [] | False |
| B1 | AVG(EnvironmentSatisfaction) | [{"table": "sheet1", "column": "EnvironmentSatisfaction"}] | [] | False |
| B1 | AVG(WorkLifeBalance) | [{"table": "sheet1", "column": "WorkLifeBalance"}] | [] | False |
| B1 | AVG(DistanceFromHome) | [{"table": "sheet1", "column": "DistanceFromHome"}] | [] | False |
| B1 | AVG(NumCompaniesWorked) | [{"table": "sheet1", "column": "NumCompaniesWorked"}] | [] | False |


## S28

类别 `data`；来源 `query_db`；调用 `68106455b11f4ec1a152624e726afadc`；状态 `success`。

```sql
SELECT 
  Attrition,
  ROUND(100.0*SUM(CASE WHEN OverTime='Yes' THEN 1 ELSE 0 END)/COUNT(*),2) AS pct_overtime,
  ROUND(100.0*SUM(CASE WHEN StockOptionLevel=0 THEN 1 ELSE 0 END)/COUNT(*),2) AS pct_no_stock,
  ROUND(AVG(MonthlyIncome),0) AS avg_income,
  ROUND(AVG(JobSatisfaction),2) AS avg_jobsat,
  ROUND(AVG(YearsSinceLastPromotion),2) AS avg_years_since_promo
FROM sheet1
WHERE YearsAtCompany >= 10
GROUP BY Attrition
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-031/attempt-01/sql/S28.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-031/attempt-01/sql/S28.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-031/attempt-01/results/S28.rows.jsonl)；完整：True；SHA256：`8f0483b16916a0be6242498bfc29678670232981bf3fb185000cf353b295f4a8`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "sheet1", "kind": "base", "block": null, "base_tables": ["sheet1"]}] | [] | ["Attrition"] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | AVG(MonthlyIncome) | [{"table": "sheet1", "column": "MonthlyIncome"}] | [] | False |
| B1 | AVG(JobSatisfaction) | [{"table": "sheet1", "column": "JobSatisfaction"}] | [] | False |
| B1 | AVG(YearsSinceLastPromotion) | [{"table": "sheet1", "column": "YearsSinceLastPromotion"}] | [] | False |
| B1 | COUNT(*) | [] | [] | True |
| B1 | COUNT(*) | [] | [] | True |
| B1 | SUM(CASE WHEN OverTime = 'Yes' THEN 1 ELSE 0 END) | [] | [{"table": "sheet1", "column": "OverTime"}] | False |
| B1 | SUM(CASE WHEN StockOptionLevel = 0 THEN 1 ELSE 0 END) | [] | [{"table": "sheet1", "column": "StockOptionLevel"}] | False |


## S29

类别 `data`；来源 `query_db`；调用 `981d9627586149faab81d1cb09a0b87d`；状态 `success`。

```sql
SELECT JobRole,
  COUNT(*) AS cnt,
  ROUND(100.0*SUM(CASE WHEN Attrition='Yes' THEN 1 ELSE 0 END)/COUNT(*),2) AS attrition_rate_pct,
  ROUND(AVG(MonthlyIncome),0) AS avg_income,
  ROUND(AVG(YearsSinceLastPromotion),2) AS avg_years_since_promo,
  ROUND(AVG(JobSatisfaction),2) AS avg_jobsat,
  ROUND(AVG(YearsAtCompany),2) AS avg_tenure
FROM sheet1
GROUP BY JobRole
ORDER BY attrition_rate_pct DESC
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-031/attempt-01/sql/S29.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-031/attempt-01/sql/S29.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-031/attempt-01/results/S29.rows.jsonl)；完整：True；SHA256：`367b5954a81109e66319f599237222b4d200d15184476c252e756bee9d643f93`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "sheet1", "kind": "base", "block": null, "base_tables": ["sheet1"]}] | [] | ["JobRole"] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |
| B1 | AVG(MonthlyIncome) | [{"table": "sheet1", "column": "MonthlyIncome"}] | [] | False |
| B1 | AVG(YearsSinceLastPromotion) | [{"table": "sheet1", "column": "YearsSinceLastPromotion"}] | [] | False |
| B1 | AVG(JobSatisfaction) | [{"table": "sheet1", "column": "JobSatisfaction"}] | [] | False |
| B1 | AVG(YearsAtCompany) | [{"table": "sheet1", "column": "YearsAtCompany"}] | [] | False |
| B1 | COUNT(*) | [] | [] | True |
| B1 | SUM(CASE WHEN Attrition = 'Yes' THEN 1 ELSE 0 END) | [] | [{"table": "sheet1", "column": "Attrition"}] | False |


## S30

类别 `data`；来源 `query_db`；调用 `ef18db8c3ec04263912a242f4ba4aff6`；状态 `success`。

```sql
SELECT EducationField,
  COUNT(*) AS cnt,
  ROUND(100.0*SUM(CASE WHEN Attrition='Yes' THEN 1 ELSE 0 END)/COUNT(*),2) AS attrition_rate_pct,
  ROUND(AVG(YearsAtCompany),2) AS avg_tenure
FROM sheet1
GROUP BY EducationField
ORDER BY attrition_rate_pct DESC
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-031/attempt-01/sql/S30.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-031/attempt-01/sql/S30.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-031/attempt-01/results/S30.rows.jsonl)；完整：True；SHA256：`aa378a4e7b5102b54f4d5fad14ca79e3444c0063f54722393fc07062a1be666b`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "sheet1", "kind": "base", "block": null, "base_tables": ["sheet1"]}] | [] | ["EducationField"] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |
| B1 | AVG(YearsAtCompany) | [{"table": "sheet1", "column": "YearsAtCompany"}] | [] | False |
| B1 | COUNT(*) | [] | [] | True |
| B1 | SUM(CASE WHEN Attrition = 'Yes' THEN 1 ELSE 0 END) | [] | [{"table": "sheet1", "column": "Attrition"}] | False |


## S31

类别 `data`；来源 `python`；调用 `d66be0847faf4ba4bf8c7bc90fdef993`；状态 `success`。

```sql

SELECT YearsAtCompany, Age, MonthlyIncome, PercentSalaryHike, JobSatisfaction,
       EnvironmentSatisfaction, WorkLifeBalance, JobInvolvement, RelationshipSatisfaction,
       PerformanceRating, StockOptionLevel, TrainingTimesLastYear, DistanceFromHome,
       NumCompaniesWorked, YearsSinceLastPromotion, YearsInCurrentRole, YearsWithCurrManager,
       JobLevel, TotalWorkingYears, DailyRate, HourlyRate, MonthlyRate
FROM sheet1

```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-031/attempt-01/sql/S31.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-031/attempt-01/sql/S31.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-031/attempt-01/results/S31.rows.jsonl)；完整：True；SHA256：`ffd1a613b8f6074a690afcea7510e1552af348bfac9570bd18a43b6546f85027`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "sheet1", "kind": "base", "block": null, "base_tables": ["sheet1"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |


## S32

类别 `data`；来源 `python`；调用 `d66be0847faf4ba4bf8c7bc90fdef993`；状态 `success`。

```sql

SELECT YearsAtCompany, Attrition, MonthlyIncome, OverTime, StockOptionLevel,
       JobSatisfaction, YearsSinceLastPromotion, SalarySlab
FROM sheet1

```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-031/attempt-01/sql/S32.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-031/attempt-01/sql/S32.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-031/attempt-01/results/S32.rows.jsonl)；完整：True；SHA256：`1a686910db330ca68a569d16c95f6c0581bcf8d742f5b03948a8ee8065be1de1`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "sheet1", "kind": "base", "block": null, "base_tables": ["sheet1"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |


## S33

类别 `data`；来源 `python`；调用 `546fabe2e0e54e92885cda243d99ec3f`；状态 `success`。

```sql

SELECT CASE 
         WHEN YearsAtCompany BETWEEN 0 AND 5 THEN '0-5 years'
         WHEN YearsAtCompany BETWEEN 6 AND 10 THEN '6-10 years'
         WHEN YearsAtCompany BETWEEN 11 AND 15 THEN '11-15 years'
         WHEN YearsAtCompany BETWEEN 16 AND 20 THEN '16-20 years'
         WHEN YearsAtCompany > 20 THEN '20+ years'
       END AS tenure_band,
       COUNT(*) AS total,
       SUM(CASE WHEN Attrition='Yes' THEN 1 ELSE 0 END) AS leavers,
       ROUND(100.0*SUM(CASE WHEN Attrition='Yes' THEN 1 ELSE 0 END)/COUNT(*),2) AS attrition_rate
FROM sheet1
GROUP BY tenure_band
ORDER BY MIN(YearsAtCompany)

```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-031/attempt-01/sql/S33.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-031/attempt-01/sql/S33.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-031/attempt-01/results/S33.rows.jsonl)；完整：True；SHA256：`7b58db046fa43636758e9100df2a34b67b3a0be03d54b5bff16fe3da25efe97a`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "sheet1", "kind": "base", "block": null, "base_tables": ["sheet1"]}] | [] | ["CASE WHEN YearsAtCompany BETWEEN 0 AND 5 THEN '0-5 years' WHEN YearsAtCompany BETWEEN 6 AND 10 THEN '6-10 years' WHEN YearsAtCompany BETWEEN 11 AND 15 THEN '11-15 years' WHEN YearsAtCompany BETWEEN 16 AND 20 THEN '16-20 years' WHEN YearsAtCompany > 20 THEN '20+ years' END"] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |
| B1 | SUM(CASE WHEN Attrition = 'Yes' THEN 1 ELSE 0 END) | [] | [{"table": "sheet1", "column": "Attrition"}] | False |
| B1 | MIN(YearsAtCompany) | [{"table": "sheet1", "column": "YearsAtCompany"}] | [] | False |
| B1 | COUNT(*) | [] | [] | True |
| B1 | SUM(CASE WHEN Attrition = 'Yes' THEN 1 ELSE 0 END) | [] | [{"table": "sheet1", "column": "Attrition"}] | False |


## S34

类别 `data`；来源 `python`；调用 `546fabe2e0e54e92885cda243d99ec3f`；状态 `success`。

```sql

SELECT CASE WHEN YearsAtCompany >= 10 THEN '10+ Years' ELSE '<10 Years' END AS group_name,
       ROUND(AVG(MonthlyIncome),0) AS avg_income,
       ROUND(AVG(YearsSinceLastPromotion),2) AS avg_years_since_promo,
       ROUND(AVG(JobLevel),2) AS avg_job_level,
       ROUND(AVG(StockOptionLevel),2) AS avg_stock,
       ROUND(AVG(JobSatisfaction),2) AS avg_jobsat,
       ROUND(AVG(WorkLifeBalance),2) AS avg_wlb,
       ROUND(100.0*SUM(CASE WHEN OverTime='Yes' THEN 1 ELSE 0 END)/COUNT(*),2) AS pct_overtime,
       ROUND(100.0*SUM(CASE WHEN StockOptionLevel=0 THEN 1 ELSE 0 END)/COUNT(*),2) AS pct_no_stock,
       COUNT(*) AS cnt
FROM sheet1
GROUP BY group_name
ORDER BY group_name DESC

```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-031/attempt-01/sql/S34.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-031/attempt-01/sql/S34.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-031/attempt-01/results/S34.rows.jsonl)；完整：True；SHA256：`94ef532e07d4ef240ffe54d17e7df502c9f7f78b8ee49a53854d806919b07116`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "sheet1", "kind": "base", "block": null, "base_tables": ["sheet1"]}] | [] | ["CASE WHEN YearsAtCompany >= 10 THEN '10+ Years' ELSE '<10 Years' END"] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |
| B1 | AVG(MonthlyIncome) | [{"table": "sheet1", "column": "MonthlyIncome"}] | [] | False |
| B1 | AVG(YearsSinceLastPromotion) | [{"table": "sheet1", "column": "YearsSinceLastPromotion"}] | [] | False |
| B1 | AVG(JobLevel) | [{"table": "sheet1", "column": "JobLevel"}] | [] | False |
| B1 | AVG(StockOptionLevel) | [{"table": "sheet1", "column": "StockOptionLevel"}] | [] | False |
| B1 | AVG(JobSatisfaction) | [{"table": "sheet1", "column": "JobSatisfaction"}] | [] | False |
| B1 | AVG(WorkLifeBalance) | [{"table": "sheet1", "column": "WorkLifeBalance"}] | [] | False |
| B1 | COUNT(*) | [] | [] | True |
| B1 | COUNT(*) | [] | [] | True |
| B1 | SUM(CASE WHEN OverTime = 'Yes' THEN 1 ELSE 0 END) | [] | [{"table": "sheet1", "column": "OverTime"}] | False |
| B1 | SUM(CASE WHEN StockOptionLevel = 0 THEN 1 ELSE 0 END) | [] | [{"table": "sheet1", "column": "StockOptionLevel"}] | False |


## S35

类别 `data`；来源 `python`；调用 `546fabe2e0e54e92885cda243d99ec3f`；状态 `success`。

```sql

SELECT CASE 
         WHEN YearsAtCompany BETWEEN 0 AND 5 THEN '0-5 years'
         WHEN YearsAtCompany BETWEEN 6 AND 10 THEN '6-10 years'
         WHEN YearsAtCompany BETWEEN 11 AND 15 THEN '11-15 years'
         WHEN YearsAtCompany BETWEEN 16 AND 20 THEN '16-20 years'
         ELSE '20+ years'
       END AS tenure_band,
       ROUND(AVG(MonthlyIncome),0) AS avg_income,
       ROUND(AVG(JobLevel),2) AS avg_job_level,
       ROUND(AVG(YearsSinceLastPromotion),2) AS avg_years_since_promo,
       ROUND(AVG(YearsInCurrentRole),2) AS avg_years_in_role
FROM sheet1
GROUP BY tenure_band
ORDER BY MIN(YearsAtCompany)

```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-031/attempt-01/sql/S35.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-031/attempt-01/sql/S35.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-031/attempt-01/results/S35.rows.jsonl)；完整：True；SHA256：`ef3fb456826a276fbb0709caf6af81a7bd192ffd36136e62e90fa3eff4ffd9b1`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "sheet1", "kind": "base", "block": null, "base_tables": ["sheet1"]}] | [] | ["CASE WHEN YearsAtCompany BETWEEN 0 AND 5 THEN '0-5 years' WHEN YearsAtCompany BETWEEN 6 AND 10 THEN '6-10 years' WHEN YearsAtCompany BETWEEN 11 AND 15 THEN '11-15 years' WHEN YearsAtCompany BETWEEN 16 AND 20 THEN '16-20 years' ELSE '20+ years' END"] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | AVG(MonthlyIncome) | [{"table": "sheet1", "column": "MonthlyIncome"}] | [] | False |
| B1 | AVG(JobLevel) | [{"table": "sheet1", "column": "JobLevel"}] | [] | False |
| B1 | AVG(YearsSinceLastPromotion) | [{"table": "sheet1", "column": "YearsSinceLastPromotion"}] | [] | False |
| B1 | AVG(YearsInCurrentRole) | [{"table": "sheet1", "column": "YearsInCurrentRole"}] | [] | False |
| B1 | MIN(YearsAtCompany) | [{"table": "sheet1", "column": "YearsAtCompany"}] | [] | False |


## S36

类别 `data`；来源 `python`；调用 `546fabe2e0e54e92885cda243d99ec3f`；状态 `success`。

```sql

SELECT OverTime, StockOptionLevel, 
       COUNT(*) AS cnt,
       ROUND(100.0*SUM(CASE WHEN Attrition='Yes' THEN 1 ELSE 0 END)/COUNT(*),1) AS attrition_rate
FROM sheet1
GROUP BY OverTime, StockOptionLevel
ORDER BY OverTime, StockOptionLevel

```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-031/attempt-01/sql/S36.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-031/attempt-01/sql/S36.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-031/attempt-01/results/S36.rows.jsonl)；完整：True；SHA256：`ef1ca10020eb45e12004bd9a334b10bb510cce165292e56909c78df090c75fe9`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "sheet1", "kind": "base", "block": null, "base_tables": ["sheet1"]}] | [] | ["OverTime", "StockOptionLevel"] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |
| B1 | COUNT(*) | [] | [] | True |
| B1 | SUM(CASE WHEN Attrition = 'Yes' THEN 1 ELSE 0 END) | [] | [{"table": "sheet1", "column": "Attrition"}] | False |


## S37

类别 `data`；来源 `query_db`；调用 `8683cdfcea1545888a1b777be4a2a144`；状态 `success`。

```sql
SELECT JobRole,
  COUNT(*) AS cnt,
  ROUND(100.0*SUM(CASE WHEN Attrition='Yes' THEN 1 ELSE 0 END)/COUNT(*),1) AS attrition_rate,
  ROUND(AVG(MonthlyIncome),0) AS avg_income,
  ROUND(AVG(YearsAtCompany),1) AS avg_tenure
FROM sheet1
WHERE YearsAtCompany BETWEEN 6 AND 10
GROUP BY JobRole
ORDER BY attrition_rate DESC
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-031/attempt-01/sql/S37.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-031/attempt-01/sql/S37.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-031/attempt-01/results/S37.rows.jsonl)；完整：True；SHA256：`b686ab4648d82b6bbcf40f5eb1383a88965c1bc365085b71f6e6db791500e0e8`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "sheet1", "kind": "base", "block": null, "base_tables": ["sheet1"]}] | [] | ["JobRole"] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |
| B1 | AVG(MonthlyIncome) | [{"table": "sheet1", "column": "MonthlyIncome"}] | [] | False |
| B1 | AVG(YearsAtCompany) | [{"table": "sheet1", "column": "YearsAtCompany"}] | [] | False |
| B1 | COUNT(*) | [] | [] | True |
| B1 | SUM(CASE WHEN Attrition = 'Yes' THEN 1 ELSE 0 END) | [] | [{"table": "sheet1", "column": "Attrition"}] | False |


## S38

类别 `data`；来源 `query_db`；调用 `e21b6dc2ffea474ab77e626553cc3be4`；状态 `success`。

```sql
SELECT
  CASE WHEN YearsAtCompany >= 10 AND Attrition='No' THEN '10+ Stayer'
       WHEN YearsAtCompany >= 10 AND Attrition='Yes' THEN '10+ Leaver'
       WHEN YearsAtCompany < 10 AND Attrition='No' THEN '<10 Stayer'
       ELSE '<10 Leaver' END AS segment,
  COUNT(*) AS cnt,
  ROUND(AVG(MonthlyIncome),0) AS avg_income,
  ROUND(AVG(JobSatisfaction),2) AS avg_jobsat,
  ROUND(AVG(EnvironmentSatisfaction),2) AS avg_envsat,
  ROUND(100.0*AVG(CASE WHEN OverTime='Yes' THEN 1 ELSE 0 END),1) AS pct_overtime
FROM sheet1
GROUP BY segment
ORDER BY segment
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-031/attempt-01/sql/S38.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-031/attempt-01/sql/S38.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-031/attempt-01/results/S38.rows.jsonl)；完整：True；SHA256：`3adcaa71d181fc4981151f14aeff8122b447fd2ee0d5be8a070790b0a1bc0dfa`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "sheet1", "kind": "base", "block": null, "base_tables": ["sheet1"]}] | [] | ["CASE WHEN YearsAtCompany >= 10 AND Attrition = 'No' THEN '10+ Stayer' WHEN YearsAtCompany >= 10 AND Attrition = 'Yes' THEN '10+ Leaver' WHEN YearsAtCompany < 10 AND Attrition = 'No' THEN '<10 Stayer' ELSE '<10 Leaver' END"] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |
| B1 | AVG(MonthlyIncome) | [{"table": "sheet1", "column": "MonthlyIncome"}] | [] | False |
| B1 | AVG(JobSatisfaction) | [{"table": "sheet1", "column": "JobSatisfaction"}] | [] | False |
| B1 | AVG(EnvironmentSatisfaction) | [{"table": "sheet1", "column": "EnvironmentSatisfaction"}] | [] | False |
| B1 | AVG(CASE WHEN OverTime = 'Yes' THEN 1 ELSE 0 END) | [] | [{"table": "sheet1", "column": "OverTime"}] | False |


## S39

类别 `data`；来源 `query_db`；调用 `a5687a7d3b814735a37fa88db434e74d`；状态 `success`。

```sql
SELECT 
  CASE WHEN YearsAtCompany BETWEEN 6 AND 10 THEN '6-10 band' ELSE 'other' END AS band,
  Attrition,
  ROUND(AVG(MonthlyIncome),0) AS avg_income,
  ROUND(AVG(PercentSalaryHike),2) AS avg_hike,
  ROUND(AVG(JobSatisfaction),2) AS avg_jobsat,
  ROUND(AVG(TrainingTimesLastYear),2) AS avg_training,
  ROUND(100.0*AVG(CASE WHEN OverTime='Yes' THEN 1 ELSE 0 END),1) AS pct_ot,
  ROUND(100.0*AVG(CASE WHEN StockOptionLevel=0 THEN 1 ELSE 0 END),1) AS pct_no_stock
FROM sheet1
WHERE YearsAtCompany BETWEEN 6 AND 10
GROUP BY Attrition
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-031/attempt-01/sql/S39.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-031/attempt-01/sql/S39.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-031/attempt-01/results/S39.rows.jsonl)；完整：True；SHA256：`2679f3d383e34a7c5fca1e754125ec47dbecf814ec28ac5aa9256ef773e952dc`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "sheet1", "kind": "base", "block": null, "base_tables": ["sheet1"]}] | [] | ["Attrition"] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | AVG(MonthlyIncome) | [{"table": "sheet1", "column": "MonthlyIncome"}] | [] | False |
| B1 | AVG(PercentSalaryHike) | [{"table": "sheet1", "column": "PercentSalaryHike"}] | [] | False |
| B1 | AVG(JobSatisfaction) | [{"table": "sheet1", "column": "JobSatisfaction"}] | [] | False |
| B1 | AVG(TrainingTimesLastYear) | [{"table": "sheet1", "column": "TrainingTimesLastYear"}] | [] | False |
| B1 | AVG(CASE WHEN OverTime = 'Yes' THEN 1 ELSE 0 END) | [] | [{"table": "sheet1", "column": "OverTime"}] | False |
| B1 | AVG(CASE WHEN StockOptionLevel = 0 THEN 1 ELSE 0 END) | [] | [{"table": "sheet1", "column": "StockOptionLevel"}] | False |


## S40

类别 `data`；来源 `query_db`；调用 `9b15aaaf5fd74ebaae8081d0888a6fb6`；状态 `success`。

```sql
SELECT 
  CASE WHEN YearsAtCompany BETWEEN 6 AND 10 THEN '6-10 band' ELSE 'other' END AS band,
  Attrition,
  ROUND(AVG(YearsSinceLastPromotion),2) AS avg_years_since_promo,
  ROUND(AVG(YearsInCurrentRole),2) AS avg_years_in_role,
  ROUND(AVG(NumCompaniesWorked),2) AS avg_num_companies
FROM sheet1
WHERE YearsAtCompany BETWEEN 6 AND 10
GROUP BY Attrition
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-031/attempt-01/sql/S40.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-031/attempt-01/sql/S40.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-031/attempt-01/results/S40.rows.jsonl)；完整：True；SHA256：`8f5db86294302ea417a0296a9a43b4284ae37fe5cfcb355649cc5f71d1bda6c0`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "sheet1", "kind": "base", "block": null, "base_tables": ["sheet1"]}] | [] | ["Attrition"] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | AVG(YearsSinceLastPromotion) | [{"table": "sheet1", "column": "YearsSinceLastPromotion"}] | [] | False |
| B1 | AVG(YearsInCurrentRole) | [{"table": "sheet1", "column": "YearsInCurrentRole"}] | [] | False |
| B1 | AVG(NumCompaniesWorked) | [{"table": "sheet1", "column": "NumCompaniesWorked"}] | [] | False |

