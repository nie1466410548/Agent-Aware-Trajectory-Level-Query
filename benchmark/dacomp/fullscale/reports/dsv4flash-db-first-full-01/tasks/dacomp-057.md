# dacomp-057

The marketing team has observed complex decay patterns in the customer acquisition efficie…

运行：已提交。官方未评分。全部 SQL 尝试/成功 74/71；数据 SQL 70/67；Python 7 次。

完整原题：

The marketing team has observed complex decay patterns in the customer acquisition efficiency of multiple long-running advertising campaigns. Based on a joined analysis of the `google_ads__customer_acquisition_analysis` and `google_ads__campaign_report` tables, identify campaigns that have been running for more than 120 days and, in the last 30 days, exhibit a Customer Acquisition Cost (CAC) growth rate exceeding 25% while their LTV/CAC ratio has declined by more than 20%.

You are required to conduct an in-depth analysis of how different combinations of `campaign_lifecycle_stage` (Growth, Mature, Decline), `advertising_channel_type`, `customer_maturity_stage`, and `account_maturity_stage` impact this acquisition efficiency decay. Incorporate multi-dimensional metrics such as `acquisition_sophistication_score`, `cac_efficiency_percentile`, and `channel_diversity_count` to build a comprehensive decay risk assessment model that includes factors like channel saturation, competitive intensity, and customer quality stratification. 

Additionally, consider the distribution of `strategic_customer_segment`, `retention_risk` warning signals, and the `scale_opportunity` potential assessment to provide differentiated optimization recommendations for campaigns in various decay stages. Your focus should be on adjusting acquisition strategies for high-value customer segments and proposing budget reallocation plans.

| 表 | 行数 | 列数 |
| --- | --- | --- |
| google_ads__campaign_report | 9976 | 16 |
| google_ads__customer_acquisition_analysis | 10000 | 44 |


实际路线（分析者依据 SQL/源码概括，不代表 Agent 自述）：SQL 连接广告与获客数据并识别衰退活动 → Python 分层汇总、月趋势和风险比较 → 渠道与客户群优化建议。

数据库大小：6,668,288 字节。

## 数据 SQL

| SQL | 状态 | 基础表 | Join 输入/类型 | GROUP BY | 聚合表达式 | 结果行数 | 数据库 ms |
| --- | --- | --- | --- | --- | --- | --- | --- |
| [S3/Q1](#s3) | success | ["google_ads__customer_acquisition_analysis"] | 0 / {} | [] | ["COUNT(*)"] | 1 | 2.6 |
| [S4/Q2](#s4) | failed | ["google_ads__customer_acquisition_analysis"] | 0 / {} | [] | ["MIN(date_day)", "MAX(date_day)", "COUNT(DISTINCT campaign_id)", "COUNT(DISTINCT account_id)"] | unknown | 未取得；调用总时长 0.185 ms |
| [S5/Q3](#s5) | success | ["google_ads__campaign_report"] | 0 / {} | [] | ["MIN(date_day)", "MAX(date_day)", "COUNT(DISTINCT campaign_id)", "COUNT(DISTINCT account_id)"] | 1 | 5.162 |
| [S8/Q4](#s8) | success | ["google_ads__customer_acquisition_analysis"] | 0 / {} | [] | [] | 6 | 3.127 |
| [S9/Q5](#s9) | success | ["google_ads__customer_acquisition_analysis"] | 0 / {} | [] | [] | 5 | 2.995 |
| [S10/Q6](#s10) | success | ["google_ads__customer_acquisition_analysis"] | 0 / {} | [] | [] | 5 | 3.097 |
| [S11/Q7](#s11) | success | ["google_ads__customer_acquisition_analysis"] | 0 / {} | [] | [] | 3 | 2.926 |
| [S12/Q8](#s12) | success | ["google_ads__customer_acquisition_analysis"] | 0 / {} | [] | [] | 6 | 3.488 |
| [S13/Q9](#s13) | success | ["google_ads__customer_acquisition_analysis"] | 0 / {} | [] | [] | 4 | 3.043 |
| [S14/Q10](#s14) | success | ["google_ads__customer_acquisition_analysis"] | 0 / {} | [] | [] | 3 | 3.362 |
| [S15/Q11](#s15) | success | ["google_ads__customer_acquisition_analysis"] | 0 / {} | [] | [] | 4 | 3.793 |
| [S16/Q12](#s16) | success | ["google_ads__customer_acquisition_analysis"] | 0 / {} | [] | [] | 8 | 3.853 |
| [S17/Q13](#s17) | success | ["google_ads__campaign_report"] | 0 / {} | [] | [] | 20 | 0.375 |
| [S18/Q14](#s18) | success | ["google_ads__campaign_report"] | 0 / {} | [] | ["MIN(date_day)", "MAX(date_day)", "COUNT(DISTINCT campaign_id)"] | 1 | 4.269 |
| [S19/Q15](#s19) | success | ["google_ads__campaign_report"] | 0 / {} | [] | [] | 3 | 2.587 |
| [S20/Q16](#s20) | success | ["google_ads__campaign_report"] | 0 / {} | [] | [] | 5 | 2.659 |
| [S21/Q17](#s21) | success | ["google_ads__campaign_report"] | 0 / {} | [] | ["COUNT(*)"] | 1 | 1.45 |
| [S22/Q18](#s22) | success | ["google_ads__customer_acquisition_analysis"] | 0 / {} | [] | [] | 8 | 3.448 |
| [S23/Q19](#s23) | success | ["google_ads__campaign_report"] | 0 / {} | [] | [] | 8 | 2.758 |
| [S24/Q20](#s24) | success | ["google_ads__customer_acquisition_analysis"] | 0 / {} | [] | [] | 5 | 0.472 |
| [S25/Q21](#s25) | success | ["google_ads__customer_acquisition_analysis"] | 0 / {} | [] | ["MIN(date_day)", "MAX(date_day)", "COUNT(DISTINCT account_id)"] | 1 | 3.908 |
| [S26/Q22](#s26) | success | ["google_ads__customer_acquisition_analysis"] | 0 / {} | ["STRFTIME('%Y-%m', date_day)"] | ["COUNT(*)", "COUNT(DISTINCT account_id)"] | 1 | 6.849 |
| [S27/Q23](#s27) | success | ["google_ads__customer_acquisition_analysis"] | 0 / {} | [] | [] | 5 | 0.373 |
| [S28/Q24](#s28) | success | ["google_ads__campaign_report"] | 0 / {} | [] | [] | 5 | 0.327 |
| [S29/Q25](#s29) | success | ["google_ads__customer_acquisition_analysis"] | 0 / {} | ["account_id", "date_day", "advertising_channel_type", "advertising_channel_subtype", "customer_maturity_stage", "campaign_lifecycle_stage"] | ["COUNT(*)"] | 10 | 12.732 |
| [S30/Q26](#s30) | success | ["google_ads__campaign_report"] | 0 / {} | ["account_id", "date_day", "advertising_channel_type", "advertising_channel_subtype"] | ["COUNT(*)", "COUNT(DISTINCT campaign_id)"] | 10 | 8.821 |
| [S31/Q27](#s31) | success | ["google_ads__customer_acquisition_analysis"] | 0 / {} | ["account_id", "date_day", "advertising_channel_type", "advertising_channel_subtype", "customer_maturity_stage", "campaign_lifecycle_stage", "strategic_customer_segment", "acquisition_cohort"] | ["COUNT(*)"] | 10 | 13.729 |
| [S32/Q28](#s32) | success | ["google_ads__customer_acquisition_analysis"] | 0 / {} | [] | ["COUNT(*)", "COUNT(DISTINCT account_id \|\| '\|' \|\| date_day \|\| '\|' \|\| advertising_channel_type \|\| '\|' \|\| advertising_channel_subtype)"] | 1 | 17.752 |
| [S33/Q29](#s33) | success | ["google_ads__campaign_report"] | 0 / {} | ["campaign_id"] | ["MIN(date_day)", "MAX(date_day)", "MAX(date_day)", "MIN(date_day)"] | 20 | 7.749 |
| [S34/Q30](#s34) | success | ["google_ads__campaign_report"] | 0 / {} | ["campaign_id"] | ["MIN(SUBSTRING(date_day, 1, 10))", "MAX(SUBSTRING(date_day, 1, 10))", "MAX(SUBSTRING(date_day, 1, 10))", "MIN(SUBSTRING(date_day, 1, 10))"] | 84 | 9.048 |
| [S35/Q31](#s35) | success | ["google_ads__campaign_report"] | 0 / {} | ["campaign_id"] | ["MIN(SUBSTRING(date_day, 1, 10))", "MAX(SUBSTRING(date_day, 1, 10))", "MAX(SUBSTRING(date_day, 1, 10))", "MIN(SUBSTRING(date_day, 1, 10))", "MAX(SUBSTRING(date_day, 1, 10))"] | 77 | 9.21 |
| [S36/Q32](#s36) | success | ["google_ads__customer_acquisition_analysis"] | 0 / {} | ["account_id"] | ["MIN(SUBSTRING(date_day, 1, 10))", "MAX(SUBSTRING(date_day, 1, 10))", "COUNT(*)"] | 8 | 8.409 |
| [S37/Q33](#s37) | success | ["google_ads__customer_acquisition_analysis"] | 0 / {} | ["SUBSTRING(date_day, 1, 7)"] | ["COUNT(*)"] | 58 | 5.965 |
| [S38/Q34](#s38) | success | ["google_ads__customer_acquisition_analysis"] | 0 / {} | ["SUBSTRING(date_day, 1, 10)"] | ["COUNT(*)"] | 70 | 3.115 |
| [S39/Q35](#s39) | success | ["google_ads__customer_acquisition_analysis"] | 0 / {} | ["SUBSTRING(date_day, 1, 7)"] | ["COUNT(*)"] | 30 | 5.028 |
| [S40/Q36](#s40) | success | ["google_ads__customer_acquisition_analysis"] | 0 / {} | ["SUBSTRING(date_day, 1, 7)"] | ["COUNT(*)"] | 18 | 3.702 |
| [S41/Q37](#s41) | success | ["google_ads__customer_acquisition_analysis"] | 0 / {} | ["account_id", "advertising_channel_type"] | ["COUNT(DISTINCT SUBSTRING(date_day, 1, 10))"] | 19 | 3.272 |
| [S42/Q38](#s42) | success | ["google_ads__customer_acquisition_analysis"] | 0 / {} | [] | ["COUNT(*)", "COUNT(DISTINCT account_id \|\| '\|' \|\| SUBSTRING(date_day, 1, 10))"] | 1 | 3.031 |
| [S43/Q39](#s43) | success | ["google_ads__customer_acquisition_analysis"] | 0 / {} | ["account_id", "advertising_channel_type"] | ["COUNT(DISTINCT SUBSTRING(date_day, 1, 10))"] | 6 | 2.896 |
| [S44/Q40](#s44) | success | ["google_ads__customer_acquisition_analysis"] | 0 / {} | ["SUBSTRING(date_day, 1, 10)"] | ["COUNT(*)"] | 18 | 3.011 |
| [S45/Q41](#s45) | success | ["google_ads__customer_acquisition_analysis"] | 0 / {} | [] | ["COUNT(*)"] | 1 | 2.971 |
| [S46/Q42](#s46) | success | ["google_ads__campaign_report"] | 0 / {} | [] | ["COUNT(*)", "COUNT(DISTINCT SUBSTRING(date_day, 1, 10))"] | 1 | 5.753 |
| [S47/Q43](#s47) | success | ["google_ads__customer_acquisition_analysis"] | 0 / {} | ["account_id", "advertising_channel_type"] | ["COUNT(DISTINCT SUBSTRING(date_day, 1, 10))"] | 20 | 3.337 |
| [S48/Q44](#s48) | success | ["google_ads__customer_acquisition_analysis"] | 0 / {} | ["account_id", "advertising_channel_type"] | ["COUNT(DISTINCT SUBSTRING(date_day, 1, 10))"] | 29 | 4.872 |
| [S49/Q45](#s49) | success | ["google_ads__customer_acquisition_analysis"] | 0 / {} | ["SUBSTRING(date_day, 1, 10)"] | ["COUNT(*)"] | 214 | 3.504 |
| [S50/Q46](#s50) | success | ["google_ads__customer_acquisition_analysis"] | 0 / {} | ["SUBSTRING(date_day, 1, 10)"] | ["COUNT(*)"] | 100 | 3.481 |
| [S51/Q47](#s51) | success | ["google_ads__customer_acquisition_analysis"] | 0 / {} | [] | ["COUNT(*)", "COUNT(DISTINCT account_id \|\| '\|' \|\| SUBSTRING(date_day, 1, 10) \|\| '\|' \|\| advertising_channel_type \|\| '\|' \|\| advertising_channel_subtype \|\| '\|' \|\| customer_maturity_stage \|\| '\|' \|\| campaign_lifecycle_stage \|\| '\|' \|\| strategic_customer_segment \|\| '\|' \|\| account_maturity_stage)"] | 1 | 28.966 |
| [S52/Q48](#s52) | success | ["google_ads__customer_acquisition_analysis"] | 0 / {} | [] | ["COUNT(DISTINCT account_id \|\| '\|' \|\| SUBSTRING(date_day, 1, 10) \|\| '\|' \|\| advertising_channel_type \|\| '\|' \|\| advertising_channel_subtype \|\| '\|' \|\| customer_maturity_stage \|\| '\|' \|\| campaign_lifecycle_stage)"] | 1 | 23.091 |
| [S53/Q49](#s53) | success | ["google_ads__campaign_report", "google_ads__customer_acquisition_analysis"] | 2 / {'LEFT': 1} | ["campaign_id", "c.campaign_id"] | ["MIN(SUBSTRING(date_day, 1, 10))", "MAX(SUBSTRING(date_day, 1, 10))", "MAX(SUBSTRING(date_day, 1, 10))", "MIN(SUBSTRING(date_day, 1, 10))", "COUNT(a.rowid)"] | 77 | 222.752 |
| [S54/Q50](#s54) | success | ["google_ads__campaign_report", "google_ads__customer_acquisition_analysis"] | 2 / {'LEFT': 1} | ["campaign_id", "c.campaign_id"] | ["MIN(SUBSTRING(date_day, 1, 10))", "MAX(SUBSTRING(date_day, 1, 10))", "MAX(SUBSTRING(date_day, 1, 10))", "MIN(SUBSTRING(date_day, 1, 10))", "COUNT(a.rowid)"] | 16 | 222.985 |
| [S55/Q51](#s55) | success | ["google_ads__customer_acquisition_analysis"] | 0 / {} | ["account_id", "advertising_channel_type", "advertising_channel_subtype"] | ["COUNT(*)"] | 45 | 9.329 |
| [S56/Q52](#s56) | success | ["google_ads__customer_acquisition_analysis"] | 0 / {} | [] | [] | 8 | 4.716 |
| [S57/Q53](#s57) | success | ["google_ads__customer_acquisition_analysis"] | 0 / {} | ["account_id", "advertising_channel_type", "advertising_channel_subtype"] | ["COUNT(*)", "MIN(SUBSTRING(date_day, 1, 10))", "MAX(SUBSTRING(date_day, 1, 10))"] | 20 | 6.91 |
| [S58/Q54](#s58) | success | ["google_ads__campaign_report", "google_ads__customer_acquisition_analysis"] | 2 / {'INNER': 1} | ["campaign_id", "c.campaign_id"] | ["MIN(SUBSTRING(date_day, 1, 10))", "MAX(SUBSTRING(date_day, 1, 10))", "MAX(SUBSTRING(date_day, 1, 10))", "MIN(SUBSTRING(date_day, 1, 10))", "MAX(SUBSTRING(a.date_day, 1, 10))", "MIN(SUBSTRING(a.date_day, 1, 10))", "COUNT(a.rowid)"] | 61 | 20.315 |
| [S59/Q55](#s59) | success | ["google_ads__campaign_report", "google_ads__customer_acquisition_analysis"] | 2 / {'INNER': 2} | ["campaign_id", "campaign_id", "j.campaign_id"] | ["MIN(SUBSTRING(date_day, 1, 10))", "MAX(SUBSTRING(date_day, 1, 10))", "MAX(SUBSTRING(date_day, 1, 10))", "MIN(SUBSTRING(date_day, 1, 10))", "MAX(jd)", "MAX(d)", "COUNT(*)", "MAX(jd)", "MIN(jd)", "SUM(CASE WHEN j.jd >= r.ref_jd - 29 THEN 1 ELSE 0 END)", "SUM(CASE WHEN j.jd BETWEEN r.ref_jd - 59 AND r.ref_jd - 30 THEN 1 ELSE 0 END)"] | 61 | 44.772 |
| [S60/Q56](#s60) | success | ["google_ads__campaign_report", "google_ads__customer_acquisition_analysis"] | 2 / {'INNER': 2} | ["campaign_id", "campaign_id", "j.campaign_id"] | ["MIN(SUBSTRING(date_day, 1, 10))", "MAX(SUBSTRING(date_day, 1, 10))", "MAX(SUBSTRING(date_day, 1, 10))", "MIN(SUBSTRING(date_day, 1, 10))", "MAX(jd)", "SUM(CASE WHEN j.jd >= r.ref_jd - 29 THEN j.spend ELSE 0 END)", "SUM(CASE WHEN j.jd >= r.ref_jd - 29 THEN j.conversions ELSE 0 END)", "SUM(CASE WHEN j.jd >= r.ref_jd - 29 THEN j.conversions * j.ltv_cac_ratio ELSE 0 END)", "SUM(CASE WHEN j.jd BETWEEN r.ref_jd - 59 AND r.ref_jd - 30 THEN j.spend ELSE 0 END)", "SUM(CASE WHEN j.jd BETWEEN r.ref_jd - 59 AND r.ref_jd - 30 THEN j.conversions ELSE 0 END)", "SUM(CASE WHEN j.jd BETWEEN r.ref_jd - 59 AND r.ref_jd - 30 THEN j.conversions * j.ltv_cac_ratio ELSE 0 END)"] | 61 | 51.003 |
| [S61/Q57](#s61) | success | ["google_ads__campaign_report", "google_ads__customer_acquisition_analysis"] | 2 / {'INNER': 2} | ["campaign_id", "campaign_id", "j.campaign_id"] | ["MIN(SUBSTRING(date_day, 1, 10))", "MAX(SUBSTRING(date_day, 1, 10))", "MAX(SUBSTRING(date_day, 1, 10))", "MIN(SUBSTRING(date_day, 1, 10))", "MAX(jd)", "SUM(CASE WHEN j.jd >= r.ref_jd - 29 THEN j.spend ELSE 0 END)", "SUM(CASE WHEN j.jd >= r.ref_jd - 29 THEN j.conversions ELSE 0 END)", "SUM(CASE WHEN j.jd >= r.ref_jd - 29 THEN j.conversions * j.ltv_cac_ratio ELSE 0 END)", "SUM(CASE WHEN j.jd BETWEEN r.ref_jd - 59 AND r.ref_jd - 30 THEN j.spend ELSE 0 END)", "SUM(CASE WHEN j.jd BETWEEN r.ref_jd - 59 AND r.ref_jd - 30 THEN j.conversions ELSE 0 END)", "SUM(CASE WHEN j.jd BETWEEN r.ref_jd - 59 AND r.ref_jd - 30 THEN j.conversions * j.ltv_cac_ratio ELSE 0 END)", "COUNT(*)", "SUM(CASE WHEN cac_last > 0 AND cac_prior > 0 AND cac_growth > 0.25 AND ltv_cac_change < -0.20 THEN 1 ELSE 0 END)"] | 1 | 49.782 |
| [S62/Q58](#s62) | success | ["google_ads__campaign_report"] | 2 / {'INNER': 2} | ["campaign_id", "campaign_id"] | ["MAX(SUBSTRING(date_day, 1, 10))", "MAX(SUBSTRING(date_day, 1, 10))", "MIN(SUBSTRING(date_day, 1, 10))", "SUM(CASE WHEN jd >= JULIANDAY(last_date) - 29 THEN spend ELSE 0 END)", "SUM(CASE WHEN jd >= JULIANDAY(last_date) - 29 THEN conversions ELSE 0 END)", "SUM(CASE WHEN jd BETWEEN JULIANDAY(last_date) - 59 AND JULIANDAY(last_date) - 30 THEN spend ELSE 0 END)", "SUM(CASE WHEN jd BETWEEN JULIANDAY(last_date) - 59 AND JULIANDAY(last_date) - 30 THEN conversions ELSE 0 END)", "SUM(CASE WHEN jd >= JULIANDAY(last_date) - 29 THEN spend ELSE 0 END)", "SUM(CASE WHEN jd BETWEEN JULIANDAY(last_date) - 59 AND JULIANDAY(last_date) - 30 THEN spend ELSE 0 END)", "SUM(CASE WHEN jd >= JULIANDAY(last_date) - 29 THEN conversions ELSE 0 END)", "SUM(CASE WHEN jd BETWEEN JULIANDAY(last_date) - 59 AND JULIANDAY(last_date) - 30 THEN conversions ELSE 0 END)"] | 77 | 39.846 |
| [S63/Q59](#s63) | failed | ["google_ads__campaign_report", "google_ads__customer_acquisition_analysis"] | 2 / {'INNER': 1} | ["campaign_id", "campaign_id"] | ["MAX(SUBSTRING(date_day, 1, 10))", "MIN(SUBSTRING(date_day, 1, 10))", "SUM(CASE WHEN jd >= JULIANDAY('2024-12-31') - 29 THEN spend ELSE 0 END)", "SUM(CASE WHEN jd >= JULIANDAY('2024-12-31') - 29 THEN conversions ELSE 0 END)", "SUM(CASE WHEN jd BETWEEN JULIANDAY('2024-12-31') - 59 AND JULIANDAY('2024-12-31') - 30 THEN spend ELSE 0 END)", "SUM(CASE WHEN jd BETWEEN JULIANDAY('2024-12-31') - 59 AND JULIANDAY('2024-12-31') - 30 THEN conversions ELSE 0 END)", "SUM(CASE WHEN jd >= JULIANDAY('2024-12-31') - 29 THEN spend ELSE 0 END)", "SUM(CASE WHEN jd BETWEEN JULIANDAY('2024-12-31') - 59 AND JULIANDAY('2024-12-31') - 30 THEN spend ELSE 0 END)", "SUM(CASE WHEN jd >= JULIANDAY('2024-12-31') - 29 THEN conversions ELSE 0 END)", "SUM(CASE WHEN jd BETWEEN JULIANDAY('2024-12-31') - 59 AND JULIANDAY('2024-12-31') - 30 THEN conversions ELSE 0 END)"] | unknown | 未取得；调用总时长 0.391 ms |
| [S64/Q60](#s64) | success | ["google_ads__campaign_report", "google_ads__customer_acquisition_analysis"] | 2 / {'INNER': 1} | ["campaign_id", "campaign_id"] | ["MIN(SUBSTRING(date_day, 1, 10))", "MAX(SUBSTRING(date_day, 1, 10))", "MAX(SUBSTRING(date_day, 1, 10))", "MIN(SUBSTRING(date_day, 1, 10))", "SUM(CASE WHEN jd >= JULIANDAY('2024-12-31') - 29 THEN spend ELSE 0 END)", "SUM(CASE WHEN jd >= JULIANDAY('2024-12-31') - 29 THEN conversions ELSE 0 END)", "SUM(CASE WHEN jd BETWEEN JULIANDAY('2024-12-31') - 59 AND JULIANDAY('2024-12-31') - 30 THEN spend ELSE 0 END)", "SUM(CASE WHEN jd BETWEEN JULIANDAY('2024-12-31') - 59 AND JULIANDAY('2024-12-31') - 30 THEN conversions ELSE 0 END)", "SUM(CASE WHEN jd >= JULIANDAY('2024-12-31') - 29 THEN spend ELSE 0 END)", "SUM(CASE WHEN jd BETWEEN JULIANDAY('2024-12-31') - 59 AND JULIANDAY('2024-12-31') - 30 THEN spend ELSE 0 END)", "SUM(CASE WHEN jd >= JULIANDAY('2024-12-31') - 29 THEN conversions ELSE 0 END)", "SUM(CASE WHEN jd BETWEEN JULIANDAY('2024-12-31') - 59 AND JULIANDAY('2024-12-31') - 30 THEN conversions ELSE 0 END)"] | 61 | 23.91 |
| [S65/Q61](#s65) | success | ["google_ads__campaign_report", "google_ads__customer_acquisition_analysis"] | 2 / {'INNER': 1} | ["campaign_id", "campaign_id"] | ["MIN(SUBSTRING(date_day, 1, 10))", "MAX(SUBSTRING(date_day, 1, 10))", "MAX(SUBSTRING(date_day, 1, 10))", "MIN(SUBSTRING(date_day, 1, 10))", "SUM(CASE WHEN jd >= JULIANDAY('2024-12-31') - 29 THEN conversions ELSE 0 END)", "SUM(CASE WHEN jd BETWEEN JULIANDAY('2024-12-31') - 59 AND JULIANDAY('2024-12-31') - 30 THEN conversions ELSE 0 END)"] | 29 | 21.878 |
| [S66/Q62](#s66) | success | ["google_ads__campaign_report", "google_ads__customer_acquisition_analysis"] | 2 / {'INNER': 1} | ["campaign_id", "campaign_id"] | ["MIN(SUBSTRING(date_day, 1, 10))", "MAX(SUBSTRING(date_day, 1, 10))", "MAX(SUBSTRING(date_day, 1, 10))", "MIN(SUBSTRING(date_day, 1, 10))", "SUM(CASE WHEN jd >= JULIANDAY('2024-12-31') - 29 THEN spend ELSE 0 END)", "SUM(CASE WHEN jd BETWEEN JULIANDAY('2024-12-31') - 59 AND JULIANDAY('2024-12-31') - 30 THEN spend ELSE 0 END)", "SUM(CASE WHEN jd >= JULIANDAY('2024-12-31') - 29 THEN conversions * ltv_cac_ratio ELSE 0 END)", "SUM(CASE WHEN jd BETWEEN JULIANDAY('2024-12-31') - 59 AND JULIANDAY('2024-12-31') - 30 THEN conversions * ltv_cac_ratio ELSE 0 END)", "SUM(CASE WHEN jd >= JULIANDAY('2024-12-31') - 29 THEN conversions ELSE 0 END)", "SUM(CASE WHEN jd BETWEEN JULIANDAY('2024-12-31') - 59 AND JULIANDAY('2024-12-31') - 30 THEN conversions ELSE 0 END)", "SUM(CASE WHEN jd >= JULIANDAY('2024-12-31') - 29 THEN conversions ELSE 0 END)", "SUM(CASE WHEN jd BETWEEN JULIANDAY('2024-12-31') - 59 AND JULIANDAY('2024-12-31') - 30 THEN conversions ELSE 0 END)", "SUM(CASE WHEN jd >= JULIANDAY('2024-12-31') - 29 THEN conversions ELSE 0 END)", "SUM(CASE WHEN jd BETWEEN JULIANDAY('2024-12-31') - 59 AND JULIANDAY('2024-12-31') - 30 THEN conversions ELSE 0 END)"] | 29 | 25.318 |
| [S67/Q63](#s67) | success | ["google_ads__campaign_report", "google_ads__customer_acquisition_analysis"] | 2 / {'INNER': 1} | ["campaign_id", "campaign_id"] | ["MIN(SUBSTRING(date_day, 1, 10))", "MAX(SUBSTRING(date_day, 1, 10))", "MAX(SUBSTRING(date_day, 1, 10))", "MIN(SUBSTRING(date_day, 1, 10))", "SUM(CASE WHEN jd >= JULIANDAY('2024-12-31') - 29 THEN spend ELSE 0 END)", "SUM(CASE WHEN jd >= JULIANDAY('2024-12-31') - 29 THEN conversions ELSE 0 END)", "SUM(CASE WHEN jd BETWEEN JULIANDAY('2024-12-31') - 59 AND JULIANDAY('2024-12-31') - 30 THEN spend ELSE 0 END)", "SUM(CASE WHEN jd BETWEEN JULIANDAY('2024-12-31') - 59 AND JULIANDAY('2024-12-31') - 30 THEN conversions ELSE 0 END)", "SUM(CASE WHEN jd >= JULIANDAY('2024-12-31') - 29 THEN conversions * ltv_cac_ratio ELSE 0 END)", "SUM(CASE WHEN jd BETWEEN JULIANDAY('2024-12-31') - 59 AND JULIANDAY('2024-12-31') - 30 THEN conversions * ltv_cac_ratio ELSE 0 END)"] | 29 | 25.467 |
| [S68/Q64](#s68) | failed | ["google_ads__campaign_report", "google_ads__customer_acquisition_analysis"] | 2 / {'INNER': 1} | ["campaign_id", "campaign_id"] | ["MAX(SUBSTRING(date_day, 1, 10))", "MAX(SUBSTRING(date_day, 1, 10))", "MIN(SUBSTRING(date_day, 1, 10))", "SUM(CASE WHEN jd >= ref_jd - 29 THEN spend ELSE 0 END)", "SUM(CASE WHEN jd >= ref_jd - 29 THEN conversions ELSE 0 END)", "SUM(CASE WHEN jd BETWEEN ref_jd - 59 AND ref_jd - 30 THEN spend ELSE 0 END)", "SUM(CASE WHEN jd BETWEEN ref_jd - 59 AND ref_jd - 30 THEN conversions ELSE 0 END)", "SUM(CASE WHEN jd >= ref_jd - 29 THEN conversions * ltv_cac_ratio ELSE 0 END)", "SUM(CASE WHEN jd BETWEEN ref_jd - 59 AND ref_jd - 30 THEN conversions * ltv_cac_ratio ELSE 0 END)"] | unknown | 未取得；调用总时长 0.436 ms |
| [S69/Q65](#s69) | success | ["google_ads__campaign_report", "google_ads__customer_acquisition_analysis"] | 2 / {'INNER': 1} | ["campaign_id", "campaign_id"] | ["MIN(SUBSTRING(date_day, 1, 10))", "MAX(SUBSTRING(date_day, 1, 10))", "MAX(SUBSTRING(date_day, 1, 10))", "MIN(SUBSTRING(date_day, 1, 10))", "SUM(CASE WHEN jd >= ref_jd - 29 THEN spend ELSE 0 END)", "SUM(CASE WHEN jd >= ref_jd - 29 THEN conversions ELSE 0 END)", "SUM(CASE WHEN jd BETWEEN ref_jd - 59 AND ref_jd - 30 THEN spend ELSE 0 END)", "SUM(CASE WHEN jd BETWEEN ref_jd - 59 AND ref_jd - 30 THEN conversions ELSE 0 END)", "SUM(CASE WHEN jd >= ref_jd - 29 THEN conversions * ltv_cac_ratio ELSE 0 END)", "SUM(CASE WHEN jd BETWEEN ref_jd - 59 AND ref_jd - 30 THEN conversions * ltv_cac_ratio ELSE 0 END)"] | 33 | 27.36 |
| [S70/Q66](#s70) | success | ["google_ads__campaign_report"] | 0 / {} | ["campaign_id"] | ["MIN(SUBSTRING(date_day, 1, 10))", "MAX(SUBSTRING(date_day, 1, 10))", "MAX(SUBSTRING(date_day, 1, 10))", "MIN(SUBSTRING(date_day, 1, 10))"] | 4 | 2.773 |
| [S71/Q67](#s71) | success | ["google_ads__campaign_report", "google_ads__customer_acquisition_analysis"] | 2 / {'INNER': 1} | ["campaign_id"] | ["MIN(SUBSTRING(date_day, 1, 10))", "MAX(SUBSTRING(date_day, 1, 10))", "MAX(SUBSTRING(date_day, 1, 10))", "MIN(SUBSTRING(date_day, 1, 10))"] | 2632 | 241.671 |
| [S72/Q68](#s72) | success | ["google_ads__campaign_report", "google_ads__customer_acquisition_analysis"] | 2 / {'INNER': 1} | ["campaign_id", "campaign_id"] | ["MIN(SUBSTRING(date_day, 1, 10))", "MAX(SUBSTRING(date_day, 1, 10))", "MAX(SUBSTRING(date_day, 1, 10))", "MIN(SUBSTRING(date_day, 1, 10))", "SUM(CASE WHEN jd >= ref_jd - 29 THEN spend ELSE 0 END)", "SUM(CASE WHEN jd >= ref_jd - 29 THEN conversions ELSE 0 END)", "SUM(CASE WHEN jd BETWEEN ref_jd - 59 AND ref_jd - 30 THEN spend ELSE 0 END)", "SUM(CASE WHEN jd BETWEEN ref_jd - 59 AND ref_jd - 30 THEN conversions ELSE 0 END)", "SUM(CASE WHEN jd >= ref_jd - 29 THEN conversions * ltv_cac_ratio ELSE 0 END)", "SUM(CASE WHEN jd BETWEEN ref_jd - 59 AND ref_jd - 30 THEN conversions * ltv_cac_ratio ELSE 0 END)", "MAX(CASE WHEN jd >= ref_jd - 29 THEN acquisition_sophistication_score ELSE 0 END)", "MAX(CASE WHEN jd >= ref_jd - 29 THEN cac_efficiency_percentile ELSE 0 END)", "MAX(CASE WHEN jd >= ref_jd - 29 THEN channel_diversity_count ELSE 0 END)", "MAX(CASE WHEN jd >= ref_jd - 29 THEN retention_risk ELSE 0 END)", "MAX(CASE WHEN jd >= ref_jd - 29 THEN scale_opportunity ELSE 0 END)", "MAX(CASE WHEN jd >= ref_jd - 29 THEN high_cac_alert ELSE 0 END)", "MAX(CASE WHEN jd >= ref_jd - 29 THEN negative_roi_alert ELSE 0 END)"] | 33 | 34.848 |
| [S73/Q69](#s73) | success | ["google_ads__customer_acquisition_analysis"] | 0 / {} | ["campaign_lifecycle_stage", "customer_maturity_stage", "account_maturity_stage", "strategic_customer_segment"] | ["COUNT(*)"] | 30 | 13.385 |
| [S74/Q70](#s74) | success | ["google_ads__customer_acquisition_analysis"] | 0 / {} | ["account_id", "advertising_channel_type", "advertising_channel_subtype", "campaign_lifecycle_stage", "customer_maturity_stage", "account_maturity_stage", "strategic_customer_segment"] | ["COUNT(*)", "SUM(retention_risk)", "SUM(scale_opportunity)", "SUM(high_cac_alert)", "SUM(negative_roi_alert)", "AVG(customer_acquisition_cost)", "AVG(ltv_cac_ratio)", "AVG(acquisition_sophistication_score)", "AVG(cac_efficiency_percentile)", "AVG(channel_diversity_count)"] | 96 | 5.255 |


## 元数据和设置

| SQL | 类别 | 状态 | 内容 |
| --- | --- | --- | --- |
| S1 | connection_setup | success | PRAGMA query_only=ON |
| S2 | metadata | success | SELECT name,sql FROM sqlite_master WHERE type='table' ORDER BY name |
| S6 | metadata | success | PRAGMA table_info(google_ads__customer_acquisition_analysis) |
| S7 | metadata | success | PRAGMA table_info(google_ads__campaign_report) |


## Python 与执行位置

人工源码审查：**database_first_violation**。Python 对广告生命周期、渠道、客户阶段和月份执行计数、均值、份额与风险比较，复现了 SQL 可支持的聚合与条件计算。用于图表的结果准备也应优先在数据库完成。 [证据](../reviews/dacomp-057.json)。

P1：Need to compute multi-dimensional decay risk analysis, build risk model, analyze segment patterns, and create visualizations - this requires statistical computation, matrix operations, and plotting beyond SQL capabilities.

[源码](../../../runs/dsv4flash-db-first-full-01/dacomp-057/attempt-01/python/P1.py)；[输出](../../../runs/dsv4flash-db-first-full-01/dacomp-057/attempt-01/python/P1.stdout)；[错误](../../../runs/dsv4flash-db-first-full-01/dacomp-057/attempt-01/python/P1.stderr)。检出需人工核验的 SQL 可实现操作：groupby(, sort_values(；不能仅凭理由判为合规。

P2：Results files are JSON arrays (not JSONL objects), need to load with json.load and assign column names to build dataframes for analysis.

[源码](../../../runs/dsv4flash-db-first-full-01/dacomp-057/attempt-01/python/P2.py)；[输出](../../../runs/dsv4flash-db-first-full-01/dacomp-057/attempt-01/python/P2.stdout)；[错误](../../../runs/dsv4flash-db-first-full-01/dacomp-057/attempt-01/python/P2.stderr)。自动源码筛查未检出预设迁出信号；这不是全面语义合规证明。

P3：Results files are JSONL where each line is a JSON array; load line by line and construct DataFrames with known column names.

[源码](../../../runs/dsv4flash-db-first-full-01/dacomp-057/attempt-01/python/P3.py)；[输出](../../../runs/dsv4flash-db-first-full-01/dacomp-057/attempt-01/python/P3.stdout)；[错误](../../../runs/dsv4flash-db-first-full-01/dacomp-057/attempt-01/python/P3.stderr)。自动源码筛查未检出预设迁出信号；这不是全面语义合规证明。

P4：Comprehensive multi-dimensional analysis: computing decay metrics, building risk model, analyzing segment patterns, and creating visualization plots. This requires statistical operations and plotting beyond SQL capabilities.

[源码](../../../runs/dsv4flash-db-first-full-01/dacomp-057/attempt-01/python/P4.py)；[输出](../../../runs/dsv4flash-db-first-full-01/dacomp-057/attempt-01/python/P4.stdout)；[错误](../../../runs/dsv4flash-db-first-full-01/dacomp-057/attempt-01/python/P4.stderr)。检出需人工核验的 SQL 可实现操作：groupby(, sort_values(；不能仅凭理由判为合规。

P5：Deep-dive into decayed zones' multi-dimensional profiles (lifecycle, maturity, segment, saturation proxies) and build budget reallocation model - statistical aggregation and modeling beyond SQL capabilities.

[源码](../../../runs/dsv4flash-db-first-full-01/dacomp-057/attempt-01/python/P5.py)；[输出](../../../runs/dsv4flash-db-first-full-01/dacomp-057/attempt-01/python/P5.stdout)；[错误](../../../runs/dsv4flash-db-first-full-01/dacomp-057/attempt-01/python/P5.stderr)。检出需人工核验的 SQL 可实现操作：groupby(, sort_values(；不能仅凭理由判为合规。

P6：Generate monthly CAC/LTV-CAC trend for decayed vs healthy zones and compute correlation of risk model factors with the decay flag - statistical analysis and time-series visualization beyond SQL.

[源码](../../../runs/dsv4flash-db-first-full-01/dacomp-057/attempt-01/python/P6.py)；[输出](../../../runs/dsv4flash-db-first-full-01/dacomp-057/attempt-01/python/P6.stdout)；[错误](../../../runs/dsv4flash-db-first-full-01/dacomp-057/attempt-01/python/P6.stderr)。检出需人工核验的 SQL 可实现操作：groupby(；不能仅凭理由判为合规。

P7：Generate monthly CAC/LTV-CAC trend for decayed vs healthy zones and correlation of risk factors with decay flag - time-series visualization and correlation analysis beyond SQL.

[源码](../../../runs/dsv4flash-db-first-full-01/dacomp-057/attempt-01/python/P7.py)；[输出](../../../runs/dsv4flash-db-first-full-01/dacomp-057/attempt-01/python/P7.stdout)；[错误](../../../runs/dsv4flash-db-first-full-01/dacomp-057/attempt-01/python/P7.stderr)。检出需人工核验的 SQL 可实现操作：groupby(；不能仅凭理由判为合规。

## 优化机会

已验证候选。筛选限于精确 SQL、相同自包含 CTE、相同单表完整过滤、可分解单表聚合；未覆盖任意 Join 等价和一般谓词蕴含。全部候选都是 offline，未测在线预测。

| 候选 | 类型 | 已有结果 | 覆盖 SQL | 后续次数 | 中间行数 | 验证 | 成本 |
| --- | --- | --- | --- | --- | --- | --- | --- |
| C1 | common subexpression | False | ["S53", "S54", "S59", "S60", "S61", "S64", "S65", "S66", "S67", "S69", "S71", "S72"] | 11 | 77 | rejected_result_mismatch | Not benchmarked; correctness alone does not establish net speedup. |
| C2 | aggregate MV | False | ["S3", "S36", "S37", "S55", "S73"] | 4 | 7270 | verified | Not benchmarked; correctness alone does not establish net speedup. |
| C3 | common filtered view | False | ["S41", "S42"] | 1 | 251 | verified | Not benchmarked; correctness alone does not establish net speedup. |


已验证覆盖（含触发查询、候选并集去重）：7/67 条成功数据 SQL。正确性仅针对当前数据库快照；未测性能的候选不能声称已加速。

[完整 build/rewrite 与比较证据](dacomp-057.analysis.json)。

### C2：aggregate MV

Union of grouping keys; decomposable aggregate states; AVG uses SUM and non-NULL COUNT.

原查询 [S3](#s3), [S36](#s36), [S37](#s37), [S55](#s55), [S73](#s73) → 新增共享状态 C2 → 后续 4 次可复用。该构建点为事后假设，不代表 Agent 当时预知后续。

构建定义：

```sql
SELECT account_id AS __g0, SUBSTRING(date_day, 1, 7) AS __g1, advertising_channel_type AS __g2, advertising_channel_subtype AS __g3, campaign_lifecycle_stage AS __g4, customer_maturity_stage AS __g5, account_maturity_stage AS __g6, strategic_customer_segment AS __g7, COUNT(*) AS __a0, MIN(SUBSTRING(date_day, 1, 10)) AS __a1, MAX(SUBSTRING(date_day, 1, 10)) AS __a2 FROM "google_ads__customer_acquisition_analysis"  GROUP BY account_id, SUBSTRING(date_day, 1, 7), advertising_channel_type, advertising_channel_subtype, campaign_lifecycle_stage, customer_maturity_stage, account_maturity_stage, strategic_customer_segment
```

受益查询 S3 的改写示例：

```sql
SELECT SUM(__a0) AS n_rows FROM temp.reuse_candidate
```

| 原 SQL | 列名一致 | 结果一致 | 比较方法 |
| --- | --- | --- | --- |
| S3 | True | True | exact_multiset |
| S36 | True | True | ordered_numeric_tolerance |
| S37 | True | True | ordered_numeric_tolerance |
| S55 | True | True | ordered_numeric_tolerance |
| S73 | True | True | ordered_numeric_tolerance |


验证状态：verified；成本结论：Not benchmarked; correctness alone does not establish net speedup.

### C3：common filtered view

Same single source and complete filter; original filter retained.

原查询 [S41](#s41), [S42](#s42) → 新增共享状态 C3 → 后续 1 次可复用。该构建点为事后假设，不代表 Agent 当时预知后续。

构建定义：

```sql
SELECT * FROM "google_ads__customer_acquisition_analysis" WHERE SUBSTRING(date_day, 1, 10) BETWEEN '2024-11-02' AND '2024-12-31'
```

受益查询 S41 的改写示例：

```sql
SELECT account_id, advertising_channel_type, COUNT(DISTINCT SUBSTRING(date_day, 1, 10)) AS n_days FROM temp.reuse_candidate AS google_ads__customer_acquisition_analysis WHERE SUBSTRING(date_day, 1, 10) BETWEEN '2024-11-02' AND '2024-12-31' GROUP BY account_id, advertising_channel_type ORDER BY account_id, advertising_channel_type
```

| 原 SQL | 列名一致 | 结果一致 | 比较方法 |
| --- | --- | --- | --- |
| S41 | True | True | ordered_numeric_tolerance |
| S42 | True | True | exact_multiset |


验证状态：verified；成本结论：Not benchmarked; correctness alone does not establish net speedup.

### C1：common subexpression

Identical self-contained CTE body across queries.

原查询 [S53](#s53), [S54](#s54), [S59](#s59), [S60](#s60), [S61](#s61), [S64](#s64), [S65](#s65), [S66](#s66), [S67](#s67), [S69](#s69), [S71](#s71), [S72](#s72) → 新增共享状态 C1 → 后续 11 次可复用。该构建点为事后假设，不代表 Agent 当时预知后续。

构建定义：

```sql
SELECT campaign_id, campaign_name, account_id, account_name, advertising_channel_type, advertising_channel_subtype, MIN(SUBSTRING(date_day, 1, 10)) AS first_date, MAX(SUBSTRING(date_day, 1, 10)) AS last_date, CAST(JULIANDAY(MAX(SUBSTRING(date_day, 1, 10))) - JULIANDAY(MIN(SUBSTRING(date_day, 1, 10))) AS INTEGER) AS days_running FROM google_ads__campaign_report GROUP BY campaign_id HAVING days_running > 120
```

受益查询 S53 的改写示例：

```sql
WITH camp AS (SELECT * FROM temp.reuse_candidate) SELECT c.campaign_id, c.account_id, c.advertising_channel_type, c.advertising_channel_subtype, COUNT(a.rowid) AS matched_rows FROM camp AS c LEFT JOIN google_ads__customer_acquisition_analysis AS a ON a.account_id = c.account_id AND a.advertising_channel_type = c.advertising_channel_type AND COALESCE(a.advertising_channel_subtype, '') = COALESCE(c.advertising_channel_subtype, '') AND SUBSTRING(a.date_day, 1, 10) BETWEEN c.first_date AND c.last_date GROUP BY c.campaign_id ORDER BY matched_rows DESC
```

| 原 SQL | 列名一致 | 结果一致 | 比较方法 |
| --- | --- | --- | --- |
| S53 | True | True | ordered_numeric_tolerance |
| S54 | True | True | ordered_numeric_tolerance |
| S59 | True | True | ordered_numeric_tolerance |
| S60 | True | True | ordered_numeric_tolerance |
| S61 | True | True | exact_multiset |
| S64 | True | True | ordered_numeric_tolerance |
| S65 | True | True | ordered_numeric_tolerance |
| S66 | True | True | ordered_numeric_tolerance |
| S67 | True | True | ordered_numeric_tolerance |
| S69 | True | True | ordered_numeric_tolerance |
| S71 | True | False | ordered_numeric_tolerance |
| S72 | True | False | exact_multiset |


验证状态：rejected_result_mismatch；成本结论：Not benchmarked; correctness alone does not establish net speedup.

结果依赖：自动记录 SQL→Python 的接口父调用，以及源码中引用归档文件的消费者；字面值相同不认定因果。模型方向选择需要人工读取消息，尚未做全面因果标注。

[原始报告](../../../runs/dsv4flash-db-first-full-01/dacomp-057/attempt-01/answer.md)；[统一消息](../../../runs/dsv4flash-db-first-full-01/dacomp-057/attempt-01/messages.jsonl)；[原始 OpenCode 事件](../../../runs/dsv4flash-db-first-full-01/dacomp-057/attempt-01/opencode.jsonl)；[SQL 引擎日志](../../../runs/dsv4flash-db-first-full-01/dacomp-057/attempt-01/sql_journal.jsonl)。

[可读报告（本地图片链接规范化）](../answers/dacomp-057.md)。原始回答保留，分析结论未改写。

## S1

类别 `connection_setup`；来源 `connection`；调用 `e507b876610c42d1a775567d6a20e1b5`；状态 `success`。

```sql
PRAGMA query_only=ON
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-057/attempt-01/sql/S1.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-057/attempt-01/sql/S1.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-057/attempt-01/results/S1.rows.jsonl)；完整：True；SHA256：`e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`。

## S2

类别 `metadata`；来源 `list_db`；调用 `e507b876610c42d1a775567d6a20e1b5`；状态 `success`。

```sql
SELECT name,sql FROM sqlite_master WHERE type='table' ORDER BY name
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-057/attempt-01/sql/S2.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-057/attempt-01/sql/S2.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-057/attempt-01/results/S2.rows.jsonl)；完整：True；SHA256：`a28256f37959f15a088f55940a7d883ac987740d5c473fcfb4e4e32e638681fb`。

## S3

类别 `data`；来源 `query_db`；调用 `e142413895b34350a91a8f7537de6e9a`；状态 `success`。

```sql
SELECT COUNT(*) AS n_rows FROM google_ads__customer_acquisition_analysis
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-057/attempt-01/sql/S3.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-057/attempt-01/sql/S3.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-057/attempt-01/results/S3.rows.jsonl)；完整：True；SHA256：`aa6d6ae6ca30e188ae245d117135dedb1eec9e98797ddc3dad4f9cec745e2f6d`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "google_ads__customer_acquisition_analysis", "kind": "base", "block": null, "base_tables": ["google_ads__customer_acquisition_analysis"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |


## S4

类别 `data`；来源 `query_db`；调用 `415e5ffb559f4e949402660d7a4cd3f9`；状态 `failed`。

```sql
SELECT MIN(date_day) AS min_date, MAX(date_day) AS max_date, COUNT(DISTINCT campaign_id) AS n_campaigns, COUNT(DISTINCT account_id) AS n_accounts FROM google_ads__customer_acquisition_analysis
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-057/attempt-01/sql/S4.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-057/attempt-01/sql/S4.parameters.json)。

错误：`OperationalError('no such column: campaign_id')`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "google_ads__customer_acquisition_analysis", "kind": "base", "block": null, "base_tables": ["google_ads__customer_acquisition_analysis"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | MIN(date_day) | [{"table": "google_ads__customer_acquisition_analysis", "column": "date_day"}] | [] | False |
| B1 | MAX(date_day) | [{"table": "google_ads__customer_acquisition_analysis", "column": "date_day"}] | [] | False |
| B1 | COUNT(DISTINCT campaign_id) | [{"unknown": "campaign_id"}] | [] | False |
| B1 | COUNT(DISTINCT account_id) | [{"table": "google_ads__customer_acquisition_analysis", "column": "account_id"}] | [] | False |


未解析列血缘：[{"block": "B1", "column": "campaign_id", "reason": "ambiguous_or_missing_source"}, {"block": "B1", "column": "campaign_id", "reason": "ambiguous_or_missing_source"}]

## S5

类别 `data`；来源 `query_db`；调用 `e0073898a617484abb0b9b22058184ae`；状态 `success`。

```sql
SELECT MIN(date_day) AS min_date, MAX(date_day) AS max_date, COUNT(DISTINCT campaign_id) AS n_campaigns, COUNT(DISTINCT account_id) AS n_accounts FROM google_ads__campaign_report
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-057/attempt-01/sql/S5.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-057/attempt-01/sql/S5.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-057/attempt-01/results/S5.rows.jsonl)；完整：True；SHA256：`4e4912dd76b03a8c566b8131bcec568abd38e4841f10499cdbd807387243b402`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "google_ads__campaign_report", "kind": "base", "block": null, "base_tables": ["google_ads__campaign_report"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | MIN(date_day) | [{"table": "google_ads__campaign_report", "column": "date_day"}] | [] | False |
| B1 | MAX(date_day) | [{"table": "google_ads__campaign_report", "column": "date_day"}] | [] | False |
| B1 | COUNT(DISTINCT campaign_id) | [{"table": "google_ads__campaign_report", "column": "campaign_id"}] | [] | False |
| B1 | COUNT(DISTINCT account_id) | [{"table": "google_ads__campaign_report", "column": "account_id"}] | [] | False |


## S6

类别 `metadata`；来源 `query_db`；调用 `0648d6d943a7441285c03a832a7fcae3`；状态 `success`。

```sql
PRAGMA table_info(google_ads__customer_acquisition_analysis)
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-057/attempt-01/sql/S6.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-057/attempt-01/sql/S6.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-057/attempt-01/results/S6.rows.jsonl)；完整：True；SHA256：`b6492b44302eb323de133215dfdc7db3dfc384e13075b29b52285a002c80141b`。

## S7

类别 `metadata`；来源 `query_db`；调用 `df99bcbb5ab44e36a9320609d0eb546d`；状态 `success`。

```sql
PRAGMA table_info(google_ads__campaign_report)
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-057/attempt-01/sql/S7.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-057/attempt-01/sql/S7.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-057/attempt-01/results/S7.rows.jsonl)；完整：True；SHA256：`7e22f8ac52387dd901e69cba88d4b148677d79b1fad00eafa9fedf7dfb98688b`。

## S8

类别 `data`；来源 `query_db`；调用 `22e908ce4f6c4e89b56e02b5c977cdb5`；状态 `success`。

```sql
SELECT DISTINCT campaign_lifecycle_stage FROM google_ads__customer_acquisition_analysis
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-057/attempt-01/sql/S8.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-057/attempt-01/sql/S8.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-057/attempt-01/results/S8.rows.jsonl)；完整：True；SHA256：`b9dea44265f66052cae3175145a135026a11d833fd7e3d3266f292e77fd7c10f`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "google_ads__customer_acquisition_analysis", "kind": "base", "block": null, "base_tables": ["google_ads__customer_acquisition_analysis"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |


## S9

类别 `data`；来源 `query_db`；调用 `8c4d777df4114588aaa91f223f696d3d`；状态 `success`。

```sql
SELECT DISTINCT advertising_channel_type FROM google_ads__customer_acquisition_analysis
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-057/attempt-01/sql/S9.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-057/attempt-01/sql/S9.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-057/attempt-01/results/S9.rows.jsonl)；完整：True；SHA256：`097046416494afac20dece5362ed9bf139cf94f548dc1806a2286651d692d5f2`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "google_ads__customer_acquisition_analysis", "kind": "base", "block": null, "base_tables": ["google_ads__customer_acquisition_analysis"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |


## S10

类别 `data`；来源 `query_db`；调用 `3ed5e4159fff4c50a374d2f1cb65d46f`；状态 `success`。

```sql
SELECT DISTINCT customer_maturity_stage FROM google_ads__customer_acquisition_analysis
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-057/attempt-01/sql/S10.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-057/attempt-01/sql/S10.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-057/attempt-01/results/S10.rows.jsonl)；完整：True；SHA256：`8e1372225b04b4899d7b42392311aa593b3453351142236b4b3103f814099c77`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "google_ads__customer_acquisition_analysis", "kind": "base", "block": null, "base_tables": ["google_ads__customer_acquisition_analysis"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |


## S11

类别 `data`；来源 `query_db`；调用 `b3e3f27805184b49ad3c8c3c04cb5dc6`；状态 `success`。

```sql
SELECT DISTINCT account_maturity_stage FROM google_ads__customer_acquisition_analysis
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-057/attempt-01/sql/S11.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-057/attempt-01/sql/S11.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-057/attempt-01/results/S11.rows.jsonl)；完整：True；SHA256：`afd9acee26dc35d2e86d2d858432aacdd0127ce707bc385652de78997d667b98`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "google_ads__customer_acquisition_analysis", "kind": "base", "block": null, "base_tables": ["google_ads__customer_acquisition_analysis"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |


## S12

类别 `data`；来源 `query_db`；调用 `6bd7cba6a186482eb8da4cdc81938b1b`；状态 `success`。

```sql
SELECT DISTINCT strategic_customer_segment FROM google_ads__customer_acquisition_analysis
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-057/attempt-01/sql/S12.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-057/attempt-01/sql/S12.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-057/attempt-01/results/S12.rows.jsonl)；完整：True；SHA256：`d60bcb142ee3d6c4f1725e68444a33adda928cb6beca30ac687362019a53eec8`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "google_ads__customer_acquisition_analysis", "kind": "base", "block": null, "base_tables": ["google_ads__customer_acquisition_analysis"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |


## S13

类别 `data`；来源 `query_db`；调用 `1167a14931454273b3d5906e82cc9262`；状态 `success`。

```sql
SELECT DISTINCT acquisition_efficiency_tier FROM google_ads__customer_acquisition_analysis
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-057/attempt-01/sql/S13.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-057/attempt-01/sql/S13.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-057/attempt-01/results/S13.rows.jsonl)；完整：True；SHA256：`1d4163f1dcd4517c94629ddbe06f7184b780cdf3f8fbe5798f9107c9195c13be`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "google_ads__customer_acquisition_analysis", "kind": "base", "block": null, "base_tables": ["google_ads__customer_acquisition_analysis"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |


## S14

类别 `data`；来源 `query_db`；调用 `6a15c0588c39427ba6388fcd1ea741ca`；状态 `success`。

```sql
SELECT DISTINCT cac_performance_tier FROM google_ads__customer_acquisition_analysis
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-057/attempt-01/sql/S14.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-057/attempt-01/sql/S14.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-057/attempt-01/results/S14.rows.jsonl)；完整：True；SHA256：`8e8639740a53224e7aa2c3c62f34a6753968e4cac4ef3286b84eb4389305d894`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "google_ads__customer_acquisition_analysis", "kind": "base", "block": null, "base_tables": ["google_ads__customer_acquisition_analysis"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |


## S15

类别 `data`；来源 `query_db`；调用 `bafed1bb22664edd9d2625c8d20470cd`；状态 `success`。

```sql
SELECT DISTINCT acquisition_recommendation FROM google_ads__customer_acquisition_analysis
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-057/attempt-01/sql/S15.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-057/attempt-01/sql/S15.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-057/attempt-01/results/S15.rows.jsonl)；完整：True；SHA256：`e8b727126fe23b67edc78ce820811568aee61bde2a5a636b32f7eef83402bc98`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "google_ads__customer_acquisition_analysis", "kind": "base", "block": null, "base_tables": ["google_ads__customer_acquisition_analysis"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |


## S16

类别 `data`；来源 `query_db`；调用 `ecabcf8c518a40578f9692b717090ad3`；状态 `success`。

```sql
SELECT DISTINCT account_name, account_id FROM google_ads__customer_acquisition_analysis
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-057/attempt-01/sql/S16.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-057/attempt-01/sql/S16.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-057/attempt-01/results/S16.rows.jsonl)；完整：True；SHA256：`3b1cd3e8ba2801438eaf18484a7172abcad92123f37df8f77c531e037563e8e0`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "google_ads__customer_acquisition_analysis", "kind": "base", "block": null, "base_tables": ["google_ads__customer_acquisition_analysis"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |


## S17

类别 `data`；来源 `query_db`；调用 `155e942da6e74ba48a31735d059fc674`；状态 `success`。

```sql
SELECT DISTINCT campaign_name, campaign_id, account_id, account_name FROM google_ads__campaign_report LIMIT 20
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-057/attempt-01/sql/S17.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-057/attempt-01/sql/S17.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-057/attempt-01/results/S17.rows.jsonl)；完整：True；SHA256：`bea4c8813b9dc466664590501714b5928f70f4c24ab53f96930e94d4a8a351c0`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "google_ads__campaign_report", "kind": "base", "block": null, "base_tables": ["google_ads__campaign_report"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |


## S18

类别 `data`；来源 `query_db`；调用 `ba7968042be3409e9d1af8cc8f35ce44`；状态 `success`。

```sql
SELECT MIN(date_day) AS min_date, MAX(date_day) AS max_date, COUNT(DISTINCT campaign_id) AS n_campaigns FROM google_ads__campaign_report
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-057/attempt-01/sql/S18.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-057/attempt-01/sql/S18.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-057/attempt-01/results/S18.rows.jsonl)；完整：True；SHA256：`1bdf85452c807a17a6e9fe74e508e5efe6fd271b54dc4f5234e9bc3cdb3b06b6`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "google_ads__campaign_report", "kind": "base", "block": null, "base_tables": ["google_ads__campaign_report"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | MIN(date_day) | [{"table": "google_ads__campaign_report", "column": "date_day"}] | [] | False |
| B1 | MAX(date_day) | [{"table": "google_ads__campaign_report", "column": "date_day"}] | [] | False |
| B1 | COUNT(DISTINCT campaign_id) | [{"table": "google_ads__campaign_report", "column": "campaign_id"}] | [] | False |


## S19

类别 `data`；来源 `query_db`；调用 `ca00db4f159044059a4a13a1141608a7`；状态 `success`。

```sql
SELECT DISTINCT status FROM google_ads__campaign_report
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-057/attempt-01/sql/S19.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-057/attempt-01/sql/S19.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-057/attempt-01/results/S19.rows.jsonl)；完整：True；SHA256：`b00276e5bf63921f409ef3c26f15335f416b7cd7621332ae3be65086a915f987`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "google_ads__campaign_report", "kind": "base", "block": null, "base_tables": ["google_ads__campaign_report"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |


## S20

类别 `data`；来源 `query_db`；调用 `734d01b4396c49f3bafacc949f0b747f`；状态 `success`。

```sql
SELECT DISTINCT advertising_channel_type FROM google_ads__campaign_report
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-057/attempt-01/sql/S20.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-057/attempt-01/sql/S20.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-057/attempt-01/results/S20.rows.jsonl)；完整：True；SHA256：`976c9d8700ad9594f456049d0d7f27e069cc274038f9f16f2a2fb72fef2d10ce`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "google_ads__campaign_report", "kind": "base", "block": null, "base_tables": ["google_ads__campaign_report"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |


## S21

类别 `data`；来源 `query_db`；调用 `26e19ea55c494e8f9265e99d43402e10`；状态 `success`。

```sql
SELECT COUNT(*) AS n_rows FROM google_ads__campaign_report
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-057/attempt-01/sql/S21.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-057/attempt-01/sql/S21.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-057/attempt-01/results/S21.rows.jsonl)；完整：True；SHA256：`9fecd09a446ab0bc3770a0c58323413d52e57f110cab7759fd1cdf6aa03f304f`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "google_ads__campaign_report", "kind": "base", "block": null, "base_tables": ["google_ads__campaign_report"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |


## S22

类别 `data`；来源 `query_db`；调用 `7349371dc8a442df9430745eea6ef6dc`；状态 `success`。

```sql
SELECT DISTINCT advertising_channel_subtype FROM google_ads__customer_acquisition_analysis
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-057/attempt-01/sql/S22.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-057/attempt-01/sql/S22.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-057/attempt-01/results/S22.rows.jsonl)；完整：True；SHA256：`6b998777983a2254bf55ab9b84f3aab37e9ecf83f1a7b0e324053f126363e9d6`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "google_ads__customer_acquisition_analysis", "kind": "base", "block": null, "base_tables": ["google_ads__customer_acquisition_analysis"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |


## S23

类别 `data`；来源 `query_db`；调用 `a2108b6d78104521837f82cb6b8bb2f1`；状态 `success`。

```sql
SELECT DISTINCT advertising_channel_subtype FROM google_ads__campaign_report
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-057/attempt-01/sql/S23.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-057/attempt-01/sql/S23.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-057/attempt-01/results/S23.rows.jsonl)；完整：True；SHA256：`0f7ac7f7e8075ad1eaa607f6373eac06bf4ff0375d4b8dab70dc1f1aeaeed25a`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "google_ads__campaign_report", "kind": "base", "block": null, "base_tables": ["google_ads__campaign_report"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |


## S24

类别 `data`；来源 `query_db`；调用 `ababad3ad8d241de8e804c6a08eb1ca1`；状态 `success`。

```sql
SELECT * FROM google_ads__customer_acquisition_analysis LIMIT 5
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-057/attempt-01/sql/S24.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-057/attempt-01/sql/S24.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-057/attempt-01/results/S24.rows.jsonl)；完整：True；SHA256：`45ed5531bad23aef25ad828ef98a0dc8ca052772cf6e2b62e7e2216804002277`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "google_ads__customer_acquisition_analysis", "kind": "base", "block": null, "base_tables": ["google_ads__customer_acquisition_analysis"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |


## S25

类别 `data`；来源 `query_db`；调用 `4bdff587626145b8b0592bd796af9b4c`；状态 `success`。

```sql
SELECT MIN(date_day) AS min_date, MAX(date_day) AS max_date, COUNT(DISTINCT account_id) AS n_accounts FROM google_ads__customer_acquisition_analysis
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-057/attempt-01/sql/S25.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-057/attempt-01/sql/S25.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-057/attempt-01/results/S25.rows.jsonl)；完整：True；SHA256：`80e498e2ca14658e626401ed54e1f3222b0eaf487c8ab05a5926b45ec075033e`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "google_ads__customer_acquisition_analysis", "kind": "base", "block": null, "base_tables": ["google_ads__customer_acquisition_analysis"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | MIN(date_day) | [{"table": "google_ads__customer_acquisition_analysis", "column": "date_day"}] | [] | False |
| B1 | MAX(date_day) | [{"table": "google_ads__customer_acquisition_analysis", "column": "date_day"}] | [] | False |
| B1 | COUNT(DISTINCT account_id) | [{"table": "google_ads__customer_acquisition_analysis", "column": "account_id"}] | [] | False |


## S26

类别 `data`；来源 `query_db`；调用 `7bdf61a8762f4c3ea33f8b3ea965acfd`；状态 `success`。

```sql
SELECT strftime('%Y-%m', date_day) AS ym, COUNT(*) AS n, COUNT(DISTINCT account_id) AS accts FROM google_ads__customer_acquisition_analysis GROUP BY ym ORDER BY ym
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-057/attempt-01/sql/S26.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-057/attempt-01/sql/S26.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-057/attempt-01/results/S26.rows.jsonl)；完整：True；SHA256：`f4592833338500d018fc561a927c3113b8ddd969ecb8ce5a36bfde9189765636`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "google_ads__customer_acquisition_analysis", "kind": "base", "block": null, "base_tables": ["google_ads__customer_acquisition_analysis"]}] | [] | ["STRFTIME('%Y-%m', date_day)"] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |
| B1 | COUNT(DISTINCT account_id) | [{"table": "google_ads__customer_acquisition_analysis", "column": "account_id"}] | [] | False |


## S27

类别 `data`；来源 `query_db`；调用 `441829f9df214846a31d1e7ade5a81f2`；状态 `success`。

```sql
SELECT date_day, typeof(date_day) FROM google_ads__customer_acquisition_analysis LIMIT 5
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-057/attempt-01/sql/S27.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-057/attempt-01/sql/S27.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-057/attempt-01/results/S27.rows.jsonl)；完整：True；SHA256：`2314595a5ede887047cc774e7a2349419664529eb261b90babd02a1423356859`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "google_ads__customer_acquisition_analysis", "kind": "base", "block": null, "base_tables": ["google_ads__customer_acquisition_analysis"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |


## S28

类别 `data`；来源 `query_db`；调用 `764eb510a4424974993c0d653e8334cb`；状态 `success`。

```sql
SELECT date_day, typeof(date_day) FROM google_ads__campaign_report LIMIT 5
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-057/attempt-01/sql/S28.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-057/attempt-01/sql/S28.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-057/attempt-01/results/S28.rows.jsonl)；完整：True；SHA256：`c53459e7524c31ee33bf6503a09d32b0add063b52f96b839d575d4e4c81a0809`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "google_ads__campaign_report", "kind": "base", "block": null, "base_tables": ["google_ads__campaign_report"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |


## S29

类别 `data`；来源 `query_db`；调用 `3ea1c9b17c9f4f31904f440e120d75f4`；状态 `success`。

```sql
SELECT account_id, date_day, advertising_channel_type, advertising_channel_subtype, customer_maturity_stage, campaign_lifecycle_stage, COUNT(*) AS cnt
FROM google_ads__customer_acquisition_analysis
GROUP BY account_id, date_day, advertising_channel_type, advertising_channel_subtype, customer_maturity_stage, campaign_lifecycle_stage
HAVING cnt > 1
LIMIT 10
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-057/attempt-01/sql/S29.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-057/attempt-01/sql/S29.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-057/attempt-01/results/S29.rows.jsonl)；完整：True；SHA256：`cd00a00fa0ae27285672718ef90cc5bf2daa499dbd16165ce4913595432294cf`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "google_ads__customer_acquisition_analysis", "kind": "base", "block": null, "base_tables": ["google_ads__customer_acquisition_analysis"]}] | [] | ["account_id", "date_day", "advertising_channel_type", "advertising_channel_subtype", "customer_maturity_stage", "campaign_lifecycle_stage"] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |


## S30

类别 `data`；来源 `query_db`；调用 `ed7be06506ae41fd989e612ccf7030c1`；状态 `success`。

```sql
SELECT account_id, date_day, advertising_channel_type, advertising_channel_subtype, COUNT(*) AS n_camps, COUNT(DISTINCT campaign_id) AS n_ids
FROM google_ads__campaign_report
GROUP BY account_id, date_day, advertising_channel_type, advertising_channel_subtype
HAVING n_camps > 1
LIMIT 10
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-057/attempt-01/sql/S30.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-057/attempt-01/sql/S30.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-057/attempt-01/results/S30.rows.jsonl)；完整：True；SHA256：`9747f592462a6df4938c293f123bdcf848bdd52c2ca27a2f6b2d207ab56f9143`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "google_ads__campaign_report", "kind": "base", "block": null, "base_tables": ["google_ads__campaign_report"]}] | [] | ["account_id", "date_day", "advertising_channel_type", "advertising_channel_subtype"] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |
| B1 | COUNT(DISTINCT campaign_id) | [{"table": "google_ads__campaign_report", "column": "campaign_id"}] | [] | False |


## S31

类别 `data`；来源 `query_db`；调用 `8beccb1142b64ba89db52fb87a604b57`；状态 `success`。

```sql
SELECT account_id, date_day, advertising_channel_type, advertising_channel_subtype, customer_maturity_stage, campaign_lifecycle_stage, strategic_customer_segment, acquisition_cohort, COUNT(*) AS cnt
FROM google_ads__customer_acquisition_analysis
GROUP BY account_id, date_day, advertising_channel_type, advertising_channel_subtype, customer_maturity_stage, campaign_lifecycle_stage, strategic_customer_segment, acquisition_cohort
HAVING cnt > 1
LIMIT 10
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-057/attempt-01/sql/S31.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-057/attempt-01/sql/S31.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-057/attempt-01/results/S31.rows.jsonl)；完整：True；SHA256：`8af5f343d737070a3c9c9b15a803e4c68ca0ce7028a3dad4670e5026b946d154`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "google_ads__customer_acquisition_analysis", "kind": "base", "block": null, "base_tables": ["google_ads__customer_acquisition_analysis"]}] | [] | ["account_id", "date_day", "advertising_channel_type", "advertising_channel_subtype", "customer_maturity_stage", "campaign_lifecycle_stage", "strategic_customer_segment", "acquisition_cohort"] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |


## S32

类别 `data`；来源 `query_db`；调用 `efdd43f6907d4da892c22e34ced8728e`；状态 `success`。

```sql
SELECT COUNT(*) AS total, COUNT(DISTINCT account_id || '|' || date_day || '|' || advertising_channel_type || '|' || advertising_channel_subtype) AS uniq_keys FROM google_ads__customer_acquisition_analysis
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-057/attempt-01/sql/S32.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-057/attempt-01/sql/S32.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-057/attempt-01/results/S32.rows.jsonl)；完整：True；SHA256：`ad8cf969eccffe0e472dacd22b1cfe45b3883af7ab81db9e175b9de784669972`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "google_ads__customer_acquisition_analysis", "kind": "base", "block": null, "base_tables": ["google_ads__customer_acquisition_analysis"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |
| B1 | COUNT(DISTINCT account_id \|\| '\|' \|\| date_day \|\| '\|' \|\| advertising_channel_type \|\| '\|' \|\| advertising_channel_subtype) | [{"table": "google_ads__customer_acquisition_analysis", "column": "advertising_channel_subtype"}, {"table": "google_ads__customer_acquisition_analysis", "column": "advertising_channel_type"}, {"table": "google_ads__customer_acquisition_analysis", "column": "date_day"}, {"table": "google_ads__customer_acquisition_analysis", "column": "account_id"}] | [] | False |


## S33

类别 `data`；来源 `query_db`；调用 `ee32b78e31324660916a8847356e8d10`；状态 `success`。

```sql
SELECT campaign_id, campaign_name, account_id, account_name, advertising_channel_type, advertising_channel_subtype,
       MIN(date_day) AS first_date, MAX(date_day) AS last_date,
       CAST(julianday(MAX(date_day)) - julianday(MIN(date_day)) AS INTEGER) AS days_running
FROM google_ads__campaign_report
GROUP BY campaign_id
ORDER BY days_running DESC
LIMIT 20
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-057/attempt-01/sql/S33.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-057/attempt-01/sql/S33.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-057/attempt-01/results/S33.rows.jsonl)；完整：True；SHA256：`ae537eb96e9ebde44601826f93151fefeb4936158c087cd025761d1acf792023`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "google_ads__campaign_report", "kind": "base", "block": null, "base_tables": ["google_ads__campaign_report"]}] | [] | ["campaign_id"] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | MIN(date_day) | [{"table": "google_ads__campaign_report", "column": "date_day"}] | [] | False |
| B1 | MAX(date_day) | [{"table": "google_ads__campaign_report", "column": "date_day"}] | [] | False |
| B1 | MAX(date_day) | [{"table": "google_ads__campaign_report", "column": "date_day"}] | [] | False |
| B1 | MIN(date_day) | [{"table": "google_ads__campaign_report", "column": "date_day"}] | [] | False |


## S34

类别 `data`；来源 `query_db`；调用 `a66497e28fb5487084dfcc7fcd95c96f`；状态 `success`。

```sql
SELECT campaign_id, campaign_name, account_id, account_name, advertising_channel_type, advertising_channel_subtype,
       MIN(substr(date_day,1,10)) AS first_date, MAX(substr(date_day,1,10)) AS last_date,
       CAST(julianday(MAX(substr(date_day,1,10))) - julianday(MIN(substr(date_day,1,10))) AS INTEGER) AS days_running
FROM google_ads__campaign_report
GROUP BY campaign_id
ORDER BY days_running DESC
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-057/attempt-01/sql/S34.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-057/attempt-01/sql/S34.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-057/attempt-01/results/S34.rows.jsonl)；完整：True；SHA256：`e7730fb4159681793f444028df005d48403ab81ef1d5bb3e561a54902ca4930f`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "google_ads__campaign_report", "kind": "base", "block": null, "base_tables": ["google_ads__campaign_report"]}] | [] | ["campaign_id"] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | MIN(SUBSTRING(date_day, 1, 10)) | [{"table": "google_ads__campaign_report", "column": "date_day"}] | [] | False |
| B1 | MAX(SUBSTRING(date_day, 1, 10)) | [{"table": "google_ads__campaign_report", "column": "date_day"}] | [] | False |
| B1 | MAX(SUBSTRING(date_day, 1, 10)) | [{"table": "google_ads__campaign_report", "column": "date_day"}] | [] | False |
| B1 | MIN(SUBSTRING(date_day, 1, 10)) | [{"table": "google_ads__campaign_report", "column": "date_day"}] | [] | False |


## S35

类别 `data`；来源 `query_db`；调用 `26381571dac4469993d996037698b96a`；状态 `success`。

```sql
SELECT campaign_id, campaign_name, account_id, account_name, advertising_channel_type, advertising_channel_subtype,
       MIN(substr(date_day,1,10)) AS first_date, MAX(substr(date_day,1,10)) AS last_date,
       CAST(julianday(MAX(substr(date_day,1,10))) - julianday(MIN(substr(date_day,1,10))) AS INTEGER) AS days_running,
       CAST(julianday('2024-12-31') - julianday(MAX(substr(date_day,1,10))) AS INTEGER) AS days_since_last_data
FROM google_ads__campaign_report
GROUP BY campaign_id
HAVING days_running > 120
ORDER BY days_running DESC
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-057/attempt-01/sql/S35.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-057/attempt-01/sql/S35.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-057/attempt-01/results/S35.rows.jsonl)；完整：True；SHA256：`dc3881f40051f824c53ce92f1381c0226068f7571a2861b58b0235cac94c95d2`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "google_ads__campaign_report", "kind": "base", "block": null, "base_tables": ["google_ads__campaign_report"]}] | [] | ["campaign_id"] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | MIN(SUBSTRING(date_day, 1, 10)) | [{"table": "google_ads__campaign_report", "column": "date_day"}] | [] | False |
| B1 | MAX(SUBSTRING(date_day, 1, 10)) | [{"table": "google_ads__campaign_report", "column": "date_day"}] | [] | False |
| B1 | MAX(SUBSTRING(date_day, 1, 10)) | [{"table": "google_ads__campaign_report", "column": "date_day"}] | [] | False |
| B1 | MIN(SUBSTRING(date_day, 1, 10)) | [{"table": "google_ads__campaign_report", "column": "date_day"}] | [] | False |
| B1 | MAX(SUBSTRING(date_day, 1, 10)) | [{"table": "google_ads__campaign_report", "column": "date_day"}] | [] | False |


## S36

类别 `data`；来源 `query_db`；调用 `936a32989589420aa37ccf57eeff7728`；状态 `success`。

```sql
SELECT account_id, MIN(substr(date_day,1,10)) AS min_date, MAX(substr(date_day,1,10)) AS max_date, COUNT(*) AS n
FROM google_ads__customer_acquisition_analysis
GROUP BY account_id
ORDER BY account_id
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-057/attempt-01/sql/S36.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-057/attempt-01/sql/S36.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-057/attempt-01/results/S36.rows.jsonl)；完整：True；SHA256：`a3639306865d3057f61412f78a2482fcd6bc47925a27de73d79b165bac5568f8`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "google_ads__customer_acquisition_analysis", "kind": "base", "block": null, "base_tables": ["google_ads__customer_acquisition_analysis"]}] | [] | ["account_id"] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | MIN(SUBSTRING(date_day, 1, 10)) | [{"table": "google_ads__customer_acquisition_analysis", "column": "date_day"}] | [] | False |
| B1 | MAX(SUBSTRING(date_day, 1, 10)) | [{"table": "google_ads__customer_acquisition_analysis", "column": "date_day"}] | [] | False |
| B1 | COUNT(*) | [] | [] | True |


## S37

类别 `data`；来源 `query_db`；调用 `faccdca6253f4d2a9403b9dd62f9043e`；状态 `success`。

```sql
SELECT substr(date_day,1,7) AS ym, COUNT(*) AS n FROM google_ads__customer_acquisition_analysis GROUP BY ym ORDER BY ym
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-057/attempt-01/sql/S37.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-057/attempt-01/sql/S37.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-057/attempt-01/results/S37.rows.jsonl)；完整：True；SHA256：`24347df7aee02b72600be2225af36e49a6afd29ee4fb0860b80c67583d78c679`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "google_ads__customer_acquisition_analysis", "kind": "base", "block": null, "base_tables": ["google_ads__customer_acquisition_analysis"]}] | [] | ["SUBSTRING(date_day, 1, 7)"] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |


## S38

类别 `data`；来源 `query_db`；调用 `429cf995d4514bf7982d54b885d248e5`；状态 `success`。

```sql
SELECT substr(date_day,1,10) AS d, COUNT(*) AS n FROM google_ads__customer_acquisition_analysis WHERE substr(date_day,1,10) >= '2024-11-01' GROUP BY d ORDER BY d LIMIT 70
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-057/attempt-01/sql/S38.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-057/attempt-01/sql/S38.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-057/attempt-01/results/S38.rows.jsonl)；完整：True；SHA256：`3580635d9314b3570cfa590916e9f61c6370456d5d04adbd05520d1a9e90a083`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "google_ads__customer_acquisition_analysis", "kind": "base", "block": null, "base_tables": ["google_ads__customer_acquisition_analysis"]}] | [] | ["SUBSTRING(date_day, 1, 10)"] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |


## S39

类别 `data`；来源 `query_db`；调用 `1ed504ef1e6345e08710ed6c1fd66bff`；状态 `success`。

```sql
SELECT substr(date_day,1,7) AS ym, COUNT(*) AS n FROM google_ads__customer_acquisition_analysis WHERE substr(date_day,1,7) >= '2023-01' GROUP BY ym ORDER BY ym
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-057/attempt-01/sql/S39.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-057/attempt-01/sql/S39.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-057/attempt-01/results/S39.rows.jsonl)；完整：True；SHA256：`52ddb1e8f47394ccdb78a6b09dd80a7c16e3ecec30fcb5409a5f8e437ea41a8d`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "google_ads__customer_acquisition_analysis", "kind": "base", "block": null, "base_tables": ["google_ads__customer_acquisition_analysis"]}] | [] | ["SUBSTRING(date_day, 1, 7)"] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |


## S40

类别 `data`；来源 `query_db`；调用 `37e7255e23724149a0d5b254fa48b2ff`；状态 `success`。

```sql
SELECT substr(date_day,1,7) AS ym, COUNT(*) AS n FROM google_ads__customer_acquisition_analysis WHERE substr(date_day,1,7) >= '2024-01' GROUP BY ym ORDER BY ym
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-057/attempt-01/sql/S40.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-057/attempt-01/sql/S40.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-057/attempt-01/results/S40.rows.jsonl)；完整：True；SHA256：`84e17ab2633c427604c452545dd08dce34c379fa7ede40f5d7a9ac6832950ac9`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "google_ads__customer_acquisition_analysis", "kind": "base", "block": null, "base_tables": ["google_ads__customer_acquisition_analysis"]}] | [] | ["SUBSTRING(date_day, 1, 7)"] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |


## S41

类别 `data`；来源 `query_db`；调用 `5d6ed2887326430eab352548b6307501`；状态 `success`。

```sql
SELECT account_id, advertising_channel_type, COUNT(DISTINCT substr(date_day,1,10)) AS n_days
FROM google_ads__customer_acquisition_analysis
WHERE substr(date_day,1,10) BETWEEN '2024-11-02' AND '2024-12-31'
GROUP BY account_id, advertising_channel_type
ORDER BY account_id, advertising_channel_type
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-057/attempt-01/sql/S41.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-057/attempt-01/sql/S41.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-057/attempt-01/results/S41.rows.jsonl)；完整：True；SHA256：`74047684e10b5b92f6d575b63a0e64a1dde90b46756ab8da4dd5b97c7edd11c3`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "google_ads__customer_acquisition_analysis", "kind": "base", "block": null, "base_tables": ["google_ads__customer_acquisition_analysis"]}] | [] | ["account_id", "advertising_channel_type"] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(DISTINCT SUBSTRING(date_day, 1, 10)) | [{"table": "google_ads__customer_acquisition_analysis", "column": "date_day"}] | [] | False |


## S42

类别 `data`；来源 `query_db`；调用 `f37747b93c574de8ade22ab7a38a5d2e`；状态 `success`。

```sql
SELECT COUNT(*) AS total_days, COUNT(DISTINCT account_id || '|' || substr(date_day,1,10)) AS acct_days
FROM google_ads__customer_acquisition_analysis
WHERE substr(date_day,1,10) BETWEEN '2024-11-02' AND '2024-12-31'
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-057/attempt-01/sql/S42.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-057/attempt-01/sql/S42.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-057/attempt-01/results/S42.rows.jsonl)；完整：True；SHA256：`51d232aedaeb37d6e9b503e96951798882a35096870e09bca44448da57c87047`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "google_ads__customer_acquisition_analysis", "kind": "base", "block": null, "base_tables": ["google_ads__customer_acquisition_analysis"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |
| B1 | COUNT(DISTINCT account_id \|\| '\|' \|\| SUBSTRING(date_day, 1, 10)) | [{"table": "google_ads__customer_acquisition_analysis", "column": "account_id"}, {"table": "google_ads__customer_acquisition_analysis", "column": "date_day"}] | [] | False |


## S43

类别 `data`；来源 `query_db`；调用 `ef647a6205a047d5aab93fb3983a92df`；状态 `success`。

```sql
SELECT account_id, advertising_channel_type, COUNT(DISTINCT substr(date_day,1,10)) AS n_days
FROM google_ads__customer_acquisition_analysis
WHERE substr(date_day,1,10) BETWEEN '2025-05-22' AND '2025-06-21'
GROUP BY account_id, advertising_channel_type
ORDER BY account_id, advertising_channel_type
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-057/attempt-01/sql/S43.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-057/attempt-01/sql/S43.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-057/attempt-01/results/S43.rows.jsonl)；完整：True；SHA256：`dfcd84724cee4b9ca06fa2d11c4d9d8fbdbf7d7f80fd6084f9bb3fc2e0ed35c4`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "google_ads__customer_acquisition_analysis", "kind": "base", "block": null, "base_tables": ["google_ads__customer_acquisition_analysis"]}] | [] | ["account_id", "advertising_channel_type"] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(DISTINCT SUBSTRING(date_day, 1, 10)) | [{"table": "google_ads__customer_acquisition_analysis", "column": "date_day"}] | [] | False |


## S44

类别 `data`；来源 `query_db`；调用 `1ea2d8ddfef04cdeb7657ff04d6e90f8`；状态 `success`。

```sql
SELECT substr(date_day,1,10) AS d, COUNT(*) AS n FROM google_ads__customer_acquisition_analysis WHERE substr(date_day,1,10) >= '2025-05-01' GROUP BY d ORDER BY d
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-057/attempt-01/sql/S44.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-057/attempt-01/sql/S44.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-057/attempt-01/results/S44.rows.jsonl)；完整：True；SHA256：`0aeb4d16c79b8d06bc1c9ccefaedd294c96f151f6f101e490777ec8e279a9c32`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "google_ads__customer_acquisition_analysis", "kind": "base", "block": null, "base_tables": ["google_ads__customer_acquisition_analysis"]}] | [] | ["SUBSTRING(date_day, 1, 10)"] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |


## S45

类别 `data`；来源 `query_db`；调用 `d6c0ca0170504b07902081d9a6032b90`；状态 `success`。

```sql
SELECT COUNT(*) AS n_in_2024 FROM google_ads__customer_acquisition_analysis WHERE substr(date_day,1,10) BETWEEN '2024-01-03' AND '2024-12-31'
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-057/attempt-01/sql/S45.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-057/attempt-01/sql/S45.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-057/attempt-01/results/S45.rows.jsonl)；完整：True；SHA256：`539d003d6e55b6cf95d41ea852d3c0380d454d11330b61dbf4e7318c9188ebbb`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "google_ads__customer_acquisition_analysis", "kind": "base", "block": null, "base_tables": ["google_ads__customer_acquisition_analysis"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |


## S46

类别 `data`；来源 `query_db`；调用 `42b53773d5e04191afd13decf4c31b0e`；状态 `success`。

```sql
SELECT COUNT(*) AS n_camp_days, COUNT(DISTINCT substr(date_day,1,10)) AS n_days FROM google_ads__campaign_report WHERE substr(date_day,1,10) BETWEEN '2024-01-03' AND '2024-12-31'
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-057/attempt-01/sql/S46.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-057/attempt-01/sql/S46.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-057/attempt-01/results/S46.rows.jsonl)；完整：True；SHA256：`2dc945321a42f03ad5cc440b92a7905022de10aba3f3756f6315fb9649dd00b6`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "google_ads__campaign_report", "kind": "base", "block": null, "base_tables": ["google_ads__campaign_report"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |
| B1 | COUNT(DISTINCT SUBSTRING(date_day, 1, 10)) | [{"table": "google_ads__campaign_report", "column": "date_day"}] | [] | False |


## S47

类别 `data`；来源 `query_db`；调用 `ec49cc352f7046a688d5a414a7d3f709`；状态 `success`。

```sql
SELECT account_id, advertising_channel_type, COUNT(DISTINCT substr(date_day,1,10)) AS n_days
FROM google_ads__customer_acquisition_analysis
WHERE substr(date_day,1,10) BETWEEN '2024-10-02' AND '2024-12-31'
GROUP BY account_id, advertising_channel_type
ORDER BY account_id, advertising_channel_type
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-057/attempt-01/sql/S47.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-057/attempt-01/sql/S47.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-057/attempt-01/results/S47.rows.jsonl)；完整：True；SHA256：`7fca5b1163861d36a558f335aef8bd68e521835b3a33131316d3ba5482180f36`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "google_ads__customer_acquisition_analysis", "kind": "base", "block": null, "base_tables": ["google_ads__customer_acquisition_analysis"]}] | [] | ["account_id", "advertising_channel_type"] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(DISTINCT SUBSTRING(date_day, 1, 10)) | [{"table": "google_ads__customer_acquisition_analysis", "column": "date_day"}] | [] | False |


## S48

类别 `data`；来源 `query_db`；调用 `8191b278d33f4034813245050a498583`；状态 `success`。

```sql
SELECT account_id, advertising_channel_type, COUNT(DISTINCT substr(date_day,1,10)) AS n_days
FROM google_ads__customer_acquisition_analysis
WHERE substr(date_day,1,10) BETWEEN '2024-01-01' AND '2024-12-31'
GROUP BY account_id, advertising_channel_type
ORDER BY account_id, advertising_channel_type
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-057/attempt-01/sql/S48.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-057/attempt-01/sql/S48.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-057/attempt-01/results/S48.rows.jsonl)；完整：True；SHA256：`a8de1061a4d835d84488b4170faf79a80bae565b47e89c37f7571e955e2dd02a`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "google_ads__customer_acquisition_analysis", "kind": "base", "block": null, "base_tables": ["google_ads__customer_acquisition_analysis"]}] | [] | ["account_id", "advertising_channel_type"] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(DISTINCT SUBSTRING(date_day, 1, 10)) | [{"table": "google_ads__customer_acquisition_analysis", "column": "date_day"}] | [] | False |


## S49

类别 `data`；来源 `query_db`；调用 `6bda8ed438b047b6a7d0730cb9bf41ce`；状态 `success`。

```sql
SELECT substr(date_day,1,10) AS d, COUNT(*) AS n
FROM google_ads__customer_acquisition_analysis
WHERE substr(date_day,1,10) BETWEEN '2024-06-01' AND '2024-12-31'
GROUP BY d ORDER BY d
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-057/attempt-01/sql/S49.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-057/attempt-01/sql/S49.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-057/attempt-01/results/S49.rows.jsonl)；完整：True；SHA256：`4227ecf83d397b820e01b0bcc54bf6ea2117944d41c56484ffb79f3b11015548`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "google_ads__customer_acquisition_analysis", "kind": "base", "block": null, "base_tables": ["google_ads__customer_acquisition_analysis"]}] | [] | ["SUBSTRING(date_day, 1, 10)"] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |


## S50

类别 `data`；来源 `query_db`；调用 `6ecd3fc295e644cb83e0b5eb68ff51b4`；状态 `success`。

```sql
SELECT substr(date_day,1,10) AS d, COUNT(*) AS n
FROM google_ads__customer_acquisition_analysis
WHERE substr(date_day,1,10) BETWEEN '2024-01-01' AND '2024-06-30'
GROUP BY d ORDER BY d LIMIT 100
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-057/attempt-01/sql/S50.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-057/attempt-01/sql/S50.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-057/attempt-01/results/S50.rows.jsonl)；完整：True；SHA256：`0ffb2f5edddf239fb6c811b534bd0fbc0e2db781bb1617298e01b4d329f5e8a6`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "google_ads__customer_acquisition_analysis", "kind": "base", "block": null, "base_tables": ["google_ads__customer_acquisition_analysis"]}] | [] | ["SUBSTRING(date_day, 1, 10)"] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |


## S51

类别 `data`；来源 `query_db`；调用 `441f9d1040b241649322a2746ebd829c`；状态 `success`。

```sql
SELECT COUNT(*) AS total,
  COUNT(DISTINCT account_id || '|' || substr(date_day,1,10) || '|' || advertising_channel_type || '|' || advertising_channel_subtype || '|' || customer_maturity_stage || '|' || campaign_lifecycle_stage || '|' || strategic_customer_segment || '|' || account_maturity_stage) AS full_key
FROM google_ads__customer_acquisition_analysis
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-057/attempt-01/sql/S51.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-057/attempt-01/sql/S51.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-057/attempt-01/results/S51.rows.jsonl)；完整：True；SHA256：`3623cc564002d8bad4d8be749ff533418fc76be2f50c2ba4ba344183419dfcfb`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "google_ads__customer_acquisition_analysis", "kind": "base", "block": null, "base_tables": ["google_ads__customer_acquisition_analysis"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |
| B1 | COUNT(DISTINCT account_id \|\| '\|' \|\| SUBSTRING(date_day, 1, 10) \|\| '\|' \|\| advertising_channel_type \|\| '\|' \|\| advertising_channel_subtype \|\| '\|' \|\| customer_maturity_stage \|\| '\|' \|\| campaign_lifecycle_stage \|\| '\|' \|\| strategic_customer_segment \|\| '\|' \|\| account_maturity_stage) | [{"table": "google_ads__customer_acquisition_analysis", "column": "account_maturity_stage"}, {"table": "google_ads__customer_acquisition_analysis", "column": "strategic_customer_segment"}, {"table": "google_ads__customer_acquisition_analysis", "column": "campaign_lifecycle_stage"}, {"table": "google_ads__customer_acquisition_analysis", "column": "customer_maturity_stage"}, {"table": "google_ads__customer_acquisition_analysis", "column": "advertising_channel_subtype"}, {"table": "google_ads__customer_acquisition_analysis", "column": "advertising_channel_type"}, {"table": "google_ads__customer_acquisition_analysis", "column": "account_id"}, {"table": "google_ads__customer_acquisition_analysis", "column": "date_day"}] | [] | False |


## S52

类别 `data`；来源 `query_db`；调用 `d281473003ca4601b704c9b25e0a5675`；状态 `success`。

```sql
SELECT COUNT(DISTINCT account_id || '|' || substr(date_day,1,10) || '|' || advertising_channel_type || '|' || advertising_channel_subtype || '|' || customer_maturity_stage || '|' || campaign_lifecycle_stage) AS key2
FROM google_ads__customer_acquisition_analysis
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-057/attempt-01/sql/S52.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-057/attempt-01/sql/S52.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-057/attempt-01/results/S52.rows.jsonl)；完整：True；SHA256：`ba199cbb95e541125e21f0abbdc59d496e35ed12fd821df223c0005ebd2d45f6`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "google_ads__customer_acquisition_analysis", "kind": "base", "block": null, "base_tables": ["google_ads__customer_acquisition_analysis"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(DISTINCT account_id \|\| '\|' \|\| SUBSTRING(date_day, 1, 10) \|\| '\|' \|\| advertising_channel_type \|\| '\|' \|\| advertising_channel_subtype \|\| '\|' \|\| customer_maturity_stage \|\| '\|' \|\| campaign_lifecycle_stage) | [{"table": "google_ads__customer_acquisition_analysis", "column": "campaign_lifecycle_stage"}, {"table": "google_ads__customer_acquisition_analysis", "column": "customer_maturity_stage"}, {"table": "google_ads__customer_acquisition_analysis", "column": "advertising_channel_subtype"}, {"table": "google_ads__customer_acquisition_analysis", "column": "advertising_channel_type"}, {"table": "google_ads__customer_acquisition_analysis", "column": "account_id"}, {"table": "google_ads__customer_acquisition_analysis", "column": "date_day"}] | [] | False |


## S53

类别 `data`；来源 `query_db`；调用 `41fd9a41189442578865bade9b545253`；状态 `success`。

```sql
WITH camp AS (
  SELECT campaign_id, campaign_name, account_id, account_name, advertising_channel_type, advertising_channel_subtype,
         MIN(substr(date_day,1,10)) AS first_date, MAX(substr(date_day,1,10)) AS last_date,
         CAST(julianday(MAX(substr(date_day,1,10))) - julianday(MIN(substr(date_day,1,10))) AS INTEGER) AS days_running
  FROM google_ads__campaign_report
  GROUP BY campaign_id
  HAVING days_running > 120
)
SELECT c.campaign_id, c.account_id, c.advertising_channel_type, c.advertising_channel_subtype,
       COUNT(a.rowid) AS matched_rows
FROM camp c
LEFT JOIN google_ads__customer_acquisition_analysis a
  ON a.account_id = c.account_id
 AND a.advertising_channel_type = c.advertising_channel_type
 AND COALESCE(a.advertising_channel_subtype,'') = COALESCE(c.advertising_channel_subtype,'')
 AND substr(a.date_day,1,10) BETWEEN c.first_date AND c.last_date
GROUP BY c.campaign_id
ORDER BY matched_rows DESC
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-057/attempt-01/sql/S53.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-057/attempt-01/sql/S53.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-057/attempt-01/results/S53.rows.jsonl)；完整：True；SHA256：`c21711b0795c6cc9fe2f633c6c43251e3ea4d7f82490a9e0c769711ab39373f0`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "google_ads__campaign_report", "kind": "base", "block": null, "base_tables": ["google_ads__campaign_report"]}] | [] | ["campaign_id"] |
| B2 | [{"alias": "c", "kind": "derived", "block": "B1", "base_tables": ["google_ads__campaign_report"]}, {"alias": "a", "kind": "base", "block": null, "base_tables": ["google_ads__customer_acquisition_analysis"]}] | [{"type": "LEFT", "right": "google_ads__customer_acquisition_analysis AS a", "on": "a.account_id = c.account_id AND a.advertising_channel_type = c.advertising_channel_type AND COALESCE(a.advertising_channel_subtype, '') = COALESCE(c.advertising_channel_subtype, '') AND SUBSTRING(a.date_day, 1, 10) BETWEEN c.first_date AND c.last_date", "using": []}] | ["c.campaign_id"] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | MIN(SUBSTRING(date_day, 1, 10)) | [{"table": "google_ads__campaign_report", "column": "date_day"}] | [] | False |
| B1 | MAX(SUBSTRING(date_day, 1, 10)) | [{"table": "google_ads__campaign_report", "column": "date_day"}] | [] | False |
| B1 | MAX(SUBSTRING(date_day, 1, 10)) | [{"table": "google_ads__campaign_report", "column": "date_day"}] | [] | False |
| B1 | MIN(SUBSTRING(date_day, 1, 10)) | [{"table": "google_ads__campaign_report", "column": "date_day"}] | [] | False |
| B2 | COUNT(a.rowid) | [{"table": "google_ads__customer_acquisition_analysis", "column": "rowid"}] | [] | False |


## S54

类别 `data`；来源 `query_db`；调用 `a60baab7ea8a4c59825b400101a793b5`；状态 `success`。

```sql
WITH camp AS (
  SELECT campaign_id, campaign_name, account_id, account_name, advertising_channel_type, advertising_channel_subtype,
         MIN(substr(date_day,1,10)) AS first_date, MAX(substr(date_day,1,10)) AS last_date,
         CAST(julianday(MAX(substr(date_day,1,10))) - julianday(MIN(substr(date_day,1,10))) AS INTEGER) AS days_running
  FROM google_ads__campaign_report
  GROUP BY campaign_id
  HAVING days_running > 120
)
SELECT c.campaign_id, c.account_id, c.advertising_channel_type, c.advertising_channel_subtype, c.days_running,
       COUNT(a.rowid) AS matched_rows
FROM camp c
LEFT JOIN google_ads__customer_acquisition_analysis a
  ON a.account_id = c.account_id
 AND a.advertising_channel_type = c.advertising_channel_type
 AND COALESCE(a.advertising_channel_subtype,'') = COALESCE(c.advertising_channel_subtype,'')
 AND substr(a.date_day,1,10) BETWEEN c.first_date AND c.last_date
GROUP BY c.campaign_id
HAVING matched_rows = 0
ORDER BY c.campaign_id
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-057/attempt-01/sql/S54.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-057/attempt-01/sql/S54.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-057/attempt-01/results/S54.rows.jsonl)；完整：True；SHA256：`4556bc864ad1ffa6323f44703c3aa1254ef575bcfe899fa5596515152743e2ed`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "google_ads__campaign_report", "kind": "base", "block": null, "base_tables": ["google_ads__campaign_report"]}] | [] | ["campaign_id"] |
| B2 | [{"alias": "c", "kind": "derived", "block": "B1", "base_tables": ["google_ads__campaign_report"]}, {"alias": "a", "kind": "base", "block": null, "base_tables": ["google_ads__customer_acquisition_analysis"]}] | [{"type": "LEFT", "right": "google_ads__customer_acquisition_analysis AS a", "on": "a.account_id = c.account_id AND a.advertising_channel_type = c.advertising_channel_type AND COALESCE(a.advertising_channel_subtype, '') = COALESCE(c.advertising_channel_subtype, '') AND SUBSTRING(a.date_day, 1, 10) BETWEEN c.first_date AND c.last_date", "using": []}] | ["c.campaign_id"] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | MIN(SUBSTRING(date_day, 1, 10)) | [{"table": "google_ads__campaign_report", "column": "date_day"}] | [] | False |
| B1 | MAX(SUBSTRING(date_day, 1, 10)) | [{"table": "google_ads__campaign_report", "column": "date_day"}] | [] | False |
| B1 | MAX(SUBSTRING(date_day, 1, 10)) | [{"table": "google_ads__campaign_report", "column": "date_day"}] | [] | False |
| B1 | MIN(SUBSTRING(date_day, 1, 10)) | [{"table": "google_ads__campaign_report", "column": "date_day"}] | [] | False |
| B2 | COUNT(a.rowid) | [{"table": "google_ads__customer_acquisition_analysis", "column": "rowid"}] | [] | False |


## S55

类别 `data`；来源 `query_db`；调用 `3e233a9ae18b43658927f769e102b4d5`；状态 `success`。

```sql
SELECT account_id, advertising_channel_type, advertising_channel_subtype, COUNT(*) AS n
FROM google_ads__customer_acquisition_analysis
GROUP BY account_id, advertising_channel_type, advertising_channel_subtype
ORDER BY account_id, advertising_channel_type
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-057/attempt-01/sql/S55.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-057/attempt-01/sql/S55.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-057/attempt-01/results/S55.rows.jsonl)；完整：True；SHA256：`b458aea9f8f50be5dceaf8fb8a7a314e57d68a9f43d0132447e4268cfc00de6e`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "google_ads__customer_acquisition_analysis", "kind": "base", "block": null, "base_tables": ["google_ads__customer_acquisition_analysis"]}] | [] | ["account_id", "advertising_channel_type", "advertising_channel_subtype"] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |


## S56

类别 `data`；来源 `query_db`；调用 `27d021027c394344a322c6d8de239f8f`；状态 `success`。

```sql
SELECT DISTINCT account_id FROM google_ads__customer_acquisition_analysis ORDER BY account_id
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-057/attempt-01/sql/S56.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-057/attempt-01/sql/S56.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-057/attempt-01/results/S56.rows.jsonl)；完整：True；SHA256：`4c46c8bab455d558920bb6c02c514811d59fe3525592f094e505fd4d38443395`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "google_ads__customer_acquisition_analysis", "kind": "base", "block": null, "base_tables": ["google_ads__customer_acquisition_analysis"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |


## S57

类别 `data`；来源 `query_db`；调用 `9765c079b8d342e2982565b90f8a4e41`；状态 `success`。

```sql
SELECT account_id, advertising_channel_type, advertising_channel_subtype, COUNT(*) AS n, MIN(substr(date_day,1,10)) AS min_d, MAX(substr(date_day,1,10)) AS max_d
FROM google_ads__customer_acquisition_analysis
WHERE account_id IN ('ACC_HLTH_001','ACC_FIN_001','ACC_GAME_001','ACC_SAAS_001')
GROUP BY account_id, advertising_channel_type, advertising_channel_subtype
ORDER BY account_id, advertising_channel_type
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-057/attempt-01/sql/S57.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-057/attempt-01/sql/S57.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-057/attempt-01/results/S57.rows.jsonl)；完整：True；SHA256：`2a0e16fb3c242d689e4007f1f6ab59e31a7f766877c17e118edee0205c6c5d6a`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "google_ads__customer_acquisition_analysis", "kind": "base", "block": null, "base_tables": ["google_ads__customer_acquisition_analysis"]}] | [] | ["account_id", "advertising_channel_type", "advertising_channel_subtype"] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |
| B1 | MIN(SUBSTRING(date_day, 1, 10)) | [{"table": "google_ads__customer_acquisition_analysis", "column": "date_day"}] | [] | False |
| B1 | MAX(SUBSTRING(date_day, 1, 10)) | [{"table": "google_ads__customer_acquisition_analysis", "column": "date_day"}] | [] | False |


## S58

类别 `data`；来源 `query_db`；调用 `48029a2d38f747e887361b9ea86e7623`；状态 `success`。

```sql
WITH camp AS (
  SELECT campaign_id, account_id, advertising_channel_type, advertising_channel_subtype,
         MIN(substr(date_day,1,10)) AS first_date, MAX(substr(date_day,1,10)) AS last_date
  FROM google_ads__campaign_report
  GROUP BY campaign_id
  HAVING CAST(julianday(MAX(substr(date_day,1,10))) - julianday(MIN(substr(date_day,1,10))) AS INTEGER) > 120
)
SELECT c.campaign_id, c.account_id, c.advertising_channel_type, c.advertising_channel_subtype,
       c.last_date AS camp_last_date,
       MAX(substr(a.date_day,1,10)) AS acq_last_date,
       MIN(substr(a.date_day,1,10)) AS acq_first_date,
       COUNT(a.rowid) AS n_rows
FROM camp c
JOIN google_ads__customer_acquisition_analysis a
  ON a.account_id = c.account_id
 AND a.advertising_channel_type = c.advertising_channel_type
 AND COALESCE(a.advertising_channel_subtype,'') = COALESCE(c.advertising_channel_subtype,'')
 AND substr(a.date_day,1,10) BETWEEN c.first_date AND c.last_date
GROUP BY c.campaign_id
ORDER BY c.campaign_id
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-057/attempt-01/sql/S58.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-057/attempt-01/sql/S58.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-057/attempt-01/results/S58.rows.jsonl)；完整：True；SHA256：`a29c07d4b24c9590f8615b0b0d5a59ab9239fc43e5df0bb4a73227b5204b6122`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "google_ads__campaign_report", "kind": "base", "block": null, "base_tables": ["google_ads__campaign_report"]}] | [] | ["campaign_id"] |
| B2 | [{"alias": "c", "kind": "derived", "block": "B1", "base_tables": ["google_ads__campaign_report"]}, {"alias": "a", "kind": "base", "block": null, "base_tables": ["google_ads__customer_acquisition_analysis"]}] | [{"type": "INNER", "right": "google_ads__customer_acquisition_analysis AS a", "on": "a.account_id = c.account_id AND a.advertising_channel_type = c.advertising_channel_type AND COALESCE(a.advertising_channel_subtype, '') = COALESCE(c.advertising_channel_subtype, '') AND SUBSTRING(a.date_day, 1, 10) BETWEEN c.first_date AND c.last_date", "using": []}] | ["c.campaign_id"] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | MIN(SUBSTRING(date_day, 1, 10)) | [{"table": "google_ads__campaign_report", "column": "date_day"}] | [] | False |
| B1 | MAX(SUBSTRING(date_day, 1, 10)) | [{"table": "google_ads__campaign_report", "column": "date_day"}] | [] | False |
| B1 | MAX(SUBSTRING(date_day, 1, 10)) | [{"table": "google_ads__campaign_report", "column": "date_day"}] | [] | False |
| B1 | MIN(SUBSTRING(date_day, 1, 10)) | [{"table": "google_ads__campaign_report", "column": "date_day"}] | [] | False |
| B2 | MAX(SUBSTRING(a.date_day, 1, 10)) | [{"table": "google_ads__customer_acquisition_analysis", "column": "date_day"}] | [] | False |
| B2 | MIN(SUBSTRING(a.date_day, 1, 10)) | [{"table": "google_ads__customer_acquisition_analysis", "column": "date_day"}] | [] | False |
| B2 | COUNT(a.rowid) | [{"table": "google_ads__customer_acquisition_analysis", "column": "rowid"}] | [] | False |


## S59

类别 `data`；来源 `query_db`；调用 `45b1818dbe294132bb54ed0c6d650cef`；状态 `success`。

```sql
WITH camp AS (
  SELECT campaign_id, campaign_name, account_id, account_name, advertising_channel_type, advertising_channel_subtype,
         MIN(substr(date_day,1,10)) AS first_date, MAX(substr(date_day,1,10)) AS last_date,
         CAST(julianday(MAX(substr(date_day,1,10))) - julianday(MIN(substr(date_day,1,10))) AS INTEGER) AS days_running
  FROM google_ads__campaign_report
  GROUP BY campaign_id
  HAVING days_running > 120
),
joined AS (
  SELECT c.campaign_id, c.campaign_name, c.account_id, c.account_name, c.advertising_channel_type, c.advertising_channel_subtype,
         substr(a.date_day,1,10) AS d, a.customer_acquisition_cost, a.ltv_cac_ratio, a.spend, a.conversions,
         a.campaign_lifecycle_stage, a.customer_maturity_stage, a.account_maturity_stage, a.strategic_customer_segment,
         a.acquisition_sophistication_score, a.cac_efficiency_percentile, a.channel_diversity_count,
         a.retention_risk, a.scale_opportunity, a.high_cac_alert, a.negative_roi_alert,
         julianday(substr(a.date_day,1,10)) AS jd
  FROM camp c
  JOIN google_ads__customer_acquisition_analysis a
    ON a.account_id = c.account_id
   AND a.advertising_channel_type = c.advertising_channel_type
   AND COALESCE(a.advertising_channel_subtype,'') = COALESCE(c.advertising_channel_subtype,'')
   AND substr(a.date_day,1,10) BETWEEN c.first_date AND c.last_date
),
refs AS (
  SELECT campaign_id, MAX(jd) AS ref_jd, MAX(d) AS ref_date, COUNT(*) AS n_rows,
         MAX(jd) - MIN(jd) AS span_days
  FROM joined
  GROUP BY campaign_id
)
SELECT j.campaign_id, j.campaign_name, j.account_id, j.advertising_channel_type, j.advertising_channel_subtype,
       r.ref_date, r.span_days,
       SUM(CASE WHEN j.jd >= r.ref_jd - 29 THEN 1 ELSE 0 END) AS n_last30,
       SUM(CASE WHEN j.jd BETWEEN r.ref_jd - 59 AND r.ref_jd - 30 THEN 1 ELSE 0 END) AS n_prior30
FROM joined j
JOIN refs r ON r.campaign_id = j.campaign_id
GROUP BY j.campaign_id
ORDER BY r.ref_date DESC
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-057/attempt-01/sql/S59.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-057/attempt-01/sql/S59.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-057/attempt-01/results/S59.rows.jsonl)；完整：True；SHA256：`a7618ef89f14d28c8163759cdb0d54f43d9ec1dd46734ee36a2480e79f4e5ed6`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "google_ads__campaign_report", "kind": "base", "block": null, "base_tables": ["google_ads__campaign_report"]}] | [] | ["campaign_id"] |
| B2 | [{"alias": "c", "kind": "derived", "block": "B1", "base_tables": ["google_ads__campaign_report"]}, {"alias": "a", "kind": "base", "block": null, "base_tables": ["google_ads__customer_acquisition_analysis"]}] | [{"type": "INNER", "right": "google_ads__customer_acquisition_analysis AS a", "on": "a.account_id = c.account_id AND a.advertising_channel_type = c.advertising_channel_type AND COALESCE(a.advertising_channel_subtype, '') = COALESCE(c.advertising_channel_subtype, '') AND SUBSTRING(a.date_day, 1, 10) BETWEEN c.first_date AND c.last_date", "using": []}] | [] |
| B3 | [{"alias": "joined", "kind": "derived", "block": "B2", "base_tables": ["google_ads__campaign_report", "google_ads__customer_acquisition_analysis"]}] | [] | ["campaign_id"] |
| B4 | [{"alias": "j", "kind": "derived", "block": "B2", "base_tables": ["google_ads__campaign_report", "google_ads__customer_acquisition_analysis"]}, {"alias": "r", "kind": "derived", "block": "B3", "base_tables": ["google_ads__campaign_report", "google_ads__customer_acquisition_analysis"]}] | [{"type": "INNER", "right": "refs AS r", "on": "r.campaign_id = j.campaign_id", "using": []}] | ["j.campaign_id"] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | MIN(SUBSTRING(date_day, 1, 10)) | [{"table": "google_ads__campaign_report", "column": "date_day"}] | [] | False |
| B1 | MAX(SUBSTRING(date_day, 1, 10)) | [{"table": "google_ads__campaign_report", "column": "date_day"}] | [] | False |
| B1 | MAX(SUBSTRING(date_day, 1, 10)) | [{"table": "google_ads__campaign_report", "column": "date_day"}] | [] | False |
| B1 | MIN(SUBSTRING(date_day, 1, 10)) | [{"table": "google_ads__campaign_report", "column": "date_day"}] | [] | False |
| B3 | MAX(jd) | [{"table": "google_ads__customer_acquisition_analysis", "column": "date_day"}] | [] | False |
| B3 | MAX(d) | [{"table": "google_ads__customer_acquisition_analysis", "column": "date_day"}] | [] | False |
| B3 | COUNT(*) | [] | [] | True |
| B3 | MAX(jd) | [{"table": "google_ads__customer_acquisition_analysis", "column": "date_day"}] | [] | False |
| B3 | MIN(jd) | [{"table": "google_ads__customer_acquisition_analysis", "column": "date_day"}] | [] | False |
| B4 | SUM(CASE WHEN j.jd >= r.ref_jd - 29 THEN 1 ELSE 0 END) | [] | [{"table": "google_ads__customer_acquisition_analysis", "column": "date_day"}, {"table": "google_ads__customer_acquisition_analysis", "column": "date_day"}] | False |
| B4 | SUM(CASE WHEN j.jd BETWEEN r.ref_jd - 59 AND r.ref_jd - 30 THEN 1 ELSE 0 END) | [] | [{"table": "google_ads__customer_acquisition_analysis", "column": "date_day"}, {"table": "google_ads__customer_acquisition_analysis", "column": "date_day"}, {"table": "google_ads__customer_acquisition_analysis", "column": "date_day"}] | False |


## S60

类别 `data`；来源 `query_db`；调用 `3772cfb5ecc9468696bc4e866b184911`；状态 `success`。

```sql
WITH camp AS (
  SELECT campaign_id, campaign_name, account_id, account_name, advertising_channel_type, advertising_channel_subtype,
         MIN(substr(date_day,1,10)) AS first_date, MAX(substr(date_day,1,10)) AS last_date,
         CAST(julianday(MAX(substr(date_day,1,10))) - julianday(MIN(substr(date_day,1,10))) AS INTEGER) AS days_running
  FROM google_ads__campaign_report
  GROUP BY campaign_id
  HAVING days_running > 120
),
joined AS (
  SELECT c.campaign_id, c.campaign_name, c.account_id, c.account_name, c.advertising_channel_type, c.advertising_channel_subtype,
         substr(a.date_day,1,10) AS d, a.customer_acquisition_cost, a.ltv_cac_ratio, a.spend, a.conversions,
         julianday(substr(a.date_day,1,10)) AS jd
  FROM camp c
  JOIN google_ads__customer_acquisition_analysis a
    ON a.account_id = c.account_id
   AND a.advertising_channel_type = c.advertising_channel_type
   AND COALESCE(a.advertising_channel_subtype,'') = COALESCE(c.advertising_channel_subtype,'')
   AND substr(a.date_day,1,10) BETWEEN c.first_date AND c.last_date
),
refs AS (
  SELECT campaign_id, MAX(jd) AS ref_jd FROM joined GROUP BY campaign_id
),
win AS (
  SELECT j.campaign_id, j.campaign_name, j.account_id, j.account_name, j.advertising_channel_type, j.advertising_channel_subtype,
         r.ref_jd,
         SUM(CASE WHEN j.jd >= r.ref_jd - 29 THEN j.spend ELSE 0 END) AS spend_last,
         SUM(CASE WHEN j.jd >= r.ref_jd - 29 THEN j.conversions ELSE 0 END) AS conv_last,
         SUM(CASE WHEN j.jd >= r.ref_jd - 29 THEN j.conversions * j.ltv_cac_ratio ELSE 0 END) AS ltv_cac_w_last,
         SUM(CASE WHEN j.jd BETWEEN r.ref_jd - 59 AND r.ref_jd - 30 THEN j.spend ELSE 0 END) AS spend_prior,
         SUM(CASE WHEN j.jd BETWEEN r.ref_jd - 59 AND r.ref_jd - 30 THEN j.conversions ELSE 0 END) AS conv_prior,
         SUM(CASE WHEN j.jd BETWEEN r.ref_jd - 59 AND r.ref_jd - 30 THEN j.conversions * j.ltv_cac_ratio ELSE 0 END) AS ltv_cac_w_prior
  FROM joined j
  JOIN refs r ON r.campaign_id = j.campaign_id
  GROUP BY j.campaign_id
)
SELECT campaign_id, campaign_name, account_id, advertising_channel_type, advertising_channel_subtype,
       spend_last, conv_last, spend_prior, conv_prior,
       ROUND(spend_last/NULLIF(conv_last,0),2) AS cac_last,
       ROUND(spend_prior/NULLIF(conv_prior,0),2) AS cac_prior,
       ROUND((spend_last/NULLIF(conv_last,0) - spend_prior/NULLIF(conv_prior,0))/NULLIF(spend_prior/NULLIF(conv_prior,0),0),4) AS cac_growth,
       ROUND(ltv_cac_w_last/NULLIF(conv_last,0),2) AS ltv_cac_last,
       ROUND(ltv_cac_w_prior/NULLIF(conv_prior,0),2) AS ltv_cac_prior,
       ROUND((ltv_cac_w_last/NULLIF(conv_last,0) - ltv_cac_w_prior/NULLIF(conv_prior,0))/NULLIF(ltv_cac_w_prior/NULLIF(conv_prior,0),0),4) AS ltv_cac_change
FROM win
ORDER BY cac_growth DESC
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-057/attempt-01/sql/S60.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-057/attempt-01/sql/S60.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-057/attempt-01/results/S60.rows.jsonl)；完整：True；SHA256：`f50e91dd92ea0cf007b7df904c628a1f90c4d35dd8f4d5fc8b9f5aa49aef08f0`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "google_ads__campaign_report", "kind": "base", "block": null, "base_tables": ["google_ads__campaign_report"]}] | [] | ["campaign_id"] |
| B2 | [{"alias": "c", "kind": "derived", "block": "B1", "base_tables": ["google_ads__campaign_report"]}, {"alias": "a", "kind": "base", "block": null, "base_tables": ["google_ads__customer_acquisition_analysis"]}] | [{"type": "INNER", "right": "google_ads__customer_acquisition_analysis AS a", "on": "a.account_id = c.account_id AND a.advertising_channel_type = c.advertising_channel_type AND COALESCE(a.advertising_channel_subtype, '') = COALESCE(c.advertising_channel_subtype, '') AND SUBSTRING(a.date_day, 1, 10) BETWEEN c.first_date AND c.last_date", "using": []}] | [] |
| B3 | [{"alias": "joined", "kind": "derived", "block": "B2", "base_tables": ["google_ads__campaign_report", "google_ads__customer_acquisition_analysis"]}] | [] | ["campaign_id"] |
| B4 | [{"alias": "j", "kind": "derived", "block": "B2", "base_tables": ["google_ads__campaign_report", "google_ads__customer_acquisition_analysis"]}, {"alias": "r", "kind": "derived", "block": "B3", "base_tables": ["google_ads__campaign_report", "google_ads__customer_acquisition_analysis"]}] | [{"type": "INNER", "right": "refs AS r", "on": "r.campaign_id = j.campaign_id", "using": []}] | ["j.campaign_id"] |
| B5 | [{"alias": "win", "kind": "derived", "block": "B4", "base_tables": ["google_ads__campaign_report", "google_ads__customer_acquisition_analysis"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | MIN(SUBSTRING(date_day, 1, 10)) | [{"table": "google_ads__campaign_report", "column": "date_day"}] | [] | False |
| B1 | MAX(SUBSTRING(date_day, 1, 10)) | [{"table": "google_ads__campaign_report", "column": "date_day"}] | [] | False |
| B1 | MAX(SUBSTRING(date_day, 1, 10)) | [{"table": "google_ads__campaign_report", "column": "date_day"}] | [] | False |
| B1 | MIN(SUBSTRING(date_day, 1, 10)) | [{"table": "google_ads__campaign_report", "column": "date_day"}] | [] | False |
| B3 | MAX(jd) | [{"table": "google_ads__customer_acquisition_analysis", "column": "date_day"}] | [] | False |
| B4 | SUM(CASE WHEN j.jd >= r.ref_jd - 29 THEN j.spend ELSE 0 END) | [{"table": "google_ads__customer_acquisition_analysis", "column": "spend"}] | [{"table": "google_ads__customer_acquisition_analysis", "column": "date_day"}, {"table": "google_ads__customer_acquisition_analysis", "column": "date_day"}] | False |
| B4 | SUM(CASE WHEN j.jd >= r.ref_jd - 29 THEN j.conversions ELSE 0 END) | [{"table": "google_ads__customer_acquisition_analysis", "column": "conversions"}] | [{"table": "google_ads__customer_acquisition_analysis", "column": "date_day"}, {"table": "google_ads__customer_acquisition_analysis", "column": "date_day"}] | False |
| B4 | SUM(CASE WHEN j.jd >= r.ref_jd - 29 THEN j.conversions * j.ltv_cac_ratio ELSE 0 END) | [{"table": "google_ads__customer_acquisition_analysis", "column": "conversions"}, {"table": "google_ads__customer_acquisition_analysis", "column": "ltv_cac_ratio"}] | [{"table": "google_ads__customer_acquisition_analysis", "column": "date_day"}, {"table": "google_ads__customer_acquisition_analysis", "column": "date_day"}] | False |
| B4 | SUM(CASE WHEN j.jd BETWEEN r.ref_jd - 59 AND r.ref_jd - 30 THEN j.spend ELSE 0 END) | [{"table": "google_ads__customer_acquisition_analysis", "column": "spend"}] | [{"table": "google_ads__customer_acquisition_analysis", "column": "date_day"}, {"table": "google_ads__customer_acquisition_analysis", "column": "date_day"}, {"table": "google_ads__customer_acquisition_analysis", "column": "date_day"}] | False |
| B4 | SUM(CASE WHEN j.jd BETWEEN r.ref_jd - 59 AND r.ref_jd - 30 THEN j.conversions ELSE 0 END) | [{"table": "google_ads__customer_acquisition_analysis", "column": "conversions"}] | [{"table": "google_ads__customer_acquisition_analysis", "column": "date_day"}, {"table": "google_ads__customer_acquisition_analysis", "column": "date_day"}, {"table": "google_ads__customer_acquisition_analysis", "column": "date_day"}] | False |
| B4 | SUM(CASE WHEN j.jd BETWEEN r.ref_jd - 59 AND r.ref_jd - 30 THEN j.conversions * j.ltv_cac_ratio ELSE 0 END) | [{"table": "google_ads__customer_acquisition_analysis", "column": "conversions"}, {"table": "google_ads__customer_acquisition_analysis", "column": "ltv_cac_ratio"}] | [{"table": "google_ads__customer_acquisition_analysis", "column": "date_day"}, {"table": "google_ads__customer_acquisition_analysis", "column": "date_day"}, {"table": "google_ads__customer_acquisition_analysis", "column": "date_day"}] | False |


## S61

类别 `data`；来源 `query_db`；调用 `f8dfc61564194fdf8e9d2d17b75622d2`；状态 `success`。

```sql
WITH camp AS (
  SELECT campaign_id, campaign_name, account_id, account_name, advertising_channel_type, advertising_channel_subtype,
         MIN(substr(date_day,1,10)) AS first_date, MAX(substr(date_day,1,10)) AS last_date,
         CAST(julianday(MAX(substr(date_day,1,10))) - julianday(MIN(substr(date_day,1,10))) AS INTEGER) AS days_running
  FROM google_ads__campaign_report
  GROUP BY campaign_id
  HAVING days_running > 120
),
joined AS (
  SELECT c.campaign_id, c.campaign_name, c.account_id, c.account_name, c.advertising_channel_type, c.advertising_channel_subtype,
         substr(a.date_day,1,10) AS d, a.customer_acquisition_cost, a.ltv_cac_ratio, a.spend, a.conversions,
         julianday(substr(a.date_day,1,10)) AS jd
  FROM camp c
  JOIN google_ads__customer_acquisition_analysis a
    ON a.account_id = c.account_id
   AND a.advertising_channel_type = c.advertising_channel_type
   AND COALESCE(a.advertising_channel_subtype,'') = COALESCE(c.advertising_channel_subtype,'')
   AND substr(a.date_day,1,10) BETWEEN c.first_date AND c.last_date
),
refs AS (
  SELECT campaign_id, MAX(jd) AS ref_jd FROM joined GROUP BY campaign_id
),
win AS (
  SELECT j.campaign_id, j.campaign_name, j.account_id, j.account_name, j.advertising_channel_type, j.advertising_channel_subtype,
         SUM(CASE WHEN j.jd >= r.ref_jd - 29 THEN j.spend ELSE 0 END) AS spend_last,
         SUM(CASE WHEN j.jd >= r.ref_jd - 29 THEN j.conversions ELSE 0 END) AS conv_last,
         SUM(CASE WHEN j.jd >= r.ref_jd - 29 THEN j.conversions * j.ltv_cac_ratio ELSE 0 END) AS ltv_cac_w_last,
         SUM(CASE WHEN j.jd BETWEEN r.ref_jd - 59 AND r.ref_jd - 30 THEN j.spend ELSE 0 END) AS spend_prior,
         SUM(CASE WHEN j.jd BETWEEN r.ref_jd - 59 AND r.ref_jd - 30 THEN j.conversions ELSE 0 END) AS conv_prior,
         SUM(CASE WHEN j.jd BETWEEN r.ref_jd - 59 AND r.ref_jd - 30 THEN j.conversions * j.ltv_cac_ratio ELSE 0 END) AS ltv_cac_w_prior
  FROM joined j
  JOIN refs r ON r.campaign_id = j.campaign_id
  GROUP BY j.campaign_id
)
SELECT COUNT(*) AS n_candidates,
       SUM(CASE WHEN cac_last > 0 AND cac_prior > 0 AND cac_growth > 0.25 AND ltv_cac_change < -0.20 THEN 1 ELSE 0 END) AS n_decay_flag
FROM (
  SELECT campaign_id, campaign_name, account_id, advertising_channel_type, advertising_channel_subtype,
         spend_last, conv_last, spend_prior, conv_prior,
         (spend_last/NULLIF(conv_last,0)) AS cac_last,
         (spend_prior/NULLIF(conv_prior,0)) AS cac_prior,
         (spend_last/NULLIF(conv_last,0) - spend_prior/NULLIF(conv_prior,0))/NULLIF(spend_prior/NULLIF(conv_prior,0),0) AS cac_growth,
         (ltv_cac_w_last/NULLIF(conv_last,0) - ltv_cac_w_prior/NULLIF(conv_prior,0))/NULLIF(ltv_cac_w_prior/NULLIF(conv_prior,0),0) AS ltv_cac_change
  FROM win
)
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-057/attempt-01/sql/S61.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-057/attempt-01/sql/S61.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-057/attempt-01/results/S61.rows.jsonl)；完整：True；SHA256：`c3b15648358845fee31c57afd3caea00a98b2c563fbfc804b36a9eb303c5992f`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "google_ads__campaign_report", "kind": "base", "block": null, "base_tables": ["google_ads__campaign_report"]}] | [] | ["campaign_id"] |
| B2 | [{"alias": "c", "kind": "derived", "block": "B1", "base_tables": ["google_ads__campaign_report"]}, {"alias": "a", "kind": "base", "block": null, "base_tables": ["google_ads__customer_acquisition_analysis"]}] | [{"type": "INNER", "right": "google_ads__customer_acquisition_analysis AS a", "on": "a.account_id = c.account_id AND a.advertising_channel_type = c.advertising_channel_type AND COALESCE(a.advertising_channel_subtype, '') = COALESCE(c.advertising_channel_subtype, '') AND SUBSTRING(a.date_day, 1, 10) BETWEEN c.first_date AND c.last_date", "using": []}] | [] |
| B3 | [{"alias": "joined", "kind": "derived", "block": "B2", "base_tables": ["google_ads__campaign_report", "google_ads__customer_acquisition_analysis"]}] | [] | ["campaign_id"] |
| B4 | [{"alias": "j", "kind": "derived", "block": "B2", "base_tables": ["google_ads__campaign_report", "google_ads__customer_acquisition_analysis"]}, {"alias": "r", "kind": "derived", "block": "B3", "base_tables": ["google_ads__campaign_report", "google_ads__customer_acquisition_analysis"]}] | [{"type": "INNER", "right": "refs AS r", "on": "r.campaign_id = j.campaign_id", "using": []}] | ["j.campaign_id"] |
| B5 | [{"alias": "win", "kind": "derived", "block": "B4", "base_tables": ["google_ads__campaign_report", "google_ads__customer_acquisition_analysis"]}] | [] | [] |
| B6 | [{"alias": "", "kind": "derived", "block": "B5", "base_tables": ["google_ads__campaign_report", "google_ads__customer_acquisition_analysis"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | MIN(SUBSTRING(date_day, 1, 10)) | [{"table": "google_ads__campaign_report", "column": "date_day"}] | [] | False |
| B1 | MAX(SUBSTRING(date_day, 1, 10)) | [{"table": "google_ads__campaign_report", "column": "date_day"}] | [] | False |
| B1 | MAX(SUBSTRING(date_day, 1, 10)) | [{"table": "google_ads__campaign_report", "column": "date_day"}] | [] | False |
| B1 | MIN(SUBSTRING(date_day, 1, 10)) | [{"table": "google_ads__campaign_report", "column": "date_day"}] | [] | False |
| B3 | MAX(jd) | [{"table": "google_ads__customer_acquisition_analysis", "column": "date_day"}] | [] | False |
| B4 | SUM(CASE WHEN j.jd >= r.ref_jd - 29 THEN j.spend ELSE 0 END) | [{"table": "google_ads__customer_acquisition_analysis", "column": "spend"}] | [{"table": "google_ads__customer_acquisition_analysis", "column": "date_day"}, {"table": "google_ads__customer_acquisition_analysis", "column": "date_day"}] | False |
| B4 | SUM(CASE WHEN j.jd >= r.ref_jd - 29 THEN j.conversions ELSE 0 END) | [{"table": "google_ads__customer_acquisition_analysis", "column": "conversions"}] | [{"table": "google_ads__customer_acquisition_analysis", "column": "date_day"}, {"table": "google_ads__customer_acquisition_analysis", "column": "date_day"}] | False |
| B4 | SUM(CASE WHEN j.jd >= r.ref_jd - 29 THEN j.conversions * j.ltv_cac_ratio ELSE 0 END) | [{"table": "google_ads__customer_acquisition_analysis", "column": "conversions"}, {"table": "google_ads__customer_acquisition_analysis", "column": "ltv_cac_ratio"}] | [{"table": "google_ads__customer_acquisition_analysis", "column": "date_day"}, {"table": "google_ads__customer_acquisition_analysis", "column": "date_day"}] | False |
| B4 | SUM(CASE WHEN j.jd BETWEEN r.ref_jd - 59 AND r.ref_jd - 30 THEN j.spend ELSE 0 END) | [{"table": "google_ads__customer_acquisition_analysis", "column": "spend"}] | [{"table": "google_ads__customer_acquisition_analysis", "column": "date_day"}, {"table": "google_ads__customer_acquisition_analysis", "column": "date_day"}, {"table": "google_ads__customer_acquisition_analysis", "column": "date_day"}] | False |
| B4 | SUM(CASE WHEN j.jd BETWEEN r.ref_jd - 59 AND r.ref_jd - 30 THEN j.conversions ELSE 0 END) | [{"table": "google_ads__customer_acquisition_analysis", "column": "conversions"}] | [{"table": "google_ads__customer_acquisition_analysis", "column": "date_day"}, {"table": "google_ads__customer_acquisition_analysis", "column": "date_day"}, {"table": "google_ads__customer_acquisition_analysis", "column": "date_day"}] | False |
| B4 | SUM(CASE WHEN j.jd BETWEEN r.ref_jd - 59 AND r.ref_jd - 30 THEN j.conversions * j.ltv_cac_ratio ELSE 0 END) | [{"table": "google_ads__customer_acquisition_analysis", "column": "conversions"}, {"table": "google_ads__customer_acquisition_analysis", "column": "ltv_cac_ratio"}] | [{"table": "google_ads__customer_acquisition_analysis", "column": "date_day"}, {"table": "google_ads__customer_acquisition_analysis", "column": "date_day"}, {"table": "google_ads__customer_acquisition_analysis", "column": "date_day"}] | False |
| B6 | COUNT(*) | [] | [] | True |
| B6 | SUM(CASE WHEN cac_last > 0 AND cac_prior > 0 AND cac_growth > 0.25 AND ltv_cac_change < -0.20 THEN 1 ELSE 0 END) | [] | [{"table": "google_ads__customer_acquisition_analysis", "column": "date_day"}, {"table": "google_ads__customer_acquisition_analysis", "column": "conversions"}, {"table": "google_ads__customer_acquisition_analysis", "column": "ltv_cac_ratio"}, {"table": "google_ads__customer_acquisition_analysis", "column": "date_day"}, {"table": "google_ads__customer_acquisition_analysis", "column": "date_day"}, {"table": "google_ads__customer_acquisition_analysis", "column": "date_day"}, {"table": "google_ads__customer_acquisition_analysis", "column": "conversions"}, {"table": "google_ads__customer_acquisition_analysis", "column": "ltv_cac_ratio"}, {"table": "google_ads__customer_acquisition_analysis", "column": "date_day"}, {"table": "google_ads__customer_acquisition_analysis", "column": "date_day"}, {"table": "google_ads__customer_acquisition_analysis", "column": "conversions"}, {"table": "google_ads__customer_acquisition_analysis", "column": "ltv_cac_ratio"}, {"table": "google_ads__customer_acquisition_analysis", "column": "date_day"}, {"table": "google_ads__customer_acquisition_analysis", "column": "date_day"}, {"table": "google_ads__customer_acquisition_analysis", "column": "conversions"}, {"table": "google_ads__customer_acquisition_analysis", "column": "date_day"}, {"table": "google_ads__customer_acquisition_analysis", "column": "date_day"}, {"table": "google_ads__customer_acquisition_analysis", "column": "date_day"}, {"table": "google_ads__customer_acquisition_analysis", "column": "conversions"}, {"table": "google_ads__customer_acquisition_analysis", "column": "date_day"}, {"table": "google_ads__customer_acquisition_analysis", "column": "date_day"}, {"table": "google_ads__customer_acquisition_analysis", "column": "conversions"}, {"table": "google_ads__customer_acquisition_analysis", "column": "date_day"}, {"table": "google_ads__customer_acquisition_analysis", "column": "date_day"}, {"table": "google_ads__customer_acquisition_analysis", "column": "date_day"}, {"table": "google_ads__customer_acquisition_analysis", "column": "spend"}, {"table": "google_ads__customer_acquisition_analysis", "column": "date_day"}, {"table": "google_ads__customer_acquisition_analysis", "column": "date_day"}, {"table": "google_ads__customer_acquisition_analysis", "column": "date_day"}, {"table": "google_ads__customer_acquisition_analysis", "column": "spend"}, {"table": "google_ads__customer_acquisition_analysis", "column": "date_day"}, {"table": "google_ads__customer_acquisition_analysis", "column": "date_day"}, {"table": "google_ads__customer_acquisition_analysis", "column": "spend"}, {"table": "google_ads__customer_acquisition_analysis", "column": "date_day"}, {"table": "google_ads__customer_acquisition_analysis", "column": "date_day"}, {"table": "google_ads__customer_acquisition_analysis", "column": "date_day"}, {"table": "google_ads__customer_acquisition_analysis", "column": "conversions"}, {"table": "google_ads__customer_acquisition_analysis", "column": "date_day"}, {"table": "google_ads__customer_acquisition_analysis", "column": "date_day"}, {"table": "google_ads__customer_acquisition_analysis", "column": "date_day"}, {"table": "google_ads__customer_acquisition_analysis", "column": "conversions"}, {"table": "google_ads__customer_acquisition_analysis", "column": "date_day"}, {"table": "google_ads__customer_acquisition_analysis", "column": "date_day"}, {"table": "google_ads__customer_acquisition_analysis", "column": "conversions"}, {"table": "google_ads__customer_acquisition_analysis", "column": "date_day"}, {"table": "google_ads__customer_acquisition_analysis", "column": "date_day"}, {"table": "google_ads__customer_acquisition_analysis", "column": "date_day"}, {"table": "google_ads__customer_acquisition_analysis", "column": "spend"}, {"table": "google_ads__customer_acquisition_analysis", "column": "date_day"}, {"table": "google_ads__customer_acquisition_analysis", "column": "date_day"}, {"table": "google_ads__customer_acquisition_analysis", "column": "conversions"}, {"table": "google_ads__customer_acquisition_analysis", "column": "date_day"}, {"table": "google_ads__customer_acquisition_analysis", "column": "date_day"}, {"table": "google_ads__customer_acquisition_analysis", "column": "spend"}, {"table": "google_ads__customer_acquisition_analysis", "column": "date_day"}, {"table": "google_ads__customer_acquisition_analysis", "column": "date_day"}, {"table": "google_ads__customer_acquisition_analysis", "column": "date_day"}, {"table": "google_ads__customer_acquisition_analysis", "column": "conversions"}, {"table": "google_ads__customer_acquisition_analysis", "column": "date_day"}, {"table": "google_ads__customer_acquisition_analysis", "column": "date_day"}, {"table": "google_ads__customer_acquisition_analysis", "column": "date_day"}] | False |


## S62

类别 `data`；来源 `query_db`；调用 `2c97ecf3bf804844a96ced5d81a39e44`；状态 `success`。

```sql
WITH camp AS (
  SELECT campaign_id, campaign_name, account_id, account_name, advertising_channel_type, advertising_channel_subtype,
         MAX(substr(date_day,1,10)) AS last_date,
         CAST(julianday(MAX(substr(date_day,1,10))) - julianday(MIN(substr(date_day,1,10))) AS INTEGER) AS days_running
  FROM google_ads__campaign_report
  GROUP BY campaign_id
  HAVING days_running > 120
),
daily AS (
  SELECT c.campaign_id, substr(r.date_day,1,10) AS d, r.spend, r.conversions,
         julianday(substr(r.date_day,1,10)) AS jd
  FROM camp c
  JOIN google_ads__campaign_report r ON r.campaign_id = c.campaign_id
)
SELECT campaign_id,
       SUM(CASE WHEN jd >= julianday(last_date) - 29 THEN spend ELSE 0 END) AS spend_last,
       SUM(CASE WHEN jd >= julianday(last_date) - 29 THEN conversions ELSE 0 END) AS conv_last,
       SUM(CASE WHEN jd BETWEEN julianday(last_date) - 59 AND julianday(last_date) - 30 THEN spend ELSE 0 END) AS spend_prior,
       SUM(CASE WHEN jd BETWEEN julianday(last_date) - 59 AND julianday(last_date) - 30 THEN conversions ELSE 0 END) AS conv_prior,
       ROUND(SUM(CASE WHEN jd >= julianday(last_date) - 29 THEN spend ELSE 0 END)/NULLIF(SUM(CASE WHEN jd >= julianday(last_date) - 29 THEN conversions ELSE 0 END),0),2) AS cac_last,
       ROUND(SUM(CASE WHEN jd BETWEEN julianday(last_date) - 59 AND julianday(last_date) - 30 THEN spend ELSE 0 END)/NULLIF(SUM(CASE WHEN jd BETWEEN julianday(last_date) - 59 AND julianday(last_date) - 30 THEN conversions ELSE 0 END),0),2) AS cac_prior
FROM camp c
JOIN daily d USING (campaign_id)
GROUP BY campaign_id
ORDER BY cac_last DESC NULLS LAST
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-057/attempt-01/sql/S62.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-057/attempt-01/sql/S62.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-057/attempt-01/results/S62.rows.jsonl)；完整：True；SHA256：`1dfd246dc75db86336ea3fb286692896e4cf09d78cb8d18ea386c40066352e1c`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "google_ads__campaign_report", "kind": "base", "block": null, "base_tables": ["google_ads__campaign_report"]}] | [] | ["campaign_id"] |
| B2 | [{"alias": "c", "kind": "derived", "block": "B1", "base_tables": ["google_ads__campaign_report"]}, {"alias": "r", "kind": "base", "block": null, "base_tables": ["google_ads__campaign_report"]}] | [{"type": "INNER", "right": "google_ads__campaign_report AS r", "on": "r.campaign_id = c.campaign_id", "using": []}] | [] |
| B3 | [{"alias": "c", "kind": "derived", "block": "B1", "base_tables": ["google_ads__campaign_report"]}, {"alias": "d", "kind": "derived", "block": "B2", "base_tables": ["google_ads__campaign_report"]}] | [{"type": "INNER", "right": "daily AS d", "on": null, "using": ["campaign_id"]}] | ["campaign_id"] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | MAX(SUBSTRING(date_day, 1, 10)) | [{"table": "google_ads__campaign_report", "column": "date_day"}] | [] | False |
| B1 | MAX(SUBSTRING(date_day, 1, 10)) | [{"table": "google_ads__campaign_report", "column": "date_day"}] | [] | False |
| B1 | MIN(SUBSTRING(date_day, 1, 10)) | [{"table": "google_ads__campaign_report", "column": "date_day"}] | [] | False |
| B3 | SUM(CASE WHEN jd >= JULIANDAY(last_date) - 29 THEN spend ELSE 0 END) | [{"table": "google_ads__campaign_report", "column": "spend"}] | [{"table": "google_ads__campaign_report", "column": "date_day"}, {"table": "google_ads__campaign_report", "column": "date_day"}] | False |
| B3 | SUM(CASE WHEN jd >= JULIANDAY(last_date) - 29 THEN conversions ELSE 0 END) | [{"table": "google_ads__campaign_report", "column": "conversions"}] | [{"table": "google_ads__campaign_report", "column": "date_day"}, {"table": "google_ads__campaign_report", "column": "date_day"}] | False |
| B3 | SUM(CASE WHEN jd BETWEEN JULIANDAY(last_date) - 59 AND JULIANDAY(last_date) - 30 THEN spend ELSE 0 END) | [{"table": "google_ads__campaign_report", "column": "spend"}] | [{"table": "google_ads__campaign_report", "column": "date_day"}, {"table": "google_ads__campaign_report", "column": "date_day"}, {"table": "google_ads__campaign_report", "column": "date_day"}] | False |
| B3 | SUM(CASE WHEN jd BETWEEN JULIANDAY(last_date) - 59 AND JULIANDAY(last_date) - 30 THEN conversions ELSE 0 END) | [{"table": "google_ads__campaign_report", "column": "conversions"}] | [{"table": "google_ads__campaign_report", "column": "date_day"}, {"table": "google_ads__campaign_report", "column": "date_day"}, {"table": "google_ads__campaign_report", "column": "date_day"}] | False |
| B3 | SUM(CASE WHEN jd >= JULIANDAY(last_date) - 29 THEN spend ELSE 0 END) | [{"table": "google_ads__campaign_report", "column": "spend"}] | [{"table": "google_ads__campaign_report", "column": "date_day"}, {"table": "google_ads__campaign_report", "column": "date_day"}] | False |
| B3 | SUM(CASE WHEN jd BETWEEN JULIANDAY(last_date) - 59 AND JULIANDAY(last_date) - 30 THEN spend ELSE 0 END) | [{"table": "google_ads__campaign_report", "column": "spend"}] | [{"table": "google_ads__campaign_report", "column": "date_day"}, {"table": "google_ads__campaign_report", "column": "date_day"}, {"table": "google_ads__campaign_report", "column": "date_day"}] | False |
| B3 | SUM(CASE WHEN jd >= JULIANDAY(last_date) - 29 THEN conversions ELSE 0 END) | [{"table": "google_ads__campaign_report", "column": "conversions"}] | [{"table": "google_ads__campaign_report", "column": "date_day"}, {"table": "google_ads__campaign_report", "column": "date_day"}] | False |
| B3 | SUM(CASE WHEN jd BETWEEN JULIANDAY(last_date) - 59 AND JULIANDAY(last_date) - 30 THEN conversions ELSE 0 END) | [{"table": "google_ads__campaign_report", "column": "conversions"}] | [{"table": "google_ads__campaign_report", "column": "date_day"}, {"table": "google_ads__campaign_report", "column": "date_day"}, {"table": "google_ads__campaign_report", "column": "date_day"}] | False |


未解析列血缘：[{"block": "B3", "column": "campaign_id", "reason": "ambiguous_or_missing_source"}, {"block": "B3", "column": "campaign_id", "reason": "ambiguous_or_missing_source"}, {"block": "B3", "column": "campaign_id", "reason": "ambiguous_or_missing_source"}]

## S63

类别 `data`；来源 `query_db`；调用 `754e0b60ebc7477aa7a8379d54bbdaba`；状态 `failed`。

```sql
WITH camp AS (
  SELECT campaign_id, campaign_name, account_id, account_name, advertising_channel_type, advertising_channel_subtype,
         CAST(julianday(MAX(substr(date_day,1,10))) - julianday(MIN(substr(date_day,1,10))) AS INTEGER) AS days_running
  FROM google_ads__campaign_report
  GROUP BY campaign_id
  HAVING days_running > 120
),
joined AS (
  SELECT c.campaign_id, c.campaign_name, c.account_id, c.account_name, c.advertising_channel_type, c.advertising_channel_subtype,
         substr(a.date_day,1,10) AS d, a.customer_acquisition_cost, a.ltv_cac_ratio, a.spend, a.conversions,
         julianday(substr(a.date_day,1,10)) AS jd
  FROM camp c
  JOIN google_ads__customer_acquisition_analysis a
    ON a.account_id = c.account_id
   AND a.advertising_channel_type = c.advertising_channel_type
   AND COALESCE(a.advertising_channel_subtype,'') = COALESCE(c.advertising_channel_subtype,'')
   AND substr(a.date_day,1,10) BETWEEN c.first_date AND c.last_date
)
SELECT campaign_id, campaign_name, account_id, advertising_channel_type, advertising_channel_subtype,
       SUM(CASE WHEN jd >= julianday('2024-12-31') - 29 THEN spend ELSE 0 END) AS spend_last,
       SUM(CASE WHEN jd >= julianday('2024-12-31') - 29 THEN conversions ELSE 0 END) AS conv_last,
       SUM(CASE WHEN jd BETWEEN julianday('2024-12-31') - 59 AND julianday('2024-12-31') - 30 THEN spend ELSE 0 END) AS spend_prior,
       SUM(CASE WHEN jd BETWEEN julianday('2024-12-31') - 59 AND julianday('2024-12-31') - 30 THEN conversions ELSE 0 END) AS conv_prior,
       ROUND((SUM(CASE WHEN jd >= julianday('2024-12-31') - 29 THEN spend ELSE 0 END)/NULLIF(SUM(CASE WHEN jd >= julianday('2024-12-31') - 29 THEN conversions ELSE 0 END),0)),2) AS cac_last,
       ROUND((SUM(CASE WHEN jd BETWEEN julianday('2024-12-31') - 59 AND julianday('2024-12-31') - 30 THEN spend ELSE 0 END)/NULLIF(SUM(CASE WHEN jd BETWEEN julianday('2024-12-31') - 59 AND julianday('2024-12-31') - 30 THEN conversions ELSE 0 END),0)),2) AS cac_prior
FROM joined
GROUP BY campaign_id
ORDER BY cac_last DESC NULLS LAST
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-057/attempt-01/sql/S63.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-057/attempt-01/sql/S63.parameters.json)。

错误：`OperationalError('no such column: c.first_date')`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "google_ads__campaign_report", "kind": "base", "block": null, "base_tables": ["google_ads__campaign_report"]}] | [] | ["campaign_id"] |
| B2 | [{"alias": "c", "kind": "derived", "block": "B1", "base_tables": ["google_ads__campaign_report"]}, {"alias": "a", "kind": "base", "block": null, "base_tables": ["google_ads__customer_acquisition_analysis"]}] | [{"type": "INNER", "right": "google_ads__customer_acquisition_analysis AS a", "on": "a.account_id = c.account_id AND a.advertising_channel_type = c.advertising_channel_type AND COALESCE(a.advertising_channel_subtype, '') = COALESCE(c.advertising_channel_subtype, '') AND SUBSTRING(a.date_day, 1, 10) BETWEEN c.first_date AND c.last_date", "using": []}] | [] |
| B3 | [{"alias": "joined", "kind": "derived", "block": "B2", "base_tables": ["google_ads__campaign_report", "google_ads__customer_acquisition_analysis"]}] | [] | ["campaign_id"] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | MAX(SUBSTRING(date_day, 1, 10)) | [{"table": "google_ads__campaign_report", "column": "date_day"}] | [] | False |
| B1 | MIN(SUBSTRING(date_day, 1, 10)) | [{"table": "google_ads__campaign_report", "column": "date_day"}] | [] | False |
| B3 | SUM(CASE WHEN jd >= JULIANDAY('2024-12-31') - 29 THEN spend ELSE 0 END) | [{"table": "google_ads__customer_acquisition_analysis", "column": "spend"}] | [{"table": "google_ads__customer_acquisition_analysis", "column": "date_day"}] | False |
| B3 | SUM(CASE WHEN jd >= JULIANDAY('2024-12-31') - 29 THEN conversions ELSE 0 END) | [{"table": "google_ads__customer_acquisition_analysis", "column": "conversions"}] | [{"table": "google_ads__customer_acquisition_analysis", "column": "date_day"}] | False |
| B3 | SUM(CASE WHEN jd BETWEEN JULIANDAY('2024-12-31') - 59 AND JULIANDAY('2024-12-31') - 30 THEN spend ELSE 0 END) | [{"table": "google_ads__customer_acquisition_analysis", "column": "spend"}] | [{"table": "google_ads__customer_acquisition_analysis", "column": "date_day"}] | False |
| B3 | SUM(CASE WHEN jd BETWEEN JULIANDAY('2024-12-31') - 59 AND JULIANDAY('2024-12-31') - 30 THEN conversions ELSE 0 END) | [{"table": "google_ads__customer_acquisition_analysis", "column": "conversions"}] | [{"table": "google_ads__customer_acquisition_analysis", "column": "date_day"}] | False |
| B3 | SUM(CASE WHEN jd >= JULIANDAY('2024-12-31') - 29 THEN spend ELSE 0 END) | [{"table": "google_ads__customer_acquisition_analysis", "column": "spend"}] | [{"table": "google_ads__customer_acquisition_analysis", "column": "date_day"}] | False |
| B3 | SUM(CASE WHEN jd BETWEEN JULIANDAY('2024-12-31') - 59 AND JULIANDAY('2024-12-31') - 30 THEN spend ELSE 0 END) | [{"table": "google_ads__customer_acquisition_analysis", "column": "spend"}] | [{"table": "google_ads__customer_acquisition_analysis", "column": "date_day"}] | False |
| B3 | SUM(CASE WHEN jd >= JULIANDAY('2024-12-31') - 29 THEN conversions ELSE 0 END) | [{"table": "google_ads__customer_acquisition_analysis", "column": "conversions"}] | [{"table": "google_ads__customer_acquisition_analysis", "column": "date_day"}] | False |
| B3 | SUM(CASE WHEN jd BETWEEN JULIANDAY('2024-12-31') - 59 AND JULIANDAY('2024-12-31') - 30 THEN conversions ELSE 0 END) | [{"table": "google_ads__customer_acquisition_analysis", "column": "conversions"}] | [{"table": "google_ads__customer_acquisition_analysis", "column": "date_day"}] | False |


未解析列血缘：[{"column": "c.first_date", "reason": "derived_star_or_missing_output"}, {"column": "c.last_date", "reason": "derived_star_or_missing_output"}]

## S64

类别 `data`；来源 `query_db`；调用 `610831f171f64a6fabf0bc75366ae2cf`；状态 `success`。

```sql
WITH camp AS (
  SELECT campaign_id, campaign_name, account_id, account_name, advertising_channel_type, advertising_channel_subtype,
         MIN(substr(date_day,1,10)) AS first_date, MAX(substr(date_day,1,10)) AS last_date,
         CAST(julianday(MAX(substr(date_day,1,10))) - julianday(MIN(substr(date_day,1,10))) AS INTEGER) AS days_running
  FROM google_ads__campaign_report
  GROUP BY campaign_id
  HAVING days_running > 120
),
joined AS (
  SELECT c.campaign_id, c.campaign_name, c.account_id, c.account_name, c.advertising_channel_type, c.advertising_channel_subtype,
         substr(a.date_day,1,10) AS d, a.customer_acquisition_cost, a.ltv_cac_ratio, a.spend, a.conversions,
         julianday(substr(a.date_day,1,10)) AS jd
  FROM camp c
  JOIN google_ads__customer_acquisition_analysis a
    ON a.account_id = c.account_id
   AND a.advertising_channel_type = c.advertising_channel_type
   AND COALESCE(a.advertising_channel_subtype,'') = COALESCE(c.advertising_channel_subtype,'')
   AND substr(a.date_day,1,10) BETWEEN c.first_date AND c.last_date
)
SELECT campaign_id, campaign_name, account_id, advertising_channel_type, advertising_channel_subtype,
       SUM(CASE WHEN jd >= julianday('2024-12-31') - 29 THEN spend ELSE 0 END) AS spend_last,
       SUM(CASE WHEN jd >= julianday('2024-12-31') - 29 THEN conversions ELSE 0 END) AS conv_last,
       SUM(CASE WHEN jd BETWEEN julianday('2024-12-31') - 59 AND julianday('2024-12-31') - 30 THEN spend ELSE 0 END) AS spend_prior,
       SUM(CASE WHEN jd BETWEEN julianday('2024-12-31') - 59 AND julianday('2024-12-31') - 30 THEN conversions ELSE 0 END) AS conv_prior,
       ROUND(SUM(CASE WHEN jd >= julianday('2024-12-31') - 29 THEN spend ELSE 0 END)/NULLIF(SUM(CASE WHEN jd >= julianday('2024-12-31') - 29 THEN conversions ELSE 0 END),0),2) AS cac_last,
       ROUND(SUM(CASE WHEN jd BETWEEN julianday('2024-12-31') - 59 AND julianday('2024-12-31') - 30 THEN spend ELSE 0 END)/NULLIF(SUM(CASE WHEN jd BETWEEN julianday('2024-12-31') - 59 AND julianday('2024-12-31') - 30 THEN conversions ELSE 0 END),0),2) AS cac_prior
FROM joined
GROUP BY campaign_id
ORDER BY cac_last DESC NULLS LAST
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-057/attempt-01/sql/S64.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-057/attempt-01/sql/S64.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-057/attempt-01/results/S64.rows.jsonl)；完整：True；SHA256：`47330465d0e303679ed08cd25c6c5a603ba028fdf29d8351789b1b724fb12ccc`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "google_ads__campaign_report", "kind": "base", "block": null, "base_tables": ["google_ads__campaign_report"]}] | [] | ["campaign_id"] |
| B2 | [{"alias": "c", "kind": "derived", "block": "B1", "base_tables": ["google_ads__campaign_report"]}, {"alias": "a", "kind": "base", "block": null, "base_tables": ["google_ads__customer_acquisition_analysis"]}] | [{"type": "INNER", "right": "google_ads__customer_acquisition_analysis AS a", "on": "a.account_id = c.account_id AND a.advertising_channel_type = c.advertising_channel_type AND COALESCE(a.advertising_channel_subtype, '') = COALESCE(c.advertising_channel_subtype, '') AND SUBSTRING(a.date_day, 1, 10) BETWEEN c.first_date AND c.last_date", "using": []}] | [] |
| B3 | [{"alias": "joined", "kind": "derived", "block": "B2", "base_tables": ["google_ads__campaign_report", "google_ads__customer_acquisition_analysis"]}] | [] | ["campaign_id"] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | MIN(SUBSTRING(date_day, 1, 10)) | [{"table": "google_ads__campaign_report", "column": "date_day"}] | [] | False |
| B1 | MAX(SUBSTRING(date_day, 1, 10)) | [{"table": "google_ads__campaign_report", "column": "date_day"}] | [] | False |
| B1 | MAX(SUBSTRING(date_day, 1, 10)) | [{"table": "google_ads__campaign_report", "column": "date_day"}] | [] | False |
| B1 | MIN(SUBSTRING(date_day, 1, 10)) | [{"table": "google_ads__campaign_report", "column": "date_day"}] | [] | False |
| B3 | SUM(CASE WHEN jd >= JULIANDAY('2024-12-31') - 29 THEN spend ELSE 0 END) | [{"table": "google_ads__customer_acquisition_analysis", "column": "spend"}] | [{"table": "google_ads__customer_acquisition_analysis", "column": "date_day"}] | False |
| B3 | SUM(CASE WHEN jd >= JULIANDAY('2024-12-31') - 29 THEN conversions ELSE 0 END) | [{"table": "google_ads__customer_acquisition_analysis", "column": "conversions"}] | [{"table": "google_ads__customer_acquisition_analysis", "column": "date_day"}] | False |
| B3 | SUM(CASE WHEN jd BETWEEN JULIANDAY('2024-12-31') - 59 AND JULIANDAY('2024-12-31') - 30 THEN spend ELSE 0 END) | [{"table": "google_ads__customer_acquisition_analysis", "column": "spend"}] | [{"table": "google_ads__customer_acquisition_analysis", "column": "date_day"}] | False |
| B3 | SUM(CASE WHEN jd BETWEEN JULIANDAY('2024-12-31') - 59 AND JULIANDAY('2024-12-31') - 30 THEN conversions ELSE 0 END) | [{"table": "google_ads__customer_acquisition_analysis", "column": "conversions"}] | [{"table": "google_ads__customer_acquisition_analysis", "column": "date_day"}] | False |
| B3 | SUM(CASE WHEN jd >= JULIANDAY('2024-12-31') - 29 THEN spend ELSE 0 END) | [{"table": "google_ads__customer_acquisition_analysis", "column": "spend"}] | [{"table": "google_ads__customer_acquisition_analysis", "column": "date_day"}] | False |
| B3 | SUM(CASE WHEN jd BETWEEN JULIANDAY('2024-12-31') - 59 AND JULIANDAY('2024-12-31') - 30 THEN spend ELSE 0 END) | [{"table": "google_ads__customer_acquisition_analysis", "column": "spend"}] | [{"table": "google_ads__customer_acquisition_analysis", "column": "date_day"}] | False |
| B3 | SUM(CASE WHEN jd >= JULIANDAY('2024-12-31') - 29 THEN conversions ELSE 0 END) | [{"table": "google_ads__customer_acquisition_analysis", "column": "conversions"}] | [{"table": "google_ads__customer_acquisition_analysis", "column": "date_day"}] | False |
| B3 | SUM(CASE WHEN jd BETWEEN JULIANDAY('2024-12-31') - 59 AND JULIANDAY('2024-12-31') - 30 THEN conversions ELSE 0 END) | [{"table": "google_ads__customer_acquisition_analysis", "column": "conversions"}] | [{"table": "google_ads__customer_acquisition_analysis", "column": "date_day"}] | False |


## S65

类别 `data`；来源 `query_db`；调用 `b4814a7faeeb468a98bd66642eaa61e8`；状态 `success`。

```sql
WITH camp AS (
  SELECT campaign_id, campaign_name, account_id, account_name, advertising_channel_type, advertising_channel_subtype,
         MIN(substr(date_day,1,10)) AS first_date, MAX(substr(date_day,1,10)) AS last_date,
         CAST(julianday(MAX(substr(date_day,1,10))) - julianday(MIN(substr(date_day,1,10))) AS INTEGER) AS days_running
  FROM google_ads__campaign_report
  GROUP BY campaign_id
  HAVING days_running > 120
),
joined AS (
  SELECT c.campaign_id, c.campaign_name, c.account_id, c.account_name, c.advertising_channel_type, c.advertising_channel_subtype,
         substr(a.date_day,1,10) AS d, a.customer_acquisition_cost, a.ltv_cac_ratio, a.spend, a.conversions,
         julianday(substr(a.date_day,1,10)) AS jd
  FROM camp c
  JOIN google_ads__customer_acquisition_analysis a
    ON a.account_id = c.account_id
   AND a.advertising_channel_type = c.advertising_channel_type
   AND COALESCE(a.advertising_channel_subtype,'') = COALESCE(c.advertising_channel_subtype,'')
   AND substr(a.date_day,1,10) BETWEEN c.first_date AND c.last_date
)
SELECT campaign_id, campaign_name, account_id, advertising_channel_type, advertising_channel_subtype,
       SUM(CASE WHEN jd >= julianday('2024-12-31') - 29 THEN conversions ELSE 0 END) AS conv_last,
       SUM(CASE WHEN jd BETWEEN julianday('2024-12-31') - 59 AND julianday('2024-12-31') - 30 THEN conversions ELSE 0 END) AS conv_prior
FROM joined
GROUP BY campaign_id
HAVING conv_last > 0 AND conv_prior > 0
ORDER BY conv_last DESC
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-057/attempt-01/sql/S65.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-057/attempt-01/sql/S65.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-057/attempt-01/results/S65.rows.jsonl)；完整：True；SHA256：`f953482c36c41756ac5271b874938cd55de20a501ab9400ad819d4621d626ce0`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "google_ads__campaign_report", "kind": "base", "block": null, "base_tables": ["google_ads__campaign_report"]}] | [] | ["campaign_id"] |
| B2 | [{"alias": "c", "kind": "derived", "block": "B1", "base_tables": ["google_ads__campaign_report"]}, {"alias": "a", "kind": "base", "block": null, "base_tables": ["google_ads__customer_acquisition_analysis"]}] | [{"type": "INNER", "right": "google_ads__customer_acquisition_analysis AS a", "on": "a.account_id = c.account_id AND a.advertising_channel_type = c.advertising_channel_type AND COALESCE(a.advertising_channel_subtype, '') = COALESCE(c.advertising_channel_subtype, '') AND SUBSTRING(a.date_day, 1, 10) BETWEEN c.first_date AND c.last_date", "using": []}] | [] |
| B3 | [{"alias": "joined", "kind": "derived", "block": "B2", "base_tables": ["google_ads__campaign_report", "google_ads__customer_acquisition_analysis"]}] | [] | ["campaign_id"] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | MIN(SUBSTRING(date_day, 1, 10)) | [{"table": "google_ads__campaign_report", "column": "date_day"}] | [] | False |
| B1 | MAX(SUBSTRING(date_day, 1, 10)) | [{"table": "google_ads__campaign_report", "column": "date_day"}] | [] | False |
| B1 | MAX(SUBSTRING(date_day, 1, 10)) | [{"table": "google_ads__campaign_report", "column": "date_day"}] | [] | False |
| B1 | MIN(SUBSTRING(date_day, 1, 10)) | [{"table": "google_ads__campaign_report", "column": "date_day"}] | [] | False |
| B3 | SUM(CASE WHEN jd >= JULIANDAY('2024-12-31') - 29 THEN conversions ELSE 0 END) | [{"table": "google_ads__customer_acquisition_analysis", "column": "conversions"}] | [{"table": "google_ads__customer_acquisition_analysis", "column": "date_day"}] | False |
| B3 | SUM(CASE WHEN jd BETWEEN JULIANDAY('2024-12-31') - 59 AND JULIANDAY('2024-12-31') - 30 THEN conversions ELSE 0 END) | [{"table": "google_ads__customer_acquisition_analysis", "column": "conversions"}] | [{"table": "google_ads__customer_acquisition_analysis", "column": "date_day"}] | False |


## S66

类别 `data`；来源 `query_db`；调用 `b1a0a7cb3ec84703af8445e57e9aa500`；状态 `success`。

```sql
WITH camp AS (
  SELECT campaign_id, campaign_name, account_id, account_name, advertising_channel_type, advertising_channel_subtype,
         MIN(substr(date_day,1,10)) AS first_date, MAX(substr(date_day,1,10)) AS last_date,
         CAST(julianday(MAX(substr(date_day,1,10))) - julianday(MIN(substr(date_day,1,10))) AS INTEGER) AS days_running
  FROM google_ads__campaign_report
  GROUP BY campaign_id
  HAVING days_running > 120
),
joined AS (
  SELECT c.campaign_id, c.campaign_name, c.account_id, c.account_name, c.advertising_channel_type, c.advertising_channel_subtype,
         substr(a.date_day,1,10) AS d, a.customer_acquisition_cost, a.ltv_cac_ratio, a.spend, a.conversions,
         julianday(substr(a.date_day,1,10)) AS jd
  FROM camp c
  JOIN google_ads__customer_acquisition_analysis a
    ON a.account_id = c.account_id
   AND a.advertising_channel_type = c.advertising_channel_type
   AND COALESCE(a.advertising_channel_subtype,'') = COALESCE(c.advertising_channel_subtype,'')
   AND substr(a.date_day,1,10) BETWEEN c.first_date AND c.last_date
)
SELECT campaign_id, campaign_name, account_id, advertising_channel_type, advertising_channel_subtype,
       ROUND(SUM(CASE WHEN jd >= julianday('2024-12-31') - 29 THEN spend ELSE 0 END)/NULLIF(SUM(CASE WHEN jd >= julianday('2024-12-31') - 29 THEN conversions ELSE 0 END),0),2) AS cac_last,
       ROUND(SUM(CASE WHEN jd BETWEEN julianday('2024-12-31') - 59 AND julianday('2024-12-31') - 30 THEN spend ELSE 0 END)/NULLIF(SUM(CASE WHEN jd BETWEEN julianday('2024-12-31') - 59 AND julianday('2024-12-31') - 30 THEN conversions ELSE 0 END),0),2) AS cac_prior,
       ROUND(SUM(CASE WHEN jd >= julianday('2024-12-31') - 29 THEN conversions*ltv_cac_ratio ELSE 0 END)/NULLIF(SUM(CASE WHEN jd >= julianday('2024-12-31') - 29 THEN conversions ELSE 0 END),0),2) AS ltv_cac_last,
       ROUND(SUM(CASE WHEN jd BETWEEN julianday('2024-12-31') - 59 AND julianday('2024-12-31') - 30 THEN conversions*ltv_cac_ratio ELSE 0 END)/NULLIF(SUM(CASE WHEN jd BETWEEN julianday('2024-12-31') - 59 AND julianday('2024-12-31') - 30 THEN conversions ELSE 0 END),0),2) AS ltv_cac_prior
FROM joined
GROUP BY campaign_id
HAVING SUM(CASE WHEN jd >= julianday('2024-12-31') - 29 THEN conversions ELSE 0 END) > 0
   AND SUM(CASE WHEN jd BETWEEN julianday('2024-12-31') - 59 AND julianday('2024-12-31') - 30 THEN conversions ELSE 0 END) > 0
ORDER BY campaign_id
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-057/attempt-01/sql/S66.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-057/attempt-01/sql/S66.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-057/attempt-01/results/S66.rows.jsonl)；完整：True；SHA256：`34de3c146dc94d62a9142b2ed33d1d7e86e4115f295d46041c99beb9f52da6c1`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "google_ads__campaign_report", "kind": "base", "block": null, "base_tables": ["google_ads__campaign_report"]}] | [] | ["campaign_id"] |
| B2 | [{"alias": "c", "kind": "derived", "block": "B1", "base_tables": ["google_ads__campaign_report"]}, {"alias": "a", "kind": "base", "block": null, "base_tables": ["google_ads__customer_acquisition_analysis"]}] | [{"type": "INNER", "right": "google_ads__customer_acquisition_analysis AS a", "on": "a.account_id = c.account_id AND a.advertising_channel_type = c.advertising_channel_type AND COALESCE(a.advertising_channel_subtype, '') = COALESCE(c.advertising_channel_subtype, '') AND SUBSTRING(a.date_day, 1, 10) BETWEEN c.first_date AND c.last_date", "using": []}] | [] |
| B3 | [{"alias": "joined", "kind": "derived", "block": "B2", "base_tables": ["google_ads__campaign_report", "google_ads__customer_acquisition_analysis"]}] | [] | ["campaign_id"] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | MIN(SUBSTRING(date_day, 1, 10)) | [{"table": "google_ads__campaign_report", "column": "date_day"}] | [] | False |
| B1 | MAX(SUBSTRING(date_day, 1, 10)) | [{"table": "google_ads__campaign_report", "column": "date_day"}] | [] | False |
| B1 | MAX(SUBSTRING(date_day, 1, 10)) | [{"table": "google_ads__campaign_report", "column": "date_day"}] | [] | False |
| B1 | MIN(SUBSTRING(date_day, 1, 10)) | [{"table": "google_ads__campaign_report", "column": "date_day"}] | [] | False |
| B3 | SUM(CASE WHEN jd >= JULIANDAY('2024-12-31') - 29 THEN spend ELSE 0 END) | [{"table": "google_ads__customer_acquisition_analysis", "column": "spend"}] | [{"table": "google_ads__customer_acquisition_analysis", "column": "date_day"}] | False |
| B3 | SUM(CASE WHEN jd BETWEEN JULIANDAY('2024-12-31') - 59 AND JULIANDAY('2024-12-31') - 30 THEN spend ELSE 0 END) | [{"table": "google_ads__customer_acquisition_analysis", "column": "spend"}] | [{"table": "google_ads__customer_acquisition_analysis", "column": "date_day"}] | False |
| B3 | SUM(CASE WHEN jd >= JULIANDAY('2024-12-31') - 29 THEN conversions * ltv_cac_ratio ELSE 0 END) | [{"table": "google_ads__customer_acquisition_analysis", "column": "conversions"}, {"table": "google_ads__customer_acquisition_analysis", "column": "ltv_cac_ratio"}] | [{"table": "google_ads__customer_acquisition_analysis", "column": "date_day"}] | False |
| B3 | SUM(CASE WHEN jd BETWEEN JULIANDAY('2024-12-31') - 59 AND JULIANDAY('2024-12-31') - 30 THEN conversions * ltv_cac_ratio ELSE 0 END) | [{"table": "google_ads__customer_acquisition_analysis", "column": "conversions"}, {"table": "google_ads__customer_acquisition_analysis", "column": "ltv_cac_ratio"}] | [{"table": "google_ads__customer_acquisition_analysis", "column": "date_day"}] | False |
| B3 | SUM(CASE WHEN jd >= JULIANDAY('2024-12-31') - 29 THEN conversions ELSE 0 END) | [{"table": "google_ads__customer_acquisition_analysis", "column": "conversions"}] | [{"table": "google_ads__customer_acquisition_analysis", "column": "date_day"}] | False |
| B3 | SUM(CASE WHEN jd BETWEEN JULIANDAY('2024-12-31') - 59 AND JULIANDAY('2024-12-31') - 30 THEN conversions ELSE 0 END) | [{"table": "google_ads__customer_acquisition_analysis", "column": "conversions"}] | [{"table": "google_ads__customer_acquisition_analysis", "column": "date_day"}] | False |
| B3 | SUM(CASE WHEN jd >= JULIANDAY('2024-12-31') - 29 THEN conversions ELSE 0 END) | [{"table": "google_ads__customer_acquisition_analysis", "column": "conversions"}] | [{"table": "google_ads__customer_acquisition_analysis", "column": "date_day"}] | False |
| B3 | SUM(CASE WHEN jd BETWEEN JULIANDAY('2024-12-31') - 59 AND JULIANDAY('2024-12-31') - 30 THEN conversions ELSE 0 END) | [{"table": "google_ads__customer_acquisition_analysis", "column": "conversions"}] | [{"table": "google_ads__customer_acquisition_analysis", "column": "date_day"}] | False |
| B3 | SUM(CASE WHEN jd >= JULIANDAY('2024-12-31') - 29 THEN conversions ELSE 0 END) | [{"table": "google_ads__customer_acquisition_analysis", "column": "conversions"}] | [{"table": "google_ads__customer_acquisition_analysis", "column": "date_day"}] | False |
| B3 | SUM(CASE WHEN jd BETWEEN JULIANDAY('2024-12-31') - 59 AND JULIANDAY('2024-12-31') - 30 THEN conversions ELSE 0 END) | [{"table": "google_ads__customer_acquisition_analysis", "column": "conversions"}] | [{"table": "google_ads__customer_acquisition_analysis", "column": "date_day"}] | False |


## S67

类别 `data`；来源 `query_db`；调用 `b057be09b6484ec4b157ea7228287d8f`；状态 `success`。

```sql
WITH camp AS (
  SELECT campaign_id, campaign_name, account_id, account_name, advertising_channel_type, advertising_channel_subtype,
         MIN(substr(date_day,1,10)) AS first_date, MAX(substr(date_day,1,10)) AS last_date,
         CAST(julianday(MAX(substr(date_day,1,10))) - julianday(MIN(substr(date_day,1,10))) AS INTEGER) AS days_running
  FROM google_ads__campaign_report
  GROUP BY campaign_id
  HAVING days_running > 120
),
joined AS (
  SELECT c.campaign_id, c.campaign_name, c.account_id, c.account_name, c.advertising_channel_type, c.advertising_channel_subtype,
         substr(a.date_day,1,10) AS d, a.customer_acquisition_cost, a.ltv_cac_ratio, a.spend, a.conversions,
         julianday(substr(a.date_day,1,10)) AS jd
  FROM camp c
  JOIN google_ads__customer_acquisition_analysis a
    ON a.account_id = c.account_id
   AND a.advertising_channel_type = c.advertising_channel_type
   AND COALESCE(a.advertising_channel_subtype,'') = COALESCE(c.advertising_channel_subtype,'')
   AND substr(a.date_day,1,10) BETWEEN c.first_date AND c.last_date
),
metrics AS (
  SELECT campaign_id, campaign_name, account_id, account_name, advertising_channel_type, advertising_channel_subtype,
         SUM(CASE WHEN jd >= julianday('2024-12-31') - 29 THEN spend ELSE 0 END) AS spend_last,
         SUM(CASE WHEN jd >= julianday('2024-12-31') - 29 THEN conversions ELSE 0 END) AS conv_last,
         SUM(CASE WHEN jd BETWEEN julianday('2024-12-31') - 59 AND julianday('2024-12-31') - 30 THEN spend ELSE 0 END) AS spend_prior,
         SUM(CASE WHEN jd BETWEEN julianday('2024-12-31') - 59 AND julianday('2024-12-31') - 30 THEN conversions ELSE 0 END) AS conv_prior,
         SUM(CASE WHEN jd >= julianday('2024-12-31') - 29 THEN conversions*ltv_cac_ratio ELSE 0 END) AS ltv_cac_w_last,
         SUM(CASE WHEN jd BETWEEN julianday('2024-12-31') - 59 AND julianday('2024-12-31') - 30 THEN conversions*ltv_cac_ratio ELSE 0 END) AS ltv_cac_w_prior
  FROM joined
  GROUP BY campaign_id
  HAVING conv_last > 0 AND conv_prior > 0
)
SELECT campaign_id, campaign_name, account_id, advertising_channel_type, advertising_channel_subtype,
       ROUND((spend_last/conv_last - spend_prior/conv_prior)/(spend_prior/conv_prior),4) AS cac_growth,
       ROUND((ltv_cac_w_last/conv_last - ltv_cac_w_prior/conv_prior)/(ltv_cac_w_prior/conv_prior),4) AS ltv_cac_change,
       CASE WHEN (spend_last/conv_last - spend_prior/conv_prior)/(spend_prior/conv_prior) > 0.25 
            AND (ltv_cac_w_last/conv_last - ltv_cac_w_prior/conv_prior)/(ltv_cac_w_prior/conv_prior) < -0.20
       THEN 'DECAY_FLAG' ELSE 'ok' END AS status
FROM metrics
ORDER BY (spend_last/conv_last - spend_prior/conv_prior)/(spend_prior/conv_prior) DESC
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-057/attempt-01/sql/S67.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-057/attempt-01/sql/S67.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-057/attempt-01/results/S67.rows.jsonl)；完整：True；SHA256：`cdccaf0421d18e129573c2c7318bc6c4dc8733809f8b1e311a6073da5fe84846`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "google_ads__campaign_report", "kind": "base", "block": null, "base_tables": ["google_ads__campaign_report"]}] | [] | ["campaign_id"] |
| B2 | [{"alias": "c", "kind": "derived", "block": "B1", "base_tables": ["google_ads__campaign_report"]}, {"alias": "a", "kind": "base", "block": null, "base_tables": ["google_ads__customer_acquisition_analysis"]}] | [{"type": "INNER", "right": "google_ads__customer_acquisition_analysis AS a", "on": "a.account_id = c.account_id AND a.advertising_channel_type = c.advertising_channel_type AND COALESCE(a.advertising_channel_subtype, '') = COALESCE(c.advertising_channel_subtype, '') AND SUBSTRING(a.date_day, 1, 10) BETWEEN c.first_date AND c.last_date", "using": []}] | [] |
| B3 | [{"alias": "joined", "kind": "derived", "block": "B2", "base_tables": ["google_ads__campaign_report", "google_ads__customer_acquisition_analysis"]}] | [] | ["campaign_id"] |
| B4 | [{"alias": "metrics", "kind": "derived", "block": "B3", "base_tables": ["google_ads__campaign_report", "google_ads__customer_acquisition_analysis"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | MIN(SUBSTRING(date_day, 1, 10)) | [{"table": "google_ads__campaign_report", "column": "date_day"}] | [] | False |
| B1 | MAX(SUBSTRING(date_day, 1, 10)) | [{"table": "google_ads__campaign_report", "column": "date_day"}] | [] | False |
| B1 | MAX(SUBSTRING(date_day, 1, 10)) | [{"table": "google_ads__campaign_report", "column": "date_day"}] | [] | False |
| B1 | MIN(SUBSTRING(date_day, 1, 10)) | [{"table": "google_ads__campaign_report", "column": "date_day"}] | [] | False |
| B3 | SUM(CASE WHEN jd >= JULIANDAY('2024-12-31') - 29 THEN spend ELSE 0 END) | [{"table": "google_ads__customer_acquisition_analysis", "column": "spend"}] | [{"table": "google_ads__customer_acquisition_analysis", "column": "date_day"}] | False |
| B3 | SUM(CASE WHEN jd >= JULIANDAY('2024-12-31') - 29 THEN conversions ELSE 0 END) | [{"table": "google_ads__customer_acquisition_analysis", "column": "conversions"}] | [{"table": "google_ads__customer_acquisition_analysis", "column": "date_day"}] | False |
| B3 | SUM(CASE WHEN jd BETWEEN JULIANDAY('2024-12-31') - 59 AND JULIANDAY('2024-12-31') - 30 THEN spend ELSE 0 END) | [{"table": "google_ads__customer_acquisition_analysis", "column": "spend"}] | [{"table": "google_ads__customer_acquisition_analysis", "column": "date_day"}] | False |
| B3 | SUM(CASE WHEN jd BETWEEN JULIANDAY('2024-12-31') - 59 AND JULIANDAY('2024-12-31') - 30 THEN conversions ELSE 0 END) | [{"table": "google_ads__customer_acquisition_analysis", "column": "conversions"}] | [{"table": "google_ads__customer_acquisition_analysis", "column": "date_day"}] | False |
| B3 | SUM(CASE WHEN jd >= JULIANDAY('2024-12-31') - 29 THEN conversions * ltv_cac_ratio ELSE 0 END) | [{"table": "google_ads__customer_acquisition_analysis", "column": "conversions"}, {"table": "google_ads__customer_acquisition_analysis", "column": "ltv_cac_ratio"}] | [{"table": "google_ads__customer_acquisition_analysis", "column": "date_day"}] | False |
| B3 | SUM(CASE WHEN jd BETWEEN JULIANDAY('2024-12-31') - 59 AND JULIANDAY('2024-12-31') - 30 THEN conversions * ltv_cac_ratio ELSE 0 END) | [{"table": "google_ads__customer_acquisition_analysis", "column": "conversions"}, {"table": "google_ads__customer_acquisition_analysis", "column": "ltv_cac_ratio"}] | [{"table": "google_ads__customer_acquisition_analysis", "column": "date_day"}] | False |


## S68

类别 `data`；来源 `query_db`；调用 `5d9a12731ffb47be9d89a021d61fba29`；状态 `failed`。

```sql
WITH camp AS (
  SELECT campaign_id, campaign_name, account_id, account_name, advertising_channel_type, advertising_channel_subtype,
         MAX(substr(date_day,1,10)) AS last_date,
         CAST(julianday(MAX(substr(date_day,1,10))) - julianday(MIN(substr(date_day,1,10))) AS INTEGER) AS days_running
  FROM google_ads__campaign_report
  GROUP BY campaign_id
  HAVING days_running > 120
),
joined AS (
  SELECT c.campaign_id, c.campaign_name, c.account_id, c.account_name, c.advertising_channel_type, c.advertising_channel_subtype,
         substr(a.date_day,1,10) AS d, a.customer_acquisition_cost, a.ltv_cac_ratio, a.spend, a.conversions,
         julianday(substr(a.date_day,1,10)) AS jd, julianday(c.last_date) AS ref_jd
  FROM camp c
  JOIN google_ads__customer_acquisition_analysis a
    ON a.account_id = c.account_id
   AND a.advertising_channel_type = c.advertising_channel_type
   AND COALESCE(a.advertising_channel_subtype,'') = COALESCE(c.advertising_channel_subtype,'')
   AND substr(a.date_day,1,10) BETWEEN c.first_date AND c.last_date
),
metrics AS (
  SELECT campaign_id, campaign_name, account_id, account_name, advertising_channel_type, advertising_channel_subtype,
         SUM(CASE WHEN jd >= ref_jd - 29 THEN spend ELSE 0 END) AS spend_last,
         SUM(CASE WHEN jd >= ref_jd - 29 THEN conversions ELSE 0 END) AS conv_last,
         SUM(CASE WHEN jd BETWEEN ref_jd - 59 AND ref_jd - 30 THEN spend ELSE 0 END) AS spend_prior,
         SUM(CASE WHEN jd BETWEEN ref_jd - 59 AND ref_jd - 30 THEN conversions ELSE 0 END) AS conv_prior,
         SUM(CASE WHEN jd >= ref_jd - 29 THEN conversions*ltv_cac_ratio ELSE 0 END) AS ltv_cac_w_last,
         SUM(CASE WHEN jd BETWEEN ref_jd - 59 AND ref_jd - 30 THEN conversions*ltv_cac_ratio ELSE 0 END) AS ltv_cac_w_prior
  FROM joined
  GROUP BY campaign_id
  HAVING conv_last > 0 AND conv_prior > 0
)
SELECT campaign_id, campaign_name, account_id, advertising_channel_type, advertising_channel_subtype,
       ROUND((spend_last/conv_last - spend_prior/conv_prior)/(spend_prior/conv_prior),4) AS cac_growth,
       ROUND((ltv_cac_w_last/conv_last - ltv_cac_w_prior/conv_prior)/(ltv_cac_w_prior/conv_prior),4) AS ltv_cac_change,
       CASE WHEN (spend_last/conv_last - spend_prior/conv_prior)/(spend_prior/conv_prior) > 0.25 
            AND (ltv_cac_w_last/conv_last - ltv_cac_w_prior/conv_prior)/(ltv_cac_w_prior/conv_prior) < -0.20
       THEN 'DECAY_FLAG' ELSE 'ok' END AS status
FROM metrics
ORDER BY (spend_last/conv_last - spend_prior/conv_prior)/(spend_prior/conv_prior) DESC
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-057/attempt-01/sql/S68.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-057/attempt-01/sql/S68.parameters.json)。

错误：`OperationalError('no such column: c.first_date')`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "google_ads__campaign_report", "kind": "base", "block": null, "base_tables": ["google_ads__campaign_report"]}] | [] | ["campaign_id"] |
| B2 | [{"alias": "c", "kind": "derived", "block": "B1", "base_tables": ["google_ads__campaign_report"]}, {"alias": "a", "kind": "base", "block": null, "base_tables": ["google_ads__customer_acquisition_analysis"]}] | [{"type": "INNER", "right": "google_ads__customer_acquisition_analysis AS a", "on": "a.account_id = c.account_id AND a.advertising_channel_type = c.advertising_channel_type AND COALESCE(a.advertising_channel_subtype, '') = COALESCE(c.advertising_channel_subtype, '') AND SUBSTRING(a.date_day, 1, 10) BETWEEN c.first_date AND c.last_date", "using": []}] | [] |
| B3 | [{"alias": "joined", "kind": "derived", "block": "B2", "base_tables": ["google_ads__campaign_report", "google_ads__customer_acquisition_analysis"]}] | [] | ["campaign_id"] |
| B4 | [{"alias": "metrics", "kind": "derived", "block": "B3", "base_tables": ["google_ads__campaign_report", "google_ads__customer_acquisition_analysis"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | MAX(SUBSTRING(date_day, 1, 10)) | [{"table": "google_ads__campaign_report", "column": "date_day"}] | [] | False |
| B1 | MAX(SUBSTRING(date_day, 1, 10)) | [{"table": "google_ads__campaign_report", "column": "date_day"}] | [] | False |
| B1 | MIN(SUBSTRING(date_day, 1, 10)) | [{"table": "google_ads__campaign_report", "column": "date_day"}] | [] | False |
| B3 | SUM(CASE WHEN jd >= ref_jd - 29 THEN spend ELSE 0 END) | [{"table": "google_ads__customer_acquisition_analysis", "column": "spend"}] | [{"table": "google_ads__customer_acquisition_analysis", "column": "date_day"}, {"table": "google_ads__campaign_report", "column": "date_day"}] | False |
| B3 | SUM(CASE WHEN jd >= ref_jd - 29 THEN conversions ELSE 0 END) | [{"table": "google_ads__customer_acquisition_analysis", "column": "conversions"}] | [{"table": "google_ads__customer_acquisition_analysis", "column": "date_day"}, {"table": "google_ads__campaign_report", "column": "date_day"}] | False |
| B3 | SUM(CASE WHEN jd BETWEEN ref_jd - 59 AND ref_jd - 30 THEN spend ELSE 0 END) | [{"table": "google_ads__customer_acquisition_analysis", "column": "spend"}] | [{"table": "google_ads__customer_acquisition_analysis", "column": "date_day"}, {"table": "google_ads__campaign_report", "column": "date_day"}, {"table": "google_ads__campaign_report", "column": "date_day"}] | False |
| B3 | SUM(CASE WHEN jd BETWEEN ref_jd - 59 AND ref_jd - 30 THEN conversions ELSE 0 END) | [{"table": "google_ads__customer_acquisition_analysis", "column": "conversions"}] | [{"table": "google_ads__customer_acquisition_analysis", "column": "date_day"}, {"table": "google_ads__campaign_report", "column": "date_day"}, {"table": "google_ads__campaign_report", "column": "date_day"}] | False |
| B3 | SUM(CASE WHEN jd >= ref_jd - 29 THEN conversions * ltv_cac_ratio ELSE 0 END) | [{"table": "google_ads__customer_acquisition_analysis", "column": "conversions"}, {"table": "google_ads__customer_acquisition_analysis", "column": "ltv_cac_ratio"}] | [{"table": "google_ads__customer_acquisition_analysis", "column": "date_day"}, {"table": "google_ads__campaign_report", "column": "date_day"}] | False |
| B3 | SUM(CASE WHEN jd BETWEEN ref_jd - 59 AND ref_jd - 30 THEN conversions * ltv_cac_ratio ELSE 0 END) | [{"table": "google_ads__customer_acquisition_analysis", "column": "conversions"}, {"table": "google_ads__customer_acquisition_analysis", "column": "ltv_cac_ratio"}] | [{"table": "google_ads__customer_acquisition_analysis", "column": "date_day"}, {"table": "google_ads__campaign_report", "column": "date_day"}, {"table": "google_ads__campaign_report", "column": "date_day"}] | False |


未解析列血缘：[{"column": "c.first_date", "reason": "derived_star_or_missing_output"}]

## S69

类别 `data`；来源 `query_db`；调用 `1645da72354a407e99ce723a6a46150e`；状态 `success`。

```sql
WITH camp AS (
  SELECT campaign_id, campaign_name, account_id, account_name, advertising_channel_type, advertising_channel_subtype,
         MIN(substr(date_day,1,10)) AS first_date, MAX(substr(date_day,1,10)) AS last_date,
         CAST(julianday(MAX(substr(date_day,1,10))) - julianday(MIN(substr(date_day,1,10))) AS INTEGER) AS days_running
  FROM google_ads__campaign_report
  GROUP BY campaign_id
  HAVING days_running > 120
),
joined AS (
  SELECT c.campaign_id, c.campaign_name, c.account_id, c.account_name, c.advertising_channel_type, c.advertising_channel_subtype,
         substr(a.date_day,1,10) AS d, a.customer_acquisition_cost, a.ltv_cac_ratio, a.spend, a.conversions,
         julianday(substr(a.date_day,1,10)) AS jd, julianday(c.last_date) AS ref_jd
  FROM camp c
  JOIN google_ads__customer_acquisition_analysis a
    ON a.account_id = c.account_id
   AND a.advertising_channel_type = c.advertising_channel_type
   AND COALESCE(a.advertising_channel_subtype,'') = COALESCE(c.advertising_channel_subtype,'')
   AND substr(a.date_day,1,10) BETWEEN c.first_date AND c.last_date
),
metrics AS (
  SELECT campaign_id, campaign_name, account_id, account_name, advertising_channel_type, advertising_channel_subtype,
         SUM(CASE WHEN jd >= ref_jd - 29 THEN spend ELSE 0 END) AS spend_last,
         SUM(CASE WHEN jd >= ref_jd - 29 THEN conversions ELSE 0 END) AS conv_last,
         SUM(CASE WHEN jd BETWEEN ref_jd - 59 AND ref_jd - 30 THEN spend ELSE 0 END) AS spend_prior,
         SUM(CASE WHEN jd BETWEEN ref_jd - 59 AND ref_jd - 30 THEN conversions ELSE 0 END) AS conv_prior,
         SUM(CASE WHEN jd >= ref_jd - 29 THEN conversions*ltv_cac_ratio ELSE 0 END) AS ltv_cac_w_last,
         SUM(CASE WHEN jd BETWEEN ref_jd - 59 AND ref_jd - 30 THEN conversions*ltv_cac_ratio ELSE 0 END) AS ltv_cac_w_prior
  FROM joined
  GROUP BY campaign_id
  HAVING conv_last > 0 AND conv_prior > 0
)
SELECT campaign_id, campaign_name, account_id, advertising_channel_type, advertising_channel_subtype,
       ROUND((spend_last/conv_last - spend_prior/conv_prior)/(spend_prior/conv_prior),4) AS cac_growth,
       ROUND((ltv_cac_w_last/conv_last - ltv_cac_w_prior/conv_prior)/(ltv_cac_w_prior/conv_prior),4) AS ltv_cac_change,
       CASE WHEN (spend_last/conv_last - spend_prior/conv_prior)/(spend_prior/conv_prior) > 0.25 
            AND (ltv_cac_w_last/conv_last - ltv_cac_w_prior/conv_prior)/(ltv_cac_w_prior/conv_prior) < -0.20
       THEN 'DECAY_FLAG' ELSE 'ok' END AS status
FROM metrics
ORDER BY (spend_last/conv_last - spend_prior/conv_prior)/(spend_prior/conv_prior) DESC
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-057/attempt-01/sql/S69.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-057/attempt-01/sql/S69.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-057/attempt-01/results/S69.rows.jsonl)；完整：True；SHA256：`d6ce8265f20038517f62e4db006e32753755f1cb7d675f0f3431c95fe12b19b4`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "google_ads__campaign_report", "kind": "base", "block": null, "base_tables": ["google_ads__campaign_report"]}] | [] | ["campaign_id"] |
| B2 | [{"alias": "c", "kind": "derived", "block": "B1", "base_tables": ["google_ads__campaign_report"]}, {"alias": "a", "kind": "base", "block": null, "base_tables": ["google_ads__customer_acquisition_analysis"]}] | [{"type": "INNER", "right": "google_ads__customer_acquisition_analysis AS a", "on": "a.account_id = c.account_id AND a.advertising_channel_type = c.advertising_channel_type AND COALESCE(a.advertising_channel_subtype, '') = COALESCE(c.advertising_channel_subtype, '') AND SUBSTRING(a.date_day, 1, 10) BETWEEN c.first_date AND c.last_date", "using": []}] | [] |
| B3 | [{"alias": "joined", "kind": "derived", "block": "B2", "base_tables": ["google_ads__campaign_report", "google_ads__customer_acquisition_analysis"]}] | [] | ["campaign_id"] |
| B4 | [{"alias": "metrics", "kind": "derived", "block": "B3", "base_tables": ["google_ads__campaign_report", "google_ads__customer_acquisition_analysis"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | MIN(SUBSTRING(date_day, 1, 10)) | [{"table": "google_ads__campaign_report", "column": "date_day"}] | [] | False |
| B1 | MAX(SUBSTRING(date_day, 1, 10)) | [{"table": "google_ads__campaign_report", "column": "date_day"}] | [] | False |
| B1 | MAX(SUBSTRING(date_day, 1, 10)) | [{"table": "google_ads__campaign_report", "column": "date_day"}] | [] | False |
| B1 | MIN(SUBSTRING(date_day, 1, 10)) | [{"table": "google_ads__campaign_report", "column": "date_day"}] | [] | False |
| B3 | SUM(CASE WHEN jd >= ref_jd - 29 THEN spend ELSE 0 END) | [{"table": "google_ads__customer_acquisition_analysis", "column": "spend"}] | [{"table": "google_ads__customer_acquisition_analysis", "column": "date_day"}, {"table": "google_ads__campaign_report", "column": "date_day"}] | False |
| B3 | SUM(CASE WHEN jd >= ref_jd - 29 THEN conversions ELSE 0 END) | [{"table": "google_ads__customer_acquisition_analysis", "column": "conversions"}] | [{"table": "google_ads__customer_acquisition_analysis", "column": "date_day"}, {"table": "google_ads__campaign_report", "column": "date_day"}] | False |
| B3 | SUM(CASE WHEN jd BETWEEN ref_jd - 59 AND ref_jd - 30 THEN spend ELSE 0 END) | [{"table": "google_ads__customer_acquisition_analysis", "column": "spend"}] | [{"table": "google_ads__customer_acquisition_analysis", "column": "date_day"}, {"table": "google_ads__campaign_report", "column": "date_day"}, {"table": "google_ads__campaign_report", "column": "date_day"}] | False |
| B3 | SUM(CASE WHEN jd BETWEEN ref_jd - 59 AND ref_jd - 30 THEN conversions ELSE 0 END) | [{"table": "google_ads__customer_acquisition_analysis", "column": "conversions"}] | [{"table": "google_ads__customer_acquisition_analysis", "column": "date_day"}, {"table": "google_ads__campaign_report", "column": "date_day"}, {"table": "google_ads__campaign_report", "column": "date_day"}] | False |
| B3 | SUM(CASE WHEN jd >= ref_jd - 29 THEN conversions * ltv_cac_ratio ELSE 0 END) | [{"table": "google_ads__customer_acquisition_analysis", "column": "conversions"}, {"table": "google_ads__customer_acquisition_analysis", "column": "ltv_cac_ratio"}] | [{"table": "google_ads__customer_acquisition_analysis", "column": "date_day"}, {"table": "google_ads__campaign_report", "column": "date_day"}] | False |
| B3 | SUM(CASE WHEN jd BETWEEN ref_jd - 59 AND ref_jd - 30 THEN conversions * ltv_cac_ratio ELSE 0 END) | [{"table": "google_ads__customer_acquisition_analysis", "column": "conversions"}, {"table": "google_ads__customer_acquisition_analysis", "column": "ltv_cac_ratio"}] | [{"table": "google_ads__customer_acquisition_analysis", "column": "date_day"}, {"table": "google_ads__campaign_report", "column": "date_day"}, {"table": "google_ads__campaign_report", "column": "date_day"}] | False |


## S70

类别 `data`；来源 `query_db`；调用 `11724a369ea2440395bb3d9b7e973f1c`；状态 `success`。

```sql
SELECT campaign_id, MIN(substr(date_day,1,10)) AS first_date, MAX(substr(date_day,1,10)) AS last_date,
       CAST(julianday(MAX(substr(date_day,1,10))) - julianday(MIN(substr(date_day,1,10))) AS INTEGER) AS days_running
FROM google_ads__campaign_report
WHERE campaign_id IN ('CMP_ACC_FIN_001_001','CMP_ACC_FIN_001_003','CMP_ACC_FIN_001_006','CMP_ACC_FIN_001_007')
GROUP BY campaign_id
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-057/attempt-01/sql/S70.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-057/attempt-01/sql/S70.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-057/attempt-01/results/S70.rows.jsonl)；完整：True；SHA256：`2c6fdae8876093c88270f395375188701295a2c2c05944afc81a9e0e80144a63`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "google_ads__campaign_report", "kind": "base", "block": null, "base_tables": ["google_ads__campaign_report"]}] | [] | ["campaign_id"] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | MIN(SUBSTRING(date_day, 1, 10)) | [{"table": "google_ads__campaign_report", "column": "date_day"}] | [] | False |
| B1 | MAX(SUBSTRING(date_day, 1, 10)) | [{"table": "google_ads__campaign_report", "column": "date_day"}] | [] | False |
| B1 | MAX(SUBSTRING(date_day, 1, 10)) | [{"table": "google_ads__campaign_report", "column": "date_day"}] | [] | False |
| B1 | MIN(SUBSTRING(date_day, 1, 10)) | [{"table": "google_ads__campaign_report", "column": "date_day"}] | [] | False |


## S71

类别 `data`；来源 `query_db`；调用 `0f2b39c707254585b151fc6597700c83`；状态 `success`。

```sql
WITH camp AS (
  SELECT campaign_id, campaign_name, account_id, account_name, advertising_channel_type, advertising_channel_subtype,
         MIN(substr(date_day,1,10)) AS first_date, MAX(substr(date_day,1,10)) AS last_date,
         CAST(julianday(MAX(substr(date_day,1,10))) - julianday(MIN(substr(date_day,1,10))) AS INTEGER) AS days_running
  FROM google_ads__campaign_report
  GROUP BY campaign_id
  HAVING days_running > 120
)
SELECT c.campaign_id, c.campaign_name, c.account_id, c.account_name, c.days_running,
       c.last_date AS camp_last_date,
       a.date_day, a.campaign_lifecycle_stage, a.advertising_channel_type, a.advertising_channel_subtype,
       a.customer_maturity_stage, a.account_maturity_stage, a.strategic_customer_segment,
       a.customer_acquisition_cost, a.ltv_cac_ratio, a.spend, a.conversions, a.conversions_value,
       a.acquisition_sophistication_score, a.cac_efficiency_percentile, a.channel_diversity_count,
       a.retention_risk, a.scale_opportunity, a.high_cac_alert, a.negative_roi_alert,
       a.cac_performance_tier, a.acquisition_efficiency_tier, a.acquisition_recommendation,
       a.roas, a.cpc, a.ctr, a.estimated_payback_days,
       a.active_campaigns_count, a.cumulative_acquisition_cost, a.cumulative_conversions, a.cumulative_ltv,
       a.cac_vs_cohort_pct, a.ltv_vs_cohort_pct,
       julianday(substr(a.date_day,1,10)) AS jd
FROM camp c
JOIN google_ads__customer_acquisition_analysis a
  ON a.account_id = c.account_id
 AND a.advertising_channel_type = c.advertising_channel_type
 AND COALESCE(a.advertising_channel_subtype,'') = COALESCE(c.advertising_channel_subtype,'')
 AND substr(a.date_day,1,10) BETWEEN c.first_date AND c.last_date
ORDER BY c.campaign_id, a.date_day
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-057/attempt-01/sql/S71.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-057/attempt-01/sql/S71.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-057/attempt-01/results/S71.rows.jsonl)；完整：True；SHA256：`a646dcc0e3c7c0b0f28718e00fdbf4e452aac260837986d803085d78ba8b4a8a`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "google_ads__campaign_report", "kind": "base", "block": null, "base_tables": ["google_ads__campaign_report"]}] | [] | ["campaign_id"] |
| B2 | [{"alias": "c", "kind": "derived", "block": "B1", "base_tables": ["google_ads__campaign_report"]}, {"alias": "a", "kind": "base", "block": null, "base_tables": ["google_ads__customer_acquisition_analysis"]}] | [{"type": "INNER", "right": "google_ads__customer_acquisition_analysis AS a", "on": "a.account_id = c.account_id AND a.advertising_channel_type = c.advertising_channel_type AND COALESCE(a.advertising_channel_subtype, '') = COALESCE(c.advertising_channel_subtype, '') AND SUBSTRING(a.date_day, 1, 10) BETWEEN c.first_date AND c.last_date", "using": []}] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | MIN(SUBSTRING(date_day, 1, 10)) | [{"table": "google_ads__campaign_report", "column": "date_day"}] | [] | False |
| B1 | MAX(SUBSTRING(date_day, 1, 10)) | [{"table": "google_ads__campaign_report", "column": "date_day"}] | [] | False |
| B1 | MAX(SUBSTRING(date_day, 1, 10)) | [{"table": "google_ads__campaign_report", "column": "date_day"}] | [] | False |
| B1 | MIN(SUBSTRING(date_day, 1, 10)) | [{"table": "google_ads__campaign_report", "column": "date_day"}] | [] | False |


## S72

类别 `data`；来源 `query_db`；调用 `73b19b3cc22248e58be6aa7160e09623`；状态 `success`。

```sql
WITH camp AS (
  SELECT campaign_id, campaign_name, account_id, account_name, advertising_channel_type, advertising_channel_subtype,
         MIN(substr(date_day,1,10)) AS first_date, MAX(substr(date_day,1,10)) AS last_date,
         CAST(julianday(MAX(substr(date_day,1,10))) - julianday(MIN(substr(date_day,1,10))) AS INTEGER) AS days_running
  FROM google_ads__campaign_report
  GROUP BY campaign_id
  HAVING days_running > 120
),
joined AS (
  SELECT c.campaign_id, c.campaign_name, c.account_id, c.account_name, c.advertising_channel_type, c.advertising_channel_subtype,
         julianday(substr(a.date_day,1,10)) AS jd, julianday(c.last_date) AS ref_jd,
         a.customer_acquisition_cost, a.ltv_cac_ratio, a.spend, a.conversions,
         a.campaign_lifecycle_stage, a.customer_maturity_stage, a.account_maturity_stage, a.strategic_customer_segment,
         a.acquisition_sophistication_score, a.cac_efficiency_percentile, a.channel_diversity_count,
         a.retention_risk, a.scale_opportunity, a.high_cac_alert, a.negative_roi_alert,
         a.cac_performance_tier, a.acquisition_efficiency_tier, a.acquisition_recommendation
  FROM camp c
  JOIN google_ads__customer_acquisition_analysis a
    ON a.account_id = c.account_id
   AND a.advertising_channel_type = c.advertising_channel_type
   AND COALESCE(a.advertising_channel_subtype,'') = COALESCE(c.advertising_channel_subtype,'')
   AND substr(a.date_day,1,10) BETWEEN c.first_date AND c.last_date
)
SELECT campaign_id, campaign_name, account_id, account_name, advertising_channel_type, advertising_channel_subtype,
       SUM(CASE WHEN jd >= ref_jd - 29 THEN spend ELSE 0 END) AS spend_last,
       SUM(CASE WHEN jd >= ref_jd - 29 THEN conversions ELSE 0 END) AS conv_last,
       SUM(CASE WHEN jd BETWEEN ref_jd - 59 AND ref_jd - 30 THEN spend ELSE 0 END) AS spend_prior,
       SUM(CASE WHEN jd BETWEEN ref_jd - 59 AND ref_jd - 30 THEN conversions ELSE 0 END) AS conv_prior,
       SUM(CASE WHEN jd >= ref_jd - 29 THEN conversions*ltv_cac_ratio ELSE 0 END) AS ltv_cac_w_last,
       SUM(CASE WHEN jd BETWEEN ref_jd - 59 AND ref_jd - 30 THEN conversions*ltv_cac_ratio ELSE 0 END) AS ltv_cac_w_prior,
       MAX(CASE WHEN jd >= ref_jd - 29 THEN acquisition_sophistication_score ELSE 0 END) AS soph_score_last,
       MAX(CASE WHEN jd >= ref_jd - 29 THEN cac_efficiency_percentile ELSE 0 END) AS eff_perc_last,
       MAX(CASE WHEN jd >= ref_jd - 29 THEN channel_diversity_count ELSE 0 END) AS ch_div_last,
       MAX(CASE WHEN jd >= ref_jd - 29 THEN retention_risk ELSE 0 END) AS retention_risk_last,
       MAX(CASE WHEN jd >= ref_jd - 29 THEN scale_opportunity ELSE 0 END) AS scale_opp_last,
       MAX(CASE WHEN jd >= ref_jd - 29 THEN high_cac_alert ELSE 0 END) AS high_cac_alert_last,
       MAX(CASE WHEN jd >= ref_jd - 29 THEN negative_roi_alert ELSE 0 END) AS neg_roi_last
FROM joined
GROUP BY campaign_id
HAVING conv_last > 0 AND conv_prior > 0
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-057/attempt-01/sql/S72.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-057/attempt-01/sql/S72.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-057/attempt-01/results/S72.rows.jsonl)；完整：True；SHA256：`55ecd80b78191491cd0ff99fe19dd8d2be292dd45b96fa31636e3a7cee2cd550`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "google_ads__campaign_report", "kind": "base", "block": null, "base_tables": ["google_ads__campaign_report"]}] | [] | ["campaign_id"] |
| B2 | [{"alias": "c", "kind": "derived", "block": "B1", "base_tables": ["google_ads__campaign_report"]}, {"alias": "a", "kind": "base", "block": null, "base_tables": ["google_ads__customer_acquisition_analysis"]}] | [{"type": "INNER", "right": "google_ads__customer_acquisition_analysis AS a", "on": "a.account_id = c.account_id AND a.advertising_channel_type = c.advertising_channel_type AND COALESCE(a.advertising_channel_subtype, '') = COALESCE(c.advertising_channel_subtype, '') AND SUBSTRING(a.date_day, 1, 10) BETWEEN c.first_date AND c.last_date", "using": []}] | [] |
| B3 | [{"alias": "joined", "kind": "derived", "block": "B2", "base_tables": ["google_ads__campaign_report", "google_ads__customer_acquisition_analysis"]}] | [] | ["campaign_id"] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | MIN(SUBSTRING(date_day, 1, 10)) | [{"table": "google_ads__campaign_report", "column": "date_day"}] | [] | False |
| B1 | MAX(SUBSTRING(date_day, 1, 10)) | [{"table": "google_ads__campaign_report", "column": "date_day"}] | [] | False |
| B1 | MAX(SUBSTRING(date_day, 1, 10)) | [{"table": "google_ads__campaign_report", "column": "date_day"}] | [] | False |
| B1 | MIN(SUBSTRING(date_day, 1, 10)) | [{"table": "google_ads__campaign_report", "column": "date_day"}] | [] | False |
| B3 | SUM(CASE WHEN jd >= ref_jd - 29 THEN spend ELSE 0 END) | [{"table": "google_ads__customer_acquisition_analysis", "column": "spend"}] | [{"table": "google_ads__customer_acquisition_analysis", "column": "date_day"}, {"table": "google_ads__campaign_report", "column": "date_day"}] | False |
| B3 | SUM(CASE WHEN jd >= ref_jd - 29 THEN conversions ELSE 0 END) | [{"table": "google_ads__customer_acquisition_analysis", "column": "conversions"}] | [{"table": "google_ads__customer_acquisition_analysis", "column": "date_day"}, {"table": "google_ads__campaign_report", "column": "date_day"}] | False |
| B3 | SUM(CASE WHEN jd BETWEEN ref_jd - 59 AND ref_jd - 30 THEN spend ELSE 0 END) | [{"table": "google_ads__customer_acquisition_analysis", "column": "spend"}] | [{"table": "google_ads__customer_acquisition_analysis", "column": "date_day"}, {"table": "google_ads__campaign_report", "column": "date_day"}, {"table": "google_ads__campaign_report", "column": "date_day"}] | False |
| B3 | SUM(CASE WHEN jd BETWEEN ref_jd - 59 AND ref_jd - 30 THEN conversions ELSE 0 END) | [{"table": "google_ads__customer_acquisition_analysis", "column": "conversions"}] | [{"table": "google_ads__customer_acquisition_analysis", "column": "date_day"}, {"table": "google_ads__campaign_report", "column": "date_day"}, {"table": "google_ads__campaign_report", "column": "date_day"}] | False |
| B3 | SUM(CASE WHEN jd >= ref_jd - 29 THEN conversions * ltv_cac_ratio ELSE 0 END) | [{"table": "google_ads__customer_acquisition_analysis", "column": "conversions"}, {"table": "google_ads__customer_acquisition_analysis", "column": "ltv_cac_ratio"}] | [{"table": "google_ads__customer_acquisition_analysis", "column": "date_day"}, {"table": "google_ads__campaign_report", "column": "date_day"}] | False |
| B3 | SUM(CASE WHEN jd BETWEEN ref_jd - 59 AND ref_jd - 30 THEN conversions * ltv_cac_ratio ELSE 0 END) | [{"table": "google_ads__customer_acquisition_analysis", "column": "conversions"}, {"table": "google_ads__customer_acquisition_analysis", "column": "ltv_cac_ratio"}] | [{"table": "google_ads__customer_acquisition_analysis", "column": "date_day"}, {"table": "google_ads__campaign_report", "column": "date_day"}, {"table": "google_ads__campaign_report", "column": "date_day"}] | False |
| B3 | MAX(CASE WHEN jd >= ref_jd - 29 THEN acquisition_sophistication_score ELSE 0 END) | [{"table": "google_ads__customer_acquisition_analysis", "column": "acquisition_sophistication_score"}] | [{"table": "google_ads__customer_acquisition_analysis", "column": "date_day"}, {"table": "google_ads__campaign_report", "column": "date_day"}] | False |
| B3 | MAX(CASE WHEN jd >= ref_jd - 29 THEN cac_efficiency_percentile ELSE 0 END) | [{"table": "google_ads__customer_acquisition_analysis", "column": "cac_efficiency_percentile"}] | [{"table": "google_ads__customer_acquisition_analysis", "column": "date_day"}, {"table": "google_ads__campaign_report", "column": "date_day"}] | False |
| B3 | MAX(CASE WHEN jd >= ref_jd - 29 THEN channel_diversity_count ELSE 0 END) | [{"table": "google_ads__customer_acquisition_analysis", "column": "channel_diversity_count"}] | [{"table": "google_ads__customer_acquisition_analysis", "column": "date_day"}, {"table": "google_ads__campaign_report", "column": "date_day"}] | False |
| B3 | MAX(CASE WHEN jd >= ref_jd - 29 THEN retention_risk ELSE 0 END) | [{"table": "google_ads__customer_acquisition_analysis", "column": "retention_risk"}] | [{"table": "google_ads__customer_acquisition_analysis", "column": "date_day"}, {"table": "google_ads__campaign_report", "column": "date_day"}] | False |
| B3 | MAX(CASE WHEN jd >= ref_jd - 29 THEN scale_opportunity ELSE 0 END) | [{"table": "google_ads__customer_acquisition_analysis", "column": "scale_opportunity"}] | [{"table": "google_ads__customer_acquisition_analysis", "column": "date_day"}, {"table": "google_ads__campaign_report", "column": "date_day"}] | False |
| B3 | MAX(CASE WHEN jd >= ref_jd - 29 THEN high_cac_alert ELSE 0 END) | [{"table": "google_ads__customer_acquisition_analysis", "column": "high_cac_alert"}] | [{"table": "google_ads__customer_acquisition_analysis", "column": "date_day"}, {"table": "google_ads__campaign_report", "column": "date_day"}] | False |
| B3 | MAX(CASE WHEN jd >= ref_jd - 29 THEN negative_roi_alert ELSE 0 END) | [{"table": "google_ads__customer_acquisition_analysis", "column": "negative_roi_alert"}] | [{"table": "google_ads__customer_acquisition_analysis", "column": "date_day"}, {"table": "google_ads__campaign_report", "column": "date_day"}] | False |


## S73

类别 `data`；来源 `query_db`；调用 `1486c7d375294db2bd53fa5b42135eb9`；状态 `success`。

```sql
SELECT DISTINCT campaign_lifecycle_stage, customer_maturity_stage, account_maturity_stage, strategic_customer_segment,
       COUNT(*) AS n_rows
FROM google_ads__customer_acquisition_analysis
GROUP BY campaign_lifecycle_stage, customer_maturity_stage, account_maturity_stage, strategic_customer_segment
ORDER BY n_rows DESC
LIMIT 30
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-057/attempt-01/sql/S73.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-057/attempt-01/sql/S73.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-057/attempt-01/results/S73.rows.jsonl)；完整：True；SHA256：`4266a8d7622d37561851beb237fbce2afba8e41cebc559c5efcb5abd93d6ea98`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "google_ads__customer_acquisition_analysis", "kind": "base", "block": null, "base_tables": ["google_ads__customer_acquisition_analysis"]}] | [] | ["campaign_lifecycle_stage", "customer_maturity_stage", "account_maturity_stage", "strategic_customer_segment"] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |


## S74

类别 `data`；来源 `query_db`；调用 `0c523c2f6e77489285780a9f24a9a55d`；状态 `success`。

```sql
SELECT account_id, advertising_channel_type, advertising_channel_subtype, campaign_lifecycle_stage, customer_maturity_stage,
       account_maturity_stage, strategic_customer_segment,
       COUNT(*) AS n_rows,
       ROUND(AVG(customer_acquisition_cost),2) AS avg_cac,
       ROUND(AVG(ltv_cac_ratio),2) AS avg_ltv_cac,
       ROUND(AVG(acquisition_sophistication_score),1) AS avg_soph,
       ROUND(AVG(cac_efficiency_percentile),1) AS avg_eff,
       ROUND(AVG(channel_diversity_count),1) AS avg_chdiv,
       SUM(retention_risk) AS retention_risk_cnt,
       SUM(scale_opportunity) AS scale_opp_cnt,
       SUM(high_cac_alert) AS high_cac_cnt,
       SUM(negative_roi_alert) AS neg_roi_cnt
FROM google_ads__customer_acquisition_analysis
WHERE (account_id = 'ACC_FIN_001' AND advertising_channel_type = 'SHOPPING')
   OR (account_id = 'ACC_ECOM_002' AND advertising_channel_type = 'VIDEO' AND advertising_channel_subtype = 'YOUTUBE_SEARCH')
GROUP BY account_id, advertising_channel_type, advertising_channel_subtype, campaign_lifecycle_stage, customer_maturity_stage, account_maturity_stage, strategic_customer_segment
ORDER BY account_id, advertising_channel_type, campaign_lifecycle_stage
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-057/attempt-01/sql/S74.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-057/attempt-01/sql/S74.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-057/attempt-01/results/S74.rows.jsonl)；完整：True；SHA256：`099a5ec04cff6524c9de21f118c7ade5e1d3233475ebc31fcfbb5287f02de5ff`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "google_ads__customer_acquisition_analysis", "kind": "base", "block": null, "base_tables": ["google_ads__customer_acquisition_analysis"]}] | [] | ["account_id", "advertising_channel_type", "advertising_channel_subtype", "campaign_lifecycle_stage", "customer_maturity_stage", "account_maturity_stage", "strategic_customer_segment"] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |
| B1 | SUM(retention_risk) | [{"table": "google_ads__customer_acquisition_analysis", "column": "retention_risk"}] | [] | False |
| B1 | SUM(scale_opportunity) | [{"table": "google_ads__customer_acquisition_analysis", "column": "scale_opportunity"}] | [] | False |
| B1 | SUM(high_cac_alert) | [{"table": "google_ads__customer_acquisition_analysis", "column": "high_cac_alert"}] | [] | False |
| B1 | SUM(negative_roi_alert) | [{"table": "google_ads__customer_acquisition_analysis", "column": "negative_roi_alert"}] | [] | False |
| B1 | AVG(customer_acquisition_cost) | [{"table": "google_ads__customer_acquisition_analysis", "column": "customer_acquisition_cost"}] | [] | False |
| B1 | AVG(ltv_cac_ratio) | [{"table": "google_ads__customer_acquisition_analysis", "column": "ltv_cac_ratio"}] | [] | False |
| B1 | AVG(acquisition_sophistication_score) | [{"table": "google_ads__customer_acquisition_analysis", "column": "acquisition_sophistication_score"}] | [] | False |
| B1 | AVG(cac_efficiency_percentile) | [{"table": "google_ads__customer_acquisition_analysis", "column": "cac_efficiency_percentile"}] | [] | False |
| B1 | AVG(channel_diversity_count) | [{"table": "google_ads__customer_acquisition_analysis", "column": "channel_diversity_count"}] | [] | False |

