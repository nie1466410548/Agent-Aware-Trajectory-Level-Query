# dacomp-046

Analyze the marketing characteristics of user groups across different age segments (churn …

运行：已提交。官方未评分。全部 SQL 尝试/成功 68/67；数据 SQL 66/65；Python 9 次。

完整原题：

Analyze the marketing characteristics of user groups across different age segments (churn risk, share rate, feedback rating), and design differentiated product and marketing campaign recommendation strategies.

| 表 | 行数 | 列数 |
| --- | --- | --- |
| marketing_campaign_interaction | 337 | 13 |
| network_environment_information | 561 | 13 |
| shopping_cart_operations_table | 269 | 10 |
| user_basic_information_table_1 | 337 | 16 |
| user_geolocation_information_ta | 337 | 11 |
| user_tags_table | 337 | 20 |


实际路线（分析者依据 SQL/源码概括，不代表 Agent 自述）：SQL 比较年龄组的流失、分享、反馈及产品偏好 → Python 图表整理与占比转换 → 分年龄营销建议。

数据库大小：618,496 字节。

## 数据 SQL

| SQL | 状态 | 基础表 | Join 输入/类型 | GROUP BY | 聚合表达式 | 结果行数 | 数据库 ms |
| --- | --- | --- | --- | --- | --- | --- | --- |
| [S3/Q1](#s3) | success | ["user_basic_information_table_1"] | 0 / {} | [] | [] | 4 | 0.437 |
| [S4/Q2](#s4) | success | ["user_basic_information_table_1"] | 0 / {} | [] | ["COUNT(*)"] | 1 | 0.355 |
| [S5/Q3](#s5) | success | ["user_tags_table"] | 0 / {} | [] | [] | 2 | 0.474 |
| [S6/Q4](#s6) | success | ["marketing_campaign_interaction"] | 0 / {} | [] | ["COUNT(*)"] | 1 | 0.363 |
| [S7/Q5](#s7) | success | ["user_basic_information_table_1"] | 0 / {} | ["\"Age group\""] | ["COUNT(*)"] | 4 | 0.432 |
| [S8/Q6](#s8) | success | ["user_basic_information_table_1"] | 0 / {} | [] | [] | 2 | 0.424 |
| [S9/Q7](#s9) | success | ["user_basic_information_table_1"] | 0 / {} | [] | [] | 4 | 0.275 |
| [S10/Q8](#s10) | success | ["user_basic_information_table_1"] | 0 / {} | [] | [] | 4 | 0.297 |
| [S11/Q9](#s11) | success | ["marketing_campaign_interaction", "user_basic_information_table_1", "user_tags_table"] | 3 / {'LEFT': 2} | ["u.\"Age group\""] | ["COUNT(DISTINCT u.\"User ID\")", "SUM(CASE WHEN t.\"Is At-Risk User\" = 'Yes' THEN 1 ELSE 0 END)", "AVG(m.\"Number of Shares\")", "AVG(m.\"Event Feedback Rating\")", "AVG(m.\"Event Conversion Rate\")", "AVG(m.\"Event Dwell Time\")", "COUNT(DISTINCT u.\"User ID\")", "SUM(CASE WHEN t.\"Is At-Risk User\" = 'Yes' THEN 1 ELSE 0 END)"] | 4 | 1.751 |
| [S12/Q10](#s12) | success | ["marketing_campaign_interaction", "user_basic_information_table_1"] | 2 / {'LEFT': 1} | ["u.\"Age group\""] | ["COUNT(m.\"User ID\")", "AVG(m.\"Number of Participants\")", "AVG(m.\"Number of Shares\")", "SUM(m.\"Number of Shares\")", "SUM(m.\"Number of Participants\")"] | 4 | 0.994 |
| [S13/Q11](#s13) | success | ["user_tags_table"] | 0 / {} | [] | [] | 3 | 0.324 |
| [S14/Q12](#s14) | success | ["user_tags_table"] | 0 / {} | [] | [] | 3 | 0.322 |
| [S15/Q13](#s15) | success | ["user_tags_table"] | 0 / {} | [] | [] | 5 | 0.293 |
| [S16/Q14](#s16) | success | ["user_tags_table"] | 0 / {} | [] | [] | 5 | 0.3 |
| [S17/Q15](#s17) | success | ["user_basic_information_table_1", "user_tags_table"] | 2 / {'INNER': 1} | ["u.\"Age group\"", "t.\"Price Sensitivity\""] | ["COUNT(*)"] | 12 | 1.03 |
| [S18/Q16](#s18) | success | ["user_basic_information_table_1", "user_tags_table"] | 2 / {'INNER': 1} | ["u.\"Age group\"", "t.\"Spending Power\""] | ["COUNT(*)"] | 12 | 1.071 |
| [S19/Q17](#s19) | success | ["user_basic_information_table_1", "user_tags_table"] | 2 / {'INNER': 1} | ["u.\"Age group\"", "t.\"Browsing Preference Tag\""] | ["COUNT(*)"] | 16 | 0.995 |
| [S20/Q18](#s20) | success | ["user_basic_information_table_1", "user_tags_table"] | 2 / {'INNER': 1} | ["u.\"Age group\"", "t.\"Purchase Preference Tag\""] | ["COUNT(*)"] | 16 | 1.128 |
| [S21/Q19](#s21) | success | ["user_basic_information_table_1", "user_tags_table"] | 2 / {'INNER': 1} | ["u.\"Age group\"", "t.\"Category Preference\""] | ["COUNT(*)"] | 12 | 1.44 |
| [S22/Q20](#s22) | success | ["user_tags_table"] | 0 / {} | [] | [] | 4 | 0.671 |
| [S23/Q21](#s23) | success | ["user_basic_information_table_1", "user_tags_table"] | 2 / {'INNER': 1} | ["\"Browsing Preference Tag\""] | ["COUNT(*)"] | 5 | 0.778 |
| [S24/Q22](#s24) | success | ["marketing_campaign_interaction"] | 0 / {} | [] | [] | 10 | 0.443 |
| [S25/Q23](#s25) | success | ["marketing_campaign_interaction"] | 0 / {} | ["\"Participation Progress\""] | ["COUNT(*)"] | 100 | 0.579 |
| [S26/Q24](#s26) | success | ["marketing_campaign_interaction"] | 0 / {} | ["\"Usage Status\""] | ["COUNT(*)"] | 2 | 0.458 |
| [S27/Q25](#s27) | success | ["marketing_campaign_interaction", "user_basic_information_table_1"] | 2 / {'INNER': 1} | ["u.\"Age group\""] | ["COUNT(*)", "AVG(m.\"Event Feedback Rating\")", "COUNT(*)", "COUNT(*)", "SUM(CASE WHEN m.\"Is Event Blocked\" = 'Yes' THEN 1 ELSE 0 END)", "SUM(CASE WHEN m.\"Usage Status\" = 'Used' THEN 1 ELSE 0 END)"] | 4 | 1.255 |
| [S28/Q26](#s28) | success | ["marketing_campaign_interaction"] | 0 / {} | ["\"Is Event Blocked\""] | ["COUNT(*)"] | 2 | 0.355 |
| [S29/Q27](#s29) | success | ["user_tags_table"] | 0 / {} | [] | [] | 3 | 0.387 |
| [S30/Q28](#s30) | success | ["user_tags_table"] | 0 / {} | [] | [] | 2 | 0.368 |
| [S31/Q29](#s31) | success | ["marketing_campaign_interaction", "user_basic_information_table_1"] | 2 / {'INNER': 1} | ["u.\"Age group\"", "m.\"Event Name\""] | ["COUNT(*)", "AVG(m.\"Event Feedback Rating\")", "AVG(m.\"Number of Shares\")", "AVG(m.\"Event Conversion Rate\")"] | 40 | 1.507 |
| [S32/Q30](#s32) | success | ["user_basic_information_table_1"] | 0 / {} | ["u.\"Age group\""] | ["AVG(u.\"Login Count\")", "AVG(u.\"Device count\")", "COUNT(*)", "SUM(CASE WHEN u.\"Marketing SMS subscription status\" = 'Subscribed' THEN 1 ELSE 0 END)"] | 4 | 0.635 |
| [S33/Q31](#s33) | success | ["user_basic_information_table_1"] | 0 / {} | [] | [] | 2 | 0.443 |
| [S34/Q32](#s34) | success | ["user_basic_information_table_1"] | 0 / {} | ["\"Occupation\""] | ["COUNT(*)"] | 20 | 0.53 |
| [S35/Q33](#s35) | success | ["user_basic_information_table_1"] | 0 / {} | ["\"Education Level\""] | ["COUNT(*)"] | 4 | 0.49 |
| [S36/Q34](#s36) | success | ["user_basic_information_table_1", "user_tags_table"] | 2 / {'INNER': 1} | ["u.\"Age group\"", "u.\"Gender\""] | ["COUNT(*)", "SUM(CASE WHEN t.\"Is At-Risk User\" = 'Yes' THEN 1 ELSE 0 END)", "COUNT(*)", "SUM(CASE WHEN t.\"Is At-Risk User\" = 'Yes' THEN 1 ELSE 0 END)"] | 8 | 1.11 |
| [S37/Q35](#s37) | success | ["user_basic_information_table_1", "user_tags_table"] | 2 / {'INNER': 1} | ["u.\"Age group\"", "u.\"Membership Level\""] | ["COUNT(*)", "SUM(CASE WHEN t.\"Is At-Risk User\" = 'Yes' THEN 1 ELSE 0 END)", "COUNT(*)", "SUM(CASE WHEN t.\"Is At-Risk User\" = 'Yes' THEN 1 ELSE 0 END)"] | 16 | 1.088 |
| [S38/Q36](#s38) | success | ["user_basic_information_table_1", "user_tags_table"] | 2 / {'INNER': 1} | ["u.\"Age group\"", "t.\"Price Sensitivity\""] | ["COUNT(*)", "SUM(CASE WHEN t.\"Is At-Risk User\" = 'Yes' THEN 1 ELSE 0 END)", "COUNT(*)", "SUM(CASE WHEN t.\"Is At-Risk User\" = 'Yes' THEN 1 ELSE 0 END)"] | 12 | 1.164 |
| [S39/Q37](#s39) | success | ["user_basic_information_table_1", "user_tags_table"] | 2 / {'INNER': 1} | ["u.\"Age group\""] | ["SUM(CASE WHEN t.\"Is At-Risk User\" = 'Yes' AND u.\"Marketing SMS subscription status\" = 'Subscribed' THEN 1 ELSE 0 END)", "SUM(CASE WHEN t.\"Is At-Risk User\" = 'Yes' AND u.\"Marketing SMS subscription status\" = 'Not Subscribed' THEN 1 ELSE 0 END)", "COUNT(*)", "SUM(CASE WHEN u.\"Marketing SMS subscription status\" = 'Subscribed' THEN 1 ELSE 0 END)", "SUM(CASE WHEN t.\"Is At-Risk User\" = 'Yes' AND u.\"Marketing SMS subscription status\" = 'Subscribed' THEN 1 ELSE 0 END)", "SUM(CASE WHEN u.\"Marketing SMS subscription status\" = 'Subscribed' THEN 1 ELSE 0 END)", "SUM(CASE WHEN t.\"Is At-Risk User\" = 'Yes' AND u.\"Marketing SMS subscription status\" = 'Not Subscribed' THEN 1 ELSE 0 END)", "SUM(CASE WHEN u.\"Marketing SMS subscription status\" = 'Not Subscribed' THEN 1 ELSE 0 END)"] | 4 | 1.51 |
| [S40/Q38](#s40) | success | ["user_basic_information_table_1", "user_tags_table"] | 2 / {'INNER': 1} | ["u.\"Age group\"", "t.\"Is High-Value User\""] | ["COUNT(*)", "SUM(CASE WHEN t.\"Is At-Risk User\" = 'Yes' THEN 1 ELSE 0 END)", "COUNT(*)", "SUM(CASE WHEN t.\"Is At-Risk User\" = 'Yes' THEN 1 ELSE 0 END)"] | 8 | 1.093 |
| [S41/Q39](#s41) | success | ["user_tags_table"] | 0 / {} | [] | [] | 2 | 0.41 |
| [S42/Q40](#s42) | success | ["marketing_campaign_interaction", "user_basic_information_table_1", "user_tags_table"] | 3 / {'INNER': 1, 'LEFT': 1} | ["u.\"Age group\"", "t.\"Is At-Risk User\""] | ["COUNT(m.\"User ID\")", "AVG(m.\"Event Feedback Rating\")", "AVG(m.\"Number of Shares\")", "AVG(m.\"Event Conversion Rate\")", "AVG(m.\"Event Dwell Time\")"] | 8 | 1.69 |
| [S43/Q41](#s43) | success | ["marketing_campaign_interaction"] | 0 / {} | ["m.\"Event Name\""] | ["COUNT(*)", "AVG(m.\"Event Feedback Rating\")", "AVG(m.\"Number of Shares\")", "AVG(m.\"Event Conversion Rate\")", "COUNT(*)", "SUM(CASE WHEN m.\"Usage Status\" = 'Used' THEN 1 ELSE 0 END)"] | 10 | 0.719 |
| [S44/Q42](#s44) | success | ["marketing_campaign_interaction", "user_basic_information_table_1"] | 2 / {'INNER': 1} | ["u.\"Age group\"", "m.\"Event Name\""] | ["COUNT(*)", "AVG(m.\"Event Feedback Rating\")"] | 40 | 1.29 |
| [S45/Q43](#s45) | success | ["user_basic_information_table_1", "user_tags_table"] | 2 / {'INNER': 1} | ["u.\"Age group\"", "u.\"Income level\""] | ["COUNT(*)", "SUM(CASE WHEN t.\"Is At-Risk User\" = 'Yes' THEN 1 ELSE 0 END)", "COUNT(*)", "SUM(CASE WHEN t.\"Is At-Risk User\" = 'Yes' THEN 1 ELSE 0 END)"] | 16 | 1.18 |
| [S46/Q44](#s46) | success | ["user_basic_information_table_1", "user_tags_table"] | 2 / {'INNER': 1} | ["u.\"Age group\"", "t.\"Activity Tag\""] | ["COUNT(*)", "SUM(CASE WHEN t.\"Is At-Risk User\" = 'Yes' THEN 1 ELSE 0 END)"] | 12 | 1.131 |
| [S47/Q45](#s47) | success | ["user_basic_information_table_1", "user_tags_table"] | 2 / {'INNER': 1} | ["u.\"Age group\"", "t.\"Is At-Risk User\"", "t.\"Is High-Value User\"", "t.\"Is Potential Conversion User\""] | ["COUNT(*)"] | 32 | 1.211 |
| [S48/Q46](#s48) | success | ["user_tags_table"] | 0 / {} | [] | [] | 2 | 0.428 |
| [S49/Q47](#s49) | success | ["user_basic_information_table_1", "user_tags_table"] | 2 / {'INNER': 1} | ["u.\"Age group\""] | ["AVG(t.\"Tag Type Count\")", "AVG(t.\"Personalization Tag Count\")"] | 4 | 0.993 |
| [S50/Q48](#s50) | success | ["shopping_cart_operations_table", "user_basic_information_table_1"] | 2 / {'LEFT': 1} | ["u.\"Age group\""] | ["COUNT(DISTINCT c.\"Cart ID\")", "SUM(CASE WHEN c.\"Is Checked Out\" = 'Yes' THEN 1 ELSE 0 END)", "AVG(c.\"Number of Modifications\")", "AVG(c.\"Quantity Added\")", "COUNT(*)", "SUM(CASE WHEN c.\"Is Checked Out\" = 'Yes' THEN 1 ELSE 0 END)"] | 4 | 1.32 |
| [S51/Q49](#s51) | success | ["shopping_cart_operations_table"] | 0 / {} | [] | [] | 2 | 0.36 |
| [S52/Q50](#s52) | failed | ["network_environment_information", "user_basic_information_table_1"] | 2 / {'INNER': 1} | ["u.\"Age group\"", "n.\"VPN Enabled\""] | ["COUNT(*)"] | unknown | 未取得；调用总时长 0.199 ms |
| [S53/Q51](#s53) | success | ["marketing_campaign_interaction", "user_basic_information_table_1", "user_tags_table"] | 3 / {'INNER': 1, 'LEFT': 1} | ["u.\"User ID\""] | ["COUNT(m.\"User ID\")", "AVG(m.\"Number of Shares\")", "AVG(m.\"Event Feedback Rating\")", "AVG(m.\"Event Conversion Rate\")", "AVG(m.\"Event Dwell Time\")", "COUNT(m.\"User ID\")", "SUM(CASE WHEN m.\"Number of Shares\" > 0 THEN 1 ELSE 0 END)"] | 337 | 4.955 |
| [S54/Q52](#s54) | success | ["marketing_campaign_interaction", "user_basic_information_table_1"] | 2 / {'INNER': 1} | ["u.\"Age group\"", "m.\"Event Name\""] | ["COUNT(*)", "AVG(m.\"Number of Shares\")", "AVG(m.\"Event Feedback Rating\")", "AVG(m.\"Event Conversion Rate\")", "AVG(m.\"Event Dwell Time\")", "COUNT(*)", "SUM(CASE WHEN m.\"Usage Status\" = 'Used' THEN 1 ELSE 0 END)", "SUM(m.\"Number of Shares\")", "SUM(m.\"Number of Participants\")"] | 40 | 1.685 |
| [S55/Q53](#s55) | success | ["marketing_campaign_interaction", "user_basic_information_table_1"] | 2 / {'INNER': 1} | ["u.\"Age group\"", "m.\"Event Name\""] | ["COUNT(*)", "AVG(m.\"Event Feedback Rating\")", "AVG(m.\"Number of Shares\")", "AVG(m.\"Event Conversion Rate\")", "AVG(m.\"Event Dwell Time\")", "COUNT(*)", "SUM(CASE WHEN m.\"Usage Status\" = 'Used' THEN 1 ELSE 0 END)"] | 40 | 1.477 |
| [S56/Q54](#s56) | success | ["user_basic_information_table_1", "user_tags_table"] | 2 / {'INNER': 1} | ["u.\"Age group\"", "t.\"Browsing Preference Tag\""] | ["COUNT(*)"] | 16 | 1.003 |
| [S57/Q55](#s57) | success | ["user_basic_information_table_1", "user_tags_table"] | 2 / {'INNER': 1} | ["u.\"Age group\"", "t.\"Purchase Preference Tag\""] | ["COUNT(*)"] | 16 | 0.972 |
| [S58/Q56](#s58) | success | ["marketing_campaign_interaction", "user_basic_information_table_1"] | 2 / {'INNER': 1} | ["u.\"Age group\""] | ["COUNT(*)", "AVG(m.\"Number of Shares\")", "AVG(m.\"Event Feedback Rating\")", "AVG(m.\"Event Conversion Rate\")", "COUNT(*)", "COUNT(*)", "SUM(m.\"Number of Shares\")", "SUM(m.\"Number of Participants\")", "SUM(CASE WHEN m.\"Is Event Blocked\" = 'Yes' THEN 1 ELSE 0 END)", "SUM(CASE WHEN m.\"Usage Status\" = 'Used' THEN 1 ELSE 0 END)"] | 4 | 1.323 |
| [S59/Q57](#s59) | success | ["user_basic_information_table_1"] | 0 / {} | ["\"Age group\"", "\"Gender\""] | ["COUNT(*)"] | 8 | 0.521 |
| [S60/Q58](#s60) | success | ["user_basic_information_table_1"] | 0 / {} | ["\"Age group\"", "\"Income level\""] | ["COUNT(*)"] | 16 | 0.556 |
| [S61/Q59](#s61) | success | ["user_basic_information_table_1"] | 0 / {} | ["\"Age group\"", "\"Education Level\""] | ["COUNT(*)"] | 16 | 0.454 |
| [S62/Q60](#s62) | success | ["user_basic_information_table_1", "user_tags_table"] | 2 / {'INNER': 1} | ["u.\"Age group\"", "t.\"Price Sensitivity\""] | ["COUNT(*)", "SUM(CASE WHEN t.\"Is At-Risk User\" = 'Yes' THEN 1 ELSE 0 END)"] | 12 | 1.134 |
| [S63/Q61](#s63) | success | ["user_basic_information_table_1", "user_tags_table"] | 2 / {'INNER': 1} | ["u.\"Age group\"", "t.\"Spending Power\""] | ["COUNT(*)"] | 12 | 1.07 |
| [S64/Q62](#s64) | success | ["user_basic_information_table_1", "user_tags_table"] | 2 / {'INNER': 1} | ["u.\"Age group\"", "t.\"Is High-Value User\"", "t.\"Is Potential Conversion User\""] | ["COUNT(*)"] | 16 | 1.095 |
| [S65/Q63](#s65) | success | ["user_basic_information_table_1", "user_tags_table"] | 2 / {'INNER': 1} | ["u.\"Age group\"", "t.\"Is High-Value User\""] | ["COUNT(*)", "SUM(CASE WHEN t.\"Is At-Risk User\" = 'Yes' THEN 1 ELSE 0 END)", "COUNT(*)", "SUM(CASE WHEN t.\"Is At-Risk User\" = 'Yes' THEN 1 ELSE 0 END)"] | 8 | 1.031 |
| [S66/Q64](#s66) | success | ["marketing_campaign_interaction", "user_basic_information_table_1"] | 2 / {'INNER': 1} | ["u.\"Age group\"", "m.\"Event Name\""] | ["COUNT(*)", "AVG(m.\"Event Feedback Rating\")", "AVG(m.\"Number of Shares\")", "AVG(m.\"Event Conversion Rate\")", "COUNT(*)", "COUNT(*)", "SUM(CASE WHEN m.\"Usage Status\" = 'Used' THEN 1 ELSE 0 END)", "AVG(m.\"Event Feedback Rating\")"] | 12 | 1.416 |
| [S67/Q65](#s67) | success | ["marketing_campaign_interaction", "user_basic_information_table_1"] | 2 / {'INNER': 1} | [] | [] | 337 | 1.35 |
| [S68/Q66](#s68) | success | ["marketing_campaign_interaction", "user_basic_information_table_1", "user_tags_table"] | 3 / {'INNER': 2} | ["u.\"Age group\"", "t.\"Is At-Risk User\""] | ["AVG(m.\"Number of Shares\")", "AVG(m.\"Event Feedback Rating\")", "AVG(m.\"Event Conversion Rate\")", "AVG(m.\"Event Dwell Time\")"] | 8 | 1.406 |


## 元数据和设置

| SQL | 类别 | 状态 | 内容 |
| --- | --- | --- | --- |
| S1 | connection_setup | success | PRAGMA query_only=ON |
| S2 | metadata | success | SELECT name,sql FROM sqlite_master WHERE type='table' ORDER BY name |


## Python 与执行位置

人工源码审查：**reviewed_SQL_dominant_with_chart_preparation_exceptions**。主要分年龄连接、计数和均值在 SQL 内完成。Python 绘图时计算百分比、按年龄截取前 3，并对已经按相同键汇总的结果再求和；这些操作可由 SQL 完成，应作为有限的协议例外记录。后者并不是对原始明细的首次聚合。 [证据](../reviews/dacomp-046.json)。

P1：Aggregated metrics (churn risk, share/rating/conversion, demographics, campaign preferences) have been computed in SQL. Matplotlib is used here only to render these pre-aggregated results into figures for the report; no SQL-equivalent groupby is reproduced in pandas beyond what SQL already produced.

[源码](../../../runs/dsv4flash-db-first-full-01/dacomp-046/attempt-01/python/P1.py)；[输出](../../../runs/dsv4flash-db-first-full-01/dacomp-046/attempt-01/python/P1.stdout)；[错误](../../../runs/dsv4flash-db-first-full-01/dacomp-046/attempt-01/python/P1.stderr)。检出需人工核验的 SQL 可实现操作：sort_values(；不能仅凭理由判为合规。

P2：Check working directory layout to save figures with correct relative paths.

[源码](../../../runs/dsv4flash-db-first-full-01/dacomp-046/attempt-01/python/P2.py)；[输出](../../../runs/dsv4flash-db-first-full-01/dacomp-046/attempt-01/python/P2.stdout)；[错误](../../../runs/dsv4flash-db-first-full-01/dacomp-046/attempt-01/python/P2.stderr)。自动源码筛查未检出预设迁出信号；这不是全面语义合规证明。

P3：Render pre-aggregated SQL results (churn risk, avg shares, feedback rating, conversion rate, dwell time) into bar charts. The aggregation was done in SQL; this is pure visualization.

[源码](../../../runs/dsv4flash-db-first-full-01/dacomp-046/attempt-01/python/P3.py)；[输出](../../../runs/dsv4flash-db-first-full-01/dacomp-046/attempt-01/python/P3.stdout)；[错误](../../../runs/dsv4flash-db-first-full-01/dacomp-046/attempt-01/python/P3.stderr)。检出需人工核验的 SQL 可实现操作：sort_values(；不能仅凭理由判为合规。

P4：Creating visualizations for campaign heatmap (fig3), browsing preferences (fig4), churn by gender/membership (fig5), and cart checkout rates (fig6). All data was pre-aggregated in SQL queries; matplotlib is used for rendering only.

[源码](../../../runs/dsv4flash-db-first-full-01/dacomp-046/attempt-01/python/P4.py)；[输出](../../../runs/dsv4flash-db-first-full-01/dacomp-046/attempt-01/python/P4.stdout)；[错误](../../../runs/dsv4flash-db-first-full-01/dacomp-046/attempt-01/python/P4.stderr)。自动源码筛查未检出预设迁出信号；这不是全面语义合规证明。

P5：Regenerating the campaign heatmap with exact values from the database (previous run used partially hand-filled preview values). This reads the fully aggregated SQL result into pandas purely for rendering.

[源码](../../../runs/dsv4flash-db-first-full-01/dacomp-046/attempt-01/python/P5.py)；[输出](../../../runs/dsv4flash-db-first-full-01/dacomp-046/attempt-01/python/P5.stdout)；[错误](../../../runs/dsv4flash-db-first-full-01/dacomp-046/attempt-01/python/P5.stderr)。检出需人工核验的 SQL 可实现操作：groupby(, .query(, sort_values(；不能仅凭理由判为合规。

P6：Regenerate browsing-preference figure and add purchase-preference figure using exact aggregated data pulled from the database (preference distributions by age group), rendered via matplotlib.

[源码](../../../runs/dsv4flash-db-first-full-01/dacomp-046/attempt-01/python/P6.py)；[输出](../../../runs/dsv4flash-db-first-full-01/dacomp-046/attempt-01/python/P6.stdout)；[错误](../../../runs/dsv4flash-db-first-full-01/dacomp-046/attempt-01/python/P6.stderr)。检出需人工核验的 SQL 可实现操作：.query(；不能仅凭理由判为合规。

P7：Pull additional summary statistics for the report: share rate (shares/participants), blocked/used percentages, and demographic distributions by age group. These are simple SQL aggregations rendered here for inclusion in the report text.

[源码](../../../runs/dsv4flash-db-first-full-01/dacomp-046/attempt-01/python/P7.py)；[输出](../../../runs/dsv4flash-db-first-full-01/dacomp-046/attempt-01/python/P7.stdout)；[错误](../../../runs/dsv4flash-db-first-full-01/dacomp-046/attempt-01/python/P7.stderr)。检出需人工核验的 SQL 可实现操作：.query(；不能仅凭理由判为合规。

P8：Generate additional insight figures: price sensitivity & spending power by age (fig7), and query high-value/potential conversion user distributions and top-rated campaigns per age group. These are SQL aggregations rendered purely for visualization and report text.

[源码](../../../runs/dsv4flash-db-first-full-01/dacomp-046/attempt-01/python/P8.py)；[输出](../../../runs/dsv4flash-db-first-full-01/dacomp-046/attempt-01/python/P8.stdout)；[错误](../../../runs/dsv4flash-db-first-full-01/dacomp-046/attempt-01/python/P8.stderr)。检出需人工核验的 SQL 可实现操作：groupby(, .query(；不能仅凭理由判为合规。

P9：Compute correlation coefficients between feedback rating, shares, conversion, and dwell time — a statistical procedure not reasonably supported by SQLite — plus campaign-behavior comparison by at-risk status for the recommendation section.

[源码](../../../runs/dsv4flash-db-first-full-01/dacomp-046/attempt-01/python/P9.py)；[输出](../../../runs/dsv4flash-db-first-full-01/dacomp-046/attempt-01/python/P9.stdout)；[错误](../../../runs/dsv4flash-db-first-full-01/dacomp-046/attempt-01/python/P9.stderr)。检出需人工核验的 SQL 可实现操作：.query(；不能仅凭理由判为合规。

## 优化机会

已验证候选。筛选限于精确 SQL、相同自包含 CTE、相同单表完整过滤、可分解单表聚合；未覆盖任意 Join 等价和一般谓词蕴含。全部候选都是 offline，未测在线预测。

| 候选 | 类型 | 已有结果 | 覆盖 SQL | 后续次数 | 中间行数 | 验证 | 成本 |
| --- | --- | --- | --- | --- | --- | --- | --- |
| C1 | aggregate MV | False | ["S4", "S7", "S32", "S34", "S35", "S59", "S60", "S61"] | 7 | 313 | verified | Not benchmarked; correctness alone does not establish net speedup. |
| C2 | aggregate MV | False | ["S6", "S25", "S26", "S28", "S43"] | 4 | 305 | verified | Not benchmarked; correctness alone does not establish net speedup. |


已验证覆盖（含触发查询、候选并集去重）：13/65 条成功数据 SQL。正确性仅针对当前数据库快照；未测性能的候选不能声称已加速。

[完整 build/rewrite 与比较证据](dacomp-046.analysis.json)。

### C1：aggregate MV

Union of grouping keys; decomposable aggregate states; AVG uses SUM and non-NULL COUNT.

原查询 [S4](#s4), [S7](#s7), [S32](#s32), [S34](#s34), [S35](#s35), [S59](#s59), [S60](#s60), [S61](#s61) → 新增共享状态 C1 → 后续 7 次可复用。该构建点为事后假设，不代表 Agent 当时预知后续。

构建定义：

```sql
SELECT "Age group" AS __g0, "Occupation" AS __g1, "Education Level" AS __g2, "Gender" AS __g3, "Income level" AS __g4, COUNT(*) AS __a0, SUM("Login Count") AS __a1_sum, COUNT("Login Count") AS __a1_n, SUM("Device count") AS __a2_sum, COUNT("Device count") AS __a2_n, SUM(CASE WHEN "Marketing SMS subscription status" = 'Subscribed' THEN 1 ELSE 0 END) AS __a3 FROM "user_basic_information_table_1"  GROUP BY "Age group", "Occupation", "Education Level", "Gender", "Income level"
```

受益查询 S4 的改写示例：

```sql
SELECT SUM(__a0) AS total_users FROM temp.reuse_candidate
```

| 原 SQL | 列名一致 | 结果一致 | 比较方法 |
| --- | --- | --- | --- |
| S4 | True | True | exact_multiset |
| S7 | True | True | ordered_numeric_tolerance |
| S32 | True | True | ordered_numeric_tolerance |
| S34 | True | True | ordered_numeric_tolerance |
| S35 | True | True | ordered_numeric_tolerance |
| S59 | True | True | exact_multiset |
| S60 | True | True | exact_multiset |
| S61 | True | True | exact_multiset |


验证状态：verified；成本结论：Not benchmarked; correctness alone does not establish net speedup.

### C2：aggregate MV

Union of grouping keys; decomposable aggregate states; AVG uses SUM and non-NULL COUNT.

原查询 [S6](#s6), [S25](#s25), [S26](#s26), [S28](#s28), [S43](#s43) → 新增共享状态 C2 → 后续 4 次可复用。该构建点为事后假设，不代表 Agent 当时预知后续。

构建定义：

```sql
SELECT "Participation Progress" AS __g0, "Usage Status" AS __g1, "Is Event Blocked" AS __g2, "Event Name" AS __g3, COUNT(*) AS __a0, SUM("Event Feedback Rating") AS __a1_sum, COUNT("Event Feedback Rating") AS __a1_n, SUM("Number of Shares") AS __a2_sum, COUNT("Number of Shares") AS __a2_n, SUM("Event Conversion Rate") AS __a3_sum, COUNT("Event Conversion Rate") AS __a3_n, SUM(CASE WHEN "Usage Status" = 'Used' THEN 1 ELSE 0 END) AS __a4 FROM "marketing_campaign_interaction"  GROUP BY "Participation Progress", "Usage Status", "Is Event Blocked", "Event Name"
```

受益查询 S6 的改写示例：

```sql
SELECT SUM(__a0) AS total_campaigns FROM temp.reuse_candidate
```

| 原 SQL | 列名一致 | 结果一致 | 比较方法 |
| --- | --- | --- | --- |
| S6 | True | True | exact_multiset |
| S25 | True | True | exact_multiset |
| S26 | True | True | exact_multiset |
| S28 | True | True | exact_multiset |
| S43 | True | True | ordered_numeric_tolerance |


验证状态：verified；成本结论：Not benchmarked; correctness alone does not establish net speedup.

结果依赖：自动记录 SQL→Python 的接口父调用，以及源码中引用归档文件的消费者；字面值相同不认定因果。模型方向选择需要人工读取消息，尚未做全面因果标注。

[原始报告](../../../runs/dsv4flash-db-first-full-01/dacomp-046/attempt-01/answer.md)；[统一消息](../../../runs/dsv4flash-db-first-full-01/dacomp-046/attempt-01/messages.jsonl)；[原始 OpenCode 事件](../../../runs/dsv4flash-db-first-full-01/dacomp-046/attempt-01/opencode.jsonl)；[SQL 引擎日志](../../../runs/dsv4flash-db-first-full-01/dacomp-046/attempt-01/sql_journal.jsonl)。

[可读报告（本地图片链接规范化）](../answers/dacomp-046.md)。原始回答保留，分析结论未改写。

## S1

类别 `connection_setup`；来源 `connection`；调用 `e55679e897e548a1948863b78d02eefb`；状态 `success`。

```sql
PRAGMA query_only=ON
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-046/attempt-01/sql/S1.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-046/attempt-01/sql/S1.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-046/attempt-01/results/S1.rows.jsonl)；完整：True；SHA256：`e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`。

## S2

类别 `metadata`；来源 `list_db`；调用 `e55679e897e548a1948863b78d02eefb`；状态 `success`。

```sql
SELECT name,sql FROM sqlite_master WHERE type='table' ORDER BY name
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-046/attempt-01/sql/S2.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-046/attempt-01/sql/S2.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-046/attempt-01/results/S2.rows.jsonl)；完整：True；SHA256：`aad63046c77d67a252a4b124d2f0cde1cdade05de94e5b80ece157a2ea17525c`。

## S3

类别 `data`；来源 `query_db`；调用 `7e8bbd4422624bd4b9b55eeff73cb0f2`；状态 `success`。

```sql
SELECT DISTINCT "Age group" FROM user_basic_information_table_1 ORDER BY "Age group"
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-046/attempt-01/sql/S3.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-046/attempt-01/sql/S3.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-046/attempt-01/results/S3.rows.jsonl)；完整：True；SHA256：`0ef0677841547e3b6617cca9d6b192fca1b4c49c5a30af81b4b17c26eca24b8d`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "user_basic_information_table_1", "kind": "base", "block": null, "base_tables": ["user_basic_information_table_1"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |


## S4

类别 `data`；来源 `query_db`；调用 `73fff758108943c4bf2b1f8b6da2d7ad`；状态 `success`。

```sql
SELECT COUNT(*) as total_users FROM user_basic_information_table_1
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-046/attempt-01/sql/S4.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-046/attempt-01/sql/S4.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-046/attempt-01/results/S4.rows.jsonl)；完整：True；SHA256：`950cff33a152a9f532994d6a2381dbe91e2b3ef83f32e6b69422800efd0340f7`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "user_basic_information_table_1", "kind": "base", "block": null, "base_tables": ["user_basic_information_table_1"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |


## S5

类别 `data`；来源 `query_db`；调用 `4bbb9d3c563843de8a9ea7629a6f8ef7`；状态 `success`。

```sql
SELECT DISTINCT "Is At-Risk User" FROM user_tags_table
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-046/attempt-01/sql/S5.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-046/attempt-01/sql/S5.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-046/attempt-01/results/S5.rows.jsonl)；完整：True；SHA256：`515c939d13296b58a8487bb4e2e49330905690e90beb1c66b38fbb943e35d2ec`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "user_tags_table", "kind": "base", "block": null, "base_tables": ["user_tags_table"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |


## S6

类别 `data`；来源 `query_db`；调用 `b03fefcaff88453cb7053cf399e4c2e9`；状态 `success`。

```sql
SELECT COUNT(*) as total_campaigns FROM marketing_campaign_interaction
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-046/attempt-01/sql/S6.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-046/attempt-01/sql/S6.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-046/attempt-01/results/S6.rows.jsonl)；完整：True；SHA256：`950cff33a152a9f532994d6a2381dbe91e2b3ef83f32e6b69422800efd0340f7`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "marketing_campaign_interaction", "kind": "base", "block": null, "base_tables": ["marketing_campaign_interaction"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |


## S7

类别 `data`；来源 `query_db`；调用 `5764da9ffff94acf9ed1e10a342c6411`；状态 `success`。

```sql
SELECT "Age group", COUNT(*) as user_count
FROM user_basic_information_table_1
GROUP BY "Age group"
ORDER BY "Age group"
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-046/attempt-01/sql/S7.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-046/attempt-01/sql/S7.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-046/attempt-01/results/S7.rows.jsonl)；完整：True；SHA256：`f7aa7a70fd04ef4e52e1bd18c34c33a1a21e95d35cf3ba610157034ad8d844cb`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "user_basic_information_table_1", "kind": "base", "block": null, "base_tables": ["user_basic_information_table_1"]}] | [] | ["\"Age group\""] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |


## S8

类别 `data`；来源 `query_db`；调用 `2e885e0987b843e88aa34f7e7b4ad40f`；状态 `success`。

```sql
SELECT DISTINCT "Gender" FROM user_basic_information_table_1
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-046/attempt-01/sql/S8.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-046/attempt-01/sql/S8.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-046/attempt-01/results/S8.rows.jsonl)；完整：True；SHA256：`6f14579d09bb3c4bc94e45f0cbce1e619568b0ac3d575311bae3c810137dda1d`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "user_basic_information_table_1", "kind": "base", "block": null, "base_tables": ["user_basic_information_table_1"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |


## S9

类别 `data`；来源 `query_db`；调用 `68f415e3ba3344149977f692187c1a1f`；状态 `success`。

```sql
SELECT DISTINCT "Membership Level" FROM user_basic_information_table_1
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-046/attempt-01/sql/S9.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-046/attempt-01/sql/S9.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-046/attempt-01/results/S9.rows.jsonl)；完整：True；SHA256：`50099cc625caa689e6fc9b76a22f124c6f07c2c4ed145f2c17ddc494f63f9dc9`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "user_basic_information_table_1", "kind": "base", "block": null, "base_tables": ["user_basic_information_table_1"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |


## S10

类别 `data`；来源 `query_db`；调用 `d4a8e9dd97374b3595a940a553da02e8`；状态 `success`。

```sql
SELECT DISTINCT "Income level" FROM user_basic_information_table_1
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-046/attempt-01/sql/S10.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-046/attempt-01/sql/S10.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-046/attempt-01/results/S10.rows.jsonl)；完整：True；SHA256：`ebd368b55f30bd611d6d8b245a97a4200d72b199e6876723c9307fb9e46a8c3d`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "user_basic_information_table_1", "kind": "base", "block": null, "base_tables": ["user_basic_information_table_1"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |


## S11

类别 `data`；来源 `query_db`；调用 `5d2720180f3c4d1c9d4d12cdc64b0c4f`；状态 `success`。

```sql
SELECT 
  u."Age group",
  COUNT(DISTINCT u."User ID") as user_count,
  SUM(CASE WHEN t."Is At-Risk User" = 'Yes' THEN 1 ELSE 0 END) as at_risk_count,
  ROUND(100.0 * SUM(CASE WHEN t."Is At-Risk User" = 'Yes' THEN 1 ELSE 0 END) / COUNT(DISTINCT u."User ID"), 2) as churn_risk_pct,
  ROUND(AVG(m."Number of Shares"), 2) as avg_shares,
  ROUND(AVG(m."Event Feedback Rating"), 2) as avg_feedback_rating,
  ROUND(AVG(m."Event Conversion Rate"), 2) as avg_conversion_rate,
  ROUND(AVG(m."Event Dwell Time"), 2) as avg_dwell_time
FROM user_basic_information_table_1 u
LEFT JOIN user_tags_table t ON u."User ID" = t."User ID"
LEFT JOIN marketing_campaign_interaction m ON u."User ID" = m."User ID"
GROUP BY u."Age group"
ORDER BY u."Age group"
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-046/attempt-01/sql/S11.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-046/attempt-01/sql/S11.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-046/attempt-01/results/S11.rows.jsonl)；完整：True；SHA256：`ac410a5b722d180d877d368d5913a57c8a6ec1ab4454b81f1c7b79a5e65e37dc`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "u", "kind": "base", "block": null, "base_tables": ["user_basic_information_table_1"]}, {"alias": "t", "kind": "base", "block": null, "base_tables": ["user_tags_table"]}, {"alias": "m", "kind": "base", "block": null, "base_tables": ["marketing_campaign_interaction"]}] | [{"type": "LEFT", "right": "user_tags_table AS t", "on": "u.\"User ID\" = t.\"User ID\"", "using": []}, {"type": "LEFT", "right": "marketing_campaign_interaction AS m", "on": "u.\"User ID\" = m.\"User ID\"", "using": []}] | ["u.\"Age group\""] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(DISTINCT u."User ID") | [{"table": "user_basic_information_table_1", "column": "User ID"}] | [] | False |
| B1 | SUM(CASE WHEN t."Is At-Risk User" = 'Yes' THEN 1 ELSE 0 END) | [] | [{"table": "user_tags_table", "column": "Is At-Risk User"}] | False |
| B1 | AVG(m."Number of Shares") | [{"table": "marketing_campaign_interaction", "column": "Number of Shares"}] | [] | False |
| B1 | AVG(m."Event Feedback Rating") | [{"table": "marketing_campaign_interaction", "column": "Event Feedback Rating"}] | [] | False |
| B1 | AVG(m."Event Conversion Rate") | [{"table": "marketing_campaign_interaction", "column": "Event Conversion Rate"}] | [] | False |
| B1 | AVG(m."Event Dwell Time") | [{"table": "marketing_campaign_interaction", "column": "Event Dwell Time"}] | [] | False |
| B1 | COUNT(DISTINCT u."User ID") | [{"table": "user_basic_information_table_1", "column": "User ID"}] | [] | False |
| B1 | SUM(CASE WHEN t."Is At-Risk User" = 'Yes' THEN 1 ELSE 0 END) | [] | [{"table": "user_tags_table", "column": "Is At-Risk User"}] | False |


## S12

类别 `data`；来源 `query_db`；调用 `ed9287549f99467e9b8efec1f3502984`；状态 `success`。

```sql
SELECT 
  u."Age group",
  ROUND(100.0 * SUM(m."Number of Shares") / NULLIF(SUM(m."Number of Participants"), 0), 2) as share_rate_pct,
  ROUND(AVG(m."Number of Participants"), 2) as avg_participants,
  ROUND(AVG(m."Number of Shares"), 2) as avg_shares,
  COUNT(m."User ID") as campaign_interactions
FROM user_basic_information_table_1 u
LEFT JOIN marketing_campaign_interaction m ON u."User ID" = m."User ID"
GROUP BY u."Age group"
ORDER BY u."Age group"
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-046/attempt-01/sql/S12.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-046/attempt-01/sql/S12.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-046/attempt-01/results/S12.rows.jsonl)；完整：True；SHA256：`ca6f248a01e08b0e9f5c53c150efcfc5a523f11135da6fb8585d904fe5fc8275`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "u", "kind": "base", "block": null, "base_tables": ["user_basic_information_table_1"]}, {"alias": "m", "kind": "base", "block": null, "base_tables": ["marketing_campaign_interaction"]}] | [{"type": "LEFT", "right": "marketing_campaign_interaction AS m", "on": "u.\"User ID\" = m.\"User ID\"", "using": []}] | ["u.\"Age group\""] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(m."User ID") | [{"table": "marketing_campaign_interaction", "column": "User ID"}] | [] | False |
| B1 | AVG(m."Number of Participants") | [{"table": "marketing_campaign_interaction", "column": "Number of Participants"}] | [] | False |
| B1 | AVG(m."Number of Shares") | [{"table": "marketing_campaign_interaction", "column": "Number of Shares"}] | [] | False |
| B1 | SUM(m."Number of Shares") | [{"table": "marketing_campaign_interaction", "column": "Number of Shares"}] | [] | False |
| B1 | SUM(m."Number of Participants") | [{"table": "marketing_campaign_interaction", "column": "Number of Participants"}] | [] | False |


## S13

类别 `data`；来源 `query_db`；调用 `c3e0f1445cd545b5bcccd6c89467ade0`；状态 `success`。

```sql
SELECT DISTINCT "Price Sensitivity" FROM user_tags_table
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-046/attempt-01/sql/S13.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-046/attempt-01/sql/S13.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-046/attempt-01/results/S13.rows.jsonl)；完整：True；SHA256：`6920439bdd032fd951cf5916834e120c2493edd979281f0b7587f18a49949857`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "user_tags_table", "kind": "base", "block": null, "base_tables": ["user_tags_table"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |


## S14

类别 `data`；来源 `query_db`；调用 `9ec89e309bdb458bab47c5e93112bdcb`；状态 `success`。

```sql
SELECT DISTINCT "Spending Power" FROM user_tags_table
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-046/attempt-01/sql/S14.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-046/attempt-01/sql/S14.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-046/attempt-01/results/S14.rows.jsonl)；完整：True；SHA256：`19441d1d827bb9617a9b51e84e8341de1812dc5c19f1995771ca55e323655cbe`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "user_tags_table", "kind": "base", "block": null, "base_tables": ["user_tags_table"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |


## S15

类别 `data`；来源 `query_db`；调用 `ec4fcf35afc744078a609a038287a29d`；状态 `success`。

```sql
SELECT DISTINCT "Browsing Preference Tag" FROM user_tags_table
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-046/attempt-01/sql/S15.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-046/attempt-01/sql/S15.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-046/attempt-01/results/S15.rows.jsonl)；完整：True；SHA256：`66ce8a946569ac54bd201e81d9f8331f4cd4ad65f6590959e39307a2a22b9959`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "user_tags_table", "kind": "base", "block": null, "base_tables": ["user_tags_table"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |


## S16

类别 `data`；来源 `query_db`；调用 `6c1656ea7dbc4f12992268b7bb2b00be`；状态 `success`。

```sql
SELECT DISTINCT "Purchase Preference Tag" FROM user_tags_table
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-046/attempt-01/sql/S16.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-046/attempt-01/sql/S16.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-046/attempt-01/results/S16.rows.jsonl)；完整：True；SHA256：`d9ba7d048e93c27d68d6d0c74b05ed7da2a0d54cd4369f38b213827549f25bcb`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "user_tags_table", "kind": "base", "block": null, "base_tables": ["user_tags_table"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |


## S17

类别 `data`；来源 `query_db`；调用 `5b6def2467994976ba9a907598005adf`；状态 `success`。

```sql
SELECT 
  u."Age group",
  t."Price Sensitivity",
  COUNT(*) as count
FROM user_basic_information_table_1 u
JOIN user_tags_table t ON u."User ID" = t."User ID"
GROUP BY u."Age group", t."Price Sensitivity"
ORDER BY u."Age group", t."Price Sensitivity"
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-046/attempt-01/sql/S17.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-046/attempt-01/sql/S17.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-046/attempt-01/results/S17.rows.jsonl)；完整：True；SHA256：`433a58ea0f68121c9ebe4a2514a0d3e8344ede90abc95b06f3f4e2ff6b699f46`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "u", "kind": "base", "block": null, "base_tables": ["user_basic_information_table_1"]}, {"alias": "t", "kind": "base", "block": null, "base_tables": ["user_tags_table"]}] | [{"type": "INNER", "right": "user_tags_table AS t", "on": "u.\"User ID\" = t.\"User ID\"", "using": []}] | ["u.\"Age group\"", "t.\"Price Sensitivity\""] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |


## S18

类别 `data`；来源 `query_db`；调用 `e3620f2ec02c43819cc715bc54695714`；状态 `success`。

```sql
SELECT 
  u."Age group",
  t."Spending Power",
  COUNT(*) as count
FROM user_basic_information_table_1 u
JOIN user_tags_table t ON u."User ID" = t."User ID"
GROUP BY u."Age group", t."Spending Power"
ORDER BY u."Age group", t."Spending Power"
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-046/attempt-01/sql/S18.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-046/attempt-01/sql/S18.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-046/attempt-01/results/S18.rows.jsonl)；完整：True；SHA256：`14b48a970c3767995b691765f887d0381e21c3f8f32e33a69fc47811125c10e5`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "u", "kind": "base", "block": null, "base_tables": ["user_basic_information_table_1"]}, {"alias": "t", "kind": "base", "block": null, "base_tables": ["user_tags_table"]}] | [{"type": "INNER", "right": "user_tags_table AS t", "on": "u.\"User ID\" = t.\"User ID\"", "using": []}] | ["u.\"Age group\"", "t.\"Spending Power\""] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |


## S19

类别 `data`；来源 `query_db`；调用 `ee081aad3345449db1817b667aa324c6`；状态 `success`。

```sql
SELECT 
  u."Age group",
  t."Browsing Preference Tag",
  COUNT(*) as count
FROM user_basic_information_table_1 u
JOIN user_tags_table t ON u."User ID" = t."User ID"
WHERE t."Browsing Preference Tag" != 'None'
GROUP BY u."Age group", t."Browsing Preference Tag"
ORDER BY u."Age group", count DESC
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-046/attempt-01/sql/S19.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-046/attempt-01/sql/S19.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-046/attempt-01/results/S19.rows.jsonl)；完整：True；SHA256：`a2461304729e70a77e668f503675b238b6db0bc2366af2356cb3af4db3ff36b3`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "u", "kind": "base", "block": null, "base_tables": ["user_basic_information_table_1"]}, {"alias": "t", "kind": "base", "block": null, "base_tables": ["user_tags_table"]}] | [{"type": "INNER", "right": "user_tags_table AS t", "on": "u.\"User ID\" = t.\"User ID\"", "using": []}] | ["u.\"Age group\"", "t.\"Browsing Preference Tag\""] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |


## S20

类别 `data`；来源 `query_db`；调用 `49f56a4866b24a27998ce1423daba686`；状态 `success`。

```sql
SELECT 
  u."Age group",
  t."Purchase Preference Tag",
  COUNT(*) as count
FROM user_basic_information_table_1 u
JOIN user_tags_table t ON u."User ID" = t."User ID"
WHERE t."Purchase Preference Tag" != 'None'
GROUP BY u."Age group", t."Purchase Preference Tag"
ORDER BY u."Age group", count DESC
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-046/attempt-01/sql/S20.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-046/attempt-01/sql/S20.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-046/attempt-01/results/S20.rows.jsonl)；完整：True；SHA256：`fe4e8deb112e8b3dfb92725efb834736150e39ee27432579a16905e096360dfd`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "u", "kind": "base", "block": null, "base_tables": ["user_basic_information_table_1"]}, {"alias": "t", "kind": "base", "block": null, "base_tables": ["user_tags_table"]}] | [{"type": "INNER", "right": "user_tags_table AS t", "on": "u.\"User ID\" = t.\"User ID\"", "using": []}] | ["u.\"Age group\"", "t.\"Purchase Preference Tag\""] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |


## S21

类别 `data`；来源 `query_db`；调用 `ebebaf90fcbf4661bfd8dfb8debcf5ef`；状态 `success`。

```sql
SELECT 
  u."Age group",
  t."Category Preference",
  COUNT(*) as count
FROM user_basic_information_table_1 u
JOIN user_tags_table t ON u."User ID" = t."User ID"
WHERE t."Category Preference" IS NOT NULL AND t."Category Preference" != 'None'
GROUP BY u."Age group", t."Category Preference"
ORDER BY u."Age group", count DESC
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-046/attempt-01/sql/S21.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-046/attempt-01/sql/S21.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-046/attempt-01/results/S21.rows.jsonl)；完整：True；SHA256：`39c9fec345f5ebe5ca18fe54372ad06f405cfafa04788f64ef8ee3dbf3570654`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "u", "kind": "base", "block": null, "base_tables": ["user_basic_information_table_1"]}, {"alias": "t", "kind": "base", "block": null, "base_tables": ["user_tags_table"]}] | [{"type": "INNER", "right": "user_tags_table AS t", "on": "u.\"User ID\" = t.\"User ID\"", "using": []}] | ["u.\"Age group\"", "t.\"Category Preference\""] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |


## S22

类别 `data`；来源 `query_db`；调用 `11357e963bc34058afd7c7411fef45cc`；状态 `success`。

```sql
SELECT DISTINCT "Category Preference" FROM user_tags_table
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-046/attempt-01/sql/S22.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-046/attempt-01/sql/S22.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-046/attempt-01/results/S22.rows.jsonl)；完整：True；SHA256：`10eedcab487093dd9bf9ad45a6d8c568d39c0d5c6229bc055290e27830995603`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "user_tags_table", "kind": "base", "block": null, "base_tables": ["user_tags_table"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |


## S23

类别 `data`；来源 `query_db`；调用 `63549f56a5c04aee96032657e322e7c2`；状态 `success`。

```sql
SELECT "Browsing Preference Tag", COUNT(*) as cnt
FROM user_tags_table t JOIN user_basic_information_table_1 u ON t."User ID"=u."User ID"
WHERE u."Age group"='<25'
GROUP BY "Browsing Preference Tag"
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-046/attempt-01/sql/S23.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-046/attempt-01/sql/S23.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-046/attempt-01/results/S23.rows.jsonl)；完整：True；SHA256：`b908375e8b76afbde1fdaba36eea32d2ff3221dad31c50939c9f2fa2ff2944f6`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "t", "kind": "base", "block": null, "base_tables": ["user_tags_table"]}, {"alias": "u", "kind": "base", "block": null, "base_tables": ["user_basic_information_table_1"]}] | [{"type": "INNER", "right": "user_basic_information_table_1 AS u", "on": "t.\"User ID\" = u.\"User ID\"", "using": []}] | ["\"Browsing Preference Tag\""] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |


## S24

类别 `data`；来源 `query_db`；调用 `c87ffdc796cb40cd9a7447bbc0110684`；状态 `success`。

```sql
SELECT DISTINCT "Event Name" FROM marketing_campaign_interaction LIMIT 20
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-046/attempt-01/sql/S24.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-046/attempt-01/sql/S24.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-046/attempt-01/results/S24.rows.jsonl)；完整：True；SHA256：`b98df68cfa4e5333de77acaa164865e2b7b7c4ad727e4ffd9587e709da1bf514`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "marketing_campaign_interaction", "kind": "base", "block": null, "base_tables": ["marketing_campaign_interaction"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |


## S25

类别 `data`；来源 `query_db`；调用 `ef33db7f7b1d4651bcfe0947d74e544c`；状态 `success`。

```sql
SELECT "Participation Progress", COUNT(*) as cnt FROM marketing_campaign_interaction GROUP BY "Participation Progress"
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-046/attempt-01/sql/S25.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-046/attempt-01/sql/S25.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-046/attempt-01/results/S25.rows.jsonl)；完整：True；SHA256：`35f29864b49da594549745ec50b8b14e7f17ac24ce8494d9d43407de988ade9e`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "marketing_campaign_interaction", "kind": "base", "block": null, "base_tables": ["marketing_campaign_interaction"]}] | [] | ["\"Participation Progress\""] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |


## S26

类别 `data`；来源 `query_db`；调用 `da17b311c86d4ff79cceea9336ea15be`；状态 `success`。

```sql
SELECT "Usage Status", COUNT(*) as cnt FROM marketing_campaign_interaction GROUP BY "Usage Status"
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-046/attempt-01/sql/S26.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-046/attempt-01/sql/S26.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-046/attempt-01/results/S26.rows.jsonl)；完整：True；SHA256：`70f773ebbcc80d6c79a46540b948ad13735e363f8a0ca080bb5f0ba71b390ec6`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "marketing_campaign_interaction", "kind": "base", "block": null, "base_tables": ["marketing_campaign_interaction"]}] | [] | ["\"Usage Status\""] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |


## S27

类别 `data`；来源 `query_db`；调用 `356f917005fe4c4e9b545185c9d93990`；状态 `success`。

```sql
SELECT 
  u."Age group",
  ROUND(AVG(m."Event Feedback Rating"),3) as avg_rating,
  ROUND(100.0*SUM(CASE WHEN m."Is Event Blocked"='Yes' THEN 1 ELSE 0 END)/COUNT(*),2) as blocked_pct,
  ROUND(100.0*SUM(CASE WHEN m."Usage Status"='Used' THEN 1 ELSE 0 END)/COUNT(*),2) as used_pct,
  COUNT(*) as interactions
FROM user_basic_information_table_1 u
JOIN marketing_campaign_interaction m ON u."User ID"=m."User ID"
GROUP BY u."Age group"
ORDER BY u."Age group"
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-046/attempt-01/sql/S27.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-046/attempt-01/sql/S27.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-046/attempt-01/results/S27.rows.jsonl)；完整：True；SHA256：`7d275787c9b1fc09d45ab1368e1c0d438630c5574ec9dceff772b519afe03437`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "u", "kind": "base", "block": null, "base_tables": ["user_basic_information_table_1"]}, {"alias": "m", "kind": "base", "block": null, "base_tables": ["marketing_campaign_interaction"]}] | [{"type": "INNER", "right": "marketing_campaign_interaction AS m", "on": "u.\"User ID\" = m.\"User ID\"", "using": []}] | ["u.\"Age group\""] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |
| B1 | AVG(m."Event Feedback Rating") | [{"table": "marketing_campaign_interaction", "column": "Event Feedback Rating"}] | [] | False |
| B1 | COUNT(*) | [] | [] | True |
| B1 | COUNT(*) | [] | [] | True |
| B1 | SUM(CASE WHEN m."Is Event Blocked" = 'Yes' THEN 1 ELSE 0 END) | [] | [{"table": "marketing_campaign_interaction", "column": "Is Event Blocked"}] | False |
| B1 | SUM(CASE WHEN m."Usage Status" = 'Used' THEN 1 ELSE 0 END) | [] | [{"table": "marketing_campaign_interaction", "column": "Usage Status"}] | False |


## S28

类别 `data`；来源 `query_db`；调用 `a2e5995d390640739abdcf25bac2367a`；状态 `success`。

```sql
SELECT "Is Event Blocked", COUNT(*) as cnt FROM marketing_campaign_interaction GROUP BY "Is Event Blocked"
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-046/attempt-01/sql/S28.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-046/attempt-01/sql/S28.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-046/attempt-01/results/S28.rows.jsonl)；完整：True；SHA256：`f8342ec3fe3a6a3f491977ba29a53f06ea2069c470cf19dc00295ee8d94ee541`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "marketing_campaign_interaction", "kind": "base", "block": null, "base_tables": ["marketing_campaign_interaction"]}] | [] | ["\"Is Event Blocked\""] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |


## S29

类别 `data`；来源 `query_db`；调用 `c1b352b4975b490891fa60928d0463cf`；状态 `success`。

```sql
SELECT DISTINCT "Activity Tag" FROM user_tags_table
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-046/attempt-01/sql/S29.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-046/attempt-01/sql/S29.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-046/attempt-01/results/S29.rows.jsonl)；完整：True；SHA256：`2d04826d144249da89efbb93d43bb8c57685d32a1bcbd48693935f0de6519ef6`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "user_tags_table", "kind": "base", "block": null, "base_tables": ["user_tags_table"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |


## S30

类别 `data`；来源 `query_db`；调用 `1ccfe45bc8e34adbbf0f34289491ffb8`；状态 `success`。

```sql
SELECT DISTINCT "New/Returning User Tag" FROM user_tags_table
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-046/attempt-01/sql/S30.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-046/attempt-01/sql/S30.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-046/attempt-01/results/S30.rows.jsonl)；完整：True；SHA256：`5b54e796edf3561de87ea018d936a8707b0c440b3a0610cbd94b817431c6146d`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "user_tags_table", "kind": "base", "block": null, "base_tables": ["user_tags_table"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |


## S31

类别 `data`；来源 `query_db`；调用 `d2b9020239f74028a3f9f235767654af`；状态 `success`。

```sql
SELECT 
  u."Age group",
  m."Event Name",
  COUNT(*) as interactions,
  ROUND(AVG(m."Event Feedback Rating"),2) as avg_rating,
  ROUND(AVG(m."Number of Shares"),1) as avg_shares,
  ROUND(AVG(m."Event Conversion Rate"),2) as avg_conv
FROM user_basic_information_table_1 u
JOIN marketing_campaign_interaction m ON u."User ID"=m."User ID"
GROUP BY u."Age group", m."Event Name"
ORDER BY u."Age group", interactions DESC
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-046/attempt-01/sql/S31.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-046/attempt-01/sql/S31.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-046/attempt-01/results/S31.rows.jsonl)；完整：True；SHA256：`caf6b1b86497c076efc879b8f66a686b82845890cca85c54db4684a8ab8f2a79`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "u", "kind": "base", "block": null, "base_tables": ["user_basic_information_table_1"]}, {"alias": "m", "kind": "base", "block": null, "base_tables": ["marketing_campaign_interaction"]}] | [{"type": "INNER", "right": "marketing_campaign_interaction AS m", "on": "u.\"User ID\" = m.\"User ID\"", "using": []}] | ["u.\"Age group\"", "m.\"Event Name\""] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |
| B1 | AVG(m."Event Feedback Rating") | [{"table": "marketing_campaign_interaction", "column": "Event Feedback Rating"}] | [] | False |
| B1 | AVG(m."Number of Shares") | [{"table": "marketing_campaign_interaction", "column": "Number of Shares"}] | [] | False |
| B1 | AVG(m."Event Conversion Rate") | [{"table": "marketing_campaign_interaction", "column": "Event Conversion Rate"}] | [] | False |


## S32

类别 `data`；来源 `query_db`；调用 `3f657084801a4f0c948871f5a939f2f4`；状态 `success`。

```sql
SELECT 
  u."Age group",
  ROUND(AVG(u."Login Count"),1) as avg_login,
  ROUND(AVG(u."Device count"),2) as avg_devices,
  ROUND(100.0*SUM(CASE WHEN u."Marketing SMS subscription status"='Subscribed' THEN 1 ELSE 0 END)/COUNT(*),1) as sms_sub_pct
FROM user_basic_information_table_1 u
GROUP BY u."Age group"
ORDER BY u."Age group"
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-046/attempt-01/sql/S32.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-046/attempt-01/sql/S32.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-046/attempt-01/results/S32.rows.jsonl)；完整：True；SHA256：`1aff055fb4714d7641bc9be3603f93daa35cb133ed70765cf28da4ae3af6edbf`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "u", "kind": "base", "block": null, "base_tables": ["user_basic_information_table_1"]}] | [] | ["u.\"Age group\""] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | AVG(u."Login Count") | [{"table": "user_basic_information_table_1", "column": "Login Count"}] | [] | False |
| B1 | AVG(u."Device count") | [{"table": "user_basic_information_table_1", "column": "Device count"}] | [] | False |
| B1 | COUNT(*) | [] | [] | True |
| B1 | SUM(CASE WHEN u."Marketing SMS subscription status" = 'Subscribed' THEN 1 ELSE 0 END) | [] | [{"table": "user_basic_information_table_1", "column": "Marketing SMS subscription status"}] | False |


## S33

类别 `data`；来源 `query_db`；调用 `43bc24ea2c204bcbaa1aeddbdf0f3b6d`；状态 `success`。

```sql
SELECT DISTINCT "Marketing SMS subscription status" FROM user_basic_information_table_1
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-046/attempt-01/sql/S33.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-046/attempt-01/sql/S33.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-046/attempt-01/results/S33.rows.jsonl)；完整：True；SHA256：`e31f1f744c40beaddec5b9cd082a9161ff2eda80edca62dcd3f8f8799852725c`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "user_basic_information_table_1", "kind": "base", "block": null, "base_tables": ["user_basic_information_table_1"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |


## S34

类别 `data`；来源 `query_db`；调用 `abc07f10b4924dec88c0df3412778c73`；状态 `success`。

```sql
SELECT "Occupation", COUNT(*) cnt FROM user_basic_information_table_1 GROUP BY "Occupation" ORDER BY cnt DESC
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-046/attempt-01/sql/S34.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-046/attempt-01/sql/S34.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-046/attempt-01/results/S34.rows.jsonl)；完整：True；SHA256：`e870a092f90b048ab281f262346003bad4699c23745fabeb69b0fcf35d828622`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "user_basic_information_table_1", "kind": "base", "block": null, "base_tables": ["user_basic_information_table_1"]}] | [] | ["\"Occupation\""] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |


## S35

类别 `data`；来源 `query_db`；调用 `bc137c32da09490793e078959674ef5d`；状态 `success`。

```sql
SELECT "Education Level", COUNT(*) cnt FROM user_basic_information_table_1 GROUP BY "Education Level" ORDER BY cnt DESC
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-046/attempt-01/sql/S35.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-046/attempt-01/sql/S35.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-046/attempt-01/results/S35.rows.jsonl)；完整：True；SHA256：`1145e813df68e5b775536ec92ef4028ffe13aafc2d0e70e2a59e007d51b38c7a`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "user_basic_information_table_1", "kind": "base", "block": null, "base_tables": ["user_basic_information_table_1"]}] | [] | ["\"Education Level\""] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |


## S36

类别 `data`；来源 `query_db`；调用 `6f70980c35a8464e9fdafc88081c37fb`；状态 `success`。

```sql
SELECT 
  u."Age group",
  u."Gender",
  COUNT(*) as total,
  SUM(CASE WHEN t."Is At-Risk User"='Yes' THEN 1 ELSE 0 END) as at_risk,
  ROUND(100.0*SUM(CASE WHEN t."Is At-Risk User"='Yes' THEN 1 ELSE 0 END)/COUNT(*),1) as at_risk_pct
FROM user_basic_information_table_1 u
JOIN user_tags_table t ON u."User ID"=t."User ID"
GROUP BY u."Age group", u."Gender"
ORDER BY u."Age group", u."Gender"
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-046/attempt-01/sql/S36.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-046/attempt-01/sql/S36.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-046/attempt-01/results/S36.rows.jsonl)；完整：True；SHA256：`16acd18d606b253627ef3eef1ee36a7bc0af5ac3e694cce221e137b35602b6d1`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "u", "kind": "base", "block": null, "base_tables": ["user_basic_information_table_1"]}, {"alias": "t", "kind": "base", "block": null, "base_tables": ["user_tags_table"]}] | [{"type": "INNER", "right": "user_tags_table AS t", "on": "u.\"User ID\" = t.\"User ID\"", "using": []}] | ["u.\"Age group\"", "u.\"Gender\""] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |
| B1 | SUM(CASE WHEN t."Is At-Risk User" = 'Yes' THEN 1 ELSE 0 END) | [] | [{"table": "user_tags_table", "column": "Is At-Risk User"}] | False |
| B1 | COUNT(*) | [] | [] | True |
| B1 | SUM(CASE WHEN t."Is At-Risk User" = 'Yes' THEN 1 ELSE 0 END) | [] | [{"table": "user_tags_table", "column": "Is At-Risk User"}] | False |


## S37

类别 `data`；来源 `query_db`；调用 `f75f5b265f48468694bac23111137a23`；状态 `success`。

```sql
SELECT 
  u."Age group",
  u."Membership Level",
  COUNT(*) as total,
  SUM(CASE WHEN t."Is At-Risk User"='Yes' THEN 1 ELSE 0 END) as at_risk,
  ROUND(100.0*SUM(CASE WHEN t."Is At-Risk User"='Yes' THEN 1 ELSE 0 END)/COUNT(*),1) as at_risk_pct
FROM user_basic_information_table_1 u
JOIN user_tags_table t ON u."User ID"=t."User ID"
GROUP BY u."Age group", u."Membership Level"
ORDER BY u."Age group", u."Membership Level"
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-046/attempt-01/sql/S37.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-046/attempt-01/sql/S37.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-046/attempt-01/results/S37.rows.jsonl)；完整：True；SHA256：`7d6701067cad1e76449fedb96e2fee16827c3b5ceb0c49661c4dc8ff1b583592`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "u", "kind": "base", "block": null, "base_tables": ["user_basic_information_table_1"]}, {"alias": "t", "kind": "base", "block": null, "base_tables": ["user_tags_table"]}] | [{"type": "INNER", "right": "user_tags_table AS t", "on": "u.\"User ID\" = t.\"User ID\"", "using": []}] | ["u.\"Age group\"", "u.\"Membership Level\""] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |
| B1 | SUM(CASE WHEN t."Is At-Risk User" = 'Yes' THEN 1 ELSE 0 END) | [] | [{"table": "user_tags_table", "column": "Is At-Risk User"}] | False |
| B1 | COUNT(*) | [] | [] | True |
| B1 | SUM(CASE WHEN t."Is At-Risk User" = 'Yes' THEN 1 ELSE 0 END) | [] | [{"table": "user_tags_table", "column": "Is At-Risk User"}] | False |


## S38

类别 `data`；来源 `query_db`；调用 `3cd19d7ff2a3472594f7db1b72ae3e6c`；状态 `success`。

```sql
SELECT 
  u."Age group",
  t."Price Sensitivity",
  COUNT(*) as total,
  SUM(CASE WHEN t."Is At-Risk User"='Yes' THEN 1 ELSE 0 END) as at_risk,
  ROUND(100.0*SUM(CASE WHEN t."Is At-Risk User"='Yes' THEN 1 ELSE 0 END)/COUNT(*),1) as at_risk_pct
FROM user_basic_information_table_1 u
JOIN user_tags_table t ON u."User ID"=t."User ID"
GROUP BY u."Age group", t."Price Sensitivity"
ORDER BY u."Age group", t."Price Sensitivity"
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-046/attempt-01/sql/S38.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-046/attempt-01/sql/S38.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-046/attempt-01/results/S38.rows.jsonl)；完整：True；SHA256：`cadce412458dbe2e521595c660745215af43edb85cbf2c4f7ab4748d8b2e2351`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "u", "kind": "base", "block": null, "base_tables": ["user_basic_information_table_1"]}, {"alias": "t", "kind": "base", "block": null, "base_tables": ["user_tags_table"]}] | [{"type": "INNER", "right": "user_tags_table AS t", "on": "u.\"User ID\" = t.\"User ID\"", "using": []}] | ["u.\"Age group\"", "t.\"Price Sensitivity\""] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |
| B1 | SUM(CASE WHEN t."Is At-Risk User" = 'Yes' THEN 1 ELSE 0 END) | [] | [{"table": "user_tags_table", "column": "Is At-Risk User"}] | False |
| B1 | COUNT(*) | [] | [] | True |
| B1 | SUM(CASE WHEN t."Is At-Risk User" = 'Yes' THEN 1 ELSE 0 END) | [] | [{"table": "user_tags_table", "column": "Is At-Risk User"}] | False |


## S39

类别 `data`；来源 `query_db`；调用 `937e682a6fc04da8a4367f10d8437313`；状态 `success`。

```sql
SELECT 
  u."Age group",
  ROUND(100.0*SUM(CASE WHEN u."Marketing SMS subscription status"='Subscribed' THEN 1 ELSE 0 END)/COUNT(*),1) as sms_sub_pct,
  SUM(CASE WHEN t."Is At-Risk User"='Yes' AND u."Marketing SMS subscription status"='Subscribed' THEN 1 ELSE 0 END) as at_risk_subscribed,
  SUM(CASE WHEN t."Is At-Risk User"='Yes' AND u."Marketing SMS subscription status"='Not Subscribed' THEN 1 ELSE 0 END) as at_risk_not_subscribed,
  ROUND(100.0*SUM(CASE WHEN t."Is At-Risk User"='Yes' AND u."Marketing SMS subscription status"='Subscribed' THEN 1 ELSE 0 END)/NULLIF(SUM(CASE WHEN u."Marketing SMS subscription status"='Subscribed' THEN 1 ELSE 0 END),0),1) as at_risk_pct_subscribed,
  ROUND(100.0*SUM(CASE WHEN t."Is At-Risk User"='Yes' AND u."Marketing SMS subscription status"='Not Subscribed' THEN 1 ELSE 0 END)/NULLIF(SUM(CASE WHEN u."Marketing SMS subscription status"='Not Subscribed' THEN 1 ELSE 0 END),0),1) as at_risk_pct_not_subscribed
FROM user_basic_information_table_1 u
JOIN user_tags_table t ON u."User ID"=t."User ID"
GROUP BY u."Age group"
ORDER BY u."Age group"
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-046/attempt-01/sql/S39.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-046/attempt-01/sql/S39.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-046/attempt-01/results/S39.rows.jsonl)；完整：True；SHA256：`69dba6ea0e36af8da2733584a9387421ad42655a879f893941ea2fe27150bd4f`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "u", "kind": "base", "block": null, "base_tables": ["user_basic_information_table_1"]}, {"alias": "t", "kind": "base", "block": null, "base_tables": ["user_tags_table"]}] | [{"type": "INNER", "right": "user_tags_table AS t", "on": "u.\"User ID\" = t.\"User ID\"", "using": []}] | ["u.\"Age group\""] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | SUM(CASE WHEN t."Is At-Risk User" = 'Yes' AND u."Marketing SMS subscription status" = 'Subscribed' THEN 1 ELSE 0 END) | [] | [{"table": "user_tags_table", "column": "Is At-Risk User"}, {"table": "user_basic_information_table_1", "column": "Marketing SMS subscription status"}] | False |
| B1 | SUM(CASE WHEN t."Is At-Risk User" = 'Yes' AND u."Marketing SMS subscription status" = 'Not Subscribed' THEN 1 ELSE 0 END) | [] | [{"table": "user_tags_table", "column": "Is At-Risk User"}, {"table": "user_basic_information_table_1", "column": "Marketing SMS subscription status"}] | False |
| B1 | COUNT(*) | [] | [] | True |
| B1 | SUM(CASE WHEN u."Marketing SMS subscription status" = 'Subscribed' THEN 1 ELSE 0 END) | [] | [{"table": "user_basic_information_table_1", "column": "Marketing SMS subscription status"}] | False |
| B1 | SUM(CASE WHEN t."Is At-Risk User" = 'Yes' AND u."Marketing SMS subscription status" = 'Subscribed' THEN 1 ELSE 0 END) | [] | [{"table": "user_tags_table", "column": "Is At-Risk User"}, {"table": "user_basic_information_table_1", "column": "Marketing SMS subscription status"}] | False |
| B1 | SUM(CASE WHEN u."Marketing SMS subscription status" = 'Subscribed' THEN 1 ELSE 0 END) | [] | [{"table": "user_basic_information_table_1", "column": "Marketing SMS subscription status"}] | False |
| B1 | SUM(CASE WHEN t."Is At-Risk User" = 'Yes' AND u."Marketing SMS subscription status" = 'Not Subscribed' THEN 1 ELSE 0 END) | [] | [{"table": "user_tags_table", "column": "Is At-Risk User"}, {"table": "user_basic_information_table_1", "column": "Marketing SMS subscription status"}] | False |
| B1 | SUM(CASE WHEN u."Marketing SMS subscription status" = 'Not Subscribed' THEN 1 ELSE 0 END) | [] | [{"table": "user_basic_information_table_1", "column": "Marketing SMS subscription status"}] | False |


## S40

类别 `data`；来源 `query_db`；调用 `d2366fb0c3444516b13d3ba96c630f9b`；状态 `success`。

```sql
SELECT 
  u."Age group",
  t."Is High-Value User",
  COUNT(*) as cnt,
  SUM(CASE WHEN t."Is At-Risk User"='Yes' THEN 1 ELSE 0 END) as at_risk,
  ROUND(100.0*SUM(CASE WHEN t."Is At-Risk User"='Yes' THEN 1 ELSE 0 END)/COUNT(*),1) as at_risk_pct
FROM user_basic_information_table_1 u
JOIN user_tags_table t ON u."User ID"=t."User ID"
GROUP BY u."Age group", t."Is High-Value User"
ORDER BY u."Age group", t."Is High-Value User"
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-046/attempt-01/sql/S40.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-046/attempt-01/sql/S40.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-046/attempt-01/results/S40.rows.jsonl)；完整：True；SHA256：`a714172ba9f54145921e1834246a049adc2c1a35905823dcbebcffa9c95f5f69`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "u", "kind": "base", "block": null, "base_tables": ["user_basic_information_table_1"]}, {"alias": "t", "kind": "base", "block": null, "base_tables": ["user_tags_table"]}] | [{"type": "INNER", "right": "user_tags_table AS t", "on": "u.\"User ID\" = t.\"User ID\"", "using": []}] | ["u.\"Age group\"", "t.\"Is High-Value User\""] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |
| B1 | SUM(CASE WHEN t."Is At-Risk User" = 'Yes' THEN 1 ELSE 0 END) | [] | [{"table": "user_tags_table", "column": "Is At-Risk User"}] | False |
| B1 | COUNT(*) | [] | [] | True |
| B1 | SUM(CASE WHEN t."Is At-Risk User" = 'Yes' THEN 1 ELSE 0 END) | [] | [{"table": "user_tags_table", "column": "Is At-Risk User"}] | False |


## S41

类别 `data`；来源 `query_db`；调用 `8d24ee84cb2a4dcbb4c45bd0bdf25688`；状态 `success`。

```sql
SELECT DISTINCT "Is High-Value User" FROM user_tags_table
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-046/attempt-01/sql/S41.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-046/attempt-01/sql/S41.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-046/attempt-01/results/S41.rows.jsonl)；完整：True；SHA256：`515c939d13296b58a8487bb4e2e49330905690e90beb1c66b38fbb943e35d2ec`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "user_tags_table", "kind": "base", "block": null, "base_tables": ["user_tags_table"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |


## S42

类别 `data`；来源 `query_db`；调用 `acaca8b13f974df1a7179d9f1cf91143`；状态 `success`。

```sql
SELECT 
  u."Age group",
  t."Is At-Risk User",
  COUNT(m."User ID") as interactions,
  ROUND(AVG(m."Event Feedback Rating"),2) as avg_rating,
  ROUND(AVG(m."Number of Shares"),1) as avg_shares,
  ROUND(AVG(m."Event Conversion Rate"),2) as avg_conv,
  ROUND(AVG(m."Event Dwell Time"),0) as avg_dwell
FROM user_basic_information_table_1 u
JOIN user_tags_table t ON u."User ID"=t."User ID"
LEFT JOIN marketing_campaign_interaction m ON u."User ID"=m."User ID"
GROUP BY u."Age group", t."Is At-Risk User"
ORDER BY u."Age group", t."Is At-Risk User"
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-046/attempt-01/sql/S42.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-046/attempt-01/sql/S42.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-046/attempt-01/results/S42.rows.jsonl)；完整：True；SHA256：`3256097dcc0dfae6653801785c9605809dce409c2070aeb96e55e631bbdad6ba`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "u", "kind": "base", "block": null, "base_tables": ["user_basic_information_table_1"]}, {"alias": "t", "kind": "base", "block": null, "base_tables": ["user_tags_table"]}, {"alias": "m", "kind": "base", "block": null, "base_tables": ["marketing_campaign_interaction"]}] | [{"type": "INNER", "right": "user_tags_table AS t", "on": "u.\"User ID\" = t.\"User ID\"", "using": []}, {"type": "LEFT", "right": "marketing_campaign_interaction AS m", "on": "u.\"User ID\" = m.\"User ID\"", "using": []}] | ["u.\"Age group\"", "t.\"Is At-Risk User\""] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(m."User ID") | [{"table": "marketing_campaign_interaction", "column": "User ID"}] | [] | False |
| B1 | AVG(m."Event Feedback Rating") | [{"table": "marketing_campaign_interaction", "column": "Event Feedback Rating"}] | [] | False |
| B1 | AVG(m."Number of Shares") | [{"table": "marketing_campaign_interaction", "column": "Number of Shares"}] | [] | False |
| B1 | AVG(m."Event Conversion Rate") | [{"table": "marketing_campaign_interaction", "column": "Event Conversion Rate"}] | [] | False |
| B1 | AVG(m."Event Dwell Time") | [{"table": "marketing_campaign_interaction", "column": "Event Dwell Time"}] | [] | False |


## S43

类别 `data`；来源 `query_db`；调用 `2a52f4a07209484da80d0c2b689787e0`；状态 `success`。

```sql
SELECT 
  m."Event Name",
  COUNT(*) as interactions,
  ROUND(AVG(m."Event Feedback Rating"),2) as avg_rating,
  ROUND(AVG(m."Number of Shares"),1) as avg_shares,
  ROUND(AVG(m."Event Conversion Rate"),2) as avg_conv,
  ROUND(100.0*SUM(CASE WHEN m."Usage Status"='Used' THEN 1 ELSE 0 END)/COUNT(*),1) as used_pct
FROM marketing_campaign_interaction m
GROUP BY m."Event Name"
ORDER BY interactions DESC
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-046/attempt-01/sql/S43.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-046/attempt-01/sql/S43.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-046/attempt-01/results/S43.rows.jsonl)；完整：True；SHA256：`c16b189de956b7603c56a9dde37549f6e67d84ffdffac4964d5269456783208a`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "m", "kind": "base", "block": null, "base_tables": ["marketing_campaign_interaction"]}] | [] | ["m.\"Event Name\""] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |
| B1 | AVG(m."Event Feedback Rating") | [{"table": "marketing_campaign_interaction", "column": "Event Feedback Rating"}] | [] | False |
| B1 | AVG(m."Number of Shares") | [{"table": "marketing_campaign_interaction", "column": "Number of Shares"}] | [] | False |
| B1 | AVG(m."Event Conversion Rate") | [{"table": "marketing_campaign_interaction", "column": "Event Conversion Rate"}] | [] | False |
| B1 | COUNT(*) | [] | [] | True |
| B1 | SUM(CASE WHEN m."Usage Status" = 'Used' THEN 1 ELSE 0 END) | [] | [{"table": "marketing_campaign_interaction", "column": "Usage Status"}] | False |


## S44

类别 `data`；来源 `query_db`；调用 `c48a87078e7e4196b8db18033a320158`；状态 `success`。

```sql
-- Best rated campaigns for each age group
SELECT u."Age group", m."Event Name", 
  ROUND(AVG(m."Event Feedback Rating"),2) as avg_rating,
  COUNT(*) as cnt
FROM user_basic_information_table_1 u
JOIN marketing_campaign_interaction m ON u."User ID"=m."User ID"
GROUP BY u."Age group", m."Event Name"
HAVING cnt >= 3
ORDER BY u."Age group", avg_rating DESC
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-046/attempt-01/sql/S44.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-046/attempt-01/sql/S44.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-046/attempt-01/results/S44.rows.jsonl)；完整：True；SHA256：`e000a6ddfdb176b63c500a1437c3e80c0ec722ce12da8f38289947db72bc5316`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "u", "kind": "base", "block": null, "base_tables": ["user_basic_information_table_1"]}, {"alias": "m", "kind": "base", "block": null, "base_tables": ["marketing_campaign_interaction"]}] | [{"type": "INNER", "right": "marketing_campaign_interaction AS m", "on": "u.\"User ID\" = m.\"User ID\"", "using": []}] | ["u.\"Age group\"", "m.\"Event Name\""] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |
| B1 | AVG(m."Event Feedback Rating") | [{"table": "marketing_campaign_interaction", "column": "Event Feedback Rating"}] | [] | False |


## S45

类别 `data`；来源 `query_db`；调用 `64c889d4f1294e6e89e507c3c764e59b`；状态 `success`。

```sql
SELECT 
  u."Age group",
  u."Income level",
  COUNT(*) as cnt,
  SUM(CASE WHEN t."Is At-Risk User"='Yes' THEN 1 ELSE 0 END) as at_risk,
  ROUND(100.0*SUM(CASE WHEN t."Is At-Risk User"='Yes' THEN 1 ELSE 0 END)/COUNT(*),1) as at_risk_pct
FROM user_basic_information_table_1 u
JOIN user_tags_table t ON u."User ID"=t."User ID"
GROUP BY u."Age group", u."Income level"
ORDER BY u."Age group", u."Income level"
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-046/attempt-01/sql/S45.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-046/attempt-01/sql/S45.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-046/attempt-01/results/S45.rows.jsonl)；完整：True；SHA256：`d1c97f6ce9dea3e769cb3bf0f9fa6ffb16c47f4356e796bf80a81b345f45afd8`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "u", "kind": "base", "block": null, "base_tables": ["user_basic_information_table_1"]}, {"alias": "t", "kind": "base", "block": null, "base_tables": ["user_tags_table"]}] | [{"type": "INNER", "right": "user_tags_table AS t", "on": "u.\"User ID\" = t.\"User ID\"", "using": []}] | ["u.\"Age group\"", "u.\"Income level\""] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |
| B1 | SUM(CASE WHEN t."Is At-Risk User" = 'Yes' THEN 1 ELSE 0 END) | [] | [{"table": "user_tags_table", "column": "Is At-Risk User"}] | False |
| B1 | COUNT(*) | [] | [] | True |
| B1 | SUM(CASE WHEN t."Is At-Risk User" = 'Yes' THEN 1 ELSE 0 END) | [] | [{"table": "user_tags_table", "column": "Is At-Risk User"}] | False |


## S46

类别 `data`；来源 `query_db`；调用 `f0001ef407a74bb7b565a5e4445fa098`；状态 `success`。

```sql
SELECT 
  u."Age group",
  t."Activity Tag",
  COUNT(*) as cnt,
  SUM(CASE WHEN t."Is At-Risk User"='Yes' THEN 1 ELSE 0 END) as at_risk
FROM user_basic_information_table_1 u
JOIN user_tags_table t ON u."User ID"=t."User ID"
GROUP BY u."Age group", t."Activity Tag"
ORDER BY u."Age group", t."Activity Tag"
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-046/attempt-01/sql/S46.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-046/attempt-01/sql/S46.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-046/attempt-01/results/S46.rows.jsonl)；完整：True；SHA256：`659d958bb16e8c0598b7484c5c255ab00b5417d419d6ee4f008f930060403978`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "u", "kind": "base", "block": null, "base_tables": ["user_basic_information_table_1"]}, {"alias": "t", "kind": "base", "block": null, "base_tables": ["user_tags_table"]}] | [{"type": "INNER", "right": "user_tags_table AS t", "on": "u.\"User ID\" = t.\"User ID\"", "using": []}] | ["u.\"Age group\"", "t.\"Activity Tag\""] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |
| B1 | SUM(CASE WHEN t."Is At-Risk User" = 'Yes' THEN 1 ELSE 0 END) | [] | [{"table": "user_tags_table", "column": "Is At-Risk User"}] | False |


## S47

类别 `data`；来源 `query_db`；调用 `209cb4db556a4567ae0d8634a9dfe328`；状态 `success`。

```sql
SELECT 
  u."Age group",
  t."Is At-Risk User",
  t."Is High-Value User",
  t."Is Potential Conversion User",
  COUNT(*) as cnt
FROM user_basic_information_table_1 u
JOIN user_tags_table t ON u."User ID"=t."User ID"
GROUP BY u."Age group", t."Is At-Risk User", t."Is High-Value User", t."Is Potential Conversion User"
ORDER BY u."Age group", t."Is At-Risk User", t."Is High-Value User"
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-046/attempt-01/sql/S47.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-046/attempt-01/sql/S47.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-046/attempt-01/results/S47.rows.jsonl)；完整：True；SHA256：`1945d561f62ad98536553862f6c0fbf6b3573ac2008abb186dc876c868dc2690`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "u", "kind": "base", "block": null, "base_tables": ["user_basic_information_table_1"]}, {"alias": "t", "kind": "base", "block": null, "base_tables": ["user_tags_table"]}] | [{"type": "INNER", "right": "user_tags_table AS t", "on": "u.\"User ID\" = t.\"User ID\"", "using": []}] | ["u.\"Age group\"", "t.\"Is At-Risk User\"", "t.\"Is High-Value User\"", "t.\"Is Potential Conversion User\""] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |


## S48

类别 `data`；来源 `query_db`；调用 `816e1940d7ab410b89295266a0cfff84`；状态 `success`。

```sql
SELECT DISTINCT "Is Potential Conversion User" FROM user_tags_table
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-046/attempt-01/sql/S48.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-046/attempt-01/sql/S48.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-046/attempt-01/results/S48.rows.jsonl)；完整：True；SHA256：`5a19713cda3bf0943666a353b839ac204635994c6093a1b7bb22ac4ab428ba10`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "user_tags_table", "kind": "base", "block": null, "base_tables": ["user_tags_table"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |


## S49

类别 `data`；来源 `query_db`；调用 `32e6ba0d33f1459e827ac376788c36db`；状态 `success`。

```sql
SELECT 
  u."Age group",
  ROUND(AVG(t."Tag Type Count"),1) as avg_tag_types,
  ROUND(AVG(t."Personalization Tag Count"),1) as avg_personalization_tags
FROM user_basic_information_table_1 u
JOIN user_tags_table t ON u."User ID"=t."User ID"
GROUP BY u."Age group"
ORDER BY u."Age group"
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-046/attempt-01/sql/S49.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-046/attempt-01/sql/S49.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-046/attempt-01/results/S49.rows.jsonl)；完整：True；SHA256：`99fae292457bd15481425c34f83599ccde575494b717a4c8e06c2102c0855fa8`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "u", "kind": "base", "block": null, "base_tables": ["user_basic_information_table_1"]}, {"alias": "t", "kind": "base", "block": null, "base_tables": ["user_tags_table"]}] | [{"type": "INNER", "right": "user_tags_table AS t", "on": "u.\"User ID\" = t.\"User ID\"", "using": []}] | ["u.\"Age group\""] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | AVG(t."Tag Type Count") | [{"table": "user_tags_table", "column": "Tag Type Count"}] | [] | False |
| B1 | AVG(t."Personalization Tag Count") | [{"table": "user_tags_table", "column": "Personalization Tag Count"}] | [] | False |


## S50

类别 `data`；来源 `query_db`；调用 `edd1418ce5624129a5c41140f51cdc66`；状态 `success`。

```sql
SELECT 
  u."Age group",
  COUNT(DISTINCT c."Cart ID") as carts,
  SUM(CASE WHEN c."Is Checked Out"='Yes' THEN 1 ELSE 0 END) as checked_out,
  ROUND(100.0*SUM(CASE WHEN c."Is Checked Out"='Yes' THEN 1 ELSE 0 END)/COUNT(*),1) as checkout_pct,
  ROUND(AVG(c."Number of Modifications"),2) as avg_mods,
  ROUND(AVG(c."Quantity Added"),2) as avg_qty
FROM user_basic_information_table_1 u
LEFT JOIN shopping_cart_operations_table c ON u."User ID"=c."User ID"
GROUP BY u."Age group"
ORDER BY u."Age group"
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-046/attempt-01/sql/S50.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-046/attempt-01/sql/S50.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-046/attempt-01/results/S50.rows.jsonl)；完整：True；SHA256：`780b56f7d1f3312ab7dff8f5d022b92a57c4572dfb283b53df1cdbb82f2ec677`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "u", "kind": "base", "block": null, "base_tables": ["user_basic_information_table_1"]}, {"alias": "c", "kind": "base", "block": null, "base_tables": ["shopping_cart_operations_table"]}] | [{"type": "LEFT", "right": "shopping_cart_operations_table AS c", "on": "u.\"User ID\" = c.\"User ID\"", "using": []}] | ["u.\"Age group\""] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(DISTINCT c."Cart ID") | [{"table": "shopping_cart_operations_table", "column": "Cart ID"}] | [] | False |
| B1 | SUM(CASE WHEN c."Is Checked Out" = 'Yes' THEN 1 ELSE 0 END) | [] | [{"table": "shopping_cart_operations_table", "column": "Is Checked Out"}] | False |
| B1 | AVG(c."Number of Modifications") | [{"table": "shopping_cart_operations_table", "column": "Number of Modifications"}] | [] | False |
| B1 | AVG(c."Quantity Added") | [{"table": "shopping_cart_operations_table", "column": "Quantity Added"}] | [] | False |
| B1 | COUNT(*) | [] | [] | True |
| B1 | SUM(CASE WHEN c."Is Checked Out" = 'Yes' THEN 1 ELSE 0 END) | [] | [{"table": "shopping_cart_operations_table", "column": "Is Checked Out"}] | False |


## S51

类别 `data`；来源 `query_db`；调用 `078ca24c8b044f1c9acd8af9ca417589`；状态 `success`。

```sql
SELECT DISTINCT "Is Checked Out" FROM shopping_cart_operations_table
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-046/attempt-01/sql/S51.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-046/attempt-01/sql/S51.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-046/attempt-01/results/S51.rows.jsonl)；完整：True；SHA256：`5a19713cda3bf0943666a353b839ac204635994c6093a1b7bb22ac4ab428ba10`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "shopping_cart_operations_table", "kind": "base", "block": null, "base_tables": ["shopping_cart_operations_table"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |


## S52

类别 `data`；来源 `query_db`；调用 `7b400de8d67f42e696b5de3f7054a7c6`；状态 `failed`。

```sql
SELECT 
  u."Age group",
  n."VPN Enabled",
  COUNT(*) as cnt
FROM user_basic_information_table_1 u
JOIN network_environment_information n ON u."User ID"=n."User ID"
GROUP BY u."Age group", n."VPN Enabled"
ORDER BY u."Age group", n."VPN Enabled"
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-046/attempt-01/sql/S52.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-046/attempt-01/sql/S52.parameters.json)。

错误：`OperationalError('no such column: n.User ID')`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "u", "kind": "base", "block": null, "base_tables": ["user_basic_information_table_1"]}, {"alias": "n", "kind": "base", "block": null, "base_tables": ["network_environment_information"]}] | [{"type": "INNER", "right": "network_environment_information AS n", "on": "u.\"User ID\" = n.\"User ID\"", "using": []}] | ["u.\"Age group\"", "n.\"VPN Enabled\""] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |


## S53

类别 `data`；来源 `query_db`；调用 `fca32ee5099548038ffa7e4720149924`；状态 `success`。

```sql
SELECT 
  u."Age group",
  u."Gender",
  u."Membership Level",
  u."Income level",
  t."Is At-Risk User",
  t."Price Sensitivity",
  t."Spending Power",
  t."Activity Tag",
  t."Browsing Preference Tag",
  t."Purchase Preference Tag",
  t."Category Preference",
  t."Is High-Value User",
  t."Is Potential Conversion User",
  ROUND(AVG(m."Number of Shares"),2) as avg_shares,
  ROUND(AVG(m."Event Feedback Rating"),2) as avg_rating,
  ROUND(AVG(m."Event Conversion Rate"),3) as avg_conv,
  ROUND(AVG(m."Event Dwell Time"),1) as avg_dwell,
  ROUND(100.0*SUM(CASE WHEN m."Number of Shares">0 THEN 1 ELSE 0 END)/COUNT(m."User ID"),1) as share_interaction_pct,
  COUNT(m."User ID") as interactions
FROM user_basic_information_table_1 u
JOIN user_tags_table t ON u."User ID"=t."User ID"
LEFT JOIN marketing_campaign_interaction m ON u."User ID"=m."User ID"
GROUP BY u."User ID"
ORDER BY u."Age group"
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-046/attempt-01/sql/S53.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-046/attempt-01/sql/S53.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-046/attempt-01/results/S53.rows.jsonl)；完整：True；SHA256：`7b6bfc21cdbbb22f986e5c9a9d12992a6647b2a9005cc331c39ceaeb9a039a41`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "u", "kind": "base", "block": null, "base_tables": ["user_basic_information_table_1"]}, {"alias": "t", "kind": "base", "block": null, "base_tables": ["user_tags_table"]}, {"alias": "m", "kind": "base", "block": null, "base_tables": ["marketing_campaign_interaction"]}] | [{"type": "INNER", "right": "user_tags_table AS t", "on": "u.\"User ID\" = t.\"User ID\"", "using": []}, {"type": "LEFT", "right": "marketing_campaign_interaction AS m", "on": "u.\"User ID\" = m.\"User ID\"", "using": []}] | ["u.\"User ID\""] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(m."User ID") | [{"table": "marketing_campaign_interaction", "column": "User ID"}] | [] | False |
| B1 | AVG(m."Number of Shares") | [{"table": "marketing_campaign_interaction", "column": "Number of Shares"}] | [] | False |
| B1 | AVG(m."Event Feedback Rating") | [{"table": "marketing_campaign_interaction", "column": "Event Feedback Rating"}] | [] | False |
| B1 | AVG(m."Event Conversion Rate") | [{"table": "marketing_campaign_interaction", "column": "Event Conversion Rate"}] | [] | False |
| B1 | AVG(m."Event Dwell Time") | [{"table": "marketing_campaign_interaction", "column": "Event Dwell Time"}] | [] | False |
| B1 | COUNT(m."User ID") | [{"table": "marketing_campaign_interaction", "column": "User ID"}] | [] | False |
| B1 | SUM(CASE WHEN m."Number of Shares" > 0 THEN 1 ELSE 0 END) | [] | [{"table": "marketing_campaign_interaction", "column": "Number of Shares"}] | False |


## S54

类别 `data`；来源 `query_db`；调用 `8b4ce344d6754c33af0291ba0d9a9904`；状态 `success`。

```sql
-- Get the campaign-level data aggregated by age group and event name
SELECT 
  u."Age group",
  m."Event Name",
  COUNT(*) as interactions,
  ROUND(AVG(m."Number of Shares"),1) as avg_shares,
  ROUND(SUM(m."Number of Shares")*1.0/NULLIF(SUM(m."Number of Participants"),0)*100,2) as share_rate_pct,
  ROUND(AVG(m."Event Feedback Rating"),2) as avg_rating,
  ROUND(AVG(m."Event Conversion Rate"),3) as avg_conv,
  ROUND(AVG(m."Event Dwell Time"),1) as avg_dwell,
  ROUND(100.0*SUM(CASE WHEN m."Usage Status"='Used' THEN 1 ELSE 0 END)/COUNT(*),1) as used_pct
FROM user_basic_information_table_1 u
JOIN marketing_campaign_interaction m ON u."User ID"=m."User ID"
GROUP BY u."Age group", m."Event Name"
ORDER BY u."Age group", interactions DESC
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-046/attempt-01/sql/S54.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-046/attempt-01/sql/S54.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-046/attempt-01/results/S54.rows.jsonl)；完整：True；SHA256：`832a9d1ffceac8ebd45271ca2a08f2d2cf8ddcb791881aa5e12b477a2483a1b9`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "u", "kind": "base", "block": null, "base_tables": ["user_basic_information_table_1"]}, {"alias": "m", "kind": "base", "block": null, "base_tables": ["marketing_campaign_interaction"]}] | [{"type": "INNER", "right": "marketing_campaign_interaction AS m", "on": "u.\"User ID\" = m.\"User ID\"", "using": []}] | ["u.\"Age group\"", "m.\"Event Name\""] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |
| B1 | AVG(m."Number of Shares") | [{"table": "marketing_campaign_interaction", "column": "Number of Shares"}] | [] | False |
| B1 | AVG(m."Event Feedback Rating") | [{"table": "marketing_campaign_interaction", "column": "Event Feedback Rating"}] | [] | False |
| B1 | AVG(m."Event Conversion Rate") | [{"table": "marketing_campaign_interaction", "column": "Event Conversion Rate"}] | [] | False |
| B1 | AVG(m."Event Dwell Time") | [{"table": "marketing_campaign_interaction", "column": "Event Dwell Time"}] | [] | False |
| B1 | COUNT(*) | [] | [] | True |
| B1 | SUM(CASE WHEN m."Usage Status" = 'Used' THEN 1 ELSE 0 END) | [] | [{"table": "marketing_campaign_interaction", "column": "Usage Status"}] | False |
| B1 | SUM(m."Number of Shares") | [{"table": "marketing_campaign_interaction", "column": "Number of Shares"}] | [] | False |
| B1 | SUM(m."Number of Participants") | [{"table": "marketing_campaign_interaction", "column": "Number of Participants"}] | [] | False |


## S55

类别 `data`；来源 `python`；调用 `8f521617de224b48a966cfadfd01d66b`；状态 `success`。

```sql

SELECT 
  u."Age group" as age,
  m."Event Name" as evt,
  COUNT(*) as interactions,
  ROUND(AVG(m."Event Feedback Rating"),2) as avg_rating,
  ROUND(AVG(m."Number of Shares"),1) as avg_shares,
  ROUND(AVG(m."Event Conversion Rate"),3) as avg_conv,
  ROUND(AVG(m."Event Dwell Time"),1) as avg_dwell,
  ROUND(100.0*SUM(CASE WHEN m."Usage Status"='Used' THEN 1 ELSE 0 END)/COUNT(*),1) as used_pct
FROM user_basic_information_table_1 u
JOIN marketing_campaign_interaction m ON u."User ID"=m."User ID"
GROUP BY u."Age group", m."Event Name"

```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-046/attempt-01/sql/S55.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-046/attempt-01/sql/S55.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-046/attempt-01/results/S55.rows.jsonl)；完整：True；SHA256：`dbd0588407e2a4fd9626fc814c90490d49e4084804bb825c08ab760da26dc9e5`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "u", "kind": "base", "block": null, "base_tables": ["user_basic_information_table_1"]}, {"alias": "m", "kind": "base", "block": null, "base_tables": ["marketing_campaign_interaction"]}] | [{"type": "INNER", "right": "marketing_campaign_interaction AS m", "on": "u.\"User ID\" = m.\"User ID\"", "using": []}] | ["u.\"Age group\"", "m.\"Event Name\""] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |
| B1 | AVG(m."Event Feedback Rating") | [{"table": "marketing_campaign_interaction", "column": "Event Feedback Rating"}] | [] | False |
| B1 | AVG(m."Number of Shares") | [{"table": "marketing_campaign_interaction", "column": "Number of Shares"}] | [] | False |
| B1 | AVG(m."Event Conversion Rate") | [{"table": "marketing_campaign_interaction", "column": "Event Conversion Rate"}] | [] | False |
| B1 | AVG(m."Event Dwell Time") | [{"table": "marketing_campaign_interaction", "column": "Event Dwell Time"}] | [] | False |
| B1 | COUNT(*) | [] | [] | True |
| B1 | SUM(CASE WHEN m."Usage Status" = 'Used' THEN 1 ELSE 0 END) | [] | [{"table": "marketing_campaign_interaction", "column": "Usage Status"}] | False |


## S56

类别 `data`；来源 `python`；调用 `b879b8d093a648fca03f958242611b51`；状态 `success`。

```sql

SELECT u."Age group" as age, t."Browsing Preference Tag" as pref, COUNT(*) as cnt
FROM user_basic_information_table_1 u
JOIN user_tags_table t ON u."User ID"=t."User ID"
WHERE t."Browsing Preference Tag" != 'None'
GROUP BY u."Age group", t."Browsing Preference Tag"

```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-046/attempt-01/sql/S56.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-046/attempt-01/sql/S56.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-046/attempt-01/results/S56.rows.jsonl)；完整：True；SHA256：`05833e3358a2df4e1489c2dace22b5fe9dce0659770c5aa4e402c927cb66b628`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "u", "kind": "base", "block": null, "base_tables": ["user_basic_information_table_1"]}, {"alias": "t", "kind": "base", "block": null, "base_tables": ["user_tags_table"]}] | [{"type": "INNER", "right": "user_tags_table AS t", "on": "u.\"User ID\" = t.\"User ID\"", "using": []}] | ["u.\"Age group\"", "t.\"Browsing Preference Tag\""] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |


## S57

类别 `data`；来源 `python`；调用 `b879b8d093a648fca03f958242611b51`；状态 `success`。

```sql

SELECT u."Age group" as age, t."Purchase Preference Tag" as pref, COUNT(*) as cnt
FROM user_basic_information_table_1 u
JOIN user_tags_table t ON u."User ID"=t."User ID"
WHERE t."Purchase Preference Tag" != 'None'
GROUP BY u."Age group", t."Purchase Preference Tag"

```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-046/attempt-01/sql/S57.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-046/attempt-01/sql/S57.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-046/attempt-01/results/S57.rows.jsonl)；完整：True；SHA256：`b7eb60214bed6f72eb663ffda8d3563c16f289b48c9f221aa99451d928cafa53`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "u", "kind": "base", "block": null, "base_tables": ["user_basic_information_table_1"]}, {"alias": "t", "kind": "base", "block": null, "base_tables": ["user_tags_table"]}] | [{"type": "INNER", "right": "user_tags_table AS t", "on": "u.\"User ID\" = t.\"User ID\"", "using": []}] | ["u.\"Age group\"", "t.\"Purchase Preference Tag\""] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |


## S58

类别 `data`；来源 `python`；调用 `4a14a8e4fa954ab9b25e742b253719de`；状态 `success`。

```sql

SELECT 
  u."Age group" as age,
  ROUND(100.0*SUM(m."Number of Shares")/NULLIF(SUM(m."Number of Participants"),0),3) as share_rate,
  ROUND(AVG(m."Number of Shares"),2) as avg_shares,
  ROUND(AVG(m."Event Feedback Rating"),2) as avg_rating,
  ROUND(AVG(m."Event Conversion Rate"),3) as avg_conv,
  ROUND(100.0*SUM(CASE WHEN m."Is Event Blocked"='Yes' THEN 1 ELSE 0 END)/COUNT(*),1) as blocked_pct,
  ROUND(100.0*SUM(CASE WHEN m."Usage Status"='Used' THEN 1 ELSE 0 END)/COUNT(*),1) as used_pct,
  COUNT(*) as interactions
FROM user_basic_information_table_1 u
JOIN marketing_campaign_interaction m ON u."User ID"=m."User ID"
GROUP BY u."Age group"
ORDER BY u."Age group"

```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-046/attempt-01/sql/S58.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-046/attempt-01/sql/S58.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-046/attempt-01/results/S58.rows.jsonl)；完整：True；SHA256：`c42add8fd186f027a6f3d42a9bacc2b6288cf4d99c5d8141b71c358ae9097b27`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "u", "kind": "base", "block": null, "base_tables": ["user_basic_information_table_1"]}, {"alias": "m", "kind": "base", "block": null, "base_tables": ["marketing_campaign_interaction"]}] | [{"type": "INNER", "right": "marketing_campaign_interaction AS m", "on": "u.\"User ID\" = m.\"User ID\"", "using": []}] | ["u.\"Age group\""] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |
| B1 | AVG(m."Number of Shares") | [{"table": "marketing_campaign_interaction", "column": "Number of Shares"}] | [] | False |
| B1 | AVG(m."Event Feedback Rating") | [{"table": "marketing_campaign_interaction", "column": "Event Feedback Rating"}] | [] | False |
| B1 | AVG(m."Event Conversion Rate") | [{"table": "marketing_campaign_interaction", "column": "Event Conversion Rate"}] | [] | False |
| B1 | COUNT(*) | [] | [] | True |
| B1 | COUNT(*) | [] | [] | True |
| B1 | SUM(m."Number of Shares") | [{"table": "marketing_campaign_interaction", "column": "Number of Shares"}] | [] | False |
| B1 | SUM(m."Number of Participants") | [{"table": "marketing_campaign_interaction", "column": "Number of Participants"}] | [] | False |
| B1 | SUM(CASE WHEN m."Is Event Blocked" = 'Yes' THEN 1 ELSE 0 END) | [] | [{"table": "marketing_campaign_interaction", "column": "Is Event Blocked"}] | False |
| B1 | SUM(CASE WHEN m."Usage Status" = 'Used' THEN 1 ELSE 0 END) | [] | [{"table": "marketing_campaign_interaction", "column": "Usage Status"}] | False |


## S59

类别 `data`；来源 `python`；调用 `4a14a8e4fa954ab9b25e742b253719de`；状态 `success`。

```sql
SELECT "Age group", "Gender", COUNT(*) as cnt FROM user_basic_information_table_1 GROUP BY "Age group", "Gender"
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-046/attempt-01/sql/S59.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-046/attempt-01/sql/S59.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-046/attempt-01/results/S59.rows.jsonl)；完整：True；SHA256：`a3ff2067a8c66fc20c06ee9a32cf10d88379eb732a25db53d2a70942ca3e1226`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "user_basic_information_table_1", "kind": "base", "block": null, "base_tables": ["user_basic_information_table_1"]}] | [] | ["\"Age group\"", "\"Gender\""] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |


## S60

类别 `data`；来源 `python`；调用 `4a14a8e4fa954ab9b25e742b253719de`；状态 `success`。

```sql
SELECT "Age group", "Income level", COUNT(*) as cnt FROM user_basic_information_table_1 GROUP BY "Age group", "Income level"
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-046/attempt-01/sql/S60.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-046/attempt-01/sql/S60.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-046/attempt-01/results/S60.rows.jsonl)；完整：True；SHA256：`baa2910040938136349c69adad823cc5517dd1499b391a9aebb5b93c9fc8755d`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "user_basic_information_table_1", "kind": "base", "block": null, "base_tables": ["user_basic_information_table_1"]}] | [] | ["\"Age group\"", "\"Income level\""] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |


## S61

类别 `data`；来源 `python`；调用 `4a14a8e4fa954ab9b25e742b253719de`；状态 `success`。

```sql
SELECT "Age group", "Education Level", COUNT(*) as cnt FROM user_basic_information_table_1 GROUP BY "Age group", "Education Level"
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-046/attempt-01/sql/S61.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-046/attempt-01/sql/S61.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-046/attempt-01/results/S61.rows.jsonl)；完整：True；SHA256：`ad0a440253961ec57181407f4cadb4e3bab6acda648900e28c8f8be310355650`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "user_basic_information_table_1", "kind": "base", "block": null, "base_tables": ["user_basic_information_table_1"]}] | [] | ["\"Age group\"", "\"Education Level\""] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |


## S62

类别 `data`；来源 `python`；调用 `58b4b360f06b4d0b8815104300ab7b79`；状态 `success`。

```sql

SELECT u."Age group" as age, 
  t."Price Sensitivity" as ps, 
  COUNT(*) as cnt,
  SUM(CASE WHEN t."Is At-Risk User"='Yes' THEN 1 ELSE 0 END) as at_risk
FROM user_basic_information_table_1 u
JOIN user_tags_table t ON u."User ID"=t."User ID"
GROUP BY u."Age group", t."Price Sensitivity"

```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-046/attempt-01/sql/S62.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-046/attempt-01/sql/S62.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-046/attempt-01/results/S62.rows.jsonl)；完整：True；SHA256：`0f6cffa0fc9c599f157935e9cbe83a71529d1812e3a377f511fbfa518043efec`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "u", "kind": "base", "block": null, "base_tables": ["user_basic_information_table_1"]}, {"alias": "t", "kind": "base", "block": null, "base_tables": ["user_tags_table"]}] | [{"type": "INNER", "right": "user_tags_table AS t", "on": "u.\"User ID\" = t.\"User ID\"", "using": []}] | ["u.\"Age group\"", "t.\"Price Sensitivity\""] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |
| B1 | SUM(CASE WHEN t."Is At-Risk User" = 'Yes' THEN 1 ELSE 0 END) | [] | [{"table": "user_tags_table", "column": "Is At-Risk User"}] | False |


## S63

类别 `data`；来源 `python`；调用 `58b4b360f06b4d0b8815104300ab7b79`；状态 `success`。

```sql

SELECT u."Age group" as age, 
  t."Spending Power" as sp, 
  COUNT(*) as cnt
FROM user_basic_information_table_1 u
JOIN user_tags_table t ON u."User ID"=t."User ID"
GROUP BY u."Age group", t."Spending Power"

```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-046/attempt-01/sql/S63.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-046/attempt-01/sql/S63.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-046/attempt-01/results/S63.rows.jsonl)；完整：True；SHA256：`14b48a970c3767995b691765f887d0381e21c3f8f32e33a69fc47811125c10e5`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "u", "kind": "base", "block": null, "base_tables": ["user_basic_information_table_1"]}, {"alias": "t", "kind": "base", "block": null, "base_tables": ["user_tags_table"]}] | [{"type": "INNER", "right": "user_tags_table AS t", "on": "u.\"User ID\" = t.\"User ID\"", "using": []}] | ["u.\"Age group\"", "t.\"Spending Power\""] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |


## S64

类别 `data`；来源 `python`；调用 `58b4b360f06b4d0b8815104300ab7b79`；状态 `success`。

```sql

SELECT u."Age group" as age, 
  t."Is High-Value User" as hv,
  t."Is Potential Conversion User" as pc,
  COUNT(*) as cnt
FROM user_basic_information_table_1 u
JOIN user_tags_table t ON u."User ID"=t."User ID"
GROUP BY u."Age group", t."Is High-Value User", t."Is Potential Conversion User"

```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-046/attempt-01/sql/S64.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-046/attempt-01/sql/S64.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-046/attempt-01/results/S64.rows.jsonl)；完整：True；SHA256：`f025ce7853212d7a9371f755a80acbacdc9de85e953afb5938a30613f47e7234`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "u", "kind": "base", "block": null, "base_tables": ["user_basic_information_table_1"]}, {"alias": "t", "kind": "base", "block": null, "base_tables": ["user_tags_table"]}] | [{"type": "INNER", "right": "user_tags_table AS t", "on": "u.\"User ID\" = t.\"User ID\"", "using": []}] | ["u.\"Age group\"", "t.\"Is High-Value User\"", "t.\"Is Potential Conversion User\""] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |


## S65

类别 `data`；来源 `python`；调用 `58b4b360f06b4d0b8815104300ab7b79`；状态 `success`。

```sql

SELECT u."Age group" as age, 
  t."Is High-Value User" as hv,
  COUNT(*) as cnt,
  SUM(CASE WHEN t."Is At-Risk User"='Yes' THEN 1 ELSE 0 END) as at_risk,
  ROUND(100.0*SUM(CASE WHEN t."Is At-Risk User"='Yes' THEN 1 ELSE 0 END)/COUNT(*),1) as at_risk_pct
FROM user_basic_information_table_1 u
JOIN user_tags_table t ON u."User ID"=t."User ID"
GROUP BY u."Age group", t."Is High-Value User"

```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-046/attempt-01/sql/S65.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-046/attempt-01/sql/S65.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-046/attempt-01/results/S65.rows.jsonl)；完整：True；SHA256：`a714172ba9f54145921e1834246a049adc2c1a35905823dcbebcffa9c95f5f69`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "u", "kind": "base", "block": null, "base_tables": ["user_basic_information_table_1"]}, {"alias": "t", "kind": "base", "block": null, "base_tables": ["user_tags_table"]}] | [{"type": "INNER", "right": "user_tags_table AS t", "on": "u.\"User ID\" = t.\"User ID\"", "using": []}] | ["u.\"Age group\"", "t.\"Is High-Value User\""] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |
| B1 | SUM(CASE WHEN t."Is At-Risk User" = 'Yes' THEN 1 ELSE 0 END) | [] | [{"table": "user_tags_table", "column": "Is At-Risk User"}] | False |
| B1 | COUNT(*) | [] | [] | True |
| B1 | SUM(CASE WHEN t."Is At-Risk User" = 'Yes' THEN 1 ELSE 0 END) | [] | [{"table": "user_tags_table", "column": "Is At-Risk User"}] | False |


## S66

类别 `data`；来源 `python`；调用 `58b4b360f06b4d0b8815104300ab7b79`；状态 `success`。

```sql

SELECT age, evt, interactions, avg_rating, avg_shares, avg_conv, used_pct
FROM (
  SELECT 
    u."Age group" as age,
    m."Event Name" as evt,
    COUNT(*) as interactions,
    ROUND(AVG(m."Event Feedback Rating"),2) as avg_rating,
    ROUND(AVG(m."Number of Shares"),1) as avg_shares,
    ROUND(AVG(m."Event Conversion Rate"),3) as avg_conv,
    ROUND(100.0*SUM(CASE WHEN m."Usage Status"='Used' THEN 1 ELSE 0 END)/COUNT(*),1) as used_pct,
    ROW_NUMBER() OVER (PARTITION BY u."Age group" ORDER BY AVG(m."Event Feedback Rating") DESC) as rn
  FROM user_basic_information_table_1 u
  JOIN marketing_campaign_interaction m ON u."User ID"=m."User ID"
  GROUP BY u."Age group", m."Event Name"
  HAVING COUNT(*) >= 3
)
WHERE rn <= 3

```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-046/attempt-01/sql/S66.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-046/attempt-01/sql/S66.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-046/attempt-01/results/S66.rows.jsonl)；完整：True；SHA256：`87c8643757c5f133758b2b97d5b3a2d69a730b300a33be5d6a8636365b9c5038`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "u", "kind": "base", "block": null, "base_tables": ["user_basic_information_table_1"]}, {"alias": "m", "kind": "base", "block": null, "base_tables": ["marketing_campaign_interaction"]}] | [{"type": "INNER", "right": "marketing_campaign_interaction AS m", "on": "u.\"User ID\" = m.\"User ID\"", "using": []}] | ["u.\"Age group\"", "m.\"Event Name\""] |
| B2 | [{"alias": "", "kind": "derived", "block": "B1", "base_tables": ["marketing_campaign_interaction", "user_basic_information_table_1"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |
| B1 | AVG(m."Event Feedback Rating") | [{"table": "marketing_campaign_interaction", "column": "Event Feedback Rating"}] | [] | False |
| B1 | AVG(m."Number of Shares") | [{"table": "marketing_campaign_interaction", "column": "Number of Shares"}] | [] | False |
| B1 | AVG(m."Event Conversion Rate") | [{"table": "marketing_campaign_interaction", "column": "Event Conversion Rate"}] | [] | False |
| B1 | COUNT(*) | [] | [] | True |
| B1 | COUNT(*) | [] | [] | True |
| B1 | SUM(CASE WHEN m."Usage Status" = 'Used' THEN 1 ELSE 0 END) | [] | [{"table": "marketing_campaign_interaction", "column": "Usage Status"}] | False |
| B1 | AVG(m."Event Feedback Rating") | [{"table": "marketing_campaign_interaction", "column": "Event Feedback Rating"}] | [] | False |


## S67

类别 `data`；来源 `python`；调用 `581d2ee30d22423ba17ff1842a802215`；状态 `success`。

```sql

SELECT u."Age group" as age, m."Event Feedback Rating" as rating,
       m."Number of Shares" as shares, m."Event Conversion Rate" as conv,
       m."Event Dwell Time" as dwell, m."Number of Participants" as participants
FROM user_basic_information_table_1 u
JOIN marketing_campaign_interaction m ON u."User ID"=m."User ID"

```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-046/attempt-01/sql/S67.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-046/attempt-01/sql/S67.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-046/attempt-01/results/S67.rows.jsonl)；完整：True；SHA256：`707c1a6dc655f7f3f39df658be4b3f045516c166de48bb936e841ae6180c9961`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "u", "kind": "base", "block": null, "base_tables": ["user_basic_information_table_1"]}, {"alias": "m", "kind": "base", "block": null, "base_tables": ["marketing_campaign_interaction"]}] | [{"type": "INNER", "right": "marketing_campaign_interaction AS m", "on": "u.\"User ID\" = m.\"User ID\"", "using": []}] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |


## S68

类别 `data`；来源 `python`；调用 `581d2ee30d22423ba17ff1842a802215`；状态 `success`。

```sql

SELECT u."Age group" as age,
  t."Is At-Risk User" as risk,
  AVG(m."Number of Shares") as avg_shares,
  AVG(m."Event Feedback Rating") as avg_rating,
  AVG(m."Event Conversion Rate") as avg_conv,
  AVG(m."Event Dwell Time") as avg_dwell
FROM user_basic_information_table_1 u
JOIN user_tags_table t ON u."User ID"=t."User ID"
JOIN marketing_campaign_interaction m ON u."User ID"=m."User ID"
GROUP BY u."Age group", t."Is At-Risk User"

```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-046/attempt-01/sql/S68.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-046/attempt-01/sql/S68.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-046/attempt-01/results/S68.rows.jsonl)；完整：True；SHA256：`b26c9e2f12c9128ae1df3da02c1b62f7bd3ff4d0c394a96ce0c1da09cb8c458f`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "u", "kind": "base", "block": null, "base_tables": ["user_basic_information_table_1"]}, {"alias": "t", "kind": "base", "block": null, "base_tables": ["user_tags_table"]}, {"alias": "m", "kind": "base", "block": null, "base_tables": ["marketing_campaign_interaction"]}] | [{"type": "INNER", "right": "user_tags_table AS t", "on": "u.\"User ID\" = t.\"User ID\"", "using": []}, {"type": "INNER", "right": "marketing_campaign_interaction AS m", "on": "u.\"User ID\" = m.\"User ID\"", "using": []}] | ["u.\"Age group\"", "t.\"Is At-Risk User\""] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | AVG(m."Number of Shares") | [{"table": "marketing_campaign_interaction", "column": "Number of Shares"}] | [] | False |
| B1 | AVG(m."Event Feedback Rating") | [{"table": "marketing_campaign_interaction", "column": "Event Feedback Rating"}] | [] | False |
| B1 | AVG(m."Event Conversion Rate") | [{"table": "marketing_campaign_interaction", "column": "Event Conversion Rate"}] | [] | False |
| B1 | AVG(m."Event Dwell Time") | [{"table": "marketing_campaign_interaction", "column": "Event Dwell Time"}] | [] | False |

