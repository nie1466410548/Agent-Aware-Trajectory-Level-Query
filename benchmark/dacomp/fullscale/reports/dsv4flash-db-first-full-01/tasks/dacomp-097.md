# dacomp-097

Using conversation, user profile, and usage event data from the past six months, compare t…

运行：已提交。官方未评分。全部 SQL 尝试/成功 113/110；数据 SQL 108/106；Python 5 次。

完整原题：

Using conversation, user profile, and usage event data from the past six months, compare the structural differences in Intercom conversation and product usage behavior among paying customers. The analysis should be sliced by customer segmentation (new_contract/renewal/churn_watch) and account size (seat count, annual contract value).

Calculate the following metrics:
- Message Response Delay = `first_response_at` − `initiated_at` (in minutes)
- First Response Bot Ratio = Count of conversations where responder_type = 'bot' ÷ Total conversations
- Conversation-to-Feature-Usage Conversion Rate = Number of customers with a feature event within 72 hours after a conversation ends ÷ Total customers
- Weekly/Monthly Retention Rate = Percentage of active customers in the current week/month who remain active in the next week/month (where 'active' is defined as having ≥1 core feature event).

The analysis must unify timezones and exclude outlier conversations (response time/duration > P99 or < P1). The output should be a reproducible metrics dashboard. The conclusion should focus on identifying key operational touchpoints and feature paths that can enhance the long-term activity of high-value customers.

| 表 | 行数 | 列数 |
| --- | --- | --- |
| intercom__company_enhanced | 2509 | 14 |
| intercom__company_metrics | 2509 | 25 |
| intercom__contact_enhanced | 2707 | 22 |
| intercom__conversation_enhanced | 6703 | 30 |
| intercom__conversation_metrics | 6703 | 40 |


实际路线（分析者依据 SQL/源码概括，不代表 Agent 自述）：SQL 连接、窗口和指标提取 → Python 业务聚合、统计检验与图表 → 报告

数据库大小：11,137,024 字节。

## 数据 SQL

| SQL | 状态 | 基础表 | Join 输入/类型 | GROUP BY | 聚合表达式 | 结果行数 | 数据库 ms |
| --- | --- | --- | --- | --- | --- | --- | --- |
| [S4/Q1](#s4) | success | ["intercom__company_enhanced"] | 0 / {} | [] | [] | 5 | 0.366 |
| [S5/Q2](#s5) | success | ["intercom__company_metrics"] | 0 / {} | [] | [] | 5 | 0.554 |
| [S6/Q3](#s6) | success | ["intercom__conversation_metrics"] | 0 / {} | [] | [] | 5 | 0.48 |
| [S7/Q4](#s7) | success | ["intercom__contact_enhanced"] | 0 / {} | [] | [] | 5 | 0.418 |
| [S8/Q5](#s8) | success | ["intercom__conversation_metrics"] | 0 / {} | [] | ["MIN(conversation_created_at)", "MAX(conversation_created_at)"] | 1 | 3.153 |
| [S9/Q6](#s9) | success | ["intercom__company_enhanced"] | 0 / {} | [] | [] | 16 | 1.842 |
| [S10/Q7](#s10) | success | ["intercom__company_enhanced"] | 0 / {} | [] | ["COUNT(*)"] | 1 | 0.375 |
| [S11/Q8](#s11) | success | ["intercom__conversation_metrics"] | 0 / {} | [] | ["COUNT(*)"] | 1 | 1.875 |
| [S12/Q9](#s12) | success | ["intercom__conversation_metrics"] | 0 / {} | [] | [] | 2 | 3.38 |
| [S13/Q10](#s13) | success | ["intercom__conversation_metrics"] | 0 / {} | [] | [] | 2 | 3.014 |
| [S15/Q11](#s15) | success | ["intercom__company_enhanced"] | 0 / {} | [] | [] | 16 | 1.383 |
| [S16/Q12](#s16) | success | ["intercom__contact_enhanced"] | 0 / {} | [] | [] | 16 | 1.358 |
| [S17/Q13](#s17) | success | ["intercom__company_enhanced"] | 0 / {} | [] | [] | 20 | 0.525 |
| [S18/Q14](#s18) | success | ["intercom__company_enhanced"] | 0 / {} | ["segment"] | ["COUNT(*)"] | 4 | 2.692 |
| [S19/Q15](#s19) | success | ["intercom__company_enhanced"] | 0 / {} | ["seat_bucket"] | ["COUNT(*)"] | 5 | 3.007 |
| [S20/Q16](#s20) | success | ["intercom__company_enhanced"] | 0 / {} | ["arr_bucket"] | ["COUNT(*)"] | 5 | 3.152 |
| [S21/Q17](#s21) | success | ["intercom__conversation_enhanced"] | 0 / {} | [] | [] | 20 | 0.377 |
| [S22/Q18](#s22) | success | ["intercom__conversation_enhanced"] | 0 / {} | [] | [] | 30 | 0.343 |
| [S23/Q19](#s23) | success | ["intercom__conversation_enhanced"] | 0 / {} | [] | [] | 3 | 3.08 |
| [S24/Q20](#s24) | success | ["intercom__conversation_enhanced"] | 0 / {} | [] | [] | 4 | 3.534 |
| [S25/Q21](#s25) | success | ["intercom__conversation_enhanced"] | 0 / {} | [] | [] | 20 | 0.334 |
| [S26/Q22](#s26) | success | ["intercom__company_enhanced"] | 0 / {} | [] | [] | 20 | 0.326 |
| [S27/Q23](#s27) | success | ["intercom__conversation_enhanced"] | 0 / {} | [] | [] | 10 | 0.303 |
| [S28/Q24](#s28) | success | ["intercom__contact_enhanced"] | 0 / {} | [] | [] | 20 | 0.322 |
| [S29/Q25](#s29) | success | ["intercom__conversation_enhanced"] | 0 / {} | [] | ["COUNT(DISTINCT all_contact_company_names)"] | 1 | 5.958 |
| [S30/Q26](#s30) | success | ["intercom__company_enhanced"] | 0 / {} | [] | ["COUNT(DISTINCT company_name)"] | 1 | 2.49 |
| [S31/Q27](#s31) | success | ["intercom__contact_enhanced"] | 0 / {} | [] | ["COUNT(DISTINCT all_contact_company_names)"] | 1 | 2.936 |
| [S32/Q28](#s32) | success | ["intercom__conversation_enhanced"] | 0 / {} | ["all_contact_company_names"] | ["COUNT(*)", "COUNT(*)"] | 30 | 5.763 |
| [S33/Q29](#s33) | success | ["intercom__contact_enhanced", "intercom__conversation_enhanced"] | 0 / {} | [] | ["COUNT(*)"] | 1 | 9.612 |
| [S34/Q30](#s34) | success | ["intercom__company_enhanced", "intercom__conversation_enhanced"] | 0 / {} | [] | ["COUNT(*)"] | 1 | 9.149 |
| [S35/Q31](#s35) | success | ["intercom__company_enhanced", "intercom__contact_enhanced", "intercom__conversation_enhanced"] | 0 / {} | [] | ["COUNT(DISTINCT all_contact_company_names)", "COUNT(DISTINCT company_name)", "COUNT(DISTINCT all_contact_company_names)"] | 3 | 10.288 |
| [S36/Q32](#s36) | success | ["intercom__company_enhanced", "intercom__contact_enhanced"] | 0 / {} | [] | ["COUNT(*)"] | 1 | 6.238 |
| [S37/Q33](#s37) | success | ["intercom__company_enhanced", "intercom__contact_enhanced"] | 2 / {'INNER': 1} | [] | ["COUNT(*)"] | 1 | 4.829 |
| [S38/Q34](#s38) | success | ["intercom__contact_enhanced"] | 0 / {} | ["all_contact_company_names"] | ["COUNT(DISTINCT contact_id)"] | 10 | 3.127 |
| [S39/Q35](#s39) | success | ["intercom__conversation_metrics"] | 0 / {} | [] | ["MIN(conversation_created_at)", "MAX(conversation_created_at)", "COUNT(*)", "SUM(CASE WHEN conversation_author_type = 'bot' THEN 1 ELSE 0 END)", "SUM(CASE WHEN conversation_author_type = 'contact' THEN 1 ELSE 0 END)"] | 1 | 3.67 |
| [S40/Q36](#s40) | success | ["intercom__conversation_enhanced"] | 0 / {} | ["CASE WHEN all_conversation_tags LIKE '%first_response:bot%' THEN 'bot' ELSE 'human' END"] | ["COUNT(*)"] | 2 | 6.49 |
| [S41/Q37](#s41) | success | ["intercom__conversation_metrics"] | 0 / {} | [] | ["COUNT(*)", "AVG(time_to_first_response_minutes)", "MIN(time_to_first_response_minutes)", "MAX(time_to_first_response_minutes)"] | 1 | 3.392 |
| [S42/Q38](#s42) | success | ["intercom__conversation_metrics"] | 0 / {} | [] | ["MIN(resp_time)", "MIN(resp_time)", "MIN(duration)", "MIN(duration)"] | 1 | 22.767 |
| [S43/Q39](#s43) | success | ["intercom__conversation_metrics"] | 0 / {} | [] | ["COUNT(*)", "SUM(CASE WHEN time_to_first_response_minutes IS NULL THEN 1 ELSE 0 END)", "SUM(CASE WHEN time_to_last_close_minutes IS NULL THEN 1 ELSE 0 END)", "SUM(CASE WHEN time_to_first_close_minutes IS NULL THEN 1 ELSE 0 END)"] | 1 | 3.553 |
| [S44/Q40](#s44) | success | ["intercom__conversation_metrics"] | 0 / {} | [] | ["SUM(CASE WHEN time_to_first_response_minutes < 11 OR time_to_first_response_minutes > 42 THEN 1 ELSE 0 END)", "SUM(CASE WHEN time_to_last_close_minutes < 91 OR time_to_last_close_minutes > 1030 THEN 1 ELSE 0 END)"] | 1 | 3.636 |
| [S45/Q41](#s45) | success | ["intercom__conversation_enhanced", "intercom__conversation_metrics"] | 2 / {'LEFT': 1} | [] | ["COUNT(*)"] | 1 | 12.815 |
| [S46/Q42](#s46) | success | ["intercom__conversation_metrics"] | 0 / {} | [] | ["COUNT(*)"] | 1 | 2.025 |
| [S47/Q43](#s47) | success | ["intercom__contact_enhanced"] | 0 / {} | [] | ["MIN(last_activity_ts)", "MAX(last_activity_ts)", "COUNT(*)"] | 1 | 1.388 |
| [S48/Q44](#s48) | success | ["intercom__contact_enhanced"] | 0 / {} | [] | ["SUM(is_active_1d)", "SUM(is_active_7d)", "SUM(is_active_30d)", "SUM(retained_7d)", "SUM(retained_30d)", "COUNT(*)"] | 1 | 1.331 |
| [S49/Q45](#s49) | success | ["intercom__company_metrics"] | 0 / {} | [] | ["AVG(registration_retention_7d)", "AVG(registration_retention_30d)", "AVG(contacts_active_7d)", "AVG(contacts_active_30d)"] | 1 | 1.097 |
| [S50/Q46](#s50) | success | ["intercom__contact_enhanced"] | 0 / {} | [] | [] | 10 | 0.333 |
| [S51/Q47](#s51) | success | ["intercom__conversation_enhanced"] | 0 / {} | [] | [] | 10 | 0.356 |
| [S53/Q48](#s53) | success | ["intercom__company_enhanced", "intercom__conversation_enhanced", "intercom__conversation_metrics"] | 2 / {'INNER': 2} | ["segment"] | ["COUNT(*)", "COUNT(DISTINCT company_name)", "AVG(resp_delay)", "AVG(CASE WHEN NOT resp_delay IS NULL THEN resp_delay END)", "AVG(duration)", "COUNT(*)", "SUM(CASE WHEN all_conversation_tags LIKE '%first_response:bot%' THEN 1 ELSE 0 END)"] | 4 | 33.753 |
| [S54/Q49](#s54) | success | ["intercom__company_enhanced"] | 0 / {} | ["company_name"] | ["COUNT(*)"] | 1 | 2.087 |
| [S55/Q50](#s55) | success | ["intercom__company_enhanced", "intercom__conversation_enhanced"] | 2 / {'LEFT': 1} | [] | ["COUNT(*)"] | 1 | 15.975 |
| [S56/Q51](#s56) | success | ["intercom__company_enhanced"] | 0 / {} | [] | [] | 2 | 0.975 |
| [S57/Q52](#s57) | success | ["intercom__company_enhanced", "intercom__conversation_enhanced", "intercom__conversation_metrics"] | 2 / {'INNER': 1} | [] | ["COUNT(*)", "COUNT(DISTINCT company_name)", "AVG(resp_delay)", "AVG(duration)", "COUNT(*)", "SUM(CASE WHEN all_conversation_tags LIKE '%first_response:bot%' THEN 1 ELSE 0 END)"] | 1 | 23.808 |
| [S58/Q53](#s58) | success | ["intercom__company_enhanced", "intercom__conversation_enhanced", "intercom__conversation_metrics"] | 2 / {'INNER': 2} | ["co.segment"] | ["COUNT(*)", "COUNT(DISTINCT c.company_name)", "AVG(c.resp_delay)", "AVG(c.duration)", "COUNT(*)", "SUM(CASE WHEN c.all_conversation_tags LIKE '%first_response:bot%' THEN 1 ELSE 0 END)"] | 4 | 37.321 |
| [S59/Q54](#s59) | success | ["intercom__company_enhanced", "intercom__conversation_enhanced", "intercom__conversation_metrics"] | 2 / {'INNER': 2} | ["co.seat_bucket"] | ["COUNT(*)", "COUNT(DISTINCT c.company_name)", "AVG(c.resp_delay)", "AVG(c.duration)", "COUNT(*)", "SUM(CASE WHEN c.all_conversation_tags LIKE '%first_response:bot%' THEN 1 ELSE 0 END)"] | 5 | 38.938 |
| [S60/Q55](#s60) | success | ["intercom__company_enhanced", "intercom__conversation_enhanced", "intercom__conversation_metrics"] | 2 / {'INNER': 2} | ["co.arr_bucket"] | ["COUNT(*)", "COUNT(DISTINCT c.company_name)", "AVG(c.resp_delay)", "AVG(c.duration)", "COUNT(*)", "SUM(CASE WHEN c.all_conversation_tags LIKE '%first_response:bot%' THEN 1 ELSE 0 END)"] | 5 | 38.603 |
| [S61/Q56](#s61) | success | ["intercom__contact_enhanced", "intercom__conversation_enhanced"] | 2 / {'INNER': 1} | [] | ["COUNT(DISTINCT company_name)", "COUNT(DISTINCT company_name)", "COUNT(DISTINCT company_name)", "COUNT(DISTINCT company_name)", "COUNT(DISTINCT conv_end.company_name)"] | 1 | 19.519 |
| [S62/Q57](#s62) | success | ["intercom__company_enhanced", "intercom__contact_enhanced", "intercom__conversation_enhanced"] | 2 / {'INNER': 1} | [] | ["COUNT(*)", "COUNT(DISTINCT company_name)", "COUNT(*)", "COUNT(*)", "COUNT(*)"] | 1 | 20.637 |
| [S63/Q58](#s63) | success | ["intercom__contact_enhanced"] | 0 / {} | ["all_contact_company_names"] | ["MAX(CASE WHEN is_active_7d = 1 THEN 1 ELSE 0 END)", "MAX(CASE WHEN retained_7d = 1 THEN 1 ELSE 0 END)", "COUNT(*)", "SUM(has_active)", "SUM(has_retained)", "SUM(has_retained)", "SUM(has_active)"] | 1 | 3.74 |
| [S64/Q59](#s64) | success | ["intercom__contact_enhanced"] | 0 / {} | ["all_contact_company_names"] | ["MAX(CASE WHEN is_active_30d = 1 THEN 1 ELSE 0 END)", "MAX(CASE WHEN retained_30d = 1 THEN 1 ELSE 0 END)", "COUNT(*)", "SUM(has_active)", "SUM(has_retained)", "SUM(has_retained)", "SUM(has_active)"] | 1 | 3.419 |
| [S65/Q60](#s65) | success | ["intercom__contact_enhanced"] | 0 / {} | ["is_active_7d", "retained_7d"] | ["COUNT(*)"] | 2 | 1.549 |
| [S66/Q61](#s66) | success | ["intercom__contact_enhanced"] | 0 / {} | ["is_active_30d", "retained_30d"] | ["COUNT(*)"] | 1 | 1.495 |
| [S67/Q62](#s67) | success | ["intercom__company_metrics"] | 0 / {} | [] | ["COUNT(*)", "AVG(registration_retention_7d)", "AVG(registration_retention_30d)"] | 1 | 1.054 |
| [S68/Q63](#s68) | success | ["intercom__company_metrics"] | 0 / {} | ["ROUND(registration_retention_7d, 2)", "ROUND(registration_retention_30d, 2)"] | ["COUNT(*)"] | 20 | 3.077 |
| [S69/Q64](#s69) | success | ["intercom__company_enhanced", "intercom__company_metrics"] | 2 / {'INNER': 1} | ["cd.segment"] | ["COUNT(*)", "AVG(cm.registration_retention_7d)", "AVG(cm.registration_retention_30d)", "AVG(cm.contacts_active_7d)", "AVG(cm.contacts_active_30d)"] | 4 | 9.09 |
| [S70/Q65](#s70) | success | ["intercom__company_enhanced", "intercom__company_metrics"] | 2 / {'INNER': 1} | ["cd.seat_bucket"] | ["COUNT(*)", "AVG(cm.registration_retention_7d)", "AVG(cm.registration_retention_30d)"] | 5 | 9.296 |
| [S71/Q66](#s71) | success | ["intercom__company_enhanced", "intercom__company_metrics"] | 2 / {'INNER': 1} | ["cd.arr_bucket"] | ["COUNT(*)", "AVG(cm.registration_retention_7d)", "AVG(cm.registration_retention_30d)"] | 5 | 9.356 |
| [S72/Q67](#s72) | success | ["intercom__company_enhanced", "intercom__contact_enhanced", "intercom__conversation_enhanced"] | 3 / {'INNER': 1, 'LEFT': 2} | ["cd.segment"] | ["COUNT(DISTINCT cd.company_name)", "COUNT(DISTINCT conv.company_name)", "COUNT(DISTINCT cv.company_name)", "COUNT(DISTINCT cd.company_name)", "COUNT(DISTINCT cv.company_name)"] | 4 | 38.141 |
| [S73/Q68](#s73) | success | ["intercom__company_enhanced", "intercom__contact_enhanced", "intercom__conversation_enhanced"] | 2 / {'INNER': 1, 'LEFT': 1} | ["cd.seat_bucket"] | ["COUNT(DISTINCT cd.company_name)", "COUNT(DISTINCT cv.company_name)", "COUNT(DISTINCT cd.company_name)", "COUNT(DISTINCT cv.company_name)"] | 5 | 29.274 |
| [S74/Q69](#s74) | success | ["intercom__company_enhanced", "intercom__contact_enhanced", "intercom__conversation_enhanced"] | 2 / {'INNER': 1, 'LEFT': 1} | ["cd.arr_bucket"] | ["COUNT(DISTINCT cd.company_name)", "COUNT(DISTINCT cv.company_name)", "COUNT(DISTINCT cd.company_name)", "COUNT(DISTINCT cv.company_name)"] | 5 | 29.449 |
| [S75/Q70](#s75) | success | ["intercom__conversation_enhanced"] | 0 / {} | ["CASE WHEN all_conversation_tags LIKE '%topic:usage_insight%' THEN 'usage_insight' WHEN all_conversation_tags LIKE '%topic:onboarding%' THEN 'onboarding' WHEN all_conversation_tags LIKE '%topic:security%' THEN 'security' WHEN all_conversation_tags LIKE '%topic:billing%' THEN 'billing' WHEN all_conversation_tags LIKE '%topic:renewal%' THEN 'renewal' WHEN all_conversation_tags LIKE '%topic:adoption%' THEN 'adoption' WHEN all_conversation_tags LIKE '%topic:product%' THEN 'product' ELSE 'other' END"] | ["COUNT(*)"] | 7 | 10.205 |
| [S76/Q71](#s76) | success | ["intercom__conversation_enhanced"] | 0 / {} | ["all_conversation_tags"] | ["COUNT(*)"] | 30 | 5.704 |
| [S77/Q72](#s77) | success | ["intercom__conversation_enhanced"] | 0 / {} | [] | [] | 10 | 10.612 |
| [S78/Q73](#s78) | success | ["intercom__conversation_enhanced"] | 0 / {} | [] | [] | 3 | 11.75 |
| [S79/Q74](#s79) | success | ["intercom__conversation_enhanced"] | 0 / {} | [] | [] | 3 | 17.412 |
| [S80/Q75](#s80) | success | ["intercom__company_enhanced", "intercom__conversation_enhanced"] | 2 / {'INNER': 1} | ["co.segment", "CASE WHEN c.all_conversation_tags LIKE '%topic:onboarding%' THEN 'onboarding' WHEN c.all_conversation_tags LIKE '%topic:billing%' THEN 'billing' WHEN c.all_conversation_tags LIKE '%topic:usage_insight%' THEN 'usage_insight' WHEN c.all_conversation_tags LIKE '%topic:security%' THEN 'security' WHEN c.all_conversation_tags LIKE '%topic:renewal%' THEN 'renewal' WHEN c.all_conversation_tags LIKE '%topic:adoption%' THEN 'adoption' WHEN c.all_conversation_tags LIKE '%topic:escalation%' THEN 'escalation' WHEN c.all_conversation_tags LIKE '%topic:feature_request%' THEN 'feature_request' WHEN c.all_conversation_tags LIKE '%topic:integration%' THEN 'integration' WHEN c.all_conversation_tags LIKE '%topic:success_plan%' THEN 'success_plan' ELSE 'other' END"] | ["COUNT(*)"] | 40 | 22.405 |
| [S81/Q76](#s81) | success | ["intercom__company_enhanced", "intercom__conversation_enhanced"] | 2 / {'INNER': 1} | ["co.segment"] | ["COUNT(*)", "COUNT(*)", "COUNT(*)", "COUNT(*)", "COUNT(*)", "SUM(CASE WHEN c.all_conversation_tags LIKE '%first_response:bot%' THEN 1 ELSE 0 END)", "SUM(CASE WHEN c.all_conversation_tags LIKE '%sla:breached%' THEN 1 ELSE 0 END)", "SUM(CASE WHEN c.all_conversation_tags LIKE '%sla:met%' THEN 1 ELSE 0 END)", "SUM(CASE WHEN c.all_conversation_tags LIKE '%sla:warning%' THEN 1 ELSE 0 END)"] | 4 | 19.015 |
| [S82/Q77](#s82) | success | ["intercom__company_enhanced", "intercom__conversation_enhanced"] | 2 / {'INNER': 1} | ["co.segment"] | ["COUNT(*)", "COUNT(*)", "COUNT(*)", "SUM(CASE WHEN c.all_conversation_tags LIKE '%channel:email%' THEN 1 ELSE 0 END)", "SUM(CASE WHEN c.all_conversation_tags LIKE '%channel:messenger%' THEN 1 ELSE 0 END)", "SUM(CASE WHEN c.all_conversation_tags LIKE '%channel:product_tour%' THEN 1 ELSE 0 END)"] | 4 | 17.395 |
| [S83/Q78](#s83) | success | ["intercom__conversation_enhanced", "intercom__conversation_metrics"] | 2 / {'INNER': 1} | ["CASE WHEN all_conversation_tags LIKE '%first_response:bot%' THEN 'bot' ELSE 'human' END"] | ["COUNT(*)", "AVG(time_to_first_response_minutes)", "AVG(time_to_last_close_minutes)", "COUNT(*)", "SUM(CASE WHEN all_conversation_tags LIKE '%sla:breached%' THEN 1 ELSE 0 END)"] | 2 | 19.698 |
| [S84/Q79](#s84) | success | ["intercom__company_enhanced", "intercom__conversation_enhanced"] | 2 / {'INNER': 1} | ["CASE WHEN co.segment = 'churn_watch' AND (co.is_high_arr = 1 OR co.is_high_seats = 1) THEN 'high_value_churn_watch' WHEN co.segment = 'new_contract' AND (co.is_high_arr = 1 OR co.is_high_seats = 1) THEN 'high_value_new_contract' ELSE co.segment END", "CASE WHEN c.all_conversation_tags LIKE '%topic:onboarding%' THEN 'onboarding' WHEN c.all_conversation_tags LIKE '%topic:billing%' THEN 'billing' WHEN c.all_conversation_tags LIKE '%topic:usage_insight%' THEN 'usage_insight' WHEN c.all_conversation_tags LIKE '%topic:security%' THEN 'security' WHEN c.all_conversation_tags LIKE '%topic:renewal%' THEN 'renewal' WHEN c.all_conversation_tags LIKE '%topic:adoption%' THEN 'adoption' WHEN c.all_conversation_tags LIKE '%topic:escalation%' THEN 'escalation' WHEN c.all_conversation_tags LIKE '%topic:feature_request%' THEN 'feature_request' WHEN c.all_conversation_tags LIKE '%topic:integration%' THEN 'integration' WHEN c.all_conversation_tags LIKE '%topic:success_plan%' THEN 'success_plan' ELSE 'other' END"] | ["COUNT(*)"] | 30 | 16.397 |
| [S85/Q80](#s85) | success | ["intercom__company_enhanced", "intercom__company_metrics", "intercom__conversation_enhanced", "intercom__conversation_metrics"] | 3 / {'INNER': 3} | ["c.company_name"] | ["COUNT(*)", "AVG(c.resp_delay)", "AVG(c.duration)", "COUNT(*)", "COUNT(*)", "COUNT(*)", "COUNT(*)", "COUNT(*)", "COUNT(*)", "SUM(CASE WHEN c.all_conversation_tags LIKE '%first_response:bot%' THEN 1 ELSE 0 END)", "SUM(CASE WHEN c.all_conversation_tags LIKE '%sla:breached%' THEN 1 ELSE 0 END)", "SUM(CASE WHEN c.all_conversation_tags LIKE '%channel:product_tour%' THEN 1 ELSE 0 END)", "SUM(CASE WHEN c.all_conversation_tags LIKE '%topic:usage_insight%' THEN 1 ELSE 0 END)", "SUM(CASE WHEN c.all_conversation_tags LIKE '%topic:adoption%' THEN 1 ELSE 0 END)", "SUM(CASE WHEN c.all_conversation_tags LIKE '%topic:escalation%' THEN 1 ELSE 0 END)"] | 2324 | 51.278 |
| [S86/Q81](#s86) | success | ["intercom__company_enhanced", "intercom__company_metrics", "intercom__conversation_enhanced", "intercom__conversation_metrics"] | 3 / {'INNER': 3} | ["c.company_name"] | ["COUNT(*)", "AVG(c.resp_delay)", "AVG(c.duration)", "COUNT(*)", "COUNT(*)", "COUNT(*)", "COUNT(*)", "COUNT(*)", "COUNT(*)", "SUM(CASE WHEN c.all_conversation_tags LIKE '%first_response:bot%' THEN 1 ELSE 0 END)", "SUM(CASE WHEN c.all_conversation_tags LIKE '%sla:breached%' THEN 1 ELSE 0 END)", "SUM(CASE WHEN c.all_conversation_tags LIKE '%channel:product_tour%' THEN 1 ELSE 0 END)", "SUM(CASE WHEN c.all_conversation_tags LIKE '%topic:usage_insight%' THEN 1 ELSE 0 END)", "SUM(CASE WHEN c.all_conversation_tags LIKE '%topic:adoption%' THEN 1 ELSE 0 END)", "SUM(CASE WHEN c.all_conversation_tags LIKE '%topic:escalation%' THEN 1 ELSE 0 END)"] | 2311 | 60.139 |
| [S87/Q82](#s87) | success | ["intercom__company_enhanced", "intercom__conversation_enhanced", "intercom__conversation_metrics"] | 2 / {'INNER': 2} | ["co.segment"] | ["COUNT(*)", "COUNT(DISTINCT c.company_name)", "AVG(c.resp_delay)", "AVG(c.duration)", "COUNT(*)", "COUNT(*)", "SUM(CASE WHEN c.all_conversation_tags LIKE '%first_response:bot%' THEN 1 ELSE 0 END)", "SUM(CASE WHEN c.all_conversation_tags LIKE '%sla:breached%' THEN 1 ELSE 0 END)"] | 4 | 39.73 |
| [S88/Q83](#s88) | success | ["intercom__company_enhanced", "intercom__company_metrics"] | 2 / {'INNER': 1} | ["cd.segment"] | ["COUNT(*)", "AVG(cm.registration_retention_7d)", "AVG(cm.registration_retention_30d)"] | 4 | 8.313 |
| [S89/Q84](#s89) | success | ["intercom__company_enhanced", "intercom__contact_enhanced", "intercom__conversation_enhanced"] | 2 / {'INNER': 1, 'LEFT': 1} | ["cd.segment"] | ["COUNT(DISTINCT cd.company_name)", "COUNT(DISTINCT cv.company_name)", "COUNT(DISTINCT cd.company_name)", "COUNT(DISTINCT cv.company_name)"] | 4 | 28.504 |
| [S90/Q85](#s90) | success | ["intercom__company_enhanced", "intercom__conversation_enhanced", "intercom__conversation_metrics"] | 2 / {'INNER': 2} | ["c.company_name", "co.arr_bucket"] | ["COUNT(*)", "AVG(c.resp_delay)", "AVG(c.duration)", "COUNT(*)", "SUM(CASE WHEN c.all_conversation_tags LIKE '%first_response:bot%' THEN 1 ELSE 0 END)", "AVG(agg.num_convs)", "AVG(agg.avg_resp_delay)", "AVG(agg.avg_duration)", "AVG(agg.bot_ratio)"] | 5 | 35.014 |
| [S91/Q86](#s91) | success | ["intercom__company_enhanced", "intercom__conversation_enhanced", "intercom__conversation_metrics"] | 2 / {'INNER': 2} | ["c.company_name", "co.seat_bucket"] | ["COUNT(*)", "AVG(c.resp_delay)", "AVG(c.duration)", "COUNT(*)", "SUM(CASE WHEN c.all_conversation_tags LIKE '%first_response:bot%' THEN 1 ELSE 0 END)", "AVG(agg.num_convs)", "AVG(agg.avg_resp_delay)", "AVG(agg.avg_duration)", "AVG(agg.bot_ratio)"] | 5 | 34.13 |
| [S92/Q87](#s92) | success | ["intercom__company_enhanced", "intercom__company_metrics"] | 2 / {'INNER': 1} | ["cd.arr_bucket"] | ["AVG(cm.registration_retention_7d)", "AVG(cm.registration_retention_30d)", "AVG(cm.contacts_active_7d)", "AVG(cm.contacts_active_30d)"] | 5 | 16.394 |
| [S93/Q88](#s93) | success | ["intercom__company_enhanced", "intercom__company_metrics"] | 2 / {'INNER': 1} | ["cd.seat_bucket"] | ["AVG(cm.registration_retention_7d)", "AVG(cm.registration_retention_30d)", "AVG(cm.contacts_active_7d)", "AVG(cm.contacts_active_30d)"] | 5 | 9.919 |
| [S94/Q89](#s94) | failed | ["intercom__conversation_enhanced", "intercom__conversation_metrics"] | 2 / {'INNER': 1} | ["STRFTIME('%Y-%m', conversation_created_at)"] | ["COUNT(*)", "AVG(time_to_first_response_minutes)", "AVG(time_to_last_close_minutes)", "COUNT(*)", "SUM(CASE WHEN all_conversation_tags LIKE '%first_response:bot%' THEN 1 ELSE 0 END)"] | unknown | 未取得；调用总时长 0.219 ms |
| [S95/Q90](#s95) | failed | ["intercom__conversation_enhanced", "intercom__conversation_metrics"] | 2 / {'INNER': 1} | ["STRFTIME('%Y-%m', conversation_created_at)"] | ["COUNT(*)", "AVG(time_to_first_response_minutes)", "AVG(time_to_last_close_minutes)", "COUNT(*)", "SUM(CASE WHEN all_conversation_tags LIKE '%first_response:bot%' THEN 1 ELSE 0 END)"] | unknown | 未取得；调用总时长 0.185 ms |
| [S96/Q91](#s96) | success | ["intercom__conversation_enhanced", "intercom__conversation_metrics"] | 2 / {'INNER': 1} | ["CASE WHEN all_conversation_tags LIKE '%sla:breached%' THEN 'breached' WHEN all_conversation_tags LIKE '%sla:met%' THEN 'met' WHEN all_conversation_tags LIKE '%sla:warning%' THEN 'warning' END"] | ["COUNT(*)", "AVG(time_to_first_response_minutes)", "AVG(time_to_last_close_minutes)"] | 3 | 20.46 |
| [S97/Q92](#s97) | success | ["intercom__conversation_enhanced", "intercom__conversation_metrics"] | 2 / {'INNER': 1} | ["STRFTIME('%Y-%m', ce.conversation_created_at)"] | ["COUNT(*)", "AVG(cm.time_to_first_response_minutes)", "AVG(cm.time_to_last_close_minutes)", "COUNT(*)", "SUM(CASE WHEN ce.all_conversation_tags LIKE '%first_response:bot%' THEN 1 ELSE 0 END)"] | 6 | 25.289 |
| [S98/Q93](#s98) | success | ["intercom__conversation_enhanced"] | 0 / {} | ["CASE WHEN all_conversation_tags LIKE '%topic:onboarding%' THEN 'onboarding' WHEN all_conversation_tags LIKE '%topic:billing%' THEN 'billing' WHEN all_conversation_tags LIKE '%topic:usage_insight%' THEN 'usage_insight' WHEN all_conversation_tags LIKE '%topic:security%' THEN 'security' WHEN all_conversation_tags LIKE '%topic:renewal%' THEN 'renewal' WHEN all_conversation_tags LIKE '%topic:adoption%' THEN 'adoption' WHEN all_conversation_tags LIKE '%topic:escalation%' THEN 'escalation' WHEN all_conversation_tags LIKE '%topic:feature_request%' THEN 'feature_request' WHEN all_conversation_tags LIKE '%topic:integration%' THEN 'integration' WHEN all_conversation_tags LIKE '%topic:success_plan%' THEN 'success_plan' ELSE 'other' END"] | ["COUNT(*)", "COUNT(*)", "SUM(CASE WHEN all_conversation_tags LIKE '%first_response:bot%' THEN 1 ELSE 0 END)"] | 10 | 11.725 |
| [S99/Q94](#s99) | success | ["intercom__company_enhanced", "intercom__conversation_enhanced"] | 2 / {'INNER': 1} | ["CASE WHEN c.all_conversation_tags LIKE '%topic:onboarding%' THEN 'onboarding' WHEN c.all_conversation_tags LIKE '%topic:billing%' THEN 'billing' WHEN c.all_conversation_tags LIKE '%topic:usage_insight%' THEN 'usage_insight' WHEN c.all_conversation_tags LIKE '%topic:security%' THEN 'security' WHEN c.all_conversation_tags LIKE '%topic:renewal%' THEN 'renewal' WHEN c.all_conversation_tags LIKE '%topic:adoption%' THEN 'adoption' WHEN c.all_conversation_tags LIKE '%topic:escalation%' THEN 'escalation' WHEN c.all_conversation_tags LIKE '%topic:feature_request%' THEN 'feature_request' WHEN c.all_conversation_tags LIKE '%topic:integration%' THEN 'integration' WHEN c.all_conversation_tags LIKE '%topic:success_plan%' THEN 'success_plan' ELSE 'other' END"] | ["COUNT(*)"] | 10 | 14.365 |
| [S100/Q95](#s100) | success | ["intercom__company_enhanced", "intercom__conversation_enhanced"] | 2 / {'INNER': 1} | ["CASE WHEN c.all_conversation_tags LIKE '%topic:onboarding%' THEN 'onboarding' WHEN c.all_conversation_tags LIKE '%topic:billing%' THEN 'billing' WHEN c.all_conversation_tags LIKE '%topic:usage_insight%' THEN 'usage_insight' WHEN c.all_conversation_tags LIKE '%topic:security%' THEN 'security' WHEN c.all_conversation_tags LIKE '%topic:renewal%' THEN 'renewal' WHEN c.all_conversation_tags LIKE '%topic:adoption%' THEN 'adoption' WHEN c.all_conversation_tags LIKE '%topic:escalation%' THEN 'escalation' WHEN c.all_conversation_tags LIKE '%topic:feature_request%' THEN 'feature_request' WHEN c.all_conversation_tags LIKE '%topic:integration%' THEN 'integration' WHEN c.all_conversation_tags LIKE '%topic:success_plan%' THEN 'success_plan' ELSE 'other' END"] | ["COUNT(*)"] | 10 | 14.313 |
| [S101/Q96](#s101) | success | ["intercom__company_enhanced"] | 0 / {} | ["CASE WHEN all_company_tags LIKE '%segment:new_contract%' THEN 'new_contract' WHEN all_company_tags LIKE '%segment:renewal%' THEN 'renewal' WHEN all_company_tags LIKE '%segment:churn_watch%' THEN 'churn_watch' WHEN all_company_tags LIKE '%segment:expansion%' THEN 'expansion' ELSE 'unknown' END"] | ["COUNT(*)"] | 1 | 1.518 |
| [S102/Q97](#s102) | success | ["intercom__company_enhanced"] | 0 / {} | ["CASE WHEN all_company_tags LIKE '%segment:new_contract%' THEN 'new_contract' WHEN all_company_tags LIKE '%segment:renewal%' THEN 'renewal' WHEN all_company_tags LIKE '%segment:churn_watch%' THEN 'churn_watch' WHEN all_company_tags LIKE '%segment:expansion%' THEN 'expansion' ELSE 'unknown' END"] | ["COUNT(*)"] | 1 | 1.55 |
| [S103/Q98](#s103) | success | ["intercom__company_enhanced"] | 0 / {} | ["segment", "arr_bucket"] | ["COUNT(*)"] | 8 | 6.512 |
| [S104/Q99](#s104) | success | ["intercom__company_enhanced", "intercom__conversation_enhanced"] | 2 / {'INNER': 1} | ["co.segment", "CASE WHEN c.all_conversation_tags LIKE '%topic:onboarding%' THEN 'onboarding' WHEN c.all_conversation_tags LIKE '%topic:escalation%' THEN 'escalation' WHEN c.all_conversation_tags LIKE '%topic:adoption%' THEN 'adoption' WHEN c.all_conversation_tags LIKE '%topic:integration%' THEN 'integration' WHEN c.all_conversation_tags LIKE '%topic:feature_request%' THEN 'feature_request' WHEN c.all_conversation_tags LIKE '%topic:usage_insight%' THEN 'usage_insight' WHEN c.all_conversation_tags LIKE '%topic:renewal%' THEN 'renewal' WHEN c.all_conversation_tags LIKE '%topic:success_plan%' THEN 'success_plan' WHEN c.all_conversation_tags LIKE '%topic:security%' THEN 'security' WHEN c.all_conversation_tags LIKE '%topic:billing%' THEN 'billing' ELSE 'other' END"] | ["COUNT(*)", "COUNT(*)", "SUM(CASE WHEN c.all_conversation_tags LIKE '%first_response:bot%' THEN 1 ELSE 0 END)"] | 40 | 22.716 |
| [S105/Q100](#s105) | success | ["intercom__contact_enhanced", "intercom__conversation_enhanced"] | 2 / {'INNER': 1, 'LEFT': 1} | ["CASE WHEN c.all_conversation_tags LIKE '%topic:onboarding%' THEN 'onboarding' WHEN c.all_conversation_tags LIKE '%topic:adoption%' THEN 'adoption' WHEN c.all_conversation_tags LIKE '%topic:usage_insight%' THEN 'usage_insight' WHEN c.all_conversation_tags LIKE '%topic:integration%' THEN 'integration' WHEN c.all_conversation_tags LIKE '%topic:feature_request%' THEN 'feature_request' WHEN c.all_conversation_tags LIKE '%topic:renewal%' THEN 'renewal' WHEN c.all_conversation_tags LIKE '%topic:success_plan%' THEN 'success_plan' WHEN c.all_conversation_tags LIKE '%topic:security%' THEN 'security' WHEN c.all_conversation_tags LIKE '%topic:escalation%' THEN 'escalation' WHEN c.all_conversation_tags LIKE '%topic:billing%' THEN 'billing' ELSE 'other' END"] | ["COUNT(DISTINCT c.all_contact_company_names)", "COUNT(DISTINCT CASE WHEN NOT cv.company_name IS NULL THEN c.all_contact_company_names END)"] | 10 | 38.001 |
| [S106/Q101](#s106) | success | ["intercom__company_enhanced"] | 0 / {} | ["segment", "seat_bucket"] | ["COUNT(*)"] | 8 | 6.381 |
| [S107/Q102](#s107) | success | ["intercom__company_enhanced", "intercom__company_metrics"] | 2 / {'INNER': 1} | ["cd.size_category"] | ["COUNT(*)", "AVG(cm.registration_retention_7d)", "AVG(cm.registration_retention_30d)", "AVG(cm.contacts_active_7d)", "AVG(cm.contacts_active_30d)", "AVG(cm.total_conversations)"] | 2 | 3.8 |
| [S108/Q103](#s108) | success | ["intercom__company_enhanced", "intercom__company_metrics", "intercom__conversation_enhanced"] | 3 / {'INNER': 2} | ["ce.all_contact_company_names", "CASE WHEN cc.total_convs <= 1 THEN '0-1' WHEN cc.total_convs <= 3 THEN '2-3' WHEN cc.total_convs <= 5 THEN '4-5' ELSE '6+' END"] | ["COUNT(*)", "COUNT(*)", "AVG(cm.registration_retention_7d)", "AVG(cm.registration_retention_30d)"] | 4 | 12.453 |
| [S109/Q104](#s109) | success | ["intercom__company_enhanced", "intercom__company_metrics", "intercom__conversation_enhanced"] | 3 / {'INNER': 2} | ["ce.all_contact_company_names", "CASE WHEN cb.bot_ratio <= 0.25 THEN '0-25%' WHEN cb.bot_ratio <= 0.50 THEN '25-50%' WHEN cb.bot_ratio <= 0.75 THEN '50-75%' ELSE '75-100%' END"] | ["COUNT(*)", "COUNT(*)", "SUM(CASE WHEN ce.all_conversation_tags LIKE '%first_response:bot%' THEN 1 ELSE 0 END)", "COUNT(*)", "AVG(cm.registration_retention_7d)", "AVG(cm.registration_retention_30d)"] | 4 | 13.267 |
| [S110/Q105](#s110) | success | ["intercom__conversation_metrics"] | 0 / {} | [] | [] | 10 | 0.365 |
| [S111/Q106](#s111) | success | ["intercom__company_enhanced", "intercom__contact_enhanced", "intercom__conversation_enhanced", "intercom__conversation_metrics"] | 0 / {} | [] | ["COUNT(*)", "COUNT(DISTINCT company_name)", "COUNT(*)", "COUNT(DISTINCT all_contact_company_names)", "COUNT(*)", "COUNT(DISTINCT all_contact_company_names)"] | 1 | 10.988 |
| [S112/Q107](#s112) | success | ["intercom__company_metrics"] | 0 / {} | [] | ["AVG(registration_retention_7d)", "AVG(registration_retention_30d)", "AVG(contacts_active_7d)", "AVG(contacts_active_30d)", "AVG(total_conversations)"] | 1 | 1.094 |
| [S113/Q108](#s113) | success | ["intercom__company_enhanced", "intercom__conversation_enhanced"] | 2 / {'INNER': 1} | ["co.segment", "STRFTIME('%Y-%m', ce.conversation_created_at)"] | ["COUNT(*)"] | 24 | 17.976 |


## 元数据和设置

| SQL | 类别 | 状态 | 内容 |
| --- | --- | --- | --- |
| S1 | connection_setup | success | PRAGMA query_only=ON |
| S2 | metadata | success | SELECT name,sql FROM sqlite_master WHERE type='table' ORDER BY name |
| S3 | metadata | success | SELECT name FROM sqlite_master WHERE type='table' ORDER BY name |
| S14 | metadata | success | SELECT name FROM sqlite_master WHERE type='table' |
| S52 | unknown | failed | -- Build company dimension with parsed tags<br>CREATE TEMP VIEW company_dim AS<br>SELECT <br>  company_id,<br>  company_name,<br>  monthly_spend,<br>  user_count,<br>  CASE <br>    WHEN all_company_tags LIKE '%segment:new_contract%' THEN 'new_contract'<br>    WHEN all_company_tags LIKE '%segment:renewal%' THEN 'renewal'<br>    WHEN all_company_tags LIKE '%segment:churn_watch%' THEN 'churn_watch'<br>    WHEN all_company_tags LIKE '%segment:expansion%' THEN 'expansion'<br>    ELSE 'unknown'<br>  END AS segment,<br>  CASE <br>    WHEN all_company_tags LIKE '%seat_bucket:seats:under_60%' THEN 'under_60'<br>    WHEN all_company_tags LIKE '%seat_bucket:seats:60_129%' THEN '60_129'<br>    WHEN all_company_tags LIKE '%seat_bucket:seats:130_259%' THEN '130_259'<br>    WHEN all_company_tags LIKE '%seat_bucket:seats:260_419%' THEN '260_419'<br>    WHEN all_company_tags LIKE '%seat_bucket:seats:420_plus%' THEN '420_plus'<br>    ELSE 'unknown'<br>  END AS seat_bucket,<br>  CASE <br>    WHEN all_company_tags LIKE '%arr_bucket:arr:<30k%' THEN '<30k'<br>    WHEN all_company_tags LIKE '%arr_bucket:arr:30k_65k%' THEN '30k_65k'<br>    WHEN all_company_tags LIKE '%arr_bucket:arr:65k_110k%' THEN '65k_110k'<br>    WHEN all_company_tags LIKE '%arr_bucket:arr:110k_200k%' THEN '110k_200k'<br>    WHEN all_company_tags LIKE '%arr_bucket:arr:200k_plus%' THEN '200k_plus'<br>    ELSE 'unknown'<br>  END AS arr_bucket<br>FROM intercom__company_enhanced |


## Python 与执行位置

人工源码审查：**database_first_violation**。SQL 完成公司级连接及业务指标，但 P1 再按客户段计算话题比例均值、筛选流失关注公司并求平均留存；P2 在 Python merge 三个 SQL 汇总结果。这些分组、过滤和关系连接可由 SQL 完成。相关检验和绘图另计为统计可视化补充。 [证据](../reviews/dacomp-097.json)。

P1：Correlation analysis between conversation metrics and retention rates, as well as segment-level comparisons. This is done in Python for statistical computation and visualization.

[源码](../../../runs/dsv4flash-db-first-full-01/dacomp-097/attempt-01/python/P1.py)；[输出](../../../runs/dsv4flash-db-first-full-01/dacomp-097/attempt-01/python/P1.stdout)；[错误](../../../runs/dsv4flash-db-first-full-01/dacomp-097/attempt-01/python/P1.stderr)。检出需人工核验的 SQL 可实现操作：groupby(, .query(；不能仅凭理由判为合规。

P2：Create a comprehensive dashboard figure combining the key segment-level metrics computed in SQL, including response delay, bot ratio, retention, and conversion rate visualizations.

[源码](../../../runs/dsv4flash-db-first-full-01/dacomp-097/attempt-01/python/P2.py)；[输出](../../../runs/dsv4flash-db-first-full-01/dacomp-097/attempt-01/python/P2.stdout)；[错误](../../../runs/dsv4flash-db-first-full-01/dacomp-097/attempt-01/python/P2.stderr)。检出需人工核验的 SQL 可实现操作：.merge(, .query(, sort_values(；不能仅凭理由判为合规。

P3：Create visualizations for ARR bucket and seat bucket analysis to understand the high-value customer dynamics.

[源码](../../../runs/dsv4flash-db-first-full-01/dacomp-097/attempt-01/python/P3.py)；[输出](../../../runs/dsv4flash-db-first-full-01/dacomp-097/attempt-01/python/P3.stdout)；[错误](../../../runs/dsv4flash-db-first-full-01/dacomp-097/attempt-01/python/P3.stderr)。检出需人工核验的 SQL 可实现操作：.query(, sort_values(；不能仅凭理由判为合规。

P4：Analyze monthly conversation trends and topic-to-activity relationships to identify feature paths and operational touchpoints, using Python for aggregation and visualization.

[源码](../../../runs/dsv4flash-db-first-full-01/dacomp-097/attempt-01/python/P4.py)；[输出](../../../runs/dsv4flash-db-first-full-01/dacomp-097/attempt-01/python/P4.stdout)；[错误](../../../runs/dsv4flash-db-first-full-01/dacomp-097/attempt-01/python/P4.stderr)。检出需人工核验的 SQL 可实现操作：.query(, sort_values(；不能仅凭理由判为合规。

P5：Create the final comprehensive dashboard visualization combining all metrics into a single report figure.

[源码](../../../runs/dsv4flash-db-first-full-01/dacomp-097/attempt-01/python/P5.py)；[输出](../../../runs/dsv4flash-db-first-full-01/dacomp-097/attempt-01/python/P5.stdout)；[错误](../../../runs/dsv4flash-db-first-full-01/dacomp-097/attempt-01/python/P5.stderr)。自动源码筛查未检出预设迁出信号；这不是全面语义合规证明。

## 优化机会

已验证候选。筛选限于精确 SQL、相同自包含 CTE、相同单表完整过滤、可分解单表聚合；未覆盖任意 Join 等价和一般谓词蕴含。全部候选都是 offline，未测在线预测。

| 候选 | 类型 | 已有结果 | 覆盖 SQL | 后续次数 | 中间行数 | 验证 | 成本 |
| --- | --- | --- | --- | --- | --- | --- | --- |
| C1 | common subexpression | False | ["S58", "S69", "S72", "S80", "S81", "S82", "S87", "S88", "S89", "S104", "S113"] | 10 | 2508 | verified | Not benchmarked; correctness alone does not establish net speedup. |
| C2 | common subexpression | False | ["S58", "S59", "S60", "S87"] | 3 | unknown | not_verified_cap | Not tested |
| C3 | common subexpression | False | ["S59", "S70", "S73", "S91", "S93"] | 4 | unknown | not_verified_cap | Not tested |
| C4 | common subexpression | False | ["S60", "S71", "S74", "S90", "S92"] | 4 | unknown | not_verified_cap | Not tested |
| C5 | common subexpression | False | ["S62", "S72", "S73", "S74", "S89", "S105"] | 5 | 2707 | verified | Not benchmarked; correctness alone does not establish net speedup. |
| C6 | common subexpression | False | ["S72", "S73", "S74", "S89", "S105"] | 4 | 6703 | verified | Not benchmarked; correctness alone does not establish net speedup. |
| C7 | common subexpression | False | ["S80", "S81", "S82", "S84"] | 3 | unknown | not_verified_cap | Not tested |
| C8 | common subexpression | False | ["S85", "S103"] | 1 | unknown | not_verified_cap | Not tested |
| C9 | common subexpression | False | ["S86", "S90", "S91"] | 2 | unknown | not_verified_cap | Not tested |
| C10 | common subexpression | False | ["S108", "S109"] | 1 | unknown | not_verified_cap | Not tested |
| C11 | aggregate MV | False | ["S49", "S67", "S68", "S112"] | 3 | unknown | not_verified_cap | Not tested |
| C12 | aggregate MV | False | ["S11", "S43", "S44", "S46"] | 3 | unknown | not_verified_cap | Not tested |
| C13 | aggregate MV | False | ["S48", "S65", "S66"] | 2 | unknown | not_verified_cap | Not tested |
| C14 | aggregate MV | False | ["S32", "S40", "S75", "S76", "S98"] | 4 | unknown | not_verified_cap | Not tested |


已验证覆盖（含触发查询、候选并集去重）：15/106 条成功数据 SQL。正确性仅针对当前数据库快照；未测性能的候选不能声称已加速。

[完整 build/rewrite 与比较证据](dacomp-097.analysis.json)。

### C1：common subexpression

Identical self-contained CTE body across queries.

原查询 [S58](#s58), [S69](#s69), [S72](#s72), [S80](#s80), [S81](#s81), [S82](#s82), [S87](#s87), [S88](#s88), [S89](#s89), [S104](#s104), [S113](#s113) → 新增共享状态 C1 → 后续 10 次可复用。该构建点为事后假设，不代表 Agent 当时预知后续。

构建定义：

```sql
SELECT DISTINCT company_name, CASE WHEN all_company_tags LIKE '%segment:new_contract%' THEN 'new_contract' WHEN all_company_tags LIKE '%segment:renewal%' THEN 'renewal' WHEN all_company_tags LIKE '%segment:churn_watch%' THEN 'churn_watch' WHEN all_company_tags LIKE '%segment:expansion%' THEN 'expansion' ELSE 'unknown' END AS segment FROM intercom__company_enhanced
```

受益查询 S58 的改写示例：

```sql
/* Metrics by segment (outlier-filtered) */ WITH company_dim AS (SELECT * FROM temp.reuse_candidate), conv AS (SELECT ce.conversation_id, ce.all_contact_company_names AS company_name, cm.time_to_first_response_minutes AS resp_delay, cm.time_to_last_close_minutes AS duration, ce.all_conversation_tags FROM intercom__conversation_enhanced AS ce JOIN intercom__conversation_metrics AS cm ON ce.conversation_id = cm.conversation_id WHERE cm.time_to_last_close_minutes BETWEEN 91 AND 1030 AND cm.time_to_first_response_minutes BETWEEN 11 AND 42) SELECT co.segment, COUNT(*) AS total_convs, COUNT(DISTINCT c.company_name) AS customers, ROUND(AVG(c.resp_delay), 2) AS avg_resp_delay_min, ROUND(AVG(c.duration), 2) AS avg_duration_min, ROUND(100.0 * SUM(CASE WHEN c.all_conversation_tags LIKE '%first_response:bot%' THEN 1 ELSE 0 END) / COUNT(*), 2) AS bot_ratio_pct FROM conv AS c JOIN company_dim AS co ON c.company_name = co.company_name GROUP BY co.segment ORDER BY co.segment
```

| 原 SQL | 列名一致 | 结果一致 | 比较方法 |
| --- | --- | --- | --- |
| S58 | True | True | ordered_numeric_tolerance |
| S69 | True | True | ordered_numeric_tolerance |
| S72 | True | True | ordered_numeric_tolerance |
| S80 | True | True | ordered_numeric_tolerance |
| S81 | True | True | exact_multiset |
| S82 | True | True | exact_multiset |
| S87 | True | True | ordered_numeric_tolerance |
| S88 | True | True | ordered_numeric_tolerance |
| S89 | True | True | ordered_numeric_tolerance |
| S104 | True | True | ordered_numeric_tolerance |
| S113 | True | True | ordered_numeric_tolerance |


验证状态：verified；成本结论：Not benchmarked; correctness alone does not establish net speedup.

### C5：common subexpression

Identical self-contained CTE body across queries.

原查询 [S62](#s62), [S72](#s72), [S73](#s73), [S74](#s74), [S89](#s89), [S105](#s105) → 新增共享状态 C5 → 后续 5 次可复用。该构建点为事后假设，不代表 Agent 当时预知后续。

构建定义：

```sql
SELECT all_contact_company_names AS company_name, last_activity_ts FROM intercom__contact_enhanced WHERE NOT last_activity_ts IS NULL
```

受益查询 S62 的改写示例：

```sql
/* Conversation-to-Feature-Usage Conversion Rate - fixed */ WITH company_dim AS (SELECT DISTINCT company_name FROM intercom__company_enhanced), contacts AS (SELECT DISTINCT all_contact_company_names AS company_name FROM intercom__contact_enhanced), conv_end AS (SELECT all_contact_company_names AS company_name, last_close_at FROM intercom__conversation_enhanced WHERE NOT last_close_at IS NULL), contact_act AS (SELECT * FROM temp.reuse_candidate), converted AS (SELECT DISTINCT c.company_name FROM conv_end AS c JOIN contact_act AS a ON c.company_name = a.company_name WHERE a.last_activity_ts >= c.last_close_at AND a.last_activity_ts <= DATETIME(c.last_close_at, '+72 hours')) SELECT (SELECT COUNT(*) FROM contacts) AS total_customers, (SELECT COUNT(DISTINCT company_name) FROM conv_end) AS customers_with_convs, (SELECT COUNT(*) FROM converted) AS customers_converted, ROUND(100.0 * (SELECT COUNT(*) FROM converted) / (SELECT COUNT(*) FROM contacts), 2) AS conversion_rate_pct
```

| 原 SQL | 列名一致 | 结果一致 | 比较方法 |
| --- | --- | --- | --- |
| S62 | True | True | exact_multiset |
| S72 | True | True | ordered_numeric_tolerance |
| S73 | True | True | ordered_numeric_tolerance |
| S74 | True | True | ordered_numeric_tolerance |
| S89 | True | True | ordered_numeric_tolerance |
| S105 | True | True | ordered_numeric_tolerance |


验证状态：verified；成本结论：Not benchmarked; correctness alone does not establish net speedup.

### C6：common subexpression

Identical self-contained CTE body across queries.

原查询 [S72](#s72), [S73](#s73), [S74](#s74), [S89](#s89), [S105](#s105) → 新增共享状态 C6 → 后续 4 次可复用。该构建点为事后假设，不代表 Agent 当时预知后续。

构建定义：

```sql
SELECT DISTINCT all_contact_company_names AS company_name, last_close_at FROM intercom__conversation_enhanced WHERE NOT last_close_at IS NULL
```

受益查询 S72 的改写示例：

```sql
/* Conversion rate by segment */ WITH company_dim AS (SELECT DISTINCT company_name, CASE WHEN all_company_tags LIKE '%segment:new_contract%' THEN 'new_contract' WHEN all_company_tags LIKE '%segment:renewal%' THEN 'renewal' WHEN all_company_tags LIKE '%segment:churn_watch%' THEN 'churn_watch' WHEN all_company_tags LIKE '%segment:expansion%' THEN 'expansion' ELSE 'unknown' END AS segment FROM intercom__company_enhanced), conv_end AS (SELECT * FROM temp.reuse_candidate), contact_act AS (SELECT all_contact_company_names AS company_name, last_activity_ts FROM intercom__contact_enhanced WHERE NOT last_activity_ts IS NULL), converted AS (SELECT DISTINCT c.company_name FROM conv_end AS c JOIN contact_act AS a ON c.company_name = a.company_name WHERE a.last_activity_ts >= c.last_close_at AND a.last_activity_ts <= DATETIME(c.last_close_at, '+72 hours')) SELECT cd.segment, COUNT(DISTINCT cd.company_name) AS total_customers, COUNT(DISTINCT conv.company_name) AS customers_with_convs, COUNT(DISTINCT cv.company_name) AS customers_converted, ROUND(100.0 * COUNT(DISTINCT cv.company_name) / COUNT(DISTINCT cd.company_name), 2) AS conversion_rate_pct FROM company_dim AS cd LEFT JOIN (SELECT DISTINCT company_name FROM conv_end) AS conv ON cd.company_name = conv.company_name LEFT JOIN converted AS cv ON cd.company_name = cv.company_name GROUP BY cd.segment ORDER BY cd.segment
```

| 原 SQL | 列名一致 | 结果一致 | 比较方法 |
| --- | --- | --- | --- |
| S72 | True | True | ordered_numeric_tolerance |
| S73 | True | True | ordered_numeric_tolerance |
| S74 | True | True | ordered_numeric_tolerance |
| S89 | True | True | ordered_numeric_tolerance |
| S105 | True | True | ordered_numeric_tolerance |


验证状态：verified；成本结论：Not benchmarked; correctness alone does not establish net speedup.

结果依赖：自动记录 SQL→Python 的接口父调用，以及源码中引用归档文件的消费者；字面值相同不认定因果。模型方向选择需要人工读取消息，尚未做全面因果标注。

[原始报告](../../../runs/dsv4flash-db-first-full-01/dacomp-097/attempt-01/answer.md)；[统一消息](../../../runs/dsv4flash-db-first-full-01/dacomp-097/attempt-01/messages.jsonl)；[原始 OpenCode 事件](../../../runs/dsv4flash-db-first-full-01/dacomp-097/attempt-01/opencode.jsonl)；[SQL 引擎日志](../../../runs/dsv4flash-db-first-full-01/dacomp-097/attempt-01/sql_journal.jsonl)。

[可读报告（本地图片链接规范化）](../answers/dacomp-097.md)。原始回答保留，分析结论未改写。

## S1

类别 `connection_setup`；来源 `connection`；调用 `bc4ecc8f0cfe4f5c952c9aaa8d2d4d31`；状态 `success`。

```sql
PRAGMA query_only=ON
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-097/attempt-01/sql/S1.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-097/attempt-01/sql/S1.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-097/attempt-01/results/S1.rows.jsonl)；完整：True；SHA256：`e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`。

## S2

类别 `metadata`；来源 `list_db`；调用 `bc4ecc8f0cfe4f5c952c9aaa8d2d4d31`；状态 `success`。

```sql
SELECT name,sql FROM sqlite_master WHERE type='table' ORDER BY name
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-097/attempt-01/sql/S2.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-097/attempt-01/sql/S2.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-097/attempt-01/results/S2.rows.jsonl)；完整：True；SHA256：`8d93f0393f0a9867afa7dae889cbd8e4baa1553a42d932850ef25d713ea5dc87`。

## S3

类别 `metadata`；来源 `query_db`；调用 `bbb76bf1a53e421ab946c2447806b250`；状态 `success`。

```sql
SELECT name FROM sqlite_master WHERE type='table' ORDER BY name
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-097/attempt-01/sql/S3.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-097/attempt-01/sql/S3.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-097/attempt-01/results/S3.rows.jsonl)；完整：True；SHA256：`fa2b56eeca32debabe3deebfafca416bcacc5016d4daeb25443ec439b0061384`。

## S4

类别 `data`；来源 `query_db`；调用 `5bcc3329c07a4a9ea75c0ea7a3007996`；状态 `success`。

```sql
SELECT * FROM intercom__company_enhanced LIMIT 5
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-097/attempt-01/sql/S4.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-097/attempt-01/sql/S4.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-097/attempt-01/results/S4.rows.jsonl)；完整：True；SHA256：`c0af9023e3aa4580642143e991274517951569c19e04ff6f0dd2aa9eff63872b`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "intercom__company_enhanced", "kind": "base", "block": null, "base_tables": ["intercom__company_enhanced"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |


## S5

类别 `data`；来源 `query_db`；调用 `1ef6b7299b184608a718588a5357d8b6`；状态 `success`。

```sql
SELECT * FROM intercom__company_metrics LIMIT 5
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-097/attempt-01/sql/S5.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-097/attempt-01/sql/S5.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-097/attempt-01/results/S5.rows.jsonl)；完整：True；SHA256：`f4a9f17ae650d13ab4c566128ec7139e30c2e6731c277ce46e17817babe08318`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "intercom__company_metrics", "kind": "base", "block": null, "base_tables": ["intercom__company_metrics"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |


## S6

类别 `data`；来源 `query_db`；调用 `3a6a1bd66ba64d43b73f1d5ed5f1f6aa`；状态 `success`。

```sql
SELECT * FROM intercom__conversation_metrics LIMIT 5
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-097/attempt-01/sql/S6.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-097/attempt-01/sql/S6.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-097/attempt-01/results/S6.rows.jsonl)；完整：True；SHA256：`0429bf16d8d0f9a0576760e5330ba740f209afb1d5d120fa03b7d9b455812329`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "intercom__conversation_metrics", "kind": "base", "block": null, "base_tables": ["intercom__conversation_metrics"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |


## S7

类别 `data`；来源 `query_db`；调用 `94d50c9ed80248ca86beedd325226ba2`；状态 `success`。

```sql
SELECT * FROM intercom__contact_enhanced LIMIT 5
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-097/attempt-01/sql/S7.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-097/attempt-01/sql/S7.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-097/attempt-01/results/S7.rows.jsonl)；完整：True；SHA256：`5d6af00c290785d5d04789faa5d8812bf9b25a4863ce30f6344348f73a44b8bb`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "intercom__contact_enhanced", "kind": "base", "block": null, "base_tables": ["intercom__contact_enhanced"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |


## S8

类别 `data`；来源 `query_db`；调用 `860a9367c3264d0fa953fa8daeac28bb`；状态 `success`。

```sql
SELECT MIN(conversation_created_at), MAX(conversation_created_at) FROM intercom__conversation_metrics
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-097/attempt-01/sql/S8.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-097/attempt-01/sql/S8.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-097/attempt-01/results/S8.rows.jsonl)；完整：True；SHA256：`7f45d76c8a17b59549424d234055fcb7d0b1033a81fa3cb98702df8f7ee599f3`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "intercom__conversation_metrics", "kind": "base", "block": null, "base_tables": ["intercom__conversation_metrics"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | MIN(conversation_created_at) | [{"table": "intercom__conversation_metrics", "column": "conversation_created_at"}] | [] | False |
| B1 | MAX(conversation_created_at) | [{"table": "intercom__conversation_metrics", "column": "conversation_created_at"}] | [] | False |


## S9

类别 `data`；来源 `query_db`；调用 `83d8ea02e0614b45a49da320ec2f6f8c`；状态 `success`。

```sql
SELECT DISTINCT all_company_tags FROM intercom__company_enhanced LIMIT 20
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-097/attempt-01/sql/S9.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-097/attempt-01/sql/S9.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-097/attempt-01/results/S9.rows.jsonl)；完整：True；SHA256：`eb398db486d6e3262443a25e72e1e35141b29dca8547ec74122398dd22764480`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "intercom__company_enhanced", "kind": "base", "block": null, "base_tables": ["intercom__company_enhanced"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |


## S10

类别 `data`；来源 `query_db`；调用 `8d1f6e21257849088e086de51d9d1de9`；状态 `success`。

```sql
SELECT COUNT(*) as total_companies FROM intercom__company_enhanced
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-097/attempt-01/sql/S10.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-097/attempt-01/sql/S10.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-097/attempt-01/results/S10.rows.jsonl)；完整：True；SHA256：`b0d6d21a6709824bcb4210d15c142d9b8c0ad2fa9f4299e758bd927ce4d24ff5`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "intercom__company_enhanced", "kind": "base", "block": null, "base_tables": ["intercom__company_enhanced"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |


## S11

类别 `data`；来源 `query_db`；调用 `685410921a1c4839bd056d8e4ed3360f`；状态 `success`。

```sql
SELECT COUNT(*) as total_conversations FROM intercom__conversation_metrics
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-097/attempt-01/sql/S11.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-097/attempt-01/sql/S11.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-097/attempt-01/results/S11.rows.jsonl)；完整：True；SHA256：`20b1d17818ff06b3c178fb6a083d46fc454d428bcb3a0a8118c827db65a82b2e`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "intercom__conversation_metrics", "kind": "base", "block": null, "base_tables": ["intercom__conversation_metrics"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |


## S12

类别 `data`；来源 `query_db`；调用 `8e9224ac4e7d4b8e9820c2c44c475bf3`；状态 `success`。

```sql
SELECT DISTINCT conversation_author_type FROM intercom__conversation_metrics
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-097/attempt-01/sql/S12.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-097/attempt-01/sql/S12.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-097/attempt-01/results/S12.rows.jsonl)；完整：True；SHA256：`a4f9eedaeece0d2c9890a94400f9e06bbcbec6c305ba9d68ae663022f5934cec`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "intercom__conversation_metrics", "kind": "base", "block": null, "base_tables": ["intercom__conversation_metrics"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |


## S13

类别 `data`；来源 `query_db`；调用 `d2e419b31bd044ee8bf5740c694ec9ff`；状态 `success`。

```sql
SELECT DISTINCT conversation_initiated_type FROM intercom__conversation_metrics
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-097/attempt-01/sql/S13.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-097/attempt-01/sql/S13.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-097/attempt-01/results/S13.rows.jsonl)；完整：True；SHA256：`a09faa7615aa21c0e7fd89d0c970046df2d1c7d19ffbc84c42a11a9ba4b42010`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "intercom__conversation_metrics", "kind": "base", "block": null, "base_tables": ["intercom__conversation_metrics"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |


## S14

类别 `metadata`；来源 `query_db`；调用 `3389b33981cc484a83430a91a45e39a5`；状态 `success`。

```sql
SELECT name FROM sqlite_master WHERE type='table'
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-097/attempt-01/sql/S14.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-097/attempt-01/sql/S14.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-097/attempt-01/results/S14.rows.jsonl)；完整：True；SHA256：`e566ad688fbc9f27963de4f7f4c54573e1541412ca164ce3d22b6b91b7d7ea0e`。

## S15

类别 `data`；来源 `query_db`；调用 `df87c8c2082e49f4ab75822d82afdc93`；状态 `success`。

```sql
SELECT DISTINCT all_company_tags FROM intercom__company_enhanced WHERE all_company_tags LIKE '%segment:%'
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-097/attempt-01/sql/S15.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-097/attempt-01/sql/S15.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-097/attempt-01/results/S15.rows.jsonl)；完整：True；SHA256：`eb398db486d6e3262443a25e72e1e35141b29dca8547ec74122398dd22764480`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "intercom__company_enhanced", "kind": "base", "block": null, "base_tables": ["intercom__company_enhanced"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |


## S16

类别 `data`；来源 `query_db`；调用 `7bc37139582d477dba42dbfc584aa64b`；状态 `success`。

```sql
SELECT DISTINCT all_contact_tags FROM intercom__contact_enhanced LIMIT 20
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-097/attempt-01/sql/S16.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-097/attempt-01/sql/S16.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-097/attempt-01/results/S16.rows.jsonl)；完整：True；SHA256：`bb215712816ec1e017faa407d89882eecef5f0f24c2607e2043fe02599e6e5b9`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "intercom__contact_enhanced", "kind": "base", "block": null, "base_tables": ["intercom__contact_enhanced"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |


## S17

类别 `data`；来源 `query_db`；调用 `e08359e0047848ea8464132ab46516bd`；状态 `success`。

```sql
-- Extract segment, seat_bucket, arr_bucket from company tags
SELECT 
  company_id,
  company_name,
  CASE 
    WHEN all_company_tags LIKE '%segment:new_contract%' THEN 'new_contract'
    WHEN all_company_tags LIKE '%segment:renewal%' THEN 'renewal'
    WHEN all_company_tags LIKE '%segment:churn_watch%' THEN 'churn_watch'
    WHEN all_company_tags LIKE '%segment:expansion%' THEN 'expansion'
    ELSE 'unknown'
  END AS segment,
  CASE 
    WHEN all_company_tags LIKE '%seat_bucket:seats:under_60%' THEN 'under_60'
    WHEN all_company_tags LIKE '%seat_bucket:seats:60_129%' THEN '60_129'
    WHEN all_company_tags LIKE '%seat_bucket:seats:130_259%' THEN '130_259'
    WHEN all_company_tags LIKE '%seat_bucket:seats:260_419%' THEN '260_419'
    WHEN all_company_tags LIKE '%seat_bucket:seats:420_plus%' THEN '420_plus'
    ELSE 'unknown'
  END AS seat_bucket,
  CASE 
    WHEN all_company_tags LIKE '%arr_bucket:arr:<30k%' THEN '<30k'
    WHEN all_company_tags LIKE '%arr_bucket:arr:30k_65k%' THEN '30k_65k'
    WHEN all_company_tags LIKE '%arr_bucket:arr:65k_110k%' THEN '65k_110k'
    WHEN all_company_tags LIKE '%arr_bucket:arr:110k_200k%' THEN '110k_200k'
    WHEN all_company_tags LIKE '%arr_bucket:arr:200k_plus%' THEN '200k_plus'
    ELSE 'unknown'
  END AS arr_bucket,
  monthly_spend,
  user_count
FROM intercom__company_enhanced
LIMIT 20
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-097/attempt-01/sql/S17.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-097/attempt-01/sql/S17.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-097/attempt-01/results/S17.rows.jsonl)；完整：True；SHA256：`21a3b93e8555a1d0bd64596343e4df49b3b5e33236e596b8c198cda022cdee74`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "intercom__company_enhanced", "kind": "base", "block": null, "base_tables": ["intercom__company_enhanced"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |


## S18

类别 `data`；来源 `query_db`；调用 `bb98039b5e49469a93b04da5dedbf25d`；状态 `success`。

```sql
SELECT segment, COUNT(*) as cnt FROM (
  SELECT 
    CASE 
      WHEN all_company_tags LIKE '%segment:new_contract%' THEN 'new_contract'
      WHEN all_company_tags LIKE '%segment:renewal%' THEN 'renewal'
      WHEN all_company_tags LIKE '%segment:churn_watch%' THEN 'churn_watch'
      WHEN all_company_tags LIKE '%segment:expansion%' THEN 'expansion'
      ELSE 'unknown'
    END AS segment
  FROM intercom__company_enhanced
) GROUP BY segment
ORDER BY cnt DESC
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-097/attempt-01/sql/S18.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-097/attempt-01/sql/S18.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-097/attempt-01/results/S18.rows.jsonl)；完整：True；SHA256：`590c902c0ade6ee8781603d0839b59555f9526b49e2eaeb1ec294e3e360d1228`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "intercom__company_enhanced", "kind": "base", "block": null, "base_tables": ["intercom__company_enhanced"]}] | [] | [] |
| B2 | [{"alias": "", "kind": "derived", "block": "B1", "base_tables": ["intercom__company_enhanced"]}] | [] | ["segment"] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B2 | COUNT(*) | [] | [] | True |


## S19

类别 `data`；来源 `query_db`；调用 `ca9181c7cc8a4b4fb2014cc1bdba897e`；状态 `success`。

```sql
SELECT seat_bucket, COUNT(*) as cnt FROM (
  SELECT 
    CASE 
      WHEN all_company_tags LIKE '%seat_bucket:seats:under_60%' THEN 'under_60'
      WHEN all_company_tags LIKE '%seat_bucket:seats:60_129%' THEN '60_129'
      WHEN all_company_tags LIKE '%seat_bucket:seats:130_259%' THEN '130_259'
      WHEN all_company_tags LIKE '%seat_bucket:seats:260_419%' THEN '260_419'
      WHEN all_company_tags LIKE '%seat_bucket:seats:420_plus%' THEN '420_plus'
      ELSE 'unknown'
    END AS seat_bucket
  FROM intercom__company_enhanced
) GROUP BY seat_bucket
ORDER BY cnt DESC
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-097/attempt-01/sql/S19.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-097/attempt-01/sql/S19.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-097/attempt-01/results/S19.rows.jsonl)；完整：True；SHA256：`b54b84876e42178cb080545cd4ecb3b9f1184d837c641e432ceb8a66e595fc52`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "intercom__company_enhanced", "kind": "base", "block": null, "base_tables": ["intercom__company_enhanced"]}] | [] | [] |
| B2 | [{"alias": "", "kind": "derived", "block": "B1", "base_tables": ["intercom__company_enhanced"]}] | [] | ["seat_bucket"] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B2 | COUNT(*) | [] | [] | True |


## S20

类别 `data`；来源 `query_db`；调用 `113c8379c3474f48a08b3975afa1f893`；状态 `success`。

```sql
SELECT arr_bucket, COUNT(*) as cnt FROM (
  SELECT 
    CASE 
      WHEN all_company_tags LIKE '%arr_bucket:arr:<30k%' THEN '<30k'
      WHEN all_company_tags LIKE '%arr_bucket:arr:30k_65k%' THEN '30k_65k'
      WHEN all_company_tags LIKE '%arr_bucket:arr:65k_110k%' THEN '65k_110k'
      WHEN all_company_tags LIKE '%arr_bucket:arr:110k_200k%' THEN '110k_200k'
      WHEN all_company_tags LIKE '%arr_bucket:arr:200k_plus%' THEN '200k_plus'
      ELSE 'unknown'
    END AS arr_bucket
  FROM intercom__company_enhanced
) GROUP BY arr_bucket
ORDER BY cnt DESC
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-097/attempt-01/sql/S20.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-097/attempt-01/sql/S20.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-097/attempt-01/results/S20.rows.jsonl)；完整：True；SHA256：`bfd4fcf135399099b4cd0bf4667348be50d1510b35af94055849bb82912f8015`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "intercom__company_enhanced", "kind": "base", "block": null, "base_tables": ["intercom__company_enhanced"]}] | [] | [] |
| B2 | [{"alias": "", "kind": "derived", "block": "B1", "base_tables": ["intercom__company_enhanced"]}] | [] | ["arr_bucket"] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B2 | COUNT(*) | [] | [] | True |


## S21

类别 `data`；来源 `query_db`；调用 `20dc24d147c54381babfe21e09da6da2`；状态 `success`。

```sql
SELECT DISTINCT all_conversation_tags FROM intercom__conversation_enhanced LIMIT 20
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-097/attempt-01/sql/S21.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-097/attempt-01/sql/S21.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-097/attempt-01/results/S21.rows.jsonl)；完整：True；SHA256：`b02719acd187d5e42d94e08f54eee8975d6da72eaf9405baa2f964071969c209`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "intercom__conversation_enhanced", "kind": "base", "block": null, "base_tables": ["intercom__conversation_enhanced"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |


## S22

类别 `data`；来源 `query_db`；调用 `5a5d013e7930472e80e43ddafeb0bcd4`；状态 `success`。

```sql
SELECT DISTINCT conversation_subject FROM intercom__conversation_enhanced LIMIT 30
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-097/attempt-01/sql/S22.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-097/attempt-01/sql/S22.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-097/attempt-01/results/S22.rows.jsonl)；完整：True；SHA256：`761f112d0519920efd6cdfe5ef5572f8f623530c9b6bf17889b7627c1e0a32c9`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "intercom__conversation_enhanced", "kind": "base", "block": null, "base_tables": ["intercom__conversation_enhanced"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |


## S23

类别 `data`；来源 `query_db`；调用 `59055c15c62d47b3afc0b92e2f6ee0cb`；状态 `success`。

```sql
SELECT DISTINCT conversation_type FROM intercom__conversation_enhanced
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-097/attempt-01/sql/S23.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-097/attempt-01/sql/S23.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-097/attempt-01/results/S23.rows.jsonl)；完整：True；SHA256：`d65a95a7dc9877eb30b3995a89da7435cc5c1dd6d1c235c0eaccc6be5b722d04`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "intercom__conversation_enhanced", "kind": "base", "block": null, "base_tables": ["intercom__conversation_enhanced"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |


## S24

类别 `data`；来源 `query_db`；调用 `6a32fbc9f8ed4abdb4c8d9bb79b688fd`；状态 `success`。

```sql
SELECT DISTINCT conversation_assignee_type, conversation_author_type, conversation_initiated_type FROM intercom__conversation_enhanced
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-097/attempt-01/sql/S24.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-097/attempt-01/sql/S24.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-097/attempt-01/results/S24.rows.jsonl)；完整：True；SHA256：`1d305d3d2b6a2abad7d80552f122d7c61d2a94b02b4f4808b7bad00230fe7902`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "intercom__conversation_enhanced", "kind": "base", "block": null, "base_tables": ["intercom__conversation_enhanced"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |


## S25

类别 `data`；来源 `query_db`；调用 `e69c72f236d4471e8757a657566cb0dc`；状态 `success`。

```sql
SELECT DISTINCT all_contact_company_names FROM intercom__conversation_enhanced LIMIT 20
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-097/attempt-01/sql/S25.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-097/attempt-01/sql/S25.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-097/attempt-01/results/S25.rows.jsonl)；完整：True；SHA256：`9609c066bc3c23bd9de9b8ea69fe440f4272ba5332bf4a05eac255f719d9358a`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "intercom__conversation_enhanced", "kind": "base", "block": null, "base_tables": ["intercom__conversation_enhanced"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |


## S26

类别 `data`；来源 `query_db`；调用 `8454b606bd8c405b85aebec2f6161b68`；状态 `success`。

```sql
SELECT company_name, company_id FROM intercom__company_enhanced LIMIT 20
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-097/attempt-01/sql/S26.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-097/attempt-01/sql/S26.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-097/attempt-01/results/S26.rows.jsonl)；完整：True；SHA256：`2342cdc4c184d930a725ea52beb7c3e958925b3193e9d50d651cf82288a664f9`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "intercom__company_enhanced", "kind": "base", "block": null, "base_tables": ["intercom__company_enhanced"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |


## S27

类别 `data`；来源 `query_db`；调用 `351e72ca8ada43acadbf83f532429798`；状态 `success`。

```sql
SELECT all_conversation_contacts FROM intercom__conversation_enhanced LIMIT 10
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-097/attempt-01/sql/S27.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-097/attempt-01/sql/S27.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-097/attempt-01/results/S27.rows.jsonl)；完整：True；SHA256：`78dbe1b428651a62032bb12ad3fd30cf5cf6262694dc761a941f2bf473431d3b`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "intercom__conversation_enhanced", "kind": "base", "block": null, "base_tables": ["intercom__conversation_enhanced"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |


## S28

类别 `data`；来源 `query_db`；调用 `1f25b03c57ff4891882a5b2813594690`；状态 `success`。

```sql
SELECT contact_id, all_contact_company_names FROM intercom__contact_enhanced LIMIT 20
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-097/attempt-01/sql/S28.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-097/attempt-01/sql/S28.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-097/attempt-01/results/S28.rows.jsonl)；完整：True；SHA256：`817e8d3a6a96084ca9b461118a6b13729697224653becea8d87f4b80fd6c4048`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "intercom__contact_enhanced", "kind": "base", "block": null, "base_tables": ["intercom__contact_enhanced"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |


## S29

类别 `data`；来源 `query_db`；调用 `e1b9da40f2724447beed53b057be09ca`；状态 `success`。

```sql
SELECT COUNT(DISTINCT all_contact_company_names) FROM intercom__conversation_enhanced
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-097/attempt-01/sql/S29.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-097/attempt-01/sql/S29.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-097/attempt-01/results/S29.rows.jsonl)；完整：True；SHA256：`4370faef085093960a8ec5f14da7b955d82d41a8253322a5a66b7b600a299635`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "intercom__conversation_enhanced", "kind": "base", "block": null, "base_tables": ["intercom__conversation_enhanced"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(DISTINCT all_contact_company_names) | [{"table": "intercom__conversation_enhanced", "column": "all_contact_company_names"}] | [] | False |


## S30

类别 `data`；来源 `query_db`；调用 `6ca9e13a4e954c298efe4ad4548377cd`；状态 `success`。

```sql
SELECT COUNT(DISTINCT company_name) FROM intercom__company_enhanced
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-097/attempt-01/sql/S30.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-097/attempt-01/sql/S30.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-097/attempt-01/results/S30.rows.jsonl)；完整：True；SHA256：`c4aee7d74b221d1af4265d49654fd71089ea1210e104404a3f53c192f8c99fac`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "intercom__company_enhanced", "kind": "base", "block": null, "base_tables": ["intercom__company_enhanced"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(DISTINCT company_name) | [{"table": "intercom__company_enhanced", "column": "company_name"}] | [] | False |


## S31

类别 `data`；来源 `query_db`；调用 `23d44511431740508e2b179acff10bb4`；状态 `success`。

```sql
SELECT COUNT(DISTINCT all_contact_company_names) FROM intercom__contact_enhanced
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-097/attempt-01/sql/S31.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-097/attempt-01/sql/S31.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-097/attempt-01/results/S31.rows.jsonl)；完整：True；SHA256：`c4aee7d74b221d1af4265d49654fd71089ea1210e104404a3f53c192f8c99fac`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "intercom__contact_enhanced", "kind": "base", "block": null, "base_tables": ["intercom__contact_enhanced"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(DISTINCT all_contact_company_names) | [{"table": "intercom__contact_enhanced", "column": "all_contact_company_names"}] | [] | False |


## S32

类别 `data`；来源 `query_db`；调用 `6edb160dd1cd4f29a3a342566ea2d83b`；状态 `success`。

```sql
SELECT all_contact_company_names, COUNT(*) FROM intercom__conversation_enhanced GROUP BY all_contact_company_names ORDER BY COUNT(*) DESC LIMIT 30
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-097/attempt-01/sql/S32.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-097/attempt-01/sql/S32.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-097/attempt-01/results/S32.rows.jsonl)；完整：True；SHA256：`bac71db08ba28a637d90d52f3abee1ffb7cb2e928b9c341cc6471e746034aa62`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "intercom__conversation_enhanced", "kind": "base", "block": null, "base_tables": ["intercom__conversation_enhanced"]}] | [] | ["all_contact_company_names"] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |
| B1 | COUNT(*) | [] | [] | True |


## S33

类别 `data`；来源 `query_db`；调用 `32d4822c383b4e089760bd5be1386fa0`；状态 `success`。

```sql
SELECT COUNT(*) AS overlap_count FROM (
  SELECT DISTINCT all_contact_company_names AS cn FROM intercom__conversation_enhanced
  INTERSECT
  SELECT DISTINCT all_contact_company_names AS cn FROM intercom__contact_enhanced
)
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-097/attempt-01/sql/S33.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-097/attempt-01/sql/S33.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-097/attempt-01/results/S33.rows.jsonl)；完整：True；SHA256：`4370faef085093960a8ec5f14da7b955d82d41a8253322a5a66b7b600a299635`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "intercom__conversation_enhanced", "kind": "base", "block": null, "base_tables": ["intercom__conversation_enhanced"]}] | [] | [] |
| B2 | [{"alias": "intercom__contact_enhanced", "kind": "base", "block": null, "base_tables": ["intercom__contact_enhanced"]}] | [] | [] |
| B3 | [] | [] | [] |
| B4 | [{"alias": "", "kind": "derived", "block": "B3", "base_tables": ["intercom__contact_enhanced", "intercom__conversation_enhanced"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B4 | COUNT(*) | [] | [] | True |


## S34

类别 `data`；来源 `query_db`；调用 `581d7fd516e64a18a5b5e467db8e8a09`；状态 `success`。

```sql
SELECT COUNT(*) AS overlap_with_companies FROM (
  SELECT DISTINCT all_contact_company_names AS cn FROM intercom__conversation_enhanced
  INTERSECT
  SELECT DISTINCT company_name AS cn FROM intercom__company_enhanced
)
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-097/attempt-01/sql/S34.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-097/attempt-01/sql/S34.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-097/attempt-01/results/S34.rows.jsonl)；完整：True；SHA256：`4370faef085093960a8ec5f14da7b955d82d41a8253322a5a66b7b600a299635`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "intercom__conversation_enhanced", "kind": "base", "block": null, "base_tables": ["intercom__conversation_enhanced"]}] | [] | [] |
| B2 | [{"alias": "intercom__company_enhanced", "kind": "base", "block": null, "base_tables": ["intercom__company_enhanced"]}] | [] | [] |
| B3 | [] | [] | [] |
| B4 | [{"alias": "", "kind": "derived", "block": "B3", "base_tables": ["intercom__company_enhanced", "intercom__conversation_enhanced"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B4 | COUNT(*) | [] | [] | True |


## S35

类别 `data`；来源 `query_db`；调用 `ad92abc977ab47ee84dcb0877ba2eaea`；状态 `success`。

```sql
SELECT COUNT(DISTINCT all_contact_company_names) FROM intercom__contact_enhanced
UNION ALL
SELECT COUNT(DISTINCT company_name) FROM intercom__company_enhanced
UNION ALL
SELECT COUNT(DISTINCT all_contact_company_names) FROM intercom__conversation_enhanced
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-097/attempt-01/sql/S35.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-097/attempt-01/sql/S35.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-097/attempt-01/results/S35.rows.jsonl)；完整：True；SHA256：`95da08d40423e472bde40fd8e48717fed0dbed17a1906c77adf62b4da50b21f0`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "intercom__contact_enhanced", "kind": "base", "block": null, "base_tables": ["intercom__contact_enhanced"]}] | [] | [] |
| B2 | [{"alias": "intercom__company_enhanced", "kind": "base", "block": null, "base_tables": ["intercom__company_enhanced"]}] | [] | [] |
| B3 | [] | [] | [] |
| B4 | [{"alias": "intercom__conversation_enhanced", "kind": "base", "block": null, "base_tables": ["intercom__conversation_enhanced"]}] | [] | [] |
| B5 | [] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(DISTINCT all_contact_company_names) | [{"table": "intercom__contact_enhanced", "column": "all_contact_company_names"}] | [] | False |
| B2 | COUNT(DISTINCT company_name) | [{"table": "intercom__company_enhanced", "column": "company_name"}] | [] | False |
| B4 | COUNT(DISTINCT all_contact_company_names) | [{"table": "intercom__conversation_enhanced", "column": "all_contact_company_names"}] | [] | False |


## S36

类别 `data`；来源 `query_db`；调用 `4c028cb117b74428bf3083e0a1a9c3c3`；状态 `success`。

```sql
SELECT COUNT(*) AS overlap_contact_company FROM (
  SELECT DISTINCT all_contact_company_names AS cn FROM intercom__contact_enhanced
  INTERSECT
  SELECT DISTINCT company_name AS cn FROM intercom__company_enhanced
)
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-097/attempt-01/sql/S36.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-097/attempt-01/sql/S36.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-097/attempt-01/results/S36.rows.jsonl)；完整：True；SHA256：`c4aee7d74b221d1af4265d49654fd71089ea1210e104404a3f53c192f8c99fac`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "intercom__contact_enhanced", "kind": "base", "block": null, "base_tables": ["intercom__contact_enhanced"]}] | [] | [] |
| B2 | [{"alias": "intercom__company_enhanced", "kind": "base", "block": null, "base_tables": ["intercom__company_enhanced"]}] | [] | [] |
| B3 | [] | [] | [] |
| B4 | [{"alias": "", "kind": "derived", "block": "B3", "base_tables": ["intercom__company_enhanced", "intercom__contact_enhanced"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B4 | COUNT(*) | [] | [] | True |


## S37

类别 `data`；来源 `query_db`；调用 `bdb797302495491884385903876416dd`；状态 `success`。

```sql
-- Check if company names match exactly between contact and company tables
SELECT COUNT(*) FROM intercom__contact_enhanced c
JOIN intercom__company_enhanced co ON c.all_contact_company_names = co.company_name
LIMIT 10
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-097/attempt-01/sql/S37.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-097/attempt-01/sql/S37.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-097/attempt-01/results/S37.rows.jsonl)；完整：True；SHA256：`24b50a52385b6b7b64b21a64772828edeada4f829ea0f6e41a92f112c45eef1f`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "c", "kind": "base", "block": null, "base_tables": ["intercom__contact_enhanced"]}, {"alias": "co", "kind": "base", "block": null, "base_tables": ["intercom__company_enhanced"]}] | [{"type": "INNER", "right": "intercom__company_enhanced AS co", "on": "c.all_contact_company_names = co.company_name", "using": []}] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |


## S38

类别 `data`；来源 `query_db`；调用 `83b6ad564a1643448f8aefcd2860de6d`；状态 `success`。

```sql
-- Check if multiple contacts can belong to same company
SELECT all_contact_company_names, COUNT(DISTINCT contact_id) as contact_count
FROM intercom__contact_enhanced
GROUP BY all_contact_company_names
ORDER BY contact_count DESC
LIMIT 10
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-097/attempt-01/sql/S38.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-097/attempt-01/sql/S38.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-097/attempt-01/results/S38.rows.jsonl)；完整：True；SHA256：`f4da1ed69ffe708e1c3ebea3245e4920e91d97cf99bbad8485cd9dfff5f1a520`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "intercom__contact_enhanced", "kind": "base", "block": null, "base_tables": ["intercom__contact_enhanced"]}] | [] | ["all_contact_company_names"] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(DISTINCT contact_id) | [{"table": "intercom__contact_enhanced", "column": "contact_id"}] | [] | False |


## S39

类别 `data`；来源 `query_db`；调用 `4ce9fc05666d40cca8ef0ea07fe49e1c`；状态 `success`。

```sql
-- Check time range for past 6 months
SELECT MIN(conversation_created_at), MAX(conversation_created_at), 
       COUNT(*) as total,
       SUM(CASE WHEN conversation_author_type = 'bot' THEN 1 ELSE 0 END) as bot_convs,
       SUM(CASE WHEN conversation_author_type = 'contact' THEN 1 ELSE 0 END) as contact_convs
FROM intercom__conversation_metrics
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-097/attempt-01/sql/S39.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-097/attempt-01/sql/S39.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-097/attempt-01/results/S39.rows.jsonl)；完整：True；SHA256：`4a8de8b19d1bdbb4febffad27b2ee0d64e9a1f91325dbdc853321d465cf4f747`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "intercom__conversation_metrics", "kind": "base", "block": null, "base_tables": ["intercom__conversation_metrics"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | MIN(conversation_created_at) | [{"table": "intercom__conversation_metrics", "column": "conversation_created_at"}] | [] | False |
| B1 | MAX(conversation_created_at) | [{"table": "intercom__conversation_metrics", "column": "conversation_created_at"}] | [] | False |
| B1 | COUNT(*) | [] | [] | True |
| B1 | SUM(CASE WHEN conversation_author_type = 'bot' THEN 1 ELSE 0 END) | [] | [{"table": "intercom__conversation_metrics", "column": "conversation_author_type"}] | False |
| B1 | SUM(CASE WHEN conversation_author_type = 'contact' THEN 1 ELSE 0 END) | [] | [{"table": "intercom__conversation_metrics", "column": "conversation_author_type"}] | False |


## S40

类别 `data`；来源 `query_db`；调用 `a1b23a38efde49c0926f087fc965d1d3`；状态 `success`。

```sql
-- Check first_response:bot/human tag distribution
SELECT 
  CASE WHEN all_conversation_tags LIKE '%first_response:bot%' THEN 'bot' ELSE 'human' END as responder_type,
  COUNT(*) as cnt
FROM intercom__conversation_enhanced
GROUP BY CASE WHEN all_conversation_tags LIKE '%first_response:bot%' THEN 'bot' ELSE 'human' END
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-097/attempt-01/sql/S40.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-097/attempt-01/sql/S40.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-097/attempt-01/results/S40.rows.jsonl)；完整：True；SHA256：`2d696018c7a9ae849c44077a7e61c340cf1286604cc5aa7b38d1f59142cb9353`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "intercom__conversation_enhanced", "kind": "base", "block": null, "base_tables": ["intercom__conversation_enhanced"]}] | [] | ["CASE WHEN all_conversation_tags LIKE '%first_response:bot%' THEN 'bot' ELSE 'human' END"] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |


## S41

类别 `data`；来源 `query_db`；调用 `ac18cf4d588f4f4499639467bf7b1fc2`；状态 `success`。

```sql
-- Check time_to_first_response_minutes distribution for outlier detection
SELECT 
  COUNT(*) as total,
  AVG(time_to_first_response_minutes) as avg,
  MIN(time_to_first_response_minutes) as min_val,
  MAX(time_to_first_response_minutes) as max_val
FROM intercom__conversation_metrics
WHERE time_to_first_response_minutes IS NOT NULL
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-097/attempt-01/sql/S41.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-097/attempt-01/sql/S41.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-097/attempt-01/results/S41.rows.jsonl)；完整：True；SHA256：`061d3f0a978cdd51ac11dee0896c1536c50d221b1fdae0bca4f6c4f94a6d531e`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "intercom__conversation_metrics", "kind": "base", "block": null, "base_tables": ["intercom__conversation_metrics"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |
| B1 | AVG(time_to_first_response_minutes) | [{"table": "intercom__conversation_metrics", "column": "time_to_first_response_minutes"}] | [] | False |
| B1 | MIN(time_to_first_response_minutes) | [{"table": "intercom__conversation_metrics", "column": "time_to_first_response_minutes"}] | [] | False |
| B1 | MAX(time_to_first_response_minutes) | [{"table": "intercom__conversation_metrics", "column": "time_to_first_response_minutes"}] | [] | False |


## S42

类别 `data`；来源 `query_db`；调用 `4c7413a30fe749feb0c362594aea9642`；状态 `success`。

```sql
-- Percentile computation using window functions for outlier thresholds
WITH vals AS (
  SELECT 
    time_to_first_response_minutes AS resp_time,
    time_to_last_close_minutes AS duration
  FROM intercom__conversation_metrics
),
resp_pct AS (
  SELECT 
    resp_time,
    CUME_DIST() OVER (ORDER BY resp_time) AS cd
  FROM vals WHERE resp_time IS NOT NULL
),
dur_pct AS (
  SELECT 
    duration,
    CUME_DIST() OVER (ORDER BY duration) AS cd
  FROM vals WHERE duration IS NOT NULL
)
SELECT 
  (SELECT MIN(resp_time) FROM resp_pct WHERE cd >= 0.01) AS resp_p1,
  (SELECT MIN(resp_time) FROM resp_pct WHERE cd >= 0.99) AS resp_p99,
  (SELECT MIN(duration) FROM dur_pct WHERE cd >= 0.01) AS dur_p1,
  (SELECT MIN(duration) FROM dur_pct WHERE cd >= 0.99) AS dur_p99
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-097/attempt-01/sql/S42.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-097/attempt-01/sql/S42.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-097/attempt-01/results/S42.rows.jsonl)；完整：True；SHA256：`e5f81ed0e76cc4bee829caa92d6e95eceb010675471fb044693689ce63a5ee2e`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "intercom__conversation_metrics", "kind": "base", "block": null, "base_tables": ["intercom__conversation_metrics"]}] | [] | [] |
| B2 | [{"alias": "vals", "kind": "derived", "block": "B1", "base_tables": ["intercom__conversation_metrics"]}] | [] | [] |
| B3 | [{"alias": "vals", "kind": "derived", "block": "B1", "base_tables": ["intercom__conversation_metrics"]}] | [] | [] |
| B4 | [{"alias": "resp_pct", "kind": "derived", "block": "B2", "base_tables": ["intercom__conversation_metrics"]}] | [] | [] |
| B5 | [{"alias": "resp_pct", "kind": "derived", "block": "B2", "base_tables": ["intercom__conversation_metrics"]}] | [] | [] |
| B6 | [{"alias": "dur_pct", "kind": "derived", "block": "B3", "base_tables": ["intercom__conversation_metrics"]}] | [] | [] |
| B7 | [{"alias": "dur_pct", "kind": "derived", "block": "B3", "base_tables": ["intercom__conversation_metrics"]}] | [] | [] |
| B8 | [] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B4 | MIN(resp_time) | [{"table": "intercom__conversation_metrics", "column": "time_to_first_response_minutes"}] | [] | False |
| B5 | MIN(resp_time) | [{"table": "intercom__conversation_metrics", "column": "time_to_first_response_minutes"}] | [] | False |
| B6 | MIN(duration) | [{"table": "intercom__conversation_metrics", "column": "time_to_last_close_minutes"}] | [] | False |
| B7 | MIN(duration) | [{"table": "intercom__conversation_metrics", "column": "time_to_last_close_minutes"}] | [] | False |


未解析列血缘：[{"block": "B8", "column": "resp_time", "reason": "ambiguous_or_missing_source"}, {"block": "B8", "column": "cd", "reason": "ambiguous_or_missing_source"}, {"block": "B8", "column": "resp_time", "reason": "ambiguous_or_missing_source"}, {"block": "B8", "column": "cd", "reason": "ambiguous_or_missing_source"}, {"block": "B8", "column": "duration", "reason": "ambiguous_or_missing_source"}, {"block": "B8", "column": "cd", "reason": "ambiguous_or_missing_source"}, {"block": "B8", "column": "duration", "reason": "ambiguous_or_missing_source"}, {"block": "B8", "column": "cd", "reason": "ambiguous_or_missing_source"}]

## S43

类别 `data`；来源 `query_db`；调用 `66c7a82f966448ddb2d42e4cd993ded9`；状态 `success`。

```sql
SELECT COUNT(*), 
  SUM(CASE WHEN time_to_first_response_minutes IS NULL THEN 1 ELSE 0 END) as null_resp,
  SUM(CASE WHEN time_to_last_close_minutes IS NULL THEN 1 ELSE 0 END) as null_close,
  SUM(CASE WHEN time_to_first_close_minutes IS NULL THEN 1 ELSE 0 END) as null_first_close
FROM intercom__conversation_metrics
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-097/attempt-01/sql/S43.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-097/attempt-01/sql/S43.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-097/attempt-01/results/S43.rows.jsonl)；完整：True；SHA256：`114be97f704fc192a8e009d1095a1e01bb88ada65c8f4a385357ce76f6eb49e4`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "intercom__conversation_metrics", "kind": "base", "block": null, "base_tables": ["intercom__conversation_metrics"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |
| B1 | SUM(CASE WHEN time_to_first_response_minutes IS NULL THEN 1 ELSE 0 END) | [] | [{"table": "intercom__conversation_metrics", "column": "time_to_first_response_minutes"}] | False |
| B1 | SUM(CASE WHEN time_to_last_close_minutes IS NULL THEN 1 ELSE 0 END) | [] | [{"table": "intercom__conversation_metrics", "column": "time_to_last_close_minutes"}] | False |
| B1 | SUM(CASE WHEN time_to_first_close_minutes IS NULL THEN 1 ELSE 0 END) | [] | [{"table": "intercom__conversation_metrics", "column": "time_to_first_close_minutes"}] | False |


## S44

类别 `data`；来源 `query_db`；调用 `aa25511ca0144bcba4a9677cfd5084a4`；状态 `success`。

```sql
-- Check how many conversations fall outside P1/P99 bounds
SELECT 
  SUM(CASE WHEN time_to_first_response_minutes < 11 OR time_to_first_response_minutes > 42 THEN 1 ELSE 0 END) AS resp_outliers,
  SUM(CASE WHEN time_to_last_close_minutes < 91 OR time_to_last_close_minutes > 1030 THEN 1 ELSE 0 END) AS dur_outliers
FROM intercom__conversation_metrics
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-097/attempt-01/sql/S44.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-097/attempt-01/sql/S44.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-097/attempt-01/results/S44.rows.jsonl)；完整：True；SHA256：`fe43d0ca94486cb03cee35fd844b337f2fd5f9425bf82b894b900775b9ba7e17`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "intercom__conversation_metrics", "kind": "base", "block": null, "base_tables": ["intercom__conversation_metrics"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | SUM(CASE WHEN time_to_first_response_minutes < 11 OR time_to_first_response_minutes > 42 THEN 1 ELSE 0 END) | [] | [{"table": "intercom__conversation_metrics", "column": "time_to_first_response_minutes"}, {"table": "intercom__conversation_metrics", "column": "time_to_first_response_minutes"}] | False |
| B1 | SUM(CASE WHEN time_to_last_close_minutes < 91 OR time_to_last_close_minutes > 1030 THEN 1 ELSE 0 END) | [] | [{"table": "intercom__conversation_metrics", "column": "time_to_last_close_minutes"}, {"table": "intercom__conversation_metrics", "column": "time_to_last_close_minutes"}] | False |


## S45

类别 `data`；来源 `query_db`；调用 `b7b08ded2c45459eaee6e8f48bc59778`；状态 `success`。

```sql
-- Check conversation metrics vs enhanced join keys
SELECT COUNT(*) FROM intercom__conversation_metrics cm
LEFT JOIN intercom__conversation_enhanced ce ON cm.conversation_id = ce.conversation_id
WHERE ce.conversation_id IS NULL
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-097/attempt-01/sql/S45.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-097/attempt-01/sql/S45.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-097/attempt-01/results/S45.rows.jsonl)；完整：True；SHA256：`c14196f132c1e9be0508ae80ab52fcb3e1d3fc05880415f3dc980971df207c9e`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "cm", "kind": "base", "block": null, "base_tables": ["intercom__conversation_metrics"]}, {"alias": "ce", "kind": "base", "block": null, "base_tables": ["intercom__conversation_enhanced"]}] | [{"type": "LEFT", "right": "intercom__conversation_enhanced AS ce", "on": "cm.conversation_id = ce.conversation_id", "using": []}] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |


## S46

类别 `data`；来源 `query_db`；调用 `dba6d38016bd4071a03e266334ba6c74`；状态 `success`。

```sql
SELECT COUNT(*) FROM intercom__conversation_metrics
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-097/attempt-01/sql/S46.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-097/attempt-01/sql/S46.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-097/attempt-01/results/S46.rows.jsonl)；完整：True；SHA256：`20b1d17818ff06b3c178fb6a083d46fc454d428bcb3a0a8118c827db65a82b2e`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "intercom__conversation_metrics", "kind": "base", "block": null, "base_tables": ["intercom__conversation_metrics"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |


## S47

类别 `data`；来源 `query_db`；调用 `0557e20e398742d2ae099ae43633542e`；状态 `success`。

```sql
SELECT MIN(last_activity_ts), MAX(last_activity_ts), COUNT(*) FROM intercom__contact_enhanced
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-097/attempt-01/sql/S47.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-097/attempt-01/sql/S47.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-097/attempt-01/results/S47.rows.jsonl)；完整：True；SHA256：`c80db78318252a7005e2a8aaa99a33e045f2b3813657c3ee342c46b3fbf46b48`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "intercom__contact_enhanced", "kind": "base", "block": null, "base_tables": ["intercom__contact_enhanced"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | MIN(last_activity_ts) | [{"table": "intercom__contact_enhanced", "column": "last_activity_ts"}] | [] | False |
| B1 | MAX(last_activity_ts) | [{"table": "intercom__contact_enhanced", "column": "last_activity_ts"}] | [] | False |
| B1 | COUNT(*) | [] | [] | True |


## S48

类别 `data`；来源 `query_db`；调用 `f3567c08e451451eb703f8899b9af762`；状态 `success`。

```sql
SELECT 
  SUM(is_active_1d) as act_1d, SUM(is_active_7d) as act_7d, SUM(is_active_30d) as act_30d,
  SUM(retained_7d) as ret_7d, SUM(retained_30d) as ret_30d,
  COUNT(*) as total
FROM intercom__contact_enhanced
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-097/attempt-01/sql/S48.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-097/attempt-01/sql/S48.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-097/attempt-01/results/S48.rows.jsonl)；完整：True；SHA256：`6ca7d6ccd6b8655af34379347996a59b730464c9240b3d1d852bf21b5914b19f`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "intercom__contact_enhanced", "kind": "base", "block": null, "base_tables": ["intercom__contact_enhanced"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | SUM(is_active_1d) | [{"table": "intercom__contact_enhanced", "column": "is_active_1d"}] | [] | False |
| B1 | SUM(is_active_7d) | [{"table": "intercom__contact_enhanced", "column": "is_active_7d"}] | [] | False |
| B1 | SUM(is_active_30d) | [{"table": "intercom__contact_enhanced", "column": "is_active_30d"}] | [] | False |
| B1 | SUM(retained_7d) | [{"table": "intercom__contact_enhanced", "column": "retained_7d"}] | [] | False |
| B1 | SUM(retained_30d) | [{"table": "intercom__contact_enhanced", "column": "retained_30d"}] | [] | False |
| B1 | COUNT(*) | [] | [] | True |


## S49

类别 `data`；来源 `query_db`；调用 `45266216c4d64af385ff1b4007cd4bb7`；状态 `success`。

```sql
-- company_metrics: distribution of registration retention
SELECT 
  AVG(registration_retention_7d) as avg_ret7, AVG(registration_retention_30d) as avg_ret30,
  AVG(contacts_active_7d) as avg_act7, AVG(contacts_active_30d) as avg_act30
FROM intercom__company_metrics
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-097/attempt-01/sql/S49.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-097/attempt-01/sql/S49.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-097/attempt-01/results/S49.rows.jsonl)；完整：True；SHA256：`5b560a3a0740cc27576c5894f2623fac762b85fd0b784820593ba9b05a411422`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "intercom__company_metrics", "kind": "base", "block": null, "base_tables": ["intercom__company_metrics"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | AVG(registration_retention_7d) | [{"table": "intercom__company_metrics", "column": "registration_retention_7d"}] | [] | False |
| B1 | AVG(registration_retention_30d) | [{"table": "intercom__company_metrics", "column": "registration_retention_30d"}] | [] | False |
| B1 | AVG(contacts_active_7d) | [{"table": "intercom__company_metrics", "column": "contacts_active_7d"}] | [] | False |
| B1 | AVG(contacts_active_30d) | [{"table": "intercom__company_metrics", "column": "contacts_active_30d"}] | [] | False |


## S50

类别 `data`；来源 `query_db`；调用 `47e674b0f5f643488d42de6039aed4f3`；状态 `success`。

```sql
-- Check if contact activity timestamps can be used for feature event tracking
SELECT last_activity_ts, last_replied_ts, last_contacted_ts, last_email_clicked_ts, last_email_opened_ts
FROM intercom__contact_enhanced LIMIT 10
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-097/attempt-01/sql/S50.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-097/attempt-01/sql/S50.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-097/attempt-01/results/S50.rows.jsonl)；完整：True；SHA256：`45f34f3797b5745a25db21bd8e7c9e3eda27fd84c43991941dd136e4f91a4d79`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "intercom__contact_enhanced", "kind": "base", "block": null, "base_tables": ["intercom__contact_enhanced"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |


## S51

类别 `data`；来源 `query_db`；调用 `f08991457d514950bf3efb08eb041cc0`；状态 `success`。

```sql
-- Check the conversation enhanced table for last_close_at and first_close_at
SELECT 
  conversation_id, 
  conversation_created_at,
  first_close_at,
  last_close_at,
  first_admin_close_at,
  last_admin_close_at
FROM intercom__conversation_enhanced LIMIT 10
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-097/attempt-01/sql/S51.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-097/attempt-01/sql/S51.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-097/attempt-01/results/S51.rows.jsonl)；完整：True；SHA256：`e078e02299c9d247c80020d9a9880deae3c90d00ea74d6686bf1e911a676573b`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "intercom__conversation_enhanced", "kind": "base", "block": null, "base_tables": ["intercom__conversation_enhanced"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |


## S52

类别 `unknown`；来源 `query_db`；调用 `829be132375f4ac8b9b30018fd47057b`；状态 `failed`。

```sql
-- Build company dimension with parsed tags
CREATE TEMP VIEW company_dim AS
SELECT 
  company_id,
  company_name,
  monthly_spend,
  user_count,
  CASE 
    WHEN all_company_tags LIKE '%segment:new_contract%' THEN 'new_contract'
    WHEN all_company_tags LIKE '%segment:renewal%' THEN 'renewal'
    WHEN all_company_tags LIKE '%segment:churn_watch%' THEN 'churn_watch'
    WHEN all_company_tags LIKE '%segment:expansion%' THEN 'expansion'
    ELSE 'unknown'
  END AS segment,
  CASE 
    WHEN all_company_tags LIKE '%seat_bucket:seats:under_60%' THEN 'under_60'
    WHEN all_company_tags LIKE '%seat_bucket:seats:60_129%' THEN '60_129'
    WHEN all_company_tags LIKE '%seat_bucket:seats:130_259%' THEN '130_259'
    WHEN all_company_tags LIKE '%seat_bucket:seats:260_419%' THEN '260_419'
    WHEN all_company_tags LIKE '%seat_bucket:seats:420_plus%' THEN '420_plus'
    ELSE 'unknown'
  END AS seat_bucket,
  CASE 
    WHEN all_company_tags LIKE '%arr_bucket:arr:<30k%' THEN '<30k'
    WHEN all_company_tags LIKE '%arr_bucket:arr:30k_65k%' THEN '30k_65k'
    WHEN all_company_tags LIKE '%arr_bucket:arr:65k_110k%' THEN '65k_110k'
    WHEN all_company_tags LIKE '%arr_bucket:arr:110k_200k%' THEN '110k_200k'
    WHEN all_company_tags LIKE '%arr_bucket:arr:200k_plus%' THEN '200k_plus'
    ELSE 'unknown'
  END AS arr_bucket
FROM intercom__company_enhanced
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-097/attempt-01/sql/S52.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-097/attempt-01/sql/S52.parameters.json)。

错误：`OperationalError('attempt to write a readonly database')`。

## S53

类别 `data`；来源 `query_db`；调用 `8ed1df6d45f64542b561b8dcc623be2e`；状态 `success`。

```sql
-- Overall and segment-level metrics: response delay, bot ratio, volume
WITH company_dim AS (
  SELECT 
    company_id, company_name,
    CASE 
      WHEN all_company_tags LIKE '%segment:new_contract%' THEN 'new_contract'
      WHEN all_company_tags LIKE '%segment:renewal%' THEN 'renewal'
      WHEN all_company_tags LIKE '%segment:churn_watch%' THEN 'churn_watch'
      WHEN all_company_tags LIKE '%segment:expansion%' THEN 'expansion'
      ELSE 'unknown' END AS segment
  FROM intercom__company_enhanced
),
conv AS (
  SELECT 
    ce.conversation_id,
    ce.all_contact_company_names AS company_name,
    cm.time_to_first_response_minutes AS resp_delay,
    cm.time_to_last_close_minutes AS duration,
    ce.all_conversation_tags
  FROM intercom__conversation_enhanced ce
  JOIN intercom__conversation_metrics cm ON ce.conversation_id = cm.conversation_id
),
merged AS (
  SELECT c.*, co.segment
  FROM conv c JOIN company_dim co ON c.company_name = co.company_name
)
SELECT 
  COALESCE(segment, 'ALL') AS segment,
  COUNT(*) AS total_convs,
  COUNT(DISTINCT company_name) AS customers,
  ROUND(AVG(resp_delay),2) AS avg_resp_delay_min,
  ROUND(AVG(CASE WHEN resp_delay IS NOT NULL THEN resp_delay END),2) AS avg_resp,
  ROUND(AVG(duration),2) AS avg_duration_min,
  ROUND(100.0 * SUM(CASE WHEN all_conversation_tags LIKE '%first_response:bot%' THEN 1 ELSE 0 END) / COUNT(*), 2) AS bot_ratio_pct
FROM merged
GROUP BY segment
ORDER BY segment
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-097/attempt-01/sql/S53.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-097/attempt-01/sql/S53.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-097/attempt-01/results/S53.rows.jsonl)；完整：True；SHA256：`c7036a98f1d3d55a95cf70427dbecc77f33b1fe64c344fd3454202595302b726`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "intercom__company_enhanced", "kind": "base", "block": null, "base_tables": ["intercom__company_enhanced"]}] | [] | [] |
| B2 | [{"alias": "ce", "kind": "base", "block": null, "base_tables": ["intercom__conversation_enhanced"]}, {"alias": "cm", "kind": "base", "block": null, "base_tables": ["intercom__conversation_metrics"]}] | [{"type": "INNER", "right": "intercom__conversation_metrics AS cm", "on": "ce.conversation_id = cm.conversation_id", "using": []}] | [] |
| B3 | [{"alias": "c", "kind": "derived", "block": "B2", "base_tables": ["intercom__conversation_enhanced", "intercom__conversation_metrics"]}, {"alias": "co", "kind": "derived", "block": "B1", "base_tables": ["intercom__company_enhanced"]}] | [{"type": "INNER", "right": "company_dim AS co", "on": "c.company_name = co.company_name", "using": []}] | [] |
| B4 | [{"alias": "merged", "kind": "derived", "block": "B3", "base_tables": ["intercom__company_enhanced", "intercom__conversation_enhanced", "intercom__conversation_metrics"]}] | [] | ["segment"] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B4 | COUNT(*) | [] | [] | True |
| B4 | COUNT(DISTINCT company_name) | [{"unknown": "company_name"}] | [] | False |
| B4 | AVG(resp_delay) | [{"table": "intercom__conversation_metrics", "column": "time_to_first_response_minutes"}] | [] | False |
| B4 | AVG(CASE WHEN NOT resp_delay IS NULL THEN resp_delay END) | [{"table": "intercom__conversation_metrics", "column": "time_to_first_response_minutes"}] | [{"table": "intercom__conversation_metrics", "column": "time_to_first_response_minutes"}] | False |
| B4 | AVG(duration) | [{"table": "intercom__conversation_metrics", "column": "time_to_last_close_minutes"}] | [] | False |
| B4 | COUNT(*) | [] | [] | True |
| B4 | SUM(CASE WHEN all_conversation_tags LIKE '%first_response:bot%' THEN 1 ELSE 0 END) | [] | [{"table": "intercom__conversation_enhanced", "column": "all_conversation_tags"}] | False |


未解析列血缘：[{"block": "B3", "column": "company_name", "reason": "ambiguous_or_missing_source"}, {"block": "B3", "column": "company_name", "reason": "ambiguous_or_missing_source"}]

## S54

类别 `data`；来源 `query_db`；调用 `df460281842841488209a89a016f825b`；状态 `success`。

```sql
SELECT company_name, COUNT(*) as cnt FROM intercom__company_enhanced GROUP BY company_name HAVING cnt > 1
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-097/attempt-01/sql/S54.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-097/attempt-01/sql/S54.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-097/attempt-01/results/S54.rows.jsonl)；完整：True；SHA256：`96c1afc3917f374a23db5dce8331826172ef9588b02b6684ad2f2eb9e26c7d05`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "intercom__company_enhanced", "kind": "base", "block": null, "base_tables": ["intercom__company_enhanced"]}] | [] | ["company_name"] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |


## S55

类别 `data`；来源 `query_db`；调用 `edd1af8c4e42472583b05e507de6250c`；状态 `success`。

```sql
-- Count conversations that don't match a company
WITH conv AS (
  SELECT DISTINCT ce.conversation_id, ce.all_contact_company_names AS company_name
  FROM intercom__conversation_enhanced ce
)
SELECT COUNT(*) AS unmatched_convs
FROM conv c
LEFT JOIN intercom__company_enhanced co ON c.company_name = co.company_name
WHERE co.company_id IS NULL
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-097/attempt-01/sql/S55.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-097/attempt-01/sql/S55.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-097/attempt-01/results/S55.rows.jsonl)；完整：True；SHA256：`c14196f132c1e9be0508ae80ab52fcb3e1d3fc05880415f3dc980971df207c9e`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "ce", "kind": "base", "block": null, "base_tables": ["intercom__conversation_enhanced"]}] | [] | [] |
| B2 | [{"alias": "c", "kind": "derived", "block": "B1", "base_tables": ["intercom__conversation_enhanced"]}, {"alias": "co", "kind": "base", "block": null, "base_tables": ["intercom__company_enhanced"]}] | [{"type": "LEFT", "right": "intercom__company_enhanced AS co", "on": "c.company_name = co.company_name", "using": []}] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B2 | COUNT(*) | [] | [] | True |


## S56

类别 `data`；来源 `query_db`；调用 `286c4ae35a4b4c8298ac36a88989b3a1`；状态 `success`。

```sql
-- Check the duplicate company
SELECT * FROM intercom__company_enhanced WHERE company_name = 'North Systems Ltd'
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-097/attempt-01/sql/S56.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-097/attempt-01/sql/S56.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-097/attempt-01/results/S56.rows.jsonl)；完整：True；SHA256：`0601f6354b3f3bbdf35c26adab346fb5c2ef55425e339e55b6fdedbdc35a10fb`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "intercom__company_enhanced", "kind": "base", "block": null, "base_tables": ["intercom__company_enhanced"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |


## S57

类别 `data`；来源 `query_db`；调用 `1f0a6b28b75d4c1aba73a0badc6024d7`；状态 `success`。

```sql
-- Overall metrics with proper dedup
WITH company_dim AS (
  SELECT DISTINCT company_name,
    CASE 
      WHEN all_company_tags LIKE '%segment:new_contract%' THEN 'new_contract'
      WHEN all_company_tags LIKE '%segment:renewal%' THEN 'renewal'
      WHEN all_company_tags LIKE '%segment:churn_watch%' THEN 'churn_watch'
      WHEN all_company_tags LIKE '%segment:expansion%' THEN 'expansion'
      ELSE 'unknown' END AS segment,
    CASE 
      WHEN all_company_tags LIKE '%seat_bucket:seats:under_60%' THEN 'under_60'
      WHEN all_company_tags LIKE '%seat_bucket:seats:60_129%' THEN '60_129'
      WHEN all_company_tags LIKE '%seat_bucket:seats:130_259%' THEN '130_259'
      WHEN all_company_tags LIKE '%seat_bucket:seats:260_419%' THEN '260_419'
      WHEN all_company_tags LIKE '%seat_bucket:seats:420_plus%' THEN '420_plus'
      ELSE 'unknown' END AS seat_bucket,
    CASE 
      WHEN all_company_tags LIKE '%arr_bucket:arr:<30k%' THEN '<30k'
      WHEN all_company_tags LIKE '%arr_bucket:arr:30k_65k%' THEN '30k_65k'
      WHEN all_company_tags LIKE '%arr_bucket:arr:65k_110k%' THEN '65k_110k'
      WHEN all_company_tags LIKE '%arr_bucket:arr:110k_200k%' THEN '110k_200k'
      WHEN all_company_tags LIKE '%arr_bucket:arr:200k_plus%' THEN '200k_plus'
      ELSE 'unknown' END AS arr_bucket
  FROM intercom__company_enhanced
),
conv AS (
  SELECT 
    ce.conversation_id,
    ce.all_contact_company_names AS company_name,
    cm.time_to_first_response_minutes AS resp_delay,
    cm.time_to_last_close_minutes AS duration,
    ce.all_conversation_tags,
    cm.conversation_created_at,
    ce.last_close_at
  FROM intercom__conversation_enhanced ce
  JOIN intercom__conversation_metrics cm ON ce.conversation_id = cm.conversation_id
  WHERE cm.time_to_last_close_minutes >= 91 AND cm.time_to_last_close_minutes <= 1030
    AND cm.time_to_first_response_minutes >= 11 AND cm.time_to_first_response_minutes <= 42
)
SELECT 
  'OVERALL' AS slice_type,
  'ALL' AS slice_value,
  COUNT(*) AS total_convs,
  COUNT(DISTINCT company_name) AS total_customers,
  ROUND(AVG(resp_delay), 2) AS avg_resp_delay_min,
  ROUND(AVG(duration), 2) AS avg_duration_min,
  ROUND(100.0 * SUM(CASE WHEN all_conversation_tags LIKE '%first_response:bot%' THEN 1 ELSE 0 END) / COUNT(*), 2) AS bot_ratio_pct
FROM conv
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-097/attempt-01/sql/S57.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-097/attempt-01/sql/S57.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-097/attempt-01/results/S57.rows.jsonl)；完整：True；SHA256：`0d020030bae09f1e28ca95fd34ba4776a832ac97b04ece6cdd8a2414d64f1cdc`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "intercom__company_enhanced", "kind": "base", "block": null, "base_tables": ["intercom__company_enhanced"]}] | [] | [] |
| B2 | [{"alias": "ce", "kind": "base", "block": null, "base_tables": ["intercom__conversation_enhanced"]}, {"alias": "cm", "kind": "base", "block": null, "base_tables": ["intercom__conversation_metrics"]}] | [{"type": "INNER", "right": "intercom__conversation_metrics AS cm", "on": "ce.conversation_id = cm.conversation_id", "using": []}] | [] |
| B3 | [{"alias": "conv", "kind": "derived", "block": "B2", "base_tables": ["intercom__conversation_enhanced", "intercom__conversation_metrics"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B3 | COUNT(*) | [] | [] | True |
| B3 | COUNT(DISTINCT company_name) | [{"table": "intercom__conversation_enhanced", "column": "all_contact_company_names"}] | [] | False |
| B3 | AVG(resp_delay) | [{"table": "intercom__conversation_metrics", "column": "time_to_first_response_minutes"}] | [] | False |
| B3 | AVG(duration) | [{"table": "intercom__conversation_metrics", "column": "time_to_last_close_minutes"}] | [] | False |
| B3 | COUNT(*) | [] | [] | True |
| B3 | SUM(CASE WHEN all_conversation_tags LIKE '%first_response:bot%' THEN 1 ELSE 0 END) | [] | [{"table": "intercom__conversation_enhanced", "column": "all_conversation_tags"}] | False |


## S58

类别 `data`；来源 `query_db`；调用 `71290fcade234bab9720d3b3e5817d6e`；状态 `success`。

```sql
-- Metrics by segment (outlier-filtered)
WITH company_dim AS (
  SELECT DISTINCT company_name,
    CASE WHEN all_company_tags LIKE '%segment:new_contract%' THEN 'new_contract'
         WHEN all_company_tags LIKE '%segment:renewal%' THEN 'renewal'
         WHEN all_company_tags LIKE '%segment:churn_watch%' THEN 'churn_watch'
         WHEN all_company_tags LIKE '%segment:expansion%' THEN 'expansion'
         ELSE 'unknown' END AS segment
  FROM intercom__company_enhanced
),
conv AS (
  SELECT 
    ce.conversation_id, ce.all_contact_company_names AS company_name,
    cm.time_to_first_response_minutes AS resp_delay,
    cm.time_to_last_close_minutes AS duration,
    ce.all_conversation_tags
  FROM intercom__conversation_enhanced ce
  JOIN intercom__conversation_metrics cm ON ce.conversation_id = cm.conversation_id
  WHERE cm.time_to_last_close_minutes BETWEEN 91 AND 1030
    AND cm.time_to_first_response_minutes BETWEEN 11 AND 42
)
SELECT 
  co.segment,
  COUNT(*) AS total_convs,
  COUNT(DISTINCT c.company_name) AS customers,
  ROUND(AVG(c.resp_delay), 2) AS avg_resp_delay_min,
  ROUND(AVG(c.duration), 2) AS avg_duration_min,
  ROUND(100.0 * SUM(CASE WHEN c.all_conversation_tags LIKE '%first_response:bot%' THEN 1 ELSE 0 END) / COUNT(*), 2) AS bot_ratio_pct
FROM conv c
JOIN company_dim co ON c.company_name = co.company_name
GROUP BY co.segment
ORDER BY co.segment
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-097/attempt-01/sql/S58.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-097/attempt-01/sql/S58.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-097/attempt-01/results/S58.rows.jsonl)；完整：True；SHA256：`554ff181d496f8afcd9e943c1a747483e15cf2fbaf9519113108145c322a1b7e`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "intercom__company_enhanced", "kind": "base", "block": null, "base_tables": ["intercom__company_enhanced"]}] | [] | [] |
| B2 | [{"alias": "ce", "kind": "base", "block": null, "base_tables": ["intercom__conversation_enhanced"]}, {"alias": "cm", "kind": "base", "block": null, "base_tables": ["intercom__conversation_metrics"]}] | [{"type": "INNER", "right": "intercom__conversation_metrics AS cm", "on": "ce.conversation_id = cm.conversation_id", "using": []}] | [] |
| B3 | [{"alias": "c", "kind": "derived", "block": "B2", "base_tables": ["intercom__conversation_enhanced", "intercom__conversation_metrics"]}, {"alias": "co", "kind": "derived", "block": "B1", "base_tables": ["intercom__company_enhanced"]}] | [{"type": "INNER", "right": "company_dim AS co", "on": "c.company_name = co.company_name", "using": []}] | ["co.segment"] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B3 | COUNT(*) | [] | [] | True |
| B3 | COUNT(DISTINCT c.company_name) | [{"table": "intercom__conversation_enhanced", "column": "all_contact_company_names"}] | [] | False |
| B3 | AVG(c.resp_delay) | [{"table": "intercom__conversation_metrics", "column": "time_to_first_response_minutes"}] | [] | False |
| B3 | AVG(c.duration) | [{"table": "intercom__conversation_metrics", "column": "time_to_last_close_minutes"}] | [] | False |
| B3 | COUNT(*) | [] | [] | True |
| B3 | SUM(CASE WHEN c.all_conversation_tags LIKE '%first_response:bot%' THEN 1 ELSE 0 END) | [] | [{"table": "intercom__conversation_enhanced", "column": "all_conversation_tags"}] | False |


## S59

类别 `data`；来源 `query_db`；调用 `901e2c837c7542c298b3855004aa8e74`；状态 `success`。

```sql
-- Metrics by seat bucket
WITH company_dim AS (
  SELECT DISTINCT company_name,
    CASE WHEN all_company_tags LIKE '%seat_bucket:seats:under_60%' THEN 'under_60'
         WHEN all_company_tags LIKE '%seat_bucket:seats:60_129%' THEN '60_129'
         WHEN all_company_tags LIKE '%seat_bucket:seats:130_259%' THEN '130_259'
         WHEN all_company_tags LIKE '%seat_bucket:seats:260_419%' THEN '260_419'
         WHEN all_company_tags LIKE '%seat_bucket:seats:420_plus%' THEN '420_plus'
         ELSE 'unknown' END AS seat_bucket
  FROM intercom__company_enhanced
),
conv AS (
  SELECT 
    ce.conversation_id, ce.all_contact_company_names AS company_name,
    cm.time_to_first_response_minutes AS resp_delay,
    cm.time_to_last_close_minutes AS duration,
    ce.all_conversation_tags
  FROM intercom__conversation_enhanced ce
  JOIN intercom__conversation_metrics cm ON ce.conversation_id = cm.conversation_id
  WHERE cm.time_to_last_close_minutes BETWEEN 91 AND 1030
    AND cm.time_to_first_response_minutes BETWEEN 11 AND 42
)
SELECT 
  co.seat_bucket,
  COUNT(*) AS total_convs,
  COUNT(DISTINCT c.company_name) AS customers,
  ROUND(AVG(c.resp_delay), 2) AS avg_resp_delay_min,
  ROUND(AVG(c.duration), 2) AS avg_duration_min,
  ROUND(100.0 * SUM(CASE WHEN c.all_conversation_tags LIKE '%first_response:bot%' THEN 1 ELSE 0 END) / COUNT(*), 2) AS bot_ratio_pct
FROM conv c
JOIN company_dim co ON c.company_name = co.company_name
GROUP BY co.seat_bucket
ORDER BY co.seat_bucket
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-097/attempt-01/sql/S59.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-097/attempt-01/sql/S59.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-097/attempt-01/results/S59.rows.jsonl)；完整：True；SHA256：`7acd9a5f3f7e5a715dc998f7f4f0c2cf5eedab7384a13a15004e950321af0041`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "intercom__company_enhanced", "kind": "base", "block": null, "base_tables": ["intercom__company_enhanced"]}] | [] | [] |
| B2 | [{"alias": "ce", "kind": "base", "block": null, "base_tables": ["intercom__conversation_enhanced"]}, {"alias": "cm", "kind": "base", "block": null, "base_tables": ["intercom__conversation_metrics"]}] | [{"type": "INNER", "right": "intercom__conversation_metrics AS cm", "on": "ce.conversation_id = cm.conversation_id", "using": []}] | [] |
| B3 | [{"alias": "c", "kind": "derived", "block": "B2", "base_tables": ["intercom__conversation_enhanced", "intercom__conversation_metrics"]}, {"alias": "co", "kind": "derived", "block": "B1", "base_tables": ["intercom__company_enhanced"]}] | [{"type": "INNER", "right": "company_dim AS co", "on": "c.company_name = co.company_name", "using": []}] | ["co.seat_bucket"] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B3 | COUNT(*) | [] | [] | True |
| B3 | COUNT(DISTINCT c.company_name) | [{"table": "intercom__conversation_enhanced", "column": "all_contact_company_names"}] | [] | False |
| B3 | AVG(c.resp_delay) | [{"table": "intercom__conversation_metrics", "column": "time_to_first_response_minutes"}] | [] | False |
| B3 | AVG(c.duration) | [{"table": "intercom__conversation_metrics", "column": "time_to_last_close_minutes"}] | [] | False |
| B3 | COUNT(*) | [] | [] | True |
| B3 | SUM(CASE WHEN c.all_conversation_tags LIKE '%first_response:bot%' THEN 1 ELSE 0 END) | [] | [{"table": "intercom__conversation_enhanced", "column": "all_conversation_tags"}] | False |


## S60

类别 `data`；来源 `query_db`；调用 `b38c65c579a94bd4b870d429a88d79d8`；状态 `success`。

```sql
-- Metrics by ARR bucket
WITH company_dim AS (
  SELECT DISTINCT company_name,
    CASE WHEN all_company_tags LIKE '%arr_bucket:arr:<30k%' THEN '<30k'
         WHEN all_company_tags LIKE '%arr_bucket:arr:30k_65k%' THEN '30k_65k'
         WHEN all_company_tags LIKE '%arr_bucket:arr:65k_110k%' THEN '65k_110k'
         WHEN all_company_tags LIKE '%arr_bucket:arr:110k_200k%' THEN '110k_200k'
         WHEN all_company_tags LIKE '%arr_bucket:arr:200k_plus%' THEN '200k_plus'
         ELSE 'unknown' END AS arr_bucket
  FROM intercom__company_enhanced
),
conv AS (
  SELECT 
    ce.conversation_id, ce.all_contact_company_names AS company_name,
    cm.time_to_first_response_minutes AS resp_delay,
    cm.time_to_last_close_minutes AS duration,
    ce.all_conversation_tags
  FROM intercom__conversation_enhanced ce
  JOIN intercom__conversation_metrics cm ON ce.conversation_id = cm.conversation_id
  WHERE cm.time_to_last_close_minutes BETWEEN 91 AND 1030
    AND cm.time_to_first_response_minutes BETWEEN 11 AND 42
)
SELECT 
  co.arr_bucket,
  COUNT(*) AS total_convs,
  COUNT(DISTINCT c.company_name) AS customers,
  ROUND(AVG(c.resp_delay), 2) AS avg_resp_delay_min,
  ROUND(AVG(c.duration), 2) AS avg_duration_min,
  ROUND(100.0 * SUM(CASE WHEN c.all_conversation_tags LIKE '%first_response:bot%' THEN 1 ELSE 0 END) / COUNT(*), 2) AS bot_ratio_pct
FROM conv c
JOIN company_dim co ON c.company_name = co.company_name
GROUP BY co.arr_bucket
ORDER BY co.arr_bucket
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-097/attempt-01/sql/S60.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-097/attempt-01/sql/S60.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-097/attempt-01/results/S60.rows.jsonl)；完整：True；SHA256：`2380847fb5e6d17773958b5c9f8cad18fd6174bcd7ab6c7e4f49a7cab8063906`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "intercom__company_enhanced", "kind": "base", "block": null, "base_tables": ["intercom__company_enhanced"]}] | [] | [] |
| B2 | [{"alias": "ce", "kind": "base", "block": null, "base_tables": ["intercom__conversation_enhanced"]}, {"alias": "cm", "kind": "base", "block": null, "base_tables": ["intercom__conversation_metrics"]}] | [{"type": "INNER", "right": "intercom__conversation_metrics AS cm", "on": "ce.conversation_id = cm.conversation_id", "using": []}] | [] |
| B3 | [{"alias": "c", "kind": "derived", "block": "B2", "base_tables": ["intercom__conversation_enhanced", "intercom__conversation_metrics"]}, {"alias": "co", "kind": "derived", "block": "B1", "base_tables": ["intercom__company_enhanced"]}] | [{"type": "INNER", "right": "company_dim AS co", "on": "c.company_name = co.company_name", "using": []}] | ["co.arr_bucket"] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B3 | COUNT(*) | [] | [] | True |
| B3 | COUNT(DISTINCT c.company_name) | [{"table": "intercom__conversation_enhanced", "column": "all_contact_company_names"}] | [] | False |
| B3 | AVG(c.resp_delay) | [{"table": "intercom__conversation_metrics", "column": "time_to_first_response_minutes"}] | [] | False |
| B3 | AVG(c.duration) | [{"table": "intercom__conversation_metrics", "column": "time_to_last_close_minutes"}] | [] | False |
| B3 | COUNT(*) | [] | [] | True |
| B3 | SUM(CASE WHEN c.all_conversation_tags LIKE '%first_response:bot%' THEN 1 ELSE 0 END) | [] | [{"table": "intercom__conversation_enhanced", "column": "all_conversation_tags"}] | False |


## S61

类别 `data`；来源 `query_db`；调用 `36246ccc83184755b080154012799f2d`；状态 `success`。

```sql
-- Conversation-to-Feature-Usage Conversion Rate
-- Proxy: a company counts as converted if any contact had activity (last_activity_ts) within 72h after a conversation ended (last_close_at)
WITH conv_end AS (
  SELECT 
    all_contact_company_names AS company_name,
    conversation_id,
    julianday(last_close_at) * 24 AS close_hr,
    julianday(last_close_at) * 24 + 72 AS close_hr_72
  FROM intercom__conversation_enhanced
  WHERE last_close_at IS NOT NULL
),
contact_act AS (
  SELECT 
    all_contact_company_names AS company_name,
    julianday(last_activity_ts) * 24 AS act_hr
  FROM intercom__contact_enhanced
  WHERE last_activity_ts IS NOT NULL
),
converted AS (
  SELECT DISTINCT c.company_name
  FROM conv_end c
  JOIN contact_act a ON c.company_name = a.company_name
  WHERE a.act_hr >= c.close_hr AND a.act_hr <= c.close_hr_72
),
all_cust AS (
  SELECT DISTINCT company_name FROM intercom__contact_enhanced
)
SELECT 
  COUNT(DISTINCT conv_end.company_name) AS customers_with_convs,
  (SELECT COUNT(DISTINCT company_name) FROM all_cust) AS total_customers,
  (SELECT COUNT(DISTINCT company_name) FROM converted) AS customers_converted,
  ROUND(100.0 * (SELECT COUNT(DISTINCT company_name) FROM converted) / (SELECT COUNT(DISTINCT company_name) FROM all_cust), 2) AS conversion_rate_pct
FROM conv_end
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-097/attempt-01/sql/S61.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-097/attempt-01/sql/S61.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-097/attempt-01/results/S61.rows.jsonl)；完整：True；SHA256：`fb7bb07c2e88baf967a86b17d7c3ec060f56cc310ef9a0c3098fb54dd5f351d8`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "intercom__conversation_enhanced", "kind": "base", "block": null, "base_tables": ["intercom__conversation_enhanced"]}] | [] | [] |
| B2 | [{"alias": "intercom__contact_enhanced", "kind": "base", "block": null, "base_tables": ["intercom__contact_enhanced"]}] | [] | [] |
| B3 | [{"alias": "c", "kind": "derived", "block": "B1", "base_tables": ["intercom__conversation_enhanced"]}, {"alias": "a", "kind": "derived", "block": "B2", "base_tables": ["intercom__contact_enhanced"]}] | [{"type": "INNER", "right": "contact_act AS a", "on": "c.company_name = a.company_name", "using": []}] | [] |
| B4 | [{"alias": "intercom__contact_enhanced", "kind": "base", "block": null, "base_tables": ["intercom__contact_enhanced"]}] | [] | [] |
| B5 | [{"alias": "all_cust", "kind": "derived", "block": "B4", "base_tables": ["intercom__contact_enhanced"]}] | [] | [] |
| B6 | [{"alias": "converted", "kind": "derived", "block": "B3", "base_tables": ["intercom__contact_enhanced", "intercom__conversation_enhanced"]}] | [] | [] |
| B7 | [{"alias": "converted", "kind": "derived", "block": "B3", "base_tables": ["intercom__contact_enhanced", "intercom__conversation_enhanced"]}] | [] | [] |
| B8 | [{"alias": "all_cust", "kind": "derived", "block": "B4", "base_tables": ["intercom__contact_enhanced"]}] | [] | [] |
| B9 | [{"alias": "conv_end", "kind": "derived", "block": "B1", "base_tables": ["intercom__conversation_enhanced"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B5 | COUNT(DISTINCT company_name) | [{"table": "intercom__conversation_enhanced", "column": "all_contact_company_names"}] | [] | False |
| B6 | COUNT(DISTINCT company_name) | [{"table": "intercom__conversation_enhanced", "column": "all_contact_company_names"}] | [] | False |
| B7 | COUNT(DISTINCT company_name) | [{"table": "intercom__conversation_enhanced", "column": "all_contact_company_names"}] | [] | False |
| B8 | COUNT(DISTINCT company_name) | [{"table": "intercom__conversation_enhanced", "column": "all_contact_company_names"}] | [] | False |
| B9 | COUNT(DISTINCT conv_end.company_name) | [{"table": "intercom__conversation_enhanced", "column": "all_contact_company_names"}] | [] | False |


## S62

类别 `data`；来源 `query_db`；调用 `7b5dda62fc574fabac178e8a17dcf1a7`；状态 `success`。

```sql
-- Conversation-to-Feature-Usage Conversion Rate - fixed
WITH company_dim AS (
  SELECT DISTINCT company_name FROM intercom__company_enhanced
),
contacts AS (
  SELECT DISTINCT all_contact_company_names AS company_name FROM intercom__contact_enhanced
),
conv_end AS (
  SELECT 
    all_contact_company_names AS company_name,
    last_close_at
  FROM intercom__conversation_enhanced
  WHERE last_close_at IS NOT NULL
),
contact_act AS (
  SELECT 
    all_contact_company_names AS company_name,
    last_activity_ts
  FROM intercom__contact_enhanced
  WHERE last_activity_ts IS NOT NULL
),
converted AS (
  SELECT DISTINCT c.company_name
  FROM conv_end c
  JOIN contact_act a ON c.company_name = a.company_name
  WHERE a.last_activity_ts >= c.last_close_at 
    AND a.last_activity_ts <= datetime(c.last_close_at, '+72 hours')
)
SELECT 
  (SELECT COUNT(*) FROM contacts) AS total_customers,
  (SELECT COUNT(DISTINCT company_name) FROM conv_end) AS customers_with_convs,
  (SELECT COUNT(*) FROM converted) AS customers_converted,
  ROUND(100.0 * (SELECT COUNT(*) FROM converted) / (SELECT COUNT(*) FROM contacts), 2) AS conversion_rate_pct
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-097/attempt-01/sql/S62.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-097/attempt-01/sql/S62.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-097/attempt-01/results/S62.rows.jsonl)；完整：True；SHA256：`b7d9a5734a0938bba4badf1d00555ed061924b3d6358c04afa8cbcc1dc2ffbf5`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "intercom__company_enhanced", "kind": "base", "block": null, "base_tables": ["intercom__company_enhanced"]}] | [] | [] |
| B2 | [{"alias": "intercom__contact_enhanced", "kind": "base", "block": null, "base_tables": ["intercom__contact_enhanced"]}] | [] | [] |
| B3 | [{"alias": "intercom__conversation_enhanced", "kind": "base", "block": null, "base_tables": ["intercom__conversation_enhanced"]}] | [] | [] |
| B4 | [{"alias": "intercom__contact_enhanced", "kind": "base", "block": null, "base_tables": ["intercom__contact_enhanced"]}] | [] | [] |
| B5 | [{"alias": "c", "kind": "derived", "block": "B3", "base_tables": ["intercom__conversation_enhanced"]}, {"alias": "a", "kind": "derived", "block": "B4", "base_tables": ["intercom__contact_enhanced"]}] | [{"type": "INNER", "right": "contact_act AS a", "on": "c.company_name = a.company_name", "using": []}] | [] |
| B6 | [{"alias": "contacts", "kind": "derived", "block": "B2", "base_tables": ["intercom__contact_enhanced"]}] | [] | [] |
| B7 | [{"alias": "conv_end", "kind": "derived", "block": "B3", "base_tables": ["intercom__conversation_enhanced"]}] | [] | [] |
| B8 | [{"alias": "converted", "kind": "derived", "block": "B5", "base_tables": ["intercom__contact_enhanced", "intercom__conversation_enhanced"]}] | [] | [] |
| B9 | [{"alias": "converted", "kind": "derived", "block": "B5", "base_tables": ["intercom__contact_enhanced", "intercom__conversation_enhanced"]}] | [] | [] |
| B10 | [{"alias": "contacts", "kind": "derived", "block": "B2", "base_tables": ["intercom__contact_enhanced"]}] | [] | [] |
| B11 | [] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B6 | COUNT(*) | [] | [] | True |
| B7 | COUNT(DISTINCT company_name) | [{"table": "intercom__conversation_enhanced", "column": "all_contact_company_names"}] | [] | False |
| B8 | COUNT(*) | [] | [] | True |
| B9 | COUNT(*) | [] | [] | True |
| B10 | COUNT(*) | [] | [] | True |


未解析列血缘：[{"block": "B11", "column": "company_name", "reason": "ambiguous_or_missing_source"}]

## S63

类别 `data`；来源 `query_db`；调用 `01a76d6c8a024ba0a26de1224f5c3c9b`；状态 `success`。

```sql
-- Weekly retention: contacts with is_active_7d=1 and retained_7d=1 at company level
WITH company_weekly AS (
  SELECT 
    all_contact_company_names AS company_name,
    MAX(CASE WHEN is_active_7d = 1 THEN 1 ELSE 0 END) AS has_active,
    MAX(CASE WHEN retained_7d = 1 THEN 1 ELSE 0 END) AS has_retained
  FROM intercom__contact_enhanced
  GROUP BY all_contact_company_names
)
SELECT 
  COUNT(*) AS total_companies,
  SUM(has_active) AS active_companies,
  SUM(has_retained) AS retained_companies,
  ROUND(100.0 * SUM(has_retained) / NULLIF(SUM(has_active), 0), 2) AS weekly_retention_pct
FROM company_weekly
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-097/attempt-01/sql/S63.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-097/attempt-01/sql/S63.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-097/attempt-01/results/S63.rows.jsonl)；完整：True；SHA256：`e864f0af22dd5371097b10c1def5516a82a82a09993a9bbf14ea76be841749c9`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "intercom__contact_enhanced", "kind": "base", "block": null, "base_tables": ["intercom__contact_enhanced"]}] | [] | ["all_contact_company_names"] |
| B2 | [{"alias": "company_weekly", "kind": "derived", "block": "B1", "base_tables": ["intercom__contact_enhanced"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | MAX(CASE WHEN is_active_7d = 1 THEN 1 ELSE 0 END) | [] | [{"table": "intercom__contact_enhanced", "column": "is_active_7d"}] | False |
| B1 | MAX(CASE WHEN retained_7d = 1 THEN 1 ELSE 0 END) | [] | [{"table": "intercom__contact_enhanced", "column": "retained_7d"}] | False |
| B2 | COUNT(*) | [] | [] | True |
| B2 | SUM(has_active) | [{"table": "intercom__contact_enhanced", "column": "is_active_7d"}] | [] | False |
| B2 | SUM(has_retained) | [{"table": "intercom__contact_enhanced", "column": "retained_7d"}] | [] | False |
| B2 | SUM(has_retained) | [{"table": "intercom__contact_enhanced", "column": "retained_7d"}] | [] | False |
| B2 | SUM(has_active) | [{"table": "intercom__contact_enhanced", "column": "is_active_7d"}] | [] | False |


## S64

类别 `data`；来源 `query_db`；调用 `1a96fecd6e7046749d5b3614facb5c00`；状态 `success`。

```sql
-- Monthly retention: contacts with is_active_30d=1 and retained_30d=1 at company level
WITH company_monthly AS (
  SELECT 
    all_contact_company_names AS company_name,
    MAX(CASE WHEN is_active_30d = 1 THEN 1 ELSE 0 END) AS has_active,
    MAX(CASE WHEN retained_30d = 1 THEN 1 ELSE 0 END) AS has_retained
  FROM intercom__contact_enhanced
  GROUP BY all_contact_company_names
)
SELECT 
  COUNT(*) AS total_companies,
  SUM(has_active) AS active_companies,
  SUM(has_retained) AS retained_companies,
  ROUND(100.0 * SUM(has_retained) / NULLIF(SUM(has_active), 0), 2) AS monthly_retention_pct
FROM company_monthly
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-097/attempt-01/sql/S64.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-097/attempt-01/sql/S64.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-097/attempt-01/results/S64.rows.jsonl)；完整：True；SHA256：`c276a01ac13f7833babc7db1b5252f76cd0ce1291539fcd5c08bc7c28a4289dc`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "intercom__contact_enhanced", "kind": "base", "block": null, "base_tables": ["intercom__contact_enhanced"]}] | [] | ["all_contact_company_names"] |
| B2 | [{"alias": "company_monthly", "kind": "derived", "block": "B1", "base_tables": ["intercom__contact_enhanced"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | MAX(CASE WHEN is_active_30d = 1 THEN 1 ELSE 0 END) | [] | [{"table": "intercom__contact_enhanced", "column": "is_active_30d"}] | False |
| B1 | MAX(CASE WHEN retained_30d = 1 THEN 1 ELSE 0 END) | [] | [{"table": "intercom__contact_enhanced", "column": "retained_30d"}] | False |
| B2 | COUNT(*) | [] | [] | True |
| B2 | SUM(has_active) | [{"table": "intercom__contact_enhanced", "column": "is_active_30d"}] | [] | False |
| B2 | SUM(has_retained) | [{"table": "intercom__contact_enhanced", "column": "retained_30d"}] | [] | False |
| B2 | SUM(has_retained) | [{"table": "intercom__contact_enhanced", "column": "retained_30d"}] | [] | False |
| B2 | SUM(has_active) | [{"table": "intercom__contact_enhanced", "column": "is_active_30d"}] | [] | False |


## S65

类别 `data`；来源 `query_db`；调用 `c1c07b9d3edb480294c2a3a742641f4f`；状态 `success`。

```sql
-- Check relationship between is_active and retained per contact
SELECT 
  is_active_7d, retained_7d, COUNT(*) as cnt
FROM intercom__contact_enhanced
GROUP BY is_active_7d, retained_7d
ORDER BY is_active_7d, retained_7d
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-097/attempt-01/sql/S65.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-097/attempt-01/sql/S65.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-097/attempt-01/results/S65.rows.jsonl)；完整：True；SHA256：`a8b1f1fd233af717f1cc1e5281007b111310f203299dd968dbe13e67f1c481b9`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "intercom__contact_enhanced", "kind": "base", "block": null, "base_tables": ["intercom__contact_enhanced"]}] | [] | ["is_active_7d", "retained_7d"] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |


## S66

类别 `data`；来源 `query_db`；调用 `7376822260e74f7e82d449145020e2f1`；状态 `success`。

```sql
SELECT 
  is_active_30d, retained_30d, COUNT(*) as cnt
FROM intercom__contact_enhanced
GROUP BY is_active_30d, retained_30d
ORDER BY is_active_30d, retained_30d
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-097/attempt-01/sql/S66.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-097/attempt-01/sql/S66.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-097/attempt-01/results/S66.rows.jsonl)；完整：True；SHA256：`85df4703518be31227c5f4f5a7614e7b1ce7f7877f315673b9fce90250af07a4`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "intercom__contact_enhanced", "kind": "base", "block": null, "base_tables": ["intercom__contact_enhanced"]}] | [] | ["is_active_30d", "retained_30d"] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |


## S67

类别 `data`；来源 `query_db`；调用 `277fa963ddeb4f658e5ecb8f06b676bb`；状态 `success`。

```sql
-- Company-level retention metrics from company_metrics
SELECT 
  ROUND(AVG(registration_retention_7d), 4) AS avg_weekly_retention,
  ROUND(AVG(registration_retention_30d), 4) AS avg_monthly_retention,
  COUNT(*) AS total_companies
FROM intercom__company_metrics
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-097/attempt-01/sql/S67.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-097/attempt-01/sql/S67.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-097/attempt-01/results/S67.rows.jsonl)；完整：True；SHA256：`c3e0f10057fef5853e7c29ee338f4215b65ae376dceb6ccdcf90c2c65b2f03ad`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "intercom__company_metrics", "kind": "base", "block": null, "base_tables": ["intercom__company_metrics"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |
| B1 | AVG(registration_retention_7d) | [{"table": "intercom__company_metrics", "column": "registration_retention_7d"}] | [] | False |
| B1 | AVG(registration_retention_30d) | [{"table": "intercom__company_metrics", "column": "registration_retention_30d"}] | [] | False |


## S68

类别 `data`；来源 `query_db`；调用 `4cd2f13f72914bdd9527f59235d78cce`；状态 `success`。

```sql
-- Distribution of company-level retention
SELECT 
  ROUND(registration_retention_7d, 2) AS ret_7d,
  ROUND(registration_retention_30d, 2) AS ret_30d,
  COUNT(*) AS cnt
FROM intercom__company_metrics
GROUP BY ROUND(registration_retention_7d, 2), ROUND(registration_retention_30d, 2)
ORDER BY ret_7d, ret_30d
LIMIT 20
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-097/attempt-01/sql/S68.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-097/attempt-01/sql/S68.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-097/attempt-01/results/S68.rows.jsonl)；完整：True；SHA256：`94d670814853419b87733658286162714678115be815a251b1b5df8454175927`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "intercom__company_metrics", "kind": "base", "block": null, "base_tables": ["intercom__company_metrics"]}] | [] | ["ROUND(registration_retention_7d, 2)", "ROUND(registration_retention_30d, 2)"] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |


## S69

类别 `data`；来源 `query_db`；调用 `7acf97ed19af40eab2951b789e1d7245`；状态 `success`。

```sql
-- Retention by segment using company_metrics
WITH company_dim AS (
  SELECT DISTINCT company_name,
    CASE WHEN all_company_tags LIKE '%segment:new_contract%' THEN 'new_contract'
         WHEN all_company_tags LIKE '%segment:renewal%' THEN 'renewal'
         WHEN all_company_tags LIKE '%segment:churn_watch%' THEN 'churn_watch'
         WHEN all_company_tags LIKE '%segment:expansion%' THEN 'expansion'
         ELSE 'unknown' END AS segment
  FROM intercom__company_enhanced
)
SELECT 
  cd.segment,
  COUNT(*) AS companies,
  ROUND(AVG(cm.registration_retention_7d), 4) AS avg_weekly_retention,
  ROUND(AVG(cm.registration_retention_30d), 4) AS avg_monthly_retention,
  ROUND(AVG(cm.contacts_active_7d), 2) AS avg_active_contacts_7d,
  ROUND(AVG(cm.contacts_active_30d), 2) AS avg_active_contacts_30d
FROM company_dim cd
JOIN intercom__company_metrics cm ON cd.company_name = cm.company_name
GROUP BY cd.segment
ORDER BY cd.segment
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-097/attempt-01/sql/S69.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-097/attempt-01/sql/S69.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-097/attempt-01/results/S69.rows.jsonl)；完整：True；SHA256：`b1749de13510c8b706768aff86b14ed8686b349da2a7d535e5c405de61cd740e`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "intercom__company_enhanced", "kind": "base", "block": null, "base_tables": ["intercom__company_enhanced"]}] | [] | [] |
| B2 | [{"alias": "cd", "kind": "derived", "block": "B1", "base_tables": ["intercom__company_enhanced"]}, {"alias": "cm", "kind": "base", "block": null, "base_tables": ["intercom__company_metrics"]}] | [{"type": "INNER", "right": "intercom__company_metrics AS cm", "on": "cd.company_name = cm.company_name", "using": []}] | ["cd.segment"] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B2 | COUNT(*) | [] | [] | True |
| B2 | AVG(cm.registration_retention_7d) | [{"table": "intercom__company_metrics", "column": "registration_retention_7d"}] | [] | False |
| B2 | AVG(cm.registration_retention_30d) | [{"table": "intercom__company_metrics", "column": "registration_retention_30d"}] | [] | False |
| B2 | AVG(cm.contacts_active_7d) | [{"table": "intercom__company_metrics", "column": "contacts_active_7d"}] | [] | False |
| B2 | AVG(cm.contacts_active_30d) | [{"table": "intercom__company_metrics", "column": "contacts_active_30d"}] | [] | False |


## S70

类别 `data`；来源 `query_db`；调用 `7b1a5e5d358d4b9ab67e78721c6e9760`；状态 `success`。

```sql
-- Retention by seat bucket
WITH company_dim AS (
  SELECT DISTINCT company_name,
    CASE WHEN all_company_tags LIKE '%seat_bucket:seats:under_60%' THEN 'under_60'
         WHEN all_company_tags LIKE '%seat_bucket:seats:60_129%' THEN '60_129'
         WHEN all_company_tags LIKE '%seat_bucket:seats:130_259%' THEN '130_259'
         WHEN all_company_tags LIKE '%seat_bucket:seats:260_419%' THEN '260_419'
         WHEN all_company_tags LIKE '%seat_bucket:seats:420_plus%' THEN '420_plus'
         ELSE 'unknown' END AS seat_bucket
  FROM intercom__company_enhanced
)
SELECT 
  cd.seat_bucket,
  COUNT(*) AS companies,
  ROUND(AVG(cm.registration_retention_7d), 4) AS avg_weekly_retention,
  ROUND(AVG(cm.registration_retention_30d), 4) AS avg_monthly_retention
FROM company_dim cd
JOIN intercom__company_metrics cm ON cd.company_name = cm.company_name
GROUP BY cd.seat_bucket
ORDER BY cd.seat_bucket
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-097/attempt-01/sql/S70.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-097/attempt-01/sql/S70.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-097/attempt-01/results/S70.rows.jsonl)；完整：True；SHA256：`239c4b380ecc93faa93a5e3e6380976cd5bc0b3d5e712462ac97c872843ce045`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "intercom__company_enhanced", "kind": "base", "block": null, "base_tables": ["intercom__company_enhanced"]}] | [] | [] |
| B2 | [{"alias": "cd", "kind": "derived", "block": "B1", "base_tables": ["intercom__company_enhanced"]}, {"alias": "cm", "kind": "base", "block": null, "base_tables": ["intercom__company_metrics"]}] | [{"type": "INNER", "right": "intercom__company_metrics AS cm", "on": "cd.company_name = cm.company_name", "using": []}] | ["cd.seat_bucket"] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B2 | COUNT(*) | [] | [] | True |
| B2 | AVG(cm.registration_retention_7d) | [{"table": "intercom__company_metrics", "column": "registration_retention_7d"}] | [] | False |
| B2 | AVG(cm.registration_retention_30d) | [{"table": "intercom__company_metrics", "column": "registration_retention_30d"}] | [] | False |


## S71

类别 `data`；来源 `query_db`；调用 `78ca24aeea6d4876ae81b2a58d3c2004`；状态 `success`。

```sql
-- Retention by ARR bucket
WITH company_dim AS (
  SELECT DISTINCT company_name,
    CASE WHEN all_company_tags LIKE '%arr_bucket:arr:<30k%' THEN '<30k'
         WHEN all_company_tags LIKE '%arr_bucket:arr:30k_65k%' THEN '30k_65k'
         WHEN all_company_tags LIKE '%arr_bucket:arr:65k_110k%' THEN '65k_110k'
         WHEN all_company_tags LIKE '%arr_bucket:arr:110k_200k%' THEN '110k_200k'
         WHEN all_company_tags LIKE '%arr_bucket:arr:200k_plus%' THEN '200k_plus'
         ELSE 'unknown' END AS arr_bucket
  FROM intercom__company_enhanced
)
SELECT 
  cd.arr_bucket,
  COUNT(*) AS companies,
  ROUND(AVG(cm.registration_retention_7d), 4) AS avg_weekly_retention,
  ROUND(AVG(cm.registration_retention_30d), 4) AS avg_monthly_retention
FROM company_dim cd
JOIN intercom__company_metrics cm ON cd.company_name = cm.company_name
GROUP BY cd.arr_bucket
ORDER BY cd.arr_bucket
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-097/attempt-01/sql/S71.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-097/attempt-01/sql/S71.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-097/attempt-01/results/S71.rows.jsonl)；完整：True；SHA256：`ec1d1e8efd37edf24c58876320e865f11b0e01295300bc87ff5d6ad98b43a618`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "intercom__company_enhanced", "kind": "base", "block": null, "base_tables": ["intercom__company_enhanced"]}] | [] | [] |
| B2 | [{"alias": "cd", "kind": "derived", "block": "B1", "base_tables": ["intercom__company_enhanced"]}, {"alias": "cm", "kind": "base", "block": null, "base_tables": ["intercom__company_metrics"]}] | [{"type": "INNER", "right": "intercom__company_metrics AS cm", "on": "cd.company_name = cm.company_name", "using": []}] | ["cd.arr_bucket"] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B2 | COUNT(*) | [] | [] | True |
| B2 | AVG(cm.registration_retention_7d) | [{"table": "intercom__company_metrics", "column": "registration_retention_7d"}] | [] | False |
| B2 | AVG(cm.registration_retention_30d) | [{"table": "intercom__company_metrics", "column": "registration_retention_30d"}] | [] | False |


## S72

类别 `data`；来源 `query_db`；调用 `31cf34b6a4de4e3b8472249a267aebd2`；状态 `success`。

```sql
-- Conversion rate by segment
WITH company_dim AS (
  SELECT DISTINCT company_name,
    CASE WHEN all_company_tags LIKE '%segment:new_contract%' THEN 'new_contract'
         WHEN all_company_tags LIKE '%segment:renewal%' THEN 'renewal'
         WHEN all_company_tags LIKE '%segment:churn_watch%' THEN 'churn_watch'
         WHEN all_company_tags LIKE '%segment:expansion%' THEN 'expansion'
         ELSE 'unknown' END AS segment
  FROM intercom__company_enhanced
),
conv_end AS (
  SELECT DISTINCT all_contact_company_names AS company_name, last_close_at
  FROM intercom__conversation_enhanced
  WHERE last_close_at IS NOT NULL
),
contact_act AS (
  SELECT all_contact_company_names AS company_name, last_activity_ts
  FROM intercom__contact_enhanced
  WHERE last_activity_ts IS NOT NULL
),
converted AS (
  SELECT DISTINCT c.company_name
  FROM conv_end c
  JOIN contact_act a ON c.company_name = a.company_name
  WHERE a.last_activity_ts >= c.last_close_at 
    AND a.last_activity_ts <= datetime(c.last_close_at, '+72 hours')
)
SELECT 
  cd.segment,
  COUNT(DISTINCT cd.company_name) AS total_customers,
  COUNT(DISTINCT conv.company_name) AS customers_with_convs,
  COUNT(DISTINCT cv.company_name) AS customers_converted,
  ROUND(100.0 * COUNT(DISTINCT cv.company_name) / COUNT(DISTINCT cd.company_name), 2) AS conversion_rate_pct
FROM company_dim cd
LEFT JOIN (SELECT DISTINCT company_name FROM conv_end) conv ON cd.company_name = conv.company_name
LEFT JOIN converted cv ON cd.company_name = cv.company_name
GROUP BY cd.segment
ORDER BY cd.segment
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-097/attempt-01/sql/S72.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-097/attempt-01/sql/S72.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-097/attempt-01/results/S72.rows.jsonl)；完整：True；SHA256：`fa32a9a7c520b951d76807841d6e6e3c1ee5cb87957e4cb637bef41525d1bfc1`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "intercom__company_enhanced", "kind": "base", "block": null, "base_tables": ["intercom__company_enhanced"]}] | [] | [] |
| B2 | [{"alias": "intercom__conversation_enhanced", "kind": "base", "block": null, "base_tables": ["intercom__conversation_enhanced"]}] | [] | [] |
| B3 | [{"alias": "intercom__contact_enhanced", "kind": "base", "block": null, "base_tables": ["intercom__contact_enhanced"]}] | [] | [] |
| B4 | [{"alias": "c", "kind": "derived", "block": "B2", "base_tables": ["intercom__conversation_enhanced"]}, {"alias": "a", "kind": "derived", "block": "B3", "base_tables": ["intercom__contact_enhanced"]}] | [{"type": "INNER", "right": "contact_act AS a", "on": "c.company_name = a.company_name", "using": []}] | [] |
| B5 | [{"alias": "conv_end", "kind": "derived", "block": "B2", "base_tables": ["intercom__conversation_enhanced"]}] | [] | [] |
| B6 | [{"alias": "cd", "kind": "derived", "block": "B1", "base_tables": ["intercom__company_enhanced"]}, {"alias": "conv", "kind": "derived", "block": "B5", "base_tables": ["intercom__conversation_enhanced"]}, {"alias": "cv", "kind": "derived", "block": "B4", "base_tables": ["intercom__contact_enhanced", "intercom__conversation_enhanced"]}] | [{"type": "LEFT", "right": "(SELECT DISTINCT company_name FROM conv_end) AS conv", "on": "cd.company_name = conv.company_name", "using": []}, {"type": "LEFT", "right": "converted AS cv", "on": "cd.company_name = cv.company_name", "using": []}] | ["cd.segment"] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B6 | COUNT(DISTINCT cd.company_name) | [{"table": "intercom__company_enhanced", "column": "company_name"}] | [] | False |
| B6 | COUNT(DISTINCT conv.company_name) | [{"table": "intercom__conversation_enhanced", "column": "all_contact_company_names"}] | [] | False |
| B6 | COUNT(DISTINCT cv.company_name) | [{"table": "intercom__conversation_enhanced", "column": "all_contact_company_names"}] | [] | False |
| B6 | COUNT(DISTINCT cd.company_name) | [{"table": "intercom__company_enhanced", "column": "company_name"}] | [] | False |
| B6 | COUNT(DISTINCT cv.company_name) | [{"table": "intercom__conversation_enhanced", "column": "all_contact_company_names"}] | [] | False |


## S73

类别 `data`；来源 `query_db`；调用 `e090651be71d42b1b0260cf585259c96`；状态 `success`。

```sql
-- Conversion rate by seat bucket
WITH company_dim AS (
  SELECT DISTINCT company_name,
    CASE WHEN all_company_tags LIKE '%seat_bucket:seats:under_60%' THEN 'under_60'
         WHEN all_company_tags LIKE '%seat_bucket:seats:60_129%' THEN '60_129'
         WHEN all_company_tags LIKE '%seat_bucket:seats:130_259%' THEN '130_259'
         WHEN all_company_tags LIKE '%seat_bucket:seats:260_419%' THEN '260_419'
         WHEN all_company_tags LIKE '%seat_bucket:seats:420_plus%' THEN '420_plus'
         ELSE 'unknown' END AS seat_bucket
  FROM intercom__company_enhanced
),
conv_end AS (
  SELECT DISTINCT all_contact_company_names AS company_name, last_close_at
  FROM intercom__conversation_enhanced WHERE last_close_at IS NOT NULL
),
contact_act AS (
  SELECT all_contact_company_names AS company_name, last_activity_ts
  FROM intercom__contact_enhanced WHERE last_activity_ts IS NOT NULL
),
converted AS (
  SELECT DISTINCT c.company_name
  FROM conv_end c JOIN contact_act a ON c.company_name = a.company_name
  WHERE a.last_activity_ts >= c.last_close_at 
    AND a.last_activity_ts <= datetime(c.last_close_at, '+72 hours')
)
SELECT 
  cd.seat_bucket,
  COUNT(DISTINCT cd.company_name) AS total_customers,
  COUNT(DISTINCT cv.company_name) AS customers_converted,
  ROUND(100.0 * COUNT(DISTINCT cv.company_name) / COUNT(DISTINCT cd.company_name), 2) AS conversion_rate_pct
FROM company_dim cd
LEFT JOIN converted cv ON cd.company_name = cv.company_name
GROUP BY cd.seat_bucket
ORDER BY cd.seat_bucket
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-097/attempt-01/sql/S73.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-097/attempt-01/sql/S73.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-097/attempt-01/results/S73.rows.jsonl)；完整：True；SHA256：`760044a89c049b8c2eb91a31f881f100116a7e015758135534261018013a2bf1`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "intercom__company_enhanced", "kind": "base", "block": null, "base_tables": ["intercom__company_enhanced"]}] | [] | [] |
| B2 | [{"alias": "intercom__conversation_enhanced", "kind": "base", "block": null, "base_tables": ["intercom__conversation_enhanced"]}] | [] | [] |
| B3 | [{"alias": "intercom__contact_enhanced", "kind": "base", "block": null, "base_tables": ["intercom__contact_enhanced"]}] | [] | [] |
| B4 | [{"alias": "c", "kind": "derived", "block": "B2", "base_tables": ["intercom__conversation_enhanced"]}, {"alias": "a", "kind": "derived", "block": "B3", "base_tables": ["intercom__contact_enhanced"]}] | [{"type": "INNER", "right": "contact_act AS a", "on": "c.company_name = a.company_name", "using": []}] | [] |
| B5 | [{"alias": "cd", "kind": "derived", "block": "B1", "base_tables": ["intercom__company_enhanced"]}, {"alias": "cv", "kind": "derived", "block": "B4", "base_tables": ["intercom__contact_enhanced", "intercom__conversation_enhanced"]}] | [{"type": "LEFT", "right": "converted AS cv", "on": "cd.company_name = cv.company_name", "using": []}] | ["cd.seat_bucket"] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B5 | COUNT(DISTINCT cd.company_name) | [{"table": "intercom__company_enhanced", "column": "company_name"}] | [] | False |
| B5 | COUNT(DISTINCT cv.company_name) | [{"table": "intercom__conversation_enhanced", "column": "all_contact_company_names"}] | [] | False |
| B5 | COUNT(DISTINCT cd.company_name) | [{"table": "intercom__company_enhanced", "column": "company_name"}] | [] | False |
| B5 | COUNT(DISTINCT cv.company_name) | [{"table": "intercom__conversation_enhanced", "column": "all_contact_company_names"}] | [] | False |


## S74

类别 `data`；来源 `query_db`；调用 `58ea1f8ad63e43808cc5a0947f3d9570`；状态 `success`。

```sql
-- Conversion rate by ARR bucket
WITH company_dim AS (
  SELECT DISTINCT company_name,
    CASE WHEN all_company_tags LIKE '%arr_bucket:arr:<30k%' THEN '<30k'
         WHEN all_company_tags LIKE '%arr_bucket:arr:30k_65k%' THEN '30k_65k'
         WHEN all_company_tags LIKE '%arr_bucket:arr:65k_110k%' THEN '65k_110k'
         WHEN all_company_tags LIKE '%arr_bucket:arr:110k_200k%' THEN '110k_200k'
         WHEN all_company_tags LIKE '%arr_bucket:arr:200k_plus%' THEN '200k_plus'
         ELSE 'unknown' END AS arr_bucket
  FROM intercom__company_enhanced
),
conv_end AS (
  SELECT DISTINCT all_contact_company_names AS company_name, last_close_at
  FROM intercom__conversation_enhanced WHERE last_close_at IS NOT NULL
),
contact_act AS (
  SELECT all_contact_company_names AS company_name, last_activity_ts
  FROM intercom__contact_enhanced WHERE last_activity_ts IS NOT NULL
),
converted AS (
  SELECT DISTINCT c.company_name
  FROM conv_end c JOIN contact_act a ON c.company_name = a.company_name
  WHERE a.last_activity_ts >= c.last_close_at 
    AND a.last_activity_ts <= datetime(c.last_close_at, '+72 hours')
)
SELECT 
  cd.arr_bucket,
  COUNT(DISTINCT cd.company_name) AS total_customers,
  COUNT(DISTINCT cv.company_name) AS customers_converted,
  ROUND(100.0 * COUNT(DISTINCT cv.company_name) / COUNT(DISTINCT cd.company_name), 2) AS conversion_rate_pct
FROM company_dim cd
LEFT JOIN converted cv ON cd.company_name = cv.company_name
GROUP BY cd.arr_bucket
ORDER BY cd.arr_bucket
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-097/attempt-01/sql/S74.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-097/attempt-01/sql/S74.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-097/attempt-01/results/S74.rows.jsonl)；完整：True；SHA256：`44145c9a6f3d71a2b4b8fc28b1b2fab82ba59d5c5c27630d70a6990bc2a7b827`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "intercom__company_enhanced", "kind": "base", "block": null, "base_tables": ["intercom__company_enhanced"]}] | [] | [] |
| B2 | [{"alias": "intercom__conversation_enhanced", "kind": "base", "block": null, "base_tables": ["intercom__conversation_enhanced"]}] | [] | [] |
| B3 | [{"alias": "intercom__contact_enhanced", "kind": "base", "block": null, "base_tables": ["intercom__contact_enhanced"]}] | [] | [] |
| B4 | [{"alias": "c", "kind": "derived", "block": "B2", "base_tables": ["intercom__conversation_enhanced"]}, {"alias": "a", "kind": "derived", "block": "B3", "base_tables": ["intercom__contact_enhanced"]}] | [{"type": "INNER", "right": "contact_act AS a", "on": "c.company_name = a.company_name", "using": []}] | [] |
| B5 | [{"alias": "cd", "kind": "derived", "block": "B1", "base_tables": ["intercom__company_enhanced"]}, {"alias": "cv", "kind": "derived", "block": "B4", "base_tables": ["intercom__contact_enhanced", "intercom__conversation_enhanced"]}] | [{"type": "LEFT", "right": "converted AS cv", "on": "cd.company_name = cv.company_name", "using": []}] | ["cd.arr_bucket"] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B5 | COUNT(DISTINCT cd.company_name) | [{"table": "intercom__company_enhanced", "column": "company_name"}] | [] | False |
| B5 | COUNT(DISTINCT cv.company_name) | [{"table": "intercom__conversation_enhanced", "column": "all_contact_company_names"}] | [] | False |
| B5 | COUNT(DISTINCT cd.company_name) | [{"table": "intercom__company_enhanced", "column": "company_name"}] | [] | False |
| B5 | COUNT(DISTINCT cv.company_name) | [{"table": "intercom__conversation_enhanced", "column": "all_contact_company_names"}] | [] | False |


## S75

类别 `data`；来源 `query_db`；调用 `572912ddc1f74620a357880ffa3bc73a`；状态 `success`。

```sql
-- Topic distribution
SELECT 
  CASE 
    WHEN all_conversation_tags LIKE '%topic:usage_insight%' THEN 'usage_insight'
    WHEN all_conversation_tags LIKE '%topic:onboarding%' THEN 'onboarding'
    WHEN all_conversation_tags LIKE '%topic:security%' THEN 'security'
    WHEN all_conversation_tags LIKE '%topic:billing%' THEN 'billing'
    WHEN all_conversation_tags LIKE '%topic:renewal%' THEN 'renewal'
    WHEN all_conversation_tags LIKE '%topic:adoption%' THEN 'adoption'
    WHEN all_conversation_tags LIKE '%topic:product%' THEN 'product'
    ELSE 'other'
  END AS topic,
  COUNT(*) AS total
FROM intercom__conversation_enhanced
GROUP BY 1
ORDER BY total DESC
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-097/attempt-01/sql/S75.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-097/attempt-01/sql/S75.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-097/attempt-01/results/S75.rows.jsonl)；完整：True；SHA256：`87557796034c7fa18798735b1ab5eb4bb77f9590c76395dbe39efd869c314bf6`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "intercom__conversation_enhanced", "kind": "base", "block": null, "base_tables": ["intercom__conversation_enhanced"]}] | [] | ["CASE WHEN all_conversation_tags LIKE '%topic:usage_insight%' THEN 'usage_insight' WHEN all_conversation_tags LIKE '%topic:onboarding%' THEN 'onboarding' WHEN all_conversation_tags LIKE '%topic:security%' THEN 'security' WHEN all_conversation_tags LIKE '%topic:billing%' THEN 'billing' WHEN all_conversation_tags LIKE '%topic:renewal%' THEN 'renewal' WHEN all_conversation_tags LIKE '%topic:adoption%' THEN 'adoption' WHEN all_conversation_tags LIKE '%topic:product%' THEN 'product' ELSE 'other' END"] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |


## S76

类别 `data`；来源 `query_db`；调用 `9a1747fe485d4068891167199fc34ad8`；状态 `success`。

```sql
-- Distinct tag fragments in conversation tags
SELECT all_conversation_tags, COUNT(*) as cnt FROM intercom__conversation_enhanced GROUP BY all_conversation_tags ORDER BY cnt DESC LIMIT 30
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-097/attempt-01/sql/S76.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-097/attempt-01/sql/S76.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-097/attempt-01/results/S76.rows.jsonl)；完整：True；SHA256：`c0392ce22abfc3e0ad1550ce3393e12f9fbeeb6cf3fa4f31b719b2e7b6a0826f`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "intercom__conversation_enhanced", "kind": "base", "block": null, "base_tables": ["intercom__conversation_enhanced"]}] | [] | ["all_conversation_tags"] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |


## S77

类别 `data`；来源 `query_db`；调用 `1ff40ccf160b4fe09ffb2b853f0e2dd8`；状态 `success`。

```sql
-- Extract all unique topic values from tags
SELECT DISTINCT 
  SUBSTR(all_conversation_tags, INSTR(all_conversation_tags, 'topic:'), 
         CASE WHEN INSTR(SUBSTR(all_conversation_tags, INSTR(all_conversation_tags, 'topic:')), '|') > 0 
              THEN INSTR(SUBSTR(all_conversation_tags, INSTR(all_conversation_tags, 'topic:')), '|') - 1 
              ELSE LENGTH(SUBSTR(all_conversation_tags, INSTR(all_conversation_tags, 'topic:'))) END) AS topic_tag
FROM intercom__conversation_enhanced
WHERE all_conversation_tags LIKE '%topic:%'
ORDER BY topic_tag
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-097/attempt-01/sql/S77.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-097/attempt-01/sql/S77.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-097/attempt-01/results/S77.rows.jsonl)；完整：True；SHA256：`ebf9469f4733936ac90fb4cccabcdc3a9a41523c143f79ef9727b3fdbd6536c8`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "intercom__conversation_enhanced", "kind": "base", "block": null, "base_tables": ["intercom__conversation_enhanced"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |


## S78

类别 `data`；来源 `query_db`；调用 `1cd4ad80a9204fd2a565b228190339cd`；状态 `success`。

```sql
-- Extract all unique channel values
SELECT DISTINCT 
  SUBSTR(all_conversation_tags, INSTR(all_conversation_tags, 'channel:'), 
         CASE WHEN INSTR(SUBSTR(all_conversation_tags, INSTR(all_conversation_tags, 'channel:')), '|') > 0 
              THEN INSTR(SUBSTR(all_conversation_tags, INSTR(all_conversation_tags, 'channel:')), '|') - 1 
              ELSE LENGTH(SUBSTR(all_conversation_tags, INSTR(all_conversation_tags, 'channel:'))) END) AS channel_tag
FROM intercom__conversation_enhanced
WHERE all_conversation_tags LIKE '%channel:%'
ORDER BY channel_tag
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-097/attempt-01/sql/S78.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-097/attempt-01/sql/S78.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-097/attempt-01/results/S78.rows.jsonl)；完整：True；SHA256：`f3843f7f67193c1bbec5ea88632f1fc5caec5fb6156ef48df6cda1cda019ba59`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "intercom__conversation_enhanced", "kind": "base", "block": null, "base_tables": ["intercom__conversation_enhanced"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |


## S79

类别 `data`；来源 `query_db`；调用 `81eab671344d4726835345401d0512bb`；状态 `success`。

```sql
-- Extract all unique SLA values
SELECT DISTINCT 
  SUBSTR(all_conversation_tags, INSTR(all_conversation_tags, 'sla:'), 
         CASE WHEN INSTR(SUBSTR(all_conversation_tags, INSTR(all_conversation_tags, 'sla:')), '|') > 0 
              THEN INSTR(SUBSTR(all_conversation_tags, INSTR(all_conversation_tags, 'sla:')), '|') - 1 
              ELSE LENGTH(SUBSTR(all_conversation_tags, INSTR(all_conversation_tags, 'sla:'))) END) AS sla_tag
FROM intercom__conversation_enhanced
WHERE all_conversation_tags LIKE '%sla:%'
ORDER BY sla_tag
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-097/attempt-01/sql/S79.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-097/attempt-01/sql/S79.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-097/attempt-01/results/S79.rows.jsonl)；完整：True；SHA256：`e16c75451652b094cfd331275c3b348bce02f3cf07b1e171401da9b205200c3e`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "intercom__conversation_enhanced", "kind": "base", "block": null, "base_tables": ["intercom__conversation_enhanced"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |


## S80

类别 `data`；来源 `query_db`；调用 `c039bbf1c14b45ccb3e7d0dded785b70`；状态 `success`。

```sql
-- Topic distribution by segment
WITH company_dim AS (
  SELECT DISTINCT company_name,
    CASE WHEN all_company_tags LIKE '%segment:new_contract%' THEN 'new_contract'
         WHEN all_company_tags LIKE '%segment:renewal%' THEN 'renewal'
         WHEN all_company_tags LIKE '%segment:churn_watch%' THEN 'churn_watch'
         WHEN all_company_tags LIKE '%segment:expansion%' THEN 'expansion'
         ELSE 'unknown' END AS segment
  FROM intercom__company_enhanced
),
conv AS (
  SELECT ce.all_contact_company_names AS company_name, ce.all_conversation_tags
  FROM intercom__conversation_enhanced ce
)
SELECT 
  co.segment,
  CASE 
    WHEN c.all_conversation_tags LIKE '%topic:onboarding%' THEN 'onboarding'
    WHEN c.all_conversation_tags LIKE '%topic:billing%' THEN 'billing'
    WHEN c.all_conversation_tags LIKE '%topic:usage_insight%' THEN 'usage_insight'
    WHEN c.all_conversation_tags LIKE '%topic:security%' THEN 'security'
    WHEN c.all_conversation_tags LIKE '%topic:renewal%' THEN 'renewal'
    WHEN c.all_conversation_tags LIKE '%topic:adoption%' THEN 'adoption'
    WHEN c.all_conversation_tags LIKE '%topic:escalation%' THEN 'escalation'
    WHEN c.all_conversation_tags LIKE '%topic:feature_request%' THEN 'feature_request'
    WHEN c.all_conversation_tags LIKE '%topic:integration%' THEN 'integration'
    WHEN c.all_conversation_tags LIKE '%topic:success_plan%' THEN 'success_plan'
    ELSE 'other' END AS topic,
  COUNT(*) AS total
FROM conv c
JOIN company_dim co ON c.company_name = co.company_name
GROUP BY co.segment, 2
ORDER BY co.segment, total DESC
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-097/attempt-01/sql/S80.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-097/attempt-01/sql/S80.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-097/attempt-01/results/S80.rows.jsonl)；完整：True；SHA256：`fbcface6975b3046e76218f1943aa70c970764479d39675049df78271506b16e`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "intercom__company_enhanced", "kind": "base", "block": null, "base_tables": ["intercom__company_enhanced"]}] | [] | [] |
| B2 | [{"alias": "ce", "kind": "base", "block": null, "base_tables": ["intercom__conversation_enhanced"]}] | [] | [] |
| B3 | [{"alias": "c", "kind": "derived", "block": "B2", "base_tables": ["intercom__conversation_enhanced"]}, {"alias": "co", "kind": "derived", "block": "B1", "base_tables": ["intercom__company_enhanced"]}] | [{"type": "INNER", "right": "company_dim AS co", "on": "c.company_name = co.company_name", "using": []}] | ["co.segment", "CASE WHEN c.all_conversation_tags LIKE '%topic:onboarding%' THEN 'onboarding' WHEN c.all_conversation_tags LIKE '%topic:billing%' THEN 'billing' WHEN c.all_conversation_tags LIKE '%topic:usage_insight%' THEN 'usage_insight' WHEN c.all_conversation_tags LIKE '%topic:security%' THEN 'security' WHEN c.all_conversation_tags LIKE '%topic:renewal%' THEN 'renewal' WHEN c.all_conversation_tags LIKE '%topic:adoption%' THEN 'adoption' WHEN c.all_conversation_tags LIKE '%topic:escalation%' THEN 'escalation' WHEN c.all_conversation_tags LIKE '%topic:feature_request%' THEN 'feature_request' WHEN c.all_conversation_tags LIKE '%topic:integration%' THEN 'integration' WHEN c.all_conversation_tags LIKE '%topic:success_plan%' THEN 'success_plan' ELSE 'other' END"] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B3 | COUNT(*) | [] | [] | True |


## S81

类别 `data`；来源 `query_db`；调用 `0ffb71eedf7148cdaa1f78e9c378ebaa`；状态 `success`。

```sql
-- Bot ratio and SLA by segment
WITH company_dim AS (
  SELECT DISTINCT company_name,
    CASE WHEN all_company_tags LIKE '%segment:new_contract%' THEN 'new_contract'
         WHEN all_company_tags LIKE '%segment:renewal%' THEN 'renewal'
         WHEN all_company_tags LIKE '%segment:churn_watch%' THEN 'churn_watch'
         WHEN all_company_tags LIKE '%segment:expansion%' THEN 'expansion'
         ELSE 'unknown' END AS segment
  FROM intercom__company_enhanced
),
conv AS (
  SELECT ce.all_contact_company_names AS company_name, ce.all_conversation_tags
  FROM intercom__conversation_enhanced ce
)
SELECT 
  co.segment,
  COUNT(*) AS total_convs,
  ROUND(100.0 * SUM(CASE WHEN c.all_conversation_tags LIKE '%first_response:bot%' THEN 1 ELSE 0 END) / COUNT(*), 1) AS bot_pct,
  ROUND(100.0 * SUM(CASE WHEN c.all_conversation_tags LIKE '%sla:breached%' THEN 1 ELSE 0 END) / COUNT(*), 1) AS sla_breached_pct,
  ROUND(100.0 * SUM(CASE WHEN c.all_conversation_tags LIKE '%sla:met%' THEN 1 ELSE 0 END) / COUNT(*), 1) AS sla_met_pct,
  ROUND(100.0 * SUM(CASE WHEN c.all_conversation_tags LIKE '%sla:warning%' THEN 1 ELSE 0 END) / COUNT(*), 1) AS sla_warning_pct
FROM conv c
JOIN company_dim co ON c.company_name = co.company_name
GROUP BY co.segment
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-097/attempt-01/sql/S81.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-097/attempt-01/sql/S81.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-097/attempt-01/results/S81.rows.jsonl)；完整：True；SHA256：`870b12b27d0ad787bec44021bd8840077037768ca6f48bfa12a613ff8b97d0b2`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "intercom__company_enhanced", "kind": "base", "block": null, "base_tables": ["intercom__company_enhanced"]}] | [] | [] |
| B2 | [{"alias": "ce", "kind": "base", "block": null, "base_tables": ["intercom__conversation_enhanced"]}] | [] | [] |
| B3 | [{"alias": "c", "kind": "derived", "block": "B2", "base_tables": ["intercom__conversation_enhanced"]}, {"alias": "co", "kind": "derived", "block": "B1", "base_tables": ["intercom__company_enhanced"]}] | [{"type": "INNER", "right": "company_dim AS co", "on": "c.company_name = co.company_name", "using": []}] | ["co.segment"] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B3 | COUNT(*) | [] | [] | True |
| B3 | COUNT(*) | [] | [] | True |
| B3 | COUNT(*) | [] | [] | True |
| B3 | COUNT(*) | [] | [] | True |
| B3 | COUNT(*) | [] | [] | True |
| B3 | SUM(CASE WHEN c.all_conversation_tags LIKE '%first_response:bot%' THEN 1 ELSE 0 END) | [] | [{"table": "intercom__conversation_enhanced", "column": "all_conversation_tags"}] | False |
| B3 | SUM(CASE WHEN c.all_conversation_tags LIKE '%sla:breached%' THEN 1 ELSE 0 END) | [] | [{"table": "intercom__conversation_enhanced", "column": "all_conversation_tags"}] | False |
| B3 | SUM(CASE WHEN c.all_conversation_tags LIKE '%sla:met%' THEN 1 ELSE 0 END) | [] | [{"table": "intercom__conversation_enhanced", "column": "all_conversation_tags"}] | False |
| B3 | SUM(CASE WHEN c.all_conversation_tags LIKE '%sla:warning%' THEN 1 ELSE 0 END) | [] | [{"table": "intercom__conversation_enhanced", "column": "all_conversation_tags"}] | False |


## S82

类别 `data`；来源 `query_db`；调用 `bc4ca9ecd18947be95d1e0bb62435133`；状态 `success`。

```sql
-- Channel distribution by segment
WITH company_dim AS (
  SELECT DISTINCT company_name,
    CASE WHEN all_company_tags LIKE '%segment:new_contract%' THEN 'new_contract'
         WHEN all_company_tags LIKE '%segment:renewal%' THEN 'renewal'
         WHEN all_company_tags LIKE '%segment:churn_watch%' THEN 'churn_watch'
         WHEN all_company_tags LIKE '%segment:expansion%' THEN 'expansion'
         ELSE 'unknown' END AS segment
  FROM intercom__company_enhanced
),
conv AS (
  SELECT ce.all_contact_company_names AS company_name, ce.all_conversation_tags
  FROM intercom__conversation_enhanced ce
)
SELECT 
  co.segment,
  ROUND(100.0 * SUM(CASE WHEN c.all_conversation_tags LIKE '%channel:email%' THEN 1 ELSE 0 END) / COUNT(*), 1) AS email_pct,
  ROUND(100.0 * SUM(CASE WHEN c.all_conversation_tags LIKE '%channel:messenger%' THEN 1 ELSE 0 END) / COUNT(*), 1) AS messenger_pct,
  ROUND(100.0 * SUM(CASE WHEN c.all_conversation_tags LIKE '%channel:product_tour%' THEN 1 ELSE 0 END) / COUNT(*), 1) AS product_tour_pct
FROM conv c
JOIN company_dim co ON c.company_name = co.company_name
GROUP BY co.segment
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-097/attempt-01/sql/S82.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-097/attempt-01/sql/S82.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-097/attempt-01/results/S82.rows.jsonl)；完整：True；SHA256：`60e358e912843aea86499a443c16e6d4ce41a6e999c64a66fd045594fd9b1c32`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "intercom__company_enhanced", "kind": "base", "block": null, "base_tables": ["intercom__company_enhanced"]}] | [] | [] |
| B2 | [{"alias": "ce", "kind": "base", "block": null, "base_tables": ["intercom__conversation_enhanced"]}] | [] | [] |
| B3 | [{"alias": "c", "kind": "derived", "block": "B2", "base_tables": ["intercom__conversation_enhanced"]}, {"alias": "co", "kind": "derived", "block": "B1", "base_tables": ["intercom__company_enhanced"]}] | [{"type": "INNER", "right": "company_dim AS co", "on": "c.company_name = co.company_name", "using": []}] | ["co.segment"] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B3 | COUNT(*) | [] | [] | True |
| B3 | COUNT(*) | [] | [] | True |
| B3 | COUNT(*) | [] | [] | True |
| B3 | SUM(CASE WHEN c.all_conversation_tags LIKE '%channel:email%' THEN 1 ELSE 0 END) | [] | [{"table": "intercom__conversation_enhanced", "column": "all_conversation_tags"}] | False |
| B3 | SUM(CASE WHEN c.all_conversation_tags LIKE '%channel:messenger%' THEN 1 ELSE 0 END) | [] | [{"table": "intercom__conversation_enhanced", "column": "all_conversation_tags"}] | False |
| B3 | SUM(CASE WHEN c.all_conversation_tags LIKE '%channel:product_tour%' THEN 1 ELSE 0 END) | [] | [{"table": "intercom__conversation_enhanced", "column": "all_conversation_tags"}] | False |


## S83

类别 `data`；来源 `query_db`；调用 `82a21b169d8b4bcd8e95cbfe127be54f`；状态 `success`。

```sql
-- Bot vs human response times
SELECT 
  CASE WHEN all_conversation_tags LIKE '%first_response:bot%' THEN 'bot' ELSE 'human' END AS responder,
  COUNT(*) AS total,
  ROUND(AVG(time_to_first_response_minutes), 2) AS avg_resp_min,
  ROUND(AVG(time_to_last_close_minutes), 2) AS avg_duration_min,
  ROUND(100.0 * SUM(CASE WHEN all_conversation_tags LIKE '%sla:breached%' THEN 1 ELSE 0 END) / COUNT(*), 1) AS sla_breached_pct
FROM intercom__conversation_enhanced ce
JOIN intercom__conversation_metrics cm ON ce.conversation_id = cm.conversation_id
GROUP BY 1
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-097/attempt-01/sql/S83.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-097/attempt-01/sql/S83.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-097/attempt-01/results/S83.rows.jsonl)；完整：True；SHA256：`0106cb369a21a9c4b8288a0ebee7c842c91a7da26ff94eb0f3297156088b2993`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "ce", "kind": "base", "block": null, "base_tables": ["intercom__conversation_enhanced"]}, {"alias": "cm", "kind": "base", "block": null, "base_tables": ["intercom__conversation_metrics"]}] | [{"type": "INNER", "right": "intercom__conversation_metrics AS cm", "on": "ce.conversation_id = cm.conversation_id", "using": []}] | ["CASE WHEN all_conversation_tags LIKE '%first_response:bot%' THEN 'bot' ELSE 'human' END"] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |
| B1 | AVG(time_to_first_response_minutes) | [{"table": "intercom__conversation_metrics", "column": "time_to_first_response_minutes"}] | [] | False |
| B1 | AVG(time_to_last_close_minutes) | [{"table": "intercom__conversation_metrics", "column": "time_to_last_close_minutes"}] | [] | False |
| B1 | COUNT(*) | [] | [] | True |
| B1 | SUM(CASE WHEN all_conversation_tags LIKE '%sla:breached%' THEN 1 ELSE 0 END) | [] | [{"table": "intercom__conversation_enhanced", "column": "all_conversation_tags"}] | False |


## S84

类别 `data`；来源 `query_db`；调用 `f0b2ec31a1e3478e818273218ee2693f`；状态 `success`。

```sql
-- Topic mix for high-value churn_watch customers (ARR 200k+ or seats 420+)
WITH company_dim AS (
  SELECT DISTINCT company_name,
    CASE WHEN all_company_tags LIKE '%segment:new_contract%' THEN 'new_contract'
         WHEN all_company_tags LIKE '%segment:renewal%' THEN 'renewal'
         WHEN all_company_tags LIKE '%segment:churn_watch%' THEN 'churn_watch'
         WHEN all_company_tags LIKE '%segment:expansion%' THEN 'expansion'
         ELSE 'unknown' END AS segment,
    CASE WHEN all_company_tags LIKE '%arr_bucket:arr:200k_plus%' THEN 1 ELSE 0 END AS is_high_arr,
    CASE WHEN all_company_tags LIKE '%seat_bucket:seats:420_plus%' THEN 1 ELSE 0 END AS is_high_seats
  FROM intercom__company_enhanced
),
conv AS (
  SELECT ce.all_contact_company_names AS company_name, ce.all_conversation_tags
  FROM intercom__conversation_enhanced ce
)
SELECT 
  CASE WHEN co.segment='churn_watch' AND (co.is_high_arr=1 OR co.is_high_seats=1) THEN 'high_value_churn_watch'
       WHEN co.segment='new_contract' AND (co.is_high_arr=1 OR co.is_high_seats=1) THEN 'high_value_new_contract'
       ELSE co.segment END AS group_label,
  CASE 
    WHEN c.all_conversation_tags LIKE '%topic:onboarding%' THEN 'onboarding'
    WHEN c.all_conversation_tags LIKE '%topic:billing%' THEN 'billing'
    WHEN c.all_conversation_tags LIKE '%topic:usage_insight%' THEN 'usage_insight'
    WHEN c.all_conversation_tags LIKE '%topic:security%' THEN 'security'
    WHEN c.all_conversation_tags LIKE '%topic:renewal%' THEN 'renewal'
    WHEN c.all_conversation_tags LIKE '%topic:adoption%' THEN 'adoption'
    WHEN c.all_conversation_tags LIKE '%topic:escalation%' THEN 'escalation'
    WHEN c.all_conversation_tags LIKE '%topic:feature_request%' THEN 'feature_request'
    WHEN c.all_conversation_tags LIKE '%topic:integration%' THEN 'integration'
    WHEN c.all_conversation_tags LIKE '%topic:success_plan%' THEN 'success_plan'
    ELSE 'other' END AS topic,
  COUNT(*) AS total
FROM conv c
JOIN company_dim co ON c.company_name = co.company_name
WHERE co.segment IN ('churn_watch','new_contract')
GROUP BY 1, 2
ORDER BY 1, total DESC
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-097/attempt-01/sql/S84.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-097/attempt-01/sql/S84.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-097/attempt-01/results/S84.rows.jsonl)；完整：True；SHA256：`e0e13319ede24fb5de3b48b74328bf8fc9fff92e4d2f77414f7f74f83494634b`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "intercom__company_enhanced", "kind": "base", "block": null, "base_tables": ["intercom__company_enhanced"]}] | [] | [] |
| B2 | [{"alias": "ce", "kind": "base", "block": null, "base_tables": ["intercom__conversation_enhanced"]}] | [] | [] |
| B3 | [{"alias": "c", "kind": "derived", "block": "B2", "base_tables": ["intercom__conversation_enhanced"]}, {"alias": "co", "kind": "derived", "block": "B1", "base_tables": ["intercom__company_enhanced"]}] | [{"type": "INNER", "right": "company_dim AS co", "on": "c.company_name = co.company_name", "using": []}] | ["CASE WHEN co.segment = 'churn_watch' AND (co.is_high_arr = 1 OR co.is_high_seats = 1) THEN 'high_value_churn_watch' WHEN co.segment = 'new_contract' AND (co.is_high_arr = 1 OR co.is_high_seats = 1) THEN 'high_value_new_contract' ELSE co.segment END", "CASE WHEN c.all_conversation_tags LIKE '%topic:onboarding%' THEN 'onboarding' WHEN c.all_conversation_tags LIKE '%topic:billing%' THEN 'billing' WHEN c.all_conversation_tags LIKE '%topic:usage_insight%' THEN 'usage_insight' WHEN c.all_conversation_tags LIKE '%topic:security%' THEN 'security' WHEN c.all_conversation_tags LIKE '%topic:renewal%' THEN 'renewal' WHEN c.all_conversation_tags LIKE '%topic:adoption%' THEN 'adoption' WHEN c.all_conversation_tags LIKE '%topic:escalation%' THEN 'escalation' WHEN c.all_conversation_tags LIKE '%topic:feature_request%' THEN 'feature_request' WHEN c.all_conversation_tags LIKE '%topic:integration%' THEN 'integration' WHEN c.all_conversation_tags LIKE '%topic:success_plan%' THEN 'success_plan' ELSE 'other' END"] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B3 | COUNT(*) | [] | [] | True |


## S85

类别 `data`；来源 `query_db`；调用 `64344d754e8148cf83fd9cd690f13452`；状态 `success`。

```sql
-- Company-level aggregate for correlation analysis with retention
WITH company_dim AS (
  SELECT DISTINCT company_name,
    CASE WHEN all_company_tags LIKE '%segment:new_contract%' THEN 'new_contract'
         WHEN all_company_tags LIKE '%segment:renewal%' THEN 'renewal'
         WHEN all_company_tags LIKE '%segment:churn_watch%' THEN 'churn_watch'
         WHEN all_company_tags LIKE '%segment:expansion%' THEN 'expansion'
         ELSE 'unknown' END AS segment,
    CASE WHEN all_company_tags LIKE '%arr_bucket:arr:200k_plus%' THEN '200k_plus'
         WHEN all_company_tags LIKE '%arr_bucket:arr:110k_200k%' THEN '110k_200k'
         WHEN all_company_tags LIKE '%arr_bucket:arr:65k_110k%' THEN '65k_110k'
         WHEN all_company_tags LIKE '%arr_bucket:arr:30k_65k%' THEN '30k_65k'
         WHEN all_company_tags LIKE '%arr_bucket:arr:<30k%' THEN '<30k'
         ELSE 'unknown' END AS arr_bucket
  FROM intercom__company_enhanced
),
conv AS (
  SELECT 
    ce.all_contact_company_names AS company_name,
    cm.time_to_first_response_minutes AS resp_delay,
    cm.time_to_last_close_minutes AS duration,
    ce.all_conversation_tags
  FROM intercom__conversation_enhanced ce
  JOIN intercom__conversation_metrics cm ON ce.conversation_id = cm.conversation_id
),
agg AS (
  SELECT 
    c.company_name,
    COUNT(*) AS num_convs,
    AVG(c.resp_delay) AS avg_resp_delay,
    AVG(c.duration) AS avg_duration,
    SUM(CASE WHEN c.all_conversation_tags LIKE '%first_response:bot%' THEN 1 ELSE 0 END) * 1.0 / COUNT(*) AS bot_ratio,
    SUM(CASE WHEN c.all_conversation_tags LIKE '%sla:breached%' THEN 1 ELSE 0 END) * 1.0 / COUNT(*) AS sla_breach_ratio,
    SUM(CASE WHEN c.all_conversation_tags LIKE '%channel:product_tour%' THEN 1 ELSE 0 END) * 1.0 / COUNT(*) AS product_tour_ratio,
    SUM(CASE WHEN c.all_conversation_tags LIKE '%topic:usage_insight%' THEN 1 ELSE 0 END) * 1.0 / COUNT(*) AS usage_insight_ratio,
    SUM(CASE WHEN c.all_conversation_tags LIKE '%topic:adoption%' THEN 1 ELSE 0 END) * 1.0 / COUNT(*) AS adoption_ratio,
    SUM(CASE WHEN c.all_conversation_tags LIKE '%topic:escalation%' THEN 1 ELSE 0 END) * 1.0 / COUNT(*) AS escalation_ratio
  FROM conv c
  GROUP BY c.company_name
)
SELECT 
  a.*, co.segment, co.arr_bucket,
  cm.registration_retention_7d AS ret_7d,
  cm.registration_retention_30d AS ret_30d,
  cm.contacts_active_7d AS active_7d,
  cm.contacts_active_30d AS active_30d
FROM agg a
JOIN company_dim co ON a.company_name = co.company_name
JOIN intercom__company_metrics cm ON a.company_name = cm.company_name
LIMIT 3000
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-097/attempt-01/sql/S85.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-097/attempt-01/sql/S85.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-097/attempt-01/results/S85.rows.jsonl)；完整：True；SHA256：`f1b0b972a407cd4ecd78fdc181449f47cb6f4875643089b5bd6e9d9107737f5b`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "intercom__company_enhanced", "kind": "base", "block": null, "base_tables": ["intercom__company_enhanced"]}] | [] | [] |
| B2 | [{"alias": "ce", "kind": "base", "block": null, "base_tables": ["intercom__conversation_enhanced"]}, {"alias": "cm", "kind": "base", "block": null, "base_tables": ["intercom__conversation_metrics"]}] | [{"type": "INNER", "right": "intercom__conversation_metrics AS cm", "on": "ce.conversation_id = cm.conversation_id", "using": []}] | [] |
| B3 | [{"alias": "c", "kind": "derived", "block": "B2", "base_tables": ["intercom__conversation_enhanced", "intercom__conversation_metrics"]}] | [] | ["c.company_name"] |
| B4 | [{"alias": "a", "kind": "derived", "block": "B3", "base_tables": ["intercom__conversation_enhanced", "intercom__conversation_metrics"]}, {"alias": "co", "kind": "derived", "block": "B1", "base_tables": ["intercom__company_enhanced"]}, {"alias": "cm", "kind": "base", "block": null, "base_tables": ["intercom__company_metrics"]}] | [{"type": "INNER", "right": "company_dim AS co", "on": "a.company_name = co.company_name", "using": []}, {"type": "INNER", "right": "intercom__company_metrics AS cm", "on": "a.company_name = cm.company_name", "using": []}] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B3 | COUNT(*) | [] | [] | True |
| B3 | AVG(c.resp_delay) | [{"table": "intercom__conversation_metrics", "column": "time_to_first_response_minutes"}] | [] | False |
| B3 | AVG(c.duration) | [{"table": "intercom__conversation_metrics", "column": "time_to_last_close_minutes"}] | [] | False |
| B3 | COUNT(*) | [] | [] | True |
| B3 | COUNT(*) | [] | [] | True |
| B3 | COUNT(*) | [] | [] | True |
| B3 | COUNT(*) | [] | [] | True |
| B3 | COUNT(*) | [] | [] | True |
| B3 | COUNT(*) | [] | [] | True |
| B3 | SUM(CASE WHEN c.all_conversation_tags LIKE '%first_response:bot%' THEN 1 ELSE 0 END) | [] | [{"table": "intercom__conversation_enhanced", "column": "all_conversation_tags"}] | False |
| B3 | SUM(CASE WHEN c.all_conversation_tags LIKE '%sla:breached%' THEN 1 ELSE 0 END) | [] | [{"table": "intercom__conversation_enhanced", "column": "all_conversation_tags"}] | False |
| B3 | SUM(CASE WHEN c.all_conversation_tags LIKE '%channel:product_tour%' THEN 1 ELSE 0 END) | [] | [{"table": "intercom__conversation_enhanced", "column": "all_conversation_tags"}] | False |
| B3 | SUM(CASE WHEN c.all_conversation_tags LIKE '%topic:usage_insight%' THEN 1 ELSE 0 END) | [] | [{"table": "intercom__conversation_enhanced", "column": "all_conversation_tags"}] | False |
| B3 | SUM(CASE WHEN c.all_conversation_tags LIKE '%topic:adoption%' THEN 1 ELSE 0 END) | [] | [{"table": "intercom__conversation_enhanced", "column": "all_conversation_tags"}] | False |
| B3 | SUM(CASE WHEN c.all_conversation_tags LIKE '%topic:escalation%' THEN 1 ELSE 0 END) | [] | [{"table": "intercom__conversation_enhanced", "column": "all_conversation_tags"}] | False |


## S86

类别 `data`；来源 `python`；调用 `71a33c1695564ca487d0c7fff8089194`；状态 `success`。

```sql

WITH company_dim AS (
  SELECT DISTINCT company_name,
    CASE WHEN all_company_tags LIKE '%segment:new_contract%' THEN 'new_contract'
         WHEN all_company_tags LIKE '%segment:renewal%' THEN 'renewal'
         WHEN all_company_tags LIKE '%segment:churn_watch%' THEN 'churn_watch'
         WHEN all_company_tags LIKE '%segment:expansion%' THEN 'expansion'
         ELSE 'unknown' END AS segment,
    CASE WHEN all_company_tags LIKE '%arr_bucket:arr:200k_plus%' THEN '200k_plus'
         WHEN all_company_tags LIKE '%arr_bucket:arr:110k_200k%' THEN '110k_200k'
         WHEN all_company_tags LIKE '%arr_bucket:arr:65k_110k%' THEN '65k_110k'
         WHEN all_company_tags LIKE '%arr_bucket:arr:30k_65k%' THEN '30k_65k'
         WHEN all_company_tags LIKE '%arr_bucket:arr:<30k%' THEN '<30k'
         ELSE 'unknown' END AS arr_bucket,
    CASE WHEN all_company_tags LIKE '%seat_bucket:seats:under_60%' THEN 'under_60'
         WHEN all_company_tags LIKE '%seat_bucket:seats:60_129%' THEN '60_129'
         WHEN all_company_tags LIKE '%seat_bucket:seats:130_259%' THEN '130_259'
         WHEN all_company_tags LIKE '%seat_bucket:seats:260_419%' THEN '260_419'
         WHEN all_company_tags LIKE '%seat_bucket:seats:420_plus%' THEN '420_plus'
         ELSE 'unknown' END AS seat_bucket
  FROM intercom__company_enhanced
),
conv AS (
  SELECT 
    ce.all_contact_company_names AS company_name,
    cm.time_to_first_response_minutes AS resp_delay,
    cm.time_to_last_close_minutes AS duration,
    ce.all_conversation_tags
  FROM intercom__conversation_enhanced ce
  JOIN intercom__conversation_metrics cm ON ce.conversation_id = cm.conversation_id
  WHERE cm.time_to_last_close_minutes BETWEEN 91 AND 1030
    AND cm.time_to_first_response_minutes BETWEEN 11 AND 42
),
agg AS (
  SELECT 
    c.company_name,
    COUNT(*) AS num_convs,
    AVG(c.resp_delay) AS avg_resp_delay,
    AVG(c.duration) AS avg_duration,
    SUM(CASE WHEN c.all_conversation_tags LIKE '%first_response:bot%' THEN 1 ELSE 0 END) * 1.0 / COUNT(*) AS bot_ratio,
    SUM(CASE WHEN c.all_conversation_tags LIKE '%sla:breached%' THEN 1 ELSE 0 END) * 1.0 / COUNT(*) AS sla_breach_ratio,
    SUM(CASE WHEN c.all_conversation_tags LIKE '%channel:product_tour%' THEN 1 ELSE 0 END) * 1.0 / COUNT(*) AS product_tour_ratio,
    SUM(CASE WHEN c.all_conversation_tags LIKE '%topic:usage_insight%' THEN 1 ELSE 0 END) * 1.0 / COUNT(*) AS usage_insight_ratio,
    SUM(CASE WHEN c.all_conversation_tags LIKE '%topic:adoption%' THEN 1 ELSE 0 END) * 1.0 / COUNT(*) AS adoption_ratio,
    SUM(CASE WHEN c.all_conversation_tags LIKE '%topic:escalation%' THEN 1 ELSE 0 END) * 1.0 / COUNT(*) AS escalation_ratio
  FROM conv c
  GROUP BY c.company_name
)
SELECT 
  a.*, co.segment, co.arr_bucket, co.seat_bucket,
  cm.registration_retention_7d AS ret_7d,
  cm.registration_retention_30d AS ret_30d,
  cm.contacts_active_7d AS active_7d,
  cm.contacts_active_30d AS active_30d
FROM agg a
JOIN company_dim co ON a.company_name = co.company_name
JOIN intercom__company_metrics cm ON a.company_name = cm.company_name

```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-097/attempt-01/sql/S86.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-097/attempt-01/sql/S86.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-097/attempt-01/results/S86.rows.jsonl)；完整：True；SHA256：`fc7f15219e93913a7d39c1192593d3f87f091206afc1a11d162b7940e840194b`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "intercom__company_enhanced", "kind": "base", "block": null, "base_tables": ["intercom__company_enhanced"]}] | [] | [] |
| B2 | [{"alias": "ce", "kind": "base", "block": null, "base_tables": ["intercom__conversation_enhanced"]}, {"alias": "cm", "kind": "base", "block": null, "base_tables": ["intercom__conversation_metrics"]}] | [{"type": "INNER", "right": "intercom__conversation_metrics AS cm", "on": "ce.conversation_id = cm.conversation_id", "using": []}] | [] |
| B3 | [{"alias": "c", "kind": "derived", "block": "B2", "base_tables": ["intercom__conversation_enhanced", "intercom__conversation_metrics"]}] | [] | ["c.company_name"] |
| B4 | [{"alias": "a", "kind": "derived", "block": "B3", "base_tables": ["intercom__conversation_enhanced", "intercom__conversation_metrics"]}, {"alias": "co", "kind": "derived", "block": "B1", "base_tables": ["intercom__company_enhanced"]}, {"alias": "cm", "kind": "base", "block": null, "base_tables": ["intercom__company_metrics"]}] | [{"type": "INNER", "right": "company_dim AS co", "on": "a.company_name = co.company_name", "using": []}, {"type": "INNER", "right": "intercom__company_metrics AS cm", "on": "a.company_name = cm.company_name", "using": []}] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B3 | COUNT(*) | [] | [] | True |
| B3 | AVG(c.resp_delay) | [{"table": "intercom__conversation_metrics", "column": "time_to_first_response_minutes"}] | [] | False |
| B3 | AVG(c.duration) | [{"table": "intercom__conversation_metrics", "column": "time_to_last_close_minutes"}] | [] | False |
| B3 | COUNT(*) | [] | [] | True |
| B3 | COUNT(*) | [] | [] | True |
| B3 | COUNT(*) | [] | [] | True |
| B3 | COUNT(*) | [] | [] | True |
| B3 | COUNT(*) | [] | [] | True |
| B3 | COUNT(*) | [] | [] | True |
| B3 | SUM(CASE WHEN c.all_conversation_tags LIKE '%first_response:bot%' THEN 1 ELSE 0 END) | [] | [{"table": "intercom__conversation_enhanced", "column": "all_conversation_tags"}] | False |
| B3 | SUM(CASE WHEN c.all_conversation_tags LIKE '%sla:breached%' THEN 1 ELSE 0 END) | [] | [{"table": "intercom__conversation_enhanced", "column": "all_conversation_tags"}] | False |
| B3 | SUM(CASE WHEN c.all_conversation_tags LIKE '%channel:product_tour%' THEN 1 ELSE 0 END) | [] | [{"table": "intercom__conversation_enhanced", "column": "all_conversation_tags"}] | False |
| B3 | SUM(CASE WHEN c.all_conversation_tags LIKE '%topic:usage_insight%' THEN 1 ELSE 0 END) | [] | [{"table": "intercom__conversation_enhanced", "column": "all_conversation_tags"}] | False |
| B3 | SUM(CASE WHEN c.all_conversation_tags LIKE '%topic:adoption%' THEN 1 ELSE 0 END) | [] | [{"table": "intercom__conversation_enhanced", "column": "all_conversation_tags"}] | False |
| B3 | SUM(CASE WHEN c.all_conversation_tags LIKE '%topic:escalation%' THEN 1 ELSE 0 END) | [] | [{"table": "intercom__conversation_enhanced", "column": "all_conversation_tags"}] | False |


## S87

类别 `data`；来源 `python`；调用 `41873d5da4b64b24bb226366c254d219`；状态 `success`。

```sql

WITH company_dim AS (
  SELECT DISTINCT company_name,
    CASE WHEN all_company_tags LIKE '%segment:new_contract%' THEN 'new_contract'
         WHEN all_company_tags LIKE '%segment:renewal%' THEN 'renewal'
         WHEN all_company_tags LIKE '%segment:churn_watch%' THEN 'churn_watch'
         WHEN all_company_tags LIKE '%segment:expansion%' THEN 'expansion'
         ELSE 'unknown' END AS segment
  FROM intercom__company_enhanced
),
conv AS (
  SELECT 
    ce.conversation_id, ce.all_contact_company_names AS company_name,
    cm.time_to_first_response_minutes AS resp_delay,
    cm.time_to_last_close_minutes AS duration,
    ce.all_conversation_tags
  FROM intercom__conversation_enhanced ce
  JOIN intercom__conversation_metrics cm ON ce.conversation_id = cm.conversation_id
  WHERE cm.time_to_last_close_minutes BETWEEN 91 AND 1030
    AND cm.time_to_first_response_minutes BETWEEN 11 AND 42
)
SELECT 
  co.segment,
  COUNT(*) AS total_convs,
  COUNT(DISTINCT c.company_name) AS customers,
  AVG(c.resp_delay) AS avg_resp_delay_min,
  AVG(c.duration) AS avg_duration_min,
  100.0 * SUM(CASE WHEN c.all_conversation_tags LIKE '%first_response:bot%' THEN 1 ELSE 0 END) / COUNT(*) AS bot_ratio_pct,
  100.0 * SUM(CASE WHEN c.all_conversation_tags LIKE '%sla:breached%' THEN 1 ELSE 0 END) / COUNT(*) AS sla_breach_pct
FROM conv c
JOIN company_dim co ON c.company_name = co.company_name
GROUP BY co.segment
ORDER BY co.segment

```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-097/attempt-01/sql/S87.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-097/attempt-01/sql/S87.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-097/attempt-01/results/S87.rows.jsonl)；完整：True；SHA256：`0290a29da9075b8f0e2237aa7b61634a4cbf20e5e0423860ee39b57dfab3525a`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "intercom__company_enhanced", "kind": "base", "block": null, "base_tables": ["intercom__company_enhanced"]}] | [] | [] |
| B2 | [{"alias": "ce", "kind": "base", "block": null, "base_tables": ["intercom__conversation_enhanced"]}, {"alias": "cm", "kind": "base", "block": null, "base_tables": ["intercom__conversation_metrics"]}] | [{"type": "INNER", "right": "intercom__conversation_metrics AS cm", "on": "ce.conversation_id = cm.conversation_id", "using": []}] | [] |
| B3 | [{"alias": "c", "kind": "derived", "block": "B2", "base_tables": ["intercom__conversation_enhanced", "intercom__conversation_metrics"]}, {"alias": "co", "kind": "derived", "block": "B1", "base_tables": ["intercom__company_enhanced"]}] | [{"type": "INNER", "right": "company_dim AS co", "on": "c.company_name = co.company_name", "using": []}] | ["co.segment"] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B3 | COUNT(*) | [] | [] | True |
| B3 | COUNT(DISTINCT c.company_name) | [{"table": "intercom__conversation_enhanced", "column": "all_contact_company_names"}] | [] | False |
| B3 | AVG(c.resp_delay) | [{"table": "intercom__conversation_metrics", "column": "time_to_first_response_minutes"}] | [] | False |
| B3 | AVG(c.duration) | [{"table": "intercom__conversation_metrics", "column": "time_to_last_close_minutes"}] | [] | False |
| B3 | COUNT(*) | [] | [] | True |
| B3 | COUNT(*) | [] | [] | True |
| B3 | SUM(CASE WHEN c.all_conversation_tags LIKE '%first_response:bot%' THEN 1 ELSE 0 END) | [] | [{"table": "intercom__conversation_enhanced", "column": "all_conversation_tags"}] | False |
| B3 | SUM(CASE WHEN c.all_conversation_tags LIKE '%sla:breached%' THEN 1 ELSE 0 END) | [] | [{"table": "intercom__conversation_enhanced", "column": "all_conversation_tags"}] | False |


## S88

类别 `data`；来源 `python`；调用 `41873d5da4b64b24bb226366c254d219`；状态 `success`。

```sql

WITH company_dim AS (
  SELECT DISTINCT company_name,
    CASE WHEN all_company_tags LIKE '%segment:new_contract%' THEN 'new_contract'
         WHEN all_company_tags LIKE '%segment:renewal%' THEN 'renewal'
         WHEN all_company_tags LIKE '%segment:churn_watch%' THEN 'churn_watch'
         WHEN all_company_tags LIKE '%segment:expansion%' THEN 'expansion'
         ELSE 'unknown' END AS segment
  FROM intercom__company_enhanced
)
SELECT 
  cd.segment,
  COUNT(*) AS companies,
  AVG(cm.registration_retention_7d) AS weekly_retention,
  AVG(cm.registration_retention_30d) AS monthly_retention
FROM company_dim cd
JOIN intercom__company_metrics cm ON cd.company_name = cm.company_name
GROUP BY cd.segment
ORDER BY cd.segment

```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-097/attempt-01/sql/S88.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-097/attempt-01/sql/S88.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-097/attempt-01/results/S88.rows.jsonl)；完整：True；SHA256：`1d70af49106b14dcdf13c12036d1959f6f38bd07292ea259a2c7df4186db7a84`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "intercom__company_enhanced", "kind": "base", "block": null, "base_tables": ["intercom__company_enhanced"]}] | [] | [] |
| B2 | [{"alias": "cd", "kind": "derived", "block": "B1", "base_tables": ["intercom__company_enhanced"]}, {"alias": "cm", "kind": "base", "block": null, "base_tables": ["intercom__company_metrics"]}] | [{"type": "INNER", "right": "intercom__company_metrics AS cm", "on": "cd.company_name = cm.company_name", "using": []}] | ["cd.segment"] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B2 | COUNT(*) | [] | [] | True |
| B2 | AVG(cm.registration_retention_7d) | [{"table": "intercom__company_metrics", "column": "registration_retention_7d"}] | [] | False |
| B2 | AVG(cm.registration_retention_30d) | [{"table": "intercom__company_metrics", "column": "registration_retention_30d"}] | [] | False |


## S89

类别 `data`；来源 `python`；调用 `41873d5da4b64b24bb226366c254d219`；状态 `success`。

```sql

WITH company_dim AS (
  SELECT DISTINCT company_name,
    CASE WHEN all_company_tags LIKE '%segment:new_contract%' THEN 'new_contract'
         WHEN all_company_tags LIKE '%segment:renewal%' THEN 'renewal'
         WHEN all_company_tags LIKE '%segment:churn_watch%' THEN 'churn_watch'
         WHEN all_company_tags LIKE '%segment:expansion%' THEN 'expansion'
         ELSE 'unknown' END AS segment
  FROM intercom__company_enhanced
),
conv_end AS (
  SELECT DISTINCT all_contact_company_names AS company_name, last_close_at
  FROM intercom__conversation_enhanced WHERE last_close_at IS NOT NULL
),
contact_act AS (
  SELECT all_contact_company_names AS company_name, last_activity_ts
  FROM intercom__contact_enhanced WHERE last_activity_ts IS NOT NULL
),
converted AS (
  SELECT DISTINCT c.company_name
  FROM conv_end c JOIN contact_act a ON c.company_name = a.company_name
  WHERE a.last_activity_ts >= c.last_close_at 
    AND a.last_activity_ts <= datetime(c.last_close_at, '+72 hours')
)
SELECT 
  cd.segment,
  COUNT(DISTINCT cd.company_name) AS total_customers,
  COUNT(DISTINCT cv.company_name) AS customers_converted,
  100.0 * COUNT(DISTINCT cv.company_name) / COUNT(DISTINCT cd.company_name) AS conversion_rate_pct
FROM company_dim cd
LEFT JOIN converted cv ON cd.company_name = cv.company_name
GROUP BY cd.segment
ORDER BY cd.segment

```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-097/attempt-01/sql/S89.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-097/attempt-01/sql/S89.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-097/attempt-01/results/S89.rows.jsonl)；完整：True；SHA256：`2a64d00e0c15d83c2b478d02ab92d89b5f010d517d58bf1d86d8ca4d36746299`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "intercom__company_enhanced", "kind": "base", "block": null, "base_tables": ["intercom__company_enhanced"]}] | [] | [] |
| B2 | [{"alias": "intercom__conversation_enhanced", "kind": "base", "block": null, "base_tables": ["intercom__conversation_enhanced"]}] | [] | [] |
| B3 | [{"alias": "intercom__contact_enhanced", "kind": "base", "block": null, "base_tables": ["intercom__contact_enhanced"]}] | [] | [] |
| B4 | [{"alias": "c", "kind": "derived", "block": "B2", "base_tables": ["intercom__conversation_enhanced"]}, {"alias": "a", "kind": "derived", "block": "B3", "base_tables": ["intercom__contact_enhanced"]}] | [{"type": "INNER", "right": "contact_act AS a", "on": "c.company_name = a.company_name", "using": []}] | [] |
| B5 | [{"alias": "cd", "kind": "derived", "block": "B1", "base_tables": ["intercom__company_enhanced"]}, {"alias": "cv", "kind": "derived", "block": "B4", "base_tables": ["intercom__contact_enhanced", "intercom__conversation_enhanced"]}] | [{"type": "LEFT", "right": "converted AS cv", "on": "cd.company_name = cv.company_name", "using": []}] | ["cd.segment"] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B5 | COUNT(DISTINCT cd.company_name) | [{"table": "intercom__company_enhanced", "column": "company_name"}] | [] | False |
| B5 | COUNT(DISTINCT cv.company_name) | [{"table": "intercom__conversation_enhanced", "column": "all_contact_company_names"}] | [] | False |
| B5 | COUNT(DISTINCT cd.company_name) | [{"table": "intercom__company_enhanced", "column": "company_name"}] | [] | False |
| B5 | COUNT(DISTINCT cv.company_name) | [{"table": "intercom__conversation_enhanced", "column": "all_contact_company_names"}] | [] | False |


## S90

类别 `data`；来源 `python`；调用 `f91593ea8e5c4fa1ab198f29cabd9547`；状态 `success`。

```sql

WITH company_dim AS (
  SELECT DISTINCT company_name,
    CASE WHEN all_company_tags LIKE '%arr_bucket:arr:<30k%' THEN '<30k'
         WHEN all_company_tags LIKE '%arr_bucket:arr:30k_65k%' THEN '30k_65k'
         WHEN all_company_tags LIKE '%arr_bucket:arr:65k_110k%' THEN '65k_110k'
         WHEN all_company_tags LIKE '%arr_bucket:arr:110k_200k%' THEN '110k_200k'
         WHEN all_company_tags LIKE '%arr_bucket:arr:200k_plus%' THEN '200k_plus'
         ELSE 'unknown' END AS arr_bucket
  FROM intercom__company_enhanced
),
conv AS (
  SELECT 
    ce.all_contact_company_names AS company_name,
    cm.time_to_first_response_minutes AS resp_delay,
    cm.time_to_last_close_minutes AS duration,
    ce.all_conversation_tags
  FROM intercom__conversation_enhanced ce
  JOIN intercom__conversation_metrics cm ON ce.conversation_id = cm.conversation_id
  WHERE cm.time_to_last_close_minutes BETWEEN 91 AND 1030
    AND cm.time_to_first_response_minutes BETWEEN 11 AND 42
),
agg AS (
  SELECT 
    c.company_name,
    COUNT(*) AS num_convs,
    AVG(c.resp_delay) AS avg_resp_delay,
    AVG(c.duration) AS avg_duration,
    SUM(CASE WHEN c.all_conversation_tags LIKE '%first_response:bot%' THEN 1 ELSE 0 END) * 100.0 / COUNT(*) AS bot_ratio
  FROM conv c
  GROUP BY c.company_name
)
SELECT 
  co.arr_bucket,
  AVG(agg.num_convs) AS avg_convs_per_company,
  AVG(agg.avg_resp_delay) AS avg_resp_delay,
  AVG(agg.avg_duration) AS avg_duration,
  AVG(agg.bot_ratio) AS avg_bot_ratio_pct
FROM agg
JOIN company_dim co ON agg.company_name = co.company_name
GROUP BY co.arr_bucket
ORDER BY co.arr_bucket

```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-097/attempt-01/sql/S90.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-097/attempt-01/sql/S90.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-097/attempt-01/results/S90.rows.jsonl)；完整：True；SHA256：`9aefb489b55d376822e7d48b47d755f1c6bcd23f178ed32aeddbcc784479670e`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "intercom__company_enhanced", "kind": "base", "block": null, "base_tables": ["intercom__company_enhanced"]}] | [] | [] |
| B2 | [{"alias": "ce", "kind": "base", "block": null, "base_tables": ["intercom__conversation_enhanced"]}, {"alias": "cm", "kind": "base", "block": null, "base_tables": ["intercom__conversation_metrics"]}] | [{"type": "INNER", "right": "intercom__conversation_metrics AS cm", "on": "ce.conversation_id = cm.conversation_id", "using": []}] | [] |
| B3 | [{"alias": "c", "kind": "derived", "block": "B2", "base_tables": ["intercom__conversation_enhanced", "intercom__conversation_metrics"]}] | [] | ["c.company_name"] |
| B4 | [{"alias": "agg", "kind": "derived", "block": "B3", "base_tables": ["intercom__conversation_enhanced", "intercom__conversation_metrics"]}, {"alias": "co", "kind": "derived", "block": "B1", "base_tables": ["intercom__company_enhanced"]}] | [{"type": "INNER", "right": "company_dim AS co", "on": "agg.company_name = co.company_name", "using": []}] | ["co.arr_bucket"] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B3 | COUNT(*) | [] | [] | True |
| B3 | AVG(c.resp_delay) | [{"table": "intercom__conversation_metrics", "column": "time_to_first_response_minutes"}] | [] | False |
| B3 | AVG(c.duration) | [{"table": "intercom__conversation_metrics", "column": "time_to_last_close_minutes"}] | [] | False |
| B3 | COUNT(*) | [] | [] | True |
| B3 | SUM(CASE WHEN c.all_conversation_tags LIKE '%first_response:bot%' THEN 1 ELSE 0 END) | [] | [{"table": "intercom__conversation_enhanced", "column": "all_conversation_tags"}] | False |
| B4 | AVG(agg.num_convs) | [] | [] | False |
| B4 | AVG(agg.avg_resp_delay) | [{"table": "intercom__conversation_metrics", "column": "time_to_first_response_minutes"}] | [] | False |
| B4 | AVG(agg.avg_duration) | [{"table": "intercom__conversation_metrics", "column": "time_to_last_close_minutes"}] | [] | False |
| B4 | AVG(agg.bot_ratio) | [{"table": "intercom__conversation_enhanced", "column": "all_conversation_tags"}] | [] | False |


## S91

类别 `data`；来源 `python`；调用 `f91593ea8e5c4fa1ab198f29cabd9547`；状态 `success`。

```sql

WITH company_dim AS (
  SELECT DISTINCT company_name,
    CASE WHEN all_company_tags LIKE '%seat_bucket:seats:under_60%' THEN 'under_60'
         WHEN all_company_tags LIKE '%seat_bucket:seats:60_129%' THEN '60_129'
         WHEN all_company_tags LIKE '%seat_bucket:seats:130_259%' THEN '130_259'
         WHEN all_company_tags LIKE '%seat_bucket:seats:260_419%' THEN '260_419'
         WHEN all_company_tags LIKE '%seat_bucket:seats:420_plus%' THEN '420_plus'
         ELSE 'unknown' END AS seat_bucket
  FROM intercom__company_enhanced
),
conv AS (
  SELECT 
    ce.all_contact_company_names AS company_name,
    cm.time_to_first_response_minutes AS resp_delay,
    cm.time_to_last_close_minutes AS duration,
    ce.all_conversation_tags
  FROM intercom__conversation_enhanced ce
  JOIN intercom__conversation_metrics cm ON ce.conversation_id = cm.conversation_id
  WHERE cm.time_to_last_close_minutes BETWEEN 91 AND 1030
    AND cm.time_to_first_response_minutes BETWEEN 11 AND 42
),
agg AS (
  SELECT 
    c.company_name,
    COUNT(*) AS num_convs,
    AVG(c.resp_delay) AS avg_resp_delay,
    AVG(c.duration) AS avg_duration,
    SUM(CASE WHEN c.all_conversation_tags LIKE '%first_response:bot%' THEN 1 ELSE 0 END) * 100.0 / COUNT(*) AS bot_ratio
  FROM conv c
  GROUP BY c.company_name
)
SELECT 
  co.seat_bucket,
  AVG(agg.num_convs) AS avg_convs_per_company,
  AVG(agg.avg_resp_delay) AS avg_resp_delay,
  AVG(agg.avg_duration) AS avg_duration,
  AVG(agg.bot_ratio) AS avg_bot_ratio_pct
FROM agg
JOIN company_dim co ON agg.company_name = co.company_name
GROUP BY co.seat_bucket
ORDER BY co.seat_bucket

```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-097/attempt-01/sql/S91.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-097/attempt-01/sql/S91.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-097/attempt-01/results/S91.rows.jsonl)；完整：True；SHA256：`3d37bd7a4afabcc523bbb185977ac4f89cc019c3e74fc34939e77716f68942c4`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "intercom__company_enhanced", "kind": "base", "block": null, "base_tables": ["intercom__company_enhanced"]}] | [] | [] |
| B2 | [{"alias": "ce", "kind": "base", "block": null, "base_tables": ["intercom__conversation_enhanced"]}, {"alias": "cm", "kind": "base", "block": null, "base_tables": ["intercom__conversation_metrics"]}] | [{"type": "INNER", "right": "intercom__conversation_metrics AS cm", "on": "ce.conversation_id = cm.conversation_id", "using": []}] | [] |
| B3 | [{"alias": "c", "kind": "derived", "block": "B2", "base_tables": ["intercom__conversation_enhanced", "intercom__conversation_metrics"]}] | [] | ["c.company_name"] |
| B4 | [{"alias": "agg", "kind": "derived", "block": "B3", "base_tables": ["intercom__conversation_enhanced", "intercom__conversation_metrics"]}, {"alias": "co", "kind": "derived", "block": "B1", "base_tables": ["intercom__company_enhanced"]}] | [{"type": "INNER", "right": "company_dim AS co", "on": "agg.company_name = co.company_name", "using": []}] | ["co.seat_bucket"] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B3 | COUNT(*) | [] | [] | True |
| B3 | AVG(c.resp_delay) | [{"table": "intercom__conversation_metrics", "column": "time_to_first_response_minutes"}] | [] | False |
| B3 | AVG(c.duration) | [{"table": "intercom__conversation_metrics", "column": "time_to_last_close_minutes"}] | [] | False |
| B3 | COUNT(*) | [] | [] | True |
| B3 | SUM(CASE WHEN c.all_conversation_tags LIKE '%first_response:bot%' THEN 1 ELSE 0 END) | [] | [{"table": "intercom__conversation_enhanced", "column": "all_conversation_tags"}] | False |
| B4 | AVG(agg.num_convs) | [] | [] | False |
| B4 | AVG(agg.avg_resp_delay) | [{"table": "intercom__conversation_metrics", "column": "time_to_first_response_minutes"}] | [] | False |
| B4 | AVG(agg.avg_duration) | [{"table": "intercom__conversation_metrics", "column": "time_to_last_close_minutes"}] | [] | False |
| B4 | AVG(agg.bot_ratio) | [{"table": "intercom__conversation_enhanced", "column": "all_conversation_tags"}] | [] | False |


## S92

类别 `data`；来源 `python`；调用 `f91593ea8e5c4fa1ab198f29cabd9547`；状态 `success`。

```sql

WITH company_dim AS (
  SELECT DISTINCT company_name,
    CASE WHEN all_company_tags LIKE '%arr_bucket:arr:<30k%' THEN '<30k'
         WHEN all_company_tags LIKE '%arr_bucket:arr:30k_65k%' THEN '30k_65k'
         WHEN all_company_tags LIKE '%arr_bucket:arr:65k_110k%' THEN '65k_110k'
         WHEN all_company_tags LIKE '%arr_bucket:arr:110k_200k%' THEN '110k_200k'
         WHEN all_company_tags LIKE '%arr_bucket:arr:200k_plus%' THEN '200k_plus'
         ELSE 'unknown' END AS arr_bucket
  FROM intercom__company_enhanced
)
SELECT 
  cd.arr_bucket,
  AVG(cm.registration_retention_7d) AS weekly_retention,
  AVG(cm.registration_retention_30d) AS monthly_retention,
  AVG(cm.contacts_active_7d) AS avg_active_7d,
  AVG(cm.contacts_active_30d) AS avg_active_30d
FROM company_dim cd
JOIN intercom__company_metrics cm ON cd.company_name = cm.company_name
GROUP BY cd.arr_bucket
ORDER BY cd.arr_bucket

```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-097/attempt-01/sql/S92.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-097/attempt-01/sql/S92.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-097/attempt-01/results/S92.rows.jsonl)；完整：True；SHA256：`88a8c9fc9717208a1bb7044e30e53e6a3da97a1b11b1ab4c1cfd43822e5b3391`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "intercom__company_enhanced", "kind": "base", "block": null, "base_tables": ["intercom__company_enhanced"]}] | [] | [] |
| B2 | [{"alias": "cd", "kind": "derived", "block": "B1", "base_tables": ["intercom__company_enhanced"]}, {"alias": "cm", "kind": "base", "block": null, "base_tables": ["intercom__company_metrics"]}] | [{"type": "INNER", "right": "intercom__company_metrics AS cm", "on": "cd.company_name = cm.company_name", "using": []}] | ["cd.arr_bucket"] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B2 | AVG(cm.registration_retention_7d) | [{"table": "intercom__company_metrics", "column": "registration_retention_7d"}] | [] | False |
| B2 | AVG(cm.registration_retention_30d) | [{"table": "intercom__company_metrics", "column": "registration_retention_30d"}] | [] | False |
| B2 | AVG(cm.contacts_active_7d) | [{"table": "intercom__company_metrics", "column": "contacts_active_7d"}] | [] | False |
| B2 | AVG(cm.contacts_active_30d) | [{"table": "intercom__company_metrics", "column": "contacts_active_30d"}] | [] | False |


## S93

类别 `data`；来源 `python`；调用 `f91593ea8e5c4fa1ab198f29cabd9547`；状态 `success`。

```sql

WITH company_dim AS (
  SELECT DISTINCT company_name,
    CASE WHEN all_company_tags LIKE '%seat_bucket:seats:under_60%' THEN 'under_60'
         WHEN all_company_tags LIKE '%seat_bucket:seats:60_129%' THEN '60_129'
         WHEN all_company_tags LIKE '%seat_bucket:seats:130_259%' THEN '130_259'
         WHEN all_company_tags LIKE '%seat_bucket:seats:260_419%' THEN '260_419'
         WHEN all_company_tags LIKE '%seat_bucket:seats:420_plus%' THEN '420_plus'
         ELSE 'unknown' END AS seat_bucket
  FROM intercom__company_enhanced
)
SELECT 
  cd.seat_bucket,
  AVG(cm.registration_retention_7d) AS weekly_retention,
  AVG(cm.registration_retention_30d) AS monthly_retention,
  AVG(cm.contacts_active_7d) AS avg_active_7d,
  AVG(cm.contacts_active_30d) AS avg_active_30d
FROM company_dim cd
JOIN intercom__company_metrics cm ON cd.company_name = cm.company_name
GROUP BY cd.seat_bucket
ORDER BY cd.seat_bucket

```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-097/attempt-01/sql/S93.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-097/attempt-01/sql/S93.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-097/attempt-01/results/S93.rows.jsonl)；完整：True；SHA256：`858f3fc86146e0baec2b565df01cba7636512e51440954d79f939b7560a1a73e`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "intercom__company_enhanced", "kind": "base", "block": null, "base_tables": ["intercom__company_enhanced"]}] | [] | [] |
| B2 | [{"alias": "cd", "kind": "derived", "block": "B1", "base_tables": ["intercom__company_enhanced"]}, {"alias": "cm", "kind": "base", "block": null, "base_tables": ["intercom__company_metrics"]}] | [{"type": "INNER", "right": "intercom__company_metrics AS cm", "on": "cd.company_name = cm.company_name", "using": []}] | ["cd.seat_bucket"] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B2 | AVG(cm.registration_retention_7d) | [{"table": "intercom__company_metrics", "column": "registration_retention_7d"}] | [] | False |
| B2 | AVG(cm.registration_retention_30d) | [{"table": "intercom__company_metrics", "column": "registration_retention_30d"}] | [] | False |
| B2 | AVG(cm.contacts_active_7d) | [{"table": "intercom__company_metrics", "column": "contacts_active_7d"}] | [] | False |
| B2 | AVG(cm.contacts_active_30d) | [{"table": "intercom__company_metrics", "column": "contacts_active_30d"}] | [] | False |


## S94

类别 `data`；来源 `python`；调用 `f1423a75f817459da523383f9d0ddb2d`；状态 `failed`。

```sql

SELECT 
  strftime('%Y-%m', conversation_created_at) AS month,
  COUNT(*) AS total_convs,
  AVG(time_to_first_response_minutes) AS avg_resp_delay,
  AVG(time_to_last_close_minutes) AS avg_duration,
  100.0 * SUM(CASE WHEN all_conversation_tags LIKE '%first_response:bot%' THEN 1 ELSE 0 END) / COUNT(*) AS bot_pct
FROM intercom__conversation_enhanced ce
JOIN intercom__conversation_metrics cm ON ce.conversation_id = cm.conversation_id
WHERE cm.time_to_last_close_minutes BETWEEN 91 AND 1030
  AND cm.time_to_first_response_minutes BETWEEN 11 AND 42
GROUP BY strftime('%Y-%m', conversation_created_at)
ORDER BY month

```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-097/attempt-01/sql/S94.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-097/attempt-01/sql/S94.parameters.json)。

错误：`OperationalError('ambiguous column name: conversation_created_at')`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "ce", "kind": "base", "block": null, "base_tables": ["intercom__conversation_enhanced"]}, {"alias": "cm", "kind": "base", "block": null, "base_tables": ["intercom__conversation_metrics"]}] | [{"type": "INNER", "right": "intercom__conversation_metrics AS cm", "on": "ce.conversation_id = cm.conversation_id", "using": []}] | ["STRFTIME('%Y-%m', conversation_created_at)"] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |
| B1 | AVG(time_to_first_response_minutes) | [{"table": "intercom__conversation_metrics", "column": "time_to_first_response_minutes"}] | [] | False |
| B1 | AVG(time_to_last_close_minutes) | [{"table": "intercom__conversation_metrics", "column": "time_to_last_close_minutes"}] | [] | False |
| B1 | COUNT(*) | [] | [] | True |
| B1 | SUM(CASE WHEN all_conversation_tags LIKE '%first_response:bot%' THEN 1 ELSE 0 END) | [] | [{"table": "intercom__conversation_enhanced", "column": "all_conversation_tags"}] | False |


未解析列血缘：[{"block": "B1", "column": "conversation_created_at", "reason": "ambiguous_or_missing_source"}, {"block": "B1", "column": "conversation_created_at", "reason": "ambiguous_or_missing_source"}, {"block": "B1", "column": "conversation_created_at", "reason": "ambiguous_or_missing_source"}]

## S95

类别 `data`；来源 `query_db`；调用 `1e147fb9b072448787170e89a60cb20a`；状态 `failed`。

```sql
SELECT 
  strftime('%Y-%m', conversation_created_at) AS month,
  COUNT(*) AS total_convs,
  ROUND(AVG(time_to_first_response_minutes),2) AS avg_resp_delay,
  ROUND(AVG(time_to_last_close_minutes),2) AS avg_duration,
  ROUND(100.0 * SUM(CASE WHEN all_conversation_tags LIKE '%first_response:bot%' THEN 1 ELSE 0 END) / COUNT(*), 2) AS bot_pct
FROM intercom__conversation_enhanced ce
JOIN intercom__conversation_metrics cm ON ce.conversation_id = cm.conversation_id
WHERE cm.time_to_last_close_minutes BETWEEN 91 AND 1030
  AND cm.time_to_first_response_minutes BETWEEN 11 AND 42
GROUP BY strftime('%Y-%m', conversation_created_at)
ORDER BY month
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-097/attempt-01/sql/S95.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-097/attempt-01/sql/S95.parameters.json)。

错误：`OperationalError('ambiguous column name: conversation_created_at')`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "ce", "kind": "base", "block": null, "base_tables": ["intercom__conversation_enhanced"]}, {"alias": "cm", "kind": "base", "block": null, "base_tables": ["intercom__conversation_metrics"]}] | [{"type": "INNER", "right": "intercom__conversation_metrics AS cm", "on": "ce.conversation_id = cm.conversation_id", "using": []}] | ["STRFTIME('%Y-%m', conversation_created_at)"] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |
| B1 | AVG(time_to_first_response_minutes) | [{"table": "intercom__conversation_metrics", "column": "time_to_first_response_minutes"}] | [] | False |
| B1 | AVG(time_to_last_close_minutes) | [{"table": "intercom__conversation_metrics", "column": "time_to_last_close_minutes"}] | [] | False |
| B1 | COUNT(*) | [] | [] | True |
| B1 | SUM(CASE WHEN all_conversation_tags LIKE '%first_response:bot%' THEN 1 ELSE 0 END) | [] | [{"table": "intercom__conversation_enhanced", "column": "all_conversation_tags"}] | False |


未解析列血缘：[{"block": "B1", "column": "conversation_created_at", "reason": "ambiguous_or_missing_source"}, {"block": "B1", "column": "conversation_created_at", "reason": "ambiguous_or_missing_source"}, {"block": "B1", "column": "conversation_created_at", "reason": "ambiguous_or_missing_source"}]

## S96

类别 `data`；来源 `query_db`；调用 `11b1bd8196ef4ffa8a8a742245fe01d6`；状态 `success`。

```sql
SELECT 
  CASE WHEN all_conversation_tags LIKE '%sla:breached%' THEN 'breached'
       WHEN all_conversation_tags LIKE '%sla:met%' THEN 'met'
       WHEN all_conversation_tags LIKE '%sla:warning%' THEN 'warning' END AS sla_status,
  COUNT(*) AS total,
  ROUND(AVG(time_to_first_response_minutes),2) AS avg_resp_delay,
  ROUND(AVG(time_to_last_close_minutes),2) AS avg_duration
FROM intercom__conversation_enhanced ce
JOIN intercom__conversation_metrics cm ON ce.conversation_id = cm.conversation_id
GROUP BY 1
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-097/attempt-01/sql/S96.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-097/attempt-01/sql/S96.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-097/attempt-01/results/S96.rows.jsonl)；完整：True；SHA256：`fd127baecfcb4a0c369085462dcd53f68af8ea4fd52f7a282c217b7c4df826da`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "ce", "kind": "base", "block": null, "base_tables": ["intercom__conversation_enhanced"]}, {"alias": "cm", "kind": "base", "block": null, "base_tables": ["intercom__conversation_metrics"]}] | [{"type": "INNER", "right": "intercom__conversation_metrics AS cm", "on": "ce.conversation_id = cm.conversation_id", "using": []}] | ["CASE WHEN all_conversation_tags LIKE '%sla:breached%' THEN 'breached' WHEN all_conversation_tags LIKE '%sla:met%' THEN 'met' WHEN all_conversation_tags LIKE '%sla:warning%' THEN 'warning' END"] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |
| B1 | AVG(time_to_first_response_minutes) | [{"table": "intercom__conversation_metrics", "column": "time_to_first_response_minutes"}] | [] | False |
| B1 | AVG(time_to_last_close_minutes) | [{"table": "intercom__conversation_metrics", "column": "time_to_last_close_minutes"}] | [] | False |


## S97

类别 `data`；来源 `query_db`；调用 `9b51f0bb126342f3836812049d26a95d`；状态 `success`。

```sql
SELECT 
  strftime('%Y-%m', ce.conversation_created_at) AS month,
  COUNT(*) AS total_convs,
  ROUND(AVG(cm.time_to_first_response_minutes),2) AS avg_resp_delay,
  ROUND(AVG(cm.time_to_last_close_minutes),2) AS avg_duration,
  ROUND(100.0 * SUM(CASE WHEN ce.all_conversation_tags LIKE '%first_response:bot%' THEN 1 ELSE 0 END) / COUNT(*), 2) AS bot_pct
FROM intercom__conversation_enhanced ce
JOIN intercom__conversation_metrics cm ON ce.conversation_id = cm.conversation_id
WHERE cm.time_to_last_close_minutes BETWEEN 91 AND 1030
  AND cm.time_to_first_response_minutes BETWEEN 11 AND 42
GROUP BY strftime('%Y-%m', ce.conversation_created_at)
ORDER BY month
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-097/attempt-01/sql/S97.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-097/attempt-01/sql/S97.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-097/attempt-01/results/S97.rows.jsonl)；完整：True；SHA256：`a93a9d3e82747845533d3703944ca612ba5c7cdbdf230759548c0f17689d29c5`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "ce", "kind": "base", "block": null, "base_tables": ["intercom__conversation_enhanced"]}, {"alias": "cm", "kind": "base", "block": null, "base_tables": ["intercom__conversation_metrics"]}] | [{"type": "INNER", "right": "intercom__conversation_metrics AS cm", "on": "ce.conversation_id = cm.conversation_id", "using": []}] | ["STRFTIME('%Y-%m', ce.conversation_created_at)"] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |
| B1 | AVG(cm.time_to_first_response_minutes) | [{"table": "intercom__conversation_metrics", "column": "time_to_first_response_minutes"}] | [] | False |
| B1 | AVG(cm.time_to_last_close_minutes) | [{"table": "intercom__conversation_metrics", "column": "time_to_last_close_minutes"}] | [] | False |
| B1 | COUNT(*) | [] | [] | True |
| B1 | SUM(CASE WHEN ce.all_conversation_tags LIKE '%first_response:bot%' THEN 1 ELSE 0 END) | [] | [{"table": "intercom__conversation_enhanced", "column": "all_conversation_tags"}] | False |


## S98

类别 `data`；来源 `query_db`；调用 `1a15de48ff3d42a9aec3a2e5ce0428aa`；状态 `success`。

```sql
SELECT 
  CASE 
    WHEN all_conversation_tags LIKE '%topic:onboarding%' THEN 'onboarding'
    WHEN all_conversation_tags LIKE '%topic:billing%' THEN 'billing'
    WHEN all_conversation_tags LIKE '%topic:usage_insight%' THEN 'usage_insight'
    WHEN all_conversation_tags LIKE '%topic:security%' THEN 'security'
    WHEN all_conversation_tags LIKE '%topic:renewal%' THEN 'renewal'
    WHEN all_conversation_tags LIKE '%topic:adoption%' THEN 'adoption'
    WHEN all_conversation_tags LIKE '%topic:escalation%' THEN 'escalation'
    WHEN all_conversation_tags LIKE '%topic:feature_request%' THEN 'feature_request'
    WHEN all_conversation_tags LIKE '%topic:integration%' THEN 'integration'
    WHEN all_conversation_tags LIKE '%topic:success_plan%' THEN 'success_plan'
    ELSE 'other' END AS topic,
  COUNT(*) AS total,
  ROUND(100.0 * SUM(CASE WHEN all_conversation_tags LIKE '%first_response:bot%' THEN 1 ELSE 0 END) / COUNT(*), 2) AS bot_pct
FROM intercom__conversation_enhanced
GROUP BY 1
ORDER BY total DESC
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-097/attempt-01/sql/S98.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-097/attempt-01/sql/S98.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-097/attempt-01/results/S98.rows.jsonl)；完整：True；SHA256：`ac83ace9ba71e24025447301614b233383fccdd706b254bcb5f3282e7a7e2d44`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "intercom__conversation_enhanced", "kind": "base", "block": null, "base_tables": ["intercom__conversation_enhanced"]}] | [] | ["CASE WHEN all_conversation_tags LIKE '%topic:onboarding%' THEN 'onboarding' WHEN all_conversation_tags LIKE '%topic:billing%' THEN 'billing' WHEN all_conversation_tags LIKE '%topic:usage_insight%' THEN 'usage_insight' WHEN all_conversation_tags LIKE '%topic:security%' THEN 'security' WHEN all_conversation_tags LIKE '%topic:renewal%' THEN 'renewal' WHEN all_conversation_tags LIKE '%topic:adoption%' THEN 'adoption' WHEN all_conversation_tags LIKE '%topic:escalation%' THEN 'escalation' WHEN all_conversation_tags LIKE '%topic:feature_request%' THEN 'feature_request' WHEN all_conversation_tags LIKE '%topic:integration%' THEN 'integration' WHEN all_conversation_tags LIKE '%topic:success_plan%' THEN 'success_plan' ELSE 'other' END"] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |
| B1 | COUNT(*) | [] | [] | True |
| B1 | SUM(CASE WHEN all_conversation_tags LIKE '%first_response:bot%' THEN 1 ELSE 0 END) | [] | [{"table": "intercom__conversation_enhanced", "column": "all_conversation_tags"}] | False |


## S99

类别 `data`；来源 `query_db`；调用 `ebce6a18f20346e9b00f25a7cd0c4069`；状态 `success`。

```sql
SELECT 
  CASE 
    WHEN c.all_conversation_tags LIKE '%topic:onboarding%' THEN 'onboarding'
    WHEN c.all_conversation_tags LIKE '%topic:billing%' THEN 'billing'
    WHEN c.all_conversation_tags LIKE '%topic:usage_insight%' THEN 'usage_insight'
    WHEN c.all_conversation_tags LIKE '%topic:security%' THEN 'security'
    WHEN c.all_conversation_tags LIKE '%topic:renewal%' THEN 'renewal'
    WHEN c.all_conversation_tags LIKE '%topic:adoption%' THEN 'adoption'
    WHEN c.all_conversation_tags LIKE '%topic:escalation%' THEN 'escalation'
    WHEN c.all_conversation_tags LIKE '%topic:feature_request%' THEN 'feature_request'
    WHEN c.all_conversation_tags LIKE '%topic:integration%' THEN 'integration'
    WHEN c.all_conversation_tags LIKE '%topic:success_plan%' THEN 'success_plan'
    ELSE 'other' END AS topic,
  COUNT(*) AS total
FROM intercom__conversation_enhanced c
JOIN intercom__company_enhanced co ON c.all_contact_company_names = co.company_name
WHERE co.all_company_tags LIKE '%arr_bucket:arr:200k_plus%'
GROUP BY 1
ORDER BY total DESC
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-097/attempt-01/sql/S99.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-097/attempt-01/sql/S99.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-097/attempt-01/results/S99.rows.jsonl)；完整：True；SHA256：`54e2dec56a08471ff379a17d7d8aac83aaa918749f16671d4e393fd2b927ce1e`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "c", "kind": "base", "block": null, "base_tables": ["intercom__conversation_enhanced"]}, {"alias": "co", "kind": "base", "block": null, "base_tables": ["intercom__company_enhanced"]}] | [{"type": "INNER", "right": "intercom__company_enhanced AS co", "on": "c.all_contact_company_names = co.company_name", "using": []}] | ["CASE WHEN c.all_conversation_tags LIKE '%topic:onboarding%' THEN 'onboarding' WHEN c.all_conversation_tags LIKE '%topic:billing%' THEN 'billing' WHEN c.all_conversation_tags LIKE '%topic:usage_insight%' THEN 'usage_insight' WHEN c.all_conversation_tags LIKE '%topic:security%' THEN 'security' WHEN c.all_conversation_tags LIKE '%topic:renewal%' THEN 'renewal' WHEN c.all_conversation_tags LIKE '%topic:adoption%' THEN 'adoption' WHEN c.all_conversation_tags LIKE '%topic:escalation%' THEN 'escalation' WHEN c.all_conversation_tags LIKE '%topic:feature_request%' THEN 'feature_request' WHEN c.all_conversation_tags LIKE '%topic:integration%' THEN 'integration' WHEN c.all_conversation_tags LIKE '%topic:success_plan%' THEN 'success_plan' ELSE 'other' END"] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |


## S100

类别 `data`；来源 `query_db`；调用 `91663e88536340d5b1a61bdd20ee5132`；状态 `success`。

```sql
-- Topic mix for churn_watch companies with high ARR (200k+)
SELECT 
  CASE 
    WHEN c.all_conversation_tags LIKE '%topic:onboarding%' THEN 'onboarding'
    WHEN c.all_conversation_tags LIKE '%topic:billing%' THEN 'billing'
    WHEN c.all_conversation_tags LIKE '%topic:usage_insight%' THEN 'usage_insight'
    WHEN c.all_conversation_tags LIKE '%topic:security%' THEN 'security'
    WHEN c.all_conversation_tags LIKE '%topic:renewal%' THEN 'renewal'
    WHEN c.all_conversation_tags LIKE '%topic:adoption%' THEN 'adoption'
    WHEN c.all_conversation_tags LIKE '%topic:escalation%' THEN 'escalation'
    WHEN c.all_conversation_tags LIKE '%topic:feature_request%' THEN 'feature_request'
    WHEN c.all_conversation_tags LIKE '%topic:integration%' THEN 'integration'
    WHEN c.all_conversation_tags LIKE '%topic:success_plan%' THEN 'success_plan'
    ELSE 'other' END AS topic,
  COUNT(*) AS total
FROM intercom__conversation_enhanced c
JOIN intercom__company_enhanced co ON c.all_contact_company_names = co.company_name
WHERE co.all_company_tags LIKE '%segment:churn_watch%' 
  AND co.all_company_tags LIKE '%arr_bucket:arr:200k_plus%'
GROUP BY 1
ORDER BY total DESC
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-097/attempt-01/sql/S100.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-097/attempt-01/sql/S100.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-097/attempt-01/results/S100.rows.jsonl)；完整：True；SHA256：`54e2dec56a08471ff379a17d7d8aac83aaa918749f16671d4e393fd2b927ce1e`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "c", "kind": "base", "block": null, "base_tables": ["intercom__conversation_enhanced"]}, {"alias": "co", "kind": "base", "block": null, "base_tables": ["intercom__company_enhanced"]}] | [{"type": "INNER", "right": "intercom__company_enhanced AS co", "on": "c.all_contact_company_names = co.company_name", "using": []}] | ["CASE WHEN c.all_conversation_tags LIKE '%topic:onboarding%' THEN 'onboarding' WHEN c.all_conversation_tags LIKE '%topic:billing%' THEN 'billing' WHEN c.all_conversation_tags LIKE '%topic:usage_insight%' THEN 'usage_insight' WHEN c.all_conversation_tags LIKE '%topic:security%' THEN 'security' WHEN c.all_conversation_tags LIKE '%topic:renewal%' THEN 'renewal' WHEN c.all_conversation_tags LIKE '%topic:adoption%' THEN 'adoption' WHEN c.all_conversation_tags LIKE '%topic:escalation%' THEN 'escalation' WHEN c.all_conversation_tags LIKE '%topic:feature_request%' THEN 'feature_request' WHEN c.all_conversation_tags LIKE '%topic:integration%' THEN 'integration' WHEN c.all_conversation_tags LIKE '%topic:success_plan%' THEN 'success_plan' ELSE 'other' END"] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |


## S101

类别 `data`；来源 `query_db`；调用 `2adcf40b450544ec998c629f3a1e8749`；状态 `success`。

```sql
-- Segment composition of ARR 200k+ customers
SELECT 
  CASE WHEN all_company_tags LIKE '%segment:new_contract%' THEN 'new_contract'
       WHEN all_company_tags LIKE '%segment:renewal%' THEN 'renewal'
       WHEN all_company_tags LIKE '%segment:churn_watch%' THEN 'churn_watch'
       WHEN all_company_tags LIKE '%segment:expansion%' THEN 'expansion'
       ELSE 'unknown' END AS segment,
  COUNT(*) AS total
FROM intercom__company_enhanced
WHERE all_company_tags LIKE '%arr_bucket:arr:200k_plus%'
GROUP BY 1
ORDER BY total DESC
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-097/attempt-01/sql/S101.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-097/attempt-01/sql/S101.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-097/attempt-01/results/S101.rows.jsonl)；完整：True；SHA256：`279429aa1f2a758facb57316873b68d6208459bf6a1c484b9823187d830f2aed`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "intercom__company_enhanced", "kind": "base", "block": null, "base_tables": ["intercom__company_enhanced"]}] | [] | ["CASE WHEN all_company_tags LIKE '%segment:new_contract%' THEN 'new_contract' WHEN all_company_tags LIKE '%segment:renewal%' THEN 'renewal' WHEN all_company_tags LIKE '%segment:churn_watch%' THEN 'churn_watch' WHEN all_company_tags LIKE '%segment:expansion%' THEN 'expansion' ELSE 'unknown' END"] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |


## S102

类别 `data`；来源 `query_db`；调用 `b83b3e293fd843f388b115ce3aa62f80`；状态 `success`。

```sql
-- Segment composition of seats 420+ customers
SELECT 
  CASE WHEN all_company_tags LIKE '%segment:new_contract%' THEN 'new_contract'
       WHEN all_company_tags LIKE '%segment:renewal%' THEN 'renewal'
       WHEN all_company_tags LIKE '%segment:churn_watch%' THEN 'churn_watch'
       WHEN all_company_tags LIKE '%segment:expansion%' THEN 'expansion'
       ELSE 'unknown' END AS segment,
  COUNT(*) AS total
FROM intercom__company_enhanced
WHERE all_company_tags LIKE '%seat_bucket:seats:420_plus%'
GROUP BY 1
ORDER BY total DESC
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-097/attempt-01/sql/S102.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-097/attempt-01/sql/S102.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-097/attempt-01/results/S102.rows.jsonl)；完整：True；SHA256：`cea90402d9e20c93205519a642173be2c8fad46771e5627d4bac1e5b30f1095a`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "intercom__company_enhanced", "kind": "base", "block": null, "base_tables": ["intercom__company_enhanced"]}] | [] | ["CASE WHEN all_company_tags LIKE '%segment:new_contract%' THEN 'new_contract' WHEN all_company_tags LIKE '%segment:renewal%' THEN 'renewal' WHEN all_company_tags LIKE '%segment:churn_watch%' THEN 'churn_watch' WHEN all_company_tags LIKE '%segment:expansion%' THEN 'expansion' ELSE 'unknown' END"] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |


## S103

类别 `data`；来源 `query_db`；调用 `535adf96d32f402daa9e1d80e2882f43`；状态 `success`。

```sql
-- Cross-tab of segment vs ARR
WITH company_dim AS (
  SELECT DISTINCT company_name,
    CASE WHEN all_company_tags LIKE '%segment:new_contract%' THEN 'new_contract'
         WHEN all_company_tags LIKE '%segment:renewal%' THEN 'renewal'
         WHEN all_company_tags LIKE '%segment:churn_watch%' THEN 'churn_watch'
         WHEN all_company_tags LIKE '%segment:expansion%' THEN 'expansion'
         ELSE 'unknown' END AS segment,
    CASE WHEN all_company_tags LIKE '%arr_bucket:arr:200k_plus%' THEN '200k_plus'
         WHEN all_company_tags LIKE '%arr_bucket:arr:110k_200k%' THEN '110k_200k'
         WHEN all_company_tags LIKE '%arr_bucket:arr:65k_110k%' THEN '65k_110k'
         WHEN all_company_tags LIKE '%arr_bucket:arr:30k_65k%' THEN '30k_65k'
         WHEN all_company_tags LIKE '%arr_bucket:arr:<30k%' THEN '<30k'
         ELSE 'unknown' END AS arr_bucket
  FROM intercom__company_enhanced
)
SELECT segment, arr_bucket, COUNT(*) AS cnt
FROM company_dim
GROUP BY segment, arr_bucket
ORDER BY segment, arr_bucket
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-097/attempt-01/sql/S103.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-097/attempt-01/sql/S103.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-097/attempt-01/results/S103.rows.jsonl)；完整：True；SHA256：`f66c0834260ac63b0be19e0144e2cffdf71e6d268f2b34344b854b91bec7786c`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "intercom__company_enhanced", "kind": "base", "block": null, "base_tables": ["intercom__company_enhanced"]}] | [] | [] |
| B2 | [{"alias": "company_dim", "kind": "derived", "block": "B1", "base_tables": ["intercom__company_enhanced"]}] | [] | ["segment", "arr_bucket"] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B2 | COUNT(*) | [] | [] | True |


## S104

类别 `data`；来源 `query_db`；调用 `34cbe31bec8445f09e9e1e526fa65656`；状态 `success`。

```sql
-- Topic distribution by segment (churn_watch vs renewal vs new_contract), with bot ratio
WITH company_dim AS (
  SELECT DISTINCT company_name,
    CASE WHEN all_company_tags LIKE '%segment:new_contract%' THEN 'new_contract'
         WHEN all_company_tags LIKE '%segment:renewal%' THEN 'renewal'
         WHEN all_company_tags LIKE '%segment:churn_watch%' THEN 'churn_watch'
         WHEN all_company_tags LIKE '%segment:expansion%' THEN 'expansion'
         ELSE 'unknown' END AS segment
  FROM intercom__company_enhanced
)
SELECT 
  co.segment,
  CASE 
    WHEN c.all_conversation_tags LIKE '%topic:onboarding%' THEN 'onboarding'
    WHEN c.all_conversation_tags LIKE '%topic:escalation%' THEN 'escalation'
    WHEN c.all_conversation_tags LIKE '%topic:adoption%' THEN 'adoption'
    WHEN c.all_conversation_tags LIKE '%topic:integration%' THEN 'integration'
    WHEN c.all_conversation_tags LIKE '%topic:feature_request%' THEN 'feature_request'
    WHEN c.all_conversation_tags LIKE '%topic:usage_insight%' THEN 'usage_insight'
    WHEN c.all_conversation_tags LIKE '%topic:renewal%' THEN 'renewal'
    WHEN c.all_conversation_tags LIKE '%topic:success_plan%' THEN 'success_plan'
    WHEN c.all_conversation_tags LIKE '%topic:security%' THEN 'security'
    WHEN c.all_conversation_tags LIKE '%topic:billing%' THEN 'billing'
    ELSE 'other' END AS topic,
  COUNT(*) AS total,
  ROUND(100.0 * SUM(CASE WHEN c.all_conversation_tags LIKE '%first_response:bot%' THEN 1 ELSE 0 END) / COUNT(*), 1) AS bot_pct
FROM intercom__conversation_enhanced c
JOIN company_dim co ON c.all_contact_company_names = co.company_name
GROUP BY co.segment, 2
ORDER BY co.segment, total DESC
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-097/attempt-01/sql/S104.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-097/attempt-01/sql/S104.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-097/attempt-01/results/S104.rows.jsonl)；完整：True；SHA256：`b1b832660f56f60aafaeb260fe6dc5c5b5b5127bc1a67c33cebe026f6eb95d03`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "intercom__company_enhanced", "kind": "base", "block": null, "base_tables": ["intercom__company_enhanced"]}] | [] | [] |
| B2 | [{"alias": "c", "kind": "base", "block": null, "base_tables": ["intercom__conversation_enhanced"]}, {"alias": "co", "kind": "derived", "block": "B1", "base_tables": ["intercom__company_enhanced"]}] | [{"type": "INNER", "right": "company_dim AS co", "on": "c.all_contact_company_names = co.company_name", "using": []}] | ["co.segment", "CASE WHEN c.all_conversation_tags LIKE '%topic:onboarding%' THEN 'onboarding' WHEN c.all_conversation_tags LIKE '%topic:escalation%' THEN 'escalation' WHEN c.all_conversation_tags LIKE '%topic:adoption%' THEN 'adoption' WHEN c.all_conversation_tags LIKE '%topic:integration%' THEN 'integration' WHEN c.all_conversation_tags LIKE '%topic:feature_request%' THEN 'feature_request' WHEN c.all_conversation_tags LIKE '%topic:usage_insight%' THEN 'usage_insight' WHEN c.all_conversation_tags LIKE '%topic:renewal%' THEN 'renewal' WHEN c.all_conversation_tags LIKE '%topic:success_plan%' THEN 'success_plan' WHEN c.all_conversation_tags LIKE '%topic:security%' THEN 'security' WHEN c.all_conversation_tags LIKE '%topic:billing%' THEN 'billing' ELSE 'other' END"] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B2 | COUNT(*) | [] | [] | True |
| B2 | COUNT(*) | [] | [] | True |
| B2 | SUM(CASE WHEN c.all_conversation_tags LIKE '%first_response:bot%' THEN 1 ELSE 0 END) | [] | [{"table": "intercom__conversation_enhanced", "column": "all_conversation_tags"}] | False |


## S105

类别 `data`；来源 `query_db`；调用 `3805fab3d3ae44caa89218e310a28a4a`；状态 `success`。

```sql
-- Conversation-to-feature-usage conversion by topic (company-level)
WITH conv_end AS (
  SELECT DISTINCT all_contact_company_names AS company_name, last_close_at
  FROM intercom__conversation_enhanced
  WHERE last_close_at IS NOT NULL
),
contact_act AS (
  SELECT all_contact_company_names AS company_name, last_activity_ts
  FROM intercom__contact_enhanced
  WHERE last_activity_ts IS NOT NULL
),
converted_companies AS (
  SELECT DISTINCT c.company_name
  FROM conv_end c JOIN contact_act a ON c.company_name = a.company_name
  WHERE a.last_activity_ts >= c.last_close_at 
    AND a.last_activity_ts <= datetime(c.last_close_at, '+72 hours')
)
SELECT 
  CASE 
    WHEN c.all_conversation_tags LIKE '%topic:onboarding%' THEN 'onboarding'
    WHEN c.all_conversation_tags LIKE '%topic:adoption%' THEN 'adoption'
    WHEN c.all_conversation_tags LIKE '%topic:usage_insight%' THEN 'usage_insight'
    WHEN c.all_conversation_tags LIKE '%topic:integration%' THEN 'integration'
    WHEN c.all_conversation_tags LIKE '%topic:feature_request%' THEN 'feature_request'
    WHEN c.all_conversation_tags LIKE '%topic:renewal%' THEN 'renewal'
    WHEN c.all_conversation_tags LIKE '%topic:success_plan%' THEN 'success_plan'
    WHEN c.all_conversation_tags LIKE '%topic:security%' THEN 'security'
    WHEN c.all_conversation_tags LIKE '%topic:escalation%' THEN 'escalation'
    WHEN c.all_conversation_tags LIKE '%topic:billing%' THEN 'billing'
    ELSE 'other' END AS topic,
  COUNT(DISTINCT c.all_contact_company_names) AS companies_with_topic,
  COUNT(DISTINCT CASE WHEN cv.company_name IS NOT NULL THEN c.all_contact_company_names END) AS converted_companies
FROM intercom__conversation_enhanced c
LEFT JOIN converted_companies cv ON c.all_contact_company_names = cv.company_name
GROUP BY 1
ORDER BY 2 DESC
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-097/attempt-01/sql/S105.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-097/attempt-01/sql/S105.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-097/attempt-01/results/S105.rows.jsonl)；完整：True；SHA256：`9acdd7b475c750048a1d459612ea6242c5948348bfc88a010fd8443de67772a0`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "intercom__conversation_enhanced", "kind": "base", "block": null, "base_tables": ["intercom__conversation_enhanced"]}] | [] | [] |
| B2 | [{"alias": "intercom__contact_enhanced", "kind": "base", "block": null, "base_tables": ["intercom__contact_enhanced"]}] | [] | [] |
| B3 | [{"alias": "c", "kind": "derived", "block": "B1", "base_tables": ["intercom__conversation_enhanced"]}, {"alias": "a", "kind": "derived", "block": "B2", "base_tables": ["intercom__contact_enhanced"]}] | [{"type": "INNER", "right": "contact_act AS a", "on": "c.company_name = a.company_name", "using": []}] | [] |
| B4 | [{"alias": "c", "kind": "base", "block": null, "base_tables": ["intercom__conversation_enhanced"]}, {"alias": "cv", "kind": "derived", "block": "B3", "base_tables": ["intercom__contact_enhanced", "intercom__conversation_enhanced"]}] | [{"type": "LEFT", "right": "converted_companies AS cv", "on": "c.all_contact_company_names = cv.company_name", "using": []}] | ["CASE WHEN c.all_conversation_tags LIKE '%topic:onboarding%' THEN 'onboarding' WHEN c.all_conversation_tags LIKE '%topic:adoption%' THEN 'adoption' WHEN c.all_conversation_tags LIKE '%topic:usage_insight%' THEN 'usage_insight' WHEN c.all_conversation_tags LIKE '%topic:integration%' THEN 'integration' WHEN c.all_conversation_tags LIKE '%topic:feature_request%' THEN 'feature_request' WHEN c.all_conversation_tags LIKE '%topic:renewal%' THEN 'renewal' WHEN c.all_conversation_tags LIKE '%topic:success_plan%' THEN 'success_plan' WHEN c.all_conversation_tags LIKE '%topic:security%' THEN 'security' WHEN c.all_conversation_tags LIKE '%topic:escalation%' THEN 'escalation' WHEN c.all_conversation_tags LIKE '%topic:billing%' THEN 'billing' ELSE 'other' END"] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B4 | COUNT(DISTINCT c.all_contact_company_names) | [{"table": "intercom__conversation_enhanced", "column": "all_contact_company_names"}] | [] | False |
| B4 | COUNT(DISTINCT CASE WHEN NOT cv.company_name IS NULL THEN c.all_contact_company_names END) | [{"table": "intercom__conversation_enhanced", "column": "all_contact_company_names"}] | [{"table": "intercom__conversation_enhanced", "column": "all_contact_company_names"}] | False |


## S106

类别 `data`；来源 `query_db`；调用 `d2aa92ce05cd4d5585d1e7e71f3731eb`；状态 `success`。

```sql
-- Cross-tab: segment vs seat bucket
WITH company_dim AS (
  SELECT DISTINCT company_name,
    CASE WHEN all_company_tags LIKE '%segment:new_contract%' THEN 'new_contract'
         WHEN all_company_tags LIKE '%segment:renewal%' THEN 'renewal'
         WHEN all_company_tags LIKE '%segment:churn_watch%' THEN 'churn_watch'
         WHEN all_company_tags LIKE '%segment:expansion%' THEN 'expansion'
         ELSE 'unknown' END AS segment,
    CASE WHEN all_company_tags LIKE '%seat_bucket:seats:under_60%' THEN 'under_60'
         WHEN all_company_tags LIKE '%seat_bucket:seats:60_129%' THEN '60_129'
         WHEN all_company_tags LIKE '%seat_bucket:seats:130_259%' THEN '130_259'
         WHEN all_company_tags LIKE '%seat_bucket:seats:260_419%' THEN '260_419'
         WHEN all_company_tags LIKE '%seat_bucket:seats:420_plus%' THEN '420_plus'
         ELSE 'unknown' END AS seat_bucket
  FROM intercom__company_enhanced
)
SELECT segment, seat_bucket, COUNT(*) AS cnt
FROM company_dim
GROUP BY segment, seat_bucket
ORDER BY segment, seat_bucket
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-097/attempt-01/sql/S106.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-097/attempt-01/sql/S106.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-097/attempt-01/results/S106.rows.jsonl)；完整：True；SHA256：`c34346272c94329bea685aee8bacd156d7cf655cf54ab5b6686017d6a21b542d`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "intercom__company_enhanced", "kind": "base", "block": null, "base_tables": ["intercom__company_enhanced"]}] | [] | [] |
| B2 | [{"alias": "company_dim", "kind": "derived", "block": "B1", "base_tables": ["intercom__company_enhanced"]}] | [] | ["segment", "seat_bucket"] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B2 | COUNT(*) | [] | [] | True |


## S107

类别 `data`；来源 `query_db`；调用 `102f6eef49084a189c189fa3254e2db6`；状态 `success`。

```sql
-- For churn_watch segment, compare high vs low retention companies
WITH company_dim AS (
  SELECT DISTINCT company_name,
    CASE WHEN all_company_tags LIKE '%seat_bucket:seats:420_plus%' THEN 'large'
         WHEN all_company_tags LIKE '%seat_bucket:seats:260_419%' THEN 'medium'
         ELSE 'small' END AS size_category
  FROM intercom__company_enhanced
  WHERE all_company_tags LIKE '%segment:churn_watch%'
)
SELECT 
  cd.size_category,
  COUNT(*) AS companies,
  ROUND(AVG(cm.registration_retention_7d), 4) AS avg_weekly_retention,
  ROUND(AVG(cm.registration_retention_30d), 4) AS avg_monthly_retention,
  ROUND(AVG(cm.contacts_active_7d), 1) AS avg_active_7d,
  ROUND(AVG(cm.contacts_active_30d), 1) AS avg_active_30d,
  ROUND(AVG(cm.total_conversations), 1) AS avg_total_convs
FROM company_dim cd
JOIN intercom__company_metrics cm ON cd.company_name = cm.company_name
GROUP BY cd.size_category
ORDER BY cd.size_category
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-097/attempt-01/sql/S107.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-097/attempt-01/sql/S107.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-097/attempt-01/results/S107.rows.jsonl)；完整：True；SHA256：`601b95a0e4f9f7eded5a803f038e978922eff23a0572d2fc2a7de3da06fc4628`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "intercom__company_enhanced", "kind": "base", "block": null, "base_tables": ["intercom__company_enhanced"]}] | [] | [] |
| B2 | [{"alias": "cd", "kind": "derived", "block": "B1", "base_tables": ["intercom__company_enhanced"]}, {"alias": "cm", "kind": "base", "block": null, "base_tables": ["intercom__company_metrics"]}] | [{"type": "INNER", "right": "intercom__company_metrics AS cm", "on": "cd.company_name = cm.company_name", "using": []}] | ["cd.size_category"] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B2 | COUNT(*) | [] | [] | True |
| B2 | AVG(cm.registration_retention_7d) | [{"table": "intercom__company_metrics", "column": "registration_retention_7d"}] | [] | False |
| B2 | AVG(cm.registration_retention_30d) | [{"table": "intercom__company_metrics", "column": "registration_retention_30d"}] | [] | False |
| B2 | AVG(cm.contacts_active_7d) | [{"table": "intercom__company_metrics", "column": "contacts_active_7d"}] | [] | False |
| B2 | AVG(cm.contacts_active_30d) | [{"table": "intercom__company_metrics", "column": "contacts_active_30d"}] | [] | False |
| B2 | AVG(cm.total_conversations) | [{"table": "intercom__company_metrics", "column": "total_conversations"}] | [] | False |


## S108

类别 `data`；来源 `query_db`；调用 `8f4715f9bb63413ba356d58d74c423b1`；状态 `success`。

```sql
-- Conversation volume per company vs retention within churn_watch
WITH company_dim AS (
  SELECT DISTINCT company_name
  FROM intercom__company_enhanced
  WHERE all_company_tags LIKE '%segment:churn_watch%'
),
conv_counts AS (
  SELECT 
    ce.all_contact_company_names AS company_name,
    COUNT(*) AS total_convs
  FROM intercom__conversation_enhanced ce
  GROUP BY ce.all_contact_company_names
)
SELECT 
  CASE WHEN cc.total_convs <= 1 THEN '0-1'
       WHEN cc.total_convs <= 3 THEN '2-3'
       WHEN cc.total_convs <= 5 THEN '4-5'
       ELSE '6+' END AS conv_volume_bucket,
  COUNT(*) AS companies,
  ROUND(AVG(cm.registration_retention_7d), 4) AS avg_weekly_retention,
  ROUND(AVG(cm.registration_retention_30d), 4) AS avg_monthly_retention
FROM company_dim cd
JOIN conv_counts cc ON cd.company_name = cc.company_name
JOIN intercom__company_metrics cm ON cd.company_name = cm.company_name
GROUP BY 1
ORDER BY 1
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-097/attempt-01/sql/S108.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-097/attempt-01/sql/S108.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-097/attempt-01/results/S108.rows.jsonl)；完整：True；SHA256：`a04d79199f041ec763e7386b1079fdba3556d5ee78c124b2cea0c66a6f84ddfa`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "intercom__company_enhanced", "kind": "base", "block": null, "base_tables": ["intercom__company_enhanced"]}] | [] | [] |
| B2 | [{"alias": "ce", "kind": "base", "block": null, "base_tables": ["intercom__conversation_enhanced"]}] | [] | ["ce.all_contact_company_names"] |
| B3 | [{"alias": "cd", "kind": "derived", "block": "B1", "base_tables": ["intercom__company_enhanced"]}, {"alias": "cc", "kind": "derived", "block": "B2", "base_tables": ["intercom__conversation_enhanced"]}, {"alias": "cm", "kind": "base", "block": null, "base_tables": ["intercom__company_metrics"]}] | [{"type": "INNER", "right": "conv_counts AS cc", "on": "cd.company_name = cc.company_name", "using": []}, {"type": "INNER", "right": "intercom__company_metrics AS cm", "on": "cd.company_name = cm.company_name", "using": []}] | ["CASE WHEN cc.total_convs <= 1 THEN '0-1' WHEN cc.total_convs <= 3 THEN '2-3' WHEN cc.total_convs <= 5 THEN '4-5' ELSE '6+' END"] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B2 | COUNT(*) | [] | [] | True |
| B3 | COUNT(*) | [] | [] | True |
| B3 | AVG(cm.registration_retention_7d) | [{"table": "intercom__company_metrics", "column": "registration_retention_7d"}] | [] | False |
| B3 | AVG(cm.registration_retention_30d) | [{"table": "intercom__company_metrics", "column": "registration_retention_30d"}] | [] | False |


## S109

类别 `data`；来源 `query_db`；调用 `2373dc4e80984a7186d79a158c703326`；状态 `success`。

```sql
-- Bot ratio buckets vs retention within churn_watch
WITH company_dim AS (
  SELECT DISTINCT company_name
  FROM intercom__company_enhanced
  WHERE all_company_tags LIKE '%segment:churn_watch%'
),
conv_bot AS (
  SELECT 
    ce.all_contact_company_names AS company_name,
    COUNT(*) AS total_convs,
    SUM(CASE WHEN ce.all_conversation_tags LIKE '%first_response:bot%' THEN 1 ELSE 0 END) * 1.0 / COUNT(*) AS bot_ratio
  FROM intercom__conversation_enhanced ce
  GROUP BY ce.all_contact_company_names
)
SELECT 
  CASE WHEN cb.bot_ratio <= 0.25 THEN '0-25%'
       WHEN cb.bot_ratio <= 0.50 THEN '25-50%'
       WHEN cb.bot_ratio <= 0.75 THEN '50-75%'
       ELSE '75-100%' END AS bot_ratio_bucket,
  COUNT(*) AS companies,
  ROUND(AVG(cm.registration_retention_7d), 4) AS avg_weekly_retention,
  ROUND(AVG(cm.registration_retention_30d), 4) AS avg_monthly_retention
FROM company_dim cd
JOIN conv_bot cb ON cd.company_name = cb.company_name
JOIN intercom__company_metrics cm ON cd.company_name = cm.company_name
GROUP BY 1
ORDER BY 1
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-097/attempt-01/sql/S109.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-097/attempt-01/sql/S109.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-097/attempt-01/results/S109.rows.jsonl)；完整：True；SHA256：`0ca675fb7670b5487b95ec813eef6c05836ee970a32d7909ae32bd0fd2c98918`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "intercom__company_enhanced", "kind": "base", "block": null, "base_tables": ["intercom__company_enhanced"]}] | [] | [] |
| B2 | [{"alias": "ce", "kind": "base", "block": null, "base_tables": ["intercom__conversation_enhanced"]}] | [] | ["ce.all_contact_company_names"] |
| B3 | [{"alias": "cd", "kind": "derived", "block": "B1", "base_tables": ["intercom__company_enhanced"]}, {"alias": "cb", "kind": "derived", "block": "B2", "base_tables": ["intercom__conversation_enhanced"]}, {"alias": "cm", "kind": "base", "block": null, "base_tables": ["intercom__company_metrics"]}] | [{"type": "INNER", "right": "conv_bot AS cb", "on": "cd.company_name = cb.company_name", "using": []}, {"type": "INNER", "right": "intercom__company_metrics AS cm", "on": "cd.company_name = cm.company_name", "using": []}] | ["CASE WHEN cb.bot_ratio <= 0.25 THEN '0-25%' WHEN cb.bot_ratio <= 0.50 THEN '25-50%' WHEN cb.bot_ratio <= 0.75 THEN '50-75%' ELSE '75-100%' END"] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B2 | COUNT(*) | [] | [] | True |
| B2 | COUNT(*) | [] | [] | True |
| B2 | SUM(CASE WHEN ce.all_conversation_tags LIKE '%first_response:bot%' THEN 1 ELSE 0 END) | [] | [{"table": "intercom__conversation_enhanced", "column": "all_conversation_tags"}] | False |
| B3 | COUNT(*) | [] | [] | True |
| B3 | AVG(cm.registration_retention_7d) | [{"table": "intercom__company_metrics", "column": "registration_retention_7d"}] | [] | False |
| B3 | AVG(cm.registration_retention_30d) | [{"table": "intercom__company_metrics", "column": "registration_retention_30d"}] | [] | False |


## S110

类别 `data`；来源 `query_db`；调用 `3fc8dd7c95664756abe538d3babc879a`；状态 `success`。

```sql
-- Verify response delay interpretation: first_admin_response_at - conversation_created_at
SELECT 
  conversation_id,
  conversation_created_at,
  first_admin_response_at,
  time_to_first_response_minutes,
  ROUND((julianday(first_admin_response_at) - julianday(conversation_created_at)) * 1440, 2) AS computed_delay
FROM intercom__conversation_metrics
LIMIT 10
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-097/attempt-01/sql/S110.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-097/attempt-01/sql/S110.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-097/attempt-01/results/S110.rows.jsonl)；完整：True；SHA256：`eb213fc28483a15dc73b67a49f865c699d0884811c5b89bda632db7c36dc23f2`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "intercom__conversation_metrics", "kind": "base", "block": null, "base_tables": ["intercom__conversation_metrics"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |


## S111

类别 `data`；来源 `query_db`；调用 `0b57aab788744bedafb53124bad10f68`；状态 `success`。

```sql
-- Summary of dataset
SELECT 
  (SELECT COUNT(*) FROM intercom__company_enhanced) AS companies,
  (SELECT COUNT(DISTINCT company_name) FROM intercom__company_enhanced) AS distinct_companies,
  (SELECT COUNT(*) FROM intercom__contact_enhanced) AS contacts,
  (SELECT COUNT(DISTINCT all_contact_company_names) FROM intercom__contact_enhanced) AS contact_companies,
  (SELECT COUNT(*) FROM intercom__conversation_metrics) AS conversations,
  (SELECT COUNT(DISTINCT all_contact_company_names) FROM intercom__conversation_enhanced) AS conv_companies
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-097/attempt-01/sql/S111.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-097/attempt-01/sql/S111.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-097/attempt-01/results/S111.rows.jsonl)；完整：True；SHA256：`96cfe1afb54eeb72b11414e604060e4d284384d5f66a1b08c7170c56bae1d8e6`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "intercom__company_enhanced", "kind": "base", "block": null, "base_tables": ["intercom__company_enhanced"]}] | [] | [] |
| B2 | [{"alias": "intercom__company_enhanced", "kind": "base", "block": null, "base_tables": ["intercom__company_enhanced"]}] | [] | [] |
| B3 | [{"alias": "intercom__contact_enhanced", "kind": "base", "block": null, "base_tables": ["intercom__contact_enhanced"]}] | [] | [] |
| B4 | [{"alias": "intercom__contact_enhanced", "kind": "base", "block": null, "base_tables": ["intercom__contact_enhanced"]}] | [] | [] |
| B5 | [{"alias": "intercom__conversation_metrics", "kind": "base", "block": null, "base_tables": ["intercom__conversation_metrics"]}] | [] | [] |
| B6 | [{"alias": "intercom__conversation_enhanced", "kind": "base", "block": null, "base_tables": ["intercom__conversation_enhanced"]}] | [] | [] |
| B7 | [] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |
| B2 | COUNT(DISTINCT company_name) | [{"table": "intercom__company_enhanced", "column": "company_name"}] | [] | False |
| B3 | COUNT(*) | [] | [] | True |
| B4 | COUNT(DISTINCT all_contact_company_names) | [{"table": "intercom__contact_enhanced", "column": "all_contact_company_names"}] | [] | False |
| B5 | COUNT(*) | [] | [] | True |
| B6 | COUNT(DISTINCT all_contact_company_names) | [{"table": "intercom__conversation_enhanced", "column": "all_contact_company_names"}] | [] | False |


未解析列血缘：[{"block": "B7", "column": "company_name", "reason": "ambiguous_or_missing_source"}, {"block": "B7", "column": "all_contact_company_names", "reason": "ambiguous_or_missing_source"}, {"block": "B7", "column": "all_contact_company_names", "reason": "ambiguous_or_missing_source"}]

## S112

类别 `data`；来源 `query_db`；调用 `b4ea84193e324ff894285aaf12c22aa0`；状态 `success`。

```sql
-- Final summary stats
SELECT 
  ROUND(AVG(registration_retention_7d), 4) AS overall_weekly_retention,
  ROUND(AVG(registration_retention_30d), 4) AS overall_monthly_retention,
  ROUND(AVG(contacts_active_7d), 1) AS avg_active_7d,
  ROUND(AVG(contacts_active_30d), 1) AS avg_active_30d,
  ROUND(AVG(total_conversations), 1) AS avg_convs_per_company
FROM intercom__company_metrics
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-097/attempt-01/sql/S112.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-097/attempt-01/sql/S112.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-097/attempt-01/results/S112.rows.jsonl)；完整：True；SHA256：`91dc12881d7d5bc9aa7fd47a60fad71ce62a0c59a15d9d027164989319d5650e`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "intercom__company_metrics", "kind": "base", "block": null, "base_tables": ["intercom__company_metrics"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | AVG(registration_retention_7d) | [{"table": "intercom__company_metrics", "column": "registration_retention_7d"}] | [] | False |
| B1 | AVG(registration_retention_30d) | [{"table": "intercom__company_metrics", "column": "registration_retention_30d"}] | [] | False |
| B1 | AVG(contacts_active_7d) | [{"table": "intercom__company_metrics", "column": "contacts_active_7d"}] | [] | False |
| B1 | AVG(contacts_active_30d) | [{"table": "intercom__company_metrics", "column": "contacts_active_30d"}] | [] | False |
| B1 | AVG(total_conversations) | [{"table": "intercom__company_metrics", "column": "total_conversations"}] | [] | False |


## S113

类别 `data`；来源 `query_db`；调用 `2fb5367622504d96a0f03b8672e8aa6c`；状态 `success`。

```sql
-- Monthly volume by segment
WITH company_dim AS (
  SELECT DISTINCT company_name,
    CASE WHEN all_company_tags LIKE '%segment:new_contract%' THEN 'new_contract'
         WHEN all_company_tags LIKE '%segment:renewal%' THEN 'renewal'
         WHEN all_company_tags LIKE '%segment:churn_watch%' THEN 'churn_watch'
         WHEN all_company_tags LIKE '%segment:expansion%' THEN 'expansion'
         ELSE 'unknown' END AS segment
  FROM intercom__company_enhanced
)
SELECT 
  co.segment,
  strftime('%Y-%m', ce.conversation_created_at) AS month,
  COUNT(*) AS total_convs
FROM intercom__conversation_enhanced ce
JOIN company_dim co ON ce.all_contact_company_names = co.company_name
GROUP BY co.segment, month
ORDER BY co.segment, month
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-097/attempt-01/sql/S113.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-097/attempt-01/sql/S113.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-097/attempt-01/results/S113.rows.jsonl)；完整：True；SHA256：`e97cef8ea3bb67d056d2e130cb00091499fd4a6d5462fca1991c62eef352935b`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "intercom__company_enhanced", "kind": "base", "block": null, "base_tables": ["intercom__company_enhanced"]}] | [] | [] |
| B2 | [{"alias": "ce", "kind": "base", "block": null, "base_tables": ["intercom__conversation_enhanced"]}, {"alias": "co", "kind": "derived", "block": "B1", "base_tables": ["intercom__company_enhanced"]}] | [{"type": "INNER", "right": "company_dim AS co", "on": "ce.all_contact_company_names = co.company_name", "using": []}] | ["co.segment", "STRFTIME('%Y-%m', ce.conversation_created_at)"] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B2 | COUNT(*) | [] | [] | True |

