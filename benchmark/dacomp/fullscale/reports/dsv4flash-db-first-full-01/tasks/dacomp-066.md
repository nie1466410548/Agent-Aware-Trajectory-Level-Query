# dacomp-066

The application screening to first interview conversion rate for the company's Engineering…

运行：已提交。官方未评分。全部 SQL 尝试/成功 44/44；数据 SQL 42/42；Python 7 次。

完整原题：

The application screening to first interview conversion rate for the company's Engineering department has dropped from 35% to 22% over the past 6 months, significantly lower than the Marketing department's 45% conversion rate. Please use the `greenhouse__recruitment_performance` table to analyze which specific roles within the Engineering department (e.g., Frontend, Backend, Data Engineer) have experienced the most severe decline in conversion rate. Then, using the `greenhouse__job_enhanced` table's data on hiring managers and interviewers, identify if there are specific hiring managers whose assigned jobs have systematically lower conversion rates. Finally, quantify the impact of factors such as the number of interviewers and the hiring manager's years of experience on the conversion rate.

| 表 | 行数 | 列数 |
| --- | --- | --- |
| greenhouse__job_enhanced | 191 | 27 |
| greenhouse__recruitment_performance | 191 | 23 |


实际路线（分析者依据 SQL/源码概括，不代表 Agent 自述）：SQL 连接岗位与招聘绩效并比较转化率 → Python 回归、相关检验及经理均值排序 → 工程岗位转化诊断。

数据库大小：81,920 字节。

## 数据 SQL

| SQL | 状态 | 基础表 | Join 输入/类型 | GROUP BY | 聚合表达式 | 结果行数 | 数据库 ms |
| --- | --- | --- | --- | --- | --- | --- | --- |
| [S3/Q1](#s3) | success | ["greenhouse__recruitment_performance"] | 0 / {} | [] | [] | 20 | 0.457 |
| [S4/Q2](#s4) | success | ["greenhouse__recruitment_performance"] | 0 / {} | [] | [] | 66 | 0.425 |
| [S5/Q3](#s5) | success | ["greenhouse__job_enhanced"] | 0 / {} | [] | [] | 2 | 0.374 |
| [S6/Q4](#s6) | success | ["greenhouse__job_enhanced"] | 0 / {} | [] | [] | 30 | 0.45 |
| [S7/Q5](#s7) | success | ["greenhouse__job_enhanced"] | 0 / {} | [] | [] | 27 | 0.423 |
| [S8/Q6](#s8) | success | ["greenhouse__recruitment_performance"] | 0 / {} | [] | [] | 2 | 0.335 |
| [S9/Q7](#s9) | success | ["greenhouse__recruitment_performance"] | 0 / {} | [] | ["COUNT(*)"] | 1 | 0.312 |
| [S10/Q8](#s10) | success | ["greenhouse__job_enhanced"] | 0 / {} | [] | ["COUNT(*)", "COUNT(DISTINCT job_id)"] | 1 | 0.326 |
| [S11/Q9](#s11) | success | ["greenhouse__job_enhanced", "greenhouse__recruitment_performance"] | 2 / {'INNER': 1} | ["r.application_quarter", "j.departments"] | ["SUM(r.total_applications)", "SUM(r.total_interviews)", "SUM(r.total_applications)", "SUM(r.total_applications)", "SUM(r.total_interviews)", "SUM(r.hired_count)"] | 4 | 0.671 |
| [S12/Q10](#s12) | success | ["greenhouse__job_enhanced"] | 0 / {} | [] | [] | 46 | 0.473 |
| [S13/Q11](#s13) | success | ["greenhouse__job_enhanced"] | 0 / {} | [] | [] | 20 | 0.394 |
| [S14/Q12](#s14) | success | ["greenhouse__job_enhanced"] | 0 / {} | [] | [] | 8 | 0.393 |
| [S15/Q13](#s15) | success | ["greenhouse__job_enhanced"] | 0 / {} | [] | [] | 154 | 0.66 |
| [S16/Q14](#s16) | success | ["greenhouse__job_enhanced"] | 0 / {} | [] | [] | 16 | 0.5 |
| [S17/Q15](#s17) | success | ["greenhouse__job_enhanced"] | 0 / {} | [] | [] | 2 | 0.409 |
| [S18/Q16](#s18) | success | ["greenhouse__job_enhanced"] | 0 / {} | [] | [] | 10 | 0.378 |
| [S19/Q17](#s19) | success | ["greenhouse__job_enhanced", "greenhouse__recruitment_performance"] | 2 / {'INNER': 1} | ["CASE WHEN r.job_title LIKE 'Frontend%' THEN 'Frontend Engineer' WHEN r.job_title LIKE 'Backend%' THEN 'Backend Engineer' WHEN r.job_title LIKE 'Full Stack%' THEN 'Full Stack Engineer' WHEN r.job_title LIKE 'Data Engineer%' THEN 'Data Engineer' ELSE r.job_title END", "r.application_year", "r.application_quarter"] | ["SUM(r.total_applications)", "SUM(r.total_interviews)", "SUM(r.hired_count)", "SUM(r.total_applications)", "SUM(r.total_interviews)"] | 46 | 0.961 |
| [S20/Q18](#s20) | success | ["greenhouse__job_enhanced"] | 0 / {} | [] | [] | 46 | 0.394 |
| [S21/Q19](#s21) | success | ["greenhouse__job_enhanced"] | 0 / {} | [] | [] | 8 | 0.666 |
| [S22/Q20](#s22) | success | ["greenhouse__job_enhanced", "greenhouse__recruitment_performance"] | 2 / {'INNER': 1} | ["role_category"] | ["SUM(CASE WHEN application_quarter = 3 THEN total_applications END)", "SUM(CASE WHEN application_quarter = 4 THEN total_applications END)", "SUM(CASE WHEN application_quarter = 3 THEN total_applications END)", "SUM(CASE WHEN application_quarter = 4 THEN total_applications END)", "SUM(CASE WHEN application_quarter = 3 THEN total_applications END)", "SUM(CASE WHEN application_quarter = 4 THEN total_applications END)", "SUM(CASE WHEN application_quarter = 3 THEN total_interviews END)", "SUM(CASE WHEN application_quarter = 4 THEN total_interviews END)", "SUM(CASE WHEN application_quarter = 3 THEN hired_count END)", "SUM(CASE WHEN application_quarter = 4 THEN hired_count END)", "SUM(CASE WHEN application_quarter = 4 THEN total_interviews END)", "SUM(CASE WHEN application_quarter = 4 THEN total_applications END)", "SUM(CASE WHEN application_quarter = 3 THEN total_interviews END)", "SUM(CASE WHEN application_quarter = 3 THEN total_applications END)"] | 8 | 1.044 |
| [S23/Q21](#s23) | success | ["greenhouse__job_enhanced", "greenhouse__recruitment_performance"] | 2 / {'INNER': 1} | ["role_category"] | ["SUM(CASE WHEN application_quarter = 3 THEN total_applications END)", "SUM(CASE WHEN application_quarter = 4 THEN total_applications END)", "SUM(CASE WHEN application_quarter = 3 THEN total_interviews END)", "SUM(CASE WHEN application_quarter = 4 THEN total_interviews END)", "SUM(CASE WHEN application_quarter = 3 THEN total_interviews END)", "SUM(CASE WHEN application_quarter = 3 THEN total_applications END)", "SUM(CASE WHEN application_quarter = 4 THEN total_interviews END)", "SUM(CASE WHEN application_quarter = 4 THEN total_applications END)", "SUM(CASE WHEN application_quarter = 3 THEN hired_count END)", "SUM(CASE WHEN application_quarter = 3 THEN total_applications END)", "SUM(CASE WHEN application_quarter = 4 THEN hired_count END)", "SUM(CASE WHEN application_quarter = 4 THEN total_applications END)"] | 8 | 1.148 |
| [S24/Q22](#s24) | success | ["greenhouse__job_enhanced", "greenhouse__recruitment_performance"] | 2 / {'INNER': 1} | [] | ["MIN(j.created_at)", "MAX(j.created_at)", "MIN(r.job_created_at)", "MAX(r.job_created_at)"] | 1 | 0.579 |
| [S25/Q23](#s25) | success | ["greenhouse__job_enhanced"] | 0 / {} | [] | [] | 10 | 0.292 |
| [S26/Q24](#s26) | success | ["greenhouse__job_enhanced"] | 0 / {} | ["j.created_year", "j.created_month"] | ["COUNT(DISTINCT j.job_id)", "SUM(j.count_total_applications)", "SUM(j.count_completed_interviews)", "AVG(j.application_to_interview_rate)", "SUM(j.count_total_applications)", "SUM(j.count_completed_interviews)"] | 6 | 0.581 |
| [S27/Q25](#s27) | success | ["greenhouse__job_enhanced"] | 0 / {} | [] | [] | 91 | 0.591 |
| [S28/Q26](#s28) | success | ["greenhouse__job_enhanced"] | 0 / {} | ["hiring_managers"] | ["COUNT(*)", "SUM(count_total_applications)", "SUM(count_completed_interviews)", "SUM(count_total_applications)", "SUM(count_completed_interviews)"] | 6 | 0.512 |
| [S29/Q27](#s29) | success | ["greenhouse__job_enhanced", "greenhouse__recruitment_performance"] | 2 / {'INNER': 1} | ["j.hiring_managers", "r.application_quarter"] | ["SUM(r.total_applications)", "SUM(r.total_interviews)", "SUM(r.hired_count)", "SUM(r.total_applications)", "SUM(r.total_applications)", "SUM(r.total_interviews)", "SUM(r.hired_count)"] | 12 | 0.766 |
| [S30/Q28](#s30) | success | ["greenhouse__job_enhanced"] | 0 / {} | [] | [] | 20 | 0.451 |
| [S31/Q29](#s31) | success | ["greenhouse__job_enhanced"] | 0 / {} | [] | [] | 154 | 1.089 |
| [S32/Q30](#s32) | success | ["greenhouse__job_enhanced"] | 0 / {} | [] | [] | 154 | 0.908 |
| [S33/Q31](#s33) | success | ["greenhouse__job_enhanced"] | 0 / {} | [] | [] | 154 | 0.868 |
| [S34/Q32](#s34) | success | ["greenhouse__job_enhanced", "greenhouse__recruitment_performance"] | 2 / {'INNER': 1} | ["role_category", "application_quarter"] | ["SUM(total_applications)", "SUM(total_interviews)", "SUM(total_applications)", "SUM(total_interviews)"] | 16 | 1.121 |
| [S35/Q33](#s35) | success | ["greenhouse__job_enhanced", "greenhouse__recruitment_performance"] | 2 / {'INNER': 1} | ["j.hiring_managers", "r.application_quarter"] | ["SUM(r.total_applications)", "SUM(r.total_interviews)", "SUM(r.hired_count)", "SUM(r.total_applications)", "SUM(r.total_applications)", "SUM(r.total_interviews)", "SUM(r.hired_count)"] | 12 | 0.742 |
| [S36/Q34](#s36) | success | ["greenhouse__job_enhanced"] | 0 / {} | ["j.created_month"] | ["COUNT(DISTINCT j.job_id)", "SUM(j.count_total_applications)", "SUM(j.count_completed_interviews)", "SUM(j.count_total_applications)", "SUM(j.count_completed_interviews)"] | 6 | 0.542 |
| [S37/Q35](#s37) | success | ["greenhouse__job_enhanced"] | 0 / {} | ["hiring_managers"] | ["MIN(created_month)", "MAX(created_month)", "COUNT(DISTINCT created_month)", "COUNT(DISTINCT name)", "COUNT(*)", "SUM(count_total_applications)"] | 6 | 0.662 |
| [S38/Q36](#s38) | success | ["greenhouse__job_enhanced"] | 0 / {} | ["j.hiring_managers", "(LENGTH(j.recruiters) - LENGTH(REPLACE(j.recruiters, ',', '')) + 1)"] | ["COUNT(*)", "AVG(j.application_to_interview_rate)"] | 12 | 0.772 |
| [S39/Q37](#s39) | success | ["greenhouse__job_enhanced", "greenhouse__recruitment_performance"] | 2 / {'INNER': 1} | ["r.application_quarter"] | ["SUM(r.total_applications)", "SUM(r.total_interviews)", "SUM(r.total_applications)", "SUM(r.total_interviews)"] | 2 | 0.61 |
| [S40/Q38](#s40) | success | ["greenhouse__job_enhanced", "greenhouse__recruitment_performance"] | 2 / {'INNER': 1} | ["CASE WHEN j.name LIKE 'Content Marketing%' THEN 'Content Marketing' WHEN j.name LIKE 'Digital Marketing%' THEN 'Digital Marketing' WHEN j.name LIKE 'Growth Marketing%' THEN 'Growth Marketing' WHEN j.name LIKE 'Marketing Analyst%' THEN 'Marketing Analyst' ELSE 'Other' END", "r.application_quarter"] | ["SUM(r.total_applications)", "SUM(r.total_interviews)", "SUM(r.total_applications)", "SUM(r.total_interviews)"] | 8 | 0.533 |
| [S41/Q39](#s41) | success | ["greenhouse__job_enhanced", "greenhouse__recruitment_performance"] | 2 / {'INNER': 1} | ["j.hiring_managers", "r.application_quarter"] | ["SUM(r.total_applications)", "SUM(r.total_interviews)", "SUM(r.total_applications)", "SUM(r.total_interviews)"] | 4 | 0.509 |
| [S42/Q40](#s42) | success | ["greenhouse__job_enhanced"] | 0 / {} | ["j.hiring_managers"] | ["COUNT(DISTINCT j.name)", "COUNT(DISTINCT j.created_month)", "COUNT(*)", "SUM(j.count_total_applications)", "AVG(j.application_to_interview_rate)"] | 6 | 0.547 |
| [S43/Q41](#s43) | success | ["greenhouse__job_enhanced"] | 0 / {} | [] | [] | 154 | 0.838 |
| [S44/Q42](#s44) | success | ["greenhouse__job_enhanced"] | 0 / {} | [] | [] | 154 | 0.743 |


## 元数据和设置

| SQL | 类别 | 状态 | 内容 |
| --- | --- | --- | --- |
| S1 | connection_setup | success | PRAGMA query_only=ON |
| S2 | metadata | success | SELECT name,sql FROM sqlite_master WHERE type='table' ORDER BY name |


## Python 与执行位置

人工源码审查：**database_first_violation**。Python 的相关分析、t 检验及回归属于统计补充，但仍按面试官数量计算均值和计数，并按招聘经理均值排序用于图表；这些准备操作可在 SQL 内完成。 [证据](../reviews/dacomp-066.json)。

P1：Need per-job data for Engineering to run correlation/regression analysis (number of interviewers, job creation month, hiring manager, ratings vs conversion rate). This statistical modeling (Pearson correlations, OLS regression) is not supported by SQLite, so I retrieve only the needed columns for Engineering jobs.

[源码](../../../runs/dsv4flash-db-first-full-01/dacomp-066/attempt-01/python/P1.py)；[输出](../../../runs/dsv4flash-db-first-full-01/dacomp-066/attempt-01/python/P1.stdout)；[错误](../../../runs/dsv4flash-db-first-full-01/dacomp-066/attempt-01/python/P1.stderr)。检出需人工核验的 SQL 可实现操作：.query(；不能仅凭理由判为合规。

P2：Run correlation and OLS regression on Engineering per-job data to quantify impact of number of interviewers, job creation month (time trend), job ratings, and hiring manager identity on the application-to-interview conversion rate. This statistical modeling is not supported by SQLite.

[源码](../../../runs/dsv4flash-db-first-full-01/dacomp-066/attempt-01/python/P2.py)；[输出](../../../runs/dsv4flash-db-first-full-01/dacomp-066/attempt-01/python/P2.stdout)；[错误](../../../runs/dsv4flash-db-first-full-01/dacomp-066/attempt-01/python/P2.stderr)。检出需人工核验的 SQL 可实现操作：groupby(, .query(；不能仅凭理由判为合规。

P3：statsmodels is not installed; I will implement ordinary least squares manually with numpy to quantify the marginal impact of number of interviewers, creation month, ratings, and hiring manager dummies on conversion rate.

[源码](../../../runs/dsv4flash-db-first-full-01/dacomp-066/attempt-01/python/P3.py)；[输出](../../../runs/dsv4flash-db-first-full-01/dacomp-066/attempt-01/python/P3.stdout)；[错误](../../../runs/dsv4flash-db-first-full-01/dacomp-066/attempt-01/python/P3.stderr)。检出需人工核验的 SQL 可实现操作：groupby(, .query(；不能仅凭理由判为合规。

P4：Create visualizations for the report: (1) Role-level conversion rate trend from Q3 to Q4, (2) Hiring manager conversion rates, (3) The impact of number of interviewers and creation month on conversion rate. These visualizations require matplotlib, not supported by SQLite.

[源码](../../../runs/dsv4flash-db-first-full-01/dacomp-066/attempt-01/python/P4.py)；[输出](../../../runs/dsv4flash-db-first-full-01/dacomp-066/attempt-01/python/P4.stdout)；[错误](../../../runs/dsv4flash-db-first-full-01/dacomp-066/attempt-01/python/P4.stderr)。检出需人工核验的 SQL 可实现操作：.query(, sort_values(；不能仅凭理由判为合规。

P5：Check if Marketing department shows similar patterns and if there is any manager-level proxy for experience (e.g., number of distinct job titles managed). This comparison is outside SQL scope.

[源码](../../../runs/dsv4flash-db-first-full-01/dacomp-066/attempt-01/python/P5.py)；[输出](../../../runs/dsv4flash-db-first-full-01/dacomp-066/attempt-01/python/P5.stdout)；[错误](../../../runs/dsv4flash-db-first-full-01/dacomp-066/attempt-01/python/P5.stderr)。检出需人工核验的 SQL 可实现操作：.query(；不能仅凭理由判为合规。

P6：Create a boxplot showing the distribution of conversion rates by hiring manager for Engineering, and a scatter plot of conversion rate vs creation month colored by number of interviewers. These visualizations help illustrate the regression findings.

[源码](../../../runs/dsv4flash-db-first-full-01/dacomp-066/attempt-01/python/P6.py)；[输出](../../../runs/dsv4flash-db-first-full-01/dacomp-066/attempt-01/python/P6.stdout)；[错误](../../../runs/dsv4flash-db-first-full-01/dacomp-066/attempt-01/python/P6.stderr)。检出需人工核验的 SQL 可实现操作：groupby(, .query(, sort_values(；不能仅凭理由判为合规。

P7：Retry the boxplot with the correct matplotlib API (set tick labels after creating boxplot) and the scatter plot for creation month vs conversion rate colored by number of interviewers.

[源码](../../../runs/dsv4flash-db-first-full-01/dacomp-066/attempt-01/python/P7.py)；[输出](../../../runs/dsv4flash-db-first-full-01/dacomp-066/attempt-01/python/P7.stdout)；[错误](../../../runs/dsv4flash-db-first-full-01/dacomp-066/attempt-01/python/P7.stderr)。检出需人工核验的 SQL 可实现操作：groupby(, .query(, sort_values(；不能仅凭理由判为合规。

## 优化机会

已验证候选。筛选限于精确 SQL、相同自包含 CTE、相同单表完整过滤、可分解单表聚合；未覆盖任意 Join 等价和一般谓词蕴含。全部候选都是 offline，未测在线预测。

| 候选 | 类型 | 已有结果 | 覆盖 SQL | 后续次数 | 中间行数 | 验证 | 成本 |
| --- | --- | --- | --- | --- | --- | --- | --- |
| C1 | exact-result reuse | True | ["S12", "S20"] | 1 | unknown | not_verified_cap | Not tested |
| C2 | exact-result reuse | True | ["S43", "S44"] | 1 | 154 | verified | Not benchmarked; correctness alone does not establish net speedup. |
| C3 | common subexpression | False | ["S22", "S23"] | 1 | 154 | verified | Not benchmarked; correctness alone does not establish net speedup. |
| C4 | common filtered view | False | ["S6", "S12", "S15", "S18", "S20", "S21", "S25", "S26", "S28", "S31", "S32", "S33", "S36", "S37", "S38", "S42", "S43", "S44"] | 17 | 154 | verified | Not benchmarked; correctness alone does not establish net speedup. |
| C5 | aggregate MV | False | ["S28", "S38"] | 1 | unknown | not_verified_cap | Not tested |
| C6 | common filtered view | False | ["S7", "S13"] | 1 | unknown | not_verified_cap | Not tested |


已验证覆盖（含触发查询、候选并集去重）：20/42 条成功数据 SQL。正确性仅针对当前数据库快照；未测性能的候选不能声称已加速。

[完整 build/rewrite 与比较证据](dacomp-066.analysis.json)。

### C4：common filtered view

Same single source and complete filter; original filter retained.

原查询 [S6](#s6), [S12](#s12), [S15](#s15), [S18](#s18), [S20](#s20), [S21](#s21), [S25](#s25), [S26](#s26), [S28](#s28), [S31](#s31), [S32](#s32), [S33](#s33), [S36](#s36), [S37](#s37), [S38](#s38), [S42](#s42), [S43](#s43), [S44](#s44) → 新增共享状态 C4 → 后续 17 次可复用。该构建点为事后假设，不代表 Agent 当时预知后续。

构建定义：

```sql
SELECT * FROM "greenhouse__job_enhanced" WHERE departments = 'Engineering'
```

受益查询 S6 的改写示例：

```sql
SELECT DISTINCT j.name, j.departments, j.hiring_managers FROM temp.reuse_candidate AS j WHERE j.departments = 'Engineering' LIMIT 30
```

| 原 SQL | 列名一致 | 结果一致 | 比较方法 |
| --- | --- | --- | --- |
| S6 | True | True | exact_multiset |
| S12 | True | True | ordered_numeric_tolerance |
| S15 | True | True | ordered_numeric_tolerance |
| S18 | True | True | exact_multiset |
| S20 | True | True | ordered_numeric_tolerance |
| S21 | True | True | ordered_numeric_tolerance |
| S25 | True | True | exact_multiset |
| S26 | True | True | ordered_numeric_tolerance |
| S28 | True | True | ordered_numeric_tolerance |
| S31 | True | True | ordered_numeric_tolerance |
| S32 | True | True | exact_multiset |
| S33 | True | True | exact_multiset |
| S36 | True | True | ordered_numeric_tolerance |
| S37 | True | True | ordered_numeric_tolerance |
| S38 | True | True | ordered_numeric_tolerance |
| S42 | True | True | ordered_numeric_tolerance |
| S43 | True | True | exact_multiset |
| S44 | True | True | exact_multiset |


验证状态：verified；成本结论：Not benchmarked; correctness alone does not establish net speedup.

### C2：exact-result reuse

Identical normalized SQL and parameters; archive equality checked.

原查询 [S43](#s43), [S44](#s44) → 保留前序结果 S43 → 后续 1 次可复用。该构建点为事后假设，不代表 Agent 当时预知后续。

| 原 SQL | 列名一致 | 结果一致 | 比较方法 |
| --- | --- | --- | --- |
| S44 | True | True | exact_multiset |


验证状态：verified；成本结论：Not benchmarked; correctness alone does not establish net speedup.

### C3：common subexpression

Identical self-contained CTE body across queries.

原查询 [S22](#s22), [S23](#s23) → 新增共享状态 C3 → 后续 1 次可复用。该构建点为事后假设，不代表 Agent 当时预知后续。

构建定义：

```sql
SELECT r.*, j.name AS job_name, j.departments, CASE WHEN j.name LIKE 'Frontend%' THEN 'Frontend' WHEN j.name LIKE 'Backend%' THEN 'Backend' WHEN j.name LIKE 'Full Stack%' THEN 'Full Stack' WHEN j.name LIKE 'Data Engineer%' THEN 'Data Engineer' WHEN j.name LIKE 'DevOps%' THEN 'DevOps' WHEN j.name LIKE 'Mobile%' THEN 'Mobile' WHEN j.name LIKE 'QA%' THEN 'QA' WHEN j.name LIKE 'Machine Learning%' THEN 'Machine Learning' ELSE 'Other' END AS role_category FROM greenhouse__recruitment_performance AS r JOIN greenhouse__job_enhanced AS j ON r.job_id = j.job_id WHERE j.departments = 'Engineering'
```

受益查询 S22 的改写示例：

```sql
WITH eng AS (SELECT * FROM temp.reuse_candidate) SELECT role_category, SUM(CASE WHEN application_quarter = 3 THEN total_applications END) AS q3_apps, SUM(CASE WHEN application_quarter = 4 THEN total_applications END) AS q4_apps, ROUND(100.0 * SUM(CASE WHEN application_quarter = 3 THEN total_interviews END) / SUM(CASE WHEN application_quarter = 3 THEN total_applications END), 2) AS q3_interview_rate, ROUND(100.0 * SUM(CASE WHEN application_quarter = 4 THEN total_interviews END) / SUM(CASE WHEN application_quarter = 4 THEN total_applications END), 2) AS q4_interview_rate, ROUND(100.0 * SUM(CASE WHEN application_quarter = 3 THEN hired_count END) / SUM(CASE WHEN application_quarter = 3 THEN total_applications END), 2) AS q3_hire_rate, ROUND(100.0 * SUM(CASE WHEN application_quarter = 4 THEN hired_count END) / SUM(CASE WHEN application_quarter = 4 THEN total_applications END), 2) AS q4_hire_rate, ROUND(100.0 * (SUM(CASE WHEN application_quarter = 4 THEN total_interviews END) / SUM(CASE WHEN application_quarter = 4 THEN total_applications END)) - 100.0 * (SUM(CASE WHEN application_quarter = 3 THEN total_interviews END) / SUM(CASE WHEN application_quarter = 3 THEN total_applications END)), 2) AS interview_rate_pp_change FROM eng GROUP BY role_category ORDER BY interview_rate_pp_change ASC
```

| 原 SQL | 列名一致 | 结果一致 | 比较方法 |
| --- | --- | --- | --- |
| S22 | True | True | ordered_numeric_tolerance |
| S23 | True | True | ordered_numeric_tolerance |


验证状态：verified；成本结论：Not benchmarked; correctness alone does not establish net speedup.

结果依赖：自动记录 SQL→Python 的接口父调用，以及源码中引用归档文件的消费者；字面值相同不认定因果。模型方向选择需要人工读取消息，尚未做全面因果标注。

[原始报告](../../../runs/dsv4flash-db-first-full-01/dacomp-066/attempt-01/answer.md)；[统一消息](../../../runs/dsv4flash-db-first-full-01/dacomp-066/attempt-01/messages.jsonl)；[原始 OpenCode 事件](../../../runs/dsv4flash-db-first-full-01/dacomp-066/attempt-01/opencode.jsonl)；[SQL 引擎日志](../../../runs/dsv4flash-db-first-full-01/dacomp-066/attempt-01/sql_journal.jsonl)。

[可读报告（本地图片链接规范化）](../answers/dacomp-066.md)。原始回答保留，分析结论未改写。

## S1

类别 `connection_setup`；来源 `connection`；调用 `0f2731f9319142178d6336c4a798324a`；状态 `success`。

```sql
PRAGMA query_only=ON
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-066/attempt-01/sql/S1.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-066/attempt-01/sql/S1.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-066/attempt-01/results/S1.rows.jsonl)；完整：True；SHA256：`e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`。

## S2

类别 `metadata`；来源 `list_db`；调用 `0f2731f9319142178d6336c4a798324a`；状态 `success`。

```sql
SELECT name,sql FROM sqlite_master WHERE type='table' ORDER BY name
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-066/attempt-01/sql/S2.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-066/attempt-01/sql/S2.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-066/attempt-01/results/S2.rows.jsonl)；完整：True；SHA256：`c3e30c5469332a0f0029e9bb5186385360e3739a70ac11b89e6f15103c358834`。

## S3

类别 `data`；来源 `query_db`；调用 `7511997df06040b19fb5bf3acde25fb2`；状态 `success`。

```sql
SELECT * FROM greenhouse__recruitment_performance LIMIT 20
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-066/attempt-01/sql/S3.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-066/attempt-01/sql/S3.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-066/attempt-01/results/S3.rows.jsonl)；完整：True；SHA256：`51c3299fde90819b80422a41c883af78644383ce8072e5db8fd0bef046d59768`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "greenhouse__recruitment_performance", "kind": "base", "block": null, "base_tables": ["greenhouse__recruitment_performance"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |


## S4

类别 `data`；来源 `query_db`；调用 `e261d5be771244f89c3d3a107596f10d`；状态 `success`。

```sql
SELECT DISTINCT job_title FROM greenhouse__recruitment_performance ORDER BY job_title
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-066/attempt-01/sql/S4.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-066/attempt-01/sql/S4.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-066/attempt-01/results/S4.rows.jsonl)；完整：True；SHA256：`75f20298f6d3b3eaa38ca4f2782a342c3b249197dfbf255b30dd4e5293ef13a9`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "greenhouse__recruitment_performance", "kind": "base", "block": null, "base_tables": ["greenhouse__recruitment_performance"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |


## S5

类别 `data`；来源 `query_db`；调用 `b0e49f66930f417c8d243417f263b876`；状态 `success`。

```sql
SELECT DISTINCT departments FROM greenhouse__job_enhanced ORDER BY departments
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-066/attempt-01/sql/S5.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-066/attempt-01/sql/S5.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-066/attempt-01/results/S5.rows.jsonl)；完整：True；SHA256：`619bc0bf2bec97c5f9c6aecc1fb2fb32949acb808927a07aafb90aa5a08513ea`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "greenhouse__job_enhanced", "kind": "base", "block": null, "base_tables": ["greenhouse__job_enhanced"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |


## S6

类别 `data`；来源 `query_db`；调用 `5582a42b1dc44917b69cf13372ca38da`；状态 `success`。

```sql
SELECT DISTINCT j.name, j.departments, j.hiring_managers 
FROM greenhouse__job_enhanced j 
WHERE j.departments = 'Engineering' 
LIMIT 30
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-066/attempt-01/sql/S6.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-066/attempt-01/sql/S6.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-066/attempt-01/results/S6.rows.jsonl)；完整：True；SHA256：`cb41e0cce2cd5ce78478a545af08d3f6cd7fed69598092562f358706f4bf08ea`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "j", "kind": "base", "block": null, "base_tables": ["greenhouse__job_enhanced"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |


## S7

类别 `data`；来源 `query_db`；调用 `fd44b1ee81ba453b8a91f9a459fefaa8`；状态 `success`。

```sql
SELECT DISTINCT j.name, j.departments, j.hiring_managers 
FROM greenhouse__job_enhanced j 
WHERE j.departments = 'Marketing' 
LIMIT 30
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-066/attempt-01/sql/S7.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-066/attempt-01/sql/S7.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-066/attempt-01/results/S7.rows.jsonl)；完整：True；SHA256：`ee5fdf7741d0e935b45842c0bf4c0e577b56f9f8b56fb79ca44856fa1226995d`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "j", "kind": "base", "block": null, "base_tables": ["greenhouse__job_enhanced"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |


## S8

类别 `data`；来源 `query_db`；调用 `548b2ad4aa2443cbb42c874511593699`；状态 `success`。

```sql
SELECT DISTINCT application_year, application_quarter FROM greenhouse__recruitment_performance ORDER BY application_year, application_quarter
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-066/attempt-01/sql/S8.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-066/attempt-01/sql/S8.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-066/attempt-01/results/S8.rows.jsonl)；完整：True；SHA256：`b660d3c57a06809abad046f7c507ba3cd53308687bf6b60b29f8ad3d72105bd3`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "greenhouse__recruitment_performance", "kind": "base", "block": null, "base_tables": ["greenhouse__recruitment_performance"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |


## S9

类别 `data`；来源 `query_db`；调用 `6880c09d87694c2fb3f0965d3422ea90`；状态 `success`。

```sql
SELECT COUNT(*) AS n FROM greenhouse__recruitment_performance
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-066/attempt-01/sql/S9.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-066/attempt-01/sql/S9.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-066/attempt-01/results/S9.rows.jsonl)；完整：True；SHA256：`2a754072b022df556c621f749199d09e057cbc139ceb3a4723cda565dc5c2916`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "greenhouse__recruitment_performance", "kind": "base", "block": null, "base_tables": ["greenhouse__recruitment_performance"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |


## S10

类别 `data`；来源 `query_db`；调用 `1f82c648b52f40d2bdace10f3aaecc2a`；状态 `success`。

```sql
SELECT COUNT(*) AS n, COUNT(DISTINCT job_id) AS jobs FROM greenhouse__job_enhanced
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-066/attempt-01/sql/S10.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-066/attempt-01/sql/S10.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-066/attempt-01/results/S10.rows.jsonl)；完整：True；SHA256：`682ad76cbf14a1ce25eb54dafed14bf455931f77deb106ee68203e30184ede31`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "greenhouse__job_enhanced", "kind": "base", "block": null, "base_tables": ["greenhouse__job_enhanced"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |
| B1 | COUNT(DISTINCT job_id) | [{"table": "greenhouse__job_enhanced", "column": "job_id"}] | [] | False |


## S11

类别 `data`；来源 `query_db`；调用 `10bca855194b4c5c9a2886fe56e4efe7`；状态 `success`。

```sql
SELECT r.application_quarter, j.departments,
  SUM(r.total_applications) AS apps,
  SUM(r.total_interviews) AS interviews,
  ROUND(100.0*SUM(r.total_interviews)/SUM(r.total_applications),2) AS app_to_interview_pct,
  ROUND(100.0*SUM(r.hired_count)/SUM(r.total_applications),2) AS hire_pct
FROM greenhouse__recruitment_performance r
JOIN greenhouse__job_enhanced j ON r.job_id = j.job_id
GROUP BY r.application_quarter, j.departments
ORDER BY r.application_quarter, j.departments
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-066/attempt-01/sql/S11.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-066/attempt-01/sql/S11.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-066/attempt-01/results/S11.rows.jsonl)；完整：True；SHA256：`846b90b47cc5e596912ea410e34d6ae2ce332534eb9a51000956717793a77346`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "r", "kind": "base", "block": null, "base_tables": ["greenhouse__recruitment_performance"]}, {"alias": "j", "kind": "base", "block": null, "base_tables": ["greenhouse__job_enhanced"]}] | [{"type": "INNER", "right": "greenhouse__job_enhanced AS j", "on": "r.job_id = j.job_id", "using": []}] | ["r.application_quarter", "j.departments"] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | SUM(r.total_applications) | [{"table": "greenhouse__recruitment_performance", "column": "total_applications"}] | [] | False |
| B1 | SUM(r.total_interviews) | [{"table": "greenhouse__recruitment_performance", "column": "total_interviews"}] | [] | False |
| B1 | SUM(r.total_applications) | [{"table": "greenhouse__recruitment_performance", "column": "total_applications"}] | [] | False |
| B1 | SUM(r.total_applications) | [{"table": "greenhouse__recruitment_performance", "column": "total_applications"}] | [] | False |
| B1 | SUM(r.total_interviews) | [{"table": "greenhouse__recruitment_performance", "column": "total_interviews"}] | [] | False |
| B1 | SUM(r.hired_count) | [{"table": "greenhouse__recruitment_performance", "column": "hired_count"}] | [] | False |


## S12

类别 `data`；来源 `query_db`；调用 `86faaf4d2ac6408b8d83b90bbb7dd1bc`；状态 `success`。

```sql
SELECT DISTINCT j.name
FROM greenhouse__job_enhanced j
WHERE j.departments = 'Engineering'
ORDER BY j.name
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-066/attempt-01/sql/S12.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-066/attempt-01/sql/S12.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-066/attempt-01/results/S12.rows.jsonl)；完整：True；SHA256：`6110798b8ba5d3cbb8c9260bbf65dc5f95682d81214c90a90e781d08280da0b7`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "j", "kind": "base", "block": null, "base_tables": ["greenhouse__job_enhanced"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |


## S13

类别 `data`；来源 `query_db`；调用 `d0b8f7c5e7ff4f6093b70fc682d9389a`；状态 `success`。

```sql
SELECT DISTINCT j.name
FROM greenhouse__job_enhanced j
WHERE j.departments = 'Marketing'
ORDER BY j.name
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-066/attempt-01/sql/S13.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-066/attempt-01/sql/S13.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-066/attempt-01/results/S13.rows.jsonl)；完整：True；SHA256：`bd5666a98b58c8c9f76370f7be46785ac13f6a33e0d4e2a760b01fe76c670682`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "j", "kind": "base", "block": null, "base_tables": ["greenhouse__job_enhanced"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |


## S14

类别 `data`；来源 `query_db`；调用 `1de6459afe48462d9ecd423ce13ff97c`；状态 `success`。

```sql
SELECT DISTINCT hiring_managers FROM greenhouse__job_enhanced ORDER BY hiring_managers
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-066/attempt-01/sql/S14.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-066/attempt-01/sql/S14.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-066/attempt-01/results/S14.rows.jsonl)；完整：True；SHA256：`d179ef429cbce79c8cd200d18697b4023577d13a657e74212c877991a5ba8697`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "greenhouse__job_enhanced", "kind": "base", "block": null, "base_tables": ["greenhouse__job_enhanced"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |


## S15

类别 `data`；来源 `query_db`；调用 `75b669c56b30470ab3eddffc9acbcbec`；状态 `success`。

```sql
SELECT j.name, j.departments, j.hiring_managers, j.recruiters, j.sourcers
FROM greenhouse__job_enhanced j
WHERE j.departments = 'Engineering'
ORDER BY j.name
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-066/attempt-01/sql/S15.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-066/attempt-01/sql/S15.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-066/attempt-01/results/S15.rows.jsonl)；完整：True；SHA256：`ed2fd1fded9cfd10ef23ee6d10a77c5df0422447d17ed25c0f0621e131e96061`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "j", "kind": "base", "block": null, "base_tables": ["greenhouse__job_enhanced"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |


## S16

类别 `data`；来源 `query_db`；调用 `90d6e8bd38f645b5a4b1dcd0974f1061`；状态 `success`。

```sql
SELECT DISTINCT recruiters FROM greenhouse__job_enhanced ORDER BY recruiters
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-066/attempt-01/sql/S16.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-066/attempt-01/sql/S16.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-066/attempt-01/results/S16.rows.jsonl)；完整：True；SHA256：`956c5efd6c4aa77164b0b9ca982e7a836184e9cc37a784a6c626a316a4a56d5c`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "greenhouse__job_enhanced", "kind": "base", "block": null, "base_tables": ["greenhouse__job_enhanced"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |


## S17

类别 `data`；来源 `query_db`；调用 `f2eed893fb7b4181a0c20aa378efacb8`；状态 `success`。

```sql
SELECT DISTINCT sourcers FROM greenhouse__job_enhanced ORDER BY sourcers
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-066/attempt-01/sql/S17.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-066/attempt-01/sql/S17.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-066/attempt-01/results/S17.rows.jsonl)；完整：True；SHA256：`78ee7479f1bf7cbac39c360a51a1f5949654a8aa952ef9116831a80301dc73f1`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "greenhouse__job_enhanced", "kind": "base", "block": null, "base_tables": ["greenhouse__job_enhanced"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |


## S18

类别 `data`；来源 `query_db`；调用 `4b8a899f3aeb4fc794e0a91270903d3e`；状态 `success`。

```sql
SELECT job_id, name, hiring_managers, recruiters, sourcers,
       count_total_interviews, count_completed_interviews,
       count_total_applications, count_completed_interviews
FROM greenhouse__job_enhanced
WHERE departments='Engineering'
LIMIT 10
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-066/attempt-01/sql/S18.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-066/attempt-01/sql/S18.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-066/attempt-01/results/S18.rows.jsonl)；完整：True；SHA256：`f951a1397c868c862ed19ed10adffc2039f45c332089389f41edb922ff907580`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "greenhouse__job_enhanced", "kind": "base", "block": null, "base_tables": ["greenhouse__job_enhanced"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |


## S19

类别 `data`；来源 `query_db`；调用 `92a40dcc66b640d7b3887c0cbb5ca3a4`；状态 `success`。

```sql
-- Get Engineering job titles and derive role categories, with quarterly conversion rates
SELECT 
  CASE 
    WHEN r.job_title LIKE 'Frontend%' THEN 'Frontend Engineer'
    WHEN r.job_title LIKE 'Backend%' THEN 'Backend Engineer'
    WHEN r.job_title LIKE 'Full Stack%' THEN 'Full Stack Engineer'
    WHEN r.job_title LIKE 'Data Engineer%' THEN 'Data Engineer'
    ELSE r.job_title
  END AS role_category,
  r.application_year,
  r.application_quarter,
  SUM(r.total_applications) AS total_apps,
  SUM(r.total_interviews) AS total_interviews,
  SUM(r.hired_count) AS total_hired,
  ROUND(100.0 * SUM(r.total_interviews) / SUM(r.total_applications), 2) AS interview_rate
FROM greenhouse__recruitment_performance r
JOIN greenhouse__job_enhanced j ON r.job_id = j.job_id
WHERE j.departments = 'Engineering'
GROUP BY role_category, r.application_year, r.application_quarter
ORDER BY role_category, r.application_year, r.application_quarter
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-066/attempt-01/sql/S19.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-066/attempt-01/sql/S19.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-066/attempt-01/results/S19.rows.jsonl)；完整：True；SHA256：`598ec950d5172304b79738b75df7270b0abe9e19e929d78dbae3ffe83291fd27`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "r", "kind": "base", "block": null, "base_tables": ["greenhouse__recruitment_performance"]}, {"alias": "j", "kind": "base", "block": null, "base_tables": ["greenhouse__job_enhanced"]}] | [{"type": "INNER", "right": "greenhouse__job_enhanced AS j", "on": "r.job_id = j.job_id", "using": []}] | ["CASE WHEN r.job_title LIKE 'Frontend%' THEN 'Frontend Engineer' WHEN r.job_title LIKE 'Backend%' THEN 'Backend Engineer' WHEN r.job_title LIKE 'Full Stack%' THEN 'Full Stack Engineer' WHEN r.job_title LIKE 'Data Engineer%' THEN 'Data Engineer' ELSE r.job_title END", "r.application_year", "r.application_quarter"] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | SUM(r.total_applications) | [{"table": "greenhouse__recruitment_performance", "column": "total_applications"}] | [] | False |
| B1 | SUM(r.total_interviews) | [{"table": "greenhouse__recruitment_performance", "column": "total_interviews"}] | [] | False |
| B1 | SUM(r.hired_count) | [{"table": "greenhouse__recruitment_performance", "column": "hired_count"}] | [] | False |
| B1 | SUM(r.total_applications) | [{"table": "greenhouse__recruitment_performance", "column": "total_applications"}] | [] | False |
| B1 | SUM(r.total_interviews) | [{"table": "greenhouse__recruitment_performance", "column": "total_interviews"}] | [] | False |


## S20

类别 `data`；来源 `query_db`；调用 `a62fc19b020c4b0aacb91ac17a253473`；状态 `success`。

```sql
SELECT DISTINCT j.name
FROM greenhouse__job_enhanced j
WHERE j.departments = 'Engineering'
ORDER BY j.name
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-066/attempt-01/sql/S20.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-066/attempt-01/sql/S20.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-066/attempt-01/results/S20.rows.jsonl)；完整：True；SHA256：`6110798b8ba5d3cbb8c9260bbf65dc5f95682d81214c90a90e781d08280da0b7`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "j", "kind": "base", "block": null, "base_tables": ["greenhouse__job_enhanced"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |


## S21

类别 `data`；来源 `query_db`；调用 `5ba6ed15dd6e498bab9ef13b024a02ca`；状态 `success`。

```sql
SELECT DISTINCT 
  CASE 
    WHEN j.name LIKE 'Frontend%' THEN 'Frontend'
    WHEN j.name LIKE 'Backend%' THEN 'Backend'
    WHEN j.name LIKE 'Full Stack%' THEN 'Full Stack'
    WHEN j.name LIKE 'Data Engineer%' THEN 'Data Engineer'
    WHEN j.name LIKE 'DevOps%' THEN 'DevOps'
    WHEN j.name LIKE 'Mobile%' THEN 'Mobile'
    WHEN j.name LIKE 'QA%' THEN 'QA'
    WHEN j.name LIKE 'Security%' THEN 'Security'
    WHEN j.name LIKE 'Site Reliability%' THEN 'Site Reliability'
    WHEN j.name LIKE 'Machine Learning%' THEN 'Machine Learning'
    WHEN j.name LIKE 'Systems%' THEN 'Systems'
    WHEN j.name LIKE 'Engineering Manager%' THEN 'Engineering Manager'
    ELSE 'Other'
  END AS role_category
FROM greenhouse__job_enhanced j
WHERE j.departments = 'Engineering'
ORDER BY role_category
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-066/attempt-01/sql/S21.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-066/attempt-01/sql/S21.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-066/attempt-01/results/S21.rows.jsonl)；完整：True；SHA256：`c5da816058b430e558630eb639af460ed662612400abf05ff2642703bb568b6b`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "j", "kind": "base", "block": null, "base_tables": ["greenhouse__job_enhanced"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |


## S22

类别 `data`；来源 `query_db`；调用 `5d2e9d7c3776439f9503a42a98670009`；状态 `success`。

```sql
WITH eng AS (
  SELECT r.*, j.name AS job_name, j.departments,
    CASE 
      WHEN j.name LIKE 'Frontend%' THEN 'Frontend'
      WHEN j.name LIKE 'Backend%' THEN 'Backend'
      WHEN j.name LIKE 'Full Stack%' THEN 'Full Stack'
      WHEN j.name LIKE 'Data Engineer%' THEN 'Data Engineer'
      WHEN j.name LIKE 'DevOps%' THEN 'DevOps'
      WHEN j.name LIKE 'Mobile%' THEN 'Mobile'
      WHEN j.name LIKE 'QA%' THEN 'QA'
      WHEN j.name LIKE 'Machine Learning%' THEN 'Machine Learning'
      ELSE 'Other'
    END AS role_category
  FROM greenhouse__recruitment_performance r
  JOIN greenhouse__job_enhanced j ON r.job_id = j.job_id
  WHERE j.departments = 'Engineering'
)
SELECT role_category,
  SUM(CASE WHEN application_quarter=3 THEN total_applications END) AS q3_apps,
  SUM(CASE WHEN application_quarter=4 THEN total_applications END) AS q4_apps,
  ROUND(100.0*SUM(CASE WHEN application_quarter=3 THEN total_interviews END)/SUM(CASE WHEN application_quarter=3 THEN total_applications END),2) AS q3_interview_rate,
  ROUND(100.0*SUM(CASE WHEN application_quarter=4 THEN total_interviews END)/SUM(CASE WHEN application_quarter=4 THEN total_applications END),2) AS q4_interview_rate,
  ROUND(100.0*SUM(CASE WHEN application_quarter=3 THEN hired_count END)/SUM(CASE WHEN application_quarter=3 THEN total_applications END),2) AS q3_hire_rate,
  ROUND(100.0*SUM(CASE WHEN application_quarter=4 THEN hired_count END)/SUM(CASE WHEN application_quarter=4 THEN total_applications END),2) AS q4_hire_rate,
  ROUND(100.0*(SUM(CASE WHEN application_quarter=4 THEN total_interviews END)/SUM(CASE WHEN application_quarter=4 THEN total_applications END)) - 100.0*(SUM(CASE WHEN application_quarter=3 THEN total_interviews END)/SUM(CASE WHEN application_quarter=3 THEN total_applications END)),2) AS interview_rate_pp_change
FROM eng
GROUP BY role_category
ORDER BY interview_rate_pp_change ASC
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-066/attempt-01/sql/S22.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-066/attempt-01/sql/S22.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-066/attempt-01/results/S22.rows.jsonl)；完整：True；SHA256：`94405745a0b3dc636fb61b51a08df0f3c44e907c42d2c7ecf2095edf421893a8`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "r", "kind": "base", "block": null, "base_tables": ["greenhouse__recruitment_performance"]}, {"alias": "j", "kind": "base", "block": null, "base_tables": ["greenhouse__job_enhanced"]}] | [{"type": "INNER", "right": "greenhouse__job_enhanced AS j", "on": "r.job_id = j.job_id", "using": []}] | [] |
| B2 | [{"alias": "eng", "kind": "derived", "block": "B1", "base_tables": ["greenhouse__job_enhanced", "greenhouse__recruitment_performance"]}] | [] | ["role_category"] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B2 | SUM(CASE WHEN application_quarter = 3 THEN total_applications END) | [{"table": "greenhouse__recruitment_performance", "column": "total_applications"}] | [{"table": "greenhouse__recruitment_performance", "column": "application_quarter"}] | False |
| B2 | SUM(CASE WHEN application_quarter = 4 THEN total_applications END) | [{"table": "greenhouse__recruitment_performance", "column": "total_applications"}] | [{"table": "greenhouse__recruitment_performance", "column": "application_quarter"}] | False |
| B2 | SUM(CASE WHEN application_quarter = 3 THEN total_applications END) | [{"table": "greenhouse__recruitment_performance", "column": "total_applications"}] | [{"table": "greenhouse__recruitment_performance", "column": "application_quarter"}] | False |
| B2 | SUM(CASE WHEN application_quarter = 4 THEN total_applications END) | [{"table": "greenhouse__recruitment_performance", "column": "total_applications"}] | [{"table": "greenhouse__recruitment_performance", "column": "application_quarter"}] | False |
| B2 | SUM(CASE WHEN application_quarter = 3 THEN total_applications END) | [{"table": "greenhouse__recruitment_performance", "column": "total_applications"}] | [{"table": "greenhouse__recruitment_performance", "column": "application_quarter"}] | False |
| B2 | SUM(CASE WHEN application_quarter = 4 THEN total_applications END) | [{"table": "greenhouse__recruitment_performance", "column": "total_applications"}] | [{"table": "greenhouse__recruitment_performance", "column": "application_quarter"}] | False |
| B2 | SUM(CASE WHEN application_quarter = 3 THEN total_interviews END) | [{"table": "greenhouse__recruitment_performance", "column": "total_interviews"}] | [{"table": "greenhouse__recruitment_performance", "column": "application_quarter"}] | False |
| B2 | SUM(CASE WHEN application_quarter = 4 THEN total_interviews END) | [{"table": "greenhouse__recruitment_performance", "column": "total_interviews"}] | [{"table": "greenhouse__recruitment_performance", "column": "application_quarter"}] | False |
| B2 | SUM(CASE WHEN application_quarter = 3 THEN hired_count END) | [{"table": "greenhouse__recruitment_performance", "column": "hired_count"}] | [{"table": "greenhouse__recruitment_performance", "column": "application_quarter"}] | False |
| B2 | SUM(CASE WHEN application_quarter = 4 THEN hired_count END) | [{"table": "greenhouse__recruitment_performance", "column": "hired_count"}] | [{"table": "greenhouse__recruitment_performance", "column": "application_quarter"}] | False |
| B2 | SUM(CASE WHEN application_quarter = 4 THEN total_interviews END) | [{"table": "greenhouse__recruitment_performance", "column": "total_interviews"}] | [{"table": "greenhouse__recruitment_performance", "column": "application_quarter"}] | False |
| B2 | SUM(CASE WHEN application_quarter = 4 THEN total_applications END) | [{"table": "greenhouse__recruitment_performance", "column": "total_applications"}] | [{"table": "greenhouse__recruitment_performance", "column": "application_quarter"}] | False |
| B2 | SUM(CASE WHEN application_quarter = 3 THEN total_interviews END) | [{"table": "greenhouse__recruitment_performance", "column": "total_interviews"}] | [{"table": "greenhouse__recruitment_performance", "column": "application_quarter"}] | False |
| B2 | SUM(CASE WHEN application_quarter = 3 THEN total_applications END) | [{"table": "greenhouse__recruitment_performance", "column": "total_applications"}] | [{"table": "greenhouse__recruitment_performance", "column": "application_quarter"}] | False |


## S23

类别 `data`；来源 `query_db`；调用 `5e2ba5b1c42f4269899a83814e05de10`；状态 `success`。

```sql
WITH eng AS (
  SELECT r.*, j.name AS job_name, j.departments,
    CASE 
      WHEN j.name LIKE 'Frontend%' THEN 'Frontend'
      WHEN j.name LIKE 'Backend%' THEN 'Backend'
      WHEN j.name LIKE 'Full Stack%' THEN 'Full Stack'
      WHEN j.name LIKE 'Data Engineer%' THEN 'Data Engineer'
      WHEN j.name LIKE 'DevOps%' THEN 'DevOps'
      WHEN j.name LIKE 'Mobile%' THEN 'Mobile'
      WHEN j.name LIKE 'QA%' THEN 'QA'
      WHEN j.name LIKE 'Machine Learning%' THEN 'Machine Learning'
      ELSE 'Other'
    END AS role_category
  FROM greenhouse__recruitment_performance r
  JOIN greenhouse__job_enhanced j ON r.job_id = j.job_id
  WHERE j.departments = 'Engineering'
)
SELECT role_category,
  SUM(CASE WHEN application_quarter=3 THEN total_applications END) AS q3_apps,
  SUM(CASE WHEN application_quarter=4 THEN total_applications END) AS q4_apps,
  SUM(CASE WHEN application_quarter=3 THEN total_interviews END) AS q3_interviews,
  SUM(CASE WHEN application_quarter=4 THEN total_interviews END) AS q4_interviews,
  ROUND(100.0 * SUM(CASE WHEN application_quarter=3 THEN total_interviews END) / NULLIF(SUM(CASE WHEN application_quarter=3 THEN total_applications END), 0), 2) AS q3_interview_rate,
  ROUND(100.0 * SUM(CASE WHEN application_quarter=4 THEN total_interviews END) / NULLIF(SUM(CASE WHEN application_quarter=4 THEN total_applications END), 0), 2) AS q4_interview_rate,
  ROUND(100.0 * SUM(CASE WHEN application_quarter=3 THEN hired_count END) / NULLIF(SUM(CASE WHEN application_quarter=3 THEN total_applications END), 0), 2) AS q3_hire_rate,
  ROUND(100.0 * SUM(CASE WHEN application_quarter=4 THEN hired_count END) / NULLIF(SUM(CASE WHEN application_quarter=4 THEN total_applications END), 0), 2) AS q4_hire_rate
FROM eng
GROUP BY role_category
ORDER BY role_category
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-066/attempt-01/sql/S23.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-066/attempt-01/sql/S23.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-066/attempt-01/results/S23.rows.jsonl)；完整：True；SHA256：`80c8dc3bf2834f9644c08a194d74377021f0ef5909183b5d6c794bf2821beab4`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "r", "kind": "base", "block": null, "base_tables": ["greenhouse__recruitment_performance"]}, {"alias": "j", "kind": "base", "block": null, "base_tables": ["greenhouse__job_enhanced"]}] | [{"type": "INNER", "right": "greenhouse__job_enhanced AS j", "on": "r.job_id = j.job_id", "using": []}] | [] |
| B2 | [{"alias": "eng", "kind": "derived", "block": "B1", "base_tables": ["greenhouse__job_enhanced", "greenhouse__recruitment_performance"]}] | [] | ["role_category"] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B2 | SUM(CASE WHEN application_quarter = 3 THEN total_applications END) | [{"table": "greenhouse__recruitment_performance", "column": "total_applications"}] | [{"table": "greenhouse__recruitment_performance", "column": "application_quarter"}] | False |
| B2 | SUM(CASE WHEN application_quarter = 4 THEN total_applications END) | [{"table": "greenhouse__recruitment_performance", "column": "total_applications"}] | [{"table": "greenhouse__recruitment_performance", "column": "application_quarter"}] | False |
| B2 | SUM(CASE WHEN application_quarter = 3 THEN total_interviews END) | [{"table": "greenhouse__recruitment_performance", "column": "total_interviews"}] | [{"table": "greenhouse__recruitment_performance", "column": "application_quarter"}] | False |
| B2 | SUM(CASE WHEN application_quarter = 4 THEN total_interviews END) | [{"table": "greenhouse__recruitment_performance", "column": "total_interviews"}] | [{"table": "greenhouse__recruitment_performance", "column": "application_quarter"}] | False |
| B2 | SUM(CASE WHEN application_quarter = 3 THEN total_interviews END) | [{"table": "greenhouse__recruitment_performance", "column": "total_interviews"}] | [{"table": "greenhouse__recruitment_performance", "column": "application_quarter"}] | False |
| B2 | SUM(CASE WHEN application_quarter = 3 THEN total_applications END) | [{"table": "greenhouse__recruitment_performance", "column": "total_applications"}] | [{"table": "greenhouse__recruitment_performance", "column": "application_quarter"}] | False |
| B2 | SUM(CASE WHEN application_quarter = 4 THEN total_interviews END) | [{"table": "greenhouse__recruitment_performance", "column": "total_interviews"}] | [{"table": "greenhouse__recruitment_performance", "column": "application_quarter"}] | False |
| B2 | SUM(CASE WHEN application_quarter = 4 THEN total_applications END) | [{"table": "greenhouse__recruitment_performance", "column": "total_applications"}] | [{"table": "greenhouse__recruitment_performance", "column": "application_quarter"}] | False |
| B2 | SUM(CASE WHEN application_quarter = 3 THEN hired_count END) | [{"table": "greenhouse__recruitment_performance", "column": "hired_count"}] | [{"table": "greenhouse__recruitment_performance", "column": "application_quarter"}] | False |
| B2 | SUM(CASE WHEN application_quarter = 3 THEN total_applications END) | [{"table": "greenhouse__recruitment_performance", "column": "total_applications"}] | [{"table": "greenhouse__recruitment_performance", "column": "application_quarter"}] | False |
| B2 | SUM(CASE WHEN application_quarter = 4 THEN hired_count END) | [{"table": "greenhouse__recruitment_performance", "column": "hired_count"}] | [{"table": "greenhouse__recruitment_performance", "column": "application_quarter"}] | False |
| B2 | SUM(CASE WHEN application_quarter = 4 THEN total_applications END) | [{"table": "greenhouse__recruitment_performance", "column": "total_applications"}] | [{"table": "greenhouse__recruitment_performance", "column": "application_quarter"}] | False |


## S24

类别 `data`；来源 `query_db`；调用 `750c539c321d43bcb6276fe6d8489811`；状态 `success`。

```sql
SELECT MIN(j.created_at) AS min_created, MAX(j.created_at) AS max_created,
       MIN(r.job_created_at) AS min_job_created, MAX(r.job_created_at) AS max_job_created
FROM greenhouse__job_enhanced j
JOIN greenhouse__recruitment_performance r ON r.job_id = j.job_id
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-066/attempt-01/sql/S24.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-066/attempt-01/sql/S24.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-066/attempt-01/results/S24.rows.jsonl)；完整：True；SHA256：`f69aa602fada2a2f670d3e3c9e91c1976b2f5355f0e2ea2585774d3d8cab8730`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "j", "kind": "base", "block": null, "base_tables": ["greenhouse__job_enhanced"]}, {"alias": "r", "kind": "base", "block": null, "base_tables": ["greenhouse__recruitment_performance"]}] | [{"type": "INNER", "right": "greenhouse__recruitment_performance AS r", "on": "r.job_id = j.job_id", "using": []}] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | MIN(j.created_at) | [{"table": "greenhouse__job_enhanced", "column": "created_at"}] | [] | False |
| B1 | MAX(j.created_at) | [{"table": "greenhouse__job_enhanced", "column": "created_at"}] | [] | False |
| B1 | MIN(r.job_created_at) | [{"table": "greenhouse__recruitment_performance", "column": "job_created_at"}] | [] | False |
| B1 | MAX(r.job_created_at) | [{"table": "greenhouse__recruitment_performance", "column": "job_created_at"}] | [] | False |


## S25

类别 `data`；来源 `query_db`；调用 `1d6c2ff693c64668a777641884416700`；状态 `success`。

```sql
SELECT j.application_to_interview_rate, j.overall_conversion_rate, j.count_total_applications, j.count_completed_interviews, j.departments
FROM greenhouse__job_enhanced j
WHERE j.departments='Engineering'
LIMIT 10
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-066/attempt-01/sql/S25.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-066/attempt-01/sql/S25.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-066/attempt-01/results/S25.rows.jsonl)；完整：True；SHA256：`4b87513cfb8ac0f2473087a428563d49905076eae6d31daaec6dc2eb9916924c`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "j", "kind": "base", "block": null, "base_tables": ["greenhouse__job_enhanced"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |


## S26

类别 `data`；来源 `query_db`；调用 `983acf21bf3e4fb49dbdcf42862f4e37`；状态 `success`。

```sql
SELECT j.created_year, j.created_month,
  COUNT(DISTINCT j.job_id) AS n_jobs,
  SUM(j.count_total_applications) AS apps,
  SUM(j.count_completed_interviews) AS interviews,
  ROUND(100.0*SUM(j.count_completed_interviews)/SUM(j.count_total_applications),2) AS weighted_interview_rate,
  ROUND(AVG(j.application_to_interview_rate),2) AS avg_job_rate
FROM greenhouse__job_enhanced j
WHERE j.departments='Engineering'
GROUP BY j.created_year, j.created_month
ORDER BY j.created_year, j.created_month
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-066/attempt-01/sql/S26.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-066/attempt-01/sql/S26.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-066/attempt-01/results/S26.rows.jsonl)；完整：True；SHA256：`f6c5d5cae50df7ea17f0ac1341be31baf68cfe38fa2988010b99dd6d3296dce3`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "j", "kind": "base", "block": null, "base_tables": ["greenhouse__job_enhanced"]}] | [] | ["j.created_year", "j.created_month"] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(DISTINCT j.job_id) | [{"table": "greenhouse__job_enhanced", "column": "job_id"}] | [] | False |
| B1 | SUM(j.count_total_applications) | [{"table": "greenhouse__job_enhanced", "column": "count_total_applications"}] | [] | False |
| B1 | SUM(j.count_completed_interviews) | [{"table": "greenhouse__job_enhanced", "column": "count_completed_interviews"}] | [] | False |
| B1 | AVG(j.application_to_interview_rate) | [{"table": "greenhouse__job_enhanced", "column": "application_to_interview_rate"}] | [] | False |
| B1 | SUM(j.count_total_applications) | [{"table": "greenhouse__job_enhanced", "column": "count_total_applications"}] | [] | False |
| B1 | SUM(j.count_completed_interviews) | [{"table": "greenhouse__job_enhanced", "column": "count_completed_interviews"}] | [] | False |


## S27

类别 `data`；来源 `query_db`；调用 `3f37db02ecbd49b799ba9d835a60c59b`；状态 `success`。

```sql
SELECT DISTINCT hiring_managers, recruiters FROM greenhouse__job_enhanced ORDER BY hiring_managers, recruiters
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-066/attempt-01/sql/S27.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-066/attempt-01/sql/S27.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-066/attempt-01/results/S27.rows.jsonl)；完整：True；SHA256：`6798c099ae1ba76bca59441127261b1c28f462f735b1aa224969e90dced39c3a`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "greenhouse__job_enhanced", "kind": "base", "block": null, "base_tables": ["greenhouse__job_enhanced"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |


## S28

类别 `data`；来源 `query_db`；调用 `5e98f57574514dc7b87bfe53f2810159`；状态 `success`。

```sql
SELECT hiring_managers, COUNT(*) AS n_jobs,
  SUM(count_total_applications) AS apps,
  SUM(count_completed_interviews) AS interviews,
  ROUND(100.0*SUM(count_completed_interviews)/SUM(count_total_applications),2) AS weighted_rate
FROM greenhouse__job_enhanced
WHERE departments='Engineering'
GROUP BY hiring_managers
ORDER BY weighted_rate
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-066/attempt-01/sql/S28.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-066/attempt-01/sql/S28.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-066/attempt-01/results/S28.rows.jsonl)；完整：True；SHA256：`7d5cac8ab8a918fc70b8bcc89cdc37b4ce0dfac3cf3d1f1f9aa2f199d5e9c85e`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "greenhouse__job_enhanced", "kind": "base", "block": null, "base_tables": ["greenhouse__job_enhanced"]}] | [] | ["hiring_managers"] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |
| B1 | SUM(count_total_applications) | [{"table": "greenhouse__job_enhanced", "column": "count_total_applications"}] | [] | False |
| B1 | SUM(count_completed_interviews) | [{"table": "greenhouse__job_enhanced", "column": "count_completed_interviews"}] | [] | False |
| B1 | SUM(count_total_applications) | [{"table": "greenhouse__job_enhanced", "column": "count_total_applications"}] | [] | False |
| B1 | SUM(count_completed_interviews) | [{"table": "greenhouse__job_enhanced", "column": "count_completed_interviews"}] | [] | False |


## S29

类别 `data`；来源 `query_db`；调用 `4d65e5000e354adc8629575d10d60679`；状态 `success`。

```sql
SELECT j.hiring_managers, r.application_quarter,
  SUM(r.total_applications) AS apps,
  SUM(r.total_interviews) AS interviews,
  ROUND(100.0*SUM(r.total_interviews)/SUM(r.total_applications),2) AS interview_rate,
  SUM(r.hired_count) AS hired,
  ROUND(100.0*SUM(r.hired_count)/SUM(r.total_applications),2) AS hire_rate
FROM greenhouse__recruitment_performance r
JOIN greenhouse__job_enhanced j ON r.job_id = j.job_id
WHERE j.departments='Engineering'
GROUP BY j.hiring_managers, r.application_quarter
ORDER BY j.hiring_managers, r.application_quarter
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-066/attempt-01/sql/S29.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-066/attempt-01/sql/S29.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-066/attempt-01/results/S29.rows.jsonl)；完整：True；SHA256：`251d449a5b87a58e9c3958880314a3001f56fc9e037bc72e39ef09179a453583`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "r", "kind": "base", "block": null, "base_tables": ["greenhouse__recruitment_performance"]}, {"alias": "j", "kind": "base", "block": null, "base_tables": ["greenhouse__job_enhanced"]}] | [{"type": "INNER", "right": "greenhouse__job_enhanced AS j", "on": "r.job_id = j.job_id", "using": []}] | ["j.hiring_managers", "r.application_quarter"] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | SUM(r.total_applications) | [{"table": "greenhouse__recruitment_performance", "column": "total_applications"}] | [] | False |
| B1 | SUM(r.total_interviews) | [{"table": "greenhouse__recruitment_performance", "column": "total_interviews"}] | [] | False |
| B1 | SUM(r.hired_count) | [{"table": "greenhouse__recruitment_performance", "column": "hired_count"}] | [] | False |
| B1 | SUM(r.total_applications) | [{"table": "greenhouse__recruitment_performance", "column": "total_applications"}] | [] | False |
| B1 | SUM(r.total_applications) | [{"table": "greenhouse__recruitment_performance", "column": "total_applications"}] | [] | False |
| B1 | SUM(r.total_interviews) | [{"table": "greenhouse__recruitment_performance", "column": "total_interviews"}] | [] | False |
| B1 | SUM(r.hired_count) | [{"table": "greenhouse__recruitment_performance", "column": "hired_count"}] | [] | False |


## S30

类别 `data`；来源 `query_db`；调用 `9090adaaf9a9436cae21a96c8cf6a9aa`；状态 `success`。

```sql
SELECT j.hiring_managers, 
  j.recruiters,
  (LENGTH(j.recruiters) - LENGTH(REPLACE(j.recruiters, ',', '')) + 1) AS n_recruiters,
  j.count_total_applications,
  j.count_completed_interviews,
  ROUND(100.0*j.count_completed_interviews/j.count_total_applications,2) AS interview_rate
FROM greenhouse__job_enhanced j
WHERE j.departments='Engineering' AND j.recruiters IS NOT NULL
LIMIT 20
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-066/attempt-01/sql/S30.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-066/attempt-01/sql/S30.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-066/attempt-01/results/S30.rows.jsonl)；完整：True；SHA256：`266e015b31949fe4e5d3905d5452c78c91903875e314f96dfd2b168666aaab49`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "j", "kind": "base", "block": null, "base_tables": ["greenhouse__job_enhanced"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |


## S31

类别 `data`；来源 `query_db`；调用 `6ceb407f505f41e9930a529809b93116`；状态 `success`。

```sql
-- Per-job factors for Engineering jobs
SELECT j.job_id, j.name, j.hiring_managers,
  (LENGTH(j.recruiters) - LENGTH(REPLACE(j.recruiters, ',', '')) + 1) AS n_interviewers,
  j.created_month,
  j.count_total_applications AS apps,
  j.count_total_interviews AS total_interviews,
  j.count_completed_interviews AS completed_interviews,
  j.avg_interviews_per_application,
  j.avg_job_rating,
  j.rating_completion_rate,
  j.application_to_interview_rate,
  j.interview_to_hire_rate,
  j.overall_conversion_rate
FROM greenhouse__job_enhanced j
WHERE j.departments='Engineering'
ORDER BY j.job_id
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-066/attempt-01/sql/S31.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-066/attempt-01/sql/S31.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-066/attempt-01/results/S31.rows.jsonl)；完整：True；SHA256：`daf9908f26c27bbb227f7d36a89568e39f0233139ff48680fc7f121bfa89cbd9`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "j", "kind": "base", "block": null, "base_tables": ["greenhouse__job_enhanced"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |


## S32

类别 `data`；来源 `python`；调用 `60d0fdf2e1334d32b080292126983f3b`；状态 `success`。

```sql

SELECT j.job_id, j.name, j.hiring_managers,
  (LENGTH(j.recruiters) - LENGTH(REPLACE(j.recruiters, ',', '')) + 1) AS n_interviewers,
  j.created_month,
  j.count_total_applications AS apps,
  j.count_total_interviews AS total_interviews,
  j.count_completed_interviews AS completed_interviews,
  j.avg_interviews_per_application,
  j.avg_job_rating,
  j.rating_completion_rate,
  j.application_to_interview_rate AS app_to_int_rate,
  j.interview_to_hire_rate,
  j.overall_conversion_rate
FROM greenhouse__job_enhanced j
WHERE j.departments='Engineering'

```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-066/attempt-01/sql/S32.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-066/attempt-01/sql/S32.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-066/attempt-01/results/S32.rows.jsonl)；完整：True；SHA256：`daf9908f26c27bbb227f7d36a89568e39f0233139ff48680fc7f121bfa89cbd9`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "j", "kind": "base", "block": null, "base_tables": ["greenhouse__job_enhanced"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |


## S33

类别 `data`；来源 `python`；调用 `f0c3a215dfd340aab5dc7d23371996c6`；状态 `success`。

```sql

SELECT j.job_id, j.name, j.hiring_managers,
  (LENGTH(j.recruiters) - LENGTH(REPLACE(j.recruiters, ',', '')) + 1) AS n_interviewers,
  j.created_month,
  j.count_total_applications AS apps,
  j.count_total_interviews AS total_interviews,
  j.avg_job_rating,
  j.rating_completion_rate,
  j.application_to_interview_rate AS app_to_int_rate,
  j.interview_to_hire_rate,
  j.overall_conversion_rate
FROM greenhouse__job_enhanced j
WHERE j.departments='Engineering'

```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-066/attempt-01/sql/S33.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-066/attempt-01/sql/S33.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-066/attempt-01/results/S33.rows.jsonl)；完整：True；SHA256：`09ccd15090d337c246da72dd0c5038d17af47c13588eb41e6a236ae858936212`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "j", "kind": "base", "block": null, "base_tables": ["greenhouse__job_enhanced"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |


## S34

类别 `data`；来源 `python`；调用 `4c1e4cc748f547c28d7d32882b1edb3b`；状态 `success`。

```sql

WITH eng AS (
  SELECT r.*,
    CASE
      WHEN j.name LIKE 'Frontend%' THEN 'Frontend'
      WHEN j.name LIKE 'Backend%' THEN 'Backend'
      WHEN j.name LIKE 'Full Stack%' THEN 'Full Stack'
      WHEN j.name LIKE 'Data Engineer%' THEN 'Data Engineer'
      WHEN j.name LIKE 'DevOps%' THEN 'DevOps'
      WHEN j.name LIKE 'Mobile%' THEN 'Mobile'
      WHEN j.name LIKE 'QA%' THEN 'QA'
      WHEN j.name LIKE 'Machine Learning%' THEN 'Machine Learning'
      ELSE 'Other'
    END AS role_category
  FROM greenhouse__recruitment_performance r
  JOIN greenhouse__job_enhanced j ON r.job_id = j.job_id
  WHERE j.departments='Engineering'
)
SELECT role_category, application_quarter,
  SUM(total_applications) AS apps,
  SUM(total_interviews) AS interviews,
  100.0*SUM(total_interviews)/SUM(total_applications) AS interview_rate
FROM eng
GROUP BY role_category, application_quarter
ORDER BY role_category, application_quarter

```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-066/attempt-01/sql/S34.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-066/attempt-01/sql/S34.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-066/attempt-01/results/S34.rows.jsonl)；完整：True；SHA256：`f6b5017b887ddc30f17fbcb79c77a1b4e6a9836a03685ca5a85064a459170d72`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "r", "kind": "base", "block": null, "base_tables": ["greenhouse__recruitment_performance"]}, {"alias": "j", "kind": "base", "block": null, "base_tables": ["greenhouse__job_enhanced"]}] | [{"type": "INNER", "right": "greenhouse__job_enhanced AS j", "on": "r.job_id = j.job_id", "using": []}] | [] |
| B2 | [{"alias": "eng", "kind": "derived", "block": "B1", "base_tables": ["greenhouse__job_enhanced", "greenhouse__recruitment_performance"]}] | [] | ["role_category", "application_quarter"] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B2 | SUM(total_applications) | [{"table": "greenhouse__recruitment_performance", "column": "total_applications"}] | [] | False |
| B2 | SUM(total_interviews) | [{"table": "greenhouse__recruitment_performance", "column": "total_interviews"}] | [] | False |
| B2 | SUM(total_applications) | [{"table": "greenhouse__recruitment_performance", "column": "total_applications"}] | [] | False |
| B2 | SUM(total_interviews) | [{"table": "greenhouse__recruitment_performance", "column": "total_interviews"}] | [] | False |


## S35

类别 `data`；来源 `python`；调用 `4c1e4cc748f547c28d7d32882b1edb3b`；状态 `success`。

```sql

SELECT j.hiring_managers, r.application_quarter,
  SUM(r.total_applications) AS apps,
  SUM(r.total_interviews) AS interviews,
  100.0*SUM(r.total_interviews)/SUM(r.total_applications) AS interview_rate,
  SUM(r.hired_count) AS hired,
  100.0*SUM(r.hired_count)/SUM(r.total_applications) AS hire_rate
FROM greenhouse__recruitment_performance r
JOIN greenhouse__job_enhanced j ON r.job_id = j.job_id
WHERE j.departments='Engineering'
GROUP BY j.hiring_managers, r.application_quarter
ORDER BY j.hiring_managers, r.application_quarter

```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-066/attempt-01/sql/S35.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-066/attempt-01/sql/S35.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-066/attempt-01/results/S35.rows.jsonl)；完整：True；SHA256：`914b2c614994b575b27a32646d53e477a25129f43daed2b4bdb9b34c2991e34c`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "r", "kind": "base", "block": null, "base_tables": ["greenhouse__recruitment_performance"]}, {"alias": "j", "kind": "base", "block": null, "base_tables": ["greenhouse__job_enhanced"]}] | [{"type": "INNER", "right": "greenhouse__job_enhanced AS j", "on": "r.job_id = j.job_id", "using": []}] | ["j.hiring_managers", "r.application_quarter"] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | SUM(r.total_applications) | [{"table": "greenhouse__recruitment_performance", "column": "total_applications"}] | [] | False |
| B1 | SUM(r.total_interviews) | [{"table": "greenhouse__recruitment_performance", "column": "total_interviews"}] | [] | False |
| B1 | SUM(r.hired_count) | [{"table": "greenhouse__recruitment_performance", "column": "hired_count"}] | [] | False |
| B1 | SUM(r.total_applications) | [{"table": "greenhouse__recruitment_performance", "column": "total_applications"}] | [] | False |
| B1 | SUM(r.total_applications) | [{"table": "greenhouse__recruitment_performance", "column": "total_applications"}] | [] | False |
| B1 | SUM(r.total_interviews) | [{"table": "greenhouse__recruitment_performance", "column": "total_interviews"}] | [] | False |
| B1 | SUM(r.hired_count) | [{"table": "greenhouse__recruitment_performance", "column": "hired_count"}] | [] | False |


## S36

类别 `data`；来源 `python`；调用 `4c1e4cc748f547c28d7d32882b1edb3b`；状态 `success`。

```sql

SELECT j.created_month,
  COUNT(DISTINCT j.job_id) AS n_jobs,
  SUM(j.count_total_applications) AS apps,
  SUM(j.count_completed_interviews) AS interviews,
  100.0*SUM(j.count_completed_interviews)/SUM(j.count_total_applications) AS interview_rate
FROM greenhouse__job_enhanced j
WHERE j.departments='Engineering'
GROUP BY j.created_month
ORDER BY j.created_month

```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-066/attempt-01/sql/S36.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-066/attempt-01/sql/S36.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-066/attempt-01/results/S36.rows.jsonl)；完整：True；SHA256：`733206ae3015b6fdbf741332e634866c58d2b76ef8dca89c5df2081a584b2e34`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "j", "kind": "base", "block": null, "base_tables": ["greenhouse__job_enhanced"]}] | [] | ["j.created_month"] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(DISTINCT j.job_id) | [{"table": "greenhouse__job_enhanced", "column": "job_id"}] | [] | False |
| B1 | SUM(j.count_total_applications) | [{"table": "greenhouse__job_enhanced", "column": "count_total_applications"}] | [] | False |
| B1 | SUM(j.count_completed_interviews) | [{"table": "greenhouse__job_enhanced", "column": "count_completed_interviews"}] | [] | False |
| B1 | SUM(j.count_total_applications) | [{"table": "greenhouse__job_enhanced", "column": "count_total_applications"}] | [] | False |
| B1 | SUM(j.count_completed_interviews) | [{"table": "greenhouse__job_enhanced", "column": "count_completed_interviews"}] | [] | False |


## S37

类别 `data`；来源 `query_db`；调用 `2113f4f71ed14e72b28fc2d62064ee01`；状态 `success`。

```sql
SELECT hiring_managers,
  MIN(created_month) AS first_month,
  MAX(created_month) AS last_month,
  COUNT(DISTINCT created_month) AS months_active,
  COUNT(DISTINCT name) AS distinct_job_titles,
  COUNT(*) AS n_jobs,
  SUM(count_total_applications) AS total_apps
FROM greenhouse__job_enhanced
WHERE departments='Engineering'
GROUP BY hiring_managers
ORDER BY hiring_managers
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-066/attempt-01/sql/S37.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-066/attempt-01/sql/S37.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-066/attempt-01/results/S37.rows.jsonl)；完整：True；SHA256：`0e0f2fd535da3e7acfc29fe381b291c2162a07aeeb85188bd8711001b2bed8e3`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "greenhouse__job_enhanced", "kind": "base", "block": null, "base_tables": ["greenhouse__job_enhanced"]}] | [] | ["hiring_managers"] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | MIN(created_month) | [{"table": "greenhouse__job_enhanced", "column": "created_month"}] | [] | False |
| B1 | MAX(created_month) | [{"table": "greenhouse__job_enhanced", "column": "created_month"}] | [] | False |
| B1 | COUNT(DISTINCT created_month) | [{"table": "greenhouse__job_enhanced", "column": "created_month"}] | [] | False |
| B1 | COUNT(DISTINCT name) | [{"table": "greenhouse__job_enhanced", "column": "name"}] | [] | False |
| B1 | COUNT(*) | [] | [] | True |
| B1 | SUM(count_total_applications) | [{"table": "greenhouse__job_enhanced", "column": "count_total_applications"}] | [] | False |


## S38

类别 `data`；来源 `query_db`；调用 `cd1beb962692487592b050d044f8696d`；状态 `success`。

```sql
-- Does number of interviewers vary systematically by hiring manager?
SELECT j.hiring_managers,
  (LENGTH(j.recruiters) - LENGTH(REPLACE(j.recruiters, ',', '')) + 1) AS n_interviewers,
  COUNT(*) AS n_jobs,
  ROUND(AVG(j.application_to_interview_rate),2) AS avg_rate
FROM greenhouse__job_enhanced j
WHERE j.departments='Engineering'
GROUP BY j.hiring_managers, n_interviewers
ORDER BY j.hiring_managers, n_interviewers
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-066/attempt-01/sql/S38.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-066/attempt-01/sql/S38.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-066/attempt-01/results/S38.rows.jsonl)；完整：True；SHA256：`60272ee1e42a2dab8d7d1cd3295c0bd1cb9a463c73a96b631db1f8b097eddebd`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "j", "kind": "base", "block": null, "base_tables": ["greenhouse__job_enhanced"]}] | [] | ["j.hiring_managers", "(LENGTH(j.recruiters) - LENGTH(REPLACE(j.recruiters, ',', '')) + 1)"] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |
| B1 | AVG(j.application_to_interview_rate) | [{"table": "greenhouse__job_enhanced", "column": "application_to_interview_rate"}] | [] | False |


## S39

类别 `data`；来源 `python`；调用 `be4e4a07b493413381aee7202227509c`；状态 `success`。

```sql

SELECT r.application_quarter,
  SUM(r.total_applications) AS apps,
  SUM(r.total_interviews) AS interviews,
  100.0*SUM(r.total_interviews)/SUM(r.total_applications) AS interview_rate
FROM greenhouse__recruitment_performance r
JOIN greenhouse__job_enhanced j ON r.job_id = j.job_id
WHERE j.departments='Marketing'
GROUP BY r.application_quarter

```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-066/attempt-01/sql/S39.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-066/attempt-01/sql/S39.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-066/attempt-01/results/S39.rows.jsonl)；完整：True；SHA256：`623413515f86cdb8f6c8be069e2f4431611864739a96bf93bec976e568f96bb7`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "r", "kind": "base", "block": null, "base_tables": ["greenhouse__recruitment_performance"]}, {"alias": "j", "kind": "base", "block": null, "base_tables": ["greenhouse__job_enhanced"]}] | [{"type": "INNER", "right": "greenhouse__job_enhanced AS j", "on": "r.job_id = j.job_id", "using": []}] | ["r.application_quarter"] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | SUM(r.total_applications) | [{"table": "greenhouse__recruitment_performance", "column": "total_applications"}] | [] | False |
| B1 | SUM(r.total_interviews) | [{"table": "greenhouse__recruitment_performance", "column": "total_interviews"}] | [] | False |
| B1 | SUM(r.total_applications) | [{"table": "greenhouse__recruitment_performance", "column": "total_applications"}] | [] | False |
| B1 | SUM(r.total_interviews) | [{"table": "greenhouse__recruitment_performance", "column": "total_interviews"}] | [] | False |


## S40

类别 `data`；来源 `python`；调用 `be4e4a07b493413381aee7202227509c`；状态 `success`。

```sql

SELECT 
  CASE 
    WHEN j.name LIKE 'Content Marketing%' THEN 'Content Marketing'
    WHEN j.name LIKE 'Digital Marketing%' THEN 'Digital Marketing'
    WHEN j.name LIKE 'Growth Marketing%' THEN 'Growth Marketing'
    WHEN j.name LIKE 'Marketing Analyst%' THEN 'Marketing Analyst'
    ELSE 'Other'
  END AS role,
  r.application_quarter,
  SUM(r.total_applications) AS apps,
  SUM(r.total_interviews) AS interviews,
  100.0*SUM(r.total_interviews)/SUM(r.total_applications) AS interview_rate
FROM greenhouse__recruitment_performance r
JOIN greenhouse__job_enhanced j ON r.job_id = j.job_id
WHERE j.departments='Marketing'
GROUP BY role, r.application_quarter
ORDER BY role, r.application_quarter

```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-066/attempt-01/sql/S40.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-066/attempt-01/sql/S40.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-066/attempt-01/results/S40.rows.jsonl)；完整：True；SHA256：`b6b37189d20eeaa58d066d1bbde8c4da380562ddcb5336c9921dc9a85d5d2bdb`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "r", "kind": "base", "block": null, "base_tables": ["greenhouse__recruitment_performance"]}, {"alias": "j", "kind": "base", "block": null, "base_tables": ["greenhouse__job_enhanced"]}] | [{"type": "INNER", "right": "greenhouse__job_enhanced AS j", "on": "r.job_id = j.job_id", "using": []}] | ["CASE WHEN j.name LIKE 'Content Marketing%' THEN 'Content Marketing' WHEN j.name LIKE 'Digital Marketing%' THEN 'Digital Marketing' WHEN j.name LIKE 'Growth Marketing%' THEN 'Growth Marketing' WHEN j.name LIKE 'Marketing Analyst%' THEN 'Marketing Analyst' ELSE 'Other' END", "r.application_quarter"] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | SUM(r.total_applications) | [{"table": "greenhouse__recruitment_performance", "column": "total_applications"}] | [] | False |
| B1 | SUM(r.total_interviews) | [{"table": "greenhouse__recruitment_performance", "column": "total_interviews"}] | [] | False |
| B1 | SUM(r.total_applications) | [{"table": "greenhouse__recruitment_performance", "column": "total_applications"}] | [] | False |
| B1 | SUM(r.total_interviews) | [{"table": "greenhouse__recruitment_performance", "column": "total_interviews"}] | [] | False |


## S41

类别 `data`；来源 `python`；调用 `be4e4a07b493413381aee7202227509c`；状态 `success`。

```sql

SELECT j.hiring_managers, r.application_quarter,
  SUM(r.total_applications) AS apps,
  SUM(r.total_interviews) AS interviews,
  100.0*SUM(r.total_interviews)/SUM(r.total_applications) AS interview_rate
FROM greenhouse__recruitment_performance r
JOIN greenhouse__job_enhanced j ON r.job_id = j.job_id
WHERE j.departments='Marketing'
GROUP BY j.hiring_managers, r.application_quarter
ORDER BY j.hiring_managers, r.application_quarter

```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-066/attempt-01/sql/S41.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-066/attempt-01/sql/S41.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-066/attempt-01/results/S41.rows.jsonl)；完整：True；SHA256：`4f779a0381820cae3b60cc49878406aa3703f6e6426b565b7297f81029e4c7da`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "r", "kind": "base", "block": null, "base_tables": ["greenhouse__recruitment_performance"]}, {"alias": "j", "kind": "base", "block": null, "base_tables": ["greenhouse__job_enhanced"]}] | [{"type": "INNER", "right": "greenhouse__job_enhanced AS j", "on": "r.job_id = j.job_id", "using": []}] | ["j.hiring_managers", "r.application_quarter"] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | SUM(r.total_applications) | [{"table": "greenhouse__recruitment_performance", "column": "total_applications"}] | [] | False |
| B1 | SUM(r.total_interviews) | [{"table": "greenhouse__recruitment_performance", "column": "total_interviews"}] | [] | False |
| B1 | SUM(r.total_applications) | [{"table": "greenhouse__recruitment_performance", "column": "total_applications"}] | [] | False |
| B1 | SUM(r.total_interviews) | [{"table": "greenhouse__recruitment_performance", "column": "total_interviews"}] | [] | False |


## S42

类别 `data`；来源 `python`；调用 `be4e4a07b493413381aee7202227509c`；状态 `success`。

```sql

SELECT j.hiring_managers, j.departments,
  COUNT(DISTINCT j.name) AS distinct_roles,
  COUNT(DISTINCT j.created_month) AS months_active,
  COUNT(*) AS n_jobs,
  SUM(j.count_total_applications) AS apps,
  ROUND(AVG(j.application_to_interview_rate),2) AS avg_rate
FROM greenhouse__job_enhanced j
WHERE j.departments='Engineering'
GROUP BY j.hiring_managers
ORDER BY avg_rate

```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-066/attempt-01/sql/S42.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-066/attempt-01/sql/S42.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-066/attempt-01/results/S42.rows.jsonl)；完整：True；SHA256：`c28376b3bf31b5b5b7e4d43ddbce685357a26739c148f45e4ede849b56033ddb`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "j", "kind": "base", "block": null, "base_tables": ["greenhouse__job_enhanced"]}] | [] | ["j.hiring_managers"] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(DISTINCT j.name) | [{"table": "greenhouse__job_enhanced", "column": "name"}] | [] | False |
| B1 | COUNT(DISTINCT j.created_month) | [{"table": "greenhouse__job_enhanced", "column": "created_month"}] | [] | False |
| B1 | COUNT(*) | [] | [] | True |
| B1 | SUM(j.count_total_applications) | [{"table": "greenhouse__job_enhanced", "column": "count_total_applications"}] | [] | False |
| B1 | AVG(j.application_to_interview_rate) | [{"table": "greenhouse__job_enhanced", "column": "application_to_interview_rate"}] | [] | False |


## S43

类别 `data`；来源 `python`；调用 `2ab2197ac6ca4934b12579f5cdb46226`；状态 `success`。

```sql

SELECT j.job_id, j.name, j.hiring_managers,
  (LENGTH(j.recruiters) - LENGTH(REPLACE(j.recruiters, ',', '')) + 1) AS n_interviewers,
  j.created_month,
  j.count_total_applications AS apps,
  j.avg_job_rating,
  j.application_to_interview_rate AS app_to_int_rate,
  j.overall_conversion_rate
FROM greenhouse__job_enhanced j
WHERE j.departments='Engineering'

```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-066/attempt-01/sql/S43.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-066/attempt-01/sql/S43.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-066/attempt-01/results/S43.rows.jsonl)；完整：True；SHA256：`52361fe17305cacf5328da11d1e33a3f639938ebb16c98ad645234fb5a24ebfa`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "j", "kind": "base", "block": null, "base_tables": ["greenhouse__job_enhanced"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |


## S44

类别 `data`；来源 `python`；调用 `043ba7f86be5415c897741b4bd73801e`；状态 `success`。

```sql

SELECT j.job_id, j.name, j.hiring_managers,
  (LENGTH(j.recruiters) - LENGTH(REPLACE(j.recruiters, ',', '')) + 1) AS n_interviewers,
  j.created_month,
  j.count_total_applications AS apps,
  j.avg_job_rating,
  j.application_to_interview_rate AS app_to_int_rate,
  j.overall_conversion_rate
FROM greenhouse__job_enhanced j
WHERE j.departments='Engineering'

```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-066/attempt-01/sql/S44.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-066/attempt-01/sql/S44.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-066/attempt-01/results/S44.rows.jsonl)；完整：True；SHA256：`52361fe17305cacf5328da11d1e33a3f639938ebb16c98ad645234fb5a24ebfa`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "j", "kind": "base", "block": null, "base_tables": ["greenhouse__job_enhanced"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |

