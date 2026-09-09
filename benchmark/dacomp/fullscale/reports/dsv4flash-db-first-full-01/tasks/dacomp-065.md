# dacomp-065

Our CEO claims that candidates from well-known tech companies (e.g., FAANG, unicorns) perf…

运行：已提交。官方未评分。全部 SQL 尝试/成功 62/60；数据 SQL 60/58；Python 5 次。

完整原题：

Our CEO claims that candidates from well-known tech companies (e.g., FAANG, unicorns) perform better in technical interviews, but the HR department is concerned about potential unconscious bias in our interview process. Please analyze our recruitment data to assess the impact of factors such as a candidate's company background, education level, and technical skills on their interview performance and final hiring outcome. Concurrently, detect any potential patterns of bias in the interview process. Specifically, you need to analyze: 1) whether there is a significant difference in the actual technical interview performance of candidates from different company backgrounds; 2) whether the impact of company background persists after controlling for educational background and work experience; and 3) identify and quantify any potential systemic biases in the interview process.

| 表 | 行数 | 列数 |
| --- | --- | --- |
| greenhouse__application_enhanced | 18186 | 99 |
| greenhouse__interview_enhanced | 14625 | 62 |


实际路线（分析者依据 SQL/源码概括，不代表 Agent 自述）：SQL 比较公司背景、教育与面试表现 → Python 控制变量回归、检验和录用率分组 → 招聘偏差分析。

数据库大小：25,169,920 字节。

## 数据 SQL

| SQL | 状态 | 基础表 | Join 输入/类型 | GROUP BY | 聚合表达式 | 结果行数 | 数据库 ms |
| --- | --- | --- | --- | --- | --- | --- | --- |
| [S3/Q1](#s3) | success | ["greenhouse__application_enhanced"] | 0 / {} | [] | ["COUNT(*)"] | 1 | 5.932 |
| [S4/Q2](#s4) | success | ["greenhouse__interview_enhanced"] | 0 / {} | [] | ["COUNT(*)"] | 1 | 2.998 |
| [S5/Q3](#s5) | success | ["greenhouse__application_enhanced"] | 0 / {} | ["candidate_company"] | ["COUNT(*)"] | 30 | 12.331 |
| [S6/Q4](#s6) | success | ["greenhouse__application_enhanced"] | 0 / {} | ["education_level"] | ["COUNT(*)"] | 5 | 12.361 |
| [S7/Q5](#s7) | success | ["greenhouse__application_enhanced"] | 0 / {} | ["university_tier"] | ["COUNT(*)"] | 5 | 12.454 |
| [S8/Q6](#s8) | success | ["greenhouse__application_enhanced"] | 0 / {} | ["status"] | ["COUNT(*)"] | 4 | 10.888 |
| [S9/Q7](#s9) | success | ["greenhouse__application_enhanced"] | 0 / {} | ["candidate_company"] | ["COUNT(*)"] | 85 | 12.053 |
| [S10/Q8](#s10) | success | ["greenhouse__interview_enhanced"] | 0 / {} | ["overall_recommendation"] | ["COUNT(*)"] | 5 | 7.787 |
| [S11/Q9](#s11) | success | ["greenhouse__interview_enhanced"] | 0 / {} | ["job_stage"] | ["COUNT(*)"] | 6 | 7.943 |
| [S12/Q10](#s12) | success | ["greenhouse__application_enhanced"] | 0 / {} | ["current_company"] | ["COUNT(*)"] | 20 | 12.498 |
| [S13/Q11](#s13) | success | ["greenhouse__interview_enhanced"] | 0 / {} | [] | ["MIN(technical_score)", "MAX(technical_score)", "AVG(technical_score)", "MIN(problem_solving_score)", "MAX(problem_solving_score)", "AVG(problem_solving_score)", "MIN(communication_score)", "MAX(communication_score)", "AVG(communication_score)", "MIN(culture_fit_score)", "MAX(culture_fit_score)", "AVG(culture_fit_score)", "MIN(leadership_score)", "MAX(leadership_score)", "AVG(leadership_score)"] | 1 | 10.933 |
| [S14/Q12](#s14) | success | ["greenhouse__application_enhanced"] | 0 / {} | ["years_of_experience"] | ["COUNT(*)"] | 15 | 10.999 |
| [S15/Q13](#s15) | success | ["greenhouse__application_enhanced"] | 0 / {} | [] | [] | 85 | 11.578 |
| [S16/Q14](#s16) | success | ["greenhouse__application_enhanced"] | 0 / {} | ["stage_hired"] | ["COUNT(*)"] | 2 | 10.437 |
| [S17/Q15](#s17) | success | ["greenhouse__application_enhanced"] | 0 / {} | ["stage_technical_interview"] | ["COUNT(*)"] | 2 | 10.347 |
| [S18/Q16](#s18) | failed | ["greenhouse__interview_enhanced"] | 0 / {} | ["candidate_company"] | ["COUNT(*)", "AVG(technical_score)", "AVG(problem_solving_score)", "AVG(communication_score)", "AVG(overall_recommendation IN ('strong_yes', 'yes'))"] | unknown | 未取得；调用总时长 0.18 ms |
| [S19/Q17](#s19) | success | ["greenhouse__interview_enhanced"] | 0 / {} | ["application_id"] | ["COUNT(*)"] | 10 | 7.37 |
| [S20/Q18](#s20) | success | ["greenhouse__application_enhanced", "greenhouse__interview_enhanced"] | 2 / {'INNER': 1} | ["i.technical_score", "a.candidate_company"] | ["COUNT(*)"] | 30 | 44.952 |
| [S21/Q19](#s21) | success | ["greenhouse__application_enhanced", "greenhouse__interview_enhanced"] | 2 / {'LEFT': 1} | [] | ["SUM(CASE WHEN i.technical_score IS NULL THEN 1 ELSE 0 END)", "SUM(CASE WHEN i.problem_solving_score IS NULL THEN 1 ELSE 0 END)", "SUM(CASE WHEN i.communication_score IS NULL THEN 1 ELSE 0 END)", "SUM(CASE WHEN i.overall_recommendation IS NULL THEN 1 ELSE 0 END)", "SUM(CASE WHEN a.education_level IS NULL THEN 1 ELSE 0 END)", "SUM(CASE WHEN a.years_of_experience IS NULL THEN 1 ELSE 0 END)", "SUM(CASE WHEN a.university_tier IS NULL THEN 1 ELSE 0 END)"] | 1 | 86.494 |
| [S22/Q20](#s22) | success | ["greenhouse__application_enhanced"] | 0 / {} | ["candidate_gender"] | ["COUNT(*)"] | 5 | 12.701 |
| [S23/Q21](#s23) | success | ["greenhouse__application_enhanced"] | 0 / {} | ["candidate_race"] | ["COUNT(*)"] | 7 | 13.043 |
| [S24/Q22](#s24) | success | ["greenhouse__interview_enhanced"] | 0 / {} | ["interviewer_gender"] | ["COUNT(*)"] | 3 | 7.842 |
| [S25/Q23](#s25) | success | ["greenhouse__application_enhanced", "greenhouse__interview_enhanced"] | 2 / {'INNER': 1} | ["cat.company_cat"] | ["COUNT(DISTINCT cat.application_id)", "COUNT(*)", "AVG(i.technical_score)", "AVG(i.problem_solving_score)", "AVG(i.communication_score)", "AVG(CASE WHEN i.overall_recommendation IN ('strong_yes', 'yes') THEN 1.0 ELSE 0 END)"] | 3 | 62.407 |
| [S26/Q24](#s26) | success | ["greenhouse__application_enhanced"] | 0 / {} | ["cat.company_cat"] | ["COUNT(*)"] | 3 | 17.804 |
| [S27/Q25](#s27) | success | ["greenhouse__application_enhanced", "greenhouse__interview_enhanced"] | 2 / {'INNER': 1} | ["i.application_id", "company_cat"] | ["AVG(i.technical_score)", "AVG(i.problem_solving_score)", "AVG(i.communication_score)", "AVG(i.culture_fit_score)", "AVG(i.leadership_score)", "MAX(CASE WHEN i.overall_recommendation IN ('strong_yes', 'yes') THEN 1 ELSE 0 END)", "COUNT(*)", "COUNT(*)", "AVG(avg_tech)", "AVG(avg_ps)", "AVG(avg_comm)", "AVG(avg_cf)", "AVG(avg_lead)", "AVG(ever_pos_rec)"] | 3 | 56.591 |
| [S28/Q26](#s28) | success | ["greenhouse__interview_enhanced"] | 0 / {} | ["job_stage"] | ["COUNT(*)", "AVG(technical_score)", "AVG(problem_solving_score)", "AVG(communication_score)", "AVG(leadership_score)"] | 6 | 12.166 |
| [S29/Q27](#s29) | success | ["greenhouse__application_enhanced"] | 0 / {} | ["a.candidate_company", "a.stage_offer", "a.stage_hired"] | ["COUNT(*)"] | 30 | 11.609 |
| [S30/Q28](#s30) | success | ["greenhouse__application_enhanced", "greenhouse__interview_enhanced"] | 2 / {'INNER': 1} | ["i.application_id"] | ["AVG(i.technical_score)", "AVG(i.problem_solving_score)", "AVG(i.communication_score)", "AVG(i.culture_fit_score)", "AVG(i.leadership_score)", "MAX(CASE WHEN i.overall_recommendation IN ('strong_yes', 'yes') THEN 1.0 ELSE 0.0 END)", "COUNT(*)"] | 4744 | 62.739 |
| [S31/Q29](#s31) | success | ["greenhouse__application_enhanced", "greenhouse__interview_enhanced"] | 2 / {'INNER': 1} | ["i.application_id"] | ["AVG(i.technical_score)", "AVG(i.problem_solving_score)", "AVG(i.communication_score)", "AVG(i.culture_fit_score)", "AVG(i.leadership_score)", "MAX(CASE WHEN i.overall_recommendation IN ('strong_yes', 'yes') THEN 1.0 ELSE 0.0 END)", "COUNT(*)"] | 4744 | 131.558 |
| [S32/Q30](#s32) | success | ["greenhouse__application_enhanced", "greenhouse__interview_enhanced"] | 2 / {'INNER': 1} | [] | [] | 32565 | 207.935 |
| [S33/Q31](#s33) | success | ["greenhouse__interview_enhanced"] | 0 / {} | [] | ["COUNT(*)", "COUNT(DISTINCT interview_id)", "COUNT(DISTINCT application_id \|\| '_' \|\| interview_id)"] | 1 | 17.635 |
| [S34/Q32](#s34) | success | ["greenhouse__interview_enhanced"] | 0 / {} | ["interview_id"] | ["COUNT(*)"] | 10 | 8.464 |
| [S35/Q33](#s35) | success | ["greenhouse__interview_enhanced"] | 0 / {} | ["application_id", "interview_id", "interviewer_user_id"] | ["COUNT(*)"] | 10 | 11.551 |
| [S36/Q34](#s36) | success | ["greenhouse__interview_enhanced"] | 0 / {} | ["application_id", "interview_id", "interviewer_user_id", "scorecard_id"] | ["COUNT(*)"] | 10 | 12.372 |
| [S37/Q35](#s37) | success | ["greenhouse__interview_enhanced"] | 0 / {} | [] | ["COUNT(*)", "COUNT(DISTINCT interview_scorecard_key)"] | 1 | 13.488 |
| [S38/Q36](#s38) | success | ["greenhouse__interview_enhanced"] | 0 / {} | ["interview_scorecard_key"] | ["COUNT(*)"] | 10 | 12.254 |
| [S39/Q37](#s39) | success | ["greenhouse__interview_enhanced"] | 0 / {} | [] | ["COUNT(*)"] | 1 | 75.232 |
| [S40/Q38](#s40) | success | ["greenhouse__interview_enhanced"] | 0 / {} | [] | ["COUNT(*)"] | 1 | 29.716 |
| [S41/Q39](#s41) | success | ["greenhouse__application_enhanced", "greenhouse__interview_enhanced"] | 2 / {'INNER': 1} | ["i.application_id"] | ["AVG(i.technical_score)", "AVG(i.problem_solving_score)", "AVG(i.communication_score)", "AVG(i.culture_fit_score)", "AVG(i.leadership_score)", "MAX(CASE WHEN i.overall_recommendation IN ('strong_yes', 'yes') THEN 1.0 ELSE 0.0 END)", "COUNT(*)"] | 4744 | 60.357 |
| [S42/Q40](#s42) | success | ["greenhouse__application_enhanced", "greenhouse__interview_enhanced"] | 2 / {'INNER': 1} | ["i.application_id"] | ["AVG(i.technical_score)", "AVG(i.problem_solving_score)", "AVG(i.communication_score)", "AVG(i.culture_fit_score)", "AVG(i.leadership_score)", "MAX(CASE WHEN i.overall_recommendation IN ('strong_yes', 'yes') THEN 1.0 ELSE 0.0 END)", "COUNT(*)"] | 4744 | 131.493 |
| [S43/Q41](#s43) | success | ["greenhouse__application_enhanced"] | 2 / {'INNER': 1} | ["cat.company_cat"] | ["COUNT(*)", "SUM(a.stage_offer)", "SUM(a.stage_hired)", "AVG(CAST(a.stage_offer AS REAL))", "AVG(CAST(a.stage_hired AS REAL))"] | 3 | 39.399 |
| [S44/Q42](#s44) | success | ["greenhouse__application_enhanced"] | 0 / {} | ["stage_technical_interview"] | ["COUNT(*)"] | 2 | 10.721 |
| [S45/Q43](#s45) | success | ["greenhouse__application_enhanced"] | 2 / {'INNER': 1} | ["cat.company_cat"] | ["COUNT(*)", "SUM(a.stage_offer)", "SUM(a.stage_hired)", "AVG(CAST(a.stage_offer AS REAL))", "AVG(CAST(a.stage_hired AS REAL))"] | 3 | 40.226 |
| [S46/Q44](#s46) | failed | ["greenSchouse__application_enhanced"] | 0 / {} | ["stage_technical_interview"] | ["COUNT(*)"] | unknown | 未取得；调用总时长 0.231 ms |
| [S47/Q45](#s47) | success | ["greenhouse__application_enhanced"] | 0 / {} | [] | ["COUNT(*)"] | 1 | 8.228 |
| [S48/Q46](#s48) | success | ["greenhouse__application_enhanced"] | 0 / {} | [] | [] | 2 | 8.486 |
| [S49/Q47](#s49) | success | ["greenhouse__application_enhanced"] | 0 / {} | [] | ["COUNT(*)", "COUNT(DISTINCT application_id)"] | 1 | 11.603 |
| [S50/Q48](#s50) | success | ["greenhouse__application_enhanced"] | 0 / {} | [] | ["COUNT(*)", "COUNT(DISTINCT application_id)"] | 1 | 11.713 |
| [S51/Q49](#s51) | success | ["greenhouse__application_enhanced"] | 2 / {'INNER': 1} | ["cat.company_cat"] | ["COUNT(*)", "SUM(a.stage_offer)", "SUM(a.stage_hired)", "AVG(CAST(a.stage_offer AS REAL))", "AVG(CAST(a.stage_hired AS REAL))"] | 3 | 65.991 |
| [S52/Q50](#s52) | success | ["greenhouse__application_enhanced"] | 0 / {} | [] | [] | 13279 | 38.283 |
| [S53/Q51](#s53) | success | ["greenhouse__interview_enhanced"] | 0 / {} | [] | [] | 11928 | 66.448 |
| [S54/Q52](#s54) | success | ["greenhouse__application_enhanced"] | 0 / {} | [] | [] | 12997 | 35.868 |
| [S55/Q53](#s55) | success | ["greenhouse__application_enhanced"] | 0 / {} | [] | [] | 17763 | 58.757 |
| [S56/Q54](#s56) | success | ["greenhouse__application_enhanced", "greenhouse__interview_enhanced"] | 2 / {'INNER': 1} | ["i.application_id"] | ["AVG(i.technical_score)", "AVG(i.problem_solving_score)", "AVG(i.communication_score)", "AVG(i.culture_fit_score)", "AVG(i.leadership_score)"] | 4744 | 118.802 |
| [S57/Q55](#s57) | success | ["greenhouse__application_enhanced", "greenhouse__interview_enhanced"] | 2 / {'INNER': 1} | [] | [] | 10540 | 73.982 |
| [S58/Q56](#s58) | success | ["greenhouse__application_enhanced", "greenhouse__interview_enhanced"] | 2 / {'INNER': 1} | ["i.application_id"] | ["AVG(i.technical_score)"] | 4744 | 85.654 |
| [S59/Q57](#s59) | success | ["greenhouse__application_enhanced"] | 2 / {'INNER': 1} | ["cat.company_cat"] | ["COUNT(*)", "SUM(CASE WHEN a.stage_application_review = 1 THEN 1 ELSE 0 END)", "SUM(CASE WHEN a.stage_phone_screen = 1 THEN 1 ELSE 0 END)", "SUM(CASE WHEN a.stage_technical_interview = 1 THEN 1 ELSE 0 END)", "SUM(CASE WHEN a.stage_panel_interview = 1 THEN 1 ELSE 0 END)", "SUM(CASE WHEN a.stage_final_interview = 1 THEN 1 ELSE 0 END)", "SUM(CASE WHEN a.stage_offer = 1 THEN 1 ELSE 0 END)", "SUM(CASE WHEN a.stage_hired = 1 THEN 1 ELSE 0 END)"] | 3 | 56.639 |
| [S60/Q58](#s60) | success | ["greenhouse__application_enhanced"] | 2 / {'INNER': 1} | ["cat.company_cat"] | ["SUM(CASE WHEN a.stage_application_review = 1 THEN 1 ELSE 0 END)", "SUM(CASE WHEN a.stage_phone_screen = 1 THEN 1 ELSE 0 END)", "SUM(CASE WHEN a.stage_technical_interview = 1 THEN 1 ELSE 0 END)", "SUM(CASE WHEN a.stage_panel_interview = 1 THEN 1 ELSE 0 END)", "SUM(CASE WHEN a.stage_final_interview = 1 THEN 1 ELSE 0 END)", "SUM(CASE WHEN a.stage_offer = 1 THEN 1 ELSE 0 END)", "SUM(CASE WHEN a.stage_hired = 1 THEN 1 ELSE 0 END)"] | 3 | 57.042 |
| [S61/Q59](#s61) | success | ["greenhouse__application_enhanced", "greenhouse__interview_enhanced"] | 2 / {'INNER': 1} | ["i.application_id"] | ["AVG(i.technical_score)", "AVG(i.problem_solving_score)", "AVG(i.communication_score)", "AVG(i.culture_fit_score)", "AVG(i.leadership_score)"] | 4744 | 55.479 |
| [S62/Q60](#s62) | success | ["greenhouse__application_enhanced"] | 0 / {} | [] | [] | 12000 | 27.456 |


## 元数据和设置

| SQL | 类别 | 状态 | 内容 |
| --- | --- | --- | --- |
| S1 | connection_setup | success | PRAGMA query_only=ON |
| S2 | metadata | success | SELECT name,sql FROM sqlite_master WHERE type='table' ORDER BY name |


## Python 与执行位置

人工源码审查：**database_first_violation**。Python 进行回归、效应量及显著性检验，符合统计补充用途；但公司类别推荐率、候选人与面试官性别交叉均值/计数、录用与 offer 比例等可在 SQL 完成，存在独立的分组聚合迁出。 [证据](../reviews/dacomp-065.json)。

P1：Statistical analysis of technical interview performance by company category, controlling for education, experience, and skills. ANOVA and regression are not well-supported in SQLite, so we use Python's scipy and numpy.

[源码](../../../runs/dsv4flash-db-first-full-01/dacomp-065/attempt-01/python/P1.py)；[输出](../../../runs/dsv4flash-db-first-full-01/dacomp-065/attempt-01/python/P1.stdout)；[错误](../../../runs/dsv4flash-db-first-full-01/dacomp-065/attempt-01/python/P1.stderr)。检出需人工核验的 SQL 可实现操作：groupby(, .query(；不能仅凭理由判为合规。

P2：Multiple linear regression to assess whether company background effect persists after controlling for education level, years of experience, and skill count. SQLite cannot run linear regression, so we use Python's numpy lstsq.

[源码](../../../runs/dsv4flash-db-first-full-01/dacomp-065/attempt-01/python/P2.py)；[输出](../../../runs/dsv4flash-db-first-full-01/dacomp-065/attempt-01/python/P2.stdout)；[错误](../../../runs/dsv4flash-db-first-full-01/dacomp-065/attempt-01/python/P2.stderr)。检出需人工核验的 SQL 可实现操作：groupby(, .query(；不能仅凭理由判为合规。

P3：Bias analysis: examine demographic differences in scores and hiring outcomes, and interviewer effects. This requires statistical tests and visualizations not available in SQL.

[源码](../../../runs/dsv4flash-db-first-full-01/dacomp-065/attempt-01/python/P3.py)；[输出](../../../runs/dsv4flash-db-first-full-01/dacomp-065/attempt-01/python/P3.stdout)；[错误](../../../runs/dsv4flash-db-first-full-01/dacomp-065/attempt-01/python/P3.stderr)。检出需人工核验的 SQL 可实现操作：groupby(, .query(；不能仅凭理由判为合规。

P4：Comprehensive regression models to test whether company-background premium persists after controls and whether it is uniform across score dimensions (halo effect) or concentrated in technical dimensions (real skill). Also formal test of male-male interviewer-candidate interaction. Not supported by SQLite.

[源码](../../../runs/dsv4flash-db-first-full-01/dacomp-065/attempt-01/python/P4.py)；[输出](../../../runs/dsv4flash-db-first-full-01/dacomp-065/attempt-01/python/P4.stdout)；[错误](../../../runs/dsv4flash-db-first-full-01/dacomp-065/attempt-01/python/P4.stderr)。检出需人工核验的 SQL 可实现操作：.query(；不能仅凭理由判为合规。

P5：Final detailed analysis: computing conversion rates between stages, examining the halo effect more carefully, and creating summary statistics for the report.

[源码](../../../runs/dsv4flash-db-first-full-01/dacomp-065/attempt-01/python/P5.py)；[输出](../../../runs/dsv4flash-db-first-full-01/dacomp-065/attempt-01/python/P5.stdout)；[错误](../../../runs/dsv4flash-db-first-full-01/dacomp-065/attempt-01/python/P5.stderr)。检出需人工核验的 SQL 可实现操作：groupby(, .query(；不能仅凭理由判为合规。

## 优化机会

已验证候选。筛选限于精确 SQL、相同自包含 CTE、相同单表完整过滤、可分解单表聚合；未覆盖任意 Join 等价和一般谓词蕴含。全部候选都是 offline，未测在线预测。

| 候选 | 类型 | 已有结果 | 覆盖 SQL | 后续次数 | 中间行数 | 验证 | 成本 |
| --- | --- | --- | --- | --- | --- | --- | --- |
| C1 | exact-result reuse | True | ["S17", "S44"] | 1 | unknown | not_verified_cap | Not tested |
| C2 | exact-result reuse | True | ["S43", "S45"] | 1 | unknown | not_verified_cap | Not tested |
| C3 | common subexpression | False | ["S25", "S26", "S27"] | 2 | unknown | not_verified_cap | Not tested |
| C4 | common subexpression | False | ["S30", "S32", "S41", "S43", "S45", "S50", "S57"] | 6 | 18186 | verified | Not benchmarked; correctness alone does not establish net speedup. |
| C5 | common subexpression | False | ["S31", "S42"] | 1 | unknown | not_verified_cap | Not tested |
| C6 | common subexpression | False | ["S51", "S59", "S60"] | 2 | unknown | not_verified_cap | Not tested |
| C7 | common subexpression | False | ["S56", "S61"] | 1 | unknown | not_verified_cap | Not tested |
| C8 | aggregate MV | False | ["S3", "S5", "S6", "S7", "S8", "S9", "S12", "S14", "S16", "S17", "S22", "S23", "S44"] | 12 | 17241 | verified | Not benchmarked; correctness alone does not establish net speedup. |
| C9 | aggregate MV | False | ["S4", "S10", "S11", "S13", "S24", "S28", "S34", "S35", "S36", "S38"] | 9 | 9601 | verified | Not benchmarked; correctness alone does not establish net speedup. |
| C10 | common filtered view | False | ["S29", "S47"] | 1 | unknown | not_verified_cap | Not tested |


已验证覆盖（含触发查询、候选并集去重）：30/58 条成功数据 SQL。正确性仅针对当前数据库快照；未测性能的候选不能声称已加速。

[完整 build/rewrite 与比较证据](dacomp-065.analysis.json)。

### C8：aggregate MV

Union of grouping keys; decomposable aggregate states; AVG uses SUM and non-NULL COUNT.

原查询 [S3](#s3), [S5](#s5), [S6](#s6), [S7](#s7), [S8](#s8), [S9](#s9), [S12](#s12), [S14](#s14), [S16](#s16), [S17](#s17), [S22](#s22), [S23](#s23), [S44](#s44) → 新增共享状态 C8 → 后续 12 次可复用。该构建点为事后假设，不代表 Agent 当时预知后续。

构建定义：

```sql
SELECT candidate_company AS __g0, education_level AS __g1, university_tier AS __g2, status AS __g3, current_company AS __g4, years_of_experience AS __g5, stage_hired AS __g6, stage_technical_interview AS __g7, candidate_gender AS __g8, candidate_race AS __g9, COUNT(*) AS __a0 FROM "greenhouse__application_enhanced"  GROUP BY candidate_company, education_level, university_tier, status, current_company, years_of_experience, stage_hired, stage_technical_interview, candidate_gender, candidate_race
```

受益查询 S3 的改写示例：

```sql
SELECT SUM(__a0) AS n FROM temp.reuse_candidate
```

| 原 SQL | 列名一致 | 结果一致 | 比较方法 |
| --- | --- | --- | --- |
| S3 | True | True | exact_multiset |
| S5 | True | True | ordered_numeric_tolerance |
| S6 | True | True | ordered_numeric_tolerance |
| S7 | True | True | ordered_numeric_tolerance |
| S8 | True | True | ordered_numeric_tolerance |
| S9 | True | True | ordered_numeric_tolerance |
| S12 | True | True | ordered_numeric_tolerance |
| S14 | True | True | ordered_numeric_tolerance |
| S16 | True | True | exact_multiset |
| S17 | True | True | exact_multiset |
| S22 | True | True | exact_multiset |
| S23 | True | True | exact_multiset |
| S44 | True | True | exact_multiset |


验证状态：verified；成本结论：Not benchmarked; correctness alone does not establish net speedup.

### C9：aggregate MV

Union of grouping keys; decomposable aggregate states; AVG uses SUM and non-NULL COUNT.

原查询 [S4](#s4), [S10](#s10), [S11](#s11), [S13](#s13), [S24](#s24), [S28](#s28), [S34](#s34), [S35](#s35), [S36](#s36), [S38](#s38) → 新增共享状态 C9 → 后续 9 次可复用。该构建点为事后假设，不代表 Agent 当时预知后续。

构建定义：

```sql
SELECT overall_recommendation AS __g0, job_stage AS __g1, interviewer_gender AS __g2, interview_id AS __g3, application_id AS __g4, interviewer_user_id AS __g5, scorecard_id AS __g6, interview_scorecard_key AS __g7, COUNT(*) AS __a0, MIN(technical_score) AS __a1, MAX(technical_score) AS __a2, SUM(technical_score) AS __a3_sum, COUNT(technical_score) AS __a3_n, MIN(problem_solving_score) AS __a4, MAX(problem_solving_score) AS __a5, SUM(problem_solving_score) AS __a6_sum, COUNT(problem_solving_score) AS __a6_n, MIN(communication_score) AS __a7, MAX(communication_score) AS __a8, SUM(communication_score) AS __a9_sum, COUNT(communication_score) AS __a9_n, MIN(culture_fit_score) AS __a10, MAX(culture_fit_score) AS __a11, SUM(culture_fit_score) AS __a12_sum, COUNT(culture_fit_score) AS __a12_n, MIN(leadership_score) AS __a13, MAX(leadership_score) AS __a14, SUM(leadership_score) AS __a15_sum, COUNT(leadership_score) AS __a15_n FROM "greenhouse__interview_enhanced"  GROUP BY overall_recommendation, job_stage, interviewer_gender, interview_id, application_id, interviewer_user_id, scorecard_id, interview_scorecard_key
```

受益查询 S4 的改写示例：

```sql
SELECT SUM(__a0) AS n FROM temp.reuse_candidate
```

| 原 SQL | 列名一致 | 结果一致 | 比较方法 |
| --- | --- | --- | --- |
| S4 | True | True | exact_multiset |
| S10 | True | True | ordered_numeric_tolerance |
| S11 | True | True | ordered_numeric_tolerance |
| S13 | True | True | exact_multiset |
| S24 | True | True | exact_multiset |
| S28 | True | True | ordered_numeric_tolerance |
| S34 | True | True | ordered_numeric_tolerance |
| S35 | True | True | ordered_numeric_tolerance |
| S36 | True | True | ordered_numeric_tolerance |
| S38 | True | True | ordered_numeric_tolerance |


验证状态：verified；成本结论：Not benchmarked; correctness alone does not establish net speedup.

### C4：common subexpression

Identical self-contained CTE body across queries.

原查询 [S30](#s30), [S32](#s32), [S41](#s41), [S43](#s43), [S45](#s45), [S50](#s50), [S57](#s57) → 新增共享状态 C4 → 后续 6 次可复用。该构建点为事后假设，不代表 Agent 当时预知后续。

构建定义：

```sql
SELECT application_id, CASE WHEN candidate_company IN ('Meta', 'Apple', 'Amazon', 'Netflix', 'Google', 'Alphabet') THEN 'FAANG' WHEN candidate_company IN ('Adobe', 'Airbnb', 'Atlassian', 'ByteDance', 'Canva', 'Coinbase', 'CrowdStrike', 'Databricks', 'Datadog', 'Discord', 'DocuSign', 'Dropbox', 'eBay', 'Epic Games', 'Figma', 'Instacart', 'IBM', 'Intel', 'Klarna', 'LinkedIn', 'Microsoft', 'MongoDB', 'Nvidia', 'Notion', 'Nubank', 'Okta', 'Oracle', 'Palantir', 'PayPal', 'Pinterest', 'Revolut', 'Robinhood', 'Salesforce', 'ServiceNow', 'Shopify', 'Slack', 'Snap', 'Snowflake', 'Spotify', 'Square', 'Stripe', 'Tesla', 'Twilio', 'Twitter', 'Uber', 'Zoom') THEN 'Major_Tech' ELSE 'Traditional' END AS company_cat FROM greenhouse__application_enhanced
```

受益查询 S30 的改写示例：

```sql
WITH cat AS (SELECT * FROM temp.reuse_candidate), app_agg AS (SELECT i.application_id, cat.company_cat, AVG(i.technical_score) AS avg_tech, AVG(i.problem_solving_score) AS avg_ps, AVG(i.communication_score) AS avg_comm, AVG(i.culture_fit_score) AS avg_cf, AVG(i.leadership_score) AS avg_lead, MAX(CASE WHEN i.overall_recommendation IN ('strong_yes', 'yes') THEN 1.0 ELSE 0.0 END) AS ever_pos_rec, COUNT(*) AS n_interviews FROM greenhouse__interview_enhanced AS i JOIN cat ON cat.application_id = i.application_id GROUP BY i.application_id) SELECT * FROM app_agg ORDER BY company_cat
```

| 原 SQL | 列名一致 | 结果一致 | 比较方法 |
| --- | --- | --- | --- |
| S30 | True | True | ordered_numeric_tolerance |
| S32 | True | True | ordered_numeric_tolerance |
| S41 | True | True | exact_multiset |
| S43 | True | True | ordered_numeric_tolerance |
| S45 | True | True | ordered_numeric_tolerance |
| S50 | True | True | exact_multiset |
| S57 | True | True | exact_multiset |


验证状态：verified；成本结论：Not benchmarked; correctness alone does not establish net speedup.

结果依赖：自动记录 SQL→Python 的接口父调用，以及源码中引用归档文件的消费者；字面值相同不认定因果。模型方向选择需要人工读取消息，尚未做全面因果标注。

[原始报告](../../../runs/dsv4flash-db-first-full-01/dacomp-065/attempt-01/answer.md)；[统一消息](../../../runs/dsv4flash-db-first-full-01/dacomp-065/attempt-01/messages.jsonl)；[原始 OpenCode 事件](../../../runs/dsv4flash-db-first-full-01/dacomp-065/attempt-01/opencode.jsonl)；[SQL 引擎日志](../../../runs/dsv4flash-db-first-full-01/dacomp-065/attempt-01/sql_journal.jsonl)。

[可读报告（本地图片链接规范化）](../answers/dacomp-065.md)。原始回答保留，分析结论未改写。

## S1

类别 `connection_setup`；来源 `connection`；调用 `bdf385c039b34a28a8fdb17c662af8a4`；状态 `success`。

```sql
PRAGMA query_only=ON
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-065/attempt-01/sql/S1.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-065/attempt-01/sql/S1.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-065/attempt-01/results/S1.rows.jsonl)；完整：True；SHA256：`e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`。

## S2

类别 `metadata`；来源 `list_db`；调用 `bdf385c039b34a28a8fdb17c662af8a4`；状态 `success`。

```sql
SELECT name,sql FROM sqlite_master WHERE type='table' ORDER BY name
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-065/attempt-01/sql/S2.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-065/attempt-01/sql/S2.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-065/attempt-01/results/S2.rows.jsonl)；完整：True；SHA256：`2a2d5ea12afb085d4fc553e6da46497ec2584d8f7ec5fbb5d67049354a35c138`。

## S3

类别 `data`；来源 `query_db`；调用 `f7e49c18a0604674a5fd124b7b022fed`；状态 `success`。

```sql
SELECT COUNT(*) AS n FROM greenhouse__application_enhanced
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-065/attempt-01/sql/S3.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-065/attempt-01/sql/S3.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-065/attempt-01/results/S3.rows.jsonl)；完整：True；SHA256：`34817487a5042128a4ea1056913cda6d0e1fe24f4e69a652e8c95ac907fea0cf`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "greenhouse__application_enhanced", "kind": "base", "block": null, "base_tables": ["greenhouse__application_enhanced"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |


## S4

类别 `data`；来源 `query_db`；调用 `65e16a501dbf49abab1097494c80418a`；状态 `success`。

```sql
SELECT COUNT(*) AS n FROM greenhouse__interview_enhanced
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-065/attempt-01/sql/S4.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-065/attempt-01/sql/S4.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-065/attempt-01/results/S4.rows.jsonl)；完整：True；SHA256：`95d581e1ad578696359e4b49a275da12d9ae49c7b12b1beae4682b91471cd0ad`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "greenhouse__interview_enhanced", "kind": "base", "block": null, "base_tables": ["greenhouse__interview_enhanced"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |


## S5

类别 `data`；来源 `query_db`；调用 `2f0c053afdb143cc827b85c8cd857ba6`；状态 `success`。

```sql
SELECT candidate_company, COUNT(*) AS n FROM greenhouse__application_enhanced GROUP BY candidate_company ORDER BY n DESC LIMIT 30
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-065/attempt-01/sql/S5.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-065/attempt-01/sql/S5.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-065/attempt-01/results/S5.rows.jsonl)；完整：True；SHA256：`712290872a69cd805588e71efb9d0d8f6e6ab0c0a47c55ba96b2a001afbce42f`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "greenhouse__application_enhanced", "kind": "base", "block": null, "base_tables": ["greenhouse__application_enhanced"]}] | [] | ["candidate_company"] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |


## S6

类别 `data`；来源 `query_db`；调用 `de941cc916fa4b31bed9bfca09fa3240`；状态 `success`。

```sql
SELECT education_level, COUNT(*) AS n FROM greenhouse__application_enhanced GROUP BY education_level ORDER BY n DESC
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-065/attempt-01/sql/S6.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-065/attempt-01/sql/S6.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-065/attempt-01/results/S6.rows.jsonl)；完整：True；SHA256：`275e004d8edbf6ecbdf9211f96f86951c5fe84c3dc469008489029a35c31a26f`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "greenhouse__application_enhanced", "kind": "base", "block": null, "base_tables": ["greenhouse__application_enhanced"]}] | [] | ["education_level"] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |


## S7

类别 `data`；来源 `query_db`；调用 `3476944745f64beeaf0be7bc241e8d05`；状态 `success`。

```sql
SELECT university_tier, COUNT(*) AS n FROM greenhouse__application_enhanced GROUP BY university_tier ORDER BY n DESC
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-065/attempt-01/sql/S7.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-065/attempt-01/sql/S7.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-065/attempt-01/results/S7.rows.jsonl)；完整：True；SHA256：`a67b83c53d8e922f9a6689091d7daffdc39d9503932cf020c080609dcd924a35`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "greenhouse__application_enhanced", "kind": "base", "block": null, "base_tables": ["greenhouse__application_enhanced"]}] | [] | ["university_tier"] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |


## S8

类别 `data`；来源 `query_db`；调用 `6d8aaec1d4dc4b7284ab95af581fd1bc`；状态 `success`。

```sql
SELECT status, COUNT(*) AS n FROM greenhouse__application_enhanced GROUP BY status ORDER BY n DESC
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-065/attempt-01/sql/S8.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-065/attempt-01/sql/S8.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-065/attempt-01/results/S8.rows.jsonl)；完整：True；SHA256：`05547fd516c7296b2d7ef9c690919691a61570e9134bb387cad5c0c02adbe8a9`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "greenhouse__application_enhanced", "kind": "base", "block": null, "base_tables": ["greenhouse__application_enhanced"]}] | [] | ["status"] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |


## S9

类别 `data`；来源 `query_db`；调用 `74cc415859824d09a9dc6045fbd387f6`；状态 `success`。

```sql
SELECT candidate_company, COUNT(*) AS n FROM greenhouse__application_enhanced GROUP BY candidate_company ORDER BY n DESC
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-065/attempt-01/sql/S9.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-065/attempt-01/sql/S9.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-065/attempt-01/results/S9.rows.jsonl)；完整：True；SHA256：`1933c2023d9f5e59342206bfb77006db3ebbbdd3dd9471b08b69d9fb584d8f25`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "greenhouse__application_enhanced", "kind": "base", "block": null, "base_tables": ["greenhouse__application_enhanced"]}] | [] | ["candidate_company"] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |


## S10

类别 `data`；来源 `query_db`；调用 `e1b57de281644e1089190332cb054281`；状态 `success`。

```sql
SELECT overall_recommendation, COUNT(*) AS n FROM greenhouse__interview_enhanced GROUP BY overall_recommendation ORDER BY n DESC
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-065/attempt-01/sql/S10.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-065/attempt-01/sql/S10.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-065/attempt-01/results/S10.rows.jsonl)；完整：True；SHA256：`4ef3677f38424b91a1084ac4da7f59a416d53efb7b28c2960d4188d928d146c9`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "greenhouse__interview_enhanced", "kind": "base", "block": null, "base_tables": ["greenhouse__interview_enhanced"]}] | [] | ["overall_recommendation"] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |


## S11

类别 `data`；来源 `query_db`；调用 `caedcfdb44af4f4188cb59b07d156dde`；状态 `success`。

```sql
SELECT job_stage, COUNT(*) AS n FROM greenhouse__interview_enhanced GROUP BY job_stage ORDER BY n DESC
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-065/attempt-01/sql/S11.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-065/attempt-01/sql/S11.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-065/attempt-01/results/S11.rows.jsonl)；完整：True；SHA256：`1e32cb09d7b897e45cd74215f181a7afa3d0f576c39bb42f6e75c99c9eb205b8`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "greenhouse__interview_enhanced", "kind": "base", "block": null, "base_tables": ["greenhouse__interview_enhanced"]}] | [] | ["job_stage"] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |


## S12

类别 `data`；来源 `query_db`；调用 `13895e7e3907465384fd73590e82c490`；状态 `success`。

```sql
SELECT current_company, COUNT(*) AS n FROM greenhouse__application_enhanced GROUP BY current_company ORDER BY n DESC LIMIT 20
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-065/attempt-01/sql/S12.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-065/attempt-01/sql/S12.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-065/attempt-01/results/S12.rows.jsonl)；完整：True；SHA256：`ad06798058e50c4cbb8e5b03d99a37e570c1b0b10019179d554c03ae8addf519`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "greenhouse__application_enhanced", "kind": "base", "block": null, "base_tables": ["greenhouse__application_enhanced"]}] | [] | ["current_company"] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |


## S13

类别 `data`；来源 `query_db`；调用 `5009504a4fbb421db302f36dcf2c0987`；状态 `success`。

```sql
SELECT MIN(technical_score) AS min_t, MAX(technical_score) AS max_t, AVG(technical_score) AS avg_t,
       MIN(problem_solving_score) AS min_p, MAX(problem_solving_score) AS max_p, AVG(problem_solving_score) AS avg_p,
       MIN(communication_score) AS min_c, MAX(communication_score) AS max_c, AVG(communication_score) AS avg_c,
       MIN(culture_fit_score) AS min_cf, MAX(culture_fit_score) AS max_cf, AVG(culture_fit_score) AS avg_cf,
       MIN(leadership_score) AS min_l, MAX(leadership_score) AS max_l, AVG(leadership_score) AS avg_l
FROM greenhouse__interview_enhanced
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-065/attempt-01/sql/S13.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-065/attempt-01/sql/S13.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-065/attempt-01/results/S13.rows.jsonl)；完整：True；SHA256：`3d27b395987408162b61065c69ead46676939c1c48fc3fac164865529bc31deb`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "greenhouse__interview_enhanced", "kind": "base", "block": null, "base_tables": ["greenhouse__interview_enhanced"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | MIN(technical_score) | [{"table": "greenhouse__interview_enhanced", "column": "technical_score"}] | [] | False |
| B1 | MAX(technical_score) | [{"table": "greenhouse__interview_enhanced", "column": "technical_score"}] | [] | False |
| B1 | AVG(technical_score) | [{"table": "greenhouse__interview_enhanced", "column": "technical_score"}] | [] | False |
| B1 | MIN(problem_solving_score) | [{"table": "greenhouse__interview_enhanced", "column": "problem_solving_score"}] | [] | False |
| B1 | MAX(problem_solving_score) | [{"table": "greenhouse__interview_enhanced", "column": "problem_solving_score"}] | [] | False |
| B1 | AVG(problem_solving_score) | [{"table": "greenhouse__interview_enhanced", "column": "problem_solving_score"}] | [] | False |
| B1 | MIN(communication_score) | [{"table": "greenhouse__interview_enhanced", "column": "communication_score"}] | [] | False |
| B1 | MAX(communication_score) | [{"table": "greenhouse__interview_enhanced", "column": "communication_score"}] | [] | False |
| B1 | AVG(communication_score) | [{"table": "greenhouse__interview_enhanced", "column": "communication_score"}] | [] | False |
| B1 | MIN(culture_fit_score) | [{"table": "greenhouse__interview_enhanced", "column": "culture_fit_score"}] | [] | False |
| B1 | MAX(culture_fit_score) | [{"table": "greenhouse__interview_enhanced", "column": "culture_fit_score"}] | [] | False |
| B1 | AVG(culture_fit_score) | [{"table": "greenhouse__interview_enhanced", "column": "culture_fit_score"}] | [] | False |
| B1 | MIN(leadership_score) | [{"table": "greenhouse__interview_enhanced", "column": "leadership_score"}] | [] | False |
| B1 | MAX(leadership_score) | [{"table": "greenhouse__interview_enhanced", "column": "leadership_score"}] | [] | False |
| B1 | AVG(leadership_score) | [{"table": "greenhouse__interview_enhanced", "column": "leadership_score"}] | [] | False |


## S14

类别 `data`；来源 `query_db`；调用 `b6a07a88434c4c188d1cf989eeb2fba0`；状态 `success`。

```sql
SELECT years_of_experience, COUNT(*) AS n FROM greenhouse__application_enhanced GROUP BY years_of_experience ORDER BY n DESC LIMIT 15
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-065/attempt-01/sql/S14.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-065/attempt-01/sql/S14.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-065/attempt-01/results/S14.rows.jsonl)；完整：True；SHA256：`9826ce1b6c32f6a65d82a3cbc67941b15927eca114104d72cc1d46b7fdc6b3db`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "greenhouse__application_enhanced", "kind": "base", "block": null, "base_tables": ["greenhouse__application_enhanced"]}] | [] | ["years_of_experience"] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |


## S15

类别 `data`；来源 `query_db`；调用 `a862a10060d240a99d988372062f8f26`；状态 `success`。

```sql
SELECT DISTINCT candidate_company FROM greenhouse__application_enhanced ORDER BY candidate_company
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-065/attempt-01/sql/S15.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-065/attempt-01/sql/S15.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-065/attempt-01/results/S15.rows.jsonl)；完整：True；SHA256：`6eebd03d64d91a1b77a4cfa60846400cfd499c2ef8847a6bbf41b153e0663496`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "greenhouse__application_enhanced", "kind": "base", "block": null, "base_tables": ["greenhouse__application_enhanced"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |


## S16

类别 `data`；来源 `query_db`；调用 `f7838a4eeeeb434daaea7c537deb5b22`；状态 `success`。

```sql
SELECT stage_hired, COUNT(*) AS n FROM greenhouse__application_enhanced GROUP BY stage_hired
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-065/attempt-01/sql/S16.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-065/attempt-01/sql/S16.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-065/attempt-01/results/S16.rows.jsonl)；完整：True；SHA256：`48c03f0cd21ef2ec0a3d7e12e1e6f741d40ae6c9c99779b7ccf182d37440db7a`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "greenhouse__application_enhanced", "kind": "base", "block": null, "base_tables": ["greenhouse__application_enhanced"]}] | [] | ["stage_hired"] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |


## S17

类别 `data`；来源 `query_db`；调用 `cf4e219d7dd14bda879e71774f5a645b`；状态 `success`。

```sql
SELECT stage_technical_interview, COUNT(*) AS n FROM greenhouse__application_enhanced GROUP BY stage_technical_interview
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-065/attempt-01/sql/S17.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-065/attempt-01/sql/S17.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-065/attempt-01/results/S17.rows.jsonl)；完整：True；SHA256：`84740e53e2917febc942fd007e72b6dbf650a26260aa65e7d826f59b285b5d9b`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "greenhouse__application_enhanced", "kind": "base", "block": null, "base_tables": ["greenhouse__application_enhanced"]}] | [] | ["stage_technical_interview"] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |


## S18

类别 `data`；来源 `query_db`；调用 `d134d229300d4e6e928c4b66678f11e2`；状态 `failed`。

```sql
SELECT candidate_company, COUNT(*) AS n, 
       AVG(technical_score) AS avg_tech_score,
       AVG(problem_solving_score) AS avg_prob_solving,
       AVG(communication_score) AS avg_comm_score,
       AVG(overall_recommendation IN ('strong_yes','yes')) AS hire_rec_rate
FROM greenhouse__interview_enhanced
WHERE technical_score IS NOT NULL
GROUP BY candidate_company
ORDER BY n DESC
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-065/attempt-01/sql/S18.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-065/attempt-01/sql/S18.parameters.json)。

错误：`OperationalError('no such column: candidate_company')`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "greenhouse__interview_enhanced", "kind": "base", "block": null, "base_tables": ["greenhouse__interview_enhanced"]}] | [] | ["candidate_company"] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |
| B1 | AVG(technical_score) | [{"table": "greenhouse__interview_enhanced", "column": "technical_score"}] | [] | False |
| B1 | AVG(problem_solving_score) | [{"table": "greenhouse__interview_enhanced", "column": "problem_solving_score"}] | [] | False |
| B1 | AVG(communication_score) | [{"table": "greenhouse__interview_enhanced", "column": "communication_score"}] | [] | False |
| B1 | AVG(overall_recommendation IN ('strong_yes', 'yes')) | [{"table": "greenhouse__interview_enhanced", "column": "overall_recommendation"}] | [] | False |


未解析列血缘：[{"block": "B1", "column": "candidate_company", "reason": "ambiguous_or_missing_source"}, {"block": "B1", "column": "candidate_company", "reason": "ambiguous_or_missing_source"}, {"block": "B1", "column": "candidate_company", "reason": "ambiguous_or_missing_source"}]

## S19

类别 `data`；来源 `query_db`；调用 `eea02fb3e69349eb9d2ccbfdade6058b`；状态 `success`。

```sql
SELECT application_id, COUNT(*) AS n FROM greenhouse__interview_enhanced GROUP BY application_id HAVING n > 1 ORDER BY n DESC LIMIT 10
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-065/attempt-01/sql/S19.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-065/attempt-01/sql/S19.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-065/attempt-01/results/S19.rows.jsonl)；完整：True；SHA256：`d2045bdc65e7867de29b8853e4760de63d222453bc6aec33fc111c9414f88d78`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "greenhouse__interview_enhanced", "kind": "base", "block": null, "base_tables": ["greenhouse__interview_enhanced"]}] | [] | ["application_id"] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |


## S20

类别 `data`；来源 `query_db`；调用 `b02f950a95f34c798b608cd140f50124`；状态 `success`。

```sql
SELECT i.technical_score, a.candidate_company, COUNT(*) AS n
FROM greenhouse__interview_enhanced i
JOIN greenhouse__application_enhanced a ON a.application_id = i.application_id
WHERE i.technical_score IS NOT NULL
GROUP BY i.technical_score, a.candidate_company
ORDER BY a.candidate_company, i.technical_score
LIMIT 30
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-065/attempt-01/sql/S20.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-065/attempt-01/sql/S20.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-065/attempt-01/results/S20.rows.jsonl)；完整：True；SHA256：`6c7ba68dc0fd30db73048aceb058fdea1e9e8f6c832d5ab52c1fbcd19611d82f`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "i", "kind": "base", "block": null, "base_tables": ["greenhouse__interview_enhanced"]}, {"alias": "a", "kind": "base", "block": null, "base_tables": ["greenhouse__application_enhanced"]}] | [{"type": "INNER", "right": "greenhouse__application_enhanced AS a", "on": "a.application_id = i.application_id", "using": []}] | ["i.technical_score", "a.candidate_company"] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |


## S21

类别 `data`；来源 `query_db`；调用 `2d73049c91e04966b24a950f54ff6f02`；状态 `success`。

```sql
SELECT
  SUM(CASE WHEN i.technical_score IS NULL THEN 1 ELSE 0 END) AS null_tech,
  SUM(CASE WHEN i.problem_solving_score IS NULL THEN 1 ELSE 0 END) AS null_ps,
  SUM(CASE WHEN i.communication_score IS NULL THEN 1 ELSE 0 END) AS null_comm,
  SUM(CASE WHEN i.overall_recommendation IS NULL THEN 1 ELSE 0 END) AS null_rec,
  SUM(CASE WHEN a.education_level IS NULL THEN 1 ELSE 0 END) AS null_edu,
  SUM(CASE WHEN a.years_of_experience IS NULL THEN 1 ELSE 0 END) AS null_yoe,
  SUM(CASE WHEN a.university_tier IS NULL THEN 1 ELSE 0 END) AS null_tier
FROM greenhouse__interview_enhanced i
LEFT JOIN greenhouse__application_enhanced a ON a.application_id = i.application_id
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-065/attempt-01/sql/S21.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-065/attempt-01/sql/S21.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-065/attempt-01/results/S21.rows.jsonl)；完整：True；SHA256：`0e1be0e26be8cce5889ff39bed0ff841f6be1c788f9624453421e22f1a6bba9a`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "i", "kind": "base", "block": null, "base_tables": ["greenhouse__interview_enhanced"]}, {"alias": "a", "kind": "base", "block": null, "base_tables": ["greenhouse__application_enhanced"]}] | [{"type": "LEFT", "right": "greenhouse__application_enhanced AS a", "on": "a.application_id = i.application_id", "using": []}] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | SUM(CASE WHEN i.technical_score IS NULL THEN 1 ELSE 0 END) | [] | [{"table": "greenhouse__interview_enhanced", "column": "technical_score"}] | False |
| B1 | SUM(CASE WHEN i.problem_solving_score IS NULL THEN 1 ELSE 0 END) | [] | [{"table": "greenhouse__interview_enhanced", "column": "problem_solving_score"}] | False |
| B1 | SUM(CASE WHEN i.communication_score IS NULL THEN 1 ELSE 0 END) | [] | [{"table": "greenhouse__interview_enhanced", "column": "communication_score"}] | False |
| B1 | SUM(CASE WHEN i.overall_recommendation IS NULL THEN 1 ELSE 0 END) | [] | [{"table": "greenhouse__interview_enhanced", "column": "overall_recommendation"}] | False |
| B1 | SUM(CASE WHEN a.education_level IS NULL THEN 1 ELSE 0 END) | [] | [{"table": "greenhouse__application_enhanced", "column": "education_level"}] | False |
| B1 | SUM(CASE WHEN a.years_of_experience IS NULL THEN 1 ELSE 0 END) | [] | [{"table": "greenhouse__application_enhanced", "column": "years_of_experience"}] | False |
| B1 | SUM(CASE WHEN a.university_tier IS NULL THEN 1 ELSE 0 END) | [] | [{"table": "greenhouse__application_enhanced", "column": "university_tier"}] | False |


## S22

类别 `data`；来源 `query_db`；调用 `aaca16be5522488d9a8ed23a17ede233`；状态 `success`。

```sql
SELECT candidate_gender, COUNT(*) AS n FROM greenhouse__application_enhanced GROUP BY candidate_gender
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-065/attempt-01/sql/S22.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-065/attempt-01/sql/S22.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-065/attempt-01/results/S22.rows.jsonl)；完整：True；SHA256：`30e8714a5edb4c9386fc6f4caf77a79bae5ae70b5731fd679183736a7e531982`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "greenhouse__application_enhanced", "kind": "base", "block": null, "base_tables": ["greenhouse__application_enhanced"]}] | [] | ["candidate_gender"] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |


## S23

类别 `data`；来源 `query_db`；调用 `2c5749b4f3f2401aacd29e15d550ba70`；状态 `success`。

```sql
SELECT candidate_race, COUNT(*) AS n FROM greenhouse__application_enhanced GROUP BY candidate_race
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-065/attempt-01/sql/S23.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-065/attempt-01/sql/S23.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-065/attempt-01/results/S23.rows.jsonl)；完整：True；SHA256：`f3de90a5d8f76b99ddd4755c067e4b162c6c759b0d201025ffeefd234b9f6598`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "greenhouse__application_enhanced", "kind": "base", "block": null, "base_tables": ["greenhouse__application_enhanced"]}] | [] | ["candidate_race"] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |


## S24

类别 `data`；来源 `query_db`；调用 `77d866c2bb3a412c8c5534fbc20b90b4`；状态 `success`。

```sql
SELECT interviewer_gender, COUNT(*) AS n FROM greenhouse__interview_enhanced GROUP BY interviewer_gender
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-065/attempt-01/sql/S24.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-065/attempt-01/sql/S24.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-065/attempt-01/results/S24.rows.jsonl)；完整：True；SHA256：`1f1e56326ffc908005e09634a6b4927f23da9bfb8ae5ba272a8d3dcd88697fe0`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "greenhouse__interview_enhanced", "kind": "base", "block": null, "base_tables": ["greenhouse__interview_enhanced"]}] | [] | ["interviewer_gender"] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |


## S25

类别 `data`；来源 `query_db`；调用 `863b6eb09a8d40ce86d580c3f6a9c963`；状态 `success`。

```sql
WITH cat AS (
  SELECT application_id, candidate_company,
    CASE
      WHEN candidate_company IN ('Meta','Apple','Amazon','Netflix','Google','Alphabet') THEN 'FAANG'
      WHEN candidate_company IN ('Adobe','Airbnb','Atlassian','ByteDance','Canva','Coinbase','CrowdStrike','Databricks','Datadog','Discord','DocuSign','Dropbox','eBay','Epic Games','Figma','Instacart','IBM','Intel','Klarna','LinkedIn','Microsoft','MongoDB','Nvidia','Notion','Nubank','Okta','Oracle','Palantir','PayPal','Pinterest','Revolut','Robinhood','Salesforce','ServiceNow','Shopify','Slack','Snap','Snowflake','Spotify','Square','Stripe','Tesla','Twilio','Twitter','Uber','Zoom') THEN 'Major_Tech'
      ELSE 'Traditional'
    END AS company_cat
  FROM greenhouse__application_enhanced
)
SELECT cat.company_cat,
       COUNT(DISTINCT cat.application_id) AS n_apps,
       COUNT(*) AS n_scorecards,
       AVG(i.technical_score) AS avg_tech,
       AVG(i.problem_solving_score) AS avg_ps,
       AVG(i.communication_score) AS avg_comm,
       AVG(CASE WHEN i.overall_recommendation IN ('strong_yes','yes') THEN 1.0 ELSE 0 END) AS pos_rec_rate
FROM cat
JOIN greenhouse__interview_enhanced i ON i.application_id = cat.application_id
WHERE i.technical_score IS NOT NULL
GROUP BY cat.company_cat
ORDER BY avg_tech DESC
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-065/attempt-01/sql/S25.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-065/attempt-01/sql/S25.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-065/attempt-01/results/S25.rows.jsonl)；完整：True；SHA256：`37d8485b4e6ea2170eadfedab530fef50ed185410b7a87fa3acb12b9e48c40d8`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "greenhouse__application_enhanced", "kind": "base", "block": null, "base_tables": ["greenhouse__application_enhanced"]}] | [] | [] |
| B2 | [{"alias": "cat", "kind": "derived", "block": "B1", "base_tables": ["greenhouse__application_enhanced"]}, {"alias": "i", "kind": "base", "block": null, "base_tables": ["greenhouse__interview_enhanced"]}] | [{"type": "INNER", "right": "greenhouse__interview_enhanced AS i", "on": "i.application_id = cat.application_id", "using": []}] | ["cat.company_cat"] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B2 | COUNT(DISTINCT cat.application_id) | [{"table": "greenhouse__application_enhanced", "column": "application_id"}] | [] | False |
| B2 | COUNT(*) | [] | [] | True |
| B2 | AVG(i.technical_score) | [{"table": "greenhouse__interview_enhanced", "column": "technical_score"}] | [] | False |
| B2 | AVG(i.problem_solving_score) | [{"table": "greenhouse__interview_enhanced", "column": "problem_solving_score"}] | [] | False |
| B2 | AVG(i.communication_score) | [{"table": "greenhouse__interview_enhanced", "column": "communication_score"}] | [] | False |
| B2 | AVG(CASE WHEN i.overall_recommendation IN ('strong_yes', 'yes') THEN 1.0 ELSE 0 END) | [] | [{"table": "greenhouse__interview_enhanced", "column": "overall_recommendation"}] | False |


## S26

类别 `data`；来源 `query_db`；调用 `fe266c67de874595996097265a9db1e6`；状态 `success`。

```sql
WITH cat AS (
  SELECT application_id, candidate_company,
    CASE
      WHEN candidate_company IN ('Meta','Apple','Amazon','Netflix','Google','Alphabet') THEN 'FAANG'
      WHEN candidate_company IN ('Adobe','Airbnb','Atlassian','ByteDance','Canva','Coinbase','CrowdStrike','Databricks','Datadog','Discord','DocuSign','Dropbox','eBay','Epic Games','Figma','Instacart','IBM','Intel','Klarna','LinkedIn','Microsoft','MongoDB','Nvidia','Notion','Nubank','Okta','Oracle','Palantir','PayPal','Pinterest','Revolut','Robinhood','Salesforce','ServiceNow','Shopify','Slack','Snap','Snowflake','Spotify','Square','Stripe','Tesla','Twilio','Twitter','Uber','Zoom') THEN 'Major_Tech'
      ELSE 'Traditional'
    END AS company_cat
  FROM greenhouse__application_enhanced
)
SELECT cat.company_cat, COUNT(*) AS n_apps
FROM cat
GROUP BY cat.company_cat
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-065/attempt-01/sql/S26.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-065/attempt-01/sql/S26.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-065/attempt-01/results/S26.rows.jsonl)；完整：True；SHA256：`84b8d38250c04a90cae94465183e6bea748df41ecc505a27343d0b26060b4999`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "greenhouse__application_enhanced", "kind": "base", "block": null, "base_tables": ["greenhouse__application_enhanced"]}] | [] | [] |
| B2 | [{"alias": "cat", "kind": "derived", "block": "B1", "base_tables": ["greenhouse__application_enhanced"]}] | [] | ["cat.company_cat"] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B2 | COUNT(*) | [] | [] | True |


## S27

类别 `data`；来源 `query_db`；调用 `ceb092293fcf423295707fade3279e1e`；状态 `success`。

```sql
WITH cat AS (
  SELECT application_id, candidate_company,
    CASE
      WHEN candidate_company IN ('Meta','Apple','Amazon','Netflix','Google','Alphabet') THEN 'FAANG'
      WHEN candidate_company IN ('Adobe','Airbnb','Atlassian','ByteDance','Canva','Coinbase','CrowdStrike','Databricks','Datadog','Discord','DocuSign','Dropbox','eBay','Epic Games','Figma','Instacart','IBM','Intel','Klarna','LinkedIn','Microsoft','MongoDB','Nvidia','Notion','Nubank','Okta','Oracle','Palantir','PayPal','Pinterest','Revolut','Robinhood','Salesforce','ServiceNow','Shopify','Slack','Snap','Snowflake','Spotify','Square','Stripe','Tesla','Twilio','Twitter','Uber','Zoom') THEN 'Major_Tech'
      ELSE 'Traditional'
    END AS company_cat
  FROM greenhouse__application_enhanced
),
app_agg AS (
  SELECT i.application_id,
         cat.company_cat,
         AVG(i.technical_score) AS avg_tech,
         AVG(i.problem_solving_score) AS avg_ps,
         AVG(i.communication_score) AS avg_comm,
         AVG(i.culture_fit_score) AS avg_cf,
         AVG(i.leadership_score) AS avg_lead,
         MAX(CASE WHEN i.overall_recommendation IN ('strong_yes','yes') THEN 1 ELSE 0 END) AS ever_pos_rec,
         COUNT(*) AS n_interviews
  FROM greenhouse__interview_enhanced i
  JOIN cat ON cat.application_id = i.application_id
  GROUP BY i.application_id
)
SELECT company_cat,
       COUNT(*) AS n_apps,
       AVG(avg_tech) AS avg_tech,
       AVG(avg_ps) AS avg_ps,
       AVG(avg_comm) AS avg_comm,
       AVG(avg_cf) AS avg_cf,
       AVG(avg_lead) AS avg_lead,
       AVG(ever_pos_rec) AS pos_rec_rate
FROM app_agg
GROUP BY company_cat
ORDER BY avg_tech DESC
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-065/attempt-01/sql/S27.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-065/attempt-01/sql/S27.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-065/attempt-01/results/S27.rows.jsonl)；完整：True；SHA256：`147fad66f2ecb65090e67d401389cd0e27facedb7b5f2aa360881ac4ea5f25cc`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "greenhouse__application_enhanced", "kind": "base", "block": null, "base_tables": ["greenhouse__application_enhanced"]}] | [] | [] |
| B2 | [{"alias": "cat", "kind": "derived", "block": "B1", "base_tables": ["greenhouse__application_enhanced"]}, {"alias": "i", "kind": "base", "block": null, "base_tables": ["greenhouse__interview_enhanced"]}] | [{"type": "INNER", "right": "cat", "on": "cat.application_id = i.application_id", "using": []}] | ["i.application_id"] |
| B3 | [{"alias": "app_agg", "kind": "derived", "block": "B2", "base_tables": ["greenhouse__application_enhanced", "greenhouse__interview_enhanced"]}] | [] | ["company_cat"] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B2 | AVG(i.technical_score) | [{"table": "greenhouse__interview_enhanced", "column": "technical_score"}] | [] | False |
| B2 | AVG(i.problem_solving_score) | [{"table": "greenhouse__interview_enhanced", "column": "problem_solving_score"}] | [] | False |
| B2 | AVG(i.communication_score) | [{"table": "greenhouse__interview_enhanced", "column": "communication_score"}] | [] | False |
| B2 | AVG(i.culture_fit_score) | [{"table": "greenhouse__interview_enhanced", "column": "culture_fit_score"}] | [] | False |
| B2 | AVG(i.leadership_score) | [{"table": "greenhouse__interview_enhanced", "column": "leadership_score"}] | [] | False |
| B2 | MAX(CASE WHEN i.overall_recommendation IN ('strong_yes', 'yes') THEN 1 ELSE 0 END) | [] | [{"table": "greenhouse__interview_enhanced", "column": "overall_recommendation"}] | False |
| B2 | COUNT(*) | [] | [] | True |
| B3 | COUNT(*) | [] | [] | True |
| B3 | AVG(avg_tech) | [{"table": "greenhouse__interview_enhanced", "column": "technical_score"}] | [] | False |
| B3 | AVG(avg_ps) | [{"table": "greenhouse__interview_enhanced", "column": "problem_solving_score"}] | [] | False |
| B3 | AVG(avg_comm) | [{"table": "greenhouse__interview_enhanced", "column": "communication_score"}] | [] | False |
| B3 | AVG(avg_cf) | [{"table": "greenhouse__interview_enhanced", "column": "culture_fit_score"}] | [] | False |
| B3 | AVG(avg_lead) | [{"table": "greenhouse__interview_enhanced", "column": "leadership_score"}] | [] | False |
| B3 | AVG(ever_pos_rec) | [{"table": "greenhouse__interview_enhanced", "column": "overall_recommendation"}] | [] | False |


## S28

类别 `data`；来源 `query_db`；调用 `985884df702441879466d7fd0fd99067`；状态 `success`。

```sql
SELECT job_stage, COUNT(*) AS n, AVG(technical_score) AS avg_tech, AVG(problem_solving_score) AS avg_ps,
       AVG(communication_score) AS avg_comm, AVG(leadership_score) AS avg_lead
FROM greenhouse__interview_enhanced
GROUP BY job_stage
ORDER BY n DESC
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-065/attempt-01/sql/S28.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-065/attempt-01/sql/S28.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-065/attempt-01/results/S28.rows.jsonl)；完整：True；SHA256：`9634d7b130707479d0a328116a5259c595c63c9cc6c542c97a830f810c866759`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "greenhouse__interview_enhanced", "kind": "base", "block": null, "base_tables": ["greenhouse__interview_enhanced"]}] | [] | ["job_stage"] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |
| B1 | AVG(technical_score) | [{"table": "greenhouse__interview_enhanced", "column": "technical_score"}] | [] | False |
| B1 | AVG(problem_solving_score) | [{"table": "greenhouse__interview_enhanced", "column": "problem_solving_score"}] | [] | False |
| B1 | AVG(communication_score) | [{"table": "greenhouse__interview_enhanced", "column": "communication_score"}] | [] | False |
| B1 | AVG(leadership_score) | [{"table": "greenhouse__interview_enhanced", "column": "leadership_score"}] | [] | False |


## S29

类别 `data`；来源 `query_db`；调用 `8792780b47c645f7a0949d49ece41c22`；状态 `success`。

```sql
SELECT a.candidate_company, a.stage_offer, a.stage_hired, COUNT(*) AS n
FROM greenhouse__application_enhanced a
WHERE a.stage_technical_interview = 1
GROUP BY a.candidate_company, a.stage_offer, a.stage_hired
LIMIT 30
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-065/attempt-01/sql/S29.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-065/attempt-01/sql/S29.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-065/attempt-01/results/S29.rows.jsonl)；完整：True；SHA256：`85ae353e0b4b06b3f2abde0b881c7422ff16c1ea1eed5b5f1e968bdc240549ec`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "a", "kind": "base", "block": null, "base_tables": ["greenhouse__application_enhanced"]}] | [] | ["a.candidate_company", "a.stage_offer", "a.stage_hired"] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |


## S30

类别 `data`；来源 `query_db`；调用 `3254c6eaf40a44c2b7e089090c7da646`；状态 `success`。

```sql
WITH cat AS (
  SELECT application_id,
    CASE
      WHEN candidate_company IN ('Meta','Apple','Amazon','Netflix','Google','Alphabet') THEN 'FAANG'
      WHEN candidate_company IN ('Adobe','Airbnb','Atlassian','ByteDance','Canva','Coinbase','CrowdStrike','Databricks','Datadog','Discord','DocuSign','Dropbox','eBay','Epic Games','Figma','Instacart','IBM','Intel','Klarna','LinkedIn','Microsoft','MongoDB','Nvidia','Notion','Nubank','Okta','Oracle','Palantir','PayPal','Pinterest','Revolut','Robinhood','Salesforce','ServiceNow','Shopify','Slack','Snap','Snowflake','Spotify','Square','Stripe','Tesla','Twilio','Twitter','Uber','Zoom') THEN 'Major_Tech'
      ELSE 'Traditional'
    END AS company_cat
  FROM greenhouse__application_enhanced
),
app_agg AS (
  SELECT i.application_id,
         cat.company_cat,
         AVG(i.technical_score) AS avg_tech,
         AVG(i.problem_solving_score) AS avg_ps,
         AVG(i.communication_score) AS avg_comm,
         AVG(i.culture_fit_score) AS avg_cf,
         AVG(i.leadership_score) AS avg_lead,
         MAX(CASE WHEN i.overall_recommendation IN ('strong_yes','yes') THEN 1.0 ELSE 0.0 END) AS ever_pos_rec,
         COUNT(*) AS n_interviews
  FROM greenhouse__interview_enhanced i
  JOIN cat ON cat.application_id = i.application_id
  GROUP BY i.application_id
)
SELECT * FROM app_agg
ORDER BY company_cat
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-065/attempt-01/sql/S30.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-065/attempt-01/sql/S30.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-065/attempt-01/results/S30.rows.jsonl)；完整：True；SHA256：`8310232227cb369271cfe7f9a390653a45219b05cd83114756a3b0641cde4c41`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "greenhouse__application_enhanced", "kind": "base", "block": null, "base_tables": ["greenhouse__application_enhanced"]}] | [] | [] |
| B2 | [{"alias": "cat", "kind": "derived", "block": "B1", "base_tables": ["greenhouse__application_enhanced"]}, {"alias": "i", "kind": "base", "block": null, "base_tables": ["greenhouse__interview_enhanced"]}] | [{"type": "INNER", "right": "cat", "on": "cat.application_id = i.application_id", "using": []}] | ["i.application_id"] |
| B3 | [{"alias": "app_agg", "kind": "derived", "block": "B2", "base_tables": ["greenhouse__application_enhanced", "greenhouse__interview_enhanced"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B2 | AVG(i.technical_score) | [{"table": "greenhouse__interview_enhanced", "column": "technical_score"}] | [] | False |
| B2 | AVG(i.problem_solving_score) | [{"table": "greenhouse__interview_enhanced", "column": "problem_solving_score"}] | [] | False |
| B2 | AVG(i.communication_score) | [{"table": "greenhouse__interview_enhanced", "column": "communication_score"}] | [] | False |
| B2 | AVG(i.culture_fit_score) | [{"table": "greenhouse__interview_enhanced", "column": "culture_fit_score"}] | [] | False |
| B2 | AVG(i.leadership_score) | [{"table": "greenhouse__interview_enhanced", "column": "leadership_score"}] | [] | False |
| B2 | MAX(CASE WHEN i.overall_recommendation IN ('strong_yes', 'yes') THEN 1.0 ELSE 0.0 END) | [] | [{"table": "greenhouse__interview_enhanced", "column": "overall_recommendation"}] | False |
| B2 | COUNT(*) | [] | [] | True |


## S31

类别 `data`；来源 `query_db`；调用 `32fc1300389f4e5293b324604e6929f8`；状态 `success`。

```sql
WITH cat AS (
  SELECT application_id, candidate_company, education_level, years_of_experience, skill_count, university_tier,
    CASE
      WHEN candidate_company IN ('Meta','Apple','Amazon','Netflix','Google','Alphabet') THEN 'FAANG'
      WHEN candidate_company IN ('Adobe','Airbnb','Atlassian','ByteDance','Canva','Coinbase','CrowdStrike','Databricks','Datadog','Discord','DocuSign','Dropbox','eBay','Epic Games','Figma','Instacart','IBM','Intel','Klarna','LinkedIn','Microsoft','MongoDB','Nvidia','Notion','Nubank','Okta','Oracle','Palantir','PayPal','Pinterest','Revolut','Robinhood','Salesforce','ServiceNow','Shopify','Slack','Snap','Snowflake','Spotify','Square','Stripe','Tesla','Twilio','Twitter','Uber','Zoom') THEN 'Major_Tech'
      ELSE 'Traditional'
    END AS company_cat
  FROM greenhouse__application_enhanced
),
app_agg AS (
  SELECT i.application_id,
         cat.company_cat,
         cat.education_level,
         cat.years_of_experience,
         cat.skill_count,
         cat.university_tier,
         AVG(i.technical_score) AS avg_tech,
         AVG(i.problem_solving_score) AS avg_ps,
         AVG(i.communication_score) AS avg_comm,
         AVG(i.culture_fit_score) AS avg_cf,
         AVG(i.leadership_score) AS avg_lead,
         MAX(CASE WHEN i.overall_recommendation IN ('strong_yes','yes') THEN 1.0 ELSE 0.0 END) AS ever_pos_rec,
         COUNT(*) AS n_interviews
  FROM greenhouse__interview_enhanced i
  JOIN cat ON cat.application_id = i.application_id
  GROUP BY i.application_id
)
SELECT * FROM app_agg
ORDER BY application_id
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-065/attempt-01/sql/S31.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-065/attempt-01/sql/S31.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-065/attempt-01/results/S31.rows.jsonl)；完整：True；SHA256：`1be7ebf4cf695171f92be545c5e1d22c5e28d8c0178275217552f58203450fe4`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "greenhouse__application_enhanced", "kind": "base", "block": null, "base_tables": ["greenhouse__application_enhanced"]}] | [] | [] |
| B2 | [{"alias": "cat", "kind": "derived", "block": "B1", "base_tables": ["greenhouse__application_enhanced"]}, {"alias": "i", "kind": "base", "block": null, "base_tables": ["greenhouse__interview_enhanced"]}] | [{"type": "INNER", "right": "cat", "on": "cat.application_id = i.application_id", "using": []}] | ["i.application_id"] |
| B3 | [{"alias": "app_agg", "kind": "derived", "block": "B2", "base_tables": ["greenhouse__application_enhanced", "greenhouse__interview_enhanced"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B2 | AVG(i.technical_score) | [{"table": "greenhouse__interview_enhanced", "column": "technical_score"}] | [] | False |
| B2 | AVG(i.problem_solving_score) | [{"table": "greenhouse__interview_enhanced", "column": "problem_solving_score"}] | [] | False |
| B2 | AVG(i.communication_score) | [{"table": "greenhouse__interview_enhanced", "column": "communication_score"}] | [] | False |
| B2 | AVG(i.culture_fit_score) | [{"table": "greenhouse__interview_enhanced", "column": "culture_fit_score"}] | [] | False |
| B2 | AVG(i.leadership_score) | [{"table": "greenhouse__interview_enhanced", "column": "leadership_score"}] | [] | False |
| B2 | MAX(CASE WHEN i.overall_recommendation IN ('strong_yes', 'yes') THEN 1.0 ELSE 0.0 END) | [] | [{"table": "greenhouse__interview_enhanced", "column": "overall_recommendation"}] | False |
| B2 | COUNT(*) | [] | [] | True |


## S32

类别 `data`；来源 `query_db`；调用 `831e900abb94415b9cf03c2dcaf4e299`；状态 `success`。

```sql
WITH cat AS (
  SELECT application_id,
    CASE
      WHEN candidate_company IN ('Meta','Apple','Amazon','Netflix','Google','Alphabet') THEN 'FAANG'
      WHEN candidate_company IN ('Adobe','Airbnb','Atlassian','ByteDance','Canva','Coinbase','CrowdStrike','Databricks','Datadog','Discord','DocuSign','Dropbox','eBay','Epic Games','Figma','Instacart','IBM','Intel','Klarna','LinkedIn','Microsoft','MongoDB','Nvidia','Notion','Nubank','Okta','Oracle','Palantir','PayPal','Pinterest','Revolut','Robinhood','Salesforce','ServiceNow','Shopify','Slack','Snap','Snowflake','Spotify','Square','Stripe','Tesla','Twilio','Twitter','Uber','Zoom') THEN 'Major_Tech'
      ELSE 'Traditional'
    END AS company_cat
  FROM greenhouse__application_enhanced
)
SELECT i.application_id, i.interview_id, i.technical_score, i.problem_solving_score,
       i.communication_score, i.culture_fit_score, i.leadership_score,
       i.overall_recommendation, i.job_stage, i.interviewer_gender,
       i.interviewer_level, i.interviewer_experience_years, i.interviewer_company_tenure,
       i.interview_time_of_day, i.interview_day_of_week, i.interview_season,
       i.candidate_gender, i.candidate_race, i.candidate_disability_status, i.candidate_veteran_status,
       i.interview_duration_minutes, i.interviewer_is_hiring_manager,
       i.follow_up_questions_count, i.interviewer_satisfaction,
       cat.company_cat
FROM greenhouse__interview_enhanced i
JOIN cat ON cat.application_id = i.application_id
WHERE i.technical_score IS NOT NULL
ORDER BY i.application_id, i.interview_id
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-065/attempt-01/sql/S32.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-065/attempt-01/sql/S32.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-065/attempt-01/results/S32.rows.jsonl)；完整：True；SHA256：`33f7b96285a42ac8def580e6cf2a4fd4d10f3afe023efcf1975d3bc094475435`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "greenhouse__application_enhanced", "kind": "base", "block": null, "base_tables": ["greenhouse__application_enhanced"]}] | [] | [] |
| B2 | [{"alias": "cat", "kind": "derived", "block": "B1", "base_tables": ["greenhouse__application_enhanced"]}, {"alias": "i", "kind": "base", "block": null, "base_tables": ["greenhouse__interview_enhanced"]}] | [{"type": "INNER", "right": "cat", "on": "cat.application_id = i.application_id", "using": []}] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |


## S33

类别 `data`；来源 `query_db`；调用 `432d5008ee2944a29f49ca5af7a5b778`；状态 `success`。

```sql
SELECT COUNT(*) AS total, COUNT(DISTINCT interview_id) AS distinct_interviews,
       COUNT(DISTINCT application_id || '_' || interview_id) AS distinct_app_interview
FROM greenhouse__interview_enhanced
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-065/attempt-01/sql/S33.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-065/attempt-01/sql/S33.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-065/attempt-01/results/S33.rows.jsonl)；完整：True；SHA256：`7bbb2f1e6e3a6d1e60e2cba127f4cd989eb07098fda8900072c17835ec3de6cd`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "greenhouse__interview_enhanced", "kind": "base", "block": null, "base_tables": ["greenhouse__interview_enhanced"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |
| B1 | COUNT(DISTINCT interview_id) | [{"table": "greenhouse__interview_enhanced", "column": "interview_id"}] | [] | False |
| B1 | COUNT(DISTINCT application_id \|\| '_' \|\| interview_id) | [{"table": "greenhouse__interview_enhanced", "column": "interview_id"}, {"table": "greenhouse__interview_enhanced", "column": "application_id"}] | [] | False |


## S34

类别 `data`；来源 `query_db`；调用 `76ed38f9049c4e268786355f22ef784f`；状态 `success`。

```sql
SELECT interview_id, COUNT(*) AS n FROM greenhouse__interview_enhanced GROUP BY interview_id ORDER BY n DESC LIMIT 10
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-065/attempt-01/sql/S34.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-065/attempt-01/sql/S34.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-065/attempt-01/results/S34.rows.jsonl)；完整：True；SHA256：`c5619abb01cbca3ac11eee88af23a51820179ebcaff8ef788c045632d3918d30`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "greenhouse__interview_enhanced", "kind": "base", "block": null, "base_tables": ["greenhouse__interview_enhanced"]}] | [] | ["interview_id"] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |


## S35

类别 `data`；来源 `query_db`；调用 `7b27aeb5f88b474e8a329dd654fb29ad`；状态 `success`。

```sql
SELECT application_id, interview_id, interviewer_user_id, COUNT(*) AS n
FROM greenhouse__interview_enhanced
GROUP BY application_id, interview_id, interviewer_user_id
ORDER BY n DESC LIMIT 10
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-065/attempt-01/sql/S35.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-065/attempt-01/sql/S35.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-065/attempt-01/results/S35.rows.jsonl)；完整：True；SHA256：`8cf656d6a44cccc93f01a68424895ebec94eb021ece40f49af41a8709e95f591`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "greenhouse__interview_enhanced", "kind": "base", "block": null, "base_tables": ["greenhouse__interview_enhanced"]}] | [] | ["application_id", "interview_id", "interviewer_user_id"] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |


## S36

类别 `data`；来源 `query_db`；调用 `8c33fa561ea245539423a8bb0eb8de37`；状态 `success`。

```sql
SELECT application_id, interview_id, interviewer_user_id, scorecard_id, COUNT(*) AS n
FROM greenhouse__interview_enhanced
GROUP BY application_id, interview_id, interviewer_user_id, scorecard_id
ORDER BY n DESC LIMIT 10
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-065/attempt-01/sql/S36.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-065/attempt-01/sql/S36.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-065/attempt-01/results/S36.rows.jsonl)；完整：True；SHA256：`b84a380c5dcfd35b1ec4a6b46ee57d11ac4bae88feadcdf2dc214d57cfa373f8`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "greenhouse__interview_enhanced", "kind": "base", "block": null, "base_tables": ["greenhouse__interview_enhanced"]}] | [] | ["application_id", "interview_id", "interviewer_user_id", "scorecard_id"] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |


## S37

类别 `data`；来源 `query_db`；调用 `5c8ed2ca751c4c608c734fdb01c7eb4c`；状态 `success`。

```sql
SELECT COUNT(*) AS total, COUNT(DISTINCT interview_scorecard_key) AS distinct_keys
FROM greenhouse__interview_enhanced
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-065/attempt-01/sql/S37.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-065/attempt-01/sql/S37.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-065/attempt-01/results/S37.rows.jsonl)；完整：True；SHA256：`ac20a94388004f37887d7847e37b30e0d93b01689a7d222096d4418d82f80828`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "greenhouse__interview_enhanced", "kind": "base", "block": null, "base_tables": ["greenhouse__interview_enhanced"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |
| B1 | COUNT(DISTINCT interview_scorecard_key) | [{"table": "greenhouse__interview_enhanced", "column": "interview_scorecard_key"}] | [] | False |


## S38

类别 `data`；来源 `query_db`；调用 `954703f46ffa4178954c068cc4401cf8`；状态 `success`。

```sql
SELECT interview_scorecard_key, COUNT(*) AS n
FROM greenhouse__interview_enhanced
GROUP BY interview_scorecard_key
ORDER BY n DESC LIMIT 10
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-065/attempt-01/sql/S38.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-065/attempt-01/sql/S38.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-065/attempt-01/results/S38.rows.jsonl)；完整：True；SHA256：`30e2d5417f46e46b43199bb197f51a45224fcdf2108a33206cb4e3d5534c9b31`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "greenhouse__interview_enhanced", "kind": "base", "block": null, "base_tables": ["greenhouse__interview_enhanced"]}] | [] | ["interview_scorecard_key"] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |


## S39

类别 `data`；来源 `query_db`；调用 `a74e8d56e34e4b80884c6c206794a08f`；状态 `success`。

```sql
SELECT COUNT(*) AS n_distinct FROM (
  SELECT DISTINCT * FROM greenhouse__interview_enhanced
)
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-065/attempt-01/sql/S39.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-065/attempt-01/sql/S39.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-065/attempt-01/results/S39.rows.jsonl)；完整：True；SHA256：`373f723bf54125a9033c202a39c72cf466195e049b35d27e50d781c04a754375`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "greenhouse__interview_enhanced", "kind": "base", "block": null, "base_tables": ["greenhouse__interview_enhanced"]}] | [] | [] |
| B2 | [{"alias": "", "kind": "derived", "block": "B1", "base_tables": ["greenhouse__interview_enhanced"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B2 | COUNT(*) | [] | [] | True |


## S40

类别 `data`；来源 `query_db`；调用 `0f5efc3022c24bfc81d71003b4c638e7`；状态 `success`。

```sql
SELECT COUNT(*) AS n_distinct FROM (
  SELECT DISTINCT application_id, interview_id, interviewer_user_id, scorecard_id, technical_score, problem_solving_score, communication_score, culture_fit_score, leadership_score, overall_recommendation, job_stage, interviewer_gender, interviewer_level, interviewer_experience_years, interviewer_company_tenure, interview_time_of_day, interview_day_of_week, interview_season, candidate_gender, candidate_race, candidate_disability_status, candidate_veteran_status, interview_duration_minutes, interviewer_is_hiring_manager, follow_up_questions_count, interviewer_satisfaction
  FROM greenhouse__interview_enhanced
)
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-065/attempt-01/sql/S40.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-065/attempt-01/sql/S40.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-065/attempt-01/results/S40.rows.jsonl)；完整：True；SHA256：`58b26c8cf9aa900adbe760a91fadf0b7a2247e0ab031c70b7c4d6e81eea9708e`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "greenhouse__interview_enhanced", "kind": "base", "block": null, "base_tables": ["greenhouse__interview_enhanced"]}] | [] | [] |
| B2 | [{"alias": "", "kind": "derived", "block": "B1", "base_tables": ["greenhouse__interview_enhanced"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B2 | COUNT(*) | [] | [] | True |


## S41

类别 `data`；来源 `python`；调用 `b83f0728629f43c393d428b7f740e139`；状态 `success`。

```sql

WITH cat AS (
  SELECT application_id,
    CASE
      WHEN candidate_company IN ('Meta','Apple','Amazon','Netflix','Google','Alphabet') THEN 'FAANG'
      WHEN candidate_company IN ('Adobe','Airbnb','Atlassian','ByteDance','Canva','Coinbase','CrowdStrike','Databricks','Datadog','Discord','DocuSign','Dropbox','eBay','Epic Games','Figma','Instacart','IBM','Intel','Klarna','LinkedIn','Microsoft','MongoDB','Nvidia','Notion','Nubank','Okta','Oracle','Palantir','PayPal','Pinterest','Revolut','Robinhood','Salesforce','ServiceNow','Shopify','Slack','Snap','Snowflake','Spotify','Square','Stripe','Tesla','Twilio','Twitter','Uber','Zoom') THEN 'Major_Tech'
      ELSE 'Traditional'
    END AS company_cat
  FROM greenhouse__application_enhanced
),
app_agg AS (
  SELECT i.application_id,
         cat.company_cat,
         AVG(i.technical_score) AS avg_tech,
         AVG(i.problem_solving_score) AS avg_ps,
         AVG(i.communication_score) AS avg_comm,
         AVG(i.culture_fit_score) AS avg_cf,
         AVG(i.leadership_score) AS avg_lead,
         MAX(CASE WHEN i.overall_recommendation IN ('strong_yes','yes') THEN 1.0 ELSE 0.0 END) AS ever_pos_rec,
         COUNT(*) AS n_interviews
  FROM greenhouse__interview_enhanced i
  JOIN cat ON cat.application_id = i.application_id
  GROUP BY i.application_id
)
SELECT * FROM app_agg

```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-065/attempt-01/sql/S41.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-065/attempt-01/sql/S41.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-065/attempt-01/results/S41.rows.jsonl)；完整：True；SHA256：`11108934b5600e2c188d15b20e5c28b6e4338aa9f91ea3f4b9ee1f4dba73eda3`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "greenhouse__application_enhanced", "kind": "base", "block": null, "base_tables": ["greenhouse__application_enhanced"]}] | [] | [] |
| B2 | [{"alias": "cat", "kind": "derived", "block": "B1", "base_tables": ["greenhouse__application_enhanced"]}, {"alias": "i", "kind": "base", "block": null, "base_tables": ["greenhouse__interview_enhanced"]}] | [{"type": "INNER", "right": "cat", "on": "cat.application_id = i.application_id", "using": []}] | ["i.application_id"] |
| B3 | [{"alias": "app_agg", "kind": "derived", "block": "B2", "base_tables": ["greenhouse__application_enhanced", "greenhouse__interview_enhanced"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B2 | AVG(i.technical_score) | [{"table": "greenhouse__interview_enhanced", "column": "technical_score"}] | [] | False |
| B2 | AVG(i.problem_solving_score) | [{"table": "greenhouse__interview_enhanced", "column": "problem_solving_score"}] | [] | False |
| B2 | AVG(i.communication_score) | [{"table": "greenhouse__interview_enhanced", "column": "communication_score"}] | [] | False |
| B2 | AVG(i.culture_fit_score) | [{"table": "greenhouse__interview_enhanced", "column": "culture_fit_score"}] | [] | False |
| B2 | AVG(i.leadership_score) | [{"table": "greenhouse__interview_enhanced", "column": "leadership_score"}] | [] | False |
| B2 | MAX(CASE WHEN i.overall_recommendation IN ('strong_yes', 'yes') THEN 1.0 ELSE 0.0 END) | [] | [{"table": "greenhouse__interview_enhanced", "column": "overall_recommendation"}] | False |
| B2 | COUNT(*) | [] | [] | True |


## S42

类别 `data`；来源 `python`；调用 `bbc7dcb0541448fb9dec1b732373d0b4`；状态 `success`。

```sql

WITH cat AS (
  SELECT application_id, candidate_company, education_level, years_of_experience, skill_count, university_tier,
    CASE
      WHEN candidate_company IN ('Meta','Apple','Amazon','Netflix','Google','Alphabet') THEN 'FAANG'
      WHEN candidate_company IN ('Adobe','Airbnb','Atlassian','ByteDance','Canva','Coinbase','CrowdStrike','Databricks','Datadog','Discord','DocuSign','Dropbox','eBay','Epic Games','Figma','Instacart','IBM','Intel','Klarna','LinkedIn','Microsoft','MongoDB','Nvidia','Notion','Nubank','Okta','Oracle','Palantir','PayPal','Pinterest','Revolut','Robinhood','Salesforce','ServiceNow','Shopify','Slack','Snap','Snowflake','Spotify','Square','Stripe','Tesla','Twilio','Twitter','Uber','Zoom') THEN 'Major_Tech'
      ELSE 'Traditional'
    END AS company_cat
  FROM greenhouse__application_enhanced
),
app_agg AS (
  SELECT i.application_id,
         cat.company_cat,
         cat.education_level,
         cat.years_of_experience,
         cat.skill_count,
         cat.university_tier,
         AVG(i.technical_score) AS avg_tech,
         AVG(i.problem_solving_score) AS avg_ps,
         AVG(i.communication_score) AS avg_comm,
         AVG(i.culture_fit_score) AS avg_cf,
         AVG(i.leadership_score) AS avg_lead,
         MAX(CASE WHEN i.overall_recommendation IN ('strong_yes','yes') THEN 1.0 ELSE 0.0 END) AS ever_pos_rec,
         COUNT(*) AS n_interviews
  FROM greenhouse__interview_enhanced i
  JOIN cat ON cat.application_id = i.application_id
  GROUP BY i.application_id
)
SELECT * FROM app_agg

```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-065/attempt-01/sql/S42.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-065/attempt-01/sql/S42.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-065/attempt-01/results/S42.rows.jsonl)；完整：True；SHA256：`1be7ebf4cf695171f92be545c5e1d22c5e28d8c0178275217552f58203450fe4`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "greenhouse__application_enhanced", "kind": "base", "block": null, "base_tables": ["greenhouse__application_enhanced"]}] | [] | [] |
| B2 | [{"alias": "cat", "kind": "derived", "block": "B1", "base_tables": ["greenhouse__application_enhanced"]}, {"alias": "i", "kind": "base", "block": null, "base_tables": ["greenhouse__interview_enhanced"]}] | [{"type": "INNER", "right": "cat", "on": "cat.application_id = i.application_id", "using": []}] | ["i.application_id"] |
| B3 | [{"alias": "app_agg", "kind": "derived", "block": "B2", "base_tables": ["greenhouse__application_enhanced", "greenhouse__interview_enhanced"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B2 | AVG(i.technical_score) | [{"table": "greenhouse__interview_enhanced", "column": "technical_score"}] | [] | False |
| B2 | AVG(i.problem_solving_score) | [{"table": "greenhouse__interview_enhanced", "column": "problem_solving_score"}] | [] | False |
| B2 | AVG(i.communication_score) | [{"table": "greenhouse__interview_enhanced", "column": "communication_score"}] | [] | False |
| B2 | AVG(i.culture_fit_score) | [{"table": "greenhouse__interview_enhanced", "column": "culture_fit_score"}] | [] | False |
| B2 | AVG(i.leadership_score) | [{"table": "greenhouse__interview_enhanced", "column": "leadership_score"}] | [] | False |
| B2 | MAX(CASE WHEN i.overall_recommendation IN ('strong_yes', 'yes') THEN 1.0 ELSE 0.0 END) | [] | [{"table": "greenhouse__interview_enhanced", "column": "overall_recommendation"}] | False |
| B2 | COUNT(*) | [] | [] | True |


## S43

类别 `data`；来源 `python`；调用 `bbc7dcb0541448fb9dec1b732373d0b4`；状态 `success`。

```sql

WITH cat AS (
  SELECT application_id,
    CASE
      WHEN candidate_company IN ('Meta','Apple','Amazon','Netflix','Google','Alphabet') THEN 'FAANG'
      WHEN candidate_company IN ('Adobe','Airbnb','Atlassian','ByteDance','Canva','Coinbase','CrowdStrike','Databricks','Datadog','Discord','DocuSign','Dropbox','eBay','Epic Games','Figma','Instacart','IBM','Intel','Klarna','LinkedIn','Microsoft','MongoDB','Nvidia','Notion','Nubank','Okta','Oracle','Palantir','PayPal','Pinterest','Revolut','Robinhood','Salesforce','ServiceNow','Shopify','Slack','Snap','Snowflake','Spotify','Square','Stripe','Tesla','Twilio','Twitter','Uber','Zoom') THEN 'Major_Tech'
      ELSE 'Traditional'
    END AS company_cat
  FROM greenhouse__application_enhanced
)
SELECT cat.company_cat,
       COUNT(*) AS n_apps,
       SUM(a.stage_offer) AS reached_offer,
       SUM(a.stage_hired) AS hired,
       AVG(CAST(a.stage_offer AS FLOAT)) AS offer_rate,
       AVG(CAST(a.stage_hired AS FLOAT)) AS hire_rate
FROM greenhouse__application_enhanced a
JOIN cat ON cat.application_id = a.application_id
WHERE a.stage_technical_interview = 1
GROUP BY cat.company_cat
ORDER BY offer_rate DESC

```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-065/attempt-01/sql/S43.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-065/attempt-01/sql/S43.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-065/attempt-01/results/S43.rows.jsonl)；完整：True；SHA256：`6a8131012a9803cfcabb8a757cb18c39cfdc3faa7b1b7fd2208d4cbbcf70f623`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "greenhouse__application_enhanced", "kind": "base", "block": null, "base_tables": ["greenhouse__application_enhanced"]}] | [] | [] |
| B2 | [{"alias": "cat", "kind": "derived", "block": "B1", "base_tables": ["greenhouse__application_enhanced"]}, {"alias": "a", "kind": "base", "block": null, "base_tables": ["greenhouse__application_enhanced"]}] | [{"type": "INNER", "right": "cat", "on": "cat.application_id = a.application_id", "using": []}] | ["cat.company_cat"] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B2 | COUNT(*) | [] | [] | True |
| B2 | SUM(a.stage_offer) | [{"table": "greenhouse__application_enhanced", "column": "stage_offer"}] | [] | False |
| B2 | SUM(a.stage_hired) | [{"table": "greenhouse__application_enhanced", "column": "stage_hired"}] | [] | False |
| B2 | AVG(CAST(a.stage_offer AS REAL)) | [{"table": "greenhouse__application_enhanced", "column": "stage_offer"}] | [] | False |
| B2 | AVG(CAST(a.stage_hired AS REAL)) | [{"table": "greenhouse__application_enhanced", "column": "stage_hired"}] | [] | False |


## S44

类别 `data`；来源 `query_db`；调用 `f593c18f899a48299cdc53cdbf78c8c5`；状态 `success`。

```sql
SELECT stage_technical_interview, COUNT(*) AS n FROM greenhouse__application_enhanced GROUP BY stage_technical_interview
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-065/attempt-01/sql/S44.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-065/attempt-01/sql/S44.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-065/attempt-01/results/S44.rows.jsonl)；完整：True；SHA256：`84740e53e2917febc942fd007e72b6dbf650a26260aa65e7d826f59b285b5d9b`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "greenhouse__application_enhanced", "kind": "base", "block": null, "base_tables": ["greenhouse__application_enhanced"]}] | [] | ["stage_technical_interview"] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |


## S45

类别 `data`；来源 `query_db`；调用 `336ce932972a4819801255b113e0f643`；状态 `success`。

```sql
WITH cat AS (
  SELECT application_id,
    CASE
      WHEN candidate_company IN ('Meta','Apple','Amazon','Netflix','Google','Alphabet') THEN 'FAANG'
      WHEN candidate_company IN ('Adobe','Airbnb','Atlassian','ByteDance','Canva','Coinbase','CrowdStrike','Databricks','Datadog','Discord','DocuSign','Dropbox','eBay','Epic Games','Figma','Instacart','IBM','Intel','Klarna','LinkedIn','Microsoft','MongoDB','Nvidia','Notion','Nubank','Okta','Oracle','Palantir','PayPal','Pinterest','Revolut','Robinhood','Salesforce','ServiceNow','Shopify','Slack','Snap','Snowflake','Spotify','Square','Stripe','Tesla','Twilio','Twitter','Uber','Zoom') THEN 'Major_Tech'
      ELSE 'Traditional'
    END AS company_cat
  FROM greenhouse__application_enhanced
)
SELECT cat.company_cat,
       COUNT(*) AS n_apps,
       SUM(a.stage_offer) AS reached_offer,
       SUM(a.stage_hired) AS hired,
       AVG(CAST(a.stage_offer AS FLOAT)) AS offer_rate,
       AVG(CAST(a.stage_hired AS FLOAT)) AS hire_rate
FROM greenhouse__application_enhanced a
JOIN cat ON cat.application_id = a.application_id
WHERE a.stage_technical_interview = 1
GROUP BY cat.company_cat
ORDER BY offer_rate DESC
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-065/attempt-01/sql/S45.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-065/attempt-01/sql/S45.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-065/attempt-01/results/S45.rows.jsonl)；完整：True；SHA256：`6a8131012a9803cfcabb8a757cb18c39cfdc3faa7b1b7fd2208d4cbbcf70f623`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "greenhouse__application_enhanced", "kind": "base", "block": null, "base_tables": ["greenhouse__application_enhanced"]}] | [] | [] |
| B2 | [{"alias": "cat", "kind": "derived", "block": "B1", "base_tables": ["greenhouse__application_enhanced"]}, {"alias": "a", "kind": "base", "block": null, "base_tables": ["greenhouse__application_enhanced"]}] | [{"type": "INNER", "right": "cat", "on": "cat.application_id = a.application_id", "using": []}] | ["cat.company_cat"] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B2 | COUNT(*) | [] | [] | True |
| B2 | SUM(a.stage_offer) | [{"table": "greenhouse__application_enhanced", "column": "stage_offer"}] | [] | False |
| B2 | SUM(a.stage_hired) | [{"table": "greenhouse__application_enhanced", "column": "stage_hired"}] | [] | False |
| B2 | AVG(CAST(a.stage_offer AS REAL)) | [{"table": "greenhouse__application_enhanced", "column": "stage_offer"}] | [] | False |
| B2 | AVG(CAST(a.stage_hired AS REAL)) | [{"table": "greenhouse__application_enhanced", "column": "stage_hired"}] | [] | False |


## S46

类别 `data`；来源 `query_db`；调用 `2db4d2380d764e86ae386b91e1a25083`；状态 `failed`。

```sql
SELECT stage_technical_interview, COUNT(*) AS n FROM greenSchouse__application_enhanced GROUP BY stage_technical_interview
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-065/attempt-01/sql/S46.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-065/attempt-01/sql/S46.parameters.json)。

错误：`OperationalError('no such table: greenSchouse__application_enhanced')`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "greenSchouse__application_enhanced", "kind": "base", "block": null, "base_tables": ["greenSchouse__application_enhanced"]}] | [] | ["stage_technical_interview"] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |


未解析列血缘：[{"block": "B1", "column": "stage_technical_interview", "reason": "ambiguous_or_missing_source"}, {"block": "B1", "column": "stage_technical_interview", "reason": "ambiguous_or_missing_source"}, {"block": "B1", "column": "stage_technical_interview", "reason": "ambiguous_or_missing_source"}]

## S47

类别 `data`；来源 `query_db`；调用 `64da3334563d4b209ddcf2e9d6dd0120`；状态 `success`。

```sql
SELECT stage_technical_interview, COUNT(*) AS n 
FROM greenhouse__application_enhanced 
WHERE stage_technical_interview = 1
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-065/attempt-01/sql/S47.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-065/attempt-01/sql/S47.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-065/attempt-01/results/S47.rows.jsonl)；完整：True；SHA256：`3933c7bd2a1768e4268262f189ba0f420c2684bddbf05ebae663e474f595f31b`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "greenhouse__application_enhanced", "kind": "base", "block": null, "base_tables": ["greenhouse__application_enhanced"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |


## S48

类别 `data`；来源 `query_db`；调用 `a6d3861ca9894149b4a0a6d94fc08344`；状态 `success`。

```sql
SELECT DISTINCT stage_technical_interview FROM greenhouse__application_enhanced
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-065/attempt-01/sql/S48.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-065/attempt-01/sql/S48.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-065/attempt-01/results/S48.rows.jsonl)；完整：True；SHA256：`2786b6182c9fb1369cbd71e3d89dd5747c4184a638ed9612cdbe129a87a39736`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "greenhouse__application_enhanced", "kind": "base", "block": null, "base_tables": ["greenhouse__application_enhanced"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |


## S49

类别 `data`；来源 `query_db`；调用 `e7b927e2e86e417bb3438bd62785427e`；状态 `success`。

```sql
SELECT COUNT(*) AS total, COUNT(DISTINCT application_id) AS distinct_apps FROM greenhouse__application_enhanced
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-065/attempt-01/sql/S49.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-065/attempt-01/sql/S49.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-065/attempt-01/results/S49.rows.jsonl)；完整：True；SHA256：`33c79d633ee73d687a05b234870b5fbb041c42182914bcdcc18bbe663b420be2`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "greenhouse__application_enhanced", "kind": "base", "block": null, "base_tables": ["greenhouse__application_enhanced"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |
| B1 | COUNT(DISTINCT application_id) | [{"table": "greenhouse__application_enhanced", "column": "application_id"}] | [] | False |


## S50

类别 `data`；来源 `query_db`；调用 `081715ce2c56405c9adce002346b004f`；状态 `success`。

```sql
WITH cat AS (
  SELECT application_id,
    CASE
      WHEN candidate_company IN ('Meta','Apple','Amazon','Netflix','Google','Alphabet') THEN 'FAANG'
      WHEN candidate_company IN ('Adobe','Airbnb','Atlassian','ByteDance','Canva','Coinbase','CrowdStrike','Databricks','Datadog','Discord','DocuSign','Dropbox','eBay','Epic Games','Figma','Instacart','IBM','Intel','Klarna','LinkedIn','Microsoft','MongoDB','Nvidia','Notion','Nubank','Okta','Oracle','Palantir','PayPal','Pinterest','Revolut','Robinhood','Salesforce','ServiceNow','Shopify','Slack','Snap','Snowflake','Spotify','Square','Stripe','Tesla','Twilio','Twitter','Uber','Zoom') THEN 'Major_Tech'
      ELSE 'Traditional'
    END AS company_cat
  FROM greenhouse__application_enhanced
)
SELECT COUNT(*) AS n, COUNT(DISTINCT application_id) AS distinct_ids FROM cat
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-065/attempt-01/sql/S50.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-065/attempt-01/sql/S50.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-065/attempt-01/results/S50.rows.jsonl)；完整：True；SHA256：`33c79d633ee73d687a05b234870b5fbb041c42182914bcdcc18bbe663b420be2`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "greenhouse__application_enhanced", "kind": "base", "block": null, "base_tables": ["greenhouse__application_enhanced"]}] | [] | [] |
| B2 | [{"alias": "cat", "kind": "derived", "block": "B1", "base_tables": ["greenhouse__application_enhanced"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B2 | COUNT(*) | [] | [] | True |
| B2 | COUNT(DISTINCT application_id) | [{"table": "greenhouse__application_enhanced", "column": "application_id"}] | [] | False |


## S51

类别 `data`；来源 `query_db`；调用 `e431035127a84483a1354f92e5ee8416`；状态 `success`。

```sql
WITH cat AS (
  SELECT DISTINCT application_id,
    CASE
      WHEN candidate_company IN ('Meta','Apple','Amazon','Netflix','Google','Alphabet') THEN 'FAANG'
      WHEN candidate_company IN ('Adobe','Airbnb','Atlassian','ByteDance','Canva','Coinbase','CrowdStrike','Databricks','Datadog','Discord','DocuSign','Dropbox','eBay','Epic Games','Figma','Instacart','IBM','Intel','Klarna','LinkedIn','Microsoft','MongoDB','Nvidia','Notion','Nubank','Okta','Oracle','Palantir','PayPal','Pinterest','Revolut','Robinhood','Salesforce','ServiceNow','Shopify','Slack','Snap','Snowflake','Spotify','Square','Stripe','Tesla','Twilio','Twitter','Uber','Zoom') THEN 'Major_Tech'
      ELSE 'Traditional'
    END AS company_cat
  FROM greenhouse__application_enhanced
)
SELECT cat.company_cat,
       COUNT(*) AS n_apps,
       SUM(a.stage_offer) AS reached_offer,
       SUM(a.stage_hired) AS hired,
       AVG(CAST(a.stage_offer AS FLOAT)) AS offer_rate,
       AVG(CAST(a.stage_hired AS FLOAT)) AS hire_rate
FROM (SELECT DISTINCT application_id, stage_offer, stage_hired, stage_technical_interview FROM greenhouse__application_enhanced) a
JOIN cat ON cat.application_id = a.application_id
WHERE a.stage_technical_interview = 1
GROUP BY cat.company_cat
ORDER BY offer_rate DESC
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-065/attempt-01/sql/S51.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-065/attempt-01/sql/S51.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-065/attempt-01/results/S51.rows.jsonl)；完整：True；SHA256：`812212478641044b7f44dfed46389b39c3e8f5be97aa41c1868bbdf1d9c6c48b`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "greenhouse__application_enhanced", "kind": "base", "block": null, "base_tables": ["greenhouse__application_enhanced"]}] | [] | [] |
| B2 | [{"alias": "greenhouse__application_enhanced", "kind": "base", "block": null, "base_tables": ["greenhouse__application_enhanced"]}] | [] | [] |
| B3 | [{"alias": "cat", "kind": "derived", "block": "B1", "base_tables": ["greenhouse__application_enhanced"]}, {"alias": "a", "kind": "derived", "block": "B2", "base_tables": ["greenhouse__application_enhanced"]}] | [{"type": "INNER", "right": "cat", "on": "cat.application_id = a.application_id", "using": []}] | ["cat.company_cat"] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B3 | COUNT(*) | [] | [] | True |
| B3 | SUM(a.stage_offer) | [{"table": "greenhouse__application_enhanced", "column": "stage_offer"}] | [] | False |
| B3 | SUM(a.stage_hired) | [{"table": "greenhouse__application_enhanced", "column": "stage_hired"}] | [] | False |
| B3 | AVG(CAST(a.stage_offer AS REAL)) | [{"table": "greenhouse__application_enhanced", "column": "stage_offer"}] | [] | False |
| B3 | AVG(CAST(a.stage_hired AS REAL)) | [{"table": "greenhouse__application_enhanced", "column": "stage_hired"}] | [] | False |


## S52

类别 `data`；来源 `python`；调用 `24685cdb492b4da19018e46d9563b3c4`；状态 `success`。

```sql

SELECT DISTINCT a.application_id, a.candidate_gender, a.candidate_race, 
       a.candidate_disability_status, a.candidate_veteran_status,
       a.stage_offer, a.stage_hired, a.status
FROM greenhouse__application_enhanced a

```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-065/attempt-01/sql/S52.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-065/attempt-01/sql/S52.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-065/attempt-01/results/S52.rows.jsonl)；完整：True；SHA256：`0e2c11d2a1a571344b1fb67fd20649967a857829a653c9484f302d90df9958b5`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "a", "kind": "base", "block": null, "base_tables": ["greenhouse__application_enhanced"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |


## S53

类别 `data`；来源 `python`；调用 `24685cdb492b4da19018e46d9563b3c4`；状态 `success`。

```sql

SELECT DISTINCT i.application_id, i.interview_id, i.interviewer_user_id,
       i.technical_score, i.problem_solving_score, i.communication_score,
       i.culture_fit_score, i.leadership_score, i.overall_recommendation,
       i.candidate_gender, i.candidate_race, i.candidate_disability_status, i.candidate_veteran_status,
       i.interviewer_gender, i.interviewer_level, i.interviewer_experience_years,
       i.interview_time_of_day, i.interview_day_of_week, i.interview_season,
       i.interview_duration_minutes, i.interviewer_is_hiring_manager,
       i.follow_up_questions_count, i.interviewer_satisfaction
FROM greenhouse__interview_enhanced i
WHERE i.technical_score IS NOT NULL

```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-065/attempt-01/sql/S53.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-065/attempt-01/sql/S53.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-065/attempt-01/results/S53.rows.jsonl)；完整：True；SHA256：`12aae86553617ed7c60622bd01a3ddb73673dcdc5f0b0568e7cd67dc685baae3`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "i", "kind": "base", "block": null, "base_tables": ["greenhouse__interview_enhanced"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |


## S54

类别 `data`；来源 `python`；调用 `24685cdb492b4da19018e46d9563b3c4`；状态 `success`。

```sql

SELECT DISTINCT a.application_id,
  CASE
    WHEN a.candidate_company IN ('Meta','Apple','Amazon','Netflix','Google','Alphabet') THEN 'FAANG'
    WHEN a.candidate_company IN ('Adobe','Airbnb','Atlassian','ByteDance','Canva','Coinbase','CrowdStrike','Databricks','Datadog','Discord','DocuSign','Dropbox','eBay','Epic Games','Figma','Instacart','IBM','Intel','Klarna','LinkedIn','Microsoft','MongoDB','Nvidia','Notion','Nubank','Okta','Oracle','Palantir','PayPal','Pinterest','Revolut','Robinhood','Salesforce','ServiceNow','Shopify','Slack','Snap','Snowflake','Spotify','Square','Stripe','Tesla','Twilio','Twitter','Uber','Zoom') THEN 'Major_Tech'
    ELSE 'Traditional'
  END AS company_cat,
  a.candidate_gender
FROM greenhouse__application_enhanced a

```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-065/attempt-01/sql/S54.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-065/attempt-01/sql/S54.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-065/attempt-01/results/S54.rows.jsonl)；完整：True；SHA256：`1ee246e034dadaa316d9a04bcca451e5b3b6ab9b7cff93d75365a10b08624b6b`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "a", "kind": "base", "block": null, "base_tables": ["greenhouse__application_enhanced"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |


## S55

类别 `data`；来源 `python`；调用 `24685cdb492b4da19018e46d9563b3c4`；状态 `success`。

```sql

SELECT DISTINCT a.application_id,
  CASE
    WHEN a.candidate_company IN ('Meta','Apple','Amazon','Netflix','Google','Alphabet') THEN 'FAANG'
    WHEN a.candidate_company IN ('Adobe','Airbnb','Atlassian','ByteDance','Canva','Coinbase','CrowdStrike','Databricks','Datadog','Discord','DocuSign','Dropbox','eBay','Epic Games','Figma','Instacart','IBM','Intel','Klarna','LinkedIn','Microsoft','MongoDB','Nvidia','Notion','Nubank','Okta','Oracle','Palantir','PayPal','Pinterest','Revolut','Robinhood','Salesforce','ServiceNow','Shopify','Slack','Snap','Snowflake','Spotify','Square','Stripe','Tesla','Twilio','Twitter','Uber','Zoom') THEN 'Major_Tech'
    ELSE 'Traditional'
  END AS company_cat,
  a.candidate_gender, a.candidate_race, a.education_level, a.years_of_experience,
  a.skill_count, a.university_tier, a.stage_hired
FROM greenhouse__application_enhanced a

```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-065/attempt-01/sql/S55.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-065/attempt-01/sql/S55.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-065/attempt-01/results/S55.rows.jsonl)；完整：True；SHA256：`42f9e45fd3e930bbf5253766bd2f18b13ed5ec67ade7c691af1cbf0cd26ebe20`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "a", "kind": "base", "block": null, "base_tables": ["greenhouse__application_enhanced"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |


## S56

类别 `data`；来源 `python`；调用 `5815637e7ada4576898f360d70e81cb0`；状态 `success`。

```sql

WITH cat AS (
  SELECT application_id, education_level, years_of_experience, skill_count, university_tier,
    CASE
      WHEN candidate_company IN ('Meta','Apple','Amazon','Netflix','Google','Alphabet') THEN 'FAANG'
      WHEN candidate_company IN ('Adobe','Airbnb','Atlassian','ByteDance','Canva','Coinbase','CrowdStrike','Databricks','Datadog','Discord','DocuSign','Dropbox','eBay','Epic Games','Figma','Instacart','IBM','Intel','Klarna','LinkedIn','Microsoft','MongoDB','Nvidia','Notion','Nubank','Okta','Oracle','Palantir','PayPal','Pinterest','Revolut','Robinhood','Salesforce','ServiceNow','Shopify','Slack','Snap','Snowflake','Spotify','Square','Stripe','Tesla','Twilio','Twitter','Uber','Zoom') THEN 'Major_Tech'
      ELSE 'Traditional'
    END AS company_cat
  FROM greenhouse__application_enhanced
),
app_agg AS (
  SELECT i.application_id,
         cat.company_cat, cat.education_level, cat.years_of_experience, cat.skill_count, cat.university_tier,
         AVG(i.technical_score) AS avg_tech,
         AVG(i.problem_solving_score) AS avg_ps,
         AVG(i.communication_score) AS avg_comm,
         AVG(i.culture_fit_score) AS avg_cf,
         AVG(i.leadership_score) AS avg_lead
  FROM greenhouse__interview_enhanced i
  JOIN cat ON cat.application_id = i.application_id
  WHERE i.technical_score IS NOT NULL
  GROUP BY i.application_id
)
SELECT * FROM app_agg

```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-065/attempt-01/sql/S56.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-065/attempt-01/sql/S56.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-065/attempt-01/results/S56.rows.jsonl)；完整：True；SHA256：`83a9617a2f8b0d6394fb63730f77d3f73ebe175d7954c273bf7cef44e446953e`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "greenhouse__application_enhanced", "kind": "base", "block": null, "base_tables": ["greenhouse__application_enhanced"]}] | [] | [] |
| B2 | [{"alias": "cat", "kind": "derived", "block": "B1", "base_tables": ["greenhouse__application_enhanced"]}, {"alias": "i", "kind": "base", "block": null, "base_tables": ["greenhouse__interview_enhanced"]}] | [{"type": "INNER", "right": "cat", "on": "cat.application_id = i.application_id", "using": []}] | ["i.application_id"] |
| B3 | [{"alias": "app_agg", "kind": "derived", "block": "B2", "base_tables": ["greenhouse__application_enhanced", "greenhouse__interview_enhanced"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B2 | AVG(i.technical_score) | [{"table": "greenhouse__interview_enhanced", "column": "technical_score"}] | [] | False |
| B2 | AVG(i.problem_solving_score) | [{"table": "greenhouse__interview_enhanced", "column": "problem_solving_score"}] | [] | False |
| B2 | AVG(i.communication_score) | [{"table": "greenhouse__interview_enhanced", "column": "communication_score"}] | [] | False |
| B2 | AVG(i.culture_fit_score) | [{"table": "greenhouse__interview_enhanced", "column": "culture_fit_score"}] | [] | False |
| B2 | AVG(i.leadership_score) | [{"table": "greenhouse__interview_enhanced", "column": "leadership_score"}] | [] | False |


## S57

类别 `data`；来源 `python`；调用 `5815637e7ada4576898f360d70e81cb0`；状态 `success`。

```sql

WITH cat AS (
  SELECT application_id,
    CASE
      WHEN candidate_company IN ('Meta','Apple','Amazon','Netflix','Google','Alphabet') THEN 'FAANG'
      WHEN candidate_company IN ('Adobe','Airbnb','Atlassian','ByteDance','Canva','Coinbase','CrowdStrike','Databricks','Datadog','Discord','DocuSign','Dropbox','eBay','Epic Games','Figma','Instacart','IBM','Intel','Klarna','LinkedIn','Microsoft','MongoDB','Nvidia','Notion','Nubank','Okta','Oracle','Palantir','PayPal','Pinterest','Revolut','Robinhood','Salesforce','ServiceNow','Shopify','Slack','Snap','Snowflake','Spotify','Square','Stripe','Tesla','Twilio','Twitter','Uber','Zoom') THEN 'Major_Tech'
      ELSE 'Traditional'
    END AS company_cat
  FROM greenhouse__application_enhanced
)
SELECT DISTINCT i.application_id, i.interview_id, i.interviewer_user_id,
       i.technical_score, i.candidate_gender, i.candidate_race,
       i.interviewer_gender, i.interviewer_level,
       cat.company_cat
FROM greenhouse__interview_enhanced i
JOIN cat ON cat.application_id = i.application_id
WHERE i.technical_score IS NOT NULL

```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-065/attempt-01/sql/S57.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-065/attempt-01/sql/S57.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-065/attempt-01/results/S57.rows.jsonl)；完整：True；SHA256：`9e6d1f9fd1cc7a4e5ced05d4e3666f2553613ea52a74b039ea27206021a2bb5a`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "greenhouse__application_enhanced", "kind": "base", "block": null, "base_tables": ["greenhouse__application_enhanced"]}] | [] | [] |
| B2 | [{"alias": "cat", "kind": "derived", "block": "B1", "base_tables": ["greenhouse__application_enhanced"]}, {"alias": "i", "kind": "base", "block": null, "base_tables": ["greenhouse__interview_enhanced"]}] | [{"type": "INNER", "right": "cat", "on": "cat.application_id = i.application_id", "using": []}] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |


## S58

类别 `data`；来源 `python`；调用 `5815637e7ada4576898f360d70e81cb0`；状态 `success`。

```sql

WITH cat AS (
  SELECT DISTINCT a.application_id, a.education_level, a.years_of_experience, a.skill_count, a.university_tier,
    CASE
      WHEN a.candidate_company IN ('Meta','Apple','Amazon','Netflix','Google','Alphabet') THEN 'FAANG'
      WHEN a.candidate_company IN ('Adobe','Airbnb','Atlassian','ByteDance','Canva','Coinbase','CrowdStrike','Databricks','Datadog','Discord','DocuSign','Dropbox','eBay','Epic Games','Figma','Instacart','IBM','Intel','Klarna','LinkedIn','Microsoft','MongoDB','Nvidia','Notion','Nubank','Okta','Oracle','Palantir','PayPal','Pinterest','Revolut','Robinhood','Salesforce','ServiceNow','Shopify','Slack','Snap','Snowflake','Spotify','Square','Stripe','Tesla','Twilio','Twitter','Uber','Zoom') THEN 'Major_Tech'
      ELSE 'Traditional'
    END AS company_cat,
    a.candidate_gender, a.candidate_race
  FROM greenhouse__application_enhanced a
),
app_agg AS (
  SELECT i.application_id,
         cat.company_cat, cat.education_level, cat.years_of_experience, cat.skill_count, cat.university_tier,
         cat.candidate_gender, cat.candidate_race,
         AVG(i.technical_score) AS avg_tech
  FROM greenhouse__interview_enhanced i
  JOIN cat ON cat.application_id = i.application_id
  GROUP BY i.application_id
)
SELECT * FROM app_agg

```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-065/attempt-01/sql/S58.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-065/attempt-01/sql/S58.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-065/attempt-01/results/S58.rows.jsonl)；完整：True；SHA256：`b29cdfe681a169a4ee40bac03a46308a887ada96c30ae197a4738ee788721769`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "a", "kind": "base", "block": null, "base_tables": ["greenhouse__application_enhanced"]}] | [] | [] |
| B2 | [{"alias": "cat", "kind": "derived", "block": "B1", "base_tables": ["greenhouse__application_enhanced"]}, {"alias": "i", "kind": "base", "block": null, "base_tables": ["greenhouse__interview_enhanced"]}] | [{"type": "INNER", "right": "cat", "on": "cat.application_id = i.application_id", "using": []}] | ["i.application_id"] |
| B3 | [{"alias": "app_agg", "kind": "derived", "block": "B2", "base_tables": ["greenhouse__application_enhanced", "greenhouse__interview_enhanced"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B2 | AVG(i.technical_score) | [{"table": "greenhouse__interview_enhanced", "column": "technical_score"}] | [] | False |


## S59

类别 `data`；来源 `python`；调用 `5815637e7ada4576898f360d70e81cb0`；状态 `success`。

```sql

WITH cat AS (
  SELECT DISTINCT application_id,
    CASE
      WHEN candidate_company IN ('Meta','Apple','Amazon','Netflix','Google','Alphabet') THEN 'FAANG'
      WHEN candidate_company IN ('Adobe','Airbnb','Atlassian','ByteDance','Canva','Coinbase','CrowdStrike','Databricks','Datadog','Discord','DocuSign','Dropbox','eBay','Epic Games','Figma','Instacart','IBM','Intel','Klarna','LinkedIn','Microsoft','MongoDB','Nvidia','Notion','Nubank','Okta','Oracle','Palantir','PayPal','Pinterest','Revolut','Robinhood','Salesforce','ServiceNow','Shopify','Slack','Snap','Snowflake','Spotify','Square','Stripe','Tesla','Twilio','Twitter','Uber','Zoom') THEN 'Major_Tech'
      ELSE 'Traditional'
    END AS company_cat
  FROM greenhouse__application_enhanced
)
SELECT cat.company_cat,
  COUNT(*) AS n_apps,
  SUM(CASE WHEN a.stage_application_review=1 THEN 1 ELSE 0 END) AS app_review,
  SUM(CASE WHEN a.stage_phone_screen=1 THEN 1 ELSE 0 END) AS phone_screen,
  SUM(CASE WHEN a.stage_technical_interview=1 THEN 1 ELSE 0 END) AS tech_int,
  SUM(CASE WHEN a.stage_panel_interview=1 THEN 1 ELSE 0 END) AS panel,
  SUM(CASE WHEN a.stage_final_interview=1 THEN 1 ELSE 0 END) AS final_int,
  SUM(CASE WHEN a.stage_offer=1 THEN 1 ELSE 0 END) AS offer,
  SUM(CASE WHEN a.stage_hired=1 THEN 1 ELSE 0 END) AS hired
FROM (SELECT DISTINCT application_id, stage_application_review, stage_phone_screen, stage_technical_interview,
      stage_panel_interview, stage_final_interview, stage_offer, stage_hired
      FROM greenhouse__application_enhanced) a
JOIN cat ON cat.application_id = a.application_id
GROUP BY cat.company_cat
ORDER BY hired DESC

```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-065/attempt-01/sql/S59.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-065/attempt-01/sql/S59.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-065/attempt-01/results/S59.rows.jsonl)；完整：True；SHA256：`be0d1372f632417e0943c847e12ac46c60f3b420d15bc79f6a125e836a607c94`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "greenhouse__application_enhanced", "kind": "base", "block": null, "base_tables": ["greenhouse__application_enhanced"]}] | [] | [] |
| B2 | [{"alias": "greenhouse__application_enhanced", "kind": "base", "block": null, "base_tables": ["greenhouse__application_enhanced"]}] | [] | [] |
| B3 | [{"alias": "cat", "kind": "derived", "block": "B1", "base_tables": ["greenhouse__application_enhanced"]}, {"alias": "a", "kind": "derived", "block": "B2", "base_tables": ["greenhouse__application_enhanced"]}] | [{"type": "INNER", "right": "cat", "on": "cat.application_id = a.application_id", "using": []}] | ["cat.company_cat"] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B3 | COUNT(*) | [] | [] | True |
| B3 | SUM(CASE WHEN a.stage_application_review = 1 THEN 1 ELSE 0 END) | [] | [{"table": "greenhouse__application_enhanced", "column": "stage_application_review"}] | False |
| B3 | SUM(CASE WHEN a.stage_phone_screen = 1 THEN 1 ELSE 0 END) | [] | [{"table": "greenhouse__application_enhanced", "column": "stage_phone_screen"}] | False |
| B3 | SUM(CASE WHEN a.stage_technical_interview = 1 THEN 1 ELSE 0 END) | [] | [{"table": "greenhouse__application_enhanced", "column": "stage_technical_interview"}] | False |
| B3 | SUM(CASE WHEN a.stage_panel_interview = 1 THEN 1 ELSE 0 END) | [] | [{"table": "greenhouse__application_enhanced", "column": "stage_panel_interview"}] | False |
| B3 | SUM(CASE WHEN a.stage_final_interview = 1 THEN 1 ELSE 0 END) | [] | [{"table": "greenhouse__application_enhanced", "column": "stage_final_interview"}] | False |
| B3 | SUM(CASE WHEN a.stage_offer = 1 THEN 1 ELSE 0 END) | [] | [{"table": "greenhouse__application_enhanced", "column": "stage_offer"}] | False |
| B3 | SUM(CASE WHEN a.stage_hired = 1 THEN 1 ELSE 0 END) | [] | [{"table": "greenhouse__application_enhanced", "column": "stage_hired"}] | False |


## S60

类别 `data`；来源 `python`；调用 `b5adb3eb1ccb433180ea8d450829d874`；状态 `success`。

```sql

WITH cat AS (
  SELECT DISTINCT application_id,
    CASE
      WHEN candidate_company IN ('Meta','Apple','Amazon','Netflix','Google','Alphabet') THEN 'FAANG'
      WHEN candidate_company IN ('Adobe','Airbnb','Atlassian','ByteDance','Canva','Coinbase','CrowdStrike','Databricks','Datadog','Discord','DocuSign','Dropbox','eBay','Epic Games','Figma','Instacart','IBM','Intel','Klarna','LinkedIn','Microsoft','MongoDB','Nvidia','Notion','Nubank','Okta','Oracle','Palantir','PayPal','Pinterest','Revolut','Robinhood','Salesforce','ServiceNow','Shopify','Slack','Snap','Snowflake','Spotify','Square','Stripe','Tesla','Twilio','Twitter','Uber','Zoom') THEN 'Major_Tech'
      ELSE 'Traditional'
    END AS company_cat
  FROM greenhouse__application_enhanced
)
SELECT cat.company_cat,
  SUM(CASE WHEN a.stage_application_review=1 THEN 1 ELSE 0 END) AS app_review,
  SUM(CASE WHEN a.stage_phone_screen=1 THEN 1 ELSE 0 END) AS phone_screen,
  SUM(CASE WHEN a.stage_technical_interview=1 THEN 1 ELSE 0 END) AS tech_int,
  SUM(CASE WHEN a.stage_panel_interview=1 THEN 1 ELSE 0 END) AS panel,
  SUM(CASE WHEN a.stage_final_interview=1 THEN 1 ELSE 0 END) AS final_int,
  SUM(CASE WHEN a.stage_offer=1 THEN 1 ELSE 0 END) AS offer,
  SUM(CASE WHEN a.stage_hired=1 THEN 1 ELSE 0 END) AS hired
FROM (SELECT DISTINCT application_id, stage_application_review, stage_phone_screen, stage_technical_interview,
      stage_panel_interview, stage_final_interview, stage_offer, stage_hired
      FROM greenhouse__application_enhanced) a
JOIN cat ON cat.application_id = a.application_id
WHERE a.stage_application_review = 1
GROUP BY cat.company_cat
ORDER BY hired DESC

```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-065/attempt-01/sql/S60.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-065/attempt-01/sql/S60.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-065/attempt-01/results/S60.rows.jsonl)；完整：True；SHA256：`be29a8573ca996d85bd3312a72b8689a90e0d522c1f1ea4d0b27aa9dde4ce9f1`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "greenhouse__application_enhanced", "kind": "base", "block": null, "base_tables": ["greenhouse__application_enhanced"]}] | [] | [] |
| B2 | [{"alias": "greenhouse__application_enhanced", "kind": "base", "block": null, "base_tables": ["greenhouse__application_enhanced"]}] | [] | [] |
| B3 | [{"alias": "cat", "kind": "derived", "block": "B1", "base_tables": ["greenhouse__application_enhanced"]}, {"alias": "a", "kind": "derived", "block": "B2", "base_tables": ["greenhouse__application_enhanced"]}] | [{"type": "INNER", "right": "cat", "on": "cat.application_id = a.application_id", "using": []}] | ["cat.company_cat"] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B3 | SUM(CASE WHEN a.stage_application_review = 1 THEN 1 ELSE 0 END) | [] | [{"table": "greenhouse__application_enhanced", "column": "stage_application_review"}] | False |
| B3 | SUM(CASE WHEN a.stage_phone_screen = 1 THEN 1 ELSE 0 END) | [] | [{"table": "greenhouse__application_enhanced", "column": "stage_phone_screen"}] | False |
| B3 | SUM(CASE WHEN a.stage_technical_interview = 1 THEN 1 ELSE 0 END) | [] | [{"table": "greenhouse__application_enhanced", "column": "stage_technical_interview"}] | False |
| B3 | SUM(CASE WHEN a.stage_panel_interview = 1 THEN 1 ELSE 0 END) | [] | [{"table": "greenhouse__application_enhanced", "column": "stage_panel_interview"}] | False |
| B3 | SUM(CASE WHEN a.stage_final_interview = 1 THEN 1 ELSE 0 END) | [] | [{"table": "greenhouse__application_enhanced", "column": "stage_final_interview"}] | False |
| B3 | SUM(CASE WHEN a.stage_offer = 1 THEN 1 ELSE 0 END) | [] | [{"table": "greenhouse__application_enhanced", "column": "stage_offer"}] | False |
| B3 | SUM(CASE WHEN a.stage_hired = 1 THEN 1 ELSE 0 END) | [] | [{"table": "greenhouse__application_enhanced", "column": "stage_hired"}] | False |


## S61

类别 `data`；来源 `python`；调用 `b5adb3eb1ccb433180ea8d450829d874`；状态 `success`。

```sql

WITH cat AS (
  SELECT application_id, education_level, years_of_experience, skill_count, university_tier,
    CASE
      WHEN candidate_company IN ('Meta','Apple','Amazon','Netflix','Google','Alphabet') THEN 'FAANG'
      WHEN candidate_company IN ('Adobe','Airbnb','Atlassian','ByteDance','Canva','Coinbase','CrowdStrike','Databricks','Datadog','Discord','DocuSign','Dropbox','eBay','Epic Games','Figma','Instacart','IBM','Intel','Klarna','LinkedIn','Microsoft','MongoDB','Nvidia','Notion','Nubank','Okta','Oracle','Palantir','PayPal','Pinterest','Revolut','Robinhood','Salesforce','ServiceNow','Shopify','Slack','Snap','Snowflake','Spotify','Square','Stripe','Tesla','Twilio','Twitter','Uber','Zoom') THEN 'Major_Tech'
      ELSE 'Traditional'
    END AS company_cat
  FROM greenhouse__application_enhanced
),
app_agg AS (
  SELECT i.application_id, cat.company_cat,
         AVG(i.technical_score) AS avg_tech,
         AVG(i.problem_solving_score) AS avg_ps,
         AVG(i.communication_score) AS avg_comm,
         AVG(i.culture_fit_score) AS avg_cf,
         AVG(i.leadership_score) AS avg_lead
  FROM greenhouse__interview_enhanced i
  JOIN cat ON cat.application_id = i.application_id
  GROUP BY i.application_id
)
SELECT * FROM app_agg

```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-065/attempt-01/sql/S61.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-065/attempt-01/sql/S61.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-065/attempt-01/results/S61.rows.jsonl)；完整：True；SHA256：`03a817248b1f9599ee27a3ed60a8b7835fce16024adf3dde97a2c87603676f6b`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "greenhouse__application_enhanced", "kind": "base", "block": null, "base_tables": ["greenhouse__application_enhanced"]}] | [] | [] |
| B2 | [{"alias": "cat", "kind": "derived", "block": "B1", "base_tables": ["greenhouse__application_enhanced"]}, {"alias": "i", "kind": "base", "block": null, "base_tables": ["greenhouse__interview_enhanced"]}] | [{"type": "INNER", "right": "cat", "on": "cat.application_id = i.application_id", "using": []}] | ["i.application_id"] |
| B3 | [{"alias": "app_agg", "kind": "derived", "block": "B2", "base_tables": ["greenhouse__application_enhanced", "greenhouse__interview_enhanced"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B2 | AVG(i.technical_score) | [{"table": "greenhouse__interview_enhanced", "column": "technical_score"}] | [] | False |
| B2 | AVG(i.problem_solving_score) | [{"table": "greenhouse__interview_enhanced", "column": "problem_solving_score"}] | [] | False |
| B2 | AVG(i.communication_score) | [{"table": "greenhouse__interview_enhanced", "column": "communication_score"}] | [] | False |
| B2 | AVG(i.culture_fit_score) | [{"table": "greenhouse__interview_enhanced", "column": "culture_fit_score"}] | [] | False |
| B2 | AVG(i.leadership_score) | [{"table": "greenhouse__interview_enhanced", "column": "leadership_score"}] | [] | False |


## S62

类别 `data`；来源 `python`；调用 `b5adb3eb1ccb433180ea8d450829d874`；状态 `success`。

```sql

SELECT DISTINCT a.application_id,
  CASE
    WHEN a.candidate_company IN ('Meta','Apple','Amazon','Netflix','Google','Alphabet') THEN 'FAANG'
    WHEN a.candidate_company IN ('Adobe','Airbnb','Atlassian','ByteDance','Canva','Coinbase','CrowdStrike','Databricks','Datadog','Discord','DocuSign','Dropbox','eBay','Epic Games','Figma','Instacart','IBM','Intel','Klarna','LinkedIn','Microsoft','MongoDB','Nvidia','Notion','Nubank','Okta','Oracle','Palantir','PayPal','Pinterest','Revolut','Robinhood','Salesforce','ServiceNow','Shopify','Slack','Snap','Snowflake','Spotify','Square','Stripe','Tesla','Twilio','Twitter','Uber','Zoom') THEN 'Major_Tech'
    ELSE 'Traditional'
  END AS company_cat
FROM greenhouse__application_enhanced a

```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-065/attempt-01/sql/S62.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-065/attempt-01/sql/S62.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-065/attempt-01/results/S62.rows.jsonl)；完整：True；SHA256：`7267ed68a169f6c7867d0196d184b5947c87f8870347cd0b4c9d6e9b50c83d92`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "a", "kind": "base", "block": null, "base_tables": ["greenhouse__application_enhanced"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |

