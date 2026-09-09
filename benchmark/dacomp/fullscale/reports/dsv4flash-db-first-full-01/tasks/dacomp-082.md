# dacomp-082

We are re-evaluating the return on investment (ROI) for each distribution channel but have…

运行：已提交。官方未评分。全部 SQL 尝试/成功 38/36；数据 SQL 36/34；Python 6 次。

完整原题：

We are re-evaluating the return on investment (ROI) for each distribution channel but have found that looking at `completion_rate` and `efficiency_score` alone is insufficient. Could you conduct a comprehensive, in-depth analysis of channel effectiveness? You will need to build a channel ROI evaluation model by combining the performance data from the `qualtrics__channel_performance` table, the project type distribution from the `qualtrics__survey` table, and the user lifecycle value from the `qualtrics__contact` table. Pay special attention to the performance differences of each channel across different `project_category` values (feedback, research, evaluation), as well as the value contribution distribution of user cohorts within each channel. The final deliverable should be a data-driven channel budget reallocation plan, including the optimal investment ratio for each channel and a forecast of expected returns.

| 表 | 行数 | 列数 |
| --- | --- | --- |
| qualtrics__channel_performance | 5 | 17 |
| qualtrics__contact | 4000 | 35 |
| qualtrics__survey | 8240 | 55 |


实际路线（分析者依据 SQL/源码概括，不代表 Agent 自述）：SQL 汇总渠道、项目类型和用户群 → Python 构建渠道评分、权重与回报情景 → 预算分配图表。

数据库大小：4,276,224 字节。

## 数据 SQL

| SQL | 状态 | 基础表 | Join 输入/类型 | GROUP BY | 聚合表达式 | 结果行数 | 数据库 ms |
| --- | --- | --- | --- | --- | --- | --- | --- |
| [S3/Q1](#s3) | success | ["qualtrics__channel_performance"] | 0 / {} | [] | [] | 5 | 0.512 |
| [S4/Q2](#s4) | success | ["qualtrics__survey"] | 0 / {} | [] | [] | 9 | 3.876 |
| [S5/Q3](#s5) | success | ["qualtrics__contact"] | 0 / {} | [] | ["COUNT(*)"] | 1 | 0.777 |
| [S6/Q4](#s6) | success | ["qualtrics__channel_performance"] | 0 / {} | [] | [] | 5 | 0.343 |
| [S7/Q5](#s7) | success | ["qualtrics__survey"] | 0 / {} | ["project_category"] | ["COUNT(*)", "SUM(count_survey_responses)", "SUM(count_completed_survey_responses)"] | 3 | 5.249 |
| [S8/Q6](#s8) | success | ["qualtrics__survey"] | 0 / {} | [] | [] | 5 | 0.521 |
| [S9/Q7](#s9) | success | ["qualtrics__survey"] | 0 / {} | ["project_category"] | ["SUM(count_email_survey_responses)", "SUM(count_email_completed_survey_responses)", "SUM(count_sms_survey_responses)", "SUM(count_sms_completed_survey_responses)", "SUM(count_social_media_survey_responses)", "SUM(count_social_media_completed_survey_responses)", "SUM(count_personal_link_survey_responses)", "SUM(count_personal_link_completed_survey_responses)", "SUM(count_qr_code_survey_responses)", "SUM(count_qr_code_completed_survey_responses)", "SUM(count_anonymous_survey_responses)", "SUM(count_anonymous_completed_survey_responses)", "SUM(count_uncategorized_survey_responses)", "SUM(count_uncategorized_completed_survey_responses)"] | 3 | 15.155 |
| [S10/Q8](#s10) | success | ["qualtrics__contact"] | 0 / {} | ["email_domain"] | ["COUNT(*)"] | 5 | 1.812 |
| [S11/Q9](#s11) | success | ["qualtrics__contact"] | 0 / {} | [] | ["MIN(total_count_surveys)", "AVG(total_count_surveys)", "MAX(total_count_surveys)", "MIN(total_count_completed_surveys)", "AVG(total_count_completed_surveys)", "MAX(total_count_completed_surveys)", "MIN(avg_survey_progress_pct)", "AVG(avg_survey_progress_pct)", "MAX(avg_survey_progress_pct)", "MIN(avg_survey_duration_in_seconds)", "AVG(avg_survey_duration_in_seconds)", "MAX(avg_survey_duration_in_seconds)"] | 1 | 2.565 |
| [S12/Q10](#s12) | success | ["qualtrics__contact"] | 0 / {} | [] | ["COUNT(*)", "SUM(CASE WHEN count_surveys_sent_email > 0 THEN 1 ELSE 0 END)", "SUM(CASE WHEN count_surveys_sent_sms > 0 THEN 1 ELSE 0 END)", "SUM(CASE WHEN count_surveys_sent_email > 0 AND count_surveys_sent_sms > 0 THEN 1 ELSE 0 END)", "SUM(count_surveys_sent_email)", "SUM(count_surveys_sent_sms)", "SUM(count_surveys_opened_email)", "SUM(count_surveys_opened_sms)", "SUM(count_surveys_started_email)", "SUM(count_surveys_started_sms)", "SUM(count_surveys_completed_email)", "SUM(count_surveys_completed_sms)"] | 1 | 2.645 |
| [S13/Q11](#s13) | success | ["qualtrics__survey"] | 0 / {} | [] | ["SUM(CASE WHEN count_email_survey_responses > 0 THEN 1 ELSE 0 END)", "SUM(CASE WHEN count_sms_survey_responses > 0 THEN 1 ELSE 0 END)", "SUM(CASE WHEN count_social_media_survey_responses > 0 THEN 1 ELSE 0 END)", "SUM(CASE WHEN count_personal_link_survey_responses > 0 THEN 1 ELSE 0 END)", "SUM(CASE WHEN count_qr_code_survey_responses > 0 THEN 1 ELSE 0 END)", "SUM(CASE WHEN count_anonymous_survey_responses > 0 THEN 1 ELSE 0 END)", "SUM(CASE WHEN count_uncategorized_survey_responses > 0 THEN 1 ELSE 0 END)"] | 1 | 4.749 |
| [S14/Q12](#s14) | success | ["qualtrics__survey"] | 0 / {} | [] | ["SUM(count_survey_responses)", "SUM(count_completed_survey_responses)", "COUNT(*)"] | 1 | 2.782 |
| [S15/Q13](#s15) | success | ["qualtrics__contact"] | 0 / {} | ["CASE WHEN total_count_completed_surveys = 0 THEN '0_inactive' WHEN total_count_completed_surveys <= 2 THEN '1_low' WHEN total_count_completed_surveys <= 6 THEN '2_mid' ELSE '3_high' END"] | ["COUNT(*)", "AVG(avg_survey_progress_pct)", "AVG(avg_survey_duration_in_seconds)", "AVG(total_count_surveys)", "AVG(count_surveys_completed_email)", "AVG(count_surveys_completed_sms)", "AVG(count_surveys_opened_email * 1.0 / NULLIF(count_surveys_sent_email, 0))", "AVG(count_surveys_opened_sms * 1.0 / NULLIF(count_surveys_sent_sms, 0))"] | 4 | 4.371 |
| [S16/Q14](#s16) | success | ["qualtrics__contact"] | 0 / {} | ["CASE WHEN count_surveys_sent_email > count_surveys_sent_sms THEN 'email_dominant' WHEN count_surveys_sent_sms > count_surveys_sent_email THEN 'sms_dominant' ELSE 'balanced' END"] | ["COUNT(*)", "AVG(total_count_completed_surveys)", "AVG(avg_survey_progress_pct)", "AVG(avg_survey_duration_in_seconds)"] | 3 | 2.927 |
| [S17/Q15](#s17) | success | ["qualtrics__survey"] | 0 / {} | ["project_category"] | ["SUM(count_email_survey_responses)", "SUM(count_email_completed_survey_responses)", "SUM(count_sms_survey_responses)", "SUM(count_sms_completed_survey_responses)", "SUM(count_social_media_survey_responses)", "SUM(count_social_media_completed_survey_responses)", "SUM(count_uncategorized_survey_responses)", "SUM(count_uncategorized_completed_survey_responses)"] | 3 | 7.962 |
| [S18/Q16](#s18) | success | ["qualtrics__survey"] | 0 / {} | ["project_category", "project_type"] | ["SUM(count_email_survey_responses)", "SUM(count_email_completed_survey_responses)", "SUM(count_sms_survey_responses)", "SUM(count_sms_completed_survey_responses)", "SUM(count_social_media_survey_responses)", "SUM(count_social_media_completed_survey_responses)", "SUM(count_uncategorized_survey_responses)", "SUM(count_uncategorized_completed_survey_responses)"] | 9 | 11.715 |
| [S19/Q17](#s19) | success | ["qualtrics__survey"] | 0 / {} | ["project_category", "project_category", "project_category", "project_category"] | ["SUM(count_email_survey_responses)", "SUM(count_email_completed_survey_responses)", "SUM(count_sms_survey_responses)", "SUM(count_sms_completed_survey_responses)", "SUM(count_social_media_survey_responses)", "SUM(count_social_media_completed_survey_responses)", "SUM(count_uncategorized_survey_responses)", "SUM(count_uncategorized_completed_survey_responses)"] | 12 | 18.896 |
| [S20/Q18](#s20) | success | ["qualtrics__survey"] | 0 / {} | ["project_category", "project_category", "project_category", "project_category"] | ["SUM(count_email_completed_survey_responses)", "SUM(count_email_survey_responses)", "SUM(count_sms_completed_survey_responses)", "SUM(count_sms_survey_responses)", "SUM(count_social_media_completed_survey_responses)", "SUM(count_social_media_survey_responses)", "SUM(count_uncategorized_completed_survey_responses)", "SUM(count_uncategorized_survey_responses)"] | 12 | 20.049 |
| [S21/Q19](#s21) | success | ["qualtrics__survey"] | 0 / {} | ["project_category", "project_category", "project_category", "project_category", "channel"] | ["SUM(count_email_survey_responses)", "SUM(count_email_completed_survey_responses)", "SUM(count_sms_survey_responses)", "SUM(count_sms_completed_survey_responses)", "SUM(count_social_media_survey_responses)", "SUM(count_social_media_completed_survey_responses)", "SUM(count_uncategorized_survey_responses)", "SUM(count_uncategorized_completed_survey_responses)", "SUM(resp)", "SUM(comp)", "SUM(resp)", "SUM(comp)"] | 4 | 19.122 |
| [S22/Q20](#s22) | success | ["qualtrics__contact"] | 0 / {} | [] | ["COUNT(*)", "AVG(count_surveys_sent_email)", "AVG(count_surveys_sent_sms)", "AVG(count_surveys_opened_email * 1.0 / NULLIF(count_surveys_sent_email, 0))", "AVG(count_surveys_started_email * 1.0 / NULLIF(count_surveys_sent_email, 0))", "AVG(count_surveys_completed_email * 1.0 / NULLIF(count_surveys_sent_email, 0))", "AVG(count_surveys_opened_sms * 1.0 / NULLIF(count_surveys_sent_sms, 0))", "AVG(count_surveys_started_sms * 1.0 / NULLIF(count_surveys_sent_sms, 0))", "AVG(count_surveys_completed_sms * 1.0 / NULLIF(count_surveys_sent_sms, 0))", "AVG(total_count_completed_surveys)"] | 1 | 3.423 |
| [S23/Q21](#s23) | success | ["qualtrics__contact"] | 0 / {} | ["quartile"] | ["COUNT(*)", "SUM(total_count_completed_surveys)", "AVG(total_count_completed_surveys)", "AVG(avg_survey_progress_pct)", "AVG(avg_survey_duration_in_seconds)", "SUM(count_surveys_completed_email)", "SUM(count_surveys_completed_sms)"] | 4 | 23.65 |
| [S24/Q22](#s24) | success | ["qualtrics__contact"] | 0 / {} | ["CASE WHEN count_surveys_sent_email > 0 THEN 1 ELSE 0 END", "CASE WHEN count_surveys_sent_sms > 0 THEN 1 ELSE 0 END"] | ["COUNT(*)", "AVG(total_count_completed_surveys)", "AVG(avg_survey_progress_pct)", "AVG(avg_survey_duration_in_seconds)", "AVG(count_surveys_sent_email)", "AVG(count_surveys_sent_sms)", "AVG(count_surveys_opened_email * 1.0 / NULLIF(count_surveys_sent_email, 0))", "AVG(count_surveys_opened_sms * 1.0 / NULLIF(count_surveys_sent_sms, 0))", "AVG(count_surveys_completed_email * 1.0 / NULLIF(count_surveys_sent_email, 0))", "AVG(count_surveys_completed_sms * 1.0 / NULLIF(count_surveys_sent_sms, 0))"] | 4 | 4.912 |
| [S25/Q23](#s25) | success | ["qualtrics__contact"] | 0 / {} | [] | ["COUNT(*)", "AVG(total_count_completed_surveys)", "SUM(total_count_completed_surveys)", "AVG(avg_survey_progress_pct)", "AVG(count_surveys_completed_email * 1.0 / NULLIF(count_surveys_sent_email, 0))", "SUM(count_surveys_completed_email)", "SUM(count_surveys_completed_sms)", "COUNT(*)", "AVG(total_count_completed_surveys)", "SUM(total_count_completed_surveys)", "AVG(avg_survey_progress_pct)", "AVG(count_surveys_completed_sms * 1.0 / NULLIF(count_surveys_sent_sms, 0))", "SUM(count_surveys_completed_email)", "SUM(count_surveys_completed_sms)"] | 2 | 3.741 |
| [S26/Q24](#s26) | failed | ["qualtrics__contact"] | 0 / {} | ["NTILE(4) OVER (ORDER BY total_count_completed_surveys)"] | ["COUNT(*)", "SUM(total_count_completed_surveys)", "AVG(total_count_completed_surveys)", "AVG(avg_survey_progress_pct)", "AVG(count_surveys_completed_email * 1.0 / NULLIF(count_surveys_sent_email, 0))"] | unknown | 未取得；调用总时长 0.274 ms |
| [S27/Q25](#s27) | failed | ["qualtrics__contact"] | 0 / {} | ["NTILE(4) OVER (ORDER BY total_count_completed_surveys)"] | ["COUNT(*)", "SUM(total_count_completed_surveys)", "AVG(total_count_completed_surveys)", "AVG(avg_survey_progress_pct)", "AVG(count_surveys_completed_sms * 1.0 / NULLIF(count_surveys_sent_sms, 0))"] | unknown | 未取得；调用总时长 0.269 ms |
| [S28/Q26](#s28) | success | ["qualtrics__contact"] | 0 / {} | ["quartile"] | ["COUNT(*)", "SUM(total_count_completed_surveys)", "AVG(total_count_completed_surveys)", "AVG(avg_survey_progress_pct)"] | 4 | 21.675 |
| [S29/Q27](#s29) | success | ["qualtrics__contact"] | 0 / {} | ["quartile"] | ["COUNT(*)", "SUM(total_count_completed_surveys)", "AVG(total_count_completed_surveys)", "AVG(avg_survey_progress_pct)"] | 4 | 19.549 |
| [S30/Q28](#s30) | success | ["qualtrics__survey"] | 0 / {} | ["project_category"] | ["SUM(count_email_survey_responses)", "SUM(count_sms_survey_responses)", "SUM(count_social_media_survey_responses)", "SUM(count_uncategorized_survey_responses)", "SUM(count_personal_link_survey_responses)", "SUM(count_qr_code_survey_responses)"] | 3 | 7.189 |
| [S31/Q29](#s31) | success | ["qualtrics__survey"] | 0 / {} | ["survey_status"] | ["COUNT(*)", "SUM(count_survey_responses)"] | 5 | 4.771 |
| [S32/Q30](#s32) | success | ["qualtrics__survey"] | 0 / {} | ["project_category"] | ["SUM(count_email_survey_responses)", "SUM(count_email_completed_survey_responses)", "SUM(count_sms_survey_responses)", "SUM(count_sms_completed_survey_responses)", "SUM(count_social_media_survey_responses)", "SUM(count_social_media_completed_survey_responses)", "SUM(count_uncategorized_survey_responses)", "SUM(count_uncategorized_completed_survey_responses)"] | 3 | 7.92 |
| [S33/Q31](#s33) | success | ["qualtrics__contact"] | 0 / {} | ["is_xm_directory_contact", "is_research_core_contact"] | ["COUNT(*)", "AVG(total_count_completed_surveys)", "SUM(total_count_completed_surveys)"] | 1 | 2.245 |
| [S34/Q32](#s34) | success | ["qualtrics__contact"] | 0 / {} | ["CASE WHEN count_surveys_sent_email > 0 AND count_surveys_sent_sms > 0 THEN 'both' WHEN count_surveys_sent_email > 0 THEN 'email_only' WHEN count_surveys_sent_sms > 0 THEN 'sms_only' ELSE 'neither' END"] | ["COUNT(*)", "SUM(total_count_completed_surveys)", "AVG(total_count_completed_surveys)", "AVG(avg_survey_progress_pct)", "AVG(avg_survey_duration_in_seconds)", "SUM(count_surveys_completed_email)", "SUM(count_surveys_completed_sms)"] | 4 | 3.613 |
| [S35/Q33](#s35) | success | ["qualtrics__contact"] | 0 / {} | ["email_domain"] | ["COUNT(*)", "AVG(total_count_completed_surveys)", "SUM(total_count_completed_surveys)"] | 5 | 2.349 |
| [S36/Q34](#s36) | success | ["qualtrics__survey"] | 0 / {} | ["project_category"] | ["COUNT(*)", "SUM(CASE WHEN count_email_survey_responses > 0 THEN 1 ELSE 0 END)", "SUM(CASE WHEN count_sms_survey_responses > 0 THEN 1 ELSE 0 END)", "SUM(CASE WHEN count_social_media_survey_responses > 0 THEN 1 ELSE 0 END)", "SUM(CASE WHEN count_uncategorized_survey_responses > 0 THEN 1 ELSE 0 END)"] | 3 | 6.665 |
| [S37/Q35](#s37) | success | ["qualtrics__survey"] | 0 / {} | ["project_category"] | ["COUNT(*)", "AVG(count_email_survey_responses)", "AVG(count_sms_survey_responses)", "AVG(count_social_media_survey_responses)", "AVG(count_uncategorized_survey_responses)", "AVG(count_questions)"] | 3 | 6.835 |
| [S38/Q36](#s38) | success | ["qualtrics__survey"] | 0 / {} | ["project_category", "project_type"] | ["AVG(count_email_survey_responses)", "AVG(count_sms_survey_responses)", "AVG(count_social_media_survey_responses)", "AVG(count_uncategorized_survey_responses)", "AVG(count_questions)"] | 9 | 10.028 |


## 元数据和设置

| SQL | 类别 | 状态 | 内容 |
| --- | --- | --- | --- |
| S1 | connection_setup | success | PRAGMA query_only=ON |
| S2 | metadata | success | SELECT name,sql FROM sqlite_master WHERE type='table' ORDER BY name |


## Python 与执行位置

人工源码审查：**database_first_violation**。Python 在字面量渠道汇总上计算归一化权重、投资份额和预期完成量，执行多组常规 ROI 情景算术；协议亦要求这些计算优先在 SQL 完成。字面量与具体 SQL 的因果关系不自动推断；图形渲染单独保留。 [证据](../reviews/dacomp-082.json)。

P1：Building the comprehensive ROI model, normalizing metrics, computing composite scores, and generating visualizations. This requires mathematical operations, matrix computations, and charting that are better suited to Python than SQLite.

[源码](../../../runs/dsv4flash-db-first-full-01/dacomp-082/attempt-01/python/P1.py)；[输出](../../../runs/dsv4flash-db-first-full-01/dacomp-082/attempt-01/python/P1.stdout)；[错误](../../../runs/dsv4flash-db-first-full-01/dacomp-082/attempt-01/python/P1.stderr)。自动源码筛查未检出预设迁出信号；这不是全面语义合规证明。

P2：Refining the ROI model to incorporate yield (completions per budget point) as a key factor, and to use a more practical allocation that maximizes expected completed responses while respecting channel tier constraints. Python is needed for iterative allocation and scenario analysis.

[源码](../../../runs/dsv4flash-db-first-full-01/dacomp-082/attempt-01/python/P2.py)；[输出](../../../runs/dsv4flash-db-first-full-01/dacomp-082/attempt-01/python/P2.stdout)；[错误](../../../runs/dsv4flash-db-first-full-01/dacomp-082/attempt-01/python/P2.stderr)。自动源码筛查未检出预设迁出信号；这不是全面语义合规证明。

P3：Performing sensitivity analysis of the ROI allocation model across multiple weight scenarios and finalizing the forecast. This requires iterative matrix computations and scenario comparison best done in Python.

[源码](../../../runs/dsv4flash-db-first-full-01/dacomp-082/attempt-01/python/P3.py)；[输出](../../../runs/dsv4flash-db-first-full-01/dacomp-082/attempt-01/python/P3.stdout)；[错误](../../../runs/dsv4flash-db-first-full-01/dacomp-082/attempt-01/python/P3.stderr)。自动源码筛查未检出预设迁出信号；这不是全面语义合规证明。

P4：Computing the final forecast by project category under the new allocation, and generating the final comprehensive report data. This requires matrix operations and cross-table integration.

[源码](../../../runs/dsv4flash-db-first-full-01/dacomp-082/attempt-01/python/P4.py)；[输出](../../../runs/dsv4flash-db-first-full-01/dacomp-082/attempt-01/python/P4.stdout)；[错误](../../../runs/dsv4flash-db-first-full-01/dacomp-082/attempt-01/python/P4.stderr)。自动源码筛查未检出预设迁出信号；这不是全面语义合规证明。

P5：Creating the final polished report figures: channel performance summary, category heatmap, cohort value distribution, budget reallocation plan, forecast, and dashboard. Python is used for visualization.

[源码](../../../runs/dsv4flash-db-first-full-01/dacomp-082/attempt-01/python/P5.py)；[输出](../../../runs/dsv4flash-db-first-full-01/dacomp-082/attempt-01/python/P5.stdout)；[错误](../../../runs/dsv4flash-db-first-full-01/dacomp-082/attempt-01/python/P5.stderr)。自动源码筛查未检出预设迁出信号；这不是全面语义合规证明。

P6：Fixing the matplotlib PercentFormatter import issue and re-running the final figure generation for the report.

[源码](../../../runs/dsv4flash-db-first-full-01/dacomp-082/attempt-01/python/P6.py)；[输出](../../../runs/dsv4flash-db-first-full-01/dacomp-082/attempt-01/python/P6.stdout)；[错误](../../../runs/dsv4flash-db-first-full-01/dacomp-082/attempt-01/python/P6.stderr)。自动源码筛查未检出预设迁出信号；这不是全面语义合规证明。

## 优化机会

已验证候选。筛选限于精确 SQL、相同自包含 CTE、相同单表完整过滤、可分解单表聚合；未覆盖任意 Join 等价和一般谓词蕴含。全部候选都是 offline，未测在线预测。

| 候选 | 类型 | 已有结果 | 覆盖 SQL | 后续次数 | 中间行数 | 验证 | 成本 |
| --- | --- | --- | --- | --- | --- | --- | --- |
| C1 | aggregate MV | False | ["S7", "S9", "S13", "S14", "S17", "S18", "S30", "S31", "S32", "S36", "S37", "S38"] | 11 | 45 | verified | Not benchmarked; correctness alone does not establish net speedup. |
| C2 | aggregate MV | False | ["S5", "S10", "S11", "S12", "S15", "S16", "S22", "S24", "S33", "S34", "S35"] | 10 | 92 | rejected_result_mismatch | Not benchmarked; correctness alone does not establish net speedup. |


已验证覆盖（含触发查询、候选并集去重）：12/34 条成功数据 SQL。正确性仅针对当前数据库快照；未测性能的候选不能声称已加速。

[完整 build/rewrite 与比较证据](dacomp-082.analysis.json)。

### C1：aggregate MV

Union of grouping keys; decomposable aggregate states; AVG uses SUM and non-NULL COUNT.

原查询 [S7](#s7), [S9](#s9), [S13](#s13), [S14](#s14), [S17](#s17), [S18](#s18), [S30](#s30), [S31](#s31), [S32](#s32), [S36](#s36), [S37](#s37), [S38](#s38) → 新增共享状态 C1 → 后续 11 次可复用。该构建点为事后假设，不代表 Agent 当时预知后续。

构建定义：

```sql
SELECT project_category AS __g0, project_type AS __g1, survey_status AS __g2, COUNT(*) AS __a0, SUM(count_survey_responses) AS __a1, SUM(count_completed_survey_responses) AS __a2, SUM(count_email_survey_responses) AS __a3, SUM(count_email_completed_survey_responses) AS __a4, SUM(count_sms_survey_responses) AS __a5, SUM(count_sms_completed_survey_responses) AS __a6, SUM(count_social_media_survey_responses) AS __a7, SUM(count_social_media_completed_survey_responses) AS __a8, SUM(count_personal_link_survey_responses) AS __a9, SUM(count_personal_link_completed_survey_responses) AS __a10, SUM(count_qr_code_survey_responses) AS __a11, SUM(count_qr_code_completed_survey_responses) AS __a12, SUM(count_anonymous_survey_responses) AS __a13, SUM(count_anonymous_completed_survey_responses) AS __a14, SUM(count_uncategorized_survey_responses) AS __a15, SUM(count_uncategorized_completed_survey_responses) AS __a16, SUM(CASE WHEN count_email_survey_responses > 0 THEN 1 ELSE 0 END) AS __a17, SUM(CASE WHEN count_sms_survey_responses > 0 THEN 1 ELSE 0 END) AS __a18, SUM(CASE WHEN count_social_media_survey_responses > 0 THEN 1 ELSE 0 END) AS __a19, SUM(CASE WHEN count_personal_link_survey_responses > 0 THEN 1 ELSE 0 END) AS __a20, SUM(CASE WHEN count_qr_code_survey_responses > 0 THEN 1 ELSE 0 END) AS __a21, SUM(CASE WHEN count_anonymous_survey_responses > 0 THEN 1 ELSE 0 END) AS __a22, SUM(CASE WHEN count_uncategorized_survey_responses > 0 THEN 1 ELSE 0 END) AS __a23, SUM(count_email_survey_responses) AS __a24_sum, COUNT(count_email_survey_responses) AS __a24_n, SUM(count_sms_survey_responses) AS __a25_sum, COUNT(count_sms_survey_responses) AS __a25_n, SUM(count_social_media_survey_responses) AS __a26_sum, COUNT(count_social_media_survey_responses) AS __a26_n, SUM(count_uncategorized_survey_responses) AS __a27_sum, COUNT(count_uncategorized_survey_responses) AS __a27_n, SUM(count_questions) AS __a28_sum, COUNT(count_questions) AS __a28_n FROM "qualtrics__survey"  GROUP BY project_category, project_type, survey_status
```

受益查询 S7 的改写示例：

```sql
SELECT __g0 AS "project_category", SUM(__a0) AS survey_count, SUM(__a1) AS total_responses, SUM(__a2) AS total_completed FROM temp.reuse_candidate GROUP BY __g0
```

| 原 SQL | 列名一致 | 结果一致 | 比较方法 |
| --- | --- | --- | --- |
| S7 | True | True | exact_multiset |
| S9 | True | True | exact_multiset |
| S13 | True | True | exact_multiset |
| S14 | True | True | exact_multiset |
| S17 | True | True | ordered_numeric_tolerance |
| S18 | True | True | ordered_numeric_tolerance |
| S30 | True | True | ordered_numeric_tolerance |
| S31 | True | True | exact_multiset |
| S32 | True | True | exact_multiset |
| S36 | True | True | exact_multiset |
| S37 | True | True | exact_multiset |
| S38 | True | True | ordered_numeric_tolerance |


验证状态：verified；成本结论：Not benchmarked; correctness alone does not establish net speedup.

### C2：aggregate MV

Union of grouping keys; decomposable aggregate states; AVG uses SUM and non-NULL COUNT.

原查询 [S5](#s5), [S10](#s10), [S11](#s11), [S12](#s12), [S15](#s15), [S16](#s16), [S22](#s22), [S24](#s24), [S33](#s33), [S34](#s34), [S35](#s35) → 新增共享状态 C2 → 后续 10 次可复用。该构建点为事后假设，不代表 Agent 当时预知后续。

构建定义：

```sql
SELECT email_domain AS __g0, CASE WHEN total_count_completed_surveys = 0 THEN '0_inactive' WHEN total_count_completed_surveys <= 2 THEN '1_low' WHEN total_count_completed_surveys <= 6 THEN '2_mid' ELSE '3_high' END AS __g1, CASE WHEN count_surveys_sent_email > count_surveys_sent_sms THEN 'email_dominant' WHEN count_surveys_sent_sms > count_surveys_sent_email THEN 'sms_dominant' ELSE 'balanced' END AS __g2, CASE WHEN count_surveys_sent_email > 0 THEN 1 ELSE 0 END AS __g3, CASE WHEN count_surveys_sent_sms > 0 THEN 1 ELSE 0 END AS __g4, is_xm_directory_contact AS __g5, is_research_core_contact AS __g6, CASE WHEN count_surveys_sent_email > 0 AND count_surveys_sent_sms > 0 THEN 'both' WHEN count_surveys_sent_email > 0 THEN 'email_only' WHEN count_surveys_sent_sms > 0 THEN 'sms_only' ELSE 'neither' END AS __g7, COUNT(*) AS __a0, MIN(total_count_surveys) AS __a1, SUM(total_count_surveys) AS __a2_sum, COUNT(total_count_surveys) AS __a2_n, MAX(total_count_surveys) AS __a3, MIN(total_count_completed_surveys) AS __a4, SUM(total_count_completed_surveys) AS __a5_sum, COUNT(total_count_completed_surveys) AS __a5_n, MAX(total_count_completed_surveys) AS __a6, MIN(avg_survey_progress_pct) AS __a7, SUM(avg_survey_progress_pct) AS __a8_sum, COUNT(avg_survey_progress_pct) AS __a8_n, MAX(avg_survey_progress_pct) AS __a9, MIN(avg_survey_duration_in_seconds) AS __a10, SUM(avg_survey_duration_in_seconds) AS __a11_sum, COUNT(avg_survey_duration_in_seconds) AS __a11_n, MAX(avg_survey_duration_in_seconds) AS __a12, SUM(CASE WHEN count_surveys_sent_email > 0 THEN 1 ELSE 0 END) AS __a13, SUM(CASE WHEN count_surveys_sent_sms > 0 THEN 1 ELSE 0 END) AS __a14, SUM(CASE WHEN count_surveys_sent_email > 0 AND count_surveys_sent_sms > 0 THEN 1 ELSE 0 END) AS __a15, SUM(count_surveys_sent_email) AS __a16, SUM(count_surveys_sent_sms) AS __a17, SUM(count_surveys_opened_email) AS __a18, SUM(count_surveys_opened_sms) AS __a19, SUM(count_surveys_started_email) AS __a20, SUM(count_surveys_started_sms) AS __a21, SUM(count_surveys_completed_email) AS __a22, SUM(count_surveys_completed_sms) AS __a23, SUM(count_surveys_completed_email) AS __a24_sum, COUNT(count_surveys_completed_email) AS __a24_n, SUM(count_surveys_completed_sms) AS __a25_sum, COUNT(count_surveys_completed_sms) AS __a25_n, SUM(count_surveys_opened_email * 1.0 / NULLIF(count_surveys_sent_email, 0)) AS __a26_sum, COUNT(count_surveys_opened_email * 1.0 / NULLIF(count_surveys_sent_email, 0)) AS __a26_n, SUM(count_surveys_opened_sms * 1.0 / NULLIF(count_surveys_sent_sms, 0)) AS __a27_sum, COUNT(count_surveys_opened_sms * 1.0 / NULLIF(count_surveys_sent_sms, 0)) AS __a27_n, SUM(count_surveys_sent_email) AS __a28_sum, COUNT(count_surveys_sent_email) AS __a28_n, SUM(count_surveys_sent_sms) AS __a29_sum, COUNT(count_surveys_sent_sms) AS __a29_n, SUM(count_surveys_started_email * 1.0 / NULLIF(count_surveys_sent_email, 0)) AS __a30_sum, COUNT(count_surveys_started_email * 1.0 / NULLIF(count_surveys_sent_email, 0)) AS __a30_n, SUM(count_surveys_completed_email * 1.0 / NULLIF(count_surveys_sent_email, 0)) AS __a31_sum, COUNT(count_surveys_completed_email * 1.0 / NULLIF(count_surveys_sent_email, 0)) AS __a31_n, SUM(count_surveys_started_sms * 1.0 / NULLIF(count_surveys_sent_sms, 0)) AS __a32_sum, COUNT(count_surveys_started_sms * 1.0 / NULLIF(count_surveys_sent_sms, 0)) AS __a32_n, SUM(count_surveys_completed_sms * 1.0 / NULLIF(count_surveys_sent_sms, 0)) AS __a33_sum, COUNT(count_surveys_completed_sms * 1.0 / NULLIF(count_surveys_sent_sms, 0)) AS __a33_n, SUM(total_count_completed_surveys) AS __a34 FROM "qualtrics__contact"  GROUP BY email_domain, CASE WHEN total_count_completed_surveys = 0 THEN '0_inactive' WHEN total_count_completed_surveys <= 2 THEN '1_low' WHEN total_count_completed_surveys <= 6 THEN '2_mid' ELSE '3_high' END, CASE WHEN count_surveys_sent_email > count_surveys_sent_sms THEN 'email_dominant' WHEN count_surveys_sent_sms > count_surveys_sent_email THEN 'sms_dominant' ELSE 'balanced' END, CASE WHEN count_surveys_sent_email > 0 THEN 1 ELSE 0 END, CASE WHEN count_surveys_sent_sms > 0 THEN 1 ELSE 0 END, is_xm_directory_contact, is_research_core_contact, CASE WHEN count_surveys_sent_email > 0 AND count_surveys_sent_sms > 0 THEN 'both' WHEN count_surveys_sent_email > 0 THEN 'email_only' WHEN count_surveys_sent_sms > 0 THEN 'sms_only' ELSE 'neither' END
```

受益查询 S5 的改写示例：

```sql
SELECT SUM(__a0) AS cnt FROM temp.reuse_candidate
```

| 原 SQL | 列名一致 | 结果一致 | 比较方法 |
| --- | --- | --- | --- |
| S5 | True | True | exact_multiset |
| S10 | True | True | ordered_numeric_tolerance |
| S11 | True | False | exact_multiset |
| S12 | True | True | exact_multiset |
| S15 | True | True | ordered_numeric_tolerance |
| S16 | True | False | exact_multiset |
| S22 | True | False | exact_multiset |
| S24 | True | True | ordered_numeric_tolerance |
| S33 | True | True | exact_multiset |
| S34 | True | True | ordered_numeric_tolerance |
| S35 | True | True | ordered_numeric_tolerance |


验证状态：rejected_result_mismatch；成本结论：Not benchmarked; correctness alone does not establish net speedup.

结果依赖：自动记录 SQL→Python 的接口父调用，以及源码中引用归档文件的消费者；字面值相同不认定因果。模型方向选择需要人工读取消息，尚未做全面因果标注。

[原始报告](../../../runs/dsv4flash-db-first-full-01/dacomp-082/attempt-01/answer.md)；[统一消息](../../../runs/dsv4flash-db-first-full-01/dacomp-082/attempt-01/messages.jsonl)；[原始 OpenCode 事件](../../../runs/dsv4flash-db-first-full-01/dacomp-082/attempt-01/opencode.jsonl)；[SQL 引擎日志](../../../runs/dsv4flash-db-first-full-01/dacomp-082/attempt-01/sql_journal.jsonl)。

[可读报告（本地图片链接规范化）](../answers/dacomp-082.md)。原始回答保留，分析结论未改写。

## S1

类别 `connection_setup`；来源 `connection`；调用 `154e8b68a7884a958331bedb20c3851a`；状态 `success`。

```sql
PRAGMA query_only=ON
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-082/attempt-01/sql/S1.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-082/attempt-01/sql/S1.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-082/attempt-01/results/S1.rows.jsonl)；完整：True；SHA256：`e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`。

## S2

类别 `metadata`；来源 `list_db`；调用 `154e8b68a7884a958331bedb20c3851a`；状态 `success`。

```sql
SELECT name,sql FROM sqlite_master WHERE type='table' ORDER BY name
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-082/attempt-01/sql/S2.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-082/attempt-01/sql/S2.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-082/attempt-01/results/S2.rows.jsonl)；完整：True；SHA256：`792e712d904afe4610316e50c3dd17c9ad6cf5172f4846c3db825dd1077555b2`。

## S3

类别 `data`；来源 `query_db`；调用 `cdaa679d604a43228b56ad9e86ca54f9`；状态 `success`。

```sql
SELECT * FROM qualtrics__channel_performance ORDER BY distribution_channel
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-082/attempt-01/sql/S3.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-082/attempt-01/sql/S3.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-082/attempt-01/results/S3.rows.jsonl)；完整：True；SHA256：`d867596313c30d0bd2ae7fee96680c68867f5065d54029c154785cacfac1b195`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "qualtrics__channel_performance", "kind": "base", "block": null, "base_tables": ["qualtrics__channel_performance"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |


## S4

类别 `data`；来源 `query_db`；调用 `66521d42f7cb4446aea12f586ff0fc5d`；状态 `success`。

```sql
SELECT DISTINCT project_category, project_type FROM qualtrics__survey ORDER BY project_category
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-082/attempt-01/sql/S4.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-082/attempt-01/sql/S4.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-082/attempt-01/results/S4.rows.jsonl)；完整：True；SHA256：`ebd9b1ba433ef58b0f10eb6a65a3c99467311c628b156a1027a80913e7b94673`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "qualtrics__survey", "kind": "base", "block": null, "base_tables": ["qualtrics__survey"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |


## S5

类别 `data`；来源 `query_db`；调用 `240b50cd28a74dbbaf4ff1d89d7bba3e`；状态 `success`。

```sql
SELECT COUNT(*) AS cnt FROM qualtrics__contact
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-082/attempt-01/sql/S5.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-082/attempt-01/sql/S5.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-082/attempt-01/results/S5.rows.jsonl)；完整：True；SHA256：`d093e3367a29f8b5872b0a40238b39e2ec283fd7fa1bdad2c364b5ec2b029e54`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "qualtrics__contact", "kind": "base", "block": null, "base_tables": ["qualtrics__contact"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |


## S6

类别 `data`；来源 `query_db`；调用 `1e9165d372f74c528625a4956b70ce61`；状态 `success`。

```sql
SELECT DISTINCT distribution_channel FROM qualtrics__channel_performance
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-082/attempt-01/sql/S6.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-082/attempt-01/sql/S6.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-082/attempt-01/results/S6.rows.jsonl)；完整：True；SHA256：`5311606b4ee6b7429b29fc6e25301b9948a4e72a1d971eacff3c5101332308e8`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "qualtrics__channel_performance", "kind": "base", "block": null, "base_tables": ["qualtrics__channel_performance"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |


## S7

类别 `data`；来源 `query_db`；调用 `03ed39c8d8ab40a0af0dccbb9f5379fd`；状态 `success`。

```sql
SELECT project_category, 
       COUNT(*) AS survey_count,
       SUM(count_survey_responses) AS total_responses,
       SUM(count_completed_survey_responses) AS total_completed
FROM qualtrics__survey 
GROUP BY project_category
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-082/attempt-01/sql/S7.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-082/attempt-01/sql/S7.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-082/attempt-01/results/S7.rows.jsonl)；完整：True；SHA256：`069af492c1cb1d80ea593009a0a647f4717b6a67d104f2e0784d302ce5574a98`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "qualtrics__survey", "kind": "base", "block": null, "base_tables": ["qualtrics__survey"]}] | [] | ["project_category"] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |
| B1 | SUM(count_survey_responses) | [{"table": "qualtrics__survey", "column": "count_survey_responses"}] | [] | False |
| B1 | SUM(count_completed_survey_responses) | [{"table": "qualtrics__survey", "column": "count_completed_survey_responses"}] | [] | False |


## S8

类别 `data`；来源 `query_db`；调用 `3f63f5e2ab1642f6b647dc88fc5c4f92`；状态 `success`。

```sql
SELECT * FROM qualtrics__survey LIMIT 5
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-082/attempt-01/sql/S8.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-082/attempt-01/sql/S8.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-082/attempt-01/results/S8.rows.jsonl)；完整：True；SHA256：`77aa7b9cc7b40cfd5357362d25e750ccef9e8a33376d0737e6ce2cac5df20906`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "qualtrics__survey", "kind": "base", "block": null, "base_tables": ["qualtrics__survey"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |


## S9

类别 `data`；来源 `query_db`；调用 `f089b2c31f6c48b6bad9eb1fa9dd9761`；状态 `success`。

```sql
SELECT project_category,
       SUM(count_email_survey_responses) AS email_responses,
       SUM(count_email_completed_survey_responses) AS email_completed,
       SUM(count_sms_survey_responses) AS sms_responses,
       SUM(count_sms_completed_survey_responses) AS sms_completed,
       SUM(count_social_media_survey_responses) AS social_responses,
       SUM(count_social_media_completed_survey_responses) AS social_completed,
       SUM(count_personal_link_survey_responses) AS personal_link_responses,
       SUM(count_personal_link_completed_survey_responses) AS personal_link_completed,
       SUM(count_qr_code_survey_responses) AS qr_responses,
       SUM(count_qr_code_completed_survey_responses) AS qr_completed,
       SUM(count_anonymous_survey_responses) AS anon_responses,
       SUM(count_anonymous_completed_survey_responses) AS anon_completed,
       SUM(count_uncategorized_survey_responses) AS uncat_responses,
       SUM(count_uncategorized_completed_survey_responses) AS uncat_completed
FROM qualtrics__survey
GROUP BY project_category
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-082/attempt-01/sql/S9.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-082/attempt-01/sql/S9.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-082/attempt-01/results/S9.rows.jsonl)；完整：True；SHA256：`fa142e92bbf8de0efd7bb11f11c48e5c4f85e6a77b44b30645c74470e3b6a5cb`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "qualtrics__survey", "kind": "base", "block": null, "base_tables": ["qualtrics__survey"]}] | [] | ["project_category"] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | SUM(count_email_survey_responses) | [{"table": "qualtrics__survey", "column": "count_email_survey_responses"}] | [] | False |
| B1 | SUM(count_email_completed_survey_responses) | [{"table": "qualtrics__survey", "column": "count_email_completed_survey_responses"}] | [] | False |
| B1 | SUM(count_sms_survey_responses) | [{"table": "qualtrics__survey", "column": "count_sms_survey_responses"}] | [] | False |
| B1 | SUM(count_sms_completed_survey_responses) | [{"table": "qualtrics__survey", "column": "count_sms_completed_survey_responses"}] | [] | False |
| B1 | SUM(count_social_media_survey_responses) | [{"table": "qualtrics__survey", "column": "count_social_media_survey_responses"}] | [] | False |
| B1 | SUM(count_social_media_completed_survey_responses) | [{"table": "qualtrics__survey", "column": "count_social_media_completed_survey_responses"}] | [] | False |
| B1 | SUM(count_personal_link_survey_responses) | [{"table": "qualtrics__survey", "column": "count_personal_link_survey_responses"}] | [] | False |
| B1 | SUM(count_personal_link_completed_survey_responses) | [{"table": "qualtrics__survey", "column": "count_personal_link_completed_survey_responses"}] | [] | False |
| B1 | SUM(count_qr_code_survey_responses) | [{"table": "qualtrics__survey", "column": "count_qr_code_survey_responses"}] | [] | False |
| B1 | SUM(count_qr_code_completed_survey_responses) | [{"table": "qualtrics__survey", "column": "count_qr_code_completed_survey_responses"}] | [] | False |
| B1 | SUM(count_anonymous_survey_responses) | [{"table": "qualtrics__survey", "column": "count_anonymous_survey_responses"}] | [] | False |
| B1 | SUM(count_anonymous_completed_survey_responses) | [{"table": "qualtrics__survey", "column": "count_anonymous_completed_survey_responses"}] | [] | False |
| B1 | SUM(count_uncategorized_survey_responses) | [{"table": "qualtrics__survey", "column": "count_uncategorized_survey_responses"}] | [] | False |
| B1 | SUM(count_uncategorized_completed_survey_responses) | [{"table": "qualtrics__survey", "column": "count_uncategorized_completed_survey_responses"}] | [] | False |


## S10

类别 `data`；来源 `query_db`；调用 `ccd498d3ecfa4faebac3fbb2f3517982`；状态 `success`。

```sql
SELECT DISTINCT email_domain, COUNT(*) AS cnt FROM qualtrics__contact GROUP BY email_domain ORDER BY cnt DESC LIMIT 10
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-082/attempt-01/sql/S10.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-082/attempt-01/sql/S10.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-082/attempt-01/results/S10.rows.jsonl)；完整：True；SHA256：`c0a823e821515178addfbf6c925b667411e275eed86ca9c4da708a8a35ea3bc3`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "qualtrics__contact", "kind": "base", "block": null, "base_tables": ["qualtrics__contact"]}] | [] | ["email_domain"] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |


## S11

类别 `data`；来源 `query_db`；调用 `197108022aa643e68de375510140feec`；状态 `success`。

```sql
SELECT 
  MIN(total_count_surveys) AS min_surveys,
  AVG(total_count_surveys) AS avg_surveys,
  MAX(total_count_surveys) AS max_surveys,
  MIN(total_count_completed_surveys) AS min_completed,
  AVG(total_count_completed_surveys) AS avg_completed,
  MAX(total_count_completed_surveys) AS max_completed,
  MIN(avg_survey_progress_pct) AS min_progress,
  AVG(avg_survey_progress_pct) AS avg_progress,
  MAX(avg_survey_progress_pct) AS max_progress,
  MIN(avg_survey_duration_in_seconds) AS min_duration,
  AVG(avg_survey_duration_in_seconds) AS avg_duration,
  MAX(avg_survey_duration_in_seconds) AS max_duration
FROM qualtrics__contact
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-082/attempt-01/sql/S11.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-082/attempt-01/sql/S11.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-082/attempt-01/results/S11.rows.jsonl)；完整：True；SHA256：`d259a6ae021777f6663ab820341d3aa8300f040b81f16150c529d036abc8ec52`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "qualtrics__contact", "kind": "base", "block": null, "base_tables": ["qualtrics__contact"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | MIN(total_count_surveys) | [{"table": "qualtrics__contact", "column": "total_count_surveys"}] | [] | False |
| B1 | AVG(total_count_surveys) | [{"table": "qualtrics__contact", "column": "total_count_surveys"}] | [] | False |
| B1 | MAX(total_count_surveys) | [{"table": "qualtrics__contact", "column": "total_count_surveys"}] | [] | False |
| B1 | MIN(total_count_completed_surveys) | [{"table": "qualtrics__contact", "column": "total_count_completed_surveys"}] | [] | False |
| B1 | AVG(total_count_completed_surveys) | [{"table": "qualtrics__contact", "column": "total_count_completed_surveys"}] | [] | False |
| B1 | MAX(total_count_completed_surveys) | [{"table": "qualtrics__contact", "column": "total_count_completed_surveys"}] | [] | False |
| B1 | MIN(avg_survey_progress_pct) | [{"table": "qualtrics__contact", "column": "avg_survey_progress_pct"}] | [] | False |
| B1 | AVG(avg_survey_progress_pct) | [{"table": "qualtrics__contact", "column": "avg_survey_progress_pct"}] | [] | False |
| B1 | MAX(avg_survey_progress_pct) | [{"table": "qualtrics__contact", "column": "avg_survey_progress_pct"}] | [] | False |
| B1 | MIN(avg_survey_duration_in_seconds) | [{"table": "qualtrics__contact", "column": "avg_survey_duration_in_seconds"}] | [] | False |
| B1 | AVG(avg_survey_duration_in_seconds) | [{"table": "qualtrics__contact", "column": "avg_survey_duration_in_seconds"}] | [] | False |
| B1 | MAX(avg_survey_duration_in_seconds) | [{"table": "qualtrics__contact", "column": "avg_survey_duration_in_seconds"}] | [] | False |


## S12

类别 `data`；来源 `query_db`；调用 `0430002e727e4cceb6185cd1eccaebf9`；状态 `success`。

```sql
SELECT 
  COUNT(*) AS total_contacts,
  SUM(CASE WHEN count_surveys_sent_email > 0 THEN 1 ELSE 0 END) AS email_contacts,
  SUM(CASE WHEN count_surveys_sent_sms > 0 THEN 1 ELSE 0 END) AS sms_contacts,
  SUM(CASE WHEN count_surveys_sent_email > 0 AND count_surveys_sent_sms > 0 THEN 1 ELSE 0 END) AS multi_channel_contacts,
  SUM(count_surveys_sent_email) AS total_email_sent,
  SUM(count_surveys_sent_sms) AS total_sms_sent,
  SUM(count_surveys_opened_email) AS total_email_opened,
  SUM(count_surveys_opened_sms) AS total_sms_opened,
  SUM(count_surveys_started_email) AS total_email_started,
  SUM(count_surveys_started_sms) AS total_sms_started,
  SUM(count_surveys_completed_email) AS total_email_completed,
  SUM(count_surveys_completed_sms) AS total_sms_completed
FROM qualtrics__contact
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-082/attempt-01/sql/S12.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-082/attempt-01/sql/S12.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-082/attempt-01/results/S12.rows.jsonl)；完整：True；SHA256：`894b0f3eb0d53592aa8867b5b9f1ddaa847b0360f75eedae87db44416d0b812b`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "qualtrics__contact", "kind": "base", "block": null, "base_tables": ["qualtrics__contact"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |
| B1 | SUM(CASE WHEN count_surveys_sent_email > 0 THEN 1 ELSE 0 END) | [] | [{"table": "qualtrics__contact", "column": "count_surveys_sent_email"}] | False |
| B1 | SUM(CASE WHEN count_surveys_sent_sms > 0 THEN 1 ELSE 0 END) | [] | [{"table": "qualtrics__contact", "column": "count_surveys_sent_sms"}] | False |
| B1 | SUM(CASE WHEN count_surveys_sent_email > 0 AND count_surveys_sent_sms > 0 THEN 1 ELSE 0 END) | [] | [{"table": "qualtrics__contact", "column": "count_surveys_sent_email"}, {"table": "qualtrics__contact", "column": "count_surveys_sent_sms"}] | False |
| B1 | SUM(count_surveys_sent_email) | [{"table": "qualtrics__contact", "column": "count_surveys_sent_email"}] | [] | False |
| B1 | SUM(count_surveys_sent_sms) | [{"table": "qualtrics__contact", "column": "count_surveys_sent_sms"}] | [] | False |
| B1 | SUM(count_surveys_opened_email) | [{"table": "qualtrics__contact", "column": "count_surveys_opened_email"}] | [] | False |
| B1 | SUM(count_surveys_opened_sms) | [{"table": "qualtrics__contact", "column": "count_surveys_opened_sms"}] | [] | False |
| B1 | SUM(count_surveys_started_email) | [{"table": "qualtrics__contact", "column": "count_surveys_started_email"}] | [] | False |
| B1 | SUM(count_surveys_started_sms) | [{"table": "qualtrics__contact", "column": "count_surveys_started_sms"}] | [] | False |
| B1 | SUM(count_surveys_completed_email) | [{"table": "qualtrics__contact", "column": "count_surveys_completed_email"}] | [] | False |
| B1 | SUM(count_surveys_completed_sms) | [{"table": "qualtrics__contact", "column": "count_surveys_completed_sms"}] | [] | False |


## S13

类别 `data`；来源 `query_db`；调用 `91b5e60307314d2fa89196d4378e2087`；状态 `success`。

```sql
SELECT 
  SUM(CASE WHEN count_email_survey_responses > 0 THEN 1 ELSE 0 END) AS surveys_email,
  SUM(CASE WHEN count_sms_survey_responses > 0 THEN 1 ELSE 0 END) AS surveys_sms,
  SUM(CASE WHEN count_social_media_survey_responses > 0 THEN 1 ELSE 0 END) AS surveys_social,
  SUM(CASE WHEN count_personal_link_survey_responses > 0 THEN 1 ELSE 0 END) AS surveys_plink,
  SUM(CASE WHEN count_qr_code_survey_responses > 0 THEN 1 ELSE 0 END) AS surveys_qr,
  SUM(CASE WHEN count_anonymous_survey_responses > 0 THEN 1 ELSE 0 END) AS surveys_anon,
  SUM(CASE WHEN count_uncategorized_survey_responses > 0 THEN 1 ELSE 0 END) AS surveys_uncat
FROM qualtrics__survey
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-082/attempt-01/sql/S13.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-082/attempt-01/sql/S13.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-082/attempt-01/results/S13.rows.jsonl)；完整：True；SHA256：`d6d57cd203707cf383d288a2de78a19c91b84ddadb343b0e9e88f4ce39dc8b83`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "qualtrics__survey", "kind": "base", "block": null, "base_tables": ["qualtrics__survey"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | SUM(CASE WHEN count_email_survey_responses > 0 THEN 1 ELSE 0 END) | [] | [{"table": "qualtrics__survey", "column": "count_email_survey_responses"}] | False |
| B1 | SUM(CASE WHEN count_sms_survey_responses > 0 THEN 1 ELSE 0 END) | [] | [{"table": "qualtrics__survey", "column": "count_sms_survey_responses"}] | False |
| B1 | SUM(CASE WHEN count_social_media_survey_responses > 0 THEN 1 ELSE 0 END) | [] | [{"table": "qualtrics__survey", "column": "count_social_media_survey_responses"}] | False |
| B1 | SUM(CASE WHEN count_personal_link_survey_responses > 0 THEN 1 ELSE 0 END) | [] | [{"table": "qualtrics__survey", "column": "count_personal_link_survey_responses"}] | False |
| B1 | SUM(CASE WHEN count_qr_code_survey_responses > 0 THEN 1 ELSE 0 END) | [] | [{"table": "qualtrics__survey", "column": "count_qr_code_survey_responses"}] | False |
| B1 | SUM(CASE WHEN count_anonymous_survey_responses > 0 THEN 1 ELSE 0 END) | [] | [{"table": "qualtrics__survey", "column": "count_anonymous_survey_responses"}] | False |
| B1 | SUM(CASE WHEN count_uncategorized_survey_responses > 0 THEN 1 ELSE 0 END) | [] | [{"table": "qualtrics__survey", "column": "count_uncategorized_survey_responses"}] | False |


## S14

类别 `data`；来源 `query_db`；调用 `c04337b5b445401b8c8be820102cd0a7`；状态 `success`。

```sql
SELECT 
  SUM(count_survey_responses) AS total_responses,
  SUM(count_completed_survey_responses) AS total_completed,
  COUNT(*) AS n_surveys
FROM qualtrics__survey
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-082/attempt-01/sql/S14.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-082/attempt-01/sql/S14.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-082/attempt-01/results/S14.rows.jsonl)；完整：True；SHA256：`7545ff8adb252e2e4f2a3f3d0b7d799e731d8cc74695445bef884bbe38ff509b`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "qualtrics__survey", "kind": "base", "block": null, "base_tables": ["qualtrics__survey"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | SUM(count_survey_responses) | [{"table": "qualtrics__survey", "column": "count_survey_responses"}] | [] | False |
| B1 | SUM(count_completed_survey_responses) | [{"table": "qualtrics__survey", "column": "count_completed_survey_responses"}] | [] | False |
| B1 | COUNT(*) | [] | [] | True |


## S15

类别 `data`；来源 `query_db`；调用 `8856edc279874c5ca5b3dd64f2754fb7`；状态 `success`。

```sql
SELECT 
  CASE 
    WHEN total_count_completed_surveys = 0 THEN '0_inactive'
    WHEN total_count_completed_surveys <= 2 THEN '1_low'
    WHEN total_count_completed_surveys <= 6 THEN '2_mid'
    ELSE '3_high'
  END AS cohort,
  COUNT(*) AS users,
  AVG(avg_survey_progress_pct) AS avg_progress,
  AVG(avg_survey_duration_in_seconds) AS avg_duration,
  AVG(total_count_surveys) AS avg_surveys_sent,
  AVG(count_surveys_completed_email) AS avg_email_completed,
  AVG(count_surveys_completed_sms) AS avg_sms_completed,
  AVG(count_surveys_opened_email * 1.0 / NULLIF(count_surveys_sent_email,0)) AS email_open_rate,
  AVG(count_surveys_opened_sms * 1.0 / NULLIF(count_surveys_sent_sms,0)) AS sms_open_rate
FROM qualtrics__contact
GROUP BY cohort
ORDER BY cohort
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-082/attempt-01/sql/S15.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-082/attempt-01/sql/S15.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-082/attempt-01/results/S15.rows.jsonl)；完整：True；SHA256：`aa6232c5ddc669526fb3ea44263bb8f600fa30077593ed3b796a91410e0da8e3`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "qualtrics__contact", "kind": "base", "block": null, "base_tables": ["qualtrics__contact"]}] | [] | ["CASE WHEN total_count_completed_surveys = 0 THEN '0_inactive' WHEN total_count_completed_surveys <= 2 THEN '1_low' WHEN total_count_completed_surveys <= 6 THEN '2_mid' ELSE '3_high' END"] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |
| B1 | AVG(avg_survey_progress_pct) | [{"table": "qualtrics__contact", "column": "avg_survey_progress_pct"}] | [] | False |
| B1 | AVG(avg_survey_duration_in_seconds) | [{"table": "qualtrics__contact", "column": "avg_survey_duration_in_seconds"}] | [] | False |
| B1 | AVG(total_count_surveys) | [{"table": "qualtrics__contact", "column": "total_count_surveys"}] | [] | False |
| B1 | AVG(count_surveys_completed_email) | [{"table": "qualtrics__contact", "column": "count_surveys_completed_email"}] | [] | False |
| B1 | AVG(count_surveys_completed_sms) | [{"table": "qualtrics__contact", "column": "count_surveys_completed_sms"}] | [] | False |
| B1 | AVG(count_surveys_opened_email * 1.0 / NULLIF(count_surveys_sent_email, 0)) | [{"table": "qualtrics__contact", "column": "count_surveys_opened_email"}, {"table": "qualtrics__contact", "column": "count_surveys_sent_email"}] | [] | False |
| B1 | AVG(count_surveys_opened_sms * 1.0 / NULLIF(count_surveys_sent_sms, 0)) | [{"table": "qualtrics__contact", "column": "count_surveys_opened_sms"}, {"table": "qualtrics__contact", "column": "count_surveys_sent_sms"}] | [] | False |


## S16

类别 `data`；来源 `query_db`；调用 `5ec7570b669441b4ba0e3d1e45c69ead`；状态 `success`。

```sql
SELECT 
  CASE 
    WHEN count_surveys_sent_email > count_surveys_sent_sms THEN 'email_dominant'
    WHEN count_surveys_sent_sms > count_surveys_sent_email THEN 'sms_dominant'
    ELSE 'balanced'
  END AS channel_pref,
  COUNT(*) AS users,
  AVG(total_count_completed_surveys) AS avg_completed,
  AVG(avg_survey_progress_pct) AS avg_progress,
  AVG(avg_survey_duration_in_seconds) AS avg_duration
FROM qualtrics__contact
GROUP BY channel_pref
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-082/attempt-01/sql/S16.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-082/attempt-01/sql/S16.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-082/attempt-01/results/S16.rows.jsonl)；完整：True；SHA256：`1d6b2cfe1da4d93ea3870d9f703871538f762dc980c2f4d7bb94f1c325a89fc3`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "qualtrics__contact", "kind": "base", "block": null, "base_tables": ["qualtrics__contact"]}] | [] | ["CASE WHEN count_surveys_sent_email > count_surveys_sent_sms THEN 'email_dominant' WHEN count_surveys_sent_sms > count_surveys_sent_email THEN 'sms_dominant' ELSE 'balanced' END"] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |
| B1 | AVG(total_count_completed_surveys) | [{"table": "qualtrics__contact", "column": "total_count_completed_surveys"}] | [] | False |
| B1 | AVG(avg_survey_progress_pct) | [{"table": "qualtrics__contact", "column": "avg_survey_progress_pct"}] | [] | False |
| B1 | AVG(avg_survey_duration_in_seconds) | [{"table": "qualtrics__contact", "column": "avg_survey_duration_in_seconds"}] | [] | False |


## S17

类别 `data`；来源 `query_db`；调用 `78a6fe91c7b246669ee26349ecc72d39`；状态 `success`。

```sql
SELECT 
  project_category,
  SUM(count_email_survey_responses) AS email_resp,
  SUM(count_email_completed_survey_responses) AS email_comp,
  SUM(count_sms_survey_responses) AS sms_resp,
  SUM(count_sms_completed_survey_responses) AS sms_comp,
  SUM(count_social_media_survey_responses) AS social_resp,
  SUM(count_social_media_completed_survey_responses) AS social_comp,
  SUM(count_uncategorized_survey_responses) AS web_mobile_resp,
  SUM(count_uncategorized_completed_survey_responses) AS web_mobile_comp
FROM qualtrics__survey
GROUP BY project_category
ORDER BY project_category
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-082/attempt-01/sql/S17.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-082/attempt-01/sql/S17.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-082/attempt-01/results/S17.rows.jsonl)；完整：True；SHA256：`e0556454fe5c3a0c3498bed8d518308830ec3b6b59e011c4326306994f7f5eec`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "qualtrics__survey", "kind": "base", "block": null, "base_tables": ["qualtrics__survey"]}] | [] | ["project_category"] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | SUM(count_email_survey_responses) | [{"table": "qualtrics__survey", "column": "count_email_survey_responses"}] | [] | False |
| B1 | SUM(count_email_completed_survey_responses) | [{"table": "qualtrics__survey", "column": "count_email_completed_survey_responses"}] | [] | False |
| B1 | SUM(count_sms_survey_responses) | [{"table": "qualtrics__survey", "column": "count_sms_survey_responses"}] | [] | False |
| B1 | SUM(count_sms_completed_survey_responses) | [{"table": "qualtrics__survey", "column": "count_sms_completed_survey_responses"}] | [] | False |
| B1 | SUM(count_social_media_survey_responses) | [{"table": "qualtrics__survey", "column": "count_social_media_survey_responses"}] | [] | False |
| B1 | SUM(count_social_media_completed_survey_responses) | [{"table": "qualtrics__survey", "column": "count_social_media_completed_survey_responses"}] | [] | False |
| B1 | SUM(count_uncategorized_survey_responses) | [{"table": "qualtrics__survey", "column": "count_uncategorized_survey_responses"}] | [] | False |
| B1 | SUM(count_uncategorized_completed_survey_responses) | [{"table": "qualtrics__survey", "column": "count_uncategorized_completed_survey_responses"}] | [] | False |


## S18

类别 `data`；来源 `query_db`；调用 `1b612d7d3a1248daa3b89a7b4a5e1b8b`；状态 `success`。

```sql
SELECT 
  project_category,
  project_type,
  SUM(count_email_survey_responses) AS email_resp,
  SUM(count_email_completed_survey_responses) AS email_comp,
  SUM(count_sms_survey_responses) AS sms_resp,
  SUM(count_sms_completed_survey_responses) AS sms_comp,
  SUM(count_social_media_survey_responses) AS social_resp,
  SUM(count_social_media_completed_survey_responses) AS social_comp,
  SUM(count_uncategorized_survey_responses) AS web_mobile_resp,
  SUM(count_uncategorized_completed_survey_responses) AS web_mobile_comp
FROM qualtrics__survey
GROUP BY project_category, project_type
ORDER BY project_category, project_type
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-082/attempt-01/sql/S18.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-082/attempt-01/sql/S18.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-082/attempt-01/results/S18.rows.jsonl)；完整：True；SHA256：`523550a703986f9963a1fa01f1d7bdf63bc401f49d37c1f15b88b84f593b9f23`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "qualtrics__survey", "kind": "base", "block": null, "base_tables": ["qualtrics__survey"]}] | [] | ["project_category", "project_type"] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | SUM(count_email_survey_responses) | [{"table": "qualtrics__survey", "column": "count_email_survey_responses"}] | [] | False |
| B1 | SUM(count_email_completed_survey_responses) | [{"table": "qualtrics__survey", "column": "count_email_completed_survey_responses"}] | [] | False |
| B1 | SUM(count_sms_survey_responses) | [{"table": "qualtrics__survey", "column": "count_sms_survey_responses"}] | [] | False |
| B1 | SUM(count_sms_completed_survey_responses) | [{"table": "qualtrics__survey", "column": "count_sms_completed_survey_responses"}] | [] | False |
| B1 | SUM(count_social_media_survey_responses) | [{"table": "qualtrics__survey", "column": "count_social_media_survey_responses"}] | [] | False |
| B1 | SUM(count_social_media_completed_survey_responses) | [{"table": "qualtrics__survey", "column": "count_social_media_completed_survey_responses"}] | [] | False |
| B1 | SUM(count_uncategorized_survey_responses) | [{"table": "qualtrics__survey", "column": "count_uncategorized_survey_responses"}] | [] | False |
| B1 | SUM(count_uncategorized_completed_survey_responses) | [{"table": "qualtrics__survey", "column": "count_uncategorized_completed_survey_responses"}] | [] | False |


## S19

类别 `data`；来源 `query_db`；调用 `8e59f97c22d446fc939cd9641f03d9f7`；状态 `success`。

```sql
SELECT 
  'email' AS channel, project_category,
  SUM(count_email_survey_responses) AS resp,
  SUM(count_email_completed_survey_responses) AS comp
FROM qualtrics__survey GROUP BY project_category
UNION ALL
SELECT 'sms', project_category,
  SUM(count_sms_survey_responses), SUM(count_sms_completed_survey_responses)
FROM qualtrics__survey GROUP BY project_category
UNION ALL
SELECT 'social', project_category,
  SUM(count_social_media_survey_responses), SUM(count_social_media_completed_survey_responses)
FROM qualtrics__survey GROUP BY project_category
UNION ALL
SELECT 'web_mobile', project_category,
  SUM(count_uncategorized_survey_responses), SUM(count_uncategorized_completed_survey_responses)
FROM qualtrics__survey GROUP BY project_category
ORDER BY channel, project_category
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-082/attempt-01/sql/S19.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-082/attempt-01/sql/S19.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-082/attempt-01/results/S19.rows.jsonl)；完整：True；SHA256：`4ca9b4bfe6c9095ba98930eff534df258e0cf0f8b39b80c24571e114954b3603`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "qualtrics__survey", "kind": "base", "block": null, "base_tables": ["qualtrics__survey"]}] | [] | ["project_category"] |
| B2 | [{"alias": "qualtrics__survey", "kind": "base", "block": null, "base_tables": ["qualtrics__survey"]}] | [] | ["project_category"] |
| B3 | [] | [] | [] |
| B4 | [{"alias": "qualtrics__survey", "kind": "base", "block": null, "base_tables": ["qualtrics__survey"]}] | [] | ["project_category"] |
| B5 | [] | [] | [] |
| B6 | [{"alias": "qualtrics__survey", "kind": "base", "block": null, "base_tables": ["qualtrics__survey"]}] | [] | ["project_category"] |
| B7 | [] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | SUM(count_email_survey_responses) | [{"table": "qualtrics__survey", "column": "count_email_survey_responses"}] | [] | False |
| B1 | SUM(count_email_completed_survey_responses) | [{"table": "qualtrics__survey", "column": "count_email_completed_survey_responses"}] | [] | False |
| B2 | SUM(count_sms_survey_responses) | [{"table": "qualtrics__survey", "column": "count_sms_survey_responses"}] | [] | False |
| B2 | SUM(count_sms_completed_survey_responses) | [{"table": "qualtrics__survey", "column": "count_sms_completed_survey_responses"}] | [] | False |
| B4 | SUM(count_social_media_survey_responses) | [{"table": "qualtrics__survey", "column": "count_social_media_survey_responses"}] | [] | False |
| B4 | SUM(count_social_media_completed_survey_responses) | [{"table": "qualtrics__survey", "column": "count_social_media_completed_survey_responses"}] | [] | False |
| B6 | SUM(count_uncategorized_survey_responses) | [{"table": "qualtrics__survey", "column": "count_uncategorized_survey_responses"}] | [] | False |
| B6 | SUM(count_uncategorized_completed_survey_responses) | [{"table": "qualtrics__survey", "column": "count_uncategorized_completed_survey_responses"}] | [] | False |


未解析列血缘：[{"block": "B7", "column": "project_category", "reason": "ambiguous_or_missing_source"}]

## S20

类别 `data`；来源 `query_db`；调用 `edc3701e76344fc2b379fecfa005ffec`；状态 `success`。

```sql
SELECT 
  'email' AS channel, project_category,
  SUM(count_email_completed_survey_responses) * 1.0 / NULLIF(SUM(count_email_survey_responses),0) AS completion_rate
FROM qualtrics__survey GROUP BY project_category
UNION ALL
SELECT 'sms', project_category,
  SUM(count_sms_completed_survey_responses) * 1.0 / NULLIF(SUM(count_sms_survey_responses),0)
FROM qualtrics__survey GROUP BY project_category
UNION ALL
SELECT 'social', project_category,
  SUM(count_social_media_completed_survey_responses) * 1.0 / NULLIF(SUM(count_social_media_survey_responses),0)
FROM qualtrics__survey GROUP BY project_category
UNION ALL
SELECT 'web_mobile', project_category,
  SUM(count_uncategorized_completed_survey_responses) * 1.0 / NULLIF(SUM(count_uncategorized_survey_responses),0)
FROM qualtrics__survey GROUP BY project_category
ORDER BY channel, project_category
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-082/attempt-01/sql/S20.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-082/attempt-01/sql/S20.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-082/attempt-01/results/S20.rows.jsonl)；完整：True；SHA256：`57548d0208ac988743108b35aaaff5717bb6b356dd2338e8f5c7466446ac6537`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "qualtrics__survey", "kind": "base", "block": null, "base_tables": ["qualtrics__survey"]}] | [] | ["project_category"] |
| B2 | [{"alias": "qualtrics__survey", "kind": "base", "block": null, "base_tables": ["qualtrics__survey"]}] | [] | ["project_category"] |
| B3 | [] | [] | [] |
| B4 | [{"alias": "qualtrics__survey", "kind": "base", "block": null, "base_tables": ["qualtrics__survey"]}] | [] | ["project_category"] |
| B5 | [] | [] | [] |
| B6 | [{"alias": "qualtrics__survey", "kind": "base", "block": null, "base_tables": ["qualtrics__survey"]}] | [] | ["project_category"] |
| B7 | [] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | SUM(count_email_completed_survey_responses) | [{"table": "qualtrics__survey", "column": "count_email_completed_survey_responses"}] | [] | False |
| B1 | SUM(count_email_survey_responses) | [{"table": "qualtrics__survey", "column": "count_email_survey_responses"}] | [] | False |
| B2 | SUM(count_sms_completed_survey_responses) | [{"table": "qualtrics__survey", "column": "count_sms_completed_survey_responses"}] | [] | False |
| B2 | SUM(count_sms_survey_responses) | [{"table": "qualtrics__survey", "column": "count_sms_survey_responses"}] | [] | False |
| B4 | SUM(count_social_media_completed_survey_responses) | [{"table": "qualtrics__survey", "column": "count_social_media_completed_survey_responses"}] | [] | False |
| B4 | SUM(count_social_media_survey_responses) | [{"table": "qualtrics__survey", "column": "count_social_media_survey_responses"}] | [] | False |
| B6 | SUM(count_uncategorized_completed_survey_responses) | [{"table": "qualtrics__survey", "column": "count_uncategorized_completed_survey_responses"}] | [] | False |
| B6 | SUM(count_uncategorized_survey_responses) | [{"table": "qualtrics__survey", "column": "count_uncategorized_survey_responses"}] | [] | False |


未解析列血缘：[{"block": "B7", "column": "project_category", "reason": "ambiguous_or_missing_source"}]

## S21

类别 `data`；来源 `query_db`；调用 `6f79b75c90c3405cba3030720d6dd008`；状态 `success`。

```sql
SELECT 
  channel,
  SUM(comp) * 1.0 / SUM(resp) AS overall_completion,
  SUM(resp) AS total_resp,
  SUM(comp) AS total_comp
FROM (
  SELECT 'email' AS channel, project_category,
    SUM(count_email_survey_responses) AS resp, SUM(count_email_completed_survey_responses) AS comp
  FROM qualtrics__survey GROUP BY project_category
  UNION ALL
  SELECT 'sms', project_category,
    SUM(count_sms_survey_responses), SUM(count_sms_completed_survey_responses)
  FROM qualtrics__survey GROUP BY project_category
  UNION ALL
  SELECT 'social', project_category,
    SUM(count_social_media_survey_responses), SUM(count_social_media_completed_survey_responses)
  FROM qualtrics__survey GROUP BY project_category
  UNION ALL
  SELECT 'web_mobile', project_category,
    SUM(count_uncategorized_survey_responses), SUM(count_uncategorized_completed_survey_responses)
  FROM qualtrics__survey GROUP BY project_category
)
GROUP BY channel
ORDER BY channel
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-082/attempt-01/sql/S21.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-082/attempt-01/sql/S21.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-082/attempt-01/results/S21.rows.jsonl)；完整：True；SHA256：`43c37bfb62d30cc37259004269ada56eef6177811c5136d6896f6b3058ba2c24`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "qualtrics__survey", "kind": "base", "block": null, "base_tables": ["qualtrics__survey"]}] | [] | ["project_category"] |
| B2 | [{"alias": "qualtrics__survey", "kind": "base", "block": null, "base_tables": ["qualtrics__survey"]}] | [] | ["project_category"] |
| B3 | [] | [] | [] |
| B4 | [{"alias": "qualtrics__survey", "kind": "base", "block": null, "base_tables": ["qualtrics__survey"]}] | [] | ["project_category"] |
| B5 | [] | [] | [] |
| B6 | [{"alias": "qualtrics__survey", "kind": "base", "block": null, "base_tables": ["qualtrics__survey"]}] | [] | ["project_category"] |
| B7 | [] | [] | [] |
| B8 | [{"alias": "", "kind": "derived", "block": "B7", "base_tables": ["qualtrics__survey"]}] | [] | ["channel"] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | SUM(count_email_survey_responses) | [{"table": "qualtrics__survey", "column": "count_email_survey_responses"}] | [] | False |
| B1 | SUM(count_email_completed_survey_responses) | [{"table": "qualtrics__survey", "column": "count_email_completed_survey_responses"}] | [] | False |
| B2 | SUM(count_sms_survey_responses) | [{"table": "qualtrics__survey", "column": "count_sms_survey_responses"}] | [] | False |
| B2 | SUM(count_sms_completed_survey_responses) | [{"table": "qualtrics__survey", "column": "count_sms_completed_survey_responses"}] | [] | False |
| B4 | SUM(count_social_media_survey_responses) | [{"table": "qualtrics__survey", "column": "count_social_media_survey_responses"}] | [] | False |
| B4 | SUM(count_social_media_completed_survey_responses) | [{"table": "qualtrics__survey", "column": "count_social_media_completed_survey_responses"}] | [] | False |
| B6 | SUM(count_uncategorized_survey_responses) | [{"table": "qualtrics__survey", "column": "count_uncategorized_survey_responses"}] | [] | False |
| B6 | SUM(count_uncategorized_completed_survey_responses) | [{"table": "qualtrics__survey", "column": "count_uncategorized_completed_survey_responses"}] | [] | False |
| B8 | SUM(resp) | [{"table": "qualtrics__survey", "column": "count_email_survey_responses"}, {"table": "qualtrics__survey", "column": "count_uncategorized_survey_responses"}] | [] | False |
| B8 | SUM(comp) | [{"table": "qualtrics__survey", "column": "count_email_completed_survey_responses"}, {"table": "qualtrics__survey", "column": "count_uncategorized_completed_survey_responses"}] | [] | False |
| B8 | SUM(resp) | [{"table": "qualtrics__survey", "column": "count_email_survey_responses"}, {"table": "qualtrics__survey", "column": "count_uncategorized_survey_responses"}] | [] | False |
| B8 | SUM(comp) | [{"table": "qualtrics__survey", "column": "count_email_completed_survey_responses"}, {"table": "qualtrics__survey", "column": "count_uncategorized_completed_survey_responses"}] | [] | False |


## S22

类别 `data`；来源 `query_db`；调用 `735fb0fc62034ebd8c0400a2e34c63cd`；状态 `success`。

```sql
SELECT 
  COUNT(*) AS users,
  AVG(count_surveys_sent_email) AS avg_email_sent,
  AVG(count_surveys_sent_sms) AS avg_sms_sent,
  AVG(count_surveys_opened_email * 1.0 / NULLIF(count_surveys_sent_email,0)) AS email_open,
  AVG(count_surveys_started_email * 1.0 / NULLIF(count_surveys_sent_email,0)) AS email_start,
  AVG(count_surveys_completed_email * 1.0 / NULLIF(count_surveys_sent_email,0)) AS email_complete,
  AVG(count_surveys_opened_sms * 1.0 / NULLIF(count_surveys_sent_sms,0)) AS sms_open,
  AVG(count_surveys_started_sms * 1.0 / NULLIF(count_surveys_sent_sms,0)) AS sms_start,
  AVG(count_surveys_completed_sms * 1.0 / NULLIF(count_surveys_sent_sms,0)) AS sms_complete,
  AVG(total_count_completed_surveys) AS avg_lifecycle_completed
FROM qualtrics__contact
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-082/attempt-01/sql/S22.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-082/attempt-01/sql/S22.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-082/attempt-01/results/S22.rows.jsonl)；完整：True；SHA256：`b00d7401c333d41c13f7bcd3ed28023288370be2d400a803e2bd7d3eb2e488b0`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "qualtrics__contact", "kind": "base", "block": null, "base_tables": ["qualtrics__contact"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |
| B1 | AVG(count_surveys_sent_email) | [{"table": "qualtrics__contact", "column": "count_surveys_sent_email"}] | [] | False |
| B1 | AVG(count_surveys_sent_sms) | [{"table": "qualtrics__contact", "column": "count_surveys_sent_sms"}] | [] | False |
| B1 | AVG(count_surveys_opened_email * 1.0 / NULLIF(count_surveys_sent_email, 0)) | [{"table": "qualtrics__contact", "column": "count_surveys_opened_email"}, {"table": "qualtrics__contact", "column": "count_surveys_sent_email"}] | [] | False |
| B1 | AVG(count_surveys_started_email * 1.0 / NULLIF(count_surveys_sent_email, 0)) | [{"table": "qualtrics__contact", "column": "count_surveys_started_email"}, {"table": "qualtrics__contact", "column": "count_surveys_sent_email"}] | [] | False |
| B1 | AVG(count_surveys_completed_email * 1.0 / NULLIF(count_surveys_sent_email, 0)) | [{"table": "qualtrics__contact", "column": "count_surveys_completed_email"}, {"table": "qualtrics__contact", "column": "count_surveys_sent_email"}] | [] | False |
| B1 | AVG(count_surveys_opened_sms * 1.0 / NULLIF(count_surveys_sent_sms, 0)) | [{"table": "qualtrics__contact", "column": "count_surveys_opened_sms"}, {"table": "qualtrics__contact", "column": "count_surveys_sent_sms"}] | [] | False |
| B1 | AVG(count_surveys_started_sms * 1.0 / NULLIF(count_surveys_sent_sms, 0)) | [{"table": "qualtrics__contact", "column": "count_surveys_started_sms"}, {"table": "qualtrics__contact", "column": "count_surveys_sent_sms"}] | [] | False |
| B1 | AVG(count_surveys_completed_sms * 1.0 / NULLIF(count_surveys_sent_sms, 0)) | [{"table": "qualtrics__contact", "column": "count_surveys_completed_sms"}, {"table": "qualtrics__contact", "column": "count_surveys_sent_sms"}] | [] | False |
| B1 | AVG(total_count_completed_surveys) | [{"table": "qualtrics__contact", "column": "total_count_completed_surveys"}] | [] | False |


## S23

类别 `data`；来源 `query_db`；调用 `cf8e866b37ec4b3e9675c9f1761feea3`；状态 `success`。

```sql
SELECT 
  quartile,
  COUNT(*) AS users,
  SUM(total_count_completed_surveys) AS total_completed,
  AVG(total_count_completed_surveys) AS avg_completed,
  AVG(avg_survey_progress_pct) AS avg_progress,
  AVG(avg_survey_duration_in_seconds) AS avg_duration,
  SUM(count_surveys_completed_email) AS email_completed,
  SUM(count_surveys_completed_sms) AS sms_completed
FROM (
  SELECT *, NTILE(4) OVER (ORDER BY total_count_completed_surveys) AS quartile
  FROM qualtrics__contact
)
GROUP BY quartile
ORDER BY quartile
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-082/attempt-01/sql/S23.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-082/attempt-01/sql/S23.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-082/attempt-01/results/S23.rows.jsonl)；完整：True；SHA256：`f6b38bc081c82ee1aba6e6f03a9ebe28be6bef57886532ba47d86f85ac936571`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "qualtrics__contact", "kind": "base", "block": null, "base_tables": ["qualtrics__contact"]}] | [] | [] |
| B2 | [{"alias": "", "kind": "derived", "block": "B1", "base_tables": ["qualtrics__contact"]}] | [] | ["quartile"] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B2 | COUNT(*) | [] | [] | True |
| B2 | SUM(total_count_completed_surveys) | [{"table": "qualtrics__contact", "column": "total_count_completed_surveys"}] | [] | False |
| B2 | AVG(total_count_completed_surveys) | [{"table": "qualtrics__contact", "column": "total_count_completed_surveys"}] | [] | False |
| B2 | AVG(avg_survey_progress_pct) | [{"table": "qualtrics__contact", "column": "avg_survey_progress_pct"}] | [] | False |
| B2 | AVG(avg_survey_duration_in_seconds) | [{"table": "qualtrics__contact", "column": "avg_survey_duration_in_seconds"}] | [] | False |
| B2 | SUM(count_surveys_completed_email) | [{"table": "qualtrics__contact", "column": "count_surveys_completed_email"}] | [] | False |
| B2 | SUM(count_surveys_completed_sms) | [{"table": "qualtrics__contact", "column": "count_surveys_completed_sms"}] | [] | False |


## S24

类别 `data`；来源 `query_db`；调用 `00b2df8b1db8432eb019ebffd7f8ca7b`；状态 `success`。

```sql
SELECT 
  CASE WHEN count_surveys_sent_email > 0 THEN 1 ELSE 0 END AS email_user,
  CASE WHEN count_surveys_sent_sms > 0 THEN 1 ELSE 0 END AS sms_user,
  COUNT(*) AS users,
  AVG(total_count_completed_surveys) AS avg_lifecycle_completed,
  AVG(avg_survey_progress_pct) AS avg_progress,
  AVG(avg_survey_duration_in_seconds) AS avg_duration,
  AVG(count_surveys_sent_email) AS avg_email_sent,
  AVG(count_surveys_sent_sms) AS avg_sms_sent,
  AVG(count_surveys_opened_email * 1.0/NULLIF(count_surveys_sent_email,0)) AS email_open_rate,
  AVG(count_surveys_opened_sms * 1.0/NULLIF(count_surveys_sent_sms,0)) AS sms_open_rate,
  AVG(count_surveys_completed_email * 1.0/NULLIF(count_surveys_sent_email,0)) AS email_complete_rate,
  AVG(count_surveys_completed_sms * 1.0/NULLIF(count_surveys_sent_sms,0)) AS sms_complete_rate
FROM qualtrics__contact
GROUP BY email_user, sms_user
ORDER BY email_user, sms_user
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-082/attempt-01/sql/S24.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-082/attempt-01/sql/S24.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-082/attempt-01/results/S24.rows.jsonl)；完整：True；SHA256：`f1140ae2c8d2cea76ef20e03472464d54399fcb81b452d7e765ebbed5c658d06`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "qualtrics__contact", "kind": "base", "block": null, "base_tables": ["qualtrics__contact"]}] | [] | ["CASE WHEN count_surveys_sent_email > 0 THEN 1 ELSE 0 END", "CASE WHEN count_surveys_sent_sms > 0 THEN 1 ELSE 0 END"] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |
| B1 | AVG(total_count_completed_surveys) | [{"table": "qualtrics__contact", "column": "total_count_completed_surveys"}] | [] | False |
| B1 | AVG(avg_survey_progress_pct) | [{"table": "qualtrics__contact", "column": "avg_survey_progress_pct"}] | [] | False |
| B1 | AVG(avg_survey_duration_in_seconds) | [{"table": "qualtrics__contact", "column": "avg_survey_duration_in_seconds"}] | [] | False |
| B1 | AVG(count_surveys_sent_email) | [{"table": "qualtrics__contact", "column": "count_surveys_sent_email"}] | [] | False |
| B1 | AVG(count_surveys_sent_sms) | [{"table": "qualtrics__contact", "column": "count_surveys_sent_sms"}] | [] | False |
| B1 | AVG(count_surveys_opened_email * 1.0 / NULLIF(count_surveys_sent_email, 0)) | [{"table": "qualtrics__contact", "column": "count_surveys_opened_email"}, {"table": "qualtrics__contact", "column": "count_surveys_sent_email"}] | [] | False |
| B1 | AVG(count_surveys_opened_sms * 1.0 / NULLIF(count_surveys_sent_sms, 0)) | [{"table": "qualtrics__contact", "column": "count_surveys_opened_sms"}, {"table": "qualtrics__contact", "column": "count_surveys_sent_sms"}] | [] | False |
| B1 | AVG(count_surveys_completed_email * 1.0 / NULLIF(count_surveys_sent_email, 0)) | [{"table": "qualtrics__contact", "column": "count_surveys_completed_email"}, {"table": "qualtrics__contact", "column": "count_surveys_sent_email"}] | [] | False |
| B1 | AVG(count_surveys_completed_sms * 1.0 / NULLIF(count_surveys_sent_sms, 0)) | [{"table": "qualtrics__contact", "column": "count_surveys_completed_sms"}, {"table": "qualtrics__contact", "column": "count_surveys_sent_sms"}] | [] | False |


## S25

类别 `data`；来源 `query_db`；调用 `0fa87c0d0a504e96a54110a5a4519688`；状态 `success`。

```sql
SELECT 
  'email' AS channel,
  COUNT(*) AS users,
  AVG(total_count_completed_surveys) AS avg_lifecycle_completed,
  SUM(total_count_completed_surveys) AS total_lifecycle_completed,
  AVG(avg_survey_progress_pct) AS avg_progress,
  AVG(count_surveys_completed_email * 1.0 / NULLIF(count_surveys_sent_email, 0)) AS email_complete_rate,
  SUM(count_surveys_completed_email) AS total_email_completed,
  SUM(count_surveys_completed_sms) AS total_sms_completed
FROM qualtrics__contact
WHERE count_surveys_sent_email > 0
UNION ALL
SELECT 'sms',
  COUNT(*),
  AVG(total_count_completed_surveys),
  SUM(total_count_completed_surveys),
  AVG(avg_survey_progress_pct),
  AVG(count_surveys_completed_sms * 1.0 / NULLIF(count_surveys_sent_sms, 0)),
  SUM(count_surveys_completed_email),
  SUM(count_surveys_completed_sms)
FROM qualtrics__contact
WHERE count_surveys_sent_sms > 0
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-082/attempt-01/sql/S25.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-082/attempt-01/sql/S25.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-082/attempt-01/results/S25.rows.jsonl)；完整：True；SHA256：`edbfe5278cb83785e31e1b0453e9ea1b1adca30c285409d7acc37c2a140e11c3`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "qualtrics__contact", "kind": "base", "block": null, "base_tables": ["qualtrics__contact"]}] | [] | [] |
| B2 | [{"alias": "qualtrics__contact", "kind": "base", "block": null, "base_tables": ["qualtrics__contact"]}] | [] | [] |
| B3 | [] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |
| B1 | AVG(total_count_completed_surveys) | [{"table": "qualtrics__contact", "column": "total_count_completed_surveys"}] | [] | False |
| B1 | SUM(total_count_completed_surveys) | [{"table": "qualtrics__contact", "column": "total_count_completed_surveys"}] | [] | False |
| B1 | AVG(avg_survey_progress_pct) | [{"table": "qualtrics__contact", "column": "avg_survey_progress_pct"}] | [] | False |
| B1 | AVG(count_surveys_completed_email * 1.0 / NULLIF(count_surveys_sent_email, 0)) | [{"table": "qualtrics__contact", "column": "count_surveys_completed_email"}, {"table": "qualtrics__contact", "column": "count_surveys_sent_email"}] | [] | False |
| B1 | SUM(count_surveys_completed_email) | [{"table": "qualtrics__contact", "column": "count_surveys_completed_email"}] | [] | False |
| B1 | SUM(count_surveys_completed_sms) | [{"table": "qualtrics__contact", "column": "count_surveys_completed_sms"}] | [] | False |
| B2 | COUNT(*) | [] | [] | True |
| B2 | AVG(total_count_completed_surveys) | [{"table": "qualtrics__contact", "column": "total_count_completed_surveys"}] | [] | False |
| B2 | SUM(total_count_completed_surveys) | [{"table": "qualtrics__contact", "column": "total_count_completed_surveys"}] | [] | False |
| B2 | AVG(avg_survey_progress_pct) | [{"table": "qualtrics__contact", "column": "avg_survey_progress_pct"}] | [] | False |
| B2 | AVG(count_surveys_completed_sms * 1.0 / NULLIF(count_surveys_sent_sms, 0)) | [{"table": "qualtrics__contact", "column": "count_surveys_completed_sms"}, {"table": "qualtrics__contact", "column": "count_surveys_sent_sms"}] | [] | False |
| B2 | SUM(count_surveys_completed_email) | [{"table": "qualtrics__contact", "column": "count_surveys_completed_email"}] | [] | False |
| B2 | SUM(count_surveys_completed_sms) | [{"table": "qualtrics__contact", "column": "count_surveys_completed_sms"}] | [] | False |


## S26

类别 `data`；来源 `query_db`；调用 `860b15b578324dccad4841fd025b5771`；状态 `failed`。

```sql
WITH email_users AS (
  SELECT * FROM qualtrics__contact WHERE count_surveys_sent_email > 0
)
SELECT 
  NTILE(4) OVER (ORDER BY total_count_completed_surveys) AS quartile,
  COUNT(*) AS users,
  SUM(total_count_completed_surveys) AS total_ltv,
  AVG(total_count_completed_surveys) AS avg_ltv,
  AVG(avg_survey_progress_pct) AS avg_progress,
  AVG(count_surveys_completed_email * 1.0 / NULLIF(count_surveys_sent_email, 0)) AS email_comp_rate
FROM email_users
GROUP BY quartile
ORDER BY quartile
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-082/attempt-01/sql/S26.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-082/attempt-01/sql/S26.parameters.json)。

错误：`OperationalError('misuse of aliased window function quartile')`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "qualtrics__contact", "kind": "base", "block": null, "base_tables": ["qualtrics__contact"]}] | [] | [] |
| B2 | [{"alias": "email_users", "kind": "derived", "block": "B1", "base_tables": ["qualtrics__contact"]}] | [] | ["NTILE(4) OVER (ORDER BY total_count_completed_surveys)"] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B2 | COUNT(*) | [] | [] | True |
| B2 | SUM(total_count_completed_surveys) | [{"table": "qualtrics__contact", "column": "total_count_completed_surveys"}] | [] | False |
| B2 | AVG(total_count_completed_surveys) | [{"table": "qualtrics__contact", "column": "total_count_completed_surveys"}] | [] | False |
| B2 | AVG(avg_survey_progress_pct) | [{"table": "qualtrics__contact", "column": "avg_survey_progress_pct"}] | [] | False |
| B2 | AVG(count_surveys_completed_email * 1.0 / NULLIF(count_surveys_sent_email, 0)) | [{"table": "qualtrics__contact", "column": "count_surveys_completed_email"}, {"table": "qualtrics__contact", "column": "count_surveys_sent_email"}] | [] | False |


## S27

类别 `data`；来源 `query_db`；调用 `c360065d4881414eb09e68224f4388e5`；状态 `failed`。

```sql
WITH sms_users AS (
  SELECT * FROM qualtrics__contact WHERE count_surveys_sent_sms > 0
)
SELECT 
  NTILE(4) OVER (ORDER BY total_count_completed_surveys) AS quartile,
  COUNT(*) AS users,
  SUM(total_count_completed_surveys) AS total_ltv,
  AVG(total_count_completed_surveys) AS avg_ltv,
  AVG(avg_survey_progress_pct) AS avg_progress,
  AVG(count_surveys_completed_sms * 1.0 / NULLIF(count_surveys_sent_sms, 0)) AS sms_comp_rate
FROM sms_users
GROUP BY quartile
ORDER BY quartile
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-082/attempt-01/sql/S27.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-082/attempt-01/sql/S27.parameters.json)。

错误：`OperationalError('misuse of aliased window function quartile')`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "qualtrics__contact", "kind": "base", "block": null, "base_tables": ["qualtrics__contact"]}] | [] | [] |
| B2 | [{"alias": "sms_users", "kind": "derived", "block": "B1", "base_tables": ["qualtrics__contact"]}] | [] | ["NTILE(4) OVER (ORDER BY total_count_completed_surveys)"] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B2 | COUNT(*) | [] | [] | True |
| B2 | SUM(total_count_completed_surveys) | [{"table": "qualtrics__contact", "column": "total_count_completed_surveys"}] | [] | False |
| B2 | AVG(total_count_completed_surveys) | [{"table": "qualtrics__contact", "column": "total_count_completed_surveys"}] | [] | False |
| B2 | AVG(avg_survey_progress_pct) | [{"table": "qualtrics__contact", "column": "avg_survey_progress_pct"}] | [] | False |
| B2 | AVG(count_surveys_completed_sms * 1.0 / NULLIF(count_surveys_sent_sms, 0)) | [{"table": "qualtrics__contact", "column": "count_surveys_completed_sms"}, {"table": "qualtrics__contact", "column": "count_surveys_sent_sms"}] | [] | False |


## S28

类别 `data`；来源 `query_db`；调用 `93a9c5d084c54a9e9023ffb8fc83c71c`；状态 `success`。

```sql
SELECT quartile, COUNT(*) AS users, SUM(total_count_completed_surveys) AS total_ltv, 
       AVG(total_count_completed_surveys) AS avg_ltv,
       AVG(avg_survey_progress_pct) AS avg_progress
FROM (
  SELECT *, NTILE(4) OVER (ORDER BY total_count_completed_surveys) AS quartile
  FROM qualtrics__contact
  WHERE count_surveys_sent_email > 0
) sub
GROUP BY quartile
ORDER BY quartile
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-082/attempt-01/sql/S28.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-082/attempt-01/sql/S28.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-082/attempt-01/results/S28.rows.jsonl)；完整：True；SHA256：`a51694a2536f8405e26c1521ac53b2e288df1319898295609bd44b30a949c838`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "qualtrics__contact", "kind": "base", "block": null, "base_tables": ["qualtrics__contact"]}] | [] | [] |
| B2 | [{"alias": "sub", "kind": "derived", "block": "B1", "base_tables": ["qualtrics__contact"]}] | [] | ["quartile"] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B2 | COUNT(*) | [] | [] | True |
| B2 | SUM(total_count_completed_surveys) | [{"table": "qualtrics__contact", "column": "total_count_completed_surveys"}] | [] | False |
| B2 | AVG(total_count_completed_surveys) | [{"table": "qualtrics__contact", "column": "total_count_completed_surveys"}] | [] | False |
| B2 | AVG(avg_survey_progress_pct) | [{"table": "qualtrics__contact", "column": "avg_survey_progress_pct"}] | [] | False |


## S29

类别 `data`；来源 `query_db`；调用 `6ff34c108f6049a489704423012c6315`；状态 `success`。

```sql
SELECT quartile, COUNT(*) AS users, SUM(total_count_completed_surveys) AS total_ltv, 
       AVG(total_count_completed_surveys) AS avg_ltv,
       AVG(avg_survey_progress_pct) AS avg_progress
FROM (
  SELECT *, NTILE(4) OVER (ORDER BY total_count_completed_surveys) AS quartile
  FROM qualtrics__contact
  WHERE count_surveys_sent_sms > 0
) sub
GROUP BY quartile
ORDER BY quartile
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-082/attempt-01/sql/S29.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-082/attempt-01/sql/S29.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-082/attempt-01/results/S29.rows.jsonl)；完整：True；SHA256：`294ba51b4db4346931745aaf1ba63332eeae1850515e9e59828eb4a0ba66351d`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "qualtrics__contact", "kind": "base", "block": null, "base_tables": ["qualtrics__contact"]}] | [] | [] |
| B2 | [{"alias": "sub", "kind": "derived", "block": "B1", "base_tables": ["qualtrics__contact"]}] | [] | ["quartile"] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B2 | COUNT(*) | [] | [] | True |
| B2 | SUM(total_count_completed_surveys) | [{"table": "qualtrics__contact", "column": "total_count_completed_surveys"}] | [] | False |
| B2 | AVG(total_count_completed_surveys) | [{"table": "qualtrics__contact", "column": "total_count_completed_surveys"}] | [] | False |
| B2 | AVG(avg_survey_progress_pct) | [{"table": "qualtrics__contact", "column": "avg_survey_progress_pct"}] | [] | False |


## S30

类别 `data`；来源 `query_db`；调用 `ceedd7d69c2b43d0805b239c6f448578`；状态 `success`。

```sql
SELECT 
  project_category,
  SUM(count_email_survey_responses) AS email_r,
  SUM(count_sms_survey_responses) AS sms_r,
  SUM(count_social_media_survey_responses) AS social_r,
  SUM(count_uncategorized_survey_responses) AS uncat_r,
  SUM(count_personal_link_survey_responses) AS plink_r,
  SUM(count_qr_code_survey_responses) AS qr_r
FROM qualtrics__survey
GROUP BY project_category
ORDER BY project_category
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-082/attempt-01/sql/S30.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-082/attempt-01/sql/S30.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-082/attempt-01/results/S30.rows.jsonl)；完整：True；SHA256：`2416464ee7894fbda8500fec505c01badb3779e30fdc7840329e4c641410fcbc`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "qualtrics__survey", "kind": "base", "block": null, "base_tables": ["qualtrics__survey"]}] | [] | ["project_category"] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | SUM(count_email_survey_responses) | [{"table": "qualtrics__survey", "column": "count_email_survey_responses"}] | [] | False |
| B1 | SUM(count_sms_survey_responses) | [{"table": "qualtrics__survey", "column": "count_sms_survey_responses"}] | [] | False |
| B1 | SUM(count_social_media_survey_responses) | [{"table": "qualtrics__survey", "column": "count_social_media_survey_responses"}] | [] | False |
| B1 | SUM(count_uncategorized_survey_responses) | [{"table": "qualtrics__survey", "column": "count_uncategorized_survey_responses"}] | [] | False |
| B1 | SUM(count_personal_link_survey_responses) | [{"table": "qualtrics__survey", "column": "count_personal_link_survey_responses"}] | [] | False |
| B1 | SUM(count_qr_code_survey_responses) | [{"table": "qualtrics__survey", "column": "count_qr_code_survey_responses"}] | [] | False |


## S31

类别 `data`；来源 `query_db`；调用 `9b4c32eefa5a454b83da47ba2a6f79d8`；状态 `success`。

```sql
SELECT 
  survey_status, COUNT(*) AS n,
  SUM(count_survey_responses) AS resp
FROM qualtrics__survey GROUP BY survey_status
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-082/attempt-01/sql/S31.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-082/attempt-01/sql/S31.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-082/attempt-01/results/S31.rows.jsonl)；完整：True；SHA256：`4eb1bf8f3605f9f6a47dfe5876718c27332b991f6463997d0276e75a2c0ead4d`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "qualtrics__survey", "kind": "base", "block": null, "base_tables": ["qualtrics__survey"]}] | [] | ["survey_status"] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |
| B1 | SUM(count_survey_responses) | [{"table": "qualtrics__survey", "column": "count_survey_responses"}] | [] | False |


## S32

类别 `data`；来源 `query_db`；调用 `d024cc96c8154591be14236f8b374aff`；状态 `success`。

```sql
SELECT project_category,
  SUM(count_email_survey_responses) AS email_r, SUM(count_email_completed_survey_responses) AS email_c,
  SUM(count_sms_survey_responses) AS sms_r, SUM(count_sms_completed_survey_responses) AS sms_c,
  SUM(count_social_media_survey_responses) AS social_r, SUM(count_social_media_completed_survey_responses) AS social_c,
  SUM(count_uncategorized_survey_responses) AS wm_r, SUM(count_uncategorized_completed_survey_responses) AS wm_c
FROM qualtrics__survey
GROUP BY project_category
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-082/attempt-01/sql/S32.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-082/attempt-01/sql/S32.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-082/attempt-01/results/S32.rows.jsonl)；完整：True；SHA256：`e0556454fe5c3a0c3498bed8d518308830ec3b6b59e011c4326306994f7f5eec`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "qualtrics__survey", "kind": "base", "block": null, "base_tables": ["qualtrics__survey"]}] | [] | ["project_category"] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | SUM(count_email_survey_responses) | [{"table": "qualtrics__survey", "column": "count_email_survey_responses"}] | [] | False |
| B1 | SUM(count_email_completed_survey_responses) | [{"table": "qualtrics__survey", "column": "count_email_completed_survey_responses"}] | [] | False |
| B1 | SUM(count_sms_survey_responses) | [{"table": "qualtrics__survey", "column": "count_sms_survey_responses"}] | [] | False |
| B1 | SUM(count_sms_completed_survey_responses) | [{"table": "qualtrics__survey", "column": "count_sms_completed_survey_responses"}] | [] | False |
| B1 | SUM(count_social_media_survey_responses) | [{"table": "qualtrics__survey", "column": "count_social_media_survey_responses"}] | [] | False |
| B1 | SUM(count_social_media_completed_survey_responses) | [{"table": "qualtrics__survey", "column": "count_social_media_completed_survey_responses"}] | [] | False |
| B1 | SUM(count_uncategorized_survey_responses) | [{"table": "qualtrics__survey", "column": "count_uncategorized_survey_responses"}] | [] | False |
| B1 | SUM(count_uncategorized_completed_survey_responses) | [{"table": "qualtrics__survey", "column": "count_uncategorized_completed_survey_responses"}] | [] | False |


## S33

类别 `data`；来源 `query_db`；调用 `b98a88a136174c4f9476060176998184`；状态 `success`。

```sql
SELECT 
  is_xm_directory_contact, is_research_core_contact,
  COUNT(*) AS n,
  AVG(total_count_completed_surveys) AS avg_ltv,
  SUM(total_count_completed_surveys) AS total_ltv
FROM qualtrics__contact
GROUP BY is_xm_directory_contact, is_research_core_contact
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-082/attempt-01/sql/S33.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-082/attempt-01/sql/S33.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-082/attempt-01/results/S33.rows.jsonl)；完整：True；SHA256：`2d33fe80fdb6cb7ba6dd5df06c494f4a8ce47bbbc2f7bea0946f8bb86293170d`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "qualtrics__contact", "kind": "base", "block": null, "base_tables": ["qualtrics__contact"]}] | [] | ["is_xm_directory_contact", "is_research_core_contact"] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |
| B1 | AVG(total_count_completed_surveys) | [{"table": "qualtrics__contact", "column": "total_count_completed_surveys"}] | [] | False |
| B1 | SUM(total_count_completed_surveys) | [{"table": "qualtrics__contact", "column": "total_count_completed_surveys"}] | [] | False |


## S34

类别 `data`；来源 `query_db`；调用 `b9299658892b4276916842efffd99020`；状态 `success`。

```sql
SELECT 
  CASE 
    WHEN count_surveys_sent_email > 0 AND count_surveys_sent_sms > 0 THEN 'both'
    WHEN count_surveys_sent_email > 0 THEN 'email_only'
    WHEN count_surveys_sent_sms > 0 THEN 'sms_only'
    ELSE 'neither'
  END AS channel_group,
  COUNT(*) AS users,
  SUM(total_count_completed_surveys) AS total_ltv,
  AVG(total_count_completed_surveys) AS avg_ltv,
  AVG(avg_survey_progress_pct) AS avg_progress,
  AVG(avg_survey_duration_in_seconds) AS avg_duration,
  SUM(count_surveys_completed_email) AS email_completed,
  SUM(count_surveys_completed_sms) AS sms_completed
FROM qualtrics__contact
GROUP BY channel_group
ORDER BY channel_group
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-082/attempt-01/sql/S34.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-082/attempt-01/sql/S34.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-082/attempt-01/results/S34.rows.jsonl)；完整：True；SHA256：`5d3eb1c899e2136205414d3a0dadfdbc5115ced4220164255fa95eea0e4e2641`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "qualtrics__contact", "kind": "base", "block": null, "base_tables": ["qualtrics__contact"]}] | [] | ["CASE WHEN count_surveys_sent_email > 0 AND count_surveys_sent_sms > 0 THEN 'both' WHEN count_surveys_sent_email > 0 THEN 'email_only' WHEN count_surveys_sent_sms > 0 THEN 'sms_only' ELSE 'neither' END"] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |
| B1 | SUM(total_count_completed_surveys) | [{"table": "qualtrics__contact", "column": "total_count_completed_surveys"}] | [] | False |
| B1 | AVG(total_count_completed_surveys) | [{"table": "qualtrics__contact", "column": "total_count_completed_surveys"}] | [] | False |
| B1 | AVG(avg_survey_progress_pct) | [{"table": "qualtrics__contact", "column": "avg_survey_progress_pct"}] | [] | False |
| B1 | AVG(avg_survey_duration_in_seconds) | [{"table": "qualtrics__contact", "column": "avg_survey_duration_in_seconds"}] | [] | False |
| B1 | SUM(count_surveys_completed_email) | [{"table": "qualtrics__contact", "column": "count_surveys_completed_email"}] | [] | False |
| B1 | SUM(count_surveys_completed_sms) | [{"table": "qualtrics__contact", "column": "count_surveys_completed_sms"}] | [] | False |


## S35

类别 `data`；来源 `query_db`；调用 `ddd2573c620b41b39d0f36fcdbb26c3a`；状态 `success`。

```sql
SELECT 
  email_domain,
  COUNT(*) AS users,
  AVG(total_count_completed_surveys) AS avg_ltv,
  SUM(total_count_completed_surveys) AS total_ltv
FROM qualtrics__contact
GROUP BY email_domain
ORDER BY avg_ltv DESC
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-082/attempt-01/sql/S35.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-082/attempt-01/sql/S35.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-082/attempt-01/results/S35.rows.jsonl)；完整：True；SHA256：`ee60745d955d510cd4c4da1185df6926592825f856781b27c0fb348796c79807`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "qualtrics__contact", "kind": "base", "block": null, "base_tables": ["qualtrics__contact"]}] | [] | ["email_domain"] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |
| B1 | AVG(total_count_completed_surveys) | [{"table": "qualtrics__contact", "column": "total_count_completed_surveys"}] | [] | False |
| B1 | SUM(total_count_completed_surveys) | [{"table": "qualtrics__contact", "column": "total_count_completed_surveys"}] | [] | False |


## S36

类别 `data`；来源 `query_db`；调用 `45602af748a14a61967be41e7118dc5b`；状态 `success`。

```sql
SELECT project_category,
  COUNT(*) AS total_surveys,
  SUM(CASE WHEN count_email_survey_responses > 0 THEN 1 ELSE 0 END) AS surveys_use_email,
  SUM(CASE WHEN count_sms_survey_responses > 0 THEN 1 ELSE 0 END) AS surveys_use_sms,
  SUM(CASE WHEN count_social_media_survey_responses > 0 THEN 1 ELSE 0 END) AS surveys_use_social,
  SUM(CASE WHEN count_uncategorized_survey_responses > 0 THEN 1 ELSE 0 END) AS surveys_use_uncat
FROM qualtrics__survey
GROUP BY project_category
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-082/attempt-01/sql/S36.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-082/attempt-01/sql/S36.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-082/attempt-01/results/S36.rows.jsonl)；完整：True；SHA256：`7ad16947485e7267fa3841338aeff63051d1e28d894a68ad1821f06aeab86347`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "qualtrics__survey", "kind": "base", "block": null, "base_tables": ["qualtrics__survey"]}] | [] | ["project_category"] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |
| B1 | SUM(CASE WHEN count_email_survey_responses > 0 THEN 1 ELSE 0 END) | [] | [{"table": "qualtrics__survey", "column": "count_email_survey_responses"}] | False |
| B1 | SUM(CASE WHEN count_sms_survey_responses > 0 THEN 1 ELSE 0 END) | [] | [{"table": "qualtrics__survey", "column": "count_sms_survey_responses"}] | False |
| B1 | SUM(CASE WHEN count_social_media_survey_responses > 0 THEN 1 ELSE 0 END) | [] | [{"table": "qualtrics__survey", "column": "count_social_media_survey_responses"}] | False |
| B1 | SUM(CASE WHEN count_uncategorized_survey_responses > 0 THEN 1 ELSE 0 END) | [] | [{"table": "qualtrics__survey", "column": "count_uncategorized_survey_responses"}] | False |


## S37

类别 `data`；来源 `query_db`；调用 `610ca41cb5974bb28e5317b6d5f7f218`；状态 `success`。

```sql
SELECT project_category,
  COUNT(*) AS n,
  AVG(count_email_survey_responses) AS avg_email_resp,
  AVG(count_sms_survey_responses) AS avg_sms_resp,
  AVG(count_social_media_survey_responses) AS avg_social_resp,
  AVG(count_uncategorized_survey_responses) AS avg_uncat_resp,
  AVG(count_questions) AS avg_questions
FROM qualtrics__survey
GROUP BY project_category
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-082/attempt-01/sql/S37.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-082/attempt-01/sql/S37.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-082/attempt-01/results/S37.rows.jsonl)；完整：True；SHA256：`b351c12f63ec02aab411668706aa2359cd2aca51527a43390c05722353452502`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "qualtrics__survey", "kind": "base", "block": null, "base_tables": ["qualtrics__survey"]}] | [] | ["project_category"] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |
| B1 | AVG(count_email_survey_responses) | [{"table": "qualtrics__survey", "column": "count_email_survey_responses"}] | [] | False |
| B1 | AVG(count_sms_survey_responses) | [{"table": "qualtrics__survey", "column": "count_sms_survey_responses"}] | [] | False |
| B1 | AVG(count_social_media_survey_responses) | [{"table": "qualtrics__survey", "column": "count_social_media_survey_responses"}] | [] | False |
| B1 | AVG(count_uncategorized_survey_responses) | [{"table": "qualtrics__survey", "column": "count_uncategorized_survey_responses"}] | [] | False |
| B1 | AVG(count_questions) | [{"table": "qualtrics__survey", "column": "count_questions"}] | [] | False |


## S38

类别 `data`；来源 `query_db`；调用 `0bdd03627b804d5c8d7e4144f4295bd6`；状态 `success`。

```sql
SELECT project_category, project_type,
  AVG(count_email_survey_responses) AS avg_email,
  AVG(count_sms_survey_responses) AS avg_sms,
  AVG(count_social_media_survey_responses) AS avg_social,
  AVG(count_uncategorized_survey_responses) AS avg_uncat,
  AVG(count_questions) AS avg_questions
FROM qualtrics__survey
GROUP BY project_category, project_type
ORDER BY project_category, project_type
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-082/attempt-01/sql/S38.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-082/attempt-01/sql/S38.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-082/attempt-01/results/S38.rows.jsonl)；完整：True；SHA256：`856a6998158b895c1c3240d83276051ab755412fdedbaed1c14ec4a4ca97ee8a`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "qualtrics__survey", "kind": "base", "block": null, "base_tables": ["qualtrics__survey"]}] | [] | ["project_category", "project_type"] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | AVG(count_email_survey_responses) | [{"table": "qualtrics__survey", "column": "count_email_survey_responses"}] | [] | False |
| B1 | AVG(count_sms_survey_responses) | [{"table": "qualtrics__survey", "column": "count_sms_survey_responses"}] | [] | False |
| B1 | AVG(count_social_media_survey_responses) | [{"table": "qualtrics__survey", "column": "count_social_media_survey_responses"}] | [] | False |
| B1 | AVG(count_uncategorized_survey_responses) | [{"table": "qualtrics__survey", "column": "count_uncategorized_survey_responses"}] | [] | False |
| B1 | AVG(count_questions) | [{"table": "qualtrics__survey", "column": "count_questions"}] | [] | False |

