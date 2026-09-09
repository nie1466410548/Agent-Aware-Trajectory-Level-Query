# dacomp-080

We've observed a clear stratification of engagement among our user base, especially noting…

运行：已提交。官方未评分。全部 SQL 尝试/成功 37/37；数据 SQL 35/35；Python 13 次。

完整原题：

We've observed a clear stratification of engagement among our user base, especially noting from the `user_cohort_analysis` table that `power_users` constitute a small fraction of the total but contribute significant value. Can you build a user value scoring model? The requirements are to calculate a composite score from 0-100 based on dimensions such as users' historical participation frequency, completion rate, and cross-channel activity. You also need to identify the key behavioral characteristics that drive the transition from `medium_value` to `high_value` users. Concurrently, analyze the differences in value transition paths among users of different languages and geographical regions. Finally, deliver an analysis report that includes a user segmentation strategy and a personalized incentive plan.

| 表 | 行数 | 列数 |
| --- | --- | --- |
| qualtrics__channel_performance | 5 | 17 |
| qualtrics__contact | 4000 | 35 |
| qualtrics__response | 72000 | 52 |
| qualtrics__user_cohort_analysis | 12 | 10 |


实际路线（分析者依据 SQL/源码概括，不代表 Agent 自述）：SQL 提取用户参与与跨渠道特征 → Python 价值分层、语言地域聚合和渠道连接 → 激励与分群建议。

数据库大小：38,604,800 字节。

## 数据 SQL

| SQL | 状态 | 基础表 | Join 输入/类型 | GROUP BY | 聚合表达式 | 结果行数 | 数据库 ms |
| --- | --- | --- | --- | --- | --- | --- | --- |
| [S3/Q1](#s3) | success | ["qualtrics__contact"] | 0 / {} | [] | ["COUNT(*)"] | 1 | 1.241 |
| [S4/Q2](#s4) | success | ["qualtrics__response"] | 0 / {} | [] | ["COUNT(*)", "COUNT(DISTINCT survey_response_id)", "COUNT(DISTINCT recipient_email)", "COUNT(DISTINCT user_language)"] | 1 | 151.746 |
| [S5/Q3](#s5) | success | ["qualtrics__user_cohort_analysis"] | 0 / {} | [] | [] | 12 | 0.358 |
| [S6/Q4](#s6) | success | ["qualtrics__channel_performance"] | 0 / {} | [] | [] | 5 | 0.353 |
| [S7/Q5](#s7) | success | ["qualtrics__response"] | 0 / {} | ["distribution_channel"] | ["COUNT(*)", "COUNT(DISTINCT survey_response_id)"] | 5 | 77.402 |
| [S8/Q6](#s8) | success | ["qualtrics__response"] | 0 / {} | ["user_language"] | ["COUNT(DISTINCT survey_response_id)", "COUNT(*)"] | 10 | 73.41 |
| [S9/Q7](#s9) | success | ["qualtrics__contact"] | 0 / {} | ["language"] | ["COUNT(*)"] | 10 | 2.049 |
| [S10/Q8](#s10) | success | ["qualtrics__response"] | 0 / {} | [] | ["MIN(survey_response_recorded_at)", "MAX(survey_response_recorded_at)", "MIN(survey_response_started_at)", "MAX(survey_response_started_at)"] | 1 | 27.141 |
| [S11/Q9](#s11) | success | ["qualtrics__contact"] | 0 / {} | [] | [] | 10 | 0.373 |
| [S12/Q10](#s12) | success | ["qualtrics__contact"] | 0 / {} | [] | ["MIN(total_count_surveys)", "MAX(total_count_surveys)", "AVG(total_count_surveys)", "MIN(total_count_completed_surveys)", "MAX(total_count_completed_surveys)", "AVG(total_count_completed_surveys)"] | 1 | 1.842 |
| [S13/Q11](#s13) | success | ["qualtrics__response"] | 0 / {} | ["survey_response_status"] | ["COUNT(*)"] | 2 | 26.543 |
| [S14/Q12](#s14) | success | ["qualtrics__contact"] | 0 / {} | [] | ["COUNT(*)"] | 1 | 1.034 |
| [S15/Q13](#s15) | success | ["qualtrics__contact", "qualtrics__response"] | 2 / {'INNER': 1} | [] | ["COUNT(DISTINCT r.recipient_email)"] | 1 | 80.059 |
| [S16/Q14](#s16) | success | ["qualtrics__response"] | 0 / {} | [] | ["COUNT(DISTINCT recipient_email)", "COUNT(DISTINCT survey_response_id)"] | 1 | 85.933 |
| [S17/Q15](#s17) | success | ["qualtrics__response"] | 0 / {} | [] | ["SUM(CASE WHEN NOT location_latitude IS NULL THEN 1 ELSE 0 END)", "SUM(CASE WHEN NOT ip_address IS NULL THEN 1 ELSE 0 END)", "SUM(CASE WHEN NOT recipient_email IS NULL THEN 1 ELSE 0 END)", "COUNT(*)"] | 1 | 24.755 |
| [S18/Q16](#s18) | success | ["qualtrics__response"] | 0 / {} | ["email_domain"] | ["COUNT(DISTINCT recipient_email)", "COUNT(*)"] | 6 | 77.579 |
| [S19/Q17](#s19) | success | ["qualtrics__response"] | 0 / {} | ["ip_address"] | ["COUNT(DISTINCT recipient_email)", "COUNT(*)"] | 20 | 69.744 |
| [S20/Q18](#s20) | success | ["qualtrics__response"] | 0 / {} | [] | [] | 9 | 18.932 |
| [S21/Q19](#s21) | success | ["qualtrics__response"] | 0 / {} | [] | ["MIN(survey_progress)", "MAX(survey_progress)", "AVG(survey_progress)", "MIN(duration_in_seconds)", "MAX(duration_in_seconds)", "AVG(duration_in_seconds)"] | 1 | 28.913 |
| [S22/Q20](#s22) | success | ["qualtrics__response"] | 0 / {} | ["is_finished_with_survey"] | ["COUNT(DISTINCT survey_response_id)"] | 2 | 70.013 |
| [S23/Q21](#s23) | success | ["qualtrics__response"] | 0 / {} | ["survey_response_id", "n_channels_in_resp"] | ["COUNT(DISTINCT distribution_channel)", "COUNT(*)"] | 1 | 68.414 |
| [S24/Q22](#s24) | success | ["qualtrics__response"] | 0 / {} | ["recipient_email", "n_langs_in_resp"] | ["COUNT(DISTINCT user_language)", "COUNT(*)"] | 8 | 63.369 |
| [S25/Q23](#s25) | success | ["qualtrics__response"] | 0 / {} | [] | ["SUM(CASE WHEN is_finished_with_survey = 1 AND survey_response_status = 1 THEN 1 ELSE 0 END)", "SUM(CASE WHEN is_finished_with_survey = 0 AND survey_response_status = 0 THEN 1 ELSE 0 END)", "SUM(CASE WHEN is_finished_with_survey = 0 AND survey_response_status = 1 THEN 1 ELSE 0 END)", "SUM(CASE WHEN is_finished_with_survey = 1 AND survey_response_status = 0 THEN 1 ELSE 0 END)"] | 1 | 28.257 |
| [S26/Q24](#s26) | success | ["qualtrics__response"] | 0 / {} | ["ROUND(location_latitude / 10) * 10", "ROUND(location_longitude / 20) * 20"] | ["COUNT(*)"] | 30 | 84.721 |
| [S27/Q25](#s27) | success | ["qualtrics__response"] | 0 / {} | ["CASE WHEN location_latitude > 0 AND location_longitude < -30 THEN 'AMERICAS' WHEN location_latitude <= 0 AND location_longitude < -30 THEN 'AMERICAS' WHEN location_latitude > 35 AND location_longitude >= -30 AND location_longitude < 60 THEN 'EUROPE' WHEN location_latitude <= 35 AND location_longitude >= -30 AND location_longitude < 60 THEN 'AFRICA/MIDEAST' WHEN location_longitude >= 60 AND location_longitude < 180 THEN 'ASIA/OCEANIA' ELSE 'OTHER' END"] | ["COUNT(*)"] | 4 | 56.511 |
| [S28/Q26](#s28) | success | ["qualtrics__response"] | 2 / {'LEFT': 1} | ["recipient_email", "user_language", "recipient_email"] | ["COUNT(*)", "COUNT(DISTINCT survey_response_id)", "COUNT(DISTINCT survey_id)", "COUNT(DISTINCT CASE WHEN is_finished_with_survey = 1 THEN survey_response_id END)", "COUNT(DISTINCT distribution_channel)", "COUNT(DISTINCT DATE(survey_response_recorded_at))", "AVG(survey_progress)", "AVG(duration_in_seconds)", "AVG(location_latitude)", "AVG(location_longitude)", "MIN(survey_response_recorded_at)", "MAX(survey_response_recorded_at)"] | 4422 | 5584.54 |
| [S29/Q27](#s29) | success | ["qualtrics__response"] | 0 / {} | ["recipient_email", "n_survey_responses"] | ["COUNT(DISTINCT survey_response_id)", "COUNT(*)", "COUNT(*)", "COUNT(*)"] | 13 | 66.461 |
| [S30/Q28](#s30) | success | ["qualtrics__response"] | 0 / {} | ["recipient_email", "user_language", "recipient_email"] | ["COUNT(*)", "COUNT(DISTINCT survey_response_id)", "COUNT(DISTINCT CASE WHEN is_finished_with_survey = 1 THEN survey_response_id END)", "COUNT(DISTINCT distribution_channel)", "AVG(survey_progress)", "MIN(n_survey_responses)", "MAX(n_survey_responses)", "AVG(n_survey_responses)", "MIN(n_completed)", "MAX(n_completed)", "AVG(n_completed)", "MIN(completion_rate)", "MAX(completion_rate)", "AVG(completion_rate)", "MIN(n_channels)", "MAX(n_channels)", "AVG(n_channels)", "MIN(avg_progress)", "MAX(avg_progress)", "AVG(avg_progress)"] | 1 | 91.401 |
| [S31/Q29](#s31) | success | ["qualtrics__response"] | 2 / {'LEFT': 1} | ["recipient_email", "user_language", "recipient_email"] | ["COUNT(*)", "COUNT(DISTINCT survey_response_id)", "COUNT(DISTINCT survey_id)", "COUNT(DISTINCT CASE WHEN is_finished_with_survey = 1 THEN survey_response_id END)", "COUNT(DISTINCT distribution_channel)", "COUNT(DISTINCT DATE(survey_response_recorded_at))", "AVG(survey_progress)", "AVG(duration_in_seconds)", "AVG(location_latitude)", "AVG(location_longitude)", "MIN(survey_response_recorded_at)", "MAX(survey_response_recorded_at)"] | 4422 | 5575.276 |
| [S32/Q30](#s32) | success | ["qualtrics__contact"] | 0 / {} | ["CASE WHEN total_count_surveys = 1 THEN 'one' WHEN total_count_surveys BETWEEN 2 AND 5 THEN '2-5' WHEN total_count_surveys BETWEEN 6 AND 10 THEN '6-10' WHEN total_count_surveys BETWEEN 11 AND 20 THEN '11-20' WHEN total_count_surveys > 20 THEN '21+' END"] | ["COUNT(*)"] | 5 | 2.223 |
| [S33/Q31](#s33) | success | ["qualtrics__contact"] | 0 / {} | ["STRFTIME('%Y-%m', created_at)"] | ["COUNT(*)"] | 1 | 1.515 |
| [S34/Q32](#s34) | success | ["qualtrics__contact"] | 0 / {} | [] | ["COUNT(*)", "SUM(CASE WHEN total_count_completed_surveys = 0 THEN 1 ELSE 0 END)", "AVG(total_count_surveys)", "AVG(total_count_completed_surveys)", "AVG(1.0 * total_count_completed_surveys / NULLIF(total_count_surveys, 0))", "AVG(avg_survey_progress_pct)", "AVG(count_surveys_completed_email)", "AVG(count_surveys_completed_sms)"] | 1 | 2.181 |
| [S35/Q33](#s35) | success | ["qualtrics__response"] | 0 / {} | ["recipient_email"] | ["MAX(CASE WHEN distribution_channel = 'email' THEN 1 ELSE 0 END)", "MAX(CASE WHEN distribution_channel = 'sms' THEN 1 ELSE 0 END)", "MAX(CASE WHEN distribution_channel = 'mobile' THEN 1 ELSE 0 END)", "MAX(CASE WHEN distribution_channel = 'web' THEN 1 ELSE 0 END)", "MAX(CASE WHEN distribution_channel = 'social' THEN 1 ELSE 0 END)", "COUNT(DISTINCT distribution_channel)"] | 4422 | 91.522 |
| [S36/Q34](#s36) | success | ["qualtrics__user_cohort_analysis"] | 0 / {} | [] | [] | 12 | 0.472 |
| [S37/Q35](#s37) | success | ["qualtrics__response"] | 0 / {} | ["recipient_email"] | ["MAX(CASE WHEN distribution_channel = 'email' THEN 1 ELSE 0 END)", "MAX(CASE WHEN distribution_channel = 'sms' THEN 1 ELSE 0 END)", "MAX(CASE WHEN distribution_channel = 'mobile' THEN 1 ELSE 0 END)", "MAX(CASE WHEN distribution_channel = 'web' THEN 1 ELSE 0 END)", "MAX(CASE WHEN distribution_channel = 'social' THEN 1 ELSE 0 END)"] | 4422 | 81.9 |


## 元数据和设置

| SQL | 类别 | 状态 | 内容 |
| --- | --- | --- | --- |
| S1 | connection_setup | success | PRAGMA query_only=ON |
| S2 | metadata | success | SELECT name,sql FROM sqlite_master WHERE type='table' ORDER BY name |


## Python 与执行位置

人工源码审查：**database_first_violation**。Python 按价值层级、语言和大洲计算均值、数量及贡献份额，按邮箱连接渠道信息并计算高低价值差异。这些 SQL 可支持的连接与聚合迁出数据库；效应量、显著性检验和绘图单独评价。 [证据](../reviews/dacomp-080.json)。

P1：Loading the user-level profile (already aggregated in SQL) into pandas to design the composite scoring model, normalize dimensions, and derive geographic regions from average coordinates — normalization/threshold decisions and geographic mapping are easier and more transparent in Python than in SQL.

[源码](../../../runs/dsv4flash-db-first-full-01/dacomp-080/attempt-01/python/P1.py)；[输出](../../../runs/dsv4flash-db-first-full-01/dacomp-080/attempt-01/python/P1.stdout)；[错误](../../../runs/dsv4flash-db-first-full-01/dacomp-080/attempt-01/python/P1.stderr)。检出需人工核验的 SQL 可实现操作：.query(；不能仅凭理由判为合规。

P2：Computing the composite 0-100 value score from the three required dimensions (participation frequency, completion rate, cross-channel activity) plus engagement depth, and assigning tiers — normalization and thresholding are model-design decisions better done in Python.

[源码](../../../runs/dsv4flash-db-first-full-01/dacomp-080/attempt-01/python/P2.py)；[输出](../../../runs/dsv4flash-db-first-full-01/dacomp-080/attempt-01/python/P2.stdout)；[错误](../../../runs/dsv4flash-db-first-full-01/dacomp-080/attempt-01/python/P2.stderr)。自动源码筛查未检出预设迁出信号；这不是全面语义合规证明。

P3：Refining the scoring normalization and tier thresholds to better match the expected proportions from the cohort analysis table, which requires experimentation with threshold values in Python.

[源码](../../../runs/dsv4flash-db-first-full-01/dacomp-080/attempt-01/python/P3.py)；[输出](../../../runs/dsv4flash-db-first-full-01/dacomp-080/attempt-01/python/P3.stdout)；[错误](../../../runs/dsv4flash-db-first-full-01/dacomp-080/attempt-01/python/P3.stderr)。自动源码筛查未检出预设迁出信号；这不是全面语义合规证明。

P4：Finalizing the composite score with min-max normalized dimensions and tier thresholds, then computing per-tier size and value contribution to validate that power/high-value users are a small fraction contributing disproportionate value — as required by the task.

[源码](../../../runs/dsv4flash-db-first-full-01/dacomp-080/attempt-01/python/P4.py)；[输出](../../../runs/dsv4flash-db-first-full-01/dacomp-080/attempt-01/python/P4.stdout)；[错误](../../../runs/dsv4flash-db-first-full-01/dacomp-080/attempt-01/python/P4.stderr)。检出需人工核验的 SQL 可实现操作：groupby(, sort_values(；不能仅凭理由判为合规。

P5：Mapping geographic regions from lat/lon coordinates and performing statistical comparison (Mann-Whitney U test + Cohen's d effect size) between medium_value and high_value users to identify the key behavioral characteristics driving the transition. This is a statistical analysis better done in Python.

[源码](../../../runs/dsv4flash-db-first-full-01/dacomp-080/attempt-01/python/P5.py)；[输出](../../../runs/dsv4flash-db-first-full-01/dacomp-080/attempt-01/python/P5.stdout)；[错误](../../../runs/dsv4flash-db-first-full-01/dacomp-080/attempt-01/python/P5.stderr)。检出需人工核验的 SQL 可实现操作：sort_values(；不能仅凭理由判为合规。

P6：Fixing the variable name typo and completing the transition analysis with Mann-Whitney U tests and Cohen's d effect sizes between medium and high value users.

[源码](../../../runs/dsv4flash-db-first-full-01/dacomp-080/attempt-01/python/P6.py)；[输出](../../../runs/dsv4flash-db-first-full-01/dacomp-080/attempt-01/python/P6.stdout)；[错误](../../../runs/dsv4flash-db-first-full-01/dacomp-080/attempt-01/python/P6.stderr)。检出需人工核验的 SQL 可实现操作：sort_values(；不能仅凭理由判为合规。

P7：Analyzing value score and tier composition differences across user languages and geographic regions using aggregation on the already-scored user profile in Python.

[源码](../../../runs/dsv4flash-db-first-full-01/dacomp-080/attempt-01/python/P7.py)；[输出](../../../runs/dsv4flash-db-first-full-01/dacomp-080/attempt-01/python/P7.stdout)；[错误](../../../runs/dsv4flash-db-first-full-01/dacomp-080/attempt-01/python/P7.stderr)。检出需人工核验的 SQL 可实现操作：groupby(, sort_values(；不能仅凭理由判为合规。

P8：Generating all visualizations (score distribution, tier contribution, medium vs high comparison, language/region analysis, tier heatmaps, and score decomposition) to support the report. These are plotting tasks that must be done outside the database.

[源码](../../../runs/dsv4flash-db-first-full-01/dacomp-080/attempt-01/python/P8.py)；[输出](../../../runs/dsv4flash-db-first-full-01/dacomp-080/attempt-01/python/P8.stdout)；[错误](../../../runs/dsv4flash-db-first-full-01/dacomp-080/attempt-01/python/P8.stderr)。检出需人工核验的 SQL 可实现操作：groupby(, sort_values(；不能仅凭理由判为合规。

P9：Using logistic regression (a statistical method better suited to Python) to quantify which behavioral features drive medium→high transition, plus chi-square tests for tier associations with language/region, and per-language/region transition-gap profiles.

[源码](../../../runs/dsv4flash-db-first-full-01/dacomp-080/attempt-01/python/P9.py)；[输出](../../../runs/dsv4flash-db-first-full-01/dacomp-080/attempt-01/python/P9.stdout)；[错误](../../../runs/dsv4flash-db-first-full-01/dacomp-080/attempt-01/python/P9.stderr)。自动源码筛查未检出预设迁出信号；这不是全面语义合规证明。

P10：Running chi-square tests for tier-language/region associations and t-tests for per-language/region transition gaps, using scipy since sklearn is unavailable. Also computing the segmentation summary table.

[源码](../../../runs/dsv4flash-db-first-full-01/dacomp-080/attempt-01/python/P10.py)；[输出](../../../runs/dsv4flash-db-first-full-01/dacomp-080/attempt-01/python/P10.stdout)；[错误](../../../runs/dsv4flash-db-first-full-01/dacomp-080/attempt-01/python/P10.stderr)。检出需人工核验的 SQL 可实现操作：groupby(；不能仅凭理由判为合规。

P11：Analyzing channel prevalence among high-value users (via a SQL-aggregated channel matrix joined to the scored profile) and visualizing cohort-table trends and per-region transition gaps — mixed SQL extraction plus Python visualization/statistics.

[源码](../../../runs/dsv4flash-db-first-full-01/dacomp-080/attempt-01/python/P11.py)；[输出](../../../runs/dsv4flash-db-first-full-01/dacomp-080/attempt-01/python/P11.stdout)；[错误](../../../runs/dsv4flash-db-first-full-01/dacomp-080/attempt-01/python/P11.stderr)。检出需人工核验的 SQL 可实现操作：groupby(, .merge(, .query(；不能仅凭理由判为合规。

P12：Fixing dataframe column name collision from merge and completing the transition-gap-by-region visualization.

[源码](../../../runs/dsv4flash-db-first-full-01/dacomp-080/attempt-01/python/P12.py)；[输出](../../../runs/dsv4flash-db-first-full-01/dacomp-080/attempt-01/python/P12.stdout)；[错误](../../../runs/dsv4flash-db-first-full-01/dacomp-080/attempt-01/python/P12.stderr)。检出需人工核验的 SQL 可实现操作：.merge(, .query(；不能仅凭理由判为合规。

P13：Verifying all figure files exist before writing the report.

[源码](../../../runs/dsv4flash-db-first-full-01/dacomp-080/attempt-01/python/P13.py)；[输出](../../../runs/dsv4flash-db-first-full-01/dacomp-080/attempt-01/python/P13.stdout)；[错误](../../../runs/dsv4flash-db-first-full-01/dacomp-080/attempt-01/python/P13.stderr)。自动源码筛查未检出预设迁出信号；这不是全面语义合规证明。

## 优化机会

已验证候选。筛选限于精确 SQL、相同自包含 CTE、相同单表完整过滤、可分解单表聚合；未覆盖任意 Join 等价和一般谓词蕴含。全部候选都是 offline，未测在线预测。

| 候选 | 类型 | 已有结果 | 覆盖 SQL | 后续次数 | 中间行数 | 验证 | 成本 |
| --- | --- | --- | --- | --- | --- | --- | --- |
| C1 | exact-result reuse | True | ["S28", "S31"] | 1 | unknown | not_verified_cap | Not tested |
| C2 | common subexpression | False | ["S28", "S30", "S31"] | 2 | 4422 | verified | Warm-cache baseline 8716.946 ms vs build+reuse 3207.390 ms, ratio 2.718; five repetitions, see performance evidence. |
| C3 | common subexpression | False | ["S28", "S31"] | 1 | unknown | not_verified_cap | Not tested |
| C4 | aggregate MV | False | ["S3", "S9", "S12", "S32", "S33", "S34"] | 5 | 50 | rejected_result_mismatch | Not benchmarked; correctness alone does not establish net speedup. |
| C5 | aggregate MV | False | ["S10", "S13", "S17", "S21", "S25", "S26", "S27", "S37"] | 7 | 17632 | rejected_result_mismatch | Not benchmarked; correctness alone does not establish net speedup. |


已验证覆盖（含触发查询、候选并集去重）：3/35 条成功数据 SQL。正确性仅针对当前数据库快照；未测性能的候选不能声称已加速。

[完整 build/rewrite 与比较证据](dacomp-080.analysis.json)。

### C2：common subexpression

Identical self-contained CTE body across queries.

原查询 [S28](#s28), [S30](#s30), [S31](#s31) → 新增共享状态 C2 → 后续 2 次可复用。该构建点为事后假设，不代表 Agent 当时预知后续。

构建定义：

```sql
SELECT recipient_email, user_language AS dom_lang FROM (SELECT recipient_email, user_language, ROW_NUMBER() OVER (PARTITION BY recipient_email ORDER BY COUNT(*) DESC) AS rn FROM qualtrics__response GROUP BY recipient_email, user_language) WHERE rn = 1
```

受益查询 S28 的改写示例：

```sql
WITH lang_mode AS (SELECT * FROM temp.reuse_candidate), user_agg AS (SELECT recipient_email AS email, COUNT(DISTINCT survey_response_id) AS n_survey_responses, COUNT(DISTINCT survey_id) AS n_distinct_surveys, COUNT(DISTINCT CASE WHEN is_finished_with_survey = 1 THEN survey_response_id END) AS n_completed, COUNT(DISTINCT distribution_channel) AS n_channels, COUNT(DISTINCT DATE(survey_response_recorded_at)) AS n_active_days, AVG(survey_progress) AS avg_progress, AVG(duration_in_seconds) AS avg_duration, AVG(location_latitude) AS avg_lat, AVG(location_longitude) AS avg_lon, MIN(survey_response_recorded_at) AS first_response_at, MAX(survey_response_recorded_at) AS last_response_at FROM qualtrics__response GROUP BY recipient_email) SELECT u.*, l.dom_lang, 1.0 * u.n_completed / u.n_survey_responses AS completion_rate, (JULIANDAY(u.last_response_at) - JULIANDAY(u.first_response_at)) / 30.44 AS active_months FROM user_agg AS u LEFT JOIN lang_mode AS l ON l.recipient_email = u.email ORDER BY u.n_survey_responses DESC
```

| 原 SQL | 列名一致 | 结果一致 | 比较方法 |
| --- | --- | --- | --- |
| S28 | True | True | ordered_numeric_tolerance |
| S30 | True | True | exact_multiset |
| S31 | True | True | ordered_numeric_tolerance |


验证状态：verified；成本结论：Warm-cache baseline 8716.946 ms vs build+reuse 3207.390 ms, ratio 2.718; five repetitions, see performance evidence.

### C5：aggregate MV

Union of grouping keys; decomposable aggregate states; AVG uses SUM and non-NULL COUNT.

原查询 [S10](#s10), [S13](#s13), [S17](#s17), [S21](#s21), [S25](#s25), [S26](#s26), [S27](#s27), [S37](#s37) → 新增共享状态 C5 → 后续 7 次可复用。该构建点为事后假设，不代表 Agent 当时预知后续。

构建定义：

```sql
SELECT survey_response_status AS __g0, ROUND(location_latitude / 10) * 10 AS __g1, ROUND(location_longitude / 20) * 20 AS __g2, CASE WHEN location_latitude > 0 AND location_longitude < -30 THEN 'AMERICAS' WHEN location_latitude <= 0 AND location_longitude < -30 THEN 'AMERICAS' WHEN location_latitude > 35 AND location_longitude >= -30 AND location_longitude < 60 THEN 'EUROPE' WHEN location_latitude <= 35 AND location_longitude >= -30 AND location_longitude < 60 THEN 'AFRICA/MIDEAST' WHEN location_longitude >= 60 AND location_longitude < 180 THEN 'ASIA/OCEANIA' ELSE 'OTHER' END AS __g3, recipient_email AS __g4, MIN(survey_response_recorded_at) AS __a0, MAX(survey_response_recorded_at) AS __a1, MIN(survey_response_started_at) AS __a2, MAX(survey_response_started_at) AS __a3, COUNT(*) AS __a4, SUM(CASE WHEN NOT location_latitude IS NULL THEN 1 ELSE 0 END) AS __a5, SUM(CASE WHEN NOT ip_address IS NULL THEN 1 ELSE 0 END) AS __a6, SUM(CASE WHEN NOT recipient_email IS NULL THEN 1 ELSE 0 END) AS __a7, MIN(survey_progress) AS __a8, MAX(survey_progress) AS __a9, SUM(survey_progress) AS __a10_sum, COUNT(survey_progress) AS __a10_n, MIN(duration_in_seconds) AS __a11, MAX(duration_in_seconds) AS __a12, SUM(duration_in_seconds) AS __a13_sum, COUNT(duration_in_seconds) AS __a13_n, SUM(CASE WHEN is_finished_with_survey = 1 AND survey_response_status = 1 THEN 1 ELSE 0 END) AS __a14, SUM(CASE WHEN is_finished_with_survey = 0 AND survey_response_status = 0 THEN 1 ELSE 0 END) AS __a15, SUM(CASE WHEN is_finished_with_survey = 0 AND survey_response_status = 1 THEN 1 ELSE 0 END) AS __a16, SUM(CASE WHEN is_finished_with_survey = 1 AND survey_response_status = 0 THEN 1 ELSE 0 END) AS __a17, MAX(CASE WHEN distribution_channel = 'email' THEN 1 ELSE 0 END) AS __a18, MAX(CASE WHEN distribution_channel = 'sms' THEN 1 ELSE 0 END) AS __a19, MAX(CASE WHEN distribution_channel = 'mobile' THEN 1 ELSE 0 END) AS __a20, MAX(CASE WHEN distribution_channel = 'web' THEN 1 ELSE 0 END) AS __a21, MAX(CASE WHEN distribution_channel = 'social' THEN 1 ELSE 0 END) AS __a22 FROM "qualtrics__response"  GROUP BY survey_response_status, ROUND(location_latitude / 10) * 10, ROUND(location_longitude / 20) * 20, CASE WHEN location_latitude > 0 AND location_longitude < -30 THEN 'AMERICAS' WHEN location_latitude <= 0 AND location_longitude < -30 THEN 'AMERICAS' WHEN location_latitude > 35 AND location_longitude >= -30 AND location_longitude < 60 THEN 'EUROPE' WHEN location_latitude <= 35 AND location_longitude >= -30 AND location_longitude < 60 THEN 'AFRICA/MIDEAST' WHEN location_longitude >= 60 AND location_longitude < 180 THEN 'ASIA/OCEANIA' ELSE 'OTHER' END, recipient_email
```

受益查询 S10 的改写示例：

```sql
SELECT MIN(__a0) AS min_ts, MAX(__a1) AS max_ts, MIN(__a2) AS min_start, MAX(__a3) AS max_start FROM temp.reuse_candidate
```

| 原 SQL | 列名一致 | 结果一致 | 比较方法 |
| --- | --- | --- | --- |
| S10 | True | True | exact_multiset |
| S13 | True | True | exact_multiset |
| S17 | True | True | exact_multiset |
| S21 | True | False | exact_multiset |
| S25 | True | True | exact_multiset |
| S26 | True | True | ordered_numeric_tolerance |
| S27 | True | True | exact_multiset |
| S37 | True | True | exact_multiset |


验证状态：rejected_result_mismatch；成本结论：Not benchmarked; correctness alone does not establish net speedup.

### C4：aggregate MV

Union of grouping keys; decomposable aggregate states; AVG uses SUM and non-NULL COUNT.

原查询 [S3](#s3), [S9](#s9), [S12](#s12), [S32](#s32), [S33](#s33), [S34](#s34) → 新增共享状态 C4 → 后续 5 次可复用。该构建点为事后假设，不代表 Agent 当时预知后续。

构建定义：

```sql
SELECT language AS __g0, CASE WHEN total_count_surveys = 1 THEN 'one' WHEN total_count_surveys BETWEEN 2 AND 5 THEN '2-5' WHEN total_count_surveys BETWEEN 6 AND 10 THEN '6-10' WHEN total_count_surveys BETWEEN 11 AND 20 THEN '11-20' WHEN total_count_surveys > 20 THEN '21+' END AS __g1, STRFTIME('%Y-%m', created_at) AS __g2, COUNT(*) AS __a0, MIN(total_count_surveys) AS __a1, MAX(total_count_surveys) AS __a2, SUM(total_count_surveys) AS __a3_sum, COUNT(total_count_surveys) AS __a3_n, MIN(total_count_completed_surveys) AS __a4, MAX(total_count_completed_surveys) AS __a5, SUM(total_count_completed_surveys) AS __a6_sum, COUNT(total_count_completed_surveys) AS __a6_n, SUM(CASE WHEN total_count_completed_surveys = 0 THEN 1 ELSE 0 END) AS __a7, SUM(1.0 * total_count_completed_surveys / NULLIF(total_count_surveys, 0)) AS __a8_sum, COUNT(1.0 * total_count_completed_surveys / NULLIF(total_count_surveys, 0)) AS __a8_n, SUM(avg_survey_progress_pct) AS __a9_sum, COUNT(avg_survey_progress_pct) AS __a9_n, SUM(count_surveys_completed_email) AS __a10_sum, COUNT(count_surveys_completed_email) AS __a10_n, SUM(count_surveys_completed_sms) AS __a11_sum, COUNT(count_surveys_completed_sms) AS __a11_n FROM "qualtrics__contact"  GROUP BY language, CASE WHEN total_count_surveys = 1 THEN 'one' WHEN total_count_surveys BETWEEN 2 AND 5 THEN '2-5' WHEN total_count_surveys BETWEEN 6 AND 10 THEN '6-10' WHEN total_count_surveys BETWEEN 11 AND 20 THEN '11-20' WHEN total_count_surveys > 20 THEN '21+' END, STRFTIME('%Y-%m', created_at)
```

受益查询 S3 的改写示例：

```sql
SELECT SUM(__a0) AS n_contacts FROM temp.reuse_candidate
```

| 原 SQL | 列名一致 | 结果一致 | 比较方法 |
| --- | --- | --- | --- |
| S3 | True | True | exact_multiset |
| S9 | True | True | ordered_numeric_tolerance |
| S12 | True | True | exact_multiset |
| S32 | True | True | ordered_numeric_tolerance |
| S33 | True | True | ordered_numeric_tolerance |
| S34 | True | False | exact_multiset |


验证状态：rejected_result_mismatch；成本结论：Not benchmarked; correctness alone does not establish net speedup.

[性能证据 C2](dacomp-080.C2.performance.json)：measured。

结果依赖：自动记录 SQL→Python 的接口父调用，以及源码中引用归档文件的消费者；字面值相同不认定因果。模型方向选择需要人工读取消息，尚未做全面因果标注。

[原始报告](../../../runs/dsv4flash-db-first-full-01/dacomp-080/attempt-01/answer.md)；[统一消息](../../../runs/dsv4flash-db-first-full-01/dacomp-080/attempt-01/messages.jsonl)；[原始 OpenCode 事件](../../../runs/dsv4flash-db-first-full-01/dacomp-080/attempt-01/opencode.jsonl)；[SQL 引擎日志](../../../runs/dsv4flash-db-first-full-01/dacomp-080/attempt-01/sql_journal.jsonl)。

[可读报告（本地图片链接规范化）](../answers/dacomp-080.md)。原始回答保留，分析结论未改写。

## S1

类别 `connection_setup`；来源 `connection`；调用 `03a49f77cb724efe85f7ab7f5031b4c3`；状态 `success`。

```sql
PRAGMA query_only=ON
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-080/attempt-01/sql/S1.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-080/attempt-01/sql/S1.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-080/attempt-01/results/S1.rows.jsonl)；完整：True；SHA256：`e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`。

## S2

类别 `metadata`；来源 `list_db`；调用 `03a49f77cb724efe85f7ab7f5031b4c3`；状态 `success`。

```sql
SELECT name,sql FROM sqlite_master WHERE type='table' ORDER BY name
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-080/attempt-01/sql/S2.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-080/attempt-01/sql/S2.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-080/attempt-01/results/S2.rows.jsonl)；完整：True；SHA256：`0a4451bbce87ac19f4f3f5878b1541ff809cd57392df7b85d1cd86f076a46d75`。

## S3

类别 `data`；来源 `query_db`；调用 `bbf68b64c3f344eea9aada2add46faa6`；状态 `success`。

```sql
SELECT COUNT(*) AS n_contacts FROM qualtrics__contact
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-080/attempt-01/sql/S3.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-080/attempt-01/sql/S3.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-080/attempt-01/results/S3.rows.jsonl)；完整：True；SHA256：`d093e3367a29f8b5872b0a40238b39e2ec283fd7fa1bdad2c364b5ec2b029e54`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "qualtrics__contact", "kind": "base", "block": null, "base_tables": ["qualtrics__contact"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |


## S4

类别 `data`；来源 `query_db`；调用 `07b7e98497e045a2b61ae5af769078a8`；状态 `success`。

```sql
SELECT COUNT(*) AS n_responses, COUNT(DISTINCT survey_response_id) AS n_survey_responses, COUNT(DISTINCT recipient_email) AS n_emails, COUNT(DISTINCT user_language) AS n_langs FROM qualtrics__response
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-080/attempt-01/sql/S4.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-080/attempt-01/sql/S4.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-080/attempt-01/results/S4.rows.jsonl)；完整：True；SHA256：`809de9337dd4e8146b7a5d37cd23e50fd23cfae0ce2694c7b3a17840770bd757`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "qualtrics__response", "kind": "base", "block": null, "base_tables": ["qualtrics__response"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |
| B1 | COUNT(DISTINCT survey_response_id) | [{"table": "qualtrics__response", "column": "survey_response_id"}] | [] | False |
| B1 | COUNT(DISTINCT recipient_email) | [{"table": "qualtrics__response", "column": "recipient_email"}] | [] | False |
| B1 | COUNT(DISTINCT user_language) | [{"table": "qualtrics__response", "column": "user_language"}] | [] | False |


## S5

类别 `data`；来源 `query_db`；调用 `b2442545524f45f79de78eafa01ebf47`；状态 `success`。

```sql
SELECT * FROM qualtrics__user_cohort_analysis ORDER BY cohort_month LIMIT 20
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-080/attempt-01/sql/S5.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-080/attempt-01/sql/S5.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-080/attempt-01/results/S5.rows.jsonl)；完整：True；SHA256：`f2194186817388282681f63879fe09e16a51b43921168285dc19ca9b51f1b2b9`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "qualtrics__user_cohort_analysis", "kind": "base", "block": null, "base_tables": ["qualtrics__user_cohort_analysis"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |


## S6

类别 `data`；来源 `query_db`；调用 `e3c022bb1aa64b95afe976aefb01f36c`；状态 `success`。

```sql
SELECT * FROM qualtrics__channel_performance ORDER BY completion_rate DESC
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-080/attempt-01/sql/S6.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-080/attempt-01/sql/S6.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-080/attempt-01/results/S6.rows.jsonl)；完整：True；SHA256：`977a1c2c082bf7a401f4aedf2ceb186b22967d3b2713dfe83daf851a5a9eb4be`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "qualtrics__channel_performance", "kind": "base", "block": null, "base_tables": ["qualtrics__channel_performance"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |


## S7

类别 `data`；来源 `query_db`；调用 `ecaada41559540d985534ba9fb66160c`；状态 `success`。

```sql
SELECT distribution_channel, COUNT(*) AS n_rows, COUNT(DISTINCT survey_response_id) AS n_survey_resp FROM qualtrics__response GROUP BY distribution_channel
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-080/attempt-01/sql/S7.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-080/attempt-01/sql/S7.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-080/attempt-01/results/S7.rows.jsonl)；完整：True；SHA256：`24d9dabde1bf33f333579ddb3dceccbbd91486339d49e44cdf0b1b907ff70187`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "qualtrics__response", "kind": "base", "block": null, "base_tables": ["qualtrics__response"]}] | [] | ["distribution_channel"] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |
| B1 | COUNT(DISTINCT survey_response_id) | [{"table": "qualtrics__response", "column": "survey_response_id"}] | [] | False |


## S8

类别 `data`；来源 `query_db`；调用 `03aa5e17033b41908d58cef6131c11f2`；状态 `success`。

```sql
SELECT user_language, COUNT(DISTINCT survey_response_id) AS n_survey_resp, COUNT(*) AS n_rows FROM qualtrics__response GROUP BY user_language ORDER BY n_survey_resp DESC
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-080/attempt-01/sql/S8.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-080/attempt-01/sql/S8.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-080/attempt-01/results/S8.rows.jsonl)；完整：True；SHA256：`fdf6ece91b1aeae355512c298e9372af93de5aa1f204f029e4f2b3423850ab09`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "qualtrics__response", "kind": "base", "block": null, "base_tables": ["qualtrics__response"]}] | [] | ["user_language"] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(DISTINCT survey_response_id) | [{"table": "qualtrics__response", "column": "survey_response_id"}] | [] | False |
| B1 | COUNT(*) | [] | [] | True |


## S9

类别 `data`；来源 `query_db`；调用 `93f6119694d14156b85080b1e62db23a`；状态 `success`。

```sql
SELECT language, COUNT(*) AS n FROM qualtrics__contact GROUP BY language ORDER BY n DESC
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-080/attempt-01/sql/S9.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-080/attempt-01/sql/S9.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-080/attempt-01/results/S9.rows.jsonl)；完整：True；SHA256：`7c525020415a584e6ea43100b5962659dfbbcd72e35c1ae49d77b8563560fe77`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "qualtrics__contact", "kind": "base", "block": null, "base_tables": ["qualtrics__contact"]}] | [] | ["language"] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |


## S10

类别 `data`；来源 `query_db`；调用 `9812ce5b94844b868233360d732d85c4`；状态 `success`。

```sql
SELECT MIN(survey_response_recorded_at) AS min_ts, MAX(survey_response_recorded_at) AS max_ts, MIN(survey_response_started_at) AS min_start, MAX(survey_response_started_at) AS max_start FROM qualtrics__response
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-080/attempt-01/sql/S10.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-080/attempt-01/sql/S10.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-080/attempt-01/results/S10.rows.jsonl)；完整：True；SHA256：`840ba47afe9f6bd2845bfee9d39274e72ae02236e5d45b3f6d78638c92a7c47e`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "qualtrics__response", "kind": "base", "block": null, "base_tables": ["qualtrics__response"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | MIN(survey_response_recorded_at) | [{"table": "qualtrics__response", "column": "survey_response_recorded_at"}] | [] | False |
| B1 | MAX(survey_response_recorded_at) | [{"table": "qualtrics__response", "column": "survey_response_recorded_at"}] | [] | False |
| B1 | MIN(survey_response_started_at) | [{"table": "qualtrics__response", "column": "survey_response_started_at"}] | [] | False |
| B1 | MAX(survey_response_started_at) | [{"table": "qualtrics__response", "column": "survey_response_started_at"}] | [] | False |


## S11

类别 `data`；来源 `query_db`；调用 `5aeb253e32e04a1e8d230c561cb80527`；状态 `success`。

```sql
SELECT contact_id, email, language, total_count_surveys, total_count_completed_surveys, avg_survey_progress_pct, avg_survey_duration_in_seconds, count_surveys_sent_email, count_surveys_sent_sms, count_surveys_opened_email, count_surveys_opened_sms, count_surveys_started_email, count_surveys_started_sms, count_surveys_completed_email, count_surveys_completed_sms FROM qualtrics__contact LIMIT 10
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-080/attempt-01/sql/S11.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-080/attempt-01/sql/S11.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-080/attempt-01/results/S11.rows.jsonl)；完整：True；SHA256：`959107acb6d63ed9e29d3664db957433157cc555018935c1798d6ca9e31a8c1e`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "qualtrics__contact", "kind": "base", "block": null, "base_tables": ["qualtrics__contact"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |


## S12

类别 `data`；来源 `query_db`；调用 `4e6f1ff7935e40d88ab693d8e17eb912`；状态 `success`。

```sql
SELECT MIN(total_count_surveys) AS min_s, MAX(total_count_surveys) AS max_s, AVG(total_count_surveys) AS avg_s, MIN(total_count_completed_surveys) AS min_c, MAX(total_count_completed_surveys) AS max_c, AVG(total_count_completed_surveys) AS avg_c FROM qualtrics__contact
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-080/attempt-01/sql/S12.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-080/attempt-01/sql/S12.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-080/attempt-01/results/S12.rows.jsonl)；完整：True；SHA256：`40e87dfdc6fb12466c1d3b005f9588b375b0ac85e24879252865108095b25558`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "qualtrics__contact", "kind": "base", "block": null, "base_tables": ["qualtrics__contact"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | MIN(total_count_surveys) | [{"table": "qualtrics__contact", "column": "total_count_surveys"}] | [] | False |
| B1 | MAX(total_count_surveys) | [{"table": "qualtrics__contact", "column": "total_count_surveys"}] | [] | False |
| B1 | AVG(total_count_surveys) | [{"table": "qualtrics__contact", "column": "total_count_surveys"}] | [] | False |
| B1 | MIN(total_count_completed_surveys) | [{"table": "qualtrics__contact", "column": "total_count_completed_surveys"}] | [] | False |
| B1 | MAX(total_count_completed_surveys) | [{"table": "qualtrics__contact", "column": "total_count_completed_surveys"}] | [] | False |
| B1 | AVG(total_count_completed_surveys) | [{"table": "qualtrics__contact", "column": "total_count_completed_surveys"}] | [] | False |


## S13

类别 `data`；来源 `query_db`；调用 `4ba7e45a9aaf439bb98ce3971f8bea7f`；状态 `success`。

```sql
SELECT DISTINCT survey_response_status, COUNT(*) AS n FROM qualtrics__response GROUP BY survey_response_status
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-080/attempt-01/sql/S13.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-080/attempt-01/sql/S13.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-080/attempt-01/results/S13.rows.jsonl)；完整：True；SHA256：`1acdaf7f5788df4c9ac84dfde2909c97a24db10695197f97a1816fc589236da0`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "qualtrics__response", "kind": "base", "block": null, "base_tables": ["qualtrics__response"]}] | [] | ["survey_response_status"] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |


## S14

类别 `data`；来源 `query_db`；调用 `02575a756d6443269a6cb7e9deb788dd`；状态 `success`。

```sql
SELECT COUNT(*) AS contacts_with_email FROM qualtrics__contact WHERE email IS NOT NULL
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-080/attempt-01/sql/S14.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-080/attempt-01/sql/S14.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-080/attempt-01/results/S14.rows.jsonl)；完整：True；SHA256：`d093e3367a29f8b5872b0a40238b39e2ec283fd7fa1bdad2c364b5ec2b029e54`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "qualtrics__contact", "kind": "base", "block": null, "base_tables": ["qualtrics__contact"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |


## S15

类别 `data`；来源 `query_db`；调用 `cfaa720554644cd882ea322313f97ef0`；状态 `success`。

```sql
SELECT COUNT(DISTINCT r.recipient_email) AS resp_emails_in_contacts
FROM qualtrics__response r
JOIN qualtrics__contact c ON c.email = r.recipient_email
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-080/attempt-01/sql/S15.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-080/attempt-01/sql/S15.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-080/attempt-01/results/S15.rows.jsonl)；完整：True；SHA256：`53ae1f42ebaf02c839998707b38972d9ed660057ef5c1b8a5266832a3cf841ff`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "r", "kind": "base", "block": null, "base_tables": ["qualtrics__response"]}, {"alias": "c", "kind": "base", "block": null, "base_tables": ["qualtrics__contact"]}] | [{"type": "INNER", "right": "qualtrics__contact AS c", "on": "c.email = r.recipient_email", "using": []}] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(DISTINCT r.recipient_email) | [{"table": "qualtrics__response", "column": "recipient_email"}] | [] | False |


## S16

类别 `data`；来源 `query_db`；调用 `b08743532b424f998470bfadacc0ea0a`；状态 `success`。

```sql
SELECT COUNT(DISTINCT recipient_email) AS n_resp_emails, COUNT(DISTINCT survey_response_id) AS n_survey_resp
FROM qualtrics__response
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-080/attempt-01/sql/S16.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-080/attempt-01/sql/S16.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-080/attempt-01/results/S16.rows.jsonl)；完整：True；SHA256：`25bdd3c94979783f0988f9d67485af804ffd71a07ec02fce8eba388b3397df4a`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "qualtrics__response", "kind": "base", "block": null, "base_tables": ["qualtrics__response"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(DISTINCT recipient_email) | [{"table": "qualtrics__response", "column": "recipient_email"}] | [] | False |
| B1 | COUNT(DISTINCT survey_response_id) | [{"table": "qualtrics__response", "column": "survey_response_id"}] | [] | False |


## S17

类别 `data`；来源 `query_db`；调用 `76d549df6e714180abe1b2a1d29f7407`；状态 `success`。

```sql
SELECT 
  SUM(CASE WHEN location_latitude IS NOT NULL THEN 1 ELSE 0 END) AS with_lat,
  SUM(CASE WHEN ip_address IS NOT NULL THEN 1 ELSE 0 END) AS with_ip,
  SUM(CASE WHEN recipient_email IS NOT NULL THEN 1 ELSE 0 END) AS with_email,
  COUNT(*) AS total
FROM qualtrics__response
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-080/attempt-01/sql/S17.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-080/attempt-01/sql/S17.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-080/attempt-01/results/S17.rows.jsonl)；完整：True；SHA256：`443035e685c359a834fc7273c091e8f1726b179a85f1b8c5f3fc27f763eecf6f`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "qualtrics__response", "kind": "base", "block": null, "base_tables": ["qualtrics__response"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | SUM(CASE WHEN NOT location_latitude IS NULL THEN 1 ELSE 0 END) | [] | [{"table": "qualtrics__response", "column": "location_latitude"}] | False |
| B1 | SUM(CASE WHEN NOT ip_address IS NULL THEN 1 ELSE 0 END) | [] | [{"table": "qualtrics__response", "column": "ip_address"}] | False |
| B1 | SUM(CASE WHEN NOT recipient_email IS NULL THEN 1 ELSE 0 END) | [] | [{"table": "qualtrics__response", "column": "recipient_email"}] | False |
| B1 | COUNT(*) | [] | [] | True |


## S18

类别 `data`；来源 `query_db`；调用 `3cc993839d6b4cf481235b7fdae1a7d8`；状态 `success`。

```sql
SELECT email_domain, COUNT(DISTINCT recipient_email) AS n_users, COUNT(*) AS n_rows FROM qualtrics__response GROUP BY email_domain ORDER BY n_users DESC LIMIT 20
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-080/attempt-01/sql/S18.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-080/attempt-01/sql/S18.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-080/attempt-01/results/S18.rows.jsonl)；完整：True；SHA256：`88b02bd0a3b296aa43621c43c3611bbe30ecc106399950e33055e3803cf1b418`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "qualtrics__response", "kind": "base", "block": null, "base_tables": ["qualtrics__response"]}] | [] | ["email_domain"] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(DISTINCT recipient_email) | [{"table": "qualtrics__response", "column": "recipient_email"}] | [] | False |
| B1 | COUNT(*) | [] | [] | True |


## S19

类别 `data`；来源 `query_db`；调用 `1d9d470458ed462e80e944e28bb965b1`；状态 `success`。

```sql
SELECT ip_address, COUNT(DISTINCT recipient_email) AS n_users, COUNT(*) AS n_rows FROM qualtrics__response GROUP BY ip_address ORDER BY n_users DESC LIMIT 20
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-080/attempt-01/sql/S19.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-080/attempt-01/sql/S19.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-080/attempt-01/results/S19.rows.jsonl)；完整：True；SHA256：`0e7e28e554444322b416a492d859f568333a2eecf1ad9be5ef501ade8f4c6688`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "qualtrics__response", "kind": "base", "block": null, "base_tables": ["qualtrics__response"]}] | [] | ["ip_address"] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(DISTINCT recipient_email) | [{"table": "qualtrics__response", "column": "recipient_email"}] | [] | False |
| B1 | COUNT(*) | [] | [] | True |


## S20

类别 `data`；来源 `query_db`；调用 `816a613602a84b5399a5b6df4dab7332`；状态 `success`。

```sql
SELECT survey_response_id, recipient_email, distribution_channel, survey_progress, duration_in_seconds, is_finished_with_survey, survey_response_status, user_language, location_latitude, location_longitude
FROM qualtrics__response
WHERE recipient_email='melissawilliams@example.com'
LIMIT 20
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-080/attempt-01/sql/S20.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-080/attempt-01/sql/S20.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-080/attempt-01/results/S20.rows.jsonl)；完整：True；SHA256：`c2db19c6e75499eba7b3d255d7a0c99c96504b4889df4a67a05551db3a43f478`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "qualtrics__response", "kind": "base", "block": null, "base_tables": ["qualtrics__response"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |


## S21

类别 `data`；来源 `query_db`；调用 `2c8cddbd302844b2915a6619ccebeb05`；状态 `success`。

```sql
SELECT MIN(survey_progress) AS min_p, MAX(survey_progress) AS max_p, AVG(survey_progress) AS avg_p,
MIN(duration_in_seconds) AS min_d, MAX(duration_in_seconds) AS max_d, AVG(duration_in_seconds) AS avg_d
FROM qualtrics__response
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-080/attempt-01/sql/S21.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-080/attempt-01/sql/S21.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-080/attempt-01/results/S21.rows.jsonl)；完整：True；SHA256：`4409038cd0f7650254691f516ac4a2028426eab816d321ae5522c119b5f2adb1`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "qualtrics__response", "kind": "base", "block": null, "base_tables": ["qualtrics__response"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | MIN(survey_progress) | [{"table": "qualtrics__response", "column": "survey_progress"}] | [] | False |
| B1 | MAX(survey_progress) | [{"table": "qualtrics__response", "column": "survey_progress"}] | [] | False |
| B1 | AVG(survey_progress) | [{"table": "qualtrics__response", "column": "survey_progress"}] | [] | False |
| B1 | MIN(duration_in_seconds) | [{"table": "qualtrics__response", "column": "duration_in_seconds"}] | [] | False |
| B1 | MAX(duration_in_seconds) | [{"table": "qualtrics__response", "column": "duration_in_seconds"}] | [] | False |
| B1 | AVG(duration_in_seconds) | [{"table": "qualtrics__response", "column": "duration_in_seconds"}] | [] | False |


## S22

类别 `data`；来源 `query_db`；调用 `26c6ebda162f4030b205dd754aa6daa9`；状态 `success`。

```sql
SELECT is_finished_with_survey, COUNT(DISTINCT survey_response_id) AS n FROM qualtrics__response GROUP BY is_finished_with_survey
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-080/attempt-01/sql/S22.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-080/attempt-01/sql/S22.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-080/attempt-01/results/S22.rows.jsonl)；完整：True；SHA256：`b38d2cd908e92106de4535ed9340b26175d3d2e9d0ebbe56b2dc5074a70b38db`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "qualtrics__response", "kind": "base", "block": null, "base_tables": ["qualtrics__response"]}] | [] | ["is_finished_with_survey"] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(DISTINCT survey_response_id) | [{"table": "qualtrics__response", "column": "survey_response_id"}] | [] | False |


## S23

类别 `data`；来源 `query_db`；调用 `95230e86ffb84a37ab486e0301733dea`；状态 `success`。

```sql
SELECT n_channels_in_resp, COUNT(*) AS n_survey_responses
FROM (
  SELECT survey_response_id, COUNT(DISTINCT distribution_channel) AS n_channels_in_resp
  FROM qualtrics__response
  GROUP BY survey_response_id
) t
GROUP BY n_channels_in_resp
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-080/attempt-01/sql/S23.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-080/attempt-01/sql/S23.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-080/attempt-01/results/S23.rows.jsonl)；完整：True；SHA256：`1e99aa9f7ac36bf2c28f2e7d7fac38f49a85e4a6765b6abd1e853fa9ce4c8f69`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "qualtrics__response", "kind": "base", "block": null, "base_tables": ["qualtrics__response"]}] | [] | ["survey_response_id"] |
| B2 | [{"alias": "t", "kind": "derived", "block": "B1", "base_tables": ["qualtrics__response"]}] | [] | ["n_channels_in_resp"] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(DISTINCT distribution_channel) | [{"table": "qualtrics__response", "column": "distribution_channel"}] | [] | False |
| B2 | COUNT(*) | [] | [] | True |


## S24

类别 `data`；来源 `query_db`；调用 `6275dd30653742d28888158a1641f394`；状态 `success`。

```sql
SELECT n_langs_in_resp, COUNT(*) AS n_users
FROM (
  SELECT recipient_email, COUNT(DISTINCT user_language) AS n_langs_in_resp
  FROM qualtrics__response
  GROUP BY recipient_email
) t
GROUP BY n_langs_in_resp
ORDER BY n_langs_in_resp
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-080/attempt-01/sql/S24.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-080/attempt-01/sql/S24.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-080/attempt-01/results/S24.rows.jsonl)；完整：True；SHA256：`d65645a163b33ac3487a4963dd2ef7ec42127c5b3756af4160aa275852ffce75`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "qualtrics__response", "kind": "base", "block": null, "base_tables": ["qualtrics__response"]}] | [] | ["recipient_email"] |
| B2 | [{"alias": "t", "kind": "derived", "block": "B1", "base_tables": ["qualtrics__response"]}] | [] | ["n_langs_in_resp"] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(DISTINCT user_language) | [{"table": "qualtrics__response", "column": "user_language"}] | [] | False |
| B2 | COUNT(*) | [] | [] | True |


## S25

类别 `data`；来源 `query_db`；调用 `186ca06ef86145f39880b787ac81d729`；状态 `success`。

```sql
SELECT 
  SUM(CASE WHEN is_finished_with_survey=1 AND survey_response_status=1 THEN 1 ELSE 0 END) AS both_1,
  SUM(CASE WHEN is_finished_with_survey=0 AND survey_response_status=0 THEN 1 ELSE 0 END) AS both_0,
  SUM(CASE WHEN is_finished_with_survey=0 AND survey_response_status=1 THEN 1 ELSE 0 END) AS f0_s1,
  SUM(CASE WHEN is_finished_with_survey=1 AND survey_response_status=0 THEN 1 ELSE 0 END) AS f1_s0
FROM qualtrics__response
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-080/attempt-01/sql/S25.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-080/attempt-01/sql/S25.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-080/attempt-01/results/S25.rows.jsonl)；完整：True；SHA256：`eb6d4c448910df5bc3eb7060ffba55bddfe9d323c3436c6ef38701c0b55b8d5a`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "qualtrics__response", "kind": "base", "block": null, "base_tables": ["qualtrics__response"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | SUM(CASE WHEN is_finished_with_survey = 1 AND survey_response_status = 1 THEN 1 ELSE 0 END) | [] | [{"table": "qualtrics__response", "column": "is_finished_with_survey"}, {"table": "qualtrics__response", "column": "survey_response_status"}] | False |
| B1 | SUM(CASE WHEN is_finished_with_survey = 0 AND survey_response_status = 0 THEN 1 ELSE 0 END) | [] | [{"table": "qualtrics__response", "column": "is_finished_with_survey"}, {"table": "qualtrics__response", "column": "survey_response_status"}] | False |
| B1 | SUM(CASE WHEN is_finished_with_survey = 0 AND survey_response_status = 1 THEN 1 ELSE 0 END) | [] | [{"table": "qualtrics__response", "column": "is_finished_with_survey"}, {"table": "qualtrics__response", "column": "survey_response_status"}] | False |
| B1 | SUM(CASE WHEN is_finished_with_survey = 1 AND survey_response_status = 0 THEN 1 ELSE 0 END) | [] | [{"table": "qualtrics__response", "column": "is_finished_with_survey"}, {"table": "qualtrics__response", "column": "survey_response_status"}] | False |


## S26

类别 `data`；来源 `query_db`；调用 `eae3aa1d56834aa6af31134cae3bde27`；状态 `success`。

```sql
SELECT 
  ROUND(location_latitude/10)*10 AS lat_bin,
  ROUND(location_longitude/20)*20 AS lon_bin,
  COUNT(*) AS n_rows
FROM qualtrics__response
GROUP BY lat_bin, lon_bin
ORDER BY n_rows DESC
LIMIT 30
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-080/attempt-01/sql/S26.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-080/attempt-01/sql/S26.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-080/attempt-01/results/S26.rows.jsonl)；完整：True；SHA256：`daa7693a6cff12a87ba863aca431b7c42d4c8106fa91e6d6dcaf2ff8d3dbe25d`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "qualtrics__response", "kind": "base", "block": null, "base_tables": ["qualtrics__response"]}] | [] | ["ROUND(location_latitude / 10) * 10", "ROUND(location_longitude / 20) * 20"] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |


## S27

类别 `data`；来源 `query_db`；调用 `a5ff1e8d6083465ea5b29da19148bca6`；状态 `success`。

```sql
SELECT
  CASE WHEN location_latitude > 0 AND location_longitude < -30 THEN 'AMERICAS'
       WHEN location_latitude <= 0 AND location_longitude < -30 THEN 'AMERICAS'
       WHEN location_latitude > 35 AND location_longitude >= -30 AND location_longitude < 60 THEN 'EUROPE'
       WHEN location_latitude <= 35 AND location_longitude >= -30 AND location_longitude < 60 THEN 'AFRICA/MIDEAST'
       WHEN location_longitude >= 60 AND location_longitude < 180 THEN 'ASIA/OCEANIA'
       ELSE 'OTHER' END AS rough_region,
  COUNT(*) AS n
FROM qualtrics__response
GROUP BY rough_region
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-080/attempt-01/sql/S27.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-080/attempt-01/sql/S27.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-080/attempt-01/results/S27.rows.jsonl)；完整：True；SHA256：`625c74592d8802e9f496105410e8b45e2771ee2c7b3cb69f03e8f3f66ba1a7c2`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "qualtrics__response", "kind": "base", "block": null, "base_tables": ["qualtrics__response"]}] | [] | ["CASE WHEN location_latitude > 0 AND location_longitude < -30 THEN 'AMERICAS' WHEN location_latitude <= 0 AND location_longitude < -30 THEN 'AMERICAS' WHEN location_latitude > 35 AND location_longitude >= -30 AND location_longitude < 60 THEN 'EUROPE' WHEN location_latitude <= 35 AND location_longitude >= -30 AND location_longitude < 60 THEN 'AFRICA/MIDEAST' WHEN location_longitude >= 60 AND location_longitude < 180 THEN 'ASIA/OCEANIA' ELSE 'OTHER' END"] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |


## S28

类别 `data`；来源 `query_db`；调用 `c80146e257814265b932993338302b65`；状态 `success`。

```sql
WITH lang_mode AS (
  SELECT recipient_email, user_language AS dom_lang
  FROM (
    SELECT recipient_email, user_language,
           ROW_NUMBER() OVER (PARTITION BY recipient_email ORDER BY COUNT(*) DESC) AS rn
    FROM qualtrics__response
    GROUP BY recipient_email, user_language
  )
  WHERE rn = 1
),
user_agg AS (
  SELECT
    recipient_email AS email,
    COUNT(DISTINCT survey_response_id) AS n_survey_responses,
    COUNT(DISTINCT survey_id) AS n_distinct_surveys,
    COUNT(DISTINCT CASE WHEN is_finished_with_survey=1 THEN survey_response_id END) AS n_completed,
    COUNT(DISTINCT distribution_channel) AS n_channels,
    COUNT(DISTINCT date(survey_response_recorded_at)) AS n_active_days,
    AVG(survey_progress) AS avg_progress,
    AVG(duration_in_seconds) AS avg_duration,
    AVG(location_latitude) AS avg_lat,
    AVG(location_longitude) AS avg_lon,
    MIN(survey_response_recorded_at) AS first_response_at,
    MAX(survey_response_recorded_at) AS last_response_at
  FROM qualtrics__response
  GROUP BY recipient_email
)
SELECT u.*, l.dom_lang,
  1.0*u.n_completed/u.n_survey_responses AS completion_rate,
  (julianday(u.last_response_at) - julianday(u.first_response_at))/30.44 AS active_months
FROM user_agg u
LEFT JOIN lang_mode l ON l.recipient_email = u.email
ORDER BY u.n_survey_responses DESC
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-080/attempt-01/sql/S28.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-080/attempt-01/sql/S28.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-080/attempt-01/results/S28.rows.jsonl)；完整：True；SHA256：`80fd775f2b2011931f9a3930b854449cbc92822eab4840bd3db6f705ed1fdf3e`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "qualtrics__response", "kind": "base", "block": null, "base_tables": ["qualtrics__response"]}] | [] | ["recipient_email", "user_language"] |
| B2 | [{"alias": "", "kind": "derived", "block": "B1", "base_tables": ["qualtrics__response"]}] | [] | [] |
| B3 | [{"alias": "qualtrics__response", "kind": "base", "block": null, "base_tables": ["qualtrics__response"]}] | [] | ["recipient_email"] |
| B4 | [{"alias": "u", "kind": "derived", "block": "B3", "base_tables": ["qualtrics__response"]}, {"alias": "l", "kind": "derived", "block": "B2", "base_tables": ["qualtrics__response"]}] | [{"type": "LEFT", "right": "lang_mode AS l", "on": "l.recipient_email = u.email", "using": []}] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |
| B3 | COUNT(DISTINCT survey_response_id) | [{"table": "qualtrics__response", "column": "survey_response_id"}] | [] | False |
| B3 | COUNT(DISTINCT survey_id) | [{"table": "qualtrics__response", "column": "survey_id"}] | [] | False |
| B3 | COUNT(DISTINCT CASE WHEN is_finished_with_survey = 1 THEN survey_response_id END) | [{"table": "qualtrics__response", "column": "survey_response_id"}] | [{"table": "qualtrics__response", "column": "is_finished_with_survey"}] | False |
| B3 | COUNT(DISTINCT distribution_channel) | [{"table": "qualtrics__response", "column": "distribution_channel"}] | [] | False |
| B3 | COUNT(DISTINCT DATE(survey_response_recorded_at)) | [{"table": "qualtrics__response", "column": "survey_response_recorded_at"}] | [] | False |
| B3 | AVG(survey_progress) | [{"table": "qualtrics__response", "column": "survey_progress"}] | [] | False |
| B3 | AVG(duration_in_seconds) | [{"table": "qualtrics__response", "column": "duration_in_seconds"}] | [] | False |
| B3 | AVG(location_latitude) | [{"table": "qualtrics__response", "column": "location_latitude"}] | [] | False |
| B3 | AVG(location_longitude) | [{"table": "qualtrics__response", "column": "location_longitude"}] | [] | False |
| B3 | MIN(survey_response_recorded_at) | [{"table": "qualtrics__response", "column": "survey_response_recorded_at"}] | [] | False |
| B3 | MAX(survey_response_recorded_at) | [{"table": "qualtrics__response", "column": "survey_response_recorded_at"}] | [] | False |


## S29

类别 `data`；来源 `query_db`；调用 `226650f098b448a8a9f725b5ada5260c`；状态 `success`。

```sql
SELECT 
  n_survey_responses,
  COUNT(*) AS n_users,
  ROUND(100.0 * COUNT(*) / SUM(COUNT(*)) OVER (), 1) AS pct
FROM (
  SELECT recipient_email, COUNT(DISTINCT survey_response_id) AS n_survey_responses
  FROM qualtrics__response
  GROUP BY recipient_email
) t
GROUP BY n_survey_responses
ORDER BY n_survey_responses
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-080/attempt-01/sql/S29.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-080/attempt-01/sql/S29.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-080/attempt-01/results/S29.rows.jsonl)；完整：True；SHA256：`c6b43610bfc757f479bea28cb0e32560286c7241c97f630c42c9a3b964415318`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "qualtrics__response", "kind": "base", "block": null, "base_tables": ["qualtrics__response"]}] | [] | ["recipient_email"] |
| B2 | [{"alias": "t", "kind": "derived", "block": "B1", "base_tables": ["qualtrics__response"]}] | [] | ["n_survey_responses"] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(DISTINCT survey_response_id) | [{"table": "qualtrics__response", "column": "survey_response_id"}] | [] | False |
| B2 | COUNT(*) | [] | [] | True |
| B2 | COUNT(*) | [] | [] | True |
| B2 | COUNT(*) | [] | [] | True |


## S30

类别 `data`；来源 `query_db`；调用 `d371972b9b2941369cf08cd2d02d6516`；状态 `success`。

```sql
SELECT 
  MIN(n_survey_responses) AS min_n,
  MAX(n_survey_responses) AS max_n,
  AVG(n_survey_responses) AS avg_n,
  MIN(n_completed) AS min_c,
  MAX(n_completed) AS max_c,
  AVG(n_completed) AS avg_c,
  MIN(completion_rate) AS min_cr,
  MAX(completion_rate) AS max_cr,
  AVG(completion_rate) AS avg_cr,
  MIN(n_channels) AS min_ch,
  MAX(n_channels) AS max_ch,
  AVG(n_channels) AS avg_ch,
  MIN(avg_progress) AS min_p,
  MAX(avg_progress) AS max_p,
  AVG(avg_progress) AS avg_p
FROM (
  WITH lang_mode AS (
    SELECT recipient_email, user_language AS dom_lang
    FROM (
      SELECT recipient_email, user_language,
             ROW_NUMBER() OVER (PARTITION BY recipient_email ORDER BY COUNT(*) DESC) AS rn
      FROM qualtrics__response
      GROUP BY recipient_email, user_language
    )
    WHERE rn = 1
  ),
  user_agg AS (
    SELECT
      recipient_email AS email,
      COUNT(DISTINCT survey_response_id) AS n_survey_responses,
      COUNT(DISTINCT CASE WHEN is_finished_with_survey=1 THEN survey_response_id END) AS n_completed,
      COUNT(DISTINCT distribution_channel) AS n_channels,
      AVG(survey_progress) AS avg_progress
    FROM qualtrics__response
    GROUP BY recipient_email
  )
  SELECT u.*, 1.0*u.n_completed/u.n_survey_responses AS completion_rate
  FROM user_agg u
)
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-080/attempt-01/sql/S30.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-080/attempt-01/sql/S30.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-080/attempt-01/results/S30.rows.jsonl)；完整：True；SHA256：`95925f18b3c6e6ebcf23bc5f22033c13146b73f85833fae793c3275c97fc9ee3`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "qualtrics__response", "kind": "base", "block": null, "base_tables": ["qualtrics__response"]}] | [] | ["recipient_email", "user_language"] |
| B2 | [{"alias": "", "kind": "derived", "block": "B1", "base_tables": ["qualtrics__response"]}] | [] | [] |
| B3 | [{"alias": "qualtrics__response", "kind": "base", "block": null, "base_tables": ["qualtrics__response"]}] | [] | ["recipient_email"] |
| B4 | [{"alias": "u", "kind": "derived", "block": "B3", "base_tables": ["qualtrics__response"]}] | [] | [] |
| B5 | [{"alias": "", "kind": "derived", "block": "B4", "base_tables": ["qualtrics__response"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |
| B3 | COUNT(DISTINCT survey_response_id) | [{"table": "qualtrics__response", "column": "survey_response_id"}] | [] | False |
| B3 | COUNT(DISTINCT CASE WHEN is_finished_with_survey = 1 THEN survey_response_id END) | [{"table": "qualtrics__response", "column": "survey_response_id"}] | [{"table": "qualtrics__response", "column": "is_finished_with_survey"}] | False |
| B3 | COUNT(DISTINCT distribution_channel) | [{"table": "qualtrics__response", "column": "distribution_channel"}] | [] | False |
| B3 | AVG(survey_progress) | [{"table": "qualtrics__response", "column": "survey_progress"}] | [] | False |
| B5 | MIN(n_survey_responses) | [{"table": "qualtrics__response", "column": "survey_response_id"}] | [] | False |
| B5 | MAX(n_survey_responses) | [{"table": "qualtrics__response", "column": "survey_response_id"}] | [] | False |
| B5 | AVG(n_survey_responses) | [{"table": "qualtrics__response", "column": "survey_response_id"}] | [] | False |
| B5 | MIN(n_completed) | [{"table": "qualtrics__response", "column": "survey_response_id"}, {"table": "qualtrics__response", "column": "is_finished_with_survey"}] | [] | False |
| B5 | MAX(n_completed) | [{"table": "qualtrics__response", "column": "survey_response_id"}, {"table": "qualtrics__response", "column": "is_finished_with_survey"}] | [] | False |
| B5 | AVG(n_completed) | [{"table": "qualtrics__response", "column": "survey_response_id"}, {"table": "qualtrics__response", "column": "is_finished_with_survey"}] | [] | False |
| B5 | MIN(completion_rate) | [{"table": "qualtrics__response", "column": "survey_response_id"}, {"table": "qualtrics__response", "column": "survey_response_id"}, {"table": "qualtrics__response", "column": "is_finished_with_survey"}] | [] | False |
| B5 | MAX(completion_rate) | [{"table": "qualtrics__response", "column": "survey_response_id"}, {"table": "qualtrics__response", "column": "survey_response_id"}, {"table": "qualtrics__response", "column": "is_finished_with_survey"}] | [] | False |
| B5 | AVG(completion_rate) | [{"table": "qualtrics__response", "column": "survey_response_id"}, {"table": "qualtrics__response", "column": "survey_response_id"}, {"table": "qualtrics__response", "column": "is_finished_with_survey"}] | [] | False |
| B5 | MIN(n_channels) | [{"table": "qualtrics__response", "column": "distribution_channel"}] | [] | False |
| B5 | MAX(n_channels) | [{"table": "qualtrics__response", "column": "distribution_channel"}] | [] | False |
| B5 | AVG(n_channels) | [{"table": "qualtrics__response", "column": "distribution_channel"}] | [] | False |
| B5 | MIN(avg_progress) | [{"table": "qualtrics__response", "column": "survey_progress"}] | [] | False |
| B5 | MAX(avg_progress) | [{"table": "qualtrics__response", "column": "survey_progress"}] | [] | False |
| B5 | AVG(avg_progress) | [{"table": "qualtrics__response", "column": "survey_progress"}] | [] | False |


## S31

类别 `data`；来源 `python`；调用 `0b8eaee2e528439f9333096c39304331`；状态 `success`。

```sql

WITH lang_mode AS (
  SELECT recipient_email, user_language AS dom_lang
  FROM (
    SELECT recipient_email, user_language,
           ROW_NUMBER() OVER (PARTITION BY recipient_email ORDER BY COUNT(*) DESC) AS rn
    FROM qualtrics__response
    GROUP BY recipient_email, user_language
  )
  WHERE rn = 1
),
user_agg AS (
  SELECT
    recipient_email AS email,
    COUNT(DISTINCT survey_response_id) AS n_survey_responses,
    COUNT(DISTINCT survey_id) AS n_distinct_surveys,
    COUNT(DISTINCT CASE WHEN is_finished_with_survey=1 THEN survey_response_id END) AS n_completed,
    COUNT(DISTINCT distribution_channel) AS n_channels,
    COUNT(DISTINCT date(survey_response_recorded_at)) AS n_active_days,
    AVG(survey_progress) AS avg_progress,
    AVG(duration_in_seconds) AS avg_duration,
    AVG(location_latitude) AS avg_lat,
    AVG(location_longitude) AS avg_lon,
    MIN(survey_response_recorded_at) AS first_response_at,
    MAX(survey_response_recorded_at) AS last_response_at
  FROM qualtrics__response
  GROUP BY recipient_email
)
SELECT u.*, l.dom_lang,
  1.0*u.n_completed/u.n_survey_responses AS completion_rate,
  (julianday(u.last_response_at) - julianday(u.first_response_at))/30.44 AS active_months
FROM user_agg u
LEFT JOIN lang_mode l ON l.recipient_email = u.email
ORDER BY u.n_survey_responses DESC

```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-080/attempt-01/sql/S31.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-080/attempt-01/sql/S31.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-080/attempt-01/results/S31.rows.jsonl)；完整：True；SHA256：`80fd775f2b2011931f9a3930b854449cbc92822eab4840bd3db6f705ed1fdf3e`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "qualtrics__response", "kind": "base", "block": null, "base_tables": ["qualtrics__response"]}] | [] | ["recipient_email", "user_language"] |
| B2 | [{"alias": "", "kind": "derived", "block": "B1", "base_tables": ["qualtrics__response"]}] | [] | [] |
| B3 | [{"alias": "qualtrics__response", "kind": "base", "block": null, "base_tables": ["qualtrics__response"]}] | [] | ["recipient_email"] |
| B4 | [{"alias": "u", "kind": "derived", "block": "B3", "base_tables": ["qualtrics__response"]}, {"alias": "l", "kind": "derived", "block": "B2", "base_tables": ["qualtrics__response"]}] | [{"type": "LEFT", "right": "lang_mode AS l", "on": "l.recipient_email = u.email", "using": []}] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |
| B3 | COUNT(DISTINCT survey_response_id) | [{"table": "qualtrics__response", "column": "survey_response_id"}] | [] | False |
| B3 | COUNT(DISTINCT survey_id) | [{"table": "qualtrics__response", "column": "survey_id"}] | [] | False |
| B3 | COUNT(DISTINCT CASE WHEN is_finished_with_survey = 1 THEN survey_response_id END) | [{"table": "qualtrics__response", "column": "survey_response_id"}] | [{"table": "qualtrics__response", "column": "is_finished_with_survey"}] | False |
| B3 | COUNT(DISTINCT distribution_channel) | [{"table": "qualtrics__response", "column": "distribution_channel"}] | [] | False |
| B3 | COUNT(DISTINCT DATE(survey_response_recorded_at)) | [{"table": "qualtrics__response", "column": "survey_response_recorded_at"}] | [] | False |
| B3 | AVG(survey_progress) | [{"table": "qualtrics__response", "column": "survey_progress"}] | [] | False |
| B3 | AVG(duration_in_seconds) | [{"table": "qualtrics__response", "column": "duration_in_seconds"}] | [] | False |
| B3 | AVG(location_latitude) | [{"table": "qualtrics__response", "column": "location_latitude"}] | [] | False |
| B3 | AVG(location_longitude) | [{"table": "qualtrics__response", "column": "location_longitude"}] | [] | False |
| B3 | MIN(survey_response_recorded_at) | [{"table": "qualtrics__response", "column": "survey_response_recorded_at"}] | [] | False |
| B3 | MAX(survey_response_recorded_at) | [{"table": "qualtrics__response", "column": "survey_response_recorded_at"}] | [] | False |


## S32

类别 `data`；来源 `query_db`；调用 `18959f6b96e7428d9832f9d972f59d17`；状态 `success`。

```sql
SELECT 
  CASE WHEN total_count_surveys=1 THEN 'one' 
       WHEN total_count_surveys BETWEEN 2 AND 5 THEN '2-5'
       WHEN total_count_surveys BETWEEN 6 AND 10 THEN '6-10'
       WHEN total_count_surveys BETWEEN 11 AND 20 THEN '11-20'
       WHEN total_count_surveys > 20 THEN '21+' END AS bucket,
  COUNT(*) AS n
FROM qualtrics__contact
GROUP BY bucket ORDER BY bucket
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-080/attempt-01/sql/S32.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-080/attempt-01/sql/S32.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-080/attempt-01/results/S32.rows.jsonl)；完整：True；SHA256：`e656fdbce0399345384f012b6d98980b5c6c876f131343b5f22415f2fd9b738d`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "qualtrics__contact", "kind": "base", "block": null, "base_tables": ["qualtrics__contact"]}] | [] | ["CASE WHEN total_count_surveys = 1 THEN 'one' WHEN total_count_surveys BETWEEN 2 AND 5 THEN '2-5' WHEN total_count_surveys BETWEEN 6 AND 10 THEN '6-10' WHEN total_count_surveys BETWEEN 11 AND 20 THEN '11-20' WHEN total_count_surveys > 20 THEN '21+' END"] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |


## S33

类别 `data`；来源 `query_db`；调用 `49582397978943d6a6ae01ffb95bf418`；状态 `success`。

```sql
SELECT strftime('%Y-%m', created_at) AS month, COUNT(*) AS n
FROM qualtrics__contact
GROUP BY month ORDER BY month
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-080/attempt-01/sql/S33.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-080/attempt-01/sql/S33.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-080/attempt-01/results/S33.rows.jsonl)；完整：True；SHA256：`0cf4759f4fd8551c9d2e61763f6564e584ede75380bd7e133dc58d0bf31c603b`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "qualtrics__contact", "kind": "base", "block": null, "base_tables": ["qualtrics__contact"]}] | [] | ["STRFTIME('%Y-%m', created_at)"] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |


## S34

类别 `data`；来源 `query_db`；调用 `481c5c15e7cb489a9448fc4f500424a4`；状态 `success`。

```sql
SELECT 
  COUNT(*) AS n,
  SUM(CASE WHEN total_count_completed_surveys=0 THEN 1 ELSE 0 END) AS zero_completed,
  AVG(total_count_surveys) AS avg_sent,
  AVG(total_count_completed_surveys) AS avg_completed,
  AVG(1.0*total_count_completed_surveys/NULLIF(total_count_surveys,0)) AS avg_completion_rate,
  AVG(avg_survey_progress_pct) AS avg_progress,
  AVG(count_surveys_completed_email) AS avg_comp_email,
  AVG(count_surveys_completed_sms) AS avg_comp_sms
FROM qualtrics__contact
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-080/attempt-01/sql/S34.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-080/attempt-01/sql/S34.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-080/attempt-01/results/S34.rows.jsonl)；完整：True；SHA256：`06dcf528bd64e6f8f0be064acc7dfb62e67ef2e9850e82ff0174efd79e830558`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "qualtrics__contact", "kind": "base", "block": null, "base_tables": ["qualtrics__contact"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |
| B1 | SUM(CASE WHEN total_count_completed_surveys = 0 THEN 1 ELSE 0 END) | [] | [{"table": "qualtrics__contact", "column": "total_count_completed_surveys"}] | False |
| B1 | AVG(total_count_surveys) | [{"table": "qualtrics__contact", "column": "total_count_surveys"}] | [] | False |
| B1 | AVG(total_count_completed_surveys) | [{"table": "qualtrics__contact", "column": "total_count_completed_surveys"}] | [] | False |
| B1 | AVG(1.0 * total_count_completed_surveys / NULLIF(total_count_surveys, 0)) | [{"table": "qualtrics__contact", "column": "total_count_completed_surveys"}, {"table": "qualtrics__contact", "column": "total_count_surveys"}] | [] | False |
| B1 | AVG(avg_survey_progress_pct) | [{"table": "qualtrics__contact", "column": "avg_survey_progress_pct"}] | [] | False |
| B1 | AVG(count_surveys_completed_email) | [{"table": "qualtrics__contact", "column": "count_surveys_completed_email"}] | [] | False |
| B1 | AVG(count_surveys_completed_sms) | [{"table": "qualtrics__contact", "column": "count_surveys_completed_sms"}] | [] | False |


## S35

类别 `data`；来源 `python`；调用 `1cbd515ce00b4cd7986c0180d6209b5f`；状态 `success`。

```sql

SELECT recipient_email AS email,
       MAX(CASE WHEN distribution_channel='email' THEN 1 ELSE 0 END) AS ch_email,
       MAX(CASE WHEN distribution_channel='sms' THEN 1 ELSE 0 END) AS ch_sms,
       MAX(CASE WHEN distribution_channel='mobile' THEN 1 ELSE 0 END) AS ch_mobile,
       MAX(CASE WHEN distribution_channel='web' THEN 1 ELSE 0 END) AS ch_web,
       MAX(CASE WHEN distribution_channel='social' THEN 1 ELSE 0 END) AS ch_social,
       COUNT(DISTINCT distribution_channel) AS n_channels
FROM qualtrics__response
GROUP BY recipient_email

```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-080/attempt-01/sql/S35.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-080/attempt-01/sql/S35.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-080/attempt-01/results/S35.rows.jsonl)；完整：True；SHA256：`f01ac366d61e9d8f50987d5836e426eb5c24e40c865ebb026da47010cd1db113`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "qualtrics__response", "kind": "base", "block": null, "base_tables": ["qualtrics__response"]}] | [] | ["recipient_email"] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | MAX(CASE WHEN distribution_channel = 'email' THEN 1 ELSE 0 END) | [] | [{"table": "qualtrics__response", "column": "distribution_channel"}] | False |
| B1 | MAX(CASE WHEN distribution_channel = 'sms' THEN 1 ELSE 0 END) | [] | [{"table": "qualtrics__response", "column": "distribution_channel"}] | False |
| B1 | MAX(CASE WHEN distribution_channel = 'mobile' THEN 1 ELSE 0 END) | [] | [{"table": "qualtrics__response", "column": "distribution_channel"}] | False |
| B1 | MAX(CASE WHEN distribution_channel = 'web' THEN 1 ELSE 0 END) | [] | [{"table": "qualtrics__response", "column": "distribution_channel"}] | False |
| B1 | MAX(CASE WHEN distribution_channel = 'social' THEN 1 ELSE 0 END) | [] | [{"table": "qualtrics__response", "column": "distribution_channel"}] | False |
| B1 | COUNT(DISTINCT distribution_channel) | [{"table": "qualtrics__response", "column": "distribution_channel"}] | [] | False |


## S36

类别 `data`；来源 `python`；调用 `1cbd515ce00b4cd7986c0180d6209b5f`；状态 `success`。

```sql
SELECT cohort_month, cohort_size, avg_responses_per_user, avg_completion_rate, power_users, high_value_users, medium_value_users, low_value_users, one_time_users, cohort_health_score FROM qualtrics__user_cohort_analysis ORDER BY cohort_month
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-080/attempt-01/sql/S36.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-080/attempt-01/sql/S36.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-080/attempt-01/results/S36.rows.jsonl)；完整：True；SHA256：`f2194186817388282681f63879fe09e16a51b43921168285dc19ca9b51f1b2b9`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "qualtrics__user_cohort_analysis", "kind": "base", "block": null, "base_tables": ["qualtrics__user_cohort_analysis"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |


## S37

类别 `data`；来源 `python`；调用 `930428e2cec14795941f0b9ac31dd9cf`；状态 `success`。

```sql

SELECT recipient_email AS email,
       MAX(CASE WHEN distribution_channel='email' THEN 1 ELSE 0 END) AS ch_email,
       MAX(CASE WHEN distribution_channel='sms' THEN 1 ELSE 0 END) AS ch_sms,
       MAX(CASE WHEN distribution_channel='mobile' THEN 1 ELSE 0 END) AS ch_mobile,
       MAX(CASE WHEN distribution_channel='web' THEN 1 ELSE 0 END) AS ch_web,
       MAX(CASE WHEN distribution_channel='social' THEN 1 ELSE 0 END) AS ch_social
FROM qualtrics__response
GROUP BY recipient_email

```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-080/attempt-01/sql/S37.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-080/attempt-01/sql/S37.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-080/attempt-01/results/S37.rows.jsonl)；完整：True；SHA256：`c60fb56f4dd4c6159907a4e694968f1fab36de26f1ae307afeb9df39a718195a`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "qualtrics__response", "kind": "base", "block": null, "base_tables": ["qualtrics__response"]}] | [] | ["recipient_email"] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | MAX(CASE WHEN distribution_channel = 'email' THEN 1 ELSE 0 END) | [] | [{"table": "qualtrics__response", "column": "distribution_channel"}] | False |
| B1 | MAX(CASE WHEN distribution_channel = 'sms' THEN 1 ELSE 0 END) | [] | [{"table": "qualtrics__response", "column": "distribution_channel"}] | False |
| B1 | MAX(CASE WHEN distribution_channel = 'mobile' THEN 1 ELSE 0 END) | [] | [{"table": "qualtrics__response", "column": "distribution_channel"}] | False |
| B1 | MAX(CASE WHEN distribution_channel = 'web' THEN 1 ELSE 0 END) | [] | [{"table": "qualtrics__response", "column": "distribution_channel"}] | False |
| B1 | MAX(CASE WHEN distribution_channel = 'social' THEN 1 ELSE 0 END) | [] | [{"table": "qualtrics__response", "column": "distribution_channel"}] | False |

