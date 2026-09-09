# dacomp-058

Upon discovering a severe imbalance between input and output in some high-cost campaigns, …

运行：已提交。官方未评分。全部 SQL 尝试/成功 58/57；数据 SQL 56/55；Python 18 次。

完整原题：

Upon discovering a severe imbalance between input and output in some high-cost campaigns, there is a need to establish a comprehensive campaign health assessment and optimization system. Based on data from multiple tables in the `google_ads` database, use a monthly cost > $1000 and an ROI < 0.8 as initial screening criteria to build a three-dimensional health score model consisting of Cost Efficiency (40%), Conversion Quality (35%), and Competitiveness (25%). The analysis must compare the performance differences across various channel types (`campaign_type`), bidding strategies (`bidding_strategy`), industry categories (`industry`), geographic distributions (`geo_target`), and device types (`device_type`) to identify high-cost, low-conversion risk campaigns. Based on multidimensional competitive metrics such as `quality_score`, `impression_share`, `ctr`, `conversion_rate`, and `avg_position`, propose targeted optimization recommendations. Additionally, consider the trend changes over 18 months, calculating year-over-year growth rates and seasonal fluctuations, to formulate differentiated optimization plans for each problematic campaign, including budget reallocation, keyword optimization, geographic adjustments, and device bidding strategies. The final output should include the health score, risk level, core problem diagnosis, and specific optimization recommendations for each campaign.

| 表 | 行数 | 列数 |
| --- | --- | --- |
| ad_groups | 58 | 4 |
| campaigns | 200 | 8 |
| google_ads__campaign_report | 714 | 18 |
| google_ads__device_report | 2142 | 15 |
| google_ads__geo_report | 2550 | 15 |
| google_ads__keyword_report | 1303 | 19 |
| keywords | 252 | 6 |


实际路线（分析者依据 SQL/源码概括，不代表 Agent 自述）：SQL 筛选高成本低 ROI 活动并计算健康评分与趋势 → Python 多维分组、关键词汇总和图表 → 活动诊断建议。

数据库大小：978,944 字节。

## 数据 SQL

| SQL | 状态 | 基础表 | Join 输入/类型 | GROUP BY | 聚合表达式 | 结果行数 | 数据库 ms |
| --- | --- | --- | --- | --- | --- | --- | --- |
| [S3/Q1](#s3) | success | ["ad_groups", "campaigns", "google_ads__campaign_report", "google_ads__device_report", "google_ads__geo_report", "google_ads__keyword_report", "keywords"] | 0 / {} | [] | ["COUNT(*)", "COUNT(DISTINCT campaign_id)", "COUNT(DISTINCT year_month)", "MIN(year_month)", "MAX(year_month)", "COUNT(*)", "COUNT(DISTINCT campaign_id)", "COUNT(DISTINCT year_month)", "MIN(year_month)", "MAX(year_month)", "COUNT(*)", "COUNT(DISTINCT campaign_id)", "COUNT(DISTINCT year_month)", "MIN(year_month)", "MAX(year_month)", "COUNT(*)", "COUNT(DISTINCT campaign_id)", "COUNT(DISTINCT year_quarter)", "MIN(year_quarter)", "MAX(year_quarter)", "COUNT(*)", "COUNT(DISTINCT campaign_id)", "COUNT(*)", "COUNT(DISTINCT keyword_id)", "COUNT(*)", "COUNT(DISTINCT ad_group_id)"] | 7 | 3.747 |
| [S4/Q2](#s4) | success | ["campaigns", "google_ads__campaign_report"] | 2 / {'LEFT': 1} | [] | ["COUNT(*)"] | 1 | 0.672 |
| [S5/Q3](#s5) | success | ["campaigns"] | 0 / {} | [] | ["MIN(start_date)", "MAX(start_date)", "COUNT(*)", "COUNT(CASE WHEN start_date IS NULL THEN 1 END)"] | 1 | 0.365 |
| [S6/Q4](#s6) | success | ["google_ads__campaign_report"] | 0 / {} | ["campaign_type"] | ["COUNT(*)"] | 5 | 0.492 |
| [S7/Q5](#s7) | success | ["google_ads__campaign_report"] | 0 / {} | ["bidding_strategy"] | ["COUNT(*)"] | 5 | 0.5 |
| [S8/Q6](#s8) | success | ["google_ads__campaign_report"] | 0 / {} | ["industry"] | ["COUNT(*)"] | 8 | 0.602 |
| [S9/Q7](#s9) | success | ["google_ads__campaign_report"] | 0 / {} | ["campaign_id"] | ["COUNT(*)", "SUM(cost)", "SUM(conversions)", "SUM(conversion_value)", "AVG(quality_score)", "AVG(impression_share)", "AVG(ctr)", "AVG(conversion_rate)", "SUM(conversion_value)", "SUM(cost)"] | 50 | 1.321 |
| [S10/Q8](#s10) | success | ["google_ads__campaign_report"] | 0 / {} | [] | ["COUNT(*)", "COUNT(CASE WHEN cost > 1000 THEN 1 END)"] | 1 | 0.394 |
| [S11/Q9](#s11) | success | ["google_ads__campaign_report"] | 0 / {} | [] | [] | 2 | 0.523 |
| [S12/Q10](#s12) | success | ["google_ads__campaign_report"] | 0 / {} | [] | ["MIN(roas)", "MAX(roas)", "AVG(roas)", "MIN(conversion_value / NULLIF(cost, 0))", "MAX(conversion_value / NULLIF(cost, 0))", "AVG(conversion_value / NULLIF(cost, 0))", "AVG(cost)", "MIN(cost)", "MAX(cost)"] | 1 | 0.777 |
| [S13/Q11](#s13) | success | ["google_ads__campaign_report"] | 0 / {} | ["CASE WHEN cost < 5000 THEN '0-5K' WHEN cost < 10000 THEN '5K-10K' WHEN cost < 30000 THEN '10K-30K' WHEN cost < 50000 THEN '30K-50K' WHEN cost < 100000 THEN '50K-100K' ELSE '100K+' END"] | ["COUNT(*)", "AVG(conversion_value / NULLIF(cost, 0))", "AVG(roas)", "MIN(cost)"] | 5 | 0.96 |
| [S14/Q12](#s14) | failed | ["google_ads__campaign_report"] | 0 / {} | [] | ["COUNT(CASE WHEN roas < 0.8 THEN 1 END)", "COUNT(CASE WHEN (conversion_value / NULLIF(cost, 0)) < 0.8 THEN 1 END)", "COUNT(CASE WHEN roas < 0.8 AND (conversion_value / NULLIF(cost, 0)) >= 0.8 THEN 1 END)", "AVG(ABS(roas - conversion_value / NULLIF(cost, 0)))", "CORR(roas, conversion_value / NULLIF(cost, 0))"] | unknown | 未取得；调用总时长 0.184 ms |
| [S15/Q13](#s15) | success | ["google_ads__campaign_report"] | 0 / {} | ["campaign_id"] | ["COUNT(*)", "COUNT(CASE WHEN roas >= 0.8 THEN 1 END)", "AVG(roas)", "AVG(conversion_value / NULLIF(cost, 0))"] | 11 | 0.577 |
| [S16/Q14](#s16) | success | ["google_ads__campaign_report"] | 0 / {} | [] | ["COUNT(*)", "COUNT(CASE WHEN roas < 0.8 THEN 1 END)", "COUNT(*)", "COUNT(CASE WHEN roas < 0.8 THEN 1 END)"] | 1 | 0.421 |
| [S17/Q15](#s17) | success | ["google_ads__campaign_report"] | 0 / {} | ["CASE WHEN roas < 0.3 THEN '<0.3' WHEN roas < 0.5 THEN '0.3-0.5' WHEN roas < 0.7 THEN '0.5-0.7' WHEN roas < 0.8 THEN '0.7-0.8' WHEN roas < 1.0 THEN '0.8-1.0' WHEN roas < 2.0 THEN '1.0-2.0' ELSE '2.0+' END"] | ["COUNT(*)", "AVG(cost)", "AVG(conversion_value)", "MIN(roas)", "COUNT(*)", "COUNT(*)"] | 5 | 0.898 |
| [S18/Q16](#s18) | success | ["google_ads__device_report"] | 0 / {} | ["device_type"] | ["COUNT(*)", "SUM(cost)", "AVG(roas)"] | 3 | 1.315 |
| [S19/Q17](#s19) | success | ["google_ads__geo_report"] | 0 / {} | ["geo_target"] | ["COUNT(*)", "SUM(cost)", "AVG(roas)"] | 7 | 1.407 |
| [S20/Q18](#s20) | success | ["google_ads__keyword_report"] | 0 / {} | ["match_type"] | ["COUNT(*)", "AVG(avg_position)", "AVG(quality_score)", "AVG(roas)"] | 3 | 0.939 |
| [S21/Q19](#s21) | success | ["google_ads__campaign_report"] | 0 / {} | ["campaign_id"] | ["COUNT(*)", "MIN(year_month)", "MAX(year_month)", "COUNT(CASE WHEN roas < 0.8 THEN 1 END)", "SUM(cost)", "AVG(cost)", "SUM(conversions)", "SUM(conversion_value)", "AVG(roas)", "AVG(quality_score)", "AVG(impression_share)", "AVG(ctr)", "AVG(conversion_rate)", "AVG(cpc)", "AVG(cost_per_conversion)", "SUM(conversion_value)", "COUNT(*)", "SUM(cost)", "COUNT(CASE WHEN roas < 0.8 THEN 1 END)"] | 50 | 2.061 |
| [S22/Q20](#s22) | success | ["google_ads__campaign_report"] | 0 / {} | [] | [] | 17 | 0.45 |
| [S23/Q21](#s23) | success | ["google_ads__campaign_report"] | 0 / {} | [] | [] | 14 | 0.444 |
| [S24/Q22](#s24) | success | ["google_ads__campaign_report"] | 0 / {} | ["campaign_id"] | ["COUNT(DISTINCT roas)", "MIN(roas)", "MAX(roas)", "AVG(roas)", "AVG(conversion_value / NULLIF(cost, 0))", "MAX(roas)", "MIN(roas)"] | 50 | 1.116 |
| [S25/Q23](#s25) | success | ["google_ads__campaign_report"] | 0 / {} | ["campaign_id"] | ["COUNT(DISTINCT roas)", "MIN(roas)", "MAX(roas)", "AVG(roas)", "AVG(conversion_value / NULLIF(cost, 0))", "AVG(cost)", "MAX(roas)", "MIN(roas)"] | 10 | 1.123 |
| [S26/Q24](#s26) | success | ["google_ads__campaign_report"] | 0 / {} | [] | [] | 714 | 3.746 |
| [S27/Q25](#s27) | success | ["google_ads__keyword_report"] | 0 / {} | ["campaign_id"] | ["AVG(avg_position)"] | 20 | 0.7 |
| [S28/Q26](#s28) | success | ["google_ads__keyword_report"] | 0 / {} | [] | [] | 20 | 0.587 |
| [S29/Q27](#s29) | success | ["google_ads__campaign_report"] | 0 / {} | [] | [] | 714 | 9.258 |
| [S30/Q28](#s30) | success | ["google_ads__campaign_report"] | 0 / {} | ["campaign_id"] | ["COUNT(*)", "AVG(cost)", "SUM(cost)", "AVG(roas)", "AVG(0.4 * roas_s + 0.3 * cpa_s + 0.3 * cpc_s)", "AVG(0.4 * cvr_s + 0.3 * aov_s + 0.3 * conv_s)", "AVG(0.4 * qs_s + 0.3 * is_s + 0.3 * ctr_s)", "AVG(0.4 * (0.4 * roas_s + 0.3 * cpa_s + 0.3 * cpc_s) + 0.35 * (0.4 * cvr_s + 0.3 * aov_s + 0.3 * conv_s) + 0.25 * (0.4 * qs_s + 0.3 * is_s + 0.3 * ctr_s))"] | 50 | 6.112 |
| [S31/Q29](#s31) | success | ["google_ads__campaign_report"] | 0 / {} | ["campaign_id"] | ["COUNT(*)"] | 50 | 0.774 |
| [S32/Q30](#s32) | success | ["google_ads__campaign_report"] | 0 / {} | ["campaign_id"] | ["COUNT(*)", "AVG(cost)", "SUM(cost)", "AVG(roas)", "AVG(roas_s)", "AVG(cpc_s)", "AVG(cpa_s)", "AVG(cvr_s)", "AVG(aov_s)", "AVG(conv_s)", "AVG(qs_s)", "AVG(is_s)", "AVG(ctr_s)", "AVG(0.4 * roas_s + 0.3 * cpa_s + 0.3 * cpc_s)", "AVG(0.4 * cvr_s + 0.3 * aov_s + 0.3 * conv_s)", "AVG(0.4 * qs_s + 0.3 * is_s + 0.3 * ctr_s)", "AVG(0.4 * (0.4 * roas_s + 0.3 * cpa_s + 0.3 * cpc_s) + 0.35 * (0.4 * cvr_s + 0.3 * aov_s + 0.3 * conv_s) + 0.25 * (0.4 * qs_s + 0.3 * is_s + 0.3 * ctr_s))"] | 50 | 6.26 |
| [S33/Q31](#s33) | success | ["google_ads__campaign_report"] | 0 / {} | ["campaign_id"] | ["COUNT(*)", "AVG(cost)", "SUM(cost)", "AVG(roas)", "AVG(0.4 * roas_s + 0.3 * cpa_s + 0.3 * cpc_s)", "AVG(0.4 * cvr_s + 0.3 * aov_s + 0.3 * conv_s)", "AVG(0.4 * qs_s + 0.3 * is_s + 0.3 * ctr_s)", "AVG(0.4 * (0.4 * roas_s + 0.3 * cpa_s + 0.3 * cpc_s) + 0.35 * (0.4 * cvr_s + 0.3 * aov_s + 0.3 * conv_s) + 0.25 * (0.4 * qs_s + 0.3 * is_s + 0.3 * ctr_s))"] | 50 | 6.01 |
| [S34/Q32](#s34) | success | ["google_ads__campaign_report"] | 0 / {} | ["campaign_id"] | ["COUNT(*)", "AVG(cost)", "SUM(cost)", "AVG(roas)", "AVG(0.4 * roas_s + 0.3 * cpa_s + 0.3 * cpc_s)", "AVG(0.4 * cvr_s + 0.3 * aov_s + 0.3 * conv_s)", "AVG(0.4 * qs_s + 0.3 * is_s + 0.3 * ctr_s)", "AVG(0.4 * (0.4 * roas_s + 0.3 * cpa_s + 0.3 * cpc_s) + 0.35 * (0.4 * cvr_s + 0.3 * aov_s + 0.3 * conv_s) + 0.25 * (0.4 * qs_s + 0.3 * is_s + 0.3 * ctr_s))"] | 50 | 5.462 |
| [S35/Q33](#s35) | success | ["google_ads__device_report"] | 0 / {} | [] | [] | 2142 | 6.674 |
| [S36/Q34](#s36) | success | ["google_ads__geo_report"] | 0 / {} | [] | [] | 2550 | 7.409 |
| [S37/Q35](#s37) | success | ["google_ads__campaign_report"] | 0 / {} | ["year_month"] | ["SUM(cost)", "SUM(conversions)", "SUM(conversion_value)", "AVG(roas)", "AVG(quality_score)", "AVG(impression_share)", "AVG(ctr)", "AVG(conversion_rate)"] | 17 | 0.954 |
| [S38/Q36](#s38) | success | ["google_ads__device_report"] | 0 / {} | [] | [] | 2142 | 6.275 |
| [S39/Q37](#s39) | success | ["google_ads__geo_report"] | 0 / {} | [] | [] | 2550 | 7.278 |
| [S40/Q38](#s40) | success | ["google_ads__campaign_report"] | 0 / {} | ["year_month"] | ["SUM(cost)", "SUM(conversions)", "SUM(conversion_value)", "AVG(roas)", "AVG(quality_score)", "AVG(impression_share)", "AVG(ctr)", "AVG(conversion_rate)"] | 17 | 0.935 |
| [S41/Q39](#s41) | success | ["google_ads__keyword_report"] | 0 / {} | [] | [] | 1303 | 5.658 |
| [S42/Q40](#s42) | success | ["google_ads__device_report"] | 0 / {} | ["campaign_id", "device_type"] | ["SUM(cost)", "AVG(roas)", "AVG(quality_score)", "AVG(conversion_rate)", "AVG(ctr)"] | 30 | 0.987 |
| [S43/Q41](#s43) | success | ["google_ads__geo_report"] | 0 / {} | ["campaign_id", "geo_target"] | ["SUM(cost)", "AVG(roas)", "AVG(quality_score)", "AVG(conversion_rate)", "AVG(ctr)", "SUM(conversions)", "SUM(conversion_value)"] | 36 | 1.485 |
| [S44/Q42](#s44) | success | ["google_ads__keyword_report"] | 0 / {} | [] | [] | 264 | 1.686 |
| [S45/Q43](#s45) | success | ["google_ads__campaign_report"] | 0 / {} | [] | [] | 154 | 0.943 |
| [S46/Q44](#s46) | success | ["google_ads__device_report"] | 0 / {} | ["campaign_id", "device_type"] | ["SUM(cost)"] | 30 | 0.975 |
| [S47/Q45](#s47) | success | ["google_ads__campaign_report"] | 0 / {} | ["campaign_id"] | ["COUNT(*)", "COUNT(CASE WHEN cost > 1000 AND roas < 0.8 THEN 1 END)"] | 50 | 0.91 |
| [S48/Q46](#s48) | success | ["google_ads__campaign_report"] | 0 / {} | [] | ["COUNT(DISTINCT campaign_id)"] | 1 | 0.363 |
| [S49/Q47](#s49) | success | ["google_ads__campaign_report"] | 0 / {} | [] | ["SUM(CASE WHEN campaign_id IN (105, 135, 36, 184, 180, 56, 69, 148, 178, 27) THEN cost ELSE 0 END)", "SUM(cost)", "SUM(cost)", "SUM(CASE WHEN campaign_id IN (105, 135, 36, 184, 180, 56, 69, 148, 178, 27) THEN cost ELSE 0 END)"] | 1 | 0.429 |
| [S50/Q48](#s50) | success | ["google_ads__campaign_report"] | 0 / {} | [] | [] | 154 | 4.05 |
| [S51/Q49](#s51) | success | ["google_ads__campaign_report"] | 0 / {} | ["year_month"] | ["SUM(cost)", "SUM(conversion_value)", "SUM(conversions)", "AVG(roas)"] | 17 | 0.61 |
| [S52/Q50](#s52) | success | ["google_ads__campaign_report"] | 0 / {} | ["campaign_id"] | ["COUNT(*)", "AVG(cost)", "SUM(cost)", "AVG(roas)", "AVG(quality_score)", "AVG(impression_share)", "AVG(ctr)", "AVG(conversion_rate)", "AVG(cpc)", "AVG(cost_per_conversion)", "AVG(0.4 * roas_s + 0.3 * cpa_s + 0.3 * cpc_s)", "AVG(0.4 * cvr_s + 0.3 * aov_s + 0.3 * conv_s)", "AVG(0.4 * qs_s + 0.3 * is_s + 0.3 * ctr_s)", "AVG(0.4 * (0.4 * roas_s + 0.3 * cpa_s + 0.3 * cpc_s) + 0.35 * (0.4 * cvr_s + 0.3 * aov_s + 0.3 * conv_s) + 0.25 * (0.4 * qs_s + 0.3 * is_s + 0.3 * ctr_s))"] | 50 | 6.551 |
| [S53/Q51](#s53) | success | ["google_ads__device_report"] | 0 / {} | ["campaign_id", "device_type"] | ["SUM(cost)", "AVG(roas)"] | 30 | 0.903 |
| [S54/Q52](#s54) | success | ["google_ads__geo_report"] | 0 / {} | ["campaign_id", "geo_target"] | ["SUM(cost)", "AVG(roas)"] | 36 | 1.085 |
| [S55/Q53](#s55) | success | ["google_ads__device_report"] | 0 / {} | ["campaign_id", "device_type"] | ["SUM(cost)", "AVG(roas)", "SUM(conversions)", "SUM(conversion_value)", "SUM(conversion_value)", "SUM(cost)"] | 30 | 1.024 |
| [S56/Q54](#s56) | success | ["google_ads__geo_report"] | 0 / {} | ["campaign_id", "geo_target"] | ["SUM(cost)", "AVG(roas)", "SUM(conversions)", "SUM(conversion_value)", "SUM(conversion_value)", "SUM(cost)"] | 36 | 1.077 |
| [S57/Q55](#s57) | success | ["google_ads__campaign_report"] | 0 / {} | ["campaign_id"] | ["SUM(cost)", "AVG(roas)", "AVG(0.4 * roas_s + 0.3 * cpa_s + 0.3 * cpc_s)", "AVG(0.4 * cvr_s + 0.3 * aov_s + 0.3 * conv_s)", "AVG(0.4 * qs_s + 0.3 * is_s + 0.3 * ctr_s)", "AVG(0.4 * (0.4 * roas_s + 0.3 * cpa_s + 0.3 * cpc_s) + 0.35 * (0.4 * cvr_s + 0.3 * aov_s + 0.3 * conv_s) + 0.25 * (0.4 * qs_s + 0.3 * is_s + 0.3 * ctr_s))"] | 50 | 6.012 |
| [S58/Q56](#s58) | success | ["google_ads__campaign_report"] | 0 / {} | ["campaign_id"] | ["SUM(cost)", "AVG(0.4 * roas_s + 0.3 * cpa_s + 0.3 * cpc_s)", "AVG(0.4 * cvr_s + 0.3 * aov_s + 0.3 * conv_s)", "AVG(0.4 * qs_s + 0.3 * is_s + 0.3 * ctr_s)", "AVG(0.4 * (0.4 * roas_s + 0.3 * cpa_s + 0.3 * cpc_s) + 0.35 * (0.4 * cvr_s + 0.3 * aov_s + 0.3 * conv_s) + 0.25 * (0.4 * qs_s + 0.3 * is_s + 0.3 * ctr_s))"] | 50 | 5.841 |


## 元数据和设置

| SQL | 类别 | 状态 | 内容 |
| --- | --- | --- | --- |
| S1 | connection_setup | success | PRAGMA query_only=ON |
| S2 | metadata | success | SELECT name,sql FROM sqlite_master WHERE type='table' ORDER BY name |


## Python 与执行位置

人工源码审查：**database_first_violation**。Python 为风险级别、渠道、行业、竞价策略、设备、地域和关键词计算分组数量、均值、成本求和与份额。这些计算可在 SQL 内完成，且并非只做图形渲染。 [证据](../reviews/dacomp-058.json)。

P1：Load campaign-level health scores and detailed monthly data into Python for comprehensive analysis, visualization, and trend computation. This is beyond SQL's capabilities for multi-dimensional visualization and statistical analysis.

[源码](../../../runs/dsv4flash-db-first-full-01/dacomp-058/attempt-01/python/P1.py)；[输出](../../../runs/dsv4flash-db-first-full-01/dacomp-058/attempt-01/python/P1.stdout)；[错误](../../../runs/dsv4flash-db-first-full-01/dacomp-058/attempt-01/python/P1.stderr)。自动源码筛查未检出预设迁出信号；这不是全面语义合规证明。

P2：Load campaign scores and monthly data into Python for visualization and comprehensive analysis. The JSON lines files need to be read with proper working directory handling.

[源码](../../../runs/dsv4flash-db-first-full-01/dacomp-058/attempt-01/python/P2.py)；[输出](../../../runs/dsv4flash-db-first-full-01/dacomp-058/attempt-01/python/P2.stdout)；[错误](../../../runs/dsv4flash-db-first-full-01/dacomp-058/attempt-01/python/P2.stderr)。检出需人工核验的 SQL 可实现操作：.query(；不能仅凭理由判为合规。

P3：Test the db global object access and file paths for reading archived results.

[源码](../../../runs/dsv4flash-db-first-full-01/dacomp-058/attempt-01/python/P3.py)；[输出](../../../runs/dsv4flash-db-first-full-01/dacomp-058/attempt-01/python/P3.stdout)；[错误](../../../runs/dsv4flash-db-first-full-01/dacomp-058/attempt-01/python/P3.stderr)。自动源码筛查未检出预设迁出信号；这不是全面语义合规证明。

P4：Locate the archived results files to load data into pandas for analysis.

[源码](../../../runs/dsv4flash-db-first-full-01/dacomp-058/attempt-01/python/P4.py)；[输出](../../../runs/dsv4flash-db-first-full-01/dacomp-058/attempt-01/python/P4.stdout)；[错误](../../../runs/dsv4flash-db-first-full-01/dacomp-058/attempt-01/python/P4.stderr)。检出需人工核验的 SQL 可实现操作：.query(；不能仅凭理由判为合规。

P5：Load all necessary data for comprehensive analysis: campaign health scores, monthly data, device data, geo data, keyword data. Use SQL to aggregate and join, then pandas for visualization.

[源码](../../../runs/dsv4flash-db-first-full-01/dacomp-058/attempt-01/python/P5.py)；[输出](../../../runs/dsv4flash-db-first-full-01/dacomp-058/attempt-01/python/P5.stdout)；[错误](../../../runs/dsv4flash-db-first-full-01/dacomp-058/attempt-01/python/P5.stderr)。检出需人工核验的 SQL 可实现操作：.query(；不能仅凭理由判为合规。

P6：Assign risk levels, analyze health score distribution, and prepare visualizations for the health score model.

[源码](../../../runs/dsv4flash-db-first-full-01/dacomp-058/attempt-01/python/P6.py)；[输出](../../../runs/dsv4flash-db-first-full-01/dacomp-058/attempt-01/python/P6.stdout)；[错误](../../../runs/dsv4flash-db-first-full-01/dacomp-058/attempt-01/python/P6.stderr)。检出需人工核验的 SQL 可实现操作：groupby(, .query(；不能仅凭理由判为合规。

P7：Check working directory and create work directory for saving figures.

[源码](../../../runs/dsv4flash-db-first-full-01/dacomp-058/attempt-01/python/P7.py)；[输出](../../../runs/dsv4flash-db-first-full-01/dacomp-058/attempt-01/python/P7.stdout)；[错误](../../../runs/dsv4flash-db-first-full-01/dacomp-058/attempt-01/python/P7.stderr)。自动源码筛查未检出预设迁出信号；这不是全面语义合规证明。

P8：Create visualizations for health score distribution, dimensions comparison, and cross-dimension comparisons. Use CWD /work for saving figures.

[源码](../../../runs/dsv4flash-db-first-full-01/dacomp-058/attempt-01/python/P8.py)；[输出](../../../runs/dsv4flash-db-first-full-01/dacomp-058/attempt-01/python/P8.stdout)；[错误](../../../runs/dsv4flash-db-first-full-01/dacomp-058/attempt-01/python/P8.stderr)。检出需人工核验的 SQL 可实现操作：groupby(, .query(, sort_values(；不能仅凭理由判为合规。

P9：Load device and geo data to compare health scores across device types and geographic targets. Also compute monthly trend and YoY growth rates.

[源码](../../../runs/dsv4flash-db-first-full-01/dacomp-058/attempt-01/python/P9.py)；[输出](../../../runs/dsv4flash-db-first-full-01/dacomp-058/attempt-01/python/P9.stdout)；[错误](../../../runs/dsv4flash-db-first-full-01/dacomp-058/attempt-01/python/P9.stderr)。检出需人工核验的 SQL 可实现操作：groupby(, .query(, sort_values(；不能仅凭理由判为合规。

P10：Fix the YoY calculation loop and generate device/geo/trend visualizations. This is statistical analysis (growth rates, seasonal comparison) better handled in pandas.

[源码](../../../runs/dsv4flash-db-first-full-01/dacomp-058/attempt-01/python/P10.py)；[输出](../../../runs/dsv4flash-db-first-full-01/dacomp-058/attempt-01/python/P10.stdout)；[错误](../../../runs/dsv4flash-db-first-full-01/dacomp-058/attempt-01/python/P10.stderr)。检出需人工核验的 SQL 可实现操作：groupby(, .query(, sort_values(；不能仅凭理由判为合规。

P11：Analyze keyword-level performance for problematic campaigns and device/geo breakdowns to formulate targeted optimization recommendations.

[源码](../../../runs/dsv4flash-db-first-full-01/dacomp-058/attempt-01/python/P11.py)；[输出](../../../runs/dsv4flash-db-first-full-01/dacomp-058/attempt-01/python/P11.stdout)；[错误](../../../runs/dsv4flash-db-first-full-01/dacomp-058/attempt-01/python/P11.stderr)。检出需人工核验的 SQL 可实现操作：groupby(, .query(；不能仅凭理由判为合规。

P12：Get geo breakdown for problematic campaigns and compute keyword-level cost-per-conversion to identify underperforming keywords for optimization recommendations.

[源码](../../../runs/dsv4flash-db-first-full-01/dacomp-058/attempt-01/python/P12.py)；[输出](../../../runs/dsv4flash-db-first-full-01/dacomp-058/attempt-01/python/P12.stdout)；[错误](../../../runs/dsv4flash-db-first-full-01/dacomp-058/attempt-01/python/P12.stderr)。检出需人工核验的 SQL 可实现操作：groupby(, .query(, sort_values(；不能仅凭理由判为合规。

P13：Compute trend/seasonality for problematic campaigns, verify screening criteria statistics, and generate the final summary table. This requires time-series decomposition and aggregation best done in pandas.

[源码](../../../runs/dsv4flash-db-first-full-01/dacomp-058/attempt-01/python/P13.py)；[输出](../../../runs/dsv4flash-db-first-full-01/dacomp-058/attempt-01/python/P13.stdout)；[错误](../../../runs/dsv4flash-db-first-full-01/dacomp-058/attempt-01/python/P13.stderr)。检出需人工核验的 SQL 可实现操作：groupby(, .query(；不能仅凭理由判为合规。

P14：Build the final comprehensive optimization recommendations table for each problematic campaign, combining all analysis results.

[源码](../../../runs/dsv4flash-db-first-full-01/dacomp-058/attempt-01/python/P14.py)；[输出](../../../runs/dsv4flash-db-first-full-01/dacomp-058/attempt-01/python/P14.stdout)；[错误](../../../runs/dsv4flash-db-first-full-01/dacomp-058/attempt-01/python/P14.stderr)。检出需人工核验的 SQL 可实现操作：.query(；不能仅凭理由判为合规。

P15：Compute actual conversion_value/cost ratio by device and geo for problematic campaigns to provide meaningful device and geo optimization recommendations, since the roas field is constant but cv/cost varies.

[源码](../../../runs/dsv4flash-db-first-full-01/dacomp-058/attempt-01/python/P15.py)；[输出](../../../runs/dsv4flash-db-first-full-01/dacomp-058/attempt-01/python/P15.stdout)；[错误](../../../runs/dsv4flash-db-first-full-01/dacomp-058/attempt-01/python/P15.stderr)。检出需人工核验的 SQL 可实现操作：.query(, sort_values(；不能仅凭理由判为合规。

P16：Generate final cross-dimension comparison tables and summary statistics for the report. Aggregation and pivoting in pandas for display purposes.

[源码](../../../runs/dsv4flash-db-first-full-01/dacomp-058/attempt-01/python/P16.py)；[输出](../../../runs/dsv4flash-db-first-full-01/dacomp-058/attempt-01/python/P16.stdout)；[错误](../../../runs/dsv4flash-db-first-full-01/dacomp-058/attempt-01/python/P16.stderr)。检出需人工核验的 SQL 可实现操作：groupby(, .query(, sort_values(；不能仅凭理由判为合规。

P17：Create final visualization showing the health score ranking with the three-dimension breakdown and risk levels for all 50 campaigns.

[源码](../../../runs/dsv4flash-db-first-full-01/dacomp-058/attempt-01/python/P17.py)；[输出](../../../runs/dsv4flash-db-first-full-01/dacomp-058/attempt-01/python/P17.stdout)；[错误](../../../runs/dsv4flash-db-first-full-01/dacomp-058/attempt-01/python/P17.stderr)。检出需人工核验的 SQL 可实现操作：.query(, sort_values(；不能仅凭理由判为合规。

P18：Find where figures are saved and check accessibility from workspace.

[源码](../../../runs/dsv4flash-db-first-full-01/dacomp-058/attempt-01/python/P18.py)；[输出](../../../runs/dsv4flash-db-first-full-01/dacomp-058/attempt-01/python/P18.stdout)；[错误](../../../runs/dsv4flash-db-first-full-01/dacomp-058/attempt-01/python/P18.stderr)。自动源码筛查未检出预设迁出信号；这不是全面语义合规证明。

## 优化机会

已验证候选。筛选限于精确 SQL、相同自包含 CTE、相同单表完整过滤、可分解单表聚合；未覆盖任意 Join 等价和一般谓词蕴含。全部候选都是 offline，未测在线预测。

| 候选 | 类型 | 已有结果 | 覆盖 SQL | 后续次数 | 中间行数 | 验证 | 成本 |
| --- | --- | --- | --- | --- | --- | --- | --- |
| C1 | exact-result reuse | True | ["S33", "S34"] | 1 | unknown | not_verified_cap | Not tested |
| C2 | exact-result reuse | True | ["S35", "S38"] | 1 | unknown | not_verified_cap | Not tested |
| C3 | exact-result reuse | True | ["S36", "S39"] | 1 | unknown | not_verified_cap | Not tested |
| C4 | exact-result reuse | True | ["S37", "S40"] | 1 | unknown | not_verified_cap | Not tested |
| C5 | common subexpression | False | ["S29", "S30", "S32", "S33", "S34", "S52", "S57", "S58"] | 7 | 714 | verified | Not benchmarked; correctness alone does not establish net speedup. |
| C6 | aggregate MV | False | ["S6", "S7", "S8", "S10", "S12", "S13", "S16", "S37", "S40", "S49"] | 9 | 683 | rejected_result_mismatch | Not benchmarked; correctness alone does not establish net speedup. |
| C7 | common filtered view | False | ["S15", "S48"] | 1 | unknown | not_verified_cap | Not tested |
| C8 | aggregate MV | False | ["S20", "S27"] | 1 | unknown | not_verified_cap | Not tested |
| C9 | common filtered view | False | ["S42", "S46", "S53", "S55"] | 3 | unknown | not_verified_cap | Not tested |
| C10 | aggregate MV | False | ["S42", "S46", "S53", "S55"] | 3 | 30 | verified | Not benchmarked; correctness alone does not establish net speedup. |
| C11 | common filtered view | False | ["S43", "S54", "S56"] | 2 | unknown | not_verified_cap | Not tested |
| C12 | aggregate MV | False | ["S43", "S54", "S56"] | 2 | unknown | not_verified_cap | Not tested |
| C13 | common filtered view | False | ["S45", "S51"] | 1 | unknown | not_verified_cap | Not tested |


已验证覆盖（含触发查询、候选并集去重）：12/55 条成功数据 SQL。正确性仅针对当前数据库快照；未测性能的候选不能声称已加速。

[完整 build/rewrite 与比较证据](dacomp-058.analysis.json)。

### C5：common subexpression

Identical self-contained CTE body across queries.

原查询 [S29](#s29), [S30](#s30), [S32](#s32), [S33](#s33), [S34](#s34), [S52](#s52), [S57](#s57), [S58](#s58) → 新增共享状态 C5 → 后续 7 次可复用。该构建点为事后假设，不代表 Agent 当时预知后续。

构建定义：

```sql
SELECT year_month, campaign_id, campaign_name, campaign_type, bidding_strategy, industry, cost, conversions, conversion_value, roas, cpc, cost_per_conversion, conversion_rate, quality_score, impression_share, ctr FROM google_ads__campaign_report
```

受益查询 S29 的改写示例（截取前 1600 字符，完整版本见证据 JSON）：

```sql
WITH base AS (SELECT * FROM temp.reuse_candidate), norm AS (SELECT b.*, (b.roas - MIN(b.roas) OVER ()) / NULLIF(MAX(b.roas) OVER () - MIN(b.roas) OVER (), 0) AS roas_s, (MAX(b.cpc) OVER () - b.cpc) / NULLIF(MAX(b.cpc) OVER () - MIN(b.cpc) OVER (), 0) AS cpc_s, (MAX(b.cost_per_conversion) OVER () - b.cost_per_conversion) / NULLIF(MAX(b.cost_per_conversion) OVER () - MIN(b.cost_per_conversion) OVER (), 0) AS cpa_s, (b.conversion_rate - MIN(b.conversion_rate) OVER ()) / NULLIF(MAX(b.conversion_rate) OVER () - MIN(b.conversion_rate) OVER (), 0) AS cvr_s, (b.conversion_value / NULLIF(b.conversions, 0) - MIN(b.conversion_value / NULLIF(b.conversions, 0)) OVER ()) / NULLIF(MAX(b.conversion_value / NULLIF(b.conversions, 0)) OVER () - MIN(b.conversion_value / NULLIF(b.conversions, 0)) OVER (), 0) AS aov_s, (b.conversions - MIN(b.conversions) OVER ()) / NULLIF(MAX(b.conversions) OVER () - MIN(b.conversions) OVER (), 0) AS conv_s, (b.quality_score - MIN(b.quality_score) OVER ()) / NULLIF(MAX(b.quality_score) OVER () - MIN(b.quality_score) OVER (), 0) AS qs_s, (b.impression_share - MIN(b.impression_share) OVER ()) / NULLIF(MAX(b.impression_share) OVER () - MIN(b.impression_share) OVER (), 0) AS is_s, (b.ctr - MIN(b.ctr) OVER ()) / NULLIF(MAX(b.ctr) OVER () - MIN(b.ctr) OVER (), 0) AS ctr_s FROM base AS b) SELECT *, 100.0 * (0.4 * roas_s + 0.3 * cpa_s + 0.3 * cpc_s) AS cost_eff, 100.0 * (0.4 * cvr_s + 0.3 * aov_s + 0.3 * conv_s) AS conv_quality, 100.0 * (0.4 * qs_s + 0.3 * is_s + 0.3 * ctr_s) AS competitive, 100.0 * (0.4 * (0.4 * roas_s + 0.3 * cpa_s + 0.3 * cpc_s) + 0.35 * (0.4 * cvr_s
```

| 原 SQL | 列名一致 | 结果一致 | 比较方法 |
| --- | --- | --- | --- |
| S29 | True | True | ordered_numeric_tolerance |
| S30 | True | True | ordered_numeric_tolerance |
| S32 | True | True | ordered_numeric_tolerance |
| S33 | True | True | ordered_numeric_tolerance |
| S34 | True | True | ordered_numeric_tolerance |
| S52 | True | True | ordered_numeric_tolerance |
| S57 | True | True | ordered_numeric_tolerance |
| S58 | True | True | ordered_numeric_tolerance |


验证状态：verified；成本结论：Not benchmarked; correctness alone does not establish net speedup.

### C10：aggregate MV

Union of grouping keys; decomposable aggregate states; AVG uses SUM and non-NULL COUNT.

原查询 [S42](#s42), [S46](#s46), [S53](#s53), [S55](#s55) → 新增共享状态 C10 → 后续 3 次可复用。该构建点为事后假设，不代表 Agent 当时预知后续。

构建定义：

```sql
SELECT campaign_id AS __g0, device_type AS __g1, SUM(cost) AS __a0, SUM(roas) AS __a1_sum, COUNT(roas) AS __a1_n, SUM(quality_score) AS __a2_sum, COUNT(quality_score) AS __a2_n, SUM(conversion_rate) AS __a3_sum, COUNT(conversion_rate) AS __a3_n, SUM(ctr) AS __a4_sum, COUNT(ctr) AS __a4_n, SUM(conversions) AS __a5, SUM(conversion_value) AS __a6 FROM "google_ads__device_report" WHERE campaign_id IN (105, 135, 36, 184, 180, 56, 69, 148, 178, 27) GROUP BY campaign_id, device_type
```

受益查询 S42 的改写示例：

```sql
SELECT __g0 AS "campaign_id", __g1 AS "device_type", ROUND(SUM(__a0), 0) AS cost, ROUND((1.0 * SUM(__a1_sum) / NULLIF(SUM(__a1_n), 0)), 3) AS avg_roas, ROUND((1.0 * SUM(__a2_sum) / NULLIF(SUM(__a2_n), 0)), 2) AS avg_qs, ROUND((1.0 * SUM(__a3_sum) / NULLIF(SUM(__a3_n), 0)), 5) AS avg_cvr, ROUND((1.0 * SUM(__a4_sum) / NULLIF(SUM(__a4_n), 0)), 5) AS avg_ctr FROM temp.reuse_candidate GROUP BY __g0, __g1 ORDER BY __g0, __g1
```

| 原 SQL | 列名一致 | 结果一致 | 比较方法 |
| --- | --- | --- | --- |
| S42 | True | True | ordered_numeric_tolerance |
| S46 | True | True | ordered_numeric_tolerance |
| S53 | True | True | ordered_numeric_tolerance |
| S55 | True | True | ordered_numeric_tolerance |


验证状态：verified；成本结论：Not benchmarked; correctness alone does not establish net speedup.

### C6：aggregate MV

Union of grouping keys; decomposable aggregate states; AVG uses SUM and non-NULL COUNT.

原查询 [S6](#s6), [S7](#s7), [S8](#s8), [S10](#s10), [S12](#s12), [S13](#s13), [S16](#s16), [S37](#s37), [S40](#s40), [S49](#s49) → 新增共享状态 C6 → 后续 9 次可复用。该构建点为事后假设，不代表 Agent 当时预知后续。

构建定义：

```sql
SELECT campaign_type AS __g0, bidding_strategy AS __g1, industry AS __g2, CASE WHEN cost < 5000 THEN '0-5K' WHEN cost < 10000 THEN '5K-10K' WHEN cost < 30000 THEN '10K-30K' WHEN cost < 50000 THEN '30K-50K' WHEN cost < 100000 THEN '50K-100K' ELSE '100K+' END AS __g3, year_month AS __g4, COUNT(*) AS __a0, COUNT(CASE WHEN cost > 1000 THEN 1 END) AS __a1, MIN(roas) AS __a2, MAX(roas) AS __a3, SUM(roas) AS __a4_sum, COUNT(roas) AS __a4_n, MIN(conversion_value / NULLIF(cost, 0)) AS __a5, MAX(conversion_value / NULLIF(cost, 0)) AS __a6, SUM(conversion_value / NULLIF(cost, 0)) AS __a7_sum, COUNT(conversion_value / NULLIF(cost, 0)) AS __a7_n, SUM(cost) AS __a8_sum, COUNT(cost) AS __a8_n, MIN(cost) AS __a9, MAX(cost) AS __a10, COUNT(CASE WHEN roas < 0.8 THEN 1 END) AS __a11, SUM(cost) AS __a12, SUM(conversions) AS __a13, SUM(conversion_value) AS __a14, SUM(quality_score) AS __a15_sum, COUNT(quality_score) AS __a15_n, SUM(impression_share) AS __a16_sum, COUNT(impression_share) AS __a16_n, SUM(ctr) AS __a17_sum, COUNT(ctr) AS __a17_n, SUM(conversion_rate) AS __a18_sum, COUNT(conversion_rate) AS __a18_n, SUM(CASE WHEN campaign_id IN (105, 135, 36, 184, 180, 56, 69, 148, 178, 27) THEN cost ELSE 0 END) AS __a19 FROM "google_ads__campaign_report"  GROUP BY campaign_type, bidding_strategy, industry, CASE WHEN cost < 5000 THEN '0-5K' WHEN cost < 10000 THEN '5K-10K' WHEN cost < 30000 THEN '10K-30K' WHEN cost < 50000 THEN '30K-50K' WHEN cost < 100000 THEN '50K-100K' ELSE '100K+' END, year_month
```

受益查询 S6 的改写示例：

```sql
SELECT __g0 AS "campaign_type", SUM(__a0) AS n FROM temp.reuse_candidate GROUP BY __g0 ORDER BY n DESC
```

| 原 SQL | 列名一致 | 结果一致 | 比较方法 |
| --- | --- | --- | --- |
| S6 | True | True | ordered_numeric_tolerance |
| S7 | True | True | ordered_numeric_tolerance |
| S8 | True | True | ordered_numeric_tolerance |
| S10 | True | True | exact_multiset |
| S12 | True | False | exact_multiset |
| S13 | True | True | ordered_numeric_tolerance |
| S16 | True | True | exact_multiset |
| S37 | True | True | ordered_numeric_tolerance |
| S40 | True | True | ordered_numeric_tolerance |
| S49 | True | True | exact_multiset |


验证状态：rejected_result_mismatch；成本结论：Not benchmarked; correctness alone does not establish net speedup.

结果依赖：自动记录 SQL→Python 的接口父调用，以及源码中引用归档文件的消费者；字面值相同不认定因果。模型方向选择需要人工读取消息，尚未做全面因果标注。

[原始报告](../../../runs/dsv4flash-db-first-full-01/dacomp-058/attempt-01/answer.md)；[统一消息](../../../runs/dsv4flash-db-first-full-01/dacomp-058/attempt-01/messages.jsonl)；[原始 OpenCode 事件](../../../runs/dsv4flash-db-first-full-01/dacomp-058/attempt-01/opencode.jsonl)；[SQL 引擎日志](../../../runs/dsv4flash-db-first-full-01/dacomp-058/attempt-01/sql_journal.jsonl)。

[可读报告（本地图片链接规范化）](../answers/dacomp-058.md)。原始回答保留，分析结论未改写。

## S1

类别 `connection_setup`；来源 `connection`；调用 `7d853869731e43e295924e399efbe414`；状态 `success`。

```sql
PRAGMA query_only=ON
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-058/attempt-01/sql/S1.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-058/attempt-01/sql/S1.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-058/attempt-01/results/S1.rows.jsonl)；完整：True；SHA256：`e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`。

## S2

类别 `metadata`；来源 `list_db`；调用 `7d853869731e43e295924e399efbe414`；状态 `success`。

```sql
SELECT name,sql FROM sqlite_master WHERE type='table' ORDER BY name
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-058/attempt-01/sql/S2.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-058/attempt-01/sql/S2.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-058/attempt-01/results/S2.rows.jsonl)；完整：True；SHA256：`f27aa44f58b02ea4c9dbf3ffc6574532a3fd2a6b3b1b7e50d761d869aff88ecb`。

## S3

类别 `data`；来源 `query_db`；调用 `609f1d0f7aa742d2ae0674b695d24532`；状态 `success`。

```sql
SELECT 'campaign_report' AS tbl, COUNT(*) AS rows, COUNT(DISTINCT campaign_id) AS campaigns, COUNT(DISTINCT year_month) AS months, MIN(year_month) AS min_m, MAX(year_month) AS max_m FROM google_ads__campaign_report
UNION ALL
SELECT 'device_report', COUNT(*), COUNT(DISTINCT campaign_id), COUNT(DISTINCT year_month), MIN(year_month), MAX(year_month) FROM google_ads__device_report
UNION ALL
SELECT 'geo_report', COUNT(*), COUNT(DISTINCT campaign_id), COUNT(DISTINCT year_month), MIN(year_month), MAX(year_month) FROM google_ads__geo_report
UNION ALL
SELECT 'keyword_report', COUNT(*), COUNT(DISTINCT campaign_id), COUNT(DISTINCT year_quarter), MIN(year_quarter), MAX(year_quarter) FROM google_ads__keyword_report
UNION ALL
SELECT 'campaigns', COUNT(*), COUNT(DISTINCT campaign_id), NULL, NULL, NULL FROM campaigns
UNION ALL
SELECT 'keywords', COUNT(*), COUNT(DISTINCT keyword_id), NULL, NULL, NULL FROM keywords
UNION ALL
SELECT 'ad_groups', COUNT(*), COUNT(DISTINCT ad_group_id), NULL, NULL, NULL FROM ad_groups
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-058/attempt-01/sql/S3.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-058/attempt-01/sql/S3.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-058/attempt-01/results/S3.rows.jsonl)；完整：True；SHA256：`6bdffaa1fe7325535146889df2aa8f4b15aecdac86de18cf41ee8aa40a8ecd15`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "google_ads__campaign_report", "kind": "base", "block": null, "base_tables": ["google_ads__campaign_report"]}] | [] | [] |
| B2 | [{"alias": "google_ads__device_report", "kind": "base", "block": null, "base_tables": ["google_ads__device_report"]}] | [] | [] |
| B3 | [] | [] | [] |
| B4 | [{"alias": "google_ads__geo_report", "kind": "base", "block": null, "base_tables": ["google_ads__geo_report"]}] | [] | [] |
| B5 | [] | [] | [] |
| B6 | [{"alias": "google_ads__keyword_report", "kind": "base", "block": null, "base_tables": ["google_ads__keyword_report"]}] | [] | [] |
| B7 | [] | [] | [] |
| B8 | [{"alias": "campaigns", "kind": "base", "block": null, "base_tables": ["campaigns"]}] | [] | [] |
| B9 | [] | [] | [] |
| B10 | [{"alias": "keywords", "kind": "base", "block": null, "base_tables": ["keywords"]}] | [] | [] |
| B11 | [] | [] | [] |
| B12 | [{"alias": "ad_groups", "kind": "base", "block": null, "base_tables": ["ad_groups"]}] | [] | [] |
| B13 | [] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |
| B1 | COUNT(DISTINCT campaign_id) | [{"table": "google_ads__campaign_report", "column": "campaign_id"}] | [] | False |
| B1 | COUNT(DISTINCT year_month) | [{"table": "google_ads__campaign_report", "column": "year_month"}] | [] | False |
| B1 | MIN(year_month) | [{"table": "google_ads__campaign_report", "column": "year_month"}] | [] | False |
| B1 | MAX(year_month) | [{"table": "google_ads__campaign_report", "column": "year_month"}] | [] | False |
| B2 | COUNT(*) | [] | [] | True |
| B2 | COUNT(DISTINCT campaign_id) | [{"table": "google_ads__device_report", "column": "campaign_id"}] | [] | False |
| B2 | COUNT(DISTINCT year_month) | [{"table": "google_ads__device_report", "column": "year_month"}] | [] | False |
| B2 | MIN(year_month) | [{"table": "google_ads__device_report", "column": "year_month"}] | [] | False |
| B2 | MAX(year_month) | [{"table": "google_ads__device_report", "column": "year_month"}] | [] | False |
| B4 | COUNT(*) | [] | [] | True |
| B4 | COUNT(DISTINCT campaign_id) | [{"table": "google_ads__geo_report", "column": "campaign_id"}] | [] | False |
| B4 | COUNT(DISTINCT year_month) | [{"table": "google_ads__geo_report", "column": "year_month"}] | [] | False |
| B4 | MIN(year_month) | [{"table": "google_ads__geo_report", "column": "year_month"}] | [] | False |
| B4 | MAX(year_month) | [{"table": "google_ads__geo_report", "column": "year_month"}] | [] | False |
| B6 | COUNT(*) | [] | [] | True |
| B6 | COUNT(DISTINCT campaign_id) | [{"table": "google_ads__keyword_report", "column": "campaign_id"}] | [] | False |
| B6 | COUNT(DISTINCT year_quarter) | [{"table": "google_ads__keyword_report", "column": "year_quarter"}] | [] | False |
| B6 | MIN(year_quarter) | [{"table": "google_ads__keyword_report", "column": "year_quarter"}] | [] | False |
| B6 | MAX(year_quarter) | [{"table": "google_ads__keyword_report", "column": "year_quarter"}] | [] | False |
| B8 | COUNT(*) | [] | [] | True |
| B8 | COUNT(DISTINCT campaign_id) | [{"table": "campaigns", "column": "campaign_id"}] | [] | False |
| B10 | COUNT(*) | [] | [] | True |
| B10 | COUNT(DISTINCT keyword_id) | [{"table": "keywords", "column": "keyword_id"}] | [] | False |
| B12 | COUNT(*) | [] | [] | True |
| B12 | COUNT(DISTINCT ad_group_id) | [{"table": "ad_groups", "column": "ad_group_id"}] | [] | False |


## S4

类别 `data`；来源 `query_db`；调用 `7fdb7e0d2fc54da286bf7347e617623f`；状态 `success`。

```sql
SELECT COUNT(*) AS n FROM campaigns c LEFT JOIN google_ads__campaign_report r ON c.campaign_id = r.campaign_id WHERE r.campaign_id IS NULL
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-058/attempt-01/sql/S4.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-058/attempt-01/sql/S4.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-058/attempt-01/results/S4.rows.jsonl)；完整：True；SHA256：`48c320e8238f5f9734818b5a7160e4a0f622a3518ea063063bf3e67385955819`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "c", "kind": "base", "block": null, "base_tables": ["campaigns"]}, {"alias": "r", "kind": "base", "block": null, "base_tables": ["google_ads__campaign_report"]}] | [{"type": "LEFT", "right": "google_ads__campaign_report AS r", "on": "c.campaign_id = r.campaign_id", "using": []}] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |


## S5

类别 `data`；来源 `query_db`；调用 `5cdcbf55c2fd4342808a1e335e62635c`；状态 `success`。

```sql
SELECT MIN(start_date) AS min_start, MAX(start_date) AS max_start, COUNT(*) AS total, COUNT(CASE WHEN start_date IS NULL THEN 1 END) AS null_start FROM campaigns
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-058/attempt-01/sql/S5.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-058/attempt-01/sql/S5.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-058/attempt-01/results/S5.rows.jsonl)；完整：True；SHA256：`e0bf43a9993a0ff721b8d6f9ab54bbf62d487626324e65dceadcc117df098cff`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "campaigns", "kind": "base", "block": null, "base_tables": ["campaigns"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | MIN(start_date) | [{"table": "campaigns", "column": "start_date"}] | [] | False |
| B1 | MAX(start_date) | [{"table": "campaigns", "column": "start_date"}] | [] | False |
| B1 | COUNT(*) | [] | [] | True |
| B1 | COUNT(CASE WHEN start_date IS NULL THEN 1 END) | [] | [{"table": "campaigns", "column": "start_date"}] | False |


## S6

类别 `data`；来源 `query_db`；调用 `6e0ccbec930a484494e67bb5dff26e14`；状态 `success`。

```sql
SELECT campaign_type, COUNT(*) AS n FROM google_ads__campaign_report GROUP BY campaign_type ORDER BY n DESC
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-058/attempt-01/sql/S6.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-058/attempt-01/sql/S6.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-058/attempt-01/results/S6.rows.jsonl)；完整：True；SHA256：`d7a3f182408877924ab263f79bee0d3005a4b1cb424d869672c91af31dc9fdb2`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "google_ads__campaign_report", "kind": "base", "block": null, "base_tables": ["google_ads__campaign_report"]}] | [] | ["campaign_type"] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |


## S7

类别 `data`；来源 `query_db`；调用 `8c63bf30f6794fbc93cb9ff46a45f2ac`；状态 `success`。

```sql
SELECT bidding_strategy, COUNT(*) AS n FROM google_ads__campaign_report GROUP BY bidding_strategy ORDER BY n DESC
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-058/attempt-01/sql/S7.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-058/attempt-01/sql/S7.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-058/attempt-01/results/S7.rows.jsonl)；完整：True；SHA256：`a2cc5284beee72ea6c4bc125f77678db49de1bab07a8457cd4059a9bfdc55be5`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "google_ads__campaign_report", "kind": "base", "block": null, "base_tables": ["google_ads__campaign_report"]}] | [] | ["bidding_strategy"] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |


## S8

类别 `data`；来源 `query_db`；调用 `220f75c5d7c743f3b4ee6fa3f4760c0c`；状态 `success`。

```sql
SELECT industry, COUNT(*) AS n FROM google_ads__campaign_report GROUP BY industry ORDER BY n DESC
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-058/attempt-01/sql/S8.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-058/attempt-01/sql/S8.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-058/attempt-01/results/S8.rows.jsonl)；完整：True；SHA256：`a1655842508a4f4b06cd9f391acf4c2e8a24f30277d3f3aaec663a55036b905c`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "google_ads__campaign_report", "kind": "base", "block": null, "base_tables": ["google_ads__campaign_report"]}] | [] | ["industry"] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |


## S9

类别 `data`；来源 `query_db`；调用 `56dd5eb97cd74df9ab11ea0ddb5bffb9`；状态 `success`。

```sql
SELECT
  campaign_id, campaign_name, campaign_type, bidding_strategy, industry,
  COUNT(*) AS n_months,
  SUM(cost) AS total_cost,
  SUM(conversions) AS total_conversions,
  SUM(conversion_value) AS total_cv,
  ROUND(SUM(conversion_value)/NULLIF(SUM(cost),0),4) AS roi,
  ROUND(AVG(quality_score),2) AS avg_qs,
  ROUND(AVG(impression_share),3) AS avg_is,
  ROUND(AVG(ctr),4) AS avg_ctr,
  ROUND(AVG(conversion_rate),4) AS avg_cvr
FROM google_ads__campaign_report
GROUP BY campaign_id
ORDER BY total_cost DESC
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-058/attempt-01/sql/S9.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-058/attempt-01/sql/S9.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-058/attempt-01/results/S9.rows.jsonl)；完整：True；SHA256：`2db6e72e13eced02686718cb64c0307df23340f4ed48c0424b8369a3acc32f77`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "google_ads__campaign_report", "kind": "base", "block": null, "base_tables": ["google_ads__campaign_report"]}] | [] | ["campaign_id"] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |
| B1 | SUM(cost) | [{"table": "google_ads__campaign_report", "column": "cost"}] | [] | False |
| B1 | SUM(conversions) | [{"table": "google_ads__campaign_report", "column": "conversions"}] | [] | False |
| B1 | SUM(conversion_value) | [{"table": "google_ads__campaign_report", "column": "conversion_value"}] | [] | False |
| B1 | AVG(quality_score) | [{"table": "google_ads__campaign_report", "column": "quality_score"}] | [] | False |
| B1 | AVG(impression_share) | [{"table": "google_ads__campaign_report", "column": "impression_share"}] | [] | False |
| B1 | AVG(ctr) | [{"table": "google_ads__campaign_report", "column": "ctr"}] | [] | False |
| B1 | AVG(conversion_rate) | [{"table": "google_ads__campaign_report", "column": "conversion_rate"}] | [] | False |
| B1 | SUM(conversion_value) | [{"table": "google_ads__campaign_report", "column": "conversion_value"}] | [] | False |
| B1 | SUM(cost) | [{"table": "google_ads__campaign_report", "column": "cost"}] | [] | False |


## S10

类别 `data`；来源 `query_db`；调用 `064c3e32f7b34ecabd5f48a950e028e9`；状态 `success`。

```sql
SELECT COUNT(*) AS total_months, COUNT(CASE WHEN cost > 1000 THEN 1 END) AS high_cost_months FROM google_ads__campaign_report
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-058/attempt-01/sql/S10.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-058/attempt-01/sql/S10.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-058/attempt-01/results/S10.rows.jsonl)；完整：True；SHA256：`08a94b882d5bd23d2c6f59da297b2bca6f7482fde64bde7e08b5d3bb002fc04d`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "google_ads__campaign_report", "kind": "base", "block": null, "base_tables": ["google_ads__campaign_report"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |
| B1 | COUNT(CASE WHEN cost > 1000 THEN 1 END) | [] | [{"table": "google_ads__campaign_report", "column": "cost"}] | False |


## S11

类别 `data`；来源 `query_db`；调用 `4809916be4264acda25983328cc5dd4d`；状态 `success`。

```sql
-- Monthly cost > 1000 and ROI < 0.8 (using conversion_value/cost as ROI)
SELECT cr.*, ROUND(cr.conversion_value/NULLIF(cr.cost,0),4) AS roi
FROM google_ads__campaign_report cr
WHERE cr.cost > 1000
  AND (cr.conversion_value/NULLIF(cr.cost,0)) < 0.8
ORDER BY cr.cost DESC
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-058/attempt-01/sql/S11.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-058/attempt-01/sql/S11.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-058/attempt-01/results/S11.rows.jsonl)；完整：True；SHA256：`a6430307ea6f3e96c587a1f24eb515914de265cc226065596dc146d5937bdf42`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "cr", "kind": "base", "block": null, "base_tables": ["google_ads__campaign_report"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |


## S12

类别 `data`；来源 `query_db`；调用 `12d2375802764272966a3be25d84c985`；状态 `success`。

```sql
SELECT
  MIN(roas) AS min_roas, 
  MAX(roas) AS max_roas,
  AVG(roas) AS avg_roas,
  MIN(conversion_value/NULLIF(cost,0)) AS min_roi_cv,
  MAX(conversion_value/NULLIF(cost,0)) AS max_roi_cv,
  AVG(conversion_value/NULLIF(cost,0)) AS avg_roi_cv,
  AVG(cost) AS avg_cost,
  MIN(cost) AS min_cost,
  MAX(cost) AS max_cost
FROM google_ads__campaign_report
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-058/attempt-01/sql/S12.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-058/attempt-01/sql/S12.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-058/attempt-01/results/S12.rows.jsonl)；完整：True；SHA256：`53c6b1ac066b669402747477c55c92c4bf537783a99ee2b3bed800701d8443b5`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "google_ads__campaign_report", "kind": "base", "block": null, "base_tables": ["google_ads__campaign_report"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | MIN(roas) | [{"table": "google_ads__campaign_report", "column": "roas"}] | [] | False |
| B1 | MAX(roas) | [{"table": "google_ads__campaign_report", "column": "roas"}] | [] | False |
| B1 | AVG(roas) | [{"table": "google_ads__campaign_report", "column": "roas"}] | [] | False |
| B1 | MIN(conversion_value / NULLIF(cost, 0)) | [{"table": "google_ads__campaign_report", "column": "conversion_value"}, {"table": "google_ads__campaign_report", "column": "cost"}] | [] | False |
| B1 | MAX(conversion_value / NULLIF(cost, 0)) | [{"table": "google_ads__campaign_report", "column": "conversion_value"}, {"table": "google_ads__campaign_report", "column": "cost"}] | [] | False |
| B1 | AVG(conversion_value / NULLIF(cost, 0)) | [{"table": "google_ads__campaign_report", "column": "conversion_value"}, {"table": "google_ads__campaign_report", "column": "cost"}] | [] | False |
| B1 | AVG(cost) | [{"table": "google_ads__campaign_report", "column": "cost"}] | [] | False |
| B1 | MIN(cost) | [{"table": "google_ads__campaign_report", "column": "cost"}] | [] | False |
| B1 | MAX(cost) | [{"table": "google_ads__campaign_report", "column": "cost"}] | [] | False |


## S13

类别 `data`；来源 `query_db`；调用 `053665afaf854e68b161ee56d57ef13e`；状态 `success`。

```sql
-- Check cost distribution
SELECT 
  CASE 
    WHEN cost < 5000 THEN '0-5K'
    WHEN cost < 10000 THEN '5K-10K'
    WHEN cost < 30000 THEN '10K-30K'
    WHEN cost < 50000 THEN '30K-50K'
    WHEN cost < 100000 THEN '50K-100K'
    ELSE '100K+'
  END AS cost_range,
  COUNT(*) AS n_months,
  ROUND(AVG(conversion_value/NULLIF(cost,0)),3) AS avg_roi,
  ROUND(AVG(roas),3) AS avg_roas
FROM google_ads__campaign_report
GROUP BY cost_range
ORDER BY MIN(cost)
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-058/attempt-01/sql/S13.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-058/attempt-01/sql/S13.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-058/attempt-01/results/S13.rows.jsonl)；完整：True；SHA256：`125c5db02f8f5658359829bffbef44371e7c8f80958c0a35d364b2fc621b6148`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "google_ads__campaign_report", "kind": "base", "block": null, "base_tables": ["google_ads__campaign_report"]}] | [] | ["CASE WHEN cost < 5000 THEN '0-5K' WHEN cost < 10000 THEN '5K-10K' WHEN cost < 30000 THEN '10K-30K' WHEN cost < 50000 THEN '30K-50K' WHEN cost < 100000 THEN '50K-100K' ELSE '100K+' END"] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |
| B1 | AVG(conversion_value / NULLIF(cost, 0)) | [{"table": "google_ads__campaign_report", "column": "conversion_value"}, {"table": "google_ads__campaign_report", "column": "cost"}] | [] | False |
| B1 | AVG(roas) | [{"table": "google_ads__campaign_report", "column": "roas"}] | [] | False |
| B1 | MIN(cost) | [{"table": "google_ads__campaign_report", "column": "cost"}] | [] | False |


## S14

类别 `data`；来源 `query_db`；调用 `d49f1664e219471db8b4c6f330a56874`；状态 `failed`。

```sql
SELECT
  COUNT(CASE WHEN roas < 0.8 THEN 1 END) AS roas_lt_08,
  COUNT(CASE WHEN (conversion_value/NULLIF(cost,0)) < 0.8 THEN 1 END) AS cv_cost_lt_08,
  COUNT(CASE WHEN roas < 0.8 AND (conversion_value/NULLIF(cost,0)) >= 0.8 THEN 1 END) AS mismatch,
  ROUND(AVG(ABS(roas - conversion_value/NULLIF(cost,0))),4) AS avg_abs_diff,
  ROUND(CORR(roas, conversion_value/NULLIF(cost,0)),4) AS corr
FROM google_ads__campaign_report
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-058/attempt-01/sql/S14.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-058/attempt-01/sql/S14.parameters.json)。

错误：`OperationalError('no such function: CORR')`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "google_ads__campaign_report", "kind": "base", "block": null, "base_tables": ["google_ads__campaign_report"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(CASE WHEN roas < 0.8 THEN 1 END) | [] | [{"table": "google_ads__campaign_report", "column": "roas"}] | False |
| B1 | COUNT(CASE WHEN (conversion_value / NULLIF(cost, 0)) < 0.8 THEN 1 END) | [] | [{"table": "google_ads__campaign_report", "column": "conversion_value"}, {"table": "google_ads__campaign_report", "column": "cost"}] | False |
| B1 | COUNT(CASE WHEN roas < 0.8 AND (conversion_value / NULLIF(cost, 0)) >= 0.8 THEN 1 END) | [] | [{"table": "google_ads__campaign_report", "column": "roas"}, {"table": "google_ads__campaign_report", "column": "conversion_value"}, {"table": "google_ads__campaign_report", "column": "cost"}] | False |
| B1 | AVG(ABS(roas - conversion_value / NULLIF(cost, 0))) | [{"table": "google_ads__campaign_report", "column": "roas"}, {"table": "google_ads__campaign_report", "column": "conversion_value"}, {"table": "google_ads__campaign_report", "column": "cost"}] | [] | False |
| B1 | CORR(roas, conversion_value / NULLIF(cost, 0)) | [{"table": "google_ads__campaign_report", "column": "roas"}, {"table": "google_ads__campaign_report", "column": "conversion_value"}, {"table": "google_ads__campaign_report", "column": "cost"}] | [] | False |


## S15

类别 `data`；来源 `query_db`；调用 `df038f0093db4941a280e6a11e9a22c8`；状态 `success`。

```sql
-- Count of months with roas<0.8 grouped by campaign
SELECT campaign_id, campaign_name, campaign_type, bidding_strategy, industry,
  COUNT(*) AS bad_months, 
  COUNT(CASE WHEN roas >= 0.8 THEN 1 END) AS good_months,
  ROUND(AVG(roas),3) AS avg_roas,
  ROUND(AVG(conversion_value/NULLIF(cost,0)),3) AS avg_cv_ratio
FROM google_ads__campaign_report
WHERE roas < 0.8
GROUP BY campaign_id
ORDER BY bad_months DESC
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-058/attempt-01/sql/S15.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-058/attempt-01/sql/S15.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-058/attempt-01/results/S15.rows.jsonl)；完整：True；SHA256：`a1a0fe838d918a86f4efe915e8493a1c5ee7088fc179b4cfd08dea3d707526f5`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "google_ads__campaign_report", "kind": "base", "block": null, "base_tables": ["google_ads__campaign_report"]}] | [] | ["campaign_id"] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |
| B1 | COUNT(CASE WHEN roas >= 0.8 THEN 1 END) | [] | [{"table": "google_ads__campaign_report", "column": "roas"}] | False |
| B1 | AVG(roas) | [{"table": "google_ads__campaign_report", "column": "roas"}] | [] | False |
| B1 | AVG(conversion_value / NULLIF(cost, 0)) | [{"table": "google_ads__campaign_report", "column": "conversion_value"}, {"table": "google_ads__campaign_report", "column": "cost"}] | [] | False |


## S16

类别 `data`；来源 `query_db`；调用 `ac93b73cd5b342a4bd416d9bebbedc65`；状态 `success`。

```sql
SELECT 
  COUNT(*) AS total,
  COUNT(CASE WHEN roas < 0.8 THEN 1 END) AS roas_lt_08,
  ROUND(100.0 * COUNT(CASE WHEN roas < 0.8 THEN 1 END) / COUNT(*), 1) AS pct_lt_08
FROM google_ads__campaign_report
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-058/attempt-01/sql/S16.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-058/attempt-01/sql/S16.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-058/attempt-01/results/S16.rows.jsonl)；完整：True；SHA256：`29a19b59f50dce7179d9f5e146a6c28f2ae3209a44761f2f209d3e3a8f613cd3`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "google_ads__campaign_report", "kind": "base", "block": null, "base_tables": ["google_ads__campaign_report"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |
| B1 | COUNT(CASE WHEN roas < 0.8 THEN 1 END) | [] | [{"table": "google_ads__campaign_report", "column": "roas"}] | False |
| B1 | COUNT(*) | [] | [] | True |
| B1 | COUNT(CASE WHEN roas < 0.8 THEN 1 END) | [] | [{"table": "google_ads__campaign_report", "column": "roas"}] | False |


## S17

类别 `data`；来源 `query_db`；调用 `978fc4edf99d448ab43758879a459900`；状态 `success`。

```sql
-- roas distribution
SELECT 
  CASE 
    WHEN roas < 0.3 THEN '<0.3'
    WHEN roas < 0.5 THEN '0.3-0.5'
    WHEN roas < 0.7 THEN '0.5-0.7'
    WHEN roas < 0.8 THEN '0.7-0.8'
    WHEN roas < 1.0 THEN '0.8-1.0'
    WHEN roas < 2.0 THEN '1.0-2.0'
    ELSE '2.0+'
  END AS roas_range,
  COUNT(*) AS n,
  ROUND(100.0 * COUNT(*) / SUM(COUNT(*)) OVER(), 1) AS pct,
  ROUND(AVG(cost), 0) AS avg_cost,
  ROUND(AVG(conversion_value), 0) AS avg_cv
FROM google_ads__campaign_report
GROUP BY roas_range
ORDER BY MIN(roas)
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-058/attempt-01/sql/S17.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-058/attempt-01/sql/S17.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-058/attempt-01/results/S17.rows.jsonl)；完整：True；SHA256：`da4c167952dfb701452df1e02fda2f1b5423bb535fa05d63d5916d432fbbfe06`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "google_ads__campaign_report", "kind": "base", "block": null, "base_tables": ["google_ads__campaign_report"]}] | [] | ["CASE WHEN roas < 0.3 THEN '<0.3' WHEN roas < 0.5 THEN '0.3-0.5' WHEN roas < 0.7 THEN '0.5-0.7' WHEN roas < 0.8 THEN '0.7-0.8' WHEN roas < 1.0 THEN '0.8-1.0' WHEN roas < 2.0 THEN '1.0-2.0' ELSE '2.0+' END"] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |
| B1 | AVG(cost) | [{"table": "google_ads__campaign_report", "column": "cost"}] | [] | False |
| B1 | AVG(conversion_value) | [{"table": "google_ads__campaign_report", "column": "conversion_value"}] | [] | False |
| B1 | MIN(roas) | [{"table": "google_ads__campaign_report", "column": "roas"}] | [] | False |
| B1 | COUNT(*) | [] | [] | True |
| B1 | COUNT(*) | [] | [] | True |


## S18

类别 `data`；来源 `query_db`；调用 `b0e5dd7d681e4435ba60b971ff81dda2`；状态 `success`。

```sql
SELECT device_type, COUNT(*) AS n, ROUND(SUM(cost),0) AS cost, ROUND(AVG(roas),3) AS avg_roas FROM google_ads__device_report GROUP BY device_type ORDER BY n DESC
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-058/attempt-01/sql/S18.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-058/attempt-01/sql/S18.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-058/attempt-01/results/S18.rows.jsonl)；完整：True；SHA256：`dd7e549eaf4028ef7342199f2e80e3117f6b915d821007bffb161f881949ca4f`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "google_ads__device_report", "kind": "base", "block": null, "base_tables": ["google_ads__device_report"]}] | [] | ["device_type"] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |
| B1 | SUM(cost) | [{"table": "google_ads__device_report", "column": "cost"}] | [] | False |
| B1 | AVG(roas) | [{"table": "google_ads__device_report", "column": "roas"}] | [] | False |


## S19

类别 `data`；来源 `query_db`；调用 `66f641dbde064a298cd5d701b56e4e17`；状态 `success`。

```sql
SELECT geo_target, COUNT(*) AS n, ROUND(SUM(cost),0) AS cost, ROUND(AVG(roas),3) AS avg_roas FROM google_ads__geo_report GROUP BY geo_target ORDER BY n DESC
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-058/attempt-01/sql/S19.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-058/attempt-01/sql/S19.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-058/attempt-01/results/S19.rows.jsonl)；完整：True；SHA256：`687725a2dfc07516dc5d04c17f43caf296be0208188b022767f37183a8b6767e`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "google_ads__geo_report", "kind": "base", "block": null, "base_tables": ["google_ads__geo_report"]}] | [] | ["geo_target"] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |
| B1 | SUM(cost) | [{"table": "google_ads__geo_report", "column": "cost"}] | [] | False |
| B1 | AVG(roas) | [{"table": "google_ads__geo_report", "column": "roas"}] | [] | False |


## S20

类别 `data`；来源 `query_db`；调用 `217d1ddf284e43408da3e7ec9fef9717`；状态 `success`。

```sql
SELECT match_type, COUNT(*) AS n, ROUND(AVG(avg_position),2) AS avg_pos, ROUND(AVG(quality_score),2) AS avg_qs, ROUND(AVG(roas),3) AS avg_roas FROM google_ads__keyword_report GROUP BY match_type ORDER BY n DESC
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-058/attempt-01/sql/S20.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-058/attempt-01/sql/S20.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-058/attempt-01/results/S20.rows.jsonl)；完整：True；SHA256：`bcfc194a58ea8ad2988ffce1294efa02e646814851c5fb2b5fa435da69df45a8`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "google_ads__keyword_report", "kind": "base", "block": null, "base_tables": ["google_ads__keyword_report"]}] | [] | ["match_type"] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |
| B1 | AVG(avg_position) | [{"table": "google_ads__keyword_report", "column": "avg_position"}] | [] | False |
| B1 | AVG(quality_score) | [{"table": "google_ads__keyword_report", "column": "quality_score"}] | [] | False |
| B1 | AVG(roas) | [{"table": "google_ads__keyword_report", "column": "roas"}] | [] | False |


## S21

类别 `data`；来源 `query_db`；调用 `6b2eecd21e6b48ad90b9764e81a7b5ff`；状态 `success`。

```sql
-- Campaign-level summary with all metrics needed
SELECT 
  campaign_id,
  campaign_name,
  campaign_type,
  bidding_strategy,
  industry,
  COUNT(*) AS n_months,
  MIN(year_month) AS first_month,
  MAX(year_month) AS last_month,
  ROUND(SUM(cost), 2) AS total_cost,
  ROUND(AVG(cost), 0) AS avg_monthly_cost,
  ROUND(SUM(conversions), 2) AS total_conversions,
  ROUND(SUM(conversion_value), 2) AS total_cv,
  ROUND(SUM(conversion_value)/NULLIF(SUM(cost),0), 4) AS overall_roi,
  ROUND(AVG(roas), 4) AS avg_roas,
  ROUND(AVG(quality_score), 2) AS avg_quality_score,
  ROUND(AVG(impression_share), 4) AS avg_impression_share,
  ROUND(AVG(ctr), 5) AS avg_ctr,
  ROUND(AVG(conversion_rate), 5) AS avg_conversion_rate,
  ROUND(AVG(cpc), 2) AS avg_cpc,
  ROUND(AVG(cost_per_conversion), 2) AS avg_cost_per_conv,
  -- Count of months with roas < 0.8
  COUNT(CASE WHEN roas < 0.8 THEN 1 END) AS bad_roas_months,
  ROUND(100.0 * COUNT(CASE WHEN roas < 0.8 THEN 1 END) / COUNT(*), 1) AS pct_bad_roas
FROM google_ads__campaign_report
GROUP BY campaign_id
ORDER BY total_cost DESC
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-058/attempt-01/sql/S21.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-058/attempt-01/sql/S21.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-058/attempt-01/results/S21.rows.jsonl)；完整：True；SHA256：`d1a0c30130060caa47d40edc0cd457321511be28d8bf01b505eb4ccdfe1e3934`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "google_ads__campaign_report", "kind": "base", "block": null, "base_tables": ["google_ads__campaign_report"]}] | [] | ["campaign_id"] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |
| B1 | MIN(year_month) | [{"table": "google_ads__campaign_report", "column": "year_month"}] | [] | False |
| B1 | MAX(year_month) | [{"table": "google_ads__campaign_report", "column": "year_month"}] | [] | False |
| B1 | COUNT(CASE WHEN roas < 0.8 THEN 1 END) | [] | [{"table": "google_ads__campaign_report", "column": "roas"}] | False |
| B1 | SUM(cost) | [{"table": "google_ads__campaign_report", "column": "cost"}] | [] | False |
| B1 | AVG(cost) | [{"table": "google_ads__campaign_report", "column": "cost"}] | [] | False |
| B1 | SUM(conversions) | [{"table": "google_ads__campaign_report", "column": "conversions"}] | [] | False |
| B1 | SUM(conversion_value) | [{"table": "google_ads__campaign_report", "column": "conversion_value"}] | [] | False |
| B1 | AVG(roas) | [{"table": "google_ads__campaign_report", "column": "roas"}] | [] | False |
| B1 | AVG(quality_score) | [{"table": "google_ads__campaign_report", "column": "quality_score"}] | [] | False |
| B1 | AVG(impression_share) | [{"table": "google_ads__campaign_report", "column": "impression_share"}] | [] | False |
| B1 | AVG(ctr) | [{"table": "google_ads__campaign_report", "column": "ctr"}] | [] | False |
| B1 | AVG(conversion_rate) | [{"table": "google_ads__campaign_report", "column": "conversion_rate"}] | [] | False |
| B1 | AVG(cpc) | [{"table": "google_ads__campaign_report", "column": "cpc"}] | [] | False |
| B1 | AVG(cost_per_conversion) | [{"table": "google_ads__campaign_report", "column": "cost_per_conversion"}] | [] | False |
| B1 | SUM(conversion_value) | [{"table": "google_ads__campaign_report", "column": "conversion_value"}] | [] | False |
| B1 | COUNT(*) | [] | [] | True |
| B1 | SUM(cost) | [{"table": "google_ads__campaign_report", "column": "cost"}] | [] | False |
| B1 | COUNT(CASE WHEN roas < 0.8 THEN 1 END) | [] | [{"table": "google_ads__campaign_report", "column": "roas"}] | False |


## S22

类别 `data`；来源 `query_db`；调用 `5dbbbff365b74c07b58660d0507f6af7`；状态 `success`。

```sql
SELECT year_month, cost, conversions, conversion_value, roas, 
  ROUND(conversion_value/NULLIF(cost,0), 4) AS computed_roas
FROM google_ads__campaign_report
WHERE campaign_id = 69
ORDER BY year_month
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-058/attempt-01/sql/S22.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-058/attempt-01/sql/S22.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-058/attempt-01/results/S22.rows.jsonl)；完整：True；SHA256：`6a7cd13ee4ce7de7049dd6768cd843691ae1bc0c78f3861b1052fa5a13fa1d81`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "google_ads__campaign_report", "kind": "base", "block": null, "base_tables": ["google_ads__campaign_report"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |


## S23

类别 `data`；来源 `query_db`；调用 `4815555383d64a70811de60deb52a7a3`；状态 `success`。

```sql
SELECT year_month, cost, conversions, conversion_value, roas, 
  ROUND(conversion_value/NULLIF(cost,0), 4) AS computed_roas
FROM google_ads__campaign_report
WHERE campaign_id = 150
ORDER BY year_month
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-058/attempt-01/sql/S23.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-058/attempt-01/sql/S23.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-058/attempt-01/results/S23.rows.jsonl)；完整：True；SHA256：`2b4c6e954ace2d49d675e55e608afd33ca9032989e16ca3e5a4d20e9b5cdbd2a`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "google_ads__campaign_report", "kind": "base", "block": null, "base_tables": ["google_ads__campaign_report"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |


## S24

类别 `data`；来源 `query_db`；调用 `5f3041692c4e43afb3c62b93a2839135`；状态 `success`。

```sql
-- Compare roas field with computed ratio: check if roas field is constant per campaign
SELECT campaign_id, COUNT(DISTINCT roas) AS distinct_roas, MIN(roas) AS min_roas, MAX(roas) AS max_roas,
  ROUND(MAX(roas) - MIN(roas), 3) AS roas_range,
  ROUND(AVG(roas), 3) AS avg_roas_field,
  ROUND(AVG(conversion_value/NULLIF(cost,0)), 3) AS avg_computed
FROM google_ads__campaign_report
GROUP BY campaign_id
ORDER BY roas_range DESC
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-058/attempt-01/sql/S24.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-058/attempt-01/sql/S24.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-058/attempt-01/results/S24.rows.jsonl)；完整：True；SHA256：`3b7efd23b9a11922fde4eacc814f277ad7128ab7c4aa19ab683786081df7c65f`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "google_ads__campaign_report", "kind": "base", "block": null, "base_tables": ["google_ads__campaign_report"]}] | [] | ["campaign_id"] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(DISTINCT roas) | [{"table": "google_ads__campaign_report", "column": "roas"}] | [] | False |
| B1 | MIN(roas) | [{"table": "google_ads__campaign_report", "column": "roas"}] | [] | False |
| B1 | MAX(roas) | [{"table": "google_ads__campaign_report", "column": "roas"}] | [] | False |
| B1 | AVG(roas) | [{"table": "google_ads__campaign_report", "column": "roas"}] | [] | False |
| B1 | AVG(conversion_value / NULLIF(cost, 0)) | [{"table": "google_ads__campaign_report", "column": "conversion_value"}, {"table": "google_ads__campaign_report", "column": "cost"}] | [] | False |
| B1 | MAX(roas) | [{"table": "google_ads__campaign_report", "column": "roas"}] | [] | False |
| B1 | MIN(roas) | [{"table": "google_ads__campaign_report", "column": "roas"}] | [] | False |


## S25

类别 `data`；来源 `query_db`；调用 `87d0061893744566a24085028797dad3`；状态 `success`。

```sql
-- Campaigns where roas field is nearly constant (low range)
SELECT campaign_id, COUNT(DISTINCT roas) AS distinct_roas, MIN(roas) AS min_roas, MAX(roas) AS max_roas,
  ROUND(MAX(roas) - MIN(roas), 3) AS roas_range,
  ROUND(AVG(roas), 3) AS avg_roas_field,
  ROUND(AVG(conversion_value/NULLIF(cost,0)), 3) AS avg_computed,
  ROUND(AVG(cost), 0) AS avg_monthly_cost
FROM google_ads__campaign_report
GROUP BY campaign_id
HAVING roas_range < 0.1
ORDER BY avg_roas_field
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-058/attempt-01/sql/S25.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-058/attempt-01/sql/S25.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-058/attempt-01/results/S25.rows.jsonl)；完整：True；SHA256：`9ba2c1beb5cfe4340955f0a5009d298ba766f9bde66bd8c91071c025bc127175`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "google_ads__campaign_report", "kind": "base", "block": null, "base_tables": ["google_ads__campaign_report"]}] | [] | ["campaign_id"] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(DISTINCT roas) | [{"table": "google_ads__campaign_report", "column": "roas"}] | [] | False |
| B1 | MIN(roas) | [{"table": "google_ads__campaign_report", "column": "roas"}] | [] | False |
| B1 | MAX(roas) | [{"table": "google_ads__campaign_report", "column": "roas"}] | [] | False |
| B1 | AVG(roas) | [{"table": "google_ads__campaign_report", "column": "roas"}] | [] | False |
| B1 | AVG(conversion_value / NULLIF(cost, 0)) | [{"table": "google_ads__campaign_report", "column": "conversion_value"}, {"table": "google_ads__campaign_report", "column": "cost"}] | [] | False |
| B1 | AVG(cost) | [{"table": "google_ads__campaign_report", "column": "cost"}] | [] | False |
| B1 | MAX(roas) | [{"table": "google_ads__campaign_report", "column": "roas"}] | [] | False |
| B1 | MIN(roas) | [{"table": "google_ads__campaign_report", "column": "roas"}] | [] | False |


## S26

类别 `data`；来源 `query_db`；调用 `b2e2ee2c1ae84653a6945c2472afadb5`；状态 `success`。

```sql
-- Get all campaign-month data for health scoring
SELECT * FROM google_ads__campaign_report ORDER BY campaign_id, year_month
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-058/attempt-01/sql/S26.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-058/attempt-01/sql/S26.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-058/attempt-01/results/S26.rows.jsonl)；完整：True；SHA256：`b853b8556eea7a427b130fd7e152714e18373485d41edf8d0b721a80f8eb5e12`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "google_ads__campaign_report", "kind": "base", "block": null, "base_tables": ["google_ads__campaign_report"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |


## S27

类别 `data`；来源 `query_db`；调用 `56edbbf8d21d49cbadbc3bf83005b2e2`；状态 `success`。

```sql
-- Get keyword-level data for avg_position
SELECT campaign_id, AVG(avg_position) AS avg_position FROM google_ads__keyword_report GROUP BY campaign_id
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-058/attempt-01/sql/S27.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-058/attempt-01/sql/S27.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-058/attempt-01/results/S27.rows.jsonl)；完整：True；SHA256：`22e8908f840ecc6f7967ec550211f9ba2076016f774c5ac513712ac4519edda4`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "google_ads__keyword_report", "kind": "base", "block": null, "base_tables": ["google_ads__keyword_report"]}] | [] | ["campaign_id"] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | AVG(avg_position) | [{"table": "google_ads__keyword_report", "column": "avg_position"}] | [] | False |


## S28

类别 `data`；来源 `query_db`；调用 `e88c2de95fac4d36865445e997e0ad84`；状态 `success`。

```sql
SELECT DISTINCT campaign_id FROM google_ads__keyword_report ORDER BY campaign_id
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-058/attempt-01/sql/S28.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-058/attempt-01/sql/S28.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-058/attempt-01/results/S28.rows.jsonl)；完整：True；SHA256：`b60c2cce2ce3dad0e916f70e81e7276739800e7b5e922ecb3d95db27a312f552`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "google_ads__keyword_report", "kind": "base", "block": null, "base_tables": ["google_ads__keyword_report"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |


## S29

类别 `data`；来源 `query_db`；调用 `ed932731c7e8483caf67498fc2c6d2f5`；状态 `success`。

```sql
WITH base AS (
  SELECT 
    year_month, campaign_id, campaign_name, campaign_type, bidding_strategy, industry,
    cost, conversions, conversion_value, roas, cpc, cost_per_conversion,
    conversion_rate, quality_score, impression_share, ctr
  FROM google_ads__campaign_report
),
norm AS (
  SELECT b.*,
    (b.roas - MIN(b.roas) OVER()) / NULLIF(MAX(b.roas) OVER() - MIN(b.roas) OVER(), 0) AS roas_s,
    (MAX(b.cpc) OVER() - b.cpc) / NULLIF(MAX(b.cpc) OVER() - MIN(b.cpc) OVER(), 0) AS cpc_s,
    (MAX(b.cost_per_conversion) OVER() - b.cost_per_conversion) / NULLIF(MAX(b.cost_per_conversion) OVER() - MIN(b.cost_per_conversion) OVER(), 0) AS cpa_s,
    (b.conversion_rate - MIN(b.conversion_rate) OVER()) / NULLIF(MAX(b.conversion_rate) OVER() - MIN(b.conversion_rate) OVER(), 0) AS cvr_s,
    (b.conversion_value/NULLIF(b.conversions,0) - MIN(b.conversion_value/NULLIF(b.conversions,0)) OVER()) / NULLIF(MAX(b.conversion_value/NULLIF(b.conversions,0)) OVER() - MIN(b.conversion_value/NULLIF(b.conversions,0)) OVER(), 0) AS aov_s,
    (b.conversions - MIN(b.conversions) OVER()) / NULLIF(MAX(b.conversions) OVER() - MIN(b.conversions) OVER(), 0) AS conv_s,
    (b.quality_score - MIN(b.quality_score) OVER()) / NULLIF(MAX(b.quality_score) OVER() - MIN(b.quality_score) OVER(), 0) AS qs_s,
    (b.impression_share - MIN(b.impression_share) OVER()) / NULLIF(MAX(b.impression_share) OVER() - MIN(b.impression_share) OVER(), 0) AS is_s,
    (b.ctr - MIN(b.ctr) OVER()) / NULLIF(MAX(b.ctr) OVER() - MIN(b.ctr) OVER(), 0) AS ctr_s
  FROM base b
)
SELECT *,
  100.0 * (0.4*roas_s + 0.3*cpa_s + 0.3*cpc_s) AS cost_eff,
  100.0 * (0.4*cvr_s + 0.3*aov_s + 0.3*conv_s) AS conv_quality,
  100.0 * (0.4*qs_s + 0.3*is_s + 0.3*ctr_s) AS competitive,
  100.0 * (0.4*(0.4*roas_s + 0.3*cpa_s + 0.3*cpc_s) + 0.35*(0.4*cvr_s + 0.3*aov_s + 0.3*conv_s) + 0.25*(0.4*qs_s + 0.3*is_s + 0.3*ctr_s)) AS health_score
FROM norm
ORDER BY campaign_id, year_month
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-058/attempt-01/sql/S29.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-058/attempt-01/sql/S29.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-058/attempt-01/results/S29.rows.jsonl)；完整：True；SHA256：`b7890fcf3f693ba757bebdd3e9e0a9d670b4095d4208f27a6411444ddd1aa11e`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "google_ads__campaign_report", "kind": "base", "block": null, "base_tables": ["google_ads__campaign_report"]}] | [] | [] |
| B2 | [{"alias": "b", "kind": "derived", "block": "B1", "base_tables": ["google_ads__campaign_report"]}] | [] | [] |
| B3 | [{"alias": "norm", "kind": "derived", "block": "B2", "base_tables": ["google_ads__campaign_report"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |


## S30

类别 `data`；来源 `query_db`；调用 `c98d21b51bc0429f95d6368f5572ca24`；状态 `success`。

```sql
WITH base AS (
  SELECT 
    year_month, campaign_id, campaign_name, campaign_type, bidding_strategy, industry,
    cost, conversions, conversion_value, roas, cpc, cost_per_conversion,
    conversion_rate, quality_score, impression_share, ctr
  FROM google_ads__campaign_report
),
norm AS (
  SELECT b.*,
    (b.roas - MIN(b.roas) OVER()) / NULLIF(MAX(b.roas) OVER() - MIN(b.roas) OVER(), 0) AS roas_s,
    (MAX(b.cpc) OVER() - b.cpc) / NULLIF(MAX(b.cpc) OVER() - MIN(b.cpc) OVER(), 0) AS cpc_s,
    (MAX(b.cost_per_conversion) OVER() - b.cost_per_conversion) / NULLIF(MAX(b.cost_per_conversion) OVER() - MIN(b.cost_per_conversion) OVER(), 0) AS cpa_s,
    (b.conversion_rate - MIN(b.conversion_rate) OVER()) / NULLIF(MAX(b.conversion_rate) OVER() - MIN(b.conversion_rate) OVER(), 0) AS cvr_s,
    (b.conversion_value/NULLIF(b.conversions,0) - MIN(b.conversion_value/NULLIF(b.conversions,0)) OVER()) / NULLIF(MAX(b.conversion_value/NULLIF(b.conversions,0)) OVER() - MIN(b.conversion_value/NULLIF(b.conversions,0)) OVER(), 0) AS aov_s,
    (b.conversions - MIN(b.conversions) OVER()) / NULLIF(MAX(b.conversions) OVER() - MIN(b.conversions) OVER(), 0) AS conv_s,
    (b.quality_score - MIN(b.quality_score) OVER()) / NULLIF(MAX(b.quality_score) OVER() - MIN(b.quality_score) OVER(), 0) AS qs_s,
    (b.impression_share - MIN(b.impression_share) OVER()) / NULLIF(MAX(b.impression_share) OVER() - MIN(b.impression_share) OVER(), 0) AS is_s,
    (b.ctr - MIN(b.ctr) OVER()) / NULLIF(MAX(b.ctr) OVER() - MIN(b.ctr) OVER(), 0) AS ctr_s
  FROM base b
)
SELECT campaign_id, campaign_name, campaign_type, bidding_strategy, industry,
  COUNT(*) AS n_months,
  ROUND(AVG(cost), 0) AS avg_monthly_cost,
  ROUND(SUM(cost), 0) AS total_cost,
  ROUND(AVG(roas), 3) AS avg_roas,
  ROUND(100.0 * AVG(0.4*roas_s + 0.3*cpa_s + 0.3*cpc_s), 2) AS cost_eff,
  ROUND(100.0 * AVG(0.4*cvr_s + 0.3*aov_s + 0.3*conv_s), 2) AS conv_quality,
  ROUND(100.0 * AVG(0.4*qs_s + 0.3*is_s + 0.3*ctr_s), 2) AS competitive,
  ROUND(100.0 * AVG(0.4*(0.4*roas_s + 0.3*cpa_s + 0.3*cpc_s) + 0.35*(0.4*cvr_s + 0.3*aov_s + 0.3*conv_s) + 0.25*(0.4*qs_s + 0.3*is_s + 0.3*ctr_s)), 2) AS health_score
FROM norm
GROUP BY campaign_id
ORDER BY health_score ASC
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-058/attempt-01/sql/S30.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-058/attempt-01/sql/S30.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-058/attempt-01/results/S30.rows.jsonl)；完整：True；SHA256：`aed59a4199c3c3a1d91cb9fe1ab9aa9bbefa9d3f6dacf20e68e899e3828fba1e`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "google_ads__campaign_report", "kind": "base", "block": null, "base_tables": ["google_ads__campaign_report"]}] | [] | [] |
| B2 | [{"alias": "b", "kind": "derived", "block": "B1", "base_tables": ["google_ads__campaign_report"]}] | [] | [] |
| B3 | [{"alias": "norm", "kind": "derived", "block": "B2", "base_tables": ["google_ads__campaign_report"]}] | [] | ["campaign_id"] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B3 | COUNT(*) | [] | [] | True |
| B3 | AVG(cost) | [{"table": "google_ads__campaign_report", "column": "cost"}] | [] | False |
| B3 | SUM(cost) | [{"table": "google_ads__campaign_report", "column": "cost"}] | [] | False |
| B3 | AVG(roas) | [{"table": "google_ads__campaign_report", "column": "roas"}] | [] | False |
| B3 | AVG(0.4 * roas_s + 0.3 * cpa_s + 0.3 * cpc_s) | [{"table": "google_ads__campaign_report", "column": "cpc"}, {"table": "google_ads__campaign_report", "column": "cpc"}, {"table": "google_ads__campaign_report", "column": "cpc"}, {"table": "google_ads__campaign_report", "column": "cpc"}, {"table": "google_ads__campaign_report", "column": "roas"}, {"table": "google_ads__campaign_report", "column": "roas"}, {"table": "google_ads__campaign_report", "column": "roas"}, {"table": "google_ads__campaign_report", "column": "roas"}, {"table": "google_ads__campaign_report", "column": "cost_per_conversion"}, {"table": "google_ads__campaign_report", "column": "cost_per_conversion"}, {"table": "google_ads__campaign_report", "column": "cost_per_conversion"}, {"table": "google_ads__campaign_report", "column": "cost_per_conversion"}] | [] | False |
| B3 | AVG(0.4 * cvr_s + 0.3 * aov_s + 0.3 * conv_s) | [{"table": "google_ads__campaign_report", "column": "conversions"}, {"table": "google_ads__campaign_report", "column": "conversions"}, {"table": "google_ads__campaign_report", "column": "conversions"}, {"table": "google_ads__campaign_report", "column": "conversions"}, {"table": "google_ads__campaign_report", "column": "conversion_rate"}, {"table": "google_ads__campaign_report", "column": "conversion_rate"}, {"table": "google_ads__campaign_report", "column": "conversion_rate"}, {"table": "google_ads__campaign_report", "column": "conversion_rate"}, {"table": "google_ads__campaign_report", "column": "conversion_value"}, {"table": "google_ads__campaign_report", "column": "conversions"}, {"table": "google_ads__campaign_report", "column": "conversion_value"}, {"table": "google_ads__campaign_report", "column": "conversion_value"}, {"table": "google_ads__campaign_report", "column": "conversion_value"}, {"table": "google_ads__campaign_report", "column": "conversions"}, {"table": "google_ads__campaign_report", "column": "conversions"}, {"table": "google_ads__campaign_report", "column": "conversions"}] | [] | False |
| B3 | AVG(0.4 * qs_s + 0.3 * is_s + 0.3 * ctr_s) | [{"table": "google_ads__campaign_report", "column": "ctr"}, {"table": "google_ads__campaign_report", "column": "ctr"}, {"table": "google_ads__campaign_report", "column": "ctr"}, {"table": "google_ads__campaign_report", "column": "ctr"}, {"table": "google_ads__campaign_report", "column": "quality_score"}, {"table": "google_ads__campaign_report", "column": "quality_score"}, {"table": "google_ads__campaign_report", "column": "quality_score"}, {"table": "google_ads__campaign_report", "column": "quality_score"}, {"table": "google_ads__campaign_report", "column": "impression_share"}, {"table": "google_ads__campaign_report", "column": "impression_share"}, {"table": "google_ads__campaign_report", "column": "impression_share"}, {"table": "google_ads__campaign_report", "column": "impression_share"}] | [] | False |
| B3 | AVG(0.4 * (0.4 * roas_s + 0.3 * cpa_s + 0.3 * cpc_s) + 0.35 * (0.4 * cvr_s + 0.3 * aov_s + 0.3 * conv_s) + 0.25 * (0.4 * qs_s + 0.3 * is_s + 0.3 * ctr_s)) | [{"table": "google_ads__campaign_report", "column": "ctr"}, {"table": "google_ads__campaign_report", "column": "ctr"}, {"table": "google_ads__campaign_report", "column": "ctr"}, {"table": "google_ads__campaign_report", "column": "ctr"}, {"table": "google_ads__campaign_report", "column": "cpc"}, {"table": "google_ads__campaign_report", "column": "cpc"}, {"table": "google_ads__campaign_report", "column": "cpc"}, {"table": "google_ads__campaign_report", "column": "cpc"}, {"table": "google_ads__campaign_report", "column": "conversions"}, {"table": "google_ads__campaign_report", "column": "conversions"}, {"table": "google_ads__campaign_report", "column": "conversions"}, {"table": "google_ads__campaign_report", "column": "conversions"}, {"table": "google_ads__campaign_report", "column": "quality_score"}, {"table": "google_ads__campaign_report", "column": "quality_score"}, {"table": "google_ads__campaign_report", "column": "quality_score"}, {"table": "google_ads__campaign_report", "column": "quality_score"}, {"table": "google_ads__campaign_report", "column": "impression_share"}, {"table": "google_ads__campaign_report", "column": "impression_share"}, {"table": "google_ads__campaign_report", "column": "impression_share"}, {"table": "google_ads__campaign_report", "column": "impression_share"}, {"table": "google_ads__campaign_report", "column": "roas"}, {"table": "google_ads__campaign_report", "column": "roas"}, {"table": "google_ads__campaign_report", "column": "roas"}, {"table": "google_ads__campaign_report", "column": "roas"}, {"table": "google_ads__campaign_report", "column": "cost_per_conversion"}, {"table": "google_ads__campaign_report", "column": "cost_per_conversion"}, {"table": "google_ads__campaign_report", "column": "cost_per_conversion"}, {"table": "google_ads__campaign_report", "column": "cost_per_conversion"}, {"table": "google_ads__campaign_report", "column": "conversion_rate"}, {"table": "google_ads__campaign_report", "column": "conversion_rate"}, {"table": "google_ads__campaign_report", "column": "conversion_rate"}, {"table": "google_ads__campaign_report", "column": "conversion_rate"}, {"table": "google_ads__campaign_report", "column": "conversion_value"}, {"table": "google_ads__campaign_report", "column": "conversions"}, {"table": "google_ads__campaign_report", "column": "conversion_value"}, {"table": "google_ads__campaign_report", "column": "conversion_value"}, {"table": "google_ads__campaign_report", "column": "conversion_value"}, {"table": "google_ads__campaign_report", "column": "conversions"}, {"table": "google_ads__campaign_report", "column": "conversions"}, {"table": "google_ads__campaign_report", "column": "conversions"}] | [] | False |


## S31

类别 `data`；来源 `python`；调用 `22ab169d6c6043a9bf0bd21687d50dab`；状态 `success`。

```sql
SELECT campaign_id, campaign_name, campaign_type, bidding_strategy, industry, COUNT(*) n FROM google_ads__campaign_report GROUP BY campaign_id
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-058/attempt-01/sql/S31.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-058/attempt-01/sql/S31.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-058/attempt-01/results/S31.rows.jsonl)；完整：True；SHA256：`f3960ec06c8702d58e0df94b5da8f8e3d14fd25641dc18054328b37c4b2a95d8`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "google_ads__campaign_report", "kind": "base", "block": null, "base_tables": ["google_ads__campaign_report"]}] | [] | ["campaign_id"] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |


## S32

类别 `data`；来源 `python`；调用 `c34707d3009740f49b349c4a4337175b`；状态 `success`。

```sql

WITH base AS (
  SELECT year_month, campaign_id, campaign_name, campaign_type, bidding_strategy, industry,
    cost, conversions, conversion_value, roas, cpc, cost_per_conversion,
    conversion_rate, quality_score, impression_share, ctr
  FROM google_ads__campaign_report
),
norm AS (
  SELECT *,
    (roas - MIN(roas) OVER()) / NULLIF(MAX(roas) OVER() - MIN(roas) OVER(), 0) AS roas_s,
    (MAX(cpc) OVER() - cpc) / NULLIF(MAX(cpc) OVER() - MIN(cpc) OVER(), 0) AS cpc_s,
    (MAX(cost_per_conversion) OVER() - cost_per_conversion) / NULLIF(MAX(cost_per_conversion) OVER() - MIN(cost_per_conversion) OVER(), 0) AS cpa_s,
    (conversion_rate - MIN(conversion_rate) OVER()) / NULLIF(MAX(conversion_rate) OVER() - MIN(conversion_rate) OVER(), 0) AS cvr_s,
    (conversion_value/NULLIF(conversions,0) - MIN(conversion_value/NULLIF(conversions,0)) OVER()) / NULLIF(MAX(conversion_value/NULLIF(conversions,0)) OVER() - MIN(conversion_value/NULLIF(conversions,0)) OVER(), 0) AS aov_s,
    (conversions - MIN(conversions) OVER()) / NULLIF(MAX(conversions) OVER() - MIN(conversions) OVER(), 0) AS conv_s,
    (quality_score - MIN(quality_score) OVER()) / NULLIF(MAX(quality_score) OVER() - MIN(quality_score) OVER(), 0) AS qs_s,
    (impression_share - MIN(impression_share) OVER()) / NULLIF(MAX(impression_share) OVER() - MIN(impression_share) OVER(), 0) AS is_s,
    (ctr - MIN(ctr) OVER()) / NULLIF(MAX(ctr) OVER() - MIN(ctr) OVER(), 0) AS ctr_s
  FROM base
)
SELECT campaign_id, campaign_name, campaign_type, bidding_strategy, industry,
  COUNT(*) AS n_months,
  AVG(cost) AS avg_monthly_cost,
  SUM(cost) AS total_cost,
  AVG(roas) AS avg_roas,
  AVG(roas_s) AS avg_roas_s,
  AVG(cpc_s) AS avg_cpc_s,
  AVG(cpa_s) AS avg_cpa_s,
  AVG(cvr_s) AS avg_cvr_s,
  AVG(aov_s) AS avg_aov_s,
  AVG(conv_s) AS avg_conv_s,
  AVG(qs_s) AS avg_qs_s,
  AVG(is_s) AS avg_is_s,
  AVG(ctr_s) AS avg_ctr_s,
  100.0 * AVG(0.4*roas_s + 0.3*cpa_s + 0.3*cpc_s) AS cost_eff,
  100.0 * AVG(0.4*cvr_s + 0.3*aov_s + 0.3*conv_s) AS conv_quality,
  100.0 * AVG(0.4*qs_s + 0.3*is_s + 0.3*ctr_s) AS competitive,
  100.0 * AVG(0.4*(0.4*roas_s + 0.3*cpa_s + 0.3*cpc_s) + 0.35*(0.4*cvr_s + 0.3*aov_s + 0.3*conv_s) + 0.25*(0.4*qs_s + 0.3*is_s + 0.3*ctr_s)) AS health_score
FROM norm
GROUP BY campaign_id
ORDER BY health_score

```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-058/attempt-01/sql/S32.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-058/attempt-01/sql/S32.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-058/attempt-01/results/S32.rows.jsonl)；完整：True；SHA256：`302a7cb65c9b9c18c1ae7a0c69202dc220902071d7bbf31344dff8e3bfaf052f`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "google_ads__campaign_report", "kind": "base", "block": null, "base_tables": ["google_ads__campaign_report"]}] | [] | [] |
| B2 | [{"alias": "base", "kind": "derived", "block": "B1", "base_tables": ["google_ads__campaign_report"]}] | [] | [] |
| B3 | [{"alias": "norm", "kind": "derived", "block": "B2", "base_tables": ["google_ads__campaign_report"]}] | [] | ["campaign_id"] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B3 | COUNT(*) | [] | [] | True |
| B3 | AVG(cost) | [{"table": "google_ads__campaign_report", "column": "cost"}] | [] | False |
| B3 | SUM(cost) | [{"table": "google_ads__campaign_report", "column": "cost"}] | [] | False |
| B3 | AVG(roas) | [{"table": "google_ads__campaign_report", "column": "roas"}] | [] | False |
| B3 | AVG(roas_s) | [{"table": "google_ads__campaign_report", "column": "roas"}, {"table": "google_ads__campaign_report", "column": "roas"}, {"table": "google_ads__campaign_report", "column": "roas"}, {"table": "google_ads__campaign_report", "column": "roas"}] | [] | False |
| B3 | AVG(cpc_s) | [{"table": "google_ads__campaign_report", "column": "cpc"}, {"table": "google_ads__campaign_report", "column": "cpc"}, {"table": "google_ads__campaign_report", "column": "cpc"}, {"table": "google_ads__campaign_report", "column": "cpc"}] | [] | False |
| B3 | AVG(cpa_s) | [{"table": "google_ads__campaign_report", "column": "cost_per_conversion"}, {"table": "google_ads__campaign_report", "column": "cost_per_conversion"}, {"table": "google_ads__campaign_report", "column": "cost_per_conversion"}, {"table": "google_ads__campaign_report", "column": "cost_per_conversion"}] | [] | False |
| B3 | AVG(cvr_s) | [{"table": "google_ads__campaign_report", "column": "conversion_rate"}, {"table": "google_ads__campaign_report", "column": "conversion_rate"}, {"table": "google_ads__campaign_report", "column": "conversion_rate"}, {"table": "google_ads__campaign_report", "column": "conversion_rate"}] | [] | False |
| B3 | AVG(aov_s) | [{"table": "google_ads__campaign_report", "column": "conversion_value"}, {"table": "google_ads__campaign_report", "column": "conversions"}, {"table": "google_ads__campaign_report", "column": "conversion_value"}, {"table": "google_ads__campaign_report", "column": "conversion_value"}, {"table": "google_ads__campaign_report", "column": "conversion_value"}, {"table": "google_ads__campaign_report", "column": "conversions"}, {"table": "google_ads__campaign_report", "column": "conversions"}, {"table": "google_ads__campaign_report", "column": "conversions"}] | [] | False |
| B3 | AVG(conv_s) | [{"table": "google_ads__campaign_report", "column": "conversions"}, {"table": "google_ads__campaign_report", "column": "conversions"}, {"table": "google_ads__campaign_report", "column": "conversions"}, {"table": "google_ads__campaign_report", "column": "conversions"}] | [] | False |
| B3 | AVG(qs_s) | [{"table": "google_ads__campaign_report", "column": "quality_score"}, {"table": "google_ads__campaign_report", "column": "quality_score"}, {"table": "google_ads__campaign_report", "column": "quality_score"}, {"table": "google_ads__campaign_report", "column": "quality_score"}] | [] | False |
| B3 | AVG(is_s) | [{"table": "google_ads__campaign_report", "column": "impression_share"}, {"table": "google_ads__campaign_report", "column": "impression_share"}, {"table": "google_ads__campaign_report", "column": "impression_share"}, {"table": "google_ads__campaign_report", "column": "impression_share"}] | [] | False |
| B3 | AVG(ctr_s) | [{"table": "google_ads__campaign_report", "column": "ctr"}, {"table": "google_ads__campaign_report", "column": "ctr"}, {"table": "google_ads__campaign_report", "column": "ctr"}, {"table": "google_ads__campaign_report", "column": "ctr"}] | [] | False |
| B3 | AVG(0.4 * roas_s + 0.3 * cpa_s + 0.3 * cpc_s) | [{"table": "google_ads__campaign_report", "column": "cpc"}, {"table": "google_ads__campaign_report", "column": "cpc"}, {"table": "google_ads__campaign_report", "column": "cpc"}, {"table": "google_ads__campaign_report", "column": "cpc"}, {"table": "google_ads__campaign_report", "column": "roas"}, {"table": "google_ads__campaign_report", "column": "roas"}, {"table": "google_ads__campaign_report", "column": "roas"}, {"table": "google_ads__campaign_report", "column": "roas"}, {"table": "google_ads__campaign_report", "column": "cost_per_conversion"}, {"table": "google_ads__campaign_report", "column": "cost_per_conversion"}, {"table": "google_ads__campaign_report", "column": "cost_per_conversion"}, {"table": "google_ads__campaign_report", "column": "cost_per_conversion"}] | [] | False |
| B3 | AVG(0.4 * cvr_s + 0.3 * aov_s + 0.3 * conv_s) | [{"table": "google_ads__campaign_report", "column": "conversions"}, {"table": "google_ads__campaign_report", "column": "conversions"}, {"table": "google_ads__campaign_report", "column": "conversions"}, {"table": "google_ads__campaign_report", "column": "conversions"}, {"table": "google_ads__campaign_report", "column": "conversion_rate"}, {"table": "google_ads__campaign_report", "column": "conversion_rate"}, {"table": "google_ads__campaign_report", "column": "conversion_rate"}, {"table": "google_ads__campaign_report", "column": "conversion_rate"}, {"table": "google_ads__campaign_report", "column": "conversion_value"}, {"table": "google_ads__campaign_report", "column": "conversions"}, {"table": "google_ads__campaign_report", "column": "conversion_value"}, {"table": "google_ads__campaign_report", "column": "conversion_value"}, {"table": "google_ads__campaign_report", "column": "conversion_value"}, {"table": "google_ads__campaign_report", "column": "conversions"}, {"table": "google_ads__campaign_report", "column": "conversions"}, {"table": "google_ads__campaign_report", "column": "conversions"}] | [] | False |
| B3 | AVG(0.4 * qs_s + 0.3 * is_s + 0.3 * ctr_s) | [{"table": "google_ads__campaign_report", "column": "ctr"}, {"table": "google_ads__campaign_report", "column": "ctr"}, {"table": "google_ads__campaign_report", "column": "ctr"}, {"table": "google_ads__campaign_report", "column": "ctr"}, {"table": "google_ads__campaign_report", "column": "quality_score"}, {"table": "google_ads__campaign_report", "column": "quality_score"}, {"table": "google_ads__campaign_report", "column": "quality_score"}, {"table": "google_ads__campaign_report", "column": "quality_score"}, {"table": "google_ads__campaign_report", "column": "impression_share"}, {"table": "google_ads__campaign_report", "column": "impression_share"}, {"table": "google_ads__campaign_report", "column": "impression_share"}, {"table": "google_ads__campaign_report", "column": "impression_share"}] | [] | False |
| B3 | AVG(0.4 * (0.4 * roas_s + 0.3 * cpa_s + 0.3 * cpc_s) + 0.35 * (0.4 * cvr_s + 0.3 * aov_s + 0.3 * conv_s) + 0.25 * (0.4 * qs_s + 0.3 * is_s + 0.3 * ctr_s)) | [{"table": "google_ads__campaign_report", "column": "ctr"}, {"table": "google_ads__campaign_report", "column": "ctr"}, {"table": "google_ads__campaign_report", "column": "ctr"}, {"table": "google_ads__campaign_report", "column": "ctr"}, {"table": "google_ads__campaign_report", "column": "cpc"}, {"table": "google_ads__campaign_report", "column": "cpc"}, {"table": "google_ads__campaign_report", "column": "cpc"}, {"table": "google_ads__campaign_report", "column": "cpc"}, {"table": "google_ads__campaign_report", "column": "conversions"}, {"table": "google_ads__campaign_report", "column": "conversions"}, {"table": "google_ads__campaign_report", "column": "conversions"}, {"table": "google_ads__campaign_report", "column": "conversions"}, {"table": "google_ads__campaign_report", "column": "quality_score"}, {"table": "google_ads__campaign_report", "column": "quality_score"}, {"table": "google_ads__campaign_report", "column": "quality_score"}, {"table": "google_ads__campaign_report", "column": "quality_score"}, {"table": "google_ads__campaign_report", "column": "impression_share"}, {"table": "google_ads__campaign_report", "column": "impression_share"}, {"table": "google_ads__campaign_report", "column": "impression_share"}, {"table": "google_ads__campaign_report", "column": "impression_share"}, {"table": "google_ads__campaign_report", "column": "roas"}, {"table": "google_ads__campaign_report", "column": "roas"}, {"table": "google_ads__campaign_report", "column": "roas"}, {"table": "google_ads__campaign_report", "column": "roas"}, {"table": "google_ads__campaign_report", "column": "cost_per_conversion"}, {"table": "google_ads__campaign_report", "column": "cost_per_conversion"}, {"table": "google_ads__campaign_report", "column": "cost_per_conversion"}, {"table": "google_ads__campaign_report", "column": "cost_per_conversion"}, {"table": "google_ads__campaign_report", "column": "conversion_rate"}, {"table": "google_ads__campaign_report", "column": "conversion_rate"}, {"table": "google_ads__campaign_report", "column": "conversion_rate"}, {"table": "google_ads__campaign_report", "column": "conversion_rate"}, {"table": "google_ads__campaign_report", "column": "conversion_value"}, {"table": "google_ads__campaign_report", "column": "conversions"}, {"table": "google_ads__campaign_report", "column": "conversion_value"}, {"table": "google_ads__campaign_report", "column": "conversion_value"}, {"table": "google_ads__campaign_report", "column": "conversion_value"}, {"table": "google_ads__campaign_report", "column": "conversions"}, {"table": "google_ads__campaign_report", "column": "conversions"}, {"table": "google_ads__campaign_report", "column": "conversions"}] | [] | False |


## S33

类别 `data`；来源 `python`；调用 `d186ec1cf2484ad69651a4a672f12f60`；状态 `success`。

```sql

WITH base AS (
  SELECT year_month, campaign_id, campaign_name, campaign_type, bidding_strategy, industry,
    cost, conversions, conversion_value, roas, cpc, cost_per_conversion,
    conversion_rate, quality_score, impression_share, ctr
  FROM google_ads__campaign_report
),
norm AS (
  SELECT *,
    (roas - MIN(roas) OVER()) / NULLIF(MAX(roas) OVER() - MIN(roas) OVER(), 0) AS roas_s,
    (MAX(cpc) OVER() - cpc) / NULLIF(MAX(cpc) OVER() - MIN(cpc) OVER(), 0) AS cpc_s,
    (MAX(cost_per_conversion) OVER() - cost_per_conversion) / NULLIF(MAX(cost_per_conversion) OVER() - MIN(cost_per_conversion) OVER(), 0) AS cpa_s,
    (conversion_rate - MIN(conversion_rate) OVER()) / NULLIF(MAX(conversion_rate) OVER() - MIN(conversion_rate) OVER(), 0) AS cvr_s,
    (conversion_value/NULLIF(conversions,0) - MIN(conversion_value/NULLIF(conversions,0)) OVER()) / NULLIF(MAX(conversion_value/NULLIF(conversions,0)) OVER() - MIN(conversion_value/NULLIF(conversions,0)) OVER(), 0) AS aov_s,
    (conversions - MIN(conversions) OVER()) / NULLIF(MAX(conversions) OVER() - MIN(conversions) OVER(), 0) AS conv_s,
    (quality_score - MIN(quality_score) OVER()) / NULLIF(MAX(quality_score) OVER() - MIN(quality_score) OVER(), 0) AS qs_s,
    (impression_share - MIN(impression_share) OVER()) / NULLIF(MAX(impression_share) OVER() - MIN(impression_share) OVER(), 0) AS is_s,
    (ctr - MIN(ctr) OVER()) / NULLIF(MAX(ctr) OVER() - MIN(ctr) OVER(), 0) AS ctr_s
  FROM base
)
SELECT campaign_id, campaign_name, campaign_type, bidding_strategy, industry,
  COUNT(*) AS n_months, AVG(cost) AS avg_monthly_cost, SUM(cost) AS total_cost,
  AVG(roas) AS avg_roas,
  100.0 * AVG(0.4*roas_s + 0.3*cpa_s + 0.3*cpc_s) AS cost_eff,
  100.0 * AVG(0.4*cvr_s + 0.3*aov_s + 0.3*conv_s) AS conv_quality,
  100.0 * AVG(0.4*qs_s + 0.3*is_s + 0.3*ctr_s) AS competitive,
  100.0 * AVG(0.4*(0.4*roas_s + 0.3*cpa_s + 0.3*cpc_s) + 0.35*(0.4*cvr_s + 0.3*aov_s + 0.3*conv_s) + 0.25*(0.4*qs_s + 0.3*is_s + 0.3*ctr_s)) AS health_score
FROM norm GROUP BY campaign_id ORDER BY health_score

```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-058/attempt-01/sql/S33.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-058/attempt-01/sql/S33.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-058/attempt-01/results/S33.rows.jsonl)；完整：True；SHA256：`715afe33d84fcdb6a5c73cdd5bb09435617cf0aaa98877b5cae21c2d9c517ab8`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "google_ads__campaign_report", "kind": "base", "block": null, "base_tables": ["google_ads__campaign_report"]}] | [] | [] |
| B2 | [{"alias": "base", "kind": "derived", "block": "B1", "base_tables": ["google_ads__campaign_report"]}] | [] | [] |
| B3 | [{"alias": "norm", "kind": "derived", "block": "B2", "base_tables": ["google_ads__campaign_report"]}] | [] | ["campaign_id"] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B3 | COUNT(*) | [] | [] | True |
| B3 | AVG(cost) | [{"table": "google_ads__campaign_report", "column": "cost"}] | [] | False |
| B3 | SUM(cost) | [{"table": "google_ads__campaign_report", "column": "cost"}] | [] | False |
| B3 | AVG(roas) | [{"table": "google_ads__campaign_report", "column": "roas"}] | [] | False |
| B3 | AVG(0.4 * roas_s + 0.3 * cpa_s + 0.3 * cpc_s) | [{"table": "google_ads__campaign_report", "column": "cpc"}, {"table": "google_ads__campaign_report", "column": "cpc"}, {"table": "google_ads__campaign_report", "column": "cpc"}, {"table": "google_ads__campaign_report", "column": "cpc"}, {"table": "google_ads__campaign_report", "column": "roas"}, {"table": "google_ads__campaign_report", "column": "roas"}, {"table": "google_ads__campaign_report", "column": "roas"}, {"table": "google_ads__campaign_report", "column": "roas"}, {"table": "google_ads__campaign_report", "column": "cost_per_conversion"}, {"table": "google_ads__campaign_report", "column": "cost_per_conversion"}, {"table": "google_ads__campaign_report", "column": "cost_per_conversion"}, {"table": "google_ads__campaign_report", "column": "cost_per_conversion"}] | [] | False |
| B3 | AVG(0.4 * cvr_s + 0.3 * aov_s + 0.3 * conv_s) | [{"table": "google_ads__campaign_report", "column": "conversions"}, {"table": "google_ads__campaign_report", "column": "conversions"}, {"table": "google_ads__campaign_report", "column": "conversions"}, {"table": "google_ads__campaign_report", "column": "conversions"}, {"table": "google_ads__campaign_report", "column": "conversion_rate"}, {"table": "google_ads__campaign_report", "column": "conversion_rate"}, {"table": "google_ads__campaign_report", "column": "conversion_rate"}, {"table": "google_ads__campaign_report", "column": "conversion_rate"}, {"table": "google_ads__campaign_report", "column": "conversion_value"}, {"table": "google_ads__campaign_report", "column": "conversions"}, {"table": "google_ads__campaign_report", "column": "conversion_value"}, {"table": "google_ads__campaign_report", "column": "conversion_value"}, {"table": "google_ads__campaign_report", "column": "conversion_value"}, {"table": "google_ads__campaign_report", "column": "conversions"}, {"table": "google_ads__campaign_report", "column": "conversions"}, {"table": "google_ads__campaign_report", "column": "conversions"}] | [] | False |
| B3 | AVG(0.4 * qs_s + 0.3 * is_s + 0.3 * ctr_s) | [{"table": "google_ads__campaign_report", "column": "ctr"}, {"table": "google_ads__campaign_report", "column": "ctr"}, {"table": "google_ads__campaign_report", "column": "ctr"}, {"table": "google_ads__campaign_report", "column": "ctr"}, {"table": "google_ads__campaign_report", "column": "quality_score"}, {"table": "google_ads__campaign_report", "column": "quality_score"}, {"table": "google_ads__campaign_report", "column": "quality_score"}, {"table": "google_ads__campaign_report", "column": "quality_score"}, {"table": "google_ads__campaign_report", "column": "impression_share"}, {"table": "google_ads__campaign_report", "column": "impression_share"}, {"table": "google_ads__campaign_report", "column": "impression_share"}, {"table": "google_ads__campaign_report", "column": "impression_share"}] | [] | False |
| B3 | AVG(0.4 * (0.4 * roas_s + 0.3 * cpa_s + 0.3 * cpc_s) + 0.35 * (0.4 * cvr_s + 0.3 * aov_s + 0.3 * conv_s) + 0.25 * (0.4 * qs_s + 0.3 * is_s + 0.3 * ctr_s)) | [{"table": "google_ads__campaign_report", "column": "ctr"}, {"table": "google_ads__campaign_report", "column": "ctr"}, {"table": "google_ads__campaign_report", "column": "ctr"}, {"table": "google_ads__campaign_report", "column": "ctr"}, {"table": "google_ads__campaign_report", "column": "cpc"}, {"table": "google_ads__campaign_report", "column": "cpc"}, {"table": "google_ads__campaign_report", "column": "cpc"}, {"table": "google_ads__campaign_report", "column": "cpc"}, {"table": "google_ads__campaign_report", "column": "conversions"}, {"table": "google_ads__campaign_report", "column": "conversions"}, {"table": "google_ads__campaign_report", "column": "conversions"}, {"table": "google_ads__campaign_report", "column": "conversions"}, {"table": "google_ads__campaign_report", "column": "quality_score"}, {"table": "google_ads__campaign_report", "column": "quality_score"}, {"table": "google_ads__campaign_report", "column": "quality_score"}, {"table": "google_ads__campaign_report", "column": "quality_score"}, {"table": "google_ads__campaign_report", "column": "impression_share"}, {"table": "google_ads__campaign_report", "column": "impression_share"}, {"table": "google_ads__campaign_report", "column": "impression_share"}, {"table": "google_ads__campaign_report", "column": "impression_share"}, {"table": "google_ads__campaign_report", "column": "roas"}, {"table": "google_ads__campaign_report", "column": "roas"}, {"table": "google_ads__campaign_report", "column": "roas"}, {"table": "google_ads__campaign_report", "column": "roas"}, {"table": "google_ads__campaign_report", "column": "cost_per_conversion"}, {"table": "google_ads__campaign_report", "column": "cost_per_conversion"}, {"table": "google_ads__campaign_report", "column": "cost_per_conversion"}, {"table": "google_ads__campaign_report", "column": "cost_per_conversion"}, {"table": "google_ads__campaign_report", "column": "conversion_rate"}, {"table": "google_ads__campaign_report", "column": "conversion_rate"}, {"table": "google_ads__campaign_report", "column": "conversion_rate"}, {"table": "google_ads__campaign_report", "column": "conversion_rate"}, {"table": "google_ads__campaign_report", "column": "conversion_value"}, {"table": "google_ads__campaign_report", "column": "conversions"}, {"table": "google_ads__campaign_report", "column": "conversion_value"}, {"table": "google_ads__campaign_report", "column": "conversion_value"}, {"table": "google_ads__campaign_report", "column": "conversion_value"}, {"table": "google_ads__campaign_report", "column": "conversions"}, {"table": "google_ads__campaign_report", "column": "conversions"}, {"table": "google_ads__campaign_report", "column": "conversions"}] | [] | False |


## S34

类别 `data`；来源 `python`；调用 `b912bc07b9c241ca83c73dbf6aa215ef`；状态 `success`。

```sql

WITH base AS (
  SELECT year_month, campaign_id, campaign_name, campaign_type, bidding_strategy, industry,
    cost, conversions, conversion_value, roas, cpc, cost_per_conversion,
    conversion_rate, quality_score, impression_share, ctr
  FROM google_ads__campaign_report
),
norm AS (
  SELECT *,
    (roas - MIN(roas) OVER()) / NULLIF(MAX(roas) OVER() - MIN(roas) OVER(), 0) AS roas_s,
    (MAX(cpc) OVER() - cpc) / NULLIF(MAX(cpc) OVER() - MIN(cpc) OVER(), 0) AS cpc_s,
    (MAX(cost_per_conversion) OVER() - cost_per_conversion) / NULLIF(MAX(cost_per_conversion) OVER() - MIN(cost_per_conversion) OVER(), 0) AS cpa_s,
    (conversion_rate - MIN(conversion_rate) OVER()) / NULLIF(MAX(conversion_rate) OVER() - MIN(conversion_rate) OVER(), 0) AS cvr_s,
    (conversion_value/NULLIF(conversions,0) - MIN(conversion_value/NULLIF(conversions,0)) OVER()) / NULLIF(MAX(conversion_value/NULLIF(conversions,0)) OVER() - MIN(conversion_value/NULLIF(conversions,0)) OVER(), 0) AS aov_s,
    (conversions - MIN(conversions) OVER()) / NULLIF(MAX(conversions) OVER() - MIN(conversions) OVER(), 0) AS conv_s,
    (quality_score - MIN(quality_score) OVER()) / NULLIF(MAX(quality_score) OVER() - MIN(quality_score) OVER(), 0) AS qs_s,
    (impression_share - MIN(impression_share) OVER()) / NULLIF(MAX(impression_share) OVER() - MIN(impression_share) OVER(), 0) AS is_s,
    (ctr - MIN(ctr) OVER()) / NULLIF(MAX(ctr) OVER() - MIN(ctr) OVER(), 0) AS ctr_s
  FROM base
)
SELECT campaign_id, campaign_name, campaign_type, bidding_strategy, industry,
  COUNT(*) AS n_months, AVG(cost) AS avg_monthly_cost, SUM(cost) AS total_cost,
  AVG(roas) AS avg_roas,
  100.0 * AVG(0.4*roas_s + 0.3*cpa_s + 0.3*cpc_s) AS cost_eff,
  100.0 * AVG(0.4*cvr_s + 0.3*aov_s + 0.3*conv_s) AS conv_quality,
  100.0 * AVG(0.4*qs_s + 0.3*is_s + 0.3*ctr_s) AS competitive,
  100.0 * AVG(0.4*(0.4*roas_s + 0.3*cpa_s + 0.3*cpc_s) + 0.35*(0.4*cvr_s + 0.3*aov_s + 0.3*conv_s) + 0.25*(0.4*qs_s + 0.3*is_s + 0.3*ctr_s)) AS health_score
FROM norm GROUP BY campaign_id ORDER BY health_score

```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-058/attempt-01/sql/S34.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-058/attempt-01/sql/S34.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-058/attempt-01/results/S34.rows.jsonl)；完整：True；SHA256：`715afe33d84fcdb6a5c73cdd5bb09435617cf0aaa98877b5cae21c2d9c517ab8`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "google_ads__campaign_report", "kind": "base", "block": null, "base_tables": ["google_ads__campaign_report"]}] | [] | [] |
| B2 | [{"alias": "base", "kind": "derived", "block": "B1", "base_tables": ["google_ads__campaign_report"]}] | [] | [] |
| B3 | [{"alias": "norm", "kind": "derived", "block": "B2", "base_tables": ["google_ads__campaign_report"]}] | [] | ["campaign_id"] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B3 | COUNT(*) | [] | [] | True |
| B3 | AVG(cost) | [{"table": "google_ads__campaign_report", "column": "cost"}] | [] | False |
| B3 | SUM(cost) | [{"table": "google_ads__campaign_report", "column": "cost"}] | [] | False |
| B3 | AVG(roas) | [{"table": "google_ads__campaign_report", "column": "roas"}] | [] | False |
| B3 | AVG(0.4 * roas_s + 0.3 * cpa_s + 0.3 * cpc_s) | [{"table": "google_ads__campaign_report", "column": "cpc"}, {"table": "google_ads__campaign_report", "column": "cpc"}, {"table": "google_ads__campaign_report", "column": "cpc"}, {"table": "google_ads__campaign_report", "column": "cpc"}, {"table": "google_ads__campaign_report", "column": "roas"}, {"table": "google_ads__campaign_report", "column": "roas"}, {"table": "google_ads__campaign_report", "column": "roas"}, {"table": "google_ads__campaign_report", "column": "roas"}, {"table": "google_ads__campaign_report", "column": "cost_per_conversion"}, {"table": "google_ads__campaign_report", "column": "cost_per_conversion"}, {"table": "google_ads__campaign_report", "column": "cost_per_conversion"}, {"table": "google_ads__campaign_report", "column": "cost_per_conversion"}] | [] | False |
| B3 | AVG(0.4 * cvr_s + 0.3 * aov_s + 0.3 * conv_s) | [{"table": "google_ads__campaign_report", "column": "conversions"}, {"table": "google_ads__campaign_report", "column": "conversions"}, {"table": "google_ads__campaign_report", "column": "conversions"}, {"table": "google_ads__campaign_report", "column": "conversions"}, {"table": "google_ads__campaign_report", "column": "conversion_rate"}, {"table": "google_ads__campaign_report", "column": "conversion_rate"}, {"table": "google_ads__campaign_report", "column": "conversion_rate"}, {"table": "google_ads__campaign_report", "column": "conversion_rate"}, {"table": "google_ads__campaign_report", "column": "conversion_value"}, {"table": "google_ads__campaign_report", "column": "conversions"}, {"table": "google_ads__campaign_report", "column": "conversion_value"}, {"table": "google_ads__campaign_report", "column": "conversion_value"}, {"table": "google_ads__campaign_report", "column": "conversion_value"}, {"table": "google_ads__campaign_report", "column": "conversions"}, {"table": "google_ads__campaign_report", "column": "conversions"}, {"table": "google_ads__campaign_report", "column": "conversions"}] | [] | False |
| B3 | AVG(0.4 * qs_s + 0.3 * is_s + 0.3 * ctr_s) | [{"table": "google_ads__campaign_report", "column": "ctr"}, {"table": "google_ads__campaign_report", "column": "ctr"}, {"table": "google_ads__campaign_report", "column": "ctr"}, {"table": "google_ads__campaign_report", "column": "ctr"}, {"table": "google_ads__campaign_report", "column": "quality_score"}, {"table": "google_ads__campaign_report", "column": "quality_score"}, {"table": "google_ads__campaign_report", "column": "quality_score"}, {"table": "google_ads__campaign_report", "column": "quality_score"}, {"table": "google_ads__campaign_report", "column": "impression_share"}, {"table": "google_ads__campaign_report", "column": "impression_share"}, {"table": "google_ads__campaign_report", "column": "impression_share"}, {"table": "google_ads__campaign_report", "column": "impression_share"}] | [] | False |
| B3 | AVG(0.4 * (0.4 * roas_s + 0.3 * cpa_s + 0.3 * cpc_s) + 0.35 * (0.4 * cvr_s + 0.3 * aov_s + 0.3 * conv_s) + 0.25 * (0.4 * qs_s + 0.3 * is_s + 0.3 * ctr_s)) | [{"table": "google_ads__campaign_report", "column": "ctr"}, {"table": "google_ads__campaign_report", "column": "ctr"}, {"table": "google_ads__campaign_report", "column": "ctr"}, {"table": "google_ads__campaign_report", "column": "ctr"}, {"table": "google_ads__campaign_report", "column": "cpc"}, {"table": "google_ads__campaign_report", "column": "cpc"}, {"table": "google_ads__campaign_report", "column": "cpc"}, {"table": "google_ads__campaign_report", "column": "cpc"}, {"table": "google_ads__campaign_report", "column": "conversions"}, {"table": "google_ads__campaign_report", "column": "conversions"}, {"table": "google_ads__campaign_report", "column": "conversions"}, {"table": "google_ads__campaign_report", "column": "conversions"}, {"table": "google_ads__campaign_report", "column": "quality_score"}, {"table": "google_ads__campaign_report", "column": "quality_score"}, {"table": "google_ads__campaign_report", "column": "quality_score"}, {"table": "google_ads__campaign_report", "column": "quality_score"}, {"table": "google_ads__campaign_report", "column": "impression_share"}, {"table": "google_ads__campaign_report", "column": "impression_share"}, {"table": "google_ads__campaign_report", "column": "impression_share"}, {"table": "google_ads__campaign_report", "column": "impression_share"}, {"table": "google_ads__campaign_report", "column": "roas"}, {"table": "google_ads__campaign_report", "column": "roas"}, {"table": "google_ads__campaign_report", "column": "roas"}, {"table": "google_ads__campaign_report", "column": "roas"}, {"table": "google_ads__campaign_report", "column": "cost_per_conversion"}, {"table": "google_ads__campaign_report", "column": "cost_per_conversion"}, {"table": "google_ads__campaign_report", "column": "cost_per_conversion"}, {"table": "google_ads__campaign_report", "column": "cost_per_conversion"}, {"table": "google_ads__campaign_report", "column": "conversion_rate"}, {"table": "google_ads__campaign_report", "column": "conversion_rate"}, {"table": "google_ads__campaign_report", "column": "conversion_rate"}, {"table": "google_ads__campaign_report", "column": "conversion_rate"}, {"table": "google_ads__campaign_report", "column": "conversion_value"}, {"table": "google_ads__campaign_report", "column": "conversions"}, {"table": "google_ads__campaign_report", "column": "conversion_value"}, {"table": "google_ads__campaign_report", "column": "conversion_value"}, {"table": "google_ads__campaign_report", "column": "conversion_value"}, {"table": "google_ads__campaign_report", "column": "conversions"}, {"table": "google_ads__campaign_report", "column": "conversions"}, {"table": "google_ads__campaign_report", "column": "conversions"}] | [] | False |


## S35

类别 `data`；来源 `python`；调用 `accc4878a90842868a7e5d8d7e237df0`；状态 `success`。

```sql

SELECT d.year_month, d.campaign_id, d.device_type, d.cost, d.roas, d.quality_score, 
  d.impression_share, d.ctr, d.conversion_rate, d.conversions, d.conversion_value,
  d.cpc, d.cost_per_conversion
FROM google_ads__device_report d
ORDER BY d.campaign_id, d.year_month, d.device_type

```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-058/attempt-01/sql/S35.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-058/attempt-01/sql/S35.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-058/attempt-01/results/S35.rows.jsonl)；完整：True；SHA256：`6b7145a341a460db4717be45b49b4f819e01c95a2290537973b030a2e3b3167b`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "d", "kind": "base", "block": null, "base_tables": ["google_ads__device_report"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |


## S36

类别 `data`；来源 `python`；调用 `accc4878a90842868a7e5d8d7e237df0`；状态 `success`。

```sql

SELECT g.year_month, g.campaign_id, g.geo_target, g.cost, g.roas, g.quality_score,
  g.impression_share, g.ctr, g.conversion_rate, g.conversions, g.conversion_value,
  g.cpc, g.cost_per_conversion
FROM google_ads__geo_report g
ORDER BY g.campaign_id, g.year_month, g.geo_target

```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-058/attempt-01/sql/S36.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-058/attempt-01/sql/S36.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-058/attempt-01/results/S36.rows.jsonl)；完整：True；SHA256：`98bf78c0d4e15d853e7c180a250f006b29fae92f332d2707945bd56d92a1477c`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "g", "kind": "base", "block": null, "base_tables": ["google_ads__geo_report"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |


## S37

类别 `data`；来源 `python`；调用 `accc4878a90842868a7e5d8d7e237df0`；状态 `success`。

```sql

SELECT year_month, 
  SUM(cost) AS total_cost,
  SUM(conversions) AS total_conversions,
  SUM(conversion_value) AS total_cv,
  AVG(roas) AS avg_roas,
  AVG(quality_score) AS avg_qs,
  AVG(impression_share) AS avg_is,
  AVG(ctr) AS avg_ctr,
  AVG(conversion_rate) AS avg_cvr
FROM google_ads__campaign_report
GROUP BY year_month
ORDER BY year_month

```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-058/attempt-01/sql/S37.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-058/attempt-01/sql/S37.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-058/attempt-01/results/S37.rows.jsonl)；完整：True；SHA256：`cbda1bc9ff5fff5f16e0c765836e76d11a10682c75cd9dd8cf048d3971f57664`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "google_ads__campaign_report", "kind": "base", "block": null, "base_tables": ["google_ads__campaign_report"]}] | [] | ["year_month"] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | SUM(cost) | [{"table": "google_ads__campaign_report", "column": "cost"}] | [] | False |
| B1 | SUM(conversions) | [{"table": "google_ads__campaign_report", "column": "conversions"}] | [] | False |
| B1 | SUM(conversion_value) | [{"table": "google_ads__campaign_report", "column": "conversion_value"}] | [] | False |
| B1 | AVG(roas) | [{"table": "google_ads__campaign_report", "column": "roas"}] | [] | False |
| B1 | AVG(quality_score) | [{"table": "google_ads__campaign_report", "column": "quality_score"}] | [] | False |
| B1 | AVG(impression_share) | [{"table": "google_ads__campaign_report", "column": "impression_share"}] | [] | False |
| B1 | AVG(ctr) | [{"table": "google_ads__campaign_report", "column": "ctr"}] | [] | False |
| B1 | AVG(conversion_rate) | [{"table": "google_ads__campaign_report", "column": "conversion_rate"}] | [] | False |


## S38

类别 `data`；来源 `python`；调用 `93ef26ffc1104297a70e1209c572a53c`；状态 `success`。

```sql

SELECT d.year_month, d.campaign_id, d.device_type, d.cost, d.roas, d.quality_score, 
  d.impression_share, d.ctr, d.conversion_rate, d.conversions, d.conversion_value,
  d.cpc, d.cost_per_conversion
FROM google_ads__device_report d
ORDER BY d.campaign_id, d.year_month, d.device_type

```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-058/attempt-01/sql/S38.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-058/attempt-01/sql/S38.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-058/attempt-01/results/S38.rows.jsonl)；完整：True；SHA256：`6b7145a341a460db4717be45b49b4f819e01c95a2290537973b030a2e3b3167b`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "d", "kind": "base", "block": null, "base_tables": ["google_ads__device_report"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |


## S39

类别 `data`；来源 `python`；调用 `93ef26ffc1104297a70e1209c572a53c`；状态 `success`。

```sql

SELECT g.year_month, g.campaign_id, g.geo_target, g.cost, g.roas, g.quality_score,
  g.impression_share, g.ctr, g.conversion_rate, g.conversions, g.conversion_value,
  g.cpc, g.cost_per_conversion
FROM google_ads__geo_report g
ORDER BY g.campaign_id, g.year_month, g.geo_target

```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-058/attempt-01/sql/S39.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-058/attempt-01/sql/S39.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-058/attempt-01/results/S39.rows.jsonl)；完整：True；SHA256：`98bf78c0d4e15d853e7c180a250f006b29fae92f332d2707945bd56d92a1477c`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "g", "kind": "base", "block": null, "base_tables": ["google_ads__geo_report"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |


## S40

类别 `data`；来源 `python`；调用 `93ef26ffc1104297a70e1209c572a53c`；状态 `success`。

```sql

SELECT year_month, SUM(cost) AS total_cost, SUM(conversions) AS total_conversions,
  SUM(conversion_value) AS total_cv, AVG(roas) AS avg_roas,
  AVG(quality_score) AS avg_qs, AVG(impression_share) AS avg_is,
  AVG(ctr) AS avg_ctr, AVG(conversion_rate) AS avg_cvr
FROM google_ads__campaign_report
GROUP BY year_month ORDER BY year_month

```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-058/attempt-01/sql/S40.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-058/attempt-01/sql/S40.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-058/attempt-01/results/S40.rows.jsonl)；完整：True；SHA256：`cbda1bc9ff5fff5f16e0c765836e76d11a10682c75cd9dd8cf048d3971f57664`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "google_ads__campaign_report", "kind": "base", "block": null, "base_tables": ["google_ads__campaign_report"]}] | [] | ["year_month"] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | SUM(cost) | [{"table": "google_ads__campaign_report", "column": "cost"}] | [] | False |
| B1 | SUM(conversions) | [{"table": "google_ads__campaign_report", "column": "conversions"}] | [] | False |
| B1 | SUM(conversion_value) | [{"table": "google_ads__campaign_report", "column": "conversion_value"}] | [] | False |
| B1 | AVG(roas) | [{"table": "google_ads__campaign_report", "column": "roas"}] | [] | False |
| B1 | AVG(quality_score) | [{"table": "google_ads__campaign_report", "column": "quality_score"}] | [] | False |
| B1 | AVG(impression_share) | [{"table": "google_ads__campaign_report", "column": "impression_share"}] | [] | False |
| B1 | AVG(ctr) | [{"table": "google_ads__campaign_report", "column": "ctr"}] | [] | False |
| B1 | AVG(conversion_rate) | [{"table": "google_ads__campaign_report", "column": "conversion_rate"}] | [] | False |


## S41

类别 `data`；来源 `python`；调用 `3604552a87ea4c83b4a6536edfcfc6ee`；状态 `success`。

```sql

SELECT k.* FROM google_ads__keyword_report k ORDER BY k.campaign_id, k.year_quarter

```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-058/attempt-01/sql/S41.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-058/attempt-01/sql/S41.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-058/attempt-01/results/S41.rows.jsonl)；完整：True；SHA256：`eecfecab7d6e7f4410cc64dc442a655249905df534efba713f1b0f866fe7eda9`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "k", "kind": "base", "block": null, "base_tables": ["google_ads__keyword_report"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |


## S42

类别 `data`；来源 `python`；调用 `3604552a87ea4c83b4a6536edfcfc6ee`；状态 `success`。

```sql

SELECT campaign_id, device_type, ROUND(SUM(cost),0) AS cost, ROUND(AVG(roas),3) AS avg_roas,
  ROUND(AVG(quality_score),2) AS avg_qs, ROUND(AVG(conversion_rate),5) AS avg_cvr,
  ROUND(AVG(ctr),5) AS avg_ctr
FROM google_ads__device_report
WHERE campaign_id IN (105,135,36,184,180,56,69,148,178,27)
GROUP BY campaign_id, device_type
ORDER BY campaign_id, device_type

```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-058/attempt-01/sql/S42.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-058/attempt-01/sql/S42.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-058/attempt-01/results/S42.rows.jsonl)；完整：True；SHA256：`85aa3b4b9c294ed9d01ead5c28174e092a4552e76568898958fb3c9f2056a660`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "google_ads__device_report", "kind": "base", "block": null, "base_tables": ["google_ads__device_report"]}] | [] | ["campaign_id", "device_type"] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | SUM(cost) | [{"table": "google_ads__device_report", "column": "cost"}] | [] | False |
| B1 | AVG(roas) | [{"table": "google_ads__device_report", "column": "roas"}] | [] | False |
| B1 | AVG(quality_score) | [{"table": "google_ads__device_report", "column": "quality_score"}] | [] | False |
| B1 | AVG(conversion_rate) | [{"table": "google_ads__device_report", "column": "conversion_rate"}] | [] | False |
| B1 | AVG(ctr) | [{"table": "google_ads__device_report", "column": "ctr"}] | [] | False |


## S43

类别 `data`；来源 `python`；调用 `e5d82c9475094b0da4d9c993096c10de`；状态 `success`。

```sql

SELECT campaign_id, geo_target, ROUND(SUM(cost),0) AS cost, ROUND(AVG(roas),3) AS avg_roas,
  ROUND(AVG(quality_score),2) AS avg_qs, ROUND(AVG(conversion_rate),5) AS avg_cvr,
  ROUND(AVG(ctr),5) AS avg_ctr, ROUND(SUM(conversions),2) AS conversions,
  ROUND(SUM(conversion_value),0) AS cv
FROM google_ads__geo_report
WHERE campaign_id IN (105,135,36,184,180,56,69,148,178,27)
GROUP BY campaign_id, geo_target
ORDER BY campaign_id, cost DESC

```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-058/attempt-01/sql/S43.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-058/attempt-01/sql/S43.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-058/attempt-01/results/S43.rows.jsonl)；完整：True；SHA256：`8de3001338f6f9a45f65bcb172ff8e39df84a2263283707477bfe5156c5e0995`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "google_ads__geo_report", "kind": "base", "block": null, "base_tables": ["google_ads__geo_report"]}] | [] | ["campaign_id", "geo_target"] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | SUM(cost) | [{"table": "google_ads__geo_report", "column": "cost"}] | [] | False |
| B1 | AVG(roas) | [{"table": "google_ads__geo_report", "column": "roas"}] | [] | False |
| B1 | AVG(quality_score) | [{"table": "google_ads__geo_report", "column": "quality_score"}] | [] | False |
| B1 | AVG(conversion_rate) | [{"table": "google_ads__geo_report", "column": "conversion_rate"}] | [] | False |
| B1 | AVG(ctr) | [{"table": "google_ads__geo_report", "column": "ctr"}] | [] | False |
| B1 | SUM(conversions) | [{"table": "google_ads__geo_report", "column": "conversions"}] | [] | False |
| B1 | SUM(conversion_value) | [{"table": "google_ads__geo_report", "column": "conversion_value"}] | [] | False |


## S44

类别 `data`；来源 `python`；调用 `e5d82c9475094b0da4d9c993096c10de`；状态 `success`。

```sql

SELECT k.* FROM google_ads__keyword_report k
WHERE k.campaign_id IN (105,135,36,184,180,56,69,148,178,27)
ORDER BY k.campaign_id, k.year_quarter

```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-058/attempt-01/sql/S44.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-058/attempt-01/sql/S44.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-058/attempt-01/results/S44.rows.jsonl)；完整：True；SHA256：`ee9452ca3d96c9d0afd964106d6ca507e48541a0839c0733ee1f169e8398eb6e`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "k", "kind": "base", "block": null, "base_tables": ["google_ads__keyword_report"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |


## S45

类别 `data`；来源 `python`；调用 `e5d82c9475094b0da4d9c993096c10de`；状态 `success`。

```sql

SELECT year_month, campaign_id, campaign_name, campaign_type, bidding_strategy, industry,
  cost, roas, quality_score, impression_share, ctr, conversion_rate, conversions, conversion_value
FROM google_ads__campaign_report
WHERE campaign_id IN (105,135,36,184,180,56,69,148,178,27)
ORDER BY campaign_id, year_month

```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-058/attempt-01/sql/S45.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-058/attempt-01/sql/S45.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-058/attempt-01/results/S45.rows.jsonl)；完整：True；SHA256：`24cf204dbcfc63471f305f0641973723068a47e4966ce63dd65923b441c6263b`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "google_ads__campaign_report", "kind": "base", "block": null, "base_tables": ["google_ads__campaign_report"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |


## S46

类别 `data`；来源 `python`；调用 `e5d82c9475094b0da4d9c993096c10de`；状态 `success`。

```sql

SELECT campaign_id, device_type, ROUND(SUM(cost),0) AS cost
FROM google_ads__device_report
WHERE campaign_id IN (105,135,36,184,180,56,69,148,178,27)
GROUP BY campaign_id, device_type
ORDER BY campaign_id, device_type

```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-058/attempt-01/sql/S46.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-058/attempt-01/sql/S46.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-058/attempt-01/results/S46.rows.jsonl)；完整：True；SHA256：`abb75cf696a15bec06881d20bab030dd53b6645de4e94d7e1f872791adbac9a5`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "google_ads__device_report", "kind": "base", "block": null, "base_tables": ["google_ads__device_report"]}] | [] | ["campaign_id", "device_type"] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | SUM(cost) | [{"table": "google_ads__device_report", "column": "cost"}] | [] | False |


## S47

类别 `data`；来源 `python`；调用 `ac491dfa20c64da69e58140b703fa7ad`；状态 `success`。

```sql

SELECT campaign_id, campaign_name, campaign_type, bidding_strategy, industry,
  COUNT(*) AS total_months,
  COUNT(CASE WHEN cost > 1000 AND roas < 0.8 THEN 1 END) AS screened_months
FROM google_ads__campaign_report
GROUP BY campaign_id
ORDER BY screened_months DESC

```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-058/attempt-01/sql/S47.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-058/attempt-01/sql/S47.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-058/attempt-01/results/S47.rows.jsonl)；完整：True；SHA256：`e22074cfc6f50ef075cd1af23588c4a9a50c25fb0c2908d3639b57819e5aee93`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "google_ads__campaign_report", "kind": "base", "block": null, "base_tables": ["google_ads__campaign_report"]}] | [] | ["campaign_id"] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |
| B1 | COUNT(CASE WHEN cost > 1000 AND roas < 0.8 THEN 1 END) | [] | [{"table": "google_ads__campaign_report", "column": "cost"}, {"table": "google_ads__campaign_report", "column": "roas"}] | False |


## S48

类别 `data`；来源 `python`；调用 `ac491dfa20c64da69e58140b703fa7ad`；状态 `success`。

```sql
SELECT COUNT(DISTINCT campaign_id) AS campaigns_with_bad_roas FROM google_ads__campaign_report WHERE roas < 0.8
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-058/attempt-01/sql/S48.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-058/attempt-01/sql/S48.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-058/attempt-01/results/S48.rows.jsonl)；完整：True；SHA256：`66c03021c935d5575384b1505bf582d78516cc55be41a4d3026e9ebbc9c3fef2`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "google_ads__campaign_report", "kind": "base", "block": null, "base_tables": ["google_ads__campaign_report"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(DISTINCT campaign_id) | [{"table": "google_ads__campaign_report", "column": "campaign_id"}] | [] | False |


## S49

类别 `data`；来源 `python`；调用 `ac491dfa20c64da69e58140b703fa7ad`；状态 `success`。

```sql

SELECT 
  ROUND(SUM(CASE WHEN campaign_id IN (105,135,36,184,180,56,69,148,178,27) THEN cost ELSE 0 END),0) AS prob_cost,
  ROUND(SUM(cost),0) AS total_cost,
  ROUND(100.0 * SUM(CASE WHEN campaign_id IN (105,135,36,184,180,56,69,148,178,27) THEN cost ELSE 0 END)/SUM(cost), 1) AS pct
FROM google_ads__campaign_report

```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-058/attempt-01/sql/S49.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-058/attempt-01/sql/S49.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-058/attempt-01/results/S49.rows.jsonl)；完整：True；SHA256：`d29a506fe8fe677caf68389cc6ec5494a49c559637189ac5daa5c51269d6f47a`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "google_ads__campaign_report", "kind": "base", "block": null, "base_tables": ["google_ads__campaign_report"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | SUM(CASE WHEN campaign_id IN (105, 135, 36, 184, 180, 56, 69, 148, 178, 27) THEN cost ELSE 0 END) | [{"table": "google_ads__campaign_report", "column": "cost"}] | [{"table": "google_ads__campaign_report", "column": "campaign_id"}] | False |
| B1 | SUM(cost) | [{"table": "google_ads__campaign_report", "column": "cost"}] | [] | False |
| B1 | SUM(cost) | [{"table": "google_ads__campaign_report", "column": "cost"}] | [] | False |
| B1 | SUM(CASE WHEN campaign_id IN (105, 135, 36, 184, 180, 56, 69, 148, 178, 27) THEN cost ELSE 0 END) | [{"table": "google_ads__campaign_report", "column": "cost"}] | [{"table": "google_ads__campaign_report", "column": "campaign_id"}] | False |


## S50

类别 `data`；来源 `python`；调用 `ac491dfa20c64da69e58140b703fa7ad`；状态 `success`。

```sql

WITH base AS (
  SELECT year_month, campaign_id, cost, roas, cpc, cost_per_conversion, conversion_rate,
    conversions, conversion_value, quality_score, impression_share, ctr
  FROM google_ads__campaign_report
),
norm AS (
  SELECT *,
    (roas - MIN(roas) OVER()) / NULLIF(MAX(roas) OVER() - MIN(roas) OVER(), 0) AS roas_s,
    (MAX(cpc) OVER() - cpc) / NULLIF(MAX(cpc) OVER() - MIN(cpc) OVER(), 0) AS cpc_s,
    (MAX(cost_per_conversion) OVER() - cost_per_conversion) / NULLIF(MAX(cost_per_conversion) OVER() - MIN(cost_per_conversion) OVER(), 0) AS cpa_s,
    (conversion_rate - MIN(conversion_rate) OVER()) / NULLIF(MAX(conversion_rate) OVER() - MIN(conversion_rate) OVER(), 0) AS cvr_s,
    (conversion_value/NULLIF(conversions,0) - MIN(conversion_value/NULLIF(conversions,0)) OVER()) / NULLIF(MAX(conversion_value/NULLIF(conversions,0)) OVER() - MIN(conversion_value/NULLIF(conversions,0)) OVER(), 0) AS aov_s,
    (conversions - MIN(conversions) OVER()) / NULLIF(MAX(conversions) OVER() - MIN(conversions) OVER(), 0) AS conv_s,
    (quality_score - MIN(quality_score) OVER()) / NULLIF(MAX(quality_score) OVER() - MIN(quality_score) OVER(), 0) AS qs_s,
    (impression_share - MIN(impression_share) OVER()) / NULLIF(MAX(impression_share) OVER() - MIN(impression_share) OVER(), 0) AS is_s,
    (ctr - MIN(ctr) OVER()) / NULLIF(MAX(ctr) OVER() - MIN(ctr) OVER(), 0) AS ctr_s
  FROM base
)
SELECT year_month, campaign_id,
  100.0 * (0.4*(0.4*roas_s + 0.3*cpa_s + 0.3*cpc_s) + 0.35*(0.4*cvr_s + 0.3*aov_s + 0.3*conv_s) + 0.25*(0.4*qs_s + 0.3*is_s + 0.3*ctr_s)) AS hs
FROM norm
WHERE campaign_id IN (105,135,36,184,180,56,69,148,178,27)
ORDER BY year_month

```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-058/attempt-01/sql/S50.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-058/attempt-01/sql/S50.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-058/attempt-01/results/S50.rows.jsonl)；完整：True；SHA256：`b4341a55cf243c661a6751900fe54de5b2b4f0e0c7293e82a604968ce7ce9000`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "google_ads__campaign_report", "kind": "base", "block": null, "base_tables": ["google_ads__campaign_report"]}] | [] | [] |
| B2 | [{"alias": "base", "kind": "derived", "block": "B1", "base_tables": ["google_ads__campaign_report"]}] | [] | [] |
| B3 | [{"alias": "norm", "kind": "derived", "block": "B2", "base_tables": ["google_ads__campaign_report"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |


## S51

类别 `data`；来源 `python`；调用 `ac491dfa20c64da69e58140b703fa7ad`；状态 `success`。

```sql

SELECT year_month, ROUND(SUM(cost),0) AS total_cost, ROUND(SUM(conversion_value),0) AS total_cv,
  ROUND(SUM(conversions),2) AS total_conv, ROUND(AVG(roas),3) AS avg_roas
FROM google_ads__campaign_report
WHERE campaign_id IN (105,135,36,184,180,56,69,148,178,27)
GROUP BY year_month ORDER BY year_month

```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-058/attempt-01/sql/S51.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-058/attempt-01/sql/S51.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-058/attempt-01/results/S51.rows.jsonl)；完整：True；SHA256：`af660b5408127f1ffed5e15408a65ec73913159d76f70eadab9886489495f5f1`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "google_ads__campaign_report", "kind": "base", "block": null, "base_tables": ["google_ads__campaign_report"]}] | [] | ["year_month"] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | SUM(cost) | [{"table": "google_ads__campaign_report", "column": "cost"}] | [] | False |
| B1 | SUM(conversion_value) | [{"table": "google_ads__campaign_report", "column": "conversion_value"}] | [] | False |
| B1 | SUM(conversions) | [{"table": "google_ads__campaign_report", "column": "conversions"}] | [] | False |
| B1 | AVG(roas) | [{"table": "google_ads__campaign_report", "column": "roas"}] | [] | False |


## S52

类别 `data`；来源 `python`；调用 `cb4d4608c84a407b8de180023c231e64`；状态 `success`。

```sql

WITH base AS (
  SELECT year_month, campaign_id, campaign_name, campaign_type, bidding_strategy, industry,
    cost, conversions, conversion_value, roas, cpc, cost_per_conversion,
    conversion_rate, quality_score, impression_share, ctr
  FROM google_ads__campaign_report
),
norm AS (
  SELECT *,
    (roas - MIN(roas) OVER()) / NULLIF(MAX(roas) OVER() - MIN(roas) OVER(), 0) AS roas_s,
    (MAX(cpc) OVER() - cpc) / NULLIF(MAX(cpc) OVER() - MIN(cpc) OVER(), 0) AS cpc_s,
    (MAX(cost_per_conversion) OVER() - cost_per_conversion) / NULLIF(MAX(cost_per_conversion) OVER() - MIN(cost_per_conversion) OVER(), 0) AS cpa_s,
    (conversion_rate - MIN(conversion_rate) OVER()) / NULLIF(MAX(conversion_rate) OVER() - MIN(conversion_rate) OVER(), 0) AS cvr_s,
    (conversion_value/NULLIF(conversions,0) - MIN(conversion_value/NULLIF(conversions,0)) OVER()) / NULLIF(MAX(conversion_value/NULLIF(conversions,0)) OVER() - MIN(conversion_value/NULLIF(conversions,0)) OVER(), 0) AS aov_s,
    (conversions - MIN(conversions) OVER()) / NULLIF(MAX(conversions) OVER() - MIN(conversions) OVER(), 0) AS conv_s,
    (quality_score - MIN(quality_score) OVER()) / NULLIF(MAX(quality_score) OVER() - MIN(quality_score) OVER(), 0) AS qs_s,
    (impression_share - MIN(impression_share) OVER()) / NULLIF(MAX(impression_share) OVER() - MIN(impression_share) OVER(), 0) AS is_s,
    (ctr - MIN(ctr) OVER()) / NULLIF(MAX(ctr) OVER() - MIN(ctr) OVER(), 0) AS ctr_s
  FROM base
)
SELECT campaign_id, campaign_name, campaign_type, bidding_strategy, industry,
  COUNT(*) AS n_months, ROUND(AVG(cost),0) AS avg_monthly_cost, ROUND(SUM(cost),0) AS total_cost,
  ROUND(AVG(roas),3) AS avg_roas, ROUND(AVG(quality_score),2) AS avg_qs,
  ROUND(AVG(impression_share),3) AS avg_is, ROUND(AVG(ctr),5) AS avg_ctr,
  ROUND(AVG(conversion_rate),5) AS avg_cvr, ROUND(AVG(cpc),2) AS avg_cpc,
  ROUND(AVG(cost_per_conversion),2) AS avg_cpa,
  100.0 * AVG(0.4*roas_s + 0.3*cpa_s + 0.3*cpc_s) AS cost_eff,
  100.0 * AVG(0.4*cvr_s + 0.3*aov_s + 0.3*conv_s) AS conv_quality,
  100.0 * AVG(0.4*qs_s + 0.3*is_s + 0.3*ctr_s) AS competitive,
  100.0 * AVG(0.4*(0.4*roas_s + 0.3*cpa_s + 0.3*cpc_s) + 0.35*(0.4*cvr_s + 0.3*aov_s + 0.3*conv_s) + 0.25*(0.4*qs_s + 0.3*is_s + 0.3*ctr_s)) AS health_score
FROM norm GROUP BY campaign_id ORDER BY health_score

```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-058/attempt-01/sql/S52.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-058/attempt-01/sql/S52.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-058/attempt-01/results/S52.rows.jsonl)；完整：True；SHA256：`3175bd5e05a4e5d519b68a84032df6fd8b05e60a510ab8e3e9c2a3827356f1ec`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "google_ads__campaign_report", "kind": "base", "block": null, "base_tables": ["google_ads__campaign_report"]}] | [] | [] |
| B2 | [{"alias": "base", "kind": "derived", "block": "B1", "base_tables": ["google_ads__campaign_report"]}] | [] | [] |
| B3 | [{"alias": "norm", "kind": "derived", "block": "B2", "base_tables": ["google_ads__campaign_report"]}] | [] | ["campaign_id"] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B3 | COUNT(*) | [] | [] | True |
| B3 | AVG(cost) | [{"table": "google_ads__campaign_report", "column": "cost"}] | [] | False |
| B3 | SUM(cost) | [{"table": "google_ads__campaign_report", "column": "cost"}] | [] | False |
| B3 | AVG(roas) | [{"table": "google_ads__campaign_report", "column": "roas"}] | [] | False |
| B3 | AVG(quality_score) | [{"table": "google_ads__campaign_report", "column": "quality_score"}] | [] | False |
| B3 | AVG(impression_share) | [{"table": "google_ads__campaign_report", "column": "impression_share"}] | [] | False |
| B3 | AVG(ctr) | [{"table": "google_ads__campaign_report", "column": "ctr"}] | [] | False |
| B3 | AVG(conversion_rate) | [{"table": "google_ads__campaign_report", "column": "conversion_rate"}] | [] | False |
| B3 | AVG(cpc) | [{"table": "google_ads__campaign_report", "column": "cpc"}] | [] | False |
| B3 | AVG(cost_per_conversion) | [{"table": "google_ads__campaign_report", "column": "cost_per_conversion"}] | [] | False |
| B3 | AVG(0.4 * roas_s + 0.3 * cpa_s + 0.3 * cpc_s) | [{"table": "google_ads__campaign_report", "column": "cpc"}, {"table": "google_ads__campaign_report", "column": "cpc"}, {"table": "google_ads__campaign_report", "column": "cpc"}, {"table": "google_ads__campaign_report", "column": "cpc"}, {"table": "google_ads__campaign_report", "column": "roas"}, {"table": "google_ads__campaign_report", "column": "roas"}, {"table": "google_ads__campaign_report", "column": "roas"}, {"table": "google_ads__campaign_report", "column": "roas"}, {"table": "google_ads__campaign_report", "column": "cost_per_conversion"}, {"table": "google_ads__campaign_report", "column": "cost_per_conversion"}, {"table": "google_ads__campaign_report", "column": "cost_per_conversion"}, {"table": "google_ads__campaign_report", "column": "cost_per_conversion"}] | [] | False |
| B3 | AVG(0.4 * cvr_s + 0.3 * aov_s + 0.3 * conv_s) | [{"table": "google_ads__campaign_report", "column": "conversions"}, {"table": "google_ads__campaign_report", "column": "conversions"}, {"table": "google_ads__campaign_report", "column": "conversions"}, {"table": "google_ads__campaign_report", "column": "conversions"}, {"table": "google_ads__campaign_report", "column": "conversion_rate"}, {"table": "google_ads__campaign_report", "column": "conversion_rate"}, {"table": "google_ads__campaign_report", "column": "conversion_rate"}, {"table": "google_ads__campaign_report", "column": "conversion_rate"}, {"table": "google_ads__campaign_report", "column": "conversion_value"}, {"table": "google_ads__campaign_report", "column": "conversions"}, {"table": "google_ads__campaign_report", "column": "conversion_value"}, {"table": "google_ads__campaign_report", "column": "conversion_value"}, {"table": "google_ads__campaign_report", "column": "conversion_value"}, {"table": "google_ads__campaign_report", "column": "conversions"}, {"table": "google_ads__campaign_report", "column": "conversions"}, {"table": "google_ads__campaign_report", "column": "conversions"}] | [] | False |
| B3 | AVG(0.4 * qs_s + 0.3 * is_s + 0.3 * ctr_s) | [{"table": "google_ads__campaign_report", "column": "ctr"}, {"table": "google_ads__campaign_report", "column": "ctr"}, {"table": "google_ads__campaign_report", "column": "ctr"}, {"table": "google_ads__campaign_report", "column": "ctr"}, {"table": "google_ads__campaign_report", "column": "quality_score"}, {"table": "google_ads__campaign_report", "column": "quality_score"}, {"table": "google_ads__campaign_report", "column": "quality_score"}, {"table": "google_ads__campaign_report", "column": "quality_score"}, {"table": "google_ads__campaign_report", "column": "impression_share"}, {"table": "google_ads__campaign_report", "column": "impression_share"}, {"table": "google_ads__campaign_report", "column": "impression_share"}, {"table": "google_ads__campaign_report", "column": "impression_share"}] | [] | False |
| B3 | AVG(0.4 * (0.4 * roas_s + 0.3 * cpa_s + 0.3 * cpc_s) + 0.35 * (0.4 * cvr_s + 0.3 * aov_s + 0.3 * conv_s) + 0.25 * (0.4 * qs_s + 0.3 * is_s + 0.3 * ctr_s)) | [{"table": "google_ads__campaign_report", "column": "ctr"}, {"table": "google_ads__campaign_report", "column": "ctr"}, {"table": "google_ads__campaign_report", "column": "ctr"}, {"table": "google_ads__campaign_report", "column": "ctr"}, {"table": "google_ads__campaign_report", "column": "cpc"}, {"table": "google_ads__campaign_report", "column": "cpc"}, {"table": "google_ads__campaign_report", "column": "cpc"}, {"table": "google_ads__campaign_report", "column": "cpc"}, {"table": "google_ads__campaign_report", "column": "conversions"}, {"table": "google_ads__campaign_report", "column": "conversions"}, {"table": "google_ads__campaign_report", "column": "conversions"}, {"table": "google_ads__campaign_report", "column": "conversions"}, {"table": "google_ads__campaign_report", "column": "quality_score"}, {"table": "google_ads__campaign_report", "column": "quality_score"}, {"table": "google_ads__campaign_report", "column": "quality_score"}, {"table": "google_ads__campaign_report", "column": "quality_score"}, {"table": "google_ads__campaign_report", "column": "impression_share"}, {"table": "google_ads__campaign_report", "column": "impression_share"}, {"table": "google_ads__campaign_report", "column": "impression_share"}, {"table": "google_ads__campaign_report", "column": "impression_share"}, {"table": "google_ads__campaign_report", "column": "roas"}, {"table": "google_ads__campaign_report", "column": "roas"}, {"table": "google_ads__campaign_report", "column": "roas"}, {"table": "google_ads__campaign_report", "column": "roas"}, {"table": "google_ads__campaign_report", "column": "cost_per_conversion"}, {"table": "google_ads__campaign_report", "column": "cost_per_conversion"}, {"table": "google_ads__campaign_report", "column": "cost_per_conversion"}, {"table": "google_ads__campaign_report", "column": "cost_per_conversion"}, {"table": "google_ads__campaign_report", "column": "conversion_rate"}, {"table": "google_ads__campaign_report", "column": "conversion_rate"}, {"table": "google_ads__campaign_report", "column": "conversion_rate"}, {"table": "google_ads__campaign_report", "column": "conversion_rate"}, {"table": "google_ads__campaign_report", "column": "conversion_value"}, {"table": "google_ads__campaign_report", "column": "conversions"}, {"table": "google_ads__campaign_report", "column": "conversion_value"}, {"table": "google_ads__campaign_report", "column": "conversion_value"}, {"table": "google_ads__campaign_report", "column": "conversion_value"}, {"table": "google_ads__campaign_report", "column": "conversions"}, {"table": "google_ads__campaign_report", "column": "conversions"}, {"table": "google_ads__campaign_report", "column": "conversions"}] | [] | False |


## S53

类别 `data`；来源 `python`；调用 `cb4d4608c84a407b8de180023c231e64`；状态 `success`。

```sql
SELECT campaign_id, device_type, ROUND(SUM(cost),0) AS cost, ROUND(AVG(roas),3) AS avg_roas FROM google_ads__device_report WHERE campaign_id IN (105,135,36,184,180,56,69,148,178,27) GROUP BY campaign_id, device_type ORDER BY campaign_id, device_type
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-058/attempt-01/sql/S53.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-058/attempt-01/sql/S53.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-058/attempt-01/results/S53.rows.jsonl)；完整：True；SHA256：`8c27f54646f85f408dd87d5ec8349dca01d17bbc876df23f41aa875da3200c84`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "google_ads__device_report", "kind": "base", "block": null, "base_tables": ["google_ads__device_report"]}] | [] | ["campaign_id", "device_type"] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | SUM(cost) | [{"table": "google_ads__device_report", "column": "cost"}] | [] | False |
| B1 | AVG(roas) | [{"table": "google_ads__device_report", "column": "roas"}] | [] | False |


## S54

类别 `data`；来源 `python`；调用 `cb4d4608c84a407b8de180023c231e64`；状态 `success`。

```sql
SELECT campaign_id, geo_target, ROUND(SUM(cost),0) AS cost, ROUND(AVG(roas),3) AS avg_roas FROM google_ads__geo_report WHERE campaign_id IN (105,135,36,184,180,56,69,148,178,27) GROUP BY campaign_id, geo_target ORDER BY campaign_id, cost DESC
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-058/attempt-01/sql/S54.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-058/attempt-01/sql/S54.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-058/attempt-01/results/S54.rows.jsonl)；完整：True；SHA256：`54700a4bc10aaefd93fd96686ab52fc368c7ca989e60ac694f5d57a22ad4e07c`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "google_ads__geo_report", "kind": "base", "block": null, "base_tables": ["google_ads__geo_report"]}] | [] | ["campaign_id", "geo_target"] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | SUM(cost) | [{"table": "google_ads__geo_report", "column": "cost"}] | [] | False |
| B1 | AVG(roas) | [{"table": "google_ads__geo_report", "column": "roas"}] | [] | False |


## S55

类别 `data`；来源 `python`；调用 `0218686d771e4ed59fb301b360039420`；状态 `success`。

```sql

SELECT campaign_id, device_type, ROUND(SUM(cost),0) AS cost, 
  ROUND(SUM(conversion_value)/NULLIF(SUM(cost),0), 3) AS computed_roas,
  ROUND(AVG(roas), 3) AS roas_field,
  ROUND(SUM(conversions),2) AS conversions,
  ROUND(SUM(conversion_value),0) AS cv
FROM google_ads__device_report
WHERE campaign_id IN (105,135,36,184,180,56,69,148,178,27)
GROUP BY campaign_id, device_type
ORDER BY campaign_id, device_type

```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-058/attempt-01/sql/S55.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-058/attempt-01/sql/S55.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-058/attempt-01/results/S55.rows.jsonl)；完整：True；SHA256：`f6c6e30921b49a6c870b786da066681c06a77c1dc16ff18d8511b9fae48e2c62`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "google_ads__device_report", "kind": "base", "block": null, "base_tables": ["google_ads__device_report"]}] | [] | ["campaign_id", "device_type"] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | SUM(cost) | [{"table": "google_ads__device_report", "column": "cost"}] | [] | False |
| B1 | AVG(roas) | [{"table": "google_ads__device_report", "column": "roas"}] | [] | False |
| B1 | SUM(conversions) | [{"table": "google_ads__device_report", "column": "conversions"}] | [] | False |
| B1 | SUM(conversion_value) | [{"table": "google_ads__device_report", "column": "conversion_value"}] | [] | False |
| B1 | SUM(conversion_value) | [{"table": "google_ads__device_report", "column": "conversion_value"}] | [] | False |
| B1 | SUM(cost) | [{"table": "google_ads__device_report", "column": "cost"}] | [] | False |


## S56

类别 `data`；来源 `python`；调用 `0218686d771e4ed59fb301b360039420`；状态 `success`。

```sql

SELECT campaign_id, geo_target, ROUND(SUM(cost),0) AS cost,
  ROUND(SUM(conversion_value)/NULLIF(SUM(cost),0), 3) AS computed_roas,
  ROUND(AVG(roas), 3) AS roas_field,
  ROUND(SUM(conversions),2) AS conversions,
  ROUND(SUM(conversion_value),0) AS cv
FROM google_ads__geo_report
WHERE campaign_id IN (105,135,36,184,180,56,69,148,178,27)
GROUP BY campaign_id, geo_target
ORDER BY campaign_id, geo_target

```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-058/attempt-01/sql/S56.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-058/attempt-01/sql/S56.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-058/attempt-01/results/S56.rows.jsonl)；完整：True；SHA256：`158f8f50e62c9e8969e6e08fbbf0837b7b64d0fc11ada8453ccd1656aec6a86c`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "google_ads__geo_report", "kind": "base", "block": null, "base_tables": ["google_ads__geo_report"]}] | [] | ["campaign_id", "geo_target"] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | SUM(cost) | [{"table": "google_ads__geo_report", "column": "cost"}] | [] | False |
| B1 | AVG(roas) | [{"table": "google_ads__geo_report", "column": "roas"}] | [] | False |
| B1 | SUM(conversions) | [{"table": "google_ads__geo_report", "column": "conversions"}] | [] | False |
| B1 | SUM(conversion_value) | [{"table": "google_ads__geo_report", "column": "conversion_value"}] | [] | False |
| B1 | SUM(conversion_value) | [{"table": "google_ads__geo_report", "column": "conversion_value"}] | [] | False |
| B1 | SUM(cost) | [{"table": "google_ads__geo_report", "column": "cost"}] | [] | False |


## S57

类别 `data`；来源 `python`；调用 `170eef6d4621462d93390ced60808bc8`；状态 `success`。

```sql

WITH base AS (
  SELECT year_month, campaign_id, campaign_name, campaign_type, bidding_strategy, industry,
    cost, conversions, conversion_value, roas, cpc, cost_per_conversion,
    conversion_rate, quality_score, impression_share, ctr
  FROM google_ads__campaign_report
),
norm AS (
  SELECT *,
    (roas - MIN(roas) OVER()) / NULLIF(MAX(roas) OVER() - MIN(roas) OVER(), 0) AS roas_s,
    (MAX(cpc) OVER() - cpc) / NULLIF(MAX(cpc) OVER() - MIN(cpc) OVER(), 0) AS cpc_s,
    (MAX(cost_per_conversion) OVER() - cost_per_conversion) / NULLIF(MAX(cost_per_conversion) OVER() - MIN(cost_per_conversion) OVER(), 0) AS cpa_s,
    (conversion_rate - MIN(conversion_rate) OVER()) / NULLIF(MAX(conversion_rate) OVER() - MIN(conversion_rate) OVER(), 0) AS cvr_s,
    (conversion_value/NULLIF(conversions,0) - MIN(conversion_value/NULLIF(conversions,0)) OVER()) / NULLIF(MAX(conversion_value/NULLIF(conversions,0)) OVER() - MIN(conversion_value/NULLIF(conversions,0)) OVER(), 0) AS aov_s,
    (conversions - MIN(conversions) OVER()) / NULLIF(MAX(conversions) OVER() - MIN(conversions) OVER(), 0) AS conv_s,
    (quality_score - MIN(quality_score) OVER()) / NULLIF(MAX(quality_score) OVER() - MIN(quality_score) OVER(), 0) AS qs_s,
    (impression_share - MIN(impression_share) OVER()) / NULLIF(MAX(impression_share) OVER() - MIN(impression_share) OVER(), 0) AS is_s,
    (ctr - MIN(ctr) OVER()) / NULLIF(MAX(ctr) OVER() - MIN(ctr) OVER(), 0) AS ctr_s
  FROM base
)
SELECT campaign_id, campaign_name, campaign_type, bidding_strategy, industry,
  SUM(cost) AS total_cost, AVG(roas) AS avg_roas,
  100.0 * AVG(0.4*roas_s + 0.3*cpa_s + 0.3*cpc_s) AS cost_eff,
  100.0 * AVG(0.4*cvr_s + 0.3*aov_s + 0.3*conv_s) AS conv_quality,
  100.0 * AVG(0.4*qs_s + 0.3*is_s + 0.3*ctr_s) AS competitive,
  100.0 * AVG(0.4*(0.4*roas_s + 0.3*cpa_s + 0.3*cpc_s) + 0.35*(0.4*cvr_s + 0.3*aov_s + 0.3*conv_s) + 0.25*(0.4*qs_s + 0.3*is_s + 0.3*ctr_s)) AS health_score
FROM norm GROUP BY campaign_id ORDER BY health_score

```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-058/attempt-01/sql/S57.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-058/attempt-01/sql/S57.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-058/attempt-01/results/S57.rows.jsonl)；完整：True；SHA256：`e2d92ce494bc248e2033150b50f967ec3eadcf0033aa6fcd1aa7da910f6f181c`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "google_ads__campaign_report", "kind": "base", "block": null, "base_tables": ["google_ads__campaign_report"]}] | [] | [] |
| B2 | [{"alias": "base", "kind": "derived", "block": "B1", "base_tables": ["google_ads__campaign_report"]}] | [] | [] |
| B3 | [{"alias": "norm", "kind": "derived", "block": "B2", "base_tables": ["google_ads__campaign_report"]}] | [] | ["campaign_id"] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B3 | SUM(cost) | [{"table": "google_ads__campaign_report", "column": "cost"}] | [] | False |
| B3 | AVG(roas) | [{"table": "google_ads__campaign_report", "column": "roas"}] | [] | False |
| B3 | AVG(0.4 * roas_s + 0.3 * cpa_s + 0.3 * cpc_s) | [{"table": "google_ads__campaign_report", "column": "cpc"}, {"table": "google_ads__campaign_report", "column": "cpc"}, {"table": "google_ads__campaign_report", "column": "cpc"}, {"table": "google_ads__campaign_report", "column": "cpc"}, {"table": "google_ads__campaign_report", "column": "roas"}, {"table": "google_ads__campaign_report", "column": "roas"}, {"table": "google_ads__campaign_report", "column": "roas"}, {"table": "google_ads__campaign_report", "column": "roas"}, {"table": "google_ads__campaign_report", "column": "cost_per_conversion"}, {"table": "google_ads__campaign_report", "column": "cost_per_conversion"}, {"table": "google_ads__campaign_report", "column": "cost_per_conversion"}, {"table": "google_ads__campaign_report", "column": "cost_per_conversion"}] | [] | False |
| B3 | AVG(0.4 * cvr_s + 0.3 * aov_s + 0.3 * conv_s) | [{"table": "google_ads__campaign_report", "column": "conversions"}, {"table": "google_ads__campaign_report", "column": "conversions"}, {"table": "google_ads__campaign_report", "column": "conversions"}, {"table": "google_ads__campaign_report", "column": "conversions"}, {"table": "google_ads__campaign_report", "column": "conversion_rate"}, {"table": "google_ads__campaign_report", "column": "conversion_rate"}, {"table": "google_ads__campaign_report", "column": "conversion_rate"}, {"table": "google_ads__campaign_report", "column": "conversion_rate"}, {"table": "google_ads__campaign_report", "column": "conversion_value"}, {"table": "google_ads__campaign_report", "column": "conversions"}, {"table": "google_ads__campaign_report", "column": "conversion_value"}, {"table": "google_ads__campaign_report", "column": "conversion_value"}, {"table": "google_ads__campaign_report", "column": "conversion_value"}, {"table": "google_ads__campaign_report", "column": "conversions"}, {"table": "google_ads__campaign_report", "column": "conversions"}, {"table": "google_ads__campaign_report", "column": "conversions"}] | [] | False |
| B3 | AVG(0.4 * qs_s + 0.3 * is_s + 0.3 * ctr_s) | [{"table": "google_ads__campaign_report", "column": "ctr"}, {"table": "google_ads__campaign_report", "column": "ctr"}, {"table": "google_ads__campaign_report", "column": "ctr"}, {"table": "google_ads__campaign_report", "column": "ctr"}, {"table": "google_ads__campaign_report", "column": "quality_score"}, {"table": "google_ads__campaign_report", "column": "quality_score"}, {"table": "google_ads__campaign_report", "column": "quality_score"}, {"table": "google_ads__campaign_report", "column": "quality_score"}, {"table": "google_ads__campaign_report", "column": "impression_share"}, {"table": "google_ads__campaign_report", "column": "impression_share"}, {"table": "google_ads__campaign_report", "column": "impression_share"}, {"table": "google_ads__campaign_report", "column": "impression_share"}] | [] | False |
| B3 | AVG(0.4 * (0.4 * roas_s + 0.3 * cpa_s + 0.3 * cpc_s) + 0.35 * (0.4 * cvr_s + 0.3 * aov_s + 0.3 * conv_s) + 0.25 * (0.4 * qs_s + 0.3 * is_s + 0.3 * ctr_s)) | [{"table": "google_ads__campaign_report", "column": "ctr"}, {"table": "google_ads__campaign_report", "column": "ctr"}, {"table": "google_ads__campaign_report", "column": "ctr"}, {"table": "google_ads__campaign_report", "column": "ctr"}, {"table": "google_ads__campaign_report", "column": "cpc"}, {"table": "google_ads__campaign_report", "column": "cpc"}, {"table": "google_ads__campaign_report", "column": "cpc"}, {"table": "google_ads__campaign_report", "column": "cpc"}, {"table": "google_ads__campaign_report", "column": "conversions"}, {"table": "google_ads__campaign_report", "column": "conversions"}, {"table": "google_ads__campaign_report", "column": "conversions"}, {"table": "google_ads__campaign_report", "column": "conversions"}, {"table": "google_ads__campaign_report", "column": "quality_score"}, {"table": "google_ads__campaign_report", "column": "quality_score"}, {"table": "google_ads__campaign_report", "column": "quality_score"}, {"table": "google_ads__campaign_report", "column": "quality_score"}, {"table": "google_ads__campaign_report", "column": "impression_share"}, {"table": "google_ads__campaign_report", "column": "impression_share"}, {"table": "google_ads__campaign_report", "column": "impression_share"}, {"table": "google_ads__campaign_report", "column": "impression_share"}, {"table": "google_ads__campaign_report", "column": "roas"}, {"table": "google_ads__campaign_report", "column": "roas"}, {"table": "google_ads__campaign_report", "column": "roas"}, {"table": "google_ads__campaign_report", "column": "roas"}, {"table": "google_ads__campaign_report", "column": "cost_per_conversion"}, {"table": "google_ads__campaign_report", "column": "cost_per_conversion"}, {"table": "google_ads__campaign_report", "column": "cost_per_conversion"}, {"table": "google_ads__campaign_report", "column": "cost_per_conversion"}, {"table": "google_ads__campaign_report", "column": "conversion_rate"}, {"table": "google_ads__campaign_report", "column": "conversion_rate"}, {"table": "google_ads__campaign_report", "column": "conversion_rate"}, {"table": "google_ads__campaign_report", "column": "conversion_rate"}, {"table": "google_ads__campaign_report", "column": "conversion_value"}, {"table": "google_ads__campaign_report", "column": "conversions"}, {"table": "google_ads__campaign_report", "column": "conversion_value"}, {"table": "google_ads__campaign_report", "column": "conversion_value"}, {"table": "google_ads__campaign_report", "column": "conversion_value"}, {"table": "google_ads__campaign_report", "column": "conversions"}, {"table": "google_ads__campaign_report", "column": "conversions"}, {"table": "google_ads__campaign_report", "column": "conversions"}] | [] | False |


## S58

类别 `data`；来源 `python`；调用 `27c39b48dd324413b4cab0d7bfee579f`；状态 `success`。

```sql

WITH base AS (
  SELECT year_month, campaign_id, campaign_name, campaign_type, bidding_strategy, industry,
    cost, conversions, conversion_value, roas, cpc, cost_per_conversion,
    conversion_rate, quality_score, impression_share, ctr
  FROM google_ads__campaign_report
),
norm AS (
  SELECT *,
    (roas - MIN(roas) OVER()) / NULLIF(MAX(roas) OVER() - MIN(roas) OVER(), 0) AS roas_s,
    (MAX(cpc) OVER() - cpc) / NULLIF(MAX(cpc) OVER() - MIN(cpc) OVER(), 0) AS cpc_s,
    (MAX(cost_per_conversion) OVER() - cost_per_conversion) / NULLIF(MAX(cost_per_conversion) OVER() - MIN(cost_per_conversion) OVER(), 0) AS cpa_s,
    (conversion_rate - MIN(conversion_rate) OVER()) / NULLIF(MAX(conversion_rate) OVER() - MIN(conversion_rate) OVER(), 0) AS cvr_s,
    (conversion_value/NULLIF(conversions,0) - MIN(conversion_value/NULLIF(conversions,0)) OVER()) / NULLIF(MAX(conversion_value/NULLIF(conversions,0)) OVER() - MIN(conversion_value/NULLIF(conversions,0)) OVER(), 0) AS aov_s,
    (conversions - MIN(conversions) OVER()) / NULLIF(MAX(conversions) OVER() - MIN(conversions) OVER(), 0) AS conv_s,
    (quality_score - MIN(quality_score) OVER()) / NULLIF(MAX(quality_score) OVER() - MIN(quality_score) OVER(), 0) AS qs_s,
    (impression_share - MIN(impression_share) OVER()) / NULLIF(MAX(impression_share) OVER() - MIN(impression_share) OVER(), 0) AS is_s,
    (ctr - MIN(ctr) OVER()) / NULLIF(MAX(ctr) OVER() - MIN(ctr) OVER(), 0) AS ctr_s
  FROM base
)
SELECT campaign_id, campaign_name, campaign_type, bidding_strategy, industry,
  SUM(cost) AS total_cost,
  100.0 * AVG(0.4*roas_s + 0.3*cpa_s + 0.3*cpc_s) AS cost_eff,
  100.0 * AVG(0.4*cvr_s + 0.3*aov_s + 0.3*conv_s) AS conv_quality,
  100.0 * AVG(0.4*qs_s + 0.3*is_s + 0.3*ctr_s) AS competitive,
  100.0 * AVG(0.4*(0.4*roas_s + 0.3*cpa_s + 0.3*cpc_s) + 0.35*(0.4*cvr_s + 0.3*aov_s + 0.3*conv_s) + 0.25*(0.4*qs_s + 0.3*is_s + 0.3*ctr_s)) AS health_score
FROM norm GROUP BY campaign_id ORDER BY health_score

```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-058/attempt-01/sql/S58.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-058/attempt-01/sql/S58.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-058/attempt-01/results/S58.rows.jsonl)；完整：True；SHA256：`887674e14bfbe872ca38ef319bf458251f1e82bf0e449adc71457ad7e501d437`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "google_ads__campaign_report", "kind": "base", "block": null, "base_tables": ["google_ads__campaign_report"]}] | [] | [] |
| B2 | [{"alias": "base", "kind": "derived", "block": "B1", "base_tables": ["google_ads__campaign_report"]}] | [] | [] |
| B3 | [{"alias": "norm", "kind": "derived", "block": "B2", "base_tables": ["google_ads__campaign_report"]}] | [] | ["campaign_id"] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B3 | SUM(cost) | [{"table": "google_ads__campaign_report", "column": "cost"}] | [] | False |
| B3 | AVG(0.4 * roas_s + 0.3 * cpa_s + 0.3 * cpc_s) | [{"table": "google_ads__campaign_report", "column": "cpc"}, {"table": "google_ads__campaign_report", "column": "cpc"}, {"table": "google_ads__campaign_report", "column": "cpc"}, {"table": "google_ads__campaign_report", "column": "cpc"}, {"table": "google_ads__campaign_report", "column": "roas"}, {"table": "google_ads__campaign_report", "column": "roas"}, {"table": "google_ads__campaign_report", "column": "roas"}, {"table": "google_ads__campaign_report", "column": "roas"}, {"table": "google_ads__campaign_report", "column": "cost_per_conversion"}, {"table": "google_ads__campaign_report", "column": "cost_per_conversion"}, {"table": "google_ads__campaign_report", "column": "cost_per_conversion"}, {"table": "google_ads__campaign_report", "column": "cost_per_conversion"}] | [] | False |
| B3 | AVG(0.4 * cvr_s + 0.3 * aov_s + 0.3 * conv_s) | [{"table": "google_ads__campaign_report", "column": "conversions"}, {"table": "google_ads__campaign_report", "column": "conversions"}, {"table": "google_ads__campaign_report", "column": "conversions"}, {"table": "google_ads__campaign_report", "column": "conversions"}, {"table": "google_ads__campaign_report", "column": "conversion_rate"}, {"table": "google_ads__campaign_report", "column": "conversion_rate"}, {"table": "google_ads__campaign_report", "column": "conversion_rate"}, {"table": "google_ads__campaign_report", "column": "conversion_rate"}, {"table": "google_ads__campaign_report", "column": "conversion_value"}, {"table": "google_ads__campaign_report", "column": "conversions"}, {"table": "google_ads__campaign_report", "column": "conversion_value"}, {"table": "google_ads__campaign_report", "column": "conversion_value"}, {"table": "google_ads__campaign_report", "column": "conversion_value"}, {"table": "google_ads__campaign_report", "column": "conversions"}, {"table": "google_ads__campaign_report", "column": "conversions"}, {"table": "google_ads__campaign_report", "column": "conversions"}] | [] | False |
| B3 | AVG(0.4 * qs_s + 0.3 * is_s + 0.3 * ctr_s) | [{"table": "google_ads__campaign_report", "column": "ctr"}, {"table": "google_ads__campaign_report", "column": "ctr"}, {"table": "google_ads__campaign_report", "column": "ctr"}, {"table": "google_ads__campaign_report", "column": "ctr"}, {"table": "google_ads__campaign_report", "column": "quality_score"}, {"table": "google_ads__campaign_report", "column": "quality_score"}, {"table": "google_ads__campaign_report", "column": "quality_score"}, {"table": "google_ads__campaign_report", "column": "quality_score"}, {"table": "google_ads__campaign_report", "column": "impression_share"}, {"table": "google_ads__campaign_report", "column": "impression_share"}, {"table": "google_ads__campaign_report", "column": "impression_share"}, {"table": "google_ads__campaign_report", "column": "impression_share"}] | [] | False |
| B3 | AVG(0.4 * (0.4 * roas_s + 0.3 * cpa_s + 0.3 * cpc_s) + 0.35 * (0.4 * cvr_s + 0.3 * aov_s + 0.3 * conv_s) + 0.25 * (0.4 * qs_s + 0.3 * is_s + 0.3 * ctr_s)) | [{"table": "google_ads__campaign_report", "column": "ctr"}, {"table": "google_ads__campaign_report", "column": "ctr"}, {"table": "google_ads__campaign_report", "column": "ctr"}, {"table": "google_ads__campaign_report", "column": "ctr"}, {"table": "google_ads__campaign_report", "column": "cpc"}, {"table": "google_ads__campaign_report", "column": "cpc"}, {"table": "google_ads__campaign_report", "column": "cpc"}, {"table": "google_ads__campaign_report", "column": "cpc"}, {"table": "google_ads__campaign_report", "column": "conversions"}, {"table": "google_ads__campaign_report", "column": "conversions"}, {"table": "google_ads__campaign_report", "column": "conversions"}, {"table": "google_ads__campaign_report", "column": "conversions"}, {"table": "google_ads__campaign_report", "column": "quality_score"}, {"table": "google_ads__campaign_report", "column": "quality_score"}, {"table": "google_ads__campaign_report", "column": "quality_score"}, {"table": "google_ads__campaign_report", "column": "quality_score"}, {"table": "google_ads__campaign_report", "column": "impression_share"}, {"table": "google_ads__campaign_report", "column": "impression_share"}, {"table": "google_ads__campaign_report", "column": "impression_share"}, {"table": "google_ads__campaign_report", "column": "impression_share"}, {"table": "google_ads__campaign_report", "column": "roas"}, {"table": "google_ads__campaign_report", "column": "roas"}, {"table": "google_ads__campaign_report", "column": "roas"}, {"table": "google_ads__campaign_report", "column": "roas"}, {"table": "google_ads__campaign_report", "column": "cost_per_conversion"}, {"table": "google_ads__campaign_report", "column": "cost_per_conversion"}, {"table": "google_ads__campaign_report", "column": "cost_per_conversion"}, {"table": "google_ads__campaign_report", "column": "cost_per_conversion"}, {"table": "google_ads__campaign_report", "column": "conversion_rate"}, {"table": "google_ads__campaign_report", "column": "conversion_rate"}, {"table": "google_ads__campaign_report", "column": "conversion_rate"}, {"table": "google_ads__campaign_report", "column": "conversion_rate"}, {"table": "google_ads__campaign_report", "column": "conversion_value"}, {"table": "google_ads__campaign_report", "column": "conversions"}, {"table": "google_ads__campaign_report", "column": "conversion_value"}, {"table": "google_ads__campaign_report", "column": "conversion_value"}, {"table": "google_ads__campaign_report", "column": "conversion_value"}, {"table": "google_ads__campaign_report", "column": "conversions"}, {"table": "google_ads__campaign_report", "column": "conversions"}, {"table": "google_ads__campaign_report", "column": "conversions"}] | [] | False |

