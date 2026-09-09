# dacomp-055

The company is reassessing its customer investment strategy and needs to identify customer…

运行：已提交。官方未评分。全部 SQL 尝试/成功 72/62；数据 SQL 70/60；Python 17 次。

完整原题：

The company is reassessing its customer investment strategy and needs to identify customer segments where investment allocation does not match actual returns. Filter for customers who are in the top 30% for `investment_priority_score` but in the bottom 50% for a composite performance metric (weighted as 40% `total_sales_amount`, 35% `product_adoption_rate`, and 25% `support_resolution_efficiency`). For these customers, calculate the ROI ratio of `customer_lifetime_value` to `acquisition_cost` and analyze their distribution characteristics across different `lifecycle_stage`s. Deep dive into the behavioral pattern disparities of this customer cohort: analyze the root causes of performance divergence by `industry_vertical` and `company_size_tier`, investigate the correlation between `customer_onboarding_score` and subsequent product adoption rates, and examine the impact mechanism of `team_size` and `decision_maker_level` on investment return effectiveness. Finally, identify systemic biases in the investment decision model and propose optimization recommendations.

| 表 | 行数 | 列数 |
| --- | --- | --- |
| customer360__customer | 102416 | 41 |
| customer360__customer_value_analysis | 5001 | 62 |
| customer360__mapping | 18036 | 15 |


实际路线（分析者依据 SQL/源码概括，不代表 Agent 自述）：SQL 提取投资与表现特征 → Python 合并销售数据、识别错配客群并分层聚合 → 相关检验与投资建议。

数据库大小：53,346,304 字节。

## 数据 SQL

| SQL | 状态 | 基础表 | Join 输入/类型 | GROUP BY | 聚合表达式 | 结果行数 | 数据库 ms |
| --- | --- | --- | --- | --- | --- | --- | --- |
| [S3/Q1](#s3) | success | ["customer360__customer_value_analysis"] | 0 / {} | [] | ["COUNT(*)"] | 1 | 2.237 |
| [S4/Q2](#s4) | success | ["customer360__customer_value_analysis"] | 0 / {} | [] | [] | 5 | 0.471 |
| [S5/Q3](#s5) | success | ["customer360__customer_value_analysis"] | 0 / {} | [] | ["COUNT(DISTINCT marketo_lead_id)"] | 1 | 3.842 |
| [S6/Q4](#s6) | success | ["customer360__customer_value_analysis"] | 0 / {} | [] | [] | 5 | 2.954 |
| [S7/Q5](#s7) | success | ["customer360__customer_value_analysis"] | 0 / {} | [] | [] | 11 | 3.241 |
| [S8/Q6](#s8) | success | ["customer360__customer_value_analysis"] | 0 / {} | [] | [] | 6 | 3.084 |
| [S9/Q7](#s9) | success | ["customer360__customer_value_analysis"] | 0 / {} | [] | [] | 6 | 3.042 |
| [S10/Q8](#s10) | failed | ["customer360__customer_value_analysis"] | 0 / {} | [] | ["MIN(investment_priority_score)", "MAX(investment_priority_score)", "AVG(investment_priority_score)", "MIN(total_sales_amount)", "MAX(total_sales_amount)", "AVG(total_sales_amount)", "MIN(product_adoption_rate)", "MAX(product_adoption_rate)", "AVG(product_adoption_rate)", "MIN(support_resolution_efficiency)", "MAX(support_resolution_efficiency)", "AVG(support_resolution_efficiency)"] | unknown | 未取得；调用总时长 0.167 ms |
| [S11/Q9](#s11) | success | ["customer360__customer_value_analysis"] | 0 / {} | [] | ["MIN(customer_lifetime_value)", "MAX(customer_lifetime_value)", "AVG(customer_lifetime_value)", "MIN(acquisition_cost)", "MAX(acquisition_cost)", "AVG(acquisition_cost)"] | 1 | 2.856 |
| [S12/Q10](#s12) | success | ["customer360__customer"] | 0 / {} | [] | ["COUNT(*)", "COUNT(DISTINCT customer360_id)"] | 1 | 70.344 |
| [S13/Q11](#s13) | success | ["customer360__customer_value_analysis"] | 0 / {} | ["marketo_lead_id"] | ["COUNT(*)"] | 10 | 3.093 |
| [S14/Q12](#s14) | success | ["customer360__mapping"] | 0 / {} | [] | ["COUNT(DISTINCT marketo_lead_id)", "COUNT(*)"] | 1 | 6.628 |
| [S15/Q13](#s15) | success | ["customer360__customer_value_analysis"] | 0 / {} | [] | [] | 5 | 0.574 |
| [S16/Q14](#s16) | success | ["customer360__customer_value_analysis"] | 0 / {} | ["marketo_lead_id"] | ["COUNT(*)", "COUNT(DISTINCT stripe_customer_id)", "COUNT(DISTINCT zendesk_user_id)", "COUNT(DISTINCT primary_email)"] | 10 | 9.488 |
| [S17/Q15](#s17) | success | ["customer360__mapping"] | 0 / {} | ["marketo_lead_id"] | ["COUNT(*)", "COUNT(DISTINCT customer360_id)"] | 10 | 16.402 |
| [S18/Q16](#s18) | success | ["customer360__mapping"] | 0 / {} | [] | ["COUNT(*)", "COUNT(DISTINCT customer360_id)", "COUNT(DISTINCT marketo_lead_id)"] | 1 | 20.071 |
| [S19/Q17](#s19) | success | ["customer360__customer", "customer360__mapping"] | 2 / {'INNER': 1} | ["m.marketo_lead_id"] | ["COUNT(DISTINCT c.customer360_id)", "COUNT(*)", "COUNT(DISTINCT c.total_sales_amount)"] | 1 | 216.37 |
| [S20/Q18](#s20) | success | ["customer360__customer_value_analysis"] | 0 / {} | [] | ["COUNT(*)", "COUNT(*)", "COUNT(DISTINCT marketo_lead_id \|\| stripe_customer_id \|\| zendesk_user_id \|\| primary_email)"] | 1 | 4.086 |
| [S21/Q19](#s21) | success | ["customer360__customer_value_analysis"] | 0 / {} | [] | ["COUNT(*)"] | 1 | 26.119 |
| [S22/Q20](#s22) | failed | ["customer360__customer_value_analysis"] | 0 / {} | [] | [] | unknown | 未取得；调用总时长 0.218 ms |
| [S23/Q21](#s23) | success | ["customer360__customer_value_analysis"] | 0 / {} | [] | [] | 4 | 1.91 |
| [S24/Q22](#s24) | success | ["customer360__customer_value_analysis"] | 0 / {} | [] | [] | 12 | 1.942 |
| [S25/Q23](#s25) | success | ["customer360__customer", "customer360__customer_value_analysis"] | 2 / {'INNER': 1} | [] | ["COUNT(*)"] | 1 | 188.022 |
| [S26/Q24](#s26) | success | ["customer360__customer", "customer360__customer_value_analysis"] | 2 / {'INNER': 1} | [] | [] | 10 | 209.403 |
| [S27/Q25](#s27) | success | ["customer360__customer"] | 0 / {} | [] | ["COUNT(*)", "COUNT(DISTINCT email)"] | 1 | 66.978 |
| [S28/Q26](#s28) | success | ["customer360__customer"] | 0 / {} | ["email"] | ["COUNT(*)", "COUNT(DISTINCT total_sales_amount)", "MAX(total_sales_amount)", "MIN(total_sales_amount)"] | 1 | 20.455 |
| [S29/Q27](#s29) | success | ["customer360__customer_value_analysis"] | 0 / {} | [] | ["COUNT(*)", "COUNT(DISTINCT marketo_lead_id \|\| '\|' \|\| stripe_customer_id \|\| '\|' \|\| zendesk_user_id)", "COUNT(DISTINCT stripe_customer_id)", "COUNT(DISTINCT primary_email)"] | 1 | 11.166 |
| [S30/Q28](#s30) | success | ["customer360__customer"] | 0 / {} | [] | ["COUNT(*)", "COUNT(DISTINCT email)", "COUNT(DISTINCT customer360_id)", "COUNT(DISTINCT customer360_organization_id)"] | 1 | 157.207 |
| [S31/Q29](#s31) | success | ["customer360__customer_value_analysis"] | 0 / {} | [] | ["COUNT(*)"] | 1 | 26.348 |
| [S32/Q30](#s32) | success | ["customer360__customer", "customer360__customer_value_analysis"] | 2 / {'INNER': 1} | [] | ["COUNT(*)"] | 1 | 85.734 |
| [S33/Q31](#s33) | failed | ["customer360__customer_value_analysis"] | 0 / {} | [] | ["PERCENTILE_CONT(0.3)", "PERCENTILE_CONT(0.5)"] | unknown | 未取得；调用总时长 0.134 ms |
| [S34/Q32](#s34) | success | ["customer360__customer_value_analysis"] | 0 / {} | ["investment_priority_score"] | ["COUNT(*)"] | 282 | 4.022 |
| [S35/Q33](#s35) | success | ["customer360__mapping"] | 0 / {} | ["stripe_customer_id"] | ["COUNT(*)"] | 5 | 5.075 |
| [S36/Q34](#s36) | success | ["customer360__mapping"] | 0 / {} | ["zendesk_user_id"] | ["COUNT(*)"] | 5 | 3.515 |
| [S37/Q35](#s37) | success | ["customer360__mapping"] | 0 / {} | [] | ["COUNT(DISTINCT stripe_customer_id)"] | 1 | 4.758 |
| [S38/Q36](#s38) | success | ["customer360__customer_value_analysis", "customer360__mapping"] | 0 / {} | [] | ["COUNT(DISTINCT v.stripe_customer_id)"] | 1 | 14.005 |
| [S39/Q37](#s39) | success | ["customer360__customer_value_analysis"] | 0 / {} | [] | ["COUNT(DISTINCT v.stripe_customer_id)"] | 1 | 3.964 |
| [S40/Q38](#s40) | success | ["customer360__customer", "customer360__customer_value_analysis"] | 2 / {'LEFT': 1} | ["v.primary_email"] | ["MAX(c.total_sales_amount)"] | 4734 | 289.145 |
| [S41/Q39](#s41) | success | ["customer360__customer_value_analysis"] | 0 / {} | [] | ["COUNT(*)"] | 1 | 9.224 |
| [S42/Q40](#s42) | success | ["customer360__customer", "customer360__customer_value_analysis"] | 2 / {'LEFT': 1} | ["email"] | ["MAX(total_sales_amount)", "COUNT(*)", "SUM(CASE WHEN v.investment_priority_score IS NULL THEN 1 ELSE 0 END)", "SUM(CASE WHEN v.product_adoption_rate IS NULL THEN 1 ELSE 0 END)", "SUM(CASE WHEN v.support_resolution_efficiency IS NULL THEN 1 ELSE 0 END)", "SUM(CASE WHEN v.total_sales_amount IS NULL THEN 1 ELSE 0 END)", "SUM(CASE WHEN v.acquisition_cost IS NULL THEN 1 ELSE 0 END)", "SUM(CASE WHEN v.customer_lifetime_value IS NULL THEN 1 ELSE 0 END)"] | 1 | 130.715 |
| [S43/Q41](#s43) | success | ["customer360__customer_value_analysis"] | 0 / {} | ["lifecycle_stage"] | ["COUNT(*)", "SUM(CASE WHEN product_adoption_rate IS NULL THEN 1 ELSE 0 END)"] | 5 | 27.534 |
| [S44/Q42](#s44) | success | ["customer360__customer", "customer360__customer_value_analysis"] | 2 / {'LEFT': 1} | ["email"] | ["MAX(total_sales_amount)", "COUNT(*)", "MIN(investment_priority_score)", "MAX(investment_priority_score)", "MIN(product_adoption_rate)", "MAX(product_adoption_rate)", "MIN(support_resolution_efficiency)", "MAX(support_resolution_efficiency)", "MIN(total_sales_amount)", "MAX(total_sales_amount)", "MIN(acquisition_cost)", "MAX(acquisition_cost)", "MIN(customer_lifetime_value)", "MAX(customer_lifetime_value)"] | 1 | 119.294 |
| [S45/Q43](#s45) | success | ["customer360__customer", "customer360__customer_value_analysis"] | 2 / {'LEFT': 1} | ["email"] | ["MAX(total_sales_amount)", "MIN(investment_priority_score)", "MAX(investment_priority_score)", "AVG(investment_priority_score)"] | 1 | 122.613 |
| [S46/Q44](#s46) | success | ["customer360__customer", "customer360__customer_value_analysis"] | 2 / {'LEFT': 1} | ["email"] | ["MAX(total_sales_amount)", "MIN(total_sales_amount)", "MAX(total_sales_amount)", "MIN(total_sales_amount)", "MIN(product_adoption_rate)", "MAX(product_adoption_rate)", "MIN(product_adoption_rate)", "MIN(support_resolution_efficiency)", "MAX(support_resolution_efficiency)", "MIN(support_resolution_efficiency)", "COUNT(*)", "SUM(CASE WHEN rn_ips_asc >= 0.7 * total_cnt AND rn_comp_asc <= 0.5 * total_cnt THEN 1 ELSE 0 END)", "SUM(CASE WHEN rn_ips_asc >= 0.7 * total_cnt THEN 1 ELSE 0 END)", "SUM(CASE WHEN rn_comp_asc <= 0.5 * total_cnt THEN 1 ELSE 0 END)"] | 1 | 151.626 |
| [S47/Q45](#s47) | success | ["customer360__customer", "customer360__customer_value_analysis"] | 2 / {'LEFT': 1} | ["email"] | ["MAX(total_sales_amount)", "MIN(total_sales_amount)", "MAX(total_sales_amount)", "MIN(total_sales_amount)", "MIN(product_adoption_rate)", "MAX(product_adoption_rate)", "MIN(product_adoption_rate)", "MIN(support_resolution_efficiency)", "MAX(support_resolution_efficiency)", "MIN(support_resolution_efficiency)", "COUNT(*)", "SUM(CASE WHEN rn_ips_asc >= 0.7 * total_cnt AND rn_comp_asc <= 0.5 * total_cnt THEN 1 ELSE 0 END)", "SUM(CASE WHEN rn_ips_asc >= 0.7 * total_cnt THEN 1 ELSE 0 END)", "SUM(CASE WHEN rn_comp_asc <= 0.5 * total_cnt THEN 1 ELSE 0 END)", "AVG(CASE WHEN rn_ips_asc >= 0.7 * total_cnt THEN investment_priority_score END)", "MIN(CASE WHEN rn_ips_asc >= 0.7 * total_cnt THEN investment_priority_score END)"] | 1 | 184.726 |
| [S48/Q46](#s48) | failed | ["customer360__customer", "customer360__customer_value_analysis"] | 2 / {'LEFT': 1} | ["email"] | ["MAX(total_sales_amount)", "MIN(total_sales_amount)", "MAX(total_sales_amount)", "MIN(total_sales_amount)", "MIN(product_adoption_rate)", "MAX(product_adoption_rate)", "MIN(product_adoption_rate)", "MIN(support_resolution_efficiency)", "MAX(support_resolution_efficiency)", "MIN(support_resolution_efficiency)", "COUNT(*)", "AVG(investment_priority_score)", "AVG(composite_score)", "AVG(total_sales_amount)", "AVG(product_adoption_rate)", "AVG(support_resolution_efficiency)", "AVG(customer_lifetime_value / acquisition_cost)", "MIN(customer_lifetime_value / acquisition_cost)", "MAX(customer_lifetime_value / acquisition_cost)", "PERCENTILE_CONT(customer_lifetime_value / acquisition_cost, 0.5)"] | unknown | 未取得；调用总时长 1.34 ms |
| [S49/Q47](#s49) | success | ["customer360__customer", "customer360__customer_value_analysis"] | 2 / {'LEFT': 1} | ["email"] | ["MAX(total_sales_amount)", "MIN(total_sales_amount)", "MAX(total_sales_amount)", "MIN(total_sales_amount)", "MIN(product_adoption_rate)", "MAX(product_adoption_rate)", "MIN(product_adoption_rate)", "MIN(support_resolution_efficiency)", "MAX(support_resolution_efficiency)", "MIN(support_resolution_efficiency)", "COUNT(*)", "AVG(investment_priority_score)", "AVG(composite_score)", "AVG(total_sales_amount)", "AVG(product_adoption_rate)", "AVG(support_resolution_efficiency)", "AVG(customer_lifetime_value / NULLIF(acquisition_cost, 0))"] | 1 | 185.228 |
| [S50/Q48](#s50) | success | ["customer360__customer", "customer360__customer_value_analysis"] | 2 / {'LEFT': 1} | ["email", "lifecycle_stage"] | ["MAX(total_sales_amount)", "MIN(total_sales_amount)", "MAX(total_sales_amount)", "MIN(total_sales_amount)", "MIN(product_adoption_rate)", "MAX(product_adoption_rate)", "MIN(product_adoption_rate)", "MIN(support_resolution_efficiency)", "MAX(support_resolution_efficiency)", "MIN(support_resolution_efficiency)", "COUNT(*)", "AVG(customer_lifetime_value / NULLIF(acquisition_cost, 0))", "MIN(customer_lifetime_value / NULLIF(acquisition_cost, 0))", "MAX(customer_lifetime_value / NULLIF(acquisition_cost, 0))", "AVG(investment_priority_score)", "AVG(composite_score)", "AVG(product_adoption_rate)", "AVG(support_resolution_efficiency)", "AVG(total_sales_amount)"] | 5 | 183.232 |
| [S51/Q49](#s51) | success | ["customer360__customer", "customer360__customer_value_analysis"] | 2 / {'LEFT': 1} | ["email", "industry_vertical", "company_size_tier"] | ["MAX(total_sales_amount)", "MIN(total_sales_amount)", "MAX(total_sales_amount)", "MIN(total_sales_amount)", "MIN(product_adoption_rate)", "MAX(product_adoption_rate)", "MIN(product_adoption_rate)", "MIN(support_resolution_efficiency)", "MAX(support_resolution_efficiency)", "MIN(support_resolution_efficiency)", "COUNT(*)", "AVG(customer_lifetime_value / NULLIF(acquisition_cost, 0))", "AVG(investment_priority_score)", "AVG(composite_score)", "AVG(product_adoption_rate)", "AVG(support_resolution_efficiency)", "AVG(total_sales_amount)"] | 47 | 183.153 |
| [S52/Q50](#s52) | success | ["customer360__customer", "customer360__customer_value_analysis"] | 2 / {'LEFT': 1} | ["email", "industry_vertical"] | ["MAX(total_sales_amount)", "MIN(total_sales_amount)", "MAX(total_sales_amount)", "MIN(total_sales_amount)", "MIN(product_adoption_rate)", "MAX(product_adoption_rate)", "MIN(product_adoption_rate)", "MIN(support_resolution_efficiency)", "MAX(support_resolution_efficiency)", "MIN(support_resolution_efficiency)", "COUNT(*)", "SUM(is_target)", "AVG(CASE WHEN is_target = 1 THEN customer_lifetime_value / NULLIF(acquisition_cost, 0) END)", "AVG(CASE WHEN is_target = 0 THEN customer_lifetime_value / NULLIF(acquisition_cost, 0) END)", "AVG(CASE WHEN is_target = 1 THEN investment_priority_score END)", "AVG(CASE WHEN is_target = 0 THEN investment_priority_score END)", "COUNT(*)", "SUM(is_target)"] | 10 | 187.168 |
| [S53/Q51](#s53) | success | ["customer360__customer", "customer360__customer_value_analysis"] | 2 / {'LEFT': 1} | ["email", "company_size_tier"] | ["MAX(total_sales_amount)", "MIN(total_sales_amount)", "MAX(total_sales_amount)", "MIN(total_sales_amount)", "MIN(product_adoption_rate)", "MAX(product_adoption_rate)", "MIN(product_adoption_rate)", "MIN(support_resolution_efficiency)", "MAX(support_resolution_efficiency)", "MIN(support_resolution_efficiency)", "COUNT(*)", "SUM(is_target)", "AVG(CASE WHEN is_target = 1 THEN customer_lifetime_value / NULLIF(acquisition_cost, 0) END)", "AVG(CASE WHEN is_target = 0 THEN customer_lifetime_value / NULLIF(acquisition_cost, 0) END)", "AVG(CASE WHEN is_target = 1 THEN investment_priority_score END)", "AVG(CASE WHEN is_target = 0 THEN investment_priority_score END)", "AVG(CASE WHEN is_target = 1 THEN customer_onboarding_score END)", "AVG(CASE WHEN is_target = 0 THEN customer_onboarding_score END)", "COUNT(*)", "SUM(is_target)"] | 5 | 185.859 |
| [S54/Q52](#s54) | success | ["customer360__customer", "customer360__customer_value_analysis"] | 2 / {'LEFT': 1} | ["email", "decision_maker_level"] | ["MAX(total_sales_amount)", "MIN(total_sales_amount)", "MAX(total_sales_amount)", "MIN(total_sales_amount)", "MIN(product_adoption_rate)", "MAX(product_adoption_rate)", "MIN(product_adoption_rate)", "MIN(support_resolution_efficiency)", "MAX(support_resolution_efficiency)", "MIN(support_resolution_efficiency)", "COUNT(*)", "SUM(is_target)", "AVG(CASE WHEN is_target = 1 THEN customer_lifetime_value / NULLIF(acquisition_cost, 0) END)", "AVG(CASE WHEN is_target = 0 THEN customer_lifetime_value / NULLIF(acquisition_cost, 0) END)", "AVG(CASE WHEN is_target = 1 THEN product_adoption_rate END)", "AVG(CASE WHEN is_target = 0 THEN product_adoption_rate END)", "AVG(CASE WHEN is_target = 1 THEN customer_onboarding_score END)", "AVG(CASE WHEN is_target = 0 THEN customer_onboarding_score END)", "COUNT(*)", "SUM(is_target)"] | 5 | 186.519 |
| [S55/Q53](#s55) | success | ["customer360__customer", "customer360__customer_value_analysis"] | 2 / {'LEFT': 1} | ["email", "team_bucket"] | ["MAX(total_sales_amount)", "MIN(total_sales_amount)", "MAX(total_sales_amount)", "MIN(total_sales_amount)", "MIN(product_adoption_rate)", "MAX(product_adoption_rate)", "MIN(product_adoption_rate)", "MIN(support_resolution_efficiency)", "MAX(support_resolution_efficiency)", "MIN(support_resolution_efficiency)", "COUNT(*)", "SUM(is_target)", "AVG(CASE WHEN is_target = 1 THEN customer_lifetime_value / NULLIF(acquisition_cost, 0) END)", "AVG(CASE WHEN is_target = 0 THEN customer_lifetime_value / NULLIF(acquisition_cost, 0) END)", "AVG(CASE WHEN is_target = 1 THEN product_adoption_rate END)", "AVG(CASE WHEN is_target = 0 THEN product_adoption_rate END)", "MIN(team_size)", "COUNT(*)", "SUM(is_target)"] | 5 | 185.36 |
| [S56/Q54](#s56) | success | ["customer360__customer", "customer360__customer_value_analysis"] | 2 / {'LEFT': 1} | ["email", "is_target"] | ["MAX(total_sales_amount)", "MIN(total_sales_amount)", "MAX(total_sales_amount)", "MIN(total_sales_amount)", "MIN(product_adoption_rate)", "MAX(product_adoption_rate)", "MIN(product_adoption_rate)", "MIN(support_resolution_efficiency)", "MAX(support_resolution_efficiency)", "MIN(support_resolution_efficiency)", "COUNT(*)", "AVG(customer_onboarding_score)", "AVG(product_adoption_rate)", "AVG(support_resolution_efficiency)", "AVG(customer_lifetime_value / NULLIF(acquisition_cost, 0))", "AVG(team_size)", "AVG(nps_score)", "AVG(digital_engagement_score)", "AVG(customer_health_score)", "AVG(churn_probability)"] | 2 | 186.356 |
| [S57/Q55](#s57) | failed | ["customer360__customer", "customer360__customer_value_analysis"] | 2 / {'LEFT': 1} | ["email"] | ["MAX(total_sales_amount)", "MIN(total_sales_amount)", "MAX(total_sales_amount)", "MIN(total_sales_amount)", "MIN(product_adoption_rate)", "MAX(product_adoption_rate)", "MIN(product_adoption_rate)", "MIN(support_resolution_efficiency)", "MAX(support_resolution_efficiency)", "MIN(support_resolution_efficiency)"] | unknown | 未取得；调用总时长 1.453 ms |
| [S58/Q56](#s58) | failed | ["customer360__customer", "customer360__customer_value_analysis"] | 2 / {'LEFT': 1} | ["email"] | ["MAX(total_sales_amount)", "MIN(total_sales_amount)", "MAX(total_sales_amount)", "MIN(total_sales_amount)", "MIN(product_adoption_rate)", "MAX(product_adoption_rate)", "MIN(product_adoption_rate)", "MIN(support_resolution_efficiency)", "MAX(support_resolution_efficiency)", "MIN(support_resolution_efficiency)"] | unknown | 未取得；调用总时长 1.62 ms |
| [S59/Q57](#s59) | success | ["customer360__customer_value_analysis"] | 0 / {} | [] | [] | 2000 | 5.397 |
| [S60/Q58](#s60) | failed | ["customer360__customer_value_analysis"] | 0 / {} | [] | [] | unknown | 未取得；调用总时长 0.205 ms |
| [S61/Q59](#s61) | failed | ["customer360__customer_value_analysis"] | 0 / {} | [] | [] | unknown | 未取得；调用总时长 0.193 ms |
| [S62/Q60](#s62) | failed | ["customer360__customer_value_analysis"] | 0 / {} | [] | [] | unknown | 未取得；调用总时长 0.198 ms |
| [S63/Q61](#s63) | failed | ["customer360__customer_value_analysis"] | 0 / {} | [] | [] | unknown | 未取得；调用总时长 0.139 ms |
| [S64/Q62](#s64) | success | ["customer360__customer_value_analysis"] | 0 / {} | [] | [] | 2000 | 9.043 |
| [S65/Q63](#s65) | success | ["customer360__customer_value_analysis"] | 0 / {} | [] | [] | 2000 | 8.484 |
| [S66/Q64](#s66) | success | ["customer360__customer_value_analysis"] | 0 / {} | [] | [] | 1001 | 5.374 |
| [S67/Q65](#s67) | success | ["customer360__customer_value_analysis"] | 0 / {} | [] | [] | 5 | 0.439 |
| [S68/Q66](#s68) | success | ["customer360__customer_value_analysis"] | 0 / {} | [] | [] | 2000 | 9.599 |
| [S69/Q67](#s69) | success | ["customer360__customer_value_analysis"] | 0 / {} | [] | [] | 2000 | 8.629 |
| [S70/Q68](#s70) | success | ["customer360__customer_value_analysis"] | 0 / {} | [] | [] | 1001 | 4.853 |
| [S71/Q69](#s71) | success | ["customer360__customer"] | 0 / {} | ["email"] | ["MAX(total_sales_amount)"] | 10571 | 93.893 |
| [S72/Q70](#s72) | success | ["customer360__customer", "customer360__customer_value_analysis"] | 2 / {'LEFT': 1} | ["email", "is_target"] | ["MAX(total_sales_amount)", "MIN(total_sales_amount)", "MAX(total_sales_amount)", "MIN(total_sales_amount)", "MIN(product_adoption_rate)", "MAX(product_adoption_rate)", "MIN(product_adoption_rate)", "MIN(support_resolution_efficiency)", "MAX(support_resolution_efficiency)", "MIN(support_resolution_efficiency)", "SUM(acquisition_cost)", "SUM(customer_lifetime_value)", "SUM(total_sales_amount)", "COUNT(*)", "SUM(acquisition_cost)", "SUM(customer_lifetime_value)", "SUM(total_sales_amount)", "SUM(acquisition_cost)", "SUM(customer_lifetime_value)", "SUM(total_sales_amount)"] | 2 | 187.658 |


## 元数据和设置

| SQL | 类别 | 状态 | 内容 |
| --- | --- | --- | --- |
| S1 | connection_setup | success | PRAGMA query_only=ON |
| S2 | metadata | success | SELECT name,sql FROM sqlite_master WHERE type='table' ORDER BY name |


## Python 与执行位置

人工源码审查：**database_first_violation**。Python 将客户与销售明细按邮箱合并，构造目标客群并按团队规模、行业及公司规模计算均值和比例，还计算投入与收入占比。这些连接、排名/筛选、常规聚合和算术可在 SQL 内完成。相关检验、回归及绘图不作为这些迁出计算的理由。 [证据](../reviews/dacomp-055.json)。

P1：Statistical correlation (Pearson/Spearman) between customer_onboarding_score and product_adoption_rate, plus t-tests comparing the target cohort vs non-cohort on key metrics, require scipy statistics that SQLite cannot reasonably perform. Fetching only the per-customer analytic rows (distinct customers with composite components, ROI, onboarding, team size, decision maker level, and cohort flag).

[源码](../../../runs/dsv4flash-db-first-full-01/dacomp-055/attempt-01/python/P1.py)；[输出](../../../runs/dsv4flash-db-first-full-01/dacomp-055/attempt-01/python/P1.stdout)；[错误](../../../runs/dsv4flash-db-first-full-01/dacomp-055/attempt-01/python/P1.stderr)。检出需人工核验的 SQL 可实现操作：.query(；不能仅凭理由判为合规。

P2：Fetching the analytic dataset with a smaller column set to avoid result size limits, then performing statistical tests (Pearson/Spearman correlations, t-tests) that require scipy.

[源码](../../../runs/dsv4flash-db-first-full-01/dacomp-055/attempt-01/python/P2.py)；[输出](../../../runs/dsv4flash-db-first-full-01/dacomp-055/attempt-01/python/P2.stdout)；[错误](../../../runs/dsv4flash-db-first-full-01/dacomp-055/attempt-01/python/P2.stderr)。检出需人工核验的 SQL 可实现操作：.query(；不能仅凭理由判为合规。

P3：Testing the result size limits for the analytic fetch so I can split the dataset retrieval into chunks within the SQL-archived interface.

[源码](../../../runs/dsv4flash-db-first-full-01/dacomp-055/attempt-01/python/P3.py)；[输出](../../../runs/dsv4flash-db-first-full-01/dacomp-055/attempt-01/python/P3.stdout)；[错误](../../../runs/dsv4flash-db-first-full-01/dacomp-055/attempt-01/python/P3.stderr)。检出需人工核验的 SQL 可实现操作：.query(；不能仅凭理由判为合规。

P4：Testing if the full dataset (5001 rows) fits within the result size limit for the archived query interface.

[源码](../../../runs/dsv4flash-db-first-full-01/dacomp-055/attempt-01/python/P4.py)；[输出](../../../runs/dsv4flash-db-first-full-01/dacomp-055/attempt-01/python/P4.stdout)；[错误](../../../runs/dsv4flash-db-first-full-01/dacomp-055/attempt-01/python/P4.stderr)。检出需人工核验的 SQL 可实现操作：.query(；不能仅凭理由判为合规。

P5：Testing different row limits to find the maximum completable result size for the analytic query interface.

[源码](../../../runs/dsv4flash-db-first-full-01/dacomp-055/attempt-01/python/P5.py)；[输出](../../../runs/dsv4flash-db-first-full-01/dacomp-055/attempt-01/python/P5.stdout)；[错误](../../../runs/dsv4flash-db-first-full-01/dacomp-055/attempt-01/python/P5.stderr)。检出需人工核验的 SQL 可实现操作：.query(；不能仅凭理由判为合规。

P6：Narrowing down the completable result size threshold for the archived query interface.

[源码](../../../runs/dsv4flash-db-first-full-01/dacomp-055/attempt-01/python/P6.py)；[输出](../../../runs/dsv4flash-db-first-full-01/dacomp-055/attempt-01/python/P6.stdout)；[错误](../../../runs/dsv4flash-db-first-full-01/dacomp-055/attempt-01/python/P6.stderr)。检出需人工核验的 SQL 可实现操作：.query(；不能仅凭理由判为合规。

P7：Fetching the dataset in 2000-row chunks from the value_analysis table to work around the result size limit, then combining in Python.

[源码](../../../runs/dsv4flash-db-first-full-01/dacomp-055/attempt-01/python/P7.py)；[输出](../../../runs/dsv4flash-db-first-full-01/dacomp-055/attempt-01/python/P7.stdout)；[错误](../../../runs/dsv4flash-db-first-full-01/dacomp-055/attempt-01/python/P7.stderr)。检出需人工核验的 SQL 可实现操作：.query(；不能仅凭理由判为合规。

P8：Debugging column names from the chunked fetch to fix the dataframe assembly issue.

[源码](../../../runs/dsv4flash-db-first-full-01/dacomp-055/attempt-01/python/P8.py)；[输出](../../../runs/dsv4flash-db-first-full-01/dacomp-055/attempt-01/python/P8.stdout)；[错误](../../../runs/dsv4flash-db-first-full-01/dacomp-055/attempt-01/python/P8.stderr)。检出需人工核验的 SQL 可实现操作：.query(；不能仅凭理由判为合规。

P9：Fixing the dataframe construction by passing column names explicitly from the query result metadata, then performing the full statistical analysis (correlations, t-tests) in Python.

[源码](../../../runs/dsv4flash-db-first-full-01/dacomp-055/attempt-01/python/P9.py)；[输出](../../../runs/dsv4flash-db-first-full-01/dacomp-055/attempt-01/python/P9.stdout)；[错误](../../../runs/dsv4flash-db-first-full-01/dacomp-055/attempt-01/python/P9.stderr)。检出需人工核验的 SQL 可实现操作：groupby(, .merge(, .query(, sort_values(；不能仅凭理由判为合规。

P10：Recomputing the cohort with the same deduplication and ROW_NUMBER-equivalent ranking as SQL (dedupe on analysis columns, method='first' percentile ranks) so Python statistics match the SQL cohort exactly, then generating visualizations for the report.

[源码](../../../runs/dsv4flash-db-first-full-01/dacomp-055/attempt-01/python/P10.py)；[输出](../../../runs/dsv4flash-db-first-full-01/dacomp-055/attempt-01/python/P10.stdout)；[错误](../../../runs/dsv4flash-db-first-full-01/dacomp-055/attempt-01/python/P10.stderr)。检出需人工核验的 SQL 可实现操作：groupby(；不能仅凭理由判为合规。

P11：Investigating investment-model bias: comparing investment_priority_score against actual ROI and its components, checking customer_health_score semantics, and quantifying which performance components drive the cohort's low composite score. These correlation/statistical checks require scipy and are outside SQL's capabilities.

[源码](../../../runs/dsv4flash-db-first-full-01/dacomp-055/attempt-01/python/P11.py)；[输出](../../../runs/dsv4flash-db-first-full-01/dacomp-055/attempt-01/python/P11.stdout)；[错误](../../../runs/dsv4flash-db-first-full-01/dacomp-055/attempt-01/python/P11.stderr)。检出需人工核验的 SQL 可实现操作：groupby(；不能仅凭理由判为合规。

P12：Completing the bias analysis after fixing the qcut issue (IPS has many tied values, so I use a rounded IPS-bucket grouping instead), plus regression-based attribution and additional visualizations.

[源码](../../../runs/dsv4flash-db-first-full-01/dacomp-055/attempt-01/python/P12.py)；[输出](../../../runs/dsv4flash-db-first-full-01/dacomp-055/attempt-01/python/P12.stdout)；[错误](../../../runs/dsv4flash-db-first-full-01/dacomp-055/attempt-01/python/P12.stderr)。检出需人工核验的 SQL 可实现操作：groupby(；不能仅凭理由判为合规。

P13：sklearn is unavailable; performing a manual OLS multiple regression with numpy to attribute ROI drivers, and generating the remaining visualization figures.

[源码](../../../runs/dsv4flash-db-first-full-01/dacomp-055/attempt-01/python/P13.py)；[输出](../../../runs/dsv4flash-db-first-full-01/dacomp-055/attempt-01/python/P13.stdout)；[错误](../../../runs/dsv4flash-db-first-full-01/dacomp-055/attempt-01/python/P13.stderr)。检出需人工核验的 SQL 可实现操作：groupby(；不能仅凭理由判为合规。

P14：Fixing the ips_bucket groupby syntax and generating the remaining figures (IPS vs ROI bar, cohort ROI by DM boxplot, acquisition cost comparison).

[源码](../../../runs/dsv4flash-db-first-full-01/dacomp-055/attempt-01/python/P14.py)；[输出](../../../runs/dsv4flash-db-first-full-01/dacomp-055/attempt-01/python/P14.stdout)；[错误](../../../runs/dsv4flash-db-first-full-01/dacomp-055/attempt-01/python/P14.stderr)。检出需人工核验的 SQL 可实现操作：groupby(；不能仅凭理由判为合规。

P15：Fixing boxplot API compatibility and completing the remaining visualizations and statistical summaries.

[源码](../../../runs/dsv4flash-db-first-full-01/dacomp-055/attempt-01/python/P15.py)；[输出](../../../runs/dsv4flash-db-first-full-01/dacomp-055/attempt-01/python/P15.stdout)；[错误](../../../runs/dsv4flash-db-first-full-01/dacomp-055/attempt-01/python/P15.stderr)。检出需人工核验的 SQL 可实现操作：groupby(, sort_values(；不能仅凭理由判为合规。

P16：Computing the final systemic bias summary: comparing investment priority score allocation vs actual value contribution per segment to quantify investment model misalignment.

[源码](../../../runs/dsv4flash-db-first-full-01/dacomp-055/attempt-01/python/P16.py)；[输出](../../../runs/dsv4flash-db-first-full-01/dacomp-055/attempt-01/python/P16.stdout)；[错误](../../../runs/dsv4flash-db-first-full-01/dacomp-055/attempt-01/python/P16.stderr)。自动源码筛查未检出预设迁出信号；这不是全面语义合规证明。

P17：Completing the final statistical summary on IPS/health confound and ROI drivers (Pearson/Spearman correlations need scipy, outside SQL).

[源码](../../../runs/dsv4flash-db-first-full-01/dacomp-055/attempt-01/python/P17.py)；[输出](../../../runs/dsv4flash-db-first-full-01/dacomp-055/attempt-01/python/P17.stdout)；[错误](../../../runs/dsv4flash-db-first-full-01/dacomp-055/attempt-01/python/P17.stderr)。自动源码筛查未检出预设迁出信号；这不是全面语义合规证明。

## 优化机会

已验证候选。筛选限于精确 SQL、相同自包含 CTE、相同单表完整过滤、可分解单表聚合；未覆盖任意 Join 等价和一般谓词蕴含。全部候选都是 offline，未测在线预测。

| 候选 | 类型 | 已有结果 | 覆盖 SQL | 后续次数 | 中间行数 | 验证 | 成本 |
| --- | --- | --- | --- | --- | --- | --- | --- |
| C1 | exact-result reuse | True | ["S64", "S68"] | 1 | unknown | not_verified_cap | Not tested |
| C2 | exact-result reuse | True | ["S65", "S69"] | 1 | unknown | not_verified_cap | Not tested |
| C3 | exact-result reuse | True | ["S66", "S70"] | 1 | unknown | not_verified_cap | Not tested |
| C4 | common subexpression | False | ["S47", "S72"] | 1 | 4847 | verified | Not benchmarked; correctness alone does not establish net speedup. |
| C5 | common subexpression | False | ["S49", "S50", "S51", "S52", "S53", "S54", "S55", "S56"] | 7 | 4855 | verified | Warm-cache baseline 1410.589 ms vs build+reuse 420.655 ms, ratio 3.353; five repetitions, see performance evidence. |
| C6 | aggregate MV | False | ["S3", "S11", "S34"] | 2 | 282 | rejected_result_mismatch | Not benchmarked; correctness alone does not establish net speedup. |
| C7 | common filtered view | False | ["S35", "S37"] | 1 | unknown | not_verified_cap | Not tested |


已验证覆盖（含触发查询、候选并集去重）：10/60 条成功数据 SQL。正确性仅针对当前数据库快照；未测性能的候选不能声称已加速。

[完整 build/rewrite 与比较证据](dacomp-055.analysis.json)。

### C5：common subexpression

Identical self-contained CTE body across queries.

原查询 [S49](#s49), [S50](#s50), [S51](#s51), [S52](#s52), [S53](#s53), [S54](#s54), [S55](#s55), [S56](#s56) → 新增共享状态 C5 → 后续 7 次可复用。该构建点为事后假设，不代表 Agent 当时预知后续。

构建定义：

```sql
SELECT DISTINCT v.primary_email, v.investment_priority_score, v.product_adoption_rate, v.support_resolution_efficiency, v.acquisition_cost, v.customer_lifetime_value, v.lifecycle_stage, v.industry_vertical, v.company_size_tier, v.customer_onboarding_score, v.team_size, v.decision_maker_level, v.digital_engagement_score, v.nps_score, v.customer_health_score, v.churn_probability, c_sales.total_sales_amount FROM (SELECT DISTINCT * FROM customer360__customer_value_analysis) AS v LEFT JOIN (SELECT email, MAX(total_sales_amount) AS total_sales_amount FROM customer360__customer WHERE NOT total_sales_amount IS NULL GROUP BY email) AS c_sales ON v.primary_email = c_sales.email WHERE NOT v.primary_email IS NULL
```

受益查询 S49 的改写示例：

```sql
WITH base AS (SELECT * FROM temp.reuse_candidate), scaled AS (SELECT *, (total_sales_amount - (SELECT MIN(total_sales_amount) FROM base)) / NULLIF((SELECT MAX(total_sales_amount) - MIN(total_sales_amount) FROM base), 0) AS nsales, (product_adoption_rate - (SELECT MIN(product_adoption_rate) FROM base)) / NULLIF((SELECT MAX(product_adoption_rate) - MIN(product_adoption_rate) FROM base), 0) AS nadopt, (support_resolution_efficiency - (SELECT MIN(support_resolution_efficiency) FROM base)) / NULLIF((SELECT MAX(support_resolution_efficiency) - MIN(support_resolution_efficiency) FROM base), 0) AS nres FROM base WHERE NOT product_adoption_rate IS NULL AND NOT support_resolution_efficiency IS NULL AND NOT total_sales_amount IS NULL AND NOT acquisition_cost IS NULL AND NOT customer_lifetime_value IS NULL), with_comp AS (SELECT *, 0.4 * nsales + 0.35 * nadopt + 0.25 * nres AS composite_score FROM scaled), ranked AS (SELECT *, ROW_NUMBER() OVER (ORDER BY investment_priority_score ASC) AS rn_ips_asc, ROW_NUMBER() OVER (ORDER BY composite_score ASC) AS rn_comp_asc, COUNT(*) OVER () AS total_cnt FROM with_comp), cohort AS (SELECT * FROM ranked WHERE rn_ips_asc >= 0.7 * total_cnt AND rn_comp_asc <= 0.5 * total_cnt) SELECT COUNT(*) AS cohort_size, AVG(investment_priority_score) AS avg_ips, AVG(composite_score) AS avg_composite, AVG(total_sales_amount) AS avg_sales, AVG(product_adoption_rate) AS avg_par, AVG(support_resolution_efficiency) AS avg_sre, AVG(customer_lifetime_value / NULLIF(acquisition_cost, 0)) AS avg_roi FROM cohort
```

| 原 SQL | 列名一致 | 结果一致 | 比较方法 |
| --- | --- | --- | --- |
| S49 | True | True | exact_multiset |
| S50 | True | True | ordered_numeric_tolerance |
| S51 | True | True | ordered_numeric_tolerance |
| S52 | True | True | ordered_numeric_tolerance |
| S53 | True | True | ordered_numeric_tolerance |
| S54 | True | True | ordered_numeric_tolerance |
| S55 | True | True | ordered_numeric_tolerance |
| S56 | True | True | exact_multiset |


验证状态：verified；成本结论：Warm-cache baseline 1410.589 ms vs build+reuse 420.655 ms, ratio 3.353; five repetitions, see performance evidence.

### C4：common subexpression

Identical self-contained CTE body across queries.

原查询 [S47](#s47), [S72](#s72) → 新增共享状态 C4 → 后续 1 次可复用。该构建点为事后假设，不代表 Agent 当时预知后续。

构建定义：

```sql
SELECT DISTINCT v.primary_email, v.investment_priority_score, v.product_adoption_rate, v.support_resolution_efficiency, v.acquisition_cost, v.customer_lifetime_value, v.lifecycle_stage, v.industry_vertical, v.company_size_tier, v.customer_onboarding_score, v.team_size, v.decision_maker_level, c_sales.total_sales_amount FROM (SELECT DISTINCT * FROM customer360__customer_value_analysis) AS v LEFT JOIN (SELECT email, MAX(total_sales_amount) AS total_sales_amount FROM customer360__customer WHERE NOT total_sales_amount IS NULL GROUP BY email) AS c_sales ON v.primary_email = c_sales.email WHERE NOT v.primary_email IS NULL
```

受益查询 S47 的改写示例（截取前 1600 字符，完整版本见证据 JSON）：

```sql
WITH base AS (SELECT * FROM temp.reuse_candidate), scaled AS (SELECT *, (total_sales_amount - (SELECT MIN(total_sales_amount) FROM base)) / NULLIF((SELECT MAX(total_sales_amount) - MIN(total_sales_amount) FROM base), 0) AS nsales, (product_adoption_rate - (SELECT MIN(product_adoption_rate) FROM base)) / NULLIF((SELECT MAX(product_adoption_rate) - MIN(product_adoption_rate) FROM base), 0) AS nadopt, (support_resolution_efficiency - (SELECT MIN(support_resolution_efficiency) FROM base)) / NULLIF((SELECT MAX(support_resolution_efficiency) - MIN(support_resolution_efficiency) FROM base), 0) AS nres FROM base WHERE NOT product_adoption_rate IS NULL AND NOT support_resolution_efficiency IS NULL AND NOT total_sales_amount IS NULL AND NOT acquisition_cost IS NULL AND NOT customer_lifetime_value IS NULL), with_comp AS (SELECT *, 0.4 * nsales + 0.35 * nadopt + 0.25 * nres AS composite_score FROM scaled), ranked AS (SELECT *, ROW_NUMBER() OVER (ORDER BY investment_priority_score ASC) AS rn_ips_asc, ROW_NUMBER() OVER (ORDER BY composite_score ASC) AS rn_comp_asc, COUNT(*) OVER () AS total_cnt FROM with_comp) SELECT COUNT(*) AS total, SUM(CASE WHEN rn_ips_asc >= 0.7 * total_cnt AND rn_comp_asc <= 0.5 * total_cnt THEN 1 ELSE 0 END) AS target_cohort, SUM(CASE WHEN rn_ips_asc >= 0.7 * total_cnt THEN 1 ELSE 0 END) AS top30_ips, SUM(CASE WHEN rn_comp_asc <= 0.5 * total_cnt THEN 1 ELSE 0 END) AS bottom50_comp, AVG(CASE WHEN rn_ips_asc >= 0.7 * total_cnt THEN investment_priority_score END) AS avg_ips_top30, MIN(CASE WHEN rn_ips_asc >= 0.7 * total_cnt THEN investment_priority_score END) AS min_
```

| 原 SQL | 列名一致 | 结果一致 | 比较方法 |
| --- | --- | --- | --- |
| S47 | True | True | exact_multiset |
| S72 | True | True | exact_multiset |


验证状态：verified；成本结论：Not benchmarked; correctness alone does not establish net speedup.

### C6：aggregate MV

Union of grouping keys; decomposable aggregate states; AVG uses SUM and non-NULL COUNT.

原查询 [S3](#s3), [S11](#s11), [S34](#s34) → 新增共享状态 C6 → 后续 2 次可复用。该构建点为事后假设，不代表 Agent 当时预知后续。

构建定义：

```sql
SELECT investment_priority_score AS __g0, COUNT(*) AS __a0, MIN(customer_lifetime_value) AS __a1, MAX(customer_lifetime_value) AS __a2, SUM(customer_lifetime_value) AS __a3_sum, COUNT(customer_lifetime_value) AS __a3_n, MIN(acquisition_cost) AS __a4, MAX(acquisition_cost) AS __a5, SUM(acquisition_cost) AS __a6_sum, COUNT(acquisition_cost) AS __a6_n FROM "customer360__customer_value_analysis"  GROUP BY investment_priority_score
```

受益查询 S3 的改写示例：

```sql
SELECT SUM(__a0) AS total_rows FROM temp.reuse_candidate
```

| 原 SQL | 列名一致 | 结果一致 | 比较方法 |
| --- | --- | --- | --- |
| S3 | True | True | exact_multiset |
| S11 | True | False | exact_multiset |
| S34 | True | True | ordered_numeric_tolerance |


验证状态：rejected_result_mismatch；成本结论：Not benchmarked; correctness alone does not establish net speedup.

[性能证据 C5](dacomp-055.C5.performance.json)：measured。

结果依赖：自动记录 SQL→Python 的接口父调用，以及源码中引用归档文件的消费者；字面值相同不认定因果。模型方向选择需要人工读取消息，尚未做全面因果标注。

[原始报告](../../../runs/dsv4flash-db-first-full-01/dacomp-055/attempt-01/answer.md)；[统一消息](../../../runs/dsv4flash-db-first-full-01/dacomp-055/attempt-01/messages.jsonl)；[原始 OpenCode 事件](../../../runs/dsv4flash-db-first-full-01/dacomp-055/attempt-01/opencode.jsonl)；[SQL 引擎日志](../../../runs/dsv4flash-db-first-full-01/dacomp-055/attempt-01/sql_journal.jsonl)。

[可读报告（本地图片链接规范化）](../answers/dacomp-055.md)。原始回答保留，分析结论未改写。

## S1

类别 `connection_setup`；来源 `connection`；调用 `6cb71740abac437982150265ceec1840`；状态 `success`。

```sql
PRAGMA query_only=ON
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-055/attempt-01/sql/S1.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-055/attempt-01/sql/S1.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-055/attempt-01/results/S1.rows.jsonl)；完整：True；SHA256：`e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`。

## S2

类别 `metadata`；来源 `list_db`；调用 `6cb71740abac437982150265ceec1840`；状态 `success`。

```sql
SELECT name,sql FROM sqlite_master WHERE type='table' ORDER BY name
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-055/attempt-01/sql/S2.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-055/attempt-01/sql/S2.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-055/attempt-01/results/S2.rows.jsonl)；完整：True；SHA256：`bd716f54cfa1dca253831d55926805f8ab3971b9cb213eb26f9094ec6eaeacce`。

## S3

类别 `data`；来源 `query_db`；调用 `297b42b750bf46f38f47211e72035008`；状态 `success`。

```sql
SELECT COUNT(*) AS total_rows FROM customer360__customer_value_analysis
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-055/attempt-01/sql/S3.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-055/attempt-01/sql/S3.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-055/attempt-01/results/S3.rows.jsonl)；完整：True；SHA256：`bdbef1caff7b48e20559d35d963fc16e07bc4b392f104c577c5c0c19de92dd94`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "customer360__customer_value_analysis", "kind": "base", "block": null, "base_tables": ["customer360__customer_value_analysis"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |


## S4

类别 `data`；来源 `query_db`；调用 `dc4fdd14fa7741f791e4fbcdf47a2f96`；状态 `success`。

```sql
SELECT * FROM customer360__customer_value_analysis LIMIT 5
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-055/attempt-01/sql/S4.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-055/attempt-01/sql/S4.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-055/attempt-01/results/S4.rows.jsonl)；完整：True；SHA256：`d53aef25d96ce9b7ee62b4e70db356242c6407c9189e32b7faf3cf92a34ea0ec`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "customer360__customer_value_analysis", "kind": "base", "block": null, "base_tables": ["customer360__customer_value_analysis"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |


## S5

类别 `data`；来源 `query_db`；调用 `6c2da745ed0945409c95c1ea1b19ddab`；状态 `success`。

```sql
SELECT COUNT(DISTINCT marketo_lead_id) AS distinct_leads FROM customer360__customer_value_analysis
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-055/attempt-01/sql/S5.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-055/attempt-01/sql/S5.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-055/attempt-01/results/S5.rows.jsonl)；完整：True；SHA256：`29433440de3cbf6d261739003c6943be8c3f2086c8c7ba6f73f02e13236537d2`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "customer360__customer_value_analysis", "kind": "base", "block": null, "base_tables": ["customer360__customer_value_analysis"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(DISTINCT marketo_lead_id) | [{"table": "customer360__customer_value_analysis", "column": "marketo_lead_id"}] | [] | False |


## S6

类别 `data`；来源 `query_db`；调用 `7931781eb3544193a44e1fdd017b15ba`；状态 `success`。

```sql
SELECT DISTINCT lifecycle_stage FROM customer360__customer_value_analysis ORDER BY lifecycle_stage
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-055/attempt-01/sql/S6.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-055/attempt-01/sql/S6.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-055/attempt-01/results/S6.rows.jsonl)；完整：True；SHA256：`98874ada66948ace887a4a0c46d7db1cd60bc736023ba6521c7e9deb832ad778`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "customer360__customer_value_analysis", "kind": "base", "block": null, "base_tables": ["customer360__customer_value_analysis"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |


## S7

类别 `data`；来源 `query_db`；调用 `ccec1e5086c741cbab5486886f6bbcc1`；状态 `success`。

```sql
SELECT DISTINCT industry_vertical FROM customer360__customer_value_analysis ORDER BY industry_vertical
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-055/attempt-01/sql/S7.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-055/attempt-01/sql/S7.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-055/attempt-01/results/S7.rows.jsonl)；完整：True；SHA256：`f3f860190584103963f5e69ce1bf092f6056ab77c74c1aab4a2dd84923a4b96c`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "customer360__customer_value_analysis", "kind": "base", "block": null, "base_tables": ["customer360__customer_value_analysis"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |


## S8

类别 `data`；来源 `query_db`；调用 `9b571339017f43b4ab68c2a6be3a3324`；状态 `success`。

```sql
SELECT DISTINCT company_size_tier FROM customer360__customer_value_analysis ORDER BY company_size_tier
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-055/attempt-01/sql/S8.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-055/attempt-01/sql/S8.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-055/attempt-01/results/S8.rows.jsonl)；完整：True；SHA256：`18d4fae56f396717f44473cbe34624604868e22fa5ed1d9b1646caa68aad1627`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "customer360__customer_value_analysis", "kind": "base", "block": null, "base_tables": ["customer360__customer_value_analysis"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |


## S9

类别 `data`；来源 `query_db`；调用 `b4f07c099eb842b780dccb48380a5b8a`；状态 `success`。

```sql
SELECT DISTINCT decision_maker_level FROM customer360__customer_value_analysis ORDER BY decision_maker_level
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-055/attempt-01/sql/S9.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-055/attempt-01/sql/S9.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-055/attempt-01/results/S9.rows.jsonl)；完整：True；SHA256：`1e3fa8f4d43fcd44ae67567ec999df161e6f1cc82b724a49e7427a81738717fc`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "customer360__customer_value_analysis", "kind": "base", "block": null, "base_tables": ["customer360__customer_value_analysis"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |


## S10

类别 `data`；来源 `query_db`；调用 `dc355743e7774f579408d99cd8580a7b`；状态 `failed`。

```sql
SELECT 
  MIN(investment_priority_score) AS min_ips,
  MAX(investment_priority_score) AS max_ips,
  AVG(investment_priority_score) AS avg_ips,
  MIN(total_sales_amount) AS min_sales,
  MAX(total_sales_amount) AS max_sales,
  AVG(total_sales_amount) AS avg_sales,
  MIN(product_adoption_rate) AS min_par,
  MAX(product_adoption_rate) AS max_par,
  AVG(product_adoption_rate) AS avg_par,
  MIN(support_resolution_efficiency) AS min_sre,
  MAX(support_resolution_efficiency) AS max_sre,
  AVG(support_resolution_efficiency) AS avg_sre
FROM customer360__customer_value_analysis
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-055/attempt-01/sql/S10.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-055/attempt-01/sql/S10.parameters.json)。

错误：`OperationalError('no such column: total_sales_amount')`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "customer360__customer_value_analysis", "kind": "base", "block": null, "base_tables": ["customer360__customer_value_analysis"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | MIN(investment_priority_score) | [{"table": "customer360__customer_value_analysis", "column": "investment_priority_score"}] | [] | False |
| B1 | MAX(investment_priority_score) | [{"table": "customer360__customer_value_analysis", "column": "investment_priority_score"}] | [] | False |
| B1 | AVG(investment_priority_score) | [{"table": "customer360__customer_value_analysis", "column": "investment_priority_score"}] | [] | False |
| B1 | MIN(total_sales_amount) | [{"unknown": "total_sales_amount"}] | [] | False |
| B1 | MAX(total_sales_amount) | [{"unknown": "total_sales_amount"}] | [] | False |
| B1 | AVG(total_sales_amount) | [{"unknown": "total_sales_amount"}] | [] | False |
| B1 | MIN(product_adoption_rate) | [{"table": "customer360__customer_value_analysis", "column": "product_adoption_rate"}] | [] | False |
| B1 | MAX(product_adoption_rate) | [{"table": "customer360__customer_value_analysis", "column": "product_adoption_rate"}] | [] | False |
| B1 | AVG(product_adoption_rate) | [{"table": "customer360__customer_value_analysis", "column": "product_adoption_rate"}] | [] | False |
| B1 | MIN(support_resolution_efficiency) | [{"table": "customer360__customer_value_analysis", "column": "support_resolution_efficiency"}] | [] | False |
| B1 | MAX(support_resolution_efficiency) | [{"table": "customer360__customer_value_analysis", "column": "support_resolution_efficiency"}] | [] | False |
| B1 | AVG(support_resolution_efficiency) | [{"table": "customer360__customer_value_analysis", "column": "support_resolution_efficiency"}] | [] | False |


未解析列血缘：[{"block": "B1", "column": "total_sales_amount", "reason": "ambiguous_or_missing_source"}, {"block": "B1", "column": "total_sales_amount", "reason": "ambiguous_or_missing_source"}, {"block": "B1", "column": "total_sales_amount", "reason": "ambiguous_or_missing_source"}, {"block": "B1", "column": "total_sales_amount", "reason": "ambiguous_or_missing_source"}, {"block": "B1", "column": "total_sales_amount", "reason": "ambiguous_or_missing_source"}, {"block": "B1", "column": "total_sales_amount", "reason": "ambiguous_or_missing_source"}]

## S11

类别 `data`；来源 `query_db`；调用 `9243eae02692456e988a79a30d261e6c`；状态 `success`。

```sql
SELECT 
  MIN(customer_lifetime_value) AS min_clv,
  MAX(customer_lifetime_value) AS max_clv,
  AVG(customer_lifetime_value) AS avg_clv,
  MIN(acquisition_cost) AS min_ac,
  MAX(acquisition_cost) AS max_ac,
  AVG(acquisition_cost) AS avg_ac
FROM customer360__customer_value_analysis
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-055/attempt-01/sql/S11.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-055/attempt-01/sql/S11.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-055/attempt-01/results/S11.rows.jsonl)；完整：True；SHA256：`0d21e9faad642609ac50b3458ffc12615c829c3e41977a4e3eae7ba830c4436e`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "customer360__customer_value_analysis", "kind": "base", "block": null, "base_tables": ["customer360__customer_value_analysis"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | MIN(customer_lifetime_value) | [{"table": "customer360__customer_value_analysis", "column": "customer_lifetime_value"}] | [] | False |
| B1 | MAX(customer_lifetime_value) | [{"table": "customer360__customer_value_analysis", "column": "customer_lifetime_value"}] | [] | False |
| B1 | AVG(customer_lifetime_value) | [{"table": "customer360__customer_value_analysis", "column": "customer_lifetime_value"}] | [] | False |
| B1 | MIN(acquisition_cost) | [{"table": "customer360__customer_value_analysis", "column": "acquisition_cost"}] | [] | False |
| B1 | MAX(acquisition_cost) | [{"table": "customer360__customer_value_analysis", "column": "acquisition_cost"}] | [] | False |
| B1 | AVG(acquisition_cost) | [{"table": "customer360__customer_value_analysis", "column": "acquisition_cost"}] | [] | False |


## S12

类别 `data`；来源 `query_db`；调用 `9006ccf2e28b4642b9d777e6d16b1f6d`；状态 `success`。

```sql
SELECT COUNT(*) AS cnt, COUNT(DISTINCT customer360_id) AS distinct_ids FROM customer360__customer
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-055/attempt-01/sql/S12.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-055/attempt-01/sql/S12.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-055/attempt-01/results/S12.rows.jsonl)；完整：True；SHA256：`6aa0fe29179f5459bba200715e2663cafb8552705c2deeefc775dfe897ef9c3e`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "customer360__customer", "kind": "base", "block": null, "base_tables": ["customer360__customer"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |
| B1 | COUNT(DISTINCT customer360_id) | [{"table": "customer360__customer", "column": "customer360_id"}] | [] | False |


## S13

类别 `data`；来源 `query_db`；调用 `69be28dbcdc845fdba70ef584746d3a1`；状态 `success`。

```sql
SELECT marketo_lead_id, COUNT(*) AS cnt FROM customer360__customer_value_analysis GROUP BY marketo_lead_id HAVING cnt > 1 LIMIT 10
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-055/attempt-01/sql/S13.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-055/attempt-01/sql/S13.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-055/attempt-01/results/S13.rows.jsonl)；完整：True；SHA256：`f85ecfaec670b2a23667780206e925af8970fe9e61eb5e9f07b5244bc03b7264`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "customer360__customer_value_analysis", "kind": "base", "block": null, "base_tables": ["customer360__customer_value_analysis"]}] | [] | ["marketo_lead_id"] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |


## S14

类别 `data`；来源 `query_db`；调用 `e45e474e8d1d4bfeb05006658fa2d858`；状态 `success`。

```sql
SELECT COUNT(DISTINCT marketo_lead_id) AS distinct_leads, COUNT(*) AS cnt FROM customer360__mapping
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-055/attempt-01/sql/S14.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-055/attempt-01/sql/S14.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-055/attempt-01/results/S14.rows.jsonl)；完整：True；SHA256：`75a51e3a21dbb1c076fe26e1f42f544bd6ebae7aaf390d67185c9b9814a52422`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "customer360__mapping", "kind": "base", "block": null, "base_tables": ["customer360__mapping"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(DISTINCT marketo_lead_id) | [{"table": "customer360__mapping", "column": "marketo_lead_id"}] | [] | False |
| B1 | COUNT(*) | [] | [] | True |


## S15

类别 `data`；来源 `query_db`；调用 `5a59c6e534af4b7a891ecdb56e9390f4`；状态 `success`。

```sql
SELECT * FROM customer360__customer_value_analysis WHERE marketo_lead_id IS NULL LIMIT 5
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-055/attempt-01/sql/S15.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-055/attempt-01/sql/S15.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-055/attempt-01/results/S15.rows.jsonl)；完整：True；SHA256：`d22d32666c868c509807a4dcd7fb917198c5725c3ccb5bb83fbc2c46be851387`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "customer360__customer_value_analysis", "kind": "base", "block": null, "base_tables": ["customer360__customer_value_analysis"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |


## S16

类别 `data`；来源 `query_db`；调用 `9db6fabe393549d386d7e84af1747279`；状态 `success`。

```sql
SELECT marketo_lead_id, COUNT(*) AS cnt, COUNT(DISTINCT stripe_customer_id) AS distinct_stripe, COUNT(DISTINCT zendesk_user_id) AS distinct_zd, COUNT(DISTINCT primary_email) AS distinct_email FROM customer360__customer_value_analysis GROUP BY marketo_lead_id HAVING cnt > 1 ORDER BY cnt DESC LIMIT 10
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-055/attempt-01/sql/S16.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-055/attempt-01/sql/S16.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-055/attempt-01/results/S16.rows.jsonl)；完整：True；SHA256：`68a504cc051d5ea63b3a1f743c5a2040c31d11ec5ed1237c575ca29b73d4b04c`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "customer360__customer_value_analysis", "kind": "base", "block": null, "base_tables": ["customer360__customer_value_analysis"]}] | [] | ["marketo_lead_id"] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |
| B1 | COUNT(DISTINCT stripe_customer_id) | [{"table": "customer360__customer_value_analysis", "column": "stripe_customer_id"}] | [] | False |
| B1 | COUNT(DISTINCT zendesk_user_id) | [{"table": "customer360__customer_value_analysis", "column": "zendesk_user_id"}] | [] | False |
| B1 | COUNT(DISTINCT primary_email) | [{"table": "customer360__customer_value_analysis", "column": "primary_email"}] | [] | False |


## S17

类别 `data`；来源 `query_db`；调用 `396bd61003204c698fd8e5c53ab04f0c`；状态 `success`。

```sql
SELECT marketo_lead_id, COUNT(*) AS cnt, COUNT(DISTINCT customer360_id) AS distinct_c360 FROM customer360__mapping GROUP BY marketo_lead_id HAVING cnt > 1 ORDER BY cnt DESC LIMIT 10
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-055/attempt-01/sql/S17.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-055/attempt-01/sql/S17.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-055/attempt-01/results/S17.rows.jsonl)；完整：True；SHA256：`57cec1dd157e2c5564674617f0e408c563bbb2a0f9c0fcf31b8193cbe06f0ba6`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "customer360__mapping", "kind": "base", "block": null, "base_tables": ["customer360__mapping"]}] | [] | ["marketo_lead_id"] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |
| B1 | COUNT(DISTINCT customer360_id) | [{"table": "customer360__mapping", "column": "customer360_id"}] | [] | False |


## S18

类别 `data`；来源 `query_db`；调用 `7f1237dba8f14adf8c87d0e07d4e40eb`；状态 `success`。

```sql
SELECT COUNT(*) AS total_rows, COUNT(DISTINCT customer360_id) AS distinct_c360, COUNT(DISTINCT marketo_lead_id) AS distinct_leads FROM customer360__mapping
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-055/attempt-01/sql/S18.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-055/attempt-01/sql/S18.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-055/attempt-01/results/S18.rows.jsonl)；完整：True；SHA256：`993a8c6ac4a0481cf0473df1765eca9e427f1f5fdeb9907bbaaadc251e053e90`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "customer360__mapping", "kind": "base", "block": null, "base_tables": ["customer360__mapping"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |
| B1 | COUNT(DISTINCT customer360_id) | [{"table": "customer360__mapping", "column": "customer360_id"}] | [] | False |
| B1 | COUNT(DISTINCT marketo_lead_id) | [{"table": "customer360__mapping", "column": "marketo_lead_id"}] | [] | False |


## S19

类别 `data`；来源 `query_db`；调用 `e6566aad423a4ac48bb5cea25a629d47`；状态 `success`。

```sql
SELECT m.marketo_lead_id, COUNT(DISTINCT c.customer360_id) AS distinct_ids, COUNT(*) AS cnt, COUNT(DISTINCT c.total_sales_amount) AS distinct_sales
FROM customer360__customer c
JOIN customer360__mapping m ON c.customer360_id = m.customer360_id
WHERE m.marketo_lead_id = 8915
GROUP BY m.marketo_lead_id
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-055/attempt-01/sql/S19.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-055/attempt-01/sql/S19.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-055/attempt-01/results/S19.rows.jsonl)；完整：True；SHA256：`337f3e846152bb458c3a707b1933053805ccd437de6ecf44366b8bbb9f38982b`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "c", "kind": "base", "block": null, "base_tables": ["customer360__customer"]}, {"alias": "m", "kind": "base", "block": null, "base_tables": ["customer360__mapping"]}] | [{"type": "INNER", "right": "customer360__mapping AS m", "on": "c.customer360_id = m.customer360_id", "using": []}] | ["m.marketo_lead_id"] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(DISTINCT c.customer360_id) | [{"table": "customer360__customer", "column": "customer360_id"}] | [] | False |
| B1 | COUNT(*) | [] | [] | True |
| B1 | COUNT(DISTINCT c.total_sales_amount) | [{"table": "customer360__customer", "column": "total_sales_amount"}] | [] | False |


## S20

类别 `data`；来源 `query_db`；调用 `a6b75d44d3394bcfb3fe79314a02ee25`；状态 `success`。

```sql
SELECT COUNT(*) AS total, COUNT(*) - COUNT(DISTINCT marketo_lead_id || stripe_customer_id || zendesk_user_id || primary_email) AS duplicate_rows FROM customer360__customer_value_analysis
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-055/attempt-01/sql/S20.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-055/attempt-01/sql/S20.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-055/attempt-01/results/S20.rows.jsonl)；完整：True；SHA256：`0e006609f50708bf05c00d36799e6b744e119d1041d734c1ed3239d637206623`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "customer360__customer_value_analysis", "kind": "base", "block": null, "base_tables": ["customer360__customer_value_analysis"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |
| B1 | COUNT(*) | [] | [] | True |
| B1 | COUNT(DISTINCT marketo_lead_id \|\| stripe_customer_id \|\| zendesk_user_id \|\| primary_email) | [{"table": "customer360__customer_value_analysis", "column": "primary_email"}, {"table": "customer360__customer_value_analysis", "column": "zendesk_user_id"}, {"table": "customer360__customer_value_analysis", "column": "marketo_lead_id"}, {"table": "customer360__customer_value_analysis", "column": "stripe_customer_id"}] | [] | False |


## S21

类别 `data`；来源 `query_db`；调用 `bbaf7976b8ba44139d100a56386306f2`；状态 `success`。

```sql
SELECT COUNT(*) AS total_distinct_rows FROM (SELECT DISTINCT * FROM customer360__customer_value_analysis)
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-055/attempt-01/sql/S21.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-055/attempt-01/sql/S21.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-055/attempt-01/results/S21.rows.jsonl)；完整：True；SHA256：`c92c646a86f54fc805ef613d17a77d8a06e83502aa93de1d69453ccc2ebcc073`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "customer360__customer_value_analysis", "kind": "base", "block": null, "base_tables": ["customer360__customer_value_analysis"]}] | [] | [] |
| B2 | [{"alias": "", "kind": "derived", "block": "B1", "base_tables": ["customer360__customer_value_analysis"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B2 | COUNT(*) | [] | [] | True |


## S22

类别 `data`；来源 `query_db`；调用 `0bdcd6c5825b4dcd929b1afd24fd9c1e`；状态 `failed`。

```sql
SELECT marketo_lead_id, stripe_customer_id, zendesk_user_id, primary_email, investment_priority_score, acquisition_cost, customer_lifetime_value, product_adoption_rate, support_resolution_efficiency, total_sales_amount_via_c
FROM (
  SELECT v.marketo_lead_id, v.stripe_customer_id, v.zendesk_user_id, v.primary_email, v.investment_priority_score, v.acquisition_cost, v.customer_lifetime_value, v.product_adoption_rate, v.support_resolution_efficiency
  FROM customer360__customer_value_analysis v
  WHERE v.marketo_lead_id IN (8915, 6947, 8230)
) 
LIMIT 20
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-055/attempt-01/sql/S22.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-055/attempt-01/sql/S22.parameters.json)。

错误：`OperationalError('no such column: total_sales_amount_via_c')`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "v", "kind": "base", "block": null, "base_tables": ["customer360__customer_value_analysis"]}] | [] | [] |
| B2 | [{"alias": "", "kind": "derived", "block": "B1", "base_tables": ["customer360__customer_value_analysis"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |


未解析列血缘：[{"block": "B2", "column": "total_sales_amount_via_c", "reason": "ambiguous_or_missing_source"}]

## S23

类别 `data`；来源 `query_db`；调用 `8c6d7ab980684170b0beda76c46496ef`；状态 `success`。

```sql
SELECT marketo_lead_id, stripe_customer_id, zendesk_user_id, primary_email, investment_priority_score, acquisition_cost, customer_lifetime_value, product_adoption_rate, support_resolution_efficiency
FROM customer360__customer_value_analysis
WHERE marketo_lead_id = 8915
LIMIT 10
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-055/attempt-01/sql/S23.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-055/attempt-01/sql/S23.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-055/attempt-01/results/S23.rows.jsonl)；完整：True；SHA256：`d27ca193c8b34ceb816723bcfe20548b517c41eda0fb43da6d56bf3ce1ff737c`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "customer360__customer_value_analysis", "kind": "base", "block": null, "base_tables": ["customer360__customer_value_analysis"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |


## S24

类别 `data`；来源 `query_db`；调用 `a77eab13e2bb45cc9dec8b08e0e0191a`；状态 `success`。

```sql
SELECT marketo_lead_id, stripe_customer_id, zendesk_user_id, primary_email, investment_priority_score, acquisition_cost, customer_lifetime_value, product_adoption_rate, support_resolution_efficiency
FROM customer360__customer_value_analysis
WHERE marketo_lead_id = 265
LIMIT 15
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-055/attempt-01/sql/S24.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-055/attempt-01/sql/S24.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-055/attempt-01/results/S24.rows.jsonl)；完整：True；SHA256：`7b9830b0190e75074a4ff86aae5af53080831d75ac1429dc8ce41e9c51232b6c`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "customer360__customer_value_analysis", "kind": "base", "block": null, "base_tables": ["customer360__customer_value_analysis"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |


## S25

类别 `data`；来源 `query_db`；调用 `671b82909e04401e8bea2fcae1a4f24d`；状态 `success`。

```sql
SELECT COUNT(*) AS matched_count
FROM customer360__customer_value_analysis v
JOIN customer360__customer c ON v.primary_email = c.email
LIMIT 10
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-055/attempt-01/sql/S25.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-055/attempt-01/sql/S25.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-055/attempt-01/results/S25.rows.jsonl)；完整：True；SHA256：`8eba6436beb10ad15e41fa7673fcd9c0313ce976f36704c5253d6ddb22b82e01`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "v", "kind": "base", "block": null, "base_tables": ["customer360__customer_value_analysis"]}, {"alias": "c", "kind": "base", "block": null, "base_tables": ["customer360__customer"]}] | [{"type": "INNER", "right": "customer360__customer AS c", "on": "v.primary_email = c.email", "using": []}] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |


## S26

类别 `data`；来源 `query_db`；调用 `a65f8cbe14c140d49ba6394bf0a36dcc`；状态 `success`。

```sql
SELECT v.primary_email, c.email, c.total_sales_amount
FROM customer360__customer_value_analysis v
JOIN customer360__customer c ON v.primary_email = c.email
WHERE v.marketo_lead_id = 8915
LIMIT 10
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-055/attempt-01/sql/S26.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-055/attempt-01/sql/S26.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-055/attempt-01/results/S26.rows.jsonl)；完整：True；SHA256：`9314614f1ca29c8100b99108ff0526eae3731ce619ccdb648fd88e7fa5308c12`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "v", "kind": "base", "block": null, "base_tables": ["customer360__customer_value_analysis"]}, {"alias": "c", "kind": "base", "block": null, "base_tables": ["customer360__customer"]}] | [{"type": "INNER", "right": "customer360__customer AS c", "on": "v.primary_email = c.email", "using": []}] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |


## S27

类别 `data`；来源 `query_db`；调用 `5a4c2db8bbd04f43b4c794b2afc429a7`；状态 `success`。

```sql
SELECT COUNT(*) AS distinct_emails, COUNT(DISTINCT email) AS unique_emails FROM customer360__customer
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-055/attempt-01/sql/S27.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-055/attempt-01/sql/S27.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-055/attempt-01/results/S27.rows.jsonl)；完整：True；SHA256：`c97f471291806351840d7416b25144ab587d68f9f763bf98e09de1dc92e82737`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "customer360__customer", "kind": "base", "block": null, "base_tables": ["customer360__customer"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |
| B1 | COUNT(DISTINCT email) | [{"table": "customer360__customer", "column": "email"}] | [] | False |


## S28

类别 `data`；来源 `query_db`；调用 `42599a8602ba4e5889e067c23d60003d`；状态 `success`。

```sql
SELECT email, COUNT(*) AS cnt, COUNT(DISTINCT total_sales_amount) AS distinct_sales, MAX(total_sales_amount) AS max_sales, MIN(total_sales_amount) AS min_sales
FROM customer360__customer
WHERE email = 'muriel.davis@gmail.com'
GROUP BY email
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-055/attempt-01/sql/S28.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-055/attempt-01/sql/S28.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-055/attempt-01/results/S28.rows.jsonl)；完整：True；SHA256：`6586412c7edaa741a418c5baff3a691d85bb2ba98c39ebdd53983f58d0b43760`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "customer360__customer", "kind": "base", "block": null, "base_tables": ["customer360__customer"]}] | [] | ["email"] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |
| B1 | COUNT(DISTINCT total_sales_amount) | [{"table": "customer360__customer", "column": "total_sales_amount"}] | [] | False |
| B1 | MAX(total_sales_amount) | [{"table": "customer360__customer", "column": "total_sales_amount"}] | [] | False |
| B1 | MIN(total_sales_amount) | [{"table": "customer360__customer", "column": "total_sales_amount"}] | [] | False |


## S29

类别 `data`；来源 `query_db`；调用 `378a869965964e8cbc8c3b9aaf8522c2`；状态 `success`。

```sql
SELECT COUNT(*) AS total, COUNT(DISTINCT marketo_lead_id || '|' || stripe_customer_id || '|' || zendesk_user_id) AS distinct_key_triple,
COUNT(DISTINCT stripe_customer_id) AS distinct_stripe,
COUNT(DISTINCT primary_email) AS distinct_email
FROM customer360__customer_value_analysis
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-055/attempt-01/sql/S29.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-055/attempt-01/sql/S29.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-055/attempt-01/results/S29.rows.jsonl)；完整：True；SHA256：`53b64100a8f64de4b228a7730d06fb73daba8e2a5aac22718a83d49a15e0dea8`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "customer360__customer_value_analysis", "kind": "base", "block": null, "base_tables": ["customer360__customer_value_analysis"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |
| B1 | COUNT(DISTINCT marketo_lead_id \|\| '\|' \|\| stripe_customer_id \|\| '\|' \|\| zendesk_user_id) | [{"table": "customer360__customer_value_analysis", "column": "zendesk_user_id"}, {"table": "customer360__customer_value_analysis", "column": "stripe_customer_id"}, {"table": "customer360__customer_value_analysis", "column": "marketo_lead_id"}] | [] | False |
| B1 | COUNT(DISTINCT stripe_customer_id) | [{"table": "customer360__customer_value_analysis", "column": "stripe_customer_id"}] | [] | False |
| B1 | COUNT(DISTINCT primary_email) | [{"table": "customer360__customer_value_analysis", "column": "primary_email"}] | [] | False |


## S30

类别 `data`；来源 `query_db`；调用 `b47a719b677c47e190f35db6a6cfbf6e`；状态 `success`。

```sql
SELECT COUNT(*) AS total_rows, COUNT(DISTINCT email) AS distinct_emails, COUNT(DISTINCT customer360_id) AS distinct_ids, COUNT(DISTINCT customer360_organization_id) AS distinct_orgs FROM customer360__customer
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-055/attempt-01/sql/S30.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-055/attempt-01/sql/S30.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-055/attempt-01/results/S30.rows.jsonl)；完整：True；SHA256：`e01955d7955bc3f1dffae081f02eb4951bb33e1de187d2c605f3df5f851b8968`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "customer360__customer", "kind": "base", "block": null, "base_tables": ["customer360__customer"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |
| B1 | COUNT(DISTINCT email) | [{"table": "customer360__customer", "column": "email"}] | [] | False |
| B1 | COUNT(DISTINCT customer360_id) | [{"table": "customer360__customer", "column": "customer360_id"}] | [] | False |
| B1 | COUNT(DISTINCT customer360_organization_id) | [{"table": "customer360__customer", "column": "customer360_organization_id"}] | [] | False |


## S31

类别 `data`；来源 `query_db`；调用 `1104342dc9c4406a8bceb7191348bc84`；状态 `success`。

```sql
SELECT COUNT(*) AS distinct_rows FROM (SELECT DISTINCT * FROM customer360__customer_value_analysis)
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-055/attempt-01/sql/S31.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-055/attempt-01/sql/S31.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-055/attempt-01/results/S31.rows.jsonl)；完整：True；SHA256：`c92c646a86f54fc805ef613d17a77d8a06e83502aa93de1d69453ccc2ebcc073`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "customer360__customer_value_analysis", "kind": "base", "block": null, "base_tables": ["customer360__customer_value_analysis"]}] | [] | [] |
| B2 | [{"alias": "", "kind": "derived", "block": "B1", "base_tables": ["customer360__customer_value_analysis"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B2 | COUNT(*) | [] | [] | True |


## S32

类别 `data`；来源 `query_db`；调用 `28f9edac20664f8ba40f00102a778eab`；状态 `success`。

```sql
SELECT COUNT(*) AS email_match_count 
FROM (SELECT DISTINCT primary_email FROM customer360__customer_value_analysis) v
JOIN (SELECT DISTINCT email FROM customer360__customer) c ON v.primary_email = c.email
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-055/attempt-01/sql/S32.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-055/attempt-01/sql/S32.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-055/attempt-01/results/S32.rows.jsonl)；完整：True；SHA256：`361e90846ad23bd410a54f7ec8d2d4a212fd3b2c96a531d219a4fa54a6ac75ae`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "customer360__customer_value_analysis", "kind": "base", "block": null, "base_tables": ["customer360__customer_value_analysis"]}] | [] | [] |
| B2 | [{"alias": "customer360__customer", "kind": "base", "block": null, "base_tables": ["customer360__customer"]}] | [] | [] |
| B3 | [{"alias": "v", "kind": "derived", "block": "B1", "base_tables": ["customer360__customer_value_analysis"]}, {"alias": "c", "kind": "derived", "block": "B2", "base_tables": ["customer360__customer"]}] | [{"type": "INNER", "right": "(SELECT DISTINCT email FROM customer360__customer) AS c", "on": "v.primary_email = c.email", "using": []}] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B3 | COUNT(*) | [] | [] | True |


## S33

类别 `data`；来源 `query_db`；调用 `210d6b2a63874cd68d70eaf95b3579a0`；状态 `failed`。

```sql
SELECT 
  PERCENTILE_CONT(0.3) WITHIN GROUP (ORDER BY investment_priority_score) AS top30_threshold,
  PERCENTILE_CONT(0.5) WITHIN GROUP (ORDER BY investment_priority_score) AS median_ips
FROM customer360__customer_value_analysis
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-055/attempt-01/sql/S33.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-055/attempt-01/sql/S33.parameters.json)。

错误：`OperationalError('near "(": syntax error')`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "customer360__customer_value_analysis", "kind": "base", "block": null, "base_tables": ["customer360__customer_value_analysis"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | PERCENTILE_CONT(0.3) | [] | [] | False |
| B1 | PERCENTILE_CONT(0.5) | [] | [] | False |


## S34

类别 `data`；来源 `query_db`；调用 `7357f7f70548442eb412d20636f9d488`；状态 `success`。

```sql
SELECT 
  investment_priority_score,
  COUNT(*) AS cnt
FROM customer360__customer_value_analysis
GROUP BY investment_priority_score
ORDER BY investment_priority_score
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-055/attempt-01/sql/S34.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-055/attempt-01/sql/S34.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-055/attempt-01/results/S34.rows.jsonl)；完整：True；SHA256：`a77c2ff2ba2b4d85f97e86b9ac2749a2cf7b55d8bb490c5b528f7d9439c5c3d9`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "customer360__customer_value_analysis", "kind": "base", "block": null, "base_tables": ["customer360__customer_value_analysis"]}] | [] | ["investment_priority_score"] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |


## S35

类别 `data`；来源 `query_db`；调用 `dfb97dfe266a49a9a04f2f19e4a9aeef`；状态 `success`。

```sql
SELECT stripe_customer_id, COUNT(*) AS cnt FROM customer360__mapping WHERE stripe_customer_id IS NOT NULL GROUP BY stripe_customer_id ORDER BY cnt DESC LIMIT 5
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-055/attempt-01/sql/S35.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-055/attempt-01/sql/S35.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-055/attempt-01/results/S35.rows.jsonl)；完整：True；SHA256：`42cad95091bbd21b5f56ad1941fb18fa691646875b4bfa4cb35faca21fe48378`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "customer360__mapping", "kind": "base", "block": null, "base_tables": ["customer360__mapping"]}] | [] | ["stripe_customer_id"] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |


## S36

类别 `data`；来源 `query_db`；调用 `65ab8b5018ba49f1a2f7e329448143b2`；状态 `success`。

```sql
SELECT zendesk_user_id, COUNT(*) AS cnt FROM customer360__mapping WHERE zendesk_user_id IS NOT NULL GROUP BY zendesk_user_id ORDER BY cnt DESC LIMIT 5
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-055/attempt-01/sql/S36.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-055/attempt-01/sql/S36.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-055/attempt-01/results/S36.rows.jsonl)；完整：True；SHA256：`b690f1e7e184e6075e39e7aae76edddd47f065ee0cbd66ae9ed705dd27a532a4`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "customer360__mapping", "kind": "base", "block": null, "base_tables": ["customer360__mapping"]}] | [] | ["zendesk_user_id"] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |


## S37

类别 `data`；来源 `query_db`；调用 `6852eb5054a1482ea68a8f618df3663a`；状态 `success`。

```sql
SELECT COUNT(DISTINCT stripe_customer_id) AS distinct_stripe_mapping FROM customer360__mapping WHERE stripe_customer_id IS NOT NULL
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-055/attempt-01/sql/S37.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-055/attempt-01/sql/S37.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-055/attempt-01/results/S37.rows.jsonl)；完整：True；SHA256：`47bf4b4bc0112aa1a953f1e63f6a5b1e5754561715af8ca827ee10d8ac1aa9e6`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "customer360__mapping", "kind": "base", "block": null, "base_tables": ["customer360__mapping"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(DISTINCT stripe_customer_id) | [{"table": "customer360__mapping", "column": "stripe_customer_id"}] | [] | False |


## S38

类别 `data`；来源 `query_db`；调用 `6f7429f3d0f7450495e73042b5c6ffd1`；状态 `success`。

```sql
SELECT COUNT(DISTINCT v.stripe_customer_id) AS in_mapping
FROM customer360__customer_value_analysis v
WHERE v.stripe_customer_id IN (SELECT DISTINCT stripe_customer_id FROM customer360__mapping)
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-055/attempt-01/sql/S38.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-055/attempt-01/sql/S38.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-055/attempt-01/results/S38.rows.jsonl)；完整：True；SHA256：`113794881ae09635bb29a22a3da3506658fdca903f346e4ce0fb4302a65868d3`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "customer360__mapping", "kind": "base", "block": null, "base_tables": ["customer360__mapping"]}] | [] | [] |
| B2 | [{"alias": "v", "kind": "base", "block": null, "base_tables": ["customer360__customer_value_analysis"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B2 | COUNT(DISTINCT v.stripe_customer_id) | [{"table": "customer360__customer_value_analysis", "column": "stripe_customer_id"}] | [] | False |


## S39

类别 `data`；来源 `query_db`；调用 `91fa4872e88943838d6a76b5bd5918de`；状态 `success`。

```sql
SELECT COUNT(DISTINCT v.stripe_customer_id) AS total_stripe_in_v
FROM customer360__customer_value_analysis v
WHERE v.stripe_customer_id IS NOT NULL
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-055/attempt-01/sql/S39.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-055/attempt-01/sql/S39.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-055/attempt-01/results/S39.rows.jsonl)；完整：True；SHA256：`113794881ae09635bb29a22a3da3506658fdca903f346e4ce0fb4302a65868d3`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "v", "kind": "base", "block": null, "base_tables": ["customer360__customer_value_analysis"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(DISTINCT v.stripe_customer_id) | [{"table": "customer360__customer_value_analysis", "column": "stripe_customer_id"}] | [] | False |


## S40

类别 `data`；来源 `query_db`；调用 `cc1b8e834df647e3b9699352b71b8189`；状态 `success`。

```sql
SELECT 
  v.primary_email,
  v.investment_priority_score,
  v.product_adoption_rate,
  v.support_resolution_efficiency,
  v.customer_lifetime_value,
  v.acquisition_cost,
  v.lifecycle_stage,
  v.industry_vertical,
  v.company_size_tier,
  v.customer_onboarding_score,
  v.team_size,
  v.decision_maker_level,
  MAX(c.total_sales_amount) AS total_sales_amount
FROM (SELECT DISTINCT * FROM customer360__customer_value_analysis) v
LEFT JOIN customer360__customer c ON v.primary_email = c.email
GROUP BY v.primary_email
HAVING v.primary_email IS NOT NULL
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-055/attempt-01/sql/S40.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-055/attempt-01/sql/S40.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-055/attempt-01/results/S40.rows.jsonl)；完整：True；SHA256：`da2ddf0dec9f9b7927eb16726fe00fccfd92f3b755cb4e4bc5b049fb7784ea06`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "customer360__customer_value_analysis", "kind": "base", "block": null, "base_tables": ["customer360__customer_value_analysis"]}] | [] | [] |
| B2 | [{"alias": "v", "kind": "derived", "block": "B1", "base_tables": ["customer360__customer_value_analysis"]}, {"alias": "c", "kind": "base", "block": null, "base_tables": ["customer360__customer"]}] | [{"type": "LEFT", "right": "customer360__customer AS c", "on": "v.primary_email = c.email", "using": []}] | ["v.primary_email"] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B2 | MAX(c.total_sales_amount) | [{"table": "customer360__customer", "column": "total_sales_amount"}] | [] | False |


## S41

类别 `data`；来源 `query_db`；调用 `c03f90b945c64e8f8b24145ff34d9bed`；状态 `success`。

```sql
SELECT COUNT(*) AS cnt
FROM (SELECT DISTINCT v.primary_email, v.investment_priority_score, v.product_adoption_rate, 
       v.support_resolution_efficiency, v.customer_lifetime_value, v.acquisition_cost,
       v.lifecycle_stage, v.industry_vertical, v.company_size_tier, 
       v.customer_onboarding_score, v.team_size, v.decision_maker_level
      FROM customer360__customer_value_analysis v
      WHERE v.primary_email IS NOT NULL) v
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-055/attempt-01/sql/S41.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-055/attempt-01/sql/S41.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-055/attempt-01/results/S41.rows.jsonl)；完整：True；SHA256：`71cb799ffc3a5580b75a5197e6f6685057d6f7b54f6b46fae3c09887eb8d6777`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "v", "kind": "base", "block": null, "base_tables": ["customer360__customer_value_analysis"]}] | [] | [] |
| B2 | [{"alias": "v", "kind": "derived", "block": "B1", "base_tables": ["customer360__customer_value_analysis"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B2 | COUNT(*) | [] | [] | True |


## S42

类别 `data`；来源 `query_db`；调用 `5c63939fce894ec6b4fab5f6e30a04c8`；状态 `success`。

```sql
SELECT 
  COUNT(*) AS total,
  SUM(CASE WHEN v.investment_priority_score IS NULL THEN 1 ELSE 0 END) AS null_ips,
  SUM(CASE WHEN v.product_adoption_rate IS NULL THEN 1 ELSE 0 END) AS null_par,
  SUM(CASE WHEN v.support_resolution_efficiency IS NULL THEN 1 ELSE 0 END) AS null_sre,
  SUM(CASE WHEN v.total_sales_amount IS NULL THEN 1 ELSE 0 END) AS null_sales,
  SUM(CASE WHEN v.acquisition_cost IS NULL THEN 1 ELSE 0 END) AS null_ac,
  SUM(CASE WHEN v.customer_lifetime_value IS NULL THEN 1 ELSE 0 END) AS null_clv
FROM (
  SELECT DISTINCT v.*, c_sales.total_sales_amount
  FROM customer360__customer_value_analysis v
  LEFT JOIN (
    SELECT email, MAX(total_sales_amount) AS total_sales_amount
    FROM customer360__customer
    WHERE total_sales_amount IS NOT NULL
    GROUP BY email
  ) c_sales ON v.primary_email = c_sales.email
) v
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-055/attempt-01/sql/S42.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-055/attempt-01/sql/S42.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-055/attempt-01/results/S42.rows.jsonl)；完整：True；SHA256：`52ce23cada03ee4dd3c4f54fe1537f0e03cf34a7b8bdeddeba5e86eb6d2acc1c`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "customer360__customer", "kind": "base", "block": null, "base_tables": ["customer360__customer"]}] | [] | ["email"] |
| B2 | [{"alias": "v", "kind": "base", "block": null, "base_tables": ["customer360__customer_value_analysis"]}, {"alias": "c_sales", "kind": "derived", "block": "B1", "base_tables": ["customer360__customer"]}] | [{"type": "LEFT", "right": "(SELECT email, MAX(total_sales_amount) AS total_sales_amount FROM customer360__customer WHERE NOT total_sales_amount IS NULL GROUP BY email) AS c_sales", "on": "v.primary_email = c_sales.email", "using": []}] | [] |
| B3 | [{"alias": "v", "kind": "derived", "block": "B2", "base_tables": ["customer360__customer", "customer360__customer_value_analysis"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | MAX(total_sales_amount) | [{"table": "customer360__customer", "column": "total_sales_amount"}] | [] | False |
| B3 | COUNT(*) | [] | [] | True |
| B3 | SUM(CASE WHEN v.investment_priority_score IS NULL THEN 1 ELSE 0 END) | [] | [{"table": "customer360__customer_value_analysis", "column": "investment_priority_score"}] | False |
| B3 | SUM(CASE WHEN v.product_adoption_rate IS NULL THEN 1 ELSE 0 END) | [] | [{"table": "customer360__customer_value_analysis", "column": "product_adoption_rate"}] | False |
| B3 | SUM(CASE WHEN v.support_resolution_efficiency IS NULL THEN 1 ELSE 0 END) | [] | [{"table": "customer360__customer_value_analysis", "column": "support_resolution_efficiency"}] | False |
| B3 | SUM(CASE WHEN v.total_sales_amount IS NULL THEN 1 ELSE 0 END) | [] | [{"table": "customer360__customer", "column": "total_sales_amount"}] | False |
| B3 | SUM(CASE WHEN v.acquisition_cost IS NULL THEN 1 ELSE 0 END) | [] | [{"table": "customer360__customer_value_analysis", "column": "acquisition_cost"}] | False |
| B3 | SUM(CASE WHEN v.customer_lifetime_value IS NULL THEN 1 ELSE 0 END) | [] | [{"table": "customer360__customer_value_analysis", "column": "customer_lifetime_value"}] | False |


## S43

类别 `data`；来源 `query_db`；调用 `5f3cbed300004d4a980883882d9b93a4`；状态 `success`。

```sql
SELECT lifecycle_stage, COUNT(*) AS cnt, 
  SUM(CASE WHEN product_adoption_rate IS NULL THEN 1 ELSE 0 END) AS null_par
FROM (SELECT DISTINCT * FROM customer360__customer_value_analysis)
GROUP BY lifecycle_stage
ORDER BY cnt DESC
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-055/attempt-01/sql/S43.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-055/attempt-01/sql/S43.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-055/attempt-01/results/S43.rows.jsonl)；完整：True；SHA256：`d341d169188f4ce244e4eead3eb0070a6bea2f90b92719705bdbca20976cb313`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "customer360__customer_value_analysis", "kind": "base", "block": null, "base_tables": ["customer360__customer_value_analysis"]}] | [] | [] |
| B2 | [{"alias": "", "kind": "derived", "block": "B1", "base_tables": ["customer360__customer_value_analysis"]}] | [] | ["lifecycle_stage"] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B2 | COUNT(*) | [] | [] | True |
| B2 | SUM(CASE WHEN product_adoption_rate IS NULL THEN 1 ELSE 0 END) | [] | [{"table": "customer360__customer_value_analysis", "column": "product_adoption_rate"}] | False |


## S44

类别 `data`；来源 `query_db`；调用 `4af43b877ee04f59b6cd42507508d241`；状态 `success`。

```sql
-- Build the analytical dataset with distinct rows, joined sales data
SELECT COUNT(*) AS total_rows,
  MIN(investment_priority_score) AS min_ips,
  MAX(investment_priority_score) AS max_ips,
  MIN(product_adoption_rate) AS min_par,
  MAX(product_adoption_rate) AS max_par,
  MIN(support_resolution_efficiency) AS min_sre,
  MAX(support_resolution_efficiency) AS max_sre,
  MIN(total_sales_amount) AS min_sales,
  MAX(total_sales_amount) AS max_sales,
  MIN(acquisition_cost) AS min_ac,
  MAX(acquisition_cost) AS max_ac,
  MIN(customer_lifetime_value) AS min_clv,
  MAX(customer_lifetime_value) AS max_clv
FROM (
  SELECT DISTINCT v.*, c_sales.total_sales_amount
  FROM customer360__customer_value_analysis v
  LEFT JOIN (
    SELECT email, MAX(total_sales_amount) AS total_sales_amount
    FROM customer360__customer
    WHERE total_sales_amount IS NOT NULL
    GROUP BY email
  ) c_sales ON v.primary_email = c_sales.email
) base
WHERE product_adoption_rate IS NOT NULL 
  AND support_resolution_efficiency IS NOT NULL
  AND total_sales_amount IS NOT NULL
  AND acquisition_cost IS NOT NULL
  AND customer_lifetime_value IS NOT NULL
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-055/attempt-01/sql/S44.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-055/attempt-01/sql/S44.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-055/attempt-01/results/S44.rows.jsonl)；完整：True；SHA256：`9789205edc98b9abc90a918d16afed79ab862b04fdc155108ef348cb310660ba`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "customer360__customer", "kind": "base", "block": null, "base_tables": ["customer360__customer"]}] | [] | ["email"] |
| B2 | [{"alias": "v", "kind": "base", "block": null, "base_tables": ["customer360__customer_value_analysis"]}, {"alias": "c_sales", "kind": "derived", "block": "B1", "base_tables": ["customer360__customer"]}] | [{"type": "LEFT", "right": "(SELECT email, MAX(total_sales_amount) AS total_sales_amount FROM customer360__customer WHERE NOT total_sales_amount IS NULL GROUP BY email) AS c_sales", "on": "v.primary_email = c_sales.email", "using": []}] | [] |
| B3 | [{"alias": "base", "kind": "derived", "block": "B2", "base_tables": ["customer360__customer", "customer360__customer_value_analysis"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | MAX(total_sales_amount) | [{"table": "customer360__customer", "column": "total_sales_amount"}] | [] | False |
| B3 | COUNT(*) | [] | [] | True |
| B3 | MIN(investment_priority_score) | [{"table": "customer360__customer_value_analysis", "column": "investment_priority_score"}] | [] | False |
| B3 | MAX(investment_priority_score) | [{"table": "customer360__customer_value_analysis", "column": "investment_priority_score"}] | [] | False |
| B3 | MIN(product_adoption_rate) | [{"table": "customer360__customer_value_analysis", "column": "product_adoption_rate"}] | [] | False |
| B3 | MAX(product_adoption_rate) | [{"table": "customer360__customer_value_analysis", "column": "product_adoption_rate"}] | [] | False |
| B3 | MIN(support_resolution_efficiency) | [{"table": "customer360__customer_value_analysis", "column": "support_resolution_efficiency"}] | [] | False |
| B3 | MAX(support_resolution_efficiency) | [{"table": "customer360__customer_value_analysis", "column": "support_resolution_efficiency"}] | [] | False |
| B3 | MIN(total_sales_amount) | [{"table": "customer360__customer", "column": "total_sales_amount"}] | [] | False |
| B3 | MAX(total_sales_amount) | [{"table": "customer360__customer", "column": "total_sales_amount"}] | [] | False |
| B3 | MIN(acquisition_cost) | [{"table": "customer360__customer_value_analysis", "column": "acquisition_cost"}] | [] | False |
| B3 | MAX(acquisition_cost) | [{"table": "customer360__customer_value_analysis", "column": "acquisition_cost"}] | [] | False |
| B3 | MIN(customer_lifetime_value) | [{"table": "customer360__customer_value_analysis", "column": "customer_lifetime_value"}] | [] | False |
| B3 | MAX(customer_lifetime_value) | [{"table": "customer360__customer_value_analysis", "column": "customer_lifetime_value"}] | [] | False |


## S45

类别 `data`；来源 `query_db`；调用 `c68b0e2e648d416fa2e061217d886f6d`；状态 `success`。

```sql
SELECT 
  MIN(investment_priority_score) AS min_ips, MAX(investment_priority_score) AS max_ips, AVG(investment_priority_score) AS avg_ips
FROM (
  SELECT DISTINCT v.*, c_sales.total_sales_amount
  FROM customer360__customer_value_analysis v
  LEFT JOIN (
    SELECT email, MAX(total_sales_amount) AS total_sales_amount
    FROM customer360__customer
    WHERE total_sales_amount IS NOT NULL
    GROUP BY email
  ) c_sales ON v.primary_email = c_sales.email
) base
WHERE product_adoption_rate IS NOT NULL 
  AND support_resolution_efficiency IS NOT NULL
  AND total_sales_amount IS NOT NULL
  AND acquisition_cost IS NOT NULL
  AND customer_lifetime_value IS NOT NULL
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-055/attempt-01/sql/S45.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-055/attempt-01/sql/S45.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-055/attempt-01/results/S45.rows.jsonl)；完整：True；SHA256：`ce922b9ce279aa39151df306d0c46c1a427b5a5061679d60259069df8ae3e937`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "customer360__customer", "kind": "base", "block": null, "base_tables": ["customer360__customer"]}] | [] | ["email"] |
| B2 | [{"alias": "v", "kind": "base", "block": null, "base_tables": ["customer360__customer_value_analysis"]}, {"alias": "c_sales", "kind": "derived", "block": "B1", "base_tables": ["customer360__customer"]}] | [{"type": "LEFT", "right": "(SELECT email, MAX(total_sales_amount) AS total_sales_amount FROM customer360__customer WHERE NOT total_sales_amount IS NULL GROUP BY email) AS c_sales", "on": "v.primary_email = c_sales.email", "using": []}] | [] |
| B3 | [{"alias": "base", "kind": "derived", "block": "B2", "base_tables": ["customer360__customer", "customer360__customer_value_analysis"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | MAX(total_sales_amount) | [{"table": "customer360__customer", "column": "total_sales_amount"}] | [] | False |
| B3 | MIN(investment_priority_score) | [{"table": "customer360__customer_value_analysis", "column": "investment_priority_score"}] | [] | False |
| B3 | MAX(investment_priority_score) | [{"table": "customer360__customer_value_analysis", "column": "investment_priority_score"}] | [] | False |
| B3 | AVG(investment_priority_score) | [{"table": "customer360__customer_value_analysis", "column": "investment_priority_score"}] | [] | False |


## S46

类别 `data`；来源 `query_db`；调用 `ccc2f4741da144b49c7773b2e1db1a28`；状态 `success`。

```sql
WITH base AS (
  SELECT DISTINCT v.primary_email, v.investment_priority_score, v.product_adoption_rate,
    v.support_resolution_efficiency, v.acquisition_cost, v.customer_lifetime_value,
    v.lifecycle_stage, v.industry_vertical, v.company_size_tier,
    v.customer_onboarding_score, v.team_size, v.decision_maker_level,
    c_sales.total_sales_amount
  FROM customer360__customer_value_analysis v
  LEFT JOIN (
    SELECT email, MAX(total_sales_amount) AS total_sales_amount
    FROM customer360__customer
    WHERE total_sales_amount IS NOT NULL
    GROUP BY email
  ) c_sales ON v.primary_email = c_sales.email
),
scaled AS (
  SELECT *,
    (total_sales_amount - (SELECT MIN(total_sales_amount) FROM base)) / 
      NULLIF((SELECT MAX(total_sales_amount) - MIN(total_sales_amount) FROM base), 0) AS nsales,
    (product_adoption_rate - (SELECT MIN(product_adoption_rate) FROM base)) / 
      NULLIF((SELECT MAX(product_adoption_rate) - MIN(product_adoption_rate) FROM base), 0) AS nadopt,
    (support_resolution_efficiency - (SELECT MIN(support_resolution_efficiency) FROM base)) / 
      NULLIF((SELECT MAX(support_resolution_efficiency) - MIN(support_resolution_efficiency) FROM base), 0) AS nres
  FROM base
  WHERE product_adoption_rate IS NOT NULL AND support_resolution_efficiency IS NOT NULL
    AND total_sales_amount IS NOT NULL AND acquisition_cost IS NOT NULL AND customer_lifetime_value IS NOT NULL
),
with_comp AS (
  SELECT *, 0.4*nsales + 0.35*nadopt + 0.25*nres AS composite_score
  FROM scaled
),
ranked AS (
  SELECT *,
    ROW_NUMBER() OVER (ORDER BY investment_priority_score ASC) AS rn_ips_asc,
    ROW_NUMBER() OVER (ORDER BY composite_score ASC) AS rn_comp_asc,
    COUNT(*) OVER () AS total_cnt
  FROM with_comp
)
SELECT 
  COUNT(*) AS total,
  SUM(CASE WHEN rn_ips_asc >= 0.7*total_cnt AND rn_comp_asc <= 0.5*total_cnt THEN 1 ELSE 0 END) AS target_cohort,
  SUM(CASE WHEN rn_ips_asc >= 0.7*total_cnt THEN 1 ELSE 0 END) AS top30_ips,
  SUM(CASE WHEN rn_comp_asc <= 0.5*total_cnt THEN 1 ELSE 0 END) AS bottom50_comp
FROM ranked
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-055/attempt-01/sql/S46.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-055/attempt-01/sql/S46.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-055/attempt-01/results/S46.rows.jsonl)；完整：True；SHA256：`9c5980345fe287575fb8e806a04372b566cfa323acf6ac0ed49b747a1ef47f48`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "customer360__customer", "kind": "base", "block": null, "base_tables": ["customer360__customer"]}] | [] | ["email"] |
| B2 | [{"alias": "v", "kind": "base", "block": null, "base_tables": ["customer360__customer_value_analysis"]}, {"alias": "c_sales", "kind": "derived", "block": "B1", "base_tables": ["customer360__customer"]}] | [{"type": "LEFT", "right": "(SELECT email, MAX(total_sales_amount) AS total_sales_amount FROM customer360__customer WHERE NOT total_sales_amount IS NULL GROUP BY email) AS c_sales", "on": "v.primary_email = c_sales.email", "using": []}] | [] |
| B3 | [{"alias": "base", "kind": "derived", "block": "B2", "base_tables": ["customer360__customer", "customer360__customer_value_analysis"]}] | [] | [] |
| B4 | [{"alias": "base", "kind": "derived", "block": "B2", "base_tables": ["customer360__customer", "customer360__customer_value_analysis"]}] | [] | [] |
| B5 | [{"alias": "base", "kind": "derived", "block": "B2", "base_tables": ["customer360__customer", "customer360__customer_value_analysis"]}] | [] | [] |
| B6 | [{"alias": "base", "kind": "derived", "block": "B2", "base_tables": ["customer360__customer", "customer360__customer_value_analysis"]}] | [] | [] |
| B7 | [{"alias": "base", "kind": "derived", "block": "B2", "base_tables": ["customer360__customer", "customer360__customer_value_analysis"]}] | [] | [] |
| B8 | [{"alias": "base", "kind": "derived", "block": "B2", "base_tables": ["customer360__customer", "customer360__customer_value_analysis"]}] | [] | [] |
| B9 | [{"alias": "base", "kind": "derived", "block": "B2", "base_tables": ["customer360__customer", "customer360__customer_value_analysis"]}] | [] | [] |
| B10 | [{"alias": "scaled", "kind": "derived", "block": "B9", "base_tables": ["customer360__customer", "customer360__customer_value_analysis"]}] | [] | [] |
| B11 | [{"alias": "with_comp", "kind": "derived", "block": "B10", "base_tables": ["customer360__customer", "customer360__customer_value_analysis"]}] | [] | [] |
| B12 | [{"alias": "ranked", "kind": "derived", "block": "B11", "base_tables": ["customer360__customer", "customer360__customer_value_analysis"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | MAX(total_sales_amount) | [{"table": "customer360__customer", "column": "total_sales_amount"}] | [] | False |
| B3 | MIN(total_sales_amount) | [{"table": "customer360__customer", "column": "total_sales_amount"}] | [] | False |
| B4 | MAX(total_sales_amount) | [{"table": "customer360__customer", "column": "total_sales_amount"}] | [] | False |
| B4 | MIN(total_sales_amount) | [{"table": "customer360__customer", "column": "total_sales_amount"}] | [] | False |
| B5 | MIN(product_adoption_rate) | [{"table": "customer360__customer_value_analysis", "column": "product_adoption_rate"}] | [] | False |
| B6 | MAX(product_adoption_rate) | [{"table": "customer360__customer_value_analysis", "column": "product_adoption_rate"}] | [] | False |
| B6 | MIN(product_adoption_rate) | [{"table": "customer360__customer_value_analysis", "column": "product_adoption_rate"}] | [] | False |
| B7 | MIN(support_resolution_efficiency) | [{"table": "customer360__customer_value_analysis", "column": "support_resolution_efficiency"}] | [] | False |
| B8 | MAX(support_resolution_efficiency) | [{"table": "customer360__customer_value_analysis", "column": "support_resolution_efficiency"}] | [] | False |
| B8 | MIN(support_resolution_efficiency) | [{"table": "customer360__customer_value_analysis", "column": "support_resolution_efficiency"}] | [] | False |
| B12 | COUNT(*) | [] | [] | True |
| B12 | SUM(CASE WHEN rn_ips_asc >= 0.7 * total_cnt AND rn_comp_asc <= 0.5 * total_cnt THEN 1 ELSE 0 END) | [] | [{"table": "customer360__customer_value_analysis", "column": "investment_priority_score"}, {"table": "customer360__customer_value_analysis", "column": "support_resolution_efficiency"}, {"table": "customer360__customer_value_analysis", "column": "support_resolution_efficiency"}, {"table": "customer360__customer_value_analysis", "column": "support_resolution_efficiency"}, {"table": "customer360__customer_value_analysis", "column": "support_resolution_efficiency"}, {"table": "customer360__customer", "column": "total_sales_amount"}, {"table": "customer360__customer", "column": "total_sales_amount"}, {"table": "customer360__customer", "column": "total_sales_amount"}, {"table": "customer360__customer", "column": "total_sales_amount"}, {"table": "customer360__customer_value_analysis", "column": "product_adoption_rate"}, {"table": "customer360__customer_value_analysis", "column": "product_adoption_rate"}, {"table": "customer360__customer_value_analysis", "column": "product_adoption_rate"}, {"table": "customer360__customer_value_analysis", "column": "product_adoption_rate"}] | False |
| B12 | SUM(CASE WHEN rn_ips_asc >= 0.7 * total_cnt THEN 1 ELSE 0 END) | [] | [{"table": "customer360__customer_value_analysis", "column": "investment_priority_score"}] | False |
| B12 | SUM(CASE WHEN rn_comp_asc <= 0.5 * total_cnt THEN 1 ELSE 0 END) | [] | [{"table": "customer360__customer_value_analysis", "column": "support_resolution_efficiency"}, {"table": "customer360__customer_value_analysis", "column": "support_resolution_efficiency"}, {"table": "customer360__customer_value_analysis", "column": "support_resolution_efficiency"}, {"table": "customer360__customer_value_analysis", "column": "support_resolution_efficiency"}, {"table": "customer360__customer", "column": "total_sales_amount"}, {"table": "customer360__customer", "column": "total_sales_amount"}, {"table": "customer360__customer", "column": "total_sales_amount"}, {"table": "customer360__customer", "column": "total_sales_amount"}, {"table": "customer360__customer_value_analysis", "column": "product_adoption_rate"}, {"table": "customer360__customer_value_analysis", "column": "product_adoption_rate"}, {"table": "customer360__customer_value_analysis", "column": "product_adoption_rate"}, {"table": "customer360__customer_value_analysis", "column": "product_adoption_rate"}] | False |


## S47

类别 `data`；来源 `query_db`；调用 `31d771ada56c4a60a809ff65a340c924`；状态 `success`。

```sql
WITH base AS (
  SELECT DISTINCT v.primary_email, v.investment_priority_score, v.product_adoption_rate,
    v.support_resolution_efficiency, v.acquisition_cost, v.customer_lifetime_value,
    v.lifecycle_stage, v.industry_vertical, v.company_size_tier,
    v.customer_onboarding_score, v.team_size, v.decision_maker_level,
    c_sales.total_sales_amount
  FROM (
    SELECT DISTINCT * FROM customer360__customer_value_analysis
  ) v
  LEFT JOIN (
    SELECT email, MAX(total_sales_amount) AS total_sales_amount
    FROM customer360__customer
    WHERE total_sales_amount IS NOT NULL
    GROUP BY email
  ) c_sales ON v.primary_email = c_sales.email
  WHERE v.primary_email IS NOT NULL
),
scaled AS (
  SELECT *,
    (total_sales_amount - (SELECT MIN(total_sales_amount) FROM base)) / 
      NULLIF((SELECT MAX(total_sales_amount) - MIN(total_sales_amount) FROM base), 0) AS nsales,
    (product_adoption_rate - (SELECT MIN(product_adoption_rate) FROM base)) / 
      NULLIF((SELECT MAX(product_adoption_rate) - MIN(product_adoption_rate) FROM base), 0) AS nadopt,
    (support_resolution_efficiency - (SELECT MIN(support_resolution_efficiency) FROM base)) / 
      NULLIF((SELECT MAX(support_resolution_efficiency) - MIN(support_resolution_efficiency) FROM base), 0) AS nres
  FROM base
  WHERE product_adoption_rate IS NOT NULL AND support_resolution_efficiency IS NOT NULL
    AND total_sales_amount IS NOT NULL AND acquisition_cost IS NOT NULL AND customer_lifetime_value IS NOT NULL
),
with_comp AS (
  SELECT *, 0.4*nsales + 0.35*nadopt + 0.25*nres AS composite_score
  FROM scaled
),
ranked AS (
  SELECT *,
    ROW_NUMBER() OVER (ORDER BY investment_priority_score ASC) AS rn_ips_asc,
    ROW_NUMBER() OVER (ORDER BY composite_score ASC) AS rn_comp_asc,
    COUNT(*) OVER () AS total_cnt
  FROM with_comp
)
SELECT 
  COUNT(*) AS total,
  SUM(CASE WHEN rn_ips_asc >= 0.7*total_cnt AND rn_comp_asc <= 0.5*total_cnt THEN 1 ELSE 0 END) AS target_cohort,
  SUM(CASE WHEN rn_ips_asc >= 0.7*total_cnt THEN 1 ELSE 0 END) AS top30_ips,
  SUM(CASE WHEN rn_comp_asc <= 0.5*total_cnt THEN 1 ELSE 0 END) AS bottom50_comp,
  AVG(CASE WHEN rn_ips_asc >= 0.7*total_cnt THEN investment_priority_score END) AS avg_ips_top30,
  MIN(CASE WHEN rn_ips_asc >= 0.7*total_cnt THEN investment_priority_score END) AS min_ips_top30
FROM ranked
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-055/attempt-01/sql/S47.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-055/attempt-01/sql/S47.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-055/attempt-01/results/S47.rows.jsonl)；完整：True；SHA256：`3c5db59f4113bd209cd4cce50c25f5564c2bc3c6a96e2a3adb30df97bdcc8088`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "customer360__customer_value_analysis", "kind": "base", "block": null, "base_tables": ["customer360__customer_value_analysis"]}] | [] | [] |
| B2 | [{"alias": "customer360__customer", "kind": "base", "block": null, "base_tables": ["customer360__customer"]}] | [] | ["email"] |
| B3 | [{"alias": "v", "kind": "derived", "block": "B1", "base_tables": ["customer360__customer_value_analysis"]}, {"alias": "c_sales", "kind": "derived", "block": "B2", "base_tables": ["customer360__customer"]}] | [{"type": "LEFT", "right": "(SELECT email, MAX(total_sales_amount) AS total_sales_amount FROM customer360__customer WHERE NOT total_sales_amount IS NULL GROUP BY email) AS c_sales", "on": "v.primary_email = c_sales.email", "using": []}] | [] |
| B4 | [{"alias": "base", "kind": "derived", "block": "B3", "base_tables": ["customer360__customer", "customer360__customer_value_analysis"]}] | [] | [] |
| B5 | [{"alias": "base", "kind": "derived", "block": "B3", "base_tables": ["customer360__customer", "customer360__customer_value_analysis"]}] | [] | [] |
| B6 | [{"alias": "base", "kind": "derived", "block": "B3", "base_tables": ["customer360__customer", "customer360__customer_value_analysis"]}] | [] | [] |
| B7 | [{"alias": "base", "kind": "derived", "block": "B3", "base_tables": ["customer360__customer", "customer360__customer_value_analysis"]}] | [] | [] |
| B8 | [{"alias": "base", "kind": "derived", "block": "B3", "base_tables": ["customer360__customer", "customer360__customer_value_analysis"]}] | [] | [] |
| B9 | [{"alias": "base", "kind": "derived", "block": "B3", "base_tables": ["customer360__customer", "customer360__customer_value_analysis"]}] | [] | [] |
| B10 | [{"alias": "base", "kind": "derived", "block": "B3", "base_tables": ["customer360__customer", "customer360__customer_value_analysis"]}] | [] | [] |
| B11 | [{"alias": "scaled", "kind": "derived", "block": "B10", "base_tables": ["customer360__customer", "customer360__customer_value_analysis"]}] | [] | [] |
| B12 | [{"alias": "with_comp", "kind": "derived", "block": "B11", "base_tables": ["customer360__customer", "customer360__customer_value_analysis"]}] | [] | [] |
| B13 | [{"alias": "ranked", "kind": "derived", "block": "B12", "base_tables": ["customer360__customer", "customer360__customer_value_analysis"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B2 | MAX(total_sales_amount) | [{"table": "customer360__customer", "column": "total_sales_amount"}] | [] | False |
| B4 | MIN(total_sales_amount) | [{"table": "customer360__customer", "column": "total_sales_amount"}] | [] | False |
| B5 | MAX(total_sales_amount) | [{"table": "customer360__customer", "column": "total_sales_amount"}] | [] | False |
| B5 | MIN(total_sales_amount) | [{"table": "customer360__customer", "column": "total_sales_amount"}] | [] | False |
| B6 | MIN(product_adoption_rate) | [{"table": "customer360__customer_value_analysis", "column": "product_adoption_rate"}] | [] | False |
| B7 | MAX(product_adoption_rate) | [{"table": "customer360__customer_value_analysis", "column": "product_adoption_rate"}] | [] | False |
| B7 | MIN(product_adoption_rate) | [{"table": "customer360__customer_value_analysis", "column": "product_adoption_rate"}] | [] | False |
| B8 | MIN(support_resolution_efficiency) | [{"table": "customer360__customer_value_analysis", "column": "support_resolution_efficiency"}] | [] | False |
| B9 | MAX(support_resolution_efficiency) | [{"table": "customer360__customer_value_analysis", "column": "support_resolution_efficiency"}] | [] | False |
| B9 | MIN(support_resolution_efficiency) | [{"table": "customer360__customer_value_analysis", "column": "support_resolution_efficiency"}] | [] | False |
| B13 | COUNT(*) | [] | [] | True |
| B13 | SUM(CASE WHEN rn_ips_asc >= 0.7 * total_cnt AND rn_comp_asc <= 0.5 * total_cnt THEN 1 ELSE 0 END) | [] | [{"table": "customer360__customer_value_analysis", "column": "investment_priority_score"}, {"table": "customer360__customer_value_analysis", "column": "support_resolution_efficiency"}, {"table": "customer360__customer_value_analysis", "column": "support_resolution_efficiency"}, {"table": "customer360__customer_value_analysis", "column": "support_resolution_efficiency"}, {"table": "customer360__customer_value_analysis", "column": "support_resolution_efficiency"}, {"table": "customer360__customer", "column": "total_sales_amount"}, {"table": "customer360__customer", "column": "total_sales_amount"}, {"table": "customer360__customer", "column": "total_sales_amount"}, {"table": "customer360__customer", "column": "total_sales_amount"}, {"table": "customer360__customer_value_analysis", "column": "product_adoption_rate"}, {"table": "customer360__customer_value_analysis", "column": "product_adoption_rate"}, {"table": "customer360__customer_value_analysis", "column": "product_adoption_rate"}, {"table": "customer360__customer_value_analysis", "column": "product_adoption_rate"}] | False |
| B13 | SUM(CASE WHEN rn_ips_asc >= 0.7 * total_cnt THEN 1 ELSE 0 END) | [] | [{"table": "customer360__customer_value_analysis", "column": "investment_priority_score"}] | False |
| B13 | SUM(CASE WHEN rn_comp_asc <= 0.5 * total_cnt THEN 1 ELSE 0 END) | [] | [{"table": "customer360__customer_value_analysis", "column": "support_resolution_efficiency"}, {"table": "customer360__customer_value_analysis", "column": "support_resolution_efficiency"}, {"table": "customer360__customer_value_analysis", "column": "support_resolution_efficiency"}, {"table": "customer360__customer_value_analysis", "column": "support_resolution_efficiency"}, {"table": "customer360__customer", "column": "total_sales_amount"}, {"table": "customer360__customer", "column": "total_sales_amount"}, {"table": "customer360__customer", "column": "total_sales_amount"}, {"table": "customer360__customer", "column": "total_sales_amount"}, {"table": "customer360__customer_value_analysis", "column": "product_adoption_rate"}, {"table": "customer360__customer_value_analysis", "column": "product_adoption_rate"}, {"table": "customer360__customer_value_analysis", "column": "product_adoption_rate"}, {"table": "customer360__customer_value_analysis", "column": "product_adoption_rate"}] | False |
| B13 | AVG(CASE WHEN rn_ips_asc >= 0.7 * total_cnt THEN investment_priority_score END) | [{"table": "customer360__customer_value_analysis", "column": "investment_priority_score"}] | [{"table": "customer360__customer_value_analysis", "column": "investment_priority_score"}] | False |
| B13 | MIN(CASE WHEN rn_ips_asc >= 0.7 * total_cnt THEN investment_priority_score END) | [{"table": "customer360__customer_value_analysis", "column": "investment_priority_score"}] | [{"table": "customer360__customer_value_analysis", "column": "investment_priority_score"}] | False |


## S48

类别 `data`；来源 `query_db`；调用 `8f4d2dcc21b545cf96c2a1e7b1fbfe3b`；状态 `failed`。

```sql
WITH base AS (
  SELECT DISTINCT v.primary_email, v.investment_priority_score, v.product_adoption_rate,
    v.support_resolution_efficiency, v.acquisition_cost, v.customer_lifetime_value,
    v.lifecycle_stage, v.industry_vertical, v.company_size_tier,
    v.customer_onboarding_score, v.team_size, v.decision_maker_level,
    v.digital_engagement_score, v.nps_score, v.customer_health_score, v.churn_probability,
    c_sales.total_sales_amount
  FROM (
    SELECT DISTINCT * FROM customer360__customer_value_analysis
  ) v
  LEFT JOIN (
    SELECT email, MAX(total_sales_amount) AS total_sales_amount
    FROM customer360__customer
    WHERE total_sales_amount IS NOT NULL
    GROUP BY email
  ) c_sales ON v.primary_email = c_sales.email
  WHERE v.primary_email IS NOT NULL
),
scaled AS (
  SELECT *,
    (total_sales_amount - (SELECT MIN(total_sales_amount) FROM base)) / 
      NULLIF((SELECT MAX(total_sales_amount) - MIN(total_sales_amount) FROM base), 0) AS nsales,
    (product_adoption_rate - (SELECT MIN(product_adoption_rate) FROM base)) / 
      NULLIF((SELECT MAX(product_adoption_rate) - MIN(product_adoption_rate) FROM base), 0) AS nadopt,
    (support_resolution_efficiency - (SELECT MIN(support_resolution_efficiency) FROM base)) / 
      NULLIF((SELECT MAX(support_resolution_efficiency) - MIN(support_resolution_efficiency) FROM base), 0) AS nres
  FROM base
  WHERE product_adoption_rate IS NOT NULL AND support_resolution_efficiency IS NOT NULL
    AND total_sales_amount IS NOT NULL AND acquisition_cost IS NOT NULL AND customer_lifetime_value IS NOT NULL
),
with_comp AS (
  SELECT *, 0.4*nsales + 0.35*nadopt + 0.25*nres AS composite_score
  FROM scaled
),
ranked AS (
  SELECT *,
    ROW_NUMBER() OVER (ORDER BY investment_priority_score ASC) AS rn_ips_asc,
    ROW_NUMBER() OVER (ORDER BY composite_score ASC) AS rn_comp_asc,
    COUNT(*) OVER () AS total_cnt
  FROM with_comp
),
cohort AS (
  SELECT * FROM ranked
  WHERE rn_ips_asc >= 0.7*total_cnt AND rn_comp_asc <= 0.5*total_cnt
)
SELECT COUNT(*) AS cohort_size,
  AVG(investment_priority_score) AS avg_ips,
  AVG(composite_score) AS avg_composite,
  AVG(total_sales_amount) AS avg_sales,
  AVG(product_adoption_rate) AS avg_par,
  AVG(support_resolution_efficiency) AS avg_sre,
  AVG(customer_lifetime_value / acquisition_cost) AS avg_roi,
  MIN(customer_lifetime_value / acquisition_cost) AS min_roi,
  MAX(customer_lifetime_value / acquisition_cost) AS max_roi,
  MEDIAN(customer_lifetime_value / acquisition_cost) AS median_roi
FROM cohort
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-055/attempt-01/sql/S48.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-055/attempt-01/sql/S48.parameters.json)。

错误：`OperationalError('no such function: MEDIAN')`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "customer360__customer_value_analysis", "kind": "base", "block": null, "base_tables": ["customer360__customer_value_analysis"]}] | [] | [] |
| B2 | [{"alias": "customer360__customer", "kind": "base", "block": null, "base_tables": ["customer360__customer"]}] | [] | ["email"] |
| B3 | [{"alias": "v", "kind": "derived", "block": "B1", "base_tables": ["customer360__customer_value_analysis"]}, {"alias": "c_sales", "kind": "derived", "block": "B2", "base_tables": ["customer360__customer"]}] | [{"type": "LEFT", "right": "(SELECT email, MAX(total_sales_amount) AS total_sales_amount FROM customer360__customer WHERE NOT total_sales_amount IS NULL GROUP BY email) AS c_sales", "on": "v.primary_email = c_sales.email", "using": []}] | [] |
| B4 | [{"alias": "base", "kind": "derived", "block": "B3", "base_tables": ["customer360__customer", "customer360__customer_value_analysis"]}] | [] | [] |
| B5 | [{"alias": "base", "kind": "derived", "block": "B3", "base_tables": ["customer360__customer", "customer360__customer_value_analysis"]}] | [] | [] |
| B6 | [{"alias": "base", "kind": "derived", "block": "B3", "base_tables": ["customer360__customer", "customer360__customer_value_analysis"]}] | [] | [] |
| B7 | [{"alias": "base", "kind": "derived", "block": "B3", "base_tables": ["customer360__customer", "customer360__customer_value_analysis"]}] | [] | [] |
| B8 | [{"alias": "base", "kind": "derived", "block": "B3", "base_tables": ["customer360__customer", "customer360__customer_value_analysis"]}] | [] | [] |
| B9 | [{"alias": "base", "kind": "derived", "block": "B3", "base_tables": ["customer360__customer", "customer360__customer_value_analysis"]}] | [] | [] |
| B10 | [{"alias": "base", "kind": "derived", "block": "B3", "base_tables": ["customer360__customer", "customer360__customer_value_analysis"]}] | [] | [] |
| B11 | [{"alias": "scaled", "kind": "derived", "block": "B10", "base_tables": ["customer360__customer", "customer360__customer_value_analysis"]}] | [] | [] |
| B12 | [{"alias": "with_comp", "kind": "derived", "block": "B11", "base_tables": ["customer360__customer", "customer360__customer_value_analysis"]}] | [] | [] |
| B13 | [{"alias": "ranked", "kind": "derived", "block": "B12", "base_tables": ["customer360__customer", "customer360__customer_value_analysis"]}] | [] | [] |
| B14 | [{"alias": "cohort", "kind": "derived", "block": "B13", "base_tables": ["customer360__customer", "customer360__customer_value_analysis"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B2 | MAX(total_sales_amount) | [{"table": "customer360__customer", "column": "total_sales_amount"}] | [] | False |
| B4 | MIN(total_sales_amount) | [{"table": "customer360__customer", "column": "total_sales_amount"}] | [] | False |
| B5 | MAX(total_sales_amount) | [{"table": "customer360__customer", "column": "total_sales_amount"}] | [] | False |
| B5 | MIN(total_sales_amount) | [{"table": "customer360__customer", "column": "total_sales_amount"}] | [] | False |
| B6 | MIN(product_adoption_rate) | [{"table": "customer360__customer_value_analysis", "column": "product_adoption_rate"}] | [] | False |
| B7 | MAX(product_adoption_rate) | [{"table": "customer360__customer_value_analysis", "column": "product_adoption_rate"}] | [] | False |
| B7 | MIN(product_adoption_rate) | [{"table": "customer360__customer_value_analysis", "column": "product_adoption_rate"}] | [] | False |
| B8 | MIN(support_resolution_efficiency) | [{"table": "customer360__customer_value_analysis", "column": "support_resolution_efficiency"}] | [] | False |
| B9 | MAX(support_resolution_efficiency) | [{"table": "customer360__customer_value_analysis", "column": "support_resolution_efficiency"}] | [] | False |
| B9 | MIN(support_resolution_efficiency) | [{"table": "customer360__customer_value_analysis", "column": "support_resolution_efficiency"}] | [] | False |
| B14 | COUNT(*) | [] | [] | True |
| B14 | AVG(investment_priority_score) | [{"table": "customer360__customer_value_analysis", "column": "investment_priority_score"}] | [] | False |
| B14 | AVG(composite_score) | [{"table": "customer360__customer_value_analysis", "column": "support_resolution_efficiency"}, {"table": "customer360__customer_value_analysis", "column": "support_resolution_efficiency"}, {"table": "customer360__customer_value_analysis", "column": "support_resolution_efficiency"}, {"table": "customer360__customer_value_analysis", "column": "support_resolution_efficiency"}, {"table": "customer360__customer", "column": "total_sales_amount"}, {"table": "customer360__customer", "column": "total_sales_amount"}, {"table": "customer360__customer", "column": "total_sales_amount"}, {"table": "customer360__customer", "column": "total_sales_amount"}, {"table": "customer360__customer_value_analysis", "column": "product_adoption_rate"}, {"table": "customer360__customer_value_analysis", "column": "product_adoption_rate"}, {"table": "customer360__customer_value_analysis", "column": "product_adoption_rate"}, {"table": "customer360__customer_value_analysis", "column": "product_adoption_rate"}] | [] | False |
| B14 | AVG(total_sales_amount) | [{"table": "customer360__customer", "column": "total_sales_amount"}] | [] | False |
| B14 | AVG(product_adoption_rate) | [{"table": "customer360__customer_value_analysis", "column": "product_adoption_rate"}] | [] | False |
| B14 | AVG(support_resolution_efficiency) | [{"table": "customer360__customer_value_analysis", "column": "support_resolution_efficiency"}] | [] | False |
| B14 | AVG(customer_lifetime_value / acquisition_cost) | [{"table": "customer360__customer_value_analysis", "column": "customer_lifetime_value"}, {"table": "customer360__customer_value_analysis", "column": "acquisition_cost"}] | [] | False |
| B14 | MIN(customer_lifetime_value / acquisition_cost) | [{"table": "customer360__customer_value_analysis", "column": "customer_lifetime_value"}, {"table": "customer360__customer_value_analysis", "column": "acquisition_cost"}] | [] | False |
| B14 | MAX(customer_lifetime_value / acquisition_cost) | [{"table": "customer360__customer_value_analysis", "column": "customer_lifetime_value"}, {"table": "customer360__customer_value_analysis", "column": "acquisition_cost"}] | [] | False |
| B14 | PERCENTILE_CONT(customer_lifetime_value / acquisition_cost, 0.5) | [{"table": "customer360__customer_value_analysis", "column": "customer_lifetime_value"}, {"table": "customer360__customer_value_analysis", "column": "acquisition_cost"}] | [] | False |


## S49

类别 `data`；来源 `query_db`；调用 `3c8ece864a604aa3a5d917e696d312f6`；状态 `success`。

```sql
WITH base AS (
  SELECT DISTINCT v.primary_email, v.investment_priority_score, v.product_adoption_rate,
    v.support_resolution_efficiency, v.acquisition_cost, v.customer_lifetime_value,
    v.lifecycle_stage, v.industry_vertical, v.company_size_tier,
    v.customer_onboarding_score, v.team_size, v.decision_maker_level,
    v.digital_engagement_score, v.nps_score, v.customer_health_score, v.churn_probability,
    c_sales.total_sales_amount
  FROM (
    SELECT DISTINCT * FROM customer360__customer_value_analysis
  ) v
  LEFT JOIN (
    SELECT email, MAX(total_sales_amount) AS total_sales_amount
    FROM customer360__customer
    WHERE total_sales_amount IS NOT NULL
    GROUP BY email
  ) c_sales ON v.primary_email = c_sales.email
  WHERE v.primary_email IS NOT NULL
),
scaled AS (
  SELECT *,
    (total_sales_amount - (SELECT MIN(total_sales_amount) FROM base)) / 
      NULLIF((SELECT MAX(total_sales_amount) - MIN(total_sales_amount) FROM base), 0) AS nsales,
    (product_adoption_rate - (SELECT MIN(product_adoption_rate) FROM base)) / 
      NULLIF((SELECT MAX(product_adoption_rate) - MIN(product_adoption_rate) FROM base), 0) AS nadopt,
    (support_resolution_efficiency - (SELECT MIN(support_resolution_efficiency) FROM base)) / 
      NULLIF((SELECT MAX(support_resolution_efficiency) - MIN(support_resolution_efficiency) FROM base), 0) AS nres
  FROM base
  WHERE product_adoption_rate IS NOT NULL AND support_resolution_efficiency IS NOT NULL
    AND total_sales_amount IS NOT NULL AND acquisition_cost IS NOT NULL AND customer_lifetime_value IS NOT NULL
),
with_comp AS (
  SELECT *, 0.4*nsales + 0.35*nadopt + 0.25*nres AS composite_score
  FROM scaled
),
ranked AS (
  SELECT *,
    ROW_NUMBER() OVER (ORDER BY investment_priority_score ASC) AS rn_ips_asc,
    ROW_NUMBER() OVER (ORDER BY composite_score ASC) AS rn_comp_asc,
    COUNT(*) OVER () AS total_cnt
  FROM with_comp
),
cohort AS (
  SELECT * FROM ranked
  WHERE rn_ips_asc >= 0.7*total_cnt AND rn_comp_asc <= 0.5*total_cnt
)
SELECT COUNT(*) AS cohort_size,
  AVG(investment_priority_score) AS avg_ips,
  AVG(composite_score) AS avg_composite,
  AVG(total_sales_amount) AS avg_sales,
  AVG(product_adoption_rate) AS avg_par,
  AVG(support_resolution_efficiency) AS avg_sre,
  AVG(customer_lifetime_value / NULLIF(acquisition_cost, 0)) AS avg_roi
FROM cohort
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-055/attempt-01/sql/S49.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-055/attempt-01/sql/S49.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-055/attempt-01/results/S49.rows.jsonl)；完整：True；SHA256：`9bb916290107101d5709ab61aba57cce11b2a14352bc846bcd23fabf3c2f1719`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "customer360__customer_value_analysis", "kind": "base", "block": null, "base_tables": ["customer360__customer_value_analysis"]}] | [] | [] |
| B2 | [{"alias": "customer360__customer", "kind": "base", "block": null, "base_tables": ["customer360__customer"]}] | [] | ["email"] |
| B3 | [{"alias": "v", "kind": "derived", "block": "B1", "base_tables": ["customer360__customer_value_analysis"]}, {"alias": "c_sales", "kind": "derived", "block": "B2", "base_tables": ["customer360__customer"]}] | [{"type": "LEFT", "right": "(SELECT email, MAX(total_sales_amount) AS total_sales_amount FROM customer360__customer WHERE NOT total_sales_amount IS NULL GROUP BY email) AS c_sales", "on": "v.primary_email = c_sales.email", "using": []}] | [] |
| B4 | [{"alias": "base", "kind": "derived", "block": "B3", "base_tables": ["customer360__customer", "customer360__customer_value_analysis"]}] | [] | [] |
| B5 | [{"alias": "base", "kind": "derived", "block": "B3", "base_tables": ["customer360__customer", "customer360__customer_value_analysis"]}] | [] | [] |
| B6 | [{"alias": "base", "kind": "derived", "block": "B3", "base_tables": ["customer360__customer", "customer360__customer_value_analysis"]}] | [] | [] |
| B7 | [{"alias": "base", "kind": "derived", "block": "B3", "base_tables": ["customer360__customer", "customer360__customer_value_analysis"]}] | [] | [] |
| B8 | [{"alias": "base", "kind": "derived", "block": "B3", "base_tables": ["customer360__customer", "customer360__customer_value_analysis"]}] | [] | [] |
| B9 | [{"alias": "base", "kind": "derived", "block": "B3", "base_tables": ["customer360__customer", "customer360__customer_value_analysis"]}] | [] | [] |
| B10 | [{"alias": "base", "kind": "derived", "block": "B3", "base_tables": ["customer360__customer", "customer360__customer_value_analysis"]}] | [] | [] |
| B11 | [{"alias": "scaled", "kind": "derived", "block": "B10", "base_tables": ["customer360__customer", "customer360__customer_value_analysis"]}] | [] | [] |
| B12 | [{"alias": "with_comp", "kind": "derived", "block": "B11", "base_tables": ["customer360__customer", "customer360__customer_value_analysis"]}] | [] | [] |
| B13 | [{"alias": "ranked", "kind": "derived", "block": "B12", "base_tables": ["customer360__customer", "customer360__customer_value_analysis"]}] | [] | [] |
| B14 | [{"alias": "cohort", "kind": "derived", "block": "B13", "base_tables": ["customer360__customer", "customer360__customer_value_analysis"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B2 | MAX(total_sales_amount) | [{"table": "customer360__customer", "column": "total_sales_amount"}] | [] | False |
| B4 | MIN(total_sales_amount) | [{"table": "customer360__customer", "column": "total_sales_amount"}] | [] | False |
| B5 | MAX(total_sales_amount) | [{"table": "customer360__customer", "column": "total_sales_amount"}] | [] | False |
| B5 | MIN(total_sales_amount) | [{"table": "customer360__customer", "column": "total_sales_amount"}] | [] | False |
| B6 | MIN(product_adoption_rate) | [{"table": "customer360__customer_value_analysis", "column": "product_adoption_rate"}] | [] | False |
| B7 | MAX(product_adoption_rate) | [{"table": "customer360__customer_value_analysis", "column": "product_adoption_rate"}] | [] | False |
| B7 | MIN(product_adoption_rate) | [{"table": "customer360__customer_value_analysis", "column": "product_adoption_rate"}] | [] | False |
| B8 | MIN(support_resolution_efficiency) | [{"table": "customer360__customer_value_analysis", "column": "support_resolution_efficiency"}] | [] | False |
| B9 | MAX(support_resolution_efficiency) | [{"table": "customer360__customer_value_analysis", "column": "support_resolution_efficiency"}] | [] | False |
| B9 | MIN(support_resolution_efficiency) | [{"table": "customer360__customer_value_analysis", "column": "support_resolution_efficiency"}] | [] | False |
| B14 | COUNT(*) | [] | [] | True |
| B14 | AVG(investment_priority_score) | [{"table": "customer360__customer_value_analysis", "column": "investment_priority_score"}] | [] | False |
| B14 | AVG(composite_score) | [{"table": "customer360__customer_value_analysis", "column": "support_resolution_efficiency"}, {"table": "customer360__customer_value_analysis", "column": "support_resolution_efficiency"}, {"table": "customer360__customer_value_analysis", "column": "support_resolution_efficiency"}, {"table": "customer360__customer_value_analysis", "column": "support_resolution_efficiency"}, {"table": "customer360__customer", "column": "total_sales_amount"}, {"table": "customer360__customer", "column": "total_sales_amount"}, {"table": "customer360__customer", "column": "total_sales_amount"}, {"table": "customer360__customer", "column": "total_sales_amount"}, {"table": "customer360__customer_value_analysis", "column": "product_adoption_rate"}, {"table": "customer360__customer_value_analysis", "column": "product_adoption_rate"}, {"table": "customer360__customer_value_analysis", "column": "product_adoption_rate"}, {"table": "customer360__customer_value_analysis", "column": "product_adoption_rate"}] | [] | False |
| B14 | AVG(total_sales_amount) | [{"table": "customer360__customer", "column": "total_sales_amount"}] | [] | False |
| B14 | AVG(product_adoption_rate) | [{"table": "customer360__customer_value_analysis", "column": "product_adoption_rate"}] | [] | False |
| B14 | AVG(support_resolution_efficiency) | [{"table": "customer360__customer_value_analysis", "column": "support_resolution_efficiency"}] | [] | False |
| B14 | AVG(customer_lifetime_value / NULLIF(acquisition_cost, 0)) | [{"table": "customer360__customer_value_analysis", "column": "customer_lifetime_value"}, {"table": "customer360__customer_value_analysis", "column": "acquisition_cost"}] | [] | False |


## S50

类别 `data`；来源 `query_db`；调用 `f1bb3d06ea0e4767abd0610082a11b7b`；状态 `success`。

```sql
WITH base AS (
  SELECT DISTINCT v.primary_email, v.investment_priority_score, v.product_adoption_rate,
    v.support_resolution_efficiency, v.acquisition_cost, v.customer_lifetime_value,
    v.lifecycle_stage, v.industry_vertical, v.company_size_tier,
    v.customer_onboarding_score, v.team_size, v.decision_maker_level,
    v.digital_engagement_score, v.nps_score, v.customer_health_score, v.churn_probability,
    c_sales.total_sales_amount
  FROM (
    SELECT DISTINCT * FROM customer360__customer_value_analysis
  ) v
  LEFT JOIN (
    SELECT email, MAX(total_sales_amount) AS total_sales_amount
    FROM customer360__customer
    WHERE total_sales_amount IS NOT NULL
    GROUP BY email
  ) c_sales ON v.primary_email = c_sales.email
  WHERE v.primary_email IS NOT NULL
),
scaled AS (
  SELECT *,
    (total_sales_amount - (SELECT MIN(total_sales_amount) FROM base)) / 
      NULLIF((SELECT MAX(total_sales_amount) - MIN(total_sales_amount) FROM base), 0) AS nsales,
    (product_adoption_rate - (SELECT MIN(product_adoption_rate) FROM base)) / 
      NULLIF((SELECT MAX(product_adoption_rate) - MIN(product_adoption_rate) FROM base), 0) AS nadopt,
    (support_resolution_efficiency - (SELECT MIN(support_resolution_efficiency) FROM base)) / 
      NULLIF((SELECT MAX(support_resolution_efficiency) - MIN(support_resolution_efficiency) FROM base), 0) AS nres
  FROM base
  WHERE product_adoption_rate IS NOT NULL AND support_resolution_efficiency IS NOT NULL
    AND total_sales_amount IS NOT NULL AND acquisition_cost IS NOT NULL AND customer_lifetime_value IS NOT NULL
),
with_comp AS (
  SELECT *, 0.4*nsales + 0.35*nadopt + 0.25*nres AS composite_score
  FROM scaled
),
ranked AS (
  SELECT *,
    ROW_NUMBER() OVER (ORDER BY investment_priority_score ASC) AS rn_ips_asc,
    ROW_NUMBER() OVER (ORDER BY composite_score ASC) AS rn_comp_asc,
    COUNT(*) OVER () AS total_cnt
  FROM with_comp
),
cohort AS (
  SELECT * FROM ranked
  WHERE rn_ips_asc >= 0.7*total_cnt AND rn_comp_asc <= 0.5*total_cnt
)
SELECT lifecycle_stage, COUNT(*) AS cnt,
  AVG(customer_lifetime_value / NULLIF(acquisition_cost, 0)) AS avg_roi,
  MIN(customer_lifetime_value / NULLIF(acquisition_cost, 0)) AS min_roi,
  MAX(customer_lifetime_value / NULLIF(acquisition_cost, 0)) AS max_roi,
  AVG(investment_priority_score) AS avg_ips,
  AVG(composite_score) AS avg_comp,
  AVG(product_adoption_rate) AS avg_par,
  AVG(support_resolution_efficiency) AS avg_sre,
  AVG(total_sales_amount) AS avg_sales
FROM cohort
GROUP BY lifecycle_stage
ORDER BY cnt DESC
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-055/attempt-01/sql/S50.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-055/attempt-01/sql/S50.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-055/attempt-01/results/S50.rows.jsonl)；完整：True；SHA256：`75232c3e54fcae37ff3e501b2a2019105658d1ace29b55541391b4a8338ea6a4`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "customer360__customer_value_analysis", "kind": "base", "block": null, "base_tables": ["customer360__customer_value_analysis"]}] | [] | [] |
| B2 | [{"alias": "customer360__customer", "kind": "base", "block": null, "base_tables": ["customer360__customer"]}] | [] | ["email"] |
| B3 | [{"alias": "v", "kind": "derived", "block": "B1", "base_tables": ["customer360__customer_value_analysis"]}, {"alias": "c_sales", "kind": "derived", "block": "B2", "base_tables": ["customer360__customer"]}] | [{"type": "LEFT", "right": "(SELECT email, MAX(total_sales_amount) AS total_sales_amount FROM customer360__customer WHERE NOT total_sales_amount IS NULL GROUP BY email) AS c_sales", "on": "v.primary_email = c_sales.email", "using": []}] | [] |
| B4 | [{"alias": "base", "kind": "derived", "block": "B3", "base_tables": ["customer360__customer", "customer360__customer_value_analysis"]}] | [] | [] |
| B5 | [{"alias": "base", "kind": "derived", "block": "B3", "base_tables": ["customer360__customer", "customer360__customer_value_analysis"]}] | [] | [] |
| B6 | [{"alias": "base", "kind": "derived", "block": "B3", "base_tables": ["customer360__customer", "customer360__customer_value_analysis"]}] | [] | [] |
| B7 | [{"alias": "base", "kind": "derived", "block": "B3", "base_tables": ["customer360__customer", "customer360__customer_value_analysis"]}] | [] | [] |
| B8 | [{"alias": "base", "kind": "derived", "block": "B3", "base_tables": ["customer360__customer", "customer360__customer_value_analysis"]}] | [] | [] |
| B9 | [{"alias": "base", "kind": "derived", "block": "B3", "base_tables": ["customer360__customer", "customer360__customer_value_analysis"]}] | [] | [] |
| B10 | [{"alias": "base", "kind": "derived", "block": "B3", "base_tables": ["customer360__customer", "customer360__customer_value_analysis"]}] | [] | [] |
| B11 | [{"alias": "scaled", "kind": "derived", "block": "B10", "base_tables": ["customer360__customer", "customer360__customer_value_analysis"]}] | [] | [] |
| B12 | [{"alias": "with_comp", "kind": "derived", "block": "B11", "base_tables": ["customer360__customer", "customer360__customer_value_analysis"]}] | [] | [] |
| B13 | [{"alias": "ranked", "kind": "derived", "block": "B12", "base_tables": ["customer360__customer", "customer360__customer_value_analysis"]}] | [] | [] |
| B14 | [{"alias": "cohort", "kind": "derived", "block": "B13", "base_tables": ["customer360__customer", "customer360__customer_value_analysis"]}] | [] | ["lifecycle_stage"] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B2 | MAX(total_sales_amount) | [{"table": "customer360__customer", "column": "total_sales_amount"}] | [] | False |
| B4 | MIN(total_sales_amount) | [{"table": "customer360__customer", "column": "total_sales_amount"}] | [] | False |
| B5 | MAX(total_sales_amount) | [{"table": "customer360__customer", "column": "total_sales_amount"}] | [] | False |
| B5 | MIN(total_sales_amount) | [{"table": "customer360__customer", "column": "total_sales_amount"}] | [] | False |
| B6 | MIN(product_adoption_rate) | [{"table": "customer360__customer_value_analysis", "column": "product_adoption_rate"}] | [] | False |
| B7 | MAX(product_adoption_rate) | [{"table": "customer360__customer_value_analysis", "column": "product_adoption_rate"}] | [] | False |
| B7 | MIN(product_adoption_rate) | [{"table": "customer360__customer_value_analysis", "column": "product_adoption_rate"}] | [] | False |
| B8 | MIN(support_resolution_efficiency) | [{"table": "customer360__customer_value_analysis", "column": "support_resolution_efficiency"}] | [] | False |
| B9 | MAX(support_resolution_efficiency) | [{"table": "customer360__customer_value_analysis", "column": "support_resolution_efficiency"}] | [] | False |
| B9 | MIN(support_resolution_efficiency) | [{"table": "customer360__customer_value_analysis", "column": "support_resolution_efficiency"}] | [] | False |
| B14 | COUNT(*) | [] | [] | True |
| B14 | AVG(customer_lifetime_value / NULLIF(acquisition_cost, 0)) | [{"table": "customer360__customer_value_analysis", "column": "customer_lifetime_value"}, {"table": "customer360__customer_value_analysis", "column": "acquisition_cost"}] | [] | False |
| B14 | MIN(customer_lifetime_value / NULLIF(acquisition_cost, 0)) | [{"table": "customer360__customer_value_analysis", "column": "customer_lifetime_value"}, {"table": "customer360__customer_value_analysis", "column": "acquisition_cost"}] | [] | False |
| B14 | MAX(customer_lifetime_value / NULLIF(acquisition_cost, 0)) | [{"table": "customer360__customer_value_analysis", "column": "customer_lifetime_value"}, {"table": "customer360__customer_value_analysis", "column": "acquisition_cost"}] | [] | False |
| B14 | AVG(investment_priority_score) | [{"table": "customer360__customer_value_analysis", "column": "investment_priority_score"}] | [] | False |
| B14 | AVG(composite_score) | [{"table": "customer360__customer_value_analysis", "column": "support_resolution_efficiency"}, {"table": "customer360__customer_value_analysis", "column": "support_resolution_efficiency"}, {"table": "customer360__customer_value_analysis", "column": "support_resolution_efficiency"}, {"table": "customer360__customer_value_analysis", "column": "support_resolution_efficiency"}, {"table": "customer360__customer", "column": "total_sales_amount"}, {"table": "customer360__customer", "column": "total_sales_amount"}, {"table": "customer360__customer", "column": "total_sales_amount"}, {"table": "customer360__customer", "column": "total_sales_amount"}, {"table": "customer360__customer_value_analysis", "column": "product_adoption_rate"}, {"table": "customer360__customer_value_analysis", "column": "product_adoption_rate"}, {"table": "customer360__customer_value_analysis", "column": "product_adoption_rate"}, {"table": "customer360__customer_value_analysis", "column": "product_adoption_rate"}] | [] | False |
| B14 | AVG(product_adoption_rate) | [{"table": "customer360__customer_value_analysis", "column": "product_adoption_rate"}] | [] | False |
| B14 | AVG(support_resolution_efficiency) | [{"table": "customer360__customer_value_analysis", "column": "support_resolution_efficiency"}] | [] | False |
| B14 | AVG(total_sales_amount) | [{"table": "customer360__customer", "column": "total_sales_amount"}] | [] | False |


## S51

类别 `data`；来源 `query_db`；调用 `9016c6939af74de789d84c7d44bd1cba`；状态 `success`。

```sql
WITH base AS (
  SELECT DISTINCT v.primary_email, v.investment_priority_score, v.product_adoption_rate,
    v.support_resolution_efficiency, v.acquisition_cost, v.customer_lifetime_value,
    v.lifecycle_stage, v.industry_vertical, v.company_size_tier,
    v.customer_onboarding_score, v.team_size, v.decision_maker_level,
    v.digital_engagement_score, v.nps_score, v.customer_health_score, v.churn_probability,
    c_sales.total_sales_amount
  FROM (
    SELECT DISTINCT * FROM customer360__customer_value_analysis
  ) v
  LEFT JOIN (
    SELECT email, MAX(total_sales_amount) AS total_sales_amount
    FROM customer360__customer
    WHERE total_sales_amount IS NOT NULL
    GROUP BY email
  ) c_sales ON v.primary_email = c_sales.email
  WHERE v.primary_email IS NOT NULL
),
scaled AS (
  SELECT *,
    (total_sales_amount - (SELECT MIN(total_sales_amount) FROM base)) / 
      NULLIF((SELECT MAX(total_sales_amount) - MIN(total_sales_amount) FROM base), 0) AS nsales,
    (product_adoption_rate - (SELECT MIN(product_adoption_rate) FROM base)) / 
      NULLIF((SELECT MAX(product_adoption_rate) - MIN(product_adoption_rate) FROM base), 0) AS nadopt,
    (support_resolution_efficiency - (SELECT MIN(support_resolution_efficiency) FROM base)) / 
      NULLIF((SELECT MAX(support_resolution_efficiency) - MIN(support_resolution_efficiency) FROM base), 0) AS nres
  FROM base
  WHERE product_adoption_rate IS NOT NULL AND support_resolution_efficiency IS NOT NULL
    AND total_sales_amount IS NOT NULL AND acquisition_cost IS NOT NULL AND customer_lifetime_value IS NOT NULL
),
with_comp AS (
  SELECT *, 0.4*nsales + 0.35*nadopt + 0.25*nres AS composite_score
  FROM scaled
),
ranked AS (
  SELECT *,
    ROW_NUMBER() OVER (ORDER BY investment_priority_score ASC) AS rn_ips_asc,
    ROW_NUMBER() OVER (ORDER BY composite_score ASC) AS rn_comp_asc,
    COUNT(*) OVER () AS total_cnt
  FROM with_comp
),
cohort AS (
  SELECT * FROM ranked
  WHERE rn_ips_asc >= 0.7*total_cnt AND rn_comp_asc <= 0.5*total_cnt
)
SELECT industry_vertical, company_size_tier, COUNT(*) AS cnt,
  AVG(customer_lifetime_value / NULLIF(acquisition_cost, 0)) AS avg_roi,
  AVG(investment_priority_score) AS avg_ips,
  AVG(composite_score) AS avg_comp,
  AVG(product_adoption_rate) AS avg_par,
  AVG(support_resolution_efficiency) AS avg_sre,
  AVG(total_sales_amount) AS avg_sales
FROM cohort
WHERE industry_vertical IS NOT NULL AND company_size_tier IS NOT NULL
GROUP BY industry_vertical, company_size_tier
ORDER BY cnt DESC
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-055/attempt-01/sql/S51.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-055/attempt-01/sql/S51.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-055/attempt-01/results/S51.rows.jsonl)；完整：True；SHA256：`5fdc86e8ea46d78521028e79db08001bc517b61b6c2e7028af419cfd76bb948f`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "customer360__customer_value_analysis", "kind": "base", "block": null, "base_tables": ["customer360__customer_value_analysis"]}] | [] | [] |
| B2 | [{"alias": "customer360__customer", "kind": "base", "block": null, "base_tables": ["customer360__customer"]}] | [] | ["email"] |
| B3 | [{"alias": "v", "kind": "derived", "block": "B1", "base_tables": ["customer360__customer_value_analysis"]}, {"alias": "c_sales", "kind": "derived", "block": "B2", "base_tables": ["customer360__customer"]}] | [{"type": "LEFT", "right": "(SELECT email, MAX(total_sales_amount) AS total_sales_amount FROM customer360__customer WHERE NOT total_sales_amount IS NULL GROUP BY email) AS c_sales", "on": "v.primary_email = c_sales.email", "using": []}] | [] |
| B4 | [{"alias": "base", "kind": "derived", "block": "B3", "base_tables": ["customer360__customer", "customer360__customer_value_analysis"]}] | [] | [] |
| B5 | [{"alias": "base", "kind": "derived", "block": "B3", "base_tables": ["customer360__customer", "customer360__customer_value_analysis"]}] | [] | [] |
| B6 | [{"alias": "base", "kind": "derived", "block": "B3", "base_tables": ["customer360__customer", "customer360__customer_value_analysis"]}] | [] | [] |
| B7 | [{"alias": "base", "kind": "derived", "block": "B3", "base_tables": ["customer360__customer", "customer360__customer_value_analysis"]}] | [] | [] |
| B8 | [{"alias": "base", "kind": "derived", "block": "B3", "base_tables": ["customer360__customer", "customer360__customer_value_analysis"]}] | [] | [] |
| B9 | [{"alias": "base", "kind": "derived", "block": "B3", "base_tables": ["customer360__customer", "customer360__customer_value_analysis"]}] | [] | [] |
| B10 | [{"alias": "base", "kind": "derived", "block": "B3", "base_tables": ["customer360__customer", "customer360__customer_value_analysis"]}] | [] | [] |
| B11 | [{"alias": "scaled", "kind": "derived", "block": "B10", "base_tables": ["customer360__customer", "customer360__customer_value_analysis"]}] | [] | [] |
| B12 | [{"alias": "with_comp", "kind": "derived", "block": "B11", "base_tables": ["customer360__customer", "customer360__customer_value_analysis"]}] | [] | [] |
| B13 | [{"alias": "ranked", "kind": "derived", "block": "B12", "base_tables": ["customer360__customer", "customer360__customer_value_analysis"]}] | [] | [] |
| B14 | [{"alias": "cohort", "kind": "derived", "block": "B13", "base_tables": ["customer360__customer", "customer360__customer_value_analysis"]}] | [] | ["industry_vertical", "company_size_tier"] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B2 | MAX(total_sales_amount) | [{"table": "customer360__customer", "column": "total_sales_amount"}] | [] | False |
| B4 | MIN(total_sales_amount) | [{"table": "customer360__customer", "column": "total_sales_amount"}] | [] | False |
| B5 | MAX(total_sales_amount) | [{"table": "customer360__customer", "column": "total_sales_amount"}] | [] | False |
| B5 | MIN(total_sales_amount) | [{"table": "customer360__customer", "column": "total_sales_amount"}] | [] | False |
| B6 | MIN(product_adoption_rate) | [{"table": "customer360__customer_value_analysis", "column": "product_adoption_rate"}] | [] | False |
| B7 | MAX(product_adoption_rate) | [{"table": "customer360__customer_value_analysis", "column": "product_adoption_rate"}] | [] | False |
| B7 | MIN(product_adoption_rate) | [{"table": "customer360__customer_value_analysis", "column": "product_adoption_rate"}] | [] | False |
| B8 | MIN(support_resolution_efficiency) | [{"table": "customer360__customer_value_analysis", "column": "support_resolution_efficiency"}] | [] | False |
| B9 | MAX(support_resolution_efficiency) | [{"table": "customer360__customer_value_analysis", "column": "support_resolution_efficiency"}] | [] | False |
| B9 | MIN(support_resolution_efficiency) | [{"table": "customer360__customer_value_analysis", "column": "support_resolution_efficiency"}] | [] | False |
| B14 | COUNT(*) | [] | [] | True |
| B14 | AVG(customer_lifetime_value / NULLIF(acquisition_cost, 0)) | [{"table": "customer360__customer_value_analysis", "column": "customer_lifetime_value"}, {"table": "customer360__customer_value_analysis", "column": "acquisition_cost"}] | [] | False |
| B14 | AVG(investment_priority_score) | [{"table": "customer360__customer_value_analysis", "column": "investment_priority_score"}] | [] | False |
| B14 | AVG(composite_score) | [{"table": "customer360__customer_value_analysis", "column": "support_resolution_efficiency"}, {"table": "customer360__customer_value_analysis", "column": "support_resolution_efficiency"}, {"table": "customer360__customer_value_analysis", "column": "support_resolution_efficiency"}, {"table": "customer360__customer_value_analysis", "column": "support_resolution_efficiency"}, {"table": "customer360__customer", "column": "total_sales_amount"}, {"table": "customer360__customer", "column": "total_sales_amount"}, {"table": "customer360__customer", "column": "total_sales_amount"}, {"table": "customer360__customer", "column": "total_sales_amount"}, {"table": "customer360__customer_value_analysis", "column": "product_adoption_rate"}, {"table": "customer360__customer_value_analysis", "column": "product_adoption_rate"}, {"table": "customer360__customer_value_analysis", "column": "product_adoption_rate"}, {"table": "customer360__customer_value_analysis", "column": "product_adoption_rate"}] | [] | False |
| B14 | AVG(product_adoption_rate) | [{"table": "customer360__customer_value_analysis", "column": "product_adoption_rate"}] | [] | False |
| B14 | AVG(support_resolution_efficiency) | [{"table": "customer360__customer_value_analysis", "column": "support_resolution_efficiency"}] | [] | False |
| B14 | AVG(total_sales_amount) | [{"table": "customer360__customer", "column": "total_sales_amount"}] | [] | False |


## S52

类别 `data`；来源 `query_db`；调用 `911177ec1a3f4385968ddb90f1138d96`；状态 `success`。

```sql
WITH base AS (
  SELECT DISTINCT v.primary_email, v.investment_priority_score, v.product_adoption_rate,
    v.support_resolution_efficiency, v.acquisition_cost, v.customer_lifetime_value,
    v.lifecycle_stage, v.industry_vertical, v.company_size_tier,
    v.customer_onboarding_score, v.team_size, v.decision_maker_level,
    v.digital_engagement_score, v.nps_score, v.customer_health_score, v.churn_probability,
    c_sales.total_sales_amount
  FROM (
    SELECT DISTINCT * FROM customer360__customer_value_analysis
  ) v
  LEFT JOIN (
    SELECT email, MAX(total_sales_amount) AS total_sales_amount
    FROM customer360__customer
    WHERE total_sales_amount IS NOT NULL
    GROUP BY email
  ) c_sales ON v.primary_email = c_sales.email
  WHERE v.primary_email IS NOT NULL
),
scaled AS (
  SELECT *,
    (total_sales_amount - (SELECT MIN(total_sales_amount) FROM base)) / 
      NULLIF((SELECT MAX(total_sales_amount) - MIN(total_sales_amount) FROM base), 0) AS nsales,
    (product_adoption_rate - (SELECT MIN(product_adoption_rate) FROM base)) / 
      NULLIF((SELECT MAX(product_adoption_rate) - MIN(product_adoption_rate) FROM base), 0) AS nadopt,
    (support_resolution_efficiency - (SELECT MIN(support_resolution_efficiency) FROM base)) / 
      NULLIF((SELECT MAX(support_resolution_efficiency) - MIN(support_resolution_efficiency) FROM base), 0) AS nres
  FROM base
  WHERE product_adoption_rate IS NOT NULL AND support_resolution_efficiency IS NOT NULL
    AND total_sales_amount IS NOT NULL AND acquisition_cost IS NOT NULL AND customer_lifetime_value IS NOT NULL
),
with_comp AS (
  SELECT *, 0.4*nsales + 0.35*nadopt + 0.25*nres AS composite_score
  FROM scaled
),
ranked AS (
  SELECT *,
    ROW_NUMBER() OVER (ORDER BY investment_priority_score ASC) AS rn_ips_asc,
    ROW_NUMBER() OVER (ORDER BY composite_score ASC) AS rn_comp_asc,
    COUNT(*) OVER () AS total_cnt
  FROM with_comp
),
flagged AS (
  SELECT *, CASE WHEN rn_ips_asc >= 0.7*total_cnt AND rn_comp_asc <= 0.5*total_cnt THEN 1 ELSE 0 END AS is_target
  FROM ranked
)
SELECT industry_vertical,
  COUNT(*) AS total_cnt,
  SUM(is_target) AS cohort_cnt,
  ROUND(100.0*SUM(is_target)/COUNT(*), 1) AS cohort_pct,
  AVG(CASE WHEN is_target=1 THEN customer_lifetime_value/NULLIF(acquisition_cost,0) END) AS cohort_avg_roi,
  AVG(CASE WHEN is_target=0 THEN customer_lifetime_value/NULLIF(acquisition_cost,0) END) AS noncohort_avg_roi,
  AVG(CASE WHEN is_target=1 THEN investment_priority_score END) AS cohort_avg_ips,
  AVG(CASE WHEN is_target=0 THEN investment_priority_score END) AS noncohort_avg_ips
FROM flagged
WHERE industry_vertical IS NOT NULL
GROUP BY industry_vertical
ORDER BY cohort_cnt DESC
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-055/attempt-01/sql/S52.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-055/attempt-01/sql/S52.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-055/attempt-01/results/S52.rows.jsonl)；完整：True；SHA256：`a3008475b0f3618ed562d0996a24277c9d14cf5b225e2cc924339a519b85d910`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "customer360__customer_value_analysis", "kind": "base", "block": null, "base_tables": ["customer360__customer_value_analysis"]}] | [] | [] |
| B2 | [{"alias": "customer360__customer", "kind": "base", "block": null, "base_tables": ["customer360__customer"]}] | [] | ["email"] |
| B3 | [{"alias": "v", "kind": "derived", "block": "B1", "base_tables": ["customer360__customer_value_analysis"]}, {"alias": "c_sales", "kind": "derived", "block": "B2", "base_tables": ["customer360__customer"]}] | [{"type": "LEFT", "right": "(SELECT email, MAX(total_sales_amount) AS total_sales_amount FROM customer360__customer WHERE NOT total_sales_amount IS NULL GROUP BY email) AS c_sales", "on": "v.primary_email = c_sales.email", "using": []}] | [] |
| B4 | [{"alias": "base", "kind": "derived", "block": "B3", "base_tables": ["customer360__customer", "customer360__customer_value_analysis"]}] | [] | [] |
| B5 | [{"alias": "base", "kind": "derived", "block": "B3", "base_tables": ["customer360__customer", "customer360__customer_value_analysis"]}] | [] | [] |
| B6 | [{"alias": "base", "kind": "derived", "block": "B3", "base_tables": ["customer360__customer", "customer360__customer_value_analysis"]}] | [] | [] |
| B7 | [{"alias": "base", "kind": "derived", "block": "B3", "base_tables": ["customer360__customer", "customer360__customer_value_analysis"]}] | [] | [] |
| B8 | [{"alias": "base", "kind": "derived", "block": "B3", "base_tables": ["customer360__customer", "customer360__customer_value_analysis"]}] | [] | [] |
| B9 | [{"alias": "base", "kind": "derived", "block": "B3", "base_tables": ["customer360__customer", "customer360__customer_value_analysis"]}] | [] | [] |
| B10 | [{"alias": "base", "kind": "derived", "block": "B3", "base_tables": ["customer360__customer", "customer360__customer_value_analysis"]}] | [] | [] |
| B11 | [{"alias": "scaled", "kind": "derived", "block": "B10", "base_tables": ["customer360__customer", "customer360__customer_value_analysis"]}] | [] | [] |
| B12 | [{"alias": "with_comp", "kind": "derived", "block": "B11", "base_tables": ["customer360__customer", "customer360__customer_value_analysis"]}] | [] | [] |
| B13 | [{"alias": "ranked", "kind": "derived", "block": "B12", "base_tables": ["customer360__customer", "customer360__customer_value_analysis"]}] | [] | [] |
| B14 | [{"alias": "flagged", "kind": "derived", "block": "B13", "base_tables": ["customer360__customer", "customer360__customer_value_analysis"]}] | [] | ["industry_vertical"] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B2 | MAX(total_sales_amount) | [{"table": "customer360__customer", "column": "total_sales_amount"}] | [] | False |
| B4 | MIN(total_sales_amount) | [{"table": "customer360__customer", "column": "total_sales_amount"}] | [] | False |
| B5 | MAX(total_sales_amount) | [{"table": "customer360__customer", "column": "total_sales_amount"}] | [] | False |
| B5 | MIN(total_sales_amount) | [{"table": "customer360__customer", "column": "total_sales_amount"}] | [] | False |
| B6 | MIN(product_adoption_rate) | [{"table": "customer360__customer_value_analysis", "column": "product_adoption_rate"}] | [] | False |
| B7 | MAX(product_adoption_rate) | [{"table": "customer360__customer_value_analysis", "column": "product_adoption_rate"}] | [] | False |
| B7 | MIN(product_adoption_rate) | [{"table": "customer360__customer_value_analysis", "column": "product_adoption_rate"}] | [] | False |
| B8 | MIN(support_resolution_efficiency) | [{"table": "customer360__customer_value_analysis", "column": "support_resolution_efficiency"}] | [] | False |
| B9 | MAX(support_resolution_efficiency) | [{"table": "customer360__customer_value_analysis", "column": "support_resolution_efficiency"}] | [] | False |
| B9 | MIN(support_resolution_efficiency) | [{"table": "customer360__customer_value_analysis", "column": "support_resolution_efficiency"}] | [] | False |
| B14 | COUNT(*) | [] | [] | True |
| B14 | SUM(is_target) | [{"table": "customer360__customer_value_analysis", "column": "investment_priority_score"}, {"table": "customer360__customer_value_analysis", "column": "support_resolution_efficiency"}, {"table": "customer360__customer_value_analysis", "column": "support_resolution_efficiency"}, {"table": "customer360__customer_value_analysis", "column": "support_resolution_efficiency"}, {"table": "customer360__customer_value_analysis", "column": "support_resolution_efficiency"}, {"table": "customer360__customer", "column": "total_sales_amount"}, {"table": "customer360__customer", "column": "total_sales_amount"}, {"table": "customer360__customer", "column": "total_sales_amount"}, {"table": "customer360__customer", "column": "total_sales_amount"}, {"table": "customer360__customer_value_analysis", "column": "product_adoption_rate"}, {"table": "customer360__customer_value_analysis", "column": "product_adoption_rate"}, {"table": "customer360__customer_value_analysis", "column": "product_adoption_rate"}, {"table": "customer360__customer_value_analysis", "column": "product_adoption_rate"}] | [] | False |
| B14 | AVG(CASE WHEN is_target = 1 THEN customer_lifetime_value / NULLIF(acquisition_cost, 0) END) | [{"table": "customer360__customer_value_analysis", "column": "customer_lifetime_value"}, {"table": "customer360__customer_value_analysis", "column": "acquisition_cost"}] | [{"table": "customer360__customer_value_analysis", "column": "investment_priority_score"}, {"table": "customer360__customer_value_analysis", "column": "support_resolution_efficiency"}, {"table": "customer360__customer_value_analysis", "column": "support_resolution_efficiency"}, {"table": "customer360__customer_value_analysis", "column": "support_resolution_efficiency"}, {"table": "customer360__customer_value_analysis", "column": "support_resolution_efficiency"}, {"table": "customer360__customer", "column": "total_sales_amount"}, {"table": "customer360__customer", "column": "total_sales_amount"}, {"table": "customer360__customer", "column": "total_sales_amount"}, {"table": "customer360__customer", "column": "total_sales_amount"}, {"table": "customer360__customer_value_analysis", "column": "product_adoption_rate"}, {"table": "customer360__customer_value_analysis", "column": "product_adoption_rate"}, {"table": "customer360__customer_value_analysis", "column": "product_adoption_rate"}, {"table": "customer360__customer_value_analysis", "column": "product_adoption_rate"}] | False |
| B14 | AVG(CASE WHEN is_target = 0 THEN customer_lifetime_value / NULLIF(acquisition_cost, 0) END) | [{"table": "customer360__customer_value_analysis", "column": "customer_lifetime_value"}, {"table": "customer360__customer_value_analysis", "column": "acquisition_cost"}] | [{"table": "customer360__customer_value_analysis", "column": "investment_priority_score"}, {"table": "customer360__customer_value_analysis", "column": "support_resolution_efficiency"}, {"table": "customer360__customer_value_analysis", "column": "support_resolution_efficiency"}, {"table": "customer360__customer_value_analysis", "column": "support_resolution_efficiency"}, {"table": "customer360__customer_value_analysis", "column": "support_resolution_efficiency"}, {"table": "customer360__customer", "column": "total_sales_amount"}, {"table": "customer360__customer", "column": "total_sales_amount"}, {"table": "customer360__customer", "column": "total_sales_amount"}, {"table": "customer360__customer", "column": "total_sales_amount"}, {"table": "customer360__customer_value_analysis", "column": "product_adoption_rate"}, {"table": "customer360__customer_value_analysis", "column": "product_adoption_rate"}, {"table": "customer360__customer_value_analysis", "column": "product_adoption_rate"}, {"table": "customer360__customer_value_analysis", "column": "product_adoption_rate"}] | False |
| B14 | AVG(CASE WHEN is_target = 1 THEN investment_priority_score END) | [{"table": "customer360__customer_value_analysis", "column": "investment_priority_score"}] | [{"table": "customer360__customer_value_analysis", "column": "investment_priority_score"}, {"table": "customer360__customer_value_analysis", "column": "support_resolution_efficiency"}, {"table": "customer360__customer_value_analysis", "column": "support_resolution_efficiency"}, {"table": "customer360__customer_value_analysis", "column": "support_resolution_efficiency"}, {"table": "customer360__customer_value_analysis", "column": "support_resolution_efficiency"}, {"table": "customer360__customer", "column": "total_sales_amount"}, {"table": "customer360__customer", "column": "total_sales_amount"}, {"table": "customer360__customer", "column": "total_sales_amount"}, {"table": "customer360__customer", "column": "total_sales_amount"}, {"table": "customer360__customer_value_analysis", "column": "product_adoption_rate"}, {"table": "customer360__customer_value_analysis", "column": "product_adoption_rate"}, {"table": "customer360__customer_value_analysis", "column": "product_adoption_rate"}, {"table": "customer360__customer_value_analysis", "column": "product_adoption_rate"}] | False |
| B14 | AVG(CASE WHEN is_target = 0 THEN investment_priority_score END) | [{"table": "customer360__customer_value_analysis", "column": "investment_priority_score"}] | [{"table": "customer360__customer_value_analysis", "column": "investment_priority_score"}, {"table": "customer360__customer_value_analysis", "column": "support_resolution_efficiency"}, {"table": "customer360__customer_value_analysis", "column": "support_resolution_efficiency"}, {"table": "customer360__customer_value_analysis", "column": "support_resolution_efficiency"}, {"table": "customer360__customer_value_analysis", "column": "support_resolution_efficiency"}, {"table": "customer360__customer", "column": "total_sales_amount"}, {"table": "customer360__customer", "column": "total_sales_amount"}, {"table": "customer360__customer", "column": "total_sales_amount"}, {"table": "customer360__customer", "column": "total_sales_amount"}, {"table": "customer360__customer_value_analysis", "column": "product_adoption_rate"}, {"table": "customer360__customer_value_analysis", "column": "product_adoption_rate"}, {"table": "customer360__customer_value_analysis", "column": "product_adoption_rate"}, {"table": "customer360__customer_value_analysis", "column": "product_adoption_rate"}] | False |
| B14 | COUNT(*) | [] | [] | True |
| B14 | SUM(is_target) | [{"table": "customer360__customer_value_analysis", "column": "investment_priority_score"}, {"table": "customer360__customer_value_analysis", "column": "support_resolution_efficiency"}, {"table": "customer360__customer_value_analysis", "column": "support_resolution_efficiency"}, {"table": "customer360__customer_value_analysis", "column": "support_resolution_efficiency"}, {"table": "customer360__customer_value_analysis", "column": "support_resolution_efficiency"}, {"table": "customer360__customer", "column": "total_sales_amount"}, {"table": "customer360__customer", "column": "total_sales_amount"}, {"table": "customer360__customer", "column": "total_sales_amount"}, {"table": "customer360__customer", "column": "total_sales_amount"}, {"table": "customer360__customer_value_analysis", "column": "product_adoption_rate"}, {"table": "customer360__customer_value_analysis", "column": "product_adoption_rate"}, {"table": "customer360__customer_value_analysis", "column": "product_adoption_rate"}, {"table": "customer360__customer_value_analysis", "column": "product_adoption_rate"}] | [] | False |


## S53

类别 `data`；来源 `query_db`；调用 `41ab470c5b284ed38e3aa9d038fb3673`；状态 `success`。

```sql
WITH base AS (
  SELECT DISTINCT v.primary_email, v.investment_priority_score, v.product_adoption_rate,
    v.support_resolution_efficiency, v.acquisition_cost, v.customer_lifetime_value,
    v.lifecycle_stage, v.industry_vertical, v.company_size_tier,
    v.customer_onboarding_score, v.team_size, v.decision_maker_level,
    v.digital_engagement_score, v.nps_score, v.customer_health_score, v.churn_probability,
    c_sales.total_sales_amount
  FROM (
    SELECT DISTINCT * FROM customer360__customer_value_analysis
  ) v
  LEFT JOIN (
    SELECT email, MAX(total_sales_amount) AS total_sales_amount
    FROM customer360__customer
    WHERE total_sales_amount IS NOT NULL
    GROUP BY email
  ) c_sales ON v.primary_email = c_sales.email
  WHERE v.primary_email IS NOT NULL
),
scaled AS (
  SELECT *,
    (total_sales_amount - (SELECT MIN(total_sales_amount) FROM base)) / 
      NULLIF((SELECT MAX(total_sales_amount) - MIN(total_sales_amount) FROM base), 0) AS nsales,
    (product_adoption_rate - (SELECT MIN(product_adoption_rate) FROM base)) / 
      NULLIF((SELECT MAX(product_adoption_rate) - MIN(product_adoption_rate) FROM base), 0) AS nadopt,
    (support_resolution_efficiency - (SELECT MIN(support_resolution_efficiency) FROM base)) / 
      NULLIF((SELECT MAX(support_resolution_efficiency) - MIN(support_resolution_efficiency) FROM base), 0) AS nres
  FROM base
  WHERE product_adoption_rate IS NOT NULL AND support_resolution_efficiency IS NOT NULL
    AND total_sales_amount IS NOT NULL AND acquisition_cost IS NOT NULL AND customer_lifetime_value IS NOT NULL
),
with_comp AS (
  SELECT *, 0.4*nsales + 0.35*nadopt + 0.25*nres AS composite_score
  FROM scaled
),
ranked AS (
  SELECT *,
    ROW_NUMBER() OVER (ORDER BY investment_priority_score ASC) AS rn_ips_asc,
    ROW_NUMBER() OVER (ORDER BY composite_score ASC) AS rn_comp_asc,
    COUNT(*) OVER () AS total_cnt
  FROM with_comp
),
flagged AS (
  SELECT *, CASE WHEN rn_ips_asc >= 0.7*total_cnt AND rn_comp_asc <= 0.5*total_cnt THEN 1 ELSE 0 END AS is_target
  FROM ranked
)
SELECT company_size_tier,
  COUNT(*) AS total_cnt,
  SUM(is_target) AS cohort_cnt,
  ROUND(100.0*SUM(is_target)/COUNT(*), 1) AS cohort_pct,
  AVG(CASE WHEN is_target=1 THEN customer_lifetime_value/NULLIF(acquisition_cost,0) END) AS cohort_avg_roi,
  AVG(CASE WHEN is_target=0 THEN customer_lifetime_value/NULLIF(acquisition_cost,0) END) AS noncohort_avg_roi,
  AVG(CASE WHEN is_target=1 THEN investment_priority_score END) AS cohort_avg_ips,
  AVG(CASE WHEN is_target=0 THEN investment_priority_score END) AS noncohort_avg_ips,
  AVG(CASE WHEN is_target=1 THEN customer_onboarding_score END) AS cohort_avg_onb,
  AVG(CASE WHEN is_target=0 THEN customer_onboarding_score END) AS noncohort_avg_onb
FROM flagged
WHERE company_size_tier IS NOT NULL
GROUP BY company_size_tier
ORDER BY cohort_cnt DESC
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-055/attempt-01/sql/S53.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-055/attempt-01/sql/S53.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-055/attempt-01/results/S53.rows.jsonl)；完整：True；SHA256：`3ac74e562df660a17021e2edade9b1266dd811533cafaeb98f8ce97f00acb286`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "customer360__customer_value_analysis", "kind": "base", "block": null, "base_tables": ["customer360__customer_value_analysis"]}] | [] | [] |
| B2 | [{"alias": "customer360__customer", "kind": "base", "block": null, "base_tables": ["customer360__customer"]}] | [] | ["email"] |
| B3 | [{"alias": "v", "kind": "derived", "block": "B1", "base_tables": ["customer360__customer_value_analysis"]}, {"alias": "c_sales", "kind": "derived", "block": "B2", "base_tables": ["customer360__customer"]}] | [{"type": "LEFT", "right": "(SELECT email, MAX(total_sales_amount) AS total_sales_amount FROM customer360__customer WHERE NOT total_sales_amount IS NULL GROUP BY email) AS c_sales", "on": "v.primary_email = c_sales.email", "using": []}] | [] |
| B4 | [{"alias": "base", "kind": "derived", "block": "B3", "base_tables": ["customer360__customer", "customer360__customer_value_analysis"]}] | [] | [] |
| B5 | [{"alias": "base", "kind": "derived", "block": "B3", "base_tables": ["customer360__customer", "customer360__customer_value_analysis"]}] | [] | [] |
| B6 | [{"alias": "base", "kind": "derived", "block": "B3", "base_tables": ["customer360__customer", "customer360__customer_value_analysis"]}] | [] | [] |
| B7 | [{"alias": "base", "kind": "derived", "block": "B3", "base_tables": ["customer360__customer", "customer360__customer_value_analysis"]}] | [] | [] |
| B8 | [{"alias": "base", "kind": "derived", "block": "B3", "base_tables": ["customer360__customer", "customer360__customer_value_analysis"]}] | [] | [] |
| B9 | [{"alias": "base", "kind": "derived", "block": "B3", "base_tables": ["customer360__customer", "customer360__customer_value_analysis"]}] | [] | [] |
| B10 | [{"alias": "base", "kind": "derived", "block": "B3", "base_tables": ["customer360__customer", "customer360__customer_value_analysis"]}] | [] | [] |
| B11 | [{"alias": "scaled", "kind": "derived", "block": "B10", "base_tables": ["customer360__customer", "customer360__customer_value_analysis"]}] | [] | [] |
| B12 | [{"alias": "with_comp", "kind": "derived", "block": "B11", "base_tables": ["customer360__customer", "customer360__customer_value_analysis"]}] | [] | [] |
| B13 | [{"alias": "ranked", "kind": "derived", "block": "B12", "base_tables": ["customer360__customer", "customer360__customer_value_analysis"]}] | [] | [] |
| B14 | [{"alias": "flagged", "kind": "derived", "block": "B13", "base_tables": ["customer360__customer", "customer360__customer_value_analysis"]}] | [] | ["company_size_tier"] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B2 | MAX(total_sales_amount) | [{"table": "customer360__customer", "column": "total_sales_amount"}] | [] | False |
| B4 | MIN(total_sales_amount) | [{"table": "customer360__customer", "column": "total_sales_amount"}] | [] | False |
| B5 | MAX(total_sales_amount) | [{"table": "customer360__customer", "column": "total_sales_amount"}] | [] | False |
| B5 | MIN(total_sales_amount) | [{"table": "customer360__customer", "column": "total_sales_amount"}] | [] | False |
| B6 | MIN(product_adoption_rate) | [{"table": "customer360__customer_value_analysis", "column": "product_adoption_rate"}] | [] | False |
| B7 | MAX(product_adoption_rate) | [{"table": "customer360__customer_value_analysis", "column": "product_adoption_rate"}] | [] | False |
| B7 | MIN(product_adoption_rate) | [{"table": "customer360__customer_value_analysis", "column": "product_adoption_rate"}] | [] | False |
| B8 | MIN(support_resolution_efficiency) | [{"table": "customer360__customer_value_analysis", "column": "support_resolution_efficiency"}] | [] | False |
| B9 | MAX(support_resolution_efficiency) | [{"table": "customer360__customer_value_analysis", "column": "support_resolution_efficiency"}] | [] | False |
| B9 | MIN(support_resolution_efficiency) | [{"table": "customer360__customer_value_analysis", "column": "support_resolution_efficiency"}] | [] | False |
| B14 | COUNT(*) | [] | [] | True |
| B14 | SUM(is_target) | [{"table": "customer360__customer_value_analysis", "column": "investment_priority_score"}, {"table": "customer360__customer_value_analysis", "column": "support_resolution_efficiency"}, {"table": "customer360__customer_value_analysis", "column": "support_resolution_efficiency"}, {"table": "customer360__customer_value_analysis", "column": "support_resolution_efficiency"}, {"table": "customer360__customer_value_analysis", "column": "support_resolution_efficiency"}, {"table": "customer360__customer", "column": "total_sales_amount"}, {"table": "customer360__customer", "column": "total_sales_amount"}, {"table": "customer360__customer", "column": "total_sales_amount"}, {"table": "customer360__customer", "column": "total_sales_amount"}, {"table": "customer360__customer_value_analysis", "column": "product_adoption_rate"}, {"table": "customer360__customer_value_analysis", "column": "product_adoption_rate"}, {"table": "customer360__customer_value_analysis", "column": "product_adoption_rate"}, {"table": "customer360__customer_value_analysis", "column": "product_adoption_rate"}] | [] | False |
| B14 | AVG(CASE WHEN is_target = 1 THEN customer_lifetime_value / NULLIF(acquisition_cost, 0) END) | [{"table": "customer360__customer_value_analysis", "column": "customer_lifetime_value"}, {"table": "customer360__customer_value_analysis", "column": "acquisition_cost"}] | [{"table": "customer360__customer_value_analysis", "column": "investment_priority_score"}, {"table": "customer360__customer_value_analysis", "column": "support_resolution_efficiency"}, {"table": "customer360__customer_value_analysis", "column": "support_resolution_efficiency"}, {"table": "customer360__customer_value_analysis", "column": "support_resolution_efficiency"}, {"table": "customer360__customer_value_analysis", "column": "support_resolution_efficiency"}, {"table": "customer360__customer", "column": "total_sales_amount"}, {"table": "customer360__customer", "column": "total_sales_amount"}, {"table": "customer360__customer", "column": "total_sales_amount"}, {"table": "customer360__customer", "column": "total_sales_amount"}, {"table": "customer360__customer_value_analysis", "column": "product_adoption_rate"}, {"table": "customer360__customer_value_analysis", "column": "product_adoption_rate"}, {"table": "customer360__customer_value_analysis", "column": "product_adoption_rate"}, {"table": "customer360__customer_value_analysis", "column": "product_adoption_rate"}] | False |
| B14 | AVG(CASE WHEN is_target = 0 THEN customer_lifetime_value / NULLIF(acquisition_cost, 0) END) | [{"table": "customer360__customer_value_analysis", "column": "customer_lifetime_value"}, {"table": "customer360__customer_value_analysis", "column": "acquisition_cost"}] | [{"table": "customer360__customer_value_analysis", "column": "investment_priority_score"}, {"table": "customer360__customer_value_analysis", "column": "support_resolution_efficiency"}, {"table": "customer360__customer_value_analysis", "column": "support_resolution_efficiency"}, {"table": "customer360__customer_value_analysis", "column": "support_resolution_efficiency"}, {"table": "customer360__customer_value_analysis", "column": "support_resolution_efficiency"}, {"table": "customer360__customer", "column": "total_sales_amount"}, {"table": "customer360__customer", "column": "total_sales_amount"}, {"table": "customer360__customer", "column": "total_sales_amount"}, {"table": "customer360__customer", "column": "total_sales_amount"}, {"table": "customer360__customer_value_analysis", "column": "product_adoption_rate"}, {"table": "customer360__customer_value_analysis", "column": "product_adoption_rate"}, {"table": "customer360__customer_value_analysis", "column": "product_adoption_rate"}, {"table": "customer360__customer_value_analysis", "column": "product_adoption_rate"}] | False |
| B14 | AVG(CASE WHEN is_target = 1 THEN investment_priority_score END) | [{"table": "customer360__customer_value_analysis", "column": "investment_priority_score"}] | [{"table": "customer360__customer_value_analysis", "column": "investment_priority_score"}, {"table": "customer360__customer_value_analysis", "column": "support_resolution_efficiency"}, {"table": "customer360__customer_value_analysis", "column": "support_resolution_efficiency"}, {"table": "customer360__customer_value_analysis", "column": "support_resolution_efficiency"}, {"table": "customer360__customer_value_analysis", "column": "support_resolution_efficiency"}, {"table": "customer360__customer", "column": "total_sales_amount"}, {"table": "customer360__customer", "column": "total_sales_amount"}, {"table": "customer360__customer", "column": "total_sales_amount"}, {"table": "customer360__customer", "column": "total_sales_amount"}, {"table": "customer360__customer_value_analysis", "column": "product_adoption_rate"}, {"table": "customer360__customer_value_analysis", "column": "product_adoption_rate"}, {"table": "customer360__customer_value_analysis", "column": "product_adoption_rate"}, {"table": "customer360__customer_value_analysis", "column": "product_adoption_rate"}] | False |
| B14 | AVG(CASE WHEN is_target = 0 THEN investment_priority_score END) | [{"table": "customer360__customer_value_analysis", "column": "investment_priority_score"}] | [{"table": "customer360__customer_value_analysis", "column": "investment_priority_score"}, {"table": "customer360__customer_value_analysis", "column": "support_resolution_efficiency"}, {"table": "customer360__customer_value_analysis", "column": "support_resolution_efficiency"}, {"table": "customer360__customer_value_analysis", "column": "support_resolution_efficiency"}, {"table": "customer360__customer_value_analysis", "column": "support_resolution_efficiency"}, {"table": "customer360__customer", "column": "total_sales_amount"}, {"table": "customer360__customer", "column": "total_sales_amount"}, {"table": "customer360__customer", "column": "total_sales_amount"}, {"table": "customer360__customer", "column": "total_sales_amount"}, {"table": "customer360__customer_value_analysis", "column": "product_adoption_rate"}, {"table": "customer360__customer_value_analysis", "column": "product_adoption_rate"}, {"table": "customer360__customer_value_analysis", "column": "product_adoption_rate"}, {"table": "customer360__customer_value_analysis", "column": "product_adoption_rate"}] | False |
| B14 | AVG(CASE WHEN is_target = 1 THEN customer_onboarding_score END) | [{"table": "customer360__customer_value_analysis", "column": "customer_onboarding_score"}] | [{"table": "customer360__customer_value_analysis", "column": "investment_priority_score"}, {"table": "customer360__customer_value_analysis", "column": "support_resolution_efficiency"}, {"table": "customer360__customer_value_analysis", "column": "support_resolution_efficiency"}, {"table": "customer360__customer_value_analysis", "column": "support_resolution_efficiency"}, {"table": "customer360__customer_value_analysis", "column": "support_resolution_efficiency"}, {"table": "customer360__customer", "column": "total_sales_amount"}, {"table": "customer360__customer", "column": "total_sales_amount"}, {"table": "customer360__customer", "column": "total_sales_amount"}, {"table": "customer360__customer", "column": "total_sales_amount"}, {"table": "customer360__customer_value_analysis", "column": "product_adoption_rate"}, {"table": "customer360__customer_value_analysis", "column": "product_adoption_rate"}, {"table": "customer360__customer_value_analysis", "column": "product_adoption_rate"}, {"table": "customer360__customer_value_analysis", "column": "product_adoption_rate"}] | False |
| B14 | AVG(CASE WHEN is_target = 0 THEN customer_onboarding_score END) | [{"table": "customer360__customer_value_analysis", "column": "customer_onboarding_score"}] | [{"table": "customer360__customer_value_analysis", "column": "investment_priority_score"}, {"table": "customer360__customer_value_analysis", "column": "support_resolution_efficiency"}, {"table": "customer360__customer_value_analysis", "column": "support_resolution_efficiency"}, {"table": "customer360__customer_value_analysis", "column": "support_resolution_efficiency"}, {"table": "customer360__customer_value_analysis", "column": "support_resolution_efficiency"}, {"table": "customer360__customer", "column": "total_sales_amount"}, {"table": "customer360__customer", "column": "total_sales_amount"}, {"table": "customer360__customer", "column": "total_sales_amount"}, {"table": "customer360__customer", "column": "total_sales_amount"}, {"table": "customer360__customer_value_analysis", "column": "product_adoption_rate"}, {"table": "customer360__customer_value_analysis", "column": "product_adoption_rate"}, {"table": "customer360__customer_value_analysis", "column": "product_adoption_rate"}, {"table": "customer360__customer_value_analysis", "column": "product_adoption_rate"}] | False |
| B14 | COUNT(*) | [] | [] | True |
| B14 | SUM(is_target) | [{"table": "customer360__customer_value_analysis", "column": "investment_priority_score"}, {"table": "customer360__customer_value_analysis", "column": "support_resolution_efficiency"}, {"table": "customer360__customer_value_analysis", "column": "support_resolution_efficiency"}, {"table": "customer360__customer_value_analysis", "column": "support_resolution_efficiency"}, {"table": "customer360__customer_value_analysis", "column": "support_resolution_efficiency"}, {"table": "customer360__customer", "column": "total_sales_amount"}, {"table": "customer360__customer", "column": "total_sales_amount"}, {"table": "customer360__customer", "column": "total_sales_amount"}, {"table": "customer360__customer", "column": "total_sales_amount"}, {"table": "customer360__customer_value_analysis", "column": "product_adoption_rate"}, {"table": "customer360__customer_value_analysis", "column": "product_adoption_rate"}, {"table": "customer360__customer_value_analysis", "column": "product_adoption_rate"}, {"table": "customer360__customer_value_analysis", "column": "product_adoption_rate"}] | [] | False |


## S54

类别 `data`；来源 `query_db`；调用 `9071a49534ab45788752e70c655db64e`；状态 `success`。

```sql
WITH base AS (
  SELECT DISTINCT v.primary_email, v.investment_priority_score, v.product_adoption_rate,
    v.support_resolution_efficiency, v.acquisition_cost, v.customer_lifetime_value,
    v.lifecycle_stage, v.industry_vertical, v.company_size_tier,
    v.customer_onboarding_score, v.team_size, v.decision_maker_level,
    v.digital_engagement_score, v.nps_score, v.customer_health_score, v.churn_probability,
    c_sales.total_sales_amount
  FROM (
    SELECT DISTINCT * FROM customer360__customer_value_analysis
  ) v
  LEFT JOIN (
    SELECT email, MAX(total_sales_amount) AS total_sales_amount
    FROM customer360__customer
    WHERE total_sales_amount IS NOT NULL
    GROUP BY email
  ) c_sales ON v.primary_email = c_sales.email
  WHERE v.primary_email IS NOT NULL
),
scaled AS (
  SELECT *,
    (total_sales_amount - (SELECT MIN(total_sales_amount) FROM base)) / 
      NULLIF((SELECT MAX(total_sales_amount) - MIN(total_sales_amount) FROM base), 0) AS nsales,
    (product_adoption_rate - (SELECT MIN(product_adoption_rate) FROM base)) / 
      NULLIF((SELECT MAX(product_adoption_rate) - MIN(product_adoption_rate) FROM base), 0) AS nadopt,
    (support_resolution_efficiency - (SELECT MIN(support_resolution_efficiency) FROM base)) / 
      NULLIF((SELECT MAX(support_resolution_efficiency) - MIN(support_resolution_efficiency) FROM base), 0) AS nres
  FROM base
  WHERE product_adoption_rate IS NOT NULL AND support_resolution_efficiency IS NOT NULL
    AND total_sales_amount IS NOT NULL AND acquisition_cost IS NOT NULL AND customer_lifetime_value IS NOT NULL
),
with_comp AS (
  SELECT *, 0.4*nsales + 0.35*nadopt + 0.25*nres AS composite_score
  FROM scaled
),
ranked AS (
  SELECT *,
    ROW_NUMBER() OVER (ORDER BY investment_priority_score ASC) AS rn_ips_asc,
    ROW_NUMBER() OVER (ORDER BY composite_score ASC) AS rn_comp_asc,
    COUNT(*) OVER () AS total_cnt
  FROM with_comp
),
flagged AS (
  SELECT *, CASE WHEN rn_ips_asc >= 0.7*total_cnt AND rn_comp_asc <= 0.5*total_cnt THEN 1 ELSE 0 END AS is_target
  FROM ranked
)
SELECT decision_maker_level,
  COUNT(*) AS total_cnt,
  SUM(is_target) AS cohort_cnt,
  ROUND(100.0*SUM(is_target)/COUNT(*), 1) AS cohort_pct,
  AVG(CASE WHEN is_target=1 THEN customer_lifetime_value/NULLIF(acquisition_cost,0) END) AS cohort_avg_roi,
  AVG(CASE WHEN is_target=0 THEN customer_lifetime_value/NULLIF(acquisition_cost,0) END) AS noncohort_avg_roi,
  AVG(CASE WHEN is_target=1 THEN product_adoption_rate END) AS cohort_avg_par,
  AVG(CASE WHEN is_target=0 THEN product_adoption_rate END) AS noncohort_avg_par,
  AVG(CASE WHEN is_target=1 THEN customer_onboarding_score END) AS cohort_avg_onb,
  AVG(CASE WHEN is_target=0 THEN customer_onboarding_score END) AS noncohort_avg_onb
FROM flagged
WHERE decision_maker_level IS NOT NULL
GROUP BY decision_maker_level
ORDER BY cohort_cnt DESC
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-055/attempt-01/sql/S54.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-055/attempt-01/sql/S54.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-055/attempt-01/results/S54.rows.jsonl)；完整：True；SHA256：`29704d3738b00345cad7cfff4c5df44f5e96a0a30288c9744134fb36414395ae`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "customer360__customer_value_analysis", "kind": "base", "block": null, "base_tables": ["customer360__customer_value_analysis"]}] | [] | [] |
| B2 | [{"alias": "customer360__customer", "kind": "base", "block": null, "base_tables": ["customer360__customer"]}] | [] | ["email"] |
| B3 | [{"alias": "v", "kind": "derived", "block": "B1", "base_tables": ["customer360__customer_value_analysis"]}, {"alias": "c_sales", "kind": "derived", "block": "B2", "base_tables": ["customer360__customer"]}] | [{"type": "LEFT", "right": "(SELECT email, MAX(total_sales_amount) AS total_sales_amount FROM customer360__customer WHERE NOT total_sales_amount IS NULL GROUP BY email) AS c_sales", "on": "v.primary_email = c_sales.email", "using": []}] | [] |
| B4 | [{"alias": "base", "kind": "derived", "block": "B3", "base_tables": ["customer360__customer", "customer360__customer_value_analysis"]}] | [] | [] |
| B5 | [{"alias": "base", "kind": "derived", "block": "B3", "base_tables": ["customer360__customer", "customer360__customer_value_analysis"]}] | [] | [] |
| B6 | [{"alias": "base", "kind": "derived", "block": "B3", "base_tables": ["customer360__customer", "customer360__customer_value_analysis"]}] | [] | [] |
| B7 | [{"alias": "base", "kind": "derived", "block": "B3", "base_tables": ["customer360__customer", "customer360__customer_value_analysis"]}] | [] | [] |
| B8 | [{"alias": "base", "kind": "derived", "block": "B3", "base_tables": ["customer360__customer", "customer360__customer_value_analysis"]}] | [] | [] |
| B9 | [{"alias": "base", "kind": "derived", "block": "B3", "base_tables": ["customer360__customer", "customer360__customer_value_analysis"]}] | [] | [] |
| B10 | [{"alias": "base", "kind": "derived", "block": "B3", "base_tables": ["customer360__customer", "customer360__customer_value_analysis"]}] | [] | [] |
| B11 | [{"alias": "scaled", "kind": "derived", "block": "B10", "base_tables": ["customer360__customer", "customer360__customer_value_analysis"]}] | [] | [] |
| B12 | [{"alias": "with_comp", "kind": "derived", "block": "B11", "base_tables": ["customer360__customer", "customer360__customer_value_analysis"]}] | [] | [] |
| B13 | [{"alias": "ranked", "kind": "derived", "block": "B12", "base_tables": ["customer360__customer", "customer360__customer_value_analysis"]}] | [] | [] |
| B14 | [{"alias": "flagged", "kind": "derived", "block": "B13", "base_tables": ["customer360__customer", "customer360__customer_value_analysis"]}] | [] | ["decision_maker_level"] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B2 | MAX(total_sales_amount) | [{"table": "customer360__customer", "column": "total_sales_amount"}] | [] | False |
| B4 | MIN(total_sales_amount) | [{"table": "customer360__customer", "column": "total_sales_amount"}] | [] | False |
| B5 | MAX(total_sales_amount) | [{"table": "customer360__customer", "column": "total_sales_amount"}] | [] | False |
| B5 | MIN(total_sales_amount) | [{"table": "customer360__customer", "column": "total_sales_amount"}] | [] | False |
| B6 | MIN(product_adoption_rate) | [{"table": "customer360__customer_value_analysis", "column": "product_adoption_rate"}] | [] | False |
| B7 | MAX(product_adoption_rate) | [{"table": "customer360__customer_value_analysis", "column": "product_adoption_rate"}] | [] | False |
| B7 | MIN(product_adoption_rate) | [{"table": "customer360__customer_value_analysis", "column": "product_adoption_rate"}] | [] | False |
| B8 | MIN(support_resolution_efficiency) | [{"table": "customer360__customer_value_analysis", "column": "support_resolution_efficiency"}] | [] | False |
| B9 | MAX(support_resolution_efficiency) | [{"table": "customer360__customer_value_analysis", "column": "support_resolution_efficiency"}] | [] | False |
| B9 | MIN(support_resolution_efficiency) | [{"table": "customer360__customer_value_analysis", "column": "support_resolution_efficiency"}] | [] | False |
| B14 | COUNT(*) | [] | [] | True |
| B14 | SUM(is_target) | [{"table": "customer360__customer_value_analysis", "column": "investment_priority_score"}, {"table": "customer360__customer_value_analysis", "column": "support_resolution_efficiency"}, {"table": "customer360__customer_value_analysis", "column": "support_resolution_efficiency"}, {"table": "customer360__customer_value_analysis", "column": "support_resolution_efficiency"}, {"table": "customer360__customer_value_analysis", "column": "support_resolution_efficiency"}, {"table": "customer360__customer", "column": "total_sales_amount"}, {"table": "customer360__customer", "column": "total_sales_amount"}, {"table": "customer360__customer", "column": "total_sales_amount"}, {"table": "customer360__customer", "column": "total_sales_amount"}, {"table": "customer360__customer_value_analysis", "column": "product_adoption_rate"}, {"table": "customer360__customer_value_analysis", "column": "product_adoption_rate"}, {"table": "customer360__customer_value_analysis", "column": "product_adoption_rate"}, {"table": "customer360__customer_value_analysis", "column": "product_adoption_rate"}] | [] | False |
| B14 | AVG(CASE WHEN is_target = 1 THEN customer_lifetime_value / NULLIF(acquisition_cost, 0) END) | [{"table": "customer360__customer_value_analysis", "column": "customer_lifetime_value"}, {"table": "customer360__customer_value_analysis", "column": "acquisition_cost"}] | [{"table": "customer360__customer_value_analysis", "column": "investment_priority_score"}, {"table": "customer360__customer_value_analysis", "column": "support_resolution_efficiency"}, {"table": "customer360__customer_value_analysis", "column": "support_resolution_efficiency"}, {"table": "customer360__customer_value_analysis", "column": "support_resolution_efficiency"}, {"table": "customer360__customer_value_analysis", "column": "support_resolution_efficiency"}, {"table": "customer360__customer", "column": "total_sales_amount"}, {"table": "customer360__customer", "column": "total_sales_amount"}, {"table": "customer360__customer", "column": "total_sales_amount"}, {"table": "customer360__customer", "column": "total_sales_amount"}, {"table": "customer360__customer_value_analysis", "column": "product_adoption_rate"}, {"table": "customer360__customer_value_analysis", "column": "product_adoption_rate"}, {"table": "customer360__customer_value_analysis", "column": "product_adoption_rate"}, {"table": "customer360__customer_value_analysis", "column": "product_adoption_rate"}] | False |
| B14 | AVG(CASE WHEN is_target = 0 THEN customer_lifetime_value / NULLIF(acquisition_cost, 0) END) | [{"table": "customer360__customer_value_analysis", "column": "customer_lifetime_value"}, {"table": "customer360__customer_value_analysis", "column": "acquisition_cost"}] | [{"table": "customer360__customer_value_analysis", "column": "investment_priority_score"}, {"table": "customer360__customer_value_analysis", "column": "support_resolution_efficiency"}, {"table": "customer360__customer_value_analysis", "column": "support_resolution_efficiency"}, {"table": "customer360__customer_value_analysis", "column": "support_resolution_efficiency"}, {"table": "customer360__customer_value_analysis", "column": "support_resolution_efficiency"}, {"table": "customer360__customer", "column": "total_sales_amount"}, {"table": "customer360__customer", "column": "total_sales_amount"}, {"table": "customer360__customer", "column": "total_sales_amount"}, {"table": "customer360__customer", "column": "total_sales_amount"}, {"table": "customer360__customer_value_analysis", "column": "product_adoption_rate"}, {"table": "customer360__customer_value_analysis", "column": "product_adoption_rate"}, {"table": "customer360__customer_value_analysis", "column": "product_adoption_rate"}, {"table": "customer360__customer_value_analysis", "column": "product_adoption_rate"}] | False |
| B14 | AVG(CASE WHEN is_target = 1 THEN product_adoption_rate END) | [{"table": "customer360__customer_value_analysis", "column": "product_adoption_rate"}] | [{"table": "customer360__customer_value_analysis", "column": "investment_priority_score"}, {"table": "customer360__customer_value_analysis", "column": "support_resolution_efficiency"}, {"table": "customer360__customer_value_analysis", "column": "support_resolution_efficiency"}, {"table": "customer360__customer_value_analysis", "column": "support_resolution_efficiency"}, {"table": "customer360__customer_value_analysis", "column": "support_resolution_efficiency"}, {"table": "customer360__customer", "column": "total_sales_amount"}, {"table": "customer360__customer", "column": "total_sales_amount"}, {"table": "customer360__customer", "column": "total_sales_amount"}, {"table": "customer360__customer", "column": "total_sales_amount"}, {"table": "customer360__customer_value_analysis", "column": "product_adoption_rate"}, {"table": "customer360__customer_value_analysis", "column": "product_adoption_rate"}, {"table": "customer360__customer_value_analysis", "column": "product_adoption_rate"}, {"table": "customer360__customer_value_analysis", "column": "product_adoption_rate"}] | False |
| B14 | AVG(CASE WHEN is_target = 0 THEN product_adoption_rate END) | [{"table": "customer360__customer_value_analysis", "column": "product_adoption_rate"}] | [{"table": "customer360__customer_value_analysis", "column": "investment_priority_score"}, {"table": "customer360__customer_value_analysis", "column": "support_resolution_efficiency"}, {"table": "customer360__customer_value_analysis", "column": "support_resolution_efficiency"}, {"table": "customer360__customer_value_analysis", "column": "support_resolution_efficiency"}, {"table": "customer360__customer_value_analysis", "column": "support_resolution_efficiency"}, {"table": "customer360__customer", "column": "total_sales_amount"}, {"table": "customer360__customer", "column": "total_sales_amount"}, {"table": "customer360__customer", "column": "total_sales_amount"}, {"table": "customer360__customer", "column": "total_sales_amount"}, {"table": "customer360__customer_value_analysis", "column": "product_adoption_rate"}, {"table": "customer360__customer_value_analysis", "column": "product_adoption_rate"}, {"table": "customer360__customer_value_analysis", "column": "product_adoption_rate"}, {"table": "customer360__customer_value_analysis", "column": "product_adoption_rate"}] | False |
| B14 | AVG(CASE WHEN is_target = 1 THEN customer_onboarding_score END) | [{"table": "customer360__customer_value_analysis", "column": "customer_onboarding_score"}] | [{"table": "customer360__customer_value_analysis", "column": "investment_priority_score"}, {"table": "customer360__customer_value_analysis", "column": "support_resolution_efficiency"}, {"table": "customer360__customer_value_analysis", "column": "support_resolution_efficiency"}, {"table": "customer360__customer_value_analysis", "column": "support_resolution_efficiency"}, {"table": "customer360__customer_value_analysis", "column": "support_resolution_efficiency"}, {"table": "customer360__customer", "column": "total_sales_amount"}, {"table": "customer360__customer", "column": "total_sales_amount"}, {"table": "customer360__customer", "column": "total_sales_amount"}, {"table": "customer360__customer", "column": "total_sales_amount"}, {"table": "customer360__customer_value_analysis", "column": "product_adoption_rate"}, {"table": "customer360__customer_value_analysis", "column": "product_adoption_rate"}, {"table": "customer360__customer_value_analysis", "column": "product_adoption_rate"}, {"table": "customer360__customer_value_analysis", "column": "product_adoption_rate"}] | False |
| B14 | AVG(CASE WHEN is_target = 0 THEN customer_onboarding_score END) | [{"table": "customer360__customer_value_analysis", "column": "customer_onboarding_score"}] | [{"table": "customer360__customer_value_analysis", "column": "investment_priority_score"}, {"table": "customer360__customer_value_analysis", "column": "support_resolution_efficiency"}, {"table": "customer360__customer_value_analysis", "column": "support_resolution_efficiency"}, {"table": "customer360__customer_value_analysis", "column": "support_resolution_efficiency"}, {"table": "customer360__customer_value_analysis", "column": "support_resolution_efficiency"}, {"table": "customer360__customer", "column": "total_sales_amount"}, {"table": "customer360__customer", "column": "total_sales_amount"}, {"table": "customer360__customer", "column": "total_sales_amount"}, {"table": "customer360__customer", "column": "total_sales_amount"}, {"table": "customer360__customer_value_analysis", "column": "product_adoption_rate"}, {"table": "customer360__customer_value_analysis", "column": "product_adoption_rate"}, {"table": "customer360__customer_value_analysis", "column": "product_adoption_rate"}, {"table": "customer360__customer_value_analysis", "column": "product_adoption_rate"}] | False |
| B14 | COUNT(*) | [] | [] | True |
| B14 | SUM(is_target) | [{"table": "customer360__customer_value_analysis", "column": "investment_priority_score"}, {"table": "customer360__customer_value_analysis", "column": "support_resolution_efficiency"}, {"table": "customer360__customer_value_analysis", "column": "support_resolution_efficiency"}, {"table": "customer360__customer_value_analysis", "column": "support_resolution_efficiency"}, {"table": "customer360__customer_value_analysis", "column": "support_resolution_efficiency"}, {"table": "customer360__customer", "column": "total_sales_amount"}, {"table": "customer360__customer", "column": "total_sales_amount"}, {"table": "customer360__customer", "column": "total_sales_amount"}, {"table": "customer360__customer", "column": "total_sales_amount"}, {"table": "customer360__customer_value_analysis", "column": "product_adoption_rate"}, {"table": "customer360__customer_value_analysis", "column": "product_adoption_rate"}, {"table": "customer360__customer_value_analysis", "column": "product_adoption_rate"}, {"table": "customer360__customer_value_analysis", "column": "product_adoption_rate"}] | [] | False |


## S55

类别 `data`；来源 `query_db`；调用 `e0d09d03a1214a7c85488ea67472f30f`；状态 `success`。

```sql
WITH base AS (
  SELECT DISTINCT v.primary_email, v.investment_priority_score, v.product_adoption_rate,
    v.support_resolution_efficiency, v.acquisition_cost, v.customer_lifetime_value,
    v.lifecycle_stage, v.industry_vertical, v.company_size_tier,
    v.customer_onboarding_score, v.team_size, v.decision_maker_level,
    v.digital_engagement_score, v.nps_score, v.customer_health_score, v.churn_probability,
    c_sales.total_sales_amount
  FROM (
    SELECT DISTINCT * FROM customer360__customer_value_analysis
  ) v
  LEFT JOIN (
    SELECT email, MAX(total_sales_amount) AS total_sales_amount
    FROM customer360__customer
    WHERE total_sales_amount IS NOT NULL
    GROUP BY email
  ) c_sales ON v.primary_email = c_sales.email
  WHERE v.primary_email IS NOT NULL
),
scaled AS (
  SELECT *,
    (total_sales_amount - (SELECT MIN(total_sales_amount) FROM base)) / 
      NULLIF((SELECT MAX(total_sales_amount) - MIN(total_sales_amount) FROM base), 0) AS nsales,
    (product_adoption_rate - (SELECT MIN(product_adoption_rate) FROM base)) / 
      NULLIF((SELECT MAX(product_adoption_rate) - MIN(product_adoption_rate) FROM base), 0) AS nadopt,
    (support_resolution_efficiency - (SELECT MIN(support_resolution_efficiency) FROM base)) / 
      NULLIF((SELECT MAX(support_resolution_efficiency) - MIN(support_resolution_efficiency) FROM base), 0) AS nres
  FROM base
  WHERE product_adoption_rate IS NOT NULL AND support_resolution_efficiency IS NOT NULL
    AND total_sales_amount IS NOT NULL AND acquisition_cost IS NOT NULL AND customer_lifetime_value IS NOT NULL
),
with_comp AS (
  SELECT *, 0.4*nsales + 0.35*nadopt + 0.25*nres AS composite_score
  FROM scaled
),
ranked AS (
  SELECT *,
    ROW_NUMBER() OVER (ORDER BY investment_priority_score ASC) AS rn_ips_asc,
    ROW_NUMBER() OVER (ORDER BY composite_score ASC) AS rn_comp_asc,
    COUNT(*) OVER () AS total_cnt
  FROM with_comp
),
flagged AS (
  SELECT *, CASE WHEN rn_ips_asc >= 0.7*total_cnt AND rn_comp_asc <= 0.5*total_cnt THEN 1 ELSE 0 END AS is_target,
    CASE WHEN team_size <= 2 THEN '1-2' WHEN team_size <= 5 THEN '3-5' WHEN team_size <= 10 THEN '6-10' WHEN team_size <= 20 THEN '11-20' ELSE '20+' END AS team_bucket
  FROM ranked
)
SELECT team_bucket,
  COUNT(*) AS total_cnt,
  SUM(is_target) AS cohort_cnt,
  ROUND(100.0*SUM(is_target)/COUNT(*), 1) AS cohort_pct,
  AVG(CASE WHEN is_target=1 THEN customer_lifetime_value/NULLIF(acquisition_cost,0) END) AS cohort_avg_roi,
  AVG(CASE WHEN is_target=0 THEN customer_lifetime_value/NULLIF(acquisition_cost,0) END) AS noncohort_avg_roi,
  AVG(CASE WHEN is_target=1 THEN product_adoption_rate END) AS cohort_avg_par,
  AVG(CASE WHEN is_target=0 THEN product_adoption_rate END) AS noncohort_avg_par
FROM flagged
WHERE team_size IS NOT NULL
GROUP BY team_bucket
ORDER BY MIN(team_size)
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-055/attempt-01/sql/S55.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-055/attempt-01/sql/S55.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-055/attempt-01/results/S55.rows.jsonl)；完整：True；SHA256：`34a6dcae33c58f94c77d498e37b586386d6aae0394e6cf666e6d1c825af1e983`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "customer360__customer_value_analysis", "kind": "base", "block": null, "base_tables": ["customer360__customer_value_analysis"]}] | [] | [] |
| B2 | [{"alias": "customer360__customer", "kind": "base", "block": null, "base_tables": ["customer360__customer"]}] | [] | ["email"] |
| B3 | [{"alias": "v", "kind": "derived", "block": "B1", "base_tables": ["customer360__customer_value_analysis"]}, {"alias": "c_sales", "kind": "derived", "block": "B2", "base_tables": ["customer360__customer"]}] | [{"type": "LEFT", "right": "(SELECT email, MAX(total_sales_amount) AS total_sales_amount FROM customer360__customer WHERE NOT total_sales_amount IS NULL GROUP BY email) AS c_sales", "on": "v.primary_email = c_sales.email", "using": []}] | [] |
| B4 | [{"alias": "base", "kind": "derived", "block": "B3", "base_tables": ["customer360__customer", "customer360__customer_value_analysis"]}] | [] | [] |
| B5 | [{"alias": "base", "kind": "derived", "block": "B3", "base_tables": ["customer360__customer", "customer360__customer_value_analysis"]}] | [] | [] |
| B6 | [{"alias": "base", "kind": "derived", "block": "B3", "base_tables": ["customer360__customer", "customer360__customer_value_analysis"]}] | [] | [] |
| B7 | [{"alias": "base", "kind": "derived", "block": "B3", "base_tables": ["customer360__customer", "customer360__customer_value_analysis"]}] | [] | [] |
| B8 | [{"alias": "base", "kind": "derived", "block": "B3", "base_tables": ["customer360__customer", "customer360__customer_value_analysis"]}] | [] | [] |
| B9 | [{"alias": "base", "kind": "derived", "block": "B3", "base_tables": ["customer360__customer", "customer360__customer_value_analysis"]}] | [] | [] |
| B10 | [{"alias": "base", "kind": "derived", "block": "B3", "base_tables": ["customer360__customer", "customer360__customer_value_analysis"]}] | [] | [] |
| B11 | [{"alias": "scaled", "kind": "derived", "block": "B10", "base_tables": ["customer360__customer", "customer360__customer_value_analysis"]}] | [] | [] |
| B12 | [{"alias": "with_comp", "kind": "derived", "block": "B11", "base_tables": ["customer360__customer", "customer360__customer_value_analysis"]}] | [] | [] |
| B13 | [{"alias": "ranked", "kind": "derived", "block": "B12", "base_tables": ["customer360__customer", "customer360__customer_value_analysis"]}] | [] | [] |
| B14 | [{"alias": "flagged", "kind": "derived", "block": "B13", "base_tables": ["customer360__customer", "customer360__customer_value_analysis"]}] | [] | ["team_bucket"] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B2 | MAX(total_sales_amount) | [{"table": "customer360__customer", "column": "total_sales_amount"}] | [] | False |
| B4 | MIN(total_sales_amount) | [{"table": "customer360__customer", "column": "total_sales_amount"}] | [] | False |
| B5 | MAX(total_sales_amount) | [{"table": "customer360__customer", "column": "total_sales_amount"}] | [] | False |
| B5 | MIN(total_sales_amount) | [{"table": "customer360__customer", "column": "total_sales_amount"}] | [] | False |
| B6 | MIN(product_adoption_rate) | [{"table": "customer360__customer_value_analysis", "column": "product_adoption_rate"}] | [] | False |
| B7 | MAX(product_adoption_rate) | [{"table": "customer360__customer_value_analysis", "column": "product_adoption_rate"}] | [] | False |
| B7 | MIN(product_adoption_rate) | [{"table": "customer360__customer_value_analysis", "column": "product_adoption_rate"}] | [] | False |
| B8 | MIN(support_resolution_efficiency) | [{"table": "customer360__customer_value_analysis", "column": "support_resolution_efficiency"}] | [] | False |
| B9 | MAX(support_resolution_efficiency) | [{"table": "customer360__customer_value_analysis", "column": "support_resolution_efficiency"}] | [] | False |
| B9 | MIN(support_resolution_efficiency) | [{"table": "customer360__customer_value_analysis", "column": "support_resolution_efficiency"}] | [] | False |
| B14 | COUNT(*) | [] | [] | True |
| B14 | SUM(is_target) | [{"table": "customer360__customer_value_analysis", "column": "investment_priority_score"}, {"table": "customer360__customer_value_analysis", "column": "support_resolution_efficiency"}, {"table": "customer360__customer_value_analysis", "column": "support_resolution_efficiency"}, {"table": "customer360__customer_value_analysis", "column": "support_resolution_efficiency"}, {"table": "customer360__customer_value_analysis", "column": "support_resolution_efficiency"}, {"table": "customer360__customer", "column": "total_sales_amount"}, {"table": "customer360__customer", "column": "total_sales_amount"}, {"table": "customer360__customer", "column": "total_sales_amount"}, {"table": "customer360__customer", "column": "total_sales_amount"}, {"table": "customer360__customer_value_analysis", "column": "product_adoption_rate"}, {"table": "customer360__customer_value_analysis", "column": "product_adoption_rate"}, {"table": "customer360__customer_value_analysis", "column": "product_adoption_rate"}, {"table": "customer360__customer_value_analysis", "column": "product_adoption_rate"}] | [] | False |
| B14 | AVG(CASE WHEN is_target = 1 THEN customer_lifetime_value / NULLIF(acquisition_cost, 0) END) | [{"table": "customer360__customer_value_analysis", "column": "customer_lifetime_value"}, {"table": "customer360__customer_value_analysis", "column": "acquisition_cost"}] | [{"table": "customer360__customer_value_analysis", "column": "investment_priority_score"}, {"table": "customer360__customer_value_analysis", "column": "support_resolution_efficiency"}, {"table": "customer360__customer_value_analysis", "column": "support_resolution_efficiency"}, {"table": "customer360__customer_value_analysis", "column": "support_resolution_efficiency"}, {"table": "customer360__customer_value_analysis", "column": "support_resolution_efficiency"}, {"table": "customer360__customer", "column": "total_sales_amount"}, {"table": "customer360__customer", "column": "total_sales_amount"}, {"table": "customer360__customer", "column": "total_sales_amount"}, {"table": "customer360__customer", "column": "total_sales_amount"}, {"table": "customer360__customer_value_analysis", "column": "product_adoption_rate"}, {"table": "customer360__customer_value_analysis", "column": "product_adoption_rate"}, {"table": "customer360__customer_value_analysis", "column": "product_adoption_rate"}, {"table": "customer360__customer_value_analysis", "column": "product_adoption_rate"}] | False |
| B14 | AVG(CASE WHEN is_target = 0 THEN customer_lifetime_value / NULLIF(acquisition_cost, 0) END) | [{"table": "customer360__customer_value_analysis", "column": "customer_lifetime_value"}, {"table": "customer360__customer_value_analysis", "column": "acquisition_cost"}] | [{"table": "customer360__customer_value_analysis", "column": "investment_priority_score"}, {"table": "customer360__customer_value_analysis", "column": "support_resolution_efficiency"}, {"table": "customer360__customer_value_analysis", "column": "support_resolution_efficiency"}, {"table": "customer360__customer_value_analysis", "column": "support_resolution_efficiency"}, {"table": "customer360__customer_value_analysis", "column": "support_resolution_efficiency"}, {"table": "customer360__customer", "column": "total_sales_amount"}, {"table": "customer360__customer", "column": "total_sales_amount"}, {"table": "customer360__customer", "column": "total_sales_amount"}, {"table": "customer360__customer", "column": "total_sales_amount"}, {"table": "customer360__customer_value_analysis", "column": "product_adoption_rate"}, {"table": "customer360__customer_value_analysis", "column": "product_adoption_rate"}, {"table": "customer360__customer_value_analysis", "column": "product_adoption_rate"}, {"table": "customer360__customer_value_analysis", "column": "product_adoption_rate"}] | False |
| B14 | AVG(CASE WHEN is_target = 1 THEN product_adoption_rate END) | [{"table": "customer360__customer_value_analysis", "column": "product_adoption_rate"}] | [{"table": "customer360__customer_value_analysis", "column": "investment_priority_score"}, {"table": "customer360__customer_value_analysis", "column": "support_resolution_efficiency"}, {"table": "customer360__customer_value_analysis", "column": "support_resolution_efficiency"}, {"table": "customer360__customer_value_analysis", "column": "support_resolution_efficiency"}, {"table": "customer360__customer_value_analysis", "column": "support_resolution_efficiency"}, {"table": "customer360__customer", "column": "total_sales_amount"}, {"table": "customer360__customer", "column": "total_sales_amount"}, {"table": "customer360__customer", "column": "total_sales_amount"}, {"table": "customer360__customer", "column": "total_sales_amount"}, {"table": "customer360__customer_value_analysis", "column": "product_adoption_rate"}, {"table": "customer360__customer_value_analysis", "column": "product_adoption_rate"}, {"table": "customer360__customer_value_analysis", "column": "product_adoption_rate"}, {"table": "customer360__customer_value_analysis", "column": "product_adoption_rate"}] | False |
| B14 | AVG(CASE WHEN is_target = 0 THEN product_adoption_rate END) | [{"table": "customer360__customer_value_analysis", "column": "product_adoption_rate"}] | [{"table": "customer360__customer_value_analysis", "column": "investment_priority_score"}, {"table": "customer360__customer_value_analysis", "column": "support_resolution_efficiency"}, {"table": "customer360__customer_value_analysis", "column": "support_resolution_efficiency"}, {"table": "customer360__customer_value_analysis", "column": "support_resolution_efficiency"}, {"table": "customer360__customer_value_analysis", "column": "support_resolution_efficiency"}, {"table": "customer360__customer", "column": "total_sales_amount"}, {"table": "customer360__customer", "column": "total_sales_amount"}, {"table": "customer360__customer", "column": "total_sales_amount"}, {"table": "customer360__customer", "column": "total_sales_amount"}, {"table": "customer360__customer_value_analysis", "column": "product_adoption_rate"}, {"table": "customer360__customer_value_analysis", "column": "product_adoption_rate"}, {"table": "customer360__customer_value_analysis", "column": "product_adoption_rate"}, {"table": "customer360__customer_value_analysis", "column": "product_adoption_rate"}] | False |
| B14 | MIN(team_size) | [{"table": "customer360__customer_value_analysis", "column": "team_size"}] | [] | False |
| B14 | COUNT(*) | [] | [] | True |
| B14 | SUM(is_target) | [{"table": "customer360__customer_value_analysis", "column": "investment_priority_score"}, {"table": "customer360__customer_value_analysis", "column": "support_resolution_efficiency"}, {"table": "customer360__customer_value_analysis", "column": "support_resolution_efficiency"}, {"table": "customer360__customer_value_analysis", "column": "support_resolution_efficiency"}, {"table": "customer360__customer_value_analysis", "column": "support_resolution_efficiency"}, {"table": "customer360__customer", "column": "total_sales_amount"}, {"table": "customer360__customer", "column": "total_sales_amount"}, {"table": "customer360__customer", "column": "total_sales_amount"}, {"table": "customer360__customer", "column": "total_sales_amount"}, {"table": "customer360__customer_value_analysis", "column": "product_adoption_rate"}, {"table": "customer360__customer_value_analysis", "column": "product_adoption_rate"}, {"table": "customer360__customer_value_analysis", "column": "product_adoption_rate"}, {"table": "customer360__customer_value_analysis", "column": "product_adoption_rate"}] | [] | False |


## S56

类别 `data`；来源 `query_db`；调用 `f12b6cdec944455999646a52f8cc586d`；状态 `success`。

```sql
WITH base AS (
  SELECT DISTINCT v.primary_email, v.investment_priority_score, v.product_adoption_rate,
    v.support_resolution_efficiency, v.acquisition_cost, v.customer_lifetime_value,
    v.lifecycle_stage, v.industry_vertical, v.company_size_tier,
    v.customer_onboarding_score, v.team_size, v.decision_maker_level,
    v.digital_engagement_score, v.nps_score, v.customer_health_score, v.churn_probability,
    c_sales.total_sales_amount
  FROM (
    SELECT DISTINCT * FROM customer360__customer_value_analysis
  ) v
  LEFT JOIN (
    SELECT email, MAX(total_sales_amount) AS total_sales_amount
    FROM customer360__customer
    WHERE total_sales_amount IS NOT NULL
    GROUP BY email
  ) c_sales ON v.primary_email = c_sales.email
  WHERE v.primary_email IS NOT NULL
),
scaled AS (
  SELECT *,
    (total_sales_amount - (SELECT MIN(total_sales_amount) FROM base)) / 
      NULLIF((SELECT MAX(total_sales_amount) - MIN(total_sales_amount) FROM base), 0) AS nsales,
    (product_adoption_rate - (SELECT MIN(product_adoption_rate) FROM base)) / 
      NULLIF((SELECT MAX(product_adoption_rate) - MIN(product_adoption_rate) FROM base), 0) AS nadopt,
    (support_resolution_efficiency - (SELECT MIN(support_resolution_efficiency) FROM base)) / 
      NULLIF((SELECT MAX(support_resolution_efficiency) - MIN(support_resolution_efficiency) FROM base), 0) AS nres
  FROM base
  WHERE product_adoption_rate IS NOT NULL AND support_resolution_efficiency IS NOT NULL
    AND total_sales_amount IS NOT NULL AND acquisition_cost IS NOT NULL AND customer_lifetime_value IS NOT NULL
),
with_comp AS (
  SELECT *, 0.4*nsales + 0.35*nadopt + 0.25*nres AS composite_score
  FROM scaled
),
ranked AS (
  SELECT *,
    ROW_NUMBER() OVER (ORDER BY investment_priority_score ASC) AS rn_ips_asc,
    ROW_NUMBER() OVER (ORDER BY composite_score ASC) AS rn_comp_asc,
    COUNT(*) OVER () AS total_cnt
  FROM with_comp
),
flagged AS (
  SELECT *, CASE WHEN rn_ips_asc >= 0.7*total_cnt AND rn_comp_asc <= 0.5*total_cnt THEN 1 ELSE 0 END AS is_target
  FROM ranked
)
SELECT is_target, COUNT(*) AS cnt,
  AVG(customer_onboarding_score) AS avg_onboarding,
  AVG(product_adoption_rate) AS avg_par,
  AVG(support_resolution_efficiency) AS avg_sre,
  AVG(customer_lifetime_value / NULLIF(acquisition_cost, 0)) AS avg_roi,
  AVG(team_size) AS avg_team_size,
  AVG(nps_score) AS avg_nps,
  AVG(digital_engagement_score) AS avg_digital_eng,
  AVG(customer_health_score) AS avg_health,
  AVG(churn_probability) AS avg_churn
FROM flagged
GROUP BY is_target
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-055/attempt-01/sql/S56.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-055/attempt-01/sql/S56.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-055/attempt-01/results/S56.rows.jsonl)；完整：True；SHA256：`473b7de734a0a3da05c9824484e97b287e845ce1a33a6594f4534576309f5b72`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "customer360__customer_value_analysis", "kind": "base", "block": null, "base_tables": ["customer360__customer_value_analysis"]}] | [] | [] |
| B2 | [{"alias": "customer360__customer", "kind": "base", "block": null, "base_tables": ["customer360__customer"]}] | [] | ["email"] |
| B3 | [{"alias": "v", "kind": "derived", "block": "B1", "base_tables": ["customer360__customer_value_analysis"]}, {"alias": "c_sales", "kind": "derived", "block": "B2", "base_tables": ["customer360__customer"]}] | [{"type": "LEFT", "right": "(SELECT email, MAX(total_sales_amount) AS total_sales_amount FROM customer360__customer WHERE NOT total_sales_amount IS NULL GROUP BY email) AS c_sales", "on": "v.primary_email = c_sales.email", "using": []}] | [] |
| B4 | [{"alias": "base", "kind": "derived", "block": "B3", "base_tables": ["customer360__customer", "customer360__customer_value_analysis"]}] | [] | [] |
| B5 | [{"alias": "base", "kind": "derived", "block": "B3", "base_tables": ["customer360__customer", "customer360__customer_value_analysis"]}] | [] | [] |
| B6 | [{"alias": "base", "kind": "derived", "block": "B3", "base_tables": ["customer360__customer", "customer360__customer_value_analysis"]}] | [] | [] |
| B7 | [{"alias": "base", "kind": "derived", "block": "B3", "base_tables": ["customer360__customer", "customer360__customer_value_analysis"]}] | [] | [] |
| B8 | [{"alias": "base", "kind": "derived", "block": "B3", "base_tables": ["customer360__customer", "customer360__customer_value_analysis"]}] | [] | [] |
| B9 | [{"alias": "base", "kind": "derived", "block": "B3", "base_tables": ["customer360__customer", "customer360__customer_value_analysis"]}] | [] | [] |
| B10 | [{"alias": "base", "kind": "derived", "block": "B3", "base_tables": ["customer360__customer", "customer360__customer_value_analysis"]}] | [] | [] |
| B11 | [{"alias": "scaled", "kind": "derived", "block": "B10", "base_tables": ["customer360__customer", "customer360__customer_value_analysis"]}] | [] | [] |
| B12 | [{"alias": "with_comp", "kind": "derived", "block": "B11", "base_tables": ["customer360__customer", "customer360__customer_value_analysis"]}] | [] | [] |
| B13 | [{"alias": "ranked", "kind": "derived", "block": "B12", "base_tables": ["customer360__customer", "customer360__customer_value_analysis"]}] | [] | [] |
| B14 | [{"alias": "flagged", "kind": "derived", "block": "B13", "base_tables": ["customer360__customer", "customer360__customer_value_analysis"]}] | [] | ["is_target"] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B2 | MAX(total_sales_amount) | [{"table": "customer360__customer", "column": "total_sales_amount"}] | [] | False |
| B4 | MIN(total_sales_amount) | [{"table": "customer360__customer", "column": "total_sales_amount"}] | [] | False |
| B5 | MAX(total_sales_amount) | [{"table": "customer360__customer", "column": "total_sales_amount"}] | [] | False |
| B5 | MIN(total_sales_amount) | [{"table": "customer360__customer", "column": "total_sales_amount"}] | [] | False |
| B6 | MIN(product_adoption_rate) | [{"table": "customer360__customer_value_analysis", "column": "product_adoption_rate"}] | [] | False |
| B7 | MAX(product_adoption_rate) | [{"table": "customer360__customer_value_analysis", "column": "product_adoption_rate"}] | [] | False |
| B7 | MIN(product_adoption_rate) | [{"table": "customer360__customer_value_analysis", "column": "product_adoption_rate"}] | [] | False |
| B8 | MIN(support_resolution_efficiency) | [{"table": "customer360__customer_value_analysis", "column": "support_resolution_efficiency"}] | [] | False |
| B9 | MAX(support_resolution_efficiency) | [{"table": "customer360__customer_value_analysis", "column": "support_resolution_efficiency"}] | [] | False |
| B9 | MIN(support_resolution_efficiency) | [{"table": "customer360__customer_value_analysis", "column": "support_resolution_efficiency"}] | [] | False |
| B14 | COUNT(*) | [] | [] | True |
| B14 | AVG(customer_onboarding_score) | [{"table": "customer360__customer_value_analysis", "column": "customer_onboarding_score"}] | [] | False |
| B14 | AVG(product_adoption_rate) | [{"table": "customer360__customer_value_analysis", "column": "product_adoption_rate"}] | [] | False |
| B14 | AVG(support_resolution_efficiency) | [{"table": "customer360__customer_value_analysis", "column": "support_resolution_efficiency"}] | [] | False |
| B14 | AVG(customer_lifetime_value / NULLIF(acquisition_cost, 0)) | [{"table": "customer360__customer_value_analysis", "column": "customer_lifetime_value"}, {"table": "customer360__customer_value_analysis", "column": "acquisition_cost"}] | [] | False |
| B14 | AVG(team_size) | [{"table": "customer360__customer_value_analysis", "column": "team_size"}] | [] | False |
| B14 | AVG(nps_score) | [{"table": "customer360__customer_value_analysis", "column": "nps_score"}] | [] | False |
| B14 | AVG(digital_engagement_score) | [{"table": "customer360__customer_value_analysis", "column": "digital_engagement_score"}] | [] | False |
| B14 | AVG(customer_health_score) | [{"table": "customer360__customer_value_analysis", "column": "customer_health_score"}] | [] | False |
| B14 | AVG(churn_probability) | [{"table": "customer360__customer_value_analysis", "column": "churn_probability"}] | [] | False |


## S57

类别 `data`；来源 `python`；调用 `5f91840c797b4a7f8129f6ccf32b7f2c`；状态 `failed`。

```sql

WITH base AS (
  SELECT DISTINCT v.primary_email, v.investment_priority_score, v.product_adoption_rate,
    v.support_resolution_efficiency, v.acquisition_cost, v.customer_lifetime_value,
    v.lifecycle_stage, v.industry_vertical, v.company_size_tier,
    v.customer_onboarding_score, v.team_size, v.decision_maker_level,
    v.digital_engagement_score, v.nps_score, v.customer_health_score, v.churn_probability,
    v.competitive_pressure_index, v.renewal_probability, v.expansion_revenue_potential, v.time_to_value_days,
    c_sales.total_sales_amount
  FROM (
    SELECT DISTINCT * FROM customer360__customer_value_analysis
  ) v
  LEFT JOIN (
    SELECT email, MAX(total_sales_amount) AS total_sales_amount
    FROM customer360__customer
    WHERE total_sales_amount IS NOT NULL
    GROUP BY email
  ) c_sales ON v.primary_email = c_sales.email
  WHERE v.primary_email IS NOT NULL
),
scaled AS (
  SELECT *,
    (total_sales_amount - (SELECT MIN(total_sales_amount) FROM base)) / 
      NULLIF((SELECT MAX(total_sales_amount) - MIN(total_sales_amount) FROM base), 0) AS nsales,
    (product_adoption_rate - (SELECT MIN(product_adoption_rate) FROM base)) / 
      NULLIF((SELECT MAX(product_adoption_rate) - MIN(product_adoption_rate) FROM base), 0) AS nadopt,
    (support_resolution_efficiency - (SELECT MIN(support_resolution_efficiency) FROM base)) / 
      NULLIF((SELECT MAX(support_resolution_efficiency) - MIN(support_resolution_efficiency) FROM base), 0) AS nres
  FROM base
  WHERE product_adoption_rate IS NOT NULL AND support_resolution_efficiency IS NOT NULL
    AND total_sales_amount IS NOT NULL AND acquisition_cost IS NOT NULL AND customer_lifetime_value IS NOT NULL
),
with_comp AS (
  SELECT *, 0.4*nsales + 0.35*nadopt + 0.25*nres AS composite_score
  FROM scaled
),
ranked AS (
  SELECT *,
    ROW_NUMBER() OVER (ORDER BY investment_priority_score ASC) AS rn_ips_asc,
    ROW_NUMBER() OVER (ORDER BY composite_score ASC) AS rn_comp_asc,
    COUNT(*) OVER () AS total_cnt
  FROM with_comp
),
flagged AS (
  SELECT *, CASE WHEN rn_ips_asc >= 0.7*total_cnt AND rn_comp_asc <= 0.5*total_cnt THEN 1 ELSE 0 END AS is_target
  FROM ranked
)
SELECT primary_email, investment_priority_score AS ips, product_adoption_rate AS par,
  support_resolution_efficiency AS sre, total_sales_amount AS sales, acquisition_cost AS acq,
  customer_lifetime_value AS clv, clv/NULLIF(acquisition_cost,0) AS roi,
  composite_score AS comp, customer_onboarding_score AS onboarding, team_size, decision_maker_level AS dm,
  lifecycle_stage, industry_vertical, company_size_tier, digital_engagement_score AS digi_eng,
  nps_score AS nps, customer_health_score AS health, churn_probability AS churn,
  competitive_pressure_index AS cpi, renewal_probability AS renew, expansion_revenue_potential AS expansion,
  time_to_value_days AS ttv, is_target
FROM flagged

```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-055/attempt-01/sql/S57.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-055/attempt-01/sql/S57.parameters.json)。

错误：`OperationalError('no such column: clv')`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "customer360__customer_value_analysis", "kind": "base", "block": null, "base_tables": ["customer360__customer_value_analysis"]}] | [] | [] |
| B2 | [{"alias": "customer360__customer", "kind": "base", "block": null, "base_tables": ["customer360__customer"]}] | [] | ["email"] |
| B3 | [{"alias": "v", "kind": "derived", "block": "B1", "base_tables": ["customer360__customer_value_analysis"]}, {"alias": "c_sales", "kind": "derived", "block": "B2", "base_tables": ["customer360__customer"]}] | [{"type": "LEFT", "right": "(SELECT email, MAX(total_sales_amount) AS total_sales_amount FROM customer360__customer WHERE NOT total_sales_amount IS NULL GROUP BY email) AS c_sales", "on": "v.primary_email = c_sales.email", "using": []}] | [] |
| B4 | [{"alias": "base", "kind": "derived", "block": "B3", "base_tables": ["customer360__customer", "customer360__customer_value_analysis"]}] | [] | [] |
| B5 | [{"alias": "base", "kind": "derived", "block": "B3", "base_tables": ["customer360__customer", "customer360__customer_value_analysis"]}] | [] | [] |
| B6 | [{"alias": "base", "kind": "derived", "block": "B3", "base_tables": ["customer360__customer", "customer360__customer_value_analysis"]}] | [] | [] |
| B7 | [{"alias": "base", "kind": "derived", "block": "B3", "base_tables": ["customer360__customer", "customer360__customer_value_analysis"]}] | [] | [] |
| B8 | [{"alias": "base", "kind": "derived", "block": "B3", "base_tables": ["customer360__customer", "customer360__customer_value_analysis"]}] | [] | [] |
| B9 | [{"alias": "base", "kind": "derived", "block": "B3", "base_tables": ["customer360__customer", "customer360__customer_value_analysis"]}] | [] | [] |
| B10 | [{"alias": "base", "kind": "derived", "block": "B3", "base_tables": ["customer360__customer", "customer360__customer_value_analysis"]}] | [] | [] |
| B11 | [{"alias": "scaled", "kind": "derived", "block": "B10", "base_tables": ["customer360__customer", "customer360__customer_value_analysis"]}] | [] | [] |
| B12 | [{"alias": "with_comp", "kind": "derived", "block": "B11", "base_tables": ["customer360__customer", "customer360__customer_value_analysis"]}] | [] | [] |
| B13 | [{"alias": "ranked", "kind": "derived", "block": "B12", "base_tables": ["customer360__customer", "customer360__customer_value_analysis"]}] | [] | [] |
| B14 | [{"alias": "flagged", "kind": "derived", "block": "B13", "base_tables": ["customer360__customer", "customer360__customer_value_analysis"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B2 | MAX(total_sales_amount) | [{"table": "customer360__customer", "column": "total_sales_amount"}] | [] | False |
| B4 | MIN(total_sales_amount) | [{"table": "customer360__customer", "column": "total_sales_amount"}] | [] | False |
| B5 | MAX(total_sales_amount) | [{"table": "customer360__customer", "column": "total_sales_amount"}] | [] | False |
| B5 | MIN(total_sales_amount) | [{"table": "customer360__customer", "column": "total_sales_amount"}] | [] | False |
| B6 | MIN(product_adoption_rate) | [{"table": "customer360__customer_value_analysis", "column": "product_adoption_rate"}] | [] | False |
| B7 | MAX(product_adoption_rate) | [{"table": "customer360__customer_value_analysis", "column": "product_adoption_rate"}] | [] | False |
| B7 | MIN(product_adoption_rate) | [{"table": "customer360__customer_value_analysis", "column": "product_adoption_rate"}] | [] | False |
| B8 | MIN(support_resolution_efficiency) | [{"table": "customer360__customer_value_analysis", "column": "support_resolution_efficiency"}] | [] | False |
| B9 | MAX(support_resolution_efficiency) | [{"table": "customer360__customer_value_analysis", "column": "support_resolution_efficiency"}] | [] | False |
| B9 | MIN(support_resolution_efficiency) | [{"table": "customer360__customer_value_analysis", "column": "support_resolution_efficiency"}] | [] | False |


## S58

类别 `data`；来源 `python`；调用 `5e1eae5fe4c84c9e8ed596469ddd504f`；状态 `failed`。

```sql

WITH base AS (
  SELECT DISTINCT v.primary_email, v.investment_priority_score, v.product_adoption_rate,
    v.support_resolution_efficiency, v.acquisition_cost, v.customer_lifetime_value,
    v.lifecycle_stage, v.industry_vertical, v.company_size_tier,
    v.customer_onboarding_score, v.team_size, v.decision_maker_level,
    v.digital_engagement_score, v.nps_score, v.customer_health_score, v.churn_probability,
    v.competitive_pressure_index, v.renewal_probability, v.expansion_revenue_potential, v.time_to_value_days,
    c_sales.total_sales_amount
  FROM (
    SELECT DISTINCT * FROM customer360__customer_value_analysis
  ) v
  LEFT JOIN (
    SELECT email, MAX(total_sales_amount) AS total_sales_amount
    FROM customer360__customer
    WHERE total_sales_amount IS NOT NULL
    GROUP BY email
  ) c_sales ON v.primary_email = c_sales.email
  WHERE v.primary_email IS NOT NULL
),
scaled AS (
  SELECT *,
    (total_sales_amount - (SELECT MIN(total_sales_amount) FROM base)) / 
      NULLIF((SELECT MAX(total_sales_amount) - MIN(total_sales_amount) FROM base), 0) AS nsales,
    (product_adoption_rate - (SELECT MIN(product_adoption_rate) FROM base)) / 
      NULLIF((SELECT MAX(product_adoption_rate) - MIN(product_adoption_rate) FROM base), 0) AS nadopt,
    (support_resolution_efficiency - (SELECT MIN(support_resolution_efficiency) FROM base)) / 
      NULLIF((SELECT MAX(support_resolution_efficiency) - MIN(support_resolution_efficiency) FROM base), 0) AS nres
  FROM base
  WHERE product_adoption_rate IS NOT NULL AND support_resolution_efficiency IS NOT NULL
    AND total_sales_amount IS NOT NULL AND acquisition_cost IS NOT NULL AND customer_lifetime_value IS NOT NULL
),
with_comp AS (
  SELECT *, 0.4*nsales + 0.35*nadopt + 0.25*nres AS composite_score
  FROM scaled
),
ranked AS (
  SELECT *,
    ROW_NUMBER() OVER (ORDER BY investment_priority_score ASC) AS rn_ips_asc,
    ROW_NUMBER() OVER (ORDER BY composite_score ASC) AS rn_comp_asc,
    COUNT(*) OVER () AS total_cnt
  FROM with_comp
),
flagged AS (
  SELECT *, CASE WHEN rn_ips_asc >= 0.7*total_cnt AND rn_comp_asc <= 0.5*total_cnt THEN 1 ELSE 0 END AS is_target
  FROM ranked
)
SELECT primary_email, investment_priority_score AS ips, product_adoption_rate AS par,
  support_resolution_efficiency AS sre, total_sales_amount AS sales, acquisition_cost AS acq,
  customer_lifetime_value AS clv, clv/NULLIF(acquisition_cost,0) AS roi,
  composite_score AS comp, customer_onboarding_score AS onboarding, team_size, decision_maker_level AS dm,
  lifecycle_stage, industry_vertical, company_size_tier, digital_engagement_score AS digi_eng,
  nps_score AS nps, customer_health_score AS health, churn_probability AS churn,
  competitive_pressure_index AS cpi, renewal_probability AS renew, expansion_revenue_potential AS expansion,
  time_to_value_days AS ttv, is_target
FROM flagged

```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-055/attempt-01/sql/S58.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-055/attempt-01/sql/S58.parameters.json)。

错误：`OperationalError('no such column: clv')`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "customer360__customer_value_analysis", "kind": "base", "block": null, "base_tables": ["customer360__customer_value_analysis"]}] | [] | [] |
| B2 | [{"alias": "customer360__customer", "kind": "base", "block": null, "base_tables": ["customer360__customer"]}] | [] | ["email"] |
| B3 | [{"alias": "v", "kind": "derived", "block": "B1", "base_tables": ["customer360__customer_value_analysis"]}, {"alias": "c_sales", "kind": "derived", "block": "B2", "base_tables": ["customer360__customer"]}] | [{"type": "LEFT", "right": "(SELECT email, MAX(total_sales_amount) AS total_sales_amount FROM customer360__customer WHERE NOT total_sales_amount IS NULL GROUP BY email) AS c_sales", "on": "v.primary_email = c_sales.email", "using": []}] | [] |
| B4 | [{"alias": "base", "kind": "derived", "block": "B3", "base_tables": ["customer360__customer", "customer360__customer_value_analysis"]}] | [] | [] |
| B5 | [{"alias": "base", "kind": "derived", "block": "B3", "base_tables": ["customer360__customer", "customer360__customer_value_analysis"]}] | [] | [] |
| B6 | [{"alias": "base", "kind": "derived", "block": "B3", "base_tables": ["customer360__customer", "customer360__customer_value_analysis"]}] | [] | [] |
| B7 | [{"alias": "base", "kind": "derived", "block": "B3", "base_tables": ["customer360__customer", "customer360__customer_value_analysis"]}] | [] | [] |
| B8 | [{"alias": "base", "kind": "derived", "block": "B3", "base_tables": ["customer360__customer", "customer360__customer_value_analysis"]}] | [] | [] |
| B9 | [{"alias": "base", "kind": "derived", "block": "B3", "base_tables": ["customer360__customer", "customer360__customer_value_analysis"]}] | [] | [] |
| B10 | [{"alias": "base", "kind": "derived", "block": "B3", "base_tables": ["customer360__customer", "customer360__customer_value_analysis"]}] | [] | [] |
| B11 | [{"alias": "scaled", "kind": "derived", "block": "B10", "base_tables": ["customer360__customer", "customer360__customer_value_analysis"]}] | [] | [] |
| B12 | [{"alias": "with_comp", "kind": "derived", "block": "B11", "base_tables": ["customer360__customer", "customer360__customer_value_analysis"]}] | [] | [] |
| B13 | [{"alias": "ranked", "kind": "derived", "block": "B12", "base_tables": ["customer360__customer", "customer360__customer_value_analysis"]}] | [] | [] |
| B14 | [{"alias": "flagged", "kind": "derived", "block": "B13", "base_tables": ["customer360__customer", "customer360__customer_value_analysis"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B2 | MAX(total_sales_amount) | [{"table": "customer360__customer", "column": "total_sales_amount"}] | [] | False |
| B4 | MIN(total_sales_amount) | [{"table": "customer360__customer", "column": "total_sales_amount"}] | [] | False |
| B5 | MAX(total_sales_amount) | [{"table": "customer360__customer", "column": "total_sales_amount"}] | [] | False |
| B5 | MIN(total_sales_amount) | [{"table": "customer360__customer", "column": "total_sales_amount"}] | [] | False |
| B6 | MIN(product_adoption_rate) | [{"table": "customer360__customer_value_analysis", "column": "product_adoption_rate"}] | [] | False |
| B7 | MAX(product_adoption_rate) | [{"table": "customer360__customer_value_analysis", "column": "product_adoption_rate"}] | [] | False |
| B7 | MIN(product_adoption_rate) | [{"table": "customer360__customer_value_analysis", "column": "product_adoption_rate"}] | [] | False |
| B8 | MIN(support_resolution_efficiency) | [{"table": "customer360__customer_value_analysis", "column": "support_resolution_efficiency"}] | [] | False |
| B9 | MAX(support_resolution_efficiency) | [{"table": "customer360__customer_value_analysis", "column": "support_resolution_efficiency"}] | [] | False |
| B9 | MIN(support_resolution_efficiency) | [{"table": "customer360__customer_value_analysis", "column": "support_resolution_efficiency"}] | [] | False |


## S59

类别 `data`；来源 `python`；调用 `52f28e7dcff94ea6a0992e42072a4c06`；状态 `success`。

```sql

SELECT investment_priority_score AS ips, product_adoption_rate AS par,
  support_resolution_efficiency AS sre, acquisition_cost AS acq,
  customer_lifetime_value AS clv, customer_onboarding_score AS onboarding, team_size,
  decision_maker_level AS dm, lifecycle_stage, industry_vertical, company_size_tier
FROM customer360__customer_value_analysis
LIMIT 2000

```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-055/attempt-01/sql/S59.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-055/attempt-01/sql/S59.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-055/attempt-01/results/S59.rows.jsonl)；完整：True；SHA256：`e09d4d642a9a59c82fdfc57ff490c3e7f904aaa32be4e8b7074dcf4f2617d7fc`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "customer360__customer_value_analysis", "kind": "base", "block": null, "base_tables": ["customer360__customer_value_analysis"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |


## S60

类别 `data`；来源 `python`；调用 `bd72188b869e460ab293d42e775c8bc5`；状态 `failed`。

```sql

SELECT investment_priority_score AS ips, product_adoption_rate AS par,
  support_resolution_efficiency AS sre, acquisition_cost AS acq,
  customer_lifetime_value AS clv, customer_onboarding_score AS onboarding, team_size,
  decision_maker_level AS dm, lifecycle_stage, industry_vertical, company_size_tier,
  total_sales_amount AS sales, digital_engagement_score AS digi_eng, nps_score AS nps,
  customer_health_score AS health, churn_probability AS churn,
  competitive_pressure_index AS cpi, renewal_probability AS renew,
  expansion_revenue_potential AS expansion, time_to_value_days AS ttv
FROM customer360__customer_value_analysis
LIMIT 5000

```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-055/attempt-01/sql/S60.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-055/attempt-01/sql/S60.parameters.json)。

错误：`OperationalError('no such column: total_sales_amount')`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "customer360__customer_value_analysis", "kind": "base", "block": null, "base_tables": ["customer360__customer_value_analysis"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |


未解析列血缘：[{"block": "B1", "column": "total_sales_amount", "reason": "ambiguous_or_missing_source"}]

## S61

类别 `data`；来源 `python`；调用 `8d2c06b33df941d6ba9aaaa34960b20c`；状态 `failed`。

```sql

SELECT investment_priority_score AS ips, product_adoption_rate AS par,
  support_resolution_efficiency AS sre, acquisition_cost AS acq,
  customer_lifetime_value AS clv, customer_onboarding_score AS onboarding, team_size,
  decision_maker_level AS dm, lifecycle_stage, industry_vertical, company_size_tier,
  total_sales_amount AS sales, digital_engagement_score AS digi_eng, nps_score AS nps,
  customer_health_score AS health, churn_probability AS churn
FROM customer360__customer_value_analysis
LIMIT 3000

```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-055/attempt-01/sql/S61.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-055/attempt-01/sql/S61.parameters.json)。

错误：`OperationalError('no such column: total_sales_amount')`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "customer360__customer_value_analysis", "kind": "base", "block": null, "base_tables": ["customer360__customer_value_analysis"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |


未解析列血缘：[{"block": "B1", "column": "total_sales_amount", "reason": "ambiguous_or_missing_source"}]

## S62

类别 `data`；来源 `python`；调用 `df5d315f3c384211babe9f6b8c41be12`；状态 `failed`。

```sql

    SELECT investment_priority_score AS ips, product_adoption_rate AS par,
      support_resolution_efficiency AS sre, acquisition_cost AS acq,
      customer_lifetime_value AS clv, customer_onboarding_score AS onboarding, team_size,
      decision_maker_level AS dm, lifecycle_stage, industry_vertical, company_size_tier,
      total_sales_amount AS sales, digital_engagement_score AS digi_eng, nps_score AS nps,
      customer_health_score AS health, churn_probability AS churn
    FROM customer360__customer_value_analysis
    LIMIT 2200
    
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-055/attempt-01/sql/S62.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-055/attempt-01/sql/S62.parameters.json)。

错误：`OperationalError('no such column: total_sales_amount')`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "customer360__customer_value_analysis", "kind": "base", "block": null, "base_tables": ["customer360__customer_value_analysis"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |


未解析列血缘：[{"block": "B1", "column": "total_sales_amount", "reason": "ambiguous_or_missing_source"}]

## S63

类别 `data`；来源 `python`；调用 `df5d315f3c384211babe9f6b8c41be12`；状态 `failed`。

```sql

    SELECT investment_priority_score AS ips, product_adoption_rate AS par,
      support_resolution_efficiency AS sre, acquisition_cost AS acq,
      customer_lifetime_value AS clv, customer_onboarding_score AS onboarding, team_size,
      decision_maker_level AS dm, lifecycle_stage, industry_vertical, company_size_tier,
      total_sales_amount AS sales, digital_engagement_score AS digi_eng, nps_score AS nps,
      customer_health_score AS health, churn_probability AS churn
    FROM customer360__customer_value_analysis
    LIMIT 2500
    
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-055/attempt-01/sql/S63.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-055/attempt-01/sql/S63.parameters.json)。

错误：`OperationalError('no such column: total_sales_amount')`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "customer360__customer_value_analysis", "kind": "base", "block": null, "base_tables": ["customer360__customer_value_analysis"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |


未解析列血缘：[{"block": "B1", "column": "total_sales_amount", "reason": "ambiguous_or_missing_source"}]

## S64

类别 `data`；来源 `python`；调用 `79a470ef59b7439297450aa60d47af6f`；状态 `success`。

```sql

    SELECT marketo_lead_id, stripe_customer_id, zendesk_user_id, primary_email,
      investment_priority_score AS ips, product_adoption_rate AS par,
      support_resolution_efficiency AS sre, acquisition_cost AS acq,
      customer_lifetime_value AS clv, customer_onboarding_score AS onboarding, team_size,
      decision_maker_level AS dm, lifecycle_stage, industry_vertical, company_size_tier,
      digital_engagement_score AS digi_eng, nps_score AS nps,
      customer_health_score AS health, churn_probability AS churn,
      competitive_pressure_index AS cpi, renewal_probability AS renew,
      expansion_revenue_potential AS expansion, time_to_value_days AS ttv
    FROM customer360__customer_value_analysis
    LIMIT 2000 OFFSET 0
    
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-055/attempt-01/sql/S64.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-055/attempt-01/sql/S64.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-055/attempt-01/results/S64.rows.jsonl)；完整：True；SHA256：`5fb0111b2f4bb3120d2faf6af2c37883b5cc02bbfe2541144ea39cd8d8044088`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "customer360__customer_value_analysis", "kind": "base", "block": null, "base_tables": ["customer360__customer_value_analysis"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |


## S65

类别 `data`；来源 `python`；调用 `79a470ef59b7439297450aa60d47af6f`；状态 `success`。

```sql

    SELECT marketo_lead_id, stripe_customer_id, zendesk_user_id, primary_email,
      investment_priority_score AS ips, product_adoption_rate AS par,
      support_resolution_efficiency AS sre, acquisition_cost AS acq,
      customer_lifetime_value AS clv, customer_onboarding_score AS onboarding, team_size,
      decision_maker_level AS dm, lifecycle_stage, industry_vertical, company_size_tier,
      digital_engagement_score AS digi_eng, nps_score AS nps,
      customer_health_score AS health, churn_probability AS churn,
      competitive_pressure_index AS cpi, renewal_probability AS renew,
      expansion_revenue_potential AS expansion, time_to_value_days AS ttv
    FROM customer360__customer_value_analysis
    LIMIT 2000 OFFSET 2000
    
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-055/attempt-01/sql/S65.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-055/attempt-01/sql/S65.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-055/attempt-01/results/S65.rows.jsonl)；完整：True；SHA256：`94af64db27d3ff8a11b6ff0df4ef5c39c1a85073db922280dca0c24707ae383b`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "customer360__customer_value_analysis", "kind": "base", "block": null, "base_tables": ["customer360__customer_value_analysis"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |


## S66

类别 `data`；来源 `python`；调用 `79a470ef59b7439297450aa60d47af6f`；状态 `success`。

```sql

    SELECT marketo_lead_id, stripe_customer_id, zendesk_user_id, primary_email,
      investment_priority_score AS ips, product_adoption_rate AS par,
      support_resolution_efficiency AS sre, acquisition_cost AS acq,
      customer_lifetime_value AS clv, customer_onboarding_score AS onboarding, team_size,
      decision_maker_level AS dm, lifecycle_stage, industry_vertical, company_size_tier,
      digital_engagement_score AS digi_eng, nps_score AS nps,
      customer_health_score AS health, churn_probability AS churn,
      competitive_pressure_index AS cpi, renewal_probability AS renew,
      expansion_revenue_potential AS expansion, time_to_value_days AS ttv
    FROM customer360__customer_value_analysis
    LIMIT 2000 OFFSET 4000
    
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-055/attempt-01/sql/S66.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-055/attempt-01/sql/S66.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-055/attempt-01/results/S66.rows.jsonl)；完整：True；SHA256：`8322e4e107f55316fb709a48d923e79f5f4c91bd4af2d607db13ccd928e9f864`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "customer360__customer_value_analysis", "kind": "base", "block": null, "base_tables": ["customer360__customer_value_analysis"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |


## S67

类别 `data`；来源 `python`；调用 `2656db0b691841a3a9c0df9c1633970f`；状态 `success`。

```sql

SELECT marketo_lead_id, stripe_customer_id, zendesk_user_id, primary_email,
  investment_priority_score AS ips, product_adoption_rate AS par,
  support_resolution_efficiency AS sre, acquisition_cost AS acq,
  customer_lifetime_value AS clv, customer_onboarding_score AS onboarding, team_size,
  decision_maker_level AS dm, lifecycle_stage, industry_vertical, company_size_tier,
  digital_engagement_score AS digi_eng, nps_score AS nps,
  customer_health_score AS health, churn_probability AS churn,
  competitive_pressure_index AS cpi, renewal_probability AS renew,
  expansion_revenue_potential AS expansion, time_to_value_days AS ttv
FROM customer360__customer_value_analysis
LIMIT 5

```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-055/attempt-01/sql/S67.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-055/attempt-01/sql/S67.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-055/attempt-01/results/S67.rows.jsonl)；完整：True；SHA256：`cffc289fa0c81a225716c615d0c4abd54cf62bbf54c773d02be69871a458bed9`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "customer360__customer_value_analysis", "kind": "base", "block": null, "base_tables": ["customer360__customer_value_analysis"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |


## S68

类别 `data`；来源 `python`；调用 `8da35c808ed84d73bf7b3799800757ea`；状态 `success`。

```sql

    SELECT marketo_lead_id, stripe_customer_id, zendesk_user_id, primary_email,
      investment_priority_score AS ips, product_adoption_rate AS par,
      support_resolution_efficiency AS sre, acquisition_cost AS acq,
      customer_lifetime_value AS clv, customer_onboarding_score AS onboarding, team_size,
      decision_maker_level AS dm, lifecycle_stage, industry_vertical, company_size_tier,
      digital_engagement_score AS digi_eng, nps_score AS nps,
      customer_health_score AS health, churn_probability AS churn,
      competitive_pressure_index AS cpi, renewal_probability AS renew,
      expansion_revenue_potential AS expansion, time_to_value_days AS ttv
    FROM customer360__customer_value_analysis
    LIMIT 2000 OFFSET 0
    
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-055/attempt-01/sql/S68.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-055/attempt-01/sql/S68.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-055/attempt-01/results/S68.rows.jsonl)；完整：True；SHA256：`5fb0111b2f4bb3120d2faf6af2c37883b5cc02bbfe2541144ea39cd8d8044088`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "customer360__customer_value_analysis", "kind": "base", "block": null, "base_tables": ["customer360__customer_value_analysis"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |


## S69

类别 `data`；来源 `python`；调用 `8da35c808ed84d73bf7b3799800757ea`；状态 `success`。

```sql

    SELECT marketo_lead_id, stripe_customer_id, zendesk_user_id, primary_email,
      investment_priority_score AS ips, product_adoption_rate AS par,
      support_resolution_efficiency AS sre, acquisition_cost AS acq,
      customer_lifetime_value AS clv, customer_onboarding_score AS onboarding, team_size,
      decision_maker_level AS dm, lifecycle_stage, industry_vertical, company_size_tier,
      digital_engagement_score AS digi_eng, nps_score AS nps,
      customer_health_score AS health, churn_probability AS churn,
      competitive_pressure_index AS cpi, renewal_probability AS renew,
      expansion_revenue_potential AS expansion, time_to_value_days AS ttv
    FROM customer360__customer_value_analysis
    LIMIT 2000 OFFSET 2000
    
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-055/attempt-01/sql/S69.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-055/attempt-01/sql/S69.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-055/attempt-01/results/S69.rows.jsonl)；完整：True；SHA256：`94af64db27d3ff8a11b6ff0df4ef5c39c1a85073db922280dca0c24707ae383b`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "customer360__customer_value_analysis", "kind": "base", "block": null, "base_tables": ["customer360__customer_value_analysis"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |


## S70

类别 `data`；来源 `python`；调用 `8da35c808ed84d73bf7b3799800757ea`；状态 `success`。

```sql

    SELECT marketo_lead_id, stripe_customer_id, zendesk_user_id, primary_email,
      investment_priority_score AS ips, product_adoption_rate AS par,
      support_resolution_efficiency AS sre, acquisition_cost AS acq,
      customer_lifetime_value AS clv, customer_onboarding_score AS onboarding, team_size,
      decision_maker_level AS dm, lifecycle_stage, industry_vertical, company_size_tier,
      digital_engagement_score AS digi_eng, nps_score AS nps,
      customer_health_score AS health, churn_probability AS churn,
      competitive_pressure_index AS cpi, renewal_probability AS renew,
      expansion_revenue_potential AS expansion, time_to_value_days AS ttv
    FROM customer360__customer_value_analysis
    LIMIT 2000 OFFSET 4000
    
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-055/attempt-01/sql/S70.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-055/attempt-01/sql/S70.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-055/attempt-01/results/S70.rows.jsonl)；完整：True；SHA256：`8322e4e107f55316fb709a48d923e79f5f4c91bd4af2d607db13ccd928e9f864`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "customer360__customer_value_analysis", "kind": "base", "block": null, "base_tables": ["customer360__customer_value_analysis"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |


## S71

类别 `data`；来源 `python`；调用 `8da35c808ed84d73bf7b3799800757ea`；状态 `success`。

```sql

SELECT email, MAX(total_sales_amount) AS total_sales_amount
FROM customer360__customer
WHERE total_sales_amount IS NOT NULL AND email IS NOT NULL
GROUP BY email

```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-055/attempt-01/sql/S71.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-055/attempt-01/sql/S71.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-055/attempt-01/results/S71.rows.jsonl)；完整：True；SHA256：`bfeb187d2a1f14916bd1c1bd97c021f3383741fcf63e5ba6bae40eef16f093a7`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "customer360__customer", "kind": "base", "block": null, "base_tables": ["customer360__customer"]}] | [] | ["email"] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | MAX(total_sales_amount) | [{"table": "customer360__customer", "column": "total_sales_amount"}] | [] | False |


## S72

类别 `data`；来源 `query_db`；调用 `6f954ddf4c33436f8f3733aac00689f3`；状态 `success`。

```sql
WITH base AS (
  SELECT DISTINCT v.primary_email, v.investment_priority_score, v.product_adoption_rate,
    v.support_resolution_efficiency, v.acquisition_cost, v.customer_lifetime_value,
    v.lifecycle_stage, v.industry_vertical, v.company_size_tier,
    v.customer_onboarding_score, v.team_size, v.decision_maker_level,
    c_sales.total_sales_amount
  FROM (
    SELECT DISTINCT * FROM customer360__customer_value_analysis
  ) v
  LEFT JOIN (
    SELECT email, MAX(total_sales_amount) AS total_sales_amount
    FROM customer360__customer
    WHERE total_sales_amount IS NOT NULL
    GROUP BY email
  ) c_sales ON v.primary_email = c_sales.email
  WHERE v.primary_email IS NOT NULL
),
scaled AS (
  SELECT *,
    (total_sales_amount - (SELECT MIN(total_sales_amount) FROM base)) / 
      NULLIF((SELECT MAX(total_sales_amount) - MIN(total_sales_amount) FROM base), 0) AS nsales,
    (product_adoption_rate - (SELECT MIN(product_adoption_rate) FROM base)) / 
      NULLIF((SELECT MAX(product_adoption_rate) - MIN(product_adoption_rate) FROM base), 0) AS nadopt,
    (support_resolution_efficiency - (SELECT MIN(support_resolution_efficiency) FROM base)) / 
      NULLIF((SELECT MAX(support_resolution_efficiency) - MIN(support_resolution_efficiency) FROM base), 0) AS nres
  FROM base
  WHERE product_adoption_rate IS NOT NULL AND support_resolution_efficiency IS NOT NULL
    AND total_sales_amount IS NOT NULL AND acquisition_cost IS NOT NULL AND customer_lifetime_value IS NOT NULL
),
with_comp AS (
  SELECT *, 0.4*nsales + 0.35*nadopt + 0.25*nres AS composite_score
  FROM scaled
),
ranked AS (
  SELECT *,
    ROW_NUMBER() OVER (ORDER BY investment_priority_score ASC) AS rn_ips_asc,
    ROW_NUMBER() OVER (ORDER BY composite_score ASC) AS rn_comp_asc,
    COUNT(*) OVER () AS total_cnt
  FROM with_comp
),
flagged AS (
  SELECT *, CASE WHEN rn_ips_asc >= 0.7*total_cnt AND rn_comp_asc <= 0.5*total_cnt THEN 1 ELSE 0 END AS is_target
  FROM ranked
)
SELECT is_target,
  COUNT(*) AS n,
  SUM(acquisition_cost) AS total_acq_cost,
  SUM(customer_lifetime_value) AS total_clv,
  SUM(total_sales_amount) AS total_sales,
  ROUND(100.0*SUM(acquisition_cost)/ (SELECT SUM(acquisition_cost) FROM flagged), 1) AS pct_of_total_acq,
  ROUND(100.0*SUM(customer_lifetime_value)/ (SELECT SUM(customer_lifetime_value) FROM flagged), 1) AS pct_of_total_clv,
  ROUND(100.0*SUM(total_sales_amount)/ (SELECT SUM(total_sales_amount) FROM flagged), 1) AS pct_of_total_sales
FROM flagged
GROUP BY is_target
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-055/attempt-01/sql/S72.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-055/attempt-01/sql/S72.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-055/attempt-01/results/S72.rows.jsonl)；完整：True；SHA256：`4d4fa2ba4ec50b89428cf676d14a045dbfe3db9e7eaf98dbc68df0e2ad94af00`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "customer360__customer_value_analysis", "kind": "base", "block": null, "base_tables": ["customer360__customer_value_analysis"]}] | [] | [] |
| B2 | [{"alias": "customer360__customer", "kind": "base", "block": null, "base_tables": ["customer360__customer"]}] | [] | ["email"] |
| B3 | [{"alias": "v", "kind": "derived", "block": "B1", "base_tables": ["customer360__customer_value_analysis"]}, {"alias": "c_sales", "kind": "derived", "block": "B2", "base_tables": ["customer360__customer"]}] | [{"type": "LEFT", "right": "(SELECT email, MAX(total_sales_amount) AS total_sales_amount FROM customer360__customer WHERE NOT total_sales_amount IS NULL GROUP BY email) AS c_sales", "on": "v.primary_email = c_sales.email", "using": []}] | [] |
| B4 | [{"alias": "base", "kind": "derived", "block": "B3", "base_tables": ["customer360__customer", "customer360__customer_value_analysis"]}] | [] | [] |
| B5 | [{"alias": "base", "kind": "derived", "block": "B3", "base_tables": ["customer360__customer", "customer360__customer_value_analysis"]}] | [] | [] |
| B6 | [{"alias": "base", "kind": "derived", "block": "B3", "base_tables": ["customer360__customer", "customer360__customer_value_analysis"]}] | [] | [] |
| B7 | [{"alias": "base", "kind": "derived", "block": "B3", "base_tables": ["customer360__customer", "customer360__customer_value_analysis"]}] | [] | [] |
| B8 | [{"alias": "base", "kind": "derived", "block": "B3", "base_tables": ["customer360__customer", "customer360__customer_value_analysis"]}] | [] | [] |
| B9 | [{"alias": "base", "kind": "derived", "block": "B3", "base_tables": ["customer360__customer", "customer360__customer_value_analysis"]}] | [] | [] |
| B10 | [{"alias": "base", "kind": "derived", "block": "B3", "base_tables": ["customer360__customer", "customer360__customer_value_analysis"]}] | [] | [] |
| B11 | [{"alias": "scaled", "kind": "derived", "block": "B10", "base_tables": ["customer360__customer", "customer360__customer_value_analysis"]}] | [] | [] |
| B12 | [{"alias": "with_comp", "kind": "derived", "block": "B11", "base_tables": ["customer360__customer", "customer360__customer_value_analysis"]}] | [] | [] |
| B13 | [{"alias": "ranked", "kind": "derived", "block": "B12", "base_tables": ["customer360__customer", "customer360__customer_value_analysis"]}] | [] | [] |
| B14 | [{"alias": "flagged", "kind": "derived", "block": "B13", "base_tables": ["customer360__customer", "customer360__customer_value_analysis"]}] | [] | [] |
| B15 | [{"alias": "flagged", "kind": "derived", "block": "B13", "base_tables": ["customer360__customer", "customer360__customer_value_analysis"]}] | [] | [] |
| B16 | [{"alias": "flagged", "kind": "derived", "block": "B13", "base_tables": ["customer360__customer", "customer360__customer_value_analysis"]}] | [] | [] |
| B17 | [{"alias": "flagged", "kind": "derived", "block": "B13", "base_tables": ["customer360__customer", "customer360__customer_value_analysis"]}] | [] | ["is_target"] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B2 | MAX(total_sales_amount) | [{"table": "customer360__customer", "column": "total_sales_amount"}] | [] | False |
| B4 | MIN(total_sales_amount) | [{"table": "customer360__customer", "column": "total_sales_amount"}] | [] | False |
| B5 | MAX(total_sales_amount) | [{"table": "customer360__customer", "column": "total_sales_amount"}] | [] | False |
| B5 | MIN(total_sales_amount) | [{"table": "customer360__customer", "column": "total_sales_amount"}] | [] | False |
| B6 | MIN(product_adoption_rate) | [{"table": "customer360__customer_value_analysis", "column": "product_adoption_rate"}] | [] | False |
| B7 | MAX(product_adoption_rate) | [{"table": "customer360__customer_value_analysis", "column": "product_adoption_rate"}] | [] | False |
| B7 | MIN(product_adoption_rate) | [{"table": "customer360__customer_value_analysis", "column": "product_adoption_rate"}] | [] | False |
| B8 | MIN(support_resolution_efficiency) | [{"table": "customer360__customer_value_analysis", "column": "support_resolution_efficiency"}] | [] | False |
| B9 | MAX(support_resolution_efficiency) | [{"table": "customer360__customer_value_analysis", "column": "support_resolution_efficiency"}] | [] | False |
| B9 | MIN(support_resolution_efficiency) | [{"table": "customer360__customer_value_analysis", "column": "support_resolution_efficiency"}] | [] | False |
| B14 | SUM(acquisition_cost) | [{"table": "customer360__customer_value_analysis", "column": "acquisition_cost"}] | [] | False |
| B15 | SUM(customer_lifetime_value) | [{"table": "customer360__customer_value_analysis", "column": "customer_lifetime_value"}] | [] | False |
| B16 | SUM(total_sales_amount) | [{"table": "customer360__customer", "column": "total_sales_amount"}] | [] | False |
| B17 | COUNT(*) | [] | [] | True |
| B17 | SUM(acquisition_cost) | [{"table": "customer360__customer_value_analysis", "column": "acquisition_cost"}] | [] | False |
| B17 | SUM(customer_lifetime_value) | [{"table": "customer360__customer_value_analysis", "column": "customer_lifetime_value"}] | [] | False |
| B17 | SUM(total_sales_amount) | [{"table": "customer360__customer", "column": "total_sales_amount"}] | [] | False |
| B17 | SUM(acquisition_cost) | [{"table": "customer360__customer_value_analysis", "column": "acquisition_cost"}] | [] | False |
| B17 | SUM(customer_lifetime_value) | [{"table": "customer360__customer_value_analysis", "column": "customer_lifetime_value"}] | [] | False |
| B17 | SUM(total_sales_amount) | [{"table": "customer360__customer", "column": "total_sales_amount"}] | [] | False |

