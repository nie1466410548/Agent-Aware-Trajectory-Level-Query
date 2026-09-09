# dacomp-081

Capital efficiency issue for high-investment priority applications. The CFO is concerned a…

运行：已提交（截断）。官方未评分。全部 SQL 尝试/成功 122/121；数据 SQL 120/119；Python 7 次。

完整原题：

Capital efficiency issue for high-investment priority applications. The CFO is concerned about the `com.dev.photoeditor` application: a $2M research budget was invested over the past 12 months, yet the `overall_performance_score` dropped from 85 to 72. Please analyze the performance divergence of this application across different geographical regions, specifically focusing on the differences between top markets with revenue exceeding $7 and markets with revenue below $3.

| 表 | 行数 | 列数 |
| --- | --- | --- |
| qualtrics__contact | 4000 | 35 |
| qualtrics__response | 72000 | 53 |
| qualtrics__survey | 8240 | 55 |


实际路线（分析者依据 SQL/源码概括，不代表 Agent 自述）：SQL 探查可用调查数据 → Python 将调查值按语言和高低值聚合 → 代理市场分析；原题与实际分析对象存在差异。

数据库大小：35,479,552 字节。

## 数据 SQL

| SQL | 状态 | 基础表 | Join 输入/类型 | GROUP BY | 聚合表达式 | 结果行数 | 数据库 ms |
| --- | --- | --- | --- | --- | --- | --- | --- |
| [S3/Q1](#s3) | success | ["qualtrics__survey"] | 0 / {} | [] | ["COUNT(*)"] | 1 | 2.285 |
| [S4/Q2](#s4) | success | ["qualtrics__survey"] | 0 / {} | [] | [] | 8240 | 17.633 |
| [S5/Q3](#s5) | success | ["qualtrics__response"] | 0 / {} | [] | ["COUNT(*)"] | 1 | 9.025 |
| [S6/Q4](#s6) | success | ["qualtrics__contact"] | 0 / {} | [] | ["COUNT(*)"] | 1 | 0.536 |
| [S7/Q5](#s7) | success | ["qualtrics__survey"] | 0 / {} | [] | [] | 0 | 4.385 |
| [S8/Q6](#s8) | success | ["qualtrics__response"] | 0 / {} | [] | [] | 20 | 0.408 |
| [S9/Q7](#s9) | success | ["qualtrics__response"] | 0 / {} | [] | [] | 30 | 0.3 |
| [S10/Q8](#s10) | success | ["qualtrics__contact"] | 0 / {} | [] | [] | 30 | 0.389 |
| [S11/Q9](#s11) | success | ["qualtrics__response"] | 0 / {} | [] | [] | 30 | 0.4 |
| [S12/Q10](#s12) | success | ["qualtrics__survey"] | 0 / {} | [] | [] | 7 | 2.554 |
| [S13/Q11](#s13) | success | ["qualtrics__survey"] | 0 / {} | [] | [] | 4 | 2.04 |
| [S14/Q12](#s14) | success | ["qualtrics__response"] | 0 / {} | [] | [] | 25 | 0.593 |
| [S15/Q13](#s15) | success | ["qualtrics__response"] | 0 / {} | [] | [] | 9 | 25.368 |
| [S16/Q14](#s16) | success | ["qualtrics__response"] | 0 / {} | [] | ["COUNT(*)"] | 1 | 44.431 |
| [S17/Q15](#s17) | success | ["qualtrics__response"] | 0 / {} | [] | [] | 100 | 37.088 |
| [S18/Q16](#s18) | success | ["qualtrics__survey"] | 0 / {} | [] | ["COUNT(*)"] | 1 | 5.15 |
| [S19/Q17](#s19) | success | ["qualtrics__response"] | 0 / {} | [] | ["COUNT(*)"] | 1 | 29.028 |
| [S20/Q18](#s20) | success | ["qualtrics__survey"] | 0 / {} | [] | [] | 50 | 4.5 |
| [S21/Q19](#s21) | success | ["qualtrics__response"] | 0 / {} | [] | [] | 0 | 16.41 |
| [S22/Q20](#s22) | success | ["qualtrics__response"] | 0 / {} | [] | ["MIN(value)", "MAX(value)", "AVG(value)", "COUNT(*)"] | 1 | 18.933 |
| [S23/Q21](#s23) | success | ["qualtrics__response"] | 0 / {} | [] | [] | 8 | 21.81 |
| [S24/Q22](#s24) | success | ["qualtrics__survey"] | 0 / {} | [] | [] | 3 | 2.404 |
| [S25/Q23](#s25) | success | ["qualtrics__survey"] | 0 / {} | [] | [] | 50 | 0.441 |
| [S26/Q24](#s26) | success | ["qualtrics__contact"] | 0 / {} | [] | [] | 5 | 1.13 |
| [S27/Q25](#s27) | success | ["qualtrics__survey"] | 0 / {} | [] | [] | 30 | 0.473 |
| [S28/Q26](#s28) | success | ["qualtrics__response"] | 0 / {} | [] | [] | 30 | 0.373 |
| [S29/Q27](#s29) | success | ["qualtrics__response"] | 0 / {} | [] | ["COUNT(DISTINCT survey_id)"] | 1 | 41.087 |
| [S30/Q28](#s30) | success | ["qualtrics__survey"] | 0 / {} | [] | ["COUNT(DISTINCT survey_id)"] | 1 | 4.93 |
| [S31/Q29](#s31) | success | ["qualtrics__response"] | 0 / {} | [] | ["COUNT(DISTINCT question_id)"] | 1 | 51.809 |
| [S32/Q30](#s32) | success | ["qualtrics__response"] | 0 / {} | [] | ["COUNT(DISTINCT embedded_data)"] | 1 | 26.006 |
| [S33/Q31](#s33) | success | ["qualtrics__response"] | 0 / {} | [] | ["COUNT(*)", "SUM(CASE WHEN NOT embedded_data IS NULL AND embedded_data <> '' THEN 1 ELSE 0 END)"] | 1 | 18.298 |
| [S34/Q32](#s34) | success | ["qualtrics__response"] | 0 / {} | [] | ["COUNT(DISTINCT ip_address)"] | 1 | 53.456 |
| [S35/Q33](#s35) | success | ["qualtrics__response"] | 0 / {} | [] | ["COUNT(DISTINCT location_latitude)"] | 1 | 43.613 |
| [S36/Q34](#s36) | success | ["qualtrics__contact"] | 0 / {} | [] | [] | 10 | 0.485 |
| [S37/Q35](#s37) | success | ["qualtrics__contact"] | 0 / {} | [] | [] | 5 | 1.342 |
| [S38/Q36](#s38) | success | ["qualtrics__contact"] | 0 / {} | [] | [] | 10 | 1.175 |
| [S39/Q37](#s39) | success | ["qualtrics__response"] | 0 / {} | [] | [] | 10 | 21.166 |
| [S40/Q38](#s40) | success | ["qualtrics__response"] | 0 / {} | [] | [] | 11 | 20.271 |
| [S41/Q39](#s41) | success | ["qualtrics__response"] | 0 / {} | ["survey_id"] | ["COUNT(*)", "COUNT(DISTINCT survey_response_id)", "COUNT(DISTINCT question_id)", "MIN(value)", "MAX(value)", "AVG(value)"] | 15 | 93.497 |
| [S42/Q40](#s42) | success | ["qualtrics__response"] | 0 / {} | [] | [] | 50 | 12.533 |
| [S43/Q41](#s43) | success | ["qualtrics__survey"] | 0 / {} | [] | [] | 100 | 2.564 |
| [S44/Q42](#s44) | success | ["qualtrics__response"] | 0 / {} | ["survey_response_id"] | ["COUNT(*)"] | 20 | 50.424 |
| [S45/Q43](#s45) | success | ["qualtrics__response"] | 0 / {} | [] | [] | 3 | 0.477 |
| [S46/Q44](#s46) | success | ["qualtrics__response"] | 0 / {} | ["question_id"] | ["COUNT(*)", "MIN(value)", "MAX(value)", "AVG(value)", "COUNT(DISTINCT survey_id)"] | 20 | 92.325 |
| [S47/Q45](#s47) | success | ["qualtrics__response"] | 0 / {} | [] | ["COUNT(*)", "SUM(CASE WHEN NOT survey_response_recorded_at IS NULL THEN 1 ELSE 0 END)", "SUM(CASE WHEN NOT survey_response_started_at IS NULL THEN 1 ELSE 0 END)", "SUM(CASE WHEN NOT survey_finished_at IS NULL THEN 1 ELSE 0 END)"] | 1 | 21.015 |
| [S48/Q46](#s48) | success | ["qualtrics__response"] | 0 / {} | [] | [] | 0 | 13.49 |
| [S49/Q47](#s49) | success | ["qualtrics__response"] | 0 / {} | ["embedded_data"] | ["COUNT(*)"] | 30 | 25.637 |
| [S50/Q48](#s50) | success | ["qualtrics__response"] | 0 / {} | ["embedded_data"] | ["COUNT(*)"] | 30 | 25.369 |
| [S51/Q49](#s51) | success | ["qualtrics__response"] | 0 / {} | ["user_language"] | ["COUNT(*)", "AVG(value)", "MIN(value)", "MAX(value)"] | 10 | 51.047 |
| [S52/Q50](#s52) | success | ["qualtrics__response"] | 0 / {} | ["contact_language"] | ["COUNT(*)", "AVG(value)", "MIN(value)", "MAX(value)"] | 11 | 58.113 |
| [S53/Q51](#s53) | success | ["qualtrics__response", "qualtrics__survey"] | 2 / {'INNER': 1} | ["r.survey_id"] | ["COUNT(*)", "AVG(r.value)", "MIN(r.value)", "MAX(r.value)"] | 30 | 145.824 |
| [S54/Q52](#s54) | success | ["qualtrics__response", "qualtrics__survey"] | 2 / {'INNER': 1} | ["r.survey_id"] | ["COUNT(*)", "AVG(r.value)"] | 30 | 136.168 |
| [S55/Q53](#s55) | success | ["qualtrics__response", "qualtrics__survey"] | 2 / {'INNER': 1} | ["r.survey_id", "r.user_language"] | ["COUNT(*)", "AVG(r.value)"] | 50 | 112.876 |
| [S56/Q54](#s56) | success | ["qualtrics__response"] | 0 / {} | ["response_text"] | ["COUNT(*)"] | 8 | 39.771 |
| [S57/Q55](#s57) | success | ["qualtrics__response"] | 0 / {} | ["question_type"] | ["COUNT(*)"] | 9 | 37.742 |
| [S58/Q56](#s58) | success | ["qualtrics__response"] | 0 / {} | ["response_text"] | ["MIN(value)", "MAX(value)", "AVG(value)"] | 8 | 47.43 |
| [S59/Q57](#s59) | success | ["qualtrics__survey"] | 0 / {} | [] | [] | 0 | 4.708 |
| [S60/Q58](#s60) | success | ["qualtrics__survey"] | 0 / {} | [] | [] | 0 | 5.188 |
| [S61/Q59](#s61) | success | ["qualtrics__survey"] | 0 / {} | [] | [] | 4139 | 8.758 |
| [S62/Q60](#s62) | success | ["qualtrics__survey"] | 0 / {} | ["survey_name"] | ["COUNT(*)"] | 200 | 4.386 |
| [S63/Q61](#s63) | success | ["qualtrics__response"] | 0 / {} | [] | [] | 0 | 15.801 |
| [S64/Q62](#s64) | success | ["qualtrics__response"] | 0 / {} | [] | [] | 20 | 0.387 |
| [S65/Q63](#s65) | success | ["qualtrics__response"] | 0 / {} | [] | [] | 20 | 0.389 |
| [S66/Q64](#s66) | success | ["qualtrics__survey"] | 0 / {} | [] | [] | 1777 | 5.054 |
| [S67/Q65](#s67) | success | ["qualtrics__survey"] | 0 / {} | [] | [] | 6000 | 6.515 |
| [S68/Q66](#s68) | success | ["qualtrics__response"] | 0 / {} | ["r.survey_id", "r.user_language"] | ["COUNT(*)", "AVG(r.value)", "MIN(r.value)", "MAX(r.value)", "AVG(r.value)"] | 30 | 97.384 |
| [S69/Q67](#s69) | success | ["qualtrics__response"] | 0 / {} | ["r.survey_id", "r.user_language"] | ["COUNT(*)", "AVG(r.value)", "AVG(r.value)"] | 30 | 77.592 |
| [S70/Q68](#s70) | success | ["qualtrics__response"] | 0 / {} | ["r.user_language"] | ["COUNT(*)", "AVG(r.value)", "MIN(r.value)", "MAX(r.value)"] | 4 | 13.309 |
| [S71/Q69](#s71) | success | ["qualtrics__survey"] | 0 / {} | [] | [] | 1 | 2.002 |
| [S72/Q70](#s72) | success | ["qualtrics__response"] | 0 / {} | [] | ["COUNT(*)"] | 1 | 12.818 |
| [S73/Q71](#s73) | success | ["qualtrics__survey"] | 0 / {} | [] | [] | 5 | 0.538 |
| [S74/Q72](#s74) | success | ["qualtrics__response"] | 0 / {} | ["survey_id", "user_language", "survey_id"] | ["COUNT(*)", "AVG(value)", "MAX(avg_v)", "MIN(avg_v)", "SUM(n)", "COUNT(*)"] | 30 | 80.545 |
| [S75/Q73](#s75) | failed | ["qualtrics__response", "qualtrics__survey"] | 2 / {'INNER': 1} | ["r.survey_id"] | ["COUNT(*)", "AVG(r.value)", "STDDEV(r.value)", "AVG(r.value)"] | unknown | 未取得；调用总时长 0.286 ms |
| [S76/Q74](#s76) | success | ["qualtrics__response", "qualtrics__survey"] | 2 / {'INNER': 1} | ["r.survey_id"] | ["COUNT(*)", "AVG(r.value)", "AVG(r.value)"] | 40 | 122.711 |
| [S77/Q75](#s77) | success | ["qualtrics__response", "qualtrics__survey"] | 2 / {'INNER': 1} | ["r.survey_id"] | ["COUNT(*)", "AVG(r.value)", "AVG(r.value)"] | 40 | 123.461 |
| [S78/Q76](#s78) | success | ["qualtrics__response"] | 0 / {} | ["r.user_language"] | ["COUNT(*)", "AVG(r.value)", "MIN(r.value)", "MAX(r.value)"] | 1 | 16.232 |
| [S79/Q77](#s79) | success | ["qualtrics__survey"] | 0 / {} | [] | [] | 2 | 2.125 |
| [S80/Q78](#s80) | success | ["qualtrics__survey"] | 0 / {} | ["survey_id"] | ["COUNT(*)"] | 20 | 3.055 |
| [S81/Q79](#s81) | success | ["qualtrics__response"] | 0 / {} | ["user_language"] | ["COUNT(*)", "AVG(value)"] | 1 | 13.853 |
| [S82/Q80](#s82) | success | ["qualtrics__survey"] | 0 / {} | ["survey_id", "survey_name"] | ["COUNT(*)"] | 1 | 1.749 |
| [S83/Q81](#s83) | success | ["qualtrics__response"] | 0 / {} | [] | [] | 5 | 13.7 |
| [S84/Q82](#s84) | success | ["qualtrics__response"] | 0 / {} | [] | ["COUNT(*)"] | 1 | 14.009 |
| [S85/Q83](#s85) | success | ["qualtrics__response"] | 0 / {} | [] | [] | 5 | 13.916 |
| [S86/Q84](#s86) | success | ["qualtrics__survey"] | 0 / {} | [] | ["COUNT(*)", "COUNT(DISTINCT survey_id)"] | 1 | 5.132 |
| [S87/Q85](#s87) | success | ["qualtrics__survey"] | 0 / {} | ["survey_id"] | ["COUNT(*)", "COUNT(*)"] | 1 | 4.926 |
| [S88/Q86](#s88) | success | ["qualtrics__survey"] | 0 / {} | ["survey_id"] | ["COUNT(*)"] | 10 | 5.409 |
| [S89/Q87](#s89) | success | ["qualtrics__survey"] | 0 / {} | [] | [] | 22 | 5.335 |
| [S90/Q88](#s90) | success | ["qualtrics__survey"] | 0 / {} | [] | [] | 22 | 4.904 |
| [S91/Q89](#s91) | success | ["qualtrics__survey"] | 0 / {} | [] | [] | 22 | 5.046 |
| [S92/Q90](#s92) | success | ["qualtrics__response"] | 0 / {} | ["r.user_language"] | ["COUNT(*)", "AVG(r.value)", "MIN(r.value)", "MAX(r.value)"] | 6 | 13.81 |
| [S93/Q91](#s93) | success | ["qualtrics__survey"] | 0 / {} | [] | [] | 1 | 0.465 |
| [S94/Q92](#s94) | success | ["qualtrics__response"] | 0 / {} | ["question_type"] | ["COUNT(*)", "MIN(value)", "MAX(value)", "AVG(value)"] | 9 | 52.373 |
| [S95/Q93](#s95) | success | ["qualtrics__response"] | 0 / {} | ["distribution_channel"] | ["COUNT(*)"] | 5 | 34.237 |
| [S96/Q94](#s96) | success | ["qualtrics__response"] | 0 / {} | ["contact_id"] | ["COUNT(*)"] | 10 | 53.88 |
| [S97/Q95](#s97) | success | ["qualtrics__response"] | 0 / {} | [] | ["COUNT(DISTINCT contact_id)"] | 1 | 48.877 |
| [S98/Q96](#s98) | success | ["qualtrics__response"] | 0 / {} | ["question_id"] | ["COUNT(DISTINCT survey_id)", "COUNT(*)"] | 20 | 72.989 |
| [S99/Q97](#s99) | success | ["qualtrics__response"] | 0 / {} | ["question_id"] | ["COUNT(*)", "COUNT(DISTINCT survey_id)", "COUNT(DISTINCT survey_response_id)"] | 20 | 93.029 |
| [S100/Q98](#s100) | success | ["qualtrics__response"] | 0 / {} | ["question_id"] | ["COUNT(*)"] | 30 | 64.498 |
| [S101/Q99](#s101) | success | ["qualtrics__response"] | 0 / {} | ["CAST(value AS INTEGER)"] | ["COUNT(*)", "AVG(value)"] | 10 | 38.888 |
| [S102/Q100](#s102) | success | ["qualtrics__response"] | 0 / {} | ["sub_question_text"] | ["COUNT(*)", "AVG(value)"] | 30 | 76.781 |
| [S103/Q101](#s103) | success | ["qualtrics__response"] | 0 / {} | ["question_option_key"] | ["COUNT(*)", "AVG(value)"] | 30 | 76.168 |
| [S104/Q102](#s104) | success | ["qualtrics__response"] | 0 / {} | ["survey_id", "user_language"] | ["COUNT(*)", "AVG(value)", "MIN(value)", "MAX(value)"] | 12296 | 96.903 |
| [S105/Q103](#s105) | success | ["qualtrics__response"] | 0 / {} | [] | [] | 5 | 13.921 |
| [S106/Q104](#s106) | success | ["qualtrics__response"] | 0 / {} | ["survey_id", "question_type"] | ["COUNT(*)", "COUNT(*)"] | 20 | 73.369 |
| [S107/Q105](#s107) | success | ["qualtrics__response"] | 0 / {} | ["survey_response_id"] | ["COUNT(*)"] | 20 | 50.577 |
| [S108/Q106](#s108) | success | ["qualtrics__response"] | 0 / {} | ["question_text"] | ["COUNT(*)"] | 30 | 45.176 |
| [S109/Q107](#s109) | success | ["qualtrics__response"] | 0 / {} | [] | [] | 50000 | 90.072 |
| [S110/Q108](#s110) | success | ["qualtrics__response"] | 0 / {} | ["survey_id", "user_language"] | ["COUNT(*)", "AVG(value)"] | 14299 | 87.82 |
| [S111/Q109](#s111) | success | ["qualtrics__response"] | 0 / {} | [] | [] | 72000 | 127.535 |
| [S112/Q110](#s112) | success | ["qualtrics__response"] | 0 / {} | ["survey_id", "user_language"] | ["COUNT(*)", "AVG(value)"] | 14299 | 85.895 |
| [S113/Q111](#s113) | success | ["qualtrics__survey"] | 0 / {} | [] | [] | 1 | 1.057 |
| [S114/Q112](#s114) | success | ["qualtrics__response"] | 0 / {} | [] | ["AVG(value)", "COUNT(*)"] | 1 | 13.38 |
| [S115/Q113](#s115) | success | ["qualtrics__survey"] | 0 / {} | [] | [] | 1 | 1.086 |
| [S116/Q114](#s116) | success | ["qualtrics__response"] | 0 / {} | [] | ["AVG(value)", "COUNT(*)"] | 1 | 13.415 |
| [S117/Q115](#s117) | success | ["qualtrics__survey"] | 0 / {} | [] | [] | 1 | 1.505 |
| [S118/Q116](#s118) | success | ["qualtrics__response"] | 0 / {} | [] | ["AVG(value)", "COUNT(*)"] | 1 | 13.053 |
| [S119/Q117](#s119) | success | ["qualtrics__survey"] | 0 / {} | [] | [] | 1 | 0.304 |
| [S120/Q118](#s120) | success | ["qualtrics__response"] | 0 / {} | [] | ["AVG(value)", "COUNT(*)"] | 1 | 12.92 |
| [S121/Q119](#s121) | success | ["qualtrics__survey"] | 0 / {} | [] | [] | 1 | 1.141 |
| [S122/Q120](#s122) | success | ["qualtrics__response"] | 0 / {} | [] | ["AVG(value)", "COUNT(*)"] | 1 | 13.547 |


## 元数据和设置

| SQL | 类别 | 状态 | 内容 |
| --- | --- | --- | --- |
| S1 | connection_setup | success | PRAGMA query_only=ON |
| S2 | metadata | success | SELECT name,sql FROM sqlite_master WHERE type='table' ORDER BY name |


## Python 与执行位置

人工源码审查：**database_first_violation**。Python 对调查、语言及数值高低组计算均值、计数和排序，属于 SQL 可执行的聚合。原题询问应用地域收入，而这些代码使用调查值和语言作代理；仅记录实际轨迹，不据此认定回答了原题。该尝试触及 120 次数据 SQL 上限并有 4 次拒绝，应标为截断提交。 [证据](../reviews/dacomp-081.json)。

P1：Compute per-survey language performance divergence to identify surveys with the strongest pattern of some regions having high average value (>7) and others low (<3), which would match the task description of top markets vs underperforming markets. This is complex multi-step aggregation that requires sorting and filtering in Python.

[源码](../../../runs/dsv4flash-db-first-full-01/dacomp-081/attempt-01/python/P1.py)；[输出](../../../runs/dsv4flash-db-first-full-01/dacomp-081/attempt-01/python/P1.stdout)；[错误](../../../runs/dsv4flash-db-first-full-01/dacomp-081/attempt-01/python/P1.stderr)。检出需人工核验的 SQL 可实现操作：groupby(, .query(, sort_values(；不能仅凭理由判为合规。

P2：Examine the structure of responses within a single survey session to understand how questions relate to each other and identify potential revenue vs performance questions.

[源码](../../../runs/dsv4flash-db-first-full-01/dacomp-081/attempt-01/python/P2.py)；[输出](../../../runs/dsv4flash-db-first-full-01/dacomp-081/attempt-01/python/P2.stdout)；[错误](../../../runs/dsv4flash-db-first-full-01/dacomp-081/attempt-01/python/P2.stderr)。检出需人工核验的 SQL 可实现操作：.query(；不能仅凭理由判为合规。

P3：Check whether numeric columns (sub_question_text, question_option_key, value) have meaningful relationships or bimodal distributions that could encode revenue vs performance. This is correlation analysis better suited to Python.

[源码](../../../runs/dsv4flash-db-first-full-01/dacomp-081/attempt-01/python/P3.py)；[输出](../../../runs/dsv4flash-db-first-full-01/dacomp-081/attempt-01/python/P3.stdout)；[错误](../../../runs/dsv4flash-db-first-full-01/dacomp-081/attempt-01/python/P3.stderr)。检出需人工核验的 SQL 可实现操作：groupby(, .query(；不能仅凭理由判为合规。

P4：Search for the survey that best matches the task narrative: an app whose overall performance score (avg value * 10) is around 72 and which has both high-scoring (>8) and low-scoring regions. This requires aggregation and filtering in Python.

[源码](../../../runs/dsv4flash-db-first-full-01/dacomp-081/attempt-01/python/P4.py)；[输出](../../../runs/dsv4flash-db-first-full-01/dacomp-081/attempt-01/python/P4.stdout)；[错误](../../../runs/dsv4flash-db-first-full-01/dacomp-081/attempt-01/python/P4.stderr)。检出需人工核验的 SQL 可实现操作：groupby(, .query(, sort_values(；不能仅凭理由判为合规。

P5：Perform the final analysis: compute performance scores per region (language), segment markets into top (avg value > 7) and low (avg value < 3), and compare divergence. Also compute the app's overall performance score and analyze regional patterns. This requires multiple aggregation steps and statistical analysis best done in Python.

[源码](../../../runs/dsv4flash-db-first-full-01/dacomp-081/attempt-01/python/P5.py)；[输出](../../../runs/dsv4flash-db-first-full-01/dacomp-081/attempt-01/python/P5.stdout)；[错误](../../../runs/dsv4flash-db-first-full-01/dacomp-081/attempt-01/python/P5.stderr)。检出需人工核验的 SQL 可实现操作：groupby(, .query(, sort_values(；不能仅凭理由判为合规。

P6：Create detailed visualization of the most divergent survey showing regional performance divergence, and also analyze the top 5 divergent surveys more closely to identify the best candidate for the photoeditor app.

[源码](../../../runs/dsv4flash-db-first-full-01/dacomp-081/attempt-01/python/P6.py)；[输出](../../../runs/dsv4flash-db-first-full-01/dacomp-081/attempt-01/python/P6.stdout)；[错误](../../../runs/dsv4flash-db-first-full-01/dacomp-081/attempt-01/python/P6.stderr)。检出需人工核验的 SQL 可实现操作：groupby(, .query(, sort_values(；不能仅凭理由判为合规。

P7：Complete the analysis with the available survey data. Create visualizations for the performance divergence analysis.

[源码](../../../runs/dsv4flash-db-first-full-01/dacomp-081/attempt-01/python/P7.py)；[输出](../../../runs/dsv4flash-db-first-full-01/dacomp-081/attempt-01/python/P7.stdout)；[错误](../../../runs/dsv4flash-db-first-full-01/dacomp-081/attempt-01/python/P7.stderr)。检出需人工核验的 SQL 可实现操作：groupby(, .query(, sort_values(；不能仅凭理由判为合规。

## 优化机会

已验证候选。筛选限于精确 SQL、相同自包含 CTE、相同单表完整过滤、可分解单表聚合；未覆盖任意 Join 等价和一般谓词蕴含。全部候选都是 offline，未测在线预测。

| 候选 | 类型 | 已有结果 | 覆盖 SQL | 后续次数 | 中间行数 | 验证 | 成本 |
| --- | --- | --- | --- | --- | --- | --- | --- |
| C1 | exact-result reuse | True | ["S89", "S90", "S91"] | 2 | unknown | not_verified_cap | Not tested |
| C2 | exact-result reuse | True | ["S110", "S112"] | 1 | unknown | not_verified_cap | Not tested |
| C3 | exact-result reuse | True | ["S114", "S116"] | 1 | unknown | not_verified_cap | Not tested |
| C4 | aggregate MV | False | ["S3", "S62", "S88"] | 2 | unknown | not_verified_cap | Not tested |
| C5 | aggregate MV | False | ["S5", "S33", "S44", "S47", "S51", "S52", "S56", "S57", "S58", "S94", "S95", "S96", "S101", "S102", "S103", "S106", "S107", "S108"] | 17 | 72000 | verified | Warm-cache baseline 774.914 ms vs build+reuse 1133.398 ms, ratio 0.684; five repetitions, see performance evidence. |
| C6 | common filtered view | False | ["S8", "S49", "S50"] | 2 | 20480 | verified | Not benchmarked; correctness alone does not establish net speedup. |
| C7 | aggregate MV | False | ["S49", "S50"] | 1 | unknown | not_verified_cap | Not tested |
| C8 | common filtered view | False | ["S64", "S109"] | 1 | unknown | not_verified_cap | Not tested |
| C9 | common filtered view | False | ["S70", "S72"] | 1 | unknown | not_verified_cap | Not tested |
| C10 | aggregate MV | False | ["S70", "S72"] | 1 | unknown | not_verified_cap | Not tested |
| C11 | common filtered view | False | ["S78", "S81", "S83", "S84", "S85"] | 4 | 5 | verified | Not benchmarked; correctness alone does not establish net speedup. |
| C12 | aggregate MV | False | ["S78", "S81", "S84"] | 2 | unknown | not_verified_cap | Not tested |
| C13 | common filtered view | False | ["S79", "S82"] | 1 | unknown | not_verified_cap | Not tested |
| C14 | common filtered view | False | ["S113", "S115"] | 1 | unknown | not_verified_cap | Not tested |
| C15 | common filtered view | False | ["S114", "S116"] | 1 | unknown | not_verified_cap | Not tested |
| C16 | aggregate MV | False | ["S114", "S116"] | 1 | unknown | not_verified_cap | Not tested |


已验证覆盖（含触发查询、候选并集去重）：26/119 条成功数据 SQL。正确性仅针对当前数据库快照；未测性能的候选不能声称已加速。

[完整 build/rewrite 与比较证据](dacomp-081.analysis.json)。

### C5：aggregate MV

Union of grouping keys; decomposable aggregate states; AVG uses SUM and non-NULL COUNT.

原查询 [S5](#s5), [S33](#s33), [S44](#s44), [S47](#s47), [S51](#s51), [S52](#s52), [S56](#s56), [S57](#s57), [S58](#s58), [S94](#s94), [S95](#s95), [S96](#s96), [S101](#s101), [S102](#s102), [S103](#s103), [S106](#s106), [S107](#s107), [S108](#s108) → 新增共享状态 C5 → 后续 17 次可复用。该构建点为事后假设，不代表 Agent 当时预知后续。

构建定义：

```sql
SELECT survey_response_id AS __g0, user_language AS __g1, contact_language AS __g2, response_text AS __g3, question_type AS __g4, distribution_channel AS __g5, contact_id AS __g6, CAST(value AS INTEGER) AS __g7, sub_question_text AS __g8, question_option_key AS __g9, survey_id AS __g10, question_text AS __g11, COUNT(*) AS __a0, SUM(CASE WHEN NOT embedded_data IS NULL AND embedded_data <> '' THEN 1 ELSE 0 END) AS __a1, SUM(CASE WHEN NOT survey_response_recorded_at IS NULL THEN 1 ELSE 0 END) AS __a2, SUM(CASE WHEN NOT survey_response_started_at IS NULL THEN 1 ELSE 0 END) AS __a3, SUM(CASE WHEN NOT survey_finished_at IS NULL THEN 1 ELSE 0 END) AS __a4, SUM(value) AS __a5_sum, COUNT(value) AS __a5_n, MIN(value) AS __a6, MAX(value) AS __a7 FROM "qualtrics__response"  GROUP BY survey_response_id, user_language, contact_language, response_text, question_type, distribution_channel, contact_id, CAST(value AS INTEGER), sub_question_text, question_option_key, survey_id, question_text
```

受益查询 S5 的改写示例：

```sql
SELECT SUM(__a0) AS total FROM temp.reuse_candidate
```

| 原 SQL | 列名一致 | 结果一致 | 比较方法 |
| --- | --- | --- | --- |
| S5 | True | True | exact_multiset |
| S33 | True | True | exact_multiset |
| S44 | True | True | ordered_numeric_tolerance |
| S47 | True | True | exact_multiset |
| S51 | True | True | ordered_numeric_tolerance |
| S52 | True | True | ordered_numeric_tolerance |
| S56 | True | True | ordered_numeric_tolerance |
| S57 | True | True | ordered_numeric_tolerance |
| S58 | True | True | ordered_numeric_tolerance |
| S94 | True | True | ordered_numeric_tolerance |
| S95 | True | True | ordered_numeric_tolerance |
| S96 | True | True | ordered_numeric_tolerance |
| S101 | True | True | ordered_numeric_tolerance |
| S102 | True | True | ordered_numeric_tolerance |
| S103 | True | True | ordered_numeric_tolerance |
| S106 | True | True | ordered_numeric_tolerance |
| S107 | True | True | ordered_numeric_tolerance |
| S108 | True | True | ordered_numeric_tolerance |


验证状态：verified；成本结论：Warm-cache baseline 774.914 ms vs build+reuse 1133.398 ms, ratio 0.684; five repetitions, see performance evidence.

### C11：common filtered view

Same single source and complete filter; original filter retained.

原查询 [S78](#s78), [S81](#s81), [S83](#s83), [S84](#s84), [S85](#s85) → 新增共享状态 C11 → 后续 4 次可复用。该构建点为事后假设，不代表 Agent 当时预知后续。

构建定义：

```sql
SELECT * FROM "qualtrics__response" WHERE survey_id = 'SUR10001882036'
```

受益查询 S78 的改写示例：

```sql
SELECT r.user_language, COUNT(*) AS n, AVG(r.value) AS avg_v, MIN(r.value) AS min_v, MAX(r.value) AS max_v FROM temp.reuse_candidate AS r WHERE r.survey_id = 'SUR10001882036' GROUP BY r.user_language ORDER BY avg_v DESC
```

| 原 SQL | 列名一致 | 结果一致 | 比较方法 |
| --- | --- | --- | --- |
| S78 | True | True | ordered_numeric_tolerance |
| S81 | True | True | exact_multiset |
| S83 | True | True | exact_multiset |
| S84 | True | True | exact_multiset |
| S85 | True | True | exact_multiset |


验证状态：verified；成本结论：Not benchmarked; correctness alone does not establish net speedup.

### C6：common filtered view

Same single source and complete filter; original filter retained.

原查询 [S8](#s8), [S49](#s49), [S50](#s50) → 新增共享状态 C6 → 后续 2 次可复用。该构建点为事后假设，不代表 Agent 当时预知后续。

构建定义：

```sql
SELECT * FROM "qualtrics__response" WHERE NOT embedded_data IS NULL AND embedded_data <> ''
```

受益查询 S8 的改写示例：

```sql
SELECT DISTINCT embedded_data FROM temp.reuse_candidate AS qualtrics__response WHERE NOT embedded_data IS NULL AND embedded_data <> '' LIMIT 20
```

| 原 SQL | 列名一致 | 结果一致 | 比较方法 |
| --- | --- | --- | --- |
| S8 | True | True | exact_multiset |
| S49 | True | True | ordered_numeric_tolerance |
| S50 | True | True | ordered_numeric_tolerance |


验证状态：verified；成本结论：Not benchmarked; correctness alone does not establish net speedup.

[性能证据 C5](dacomp-081.C5.performance.json)：measured。

结果依赖：自动记录 SQL→Python 的接口父调用，以及源码中引用归档文件的消费者；字面值相同不认定因果。模型方向选择需要人工读取消息，尚未做全面因果标注。

[原始报告](../../../runs/dsv4flash-db-first-full-01/dacomp-081/attempt-01/answer.md)；[统一消息](../../../runs/dsv4flash-db-first-full-01/dacomp-081/attempt-01/messages.jsonl)；[原始 OpenCode 事件](../../../runs/dsv4flash-db-first-full-01/dacomp-081/attempt-01/opencode.jsonl)；[SQL 引擎日志](../../../runs/dsv4flash-db-first-full-01/dacomp-081/attempt-01/sql_journal.jsonl)。

[可读报告（本地图片链接规范化）](../answers/dacomp-081.md)。原始回答保留，分析结论未改写。

## S1

类别 `connection_setup`；来源 `connection`；调用 `723aeaa37fbb4c3f8002c8c602a3869a`；状态 `success`。

```sql
PRAGMA query_only=ON
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-081/attempt-01/sql/S1.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-081/attempt-01/sql/S1.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-081/attempt-01/results/S1.rows.jsonl)；完整：True；SHA256：`e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`。

## S2

类别 `metadata`；来源 `list_db`；调用 `723aeaa37fbb4c3f8002c8c602a3869a`；状态 `success`。

```sql
SELECT name,sql FROM sqlite_master WHERE type='table' ORDER BY name
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-081/attempt-01/sql/S2.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-081/attempt-01/sql/S2.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-081/attempt-01/results/S2.rows.jsonl)；完整：True；SHA256：`fd4919312b0d88b2ff6fc7a3750f02d42590ae3ddec7e20004df3fce00265b21`。

## S3

类别 `data`；来源 `query_db`；调用 `b514d2a68b21492790f9bb79dc711c2d`；状态 `success`。

```sql
SELECT COUNT(*) AS total FROM qualtrics__survey
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-081/attempt-01/sql/S3.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-081/attempt-01/sql/S3.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-081/attempt-01/results/S3.rows.jsonl)；完整：True；SHA256：`18cdad7d714ada0a4df655e0e388254fde78045fbd716a98df483a7e833f400b`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "qualtrics__survey", "kind": "base", "block": null, "base_tables": ["qualtrics__survey"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |


## S4

类别 `data`；来源 `query_db`；调用 `0a02dcbef0b4430b9334b990440a4846`；状态 `success`。

```sql
SELECT survey_id, survey_name, survey_status, project_category, project_type, brand_base_url, count_questions, count_survey_responses, count_completed_survey_responses FROM qualtrics__survey
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-081/attempt-01/sql/S4.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-081/attempt-01/sql/S4.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-081/attempt-01/results/S4.rows.jsonl)；完整：True；SHA256：`ad7da122aab87668fd29cbf0dd17ccc87e6643eefa5a433928bf91d5b3a43965`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "qualtrics__survey", "kind": "base", "block": null, "base_tables": ["qualtrics__survey"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |


## S5

类别 `data`；来源 `query_db`；调用 `68883cc7e2d64cb0b7b02a5b4be7887f`；状态 `success`。

```sql
SELECT COUNT(*) AS total FROM qualtrics__response
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-081/attempt-01/sql/S5.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-081/attempt-01/sql/S5.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-081/attempt-01/results/S5.rows.jsonl)；完整：True；SHA256：`cf4c32f60fb432ffe39514bdaae92447185dc7f76620587d798faa1bb47a73e0`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "qualtrics__response", "kind": "base", "block": null, "base_tables": ["qualtrics__response"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |


## S6

类别 `data`；来源 `query_db`；调用 `da625b01585f450abe97b1d042607022`；状态 `success`。

```sql
SELECT COUNT(*) AS total FROM qualtrics__contact
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-081/attempt-01/sql/S6.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-081/attempt-01/sql/S6.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-081/attempt-01/results/S6.rows.jsonl)；完整：True；SHA256：`d093e3367a29f8b5872b0a40238b39e2ec283fd7fa1bdad2c364b5ec2b029e54`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "qualtrics__contact", "kind": "base", "block": null, "base_tables": ["qualtrics__contact"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |


## S7

类别 `data`；来源 `query_db`；调用 `163e22b662ba4315a76c37db96b6d3e0`；状态 `success`。

```sql
SELECT DISTINCT survey_name, project_category, project_type, brand_base_url FROM qualtrics__survey WHERE survey_name LIKE '%photo%' OR survey_name LIKE '%editor%' OR project_category LIKE '%photo%' OR project_type LIKE '%photo%'
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-081/attempt-01/sql/S7.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-081/attempt-01/sql/S7.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-081/attempt-01/results/S7.rows.jsonl)；完整：True；SHA256：`e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "qualtrics__survey", "kind": "base", "block": null, "base_tables": ["qualtrics__survey"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |


## S8

类别 `data`；来源 `query_db`；调用 `3d92886b5c514ef9933fdbf9c7da59d8`；状态 `success`。

```sql
SELECT DISTINCT embedded_data FROM qualtrics__response WHERE embedded_data IS NOT NULL AND embedded_data != '' LIMIT 20
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-081/attempt-01/sql/S8.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-081/attempt-01/sql/S8.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-081/attempt-01/results/S8.rows.jsonl)；完整：True；SHA256：`97df89ad7eac12906cf8e14f4454ccd9b9f84186519ed8bbfa14c6b291e5fdc3`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "qualtrics__response", "kind": "base", "block": null, "base_tables": ["qualtrics__response"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |


## S9

类别 `data`；来源 `query_db`；调用 `c502b35e24594318ba6be3f22247c09d`；状态 `success`。

```sql
SELECT DISTINCT question_text, question_id FROM qualtrics__response WHERE question_text IS NOT NULL AND question_text != '' LIMIT 30
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-081/attempt-01/sql/S9.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-081/attempt-01/sql/S9.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-081/attempt-01/results/S9.rows.jsonl)；完整：True；SHA256：`34329bea2c8ebdc41a99606efe4302c2aa3ae9300960100075d352f6aa125a9d`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "qualtrics__response", "kind": "base", "block": null, "base_tables": ["qualtrics__response"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |


## S10

类别 `data`；来源 `query_db`；调用 `676f41820f834e26b8036688171a63c4`；状态 `success`。

```sql
SELECT DISTINCT external_data_reference FROM qualtrics__contact WHERE external_data_reference IS NOT NULL AND external_data_reference != '' LIMIT 30
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-081/attempt-01/sql/S10.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-081/attempt-01/sql/S10.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-081/attempt-01/results/S10.rows.jsonl)；完整：True；SHA256：`58a4a9bc081b0a058a424aca61322c8b4d07a9fb58668e66f89243dff4453459`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "qualtrics__contact", "kind": "base", "block": null, "base_tables": ["qualtrics__contact"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |


## S11

类别 `data`；来源 `query_db`；调用 `b63ce99cead040f3b7dc8d4bb64a59e4`；状态 `success`。

```sql
SELECT DISTINCT contact_external_data_reference FROM qualtrics__response WHERE contact_external_data_reference IS NOT NULL AND contact_external_data_reference != '' LIMIT 30
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-081/attempt-01/sql/S11.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-081/attempt-01/sql/S11.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-081/attempt-01/results/S11.rows.jsonl)；完整：True；SHA256：`5fb029e751743048644e0520ef653a0459cd6b6d39be5f25a5dd9ad1432f1d07`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "qualtrics__response", "kind": "base", "block": null, "base_tables": ["qualtrics__response"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |


## S12

类别 `data`；来源 `query_db`；调用 `b68246014fef4c44a37ba46628ac548f`；状态 `success`。

```sql
SELECT DISTINCT project_category FROM qualtrics__survey
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-081/attempt-01/sql/S12.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-081/attempt-01/sql/S12.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-081/attempt-01/results/S12.rows.jsonl)；完整：True；SHA256：`9bab670735103b6d3ea78b024836d83a7ef3ec58456e2e04bae7eb816499511d`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "qualtrics__survey", "kind": "base", "block": null, "base_tables": ["qualtrics__survey"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |


## S13

类别 `data`；来源 `query_db`；调用 `d2b850fa13d34eeaad7473ea000f6ce7`；状态 `success`。

```sql
SELECT DISTINCT project_type FROM qualtrics__survey
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-081/attempt-01/sql/S13.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-081/attempt-01/sql/S13.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-081/attempt-01/results/S13.rows.jsonl)；完整：True；SHA256：`7ddd2a9819d6be7c669d75eb082be613307ab39ec799dd7f953125131e8944cc`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "qualtrics__survey", "kind": "base", "block": null, "base_tables": ["qualtrics__survey"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |


## S14

类别 `data`；来源 `query_db`；调用 `35e819b715b448c08faf171b6c8657fb`；状态 `success`。

```sql
SELECT question_response_id, survey_response_id, survey_id, question_id, question_text, sub_question_key, sub_question_text, question_option_key, value, response_text, question_option_text FROM qualtrics__response LIMIT 25
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-081/attempt-01/sql/S14.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-081/attempt-01/sql/S14.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-081/attempt-01/results/S14.rows.jsonl)；完整：True；SHA256：`140c2b2b44269e4e2012369a8dbd65f4dc8bdc214b5955448f0f9cfa730b7502`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "qualtrics__response", "kind": "base", "block": null, "base_tables": ["qualtrics__response"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |


## S15

类别 `data`；来源 `query_db`；调用 `6b814b295948422c97c28ac0737a0aeb`；状态 `success`。

```sql
SELECT DISTINCT question_description, question_type FROM qualtrics__response LIMIT 30
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-081/attempt-01/sql/S15.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-081/attempt-01/sql/S15.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-081/attempt-01/results/S15.rows.jsonl)；完整：True；SHA256：`c69fa76cf19253835781629b7f91325003c603814730b96e25d87e6e98d57647`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "qualtrics__response", "kind": "base", "block": null, "base_tables": ["qualtrics__response"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |


## S16

类别 `data`；来源 `query_db`；调用 `3e7d1d6f86bd4b6da0a25ad3075a03e2`；状态 `success`。

```sql
SELECT COUNT(*) AS c FROM qualtrics__response WHERE question_text LIKE '%revenue%' OR question_text LIKE '%Revenue%' OR question_text LIKE '%performance%' OR question_text LIKE '%score%' OR question_text LIKE '%budget%' OR question_text LIKE '%app%' OR question_text LIKE '%photo%' OR question_text LIKE '%region%' OR question_text LIKE '%market%'
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-081/attempt-01/sql/S16.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-081/attempt-01/sql/S16.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-081/attempt-01/results/S16.rows.jsonl)；完整：True；SHA256：`c14196f132c1e9be0508ae80ab52fcb3e1d3fc05880415f3dc980971df207c9e`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "qualtrics__response", "kind": "base", "block": null, "base_tables": ["qualtrics__response"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |


## S17

类别 `data`；来源 `query_db`；调用 `09919ace99c14f65873d02766ac68ab9`；状态 `success`。

```sql
SELECT DISTINCT question_text FROM qualtrics__response ORDER BY question_text LIMIT 100
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-081/attempt-01/sql/S17.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-081/attempt-01/sql/S17.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-081/attempt-01/results/S17.rows.jsonl)；完整：True；SHA256：`3005dedb01faa4198da70afb69042bacb0ee926bb99044dcada73c209e8a9b42`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "qualtrics__response", "kind": "base", "block": null, "base_tables": ["qualtrics__response"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |


## S18

类别 `data`；来源 `query_db`；调用 `22474b9995fe470180ca8d3d7bc4a2a6`；状态 `success`。

```sql
SELECT COUNT(*) AS c FROM qualtrics__survey WHERE survey_name LIKE '%photo%' OR survey_name LIKE '%editor%' OR brand_base_url LIKE '%photo%' OR brand_base_url LIKE '%dev%' OR brand_id LIKE '%photo%'
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-081/attempt-01/sql/S18.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-081/attempt-01/sql/S18.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-081/attempt-01/results/S18.rows.jsonl)；完整：True；SHA256：`c14196f132c1e9be0508ae80ab52fcb3e1d3fc05880415f3dc980971df207c9e`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "qualtrics__survey", "kind": "base", "block": null, "base_tables": ["qualtrics__survey"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |


## S19

类别 `data`；来源 `query_db`；调用 `5a2eb5e89c4042d6b203167979aca5de`；状态 `success`。

```sql
SELECT COUNT(*) AS c FROM qualtrics__response WHERE embedded_data LIKE '%photo%' OR embedded_data LIKE '%dev%' OR response_text LIKE '%photo%' OR question_option_text LIKE '%photo%'
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-081/attempt-01/sql/S19.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-081/attempt-01/sql/S19.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-081/attempt-01/results/S19.rows.jsonl)；完整：True；SHA256：`c14196f132c1e9be0508ae80ab52fcb3e1d3fc05880415f3dc980971df207c9e`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "qualtrics__response", "kind": "base", "block": null, "base_tables": ["qualtrics__response"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |


## S20

类别 `data`；来源 `query_db`；调用 `85b64df3baa445e7838d2a81cf9624da`；状态 `success`。

```sql
SELECT DISTINCT survey_name FROM qualtrics__survey ORDER BY survey_name LIMIT 50
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-081/attempt-01/sql/S20.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-081/attempt-01/sql/S20.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-081/attempt-01/results/S20.rows.jsonl)；完整：True；SHA256：`f434570386630eb0cee82a23f07e48f0c6802ae049dcbed8062201f7e1048bf9`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "qualtrics__survey", "kind": "base", "block": null, "base_tables": ["qualtrics__survey"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |


## S21

类别 `data`；来源 `query_db`；调用 `37390cbd76194b57b53af9fb303abd62`；状态 `success`。

```sql
SELECT DISTINCT question_option_text FROM qualtrics__response WHERE question_option_text IS NOT NULL AND question_option_text != '' LIMIT 30
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-081/attempt-01/sql/S21.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-081/attempt-01/sql/S21.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-081/attempt-01/results/S21.rows.jsonl)；完整：True；SHA256：`e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "qualtrics__response", "kind": "base", "block": null, "base_tables": ["qualtrics__response"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |


## S22

类别 `data`；来源 `query_db`；调用 `f3945f403ae047bb9afb7484b2610812`；状态 `success`。

```sql
SELECT MIN(value), MAX(value), AVG(value), COUNT(*) FROM qualtrics__response
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-081/attempt-01/sql/S22.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-081/attempt-01/sql/S22.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-081/attempt-01/results/S22.rows.jsonl)；完整：True；SHA256：`8df6dc403ddd1eb06309b4931b012679d46a0bcbcd80627983cfb076ab18deff`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "qualtrics__response", "kind": "base", "block": null, "base_tables": ["qualtrics__response"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | MIN(value) | [{"table": "qualtrics__response", "column": "value"}] | [] | False |
| B1 | MAX(value) | [{"table": "qualtrics__response", "column": "value"}] | [] | False |
| B1 | AVG(value) | [{"table": "qualtrics__response", "column": "value"}] | [] | False |
| B1 | COUNT(*) | [] | [] | True |


## S23

类别 `data`；来源 `query_db`；调用 `009387ac2e3f45e98279c0abf1e679c5`；状态 `success`。

```sql
SELECT DISTINCT response_text FROM qualtrics__response WHERE response_text IS NOT NULL AND response_text != '' LIMIT 30
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-081/attempt-01/sql/S23.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-081/attempt-01/sql/S23.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-081/attempt-01/results/S23.rows.jsonl)；完整：True；SHA256：`6cfb409e301aeafdf7aa2ea31eec720b459993e61d72d07ac32498cfe5155883`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "qualtrics__response", "kind": "base", "block": null, "base_tables": ["qualtrics__response"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |


## S24

类别 `data`；来源 `query_db`；调用 `2043a572d2ee4521a3a7de9e2c7d740b`；状态 `success`。

```sql
SELECT DISTINCT brand_base_url FROM qualtrics__survey LIMIT 50
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-081/attempt-01/sql/S24.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-081/attempt-01/sql/S24.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-081/attempt-01/results/S24.rows.jsonl)；完整：True；SHA256：`83100d6b117eef18b37446c3c7e2b8afd1d3fa04be43e373f637f62b7b2725ea`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "qualtrics__survey", "kind": "base", "block": null, "base_tables": ["qualtrics__survey"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |


## S25

类别 `data`；来源 `query_db`；调用 `1e9b67f186174390a0321b88333576f5`；状态 `success`。

```sql
SELECT DISTINCT brand_id FROM qualtrics__survey LIMIT 50
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-081/attempt-01/sql/S25.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-081/attempt-01/sql/S25.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-081/attempt-01/results/S25.rows.jsonl)；完整：True；SHA256：`34bff78db57b9ff591076acb14fe6f28352a1d09b20c42e0ccc83c4840fa4221`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "qualtrics__survey", "kind": "base", "block": null, "base_tables": ["qualtrics__survey"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |


## S26

类别 `data`；来源 `query_db`；调用 `75633224268b44b0939b04b788b0fe99`；状态 `success`。

```sql
SELECT DISTINCT email_domain FROM qualtrics__contact LIMIT 50
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-081/attempt-01/sql/S26.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-081/attempt-01/sql/S26.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-081/attempt-01/results/S26.rows.jsonl)；完整：True；SHA256：`5529056eec418bff583d11d1a8ce252cc693536b4a134088ee22918ba74ccbb5`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "qualtrics__contact", "kind": "base", "block": null, "base_tables": ["qualtrics__contact"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |


## S27

类别 `data`；来源 `query_db`；调用 `71688d08ca1c42a7880dde4d06312d91`；状态 `success`。

```sql
SELECT survey_id, survey_name, project_category, project_type, brand_base_url, count_questions, count_survey_responses FROM qualtrics__survey WHERE survey_name LIKE '%Product%' OR survey_name LIKE '%User%' OR survey_name LIKE '%App%' OR survey_name LIKE '%Experience%' LIMIT 30
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-081/attempt-01/sql/S27.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-081/attempt-01/sql/S27.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-081/attempt-01/results/S27.rows.jsonl)；完整：True；SHA256：`3ec6d41d9fc2ab9ab32391152113875ca85c75ee9fb7e02aa013111edfabfc12`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "qualtrics__survey", "kind": "base", "block": null, "base_tables": ["qualtrics__survey"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |


## S28

类别 `data`；来源 `query_db`；调用 `01d8425be8db4559959f0b5931f10038`；状态 `success`。

```sql
SELECT DISTINCT survey_id FROM qualtrics__response LIMIT 30
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-081/attempt-01/sql/S28.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-081/attempt-01/sql/S28.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-081/attempt-01/results/S28.rows.jsonl)；完整：True；SHA256：`917092d0f2e9b501db73595b2c4266842b3ea1e46eb5320233df5e657674526f`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "qualtrics__response", "kind": "base", "block": null, "base_tables": ["qualtrics__response"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |


## S29

类别 `data`；来源 `query_db`；调用 `f86053e3ccea42a095cd3ee02b6c302f`；状态 `success`。

```sql
SELECT COUNT(DISTINCT survey_id) FROM qualtrics__response
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-081/attempt-01/sql/S29.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-081/attempt-01/sql/S29.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-081/attempt-01/results/S29.rows.jsonl)；完整：True；SHA256：`61108990661ad187e131f0e9268e6b08c2ac34c08f5b89ec8aeef350af733117`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "qualtrics__response", "kind": "base", "block": null, "base_tables": ["qualtrics__response"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(DISTINCT survey_id) | [{"table": "qualtrics__response", "column": "survey_id"}] | [] | False |


## S30

类别 `data`；来源 `query_db`；调用 `5bdd9d42debc44bd952a2294db030e1a`；状态 `success`。

```sql
SELECT COUNT(DISTINCT survey_id) FROM qualtrics__survey
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-081/attempt-01/sql/S30.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-081/attempt-01/sql/S30.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-081/attempt-01/results/S30.rows.jsonl)；完整：True；SHA256：`b2277788c7bdae0316d26e2a27143de401864da0b0c336e9bafee7e4507db2c3`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "qualtrics__survey", "kind": "base", "block": null, "base_tables": ["qualtrics__survey"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(DISTINCT survey_id) | [{"table": "qualtrics__survey", "column": "survey_id"}] | [] | False |


## S31

类别 `data`；来源 `query_db`；调用 `1fa7dd5aa13b46209fcb7224bf74e1a0`；状态 `success`。

```sql
SELECT COUNT(DISTINCT question_id) FROM qualtrics__response
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-081/attempt-01/sql/S31.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-081/attempt-01/sql/S31.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-081/attempt-01/results/S31.rows.jsonl)；完整：True；SHA256：`8f68b2bc7b420abef80671b96c74d22655a66654787e8a83118d5d318218f865`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "qualtrics__response", "kind": "base", "block": null, "base_tables": ["qualtrics__response"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(DISTINCT question_id) | [{"table": "qualtrics__response", "column": "question_id"}] | [] | False |


## S32

类别 `data`；来源 `query_db`；调用 `2f7f9935bd7a4e1eb84f0c5825c51fd8`；状态 `success`。

```sql
SELECT COUNT(DISTINCT embedded_data) AS cnt FROM qualtrics__response WHERE embedded_data IS NOT NULL
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-081/attempt-01/sql/S32.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-081/attempt-01/sql/S32.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-081/attempt-01/results/S32.rows.jsonl)；完整：True；SHA256：`a36f53d079de57022c0e2071f127ef2974187e355acf2d5523a9194d5979aab2`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "qualtrics__response", "kind": "base", "block": null, "base_tables": ["qualtrics__response"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(DISTINCT embedded_data) | [{"table": "qualtrics__response", "column": "embedded_data"}] | [] | False |


## S33

类别 `data`；来源 `query_db`；调用 `2712828d38d943f19673a76cb96c54d2`；状态 `success`。

```sql
SELECT COUNT(*) AS total, SUM(CASE WHEN embedded_data IS NOT NULL AND embedded_data != '' THEN 1 ELSE 0 END) AS has_embedded FROM qualtrics__response
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-081/attempt-01/sql/S33.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-081/attempt-01/sql/S33.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-081/attempt-01/results/S33.rows.jsonl)；完整：True；SHA256：`b385219fcd6d48e40faf0477f77bb76c5ea1778a3c6ac01d7f5126abf0e66f7f`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "qualtrics__response", "kind": "base", "block": null, "base_tables": ["qualtrics__response"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |
| B1 | SUM(CASE WHEN NOT embedded_data IS NULL AND embedded_data <> '' THEN 1 ELSE 0 END) | [] | [{"table": "qualtrics__response", "column": "embedded_data"}, {"table": "qualtrics__response", "column": "embedded_data"}] | False |


## S34

类别 `data`；来源 `query_db`；调用 `74dc45167b844f45a0136c8cad65290e`；状态 `success`。

```sql
SELECT COUNT(DISTINCT ip_address) FROM qualtrics__response
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-081/attempt-01/sql/S34.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-081/attempt-01/sql/S34.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-081/attempt-01/results/S34.rows.jsonl)；完整：True；SHA256：`4d759fdcc70a867d6bc349e6aaad648540c533c87ffecfc97d5694750d0d01cf`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "qualtrics__response", "kind": "base", "block": null, "base_tables": ["qualtrics__response"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(DISTINCT ip_address) | [{"table": "qualtrics__response", "column": "ip_address"}] | [] | False |


## S35

类别 `data`；来源 `query_db`；调用 `e8fc59e04f5f47f6842a6c616b8b6f37`；状态 `success`。

```sql
SELECT COUNT(DISTINCT location_latitude) FROM qualtrics__response WHERE location_latitude IS NOT NULL
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-081/attempt-01/sql/S35.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-081/attempt-01/sql/S35.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-081/attempt-01/results/S35.rows.jsonl)；完整：True；SHA256：`9c6d877b0b3f6297bb7a74c6057eabc81769296e74a9d8ab35cc00e59ceaf036`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "qualtrics__response", "kind": "base", "block": null, "base_tables": ["qualtrics__response"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(DISTINCT location_latitude) | [{"table": "qualtrics__response", "column": "location_latitude"}] | [] | False |


## S36

类别 `data`；来源 `query_db`；调用 `c98433760d654fd3815f6201255c8678`；状态 `success`。

```sql
SELECT * FROM qualtrics__contact LIMIT 10
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-081/attempt-01/sql/S36.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-081/attempt-01/sql/S36.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-081/attempt-01/results/S36.rows.jsonl)；完整：True；SHA256：`2526fdac9bb8429aa9d1e65c6618448f77955cc8d231874eab1fe258fbce106e`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "qualtrics__contact", "kind": "base", "block": null, "base_tables": ["qualtrics__contact"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |


## S37

类别 `data`；来源 `query_db`；调用 `1d90782465fd4e6e9c1bdd9ff04d7f89`；状态 `success`。

```sql
SELECT DISTINCT directory_name FROM qualtrics__contact
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-081/attempt-01/sql/S37.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-081/attempt-01/sql/S37.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-081/attempt-01/results/S37.rows.jsonl)；完整：True；SHA256：`1f83f3082fbe97f4d73a2478a7569c97e90484ae458f00d26baa9cc3aeeb7bb3`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "qualtrics__contact", "kind": "base", "block": null, "base_tables": ["qualtrics__contact"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |


## S38

类别 `data`；来源 `query_db`；调用 `6843800af13c4a9f865ef15c4eedce38`；状态 `success`。

```sql
SELECT DISTINCT language FROM qualtrics__contact
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-081/attempt-01/sql/S38.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-081/attempt-01/sql/S38.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-081/attempt-01/results/S38.rows.jsonl)；完整：True；SHA256：`b77787cf4bf7594f7da84afdd4fac9b1aeabce2cad164a06d69fdcb739635995`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "qualtrics__contact", "kind": "base", "block": null, "base_tables": ["qualtrics__contact"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |


## S39

类别 `data`；来源 `query_db`；调用 `0b6dc79a654449a4a7fb6dff77aa2410`；状态 `success`。

```sql
SELECT DISTINCT user_language FROM qualtrics__response
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-081/attempt-01/sql/S39.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-081/attempt-01/sql/S39.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-081/attempt-01/results/S39.rows.jsonl)；完整：True；SHA256：`df288952b427c8fa4425a50dbcbd6f2db2327e7d73d4087fcfd7fb6933f502fa`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "qualtrics__response", "kind": "base", "block": null, "base_tables": ["qualtrics__response"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |


## S40

类别 `data`；来源 `query_db`；调用 `ea97b49b570148a68ecf8ac07005365e`；状态 `success`。

```sql
SELECT DISTINCT contact_language FROM qualtrics__response
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-081/attempt-01/sql/S40.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-081/attempt-01/sql/S40.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-081/attempt-01/results/S40.rows.jsonl)；完整：True；SHA256：`5eddbe43277eed5e5bbd43294ad9191789d7b5bd9b0f9c59b9b335588467c391`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "qualtrics__response", "kind": "base", "block": null, "base_tables": ["qualtrics__response"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |


## S41

类别 `data`；来源 `query_db`；调用 `1227124b678d47f58a25d3d3e31d2111`；状态 `success`。

```sql
SELECT survey_id, COUNT(*) AS n_resp, COUNT(DISTINCT survey_response_id) AS n_survey_resp, COUNT(DISTINCT question_id) AS n_q, MIN(value) AS min_v, MAX(value) AS max_v, AVG(value) AS avg_v FROM qualtrics__response GROUP BY survey_id ORDER BY n_survey_resp DESC LIMIT 15
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-081/attempt-01/sql/S41.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-081/attempt-01/sql/S41.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-081/attempt-01/results/S41.rows.jsonl)；完整：True；SHA256：`378c6ca2ee00a39f4ea7e389773f748bb301644b403262f4a53019a628c86c47`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "qualtrics__response", "kind": "base", "block": null, "base_tables": ["qualtrics__response"]}] | [] | ["survey_id"] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |
| B1 | COUNT(DISTINCT survey_response_id) | [{"table": "qualtrics__response", "column": "survey_response_id"}] | [] | False |
| B1 | COUNT(DISTINCT question_id) | [{"table": "qualtrics__response", "column": "question_id"}] | [] | False |
| B1 | MIN(value) | [{"table": "qualtrics__response", "column": "value"}] | [] | False |
| B1 | MAX(value) | [{"table": "qualtrics__response", "column": "value"}] | [] | False |
| B1 | AVG(value) | [{"table": "qualtrics__response", "column": "value"}] | [] | False |


## S42

类别 `data`；来源 `query_db`；调用 `747ced0400c340c98f2ae7ce0c43cd09`；状态 `success`。

```sql
SELECT survey_response_id, survey_id, question_id, sub_question_key, value, response_text, user_language, location_latitude, location_longitude FROM qualtrics__response WHERE survey_id = 'SUR10000587639' LIMIT 50
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-081/attempt-01/sql/S42.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-081/attempt-01/sql/S42.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-081/attempt-01/results/S42.rows.jsonl)；完整：True；SHA256：`56340c83374c9edd73f96a1c6dc5317f0764f7c086e1223ebfef62c95e376f19`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "qualtrics__response", "kind": "base", "block": null, "base_tables": ["qualtrics__response"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |


## S43

类别 `data`；来源 `query_db`；调用 `ef95296f800e4747833e0b0e7a0284be`；状态 `success`。

```sql
SELECT survey_id, survey_name FROM qualtrics__survey ORDER BY survey_name LIMIT 100
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-081/attempt-01/sql/S43.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-081/attempt-01/sql/S43.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-081/attempt-01/results/S43.rows.jsonl)；完整：True；SHA256：`68180a30f54b891c2d8b5687d1b96ad78adf49a41d471f007f03f80dd062021d`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "qualtrics__survey", "kind": "base", "block": null, "base_tables": ["qualtrics__survey"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |


## S44

类别 `data`；来源 `query_db`；调用 `3b7d90f55e7341fe89eb5318f2dbcbc3`；状态 `success`。

```sql
SELECT survey_response_id, COUNT(*) AS n_q_per_resp FROM qualtrics__response GROUP BY survey_response_id ORDER BY n_q_per_resp DESC LIMIT 20
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-081/attempt-01/sql/S44.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-081/attempt-01/sql/S44.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-081/attempt-01/results/S44.rows.jsonl)；完整：True；SHA256：`8ad3572ed78eccc4299e1661db7bc89ffe703945a14518b2d606cb9b46fbe1e5`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "qualtrics__response", "kind": "base", "block": null, "base_tables": ["qualtrics__response"]}] | [] | ["survey_response_id"] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |


## S45

类别 `data`；来源 `query_db`；调用 `1c4a3b8f2eeb4f9aa2fe5782e7ea100c`；状态 `success`。

```sql
SELECT * FROM qualtrics__response LIMIT 3
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-081/attempt-01/sql/S45.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-081/attempt-01/sql/S45.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-081/attempt-01/results/S45.rows.jsonl)；完整：True；SHA256：`b00801e05ea32c2df7133e469a0adb2cb1aab4dbcd62054e260e381a2ec0190f`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "qualtrics__response", "kind": "base", "block": null, "base_tables": ["qualtrics__response"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |


## S46

类别 `data`；来源 `query_db`；调用 `4ada997d1d4e46d7861cd8aa591caa67`；状态 `success`。

```sql
SELECT question_id, COUNT(*) AS n, MIN(value) AS min_v, MAX(value) AS max_v, AVG(value) AS avg_v, COUNT(DISTINCT survey_id) AS n_surveys FROM qualtrics__response GROUP BY question_id ORDER BY n DESC LIMIT 20
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-081/attempt-01/sql/S46.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-081/attempt-01/sql/S46.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-081/attempt-01/results/S46.rows.jsonl)；完整：True；SHA256：`3d390574263e7863443778ee343e6c180f0722733e605a9a1f2b8d3b0caa201e`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "qualtrics__response", "kind": "base", "block": null, "base_tables": ["qualtrics__response"]}] | [] | ["question_id"] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |
| B1 | MIN(value) | [{"table": "qualtrics__response", "column": "value"}] | [] | False |
| B1 | MAX(value) | [{"table": "qualtrics__response", "column": "value"}] | [] | False |
| B1 | AVG(value) | [{"table": "qualtrics__response", "column": "value"}] | [] | False |
| B1 | COUNT(DISTINCT survey_id) | [{"table": "qualtrics__response", "column": "survey_id"}] | [] | False |


## S47

类别 `data`；来源 `query_db`；调用 `cae4874ce51e47e29d68f19369e3eee8`；状态 `success`。

```sql
SELECT COUNT(*) AS total, SUM(CASE WHEN survey_response_recorded_at IS NOT NULL THEN 1 ELSE 0 END) AS has_recorded, SUM(CASE WHEN survey_response_started_at IS NOT NULL THEN 1 ELSE 0 END) AS has_started, SUM(CASE WHEN survey_finished_at IS NOT NULL THEN 1 ELSE 0 END) AS has_finished FROM qualtrics__response
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-081/attempt-01/sql/S47.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-081/attempt-01/sql/S47.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-081/attempt-01/results/S47.rows.jsonl)；完整：True；SHA256：`d668852a82a7a0e6ae84259672c5fe3eae9c7ece0399ce19a03d0a36e3cfb5e9`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "qualtrics__response", "kind": "base", "block": null, "base_tables": ["qualtrics__response"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |
| B1 | SUM(CASE WHEN NOT survey_response_recorded_at IS NULL THEN 1 ELSE 0 END) | [] | [{"table": "qualtrics__response", "column": "survey_response_recorded_at"}] | False |
| B1 | SUM(CASE WHEN NOT survey_response_started_at IS NULL THEN 1 ELSE 0 END) | [] | [{"table": "qualtrics__response", "column": "survey_response_started_at"}] | False |
| B1 | SUM(CASE WHEN NOT survey_finished_at IS NULL THEN 1 ELSE 0 END) | [] | [{"table": "qualtrics__response", "column": "survey_finished_at"}] | False |


## S48

类别 `data`；来源 `query_db`；调用 `541a14adc4ec41679a7563bb6c00a299`；状态 `success`。

```sql
SELECT survey_response_recorded_at, survey_response_started_at, survey_finished_at FROM qualtrics__response WHERE survey_response_recorded_at IS NOT NULL LIMIT 10
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-081/attempt-01/sql/S48.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-081/attempt-01/sql/S48.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-081/attempt-01/results/S48.rows.jsonl)；完整：True；SHA256：`e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "qualtrics__response", "kind": "base", "block": null, "base_tables": ["qualtrics__response"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |


## S49

类别 `data`；来源 `query_db`；调用 `687a92673c4748aca882022200b4177f`；状态 `success`。

```sql
SELECT embedded_data, COUNT(*) AS cnt FROM qualtrics__response WHERE embedded_data IS NOT NULL AND embedded_data != '' GROUP BY embedded_data ORDER BY cnt DESC LIMIT 30
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-081/attempt-01/sql/S49.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-081/attempt-01/sql/S49.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-081/attempt-01/results/S49.rows.jsonl)；完整：True；SHA256：`55aa7c269d57d1a44c47f865a92ee495f3545b158489d6b9eea3b26474c53dae`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "qualtrics__response", "kind": "base", "block": null, "base_tables": ["qualtrics__response"]}] | [] | ["embedded_data"] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |


## S50

类别 `data`；来源 `query_db`；调用 `06c5296173df433db5c566e9f2321d50`；状态 `success`。

```sql
SELECT embedded_data, COUNT(*) AS cnt FROM qualtrics__response WHERE embedded_data IS NOT NULL AND embedded_data != '' GROUP BY embedded_data ORDER BY cnt ASC LIMIT 30
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-081/attempt-01/sql/S50.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-081/attempt-01/sql/S50.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-081/attempt-01/results/S50.rows.jsonl)；完整：True；SHA256：`4510a446e36330fc6ee1847ca0a29774e4328a42190fc7be36ef71d690b81212`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "qualtrics__response", "kind": "base", "block": null, "base_tables": ["qualtrics__response"]}] | [] | ["embedded_data"] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |


## S51

类别 `data`；来源 `query_db`；调用 `f80257a8a8cf487d8d33641504fac313`；状态 `success`。

```sql
SELECT user_language, COUNT(*) AS n, AVG(value) AS avg_value, MIN(value) AS min_v, MAX(value) AS max_v FROM qualtrics__response GROUP BY user_language ORDER BY avg_value DESC
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-081/attempt-01/sql/S51.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-081/attempt-01/sql/S51.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-081/attempt-01/results/S51.rows.jsonl)；完整：True；SHA256：`e1ec59053438c003dde294e882f2f9e345584c174a0f69853d0c16583dd10b16`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "qualtrics__response", "kind": "base", "block": null, "base_tables": ["qualtrics__response"]}] | [] | ["user_language"] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |
| B1 | AVG(value) | [{"table": "qualtrics__response", "column": "value"}] | [] | False |
| B1 | MIN(value) | [{"table": "qualtrics__response", "column": "value"}] | [] | False |
| B1 | MAX(value) | [{"table": "qualtrics__response", "column": "value"}] | [] | False |


## S52

类别 `data`；来源 `query_db`；调用 `0ca24336804041b1a37a70f05c546447`；状态 `success`。

```sql
SELECT contact_language, COUNT(*) AS n, AVG(value) AS avg_value, MIN(value) AS min_v, MAX(value) AS max_v FROM qualtrics__response GROUP BY contact_language ORDER BY avg_value DESC
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-081/attempt-01/sql/S52.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-081/attempt-01/sql/S52.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-081/attempt-01/results/S52.rows.jsonl)；完整：True；SHA256：`9ddc1e1263770893e502259a2135dc81fec1aae3a6967d05262a9de3e8903022`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "qualtrics__response", "kind": "base", "block": null, "base_tables": ["qualtrics__response"]}] | [] | ["contact_language"] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |
| B1 | AVG(value) | [{"table": "qualtrics__response", "column": "value"}] | [] | False |
| B1 | MIN(value) | [{"table": "qualtrics__response", "column": "value"}] | [] | False |
| B1 | MAX(value) | [{"table": "qualtrics__response", "column": "value"}] | [] | False |


## S53

类别 `data`；来源 `query_db`；调用 `b5aa9a7229694ce998d8f631b992d5e8`；状态 `success`。

```sql
SELECT r.survey_id, s.survey_name, s.project_category, s.project_type, COUNT(*) AS n_resp, AVG(r.value) AS avg_v, MIN(r.value) AS min_v, MAX(r.value) AS max_v FROM qualtrics__response r JOIN qualtrics__survey s ON r.survey_id = s.survey_id GROUP BY r.survey_id HAVING n_resp >= 20 ORDER BY avg_v DESC LIMIT 30
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-081/attempt-01/sql/S53.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-081/attempt-01/sql/S53.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-081/attempt-01/results/S53.rows.jsonl)；完整：True；SHA256：`10e350d38252a7203876a43fb64228adce632ff51e1a004ff3e9da3938de917e`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "r", "kind": "base", "block": null, "base_tables": ["qualtrics__response"]}, {"alias": "s", "kind": "base", "block": null, "base_tables": ["qualtrics__survey"]}] | [{"type": "INNER", "right": "qualtrics__survey AS s", "on": "r.survey_id = s.survey_id", "using": []}] | ["r.survey_id"] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |
| B1 | AVG(r.value) | [{"table": "qualtrics__response", "column": "value"}] | [] | False |
| B1 | MIN(r.value) | [{"table": "qualtrics__response", "column": "value"}] | [] | False |
| B1 | MAX(r.value) | [{"table": "qualtrics__response", "column": "value"}] | [] | False |


## S54

类别 `data`；来源 `query_db`；调用 `cdee286a82d643e690e6cc9bb63d19c5`；状态 `success`。

```sql
SELECT r.survey_id, s.survey_name, s.project_category, s.project_type, COUNT(*) AS n_resp, AVG(r.value) AS avg_v FROM qualtrics__response r JOIN qualtrics__survey s ON r.survey_id = s.survey_id GROUP BY r.survey_id HAVING n_resp >= 20 ORDER BY avg_v ASC LIMIT 30
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-081/attempt-01/sql/S54.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-081/attempt-01/sql/S54.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-081/attempt-01/results/S54.rows.jsonl)；完整：True；SHA256：`f41e6a3eddbafeefa149e5075fbd9b101385a30970a00b66ce2bc3e59fc97acc`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "r", "kind": "base", "block": null, "base_tables": ["qualtrics__response"]}, {"alias": "s", "kind": "base", "block": null, "base_tables": ["qualtrics__survey"]}] | [{"type": "INNER", "right": "qualtrics__survey AS s", "on": "r.survey_id = s.survey_id", "using": []}] | ["r.survey_id"] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |
| B1 | AVG(r.value) | [{"table": "qualtrics__response", "column": "value"}] | [] | False |


## S55

类别 `data`；来源 `query_db`；调用 `04ad0d98c507413ea2e3522445833e81`；状态 `success`。

```sql
SELECT r.survey_id, s.survey_name, r.user_language, COUNT(*) AS n, AVG(r.value) AS avg_v FROM qualtrics__response r JOIN qualtrics__survey s ON r.survey_id = s.survey_id GROUP BY r.survey_id, r.user_language HAVING n >= 5 ORDER BY r.survey_id, r.user_language LIMIT 50
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-081/attempt-01/sql/S55.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-081/attempt-01/sql/S55.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-081/attempt-01/results/S55.rows.jsonl)；完整：True；SHA256：`88b4a01da2a6e17288def4b29f7ed4989223b4034de84ce4f9c68c04aec52aad`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "r", "kind": "base", "block": null, "base_tables": ["qualtrics__response"]}, {"alias": "s", "kind": "base", "block": null, "base_tables": ["qualtrics__survey"]}] | [{"type": "INNER", "right": "qualtrics__survey AS s", "on": "r.survey_id = s.survey_id", "using": []}] | ["r.survey_id", "r.user_language"] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |
| B1 | AVG(r.value) | [{"table": "qualtrics__response", "column": "value"}] | [] | False |


## S56

类别 `data`；来源 `query_db`；调用 `26ccb0843f2e4e9bb88d2f75c092ae6b`；状态 `success`。

```sql
SELECT response_text, COUNT(*) AS n FROM qualtrics__response GROUP BY response_text ORDER BY n DESC
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-081/attempt-01/sql/S56.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-081/attempt-01/sql/S56.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-081/attempt-01/results/S56.rows.jsonl)；完整：True；SHA256：`06074ef0ffed190d0debe17519d16bc8d9aaf79c284fe3d0bca8cf183327f28c`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "qualtrics__response", "kind": "base", "block": null, "base_tables": ["qualtrics__response"]}] | [] | ["response_text"] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |


## S57

类别 `data`；来源 `query_db`；调用 `4e0973ddece548be86e172e0b4cba86a`；状态 `success`。

```sql
SELECT question_type, COUNT(*) AS n FROM qualtrics__response GROUP BY question_type ORDER BY n DESC
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-081/attempt-01/sql/S57.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-081/attempt-01/sql/S57.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-081/attempt-01/results/S57.rows.jsonl)；完整：True；SHA256：`ae042dc4e3d7e7740a40cadc32ccfac858559367a3bbd2483b5aa5b4e3250ac6`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "qualtrics__response", "kind": "base", "block": null, "base_tables": ["qualtrics__response"]}] | [] | ["question_type"] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |


## S58

类别 `data`；来源 `query_db`；调用 `d447cfca29414bc69ebc81d682287c48`；状态 `success`。

```sql
SELECT response_text, MIN(value) AS min_v, MAX(value) AS max_v, AVG(value) AS avg_v FROM qualtrics__response GROUP BY response_text ORDER BY avg_v DESC
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-081/attempt-01/sql/S58.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-081/attempt-01/sql/S58.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-081/attempt-01/results/S58.rows.jsonl)；完整：True；SHA256：`be59e77e7f4caeb47f2993bfb1f5f697fe1fb0b6033864a098081d79b2f1f38c`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "qualtrics__response", "kind": "base", "block": null, "base_tables": ["qualtrics__response"]}] | [] | ["response_text"] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | MIN(value) | [{"table": "qualtrics__response", "column": "value"}] | [] | False |
| B1 | MAX(value) | [{"table": "qualtrics__response", "column": "value"}] | [] | False |
| B1 | AVG(value) | [{"table": "qualtrics__response", "column": "value"}] | [] | False |


## S59

类别 `data`；来源 `query_db`；调用 `f524ed359c8e4f16a30c9811d5fd629a`；状态 `success`。

```sql
SELECT DISTINCT survey_name FROM qualtrics__survey WHERE survey_name LIKE '%Photo%' OR survey_name LIKE '%photo%' OR survey_name LIKE '%Editor%' OR survey_name LIKE '%editor%'
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-081/attempt-01/sql/S59.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-081/attempt-01/sql/S59.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-081/attempt-01/results/S59.rows.jsonl)；完整：True；SHA256：`e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "qualtrics__survey", "kind": "base", "block": null, "base_tables": ["qualtrics__survey"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |


## S60

类别 `data`；来源 `query_db`；调用 `3599ca71e21a4f5880c92a12bf8d2431`；状态 `success`。

```sql
SELECT DISTINCT survey_name FROM qualtrics__survey WHERE survey_name LIKE '%App%' OR survey_name LIKE '%app%' OR survey_name LIKE '%Mobile%' OR survey_name LIKE '%mobile%' OR survey_name LIKE '%Dev%' OR survey_name LIKE '%dev%'
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-081/attempt-01/sql/S60.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-081/attempt-01/sql/S60.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-081/attempt-01/results/S60.rows.jsonl)；完整：True；SHA256：`e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "qualtrics__survey", "kind": "base", "block": null, "base_tables": ["qualtrics__survey"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |


## S61

类别 `data`；来源 `query_db`；调用 `8d82e010f48445d39980089690d02ba4`；状态 `success`。

```sql
SELECT DISTINCT substr(survey_name, 1, 30) AS name_prefix FROM qualtrics__survey ORDER BY name_prefix
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-081/attempt-01/sql/S61.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-081/attempt-01/sql/S61.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-081/attempt-01/results/S61.rows.jsonl)；完整：True；SHA256：`cbe158d01f2a46e66904697a2d36412f82ad0f9631f83630df615dfa1fdd3e24`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "qualtrics__survey", "kind": "base", "block": null, "base_tables": ["qualtrics__survey"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |


## S62

类别 `data`；来源 `query_db`；调用 `0602e825fea1411994d5025fcfb92258`；状态 `success`。

```sql
SELECT survey_name, COUNT(*) AS n FROM qualtrics__survey GROUP BY survey_name ORDER BY survey_name LIMIT 200
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-081/attempt-01/sql/S62.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-081/attempt-01/sql/S62.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-081/attempt-01/results/S62.rows.jsonl)；完整：True；SHA256：`7dca815c0bdf3f3bed577255c933e2baba06989d5c52f17840af20c63aa23a6f`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "qualtrics__survey", "kind": "base", "block": null, "base_tables": ["qualtrics__survey"]}] | [] | ["survey_name"] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |


## S63

类别 `data`；来源 `query_db`；调用 `6ed0be46249f4f31bef1083d956a279d`；状态 `success`。

```sql
SELECT DISTINCT question_description FROM qualtrics__response WHERE question_description IS NOT NULL AND question_description != '' LIMIT 30
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-081/attempt-01/sql/S63.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-081/attempt-01/sql/S63.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-081/attempt-01/results/S63.rows.jsonl)；完整：True；SHA256：`e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "qualtrics__response", "kind": "base", "block": null, "base_tables": ["qualtrics__response"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |


## S64

类别 `data`；来源 `query_db`；调用 `d4f031831c384593b1f61d1430f212bd`；状态 `success`。

```sql
SELECT DISTINCT sub_question_text FROM qualtrics__response WHERE sub_question_text IS NOT NULL LIMIT 20
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-081/attempt-01/sql/S64.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-081/attempt-01/sql/S64.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-081/attempt-01/results/S64.rows.jsonl)；完整：True；SHA256：`28b781c60ae1fc89d390a436f2d3b2e485dc6fe94194e82fe4692d9bdfe5d4d3`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "qualtrics__response", "kind": "base", "block": null, "base_tables": ["qualtrics__response"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |


## S65

类别 `data`；来源 `query_db`；调用 `4bc5a85c33d84a39ac024bd96ccc0a23`；状态 `success`。

```sql
SELECT DISTINCT question_option_key FROM qualtrics__response WHERE question_option_key IS NOT NULL LIMIT 20
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-081/attempt-01/sql/S65.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-081/attempt-01/sql/S65.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-081/attempt-01/results/S65.rows.jsonl)；完整：True；SHA256：`96133edd30570394cb703f5c459f9f5ea73fc228a558cc9e3d71641bdc7faf1f`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "qualtrics__response", "kind": "base", "block": null, "base_tables": ["qualtrics__response"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |


## S66

类别 `data`；来源 `query_db`；调用 `a074cc5ed8334f65876441abd53b3c65`；状态 `success`。

```sql
SELECT DISTINCT brand_id FROM qualtrics__survey ORDER BY brand_id
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-081/attempt-01/sql/S66.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-081/attempt-01/sql/S66.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-081/attempt-01/results/S66.rows.jsonl)；完整：True；SHA256：`1902ef0886915a1eec9de29a334f6d40648ce7cf02d7ffd4e6e72d01169bf8e7`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "qualtrics__survey", "kind": "base", "block": null, "base_tables": ["qualtrics__survey"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |


## S67

类别 `data`；来源 `query_db`；调用 `dabc35dfe5e941e2bf9a6bbd8ee28485`；状态 `success`。

```sql
SELECT DISTINCT division_id FROM qualtrics__survey ORDER BY division_id
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-081/attempt-01/sql/S67.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-081/attempt-01/sql/S67.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-081/attempt-01/results/S67.rows.jsonl)；完整：True；SHA256：`9108f736b9acefcc1d86a1f6bf2c4b9b0d947582823efa65f1609ea6a76a1621`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "qualtrics__survey", "kind": "base", "block": null, "base_tables": ["qualtrics__survey"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |


## S68

类别 `data`；来源 `query_db`；调用 `30b2d7484085410398193fb440a756f1`；状态 `success`。

```sql
SELECT r.survey_id, r.user_language, COUNT(*) AS n, AVG(r.value) AS avg_v, MIN(r.value) AS min_v, MAX(r.value) AS max_v FROM qualtrics__response r GROUP BY r.survey_id, r.user_language HAVING n >= 5 AND AVG(r.value) > 7.0 ORDER BY avg_v DESC LIMIT 30
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-081/attempt-01/sql/S68.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-081/attempt-01/sql/S68.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-081/attempt-01/results/S68.rows.jsonl)；完整：True；SHA256：`57a34ec65d35618b913fa2f6a38d2bf00dc65d95e9875178c4270176bfa1b38d`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "r", "kind": "base", "block": null, "base_tables": ["qualtrics__response"]}] | [] | ["r.survey_id", "r.user_language"] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |
| B1 | AVG(r.value) | [{"table": "qualtrics__response", "column": "value"}] | [] | False |
| B1 | MIN(r.value) | [{"table": "qualtrics__response", "column": "value"}] | [] | False |
| B1 | MAX(r.value) | [{"table": "qualtrics__response", "column": "value"}] | [] | False |
| B1 | AVG(r.value) | [{"table": "qualtrics__response", "column": "value"}] | [] | False |


## S69

类别 `data`；来源 `query_db`；调用 `d4cb45eed7404f2c818c731dc3ad76ac`；状态 `success`。

```sql
SELECT r.survey_id, r.user_language, COUNT(*) AS n, AVG(r.value) AS avg_v FROM qualtrics__response r GROUP BY r.survey_id, r.user_language HAVING n >= 5 AND AVG(r.value) < 3.0 ORDER BY avg_v ASC LIMIT 30
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-081/attempt-01/sql/S69.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-081/attempt-01/sql/S69.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-081/attempt-01/results/S69.rows.jsonl)；完整：True；SHA256：`3d8be79b1db67a9d792c2bb92c05436c45053353c374283d2ede4bcc35ed1a86`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "r", "kind": "base", "block": null, "base_tables": ["qualtrics__response"]}] | [] | ["r.survey_id", "r.user_language"] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |
| B1 | AVG(r.value) | [{"table": "qualtrics__response", "column": "value"}] | [] | False |
| B1 | AVG(r.value) | [{"table": "qualtrics__response", "column": "value"}] | [] | False |


## S70

类别 `data`；来源 `query_db`；调用 `99ecf597fa9647e19ac678ff9161342e`；状态 `success`。

```sql
SELECT r.user_language, COUNT(*) AS n, AVG(r.value) AS avg_v, MIN(r.value) AS min_v, MAX(r.value) AS max_v FROM qualtrics__response r WHERE r.survey_id = 'SUR10002866953' GROUP BY r.user_language ORDER BY avg_v DESC
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-081/attempt-01/sql/S70.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-081/attempt-01/sql/S70.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-081/attempt-01/results/S70.rows.jsonl)；完整：True；SHA256：`5ddf862c2a94471b332ceef1d07f109fbf379b40faefbff85bdbe6f9f83dc6e3`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "r", "kind": "base", "block": null, "base_tables": ["qualtrics__response"]}] | [] | ["r.user_language"] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |
| B1 | AVG(r.value) | [{"table": "qualtrics__response", "column": "value"}] | [] | False |
| B1 | MIN(r.value) | [{"table": "qualtrics__response", "column": "value"}] | [] | False |
| B1 | MAX(r.value) | [{"table": "qualtrics__response", "column": "value"}] | [] | False |


## S71

类别 `data`；来源 `query_db`；调用 `c0af8d8441ef4051abfcc10d436bdb35`；状态 `success`。

```sql
SELECT s.survey_name, s.project_category, s.project_type, s.brand_base_url, s.count_questions, s.count_survey_responses FROM qualtrics__survey s WHERE s.survey_id = 'SUR10002866953'
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-081/attempt-01/sql/S71.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-081/attempt-01/sql/S71.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-081/attempt-01/results/S71.rows.jsonl)；完整：True；SHA256：`5d759d743409d2955ea95f882487f81d3e4a4686d3dfb8e3b03770517d9caf9d`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "s", "kind": "base", "block": null, "base_tables": ["qualtrics__survey"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |


## S72

类别 `data`；来源 `query_db`；调用 `eae5cc7ddeb7478da9760aa7aff10e63`；状态 `success`。

```sql
SELECT COUNT(*) AS n_resp FROM qualtrics__response r WHERE r.survey_id = 'SUR10002866953'
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-081/attempt-01/sql/S72.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-081/attempt-01/sql/S72.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-081/attempt-01/results/S72.rows.jsonl)；完整：True；SHA256：`275833d9a885824432f31affecec70375616cf7a601aac3439791acddb2a66df`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "r", "kind": "base", "block": null, "base_tables": ["qualtrics__response"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |


## S73

类别 `data`；来源 `query_db`；调用 `98587ef12f3d49af941c42a74c24f1d2`；状态 `success`。

```sql
SELECT * FROM qualtrics__survey LIMIT 5
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-081/attempt-01/sql/S73.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-081/attempt-01/sql/S73.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-081/attempt-01/results/S73.rows.jsonl)；完整：True；SHA256：`b6948fbfa75d954bab7a249f629a9652b8ca6c2383e3736199c54273844a3388`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "qualtrics__survey", "kind": "base", "block": null, "base_tables": ["qualtrics__survey"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |


## S74

类别 `data`；来源 `query_db`；调用 `24b83d6b6a92459cb336f301d68baebb`；状态 `success`。

```sql

WITH lang_stats AS (
  SELECT survey_id, user_language, COUNT(*) AS n, AVG(value) AS avg_v
  FROM qualtrics__response
  GROUP BY survey_id, user_language
  HAVING n >= 3
),
survey_stats AS (
  SELECT survey_id,
         MAX(avg_v) AS max_lang_avg,
         MIN(avg_v) AS min_lang_avg,
         SUM(n) AS total_resp,
         COUNT(*) AS n_langs
  FROM lang_stats
  GROUP BY survey_id
)
SELECT survey_id, max_lang_avg, min_lang_avg, total_resp, n_langs
FROM survey_stats
WHERE max_lang_avg > 7.0 AND min_lang_avg < 3.0
ORDER BY (max_lang_avg - min_lang_avg) DESC
LIMIT 30

```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-081/attempt-01/sql/S74.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-081/attempt-01/sql/S74.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-081/attempt-01/results/S74.rows.jsonl)；完整：True；SHA256：`86cafd816419e3a0619ce8369adacf85c44306f5e6848294df2de3af843cd5b4`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "qualtrics__response", "kind": "base", "block": null, "base_tables": ["qualtrics__response"]}] | [] | ["survey_id", "user_language"] |
| B2 | [{"alias": "lang_stats", "kind": "derived", "block": "B1", "base_tables": ["qualtrics__response"]}] | [] | ["survey_id"] |
| B3 | [{"alias": "survey_stats", "kind": "derived", "block": "B2", "base_tables": ["qualtrics__response"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |
| B1 | AVG(value) | [{"table": "qualtrics__response", "column": "value"}] | [] | False |
| B2 | MAX(avg_v) | [{"table": "qualtrics__response", "column": "value"}] | [] | False |
| B2 | MIN(avg_v) | [{"table": "qualtrics__response", "column": "value"}] | [] | False |
| B2 | SUM(n) | [] | [] | False |
| B2 | COUNT(*) | [] | [] | True |


## S75

类别 `data`；来源 `query_db`；调用 `04d0d6efae6c4dd986eedf3962087ffb`；状态 `failed`。

```sql
SELECT r.survey_id, s.survey_name, COUNT(*) AS n, AVG(r.value) AS avg_v, AVG(r.value)*10 AS score, STDDEV(r.value) AS sd FROM qualtrics__response r JOIN qualtrics__survey s ON r.survey_id=s.survey_id GROUP BY r.survey_id HAVING n >= 30 ORDER BY avg_v DESC LIMIT 40
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-081/attempt-01/sql/S75.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-081/attempt-01/sql/S75.parameters.json)。

错误：`OperationalError('no such function: STDDEV')`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "r", "kind": "base", "block": null, "base_tables": ["qualtrics__response"]}, {"alias": "s", "kind": "base", "block": null, "base_tables": ["qualtrics__survey"]}] | [{"type": "INNER", "right": "qualtrics__survey AS s", "on": "r.survey_id = s.survey_id", "using": []}] | ["r.survey_id"] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |
| B1 | AVG(r.value) | [{"table": "qualtrics__response", "column": "value"}] | [] | False |
| B1 | STDDEV(r.value) | [{"table": "qualtrics__response", "column": "value"}] | [] | False |
| B1 | AVG(r.value) | [{"table": "qualtrics__response", "column": "value"}] | [] | False |


## S76

类别 `data`；来源 `query_db`；调用 `b7e0342a15424fd29b28a5d5af9d3620`；状态 `success`。

```sql
SELECT r.survey_id, s.survey_name, COUNT(*) AS n, AVG(r.value) AS avg_v, AVG(r.value)*10 AS score FROM qualtrics__response r JOIN qualtrics__survey s ON r.survey_id=s.survey_id GROUP BY r.survey_id HAVING n >= 30 ORDER BY avg_v DESC LIMIT 40
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-081/attempt-01/sql/S76.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-081/attempt-01/sql/S76.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-081/attempt-01/results/S76.rows.jsonl)；完整：True；SHA256：`281ecda75caec713f79c4437fdeee12f893f9f6aaf641c650881ca5fa6be703c`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "r", "kind": "base", "block": null, "base_tables": ["qualtrics__response"]}, {"alias": "s", "kind": "base", "block": null, "base_tables": ["qualtrics__survey"]}] | [{"type": "INNER", "right": "qualtrics__survey AS s", "on": "r.survey_id = s.survey_id", "using": []}] | ["r.survey_id"] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |
| B1 | AVG(r.value) | [{"table": "qualtrics__response", "column": "value"}] | [] | False |
| B1 | AVG(r.value) | [{"table": "qualtrics__response", "column": "value"}] | [] | False |


## S77

类别 `data`；来源 `query_db`；调用 `2892db8760b44d8eaea2d2f1f5dcb12f`；状态 `success`。

```sql
SELECT r.survey_id, s.survey_name, COUNT(*) AS n, AVG(r.value) AS avg_v, AVG(r.value)*10 AS score FROM qualtrics__response r JOIN qualtrics__survey s ON r.survey_id=s.survey_id GROUP BY r.survey_id HAVING n >= 10 ORDER BY avg_v DESC LIMIT 40
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-081/attempt-01/sql/S77.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-081/attempt-01/sql/S77.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-081/attempt-01/results/S77.rows.jsonl)；完整：True；SHA256：`1cf71d3329860d5c99c09fc80dec055a26a081298a06c43382b0876a1212e144`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "r", "kind": "base", "block": null, "base_tables": ["qualtrics__response"]}, {"alias": "s", "kind": "base", "block": null, "base_tables": ["qualtrics__survey"]}] | [{"type": "INNER", "right": "qualtrics__survey AS s", "on": "r.survey_id = s.survey_id", "using": []}] | ["r.survey_id"] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |
| B1 | AVG(r.value) | [{"table": "qualtrics__response", "column": "value"}] | [] | False |
| B1 | AVG(r.value) | [{"table": "qualtrics__response", "column": "value"}] | [] | False |


## S78

类别 `data`；来源 `query_db`；调用 `7be156bea6dd4d84b7706a921e80a42c`；状态 `success`。

```sql
SELECT r.user_language, COUNT(*) AS n, AVG(r.value) AS avg_v, MIN(r.value) AS min_v, MAX(r.value) AS max_v FROM qualtrics__response r WHERE r.survey_id = 'SUR10001882036' GROUP BY r.user_language ORDER BY avg_v DESC
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-081/attempt-01/sql/S78.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-081/attempt-01/sql/S78.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-081/attempt-01/results/S78.rows.jsonl)；完整：True；SHA256：`6aebcf093bf3140fd91e9b0dc97acc3ea981a56c4cfa90ef1e74539282bb3034`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "r", "kind": "base", "block": null, "base_tables": ["qualtrics__response"]}] | [] | ["r.user_language"] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |
| B1 | AVG(r.value) | [{"table": "qualtrics__response", "column": "value"}] | [] | False |
| B1 | MIN(r.value) | [{"table": "qualtrics__response", "column": "value"}] | [] | False |
| B1 | MAX(r.value) | [{"table": "qualtrics__response", "column": "value"}] | [] | False |


## S79

类别 `data`；来源 `query_db`；调用 `e20b2185f51b47c8ba9a6166c5d59ebe`；状态 `success`。

```sql
SELECT s.survey_name, s.project_category, s.project_type, s.brand_base_url, s.count_questions, s.count_survey_responses FROM qualtrics__survey s WHERE s.survey_id = 'SUR10001882036'
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-081/attempt-01/sql/S79.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-081/attempt-01/sql/S79.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-081/attempt-01/results/S79.rows.jsonl)；完整：True；SHA256：`294657f9f85e18e4b448c213dffd55474d2004ba15ced9d4c7ff53be512e6e46`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "s", "kind": "base", "block": null, "base_tables": ["qualtrics__survey"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |


## S80

类别 `data`；来源 `query_db`；调用 `8ee5c8fbdf2e42aea635cff0d07f805b`；状态 `success`。

```sql
SELECT survey_id, COUNT(*) AS cnt FROM qualtrics__survey GROUP BY survey_id HAVING cnt > 1 LIMIT 20
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-081/attempt-01/sql/S80.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-081/attempt-01/sql/S80.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-081/attempt-01/results/S80.rows.jsonl)；完整：True；SHA256：`cdbf7cf91fb0175ded4f16ef3d1cc6fea3e29062768d99e5123a5d599b3bf7a1`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "qualtrics__survey", "kind": "base", "block": null, "base_tables": ["qualtrics__survey"]}] | [] | ["survey_id"] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |


## S81

类别 `data`；来源 `query_db`；调用 `8f6d2248783649fdac4975af36bef24a`；状态 `success`。

```sql
SELECT user_language, COUNT(*) AS n, AVG(value) AS avg_v FROM qualtrics__response WHERE survey_id = 'SUR10001882036' GROUP BY user_language
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-081/attempt-01/sql/S81.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-081/attempt-01/sql/S81.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-081/attempt-01/results/S81.rows.jsonl)；完整：True；SHA256：`16bd01ef2f9f50840231a0ecbfd10389e1d6ec912ecc4ce69f1f223d94de569b`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "qualtrics__response", "kind": "base", "block": null, "base_tables": ["qualtrics__response"]}] | [] | ["user_language"] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |
| B1 | AVG(value) | [{"table": "qualtrics__response", "column": "value"}] | [] | False |


## S82

类别 `data`；来源 `query_db`；调用 `d46fcdca588941a0969dee536a707877`；状态 `success`。

```sql
SELECT survey_id, survey_name, COUNT(*) FROM qualtrics__survey WHERE survey_id = 'SUR10001882036' GROUP BY survey_id, survey_name
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-081/attempt-01/sql/S82.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-081/attempt-01/sql/S82.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-081/attempt-01/results/S82.rows.jsonl)；完整：True；SHA256：`213286bd7419497fd7077468d26ed1c794b92f89361e7749fbb53e204f5b7c77`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "qualtrics__survey", "kind": "base", "block": null, "base_tables": ["qualtrics__survey"]}] | [] | ["survey_id", "survey_name"] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |


## S83

类别 `data`；来源 `query_db`；调用 `b0f129a0d5304bc59cc773bd0a2d933e`；状态 `success`。

```sql
SELECT survey_id, user_language, contact_language, value, response_text, survey_name FROM qualtrics__response WHERE survey_id = 'SUR10001882036'
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-081/attempt-01/sql/S83.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-081/attempt-01/sql/S83.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-081/attempt-01/results/S83.rows.jsonl)；完整：True；SHA256：`cd7d0d8e15594332d1025751730b8129e38e2161fb5e10bcab9ac92de98b9282`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "qualtrics__response", "kind": "base", "block": null, "base_tables": ["qualtrics__response"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |


## S84

类别 `data`；来源 `query_db`；调用 `bd0adfea7fe0429ca52900a54eb3c6c9`；状态 `success`。

```sql
SELECT COUNT(*) FROM qualtrics__response WHERE survey_id = 'SUR10001882036'
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-081/attempt-01/sql/S84.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-081/attempt-01/sql/S84.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-081/attempt-01/results/S84.rows.jsonl)；完整：True；SHA256：`631e21d653c4403cc79be7266a9ded76c4f00e70e98fc0ef2bb3d0d0d3e0a09e`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "qualtrics__response", "kind": "base", "block": null, "base_tables": ["qualtrics__response"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |


## S85

类别 `data`；来源 `query_db`；调用 `0cac1c58f124443f8360f5c6430b5fa7`；状态 `success`。

```sql
SELECT * FROM qualtrics__response WHERE survey_id = 'SUR10001882036'
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-081/attempt-01/sql/S85.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-081/attempt-01/sql/S85.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-081/attempt-01/results/S85.rows.jsonl)；完整：True；SHA256：`3e1242e45aa7bf8a8c06c3491e1803b984a43855c741bdfd517f89f74ca7ea8b`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "qualtrics__response", "kind": "base", "block": null, "base_tables": ["qualtrics__response"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |


## S86

类别 `data`；来源 `query_db`；调用 `f73bcd29871c408f87a2a254b35203de`；状态 `success`。

```sql
SELECT COUNT(*) AS total_rows, COUNT(DISTINCT survey_id) AS distinct_ids FROM qualtrics__survey
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-081/attempt-01/sql/S86.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-081/attempt-01/sql/S86.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-081/attempt-01/results/S86.rows.jsonl)；完整：True；SHA256：`29e6e6e92a873543ebff2b3a5d8321b1a629dcc865b5a853a556bb390ebdf00f`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "qualtrics__survey", "kind": "base", "block": null, "base_tables": ["qualtrics__survey"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |
| B1 | COUNT(DISTINCT survey_id) | [{"table": "qualtrics__survey", "column": "survey_id"}] | [] | False |


## S87

类别 `data`；来源 `query_db`；调用 `fae17fb1375f46a5b7b556988999e575`；状态 `success`。

```sql
SELECT COUNT(*) AS n FROM (SELECT survey_id FROM qualtrics__survey GROUP BY survey_id HAVING COUNT(*) > 1)
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-081/attempt-01/sql/S87.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-081/attempt-01/sql/S87.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-081/attempt-01/results/S87.rows.jsonl)；完整：True；SHA256：`76de9bc73628d2c92d3248d41c87a1aa2d02fc59487a61cfb840ba7e12a98a8d`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "qualtrics__survey", "kind": "base", "block": null, "base_tables": ["qualtrics__survey"]}] | [] | ["survey_id"] |
| B2 | [{"alias": "", "kind": "derived", "block": "B1", "base_tables": ["qualtrics__survey"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |
| B2 | COUNT(*) | [] | [] | True |


## S88

类别 `data`；来源 `query_db`；调用 `d48f7c2b65194dad95cf95351b05e84c`；状态 `success`。

```sql
SELECT survey_id, COUNT(*) AS cnt FROM qualtrics__survey GROUP BY survey_id ORDER BY cnt DESC LIMIT 10
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-081/attempt-01/sql/S88.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-081/attempt-01/sql/S88.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-081/attempt-01/results/S88.rows.jsonl)；完整：True；SHA256：`b14547c8551e7983f1ff74a5b57b10d5ba8b84523b977fbc996051848e5e2491`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "qualtrics__survey", "kind": "base", "block": null, "base_tables": ["qualtrics__survey"]}] | [] | ["survey_id"] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |


## S89

类别 `data`；来源 `query_db`；调用 `c400f48eb11649ffba27a58abb3bc421`；状态 `success`。

```sql
SELECT DISTINCT substr(survey_name, 1, length(survey_name) - 5) AS base_name FROM qualtrics__survey ORDER BY base_name
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-081/attempt-01/sql/S89.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-081/attempt-01/sql/S89.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-081/attempt-01/results/S89.rows.jsonl)；完整：True；SHA256：`a5dcefcded97c2388dc6d7c1de043b7eed34f69fec273073f155ae5c4a79409b`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "qualtrics__survey", "kind": "base", "block": null, "base_tables": ["qualtrics__survey"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |


## S90

类别 `data`；来源 `query_db`；调用 `e4c3b0a2f26042e9b86ecf0daf932852`；状态 `success`。

```sql
SELECT DISTINCT substr(survey_name, 1, length(survey_name) - 5) AS base_name FROM qualtrics__survey ORDER BY base_name
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-081/attempt-01/sql/S90.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-081/attempt-01/sql/S90.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-081/attempt-01/results/S90.rows.jsonl)；完整：True；SHA256：`a5dcefcded97c2388dc6d7c1de043b7eed34f69fec273073f155ae5c4a79409b`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "qualtrics__survey", "kind": "base", "block": null, "base_tables": ["qualtrics__survey"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |


## S91

类别 `data`；来源 `query_db`；调用 `20dacf38cdb14578be59797efb84d9f9`；状态 `success`。

```sql
SELECT DISTINCT substr(survey_name, 1, length(survey_name) - 5) AS base_name FROM qualtrics__survey ORDER BY base_name
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-081/attempt-01/sql/S91.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-081/attempt-01/sql/S91.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-081/attempt-01/results/S91.rows.jsonl)；完整：True；SHA256：`a5dcefcded97c2388dc6d7c1de043b7eed34f69fec273073f155ae5c4a79409b`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "qualtrics__survey", "kind": "base", "block": null, "base_tables": ["qualtrics__survey"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |


## S92

类别 `data`；来源 `query_db`；调用 `496196c152d047b68003955a761e9693`；状态 `success`。

```sql
SELECT r.user_language, COUNT(*) AS n, AVG(r.value) AS avg_v, MIN(r.value) AS min_v, MAX(r.value) AS max_v FROM qualtrics__response r WHERE r.survey_id = 'SUR10000974099' GROUP BY r.user_language ORDER BY avg_v DESC
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-081/attempt-01/sql/S92.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-081/attempt-01/sql/S92.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-081/attempt-01/results/S92.rows.jsonl)；完整：True；SHA256：`5e7d85d120aa97e66a9e6077b23d6c0f7457445fa2bc7c9b673cc31ce4eb629f`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "r", "kind": "base", "block": null, "base_tables": ["qualtrics__response"]}] | [] | ["r.user_language"] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |
| B1 | AVG(r.value) | [{"table": "qualtrics__response", "column": "value"}] | [] | False |
| B1 | MIN(r.value) | [{"table": "qualtrics__response", "column": "value"}] | [] | False |
| B1 | MAX(r.value) | [{"table": "qualtrics__response", "column": "value"}] | [] | False |


## S93

类别 `data`；来源 `query_db`；调用 `0c637a26f29c4a8d9d2bfedb2e720c6f`；状态 `success`。

```sql
SELECT s.survey_name, s.project_category, s.project_type FROM qualtrics__survey s WHERE s.survey_id = 'SUR10000974099' LIMIT 1
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-081/attempt-01/sql/S93.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-081/attempt-01/sql/S93.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-081/attempt-01/results/S93.rows.jsonl)；完整：True；SHA256：`c47350e1f8c768fc66b8de6c8df815b0aababf4e2272656d84ba3b45f8bde67d`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "s", "kind": "base", "block": null, "base_tables": ["qualtrics__survey"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |


## S94

类别 `data`；来源 `query_db`；调用 `ed36909a05e34664a9a248f691cf712b`；状态 `success`。

```sql
SELECT question_type, COUNT(*) AS n, MIN(value) AS min_v, MAX(value) AS max_v, AVG(value) AS avg_v FROM qualtrics__response GROUP BY question_type ORDER BY n DESC
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-081/attempt-01/sql/S94.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-081/attempt-01/sql/S94.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-081/attempt-01/results/S94.rows.jsonl)；完整：True；SHA256：`8c1ace5c0a728f8381290d950c2562f7e4c7bbb55b20c762a8018e6c49d86756`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "qualtrics__response", "kind": "base", "block": null, "base_tables": ["qualtrics__response"]}] | [] | ["question_type"] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |
| B1 | MIN(value) | [{"table": "qualtrics__response", "column": "value"}] | [] | False |
| B1 | MAX(value) | [{"table": "qualtrics__response", "column": "value"}] | [] | False |
| B1 | AVG(value) | [{"table": "qualtrics__response", "column": "value"}] | [] | False |


## S95

类别 `data`；来源 `query_db`；调用 `737e37a1d81047069d2e348fe0a13b53`；状态 `success`。

```sql
SELECT distribution_channel, COUNT(*) AS n FROM qualtrics__response GROUP BY distribution_channel ORDER BY n DESC
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-081/attempt-01/sql/S95.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-081/attempt-01/sql/S95.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-081/attempt-01/results/S95.rows.jsonl)；完整：True；SHA256：`539c1f542b77336f157256ff6c35783c6b0bfff3b8b69f686061f0936bd365c1`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "qualtrics__response", "kind": "base", "block": null, "base_tables": ["qualtrics__response"]}] | [] | ["distribution_channel"] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |


## S96

类别 `data`；来源 `query_db`；调用 `280e41cc69ca45aaa0c993cd072d6fae`；状态 `success`。

```sql
SELECT contact_id, COUNT(*) AS n FROM qualtrics__response GROUP BY contact_id ORDER BY n DESC LIMIT 10
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-081/attempt-01/sql/S96.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-081/attempt-01/sql/S96.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-081/attempt-01/results/S96.rows.jsonl)；完整：True；SHA256：`c70e06319e1d0d0874303aef098151f5a70be0531f22c494e7146d81e47489b1`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "qualtrics__response", "kind": "base", "block": null, "base_tables": ["qualtrics__response"]}] | [] | ["contact_id"] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |


## S97

类别 `data`；来源 `query_db`；调用 `7a87f29e73824eb1bb81ef90cff43f98`；状态 `success`。

```sql
SELECT COUNT(DISTINCT contact_id) FROM qualtrics__response
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-081/attempt-01/sql/S97.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-081/attempt-01/sql/S97.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-081/attempt-01/results/S97.rows.jsonl)；完整：True；SHA256：`9225ddc6fea44527335bcaa47bcf97c0382cb1e3e59e42aa15116485e723e089`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "qualtrics__response", "kind": "base", "block": null, "base_tables": ["qualtrics__response"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(DISTINCT contact_id) | [{"table": "qualtrics__response", "column": "contact_id"}] | [] | False |


## S98

类别 `data`；来源 `query_db`；调用 `df96f01920384f898393e5feb646aaa8`；状态 `success`。

```sql
SELECT question_id, COUNT(DISTINCT survey_id) AS n_surveys, COUNT(*) AS n_resp FROM qualtrics__response GROUP BY question_id ORDER BY n_surveys DESC LIMIT 20
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-081/attempt-01/sql/S98.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-081/attempt-01/sql/S98.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-081/attempt-01/results/S98.rows.jsonl)；完整：True；SHA256：`d840be81d08ed89ae40804e831b6f939799375301337263186cd3e911b377110`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "qualtrics__response", "kind": "base", "block": null, "base_tables": ["qualtrics__response"]}] | [] | ["question_id"] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(DISTINCT survey_id) | [{"table": "qualtrics__response", "column": "survey_id"}] | [] | False |
| B1 | COUNT(*) | [] | [] | True |


## S99

类别 `data`；来源 `query_db`；调用 `ab27358084fc418a849dfc042d291f99`；状态 `success`。

```sql
SELECT question_id, COUNT(*) AS n_resp, COUNT(DISTINCT survey_id) AS n_surveys, COUNT(DISTINCT survey_response_id) AS n_respondents FROM qualtrics__response GROUP BY question_id ORDER BY n_respondents DESC LIMIT 20
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-081/attempt-01/sql/S99.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-081/attempt-01/sql/S99.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-081/attempt-01/results/S99.rows.jsonl)；完整：True；SHA256：`d0064b372e0502cb6c0ed8e829999bc62573d44e789f21cd48055d138037378e`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "qualtrics__response", "kind": "base", "block": null, "base_tables": ["qualtrics__response"]}] | [] | ["question_id"] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |
| B1 | COUNT(DISTINCT survey_id) | [{"table": "qualtrics__response", "column": "survey_id"}] | [] | False |
| B1 | COUNT(DISTINCT survey_response_id) | [{"table": "qualtrics__response", "column": "survey_response_id"}] | [] | False |


## S100

类别 `data`；来源 `query_db`；调用 `a35c8f0e0d814f718adbba37b5d0f4b1`；状态 `success`。

```sql
SELECT question_id, question_text, question_type, COUNT(*) AS n_resp FROM qualtrics__response GROUP BY question_id ORDER BY n_resp DESC LIMIT 30
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-081/attempt-01/sql/S100.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-081/attempt-01/sql/S100.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-081/attempt-01/results/S100.rows.jsonl)；完整：True；SHA256：`279917adeba75e39475271994e64792e4b3bc48ef14d5f67a89276414f655623`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "qualtrics__response", "kind": "base", "block": null, "base_tables": ["qualtrics__response"]}] | [] | ["question_id"] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |


## S101

类别 `data`；来源 `query_db`；调用 `3f8499575f164269a84669f365b921ab`；状态 `success`。

```sql
SELECT CAST(value AS INTEGER) AS v_int, COUNT(*) AS n, AVG(value) AS avg_val FROM qualtrics__response GROUP BY CAST(value AS INTEGER) ORDER BY v_int
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-081/attempt-01/sql/S101.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-081/attempt-01/sql/S101.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-081/attempt-01/results/S101.rows.jsonl)；完整：True；SHA256：`8804eb557bcbed361c1cf4cfe96db73ce1271db083cad3f43b0514a271644e66`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "qualtrics__response", "kind": "base", "block": null, "base_tables": ["qualtrics__response"]}] | [] | ["CAST(value AS INTEGER)"] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |
| B1 | AVG(value) | [{"table": "qualtrics__response", "column": "value"}] | [] | False |


## S102

类别 `data`；来源 `query_db`；调用 `9810f08346ec42e7af0e869788747be9`；状态 `success`。

```sql
SELECT sub_question_text, COUNT(*) AS n, AVG(value) AS avg_v FROM qualtrics__response GROUP BY sub_question_text ORDER BY n DESC LIMIT 30
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-081/attempt-01/sql/S102.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-081/attempt-01/sql/S102.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-081/attempt-01/results/S102.rows.jsonl)；完整：True；SHA256：`011133c5b4d02015dded47b17e40329bac6a0ac02198f4d1bd90eaa9b1d333a5`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "qualtrics__response", "kind": "base", "block": null, "base_tables": ["qualtrics__response"]}] | [] | ["sub_question_text"] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |
| B1 | AVG(value) | [{"table": "qualtrics__response", "column": "value"}] | [] | False |


## S103

类别 `data`；来源 `query_db`；调用 `1956029e7b0b4549a03480ec317152fe`；状态 `success`。

```sql
SELECT question_option_key, COUNT(*) AS n, AVG(value) AS avg_v FROM qualtrics__response GROUP BY question_option_key ORDER BY n DESC LIMIT 30
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-081/attempt-01/sql/S103.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-081/attempt-01/sql/S103.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-081/attempt-01/results/S103.rows.jsonl)；完整：True；SHA256：`f57a211d2cdc52f9d0a346c8382a7adf85ee0d3ef49475202460db58349507d6`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "qualtrics__response", "kind": "base", "block": null, "base_tables": ["qualtrics__response"]}] | [] | ["question_option_key"] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |
| B1 | AVG(value) | [{"table": "qualtrics__response", "column": "value"}] | [] | False |


## S104

类别 `data`；来源 `python`；调用 `8e5d04390c80439381876da39b2b5f33`；状态 `success`。

```sql

    SELECT survey_id, user_language, COUNT(*) AS n, 
           AVG(value) AS avg_v, MIN(value) AS min_v, MAX(value) AS max_v
    FROM qualtrics__response
    GROUP BY survey_id, user_language
    HAVING n >= 3

```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-081/attempt-01/sql/S104.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-081/attempt-01/sql/S104.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-081/attempt-01/results/S104.rows.jsonl)；完整：True；SHA256：`53343d34cf0ba34f3376cd33036a9fd697a1ab5c233f380bf925a32e3d411919`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "qualtrics__response", "kind": "base", "block": null, "base_tables": ["qualtrics__response"]}] | [] | ["survey_id", "user_language"] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |
| B1 | AVG(value) | [{"table": "qualtrics__response", "column": "value"}] | [] | False |
| B1 | MIN(value) | [{"table": "qualtrics__response", "column": "value"}] | [] | False |
| B1 | MAX(value) | [{"table": "qualtrics__response", "column": "value"}] | [] | False |


## S105

类别 `data`；来源 `python`；调用 `b4f9642575d84cdb97c4ce35a02928b1`；状态 `success`。

```sql

    SELECT survey_response_id, survey_id, question_id, question_text, 
           question_type, value, response_text, sub_question_key,
           sub_question_text, question_option_key, user_language,
           contact_language, embedded_data
    FROM qualtrics__response
    WHERE survey_response_id = 'SUR10008772252'
    ORDER BY question_id

```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-081/attempt-01/sql/S105.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-081/attempt-01/sql/S105.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-081/attempt-01/results/S105.rows.jsonl)；完整：True；SHA256：`1bf131348959b0b9f186686181924ec49c9f58d5ae7ad716605e195c72ae0ddc`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "qualtrics__response", "kind": "base", "block": null, "base_tables": ["qualtrics__response"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |


## S106

类别 `data`；来源 `python`；调用 `b4f9642575d84cdb97c4ce35a02928b1`；状态 `success`。

```sql

    SELECT survey_id, question_type, COUNT(*) as cnt
    FROM qualtrics__response
    GROUP BY survey_id, question_type
    HAVING COUNT(*) >= 10
    ORDER BY cnt DESC
    LIMIT 20

```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-081/attempt-01/sql/S106.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-081/attempt-01/sql/S106.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-081/attempt-01/results/S106.rows.jsonl)；完整：True；SHA256：`b65a1a3cd53844f5a3a9dc74757db045e47b0525dfb59195cab4bd79f762700e`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "qualtrics__response", "kind": "base", "block": null, "base_tables": ["qualtrics__response"]}] | [] | ["survey_id", "question_type"] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |
| B1 | COUNT(*) | [] | [] | True |


## S107

类别 `data`；来源 `python`；调用 `b4f9642575d84cdb97c4ce35a02928b1`；状态 `success`。

```sql

    SELECT survey_response_id, COUNT(*) as n_questions
    FROM qualtrics__response
    GROUP BY survey_response_id
    ORDER BY n_questions DESC
    LIMIT 20

```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-081/attempt-01/sql/S107.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-081/attempt-01/sql/S107.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-081/attempt-01/results/S107.rows.jsonl)；完整：True；SHA256：`8ad3572ed78eccc4299e1661db7bc89ffe703945a14518b2d606cb9b46fbe1e5`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "qualtrics__response", "kind": "base", "block": null, "base_tables": ["qualtrics__response"]}] | [] | ["survey_response_id"] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |


## S108

类别 `data`；来源 `python`；调用 `b4f9642575d84cdb97c4ce35a02928b1`；状态 `success`。

```sql

    SELECT question_text, COUNT(*) as cnt
    FROM qualtrics__response
    GROUP BY question_text
    ORDER BY cnt DESC
    LIMIT 30

```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-081/attempt-01/sql/S108.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-081/attempt-01/sql/S108.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-081/attempt-01/results/S108.rows.jsonl)；完整：True；SHA256：`ec62eb79d9968ad81257ffb64535fcd0b119720401fca2386f5fe2a36cfce71b`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "qualtrics__response", "kind": "base", "block": null, "base_tables": ["qualtrics__response"]}] | [] | ["question_text"] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |


## S109

类别 `data`；来源 `python`；调用 `5712bc62820e4dabba1fa613feda4ede`；状态 `success`。

```sql

    SELECT value, sub_question_text, question_option_key, sub_question_key,
           user_language, question_type, question_id
    FROM qualtrics__response
    WHERE sub_question_text IS NOT NULL
    LIMIT 50000

```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-081/attempt-01/sql/S109.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-081/attempt-01/sql/S109.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-081/attempt-01/results/S109.rows.jsonl)；完整：True；SHA256：`48c94aeecde1b35decc2349d61cd4b23f9e8cda95df86fec6afe2812f4daa08b`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "qualtrics__response", "kind": "base", "block": null, "base_tables": ["qualtrics__response"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |


## S110

类别 `data`；来源 `python`；调用 `b67547d11b6144b585c64d4748a94904`；状态 `success`。

```sql

    SELECT survey_id, user_language, COUNT(*) AS n, AVG(value) AS avg_v
    FROM qualtrics__response
    GROUP BY survey_id, user_language
    HAVING n >= 2

```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-081/attempt-01/sql/S110.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-081/attempt-01/sql/S110.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-081/attempt-01/results/S110.rows.jsonl)；完整：True；SHA256：`81ee9d1c30a8c9178f8a4034eaeb75f87386386552b4f0e32b740fdfa1a4efdf`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "qualtrics__response", "kind": "base", "block": null, "base_tables": ["qualtrics__response"]}] | [] | ["survey_id", "user_language"] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |
| B1 | AVG(value) | [{"table": "qualtrics__response", "column": "value"}] | [] | False |


## S111

类别 `data`；来源 `python`；调用 `2b0e3a930f85450caa4e90af3a91ab7a`；状态 `success`。

```sql

    SELECT value, user_language, contact_language, survey_id, survey_response_id,
           question_type, response_text
    FROM qualtrics__response

```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-081/attempt-01/sql/S111.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-081/attempt-01/sql/S111.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-081/attempt-01/results/S111.rows.jsonl)；完整：True；SHA256：`f5648953224d099ee2b4d7f5be9b9863c0ee09409f2461739d9257d824b43c64`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "qualtrics__response", "kind": "base", "block": null, "base_tables": ["qualtrics__response"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |


## S112

类别 `data`；来源 `python`；调用 `2b0e3a930f85450caa4e90af3a91ab7a`；状态 `success`。

```sql

    SELECT survey_id, user_language, COUNT(*) AS n, AVG(value) AS avg_v
    FROM qualtrics__response
    GROUP BY survey_id, user_language
    HAVING n >= 2

```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-081/attempt-01/sql/S112.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-081/attempt-01/sql/S112.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-081/attempt-01/results/S112.rows.jsonl)；完整：True；SHA256：`81ee9d1c30a8c9178f8a4034eaeb75f87386386552b4f0e32b740fdfa1a4efdf`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "qualtrics__response", "kind": "base", "block": null, "base_tables": ["qualtrics__response"]}] | [] | ["survey_id", "user_language"] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |
| B1 | AVG(value) | [{"table": "qualtrics__response", "column": "value"}] | [] | False |


## S113

类别 `data`；来源 `python`；调用 `2b0e3a930f85450caa4e90af3a91ab7a`；状态 `success`。

```sql
SELECT survey_name, project_category, project_type FROM qualtrics__survey WHERE survey_id = 'SUR10001791916' LIMIT 1
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-081/attempt-01/sql/S113.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-081/attempt-01/sql/S113.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-081/attempt-01/results/S113.rows.jsonl)；完整：True；SHA256：`730b0ff3cc4fa904d2f412855ce984d843a5dc5eff158ac5657927d50cf8ddc5`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "qualtrics__survey", "kind": "base", "block": null, "base_tables": ["qualtrics__survey"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |


## S114

类别 `data`；来源 `python`；调用 `2b0e3a930f85450caa4e90af3a91ab7a`；状态 `success`。

```sql
SELECT AVG(value) as avg_val, COUNT(*) as n FROM qualtrics__response WHERE survey_id = 'SUR10001791916'
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-081/attempt-01/sql/S114.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-081/attempt-01/sql/S114.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-081/attempt-01/results/S114.rows.jsonl)；完整：True；SHA256：`db08000caf59980f8c58b6c3b024c83b8e24215972e8a74592ac6537e2b9973f`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "qualtrics__response", "kind": "base", "block": null, "base_tables": ["qualtrics__response"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | AVG(value) | [{"table": "qualtrics__response", "column": "value"}] | [] | False |
| B1 | COUNT(*) | [] | [] | True |


## S115

类别 `data`；来源 `python`；调用 `ea70e3881ab74d549c70d72eacf07dd3`；状态 `success`。

```sql
SELECT survey_name, project_category, project_type, count_questions FROM qualtrics__survey WHERE survey_id = 'SUR10001791916' LIMIT 1
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-081/attempt-01/sql/S115.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-081/attempt-01/sql/S115.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-081/attempt-01/results/S115.rows.jsonl)；完整：True；SHA256：`e9071c06cbca0e6e45cfc2e3945097e55a9bf3f3d4cdfb5829e91141f666e0a6`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "qualtrics__survey", "kind": "base", "block": null, "base_tables": ["qualtrics__survey"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |


## S116

类别 `data`；来源 `python`；调用 `ea70e3881ab74d549c70d72eacf07dd3`；状态 `success`。

```sql
SELECT AVG(value) as avg_val, COUNT(*) as n FROM qualtrics__response WHERE survey_id = 'SUR10001791916'
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-081/attempt-01/sql/S116.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-081/attempt-01/sql/S116.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-081/attempt-01/results/S116.rows.jsonl)；完整：True；SHA256：`db08000caf59980f8c58b6c3b024c83b8e24215972e8a74592ac6537e2b9973f`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "qualtrics__response", "kind": "base", "block": null, "base_tables": ["qualtrics__response"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | AVG(value) | [{"table": "qualtrics__response", "column": "value"}] | [] | False |
| B1 | COUNT(*) | [] | [] | True |


## S117

类别 `data`；来源 `python`；调用 `ea70e3881ab74d549c70d72eacf07dd3`；状态 `success`。

```sql
SELECT survey_name, project_category, project_type, count_questions FROM qualtrics__survey WHERE survey_id = 'SUR10002490769' LIMIT 1
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-081/attempt-01/sql/S117.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-081/attempt-01/sql/S117.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-081/attempt-01/results/S117.rows.jsonl)；完整：True；SHA256：`1b6f1be0dc3eb4641f61558e6d238187ec45ca0bc77cb920978d47aa95b79dbb`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "qualtrics__survey", "kind": "base", "block": null, "base_tables": ["qualtrics__survey"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |


## S118

类别 `data`；来源 `python`；调用 `ea70e3881ab74d549c70d72eacf07dd3`；状态 `success`。

```sql
SELECT AVG(value) as avg_val, COUNT(*) as n FROM qualtrics__response WHERE survey_id = 'SUR10002490769'
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-081/attempt-01/sql/S118.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-081/attempt-01/sql/S118.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-081/attempt-01/results/S118.rows.jsonl)；完整：True；SHA256：`93f14ed3ab19a905e2eb1a4f7624f3068df6d08fb3106b3caa8f4d6cbf0ce1d3`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "qualtrics__response", "kind": "base", "block": null, "base_tables": ["qualtrics__response"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | AVG(value) | [{"table": "qualtrics__response", "column": "value"}] | [] | False |
| B1 | COUNT(*) | [] | [] | True |


## S119

类别 `data`；来源 `python`；调用 `ea70e3881ab74d549c70d72eacf07dd3`；状态 `success`。

```sql
SELECT survey_name, project_category, project_type, count_questions FROM qualtrics__survey WHERE survey_id = 'SUR10000172961' LIMIT 1
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-081/attempt-01/sql/S119.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-081/attempt-01/sql/S119.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-081/attempt-01/results/S119.rows.jsonl)；完整：True；SHA256：`c95cffe17af88503bcc840f71615ab6883d45094199eafcb6524acc2530c80bb`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "qualtrics__survey", "kind": "base", "block": null, "base_tables": ["qualtrics__survey"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |


## S120

类别 `data`；来源 `python`；调用 `ea70e3881ab74d549c70d72eacf07dd3`；状态 `success`。

```sql
SELECT AVG(value) as avg_val, COUNT(*) as n FROM qualtrics__response WHERE survey_id = 'SUR10000172961'
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-081/attempt-01/sql/S120.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-081/attempt-01/sql/S120.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-081/attempt-01/results/S120.rows.jsonl)；完整：True；SHA256：`31456a04c1134aa3985c56e9ee286df34866b2022300c5ac875bfe001006dc7c`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "qualtrics__response", "kind": "base", "block": null, "base_tables": ["qualtrics__response"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | AVG(value) | [{"table": "qualtrics__response", "column": "value"}] | [] | False |
| B1 | COUNT(*) | [] | [] | True |


## S121

类别 `data`；来源 `python`；调用 `ea70e3881ab74d549c70d72eacf07dd3`；状态 `success`。

```sql
SELECT survey_name, project_category, project_type, count_questions FROM qualtrics__survey WHERE survey_id = 'SUR10001778080' LIMIT 1
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-081/attempt-01/sql/S121.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-081/attempt-01/sql/S121.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-081/attempt-01/results/S121.rows.jsonl)；完整：True；SHA256：`51039849e60db0dc0e7fc964a7ec37e7b6785d9887f15be8e3061ea4118d7dd3`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "qualtrics__survey", "kind": "base", "block": null, "base_tables": ["qualtrics__survey"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |


## S122

类别 `data`；来源 `python`；调用 `ea70e3881ab74d549c70d72eacf07dd3`；状态 `success`。

```sql
SELECT AVG(value) as avg_val, COUNT(*) as n FROM qualtrics__response WHERE survey_id = 'SUR10001778080'
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-081/attempt-01/sql/S122.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-081/attempt-01/sql/S122.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-081/attempt-01/results/S122.rows.jsonl)；完整：True；SHA256：`d8ab56c44451bb8e7934db652c0f597c58fa4c9152cf9c9baa2d4a00dbfa03cd`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "qualtrics__response", "kind": "base", "block": null, "base_tables": ["qualtrics__response"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | AVG(value) | [{"table": "qualtrics__response", "column": "value"}] | [] | False |
| B1 | COUNT(*) | [] | [] | True |

