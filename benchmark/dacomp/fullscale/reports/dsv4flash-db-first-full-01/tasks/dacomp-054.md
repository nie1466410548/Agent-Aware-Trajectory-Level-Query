# dacomp-054

We have identified a group of customers exhibiting specific conversion behaviors: their `m…

运行：已提交。官方未评分。全部 SQL 尝试/成功 96/93；数据 SQL 93/90；Python 14 次。

完整原题：

We have identified a group of customers exhibiting specific conversion behaviors: their `marketing_to_sales_days` is between 10 and 20 days, `sales_to_support_days` exceeds 30 days, and their `composite_engagement_score` is higher than the average for all customers. Please conduct an analysis of this cohort: first, calculate the specific count of this group, the average scores for the three RFM dimensions, the average difference in their `estimated_customer_ltv` compared to other customers in the same `customer_tier`, the distribution of their `primary_engagement_channel`, and the proportion of their `zendesk_active` status. Then, deeply explore their geographical distribution characteristics (by `country` and `state`), analyze the impact of their multi-platform engagement patterns (combinations of `in_marketo`, `in_stripe`, `in_zendesk`) on `customer_health_score`, and design a framework for customer value assessment and risk identification based on metrics such as `activity_risk_level` and `engagement_velocity`.

| 表 | 行数 | 列数 |
| --- | --- | --- |
| customer360__address | 90069 | 14 |
| customer360__conversion_funnel_analysis | 441119 | 43 |
| customer360__customer_activity_metrics | 6947 | 57 |
| customer360__customer_value_analysis | 5001 | 37 |


实际路线（分析者依据 SQL/源码概括，不代表 Agent 自述）：SQL 识别特定转化时长与互动分数客户 → Python 统计检验、平台分组汇总及交叉计数 → 地域与风险图表。

数据库大小：221,306,880 字节。

## 数据 SQL

| SQL | 状态 | 基础表 | Join 输入/类型 | GROUP BY | 聚合表达式 | 结果行数 | 数据库 ms |
| --- | --- | --- | --- | --- | --- | --- | --- |
| [S3/Q1](#s3) | success | ["customer360__customer_activity_metrics"] | 0 / {} | [] | ["COUNT(*)"] | 1 | 2.321 |
| [S4/Q2](#s4) | success | ["customer360__conversion_funnel_analysis"] | 0 / {} | [] | ["COUNT(*)"] | 1 | 56.141 |
| [S5/Q3](#s5) | success | ["customer360__customer_value_analysis"] | 0 / {} | [] | ["COUNT(*)"] | 1 | 1.038 |
| [S6/Q4](#s6) | success | ["customer360__address"] | 0 / {} | [] | ["COUNT(*)"] | 1 | 4.234 |
| [S7/Q5](#s7) | success | ["customer360__customer_activity_metrics"] | 0 / {} | [] | ["AVG(composite_engagement_score)"] | 1 | 2.025 |
| [S8/Q6](#s8) | success | ["customer360__conversion_funnel_analysis"] | 0 / {} | [] | [] | 5 | 192.498 |
| [S9/Q7](#s9) | success | ["customer360__customer_activity_metrics"] | 0 / {} | [] | [] | 9 | 3.506 |
| [S10/Q8](#s10) | success | ["customer360__conversion_funnel_analysis", "customer360__customer_activity_metrics"] | 2 / {'INNER': 1} | [] | ["COUNT(*)"] | 1 | 3621.362 |
| [S11/Q9](#s11) | success | ["customer360__conversion_funnel_analysis", "customer360__customer_value_analysis"] | 2 / {'INNER': 1} | [] | ["COUNT(*)"] | 1 | 323.706 |
| [S12/Q10](#s12) | success | ["customer360__customer_activity_metrics"] | 0 / {} | [] | ["COUNT(DISTINCT marketo_lead_id)"] | 1 | 4.502 |
| [S13/Q11](#s13) | success | ["customer360__conversion_funnel_analysis"] | 0 / {} | [] | ["COUNT(DISTINCT marketo_lead_id)"] | 1 | 131.497 |
| [S14/Q12](#s14) | success | ["customer360__customer_value_analysis"] | 0 / {} | [] | ["COUNT(DISTINCT marketo_lead_id)"] | 1 | 3.7 |
| [S15/Q13](#s15) | success | ["customer360__customer_activity_metrics"] | 0 / {} | [] | ["COUNT(DISTINCT stripe_customer_id)", "COUNT(DISTINCT zendesk_user_id)", "COUNT(DISTINCT primary_email)"] | 1 | 11.184 |
| [S16/Q14](#s16) | success | ["customer360__conversion_funnel_analysis"] | 0 / {} | [] | ["COUNT(DISTINCT stripe_customer_id)", "COUNT(DISTINCT zendesk_user_id)", "COUNT(DISTINCT primary_email)"] | 1 | 418.14 |
| [S17/Q15](#s17) | success | ["customer360__customer_value_analysis"] | 0 / {} | [] | ["COUNT(DISTINCT stripe_customer_id)", "COUNT(DISTINCT zendesk_user_id)", "COUNT(DISTINCT primary_email)"] | 1 | 8.901 |
| [S18/Q16](#s18) | success | ["customer360__conversion_funnel_analysis", "customer360__customer_activity_metrics"] | 2 / {'INNER': 1} | [] | [] | 20 | 5.79 |
| [S19/Q17](#s19) | success | ["customer360__customer_activity_metrics"] | 0 / {} | ["primary_email"] | ["COUNT(*)"] | 10 | 5.5 |
| [S20/Q18](#s20) | success | ["customer360__conversion_funnel_analysis"] | 0 / {} | ["primary_email"] | ["COUNT(*)"] | 10 | 227.992 |
| [S21/Q19](#s21) | success | ["customer360__customer_activity_metrics"] | 0 / {} | [] | [] | 5 | 0.771 |
| [S22/Q20](#s22) | success | ["customer360__conversion_funnel_analysis"] | 0 / {} | [] | [] | 5 | 4.874 |
| [S23/Q21](#s23) | failed | ["customer360__customer_activity_metrics"] | 0 / {} | [] | ["COUNT(DISTINCT marketo_lead_id \|\| '-' \|\| stripe_customer_id \|\| '-' \|\| zendesk_user_id)"] | unknown | 未取得；调用总时长 0.155 ms |
| [S24/Q22](#s24) | failed | ["customer360__conversion_funnel_analysis"] | 0 / {} | [] | ["COUNT(DISTINCT marketo_lead_id \|\| '-' \|\| stripe_customer_id \|\| '-' \|\| zendesk_user_id)"] | unknown | 未取得；调用总时长 0.154 ms |
| [S25/Q23](#s25) | success | ["customer360__customer_activity_metrics"] | 0 / {} | [] | ["COUNT(DISTINCT marketo_lead_id \|\| '-' \|\| stripe_customer_id \|\| '-' \|\| zendesk_user_id)"] | 1 | 5.771 |
| [S26/Q24](#s26) | success | ["customer360__conversion_funnel_analysis"] | 0 / {} | [] | ["COUNT(DISTINCT marketo_lead_id \|\| '-' \|\| stripe_customer_id \|\| '-' \|\| zendesk_user_id)"] | 1 | 393.914 |
| [S27/Q25](#s27) | success | ["customer360__customer_activity_metrics"] | 0 / {} | [] | ["COUNT(DISTINCT activity_analysis_timestamp)"] | 1 | 4.804 |
| [S28/Q26](#s28) | success | ["customer360__conversion_funnel_analysis"] | 0 / {} | [] | ["COUNT(DISTINCT funnel_analysis_timestamp)"] | 1 | 208.909 |
| [S29/Q27](#s29) | success | ["customer360__customer_value_analysis"] | 0 / {} | [] | ["COUNT(DISTINCT analysis_timestamp)"] | 1 | 3.536 |
| [S30/Q28](#s30) | success | ["customer360__conversion_funnel_analysis"] | 0 / {} | [] | ["COUNT(DISTINCT primary_email)"] | 1 | 196.3 |
| [S31/Q29](#s31) | success | ["customer360__customer_activity_metrics"] | 0 / {} | [] | ["COUNT(DISTINCT primary_email)"] | 1 | 6.201 |
| [S32/Q30](#s32) | success | ["customer360__customer_value_analysis"] | 0 / {} | [] | ["COUNT(DISTINCT primary_email)"] | 1 | 5.24 |
| [S33/Q31](#s33) | success | ["customer360__customer_activity_metrics"] | 0 / {} | [] | [] | 10 | 19.836 |
| [S34/Q32](#s34) | success | ["customer360__conversion_funnel_analysis"] | 0 / {} | [] | [] | 10 | 901.896 |
| [S35/Q33](#s35) | success | ["customer360__conversion_funnel_analysis", "customer360__customer_activity_metrics", "customer360__customer_value_analysis"] | 3 / {'INNER': 2} | [] | ["AVG(composite_engagement_score)", "COUNT(*)"] | 1 | 3890.385 |
| [S36/Q34](#s36) | success | ["customer360__conversion_funnel_analysis", "customer360__customer_activity_metrics", "customer360__customer_value_analysis"] | 3 / {'INNER': 2} | [] | ["AVG(composite_engagement_score)", "COUNT(*)", "AVG(recency_score)", "AVG(frequency_score)", "AVG(monetary_score)", "AVG(composite_engagement_score)", "AVG(marketing_to_sales_days)", "AVG(sales_to_support_days)"] | 1 | 3867.596 |
| [S37/Q35](#s37) | success | ["customer360__conversion_funnel_analysis", "customer360__customer_activity_metrics", "customer360__customer_value_analysis"] | 3 / {'INNER': 3} | ["customer_tier", "c.customer_tier"] | ["AVG(composite_engagement_score)", "AVG(funnel_ltv)", "COUNT(*)", "AVG(c.funnel_ltv)", "AVG(t.tier_avg_ltv)", "AVG(c.funnel_ltv)", "AVG(t.tier_avg_ltv)"] | 5 | 4006.764 |
| [S38/Q36](#s38) | success | ["customer360__conversion_funnel_analysis", "customer360__customer_activity_metrics", "customer360__customer_value_analysis"] | 3 / {'INNER': 3} | ["c2.customer_tier", "c.customer_tier"] | ["AVG(composite_engagement_score)", "AVG(c2.funnel_ltv)", "COUNT(*)", "AVG(c.funnel_ltv)", "AVG(t.non_cohort_tier_avg_ltv)", "AVG(c.funnel_ltv - t.non_cohort_tier_avg_ltv)"] | 5 | 4117.526 |
| [S39/Q37](#s39) | success | ["customer360__conversion_funnel_analysis", "customer360__customer_activity_metrics", "customer360__customer_value_analysis"] | 3 / {'INNER': 3} | ["c2.customer_tier"] | ["AVG(composite_engagement_score)", "AVG(c2.funnel_ltv)", "AVG(c.funnel_ltv - t.non_cohort_tier_avg_ltv)"] | 1 | 4113.786 |
| [S40/Q38](#s40) | success | ["customer360__conversion_funnel_analysis", "customer360__customer_activity_metrics", "customer360__customer_value_analysis"] | 3 / {'INNER': 2} | ["primary_engagement_channel"] | ["AVG(composite_engagement_score)", "COUNT(*)", "COUNT(*)", "COUNT(*)"] | 6 | 3947.02 |
| [S41/Q39](#s41) | success | ["customer360__conversion_funnel_analysis", "customer360__customer_activity_metrics", "customer360__customer_value_analysis"] | 3 / {'INNER': 2} | ["zendesk_active"] | ["AVG(composite_engagement_score)", "COUNT(*)", "COUNT(*)", "COUNT(*)"] | 2 | 3948.77 |
| [S42/Q40](#s42) | success | ["customer360__address"] | 0 / {} | [] | [] | 10 | 0.349 |
| [S43/Q41](#s43) | success | ["customer360__address"] | 0 / {} | [] | [] | 10 | 0.36 |
| [S44/Q42](#s44) | success | ["customer360__address"] | 0 / {} | [] | [] | 8 | 9.973 |
| [S45/Q43](#s45) | success | ["customer360__address"] | 0 / {} | [] | ["COUNT(DISTINCT customer360_id)"] | 1 | 36.051 |
| [S46/Q44](#s46) | success | ["customer360__customer_activity_metrics"] | 0 / {} | [] | [] | 10 | 0.33 |
| [S47/Q45](#s47) | failed | ["customer360__customer_activity_metrics"] | 0 / {} | [] | [] | unknown | 未取得；调用总时长 0.11 ms |
| [S48/Q46](#s48) | success | ["customer360__address"] | 0 / {} | [] | [] | 4 | 63.507 |
| [S49/Q47](#s49) | success | ["customer360__address"] | 0 / {} | ["source_system"] | ["COUNT(DISTINCT customer360_id)"] | 2 | 68.982 |
| [S50/Q48](#s50) | success | ["customer360__customer_activity_metrics"] | 0 / {} | [] | [] | 20 | 19.628 |
| [S51/Q49](#s51) | success | ["customer360__address"] | 0 / {} | [] | [] | 20 | 0.297 |
| [S52/Q50](#s52) | success | ["customer360__customer_activity_metrics"] | 0 / {} | [] | [] | 50 | 22.021 |
| [S53/Q51](#s53) | success | ["customer360__address"] | 0 / {} | [] | [] | 200 | 0.735 |
| [S55/Q52](#s55) | success | ["customer360__address"] | 0 / {} | [] | [] | 10378 | 42.86 |
| [S56/Q53](#s56) | success | ["customer360__customer_activity_metrics"] | 0 / {} | [] | [] | 4734 | 68.225 |
| [S57/Q54](#s57) | success | ["customer360__customer_activity_metrics"] | 0 / {} | [] | [] | 4734 | 66.508 |
| [S58/Q55](#s58) | success | ["customer360__address"] | 0 / {} | [] | [] | 13481 | 52.103 |
| [S59/Q56](#s59) | success | ["customer360__address"] | 0 / {} | [] | [] | 13481 | 52.557 |
| [S60/Q57](#s60) | success | ["customer360__customer_activity_metrics"] | 0 / {} | [] | [] | 4734 | 66.868 |
| [S61/Q58](#s61) | success | ["customer360__customer_activity_metrics"] | 0 / {} | [] | [] | 3 | 19.673 |
| [S62/Q59](#s62) | success | ["customer360__customer_activity_metrics"] | 0 / {} | [] | [] | 1 | 0.425 |
| [S63/Q60](#s63) | success | ["customer360__customer_activity_metrics"] | 0 / {} | [] | [] | 1 | 0.226 |
| [S64/Q61](#s64) | success | ["customer360__customer_activity_metrics"] | 0 / {} | [] | [] | 1000 | 11.426 |
| [S65/Q62](#s65) | success | ["customer360__customer_activity_metrics"] | 0 / {} | [] | [] | 1 | 0.303 |
| [S66/Q63](#s66) | success | ["customer360__customer_activity_metrics"] | 0 / {} | [] | [] | 2000 | 20.875 |
| [S67/Q64](#s67) | success | ["customer360__conversion_funnel_analysis"] | 0 / {} | [] | [] | 1 | 0.572 |
| [S68/Q65](#s68) | success | ["customer360__conversion_funnel_analysis"] | 0 / {} | [] | [] | 2000 | 17.304 |
| [S69/Q66](#s69) | success | ["customer360__customer_value_analysis"] | 0 / {} | [] | [] | 1 | 0.408 |
| [S70/Q67](#s70) | success | ["customer360__customer_value_analysis"] | 0 / {} | [] | [] | 2000 | 15.26 |
| [S71/Q68](#s71) | success | ["customer360__address"] | 0 / {} | [] | [] | 10378 | 41.818 |
| [S72/Q69](#s72) | success | ["customer360__customer_activity_metrics"] | 0 / {} | [] | [] | 4734 | 63.193 |
| [S73/Q70](#s73) | success | ["customer360__address"] | 0 / {} | [] | [] | 13481 | 52.189 |
| [S74/Q71](#s74) | success | ["customer360__customer_activity_metrics"] | 0 / {} | [] | [] | 4734 | 66.97 |
| [S75/Q72](#s75) | success | ["customer360__address"] | 0 / {} | ["customer360_id"] | ["COUNT(*)"] | 10 | 36.238 |
| [S76/Q73](#s76) | success | ["customer360__address"] | 0 / {} | [] | [] | 10378 | 41.674 |
| [S77/Q74](#s77) | success | ["customer360__customer_activity_metrics"] | 0 / {} | [] | [] | 4734 | 66.731 |
| [S78/Q75](#s78) | success | ["customer360__conversion_funnel_analysis"] | 0 / {} | [] | ["COUNT(DISTINCT marketo_lead_id \|\| '-' \|\| stripe_customer_id \|\| '-' \|\| zendesk_user_id)"] | 1 | 405.688 |
| [S79/Q76](#s79) | success | ["customer360__conversion_funnel_analysis"] | 0 / {} | [] | ["COUNT(DISTINCT marketo_lead_id \|\| '-' \|\| funnel_analysis_timestamp)"] | 1 | 303.429 |
| [S80/Q77](#s80) | success | ["customer360__address"] | 0 / {} | [] | [] | 20 | 52.819 |
| [S81/Q78](#s81) | success | ["customer360__address"] | 0 / {} | [] | ["COUNT(DISTINCT country)"] | 1 | 33.7 |
| [S82/Q79](#s82) | success | ["customer360__conversion_funnel_analysis", "customer360__customer_activity_metrics", "customer360__customer_value_analysis"] | 3 / {'INNER': 2} | ["CASE WHEN in_marketo = 1 AND in_stripe = 1 AND in_zendesk = 1 THEN 'All 3 Platforms' WHEN in_marketo = 1 AND in_stripe = 1 AND in_zendesk = 0 THEN 'Marketo + Stripe' WHEN in_marketo = 1 AND in_stripe = 0 AND in_zendesk = 1 THEN 'Marketo + Zendesk' WHEN in_marketo = 0 AND in_stripe = 1 AND in_zendesk = 1 THEN 'Stripe + Zendesk' WHEN in_marketo = 1 AND in_stripe = 0 AND in_zendesk = 0 THEN 'Marketo Only' WHEN in_marketo = 0 AND in_stripe = 1 AND in_zendesk = 0 THEN 'Stripe Only' WHEN in_marketo = 0 AND in_stripe = 0 AND in_zendesk = 1 THEN 'Zendesk Only' ELSE 'None' END"] | ["AVG(composite_engagement_score)", "COUNT(*)", "COUNT(*)", "AVG(customer_health_score)", "AVG(composite_engagement_score)", "AVG(funnel_ltv)", "COUNT(*)"] | 8 | 4029.59 |
| [S83/Q80](#s83) | success | ["customer360__conversion_funnel_analysis", "customer360__customer_activity_metrics", "customer360__customer_value_analysis"] | 3 / {'INNER': 2} | ["activity_risk_level"] | ["AVG(composite_engagement_score)", "COUNT(*)", "COUNT(*)", "AVG(customer_health_score)", "AVG(funnel_ltv)", "COUNT(*)"] | 6 | 3959.684 |
| [S84/Q81](#s84) | success | ["customer360__conversion_funnel_analysis", "customer360__customer_activity_metrics", "customer360__customer_value_analysis"] | 3 / {'INNER': 2} | ["engagement_velocity"] | ["AVG(composite_engagement_score)", "COUNT(*)", "COUNT(*)", "AVG(customer_health_score)", "AVG(funnel_ltv)", "COUNT(*)"] | 5 | 3974.929 |
| [S85/Q82](#s85) | success | ["customer360__conversion_funnel_analysis", "customer360__customer_activity_metrics", "customer360__customer_value_analysis"] | 3 / {'INNER': 2} | ["customer_segment"] | ["AVG(composite_engagement_score)", "COUNT(*)", "COUNT(*)", "COUNT(*)"] | 6 | 3949.067 |
| [S86/Q83](#s86) | success | ["customer360__conversion_funnel_analysis", "customer360__customer_activity_metrics", "customer360__customer_value_analysis"] | 3 / {'INNER': 2} | ["lifecycle_stage"] | ["AVG(composite_engagement_score)", "COUNT(*)", "COUNT(*)", "COUNT(*)"] | 7 | 3968.194 |
| [S87/Q84](#s87) | success | ["customer360__conversion_funnel_analysis", "customer360__customer_activity_metrics", "customer360__customer_value_analysis"] | 3 / {'INNER': 2} | [] | ["AVG(composite_engagement_score)"] | 850 | 3850.924 |
| [S88/Q85](#s88) | success | ["customer360__address"] | 0 / {} | ["country"] | ["COUNT(DISTINCT customer360_id)"] | 20 | 69.079 |
| [S89/Q86](#s89) | success | ["customer360__address"] | 0 / {} | [] | ["COUNT(DISTINCT customer360_id)", "COUNT(*)"] | 1 | 45.017 |
| [S90/Q87](#s90) | success | ["customer360__address"] | 0 / {} | ["country_code"] | ["COUNT(DISTINCT customer360_id)"] | 20 | 61.358 |
| [S91/Q88](#s91) | success | ["customer360__address"] | 0 / {} | ["state"] | ["COUNT(DISTINCT customer360_id)"] | 20 | 57.324 |
| [S92/Q89](#s92) | success | ["customer360__address"] | 0 / {} | ["country"] | ["COUNT(DISTINCT customer360_id)"] | 15 | 70.278 |
| [S93/Q90](#s93) | success | ["customer360__address"] | 0 / {} | ["state"] | ["COUNT(DISTINCT customer360_id)"] | 15 | 49.838 |
| [S94/Q91](#s94) | success | ["customer360__conversion_funnel_analysis", "customer360__customer_activity_metrics", "customer360__customer_value_analysis"] | 3 / {'INNER': 2} | ["activity_risk_level", "engagement_velocity"] | ["AVG(composite_engagement_score)", "COUNT(*)", "AVG(customer_health_score)", "AVG(funnel_ltv)", "AVG(composite_engagement_score)", "AVG(churn_probability)", "AVG(cross_platform_consistency)", "AVG(days_since_last_activity)"] | 21 | 3869.305 |
| [S95/Q92](#s95) | success | ["customer360__conversion_funnel_analysis", "customer360__customer_activity_metrics", "customer360__customer_value_analysis"] | 3 / {'INNER': 2} | ["activity_risk_level", "engagement_velocity"] | ["AVG(composite_engagement_score)", "COUNT(*)", "AVG(customer_health_score)", "AVG(funnel_ltv)", "AVG(composite_engagement_score)", "AVG(churn_probability)", "AVG(cross_platform_consistency)", "AVG(days_since_last_activity)"] | 21 | 3908.569 |
| [S96/Q93](#s96) | success | ["customer360__conversion_funnel_analysis", "customer360__customer_activity_metrics", "customer360__customer_value_analysis"] | 3 / {'INNER': 2} | ["rfm_segment"] | ["AVG(composite_engagement_score)", "COUNT(*)", "COUNT(*)", "AVG(recency_score)", "AVG(frequency_score)", "AVG(monetary_score)", "AVG(funnel_ltv)", "AVG(customer_health_score)", "COUNT(*)"] | 7 | 4004.722 |


## 元数据和设置

| SQL | 类别 | 状态 | 内容 |
| --- | --- | --- | --- |
| S1 | connection_setup | success | PRAGMA query_only=ON |
| S2 | metadata | success | SELECT name,sql FROM sqlite_master WHERE type='table' ORDER BY name |
| S54 | metadata | success | PRAGMA table_info(customer360__address) |


## Python 与执行位置

人工源码审查：**database_first_violation**。Python 为平台组合计算健康度、LTV 的分组均值与数量，并计算活跃率和客户细分×生命周期交叉计数；这些可在 SQL 完成。按组传递原始样本给 ANOVA 是合理统计输入，不能仅因出现 groupby 就判为迁出聚合。 [证据](../reviews/dacomp-054.json)。

P1：Need to determine how customer360__address.customer360_id maps to the customer tables. Testing common hash schemes (md5/sha1 of email, lead id, stripe id) in Python since SQLite lacks hash functions and no obvious join key exists.

[源码](../../../runs/dsv4flash-db-first-full-01/dacomp-054/attempt-01/python/P1.py)；[输出](../../../runs/dsv4flash-db-first-full-01/dacomp-054/attempt-01/python/P1.stdout)；[错误](../../../runs/dsv4flash-db-first-full-01/dacomp-054/attempt-01/python/P1.stderr)。检出需人工核验的 SQL 可实现操作：.query(；不能仅凭理由判为合规。

P2：Continuing the hash-mapping test for customer360_id; adapting to list-based row format from db.rows.

[源码](../../../runs/dsv4flash-db-first-full-01/dacomp-054/attempt-01/python/P2.py)；[输出](../../../runs/dsv4flash-db-first-full-01/dacomp-054/attempt-01/python/P2.stdout)；[错误](../../../runs/dsv4flash-db-first-full-01/dacomp-054/attempt-01/python/P2.stderr)。检出需人工核验的 SQL 可实现操作：.query(；不能仅凭理由判为合规。

P3：Investigating whether customer360_id maps via hash of customer identifiers; checking format of address IDs and testing additional candidate fields.

[源码](../../../runs/dsv4flash-db-first-full-01/dacomp-054/attempt-01/python/P3.py)；[输出](../../../runs/dsv4flash-db-first-full-01/dacomp-054/attempt-01/python/P3.stdout)；[错误](../../../runs/dsv4flash-db-first-full-01/dacomp-054/attempt-01/python/P3.stderr)。检出需人工核验的 SQL 可实现操作：.query(；不能仅凭理由判为合规。

P4：Testing more hash combinations (email+org, email+lid etc.) to find the mapping between customer360_id and the customer tables.

[源码](../../../runs/dsv4flash-db-first-full-01/dacomp-054/attempt-01/python/P4.py)；[输出](../../../runs/dsv4flash-db-first-full-01/dacomp-054/attempt-01/python/P4.stdout)；[错误](../../../runs/dsv4flash-db-first-full-01/dacomp-054/attempt-01/python/P4.stderr)。检出需人工核验的 SQL 可实现操作：.query(；不能仅凭理由判为合规。

P5：Running systematic hash-mapping checks across all customers to determine the customer360_id join key for geographic analysis.

[源码](../../../runs/dsv4flash-db-first-full-01/dacomp-054/attempt-01/python/P5.py)；[输出](../../../runs/dsv4flash-db-first-full-01/dacomp-054/attempt-01/python/P5.stdout)；[错误](../../../runs/dsv4flash-db-first-full-01/dacomp-054/attempt-01/python/P5.stderr)。检出需人工核验的 SQL 可实现操作：.query(；不能仅凭理由判为合规。

P6：Searching all text columns in the three customer tables for 32-character hex identifiers that could match customer360__address.customer360_id.

[源码](../../../runs/dsv4flash-db-first-full-01/dacomp-054/attempt-01/python/P6.py)；[输出](../../../runs/dsv4flash-db-first-full-01/dacomp-054/attempt-01/python/P6.stdout)；[错误](../../../runs/dsv4flash-db-first-full-01/dacomp-054/attempt-01/python/P6.stderr)。检出需人工核验的 SQL 可实现操作：.query(；不能仅凭理由判为合规。

P7：Scanning text columns in customer tables for 32-hex identifiers, fixing row indexing (list-based).

[源码](../../../runs/dsv4flash-db-first-full-01/dacomp-054/attempt-01/python/P7.py)；[输出](../../../runs/dsv4flash-db-first-full-01/dacomp-054/attempt-01/python/P7.stdout)；[错误](../../../runs/dsv4flash-db-first-full-01/dacomp-054/attempt-01/python/P7.stderr)。检出需人工核验的 SQL 可实现操作：.query(；不能仅凭理由判为合规。

P8：Testing various email transformations and hash algorithms to find the mapping between primary_email and customer360_id.

[源码](../../../runs/dsv4flash-db-first-full-01/dacomp-054/attempt-01/python/P8.py)；[输出](../../../runs/dsv4flash-db-first-full-01/dacomp-054/attempt-01/python/P8.stdout)；[错误](../../../runs/dsv4flash-db-first-full-01/dacomp-054/attempt-01/python/P8.stderr)。检出需人工核验的 SQL 可实现操作：.query(；不能仅凭理由判为合规。

P9：Checking whether customer360_id hashes include system prefixes (marketo_/stripe_) and examining address row distribution per customer360_id.

[源码](../../../runs/dsv4flash-db-first-full-01/dacomp-054/attempt-01/python/P9.py)；[输出](../../../runs/dsv4flash-db-first-full-01/dacomp-054/attempt-01/python/P9.stdout)；[错误](../../../runs/dsv4flash-db-first-full-01/dacomp-054/attempt-01/python/P9.stderr)。检出需人工核验的 SQL 可实现操作：.query(；不能仅凭理由判为合规。

P10：Testing hash of primary_organization and exploring address table structure since direct mapping remains elusive.

[源码](../../../runs/dsv4flash-db-first-full-01/dacomp-054/attempt-01/python/P10.py)；[输出](../../../runs/dsv4flash-db-first-full-01/dacomp-054/attempt-01/python/P10.stdout)；[错误](../../../runs/dsv4flash-db-first-full-01/dacomp-054/attempt-01/python/P10.stderr)。检出需人工核验的 SQL 可实现操作：.query(；不能仅凭理由判为合规。

P11：Exporting the cohort-level joined dataset to pandas for statistical procedures (ANOVA on platform patterns, correlations for the value/risk framework) that are not well supported by SQLite.

[源码](../../../runs/dsv4flash-db-first-full-01/dacomp-054/attempt-01/python/P11.py)；[输出](../../../runs/dsv4flash-db-first-full-01/dacomp-054/attempt-01/python/P11.stdout)；[错误](../../../runs/dsv4flash-db-first-full-01/dacomp-054/attempt-01/python/P11.stderr)。检出需人工核验的 SQL 可实现操作：.query(；不能仅凭理由判为合规。

P12：Performing statistical analysis (ANOVA, Tukey HSD, correlations) and generating visualizations for the platform pattern impact on health score, risk-velocity framework, and LTV distribution. These procedures require statistical testing and visualization capabilities beyond SQL.

[源码](../../../runs/dsv4flash-db-first-full-01/dacomp-054/attempt-01/python/P12.py)；[输出](../../../runs/dsv4flash-db-first-full-01/dacomp-054/attempt-01/python/P12.stdout)；[错误](../../../runs/dsv4flash-db-first-full-01/dacomp-054/attempt-01/python/P12.stderr)。检出需人工核验的 SQL 可实现操作：groupby(；不能仅凭理由判为合规。

P13：Completing statistical analysis (ANOVA, correlation) and generating all 5 visualizations for the report. statsmodels is unavailable, so using scipy.stats for ANOVA.

[源码](../../../runs/dsv4flash-db-first-full-01/dacomp-054/attempt-01/python/P13.py)；[输出](../../../runs/dsv4flash-db-first-full-01/dacomp-054/attempt-01/python/P13.stdout)；[错误](../../../runs/dsv4flash-db-first-full-01/dacomp-054/attempt-01/python/P13.stderr)。检出需人工核验的 SQL 可实现操作：groupby(；不能仅凭理由判为合规。

P14：Generating geography context and additional visualizations (segment-lifecycle heatmap, health score distribution) for the report, since the address table cannot be joined to the cohort.

[源码](../../../runs/dsv4flash-db-first-full-01/dacomp-054/attempt-01/python/P14.py)；[输出](../../../runs/dsv4flash-db-first-full-01/dacomp-054/attempt-01/python/P14.stdout)；[错误](../../../runs/dsv4flash-db-first-full-01/dacomp-054/attempt-01/python/P14.stderr)。检出需人工核验的 SQL 可实现操作：.query(；不能仅凭理由判为合规。

## 优化机会

已验证候选。筛选限于精确 SQL、相同自包含 CTE、相同单表完整过滤、可分解单表聚合；未覆盖任意 Join 等价和一般谓词蕴含。全部候选都是 offline，未测在线预测。

| 候选 | 类型 | 已有结果 | 覆盖 SQL | 后续次数 | 中间行数 | 验证 | 成本 |
| --- | --- | --- | --- | --- | --- | --- | --- |
| C1 | exact-result reuse | True | ["S55", "S71", "S76"] | 2 | unknown | not_verified_cap | Not tested |
| C2 | exact-result reuse | True | ["S56", "S57", "S60"] | 2 | unknown | not_verified_cap | Not tested |
| C3 | exact-result reuse | True | ["S58", "S59", "S73"] | 2 | unknown | not_verified_cap | Not tested |
| C4 | exact-result reuse | True | ["S62", "S63", "S65"] | 2 | unknown | not_verified_cap | Not tested |
| C5 | common subexpression | False | ["S35", "S36", "S37", "S38", "S39", "S40", "S41", "S50", "S52", "S56", "S57", "S60", "S61", "S72", "S74", "S77", "S82", "S83", "S84", "S85", "S86", "S87", "S94", "S95", "S96"] | 24 | 6947 | verification_limited | Not benchmarked; correctness alone does not establish net speedup. |
| C6 | common subexpression | False | ["S35", "S36", "S37", "S38", "S39", "S40", "S41", "S82", "S83", "S84", "S85", "S86", "S87", "S94", "S95", "S96"] | 15 | 441119 | verified | Not benchmarked; correctness alone does not establish net speedup. |
| C7 | common subexpression | False | ["S35", "S36", "S37", "S38", "S39", "S40", "S41", "S82", "S83", "S84", "S85", "S86", "S87", "S94", "S95", "S96"] | 15 | 5001 | verified | Not benchmarked; correctness alone does not establish net speedup. |
| C8 | aggregate MV | False | ["S3", "S7", "S19"] | 2 | unknown | not_verified_cap | Not tested |
| C9 | aggregate MV | False | ["S4", "S20"] | 1 | unknown | not_verified_cap | Not tested |
| C10 | common filtered view | False | ["S88", "S92"] | 1 | unknown | not_verified_cap | Not tested |
| C11 | common filtered view | False | ["S91", "S93"] | 1 | unknown | not_verified_cap | Not tested |


已验证覆盖（含触发查询、候选并集去重）：16/90 条成功数据 SQL。正确性仅针对当前数据库快照；未测性能的候选不能声称已加速。

[完整 build/rewrite 与比较证据](dacomp-054.analysis.json)。

### C6：common subexpression

Identical self-contained CTE body across queries.

原查询 [S35](#s35), [S36](#s36), [S37](#s37), [S38](#s38), [S39](#s39), [S40](#s40), [S41](#s41), [S82](#s82), [S83](#s83), [S84](#s84), [S85](#s85), [S86](#s86), [S87](#s87), [S94](#s94), [S95](#s95), [S96](#s96) → 新增共享状态 C6 → 后续 15 次可复用。该构建点为事后假设，不代表 Agent 当时预知后续。

构建定义：

```sql
SELECT *, ROW_NUMBER() OVER (PARTITION BY primary_email ORDER BY funnel_analysis_timestamp DESC) AS rn FROM customer360__conversion_funnel_analysis
```

受益查询 S35 的改写示例：

```sql
/* Build the cohort: latest records per email joined together */ WITH latest_activity AS (SELECT *, ROW_NUMBER() OVER (PARTITION BY primary_email ORDER BY activity_analysis_timestamp DESC) AS rn FROM customer360__customer_activity_metrics), latest_funnel AS (SELECT * FROM temp.reuse_candidate), latest_value AS (SELECT *, ROW_NUMBER() OVER (PARTITION BY primary_email ORDER BY analysis_timestamp DESC) AS rn FROM customer360__customer_value_analysis), cohort AS (SELECT a.primary_email, a.composite_engagement_score, f.marketing_to_sales_days, f.sales_to_support_days, f.customer_tier, f.estimated_customer_ltv AS funnel_ltv, v.recency_score, v.frequency_score, v.monetary_score, v.estimated_customer_ltv AS value_ltv, a.primary_engagement_channel, a.zendesk_active, a.in_marketo, a.in_stripe, a.in_zendesk, a.customer_health_score, a.activity_risk_level, a.engagement_velocity, a.customer_segment, a.lifecycle_stage FROM latest_activity AS a JOIN latest_funnel AS f ON a.primary_email = f.primary_email AND f.rn = 1 JOIN latest_value AS v ON a.primary_email = v.primary_email AND v.rn = 1 WHERE a.rn = 1 AND f.marketing_to_sales_days BETWEEN 10 AND 20 AND f.sales_to_support_days > 30 AND a.composite_engagement_score > (SELECT AVG(composite_engagement_score) FROM customer360__customer_activity_metrics)) SELECT COUNT(*) AS cohort_count FROM cohort
```

| 原 SQL | 列名一致 | 结果一致 | 比较方法 |
| --- | --- | --- | --- |
| S35 | True | True | exact_multiset |
| S36 | True | True | exact_multiset |
| S37 | True | True | ordered_numeric_tolerance |
| S38 | True | True | ordered_numeric_tolerance |
| S39 | True | True | exact_multiset |
| S40 | True | True | ordered_numeric_tolerance |
| S41 | True | True | ordered_numeric_tolerance |
| S82 | True | True | ordered_numeric_tolerance |
| S83 | True | True | ordered_numeric_tolerance |
| S84 | True | True | ordered_numeric_tolerance |
| S85 | True | True | ordered_numeric_tolerance |
| S86 | True | True | ordered_numeric_tolerance |
| S87 | True | True | exact_multiset |
| S94 | True | True | ordered_numeric_tolerance |
| S95 | True | True | ordered_numeric_tolerance |
| S96 | True | True | ordered_numeric_tolerance |


验证状态：verified；成本结论：Not benchmarked; correctness alone does not establish net speedup.

### C7：common subexpression

Identical self-contained CTE body across queries.

原查询 [S35](#s35), [S36](#s36), [S37](#s37), [S38](#s38), [S39](#s39), [S40](#s40), [S41](#s41), [S82](#s82), [S83](#s83), [S84](#s84), [S85](#s85), [S86](#s86), [S87](#s87), [S94](#s94), [S95](#s95), [S96](#s96) → 新增共享状态 C7 → 后续 15 次可复用。该构建点为事后假设，不代表 Agent 当时预知后续。

构建定义：

```sql
SELECT *, ROW_NUMBER() OVER (PARTITION BY primary_email ORDER BY analysis_timestamp DESC) AS rn FROM customer360__customer_value_analysis
```

受益查询 S35 的改写示例：

```sql
/* Build the cohort: latest records per email joined together */ WITH latest_activity AS (SELECT *, ROW_NUMBER() OVER (PARTITION BY primary_email ORDER BY activity_analysis_timestamp DESC) AS rn FROM customer360__customer_activity_metrics), latest_funnel AS (SELECT *, ROW_NUMBER() OVER (PARTITION BY primary_email ORDER BY funnel_analysis_timestamp DESC) AS rn FROM customer360__conversion_funnel_analysis), latest_value AS (SELECT * FROM temp.reuse_candidate), cohort AS (SELECT a.primary_email, a.composite_engagement_score, f.marketing_to_sales_days, f.sales_to_support_days, f.customer_tier, f.estimated_customer_ltv AS funnel_ltv, v.recency_score, v.frequency_score, v.monetary_score, v.estimated_customer_ltv AS value_ltv, a.primary_engagement_channel, a.zendesk_active, a.in_marketo, a.in_stripe, a.in_zendesk, a.customer_health_score, a.activity_risk_level, a.engagement_velocity, a.customer_segment, a.lifecycle_stage FROM latest_activity AS a JOIN latest_funnel AS f ON a.primary_email = f.primary_email AND f.rn = 1 JOIN latest_value AS v ON a.primary_email = v.primary_email AND v.rn = 1 WHERE a.rn = 1 AND f.marketing_to_sales_days BETWEEN 10 AND 20 AND f.sales_to_support_days > 30 AND a.composite_engagement_score > (SELECT AVG(composite_engagement_score) FROM customer360__customer_activity_metrics)) SELECT COUNT(*) AS cohort_count FROM cohort
```

| 原 SQL | 列名一致 | 结果一致 | 比较方法 |
| --- | --- | --- | --- |
| S35 | True | True | exact_multiset |
| S36 | True | True | exact_multiset |
| S37 | True | True | ordered_numeric_tolerance |
| S38 | True | True | ordered_numeric_tolerance |
| S39 | True | True | exact_multiset |
| S40 | True | True | ordered_numeric_tolerance |
| S41 | True | True | ordered_numeric_tolerance |
| S82 | True | True | ordered_numeric_tolerance |
| S83 | True | True | ordered_numeric_tolerance |
| S84 | True | True | ordered_numeric_tolerance |
| S85 | True | True | ordered_numeric_tolerance |
| S86 | True | True | ordered_numeric_tolerance |
| S87 | True | True | exact_multiset |
| S94 | True | True | ordered_numeric_tolerance |
| S95 | True | True | ordered_numeric_tolerance |
| S96 | True | True | ordered_numeric_tolerance |


验证状态：verified；成本结论：Not benchmarked; correctness alone does not establish net speedup.

### C5：common subexpression

Identical self-contained CTE body across queries.

原查询 [S35](#s35), [S36](#s36), [S37](#s37), [S38](#s38), [S39](#s39), [S40](#s40), [S41](#s41), [S50](#s50), [S52](#s52), [S56](#s56), [S57](#s57), [S60](#s60), [S61](#s61), [S72](#s72), [S74](#s74), [S77](#s77), [S82](#s82), [S83](#s83), [S84](#s84), [S85](#s85), [S86](#s86), [S87](#s87), [S94](#s94), [S95](#s95), [S96](#s96) → 新增共享状态 C5 → 后续 24 次可复用。该构建点为事后假设，不代表 Agent 当时预知后续。

构建定义：

```sql
SELECT *, ROW_NUMBER() OVER (PARTITION BY primary_email ORDER BY activity_analysis_timestamp DESC) AS rn FROM customer360__customer_activity_metrics
```

受益查询 S35 的改写示例：

```sql
/* Build the cohort: latest records per email joined together */ WITH latest_activity AS (SELECT * FROM temp.reuse_candidate), latest_funnel AS (SELECT *, ROW_NUMBER() OVER (PARTITION BY primary_email ORDER BY funnel_analysis_timestamp DESC) AS rn FROM customer360__conversion_funnel_analysis), latest_value AS (SELECT *, ROW_NUMBER() OVER (PARTITION BY primary_email ORDER BY analysis_timestamp DESC) AS rn FROM customer360__customer_value_analysis), cohort AS (SELECT a.primary_email, a.composite_engagement_score, f.marketing_to_sales_days, f.sales_to_support_days, f.customer_tier, f.estimated_customer_ltv AS funnel_ltv, v.recency_score, v.frequency_score, v.monetary_score, v.estimated_customer_ltv AS value_ltv, a.primary_engagement_channel, a.zendesk_active, a.in_marketo, a.in_stripe, a.in_zendesk, a.customer_health_score, a.activity_risk_level, a.engagement_velocity, a.customer_segment, a.lifecycle_stage FROM latest_activity AS a JOIN latest_funnel AS f ON a.primary_email = f.primary_email AND f.rn = 1 JOIN latest_value AS v ON a.primary_email = v.primary_email AND v.rn = 1 WHERE a.rn = 1 AND f.marketing_to_sales_days BETWEEN 10 AND 20 AND f.sales_to_support_days > 30 AND a.composite_engagement_score > (SELECT AVG(composite_engagement_score) FROM customer360__customer_activity_metrics)) SELECT COUNT(*) AS cohort_count FROM cohort
```

| 原 SQL | 列名一致 | 结果一致 | 比较方法 |
| --- | --- | --- | --- |
| S35 | True | True | exact_multiset |
| S36 | True | True | exact_multiset |
| S37 | True | True | ordered_numeric_tolerance |
| S38 | True | True | ordered_numeric_tolerance |
| S39 | True | True | exact_multiset |
| S40 | True | True | ordered_numeric_tolerance |
| S41 | True | True | ordered_numeric_tolerance |
| S50 | True | True | exact_multiset |
| S52 | True | True | exact_multiset |
| S56 | True | True | exact_multiset |
| S57 | True | True | exact_multiset |
| S60 | True | True | exact_multiset |
| S61 | True | True | exact_multiset |
| S72 | True | True | exact_multiset |
| S74 | True | True | exact_multiset |
| S77 | True | True | exact_multiset |
| S82 | True | True | ordered_numeric_tolerance |
| S83 | True | True | ordered_numeric_tolerance |


验证状态：verification_limited；成本结论：Not benchmarked; correctness alone does not establish net speedup.

[性能证据 C6](dacomp-054.C6.performance.json)：limited_or_failed。

结果依赖：自动记录 SQL→Python 的接口父调用，以及源码中引用归档文件的消费者；字面值相同不认定因果。模型方向选择需要人工读取消息，尚未做全面因果标注。

[原始报告](../../../runs/dsv4flash-db-first-full-01/dacomp-054/attempt-01/answer.md)；[统一消息](../../../runs/dsv4flash-db-first-full-01/dacomp-054/attempt-01/messages.jsonl)；[原始 OpenCode 事件](../../../runs/dsv4flash-db-first-full-01/dacomp-054/attempt-01/opencode.jsonl)；[SQL 引擎日志](../../../runs/dsv4flash-db-first-full-01/dacomp-054/attempt-01/sql_journal.jsonl)。

[可读报告（本地图片链接规范化）](../answers/dacomp-054.md)。原始回答保留，分析结论未改写。

## S1

类别 `connection_setup`；来源 `connection`；调用 `358174fec7cb400180434ff3657eab9b`；状态 `success`。

```sql
PRAGMA query_only=ON
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-054/attempt-01/sql/S1.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-054/attempt-01/sql/S1.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-054/attempt-01/results/S1.rows.jsonl)；完整：True；SHA256：`e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`。

## S2

类别 `metadata`；来源 `list_db`；调用 `358174fec7cb400180434ff3657eab9b`；状态 `success`。

```sql
SELECT name,sql FROM sqlite_master WHERE type='table' ORDER BY name
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-054/attempt-01/sql/S2.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-054/attempt-01/sql/S2.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-054/attempt-01/results/S2.rows.jsonl)；完整：True；SHA256：`f4acc102fd4c78ef29049a1f012db34836c9725574742e8ef867e263ef240e3d`。

## S3

类别 `data`；来源 `query_db`；调用 `8e9cb771e370462784cdb57655c0f2b9`；状态 `success`。

```sql
SELECT COUNT(*) AS total_rows FROM customer360__customer_activity_metrics
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-054/attempt-01/sql/S3.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-054/attempt-01/sql/S3.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-054/attempt-01/results/S3.rows.jsonl)；完整：True；SHA256：`819d798b9337f37beeac92ec2ff20d912674ae0fc768e72658ba66ea4bdc0ad1`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "customer360__customer_activity_metrics", "kind": "base", "block": null, "base_tables": ["customer360__customer_activity_metrics"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |


## S4

类别 `data`；来源 `query_db`；调用 `e76b7bed721a41e3babefced18dcbdc0`；状态 `success`。

```sql
SELECT COUNT(*) AS total_rows FROM customer360__conversion_funnel_analysis
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-054/attempt-01/sql/S4.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-054/attempt-01/sql/S4.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-054/attempt-01/results/S4.rows.jsonl)；完整：True；SHA256：`d67f3ad6a82274c8ab519097cdbbdb4f706a9edd57d9863e94c96de71f798556`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "customer360__conversion_funnel_analysis", "kind": "base", "block": null, "base_tables": ["customer360__conversion_funnel_analysis"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |


## S5

类别 `data`；来源 `query_db`；调用 `7817496c27da4dc684670e83b8ccb4e9`；状态 `success`。

```sql
SELECT COUNT(*) AS total_rows FROM customer360__customer_value_analysis
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-054/attempt-01/sql/S5.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-054/attempt-01/sql/S5.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-054/attempt-01/results/S5.rows.jsonl)；完整：True；SHA256：`bdbef1caff7b48e20559d35d963fc16e07bc4b392f104c577c5c0c19de92dd94`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "customer360__customer_value_analysis", "kind": "base", "block": null, "base_tables": ["customer360__customer_value_analysis"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |


## S6

类别 `data`；来源 `query_db`；调用 `847f08119cd64ad9860e29e474975107`；状态 `success`。

```sql
SELECT COUNT(*) AS total_rows FROM customer360__address
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-054/attempt-01/sql/S6.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-054/attempt-01/sql/S6.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-054/attempt-01/results/S6.rows.jsonl)；完整：True；SHA256：`0503cc454e3a6dd53654c9b4b2178acaaa9042b236f70cc1d2fdfa42545eafe8`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "customer360__address", "kind": "base", "block": null, "base_tables": ["customer360__address"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |


## S7

类别 `data`；来源 `query_db`；调用 `88b282604d944a2dac5697a67fcc5906`；状态 `success`。

```sql
SELECT AVG(composite_engagement_score) AS avg_composite_engagement_score FROM customer360__customer_activity_metrics
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-054/attempt-01/sql/S7.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-054/attempt-01/sql/S7.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-054/attempt-01/results/S7.rows.jsonl)；完整：True；SHA256：`e13edb8b13b4b46064abf6c0cead90732af573456f3f66d3df6d66e36be7e0eb`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "customer360__customer_activity_metrics", "kind": "base", "block": null, "base_tables": ["customer360__customer_activity_metrics"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | AVG(composite_engagement_score) | [{"table": "customer360__customer_activity_metrics", "column": "composite_engagement_score"}] | [] | False |


## S8

类别 `data`；来源 `query_db`；调用 `70e5c8d17c434ca198a0591900504456`；状态 `success`。

```sql
SELECT DISTINCT customer_tier FROM customer360__conversion_funnel_analysis ORDER BY customer_tier
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-054/attempt-01/sql/S8.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-054/attempt-01/sql/S8.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-054/attempt-01/results/S8.rows.jsonl)；完整：True；SHA256：`0247280cee89907e617e0bf91816fd7b470c0f7c042bae332cbeda2b75c5b59b`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "customer360__conversion_funnel_analysis", "kind": "base", "block": null, "base_tables": ["customer360__conversion_funnel_analysis"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |


## S9

类别 `data`；来源 `query_db`；调用 `15b3e4cbb95b4f06b5485224435c9b7e`；状态 `success`。

```sql
SELECT DISTINCT primary_engagement_channel FROM customer360__customer_activity_metrics ORDER BY primary_engagement_channel
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-054/attempt-01/sql/S9.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-054/attempt-01/sql/S9.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-054/attempt-01/results/S9.rows.jsonl)；完整：True；SHA256：`6839b0d2061a505aa5741cc142a1979fb2749768aa8530806b43e83d6ad185ec`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "customer360__customer_activity_metrics", "kind": "base", "block": null, "base_tables": ["customer360__customer_activity_metrics"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |


## S10

类别 `data`；来源 `query_db`；调用 `a2ab19d3bbe14a2da3062a8be144a227`；状态 `success`。

```sql
SELECT COUNT(*) AS matching_rows
FROM customer360__conversion_funnel_analysis f
INNER JOIN customer360__customer_activity_metrics a ON f.marketo_lead_id = a.marketo_lead_id
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-054/attempt-01/sql/S10.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-054/attempt-01/sql/S10.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-054/attempt-01/results/S10.rows.jsonl)；完整：True；SHA256：`b10e8a7ba89866fa7bf3afc0edcef2f3fd1108188b95456a45c99a138f82b290`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "f", "kind": "base", "block": null, "base_tables": ["customer360__conversion_funnel_analysis"]}, {"alias": "a", "kind": "base", "block": null, "base_tables": ["customer360__customer_activity_metrics"]}] | [{"type": "INNER", "right": "customer360__customer_activity_metrics AS a", "on": "f.marketo_lead_id = a.marketo_lead_id", "using": []}] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |


## S11

类别 `data`；来源 `query_db`；调用 `205d9234c3834d86a4a53fb31a00699b`；状态 `success`。

```sql
SELECT COUNT(*) AS matching_rows
FROM customer360__conversion_funnel_analysis f
INNER JOIN customer360__customer_value_analysis v ON f.marketo_lead_id = v.marketo_lead_id
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-054/attempt-01/sql/S11.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-054/attempt-01/sql/S11.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-054/attempt-01/results/S11.rows.jsonl)；完整：True；SHA256：`8a75a17747bb8544b3779c7b83b9a2974148bcb490a778c5afa1a5a150807a9d`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "f", "kind": "base", "block": null, "base_tables": ["customer360__conversion_funnel_analysis"]}, {"alias": "v", "kind": "base", "block": null, "base_tables": ["customer360__customer_value_analysis"]}] | [{"type": "INNER", "right": "customer360__customer_value_analysis AS v", "on": "f.marketo_lead_id = v.marketo_lead_id", "using": []}] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |


## S12

类别 `data`；来源 `query_db`；调用 `f330cf8460304f15a774439a6ffb95b3`；状态 `success`。

```sql
SELECT COUNT(DISTINCT marketo_lead_id) AS distinct_leads_activity FROM customer360__customer_activity_metrics
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-054/attempt-01/sql/S12.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-054/attempt-01/sql/S12.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-054/attempt-01/results/S12.rows.jsonl)；完整：True；SHA256：`29433440de3cbf6d261739003c6943be8c3f2086c8c7ba6f73f02e13236537d2`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "customer360__customer_activity_metrics", "kind": "base", "block": null, "base_tables": ["customer360__customer_activity_metrics"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(DISTINCT marketo_lead_id) | [{"table": "customer360__customer_activity_metrics", "column": "marketo_lead_id"}] | [] | False |


## S13

类别 `data`；来源 `query_db`；调用 `7da3a575bb3f4f82831e9393d5b38d3a`；状态 `success`。

```sql
SELECT COUNT(DISTINCT marketo_lead_id) AS distinct_leads_funnel FROM customer360__conversion_funnel_analysis
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-054/attempt-01/sql/S13.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-054/attempt-01/sql/S13.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-054/attempt-01/results/S13.rows.jsonl)；完整：True；SHA256：`29433440de3cbf6d261739003c6943be8c3f2086c8c7ba6f73f02e13236537d2`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "customer360__conversion_funnel_analysis", "kind": "base", "block": null, "base_tables": ["customer360__conversion_funnel_analysis"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(DISTINCT marketo_lead_id) | [{"table": "customer360__conversion_funnel_analysis", "column": "marketo_lead_id"}] | [] | False |


## S14

类别 `data`；来源 `query_db`；调用 `2140cf5599d24974a0d89fa4d7a92891`；状态 `success`。

```sql
SELECT COUNT(DISTINCT marketo_lead_id) AS distinct_leads_value FROM customer360__customer_value_analysis
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-054/attempt-01/sql/S14.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-054/attempt-01/sql/S14.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-054/attempt-01/results/S14.rows.jsonl)；完整：True；SHA256：`29433440de3cbf6d261739003c6943be8c3f2086c8c7ba6f73f02e13236537d2`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "customer360__customer_value_analysis", "kind": "base", "block": null, "base_tables": ["customer360__customer_value_analysis"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(DISTINCT marketo_lead_id) | [{"table": "customer360__customer_value_analysis", "column": "marketo_lead_id"}] | [] | False |


## S15

类别 `data`；来源 `query_db`；调用 `1377d2473ac749c7be04a47eb169513c`；状态 `success`。

```sql
SELECT COUNT(DISTINCT stripe_customer_id) AS distinct_stripe_activity,
       COUNT(DISTINCT zendesk_user_id) AS distinct_zd_activity,
       COUNT(DISTINCT primary_email) AS distinct_email_activity
FROM customer360__customer_activity_metrics
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-054/attempt-01/sql/S15.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-054/attempt-01/sql/S15.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-054/attempt-01/results/S15.rows.jsonl)；完整：True；SHA256：`c3d5292524da39c95d7d725b1ca6a645362174621c7ec658d686c06f1908a385`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "customer360__customer_activity_metrics", "kind": "base", "block": null, "base_tables": ["customer360__customer_activity_metrics"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(DISTINCT stripe_customer_id) | [{"table": "customer360__customer_activity_metrics", "column": "stripe_customer_id"}] | [] | False |
| B1 | COUNT(DISTINCT zendesk_user_id) | [{"table": "customer360__customer_activity_metrics", "column": "zendesk_user_id"}] | [] | False |
| B1 | COUNT(DISTINCT primary_email) | [{"table": "customer360__customer_activity_metrics", "column": "primary_email"}] | [] | False |


## S16

类别 `data`；来源 `query_db`；调用 `7a8fd71a9ace422bb278a62cce3653d5`；状态 `success`。

```sql
SELECT COUNT(DISTINCT stripe_customer_id) AS distinct_stripe_funnel,
       COUNT(DISTINCT zendesk_user_id) AS distinct_zd_funnel,
       COUNT(DISTINCT primary_email) AS distinct_email_funnel
FROM customer360__conversion_funnel_analysis
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-054/attempt-01/sql/S16.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-054/attempt-01/sql/S16.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-054/attempt-01/results/S16.rows.jsonl)；完整：True；SHA256：`047b7ecb201db661c6bd11528accedb3f2fee934c0851fe3ba3ba77c5a920bc6`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "customer360__conversion_funnel_analysis", "kind": "base", "block": null, "base_tables": ["customer360__conversion_funnel_analysis"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(DISTINCT stripe_customer_id) | [{"table": "customer360__conversion_funnel_analysis", "column": "stripe_customer_id"}] | [] | False |
| B1 | COUNT(DISTINCT zendesk_user_id) | [{"table": "customer360__conversion_funnel_analysis", "column": "zendesk_user_id"}] | [] | False |
| B1 | COUNT(DISTINCT primary_email) | [{"table": "customer360__conversion_funnel_analysis", "column": "primary_email"}] | [] | False |


## S17

类别 `data`；来源 `query_db`；调用 `24cf9d86778c4082b1affcd1de9f45ce`；状态 `success`。

```sql
SELECT COUNT(DISTINCT stripe_customer_id) AS distinct_stripe_value,
       COUNT(DISTINCT zendesk_user_id) AS distinct_zd_value,
       COUNT(DISTINCT primary_email) AS distinct_email_value
FROM customer360__customer_value_analysis
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-054/attempt-01/sql/S17.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-054/attempt-01/sql/S17.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-054/attempt-01/results/S17.rows.jsonl)；完整：True；SHA256：`c3d5292524da39c95d7d725b1ca6a645362174621c7ec658d686c06f1908a385`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "customer360__customer_value_analysis", "kind": "base", "block": null, "base_tables": ["customer360__customer_value_analysis"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(DISTINCT stripe_customer_id) | [{"table": "customer360__customer_value_analysis", "column": "stripe_customer_id"}] | [] | False |
| B1 | COUNT(DISTINCT zendesk_user_id) | [{"table": "customer360__customer_value_analysis", "column": "zendesk_user_id"}] | [] | False |
| B1 | COUNT(DISTINCT primary_email) | [{"table": "customer360__customer_value_analysis", "column": "primary_email"}] | [] | False |


## S18

类别 `data`；来源 `query_db`；调用 `e24890a1a6194e0e8d6856337a651bf5`；状态 `success`。

```sql
SELECT a.primary_email, a.composite_engagement_score, f.marketing_to_sales_days, f.sales_to_support_days
FROM customer360__customer_activity_metrics a
INNER JOIN customer360__conversion_funnel_analysis f ON a.primary_email = f.primary_email
WHERE f.marketing_to_sales_days BETWEEN 10 AND 20
  AND f.sales_to_support_days > 30
  AND a.composite_engagement_score > 8.99949618540379
LIMIT 20
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-054/attempt-01/sql/S18.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-054/attempt-01/sql/S18.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-054/attempt-01/results/S18.rows.jsonl)；完整：True；SHA256：`b0d4a8dec8fe832285c1024cec5f79fce7f17db437e1a554f5ea4bfdd72537da`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "a", "kind": "base", "block": null, "base_tables": ["customer360__customer_activity_metrics"]}, {"alias": "f", "kind": "base", "block": null, "base_tables": ["customer360__conversion_funnel_analysis"]}] | [{"type": "INNER", "right": "customer360__conversion_funnel_analysis AS f", "on": "a.primary_email = f.primary_email", "using": []}] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |


## S19

类别 `data`；来源 `query_db`；调用 `611eb3793f0249fb998efed6d6c4edc6`；状态 `success`。

```sql
SELECT primary_email, COUNT(*) AS cnt
FROM customer360__customer_activity_metrics
GROUP BY primary_email
ORDER BY cnt DESC
LIMIT 10
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-054/attempt-01/sql/S19.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-054/attempt-01/sql/S19.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-054/attempt-01/results/S19.rows.jsonl)；完整：True；SHA256：`5e901bf342577be7fc2a0cd8ce40cb3c0e582ae327c8ff82e651e917fea17abc`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "customer360__customer_activity_metrics", "kind": "base", "block": null, "base_tables": ["customer360__customer_activity_metrics"]}] | [] | ["primary_email"] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |


## S20

类别 `data`；来源 `query_db`；调用 `5ad615578d974c159da33cf5bacaf2a3`；状态 `success`。

```sql
SELECT primary_email, COUNT(*) AS cnt
FROM customer360__conversion_funnel_analysis
GROUP BY primary_email
ORDER BY cnt DESC
LIMIT 10
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-054/attempt-01/sql/S20.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-054/attempt-01/sql/S20.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-054/attempt-01/results/S20.rows.jsonl)；完整：True；SHA256：`923f862d12e41b53a051c31beb2968003de0598ffebb2d4d494ba55b42550f19`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "customer360__conversion_funnel_analysis", "kind": "base", "block": null, "base_tables": ["customer360__conversion_funnel_analysis"]}] | [] | ["primary_email"] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |


## S21

类别 `data`；来源 `query_db`；调用 `56b1368149204ce69ce264cb2d4951a4`；状态 `success`。

```sql
SELECT * FROM customer360__customer_activity_metrics
WHERE primary_email = 'brenda.davis@enterprise.org'
LIMIT 5
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-054/attempt-01/sql/S21.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-054/attempt-01/sql/S21.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-054/attempt-01/results/S21.rows.jsonl)；完整：True；SHA256：`49e355ad62702a7f4881f8fd6a3f6c1754898455ba37bf3c41deaa0cbe44a3e3`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "customer360__customer_activity_metrics", "kind": "base", "block": null, "base_tables": ["customer360__customer_activity_metrics"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |


## S22

类别 `data`；来源 `query_db`；调用 `1d092d8868bd4a62b3550cecf55c4f92`；状态 `success`。

```sql
SELECT * FROM customer360__conversion_funnel_analysis
WHERE primary_email = 'brenda.davis@enterprise.org'
LIMIT 5
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-054/attempt-01/sql/S22.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-054/attempt-01/sql/S22.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-054/attempt-01/results/S22.rows.jsonl)；完整：True；SHA256：`4bc79db087b09ff09a6f4b1cf691a06153c7719311cc5aea1ada9ed31621a250`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "customer360__conversion_funnel_analysis", "kind": "base", "block": null, "base_tables": ["customer360__conversion_funnel_analysis"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |


## S23

类别 `data`；来源 `query_db`；调用 `a52627b6f1874b5e9a31466c7743f453`；状态 `failed`。

```sql
SELECT COUNT(DISTINCT CONCAT(marketo_lead_id, '-', stripe_customer_id, '-', zendesk_user_id)) AS distinct_combo
FROM customer360__customer_activity_metrics
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-054/attempt-01/sql/S23.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-054/attempt-01/sql/S23.parameters.json)。

错误：`OperationalError('no such function: CONCAT')`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "customer360__customer_activity_metrics", "kind": "base", "block": null, "base_tables": ["customer360__customer_activity_metrics"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(DISTINCT marketo_lead_id \|\| '-' \|\| stripe_customer_id \|\| '-' \|\| zendesk_user_id) | [{"table": "customer360__customer_activity_metrics", "column": "marketo_lead_id"}, {"table": "customer360__customer_activity_metrics", "column": "stripe_customer_id"}, {"table": "customer360__customer_activity_metrics", "column": "zendesk_user_id"}] | [] | False |


## S24

类别 `data`；来源 `query_db`；调用 `81e08199fabc4ea6829f4df01ef25a52`；状态 `failed`。

```sql
SELECT COUNT(DISTINCT CONCAT(marketo_lead_id, '-', stripe_customer_id, '-', zendesk_user_id)) AS distinct_combo
FROM customer360__conversion_funnel_analysis
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-054/attempt-01/sql/S24.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-054/attempt-01/sql/S24.parameters.json)。

错误：`OperationalError('no such function: CONCAT')`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "customer360__conversion_funnel_analysis", "kind": "base", "block": null, "base_tables": ["customer360__conversion_funnel_analysis"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(DISTINCT marketo_lead_id \|\| '-' \|\| stripe_customer_id \|\| '-' \|\| zendesk_user_id) | [{"table": "customer360__conversion_funnel_analysis", "column": "marketo_lead_id"}, {"table": "customer360__conversion_funnel_analysis", "column": "stripe_customer_id"}, {"table": "customer360__conversion_funnel_analysis", "column": "zendesk_user_id"}] | [] | False |


## S25

类别 `data`；来源 `query_db`；调用 `c381400b18cd494fa7c31ae4e97cc188`；状态 `success`。

```sql
SELECT COUNT(DISTINCT marketo_lead_id || '-' || stripe_customer_id || '-' || zendesk_user_id) AS distinct_combo
FROM customer360__customer_activity_metrics
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-054/attempt-01/sql/S25.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-054/attempt-01/sql/S25.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-054/attempt-01/results/S25.rows.jsonl)；完整：True；SHA256：`08f216373a2aaf41826ad33d073461693c17b833962fb7747bfff99874ac377b`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "customer360__customer_activity_metrics", "kind": "base", "block": null, "base_tables": ["customer360__customer_activity_metrics"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(DISTINCT marketo_lead_id \|\| '-' \|\| stripe_customer_id \|\| '-' \|\| zendesk_user_id) | [{"table": "customer360__customer_activity_metrics", "column": "zendesk_user_id"}, {"table": "customer360__customer_activity_metrics", "column": "stripe_customer_id"}, {"table": "customer360__customer_activity_metrics", "column": "marketo_lead_id"}] | [] | False |


## S26

类别 `data`；来源 `query_db`；调用 `6ffc2f8417204403bb54d8aebfc1e900`；状态 `success`。

```sql
SELECT COUNT(DISTINCT marketo_lead_id || '-' || stripe_customer_id || '-' || zendesk_user_id) AS distinct_combo
FROM customer360__conversion_funnel_analysis
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-054/attempt-01/sql/S26.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-054/attempt-01/sql/S26.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-054/attempt-01/results/S26.rows.jsonl)；完整：True；SHA256：`c1fd73d932ff759f5e941c045c4c6d772d20494a1140706678dfb979a0679557`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "customer360__conversion_funnel_analysis", "kind": "base", "block": null, "base_tables": ["customer360__conversion_funnel_analysis"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(DISTINCT marketo_lead_id \|\| '-' \|\| stripe_customer_id \|\| '-' \|\| zendesk_user_id) | [{"table": "customer360__conversion_funnel_analysis", "column": "zendesk_user_id"}, {"table": "customer360__conversion_funnel_analysis", "column": "stripe_customer_id"}, {"table": "customer360__conversion_funnel_analysis", "column": "marketo_lead_id"}] | [] | False |


## S27

类别 `data`；来源 `query_db`；调用 `8462c24471ba4ab5b1275c0502723702`；状态 `success`。

```sql
SELECT COUNT(DISTINCT activity_analysis_timestamp) AS distinct_ts_activity FROM customer360__customer_activity_metrics
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-054/attempt-01/sql/S27.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-054/attempt-01/sql/S27.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-054/attempt-01/results/S27.rows.jsonl)；完整：True；SHA256：`40f6972e8fdf792d24b2f2ef74ae57657e84c6b62b1e81e6a933c648e52b62fc`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "customer360__customer_activity_metrics", "kind": "base", "block": null, "base_tables": ["customer360__customer_activity_metrics"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(DISTINCT activity_analysis_timestamp) | [{"table": "customer360__customer_activity_metrics", "column": "activity_analysis_timestamp"}] | [] | False |


## S28

类别 `data`；来源 `query_db`；调用 `b0d34b5ebea04b77a15567ee90e56081`；状态 `success`。

```sql
SELECT COUNT(DISTINCT funnel_analysis_timestamp) AS distinct_ts_funnel FROM customer360__conversion_funnel_analysis
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-054/attempt-01/sql/S28.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-054/attempt-01/sql/S28.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-054/attempt-01/results/S28.rows.jsonl)；完整：True；SHA256：`d95e3d62b77dfee50a608e761dceabe0bdba5154fdc4a69f24fc9ee50c6ae3a4`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "customer360__conversion_funnel_analysis", "kind": "base", "block": null, "base_tables": ["customer360__conversion_funnel_analysis"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(DISTINCT funnel_analysis_timestamp) | [{"table": "customer360__conversion_funnel_analysis", "column": "funnel_analysis_timestamp"}] | [] | False |


## S29

类别 `data`；来源 `query_db`；调用 `b48ee380e4764b54a466c52b20a42115`；状态 `success`。

```sql
SELECT COUNT(DISTINCT analysis_timestamp) AS distinct_ts_value FROM customer360__customer_value_analysis
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-054/attempt-01/sql/S29.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-054/attempt-01/sql/S29.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-054/attempt-01/results/S29.rows.jsonl)；完整：True；SHA256：`29433440de3cbf6d261739003c6943be8c3f2086c8c7ba6f73f02e13236537d2`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "customer360__customer_value_analysis", "kind": "base", "block": null, "base_tables": ["customer360__customer_value_analysis"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(DISTINCT analysis_timestamp) | [{"table": "customer360__customer_value_analysis", "column": "analysis_timestamp"}] | [] | False |


## S30

类别 `data`；来源 `query_db`；调用 `ba7b50e17bc0455493e911e63042af2c`；状态 `success`。

```sql
SELECT COUNT(DISTINCT primary_email) AS distinct_emails_funnel FROM customer360__conversion_funnel_analysis
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-054/attempt-01/sql/S30.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-054/attempt-01/sql/S30.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-054/attempt-01/results/S30.rows.jsonl)；完整：True；SHA256：`361e90846ad23bd410a54f7ec8d2d4a212fd3b2c96a531d219a4fa54a6ac75ae`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "customer360__conversion_funnel_analysis", "kind": "base", "block": null, "base_tables": ["customer360__conversion_funnel_analysis"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(DISTINCT primary_email) | [{"table": "customer360__conversion_funnel_analysis", "column": "primary_email"}] | [] | False |


## S31

类别 `data`；来源 `query_db`；调用 `a414284c15464a01ae6a228c035001c4`；状态 `success`。

```sql
SELECT COUNT(DISTINCT primary_email) AS distinct_emails_activity FROM customer360__customer_activity_metrics
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-054/attempt-01/sql/S31.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-054/attempt-01/sql/S31.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-054/attempt-01/results/S31.rows.jsonl)；完整：True；SHA256：`361e90846ad23bd410a54f7ec8d2d4a212fd3b2c96a531d219a4fa54a6ac75ae`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "customer360__customer_activity_metrics", "kind": "base", "block": null, "base_tables": ["customer360__customer_activity_metrics"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(DISTINCT primary_email) | [{"table": "customer360__customer_activity_metrics", "column": "primary_email"}] | [] | False |


## S32

类别 `data`；来源 `query_db`；调用 `ea1cf0fdc2df40f480b16b8cd6c95555`；状态 `success`。

```sql
SELECT COUNT(DISTINCT primary_email) AS distinct_emails_value FROM customer360__customer_value_analysis
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-054/attempt-01/sql/S32.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-054/attempt-01/sql/S32.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-054/attempt-01/results/S32.rows.jsonl)；完整：True；SHA256：`361e90846ad23bd410a54f7ec8d2d4a212fd3b2c96a531d219a4fa54a6ac75ae`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "customer360__customer_value_analysis", "kind": "base", "block": null, "base_tables": ["customer360__customer_value_analysis"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(DISTINCT primary_email) | [{"table": "customer360__customer_value_analysis", "column": "primary_email"}] | [] | False |


## S33

类别 `data`；来源 `query_db`；调用 `5ac3b4fd03df4c7c92875b8e6ad700e1`；状态 `success`。

```sql
-- Get the latest activity record per email
SELECT primary_email, composite_engagement_score, in_marketo, in_stripe, in_zendesk, 
       zendesk_active, primary_engagement_channel, customer_health_score,
       activity_risk_level, engagement_velocity
FROM (
  SELECT *, ROW_NUMBER() OVER (PARTITION BY primary_email ORDER BY activity_analysis_timestamp DESC) AS rn
  FROM customer360__customer_activity_metrics
) WHERE rn = 1
LIMIT 10
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-054/attempt-01/sql/S33.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-054/attempt-01/sql/S33.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-054/attempt-01/results/S33.rows.jsonl)；完整：True；SHA256：`40c9bcddb2b546ea0fa34e0115d02689b2f6b697994927f39a64f5e04ae7b9c4`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "customer360__customer_activity_metrics", "kind": "base", "block": null, "base_tables": ["customer360__customer_activity_metrics"]}] | [] | [] |
| B2 | [{"alias": "", "kind": "derived", "block": "B1", "base_tables": ["customer360__customer_activity_metrics"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |


## S34

类别 `data`；来源 `query_db`；调用 `0e6935d8a71c485693453944abfabc4b`；状态 `success`。

```sql
-- Get the latest funnel record per email
SELECT primary_email, marketing_to_sales_days, sales_to_support_days, customer_tier, estimated_customer_ltv
FROM (
  SELECT *, ROW_NUMBER() OVER (PARTITION BY primary_email ORDER BY funnel_analysis_timestamp DESC) AS rn
  FROM customer360__conversion_funnel_analysis
) WHERE rn = 1
LIMIT 10
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-054/attempt-01/sql/S34.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-054/attempt-01/sql/S34.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-054/attempt-01/results/S34.rows.jsonl)；完整：True；SHA256：`c2091ae547ad2f320edf6875b02674e31a36aca6d96e83c94b87161541c99e58`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "customer360__conversion_funnel_analysis", "kind": "base", "block": null, "base_tables": ["customer360__conversion_funnel_analysis"]}] | [] | [] |
| B2 | [{"alias": "", "kind": "derived", "block": "B1", "base_tables": ["customer360__conversion_funnel_analysis"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |


## S35

类别 `data`；来源 `query_db`；调用 `d87f68ec506d47df9a80672331cb5138`；状态 `success`。

```sql
-- Build the cohort: latest records per email joined together
WITH latest_activity AS (
  SELECT *, ROW_NUMBER() OVER (PARTITION BY primary_email ORDER BY activity_analysis_timestamp DESC) AS rn
  FROM customer360__customer_activity_metrics
),
latest_funnel AS (
  SELECT *, ROW_NUMBER() OVER (PARTITION BY primary_email ORDER BY funnel_analysis_timestamp DESC) AS rn
  FROM customer360__conversion_funnel_analysis
),
latest_value AS (
  SELECT *, ROW_NUMBER() OVER (PARTITION BY primary_email ORDER BY analysis_timestamp DESC) AS rn
  FROM customer360__customer_value_analysis
),
cohort AS (
  SELECT a.primary_email, a.composite_engagement_score, 
         f.marketing_to_sales_days, f.sales_to_support_days,
         f.customer_tier, f.estimated_customer_ltv AS funnel_ltv,
         v.recency_score, v.frequency_score, v.monetary_score,
         v.estimated_customer_ltv AS value_ltv,
         a.primary_engagement_channel, a.zendesk_active,
         a.in_marketo, a.in_stripe, a.in_zendesk,
         a.customer_health_score, a.activity_risk_level, a.engagement_velocity,
         a.customer_segment, a.lifecycle_stage
  FROM latest_activity a
  JOIN latest_funnel f ON a.primary_email = f.primary_email AND f.rn = 1
  JOIN latest_value v ON a.primary_email = v.primary_email AND v.rn = 1
  WHERE a.rn = 1
    AND f.marketing_to_sales_days BETWEEN 10 AND 20
    AND f.sales_to_support_days > 30
    AND a.composite_engagement_score > (SELECT AVG(composite_engagement_score) FROM customer360__customer_activity_metrics)
)
SELECT COUNT(*) AS cohort_count FROM cohort
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-054/attempt-01/sql/S35.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-054/attempt-01/sql/S35.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-054/attempt-01/results/S35.rows.jsonl)；完整：True；SHA256：`02bfbb2fc9acb5817dbee70996708cda3ea3ca09f9cee9a29c3a9ee5da60e23d`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "customer360__customer_activity_metrics", "kind": "base", "block": null, "base_tables": ["customer360__customer_activity_metrics"]}] | [] | [] |
| B2 | [{"alias": "customer360__conversion_funnel_analysis", "kind": "base", "block": null, "base_tables": ["customer360__conversion_funnel_analysis"]}] | [] | [] |
| B3 | [{"alias": "customer360__customer_value_analysis", "kind": "base", "block": null, "base_tables": ["customer360__customer_value_analysis"]}] | [] | [] |
| B4 | [{"alias": "customer360__customer_activity_metrics", "kind": "base", "block": null, "base_tables": ["customer360__customer_activity_metrics"]}] | [] | [] |
| B5 | [{"alias": "a", "kind": "derived", "block": "B1", "base_tables": ["customer360__customer_activity_metrics"]}, {"alias": "f", "kind": "derived", "block": "B2", "base_tables": ["customer360__conversion_funnel_analysis"]}, {"alias": "v", "kind": "derived", "block": "B3", "base_tables": ["customer360__customer_value_analysis"]}] | [{"type": "INNER", "right": "latest_funnel AS f", "on": "a.primary_email = f.primary_email AND f.rn = 1", "using": []}, {"type": "INNER", "right": "latest_value AS v", "on": "a.primary_email = v.primary_email AND v.rn = 1", "using": []}] | [] |
| B6 | [{"alias": "cohort", "kind": "derived", "block": "B5", "base_tables": ["customer360__conversion_funnel_analysis", "customer360__customer_activity_metrics", "customer360__customer_value_analysis"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B4 | AVG(composite_engagement_score) | [{"table": "customer360__customer_activity_metrics", "column": "composite_engagement_score"}] | [] | False |
| B6 | COUNT(*) | [] | [] | True |


未解析列血缘：[{"block": "B5", "column": "composite_engagement_score", "reason": "ambiguous_or_missing_source"}]

## S36

类别 `data`；来源 `query_db`；调用 `70bfe13e0dd643fe9e96c6f913df4768`；状态 `success`。

```sql
-- Full cohort analysis
WITH latest_activity AS (
  SELECT *, ROW_NUMBER() OVER (PARTITION BY primary_email ORDER BY activity_analysis_timestamp DESC) AS rn
  FROM customer360__customer_activity_metrics
),
latest_funnel AS (
  SELECT *, ROW_NUMBER() OVER (PARTITION BY primary_email ORDER BY funnel_analysis_timestamp DESC) AS rn
  FROM customer360__conversion_funnel_analysis
),
latest_value AS (
  SELECT *, ROW_NUMBER() OVER (PARTITION BY primary_email ORDER BY analysis_timestamp DESC) AS rn
  FROM customer360__customer_value_analysis
),
cohort AS (
  SELECT a.primary_email, a.composite_engagement_score, 
         f.marketing_to_sales_days, f.sales_to_support_days,
         f.customer_tier, f.estimated_customer_ltv AS funnel_ltv,
         v.recency_score, v.frequency_score, v.monetary_score,
         v.estimated_customer_ltv AS value_ltv,
         a.primary_engagement_channel, a.zendesk_active,
         a.in_marketo, a.in_stripe, a.in_zendesk,
         a.customer_health_score, a.activity_risk_level, a.engagement_velocity,
         a.customer_segment, a.lifecycle_stage
  FROM latest_activity a
  JOIN latest_funnel f ON a.primary_email = f.primary_email AND f.rn = 1
  JOIN latest_value v ON a.primary_email = v.primary_email AND v.rn = 1
  WHERE a.rn = 1
    AND f.marketing_to_sales_days BETWEEN 10 AND 20
    AND f.sales_to_support_days > 30
    AND a.composite_engagement_score > (SELECT AVG(composite_engagement_score) FROM customer360__customer_activity_metrics)
)
SELECT 
  COUNT(*) AS cohort_count,
  AVG(recency_score) AS avg_recency_score,
  AVG(frequency_score) AS avg_frequency_score,
  AVG(monetary_score) AS avg_monetary_score,
  AVG(composite_engagement_score) AS avg_engagement_score,
  AVG(marketing_to_sales_days) AS avg_marketing_to_sales_days,
  AVG(sales_to_support_days) AS avg_sales_to_support_days
FROM cohort
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-054/attempt-01/sql/S36.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-054/attempt-01/sql/S36.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-054/attempt-01/results/S36.rows.jsonl)；完整：True；SHA256：`9a36232c485a166a37d58d797a210fffc0c218416efabf1b2b0fb262ba9368a2`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "customer360__customer_activity_metrics", "kind": "base", "block": null, "base_tables": ["customer360__customer_activity_metrics"]}] | [] | [] |
| B2 | [{"alias": "customer360__conversion_funnel_analysis", "kind": "base", "block": null, "base_tables": ["customer360__conversion_funnel_analysis"]}] | [] | [] |
| B3 | [{"alias": "customer360__customer_value_analysis", "kind": "base", "block": null, "base_tables": ["customer360__customer_value_analysis"]}] | [] | [] |
| B4 | [{"alias": "customer360__customer_activity_metrics", "kind": "base", "block": null, "base_tables": ["customer360__customer_activity_metrics"]}] | [] | [] |
| B5 | [{"alias": "a", "kind": "derived", "block": "B1", "base_tables": ["customer360__customer_activity_metrics"]}, {"alias": "f", "kind": "derived", "block": "B2", "base_tables": ["customer360__conversion_funnel_analysis"]}, {"alias": "v", "kind": "derived", "block": "B3", "base_tables": ["customer360__customer_value_analysis"]}] | [{"type": "INNER", "right": "latest_funnel AS f", "on": "a.primary_email = f.primary_email AND f.rn = 1", "using": []}, {"type": "INNER", "right": "latest_value AS v", "on": "a.primary_email = v.primary_email AND v.rn = 1", "using": []}] | [] |
| B6 | [{"alias": "cohort", "kind": "derived", "block": "B5", "base_tables": ["customer360__conversion_funnel_analysis", "customer360__customer_activity_metrics", "customer360__customer_value_analysis"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B4 | AVG(composite_engagement_score) | [{"table": "customer360__customer_activity_metrics", "column": "composite_engagement_score"}] | [] | False |
| B6 | COUNT(*) | [] | [] | True |
| B6 | AVG(recency_score) | [{"table": "customer360__customer_value_analysis", "column": "recency_score"}] | [] | False |
| B6 | AVG(frequency_score) | [{"table": "customer360__customer_value_analysis", "column": "frequency_score"}] | [] | False |
| B6 | AVG(monetary_score) | [{"table": "customer360__customer_value_analysis", "column": "monetary_score"}] | [] | False |
| B6 | AVG(composite_engagement_score) | [{"table": "customer360__customer_activity_metrics", "column": "composite_engagement_score"}] | [] | False |
| B6 | AVG(marketing_to_sales_days) | [{"table": "customer360__conversion_funnel_analysis", "column": "marketing_to_sales_days"}] | [] | False |
| B6 | AVG(sales_to_support_days) | [{"table": "customer360__conversion_funnel_analysis", "column": "sales_to_support_days"}] | [] | False |


未解析列血缘：[{"block": "B5", "column": "composite_engagement_score", "reason": "ambiguous_or_missing_source"}]

## S37

类别 `data`；来源 `query_db`；调用 `0bfa1143073340ba92279741ce553cec`；状态 `success`。

```sql
-- Calculate LTV difference vs others in same tier
WITH latest_activity AS (
  SELECT *, ROW_NUMBER() OVER (PARTITION BY primary_email ORDER BY activity_analysis_timestamp DESC) AS rn
  FROM customer360__customer_activity_metrics
),
latest_funnel AS (
  SELECT *, ROW_NUMBER() OVER (PARTITION BY primary_email ORDER BY funnel_analysis_timestamp DESC) AS rn
  FROM customer360__conversion_funnel_analysis
),
latest_value AS (
  SELECT *, ROW_NUMBER() OVER (PARTITION BY primary_email ORDER BY analysis_timestamp DESC) AS rn
  FROM customer360__customer_value_analysis
),
combined AS (
  SELECT a.primary_email, a.composite_engagement_score, 
         f.marketing_to_sales_days, f.sales_to_support_days,
         f.customer_tier, f.estimated_customer_ltv AS funnel_ltv,
         v.recency_score, v.frequency_score, v.monetary_score,
         v.estimated_customer_ltv AS value_ltv,
         a.primary_engagement_channel, a.zendesk_active,
         a.in_marketo, a.in_stripe, a.in_zendesk,
         a.customer_health_score, a.activity_risk_level, a.engagement_velocity,
         a.customer_segment, a.lifecycle_stage
  FROM latest_activity a
  JOIN latest_funnel f ON a.primary_email = f.primary_email AND f.rn = 1
  JOIN latest_value v ON a.primary_email = v.primary_email AND v.rn = 1
  WHERE a.rn = 1
),
cohort AS (
  SELECT * FROM combined
  WHERE marketing_to_sales_days BETWEEN 10 AND 20
    AND sales_to_support_days > 30
    AND composite_engagement_score > (SELECT AVG(composite_engagement_score) FROM customer360__customer_activity_metrics)
),
tier_avg_ltv AS (
  SELECT customer_tier, AVG(funnel_ltv) AS tier_avg_ltv
  FROM combined
  GROUP BY customer_tier
)
SELECT c.customer_tier, 
       COUNT(*) AS cohort_in_tier,
       AVG(c.funnel_ltv) AS cohort_avg_ltv,
       AVG(t.tier_avg_ltv) AS tier_avg_ltv,
       AVG(c.funnel_ltv) - AVG(t.tier_avg_ltv) AS ltv_difference
FROM cohort c
JOIN tier_avg_ltv t ON c.customer_tier = t.customer_tier
GROUP BY c.customer_tier
ORDER BY c.customer_tier
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-054/attempt-01/sql/S37.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-054/attempt-01/sql/S37.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-054/attempt-01/results/S37.rows.jsonl)；完整：True；SHA256：`425388a3a52eaa2fdd2f40fdb465a3c830215615760083aa50874d333e7b31db`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "customer360__customer_activity_metrics", "kind": "base", "block": null, "base_tables": ["customer360__customer_activity_metrics"]}] | [] | [] |
| B2 | [{"alias": "customer360__conversion_funnel_analysis", "kind": "base", "block": null, "base_tables": ["customer360__conversion_funnel_analysis"]}] | [] | [] |
| B3 | [{"alias": "customer360__customer_value_analysis", "kind": "base", "block": null, "base_tables": ["customer360__customer_value_analysis"]}] | [] | [] |
| B4 | [{"alias": "a", "kind": "derived", "block": "B1", "base_tables": ["customer360__customer_activity_metrics"]}, {"alias": "f", "kind": "derived", "block": "B2", "base_tables": ["customer360__conversion_funnel_analysis"]}, {"alias": "v", "kind": "derived", "block": "B3", "base_tables": ["customer360__customer_value_analysis"]}] | [{"type": "INNER", "right": "latest_funnel AS f", "on": "a.primary_email = f.primary_email AND f.rn = 1", "using": []}, {"type": "INNER", "right": "latest_value AS v", "on": "a.primary_email = v.primary_email AND v.rn = 1", "using": []}] | [] |
| B5 | [{"alias": "customer360__customer_activity_metrics", "kind": "base", "block": null, "base_tables": ["customer360__customer_activity_metrics"]}] | [] | [] |
| B6 | [{"alias": "combined", "kind": "derived", "block": "B4", "base_tables": ["customer360__conversion_funnel_analysis", "customer360__customer_activity_metrics", "customer360__customer_value_analysis"]}] | [] | [] |
| B7 | [{"alias": "combined", "kind": "derived", "block": "B4", "base_tables": ["customer360__conversion_funnel_analysis", "customer360__customer_activity_metrics", "customer360__customer_value_analysis"]}] | [] | ["customer_tier"] |
| B8 | [{"alias": "c", "kind": "derived", "block": "B6", "base_tables": ["customer360__conversion_funnel_analysis", "customer360__customer_activity_metrics", "customer360__customer_value_analysis"]}, {"alias": "t", "kind": "derived", "block": "B7", "base_tables": ["customer360__conversion_funnel_analysis", "customer360__customer_activity_metrics", "customer360__customer_value_analysis"]}] | [{"type": "INNER", "right": "tier_avg_ltv AS t", "on": "c.customer_tier = t.customer_tier", "using": []}] | ["c.customer_tier"] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B5 | AVG(composite_engagement_score) | [{"table": "customer360__customer_activity_metrics", "column": "composite_engagement_score"}] | [] | False |
| B7 | AVG(funnel_ltv) | [{"table": "customer360__conversion_funnel_analysis", "column": "estimated_customer_ltv"}] | [] | False |
| B8 | COUNT(*) | [] | [] | True |
| B8 | AVG(c.funnel_ltv) | [{"table": "customer360__conversion_funnel_analysis", "column": "estimated_customer_ltv"}] | [] | False |
| B8 | AVG(t.tier_avg_ltv) | [{"table": "customer360__conversion_funnel_analysis", "column": "estimated_customer_ltv"}] | [] | False |
| B8 | AVG(c.funnel_ltv) | [{"table": "customer360__conversion_funnel_analysis", "column": "estimated_customer_ltv"}] | [] | False |
| B8 | AVG(t.tier_avg_ltv) | [{"table": "customer360__conversion_funnel_analysis", "column": "estimated_customer_ltv"}] | [] | False |


## S38

类别 `data`；来源 `query_db`；调用 `718b665519a541e9bc3441eba12225ed`；状态 `success`。

```sql
-- Precise LTV difference: cohort LTV minus avg LTV of OTHER (non-cohort) customers in same tier
WITH latest_activity AS (
  SELECT *, ROW_NUMBER() OVER (PARTITION BY primary_email ORDER BY activity_analysis_timestamp DESC) AS rn
  FROM customer360__customer_activity_metrics
),
latest_funnel AS (
  SELECT *, ROW_NUMBER() OVER (PARTITION BY primary_email ORDER BY funnel_analysis_timestamp DESC) AS rn
  FROM customer360__conversion_funnel_analysis
),
latest_value AS (
  SELECT *, ROW_NUMBER() OVER (PARTITION BY primary_email ORDER BY analysis_timestamp DESC) AS rn
  FROM customer360__customer_value_analysis
),
combined AS (
  SELECT a.primary_email, a.composite_engagement_score, 
         f.marketing_to_sales_days, f.sales_to_support_days,
         f.customer_tier, f.estimated_customer_ltv AS funnel_ltv,
         a.primary_engagement_channel, a.zendesk_active,
         a.in_marketo, a.in_stripe, a.in_zendesk,
         a.customer_health_score, a.activity_risk_level, a.engagement_velocity,
         a.customer_segment, a.lifecycle_stage
  FROM latest_activity a
  JOIN latest_funnel f ON a.primary_email = f.primary_email AND f.rn = 1
  JOIN latest_value v ON a.primary_email = v.primary_email AND v.rn = 1
  WHERE a.rn = 1
),
cohort AS (
  SELECT * FROM combined
  WHERE marketing_to_sales_days BETWEEN 10 AND 20
    AND sales_to_support_days > 30
    AND composite_engagement_score > (SELECT AVG(composite_engagement_score) FROM customer360__customer_activity_metrics)
),
non_cohort_tier_avg AS (
  SELECT c2.customer_tier, AVG(c2.funnel_ltv) AS non_cohort_tier_avg_ltv
  FROM combined c2
  WHERE c2.primary_email NOT IN (SELECT primary_email FROM cohort)
  GROUP BY c2.customer_tier
)
SELECT c.customer_tier,
       COUNT(*) AS cohort_in_tier,
       AVG(c.funnel_ltv) AS cohort_avg_ltv,
       AVG(t.non_cohort_tier_avg_ltv) AS non_cohort_tier_avg_ltv,
       AVG(c.funnel_ltv - t.non_cohort_tier_avg_ltv) AS avg_ltv_diff_vs_others
FROM cohort c
JOIN non_cohort_tier_avg t ON c.customer_tier = t.customer_tier
GROUP BY c.customer_tier
ORDER BY c.customer_tier
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-054/attempt-01/sql/S38.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-054/attempt-01/sql/S38.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-054/attempt-01/results/S38.rows.jsonl)；完整：True；SHA256：`8c54272420027c9067a1b7e0b7bfe54c6d092abd86ebd06cfac613fd84fac033`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "customer360__customer_activity_metrics", "kind": "base", "block": null, "base_tables": ["customer360__customer_activity_metrics"]}] | [] | [] |
| B2 | [{"alias": "customer360__conversion_funnel_analysis", "kind": "base", "block": null, "base_tables": ["customer360__conversion_funnel_analysis"]}] | [] | [] |
| B3 | [{"alias": "customer360__customer_value_analysis", "kind": "base", "block": null, "base_tables": ["customer360__customer_value_analysis"]}] | [] | [] |
| B4 | [{"alias": "a", "kind": "derived", "block": "B1", "base_tables": ["customer360__customer_activity_metrics"]}, {"alias": "f", "kind": "derived", "block": "B2", "base_tables": ["customer360__conversion_funnel_analysis"]}, {"alias": "v", "kind": "derived", "block": "B3", "base_tables": ["customer360__customer_value_analysis"]}] | [{"type": "INNER", "right": "latest_funnel AS f", "on": "a.primary_email = f.primary_email AND f.rn = 1", "using": []}, {"type": "INNER", "right": "latest_value AS v", "on": "a.primary_email = v.primary_email AND v.rn = 1", "using": []}] | [] |
| B5 | [{"alias": "customer360__customer_activity_metrics", "kind": "base", "block": null, "base_tables": ["customer360__customer_activity_metrics"]}] | [] | [] |
| B6 | [{"alias": "combined", "kind": "derived", "block": "B4", "base_tables": ["customer360__conversion_funnel_analysis", "customer360__customer_activity_metrics", "customer360__customer_value_analysis"]}] | [] | [] |
| B7 | [{"alias": "cohort", "kind": "derived", "block": "B6", "base_tables": ["customer360__conversion_funnel_analysis", "customer360__customer_activity_metrics", "customer360__customer_value_analysis"]}] | [] | [] |
| B8 | [{"alias": "c2", "kind": "derived", "block": "B4", "base_tables": ["customer360__conversion_funnel_analysis", "customer360__customer_activity_metrics", "customer360__customer_value_analysis"]}] | [] | ["c2.customer_tier"] |
| B9 | [{"alias": "c", "kind": "derived", "block": "B6", "base_tables": ["customer360__conversion_funnel_analysis", "customer360__customer_activity_metrics", "customer360__customer_value_analysis"]}, {"alias": "t", "kind": "derived", "block": "B8", "base_tables": ["customer360__conversion_funnel_analysis", "customer360__customer_activity_metrics", "customer360__customer_value_analysis"]}] | [{"type": "INNER", "right": "non_cohort_tier_avg AS t", "on": "c.customer_tier = t.customer_tier", "using": []}] | ["c.customer_tier"] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B5 | AVG(composite_engagement_score) | [{"table": "customer360__customer_activity_metrics", "column": "composite_engagement_score"}] | [] | False |
| B8 | AVG(c2.funnel_ltv) | [{"table": "customer360__conversion_funnel_analysis", "column": "estimated_customer_ltv"}] | [] | False |
| B9 | COUNT(*) | [] | [] | True |
| B9 | AVG(c.funnel_ltv) | [{"table": "customer360__conversion_funnel_analysis", "column": "estimated_customer_ltv"}] | [] | False |
| B9 | AVG(t.non_cohort_tier_avg_ltv) | [{"table": "customer360__conversion_funnel_analysis", "column": "estimated_customer_ltv"}] | [] | False |
| B9 | AVG(c.funnel_ltv - t.non_cohort_tier_avg_ltv) | [{"table": "customer360__conversion_funnel_analysis", "column": "estimated_customer_ltv"}, {"table": "customer360__conversion_funnel_analysis", "column": "estimated_customer_ltv"}] | [] | False |


## S39

类别 `data`；来源 `query_db`；调用 `6f00478500e84afe80aca98e0470cb8c`；状态 `success`。

```sql
-- Overall average LTV difference
WITH latest_activity AS (
  SELECT *, ROW_NUMBER() OVER (PARTITION BY primary_email ORDER BY activity_analysis_timestamp DESC) AS rn
  FROM customer360__customer_activity_metrics
),
latest_funnel AS (
  SELECT *, ROW_NUMBER() OVER (PARTITION BY primary_email ORDER BY funnel_analysis_timestamp DESC) AS rn
  FROM customer360__conversion_funnel_analysis
),
latest_value AS (
  SELECT *, ROW_NUMBER() OVER (PARTITION BY primary_email ORDER BY analysis_timestamp DESC) AS rn
  FROM customer360__customer_value_analysis
),
combined AS (
  SELECT a.primary_email, a.composite_engagement_score, 
         f.marketing_to_sales_days, f.sales_to_support_days,
         f.customer_tier, f.estimated_customer_ltv AS funnel_ltv,
         a.primary_engagement_channel, a.zendesk_active,
         a.in_marketo, a.in_stripe, a.in_zendesk,
         a.customer_health_score, a.activity_risk_level, a.engagement_velocity,
         a.customer_segment, a.lifecycle_stage
  FROM latest_activity a
  JOIN latest_funnel f ON a.primary_email = f.primary_email AND f.rn = 1
  JOIN latest_value v ON a.primary_email = v.primary_email AND v.rn = 1
  WHERE a.rn = 1
),
cohort AS (
  SELECT * FROM combined
  WHERE marketing_to_sales_days BETWEEN 10 AND 20
    AND sales_to_support_days > 30
    AND composite_engagement_score > (SELECT AVG(composite_engagement_score) FROM customer360__customer_activity_metrics)
),
non_cohort_tier_avg AS (
  SELECT c2.customer_tier, AVG(c2.funnel_ltv) AS non_cohort_tier_avg_ltv
  FROM combined c2
  WHERE c2.primary_email NOT IN (SELECT primary_email FROM cohort)
  GROUP BY c2.customer_tier
)
SELECT AVG(c.funnel_ltv - t.non_cohort_tier_avg_ltv) AS overall_avg_ltv_diff
FROM cohort c
JOIN non_cohort_tier_avg t ON c.customer_tier = t.customer_tier
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-054/attempt-01/sql/S39.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-054/attempt-01/sql/S39.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-054/attempt-01/results/S39.rows.jsonl)；完整：True；SHA256：`e1585c74133df1fb2d363f0bfd9ea2f503c78ea2359c8b19eec281ce9d707ef3`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "customer360__customer_activity_metrics", "kind": "base", "block": null, "base_tables": ["customer360__customer_activity_metrics"]}] | [] | [] |
| B2 | [{"alias": "customer360__conversion_funnel_analysis", "kind": "base", "block": null, "base_tables": ["customer360__conversion_funnel_analysis"]}] | [] | [] |
| B3 | [{"alias": "customer360__customer_value_analysis", "kind": "base", "block": null, "base_tables": ["customer360__customer_value_analysis"]}] | [] | [] |
| B4 | [{"alias": "a", "kind": "derived", "block": "B1", "base_tables": ["customer360__customer_activity_metrics"]}, {"alias": "f", "kind": "derived", "block": "B2", "base_tables": ["customer360__conversion_funnel_analysis"]}, {"alias": "v", "kind": "derived", "block": "B3", "base_tables": ["customer360__customer_value_analysis"]}] | [{"type": "INNER", "right": "latest_funnel AS f", "on": "a.primary_email = f.primary_email AND f.rn = 1", "using": []}, {"type": "INNER", "right": "latest_value AS v", "on": "a.primary_email = v.primary_email AND v.rn = 1", "using": []}] | [] |
| B5 | [{"alias": "customer360__customer_activity_metrics", "kind": "base", "block": null, "base_tables": ["customer360__customer_activity_metrics"]}] | [] | [] |
| B6 | [{"alias": "combined", "kind": "derived", "block": "B4", "base_tables": ["customer360__conversion_funnel_analysis", "customer360__customer_activity_metrics", "customer360__customer_value_analysis"]}] | [] | [] |
| B7 | [{"alias": "cohort", "kind": "derived", "block": "B6", "base_tables": ["customer360__conversion_funnel_analysis", "customer360__customer_activity_metrics", "customer360__customer_value_analysis"]}] | [] | [] |
| B8 | [{"alias": "c2", "kind": "derived", "block": "B4", "base_tables": ["customer360__conversion_funnel_analysis", "customer360__customer_activity_metrics", "customer360__customer_value_analysis"]}] | [] | ["c2.customer_tier"] |
| B9 | [{"alias": "c", "kind": "derived", "block": "B6", "base_tables": ["customer360__conversion_funnel_analysis", "customer360__customer_activity_metrics", "customer360__customer_value_analysis"]}, {"alias": "t", "kind": "derived", "block": "B8", "base_tables": ["customer360__conversion_funnel_analysis", "customer360__customer_activity_metrics", "customer360__customer_value_analysis"]}] | [{"type": "INNER", "right": "non_cohort_tier_avg AS t", "on": "c.customer_tier = t.customer_tier", "using": []}] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B5 | AVG(composite_engagement_score) | [{"table": "customer360__customer_activity_metrics", "column": "composite_engagement_score"}] | [] | False |
| B8 | AVG(c2.funnel_ltv) | [{"table": "customer360__conversion_funnel_analysis", "column": "estimated_customer_ltv"}] | [] | False |
| B9 | AVG(c.funnel_ltv - t.non_cohort_tier_avg_ltv) | [{"table": "customer360__conversion_funnel_analysis", "column": "estimated_customer_ltv"}, {"table": "customer360__conversion_funnel_analysis", "column": "estimated_customer_ltv"}] | [] | False |


## S40

类别 `data`；来源 `query_db`；调用 `c274a525bda14dc2b191c5c4a290ac31`；状态 `success`。

```sql
-- Distribution of primary_engagement_channel
WITH latest_activity AS (
  SELECT *, ROW_NUMBER() OVER (PARTITION BY primary_email ORDER BY activity_analysis_timestamp DESC) AS rn
  FROM customer360__customer_activity_metrics
),
latest_funnel AS (
  SELECT *, ROW_NUMBER() OVER (PARTITION BY primary_email ORDER BY funnel_analysis_timestamp DESC) AS rn
  FROM customer360__conversion_funnel_analysis
),
latest_value AS (
  SELECT *, ROW_NUMBER() OVER (PARTITION BY primary_email ORDER BY analysis_timestamp DESC) AS rn
  FROM customer360__customer_value_analysis
),
cohort AS (
  SELECT a.primary_email, a.composite_engagement_score, 
         f.marketing_to_sales_days, f.sales_to_support_days,
         f.customer_tier, f.estimated_customer_ltv AS funnel_ltv,
         a.primary_engagement_channel, a.zendesk_active,
         a.in_marketo, a.in_stripe, a.in_zendesk,
         a.customer_health_score, a.activity_risk_level, a.engagement_velocity
  FROM latest_activity a
  JOIN latest_funnel f ON a.primary_email = f.primary_email AND f.rn = 1
  JOIN latest_value v ON a.primary_email = v.primary_email AND v.rn = 1
  WHERE a.rn = 1
    AND f.marketing_to_sales_days BETWEEN 10 AND 20
    AND f.sales_to_support_days > 30
    AND a.composite_engagement_score > (SELECT AVG(composite_engagement_score) FROM customer360__customer_activity_metrics)
)
SELECT primary_engagement_channel, COUNT(*) AS cnt, 
       ROUND(100.0 * COUNT(*) / (SELECT COUNT(*) FROM cohort), 2) AS pct
FROM cohort
GROUP BY primary_engagement_channel
ORDER BY cnt DESC
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-054/attempt-01/sql/S40.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-054/attempt-01/sql/S40.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-054/attempt-01/results/S40.rows.jsonl)；完整：True；SHA256：`176e7223bd236b7f47ffe257769ae5596fc36cf3cc75f682d2098c4675a35d58`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "customer360__customer_activity_metrics", "kind": "base", "block": null, "base_tables": ["customer360__customer_activity_metrics"]}] | [] | [] |
| B2 | [{"alias": "customer360__conversion_funnel_analysis", "kind": "base", "block": null, "base_tables": ["customer360__conversion_funnel_analysis"]}] | [] | [] |
| B3 | [{"alias": "customer360__customer_value_analysis", "kind": "base", "block": null, "base_tables": ["customer360__customer_value_analysis"]}] | [] | [] |
| B4 | [{"alias": "customer360__customer_activity_metrics", "kind": "base", "block": null, "base_tables": ["customer360__customer_activity_metrics"]}] | [] | [] |
| B5 | [{"alias": "a", "kind": "derived", "block": "B1", "base_tables": ["customer360__customer_activity_metrics"]}, {"alias": "f", "kind": "derived", "block": "B2", "base_tables": ["customer360__conversion_funnel_analysis"]}, {"alias": "v", "kind": "derived", "block": "B3", "base_tables": ["customer360__customer_value_analysis"]}] | [{"type": "INNER", "right": "latest_funnel AS f", "on": "a.primary_email = f.primary_email AND f.rn = 1", "using": []}, {"type": "INNER", "right": "latest_value AS v", "on": "a.primary_email = v.primary_email AND v.rn = 1", "using": []}] | [] |
| B6 | [{"alias": "cohort", "kind": "derived", "block": "B5", "base_tables": ["customer360__conversion_funnel_analysis", "customer360__customer_activity_metrics", "customer360__customer_value_analysis"]}] | [] | [] |
| B7 | [{"alias": "cohort", "kind": "derived", "block": "B5", "base_tables": ["customer360__conversion_funnel_analysis", "customer360__customer_activity_metrics", "customer360__customer_value_analysis"]}] | [] | ["primary_engagement_channel"] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B4 | AVG(composite_engagement_score) | [{"table": "customer360__customer_activity_metrics", "column": "composite_engagement_score"}] | [] | False |
| B6 | COUNT(*) | [] | [] | True |
| B7 | COUNT(*) | [] | [] | True |
| B7 | COUNT(*) | [] | [] | True |


未解析列血缘：[{"block": "B5", "column": "composite_engagement_score", "reason": "ambiguous_or_missing_source"}]

## S41

类别 `data`；来源 `query_db`；调用 `2bbabe8d79294f4a8fa873321d9b737e`；状态 `success`。

```sql
-- Proportion of zendesk_active
WITH latest_activity AS (
  SELECT *, ROW_NUMBER() OVER (PARTITION BY primary_email ORDER BY activity_analysis_timestamp DESC) AS rn
  FROM customer360__customer_activity_metrics
),
latest_funnel AS (
  SELECT *, ROW_NUMBER() OVER (PARTITION BY primary_email ORDER BY funnel_analysis_timestamp DESC) AS rn
  FROM customer360__conversion_funnel_analysis
),
latest_value AS (
  SELECT *, ROW_NUMBER() OVER (PARTITION BY primary_email ORDER BY analysis_timestamp DESC) AS rn
  FROM customer360__customer_value_analysis
),
cohort AS (
  SELECT a.primary_email, a.composite_engagement_score, 
         f.marketing_to_sales_days, f.sales_to_support_days,
         f.customer_tier, f.estimated_customer_ltv AS funnel_ltv,
         a.primary_engagement_channel, a.zendesk_active,
         a.in_marketo, a.in_stripe, a.in_zendesk,
         a.customer_health_score, a.activity_risk_level, a.engagement_velocity
  FROM latest_activity a
  JOIN latest_funnel f ON a.primary_email = f.primary_email AND f.rn = 1
  JOIN latest_value v ON a.primary_email = v.primary_email AND v.rn = 1
  WHERE a.rn = 1
    AND f.marketing_to_sales_days BETWEEN 10 AND 20
    AND f.sales_to_support_days > 30
    AND a.composite_engagement_score > (SELECT AVG(composite_engagement_score) FROM customer360__customer_activity_metrics)
)
SELECT zendesk_active, COUNT(*) AS cnt, 
       ROUND(100.0 * COUNT(*) / (SELECT COUNT(*) FROM cohort), 2) AS pct
FROM cohort
GROUP BY zendesk_active
ORDER BY zendesk_active
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-054/attempt-01/sql/S41.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-054/attempt-01/sql/S41.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-054/attempt-01/results/S41.rows.jsonl)；完整：True；SHA256：`ea1b4593518cfc1e34e303bc5855c4a65c5db29e68bade7e89ee950fa338f476`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "customer360__customer_activity_metrics", "kind": "base", "block": null, "base_tables": ["customer360__customer_activity_metrics"]}] | [] | [] |
| B2 | [{"alias": "customer360__conversion_funnel_analysis", "kind": "base", "block": null, "base_tables": ["customer360__conversion_funnel_analysis"]}] | [] | [] |
| B3 | [{"alias": "customer360__customer_value_analysis", "kind": "base", "block": null, "base_tables": ["customer360__customer_value_analysis"]}] | [] | [] |
| B4 | [{"alias": "customer360__customer_activity_metrics", "kind": "base", "block": null, "base_tables": ["customer360__customer_activity_metrics"]}] | [] | [] |
| B5 | [{"alias": "a", "kind": "derived", "block": "B1", "base_tables": ["customer360__customer_activity_metrics"]}, {"alias": "f", "kind": "derived", "block": "B2", "base_tables": ["customer360__conversion_funnel_analysis"]}, {"alias": "v", "kind": "derived", "block": "B3", "base_tables": ["customer360__customer_value_analysis"]}] | [{"type": "INNER", "right": "latest_funnel AS f", "on": "a.primary_email = f.primary_email AND f.rn = 1", "using": []}, {"type": "INNER", "right": "latest_value AS v", "on": "a.primary_email = v.primary_email AND v.rn = 1", "using": []}] | [] |
| B6 | [{"alias": "cohort", "kind": "derived", "block": "B5", "base_tables": ["customer360__conversion_funnel_analysis", "customer360__customer_activity_metrics", "customer360__customer_value_analysis"]}] | [] | [] |
| B7 | [{"alias": "cohort", "kind": "derived", "block": "B5", "base_tables": ["customer360__conversion_funnel_analysis", "customer360__customer_activity_metrics", "customer360__customer_value_analysis"]}] | [] | ["zendesk_active"] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B4 | AVG(composite_engagement_score) | [{"table": "customer360__customer_activity_metrics", "column": "composite_engagement_score"}] | [] | False |
| B6 | COUNT(*) | [] | [] | True |
| B7 | COUNT(*) | [] | [] | True |
| B7 | COUNT(*) | [] | [] | True |


未解析列血缘：[{"block": "B5", "column": "composite_engagement_score", "reason": "ambiguous_or_missing_source"}]

## S42

类别 `data`；来源 `query_db`；调用 `00d3bcf009aa4b038f34399aa4ba46bc`；状态 `success`。

```sql
SELECT customer360_id, source_system, address_type, state, country FROM customer360__address LIMIT 10
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-054/attempt-01/sql/S42.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-054/attempt-01/sql/S42.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-054/attempt-01/results/S42.rows.jsonl)；完整：True；SHA256：`03ba499373858da370858d84bc0742d50552dbc91197eead6c5c97d8d3a9c03c`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "customer360__address", "kind": "base", "block": null, "base_tables": ["customer360__address"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |


## S43

类别 `data`；来源 `query_db`；调用 `d59952ef68d3446e8b9a0b36b6287966`；状态 `success`。

```sql
SELECT DISTINCT customer360_id FROM customer360__address LIMIT 10
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-054/attempt-01/sql/S43.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-054/attempt-01/sql/S43.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-054/attempt-01/results/S43.rows.jsonl)；完整：True；SHA256：`072c2d2917dfb9821ffe370be7feabbb142b0d16d9f221e85ff713ade625c804`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "customer360__address", "kind": "base", "block": null, "base_tables": ["customer360__address"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |


## S44

类别 `data`；来源 `query_db`；调用 `d995f729e76f4eedb785640059011e0a`；状态 `success`。

```sql
-- Check if customer360_id relates to marketo_lead_id, stripe_customer_id, or zendesk_user_id
-- First, let's see if there's a pattern
SELECT customer360_id, source_system, address_type, priority, rank
FROM customer360__address
WHERE customer360_id = '7eed12549eff566d1179fc92b723bc9c'
ORDER BY source_system, address_type
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-054/attempt-01/sql/S44.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-054/attempt-01/sql/S44.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-054/attempt-01/results/S44.rows.jsonl)；完整：True；SHA256：`935fed0a8943d743f681ae6cc72d1dbbb3eaedd8126dd785d4fafcd2c4cb86b2`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "customer360__address", "kind": "base", "block": null, "base_tables": ["customer360__address"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |


## S45

类别 `data`；来源 `query_db`；调用 `12dd0ea078e74100a951cc17833072a0`；状态 `success`。

```sql
SELECT COUNT(DISTINCT customer360_id) AS distinct_ids FROM customer360__address
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-054/attempt-01/sql/S45.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-054/attempt-01/sql/S45.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-054/attempt-01/results/S45.rows.jsonl)；完整：True；SHA256：`e7831aff6a45426215ada41bc17c93aaef3c291633484a5e63213336a5f25553`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "customer360__address", "kind": "base", "block": null, "base_tables": ["customer360__address"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(DISTINCT customer360_id) | [{"table": "customer360__address", "column": "customer360_id"}] | [] | False |


## S46

类别 `data`；来源 `query_db`；调用 `f44bcaa504f04c8082904fd29e8801ae`；状态 `success`。

```sql
-- Check if there's a Stripe customer ID that looks like a hash
SELECT stripe_customer_id FROM customer360__customer_activity_metrics LIMIT 10
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-054/attempt-01/sql/S46.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-054/attempt-01/sql/S46.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-054/attempt-01/results/S46.rows.jsonl)；完整：True；SHA256：`c33f01f821e30ce3dc6a588e58f93e1c262633e4f6e2794fc03c418a2d4530b4`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "customer360__customer_activity_metrics", "kind": "base", "block": null, "base_tables": ["customer360__customer_activity_metrics"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |


## S47

类别 `data`；来源 `query_db`；调用 `9f5f804177ad4c46917c90701c444a22`；状态 `failed`。

```sql
-- Check if customer360_id might be a hash of email
SELECT primary_email, MD5(primary_email) FROM customer360__customer_activity_metrics LIMIT 5
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-054/attempt-01/sql/S47.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-054/attempt-01/sql/S47.parameters.json)。

错误：`OperationalError('no such function: MD5')`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "customer360__customer_activity_metrics", "kind": "base", "block": null, "base_tables": ["customer360__customer_activity_metrics"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |


## S48

类别 `data`；来源 `query_db`；调用 `a454ecb8999e42578281e12a5bef423d`；状态 `success`。

```sql
SELECT DISTINCT source_system, address_type FROM customer360__address ORDER BY source_system, address_type
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-054/attempt-01/sql/S48.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-054/attempt-01/sql/S48.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-054/attempt-01/results/S48.rows.jsonl)；完整：True；SHA256：`d22bcd77198b0c3349b6a544a8ae7aeaaf5b0d57a0fc606f44d62297519a0c7e`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "customer360__address", "kind": "base", "block": null, "base_tables": ["customer360__address"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |


## S49

类别 `data`；来源 `query_db`；调用 `c50514ac734d4dc8bba2028262c86017`；状态 `success`。

```sql
-- Check if customer360_id might be related to primary_email or marketo_lead_id
-- Let's see all unique source_systems and their counts
SELECT source_system, COUNT(DISTINCT customer360_id) AS cnt
FROM customer360__address
GROUP BY source_system
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-054/attempt-01/sql/S49.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-054/attempt-01/sql/S49.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-054/attempt-01/results/S49.rows.jsonl)；完整：True；SHA256：`db772b24e936c80ba1f59ff6fddb311cb46bcaa957ef5828f6015d7c3a50bc80`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "customer360__address", "kind": "base", "block": null, "base_tables": ["customer360__address"]}] | [] | ["source_system"] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(DISTINCT customer360_id) | [{"table": "customer360__address", "column": "customer360_id"}] | [] | False |


## S50

类别 `data`；来源 `python`；调用 `42b5c3ddcc944568a8bd586a3ebaa603`；状态 `success`。

```sql

  WITH la AS (
    SELECT *, ROW_NUMBER() OVER (PARTITION BY primary_email ORDER BY activity_analysis_timestamp DESC) rn
    FROM customer360__customer_activity_metrics
  )
  SELECT primary_email, marketo_lead_id, stripe_customer_id, zendesk_user_id
  FROM la WHERE rn=1 LIMIT 20

```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-054/attempt-01/sql/S50.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-054/attempt-01/sql/S50.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-054/attempt-01/results/S50.rows.jsonl)；完整：True；SHA256：`cbb46c85ca19a456488276c2abb1c1512221d8280373e6cc92c71757f355f3e3`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "customer360__customer_activity_metrics", "kind": "base", "block": null, "base_tables": ["customer360__customer_activity_metrics"]}] | [] | [] |
| B2 | [{"alias": "la", "kind": "derived", "block": "B1", "base_tables": ["customer360__customer_activity_metrics"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |


## S51

类别 `data`；来源 `python`；调用 `42b5c3ddcc944568a8bd586a3ebaa603`；状态 `success`。

```sql
SELECT DISTINCT customer360_id, source_system FROM customer360__address LIMIT 20
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-054/attempt-01/sql/S51.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-054/attempt-01/sql/S51.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-054/attempt-01/results/S51.rows.jsonl)；完整：True；SHA256：`ade7bebf57771068fda5e8f0c69828fce42c76f4a9ff41beab15a9b965aa5cc2`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "customer360__address", "kind": "base", "block": null, "base_tables": ["customer360__address"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |


## S52

类别 `data`；来源 `python`；调用 `d0bc5ca2bfc749e69c68748ac2a31e4b`；状态 `success`。

```sql

  WITH la AS (
    SELECT *, ROW_NUMBER() OVER (PARTITION BY primary_email ORDER BY activity_analysis_timestamp DESC) rn
    FROM customer360__customer_activity_metrics
  )
  SELECT primary_email, marketo_lead_id, stripe_customer_id, zendesk_user_id
  FROM la WHERE rn=1 LIMIT 50

```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-054/attempt-01/sql/S52.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-054/attempt-01/sql/S52.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-054/attempt-01/results/S52.rows.jsonl)；完整：True；SHA256：`6e79664684124ef79cb365a6bcd7ce9084e5de0af2f717db19a980ed352d8f79`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "customer360__customer_activity_metrics", "kind": "base", "block": null, "base_tables": ["customer360__customer_activity_metrics"]}] | [] | [] |
| B2 | [{"alias": "la", "kind": "derived", "block": "B1", "base_tables": ["customer360__customer_activity_metrics"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |


## S53

类别 `data`；来源 `python`；调用 `d0bc5ca2bfc749e69c68748ac2a31e4b`；状态 `success`。

```sql
SELECT DISTINCT customer360_id, source_system FROM customer360__address LIMIT 200
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-054/attempt-01/sql/S53.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-054/attempt-01/sql/S53.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-054/attempt-01/results/S53.rows.jsonl)；完整：True；SHA256：`9083a764a0e0edbefdfeccf87ec030a45af9b29a5b98d07d3d46978121a5dd96`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "customer360__address", "kind": "base", "block": null, "base_tables": ["customer360__address"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |


## S54

类别 `metadata`；来源 `query_db`；调用 `dbe90bf0d4a143b78f733c1b1fec6ea2`；状态 `success`。

```sql
PRAGMA table_info(customer360__address)
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-054/attempt-01/sql/S54.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-054/attempt-01/sql/S54.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-054/attempt-01/results/S54.rows.jsonl)；完整：True；SHA256：`67a91187cf01b8206f28b5b119cb4882ec358466cba14a4c6345371011c22137`。

## S55

类别 `data`；来源 `python`；调用 `9732161d0e214858acc3a1d2ff2c5cc3`；状态 `success`。

```sql
SELECT DISTINCT customer360_id FROM customer360__address
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-054/attempt-01/sql/S55.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-054/attempt-01/sql/S55.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-054/attempt-01/results/S55.rows.jsonl)；完整：True；SHA256：`8da075634b563ba25c2fb0bee52cd9f702365aa02a91d1cdb0844fa7013158a8`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "customer360__address", "kind": "base", "block": null, "base_tables": ["customer360__address"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |


## S56

类别 `data`；来源 `python`；调用 `9732161d0e214858acc3a1d2ff2c5cc3`；状态 `success`。

```sql

  WITH la AS (
    SELECT *, ROW_NUMBER() OVER (PARTITION BY primary_email ORDER BY activity_analysis_timestamp DESC) rn
    FROM customer360__customer_activity_metrics
  )
  SELECT primary_email, marketo_lead_id, stripe_customer_id, zendesk_user_id, primary_organization
  FROM la WHERE rn=1

```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-054/attempt-01/sql/S56.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-054/attempt-01/sql/S56.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-054/attempt-01/results/S56.rows.jsonl)；完整：True；SHA256：`5e0b89d860510dbe430586372325fcb84136e66b70ab8f36d73a5551ac43061f`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "customer360__customer_activity_metrics", "kind": "base", "block": null, "base_tables": ["customer360__customer_activity_metrics"]}] | [] | [] |
| B2 | [{"alias": "la", "kind": "derived", "block": "B1", "base_tables": ["customer360__customer_activity_metrics"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |


## S57

类别 `data`；来源 `python`；调用 `c19784a3972249a6b95db21abdc82c32`；状态 `success`。

```sql

  WITH la AS (
    SELECT *, ROW_NUMBER() OVER (PARTITION BY primary_email ORDER BY activity_analysis_timestamp DESC) rn
    FROM customer360__customer_activity_metrics
  )
  SELECT primary_email, marketo_lead_id, stripe_customer_id, zendesk_user_id, primary_organization
  FROM la WHERE rn=1

```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-054/attempt-01/sql/S57.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-054/attempt-01/sql/S57.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-054/attempt-01/results/S57.rows.jsonl)；完整：True；SHA256：`5e0b89d860510dbe430586372325fcb84136e66b70ab8f36d73a5551ac43061f`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "customer360__customer_activity_metrics", "kind": "base", "block": null, "base_tables": ["customer360__customer_activity_metrics"]}] | [] | [] |
| B2 | [{"alias": "la", "kind": "derived", "block": "B1", "base_tables": ["customer360__customer_activity_metrics"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |


## S58

类别 `data`；来源 `python`；调用 `c19784a3972249a6b95db21abdc82c32`；状态 `success`。

```sql
SELECT DISTINCT customer360_id, source_system FROM customer360__address
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-054/attempt-01/sql/S58.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-054/attempt-01/sql/S58.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-054/attempt-01/results/S58.rows.jsonl)；完整：True；SHA256：`3db100c9e386e0b3415aa14141d7c3810016a4a868016aa3cda5bebbb858a00b`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "customer360__address", "kind": "base", "block": null, "base_tables": ["customer360__address"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |


## S59

类别 `data`；来源 `python`；调用 `6490722a685d4bbe9f024102f00045b5`；状态 `success`。

```sql
SELECT DISTINCT customer360_id, source_system FROM customer360__address
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-054/attempt-01/sql/S59.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-054/attempt-01/sql/S59.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-054/attempt-01/results/S59.rows.jsonl)；完整：True；SHA256：`3db100c9e386e0b3415aa14141d7c3810016a4a868016aa3cda5bebbb858a00b`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "customer360__address", "kind": "base", "block": null, "base_tables": ["customer360__address"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |


## S60

类别 `data`；来源 `python`；调用 `6490722a685d4bbe9f024102f00045b5`；状态 `success`。

```sql

  WITH la AS (
    SELECT *, ROW_NUMBER() OVER (PARTITION BY primary_email ORDER BY activity_analysis_timestamp DESC) rn
    FROM customer360__customer_activity_metrics
  )
  SELECT primary_email, marketo_lead_id, stripe_customer_id, zendesk_user_id, primary_organization
  FROM la WHERE rn=1

```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-054/attempt-01/sql/S60.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-054/attempt-01/sql/S60.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-054/attempt-01/results/S60.rows.jsonl)；完整：True；SHA256：`5e0b89d860510dbe430586372325fcb84136e66b70ab8f36d73a5551ac43061f`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "customer360__customer_activity_metrics", "kind": "base", "block": null, "base_tables": ["customer360__customer_activity_metrics"]}] | [] | [] |
| B2 | [{"alias": "la", "kind": "derived", "block": "B1", "base_tables": ["customer360__customer_activity_metrics"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |


## S61

类别 `data`；来源 `python`；调用 `2ea91f37d0db46b4a0e03ed771193c7c`；状态 `success`。

```sql

  WITH la AS (
    SELECT *, ROW_NUMBER() OVER (PARTITION BY primary_email ORDER BY activity_analysis_timestamp DESC) rn
    FROM customer360__customer_activity_metrics
  )
  SELECT * FROM la WHERE rn=1 LIMIT 3

```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-054/attempt-01/sql/S61.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-054/attempt-01/sql/S61.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-054/attempt-01/results/S61.rows.jsonl)；完整：True；SHA256：`6f42e4e1f9a81197b37db7e0f10a747aba817e8a326edbb37f84ce55773ea22d`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "customer360__customer_activity_metrics", "kind": "base", "block": null, "base_tables": ["customer360__customer_activity_metrics"]}] | [] | [] |
| B2 | [{"alias": "la", "kind": "derived", "block": "B1", "base_tables": ["customer360__customer_activity_metrics"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |


## S62

类别 `data`；来源 `python`；调用 `2ea91f37d0db46b4a0e03ed771193c7c`；状态 `success`。

```sql
SELECT * FROM customer360__customer_activity_metrics LIMIT 1
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-054/attempt-01/sql/S62.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-054/attempt-01/sql/S62.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-054/attempt-01/results/S62.rows.jsonl)；完整：True；SHA256：`4a64ec5c68ea52f477d4d8dc4ffc0db5573e5e4410a9eb722ad4e191f1e3ce14`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "customer360__customer_activity_metrics", "kind": "base", "block": null, "base_tables": ["customer360__customer_activity_metrics"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |


## S63

类别 `data`；来源 `python`；调用 `2ea91f37d0db46b4a0e03ed771193c7c`；状态 `success`。

```sql
SELECT * FROM customer360__customer_activity_metrics LIMIT 1
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-054/attempt-01/sql/S63.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-054/attempt-01/sql/S63.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-054/attempt-01/results/S63.rows.jsonl)；完整：True；SHA256：`4a64ec5c68ea52f477d4d8dc4ffc0db5573e5e4410a9eb722ad4e191f1e3ce14`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "customer360__customer_activity_metrics", "kind": "base", "block": null, "base_tables": ["customer360__customer_activity_metrics"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |


## S64

类别 `data`；来源 `python`；调用 `2ea91f37d0db46b4a0e03ed771193c7c`；状态 `success`。

```sql
SELECT * FROM customer360__customer_activity_metrics LIMIT 1000
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-054/attempt-01/sql/S64.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-054/attempt-01/sql/S64.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-054/attempt-01/results/S64.rows.jsonl)；完整：True；SHA256：`cd52468ce6c2cde66dd44e4efd77a465c2af04eb97f92422d241b2ad2f98136e`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "customer360__customer_activity_metrics", "kind": "base", "block": null, "base_tables": ["customer360__customer_activity_metrics"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |


## S65

类别 `data`；来源 `python`；调用 `b9b88dab7fe24f36aaf6a7f32a2affaa`；状态 `success`。

```sql
SELECT * FROM customer360__customer_activity_metrics LIMIT 1
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-054/attempt-01/sql/S65.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-054/attempt-01/sql/S65.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-054/attempt-01/results/S65.rows.jsonl)；完整：True；SHA256：`4a64ec5c68ea52f477d4d8dc4ffc0db5573e5e4410a9eb722ad4e191f1e3ce14`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "customer360__customer_activity_metrics", "kind": "base", "block": null, "base_tables": ["customer360__customer_activity_metrics"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |


## S66

类别 `data`；来源 `python`；调用 `b9b88dab7fe24f36aaf6a7f32a2affaa`；状态 `success`。

```sql
SELECT * FROM customer360__customer_activity_metrics LIMIT 2000
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-054/attempt-01/sql/S66.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-054/attempt-01/sql/S66.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-054/attempt-01/results/S66.rows.jsonl)；完整：True；SHA256：`f74ddd670eac0e3c05822a3474d4c5c5180918cdd5a12944d0bc5d5f01ceef57`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "customer360__customer_activity_metrics", "kind": "base", "block": null, "base_tables": ["customer360__customer_activity_metrics"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |


## S67

类别 `data`；来源 `python`；调用 `b9b88dab7fe24f36aaf6a7f32a2affaa`；状态 `success`。

```sql
SELECT * FROM customer360__conversion_funnel_analysis LIMIT 1
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-054/attempt-01/sql/S67.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-054/attempt-01/sql/S67.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-054/attempt-01/results/S67.rows.jsonl)；完整：True；SHA256：`27b8596606b8c7940432c6b36d22c58d1f694fb59ccb6c65e44294381b0b9a61`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "customer360__conversion_funnel_analysis", "kind": "base", "block": null, "base_tables": ["customer360__conversion_funnel_analysis"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |


## S68

类别 `data`；来源 `python`；调用 `b9b88dab7fe24f36aaf6a7f32a2affaa`；状态 `success`。

```sql
SELECT * FROM customer360__conversion_funnel_analysis LIMIT 2000
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-054/attempt-01/sql/S68.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-054/attempt-01/sql/S68.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-054/attempt-01/results/S68.rows.jsonl)；完整：True；SHA256：`50da613d4d5077293507d1363d02fca36301fe36b202698e131defe9adbe1979`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "customer360__conversion_funnel_analysis", "kind": "base", "block": null, "base_tables": ["customer360__conversion_funnel_analysis"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |


## S69

类别 `data`；来源 `python`；调用 `b9b88dab7fe24f36aaf6a7f32a2affaa`；状态 `success`。

```sql
SELECT * FROM customer360__customer_value_analysis LIMIT 1
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-054/attempt-01/sql/S69.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-054/attempt-01/sql/S69.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-054/attempt-01/results/S69.rows.jsonl)；完整：True；SHA256：`bdb0c360d1f269d6265cdb7981fe0be6cb7995670f478e71926835e754580afe`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "customer360__customer_value_analysis", "kind": "base", "block": null, "base_tables": ["customer360__customer_value_analysis"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |


## S70

类别 `data`；来源 `python`；调用 `b9b88dab7fe24f36aaf6a7f32a2affaa`；状态 `success`。

```sql
SELECT * FROM customer360__customer_value_analysis LIMIT 2000
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-054/attempt-01/sql/S70.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-054/attempt-01/sql/S70.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-054/attempt-01/results/S70.rows.jsonl)；完整：True；SHA256：`2938ebcba37fcc50d308474d65dbf01b295e5b059a0ffe22fc3704a163c68f5b`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "customer360__customer_value_analysis", "kind": "base", "block": null, "base_tables": ["customer360__customer_value_analysis"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |


## S71

类别 `data`；来源 `python`；调用 `2fa7535386774c5f96ead055eb8b5692`；状态 `success`。

```sql
SELECT DISTINCT customer360_id FROM customer360__address
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-054/attempt-01/sql/S71.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-054/attempt-01/sql/S71.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-054/attempt-01/results/S71.rows.jsonl)；完整：True；SHA256：`8da075634b563ba25c2fb0bee52cd9f702365aa02a91d1cdb0844fa7013158a8`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "customer360__address", "kind": "base", "block": null, "base_tables": ["customer360__address"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |


## S72

类别 `data`；来源 `python`；调用 `2fa7535386774c5f96ead055eb8b5692`；状态 `success`。

```sql

  WITH la AS (
    SELECT *, ROW_NUMBER() OVER (PARTITION BY primary_email ORDER BY activity_analysis_timestamp DESC) rn
    FROM customer360__customer_activity_metrics
  )
  SELECT primary_email FROM la WHERE rn=1

```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-054/attempt-01/sql/S72.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-054/attempt-01/sql/S72.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-054/attempt-01/results/S72.rows.jsonl)；完整：True；SHA256：`9b89fbc58b0d683d9cf5f790a8015b051b504f38d4cb3ba1ebcf4742f59b5923`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "customer360__customer_activity_metrics", "kind": "base", "block": null, "base_tables": ["customer360__customer_activity_metrics"]}] | [] | [] |
| B2 | [{"alias": "la", "kind": "derived", "block": "B1", "base_tables": ["customer360__customer_activity_metrics"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |


## S73

类别 `data`；来源 `python`；调用 `d222586cc7ee491c998c4d323856434e`；状态 `success`。

```sql
SELECT DISTINCT customer360_id, source_system FROM customer360__address
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-054/attempt-01/sql/S73.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-054/attempt-01/sql/S73.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-054/attempt-01/results/S73.rows.jsonl)；完整：True；SHA256：`3db100c9e386e0b3415aa14141d7c3810016a4a868016aa3cda5bebbb858a00b`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "customer360__address", "kind": "base", "block": null, "base_tables": ["customer360__address"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |


## S74

类别 `data`；来源 `python`；调用 `d222586cc7ee491c998c4d323856434e`；状态 `success`。

```sql

  WITH la AS (
    SELECT *, ROW_NUMBER() OVER (PARTITION BY primary_email ORDER BY activity_analysis_timestamp DESC) rn
    FROM customer360__customer_activity_metrics
  )
  SELECT primary_email, marketo_lead_id, stripe_customer_id, zendesk_user_id FROM la WHERE rn=1

```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-054/attempt-01/sql/S74.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-054/attempt-01/sql/S74.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-054/attempt-01/results/S74.rows.jsonl)；完整：True；SHA256：`8e0c437ca2de36cd8f8a048dca6d00f33756299fe2464ebf65bf23cc523b5226`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "customer360__customer_activity_metrics", "kind": "base", "block": null, "base_tables": ["customer360__customer_activity_metrics"]}] | [] | [] |
| B2 | [{"alias": "la", "kind": "derived", "block": "B1", "base_tables": ["customer360__customer_activity_metrics"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |


## S75

类别 `data`；来源 `python`；调用 `d222586cc7ee491c998c4d323856434e`；状态 `success`。

```sql

  SELECT customer360_id, COUNT(*) cnt FROM customer360__address 
  WHERE source_system='marketo' GROUP BY customer360_id ORDER BY cnt DESC LIMIT 10

```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-054/attempt-01/sql/S75.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-054/attempt-01/sql/S75.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-054/attempt-01/results/S75.rows.jsonl)；完整：True；SHA256：`e7f0375950ada5dd65d79439b6e9455d9e6a467405f93beb0c6a4cb6832e65da`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "customer360__address", "kind": "base", "block": null, "base_tables": ["customer360__address"]}] | [] | ["customer360_id"] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |


## S76

类别 `data`；来源 `python`；调用 `2cbe65f21f4247e3bf984519dc3578f6`；状态 `success`。

```sql
SELECT DISTINCT customer360_id FROM customer360__address
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-054/attempt-01/sql/S76.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-054/attempt-01/sql/S76.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-054/attempt-01/results/S76.rows.jsonl)；完整：True；SHA256：`8da075634b563ba25c2fb0bee52cd9f702365aa02a91d1cdb0844fa7013158a8`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "customer360__address", "kind": "base", "block": null, "base_tables": ["customer360__address"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |


## S77

类别 `data`；来源 `python`；调用 `2cbe65f21f4247e3bf984519dc3578f6`；状态 `success`。

```sql

  WITH la AS (
    SELECT *, ROW_NUMBER() OVER (PARTITION BY primary_email ORDER BY activity_analysis_timestamp DESC) rn
    FROM customer360__customer_activity_metrics
  )
  SELECT primary_email, primary_organization, marketo_lead_id, stripe_customer_id, zendesk_user_id
  FROM la WHERE rn=1

```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-054/attempt-01/sql/S77.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-054/attempt-01/sql/S77.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-054/attempt-01/results/S77.rows.jsonl)；完整：True；SHA256：`014e6a7511be547047e1514042f337bd2619ab50d93eeb46e55c14a78939daa1`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "customer360__customer_activity_metrics", "kind": "base", "block": null, "base_tables": ["customer360__customer_activity_metrics"]}] | [] | [] |
| B2 | [{"alias": "la", "kind": "derived", "block": "B1", "base_tables": ["customer360__customer_activity_metrics"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |


## S78

类别 `data`；来源 `python`；调用 `2cbe65f21f4247e3bf984519dc3578f6`；状态 `success`。

```sql
SELECT COUNT(DISTINCT marketo_lead_id || '-' || stripe_customer_id || '-' || zendesk_user_id) FROM customer360__conversion_funnel_analysis
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-054/attempt-01/sql/S78.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-054/attempt-01/sql/S78.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-054/attempt-01/results/S78.rows.jsonl)；完整：True；SHA256：`c1fd73d932ff759f5e941c045c4c6d772d20494a1140706678dfb979a0679557`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "customer360__conversion_funnel_analysis", "kind": "base", "block": null, "base_tables": ["customer360__conversion_funnel_analysis"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(DISTINCT marketo_lead_id \|\| '-' \|\| stripe_customer_id \|\| '-' \|\| zendesk_user_id) | [{"table": "customer360__conversion_funnel_analysis", "column": "zendesk_user_id"}, {"table": "customer360__conversion_funnel_analysis", "column": "stripe_customer_id"}, {"table": "customer360__conversion_funnel_analysis", "column": "marketo_lead_id"}] | [] | False |


## S79

类别 `data`；来源 `python`；调用 `2cbe65f21f4247e3bf984519dc3578f6`；状态 `success`。

```sql
SELECT COUNT(DISTINCT marketo_lead_id || '-' || funnel_analysis_timestamp) FROM customer360__conversion_funnel_analysis
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-054/attempt-01/sql/S79.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-054/attempt-01/sql/S79.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-054/attempt-01/results/S79.rows.jsonl)；完整：True；SHA256：`29433440de3cbf6d261739003c6943be8c3f2086c8c7ba6f73f02e13236537d2`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "customer360__conversion_funnel_analysis", "kind": "base", "block": null, "base_tables": ["customer360__conversion_funnel_analysis"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(DISTINCT marketo_lead_id \|\| '-' \|\| funnel_analysis_timestamp) | [{"table": "customer360__conversion_funnel_analysis", "column": "funnel_analysis_timestamp"}, {"table": "customer360__conversion_funnel_analysis", "column": "marketo_lead_id"}] | [] | False |


## S80

类别 `data`；来源 `python`；调用 `2cbe65f21f4247e3bf984519dc3578f6`；状态 `success`。

```sql
SELECT DISTINCT country FROM customer360__address ORDER BY country LIMIT 20
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-054/attempt-01/sql/S80.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-054/attempt-01/sql/S80.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-054/attempt-01/results/S80.rows.jsonl)；完整：True；SHA256：`1d04a3819b5d51cc60c4f00435acb8331d55a7529c2d5adca00122d917ba70ef`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "customer360__address", "kind": "base", "block": null, "base_tables": ["customer360__address"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |


## S81

类别 `data`；来源 `python`；调用 `2cbe65f21f4247e3bf984519dc3578f6`；状态 `success`。

```sql
SELECT COUNT(DISTINCT country) FROM customer360__address
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-054/attempt-01/sql/S81.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-054/attempt-01/sql/S81.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-054/attempt-01/results/S81.rows.jsonl)；完整：True；SHA256：`df900a8b3167592dc3bc440ced670b6674b5026c57d0ec54f10479b3d5898bdc`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "customer360__address", "kind": "base", "block": null, "base_tables": ["customer360__address"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(DISTINCT country) | [{"table": "customer360__address", "column": "country"}] | [] | False |


## S82

类别 `data`；来源 `query_db`；调用 `4ffdcce673844cbea5407e492faefa9c`；状态 `success`。

```sql
-- Multi-platform engagement patterns impact on customer_health_score
WITH latest_activity AS (
  SELECT *, ROW_NUMBER() OVER (PARTITION BY primary_email ORDER BY activity_analysis_timestamp DESC) AS rn
  FROM customer360__customer_activity_metrics
),
latest_funnel AS (
  SELECT *, ROW_NUMBER() OVER (PARTITION BY primary_email ORDER BY funnel_analysis_timestamp DESC) AS rn
  FROM customer360__conversion_funnel_analysis
),
latest_value AS (
  SELECT *, ROW_NUMBER() OVER (PARTITION BY primary_email ORDER BY analysis_timestamp DESC) AS rn
  FROM customer360__customer_value_analysis
),
cohort AS (
  SELECT a.primary_email, a.composite_engagement_score, 
         f.marketing_to_sales_days, f.sales_to_support_days,
         f.customer_tier, f.estimated_customer_ltv AS funnel_ltv,
         a.primary_engagement_channel, a.zendesk_active,
         a.in_marketo, a.in_stripe, a.in_zendesk,
         a.customer_health_score, a.activity_risk_level, a.engagement_velocity
  FROM latest_activity a
  JOIN latest_funnel f ON a.primary_email = f.primary_email AND f.rn = 1
  JOIN latest_value v ON a.primary_email = v.primary_email AND v.rn = 1
  WHERE a.rn = 1
    AND f.marketing_to_sales_days BETWEEN 10 AND 20
    AND f.sales_to_support_days > 30
    AND a.composite_engagement_score > (SELECT AVG(composite_engagement_score) FROM customer360__customer_activity_metrics)
)
SELECT 
  CASE 
    WHEN in_marketo = 1 AND in_stripe = 1 AND in_zendesk = 1 THEN 'All 3 Platforms'
    WHEN in_marketo = 1 AND in_stripe = 1 AND in_zendesk = 0 THEN 'Marketo + Stripe'
    WHEN in_marketo = 1 AND in_stripe = 0 AND in_zendesk = 1 THEN 'Marketo + Zendesk'
    WHEN in_marketo = 0 AND in_stripe = 1 AND in_zendesk = 1 THEN 'Stripe + Zendesk'
    WHEN in_marketo = 1 AND in_stripe = 0 AND in_zendesk = 0 THEN 'Marketo Only'
    WHEN in_marketo = 0 AND in_stripe = 1 AND in_zendesk = 0 THEN 'Stripe Only'
    WHEN in_marketo = 0 AND in_stripe = 0 AND in_zendesk = 1 THEN 'Zendesk Only'
    ELSE 'None'
  END AS platform_pattern,
  COUNT(*) AS cnt,
  ROUND(100.0 * COUNT(*) / (SELECT COUNT(*) FROM cohort), 2) AS pct,
  ROUND(AVG(customer_health_score), 2) AS avg_health_score,
  ROUND(AVG(composite_engagement_score), 2) AS avg_engagement_score,
  ROUND(AVG(funnel_ltv), 2) AS avg_ltv
FROM cohort
GROUP BY platform_pattern
ORDER BY cnt DESC
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-054/attempt-01/sql/S82.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-054/attempt-01/sql/S82.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-054/attempt-01/results/S82.rows.jsonl)；完整：True；SHA256：`fdd6e7748bd10ae8174d92c38591a3533c913800457c92f9cdb5e412bb411ddf`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "customer360__customer_activity_metrics", "kind": "base", "block": null, "base_tables": ["customer360__customer_activity_metrics"]}] | [] | [] |
| B2 | [{"alias": "customer360__conversion_funnel_analysis", "kind": "base", "block": null, "base_tables": ["customer360__conversion_funnel_analysis"]}] | [] | [] |
| B3 | [{"alias": "customer360__customer_value_analysis", "kind": "base", "block": null, "base_tables": ["customer360__customer_value_analysis"]}] | [] | [] |
| B4 | [{"alias": "customer360__customer_activity_metrics", "kind": "base", "block": null, "base_tables": ["customer360__customer_activity_metrics"]}] | [] | [] |
| B5 | [{"alias": "a", "kind": "derived", "block": "B1", "base_tables": ["customer360__customer_activity_metrics"]}, {"alias": "f", "kind": "derived", "block": "B2", "base_tables": ["customer360__conversion_funnel_analysis"]}, {"alias": "v", "kind": "derived", "block": "B3", "base_tables": ["customer360__customer_value_analysis"]}] | [{"type": "INNER", "right": "latest_funnel AS f", "on": "a.primary_email = f.primary_email AND f.rn = 1", "using": []}, {"type": "INNER", "right": "latest_value AS v", "on": "a.primary_email = v.primary_email AND v.rn = 1", "using": []}] | [] |
| B6 | [{"alias": "cohort", "kind": "derived", "block": "B5", "base_tables": ["customer360__conversion_funnel_analysis", "customer360__customer_activity_metrics", "customer360__customer_value_analysis"]}] | [] | [] |
| B7 | [{"alias": "cohort", "kind": "derived", "block": "B5", "base_tables": ["customer360__conversion_funnel_analysis", "customer360__customer_activity_metrics", "customer360__customer_value_analysis"]}] | [] | ["CASE WHEN in_marketo = 1 AND in_stripe = 1 AND in_zendesk = 1 THEN 'All 3 Platforms' WHEN in_marketo = 1 AND in_stripe = 1 AND in_zendesk = 0 THEN 'Marketo + Stripe' WHEN in_marketo = 1 AND in_stripe = 0 AND in_zendesk = 1 THEN 'Marketo + Zendesk' WHEN in_marketo = 0 AND in_stripe = 1 AND in_zendesk = 1 THEN 'Stripe + Zendesk' WHEN in_marketo = 1 AND in_stripe = 0 AND in_zendesk = 0 THEN 'Marketo Only' WHEN in_marketo = 0 AND in_stripe = 1 AND in_zendesk = 0 THEN 'Stripe Only' WHEN in_marketo = 0 AND in_stripe = 0 AND in_zendesk = 1 THEN 'Zendesk Only' ELSE 'None' END"] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B4 | AVG(composite_engagement_score) | [{"table": "customer360__customer_activity_metrics", "column": "composite_engagement_score"}] | [] | False |
| B6 | COUNT(*) | [] | [] | True |
| B7 | COUNT(*) | [] | [] | True |
| B7 | AVG(customer_health_score) | [{"table": "customer360__customer_activity_metrics", "column": "customer_health_score"}] | [] | False |
| B7 | AVG(composite_engagement_score) | [{"table": "customer360__customer_activity_metrics", "column": "composite_engagement_score"}] | [] | False |
| B7 | AVG(funnel_ltv) | [{"table": "customer360__conversion_funnel_analysis", "column": "estimated_customer_ltv"}] | [] | False |
| B7 | COUNT(*) | [] | [] | True |


未解析列血缘：[{"block": "B5", "column": "composite_engagement_score", "reason": "ambiguous_or_missing_source"}]

## S83

类别 `data`；来源 `query_db`；调用 `dd9ceed3151e43f2a78432ec7d6f9ba2`；状态 `success`。

```sql
-- Risk level and engagement velocity distribution for cohort
WITH latest_activity AS (
  SELECT *, ROW_NUMBER() OVER (PARTITION BY primary_email ORDER BY activity_analysis_timestamp DESC) AS rn
  FROM customer360__customer_activity_metrics
),
latest_funnel AS (
  SELECT *, ROW_NUMBER() OVER (PARTITION BY primary_email ORDER BY funnel_analysis_timestamp DESC) AS rn
  FROM customer360__conversion_funnel_analysis
),
latest_value AS (
  SELECT *, ROW_NUMBER() OVER (PARTITION BY primary_email ORDER BY analysis_timestamp DESC) AS rn
  FROM customer360__customer_value_analysis
),
cohort AS (
  SELECT a.primary_email, a.composite_engagement_score, 
         f.marketing_to_sales_days, f.sales_to_support_days,
         f.customer_tier, f.estimated_customer_ltv AS funnel_ltv,
         a.primary_engagement_channel, a.zendesk_active,
         a.in_marketo, a.in_stripe, a.in_zendesk,
         a.customer_health_score, a.activity_risk_level, a.engagement_velocity,
         a.customer_segment, a.lifecycle_stage
  FROM latest_activity a
  JOIN latest_funnel f ON a.primary_email = f.primary_email AND f.rn = 1
  JOIN latest_value v ON a.primary_email = v.primary_email AND v.rn = 1
  WHERE a.rn = 1
    AND f.marketing_to_sales_days BETWEEN 10 AND 20
    AND f.sales_to_support_days > 30
    AND a.composite_engagement_score > (SELECT AVG(composite_engagement_score) FROM customer360__customer_activity_metrics)
)
SELECT activity_risk_level, COUNT(*) AS cnt,
       ROUND(100.0 * COUNT(*) / (SELECT COUNT(*) FROM cohort), 2) AS pct,
       ROUND(AVG(customer_health_score), 2) AS avg_health,
       ROUND(AVG(funnel_ltv), 2) AS avg_ltv
FROM cohort
GROUP BY activity_risk_level
ORDER BY cnt DESC
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-054/attempt-01/sql/S83.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-054/attempt-01/sql/S83.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-054/attempt-01/results/S83.rows.jsonl)；完整：True；SHA256：`c45917525bf913761a5ee560f1a45bf6a136b1d3019aea0f9ce181af87d1b1b7`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "customer360__customer_activity_metrics", "kind": "base", "block": null, "base_tables": ["customer360__customer_activity_metrics"]}] | [] | [] |
| B2 | [{"alias": "customer360__conversion_funnel_analysis", "kind": "base", "block": null, "base_tables": ["customer360__conversion_funnel_analysis"]}] | [] | [] |
| B3 | [{"alias": "customer360__customer_value_analysis", "kind": "base", "block": null, "base_tables": ["customer360__customer_value_analysis"]}] | [] | [] |
| B4 | [{"alias": "customer360__customer_activity_metrics", "kind": "base", "block": null, "base_tables": ["customer360__customer_activity_metrics"]}] | [] | [] |
| B5 | [{"alias": "a", "kind": "derived", "block": "B1", "base_tables": ["customer360__customer_activity_metrics"]}, {"alias": "f", "kind": "derived", "block": "B2", "base_tables": ["customer360__conversion_funnel_analysis"]}, {"alias": "v", "kind": "derived", "block": "B3", "base_tables": ["customer360__customer_value_analysis"]}] | [{"type": "INNER", "right": "latest_funnel AS f", "on": "a.primary_email = f.primary_email AND f.rn = 1", "using": []}, {"type": "INNER", "right": "latest_value AS v", "on": "a.primary_email = v.primary_email AND v.rn = 1", "using": []}] | [] |
| B6 | [{"alias": "cohort", "kind": "derived", "block": "B5", "base_tables": ["customer360__conversion_funnel_analysis", "customer360__customer_activity_metrics", "customer360__customer_value_analysis"]}] | [] | [] |
| B7 | [{"alias": "cohort", "kind": "derived", "block": "B5", "base_tables": ["customer360__conversion_funnel_analysis", "customer360__customer_activity_metrics", "customer360__customer_value_analysis"]}] | [] | ["activity_risk_level"] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B4 | AVG(composite_engagement_score) | [{"table": "customer360__customer_activity_metrics", "column": "composite_engagement_score"}] | [] | False |
| B6 | COUNT(*) | [] | [] | True |
| B7 | COUNT(*) | [] | [] | True |
| B7 | AVG(customer_health_score) | [{"table": "customer360__customer_activity_metrics", "column": "customer_health_score"}] | [] | False |
| B7 | AVG(funnel_ltv) | [{"table": "customer360__conversion_funnel_analysis", "column": "estimated_customer_ltv"}] | [] | False |
| B7 | COUNT(*) | [] | [] | True |


未解析列血缘：[{"block": "B5", "column": "composite_engagement_score", "reason": "ambiguous_or_missing_source"}]

## S84

类别 `data`；来源 `query_db`；调用 `432bfa13980948cf961144807de27b7d`；状态 `success`。

```sql
-- Engagement velocity distribution for cohort
WITH latest_activity AS (
  SELECT *, ROW_NUMBER() OVER (PARTITION BY primary_email ORDER BY activity_analysis_timestamp DESC) AS rn
  FROM customer360__customer_activity_metrics
),
latest_funnel AS (
  SELECT *, ROW_NUMBER() OVER (PARTITION BY primary_email ORDER BY funnel_analysis_timestamp DESC) AS rn
  FROM customer360__conversion_funnel_analysis
),
latest_value AS (
  SELECT *, ROW_NUMBER() OVER (PARTITION BY primary_email ORDER BY analysis_timestamp DESC) AS rn
  FROM customer360__customer_value_analysis
),
cohort AS (
  SELECT a.primary_email, a.composite_engagement_score, 
         f.marketing_to_sales_days, f.sales_to_support_days,
         f.customer_tier, f.estimated_customer_ltv AS funnel_ltv,
         a.primary_engagement_channel, a.zendesk_active,
         a.in_marketo, a.in_stripe, a.in_zendesk,
         a.customer_health_score, a.activity_risk_level, a.engagement_velocity,
         a.customer_segment, a.lifecycle_stage
  FROM latest_activity a
  JOIN latest_funnel f ON a.primary_email = f.primary_email AND f.rn = 1
  JOIN latest_value v ON a.primary_email = v.primary_email AND v.rn = 1
  WHERE a.rn = 1
    AND f.marketing_to_sales_days BETWEEN 10 AND 20
    AND f.sales_to_support_days > 30
    AND a.composite_engagement_score > (SELECT AVG(composite_engagement_score) FROM customer360__customer_activity_metrics)
)
SELECT engagement_velocity, COUNT(*) AS cnt,
       ROUND(100.0 * COUNT(*) / (SELECT COUNT(*) FROM cohort), 2) AS pct,
       ROUND(AVG(customer_health_score), 2) AS avg_health,
       ROUND(AVG(funnel_ltv), 2) AS avg_ltv
FROM cohort
GROUP BY engagement_velocity
ORDER BY cnt DESC
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-054/attempt-01/sql/S84.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-054/attempt-01/sql/S84.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-054/attempt-01/results/S84.rows.jsonl)；完整：True；SHA256：`59d9128941d5bf91fa04ac47e48da3ee1e842e80141c8633d12221641cc0de51`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "customer360__customer_activity_metrics", "kind": "base", "block": null, "base_tables": ["customer360__customer_activity_metrics"]}] | [] | [] |
| B2 | [{"alias": "customer360__conversion_funnel_analysis", "kind": "base", "block": null, "base_tables": ["customer360__conversion_funnel_analysis"]}] | [] | [] |
| B3 | [{"alias": "customer360__customer_value_analysis", "kind": "base", "block": null, "base_tables": ["customer360__customer_value_analysis"]}] | [] | [] |
| B4 | [{"alias": "customer360__customer_activity_metrics", "kind": "base", "block": null, "base_tables": ["customer360__customer_activity_metrics"]}] | [] | [] |
| B5 | [{"alias": "a", "kind": "derived", "block": "B1", "base_tables": ["customer360__customer_activity_metrics"]}, {"alias": "f", "kind": "derived", "block": "B2", "base_tables": ["customer360__conversion_funnel_analysis"]}, {"alias": "v", "kind": "derived", "block": "B3", "base_tables": ["customer360__customer_value_analysis"]}] | [{"type": "INNER", "right": "latest_funnel AS f", "on": "a.primary_email = f.primary_email AND f.rn = 1", "using": []}, {"type": "INNER", "right": "latest_value AS v", "on": "a.primary_email = v.primary_email AND v.rn = 1", "using": []}] | [] |
| B6 | [{"alias": "cohort", "kind": "derived", "block": "B5", "base_tables": ["customer360__conversion_funnel_analysis", "customer360__customer_activity_metrics", "customer360__customer_value_analysis"]}] | [] | [] |
| B7 | [{"alias": "cohort", "kind": "derived", "block": "B5", "base_tables": ["customer360__conversion_funnel_analysis", "customer360__customer_activity_metrics", "customer360__customer_value_analysis"]}] | [] | ["engagement_velocity"] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B4 | AVG(composite_engagement_score) | [{"table": "customer360__customer_activity_metrics", "column": "composite_engagement_score"}] | [] | False |
| B6 | COUNT(*) | [] | [] | True |
| B7 | COUNT(*) | [] | [] | True |
| B7 | AVG(customer_health_score) | [{"table": "customer360__customer_activity_metrics", "column": "customer_health_score"}] | [] | False |
| B7 | AVG(funnel_ltv) | [{"table": "customer360__conversion_funnel_analysis", "column": "estimated_customer_ltv"}] | [] | False |
| B7 | COUNT(*) | [] | [] | True |


未解析列血缘：[{"block": "B5", "column": "composite_engagement_score", "reason": "ambiguous_or_missing_source"}]

## S85

类别 `data`；来源 `query_db`；调用 `6a623bb6303d496995c983c4f3465df9`；状态 `success`。

```sql
-- Cohort by customer_segment and lifecycle_stage
WITH latest_activity AS (
  SELECT *, ROW_NUMBER() OVER (PARTITION BY primary_email ORDER BY activity_analysis_timestamp DESC) AS rn
  FROM customer360__customer_activity_metrics
),
latest_funnel AS (
  SELECT *, ROW_NUMBER() OVER (PARTITION BY primary_email ORDER BY funnel_analysis_timestamp DESC) AS rn
  FROM customer360__conversion_funnel_analysis
),
latest_value AS (
  SELECT *, ROW_NUMBER() OVER (PARTITION BY primary_email ORDER BY analysis_timestamp DESC) AS rn
  FROM customer360__customer_value_analysis
),
cohort AS (
  SELECT a.primary_email, f.customer_tier,
         a.customer_segment, a.lifecycle_stage,
         v.rfm_segment, v.rfm_score,
         a.customer_health_score, f.estimated_customer_ltv AS funnel_ltv
  FROM latest_activity a
  JOIN latest_funnel f ON a.primary_email = f.primary_email AND f.rn = 1
  JOIN latest_value v ON a.primary_email = v.primary_email AND v.rn = 1
  WHERE a.rn = 1
    AND f.marketing_to_sales_days BETWEEN 10 AND 20
    AND f.sales_to_support_days > 30
    AND a.composite_engagement_score > (SELECT AVG(composite_engagement_score) FROM customer360__customer_activity_metrics)
)
SELECT customer_segment, COUNT(*) AS cnt, ROUND(100.0*COUNT(*)/(SELECT COUNT(*) FROM cohort),2) AS pct
FROM cohort GROUP BY customer_segment ORDER BY cnt DESC
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-054/attempt-01/sql/S85.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-054/attempt-01/sql/S85.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-054/attempt-01/results/S85.rows.jsonl)；完整：True；SHA256：`6e6e42ffcfd991c5c2f819b37bdf938401dbd4c445e7d8dc5d0fad98cba3722c`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "customer360__customer_activity_metrics", "kind": "base", "block": null, "base_tables": ["customer360__customer_activity_metrics"]}] | [] | [] |
| B2 | [{"alias": "customer360__conversion_funnel_analysis", "kind": "base", "block": null, "base_tables": ["customer360__conversion_funnel_analysis"]}] | [] | [] |
| B3 | [{"alias": "customer360__customer_value_analysis", "kind": "base", "block": null, "base_tables": ["customer360__customer_value_analysis"]}] | [] | [] |
| B4 | [{"alias": "customer360__customer_activity_metrics", "kind": "base", "block": null, "base_tables": ["customer360__customer_activity_metrics"]}] | [] | [] |
| B5 | [{"alias": "a", "kind": "derived", "block": "B1", "base_tables": ["customer360__customer_activity_metrics"]}, {"alias": "f", "kind": "derived", "block": "B2", "base_tables": ["customer360__conversion_funnel_analysis"]}, {"alias": "v", "kind": "derived", "block": "B3", "base_tables": ["customer360__customer_value_analysis"]}] | [{"type": "INNER", "right": "latest_funnel AS f", "on": "a.primary_email = f.primary_email AND f.rn = 1", "using": []}, {"type": "INNER", "right": "latest_value AS v", "on": "a.primary_email = v.primary_email AND v.rn = 1", "using": []}] | [] |
| B6 | [{"alias": "cohort", "kind": "derived", "block": "B5", "base_tables": ["customer360__conversion_funnel_analysis", "customer360__customer_activity_metrics", "customer360__customer_value_analysis"]}] | [] | [] |
| B7 | [{"alias": "cohort", "kind": "derived", "block": "B5", "base_tables": ["customer360__conversion_funnel_analysis", "customer360__customer_activity_metrics", "customer360__customer_value_analysis"]}] | [] | ["customer_segment"] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B4 | AVG(composite_engagement_score) | [{"table": "customer360__customer_activity_metrics", "column": "composite_engagement_score"}] | [] | False |
| B6 | COUNT(*) | [] | [] | True |
| B7 | COUNT(*) | [] | [] | True |
| B7 | COUNT(*) | [] | [] | True |


未解析列血缘：[{"block": "B5", "column": "composite_engagement_score", "reason": "ambiguous_or_missing_source"}]

## S86

类别 `data`；来源 `query_db`；调用 `92de2d9ba8c34046b068a2585d691c89`；状态 `success`。

```sql
-- Cohort by lifecycle_stage
WITH latest_activity AS (
  SELECT *, ROW_NUMBER() OVER (PARTITION BY primary_email ORDER BY activity_analysis_timestamp DESC) AS rn
  FROM customer360__customer_activity_metrics
),
latest_funnel AS (
  SELECT *, ROW_NUMBER() OVER (PARTITION BY primary_email ORDER BY funnel_analysis_timestamp DESC) AS rn
  FROM customer360__conversion_funnel_analysis
),
latest_value AS (
  SELECT *, ROW_NUMBER() OVER (PARTITION BY primary_email ORDER BY analysis_timestamp DESC) AS rn
  FROM customer360__customer_value_analysis
),
cohort AS (
  SELECT a.primary_email, f.customer_tier,
         a.customer_segment, a.lifecycle_stage,
         v.rfm_segment, v.rfm_score,
         a.customer_health_score, f.estimated_customer_ltv AS funnel_ltv
  FROM latest_activity a
  JOIN latest_funnel f ON a.primary_email = f.primary_email AND f.rn = 1
  JOIN latest_value v ON a.primary_email = v.primary_email AND v.rn = 1
  WHERE a.rn = 1
    AND f.marketing_to_sales_days BETWEEN 10 AND 20
    AND f.sales_to_support_days > 30
    AND a.composite_engagement_score > (SELECT AVG(composite_engagement_score) FROM customer360__customer_activity_metrics)
)
SELECT lifecycle_stage, COUNT(*) AS cnt, ROUND(100.0*COUNT(*)/(SELECT COUNT(*) FROM cohort),2) AS pct
FROM cohort GROUP BY lifecycle_stage ORDER BY cnt DESC
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-054/attempt-01/sql/S86.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-054/attempt-01/sql/S86.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-054/attempt-01/results/S86.rows.jsonl)；完整：True；SHA256：`20bafcfddaa01c1a6d6114e9fb18f8d43bf7b19db4fd60214c5c4c915a487892`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "customer360__customer_activity_metrics", "kind": "base", "block": null, "base_tables": ["customer360__customer_activity_metrics"]}] | [] | [] |
| B2 | [{"alias": "customer360__conversion_funnel_analysis", "kind": "base", "block": null, "base_tables": ["customer360__conversion_funnel_analysis"]}] | [] | [] |
| B3 | [{"alias": "customer360__customer_value_analysis", "kind": "base", "block": null, "base_tables": ["customer360__customer_value_analysis"]}] | [] | [] |
| B4 | [{"alias": "customer360__customer_activity_metrics", "kind": "base", "block": null, "base_tables": ["customer360__customer_activity_metrics"]}] | [] | [] |
| B5 | [{"alias": "a", "kind": "derived", "block": "B1", "base_tables": ["customer360__customer_activity_metrics"]}, {"alias": "f", "kind": "derived", "block": "B2", "base_tables": ["customer360__conversion_funnel_analysis"]}, {"alias": "v", "kind": "derived", "block": "B3", "base_tables": ["customer360__customer_value_analysis"]}] | [{"type": "INNER", "right": "latest_funnel AS f", "on": "a.primary_email = f.primary_email AND f.rn = 1", "using": []}, {"type": "INNER", "right": "latest_value AS v", "on": "a.primary_email = v.primary_email AND v.rn = 1", "using": []}] | [] |
| B6 | [{"alias": "cohort", "kind": "derived", "block": "B5", "base_tables": ["customer360__conversion_funnel_analysis", "customer360__customer_activity_metrics", "customer360__customer_value_analysis"]}] | [] | [] |
| B7 | [{"alias": "cohort", "kind": "derived", "block": "B5", "base_tables": ["customer360__conversion_funnel_analysis", "customer360__customer_activity_metrics", "customer360__customer_value_analysis"]}] | [] | ["lifecycle_stage"] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B4 | AVG(composite_engagement_score) | [{"table": "customer360__customer_activity_metrics", "column": "composite_engagement_score"}] | [] | False |
| B6 | COUNT(*) | [] | [] | True |
| B7 | COUNT(*) | [] | [] | True |
| B7 | COUNT(*) | [] | [] | True |


未解析列血缘：[{"block": "B5", "column": "composite_engagement_score", "reason": "ambiguous_or_missing_source"}]

## S87

类别 `data`；来源 `python`；调用 `7c1f4cd1177543a78cc39e8eb4d696a0`；状态 `success`。

```sql

WITH latest_activity AS (
  SELECT *, ROW_NUMBER() OVER (PARTITION BY primary_email ORDER BY activity_analysis_timestamp DESC) AS rn
  FROM customer360__customer_activity_metrics
),
latest_funnel AS (
  SELECT *, ROW_NUMBER() OVER (PARTITION BY primary_email ORDER BY funnel_analysis_timestamp DESC) AS rn
  FROM customer360__conversion_funnel_analysis
),
latest_value AS (
  SELECT *, ROW_NUMBER() OVER (PARTITION BY primary_email ORDER BY analysis_timestamp DESC) AS rn
  FROM customer360__customer_value_analysis
),
cohort AS (
  SELECT a.primary_email, a.composite_engagement_score, 
         f.marketing_to_sales_days, f.sales_to_support_days,
         f.customer_tier, f.estimated_customer_ltv AS funnel_ltv,
         a.primary_engagement_channel, a.zendesk_active,
         a.in_marketo, a.in_stripe, a.in_zendesk,
         a.customer_health_score, a.activity_risk_level, a.engagement_velocity,
         a.customer_segment, a.lifecycle_stage,
         a.cross_platform_consistency, a.activity_efficiency,
         a.days_since_last_activity, a.estimated_monthly_activities,
         v.rfm_segment, v.churn_probability, v.investment_priority_score,
         v.risk_category
  FROM latest_activity a
  JOIN latest_funnel f ON a.primary_email = f.primary_email AND f.rn = 1
  JOIN latest_value v ON a.primary_email = v.primary_email AND v.rn = 1
  WHERE a.rn = 1
    AND f.marketing_to_sales_days BETWEEN 10 AND 20
    AND f.sales_to_support_days > 30
    AND a.composite_engagement_score > (SELECT AVG(composite_engagement_score) FROM customer360__customer_activity_metrics)
)
SELECT * FROM cohort

```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-054/attempt-01/sql/S87.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-054/attempt-01/sql/S87.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-054/attempt-01/results/S87.rows.jsonl)；完整：True；SHA256：`8b6520fc50dc611cd4d5571d848e23fc9e156f2b038ed7a0adb6e28d814c9e42`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "customer360__customer_activity_metrics", "kind": "base", "block": null, "base_tables": ["customer360__customer_activity_metrics"]}] | [] | [] |
| B2 | [{"alias": "customer360__conversion_funnel_analysis", "kind": "base", "block": null, "base_tables": ["customer360__conversion_funnel_analysis"]}] | [] | [] |
| B3 | [{"alias": "customer360__customer_value_analysis", "kind": "base", "block": null, "base_tables": ["customer360__customer_value_analysis"]}] | [] | [] |
| B4 | [{"alias": "customer360__customer_activity_metrics", "kind": "base", "block": null, "base_tables": ["customer360__customer_activity_metrics"]}] | [] | [] |
| B5 | [{"alias": "a", "kind": "derived", "block": "B1", "base_tables": ["customer360__customer_activity_metrics"]}, {"alias": "f", "kind": "derived", "block": "B2", "base_tables": ["customer360__conversion_funnel_analysis"]}, {"alias": "v", "kind": "derived", "block": "B3", "base_tables": ["customer360__customer_value_analysis"]}] | [{"type": "INNER", "right": "latest_funnel AS f", "on": "a.primary_email = f.primary_email AND f.rn = 1", "using": []}, {"type": "INNER", "right": "latest_value AS v", "on": "a.primary_email = v.primary_email AND v.rn = 1", "using": []}] | [] |
| B6 | [{"alias": "cohort", "kind": "derived", "block": "B5", "base_tables": ["customer360__conversion_funnel_analysis", "customer360__customer_activity_metrics", "customer360__customer_value_analysis"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B4 | AVG(composite_engagement_score) | [{"table": "customer360__customer_activity_metrics", "column": "composite_engagement_score"}] | [] | False |


未解析列血缘：[{"block": "B5", "column": "composite_engagement_score", "reason": "ambiguous_or_missing_source"}]

## S88

类别 `data`；来源 `query_db`；调用 `d2cd4fddc21a42fcb4fb7d9d83ddfdfb`；状态 `success`。

```sql
-- Check the address table country distribution
SELECT country, COUNT(DISTINCT customer360_id) AS cnt
FROM customer360__address
WHERE country IS NOT NULL AND country != ''
GROUP BY country
ORDER BY cnt DESC
LIMIT 20
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-054/attempt-01/sql/S88.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-054/attempt-01/sql/S88.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-054/attempt-01/results/S88.rows.jsonl)；完整：True；SHA256：`88e6f9eaa0c521306b3487d7a7736b91bab2ea4500901eebf518b338bf7593de`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "customer360__address", "kind": "base", "block": null, "base_tables": ["customer360__address"]}] | [] | ["country"] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(DISTINCT customer360_id) | [{"table": "customer360__address", "column": "customer360_id"}] | [] | False |


## S89

类别 `data`；来源 `query_db`；调用 `596e867392934195b505d50784725157`；状态 `success`。

```sql
-- Check if there's a way to link address by looking at the frequency of customer360_id values
-- that match the count of distinct customer records
SELECT COUNT(DISTINCT customer360_id) AS total_ids,
       COUNT(*) AS total_rows
FROM customer360__address
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-054/attempt-01/sql/S89.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-054/attempt-01/sql/S89.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-054/attempt-01/results/S89.rows.jsonl)；完整：True；SHA256：`195c25030d8b194af80ec8e8129d44fc27dc6ddd6342a4318587445969639a8d`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "customer360__address", "kind": "base", "block": null, "base_tables": ["customer360__address"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(DISTINCT customer360_id) | [{"table": "customer360__address", "column": "customer360_id"}] | [] | False |
| B1 | COUNT(*) | [] | [] | True |


## S90

类别 `data`；来源 `query_db`；调用 `b82b0ac1385b40b9afe93f9e12785e42`；状态 `success`。

```sql
-- Check real country info
SELECT country_code, COUNT(DISTINCT customer360_id) AS cnt
FROM customer360__address
WHERE country_code IS NOT NULL AND country_code != ''
GROUP BY country_code
ORDER BY cnt DESC
LIMIT 20
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-054/attempt-01/sql/S90.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-054/attempt-01/sql/S90.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-054/attempt-01/results/S90.rows.jsonl)；完整：True；SHA256：`e9546734265bf24fedac88b82bb647272084cc1640176eada73490f4a04cfeec`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "customer360__address", "kind": "base", "block": null, "base_tables": ["customer360__address"]}] | [] | ["country_code"] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(DISTINCT customer360_id) | [{"table": "customer360__address", "column": "customer360_id"}] | [] | False |


## S91

类别 `data`；来源 `query_db`；调用 `0003fd2d48094743963b8f60498f78d5`；状态 `success`。

```sql
-- Check state distribution
SELECT state, COUNT(DISTINCT customer360_id) AS cnt
FROM customer360__address
WHERE state IS NOT NULL AND state != ''
GROUP BY state
ORDER BY cnt DESC
LIMIT 20
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-054/attempt-01/sql/S91.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-054/attempt-01/sql/S91.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-054/attempt-01/results/S91.rows.jsonl)；完整：True；SHA256：`868dd07331f41bdcab292a9ae6efdaaa3b8bf5598e83b29452547bf49ffe57e9`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "customer360__address", "kind": "base", "block": null, "base_tables": ["customer360__address"]}] | [] | ["state"] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(DISTINCT customer360_id) | [{"table": "customer360__address", "column": "customer360_id"}] | [] | False |


## S92

类别 `data`；来源 `python`；调用 `d18050c2749f4c01a9353405bfc1e8a4`；状态 `success`。

```sql

  SELECT country, country_code, state, COUNT(DISTINCT customer360_id) AS customer_count
  FROM customer360__address
  WHERE country IS NOT NULL AND country != ''
  GROUP BY country
  ORDER BY customer_count DESC
  LIMIT 15

```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-054/attempt-01/sql/S92.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-054/attempt-01/sql/S92.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-054/attempt-01/results/S92.rows.jsonl)；完整：True；SHA256：`1002142a45821fb44ea1b39b08bce9d39752d97d41c4bf5062664327b938f2e9`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "customer360__address", "kind": "base", "block": null, "base_tables": ["customer360__address"]}] | [] | ["country"] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(DISTINCT customer360_id) | [{"table": "customer360__address", "column": "customer360_id"}] | [] | False |


## S93

类别 `data`；来源 `python`；调用 `d18050c2749f4c01a9353405bfc1e8a4`；状态 `success`。

```sql

  SELECT state, COUNT(DISTINCT customer360_id) AS customer_count
  FROM customer360__address
  WHERE state IS NOT NULL AND state != ''
  GROUP BY state
  ORDER BY customer_count DESC
  LIMIT 15

```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-054/attempt-01/sql/S93.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-054/attempt-01/sql/S93.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-054/attempt-01/results/S93.rows.jsonl)；完整：True；SHA256：`82dfa3eb89256683e99b31a5e3805da70d9aeefe0856d1372e8c3271e04c4cd0`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "customer360__address", "kind": "base", "block": null, "base_tables": ["customer360__address"]}] | [] | ["state"] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(DISTINCT customer360_id) | [{"table": "customer360__address", "column": "customer360_id"}] | [] | False |


## S94

类别 `data`；来源 `query_db`；调用 `8e976eba52cf4ce9aa3bb5843cb71659`；状态 `success`。

```sql
-- Framework analysis: cross_platform_consistency and activity_efficiency impact on health
WITH latest_activity AS (
  SELECT *, ROW_NUMBER() OVER (PARTITION BY primary_email ORDER BY activity_analysis_timestamp DESC) AS rn
  FROM customer360__customer_activity_metrics
),
latest_funnel AS (
  SELECT *, ROW_NUMBER() OVER (PARTITION BY primary_email ORDER BY funnel_analysis_timestamp DESC) AS rn
  FROM customer360__conversion_funnel_analysis
),
latest_value AS (
  SELECT *, ROW_NUMBER() OVER (PARTITION BY primary_email ORDER BY analysis_timestamp DESC) AS rn
  FROM customer360__customer_value_analysis
),
cohort AS (
  SELECT a.primary_email, a.composite_engagement_score, 
         f.marketing_to_sales_days, f.sales_to_support_days,
         f.customer_tier, f.estimated_customer_ltv AS funnel_ltv,
         a.primary_engagement_channel, a.zendesk_active,
         a.in_marketo, a.in_stripe, a.in_zendesk,
         a.customer_health_score, a.activity_risk_level, a.engagement_velocity,
         a.cross_platform_consistency, a.activity_efficiency,
         a.days_since_last_activity, a.estimated_monthly_activities,
         v.rfm_segment, v.churn_probability, v.investment_priority_score,
         v.risk_category, v.rfm_score, v.recency_score, v.frequency_score, v.monetary_score
  FROM latest_activity a
  JOIN latest_funnel f ON a.primary_email = f.primary_email AND f.rn = 1
  JOIN latest_value v ON a.primary_email = v.primary_email AND v.rn = 1
  WHERE a.rn = 1
    AND f.marketing_to_sales_days BETWEEN 10 AND 20
    AND f.sales_to_support_days > 30
    AND a.composite_engagement_score > (SELECT AVG(composite_engagement_score) FROM customer360__customer_activity_metrics)
)
SELECT 
  activity_risk_level,
  engagement_velocity,
  COUNT(*) AS cnt,
  ROUND(AVG(customer_health_score), 1) AS avg_health,
  ROUND(AVG(funnel_ltv), 0) AS avg_ltv,
  ROUND(AVG(composite_engagement_score), 1) AS avg_engagement,
  ROUND(AVG(churn_probability), 3) AS avg_churn_prob,
  ROUND(AVG(cross_platform_consistency), 3) AS avg_platform_consistency,
  ROUND(AVG(days_since_last_activity), 0) AS avg_days_since_activity
FROM cohort
GROUP BY activity_risk_level, engagement_velocity
ORDER BY activity_risk_level, engagement_velocity
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-054/attempt-01/sql/S94.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-054/attempt-01/sql/S94.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-054/attempt-01/results/S94.rows.jsonl)；完整：True；SHA256：`4dd54731e2280a989eb5bf7e528157c03ea71c04b56681fb64cb2bfe7eefaf7c`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "customer360__customer_activity_metrics", "kind": "base", "block": null, "base_tables": ["customer360__customer_activity_metrics"]}] | [] | [] |
| B2 | [{"alias": "customer360__conversion_funnel_analysis", "kind": "base", "block": null, "base_tables": ["customer360__conversion_funnel_analysis"]}] | [] | [] |
| B3 | [{"alias": "customer360__customer_value_analysis", "kind": "base", "block": null, "base_tables": ["customer360__customer_value_analysis"]}] | [] | [] |
| B4 | [{"alias": "customer360__customer_activity_metrics", "kind": "base", "block": null, "base_tables": ["customer360__customer_activity_metrics"]}] | [] | [] |
| B5 | [{"alias": "a", "kind": "derived", "block": "B1", "base_tables": ["customer360__customer_activity_metrics"]}, {"alias": "f", "kind": "derived", "block": "B2", "base_tables": ["customer360__conversion_funnel_analysis"]}, {"alias": "v", "kind": "derived", "block": "B3", "base_tables": ["customer360__customer_value_analysis"]}] | [{"type": "INNER", "right": "latest_funnel AS f", "on": "a.primary_email = f.primary_email AND f.rn = 1", "using": []}, {"type": "INNER", "right": "latest_value AS v", "on": "a.primary_email = v.primary_email AND v.rn = 1", "using": []}] | [] |
| B6 | [{"alias": "cohort", "kind": "derived", "block": "B5", "base_tables": ["customer360__conversion_funnel_analysis", "customer360__customer_activity_metrics", "customer360__customer_value_analysis"]}] | [] | ["activity_risk_level", "engagement_velocity"] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B4 | AVG(composite_engagement_score) | [{"table": "customer360__customer_activity_metrics", "column": "composite_engagement_score"}] | [] | False |
| B6 | COUNT(*) | [] | [] | True |
| B6 | AVG(customer_health_score) | [{"table": "customer360__customer_activity_metrics", "column": "customer_health_score"}] | [] | False |
| B6 | AVG(funnel_ltv) | [{"table": "customer360__conversion_funnel_analysis", "column": "estimated_customer_ltv"}] | [] | False |
| B6 | AVG(composite_engagement_score) | [{"table": "customer360__customer_activity_metrics", "column": "composite_engagement_score"}] | [] | False |
| B6 | AVG(churn_probability) | [{"table": "customer360__customer_value_analysis", "column": "churn_probability"}] | [] | False |
| B6 | AVG(cross_platform_consistency) | [{"table": "customer360__customer_activity_metrics", "column": "cross_platform_consistency"}] | [] | False |
| B6 | AVG(days_since_last_activity) | [{"table": "customer360__customer_activity_metrics", "column": "days_since_last_activity"}] | [] | False |


未解析列血缘：[{"block": "B5", "column": "composite_engagement_score", "reason": "ambiguous_or_missing_source"}]

## S95

类别 `data`；来源 `query_db`；调用 `682397f307884dd1a83e264fcc1220a4`；状态 `success`。

```sql
-- Full risk-velocity breakdown
WITH latest_activity AS (
  SELECT *, ROW_NUMBER() OVER (PARTITION BY primary_email ORDER BY activity_analysis_timestamp DESC) AS rn
  FROM customer360__customer_activity_metrics
),
latest_funnel AS (
  SELECT *, ROW_NUMBER() OVER (PARTITION BY primary_email ORDER BY funnel_analysis_timestamp DESC) AS rn
  FROM customer360__conversion_funnel_analysis
),
latest_value AS (
  SELECT *, ROW_NUMBER() OVER (PARTITION BY primary_email ORDER BY analysis_timestamp DESC) AS rn
  FROM customer360__customer_value_analysis
),
cohort AS (
  SELECT a.primary_email, a.composite_engagement_score, 
         f.marketing_to_sales_days, f.sales_to_support_days,
         f.customer_tier, f.estimated_customer_ltv AS funnel_ltv,
         a.primary_engagement_channel, a.zendesk_active,
         a.in_marketo, a.in_stripe, a.in_zendesk,
         a.customer_health_score, a.activity_risk_level, a.engagement_velocity,
         a.cross_platform_consistency, a.activity_efficiency,
         a.days_since_last_activity, a.estimated_monthly_activities,
         v.rfm_segment, v.churn_probability, v.investment_priority_score,
         v.risk_category, v.rfm_score, v.recency_score, v.frequency_score, v.monetary_score
  FROM latest_activity a
  JOIN latest_funnel f ON a.primary_email = f.primary_email AND f.rn = 1
  JOIN latest_value v ON a.primary_email = v.primary_email AND v.rn = 1
  WHERE a.rn = 1
    AND f.marketing_to_sales_days BETWEEN 10 AND 20
    AND f.sales_to_support_days > 30
    AND a.composite_engagement_score > (SELECT AVG(composite_engagement_score) FROM customer360__customer_activity_metrics)
)
SELECT 
  activity_risk_level,
  engagement_velocity,
  COUNT(*) AS cnt,
  ROUND(AVG(customer_health_score), 1) AS avg_health,
  ROUND(AVG(funnel_ltv), 0) AS avg_ltv,
  ROUND(AVG(composite_engagement_score), 1) AS avg_engagement,
  ROUND(AVG(churn_probability), 3) AS avg_churn_prob,
  ROUND(AVG(cross_platform_consistency), 3) AS avg_platform_consistency,
  ROUND(AVG(days_since_last_activity), 0) AS avg_days_since_activity
FROM cohort
GROUP BY activity_risk_level, engagement_velocity
ORDER BY activity_risk_level, engagement_velocity
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-054/attempt-01/sql/S95.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-054/attempt-01/sql/S95.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-054/attempt-01/results/S95.rows.jsonl)；完整：True；SHA256：`4dd54731e2280a989eb5bf7e528157c03ea71c04b56681fb64cb2bfe7eefaf7c`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "customer360__customer_activity_metrics", "kind": "base", "block": null, "base_tables": ["customer360__customer_activity_metrics"]}] | [] | [] |
| B2 | [{"alias": "customer360__conversion_funnel_analysis", "kind": "base", "block": null, "base_tables": ["customer360__conversion_funnel_analysis"]}] | [] | [] |
| B3 | [{"alias": "customer360__customer_value_analysis", "kind": "base", "block": null, "base_tables": ["customer360__customer_value_analysis"]}] | [] | [] |
| B4 | [{"alias": "customer360__customer_activity_metrics", "kind": "base", "block": null, "base_tables": ["customer360__customer_activity_metrics"]}] | [] | [] |
| B5 | [{"alias": "a", "kind": "derived", "block": "B1", "base_tables": ["customer360__customer_activity_metrics"]}, {"alias": "f", "kind": "derived", "block": "B2", "base_tables": ["customer360__conversion_funnel_analysis"]}, {"alias": "v", "kind": "derived", "block": "B3", "base_tables": ["customer360__customer_value_analysis"]}] | [{"type": "INNER", "right": "latest_funnel AS f", "on": "a.primary_email = f.primary_email AND f.rn = 1", "using": []}, {"type": "INNER", "right": "latest_value AS v", "on": "a.primary_email = v.primary_email AND v.rn = 1", "using": []}] | [] |
| B6 | [{"alias": "cohort", "kind": "derived", "block": "B5", "base_tables": ["customer360__conversion_funnel_analysis", "customer360__customer_activity_metrics", "customer360__customer_value_analysis"]}] | [] | ["activity_risk_level", "engagement_velocity"] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B4 | AVG(composite_engagement_score) | [{"table": "customer360__customer_activity_metrics", "column": "composite_engagement_score"}] | [] | False |
| B6 | COUNT(*) | [] | [] | True |
| B6 | AVG(customer_health_score) | [{"table": "customer360__customer_activity_metrics", "column": "customer_health_score"}] | [] | False |
| B6 | AVG(funnel_ltv) | [{"table": "customer360__conversion_funnel_analysis", "column": "estimated_customer_ltv"}] | [] | False |
| B6 | AVG(composite_engagement_score) | [{"table": "customer360__customer_activity_metrics", "column": "composite_engagement_score"}] | [] | False |
| B6 | AVG(churn_probability) | [{"table": "customer360__customer_value_analysis", "column": "churn_probability"}] | [] | False |
| B6 | AVG(cross_platform_consistency) | [{"table": "customer360__customer_activity_metrics", "column": "cross_platform_consistency"}] | [] | False |
| B6 | AVG(days_since_last_activity) | [{"table": "customer360__customer_activity_metrics", "column": "days_since_last_activity"}] | [] | False |


未解析列血缘：[{"block": "B5", "column": "composite_engagement_score", "reason": "ambiguous_or_missing_source"}]

## S96

类别 `data`；来源 `query_db`；调用 `794e5678ad3a47b7bcc8139aee165215`；状态 `success`。

```sql
-- RFM segment distribution in cohort
WITH latest_activity AS (
  SELECT *, ROW_NUMBER() OVER (PARTITION BY primary_email ORDER BY activity_analysis_timestamp DESC) AS rn
  FROM customer360__customer_activity_metrics
),
latest_funnel AS (
  SELECT *, ROW_NUMBER() OVER (PARTITION BY primary_email ORDER BY funnel_analysis_timestamp DESC) AS rn
  FROM customer360__conversion_funnel_analysis
),
latest_value AS (
  SELECT *, ROW_NUMBER() OVER (PARTITION BY primary_email ORDER BY analysis_timestamp DESC) AS rn
  FROM customer360__customer_value_analysis
),
cohort AS (
  SELECT a.primary_email, f.customer_tier, v.rfm_segment, v.rfm_score,
         v.recency_score, v.frequency_score, v.monetary_score,
         a.customer_health_score, f.estimated_customer_ltv AS funnel_ltv,
         a.activity_risk_level, a.engagement_velocity
  FROM latest_activity a
  JOIN latest_funnel f ON a.primary_email = f.primary_email AND f.rn = 1
  JOIN latest_value v ON a.primary_email = v.primary_email AND v.rn = 1
  WHERE a.rn = 1
    AND f.marketing_to_sales_days BETWEEN 10 AND 20
    AND f.sales_to_support_days > 30
    AND a.composite_engagement_score > (SELECT AVG(composite_engagement_score) FROM customer360__customer_activity_metrics)
)
SELECT rfm_segment, COUNT(*) AS cnt, 
       ROUND(100.0 * COUNT(*) / (SELECT COUNT(*) FROM cohort), 2) AS pct,
       ROUND(AVG(recency_score), 1) AS avg_recency,
       ROUND(AVG(frequency_score), 1) AS avg_frequency,
       ROUND(AVG(monetary_score), 1) AS avg_monetary,
       ROUND(AVG(funnel_ltv), 0) AS avg_ltv,
       ROUND(AVG(customer_health_score), 1) AS avg_health
FROM cohort
GROUP BY rfm_segment
ORDER BY cnt DESC
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-054/attempt-01/sql/S96.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-054/attempt-01/sql/S96.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-054/attempt-01/results/S96.rows.jsonl)；完整：True；SHA256：`90370ce2468a0ce894241e7962d3336a23ba31fec494d9bdb5578f6ba4c3fe81`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "customer360__customer_activity_metrics", "kind": "base", "block": null, "base_tables": ["customer360__customer_activity_metrics"]}] | [] | [] |
| B2 | [{"alias": "customer360__conversion_funnel_analysis", "kind": "base", "block": null, "base_tables": ["customer360__conversion_funnel_analysis"]}] | [] | [] |
| B3 | [{"alias": "customer360__customer_value_analysis", "kind": "base", "block": null, "base_tables": ["customer360__customer_value_analysis"]}] | [] | [] |
| B4 | [{"alias": "customer360__customer_activity_metrics", "kind": "base", "block": null, "base_tables": ["customer360__customer_activity_metrics"]}] | [] | [] |
| B5 | [{"alias": "a", "kind": "derived", "block": "B1", "base_tables": ["customer360__customer_activity_metrics"]}, {"alias": "f", "kind": "derived", "block": "B2", "base_tables": ["customer360__conversion_funnel_analysis"]}, {"alias": "v", "kind": "derived", "block": "B3", "base_tables": ["customer360__customer_value_analysis"]}] | [{"type": "INNER", "right": "latest_funnel AS f", "on": "a.primary_email = f.primary_email AND f.rn = 1", "using": []}, {"type": "INNER", "right": "latest_value AS v", "on": "a.primary_email = v.primary_email AND v.rn = 1", "using": []}] | [] |
| B6 | [{"alias": "cohort", "kind": "derived", "block": "B5", "base_tables": ["customer360__conversion_funnel_analysis", "customer360__customer_activity_metrics", "customer360__customer_value_analysis"]}] | [] | [] |
| B7 | [{"alias": "cohort", "kind": "derived", "block": "B5", "base_tables": ["customer360__conversion_funnel_analysis", "customer360__customer_activity_metrics", "customer360__customer_value_analysis"]}] | [] | ["rfm_segment"] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B4 | AVG(composite_engagement_score) | [{"table": "customer360__customer_activity_metrics", "column": "composite_engagement_score"}] | [] | False |
| B6 | COUNT(*) | [] | [] | True |
| B7 | COUNT(*) | [] | [] | True |
| B7 | AVG(recency_score) | [{"table": "customer360__customer_value_analysis", "column": "recency_score"}] | [] | False |
| B7 | AVG(frequency_score) | [{"table": "customer360__customer_value_analysis", "column": "frequency_score"}] | [] | False |
| B7 | AVG(monetary_score) | [{"table": "customer360__customer_value_analysis", "column": "monetary_score"}] | [] | False |
| B7 | AVG(funnel_ltv) | [{"table": "customer360__conversion_funnel_analysis", "column": "estimated_customer_ltv"}] | [] | False |
| B7 | AVG(customer_health_score) | [{"table": "customer360__customer_activity_metrics", "column": "customer_health_score"}] | [] | False |
| B7 | COUNT(*) | [] | [] | True |


未解析列血缘：[{"block": "B5", "column": "composite_engagement_score", "reason": "ambiguous_or_missing_source"}]
