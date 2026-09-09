# dacomp-035

The company is conducting a special initiative on office system security governance. Based…

运行：已提交。官方未评分。全部 SQL 尝试/成功 82/82；数据 SQL 80/80；Python 5 次。

完整原题：

The company is conducting a special initiative on office system security governance. Based on historical data (e.g., abnormal login data), please help analyze which departments have relatively weak security awareness and need prioritized strengthening of security awareness guidance.

| 表 | 行数 | 列数 |
| --- | --- | --- |
| abnormal_logins_table | 414 | 12 |
| authentication_methods_table | 692 | 16 |
| ip_address_information_table | 474 | 12 |
| login_records_table | 487 | 17 |
| menu_access_table | 375 | 13 |
| network_connections_table | 416 | 13 |
| security_events_table | 350 | 13 |
| system_logs_table | 416 | 12 |
| user_account_table | 307 | 15 |
| user_information_table | 661 | 14 |
| user_operations_table | 471 | 10 |
| user_permissions_table | 416 | 9 |


实际路线（分析者依据 SQL/源码概括，不代表 Agent 自述）：关联部门、用户、登录与异常安全事件 → 汇总风险分布和重复异常 → Python 合并部门摘要并检验群体差异 → 绘制重点部门对比。

数据库大小：1,777,664 字节。

## 数据 SQL

| SQL | 状态 | 基础表 | Join 输入/类型 | GROUP BY | 聚合表达式 | 结果行数 | 数据库 ms |
| --- | --- | --- | --- | --- | --- | --- | --- |
| [S3/Q1](#s3) | success | ["abnormal_logins_table"] | 0 / {} | [] | ["COUNT(*)"] | 1 | 0.336 |
| [S4/Q2](#s4) | success | ["abnormal_logins_table"] | 0 / {} | [] | [] | 20 | 0.386 |
| [S5/Q3](#s5) | success | ["user_information_table"] | 0 / {} | [] | [] | 20 | 0.433 |
| [S6/Q4](#s6) | success | ["login_records_table"] | 0 / {} | [] | [] | 20 | 0.44 |
| [S7/Q5](#s7) | success | ["user_information_table"] | 0 / {} | [] | [] | 4 | 0.652 |
| [S8/Q6](#s8) | success | ["user_information_table"] | 0 / {} | [] | ["COUNT(DISTINCT \"User ID\")"] | 1 | 0.739 |
| [S9/Q7](#s9) | success | ["login_records_table"] | 0 / {} | [] | ["COUNT(DISTINCT \"Login Record ID\")"] | 1 | 0.696 |
| [S10/Q8](#s10) | success | ["abnormal_logins_table"] | 0 / {} | [] | [] | 4 | 0.512 |
| [S11/Q9](#s11) | success | ["abnormal_logins_table"] | 0 / {} | [] | [] | 4 | 0.406 |
| [S12/Q10](#s12) | success | ["user_information_table"] | 0 / {} | ["Department"] | ["COUNT(*)"] | 4 | 0.841 |
| [S13/Q11](#s13) | success | ["abnormal_logins_table"] | 0 / {} | [] | [] | 2 | 0.479 |
| [S14/Q12](#s14) | success | ["abnormal_logins_table", "login_records_table", "user_information_table"] | 3 / {'INNER': 2} | ["u.Department"] | ["COUNT(DISTINCT a.\"Anomaly ID\")", "COUNT(DISTINCT a.\"Login Record ID\")", "COUNT(DISTINCT u.\"User ID\")", "AVG(a.\"Anomaly Score\")", "AVG(a.\"Device Anomaly Indicators\")", "AVG(a.\"Network Anomaly Indicators\")", "AVG(a.\"Behavior Anomaly Indicators\")"] | 4 | 2.506 |
| [S15/Q13](#s15) | success | ["abnormal_logins_table", "login_records_table", "user_information_table"] | 3 / {'INNER': 2} | ["u.Department", "a.\"Risk Level\""] | ["COUNT(*)"] | 16 | 1.919 |
| [S16/Q14](#s16) | success | ["abnormal_logins_table", "login_records_table", "user_information_table"] | 3 / {'INNER': 2} | ["u.Department", "a.\"Anomaly Type\""] | ["COUNT(*)"] | 16 | 1.942 |
| [S17/Q15](#s17) | success | ["abnormal_logins_table", "login_records_table", "user_information_table"] | 3 / {'INNER': 2} | ["u.Department", "a.\"Risk Level\""] | ["COUNT(*)"] | 4 | 1.421 |
| [S18/Q16](#s18) | success | ["abnormal_logins_table", "login_records_table", "user_information_table"] | 3 / {'INNER': 2} | ["u.Department", "a.\"Anomaly Type\""] | ["COUNT(*)"] | 4 | 1.378 |
| [S19/Q17](#s19) | success | ["login_records_table"] | 0 / {} | ["l.\"Authentication Status\""] | ["COUNT(*)"] | 2 | 0.489 |
| [S20/Q18](#s20) | success | ["login_records_table"] | 0 / {} | ["l.\"Two-Factor Authentication Status\""] | ["COUNT(*)"] | 2 | 0.49 |
| [S21/Q19](#s21) | success | ["login_records_table", "user_information_table"] | 2 / {'INNER': 1} | ["u.Department"] | ["COUNT(*)", "SUM(CASE WHEN l.\"Authentication Status\" = 'Failure' THEN 1 ELSE 0 END)", "SUM(CASE WHEN l.\"Two-Factor Authentication Status\" = 'Not Enabled' THEN 1 ELSE 0 END)", "COUNT(*)", "COUNT(*)", "SUM(CASE WHEN l.\"Authentication Status\" = 'Failure' THEN 1 ELSE 0 END)", "SUM(CASE WHEN l.\"Two-Factor Authentication Status\" = 'Not Enabled' THEN 1 ELSE 0 END)"] | 4 | 1.463 |
| [S22/Q20](#s22) | success | ["user_account_table", "user_information_table"] | 2 / {'INNER': 1} | ["u.Department"] | ["AVG(ua.\"Password Attempt Count\")", "SUM(CASE WHEN ua.\"Account Lock Status\" = 'Locked' THEN 1 ELSE 0 END)", "COUNT(DISTINCT ua.\"Account ID\")", "SUM(CASE WHEN ua.\"Password Status\" = 'Expired' THEN 1 ELSE 0 END)"] | 4 | 1.436 |
| [S23/Q21](#s23) | success | ["login_records_table", "security_events_table", "user_information_table"] | 3 / {'INNER': 2} | ["u.Department"] | ["COUNT(*)", "SUM(CASE WHEN se.\"Severity\" = 'High' OR se.\"Severity\" = 'Critical' OR se.\"Severity\" = 'Severe' THEN 1 ELSE 0 END)", "AVG(se.\"Risk Score\")"] | 4 | 1.886 |
| [S24/Q22](#s24) | success | ["security_events_table"] | 0 / {} | [] | [] | 4 | 0.3 |
| [S25/Q23](#s25) | success | ["security_events_table"] | 0 / {} | [] | ["COUNT(*)"] | 1 | 0.229 |
| [S26/Q24](#s26) | success | ["abnormal_logins_table", "login_records_table", "user_information_table"] | 3 / {'INNER': 2} | ["u.Department", "a.\"Confirmation Status\""] | ["COUNT(*)"] | 8 | 1.938 |
| [S27/Q25](#s27) | success | ["abnormal_logins_table", "login_records_table", "user_information_table"] | 3 / {'INNER': 1, 'LEFT': 1} | ["u.Department"] | ["COUNT(DISTINCT l.\"User ID\")", "COUNT(DISTINCT l.\"Login Record ID\")", "COUNT(DISTINCT l.\"Login Record ID\")", "COUNT(DISTINCT a.\"Login Record ID\")"] | 4 | 2.367 |
| [S28/Q26](#s28) | success | ["abnormal_logins_table", "login_records_table", "user_information_table"] | 2 / {'INNER': 2} | ["l.\"User ID\"", "u.Department", "CASE WHEN user_anomaly_count.anomaly_count >= 2 THEN 'Multiple' ELSE 'Single' END"] | ["COUNT(*)", "COUNT(DISTINCT u.\"User ID\")", "SUM(user_anomaly_count.anomaly_count)"] | 8 | 1.901 |
| [S29/Q27](#s29) | success | ["abnormal_logins_table", "login_records_table", "user_information_table"] | 3 / {'INNER': 2} | ["u.Department", "a.\"Risk Level\"", "a.\"Confirmation Status\""] | ["COUNT(*)"] | 16 | 1.718 |
| [S30/Q28](#s30) | success | ["abnormal_logins_table", "login_records_table", "user_information_table"] | 3 / {'INNER': 2} | ["u.Department", "a.\"Risk Level\"", "a.\"Confirmation Status\""] | ["COUNT(*)"] | 4 | 1.25 |
| [S31/Q29](#s31) | success | ["abnormal_logins_table", "login_records_table", "user_information_table"] | 3 / {'INNER': 2} | ["u.Department", "a.\"Anomaly Features\""] | ["COUNT(*)"] | 16 | 1.885 |
| [S32/Q30](#s32) | success | ["abnormal_logins_table", "login_records_table", "user_information_table"] | 3 / {'INNER': 2} | ["u.Department", "a.\"Anomaly Features\""] | ["COUNT(*)"] | 4 | 1.33 |
| [S33/Q31](#s33) | success | ["abnormal_logins_table", "login_records_table", "user_information_table"] | 3 / {'INNER': 2} | ["u.Department"] | ["AVG(a.\"Anomaly Score\")", "AVG(CASE WHEN a.\"Risk Level\" IN ('High', 'Severe') THEN a.\"Anomaly Score\" ELSE NULL END)", "COUNT(*)", "COUNT(*)", "SUM(CASE WHEN a.\"Risk Level\" IN ('High', 'Severe') THEN 1 ELSE 0 END)", "SUM(CASE WHEN a.\"Confirmation Status\" = 'Confirmed' THEN 1 ELSE 0 END)"] | 4 | 2.125 |
| [S34/Q32](#s34) | success | ["login_records_table", "system_logs_table", "user_information_table"] | 3 / {'INNER': 2} | ["u.Department", "sl.\"Log Level\""] | ["COUNT(*)"] | 12 | 1.917 |
| [S35/Q33](#s35) | success | ["system_logs_table"] | 0 / {} | [] | [] | 3 | 0.394 |
| [S36/Q34](#s36) | success | ["system_logs_table"] | 0 / {} | [] | [] | 3 | 0.374 |
| [S37/Q35](#s37) | success | ["login_records_table", "network_connections_table", "user_information_table"] | 3 / {'INNER': 2} | ["u.Department", "nc.\"VPN Status\"", "nc.\"Proxy Status\"", "nc.\"Firewall Status\""] | ["COUNT(*)"] | 32 | 2.115 |
| [S38/Q36](#s38) | success | ["network_connections_table"] | 0 / {} | [] | [] | 2 | 0.301 |
| [S39/Q37](#s39) | success | ["login_records_table", "network_connections_table", "user_information_table"] | 3 / {'INNER': 2} | ["u.Department"] | ["COUNT(*)", "SUM(CASE WHEN nc.\"VPN Status\" = 'Not Connected' THEN 1 ELSE 0 END)", "SUM(CASE WHEN nc.\"Proxy Status\" = 'Closed' THEN 1 ELSE 0 END)", "SUM(CASE WHEN nc.\"Firewall Status\" = 'Closed' THEN 1 ELSE 0 END)", "COUNT(*)", "COUNT(*)", "SUM(CASE WHEN nc.\"VPN Status\" = 'Not Connected' THEN 1 ELSE 0 END)", "SUM(CASE WHEN nc.\"Firewall Status\" = 'Closed' THEN 1 ELSE 0 END)"] | 4 | 3.282 |
| [S40/Q38](#s40) | success | ["login_records_table", "user_information_table"] | 2 / {'INNER': 1} | ["u.Department", "l.\"Login Method\""] | ["COUNT(*)"] | 16 | 1.522 |
| [S41/Q39](#s41) | success | ["login_records_table", "user_information_table"] | 2 / {'INNER': 1} | ["u.Department", "l.\"Authentication Level\""] | ["COUNT(*)"] | 12 | 1.509 |
| [S42/Q40](#s42) | success | ["ip_address_information_table", "login_records_table", "user_information_table"] | 3 / {'INNER': 2} | ["u.Department", "ip.\"Province\""] | ["COUNT(*)"] | 40 | 2.257 |
| [S43/Q41](#s43) | success | ["user_information_table"] | 0 / {} | ["Department"] | ["COUNT(*)"] | 4 | 0.644 |
| [S44/Q42](#s44) | success | ["abnormal_logins_table", "login_records_table", "user_information_table"] | 3 / {'INNER': 2} | ["u.Department"] | ["COUNT(*)", "COUNT(DISTINCT l.\"User ID\")", "AVG(a.\"Anomaly Score\")", "AVG(a.\"Device Anomaly Indicators\")", "AVG(a.\"Network Anomaly Indicators\")", "AVG(a.\"Behavior Anomaly Indicators\")", "COUNT(*)", "COUNT(*)", "SUM(CASE WHEN a.\"Risk Level\" IN ('High', 'Severe') THEN 1 ELSE 0 END)", "SUM(CASE WHEN a.\"Confirmation Status\" = 'Confirmed' THEN 1 ELSE 0 END)"] | 4 | 2.27 |
| [S45/Q43](#s45) | success | ["abnormal_logins_table", "login_records_table", "user_information_table"] | 2 / {'INNER': 2} | ["l.\"User ID\"", "u.Department"] | ["COUNT(*)", "COUNT(DISTINCT CASE WHEN ua.anomaly_count >= 2 THEN u.\"User ID\" ELSE NULL END)", "SUM(CASE WHEN ua.anomaly_count >= 2 THEN ua.anomaly_count ELSE 0 END)"] | 4 | 1.64 |
| [S46/Q44](#s46) | success | ["login_records_table", "user_information_table"] | 2 / {'INNER': 1} | ["u.Department"] | ["COUNT(*)", "SUM(CASE WHEN l.\"Authentication Status\" = 'Failure' THEN 1 ELSE 0 END)", "SUM(CASE WHEN l.\"Two-Factor Authentication Status\" = 'Not Enabled' THEN 1 ELSE 0 END)", "COUNT(DISTINCT l.\"User ID\")"] | 4 | 1.39 |
| [S47/Q45](#s47) | success | ["user_account_table", "user_information_table"] | 2 / {'INNER': 1} | ["u.Department"] | ["AVG(ua.\"Password Attempt Count\")", "SUM(CASE WHEN ua.\"Account Lock Status\" = 'Locked' THEN 1 ELSE 0 END)", "COUNT(*)"] | 4 | 1.072 |
| [S48/Q46](#s48) | success | ["login_records_table", "security_events_table", "user_information_table"] | 3 / {'INNER': 2} | ["u.Department"] | ["COUNT(*)", "SUM(CASE WHEN se.\"Severity\" IN ('High', 'Severe') THEN 1 ELSE 0 END)", "AVG(se.\"Risk Score\")"] | 4 | 1.593 |
| [S49/Q47](#s49) | success | ["user_information_table"] | 0 / {} | ["Department"] | ["COUNT(*)"] | 4 | 0.553 |
| [S50/Q48](#s50) | success | ["abnormal_logins_table", "login_records_table", "user_information_table"] | 3 / {'INNER': 2} | ["u.Department"] | ["COUNT(*)"] | 4 | 1.861 |
| [S51/Q49](#s51) | success | ["abnormal_logins_table", "login_records_table", "user_information_table"] | 3 / {'INNER': 2} | ["u.Department", "a.\"Risk Level\""] | ["COUNT(*)"] | 16 | 1.83 |
| [S52/Q50](#s52) | success | ["abnormal_logins_table", "login_records_table", "user_information_table"] | 3 / {'INNER': 2} | ["u.Department", "a.\"Anomaly Type\""] | ["COUNT(*)"] | 16 | 1.738 |
| [S53/Q51](#s53) | success | ["login_records_table", "user_information_table"] | 2 / {'INNER': 1} | ["u.Department"] | ["COUNT(*)", "SUM(CASE WHEN l.\"Authentication Status\" = 'Failure' THEN 1 ELSE 0 END)", "SUM(CASE WHEN l.\"Two-Factor Authentication Status\" = 'Not Enabled' THEN 1 ELSE 0 END)", "COUNT(DISTINCT l.\"User ID\")"] | 4 | 1.324 |
| [S54/Q52](#s54) | success | ["abnormal_logins_table", "login_records_table", "user_information_table"] | 2 / {'INNER': 2} | ["l.\"User ID\"", "u.Department"] | ["COUNT(*)", "COUNT(DISTINCT CASE WHEN ua.anomaly_count >= 2 THEN u.\"User ID\" ELSE NULL END)", "COUNT(DISTINCT u.\"User ID\")"] | 4 | 1.807 |
| [S55/Q53](#s55) | success | ["user_account_table", "user_information_table"] | 2 / {'INNER': 1} | ["u.Department"] | ["AVG(ua.\"Password Attempt Count\")", "SUM(CASE WHEN ua.\"Account Lock Status\" = 'Locked' THEN 1 ELSE 0 END)", "COUNT(*)"] | 4 | 1.069 |
| [S56/Q54](#s56) | success | ["user_information_table"] | 0 / {} | ["Department"] | ["COUNT(*)"] | 4 | 0.543 |
| [S57/Q55](#s57) | success | ["abnormal_logins_table", "login_records_table", "user_information_table"] | 3 / {'INNER': 2} | ["u.Department"] | ["COUNT(*)"] | 4 | 1.829 |
| [S58/Q56](#s58) | success | ["abnormal_logins_table", "login_records_table", "user_information_table"] | 3 / {'INNER': 2} | ["u.Department", "a.\"Risk Level\""] | ["COUNT(*)"] | 16 | 1.845 |
| [S59/Q57](#s59) | success | ["login_records_table", "user_information_table"] | 2 / {'INNER': 1} | ["u.Department"] | ["COUNT(*)", "SUM(CASE WHEN l.\"Authentication Status\" = 'Failure' THEN 1 ELSE 0 END)", "SUM(CASE WHEN l.\"Two-Factor Authentication Status\" = 'Not Enabled' THEN 1 ELSE 0 END)"] | 4 | 1.253 |
| [S60/Q58](#s60) | success | ["abnormal_logins_table", "login_records_table", "user_information_table"] | 2 / {'INNER': 2} | ["l.\"User ID\"", "u.Department"] | ["COUNT(*)", "COUNT(DISTINCT CASE WHEN ua.anomaly_count >= 2 THEN u.\"User ID\" ELSE NULL END)", "COUNT(DISTINCT u.\"User ID\")"] | 4 | 1.781 |
| [S61/Q59](#s61) | success | ["user_account_table", "user_information_table"] | 2 / {'INNER': 1} | ["u.Department"] | ["AVG(ua.\"Password Attempt Count\")", "SUM(CASE WHEN ua.\"Account Lock Status\" = 'Locked' THEN 1 ELSE 0 END)", "COUNT(*)"] | 4 | 1.098 |
| [S62/Q60](#s62) | success | ["abnormal_logins_table", "login_records_table", "user_information_table"] | 3 / {'INNER': 2} | ["u.Department"] | ["AVG(a.\"Anomaly Score\")"] | 4 | 1.615 |
| [S63/Q61](#s63) | success | ["login_records_table", "security_events_table", "user_information_table"] | 3 / {'INNER': 2} | ["u.Department"] | ["COUNT(*)"] | 4 | 1.539 |
| [S64/Q62](#s64) | success | ["abnormal_logins_table", "login_records_table", "user_information_table"] | 3 / {'INNER': 2} | [] | [] | 414 | 2.413 |
| [S65/Q63](#s65) | success | ["login_records_table", "user_information_table"] | 2 / {'INNER': 1} | [] | [] | 487 | 1.519 |
| [S66/Q64](#s66) | success | ["login_records_table", "user_information_table"] | 2 / {'INNER': 1} | [] | [] | 487 | 1.466 |
| [S67/Q65](#s67) | success | ["login_records_table", "system_logs_table", "user_information_table"] | 3 / {'INNER': 2} | ["u.Department", "sl.\"Handling Status\""] | ["COUNT(*)"] | 12 | 2.053 |
| [S68/Q66](#s68) | success | ["system_logs_table"] | 0 / {} | [] | [] | 3 | 0.406 |
| [S69/Q67](#s69) | success | ["abnormal_logins_table", "login_records_table", "user_information_table"] | 3 / {'INNER': 2} | ["u.Department"] | ["COUNT(*)"] | 4 | 1.503 |
| [S70/Q68](#s70) | success | ["user_information_table"] | 0 / {} | ["Department"] | ["COUNT(*)"] | 4 | 0.592 |
| [S71/Q69](#s71) | success | ["abnormal_logins_table", "login_records_table", "user_information_table"] | 3 / {'INNER': 2} | ["u.Department"] | ["COUNT(*)"] | 4 | 1.764 |
| [S72/Q70](#s72) | success | ["abnormal_logins_table", "login_records_table", "user_information_table"] | 3 / {'INNER': 2} | ["u.Department"] | ["COUNT(*)"] | 4 | 1.296 |
| [S73/Q71](#s73) | success | ["abnormal_logins_table", "login_records_table", "user_information_table"] | 2 / {'INNER': 2} | ["l.\"User ID\"", "u.Department"] | ["COUNT(*)", "COUNT(DISTINCT CASE WHEN ua.anomaly_count >= 2 THEN u.\"User ID\" ELSE NULL END)", "COUNT(DISTINCT u.\"User ID\")"] | 4 | 1.663 |
| [S74/Q72](#s74) | success | ["login_records_table", "user_information_table"] | 2 / {'INNER': 1} | ["u.Department"] | ["COUNT(*)", "SUM(CASE WHEN l.\"Authentication Status\" = 'Failure' THEN 1 ELSE 0 END)", "SUM(CASE WHEN l.\"Two-Factor Authentication Status\" = 'Not Enabled' THEN 1 ELSE 0 END)"] | 4 | 1.27 |
| [S75/Q73](#s75) | success | ["user_account_table", "user_information_table"] | 2 / {'INNER': 1} | ["u.Department"] | ["AVG(ua.\"Password Attempt Count\")", "SUM(CASE WHEN ua.\"Account Lock Status\" = 'Locked' THEN 1 ELSE 0 END)", "COUNT(*)"] | 4 | 1.042 |
| [S76/Q74](#s76) | success | ["login_records_table", "system_logs_table", "user_information_table"] | 3 / {'INNER': 2} | ["u.Department"] | ["COUNT(*)", "SUM(CASE WHEN sl.\"Handling Status\" = 'Unprocessed' THEN 1 ELSE 0 END)"] | 4 | 1.632 |
| [S77/Q75](#s77) | success | ["login_records_table", "security_events_table", "user_information_table"] | 3 / {'INNER': 2} | ["u.Department"] | ["COUNT(*)", "SUM(CASE WHEN se.\"Severity\" IN ('High', 'Severe') THEN 1 ELSE 0 END)"] | 4 | 1.559 |
| [S78/Q76](#s78) | success | ["abnormal_logins_table", "login_records_table", "user_information_table"] | 3 / {'INNER': 2} | ["u.Department"] | ["SUM(CASE WHEN a.\"Confirmation Status\" = 'Confirmed' THEN 1 ELSE 0 END)", "COUNT(*)"] | 4 | 1.611 |
| [S79/Q77](#s79) | success | ["abnormal_logins_table", "login_records_table", "user_information_table"] | 2 / {'INNER': 2} | ["l.\"User ID\"", "u.Department", "CASE WHEN ua.anomaly_count >= 3 THEN '3+' WHEN ua.anomaly_count = 2 THEN '2' ELSE '1' END"] | ["COUNT(*)", "COUNT(DISTINCT u.\"User ID\")", "SUM(ua.anomaly_count)"] | 12 | 2.01 |
| [S80/Q78](#s80) | success | ["abnormal_logins_table", "login_records_table", "user_information_table"] | 3 / {'INNER': 2} | ["u.Department"] | ["COUNT(*)"] | 4 | 2.221 |
| [S81/Q79](#s81) | success | ["abnormal_logins_table", "login_records_table", "user_information_table"] | 3 / {'INNER': 2} | ["u.Department"] | ["SUM(CASE WHEN CAST(STRFTIME('%H', a.\"Detection Time\") AS INTEGER) BETWEEN 0 AND 6 THEN 1 ELSE 0 END)", "COUNT(*)", "COUNT(*)", "SUM(CASE WHEN CAST(STRFTIME('%H', a.\"Detection Time\") AS INTEGER) BETWEEN 0 AND 6 THEN 1 ELSE 0 END)"] | 4 | 2.223 |
| [S82/Q80](#s82) | success | ["abnormal_logins_table", "login_records_table", "user_information_table"] | 3 / {'INNER': 2} | ["u.Department"] | ["COUNT(DISTINCT a.\"Anomaly ID\")", "COUNT(DISTINCT l.\"User ID\")", "COUNT(DISTINCT a.\"Anomaly ID\")", "COUNT(DISTINCT l.\"User ID\")"] | 4 | 2.19 |


## 元数据和设置

| SQL | 类别 | 状态 | 内容 |
| --- | --- | --- | --- |
| S1 | connection_setup | success | PRAGMA query_only=ON |
| S2 | metadata | success | SELECT name,sql FROM sqlite_master WHERE type='table' ORDER BY name |


## Python 与执行位置

人工源码审查：**partial_violation**。SQL 完成部门、账号、登录和异常事件的主要关联与汇总。P1 将多个部门摘要在 pandas 中连续合并，P2/P3 计算风险占比，P4 追加部门均值；这些关系与汇总计算可以放在 SQL。Kruskal、卡方检验和绘图单独视为合理补充，不因使用统计检验就判整次 Python 调用违规。 [证据](../reviews/dacomp-035.json)。

P1：Need to compute a composite security awareness risk index across departments using multiple indicators from different tables. This requires combining data from multiple queries and computing weighted scores, which is better done in Python for flexibility and visualization.

[源码](../../../runs/dsv4flash-db-first-full-01/dacomp-035/attempt-01/python/P1.py)；[输出](../../../runs/dsv4flash-db-first-full-01/dacomp-035/attempt-01/python/P1.stdout)；[错误](../../../runs/dsv4flash-db-first-full-01/dacomp-035/attempt-01/python/P1.stderr)。检出需人工核验的 SQL 可实现操作：.merge(, .query(, sort_values(；不能仅凭理由判为合规。

P2：Create visualizations to compare departments across key security awareness indicators. This is a visualization task best done in Python with matplotlib.

[源码](../../../runs/dsv4flash-db-first-full-01/dacomp-035/attempt-01/python/P2.py)；[输出](../../../runs/dsv4flash-db-first-full-01/dacomp-035/attempt-01/python/P2.stdout)；[错误](../../../runs/dsv4flash-db-first-full-01/dacomp-035/attempt-01/python/P2.stderr)。检出需人工核验的 SQL 可实现操作：.merge(, .query(；不能仅凭理由判为合规。

P3：Fix the radar chart creation; the events query column naming caused a KeyError. Redo the radar visualization in Python.

[源码](../../../runs/dsv4flash-db-first-full-01/dacomp-035/attempt-01/python/P3.py)；[输出](../../../runs/dsv4flash-db-first-full-01/dacomp-035/attempt-01/python/P3.stdout)；[错误](../../../runs/dsv4flash-db-first-full-01/dacomp-035/attempt-01/python/P3.stderr)。检出需人工核验的 SQL 可实现操作：.query(；不能仅凭理由判为合规。

P4：Perform statistical tests (Kruskal-Wallis, chi-square) to assess whether department differences in anomaly scores and risk-level distributions are statistically significant. These tests are not supported by SQLite.

[源码](../../../runs/dsv4flash-db-first-full-01/dacomp-035/attempt-01/python/P4.py)；[输出](../../../runs/dsv4flash-db-first-full-01/dacomp-035/attempt-01/python/P4.stdout)；[错误](../../../runs/dsv4flash-db-first-full-01/dacomp-035/attempt-01/python/P4.stderr)。检出需人工核验的 SQL 可实现操作：groupby(, .query(；不能仅凭理由判为合规。

P5：Compute a focused security awareness weakness score weighing only the most behavioral indicators (repeat offenders, remote logins, no 2FA, locked accounts, failed logins, unprocessed logs). Visualization in Python.

[源码](../../../runs/dsv4flash-db-first-full-01/dacomp-035/attempt-01/python/P5.py)；[输出](../../../runs/dsv4flash-db-first-full-01/dacomp-035/attempt-01/python/P5.stdout)；[错误](../../../runs/dsv4flash-db-first-full-01/dacomp-035/attempt-01/python/P5.stderr)。检出需人工核验的 SQL 可实现操作：.query(, sort_values(；不能仅凭理由判为合规。

## 优化机会

已验证候选。筛选限于精确 SQL、相同自包含 CTE、相同单表完整过滤、可分解单表聚合；未覆盖任意 Join 等价和一般谓词蕴含。全部候选都是 offline，未测在线预测。

| 候选 | 类型 | 已有结果 | 覆盖 SQL | 后续次数 | 中间行数 | 验证 | 成本 |
| --- | --- | --- | --- | --- | --- | --- | --- |
| C1 | exact-result reuse | True | ["S15", "S51"] | 1 | 16 | verified | Not benchmarked; correctness alone does not establish net speedup. |
| C2 | exact-result reuse | True | ["S16", "S52"] | 1 | unknown | not_verified_cap | Not tested |
| C3 | exact-result reuse | True | ["S43", "S49", "S56", "S70"] | 3 | 4 | verified | Not benchmarked; correctness alone does not establish net speedup. |
| C4 | exact-result reuse | True | ["S46", "S53"] | 1 | unknown | not_verified_cap | Not tested |
| C5 | exact-result reuse | True | ["S47", "S55"] | 1 | unknown | not_verified_cap | Not tested |
| C6 | exact-result reuse | True | ["S60", "S73"] | 1 | unknown | not_verified_cap | Not tested |
| C7 | aggregate MV | False | ["S12", "S43", "S49", "S56", "S70"] | 4 | 4 | verified | Not benchmarked; correctness alone does not establish net speedup. |
| C8 | aggregate MV | False | ["S19", "S20"] | 1 | unknown | not_verified_cap | Not tested |


已验证覆盖（含触发查询、候选并集去重）：7/80 条成功数据 SQL。正确性仅针对当前数据库快照；未测性能的候选不能声称已加速。

[完整 build/rewrite 与比较证据](dacomp-035.analysis.json)。

### C7：aggregate MV

Union of grouping keys; decomposable aggregate states; AVG uses SUM and non-NULL COUNT.

原查询 [S12](#s12), [S43](#s43), [S49](#s49), [S56](#s56), [S70](#s70) → 新增共享状态 C7 → 后续 4 次可复用。该构建点为事后假设，不代表 Agent 当时预知后续。

构建定义：

```sql
SELECT department AS __g0, COUNT(*) AS __a0 FROM "user_information_table"  GROUP BY department
```

受益查询 S12 的改写示例：

```sql
SELECT __g0 AS "Department", SUM(__a0) AS user_count FROM temp.reuse_candidate GROUP BY __g0 ORDER BY __g0
```

| 原 SQL | 列名一致 | 结果一致 | 比较方法 |
| --- | --- | --- | --- |
| S12 | True | True | ordered_numeric_tolerance |
| S43 | True | True | exact_multiset |
| S49 | True | True | exact_multiset |
| S56 | True | True | exact_multiset |
| S70 | True | True | exact_multiset |


验证状态：verified；成本结论：Not benchmarked; correctness alone does not establish net speedup.

### C3：exact-result reuse

Identical normalized SQL and parameters; archive equality checked.

原查询 [S43](#s43), [S49](#s49), [S56](#s56), [S70](#s70) → 保留前序结果 S43 → 后续 3 次可复用。该构建点为事后假设，不代表 Agent 当时预知后续。

| 原 SQL | 列名一致 | 结果一致 | 比较方法 |
| --- | --- | --- | --- |
| S49 | True | True | exact_multiset |
| S56 | True | True | exact_multiset |
| S70 | True | True | exact_multiset |


验证状态：verified；成本结论：Not benchmarked; correctness alone does not establish net speedup.

### C1：exact-result reuse

Identical normalized SQL and parameters; archive equality checked.

原查询 [S15](#s15), [S51](#s51) → 保留前序结果 S15 → 后续 1 次可复用。该构建点为事后假设，不代表 Agent 当时预知后续。

| 原 SQL | 列名一致 | 结果一致 | 比较方法 |
| --- | --- | --- | --- |
| S51 | True | True | ordered_numeric_tolerance |


验证状态：verified；成本结论：Not benchmarked; correctness alone does not establish net speedup.

结果依赖：自动记录 SQL→Python 的接口父调用，以及源码中引用归档文件的消费者；字面值相同不认定因果。模型方向选择需要人工读取消息，尚未做全面因果标注。

[原始报告](../../../runs/dsv4flash-db-first-full-01/dacomp-035/attempt-01/answer.md)；[统一消息](../../../runs/dsv4flash-db-first-full-01/dacomp-035/attempt-01/messages.jsonl)；[原始 OpenCode 事件](../../../runs/dsv4flash-db-first-full-01/dacomp-035/attempt-01/opencode.jsonl)；[SQL 引擎日志](../../../runs/dsv4flash-db-first-full-01/dacomp-035/attempt-01/sql_journal.jsonl)。

[可读报告（本地图片链接规范化）](../answers/dacomp-035.md)。原始回答保留，分析结论未改写。

## S1

类别 `connection_setup`；来源 `connection`；调用 `9dc1d409ce2a47b5a64c1686bfaceedc`；状态 `success`。

```sql
PRAGMA query_only=ON
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-035/attempt-01/sql/S1.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-035/attempt-01/sql/S1.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-035/attempt-01/results/S1.rows.jsonl)；完整：True；SHA256：`e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`。

## S2

类别 `metadata`；来源 `list_db`；调用 `9dc1d409ce2a47b5a64c1686bfaceedc`；状态 `success`。

```sql
SELECT name,sql FROM sqlite_master WHERE type='table' ORDER BY name
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-035/attempt-01/sql/S2.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-035/attempt-01/sql/S2.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-035/attempt-01/results/S2.rows.jsonl)；完整：True；SHA256：`63b208e518465ab4f8748a5c98784a91a85fd045e8fe63ada92353691e34975a`。

## S3

类别 `data`；来源 `query_db`；调用 `5fd7e26f49d742f3bbbf61e8772010df`；状态 `success`。

```sql
SELECT COUNT(*) AS n FROM abnormal_logins_table
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-035/attempt-01/sql/S3.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-035/attempt-01/sql/S3.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-035/attempt-01/results/S3.rows.jsonl)；完整：True；SHA256：`8da9b04c68a0f6ae33c833dfb98a372d13868f387160448745227e7081a5f4c5`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "abnormal_logins_table", "kind": "base", "block": null, "base_tables": ["abnormal_logins_table"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |


## S4

类别 `data`；来源 `query_db`；调用 `e1ee69dd718a45fd9cdfe7a19f21485d`；状态 `success`。

```sql
SELECT * FROM abnormal_logins_table LIMIT 20
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-035/attempt-01/sql/S4.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-035/attempt-01/sql/S4.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-035/attempt-01/results/S4.rows.jsonl)；完整：True；SHA256：`9751fc2fe3a9eb2c177ef5bf3060776cd8abfdd36b8143d4ac3169529b929856`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "abnormal_logins_table", "kind": "base", "block": null, "base_tables": ["abnormal_logins_table"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |


## S5

类别 `data`；来源 `query_db`；调用 `9ba417ccabe74f709ab10cb0de310c37`；状态 `success`。

```sql
SELECT * FROM user_information_table LIMIT 20
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-035/attempt-01/sql/S5.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-035/attempt-01/sql/S5.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-035/attempt-01/results/S5.rows.jsonl)；完整：True；SHA256：`f8ec6bfb5b850e9f906854f63b01a14d72e5a2de0c9ffcb1e074e53c945bb739`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "user_information_table", "kind": "base", "block": null, "base_tables": ["user_information_table"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |


## S6

类别 `data`；来源 `query_db`；调用 `95db90c70b29423c9b90228a4a08caa2`；状态 `success`。

```sql
SELECT * FROM login_records_table LIMIT 20
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-035/attempt-01/sql/S6.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-035/attempt-01/sql/S6.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-035/attempt-01/results/S6.rows.jsonl)；完整：True；SHA256：`5d6812fde0e7a1d9ec6a2e2653d298a4555046537aafd36086e493f61df77009`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "login_records_table", "kind": "base", "block": null, "base_tables": ["login_records_table"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |


## S7

类别 `data`；来源 `query_db`；调用 `ad3f8fd716c34d969cc4b4e456ec0233`；状态 `success`。

```sql
SELECT DISTINCT Department FROM user_information_table ORDER BY Department
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-035/attempt-01/sql/S7.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-035/attempt-01/sql/S7.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-035/attempt-01/results/S7.rows.jsonl)；完整：True；SHA256：`24ff1ee47182e079bd480b87df583e4c723436c091953416b2e95cce198e0a93`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "user_information_table", "kind": "base", "block": null, "base_tables": ["user_information_table"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |


## S8

类别 `data`；来源 `query_db`；调用 `0543c1e1521e44d4bf99b7c607168b66`；状态 `success`。

```sql
SELECT COUNT(DISTINCT "User ID") AS cnt FROM user_information_table
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-035/attempt-01/sql/S8.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-035/attempt-01/sql/S8.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-035/attempt-01/results/S8.rows.jsonl)；完整：True；SHA256：`187fe069e9ba510c313b1ce0344433073002d23e464d8c1786569dac40d9fb75`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "user_information_table", "kind": "base", "block": null, "base_tables": ["user_information_table"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(DISTINCT "User ID") | [{"table": "user_information_table", "column": "User ID"}] | [] | False |


## S9

类别 `data`；来源 `query_db`；调用 `ecafe96de693494993d7098af9169505`；状态 `success`。

```sql
SELECT COUNT(DISTINCT "Login Record ID") AS cnt FROM login_records_table
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-035/attempt-01/sql/S9.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-035/attempt-01/sql/S9.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-035/attempt-01/results/S9.rows.jsonl)；完整：True；SHA256：`34bc8f25b32f719b9792aee1512776e55862d1033145f0c48a53d4ce9a30baa7`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "login_records_table", "kind": "base", "block": null, "base_tables": ["login_records_table"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(DISTINCT "Login Record ID") | [{"table": "login_records_table", "column": "Login Record ID"}] | [] | False |


## S10

类别 `data`；来源 `query_db`；调用 `b35da6e6c31d464db23bae37623998e1`；状态 `success`。

```sql
SELECT DISTINCT "Anomaly Type" FROM abnormal_logins_table
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-035/attempt-01/sql/S10.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-035/attempt-01/sql/S10.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-035/attempt-01/results/S10.rows.jsonl)；完整：True；SHA256：`b8c83ab9af1958032925f9f4fe6a017aa59d4709689fcdf56c17edb990b53c5f`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "abnormal_logins_table", "kind": "base", "block": null, "base_tables": ["abnormal_logins_table"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |


## S11

类别 `data`；来源 `query_db`；调用 `c772ed943540417c877b8c65bf1cc3ee`；状态 `success`。

```sql
SELECT DISTINCT "Risk Level" FROM abnormal_logins_table
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-035/attempt-01/sql/S11.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-035/attempt-01/sql/S11.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-035/attempt-01/results/S11.rows.jsonl)；完整：True；SHA256：`1bf178131e0764121d10c738f146c032aab8b98df312ab8e6e759c3b65133a19`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "abnormal_logins_table", "kind": "base", "block": null, "base_tables": ["abnormal_logins_table"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |


## S12

类别 `data`；来源 `query_db`；调用 `dfd3a671cc8e4fa292d9a6e1660a9b45`；状态 `success`。

```sql
SELECT Department, COUNT(*) AS user_count FROM user_information_table GROUP BY Department ORDER BY Department
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-035/attempt-01/sql/S12.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-035/attempt-01/sql/S12.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-035/attempt-01/results/S12.rows.jsonl)；完整：True；SHA256：`4a8a8a83aabaca7f9a5e414971633557a7c8d33468180fa69b5165e584085664`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "user_information_table", "kind": "base", "block": null, "base_tables": ["user_information_table"]}] | [] | ["Department"] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |


## S13

类别 `data`；来源 `query_db`；调用 `1b7e74719790438f904d282597e3c40e`；状态 `success`。

```sql
SELECT DISTINCT "Confirmation Status" FROM abnormal_logins_table
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-035/attempt-01/sql/S13.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-035/attempt-01/sql/S13.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-035/attempt-01/results/S13.rows.jsonl)；完整：True；SHA256：`8ef90dba4fe00bb151d60ef8d1c91b57a78ce6bd2d20295629314101786030fc`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "abnormal_logins_table", "kind": "base", "block": null, "base_tables": ["abnormal_logins_table"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |


## S14

类别 `data`；来源 `query_db`；调用 `bf715c6fb2234ae496255fc5815b6ab1`；状态 `success`。

```sql
SELECT 
  u.Department,
  COUNT(DISTINCT a."Anomaly ID") AS anomaly_count,
  COUNT(DISTINCT a."Login Record ID") AS login_records_with_anomalies,
  COUNT(DISTINCT u."User ID") AS users_with_anomalies,
  ROUND(AVG(a."Anomaly Score"), 2) AS avg_anomaly_score,
  ROUND(AVG(a."Device Anomaly Indicators"), 2) AS avg_device_indicator,
  ROUND(AVG(a."Network Anomaly Indicators"), 2) AS avg_network_indicator,
  ROUND(AVG(a."Behavior Anomaly Indicators"), 2) AS avg_behavior_indicator
FROM abnormal_logins_table a
JOIN login_records_table l ON a."Login Record ID" = l."Login Record ID"
JOIN user_information_table u ON l."User ID" = u."User ID"
GROUP BY u.Department
ORDER BY anomaly_count DESC
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-035/attempt-01/sql/S14.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-035/attempt-01/sql/S14.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-035/attempt-01/results/S14.rows.jsonl)；完整：True；SHA256：`6cafda215cabcd64aeabd76b21909140adb782e48362867ef8e3dea2abe83173`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "a", "kind": "base", "block": null, "base_tables": ["abnormal_logins_table"]}, {"alias": "l", "kind": "base", "block": null, "base_tables": ["login_records_table"]}, {"alias": "u", "kind": "base", "block": null, "base_tables": ["user_information_table"]}] | [{"type": "INNER", "right": "login_records_table AS l", "on": "a.\"Login Record ID\" = l.\"Login Record ID\"", "using": []}, {"type": "INNER", "right": "user_information_table AS u", "on": "l.\"User ID\" = u.\"User ID\"", "using": []}] | ["u.Department"] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(DISTINCT a."Anomaly ID") | [{"table": "abnormal_logins_table", "column": "Anomaly ID"}] | [] | False |
| B1 | COUNT(DISTINCT a."Login Record ID") | [{"table": "abnormal_logins_table", "column": "Login Record ID"}] | [] | False |
| B1 | COUNT(DISTINCT u."User ID") | [{"table": "user_information_table", "column": "User ID"}] | [] | False |
| B1 | AVG(a."Anomaly Score") | [{"table": "abnormal_logins_table", "column": "Anomaly Score"}] | [] | False |
| B1 | AVG(a."Device Anomaly Indicators") | [{"table": "abnormal_logins_table", "column": "Device Anomaly Indicators"}] | [] | False |
| B1 | AVG(a."Network Anomaly Indicators") | [{"table": "abnormal_logins_table", "column": "Network Anomaly Indicators"}] | [] | False |
| B1 | AVG(a."Behavior Anomaly Indicators") | [{"table": "abnormal_logins_table", "column": "Behavior Anomaly Indicators"}] | [] | False |


## S15

类别 `data`；来源 `query_db`；调用 `a837816161be4b9bafe3e71079e5b3d5`；状态 `success`。

```sql
SELECT 
  u.Department,
  a."Risk Level",
  COUNT(*) AS cnt
FROM abnormal_logins_table a
JOIN login_records_table l ON a."Login Record ID" = l."Login Record ID"
JOIN user_information_table u ON l."User ID" = u."User ID"
GROUP BY u.Department, a."Risk Level"
ORDER BY u.Department, a."Risk Level"
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-035/attempt-01/sql/S15.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-035/attempt-01/sql/S15.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-035/attempt-01/results/S15.rows.jsonl)；完整：True；SHA256：`3961f570f2642e998c0852641d28cfd78b356fa192491e642d0845fda5348cc4`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "a", "kind": "base", "block": null, "base_tables": ["abnormal_logins_table"]}, {"alias": "l", "kind": "base", "block": null, "base_tables": ["login_records_table"]}, {"alias": "u", "kind": "base", "block": null, "base_tables": ["user_information_table"]}] | [{"type": "INNER", "right": "login_records_table AS l", "on": "a.\"Login Record ID\" = l.\"Login Record ID\"", "using": []}, {"type": "INNER", "right": "user_information_table AS u", "on": "l.\"User ID\" = u.\"User ID\"", "using": []}] | ["u.Department", "a.\"Risk Level\""] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |


## S16

类别 `data`；来源 `query_db`；调用 `de923c0da6454a809940c929d0fa8294`；状态 `success`。

```sql
SELECT 
  u.Department,
  a."Anomaly Type",
  COUNT(*) AS cnt
FROM abnormal_logins_table a
JOIN login_records_table l ON a."Login Record ID" = l."Login Record ID"
JOIN user_information_table u ON l."User ID" = u."User ID"
GROUP BY u.Department, a."Anomaly Type"
ORDER BY u.Department, a."Anomaly Type"
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-035/attempt-01/sql/S16.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-035/attempt-01/sql/S16.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-035/attempt-01/results/S16.rows.jsonl)；完整：True；SHA256：`1eea26781fae46c826653afd5dcd129836e9d3c956ba497797f4c06c09a03305`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "a", "kind": "base", "block": null, "base_tables": ["abnormal_logins_table"]}, {"alias": "l", "kind": "base", "block": null, "base_tables": ["login_records_table"]}, {"alias": "u", "kind": "base", "block": null, "base_tables": ["user_information_table"]}] | [{"type": "INNER", "right": "login_records_table AS l", "on": "a.\"Login Record ID\" = l.\"Login Record ID\"", "using": []}, {"type": "INNER", "right": "user_information_table AS u", "on": "l.\"User ID\" = u.\"User ID\"", "using": []}] | ["u.Department", "a.\"Anomaly Type\""] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |


## S17

类别 `data`；来源 `query_db`；调用 `8a11bb54780145dfbe4e8cef672848f4`；状态 `success`。

```sql
SELECT 
  u.Department,
  a."Risk Level",
  COUNT(*) AS cnt
FROM abnormal_logins_table a
JOIN login_records_table l ON a."Login Record ID" = l."Login Record ID"
JOIN user_information_table u ON l."User ID" = u."User ID"
WHERE u.Department = 'Technical Department'
GROUP BY u.Department, a."Risk Level"
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-035/attempt-01/sql/S17.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-035/attempt-01/sql/S17.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-035/attempt-01/results/S17.rows.jsonl)；完整：True；SHA256：`0f9555c9400cb28f31b2199c5b4a33921bf9f4025a5c18a4a21604c915bb6ed4`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "a", "kind": "base", "block": null, "base_tables": ["abnormal_logins_table"]}, {"alias": "l", "kind": "base", "block": null, "base_tables": ["login_records_table"]}, {"alias": "u", "kind": "base", "block": null, "base_tables": ["user_information_table"]}] | [{"type": "INNER", "right": "login_records_table AS l", "on": "a.\"Login Record ID\" = l.\"Login Record ID\"", "using": []}, {"type": "INNER", "right": "user_information_table AS u", "on": "l.\"User ID\" = u.\"User ID\"", "using": []}] | ["u.Department", "a.\"Risk Level\""] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |


## S18

类别 `data`；来源 `query_db`；调用 `a240becdad954605949d8a407aac17c1`；状态 `success`。

```sql
SELECT 
  u.Department,
  a."Anomaly Type",
  COUNT(*) AS cnt
FROM abnormal_logins_table a
JOIN login_records_table l ON a."Login Record ID" = l."Login Record ID"
JOIN user_information_table u ON l."User ID" = u."User ID"
WHERE u.Department = 'Technical Department'
GROUP BY u.Department, a."Anomaly Type"
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-035/attempt-01/sql/S18.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-035/attempt-01/sql/S18.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-035/attempt-01/results/S18.rows.jsonl)；完整：True；SHA256：`bfab41957f085ee261dd0236f26ad4c88b821e9cdb85c18b6b32b8721f284789`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "a", "kind": "base", "block": null, "base_tables": ["abnormal_logins_table"]}, {"alias": "l", "kind": "base", "block": null, "base_tables": ["login_records_table"]}, {"alias": "u", "kind": "base", "block": null, "base_tables": ["user_information_table"]}] | [{"type": "INNER", "right": "login_records_table AS l", "on": "a.\"Login Record ID\" = l.\"Login Record ID\"", "using": []}, {"type": "INNER", "right": "user_information_table AS u", "on": "l.\"User ID\" = u.\"User ID\"", "using": []}] | ["u.Department", "a.\"Anomaly Type\""] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |


## S19

类别 `data`；来源 `query_db`；调用 `7ad0467bdfc745b1b41f8923cff1b707`；状态 `success`。

```sql
SELECT l."Authentication Status", COUNT(*) AS cnt FROM login_records_table l GROUP BY l."Authentication Status"
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-035/attempt-01/sql/S19.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-035/attempt-01/sql/S19.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-035/attempt-01/results/S19.rows.jsonl)；完整：True；SHA256：`db5f275df52f6b384846ef5b7e514122f3cc20f00fac77ade91a3e42e86a0649`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "l", "kind": "base", "block": null, "base_tables": ["login_records_table"]}] | [] | ["l.\"Authentication Status\""] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |


## S20

类别 `data`；来源 `query_db`；调用 `4f9a087590504e6da5c05f6d9d1ac0ff`；状态 `success`。

```sql
SELECT l."Two-Factor Authentication Status", COUNT(*) AS cnt FROM login_records_table l GROUP BY l."Two-Factor Authentication Status"
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-035/attempt-01/sql/S20.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-035/attempt-01/sql/S20.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-035/attempt-01/results/S20.rows.jsonl)；完整：True；SHA256：`e014ba56e1127724bf787bf8a44a0fd21f71298d3c86e48fbd3a96ec7e1028d6`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "l", "kind": "base", "block": null, "base_tables": ["login_records_table"]}] | [] | ["l.\"Two-Factor Authentication Status\""] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |


## S21

类别 `data`；来源 `query_db`；调用 `d5c47e0659b84947ab61140aeba40c73`；状态 `success`。

```sql
SELECT 
  u.Department,
  COUNT(*) AS total_logins,
  SUM(CASE WHEN l."Authentication Status" = 'Failure' THEN 1 ELSE 0 END) AS failed_logins,
  SUM(CASE WHEN l."Two-Factor Authentication Status" = 'Not Enabled' THEN 1 ELSE 0 END) AS no_2fa_logins,
  ROUND(100.0 * SUM(CASE WHEN l."Authentication Status" = 'Failure' THEN 1 ELSE 0 END) / COUNT(*), 1) AS pct_failed,
  ROUND(100.0 * SUM(CASE WHEN l."Two-Factor Authentication Status" = 'Not Enabled' THEN 1 ELSE 0 END) / COUNT(*), 1) AS pct_no_2fa
FROM login_records_table l
JOIN user_information_table u ON l."User ID" = u."User ID"
GROUP BY u.Department
ORDER BY pct_failed DESC
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-035/attempt-01/sql/S21.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-035/attempt-01/sql/S21.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-035/attempt-01/results/S21.rows.jsonl)；完整：True；SHA256：`aa835d38a50adc9e79d90a935f7fe71a09ff498574ca54722f54e37ecb2e6bf2`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "l", "kind": "base", "block": null, "base_tables": ["login_records_table"]}, {"alias": "u", "kind": "base", "block": null, "base_tables": ["user_information_table"]}] | [{"type": "INNER", "right": "user_information_table AS u", "on": "l.\"User ID\" = u.\"User ID\"", "using": []}] | ["u.Department"] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |
| B1 | SUM(CASE WHEN l."Authentication Status" = 'Failure' THEN 1 ELSE 0 END) | [] | [{"table": "login_records_table", "column": "Authentication Status"}] | False |
| B1 | SUM(CASE WHEN l."Two-Factor Authentication Status" = 'Not Enabled' THEN 1 ELSE 0 END) | [] | [{"table": "login_records_table", "column": "Two-Factor Authentication Status"}] | False |
| B1 | COUNT(*) | [] | [] | True |
| B1 | COUNT(*) | [] | [] | True |
| B1 | SUM(CASE WHEN l."Authentication Status" = 'Failure' THEN 1 ELSE 0 END) | [] | [{"table": "login_records_table", "column": "Authentication Status"}] | False |
| B1 | SUM(CASE WHEN l."Two-Factor Authentication Status" = 'Not Enabled' THEN 1 ELSE 0 END) | [] | [{"table": "login_records_table", "column": "Two-Factor Authentication Status"}] | False |


## S22

类别 `data`；来源 `query_db`；调用 `0c68a617a9924ee38e5e5691ed457c4f`；状态 `success`。

```sql
SELECT 
  u.Department,
  AVG(ua."Password Attempt Count") AS avg_password_attempts,
  SUM(CASE WHEN ua."Account Lock Status" = 'Locked' THEN 1 ELSE 0 END) AS locked_accounts,
  COUNT(DISTINCT ua."Account ID") AS account_count,
  SUM(CASE WHEN ua."Password Status" = 'Expired' THEN 1 ELSE 0 END) AS expired_passwords
FROM user_account_table ua
JOIN user_information_table u ON ua."User ID" = u."User ID"
GROUP BY u.Department
ORDER BY avg_password_attempts DESC
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-035/attempt-01/sql/S22.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-035/attempt-01/sql/S22.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-035/attempt-01/results/S22.rows.jsonl)；完整：True；SHA256：`73804f48ca12f9dd76f6cae63c6afc4bb52edb8c504c7de11031802c3fed95b2`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "ua", "kind": "base", "block": null, "base_tables": ["user_account_table"]}, {"alias": "u", "kind": "base", "block": null, "base_tables": ["user_information_table"]}] | [{"type": "INNER", "right": "user_information_table AS u", "on": "ua.\"User ID\" = u.\"User ID\"", "using": []}] | ["u.Department"] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | AVG(ua."Password Attempt Count") | [{"table": "user_account_table", "column": "Password Attempt Count"}] | [] | False |
| B1 | SUM(CASE WHEN ua."Account Lock Status" = 'Locked' THEN 1 ELSE 0 END) | [] | [{"table": "user_account_table", "column": "Account Lock Status"}] | False |
| B1 | COUNT(DISTINCT ua."Account ID") | [{"table": "user_account_table", "column": "Account ID"}] | [] | False |
| B1 | SUM(CASE WHEN ua."Password Status" = 'Expired' THEN 1 ELSE 0 END) | [] | [{"table": "user_account_table", "column": "Password Status"}] | False |


## S23

类别 `data`；来源 `query_db`；调用 `2f9f9ca87478489f8e6827b2b30b4480`；状态 `success`。

```sql
SELECT 
  u.Department,
  COUNT(*) AS total_events,
  SUM(CASE WHEN se."Severity" = 'High' OR se."Severity" = 'Critical' OR se."Severity" = 'Severe' THEN 1 ELSE 0 END) AS high_severity_events,
  AVG(se."Risk Score") AS avg_risk_score
FROM security_events_table se
JOIN login_records_table l ON se."Login Record ID" = l."Login Record ID"
JOIN user_information_table u ON l."User ID" = u."User ID"
GROUP BY u.Department
ORDER BY total_events DESC
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-035/attempt-01/sql/S23.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-035/attempt-01/sql/S23.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-035/attempt-01/results/S23.rows.jsonl)；完整：True；SHA256：`f19713e1fde3751c433a1c6cdf46671415c060a6b21b58ec3f9ec2ed7e18483e`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "se", "kind": "base", "block": null, "base_tables": ["security_events_table"]}, {"alias": "l", "kind": "base", "block": null, "base_tables": ["login_records_table"]}, {"alias": "u", "kind": "base", "block": null, "base_tables": ["user_information_table"]}] | [{"type": "INNER", "right": "login_records_table AS l", "on": "se.\"Login Record ID\" = l.\"Login Record ID\"", "using": []}, {"type": "INNER", "right": "user_information_table AS u", "on": "l.\"User ID\" = u.\"User ID\"", "using": []}] | ["u.Department"] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |
| B1 | SUM(CASE WHEN se."Severity" = 'High' OR se."Severity" = 'Critical' OR se."Severity" = 'Severe' THEN 1 ELSE 0 END) | [] | [{"table": "security_events_table", "column": "Severity"}, {"table": "security_events_table", "column": "Severity"}, {"table": "security_events_table", "column": "Severity"}] | False |
| B1 | AVG(se."Risk Score") | [{"table": "security_events_table", "column": "Risk Score"}] | [] | False |


## S24

类别 `data`；来源 `query_db`；调用 `7b73d354be5444d38d100672f6c1acc0`；状态 `success`。

```sql
SELECT DISTINCT "Severity" FROM security_events_table
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-035/attempt-01/sql/S24.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-035/attempt-01/sql/S24.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-035/attempt-01/results/S24.rows.jsonl)；完整：True；SHA256：`bceaa0cc607eae0e99594208f3e25d66ebf4c034f577cff95ce83aa8bf26eb37`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "security_events_table", "kind": "base", "block": null, "base_tables": ["security_events_table"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |


## S25

类别 `data`；来源 `query_db`；调用 `c6a9b8c110dd4260ab3ed250214c6b1a`；状态 `success`。

```sql
SELECT COUNT(*) FROM security_events_table
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-035/attempt-01/sql/S25.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-035/attempt-01/sql/S25.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-035/attempt-01/results/S25.rows.jsonl)；完整：True；SHA256：`0f62ee75c20d007f2b4a4d2dbf75f51f7a171ffc45ce70c3138f97f247bf4a52`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "security_events_table", "kind": "base", "block": null, "base_tables": ["security_events_table"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |


## S26

类别 `data`；来源 `query_db`；调用 `abdd8209aebf48af9be37677f6f2ba7f`；状态 `success`。

```sql
SELECT 
  u.Department,
  a."Confirmation Status",
  COUNT(*) AS cnt
FROM abnormal_logins_table a
JOIN login_records_table l ON a."Login Record ID" = l."Login Record ID"
JOIN user_information_table u ON l."User ID" = u."User ID"
GROUP BY u.Department, a."Confirmation Status"
ORDER BY u.Department
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-035/attempt-01/sql/S26.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-035/attempt-01/sql/S26.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-035/attempt-01/results/S26.rows.jsonl)；完整：True；SHA256：`bddde0af26f737452f49880ec0e3d01e189e971fac7b09c938d642551facd4e9`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "a", "kind": "base", "block": null, "base_tables": ["abnormal_logins_table"]}, {"alias": "l", "kind": "base", "block": null, "base_tables": ["login_records_table"]}, {"alias": "u", "kind": "base", "block": null, "base_tables": ["user_information_table"]}] | [{"type": "INNER", "right": "login_records_table AS l", "on": "a.\"Login Record ID\" = l.\"Login Record ID\"", "using": []}, {"type": "INNER", "right": "user_information_table AS u", "on": "l.\"User ID\" = u.\"User ID\"", "using": []}] | ["u.Department", "a.\"Confirmation Status\""] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |


## S27

类别 `data`；来源 `query_db`；调用 `46b8ce898788471d9ea13712982db348`；状态 `success`。

```sql
SELECT 
  u.Department,
  COUNT(DISTINCT l."User ID") AS active_users_with_logins,
  COUNT(DISTINCT l."Login Record ID") AS logins,
  ROUND(1.0 * COUNT(DISTINCT a."Login Record ID") / COUNT(DISTINCT l."Login Record ID"), 3) AS anomaly_rate_per_login
FROM login_records_table l
JOIN user_information_table u ON l."User ID" = u."User ID"
LEFT JOIN abnormal_logins_table a ON l."Login Record ID" = a."Login Record ID"
GROUP BY u.Department
ORDER BY anomaly_rate_per_login DESC
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-035/attempt-01/sql/S27.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-035/attempt-01/sql/S27.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-035/attempt-01/results/S27.rows.jsonl)；完整：True；SHA256：`bc8c64673b57d75a31b30bf9fff864dbf25c691ae891a6a50522ccd7a31ed88b`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "l", "kind": "base", "block": null, "base_tables": ["login_records_table"]}, {"alias": "u", "kind": "base", "block": null, "base_tables": ["user_information_table"]}, {"alias": "a", "kind": "base", "block": null, "base_tables": ["abnormal_logins_table"]}] | [{"type": "INNER", "right": "user_information_table AS u", "on": "l.\"User ID\" = u.\"User ID\"", "using": []}, {"type": "LEFT", "right": "abnormal_logins_table AS a", "on": "l.\"Login Record ID\" = a.\"Login Record ID\"", "using": []}] | ["u.Department"] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(DISTINCT l."User ID") | [{"table": "login_records_table", "column": "User ID"}] | [] | False |
| B1 | COUNT(DISTINCT l."Login Record ID") | [{"table": "login_records_table", "column": "Login Record ID"}] | [] | False |
| B1 | COUNT(DISTINCT l."Login Record ID") | [{"table": "login_records_table", "column": "Login Record ID"}] | [] | False |
| B1 | COUNT(DISTINCT a."Login Record ID") | [{"table": "abnormal_logins_table", "column": "Login Record ID"}] | [] | False |


## S28

类别 `data`；来源 `query_db`；调用 `236c9c7b41f14b1f85df6fa539e4421f`；状态 `success`。

```sql
SELECT 
  u.Department,
  CASE WHEN user_anomaly_count.anomaly_count >= 2 THEN 'Multiple' ELSE 'Single' END AS anomaly_frequency,
  COUNT(DISTINCT u."User ID") AS user_count,
  SUM(user_anomaly_count.anomaly_count) AS total_anomalies
FROM (
  SELECT l."User ID", COUNT(*) AS anomaly_count
  FROM abnormal_logins_table a
  JOIN login_records_table l ON a."Login Record ID" = l."Login Record ID"
  GROUP BY l."User ID"
) user_anomaly_count
JOIN user_information_table u ON user_anomaly_count."User ID" = u."User ID"
GROUP BY u.Department, anomaly_frequency
ORDER BY u.Department, anomaly_frequency
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-035/attempt-01/sql/S28.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-035/attempt-01/sql/S28.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-035/attempt-01/results/S28.rows.jsonl)；完整：True；SHA256：`7f41883186319ac480716b7a365a111071589a018e7695d37d3711a1cb1e06b8`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "a", "kind": "base", "block": null, "base_tables": ["abnormal_logins_table"]}, {"alias": "l", "kind": "base", "block": null, "base_tables": ["login_records_table"]}] | [{"type": "INNER", "right": "login_records_table AS l", "on": "a.\"Login Record ID\" = l.\"Login Record ID\"", "using": []}] | ["l.\"User ID\""] |
| B2 | [{"alias": "user_anomaly_count", "kind": "derived", "block": "B1", "base_tables": ["abnormal_logins_table", "login_records_table"]}, {"alias": "u", "kind": "base", "block": null, "base_tables": ["user_information_table"]}] | [{"type": "INNER", "right": "user_information_table AS u", "on": "user_anomaly_count.\"User ID\" = u.\"User ID\"", "using": []}] | ["u.Department", "CASE WHEN user_anomaly_count.anomaly_count >= 2 THEN 'Multiple' ELSE 'Single' END"] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |
| B2 | COUNT(DISTINCT u."User ID") | [{"table": "user_information_table", "column": "User ID"}] | [] | False |
| B2 | SUM(user_anomaly_count.anomaly_count) | [] | [] | False |


## S29

类别 `data`；来源 `query_db`；调用 `cfca362ce44d45589cf23d75f971a39e`；状态 `success`。

```sql
SELECT 
  u.Department,
  a."Risk Level",
  a."Confirmation Status",
  COUNT(*) AS cnt
FROM abnormal_logins_table a
JOIN login_records_table l ON a."Login Record ID" = l."Login Record ID"
JOIN user_information_table u ON l."User ID" = u."User ID"
WHERE a."Risk Level" IN ('High', 'Severe')
GROUP BY u.Department, a."Risk Level", a."Confirmation Status"
ORDER BY u.Department, a."Risk Level"
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-035/attempt-01/sql/S29.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-035/attempt-01/sql/S29.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-035/attempt-01/results/S29.rows.jsonl)；完整：True；SHA256：`4bebcb128d60b017bc0e6b5d2b22a25dbf433f607712a6e9a4c2895e5a9d05b9`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "a", "kind": "base", "block": null, "base_tables": ["abnormal_logins_table"]}, {"alias": "l", "kind": "base", "block": null, "base_tables": ["login_records_table"]}, {"alias": "u", "kind": "base", "block": null, "base_tables": ["user_information_table"]}] | [{"type": "INNER", "right": "login_records_table AS l", "on": "a.\"Login Record ID\" = l.\"Login Record ID\"", "using": []}, {"type": "INNER", "right": "user_information_table AS u", "on": "l.\"User ID\" = u.\"User ID\"", "using": []}] | ["u.Department", "a.\"Risk Level\"", "a.\"Confirmation Status\""] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |


## S30

类别 `data`；来源 `query_db`；调用 `12798e5e31bb4766be07f364528fb045`；状态 `success`。

```sql
SELECT 
  u.Department,
  a."Risk Level",
  a."Confirmation Status",
  COUNT(*) AS cnt
FROM abnormal_logins_table a
JOIN login_records_table l ON a."Login Record ID" = l."Login Record ID"
JOIN user_information_table u ON l."User ID" = u."User ID"
WHERE u.Department = 'Technical Department' AND a."Risk Level" IN ('High', 'Severe')
GROUP BY u.Department, a."Risk Level", a."Confirmation Status"
ORDER BY u.Department, a."Risk Level"
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-035/attempt-01/sql/S30.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-035/attempt-01/sql/S30.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-035/attempt-01/results/S30.rows.jsonl)；完整：True；SHA256：`790b1902ec5bae01520b99d02691b1df14141e006565b52eca5ec8a600af982b`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "a", "kind": "base", "block": null, "base_tables": ["abnormal_logins_table"]}, {"alias": "l", "kind": "base", "block": null, "base_tables": ["login_records_table"]}, {"alias": "u", "kind": "base", "block": null, "base_tables": ["user_information_table"]}] | [{"type": "INNER", "right": "login_records_table AS l", "on": "a.\"Login Record ID\" = l.\"Login Record ID\"", "using": []}, {"type": "INNER", "right": "user_information_table AS u", "on": "l.\"User ID\" = u.\"User ID\"", "using": []}] | ["u.Department", "a.\"Risk Level\"", "a.\"Confirmation Status\""] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |


## S31

类别 `data`；来源 `query_db`；调用 `14185ea44ec34079be869b67cec8e744`；状态 `success`。

```sql
SELECT 
  u.Department,
  a."Anomaly Features",
  COUNT(*) AS cnt
FROM abnormal_logins_table a
JOIN login_records_table l ON a."Login Record ID" = l."Login Record ID"
JOIN user_information_table u ON l."User ID" = u."User ID"
GROUP BY u.Department, a."Anomaly Features"
ORDER BY u.Department, cnt DESC
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-035/attempt-01/sql/S31.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-035/attempt-01/sql/S31.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-035/attempt-01/results/S31.rows.jsonl)；完整：True；SHA256：`ebd613488b3846ef39800c6012fe019ac65e313ea31e2e7b970e4a48f162fde8`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "a", "kind": "base", "block": null, "base_tables": ["abnormal_logins_table"]}, {"alias": "l", "kind": "base", "block": null, "base_tables": ["login_records_table"]}, {"alias": "u", "kind": "base", "block": null, "base_tables": ["user_information_table"]}] | [{"type": "INNER", "right": "login_records_table AS l", "on": "a.\"Login Record ID\" = l.\"Login Record ID\"", "using": []}, {"type": "INNER", "right": "user_information_table AS u", "on": "l.\"User ID\" = u.\"User ID\"", "using": []}] | ["u.Department", "a.\"Anomaly Features\""] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |


## S32

类别 `data`；来源 `query_db`；调用 `d7e8a74b19574b46bdad6219e5445da0`；状态 `success`。

```sql
SELECT 
  u.Department,
  a."Anomaly Features",
  COUNT(*) AS cnt
FROM abnormal_logins_table a
JOIN login_records_table l ON a."Login Record ID" = l."Login Record ID"
JOIN user_information_table u ON l."User ID" = u."User ID"
WHERE u.Department = 'Technical Department'
GROUP BY u.Department, a."Anomaly Features"
ORDER BY cnt DESC
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-035/attempt-01/sql/S32.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-035/attempt-01/sql/S32.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-035/attempt-01/results/S32.rows.jsonl)；完整：True；SHA256：`99b6dffd6e838f6b4cd518f3ea31413aa3351df01d18e8c1f70cb53f71d841db`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "a", "kind": "base", "block": null, "base_tables": ["abnormal_logins_table"]}, {"alias": "l", "kind": "base", "block": null, "base_tables": ["login_records_table"]}, {"alias": "u", "kind": "base", "block": null, "base_tables": ["user_information_table"]}] | [{"type": "INNER", "right": "login_records_table AS l", "on": "a.\"Login Record ID\" = l.\"Login Record ID\"", "using": []}, {"type": "INNER", "right": "user_information_table AS u", "on": "l.\"User ID\" = u.\"User ID\"", "using": []}] | ["u.Department", "a.\"Anomaly Features\""] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |


## S33

类别 `data`；来源 `query_db`；调用 `8e0f1a617cca4bbc8ef5b749c803bc8a`；状态 `success`。

```sql
SELECT 
  u.Department,
  ROUND(AVG(a."Anomaly Score"), 2) AS avg_anomaly_score,
  ROUND(AVG(CASE WHEN a."Risk Level" IN ('High', 'Severe') THEN a."Anomaly Score" ELSE NULL END), 2) AS avg_high_severe_score,
  ROUND(100.0 * SUM(CASE WHEN a."Risk Level" IN ('High', 'Severe') THEN 1 ELSE 0 END) / COUNT(*), 1) AS pct_high_severe,
  ROUND(100.0 * SUM(CASE WHEN a."Confirmation Status" = 'Confirmed' THEN 1 ELSE 0 END) / COUNT(*), 1) AS pct_confirmed
FROM abnormal_logins_table a
JOIN login_records_table l ON a."Login Record ID" = l."Login Record ID"
JOIN user_information_table u ON l."User ID" = u."User ID"
GROUP BY u.Department
ORDER BY pct_high_severe DESC
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-035/attempt-01/sql/S33.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-035/attempt-01/sql/S33.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-035/attempt-01/results/S33.rows.jsonl)；完整：True；SHA256：`2d1e932801f800c5f45a1bab8833022b167abd47b29492a6fbd0c5d71356b8e0`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "a", "kind": "base", "block": null, "base_tables": ["abnormal_logins_table"]}, {"alias": "l", "kind": "base", "block": null, "base_tables": ["login_records_table"]}, {"alias": "u", "kind": "base", "block": null, "base_tables": ["user_information_table"]}] | [{"type": "INNER", "right": "login_records_table AS l", "on": "a.\"Login Record ID\" = l.\"Login Record ID\"", "using": []}, {"type": "INNER", "right": "user_information_table AS u", "on": "l.\"User ID\" = u.\"User ID\"", "using": []}] | ["u.Department"] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | AVG(a."Anomaly Score") | [{"table": "abnormal_logins_table", "column": "Anomaly Score"}] | [] | False |
| B1 | AVG(CASE WHEN a."Risk Level" IN ('High', 'Severe') THEN a."Anomaly Score" ELSE NULL END) | [{"table": "abnormal_logins_table", "column": "Anomaly Score"}] | [{"table": "abnormal_logins_table", "column": "Risk Level"}] | False |
| B1 | COUNT(*) | [] | [] | True |
| B1 | COUNT(*) | [] | [] | True |
| B1 | SUM(CASE WHEN a."Risk Level" IN ('High', 'Severe') THEN 1 ELSE 0 END) | [] | [{"table": "abnormal_logins_table", "column": "Risk Level"}] | False |
| B1 | SUM(CASE WHEN a."Confirmation Status" = 'Confirmed' THEN 1 ELSE 0 END) | [] | [{"table": "abnormal_logins_table", "column": "Confirmation Status"}] | False |


## S34

类别 `data`；来源 `query_db`；调用 `66b23b49fa514636a7f305687356af17`；状态 `success`。

```sql
SELECT 
  u.Department,
  sl."Log Level",
  COUNT(*) AS cnt
FROM system_logs_table sl
JOIN login_records_table l ON sl."Login Record ID" = l."Login Record ID"
JOIN user_information_table u ON l."User ID" = u."User ID"
GROUP BY u.Department, sl."Log Level"
ORDER BY u.Department, sl."Log Level"
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-035/attempt-01/sql/S34.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-035/attempt-01/sql/S34.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-035/attempt-01/results/S34.rows.jsonl)；完整：True；SHA256：`08e815d736c16bfb05f600ca74b69ce3e93196f07b931e8a273eec657996ca24`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "sl", "kind": "base", "block": null, "base_tables": ["system_logs_table"]}, {"alias": "l", "kind": "base", "block": null, "base_tables": ["login_records_table"]}, {"alias": "u", "kind": "base", "block": null, "base_tables": ["user_information_table"]}] | [{"type": "INNER", "right": "login_records_table AS l", "on": "sl.\"Login Record ID\" = l.\"Login Record ID\"", "using": []}, {"type": "INNER", "right": "user_information_table AS u", "on": "l.\"User ID\" = u.\"User ID\"", "using": []}] | ["u.Department", "sl.\"Log Level\""] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |


## S35

类别 `data`；来源 `query_db`；调用 `2f5b79491e2f482381125362dcddfbdd`；状态 `success`。

```sql
SELECT DISTINCT "Log Level" FROM system_logs_table
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-035/attempt-01/sql/S35.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-035/attempt-01/sql/S35.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-035/attempt-01/results/S35.rows.jsonl)；完整：True；SHA256：`10e9e6fe9d879bd8fd2354289e25cd7bf48369d352d2811e4f34ee32ffbe4142`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "system_logs_table", "kind": "base", "block": null, "base_tables": ["system_logs_table"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |


## S36

类别 `data`；来源 `query_db`；调用 `82be37e6f95e4d8a8d84985a0883bfa7`；状态 `success`。

```sql
SELECT DISTINCT "Log Type" FROM system_logs_table
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-035/attempt-01/sql/S36.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-035/attempt-01/sql/S36.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-035/attempt-01/results/S36.rows.jsonl)；完整：True；SHA256：`659e1df2d7035120543949680e4c0fcb6782c96ea450512832c982466669e104`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "system_logs_table", "kind": "base", "block": null, "base_tables": ["system_logs_table"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |


## S37

类别 `data`；来源 `query_db`；调用 `857190abec474ba1b5fc5455fcc2ab23`；状态 `success`。

```sql
SELECT 
  u.Department,
  nc."VPN Status",
  nc."Proxy Status",
  nc."Firewall Status",
  COUNT(*) AS cnt
FROM network_connections_table nc
JOIN login_records_table l ON nc."Login Record ID" = l."Login Record ID"
JOIN user_information_table u ON l."User ID" = u."User ID"
GROUP BY u.Department, nc."VPN Status", nc."Proxy Status", nc."Firewall Status"
ORDER BY u.Department, cnt DESC
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-035/attempt-01/sql/S37.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-035/attempt-01/sql/S37.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-035/attempt-01/results/S37.rows.jsonl)；完整：True；SHA256：`c41af9635eecd4745a103b495d2282bd71fc186eae6a549f0fe8eb74b6e9c534`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "nc", "kind": "base", "block": null, "base_tables": ["network_connections_table"]}, {"alias": "l", "kind": "base", "block": null, "base_tables": ["login_records_table"]}, {"alias": "u", "kind": "base", "block": null, "base_tables": ["user_information_table"]}] | [{"type": "INNER", "right": "login_records_table AS l", "on": "nc.\"Login Record ID\" = l.\"Login Record ID\"", "using": []}, {"type": "INNER", "right": "user_information_table AS u", "on": "l.\"User ID\" = u.\"User ID\"", "using": []}] | ["u.Department", "nc.\"VPN Status\"", "nc.\"Proxy Status\"", "nc.\"Firewall Status\""] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |


## S38

类别 `data`；来源 `query_db`；调用 `2bf37fb51b204d7bbd921fe93ba20cfe`；状态 `success`。

```sql
SELECT DISTINCT "VPN Status" FROM network_connections_table
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-035/attempt-01/sql/S38.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-035/attempt-01/sql/S38.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-035/attempt-01/results/S38.rows.jsonl)；完整：True；SHA256：`6d12e1fa1b37f0561f48ff88d96e17d638f8e2eb9053937d626a2fea5c3d85f4`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "network_connections_table", "kind": "base", "block": null, "base_tables": ["network_connections_table"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |


## S39

类别 `data`；来源 `query_db`；调用 `b2b24eaebbda431292765a170d846c28`；状态 `success`。

```sql
SELECT 
  u.Department,
  COUNT(*) AS total_connections,
  SUM(CASE WHEN nc."VPN Status" = 'Not Connected' THEN 1 ELSE 0 END) AS no_vpn,
  SUM(CASE WHEN nc."Proxy Status" = 'Closed' THEN 1 ELSE 0 END) AS proxy_closed,
  SUM(CASE WHEN nc."Firewall Status" = 'Closed' THEN 1 ELSE 0 END) AS firewall_closed,
  ROUND(100.0 * SUM(CASE WHEN nc."VPN Status" = 'Not Connected' THEN 1 ELSE 0 END) / COUNT(*), 1) AS pct_no_vpn,
  ROUND(100.0 * SUM(CASE WHEN nc."Firewall Status" = 'Closed' THEN 1 ELSE 0 END) / COUNT(*), 1) AS pct_firewall_closed
FROM network_connections_table nc
JOIN login_records_table l ON nc."Login Record ID" = l."Login Record ID"
JOIN user_information_table u ON l."User ID" = u."User ID"
GROUP BY u.Department
ORDER BY pct_no_vpn DESC
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-035/attempt-01/sql/S39.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-035/attempt-01/sql/S39.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-035/attempt-01/results/S39.rows.jsonl)；完整：True；SHA256：`0fb8496a3695af2e81fcf279dc18aafe570cbd97fc982b7c5b21186540b61f07`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "nc", "kind": "base", "block": null, "base_tables": ["network_connections_table"]}, {"alias": "l", "kind": "base", "block": null, "base_tables": ["login_records_table"]}, {"alias": "u", "kind": "base", "block": null, "base_tables": ["user_information_table"]}] | [{"type": "INNER", "right": "login_records_table AS l", "on": "nc.\"Login Record ID\" = l.\"Login Record ID\"", "using": []}, {"type": "INNER", "right": "user_information_table AS u", "on": "l.\"User ID\" = u.\"User ID\"", "using": []}] | ["u.Department"] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |
| B1 | SUM(CASE WHEN nc."VPN Status" = 'Not Connected' THEN 1 ELSE 0 END) | [] | [{"table": "network_connections_table", "column": "VPN Status"}] | False |
| B1 | SUM(CASE WHEN nc."Proxy Status" = 'Closed' THEN 1 ELSE 0 END) | [] | [{"table": "network_connections_table", "column": "Proxy Status"}] | False |
| B1 | SUM(CASE WHEN nc."Firewall Status" = 'Closed' THEN 1 ELSE 0 END) | [] | [{"table": "network_connections_table", "column": "Firewall Status"}] | False |
| B1 | COUNT(*) | [] | [] | True |
| B1 | COUNT(*) | [] | [] | True |
| B1 | SUM(CASE WHEN nc."VPN Status" = 'Not Connected' THEN 1 ELSE 0 END) | [] | [{"table": "network_connections_table", "column": "VPN Status"}] | False |
| B1 | SUM(CASE WHEN nc."Firewall Status" = 'Closed' THEN 1 ELSE 0 END) | [] | [{"table": "network_connections_table", "column": "Firewall Status"}] | False |


## S40

类别 `data`；来源 `query_db`；调用 `dd3c5adf10c9456e8feb522c1ff02a8a`；状态 `success`。

```sql
SELECT 
  u.Department,
  l."Login Method",
  COUNT(*) AS cnt
FROM login_records_table l
JOIN user_information_table u ON l."User ID" = u."User ID"
GROUP BY u.Department, l."Login Method"
ORDER BY u.Department, cnt DESC
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-035/attempt-01/sql/S40.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-035/attempt-01/sql/S40.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-035/attempt-01/results/S40.rows.jsonl)；完整：True；SHA256：`1755554876d96ebb9890adec98376d8235d4647aeceaa54b1eaecd8ae48ea0ce`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "l", "kind": "base", "block": null, "base_tables": ["login_records_table"]}, {"alias": "u", "kind": "base", "block": null, "base_tables": ["user_information_table"]}] | [{"type": "INNER", "right": "user_information_table AS u", "on": "l.\"User ID\" = u.\"User ID\"", "using": []}] | ["u.Department", "l.\"Login Method\""] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |


## S41

类别 `data`；来源 `query_db`；调用 `863d456277d94efd83dc9fb8df349363`；状态 `success`。

```sql
SELECT 
  u.Department,
  l."Authentication Level",
  COUNT(*) AS cnt
FROM login_records_table l
JOIN user_information_table u ON l."User ID" = u."User ID"
GROUP BY u.Department, l."Authentication Level"
ORDER BY u.Department, l."Authentication Level"
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-035/attempt-01/sql/S41.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-035/attempt-01/sql/S41.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-035/attempt-01/results/S41.rows.jsonl)；完整：True；SHA256：`a586758287fd84f81c17623d57c5cb0b7935cb313b3a37c2161354876bf66b99`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "l", "kind": "base", "block": null, "base_tables": ["login_records_table"]}, {"alias": "u", "kind": "base", "block": null, "base_tables": ["user_information_table"]}] | [{"type": "INNER", "right": "user_information_table AS u", "on": "l.\"User ID\" = u.\"User ID\"", "using": []}] | ["u.Department", "l.\"Authentication Level\""] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |


## S42

类别 `data`；来源 `query_db`；调用 `a091a20b068c46c79a1baf97f7500280`；状态 `success`。

```sql
SELECT 
  u.Department,
  ip."Province",
  COUNT(*) AS cnt
FROM ip_address_information_table ip
JOIN login_records_table l ON ip."Login record ID" = l."Login Record ID"
JOIN user_information_table u ON l."User ID" = u."User ID"
GROUP BY u.Department, ip."Province"
ORDER BY u.Department, cnt DESC
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-035/attempt-01/sql/S42.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-035/attempt-01/sql/S42.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-035/attempt-01/results/S42.rows.jsonl)；完整：True；SHA256：`eb9b308d201c18565099ca2dab5df92eb4cd8654cad32c21cd009b1570f16e53`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "ip", "kind": "base", "block": null, "base_tables": ["ip_address_information_table"]}, {"alias": "l", "kind": "base", "block": null, "base_tables": ["login_records_table"]}, {"alias": "u", "kind": "base", "block": null, "base_tables": ["user_information_table"]}] | [{"type": "INNER", "right": "login_records_table AS l", "on": "ip.\"Login record ID\" = l.\"Login Record ID\"", "using": []}, {"type": "INNER", "right": "user_information_table AS u", "on": "l.\"User ID\" = u.\"User ID\"", "using": []}] | ["u.Department", "ip.\"Province\""] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |


## S43

类别 `data`；来源 `python`；调用 `6b8d6e721ab94e92aefd0a28a3df8105`；状态 `success`。

```sql
SELECT Department, COUNT(*) AS user_count FROM user_information_table GROUP BY Department
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-035/attempt-01/sql/S43.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-035/attempt-01/sql/S43.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-035/attempt-01/results/S43.rows.jsonl)；完整：True；SHA256：`4a8a8a83aabaca7f9a5e414971633557a7c8d33468180fa69b5165e584085664`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "user_information_table", "kind": "base", "block": null, "base_tables": ["user_information_table"]}] | [] | ["Department"] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |


## S44

类别 `data`；来源 `python`；调用 `6b8d6e721ab94e92aefd0a28a3df8105`；状态 `success`。

```sql

SELECT 
  u.Department,
  COUNT(*) AS anomaly_count,
  COUNT(DISTINCT l."User ID") AS users_with_anomalies,
  ROUND(AVG(a."Anomaly Score"), 2) AS avg_anomaly_score,
  ROUND(AVG(a."Device Anomaly Indicators"), 2) AS avg_device_indicator,
  ROUND(AVG(a."Network Anomaly Indicators"), 2) AS avg_network_indicator,
  ROUND(AVG(a."Behavior Anomaly Indicators"), 2) AS avg_behavior_indicator,
  ROUND(100.0 * SUM(CASE WHEN a."Risk Level" IN ('High', 'Severe') THEN 1 ELSE 0 END) / COUNT(*), 1) AS pct_high_severe,
  ROUND(100.0 * SUM(CASE WHEN a."Confirmation Status" = 'Confirmed' THEN 1 ELSE 0 END) / COUNT(*), 1) AS pct_confirmed
FROM abnormal_logins_table a
JOIN login_records_table l ON a."Login Record ID" = l."Login Record ID"
JOIN user_information_table u ON l."User ID" = u."User ID"
GROUP BY u.Department

```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-035/attempt-01/sql/S44.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-035/attempt-01/sql/S44.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-035/attempt-01/results/S44.rows.jsonl)；完整：True；SHA256：`5aa1d5cd4985732b0fb2905aef93fdc505e24b531a87e79ce371ad76419e72da`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "a", "kind": "base", "block": null, "base_tables": ["abnormal_logins_table"]}, {"alias": "l", "kind": "base", "block": null, "base_tables": ["login_records_table"]}, {"alias": "u", "kind": "base", "block": null, "base_tables": ["user_information_table"]}] | [{"type": "INNER", "right": "login_records_table AS l", "on": "a.\"Login Record ID\" = l.\"Login Record ID\"", "using": []}, {"type": "INNER", "right": "user_information_table AS u", "on": "l.\"User ID\" = u.\"User ID\"", "using": []}] | ["u.Department"] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |
| B1 | COUNT(DISTINCT l."User ID") | [{"table": "login_records_table", "column": "User ID"}] | [] | False |
| B1 | AVG(a."Anomaly Score") | [{"table": "abnormal_logins_table", "column": "Anomaly Score"}] | [] | False |
| B1 | AVG(a."Device Anomaly Indicators") | [{"table": "abnormal_logins_table", "column": "Device Anomaly Indicators"}] | [] | False |
| B1 | AVG(a."Network Anomaly Indicators") | [{"table": "abnormal_logins_table", "column": "Network Anomaly Indicators"}] | [] | False |
| B1 | AVG(a."Behavior Anomaly Indicators") | [{"table": "abnormal_logins_table", "column": "Behavior Anomaly Indicators"}] | [] | False |
| B1 | COUNT(*) | [] | [] | True |
| B1 | COUNT(*) | [] | [] | True |
| B1 | SUM(CASE WHEN a."Risk Level" IN ('High', 'Severe') THEN 1 ELSE 0 END) | [] | [{"table": "abnormal_logins_table", "column": "Risk Level"}] | False |
| B1 | SUM(CASE WHEN a."Confirmation Status" = 'Confirmed' THEN 1 ELSE 0 END) | [] | [{"table": "abnormal_logins_table", "column": "Confirmation Status"}] | False |


## S45

类别 `data`；来源 `python`；调用 `6b8d6e721ab94e92aefd0a28a3df8105`；状态 `success`。

```sql

SELECT 
  u.Department,
  COUNT(DISTINCT CASE WHEN ua.anomaly_count >= 2 THEN u."User ID" ELSE NULL END) AS repeat_users,
  SUM(CASE WHEN ua.anomaly_count >= 2 THEN ua.anomaly_count ELSE 0 END) AS repeat_anomalies
FROM (
  SELECT l."User ID", COUNT(*) AS anomaly_count
  FROM abnormal_logins_table a
  JOIN login_records_table l ON a."Login Record ID" = l."Login Record ID"
  GROUP BY l."User ID"
) ua
JOIN user_information_table u ON ua."User ID" = u."User ID"
GROUP BY u.Department

```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-035/attempt-01/sql/S45.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-035/attempt-01/sql/S45.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-035/attempt-01/results/S45.rows.jsonl)；完整：True；SHA256：`8ef2ded559d05d119d13a4865f5fa1419c47b440c387c9f0db0f01afd361aa70`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "a", "kind": "base", "block": null, "base_tables": ["abnormal_logins_table"]}, {"alias": "l", "kind": "base", "block": null, "base_tables": ["login_records_table"]}] | [{"type": "INNER", "right": "login_records_table AS l", "on": "a.\"Login Record ID\" = l.\"Login Record ID\"", "using": []}] | ["l.\"User ID\""] |
| B2 | [{"alias": "ua", "kind": "derived", "block": "B1", "base_tables": ["abnormal_logins_table", "login_records_table"]}, {"alias": "u", "kind": "base", "block": null, "base_tables": ["user_information_table"]}] | [{"type": "INNER", "right": "user_information_table AS u", "on": "ua.\"User ID\" = u.\"User ID\"", "using": []}] | ["u.Department"] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |
| B2 | COUNT(DISTINCT CASE WHEN ua.anomaly_count >= 2 THEN u."User ID" ELSE NULL END) | [{"table": "user_information_table", "column": "User ID"}] | [] | False |
| B2 | SUM(CASE WHEN ua.anomaly_count >= 2 THEN ua.anomaly_count ELSE 0 END) | [] | [] | False |


## S46

类别 `data`；来源 `python`；调用 `6b8d6e721ab94e92aefd0a28a3df8105`；状态 `success`。

```sql

SELECT 
  u.Department,
  COUNT(*) AS total_logins,
  SUM(CASE WHEN l."Authentication Status" = 'Failure' THEN 1 ELSE 0 END) AS failed_logins,
  SUM(CASE WHEN l."Two-Factor Authentication Status" = 'Not Enabled' THEN 1 ELSE 0 END) AS no_2fa_logins,
  COUNT(DISTINCT l."User ID") AS active_users
FROM login_records_table l
JOIN user_information_table u ON l."User ID" = u."User ID"
GROUP BY u.Department

```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-035/attempt-01/sql/S46.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-035/attempt-01/sql/S46.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-035/attempt-01/results/S46.rows.jsonl)；完整：True；SHA256：`e67c8567d2b993177ef8010c712e7ddbc2599a32fd92ec3412753556d797174f`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "l", "kind": "base", "block": null, "base_tables": ["login_records_table"]}, {"alias": "u", "kind": "base", "block": null, "base_tables": ["user_information_table"]}] | [{"type": "INNER", "right": "user_information_table AS u", "on": "l.\"User ID\" = u.\"User ID\"", "using": []}] | ["u.Department"] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |
| B1 | SUM(CASE WHEN l."Authentication Status" = 'Failure' THEN 1 ELSE 0 END) | [] | [{"table": "login_records_table", "column": "Authentication Status"}] | False |
| B1 | SUM(CASE WHEN l."Two-Factor Authentication Status" = 'Not Enabled' THEN 1 ELSE 0 END) | [] | [{"table": "login_records_table", "column": "Two-Factor Authentication Status"}] | False |
| B1 | COUNT(DISTINCT l."User ID") | [{"table": "login_records_table", "column": "User ID"}] | [] | False |


## S47

类别 `data`；来源 `python`；调用 `6b8d6e721ab94e92aefd0a28a3df8105`；状态 `success`。

```sql

SELECT 
  u.Department,
  AVG(ua."Password Attempt Count") AS avg_password_attempts,
  SUM(CASE WHEN ua."Account Lock Status" = 'Locked' THEN 1 ELSE 0 END) AS locked_accounts,
  COUNT(*) AS account_count
FROM user_account_table ua
JOIN user_information_table u ON ua."User ID" = u."User ID"
GROUP BY u.Department

```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-035/attempt-01/sql/S47.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-035/attempt-01/sql/S47.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-035/attempt-01/results/S47.rows.jsonl)；完整：True；SHA256：`953a984ce6125a0dac2b2e7c294f91420d7270ed9ae34f9cdafc4419b13027d8`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "ua", "kind": "base", "block": null, "base_tables": ["user_account_table"]}, {"alias": "u", "kind": "base", "block": null, "base_tables": ["user_information_table"]}] | [{"type": "INNER", "right": "user_information_table AS u", "on": "ua.\"User ID\" = u.\"User ID\"", "using": []}] | ["u.Department"] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | AVG(ua."Password Attempt Count") | [{"table": "user_account_table", "column": "Password Attempt Count"}] | [] | False |
| B1 | SUM(CASE WHEN ua."Account Lock Status" = 'Locked' THEN 1 ELSE 0 END) | [] | [{"table": "user_account_table", "column": "Account Lock Status"}] | False |
| B1 | COUNT(*) | [] | [] | True |


## S48

类别 `data`；来源 `python`；调用 `6b8d6e721ab94e92aefd0a28a3df8105`；状态 `success`。

```sql

SELECT 
  u.Department,
  COUNT(*) AS total_events,
  SUM(CASE WHEN se."Severity" IN ('High', 'Severe') THEN 1 ELSE 0 END) AS high_sev_events,
  AVG(se."Risk Score") AS avg_risk_score
FROM security_events_table se
JOIN login_records_table l ON se."Login Record ID" = l."Login Record ID"
JOIN user_information_table u ON l."User ID" = u."User ID"
GROUP BY u.Department

```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-035/attempt-01/sql/S48.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-035/attempt-01/sql/S48.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-035/attempt-01/results/S48.rows.jsonl)；完整：True；SHA256：`80733275062a3955fb1713a0e87f11d6b85062e6f78c5018e1a47ab5f4eff132`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "se", "kind": "base", "block": null, "base_tables": ["security_events_table"]}, {"alias": "l", "kind": "base", "block": null, "base_tables": ["login_records_table"]}, {"alias": "u", "kind": "base", "block": null, "base_tables": ["user_information_table"]}] | [{"type": "INNER", "right": "login_records_table AS l", "on": "se.\"Login Record ID\" = l.\"Login Record ID\"", "using": []}, {"type": "INNER", "right": "user_information_table AS u", "on": "l.\"User ID\" = u.\"User ID\"", "using": []}] | ["u.Department"] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |
| B1 | SUM(CASE WHEN se."Severity" IN ('High', 'Severe') THEN 1 ELSE 0 END) | [] | [{"table": "security_events_table", "column": "Severity"}] | False |
| B1 | AVG(se."Risk Score") | [{"table": "security_events_table", "column": "Risk Score"}] | [] | False |


## S49

类别 `data`；来源 `python`；调用 `c8c18e7ba3834e3bbdce91311032ff17`；状态 `success`。

```sql
SELECT Department, COUNT(*) AS user_count FROM user_information_table GROUP BY Department
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-035/attempt-01/sql/S49.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-035/attempt-01/sql/S49.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-035/attempt-01/results/S49.rows.jsonl)；完整：True；SHA256：`4a8a8a83aabaca7f9a5e414971633557a7c8d33468180fa69b5165e584085664`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "user_information_table", "kind": "base", "block": null, "base_tables": ["user_information_table"]}] | [] | ["Department"] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |


## S50

类别 `data`；来源 `python`；调用 `c8c18e7ba3834e3bbdce91311032ff17`；状态 `success`。

```sql

SELECT u.Department, COUNT(*) AS anomaly_count
FROM abnormal_logins_table a
JOIN login_records_table l ON a."Login Record ID" = l."Login Record ID"
JOIN user_information_table u ON l."User ID" = u."User ID"
GROUP BY u.Department
ORDER BY anomaly_count DESC

```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-035/attempt-01/sql/S50.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-035/attempt-01/sql/S50.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-035/attempt-01/results/S50.rows.jsonl)；完整：True；SHA256：`0e00f1349f6885f9aeda5a10b348587dd64b130d189308811e62ec76f971e5b7`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "a", "kind": "base", "block": null, "base_tables": ["abnormal_logins_table"]}, {"alias": "l", "kind": "base", "block": null, "base_tables": ["login_records_table"]}, {"alias": "u", "kind": "base", "block": null, "base_tables": ["user_information_table"]}] | [{"type": "INNER", "right": "login_records_table AS l", "on": "a.\"Login Record ID\" = l.\"Login Record ID\"", "using": []}, {"type": "INNER", "right": "user_information_table AS u", "on": "l.\"User ID\" = u.\"User ID\"", "using": []}] | ["u.Department"] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |


## S51

类别 `data`；来源 `python`；调用 `c8c18e7ba3834e3bbdce91311032ff17`；状态 `success`。

```sql

SELECT u.Department, a."Risk Level", COUNT(*) AS cnt
FROM abnormal_logins_table a
JOIN login_records_table l ON a."Login Record ID" = l."Login Record ID"
JOIN user_information_table u ON l."User ID" = u."User ID"
GROUP BY u.Department, a."Risk Level"
ORDER BY u.Department, a."Risk Level"

```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-035/attempt-01/sql/S51.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-035/attempt-01/sql/S51.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-035/attempt-01/results/S51.rows.jsonl)；完整：True；SHA256：`3961f570f2642e998c0852641d28cfd78b356fa192491e642d0845fda5348cc4`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "a", "kind": "base", "block": null, "base_tables": ["abnormal_logins_table"]}, {"alias": "l", "kind": "base", "block": null, "base_tables": ["login_records_table"]}, {"alias": "u", "kind": "base", "block": null, "base_tables": ["user_information_table"]}] | [{"type": "INNER", "right": "login_records_table AS l", "on": "a.\"Login Record ID\" = l.\"Login Record ID\"", "using": []}, {"type": "INNER", "right": "user_information_table AS u", "on": "l.\"User ID\" = u.\"User ID\"", "using": []}] | ["u.Department", "a.\"Risk Level\""] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |


## S52

类别 `data`；来源 `python`；调用 `c8c18e7ba3834e3bbdce91311032ff17`；状态 `success`。

```sql

SELECT u.Department, a."Anomaly Type", COUNT(*) AS cnt
FROM abnormal_logins_table a
JOIN login_records_table l ON a."Login Record ID" = l."Login Record ID"
JOIN user_information_table u ON l."User ID" = u."User ID"
GROUP BY u.Department, a."Anomaly Type"
ORDER BY u.Department, a."Anomaly Type"

```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-035/attempt-01/sql/S52.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-035/attempt-01/sql/S52.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-035/attempt-01/results/S52.rows.jsonl)；完整：True；SHA256：`1eea26781fae46c826653afd5dcd129836e9d3c956ba497797f4c06c09a03305`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "a", "kind": "base", "block": null, "base_tables": ["abnormal_logins_table"]}, {"alias": "l", "kind": "base", "block": null, "base_tables": ["login_records_table"]}, {"alias": "u", "kind": "base", "block": null, "base_tables": ["user_information_table"]}] | [{"type": "INNER", "right": "login_records_table AS l", "on": "a.\"Login Record ID\" = l.\"Login Record ID\"", "using": []}, {"type": "INNER", "right": "user_information_table AS u", "on": "l.\"User ID\" = u.\"User ID\"", "using": []}] | ["u.Department", "a.\"Anomaly Type\""] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |


## S53

类别 `data`；来源 `python`；调用 `c8c18e7ba3834e3bbdce91311032ff17`；状态 `success`。

```sql

SELECT 
  u.Department,
  COUNT(*) AS total_logins,
  SUM(CASE WHEN l."Authentication Status" = 'Failure' THEN 1 ELSE 0 END) AS failed_logins,
  SUM(CASE WHEN l."Two-Factor Authentication Status" = 'Not Enabled' THEN 1 ELSE 0 END) AS no_2fa_logins,
  COUNT(DISTINCT l."User ID") AS active_users
FROM login_records_table l
JOIN user_information_table u ON l."User ID" = u."User ID"
GROUP BY u.Department

```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-035/attempt-01/sql/S53.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-035/attempt-01/sql/S53.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-035/attempt-01/results/S53.rows.jsonl)；完整：True；SHA256：`e67c8567d2b993177ef8010c712e7ddbc2599a32fd92ec3412753556d797174f`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "l", "kind": "base", "block": null, "base_tables": ["login_records_table"]}, {"alias": "u", "kind": "base", "block": null, "base_tables": ["user_information_table"]}] | [{"type": "INNER", "right": "user_information_table AS u", "on": "l.\"User ID\" = u.\"User ID\"", "using": []}] | ["u.Department"] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |
| B1 | SUM(CASE WHEN l."Authentication Status" = 'Failure' THEN 1 ELSE 0 END) | [] | [{"table": "login_records_table", "column": "Authentication Status"}] | False |
| B1 | SUM(CASE WHEN l."Two-Factor Authentication Status" = 'Not Enabled' THEN 1 ELSE 0 END) | [] | [{"table": "login_records_table", "column": "Two-Factor Authentication Status"}] | False |
| B1 | COUNT(DISTINCT l."User ID") | [{"table": "login_records_table", "column": "User ID"}] | [] | False |


## S54

类别 `data`；来源 `python`；调用 `c8c18e7ba3834e3bbdce91311032ff17`；状态 `success`。

```sql

SELECT 
  u.Department,
  COUNT(DISTINCT CASE WHEN ua.anomaly_count >= 2 THEN u."User ID" ELSE NULL END) AS repeat_users,
  COUNT(DISTINCT u."User ID") AS total_users_with_anomalies
FROM (
  SELECT l."User ID", COUNT(*) AS anomaly_count
  FROM abnormal_logins_table a
  JOIN login_records_table l ON a."Login Record ID" = l."Login Record ID"
  GROUP BY l."User ID"
) ua
JOIN user_information_table u ON ua."User ID" = u."User ID"
GROUP BY u.Department

```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-035/attempt-01/sql/S54.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-035/attempt-01/sql/S54.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-035/attempt-01/results/S54.rows.jsonl)；完整：True；SHA256：`a77393eb0fa062f13bf9a9f22da48a2fce6be2e98f2be53fb4282b0f6bd9f320`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "a", "kind": "base", "block": null, "base_tables": ["abnormal_logins_table"]}, {"alias": "l", "kind": "base", "block": null, "base_tables": ["login_records_table"]}] | [{"type": "INNER", "right": "login_records_table AS l", "on": "a.\"Login Record ID\" = l.\"Login Record ID\"", "using": []}] | ["l.\"User ID\""] |
| B2 | [{"alias": "ua", "kind": "derived", "block": "B1", "base_tables": ["abnormal_logins_table", "login_records_table"]}, {"alias": "u", "kind": "base", "block": null, "base_tables": ["user_information_table"]}] | [{"type": "INNER", "right": "user_information_table AS u", "on": "ua.\"User ID\" = u.\"User ID\"", "using": []}] | ["u.Department"] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |
| B2 | COUNT(DISTINCT CASE WHEN ua.anomaly_count >= 2 THEN u."User ID" ELSE NULL END) | [{"table": "user_information_table", "column": "User ID"}] | [] | False |
| B2 | COUNT(DISTINCT u."User ID") | [{"table": "user_information_table", "column": "User ID"}] | [] | False |


## S55

类别 `data`；来源 `python`；调用 `c8c18e7ba3834e3bbdce91311032ff17`；状态 `success`。

```sql

SELECT 
  u.Department,
  AVG(ua."Password Attempt Count") AS avg_password_attempts,
  SUM(CASE WHEN ua."Account Lock Status" = 'Locked' THEN 1 ELSE 0 END) AS locked_accounts,
  COUNT(*) AS account_count
FROM user_account_table ua
JOIN user_information_table u ON ua."User ID" = u."User ID"
GROUP BY u.Department

```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-035/attempt-01/sql/S55.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-035/attempt-01/sql/S55.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-035/attempt-01/results/S55.rows.jsonl)；完整：True；SHA256：`953a984ce6125a0dac2b2e7c294f91420d7270ed9ae34f9cdafc4419b13027d8`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "ua", "kind": "base", "block": null, "base_tables": ["user_account_table"]}, {"alias": "u", "kind": "base", "block": null, "base_tables": ["user_information_table"]}] | [{"type": "INNER", "right": "user_information_table AS u", "on": "ua.\"User ID\" = u.\"User ID\"", "using": []}] | ["u.Department"] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | AVG(ua."Password Attempt Count") | [{"table": "user_account_table", "column": "Password Attempt Count"}] | [] | False |
| B1 | SUM(CASE WHEN ua."Account Lock Status" = 'Locked' THEN 1 ELSE 0 END) | [] | [{"table": "user_account_table", "column": "Account Lock Status"}] | False |
| B1 | COUNT(*) | [] | [] | True |


## S56

类别 `data`；来源 `python`；调用 `ea46dbfbe80b44e2bdfd942188188526`；状态 `success`。

```sql
SELECT Department, COUNT(*) AS user_count FROM user_information_table GROUP BY Department
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-035/attempt-01/sql/S56.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-035/attempt-01/sql/S56.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-035/attempt-01/results/S56.rows.jsonl)；完整：True；SHA256：`4a8a8a83aabaca7f9a5e414971633557a7c8d33468180fa69b5165e584085664`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "user_information_table", "kind": "base", "block": null, "base_tables": ["user_information_table"]}] | [] | ["Department"] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |


## S57

类别 `data`；来源 `python`；调用 `ea46dbfbe80b44e2bdfd942188188526`；状态 `success`。

```sql

SELECT u.Department AS dept, COUNT(*) AS anomaly_count
FROM abnormal_logins_table a
JOIN login_records_table l ON a."Login Record ID" = l."Login Record ID"
JOIN user_information_table u ON l."User ID" = u."User ID"
GROUP BY u.Department

```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-035/attempt-01/sql/S57.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-035/attempt-01/sql/S57.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-035/attempt-01/results/S57.rows.jsonl)；完整：True；SHA256：`c52cbcec8883fa7e5dce8294e99990118974977b746166f3ee6c57eb27000a34`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "a", "kind": "base", "block": null, "base_tables": ["abnormal_logins_table"]}, {"alias": "l", "kind": "base", "block": null, "base_tables": ["login_records_table"]}, {"alias": "u", "kind": "base", "block": null, "base_tables": ["user_information_table"]}] | [{"type": "INNER", "right": "login_records_table AS l", "on": "a.\"Login Record ID\" = l.\"Login Record ID\"", "using": []}, {"type": "INNER", "right": "user_information_table AS u", "on": "l.\"User ID\" = u.\"User ID\"", "using": []}] | ["u.Department"] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |


## S58

类别 `data`；来源 `python`；调用 `ea46dbfbe80b44e2bdfd942188188526`；状态 `success`。

```sql

SELECT u.Department AS dept, a."Risk Level" AS rl, COUNT(*) AS cnt
FROM abnormal_logins_table a
JOIN login_records_table l ON a."Login Record ID" = l."Login Record ID"
JOIN user_information_table u ON l."User ID" = u."User ID"
GROUP BY u.Department, a."Risk Level"

```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-035/attempt-01/sql/S58.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-035/attempt-01/sql/S58.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-035/attempt-01/results/S58.rows.jsonl)；完整：True；SHA256：`3961f570f2642e998c0852641d28cfd78b356fa192491e642d0845fda5348cc4`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "a", "kind": "base", "block": null, "base_tables": ["abnormal_logins_table"]}, {"alias": "l", "kind": "base", "block": null, "base_tables": ["login_records_table"]}, {"alias": "u", "kind": "base", "block": null, "base_tables": ["user_information_table"]}] | [{"type": "INNER", "right": "login_records_table AS l", "on": "a.\"Login Record ID\" = l.\"Login Record ID\"", "using": []}, {"type": "INNER", "right": "user_information_table AS u", "on": "l.\"User ID\" = u.\"User ID\"", "using": []}] | ["u.Department", "a.\"Risk Level\""] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |


## S59

类别 `data`；来源 `python`；调用 `ea46dbfbe80b44e2bdfd942188188526`；状态 `success`。

```sql

SELECT u.Department AS dept,
  COUNT(*) AS total_logins,
  SUM(CASE WHEN l."Authentication Status" = 'Failure' THEN 1 ELSE 0 END) AS failed_logins,
  SUM(CASE WHEN l."Two-Factor Authentication Status" = 'Not Enabled' THEN 1 ELSE 0 END) AS no_2fa_logins
FROM login_records_table l
JOIN user_information_table u ON l."User ID" = u."User ID"
GROUP BY u.Department

```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-035/attempt-01/sql/S59.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-035/attempt-01/sql/S59.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-035/attempt-01/results/S59.rows.jsonl)；完整：True；SHA256：`0088fb3c0fc0fd489dfe96d5e4593566768841e297932e52026cedffc40749d8`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "l", "kind": "base", "block": null, "base_tables": ["login_records_table"]}, {"alias": "u", "kind": "base", "block": null, "base_tables": ["user_information_table"]}] | [{"type": "INNER", "right": "user_information_table AS u", "on": "l.\"User ID\" = u.\"User ID\"", "using": []}] | ["u.Department"] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |
| B1 | SUM(CASE WHEN l."Authentication Status" = 'Failure' THEN 1 ELSE 0 END) | [] | [{"table": "login_records_table", "column": "Authentication Status"}] | False |
| B1 | SUM(CASE WHEN l."Two-Factor Authentication Status" = 'Not Enabled' THEN 1 ELSE 0 END) | [] | [{"table": "login_records_table", "column": "Two-Factor Authentication Status"}] | False |


## S60

类别 `data`；来源 `python`；调用 `ea46dbfbe80b44e2bdfd942188188526`；状态 `success`。

```sql

SELECT u.Department AS dept,
  COUNT(DISTINCT CASE WHEN ua.anomaly_count >= 2 THEN u."User ID" ELSE NULL END) AS repeat_users,
  COUNT(DISTINCT u."User ID") AS total_users_with_anomalies
FROM (
  SELECT l."User ID", COUNT(*) AS anomaly_count
  FROM abnormal_logins_table a
  JOIN login_records_table l ON a."Login Record ID" = l."Login Record ID"
  GROUP BY l."User ID"
) ua
JOIN user_information_table u ON ua."User ID" = u."User ID"
GROUP BY u.Department

```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-035/attempt-01/sql/S60.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-035/attempt-01/sql/S60.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-035/attempt-01/results/S60.rows.jsonl)；完整：True；SHA256：`a77393eb0fa062f13bf9a9f22da48a2fce6be2e98f2be53fb4282b0f6bd9f320`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "a", "kind": "base", "block": null, "base_tables": ["abnormal_logins_table"]}, {"alias": "l", "kind": "base", "block": null, "base_tables": ["login_records_table"]}] | [{"type": "INNER", "right": "login_records_table AS l", "on": "a.\"Login Record ID\" = l.\"Login Record ID\"", "using": []}] | ["l.\"User ID\""] |
| B2 | [{"alias": "ua", "kind": "derived", "block": "B1", "base_tables": ["abnormal_logins_table", "login_records_table"]}, {"alias": "u", "kind": "base", "block": null, "base_tables": ["user_information_table"]}] | [{"type": "INNER", "right": "user_information_table AS u", "on": "ua.\"User ID\" = u.\"User ID\"", "using": []}] | ["u.Department"] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |
| B2 | COUNT(DISTINCT CASE WHEN ua.anomaly_count >= 2 THEN u."User ID" ELSE NULL END) | [{"table": "user_information_table", "column": "User ID"}] | [] | False |
| B2 | COUNT(DISTINCT u."User ID") | [{"table": "user_information_table", "column": "User ID"}] | [] | False |


## S61

类别 `data`；来源 `python`；调用 `ea46dbfbe80b44e2bdfd942188188526`；状态 `success`。

```sql

SELECT u.Department AS dept,
  AVG(ua."Password Attempt Count") AS avg_pw,
  SUM(CASE WHEN ua."Account Lock Status" = 'Locked' THEN 1 ELSE 0 END) AS locked,
  COUNT(*) AS acct_count
FROM user_account_table ua
JOIN user_information_table u ON ua."User ID" = u."User ID"
GROUP BY u.Department

```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-035/attempt-01/sql/S61.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-035/attempt-01/sql/S61.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-035/attempt-01/results/S61.rows.jsonl)；完整：True；SHA256：`953a984ce6125a0dac2b2e7c294f91420d7270ed9ae34f9cdafc4419b13027d8`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "ua", "kind": "base", "block": null, "base_tables": ["user_account_table"]}, {"alias": "u", "kind": "base", "block": null, "base_tables": ["user_information_table"]}] | [{"type": "INNER", "right": "user_information_table AS u", "on": "ua.\"User ID\" = u.\"User ID\"", "using": []}] | ["u.Department"] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | AVG(ua."Password Attempt Count") | [{"table": "user_account_table", "column": "Password Attempt Count"}] | [] | False |
| B1 | SUM(CASE WHEN ua."Account Lock Status" = 'Locked' THEN 1 ELSE 0 END) | [] | [{"table": "user_account_table", "column": "Account Lock Status"}] | False |
| B1 | COUNT(*) | [] | [] | True |


## S62

类别 `data`；来源 `python`；调用 `ea46dbfbe80b44e2bdfd942188188526`；状态 `success`。

```sql

SELECT u.Department AS dept, AVG(a."Anomaly Score") AS avg_score
FROM abnormal_logins_table a
JOIN login_records_table l ON a."Login Record ID" = l."Login Record ID"
JOIN user_information_table u ON l."User ID" = u."User ID"
GROUP BY u.Department

```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-035/attempt-01/sql/S62.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-035/attempt-01/sql/S62.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-035/attempt-01/results/S62.rows.jsonl)；完整：True；SHA256：`73dea1f5d395bdd17a4bdbbfdb69beb184e31a1d5afb4fceb57ffe71e6550fd4`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "a", "kind": "base", "block": null, "base_tables": ["abnormal_logins_table"]}, {"alias": "l", "kind": "base", "block": null, "base_tables": ["login_records_table"]}, {"alias": "u", "kind": "base", "block": null, "base_tables": ["user_information_table"]}] | [{"type": "INNER", "right": "login_records_table AS l", "on": "a.\"Login Record ID\" = l.\"Login Record ID\"", "using": []}, {"type": "INNER", "right": "user_information_table AS u", "on": "l.\"User ID\" = u.\"User ID\"", "using": []}] | ["u.Department"] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | AVG(a."Anomaly Score") | [{"table": "abnormal_logins_table", "column": "Anomaly Score"}] | [] | False |


## S63

类别 `data`；来源 `python`；调用 `ea46dbfbe80b44e2bdfd942188188526`；状态 `success`。

```sql

SELECT u.Department AS dept, COUNT(*) AS event_count
FROM security_events_table se
JOIN login_records_table l ON se."Login Record ID" = l."Login Record ID"
JOIN user_information_table u ON l."User ID" = u."User ID"
GROUP BY u.Department

```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-035/attempt-01/sql/S63.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-035/attempt-01/sql/S63.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-035/attempt-01/results/S63.rows.jsonl)；完整：True；SHA256：`7f22dc00e0c91d03d0eda93be56d7defa1144b69ba10811e07084faa99e49bde`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "se", "kind": "base", "block": null, "base_tables": ["security_events_table"]}, {"alias": "l", "kind": "base", "block": null, "base_tables": ["login_records_table"]}, {"alias": "u", "kind": "base", "block": null, "base_tables": ["user_information_table"]}] | [{"type": "INNER", "right": "login_records_table AS l", "on": "se.\"Login Record ID\" = l.\"Login Record ID\"", "using": []}, {"type": "INNER", "right": "user_information_table AS u", "on": "l.\"User ID\" = u.\"User ID\"", "using": []}] | ["u.Department"] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |


## S64

类别 `data`；来源 `python`；调用 `d1e513c6024e4ee098e13b47704f7848`；状态 `success`。

```sql

SELECT u.Department AS dept, a."Anomaly Score" AS score, a."Risk Level" AS risk,
       a."Device Anomaly Indicators" AS dev, a."Network Anomaly Indicators" AS net,
       a."Behavior Anomaly Indicators" AS beh
FROM abnormal_logins_table a
JOIN login_records_table l ON a."Login Record ID" = l."Login Record ID"
JOIN user_information_table u ON l."User ID" = u."User ID"

```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-035/attempt-01/sql/S64.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-035/attempt-01/sql/S64.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-035/attempt-01/results/S64.rows.jsonl)；完整：True；SHA256：`a49c524d30e0428ff35b844d292e6ed893d5a55848fcec2fb2a439ceeefaf693`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "a", "kind": "base", "block": null, "base_tables": ["abnormal_logins_table"]}, {"alias": "l", "kind": "base", "block": null, "base_tables": ["login_records_table"]}, {"alias": "u", "kind": "base", "block": null, "base_tables": ["user_information_table"]}] | [{"type": "INNER", "right": "login_records_table AS l", "on": "a.\"Login Record ID\" = l.\"Login Record ID\"", "using": []}, {"type": "INNER", "right": "user_information_table AS u", "on": "l.\"User ID\" = u.\"User ID\"", "using": []}] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |


## S65

类别 `data`；来源 `python`；调用 `d1e513c6024e4ee098e13b47704f7848`；状态 `success`。

```sql

SELECT u.Department AS dept, l."Login Duration" AS dur, l."Authentication Status" AS auth
FROM login_records_table l
JOIN user_information_table u ON l."User ID" = u."User ID"

```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-035/attempt-01/sql/S65.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-035/attempt-01/sql/S65.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-035/attempt-01/results/S65.rows.jsonl)；完整：True；SHA256：`498d94de93b9ffaa2c7d5fcd34c7a538862b60d60cd861d4adbc570f606f822d`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "l", "kind": "base", "block": null, "base_tables": ["login_records_table"]}, {"alias": "u", "kind": "base", "block": null, "base_tables": ["user_information_table"]}] | [{"type": "INNER", "right": "user_information_table AS u", "on": "l.\"User ID\" = u.\"User ID\"", "using": []}] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |


## S66

类别 `data`；来源 `python`；调用 `d1e513c6024e4ee098e13b47704f7848`；状态 `success`。

```sql

SELECT u.Department AS dept, l."Two-Factor Authentication Status" AS tfa
FROM login_records_table l
JOIN user_information_table u ON l."User ID" = u."User ID"

```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-035/attempt-01/sql/S66.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-035/attempt-01/sql/S66.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-035/attempt-01/results/S66.rows.jsonl)；完整：True；SHA256：`6c7e9e52fdfb51cdcbd15fdd4dc7b09d109540fcffe1a3995a794cadcac4adaf`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "l", "kind": "base", "block": null, "base_tables": ["login_records_table"]}, {"alias": "u", "kind": "base", "block": null, "base_tables": ["user_information_table"]}] | [{"type": "INNER", "right": "user_information_table AS u", "on": "l.\"User ID\" = u.\"User ID\"", "using": []}] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |


## S67

类别 `data`；来源 `query_db`；调用 `4007259c7a694458bafb56ccc8d31160`；状态 `success`。

```sql
SELECT 
  u.Department,
  sl."Handling Status",
  COUNT(*) AS cnt
FROM system_logs_table sl
JOIN login_records_table l ON sl."Login Record ID" = l."Login Record ID"
JOIN user_information_table u ON l."User ID" = u."User ID"
GROUP BY u.Department, sl."Handling Status"
ORDER BY u.Department
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-035/attempt-01/sql/S67.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-035/attempt-01/sql/S67.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-035/attempt-01/results/S67.rows.jsonl)；完整：True；SHA256：`49a401db1e28f33d709b7d3c76c49e8bfe42543dc821f37d27a13c0be52903a9`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "sl", "kind": "base", "block": null, "base_tables": ["system_logs_table"]}, {"alias": "l", "kind": "base", "block": null, "base_tables": ["login_records_table"]}, {"alias": "u", "kind": "base", "block": null, "base_tables": ["user_information_table"]}] | [{"type": "INNER", "right": "login_records_table AS l", "on": "sl.\"Login Record ID\" = l.\"Login Record ID\"", "using": []}, {"type": "INNER", "right": "user_information_table AS u", "on": "l.\"User ID\" = u.\"User ID\"", "using": []}] | ["u.Department", "sl.\"Handling Status\""] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |


## S68

类别 `data`；来源 `query_db`；调用 `3187eef41583462f83f32dd1bbdc9020`；状态 `success`。

```sql
SELECT DISTINCT "Handling Status" FROM system_logs_table
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-035/attempt-01/sql/S68.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-035/attempt-01/sql/S68.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-035/attempt-01/results/S68.rows.jsonl)；完整：True；SHA256：`4ab24a4d88e75a0a695783a918513f08b4bc21e4d7bc04047f2162ce9fd421ed`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "system_logs_table", "kind": "base", "block": null, "base_tables": ["system_logs_table"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |


## S69

类别 `data`；来源 `query_db`；调用 `1670bbcabd484924aa649a04a46ba9c6`；状态 `success`。

```sql
SELECT 
  u.Department,
  COUNT(*) AS remote_logins
FROM abnormal_logins_table a
JOIN login_records_table l ON a."Login Record ID" = l."Login Record ID"
JOIN user_information_table u ON l."User ID" = u."User ID"
WHERE a."Anomaly Type" = 'Remote Login'
GROUP BY u.Department
ORDER BY remote_logins DESC
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-035/attempt-01/sql/S69.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-035/attempt-01/sql/S69.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-035/attempt-01/results/S69.rows.jsonl)；完整：True；SHA256：`ebef86fb3b56079625caf85ccf43e08f6f624f4c34ea943fb3fdfc6233b8a611`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "a", "kind": "base", "block": null, "base_tables": ["abnormal_logins_table"]}, {"alias": "l", "kind": "base", "block": null, "base_tables": ["login_records_table"]}, {"alias": "u", "kind": "base", "block": null, "base_tables": ["user_information_table"]}] | [{"type": "INNER", "right": "login_records_table AS l", "on": "a.\"Login Record ID\" = l.\"Login Record ID\"", "using": []}, {"type": "INNER", "right": "user_information_table AS u", "on": "l.\"User ID\" = u.\"User ID\"", "using": []}] | ["u.Department"] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |


## S70

类别 `data`；来源 `python`；调用 `c919f2ecbc3344469fed1f0a30dd1d0c`；状态 `success`。

```sql
SELECT Department, COUNT(*) AS user_count FROM user_information_table GROUP BY Department
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-035/attempt-01/sql/S70.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-035/attempt-01/sql/S70.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-035/attempt-01/results/S70.rows.jsonl)；完整：True；SHA256：`4a8a8a83aabaca7f9a5e414971633557a7c8d33468180fa69b5165e584085664`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "user_information_table", "kind": "base", "block": null, "base_tables": ["user_information_table"]}] | [] | ["Department"] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |


## S71

类别 `data`；来源 `python`；调用 `c919f2ecbc3344469fed1f0a30dd1d0c`；状态 `success`。

```sql

SELECT u.Department AS dept, COUNT(*) AS cnt
FROM abnormal_logins_table a
JOIN login_records_table l ON a."Login Record ID" = l."Login Record ID"
JOIN user_information_table u ON l."User ID" = u."User ID"
GROUP BY u.Department

```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-035/attempt-01/sql/S71.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-035/attempt-01/sql/S71.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-035/attempt-01/results/S71.rows.jsonl)；完整：True；SHA256：`c52cbcec8883fa7e5dce8294e99990118974977b746166f3ee6c57eb27000a34`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "a", "kind": "base", "block": null, "base_tables": ["abnormal_logins_table"]}, {"alias": "l", "kind": "base", "block": null, "base_tables": ["login_records_table"]}, {"alias": "u", "kind": "base", "block": null, "base_tables": ["user_information_table"]}] | [{"type": "INNER", "right": "login_records_table AS l", "on": "a.\"Login Record ID\" = l.\"Login Record ID\"", "using": []}, {"type": "INNER", "right": "user_information_table AS u", "on": "l.\"User ID\" = u.\"User ID\"", "using": []}] | ["u.Department"] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |


## S72

类别 `data`；来源 `python`；调用 `c919f2ecbc3344469fed1f0a30dd1d0c`；状态 `success`。

```sql

SELECT u.Department AS dept, COUNT(*) AS remote_cnt
FROM abnormal_logins_table a
JOIN login_records_table l ON a."Login Record ID" = l."Login Record ID"
JOIN user_information_table u ON l."User ID" = u."User ID"
WHERE a."Anomaly Type" = 'Remote Login'
GROUP BY u.Department

```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-035/attempt-01/sql/S72.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-035/attempt-01/sql/S72.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-035/attempt-01/results/S72.rows.jsonl)；完整：True；SHA256：`36b77c26c08e152563588d297bc67cefd306cb56fe881e3bf1c8d2f55f6aeb93`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "a", "kind": "base", "block": null, "base_tables": ["abnormal_logins_table"]}, {"alias": "l", "kind": "base", "block": null, "base_tables": ["login_records_table"]}, {"alias": "u", "kind": "base", "block": null, "base_tables": ["user_information_table"]}] | [{"type": "INNER", "right": "login_records_table AS l", "on": "a.\"Login Record ID\" = l.\"Login Record ID\"", "using": []}, {"type": "INNER", "right": "user_information_table AS u", "on": "l.\"User ID\" = u.\"User ID\"", "using": []}] | ["u.Department"] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |


## S73

类别 `data`；来源 `python`；调用 `c919f2ecbc3344469fed1f0a30dd1d0c`；状态 `success`。

```sql

SELECT u.Department AS dept,
  COUNT(DISTINCT CASE WHEN ua.anomaly_count >= 2 THEN u."User ID" ELSE NULL END) AS repeat_users,
  COUNT(DISTINCT u."User ID") AS total_users_with_anomalies
FROM (
  SELECT l."User ID", COUNT(*) AS anomaly_count
  FROM abnormal_logins_table a
  JOIN login_records_table l ON a."Login Record ID" = l."Login Record ID"
  GROUP BY l."User ID"
) ua
JOIN user_information_table u ON ua."User ID" = u."User ID"
GROUP BY u.Department

```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-035/attempt-01/sql/S73.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-035/attempt-01/sql/S73.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-035/attempt-01/results/S73.rows.jsonl)；完整：True；SHA256：`a77393eb0fa062f13bf9a9f22da48a2fce6be2e98f2be53fb4282b0f6bd9f320`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "a", "kind": "base", "block": null, "base_tables": ["abnormal_logins_table"]}, {"alias": "l", "kind": "base", "block": null, "base_tables": ["login_records_table"]}] | [{"type": "INNER", "right": "login_records_table AS l", "on": "a.\"Login Record ID\" = l.\"Login Record ID\"", "using": []}] | ["l.\"User ID\""] |
| B2 | [{"alias": "ua", "kind": "derived", "block": "B1", "base_tables": ["abnormal_logins_table", "login_records_table"]}, {"alias": "u", "kind": "base", "block": null, "base_tables": ["user_information_table"]}] | [{"type": "INNER", "right": "user_information_table AS u", "on": "ua.\"User ID\" = u.\"User ID\"", "using": []}] | ["u.Department"] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |
| B2 | COUNT(DISTINCT CASE WHEN ua.anomaly_count >= 2 THEN u."User ID" ELSE NULL END) | [{"table": "user_information_table", "column": "User ID"}] | [] | False |
| B2 | COUNT(DISTINCT u."User ID") | [{"table": "user_information_table", "column": "User ID"}] | [] | False |


## S74

类别 `data`；来源 `python`；调用 `c919f2ecbc3344469fed1f0a30dd1d0c`；状态 `success`。

```sql

SELECT u.Department AS dept,
  COUNT(*) AS total_logins,
  SUM(CASE WHEN l."Authentication Status" = 'Failure' THEN 1 ELSE 0 END) AS failed,
  SUM(CASE WHEN l."Two-Factor Authentication Status" = 'Not Enabled' THEN 1 ELSE 0 END) AS no_2fa
FROM login_records_table l
JOIN user_information_table u ON l."User ID" = u."User ID"
GROUP BY u.Department

```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-035/attempt-01/sql/S74.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-035/attempt-01/sql/S74.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-035/attempt-01/results/S74.rows.jsonl)；完整：True；SHA256：`0088fb3c0fc0fd489dfe96d5e4593566768841e297932e52026cedffc40749d8`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "l", "kind": "base", "block": null, "base_tables": ["login_records_table"]}, {"alias": "u", "kind": "base", "block": null, "base_tables": ["user_information_table"]}] | [{"type": "INNER", "right": "user_information_table AS u", "on": "l.\"User ID\" = u.\"User ID\"", "using": []}] | ["u.Department"] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |
| B1 | SUM(CASE WHEN l."Authentication Status" = 'Failure' THEN 1 ELSE 0 END) | [] | [{"table": "login_records_table", "column": "Authentication Status"}] | False |
| B1 | SUM(CASE WHEN l."Two-Factor Authentication Status" = 'Not Enabled' THEN 1 ELSE 0 END) | [] | [{"table": "login_records_table", "column": "Two-Factor Authentication Status"}] | False |


## S75

类别 `data`；来源 `python`；调用 `c919f2ecbc3344469fed1f0a30dd1d0c`；状态 `success`。

```sql

SELECT u.Department AS dept,
  AVG(ua."Password Attempt Count") AS avg_pw_attempts,
  SUM(CASE WHEN ua."Account Lock Status" = 'Locked' THEN 1 ELSE 0 END) AS locked,
  COUNT(*) AS acct_count
FROM user_account_table ua
JOIN user_information_table u ON ua."User ID" = u."User ID"
GROUP BY u.Department

```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-035/attempt-01/sql/S75.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-035/attempt-01/sql/S75.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-035/attempt-01/results/S75.rows.jsonl)；完整：True；SHA256：`953a984ce6125a0dac2b2e7c294f91420d7270ed9ae34f9cdafc4419b13027d8`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "ua", "kind": "base", "block": null, "base_tables": ["user_account_table"]}, {"alias": "u", "kind": "base", "block": null, "base_tables": ["user_information_table"]}] | [{"type": "INNER", "right": "user_information_table AS u", "on": "ua.\"User ID\" = u.\"User ID\"", "using": []}] | ["u.Department"] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | AVG(ua."Password Attempt Count") | [{"table": "user_account_table", "column": "Password Attempt Count"}] | [] | False |
| B1 | SUM(CASE WHEN ua."Account Lock Status" = 'Locked' THEN 1 ELSE 0 END) | [] | [{"table": "user_account_table", "column": "Account Lock Status"}] | False |
| B1 | COUNT(*) | [] | [] | True |


## S76

类别 `data`；来源 `python`；调用 `c919f2ecbc3344469fed1f0a30dd1d0c`；状态 `success`。

```sql

SELECT u.Department AS dept,
  COUNT(*) AS total_logs,
  SUM(CASE WHEN sl."Handling Status" = 'Unprocessed' THEN 1 ELSE 0 END) AS unprocessed
FROM system_logs_table sl
JOIN login_records_table l ON sl."Login Record ID" = l."Login Record ID"
JOIN user_information_table u ON l."User ID" = u."User ID"
GROUP BY u.Department

```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-035/attempt-01/sql/S76.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-035/attempt-01/sql/S76.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-035/attempt-01/results/S76.rows.jsonl)；完整：True；SHA256：`446a9f43933ea00cc441054bfc7ae66460f549728c418d970e9a5f159cf068c8`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "sl", "kind": "base", "block": null, "base_tables": ["system_logs_table"]}, {"alias": "l", "kind": "base", "block": null, "base_tables": ["login_records_table"]}, {"alias": "u", "kind": "base", "block": null, "base_tables": ["user_information_table"]}] | [{"type": "INNER", "right": "login_records_table AS l", "on": "sl.\"Login Record ID\" = l.\"Login Record ID\"", "using": []}, {"type": "INNER", "right": "user_information_table AS u", "on": "l.\"User ID\" = u.\"User ID\"", "using": []}] | ["u.Department"] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |
| B1 | SUM(CASE WHEN sl."Handling Status" = 'Unprocessed' THEN 1 ELSE 0 END) | [] | [{"table": "system_logs_table", "column": "Handling Status"}] | False |


## S77

类别 `data`；来源 `python`；调用 `c919f2ecbc3344469fed1f0a30dd1d0c`；状态 `success`。

```sql

SELECT u.Department AS dept,
  COUNT(*) AS total_events,
  SUM(CASE WHEN se."Severity" IN ('High', 'Severe') THEN 1 ELSE 0 END) AS high_events
FROM security_events_table se
JOIN login_records_table l ON se."Login Record ID" = l."Login Record ID"
JOIN user_information_table u ON l."User ID" = u."User ID"
GROUP BY u.Department

```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-035/attempt-01/sql/S77.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-035/attempt-01/sql/S77.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-035/attempt-01/results/S77.rows.jsonl)；完整：True；SHA256：`963f51fb25d1a132b1e287ce0aa0f7905d11679cbbe62e9c82d049db0daf6ad7`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "se", "kind": "base", "block": null, "base_tables": ["security_events_table"]}, {"alias": "l", "kind": "base", "block": null, "base_tables": ["login_records_table"]}, {"alias": "u", "kind": "base", "block": null, "base_tables": ["user_information_table"]}] | [{"type": "INNER", "right": "login_records_table AS l", "on": "se.\"Login Record ID\" = l.\"Login Record ID\"", "using": []}, {"type": "INNER", "right": "user_information_table AS u", "on": "l.\"User ID\" = u.\"User ID\"", "using": []}] | ["u.Department"] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |
| B1 | SUM(CASE WHEN se."Severity" IN ('High', 'Severe') THEN 1 ELSE 0 END) | [] | [{"table": "security_events_table", "column": "Severity"}] | False |


## S78

类别 `data`；来源 `python`；调用 `c919f2ecbc3344469fed1f0a30dd1d0c`；状态 `success`。

```sql

SELECT u.Department AS dept,
  SUM(CASE WHEN a."Confirmation Status" = 'Confirmed' THEN 1 ELSE 0 END) AS confirmed_cnt,
  COUNT(*) AS total_anomalies
FROM abnormal_logins_table a
JOIN login_records_table l ON a."Login Record ID" = l."Login Record ID"
JOIN user_information_table u ON l."User ID" = u."User ID"
GROUP BY u.Department

```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-035/attempt-01/sql/S78.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-035/attempt-01/sql/S78.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-035/attempt-01/results/S78.rows.jsonl)；完整：True；SHA256：`9a97f2865964ef02b628b287d276839d57b5f04a5dd0c88999c7ac9917d1ad7c`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "a", "kind": "base", "block": null, "base_tables": ["abnormal_logins_table"]}, {"alias": "l", "kind": "base", "block": null, "base_tables": ["login_records_table"]}, {"alias": "u", "kind": "base", "block": null, "base_tables": ["user_information_table"]}] | [{"type": "INNER", "right": "login_records_table AS l", "on": "a.\"Login Record ID\" = l.\"Login Record ID\"", "using": []}, {"type": "INNER", "right": "user_information_table AS u", "on": "l.\"User ID\" = u.\"User ID\"", "using": []}] | ["u.Department"] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | SUM(CASE WHEN a."Confirmation Status" = 'Confirmed' THEN 1 ELSE 0 END) | [] | [{"table": "abnormal_logins_table", "column": "Confirmation Status"}] | False |
| B1 | COUNT(*) | [] | [] | True |


## S79

类别 `data`；来源 `query_db`；调用 `54619d93ce814199bb7d153b30411639`；状态 `success`。

```sql
SELECT 
  u.Department,
  CASE WHEN ua.anomaly_count >= 3 THEN '3+' 
       WHEN ua.anomaly_count = 2 THEN '2' 
       ELSE '1' END AS anomaly_bucket,
  COUNT(DISTINCT u."User ID") AS user_count,
  SUM(ua.anomaly_count) AS anomalies
FROM (
  SELECT l."User ID", COUNT(*) AS anomaly_count
  FROM abnormal_logins_table a
  JOIN login_records_table l ON a."Login Record ID" = l."Login Record ID"
  GROUP BY l."User ID"
) ua
JOIN user_information_table u ON ua."User ID" = u."User ID"
GROUP BY u.Department, anomaly_bucket
ORDER BY u.Department, anomaly_bucket
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-035/attempt-01/sql/S79.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-035/attempt-01/sql/S79.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-035/attempt-01/results/S79.rows.jsonl)；完整：True；SHA256：`41d8c30151dbfaba64b22dec4a89b1051cd2e0365a634bdd2456f0049812a83b`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "a", "kind": "base", "block": null, "base_tables": ["abnormal_logins_table"]}, {"alias": "l", "kind": "base", "block": null, "base_tables": ["login_records_table"]}] | [{"type": "INNER", "right": "login_records_table AS l", "on": "a.\"Login Record ID\" = l.\"Login Record ID\"", "using": []}] | ["l.\"User ID\""] |
| B2 | [{"alias": "ua", "kind": "derived", "block": "B1", "base_tables": ["abnormal_logins_table", "login_records_table"]}, {"alias": "u", "kind": "base", "block": null, "base_tables": ["user_information_table"]}] | [{"type": "INNER", "right": "user_information_table AS u", "on": "ua.\"User ID\" = u.\"User ID\"", "using": []}] | ["u.Department", "CASE WHEN ua.anomaly_count >= 3 THEN '3+' WHEN ua.anomaly_count = 2 THEN '2' ELSE '1' END"] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |
| B2 | COUNT(DISTINCT u."User ID") | [{"table": "user_information_table", "column": "User ID"}] | [] | False |
| B2 | SUM(ua.anomaly_count) | [] | [] | False |


## S80

类别 `data`；来源 `query_db`；调用 `2a96d92eced74822adcbd2d113290c09`；状态 `success`。

```sql
SELECT 
  u.Department,
  strftime('%H', a."Detection Time") AS hour,
  COUNT(*) AS cnt
FROM abnormal_logins_table a
JOIN login_records_table l ON a."Login Record ID" = l."Login Record ID"
JOIN user_information_table u ON l."User ID" = u."User ID"
WHERE CAST(strftime('%H', a."Detection Time") AS INTEGER) BETWEEN 0 AND 6
GROUP BY u.Department
ORDER BY u.Department
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-035/attempt-01/sql/S80.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-035/attempt-01/sql/S80.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-035/attempt-01/results/S80.rows.jsonl)；完整：True；SHA256：`799e556cc86e1f8e8739dd04f3f088404efe9ac11501745cd098f2939073f88f`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "a", "kind": "base", "block": null, "base_tables": ["abnormal_logins_table"]}, {"alias": "l", "kind": "base", "block": null, "base_tables": ["login_records_table"]}, {"alias": "u", "kind": "base", "block": null, "base_tables": ["user_information_table"]}] | [{"type": "INNER", "right": "login_records_table AS l", "on": "a.\"Login Record ID\" = l.\"Login Record ID\"", "using": []}, {"type": "INNER", "right": "user_information_table AS u", "on": "l.\"User ID\" = u.\"User ID\"", "using": []}] | ["u.Department"] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |


## S81

类别 `data`；来源 `query_db`；调用 `65f523db7426486c984fd6051a847b60`；状态 `success`。

```sql
SELECT 
  u.Department,
  SUM(CASE WHEN CAST(strftime('%H', a."Detection Time") AS INTEGER) BETWEEN 0 AND 6 THEN 1 ELSE 0 END) AS off_hours_anomalies,
  COUNT(*) AS total_anomalies,
  ROUND(100.0 * SUM(CASE WHEN CAST(strftime('%H', a."Detection Time") AS INTEGER) BETWEEN 0 AND 6 THEN 1 ELSE 0 END) / COUNT(*), 1) AS pct_off_hours
FROM abnormal_logins_table a
JOIN login_records_table l ON a."Login Record ID" = l."Login Record ID"
JOIN user_information_table u ON l."User ID" = u."User ID"
GROUP BY u.Department
ORDER BY pct_off_hours DESC
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-035/attempt-01/sql/S81.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-035/attempt-01/sql/S81.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-035/attempt-01/results/S81.rows.jsonl)；完整：True；SHA256：`957fc605ddd95ced028dd9970f6d44d34b5fc829cdb4c93a292758d7f85ad32e`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "a", "kind": "base", "block": null, "base_tables": ["abnormal_logins_table"]}, {"alias": "l", "kind": "base", "block": null, "base_tables": ["login_records_table"]}, {"alias": "u", "kind": "base", "block": null, "base_tables": ["user_information_table"]}] | [{"type": "INNER", "right": "login_records_table AS l", "on": "a.\"Login Record ID\" = l.\"Login Record ID\"", "using": []}, {"type": "INNER", "right": "user_information_table AS u", "on": "l.\"User ID\" = u.\"User ID\"", "using": []}] | ["u.Department"] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | SUM(CASE WHEN CAST(STRFTIME('%H', a."Detection Time") AS INTEGER) BETWEEN 0 AND 6 THEN 1 ELSE 0 END) | [] | [{"table": "abnormal_logins_table", "column": "Detection Time"}] | False |
| B1 | COUNT(*) | [] | [] | True |
| B1 | COUNT(*) | [] | [] | True |
| B1 | SUM(CASE WHEN CAST(STRFTIME('%H', a."Detection Time") AS INTEGER) BETWEEN 0 AND 6 THEN 1 ELSE 0 END) | [] | [{"table": "abnormal_logins_table", "column": "Detection Time"}] | False |


## S82

类别 `data`；来源 `query_db`；调用 `2e7591a0204e473ea2613218caba1333`；状态 `success`。

```sql
SELECT 
  u.Department,
  COUNT(DISTINCT a."Anomaly ID") AS anomaly_count,
  COUNT(DISTINCT l."User ID") AS distinct_users,
  ROUND(1.0 * COUNT(DISTINCT a."Anomaly ID") / NULLIF(COUNT(DISTINCT l."User ID"), 0), 2) AS anomalies_per_affected_user
FROM abnormal_logins_table a
JOIN login_records_table l ON a."Login Record ID" = l."Login Record ID"
JOIN user_information_table u ON l."User ID" = u."User ID"
GROUP BY u.Department
ORDER BY anomalies_per_affected_user DESC
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-035/attempt-01/sql/S82.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-035/attempt-01/sql/S82.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-035/attempt-01/results/S82.rows.jsonl)；完整：True；SHA256：`f7551fc8214178b4f04991733a2ebd179deed9ecfc2797f833d8112bcd26a5c3`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "a", "kind": "base", "block": null, "base_tables": ["abnormal_logins_table"]}, {"alias": "l", "kind": "base", "block": null, "base_tables": ["login_records_table"]}, {"alias": "u", "kind": "base", "block": null, "base_tables": ["user_information_table"]}] | [{"type": "INNER", "right": "login_records_table AS l", "on": "a.\"Login Record ID\" = l.\"Login Record ID\"", "using": []}, {"type": "INNER", "right": "user_information_table AS u", "on": "l.\"User ID\" = u.\"User ID\"", "using": []}] | ["u.Department"] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(DISTINCT a."Anomaly ID") | [{"table": "abnormal_logins_table", "column": "Anomaly ID"}] | [] | False |
| B1 | COUNT(DISTINCT l."User ID") | [{"table": "login_records_table", "column": "User ID"}] | [] | False |
| B1 | COUNT(DISTINCT a."Anomaly ID") | [{"table": "abnormal_logins_table", "column": "Anomaly ID"}] | [] | False |
| B1 | COUNT(DISTINCT l."User ID") | [{"table": "login_records_table", "column": "User ID"}] | [] | False |

