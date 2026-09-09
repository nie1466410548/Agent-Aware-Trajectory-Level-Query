# dacomp-059

In a recent analysis of ad performance, an anomaly was discovered where some ad groups exh…

运行：已提交。官方未评分。全部 SQL 尝试/成功 58/58；数据 SQL 56/56；Python 16 次。

完整原题：

In a recent analysis of ad performance, an anomaly was discovered where some ad groups exhibit a high click-through rate (CTR) but a low conversion rate. This suggests a potential mismatch between user search intent and ad content. Using the criteria of a CTR greater than the 75th percentile and a conversion rate less than the 25th percentile to identify problem ad groups, please conduct an in-depth analysis of the characteristic patterns of these high-CTR, low-conversion ad groups. Your analysis should incorporate multiple dimensions, including basic ad group data, keyword match types, audience targeting attributes, device distribution, time-of-day performance, geographical distribution, landing page quality scores, and bidding strategy. You are required to calculate an Intent Match Index (actual conversion rate / expected conversion rate for the same industry and keyword) and a Traffic Quality Score. Based on your findings, identify the root causes and propose a systematic solution that includes keyword optimization, audience segmentation, landing page improvements, bid adjustments, and time-of-day optimizations.

| 表 | 行数 | 列数 |
| --- | --- | --- |
| google_ads__ad_group_report | 10000 | 17 |
| google_ads__keyword_report | 10000 | 20 |


实际路线（分析者依据 SQL/源码概括，不代表 Agent 自述）：SQL 提取异常广告组及关键词 → Python 构建行业基准、意图匹配和流量评分 → 分时段与渠道诊断。

数据库大小：5,156,864 字节。

## 数据 SQL

| SQL | 状态 | 基础表 | Join 输入/类型 | GROUP BY | 聚合表达式 | 结果行数 | 数据库 ms |
| --- | --- | --- | --- | --- | --- | --- | --- |
| [S3/Q1](#s3) | success | ["google_ads__ad_group_report"] | 0 / {} | [] | [] | 5 | 0.394 |
| [S4/Q2](#s4) | success | ["google_ads__keyword_report"] | 0 / {} | [] | [] | 5 | 0.38 |
| [S5/Q3](#s5) | success | ["google_ads__ad_group_report"] | 0 / {} | [] | ["COUNT(*)", "COUNT(DISTINCT ad_group_id)", "COUNT(DISTINCT campaign_id)", "COUNT(DISTINCT account_id)", "MIN(date_day)", "MAX(date_day)"] | 1 | 14.891 |
| [S6/Q4](#s6) | success | ["google_ads__keyword_report"] | 0 / {} | [] | ["COUNT(*)", "COUNT(DISTINCT ad_group_id)", "COUNT(DISTINCT criterion_id)"] | 1 | 13.571 |
| [S7/Q5](#s7) | success | ["google_ads__ad_group_report"] | 0 / {} | ["campaign_name"] | ["COUNT(*)", "SUM(clicks)", "SUM(impressions)", "SUM(conversions)", "SUM(spend)"] | 100 | 8.567 |
| [S8/Q6](#s8) | success | ["google_ads__ad_group_report"] | 0 / {} | ["ad_group_name"] | ["COUNT(*)"] | 1 | 3.452 |
| [S9/Q7](#s9) | success | ["google_ads__ad_group_report"] | 0 / {} | ["ad_group_type", "status"] | ["COUNT(*)"] | 3 | 6.802 |
| [S10/Q8](#s10) | success | ["google_ads__keyword_report"] | 0 / {} | [] | [] | 4 | 2.59 |
| [S11/Q9](#s11) | success | ["google_ads__ad_group_report"] | 0 / {} | ["account_name"] | ["COUNT(*)"] | 50 | 4.558 |
| [S12/Q10](#s12) | success | ["google_ads__ad_group_report"] | 0 / {} | ["campaign_name"] | [] | 200 | 4.643 |
| [S13/Q11](#s13) | success | ["google_ads__ad_group_report"] | 0 / {} | ["account_name"] | ["COUNT(DISTINCT account_id)"] | 94 | 5.615 |
| [S14/Q12](#s14) | success | ["google_ads__ad_group_report"] | 0 / {} | ["campaign_name"] | ["COUNT(*)"] | 200 | 5.182 |
| [S15/Q13](#s15) | success | ["google_ads__keyword_report"] | 0 / {} | ["keyword_text", "keyword_match_type"] | ["COUNT(*)", "SUM(clicks)", "SUM(conversions)", "SUM(impressions)"] | 100 | 12.833 |
| [S16/Q14](#s16) | success | ["google_ads__ad_group_report"] | 0 / {} | [] | ["COUNT(*)", "COUNT(DISTINCT ad_group_id \|\| '\|' \|\| date_day)"] | 1 | 11.78 |
| [S17/Q15](#s17) | success | ["google_ads__ad_group_report"] | 0 / {} | ["SUBSTRING(campaign_name, 1, INSTR(campaign_name, ' -') - 1)"] | ["COUNT(*)"] | 25 | 6.207 |
| [S18/Q16](#s18) | success | ["google_ads__ad_group_report"] | 0 / {} | ["currency_code"] | ["COUNT(*)"] | 10 | 4.138 |
| [S19/Q17](#s19) | success | ["google_ads__ad_group_report"] | 0 / {} | ["campaign_type"] | ["COUNT(*)"] | 25 | 6.371 |
| [S20/Q18](#s20) | success | ["google_ads__ad_group_report"] | 0 / {} | ["date_day"] | ["COUNT(*)"] | 1457 | 6.314 |
| [S21/Q19](#s21) | success | ["google_ads__ad_group_report"] | 0 / {} | [] | [] | 25 | 6.365 |
| [S22/Q20](#s22) | success | ["google_ads__ad_group_report"] | 0 / {} | [] | [] | 16 | 8.874 |
| [S23/Q21](#s23) | success | ["google_ads__ad_group_report"] | 0 / {} | [] | [] | 25 | 6.218 |
| [S24/Q22](#s24) | success | ["google_ads__keyword_report"] | 0 / {} | [] | [] | 50 | 4.59 |
| [S25/Q23](#s25) | success | ["google_ads__ad_group_report"] | 0 / {} | [] | [] | 25 | 4.488 |
| [S26/Q24](#s26) | success | ["google_ads__keyword_report"] | 0 / {} | ["keyword_text"] | [] | 100 | 4.663 |
| [S27/Q25](#s27) | success | ["google_ads__ad_group_report"] | 0 / {} | [] | ["MIN(clicks)", "MAX(clicks)", "MIN(impressions)", "MAX(impressions)", "MIN(conversions)", "MAX(conversions)", "MIN(spend)", "MAX(spend)"] | 1 | 5.018 |
| [S28/Q26](#s28) | success | ["google_ads__ad_group_report"] | 0 / {} | ["ad_group_id"] | ["COUNT(*)", "SUM(clicks)", "SUM(impressions)", "SUM(conversions)", "SUM(spend)"] | 30 | 10.596 |
| [S29/Q27](#s29) | success | ["google_ads__ad_group_report"] | 0 / {} | ["ad_group_id"] | ["SUM(clicks)", "SUM(impressions)", "SUM(conversions)", "SUM(spend)", "SUM(conversions_value)", "SUM(clicks)", "SUM(impressions)", "MIN(ctr)", "MAX(rn_ctr)", "MIN(ctr)", "MAX(rn_ctr)", "MIN(cvr)", "MAX(rn_cvr)", "MIN(cvr)", "MAX(rn_cvr)", "MIN(n)", "MAX(n)"] | 5 | 36.346 |
| [S30/Q28](#s30) | success | ["google_ads__keyword_report"] | 0 / {} | [] | ["COUNT(*)", "COUNT(DISTINCT ad_group_id \|\| '\|' \|\| criterion_id \|\| '\|' \|\| date_day)"] | 1 | 15.28 |
| [S31/Q29](#s31) | success | ["google_ads__ad_group_report"] | 2 / {'CROSS': 1} | ["ad_group_id"] | ["SUM(clicks)", "SUM(impressions)", "SUM(conversions)", "SUM(spend)", "SUM(conversions_value)", "SUM(clicks)", "SUM(impressions)"] | 1 | 36.902 |
| [S32/Q30](#s32) | success | ["google_ads__ad_group_report"] | 0 / {} | ["ad_group_id"] | ["SUM(clicks)", "SUM(impressions)", "SUM(conversions)", "SUM(spend)", "SUM(conversions_value)", "SUM(clicks)", "SUM(impressions)", "COUNT(*)", "SUM(CASE WHEN ctr > 0.035874 AND cvr < 0.038462 THEN 1 ELSE 0 END)"] | 1 | 12.009 |
| [S33/Q31](#s33) | success | ["google_ads__ad_group_report"] | 0 / {} | ["ad_group_id"] | ["SUM(clicks)", "SUM(impressions)", "SUM(conversions)", "SUM(spend)", "SUM(conversions_value)", "SUM(clicks)", "SUM(impressions)"] | 30 | 11.846 |
| [S34/Q32](#s34) | success | ["google_ads__ad_group_report"] | 0 / {} | [] | [] | 94 | 4.688 |
| [S35/Q33](#s35) | success | ["google_ads__ad_group_report"] | 0 / {} | ["r.ad_group_id", "(ctr > 0.0358744 AND cvr < 0.0384615)"] | ["SUM(r.clicks)", "SUM(r.impressions)", "SUM(r.conversions)", "SUM(r.spend)", "SUM(r.impressions)", "SUM(r.clicks)", "SUM(r.clicks)", "SUM(r.conversions)", "SUM(r.clicks)", "SUM(r.impressions)", "COUNT(*)", "SUM(clicks)", "SUM(impressions)", "SUM(conversions)", "SUM(spend)", "SUM(impressions)", "SUM(clicks)", "SUM(clicks)", "SUM(conversions)"] | 2 | 22.241 |
| [S36/Q34](#s36) | success | ["google_ads__ad_group_report"] | 0 / {} | ["r.ad_group_id", "CASE WHEN campaign_name LIKE 'Brand%' THEN 'Brand' WHEN campaign_name LIKE 'Display%' THEN 'Display' WHEN campaign_name LIKE 'Performance%' THEN 'Performance' WHEN campaign_name LIKE 'Search%' THEN 'Search' WHEN campaign_name LIKE 'Shopping%' THEN 'Shopping' END", "(ctr > 0.0358744 AND cvr < 0.0384615)"] | ["SUM(r.clicks)", "SUM(r.impressions)", "SUM(r.conversions)", "SUM(r.spend)", "SUM(r.impressions)", "SUM(r.clicks)", "SUM(r.clicks)", "SUM(r.conversions)", "SUM(r.clicks)", "SUM(r.impressions)", "COUNT(*)", "SUM(spend)", "SUM(impressions)", "SUM(clicks)", "SUM(clicks)", "SUM(conversions)"] | 10 | 18.262 |
| [S37/Q35](#s37) | success | ["google_ads__ad_group_report"] | 0 / {} | ["r.ad_group_id", "(ctr > 0.03587443946188341 AND cvr < 0.038461538461538464)"] | ["SUM(r.clicks)", "SUM(r.impressions)", "SUM(r.conversions)", "SUM(r.spend)", "SUM(r.impressions)", "SUM(r.clicks)", "SUM(r.clicks)", "SUM(r.conversions)", "SUM(r.clicks)", "SUM(r.impressions)", "COUNT(*)", "SUM(clicks)", "SUM(spend)", "SUM(impressions)", "SUM(clicks)", "SUM(clicks)", "SUM(conversions)"] | 2 | 14.126 |
| [S38/Q36](#s38) | success | ["google_ads__ad_group_report"] | 0 / {} | ["r.ad_group_id", "period"] | ["SUM(r.clicks)", "SUM(r.impressions)", "SUM(r.conversions)", "SUM(r.spend)", "SUM(r.impressions)", "SUM(r.clicks)", "SUM(r.clicks)", "SUM(r.conversions)", "SUM(r.clicks)", "SUM(r.impressions)", "SUM(CASE WHEN (ctr > 0.03587443946188341 AND cvr < 0.038461538461538464) THEN 1 ELSE 0 END)", "SUM(CASE WHEN NOT (ctr > 0.03587443946188341 AND cvr < 0.038461538461538464) THEN 1 ELSE 0 END)", "COUNT(*)", "SUM(CASE WHEN (ctr > 0.03587443946188341 AND cvr < 0.038461538461538464) THEN 1 ELSE 0 END)"] | 16 | 16.838 |
| [S39/Q37](#s39) | success | ["google_ads__ad_group_report"] | 0 / {} | ["r.ad_group_id", "strategy"] | ["SUM(r.clicks)", "SUM(r.impressions)", "SUM(r.conversions)", "SUM(r.spend)", "SUM(r.impressions)", "SUM(r.clicks)", "SUM(r.clicks)", "SUM(r.conversions)", "SUM(r.clicks)", "SUM(r.impressions)", "SUM(CASE WHEN (ctr > 0.03587443946188341 AND cvr < 0.038461538461538464) THEN 1 ELSE 0 END)", "SUM(CASE WHEN NOT (ctr > 0.03587443946188341 AND cvr < 0.038461538461538464) THEN 1 ELSE 0 END)", "COUNT(*)", "SUM(clicks)", "SUM(spend)", "SUM(CASE WHEN (ctr > 0.03587443946188341 AND cvr < 0.038461538461538464) THEN 1 ELSE 0 END)", "SUM(CASE WHEN (ctr > 0.03587443946188341 AND cvr < 0.038461538461538464) THEN clicks ELSE 0 END)", "SUM(CASE WHEN (ctr > 0.03587443946188341 AND cvr < 0.038461538461538464) THEN spend ELSE 0 END)"] | 5 | 18.909 |
| [S40/Q38](#s40) | success | ["google_ads__ad_group_report", "google_ads__keyword_report"] | 2 / {'INNER': 1} | ["ad_group_id", "keyword_match_type", "ad_group_id", "k.keyword_match_type", "f.is_problem"] | ["SUM(clicks)", "SUM(impressions)", "SUM(conversions)", "SUM(spend)", "SUM(clicks)", "SUM(impressions)", "SUM(conversions)", "SUM(clicks)", "SUM(impressions)", "COUNT(DISTINCT f.ad_group_id)", "SUM(k.clicks)", "SUM(k.conv)", "SUM(k.spend)", "SUM(k.clicks)", "SUM(k.conv)"] | 8 | 39.26 |
| [S41/Q39](#s41) | success | ["google_ads__ad_group_report"] | 0 / {} | ["r.ad_group_id", "industry"] | ["SUM(r.clicks)", "SUM(r.impressions)", "SUM(r.conversions)", "SUM(r.spend)", "SUM(r.impressions)", "SUM(r.clicks)", "SUM(r.clicks)", "SUM(r.conversions)", "SUM(r.clicks)", "SUM(r.impressions)", "COUNT(*)", "SUM(CASE WHEN (ctr > 0.03587443946188341 AND cvr < 0.038461538461538464) THEN 1 ELSE 0 END)", "COUNT(*)", "SUM(clicks)", "SUM(spend)", "SUM(CASE WHEN (ctr > 0.03587443946188341 AND cvr < 0.038461538461538464) THEN 1 ELSE 0 END)", "SUM(CASE WHEN (ctr > 0.03587443946188341 AND cvr < 0.038461538461538464) THEN clicks ELSE 0 END)", "SUM(CASE WHEN (ctr > 0.03587443946188341 AND cvr < 0.038461538461538464) THEN spend ELSE 0 END)"] | 12 | 27.264 |
| [S42/Q40](#s42) | success | ["google_ads__ad_group_report"] | 0 / {} | ["r.ad_group_id", "status"] | ["SUM(r.clicks)", "SUM(r.impressions)", "SUM(r.conversions)", "SUM(r.spend)", "SUM(r.impressions)", "SUM(r.clicks)", "SUM(r.clicks)", "SUM(r.conversions)", "SUM(r.clicks)", "SUM(r.impressions)", "SUM(CASE WHEN (ctr > 0.03587443946188341 AND cvr < 0.038461538461538464) THEN 1 ELSE 0 END)", "SUM(CASE WHEN NOT (ctr > 0.03587443946188341 AND cvr < 0.038461538461538464) THEN 1 ELSE 0 END)", "COUNT(*)", "SUM(CASE WHEN (ctr > 0.03587443946188341 AND cvr < 0.038461538461538464) THEN 1 ELSE 0 END)"] | 3 | 13.969 |
| [S43/Q41](#s43) | success | ["google_ads__ad_group_report", "google_ads__keyword_report"] | 0 / {} | [] | ["SUM(clicks)", "SUM(clicks)", "SUM(impressions)", "SUM(impressions)", "SUM(conversions)", "SUM(conversions)"] | 1 | 9.018 |
| [S44/Q42](#s44) | success | ["google_ads__ad_group_report", "google_ads__keyword_report"] | 2 / {'INNER': 1} | ["ad_group_id", "f.is_problem", "k.keyword_match_type"] | ["SUM(clicks)", "SUM(impressions)", "SUM(impressions)", "SUM(clicks)", "SUM(clicks)", "SUM(conversions)", "COUNT(*)", "SUM(k.clicks)", "SUM(k.impressions)", "SUM(k.conversions)", "SUM(k.spend)"] | 8 | 30.794 |
| [S45/Q43](#s45) | success | ["google_ads__keyword_report"] | 0 / {} | ["keyword_text"] | [] | 100 | 4.895 |
| [S46/Q44](#s46) | success | ["google_ads__keyword_report"] | 0 / {} | [] | [] | 200 | 4.731 |
| [S47/Q45](#s47) | success | ["google_ads__keyword_report"] | 0 / {} | [] | [] | 32 | 3.299 |
| [S48/Q46](#s48) | success | ["google_ads__keyword_report"] | 0 / {} | [] | ["COUNT(DISTINCT keyword_text)", "COUNT(*)"] | 1 | 7.693 |
| [S49/Q47](#s49) | success | ["google_ads__ad_group_report"] | 0 / {} | ["r.ad_group_id"] | ["SUM(r.clicks)", "SUM(r.impressions)", "SUM(r.conversions)", "SUM(r.spend)", "SUM(r.impressions)", "SUM(r.clicks)", "SUM(r.clicks)", "SUM(r.conversions)", "SUM(r.clicks)", "SUM(r.impressions)"] | 4324 | 42.335 |
| [S50/Q48](#s50) | success | ["google_ads__ad_group_report"] | 0 / {} | ["ad_group_id"] | ["SUM(clicks)"] | 3 | 4.589 |
| [S51/Q49](#s51) | success | ["google_ads__ad_group_report"] | 0 / {} | ["r.ad_group_id"] | ["SUM(r.clicks)", "SUM(r.impressions)", "SUM(r.conversions)", "SUM(r.spend)", "SUM(r.impressions)", "SUM(r.clicks)", "SUM(r.clicks)", "SUM(r.conversions)", "SUM(r.clicks)", "SUM(r.impressions)"] | 4324 | 41.974 |
| [S52/Q50](#s52) | success | ["google_ads__keyword_report"] | 0 / {} | [] | [] | 10000 | 16.084 |
| [S53/Q51](#s53) | success | ["google_ads__ad_group_report"] | 0 / {} | ["r.ad_group_id"] | ["SUM(r.clicks)", "SUM(r.impressions)", "SUM(r.conversions)", "SUM(r.spend)", "SUM(r.impressions)", "SUM(r.clicks)", "SUM(r.clicks)", "SUM(r.conversions)", "SUM(r.clicks)", "SUM(r.impressions)"] | 4324 | 41.537 |
| [S54/Q52](#s54) | success | ["google_ads__keyword_report"] | 0 / {} | [] | [] | 10000 | 16.082 |
| [S55/Q53](#s55) | success | ["google_ads__ad_group_report"] | 0 / {} | ["r.ad_group_id"] | ["SUM(r.clicks)", "SUM(r.impressions)", "SUM(r.conversions)", "SUM(r.spend)", "SUM(r.impressions)", "SUM(r.clicks)", "SUM(r.clicks)", "SUM(r.conversions)", "SUM(r.clicks)", "SUM(r.impressions)"] | 4324 | 44.136 |
| [S56/Q54](#s56) | success | ["google_ads__keyword_report"] | 0 / {} | [] | [] | 10000 | 16.013 |
| [S57/Q55](#s57) | success | ["google_ads__ad_group_report"] | 0 / {} | ["ad_group_id"] | ["SUM(conversions_value)", "SUM(conversions)", "SUM(clicks)", "SUM(impressions)"] | 4324 | 14.07 |
| [S58/Q56](#s58) | success | ["google_ads__ad_group_report"] | 0 / {} | ["ad_group_id"] | ["SUM(conversions_value)"] | 4324 | 10.925 |


## 元数据和设置

| SQL | 类别 | 状态 | 内容 |
| --- | --- | --- | --- |
| S1 | connection_setup | success | PRAGMA query_only=ON |
| S2 | metadata | success | SELECT name,sql FROM sqlite_master WHERE type='table' ORDER BY name |


## Python 与执行位置

人工源码审查：**database_first_violation**。Python 连接广告组、关键词和行业基准，对匹配类型、时段及渠道策略分组计数，计算加权预期转化率及流量评分。这些关系运算、聚合和常规评分可由 SQL 完成。文本拆词、检验与图形渲染另行评价，不作为全部迁出计算的理由。 [证据](../reviews/dacomp-059.json)。

P1：Complex multi-step computation: keyword tokenization, industry-keyword benchmark CVRs per ad group, Intent Match Index calculation, and Traffic Quality Score composite. These involve string parsing, cross-referencing, and weighted indexing that is more manageable in Python than SQL.

[源码](../../../runs/dsv4flash-db-first-full-01/dacomp-059/attempt-01/python/P1.py)；[输出](../../../runs/dsv4flash-db-first-full-01/dacomp-059/attempt-01/python/P1.stdout)；[错误](../../../runs/dsv4flash-db-first-full-01/dacomp-059/attempt-01/python/P1.stderr)。检出需人工核验的 SQL 可实现操作：.merge(, .query(；不能仅凭理由判为合规。

P2：Debugging the structure of the rows returned by db.rows to correctly parse query results in pandas.

[源码](../../../runs/dsv4flash-db-first-full-01/dacomp-059/attempt-01/python/P2.py)；[输出](../../../runs/dsv4flash-db-first-full-01/dacomp-059/attempt-01/python/P2.stdout)；[错误](../../../runs/dsv4flash-db-first-full-01/dacomp-059/attempt-01/python/P2.stderr)。检出需人工核验的 SQL 可实现操作：.query(；不能仅凭理由判为合规。

P3：Fixing the data retrieval approach using query_to_df helper that properly handles db.rows output format.

[源码](../../../runs/dsv4flash-db-first-full-01/dacomp-059/attempt-01/python/P3.py)；[输出](../../../runs/dsv4flash-db-first-full-01/dacomp-059/attempt-01/python/P3.stdout)；[错误](../../../runs/dsv4flash-db-first-full-01/dacomp-059/attempt-01/python/P3.stderr)。检出需人工核验的 SQL 可实现操作：.merge(, .query(；不能仅凭理由判为合规。

P4：Loading full datasets from the result archives using db.rows which returns complete results, not truncated previews.

[源码](../../../runs/dsv4flash-db-first-full-01/dacomp-059/attempt-01/python/P4.py)；[输出](../../../runs/dsv4flash-db-first-full-01/dacomp-059/attempt-01/python/P4.stdout)；[错误](../../../runs/dsv4flash-db-first-full-01/dacomp-059/attempt-01/python/P4.stderr)。检出需人工核验的 SQL 可实现操作：.merge(, .query(；不能仅凭理由判为合规。

P5：Reloading datasets with is_problem as integer type to avoid merge type issues.

[源码](../../../runs/dsv4flash-db-first-full-01/dacomp-059/attempt-01/python/P5.py)；[输出](../../../runs/dsv4flash-db-first-full-01/dacomp-059/attempt-01/python/P5.stdout)；[错误](../../../runs/dsv4flash-db-first-full-01/dacomp-059/attempt-01/python/P5.stderr)。检出需人工核验的 SQL 可实现操作：.merge(, .query(；不能仅凭理由判为合规。

P6：Keyword tokenization and intent classification require string parsing and per-word aggregation across groups, done in Python because SQLite lacks tokenization.

[源码](../../../runs/dsv4flash-db-first-full-01/dacomp-059/attempt-01/python/P6.py)；[输出](../../../runs/dsv4flash-db-first-full-01/dacomp-059/attempt-01/python/P6.stdout)；[错误](../../../runs/dsv4flash-db-first-full-01/dacomp-059/attempt-01/python/P6.stderr)。检出需人工核验的 SQL 可实现操作：sort_values(；不能仅凭理由判为合规。

P7：Intent Match Index requires leave-one-out benchmark computation (expected conversion rate per industry-keyword pair), which needs iterative per-ad-group weighted averaging better handled in Python.

[源码](../../../runs/dsv4flash-db-first-full-01/dacomp-059/attempt-01/python/P7.py)；[输出](../../../runs/dsv4flash-db-first-full-01/dacomp-059/attempt-01/python/P7.stdout)；[错误](../../../runs/dsv4flash-db-first-full-01/dacomp-059/attempt-01/python/P7.stderr)。检出需人工核验的 SQL 可实现操作：groupby(, .merge(；不能仅凭理由判为合规。

P8：Rerunning IMI calculation without leave-one-out to get wider coverage, since many ad groups have unique keyword combinations in their industry.

[源码](../../../runs/dsv4flash-db-first-full-01/dacomp-059/attempt-01/python/P8.py)；[输出](../../../runs/dsv4flash-db-first-full-01/dacomp-059/attempt-01/python/P8.stdout)；[错误](../../../runs/dsv4flash-db-first-full-01/dacomp-059/attempt-01/python/P8.stderr)。检出需人工核验的 SQL 可实现操作：groupby(, .merge(；不能仅凭理由判为合规。

P9：Traffic Quality Score is a weighted composite requiring per-ad-group keyword tokenization and match-type scoring, best computed in Python.

[源码](../../../runs/dsv4flash-db-first-full-01/dacomp-059/attempt-01/python/P9.py)；[输出](../../../runs/dsv4flash-db-first-full-01/dacomp-059/attempt-01/python/P9.stdout)；[错误](../../../runs/dsv4flash-db-first-full-01/dacomp-059/attempt-01/python/P9.stderr)。检出需人工核验的 SQL 可实现操作：groupby(, .merge(；不能仅凭理由判为合规。

P10：Economic metrics and non-parametric statistical tests plus cross-tabulations involve computations best handled in Python with scipy.

[源码](../../../runs/dsv4flash-db-first-full-01/dacomp-059/attempt-01/python/P10.py)；[输出](../../../runs/dsv4flash-db-first-full-01/dacomp-059/attempt-01/python/P10.stdout)；[错误](../../../runs/dsv4flash-db-first-full-01/dacomp-059/attempt-01/python/P10.stderr)。检出需人工核验的 SQL 可实现操作：groupby(, .merge(, sort_values(；不能仅凭理由判为合规。

P11：Need conversions_value from original table for economic metrics, plus statistical tests via scipy.

[源码](../../../runs/dsv4flash-db-first-full-01/dacomp-059/attempt-01/python/P11.py)；[输出](../../../runs/dsv4flash-db-first-full-01/dacomp-059/attempt-01/python/P11.stdout)；[错误](../../../runs/dsv4flash-db-first-full-01/dacomp-059/attempt-01/python/P11.stderr)。检出需人工核验的 SQL 可实现操作：groupby(, .merge(, .query(, sort_values(；不能仅凭理由判为合规。

P12：Seasonality and top-problem-group profiling using pandas aggregation on the computed dataset.

[源码](../../../runs/dsv4flash-db-first-full-01/dacomp-059/attempt-01/python/P12.py)；[输出](../../../runs/dsv4flash-db-first-full-01/dacomp-059/attempt-01/python/P12.stdout)；[错误](../../../runs/dsv4flash-db-first-full-01/dacomp-059/attempt-01/python/P12.stderr)。检出需人工核验的 SQL 可实现操作：groupby(, sort_values(；不能仅凭理由判为合规。

P13：Creating report visualizations from the computed ad group dataset using matplotlib/seaborn.

[源码](../../../runs/dsv4flash-db-first-full-01/dacomp-059/attempt-01/python/P13.py)；[输出](../../../runs/dsv4flash-db-first-full-01/dacomp-059/attempt-01/python/P13.stdout)；[错误](../../../runs/dsv4flash-db-first-full-01/dacomp-059/attempt-01/python/P13.stderr)。检出需人工核验的 SQL 可实现操作：groupby(, sort_values(；不能仅凭理由判为合规。

P14：Creating keyword word-lift and economics comparison figures for the report.

[源码](../../../runs/dsv4flash-db-first-full-01/dacomp-059/attempt-01/python/P14.py)；[输出](../../../runs/dsv4flash-db-first-full-01/dacomp-059/attempt-01/python/P14.stdout)；[错误](../../../runs/dsv4flash-db-first-full-01/dacomp-059/attempt-01/python/P14.stderr)。检出需人工核验的 SQL 可实现操作：.merge(, .query(, sort_values(；不能仅凭理由判为合规。

P15：Fixing figure generation: word lift chart and economics chart with robust column handling.

[源码](../../../runs/dsv4flash-db-first-full-01/dacomp-059/attempt-01/python/P15.py)；[输出](../../../runs/dsv4flash-db-first-full-01/dacomp-059/attempt-01/python/P15.stdout)；[错误](../../../runs/dsv4flash-db-first-full-01/dacomp-059/attempt-01/python/P15.stderr)。检出需人工核验的 SQL 可实现操作：.merge(, .query(, sort_values(；不能仅凭理由判为合规。

P16：Analyzing keyword match type distribution differences between problem and non-problem groups for the report.

[源码](../../../runs/dsv4flash-db-first-full-01/dacomp-059/attempt-01/python/P16.py)；[输出](../../../runs/dsv4flash-db-first-full-01/dacomp-059/attempt-01/python/P16.stdout)；[错误](../../../runs/dsv4flash-db-first-full-01/dacomp-059/attempt-01/python/P16.stderr)。检出需人工核验的 SQL 可实现操作：groupby(；不能仅凭理由判为合规。

## 优化机会

已验证候选。筛选限于精确 SQL、相同自包含 CTE、相同单表完整过滤、可分解单表聚合；未覆盖任意 Join 等价和一般谓词蕴含。全部候选都是 offline，未测在线预测。

| 候选 | 类型 | 已有结果 | 覆盖 SQL | 后续次数 | 中间行数 | 验证 | 成本 |
| --- | --- | --- | --- | --- | --- | --- | --- |
| C1 | exact-result reuse | True | ["S21", "S23"] | 1 | unknown | not_verified_cap | Not tested |
| C2 | exact-result reuse | True | ["S49", "S51", "S53", "S55"] | 3 | 4324 | verified | Not benchmarked; correctness alone does not establish net speedup. |
| C3 | exact-result reuse | True | ["S52", "S54", "S56"] | 2 | unknown | not_verified_cap | Not tested |
| C4 | common subexpression | False | ["S29", "S31", "S32", "S33"] | 3 | unknown | not_verified_cap | Not tested |
| C5 | common subexpression | False | ["S36", "S37"] | 1 | unknown | not_verified_cap | Not tested |
| C6 | common subexpression | False | ["S49", "S51", "S53", "S55"] | 3 | 4324 | verified | Not benchmarked; correctness alone does not establish net speedup. |
| C7 | aggregate MV | False | ["S7", "S8", "S9", "S11", "S14", "S17", "S18", "S20", "S27", "S50", "S57", "S58"] | 11 | 10000 | rejected_result_mismatch | Not benchmarked; correctness alone does not establish net speedup. |


已验证覆盖（含触发查询、候选并集去重）：4/56 条成功数据 SQL。正确性仅针对当前数据库快照；未测性能的候选不能声称已加速。

[完整 build/rewrite 与比较证据](dacomp-059.analysis.json)。

### C2：exact-result reuse

Identical normalized SQL and parameters; archive equality checked.

原查询 [S49](#s49), [S51](#s51), [S53](#s53), [S55](#s55) → 保留前序结果 S49 → 后续 3 次可复用。该构建点为事后假设，不代表 Agent 当时预知后续。

| 原 SQL | 列名一致 | 结果一致 | 比较方法 |
| --- | --- | --- | --- |
| S51 | True | True | exact_multiset |
| S53 | True | True | exact_multiset |
| S55 | True | True | exact_multiset |


验证状态：verified；成本结论：Not benchmarked; correctness alone does not establish net speedup.

### C6：common subexpression

Identical self-contained CTE body across queries.

原查询 [S49](#s49), [S51](#s51), [S53](#s53), [S55](#s55) → 新增共享状态 C6 → 后续 3 次可复用。该构建点为事后假设，不代表 Agent 当时预知后续。

构建定义：

```sql
SELECT r.ad_group_id, r.account_name, r.campaign_name, r.status, r.ad_group_type, SUM(r.clicks) AS clicks, SUM(r.impressions) AS impressions, SUM(r.conversions) AS conversions, SUM(r.spend) AS spend, SUM(r.clicks) * 1.0 / SUM(r.impressions) AS ctr, SUM(r.conversions) * 1.0 / SUM(r.clicks) AS cvr, CASE WHEN r.account_name LIKE '%Automotive%' THEN 'Automotive' WHEN r.account_name LIKE '%Education%' THEN 'Education' WHEN r.account_name LIKE '%Entertainment%' THEN 'Entertainment' WHEN r.account_name LIKE '%Fashion%' THEN 'Fashion' WHEN r.account_name LIKE '%Finance%' THEN 'Finance' WHEN r.account_name LIKE '%Food%' THEN 'Food' WHEN r.account_name LIKE '%Healthcare%' THEN 'Healthcare' WHEN r.account_name LIKE '%Real Estate%' THEN 'Real Estate' WHEN r.account_name LIKE '%Retail%' THEN 'Retail' WHEN r.account_name LIKE '%Sports%' THEN 'Sports' WHEN r.account_name LIKE '%Technology%' THEN 'Technology' WHEN r.account_name LIKE '%Travel%' THEN 'Travel' ELSE 'Other' END AS industry, CASE WHEN r.campaign_name LIKE 'Brand%' THEN 'Brand' WHEN r.campaign_name LIKE 'Display%' THEN 'Display' WHEN r.campaign_name LIKE 'Performance%' THEN 'Performance' WHEN r.campaign_name LIKE 'Search%' THEN 'Search' WHEN r.campaign_name LIKE 'Shopping%' THEN 'Shopping' END AS channel, CASE WHEN r.campaign_name LIKE '% Audience%' THEN 'Audience' WHEN r.campaign_name LIKE '% Broad%' THEN 'Broad' WHEN r.campaign_name LIKE '% Exact%' THEN 'Exact' WHEN r.campaign_name LIKE '% Keywords%' THEN 'Keywords' WHEN r.campaign_name LIKE '% Remarketing%' THEN 'Remarketing' END AS strategy, LTRIM(SUBSTRING(r.campaign_name, INSTR(r.campaign_name, ' -') + 2)) AS period FROM google_ads__ad_group_report AS r GROUP BY r.ad_group_id HAVING SUM(r.clicks) > 0 AND SUM(r.impressions) > 0
```

受益查询 S49 的改写示例：

```sql
WITH agg AS (SELECT * FROM temp.reuse_candidate) SELECT * FROM agg
```

| 原 SQL | 列名一致 | 结果一致 | 比较方法 |
| --- | --- | --- | --- |
| S49 | True | True | exact_multiset |
| S51 | True | True | exact_multiset |
| S53 | True | True | exact_multiset |
| S55 | True | True | exact_multiset |


验证状态：verified；成本结论：Not benchmarked; correctness alone does not establish net speedup.

### C7：aggregate MV

Union of grouping keys; decomposable aggregate states; AVG uses SUM and non-NULL COUNT.

原查询 [S7](#s7), [S8](#s8), [S9](#s9), [S11](#s11), [S14](#s14), [S17](#s17), [S18](#s18), [S20](#s20), [S27](#s27), [S50](#s50), [S57](#s57), [S58](#s58) → 新增共享状态 C7 → 后续 11 次可复用。该构建点为事后假设，不代表 Agent 当时预知后续。

构建定义：

```sql
SELECT campaign_name AS __g0, ad_group_name AS __g1, ad_group_type AS __g2, status AS __g3, account_name AS __g4, SUBSTRING(campaign_name, 1, INSTR(campaign_name, ' -') - 1) AS __g5, currency_code AS __g6, date_day AS __g7, ad_group_id AS __g8, COUNT(*) AS __a0, SUM(clicks) AS __a1, SUM(impressions) AS __a2, SUM(conversions) AS __a3, SUM(spend) AS __a4, MIN(clicks) AS __a5, MAX(clicks) AS __a6, MIN(impressions) AS __a7, MAX(impressions) AS __a8, MIN(conversions) AS __a9, MAX(conversions) AS __a10, MIN(spend) AS __a11, MAX(spend) AS __a12, SUM(conversions_value) AS __a13 FROM "google_ads__ad_group_report"  GROUP BY campaign_name, ad_group_name, ad_group_type, status, account_name, SUBSTRING(campaign_name, 1, INSTR(campaign_name, ' -') - 1), currency_code, date_day, ad_group_id
```

受益查询 S7 的改写示例：

```sql
SELECT __g0 AS "campaign_name", SUM(__a0) AS cnt, SUM(__a1) AS clicks, SUM(__a2) AS imp, SUM(__a3) AS conv, SUM(__a4) AS spend FROM temp.reuse_candidate GROUP BY __g0 ORDER BY cnt DESC LIMIT 100
```

| 原 SQL | 列名一致 | 结果一致 | 比较方法 |
| --- | --- | --- | --- |
| S7 | True | True | ordered_numeric_tolerance |
| S8 | True | True | ordered_numeric_tolerance |
| S9 | True | True | ordered_numeric_tolerance |
| S11 | True | True | ordered_numeric_tolerance |
| S14 | True | True | ordered_numeric_tolerance |
| S17 | True | True | ordered_numeric_tolerance |
| S18 | True | True | ordered_numeric_tolerance |
| S20 | True | True | ordered_numeric_tolerance |
| S27 | True | True | exact_multiset |
| S50 | True | True | exact_multiset |
| S57 | True | False | exact_multiset |
| S58 | True | False | exact_multiset |


验证状态：rejected_result_mismatch；成本结论：Not benchmarked; correctness alone does not establish net speedup.

结果依赖：自动记录 SQL→Python 的接口父调用，以及源码中引用归档文件的消费者；字面值相同不认定因果。模型方向选择需要人工读取消息，尚未做全面因果标注。

[原始报告](../../../runs/dsv4flash-db-first-full-01/dacomp-059/attempt-01/answer.md)；[统一消息](../../../runs/dsv4flash-db-first-full-01/dacomp-059/attempt-01/messages.jsonl)；[原始 OpenCode 事件](../../../runs/dsv4flash-db-first-full-01/dacomp-059/attempt-01/opencode.jsonl)；[SQL 引擎日志](../../../runs/dsv4flash-db-first-full-01/dacomp-059/attempt-01/sql_journal.jsonl)。

[可读报告（本地图片链接规范化）](../answers/dacomp-059.md)。原始回答保留，分析结论未改写。

## S1

类别 `connection_setup`；来源 `connection`；调用 `ae3b60e5cc1a49eaae96f375c39cdb93`；状态 `success`。

```sql
PRAGMA query_only=ON
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-059/attempt-01/sql/S1.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-059/attempt-01/sql/S1.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-059/attempt-01/results/S1.rows.jsonl)；完整：True；SHA256：`e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`。

## S2

类别 `metadata`；来源 `list_db`；调用 `ae3b60e5cc1a49eaae96f375c39cdb93`；状态 `success`。

```sql
SELECT name,sql FROM sqlite_master WHERE type='table' ORDER BY name
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-059/attempt-01/sql/S2.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-059/attempt-01/sql/S2.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-059/attempt-01/results/S2.rows.jsonl)；完整：True；SHA256：`0d6cc26a005e41fab9bfd8d92b5ac31f46393ae38f66092152f26017e984332a`。

## S3

类别 `data`；来源 `query_db`；调用 `19a67cc5e0b94d7e8ae33df1036e7a91`；状态 `success`。

```sql
SELECT * FROM google_ads__ad_group_report LIMIT 5
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-059/attempt-01/sql/S3.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-059/attempt-01/sql/S3.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-059/attempt-01/results/S3.rows.jsonl)；完整：True；SHA256：`8c39b2890f974fb40edbcbb48fade770911ae60def2bc76dd46ee680ace689ce`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "google_ads__ad_group_report", "kind": "base", "block": null, "base_tables": ["google_ads__ad_group_report"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |


## S4

类别 `data`；来源 `query_db`；调用 `5d43e3c9d2694f5c91ca44490a6a1f35`；状态 `success`。

```sql
SELECT * FROM google_ads__keyword_report LIMIT 5
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-059/attempt-01/sql/S4.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-059/attempt-01/sql/S4.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-059/attempt-01/results/S4.rows.jsonl)；完整：True；SHA256：`7f5b34ccddd358d5e3a955d5d1b1841a98e853d45cd168cbce9caaeea98eef6c`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "google_ads__keyword_report", "kind": "base", "block": null, "base_tables": ["google_ads__keyword_report"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |


## S5

类别 `data`；来源 `query_db`；调用 `a1d2f2fa156d449fafe35c2d0faa93b1`；状态 `success`。

```sql
SELECT COUNT(*) AS total_rows, COUNT(DISTINCT ad_group_id) AS distinct_ad_groups, COUNT(DISTINCT campaign_id) AS distinct_campaigns, COUNT(DISTINCT account_id) AS distinct_accounts, MIN(date_day) AS min_date, MAX(date_day) AS max_date FROM google_ads__ad_group_report
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-059/attempt-01/sql/S5.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-059/attempt-01/sql/S5.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-059/attempt-01/results/S5.rows.jsonl)；完整：True；SHA256：`1d6c13cd8c58ada9f36f78be96b186b228fb30af01057490ea5248252fae3041`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "google_ads__ad_group_report", "kind": "base", "block": null, "base_tables": ["google_ads__ad_group_report"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |
| B1 | COUNT(DISTINCT ad_group_id) | [{"table": "google_ads__ad_group_report", "column": "ad_group_id"}] | [] | False |
| B1 | COUNT(DISTINCT campaign_id) | [{"table": "google_ads__ad_group_report", "column": "campaign_id"}] | [] | False |
| B1 | COUNT(DISTINCT account_id) | [{"table": "google_ads__ad_group_report", "column": "account_id"}] | [] | False |
| B1 | MIN(date_day) | [{"table": "google_ads__ad_group_report", "column": "date_day"}] | [] | False |
| B1 | MAX(date_day) | [{"table": "google_ads__ad_group_report", "column": "date_day"}] | [] | False |


## S6

类别 `data`；来源 `query_db`；调用 `35e0f0f9df0f43cc911c4b8301865dbe`；状态 `success`。

```sql
SELECT COUNT(*) AS total_rows, COUNT(DISTINCT ad_group_id) AS distinct_ad_groups, COUNT(DISTINCT criterion_id) AS distinct_keywords FROM google_ads__keyword_report
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-059/attempt-01/sql/S6.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-059/attempt-01/sql/S6.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-059/attempt-01/results/S6.rows.jsonl)；完整：True；SHA256：`93ba7d81af0354e3809dddf59229f2a4f510b9a09b6cbb6acdec550a8e86465d`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "google_ads__keyword_report", "kind": "base", "block": null, "base_tables": ["google_ads__keyword_report"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |
| B1 | COUNT(DISTINCT ad_group_id) | [{"table": "google_ads__keyword_report", "column": "ad_group_id"}] | [] | False |
| B1 | COUNT(DISTINCT criterion_id) | [{"table": "google_ads__keyword_report", "column": "criterion_id"}] | [] | False |


## S7

类别 `data`；来源 `query_db`；调用 `9401a0ba55f045058a84e80e3c255b68`；状态 `success`。

```sql
SELECT campaign_name, COUNT(*) AS cnt, SUM(clicks) AS clicks, SUM(impressions) AS imp, SUM(conversions) AS conv, SUM(spend) AS spend FROM google_ads__ad_group_report GROUP BY campaign_name ORDER BY cnt DESC LIMIT 100
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-059/attempt-01/sql/S7.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-059/attempt-01/sql/S7.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-059/attempt-01/results/S7.rows.jsonl)；完整：True；SHA256：`421094a6cff873bb8e162869a8a1830eede25a558d5e6c7529edf60cff55c3dc`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "google_ads__ad_group_report", "kind": "base", "block": null, "base_tables": ["google_ads__ad_group_report"]}] | [] | ["campaign_name"] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |
| B1 | SUM(clicks) | [{"table": "google_ads__ad_group_report", "column": "clicks"}] | [] | False |
| B1 | SUM(impressions) | [{"table": "google_ads__ad_group_report", "column": "impressions"}] | [] | False |
| B1 | SUM(conversions) | [{"table": "google_ads__ad_group_report", "column": "conversions"}] | [] | False |
| B1 | SUM(spend) | [{"table": "google_ads__ad_group_report", "column": "spend"}] | [] | False |


## S8

类别 `data`；来源 `query_db`；调用 `74cf58e82cca465ba667cfc24cdc2f43`；状态 `success`。

```sql
SELECT ad_group_name, COUNT(*) AS cnt FROM google_ads__ad_group_report GROUP BY ad_group_name ORDER BY cnt DESC LIMIT 60
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-059/attempt-01/sql/S8.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-059/attempt-01/sql/S8.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-059/attempt-01/results/S8.rows.jsonl)；完整：True；SHA256：`0f4f9fbd2b5fcc7a1abfe0ed6495d3df76e9b166a54d9d898e0fadfa1b09e3e6`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "google_ads__ad_group_report", "kind": "base", "block": null, "base_tables": ["google_ads__ad_group_report"]}] | [] | ["ad_group_name"] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |


## S9

类别 `data`；来源 `query_db`；调用 `02cf1411bb8e4b0481888feb4774fb4b`；状态 `success`。

```sql
SELECT ad_group_type, status, COUNT(*) AS cnt FROM google_ads__ad_group_report GROUP BY ad_group_type, status ORDER BY cnt DESC
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-059/attempt-01/sql/S9.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-059/attempt-01/sql/S9.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-059/attempt-01/results/S9.rows.jsonl)；完整：True；SHA256：`fd971e03b85761586a2832150fa22c3b2d4da09cd5eb9409e5b67dbd5513aae6`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "google_ads__ad_group_report", "kind": "base", "block": null, "base_tables": ["google_ads__ad_group_report"]}] | [] | ["ad_group_type", "status"] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |


## S10

类别 `data`；来源 `query_db`；调用 `3137798759ca43ad99805edfffd1254d`；状态 `success`。

```sql
SELECT DISTINCT keyword_match_type FROM google_ads__keyword_report
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-059/attempt-01/sql/S10.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-059/attempt-01/sql/S10.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-059/attempt-01/results/S10.rows.jsonl)；完整：True；SHA256：`3b9aa9d115828aeab08f4f576bb00a937d0c0d4b2e17f1e438d3b02a2dcee788`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "google_ads__keyword_report", "kind": "base", "block": null, "base_tables": ["google_ads__keyword_report"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |


## S11

类别 `data`；来源 `query_db`；调用 `acf5643bc75c49d28988bf1f8afd8303`；状态 `success`。

```sql
SELECT account_name, COUNT(*) AS cnt FROM google_ads__ad_group_report GROUP BY account_name ORDER BY cnt DESC LIMIT 50
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-059/attempt-01/sql/S11.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-059/attempt-01/sql/S11.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-059/attempt-01/results/S11.rows.jsonl)；完整：True；SHA256：`f0f0760ab061b9736878e8708a5b1c17b01d6dc635e95b1acab69f54f2590ef3`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "google_ads__ad_group_report", "kind": "base", "block": null, "base_tables": ["google_ads__ad_group_report"]}] | [] | ["account_name"] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |


## S12

类别 `data`；来源 `query_db`；调用 `6426194620c8450e9132791dc9d6816d`；状态 `success`。

```sql
SELECT campaign_name FROM google_ads__ad_group_report GROUP BY campaign_name ORDER BY campaign_name LIMIT 200
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-059/attempt-01/sql/S12.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-059/attempt-01/sql/S12.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-059/attempt-01/results/S12.rows.jsonl)；完整：True；SHA256：`41e705c3627669fc3d5ca9ec8d4175bb4b561f8520d7be5260a1fc18f6cb6e91`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "google_ads__ad_group_report", "kind": "base", "block": null, "base_tables": ["google_ads__ad_group_report"]}] | [] | ["campaign_name"] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |


## S13

类别 `data`；来源 `query_db`；调用 `edec1bd209f64338b898351ca1efaf09`；状态 `success`。

```sql
SELECT account_name, COUNT(DISTINCT account_id) AS ids FROM google_ads__ad_group_report GROUP BY account_name ORDER BY account_name
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-059/attempt-01/sql/S13.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-059/attempt-01/sql/S13.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-059/attempt-01/results/S13.rows.jsonl)；完整：True；SHA256：`2dfb7d0e4ca1863eae3f090f7e76ad3ac7323f09d575f243510fd3789461be5a`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "google_ads__ad_group_report", "kind": "base", "block": null, "base_tables": ["google_ads__ad_group_report"]}] | [] | ["account_name"] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(DISTINCT account_id) | [{"table": "google_ads__ad_group_report", "column": "account_id"}] | [] | False |


## S14

类别 `data`；来源 `query_db`；调用 `dde72ffdf7a74a22af83f5a04633dcd9`；状态 `success`。

```sql
SELECT campaign_name, COUNT(*) AS cnt FROM google_ads__ad_group_report GROUP BY campaign_name ORDER BY cnt DESC LIMIT 200
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-059/attempt-01/sql/S14.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-059/attempt-01/sql/S14.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-059/attempt-01/results/S14.rows.jsonl)；完整：True；SHA256：`527f4f2d337ce65572551382fb359bcf28f54b704d598491aa4957d2fe61d53d`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "google_ads__ad_group_report", "kind": "base", "block": null, "base_tables": ["google_ads__ad_group_report"]}] | [] | ["campaign_name"] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |


## S15

类别 `data`；来源 `query_db`；调用 `8aea18c31aee4420af620318c6b2c36f`；状态 `success`。

```sql
SELECT keyword_text, keyword_match_type, COUNT(*) AS cnt, SUM(clicks) AS total_clicks, SUM(conversions) AS total_conv, SUM(impressions) AS total_imp FROM google_ads__keyword_report GROUP BY keyword_text, keyword_match_type ORDER BY cnt DESC LIMIT 100
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-059/attempt-01/sql/S15.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-059/attempt-01/sql/S15.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-059/attempt-01/results/S15.rows.jsonl)；完整：True；SHA256：`318ccf7d6df42ba0075b6b38b7397dd14ff1adc4e0acfe3ba46f5eb4c456e0ff`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "google_ads__keyword_report", "kind": "base", "block": null, "base_tables": ["google_ads__keyword_report"]}] | [] | ["keyword_text", "keyword_match_type"] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |
| B1 | SUM(clicks) | [{"table": "google_ads__keyword_report", "column": "clicks"}] | [] | False |
| B1 | SUM(conversions) | [{"table": "google_ads__keyword_report", "column": "conversions"}] | [] | False |
| B1 | SUM(impressions) | [{"table": "google_ads__keyword_report", "column": "impressions"}] | [] | False |


## S16

类别 `data`；来源 `query_db`；调用 `c55057c7164e4ecabbaf48c9005a3bcd`；状态 `success`。

```sql
SELECT COUNT(*) AS total, COUNT(DISTINCT ad_group_id || '|' || date_day) AS unique_pairs FROM google_ads__ad_group_report
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-059/attempt-01/sql/S16.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-059/attempt-01/sql/S16.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-059/attempt-01/results/S16.rows.jsonl)；完整：True；SHA256：`1c9881d5e0ba36d898a5a1b98d8d02c74bf55b26b6d842bcda9d3b5d7586df07`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "google_ads__ad_group_report", "kind": "base", "block": null, "base_tables": ["google_ads__ad_group_report"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |
| B1 | COUNT(DISTINCT ad_group_id \|\| '\|' \|\| date_day) | [{"table": "google_ads__ad_group_report", "column": "date_day"}, {"table": "google_ads__ad_group_report", "column": "ad_group_id"}] | [] | False |


## S17

类别 `data`；来源 `query_db`；调用 `894a8119cb424d958e6c04c180b88137`；状态 `success`。

```sql
SELECT substr(campaign_name, 1, instr(campaign_name,' -')-1) AS campaign_type, COUNT(*) AS cnt FROM google_ads__ad_group_report GROUP BY campaign_type ORDER BY cnt DESC
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-059/attempt-01/sql/S17.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-059/attempt-01/sql/S17.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-059/attempt-01/results/S17.rows.jsonl)；完整：True；SHA256：`ecc19ba548dc367bb2c5c616d61ed772382497153be8ca322c5938fc4293fd5e`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "google_ads__ad_group_report", "kind": "base", "block": null, "base_tables": ["google_ads__ad_group_report"]}] | [] | ["SUBSTRING(campaign_name, 1, INSTR(campaign_name, ' -') - 1)"] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |


## S18

类别 `data`；来源 `query_db`；调用 `e79535aa4993486ba495f7f56e8850c5`；状态 `success`。

```sql
SELECT currency_code, COUNT(*) AS cnt FROM google_ads__ad_group_report GROUP BY currency_code ORDER BY cnt DESC
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-059/attempt-01/sql/S18.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-059/attempt-01/sql/S18.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-059/attempt-01/results/S18.rows.jsonl)；完整：True；SHA256：`231fa8d7607dd8b973e858d5883875e3a4b0bb725aad894e5d6d29f025aa42d0`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "google_ads__ad_group_report", "kind": "base", "block": null, "base_tables": ["google_ads__ad_group_report"]}] | [] | ["currency_code"] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |


## S19

类别 `data`；来源 `query_db`；调用 `40145ff0f7c543f2a020e733f8421cba`；状态 `success`。

```sql
SELECT campaign_type, COUNT(*) AS cnt FROM (SELECT substr(campaign_name, 1, instr(campaign_name,' -')-1) AS campaign_type FROM google_ads__ad_group_report) GROUP BY campaign_type ORDER BY cnt DESC
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-059/attempt-01/sql/S19.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-059/attempt-01/sql/S19.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-059/attempt-01/results/S19.rows.jsonl)；完整：True；SHA256：`ecc19ba548dc367bb2c5c616d61ed772382497153be8ca322c5938fc4293fd5e`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "google_ads__ad_group_report", "kind": "base", "block": null, "base_tables": ["google_ads__ad_group_report"]}] | [] | [] |
| B2 | [{"alias": "", "kind": "derived", "block": "B1", "base_tables": ["google_ads__ad_group_report"]}] | [] | ["campaign_type"] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B2 | COUNT(*) | [] | [] | True |


## S20

类别 `data`；来源 `query_db`；调用 `24c8a09f710f44be8477d5f31b612a2e`；状态 `success`。

```sql
SELECT date_day, COUNT(*) AS cnt FROM google_ads__ad_group_report GROUP BY date_day ORDER BY date_day
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-059/attempt-01/sql/S20.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-059/attempt-01/sql/S20.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-059/attempt-01/results/S20.rows.jsonl)；完整：True；SHA256：`6bb45922297b6a8b23164526df6a528c2e67d08d496969de53e1e9c4996db5e7`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "google_ads__ad_group_report", "kind": "base", "block": null, "base_tables": ["google_ads__ad_group_report"]}] | [] | ["date_day"] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |


## S21

类别 `data`；来源 `query_db`；调用 `927a8be8b4104e4bb42693a03d2d56f5`；状态 `success`。

```sql
SELECT DISTINCT substr(campaign_name, 1, instr(campaign_name,' -')-1) AS campaign_type FROM google_ads__ad_group_report ORDER BY campaign_type
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-059/attempt-01/sql/S21.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-059/attempt-01/sql/S21.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-059/attempt-01/results/S21.rows.jsonl)；完整：True；SHA256：`1c7c1bc9f35e7a4a4343ed9ca05b0e53da215b94d3b650edd57c42085d101bcf`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "google_ads__ad_group_report", "kind": "base", "block": null, "base_tables": ["google_ads__ad_group_report"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |


## S22

类别 `data`；来源 `query_db`；调用 `a286e91e1d6b40bf948f04820caf141d`；状态 `success`。

```sql
SELECT DISTINCT ltrim(substr(campaign_name, instr(campaign_name,' -')+2)) AS time_period FROM google_ads__ad_group_report ORDER BY time_period
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-059/attempt-01/sql/S22.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-059/attempt-01/sql/S22.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-059/attempt-01/results/S22.rows.jsonl)；完整：True；SHA256：`d44c348a574be618454fff55a041355a20924903f9c7ad112a096c9a682ef898`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "google_ads__ad_group_report", "kind": "base", "block": null, "base_tables": ["google_ads__ad_group_report"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |


## S23

类别 `data`；来源 `query_db`；调用 `1c3fdf0a66cf433fb1935f584c89c3b3`；状态 `success`。

```sql
SELECT DISTINCT substr(campaign_name, 1, instr(campaign_name,' -')-1) AS campaign_type FROM google_ads__ad_group_report ORDER BY campaign_type
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-059/attempt-01/sql/S23.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-059/attempt-01/sql/S23.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-059/attempt-01/results/S23.rows.jsonl)；完整：True；SHA256：`1c7c1bc9f35e7a4a4343ed9ca05b0e53da215b94d3b650edd57c42085d101bcf`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "google_ads__ad_group_report", "kind": "base", "block": null, "base_tables": ["google_ads__ad_group_report"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |


## S24

类别 `data`；来源 `query_db`；调用 `abbd89ba4cb84d0b8fbbde0b15b11bef`；状态 `success`。

```sql
SELECT DISTINCT keyword_text FROM google_ads__keyword_report ORDER BY keyword_text LIMIT 50
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-059/attempt-01/sql/S24.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-059/attempt-01/sql/S24.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-059/attempt-01/results/S24.rows.jsonl)；完整：True；SHA256：`6b5c150a2d5e9bd8b425df74eb338e34d445c264101c4d40a2fa4ccaf8c93308`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "google_ads__keyword_report", "kind": "base", "block": null, "base_tables": ["google_ads__keyword_report"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |


## S25

类别 `data`；来源 `query_db`；调用 `2ba6882f05bd41d59243a63adcb0a821`；状态 `success`。

```sql
SELECT campaign_type FROM (SELECT DISTINCT substr(campaign_name, 1, instr(campaign_name,' -')-1) AS campaign_type FROM google_ads__ad_group_report) ORDER BY campaign_type
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-059/attempt-01/sql/S25.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-059/attempt-01/sql/S25.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-059/attempt-01/results/S25.rows.jsonl)；完整：True；SHA256：`1c7c1bc9f35e7a4a4343ed9ca05b0e53da215b94d3b650edd57c42085d101bcf`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "google_ads__ad_group_report", "kind": "base", "block": null, "base_tables": ["google_ads__ad_group_report"]}] | [] | [] |
| B2 | [{"alias": "", "kind": "derived", "block": "B1", "base_tables": ["google_ads__ad_group_report"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |


## S26

类别 `data`；来源 `query_db`；调用 `e26a8dbb4efb4b29bd2ca3f9433845ee`；状态 `success`。

```sql
SELECT keyword_text FROM google_ads__keyword_report GROUP BY keyword_text ORDER BY keyword_text LIMIT 100
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-059/attempt-01/sql/S26.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-059/attempt-01/sql/S26.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-059/attempt-01/results/S26.rows.jsonl)；完整：True；SHA256：`bc8434946aac5195a2868775e4f79b323ac0777dc6447e5d7f6cb1268e5ec92a`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "google_ads__keyword_report", "kind": "base", "block": null, "base_tables": ["google_ads__keyword_report"]}] | [] | ["keyword_text"] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |


## S27

类别 `data`；来源 `query_db`；调用 `4f5d8c41ab234faf849bf45f8f662c9a`；状态 `success`。

```sql
SELECT MIN(clicks) AS min_clk, MAX(clicks) AS max_clk, MIN(impressions) AS min_imp, MAX(impressions) AS max_imp, MIN(conversions) AS min_conv, MAX(conversions) AS max_conv, MIN(spend) AS min_spend, MAX(spend) AS max_spend FROM google_ads__ad_group_report
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-059/attempt-01/sql/S27.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-059/attempt-01/sql/S27.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-059/attempt-01/results/S27.rows.jsonl)；完整：True；SHA256：`00ba3bbb2782cb069f6ddfc908c798bb25d19058157aedc4c4be03297d387a64`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "google_ads__ad_group_report", "kind": "base", "block": null, "base_tables": ["google_ads__ad_group_report"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | MIN(clicks) | [{"table": "google_ads__ad_group_report", "column": "clicks"}] | [] | False |
| B1 | MAX(clicks) | [{"table": "google_ads__ad_group_report", "column": "clicks"}] | [] | False |
| B1 | MIN(impressions) | [{"table": "google_ads__ad_group_report", "column": "impressions"}] | [] | False |
| B1 | MAX(impressions) | [{"table": "google_ads__ad_group_report", "column": "impressions"}] | [] | False |
| B1 | MIN(conversions) | [{"table": "google_ads__ad_group_report", "column": "conversions"}] | [] | False |
| B1 | MAX(conversions) | [{"table": "google_ads__ad_group_report", "column": "conversions"}] | [] | False |
| B1 | MIN(spend) | [{"table": "google_ads__ad_group_report", "column": "spend"}] | [] | False |
| B1 | MAX(spend) | [{"table": "google_ads__ad_group_report", "column": "spend"}] | [] | False |


## S28

类别 `data`；来源 `query_db`；调用 `3688665fe2b94bd29e2726b43095a64e`；状态 `success`。

```sql
SELECT ad_group_id, COUNT(*) AS n, SUM(clicks) AS clicks, SUM(impressions) AS imp, SUM(conversions) AS conv, SUM(spend) AS spend FROM google_ads__ad_group_report GROUP BY ad_group_id HAVING clicks > 0 AND imp > 0 ORDER BY clicks DESC LIMIT 30
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-059/attempt-01/sql/S28.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-059/attempt-01/sql/S28.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-059/attempt-01/results/S28.rows.jsonl)；完整：True；SHA256：`82072d59d302a7bf73b1d4b34a396654ff36811f8518f13b280f4e00441f1e73`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "google_ads__ad_group_report", "kind": "base", "block": null, "base_tables": ["google_ads__ad_group_report"]}] | [] | ["ad_group_id"] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |
| B1 | SUM(clicks) | [{"table": "google_ads__ad_group_report", "column": "clicks"}] | [] | False |
| B1 | SUM(impressions) | [{"table": "google_ads__ad_group_report", "column": "impressions"}] | [] | False |
| B1 | SUM(conversions) | [{"table": "google_ads__ad_group_report", "column": "conversions"}] | [] | False |
| B1 | SUM(spend) | [{"table": "google_ads__ad_group_report", "column": "spend"}] | [] | False |


## S29

类别 `data`；来源 `query_db`；调用 `f08e1e5cd38f4b42908c0e235a0213c1`；状态 `success`。

```sql
WITH agg AS (
  SELECT ad_group_id,
         SUM(clicks) AS clicks,
         SUM(impressions) AS impressions,
         SUM(conversions) AS conversions,
         SUM(spend) AS spend,
         SUM(conversions_value) AS conv_value
  FROM google_ads__ad_group_report
  GROUP BY ad_group_id
  HAVING SUM(clicks) > 0 AND SUM(impressions) > 0
),
metrics AS (
  SELECT ad_group_id, clicks, impressions, conversions, spend, conv_value,
         clicks*1.0/impressions AS ctr,
         conversions*1.0/clicks AS cvr
  FROM agg
),
ranked AS (
  SELECT m.*,
         ROW_NUMBER() OVER (ORDER BY ctr) AS rn_ctr,
         ROW_NUMBER() OVER (ORDER BY cvr) AS rn_cvr,
         COUNT(*) OVER () AS n
  FROM metrics m
)
SELECT 'ctr_p75' AS metric, MIN(ctr) AS value, MAX(rn_ctr) AS rank FROM ranked WHERE rn_ctr >= CAST(0.75*n AS INT) AND rn_ctr <= CAST(0.75*n AS INT)+1
UNION ALL
SELECT 'ctr_p25', MIN(ctr), MAX(rn_ctr) FROM ranked WHERE rn_ctr >= CAST(0.25*n AS INT) AND rn_ctr <= CAST(0.25*n AS INT)+1
UNION ALL
SELECT 'cvr_p75', MIN(cvr), MAX(rn_cvr) FROM ranked WHERE rn_cvr >= CAST(0.75*n AS INT) AND rn_cvr <= CAST(0.75*n AS INT)+1
UNION ALL
SELECT 'cvr_p25', MIN(cvr), MAX(rn_cvr) FROM ranked WHERE rn_cvr >= CAST(0.25*n AS INT) AND rn_cvr <= CAST(0.25*n AS INT)+1
UNION ALL
SELECT 'n', MIN(n), MAX(n) FROM ranked
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-059/attempt-01/sql/S29.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-059/attempt-01/sql/S29.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-059/attempt-01/results/S29.rows.jsonl)；完整：True；SHA256：`44db2372ed4c015cc6cebc2c29333be5eac983d4aee6270d90ad010f82a12c18`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "google_ads__ad_group_report", "kind": "base", "block": null, "base_tables": ["google_ads__ad_group_report"]}] | [] | ["ad_group_id"] |
| B2 | [{"alias": "agg", "kind": "derived", "block": "B1", "base_tables": ["google_ads__ad_group_report"]}] | [] | [] |
| B3 | [{"alias": "m", "kind": "derived", "block": "B2", "base_tables": ["google_ads__ad_group_report"]}] | [] | [] |
| B4 | [{"alias": "ranked", "kind": "derived", "block": "B3", "base_tables": ["google_ads__ad_group_report"]}] | [] | [] |
| B5 | [{"alias": "ranked", "kind": "derived", "block": "B3", "base_tables": ["google_ads__ad_group_report"]}] | [] | [] |
| B6 | [] | [] | [] |
| B7 | [{"alias": "ranked", "kind": "derived", "block": "B3", "base_tables": ["google_ads__ad_group_report"]}] | [] | [] |
| B8 | [] | [] | [] |
| B9 | [{"alias": "ranked", "kind": "derived", "block": "B3", "base_tables": ["google_ads__ad_group_report"]}] | [] | [] |
| B10 | [] | [] | [] |
| B11 | [{"alias": "ranked", "kind": "derived", "block": "B3", "base_tables": ["google_ads__ad_group_report"]}] | [] | [] |
| B12 | [] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | SUM(clicks) | [{"table": "google_ads__ad_group_report", "column": "clicks"}] | [] | False |
| B1 | SUM(impressions) | [{"table": "google_ads__ad_group_report", "column": "impressions"}] | [] | False |
| B1 | SUM(conversions) | [{"table": "google_ads__ad_group_report", "column": "conversions"}] | [] | False |
| B1 | SUM(spend) | [{"table": "google_ads__ad_group_report", "column": "spend"}] | [] | False |
| B1 | SUM(conversions_value) | [{"table": "google_ads__ad_group_report", "column": "conversions_value"}] | [] | False |
| B1 | SUM(clicks) | [{"table": "google_ads__ad_group_report", "column": "clicks"}] | [] | False |
| B1 | SUM(impressions) | [{"table": "google_ads__ad_group_report", "column": "impressions"}] | [] | False |
| B4 | MIN(ctr) | [{"table": "google_ads__ad_group_report", "column": "impressions"}, {"table": "google_ads__ad_group_report", "column": "clicks"}] | [] | False |
| B4 | MAX(rn_ctr) | [{"table": "google_ads__ad_group_report", "column": "impressions"}, {"table": "google_ads__ad_group_report", "column": "clicks"}] | [] | False |
| B5 | MIN(ctr) | [{"table": "google_ads__ad_group_report", "column": "impressions"}, {"table": "google_ads__ad_group_report", "column": "clicks"}] | [] | False |
| B5 | MAX(rn_ctr) | [{"table": "google_ads__ad_group_report", "column": "impressions"}, {"table": "google_ads__ad_group_report", "column": "clicks"}] | [] | False |
| B7 | MIN(cvr) | [{"table": "google_ads__ad_group_report", "column": "clicks"}, {"table": "google_ads__ad_group_report", "column": "conversions"}] | [] | False |
| B7 | MAX(rn_cvr) | [{"table": "google_ads__ad_group_report", "column": "clicks"}, {"table": "google_ads__ad_group_report", "column": "conversions"}] | [] | False |
| B9 | MIN(cvr) | [{"table": "google_ads__ad_group_report", "column": "clicks"}, {"table": "google_ads__ad_group_report", "column": "conversions"}] | [] | False |
| B9 | MAX(rn_cvr) | [{"table": "google_ads__ad_group_report", "column": "clicks"}, {"table": "google_ads__ad_group_report", "column": "conversions"}] | [] | False |
| B11 | MIN(n) | [] | [] | False |
| B11 | MAX(n) | [] | [] | False |


## S30

类别 `data`；来源 `query_db`；调用 `d806be80c2ef490da8ac804d1b47abe1`；状态 `success`。

```sql
SELECT COUNT(*) AS rows_total, COUNT(DISTINCT ad_group_id || '|' || criterion_id || '|' || date_day) AS uniq FROM google_ads__keyword_report
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-059/attempt-01/sql/S30.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-059/attempt-01/sql/S30.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-059/attempt-01/results/S30.rows.jsonl)；完整：True；SHA256：`35dfb32a23eba63da5db8239321865450a6ce3959048a722beb2bcdf9ebfb569`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "google_ads__keyword_report", "kind": "base", "block": null, "base_tables": ["google_ads__keyword_report"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |
| B1 | COUNT(DISTINCT ad_group_id \|\| '\|' \|\| criterion_id \|\| '\|' \|\| date_day) | [{"table": "google_ads__keyword_report", "column": "date_day"}, {"table": "google_ads__keyword_report", "column": "criterion_id"}, {"table": "google_ads__keyword_report", "column": "ad_group_id"}] | [] | False |


## S31

类别 `data`；来源 `query_db`；调用 `0c9f84b8f7fb40368609140af0ed7ec3`；状态 `success`。

```sql
WITH agg AS (
  SELECT ad_group_id,
         SUM(clicks) AS clicks,
         SUM(impressions) AS impressions,
         SUM(conversions) AS conversions,
         SUM(spend) AS spend,
         SUM(conversions_value) AS conv_value
  FROM google_ads__ad_group_report
  GROUP BY ad_group_id
  HAVING SUM(clicks) > 0 AND SUM(impressions) > 0
),
metrics AS (
  SELECT ad_group_id, clicks, impressions, conversions, spend, conv_value,
         clicks*1.0/impressions AS ctr,
         conversions*1.0/clicks AS cvr
  FROM agg
),
ranked AS (
  SELECT m.*,
         ROW_NUMBER() OVER (ORDER BY ctr) AS rn_ctr,
         ROW_NUMBER() OVER (ORDER BY cvr) AS rn_cvr,
         COUNT(*) OVER () AS n
  FROM metrics m
)
SELECT ctr_value, cvr_value, n
FROM (
  SELECT ctr AS ctr_value, rn_ctr, n FROM ranked WHERE rn_ctr = CAST(0.75*n AS INTEGER)
) AS ctr_t
CROSS JOIN (
  SELECT cvr AS cvr_value, rn_cvr FROM ranked WHERE rn_cvr = CAST(0.25*n AS INTEGER)
) AS cvr_t
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-059/attempt-01/sql/S31.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-059/attempt-01/sql/S31.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-059/attempt-01/results/S31.rows.jsonl)；完整：True；SHA256：`cd24d41da28db5eea0d3b2c0151e70d189989b3a28a1ca6d19fd528bf5819511`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "google_ads__ad_group_report", "kind": "base", "block": null, "base_tables": ["google_ads__ad_group_report"]}] | [] | ["ad_group_id"] |
| B2 | [{"alias": "agg", "kind": "derived", "block": "B1", "base_tables": ["google_ads__ad_group_report"]}] | [] | [] |
| B3 | [{"alias": "m", "kind": "derived", "block": "B2", "base_tables": ["google_ads__ad_group_report"]}] | [] | [] |
| B4 | [{"alias": "ranked", "kind": "derived", "block": "B3", "base_tables": ["google_ads__ad_group_report"]}] | [] | [] |
| B5 | [{"alias": "ranked", "kind": "derived", "block": "B3", "base_tables": ["google_ads__ad_group_report"]}] | [] | [] |
| B6 | [{"alias": "ctr_t", "kind": "derived", "block": "B4", "base_tables": ["google_ads__ad_group_report"]}, {"alias": "cvr_t", "kind": "derived", "block": "B5", "base_tables": ["google_ads__ad_group_report"]}] | [{"type": "CROSS", "right": "(SELECT cvr AS cvr_value, rn_cvr FROM ranked WHERE rn_cvr = CAST(0.25 * n AS INTEGER)) AS cvr_t", "on": null, "using": []}] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | SUM(clicks) | [{"table": "google_ads__ad_group_report", "column": "clicks"}] | [] | False |
| B1 | SUM(impressions) | [{"table": "google_ads__ad_group_report", "column": "impressions"}] | [] | False |
| B1 | SUM(conversions) | [{"table": "google_ads__ad_group_report", "column": "conversions"}] | [] | False |
| B1 | SUM(spend) | [{"table": "google_ads__ad_group_report", "column": "spend"}] | [] | False |
| B1 | SUM(conversions_value) | [{"table": "google_ads__ad_group_report", "column": "conversions_value"}] | [] | False |
| B1 | SUM(clicks) | [{"table": "google_ads__ad_group_report", "column": "clicks"}] | [] | False |
| B1 | SUM(impressions) | [{"table": "google_ads__ad_group_report", "column": "impressions"}] | [] | False |


## S32

类别 `data`；来源 `query_db`；调用 `f621a96ebcdd4fa6b6bb40769f34ec0f`；状态 `success`。

```sql
WITH agg AS (
  SELECT ad_group_id,
         SUM(clicks) AS clicks,
         SUM(impressions) AS impressions,
         SUM(conversions) AS conversions,
         SUM(spend) AS spend,
         SUM(conversions_value) AS conv_value
  FROM google_ads__ad_group_report
  GROUP BY ad_group_id
  HAVING SUM(clicks) > 0 AND SUM(impressions) > 0
),
metrics AS (
  SELECT ad_group_id, clicks, impressions, conversions, spend, conv_value,
         clicks*1.0/impressions AS ctr,
         conversions*1.0/clicks AS cvr
  FROM agg
)
SELECT COUNT(*) AS total,
       SUM(CASE WHEN ctr > 0.035874 AND cvr < 0.038462 THEN 1 ELSE 0 END) AS problem_count
FROM metrics
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-059/attempt-01/sql/S32.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-059/attempt-01/sql/S32.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-059/attempt-01/results/S32.rows.jsonl)；完整：True；SHA256：`6312b58a8c52a13e49d43785ebfc9123d57fa57b223307d2331fb2072bfae36b`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "google_ads__ad_group_report", "kind": "base", "block": null, "base_tables": ["google_ads__ad_group_report"]}] | [] | ["ad_group_id"] |
| B2 | [{"alias": "agg", "kind": "derived", "block": "B1", "base_tables": ["google_ads__ad_group_report"]}] | [] | [] |
| B3 | [{"alias": "metrics", "kind": "derived", "block": "B2", "base_tables": ["google_ads__ad_group_report"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | SUM(clicks) | [{"table": "google_ads__ad_group_report", "column": "clicks"}] | [] | False |
| B1 | SUM(impressions) | [{"table": "google_ads__ad_group_report", "column": "impressions"}] | [] | False |
| B1 | SUM(conversions) | [{"table": "google_ads__ad_group_report", "column": "conversions"}] | [] | False |
| B1 | SUM(spend) | [{"table": "google_ads__ad_group_report", "column": "spend"}] | [] | False |
| B1 | SUM(conversions_value) | [{"table": "google_ads__ad_group_report", "column": "conversions_value"}] | [] | False |
| B1 | SUM(clicks) | [{"table": "google_ads__ad_group_report", "column": "clicks"}] | [] | False |
| B1 | SUM(impressions) | [{"table": "google_ads__ad_group_report", "column": "impressions"}] | [] | False |
| B3 | COUNT(*) | [] | [] | True |
| B3 | SUM(CASE WHEN ctr > 0.035874 AND cvr < 0.038462 THEN 1 ELSE 0 END) | [] | [{"table": "google_ads__ad_group_report", "column": "impressions"}, {"table": "google_ads__ad_group_report", "column": "clicks"}, {"table": "google_ads__ad_group_report", "column": "clicks"}, {"table": "google_ads__ad_group_report", "column": "conversions"}] | False |


## S33

类别 `data`；来源 `query_db`；调用 `61975b04329c4b2a93707cda7fd8fb1e`；状态 `success`。

```sql
WITH agg AS (
  SELECT ad_group_id,
         SUM(clicks) AS clicks,
         SUM(impressions) AS impressions,
         SUM(conversions) AS conversions,
         SUM(spend) AS spend,
         SUM(conversions_value) AS conv_value
  FROM google_ads__ad_group_report
  GROUP BY ad_group_id
  HAVING SUM(clicks) > 0 AND SUM(impressions) > 0
),
metrics AS (
  SELECT ad_group_id, clicks, impressions, conversions, spend, conv_value,
         clicks*1.0/impressions AS ctr,
         conversions*1.0/clicks AS cvr
  FROM agg
)
SELECT ad_group_id, clicks, impressions, conversions, ROUND(ctr*100,4) AS ctr_pct, ROUND(cvr*100,4) AS cvr_pct, ROUND(spend,2) AS spend
FROM metrics
WHERE ctr > 0.035874 AND cvr < 0.038462
ORDER BY ctr DESC, cvr ASC
LIMIT 30
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-059/attempt-01/sql/S33.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-059/attempt-01/sql/S33.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-059/attempt-01/results/S33.rows.jsonl)；完整：True；SHA256：`352124a086aa54e7a93505a8a8612c27b21127f605cad556699832f085e9c2e6`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "google_ads__ad_group_report", "kind": "base", "block": null, "base_tables": ["google_ads__ad_group_report"]}] | [] | ["ad_group_id"] |
| B2 | [{"alias": "agg", "kind": "derived", "block": "B1", "base_tables": ["google_ads__ad_group_report"]}] | [] | [] |
| B3 | [{"alias": "metrics", "kind": "derived", "block": "B2", "base_tables": ["google_ads__ad_group_report"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | SUM(clicks) | [{"table": "google_ads__ad_group_report", "column": "clicks"}] | [] | False |
| B1 | SUM(impressions) | [{"table": "google_ads__ad_group_report", "column": "impressions"}] | [] | False |
| B1 | SUM(conversions) | [{"table": "google_ads__ad_group_report", "column": "conversions"}] | [] | False |
| B1 | SUM(spend) | [{"table": "google_ads__ad_group_report", "column": "spend"}] | [] | False |
| B1 | SUM(conversions_value) | [{"table": "google_ads__ad_group_report", "column": "conversions_value"}] | [] | False |
| B1 | SUM(clicks) | [{"table": "google_ads__ad_group_report", "column": "clicks"}] | [] | False |
| B1 | SUM(impressions) | [{"table": "google_ads__ad_group_report", "column": "impressions"}] | [] | False |


## S34

类别 `data`；来源 `query_db`；调用 `7a546815033c40a28bddf669548bac62`；状态 `success`。

```sql
SELECT DISTINCT account_name FROM google_ads__ad_group_report ORDER BY account_name
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-059/attempt-01/sql/S34.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-059/attempt-01/sql/S34.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-059/attempt-01/results/S34.rows.jsonl)；完整：True；SHA256：`39e92ef0e825c609b17e3ed03f526761b4ec44a20ee303d19564b8eca2b68d67`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "google_ads__ad_group_report", "kind": "base", "block": null, "base_tables": ["google_ads__ad_group_report"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |


## S35

类别 `data`；来源 `query_db`；调用 `1af0bb80acc14d598fbb0387bfb48c6c`；状态 `success`。

```sql
WITH master AS (
  SELECT r.ad_group_id, r.account_name, r.campaign_name, r.campaign_id, r.ad_group_type, r.status,
         SUM(r.clicks) AS clicks, SUM(r.impressions) AS impressions,
         SUM(r.conversions) AS conversions, SUM(r.spend) AS spend,
         SUM(r.clicks)*1.0/SUM(r.impressions) AS ctr,
         SUM(r.conversions)*1.0/SUM(r.clicks) AS cvr,
         CASE
           WHEN r.account_name LIKE '%Automotive%' THEN 'Automotive'
           WHEN r.account_name LIKE '%Education%' THEN 'Education'
           WHEN r.account_name LIKE '%Entertainment%' THEN 'Entertainment'
           WHEN r.account_name LIKE '%Fashion%' THEN 'Fashion'
           WHEN r.account_name LIKE '%Finance%' THEN 'Finance'
           WHEN r.account_name LIKE '%Food%' THEN 'Food'
           WHEN r.account_name LIKE '%Healthcare%' THEN 'Healthcare'
           WHEN r.account_name LIKE '%Real Estate%' THEN 'Real Estate'
           WHEN r.account_name LIKE '%Retail%' THEN 'Retail'
           WHEN r.account_name LIKE '%Sports%' THEN 'Sports'
           WHEN r.account_name LIKE '%Technology%' THEN 'Technology'
           WHEN r.account_name LIKE '%Travel%' THEN 'Travel'
           ELSE 'Other'
         END AS industry
  FROM google_ads__ad_group_report r
  GROUP BY r.ad_group_id
  HAVING SUM(r.clicks) > 0 AND SUM(r.impressions) > 0
)
SELECT (ctr > 0.0358744 AND cvr < 0.0384615) AS is_problem,
       COUNT(*) AS ad_groups,
       SUM(clicks) AS clicks, SUM(impressions) AS impressions,
       SUM(conversions) AS conversions, ROUND(SUM(spend),2) AS spend,
       ROUND(100.0*SUM(clicks)/SUM(impressions),3) AS ctr_pct,
       ROUND(100.0*SUM(conversions)/SUM(clicks),3) AS cvr_pct
FROM master
GROUP BY is_problem
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-059/attempt-01/sql/S35.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-059/attempt-01/sql/S35.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-059/attempt-01/results/S35.rows.jsonl)；完整：True；SHA256：`6c54cf4b493197486ffe223e366782d0549ec68e5c5212fe537018772eb21631`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "r", "kind": "base", "block": null, "base_tables": ["google_ads__ad_group_report"]}] | [] | ["r.ad_group_id"] |
| B2 | [{"alias": "master", "kind": "derived", "block": "B1", "base_tables": ["google_ads__ad_group_report"]}] | [] | ["(ctr > 0.0358744 AND cvr < 0.0384615)"] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | SUM(r.clicks) | [{"table": "google_ads__ad_group_report", "column": "clicks"}] | [] | False |
| B1 | SUM(r.impressions) | [{"table": "google_ads__ad_group_report", "column": "impressions"}] | [] | False |
| B1 | SUM(r.conversions) | [{"table": "google_ads__ad_group_report", "column": "conversions"}] | [] | False |
| B1 | SUM(r.spend) | [{"table": "google_ads__ad_group_report", "column": "spend"}] | [] | False |
| B1 | SUM(r.impressions) | [{"table": "google_ads__ad_group_report", "column": "impressions"}] | [] | False |
| B1 | SUM(r.clicks) | [{"table": "google_ads__ad_group_report", "column": "clicks"}] | [] | False |
| B1 | SUM(r.clicks) | [{"table": "google_ads__ad_group_report", "column": "clicks"}] | [] | False |
| B1 | SUM(r.conversions) | [{"table": "google_ads__ad_group_report", "column": "conversions"}] | [] | False |
| B1 | SUM(r.clicks) | [{"table": "google_ads__ad_group_report", "column": "clicks"}] | [] | False |
| B1 | SUM(r.impressions) | [{"table": "google_ads__ad_group_report", "column": "impressions"}] | [] | False |
| B2 | COUNT(*) | [] | [] | True |
| B2 | SUM(clicks) | [{"table": "google_ads__ad_group_report", "column": "clicks"}] | [] | False |
| B2 | SUM(impressions) | [{"table": "google_ads__ad_group_report", "column": "impressions"}] | [] | False |
| B2 | SUM(conversions) | [{"table": "google_ads__ad_group_report", "column": "conversions"}] | [] | False |
| B2 | SUM(spend) | [{"table": "google_ads__ad_group_report", "column": "spend"}] | [] | False |
| B2 | SUM(impressions) | [{"table": "google_ads__ad_group_report", "column": "impressions"}] | [] | False |
| B2 | SUM(clicks) | [{"table": "google_ads__ad_group_report", "column": "clicks"}] | [] | False |
| B2 | SUM(clicks) | [{"table": "google_ads__ad_group_report", "column": "clicks"}] | [] | False |
| B2 | SUM(conversions) | [{"table": "google_ads__ad_group_report", "column": "conversions"}] | [] | False |


## S36

类别 `data`；来源 `query_db`；调用 `3992f658e3484060b2e49fe13b317b7e`；状态 `success`。

```sql
WITH master AS (
  SELECT r.ad_group_id, r.account_name, r.campaign_name,
         SUM(r.clicks) AS clicks, SUM(r.impressions) AS impressions,
         SUM(r.conversions) AS conversions, SUM(r.spend) AS spend,
         SUM(r.clicks)*1.0/SUM(r.impressions) AS ctr,
         SUM(r.conversions)*1.0/SUM(r.clicks) AS cvr
  FROM google_ads__ad_group_report r
  GROUP BY r.ad_group_id
  HAVING SUM(r.clicks) > 0 AND SUM(r.impressions) > 0
)
SELECT CASE
         WHEN campaign_name LIKE 'Brand%' THEN 'Brand'
         WHEN campaign_name LIKE 'Display%' THEN 'Display'
         WHEN campaign_name LIKE 'Performance%' THEN 'Performance'
         WHEN campaign_name LIKE 'Search%' THEN 'Search'
         WHEN campaign_name LIKE 'Shopping%' THEN 'Shopping'
       END AS channel,
       (ctr > 0.0358744 AND cvr < 0.0384615) AS is_problem,
       COUNT(*) AS ad_groups,
       ROUND(100.0*SUM(clicks)/SUM(impressions),3) AS ctr_pct,
       ROUND(100.0*SUM(conversions)/SUM(clicks),3) AS cvr_pct,
       ROUND(SUM(spend),2) AS spend
FROM master
GROUP BY channel, is_problem
ORDER BY channel, is_problem
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-059/attempt-01/sql/S36.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-059/attempt-01/sql/S36.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-059/attempt-01/results/S36.rows.jsonl)；完整：True；SHA256：`665b95588bf17ca559ca578364dbd4568c7789427d04f5fb0a13e358241d2c86`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "r", "kind": "base", "block": null, "base_tables": ["google_ads__ad_group_report"]}] | [] | ["r.ad_group_id"] |
| B2 | [{"alias": "master", "kind": "derived", "block": "B1", "base_tables": ["google_ads__ad_group_report"]}] | [] | ["CASE WHEN campaign_name LIKE 'Brand%' THEN 'Brand' WHEN campaign_name LIKE 'Display%' THEN 'Display' WHEN campaign_name LIKE 'Performance%' THEN 'Performance' WHEN campaign_name LIKE 'Search%' THEN 'Search' WHEN campaign_name LIKE 'Shopping%' THEN 'Shopping' END", "(ctr > 0.0358744 AND cvr < 0.0384615)"] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | SUM(r.clicks) | [{"table": "google_ads__ad_group_report", "column": "clicks"}] | [] | False |
| B1 | SUM(r.impressions) | [{"table": "google_ads__ad_group_report", "column": "impressions"}] | [] | False |
| B1 | SUM(r.conversions) | [{"table": "google_ads__ad_group_report", "column": "conversions"}] | [] | False |
| B1 | SUM(r.spend) | [{"table": "google_ads__ad_group_report", "column": "spend"}] | [] | False |
| B1 | SUM(r.impressions) | [{"table": "google_ads__ad_group_report", "column": "impressions"}] | [] | False |
| B1 | SUM(r.clicks) | [{"table": "google_ads__ad_group_report", "column": "clicks"}] | [] | False |
| B1 | SUM(r.clicks) | [{"table": "google_ads__ad_group_report", "column": "clicks"}] | [] | False |
| B1 | SUM(r.conversions) | [{"table": "google_ads__ad_group_report", "column": "conversions"}] | [] | False |
| B1 | SUM(r.clicks) | [{"table": "google_ads__ad_group_report", "column": "clicks"}] | [] | False |
| B1 | SUM(r.impressions) | [{"table": "google_ads__ad_group_report", "column": "impressions"}] | [] | False |
| B2 | COUNT(*) | [] | [] | True |
| B2 | SUM(spend) | [{"table": "google_ads__ad_group_report", "column": "spend"}] | [] | False |
| B2 | SUM(impressions) | [{"table": "google_ads__ad_group_report", "column": "impressions"}] | [] | False |
| B2 | SUM(clicks) | [{"table": "google_ads__ad_group_report", "column": "clicks"}] | [] | False |
| B2 | SUM(clicks) | [{"table": "google_ads__ad_group_report", "column": "clicks"}] | [] | False |
| B2 | SUM(conversions) | [{"table": "google_ads__ad_group_report", "column": "conversions"}] | [] | False |


## S37

类别 `data`；来源 `query_db`；调用 `07074800861d46f3b58466550295b638`；状态 `success`。

```sql
WITH master AS (
  SELECT r.ad_group_id, r.account_name, r.campaign_name,
         SUM(r.clicks) AS clicks, SUM(r.impressions) AS impressions,
         SUM(r.conversions) AS conversions, SUM(r.spend) AS spend,
         SUM(r.clicks)*1.0/SUM(r.impressions) AS ctr,
         SUM(r.conversions)*1.0/SUM(r.clicks) AS cvr
  FROM google_ads__ad_group_report r
  GROUP BY r.ad_group_id
  HAVING SUM(r.clicks) > 0 AND SUM(r.impressions) > 0
)
SELECT (ctr > 0.03587443946188341 AND cvr < 0.038461538461538464) AS is_problem,
       COUNT(*) AS n,
       ROUND(100.0*SUM(clicks)/SUM(impressions),3) AS ctr_pct,
       ROUND(100.0*SUM(conversions)/SUM(clicks),3) AS cvr_pct,
       ROUND(SUM(spend),2) AS spend, SUM(clicks) AS clicks
FROM master GROUP BY is_problem
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-059/attempt-01/sql/S37.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-059/attempt-01/sql/S37.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-059/attempt-01/results/S37.rows.jsonl)；完整：True；SHA256：`27853f8dd02eaf20caa8b18fbee50809820ec901cbb3ae61d4446f14a7665315`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "r", "kind": "base", "block": null, "base_tables": ["google_ads__ad_group_report"]}] | [] | ["r.ad_group_id"] |
| B2 | [{"alias": "master", "kind": "derived", "block": "B1", "base_tables": ["google_ads__ad_group_report"]}] | [] | ["(ctr > 0.03587443946188341 AND cvr < 0.038461538461538464)"] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | SUM(r.clicks) | [{"table": "google_ads__ad_group_report", "column": "clicks"}] | [] | False |
| B1 | SUM(r.impressions) | [{"table": "google_ads__ad_group_report", "column": "impressions"}] | [] | False |
| B1 | SUM(r.conversions) | [{"table": "google_ads__ad_group_report", "column": "conversions"}] | [] | False |
| B1 | SUM(r.spend) | [{"table": "google_ads__ad_group_report", "column": "spend"}] | [] | False |
| B1 | SUM(r.impressions) | [{"table": "google_ads__ad_group_report", "column": "impressions"}] | [] | False |
| B1 | SUM(r.clicks) | [{"table": "google_ads__ad_group_report", "column": "clicks"}] | [] | False |
| B1 | SUM(r.clicks) | [{"table": "google_ads__ad_group_report", "column": "clicks"}] | [] | False |
| B1 | SUM(r.conversions) | [{"table": "google_ads__ad_group_report", "column": "conversions"}] | [] | False |
| B1 | SUM(r.clicks) | [{"table": "google_ads__ad_group_report", "column": "clicks"}] | [] | False |
| B1 | SUM(r.impressions) | [{"table": "google_ads__ad_group_report", "column": "impressions"}] | [] | False |
| B2 | COUNT(*) | [] | [] | True |
| B2 | SUM(clicks) | [{"table": "google_ads__ad_group_report", "column": "clicks"}] | [] | False |
| B2 | SUM(spend) | [{"table": "google_ads__ad_group_report", "column": "spend"}] | [] | False |
| B2 | SUM(impressions) | [{"table": "google_ads__ad_group_report", "column": "impressions"}] | [] | False |
| B2 | SUM(clicks) | [{"table": "google_ads__ad_group_report", "column": "clicks"}] | [] | False |
| B2 | SUM(clicks) | [{"table": "google_ads__ad_group_report", "column": "clicks"}] | [] | False |
| B2 | SUM(conversions) | [{"table": "google_ads__ad_group_report", "column": "conversions"}] | [] | False |


## S38

类别 `data`；来源 `query_db`；调用 `e021f1650aef4fe2a3c7617141952755`；状态 `success`。

```sql
WITH master AS (
  SELECT r.ad_group_id, r.account_name, r.campaign_name,
         SUM(r.clicks) AS clicks, SUM(r.impressions) AS impressions,
         SUM(r.conversions) AS conversions, SUM(r.spend) AS spend,
         SUM(r.clicks)*1.0/SUM(r.impressions) AS ctr,
         SUM(r.conversions)*1.0/SUM(r.clicks) AS cvr,
         ltrim(substr(r.campaign_name, instr(r.campaign_name,' -')+2)) AS period
  FROM google_ads__ad_group_report r
  GROUP BY r.ad_group_id
  HAVING SUM(r.clicks) > 0 AND SUM(r.impressions) > 0
)
SELECT period,
       SUM(CASE WHEN (ctr > 0.03587443946188341 AND cvr < 0.038461538461538464) THEN 1 ELSE 0 END) AS problem,
       SUM(CASE WHEN NOT (ctr > 0.03587443946188341 AND cvr < 0.038461538461538464) THEN 1 ELSE 0 END) AS non_problem,
       ROUND(100.0*SUM(CASE WHEN (ctr > 0.03587443946188341 AND cvr < 0.038461538461538464) THEN 1 ELSE 0 END)/COUNT(*),1) AS problem_pct
FROM master GROUP BY period ORDER BY problem_pct DESC
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-059/attempt-01/sql/S38.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-059/attempt-01/sql/S38.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-059/attempt-01/results/S38.rows.jsonl)；完整：True；SHA256：`5feba1e8f1462e7d4aa85ebc8c264a55746f1d3ef1cec1fd152f7b4a42965a03`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "r", "kind": "base", "block": null, "base_tables": ["google_ads__ad_group_report"]}] | [] | ["r.ad_group_id"] |
| B2 | [{"alias": "master", "kind": "derived", "block": "B1", "base_tables": ["google_ads__ad_group_report"]}] | [] | ["period"] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | SUM(r.clicks) | [{"table": "google_ads__ad_group_report", "column": "clicks"}] | [] | False |
| B1 | SUM(r.impressions) | [{"table": "google_ads__ad_group_report", "column": "impressions"}] | [] | False |
| B1 | SUM(r.conversions) | [{"table": "google_ads__ad_group_report", "column": "conversions"}] | [] | False |
| B1 | SUM(r.spend) | [{"table": "google_ads__ad_group_report", "column": "spend"}] | [] | False |
| B1 | SUM(r.impressions) | [{"table": "google_ads__ad_group_report", "column": "impressions"}] | [] | False |
| B1 | SUM(r.clicks) | [{"table": "google_ads__ad_group_report", "column": "clicks"}] | [] | False |
| B1 | SUM(r.clicks) | [{"table": "google_ads__ad_group_report", "column": "clicks"}] | [] | False |
| B1 | SUM(r.conversions) | [{"table": "google_ads__ad_group_report", "column": "conversions"}] | [] | False |
| B1 | SUM(r.clicks) | [{"table": "google_ads__ad_group_report", "column": "clicks"}] | [] | False |
| B1 | SUM(r.impressions) | [{"table": "google_ads__ad_group_report", "column": "impressions"}] | [] | False |
| B2 | SUM(CASE WHEN (ctr > 0.03587443946188341 AND cvr < 0.038461538461538464) THEN 1 ELSE 0 END) | [] | [{"table": "google_ads__ad_group_report", "column": "impressions"}, {"table": "google_ads__ad_group_report", "column": "clicks"}, {"table": "google_ads__ad_group_report", "column": "clicks"}, {"table": "google_ads__ad_group_report", "column": "conversions"}] | False |
| B2 | SUM(CASE WHEN NOT (ctr > 0.03587443946188341 AND cvr < 0.038461538461538464) THEN 1 ELSE 0 END) | [] | [{"table": "google_ads__ad_group_report", "column": "impressions"}, {"table": "google_ads__ad_group_report", "column": "clicks"}, {"table": "google_ads__ad_group_report", "column": "clicks"}, {"table": "google_ads__ad_group_report", "column": "conversions"}] | False |
| B2 | COUNT(*) | [] | [] | True |
| B2 | SUM(CASE WHEN (ctr > 0.03587443946188341 AND cvr < 0.038461538461538464) THEN 1 ELSE 0 END) | [] | [{"table": "google_ads__ad_group_report", "column": "impressions"}, {"table": "google_ads__ad_group_report", "column": "clicks"}, {"table": "google_ads__ad_group_report", "column": "clicks"}, {"table": "google_ads__ad_group_report", "column": "conversions"}] | False |


## S39

类别 `data`；来源 `query_db`；调用 `77b020cbc87d4350a6fd0398f8fdb0a4`；状态 `success`。

```sql
WITH master AS (
  SELECT r.ad_group_id, r.campaign_name,
         SUM(r.clicks) AS clicks, SUM(r.impressions) AS impressions,
         SUM(r.conversions) AS conversions, SUM(r.spend) AS spend,
         SUM(r.clicks)*1.0/SUM(r.impressions) AS ctr,
         SUM(r.conversions)*1.0/SUM(r.clicks) AS cvr,
         CASE
           WHEN r.campaign_name LIKE 'Brand%' THEN 'Brand'
           WHEN r.campaign_name LIKE 'Display%' THEN 'Display'
           WHEN r.campaign_name LIKE 'Performance%' THEN 'Performance'
           WHEN r.campaign_name LIKE 'Search%' THEN 'Search'
           WHEN r.campaign_name LIKE 'Shopping%' THEN 'Shopping'
         END AS channel,
         CASE
           WHEN r.campaign_name LIKE '% Audience%' THEN 'Audience'
           WHEN r.campaign_name LIKE '% Broad%' THEN 'Broad'
           WHEN r.campaign_name LIKE '% Exact%' THEN 'Exact'
           WHEN r.campaign_name LIKE '% Keywords%' THEN 'Keywords'
           WHEN r.campaign_name LIKE '% Remarketing%' THEN 'Remarketing'
         END AS strategy
  FROM google_ads__ad_group_report r
  GROUP BY r.ad_group_id
  HAVING SUM(r.clicks) > 0 AND SUM(r.impressions) > 0
)
SELECT strategy,
       SUM(CASE WHEN (ctr > 0.03587443946188341 AND cvr < 0.038461538461538464) THEN 1 ELSE 0 END) AS problem,
       SUM(CASE WHEN NOT (ctr > 0.03587443946188341 AND cvr < 0.038461538461538464) THEN 1 ELSE 0 END) AS non_problem,
       ROUND(100.0*SUM(CASE WHEN (ctr > 0.03587443946188341 AND cvr < 0.038461538461538464) THEN 1 ELSE 0 END)/COUNT(*),1) AS problem_pct,
       ROUND(100.0*SUM(CASE WHEN (ctr > 0.03587443946188341 AND cvr < 0.038461538461538464) THEN clicks ELSE 0 END)/SUM(clicks),1) AS pct_of_clicks,
       ROUND(100.0*SUM(CASE WHEN (ctr > 0.03587443946188341 AND cvr < 0.038461538461538464) THEN spend ELSE 0 END)/SUM(spend),1) AS pct_of_spend
FROM master GROUP BY strategy ORDER BY problem_pct DESC
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-059/attempt-01/sql/S39.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-059/attempt-01/sql/S39.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-059/attempt-01/results/S39.rows.jsonl)；完整：True；SHA256：`59babe613c23905c4f86f810ba156d391f0675ddb14160890767d5994bc0a03c`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "r", "kind": "base", "block": null, "base_tables": ["google_ads__ad_group_report"]}] | [] | ["r.ad_group_id"] |
| B2 | [{"alias": "master", "kind": "derived", "block": "B1", "base_tables": ["google_ads__ad_group_report"]}] | [] | ["strategy"] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | SUM(r.clicks) | [{"table": "google_ads__ad_group_report", "column": "clicks"}] | [] | False |
| B1 | SUM(r.impressions) | [{"table": "google_ads__ad_group_report", "column": "impressions"}] | [] | False |
| B1 | SUM(r.conversions) | [{"table": "google_ads__ad_group_report", "column": "conversions"}] | [] | False |
| B1 | SUM(r.spend) | [{"table": "google_ads__ad_group_report", "column": "spend"}] | [] | False |
| B1 | SUM(r.impressions) | [{"table": "google_ads__ad_group_report", "column": "impressions"}] | [] | False |
| B1 | SUM(r.clicks) | [{"table": "google_ads__ad_group_report", "column": "clicks"}] | [] | False |
| B1 | SUM(r.clicks) | [{"table": "google_ads__ad_group_report", "column": "clicks"}] | [] | False |
| B1 | SUM(r.conversions) | [{"table": "google_ads__ad_group_report", "column": "conversions"}] | [] | False |
| B1 | SUM(r.clicks) | [{"table": "google_ads__ad_group_report", "column": "clicks"}] | [] | False |
| B1 | SUM(r.impressions) | [{"table": "google_ads__ad_group_report", "column": "impressions"}] | [] | False |
| B2 | SUM(CASE WHEN (ctr > 0.03587443946188341 AND cvr < 0.038461538461538464) THEN 1 ELSE 0 END) | [] | [{"table": "google_ads__ad_group_report", "column": "impressions"}, {"table": "google_ads__ad_group_report", "column": "clicks"}, {"table": "google_ads__ad_group_report", "column": "clicks"}, {"table": "google_ads__ad_group_report", "column": "conversions"}] | False |
| B2 | SUM(CASE WHEN NOT (ctr > 0.03587443946188341 AND cvr < 0.038461538461538464) THEN 1 ELSE 0 END) | [] | [{"table": "google_ads__ad_group_report", "column": "impressions"}, {"table": "google_ads__ad_group_report", "column": "clicks"}, {"table": "google_ads__ad_group_report", "column": "clicks"}, {"table": "google_ads__ad_group_report", "column": "conversions"}] | False |
| B2 | COUNT(*) | [] | [] | True |
| B2 | SUM(clicks) | [{"table": "google_ads__ad_group_report", "column": "clicks"}] | [] | False |
| B2 | SUM(spend) | [{"table": "google_ads__ad_group_report", "column": "spend"}] | [] | False |
| B2 | SUM(CASE WHEN (ctr > 0.03587443946188341 AND cvr < 0.038461538461538464) THEN 1 ELSE 0 END) | [] | [{"table": "google_ads__ad_group_report", "column": "impressions"}, {"table": "google_ads__ad_group_report", "column": "clicks"}, {"table": "google_ads__ad_group_report", "column": "clicks"}, {"table": "google_ads__ad_group_report", "column": "conversions"}] | False |
| B2 | SUM(CASE WHEN (ctr > 0.03587443946188341 AND cvr < 0.038461538461538464) THEN clicks ELSE 0 END) | [{"table": "google_ads__ad_group_report", "column": "clicks"}] | [{"table": "google_ads__ad_group_report", "column": "impressions"}, {"table": "google_ads__ad_group_report", "column": "clicks"}, {"table": "google_ads__ad_group_report", "column": "clicks"}, {"table": "google_ads__ad_group_report", "column": "conversions"}] | False |
| B2 | SUM(CASE WHEN (ctr > 0.03587443946188341 AND cvr < 0.038461538461538464) THEN spend ELSE 0 END) | [{"table": "google_ads__ad_group_report", "column": "spend"}] | [{"table": "google_ads__ad_group_report", "column": "impressions"}, {"table": "google_ads__ad_group_report", "column": "clicks"}, {"table": "google_ads__ad_group_report", "column": "clicks"}, {"table": "google_ads__ad_group_report", "column": "conversions"}] | False |


## S40

类别 `data`；来源 `query_db`；调用 `7f10ed1dd0c74c2e8403b721492ee959`；状态 `success`。

```sql
WITH k AS (
  SELECT ad_group_id, keyword_match_type, SUM(clicks) AS clicks, SUM(impressions) AS imp, SUM(conversions) AS conv, SUM(spend) AS spend
  FROM google_ads__keyword_report GROUP BY ad_group_id, keyword_match_type
),
agg AS (
  SELECT ad_group_id, SUM(clicks) AS clicks, SUM(impressions) AS impressions, SUM(conversions) AS conversions
  FROM google_ads__ad_group_report GROUP BY ad_group_id HAVING SUM(clicks)>0 AND SUM(impressions)>0
),
m AS (
  SELECT a.ad_group_id, a.clicks, a.impressions, a.conversions,
         a.clicks*1.0/a.impressions AS ctr, a.conversions*1.0/a.clicks AS cvr
  FROM agg a
),
flag AS (
  SELECT m.*, (ctr > 0.03587443946188341 AND cvr < 0.038461538461538464) AS is_problem FROM m
)
SELECT k.keyword_match_type, f.is_problem,
       COUNT(DISTINCT f.ad_group_id) AS ad_groups,
       SUM(k.clicks) AS clicks, SUM(k.conv) AS conv, ROUND(100.0*SUM(k.conv)/SUM(k.clicks),3) AS cvr_pct, ROUND(SUM(k.spend),2) AS spend
FROM k JOIN flag f ON k.ad_group_id = f.ad_group_id
GROUP BY k.keyword_match_type, f.is_problem
ORDER BY k.keyword_match_type, f.is_problem
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-059/attempt-01/sql/S40.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-059/attempt-01/sql/S40.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-059/attempt-01/results/S40.rows.jsonl)；完整：True；SHA256：`c0d02a75508fc444cbbd7d658713e0650cc268c4d9e00b60c060c6fe6ee36a6c`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "google_ads__keyword_report", "kind": "base", "block": null, "base_tables": ["google_ads__keyword_report"]}] | [] | ["ad_group_id", "keyword_match_type"] |
| B2 | [{"alias": "google_ads__ad_group_report", "kind": "base", "block": null, "base_tables": ["google_ads__ad_group_report"]}] | [] | ["ad_group_id"] |
| B3 | [{"alias": "a", "kind": "derived", "block": "B2", "base_tables": ["google_ads__ad_group_report"]}] | [] | [] |
| B4 | [{"alias": "m", "kind": "derived", "block": "B3", "base_tables": ["google_ads__ad_group_report"]}] | [] | [] |
| B5 | [{"alias": "k", "kind": "derived", "block": "B1", "base_tables": ["google_ads__keyword_report"]}, {"alias": "f", "kind": "derived", "block": "B4", "base_tables": ["google_ads__ad_group_report"]}] | [{"type": "INNER", "right": "flag AS f", "on": "k.ad_group_id = f.ad_group_id", "using": []}] | ["k.keyword_match_type", "f.is_problem"] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | SUM(clicks) | [{"table": "google_ads__keyword_report", "column": "clicks"}] | [] | False |
| B1 | SUM(impressions) | [{"table": "google_ads__keyword_report", "column": "impressions"}] | [] | False |
| B1 | SUM(conversions) | [{"table": "google_ads__keyword_report", "column": "conversions"}] | [] | False |
| B1 | SUM(spend) | [{"table": "google_ads__keyword_report", "column": "spend"}] | [] | False |
| B2 | SUM(clicks) | [{"table": "google_ads__ad_group_report", "column": "clicks"}] | [] | False |
| B2 | SUM(impressions) | [{"table": "google_ads__ad_group_report", "column": "impressions"}] | [] | False |
| B2 | SUM(conversions) | [{"table": "google_ads__ad_group_report", "column": "conversions"}] | [] | False |
| B2 | SUM(clicks) | [{"table": "google_ads__ad_group_report", "column": "clicks"}] | [] | False |
| B2 | SUM(impressions) | [{"table": "google_ads__ad_group_report", "column": "impressions"}] | [] | False |
| B5 | COUNT(DISTINCT f.ad_group_id) | [{"table": "google_ads__ad_group_report", "column": "ad_group_id"}] | [] | False |
| B5 | SUM(k.clicks) | [{"table": "google_ads__keyword_report", "column": "clicks"}] | [] | False |
| B5 | SUM(k.conv) | [{"table": "google_ads__keyword_report", "column": "conversions"}] | [] | False |
| B5 | SUM(k.spend) | [{"table": "google_ads__keyword_report", "column": "spend"}] | [] | False |
| B5 | SUM(k.clicks) | [{"table": "google_ads__keyword_report", "column": "clicks"}] | [] | False |
| B5 | SUM(k.conv) | [{"table": "google_ads__keyword_report", "column": "conversions"}] | [] | False |


## S41

类别 `data`；来源 `query_db`；调用 `eefa3e0c7c4348b3898df5cec3f9bdbc`；状态 `success`。

```sql
WITH master AS (
  SELECT r.ad_group_id, r.account_name,
         SUM(r.clicks) AS clicks, SUM(r.impressions) AS impressions,
         SUM(r.conversions) AS conversions, SUM(r.spend) AS spend,
         SUM(r.clicks)*1.0/SUM(r.impressions) AS ctr,
         SUM(r.conversions)*1.0/SUM(r.clicks) AS cvr,
         CASE
           WHEN r.account_name LIKE '%Automotive%' THEN 'Automotive'
           WHEN r.account_name LIKE '%Education%' THEN 'Education'
           WHEN r.account_name LIKE '%Entertainment%' THEN 'Entertainment'
           WHEN r.account_name LIKE '%Fashion%' THEN 'Fashion'
           WHEN r.account_name LIKE '%Finance%' THEN 'Finance'
           WHEN r.account_name LIKE '%Food%' THEN 'Food'
           WHEN r.account_name LIKE '%Healthcare%' THEN 'Healthcare'
           WHEN r.account_name LIKE '%Real Estate%' THEN 'Real Estate'
           WHEN r.account_name LIKE '%Retail%' THEN 'Retail'
           WHEN r.account_name LIKE '%Sports%' THEN 'Sports'
           WHEN r.account_name LIKE '%Technology%' THEN 'Technology'
           WHEN r.account_name LIKE '%Travel%' THEN 'Travel'
           ELSE 'Other'
         END AS industry
  FROM google_ads__ad_group_report r
  GROUP BY r.ad_group_id
  HAVING SUM(r.clicks) > 0 AND SUM(r.impressions) > 0
)
SELECT industry,
       COUNT(*) AS total,
       SUM(CASE WHEN (ctr > 0.03587443946188341 AND cvr < 0.038461538461538464) THEN 1 ELSE 0 END) AS problem,
       ROUND(100.0*SUM(CASE WHEN (ctr > 0.03587443946188341 AND cvr < 0.038461538461538464) THEN 1 ELSE 0 END)/COUNT(*),1) AS problem_pct,
       ROUND(100.0*SUM(CASE WHEN (ctr > 0.03587443946188341 AND cvr < 0.038461538461538464) THEN clicks ELSE 0 END)/SUM(clicks),1) AS pct_clicks,
       ROUND(100.0*SUM(CASE WHEN (ctr > 0.03587443946188341 AND cvr < 0.038461538461538464) THEN spend ELSE 0 END)/SUM(spend),1) AS pct_spend
FROM master GROUP BY industry ORDER BY problem_pct DESC
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-059/attempt-01/sql/S41.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-059/attempt-01/sql/S41.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-059/attempt-01/results/S41.rows.jsonl)；完整：True；SHA256：`5526cfc4592aa477033ae146284d7b5d9ff9ec9d19ee73062a1d20b9f16174ad`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "r", "kind": "base", "block": null, "base_tables": ["google_ads__ad_group_report"]}] | [] | ["r.ad_group_id"] |
| B2 | [{"alias": "master", "kind": "derived", "block": "B1", "base_tables": ["google_ads__ad_group_report"]}] | [] | ["industry"] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | SUM(r.clicks) | [{"table": "google_ads__ad_group_report", "column": "clicks"}] | [] | False |
| B1 | SUM(r.impressions) | [{"table": "google_ads__ad_group_report", "column": "impressions"}] | [] | False |
| B1 | SUM(r.conversions) | [{"table": "google_ads__ad_group_report", "column": "conversions"}] | [] | False |
| B1 | SUM(r.spend) | [{"table": "google_ads__ad_group_report", "column": "spend"}] | [] | False |
| B1 | SUM(r.impressions) | [{"table": "google_ads__ad_group_report", "column": "impressions"}] | [] | False |
| B1 | SUM(r.clicks) | [{"table": "google_ads__ad_group_report", "column": "clicks"}] | [] | False |
| B1 | SUM(r.clicks) | [{"table": "google_ads__ad_group_report", "column": "clicks"}] | [] | False |
| B1 | SUM(r.conversions) | [{"table": "google_ads__ad_group_report", "column": "conversions"}] | [] | False |
| B1 | SUM(r.clicks) | [{"table": "google_ads__ad_group_report", "column": "clicks"}] | [] | False |
| B1 | SUM(r.impressions) | [{"table": "google_ads__ad_group_report", "column": "impressions"}] | [] | False |
| B2 | COUNT(*) | [] | [] | True |
| B2 | SUM(CASE WHEN (ctr > 0.03587443946188341 AND cvr < 0.038461538461538464) THEN 1 ELSE 0 END) | [] | [{"table": "google_ads__ad_group_report", "column": "impressions"}, {"table": "google_ads__ad_group_report", "column": "clicks"}, {"table": "google_ads__ad_group_report", "column": "clicks"}, {"table": "google_ads__ad_group_report", "column": "conversions"}] | False |
| B2 | COUNT(*) | [] | [] | True |
| B2 | SUM(clicks) | [{"table": "google_ads__ad_group_report", "column": "clicks"}] | [] | False |
| B2 | SUM(spend) | [{"table": "google_ads__ad_group_report", "column": "spend"}] | [] | False |
| B2 | SUM(CASE WHEN (ctr > 0.03587443946188341 AND cvr < 0.038461538461538464) THEN 1 ELSE 0 END) | [] | [{"table": "google_ads__ad_group_report", "column": "impressions"}, {"table": "google_ads__ad_group_report", "column": "clicks"}, {"table": "google_ads__ad_group_report", "column": "clicks"}, {"table": "google_ads__ad_group_report", "column": "conversions"}] | False |
| B2 | SUM(CASE WHEN (ctr > 0.03587443946188341 AND cvr < 0.038461538461538464) THEN clicks ELSE 0 END) | [{"table": "google_ads__ad_group_report", "column": "clicks"}] | [{"table": "google_ads__ad_group_report", "column": "impressions"}, {"table": "google_ads__ad_group_report", "column": "clicks"}, {"table": "google_ads__ad_group_report", "column": "clicks"}, {"table": "google_ads__ad_group_report", "column": "conversions"}] | False |
| B2 | SUM(CASE WHEN (ctr > 0.03587443946188341 AND cvr < 0.038461538461538464) THEN spend ELSE 0 END) | [{"table": "google_ads__ad_group_report", "column": "spend"}] | [{"table": "google_ads__ad_group_report", "column": "impressions"}, {"table": "google_ads__ad_group_report", "column": "clicks"}, {"table": "google_ads__ad_group_report", "column": "clicks"}, {"table": "google_ads__ad_group_report", "column": "conversions"}] | False |


## S42

类别 `data`；来源 `query_db`；调用 `d9bc475a04a44f0296099dd05818402a`；状态 `success`。

```sql
WITH master AS (
  SELECT r.ad_group_id, r.status, r.ad_group_type,
         SUM(r.clicks) AS clicks, SUM(r.impressions) AS impressions,
         SUM(r.conversions) AS conversions, SUM(r.spend) AS spend,
         SUM(r.clicks)*1.0/SUM(r.impressions) AS ctr,
         SUM(r.conversions)*1.0/SUM(r.clicks) AS cvr
  FROM google_ads__ad_group_report r
  GROUP BY r.ad_group_id
  HAVING SUM(r.clicks) > 0 AND SUM(r.impressions) > 0
)
SELECT status,
       SUM(CASE WHEN (ctr > 0.03587443946188341 AND cvr < 0.038461538461538464) THEN 1 ELSE 0 END) AS problem,
       SUM(CASE WHEN NOT (ctr > 0.03587443946188341 AND cvr < 0.038461538461538464) THEN 1 ELSE 0 END) AS non_problem,
       ROUND(100.0*SUM(CASE WHEN (ctr > 0.03587443946188341 AND cvr < 0.038461538461538464) THEN 1 ELSE 0 END)/COUNT(*),1) AS problem_pct
FROM master GROUP BY status ORDER BY problem_pct DESC
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-059/attempt-01/sql/S42.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-059/attempt-01/sql/S42.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-059/attempt-01/results/S42.rows.jsonl)；完整：True；SHA256：`5f7482280b5648f9fd8ecef88cefed1659843579ca68584b67d12b2b7d5d3a25`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "r", "kind": "base", "block": null, "base_tables": ["google_ads__ad_group_report"]}] | [] | ["r.ad_group_id"] |
| B2 | [{"alias": "master", "kind": "derived", "block": "B1", "base_tables": ["google_ads__ad_group_report"]}] | [] | ["status"] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | SUM(r.clicks) | [{"table": "google_ads__ad_group_report", "column": "clicks"}] | [] | False |
| B1 | SUM(r.impressions) | [{"table": "google_ads__ad_group_report", "column": "impressions"}] | [] | False |
| B1 | SUM(r.conversions) | [{"table": "google_ads__ad_group_report", "column": "conversions"}] | [] | False |
| B1 | SUM(r.spend) | [{"table": "google_ads__ad_group_report", "column": "spend"}] | [] | False |
| B1 | SUM(r.impressions) | [{"table": "google_ads__ad_group_report", "column": "impressions"}] | [] | False |
| B1 | SUM(r.clicks) | [{"table": "google_ads__ad_group_report", "column": "clicks"}] | [] | False |
| B1 | SUM(r.clicks) | [{"table": "google_ads__ad_group_report", "column": "clicks"}] | [] | False |
| B1 | SUM(r.conversions) | [{"table": "google_ads__ad_group_report", "column": "conversions"}] | [] | False |
| B1 | SUM(r.clicks) | [{"table": "google_ads__ad_group_report", "column": "clicks"}] | [] | False |
| B1 | SUM(r.impressions) | [{"table": "google_ads__ad_group_report", "column": "impressions"}] | [] | False |
| B2 | SUM(CASE WHEN (ctr > 0.03587443946188341 AND cvr < 0.038461538461538464) THEN 1 ELSE 0 END) | [] | [{"table": "google_ads__ad_group_report", "column": "impressions"}, {"table": "google_ads__ad_group_report", "column": "clicks"}, {"table": "google_ads__ad_group_report", "column": "clicks"}, {"table": "google_ads__ad_group_report", "column": "conversions"}] | False |
| B2 | SUM(CASE WHEN NOT (ctr > 0.03587443946188341 AND cvr < 0.038461538461538464) THEN 1 ELSE 0 END) | [] | [{"table": "google_ads__ad_group_report", "column": "impressions"}, {"table": "google_ads__ad_group_report", "column": "clicks"}, {"table": "google_ads__ad_group_report", "column": "clicks"}, {"table": "google_ads__ad_group_report", "column": "conversions"}] | False |
| B2 | COUNT(*) | [] | [] | True |
| B2 | SUM(CASE WHEN (ctr > 0.03587443946188341 AND cvr < 0.038461538461538464) THEN 1 ELSE 0 END) | [] | [{"table": "google_ads__ad_group_report", "column": "impressions"}, {"table": "google_ads__ad_group_report", "column": "clicks"}, {"table": "google_ads__ad_group_report", "column": "clicks"}, {"table": "google_ads__ad_group_report", "column": "conversions"}] | False |


## S43

类别 `data`；来源 `query_db`；调用 `d5da6caec2f142cdbaa72a103448e71f`；状态 `success`。

```sql
SELECT 
  (SELECT SUM(clicks) FROM google_ads__ad_group_report) AS ag_clicks,
  (SELECT SUM(clicks) FROM google_ads__keyword_report) AS kw_clicks,
  (SELECT SUM(impressions) FROM google_ads__ad_group_report) AS ag_imp,
  (SELECT SUM(impressions) FROM google_ads__keyword_report) AS kw_imp,
  (SELECT SUM(conversions) FROM google_ads__ad_group_report) AS ag_conv,
  (SELECT SUM(conversions) FROM google_ads__keyword_report) AS kw_conv
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-059/attempt-01/sql/S43.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-059/attempt-01/sql/S43.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-059/attempt-01/results/S43.rows.jsonl)；完整：True；SHA256：`05f26b8bbdb5ae9a0a93e4734f7e78df1e5ca8dae3d8f1190a1cce15587efadb`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "google_ads__ad_group_report", "kind": "base", "block": null, "base_tables": ["google_ads__ad_group_report"]}] | [] | [] |
| B2 | [{"alias": "google_ads__keyword_report", "kind": "base", "block": null, "base_tables": ["google_ads__keyword_report"]}] | [] | [] |
| B3 | [{"alias": "google_ads__ad_group_report", "kind": "base", "block": null, "base_tables": ["google_ads__ad_group_report"]}] | [] | [] |
| B4 | [{"alias": "google_ads__keyword_report", "kind": "base", "block": null, "base_tables": ["google_ads__keyword_report"]}] | [] | [] |
| B5 | [{"alias": "google_ads__ad_group_report", "kind": "base", "block": null, "base_tables": ["google_ads__ad_group_report"]}] | [] | [] |
| B6 | [{"alias": "google_ads__keyword_report", "kind": "base", "block": null, "base_tables": ["google_ads__keyword_report"]}] | [] | [] |
| B7 | [] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | SUM(clicks) | [{"table": "google_ads__ad_group_report", "column": "clicks"}] | [] | False |
| B2 | SUM(clicks) | [{"table": "google_ads__keyword_report", "column": "clicks"}] | [] | False |
| B3 | SUM(impressions) | [{"table": "google_ads__ad_group_report", "column": "impressions"}] | [] | False |
| B4 | SUM(impressions) | [{"table": "google_ads__keyword_report", "column": "impressions"}] | [] | False |
| B5 | SUM(conversions) | [{"table": "google_ads__ad_group_report", "column": "conversions"}] | [] | False |
| B6 | SUM(conversions) | [{"table": "google_ads__keyword_report", "column": "conversions"}] | [] | False |


未解析列血缘：[{"block": "B7", "column": "clicks", "reason": "ambiguous_or_missing_source"}, {"block": "B7", "column": "clicks", "reason": "ambiguous_or_missing_source"}, {"block": "B7", "column": "impressions", "reason": "ambiguous_or_missing_source"}, {"block": "B7", "column": "impressions", "reason": "ambiguous_or_missing_source"}, {"block": "B7", "column": "conversions", "reason": "ambiguous_or_missing_source"}, {"block": "B7", "column": "conversions", "reason": "ambiguous_or_missing_source"}]

## S44

类别 `data`；来源 `query_db`；调用 `d48bbfa08baa46f3b358a53a8ea650c9`；状态 `success`。

```sql
WITH flag AS (
  SELECT ad_group_id,
         (SUM(clicks)*1.0/SUM(impressions) > 0.03587443946188341 AND SUM(conversions)*1.0/SUM(clicks) < 0.038461538461538464) AS is_problem
  FROM google_ads__ad_group_report
  GROUP BY ad_group_id
  HAVING SUM(clicks) > 0 AND SUM(impressions) > 0
)
SELECT f.is_problem, k.keyword_match_type, COUNT(*) AS kw_rows, ROUND(SUM(k.clicks),0) AS clicks, ROUND(SUM(k.impressions),0) AS imp, ROUND(SUM(k.conversions),2) AS conv, ROUND(SUM(k.spend),2) AS spend
FROM google_ads__keyword_report k JOIN flag f ON k.ad_group_id = f.ad_group_id
GROUP BY f.is_problem, k.keyword_match_type
ORDER BY f.is_problem, k.keyword_match_type
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-059/attempt-01/sql/S44.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-059/attempt-01/sql/S44.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-059/attempt-01/results/S44.rows.jsonl)；完整：True；SHA256：`7831056196eacfec99573a6a3cc227215cb5730f6df444f5253d4ac8b42af5ef`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "google_ads__ad_group_report", "kind": "base", "block": null, "base_tables": ["google_ads__ad_group_report"]}] | [] | ["ad_group_id"] |
| B2 | [{"alias": "k", "kind": "base", "block": null, "base_tables": ["google_ads__keyword_report"]}, {"alias": "f", "kind": "derived", "block": "B1", "base_tables": ["google_ads__ad_group_report"]}] | [{"type": "INNER", "right": "flag AS f", "on": "k.ad_group_id = f.ad_group_id", "using": []}] | ["f.is_problem", "k.keyword_match_type"] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | SUM(clicks) | [{"table": "google_ads__ad_group_report", "column": "clicks"}] | [] | False |
| B1 | SUM(impressions) | [{"table": "google_ads__ad_group_report", "column": "impressions"}] | [] | False |
| B1 | SUM(impressions) | [{"table": "google_ads__ad_group_report", "column": "impressions"}] | [] | False |
| B1 | SUM(clicks) | [{"table": "google_ads__ad_group_report", "column": "clicks"}] | [] | False |
| B1 | SUM(clicks) | [{"table": "google_ads__ad_group_report", "column": "clicks"}] | [] | False |
| B1 | SUM(conversions) | [{"table": "google_ads__ad_group_report", "column": "conversions"}] | [] | False |
| B2 | COUNT(*) | [] | [] | True |
| B2 | SUM(k.clicks) | [{"table": "google_ads__keyword_report", "column": "clicks"}] | [] | False |
| B2 | SUM(k.impressions) | [{"table": "google_ads__keyword_report", "column": "impressions"}] | [] | False |
| B2 | SUM(k.conversions) | [{"table": "google_ads__keyword_report", "column": "conversions"}] | [] | False |
| B2 | SUM(k.spend) | [{"table": "google_ads__keyword_report", "column": "spend"}] | [] | False |


## S45

类别 `data`；来源 `query_db`；调用 `76f448b186cd4a3ea8c72f678a84517e`；状态 `success`。

```sql
SELECT keyword_text, keyword_match_type FROM google_ads__keyword_report GROUP BY keyword_text ORDER BY keyword_text LIMIT 100
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-059/attempt-01/sql/S45.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-059/attempt-01/sql/S45.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-059/attempt-01/results/S45.rows.jsonl)；完整：True；SHA256：`55c85f073018406976fd4f4ab5836cf217e56808eb343be0133305713b8266d6`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "google_ads__keyword_report", "kind": "base", "block": null, "base_tables": ["google_ads__keyword_report"]}] | [] | ["keyword_text"] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |


## S46

类别 `data`；来源 `query_db`；调用 `d9399d4fe1a84f1db760b84c1d780fb6`；状态 `success`。

```sql
SELECT DISTINCT keyword_text FROM google_ads__keyword_report ORDER BY keyword_text LIMIT 200
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-059/attempt-01/sql/S46.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-059/attempt-01/sql/S46.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-059/attempt-01/results/S46.rows.jsonl)；完整：True；SHA256：`0958f4ef5b146e899cabb1de38b595941b7d31bf0fefedc099dc15b02350fd05`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "google_ads__keyword_report", "kind": "base", "block": null, "base_tables": ["google_ads__keyword_report"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |


## S47

类别 `data`；来源 `query_db`；调用 `fc8e272bcaa54f958403a388e913391c`；状态 `success`。

```sql
SELECT DISTINCT keyword_text FROM google_ads__keyword_report WHERE keyword_text NOT LIKE '% %' ORDER BY keyword_text
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-059/attempt-01/sql/S47.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-059/attempt-01/sql/S47.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-059/attempt-01/results/S47.rows.jsonl)；完整：True；SHA256：`86025c2a71621a8afb4a0b3a87ac586403a1ad7a6c776fc52fa25ad75eb11037`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "google_ads__keyword_report", "kind": "base", "block": null, "base_tables": ["google_ads__keyword_report"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |


## S48

类别 `data`；来源 `query_db`；调用 `a18493cc45db442bb177ca44929494e2`；状态 `success`。

```sql
SELECT COUNT(DISTINCT keyword_text) AS unique_keywords, COUNT(*) AS total_rows FROM google_ads__keyword_report
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-059/attempt-01/sql/S48.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-059/attempt-01/sql/S48.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-059/attempt-01/results/S48.rows.jsonl)；完整：True；SHA256：`f78ee798efc9aa99acd1edd3a2c99e931b88e3ef1343abba04d4300fcaedb71c`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "google_ads__keyword_report", "kind": "base", "block": null, "base_tables": ["google_ads__keyword_report"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(DISTINCT keyword_text) | [{"table": "google_ads__keyword_report", "column": "keyword_text"}] | [] | False |
| B1 | COUNT(*) | [] | [] | True |


## S49

类别 `data`；来源 `python`；调用 `54a5ab73f5eb475aafcdeedf1b6735ff`；状态 `success`。

```sql

    WITH agg AS (
      SELECT r.ad_group_id, r.account_name, r.campaign_name, r.status, r.ad_group_type,
             SUM(r.clicks) AS clicks, SUM(r.impressions) AS impressions,
             SUM(r.conversions) AS conversions, SUM(r.spend) AS spend,
             SUM(r.clicks)*1.0/SUM(r.impressions) AS ctr,
             SUM(r.conversions)*1.0/SUM(r.clicks) AS cvr,
             CASE
               WHEN r.account_name LIKE '%Automotive%' THEN 'Automotive'
               WHEN r.account_name LIKE '%Education%' THEN 'Education'
               WHEN r.account_name LIKE '%Entertainment%' THEN 'Entertainment'
               WHEN r.account_name LIKE '%Fashion%' THEN 'Fashion'
               WHEN r.account_name LIKE '%Finance%' THEN 'Finance'
               WHEN r.account_name LIKE '%Food%' THEN 'Food'
               WHEN r.account_name LIKE '%Healthcare%' THEN 'Healthcare'
               WHEN r.account_name LIKE '%Real Estate%' THEN 'Real Estate'
               WHEN r.account_name LIKE '%Retail%' THEN 'Retail'
               WHEN r.account_name LIKE '%Sports%' THEN 'Sports'
               WHEN r.account_name LIKE '%Technology%' THEN 'Technology'
               WHEN r.account_name LIKE '%Travel%' THEN 'Travel'
               ELSE 'Other'
             END AS industry,
             CASE
               WHEN r.campaign_name LIKE 'Brand%' THEN 'Brand'
               WHEN r.campaign_name LIKE 'Display%' THEN 'Display'
               WHEN r.campaign_name LIKE 'Performance%' THEN 'Performance'
               WHEN r.campaign_name LIKE 'Search%' THEN 'Search'
               WHEN r.campaign_name LIKE 'Shopping%' THEN 'Shopping'
             END AS channel,
             CASE
               WHEN r.campaign_name LIKE '% Audience%' THEN 'Audience'
               WHEN r.campaign_name LIKE '% Broad%' THEN 'Broad'
               WHEN r.campaign_name LIKE '% Exact%' THEN 'Exact'
               WHEN r.campaign_name LIKE '% Keywords%' THEN 'Keywords'
               WHEN r.campaign_name LIKE '% Remarketing%' THEN 'Remarketing'
             END AS strategy,
             ltrim(substr(r.campaign_name, instr(r.campaign_name,' -')+2)) AS period
      FROM google_ads__ad_group_report r
      GROUP BY r.ad_group_id
      HAVING SUM(r.clicks) > 0 AND SUM(r.impressions) > 0
    )
    SELECT * FROM agg

```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-059/attempt-01/sql/S49.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-059/attempt-01/sql/S49.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-059/attempt-01/results/S49.rows.jsonl)；完整：True；SHA256：`a0d274169ab507198dd4eb5ef0f30f5c495f9e0f9d21e7ee91f15f0fffa92bec`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "r", "kind": "base", "block": null, "base_tables": ["google_ads__ad_group_report"]}] | [] | ["r.ad_group_id"] |
| B2 | [{"alias": "agg", "kind": "derived", "block": "B1", "base_tables": ["google_ads__ad_group_report"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | SUM(r.clicks) | [{"table": "google_ads__ad_group_report", "column": "clicks"}] | [] | False |
| B1 | SUM(r.impressions) | [{"table": "google_ads__ad_group_report", "column": "impressions"}] | [] | False |
| B1 | SUM(r.conversions) | [{"table": "google_ads__ad_group_report", "column": "conversions"}] | [] | False |
| B1 | SUM(r.spend) | [{"table": "google_ads__ad_group_report", "column": "spend"}] | [] | False |
| B1 | SUM(r.impressions) | [{"table": "google_ads__ad_group_report", "column": "impressions"}] | [] | False |
| B1 | SUM(r.clicks) | [{"table": "google_ads__ad_group_report", "column": "clicks"}] | [] | False |
| B1 | SUM(r.clicks) | [{"table": "google_ads__ad_group_report", "column": "clicks"}] | [] | False |
| B1 | SUM(r.conversions) | [{"table": "google_ads__ad_group_report", "column": "conversions"}] | [] | False |
| B1 | SUM(r.clicks) | [{"table": "google_ads__ad_group_report", "column": "clicks"}] | [] | False |
| B1 | SUM(r.impressions) | [{"table": "google_ads__ad_group_report", "column": "impressions"}] | [] | False |


## S50

类别 `data`；来源 `python`；调用 `042bcb3a504c42b0b6596d870910fd1b`；状态 `success`。

```sql
SELECT ad_group_id, SUM(clicks) AS clicks FROM google_ads__ad_group_report GROUP BY ad_group_id LIMIT 3
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-059/attempt-01/sql/S50.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-059/attempt-01/sql/S50.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-059/attempt-01/results/S50.rows.jsonl)；完整：True；SHA256：`ef0f5ba580a0835f2fec35ef60e4ba90c4923ec5e6f1d83ff9feea554c11af83`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "google_ads__ad_group_report", "kind": "base", "block": null, "base_tables": ["google_ads__ad_group_report"]}] | [] | ["ad_group_id"] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | SUM(clicks) | [{"table": "google_ads__ad_group_report", "column": "clicks"}] | [] | False |


## S51

类别 `data`；来源 `python`；调用 `71119ebf83a94c3496178bea82f32ae7`；状态 `success`。

```sql

    WITH agg AS (
      SELECT r.ad_group_id, r.account_name, r.campaign_name, r.status, r.ad_group_type,
             SUM(r.clicks) AS clicks, SUM(r.impressions) AS impressions,
             SUM(r.conversions) AS conversions, SUM(r.spend) AS spend,
             SUM(r.clicks)*1.0/SUM(r.impressions) AS ctr,
             SUM(r.conversions)*1.0/SUM(r.clicks) AS cvr,
             CASE
               WHEN r.account_name LIKE '%Automotive%' THEN 'Automotive'
               WHEN r.account_name LIKE '%Education%' THEN 'Education'
               WHEN r.account_name LIKE '%Entertainment%' THEN 'Entertainment'
               WHEN r.account_name LIKE '%Fashion%' THEN 'Fashion'
               WHEN r.account_name LIKE '%Finance%' THEN 'Finance'
               WHEN r.account_name LIKE '%Food%' THEN 'Food'
               WHEN r.account_name LIKE '%Healthcare%' THEN 'Healthcare'
               WHEN r.account_name LIKE '%Real Estate%' THEN 'Real Estate'
               WHEN r.account_name LIKE '%Retail%' THEN 'Retail'
               WHEN r.account_name LIKE '%Sports%' THEN 'Sports'
               WHEN r.account_name LIKE '%Technology%' THEN 'Technology'
               WHEN r.account_name LIKE '%Travel%' THEN 'Travel'
               ELSE 'Other'
             END AS industry,
             CASE
               WHEN r.campaign_name LIKE 'Brand%' THEN 'Brand'
               WHEN r.campaign_name LIKE 'Display%' THEN 'Display'
               WHEN r.campaign_name LIKE 'Performance%' THEN 'Performance'
               WHEN r.campaign_name LIKE 'Search%' THEN 'Search'
               WHEN r.campaign_name LIKE 'Shopping%' THEN 'Shopping'
             END AS channel,
             CASE
               WHEN r.campaign_name LIKE '% Audience%' THEN 'Audience'
               WHEN r.campaign_name LIKE '% Broad%' THEN 'Broad'
               WHEN r.campaign_name LIKE '% Exact%' THEN 'Exact'
               WHEN r.campaign_name LIKE '% Keywords%' THEN 'Keywords'
               WHEN r.campaign_name LIKE '% Remarketing%' THEN 'Remarketing'
             END AS strategy,
             ltrim(substr(r.campaign_name, instr(r.campaign_name,' -')+2)) AS period
      FROM google_ads__ad_group_report r
      GROUP BY r.ad_group_id
      HAVING SUM(r.clicks) > 0 AND SUM(r.impressions) > 0
    )
    SELECT * FROM agg

```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-059/attempt-01/sql/S51.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-059/attempt-01/sql/S51.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-059/attempt-01/results/S51.rows.jsonl)；完整：True；SHA256：`a0d274169ab507198dd4eb5ef0f30f5c495f9e0f9d21e7ee91f15f0fffa92bec`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "r", "kind": "base", "block": null, "base_tables": ["google_ads__ad_group_report"]}] | [] | ["r.ad_group_id"] |
| B2 | [{"alias": "agg", "kind": "derived", "block": "B1", "base_tables": ["google_ads__ad_group_report"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | SUM(r.clicks) | [{"table": "google_ads__ad_group_report", "column": "clicks"}] | [] | False |
| B1 | SUM(r.impressions) | [{"table": "google_ads__ad_group_report", "column": "impressions"}] | [] | False |
| B1 | SUM(r.conversions) | [{"table": "google_ads__ad_group_report", "column": "conversions"}] | [] | False |
| B1 | SUM(r.spend) | [{"table": "google_ads__ad_group_report", "column": "spend"}] | [] | False |
| B1 | SUM(r.impressions) | [{"table": "google_ads__ad_group_report", "column": "impressions"}] | [] | False |
| B1 | SUM(r.clicks) | [{"table": "google_ads__ad_group_report", "column": "clicks"}] | [] | False |
| B1 | SUM(r.clicks) | [{"table": "google_ads__ad_group_report", "column": "clicks"}] | [] | False |
| B1 | SUM(r.conversions) | [{"table": "google_ads__ad_group_report", "column": "conversions"}] | [] | False |
| B1 | SUM(r.clicks) | [{"table": "google_ads__ad_group_report", "column": "clicks"}] | [] | False |
| B1 | SUM(r.impressions) | [{"table": "google_ads__ad_group_report", "column": "impressions"}] | [] | False |


## S52

类别 `data`；来源 `python`；调用 `71119ebf83a94c3496178bea82f32ae7`；状态 `success`。

```sql

    SELECT k.ad_group_id, k.keyword_text, k.keyword_match_type, k.clicks, k.impressions, k.conversions, k.spend
    FROM google_ads__keyword_report k

```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-059/attempt-01/sql/S52.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-059/attempt-01/sql/S52.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-059/attempt-01/results/S52.rows.jsonl)；完整：True；SHA256：`ec5dc40f155f534d5b5eaa93a2d2019e26dd95d64e8fed76ebafc740bdcfe079`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "k", "kind": "base", "block": null, "base_tables": ["google_ads__keyword_report"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |


## S53

类别 `data`；来源 `python`；调用 `d0e71db9c71940a4bc4e4affdb8ff710`；状态 `success`。

```sql

    WITH agg AS (
      SELECT r.ad_group_id, r.account_name, r.campaign_name, r.status, r.ad_group_type,
             SUM(r.clicks) AS clicks, SUM(r.impressions) AS impressions,
             SUM(r.conversions) AS conversions, SUM(r.spend) AS spend,
             SUM(r.clicks)*1.0/SUM(r.impressions) AS ctr,
             SUM(r.conversions)*1.0/SUM(r.clicks) AS cvr,
             CASE
               WHEN r.account_name LIKE '%Automotive%' THEN 'Automotive'
               WHEN r.account_name LIKE '%Education%' THEN 'Education'
               WHEN r.account_name LIKE '%Entertainment%' THEN 'Entertainment'
               WHEN r.account_name LIKE '%Fashion%' THEN 'Fashion'
               WHEN r.account_name LIKE '%Finance%' THEN 'Finance'
               WHEN r.account_name LIKE '%Food%' THEN 'Food'
               WHEN r.account_name LIKE '%Healthcare%' THEN 'Healthcare'
               WHEN r.account_name LIKE '%Real Estate%' THEN 'Real Estate'
               WHEN r.account_name LIKE '%Retail%' THEN 'Retail'
               WHEN r.account_name LIKE '%Sports%' THEN 'Sports'
               WHEN r.account_name LIKE '%Technology%' THEN 'Technology'
               WHEN r.account_name LIKE '%Travel%' THEN 'Travel'
               ELSE 'Other'
             END AS industry,
             CASE
               WHEN r.campaign_name LIKE 'Brand%' THEN 'Brand'
               WHEN r.campaign_name LIKE 'Display%' THEN 'Display'
               WHEN r.campaign_name LIKE 'Performance%' THEN 'Performance'
               WHEN r.campaign_name LIKE 'Search%' THEN 'Search'
               WHEN r.campaign_name LIKE 'Shopping%' THEN 'Shopping'
             END AS channel,
             CASE
               WHEN r.campaign_name LIKE '% Audience%' THEN 'Audience'
               WHEN r.campaign_name LIKE '% Broad%' THEN 'Broad'
               WHEN r.campaign_name LIKE '% Exact%' THEN 'Exact'
               WHEN r.campaign_name LIKE '% Keywords%' THEN 'Keywords'
               WHEN r.campaign_name LIKE '% Remarketing%' THEN 'Remarketing'
             END AS strategy,
             ltrim(substr(r.campaign_name, instr(r.campaign_name,' -')+2)) AS period
      FROM google_ads__ad_group_report r
      GROUP BY r.ad_group_id
      HAVING SUM(r.clicks) > 0 AND SUM(r.impressions) > 0
    )
    SELECT * FROM agg

```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-059/attempt-01/sql/S53.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-059/attempt-01/sql/S53.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-059/attempt-01/results/S53.rows.jsonl)；完整：True；SHA256：`a0d274169ab507198dd4eb5ef0f30f5c495f9e0f9d21e7ee91f15f0fffa92bec`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "r", "kind": "base", "block": null, "base_tables": ["google_ads__ad_group_report"]}] | [] | ["r.ad_group_id"] |
| B2 | [{"alias": "agg", "kind": "derived", "block": "B1", "base_tables": ["google_ads__ad_group_report"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | SUM(r.clicks) | [{"table": "google_ads__ad_group_report", "column": "clicks"}] | [] | False |
| B1 | SUM(r.impressions) | [{"table": "google_ads__ad_group_report", "column": "impressions"}] | [] | False |
| B1 | SUM(r.conversions) | [{"table": "google_ads__ad_group_report", "column": "conversions"}] | [] | False |
| B1 | SUM(r.spend) | [{"table": "google_ads__ad_group_report", "column": "spend"}] | [] | False |
| B1 | SUM(r.impressions) | [{"table": "google_ads__ad_group_report", "column": "impressions"}] | [] | False |
| B1 | SUM(r.clicks) | [{"table": "google_ads__ad_group_report", "column": "clicks"}] | [] | False |
| B1 | SUM(r.clicks) | [{"table": "google_ads__ad_group_report", "column": "clicks"}] | [] | False |
| B1 | SUM(r.conversions) | [{"table": "google_ads__ad_group_report", "column": "conversions"}] | [] | False |
| B1 | SUM(r.clicks) | [{"table": "google_ads__ad_group_report", "column": "clicks"}] | [] | False |
| B1 | SUM(r.impressions) | [{"table": "google_ads__ad_group_report", "column": "impressions"}] | [] | False |


## S54

类别 `data`；来源 `python`；调用 `d0e71db9c71940a4bc4e4affdb8ff710`；状态 `success`。

```sql

    SELECT k.ad_group_id, k.keyword_text, k.keyword_match_type, k.clicks, k.impressions, k.conversions, k.spend
    FROM google_ads__keyword_report k

```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-059/attempt-01/sql/S54.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-059/attempt-01/sql/S54.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-059/attempt-01/results/S54.rows.jsonl)；完整：True；SHA256：`ec5dc40f155f534d5b5eaa93a2d2019e26dd95d64e8fed76ebafc740bdcfe079`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "k", "kind": "base", "block": null, "base_tables": ["google_ads__keyword_report"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |


## S55

类别 `data`；来源 `python`；调用 `dcb8b6589d68420b8a1438636f5e8625`；状态 `success`。

```sql

    WITH agg AS (
      SELECT r.ad_group_id, r.account_name, r.campaign_name, r.status, r.ad_group_type,
             SUM(r.clicks) AS clicks, SUM(r.impressions) AS impressions,
             SUM(r.conversions) AS conversions, SUM(r.spend) AS spend,
             SUM(r.clicks)*1.0/SUM(r.impressions) AS ctr,
             SUM(r.conversions)*1.0/SUM(r.clicks) AS cvr,
             CASE
               WHEN r.account_name LIKE '%Automotive%' THEN 'Automotive'
               WHEN r.account_name LIKE '%Education%' THEN 'Education'
               WHEN r.account_name LIKE '%Entertainment%' THEN 'Entertainment'
               WHEN r.account_name LIKE '%Fashion%' THEN 'Fashion'
               WHEN r.account_name LIKE '%Finance%' THEN 'Finance'
               WHEN r.account_name LIKE '%Food%' THEN 'Food'
               WHEN r.account_name LIKE '%Healthcare%' THEN 'Healthcare'
               WHEN r.account_name LIKE '%Real Estate%' THEN 'Real Estate'
               WHEN r.account_name LIKE '%Retail%' THEN 'Retail'
               WHEN r.account_name LIKE '%Sports%' THEN 'Sports'
               WHEN r.account_name LIKE '%Technology%' THEN 'Technology'
               WHEN r.account_name LIKE '%Travel%' THEN 'Travel'
               ELSE 'Other'
             END AS industry,
             CASE
               WHEN r.campaign_name LIKE 'Brand%' THEN 'Brand'
               WHEN r.campaign_name LIKE 'Display%' THEN 'Display'
               WHEN r.campaign_name LIKE 'Performance%' THEN 'Performance'
               WHEN r.campaign_name LIKE 'Search%' THEN 'Search'
               WHEN r.campaign_name LIKE 'Shopping%' THEN 'Shopping'
             END AS channel,
             CASE
               WHEN r.campaign_name LIKE '% Audience%' THEN 'Audience'
               WHEN r.campaign_name LIKE '% Broad%' THEN 'Broad'
               WHEN r.campaign_name LIKE '% Exact%' THEN 'Exact'
               WHEN r.campaign_name LIKE '% Keywords%' THEN 'Keywords'
               WHEN r.campaign_name LIKE '% Remarketing%' THEN 'Remarketing'
             END AS strategy,
             ltrim(substr(r.campaign_name, instr(r.campaign_name,' -')+2)) AS period
      FROM google_ads__ad_group_report r
      GROUP BY r.ad_group_id
      HAVING SUM(r.clicks) > 0 AND SUM(r.impressions) > 0
    )
    SELECT * FROM agg

```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-059/attempt-01/sql/S55.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-059/attempt-01/sql/S55.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-059/attempt-01/results/S55.rows.jsonl)；完整：True；SHA256：`a0d274169ab507198dd4eb5ef0f30f5c495f9e0f9d21e7ee91f15f0fffa92bec`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "r", "kind": "base", "block": null, "base_tables": ["google_ads__ad_group_report"]}] | [] | ["r.ad_group_id"] |
| B2 | [{"alias": "agg", "kind": "derived", "block": "B1", "base_tables": ["google_ads__ad_group_report"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | SUM(r.clicks) | [{"table": "google_ads__ad_group_report", "column": "clicks"}] | [] | False |
| B1 | SUM(r.impressions) | [{"table": "google_ads__ad_group_report", "column": "impressions"}] | [] | False |
| B1 | SUM(r.conversions) | [{"table": "google_ads__ad_group_report", "column": "conversions"}] | [] | False |
| B1 | SUM(r.spend) | [{"table": "google_ads__ad_group_report", "column": "spend"}] | [] | False |
| B1 | SUM(r.impressions) | [{"table": "google_ads__ad_group_report", "column": "impressions"}] | [] | False |
| B1 | SUM(r.clicks) | [{"table": "google_ads__ad_group_report", "column": "clicks"}] | [] | False |
| B1 | SUM(r.clicks) | [{"table": "google_ads__ad_group_report", "column": "clicks"}] | [] | False |
| B1 | SUM(r.conversions) | [{"table": "google_ads__ad_group_report", "column": "conversions"}] | [] | False |
| B1 | SUM(r.clicks) | [{"table": "google_ads__ad_group_report", "column": "clicks"}] | [] | False |
| B1 | SUM(r.impressions) | [{"table": "google_ads__ad_group_report", "column": "impressions"}] | [] | False |


## S56

类别 `data`；来源 `python`；调用 `dcb8b6589d68420b8a1438636f5e8625`；状态 `success`。

```sql

    SELECT k.ad_group_id, k.keyword_text, k.keyword_match_type, k.clicks, k.impressions, k.conversions, k.spend
    FROM google_ads__keyword_report k

```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-059/attempt-01/sql/S56.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-059/attempt-01/sql/S56.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-059/attempt-01/results/S56.rows.jsonl)；完整：True；SHA256：`ec5dc40f155f534d5b5eaa93a2d2019e26dd95d64e8fed76ebafc740bdcfe079`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "k", "kind": "base", "block": null, "base_tables": ["google_ads__keyword_report"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |


## S57

类别 `data`；来源 `python`；调用 `d43030aa601e45758b5c6eaa883d5e1a`；状态 `success`。

```sql

    SELECT ad_group_id, SUM(conversions_value) AS conv_value, SUM(conversions) AS conv
    FROM google_ads__ad_group_report
    GROUP BY ad_group_id
    HAVING SUM(clicks) > 0 AND SUM(impressions) > 0

```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-059/attempt-01/sql/S57.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-059/attempt-01/sql/S57.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-059/attempt-01/results/S57.rows.jsonl)；完整：True；SHA256：`fd51d6c3409409a4548981b70b69348e4cd453eac774bd802ecc0b088708bf54`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "google_ads__ad_group_report", "kind": "base", "block": null, "base_tables": ["google_ads__ad_group_report"]}] | [] | ["ad_group_id"] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | SUM(conversions_value) | [{"table": "google_ads__ad_group_report", "column": "conversions_value"}] | [] | False |
| B1 | SUM(conversions) | [{"table": "google_ads__ad_group_report", "column": "conversions"}] | [] | False |
| B1 | SUM(clicks) | [{"table": "google_ads__ad_group_report", "column": "clicks"}] | [] | False |
| B1 | SUM(impressions) | [{"table": "google_ads__ad_group_report", "column": "impressions"}] | [] | False |


## S58

类别 `data`；来源 `python`；调用 `4357a0a733fe413caab61f9368dbef30`；状态 `success`。

```sql
SELECT ad_group_id, SUM(conversions_value) AS conv_value FROM google_ads__ad_group_report GROUP BY ad_group_id
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-059/attempt-01/sql/S58.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-059/attempt-01/sql/S58.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-059/attempt-01/results/S58.rows.jsonl)；完整：True；SHA256：`0a09583edec210334ea5c26945418edbe854cafd00eff2855a4393c6bc649a18`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "google_ads__ad_group_report", "kind": "base", "block": null, "base_tables": ["google_ads__ad_group_report"]}] | [] | ["ad_group_id"] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | SUM(conversions_value) | [{"table": "google_ads__ad_group_report", "column": "conversions_value"}] | [] | False |

