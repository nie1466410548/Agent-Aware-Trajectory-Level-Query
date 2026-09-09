# dacomp-067

The company's CEO has tasked the Human Resources department with developing a comprehensiv…

运行：已提交。官方未评分。全部 SQL 尝试/成功 91/90；数据 SQL 89/88；Python 9 次。

完整原题：

The company's CEO has tasked the Human Resources department with developing a comprehensive strategy for 2024 to improve recruiting efficiency and optimize costs. The analysis must address how to achieve a 15% reduction in total recruitment costs while simultaneously enhancing overall hiring quality. This must be done under the constraints of meeting candidate diversity targets (a female hire representation of no less than 40% and a non-white hire representation of no less than 30%) and maintaining an interviewer satisfaction score above 4.0.

Based on data from the past year, you are required to design a complete recruitment strategy proposal. This proposal should include channel weight allocation, recommendations for optimizing the interview process, and an assessment of the expected ROI. Your analysis must comprehensively consider the differences in hiring needs across various departments, the time efficiency and cost-effectiveness of different sourcing channels, the impact of interviewer's professional background alignment on hiring decisions, and the retention rates of candidates at each stage of the recruitment process.

| 表 | 行数 | 列数 |
| --- | --- | --- |
| greenhouse__application_enhanced | 18186 | 53 |
| greenhouse__candidate_summary | 5201 | 20 |
| greenhouse__diversity_metrics | 1 | 28 |
| greenhouse__interview_enhanced | 14625 | 41 |
| greenhouse__interview_scorecard_detail | 36634 | 18 |
| greenhouse__job_enhanced | 1200 | 27 |
| greenhouse__talent_pipeline_simplified | 8 | 20 |


实际路线（分析者依据 SQL/源码概括，不代表 Agent 自述）：SQL 汇总招聘渠道、成本、流程和多样性 → Python 评分聚合及成本分配情景 → 招聘策略与图表。

数据库大小：26,923,008 字节。

## 数据 SQL

| SQL | 状态 | 基础表 | Join 输入/类型 | GROUP BY | 聚合表达式 | 结果行数 | 数据库 ms |
| --- | --- | --- | --- | --- | --- | --- | --- |
| [S3/Q1](#s3) | success | ["greenhouse__talent_pipeline_simplified"] | 0 / {} | [] | [] | 8 | 0.403 |
| [S4/Q2](#s4) | success | ["greenhouse__diversity_metrics"] | 0 / {} | [] | [] | 1 | 0.379 |
| [S5/Q3](#s5) | success | ["greenhouse__application_enhanced"] | 0 / {} | [] | [] | 20 | 0.414 |
| [S6/Q4](#s6) | success | ["greenhouse__application_enhanced"] | 0 / {} | [] | [] | 4 | 6.826 |
| [S7/Q5](#s7) | success | ["greenhouse__application_enhanced"] | 0 / {} | [] | [] | 141 | 7.911 |
| [S8/Q6](#s8) | success | ["greenhouse__talent_pipeline_simplified"] | 0 / {} | [] | [] | 8 | 0.361 |
| [S9/Q7](#s9) | success | ["greenhouse__interview_enhanced"] | 0 / {} | [] | [] | 10 | 4.478 |
| [S10/Q8](#s10) | success | ["greenhouse__interview_enhanced"] | 0 / {} | [] | [] | 6 | 4.529 |
| [S11/Q9](#s11) | success | ["greenhouse__application_enhanced"] | 0 / {} | ["status"] | ["COUNT(*)"] | 4 | 9.643 |
| [S12/Q10](#s12) | success | ["greenhouse__application_enhanced"] | 0 / {} | ["job_parent_departments"] | ["COUNT(*)", "SUM(CASE WHEN status = 'hired' THEN 1 ELSE 0 END)", "COUNT(*)", "SUM(CASE WHEN status = 'hired' THEN 1 ELSE 0 END)"] | 20 | 9.645 |
| [S13/Q11](#s13) | success | ["greenhouse__application_enhanced"] | 0 / {} | ["candidate_gender"] | ["COUNT(*)", "SUM(CASE WHEN status = 'hired' THEN 1 ELSE 0 END)"] | 4 | 8.046 |
| [S14/Q12](#s14) | success | ["greenhouse__application_enhanced"] | 0 / {} | ["candidate_race"] | ["COUNT(*)", "SUM(CASE WHEN status = 'hired' THEN 1 ELSE 0 END)"] | 6 | 8.268 |
| [S15/Q13](#s15) | success | ["greenhouse__job_enhanced"] | 0 / {} | [] | [] | 20 | 0.801 |
| [S16/Q14](#s16) | success | ["greenhouse__job_enhanced"] | 0 / {} | [] | [] | 20 | 0.446 |
| [S17/Q15](#s17) | success | ["greenhouse__application_enhanced"] | 0 / {} | [] | [] | 6 | 6.648 |
| [S18/Q16](#s18) | success | ["greenhouse__application_enhanced"] | 0 / {} | [] | ["MIN(applied_at)", "MAX(applied_at)", "MIN(candidate_created_at)", "MAX(candidate_created_at)", "COUNT(*)"] | 1 | 8.266 |
| [S19/Q17](#s19) | success | ["greenhouse__application_enhanced"] | 0 / {} | ["sourced_from", "sourced_from_type"] | ["COUNT(*)"] | 4 | 13.335 |
| [S20/Q18](#s20) | success | ["greenhouse__application_enhanced"] | 0 / {} | ["source_id"] | ["COUNT(*)"] | 150 | 8.638 |
| [S21/Q19](#s21) | success | ["greenhouse__application_enhanced"] | 0 / {} | ["source_id", "sourced_from", "sourced_from_type"] | ["COUNT(*)"] | 20 | 16.191 |
| [S22/Q20](#s22) | success | ["greenhouse__application_enhanced"] | 0 / {} | [] | [] | 20 | 9.603 |
| [S23/Q21](#s23) | success | ["greenhouse__application_enhanced"] | 0 / {} | ["sourced_from"] | ["COUNT(*)", "SUM(CASE WHEN source_id <= 8 THEN 1 ELSE 0 END)", "MIN(source_id)", "MAX(source_id)"] | 4 | 12.103 |
| [S24/Q22](#s24) | success | ["greenhouse__application_enhanced"] | 0 / {} | ["candidate_gender", "candidate_race"] | ["COUNT(*)"] | 35 | 7.716 |
| [S25/Q23](#s25) | success | ["greenhouse__application_enhanced"] | 0 / {} | [] | ["COUNT(*)", "SUM(CASE WHEN candidate_gender = 'Female' THEN 1 ELSE 0 END)", "SUM(CASE WHEN candidate_race <> 'White' AND NOT candidate_race IS NULL THEN 1 ELSE 0 END)", "COUNT(*)", "COUNT(*)", "SUM(CASE WHEN candidate_gender = 'Female' THEN 1 ELSE 0 END)", "SUM(CASE WHEN candidate_race <> 'White' AND NOT candidate_race IS NULL THEN 1 ELSE 0 END)"] | 1 | 6.013 |
| [S26/Q24](#s26) | success | ["greenhouse__application_enhanced"] | 0 / {} | ["current_job_stage"] | ["COUNT(*)", "SUM(CASE WHEN status = 'hired' THEN 1 ELSE 0 END)"] | 6 | 11.63 |
| [S27/Q25](#s27) | success | ["greenhouse__interview_enhanced"] | 0 / {} | ["overall_recommendation"] | ["COUNT(*)", "COUNT(DISTINCT interview_id)", "AVG(duration_interview_minutes)", "COUNT(*)"] | 9 | 8.172 |
| [S28/Q26](#s28) | success | ["greenhouse__application_enhanced"] | 0 / {} | ["candidate_gender"] | ["COUNT(*)", "SUM(CASE WHEN status = 'hired' THEN 1 ELSE 0 END)"] | 5 | 13.039 |
| [S29/Q27](#s29) | success | ["greenhouse__application_enhanced"] | 0 / {} | ["candidate_race"] | ["COUNT(*)", "SUM(CASE WHEN status = 'hired' THEN 1 ELSE 0 END)"] | 7 | 13.35 |
| [S30/Q28](#s30) | success | ["greenhouse__application_enhanced"] | 0 / {} | [] | ["COUNT(DISTINCT source_id)"] | 1 | 6.388 |
| [S31/Q29](#s31) | success | ["greenhouse__talent_pipeline_simplified"] | 0 / {} | [] | [] | 8 | 0.321 |
| [S32/Q30](#s32) | success | ["greenhouse__application_enhanced"] | 0 / {} | ["sourced_from"] | ["COUNT(*)", "SUM(CASE WHEN status = 'hired' THEN 1 ELSE 0 END)", "SUM(CASE WHEN status = 'rejected' THEN 1 ELSE 0 END)", "SUM(CASE WHEN status = 'active' THEN 1 ELSE 0 END)", "SUM(CASE WHEN status = 'withdrawn' THEN 1 ELSE 0 END)", "COUNT(*)", "SUM(CASE WHEN status = 'hired' THEN 1 ELSE 0 END)"] | 4 | 14.332 |
| [S33/Q31](#s33) | success | ["greenhouse__application_enhanced"] | 0 / {} | ["job_parent_departments"] | ["COUNT(*)", "SUM(CASE WHEN status = 'hired' THEN 1 ELSE 0 END)", "COUNT(*)", "SUM(CASE WHEN status = 'hired' THEN 1 ELSE 0 END)"] | 15 | 9.214 |
| [S34/Q32](#s34) | success | ["greenhouse__application_enhanced"] | 0 / {} | ["sourced_from"] | ["SUM(CASE WHEN has_interviewed_w_hiring_manager = 1 THEN 1 ELSE 0 END)", "COUNT(*)", "AVG(count_interviews)", "AVG(count_distinct_interviewers)"] | 4 | 8.925 |
| [S35/Q33](#s35) | success | ["greenhouse__application_enhanced"] | 0 / {} | [] | ["MAX(has_interviewed_w_hiring_manager)", "MIN(has_interviewed_w_hiring_manager)", "SUM(has_interviewed_w_hiring_manager)"] | 1 | 6.954 |
| [S36/Q34](#s36) | success | ["greenhouse__interview_scorecard_detail"] | 0 / {} | [] | ["COUNT(*)", "AVG(rating)", "MIN(rating)", "MAX(rating)"] | 1 | 7.091 |
| [S37/Q35](#s37) | success | ["greenhouse__interview_scorecard_detail"] | 0 / {} | ["attribute_category"] | ["COUNT(*)", "AVG(rating)"] | 5 | 21.078 |
| [S38/Q36](#s38) | success | ["greenhouse__interview_scorecard_detail"] | 0 / {} | [] | [] | 7 | 6.697 |
| [S39/Q37](#s39) | success | ["greenhouse__interview_enhanced"] | 0 / {} | ["interviewer_is_hiring_manager"] | ["COUNT(*)", "AVG(duration_interview_minutes)"] | 2 | 8.203 |
| [S40/Q38](#s40) | success | ["greenhouse__interview_enhanced"] | 0 / {} | ["job_parent_departments"] | ["COUNT(*)", "AVG(duration_interview_minutes)", "COUNT(*)", "SUM(CASE WHEN LOWER(overall_recommendation) IN ('strong_yes', 'yes', 'strong yes', 'yes') THEN 1 ELSE 0 END)"] | 15 | 7.96 |
| [S41/Q39](#s41) | success | ["greenhouse__interview_enhanced"] | 0 / {} | ["interview_name"] | ["COUNT(*)", "AVG(duration_interview_minutes)", "SUM(CASE WHEN LOWER(overall_recommendation) IN ('strong_yes', 'yes', 'strong yes', 'yes') THEN 1 ELSE 0 END)", "COUNT(*)"] | 4 | 10.62 |
| [S42/Q40](#s42) | success | ["greenhouse__application_enhanced"] | 0 / {} | ["sourced_from", "current_job_stage"] | ["COUNT(*)", "SUM(CASE WHEN status = 'hired' THEN 1 ELSE 0 END)"] | 24 | 18.706 |
| [S43/Q41](#s43) | success | ["greenhouse__application_enhanced"] | 0 / {} | ["sourced_from"] | ["COUNT(*)", "SUM(CASE WHEN status = 'hired' THEN 1 ELSE 0 END)", "AVG(count_interviews)", "COUNT(*)", "COUNT(*)", "SUM(CASE WHEN status = 'hired' THEN 1 ELSE 0 END)", "SUM(CASE WHEN count_interviews > 0 THEN 1 ELSE 0 END)"] | 4 | 13.593 |
| [S44/Q42](#s44) | success | ["greenhouse__application_enhanced"] | 0 / {} | ["sourced_from"] | ["SUM(CASE WHEN candidate_gender = 'Female' AND status = 'hired' THEN 1 ELSE 0 END)", "SUM(CASE WHEN status = 'hired' THEN 1 ELSE 0 END)", "SUM(CASE WHEN candidate_gender = 'Female' AND status = 'hired' THEN 1 ELSE 0 END)", "SUM(CASE WHEN NOT candidate_gender IS NULL AND status = 'hired' THEN 1 ELSE 0 END)"] | 4 | 14.243 |
| [S45/Q43](#s45) | success | ["greenhouse__application_enhanced"] | 0 / {} | [] | ["COUNT(*)", "SUM(CASE WHEN count_interviews > 0 THEN 1 ELSE 0 END)", "SUM(CASE WHEN status = 'hired' THEN 1 ELSE 0 END)"] | 1 | 7.548 |
| [S46/Q44](#s46) | success | ["greenhouse__application_enhanced"] | 0 / {} | ["sourced_from"] | ["SUM(CASE WHEN candidate_race <> 'White' AND NOT candidate_race IS NULL AND status = 'hired' THEN 1 ELSE 0 END)", "SUM(CASE WHEN status = 'hired' AND NOT candidate_race IS NULL THEN 1 ELSE 0 END)", "SUM(CASE WHEN candidate_race <> 'White' AND NOT candidate_race IS NULL AND status = 'hired' THEN 1 ELSE 0 END)", "SUM(CASE WHEN status = 'hired' AND NOT candidate_race IS NULL THEN 1 ELSE 0 END)"] | 4 | 13.536 |
| [S47/Q45](#s47) | success | ["greenhouse__application_enhanced"] | 0 / {} | ["job_parent_departments"] | ["SUM(CASE WHEN candidate_gender = 'Female' AND status = 'hired' THEN 1 ELSE 0 END)", "SUM(CASE WHEN status = 'hired' AND NOT candidate_gender IS NULL THEN 1 ELSE 0 END)", "SUM(CASE WHEN candidate_gender = 'Female' AND status = 'hired' THEN 1 ELSE 0 END)", "SUM(CASE WHEN status = 'hired' AND NOT candidate_gender IS NULL THEN 1 ELSE 0 END)"] | 15 | 10.232 |
| [S48/Q46](#s48) | success | ["greenhouse__interview_enhanced"] | 0 / {} | [] | [] | 20 | 0.396 |
| [S49/Q47](#s49) | success | ["greenhouse__interview_enhanced"] | 0 / {} | [] | ["COUNT(DISTINCT interviewer_name)", "COUNT(DISTINCT interview_id)"] | 1 | 12.843 |
| [S50/Q48](#s50) | success | ["greenhouse__interview_scorecard_detail"] | 0 / {} | [] | ["AVG(rating)", "AVG(CASE WHEN overall_recommendation IN ('strong_yes', 'yes', 'Strong Yes', 'Yes') THEN rating END)", "AVG(CASE WHEN overall_recommendation IN ('strong_no', 'no', 'Strong No', 'No') THEN rating END)", "AVG(CASE WHEN overall_recommendation = 'Maybe' THEN rating END)"] | 1 | 13.879 |
| [S51/Q49](#s51) | success | ["greenhouse__interview_scorecard_detail"] | 0 / {} | ["attribute_name"] | ["COUNT(*)", "AVG(rating)", "COUNT(*)", "SUM(CASE WHEN rating >= 4 THEN 1 ELSE 0 END)"] | 6 | 15.386 |
| [S52/Q50](#s52) | success | ["greenhouse__interview_enhanced"] | 0 / {} | [] | [] | 5 | 0.334 |
| [S53/Q51](#s53) | failed | ["greenhouse__application_enhanced"] | 0 / {} | ["sourced_from"] | ["COUNT(*)", "AVG(EXTRACT(EPOCH FROM (last_activity_at - applied_at)) / 86400.0)"] | unknown | 未取得；调用总时长 0.119 ms |
| [S54/Q52](#s54) | success | ["greenhouse__application_enhanced", "greenhouse__candidate_summary"] | 2 / {'INNER': 1} | ["status"] | ["COUNT(*)", "AVG(candidate_quality_score)"] | 4 | 27.464 |
| [S55/Q53](#s55) | success | ["greenhouse__application_enhanced"] | 0 / {} | ["sourced_from"] | ["AVG(JULIANDAY(last_activity_at) - JULIANDAY(applied_at))", "MIN(JULIANDAY(last_activity_at) - JULIANDAY(applied_at))", "MAX(JULIANDAY(last_activity_at) - JULIANDAY(applied_at))"] | 4 | 25.346 |
| [S56/Q54](#s56) | success | ["greenhouse__application_enhanced"] | 0 / {} | ["current_job_stage"] | ["COUNT(*)", "AVG(JULIANDAY(last_activity_at) - JULIANDAY(applied_at))"] | 6 | 16.331 |
| [S57/Q55](#s57) | success | ["greenhouse__application_enhanced"] | 0 / {} | ["candidate_gender"] | ["COUNT(*)", "COUNT(*)", "SUM(CASE WHEN status = 'hired' THEN 1 ELSE 0 END)"] | 4 | 8.015 |
| [S58/Q56](#s58) | success | ["greenhouse__application_enhanced", "greenhouse__candidate_summary"] | 2 / {'INNER': 1} | ["CASE WHEN candidate_quality_score >= 4 THEN 'high_quality' ELSE 'low_quality' END"] | ["COUNT(*)", "AVG(candidate_quality_score)", "COUNT(*)", "SUM(CASE WHEN status = 'hired' THEN 1 ELSE 0 END)"] | 2 | 22.63 |
| [S59/Q57](#s59) | success | ["greenhouse__application_enhanced", "greenhouse__candidate_summary"] | 2 / {'INNER': 1} | ["ae.sourced_from"] | ["AVG(cs.candidate_quality_score)", "AVG(cs.avg_interview_score)", "AVG(cs.interview_success_rate)"] | 4 | 25.07 |
| [S60/Q58](#s60) | success | ["greenhouse__candidate_summary"] | 0 / {} | [] | ["COUNT(*)", "SUM(CASE WHEN NOT avg_interview_score IS NULL THEN 1 ELSE 0 END)"] | 1 | 1.391 |
| [S61/Q59](#s61) | success | ["greenhouse__talent_pipeline_simplified"] | 0 / {} | [] | [] | 8 | 0.392 |
| [S62/Q60](#s62) | success | ["greenhouse__application_enhanced"] | 0 / {} | ["CASE WHEN job_parent_departments LIKE '%Engineering%' THEN 'Engineering' WHEN job_parent_departments LIKE '%Product%' THEN 'Product' WHEN job_parent_departments LIKE '%Design%' THEN 'Design' WHEN job_parent_departments LIKE '%Marketing%' THEN 'Marketing' WHEN job_parent_departments LIKE '%Sales%' THEN 'Sales' ELSE 'Other' END"] | ["COUNT(*)", "SUM(CASE WHEN status = 'hired' THEN 1 ELSE 0 END)", "AVG(count_interviews)", "COUNT(*)", "SUM(CASE WHEN status = 'hired' THEN 1 ELSE 0 END)"] | 5 | 12.395 |
| [S63/Q61](#s63) | success | ["greenhouse__application_enhanced"] | 0 / {} | ["sourced_from"] | ["SUM(CASE WHEN status = 'hired' THEN 1 ELSE 0 END)", "COUNT(*)", "COUNT(*)", "SUM(CASE WHEN status = 'hired' THEN 1 ELSE 0 END)"] | 4 | 11.489 |
| [S64/Q62](#s64) | success | ["greenhouse__interview_enhanced"] | 0 / {} | ["CASE WHEN LOWER(overall_recommendation) IN ('strong_yes', 'yes') THEN 'Positive' WHEN LOWER(overall_recommendation) IN ('strong_no', 'no', 'maybe') THEN 'Non-Positive' ELSE 'Other' END"] | ["COUNT(*)"] | 3 | 8.499 |
| [S65/Q63](#s65) | success | ["greenhouse__interview_enhanced"] | 0 / {} | ["interview_name"] | ["COUNT(*)", "AVG(duration_interview_minutes)", "COUNT(*)", "SUM(CASE WHEN LOWER(overall_recommendation) IN ('strong_yes', 'yes') THEN 1 ELSE 0 END)"] | 4 | 7.855 |
| [S66/Q64](#s66) | success | ["greenhouse__interview_scorecard_detail"] | 0 / {} | ["attribute_name"] | ["COUNT(*)", "AVG(rating)"] | 6 | 14.067 |
| [S67/Q65](#s67) | success | ["greenhouse__diversity_metrics"] | 0 / {} | [] | [] | 1 | 0.282 |
| [S68/Q66](#s68) | success | ["greenhouse__application_enhanced"] | 0 / {} | ["current_job_stage"] | ["COUNT(*)", "SUM(CASE WHEN status = 'hired' THEN 1 ELSE 0 END)", "SUM(CASE WHEN status = 'withdrawn' THEN 1 ELSE 0 END)", "SUM(CASE WHEN status = 'rejected' THEN 1 ELSE 0 END)", "SUM(CASE WHEN status = 'active' THEN 1 ELSE 0 END)"] | 6 | 15.297 |
| [S69/Q67](#s69) | success | ["greenhouse__application_enhanced"] | 0 / {} | ["sourced_from"] | ["COUNT(*)", "SUM(CASE WHEN count_interviews > 0 THEN 1 ELSE 0 END)", "SUM(CASE WHEN status = 'hired' THEN 1 ELSE 0 END)"] | 4 | 13.287 |
| [S70/Q68](#s70) | success | ["greenhouse__application_enhanced", "greenhouse__interview_scorecard_detail"] | 0 / {} | [] | [] | 1000 | 34.095 |
| [S71/Q69](#s71) | success | ["greenhouse__application_enhanced"] | 0 / {} | ["CASE WHEN job_parent_departments LIKE '%Engineering%' THEN 'Engineering' WHEN job_parent_departments LIKE '%Product%' THEN 'Product' WHEN job_parent_departments LIKE '%Design%' THEN 'Design' WHEN job_parent_departments LIKE '%Marketing%' THEN 'Marketing' WHEN job_parent_departments LIKE '%Sales%' THEN 'Sales' ELSE 'Other' END"] | ["SUM(CASE WHEN status = 'hired' AND candidate_gender = 'Female' THEN 1 ELSE 0 END)", "SUM(CASE WHEN status = 'hired' AND NOT candidate_gender IS NULL THEN 1 ELSE 0 END)", "SUM(CASE WHEN status = 'hired' AND candidate_race <> 'White' AND NOT candidate_race IS NULL THEN 1 ELSE 0 END)", "SUM(CASE WHEN status = 'hired' AND NOT candidate_race IS NULL THEN 1 ELSE 0 END)"] | 5 | 12.829 |
| [S72/Q70](#s72) | success | ["greenhouse__application_enhanced"] | 0 / {} | ["CASE WHEN job_parent_departments LIKE '%Engineering%' THEN 'Engineering' WHEN job_parent_departments LIKE '%Product%' THEN 'Product' WHEN job_parent_departments LIKE '%Design%' THEN 'Design' WHEN job_parent_departments LIKE '%Marketing%' THEN 'Marketing' WHEN job_parent_departments LIKE '%Sales%' THEN 'Sales' ELSE 'Other' END"] | ["COUNT(*)", "SUM(CASE WHEN status = 'hired' THEN 1 ELSE 0 END)", "COUNT(*)", "SUM(CASE WHEN status = 'hired' THEN 1 ELSE 0 END)"] | 5 | 11.751 |
| [S73/Q71](#s73) | success | ["greenhouse__application_enhanced", "greenhouse__interview_enhanced"] | 2 / {'INNER': 1} | [] | [] | 12932 | 50.868 |
| [S74/Q72](#s74) | success | ["greenhouse__application_enhanced", "greenhouse__interview_enhanced"] | 2 / {'INNER': 1} | [] | [] | 21881 | 52.146 |
| [S75/Q73](#s75) | success | ["greenhouse__application_enhanced"] | 0 / {} | ["current_job_stage"] | ["COUNT(*)", "SUM(CASE WHEN status = 'hired' THEN 1 ELSE 0 END)", "SUM(CASE WHEN status = 'rejected' THEN 1 ELSE 0 END)", "SUM(CASE WHEN status = 'withdrawn' THEN 1 ELSE 0 END)", "SUM(CASE WHEN status = 'active' THEN 1 ELSE 0 END)"] | 6 | 15.375 |
| [S76/Q74](#s76) | success | ["greenhouse__interview_scorecard_detail"] | 0 / {} | ["scd.interview_name"] | ["AVG(scd.rating)", "COUNT(*)", "COUNT(*)", "SUM(CASE WHEN scd.rating >= 4 THEN 1 ELSE 0 END)"] | 4 | 15.272 |
| [S77/Q75](#s77) | success | ["greenhouse__application_enhanced", "greenhouse__interview_enhanced"] | 2 / {'INNER': 1} | ["ie.interview_name"] | ["COUNT(DISTINCT ie.application_id)", "SUM(CASE WHEN ae.status = 'hired' THEN 1 ELSE 0 END)", "COUNT(DISTINCT ie.application_id)", "SUM(CASE WHEN ae.status = 'hired' THEN 1 ELSE 0 END)"] | 4 | 40.465 |
| [S78/Q76](#s78) | success | ["greenhouse__application_enhanced", "greenhouse__interview_enhanced"] | 2 / {'LEFT': 1} | [] | [] | 21881 | 61.717 |
| [S79/Q77](#s79) | success | ["greenhouse__application_enhanced", "greenhouse__interview_scorecard_detail"] | 0 / {} | [] | [] | 29107 | 44187.644 |
| [S80/Q78](#s80) | success | ["greenhouse__interview_scorecard_detail"] | 0 / {} | ["scorecard_id"] | ["AVG(rating)", "MAX(rating)", "MIN(rating)"] | 2738 | 22.818 |
| [S81/Q79](#s81) | success | ["greenhouse__interview_scorecard_detail"] | 0 / {} | ["scd.application_id"] | ["AVG(scd.rating)", "COUNT(scd.scorecard_id)"] | 2852 | 17.258 |
| [S82/Q80](#s82) | success | ["greenhouse__interview_scorecard_detail"] | 0 / {} | [] | ["AVG(rating)"] | 1 | 4.928 |
| [S83/Q81](#s83) | success | ["greenhouse__candidate_summary"] | 0 / {} | [] | ["AVG(avg_interview_score)"] | 1 | 1.078 |
| [S84/Q82](#s84) | success | ["greenhouse__job_enhanced"] | 0 / {} | [] | ["AVG(avg_job_rating)"] | 1 | 0.467 |
| [S85/Q83](#s85) | success | ["greenhouse__interview_scorecard_detail"] | 0 / {} | ["rating"] | ["COUNT(*)"] | 5 | 9.541 |
| [S86/Q84](#s86) | success | ["greenhouse__interview_enhanced"] | 0 / {} | ["CASE WHEN LOWER(overall_recommendation) IN ('strong_yes', 'strong yes') THEN 5 WHEN LOWER(overall_recommendation) IN ('yes') THEN 4 WHEN LOWER(overall_recommendation) IN ('maybe') THEN 3 WHEN LOWER(overall_recommendation) IN ('no') THEN 2 WHEN LOWER(overall_recommendation) IN ('strong_no', 'strong no') THEN 1 ELSE NULL END"] | ["COUNT(*)"] | 5 | 10.025 |
| [S87/Q85](#s87) | success | ["greenhouse__interview_enhanced"] | 0 / {} | ["interview_name", "status"] | ["COUNT(*)"] | 16 | 11.816 |
| [S88/Q86](#s88) | success | ["greenhouse__application_enhanced"] | 0 / {} | ["count_interviews"] | ["COUNT(*)", "SUM(CASE WHEN status = 'hired' THEN 1 ELSE 0 END)", "COUNT(*)", "SUM(CASE WHEN status = 'hired' THEN 1 ELSE 0 END)"] | 5 | 8.276 |
| [S89/Q87](#s89) | success | ["greenhouse__interview_enhanced"] | 0 / {} | [] | ["COUNT(*)", "SUM(CASE WHEN NOT scorecard_submitted_at IS NULL THEN 1 ELSE 0 END)", "COUNT(*)", "SUM(CASE WHEN NOT scorecard_submitted_at IS NULL THEN 1 ELSE 0 END)"] | 1 | 4.018 |
| [S90/Q88](#s90) | success | ["greenhouse__interview_enhanced"] | 0 / {} | ["status"] | ["COUNT(*)", "COUNT(*)", "COUNT(*)"] | 4 | 8.7 |
| [S91/Q89](#s91) | success | ["greenhouse__interview_enhanced"] | 0 / {} | ["interview_name", "status"] | ["COUNT(*)"] | 16 | 12.258 |


## 元数据和设置

| SQL | 类别 | 状态 | 内容 |
| --- | --- | --- | --- |
| S1 | connection_setup | success | PRAGMA query_only=ON |
| S2 | metadata | success | SELECT name,sql FROM sqlite_master WHERE type='table' ORDER BY name |


## Python 与执行位置

人工源码审查：**database_first_violation**。Python 按推荐和申请状态重算评分均值及高分率，计算对齐人数，并在字面量分配与成本假设上执行常规情景求和。数据库内优先协议也涵盖常规情景算术，因此记录这些偏离；字面量不据此自动认定来自某条 SQL。绘图单独保留。 [证据](../reviews/dacomp-067.json)。

P1：Building a comprehensive cost model and ROI analysis. No cost data exists in the database, so I need to estimate channel costs using industry benchmarks and compute 15% reduction scenarios. Also need to analyze the full pipeline funnel, department-level hiring needs, diversity metrics, and interviewer satisfaction for the strategy proposal.

[源码](../../../runs/dsv4flash-db-first-full-01/dacomp-067/attempt-01/python/P1.py)；[输出](../../../runs/dsv4flash-db-first-full-01/dacomp-067/attempt-01/python/P1.stdout)；[错误](../../../runs/dsv4flash-db-first-full-01/dacomp-067/attempt-01/python/P1.stderr)。检出需人工核验的 SQL 可实现操作：.query(；不能仅凭理由判为合规。

P2：Analyzing funnel retention by stage and channel, plus cost model construction. The database has no cost data, so I need to establish a transparent industry-benchmark cost model and compute scenario impacts in Python (scenario simulation with multiple assumptions and reallocations is better handled outside SQL).

[源码](../../../runs/dsv4flash-db-first-full-01/dacomp-067/attempt-01/python/P2.py)；[输出](../../../runs/dsv4flash-db-first-full-01/dacomp-067/attempt-01/python/P2.stdout)；[错误](../../../runs/dsv4flash-db-first-full-01/dacomp-067/attempt-01/python/P2.stderr)。检出需人工核验的 SQL 可实现操作：.query(；不能仅凭理由判为合规。

P3：Fixed the import error. Now building the comprehensive cost model, funnel analysis, and ROI scenario simulation. No cost data exists in the database, so industry benchmarks are used transparently.

[源码](../../../runs/dsv4flash-db-first-full-01/dacomp-067/attempt-01/python/P3.py)；[输出](../../../runs/dsv4flash-db-first-full-01/dacomp-067/attempt-01/python/P3.stdout)；[错误](../../../runs/dsv4flash-db-first-full-01/dacomp-067/attempt-01/python/P3.stderr)。检出需人工核验的 SQL 可实现操作：.query(；不能仅凭理由判为合规。

P4：Analyzing the impact of interviewer's professional background alignment on hiring decisions. Need to join interview_enhanced with application_enhanced to see if interviewers from the same department as the job are more likely to recommend hiring. This involves string matching of department names which is more practical in Python.

[源码](../../../runs/dsv4flash-db-first-full-01/dacomp-067/attempt-01/python/P4.py)；[输出](../../../runs/dsv4flash-db-first-full-01/dacomp-067/attempt-01/python/P4.stdout)；[错误](../../../runs/dsv4flash-db-first-full-01/dacomp-067/attempt-01/python/P4.stderr)。检出需人工核验的 SQL 可实现操作：groupby(, .query(；不能仅凭理由判为合规。

P5：Creating visualizations for the strategy report. Need to generate charts showing channel performance, cost optimization, diversity metrics, and funnel analysis.

[源码](../../../runs/dsv4flash-db-first-full-01/dacomp-067/attempt-01/python/P5.py)；[输出](../../../runs/dsv4flash-db-first-full-01/dacomp-067/attempt-01/python/P5.stdout)；[错误](../../../runs/dsv4flash-db-first-full-01/dacomp-067/attempt-01/python/P5.stderr)。自动源码筛查未检出预设迁出信号；这不是全面语义合规证明。

P6：Analyzing interviewer professional background alignment with job departments and its impact on hiring decisions. Need to examine whether interviewers from the same department as the job give more positive recommendations and whether scorecards correlate with hire outcomes. This string-matching analysis is better suited for Python.

[源码](../../../runs/dsv4flash-db-first-full-01/dacomp-067/attempt-01/python/P6.py)；[输出](../../../runs/dsv4flash-db-first-full-01/dacomp-067/attempt-01/python/P6.stdout)；[错误](../../../runs/dsv4flash-db-first-full-01/dacomp-067/attempt-01/python/P6.stderr)。检出需人工核验的 SQL 可实现操作：groupby(, .query(；不能仅凭理由判为合规。

P7：Running final comprehensive analysis to compute the optimal channel weights, process optimization recommendations, and expected ROI with all constraints verified.

[源码](../../../runs/dsv4flash-db-first-full-01/dacomp-067/attempt-01/python/P7.py)；[输出](../../../runs/dsv4flash-db-first-full-01/dacomp-067/attempt-01/python/P7.stdout)；[错误](../../../runs/dsv4flash-db-first-full-01/dacomp-067/attempt-01/python/P7.stderr)。自动源码筛查未检出预设迁出信号；这不是全面语义合规证明。

P8：Investigating the "interviewer satisfaction score" metric. The scorecard ratings are 1-5 scale but average 2.70. Let me compute the overall_recommendation mapped to numeric and check if it's above 4.0, or compute the average score per interview to see if aggregating differently yields a score above 4.0.

[源码](../../../runs/dsv4flash-db-first-full-01/dacomp-067/attempt-01/python/P8.py)；[输出](../../../runs/dsv4flash-db-first-full-01/dacomp-067/attempt-01/python/P8.stdout)；[错误](../../../runs/dsv4flash-db-first-full-01/dacomp-067/attempt-01/python/P8.stderr)。检出需人工核验的 SQL 可实现操作：.query(；不能仅凭理由判为合规。

P9：Creating final visualization for interview process efficiency (completion/cancellation rates) and analyzing stage retention by channel for the strategy report.

[源码](../../../runs/dsv4flash-db-first-full-01/dacomp-067/attempt-01/python/P9.py)；[输出](../../../runs/dsv4flash-db-first-full-01/dacomp-067/attempt-01/python/P9.stdout)；[错误](../../../runs/dsv4flash-db-first-full-01/dacomp-067/attempt-01/python/P9.stderr)。自动源码筛查未检出预设迁出信号；这不是全面语义合规证明。

## 优化机会

已验证候选。筛选限于精确 SQL、相同自包含 CTE、相同单表完整过滤、可分解单表聚合；未覆盖任意 Join 等价和一般谓词蕴含。全部候选都是 offline，未测在线预测。

| 候选 | 类型 | 已有结果 | 覆盖 SQL | 后续次数 | 中间行数 | 验证 | 成本 |
| --- | --- | --- | --- | --- | --- | --- | --- |
| C1 | aggregate MV | False | ["S11", "S18", "S19", "S20", "S23", "S26", "S28", "S29", "S32", "S35", "S42", "S43", "S44", "S46", "S63", "S68", "S69", "S75"] | 17 | 11564 | verified | Not benchmarked; correctness alone does not establish net speedup. |
| C2 | common filtered view | False | ["S7", "S12", "S33", "S47", "S62", "S71", "S72"] | 6 | 9233 | verified | Not benchmarked; correctness alone does not establish net speedup. |
| C3 | aggregate MV | False | ["S12", "S33", "S62", "S71", "S72"] | 4 | unknown | not_verified_cap | Not tested |
| C4 | aggregate MV | False | ["S39", "S41", "S87", "S89", "S91"] | 4 | unknown | not_verified_cap | Not tested |
| C5 | common filtered view | False | ["S13", "S57"] | 1 | unknown | not_verified_cap | Not tested |
| C6 | aggregate MV | False | ["S13", "S57"] | 1 | unknown | not_verified_cap | Not tested |
| C7 | common filtered view | False | ["S24", "S25"] | 1 | unknown | not_verified_cap | Not tested |
| C8 | aggregate MV | False | ["S24", "S25"] | 1 | unknown | not_verified_cap | Not tested |
| C9 | common filtered view | False | ["S27", "S48", "S64", "S65", "S86"] | 4 | unknown | not_verified_cap | Not tested |
| C10 | aggregate MV | False | ["S64", "S65", "S86"] | 2 | unknown | not_verified_cap | Not tested |
| C11 | common filtered view | False | ["S34", "S88"] | 1 | unknown | not_verified_cap | Not tested |
| C12 | aggregate MV | False | ["S34", "S88"] | 1 | unknown | not_verified_cap | Not tested |
| C13 | aggregate MV | False | ["S36", "S37"] | 1 | unknown | not_verified_cap | Not tested |
| C14 | common filtered view | False | ["S50", "S80", "S81", "S82", "S85"] | 4 | 29107 | verified | Not benchmarked; correctness alone does not establish net speedup. |
| C15 | aggregate MV | False | ["S50", "S81", "S82", "S85"] | 3 | unknown | not_verified_cap | Not tested |
| C16 | common filtered view | False | ["S51", "S66"] | 1 | unknown | not_verified_cap | Not tested |
| C17 | aggregate MV | False | ["S51", "S66"] | 1 | unknown | not_verified_cap | Not tested |
| C18 | common filtered view | False | ["S55", "S56"] | 1 | unknown | not_verified_cap | Not tested |
| C19 | aggregate MV | False | ["S55", "S56"] | 1 | unknown | not_verified_cap | Not tested |


已验证覆盖（含触发查询、候选并集去重）：30/88 条成功数据 SQL。正确性仅针对当前数据库快照；未测性能的候选不能声称已加速。

[完整 build/rewrite 与比较证据](dacomp-067.analysis.json)。

### C1：aggregate MV

Union of grouping keys; decomposable aggregate states; AVG uses SUM and non-NULL COUNT.

原查询 [S11](#s11), [S18](#s18), [S19](#s19), [S20](#s20), [S23](#s23), [S26](#s26), [S28](#s28), [S29](#s29), [S32](#s32), [S35](#s35), [S42](#s42), [S43](#s43), [S44](#s44), [S46](#s46), [S63](#s63), [S68](#s68), [S69](#s69), [S75](#s75) → 新增共享状态 C1 → 后续 17 次可复用。该构建点为事后假设，不代表 Agent 当时预知后续。

构建定义：

```sql
SELECT status AS __g0, sourced_from AS __g1, sourced_from_type AS __g2, source_id AS __g3, current_job_stage AS __g4, candidate_gender AS __g5, candidate_race AS __g6, COUNT(*) AS __a0, MIN(applied_at) AS __a1, MAX(applied_at) AS __a2, MIN(candidate_created_at) AS __a3, MAX(candidate_created_at) AS __a4, SUM(CASE WHEN source_id <= 8 THEN 1 ELSE 0 END) AS __a5, MIN(source_id) AS __a6, MAX(source_id) AS __a7, SUM(CASE WHEN status = 'hired' THEN 1 ELSE 0 END) AS __a8, SUM(CASE WHEN status = 'rejected' THEN 1 ELSE 0 END) AS __a9, SUM(CASE WHEN status = 'active' THEN 1 ELSE 0 END) AS __a10, SUM(CASE WHEN status = 'withdrawn' THEN 1 ELSE 0 END) AS __a11, MAX(has_interviewed_w_hiring_manager) AS __a12, MIN(has_interviewed_w_hiring_manager) AS __a13, SUM(has_interviewed_w_hiring_manager) AS __a14, SUM(count_interviews) AS __a15_sum, COUNT(count_interviews) AS __a15_n, SUM(CASE WHEN count_interviews > 0 THEN 1 ELSE 0 END) AS __a16, SUM(CASE WHEN candidate_gender = 'Female' AND status = 'hired' THEN 1 ELSE 0 END) AS __a17, SUM(CASE WHEN NOT candidate_gender IS NULL AND status = 'hired' THEN 1 ELSE 0 END) AS __a18, SUM(CASE WHEN candidate_race <> 'White' AND NOT candidate_race IS NULL AND status = 'hired' THEN 1 ELSE 0 END) AS __a19, SUM(CASE WHEN status = 'hired' AND NOT candidate_race IS NULL THEN 1 ELSE 0 END) AS __a20 FROM "greenhouse__application_enhanced"  GROUP BY status, sourced_from, sourced_from_type, source_id, current_job_stage, candidate_gender, candidate_race
```

受益查询 S11 的改写示例：

```sql
SELECT __g0 AS "status", SUM(__a0) AS cnt FROM temp.reuse_candidate GROUP BY __g0
```

| 原 SQL | 列名一致 | 结果一致 | 比较方法 |
| --- | --- | --- | --- |
| S11 | True | True | exact_multiset |
| S18 | True | True | exact_multiset |
| S19 | True | True | ordered_numeric_tolerance |
| S20 | True | True | ordered_numeric_tolerance |
| S23 | True | True | exact_multiset |
| S26 | True | True | ordered_numeric_tolerance |
| S28 | True | True | exact_multiset |
| S29 | True | True | exact_multiset |
| S32 | True | True | ordered_numeric_tolerance |
| S35 | True | True | exact_multiset |
| S42 | True | True | ordered_numeric_tolerance |
| S43 | True | True | ordered_numeric_tolerance |
| S44 | True | True | exact_multiset |
| S46 | True | True | exact_multiset |
| S63 | True | True | ordered_numeric_tolerance |
| S68 | True | True | ordered_numeric_tolerance |
| S69 | True | True | exact_multiset |
| S75 | True | True | ordered_numeric_tolerance |


验证状态：verified；成本结论：Not benchmarked; correctness alone does not establish net speedup.

### C2：common filtered view

Same single source and complete filter; original filter retained.

原查询 [S7](#s7), [S12](#s12), [S33](#s33), [S47](#s47), [S62](#s62), [S71](#s71), [S72](#s72) → 新增共享状态 C2 → 后续 6 次可复用。该构建点为事后假设，不代表 Agent 当时预知后续。

构建定义：

```sql
SELECT * FROM "greenhouse__application_enhanced" WHERE NOT job_parent_departments IS NULL
```

受益查询 S7 的改写示例：

```sql
SELECT DISTINCT job_parent_departments FROM temp.reuse_candidate AS greenhouse__application_enhanced WHERE NOT job_parent_departments IS NULL
```

| 原 SQL | 列名一致 | 结果一致 | 比较方法 |
| --- | --- | --- | --- |
| S7 | True | True | exact_multiset |
| S12 | True | True | ordered_numeric_tolerance |
| S33 | True | True | ordered_numeric_tolerance |
| S47 | True | True | ordered_numeric_tolerance |
| S62 | True | True | ordered_numeric_tolerance |
| S71 | True | True | ordered_numeric_tolerance |
| S72 | True | True | ordered_numeric_tolerance |


验证状态：verified；成本结论：Not benchmarked; correctness alone does not establish net speedup.

### C14：common filtered view

Same single source and complete filter; original filter retained.

原查询 [S50](#s50), [S80](#s80), [S81](#s81), [S82](#s82), [S85](#s85) → 新增共享状态 C14 → 后续 4 次可复用。该构建点为事后假设，不代表 Agent 当时预知后续。

构建定义：

```sql
SELECT * FROM "greenhouse__interview_scorecard_detail" WHERE NOT rating IS NULL
```

受益查询 S50 的改写示例：

```sql
SELECT ROUND(AVG(rating), 2) AS avg_rating, ROUND(AVG(CASE WHEN overall_recommendation IN ('strong_yes', 'yes', 'Strong Yes', 'Yes') THEN rating END), 2) AS avg_positive_rating, ROUND(AVG(CASE WHEN overall_recommendation IN ('strong_no', 'no', 'Strong No', 'No') THEN rating END), 2) AS avg_negative_rating, ROUND(AVG(CASE WHEN overall_recommendation = 'Maybe' THEN rating END), 2) AS avg_maybe_rating FROM temp.reuse_candidate AS greenhouse__interview_scorecard_detail WHERE NOT rating IS NULL
```

| 原 SQL | 列名一致 | 结果一致 | 比较方法 |
| --- | --- | --- | --- |
| S50 | True | True | exact_multiset |
| S80 | True | True | exact_multiset |
| S81 | True | True | exact_multiset |
| S82 | True | True | exact_multiset |
| S85 | True | True | ordered_numeric_tolerance |


验证状态：verified；成本结论：Not benchmarked; correctness alone does not establish net speedup.

结果依赖：自动记录 SQL→Python 的接口父调用，以及源码中引用归档文件的消费者；字面值相同不认定因果。模型方向选择需要人工读取消息，尚未做全面因果标注。

[原始报告](../../../runs/dsv4flash-db-first-full-01/dacomp-067/attempt-01/answer.md)；[统一消息](../../../runs/dsv4flash-db-first-full-01/dacomp-067/attempt-01/messages.jsonl)；[原始 OpenCode 事件](../../../runs/dsv4flash-db-first-full-01/dacomp-067/attempt-01/opencode.jsonl)；[SQL 引擎日志](../../../runs/dsv4flash-db-first-full-01/dacomp-067/attempt-01/sql_journal.jsonl)。

[可读报告（本地图片链接规范化）](../answers/dacomp-067.md)。原始回答保留，分析结论未改写。

## S1

类别 `connection_setup`；来源 `connection`；调用 `9fd889da7a3c4450baa654474118b29b`；状态 `success`。

```sql
PRAGMA query_only=ON
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-067/attempt-01/sql/S1.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-067/attempt-01/sql/S1.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-067/attempt-01/results/S1.rows.jsonl)；完整：True；SHA256：`e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`。

## S2

类别 `metadata`；来源 `list_db`；调用 `9fd889da7a3c4450baa654474118b29b`；状态 `success`。

```sql
SELECT name,sql FROM sqlite_master WHERE type='table' ORDER BY name
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-067/attempt-01/sql/S2.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-067/attempt-01/sql/S2.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-067/attempt-01/results/S2.rows.jsonl)；完整：True；SHA256：`2bcd9726d215ed04e70ce1ede4a770b03abf011b5e4db284a95ba0d8190a1404`。

## S3

类别 `data`；来源 `query_db`；调用 `57f6e4b8fbec45688a0f4649d7935590`；状态 `success`。

```sql
SELECT * FROM greenhouse__talent_pipeline_simplified ORDER BY source_name
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-067/attempt-01/sql/S3.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-067/attempt-01/sql/S3.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-067/attempt-01/results/S3.rows.jsonl)；完整：True；SHA256：`8963974d086d1e72b3f32664617d41aa7cdf0f2e535bf973e0b99746aecb5cbe`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "greenhouse__talent_pipeline_simplified", "kind": "base", "block": null, "base_tables": ["greenhouse__talent_pipeline_simplified"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |


## S4

类别 `data`；来源 `query_db`；调用 `5839828449674506a278e727b702b20b`；状态 `success`。

```sql
SELECT * FROM greenhouse__diversity_metrics ORDER BY application_year, application_quarter
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-067/attempt-01/sql/S4.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-067/attempt-01/sql/S4.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-067/attempt-01/results/S4.rows.jsonl)；完整：True；SHA256：`9538399a73a519b1fd82f02b8ff9f8ecddd385c59835d9c616e397d187395a6f`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "greenhouse__diversity_metrics", "kind": "base", "block": null, "base_tables": ["greenhouse__diversity_metrics"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |


## S5

类别 `data`；来源 `query_db`；调用 `1bf0d21834624d7190dc58d09a2755ba`；状态 `success`。

```sql
SELECT DISTINCT job_departments, job_parent_departments FROM greenhouse__application_enhanced LIMIT 20
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-067/attempt-01/sql/S5.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-067/attempt-01/sql/S5.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-067/attempt-01/results/S5.rows.jsonl)；完整：True；SHA256：`075458cef3c9a313a80d36014e9d4812f71eec543576e40726b2080d347c08ad`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "greenhouse__application_enhanced", "kind": "base", "block": null, "base_tables": ["greenhouse__application_enhanced"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |


## S6

类别 `data`；来源 `query_db`；调用 `c30db8c56bab494a90dd06805af5e48c`；状态 `success`。

```sql
SELECT DISTINCT status FROM greenhouse__application_enhanced
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-067/attempt-01/sql/S6.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-067/attempt-01/sql/S6.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-067/attempt-01/results/S6.rows.jsonl)；完整：True；SHA256：`9454836c1f2946e71159748573eef35eac218f61f333d1e5317e7b789b902dd0`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "greenhouse__application_enhanced", "kind": "base", "block": null, "base_tables": ["greenhouse__application_enhanced"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |


## S7

类别 `data`；来源 `query_db`；调用 `9731d858ed694fe5976df538442ea336`；状态 `success`。

```sql
SELECT DISTINCT job_parent_departments FROM greenhouse__application_enhanced WHERE job_parent_departments IS NOT NULL
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-067/attempt-01/sql/S7.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-067/attempt-01/sql/S7.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-067/attempt-01/results/S7.rows.jsonl)；完整：True；SHA256：`587c2bb677d157504049f9ce06a30a03d852eab47beea61ca5dd6f70c09b99c4`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "greenhouse__application_enhanced", "kind": "base", "block": null, "base_tables": ["greenhouse__application_enhanced"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |


## S8

类别 `data`；来源 `query_db`；调用 `ccacfa46b30a42f2a183fc4cbbb13f76`；状态 `success`。

```sql
SELECT source_name, source_type, total_applications, total_hires, avg_process_days, hire_rate, interview_rate, interview_to_hire_rate, efficiency_score 
FROM greenhouse__talent_pipeline_simplified 
ORDER BY efficiency_score DESC
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-067/attempt-01/sql/S8.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-067/attempt-01/sql/S8.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-067/attempt-01/results/S8.rows.jsonl)；完整：True；SHA256：`d7040707d358a9b04462dcd585651b602ae1229c3945f1e42fddb59c27ad3a0c`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "greenhouse__talent_pipeline_simplified", "kind": "base", "block": null, "base_tables": ["greenhouse__talent_pipeline_simplified"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |


## S9

类别 `data`；来源 `query_db`；调用 `2cede9500136484196f64a483a0e5b75`；状态 `success`。

```sql
SELECT DISTINCT overall_recommendation FROM greenhouse__interview_enhanced
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-067/attempt-01/sql/S9.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-067/attempt-01/sql/S9.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-067/attempt-01/results/S9.rows.jsonl)；完整：True；SHA256：`625849fb284f2ceadbdf5d0fe013a7a225bd0323f3539a546c243deb0d2db4fe`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "greenhouse__interview_enhanced", "kind": "base", "block": null, "base_tables": ["greenhouse__interview_enhanced"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |


## S10

类别 `data`；来源 `query_db`；调用 `70f1d9263b9840ce99d04b1eb513ff4f`；状态 `success`。

```sql
SELECT DISTINCT job_stage FROM greenhouse__interview_enhanced
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-067/attempt-01/sql/S10.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-067/attempt-01/sql/S10.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-067/attempt-01/results/S10.rows.jsonl)；完整：True；SHA256：`f7b5353ae77f80c4d9082ba012bb3dd9b58fb624c8d810154eec25b3e93860c8`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "greenhouse__interview_enhanced", "kind": "base", "block": null, "base_tables": ["greenhouse__interview_enhanced"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |


## S11

类别 `data`；来源 `query_db`；调用 `ccbb52aa8f4c4e4f8caafade626d1ac7`；状态 `success`。

```sql
SELECT status, COUNT(*) as cnt FROM greenhouse__application_enhanced GROUP BY status
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-067/attempt-01/sql/S11.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-067/attempt-01/sql/S11.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-067/attempt-01/results/S11.rows.jsonl)；完整：True；SHA256：`bf07faa0d3ca2aa06921aaff9b21489160807054bf7b555afad1c060e727f1fc`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "greenhouse__application_enhanced", "kind": "base", "block": null, "base_tables": ["greenhouse__application_enhanced"]}] | [] | ["status"] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |


## S12

类别 `data`；来源 `query_db`；调用 `ed14aeaa57f743fdb4686ffc4cdbfa42`；状态 `success`。

```sql
SELECT job_parent_departments, COUNT(*) as apps, 
       SUM(CASE WHEN status='hired' THEN 1 ELSE 0 END) as hires,
       ROUND(100.0 * SUM(CASE WHEN status='hired' THEN 1 ELSE 0 END) / COUNT(*), 1) as hire_rate
FROM greenhouse__application_enhanced 
WHERE job_parent_departments IS NOT NULL
GROUP BY job_parent_departments
ORDER BY hires DESC
LIMIT 20
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-067/attempt-01/sql/S12.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-067/attempt-01/sql/S12.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-067/attempt-01/results/S12.rows.jsonl)；完整：True；SHA256：`65717fd399bdf1611365258dc2306f29683b3a87098064dea710377c04a75f0f`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "greenhouse__application_enhanced", "kind": "base", "block": null, "base_tables": ["greenhouse__application_enhanced"]}] | [] | ["job_parent_departments"] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |
| B1 | SUM(CASE WHEN status = 'hired' THEN 1 ELSE 0 END) | [] | [{"table": "greenhouse__application_enhanced", "column": "status"}] | False |
| B1 | COUNT(*) | [] | [] | True |
| B1 | SUM(CASE WHEN status = 'hired' THEN 1 ELSE 0 END) | [] | [{"table": "greenhouse__application_enhanced", "column": "status"}] | False |


## S13

类别 `data`；来源 `query_db`；调用 `024184f91da74165b2e11c7edc11887b`；状态 `success`。

```sql
SELECT candidate_gender, COUNT(*) as cnt, 
       SUM(CASE WHEN status='hired' THEN 1 ELSE 0 END) as hires
FROM greenhouse__application_enhanced 
WHERE candidate_gender IS NOT NULL
GROUP BY candidate_gender
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-067/attempt-01/sql/S13.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-067/attempt-01/sql/S13.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-067/attempt-01/results/S13.rows.jsonl)；完整：True；SHA256：`4d971cadde52b6d0fb8a8988a2900e36cffd791a9a8d5e2d63833d27781a7515`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "greenhouse__application_enhanced", "kind": "base", "block": null, "base_tables": ["greenhouse__application_enhanced"]}] | [] | ["candidate_gender"] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |
| B1 | SUM(CASE WHEN status = 'hired' THEN 1 ELSE 0 END) | [] | [{"table": "greenhouse__application_enhanced", "column": "status"}] | False |


## S14

类别 `data`；来源 `query_db`；调用 `92a82a6884064109b9fe1435714b593f`；状态 `success`。

```sql
SELECT candidate_race, COUNT(*) as cnt, 
       SUM(CASE WHEN status='hired' THEN 1 ELSE 0 END) as hires
FROM greenhouse__application_enhanced 
WHERE candidate_race IS NOT NULL
GROUP BY candidate_race
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-067/attempt-01/sql/S14.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-067/attempt-01/sql/S14.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-067/attempt-01/results/S14.rows.jsonl)；完整：True；SHA256：`b7de28dc3c7bcdad6fb2a1e62640fbb315bb239d13332b7e5d085b2dd14b3b49`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "greenhouse__application_enhanced", "kind": "base", "block": null, "base_tables": ["greenhouse__application_enhanced"]}] | [] | ["candidate_race"] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |
| B1 | SUM(CASE WHEN status = 'hired' THEN 1 ELSE 0 END) | [] | [{"table": "greenhouse__application_enhanced", "column": "status"}] | False |


## S15

类别 `data`；来源 `query_db`；调用 `66ad950de80b41038781258644a01e20`；状态 `success`。

```sql
SELECT * FROM greenhouse__job_enhanced ORDER BY count_total_applications DESC LIMIT 20
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-067/attempt-01/sql/S15.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-067/attempt-01/sql/S15.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-067/attempt-01/results/S15.rows.jsonl)；完整：True；SHA256：`3cd4f63416932095f32aedca4b907a20e163ce9381d43761fbfbf7a43f81a885`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "greenhouse__job_enhanced", "kind": "base", "block": null, "base_tables": ["greenhouse__job_enhanced"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |


## S16

类别 `data`；来源 `query_db`；调用 `05aa4300bd5d4b87a2c163097c0d8625`；状态 `success`。

```sql
SELECT DISTINCT departments FROM greenhouse__job_enhanced WHERE departments IS NOT NULL LIMIT 20
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-067/attempt-01/sql/S16.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-067/attempt-01/sql/S16.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-067/attempt-01/results/S16.rows.jsonl)；完整：True；SHA256：`0ac712bd4325cacda41cb2488c80fe28f6247c33d44d93829435113d2c2917f8`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "greenhouse__job_enhanced", "kind": "base", "block": null, "base_tables": ["greenhouse__job_enhanced"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |


## S17

类别 `data`；来源 `query_db`；调用 `70537200fa324540bb243bf3a8019fe0`；状态 `success`。

```sql
SELECT DISTINCT current_job_stage FROM greenhouse__application_enhanced
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-067/attempt-01/sql/S17.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-067/attempt-01/sql/S17.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-067/attempt-01/results/S17.rows.jsonl)；完整：True；SHA256：`40e8653ba137a8d856b61fa4c2c7fb0627b8b5ad898866b5702c96cfd63356ee`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "greenhouse__application_enhanced", "kind": "base", "block": null, "base_tables": ["greenhouse__application_enhanced"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |


## S18

类别 `data`；来源 `query_db`；调用 `d37f963108a14f54883275de91c841bd`；状态 `success`。

```sql
SELECT MIN(applied_at) as min_a, MAX(applied_at) as max_a, MIN(candidate_created_at) as min_c, MAX(candidate_created_at) as max_c, COUNT(*) as total_rows FROM greenhouse__application_enhanced
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-067/attempt-01/sql/S18.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-067/attempt-01/sql/S18.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-067/attempt-01/results/S18.rows.jsonl)；完整：True；SHA256：`b50902469fe16f4b432a4189ac93a960afca0ff2ff13e30eb6f83cb880e94248`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "greenhouse__application_enhanced", "kind": "base", "block": null, "base_tables": ["greenhouse__application_enhanced"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | MIN(applied_at) | [{"table": "greenhouse__application_enhanced", "column": "applied_at"}] | [] | False |
| B1 | MAX(applied_at) | [{"table": "greenhouse__application_enhanced", "column": "applied_at"}] | [] | False |
| B1 | MIN(candidate_created_at) | [{"table": "greenhouse__application_enhanced", "column": "candidate_created_at"}] | [] | False |
| B1 | MAX(candidate_created_at) | [{"table": "greenhouse__application_enhanced", "column": "candidate_created_at"}] | [] | False |
| B1 | COUNT(*) | [] | [] | True |


## S19

类别 `data`；来源 `query_db`；调用 `0caa9fc522cd4a69b58ff904d88d7875`；状态 `success`。

```sql
SELECT sourced_from, sourced_from_type, COUNT(*) as cnt FROM greenhouse__application_enhanced GROUP BY sourced_from, sourced_from_type ORDER BY cnt DESC LIMIT 20
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-067/attempt-01/sql/S19.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-067/attempt-01/sql/S19.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-067/attempt-01/results/S19.rows.jsonl)；完整：True；SHA256：`de28a797743e88c694ec1d461fa7a6dbe8167ce60b5ad408d2de3a42b20a78b6`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "greenhouse__application_enhanced", "kind": "base", "block": null, "base_tables": ["greenhouse__application_enhanced"]}] | [] | ["sourced_from", "sourced_from_type"] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |


## S20

类别 `data`；来源 `query_db`；调用 `b106f8f87d394ca19e9fe86e3d744ac0`；状态 `success`。

```sql
SELECT source_id, COUNT(*) as cnt FROM greenhouse__application_enhanced GROUP BY source_id ORDER BY cnt DESC
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-067/attempt-01/sql/S20.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-067/attempt-01/sql/S20.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-067/attempt-01/results/S20.rows.jsonl)；完整：True；SHA256：`15eda38cb18fdb6ebeb4bf018dafbe2976ce317208fe0c5217954c79f82fa140`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "greenhouse__application_enhanced", "kind": "base", "block": null, "base_tables": ["greenhouse__application_enhanced"]}] | [] | ["source_id"] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |


## S21

类别 `data`；来源 `query_db`；调用 `8bd6041951184f7d9410adcb509c1582`；状态 `success`。

```sql
SELECT source_id, sourced_from, sourced_from_type, COUNT(*) as cnt
FROM greenhouse__application_enhanced 
WHERE source_id IS NOT NULL
GROUP BY source_id, sourced_from, sourced_from_type
ORDER BY cnt DESC
LIMIT 20
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-067/attempt-01/sql/S21.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-067/attempt-01/sql/S21.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-067/attempt-01/results/S21.rows.jsonl)；完整：True；SHA256：`e7587d3c2888525c406413a4aba7345cb405479120ff4d5b4f43ccee3e0daa17`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "greenhouse__application_enhanced", "kind": "base", "block": null, "base_tables": ["greenhouse__application_enhanced"]}] | [] | ["source_id", "sourced_from", "sourced_from_type"] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |


## S22

类别 `data`；来源 `query_db`；调用 `6295224c7f9b4ebba9707706996ab734`；状态 `success`。

```sql
SELECT DISTINCT source_id, sourced_from FROM greenhouse__application_enhanced ORDER BY source_id LIMIT 20
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-067/attempt-01/sql/S22.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-067/attempt-01/sql/S22.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-067/attempt-01/results/S22.rows.jsonl)；完整：True；SHA256：`7a4a8ddbfc4a7f0e41c594003fb992a24603babfc7245ce46979a0552d282374`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "greenhouse__application_enhanced", "kind": "base", "block": null, "base_tables": ["greenhouse__application_enhanced"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |


## S23

类别 `data`；来源 `query_db`；调用 `e3ee01fea67e4cdab1257b0d65b5c69e`；状态 `success`。

```sql
SELECT sourced_from, COUNT(*) as cnt, 
       SUM(CASE WHEN source_id <= 8 THEN 1 ELSE 0 END) as mapped,
       MIN(source_id) as min_sid, MAX(source_id) as max_sid
FROM greenhouse__application_enhanced 
GROUP BY sourced_from
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-067/attempt-01/sql/S23.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-067/attempt-01/sql/S23.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-067/attempt-01/results/S23.rows.jsonl)；完整：True；SHA256：`41c5a151a7732f26156c047f78b3c3fa85f190db121aaa38917ad71a5a51f0d6`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "greenhouse__application_enhanced", "kind": "base", "block": null, "base_tables": ["greenhouse__application_enhanced"]}] | [] | ["sourced_from"] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |
| B1 | SUM(CASE WHEN source_id <= 8 THEN 1 ELSE 0 END) | [] | [{"table": "greenhouse__application_enhanced", "column": "source_id"}] | False |
| B1 | MIN(source_id) | [{"table": "greenhouse__application_enhanced", "column": "source_id"}] | [] | False |
| B1 | MAX(source_id) | [{"table": "greenhouse__application_enhanced", "column": "source_id"}] | [] | False |


## S24

类别 `data`；来源 `query_db`；调用 `d177629814744635a66a8db337f827f4`；状态 `success`。

```sql
SELECT candidate_gender, candidate_race, COUNT(*) as cnt 
FROM greenhouse__application_enhanced 
WHERE status = 'hired'
GROUP BY candidate_gender, candidate_race
ORDER BY cnt DESC
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-067/attempt-01/sql/S24.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-067/attempt-01/sql/S24.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-067/attempt-01/results/S24.rows.jsonl)；完整：True；SHA256：`ace1d4f7e3dadab3c06b8cc2979b0c6c3db26f4ebb6c7c1c011aceefa9a33066`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "greenhouse__application_enhanced", "kind": "base", "block": null, "base_tables": ["greenhouse__application_enhanced"]}] | [] | ["candidate_gender", "candidate_race"] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |


## S25

类别 `data`；来源 `query_db`；调用 `84a935ee25f042e98d158379410f0e50`；状态 `success`。

```sql
SELECT COUNT(*) as total_hires,
       SUM(CASE WHEN candidate_gender = 'Female' THEN 1 ELSE 0 END) as female_hires,
       ROUND(100.0 * SUM(CASE WHEN candidate_gender = 'Female' THEN 1 ELSE 0 END) / COUNT(*), 1) as female_pct,
       SUM(CASE WHEN candidate_race != 'White' AND candidate_race IS NOT NULL THEN 1 ELSE 0 END) as non_white_hires,
       ROUND(100.0 * SUM(CASE WHEN candidate_race != 'White' AND candidate_race IS NOT NULL THEN 1 ELSE 0 END) / COUNT(*), 1) as non_white_pct
FROM greenhouse__application_enhanced 
WHERE status = 'hired'
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-067/attempt-01/sql/S25.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-067/attempt-01/sql/S25.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-067/attempt-01/results/S25.rows.jsonl)；完整：True；SHA256：`e639c8044cc3021038cb1b8e5f4e036c73609e0b4b7bcd1a9d66ae714f217b27`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "greenhouse__application_enhanced", "kind": "base", "block": null, "base_tables": ["greenhouse__application_enhanced"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |
| B1 | SUM(CASE WHEN candidate_gender = 'Female' THEN 1 ELSE 0 END) | [] | [{"table": "greenhouse__application_enhanced", "column": "candidate_gender"}] | False |
| B1 | SUM(CASE WHEN candidate_race <> 'White' AND NOT candidate_race IS NULL THEN 1 ELSE 0 END) | [] | [{"table": "greenhouse__application_enhanced", "column": "candidate_race"}, {"table": "greenhouse__application_enhanced", "column": "candidate_race"}] | False |
| B1 | COUNT(*) | [] | [] | True |
| B1 | COUNT(*) | [] | [] | True |
| B1 | SUM(CASE WHEN candidate_gender = 'Female' THEN 1 ELSE 0 END) | [] | [{"table": "greenhouse__application_enhanced", "column": "candidate_gender"}] | False |
| B1 | SUM(CASE WHEN candidate_race <> 'White' AND NOT candidate_race IS NULL THEN 1 ELSE 0 END) | [] | [{"table": "greenhouse__application_enhanced", "column": "candidate_race"}, {"table": "greenhouse__application_enhanced", "column": "candidate_race"}] | False |


## S26

类别 `data`；来源 `query_db`；调用 `5e9d90e0dbb24beab0cd8093e6c71e56`；状态 `success`。

```sql
SELECT current_job_stage, COUNT(*) as cnt,
       SUM(CASE WHEN status='hired' THEN 1 ELSE 0 END) as hired
FROM greenhouse__application_enhanced 
GROUP BY current_job_stage
ORDER BY cnt DESC
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-067/attempt-01/sql/S26.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-067/attempt-01/sql/S26.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-067/attempt-01/results/S26.rows.jsonl)；完整：True；SHA256：`67af66113d3aed8fc59febdf3440ba388c126ee3fe582f10375ea1fe36acb5e6`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "greenhouse__application_enhanced", "kind": "base", "block": null, "base_tables": ["greenhouse__application_enhanced"]}] | [] | ["current_job_stage"] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |
| B1 | SUM(CASE WHEN status = 'hired' THEN 1 ELSE 0 END) | [] | [{"table": "greenhouse__application_enhanced", "column": "status"}] | False |


## S27

类别 `data`；来源 `query_db`；调用 `7f5c35585afb4bfa9ff9a22e6ed51f57`；状态 `success`。

```sql
SELECT COUNT(*) as total_interviews, 
       COUNT(DISTINCT interview_id) as unique_interviews,
       AVG(duration_interview_minutes) as avg_duration,
       overall_recommendation,
       COUNT(*) as cnt
FROM greenhouse__interview_enhanced 
WHERE overall_recommendation IS NOT NULL
GROUP BY overall_recommendation
ORDER BY cnt DESC
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-067/attempt-01/sql/S27.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-067/attempt-01/sql/S27.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-067/attempt-01/results/S27.rows.jsonl)；完整：True；SHA256：`9899d1b57ebc235dae3503565171b35fcad2a233198fc7f6249d81b6bf05164a`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "greenhouse__interview_enhanced", "kind": "base", "block": null, "base_tables": ["greenhouse__interview_enhanced"]}] | [] | ["overall_recommendation"] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |
| B1 | COUNT(DISTINCT interview_id) | [{"table": "greenhouse__interview_enhanced", "column": "interview_id"}] | [] | False |
| B1 | AVG(duration_interview_minutes) | [{"table": "greenhouse__interview_enhanced", "column": "duration_interview_minutes"}] | [] | False |
| B1 | COUNT(*) | [] | [] | True |


## S28

类别 `data`；来源 `query_db`；调用 `007410cf555743968bb9778b87776919`；状态 `success`。

```sql
SELECT candidate_gender, COUNT(*) as total, 
       SUM(CASE WHEN status='hired' THEN 1 ELSE 0 END) as hired
FROM greenhouse__application_enhanced 
GROUP BY candidate_gender
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-067/attempt-01/sql/S28.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-067/attempt-01/sql/S28.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-067/attempt-01/results/S28.rows.jsonl)；完整：True；SHA256：`0312572e6569e1728527b983c15ec2bdfa7450e06d9d3555e02bf4535dbdddb7`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "greenhouse__application_enhanced", "kind": "base", "block": null, "base_tables": ["greenhouse__application_enhanced"]}] | [] | ["candidate_gender"] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |
| B1 | SUM(CASE WHEN status = 'hired' THEN 1 ELSE 0 END) | [] | [{"table": "greenhouse__application_enhanced", "column": "status"}] | False |


## S29

类别 `data`；来源 `query_db`；调用 `ef5f4ff5f70c4da5843fd46aa456f5c1`；状态 `success`。

```sql
SELECT candidate_race, COUNT(*) as total, 
       SUM(CASE WHEN status='hired' THEN 1 ELSE 0 END) as hired
FROM greenhouse__application_enhanced 
GROUP BY candidate_race
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-067/attempt-01/sql/S29.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-067/attempt-01/sql/S29.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-067/attempt-01/results/S29.rows.jsonl)；完整：True；SHA256：`989161d24b1ef7cd0ef7a6e06b755fc844cb58cb6f43abe90fc14c90c9d48368`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "greenhouse__application_enhanced", "kind": "base", "block": null, "base_tables": ["greenhouse__application_enhanced"]}] | [] | ["candidate_race"] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |
| B1 | SUM(CASE WHEN status = 'hired' THEN 1 ELSE 0 END) | [] | [{"table": "greenhouse__application_enhanced", "column": "status"}] | False |


## S30

类别 `data`；来源 `query_db`；调用 `a86a92a4d355430f9e77fa035d0abe20`；状态 `success`。

```sql
SELECT COUNT(DISTINCT source_id) FROM greenhouse__application_enhanced
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-067/attempt-01/sql/S30.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-067/attempt-01/sql/S30.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-067/attempt-01/results/S30.rows.jsonl)；完整：True；SHA256：`48c320e8238f5f9734818b5a7160e4a0f622a3518ea063063bf3e67385955819`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "greenhouse__application_enhanced", "kind": "base", "block": null, "base_tables": ["greenhouse__application_enhanced"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(DISTINCT source_id) | [{"table": "greenhouse__application_enhanced", "column": "source_id"}] | [] | False |


## S31

类别 `data`；来源 `query_db`；调用 `c66ec8d7d28e4afd9b5c1bf53127e878`；状态 `success`。

```sql
SELECT source_id, source_name, source_type FROM greenhouse__talent_pipeline_simplified
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-067/attempt-01/sql/S31.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-067/attempt-01/sql/S31.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-067/attempt-01/results/S31.rows.jsonl)；完整：True；SHA256：`b2f7919f6de17a9096f91bcd89ee739387b98dc8e6974382110fd6ed2f134889`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "greenhouse__talent_pipeline_simplified", "kind": "base", "block": null, "base_tables": ["greenhouse__talent_pipeline_simplified"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |


## S32

类别 `data`；来源 `query_db`；调用 `375b94f2cbde44359018ef96a061d066`；状态 `success`。

```sql
SELECT sourced_from,
       COUNT(*) as total_apps,
       SUM(CASE WHEN status='hired' THEN 1 ELSE 0 END) as hires,
       SUM(CASE WHEN status='rejected' THEN 1 ELSE 0 END) as rejected,
       SUM(CASE WHEN status='active' THEN 1 ELSE 0 END) as active,
       SUM(CASE WHEN status='withdrawn' THEN 1 ELSE 0 END) as withdrawn,
       ROUND(100.0 * SUM(CASE WHEN status='hired' THEN 1 ELSE 0 END) / COUNT(*), 1) as hire_rate
FROM greenhouse__application_enhanced 
GROUP BY sourced_from
ORDER BY hires DESC
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-067/attempt-01/sql/S32.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-067/attempt-01/sql/S32.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-067/attempt-01/results/S32.rows.jsonl)；完整：True；SHA256：`1f1c4ecec5517545084a0e1c90c077b3dec2555504f50eebba945b03d41007e9`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "greenhouse__application_enhanced", "kind": "base", "block": null, "base_tables": ["greenhouse__application_enhanced"]}] | [] | ["sourced_from"] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |
| B1 | SUM(CASE WHEN status = 'hired' THEN 1 ELSE 0 END) | [] | [{"table": "greenhouse__application_enhanced", "column": "status"}] | False |
| B1 | SUM(CASE WHEN status = 'rejected' THEN 1 ELSE 0 END) | [] | [{"table": "greenhouse__application_enhanced", "column": "status"}] | False |
| B1 | SUM(CASE WHEN status = 'active' THEN 1 ELSE 0 END) | [] | [{"table": "greenhouse__application_enhanced", "column": "status"}] | False |
| B1 | SUM(CASE WHEN status = 'withdrawn' THEN 1 ELSE 0 END) | [] | [{"table": "greenhouse__application_enhanced", "column": "status"}] | False |
| B1 | COUNT(*) | [] | [] | True |
| B1 | SUM(CASE WHEN status = 'hired' THEN 1 ELSE 0 END) | [] | [{"table": "greenhouse__application_enhanced", "column": "status"}] | False |


## S33

类别 `data`；来源 `query_db`；调用 `427bab0b5b0f4819b4740d9a2bbb8c78`；状态 `success`。

```sql
SELECT job_parent_departments,
       COUNT(*) as total_apps,
       SUM(CASE WHEN status='hired' THEN 1 ELSE 0 END) as hires,
       ROUND(100.0 * SUM(CASE WHEN status='hired' THEN 1 ELSE 0 END) / COUNT(*), 1) as hire_rate
FROM greenhouse__application_enhanced 
WHERE job_parent_departments IS NOT NULL
GROUP BY job_parent_departments
ORDER BY hires DESC
LIMIT 15
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-067/attempt-01/sql/S33.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-067/attempt-01/sql/S33.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-067/attempt-01/results/S33.rows.jsonl)；完整：True；SHA256：`29fc790b7608aade541640f2cc0667c69698daea5a2ed36e87ae4a214f7fa9a4`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "greenhouse__application_enhanced", "kind": "base", "block": null, "base_tables": ["greenhouse__application_enhanced"]}] | [] | ["job_parent_departments"] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |
| B1 | SUM(CASE WHEN status = 'hired' THEN 1 ELSE 0 END) | [] | [{"table": "greenhouse__application_enhanced", "column": "status"}] | False |
| B1 | COUNT(*) | [] | [] | True |
| B1 | SUM(CASE WHEN status = 'hired' THEN 1 ELSE 0 END) | [] | [{"table": "greenhouse__application_enhanced", "column": "status"}] | False |


## S34

类别 `data`；来源 `query_db`；调用 `a7d046a762314c79bba51108cdf3391c`；状态 `success`。

```sql
SELECT sourced_from,
       ROUND(AVG(count_interviews), 2) as avg_interviews,
       ROUND(AVG(count_distinct_interviewers), 2) as avg_interviewers,
       SUM(CASE WHEN has_interviewed_w_hiring_manager = 1 THEN 1 ELSE 0 END) as interviewed_with_hm,
       COUNT(*) as total_with_interview_data
FROM greenhouse__application_enhanced 
WHERE count_interviews > 0
GROUP BY sourced_from
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-067/attempt-01/sql/S34.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-067/attempt-01/sql/S34.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-067/attempt-01/results/S34.rows.jsonl)；完整：True；SHA256：`84a869fd2b685e9736dde19a7fce8bebd6bbce222d3530d98a1995214df5e6eb`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "greenhouse__application_enhanced", "kind": "base", "block": null, "base_tables": ["greenhouse__application_enhanced"]}] | [] | ["sourced_from"] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | SUM(CASE WHEN has_interviewed_w_hiring_manager = 1 THEN 1 ELSE 0 END) | [] | [{"table": "greenhouse__application_enhanced", "column": "has_interviewed_w_hiring_manager"}] | False |
| B1 | COUNT(*) | [] | [] | True |
| B1 | AVG(count_interviews) | [{"table": "greenhouse__application_enhanced", "column": "count_interviews"}] | [] | False |
| B1 | AVG(count_distinct_interviewers) | [{"table": "greenhouse__application_enhanced", "column": "count_distinct_interviewers"}] | [] | False |


## S35

类别 `data`；来源 `query_db`；调用 `d15f22dce0724f3db085d2170e6e8f52`；状态 `success`。

```sql
SELECT MAX(has_interviewed_w_hiring_manager) as max_hm, 
       MIN(has_interviewed_w_hiring_manager) as min_hm,
       SUM(has_interviewed_w_hiring_manager) as sum_hm
FROM greenhouse__application_enhanced
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-067/attempt-01/sql/S35.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-067/attempt-01/sql/S35.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-067/attempt-01/results/S35.rows.jsonl)；完整：True；SHA256：`32d31f8e37e0790192e2811106c2a3ade88b6cf0ce7061c37a5147424bbcee3c`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "greenhouse__application_enhanced", "kind": "base", "block": null, "base_tables": ["greenhouse__application_enhanced"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | MAX(has_interviewed_w_hiring_manager) | [{"table": "greenhouse__application_enhanced", "column": "has_interviewed_w_hiring_manager"}] | [] | False |
| B1 | MIN(has_interviewed_w_hiring_manager) | [{"table": "greenhouse__application_enhanced", "column": "has_interviewed_w_hiring_manager"}] | [] | False |
| B1 | SUM(has_interviewed_w_hiring_manager) | [{"table": "greenhouse__application_enhanced", "column": "has_interviewed_w_hiring_manager"}] | [] | False |


## S36

类别 `data`；来源 `query_db`；调用 `d20eac5bf0f84451915a2546193ef397`；状态 `success`。

```sql
SELECT COUNT(*) as total_scores, 
       AVG(rating) as avg_rating,
       MIN(rating) as min_rating,
       MAX(rating) as max_rating
FROM greenhouse__interview_scorecard_detail
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-067/attempt-01/sql/S36.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-067/attempt-01/sql/S36.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-067/attempt-01/results/S36.rows.jsonl)；完整：True；SHA256：`109b5418f8eecc78b13885eccde5a707c5b3a6efa57aa0d96c4fa429cce3a5e2`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "greenhouse__interview_scorecard_detail", "kind": "base", "block": null, "base_tables": ["greenhouse__interview_scorecard_detail"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |
| B1 | AVG(rating) | [{"table": "greenhouse__interview_scorecard_detail", "column": "rating"}] | [] | False |
| B1 | MIN(rating) | [{"table": "greenhouse__interview_scorecard_detail", "column": "rating"}] | [] | False |
| B1 | MAX(rating) | [{"table": "greenhouse__interview_scorecard_detail", "column": "rating"}] | [] | False |


## S37

类别 `data`；来源 `query_db`；调用 `7678c6b0bfc04f5e9eba732f8501a82a`；状态 `success`。

```sql
SELECT attribute_category, COUNT(*) as cnt, 
       AVG(rating) as avg_rating
FROM greenhouse__interview_scorecard_detail
GROUP BY attribute_category
ORDER BY cnt DESC
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-067/attempt-01/sql/S37.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-067/attempt-01/sql/S37.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-067/attempt-01/results/S37.rows.jsonl)；完整：True；SHA256：`e02b11b76cd21ee0757618e4c94d0b99bd861e03a06ad04599b8ac75c4c78d1e`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "greenhouse__interview_scorecard_detail", "kind": "base", "block": null, "base_tables": ["greenhouse__interview_scorecard_detail"]}] | [] | ["attribute_category"] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |
| B1 | AVG(rating) | [{"table": "greenhouse__interview_scorecard_detail", "column": "rating"}] | [] | False |


## S38

类别 `data`；来源 `query_db`；调用 `5443a0b6913a4e909e3443062304c9b6`；状态 `success`。

```sql
SELECT DISTINCT attribute_name FROM greenhouse__interview_scorecard_detail LIMIT 20
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-067/attempt-01/sql/S38.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-067/attempt-01/sql/S38.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-067/attempt-01/results/S38.rows.jsonl)；完整：True；SHA256：`29cb9a4302d9109e050921ca9523a72f6d4e1d8bd93ed36384157d7f4435afd6`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "greenhouse__interview_scorecard_detail", "kind": "base", "block": null, "base_tables": ["greenhouse__interview_scorecard_detail"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |


## S39

类别 `data`；来源 `query_db`；调用 `e03c9ff895794affb0951403d56162ae`；状态 `success`。

```sql
SELECT interviewer_is_hiring_manager, COUNT(*) as cnt,
       AVG(duration_interview_minutes) as avg_duration
FROM greenhouse__interview_enhanced
GROUP BY interviewer_is_hiring_manager
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-067/attempt-01/sql/S39.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-067/attempt-01/sql/S39.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-067/attempt-01/results/S39.rows.jsonl)；完整：True；SHA256：`69a24a66d132ce8690b88ac8ee3694913bd91881c03e3ddd3f230e882b1fe2b9`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "greenhouse__interview_enhanced", "kind": "base", "block": null, "base_tables": ["greenhouse__interview_enhanced"]}] | [] | ["interviewer_is_hiring_manager"] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |
| B1 | AVG(duration_interview_minutes) | [{"table": "greenhouse__interview_enhanced", "column": "duration_interview_minutes"}] | [] | False |


## S40

类别 `data`；来源 `query_db`；调用 `82cacbf858cc45b5ab9c0bb71160095a`；状态 `success`。

```sql
SELECT job_parent_departments, COUNT(*) as cnt, 
       AVG(duration_interview_minutes) as avg_duration,
       ROUND(SUM(CASE WHEN lower(overall_recommendation) IN ('strong_yes','yes','strong yes','yes') THEN 1 ELSE 0 END) * 100.0 / COUNT(*), 1) as positive_pct
FROM greenhouse__interview_enhanced
WHERE job_parent_departments IS NOT NULL
GROUP BY job_parent_departments
ORDER BY cnt DESC
LIMIT 15
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-067/attempt-01/sql/S40.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-067/attempt-01/sql/S40.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-067/attempt-01/results/S40.rows.jsonl)；完整：True；SHA256：`382616f5d117b19323f25991a63059ffb56477f50647dd574eacb20b9f8a51be`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "greenhouse__interview_enhanced", "kind": "base", "block": null, "base_tables": ["greenhouse__interview_enhanced"]}] | [] | ["job_parent_departments"] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |
| B1 | AVG(duration_interview_minutes) | [{"table": "greenhouse__interview_enhanced", "column": "duration_interview_minutes"}] | [] | False |
| B1 | COUNT(*) | [] | [] | True |
| B1 | SUM(CASE WHEN LOWER(overall_recommendation) IN ('strong_yes', 'yes', 'strong yes', 'yes') THEN 1 ELSE 0 END) | [] | [{"table": "greenhouse__interview_enhanced", "column": "overall_recommendation"}] | False |


## S41

类别 `data`；来源 `query_db`；调用 `0b66d75c1cea493ca15ab808125030be`；状态 `success`。

```sql
SELECT interview_name, COUNT(*) as cnt,
       AVG(duration_interview_minutes) as avg_duration,
       ROUND(SUM(CASE WHEN lower(overall_recommendation) IN ('strong_yes','yes','strong yes','yes') THEN 1 ELSE 0 END) * 100.0 / NULLIF(COUNT(*),0), 1) as positive_pct
FROM greenhouse__interview_enhanced
GROUP BY interview_name
ORDER BY cnt DESC
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-067/attempt-01/sql/S41.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-067/attempt-01/sql/S41.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-067/attempt-01/results/S41.rows.jsonl)；完整：True；SHA256：`3daddafb1d2300ed00e2fe31eaf5456140de7aa983ce946239a80dcbc47124c2`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "greenhouse__interview_enhanced", "kind": "base", "block": null, "base_tables": ["greenhouse__interview_enhanced"]}] | [] | ["interview_name"] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |
| B1 | AVG(duration_interview_minutes) | [{"table": "greenhouse__interview_enhanced", "column": "duration_interview_minutes"}] | [] | False |
| B1 | SUM(CASE WHEN LOWER(overall_recommendation) IN ('strong_yes', 'yes', 'strong yes', 'yes') THEN 1 ELSE 0 END) | [] | [{"table": "greenhouse__interview_enhanced", "column": "overall_recommendation"}] | False |
| B1 | COUNT(*) | [] | [] | True |


## S42

类别 `data`；来源 `query_db`；调用 `aa7f3758f068499abf12845e9ac93ed1`；状态 `success`。

```sql
SELECT sourced_from, 
       current_job_stage,
       COUNT(*) as cnt,
       SUM(CASE WHEN status='hired' THEN 1 ELSE 0 END) as hired
FROM greenhouse__application_enhanced 
GROUP BY sourced_from, current_job_stage
ORDER BY sourced_from, current_job_stage
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-067/attempt-01/sql/S42.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-067/attempt-01/sql/S42.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-067/attempt-01/results/S42.rows.jsonl)；完整：True；SHA256：`31d425f812e827c4cbec3bc87786ba0b45d419db4644c5d667cbb1651f324ace`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "greenhouse__application_enhanced", "kind": "base", "block": null, "base_tables": ["greenhouse__application_enhanced"]}] | [] | ["sourced_from", "current_job_stage"] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |
| B1 | SUM(CASE WHEN status = 'hired' THEN 1 ELSE 0 END) | [] | [{"table": "greenhouse__application_enhanced", "column": "status"}] | False |


## S43

类别 `data`；来源 `query_db`；调用 `784a148e8337492c9df106dafd085d92`；状态 `success`。

```sql
SELECT sourced_from as channel,
       COUNT(*) as applications,
       SUM(CASE WHEN status='hired' THEN 1 ELSE 0 END) as hires,
       ROUND(100.0 * SUM(CASE WHEN status='hired' THEN 1 ELSE 0 END) / COUNT(*), 1) as hire_rate,
       ROUND(100.0 * SUM(CASE WHEN count_interviews > 0 THEN 1 ELSE 0 END) / COUNT(*), 1) as interview_rate,
       AVG(count_interviews) as avg_interviews_per_app
FROM greenhouse__application_enhanced 
GROUP BY sourced_from
ORDER BY hires DESC
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-067/attempt-01/sql/S43.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-067/attempt-01/sql/S43.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-067/attempt-01/results/S43.rows.jsonl)；完整：True；SHA256：`59190f543cdd3da1d292b61257664a3ebb04e56325cb8e3bead0722cea65b458`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "greenhouse__application_enhanced", "kind": "base", "block": null, "base_tables": ["greenhouse__application_enhanced"]}] | [] | ["sourced_from"] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |
| B1 | SUM(CASE WHEN status = 'hired' THEN 1 ELSE 0 END) | [] | [{"table": "greenhouse__application_enhanced", "column": "status"}] | False |
| B1 | AVG(count_interviews) | [{"table": "greenhouse__application_enhanced", "column": "count_interviews"}] | [] | False |
| B1 | COUNT(*) | [] | [] | True |
| B1 | COUNT(*) | [] | [] | True |
| B1 | SUM(CASE WHEN status = 'hired' THEN 1 ELSE 0 END) | [] | [{"table": "greenhouse__application_enhanced", "column": "status"}] | False |
| B1 | SUM(CASE WHEN count_interviews > 0 THEN 1 ELSE 0 END) | [] | [{"table": "greenhouse__application_enhanced", "column": "count_interviews"}] | False |


## S44

类别 `data`；来源 `query_db`；调用 `a71f0769573446dd843f75f6d1234f1b`；状态 `success`。

```sql
SELECT sourced_from,
       SUM(CASE WHEN candidate_gender='Female' AND status='hired' THEN 1 ELSE 0 END) as female_hires,
       SUM(CASE WHEN status='hired' THEN 1 ELSE 0 END) as total_hires_with_gender,
       ROUND(100.0 * SUM(CASE WHEN candidate_gender='Female' AND status='hired' THEN 1 ELSE 0 END) / 
             NULLIF(SUM(CASE WHEN candidate_gender IS NOT NULL AND status='hired' THEN 1 ELSE 0 END), 0), 1) as female_pct
FROM greenhouse__application_enhanced 
GROUP BY sourced_from
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-067/attempt-01/sql/S44.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-067/attempt-01/sql/S44.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-067/attempt-01/results/S44.rows.jsonl)；完整：True；SHA256：`fe9e4eb01cb592fd9f6635517623071cc32f51c6f7f71792910d5a67c8f6685b`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "greenhouse__application_enhanced", "kind": "base", "block": null, "base_tables": ["greenhouse__application_enhanced"]}] | [] | ["sourced_from"] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | SUM(CASE WHEN candidate_gender = 'Female' AND status = 'hired' THEN 1 ELSE 0 END) | [] | [{"table": "greenhouse__application_enhanced", "column": "candidate_gender"}, {"table": "greenhouse__application_enhanced", "column": "status"}] | False |
| B1 | SUM(CASE WHEN status = 'hired' THEN 1 ELSE 0 END) | [] | [{"table": "greenhouse__application_enhanced", "column": "status"}] | False |
| B1 | SUM(CASE WHEN candidate_gender = 'Female' AND status = 'hired' THEN 1 ELSE 0 END) | [] | [{"table": "greenhouse__application_enhanced", "column": "candidate_gender"}, {"table": "greenhouse__application_enhanced", "column": "status"}] | False |
| B1 | SUM(CASE WHEN NOT candidate_gender IS NULL AND status = 'hired' THEN 1 ELSE 0 END) | [] | [{"table": "greenhouse__application_enhanced", "column": "status"}, {"table": "greenhouse__application_enhanced", "column": "candidate_gender"}] | False |


## S45

类别 `data`；来源 `query_db`；调用 `883ba381497e4ebeb0da7f14f60cd02e`；状态 `success`。

```sql
WITH funnel AS (
  SELECT 
    COUNT(*) as total_applications,
    SUM(CASE WHEN count_interviews > 0 THEN 1 ELSE 0 END) as interviewed,
    SUM(CASE WHEN status='hired' THEN 1 ELSE 0 END) as hired
  FROM greenhouse__application_enhanced
)
SELECT total_applications, interviewed, hired,
       ROUND(100.0 * interviewed / total_applications, 1) as app_to_interview_pct,
       ROUND(100.0 * hired / interviewed, 1) as interview_to_hire_pct,
       ROUND(100.0 * hired / total_applications, 1) as overall_hire_rate
FROM funnel
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-067/attempt-01/sql/S45.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-067/attempt-01/sql/S45.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-067/attempt-01/results/S45.rows.jsonl)；完整：True；SHA256：`a809df7f8f3a96fbf967e0c85f8fc8801e068a6b943c4c331701c14bebc0d4c2`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "greenhouse__application_enhanced", "kind": "base", "block": null, "base_tables": ["greenhouse__application_enhanced"]}] | [] | [] |
| B2 | [{"alias": "funnel", "kind": "derived", "block": "B1", "base_tables": ["greenhouse__application_enhanced"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |
| B1 | SUM(CASE WHEN count_interviews > 0 THEN 1 ELSE 0 END) | [] | [{"table": "greenhouse__application_enhanced", "column": "count_interviews"}] | False |
| B1 | SUM(CASE WHEN status = 'hired' THEN 1 ELSE 0 END) | [] | [{"table": "greenhouse__application_enhanced", "column": "status"}] | False |


## S46

类别 `data`；来源 `query_db`；调用 `f57399c721ee47a0a4711ddfb5dec05c`；状态 `success`。

```sql
SELECT sourced_from,
       SUM(CASE WHEN candidate_race != 'White' AND candidate_race IS NOT NULL AND status='hired' THEN 1 ELSE 0 END) as non_white_hires,
       SUM(CASE WHEN status='hired' AND candidate_race IS NOT NULL THEN 1 ELSE 0 END) as total_hires_with_race,
       ROUND(100.0 * SUM(CASE WHEN candidate_race != 'White' AND candidate_race IS NOT NULL AND status='hired' THEN 1 ELSE 0 END) / 
             NULLIF(SUM(CASE WHEN status='hired' AND candidate_race IS NOT NULL THEN 1 ELSE 0 END), 0), 1) as non_white_pct
FROM greenhouse__application_enhanced 
GROUP BY sourced_from
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-067/attempt-01/sql/S46.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-067/attempt-01/sql/S46.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-067/attempt-01/results/S46.rows.jsonl)；完整：True；SHA256：`df75f410668e620f7c20ae09b0db1d252aaa81e9855eefe2dca5ca1148401b21`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "greenhouse__application_enhanced", "kind": "base", "block": null, "base_tables": ["greenhouse__application_enhanced"]}] | [] | ["sourced_from"] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | SUM(CASE WHEN candidate_race <> 'White' AND NOT candidate_race IS NULL AND status = 'hired' THEN 1 ELSE 0 END) | [] | [{"table": "greenhouse__application_enhanced", "column": "status"}, {"table": "greenhouse__application_enhanced", "column": "candidate_race"}, {"table": "greenhouse__application_enhanced", "column": "candidate_race"}] | False |
| B1 | SUM(CASE WHEN status = 'hired' AND NOT candidate_race IS NULL THEN 1 ELSE 0 END) | [] | [{"table": "greenhouse__application_enhanced", "column": "status"}, {"table": "greenhouse__application_enhanced", "column": "candidate_race"}] | False |
| B1 | SUM(CASE WHEN candidate_race <> 'White' AND NOT candidate_race IS NULL AND status = 'hired' THEN 1 ELSE 0 END) | [] | [{"table": "greenhouse__application_enhanced", "column": "status"}, {"table": "greenhouse__application_enhanced", "column": "candidate_race"}, {"table": "greenhouse__application_enhanced", "column": "candidate_race"}] | False |
| B1 | SUM(CASE WHEN status = 'hired' AND NOT candidate_race IS NULL THEN 1 ELSE 0 END) | [] | [{"table": "greenhouse__application_enhanced", "column": "status"}, {"table": "greenhouse__application_enhanced", "column": "candidate_race"}] | False |


## S47

类别 `data`；来源 `query_db`；调用 `f14a279add0a499c8b96cc498c2af6dd`；状态 `success`。

```sql
SELECT job_parent_departments,
       SUM(CASE WHEN candidate_gender='Female' AND status='hired' THEN 1 ELSE 0 END) as female_hires,
       SUM(CASE WHEN status='hired' AND candidate_gender IS NOT NULL THEN 1 ELSE 0 END) as hires_with_gender,
       ROUND(100.0 * SUM(CASE WHEN candidate_gender='Female' AND status='hired' THEN 1 ELSE 0 END) / 
             NULLIF(SUM(CASE WHEN status='hired' AND candidate_gender IS NOT NULL THEN 1 ELSE 0 END), 0), 1) as female_pct
FROM greenhouse__application_enhanced 
WHERE job_parent_departments IS NOT NULL
GROUP BY job_parent_departments
HAVING hires_with_gender >= 5
ORDER BY female_pct DESC
LIMIT 15
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-067/attempt-01/sql/S47.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-067/attempt-01/sql/S47.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-067/attempt-01/results/S47.rows.jsonl)；完整：True；SHA256：`873124fdb2db02f86b4cde979b35ca782a411647c3c01582937c8e3f20c34218`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "greenhouse__application_enhanced", "kind": "base", "block": null, "base_tables": ["greenhouse__application_enhanced"]}] | [] | ["job_parent_departments"] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | SUM(CASE WHEN candidate_gender = 'Female' AND status = 'hired' THEN 1 ELSE 0 END) | [] | [{"table": "greenhouse__application_enhanced", "column": "candidate_gender"}, {"table": "greenhouse__application_enhanced", "column": "status"}] | False |
| B1 | SUM(CASE WHEN status = 'hired' AND NOT candidate_gender IS NULL THEN 1 ELSE 0 END) | [] | [{"table": "greenhouse__application_enhanced", "column": "status"}, {"table": "greenhouse__application_enhanced", "column": "candidate_gender"}] | False |
| B1 | SUM(CASE WHEN candidate_gender = 'Female' AND status = 'hired' THEN 1 ELSE 0 END) | [] | [{"table": "greenhouse__application_enhanced", "column": "candidate_gender"}, {"table": "greenhouse__application_enhanced", "column": "status"}] | False |
| B1 | SUM(CASE WHEN status = 'hired' AND NOT candidate_gender IS NULL THEN 1 ELSE 0 END) | [] | [{"table": "greenhouse__application_enhanced", "column": "status"}, {"table": "greenhouse__application_enhanced", "column": "candidate_gender"}] | False |


## S48

类别 `data`；来源 `query_db`；调用 `2d59239b6f304640b8cd4999ea1b722b`；状态 `success`。

```sql
SELECT ie.interviewer_name, ie.job_title, ie.job_departments, ie.job_parent_departments,
       ie.overall_recommendation, ie.application_id, ie.candidate_id
FROM greenhouse__interview_enhanced ie
WHERE ie.overall_recommendation IS NOT NULL
LIMIT 20
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-067/attempt-01/sql/S48.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-067/attempt-01/sql/S48.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-067/attempt-01/results/S48.rows.jsonl)；完整：True；SHA256：`7679809720e338d523bdcb305afcaee39127663c6dbea91e509ebe2e4a5b7dd2`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "ie", "kind": "base", "block": null, "base_tables": ["greenhouse__interview_enhanced"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |


## S49

类别 `data`；来源 `query_db`；调用 `c87fac21e0eb40b88b3b29f050759b28`；状态 `success`。

```sql
SELECT COUNT(DISTINCT interviewer_name) as unique_interviewers,
       COUNT(DISTINCT interview_id) as unique_interviews
FROM greenhouse__interview_enhanced
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-067/attempt-01/sql/S49.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-067/attempt-01/sql/S49.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-067/attempt-01/results/S49.rows.jsonl)；完整：True；SHA256：`a561844326c148428151aa669dcb09ab2b2c5651091b1d29126aef592f11cdc4`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "greenhouse__interview_enhanced", "kind": "base", "block": null, "base_tables": ["greenhouse__interview_enhanced"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(DISTINCT interviewer_name) | [{"table": "greenhouse__interview_enhanced", "column": "interviewer_name"}] | [] | False |
| B1 | COUNT(DISTINCT interview_id) | [{"table": "greenhouse__interview_enhanced", "column": "interview_id"}] | [] | False |


## S50

类别 `data`；来源 `query_db`；调用 `12804e51579040abb4ab949f1452ad88`；状态 `success`。

```sql
SELECT 
  ROUND(AVG(rating), 2) as avg_rating,
  ROUND(AVG(CASE WHEN overall_recommendation IN ('strong_yes','yes','Strong Yes','Yes') THEN rating END), 2) as avg_positive_rating,
  ROUND(AVG(CASE WHEN overall_recommendation IN ('strong_no','no','Strong No','No') THEN rating END), 2) as avg_negative_rating,
  ROUND(AVG(CASE WHEN overall_recommendation = 'Maybe' THEN rating END), 2) as avg_maybe_rating
FROM greenhouse__interview_scorecard_detail
WHERE rating IS NOT NULL
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-067/attempt-01/sql/S50.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-067/attempt-01/sql/S50.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-067/attempt-01/results/S50.rows.jsonl)；完整：True；SHA256：`b175a74606b6c77984a9cdbda1d61cbda3f3b9b6745894c0f5cadf4258136c4a`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "greenhouse__interview_scorecard_detail", "kind": "base", "block": null, "base_tables": ["greenhouse__interview_scorecard_detail"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | AVG(rating) | [{"table": "greenhouse__interview_scorecard_detail", "column": "rating"}] | [] | False |
| B1 | AVG(CASE WHEN overall_recommendation IN ('strong_yes', 'yes', 'Strong Yes', 'Yes') THEN rating END) | [{"table": "greenhouse__interview_scorecard_detail", "column": "rating"}] | [{"table": "greenhouse__interview_scorecard_detail", "column": "overall_recommendation"}] | False |
| B1 | AVG(CASE WHEN overall_recommendation IN ('strong_no', 'no', 'Strong No', 'No') THEN rating END) | [{"table": "greenhouse__interview_scorecard_detail", "column": "rating"}] | [{"table": "greenhouse__interview_scorecard_detail", "column": "overall_recommendation"}] | False |
| B1 | AVG(CASE WHEN overall_recommendation = 'Maybe' THEN rating END) | [{"table": "greenhouse__interview_scorecard_detail", "column": "rating"}] | [{"table": "greenhouse__interview_scorecard_detail", "column": "overall_recommendation"}] | False |


## S51

类别 `data`；来源 `query_db`；调用 `86305a7bc9044dc98586339fd34d0d8e`；状态 `success`。

```sql
SELECT attribute_name, 
       COUNT(*) as cnt,
       AVG(rating) as avg_rating,
       ROUND(SUM(CASE WHEN rating >= 4 THEN 1 ELSE 0 END) * 100.0 / COUNT(*), 1) as high_score_pct
FROM greenhouse__interview_scorecard_detail
WHERE attribute_name IS NOT NULL AND rating IS NOT NULL
GROUP BY attribute_name
ORDER BY avg_rating DESC
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-067/attempt-01/sql/S51.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-067/attempt-01/sql/S51.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-067/attempt-01/results/S51.rows.jsonl)；完整：True；SHA256：`aaa8c7180ca6589edcddba0e0a35d7bcf5a5a95e77d195dbca60c61be5e10aac`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "greenhouse__interview_scorecard_detail", "kind": "base", "block": null, "base_tables": ["greenhouse__interview_scorecard_detail"]}] | [] | ["attribute_name"] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |
| B1 | AVG(rating) | [{"table": "greenhouse__interview_scorecard_detail", "column": "rating"}] | [] | False |
| B1 | COUNT(*) | [] | [] | True |
| B1 | SUM(CASE WHEN rating >= 4 THEN 1 ELSE 0 END) | [] | [{"table": "greenhouse__interview_scorecard_detail", "column": "rating"}] | False |


## S52

类别 `data`；来源 `query_db`；调用 `5a32111f141347ebb4f727dbfcee6f4e`；状态 `success`。

```sql
SELECT ie.interviewer_name, ie.job_title, ie.job_parent_departments, ie.overall_recommendation
FROM greenhouse__interview_enhanced ie
WHERE ie.interviewer_name IS NOT NULL AND ie.job_parent_departments IS NOT NULL
LIMIT 5
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-067/attempt-01/sql/S52.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-067/attempt-01/sql/S52.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-067/attempt-01/results/S52.rows.jsonl)；完整：True；SHA256：`1cdab143e5c21255fbfaa6605fa58ef136f67f3ff440494b61fc4cc61bc6b961`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "ie", "kind": "base", "block": null, "base_tables": ["greenhouse__interview_enhanced"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |


## S53

类别 `data`；来源 `query_db`；调用 `e0c358e6cb4d47318d83456cbb659437`；状态 `failed`。

```sql
SELECT sourced_from, COUNT(*) as cnt,
       AVG(EXTRACT(EPOCH FROM (last_activity_at - applied_at))/86400.0) as avg_days
FROM greenhouse__application_enhanced
GROUP BY sourced_from
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-067/attempt-01/sql/S53.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-067/attempt-01/sql/S53.parameters.json)。

错误：`OperationalError('near "FROM": syntax error')`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "greenhouse__application_enhanced", "kind": "base", "block": null, "base_tables": ["greenhouse__application_enhanced"]}] | [] | ["sourced_from"] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |
| B1 | AVG(EXTRACT(EPOCH FROM (last_activity_at - applied_at)) / 86400.0) | [{"table": "greenhouse__application_enhanced", "column": "last_activity_at"}, {"table": "greenhouse__application_enhanced", "column": "applied_at"}] | [] | False |


## S54

类别 `data`；来源 `query_db`；调用 `efc1a06d5667471fbab4789391d803a7`；状态 `success`。

```sql
SELECT status, COUNT(*) as cnt,
       AVG(candidate_quality_score) as avg_quality
FROM greenhouse__candidate_summary cs
JOIN greenhouse__application_enhanced ae USING (candidate_id)
GROUP BY status
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-067/attempt-01/sql/S54.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-067/attempt-01/sql/S54.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-067/attempt-01/results/S54.rows.jsonl)；完整：True；SHA256：`01aee20d84ebe72f2c85f424dc6a9689878a45dc35915d05883922c7b6abcc4d`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "cs", "kind": "base", "block": null, "base_tables": ["greenhouse__candidate_summary"]}, {"alias": "ae", "kind": "base", "block": null, "base_tables": ["greenhouse__application_enhanced"]}] | [{"type": "INNER", "right": "greenhouse__application_enhanced AS ae", "on": null, "using": ["candidate_id"]}] | ["status"] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |
| B1 | AVG(candidate_quality_score) | [{"table": "greenhouse__candidate_summary", "column": "candidate_quality_score"}] | [] | False |


## S55

类别 `data`；来源 `query_db`；调用 `dd8711ee3934470b90510e3be91b9b6a`；状态 `success`。

```sql
SELECT sourced_from, 
       AVG(julianday(last_activity_at) - julianday(applied_at)) as avg_days,
       MIN(julianday(last_activity_at) - julianday(applied_at)) as min_days,
       MAX(julianday(last_activity_at) - julianday(applied_at)) as max_days
FROM greenhouse__application_enhanced
WHERE last_activity_at IS NOT NULL AND applied_at IS NOT NULL
GROUP BY sourced_from
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-067/attempt-01/sql/S55.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-067/attempt-01/sql/S55.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-067/attempt-01/results/S55.rows.jsonl)；完整：True；SHA256：`e509bdcb5d06eb16600f620131638a9d7401176526be2f90f3227a9ec569596e`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "greenhouse__application_enhanced", "kind": "base", "block": null, "base_tables": ["greenhouse__application_enhanced"]}] | [] | ["sourced_from"] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | AVG(JULIANDAY(last_activity_at) - JULIANDAY(applied_at)) | [{"table": "greenhouse__application_enhanced", "column": "last_activity_at"}, {"table": "greenhouse__application_enhanced", "column": "applied_at"}] | [] | False |
| B1 | MIN(JULIANDAY(last_activity_at) - JULIANDAY(applied_at)) | [{"table": "greenhouse__application_enhanced", "column": "last_activity_at"}, {"table": "greenhouse__application_enhanced", "column": "applied_at"}] | [] | False |
| B1 | MAX(JULIANDAY(last_activity_at) - JULIANDAY(applied_at)) | [{"table": "greenhouse__application_enhanced", "column": "last_activity_at"}, {"table": "greenhouse__application_enhanced", "column": "applied_at"}] | [] | False |


## S56

类别 `data`；来源 `query_db`；调用 `75c0cbd9886c46e58c6653bb64179b2a`；状态 `success`。

```sql
SELECT current_job_stage, COUNT(*) as cnt,
       AVG(julianday(last_activity_at) - julianday(applied_at)) as avg_days_in_process
FROM greenhouse__application_enhanced
WHERE last_activity_at IS NOT NULL AND applied_at IS NOT NULL
GROUP BY current_job_stage
ORDER BY avg_days_in_process
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-067/attempt-01/sql/S56.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-067/attempt-01/sql/S56.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-067/attempt-01/results/S56.rows.jsonl)；完整：True；SHA256：`103552d452d3441f309e0a510a42ceec880732634e6b52d0e0f2928be3a91931`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "greenhouse__application_enhanced", "kind": "base", "block": null, "base_tables": ["greenhouse__application_enhanced"]}] | [] | ["current_job_stage"] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |
| B1 | AVG(JULIANDAY(last_activity_at) - JULIANDAY(applied_at)) | [{"table": "greenhouse__application_enhanced", "column": "last_activity_at"}, {"table": "greenhouse__application_enhanced", "column": "applied_at"}] | [] | False |


## S57

类别 `data`；来源 `query_db`；调用 `6bede44527c346ddb52f2b8a20eef4d1`；状态 `success`。

```sql
SELECT candidate_gender, COUNT(*) as cnt,
       ROUND(100.0 * SUM(CASE WHEN status='hired' THEN 1 ELSE 0 END) / COUNT(*), 1) as hire_rate
FROM greenhouse__application_enhanced
WHERE candidate_gender IS NOT NULL
GROUP BY candidate_gender
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-067/attempt-01/sql/S57.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-067/attempt-01/sql/S57.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-067/attempt-01/results/S57.rows.jsonl)；完整：True；SHA256：`ec631614d06e17614922800d0470b8de845384b4d7628f45983f19b21b584603`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "greenhouse__application_enhanced", "kind": "base", "block": null, "base_tables": ["greenhouse__application_enhanced"]}] | [] | ["candidate_gender"] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |
| B1 | COUNT(*) | [] | [] | True |
| B1 | SUM(CASE WHEN status = 'hired' THEN 1 ELSE 0 END) | [] | [{"table": "greenhouse__application_enhanced", "column": "status"}] | False |


## S58

类别 `data`；来源 `query_db`；调用 `a00b84c3b39845c79f358dab0fd2745a`；状态 `success`。

```sql
SELECT 
  CASE WHEN candidate_quality_score >= 4 THEN 'high_quality' ELSE 'low_quality' END as quality_tier,
  COUNT(*) as cnt,
  ROUND(100.0 * SUM(CASE WHEN status='hired' THEN 1 ELSE 0 END) / COUNT(*), 1) as hire_rate,
  AVG(candidate_quality_score) as avg_score
FROM greenhouse__application_enhanced ae
JOIN greenhouse__candidate_summary cs USING (candidate_id)
GROUP BY quality_tier
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-067/attempt-01/sql/S58.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-067/attempt-01/sql/S58.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-067/attempt-01/results/S58.rows.jsonl)；完整：True；SHA256：`5e974812ef910bd193d1abcb81fb744ca3d575f1012f294cf18ea834b6441253`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "ae", "kind": "base", "block": null, "base_tables": ["greenhouse__application_enhanced"]}, {"alias": "cs", "kind": "base", "block": null, "base_tables": ["greenhouse__candidate_summary"]}] | [{"type": "INNER", "right": "greenhouse__candidate_summary AS cs", "on": null, "using": ["candidate_id"]}] | ["CASE WHEN candidate_quality_score >= 4 THEN 'high_quality' ELSE 'low_quality' END"] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |
| B1 | AVG(candidate_quality_score) | [{"table": "greenhouse__candidate_summary", "column": "candidate_quality_score"}] | [] | False |
| B1 | COUNT(*) | [] | [] | True |
| B1 | SUM(CASE WHEN status = 'hired' THEN 1 ELSE 0 END) | [] | [{"table": "greenhouse__application_enhanced", "column": "status"}] | False |


## S59

类别 `data`；来源 `query_db`；调用 `47a8794443f841d18147ed2ac010fe57`；状态 `success`。

```sql
SELECT ae.sourced_from,
       ROUND(AVG(cs.candidate_quality_score), 2) as avg_quality,
       ROUND(AVG(cs.avg_interview_score), 2) as avg_interview_score,
       ROUND(AVG(cs.interview_success_rate), 2) as avg_int_success
FROM greenhouse__application_enhanced ae
JOIN greenhouse__candidate_summary cs USING (candidate_id)
GROUP BY ae.sourced_from
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-067/attempt-01/sql/S59.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-067/attempt-01/sql/S59.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-067/attempt-01/results/S59.rows.jsonl)；完整：True；SHA256：`6ef81500f096cd304de43e38eaa0bd335c5087d7fe87ce3261545a8056cf4924`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "ae", "kind": "base", "block": null, "base_tables": ["greenhouse__application_enhanced"]}, {"alias": "cs", "kind": "base", "block": null, "base_tables": ["greenhouse__candidate_summary"]}] | [{"type": "INNER", "right": "greenhouse__candidate_summary AS cs", "on": null, "using": ["candidate_id"]}] | ["ae.sourced_from"] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | AVG(cs.candidate_quality_score) | [{"table": "greenhouse__candidate_summary", "column": "candidate_quality_score"}] | [] | False |
| B1 | AVG(cs.avg_interview_score) | [{"table": "greenhouse__candidate_summary", "column": "avg_interview_score"}] | [] | False |
| B1 | AVG(cs.interview_success_rate) | [{"table": "greenhouse__candidate_summary", "column": "interview_success_rate"}] | [] | False |


## S60

类别 `data`；来源 `query_db`；调用 `c0131e1e78d340a7848761236874baeb`；状态 `success`。

```sql
SELECT COUNT(*) as total,
       SUM(CASE WHEN avg_interview_score IS NOT NULL THEN 1 ELSE 0 END) as with_score
FROM greenhouse__candidate_summary
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-067/attempt-01/sql/S60.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-067/attempt-01/sql/S60.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-067/attempt-01/results/S60.rows.jsonl)；完整：True；SHA256：`72e24897aeeae060be3e4d14d71b4444edd3653e93ae7e4eb576a23cd061a799`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "greenhouse__candidate_summary", "kind": "base", "block": null, "base_tables": ["greenhouse__candidate_summary"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |
| B1 | SUM(CASE WHEN NOT avg_interview_score IS NULL THEN 1 ELSE 0 END) | [] | [{"table": "greenhouse__candidate_summary", "column": "avg_interview_score"}] | False |


## S61

类别 `data`；来源 `python`；调用 `d6e5bdf2815e4fa88d507ad13e2495d3`；状态 `success`。

```sql

SELECT source_name, source_type, total_applications, unique_candidates, 
       total_hires, applications_with_interviews, avg_process_days,
       hire_rate, interview_rate, interview_to_hire_rate, efficiency_score
FROM greenhouse__talent_pipeline_simplified
ORDER BY source_name

```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-067/attempt-01/sql/S61.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-067/attempt-01/sql/S61.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-067/attempt-01/results/S61.rows.jsonl)；完整：True；SHA256：`70669de81a268c52539cd99f6a96c345b95ec460591f54705dd878ebb3441553`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "greenhouse__talent_pipeline_simplified", "kind": "base", "block": null, "base_tables": ["greenhouse__talent_pipeline_simplified"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |


## S62

类别 `data`；来源 `python`；调用 `d6e5bdf2815e4fa88d507ad13e2495d3`；状态 `success`。

```sql

SELECT 
  CASE 
    WHEN job_parent_departments LIKE '%Engineering%' THEN 'Engineering'
    WHEN job_parent_departments LIKE '%Product%' THEN 'Product'
    WHEN job_parent_departments LIKE '%Design%' THEN 'Design'
    WHEN job_parent_departments LIKE '%Marketing%' THEN 'Marketing'
    WHEN job_parent_departments LIKE '%Sales%' THEN 'Sales'
    ELSE 'Other'
  END as dept_group,
  COUNT(*) as applications,
  SUM(CASE WHEN status='hired' THEN 1 ELSE 0 END) as hires,
  ROUND(100.0 * SUM(CASE WHEN status='hired' THEN 1 ELSE 0 END) / COUNT(*), 1) as hire_rate,
  AVG(count_interviews) as avg_interviews
FROM greenhouse__application_enhanced
WHERE job_parent_departments IS NOT NULL
GROUP BY dept_group
ORDER BY hires DESC

```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-067/attempt-01/sql/S62.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-067/attempt-01/sql/S62.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-067/attempt-01/results/S62.rows.jsonl)；完整：True；SHA256：`3d3b2e973af417c792312c7b3b2f82df5c5a9181a5e48cb26794aa8d7726a6d3`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "greenhouse__application_enhanced", "kind": "base", "block": null, "base_tables": ["greenhouse__application_enhanced"]}] | [] | ["CASE WHEN job_parent_departments LIKE '%Engineering%' THEN 'Engineering' WHEN job_parent_departments LIKE '%Product%' THEN 'Product' WHEN job_parent_departments LIKE '%Design%' THEN 'Design' WHEN job_parent_departments LIKE '%Marketing%' THEN 'Marketing' WHEN job_parent_departments LIKE '%Sales%' THEN 'Sales' ELSE 'Other' END"] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |
| B1 | SUM(CASE WHEN status = 'hired' THEN 1 ELSE 0 END) | [] | [{"table": "greenhouse__application_enhanced", "column": "status"}] | False |
| B1 | AVG(count_interviews) | [{"table": "greenhouse__application_enhanced", "column": "count_interviews"}] | [] | False |
| B1 | COUNT(*) | [] | [] | True |
| B1 | SUM(CASE WHEN status = 'hired' THEN 1 ELSE 0 END) | [] | [{"table": "greenhouse__application_enhanced", "column": "status"}] | False |


## S63

类别 `data`；来源 `python`；调用 `d6e5bdf2815e4fa88d507ad13e2495d3`；状态 `success`。

```sql

SELECT sourced_from,
  SUM(CASE WHEN status='hired' THEN 1 ELSE 0 END) as hires,
  COUNT(*) as applications,
  ROUND(100.0 * SUM(CASE WHEN status='hired' THEN 1 ELSE 0 END) / COUNT(*), 1) as hire_rate
FROM greenhouse__application_enhanced
GROUP BY sourced_from
ORDER BY hires DESC

```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-067/attempt-01/sql/S63.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-067/attempt-01/sql/S63.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-067/attempt-01/results/S63.rows.jsonl)；完整：True；SHA256：`45417484026676207c5aec4be2edb3b24c32c4c346dc3cf55056193a00ef84fc`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "greenhouse__application_enhanced", "kind": "base", "block": null, "base_tables": ["greenhouse__application_enhanced"]}] | [] | ["sourced_from"] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | SUM(CASE WHEN status = 'hired' THEN 1 ELSE 0 END) | [] | [{"table": "greenhouse__application_enhanced", "column": "status"}] | False |
| B1 | COUNT(*) | [] | [] | True |
| B1 | COUNT(*) | [] | [] | True |
| B1 | SUM(CASE WHEN status = 'hired' THEN 1 ELSE 0 END) | [] | [{"table": "greenhouse__application_enhanced", "column": "status"}] | False |


## S64

类别 `data`；来源 `python`；调用 `d6e5bdf2815e4fa88d507ad13e2495d3`；状态 `success`。

```sql

SELECT 
  CASE 
    WHEN lower(overall_recommendation) IN ('strong_yes','yes') THEN 'Positive'
    WHEN lower(overall_recommendation) IN ('strong_no','no','maybe') THEN 'Non-Positive'
    ELSE 'Other'
  END as rec_group,
  COUNT(*) as cnt
FROM greenhouse__interview_enhanced
WHERE overall_recommendation IS NOT NULL
GROUP BY rec_group

```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-067/attempt-01/sql/S64.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-067/attempt-01/sql/S64.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-067/attempt-01/results/S64.rows.jsonl)；完整：True；SHA256：`2bcd24582f0aa9cae1ffe793b4a6ade0071b967085e48a75c35ad57a7cca1c2b`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "greenhouse__interview_enhanced", "kind": "base", "block": null, "base_tables": ["greenhouse__interview_enhanced"]}] | [] | ["CASE WHEN LOWER(overall_recommendation) IN ('strong_yes', 'yes') THEN 'Positive' WHEN LOWER(overall_recommendation) IN ('strong_no', 'no', 'maybe') THEN 'Non-Positive' ELSE 'Other' END"] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |


## S65

类别 `data`；来源 `python`；调用 `d6e5bdf2815e4fa88d507ad13e2495d3`；状态 `success`。

```sql

SELECT interview_name,
  COUNT(*) as total,
  ROUND(SUM(CASE WHEN lower(overall_recommendation) IN ('strong_yes','yes') THEN 1 ELSE 0 END) * 100.0 / COUNT(*), 1) as positive_pct,
  AVG(duration_interview_minutes) as avg_duration
FROM greenhouse__interview_enhanced
WHERE overall_recommendation IS NOT NULL
GROUP BY interview_name
ORDER BY total DESC

```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-067/attempt-01/sql/S65.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-067/attempt-01/sql/S65.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-067/attempt-01/results/S65.rows.jsonl)；完整：True；SHA256：`6e559952d52d32791b8e3a6e15b2267a71f638ffbf1fe09c73ccc66d04f3f4bc`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "greenhouse__interview_enhanced", "kind": "base", "block": null, "base_tables": ["greenhouse__interview_enhanced"]}] | [] | ["interview_name"] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |
| B1 | AVG(duration_interview_minutes) | [{"table": "greenhouse__interview_enhanced", "column": "duration_interview_minutes"}] | [] | False |
| B1 | COUNT(*) | [] | [] | True |
| B1 | SUM(CASE WHEN LOWER(overall_recommendation) IN ('strong_yes', 'yes') THEN 1 ELSE 0 END) | [] | [{"table": "greenhouse__interview_enhanced", "column": "overall_recommendation"}] | False |


## S66

类别 `data`；来源 `python`；调用 `d6e5bdf2815e4fa88d507ad13e2495d3`；状态 `success`。

```sql

SELECT attribute_name, 
  COUNT(*) as cnt,
  AVG(rating) as avg_rating
FROM greenhouse__interview_scorecard_detail
WHERE attribute_name IS NOT NULL AND rating IS NOT NULL
GROUP BY attribute_name
ORDER BY avg_rating DESC

```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-067/attempt-01/sql/S66.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-067/attempt-01/sql/S66.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-067/attempt-01/results/S66.rows.jsonl)；完整：True；SHA256：`48fa241541b452af3195604974e97b4dfac7e1d22ca1360174e8dd243f016a1d`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "greenhouse__interview_scorecard_detail", "kind": "base", "block": null, "base_tables": ["greenhouse__interview_scorecard_detail"]}] | [] | ["attribute_name"] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |
| B1 | AVG(rating) | [{"table": "greenhouse__interview_scorecard_detail", "column": "rating"}] | [] | False |


## S67

类别 `data`；来源 `python`；调用 `d6e5bdf2815e4fa88d507ad13e2495d3`；状态 `success`。

```sql
SELECT * FROM greenhouse__diversity_metrics
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-067/attempt-01/sql/S67.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-067/attempt-01/sql/S67.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-067/attempt-01/results/S67.rows.jsonl)；完整：True；SHA256：`9538399a73a519b1fd82f02b8ff9f8ecddd385c59835d9c616e397d187395a6f`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "greenhouse__diversity_metrics", "kind": "base", "block": null, "base_tables": ["greenhouse__diversity_metrics"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |


## S68

类别 `data`；来源 `python`；调用 `bce31ec3600f42958c825d8dfa54310b`；状态 `success`。

```sql

SELECT current_job_stage,
       COUNT(*) as cnt,
       SUM(CASE WHEN status='hired' THEN 1 ELSE 0 END) as hired,
       SUM(CASE WHEN status='withdrawn' THEN 1 ELSE 0 END) as withdrawn,
       SUM(CASE WHEN status='rejected' THEN 1 ELSE 0 END) as rejected,
       SUM(CASE WHEN status='active' THEN 1 ELSE 0 END) as active
FROM greenhouse__application_enhanced
GROUP BY current_job_stage
ORDER BY cnt DESC

```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-067/attempt-01/sql/S68.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-067/attempt-01/sql/S68.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-067/attempt-01/results/S68.rows.jsonl)；完整：True；SHA256：`0b44c9873ef18169341373f2e9894d7cf580869840b024e1603b7c4aa111932c`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "greenhouse__application_enhanced", "kind": "base", "block": null, "base_tables": ["greenhouse__application_enhanced"]}] | [] | ["current_job_stage"] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |
| B1 | SUM(CASE WHEN status = 'hired' THEN 1 ELSE 0 END) | [] | [{"table": "greenhouse__application_enhanced", "column": "status"}] | False |
| B1 | SUM(CASE WHEN status = 'withdrawn' THEN 1 ELSE 0 END) | [] | [{"table": "greenhouse__application_enhanced", "column": "status"}] | False |
| B1 | SUM(CASE WHEN status = 'rejected' THEN 1 ELSE 0 END) | [] | [{"table": "greenhouse__application_enhanced", "column": "status"}] | False |
| B1 | SUM(CASE WHEN status = 'active' THEN 1 ELSE 0 END) | [] | [{"table": "greenhouse__application_enhanced", "column": "status"}] | False |


## S69

类别 `data`；来源 `python`；调用 `bce31ec3600f42958c825d8dfa54310b`；状态 `success`。

```sql

SELECT sourced_from,
  COUNT(*) as apps,
  SUM(CASE WHEN count_interviews>0 THEN 1 ELSE 0 END) as interviewed,
  SUM(CASE WHEN status='hired' THEN 1 ELSE 0 END) as hired
FROM greenhouse__application_enhanced
GROUP BY sourced_from

```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-067/attempt-01/sql/S69.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-067/attempt-01/sql/S69.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-067/attempt-01/results/S69.rows.jsonl)；完整：True；SHA256：`44eae58c3599c9cbc3d0b56ecba7dbe232b867204f52f2fb15bb71ecc3a7431d`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "greenhouse__application_enhanced", "kind": "base", "block": null, "base_tables": ["greenhouse__application_enhanced"]}] | [] | ["sourced_from"] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |
| B1 | SUM(CASE WHEN count_interviews > 0 THEN 1 ELSE 0 END) | [] | [{"table": "greenhouse__application_enhanced", "column": "count_interviews"}] | False |
| B1 | SUM(CASE WHEN status = 'hired' THEN 1 ELSE 0 END) | [] | [{"table": "greenhouse__application_enhanced", "column": "status"}] | False |


## S70

类别 `data`；来源 `python`；调用 `bce31ec3600f42958c825d8dfa54310b`；状态 `success`。

```sql

SELECT scd.attribute_name, scd.rating, scd.overall_recommendation,
       scd.interview_name, scd.job_id,
       (SELECT status FROM greenhouse__application_enhanced ae WHERE ae.application_id = scd.application_id) as app_status
FROM greenhouse__interview_scorecard_detail scd
WHERE scd.rating IS NOT NULL
LIMIT 1000

```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-067/attempt-01/sql/S70.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-067/attempt-01/sql/S70.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-067/attempt-01/results/S70.rows.jsonl)；完整：True；SHA256：`5042ba695bd322a8bba9cf53acea43d5fc1a0375623de62efa2e4c801d30a6a2`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "ae", "kind": "base", "block": null, "base_tables": ["greenhouse__application_enhanced"]}] | [] | [] |
| B2 | [{"alias": "scd", "kind": "base", "block": null, "base_tables": ["greenhouse__interview_scorecard_detail"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |


未解析列血缘：[{"block": "B2", "column": "status", "reason": "ambiguous_or_missing_source"}]

## S71

类别 `data`；来源 `python`；调用 `bce31ec3600f42958c825d8dfa54310b`；状态 `success`。

```sql

SELECT 
  CASE 
    WHEN job_parent_departments LIKE '%Engineering%' THEN 'Engineering'
    WHEN job_parent_departments LIKE '%Product%' THEN 'Product'
    WHEN job_parent_departments LIKE '%Design%' THEN 'Design'
    WHEN job_parent_departments LIKE '%Marketing%' THEN 'Marketing'
    WHEN job_parent_departments LIKE '%Sales%' THEN 'Sales'
    ELSE 'Other'
  END as dept,
  SUM(CASE WHEN status='hired' AND candidate_gender='Female' THEN 1 ELSE 0 END) as fh,
  SUM(CASE WHEN status='hired' AND candidate_gender IS NOT NULL THEN 1 ELSE 0 END) as th_g,
  SUM(CASE WHEN status='hired' AND candidate_race != 'White' AND candidate_race IS NOT NULL THEN 1 ELSE 0 END) as nwh,
  SUM(CASE WHEN status='hired' AND candidate_race IS NOT NULL THEN 1 ELSE 0 END) as th_r
FROM greenhouse__application_enhanced
WHERE job_parent_departments IS NOT NULL
GROUP BY dept
ORDER BY th_g DESC

```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-067/attempt-01/sql/S71.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-067/attempt-01/sql/S71.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-067/attempt-01/results/S71.rows.jsonl)；完整：True；SHA256：`8aed72569f5ba4b37cc27c26bed9539bd67e672812e32a1068e3ac955eace053`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "greenhouse__application_enhanced", "kind": "base", "block": null, "base_tables": ["greenhouse__application_enhanced"]}] | [] | ["CASE WHEN job_parent_departments LIKE '%Engineering%' THEN 'Engineering' WHEN job_parent_departments LIKE '%Product%' THEN 'Product' WHEN job_parent_departments LIKE '%Design%' THEN 'Design' WHEN job_parent_departments LIKE '%Marketing%' THEN 'Marketing' WHEN job_parent_departments LIKE '%Sales%' THEN 'Sales' ELSE 'Other' END"] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | SUM(CASE WHEN status = 'hired' AND candidate_gender = 'Female' THEN 1 ELSE 0 END) | [] | [{"table": "greenhouse__application_enhanced", "column": "status"}, {"table": "greenhouse__application_enhanced", "column": "candidate_gender"}] | False |
| B1 | SUM(CASE WHEN status = 'hired' AND NOT candidate_gender IS NULL THEN 1 ELSE 0 END) | [] | [{"table": "greenhouse__application_enhanced", "column": "status"}, {"table": "greenhouse__application_enhanced", "column": "candidate_gender"}] | False |
| B1 | SUM(CASE WHEN status = 'hired' AND candidate_race <> 'White' AND NOT candidate_race IS NULL THEN 1 ELSE 0 END) | [] | [{"table": "greenhouse__application_enhanced", "column": "status"}, {"table": "greenhouse__application_enhanced", "column": "candidate_race"}, {"table": "greenhouse__application_enhanced", "column": "candidate_race"}] | False |
| B1 | SUM(CASE WHEN status = 'hired' AND NOT candidate_race IS NULL THEN 1 ELSE 0 END) | [] | [{"table": "greenhouse__application_enhanced", "column": "status"}, {"table": "greenhouse__application_enhanced", "column": "candidate_race"}] | False |


## S72

类别 `data`；来源 `python`；调用 `63668651247841d4888e3be593d2ad2d`；状态 `success`。

```sql

SELECT 
  CASE 
    WHEN job_parent_departments LIKE '%Engineering%' THEN 'Engineering'
    WHEN job_parent_departments LIKE '%Product%' THEN 'Product'
    WHEN job_parent_departments LIKE '%Design%' THEN 'Design'
    WHEN job_parent_departments LIKE '%Marketing%' THEN 'Marketing'
    WHEN job_parent_departments LIKE '%Sales%' THEN 'Sales'
    ELSE 'Other'
  END as dept,
  COUNT(*) as apps,
  SUM(CASE WHEN status='hired' THEN 1 ELSE 0 END) as hires,
  ROUND(100.0 * SUM(CASE WHEN status='hired' THEN 1 ELSE 0 END) / COUNT(*), 1) as hire_rate
FROM greenhouse__application_enhanced
WHERE job_parent_departments IS NOT NULL
GROUP BY dept
ORDER BY hires DESC

```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-067/attempt-01/sql/S72.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-067/attempt-01/sql/S72.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-067/attempt-01/results/S72.rows.jsonl)；完整：True；SHA256：`03f05de66f7b743242dc350b44434b056cef83db8ae13486261a1579fd78c837`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "greenhouse__application_enhanced", "kind": "base", "block": null, "base_tables": ["greenhouse__application_enhanced"]}] | [] | ["CASE WHEN job_parent_departments LIKE '%Engineering%' THEN 'Engineering' WHEN job_parent_departments LIKE '%Product%' THEN 'Product' WHEN job_parent_departments LIKE '%Design%' THEN 'Design' WHEN job_parent_departments LIKE '%Marketing%' THEN 'Marketing' WHEN job_parent_departments LIKE '%Sales%' THEN 'Sales' ELSE 'Other' END"] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |
| B1 | SUM(CASE WHEN status = 'hired' THEN 1 ELSE 0 END) | [] | [{"table": "greenhouse__application_enhanced", "column": "status"}] | False |
| B1 | COUNT(*) | [] | [] | True |
| B1 | SUM(CASE WHEN status = 'hired' THEN 1 ELSE 0 END) | [] | [{"table": "greenhouse__application_enhanced", "column": "status"}] | False |


## S73

类别 `data`；来源 `python`；调用 `a8a8faba319146cfa11ea3c59529ea26`；状态 `success`。

```sql

SELECT ie.application_id, ie.interviewer_name, ie.job_title, 
       ie.job_parent_departments as job_depts,
       ie.overall_recommendation, ie.interviewer_is_hiring_manager,
       ae.status as app_status, ae.job_parent_departments as app_job_depts
FROM greenhouse__interview_enhanced ie
JOIN greenhouse__application_enhanced ae ON ie.application_id = ae.application_id
WHERE ie.overall_recommendation IS NOT NULL AND ie.job_parent_departments IS NOT NULL

```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-067/attempt-01/sql/S73.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-067/attempt-01/sql/S73.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-067/attempt-01/results/S73.rows.jsonl)；完整：True；SHA256：`7a76da694b704294e54a02090ac40e398fc9bf310510cc80b19ffb63894fd4e0`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "ie", "kind": "base", "block": null, "base_tables": ["greenhouse__interview_enhanced"]}, {"alias": "ae", "kind": "base", "block": null, "base_tables": ["greenhouse__application_enhanced"]}] | [{"type": "INNER", "right": "greenhouse__application_enhanced AS ae", "on": "ie.application_id = ae.application_id", "using": []}] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |


## S74

类别 `data`；来源 `python`；调用 `a8a8faba319146cfa11ea3c59529ea26`；状态 `success`。

```sql

SELECT ie.overall_recommendation, ie.duration_interview_minutes,
       ie.interview_name, ie.job_parent_departments,
       ae.status as app_status
FROM greenhouse__interview_enhanced ie
JOIN greenhouse__application_enhanced ae ON ie.application_id = ae.application_id
WHERE ie.overall_recommendation IS NOT NULL AND ie.duration_interview_minutes IS NOT NULL

```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-067/attempt-01/sql/S74.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-067/attempt-01/sql/S74.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-067/attempt-01/results/S74.rows.jsonl)；完整：True；SHA256：`c15e0644f8051e5a432fa81af295a4ddbb3b9ea15f5fcb266b9f3023aaf19cb3`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "ie", "kind": "base", "block": null, "base_tables": ["greenhouse__interview_enhanced"]}, {"alias": "ae", "kind": "base", "block": null, "base_tables": ["greenhouse__application_enhanced"]}] | [{"type": "INNER", "right": "greenhouse__application_enhanced AS ae", "on": "ie.application_id = ae.application_id", "using": []}] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |


## S75

类别 `data`；来源 `python`；调用 `a8a8faba319146cfa11ea3c59529ea26`；状态 `success`。

```sql

SELECT current_job_stage,
  COUNT(*) as total,
  SUM(CASE WHEN status='hired' THEN 1 ELSE 0 END) as hired,
  SUM(CASE WHEN status='rejected' THEN 1 ELSE 0 END) as rejected,
  SUM(CASE WHEN status='withdrawn' THEN 1 ELSE 0 END) as withdrawn,
  SUM(CASE WHEN status='active' THEN 1 ELSE 0 END) as active
FROM greenhouse__application_enhanced
GROUP BY current_job_stage
ORDER BY 
  CASE current_job_stage
    WHEN 'Application Review' THEN 1
    WHEN 'Phone Screen' THEN 2
    WHEN 'Technical Interview' THEN 3
    WHEN 'Panel Interview' THEN 4
    WHEN 'Final Interview' THEN 5
    WHEN 'Offer' THEN 6
    ELSE 7
  END

```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-067/attempt-01/sql/S75.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-067/attempt-01/sql/S75.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-067/attempt-01/results/S75.rows.jsonl)；完整：True；SHA256：`6d23cb7959305a38f534fff5654a3fee3831739d4ef44af190c8f68a74b6b01a`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "greenhouse__application_enhanced", "kind": "base", "block": null, "base_tables": ["greenhouse__application_enhanced"]}] | [] | ["current_job_stage"] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |
| B1 | SUM(CASE WHEN status = 'hired' THEN 1 ELSE 0 END) | [] | [{"table": "greenhouse__application_enhanced", "column": "status"}] | False |
| B1 | SUM(CASE WHEN status = 'rejected' THEN 1 ELSE 0 END) | [] | [{"table": "greenhouse__application_enhanced", "column": "status"}] | False |
| B1 | SUM(CASE WHEN status = 'withdrawn' THEN 1 ELSE 0 END) | [] | [{"table": "greenhouse__application_enhanced", "column": "status"}] | False |
| B1 | SUM(CASE WHEN status = 'active' THEN 1 ELSE 0 END) | [] | [{"table": "greenhouse__application_enhanced", "column": "status"}] | False |


## S76

类别 `data`；来源 `python`；调用 `a8a8faba319146cfa11ea3c59529ea26`；状态 `success`。

```sql

SELECT scd.interview_name,
  AVG(scd.rating) as avg_rating,
  COUNT(*) as cnt,
  ROUND(SUM(CASE WHEN scd.rating >= 4 THEN 1 ELSE 0 END) * 100.0 / COUNT(*), 1) as high_score_pct
FROM greenhouse__interview_scorecard_detail scd
WHERE scd.rating IS NOT NULL AND scd.interview_name IS NOT NULL
GROUP BY scd.interview_name
ORDER BY avg_rating DESC

```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-067/attempt-01/sql/S76.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-067/attempt-01/sql/S76.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-067/attempt-01/results/S76.rows.jsonl)；完整：True；SHA256：`91e4f283d37b5682d53639853501b8faa7a34fbb28bae761c68c4d135086be04`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "scd", "kind": "base", "block": null, "base_tables": ["greenhouse__interview_scorecard_detail"]}] | [] | ["scd.interview_name"] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | AVG(scd.rating) | [{"table": "greenhouse__interview_scorecard_detail", "column": "rating"}] | [] | False |
| B1 | COUNT(*) | [] | [] | True |
| B1 | COUNT(*) | [] | [] | True |
| B1 | SUM(CASE WHEN scd.rating >= 4 THEN 1 ELSE 0 END) | [] | [{"table": "greenhouse__interview_scorecard_detail", "column": "rating"}] | False |


## S77

类别 `data`；来源 `python`；调用 `a8a8faba319146cfa11ea3c59529ea26`；状态 `success`。

```sql

SELECT ie.interview_name,
  COUNT(DISTINCT ie.application_id) as candidates,
  SUM(CASE WHEN ae.status='hired' THEN 1 ELSE 0 END) as hired,
  ROUND(100.0 * SUM(CASE WHEN ae.status='hired' THEN 1 ELSE 0 END) / COUNT(DISTINCT ie.application_id), 1) as hire_rate
FROM greenhouse__interview_enhanced ie
JOIN greenhouse__application_enhanced ae ON ie.application_id = ae.application_id
GROUP BY ie.interview_name
ORDER BY hire_rate DESC

```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-067/attempt-01/sql/S77.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-067/attempt-01/sql/S77.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-067/attempt-01/results/S77.rows.jsonl)；完整：True；SHA256：`c304f685eff9512ed02bbd27a9de651b043096514099041af1d516420ba4687d`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "ie", "kind": "base", "block": null, "base_tables": ["greenhouse__interview_enhanced"]}, {"alias": "ae", "kind": "base", "block": null, "base_tables": ["greenhouse__application_enhanced"]}] | [{"type": "INNER", "right": "greenhouse__application_enhanced AS ae", "on": "ie.application_id = ae.application_id", "using": []}] | ["ie.interview_name"] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(DISTINCT ie.application_id) | [{"table": "greenhouse__interview_enhanced", "column": "application_id"}] | [] | False |
| B1 | SUM(CASE WHEN ae.status = 'hired' THEN 1 ELSE 0 END) | [] | [{"table": "greenhouse__application_enhanced", "column": "status"}] | False |
| B1 | COUNT(DISTINCT ie.application_id) | [{"table": "greenhouse__interview_enhanced", "column": "application_id"}] | [] | False |
| B1 | SUM(CASE WHEN ae.status = 'hired' THEN 1 ELSE 0 END) | [] | [{"table": "greenhouse__application_enhanced", "column": "status"}] | False |


## S78

类别 `data`；来源 `python`；调用 `93ea9d98c4ee4dfcb1ffe6f9b958894a`；状态 `success`。

```sql

SELECT ie.application_id, ie.interviewer_name, ie.job_title,
       ie.job_parent_departments as job_depts,
       ie.overall_recommendation,
       ie.interview_name,
       ae.status as app_status
FROM greenhouse__interview_enhanced ie
LEFT JOIN greenhouse__application_enhanced ae ON ie.application_id = ae.application_id
WHERE ie.overall_recommendation IS NOT NULL

```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-067/attempt-01/sql/S78.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-067/attempt-01/sql/S78.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-067/attempt-01/results/S78.rows.jsonl)；完整：True；SHA256：`7225636f12087de52f48315052f9fefff5fd6f2f1c4e16019242e7e274ba15e9`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "ie", "kind": "base", "block": null, "base_tables": ["greenhouse__interview_enhanced"]}, {"alias": "ae", "kind": "base", "block": null, "base_tables": ["greenhouse__application_enhanced"]}] | [{"type": "LEFT", "right": "greenhouse__application_enhanced AS ae", "on": "ie.application_id = ae.application_id", "using": []}] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |


## S79

类别 `data`；来源 `python`；调用 `93ea9d98c4ee4dfcb1ffe6f9b958894a`；状态 `success`。

```sql

SELECT scd.scorecard_id, scd.rating, scd.attribute_name,
       scd.overall_recommendation, scd.interview_name, scd.application_id,
       (SELECT status FROM greenhouse__application_enhanced ae WHERE ae.application_id = scd.application_id) as app_status
FROM greenhouse__interview_scorecard_detail scd
WHERE scd.rating IS NOT NULL AND scd.overall_recommendation IS NOT NULL

```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-067/attempt-01/sql/S79.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-067/attempt-01/sql/S79.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-067/attempt-01/results/S79.rows.jsonl)；完整：True；SHA256：`c2268bed18eae4d5d8762934115815ea0b6d7c3cf819b7a682fcb54505c53293`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "ae", "kind": "base", "block": null, "base_tables": ["greenhouse__application_enhanced"]}] | [] | [] |
| B2 | [{"alias": "scd", "kind": "base", "block": null, "base_tables": ["greenhouse__interview_scorecard_detail"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |


未解析列血缘：[{"block": "B2", "column": "status", "reason": "ambiguous_or_missing_source"}]

## S80

类别 `data`；来源 `python`；调用 `8339d1033a004905a1df96a28e0d5a0c`；状态 `success`。

```sql

SELECT scorecard_id, 
       AVG(rating) as avg_scorecard_rating,
       MAX(rating) as max_rating,
       MIN(rating) as min_rating,
       overall_recommendation
FROM greenhouse__interview_scorecard_detail
WHERE rating IS NOT NULL
GROUP BY scorecard_id

```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-067/attempt-01/sql/S80.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-067/attempt-01/sql/S80.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-067/attempt-01/results/S80.rows.jsonl)；完整：True；SHA256：`b0254de2911e2bf74bf1ab9b0bffe2f836ca27e09b644853c0256eebfa5e8aa7`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "greenhouse__interview_scorecard_detail", "kind": "base", "block": null, "base_tables": ["greenhouse__interview_scorecard_detail"]}] | [] | ["scorecard_id"] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | AVG(rating) | [{"table": "greenhouse__interview_scorecard_detail", "column": "rating"}] | [] | False |
| B1 | MAX(rating) | [{"table": "greenhouse__interview_scorecard_detail", "column": "rating"}] | [] | False |
| B1 | MIN(rating) | [{"table": "greenhouse__interview_scorecard_detail", "column": "rating"}] | [] | False |


## S81

类别 `data`；来源 `python`；调用 `8339d1033a004905a1df96a28e0d5a0c`；状态 `success`。

```sql

SELECT scd.application_id,
       AVG(scd.rating) as avg_candidate_rating,
       COUNT(scd.scorecard_id) as num_scorecards
FROM greenhouse__interview_scorecard_detail scd
WHERE scd.rating IS NOT NULL
GROUP BY scd.application_id

```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-067/attempt-01/sql/S81.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-067/attempt-01/sql/S81.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-067/attempt-01/results/S81.rows.jsonl)；完整：True；SHA256：`61293d9f600c69590c89058c5cac72223b890699d143bbc6d7ac63beaacbec8e`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "scd", "kind": "base", "block": null, "base_tables": ["greenhouse__interview_scorecard_detail"]}] | [] | ["scd.application_id"] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | AVG(scd.rating) | [{"table": "greenhouse__interview_scorecard_detail", "column": "rating"}] | [] | False |
| B1 | COUNT(scd.scorecard_id) | [{"table": "greenhouse__interview_scorecard_detail", "column": "scorecard_id"}] | [] | False |


## S82

类别 `data`；来源 `python`；调用 `8339d1033a004905a1df96a28e0d5a0c`；状态 `success`。

```sql
SELECT AVG(rating) as avg_all FROM greenhouse__interview_scorecard_detail WHERE rating IS NOT NULL
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-067/attempt-01/sql/S82.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-067/attempt-01/sql/S82.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-067/attempt-01/results/S82.rows.jsonl)；完整：True；SHA256：`6784fdfac03bb6c57fe3f3b1aa0b7337e51bc8dc733bb28f71899d3a996626a7`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "greenhouse__interview_scorecard_detail", "kind": "base", "block": null, "base_tables": ["greenhouse__interview_scorecard_detail"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | AVG(rating) | [{"table": "greenhouse__interview_scorecard_detail", "column": "rating"}] | [] | False |


## S83

类别 `data`；来源 `python`；调用 `8339d1033a004905a1df96a28e0d5a0c`；状态 `success`。

```sql
SELECT AVG(avg_interview_score) as avg FROM greenhouse__candidate_summary WHERE avg_interview_score IS NOT NULL
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-067/attempt-01/sql/S83.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-067/attempt-01/sql/S83.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-067/attempt-01/results/S83.rows.jsonl)；完整：True；SHA256：`1ce04c0d3df1ce17b3cda6d3e9c45eb5a14aaf7e2dd7caeafdb8d4e465d1762a`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "greenhouse__candidate_summary", "kind": "base", "block": null, "base_tables": ["greenhouse__candidate_summary"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | AVG(avg_interview_score) | [{"table": "greenhouse__candidate_summary", "column": "avg_interview_score"}] | [] | False |


## S84

类别 `data`；来源 `python`；调用 `8339d1033a004905a1df96a28e0d5a0c`；状态 `success`。

```sql
SELECT AVG(avg_job_rating) as avg FROM greenhouse__job_enhanced WHERE avg_job_rating IS NOT NULL
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-067/attempt-01/sql/S84.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-067/attempt-01/sql/S84.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-067/attempt-01/results/S84.rows.jsonl)；完整：True；SHA256：`87d0508bb2218165a94e4154abf37bb2803f1c077c5184d7a57e295d6e9a977a`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "greenhouse__job_enhanced", "kind": "base", "block": null, "base_tables": ["greenhouse__job_enhanced"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | AVG(avg_job_rating) | [{"table": "greenhouse__job_enhanced", "column": "avg_job_rating"}] | [] | False |


## S85

类别 `data`；来源 `python`；调用 `8339d1033a004905a1df96a28e0d5a0c`；状态 `success`。

```sql

SELECT rating, COUNT(*) as cnt
FROM greenhouse__interview_scorecard_detail
WHERE rating IS NOT NULL
GROUP BY rating
ORDER BY rating

```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-067/attempt-01/sql/S85.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-067/attempt-01/sql/S85.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-067/attempt-01/results/S85.rows.jsonl)；完整：True；SHA256：`88324058573306529c7530a661b066e6034c8edb8c74fe8a5bb5789835a2dc93`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "greenhouse__interview_scorecard_detail", "kind": "base", "block": null, "base_tables": ["greenhouse__interview_scorecard_detail"]}] | [] | ["rating"] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |


## S86

类别 `data`；来源 `python`；调用 `8339d1033a004905a1df96a28e0d5a0c`；状态 `success`。

```sql

SELECT 
  CASE 
    WHEN lower(overall_recommendation) IN ('strong_yes', 'strong yes') THEN 5
    WHEN lower(overall_recommendation) IN ('yes') THEN 4
    WHEN lower(overall_recommendation) IN ('maybe') THEN 3
    WHEN lower(overall_recommendation) IN ('no') THEN 2
    WHEN lower(overall_recommendation) IN ('strong_no', 'strong no') THEN 1
    ELSE NULL
  END as rec_score,
  COUNT(*) as cnt
FROM greenhouse__interview_enhanced
WHERE overall_recommendation IS NOT NULL
GROUP BY rec_score
ORDER BY rec_score

```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-067/attempt-01/sql/S86.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-067/attempt-01/sql/S86.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-067/attempt-01/results/S86.rows.jsonl)；完整：True；SHA256：`b4fb24c461aaddfcfb238d7835816edae0af27262c31410e9f247e13cd6ca2a3`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "greenhouse__interview_enhanced", "kind": "base", "block": null, "base_tables": ["greenhouse__interview_enhanced"]}] | [] | ["CASE WHEN LOWER(overall_recommendation) IN ('strong_yes', 'strong yes') THEN 5 WHEN LOWER(overall_recommendation) IN ('yes') THEN 4 WHEN LOWER(overall_recommendation) IN ('maybe') THEN 3 WHEN LOWER(overall_recommendation) IN ('no') THEN 2 WHEN LOWER(overall_recommendation) IN ('strong_no', 'strong no') THEN 1 ELSE NULL END"] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |


## S87

类别 `data`；来源 `query_db`；调用 `c4b4eeaa3e59452fb8e1f391d53886d9`；状态 `success`。

```sql
SELECT interview_name, status, COUNT(*) as cnt
FROM greenhouse__interview_enhanced
GROUP BY interview_name, status
ORDER BY interview_name, cnt DESC
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-067/attempt-01/sql/S87.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-067/attempt-01/sql/S87.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-067/attempt-01/results/S87.rows.jsonl)；完整：True；SHA256：`39b177106e6da1dde18b959aa4c98d4d48a624012587ce2cbcfa64577a079ee2`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "greenhouse__interview_enhanced", "kind": "base", "block": null, "base_tables": ["greenhouse__interview_enhanced"]}] | [] | ["interview_name", "status"] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |


## S88

类别 `data`；来源 `query_db`；调用 `aebbe029a4ea43a2b3f32eaaf6e609c2`；状态 `success`。

```sql
SELECT count_interviews, 
       COUNT(*) as apps,
       SUM(CASE WHEN status='hired' THEN 1 ELSE 0 END) as hired,
       ROUND(100.0 * SUM(CASE WHEN status='hired' THEN 1 ELSE 0 END) / COUNT(*), 1) as hire_rate
FROM greenhouse__application_enhanced
WHERE count_interviews > 0
GROUP BY count_interviews
ORDER BY count_interviews
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-067/attempt-01/sql/S88.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-067/attempt-01/sql/S88.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-067/attempt-01/results/S88.rows.jsonl)；完整：True；SHA256：`aa907a2a603464dc8549b71e8786d818eee86badeec62a3aa51cae8f819f774b`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "greenhouse__application_enhanced", "kind": "base", "block": null, "base_tables": ["greenhouse__application_enhanced"]}] | [] | ["count_interviews"] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |
| B1 | SUM(CASE WHEN status = 'hired' THEN 1 ELSE 0 END) | [] | [{"table": "greenhouse__application_enhanced", "column": "status"}] | False |
| B1 | COUNT(*) | [] | [] | True |
| B1 | SUM(CASE WHEN status = 'hired' THEN 1 ELSE 0 END) | [] | [{"table": "greenhouse__application_enhanced", "column": "status"}] | False |


## S89

类别 `data`；来源 `query_db`；调用 `2500f19f2158414a9be13ef38db4ca36`；状态 `success`。

```sql
SELECT COUNT(*) as total_scorecards, 
       SUM(CASE WHEN scorecard_submitted_at IS NOT NULL THEN 1 ELSE 0 END) as submitted,
       ROUND(100.0 * SUM(CASE WHEN scorecard_submitted_at IS NOT NULL THEN 1 ELSE 0 END) / COUNT(*), 1) as submission_rate
FROM greenhouse__interview_enhanced
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-067/attempt-01/sql/S89.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-067/attempt-01/sql/S89.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-067/attempt-01/results/S89.rows.jsonl)；完整：True；SHA256：`e4f8e61401f40b7074c7c6ba99975d2bee07f1106cdc35e95b12ea1531ea5c24`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "greenhouse__interview_enhanced", "kind": "base", "block": null, "base_tables": ["greenhouse__interview_enhanced"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |
| B1 | SUM(CASE WHEN NOT scorecard_submitted_at IS NULL THEN 1 ELSE 0 END) | [] | [{"table": "greenhouse__interview_enhanced", "column": "scorecard_submitted_at"}] | False |
| B1 | COUNT(*) | [] | [] | True |
| B1 | SUM(CASE WHEN NOT scorecard_submitted_at IS NULL THEN 1 ELSE 0 END) | [] | [{"table": "greenhouse__interview_enhanced", "column": "scorecard_submitted_at"}] | False |


## S90

类别 `data`；来源 `query_db`；调用 `8e3826a879d84270b4b110ede3ad5676`；状态 `success`。

```sql
SELECT status, COUNT(*) as cnt, 
       ROUND(100.0 * COUNT(*) / (SELECT COUNT(*) FROM greenhouse__interview_enhanced), 1) as pct
FROM greenhouse__interview_enhanced
GROUP BY status
ORDER BY cnt DESC
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-067/attempt-01/sql/S90.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-067/attempt-01/sql/S90.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-067/attempt-01/results/S90.rows.jsonl)；完整：True；SHA256：`9e3fb12849a8eb1cb09bcc2e59525e56dfbbd4e4e1f467b82c0ffe31a50d6e55`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "greenhouse__interview_enhanced", "kind": "base", "block": null, "base_tables": ["greenhouse__interview_enhanced"]}] | [] | [] |
| B2 | [{"alias": "greenhouse__interview_enhanced", "kind": "base", "block": null, "base_tables": ["greenhouse__interview_enhanced"]}] | [] | ["status"] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |
| B2 | COUNT(*) | [] | [] | True |
| B2 | COUNT(*) | [] | [] | True |


## S91

类别 `data`；来源 `query_db`；调用 `0d10276f277140a099ff162c397b638c`；状态 `success`。

```sql
SELECT interview_name, status, COUNT(*) as cnt
FROM greenhouse__interview_enhanced
GROUP BY interview_name, status
ORDER BY interview_name, status
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-067/attempt-01/sql/S91.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-067/attempt-01/sql/S91.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-067/attempt-01/results/S91.rows.jsonl)；完整：True；SHA256：`15f32ac5b70327c13d4c037008e4f443fd490275e3d94eed68db404941b0fb7f`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "greenhouse__interview_enhanced", "kind": "base", "block": null, "base_tables": ["greenhouse__interview_enhanced"]}] | [] | ["interview_name", "status"] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |

