# dacomp-033

For customers with completed high-amount transaction behavior (cumulative over 5000), help…

运行：已提交（截断）。官方未评分。全部 SQL 尝试/成功 122/117；数据 SQL 120/115；Python 1 次。

完整原题：

For customers with completed high-amount transaction behavior (cumulative over 5000), help me gain insights into these customers’ characteristics from aspects such as customer tags, the membership system, credit ratings, etc.

| 表 | 行数 | 列数 |
| --- | --- | --- |
| campaign_participation_table | 527 | 11 |
| channel_source_table | 471 | 11 |
| complaints_table | 630 | 11 |
| contracts_table | 527 | 11 |
| customer_account_table | 527 | 10 |
| customer_contact_table | 527 | 8 |
| customer_credit_rating_table | 527 | 11 |
| customer_device_table | 510 | 12 |
| customer_feedback_table | 527 | 10 |
| customer_segments_table | 415 | 10 |
| customer_tag_table | 619 | 11 |
| financials_table | 527 | 12 |
| membership_table | 447 | 11 |
| permissions_table | 527 | 11 |
| product_service_order_table | 435 | 12 |
| sales_follow_up_table | 448 | 10 |
| service_ticket_table | 428 | 10 |
| service_usage_table | 527 | 12 |
| transaction_history_table | 483 | 11 |


实际路线（分析者依据 SQL/源码概括，不代表 Agent 自述）：SQL 筛选累计完成交易超 5000 的客户 → 关联标签、会员、信用、合同和服务信息 → 对比高价值群体与总体分布 → 达到查询上限后用 Python 绘图并提交。

数据库大小：2,449,408 字节。

## 数据 SQL

| SQL | 状态 | 基础表 | Join 输入/类型 | GROUP BY | 聚合表达式 | 结果行数 | 数据库 ms |
| --- | --- | --- | --- | --- | --- | --- | --- |
| [S3/Q1](#s3) | success | ["transaction_history_table"] | 0 / {} | [] | [] | 5 | 0.351 |
| [S4/Q2](#s4) | success | ["transaction_history_table"] | 0 / {} | [] | [] | 3 | 0.448 |
| [S5/Q3](#s5) | success | ["transaction_history_table"] | 0 / {} | [] | [] | 4 | 0.67 |
| [S6/Q4](#s6) | success | ["transaction_history_table"] | 0 / {} | [] | ["COUNT(*)", "COUNT(DISTINCT \"Customer ID\")"] | 1 | 0.567 |
| [S7/Q5](#s7) | success | ["transaction_history_table"] | 0 / {} | ["\"Customer ID\""] | ["COUNT(*)", "SUM(\"Transaction Amount\")", "SUM(CASE WHEN \"Transaction Payment Status\" = 'Paid' THEN \"Transaction Amount\" ELSE 0 END)", "SUM(CASE WHEN \"Transaction Payment Status\" = 'Paid' THEN \"Transaction Amount\" ELSE 0 END)"] | 71 | 0.873 |
| [S8/Q6](#s8) | success | ["membership_table"] | 0 / {} | [] | ["COUNT(*)", "COUNT(DISTINCT \"Customer ID\")"] | 1 | 0.585 |
| [S9/Q7](#s9) | success | ["customer_tag_table"] | 0 / {} | [] | ["COUNT(*)", "COUNT(DISTINCT \"Customer ID\")"] | 1 | 0.689 |
| [S10/Q8](#s10) | success | ["customer_credit_rating_table"] | 0 / {} | [] | ["COUNT(*)", "COUNT(DISTINCT \"Account ID\")"] | 1 | 0.623 |
| [S11/Q9](#s11) | success | ["membership_table"] | 0 / {} | ["\"Membership Level\""] | ["COUNT(*)"] | 5 | 0.487 |
| [S12/Q10](#s12) | success | ["customer_tag_table"] | 0 / {} | ["\"Tag Name\""] | ["COUNT(*)"] | 10 | 0.608 |
| [S13/Q11](#s13) | success | ["customer_credit_rating_table"] | 0 / {} | ["\"Credit Grade\""] | ["COUNT(*)"] | 5 | 0.505 |
| [S14/Q12](#s14) | success | ["customer_segments_table"] | 0 / {} | ["\"Segment Name\""] | ["COUNT(*)"] | 5 | 0.511 |
| [S15/Q13](#s15) | success | ["customer_contact_table"] | 0 / {} | [] | [] | 2 | 0.431 |
| [S16/Q14](#s16) | success | ["membership_table"] | 0 / {} | [] | [] | 3 | 0.437 |
| [S17/Q15](#s17) | success | ["membership_table"] | 0 / {} | [] | [] | 5 | 0.407 |
| [S18/Q16](#s18) | success | ["contracts_table"] | 0 / {} | [] | [] | 3 | 0.429 |
| [S19/Q17](#s19) | success | ["customer_account_table"] | 0 / {} | [] | [] | 5 | 0.473 |
| [S20/Q18](#s20) | success | ["customer_account_table"] | 0 / {} | [] | [] | 3 | 0.459 |
| [S21/Q19](#s21) | success | ["membership_table", "transaction_history_table"] | 2 / {'LEFT': 1} | ["\"Customer ID\"", "m.\"Membership Level\""] | ["SUM(\"Transaction Amount\")", "COUNT(*)", "SUM(\"Transaction Amount\")", "COUNT(DISTINCT hv.\"Customer ID\")"] | 6 | 4.977 |
| [S22/Q20](#s22) | success | ["customer_tag_table", "transaction_history_table"] | 2 / {'LEFT': 1} | ["\"Customer ID\"", "t.\"Tag Name\""] | ["SUM(\"Transaction Amount\")", "SUM(\"Transaction Amount\")", "COUNT(DISTINCT hv.\"Customer ID\")", "SUM(t.\"Tag Weight Value\")"] | 10 | 6.962 |
| [S23/Q21](#s23) | success | ["customer_account_table", "customer_credit_rating_table", "transaction_history_table"] | 3 / {'LEFT': 2} | ["\"Customer ID\"", "c.\"Credit Grade\""] | ["SUM(\"Transaction Amount\")", "SUM(\"Transaction Amount\")", "COUNT(DISTINCT hv.\"Customer ID\")", "AVG(c.\"Credit Score\")"] | 6 | 6.368 |
| [S24/Q22](#s24) | success | ["customer_segments_table", "transaction_history_table"] | 2 / {'LEFT': 1} | ["\"Customer ID\"", "s.\"Segment Name\""] | ["SUM(\"Transaction Amount\")", "SUM(\"Transaction Amount\")", "COUNT(DISTINCT hv.\"Customer ID\")"] | 1 | 4.54 |
| [S25/Q23](#s25) | failed | ["transaction_history_table"] | 0 / {} | ["LEFT(\"Customer ID\", 1)", "LENGTH(\"Customer ID\")"] | [] | unknown | 未取得；调用总时长 0.151 ms |
| [S26/Q24](#s26) | failed | ["membership_table"] | 0 / {} | ["LEFT(\"Customer ID\", 1)", "LENGTH(\"Customer ID\")"] | ["COUNT(*)"] | unknown | 未取得；调用总时长 0.14 ms |
| [S27/Q25](#s27) | failed | ["customer_tag_table"] | 0 / {} | ["LEFT(\"Customer ID\", 1)", "LENGTH(\"Customer ID\")"] | ["COUNT(*)"] | unknown | 未取得；调用总时长 0.141 ms |
| [S28/Q26](#s28) | failed | ["customer_segments_table"] | 0 / {} | ["LEFT(\"Customer ID\", 1)", "LENGTH(\"Customer ID\")"] | ["COUNT(*)"] | unknown | 未取得；调用总时长 0.136 ms |
| [S29/Q27](#s29) | success | ["transaction_history_table"] | 0 / {} | ["SUBSTRING(\"Customer ID\", 1, 1)", "LENGTH(\"Customer ID\")"] | ["COUNT(*)"] | 1 | 0.576 |
| [S30/Q28](#s30) | success | ["membership_table"] | 0 / {} | ["SUBSTRING(\"Customer ID\", 1, 1)", "LENGTH(\"Customer ID\")"] | ["COUNT(*)"] | 1 | 0.536 |
| [S31/Q29](#s31) | success | ["customer_tag_table"] | 0 / {} | ["SUBSTRING(\"Customer ID\", 1, 1)", "LENGTH(\"Customer ID\")"] | ["COUNT(*)"] | 1 | 0.741 |
| [S32/Q30](#s32) | success | ["customer_segments_table"] | 0 / {} | ["SUBSTRING(\"Customer ID\", 1, 1)", "LENGTH(\"Customer ID\")"] | ["COUNT(*)"] | 1 | 0.545 |
| [S33/Q31](#s33) | success | ["customer_contact_table"] | 0 / {} | ["SUBSTRING(\"Customer ID\", 1, 1)", "LENGTH(\"Customer ID\")"] | ["COUNT(*)"] | 1 | 0.612 |
| [S34/Q32](#s34) | success | ["customer_account_table"] | 0 / {} | ["SUBSTRING(\"Customer ID\", 1, 1)", "LENGTH(\"Customer ID\")"] | ["COUNT(*)"] | 1 | 0.599 |
| [S35/Q33](#s35) | success | ["contracts_table"] | 0 / {} | ["SUBSTRING(\"Customer ID\", 1, 1)", "LENGTH(\"Customer ID\")"] | ["COUNT(*)"] | 1 | 0.613 |
| [S36/Q34](#s36) | success | ["financials_table"] | 0 / {} | ["SUBSTRING(\"Customer ID\", 1, 1)", "LENGTH(\"Customer ID\")"] | ["COUNT(*)"] | 1 | 0.682 |
| [S37/Q35](#s37) | success | ["product_service_order_table"] | 0 / {} | ["SUBSTRING(\"Customer ID\", 1, 1)", "LENGTH(\"Customer ID\")"] | ["COUNT(*)"] | 1 | 0.569 |
| [S38/Q36](#s38) | success | ["sales_follow_up_table"] | 0 / {} | ["SUBSTRING(\"Customer ID\", 1, 1)", "LENGTH(\"Customer ID\")"] | ["COUNT(*)"] | 1 | 0.576 |
| [S39/Q37](#s39) | success | ["customer_account_table"] | 0 / {} | [] | [] | 5 | 0.307 |
| [S40/Q38](#s40) | success | ["customer_credit_rating_table"] | 0 / {} | [] | [] | 5 | 0.44 |
| [S41/Q39](#s41) | success | ["customer_account_table", "customer_credit_rating_table"] | 2 / {'LEFT': 1} | [] | [] | 10 | 0.775 |
| [S42/Q40](#s42) | success | ["customer_account_table", "customer_credit_rating_table"] | 2 / {'INNER': 1} | [] | ["COUNT(*)", "COUNT(*)"] | 1 | 0.947 |
| [S43/Q41](#s43) | success | ["customer_credit_rating_table"] | 0 / {} | ["SUBSTRING(\"Account ID\", 1, 1)", "LENGTH(\"Account ID\")"] | ["COUNT(*)"] | 1 | 0.61 |
| [S44/Q42](#s44) | success | ["customer_account_table"] | 0 / {} | ["SUBSTRING(\"Account ID\", 1, 1)", "LENGTH(\"Account ID\")"] | ["COUNT(*)"] | 1 | 0.584 |
| [S45/Q43](#s45) | success | ["transaction_history_table"] | 0 / {} | ["SUBSTRING(\"Account ID\", 1, 1)", "LENGTH(\"Account ID\")"] | ["COUNT(*)"] | 1 | 0.554 |
| [S46/Q44](#s46) | success | ["contracts_table", "customer_account_table", "customer_contact_table", "customer_tag_table", "financials_table", "membership_table", "product_service_order_table", "sales_follow_up_table", "transaction_history_table"] | 0 / {} | ["\"Customer ID\""] | ["SUM(\"Transaction Amount\")", "COUNT(*)", "COUNT(*)", "COUNT(*)", "COUNT(*)", "COUNT(*)", "COUNT(*)", "COUNT(*)", "COUNT(*)", "COUNT(*)"] | 1 | 3.472 |
| [S47/Q45](#s47) | success | ["membership_table", "transaction_history_table"] | 2 / {'INNER': 1} | ["\"Customer ID\"", "m.\"Membership Level\""] | ["SUM(\"Transaction Amount\")", "COUNT(*)"] | 5 | 0.845 |
| [S48/Q46](#s48) | success | ["membership_table", "transaction_history_table"] | 2 / {'INNER': 1} | ["\"Customer ID\"", "m.\"Member Status\""] | ["SUM(\"Transaction Amount\")", "COUNT(*)"] | 3 | 0.862 |
| [S49/Q47](#s49) | success | ["membership_table", "transaction_history_table"] | 2 / {'INNER': 1} | ["\"Customer ID\"", "m.\"Privilege Level\""] | ["SUM(\"Transaction Amount\")", "COUNT(*)"] | 5 | 0.813 |
| [S50/Q48](#s50) | success | ["membership_table", "transaction_history_table"] | 2 / {'INNER': 1} | ["\"Customer ID\"", "m.\"Automatic Renewal\""] | ["SUM(\"Transaction Amount\")", "COUNT(*)"] | 2 | 0.845 |
| [S51/Q49](#s51) | success | ["customer_tag_table", "transaction_history_table"] | 2 / {'INNER': 1} | ["\"Customer ID\"", "t.\"Tag Name\""] | ["SUM(\"Transaction Amount\")", "COUNT(*)", "AVG(t.\"Tag Weight Value\")"] | 9 | 1.065 |
| [S52/Q50](#s52) | success | ["customer_contact_table", "transaction_history_table"] | 2 / {'INNER': 1} | ["\"Customer ID\"", "c.\"Gender\""] | ["SUM(\"Transaction Amount\")", "COUNT(*)"] | 2 | 0.903 |
| [S53/Q51](#s53) | success | ["contracts_table", "transaction_history_table"] | 2 / {'INNER': 1} | ["\"Customer ID\"", "ct.\"Contract Type\""] | ["SUM(\"Transaction Amount\")", "COUNT(*)"] | 3 | 0.878 |
| [S54/Q52](#s54) | success | ["customer_account_table", "customer_credit_rating_table", "transaction_history_table"] | 3 / {'INNER': 2} | ["\"Customer ID\"", "cr.\"Credit Grade\""] | ["SUM(\"Transaction Amount\")", "COUNT(*)", "AVG(cr.\"Credit Score\")", "AVG(cr.\"Credit Limit\")"] | 5 | 1.56 |
| [S55/Q53](#s55) | success | ["transaction_history_table"] | 2 / {'INNER': 1} | ["\"Customer ID\"", "t.\"Transaction Payment Method\""] | ["SUM(\"Transaction Amount\")", "COUNT(*)", "SUM(t.\"Transaction Amount\")"] | 4 | 0.779 |
| [S56/Q54](#s56) | success | ["transaction_history_table"] | 0 / {} | ["\"Customer ID\""] | ["SUM(\"Transaction Amount\")", "COUNT(*)", "SUM(\"Transaction Amount\")", "MIN(paid_amt)", "MAX(paid_amt)", "AVG(paid_amt)", "SUM(paid_amt)", "COUNT(*)", "AVG(n_tx)"] | 1 | 0.61 |
| [S57/Q55](#s57) | success | ["transaction_history_table"] | 0 / {} | ["\"Customer ID\"", "n_tx"] | ["COUNT(*)", "COUNT(*)"] | 1 | 0.753 |
| [S58/Q56](#s58) | success | ["transaction_history_table"] | 0 / {} | ["\"Customer ID\""] | ["SUM(CASE WHEN \"Transaction Payment Status\" = 'Paid' THEN \"Transaction Amount\" ELSE 0 END)", "COUNT(*)", "SUM(\"Transaction Amount\")", "SUM(CASE WHEN \"Transaction Payment Status\" = 'Paid' THEN \"Transaction Amount\" ELSE 0 END)", "COUNT(*)", "SUM(all_tx)", "SUM(CASE WHEN all_tx > 1 THEN 1 ELSE 0 END)", "AVG(total_amt_all)"] | 1 | 0.988 |
| [S59/Q57](#s59) | success | ["transaction_history_table"] | 0 / {} | ["\"Transaction Payment Status\""] | ["COUNT(*)", "SUM(\"Transaction Amount\")"] | 3 | 0.533 |
| [S60/Q58](#s60) | success | ["financials_table", "transaction_history_table"] | 2 / {'INNER': 1} | ["\"Customer ID\"", "f.\"Outstanding Amount\""] | ["SUM(\"Transaction Amount\")", "COUNT(*)", "AVG(f.\"Outstanding Amount\")", "AVG(f.\"Amount Received\")", "AVG(f.\"Receivable Amount\")"] | 34 | 0.953 |
| [S61/Q59](#s61) | success | ["product_service_order_table", "transaction_history_table"] | 2 / {'INNER': 1} | ["\"Customer ID\"", "po.\"Subscribed Product Name\""] | ["SUM(\"Transaction Amount\")", "COUNT(*)", "SUM(po.\"Total Amount\")"] | 5 | 0.891 |
| [S62/Q60](#s62) | success | ["channel_source_table", "transaction_history_table"] | 2 / {'INNER': 1} | ["\"Customer ID\"", "cs.\"Channel Name\""] | ["SUM(\"Transaction Amount\")", "COUNT(*)"] | 5 | 1.086 |
| [S63/Q61](#s63) | success | ["contracts_table", "transaction_history_table"] | 2 / {'INNER': 1} | ["\"Customer ID\"", "ct.\"Contract Performance Status\""] | ["SUM(\"Transaction Amount\")", "COUNT(*)"] | 3 | 0.865 |
| [S64/Q62](#s64) | success | ["product_service_order_table", "transaction_history_table"] | 2 / {'INNER': 1} | ["\"Customer ID\"", "po.\"Current Service Status\""] | ["SUM(\"Transaction Amount\")", "COUNT(*)", "SUM(po.\"Total Amount\")"] | 3 | 0.813 |
| [S65/Q63](#s65) | success | ["sales_follow_up_table", "transaction_history_table"] | 2 / {'INNER': 1} | ["\"Customer ID\"", "sf.\"Follow-up Result Status\"", "sf.\"Follow-up Priority\""] | ["SUM(\"Transaction Amount\")", "COUNT(*)"] | 12 | 0.831 |
| [S66/Q64](#s66) | success | ["customer_account_table"] | 0 / {} | [] | ["COUNT(DISTINCT \"Customer ID\")", "COUNT(*)"] | 1 | 0.624 |
| [S67/Q65](#s67) | success | ["customer_account_table", "transaction_history_table"] | 2 / {'INNER': 1} | [] | ["COUNT(*)"] | 1 | 0.886 |
| [S68/Q66](#s68) | failed | ["customer_account_table", "transaction_history_table"] | 2 / {'LEFT': 1} | ["\"Customer ID\"", "a.\"Account Type\""] | ["SUM(\"Transaction Amount\")", "COUNT(DISTINCT t.\"Customer ID\")"] | unknown | 未取得；调用总时长 0.211 ms |
| [S69/Q67](#s69) | success | ["customer_account_table"] | 0 / {} | ["a.\"Account Type\""] | ["COUNT(*)"] | 3 | 0.528 |
| [S70/Q68](#s70) | success | ["customer_account_table", "transaction_history_table"] | 2 / {'INNER': 1} | ["\"Customer ID\"", "a.\"Account Type\""] | ["SUM(\"Transaction Amount\")", "COUNT(*)"] | 3 | 0.833 |
| [S71/Q69](#s71) | success | ["customer_account_table", "transaction_history_table"] | 2 / {'INNER': 1} | ["\"Customer ID\"", "a.\"Account Credit Rating\""] | ["SUM(\"Transaction Amount\")", "COUNT(*)"] | 3 | 0.929 |
| [S72/Q70](#s72) | success | ["customer_account_table"] | 0 / {} | ["a.\"Account Credit Rating\""] | ["COUNT(*)"] | 5 | 0.529 |
| [S73/Q71](#s73) | success | ["membership_table"] | 0 / {} | ["\"Membership Level\""] | ["COUNT(*)"] | 5 | 0.497 |
| [S74/Q72](#s74) | success | ["membership_table", "transaction_history_table"] | 2 / {'INNER': 1} | ["\"Customer ID\"", "m.\"Membership Level\""] | ["SUM(\"Transaction Amount\")", "COUNT(*)"] | 5 | 0.925 |
| [S75/Q73](#s75) | success | ["customer_tag_table"] | 0 / {} | ["\"Tag Name\""] | ["COUNT(*)"] | 10 | 0.817 |
| [S76/Q74](#s76) | success | ["contracts_table"] | 0 / {} | ["\"Contract Type\""] | ["COUNT(*)"] | 3 | 0.544 |
| [S77/Q75](#s77) | success | ["contracts_table"] | 0 / {} | ["\"Contract Performance Status\""] | ["COUNT(*)"] | 3 | 0.533 |
| [S78/Q76](#s78) | success | ["product_service_order_table"] | 0 / {} | ["\"Subscribed Product Name\""] | ["COUNT(*)", "SUM(\"Total Amount\")"] | 5 | 0.548 |
| [S79/Q77](#s79) | success | ["customer_contact_table"] | 0 / {} | ["\"Gender\""] | ["COUNT(*)"] | 2 | 0.52 |
| [S80/Q78](#s80) | success | ["customer_contact_table", "transaction_history_table"] | 2 / {'INNER': 1} | ["\"Customer ID\"", "c.\"Gender\""] | ["SUM(\"Transaction Amount\")", "COUNT(*)"] | 2 | 0.83 |
| [S81/Q79](#s81) | success | ["channel_source_table"] | 0 / {} | ["\"Channel Name\""] | ["COUNT(*)"] | 5 | 0.718 |
| [S82/Q80](#s82) | success | ["channel_source_table", "transaction_history_table"] | 2 / {'INNER': 1} | ["\"Customer ID\"", "cs.\"Channel Name\""] | ["SUM(\"Transaction Amount\")", "COUNT(*)"] | 5 | 0.829 |
| [S83/Q81](#s83) | success | ["complaints_table"] | 0 / {} | ["\"Complaint Customer Satisfaction\""] | ["COUNT(*)"] | 5 | 0.471 |
| [S84/Q82](#s84) | success | ["service_ticket_table"] | 0 / {} | ["\"Ticket customer satisfaction score\""] | ["COUNT(*)"] | 5 | 0.671 |
| [S85/Q83](#s85) | success | ["complaints_table", "service_ticket_table"] | 2 / {'INNER': 1} | [] | ["COUNT(*)"] | 1 | 1.012 |
| [S86/Q84](#s86) | success | ["contracts_table", "service_ticket_table"] | 2 / {'INNER': 1} | [] | ["COUNT(*)"] | 1 | 0.916 |
| [S87/Q85](#s87) | success | ["contracts_table", "service_ticket_table", "transaction_history_table"] | 3 / {'INNER': 2} | ["\"Customer ID\"", "s.\"Ticket customer satisfaction score\""] | ["SUM(\"Transaction Amount\")", "COUNT(*)"] | 5 | 2.127 |
| [S88/Q86](#s88) | success | ["complaints_table", "contracts_table", "service_ticket_table", "transaction_history_table"] | 4 / {'INNER': 3} | ["\"Customer ID\"", "comp.\"Complaint Customer Satisfaction\""] | ["SUM(\"Transaction Amount\")", "COUNT(*)"] | 5 | 1.857 |
| [S89/Q87](#s89) | success | ["service_ticket_table"] | 0 / {} | ["s.\"Ticket customer satisfaction score\""] | ["COUNT(*)"] | 5 | 0.565 |
| [S90/Q88](#s90) | success | ["complaints_table"] | 0 / {} | ["comp.\"Complaint Customer Satisfaction\""] | ["COUNT(*)"] | 5 | 0.499 |
| [S91/Q89](#s91) | success | ["contracts_table", "service_ticket_table", "transaction_history_table"] | 3 / {'INNER': 2} | ["\"Customer ID\""] | ["SUM(\"Transaction Amount\")", "COUNT(DISTINCT s.\"Work Order ID\")", "AVG(s.\"Ticket customer satisfaction score\")", "AVG(s.\"Ticket resolution duration\")"] | 1 | 22.358 |
| [S92/Q90](#s92) | success | ["service_ticket_table"] | 0 / {} | [] | ["AVG(\"Ticket customer satisfaction score\")", "AVG(\"Ticket resolution duration\")"] | 1 | 0.573 |
| [S93/Q91](#s93) | success | ["membership_table", "transaction_history_table"] | 2 / {'INNER': 1} | ["\"Customer ID\""] | ["SUM(\"Transaction Amount\")", "AVG(m.\"Current Points\")", "AVG(m.\"Lifetime Points\")", "MIN(m.\"Lifetime Points\")", "MAX(m.\"Lifetime Points\")"] | 1 | 0.852 |
| [S94/Q92](#s94) | success | ["membership_table"] | 0 / {} | [] | ["AVG(\"Current Points\")", "AVG(\"Lifetime Points\")", "MIN(\"Lifetime Points\")", "MAX(\"Lifetime Points\")"] | 1 | 0.456 |
| [S95/Q93](#s95) | success | ["membership_table", "transaction_history_table"] | 2 / {'INNER': 1} | ["\"Customer ID\"", "m.\"Upgrade Requirements Met\""] | ["SUM(\"Transaction Amount\")", "COUNT(*)"] | 2 | 1.163 |
| [S96/Q94](#s96) | success | ["membership_table"] | 0 / {} | ["\"Upgrade Requirements Met\""] | ["COUNT(*)"] | 2 | 0.62 |
| [S97/Q95](#s97) | success | ["customer_credit_rating_table", "transaction_history_table"] | 2 / {'CROSS': 1} | [] | ["COUNT(DISTINCT t.\"Account ID\")", "COUNT(DISTINCT cr.\"Account ID\")", "COUNT(DISTINCT CASE WHEN t.\"Account ID\" = cr.\"Account ID\" THEN t.\"Account ID\" END)"] | 1 | 151.556 |
| [S98/Q96](#s98) | success | ["customer_credit_rating_table", "transaction_history_table"] | 2 / {'INNER': 1} | [] | ["COUNT(*)"] | 1 | 1.514 |
| [S99/Q97](#s99) | success | ["customer_credit_rating_table", "transaction_history_table"] | 2 / {'INNER': 1} | [] | ["COUNT(*)"] | 1 | 1.201 |
| [S100/Q98](#s100) | success | ["customer_credit_rating_table", "transaction_history_table"] | 3 / {'INNER': 2} | ["\"Customer ID\"", "cr.\"Credit Grade\""] | ["SUM(\"Transaction Amount\")", "COUNT(*)", "AVG(cr.\"Credit Score\")", "AVG(cr.\"Credit Limit\")"] | 5 | 2.123 |
| [S101/Q99](#s101) | success | ["customer_credit_rating_table", "transaction_history_table"] | 2 / {'INNER': 1} | ["cr.\"Credit Grade\""] | ["COUNT(*)", "AVG(cr.\"Credit Score\")", "AVG(cr.\"Credit Limit\")"] | 5 | 1.347 |
| [S102/Q100](#s102) | success | ["customer_credit_rating_table"] | 0 / {} | ["cr.\"Credit Grade\""] | ["COUNT(*)", "AVG(cr.\"Credit Score\")", "AVG(cr.\"Credit Limit\")"] | 5 | 0.618 |
| [S103/Q101](#s103) | success | ["financials_table", "transaction_history_table"] | 2 / {'INNER': 1} | ["\"Customer ID\""] | ["SUM(\"Transaction Amount\")", "AVG(f.\"Receivable Amount\")", "AVG(f.\"Amount Received\")", "AVG(f.\"Outstanding Amount\")", "AVG(f.\"Tax Amount\")"] | 1 | 0.86 |
| [S104/Q102](#s104) | success | ["financials_table"] | 0 / {} | [] | ["AVG(\"Receivable Amount\")", "AVG(\"Amount Received\")", "AVG(\"Outstanding Amount\")", "AVG(\"Tax Amount\")"] | 1 | 0.473 |
| [S105/Q103](#s105) | success | ["transaction_history_table"] | 2 / {'INNER': 1} | ["\"Customer ID\"", "t.\"Transaction Currency\""] | ["SUM(\"Transaction Amount\")", "COUNT(*)", "SUM(t.\"Transaction Amount\")"] | 1 | 1.135 |
| [S106/Q104](#s106) | success | ["transaction_history_table"] | 0 / {} | [] | [] | 1 | 0.395 |
| [S107/Q105](#s107) | success | ["customer_device_table", "transaction_history_table"] | 2 / {'INNER': 1} | ["\"Customer ID\"", "d.\"Device Type\""] | ["SUM(\"Transaction Amount\")", "COUNT(*)"] | 5 | 1.343 |
| [S108/Q106](#s108) | success | ["customer_device_table"] | 0 / {} | ["\"Device Type\""] | ["COUNT(*)"] | 5 | 0.515 |
| [S109/Q107](#s109) | success | ["permissions_table", "transaction_history_table"] | 2 / {'INNER': 1} | ["\"Customer ID\"", "p.\"Role Name\""] | ["SUM(\"Transaction Amount\")", "COUNT(*)"] | 5 | 1.303 |
| [S110/Q108](#s110) | success | ["permissions_table"] | 0 / {} | ["\"Role Name\""] | ["COUNT(*)"] | 5 | 0.733 |
| [S111/Q109](#s111) | success | ["campaign_participation_table", "transaction_history_table"] | 2 / {'INNER': 1} | ["\"Customer ID\"", "cp.\"Event Participation Prize Level\""] | ["SUM(\"Transaction Amount\")", "COUNT(*)"] | 0 | 0.935 |
| [S112/Q110](#s112) | success | ["campaign_participation_table"] | 0 / {} | ["\"Event Participation Prize Level\""] | ["COUNT(*)"] | 3 | 0.499 |
| [S113/Q111](#s113) | success | ["customer_feedback_table", "transaction_history_table"] | 2 / {'INNER': 1} | ["\"Customer ID\"", "cf.\"Satisfaction Rating\""] | ["SUM(\"Transaction Amount\")", "COUNT(*)"] | 0 | 0.796 |
| [S114/Q112](#s114) | success | ["customer_feedback_table"] | 0 / {} | ["\"Satisfaction Rating\""] | ["COUNT(*)"] | 5 | 0.711 |
| [S115/Q113](#s115) | success | ["customer_contact_table"] | 0 / {} | ["SUBSTRING(\"Contact\", 1, 1)", "LENGTH(\"Contact\")"] | ["COUNT(*)"] | 143 | 0.888 |
| [S116/Q114](#s116) | success | ["campaign_participation_table"] | 0 / {} | ["SUBSTRING(\"Event Participant Contact ID\", 1, 1)", "LENGTH(\"Event Participant Contact ID\")"] | ["COUNT(*)"] | 1 | 0.577 |
| [S117/Q115](#s117) | success | ["customer_feedback_table"] | 0 / {} | ["SUBSTRING(\"Contact ID\", 1, 1)", "LENGTH(\"Contact ID\")"] | ["COUNT(*)"] | 1 | 0.559 |
| [S118/Q116](#s118) | success | ["customer_tag_table"] | 0 / {} | ["SUBSTRING(\"Contact ID\", 1, 1)", "LENGTH(\"Contact ID\")"] | ["COUNT(*)"] | 1 | 0.663 |
| [S119/Q117](#s119) | success | ["customer_feedback_table", "customer_tag_table"] | 2 / {'INNER': 1} | [] | ["COUNT(*)"] | 1 | 1.787 |
| [S120/Q118](#s120) | success | ["customer_feedback_table", "customer_tag_table", "transaction_history_table"] | 3 / {'INNER': 2} | ["\"Customer ID\"", "cf.\"Satisfaction Rating\""] | ["SUM(\"Transaction Amount\")", "COUNT(*)"] | 5 | 1.491 |
| [S121/Q119](#s121) | success | ["customer_contact_table", "customer_tag_table"] | 2 / {'INNER': 1} | [] | ["COUNT(*)"] | 1 | 1.338 |
| [S122/Q120](#s122) | success | ["campaign_participation_table", "customer_tag_table", "transaction_history_table"] | 3 / {'INNER': 2} | ["\"Customer ID\"", "cp.\"Event Participation Prize Level\""] | ["SUM(\"Transaction Amount\")", "COUNT(*)"] | 0 | 1.483 |


## 元数据和设置

| SQL | 类别 | 状态 | 内容 |
| --- | --- | --- | --- |
| S1 | connection_setup | success | PRAGMA query_only=ON |
| S2 | metadata | success | SELECT name,sql FROM sqlite_master WHERE type='table' ORDER BY name |


## Python 与执行位置

人工源码审查：**reviewed_SQL_dominant_with_chart_arithmetic**。The core high-value-customer cohort, joins and categorical summaries are in SQL. The sole Python call renders literal summary arrays and converts counts into chart percentages; no pandas joins/groupby over exported raw rows were observed. The small chart-percentage arithmetic is SQL-capable and disclosed, while rendering is an allowed use. Literal arrays are not automatically asserted to equal archived query results. The trajectory hit its SQL call cap and is analyzed separately as truncated despite having submitted an answer. [证据](../reviews/dacomp-033.json)。

P1：Creating comprehensive visualizations comparing high-value customers (cumulative paid > 5000) with general customer population across membership, tags, credit ratings, and other dimensions. Python needed for matplotlib visualizations.

[源码](../../../runs/dsv4flash-db-first-full-01/dacomp-033/attempt-01/python/P1.py)；[输出](../../../runs/dsv4flash-db-first-full-01/dacomp-033/attempt-01/python/P1.stdout)；[错误](../../../runs/dsv4flash-db-first-full-01/dacomp-033/attempt-01/python/P1.stderr)。自动源码筛查未检出预设迁出信号；这不是全面语义合规证明。

## 优化机会

已验证候选。筛选限于精确 SQL、相同自包含 CTE、相同单表完整过滤、可分解单表聚合；未覆盖任意 Join 等价和一般谓词蕴含。全部候选都是 offline，未测在线预测。

| 候选 | 类型 | 已有结果 | 覆盖 SQL | 后续次数 | 中间行数 | 验证 | 成本 |
| --- | --- | --- | --- | --- | --- | --- | --- |
| C1 | common subexpression | False | ["S21", "S56"] | 1 | unknown | not_verified_cap | Not tested |
| C2 | common subexpression | False | ["S22", "S23", "S24"] | 2 | unknown | not_verified_cap | Not tested |
| C3 | common subexpression | False | ["S46", "S47", "S48", "S49", "S50", "S51", "S52", "S53", "S54", "S55", "S60", "S61", "S62", "S63", "S64", "S65", "S74", "S80", "S82", "S87", "S88", "S91", "S93", "S95", "S100", "S103", "S105", "S107", "S109", "S111", "S113", "S120", "S122"] | 32 | 71 | rejected_result_mismatch | Not benchmarked; correctness alone does not establish net speedup. |
| C4 | aggregate MV | False | ["S7", "S29", "S45", "S59"] | 3 | unknown | not_verified_cap | Not tested |
| C5 | aggregate MV | False | ["S11", "S30", "S73", "S94", "S96"] | 4 | 10 | verified | Not benchmarked; correctness alone does not establish net speedup. |
| C6 | aggregate MV | False | ["S12", "S31", "S75", "S118"] | 3 | 10 | verified | Not benchmarked; correctness alone does not establish net speedup. |
| C7 | aggregate MV | False | ["S13", "S43", "S102"] | 2 | unknown | not_verified_cap | Not tested |
| C8 | aggregate MV | False | ["S14", "S32"] | 1 | unknown | not_verified_cap | Not tested |
| C9 | aggregate MV | False | ["S33", "S79", "S115"] | 2 | unknown | not_verified_cap | Not tested |
| C10 | aggregate MV | False | ["S35", "S76", "S77"] | 2 | unknown | not_verified_cap | Not tested |
| C11 | aggregate MV | False | ["S34", "S44", "S69", "S72"] | 3 | unknown | not_verified_cap | Not tested |
| C12 | aggregate MV | False | ["S36", "S104"] | 1 | unknown | not_verified_cap | Not tested |
| C13 | aggregate MV | False | ["S37", "S78"] | 1 | unknown | not_verified_cap | Not tested |
| C14 | aggregate MV | False | ["S83", "S90"] | 1 | unknown | not_verified_cap | Not tested |
| C15 | aggregate MV | False | ["S84", "S89", "S92"] | 2 | unknown | not_verified_cap | Not tested |
| C16 | aggregate MV | False | ["S112", "S116"] | 1 | unknown | not_verified_cap | Not tested |
| C17 | aggregate MV | False | ["S114", "S117"] | 1 | unknown | not_verified_cap | Not tested |


已验证覆盖（含触发查询、候选并集去重）：9/115 条成功数据 SQL。正确性仅针对当前数据库快照；未测性能的候选不能声称已加速。

[完整 build/rewrite 与比较证据](dacomp-033.analysis.json)。

### C5：aggregate MV

Union of grouping keys; decomposable aggregate states; AVG uses SUM and non-NULL COUNT.

原查询 [S11](#s11), [S30](#s30), [S73](#s73), [S94](#s94), [S96](#s96) → 新增共享状态 C5 → 后续 4 次可复用。该构建点为事后假设，不代表 Agent 当时预知后续。

构建定义：

```sql
SELECT "Membership Level" AS __g0, SUBSTRING("Customer ID", 1, 1) AS __g1, LENGTH("Customer ID") AS __g2, "Upgrade Requirements Met" AS __g3, COUNT(*) AS __a0, SUM("Current Points") AS __a1_sum, COUNT("Current Points") AS __a1_n, SUM("Lifetime Points") AS __a2_sum, COUNT("Lifetime Points") AS __a2_n, MIN("Lifetime Points") AS __a3, MAX("Lifetime Points") AS __a4 FROM "membership_table"  GROUP BY "Membership Level", SUBSTRING("Customer ID", 1, 1), LENGTH("Customer ID"), "Upgrade Requirements Met"
```

受益查询 S11 的改写示例：

```sql
SELECT __g0 AS "Membership Level", SUM(__a0) AS cnt FROM temp.reuse_candidate GROUP BY __g0 ORDER BY cnt DESC
```

| 原 SQL | 列名一致 | 结果一致 | 比较方法 |
| --- | --- | --- | --- |
| S11 | True | True | ordered_numeric_tolerance |
| S30 | True | True | exact_multiset |
| S73 | True | True | ordered_numeric_tolerance |
| S94 | True | True | exact_multiset |
| S96 | True | True | exact_multiset |


验证状态：verified；成本结论：Not benchmarked; correctness alone does not establish net speedup.

### C6：aggregate MV

Union of grouping keys; decomposable aggregate states; AVG uses SUM and non-NULL COUNT.

原查询 [S12](#s12), [S31](#s31), [S75](#s75), [S118](#s118) → 新增共享状态 C6 → 后续 3 次可复用。该构建点为事后假设，不代表 Agent 当时预知后续。

构建定义：

```sql
SELECT "Tag Name" AS __g0, SUBSTRING("Customer ID", 1, 1) AS __g1, LENGTH("Customer ID") AS __g2, SUBSTRING("Contact ID", 1, 1) AS __g3, LENGTH("Contact ID") AS __g4, COUNT(*) AS __a0 FROM "customer_tag_table"  GROUP BY "Tag Name", SUBSTRING("Customer ID", 1, 1), LENGTH("Customer ID"), SUBSTRING("Contact ID", 1, 1), LENGTH("Contact ID")
```

受益查询 S12 的改写示例：

```sql
SELECT __g0 AS "Tag Name", SUM(__a0) AS cnt FROM temp.reuse_candidate GROUP BY __g0 ORDER BY cnt DESC LIMIT 20
```

| 原 SQL | 列名一致 | 结果一致 | 比较方法 |
| --- | --- | --- | --- |
| S12 | True | True | ordered_numeric_tolerance |
| S31 | True | True | exact_multiset |
| S75 | True | True | ordered_numeric_tolerance |
| S118 | True | True | exact_multiset |


验证状态：verified；成本结论：Not benchmarked; correctness alone does not establish net speedup.

### C3：common subexpression

Identical self-contained CTE body across queries.

原查询 [S46](#s46), [S47](#s47), [S48](#s48), [S49](#s49), [S50](#s50), [S51](#s51), [S52](#s52), [S53](#s53), [S54](#s54), [S55](#s55), [S60](#s60), [S61](#s61), [S62](#s62), [S63](#s63), [S64](#s64), [S65](#s65), [S74](#s74), [S80](#s80), [S82](#s82), [S87](#s87), [S88](#s88), [S91](#s91), [S93](#s93), [S95](#s95), [S100](#s100), [S103](#s103), [S105](#s105), [S107](#s107), [S109](#s109), [S111](#s111), [S113](#s113), [S120](#s120), [S122](#s122) → 新增共享状态 C3 → 后续 32 次可复用。该构建点为事后假设，不代表 Agent 当时预知后续。

构建定义：

```sql
SELECT DISTINCT "Customer ID" FROM transaction_history_table WHERE "Transaction Payment Status" = 'Paid' GROUP BY "Customer ID" HAVING SUM("Transaction Amount") > 5000
```

受益查询 S46 的改写示例：

```sql
WITH hv AS (SELECT * FROM temp.reuse_candidate) SELECT (SELECT COUNT(*) FROM hv) AS total_hv, (SELECT COUNT(*) FROM hv WHERE "Customer ID" IN (SELECT "Customer ID" FROM membership_table)) AS in_membership, (SELECT COUNT(*) FROM hv WHERE "Customer ID" IN (SELECT "Customer ID" FROM customer_tag_table)) AS in_tags, (SELECT COUNT(*) FROM hv WHERE "Customer ID" IN (SELECT "Customer ID" FROM customer_contact_table)) AS in_contact, (SELECT COUNT(*) FROM hv WHERE "Customer ID" IN (SELECT "Customer ID" FROM contracts_table)) AS in_contracts, (SELECT COUNT(*) FROM hv WHERE "Customer ID" IN (SELECT "Customer ID" FROM financials_table)) AS in_financials, (SELECT COUNT(*) FROM hv WHERE "Customer ID" IN (SELECT "Customer ID" FROM product_service_order_table)) AS in_orders, (SELECT COUNT(*) FROM hv WHERE "Customer ID" IN (SELECT "Customer ID" FROM customer_account_table)) AS in_accounts, (SELECT COUNT(*) FROM hv WHERE "Customer ID" IN (SELECT "Customer ID" FROM sales_follow_up_table)) AS in_followup
```

| 原 SQL | 列名一致 | 结果一致 | 比较方法 |
| --- | --- | --- | --- |
| S46 | True | True | exact_multiset |
| S47 | True | True | ordered_numeric_tolerance |
| S48 | True | True | ordered_numeric_tolerance |
| S49 | True | True | ordered_numeric_tolerance |
| S50 | True | True | ordered_numeric_tolerance |
| S51 | True | True | ordered_numeric_tolerance |
| S52 | True | True | exact_multiset |
| S53 | True | True | ordered_numeric_tolerance |
| S54 | True | True | ordered_numeric_tolerance |
| S55 | True | True | ordered_numeric_tolerance |
| S60 | True | True | ordered_numeric_tolerance |
| S61 | True | True | ordered_numeric_tolerance |
| S62 | True | True | ordered_numeric_tolerance |
| S63 | True | True | ordered_numeric_tolerance |
| S64 | True | True | ordered_numeric_tolerance |
| S65 | True | True | ordered_numeric_tolerance |
| S74 | True | True | ordered_numeric_tolerance |
| S80 | True | True | exact_multiset |
| S82 | True | True | ordered_numeric_tolerance |
| S87 | True | True | exact_multiset |
| S88 | True | True | exact_multiset |
| S91 | True | True | exact_multiset |
| S93 | True | True | exact_multiset |
| S95 | True | True | exact_multiset |
| S100 | True | True | ordered_numeric_tolerance |
| S103 | True | False | exact_multiset |
| S105 | True | True | exact_multiset |
| S107 | True | True | ordered_numeric_tolerance |
| S109 | True | True | ordered_numeric_tolerance |
| S111 | True | True | ordered_numeric_tolerance |
| S113 | True | True | exact_multiset |
| S120 | True | True | exact_multiset |
| S122 | True | True | exact_multiset |


验证状态：rejected_result_mismatch；成本结论：Not benchmarked; correctness alone does not establish net speedup.

结果依赖：自动记录 SQL→Python 的接口父调用，以及源码中引用归档文件的消费者；字面值相同不认定因果。模型方向选择需要人工读取消息，尚未做全面因果标注。

[原始报告](../../../runs/dsv4flash-db-first-full-01/dacomp-033/attempt-01/answer.md)；[统一消息](../../../runs/dsv4flash-db-first-full-01/dacomp-033/attempt-01/messages.jsonl)；[原始 OpenCode 事件](../../../runs/dsv4flash-db-first-full-01/dacomp-033/attempt-01/opencode.jsonl)；[SQL 引擎日志](../../../runs/dsv4flash-db-first-full-01/dacomp-033/attempt-01/sql_journal.jsonl)。

[可读报告（本地图片链接规范化）](../answers/dacomp-033.md)。原始回答保留，分析结论未改写。

## S1

类别 `connection_setup`；来源 `connection`；调用 `52cfbba587694409a609568ad3792219`；状态 `success`。

```sql
PRAGMA query_only=ON
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-033/attempt-01/sql/S1.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-033/attempt-01/sql/S1.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-033/attempt-01/results/S1.rows.jsonl)；完整：True；SHA256：`e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`。

## S2

类别 `metadata`；来源 `list_db`；调用 `52cfbba587694409a609568ad3792219`；状态 `success`。

```sql
SELECT name,sql FROM sqlite_master WHERE type='table' ORDER BY name
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-033/attempt-01/sql/S2.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-033/attempt-01/sql/S2.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-033/attempt-01/results/S2.rows.jsonl)；完整：True；SHA256：`2c6faedce06ef30ba1a94a94ce6b11e8835fd623351f785ce3a08d61f286462d`。

## S3

类别 `data`；来源 `query_db`；调用 `a40d6a53c9d44eafbe12add97e75bc58`；状态 `success`。

```sql
SELECT * FROM transaction_history_table LIMIT 5
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-033/attempt-01/sql/S3.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-033/attempt-01/sql/S3.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-033/attempt-01/results/S3.rows.jsonl)；完整：True；SHA256：`5ac278d45ffec9853ab49c327f1d68c4035ca0761f5009a04e55d38299e56992`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "transaction_history_table", "kind": "base", "block": null, "base_tables": ["transaction_history_table"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |


## S4

类别 `data`；来源 `query_db`；调用 `e26a30384af14492b46018ff8d19d79e`；状态 `success`。

```sql
SELECT DISTINCT "Transaction Payment Status" FROM transaction_history_table
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-033/attempt-01/sql/S4.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-033/attempt-01/sql/S4.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-033/attempt-01/results/S4.rows.jsonl)；完整：True；SHA256：`b65d4cdc1e740a8f1108a64d47611defff3bc3ff8b4808fbc75d2a64a3302a18`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "transaction_history_table", "kind": "base", "block": null, "base_tables": ["transaction_history_table"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |


## S5

类别 `data`；来源 `query_db`；调用 `606d230856444d00b049ce8282da0d64`；状态 `success`。

```sql
SELECT DISTINCT "Transaction Payment Method" FROM transaction_history_table
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-033/attempt-01/sql/S5.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-033/attempt-01/sql/S5.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-033/attempt-01/results/S5.rows.jsonl)；完整：True；SHA256：`22e735f13cee29e8725fde1e22889f0f7265bdcca36b712750c4ea7c6e0f51bd`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "transaction_history_table", "kind": "base", "block": null, "base_tables": ["transaction_history_table"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |


## S6

类别 `data`；来源 `query_db`；调用 `4d959b67ff17408781d452eed004bd46`；状态 `success`。

```sql
SELECT COUNT(*) as total_customers, COUNT(DISTINCT "Customer ID") as unique_customers FROM transaction_history_table
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-033/attempt-01/sql/S6.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-033/attempt-01/sql/S6.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-033/attempt-01/results/S6.rows.jsonl)；完整：True；SHA256：`333d2b1f95516dc34153417a3e42b85937e30ab79f92d2cb909b2897337b7ee8`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "transaction_history_table", "kind": "base", "block": null, "base_tables": ["transaction_history_table"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |
| B1 | COUNT(DISTINCT "Customer ID") | [{"table": "transaction_history_table", "column": "Customer ID"}] | [] | False |


## S7

类别 `data`；来源 `query_db`；调用 `61b2731fd90b460da77b7f3c7a92f489`；状态 `success`。

```sql
SELECT "Customer ID", COUNT(*) as n_tx, SUM("Transaction Amount") as total_amt, SUM(CASE WHEN "Transaction Payment Status"='Paid' THEN "Transaction Amount" ELSE 0 END) as paid_amt FROM transaction_history_table GROUP BY "Customer ID" HAVING SUM(CASE WHEN "Transaction Payment Status"='Paid' THEN "Transaction Amount" ELSE 0 END) > 5000 ORDER BY paid_amt DESC
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-033/attempt-01/sql/S7.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-033/attempt-01/sql/S7.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-033/attempt-01/results/S7.rows.jsonl)；完整：True；SHA256：`68b860e7258b8b0520a70f4c2596d0a6f47c391a7c0a795a728219cc91b362f8`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "transaction_history_table", "kind": "base", "block": null, "base_tables": ["transaction_history_table"]}] | [] | ["\"Customer ID\""] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |
| B1 | SUM("Transaction Amount") | [{"table": "transaction_history_table", "column": "Transaction Amount"}] | [] | False |
| B1 | SUM(CASE WHEN "Transaction Payment Status" = 'Paid' THEN "Transaction Amount" ELSE 0 END) | [{"table": "transaction_history_table", "column": "Transaction Amount"}] | [{"table": "transaction_history_table", "column": "Transaction Payment Status"}] | False |
| B1 | SUM(CASE WHEN "Transaction Payment Status" = 'Paid' THEN "Transaction Amount" ELSE 0 END) | [{"table": "transaction_history_table", "column": "Transaction Amount"}] | [{"table": "transaction_history_table", "column": "Transaction Payment Status"}] | False |


## S8

类别 `data`；来源 `query_db`；调用 `73d6ce3389a34f80afcd0dcf775f2a6b`；状态 `success`。

```sql
SELECT COUNT(*) as cnt, COUNT(DISTINCT "Customer ID") as uniq_cust FROM membership_table
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-033/attempt-01/sql/S8.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-033/attempt-01/sql/S8.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-033/attempt-01/results/S8.rows.jsonl)；完整：True；SHA256：`80b609ce015948f757fbe3bced9dc10d7606cefd3d726a1ab278a70e54051a4b`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "membership_table", "kind": "base", "block": null, "base_tables": ["membership_table"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |
| B1 | COUNT(DISTINCT "Customer ID") | [{"table": "membership_table", "column": "Customer ID"}] | [] | False |


## S9

类别 `data`；来源 `query_db`；调用 `7f1fd9f52a60429b8ab3886159c43626`；状态 `success`。

```sql
SELECT COUNT(*) as cnt, COUNT(DISTINCT "Customer ID") as uniq_cust FROM customer_tag_table
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-033/attempt-01/sql/S9.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-033/attempt-01/sql/S9.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-033/attempt-01/results/S9.rows.jsonl)；完整：True；SHA256：`1ebfe826c46f1b1d68a90fc31b972607b6a335e7c7407bb1fe69fb31f76bfd92`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "customer_tag_table", "kind": "base", "block": null, "base_tables": ["customer_tag_table"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |
| B1 | COUNT(DISTINCT "Customer ID") | [{"table": "customer_tag_table", "column": "Customer ID"}] | [] | False |


## S10

类别 `data`；来源 `query_db`；调用 `f0c96e8ae3aa4f7cbe9badd505f06985`；状态 `success`。

```sql
SELECT COUNT(*) as cnt, COUNT(DISTINCT "Account ID") as uniq_acc FROM customer_credit_rating_table
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-033/attempt-01/sql/S10.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-033/attempt-01/sql/S10.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-033/attempt-01/results/S10.rows.jsonl)；完整：True；SHA256：`0b8258efc4fe7ecfe73ee6931cda975133f8e941b220fc2c09f6d32384dc4a3b`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "customer_credit_rating_table", "kind": "base", "block": null, "base_tables": ["customer_credit_rating_table"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |
| B1 | COUNT(DISTINCT "Account ID") | [{"table": "customer_credit_rating_table", "column": "Account ID"}] | [] | False |


## S11

类别 `data`；来源 `query_db`；调用 `3fdb6a5227f7484880f611f694c56f2b`；状态 `success`。

```sql
SELECT "Membership Level", COUNT(*) as cnt FROM membership_table GROUP BY "Membership Level" ORDER BY cnt DESC
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-033/attempt-01/sql/S11.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-033/attempt-01/sql/S11.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-033/attempt-01/results/S11.rows.jsonl)；完整：True；SHA256：`a706e0c9e4bc2dcfab4e798276c44b0b33d7acefe9cb58ac858b32491469fb2b`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "membership_table", "kind": "base", "block": null, "base_tables": ["membership_table"]}] | [] | ["\"Membership Level\""] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |


## S12

类别 `data`；来源 `query_db`；调用 `d906a66a70954fb98e73d39f5e3b9c7b`；状态 `success`。

```sql
SELECT "Tag Name", COUNT(*) as cnt FROM customer_tag_table GROUP BY "Tag Name" ORDER BY cnt DESC LIMIT 20
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-033/attempt-01/sql/S12.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-033/attempt-01/sql/S12.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-033/attempt-01/results/S12.rows.jsonl)；完整：True；SHA256：`99cbf70c3e11994a8d4f7e21ddb9902e6a7c363fa1a82726899730fc1286bfae`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "customer_tag_table", "kind": "base", "block": null, "base_tables": ["customer_tag_table"]}] | [] | ["\"Tag Name\""] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |


## S13

类别 `data`；来源 `query_db`；调用 `73ac77b4680d4615861b0d88a94035ed`；状态 `success`。

```sql
SELECT "Credit Grade", COUNT(*) as cnt FROM customer_credit_rating_table GROUP BY "Credit Grade" ORDER BY cnt DESC
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-033/attempt-01/sql/S13.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-033/attempt-01/sql/S13.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-033/attempt-01/results/S13.rows.jsonl)；完整：True；SHA256：`5132531d354b257fa3f84fd9e130ec9b8e7ec6f2c022c1a4073e5b5d9b734e4b`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "customer_credit_rating_table", "kind": "base", "block": null, "base_tables": ["customer_credit_rating_table"]}] | [] | ["\"Credit Grade\""] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |


## S14

类别 `data`；来源 `query_db`；调用 `80c82b170f934a198efab48e23fd7b36`；状态 `success`。

```sql
SELECT "Segment Name", COUNT(*) as cnt FROM customer_segments_table GROUP BY "Segment Name" ORDER BY cnt DESC
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-033/attempt-01/sql/S14.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-033/attempt-01/sql/S14.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-033/attempt-01/results/S14.rows.jsonl)；完整：True；SHA256：`d626b0218cf694f063523ed8a24d1e4ab75296ab197cab57d4b8c24855e8a264`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "customer_segments_table", "kind": "base", "block": null, "base_tables": ["customer_segments_table"]}] | [] | ["\"Segment Name\""] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |


## S15

类别 `data`；来源 `query_db`；调用 `5b2f367f4d624b3eb5d0b2d6113aa902`；状态 `success`。

```sql
SELECT DISTINCT "Gender" FROM customer_contact_table
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-033/attempt-01/sql/S15.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-033/attempt-01/sql/S15.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-033/attempt-01/results/S15.rows.jsonl)；完整：True；SHA256：`0574fdbc1ac9aafdd6e083b2978cfef222387d868dcb55c191c9e424e5e87023`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "customer_contact_table", "kind": "base", "block": null, "base_tables": ["customer_contact_table"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |


## S16

类别 `data`；来源 `query_db`；调用 `caad34c544bd4abe80a73f3c7c1989b2`；状态 `success`。

```sql
SELECT DISTINCT "Member Status" FROM membership_table
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-033/attempt-01/sql/S16.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-033/attempt-01/sql/S16.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-033/attempt-01/results/S16.rows.jsonl)；完整：True；SHA256：`9d656367a3ef9c256bf161ddc9ea525f98f39f990762af3e6a2165239531932e`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "membership_table", "kind": "base", "block": null, "base_tables": ["membership_table"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |


## S17

类别 `data`；来源 `query_db`；调用 `9689f532114343f4b7cbee2ea2e8de5e`；状态 `success`。

```sql
SELECT DISTINCT "Privilege Level" FROM membership_table
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-033/attempt-01/sql/S17.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-033/attempt-01/sql/S17.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-033/attempt-01/results/S17.rows.jsonl)；完整：True；SHA256：`c1bb00c0ee5588919194c3520d56ff63712b9e2380a02d8fac0f4406198828bd`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "membership_table", "kind": "base", "block": null, "base_tables": ["membership_table"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |


## S18

类别 `data`；来源 `query_db`；调用 `ba9a439c0bcb4b2fb41d84706610ebaa`；状态 `success`。

```sql
SELECT DISTINCT "Contract Type" FROM contracts_table
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-033/attempt-01/sql/S18.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-033/attempt-01/sql/S18.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-033/attempt-01/results/S18.rows.jsonl)；完整：True；SHA256：`7477b58d16df0793dfc8bbf0a023d2e583f06833e80ae99a5f9d20856137fe8d`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "contracts_table", "kind": "base", "block": null, "base_tables": ["contracts_table"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |


## S19

类别 `data`；来源 `query_db`；调用 `111b76d373704a36b4964f6eee939d2c`；状态 `success`。

```sql
SELECT DISTINCT "Account Credit Rating" FROM customer_account_table
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-033/attempt-01/sql/S19.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-033/attempt-01/sql/S19.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-033/attempt-01/results/S19.rows.jsonl)；完整：True；SHA256：`78048121cfa043ecd3adee91a70f7ba8ebe8132c64bba21bfbd34b8803f4ef8c`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "customer_account_table", "kind": "base", "block": null, "base_tables": ["customer_account_table"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |


## S20

类别 `data`；来源 `query_db`；调用 `0ed9f61739a94edcbcf3d339e0531889`；状态 `success`。

```sql
SELECT DISTINCT "Account Type" FROM customer_account_table
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-033/attempt-01/sql/S20.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-033/attempt-01/sql/S20.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-033/attempt-01/results/S20.rows.jsonl)；完整：True；SHA256：`98e0155fd533995b589a375f37a37686e73cd5948baa7c0da86f50004c126387`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "customer_account_table", "kind": "base", "block": null, "base_tables": ["customer_account_table"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |


## S21

类别 `data`；来源 `query_db`；调用 `7b097b2883a045d781c65736c9e321df`；状态 `success`。

```sql
WITH hv AS (
  SELECT "Customer ID", SUM("Transaction Amount") as paid_amt, COUNT(*) as n_tx
  FROM transaction_history_table
  WHERE "Transaction Payment Status"='Paid'
  GROUP BY "Customer ID"
  HAVING SUM("Transaction Amount") > 5000
)
SELECT m."Membership Level", COUNT(DISTINCT hv."Customer ID") as hv_customers
FROM hv LEFT JOIN membership_table m ON hv."Customer ID"=m."Customer ID"
GROUP BY m."Membership Level" ORDER BY hv_customers DESC
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-033/attempt-01/sql/S21.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-033/attempt-01/sql/S21.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-033/attempt-01/results/S21.rows.jsonl)；完整：True；SHA256：`64780ba1f039a3d5abc97c3046987eb3437bff23938a17cdcbd80ef225e669ce`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "transaction_history_table", "kind": "base", "block": null, "base_tables": ["transaction_history_table"]}] | [] | ["\"Customer ID\""] |
| B2 | [{"alias": "hv", "kind": "derived", "block": "B1", "base_tables": ["transaction_history_table"]}, {"alias": "m", "kind": "base", "block": null, "base_tables": ["membership_table"]}] | [{"type": "LEFT", "right": "membership_table AS m", "on": "hv.\"Customer ID\" = m.\"Customer ID\"", "using": []}] | ["m.\"Membership Level\""] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | SUM("Transaction Amount") | [{"table": "transaction_history_table", "column": "Transaction Amount"}] | [] | False |
| B1 | COUNT(*) | [] | [] | True |
| B1 | SUM("Transaction Amount") | [{"table": "transaction_history_table", "column": "Transaction Amount"}] | [] | False |
| B2 | COUNT(DISTINCT hv."Customer ID") | [{"table": "transaction_history_table", "column": "Customer ID"}] | [] | False |


## S22

类别 `data`；来源 `query_db`；调用 `4728a7c8f49d46249c8d905984931dff`；状态 `success`。

```sql
WITH hv AS (
  SELECT "Customer ID", SUM("Transaction Amount") as paid_amt
  FROM transaction_history_table
  WHERE "Transaction Payment Status"='Paid'
  GROUP BY "Customer ID"
  HAVING SUM("Transaction Amount") > 5000
)
SELECT t."Tag Name", COUNT(DISTINCT hv."Customer ID") as hv_customers, SUM(t."Tag Weight Value") as tot_weight
FROM hv LEFT JOIN customer_tag_table t ON hv."Customer ID"=t."Customer ID"
GROUP BY t."Tag Name" ORDER BY hv_customers DESC
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-033/attempt-01/sql/S22.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-033/attempt-01/sql/S22.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-033/attempt-01/results/S22.rows.jsonl)；完整：True；SHA256：`5376b6c70c6963d68cd97fad5aaca440fd48e49b0469f17f2d45008f03634ac9`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "transaction_history_table", "kind": "base", "block": null, "base_tables": ["transaction_history_table"]}] | [] | ["\"Customer ID\""] |
| B2 | [{"alias": "hv", "kind": "derived", "block": "B1", "base_tables": ["transaction_history_table"]}, {"alias": "t", "kind": "base", "block": null, "base_tables": ["customer_tag_table"]}] | [{"type": "LEFT", "right": "customer_tag_table AS t", "on": "hv.\"Customer ID\" = t.\"Customer ID\"", "using": []}] | ["t.\"Tag Name\""] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | SUM("Transaction Amount") | [{"table": "transaction_history_table", "column": "Transaction Amount"}] | [] | False |
| B1 | SUM("Transaction Amount") | [{"table": "transaction_history_table", "column": "Transaction Amount"}] | [] | False |
| B2 | COUNT(DISTINCT hv."Customer ID") | [{"table": "transaction_history_table", "column": "Customer ID"}] | [] | False |
| B2 | SUM(t."Tag Weight Value") | [{"table": "customer_tag_table", "column": "Tag Weight Value"}] | [] | False |


## S23

类别 `data`；来源 `query_db`；调用 `4626c9c976b14a5e898e1cd5f3d20091`；状态 `success`。

```sql
WITH hv AS (
  SELECT "Customer ID", SUM("Transaction Amount") as paid_amt
  FROM transaction_history_table
  WHERE "Transaction Payment Status"='Paid'
  GROUP BY "Customer ID"
  HAVING SUM("Transaction Amount") > 5000
)
SELECT c."Credit Grade", COUNT(DISTINCT hv."Customer ID") as hv_customers, AVG(c."Credit Score") as avg_score
FROM hv LEFT JOIN customer_account_table a ON hv."Customer ID"=a."Customer ID"
LEFT JOIN customer_credit_rating_table c ON a."Account ID"=c."Account ID"
GROUP BY c."Credit Grade" ORDER BY hv_customers DESC
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-033/attempt-01/sql/S23.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-033/attempt-01/sql/S23.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-033/attempt-01/results/S23.rows.jsonl)；完整：True；SHA256：`92b92e837683870748bf6882119fa091aeb7b2ce00e66cd3cb23ac756eb09500`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "transaction_history_table", "kind": "base", "block": null, "base_tables": ["transaction_history_table"]}] | [] | ["\"Customer ID\""] |
| B2 | [{"alias": "hv", "kind": "derived", "block": "B1", "base_tables": ["transaction_history_table"]}, {"alias": "a", "kind": "base", "block": null, "base_tables": ["customer_account_table"]}, {"alias": "c", "kind": "base", "block": null, "base_tables": ["customer_credit_rating_table"]}] | [{"type": "LEFT", "right": "customer_account_table AS a", "on": "hv.\"Customer ID\" = a.\"Customer ID\"", "using": []}, {"type": "LEFT", "right": "customer_credit_rating_table AS c", "on": "a.\"Account ID\" = c.\"Account ID\"", "using": []}] | ["c.\"Credit Grade\""] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | SUM("Transaction Amount") | [{"table": "transaction_history_table", "column": "Transaction Amount"}] | [] | False |
| B1 | SUM("Transaction Amount") | [{"table": "transaction_history_table", "column": "Transaction Amount"}] | [] | False |
| B2 | COUNT(DISTINCT hv."Customer ID") | [{"table": "transaction_history_table", "column": "Customer ID"}] | [] | False |
| B2 | AVG(c."Credit Score") | [{"table": "customer_credit_rating_table", "column": "Credit Score"}] | [] | False |


## S24

类别 `data`；来源 `query_db`；调用 `c6fb3db8de3249aeb50bdfdc9e3565b0`；状态 `success`。

```sql
WITH hv AS (
  SELECT "Customer ID", SUM("Transaction Amount") as paid_amt
  FROM transaction_history_table
  WHERE "Transaction Payment Status"='Paid'
  GROUP BY "Customer ID"
  HAVING SUM("Transaction Amount") > 5000
)
SELECT s."Segment Name", COUNT(DISTINCT hv."Customer ID") as hv_customers
FROM hv LEFT JOIN customer_segments_table s ON hv."Customer ID"=s."Customer ID"
GROUP BY s."Segment Name" ORDER BY hv_customers DESC
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-033/attempt-01/sql/S24.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-033/attempt-01/sql/S24.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-033/attempt-01/results/S24.rows.jsonl)；完整：True；SHA256：`1542d1efb81ccb0e0cc98b573b3e07c1fb0ffbd4a2f81e673a329e366ca56fb7`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "transaction_history_table", "kind": "base", "block": null, "base_tables": ["transaction_history_table"]}] | [] | ["\"Customer ID\""] |
| B2 | [{"alias": "hv", "kind": "derived", "block": "B1", "base_tables": ["transaction_history_table"]}, {"alias": "s", "kind": "base", "block": null, "base_tables": ["customer_segments_table"]}] | [{"type": "LEFT", "right": "customer_segments_table AS s", "on": "hv.\"Customer ID\" = s.\"Customer ID\"", "using": []}] | ["s.\"Segment Name\""] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | SUM("Transaction Amount") | [{"table": "transaction_history_table", "column": "Transaction Amount"}] | [] | False |
| B1 | SUM("Transaction Amount") | [{"table": "transaction_history_table", "column": "Transaction Amount"}] | [] | False |
| B2 | COUNT(DISTINCT hv."Customer ID") | [{"table": "transaction_history_table", "column": "Customer ID"}] | [] | False |


## S25

类别 `data`；来源 `query_db`；调用 `8933a8919de8400e9c2b4d92877506aa`；状态 `failed`。

```sql
SELECT "Customer ID", LEFT("Customer ID",1) as prefix, LENGTH("Customer ID") as len FROM transaction_history_table GROUP BY prefix, len LIMIT 20
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-033/attempt-01/sql/S25.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-033/attempt-01/sql/S25.parameters.json)。

错误：`OperationalError('no such function: LEFT')`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "transaction_history_table", "kind": "base", "block": null, "base_tables": ["transaction_history_table"]}] | [] | ["LEFT(\"Customer ID\", 1)", "LENGTH(\"Customer ID\")"] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |


## S26

类别 `data`；来源 `query_db`；调用 `3b01a633aea54d9db997014b14ac970e`；状态 `failed`。

```sql
SELECT LEFT("Customer ID",1) as prefix, LENGTH("Customer ID") as len, COUNT(*) as cnt FROM membership_table GROUP BY prefix, len
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-033/attempt-01/sql/S26.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-033/attempt-01/sql/S26.parameters.json)。

错误：`OperationalError('no such function: LEFT')`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "membership_table", "kind": "base", "block": null, "base_tables": ["membership_table"]}] | [] | ["LEFT(\"Customer ID\", 1)", "LENGTH(\"Customer ID\")"] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |


## S27

类别 `data`；来源 `query_db`；调用 `862b0392ade84371b0d7d44d5d310e70`；状态 `failed`。

```sql
SELECT LEFT("Customer ID",1) as prefix, LENGTH("Customer ID") as len, COUNT(*) as cnt FROM customer_tag_table GROUP BY prefix, len
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-033/attempt-01/sql/S27.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-033/attempt-01/sql/S27.parameters.json)。

错误：`OperationalError('no such function: LEFT')`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "customer_tag_table", "kind": "base", "block": null, "base_tables": ["customer_tag_table"]}] | [] | ["LEFT(\"Customer ID\", 1)", "LENGTH(\"Customer ID\")"] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |


## S28

类别 `data`；来源 `query_db`；调用 `98be1cbd8abe4de1b602c7cfbe3fafa6`；状态 `failed`。

```sql
SELECT LEFT("Customer ID",1) as prefix, LENGTH("Customer ID") as len, COUNT(*) as cnt FROM customer_segments_table GROUP BY prefix, len
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-033/attempt-01/sql/S28.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-033/attempt-01/sql/S28.parameters.json)。

错误：`OperationalError('no such function: LEFT')`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "customer_segments_table", "kind": "base", "block": null, "base_tables": ["customer_segments_table"]}] | [] | ["LEFT(\"Customer ID\", 1)", "LENGTH(\"Customer ID\")"] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |


## S29

类别 `data`；来源 `query_db`；调用 `c8e58ceae96649459a578ade794e4ce4`；状态 `success`。

```sql
SELECT SUBSTR("Customer ID",1,1) as prefix, LENGTH("Customer ID") as len, COUNT(*) as cnt FROM transaction_history_table GROUP BY prefix, len
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-033/attempt-01/sql/S29.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-033/attempt-01/sql/S29.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-033/attempt-01/results/S29.rows.jsonl)；完整：True；SHA256：`b43515e0565755690ad718e5d099f99b2bb251d6c8c0d69df405b78cf26077c2`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "transaction_history_table", "kind": "base", "block": null, "base_tables": ["transaction_history_table"]}] | [] | ["SUBSTRING(\"Customer ID\", 1, 1)", "LENGTH(\"Customer ID\")"] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |


## S30

类别 `data`；来源 `query_db`；调用 `d73b1320a9064a88bd4cfc71613b1b39`；状态 `success`。

```sql
SELECT SUBSTR("Customer ID",1,1) as prefix, LENGTH("Customer ID") as len, COUNT(*) as cnt FROM membership_table GROUP BY prefix, len
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-033/attempt-01/sql/S30.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-033/attempt-01/sql/S30.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-033/attempt-01/results/S30.rows.jsonl)；完整：True；SHA256：`9b075b8e23c1ff0907388cef2f52f95eaf6e61628fd6877db41021d9bb86caad`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "membership_table", "kind": "base", "block": null, "base_tables": ["membership_table"]}] | [] | ["SUBSTRING(\"Customer ID\", 1, 1)", "LENGTH(\"Customer ID\")"] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |


## S31

类别 `data`；来源 `query_db`；调用 `6c2862f524ed43f9aa197c464e478f99`；状态 `success`。

```sql
SELECT SUBSTR("Customer ID",1,1) as prefix, LENGTH("Customer ID") as len, COUNT(*) as cnt FROM customer_tag_table GROUP BY prefix, len
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-033/attempt-01/sql/S31.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-033/attempt-01/sql/S31.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-033/attempt-01/results/S31.rows.jsonl)；完整：True；SHA256：`a2fe185362a34a7d38820b1401e9c3785f6aa4ea17609fa2c7291181d29da3d5`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "customer_tag_table", "kind": "base", "block": null, "base_tables": ["customer_tag_table"]}] | [] | ["SUBSTRING(\"Customer ID\", 1, 1)", "LENGTH(\"Customer ID\")"] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |


## S32

类别 `data`；来源 `query_db`；调用 `9aa4b94032594507bfa044b4f963c1d1`；状态 `success`。

```sql
SELECT SUBSTR("Customer ID",1,1) as prefix, LENGTH("Customer ID") as len, COUNT(*) as cnt FROM customer_segments_table GROUP BY prefix, len
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-033/attempt-01/sql/S32.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-033/attempt-01/sql/S32.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-033/attempt-01/results/S32.rows.jsonl)；完整：True；SHA256：`605afd089403284143e45d7c5cc145d36db404b5736aec40b64b9a5ed7af2f70`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "customer_segments_table", "kind": "base", "block": null, "base_tables": ["customer_segments_table"]}] | [] | ["SUBSTRING(\"Customer ID\", 1, 1)", "LENGTH(\"Customer ID\")"] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |


## S33

类别 `data`；来源 `query_db`；调用 `c28eb2b6a2a34aa1a1d244cee58f7737`；状态 `success`。

```sql
SELECT SUBSTR("Customer ID",1,1) as prefix, LENGTH("Customer ID") as len, COUNT(*) as cnt FROM customer_contact_table GROUP BY prefix, len
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-033/attempt-01/sql/S33.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-033/attempt-01/sql/S33.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-033/attempt-01/results/S33.rows.jsonl)；完整：True；SHA256：`85785caed55c77d9f282ef86dedaa57c94a67f64dbc9aafb417f469031a9bbff`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "customer_contact_table", "kind": "base", "block": null, "base_tables": ["customer_contact_table"]}] | [] | ["SUBSTRING(\"Customer ID\", 1, 1)", "LENGTH(\"Customer ID\")"] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |


## S34

类别 `data`；来源 `query_db`；调用 `8d45cdb124234b1ca0cfee9dba1670f0`；状态 `success`。

```sql
SELECT SUBSTR("Customer ID",1,1) as prefix, LENGTH("Customer ID") as len, COUNT(*) as cnt FROM customer_account_table GROUP BY prefix, len
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-033/attempt-01/sql/S34.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-033/attempt-01/sql/S34.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-033/attempt-01/results/S34.rows.jsonl)；完整：True；SHA256：`85785caed55c77d9f282ef86dedaa57c94a67f64dbc9aafb417f469031a9bbff`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "customer_account_table", "kind": "base", "block": null, "base_tables": ["customer_account_table"]}] | [] | ["SUBSTRING(\"Customer ID\", 1, 1)", "LENGTH(\"Customer ID\")"] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |


## S35

类别 `data`；来源 `query_db`；调用 `0bc0b8ecc78f444483ae26db16db537c`；状态 `success`。

```sql
SELECT SUBSTR("Customer ID",1,1) as prefix, LENGTH("Customer ID") as len, COUNT(*) as cnt FROM contracts_table GROUP BY prefix, len
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-033/attempt-01/sql/S35.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-033/attempt-01/sql/S35.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-033/attempt-01/results/S35.rows.jsonl)；完整：True；SHA256：`85785caed55c77d9f282ef86dedaa57c94a67f64dbc9aafb417f469031a9bbff`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "contracts_table", "kind": "base", "block": null, "base_tables": ["contracts_table"]}] | [] | ["SUBSTRING(\"Customer ID\", 1, 1)", "LENGTH(\"Customer ID\")"] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |


## S36

类别 `data`；来源 `query_db`；调用 `fe9feb16540e461aaf74c80adb0f6f86`；状态 `success`。

```sql
SELECT SUBSTR("Customer ID",1,1) as prefix, LENGTH("Customer ID") as len, COUNT(*) as cnt FROM financials_table GROUP BY prefix, len
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-033/attempt-01/sql/S36.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-033/attempt-01/sql/S36.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-033/attempt-01/results/S36.rows.jsonl)；完整：True；SHA256：`85785caed55c77d9f282ef86dedaa57c94a67f64dbc9aafb417f469031a9bbff`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "financials_table", "kind": "base", "block": null, "base_tables": ["financials_table"]}] | [] | ["SUBSTRING(\"Customer ID\", 1, 1)", "LENGTH(\"Customer ID\")"] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |


## S37

类别 `data`；来源 `query_db`；调用 `8ef477825fd141969505c88f55392efd`；状态 `success`。

```sql
SELECT SUBSTR("Customer ID",1,1) as prefix, LENGTH("Customer ID") as len, COUNT(*) as cnt FROM product_service_order_table GROUP BY prefix, len
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-033/attempt-01/sql/S37.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-033/attempt-01/sql/S37.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-033/attempt-01/results/S37.rows.jsonl)；完整：True；SHA256：`a8b98c26fe8de210c8464a59ad295a679bfc47475866092b0e91bd0cb73d7d65`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "product_service_order_table", "kind": "base", "block": null, "base_tables": ["product_service_order_table"]}] | [] | ["SUBSTRING(\"Customer ID\", 1, 1)", "LENGTH(\"Customer ID\")"] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |


## S38

类别 `data`；来源 `query_db`；调用 `0c8b93412fb942b0803f9ef03b7937a2`；状态 `success`。

```sql
SELECT SUBSTR("Customer ID",1,1) as prefix, LENGTH("Customer ID") as len, COUNT(*) as cnt FROM sales_follow_up_table GROUP BY prefix, len
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-033/attempt-01/sql/S38.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-033/attempt-01/sql/S38.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-033/attempt-01/results/S38.rows.jsonl)；完整：True；SHA256：`c2c37bd8f3c821fb5b72f3b4109e05b5f27879c1837732f5f84935f30777cd53`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "sales_follow_up_table", "kind": "base", "block": null, "base_tables": ["sales_follow_up_table"]}] | [] | ["SUBSTRING(\"Customer ID\", 1, 1)", "LENGTH(\"Customer ID\")"] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |


## S39

类别 `data`；来源 `query_db`；调用 `27fdffc7899d4198a5b372f1047050bc`；状态 `success`。

```sql
SELECT cc."Customer ID", cc."Account ID" FROM customer_account_table cc LIMIT 5
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-033/attempt-01/sql/S39.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-033/attempt-01/sql/S39.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-033/attempt-01/results/S39.rows.jsonl)；完整：True；SHA256：`20d10c238582e7d67073dae8db589e7fd427f064ebe5371e0d17a355e3569447`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "cc", "kind": "base", "block": null, "base_tables": ["customer_account_table"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |


## S40

类别 `data`；来源 `query_db`；调用 `bad1e260fef547d1b0ae18c9d5571dd4`；状态 `success`。

```sql
SELECT * FROM customer_credit_rating_table LIMIT 5
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-033/attempt-01/sql/S40.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-033/attempt-01/sql/S40.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-033/attempt-01/results/S40.rows.jsonl)；完整：True；SHA256：`ffe3ca963f351b5da373ea6e78bf5503f2a6cfac6414b5866c6760a223d0764f`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "customer_credit_rating_table", "kind": "base", "block": null, "base_tables": ["customer_credit_rating_table"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |


## S41

类别 `data`；来源 `query_db`；调用 `cbf68c993fd0483bb495cd67af3b5b2b`；状态 `success`。

```sql
SELECT cr."Account ID", a."Customer ID" FROM customer_credit_rating_table cr LEFT JOIN customer_account_table a ON cr."Account ID"=a."Account ID" LIMIT 10
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-033/attempt-01/sql/S41.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-033/attempt-01/sql/S41.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-033/attempt-01/results/S41.rows.jsonl)；完整：True；SHA256：`5717feb3081ddb297579065eba303dd6890937d4cc172eaf2e04aa7c60ea25ef`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "cr", "kind": "base", "block": null, "base_tables": ["customer_credit_rating_table"]}, {"alias": "a", "kind": "base", "block": null, "base_tables": ["customer_account_table"]}] | [{"type": "LEFT", "right": "customer_account_table AS a", "on": "cr.\"Account ID\" = a.\"Account ID\"", "using": []}] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |


## S42

类别 `data`；来源 `query_db`；调用 `f4e7234bd8e647388c3d22a2df57536c`；状态 `success`。

```sql
SELECT COUNT(*) as matched, (SELECT COUNT(*) FROM customer_credit_rating_table) as total FROM customer_credit_rating_table cr JOIN customer_account_table a ON cr."Account ID"=a."Account ID"
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-033/attempt-01/sql/S42.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-033/attempt-01/sql/S42.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-033/attempt-01/results/S42.rows.jsonl)；完整：True；SHA256：`2f10ba9029b122c964aa159b043062503cb785139f595cfe010a80a0017537fd`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "customer_credit_rating_table", "kind": "base", "block": null, "base_tables": ["customer_credit_rating_table"]}] | [] | [] |
| B2 | [{"alias": "cr", "kind": "base", "block": null, "base_tables": ["customer_credit_rating_table"]}, {"alias": "a", "kind": "base", "block": null, "base_tables": ["customer_account_table"]}] | [{"type": "INNER", "right": "customer_account_table AS a", "on": "cr.\"Account ID\" = a.\"Account ID\"", "using": []}] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |
| B2 | COUNT(*) | [] | [] | True |


## S43

类别 `data`；来源 `query_db`；调用 `ea3e0086df3c4116a2094612375f7745`；状态 `success`。

```sql
SELECT SUBSTR("Account ID",1,1) as prefix, LENGTH("Account ID") as len, COUNT(*) as cnt FROM customer_credit_rating_table GROUP BY prefix, len
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-033/attempt-01/sql/S43.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-033/attempt-01/sql/S43.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-033/attempt-01/results/S43.rows.jsonl)；完整：True；SHA256：`080c7519c2d615cf12cb6552ccf94bd278891d7c7a1687e940789e6af6439af8`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "customer_credit_rating_table", "kind": "base", "block": null, "base_tables": ["customer_credit_rating_table"]}] | [] | ["SUBSTRING(\"Account ID\", 1, 1)", "LENGTH(\"Account ID\")"] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |


## S44

类别 `data`；来源 `query_db`；调用 `caf28c07e4fa408f8c3b466e68d4be7f`；状态 `success`。

```sql
SELECT SUBSTR("Account ID",1,1) as prefix, LENGTH("Account ID") as len, COUNT(*) as cnt FROM customer_account_table GROUP BY prefix, len
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-033/attempt-01/sql/S44.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-033/attempt-01/sql/S44.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-033/attempt-01/results/S44.rows.jsonl)；完整：True；SHA256：`080c7519c2d615cf12cb6552ccf94bd278891d7c7a1687e940789e6af6439af8`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "customer_account_table", "kind": "base", "block": null, "base_tables": ["customer_account_table"]}] | [] | ["SUBSTRING(\"Account ID\", 1, 1)", "LENGTH(\"Account ID\")"] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |


## S45

类别 `data`；来源 `query_db`；调用 `9f39c79ab0954f539dbafc44b9002664`；状态 `success`。

```sql
SELECT SUBSTR("Account ID",1,1) as prefix, LENGTH("Account ID") as len, COUNT(*) as cnt FROM transaction_history_table GROUP BY prefix, len
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-033/attempt-01/sql/S45.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-033/attempt-01/sql/S45.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-033/attempt-01/results/S45.rows.jsonl)；完整：True；SHA256：`e164cdabed0d7ffca0bdb4de63d328fc173a625e64e9a108e8bd988736f9e9ca`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "transaction_history_table", "kind": "base", "block": null, "base_tables": ["transaction_history_table"]}] | [] | ["SUBSTRING(\"Account ID\", 1, 1)", "LENGTH(\"Account ID\")"] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |


## S46

类别 `data`；来源 `query_db`；调用 `83a0307bf1994298aeb662086a957743`；状态 `success`。

```sql
WITH hv AS (
  SELECT DISTINCT "Customer ID" FROM transaction_history_table
  WHERE "Transaction Payment Status"='Paid'
  GROUP BY "Customer ID"
  HAVING SUM("Transaction Amount") > 5000
)
SELECT 
  (SELECT COUNT(*) FROM hv) as total_hv,
  (SELECT COUNT(*) FROM hv WHERE "Customer ID" IN (SELECT "Customer ID" FROM membership_table)) as in_membership,
  (SELECT COUNT(*) FROM hv WHERE "Customer ID" IN (SELECT "Customer ID" FROM customer_tag_table)) as in_tags,
  (SELECT COUNT(*) FROM hv WHERE "Customer ID" IN (SELECT "Customer ID" FROM customer_contact_table)) as in_contact,
  (SELECT COUNT(*) FROM hv WHERE "Customer ID" IN (SELECT "Customer ID" FROM contracts_table)) as in_contracts,
  (SELECT COUNT(*) FROM hv WHERE "Customer ID" IN (SELECT "Customer ID" FROM financials_table)) as in_financials,
  (SELECT COUNT(*) FROM hv WHERE "Customer ID" IN (SELECT "Customer ID" FROM product_service_order_table)) as in_orders,
  (SELECT COUNT(*) FROM hv WHERE "Customer ID" IN (SELECT "Customer ID" FROM customer_account_table)) as in_accounts,
  (SELECT COUNT(*) FROM hv WHERE "Customer ID" IN (SELECT "Customer ID" FROM sales_follow_up_table)) as in_followup
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-033/attempt-01/sql/S46.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-033/attempt-01/sql/S46.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-033/attempt-01/results/S46.rows.jsonl)；完整：True；SHA256：`f2e56a18ad5b0892ede8252f44e2b2d3189180173b39c3fc011529179e403635`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "transaction_history_table", "kind": "base", "block": null, "base_tables": ["transaction_history_table"]}] | [] | ["\"Customer ID\""] |
| B2 | [{"alias": "hv", "kind": "derived", "block": "B1", "base_tables": ["transaction_history_table"]}] | [] | [] |
| B3 | [{"alias": "membership_table", "kind": "base", "block": null, "base_tables": ["membership_table"]}] | [] | [] |
| B4 | [{"alias": "hv", "kind": "derived", "block": "B1", "base_tables": ["transaction_history_table"]}] | [] | [] |
| B5 | [{"alias": "customer_tag_table", "kind": "base", "block": null, "base_tables": ["customer_tag_table"]}] | [] | [] |
| B6 | [{"alias": "hv", "kind": "derived", "block": "B1", "base_tables": ["transaction_history_table"]}] | [] | [] |
| B7 | [{"alias": "customer_contact_table", "kind": "base", "block": null, "base_tables": ["customer_contact_table"]}] | [] | [] |
| B8 | [{"alias": "hv", "kind": "derived", "block": "B1", "base_tables": ["transaction_history_table"]}] | [] | [] |
| B9 | [{"alias": "contracts_table", "kind": "base", "block": null, "base_tables": ["contracts_table"]}] | [] | [] |
| B10 | [{"alias": "hv", "kind": "derived", "block": "B1", "base_tables": ["transaction_history_table"]}] | [] | [] |
| B11 | [{"alias": "financials_table", "kind": "base", "block": null, "base_tables": ["financials_table"]}] | [] | [] |
| B12 | [{"alias": "hv", "kind": "derived", "block": "B1", "base_tables": ["transaction_history_table"]}] | [] | [] |
| B13 | [{"alias": "product_service_order_table", "kind": "base", "block": null, "base_tables": ["product_service_order_table"]}] | [] | [] |
| B14 | [{"alias": "hv", "kind": "derived", "block": "B1", "base_tables": ["transaction_history_table"]}] | [] | [] |
| B15 | [{"alias": "customer_account_table", "kind": "base", "block": null, "base_tables": ["customer_account_table"]}] | [] | [] |
| B16 | [{"alias": "hv", "kind": "derived", "block": "B1", "base_tables": ["transaction_history_table"]}] | [] | [] |
| B17 | [{"alias": "sales_follow_up_table", "kind": "base", "block": null, "base_tables": ["sales_follow_up_table"]}] | [] | [] |
| B18 | [{"alias": "hv", "kind": "derived", "block": "B1", "base_tables": ["transaction_history_table"]}] | [] | [] |
| B19 | [] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | SUM("Transaction Amount") | [{"table": "transaction_history_table", "column": "Transaction Amount"}] | [] | False |
| B2 | COUNT(*) | [] | [] | True |
| B4 | COUNT(*) | [] | [] | True |
| B6 | COUNT(*) | [] | [] | True |
| B8 | COUNT(*) | [] | [] | True |
| B10 | COUNT(*) | [] | [] | True |
| B12 | COUNT(*) | [] | [] | True |
| B14 | COUNT(*) | [] | [] | True |
| B16 | COUNT(*) | [] | [] | True |
| B18 | COUNT(*) | [] | [] | True |


未解析列血缘：[{"block": "B19", "column": "\"Customer ID\"", "reason": "ambiguous_or_missing_source"}, {"block": "B19", "column": "\"Customer ID\"", "reason": "ambiguous_or_missing_source"}, {"block": "B19", "column": "\"Customer ID\"", "reason": "ambiguous_or_missing_source"}, {"block": "B19", "column": "\"Customer ID\"", "reason": "ambiguous_or_missing_source"}, {"block": "B19", "column": "\"Customer ID\"", "reason": "ambiguous_or_missing_source"}, {"block": "B19", "column": "\"Customer ID\"", "reason": "ambiguous_or_missing_source"}, {"block": "B19", "column": "\"Customer ID\"", "reason": "ambiguous_or_missing_source"}, {"block": "B19", "column": "\"Customer ID\"", "reason": "ambiguous_or_missing_source"}, {"block": "B19", "column": "\"Customer ID\"", "reason": "ambiguous_or_missing_source"}, {"block": "B19", "column": "\"Customer ID\"", "reason": "ambiguous_or_missing_source"}, {"block": "B19", "column": "\"Customer ID\"", "reason": "ambiguous_or_missing_source"}, {"block": "B19", "column": "\"Customer ID\"", "reason": "ambiguous_or_missing_source"}, {"block": "B19", "column": "\"Customer ID\"", "reason": "ambiguous_or_missing_source"}, {"block": "B19", "column": "\"Customer ID\"", "reason": "ambiguous_or_missing_source"}, {"block": "B19", "column": "\"Customer ID\"", "reason": "ambiguous_or_missing_source"}, {"block": "B19", "column": "\"Customer ID\"", "reason": "ambiguous_or_missing_source"}]

## S47

类别 `data`；来源 `query_db`；调用 `dabaa39b7bea45e7b97e8d83a4d80fbd`；状态 `success`。

```sql
WITH hv AS (
  SELECT DISTINCT "Customer ID" FROM transaction_history_table
  WHERE "Transaction Payment Status"='Paid'
  GROUP BY "Customer ID"
  HAVING SUM("Transaction Amount") > 5000
)
SELECT m."Membership Level", COUNT(*) as cnt
FROM hv JOIN membership_table m ON hv."Customer ID"=m."Customer ID"
GROUP BY m."Membership Level" ORDER BY cnt DESC
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-033/attempt-01/sql/S47.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-033/attempt-01/sql/S47.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-033/attempt-01/results/S47.rows.jsonl)；完整：True；SHA256：`bd027af92d6b1175562089508c85825202703f1fff0401903e7639fa872e5039`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "transaction_history_table", "kind": "base", "block": null, "base_tables": ["transaction_history_table"]}] | [] | ["\"Customer ID\""] |
| B2 | [{"alias": "hv", "kind": "derived", "block": "B1", "base_tables": ["transaction_history_table"]}, {"alias": "m", "kind": "base", "block": null, "base_tables": ["membership_table"]}] | [{"type": "INNER", "right": "membership_table AS m", "on": "hv.\"Customer ID\" = m.\"Customer ID\"", "using": []}] | ["m.\"Membership Level\""] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | SUM("Transaction Amount") | [{"table": "transaction_history_table", "column": "Transaction Amount"}] | [] | False |
| B2 | COUNT(*) | [] | [] | True |


## S48

类别 `data`；来源 `query_db`；调用 `8ae9b7335de94c40a4823e3356b34ef2`；状态 `success`。

```sql
WITH hv AS (
  SELECT DISTINCT "Customer ID" FROM transaction_history_table
  WHERE "Transaction Payment Status"='Paid'
  GROUP BY "Customer ID"
  HAVING SUM("Transaction Amount") > 5000
)
SELECT m."Member Status", COUNT(*) as cnt
FROM hv JOIN membership_table m ON hv."Customer ID"=m."Customer ID"
GROUP BY m."Member Status" ORDER BY cnt DESC
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-033/attempt-01/sql/S48.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-033/attempt-01/sql/S48.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-033/attempt-01/results/S48.rows.jsonl)；完整：True；SHA256：`a60c9d58623a45291a1b100d7d51575369df58a0c6346227e257232b3ee05c30`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "transaction_history_table", "kind": "base", "block": null, "base_tables": ["transaction_history_table"]}] | [] | ["\"Customer ID\""] |
| B2 | [{"alias": "hv", "kind": "derived", "block": "B1", "base_tables": ["transaction_history_table"]}, {"alias": "m", "kind": "base", "block": null, "base_tables": ["membership_table"]}] | [{"type": "INNER", "right": "membership_table AS m", "on": "hv.\"Customer ID\" = m.\"Customer ID\"", "using": []}] | ["m.\"Member Status\""] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | SUM("Transaction Amount") | [{"table": "transaction_history_table", "column": "Transaction Amount"}] | [] | False |
| B2 | COUNT(*) | [] | [] | True |


## S49

类别 `data`；来源 `query_db`；调用 `5ddc15b4f4a546779440e7cec18aa956`；状态 `success`。

```sql
WITH hv AS (
  SELECT DISTINCT "Customer ID" FROM transaction_history_table
  WHERE "Transaction Payment Status"='Paid'
  GROUP BY "Customer ID"
  HAVING SUM("Transaction Amount") > 5000
)
SELECT m."Privilege Level", COUNT(*) as cnt
FROM hv JOIN membership_table m ON hv."Customer ID"=m."Customer ID"
GROUP BY m."Privilege Level" ORDER BY cnt DESC
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-033/attempt-01/sql/S49.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-033/attempt-01/sql/S49.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-033/attempt-01/results/S49.rows.jsonl)；完整：True；SHA256：`cddc9b976cbb79f1d8b40d38598906e99a682550bd2c1f66c9794af64b1acc18`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "transaction_history_table", "kind": "base", "block": null, "base_tables": ["transaction_history_table"]}] | [] | ["\"Customer ID\""] |
| B2 | [{"alias": "hv", "kind": "derived", "block": "B1", "base_tables": ["transaction_history_table"]}, {"alias": "m", "kind": "base", "block": null, "base_tables": ["membership_table"]}] | [{"type": "INNER", "right": "membership_table AS m", "on": "hv.\"Customer ID\" = m.\"Customer ID\"", "using": []}] | ["m.\"Privilege Level\""] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | SUM("Transaction Amount") | [{"table": "transaction_history_table", "column": "Transaction Amount"}] | [] | False |
| B2 | COUNT(*) | [] | [] | True |


## S50

类别 `data`；来源 `query_db`；调用 `280928169eb740a7a16ad928aaec930b`；状态 `success`。

```sql
WITH hv AS (
  SELECT DISTINCT "Customer ID" FROM transaction_history_table
  WHERE "Transaction Payment Status"='Paid'
  GROUP BY "Customer ID"
  HAVING SUM("Transaction Amount") > 5000
)
SELECT m."Automatic Renewal", COUNT(*) as cnt
FROM hv JOIN membership_table m ON hv."Customer ID"=m."Customer ID"
GROUP BY m."Automatic Renewal" ORDER BY cnt DESC
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-033/attempt-01/sql/S50.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-033/attempt-01/sql/S50.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-033/attempt-01/results/S50.rows.jsonl)；完整：True；SHA256：`55019175c0d6061adb9d5381e2a534198c6f79fb14aa4b5a884c0de50858ffa3`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "transaction_history_table", "kind": "base", "block": null, "base_tables": ["transaction_history_table"]}] | [] | ["\"Customer ID\""] |
| B2 | [{"alias": "hv", "kind": "derived", "block": "B1", "base_tables": ["transaction_history_table"]}, {"alias": "m", "kind": "base", "block": null, "base_tables": ["membership_table"]}] | [{"type": "INNER", "right": "membership_table AS m", "on": "hv.\"Customer ID\" = m.\"Customer ID\"", "using": []}] | ["m.\"Automatic Renewal\""] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | SUM("Transaction Amount") | [{"table": "transaction_history_table", "column": "Transaction Amount"}] | [] | False |
| B2 | COUNT(*) | [] | [] | True |


## S51

类别 `data`；来源 `query_db`；调用 `ca190a11cb2c410c96c6490e25ba3f20`；状态 `success`。

```sql
WITH hv AS (
  SELECT DISTINCT "Customer ID" FROM transaction_history_table
  WHERE "Transaction Payment Status"='Paid'
  GROUP BY "Customer ID"
  HAVING SUM("Transaction Amount") > 5000
)
SELECT t."Tag Name", COUNT(*) as cnt, AVG(t."Tag Weight Value") as avg_weight
FROM hv JOIN customer_tag_table t ON hv."Customer ID"=t."Customer ID"
GROUP BY t."Tag Name" ORDER BY cnt DESC
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-033/attempt-01/sql/S51.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-033/attempt-01/sql/S51.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-033/attempt-01/results/S51.rows.jsonl)；完整：True；SHA256：`81e9ed7918c920a77be3bcf6836c7335e89ee2a40914bfbaaee58829d08afbb0`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "transaction_history_table", "kind": "base", "block": null, "base_tables": ["transaction_history_table"]}] | [] | ["\"Customer ID\""] |
| B2 | [{"alias": "hv", "kind": "derived", "block": "B1", "base_tables": ["transaction_history_table"]}, {"alias": "t", "kind": "base", "block": null, "base_tables": ["customer_tag_table"]}] | [{"type": "INNER", "right": "customer_tag_table AS t", "on": "hv.\"Customer ID\" = t.\"Customer ID\"", "using": []}] | ["t.\"Tag Name\""] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | SUM("Transaction Amount") | [{"table": "transaction_history_table", "column": "Transaction Amount"}] | [] | False |
| B2 | COUNT(*) | [] | [] | True |
| B2 | AVG(t."Tag Weight Value") | [{"table": "customer_tag_table", "column": "Tag Weight Value"}] | [] | False |


## S52

类别 `data`；来源 `query_db`；调用 `54ac40c511054cae8b2085de662e066c`；状态 `success`。

```sql
WITH hv AS (
  SELECT DISTINCT "Customer ID" FROM transaction_history_table
  WHERE "Transaction Payment Status"='Paid'
  GROUP BY "Customer ID"
  HAVING SUM("Transaction Amount") > 5000
)
SELECT c."Gender", COUNT(*) as cnt
FROM hv JOIN customer_contact_table c ON hv."Customer ID"=c."Customer ID"
GROUP BY c."Gender"
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-033/attempt-01/sql/S52.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-033/attempt-01/sql/S52.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-033/attempt-01/results/S52.rows.jsonl)；完整：True；SHA256：`3921aecb2194538a327d817e8b2e9156f93bfb51313c513767e53f3ea25057d2`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "transaction_history_table", "kind": "base", "block": null, "base_tables": ["transaction_history_table"]}] | [] | ["\"Customer ID\""] |
| B2 | [{"alias": "hv", "kind": "derived", "block": "B1", "base_tables": ["transaction_history_table"]}, {"alias": "c", "kind": "base", "block": null, "base_tables": ["customer_contact_table"]}] | [{"type": "INNER", "right": "customer_contact_table AS c", "on": "hv.\"Customer ID\" = c.\"Customer ID\"", "using": []}] | ["c.\"Gender\""] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | SUM("Transaction Amount") | [{"table": "transaction_history_table", "column": "Transaction Amount"}] | [] | False |
| B2 | COUNT(*) | [] | [] | True |


## S53

类别 `data`；来源 `query_db`；调用 `a6489c8a716a47f38816a2d6ecb43d15`；状态 `success`。

```sql
WITH hv AS (
  SELECT DISTINCT "Customer ID" FROM transaction_history_table
  WHERE "Transaction Payment Status"='Paid'
  GROUP BY "Customer ID"
  HAVING SUM("Transaction Amount") > 5000
)
SELECT ct."Contract Type", COUNT(*) as cnt
FROM hv JOIN contracts_table ct ON hv."Customer ID"=ct."Customer ID"
GROUP BY ct."Contract Type" ORDER BY cnt DESC
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-033/attempt-01/sql/S53.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-033/attempt-01/sql/S53.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-033/attempt-01/results/S53.rows.jsonl)；完整：True；SHA256：`28cf12827f2afcefe165c532b16f572022a2fa3c4512bfc5a5cd946c37b5a22a`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "transaction_history_table", "kind": "base", "block": null, "base_tables": ["transaction_history_table"]}] | [] | ["\"Customer ID\""] |
| B2 | [{"alias": "hv", "kind": "derived", "block": "B1", "base_tables": ["transaction_history_table"]}, {"alias": "ct", "kind": "base", "block": null, "base_tables": ["contracts_table"]}] | [{"type": "INNER", "right": "contracts_table AS ct", "on": "hv.\"Customer ID\" = ct.\"Customer ID\"", "using": []}] | ["ct.\"Contract Type\""] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | SUM("Transaction Amount") | [{"table": "transaction_history_table", "column": "Transaction Amount"}] | [] | False |
| B2 | COUNT(*) | [] | [] | True |


## S54

类别 `data`；来源 `query_db`；调用 `531cd071b08a476a99649a3580e45b7f`；状态 `success`。

```sql
WITH hv AS (
  SELECT DISTINCT "Customer ID" FROM transaction_history_table
  WHERE "Transaction Payment Status"='Paid'
  GROUP BY "Customer ID"
  HAVING SUM("Transaction Amount") > 5000
)
SELECT cr."Credit Grade", COUNT(*) as cnt, AVG(cr."Credit Score") as avg_score, AVG(cr."Credit Limit") as avg_limit
FROM hv 
JOIN customer_account_table a ON hv."Customer ID"=a."Customer ID"
JOIN customer_credit_rating_table cr ON a."Account ID"=cr."Account ID"
GROUP BY cr."Credit Grade" ORDER BY cnt DESC
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-033/attempt-01/sql/S54.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-033/attempt-01/sql/S54.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-033/attempt-01/results/S54.rows.jsonl)；完整：True；SHA256：`8337d80493b41191fddde278207da3ca97f819e0fb82acf3974a644a69d3e382`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "transaction_history_table", "kind": "base", "block": null, "base_tables": ["transaction_history_table"]}] | [] | ["\"Customer ID\""] |
| B2 | [{"alias": "hv", "kind": "derived", "block": "B1", "base_tables": ["transaction_history_table"]}, {"alias": "a", "kind": "base", "block": null, "base_tables": ["customer_account_table"]}, {"alias": "cr", "kind": "base", "block": null, "base_tables": ["customer_credit_rating_table"]}] | [{"type": "INNER", "right": "customer_account_table AS a", "on": "hv.\"Customer ID\" = a.\"Customer ID\"", "using": []}, {"type": "INNER", "right": "customer_credit_rating_table AS cr", "on": "a.\"Account ID\" = cr.\"Account ID\"", "using": []}] | ["cr.\"Credit Grade\""] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | SUM("Transaction Amount") | [{"table": "transaction_history_table", "column": "Transaction Amount"}] | [] | False |
| B2 | COUNT(*) | [] | [] | True |
| B2 | AVG(cr."Credit Score") | [{"table": "customer_credit_rating_table", "column": "Credit Score"}] | [] | False |
| B2 | AVG(cr."Credit Limit") | [{"table": "customer_credit_rating_table", "column": "Credit Limit"}] | [] | False |


## S55

类别 `data`；来源 `query_db`；调用 `7c3b4d3842b34fad8b577c1b67ee7f9c`；状态 `success`。

```sql
WITH hv AS (
  SELECT DISTINCT "Customer ID" FROM transaction_history_table
  WHERE "Transaction Payment Status"='Paid'
  GROUP BY "Customer ID"
  HAVING SUM("Transaction Amount") > 5000
)
SELECT t."Transaction Payment Method", COUNT(*) as tx_count, SUM(t."Transaction Amount") as total_amt
FROM hv JOIN transaction_history_table t ON hv."Customer ID"=t."Customer ID" AND t."Transaction Payment Status"='Paid'
GROUP BY t."Transaction Payment Method" ORDER BY total_amt DESC
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-033/attempt-01/sql/S55.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-033/attempt-01/sql/S55.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-033/attempt-01/results/S55.rows.jsonl)；完整：True；SHA256：`c5f8faed54bb92fc8c9e0177354cf67abc67ac2df6735c5326350eb68709a3ce`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "transaction_history_table", "kind": "base", "block": null, "base_tables": ["transaction_history_table"]}] | [] | ["\"Customer ID\""] |
| B2 | [{"alias": "hv", "kind": "derived", "block": "B1", "base_tables": ["transaction_history_table"]}, {"alias": "t", "kind": "base", "block": null, "base_tables": ["transaction_history_table"]}] | [{"type": "INNER", "right": "transaction_history_table AS t", "on": "hv.\"Customer ID\" = t.\"Customer ID\" AND t.\"Transaction Payment Status\" = 'Paid'", "using": []}] | ["t.\"Transaction Payment Method\""] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | SUM("Transaction Amount") | [{"table": "transaction_history_table", "column": "Transaction Amount"}] | [] | False |
| B2 | COUNT(*) | [] | [] | True |
| B2 | SUM(t."Transaction Amount") | [{"table": "transaction_history_table", "column": "Transaction Amount"}] | [] | False |


## S56

类别 `data`；来源 `query_db`；调用 `d14cda9c7cce41c998662c332282efbc`；状态 `success`。

```sql
WITH hv AS (
  SELECT "Customer ID", SUM("Transaction Amount") as paid_amt, COUNT(*) as n_tx
  FROM transaction_history_table
  WHERE "Transaction Payment Status"='Paid'
  GROUP BY "Customer ID"
  HAVING SUM("Transaction Amount") > 5000
)
SELECT 
  MIN(paid_amt) as min_amt, 
  MAX(paid_amt) as max_amt, 
  AVG(paid_amt) as avg_amt,
  SUM(paid_amt) as total_amt,
  COUNT(*) as n_customers,
  AVG(n_tx) as avg_tx_count
FROM hv
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-033/attempt-01/sql/S56.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-033/attempt-01/sql/S56.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-033/attempt-01/results/S56.rows.jsonl)；完整：True；SHA256：`c40c2152a268aa5694ec27f0f61b9def802415bdd7238383f40d0723bed93e5c`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "transaction_history_table", "kind": "base", "block": null, "base_tables": ["transaction_history_table"]}] | [] | ["\"Customer ID\""] |
| B2 | [{"alias": "hv", "kind": "derived", "block": "B1", "base_tables": ["transaction_history_table"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | SUM("Transaction Amount") | [{"table": "transaction_history_table", "column": "Transaction Amount"}] | [] | False |
| B1 | COUNT(*) | [] | [] | True |
| B1 | SUM("Transaction Amount") | [{"table": "transaction_history_table", "column": "Transaction Amount"}] | [] | False |
| B2 | MIN(paid_amt) | [{"table": "transaction_history_table", "column": "Transaction Amount"}] | [] | False |
| B2 | MAX(paid_amt) | [{"table": "transaction_history_table", "column": "Transaction Amount"}] | [] | False |
| B2 | AVG(paid_amt) | [{"table": "transaction_history_table", "column": "Transaction Amount"}] | [] | False |
| B2 | SUM(paid_amt) | [{"table": "transaction_history_table", "column": "Transaction Amount"}] | [] | False |
| B2 | COUNT(*) | [] | [] | True |
| B2 | AVG(n_tx) | [] | [] | False |


## S57

类别 `data`；来源 `query_db`；调用 `bba99d4330eb4171a7a95c8f6bb5120e`；状态 `success`。

```sql
SELECT n_tx, COUNT(*) as n_customers FROM (SELECT "Customer ID", COUNT(*) as n_tx FROM transaction_history_table GROUP BY "Customer ID") GROUP BY n_tx ORDER BY n_tx
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-033/attempt-01/sql/S57.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-033/attempt-01/sql/S57.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-033/attempt-01/results/S57.rows.jsonl)；完整：True；SHA256：`756f541edebe82527d1221fe81462ac08788d0dbb023e7963882adc0615260d5`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "transaction_history_table", "kind": "base", "block": null, "base_tables": ["transaction_history_table"]}] | [] | ["\"Customer ID\""] |
| B2 | [{"alias": "", "kind": "derived", "block": "B1", "base_tables": ["transaction_history_table"]}] | [] | ["n_tx"] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |
| B2 | COUNT(*) | [] | [] | True |


## S58

类别 `data`；来源 `query_db`；调用 `d784891b37ec45438390b5004c21f7a3`；状态 `success`。

```sql
WITH hv AS (
  SELECT "Customer ID", SUM(CASE WHEN "Transaction Payment Status"='Paid' THEN "Transaction Amount" ELSE 0 END) as paid_amt,
         COUNT(*) as all_tx, SUM("Transaction Amount") as total_amt_all
  FROM transaction_history_table
  GROUP BY "Customer ID"
  HAVING SUM(CASE WHEN "Transaction Payment Status"='Paid' THEN "Transaction Amount" ELSE 0 END) > 5000
)
SELECT COUNT(*) as hv_customers, SUM(all_tx) as total_tx, SUM(CASE WHEN all_tx>1 THEN 1 ELSE 0 END) as multi_tx_cust, AVG(total_amt_all) as avg_total_amt FROM hv
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-033/attempt-01/sql/S58.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-033/attempt-01/sql/S58.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-033/attempt-01/results/S58.rows.jsonl)；完整：True；SHA256：`dc93c55dd995c2c863569f2aca464d02a705d5dd3227b7bdad513ef7a9db624e`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "transaction_history_table", "kind": "base", "block": null, "base_tables": ["transaction_history_table"]}] | [] | ["\"Customer ID\""] |
| B2 | [{"alias": "hv", "kind": "derived", "block": "B1", "base_tables": ["transaction_history_table"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | SUM(CASE WHEN "Transaction Payment Status" = 'Paid' THEN "Transaction Amount" ELSE 0 END) | [{"table": "transaction_history_table", "column": "Transaction Amount"}] | [{"table": "transaction_history_table", "column": "Transaction Payment Status"}] | False |
| B1 | COUNT(*) | [] | [] | True |
| B1 | SUM("Transaction Amount") | [{"table": "transaction_history_table", "column": "Transaction Amount"}] | [] | False |
| B1 | SUM(CASE WHEN "Transaction Payment Status" = 'Paid' THEN "Transaction Amount" ELSE 0 END) | [{"table": "transaction_history_table", "column": "Transaction Amount"}] | [{"table": "transaction_history_table", "column": "Transaction Payment Status"}] | False |
| B2 | COUNT(*) | [] | [] | True |
| B2 | SUM(all_tx) | [] | [] | False |
| B2 | SUM(CASE WHEN all_tx > 1 THEN 1 ELSE 0 END) | [] | [] | False |
| B2 | AVG(total_amt_all) | [{"table": "transaction_history_table", "column": "Transaction Amount"}] | [] | False |


## S59

类别 `data`；来源 `query_db`；调用 `13edde34c3c442ebaed681001e41eafe`；状态 `success`。

```sql
SELECT "Transaction Payment Status", COUNT(*) as cnt, SUM("Transaction Amount") as amt FROM transaction_history_table GROUP BY "Transaction Payment Status"
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-033/attempt-01/sql/S59.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-033/attempt-01/sql/S59.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-033/attempt-01/results/S59.rows.jsonl)；完整：True；SHA256：`17726611942e5209e9536fb6b276733cf61d1e6a221180906a2bdc7a7a1af0a7`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "transaction_history_table", "kind": "base", "block": null, "base_tables": ["transaction_history_table"]}] | [] | ["\"Transaction Payment Status\""] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |
| B1 | SUM("Transaction Amount") | [{"table": "transaction_history_table", "column": "Transaction Amount"}] | [] | False |


## S60

类别 `data`；来源 `query_db`；调用 `12a1c663e911431da0a38c35738e78fe`；状态 `success`。

```sql
WITH hv AS (
  SELECT DISTINCT "Customer ID" FROM transaction_history_table
  WHERE "Transaction Payment Status"='Paid'
  GROUP BY "Customer ID"
  HAVING SUM("Transaction Amount") > 5000
)
SELECT f."Outstanding Amount" as outstanding, COUNT(*) as cnt, AVG(f."Outstanding Amount") as avg_out, AVG(f."Amount Received") as avg_recv, AVG(f."Receivable Amount") as avg_recvbl
FROM hv JOIN financials_table f ON hv."Customer ID"=f."Customer ID"
GROUP BY f."Outstanding Amount" ORDER BY cnt DESC
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-033/attempt-01/sql/S60.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-033/attempt-01/sql/S60.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-033/attempt-01/results/S60.rows.jsonl)；完整：True；SHA256：`fb368a915dc2f9986748988ccb434a5e8d736bb28308c933dbc54d1432ac7702`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "transaction_history_table", "kind": "base", "block": null, "base_tables": ["transaction_history_table"]}] | [] | ["\"Customer ID\""] |
| B2 | [{"alias": "hv", "kind": "derived", "block": "B1", "base_tables": ["transaction_history_table"]}, {"alias": "f", "kind": "base", "block": null, "base_tables": ["financials_table"]}] | [{"type": "INNER", "right": "financials_table AS f", "on": "hv.\"Customer ID\" = f.\"Customer ID\"", "using": []}] | ["f.\"Outstanding Amount\""] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | SUM("Transaction Amount") | [{"table": "transaction_history_table", "column": "Transaction Amount"}] | [] | False |
| B2 | COUNT(*) | [] | [] | True |
| B2 | AVG(f."Outstanding Amount") | [{"table": "financials_table", "column": "Outstanding Amount"}] | [] | False |
| B2 | AVG(f."Amount Received") | [{"table": "financials_table", "column": "Amount Received"}] | [] | False |
| B2 | AVG(f."Receivable Amount") | [{"table": "financials_table", "column": "Receivable Amount"}] | [] | False |


## S61

类别 `data`；来源 `query_db`；调用 `ab6252e607534a6db36802b04a332c9e`；状态 `success`。

```sql
WITH hv AS (
  SELECT DISTINCT "Customer ID" FROM transaction_history_table
  WHERE "Transaction Payment Status"='Paid'
  GROUP BY "Customer ID"
  HAVING SUM("Transaction Amount") > 5000
)
SELECT po."Subscribed Product Name", COUNT(*) as cnt, SUM(po."Total Amount") as tot_amt
FROM hv JOIN product_service_order_table po ON hv."Customer ID"=po."Customer ID"
GROUP BY po."Subscribed Product Name" ORDER BY cnt DESC LIMIT 15
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-033/attempt-01/sql/S61.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-033/attempt-01/sql/S61.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-033/attempt-01/results/S61.rows.jsonl)；完整：True；SHA256：`10d67f1599ec418a1d1b24736eec05877891c40417579d5931f07f6e51a041a9`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "transaction_history_table", "kind": "base", "block": null, "base_tables": ["transaction_history_table"]}] | [] | ["\"Customer ID\""] |
| B2 | [{"alias": "hv", "kind": "derived", "block": "B1", "base_tables": ["transaction_history_table"]}, {"alias": "po", "kind": "base", "block": null, "base_tables": ["product_service_order_table"]}] | [{"type": "INNER", "right": "product_service_order_table AS po", "on": "hv.\"Customer ID\" = po.\"Customer ID\"", "using": []}] | ["po.\"Subscribed Product Name\""] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | SUM("Transaction Amount") | [{"table": "transaction_history_table", "column": "Transaction Amount"}] | [] | False |
| B2 | COUNT(*) | [] | [] | True |
| B2 | SUM(po."Total Amount") | [{"table": "product_service_order_table", "column": "Total Amount"}] | [] | False |


## S62

类别 `data`；来源 `query_db`；调用 `3616b4bab74a4ec695de54014ed53188`；状态 `success`。

```sql
WITH hv AS (
  SELECT DISTINCT "Customer ID" FROM transaction_history_table
  WHERE "Transaction Payment Status"='Paid'
  GROUP BY "Customer ID"
  HAVING SUM("Transaction Amount") > 5000
)
SELECT cs."Channel Name", COUNT(*) as cnt
FROM hv JOIN channel_source_table cs ON hv."Customer ID"=cs."Customer ID"
GROUP BY cs."Channel Name" ORDER BY cnt DESC LIMIT 15
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-033/attempt-01/sql/S62.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-033/attempt-01/sql/S62.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-033/attempt-01/results/S62.rows.jsonl)；完整：True；SHA256：`8e6bbc78a1cab6b4e900537d621110104313d9ef2a12e7898f6f7f00fc05eb00`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "transaction_history_table", "kind": "base", "block": null, "base_tables": ["transaction_history_table"]}] | [] | ["\"Customer ID\""] |
| B2 | [{"alias": "hv", "kind": "derived", "block": "B1", "base_tables": ["transaction_history_table"]}, {"alias": "cs", "kind": "base", "block": null, "base_tables": ["channel_source_table"]}] | [{"type": "INNER", "right": "channel_source_table AS cs", "on": "hv.\"Customer ID\" = cs.\"Customer ID\"", "using": []}] | ["cs.\"Channel Name\""] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | SUM("Transaction Amount") | [{"table": "transaction_history_table", "column": "Transaction Amount"}] | [] | False |
| B2 | COUNT(*) | [] | [] | True |


## S63

类别 `data`；来源 `query_db`；调用 `cc59f86b3d444708830b33690250802c`；状态 `success`。

```sql
WITH hv AS (
  SELECT DISTINCT "Customer ID" FROM transaction_history_table
  WHERE "Transaction Payment Status"='Paid'
  GROUP BY "Customer ID"
  HAVING SUM("Transaction Amount") > 5000
)
SELECT ct."Contract Performance Status", COUNT(*) as cnt
FROM hv JOIN contracts_table ct ON hv."Customer ID"=ct."Customer ID"
GROUP BY ct."Contract Performance Status" ORDER BY cnt DESC
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-033/attempt-01/sql/S63.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-033/attempt-01/sql/S63.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-033/attempt-01/results/S63.rows.jsonl)；完整：True；SHA256：`861c17a1321011202b37cb7a8b7d89858bb5de2798672d6635c3e544f4afcb54`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "transaction_history_table", "kind": "base", "block": null, "base_tables": ["transaction_history_table"]}] | [] | ["\"Customer ID\""] |
| B2 | [{"alias": "hv", "kind": "derived", "block": "B1", "base_tables": ["transaction_history_table"]}, {"alias": "ct", "kind": "base", "block": null, "base_tables": ["contracts_table"]}] | [{"type": "INNER", "right": "contracts_table AS ct", "on": "hv.\"Customer ID\" = ct.\"Customer ID\"", "using": []}] | ["ct.\"Contract Performance Status\""] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | SUM("Transaction Amount") | [{"table": "transaction_history_table", "column": "Transaction Amount"}] | [] | False |
| B2 | COUNT(*) | [] | [] | True |


## S64

类别 `data`；来源 `query_db`；调用 `67f15da42afd48279c4cf5c79d9e5080`；状态 `success`。

```sql
WITH hv AS (
  SELECT DISTINCT "Customer ID" FROM transaction_history_table
  WHERE "Transaction Payment Status"='Paid'
  GROUP BY "Customer ID"
  HAVING SUM("Transaction Amount") > 5000
)
SELECT po."Current Service Status", COUNT(*) as cnt, SUM(po."Total Amount") as tot_amt
FROM hv JOIN product_service_order_table po ON hv."Customer ID"=po."Customer ID"
GROUP BY po."Current Service Status" ORDER BY cnt DESC
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-033/attempt-01/sql/S64.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-033/attempt-01/sql/S64.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-033/attempt-01/results/S64.rows.jsonl)；完整：True；SHA256：`3533b132a0ac9943ab6b89e24b7011047fb60293a6358ccb5ec92bb94f8e7a74`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "transaction_history_table", "kind": "base", "block": null, "base_tables": ["transaction_history_table"]}] | [] | ["\"Customer ID\""] |
| B2 | [{"alias": "hv", "kind": "derived", "block": "B1", "base_tables": ["transaction_history_table"]}, {"alias": "po", "kind": "base", "block": null, "base_tables": ["product_service_order_table"]}] | [{"type": "INNER", "right": "product_service_order_table AS po", "on": "hv.\"Customer ID\" = po.\"Customer ID\"", "using": []}] | ["po.\"Current Service Status\""] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | SUM("Transaction Amount") | [{"table": "transaction_history_table", "column": "Transaction Amount"}] | [] | False |
| B2 | COUNT(*) | [] | [] | True |
| B2 | SUM(po."Total Amount") | [{"table": "product_service_order_table", "column": "Total Amount"}] | [] | False |


## S65

类别 `data`；来源 `query_db`；调用 `80d47cbb877143bdaf70e077e53573cc`；状态 `success`。

```sql
WITH hv AS (
  SELECT DISTINCT "Customer ID" FROM transaction_history_table
  WHERE "Transaction Payment Status"='Paid'
  GROUP BY "Customer ID"
  HAVING SUM("Transaction Amount") > 5000
)
SELECT sf."Follow-up Result Status", sf."Follow-up Priority", COUNT(*) as cnt
FROM hv JOIN sales_follow_up_table sf ON hv."Customer ID"=sf."Customer ID"
GROUP BY sf."Follow-up Result Status", sf."Follow-up Priority" ORDER BY cnt DESC
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-033/attempt-01/sql/S65.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-033/attempt-01/sql/S65.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-033/attempt-01/results/S65.rows.jsonl)；完整：True；SHA256：`42ef5b4becb3854763790320ccb35b5e5d7e9eb4d5cfabf604fd9d7ce765b064`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "transaction_history_table", "kind": "base", "block": null, "base_tables": ["transaction_history_table"]}] | [] | ["\"Customer ID\""] |
| B2 | [{"alias": "hv", "kind": "derived", "block": "B1", "base_tables": ["transaction_history_table"]}, {"alias": "sf", "kind": "base", "block": null, "base_tables": ["sales_follow_up_table"]}] | [{"type": "INNER", "right": "sales_follow_up_table AS sf", "on": "hv.\"Customer ID\" = sf.\"Customer ID\"", "using": []}] | ["sf.\"Follow-up Result Status\"", "sf.\"Follow-up Priority\""] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | SUM("Transaction Amount") | [{"table": "transaction_history_table", "column": "Transaction Amount"}] | [] | False |
| B2 | COUNT(*) | [] | [] | True |


## S66

类别 `data`；来源 `query_db`；调用 `0c89eee5100341a78f1de9936d2c8689`；状态 `success`。

```sql
SELECT COUNT(DISTINCT "Customer ID") as custs, COUNT(*) as rows FROM customer_account_table
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-033/attempt-01/sql/S66.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-033/attempt-01/sql/S66.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-033/attempt-01/results/S66.rows.jsonl)；完整：True；SHA256：`0b8258efc4fe7ecfe73ee6931cda975133f8e941b220fc2c09f6d32384dc4a3b`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "customer_account_table", "kind": "base", "block": null, "base_tables": ["customer_account_table"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(DISTINCT "Customer ID") | [{"table": "customer_account_table", "column": "Customer ID"}] | [] | False |
| B1 | COUNT(*) | [] | [] | True |


## S67

类别 `data`；来源 `query_db`；调用 `1717e3f27e704e109993aa6ff54aa930`；状态 `success`。

```sql
SELECT COUNT(*) as matched_tx FROM transaction_history_table t JOIN customer_account_table a ON t."Account ID"=a."Account ID"
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-033/attempt-01/sql/S67.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-033/attempt-01/sql/S67.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-033/attempt-01/results/S67.rows.jsonl)；完整：True；SHA256：`a860af813318abf340e86b3863f8e8ca2484e44229650b01ef2f15d3e8c700a3`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "t", "kind": "base", "block": null, "base_tables": ["transaction_history_table"]}, {"alias": "a", "kind": "base", "block": null, "base_tables": ["customer_account_table"]}] | [{"type": "INNER", "right": "customer_account_table AS a", "on": "t.\"Account ID\" = a.\"Account ID\"", "using": []}] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |


## S68

类别 `data`；来源 `query_db`；调用 `e6dec62d237345d1b5f23309b3d60400`；状态 `failed`。

```sql
SELECT a."Account Type", COUNT(DISTINCT t."Customer ID") as hv_customers
FROM (SELECT DISTINCT "Customer ID" FROM transaction_history_table WHERE "Transaction Payment Status"='Paid' GROUP BY "Customer ID" HAVING SUM("Transaction Amount")>5000) hv
LEFT JOIN customer_account_table a ON hv."Customer ID"=a."Customer ID"
GROUP BY a."Account Type"
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-033/attempt-01/sql/S68.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-033/attempt-01/sql/S68.parameters.json)。

错误：`OperationalError('no such column: t.Customer ID')`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "transaction_history_table", "kind": "base", "block": null, "base_tables": ["transaction_history_table"]}] | [] | ["\"Customer ID\""] |
| B2 | [{"alias": "hv", "kind": "derived", "block": "B1", "base_tables": ["transaction_history_table"]}, {"alias": "a", "kind": "base", "block": null, "base_tables": ["customer_account_table"]}] | [{"type": "LEFT", "right": "customer_account_table AS a", "on": "hv.\"Customer ID\" = a.\"Customer ID\"", "using": []}] | ["a.\"Account Type\""] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | SUM("Transaction Amount") | [{"table": "transaction_history_table", "column": "Transaction Amount"}] | [] | False |
| B2 | COUNT(DISTINCT t."Customer ID") | [{"unknown": "t.\"Customer ID\""}] | [] | False |


未解析列血缘：[{"block": "B2", "column": "t.\"Customer ID\"", "reason": "ambiguous_or_missing_source"}, {"block": "B2", "column": "t.\"Customer ID\"", "reason": "ambiguous_or_missing_source"}]

## S69

类别 `data`；来源 `query_db`；调用 `bfc34afb8e854d6ca78312469eea20a8`；状态 `success`。

```sql
SELECT a."Account Type", COUNT(*) as cnt FROM customer_account_table a GROUP BY a."Account Type"
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-033/attempt-01/sql/S69.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-033/attempt-01/sql/S69.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-033/attempt-01/results/S69.rows.jsonl)；完整：True；SHA256：`7ea04928d651f5ec4c398b713821875baeceb36ab23309a753c651d2ae98fb6e`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "a", "kind": "base", "block": null, "base_tables": ["customer_account_table"]}] | [] | ["a.\"Account Type\""] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |


## S70

类别 `data`；来源 `query_db`；调用 `2f790b87ac5c4ff58994ebe012d6fe22`；状态 `success`。

```sql
SELECT a."Account Type", COUNT(*) as cnt
FROM (SELECT DISTINCT "Customer ID" FROM transaction_history_table WHERE "Transaction Payment Status"='Paid' GROUP BY "Customer ID" HAVING SUM("Transaction Amount")>5000) hv
JOIN customer_account_table a ON hv."Customer ID"=a."Customer ID"
GROUP BY a."Account Type"
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-033/attempt-01/sql/S70.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-033/attempt-01/sql/S70.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-033/attempt-01/results/S70.rows.jsonl)；完整：True；SHA256：`f791a57dbe269f9f1fe058fde89858813d6c8d8519630e8de397cf898aa0e644`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "transaction_history_table", "kind": "base", "block": null, "base_tables": ["transaction_history_table"]}] | [] | ["\"Customer ID\""] |
| B2 | [{"alias": "hv", "kind": "derived", "block": "B1", "base_tables": ["transaction_history_table"]}, {"alias": "a", "kind": "base", "block": null, "base_tables": ["customer_account_table"]}] | [{"type": "INNER", "right": "customer_account_table AS a", "on": "hv.\"Customer ID\" = a.\"Customer ID\"", "using": []}] | ["a.\"Account Type\""] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | SUM("Transaction Amount") | [{"table": "transaction_history_table", "column": "Transaction Amount"}] | [] | False |
| B2 | COUNT(*) | [] | [] | True |


## S71

类别 `data`；来源 `query_db`；调用 `d9b7f6f27d4b435c88c3ec245f85a7a4`；状态 `success`。

```sql
SELECT a."Account Credit Rating", COUNT(*) as cnt
FROM (SELECT DISTINCT "Customer ID" FROM transaction_history_table WHERE "Transaction Payment Status"='Paid' GROUP BY "Customer ID" HAVING SUM("Transaction Amount")>5000) hv
JOIN customer_account_table a ON hv."Customer ID"=a."Customer ID"
GROUP BY a."Account Credit Rating"
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-033/attempt-01/sql/S71.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-033/attempt-01/sql/S71.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-033/attempt-01/results/S71.rows.jsonl)；完整：True；SHA256：`a5fa27d7fd4c0c0ef8891b8aadf29bb3030290a585766ce512441542e056a060`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "transaction_history_table", "kind": "base", "block": null, "base_tables": ["transaction_history_table"]}] | [] | ["\"Customer ID\""] |
| B2 | [{"alias": "hv", "kind": "derived", "block": "B1", "base_tables": ["transaction_history_table"]}, {"alias": "a", "kind": "base", "block": null, "base_tables": ["customer_account_table"]}] | [{"type": "INNER", "right": "customer_account_table AS a", "on": "hv.\"Customer ID\" = a.\"Customer ID\"", "using": []}] | ["a.\"Account Credit Rating\""] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | SUM("Transaction Amount") | [{"table": "transaction_history_table", "column": "Transaction Amount"}] | [] | False |
| B2 | COUNT(*) | [] | [] | True |


## S72

类别 `data`；来源 `query_db`；调用 `757615d5334040149439eec90b156fd2`；状态 `success`。

```sql
SELECT a."Account Credit Rating", COUNT(*) as cnt FROM customer_account_table a GROUP BY a."Account Credit Rating"
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-033/attempt-01/sql/S72.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-033/attempt-01/sql/S72.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-033/attempt-01/results/S72.rows.jsonl)；完整：True；SHA256：`252362dbeb954d9aac3e597b3f060437e795349c43fae99bdac6e2bd41d136fd`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "a", "kind": "base", "block": null, "base_tables": ["customer_account_table"]}] | [] | ["a.\"Account Credit Rating\""] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |


## S73

类别 `data`；来源 `query_db`；调用 `87833ad15c2d44838979d7d9f5e19927`；状态 `success`。

```sql
SELECT "Membership Level", COUNT(*) as all_cust FROM membership_table GROUP BY "Membership Level" ORDER BY all_cust DESC
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-033/attempt-01/sql/S73.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-033/attempt-01/sql/S73.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-033/attempt-01/results/S73.rows.jsonl)；完整：True；SHA256：`a706e0c9e4bc2dcfab4e798276c44b0b33d7acefe9cb58ac858b32491469fb2b`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "membership_table", "kind": "base", "block": null, "base_tables": ["membership_table"]}] | [] | ["\"Membership Level\""] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |


## S74

类别 `data`；来源 `query_db`；调用 `da297dd086de40208a7c5080aa56112d`；状态 `success`。

```sql
WITH hv AS (SELECT DISTINCT "Customer ID" FROM transaction_history_table WHERE "Transaction Payment Status"='Paid' GROUP BY "Customer ID" HAVING SUM("Transaction Amount")>5000)
SELECT m."Membership Level", COUNT(*) as hv_cust FROM hv JOIN membership_table m ON hv."Customer ID"=m."Customer ID" GROUP BY m."Membership Level" ORDER BY hv_cust DESC
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-033/attempt-01/sql/S74.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-033/attempt-01/sql/S74.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-033/attempt-01/results/S74.rows.jsonl)；完整：True；SHA256：`bd027af92d6b1175562089508c85825202703f1fff0401903e7639fa872e5039`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "transaction_history_table", "kind": "base", "block": null, "base_tables": ["transaction_history_table"]}] | [] | ["\"Customer ID\""] |
| B2 | [{"alias": "hv", "kind": "derived", "block": "B1", "base_tables": ["transaction_history_table"]}, {"alias": "m", "kind": "base", "block": null, "base_tables": ["membership_table"]}] | [{"type": "INNER", "right": "membership_table AS m", "on": "hv.\"Customer ID\" = m.\"Customer ID\"", "using": []}] | ["m.\"Membership Level\""] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | SUM("Transaction Amount") | [{"table": "transaction_history_table", "column": "Transaction Amount"}] | [] | False |
| B2 | COUNT(*) | [] | [] | True |


## S75

类别 `data`；来源 `query_db`；调用 `70d7f47f4091493bb37713bcfdfa959b`；状态 `success`。

```sql
SELECT "Tag Name", COUNT(*) as all_cust FROM customer_tag_table GROUP BY "Tag Name" ORDER BY all_cust DESC
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-033/attempt-01/sql/S75.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-033/attempt-01/sql/S75.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-033/attempt-01/results/S75.rows.jsonl)；完整：True；SHA256：`99cbf70c3e11994a8d4f7e21ddb9902e6a7c363fa1a82726899730fc1286bfae`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "customer_tag_table", "kind": "base", "block": null, "base_tables": ["customer_tag_table"]}] | [] | ["\"Tag Name\""] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |


## S76

类别 `data`；来源 `query_db`；调用 `d2e3418a9f164d8dad18faf317dffc40`；状态 `success`。

```sql
SELECT "Contract Type", COUNT(*) as all_cust FROM contracts_table GROUP BY "Contract Type" ORDER BY all_cust DESC
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-033/attempt-01/sql/S76.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-033/attempt-01/sql/S76.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-033/attempt-01/results/S76.rows.jsonl)；完整：True；SHA256：`4d43d088b77d63b874224b006f850df1fd7e2fbc0dfc03f27fd1ee7c781f8172`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "contracts_table", "kind": "base", "block": null, "base_tables": ["contracts_table"]}] | [] | ["\"Contract Type\""] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |


## S77

类别 `data`；来源 `query_db`；调用 `c9a48b632dc54b42a90b25dea09f8524`；状态 `success`。

```sql
SELECT "Contract Performance Status", COUNT(*) as all_cust FROM contracts_table GROUP BY "Contract Performance Status" ORDER BY all_cust DESC
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-033/attempt-01/sql/S77.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-033/attempt-01/sql/S77.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-033/attempt-01/results/S77.rows.jsonl)；完整：True；SHA256：`df197364bba2efc063c5d105d1c2d2bf88277bd787382918e6c8e9d1303d9a76`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "contracts_table", "kind": "base", "block": null, "base_tables": ["contracts_table"]}] | [] | ["\"Contract Performance Status\""] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |


## S78

类别 `data`；来源 `query_db`；调用 `6ea5133d7ae944d8a57147be6ead5071`；状态 `success`。

```sql
SELECT "Subscribed Product Name", COUNT(*) as all_cust, SUM("Total Amount") as total_amt FROM product_service_order_table GROUP BY "Subscribed Product Name" ORDER BY all_cust DESC
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-033/attempt-01/sql/S78.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-033/attempt-01/sql/S78.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-033/attempt-01/results/S78.rows.jsonl)；完整：True；SHA256：`46e80645072fa711ec17824721e6df6df9b30ca64626c241fb27512e23931404`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "product_service_order_table", "kind": "base", "block": null, "base_tables": ["product_service_order_table"]}] | [] | ["\"Subscribed Product Name\""] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |
| B1 | SUM("Total Amount") | [{"table": "product_service_order_table", "column": "Total Amount"}] | [] | False |


## S79

类别 `data`；来源 `query_db`；调用 `f1017ccfa41442698b8d3eb27e924c9c`；状态 `success`。

```sql
SELECT "Gender", COUNT(*) as all_cust FROM customer_contact_table GROUP BY "Gender"
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-033/attempt-01/sql/S79.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-033/attempt-01/sql/S79.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-033/attempt-01/results/S79.rows.jsonl)；完整：True；SHA256：`e8b5dca886b504fcc28495676f7a5a259ee31d0ece08f7eb50f855e595a4e3f4`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "customer_contact_table", "kind": "base", "block": null, "base_tables": ["customer_contact_table"]}] | [] | ["\"Gender\""] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |


## S80

类别 `data`；来源 `query_db`；调用 `85534331b46f4a9c8b74f030c97cd947`；状态 `success`。

```sql
WITH hv AS (SELECT DISTINCT "Customer ID" FROM transaction_history_table WHERE "Transaction Payment Status"='Paid' GROUP BY "Customer ID" HAVING SUM("Transaction Amount")>5000)
SELECT c."Gender", COUNT(*) as hv_cust FROM hv JOIN customer_contact_table c ON hv."Customer ID"=c."Customer ID" GROUP BY c."Gender"
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-033/attempt-01/sql/S80.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-033/attempt-01/sql/S80.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-033/attempt-01/results/S80.rows.jsonl)；完整：True；SHA256：`3921aecb2194538a327d817e8b2e9156f93bfb51313c513767e53f3ea25057d2`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "transaction_history_table", "kind": "base", "block": null, "base_tables": ["transaction_history_table"]}] | [] | ["\"Customer ID\""] |
| B2 | [{"alias": "hv", "kind": "derived", "block": "B1", "base_tables": ["transaction_history_table"]}, {"alias": "c", "kind": "base", "block": null, "base_tables": ["customer_contact_table"]}] | [{"type": "INNER", "right": "customer_contact_table AS c", "on": "hv.\"Customer ID\" = c.\"Customer ID\"", "using": []}] | ["c.\"Gender\""] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | SUM("Transaction Amount") | [{"table": "transaction_history_table", "column": "Transaction Amount"}] | [] | False |
| B2 | COUNT(*) | [] | [] | True |


## S81

类别 `data`；来源 `query_db`；调用 `f6940a70c89a468385f0f6351634cf35`；状态 `success`。

```sql
SELECT "Channel Name", COUNT(*) as all_cust FROM channel_source_table GROUP BY "Channel Name" ORDER BY all_cust DESC
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-033/attempt-01/sql/S81.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-033/attempt-01/sql/S81.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-033/attempt-01/results/S81.rows.jsonl)；完整：True；SHA256：`8b8992a4477d5b2fec1671564cfd30ae88545048d0b1f7ac6dbd9e889a36067a`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "channel_source_table", "kind": "base", "block": null, "base_tables": ["channel_source_table"]}] | [] | ["\"Channel Name\""] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |


## S82

类别 `data`；来源 `query_db`；调用 `39cb0359eb3944cbb0c9ffb46f78c96e`；状态 `success`。

```sql
WITH hv AS (SELECT DISTINCT "Customer ID" FROM transaction_history_table WHERE "Transaction Payment Status"='Paid' GROUP BY "Customer ID" HAVING SUM("Transaction Amount")>5000)
SELECT cs."Channel Name", COUNT(*) as hv_cust FROM hv JOIN channel_source_table cs ON hv."Customer ID"=cs."Customer ID" GROUP BY cs."Channel Name" ORDER BY hv_cust DESC
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-033/attempt-01/sql/S82.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-033/attempt-01/sql/S82.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-033/attempt-01/results/S82.rows.jsonl)；完整：True；SHA256：`8e6bbc78a1cab6b4e900537d621110104313d9ef2a12e7898f6f7f00fc05eb00`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "transaction_history_table", "kind": "base", "block": null, "base_tables": ["transaction_history_table"]}] | [] | ["\"Customer ID\""] |
| B2 | [{"alias": "hv", "kind": "derived", "block": "B1", "base_tables": ["transaction_history_table"]}, {"alias": "cs", "kind": "base", "block": null, "base_tables": ["channel_source_table"]}] | [{"type": "INNER", "right": "channel_source_table AS cs", "on": "hv.\"Customer ID\" = cs.\"Customer ID\"", "using": []}] | ["cs.\"Channel Name\""] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | SUM("Transaction Amount") | [{"table": "transaction_history_table", "column": "Transaction Amount"}] | [] | False |
| B2 | COUNT(*) | [] | [] | True |


## S83

类别 `data`；来源 `query_db`；调用 `0d28bdecc949472a925a8dd35204b911`；状态 `success`。

```sql
SELECT "Complaint Customer Satisfaction", COUNT(*) as cnt FROM complaints_table GROUP BY "Complaint Customer Satisfaction" ORDER BY cnt DESC
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-033/attempt-01/sql/S83.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-033/attempt-01/sql/S83.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-033/attempt-01/results/S83.rows.jsonl)；完整：True；SHA256：`b11fa968e71f213570020c7f4d6472fc17060a26d96c464d6d7cdfb206dc5a0d`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "complaints_table", "kind": "base", "block": null, "base_tables": ["complaints_table"]}] | [] | ["\"Complaint Customer Satisfaction\""] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |


## S84

类别 `data`；来源 `query_db`；调用 `59465df1838549d18f89010c508865d0`；状态 `success`。

```sql
SELECT "Ticket customer satisfaction score", COUNT(*) as cnt FROM service_ticket_table GROUP BY "Ticket customer satisfaction score"
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-033/attempt-01/sql/S84.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-033/attempt-01/sql/S84.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-033/attempt-01/results/S84.rows.jsonl)；完整：True；SHA256：`4670f25ce5a42f773e8067f7538207b746085c004355997a66285f86af36b555`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "service_ticket_table", "kind": "base", "block": null, "base_tables": ["service_ticket_table"]}] | [] | ["\"Ticket customer satisfaction score\""] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |


## S85

类别 `data`；来源 `query_db`；调用 `735da13125fd4c5cacb2dc9d44f2dcb4`；状态 `success`。

```sql
SELECT COUNT(*) as matched FROM complaints_table c JOIN service_ticket_table s ON c."Work Order ID"=s."Work Order ID"
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-033/attempt-01/sql/S85.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-033/attempt-01/sql/S85.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-033/attempt-01/results/S85.rows.jsonl)；完整：True；SHA256：`04de87c9cef75ee2b7959b33452fc678bdf8d6e4580f5ea21ae07279c657a3d4`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "c", "kind": "base", "block": null, "base_tables": ["complaints_table"]}, {"alias": "s", "kind": "base", "block": null, "base_tables": ["service_ticket_table"]}] | [{"type": "INNER", "right": "service_ticket_table AS s", "on": "c.\"Work Order ID\" = s.\"Work Order ID\"", "using": []}] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |


## S86

类别 `data`；来源 `query_db`；调用 `7123a7f9e85a43f881879f7bdc62b062`；状态 `success`。

```sql
SELECT COUNT(*) as matched FROM service_ticket_table s JOIN contracts_table c ON s."Contract ID"=c."Contract ID"
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-033/attempt-01/sql/S86.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-033/attempt-01/sql/S86.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-033/attempt-01/results/S86.rows.jsonl)；完整：True；SHA256：`cfb371f1a88c3424cb03342a029dd86e04138bb3d91d7648ded0be6c5aaf6210`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "s", "kind": "base", "block": null, "base_tables": ["service_ticket_table"]}, {"alias": "c", "kind": "base", "block": null, "base_tables": ["contracts_table"]}] | [{"type": "INNER", "right": "contracts_table AS c", "on": "s.\"Contract ID\" = c.\"Contract ID\"", "using": []}] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |


## S87

类别 `data`；来源 `query_db`；调用 `67371b2f505d4ac8b41c7742d3207c8c`；状态 `success`。

```sql
WITH hv AS (SELECT DISTINCT "Customer ID" FROM transaction_history_table WHERE "Transaction Payment Status"='Paid' GROUP BY "Customer ID" HAVING SUM("Transaction Amount")>5000)
SELECT s."Ticket customer satisfaction score", COUNT(*) as cnt
FROM hv 
JOIN contracts_table c ON hv."Customer ID"=c."Customer ID"
JOIN service_ticket_table s ON c."Contract ID"=s."Contract ID"
GROUP BY s."Ticket customer satisfaction score"
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-033/attempt-01/sql/S87.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-033/attempt-01/sql/S87.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-033/attempt-01/results/S87.rows.jsonl)；完整：True；SHA256：`2cf6e32c951abf49ed32df0252491ba96eb491644ba3f34b3b888bd16457deba`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "transaction_history_table", "kind": "base", "block": null, "base_tables": ["transaction_history_table"]}] | [] | ["\"Customer ID\""] |
| B2 | [{"alias": "hv", "kind": "derived", "block": "B1", "base_tables": ["transaction_history_table"]}, {"alias": "c", "kind": "base", "block": null, "base_tables": ["contracts_table"]}, {"alias": "s", "kind": "base", "block": null, "base_tables": ["service_ticket_table"]}] | [{"type": "INNER", "right": "contracts_table AS c", "on": "hv.\"Customer ID\" = c.\"Customer ID\"", "using": []}, {"type": "INNER", "right": "service_ticket_table AS s", "on": "c.\"Contract ID\" = s.\"Contract ID\"", "using": []}] | ["s.\"Ticket customer satisfaction score\""] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | SUM("Transaction Amount") | [{"table": "transaction_history_table", "column": "Transaction Amount"}] | [] | False |
| B2 | COUNT(*) | [] | [] | True |


## S88

类别 `data`；来源 `query_db`；调用 `dcfd17b117434c58b8ab37f64108353d`；状态 `success`。

```sql
WITH hv AS (SELECT DISTINCT "Customer ID" FROM transaction_history_table WHERE "Transaction Payment Status"='Paid' GROUP BY "Customer ID" HAVING SUM("Transaction Amount")>5000)
SELECT comp."Complaint Customer Satisfaction", COUNT(*) as cnt
FROM hv 
JOIN contracts_table c ON hv."Customer ID"=c."Customer ID"
JOIN service_ticket_table s ON c."Contract ID"=s."Contract ID"
JOIN complaints_table comp ON s."Work Order ID"=comp."Work Order ID"
GROUP BY comp."Complaint Customer Satisfaction"
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-033/attempt-01/sql/S88.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-033/attempt-01/sql/S88.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-033/attempt-01/results/S88.rows.jsonl)；完整：True；SHA256：`e65ffb52181b308d550d5c0bd170bfb4dab988951658c852f551271346b3467a`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "transaction_history_table", "kind": "base", "block": null, "base_tables": ["transaction_history_table"]}] | [] | ["\"Customer ID\""] |
| B2 | [{"alias": "hv", "kind": "derived", "block": "B1", "base_tables": ["transaction_history_table"]}, {"alias": "c", "kind": "base", "block": null, "base_tables": ["contracts_table"]}, {"alias": "s", "kind": "base", "block": null, "base_tables": ["service_ticket_table"]}, {"alias": "comp", "kind": "base", "block": null, "base_tables": ["complaints_table"]}] | [{"type": "INNER", "right": "contracts_table AS c", "on": "hv.\"Customer ID\" = c.\"Customer ID\"", "using": []}, {"type": "INNER", "right": "service_ticket_table AS s", "on": "c.\"Contract ID\" = s.\"Contract ID\"", "using": []}, {"type": "INNER", "right": "complaints_table AS comp", "on": "s.\"Work Order ID\" = comp.\"Work Order ID\"", "using": []}] | ["comp.\"Complaint Customer Satisfaction\""] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | SUM("Transaction Amount") | [{"table": "transaction_history_table", "column": "Transaction Amount"}] | [] | False |
| B2 | COUNT(*) | [] | [] | True |


## S89

类别 `data`；来源 `query_db`；调用 `3287d2adae4d4ce6a027e8b762f951c5`；状态 `success`。

```sql
SELECT s."Ticket customer satisfaction score", COUNT(*) as cnt_all
FROM service_ticket_table s
GROUP BY s."Ticket customer satisfaction score"
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-033/attempt-01/sql/S89.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-033/attempt-01/sql/S89.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-033/attempt-01/results/S89.rows.jsonl)；完整：True；SHA256：`4670f25ce5a42f773e8067f7538207b746085c004355997a66285f86af36b555`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "s", "kind": "base", "block": null, "base_tables": ["service_ticket_table"]}] | [] | ["s.\"Ticket customer satisfaction score\""] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |


## S90

类别 `data`；来源 `query_db`；调用 `bc39a8edcbd34cd7afc6168535e54d63`；状态 `success`。

```sql
SELECT comp."Complaint Customer Satisfaction", COUNT(*) as cnt_all 
FROM complaints_table comp
GROUP BY comp."Complaint Customer Satisfaction"
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-033/attempt-01/sql/S90.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-033/attempt-01/sql/S90.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-033/attempt-01/results/S90.rows.jsonl)；完整：True；SHA256：`c9f71296fe3cc2125e98f1e858d4d7c7e5fa86460d9d99b54d65dc46365a9eb6`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "comp", "kind": "base", "block": null, "base_tables": ["complaints_table"]}] | [] | ["comp.\"Complaint Customer Satisfaction\""] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |


## S91

类别 `data`；来源 `query_db`；调用 `b012c0c6eed14f9c8f20b5bc503b9771`；状态 `success`。

```sql
WITH hv AS (SELECT DISTINCT "Customer ID" FROM transaction_history_table WHERE "Transaction Payment Status"='Paid' GROUP BY "Customer ID" HAVING SUM("Transaction Amount")>5000)
SELECT COUNT(DISTINCT s."Work Order ID") as hv_tickets, AVG(s."Ticket customer satisfaction score") as avg_sat, AVG(s."Ticket resolution duration") as avg_duration
FROM hv 
JOIN contracts_table c ON hv."Customer ID"=c."Customer ID"
JOIN service_ticket_table s ON c."Contract ID"=s."Contract ID"
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-033/attempt-01/sql/S91.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-033/attempt-01/sql/S91.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-033/attempt-01/results/S91.rows.jsonl)；完整：True；SHA256：`6f70008f70d82c528489010a6c68bdcd0f13bff1085710372832fc87c5410489`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "transaction_history_table", "kind": "base", "block": null, "base_tables": ["transaction_history_table"]}] | [] | ["\"Customer ID\""] |
| B2 | [{"alias": "hv", "kind": "derived", "block": "B1", "base_tables": ["transaction_history_table"]}, {"alias": "c", "kind": "base", "block": null, "base_tables": ["contracts_table"]}, {"alias": "s", "kind": "base", "block": null, "base_tables": ["service_ticket_table"]}] | [{"type": "INNER", "right": "contracts_table AS c", "on": "hv.\"Customer ID\" = c.\"Customer ID\"", "using": []}, {"type": "INNER", "right": "service_ticket_table AS s", "on": "c.\"Contract ID\" = s.\"Contract ID\"", "using": []}] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | SUM("Transaction Amount") | [{"table": "transaction_history_table", "column": "Transaction Amount"}] | [] | False |
| B2 | COUNT(DISTINCT s."Work Order ID") | [{"table": "service_ticket_table", "column": "Work Order ID"}] | [] | False |
| B2 | AVG(s."Ticket customer satisfaction score") | [{"table": "service_ticket_table", "column": "Ticket customer satisfaction score"}] | [] | False |
| B2 | AVG(s."Ticket resolution duration") | [{"table": "service_ticket_table", "column": "Ticket resolution duration"}] | [] | False |


## S92

类别 `data`；来源 `query_db`；调用 `b55e1879b7604a07b289f1e88c936488`；状态 `success`。

```sql
SELECT AVG("Ticket customer satisfaction score") as avg_sat_all, AVG("Ticket resolution duration") as avg_duration_all FROM service_ticket_table
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-033/attempt-01/sql/S92.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-033/attempt-01/sql/S92.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-033/attempt-01/results/S92.rows.jsonl)；完整：True；SHA256：`1095aad1cbf3f782dc422cb3774ebd74b5fe8ad6b732ff11d2b8de066f1bb9d5`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "service_ticket_table", "kind": "base", "block": null, "base_tables": ["service_ticket_table"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | AVG("Ticket customer satisfaction score") | [{"table": "service_ticket_table", "column": "Ticket customer satisfaction score"}] | [] | False |
| B1 | AVG("Ticket resolution duration") | [{"table": "service_ticket_table", "column": "Ticket resolution duration"}] | [] | False |


## S93

类别 `data`；来源 `query_db`；调用 `3517126e75564706941934e9f6780cd6`；状态 `success`。

```sql
WITH hv AS (SELECT DISTINCT "Customer ID" FROM transaction_history_table WHERE "Transaction Payment Status"='Paid' GROUP BY "Customer ID" HAVING SUM("Transaction Amount")>5000)
SELECT AVG(m."Current Points") as avg_cur, AVG(m."Lifetime Points") as avg_life, MIN(m."Lifetime Points") as min_life, MAX(m."Lifetime Points") as max_life
FROM hv JOIN membership_table m ON hv."Customer ID"=m."Customer ID"
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-033/attempt-01/sql/S93.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-033/attempt-01/sql/S93.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-033/attempt-01/results/S93.rows.jsonl)；完整：True；SHA256：`8ba7de4b4b6fa80db3b2e37e54c4561b84b577c38e63c5ed9f4989e66f70fd80`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "transaction_history_table", "kind": "base", "block": null, "base_tables": ["transaction_history_table"]}] | [] | ["\"Customer ID\""] |
| B2 | [{"alias": "hv", "kind": "derived", "block": "B1", "base_tables": ["transaction_history_table"]}, {"alias": "m", "kind": "base", "block": null, "base_tables": ["membership_table"]}] | [{"type": "INNER", "right": "membership_table AS m", "on": "hv.\"Customer ID\" = m.\"Customer ID\"", "using": []}] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | SUM("Transaction Amount") | [{"table": "transaction_history_table", "column": "Transaction Amount"}] | [] | False |
| B2 | AVG(m."Current Points") | [{"table": "membership_table", "column": "Current Points"}] | [] | False |
| B2 | AVG(m."Lifetime Points") | [{"table": "membership_table", "column": "Lifetime Points"}] | [] | False |
| B2 | MIN(m."Lifetime Points") | [{"table": "membership_table", "column": "Lifetime Points"}] | [] | False |
| B2 | MAX(m."Lifetime Points") | [{"table": "membership_table", "column": "Lifetime Points"}] | [] | False |


## S94

类别 `data`；来源 `query_db`；调用 `52f9101811c740a19325c4eb8c378e73`；状态 `success`。

```sql
SELECT AVG("Current Points") as avg_cur_all, AVG("Lifetime Points") as avg_life_all, MIN("Lifetime Points") as min_life_all, MAX("Lifetime Points") as max_life_all FROM membership_table
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-033/attempt-01/sql/S94.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-033/attempt-01/sql/S94.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-033/attempt-01/results/S94.rows.jsonl)；完整：True；SHA256：`b0b237fa0fc355ba67b1e0fb099204b439d66be8dd9c9c63b107fc1a3cd10d2b`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "membership_table", "kind": "base", "block": null, "base_tables": ["membership_table"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | AVG("Current Points") | [{"table": "membership_table", "column": "Current Points"}] | [] | False |
| B1 | AVG("Lifetime Points") | [{"table": "membership_table", "column": "Lifetime Points"}] | [] | False |
| B1 | MIN("Lifetime Points") | [{"table": "membership_table", "column": "Lifetime Points"}] | [] | False |
| B1 | MAX("Lifetime Points") | [{"table": "membership_table", "column": "Lifetime Points"}] | [] | False |


## S95

类别 `data`；来源 `query_db`；调用 `0915ce04175443a687a6ab4dd08226e1`；状态 `success`。

```sql
WITH hv AS (SELECT DISTINCT "Customer ID" FROM transaction_history_table WHERE "Transaction Payment Status"='Paid' GROUP BY "Customer ID" HAVING SUM("Transaction Amount")>5000)
SELECT m."Upgrade Requirements Met", COUNT(*) as cnt FROM hv JOIN membership_table m ON hv."Customer ID"=m."Customer ID" GROUP BY m."Upgrade Requirements Met"
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-033/attempt-01/sql/S95.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-033/attempt-01/sql/S95.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-033/attempt-01/results/S95.rows.jsonl)；完整：True；SHA256：`9d6baad9c9f188348b86af7fb97db5eb940359331b5b249be5c7f7269717a38d`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "transaction_history_table", "kind": "base", "block": null, "base_tables": ["transaction_history_table"]}] | [] | ["\"Customer ID\""] |
| B2 | [{"alias": "hv", "kind": "derived", "block": "B1", "base_tables": ["transaction_history_table"]}, {"alias": "m", "kind": "base", "block": null, "base_tables": ["membership_table"]}] | [{"type": "INNER", "right": "membership_table AS m", "on": "hv.\"Customer ID\" = m.\"Customer ID\"", "using": []}] | ["m.\"Upgrade Requirements Met\""] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | SUM("Transaction Amount") | [{"table": "transaction_history_table", "column": "Transaction Amount"}] | [] | False |
| B2 | COUNT(*) | [] | [] | True |


## S96

类别 `data`；来源 `query_db`；调用 `14e024f7fa824751a5939c950b220809`；状态 `success`。

```sql
SELECT "Upgrade Requirements Met", COUNT(*) as cnt FROM membership_table GROUP BY "Upgrade Requirements Met"
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-033/attempt-01/sql/S96.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-033/attempt-01/sql/S96.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-033/attempt-01/results/S96.rows.jsonl)；完整：True；SHA256：`1c7eefdd96cff4635acb94304c34652167c9af46cfd4c0b6fbe29e68d7fd9d59`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "membership_table", "kind": "base", "block": null, "base_tables": ["membership_table"]}] | [] | ["\"Upgrade Requirements Met\""] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |


## S97

类别 `data`；来源 `query_db`；调用 `79157169125f4538b8580937081d0794`；状态 `success`。

```sql
SELECT COUNT(DISTINCT t."Account ID") as tx_acc, COUNT(DISTINCT cr."Account ID") as cr_acc, COUNT(DISTINCT CASE WHEN t."Account ID"=cr."Account ID" THEN t."Account ID" END) as overlap
FROM transaction_history_table t, customer_credit_rating_table cr
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-033/attempt-01/sql/S97.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-033/attempt-01/sql/S97.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-033/attempt-01/results/S97.rows.jsonl)；完整：True；SHA256：`a4e23f9ef1dbd275431cef47b074bdb560a1d1929578d68656db0498410ae690`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "t", "kind": "base", "block": null, "base_tables": ["transaction_history_table"]}, {"alias": "cr", "kind": "base", "block": null, "base_tables": ["customer_credit_rating_table"]}] | [{"type": "CROSS", "right": "customer_credit_rating_table AS cr", "on": null, "using": []}] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(DISTINCT t."Account ID") | [{"table": "transaction_history_table", "column": "Account ID"}] | [] | False |
| B1 | COUNT(DISTINCT cr."Account ID") | [{"table": "customer_credit_rating_table", "column": "Account ID"}] | [] | False |
| B1 | COUNT(DISTINCT CASE WHEN t."Account ID" = cr."Account ID" THEN t."Account ID" END) | [{"table": "transaction_history_table", "column": "Account ID"}] | [{"table": "transaction_history_table", "column": "Account ID"}, {"table": "customer_credit_rating_table", "column": "Account ID"}] | False |


## S98

类别 `data`；来源 `query_db`；调用 `558a6cfbcccd4e41bdeeba368d1af804`；状态 `success`。

```sql
SELECT COUNT(*) as cnt FROM (SELECT DISTINCT "Account ID" FROM transaction_history_table) t JOIN (SELECT DISTINCT "Account ID" FROM customer_credit_rating_table) c ON t."Account ID"=c."Account ID"
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-033/attempt-01/sql/S98.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-033/attempt-01/sql/S98.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-033/attempt-01/results/S98.rows.jsonl)；完整：True；SHA256：`cd9e37abc084d5ad3814d9fc1c92c213f84158d2ef665be8146e114539655db1`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "transaction_history_table", "kind": "base", "block": null, "base_tables": ["transaction_history_table"]}] | [] | [] |
| B2 | [{"alias": "customer_credit_rating_table", "kind": "base", "block": null, "base_tables": ["customer_credit_rating_table"]}] | [] | [] |
| B3 | [{"alias": "t", "kind": "derived", "block": "B1", "base_tables": ["transaction_history_table"]}, {"alias": "c", "kind": "derived", "block": "B2", "base_tables": ["customer_credit_rating_table"]}] | [{"type": "INNER", "right": "(SELECT DISTINCT \"Account ID\" FROM customer_credit_rating_table) AS c", "on": "t.\"Account ID\" = c.\"Account ID\"", "using": []}] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B3 | COUNT(*) | [] | [] | True |


## S99

类别 `data`；来源 `query_db`；调用 `7434da5a41e74de99ee9d980a3df094a`；状态 `success`。

```sql
SELECT COUNT(*) as cnt FROM customer_credit_rating_table cr JOIN (SELECT DISTINCT "Account ID" FROM transaction_history_table) t ON t."Account ID"=cr."Account ID"
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-033/attempt-01/sql/S99.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-033/attempt-01/sql/S99.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-033/attempt-01/results/S99.rows.jsonl)；完整：True；SHA256：`cd9e37abc084d5ad3814d9fc1c92c213f84158d2ef665be8146e114539655db1`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "transaction_history_table", "kind": "base", "block": null, "base_tables": ["transaction_history_table"]}] | [] | [] |
| B2 | [{"alias": "cr", "kind": "base", "block": null, "base_tables": ["customer_credit_rating_table"]}, {"alias": "t", "kind": "derived", "block": "B1", "base_tables": ["transaction_history_table"]}] | [{"type": "INNER", "right": "(SELECT DISTINCT \"Account ID\" FROM transaction_history_table) AS t", "on": "t.\"Account ID\" = cr.\"Account ID\"", "using": []}] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B2 | COUNT(*) | [] | [] | True |


## S100

类别 `data`；来源 `query_db`；调用 `91a0e69332b94a7f8c0e9e0880766263`；状态 `success`。

```sql
WITH hv AS (SELECT DISTINCT "Customer ID" FROM transaction_history_table WHERE "Transaction Payment Status"='Paid' GROUP BY "Customer ID" HAVING SUM("Transaction Amount")>5000)
SELECT cr."Credit Grade", COUNT(*) as cnt, AVG(cr."Credit Score") as avg_score, AVG(cr."Credit Limit") as avg_limit
FROM hv 
JOIN transaction_history_table t ON hv."Customer ID"=t."Customer ID" AND t."Transaction Payment Status"='Paid'
JOIN customer_credit_rating_table cr ON t."Account ID"=cr."Account ID"
GROUP BY cr."Credit Grade" ORDER BY cnt DESC
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-033/attempt-01/sql/S100.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-033/attempt-01/sql/S100.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-033/attempt-01/results/S100.rows.jsonl)；完整：True；SHA256：`bf70eb9ec20d5d731bf5d3a4f8a112f25cfe7920b9c7c055ff34e5535ea41c30`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "transaction_history_table", "kind": "base", "block": null, "base_tables": ["transaction_history_table"]}] | [] | ["\"Customer ID\""] |
| B2 | [{"alias": "hv", "kind": "derived", "block": "B1", "base_tables": ["transaction_history_table"]}, {"alias": "t", "kind": "base", "block": null, "base_tables": ["transaction_history_table"]}, {"alias": "cr", "kind": "base", "block": null, "base_tables": ["customer_credit_rating_table"]}] | [{"type": "INNER", "right": "transaction_history_table AS t", "on": "hv.\"Customer ID\" = t.\"Customer ID\" AND t.\"Transaction Payment Status\" = 'Paid'", "using": []}, {"type": "INNER", "right": "customer_credit_rating_table AS cr", "on": "t.\"Account ID\" = cr.\"Account ID\"", "using": []}] | ["cr.\"Credit Grade\""] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | SUM("Transaction Amount") | [{"table": "transaction_history_table", "column": "Transaction Amount"}] | [] | False |
| B2 | COUNT(*) | [] | [] | True |
| B2 | AVG(cr."Credit Score") | [{"table": "customer_credit_rating_table", "column": "Credit Score"}] | [] | False |
| B2 | AVG(cr."Credit Limit") | [{"table": "customer_credit_rating_table", "column": "Credit Limit"}] | [] | False |


## S101

类别 `data`；来源 `query_db`；调用 `0cd7cde7bf2745a88710bae75fc69d57`；状态 `success`。

```sql
SELECT cr."Credit Grade", COUNT(*) as cnt, AVG(cr."Credit Score") as avg_score, AVG(cr."Credit Limit") as avg_limit
FROM customer_credit_rating_table cr 
JOIN (SELECT DISTINCT "Account ID" FROM transaction_history_table) t ON t."Account ID"=cr."Account ID"
GROUP BY cr."Credit Grade" ORDER BY cnt DESC
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-033/attempt-01/sql/S101.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-033/attempt-01/sql/S101.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-033/attempt-01/results/S101.rows.jsonl)；完整：True；SHA256：`f5a5a8f22b6b9abb1de43f15d8e08ad9094609ed131e595c722c9694bb870aee`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "transaction_history_table", "kind": "base", "block": null, "base_tables": ["transaction_history_table"]}] | [] | [] |
| B2 | [{"alias": "cr", "kind": "base", "block": null, "base_tables": ["customer_credit_rating_table"]}, {"alias": "t", "kind": "derived", "block": "B1", "base_tables": ["transaction_history_table"]}] | [{"type": "INNER", "right": "(SELECT DISTINCT \"Account ID\" FROM transaction_history_table) AS t", "on": "t.\"Account ID\" = cr.\"Account ID\"", "using": []}] | ["cr.\"Credit Grade\""] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B2 | COUNT(*) | [] | [] | True |
| B2 | AVG(cr."Credit Score") | [{"table": "customer_credit_rating_table", "column": "Credit Score"}] | [] | False |
| B2 | AVG(cr."Credit Limit") | [{"table": "customer_credit_rating_table", "column": "Credit Limit"}] | [] | False |


## S102

类别 `data`；来源 `query_db`；调用 `c97cd83f5ec748d5946dc77f7e81b3cf`；状态 `success`。

```sql
SELECT cr."Credit Grade", COUNT(*) as cnt_all, AVG(cr."Credit Score") as avg_score_all, AVG(cr."Credit Limit") as avg_limit_all
FROM customer_credit_rating_table cr 
GROUP BY cr."Credit Grade" ORDER BY cnt_all DESC
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-033/attempt-01/sql/S102.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-033/attempt-01/sql/S102.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-033/attempt-01/results/S102.rows.jsonl)；完整：True；SHA256：`c2fbb12a6029e6e733d4fa03b95ea21d3d3ad37c47bd5cfb69ce0255e5cb6434`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "cr", "kind": "base", "block": null, "base_tables": ["customer_credit_rating_table"]}] | [] | ["cr.\"Credit Grade\""] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |
| B1 | AVG(cr."Credit Score") | [{"table": "customer_credit_rating_table", "column": "Credit Score"}] | [] | False |
| B1 | AVG(cr."Credit Limit") | [{"table": "customer_credit_rating_table", "column": "Credit Limit"}] | [] | False |


## S103

类别 `data`；来源 `query_db`；调用 `3f8e4c36956b40f28248ca206f604cfd`；状态 `success`。

```sql
WITH hv AS (SELECT DISTINCT "Customer ID" FROM transaction_history_table WHERE "Transaction Payment Status"='Paid' GROUP BY "Customer ID" HAVING SUM("Transaction Amount")>5000)
SELECT AVG(f."Receivable Amount") as avg_recvbl, AVG(f."Amount Received") as avg_recvd, AVG(f."Outstanding Amount") as avg_out, AVG(f."Tax Amount") as avg_tax
FROM hv JOIN financials_table f ON hv."Customer ID"=f."Customer ID"
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-033/attempt-01/sql/S103.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-033/attempt-01/sql/S103.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-033/attempt-01/results/S103.rows.jsonl)；完整：True；SHA256：`970804c2ee7d654799f2384368afbc61253b960d1ecc98bb4440c47e6f58723b`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "transaction_history_table", "kind": "base", "block": null, "base_tables": ["transaction_history_table"]}] | [] | ["\"Customer ID\""] |
| B2 | [{"alias": "hv", "kind": "derived", "block": "B1", "base_tables": ["transaction_history_table"]}, {"alias": "f", "kind": "base", "block": null, "base_tables": ["financials_table"]}] | [{"type": "INNER", "right": "financials_table AS f", "on": "hv.\"Customer ID\" = f.\"Customer ID\"", "using": []}] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | SUM("Transaction Amount") | [{"table": "transaction_history_table", "column": "Transaction Amount"}] | [] | False |
| B2 | AVG(f."Receivable Amount") | [{"table": "financials_table", "column": "Receivable Amount"}] | [] | False |
| B2 | AVG(f."Amount Received") | [{"table": "financials_table", "column": "Amount Received"}] | [] | False |
| B2 | AVG(f."Outstanding Amount") | [{"table": "financials_table", "column": "Outstanding Amount"}] | [] | False |
| B2 | AVG(f."Tax Amount") | [{"table": "financials_table", "column": "Tax Amount"}] | [] | False |


## S104

类别 `data`；来源 `query_db`；调用 `b0f5174509d548d1b772a4be8272808a`；状态 `success`。

```sql
SELECT AVG("Receivable Amount") as avg_recvbl_all, AVG("Amount Received") as avg_recvd_all, AVG("Outstanding Amount") as avg_out_all, AVG("Tax Amount") as avg_tax_all FROM financials_table
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-033/attempt-01/sql/S104.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-033/attempt-01/sql/S104.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-033/attempt-01/results/S104.rows.jsonl)；完整：True；SHA256：`c85b7e273f918fc2a4cbfee1d59624ea00700fb7f543aa4c1f71898b784bd142`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "financials_table", "kind": "base", "block": null, "base_tables": ["financials_table"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | AVG("Receivable Amount") | [{"table": "financials_table", "column": "Receivable Amount"}] | [] | False |
| B1 | AVG("Amount Received") | [{"table": "financials_table", "column": "Amount Received"}] | [] | False |
| B1 | AVG("Outstanding Amount") | [{"table": "financials_table", "column": "Outstanding Amount"}] | [] | False |
| B1 | AVG("Tax Amount") | [{"table": "financials_table", "column": "Tax Amount"}] | [] | False |


## S105

类别 `data`；来源 `query_db`；调用 `48e86d6c028c48f5811ed8d8b320af02`；状态 `success`。

```sql
WITH hv AS (SELECT DISTINCT "Customer ID" FROM transaction_history_table WHERE "Transaction Payment Status"='Paid' GROUP BY "Customer ID" HAVING SUM("Transaction Amount")>5000)
SELECT t."Transaction Currency", COUNT(*) as cnt, SUM(t."Transaction Amount") as total_amt
FROM hv JOIN transaction_history_table t ON hv."Customer ID"=t."Customer ID" AND t."Transaction Payment Status"='Paid'
GROUP BY t."Transaction Currency"
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-033/attempt-01/sql/S105.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-033/attempt-01/sql/S105.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-033/attempt-01/results/S105.rows.jsonl)；完整：True；SHA256：`096a82065cba128e9e7914c42885c45bcf859dc9ba1a8aadb422ef4412290afe`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "transaction_history_table", "kind": "base", "block": null, "base_tables": ["transaction_history_table"]}] | [] | ["\"Customer ID\""] |
| B2 | [{"alias": "hv", "kind": "derived", "block": "B1", "base_tables": ["transaction_history_table"]}, {"alias": "t", "kind": "base", "block": null, "base_tables": ["transaction_history_table"]}] | [{"type": "INNER", "right": "transaction_history_table AS t", "on": "hv.\"Customer ID\" = t.\"Customer ID\" AND t.\"Transaction Payment Status\" = 'Paid'", "using": []}] | ["t.\"Transaction Currency\""] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | SUM("Transaction Amount") | [{"table": "transaction_history_table", "column": "Transaction Amount"}] | [] | False |
| B2 | COUNT(*) | [] | [] | True |
| B2 | SUM(t."Transaction Amount") | [{"table": "transaction_history_table", "column": "Transaction Amount"}] | [] | False |


## S106

类别 `data`；来源 `query_db`；调用 `c3759fd8aeb94b33a61230ba38e482ca`；状态 `success`。

```sql
SELECT DISTINCT "Transaction Currency" FROM transaction_history_table
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-033/attempt-01/sql/S106.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-033/attempt-01/sql/S106.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-033/attempt-01/results/S106.rows.jsonl)；完整：True；SHA256：`2915b3cd07659e21ad4e853c2a63356808e69ea7a59887aa664fb4df32f1b363`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "transaction_history_table", "kind": "base", "block": null, "base_tables": ["transaction_history_table"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |


## S107

类别 `data`；来源 `query_db`；调用 `22816de277a8452f83ff6c379664014e`；状态 `success`。

```sql
WITH hv AS (SELECT DISTINCT "Customer ID" FROM transaction_history_table WHERE "Transaction Payment Status"='Paid' GROUP BY "Customer ID" HAVING SUM("Transaction Amount")>5000)
SELECT d."Device Type", COUNT(*) as cnt FROM hv JOIN customer_device_table d ON hv."Customer ID"=d."Customer ID" GROUP BY d."Device Type" ORDER BY cnt DESC
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-033/attempt-01/sql/S107.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-033/attempt-01/sql/S107.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-033/attempt-01/results/S107.rows.jsonl)；完整：True；SHA256：`ddb8020fe2a6680ac03f299c77957176202699d7e4d2a96060cdad0ed815cbb9`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "transaction_history_table", "kind": "base", "block": null, "base_tables": ["transaction_history_table"]}] | [] | ["\"Customer ID\""] |
| B2 | [{"alias": "hv", "kind": "derived", "block": "B1", "base_tables": ["transaction_history_table"]}, {"alias": "d", "kind": "base", "block": null, "base_tables": ["customer_device_table"]}] | [{"type": "INNER", "right": "customer_device_table AS d", "on": "hv.\"Customer ID\" = d.\"Customer ID\"", "using": []}] | ["d.\"Device Type\""] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | SUM("Transaction Amount") | [{"table": "transaction_history_table", "column": "Transaction Amount"}] | [] | False |
| B2 | COUNT(*) | [] | [] | True |


## S108

类别 `data`；来源 `query_db`；调用 `c216be1407d64e0eb74d43187e942893`；状态 `success`。

```sql
SELECT "Device Type", COUNT(*) as cnt FROM customer_device_table GROUP BY "Device Type" ORDER BY cnt DESC
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-033/attempt-01/sql/S108.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-033/attempt-01/sql/S108.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-033/attempt-01/results/S108.rows.jsonl)；完整：True；SHA256：`700ff2385d36db6def4510048cb0bb4d290c5e5a4e408cc2972d2f819779e4a4`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "customer_device_table", "kind": "base", "block": null, "base_tables": ["customer_device_table"]}] | [] | ["\"Device Type\""] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |


## S109

类别 `data`；来源 `query_db`；调用 `5c9dec7d3ea34a7ca2ea5dc44d5f3fac`；状态 `success`。

```sql
WITH hv AS (SELECT DISTINCT "Customer ID" FROM transaction_history_table WHERE "Transaction Payment Status"='Paid' GROUP BY "Customer ID" HAVING SUM("Transaction Amount")>5000)
SELECT p."Role Name", COUNT(*) as cnt FROM hv JOIN permissions_table p ON hv."Customer ID"=p."Customer ID" GROUP BY p."Role Name" ORDER BY cnt DESC
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-033/attempt-01/sql/S109.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-033/attempt-01/sql/S109.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-033/attempt-01/results/S109.rows.jsonl)；完整：True；SHA256：`194233f016a9cab992ffb51ed4c6a392e140fb9d3a5abfbe0afce5836a50038a`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "transaction_history_table", "kind": "base", "block": null, "base_tables": ["transaction_history_table"]}] | [] | ["\"Customer ID\""] |
| B2 | [{"alias": "hv", "kind": "derived", "block": "B1", "base_tables": ["transaction_history_table"]}, {"alias": "p", "kind": "base", "block": null, "base_tables": ["permissions_table"]}] | [{"type": "INNER", "right": "permissions_table AS p", "on": "hv.\"Customer ID\" = p.\"Customer ID\"", "using": []}] | ["p.\"Role Name\""] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | SUM("Transaction Amount") | [{"table": "transaction_history_table", "column": "Transaction Amount"}] | [] | False |
| B2 | COUNT(*) | [] | [] | True |


## S110

类别 `data`；来源 `query_db`；调用 `92185674d09642e488a71469dda67fe1`；状态 `success`。

```sql
SELECT "Role Name", COUNT(*) as cnt FROM permissions_table GROUP BY "Role Name" ORDER BY cnt DESC
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-033/attempt-01/sql/S110.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-033/attempt-01/sql/S110.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-033/attempt-01/results/S110.rows.jsonl)；完整：True；SHA256：`87569890ed7532f5632a9a672ebc06021f919e2ce0891b637e7a84d8328ebc41`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "permissions_table", "kind": "base", "block": null, "base_tables": ["permissions_table"]}] | [] | ["\"Role Name\""] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |


## S111

类别 `data`；来源 `query_db`；调用 `e2f1a859ec4240fdb3b57e340774a9d4`；状态 `success`。

```sql
WITH hv AS (SELECT DISTINCT "Customer ID" FROM transaction_history_table WHERE "Transaction Payment Status"='Paid' GROUP BY "Customer ID" HAVING SUM("Transaction Amount")>5000)
SELECT cp."Event Participation Prize Level", COUNT(*) as cnt FROM hv JOIN campaign_participation_table cp ON hv."Customer ID"=cp."Event Participant Contact ID" GROUP BY cp."Event Participation Prize Level" ORDER BY cnt DESC
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-033/attempt-01/sql/S111.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-033/attempt-01/sql/S111.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-033/attempt-01/results/S111.rows.jsonl)；完整：True；SHA256：`e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "transaction_history_table", "kind": "base", "block": null, "base_tables": ["transaction_history_table"]}] | [] | ["\"Customer ID\""] |
| B2 | [{"alias": "hv", "kind": "derived", "block": "B1", "base_tables": ["transaction_history_table"]}, {"alias": "cp", "kind": "base", "block": null, "base_tables": ["campaign_participation_table"]}] | [{"type": "INNER", "right": "campaign_participation_table AS cp", "on": "hv.\"Customer ID\" = cp.\"Event Participant Contact ID\"", "using": []}] | ["cp.\"Event Participation Prize Level\""] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | SUM("Transaction Amount") | [{"table": "transaction_history_table", "column": "Transaction Amount"}] | [] | False |
| B2 | COUNT(*) | [] | [] | True |


## S112

类别 `data`；来源 `query_db`；调用 `7387828c0c16444e9cc3d8526f70815d`；状态 `success`。

```sql
SELECT "Event Participation Prize Level", COUNT(*) as cnt FROM campaign_participation_table GROUP BY "Event Participation Prize Level"
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-033/attempt-01/sql/S112.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-033/attempt-01/sql/S112.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-033/attempt-01/results/S112.rows.jsonl)；完整：True；SHA256：`a39c4cee7f60837da9da826096a179560d750d1151f3e066d849b89df09a8158`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "campaign_participation_table", "kind": "base", "block": null, "base_tables": ["campaign_participation_table"]}] | [] | ["\"Event Participation Prize Level\""] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |


## S113

类别 `data`；来源 `query_db`；调用 `96e750e0c81948a58f95808810ee1d2e`；状态 `success`。

```sql
WITH hv AS (SELECT DISTINCT "Customer ID" FROM transaction_history_table WHERE "Transaction Payment Status"='Paid' GROUP BY "Customer ID" HAVING SUM("Transaction Amount")>5000)
SELECT cf."Satisfaction Rating", COUNT(*) as cnt FROM hv JOIN customer_feedback_table cf ON hv."Customer ID"=cf."Contact ID" GROUP BY cf."Satisfaction Rating"
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-033/attempt-01/sql/S113.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-033/attempt-01/sql/S113.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-033/attempt-01/results/S113.rows.jsonl)；完整：True；SHA256：`e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "transaction_history_table", "kind": "base", "block": null, "base_tables": ["transaction_history_table"]}] | [] | ["\"Customer ID\""] |
| B2 | [{"alias": "hv", "kind": "derived", "block": "B1", "base_tables": ["transaction_history_table"]}, {"alias": "cf", "kind": "base", "block": null, "base_tables": ["customer_feedback_table"]}] | [{"type": "INNER", "right": "customer_feedback_table AS cf", "on": "hv.\"Customer ID\" = cf.\"Contact ID\"", "using": []}] | ["cf.\"Satisfaction Rating\""] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | SUM("Transaction Amount") | [{"table": "transaction_history_table", "column": "Transaction Amount"}] | [] | False |
| B2 | COUNT(*) | [] | [] | True |


## S114

类别 `data`；来源 `query_db`；调用 `082874dc176b45a5a784e452b8642691`；状态 `success`。

```sql
SELECT "Satisfaction Rating", COUNT(*) as cnt FROM customer_feedback_table GROUP BY "Satisfaction Rating"
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-033/attempt-01/sql/S114.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-033/attempt-01/sql/S114.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-033/attempt-01/results/S114.rows.jsonl)；完整：True；SHA256：`c8c0c2d3b73ffa83f084633c1524c9c88c1e5df26687deab347475adfb206e98`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "customer_feedback_table", "kind": "base", "block": null, "base_tables": ["customer_feedback_table"]}] | [] | ["\"Satisfaction Rating\""] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |


## S115

类别 `data`；来源 `query_db`；调用 `24cfe74f0596467cb4d9865ebd5609ee`；状态 `success`。

```sql
SELECT SUBSTR("Contact",1,1) as prefix, LENGTH("Contact") as len, COUNT(*) as cnt FROM customer_contact_table GROUP BY prefix, len
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-033/attempt-01/sql/S115.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-033/attempt-01/sql/S115.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-033/attempt-01/results/S115.rows.jsonl)；完整：True；SHA256：`84b1836681c4fb16421300a11e1a69e11601dcbfe50b5f620011f3fa29bc6213`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "customer_contact_table", "kind": "base", "block": null, "base_tables": ["customer_contact_table"]}] | [] | ["SUBSTRING(\"Contact\", 1, 1)", "LENGTH(\"Contact\")"] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |


## S116

类别 `data`；来源 `query_db`；调用 `fe7baeb22dfe4672832f8914fd7e84d4`；状态 `success`。

```sql
SELECT SUBSTR("Event Participant Contact ID",1,1) as prefix, LENGTH("Event Participant Contact ID") as len, COUNT(*) as cnt FROM campaign_participation_table GROUP BY prefix, len
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-033/attempt-01/sql/S116.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-033/attempt-01/sql/S116.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-033/attempt-01/results/S116.rows.jsonl)；完整：True；SHA256：`8e574cac17abf0f3a71a4faa597e73024b0f36defe34202bc8b7a409b8c511fd`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "campaign_participation_table", "kind": "base", "block": null, "base_tables": ["campaign_participation_table"]}] | [] | ["SUBSTRING(\"Event Participant Contact ID\", 1, 1)", "LENGTH(\"Event Participant Contact ID\")"] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |


## S117

类别 `data`；来源 `query_db`；调用 `6c8038f50b394b55a06daa1ae3e349c3`；状态 `success`。

```sql
SELECT SUBSTR("Contact ID",1,1) as prefix, LENGTH("Contact ID") as len, COUNT(*) as cnt FROM customer_feedback_table GROUP BY prefix, len
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-033/attempt-01/sql/S117.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-033/attempt-01/sql/S117.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-033/attempt-01/results/S117.rows.jsonl)；完整：True；SHA256：`e03c60d1d0f7f97b4a066f6e5e7ae3ee783337324a600f7aac1705af44077140`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "customer_feedback_table", "kind": "base", "block": null, "base_tables": ["customer_feedback_table"]}] | [] | ["SUBSTRING(\"Contact ID\", 1, 1)", "LENGTH(\"Contact ID\")"] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |


## S118

类别 `data`；来源 `query_db`；调用 `3a9da28a37424f068f9a3d7d590b47bb`；状态 `success`。

```sql
SELECT SUBSTR("Contact ID",1,1) as prefix, LENGTH("Contact ID") as len, COUNT(*) as cnt FROM customer_tag_table GROUP BY prefix, len
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-033/attempt-01/sql/S118.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-033/attempt-01/sql/S118.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-033/attempt-01/results/S118.rows.jsonl)；完整：True；SHA256：`3979081ec6988ea05a7bf815ceff2f060f87cd185251e28ac7f19aeb65ddb91d`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "customer_tag_table", "kind": "base", "block": null, "base_tables": ["customer_tag_table"]}] | [] | ["SUBSTRING(\"Contact ID\", 1, 1)", "LENGTH(\"Contact ID\")"] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |


## S119

类别 `data`；来源 `query_db`；调用 `8ff1c8d7ca79421d887d83ae2b69f1f4`；状态 `success`。

```sql
SELECT COUNT(*) as cnt FROM (SELECT DISTINCT "Contact ID" FROM customer_feedback_table) f JOIN (SELECT DISTINCT "Contact ID", "Customer ID" FROM customer_tag_table) t ON f."Contact ID"=t."Contact ID"
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-033/attempt-01/sql/S119.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-033/attempt-01/sql/S119.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-033/attempt-01/results/S119.rows.jsonl)；完整：True；SHA256：`bd5ab910797f6a7d932afeb94e81a6bf37b981ba27641c7fd70ef27d0dd10922`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "customer_feedback_table", "kind": "base", "block": null, "base_tables": ["customer_feedback_table"]}] | [] | [] |
| B2 | [{"alias": "customer_tag_table", "kind": "base", "block": null, "base_tables": ["customer_tag_table"]}] | [] | [] |
| B3 | [{"alias": "f", "kind": "derived", "block": "B1", "base_tables": ["customer_feedback_table"]}, {"alias": "t", "kind": "derived", "block": "B2", "base_tables": ["customer_tag_table"]}] | [{"type": "INNER", "right": "(SELECT DISTINCT \"Contact ID\", \"Customer ID\" FROM customer_tag_table) AS t", "on": "f.\"Contact ID\" = t.\"Contact ID\"", "using": []}] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B3 | COUNT(*) | [] | [] | True |


## S120

类别 `data`；来源 `query_db`；调用 `e12bba09320940d982ca787fce48afe3`；状态 `success`。

```sql
WITH hv AS (SELECT DISTINCT "Customer ID" FROM transaction_history_table WHERE "Transaction Payment Status"='Paid' GROUP BY "Customer ID" HAVING SUM("Transaction Amount")>5000)
SELECT cf."Satisfaction Rating", COUNT(*) as cnt
FROM hv 
JOIN customer_tag_table t ON hv."Customer ID"=t."Customer ID"
JOIN customer_feedback_table cf ON t."Contact ID"=cf."Contact ID"
GROUP BY cf."Satisfaction Rating"
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-033/attempt-01/sql/S120.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-033/attempt-01/sql/S120.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-033/attempt-01/results/S120.rows.jsonl)；完整：True；SHA256：`eaf8bbf476aad49af725ae0f355b3d21703820e02a28bde5e26950421f6bf299`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "transaction_history_table", "kind": "base", "block": null, "base_tables": ["transaction_history_table"]}] | [] | ["\"Customer ID\""] |
| B2 | [{"alias": "hv", "kind": "derived", "block": "B1", "base_tables": ["transaction_history_table"]}, {"alias": "t", "kind": "base", "block": null, "base_tables": ["customer_tag_table"]}, {"alias": "cf", "kind": "base", "block": null, "base_tables": ["customer_feedback_table"]}] | [{"type": "INNER", "right": "customer_tag_table AS t", "on": "hv.\"Customer ID\" = t.\"Customer ID\"", "using": []}, {"type": "INNER", "right": "customer_feedback_table AS cf", "on": "t.\"Contact ID\" = cf.\"Contact ID\"", "using": []}] | ["cf.\"Satisfaction Rating\""] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | SUM("Transaction Amount") | [{"table": "transaction_history_table", "column": "Transaction Amount"}] | [] | False |
| B2 | COUNT(*) | [] | [] | True |


## S121

类别 `data`；来源 `query_db`；调用 `6459e9fe0c9144b3b37ce37779673576`；状态 `success`。

```sql
SELECT COUNT(*) as cnt FROM (SELECT "Customer ID" FROM customer_contact_table) c JOIN (SELECT DISTINCT "Customer ID" FROM customer_tag_table) t ON c."Customer ID"=t."Customer ID"
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-033/attempt-01/sql/S121.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-033/attempt-01/sql/S121.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-033/attempt-01/results/S121.rows.jsonl)；完整：True；SHA256：`25e589b97fd5838c45891ad685c9729748a85db8f893020e3b90271cb6ce740f`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "customer_contact_table", "kind": "base", "block": null, "base_tables": ["customer_contact_table"]}] | [] | [] |
| B2 | [{"alias": "customer_tag_table", "kind": "base", "block": null, "base_tables": ["customer_tag_table"]}] | [] | [] |
| B3 | [{"alias": "c", "kind": "derived", "block": "B1", "base_tables": ["customer_contact_table"]}, {"alias": "t", "kind": "derived", "block": "B2", "base_tables": ["customer_tag_table"]}] | [{"type": "INNER", "right": "(SELECT DISTINCT \"Customer ID\" FROM customer_tag_table) AS t", "on": "c.\"Customer ID\" = t.\"Customer ID\"", "using": []}] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B3 | COUNT(*) | [] | [] | True |


## S122

类别 `data`；来源 `query_db`；调用 `dcf215b9f75d41e7ab4e6092272a67e3`；状态 `success`。

```sql
WITH hv AS (SELECT DISTINCT "Customer ID" FROM transaction_history_table WHERE "Transaction Payment Status"='Paid' GROUP BY "Customer ID" HAVING SUM("Transaction Amount")>5000)
SELECT cp."Event Participation Prize Level", COUNT(*) as cnt
FROM hv 
JOIN customer_tag_table t ON hv."Customer ID"=t."Customer ID"
JOIN campaign_participation_table cp ON t."Contact ID"=cp."Event Participant Contact ID"
GROUP BY cp."Event Participation Prize Level"
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-033/attempt-01/sql/S122.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-033/attempt-01/sql/S122.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-033/attempt-01/results/S122.rows.jsonl)；完整：True；SHA256：`e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "transaction_history_table", "kind": "base", "block": null, "base_tables": ["transaction_history_table"]}] | [] | ["\"Customer ID\""] |
| B2 | [{"alias": "hv", "kind": "derived", "block": "B1", "base_tables": ["transaction_history_table"]}, {"alias": "t", "kind": "base", "block": null, "base_tables": ["customer_tag_table"]}, {"alias": "cp", "kind": "base", "block": null, "base_tables": ["campaign_participation_table"]}] | [{"type": "INNER", "right": "customer_tag_table AS t", "on": "hv.\"Customer ID\" = t.\"Customer ID\"", "using": []}, {"type": "INNER", "right": "campaign_participation_table AS cp", "on": "t.\"Contact ID\" = cp.\"Event Participant Contact ID\"", "using": []}] | ["cp.\"Event Participation Prize Level\""] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | SUM("Transaction Amount") | [{"table": "transaction_history_table", "column": "Transaction Amount"}] | [] | False |
| B2 | COUNT(*) | [] | [] | True |

