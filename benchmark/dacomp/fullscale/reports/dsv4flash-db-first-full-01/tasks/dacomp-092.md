# dacomp-092

First, from the `profitability_analysis` table, identify the high-volatility customer segm…

运行：已提交。官方未评分。全部 SQL 尝试/成功 70/68；数据 SQL 67/65；Python 5 次。

完整原题：

First, from the `profitability_analysis` table, identify the high-volatility customer segment ranking in the top 25% for `customer_margin_volatility`. Calculate the coefficient of variation (standard deviation / mean) of their `gross_profit` over the past 12 months and the variance of their quarter-over-quarter `invoice_total` growth rate to quantify their profit stability. Using behavioral features from the `customer_analytics` table such as `rfm_segment`, `payment_behavior`, and `revenue_trend_correlation`, explore the relationship between high volatility and customer lifecycle stages and payment patterns. By joining with `financial_dashboard` data, calculate the contribution of these customers to the overall `business_health_score` and the differential impact on `collection_rate_percentage`. Additionally, analyze the risk exposure distribution based on the accounts receivable structure from the `balance_sheet` table. Finally, build a multi-dimensional customer risk rating model that integrates volatility metrics, behavioral characteristics, and financial risks, and propose targeted customer management strategies.

| 表 | 行数 | 列数 |
| --- | --- | --- |
| quickbooks__balance_sheet | 111567 | 17 |
| quickbooks__customer_analytics | 2800 | 67 |
| quickbooks__financial_dashboard | 33 | 41 |
| quickbooks__profitability_analysis | 8000 | 35 |


实际路线（分析者依据 SQL/源码概括，不代表 Agent 自述）：SQL 客户波动及财务风险 → 同会话续接 → Python 统计检验、连接和再聚合 → 报告

数据库大小：29,724,672 字节。

## 数据 SQL

| SQL | 状态 | 基础表 | Join 输入/类型 | GROUP BY | 聚合表达式 | 结果行数 | 数据库 ms |
| --- | --- | --- | --- | --- | --- | --- | --- |
| [S3/Q1](#s3) | success | ["quickbooks__profitability_analysis"] | 0 / {} | [] | [] | 5 | 0.464 |
| [S4/Q2](#s4) | success | ["quickbooks__customer_analytics"] | 0 / {} | [] | [] | 5 | 0.505 |
| [S5/Q3](#s5) | success | ["quickbooks__financial_dashboard"] | 0 / {} | [] | [] | 5 | 0.438 |
| [S6/Q4](#s6) | success | ["quickbooks__balance_sheet"] | 0 / {} | [] | [] | 5 | 0.279 |
| [S7/Q5](#s7) | success | ["quickbooks__profitability_analysis"] | 0 / {} | [] | ["COUNT(*)"] | 1 | 2.357 |
| [S8/Q6](#s8) | success | ["quickbooks__customer_analytics"] | 0 / {} | [] | ["COUNT(*)"] | 1 | 0.629 |
| [S9/Q7](#s9) | success | ["quickbooks__financial_dashboard"] | 0 / {} | [] | ["COUNT(*)"] | 1 | 0.289 |
| [S10/Q8](#s10) | success | ["quickbooks__balance_sheet"] | 0 / {} | [] | ["COUNT(*)"] | 1 | 7.669 |
| [S11/Q9](#s11) | success | ["quickbooks__profitability_analysis"] | 0 / {} | [] | [] | 20 | 0.501 |
| [S12/Q10](#s12) | success | ["quickbooks__customer_analytics"] | 0 / {} | [] | [] | 20 | 0.375 |
| [S13/Q11](#s13) | success | ["quickbooks__profitability_analysis"] | 0 / {} | [] | ["MIN(transaction_date)", "MAX(transaction_date)"] | 1 | 2.272 |
| [S14/Q12](#s14) | success | ["quickbooks__customer_analytics"] | 0 / {} | [] | [] | 6 | 1.064 |
| [S15/Q13](#s15) | success | ["quickbooks__customer_analytics"] | 0 / {} | [] | [] | 4 | 0.904 |
| [S16/Q14](#s16) | success | ["quickbooks__customer_analytics"] | 0 / {} | [] | [] | 4 | 0.921 |
| [S17/Q15](#s17) | success | ["quickbooks__profitability_analysis"] | 0 / {} | [] | ["COUNT(DISTINCT customer_id)"] | 1 | 5.294 |
| [S18/Q16](#s18) | success | ["quickbooks__profitability_analysis"] | 0 / {} | ["customer_margin_volatility"] | ["COUNT(*)"] | 20 | 4.987 |
| [S19/Q17](#s19) | success | ["quickbooks__profitability_analysis"] | 0 / {} | ["customer_id"] | ["MAX(customer_margin_volatility)", "COUNT(*)", "MIN(vol)", "MAX(vol)", "AVG(vol)"] | 1 | 6.461 |
| [S20/Q18](#s20) | success | ["quickbooks__profitability_analysis"] | 0 / {} | ["customer_id"] | ["COUNT(DISTINCT customer_margin_volatility)", "COUNT(DISTINCT customer_margin_volatility)", "COUNT(DISTINCT customer_margin_volatility)"] | 5 | 4.322 |
| [S21/Q19](#s21) | success | ["quickbooks__profitability_analysis"] | 0 / {} | [] | [] | 2 | 1.85 |
| [S22/Q20](#s22) | success | ["quickbooks__profitability_analysis"] | 0 / {} | ["customer_id"] | ["AVG(customer_margin_volatility)"] | 5 | 11.134 |
| [S23/Q21](#s23) | failed | ["quickbooks__profitability_analysis"] | 0 / {} | ["customer_id"] | ["AVG(customer_margin_volatility)", "PERCENTILE_DISC(0.75)"] | unknown | 未取得；调用总时长 0.137 ms |
| [S24/Q22](#s24) | success | ["quickbooks__profitability_analysis"] | 0 / {} | ["customer_id"] | ["AVG(customer_margin_volatility)"] | 1 | 9.365 |
| [S25/Q23](#s25) | success | ["quickbooks__profitability_analysis"] | 0 / {} | ["customer_id"] | ["AVG(customer_margin_volatility)", "COUNT(*)"] | 1 | 11.215 |
| [S26/Q24](#s26) | success | ["quickbooks__profitability_analysis"] | 0 / {} | [] | ["MIN(transaction_date)", "MAX(transaction_date)"] | 1 | 2.089 |
| [S27/Q25](#s27) | success | ["quickbooks__profitability_analysis"] | 2 / {'INNER': 1} | ["customer_id"] | ["MAX(transaction_date)", "AVG(customer_margin_volatility)"] | 20 | 1509.444 |
| [S28/Q26](#s28) | failed | ["quickbooks__profitability_analysis"] | 2 / {'INNER': 1} | ["customer_id", "h.customer_id", "h.vol"] | ["MAX(transaction_date)", "AVG(customer_margin_volatility)", "AVG(p.gross_profit)", "STDDEV(p.gross_profit)", "COUNT(p.gross_profit)", "STDDEV(p.gross_profit)", "AVG(p.gross_profit)", "AVG(p.gross_profit)"] | unknown | 未取得；调用总时长 0.238 ms |
| [S29/Q27](#s29) | success | ["quickbooks__profitability_analysis"] | 2 / {'INNER': 1} | ["customer_id", "h.customer_id", "h.vol"] | ["MAX(transaction_date)", "AVG(customer_margin_volatility)", "AVG(p.gross_profit)", "COUNT(p.gross_profit)", "AVG(p.gross_profit * p.gross_profit)", "AVG(p.gross_profit)", "AVG(p.gross_profit)"] | 20 | 1215.476 |
| [S30/Q28](#s30) | success | ["quickbooks__profitability_analysis"] | 2 / {'INNER': 1} | ["customer_id", "h.customer_id", "STRFTIME('%Y-%m', p.transaction_date)", "customer_id"] | ["MAX(transaction_date)", "AVG(customer_margin_volatility)", "SUM(p.gross_profit)", "AVG(monthly_gp)", "COUNT(*)", "AVG(monthly_gp * monthly_gp)", "AVG(monthly_gp)", "AVG(monthly_gp)"] | 15 | 1222.127 |
| [S31/Q29](#s31) | success | ["quickbooks__profitability_analysis"] | 2 / {'INNER': 1} | ["customer_id", "h.customer_id", "STRFTIME('%Y-%m', p.transaction_date)"] | ["MAX(transaction_date)", "AVG(customer_margin_volatility)", "SUM(p.gross_profit)", "AVG(monthly_gp)", "COUNT(*)", "COUNT(DISTINCT customer_id)", "AVG(monthly_gp * monthly_gp)", "AVG(monthly_gp)", "AVG(monthly_gp)", "AVG(monthly_gp)", "AVG(monthly_gp * monthly_gp)", "AVG(monthly_gp)", "AVG(monthly_gp)"] | 1 | 1226.476 |
| [S32/Q30](#s32) | success | ["quickbooks__profitability_analysis"] | 0 / {} | ["revenue_year", "revenue_quarter"] | ["COUNT(*)"] | 11 | 3.856 |
| [S33/Q31](#s33) | success | ["quickbooks__profitability_analysis"] | 0 / {} | ["customer_id"] | ["AVG(customer_margin_volatility)", "COUNT(*)"] | 1 | 11.212 |
| [S34/Q32](#s34) | success | ["quickbooks__profitability_analysis"] | 2 / {'INNER': 1} | ["customer_id", "h.customer_id", "STRFTIME('%Y', p.transaction_date)", "CAST((CAST(STRFTIME('%m', p.transaction_date) AS INTEGER) + 2) / 3 AS INTEGER)"] | ["MAX(transaction_date)", "AVG(customer_margin_volatility)", "SUM(p.invoice_total)"] | 30 | 1225.357 |
| [S35/Q33](#s35) | success | ["quickbooks__profitability_analysis"] | 2 / {'INNER': 1} | ["customer_id", "h.customer_id", "STRFTIME('%Y', p.transaction_date)", "CAST((CAST(STRFTIME('%m', p.transaction_date) AS INTEGER) + 2) / 3 AS INTEGER)"] | ["MAX(transaction_date)", "AVG(customer_margin_volatility)", "SUM(p.invoice_total)", "AVG(qoq_growth)", "COUNT(*)", "AVG(qoq_growth * qoq_growth)", "AVG(qoq_growth)", "AVG(qoq_growth)", "AVG(qoq_growth * qoq_growth)", "AVG(qoq_growth)", "AVG(qoq_growth)"] | 1 | 1219.233 |
| [S36/Q34](#s36) | success | ["quickbooks__customer_analytics", "quickbooks__profitability_analysis"] | 2 / {'INNER': 1} | ["customer_id", "s.vol_segment", "a.rfm_segment"] | ["AVG(customer_margin_volatility)", "COUNT(*)"] | 18 | 1122.652 |
| [S37/Q35](#s37) | success | ["quickbooks__customer_analytics", "quickbooks__profitability_analysis"] | 2 / {'INNER': 1} | ["customer_id", "s.vol_segment", "a.payment_behavior"] | ["AVG(customer_margin_volatility)", "COUNT(*)"] | 12 | 1092.178 |
| [S38/Q36](#s38) | success | ["quickbooks__customer_analytics", "quickbooks__profitability_analysis"] | 2 / {'INNER': 1} | ["customer_id", "s.vol_segment", "a.lifecycle_stage"] | ["AVG(customer_margin_volatility)", "COUNT(*)"] | 12 | 1108.684 |
| [S39/Q37](#s39) | success | ["quickbooks__customer_analytics", "quickbooks__profitability_analysis"] | 2 / {'INNER': 1} | ["customer_id", "s.vol_segment"] | ["AVG(customer_margin_volatility)", "COUNT(*)", "AVG(a.revenue_trend_correlation)", "AVG(a.credit_score)", "AVG(a.avg_payment_days_12m)", "AVG(a.overdue_count_12m)", "AVG(a.overall_customer_score)", "AVG(a.revenue_volatility)"] | 3 | 1114.568 |
| [S40/Q38](#s40) | success | ["quickbooks__customer_analytics"] | 0 / {} | [] | ["COUNT(*)", "COUNT(revenue_trend_correlation)", "COUNT(credit_score)", "COUNT(avg_payment_days_12m)", "COUNT(overdue_count_12m)", "COUNT(overall_customer_score)", "COUNT(revenue_volatility)", "COUNT(rfm_segment)", "COUNT(payment_behavior)", "COUNT(lifecycle_stage)", "COUNT(customer_value_segment)", "COUNT(risk_assessment)", "COUNT(credit_grade)", "COUNT(payment_timeliness_score)", "COUNT(business_stability_score)"] | 1 | 2.154 |
| [S42/Q39](#s42) | success | ["quickbooks__customer_analytics"] | 0 / {} | [] | ["COUNT(*)", "COUNT(customer_value_segment)", "COUNT(business_stability_score)", "COUNT(activity_status)", "COUNT(customer_maturity_stage)", "COUNT(revenue_growth_rate_12m)", "COUNT(active_months_last_12)", "COUNT(payment_rate_percentage)", "COUNT(data_quality_flag)", "COUNT(recommended_action)"] | 1 | 2.085 |
| [S43/Q40](#s43) | success | ["quickbooks__customer_analytics"] | 0 / {} | [] | [] | 3 | 0.941 |
| [S44/Q41](#s44) | success | ["quickbooks__customer_analytics", "quickbooks__profitability_analysis"] | 2 / {'INNER': 1} | ["customer_id", "s.vol_segment", "a.customer_value_segment"] | ["AVG(customer_margin_volatility)", "COUNT(*)", "COUNT(*)", "COUNT(*)"] | 9 | 637.955 |
| [S45/Q42](#s45) | success | ["quickbooks__customer_analytics", "quickbooks__profitability_analysis"] | 2 / {'INNER': 1} | ["customer_id", "s.vol_segment"] | ["AVG(customer_margin_volatility)", "COUNT(*)", "AVG(a.business_stability_score)", "AVG(a.active_months_last_12)", "AVG(a.revenue_growth_rate_12m)", "AVG(a.revenue_trend_correlation)", "AVG(a.revenue_volatility)", "AVG(a.days_since_last_invoice)"] | 3 | 632.93 |
| [S46/Q43](#s46) | success | ["quickbooks__financial_dashboard"] | 0 / {} | [] | [] | 33 | 0.46 |
| [S47/Q44](#s47) | success | ["quickbooks__profitability_analysis"] | 2 / {'LEFT': 1} | ["customer_id", "p.revenue_month_start", "CASE WHEN NOT h.customer_id IS NULL THEN 'HighVol' ELSE 'Other' END", "m.revenue_month_start"] | ["AVG(customer_margin_volatility)", "SUM(p.invoice_total)", "SUM(p.gross_profit)", "SUM(p.outstanding_balance)", "SUM(CASE WHEN grp = 'HighVol' THEN invoice_total ELSE 0 END)", "SUM(invoice_total)", "SUM(CASE WHEN grp = 'HighVol' THEN gross_profit ELSE 0 END)", "SUM(gross_profit)", "SUM(invoice_total)", "SUM(CASE WHEN grp = 'HighVol' THEN invoice_total ELSE 0 END)", "SUM(CASE WHEN grp = 'HighVol' THEN gross_profit ELSE 0 END)", "SUM(gross_profit)"] | 19 | 1824.854 |
| [S48/Q45](#s48) | success | ["quickbooks__financial_dashboard", "quickbooks__profitability_analysis"] | 2 / {'LEFT': 1, 'INNER': 1} | ["customer_id", "p.revenue_month_start"] | ["AVG(customer_margin_volatility)", "SUM(CASE WHEN NOT h.customer_id IS NULL THEN p.invoice_total ELSE 0 END)", "SUM(p.invoice_total)", "SUM(CASE WHEN NOT h.customer_id IS NULL THEN p.gross_profit ELSE 0 END)", "SUM(p.gross_profit)"] | 19 | 1813.264 |
| [S49/Q46](#s49) | success | ["quickbooks__balance_sheet"] | 0 / {} | [] | [] | 7 | 20.007 |
| [S50/Q47](#s50) | success | ["quickbooks__balance_sheet"] | 0 / {} | ["account_type", "account_sub_type"] | ["COUNT(*)", "SUM(amount)"] | 5 | 34.461 |
| [S51/Q48](#s51) | success | ["quickbooks__balance_sheet"] | 0 / {} | ["account_sub_type"] | ["COUNT(DISTINCT calendar_date)", "MIN(calendar_date)", "MAX(calendar_date)", "SUM(amount)", "SUM(converted_amount)"] | 4 | 15.303 |
| [S52/Q49](#s52) | success | ["quickbooks__balance_sheet"] | 0 / {} | ["calendar_date", "account_sub_type"] | ["MAX(calendar_date)", "SUM(amount)"] | 4 | 29.5 |
| [S53/Q50](#s53) | success | ["quickbooks__balance_sheet"] | 0 / {} | ["account_sub_type"] | ["SUM(amount)", "SUM(amount)", "SUM(amount)"] | 4 | 15.33 |
| [S54/Q51](#s54) | success | ["quickbooks__balance_sheet"] | 0 / {} | ["calendar_date"] | ["SUM(CASE WHEN account_sub_type = 'Current (0-30 days)' THEN amount ELSE 0 END)", "SUM(CASE WHEN account_sub_type <> 'Current (0-30 days)' THEN amount ELSE 0 END)", "SUM(amount)", "SUM(CASE WHEN account_sub_type <> 'Current (0-30 days)' THEN amount ELSE 0 END)", "SUM(amount)"] | 24 | 15.376 |
| [S55/Q52](#s55) | success | ["quickbooks__profitability_analysis"] | 2 / {'LEFT': 1} | ["customer_id", "CASE WHEN NOT h.customer_id IS NULL THEN 'HighVol' ELSE 'Other' END"] | ["AVG(customer_margin_volatility)", "SUM(p.outstanding_balance)", "SUM(p.invoice_total)", "SUM(p.collected_amount)", "COUNT(*)", "COUNT(DISTINCT p.customer_id)"] | 2 | 1788.843 |
| [S56/Q53](#s56) | success | ["quickbooks__profitability_analysis"] | 2 / {'INNER': 1} | ["customer_id", "s.vol_segment"] | ["AVG(customer_margin_volatility)", "SUM(p.outstanding_balance)", "SUM(p.invoice_total)", "SUM(p.collected_amount)", "COUNT(DISTINCT s.customer_id)", "SUM(p.outstanding_balance)", "SUM(p.invoice_total)"] | 3 | 4949.593 |
| [S57/Q54](#s57) | success | ["quickbooks__customer_analytics", "quickbooks__profitability_analysis"] | 3 / {'INNER': 2} | ["customer_id", "customer_id"] | ["AVG(customer_margin_volatility)", "SUM(invoice_total)", "SUM(outstanding_balance)", "SUM(collected_amount)", "COUNT(*)", "AVG(invoice_gross_margin_pct)"] | 15 | 1115.429 |
| [S58/Q55](#s58) | success | ["quickbooks__customer_analytics", "quickbooks__profitability_analysis"] | 2 / {'INNER': 1} | ["customer_id"] | ["AVG(customer_margin_volatility)"] | 20 | 1081.985 |
| [S59/Q56](#s59) | success | ["quickbooks__customer_analytics", "quickbooks__profitability_analysis"] | 2 / {'INNER': 1} | ["customer_id", "risk_tier"] | ["AVG(customer_margin_volatility)", "COUNT(*)", "AVG(composite_risk)", "COUNT(*)"] | 3 | 1109.919 |
| [S60/Q57](#s60) | success | ["quickbooks__customer_analytics", "quickbooks__profitability_analysis"] | 2 / {'INNER': 2} | ["customer_id", "s.vol_segment", "r.risk_tier"] | ["AVG(customer_margin_volatility)", "COUNT(*)", "COUNT(*)", "COUNT(*)"] | 8 | 4985.19 |
| [S61/Q58](#s61) | success | ["quickbooks__profitability_analysis"] | 2 / {'INNER': 1} | ["customer_id", "h.customer_id", "STRFTIME('%Y', p.transaction_date)", "CAST((CAST(STRFTIME('%m', p.transaction_date) AS INTEGER) + 2) / 3 AS INTEGER)"] | ["MAX(transaction_date)", "AVG(customer_margin_volatility)", "SUM(p.invoice_total)", "AVG(qoq_growth)", "COUNT(*)", "AVG(qoq_growth * qoq_growth)", "AVG(qoq_growth)", "AVG(qoq_growth)", "AVG(qoq_growth * qoq_growth)", "AVG(qoq_growth)", "AVG(qoq_growth)"] | 1 | 1278.018 |
| [S62/Q59](#s62) | success | ["quickbooks__profitability_analysis"] | 2 / {'INNER': 1} | ["customer_id", "h.customer_id", "STRFTIME('%Y-%m', p.transaction_date)"] | ["MAX(transaction_date)", "AVG(customer_margin_volatility)", "SUM(p.gross_profit)", "AVG(monthly_gp)", "COUNT(*)", "COUNT(DISTINCT customer_id)", "AVG(monthly_gp * monthly_gp)", "AVG(monthly_gp)", "AVG(monthly_gp)", "AVG(monthly_gp)", "AVG(monthly_gp * monthly_gp)", "AVG(monthly_gp)", "AVG(monthly_gp)"] | 1 | 1268.152 |
| [S63/Q60](#s63) | success | ["quickbooks__profitability_analysis"] | 0 / {} | ["customer_id"] | ["AVG(customer_margin_volatility)"] | 2800 | 14.105 |
| [S64/Q61](#s64) | success | ["quickbooks__profitability_analysis"] | 0 / {} | ["customer_id", "STRFTIME('%Y-%m', transaction_date)"] | ["MAX(transaction_date)", "SUM(gross_profit)"] | 5064 | 17.404 |
| [S65/Q62](#s65) | success | ["quickbooks__customer_analytics", "quickbooks__profitability_analysis"] | 2 / {'INNER': 1} | ["customer_id"] | ["AVG(customer_margin_volatility)"] | 2800 | 1095.939 |
| [S66/Q63](#s66) | success | ["quickbooks__customer_analytics", "quickbooks__profitability_analysis"] | 2 / {'INNER': 2} | ["customer_id", "r.risk_tier"] | ["AVG(customer_margin_volatility)", "SUM(outstanding_balance)", "COUNT(DISTINCT r.customer_id)", "SUM(p.invoice_total)", "SUM(p.outstanding_balance)", "SUM(p.gross_profit)", "SUM(p.outstanding_balance)"] | 3 | 1150.361 |
| [S67/Q64](#s67) | success | ["quickbooks__customer_analytics", "quickbooks__profitability_analysis"] | 2 / {'INNER': 1} | ["customer_id"] | ["AVG(customer_margin_volatility)", "COUNT(*)", "SUM(CASE WHEN payment_behavior = 'Poor' THEN 1 ELSE 0 END)", "SUM(CASE WHEN rfm_segment = 'At Risk' THEN 1 ELSE 0 END)", "SUM(CASE WHEN revenue_trend_correlation < 0 THEN 1 ELSE 0 END)", "AVG(business_stability_score)", "AVG(active_months_last_12)", "AVG(revenue_growth_rate_12m)", "AVG(vol)"] | 1 | 1083.722 |
| [S68/Q65](#s68) | success | ["quickbooks__profitability_analysis"] | 0 / {} | [] | [] | 3 | 2.419 |
| [S69/Q66](#s69) | success | ["quickbooks__profitability_analysis"] | 0 / {} | [] | [] | 16 | 3.425 |
| [S70/Q67](#s70) | success | ["quickbooks__profitability_analysis"] | 2 / {'INNER': 1} | ["customer_id", "s.vol_segment", "p.profitability_sustainability"] | ["AVG(customer_margin_volatility)", "COUNT(*)", "COUNT(*)", "COUNT(*)"] | 9 | 4842.798 |


## 元数据和设置

| SQL | 类别 | 状态 | 内容 |
| --- | --- | --- | --- |
| S1 | connection_setup | success | PRAGMA query_only=ON |
| S2 | metadata | success | SELECT name,sql FROM sqlite_master WHERE type='table' ORDER BY name |
| S41 | connection_setup | success | PRAGMA query_only=ON |


## Python 与执行位置

人工源码审查：**database_first_violation**。SQL 已完成主体筛选及月度聚合，Python 仍将客户月度结果与波动分组 merge，并再次按客户聚合均值、标准差、计数，及按分组计算负增长占比；关系连接、计数、均值可下推 SQL。相关检验与分布绘图另属统计和可视化补充。 [证据](../reviews/dacomp-092.json)。

P1：Compute Pearson correlations between high-vol customer revenue share and business health score/collection rate, perform statistical tests, and create visualizations. This is statistical analysis best done outside SQL.

[源码](../../../runs/dsv4flash-db-first-full-01/dacomp-092/attempt-01/python/P1.py)；[输出](../../../runs/dsv4flash-db-first-full-01/dacomp-092/attempt-01/python/P1.stdout)；[错误](../../../runs/dsv4flash-db-first-full-01/dacomp-092/attempt-01/python/P1.stderr)。自动源码筛查未检出预设迁出信号；这不是全面语义合规证明。

P2：Create visualizations for the risk model distribution, behavioral profile comparison, and the multi-dimensional risk rating framework.

[源码](../../../runs/dsv4flash-db-first-full-01/dacomp-092/attempt-01/python/P2.py)；[输出](../../../runs/dsv4flash-db-first-full-01/dacomp-092/attempt-01/python/P2.stdout)；[错误](../../../runs/dsv4flash-db-first-full-01/dacomp-092/attempt-01/python/P2.stderr)。自动源码筛查未检出预设迁出信号；这不是全面语义合规证明。

P3：Compute exact payment behavior percentages and chi-square test for association between volatility segment and payment behavior. This is a statistical test best done in Python.

[源码](../../../runs/dsv4flash-db-first-full-01/dacomp-092/attempt-01/python/P3.py)；[输出](../../../runs/dsv4flash-db-first-full-01/dacomp-092/attempt-01/python/P3.stdout)；[错误](../../../runs/dsv4flash-db-first-full-01/dacomp-092/attempt-01/python/P3.stderr)。自动源码筛查未检出预设迁出信号；这不是全面语义合规证明。

P4：Compute customer-level profit stability (CV of gross profit per customer) and compare distributions between volatility segments with statistical tests, plus analyze revenue trend correlation distribution.

[源码](../../../runs/dsv4flash-db-first-full-01/dacomp-092/attempt-01/python/P4.py)；[输出](../../../runs/dsv4flash-db-first-full-01/dacomp-092/attempt-01/python/P4.stdout)；[错误](../../../runs/dsv4flash-db-first-full-01/dacomp-092/attempt-01/python/P4.stderr)。检出需人工核验的 SQL 可实现操作：groupby(, .merge(, .query(；不能仅凭理由判为合规。

P5：Compute differential impact of high-vol customer share on business health score and collection rate by comparing high-share vs low-share months. This requires the joined monthly data assembled in Python.

[源码](../../../runs/dsv4flash-db-first-full-01/dacomp-092/attempt-01/python/P5.py)；[输出](../../../runs/dsv4flash-db-first-full-01/dacomp-092/attempt-01/python/P5.stdout)；[错误](../../../runs/dsv4flash-db-first-full-01/dacomp-092/attempt-01/python/P5.stderr)。自动源码筛查未检出预设迁出信号；这不是全面语义合规证明。

## 优化机会

已验证候选; original verified selection retained across continuation。筛选限于精确 SQL、相同自包含 CTE、相同单表完整过滤、可分解单表聚合；未覆盖任意 Join 等价和一般谓词蕴含。全部候选都是 offline，未测在线预测。

| 候选 | 类型 | 已有结果 | 覆盖 SQL | 后续次数 | 中间行数 | 验证 | 成本 |
| --- | --- | --- | --- | --- | --- | --- | --- |
| C1 | exact-result reuse | True | ["S13", "S26"] | 1 | unknown | not_verified_cap | Not tested |
| C2 | common subexpression | False | ["S22", "S24", "S25", "S27", "S29", "S30", "S31", "S33", "S34", "S35", "S36", "S37", "S38", "S39"] | 13 | 2800 | verified | Warm-cache baseline 11838.925 ms vs build+reuse 144.199 ms, ratio 82.101; five repetitions, see performance evidence. |
| C3 | common subexpression | False | ["S27", "S29", "S30", "S31", "S34", "S35"] | 5 | 1 | verified | Not benchmarked; correctness alone does not establish net speedup. |
| C4 | aggregate MV | False | ["S7", "S32"] | 1 | 11 | verified | Not benchmarked; correctness alone does not establish net speedup. |
| C5 | aggregate MV | False | ["S8", "S40"] | 1 | unknown | not_verified_cap | Not tested |
| C6 | common subexpression | False | ["S22", "S24", "S25", "S27", "S29", "S30", "S31", "S33", "S34", "S35", "S36", "S37", "S38", "S39", "S44", "S45", "S47", "S48", "S55", "S56", "S57", "S58", "S59", "S60", "S61", "S62", "S63", "S65", "S66", "S67", "S70"] | 30 | unknown | not_verified_cap | Final continuation candidate enumerated only; original per-task three-case verification selection retained. |
| C7 | common subexpression | False | ["S27", "S29", "S30", "S31", "S34", "S35", "S61", "S62", "S64"] | 8 | unknown | not_verified_cap | Final continuation candidate enumerated only; original per-task three-case verification selection retained. |
| C8 | aggregate MV | False | ["S8", "S40", "S42"] | 2 | unknown | not_verified_cap | Final continuation candidate enumerated only; original per-task three-case verification selection retained. |
| C9 | common filtered view | False | ["S51", "S54"] | 1 | unknown | not_verified_cap | Final continuation candidate enumerated only; original per-task three-case verification selection retained. |


已验证覆盖（含触发查询、候选并集去重）：16/65 条成功数据 SQL。正确性仅针对当前数据库快照；未测性能的候选不能声称已加速。

[完整 build/rewrite 与比较证据](dacomp-092.analysis.json)。

### C2：common subexpression

Identical self-contained CTE body across queries.

原查询 [S22](#s22), [S24](#s24), [S25](#s25), [S27](#s27), [S29](#s29), [S30](#s30), [S31](#s31), [S33](#s33), [S34](#s34), [S35](#s35), [S36](#s36), [S37](#s37), [S38](#s38), [S39](#s39) → 新增共享状态 C2 → 后续 13 次可复用。该构建点为事后假设，不代表 Agent 当时预知后续。

构建定义：

```sql
SELECT customer_id, AVG(customer_margin_volatility) AS vol FROM quickbooks__profitability_analysis GROUP BY customer_id
```

受益查询 S22 的改写示例：

```sql
WITH cust_vol AS (SELECT * FROM temp.reuse_candidate), ordered AS (SELECT customer_id, vol, ROW_NUMBER() OVER (ORDER BY vol DESC) AS rn, COUNT(*) OVER () AS total FROM cust_vol) SELECT * FROM ordered WHERE rn IN (700, 701, 2100, 2101) OR rn = 2800
```

| 原 SQL | 列名一致 | 结果一致 | 比较方法 |
| --- | --- | --- | --- |
| S22 | True | True | exact_multiset |
| S24 | True | True | exact_multiset |
| S25 | True | True | exact_multiset |
| S27 | True | True | ordered_numeric_tolerance |
| S29 | True | True | ordered_numeric_tolerance |
| S30 | True | True | ordered_numeric_tolerance |
| S31 | True | True | exact_multiset |
| S33 | True | True | exact_multiset |
| S34 | True | True | ordered_numeric_tolerance |
| S35 | True | True | exact_multiset |
| S36 | True | True | ordered_numeric_tolerance |
| S37 | True | True | ordered_numeric_tolerance |
| S38 | True | True | ordered_numeric_tolerance |
| S39 | True | True | ordered_numeric_tolerance |


验证状态：verified；成本结论：Warm-cache baseline 11838.925 ms vs build+reuse 144.199 ms, ratio 82.101; five repetitions, see performance evidence.

### C3：common subexpression

Identical self-contained CTE body across queries.

原查询 [S27](#s27), [S29](#s29), [S30](#s30), [S31](#s31), [S34](#s34), [S35](#s35) → 新增共享状态 C3 → 后续 5 次可复用。该构建点为事后假设，不代表 Agent 当时预知后续。

构建定义：

```sql
SELECT DATE(MAX(transaction_date), '-12 months') AS cutoff_date FROM quickbooks__profitability_analysis
```

受益查询 S27 的改写示例：

```sql
/* Define the past 12 months date range */ WITH date_range AS (SELECT * FROM temp.reuse_candidate), cust_vol /* High volatility customers (top 25%) */ AS (SELECT customer_id, AVG(customer_margin_volatility) AS vol FROM quickbooks__profitability_analysis GROUP BY customer_id), ordered AS (SELECT customer_id, vol, ROW_NUMBER() OVER (ORDER BY vol DESC) AS rn, COUNT(*) OVER () AS total FROM cust_vol), high_vol_cust AS (SELECT customer_id, vol FROM ordered WHERE rn <= total * 0.25) /* Get gross_profit data for past 12 months */ SELECT h.customer_id, h.vol, p.gross_profit, p.transaction_date FROM high_vol_cust AS h JOIN quickbooks__profitability_analysis AS p ON h.customer_id = p.customer_id WHERE p.transaction_date >= (SELECT cutoff_date FROM date_range) ORDER BY h.vol DESC, h.customer_id, p.transaction_date LIMIT 20
```

| 原 SQL | 列名一致 | 结果一致 | 比较方法 |
| --- | --- | --- | --- |
| S27 | True | True | ordered_numeric_tolerance |
| S29 | True | True | ordered_numeric_tolerance |
| S30 | True | True | ordered_numeric_tolerance |
| S31 | True | True | exact_multiset |
| S34 | True | True | ordered_numeric_tolerance |
| S35 | True | True | exact_multiset |


验证状态：verified；成本结论：Not benchmarked; correctness alone does not establish net speedup.

### C4：aggregate MV

Union of grouping keys; decomposable aggregate states; AVG uses SUM and non-NULL COUNT.

原查询 [S7](#s7), [S32](#s32) → 新增共享状态 C4 → 后续 1 次可复用。该构建点为事后假设，不代表 Agent 当时预知后续。

构建定义：

```sql
SELECT revenue_year AS __g0, revenue_quarter AS __g1, COUNT(*) AS __a0 FROM "quickbooks__profitability_analysis"  GROUP BY revenue_year, revenue_quarter
```

受益查询 S7 的改写示例：

```sql
SELECT SUM(__a0) AS cnt FROM temp.reuse_candidate
```

| 原 SQL | 列名一致 | 结果一致 | 比较方法 |
| --- | --- | --- | --- |
| S7 | True | True | exact_multiset |
| S32 | True | True | ordered_numeric_tolerance |


验证状态：verified；成本结论：Not benchmarked; correctness alone does not establish net speedup.

[性能证据 C2](dacomp-092.C2.performance.json)：measured。

结果依赖：自动记录 SQL→Python 的接口父调用，以及源码中引用归档文件的消费者；字面值相同不认定因果。模型方向选择需要人工读取消息，尚未做全面因果标注。

[原始报告](../../../runs/dsv4flash-db-first-full-01/dacomp-092/attempt-01/answer.md)；[统一消息](../../../runs/dsv4flash-db-first-full-01/dacomp-092/attempt-01/messages.jsonl)；[原始 OpenCode 事件](../../../runs/dsv4flash-db-first-full-01/dacomp-092/attempt-01/opencode.jsonl)；[SQL 引擎日志](../../../runs/dsv4flash-db-first-full-01/dacomp-092/attempt-01/sql_journal.jsonl)。

[可读报告（本地图片链接规范化）](../answers/dacomp-092.md)。原始回答保留，分析结论未改写。

## S1

类别 `connection_setup`；来源 `connection`；调用 `506bca2386aa4963a844de9246db49e5`；状态 `success`。

```sql
PRAGMA query_only=ON
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-092/attempt-01/sql/S1.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-092/attempt-01/sql/S1.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-092/attempt-01/results/S1.rows.jsonl)；完整：True；SHA256：`e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`。

## S2

类别 `metadata`；来源 `list_db`；调用 `506bca2386aa4963a844de9246db49e5`；状态 `success`。

```sql
SELECT name,sql FROM sqlite_master WHERE type='table' ORDER BY name
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-092/attempt-01/sql/S2.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-092/attempt-01/sql/S2.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-092/attempt-01/results/S2.rows.jsonl)；完整：True；SHA256：`13b37ef047190e51a0ed33de050139ac8e4a18b2ba28908cfe985a7fecc06ed3`。

## S3

类别 `data`；来源 `query_db`；调用 `de273ce44b084d1f8b7dbc0dc717a87b`；状态 `success`。

```sql
SELECT * FROM quickbooks__profitability_analysis LIMIT 5
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-092/attempt-01/sql/S3.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-092/attempt-01/sql/S3.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-092/attempt-01/results/S3.rows.jsonl)；完整：True；SHA256：`2bc178207d2c020c85674f0420e6358f8d46f4038f454185b88d8a1f1b1ed7d8`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "quickbooks__profitability_analysis", "kind": "base", "block": null, "base_tables": ["quickbooks__profitability_analysis"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |


## S4

类别 `data`；来源 `query_db`；调用 `63fd74b7b1734039afb0dcf2b542c67b`；状态 `success`。

```sql
SELECT * FROM quickbooks__customer_analytics LIMIT 5
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-092/attempt-01/sql/S4.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-092/attempt-01/sql/S4.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-092/attempt-01/results/S4.rows.jsonl)；完整：True；SHA256：`67effb61e8a88a8846e08780be72a610f9dce4ff408c8786fe6c4604a60609d1`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "quickbooks__customer_analytics", "kind": "base", "block": null, "base_tables": ["quickbooks__customer_analytics"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |


## S5

类别 `data`；来源 `query_db`；调用 `a9185b01a1eb4fb59b54e2375d0b96f7`；状态 `success`。

```sql
SELECT * FROM quickbooks__financial_dashboard LIMIT 5
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-092/attempt-01/sql/S5.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-092/attempt-01/sql/S5.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-092/attempt-01/results/S5.rows.jsonl)；完整：True；SHA256：`d435077a9029b37a079800dd5ec5baa989d231f4e69a436881883b6253babdb3`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "quickbooks__financial_dashboard", "kind": "base", "block": null, "base_tables": ["quickbooks__financial_dashboard"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |


## S6

类别 `data`；来源 `query_db`；调用 `675b59cf66e54389a70218521da4213f`；状态 `success`。

```sql
SELECT * FROM quickbooks__balance_sheet LIMIT 5
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-092/attempt-01/sql/S6.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-092/attempt-01/sql/S6.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-092/attempt-01/results/S6.rows.jsonl)；完整：True；SHA256：`4c0fb82b5d1605806b7da8968dad65976775b1f2f6daafa5a7bdfcea0ffe16e4`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "quickbooks__balance_sheet", "kind": "base", "block": null, "base_tables": ["quickbooks__balance_sheet"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |


## S7

类别 `data`；来源 `query_db`；调用 `686431f034374e2796a86d6a895d4b12`；状态 `success`。

```sql
SELECT COUNT(*) as cnt FROM quickbooks__profitability_analysis
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-092/attempt-01/sql/S7.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-092/attempt-01/sql/S7.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-092/attempt-01/results/S7.rows.jsonl)；完整：True；SHA256：`ca5d97f4dab69813055999493cfea8f56e91e334c1465da9867b484a21b0a9bd`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "quickbooks__profitability_analysis", "kind": "base", "block": null, "base_tables": ["quickbooks__profitability_analysis"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |


## S8

类别 `data`；来源 `query_db`；调用 `cd00c464c33e47f989e8308daff6cefd`；状态 `success`。

```sql
SELECT COUNT(*) as cnt FROM quickbooks__customer_analytics
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-092/attempt-01/sql/S8.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-092/attempt-01/sql/S8.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-092/attempt-01/results/S8.rows.jsonl)；完整：True；SHA256：`409ab31294c9429f03e9f17a7e49ebfac259b29f8ad8ca8c4d51de2ef93bb943`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "quickbooks__customer_analytics", "kind": "base", "block": null, "base_tables": ["quickbooks__customer_analytics"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |


## S9

类别 `data`；来源 `query_db`；调用 `dee31b0d667a4099b971b198f961fec8`；状态 `success`。

```sql
SELECT COUNT(*) as cnt FROM quickbooks__financial_dashboard
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-092/attempt-01/sql/S9.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-092/attempt-01/sql/S9.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-092/attempt-01/results/S9.rows.jsonl)；完整：True；SHA256：`1315f0f7efc386feec13fc4575d19a3dcdd07d1b61de1fe595d7dec48df1079a`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "quickbooks__financial_dashboard", "kind": "base", "block": null, "base_tables": ["quickbooks__financial_dashboard"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |


## S10

类别 `data`；来源 `query_db`；调用 `cf2e55437b314605af287184bca15368`；状态 `success`。

```sql
SELECT COUNT(*) as cnt FROM quickbooks__balance_sheet
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-092/attempt-01/sql/S10.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-092/attempt-01/sql/S10.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-092/attempt-01/results/S10.rows.jsonl)；完整：True；SHA256：`8e0a09c905e099b226011a93e1b432e9d9128d7409a5f78e390fc5976485d446`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "quickbooks__balance_sheet", "kind": "base", "block": null, "base_tables": ["quickbooks__balance_sheet"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |


## S11

类别 `data`；来源 `query_db`；调用 `dc35bc69a60b4249866ec08d86d53901`；状态 `success`。

```sql
SELECT DISTINCT customer_id FROM quickbooks__profitability_analysis LIMIT 20
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-092/attempt-01/sql/S11.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-092/attempt-01/sql/S11.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-092/attempt-01/results/S11.rows.jsonl)；完整：True；SHA256：`de0e14140546fa7462638e50c97595b385055371c8042cf5f30564d14996eaaa`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "quickbooks__profitability_analysis", "kind": "base", "block": null, "base_tables": ["quickbooks__profitability_analysis"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |


## S12

类别 `data`；来源 `query_db`；调用 `c2cf3df564444b2b9f9f8f7fcd0f5409`；状态 `success`。

```sql
SELECT DISTINCT customer_id FROM quickbooks__customer_analytics LIMIT 20
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-092/attempt-01/sql/S12.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-092/attempt-01/sql/S12.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-092/attempt-01/results/S12.rows.jsonl)；完整：True；SHA256：`09d57b7d2026c7fb050b4c1be942cd458d37f0e736a298815e30bfa31ce986f1`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "quickbooks__customer_analytics", "kind": "base", "block": null, "base_tables": ["quickbooks__customer_analytics"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |


## S13

类别 `data`；来源 `query_db`；调用 `f3d570ff0c484d0984cfeab91b36477c`；状态 `success`。

```sql
SELECT MIN(transaction_date), MAX(transaction_date) FROM quickbooks__profitability_analysis
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-092/attempt-01/sql/S13.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-092/attempt-01/sql/S13.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-092/attempt-01/results/S13.rows.jsonl)；完整：True；SHA256：`496d0f79c219533c6657a48eff97851cb977b9458e08c9b6bc69e146e7e111b7`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "quickbooks__profitability_analysis", "kind": "base", "block": null, "base_tables": ["quickbooks__profitability_analysis"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | MIN(transaction_date) | [{"table": "quickbooks__profitability_analysis", "column": "transaction_date"}] | [] | False |
| B1 | MAX(transaction_date) | [{"table": "quickbooks__profitability_analysis", "column": "transaction_date"}] | [] | False |


## S14

类别 `data`；来源 `query_db`；调用 `0d6d3835a23b4bed9d63b92d11772f74`；状态 `success`。

```sql
SELECT DISTINCT rfm_segment FROM quickbooks__customer_analytics
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-092/attempt-01/sql/S14.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-092/attempt-01/sql/S14.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-092/attempt-01/results/S14.rows.jsonl)；完整：True；SHA256：`615f915cb24cd628e9143ba343b155902df162a88bbf1b38d11ec5f9d88f563a`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "quickbooks__customer_analytics", "kind": "base", "block": null, "base_tables": ["quickbooks__customer_analytics"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |


## S15

类别 `data`；来源 `query_db`；调用 `07a9f4fa9b9246feba6338d87ee76a1d`；状态 `success`。

```sql
SELECT DISTINCT payment_behavior FROM quickbooks__customer_analytics
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-092/attempt-01/sql/S15.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-092/attempt-01/sql/S15.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-092/attempt-01/results/S15.rows.jsonl)；完整：True；SHA256：`1d4163f1dcd4517c94629ddbe06f7184b780cdf3f8fbe5798f9107c9195c13be`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "quickbooks__customer_analytics", "kind": "base", "block": null, "base_tables": ["quickbooks__customer_analytics"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |


## S16

类别 `data`；来源 `query_db`；调用 `95b6e587e6264d7ba40cf90966e0ac3a`；状态 `success`。

```sql
SELECT DISTINCT lifecycle_stage FROM quickbooks__customer_analytics
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-092/attempt-01/sql/S16.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-092/attempt-01/sql/S16.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-092/attempt-01/results/S16.rows.jsonl)；完整：True；SHA256：`8b4dcf17295ab17a256f2b60eb070046ff3d4e03fb17bc6b244da92bab1be394`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "quickbooks__customer_analytics", "kind": "base", "block": null, "base_tables": ["quickbooks__customer_analytics"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |


## S17

类别 `data`；来源 `query_db`；调用 `e010c249818e41cd86284d0a9b4ad723`；状态 `success`。

```sql
SELECT COUNT(DISTINCT customer_id) as cnt FROM quickbooks__profitability_analysis
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-092/attempt-01/sql/S17.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-092/attempt-01/sql/S17.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-092/attempt-01/results/S17.rows.jsonl)；完整：True；SHA256：`409ab31294c9429f03e9f17a7e49ebfac259b29f8ad8ca8c4d51de2ef93bb943`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "quickbooks__profitability_analysis", "kind": "base", "block": null, "base_tables": ["quickbooks__profitability_analysis"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(DISTINCT customer_id) | [{"table": "quickbooks__profitability_analysis", "column": "customer_id"}] | [] | False |


## S18

类别 `data`；来源 `query_db`；调用 `cc719efc5ae44367ab6dd0817951db1d`；状态 `success`。

```sql
SELECT customer_margin_volatility, COUNT(*) as cnt
FROM quickbooks__profitability_analysis
WHERE customer_margin_volatility IS NOT NULL
GROUP BY customer_margin_volatility
ORDER BY customer_margin_volatility DESC
LIMIT 20
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-092/attempt-01/sql/S18.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-092/attempt-01/sql/S18.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-092/attempt-01/results/S18.rows.jsonl)；完整：True；SHA256：`8caabc44c5d32d3a9d2a256c140a6d004abe7847e8760f321f2c906739495f86`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "quickbooks__profitability_analysis", "kind": "base", "block": null, "base_tables": ["quickbooks__profitability_analysis"]}] | [] | ["customer_margin_volatility"] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |


## S19

类别 `data`；来源 `query_db`；调用 `0525f76aebc241c2b955cdb438a7f66a`；状态 `success`。

```sql
WITH cust_vol AS (
  SELECT customer_id, MAX(customer_margin_volatility) AS vol
  FROM quickbooks__profitability_analysis
  GROUP BY customer_id
)
SELECT 
  COUNT(*) AS n_customers,
  MIN(vol) AS min_vol,
  MAX(vol) AS max_vol,
  AVG(vol) AS mean_vol
FROM cust_vol
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-092/attempt-01/sql/S19.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-092/attempt-01/sql/S19.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-092/attempt-01/results/S19.rows.jsonl)；完整：True；SHA256：`47a506f4d316b1fc609b413bf6375761cc89a2293ff25bfdc09d3150d7e709c4`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "quickbooks__profitability_analysis", "kind": "base", "block": null, "base_tables": ["quickbooks__profitability_analysis"]}] | [] | ["customer_id"] |
| B2 | [{"alias": "cust_vol", "kind": "derived", "block": "B1", "base_tables": ["quickbooks__profitability_analysis"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | MAX(customer_margin_volatility) | [{"table": "quickbooks__profitability_analysis", "column": "customer_margin_volatility"}] | [] | False |
| B2 | COUNT(*) | [] | [] | True |
| B2 | MIN(vol) | [{"table": "quickbooks__profitability_analysis", "column": "customer_margin_volatility"}] | [] | False |
| B2 | MAX(vol) | [{"table": "quickbooks__profitability_analysis", "column": "customer_margin_volatility"}] | [] | False |
| B2 | AVG(vol) | [{"table": "quickbooks__profitability_analysis", "column": "customer_margin_volatility"}] | [] | False |


## S20

类别 `data`；来源 `query_db`；调用 `2e4b4b2b317d4a07a07629cd57964e84`；状态 `success`。

```sql
SELECT customer_id, COUNT(DISTINCT customer_margin_volatility) AS n_distinct_vol, COUNT(DISTINCT customer_margin_volatility) 
FROM quickbooks__profitability_analysis
GROUP BY customer_id
HAVING COUNT(DISTINCT customer_margin_volatility) > 1
LIMIT 5
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-092/attempt-01/sql/S20.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-092/attempt-01/sql/S20.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-092/attempt-01/results/S20.rows.jsonl)；完整：True；SHA256：`ab3798c8ebb03d54671ae0d8e37ecf4b60d2e503396d25a454e1e3e3dbdb50d3`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "quickbooks__profitability_analysis", "kind": "base", "block": null, "base_tables": ["quickbooks__profitability_analysis"]}] | [] | ["customer_id"] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(DISTINCT customer_margin_volatility) | [{"table": "quickbooks__profitability_analysis", "column": "customer_margin_volatility"}] | [] | False |
| B1 | COUNT(DISTINCT customer_margin_volatility) | [{"table": "quickbooks__profitability_analysis", "column": "customer_margin_volatility"}] | [] | False |
| B1 | COUNT(DISTINCT customer_margin_volatility) | [{"table": "quickbooks__profitability_analysis", "column": "customer_margin_volatility"}] | [] | False |


## S21

类别 `data`；来源 `query_db`；调用 `a645b1c164d046f3ad8a6507d9299b94`；状态 `success`。

```sql
SELECT invoice_id, customer_id, transaction_date, revenue_month_start, customer_margin_volatility, invoice_total, gross_profit
FROM quickbooks__profitability_analysis
WHERE customer_id = 'CUS00031796345'
ORDER BY transaction_date
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-092/attempt-01/sql/S21.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-092/attempt-01/sql/S21.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-092/attempt-01/results/S21.rows.jsonl)；完整：True；SHA256：`30328a2af7ba7f605c45e1d6f2fd5c9572a0ffd07696b714b430a32b28fa27aa`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "quickbooks__profitability_analysis", "kind": "base", "block": null, "base_tables": ["quickbooks__profitability_analysis"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |


## S22

类别 `data`；来源 `query_db`；调用 `010891721bbe49339c7b69ae6751fb9a`；状态 `success`。

```sql
WITH cust_vol AS (
  SELECT customer_id, AVG(customer_margin_volatility) AS vol
  FROM quickbooks__profitability_analysis
  GROUP BY customer_id
),
ordered AS (
  SELECT customer_id, vol,
    ROW_NUMBER() OVER (ORDER BY vol DESC) AS rn,
    COUNT(*) OVER () AS total
  FROM cust_vol
)
SELECT * FROM ordered WHERE rn IN (700, 701, 2100, 2101) OR rn = 2800
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-092/attempt-01/sql/S22.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-092/attempt-01/sql/S22.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-092/attempt-01/results/S22.rows.jsonl)；完整：True；SHA256：`c930526e5bd742c7d6133a29d57d3e5a8c8a964952620d3135f2e8104af708cb`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "quickbooks__profitability_analysis", "kind": "base", "block": null, "base_tables": ["quickbooks__profitability_analysis"]}] | [] | ["customer_id"] |
| B2 | [{"alias": "cust_vol", "kind": "derived", "block": "B1", "base_tables": ["quickbooks__profitability_analysis"]}] | [] | [] |
| B3 | [{"alias": "ordered", "kind": "derived", "block": "B2", "base_tables": ["quickbooks__profitability_analysis"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | AVG(customer_margin_volatility) | [{"table": "quickbooks__profitability_analysis", "column": "customer_margin_volatility"}] | [] | False |


## S23

类别 `data`；来源 `query_db`；调用 `632b5fe4bf494055ac31e47ee0a6ba87`；状态 `failed`。

```sql
WITH cust_vol AS (
  SELECT customer_id, AVG(customer_margin_volatility) AS vol
  FROM quickbooks__profitability_analysis
  GROUP BY customer_id
)
SELECT 
  PERCENTILE_DISC(0.75) WITHIN GROUP (ORDER BY vol) AS p75
FROM cust_vol
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-092/attempt-01/sql/S23.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-092/attempt-01/sql/S23.parameters.json)。

错误：`OperationalError('near "(": syntax error')`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "quickbooks__profitability_analysis", "kind": "base", "block": null, "base_tables": ["quickbooks__profitability_analysis"]}] | [] | ["customer_id"] |
| B2 | [{"alias": "cust_vol", "kind": "derived", "block": "B1", "base_tables": ["quickbooks__profitability_analysis"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | AVG(customer_margin_volatility) | [{"table": "quickbooks__profitability_analysis", "column": "customer_margin_volatility"}] | [] | False |
| B2 | PERCENTILE_DISC(0.75) | [] | [] | False |


## S24

类别 `data`；来源 `query_db`；调用 `5eeb35f7eb9948f58ebbe2a81208c327`；状态 `success`。

```sql
WITH cust_vol AS (
  SELECT customer_id, AVG(customer_margin_volatility) AS vol
  FROM quickbooks__profitability_analysis
  GROUP BY customer_id
),
ordered AS (
  SELECT customer_id, vol,
    ROW_NUMBER() OVER (ORDER BY vol DESC) AS rn
  FROM cust_vol
)
SELECT vol AS threshold FROM ordered WHERE rn = 700
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-092/attempt-01/sql/S24.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-092/attempt-01/sql/S24.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-092/attempt-01/results/S24.rows.jsonl)；完整：True；SHA256：`70ceee86b95235f1c4437f6a68405fa4bdc03b5f6e71a6fd6e1c747d2d71cd0d`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "quickbooks__profitability_analysis", "kind": "base", "block": null, "base_tables": ["quickbooks__profitability_analysis"]}] | [] | ["customer_id"] |
| B2 | [{"alias": "cust_vol", "kind": "derived", "block": "B1", "base_tables": ["quickbooks__profitability_analysis"]}] | [] | [] |
| B3 | [{"alias": "ordered", "kind": "derived", "block": "B2", "base_tables": ["quickbooks__profitability_analysis"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | AVG(customer_margin_volatility) | [{"table": "quickbooks__profitability_analysis", "column": "customer_margin_volatility"}] | [] | False |


## S25

类别 `data`；来源 `query_db`；调用 `a0e3bbe7ee644f78a353decbc7e3c1a0`；状态 `success`。

```sql
WITH cust_vol AS (
  SELECT customer_id, AVG(customer_margin_volatility) AS vol
  FROM quickbooks__profitability_analysis
  GROUP BY customer_id
),
ordered AS (
  SELECT customer_id, vol,
    ROW_NUMBER() OVER (ORDER BY vol DESC) AS rn,
    COUNT(*) OVER () AS total
  FROM cust_vol
),
high_vol_cust AS (
  SELECT customer_id, vol
  FROM ordered
  WHERE rn <= total * 0.25
)
SELECT COUNT(*) AS n_high_vol FROM high_vol_cust
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-092/attempt-01/sql/S25.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-092/attempt-01/sql/S25.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-092/attempt-01/results/S25.rows.jsonl)；完整：True；SHA256：`a482ada409c7c0efe39d3f42fd4364938468c884fb29d4e249f74acf895bba32`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "quickbooks__profitability_analysis", "kind": "base", "block": null, "base_tables": ["quickbooks__profitability_analysis"]}] | [] | ["customer_id"] |
| B2 | [{"alias": "cust_vol", "kind": "derived", "block": "B1", "base_tables": ["quickbooks__profitability_analysis"]}] | [] | [] |
| B3 | [{"alias": "ordered", "kind": "derived", "block": "B2", "base_tables": ["quickbooks__profitability_analysis"]}] | [] | [] |
| B4 | [{"alias": "high_vol_cust", "kind": "derived", "block": "B3", "base_tables": ["quickbooks__profitability_analysis"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | AVG(customer_margin_volatility) | [{"table": "quickbooks__profitability_analysis", "column": "customer_margin_volatility"}] | [] | False |
| B4 | COUNT(*) | [] | [] | True |


## S26

类别 `data`；来源 `query_db`；调用 `bd6c136a42884f90bc8ae9bd57a3ce18`；状态 `success`。

```sql
SELECT MIN(transaction_date), MAX(transaction_date) FROM quickbooks__profitability_analysis
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-092/attempt-01/sql/S26.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-092/attempt-01/sql/S26.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-092/attempt-01/results/S26.rows.jsonl)；完整：True；SHA256：`496d0f79c219533c6657a48eff97851cb977b9458e08c9b6bc69e146e7e111b7`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "quickbooks__profitability_analysis", "kind": "base", "block": null, "base_tables": ["quickbooks__profitability_analysis"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | MIN(transaction_date) | [{"table": "quickbooks__profitability_analysis", "column": "transaction_date"}] | [] | False |
| B1 | MAX(transaction_date) | [{"table": "quickbooks__profitability_analysis", "column": "transaction_date"}] | [] | False |


## S27

类别 `data`；来源 `query_db`；调用 `75d00932af2f473793c20f2fb732090f`；状态 `success`。

```sql
-- Define the past 12 months date range
WITH date_range AS (
  SELECT DATE(MAX(transaction_date), '-12 months') AS cutoff_date
  FROM quickbooks__profitability_analysis
),
-- High volatility customers (top 25%)
cust_vol AS (
  SELECT customer_id, AVG(customer_margin_volatility) AS vol
  FROM quickbooks__profitability_analysis
  GROUP BY customer_id
),
ordered AS (
  SELECT customer_id, vol,
    ROW_NUMBER() OVER (ORDER BY vol DESC) AS rn,
    COUNT(*) OVER () AS total
  FROM cust_vol
),
high_vol_cust AS (
  SELECT customer_id, vol
  FROM ordered
  WHERE rn <= total * 0.25
)
-- Get gross_profit data for past 12 months
SELECT h.customer_id, h.vol, p.gross_profit, p.transaction_date
FROM high_vol_cust h
JOIN quickbooks__profitability_analysis p ON h.customer_id = p.customer_id
WHERE p.transaction_date >= (SELECT cutoff_date FROM date_range)
ORDER BY h.vol DESC, h.customer_id, p.transaction_date
LIMIT 20
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-092/attempt-01/sql/S27.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-092/attempt-01/sql/S27.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-092/attempt-01/results/S27.rows.jsonl)；完整：True；SHA256：`5f5cddc66fbb3d01610415469e8e837b958e1788c9537f11c4a2d69a282cc9d1`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "quickbooks__profitability_analysis", "kind": "base", "block": null, "base_tables": ["quickbooks__profitability_analysis"]}] | [] | [] |
| B2 | [{"alias": "quickbooks__profitability_analysis", "kind": "base", "block": null, "base_tables": ["quickbooks__profitability_analysis"]}] | [] | ["customer_id"] |
| B3 | [{"alias": "cust_vol", "kind": "derived", "block": "B2", "base_tables": ["quickbooks__profitability_analysis"]}] | [] | [] |
| B4 | [{"alias": "ordered", "kind": "derived", "block": "B3", "base_tables": ["quickbooks__profitability_analysis"]}] | [] | [] |
| B5 | [{"alias": "date_range", "kind": "derived", "block": "B1", "base_tables": ["quickbooks__profitability_analysis"]}] | [] | [] |
| B6 | [{"alias": "h", "kind": "derived", "block": "B4", "base_tables": ["quickbooks__profitability_analysis"]}, {"alias": "p", "kind": "base", "block": null, "base_tables": ["quickbooks__profitability_analysis"]}] | [{"type": "INNER", "right": "quickbooks__profitability_analysis AS p", "on": "h.customer_id = p.customer_id", "using": []}] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | MAX(transaction_date) | [{"table": "quickbooks__profitability_analysis", "column": "transaction_date"}] | [] | False |
| B2 | AVG(customer_margin_volatility) | [{"table": "quickbooks__profitability_analysis", "column": "customer_margin_volatility"}] | [] | False |


未解析列血缘：[{"block": "B6", "column": "cutoff_date", "reason": "ambiguous_or_missing_source"}]

## S28

类别 `data`；来源 `query_db`；调用 `997f89df12df4c1baec610a02f9445e9`；状态 `failed`。

```sql
-- Compute coefficient of variation of gross_profit for high-vol customers over past 12 months
WITH date_range AS (
  SELECT DATE(MAX(transaction_date), '-12 months') AS cutoff_date
  FROM quickbooks__profitability_analysis
),
cust_vol AS (
  SELECT customer_id, AVG(customer_margin_volatility) AS vol
  FROM quickbooks__profitability_analysis
  GROUP BY customer_id
),
ordered AS (
  SELECT customer_id, vol,
    ROW_NUMBER() OVER (ORDER BY vol DESC) AS rn,
    COUNT(*) OVER () AS total
  FROM cust_vol
),
high_vol_cust AS (
  SELECT customer_id, vol
  FROM ordered
  WHERE rn <= total * 0.25
)
SELECT 
  h.customer_id,
  h.vol,
  AVG(p.gross_profit) AS mean_gross_profit,
  STDEV(p.gross_profit) AS std_gross_profit,
  CASE WHEN AVG(p.gross_profit) = 0 THEN NULL 
       ELSE STDEV(p.gross_profit) / AVG(p.gross_profit) END AS cv_gross_profit,
  COUNT(p.gross_profit) AS n_obs
FROM high_vol_cust h
JOIN quickbooks__profitability_analysis p ON h.customer_id = p.customer_id
  AND p.transaction_date >= (SELECT cutoff_date FROM date_range)
GROUP BY h.customer_id, h.vol
ORDER BY h.vol DESC
LIMIT 20
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-092/attempt-01/sql/S28.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-092/attempt-01/sql/S28.parameters.json)。

错误：`OperationalError('no such function: STDEV')`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "quickbooks__profitability_analysis", "kind": "base", "block": null, "base_tables": ["quickbooks__profitability_analysis"]}] | [] | [] |
| B2 | [{"alias": "quickbooks__profitability_analysis", "kind": "base", "block": null, "base_tables": ["quickbooks__profitability_analysis"]}] | [] | ["customer_id"] |
| B3 | [{"alias": "cust_vol", "kind": "derived", "block": "B2", "base_tables": ["quickbooks__profitability_analysis"]}] | [] | [] |
| B4 | [{"alias": "ordered", "kind": "derived", "block": "B3", "base_tables": ["quickbooks__profitability_analysis"]}] | [] | [] |
| B5 | [{"alias": "date_range", "kind": "derived", "block": "B1", "base_tables": ["quickbooks__profitability_analysis"]}] | [] | [] |
| B6 | [{"alias": "h", "kind": "derived", "block": "B4", "base_tables": ["quickbooks__profitability_analysis"]}, {"alias": "p", "kind": "base", "block": null, "base_tables": ["quickbooks__profitability_analysis"]}] | [{"type": "INNER", "right": "quickbooks__profitability_analysis AS p", "on": "h.customer_id = p.customer_id AND p.transaction_date >= (SELECT cutoff_date FROM date_range)", "using": []}] | ["h.customer_id", "h.vol"] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | MAX(transaction_date) | [{"table": "quickbooks__profitability_analysis", "column": "transaction_date"}] | [] | False |
| B2 | AVG(customer_margin_volatility) | [{"table": "quickbooks__profitability_analysis", "column": "customer_margin_volatility"}] | [] | False |
| B6 | AVG(p.gross_profit) | [{"table": "quickbooks__profitability_analysis", "column": "gross_profit"}] | [] | False |
| B6 | STDDEV(p.gross_profit) | [{"table": "quickbooks__profitability_analysis", "column": "gross_profit"}] | [] | False |
| B6 | COUNT(p.gross_profit) | [{"table": "quickbooks__profitability_analysis", "column": "gross_profit"}] | [] | False |
| B6 | STDDEV(p.gross_profit) | [{"table": "quickbooks__profitability_analysis", "column": "gross_profit"}] | [] | False |
| B6 | AVG(p.gross_profit) | [{"table": "quickbooks__profitability_analysis", "column": "gross_profit"}] | [] | False |
| B6 | AVG(p.gross_profit) | [{"table": "quickbooks__profitability_analysis", "column": "gross_profit"}] | [] | False |


未解析列血缘：[{"block": "B6", "column": "cutoff_date", "reason": "ambiguous_or_missing_source"}]

## S29

类别 `data`；来源 `query_db`；调用 `f615ac5d1c484e78b93ee30fc75a4250`；状态 `success`。

```sql
-- Compute coefficient of variation of gross_profit for high-vol customers over past 12 months
WITH date_range AS (
  SELECT DATE(MAX(transaction_date), '-12 months') AS cutoff_date
  FROM quickbooks__profitability_analysis
),
cust_vol AS (
  SELECT customer_id, AVG(customer_margin_volatility) AS vol
  FROM quickbooks__profitability_analysis
  GROUP BY customer_id
),
ordered AS (
  SELECT customer_id, vol,
    ROW_NUMBER() OVER (ORDER BY vol DESC) AS rn,
    COUNT(*) OVER () AS total
  FROM cust_vol
),
high_vol_cust AS (
  SELECT customer_id, vol
  FROM ordered
  WHERE rn <= total * 0.25
),
stats AS (
  SELECT 
    h.customer_id,
    h.vol,
    AVG(p.gross_profit) AS mean_gp,
    AVG(p.gross_profit * p.gross_profit) - AVG(p.gross_profit) * AVG(p.gross_profit) AS var_gp,
    COUNT(p.gross_profit) AS n_obs
  FROM high_vol_cust h
  JOIN quickbooks__profitability_analysis p ON h.customer_id = p.customer_id
    AND p.transaction_date >= (SELECT cutoff_date FROM date_range)
  GROUP BY h.customer_id, h.vol
)
SELECT 
  customer_id, vol, mean_gp,
  CASE WHEN var_gp < 0 THEN 0 ELSE SQRT(var_gp) END AS std_gp,
  CASE WHEN mean_gp = 0 THEN NULL 
       ELSE CASE WHEN var_gp < 0 THEN 0 ELSE SQRT(var_gp) END / mean_gp END AS cv_gp,
  n_obs
FROM stats
ORDER BY vol DESC
LIMIT 20
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-092/attempt-01/sql/S29.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-092/attempt-01/sql/S29.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-092/attempt-01/results/S29.rows.jsonl)；完整：True；SHA256：`161d41152cb6ef44a47d626c08855312565b47ef0316fb5e92ccf3610e7598b8`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "quickbooks__profitability_analysis", "kind": "base", "block": null, "base_tables": ["quickbooks__profitability_analysis"]}] | [] | [] |
| B2 | [{"alias": "quickbooks__profitability_analysis", "kind": "base", "block": null, "base_tables": ["quickbooks__profitability_analysis"]}] | [] | ["customer_id"] |
| B3 | [{"alias": "cust_vol", "kind": "derived", "block": "B2", "base_tables": ["quickbooks__profitability_analysis"]}] | [] | [] |
| B4 | [{"alias": "ordered", "kind": "derived", "block": "B3", "base_tables": ["quickbooks__profitability_analysis"]}] | [] | [] |
| B5 | [{"alias": "date_range", "kind": "derived", "block": "B1", "base_tables": ["quickbooks__profitability_analysis"]}] | [] | [] |
| B6 | [{"alias": "h", "kind": "derived", "block": "B4", "base_tables": ["quickbooks__profitability_analysis"]}, {"alias": "p", "kind": "base", "block": null, "base_tables": ["quickbooks__profitability_analysis"]}] | [{"type": "INNER", "right": "quickbooks__profitability_analysis AS p", "on": "h.customer_id = p.customer_id AND p.transaction_date >= (SELECT cutoff_date FROM date_range)", "using": []}] | ["h.customer_id", "h.vol"] |
| B7 | [{"alias": "stats", "kind": "derived", "block": "B6", "base_tables": ["quickbooks__profitability_analysis"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | MAX(transaction_date) | [{"table": "quickbooks__profitability_analysis", "column": "transaction_date"}] | [] | False |
| B2 | AVG(customer_margin_volatility) | [{"table": "quickbooks__profitability_analysis", "column": "customer_margin_volatility"}] | [] | False |
| B6 | AVG(p.gross_profit) | [{"table": "quickbooks__profitability_analysis", "column": "gross_profit"}] | [] | False |
| B6 | COUNT(p.gross_profit) | [{"table": "quickbooks__profitability_analysis", "column": "gross_profit"}] | [] | False |
| B6 | AVG(p.gross_profit * p.gross_profit) | [{"table": "quickbooks__profitability_analysis", "column": "gross_profit"}, {"table": "quickbooks__profitability_analysis", "column": "gross_profit"}] | [] | False |
| B6 | AVG(p.gross_profit) | [{"table": "quickbooks__profitability_analysis", "column": "gross_profit"}] | [] | False |
| B6 | AVG(p.gross_profit) | [{"table": "quickbooks__profitability_analysis", "column": "gross_profit"}] | [] | False |


未解析列血缘：[{"block": "B7", "column": "cutoff_date", "reason": "ambiguous_or_missing_source"}]

## S30

类别 `data`；来源 `query_db`；调用 `e3b993fec8f0421baca77fb85d4e7674`；状态 `success`。

```sql
-- Monthly gross profit per high-vol customer over past 12 months, then CV
WITH date_range AS (
  SELECT DATE(MAX(transaction_date), '-12 months') AS cutoff_date
  FROM quickbooks__profitability_analysis
),
cust_vol AS (
  SELECT customer_id, AVG(customer_margin_volatility) AS vol
  FROM quickbooks__profitability_analysis
  GROUP BY customer_id
),
ordered AS (
  SELECT customer_id, vol,
    ROW_NUMBER() OVER (ORDER BY vol DESC) AS rn,
    COUNT(*) OVER () AS total
  FROM cust_vol
),
high_vol_cust AS (
  SELECT customer_id, vol
  FROM ordered
  WHERE rn <= total * 0.25
),
monthly AS (
  SELECT 
    h.customer_id,
    STRFTIME('%Y-%m', p.transaction_date) AS month,
    SUM(p.gross_profit) AS monthly_gp
  FROM high_vol_cust h
  JOIN quickbooks__profitability_analysis p ON h.customer_id = p.customer_id
    AND p.transaction_date >= (SELECT cutoff_date FROM date_range)
  GROUP BY h.customer_id, STRFTIME('%Y-%m', p.transaction_date)
),
stats AS (
  SELECT 
    customer_id,
    AVG(monthly_gp) AS mean_mgp,
    AVG(monthly_gp * monthly_gp) - AVG(monthly_gp) * AVG(monthly_gp) AS var_mgp,
    COUNT(*) AS n_months
  FROM monthly
  GROUP BY customer_id
)
SELECT 
  customer_id,
  mean_mgp,
  CASE WHEN var_mgp < 0 THEN 0 ELSE SQRT(var_mgp) END AS std_mgp,
  CASE WHEN mean_mgp = 0 THEN NULL 
       ELSE CASE WHEN var_mgp < 0 THEN 0 ELSE SQRT(var_mgp) END / ABS(mean_mgp) END AS cv_mgp,
  n_months
FROM stats
ORDER BY cv_mgp DESC NULLS LAST
LIMIT 15
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-092/attempt-01/sql/S30.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-092/attempt-01/sql/S30.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-092/attempt-01/results/S30.rows.jsonl)；完整：True；SHA256：`89e780e4a8e395563250ae14bd47bbab53c990e8bcf8446d189c32ef0c668b79`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "quickbooks__profitability_analysis", "kind": "base", "block": null, "base_tables": ["quickbooks__profitability_analysis"]}] | [] | [] |
| B2 | [{"alias": "quickbooks__profitability_analysis", "kind": "base", "block": null, "base_tables": ["quickbooks__profitability_analysis"]}] | [] | ["customer_id"] |
| B3 | [{"alias": "cust_vol", "kind": "derived", "block": "B2", "base_tables": ["quickbooks__profitability_analysis"]}] | [] | [] |
| B4 | [{"alias": "ordered", "kind": "derived", "block": "B3", "base_tables": ["quickbooks__profitability_analysis"]}] | [] | [] |
| B5 | [{"alias": "date_range", "kind": "derived", "block": "B1", "base_tables": ["quickbooks__profitability_analysis"]}] | [] | [] |
| B6 | [{"alias": "h", "kind": "derived", "block": "B4", "base_tables": ["quickbooks__profitability_analysis"]}, {"alias": "p", "kind": "base", "block": null, "base_tables": ["quickbooks__profitability_analysis"]}] | [{"type": "INNER", "right": "quickbooks__profitability_analysis AS p", "on": "h.customer_id = p.customer_id AND p.transaction_date >= (SELECT cutoff_date FROM date_range)", "using": []}] | ["h.customer_id", "STRFTIME('%Y-%m', p.transaction_date)"] |
| B7 | [{"alias": "monthly", "kind": "derived", "block": "B6", "base_tables": ["quickbooks__profitability_analysis"]}] | [] | ["customer_id"] |
| B8 | [{"alias": "stats", "kind": "derived", "block": "B7", "base_tables": ["quickbooks__profitability_analysis"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | MAX(transaction_date) | [{"table": "quickbooks__profitability_analysis", "column": "transaction_date"}] | [] | False |
| B2 | AVG(customer_margin_volatility) | [{"table": "quickbooks__profitability_analysis", "column": "customer_margin_volatility"}] | [] | False |
| B6 | SUM(p.gross_profit) | [{"table": "quickbooks__profitability_analysis", "column": "gross_profit"}] | [] | False |
| B7 | AVG(monthly_gp) | [{"table": "quickbooks__profitability_analysis", "column": "gross_profit"}] | [] | False |
| B7 | COUNT(*) | [] | [] | True |
| B7 | AVG(monthly_gp * monthly_gp) | [{"table": "quickbooks__profitability_analysis", "column": "gross_profit"}, {"table": "quickbooks__profitability_analysis", "column": "gross_profit"}] | [] | False |
| B7 | AVG(monthly_gp) | [{"table": "quickbooks__profitability_analysis", "column": "gross_profit"}] | [] | False |
| B7 | AVG(monthly_gp) | [{"table": "quickbooks__profitability_analysis", "column": "gross_profit"}] | [] | False |


未解析列血缘：[{"block": "B8", "column": "cutoff_date", "reason": "ambiguous_or_missing_source"}]

## S31

类别 `data`；来源 `query_db`；调用 `f64a07757c884069886f4db659153d0f`；状态 `success`。

```sql
-- Overall CV of monthly gross profit for high-volatility customers
WITH date_range AS (
  SELECT DATE(MAX(transaction_date), '-12 months') AS cutoff_date
  FROM quickbooks__profitability_analysis
),
cust_vol AS (
  SELECT customer_id, AVG(customer_margin_volatility) AS vol
  FROM quickbooks__profitability_analysis
  GROUP BY customer_id
),
ordered AS (
  SELECT customer_id, vol,
    ROW_NUMBER() OVER (ORDER BY vol DESC) AS rn,
    COUNT(*) OVER () AS total
  FROM cust_vol
),
high_vol_cust AS (
  SELECT customer_id, vol
  FROM ordered
  WHERE rn <= total * 0.25
),
monthly AS (
  SELECT 
    h.customer_id,
    STRFTIME('%Y-%m', p.transaction_date) AS month,
    SUM(p.gross_profit) AS monthly_gp
  FROM high_vol_cust h
  JOIN quickbooks__profitability_analysis p ON h.customer_id = p.customer_id
    AND p.transaction_date >= (SELECT cutoff_date FROM date_range)
  GROUP BY h.customer_id, STRFTIME('%Y-%m', p.transaction_date)
)
SELECT 
  AVG(monthly_gp) AS overall_mean_gp,
  SQRT(AVG(monthly_gp * monthly_gp) - AVG(monthly_gp) * AVG(monthly_gp)) AS overall_std_gp,
  SQRT(AVG(monthly_gp * monthly_gp) - AVG(monthly_gp) * AVG(monthly_gp)) / ABS(AVG(monthly_gp)) AS overall_cv_gp,
  COUNT(*) AS total_month_obs,
  COUNT(DISTINCT customer_id) AS n_customers_with_data
FROM monthly
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-092/attempt-01/sql/S31.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-092/attempt-01/sql/S31.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-092/attempt-01/results/S31.rows.jsonl)；完整：True；SHA256：`42b281b74fe87f1d33a965cc434988c0f4e55036aca1e0fdf17c46f736d161b7`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "quickbooks__profitability_analysis", "kind": "base", "block": null, "base_tables": ["quickbooks__profitability_analysis"]}] | [] | [] |
| B2 | [{"alias": "quickbooks__profitability_analysis", "kind": "base", "block": null, "base_tables": ["quickbooks__profitability_analysis"]}] | [] | ["customer_id"] |
| B3 | [{"alias": "cust_vol", "kind": "derived", "block": "B2", "base_tables": ["quickbooks__profitability_analysis"]}] | [] | [] |
| B4 | [{"alias": "ordered", "kind": "derived", "block": "B3", "base_tables": ["quickbooks__profitability_analysis"]}] | [] | [] |
| B5 | [{"alias": "date_range", "kind": "derived", "block": "B1", "base_tables": ["quickbooks__profitability_analysis"]}] | [] | [] |
| B6 | [{"alias": "h", "kind": "derived", "block": "B4", "base_tables": ["quickbooks__profitability_analysis"]}, {"alias": "p", "kind": "base", "block": null, "base_tables": ["quickbooks__profitability_analysis"]}] | [{"type": "INNER", "right": "quickbooks__profitability_analysis AS p", "on": "h.customer_id = p.customer_id AND p.transaction_date >= (SELECT cutoff_date FROM date_range)", "using": []}] | ["h.customer_id", "STRFTIME('%Y-%m', p.transaction_date)"] |
| B7 | [{"alias": "monthly", "kind": "derived", "block": "B6", "base_tables": ["quickbooks__profitability_analysis"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | MAX(transaction_date) | [{"table": "quickbooks__profitability_analysis", "column": "transaction_date"}] | [] | False |
| B2 | AVG(customer_margin_volatility) | [{"table": "quickbooks__profitability_analysis", "column": "customer_margin_volatility"}] | [] | False |
| B6 | SUM(p.gross_profit) | [{"table": "quickbooks__profitability_analysis", "column": "gross_profit"}] | [] | False |
| B7 | AVG(monthly_gp) | [{"table": "quickbooks__profitability_analysis", "column": "gross_profit"}] | [] | False |
| B7 | COUNT(*) | [] | [] | True |
| B7 | COUNT(DISTINCT customer_id) | [{"table": "quickbooks__profitability_analysis", "column": "customer_id"}] | [] | False |
| B7 | AVG(monthly_gp * monthly_gp) | [{"table": "quickbooks__profitability_analysis", "column": "gross_profit"}, {"table": "quickbooks__profitability_analysis", "column": "gross_profit"}] | [] | False |
| B7 | AVG(monthly_gp) | [{"table": "quickbooks__profitability_analysis", "column": "gross_profit"}] | [] | False |
| B7 | AVG(monthly_gp) | [{"table": "quickbooks__profitability_analysis", "column": "gross_profit"}] | [] | False |
| B7 | AVG(monthly_gp) | [{"table": "quickbooks__profitability_analysis", "column": "gross_profit"}] | [] | False |
| B7 | AVG(monthly_gp * monthly_gp) | [{"table": "quickbooks__profitability_analysis", "column": "gross_profit"}, {"table": "quickbooks__profitability_analysis", "column": "gross_profit"}] | [] | False |
| B7 | AVG(monthly_gp) | [{"table": "quickbooks__profitability_analysis", "column": "gross_profit"}] | [] | False |
| B7 | AVG(monthly_gp) | [{"table": "quickbooks__profitability_analysis", "column": "gross_profit"}] | [] | False |


未解析列血缘：[{"block": "B7", "column": "cutoff_date", "reason": "ambiguous_or_missing_source"}]

## S32

类别 `data`；来源 `query_db`；调用 `31c2306673454d5bbc5f1729e41a3300`；状态 `success`。

```sql
SELECT DISTINCT revenue_year, revenue_quarter, COUNT(*) as cnt
FROM quickbooks__profitability_analysis
GROUP BY revenue_year, revenue_quarter
ORDER BY revenue_year, revenue_quarter
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-092/attempt-01/sql/S32.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-092/attempt-01/sql/S32.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-092/attempt-01/results/S32.rows.jsonl)；完整：True；SHA256：`f6a10f3f5c6fffdfe45397533149a4b198e036545476d70beb7644bda5d488fe`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "quickbooks__profitability_analysis", "kind": "base", "block": null, "base_tables": ["quickbooks__profitability_analysis"]}] | [] | ["revenue_year", "revenue_quarter"] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |


## S33

类别 `data`；来源 `query_db`；调用 `17aad498fd314c04949398d1f8c6affb`；状态 `success`。

```sql
-- Compare CV for bottom 25% (low volatility) customers
WITH cust_vol AS (
  SELECT customer_id, AVG(customer_margin_volatility) AS vol
  FROM quickbooks__profitability_analysis
  GROUP BY customer_id
),
ordered AS (
  SELECT customer_id, vol,
    ROW_NUMBER() OVER (ORDER BY vol ASC) AS rn,
    COUNT(*) OVER () AS total
  FROM cust_vol
),
low_vol_cust AS (
  SELECT customer_id, vol
  FROM ordered
  WHERE rn <= total * 0.25
)
SELECT COUNT(*) AS n_low_vol FROM low_vol_cust
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-092/attempt-01/sql/S33.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-092/attempt-01/sql/S33.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-092/attempt-01/results/S33.rows.jsonl)；完整：True；SHA256：`a482ada409c7c0efe39d3f42fd4364938468c884fb29d4e249f74acf895bba32`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "quickbooks__profitability_analysis", "kind": "base", "block": null, "base_tables": ["quickbooks__profitability_analysis"]}] | [] | ["customer_id"] |
| B2 | [{"alias": "cust_vol", "kind": "derived", "block": "B1", "base_tables": ["quickbooks__profitability_analysis"]}] | [] | [] |
| B3 | [{"alias": "ordered", "kind": "derived", "block": "B2", "base_tables": ["quickbooks__profitability_analysis"]}] | [] | [] |
| B4 | [{"alias": "low_vol_cust", "kind": "derived", "block": "B3", "base_tables": ["quickbooks__profitability_analysis"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | AVG(customer_margin_volatility) | [{"table": "quickbooks__profitability_analysis", "column": "customer_margin_volatility"}] | [] | False |
| B4 | COUNT(*) | [] | [] | True |


## S34

类别 `data`；来源 `query_db`；调用 `0f2608de81be404c9e907ba8fc412576`；状态 `success`。

```sql
-- QoQ invoice_total growth rate for high-vol customers (based on transaction_date quarters)
WITH date_range AS (
  SELECT DATE(MAX(transaction_date), '-12 months') AS cutoff_date
  FROM quickbooks__profitability_analysis
),
cust_vol AS (
  SELECT customer_id, AVG(customer_margin_volatility) AS vol
  FROM quickbooks__profitability_analysis
  GROUP BY customer_id
),
ordered AS (
  SELECT customer_id, vol,
    ROW_NUMBER() OVER (ORDER BY vol DESC) AS rn,
    COUNT(*) OVER () AS total
  FROM cust_vol
),
high_vol_cust AS (
  SELECT customer_id, vol
  FROM ordered
  WHERE rn <= total * 0.25
),
quarterly AS (
  SELECT 
    h.customer_id,
    STRFTIME('%Y', p.transaction_date) AS yr,
    CAST((CAST(STRFTIME('%m', p.transaction_date) AS INTEGER) + 2) / 3 AS INTEGER) AS qtr,
    SUM(p.invoice_total) AS qtr_invoice_total
  FROM high_vol_cust h
  JOIN quickbooks__profitability_analysis p ON h.customer_id = p.customer_id
    AND p.transaction_date >= (SELECT cutoff_date FROM date_range)
  GROUP BY h.customer_id, STRFTIME('%Y', p.transaction_date), CAST((CAST(STRFTIME('%m', p.transaction_date) AS INTEGER) + 2) / 3 AS INTEGER)
),
qoqs AS (
  SELECT 
    customer_id, yr, qtr, qtr_invoice_total,
    LAG(qtr_invoice_total) OVER (PARTITION BY customer_id ORDER BY yr, qtr) AS prev_qtr_total
  FROM quarterly
)
SELECT 
  customer_id, yr, qtr, qtr_invoice_total, prev_qtr_total,
  CASE WHEN prev_qtr_total IS NOT NULL AND prev_qtr_total <> 0 
       THEN (qtr_invoice_total - prev_qtr_total) / prev_qtr_total ELSE NULL END AS qoq_growth
FROM qoqs
WHERE prev_qtr_total IS NOT NULL
ORDER BY customer_id, yr, qtr
LIMIT 30
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-092/attempt-01/sql/S34.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-092/attempt-01/sql/S34.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-092/attempt-01/results/S34.rows.jsonl)；完整：True；SHA256：`1fbc84a75c22ab060417fbdd5b0da62ae96646086b90e71326fd7bb3af46aa13`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "quickbooks__profitability_analysis", "kind": "base", "block": null, "base_tables": ["quickbooks__profitability_analysis"]}] | [] | [] |
| B2 | [{"alias": "quickbooks__profitability_analysis", "kind": "base", "block": null, "base_tables": ["quickbooks__profitability_analysis"]}] | [] | ["customer_id"] |
| B3 | [{"alias": "cust_vol", "kind": "derived", "block": "B2", "base_tables": ["quickbooks__profitability_analysis"]}] | [] | [] |
| B4 | [{"alias": "ordered", "kind": "derived", "block": "B3", "base_tables": ["quickbooks__profitability_analysis"]}] | [] | [] |
| B5 | [{"alias": "date_range", "kind": "derived", "block": "B1", "base_tables": ["quickbooks__profitability_analysis"]}] | [] | [] |
| B6 | [{"alias": "h", "kind": "derived", "block": "B4", "base_tables": ["quickbooks__profitability_analysis"]}, {"alias": "p", "kind": "base", "block": null, "base_tables": ["quickbooks__profitability_analysis"]}] | [{"type": "INNER", "right": "quickbooks__profitability_analysis AS p", "on": "h.customer_id = p.customer_id AND p.transaction_date >= (SELECT cutoff_date FROM date_range)", "using": []}] | ["h.customer_id", "STRFTIME('%Y', p.transaction_date)", "CAST((CAST(STRFTIME('%m', p.transaction_date) AS INTEGER) + 2) / 3 AS INTEGER)"] |
| B7 | [{"alias": "quarterly", "kind": "derived", "block": "B6", "base_tables": ["quickbooks__profitability_analysis"]}] | [] | [] |
| B8 | [{"alias": "qoqs", "kind": "derived", "block": "B7", "base_tables": ["quickbooks__profitability_analysis"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | MAX(transaction_date) | [{"table": "quickbooks__profitability_analysis", "column": "transaction_date"}] | [] | False |
| B2 | AVG(customer_margin_volatility) | [{"table": "quickbooks__profitability_analysis", "column": "customer_margin_volatility"}] | [] | False |
| B6 | SUM(p.invoice_total) | [{"table": "quickbooks__profitability_analysis", "column": "invoice_total"}] | [] | False |


未解析列血缘：[{"block": "B8", "column": "cutoff_date", "reason": "ambiguous_or_missing_source"}]

## S35

类别 `data`；来源 `query_db`；调用 `38160a8029474b388f904bf671e6b1f6`；状态 `success`。

```sql
-- Variance of QoQ invoice_total growth rate for high-vol customers
WITH date_range AS (
  SELECT DATE(MAX(transaction_date), '-12 months') AS cutoff_date
  FROM quickbooks__profitability_analysis
),
cust_vol AS (
  SELECT customer_id, AVG(customer_margin_volatility) AS vol
  FROM quickbooks__profitability_analysis
  GROUP BY customer_id
),
ordered AS (
  SELECT customer_id, vol,
    ROW_NUMBER() OVER (ORDER BY vol DESC) AS rn,
    COUNT(*) OVER () AS total
  FROM cust_vol
),
high_vol_cust AS (
  SELECT customer_id, vol
  FROM ordered
  WHERE rn <= total * 0.25
),
quarterly AS (
  SELECT 
    h.customer_id,
    STRFTIME('%Y', p.transaction_date) AS yr,
    CAST((CAST(STRFTIME('%m', p.transaction_date) AS INTEGER) + 2) / 3 AS INTEGER) AS qtr,
    SUM(p.invoice_total) AS qtr_invoice_total
  FROM high_vol_cust h
  JOIN quickbooks__profitability_analysis p ON h.customer_id = p.customer_id
    AND p.transaction_date >= (SELECT cutoff_date FROM date_range)
  GROUP BY h.customer_id, STRFTIME('%Y', p.transaction_date), CAST((CAST(STRFTIME('%m', p.transaction_date) AS INTEGER) + 2) / 3 AS INTEGER)
),
qoqs AS (
  SELECT 
    customer_id, yr, qtr, qtr_invoice_total,
    LAG(qtr_invoice_total) OVER (PARTITION BY customer_id ORDER BY yr, qtr) AS prev_qtr_total
  FROM quarterly
)
SELECT 
  AVG(qoq_growth) AS mean_qoq_growth,
  AVG(qoq_growth * qoq_growth) - AVG(qoq_growth) * AVG(qoq_growth) AS var_qoq_growth,
  SQRT(AVG(qoq_growth * qoq_growth) - AVG(qoq_growth) * AVG(qoq_growth)) AS std_qoq_growth,
  COUNT(*) AS n_obs
FROM (
  SELECT 
    customer_id, yr, qtr, qtr_invoice_total, prev_qtr_total,
    CASE WHEN prev_qtr_total IS NOT NULL AND prev_qtr_total <> 0 
         THEN (qtr_invoice_total - prev_qtr_total) / prev_qtr_total ELSE NULL END AS qoq_growth
  FROM qoqs
  WHERE prev_qtr_total IS NOT NULL
) WHERE qoq_growth IS NOT NULL
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-092/attempt-01/sql/S35.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-092/attempt-01/sql/S35.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-092/attempt-01/results/S35.rows.jsonl)；完整：True；SHA256：`5d1d56f060f510c0b3cb1ecb9b00d95c761c7cf1ab227003a45f70bba65f1a8d`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "quickbooks__profitability_analysis", "kind": "base", "block": null, "base_tables": ["quickbooks__profitability_analysis"]}] | [] | [] |
| B2 | [{"alias": "quickbooks__profitability_analysis", "kind": "base", "block": null, "base_tables": ["quickbooks__profitability_analysis"]}] | [] | ["customer_id"] |
| B3 | [{"alias": "cust_vol", "kind": "derived", "block": "B2", "base_tables": ["quickbooks__profitability_analysis"]}] | [] | [] |
| B4 | [{"alias": "ordered", "kind": "derived", "block": "B3", "base_tables": ["quickbooks__profitability_analysis"]}] | [] | [] |
| B5 | [{"alias": "date_range", "kind": "derived", "block": "B1", "base_tables": ["quickbooks__profitability_analysis"]}] | [] | [] |
| B6 | [{"alias": "h", "kind": "derived", "block": "B4", "base_tables": ["quickbooks__profitability_analysis"]}, {"alias": "p", "kind": "base", "block": null, "base_tables": ["quickbooks__profitability_analysis"]}] | [{"type": "INNER", "right": "quickbooks__profitability_analysis AS p", "on": "h.customer_id = p.customer_id AND p.transaction_date >= (SELECT cutoff_date FROM date_range)", "using": []}] | ["h.customer_id", "STRFTIME('%Y', p.transaction_date)", "CAST((CAST(STRFTIME('%m', p.transaction_date) AS INTEGER) + 2) / 3 AS INTEGER)"] |
| B7 | [{"alias": "quarterly", "kind": "derived", "block": "B6", "base_tables": ["quickbooks__profitability_analysis"]}] | [] | [] |
| B8 | [{"alias": "qoqs", "kind": "derived", "block": "B7", "base_tables": ["quickbooks__profitability_analysis"]}] | [] | [] |
| B9 | [{"alias": "", "kind": "derived", "block": "B8", "base_tables": ["quickbooks__profitability_analysis"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | MAX(transaction_date) | [{"table": "quickbooks__profitability_analysis", "column": "transaction_date"}] | [] | False |
| B2 | AVG(customer_margin_volatility) | [{"table": "quickbooks__profitability_analysis", "column": "customer_margin_volatility"}] | [] | False |
| B6 | SUM(p.invoice_total) | [{"table": "quickbooks__profitability_analysis", "column": "invoice_total"}] | [] | False |
| B9 | AVG(qoq_growth) | [{"table": "quickbooks__profitability_analysis", "column": "customer_id"}, {"table": "quickbooks__profitability_analysis", "column": "invoice_total"}, {"table": "quickbooks__profitability_analysis", "column": "transaction_date"}, {"table": "quickbooks__profitability_analysis", "column": "transaction_date"}, {"table": "quickbooks__profitability_analysis", "column": "customer_id"}, {"table": "quickbooks__profitability_analysis", "column": "invoice_total"}, {"table": "quickbooks__profitability_analysis", "column": "transaction_date"}, {"table": "quickbooks__profitability_analysis", "column": "transaction_date"}, {"table": "quickbooks__profitability_analysis", "column": "customer_id"}, {"table": "quickbooks__profitability_analysis", "column": "invoice_total"}, {"table": "quickbooks__profitability_analysis", "column": "transaction_date"}, {"table": "quickbooks__profitability_analysis", "column": "transaction_date"}, {"table": "quickbooks__profitability_analysis", "column": "invoice_total"}, {"table": "quickbooks__profitability_analysis", "column": "customer_id"}, {"table": "quickbooks__profitability_analysis", "column": "invoice_total"}, {"table": "quickbooks__profitability_analysis", "column": "transaction_date"}, {"table": "quickbooks__profitability_analysis", "column": "transaction_date"}] | [] | False |
| B9 | COUNT(*) | [] | [] | True |
| B9 | AVG(qoq_growth * qoq_growth) | [{"table": "quickbooks__profitability_analysis", "column": "customer_id"}, {"table": "quickbooks__profitability_analysis", "column": "invoice_total"}, {"table": "quickbooks__profitability_analysis", "column": "transaction_date"}, {"table": "quickbooks__profitability_analysis", "column": "transaction_date"}, {"table": "quickbooks__profitability_analysis", "column": "customer_id"}, {"table": "quickbooks__profitability_analysis", "column": "invoice_total"}, {"table": "quickbooks__profitability_analysis", "column": "transaction_date"}, {"table": "quickbooks__profitability_analysis", "column": "transaction_date"}, {"table": "quickbooks__profitability_analysis", "column": "customer_id"}, {"table": "quickbooks__profitability_analysis", "column": "invoice_total"}, {"table": "quickbooks__profitability_analysis", "column": "transaction_date"}, {"table": "quickbooks__profitability_analysis", "column": "transaction_date"}, {"table": "quickbooks__profitability_analysis", "column": "invoice_total"}, {"table": "quickbooks__profitability_analysis", "column": "customer_id"}, {"table": "quickbooks__profitability_analysis", "column": "invoice_total"}, {"table": "quickbooks__profitability_analysis", "column": "transaction_date"}, {"table": "quickbooks__profitability_analysis", "column": "transaction_date"}, {"table": "quickbooks__profitability_analysis", "column": "customer_id"}, {"table": "quickbooks__profitability_analysis", "column": "invoice_total"}, {"table": "quickbooks__profitability_analysis", "column": "transaction_date"}, {"table": "quickbooks__profitability_analysis", "column": "transaction_date"}, {"table": "quickbooks__profitability_analysis", "column": "customer_id"}, {"table": "quickbooks__profitability_analysis", "column": "invoice_total"}, {"table": "quickbooks__profitability_analysis", "column": "transaction_date"}, {"table": "quickbooks__profitability_analysis", "column": "transaction_date"}, {"table": "quickbooks__profitability_analysis", "column": "customer_id"}, {"table": "quickbooks__profitability_analysis", "column": "invoice_total"}, {"table": "quickbooks__profitability_analysis", "column": "transaction_date"}, {"table": "quickbooks__profitability_analysis", "column": "transaction_date"}, {"table": "quickbooks__profitability_analysis", "column": "invoice_total"}, {"table": "quickbooks__profitability_analysis", "column": "customer_id"}, {"table": "quickbooks__profitability_analysis", "column": "invoice_total"}, {"table": "quickbooks__profitability_analysis", "column": "transaction_date"}, {"table": "quickbooks__profitability_analysis", "column": "transaction_date"}] | [] | False |
| B9 | AVG(qoq_growth) | [{"table": "quickbooks__profitability_analysis", "column": "customer_id"}, {"table": "quickbooks__profitability_analysis", "column": "invoice_total"}, {"table": "quickbooks__profitability_analysis", "column": "transaction_date"}, {"table": "quickbooks__profitability_analysis", "column": "transaction_date"}, {"table": "quickbooks__profitability_analysis", "column": "customer_id"}, {"table": "quickbooks__profitability_analysis", "column": "invoice_total"}, {"table": "quickbooks__profitability_analysis", "column": "transaction_date"}, {"table": "quickbooks__profitability_analysis", "column": "transaction_date"}, {"table": "quickbooks__profitability_analysis", "column": "customer_id"}, {"table": "quickbooks__profitability_analysis", "column": "invoice_total"}, {"table": "quickbooks__profitability_analysis", "column": "transaction_date"}, {"table": "quickbooks__profitability_analysis", "column": "transaction_date"}, {"table": "quickbooks__profitability_analysis", "column": "invoice_total"}, {"table": "quickbooks__profitability_analysis", "column": "customer_id"}, {"table": "quickbooks__profitability_analysis", "column": "invoice_total"}, {"table": "quickbooks__profitability_analysis", "column": "transaction_date"}, {"table": "quickbooks__profitability_analysis", "column": "transaction_date"}] | [] | False |
| B9 | AVG(qoq_growth) | [{"table": "quickbooks__profitability_analysis", "column": "customer_id"}, {"table": "quickbooks__profitability_analysis", "column": "invoice_total"}, {"table": "quickbooks__profitability_analysis", "column": "transaction_date"}, {"table": "quickbooks__profitability_analysis", "column": "transaction_date"}, {"table": "quickbooks__profitability_analysis", "column": "customer_id"}, {"table": "quickbooks__profitability_analysis", "column": "invoice_total"}, {"table": "quickbooks__profitability_analysis", "column": "transaction_date"}, {"table": "quickbooks__profitability_analysis", "column": "transaction_date"}, {"table": "quickbooks__profitability_analysis", "column": "customer_id"}, {"table": "quickbooks__profitability_analysis", "column": "invoice_total"}, {"table": "quickbooks__profitability_analysis", "column": "transaction_date"}, {"table": "quickbooks__profitability_analysis", "column": "transaction_date"}, {"table": "quickbooks__profitability_analysis", "column": "invoice_total"}, {"table": "quickbooks__profitability_analysis", "column": "customer_id"}, {"table": "quickbooks__profitability_analysis", "column": "invoice_total"}, {"table": "quickbooks__profitability_analysis", "column": "transaction_date"}, {"table": "quickbooks__profitability_analysis", "column": "transaction_date"}] | [] | False |
| B9 | AVG(qoq_growth * qoq_growth) | [{"table": "quickbooks__profitability_analysis", "column": "customer_id"}, {"table": "quickbooks__profitability_analysis", "column": "invoice_total"}, {"table": "quickbooks__profitability_analysis", "column": "transaction_date"}, {"table": "quickbooks__profitability_analysis", "column": "transaction_date"}, {"table": "quickbooks__profitability_analysis", "column": "customer_id"}, {"table": "quickbooks__profitability_analysis", "column": "invoice_total"}, {"table": "quickbooks__profitability_analysis", "column": "transaction_date"}, {"table": "quickbooks__profitability_analysis", "column": "transaction_date"}, {"table": "quickbooks__profitability_analysis", "column": "customer_id"}, {"table": "quickbooks__profitability_analysis", "column": "invoice_total"}, {"table": "quickbooks__profitability_analysis", "column": "transaction_date"}, {"table": "quickbooks__profitability_analysis", "column": "transaction_date"}, {"table": "quickbooks__profitability_analysis", "column": "invoice_total"}, {"table": "quickbooks__profitability_analysis", "column": "customer_id"}, {"table": "quickbooks__profitability_analysis", "column": "invoice_total"}, {"table": "quickbooks__profitability_analysis", "column": "transaction_date"}, {"table": "quickbooks__profitability_analysis", "column": "transaction_date"}, {"table": "quickbooks__profitability_analysis", "column": "customer_id"}, {"table": "quickbooks__profitability_analysis", "column": "invoice_total"}, {"table": "quickbooks__profitability_analysis", "column": "transaction_date"}, {"table": "quickbooks__profitability_analysis", "column": "transaction_date"}, {"table": "quickbooks__profitability_analysis", "column": "customer_id"}, {"table": "quickbooks__profitability_analysis", "column": "invoice_total"}, {"table": "quickbooks__profitability_analysis", "column": "transaction_date"}, {"table": "quickbooks__profitability_analysis", "column": "transaction_date"}, {"table": "quickbooks__profitability_analysis", "column": "customer_id"}, {"table": "quickbooks__profitability_analysis", "column": "invoice_total"}, {"table": "quickbooks__profitability_analysis", "column": "transaction_date"}, {"table": "quickbooks__profitability_analysis", "column": "transaction_date"}, {"table": "quickbooks__profitability_analysis", "column": "invoice_total"}, {"table": "quickbooks__profitability_analysis", "column": "customer_id"}, {"table": "quickbooks__profitability_analysis", "column": "invoice_total"}, {"table": "quickbooks__profitability_analysis", "column": "transaction_date"}, {"table": "quickbooks__profitability_analysis", "column": "transaction_date"}] | [] | False |
| B9 | AVG(qoq_growth) | [{"table": "quickbooks__profitability_analysis", "column": "customer_id"}, {"table": "quickbooks__profitability_analysis", "column": "invoice_total"}, {"table": "quickbooks__profitability_analysis", "column": "transaction_date"}, {"table": "quickbooks__profitability_analysis", "column": "transaction_date"}, {"table": "quickbooks__profitability_analysis", "column": "customer_id"}, {"table": "quickbooks__profitability_analysis", "column": "invoice_total"}, {"table": "quickbooks__profitability_analysis", "column": "transaction_date"}, {"table": "quickbooks__profitability_analysis", "column": "transaction_date"}, {"table": "quickbooks__profitability_analysis", "column": "customer_id"}, {"table": "quickbooks__profitability_analysis", "column": "invoice_total"}, {"table": "quickbooks__profitability_analysis", "column": "transaction_date"}, {"table": "quickbooks__profitability_analysis", "column": "transaction_date"}, {"table": "quickbooks__profitability_analysis", "column": "invoice_total"}, {"table": "quickbooks__profitability_analysis", "column": "customer_id"}, {"table": "quickbooks__profitability_analysis", "column": "invoice_total"}, {"table": "quickbooks__profitability_analysis", "column": "transaction_date"}, {"table": "quickbooks__profitability_analysis", "column": "transaction_date"}] | [] | False |
| B9 | AVG(qoq_growth) | [{"table": "quickbooks__profitability_analysis", "column": "customer_id"}, {"table": "quickbooks__profitability_analysis", "column": "invoice_total"}, {"table": "quickbooks__profitability_analysis", "column": "transaction_date"}, {"table": "quickbooks__profitability_analysis", "column": "transaction_date"}, {"table": "quickbooks__profitability_analysis", "column": "customer_id"}, {"table": "quickbooks__profitability_analysis", "column": "invoice_total"}, {"table": "quickbooks__profitability_analysis", "column": "transaction_date"}, {"table": "quickbooks__profitability_analysis", "column": "transaction_date"}, {"table": "quickbooks__profitability_analysis", "column": "customer_id"}, {"table": "quickbooks__profitability_analysis", "column": "invoice_total"}, {"table": "quickbooks__profitability_analysis", "column": "transaction_date"}, {"table": "quickbooks__profitability_analysis", "column": "transaction_date"}, {"table": "quickbooks__profitability_analysis", "column": "invoice_total"}, {"table": "quickbooks__profitability_analysis", "column": "customer_id"}, {"table": "quickbooks__profitability_analysis", "column": "invoice_total"}, {"table": "quickbooks__profitability_analysis", "column": "transaction_date"}, {"table": "quickbooks__profitability_analysis", "column": "transaction_date"}] | [] | False |


未解析列血缘：[{"block": "B9", "column": "cutoff_date", "reason": "ambiguous_or_missing_source"}]

## S36

类别 `data`；来源 `query_db`；调用 `285e0944263f471bbe393f7aa690cc22`；状态 `success`。

```sql
-- Behavioral profile of high-vol customers
WITH cust_vol AS (
  SELECT customer_id, AVG(customer_margin_volatility) AS vol
  FROM quickbooks__profitability_analysis
  GROUP BY customer_id
),
ordered AS (
  SELECT customer_id, vol,
    ROW_NUMBER() OVER (ORDER BY vol DESC) AS rn,
    COUNT(*) OVER () AS total
  FROM cust_vol
),
seg AS (
  SELECT customer_id, vol,
    CASE WHEN rn <= total * 0.25 THEN 'HighVol'
         WHEN rn > total * 0.75 THEN 'LowVol'
         ELSE 'MidVol' END AS vol_segment
  FROM ordered
)
SELECT 
  s.vol_segment,
  a.rfm_segment,
  COUNT(*) AS n_customers
FROM seg s
JOIN quickbooks__customer_analytics a ON s.customer_id = a.customer_id
GROUP BY s.vol_segment, a.rfm_segment
ORDER BY s.vol_segment, n_customers DESC
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-092/attempt-01/sql/S36.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-092/attempt-01/sql/S36.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-092/attempt-01/results/S36.rows.jsonl)；完整：True；SHA256：`e8e4c76208041784d76d45ec8883ce004ca9425092c8b5e2e03d5aac83725087`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "quickbooks__profitability_analysis", "kind": "base", "block": null, "base_tables": ["quickbooks__profitability_analysis"]}] | [] | ["customer_id"] |
| B2 | [{"alias": "cust_vol", "kind": "derived", "block": "B1", "base_tables": ["quickbooks__profitability_analysis"]}] | [] | [] |
| B3 | [{"alias": "ordered", "kind": "derived", "block": "B2", "base_tables": ["quickbooks__profitability_analysis"]}] | [] | [] |
| B4 | [{"alias": "s", "kind": "derived", "block": "B3", "base_tables": ["quickbooks__profitability_analysis"]}, {"alias": "a", "kind": "base", "block": null, "base_tables": ["quickbooks__customer_analytics"]}] | [{"type": "INNER", "right": "quickbooks__customer_analytics AS a", "on": "s.customer_id = a.customer_id", "using": []}] | ["s.vol_segment", "a.rfm_segment"] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | AVG(customer_margin_volatility) | [{"table": "quickbooks__profitability_analysis", "column": "customer_margin_volatility"}] | [] | False |
| B4 | COUNT(*) | [] | [] | True |


## S37

类别 `data`；来源 `query_db`；调用 `0a6c09598fad40109c1b69298069166e`；状态 `success`。

```sql
-- Payment behavior profile by volatility segment
WITH cust_vol AS (
  SELECT customer_id, AVG(customer_margin_volatility) AS vol
  FROM quickbooks__profitability_analysis
  GROUP BY customer_id
),
ordered AS (
  SELECT customer_id, vol,
    ROW_NUMBER() OVER (ORDER BY vol DESC) AS rn,
    COUNT(*) OVER () AS total
  FROM cust_vol
),
seg AS (
  SELECT customer_id, vol,
    CASE WHEN rn <= total * 0.25 THEN 'HighVol'
         WHEN rn > total * 0.75 THEN 'LowVol'
         ELSE 'MidVol' END AS vol_segment
  FROM ordered
)
SELECT 
  s.vol_segment,
  a.payment_behavior,
  COUNT(*) AS n_customers
FROM seg s
JOIN quickbooks__customer_analytics a ON s.customer_id = a.customer_id
GROUP BY s.vol_segment, a.payment_behavior
ORDER BY s.vol_segment, n_customers DESC
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-092/attempt-01/sql/S37.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-092/attempt-01/sql/S37.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-092/attempt-01/results/S37.rows.jsonl)；完整：True；SHA256：`18557deccf5300dddef9dc7adf559a63f44b8393b3a0a35267e768db031fded0`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "quickbooks__profitability_analysis", "kind": "base", "block": null, "base_tables": ["quickbooks__profitability_analysis"]}] | [] | ["customer_id"] |
| B2 | [{"alias": "cust_vol", "kind": "derived", "block": "B1", "base_tables": ["quickbooks__profitability_analysis"]}] | [] | [] |
| B3 | [{"alias": "ordered", "kind": "derived", "block": "B2", "base_tables": ["quickbooks__profitability_analysis"]}] | [] | [] |
| B4 | [{"alias": "s", "kind": "derived", "block": "B3", "base_tables": ["quickbooks__profitability_analysis"]}, {"alias": "a", "kind": "base", "block": null, "base_tables": ["quickbooks__customer_analytics"]}] | [{"type": "INNER", "right": "quickbooks__customer_analytics AS a", "on": "s.customer_id = a.customer_id", "using": []}] | ["s.vol_segment", "a.payment_behavior"] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | AVG(customer_margin_volatility) | [{"table": "quickbooks__profitability_analysis", "column": "customer_margin_volatility"}] | [] | False |
| B4 | COUNT(*) | [] | [] | True |


## S38

类别 `data`；来源 `query_db`；调用 `b195db71d87e48a0a5ac4e8513c34e67`；状态 `success`。

```sql
-- Lifecycle stage profile by volatility segment
WITH cust_vol AS (
  SELECT customer_id, AVG(customer_margin_volatility) AS vol
  FROM quickbooks__profitability_analysis
  GROUP BY customer_id
),
ordered AS (
  SELECT customer_id, vol,
    ROW_NUMBER() OVER (ORDER BY vol DESC) AS rn,
    COUNT(*) OVER () AS total
  FROM cust_vol
),
seg AS (
  SELECT customer_id, vol,
    CASE WHEN rn <= total * 0.25 THEN 'HighVol'
         WHEN rn > total * 0.75 THEN 'LowVol'
         ELSE 'MidVol' END AS vol_segment
  FROM ordered
)
SELECT 
  s.vol_segment,
  a.lifecycle_stage,
  COUNT(*) AS n_customers
FROM seg s
JOIN quickbooks__customer_analytics a ON s.customer_id = a.customer_id
GROUP BY s.vol_segment, a.lifecycle_stage
ORDER BY s.vol_segment, n_customers DESC
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-092/attempt-01/sql/S38.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-092/attempt-01/sql/S38.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-092/attempt-01/results/S38.rows.jsonl)；完整：True；SHA256：`55dc89fa52a478d20cacba36963dd25373fa6481aadd647ab016ef9ad46e4104`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "quickbooks__profitability_analysis", "kind": "base", "block": null, "base_tables": ["quickbooks__profitability_analysis"]}] | [] | ["customer_id"] |
| B2 | [{"alias": "cust_vol", "kind": "derived", "block": "B1", "base_tables": ["quickbooks__profitability_analysis"]}] | [] | [] |
| B3 | [{"alias": "ordered", "kind": "derived", "block": "B2", "base_tables": ["quickbooks__profitability_analysis"]}] | [] | [] |
| B4 | [{"alias": "s", "kind": "derived", "block": "B3", "base_tables": ["quickbooks__profitability_analysis"]}, {"alias": "a", "kind": "base", "block": null, "base_tables": ["quickbooks__customer_analytics"]}] | [{"type": "INNER", "right": "quickbooks__customer_analytics AS a", "on": "s.customer_id = a.customer_id", "using": []}] | ["s.vol_segment", "a.lifecycle_stage"] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | AVG(customer_margin_volatility) | [{"table": "quickbooks__profitability_analysis", "column": "customer_margin_volatility"}] | [] | False |
| B4 | COUNT(*) | [] | [] | True |


## S39

类别 `data`；来源 `query_db`；调用 `70836f5648bc4141a07fd8d3b3a1d436`；状态 `success`。

```sql
-- Revenue trend correlation and other continuous behavioral features by segment
WITH cust_vol AS (
  SELECT customer_id, AVG(customer_margin_volatility) AS vol
  FROM quickbooks__profitability_analysis
  GROUP BY customer_id
),
ordered AS (
  SELECT customer_id, vol,
    ROW_NUMBER() OVER (ORDER BY vol DESC) AS rn,
    COUNT(*) OVER () AS total
  FROM cust_vol
),
seg AS (
  SELECT customer_id, vol,
    CASE WHEN rn <= total * 0.25 THEN 'HighVol'
         WHEN rn > total * 0.75 THEN 'LowVol'
         ELSE 'MidVol' END AS vol_segment
  FROM ordered
)
SELECT 
  s.vol_segment,
  COUNT(*) AS n,
  AVG(a.revenue_trend_correlation) AS avg_trend_corr,
  AVG(a.credit_score) AS avg_credit_score,
  AVG(a.avg_payment_days_12m) AS avg_payment_days,
  AVG(a.overdue_count_12m) AS avg_overdue_count,
  AVG(a.overall_customer_score) AS avg_overall_score,
  AVG(a.revenue_volatility) AS avg_rev_volatility
FROM seg s
JOIN quickbooks__customer_analytics a ON s.customer_id = a.customer_id
GROUP BY s.vol_segment
ORDER BY s.vol_segment
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-092/attempt-01/sql/S39.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-092/attempt-01/sql/S39.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-092/attempt-01/results/S39.rows.jsonl)；完整：True；SHA256：`cfc2b5bc69eede81de891616a00f5bfeb6c931277d4184e5613db9c4f014222f`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "quickbooks__profitability_analysis", "kind": "base", "block": null, "base_tables": ["quickbooks__profitability_analysis"]}] | [] | ["customer_id"] |
| B2 | [{"alias": "cust_vol", "kind": "derived", "block": "B1", "base_tables": ["quickbooks__profitability_analysis"]}] | [] | [] |
| B3 | [{"alias": "ordered", "kind": "derived", "block": "B2", "base_tables": ["quickbooks__profitability_analysis"]}] | [] | [] |
| B4 | [{"alias": "s", "kind": "derived", "block": "B3", "base_tables": ["quickbooks__profitability_analysis"]}, {"alias": "a", "kind": "base", "block": null, "base_tables": ["quickbooks__customer_analytics"]}] | [{"type": "INNER", "right": "quickbooks__customer_analytics AS a", "on": "s.customer_id = a.customer_id", "using": []}] | ["s.vol_segment"] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | AVG(customer_margin_volatility) | [{"table": "quickbooks__profitability_analysis", "column": "customer_margin_volatility"}] | [] | False |
| B4 | COUNT(*) | [] | [] | True |
| B4 | AVG(a.revenue_trend_correlation) | [{"table": "quickbooks__customer_analytics", "column": "revenue_trend_correlation"}] | [] | False |
| B4 | AVG(a.credit_score) | [{"table": "quickbooks__customer_analytics", "column": "credit_score"}] | [] | False |
| B4 | AVG(a.avg_payment_days_12m) | [{"table": "quickbooks__customer_analytics", "column": "avg_payment_days_12m"}] | [] | False |
| B4 | AVG(a.overdue_count_12m) | [{"table": "quickbooks__customer_analytics", "column": "overdue_count_12m"}] | [] | False |
| B4 | AVG(a.overall_customer_score) | [{"table": "quickbooks__customer_analytics", "column": "overall_customer_score"}] | [] | False |
| B4 | AVG(a.revenue_volatility) | [{"table": "quickbooks__customer_analytics", "column": "revenue_volatility"}] | [] | False |


## S40

类别 `data`；来源 `query_db`；调用 `bb98c000d5834162a01b25c88aa51434`；状态 `success`。

```sql
SELECT 
  COUNT(*) AS total,
  COUNT(revenue_trend_correlation) AS n_trend_corr,
  COUNT(credit_score) AS n_credit,
  COUNT(avg_payment_days_12m) AS n_pay_days,
  COUNT(overdue_count_12m) AS n_overdue,
  COUNT(overall_customer_score) AS n_overall,
  COUNT(revenue_volatility) AS n_rev_vol,
  COUNT(rfm_segment) AS n_rfm,
  COUNT(payment_behavior) AS n_payment,
  COUNT(lifecycle_stage) AS n_lifecycle,
  COUNT(customer_value_segment) AS n_value_seg,
  COUNT(risk_assessment) AS n_risk,
  COUNT(credit_grade) AS n_credit_grade,
  COUNT(payment_timeliness_score) AS n_pay_timeliness,
  COUNT(business_stability_score) AS n_biz_stab
FROM quickbooks__customer_analytics
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-092/attempt-01/sql/S40.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-092/attempt-01/sql/S40.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-092/attempt-01/results/S40.rows.jsonl)；完整：True；SHA256：`495e8b96083f4867d42564fa55e51954c3984b2bbb65c725702592867990213b`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "quickbooks__customer_analytics", "kind": "base", "block": null, "base_tables": ["quickbooks__customer_analytics"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |
| B1 | COUNT(revenue_trend_correlation) | [{"table": "quickbooks__customer_analytics", "column": "revenue_trend_correlation"}] | [] | False |
| B1 | COUNT(credit_score) | [{"table": "quickbooks__customer_analytics", "column": "credit_score"}] | [] | False |
| B1 | COUNT(avg_payment_days_12m) | [{"table": "quickbooks__customer_analytics", "column": "avg_payment_days_12m"}] | [] | False |
| B1 | COUNT(overdue_count_12m) | [{"table": "quickbooks__customer_analytics", "column": "overdue_count_12m"}] | [] | False |
| B1 | COUNT(overall_customer_score) | [{"table": "quickbooks__customer_analytics", "column": "overall_customer_score"}] | [] | False |
| B1 | COUNT(revenue_volatility) | [{"table": "quickbooks__customer_analytics", "column": "revenue_volatility"}] | [] | False |
| B1 | COUNT(rfm_segment) | [{"table": "quickbooks__customer_analytics", "column": "rfm_segment"}] | [] | False |
| B1 | COUNT(payment_behavior) | [{"table": "quickbooks__customer_analytics", "column": "payment_behavior"}] | [] | False |
| B1 | COUNT(lifecycle_stage) | [{"table": "quickbooks__customer_analytics", "column": "lifecycle_stage"}] | [] | False |
| B1 | COUNT(customer_value_segment) | [{"table": "quickbooks__customer_analytics", "column": "customer_value_segment"}] | [] | False |
| B1 | COUNT(risk_assessment) | [{"table": "quickbooks__customer_analytics", "column": "risk_assessment"}] | [] | False |
| B1 | COUNT(credit_grade) | [{"table": "quickbooks__customer_analytics", "column": "credit_grade"}] | [] | False |
| B1 | COUNT(payment_timeliness_score) | [{"table": "quickbooks__customer_analytics", "column": "payment_timeliness_score"}] | [] | False |
| B1 | COUNT(business_stability_score) | [{"table": "quickbooks__customer_analytics", "column": "business_stability_score"}] | [] | False |


## S41

类别 `connection_setup`；来源 `connection`；调用 `0fa8b32d6f974180ad1c65758a1c6205`；状态 `success`。

```sql
PRAGMA query_only=ON
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-092/attempt-01/sql/S41.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-092/attempt-01/sql/S41.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-092/attempt-01/results/S41.rows.jsonl)；完整：True；SHA256：`e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`。

## S42

类别 `data`；来源 `query_db`；调用 `0fa8b32d6f974180ad1c65758a1c6205`；状态 `success`。

```sql
SELECT 
  COUNT(*) AS total,
  COUNT(customer_value_segment) AS n_value_seg,
  COUNT(business_stability_score) AS n_biz_stab,
  COUNT(activity_status) AS n_activity,
  COUNT(customer_maturity_stage) AS n_maturity,
  COUNT(revenue_growth_rate_12m) AS n_growth12,
  COUNT(active_months_last_12) AS n_act_months,
  COUNT(payment_rate_percentage) AS n_pay_rate,
  COUNT(data_quality_flag) AS n_dq,
  COUNT(recommended_action) AS n_recommended
FROM quickbooks__customer_analytics
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-092/attempt-01/sql/S42.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-092/attempt-01/sql/S42.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-092/attempt-01/results/S42.rows.jsonl)；完整：True；SHA256：`37e3c7bd4b8e66e1030f67284e904136557d2a9c9dbd9ee98e7157624798ef72`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "quickbooks__customer_analytics", "kind": "base", "block": null, "base_tables": ["quickbooks__customer_analytics"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |
| B1 | COUNT(customer_value_segment) | [{"table": "quickbooks__customer_analytics", "column": "customer_value_segment"}] | [] | False |
| B1 | COUNT(business_stability_score) | [{"table": "quickbooks__customer_analytics", "column": "business_stability_score"}] | [] | False |
| B1 | COUNT(activity_status) | [{"table": "quickbooks__customer_analytics", "column": "activity_status"}] | [] | False |
| B1 | COUNT(customer_maturity_stage) | [{"table": "quickbooks__customer_analytics", "column": "customer_maturity_stage"}] | [] | False |
| B1 | COUNT(revenue_growth_rate_12m) | [{"table": "quickbooks__customer_analytics", "column": "revenue_growth_rate_12m"}] | [] | False |
| B1 | COUNT(active_months_last_12) | [{"table": "quickbooks__customer_analytics", "column": "active_months_last_12"}] | [] | False |
| B1 | COUNT(payment_rate_percentage) | [{"table": "quickbooks__customer_analytics", "column": "payment_rate_percentage"}] | [] | False |
| B1 | COUNT(data_quality_flag) | [{"table": "quickbooks__customer_analytics", "column": "data_quality_flag"}] | [] | False |
| B1 | COUNT(recommended_action) | [{"table": "quickbooks__customer_analytics", "column": "recommended_action"}] | [] | False |


## S43

类别 `data`；来源 `query_db`；调用 `859949c1877347fc94a4c07de47ec860`；状态 `success`。

```sql
SELECT DISTINCT customer_value_segment FROM quickbooks__customer_analytics
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-092/attempt-01/sql/S43.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-092/attempt-01/sql/S43.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-092/attempt-01/results/S43.rows.jsonl)；完整：True；SHA256：`f0ca99433ebec10412201b83b4445b68fadc6634e070901ab22c964470759d51`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "quickbooks__customer_analytics", "kind": "base", "block": null, "base_tables": ["quickbooks__customer_analytics"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |


## S44

类别 `data`；来源 `query_db`；调用 `1a1a32e4ae7747b69c77462d2a835572`；状态 `success`。

```sql
-- Customer value segment by volatility segment
WITH cust_vol AS (
  SELECT customer_id, AVG(customer_margin_volatility) AS vol
  FROM quickbooks__profitability_analysis
  GROUP BY customer_id
),
ordered AS (
  SELECT customer_id, vol,
    ROW_NUMBER() OVER (ORDER BY vol DESC) AS rn,
    COUNT(*) OVER () AS total
  FROM cust_vol
),
seg AS (
  SELECT customer_id, vol,
    CASE WHEN rn <= total * 0.25 THEN 'HighVol'
         WHEN rn > total * 0.75 THEN 'LowVol'
         ELSE 'MidVol' END AS vol_segment
  FROM ordered
)
SELECT 
  s.vol_segment,
  a.customer_value_segment,
  COUNT(*) AS n_customers,
  ROUND(100.0 * COUNT(*) / SUM(COUNT(*)) OVER (PARTITION BY s.vol_segment), 1) AS pct
FROM seg s
JOIN quickbooks__customer_analytics a ON s.customer_id = a.customer_id
GROUP BY s.vol_segment, a.customer_value_segment
ORDER BY s.vol_segment, n_customers DESC
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-092/attempt-01/sql/S44.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-092/attempt-01/sql/S44.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-092/attempt-01/results/S44.rows.jsonl)；完整：True；SHA256：`1c61879bd0b197470349a786a9e0179637b90ba6240b0f6fae907da00fd6f121`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "quickbooks__profitability_analysis", "kind": "base", "block": null, "base_tables": ["quickbooks__profitability_analysis"]}] | [] | ["customer_id"] |
| B2 | [{"alias": "cust_vol", "kind": "derived", "block": "B1", "base_tables": ["quickbooks__profitability_analysis"]}] | [] | [] |
| B3 | [{"alias": "ordered", "kind": "derived", "block": "B2", "base_tables": ["quickbooks__profitability_analysis"]}] | [] | [] |
| B4 | [{"alias": "s", "kind": "derived", "block": "B3", "base_tables": ["quickbooks__profitability_analysis"]}, {"alias": "a", "kind": "base", "block": null, "base_tables": ["quickbooks__customer_analytics"]}] | [{"type": "INNER", "right": "quickbooks__customer_analytics AS a", "on": "s.customer_id = a.customer_id", "using": []}] | ["s.vol_segment", "a.customer_value_segment"] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | AVG(customer_margin_volatility) | [{"table": "quickbooks__profitability_analysis", "column": "customer_margin_volatility"}] | [] | False |
| B4 | COUNT(*) | [] | [] | True |
| B4 | COUNT(*) | [] | [] | True |
| B4 | COUNT(*) | [] | [] | True |


## S45

类别 `data`；来源 `query_db`；调用 `71903b0d28d04f32b53669bba24d1b08`；状态 `success`。

```sql
-- Business stability score, active months, revenue growth by segment
WITH cust_vol AS (
  SELECT customer_id, AVG(customer_margin_volatility) AS vol
  FROM quickbooks__profitability_analysis
  GROUP BY customer_id
),
ordered AS (
  SELECT customer_id, vol,
    ROW_NUMBER() OVER (ORDER BY vol DESC) AS rn,
    COUNT(*) OVER () AS total
  FROM cust_vol
),
seg AS (
  SELECT customer_id, vol,
    CASE WHEN rn <= total * 0.25 THEN 'HighVol'
         WHEN rn > total * 0.75 THEN 'LowVol'
         ELSE 'MidVol' END AS vol_segment
  FROM ordered
)
SELECT 
  s.vol_segment,
  COUNT(*) AS n,
  AVG(a.business_stability_score) AS avg_stability,
  AVG(a.active_months_last_12) AS avg_active_months,
  AVG(a.revenue_growth_rate_12m) AS avg_growth12,
  AVG(a.revenue_trend_correlation) AS avg_trend_corr,
  AVG(a.revenue_volatility) AS avg_rev_vol,
  AVG(a.days_since_last_invoice) AS avg_days_since_last
FROM seg s
JOIN quickbooks__customer_analytics a ON s.customer_id = a.customer_id
GROUP BY s.vol_segment
ORDER BY s.vol_segment
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-092/attempt-01/sql/S45.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-092/attempt-01/sql/S45.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-092/attempt-01/results/S45.rows.jsonl)；完整：True；SHA256：`9d33f9b37d6f4fc7cde5ef6fae154306bed1b4b8828f44551558c2c29373558e`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "quickbooks__profitability_analysis", "kind": "base", "block": null, "base_tables": ["quickbooks__profitability_analysis"]}] | [] | ["customer_id"] |
| B2 | [{"alias": "cust_vol", "kind": "derived", "block": "B1", "base_tables": ["quickbooks__profitability_analysis"]}] | [] | [] |
| B3 | [{"alias": "ordered", "kind": "derived", "block": "B2", "base_tables": ["quickbooks__profitability_analysis"]}] | [] | [] |
| B4 | [{"alias": "s", "kind": "derived", "block": "B3", "base_tables": ["quickbooks__profitability_analysis"]}, {"alias": "a", "kind": "base", "block": null, "base_tables": ["quickbooks__customer_analytics"]}] | [{"type": "INNER", "right": "quickbooks__customer_analytics AS a", "on": "s.customer_id = a.customer_id", "using": []}] | ["s.vol_segment"] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | AVG(customer_margin_volatility) | [{"table": "quickbooks__profitability_analysis", "column": "customer_margin_volatility"}] | [] | False |
| B4 | COUNT(*) | [] | [] | True |
| B4 | AVG(a.business_stability_score) | [{"table": "quickbooks__customer_analytics", "column": "business_stability_score"}] | [] | False |
| B4 | AVG(a.active_months_last_12) | [{"table": "quickbooks__customer_analytics", "column": "active_months_last_12"}] | [] | False |
| B4 | AVG(a.revenue_growth_rate_12m) | [{"table": "quickbooks__customer_analytics", "column": "revenue_growth_rate_12m"}] | [] | False |
| B4 | AVG(a.revenue_trend_correlation) | [{"table": "quickbooks__customer_analytics", "column": "revenue_trend_correlation"}] | [] | False |
| B4 | AVG(a.revenue_volatility) | [{"table": "quickbooks__customer_analytics", "column": "revenue_volatility"}] | [] | False |
| B4 | AVG(a.days_since_last_invoice) | [{"table": "quickbooks__customer_analytics", "column": "days_since_last_invoice"}] | [] | False |


## S46

类别 `data`；来源 `query_db`；调用 `ba0668a881d6437da984d42153f03a15`；状态 `success`。

```sql
SELECT dashboard_month, total_revenue, collected_revenue, outstanding_receivables, gross_profit, gross_margin_percentage, collection_rate_percentage, collection_risk_level, business_health_score, revenue_growth_rate, high_risk_transactions
FROM quickbooks__financial_dashboard
ORDER BY dashboard_month
LIMIT 35
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-092/attempt-01/sql/S46.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-092/attempt-01/sql/S46.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-092/attempt-01/results/S46.rows.jsonl)；完整：True；SHA256：`966944fd6ce229f9efea266ca4952176fff86af8b240fa2dd9533b2f6877efcd`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "quickbooks__financial_dashboard", "kind": "base", "block": null, "base_tables": ["quickbooks__financial_dashboard"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |


## S47

类别 `data`；来源 `query_db`；调用 `34560c8317444ab5aa44954422a9c234`；状态 `success`。

```sql
-- Monthly contribution of high-vol customers vs overall, matched to dashboard months
WITH cust_vol AS (
  SELECT customer_id, AVG(customer_margin_volatility) AS vol
  FROM quickbooks__profitability_analysis
  GROUP BY customer_id
),
ordered AS (
  SELECT customer_id, vol,
    ROW_NUMBER() OVER (ORDER BY vol DESC) AS rn,
    COUNT(*) OVER () AS total
  FROM cust_vol
),
high_vol_cust AS (
  SELECT customer_id FROM ordered WHERE rn <= total * 0.25
),
monthly_seg AS (
  SELECT 
    p.revenue_month_start,
    CASE WHEN h.customer_id IS NOT NULL THEN 'HighVol' ELSE 'Other' END AS grp,
    SUM(p.invoice_total) AS invoice_total,
    SUM(p.gross_profit) AS gross_profit,
    SUM(p.outstanding_balance) AS outstanding
  FROM quickbooks__profitability_analysis p
  LEFT JOIN high_vol_cust h ON p.customer_id = h.customer_id
  GROUP BY p.revenue_month_start, CASE WHEN h.customer_id IS NOT NULL THEN 'HighVol' ELSE 'Other' END
)
SELECT 
  m.revenue_month_start,
  SUM(CASE WHEN grp='HighVol' THEN invoice_total ELSE 0 END) AS hv_rev,
  SUM(invoice_total) AS total_rev,
  ROUND(100.0 * SUM(CASE WHEN grp='HighVol' THEN invoice_total ELSE 0 END) / SUM(invoice_total), 2) AS hv_rev_share_pct,
  SUM(CASE WHEN grp='HighVol' THEN gross_profit ELSE 0 END) AS hv_gp,
  SUM(gross_profit) AS total_gp,
  ROUND(100.0 * SUM(CASE WHEN grp='HighVol' THEN gross_profit ELSE 0 END) / NULLIF(SUM(gross_profit),0), 2) AS hv_gp_share_pct
FROM monthly_seg m
GROUP BY m.revenue_month_start
HAVING revenue_month_start >= '2023-01-01'
ORDER BY m.revenue_month_start
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-092/attempt-01/sql/S47.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-092/attempt-01/sql/S47.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-092/attempt-01/results/S47.rows.jsonl)；完整：True；SHA256：`3fa8d77d783efc9ecf4d6ffcd15157a62bfddf4f5125a56f95465f18f138aed5`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "quickbooks__profitability_analysis", "kind": "base", "block": null, "base_tables": ["quickbooks__profitability_analysis"]}] | [] | ["customer_id"] |
| B2 | [{"alias": "cust_vol", "kind": "derived", "block": "B1", "base_tables": ["quickbooks__profitability_analysis"]}] | [] | [] |
| B3 | [{"alias": "ordered", "kind": "derived", "block": "B2", "base_tables": ["quickbooks__profitability_analysis"]}] | [] | [] |
| B4 | [{"alias": "p", "kind": "base", "block": null, "base_tables": ["quickbooks__profitability_analysis"]}, {"alias": "h", "kind": "derived", "block": "B3", "base_tables": ["quickbooks__profitability_analysis"]}] | [{"type": "LEFT", "right": "high_vol_cust AS h", "on": "p.customer_id = h.customer_id", "using": []}] | ["p.revenue_month_start", "CASE WHEN NOT h.customer_id IS NULL THEN 'HighVol' ELSE 'Other' END"] |
| B5 | [{"alias": "m", "kind": "derived", "block": "B4", "base_tables": ["quickbooks__profitability_analysis"]}] | [] | ["m.revenue_month_start"] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | AVG(customer_margin_volatility) | [{"table": "quickbooks__profitability_analysis", "column": "customer_margin_volatility"}] | [] | False |
| B4 | SUM(p.invoice_total) | [{"table": "quickbooks__profitability_analysis", "column": "invoice_total"}] | [] | False |
| B4 | SUM(p.gross_profit) | [{"table": "quickbooks__profitability_analysis", "column": "gross_profit"}] | [] | False |
| B4 | SUM(p.outstanding_balance) | [{"table": "quickbooks__profitability_analysis", "column": "outstanding_balance"}] | [] | False |
| B5 | SUM(CASE WHEN grp = 'HighVol' THEN invoice_total ELSE 0 END) | [{"table": "quickbooks__profitability_analysis", "column": "invoice_total"}] | [{"table": "quickbooks__profitability_analysis", "column": "customer_id"}] | False |
| B5 | SUM(invoice_total) | [{"table": "quickbooks__profitability_analysis", "column": "invoice_total"}] | [] | False |
| B5 | SUM(CASE WHEN grp = 'HighVol' THEN gross_profit ELSE 0 END) | [{"table": "quickbooks__profitability_analysis", "column": "gross_profit"}] | [{"table": "quickbooks__profitability_analysis", "column": "customer_id"}] | False |
| B5 | SUM(gross_profit) | [{"table": "quickbooks__profitability_analysis", "column": "gross_profit"}] | [] | False |
| B5 | SUM(invoice_total) | [{"table": "quickbooks__profitability_analysis", "column": "invoice_total"}] | [] | False |
| B5 | SUM(CASE WHEN grp = 'HighVol' THEN invoice_total ELSE 0 END) | [{"table": "quickbooks__profitability_analysis", "column": "invoice_total"}] | [{"table": "quickbooks__profitability_analysis", "column": "customer_id"}] | False |
| B5 | SUM(CASE WHEN grp = 'HighVol' THEN gross_profit ELSE 0 END) | [{"table": "quickbooks__profitability_analysis", "column": "gross_profit"}] | [{"table": "quickbooks__profitability_analysis", "column": "customer_id"}] | False |
| B5 | SUM(gross_profit) | [{"table": "quickbooks__profitability_analysis", "column": "gross_profit"}] | [] | False |


## S48

类别 `data`；来源 `query_db`；调用 `84bbde203e1b4f15a196af8d78ddd6e4`；状态 `success`。

```sql
-- Join monthly high-vol share with financial dashboard
WITH cust_vol AS (
  SELECT customer_id, AVG(customer_margin_volatility) AS vol
  FROM quickbooks__profitability_analysis
  GROUP BY customer_id
),
ordered AS (
  SELECT customer_id, vol,
    ROW_NUMBER() OVER (ORDER BY vol DESC) AS rn,
    COUNT(*) OVER () AS total
  FROM cust_vol
),
high_vol_cust AS (
  SELECT customer_id FROM ordered WHERE rn <= total * 0.25
),
monthly_seg AS (
  SELECT 
    p.revenue_month_start,
    SUM(CASE WHEN h.customer_id IS NOT NULL THEN p.invoice_total ELSE 0 END) AS hv_rev,
    SUM(p.invoice_total) AS total_rev,
    SUM(CASE WHEN h.customer_id IS NOT NULL THEN p.gross_profit ELSE 0 END) AS hv_gp,
    SUM(p.gross_profit) AS total_gp
  FROM quickbooks__profitability_analysis p
  LEFT JOIN high_vol_cust h ON p.customer_id = h.customer_id
  GROUP BY p.revenue_month_start
)
SELECT 
  m.revenue_month_start,
  ROUND(100.0 * m.hv_rev / NULLIF(m.total_rev, 0), 2) AS hv_rev_share,
  ROUND(100.0 * m.hv_gp / NULLIF(m.total_gp, 0), 2) AS hv_gp_share,
  f.business_health_score,
  f.collection_rate_percentage,
  f.gross_margin_percentage,
  f.total_revenue,
  f.outstanding_receivables,
  f.collection_risk_level
FROM monthly_seg m
JOIN quickbooks__financial_dashboard f 
  ON STRFTIME('%Y-%m', m.revenue_month_start) = STRFTIME('%Y-%m', f.dashboard_month)
ORDER BY m.revenue_month_start
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-092/attempt-01/sql/S48.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-092/attempt-01/sql/S48.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-092/attempt-01/results/S48.rows.jsonl)；完整：True；SHA256：`0efb735248d1d74fd1393d348fdedbdc198373fd2da64563f4c41ef846280f84`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "quickbooks__profitability_analysis", "kind": "base", "block": null, "base_tables": ["quickbooks__profitability_analysis"]}] | [] | ["customer_id"] |
| B2 | [{"alias": "cust_vol", "kind": "derived", "block": "B1", "base_tables": ["quickbooks__profitability_analysis"]}] | [] | [] |
| B3 | [{"alias": "ordered", "kind": "derived", "block": "B2", "base_tables": ["quickbooks__profitability_analysis"]}] | [] | [] |
| B4 | [{"alias": "p", "kind": "base", "block": null, "base_tables": ["quickbooks__profitability_analysis"]}, {"alias": "h", "kind": "derived", "block": "B3", "base_tables": ["quickbooks__profitability_analysis"]}] | [{"type": "LEFT", "right": "high_vol_cust AS h", "on": "p.customer_id = h.customer_id", "using": []}] | ["p.revenue_month_start"] |
| B5 | [{"alias": "m", "kind": "derived", "block": "B4", "base_tables": ["quickbooks__profitability_analysis"]}, {"alias": "f", "kind": "base", "block": null, "base_tables": ["quickbooks__financial_dashboard"]}] | [{"type": "INNER", "right": "quickbooks__financial_dashboard AS f", "on": "STRFTIME('%Y-%m', m.revenue_month_start) = STRFTIME('%Y-%m', f.dashboard_month)", "using": []}] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | AVG(customer_margin_volatility) | [{"table": "quickbooks__profitability_analysis", "column": "customer_margin_volatility"}] | [] | False |
| B4 | SUM(CASE WHEN NOT h.customer_id IS NULL THEN p.invoice_total ELSE 0 END) | [{"table": "quickbooks__profitability_analysis", "column": "invoice_total"}] | [{"table": "quickbooks__profitability_analysis", "column": "customer_id"}] | False |
| B4 | SUM(p.invoice_total) | [{"table": "quickbooks__profitability_analysis", "column": "invoice_total"}] | [] | False |
| B4 | SUM(CASE WHEN NOT h.customer_id IS NULL THEN p.gross_profit ELSE 0 END) | [{"table": "quickbooks__profitability_analysis", "column": "gross_profit"}] | [{"table": "quickbooks__profitability_analysis", "column": "customer_id"}] | False |
| B4 | SUM(p.gross_profit) | [{"table": "quickbooks__profitability_analysis", "column": "gross_profit"}] | [] | False |


## S49

类别 `data`；来源 `query_db`；调用 `a43d597639094f94a4e5a16333d98cee`；状态 `success`。

```sql
SELECT DISTINCT account_type FROM quickbooks__balance_sheet
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-092/attempt-01/sql/S49.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-092/attempt-01/sql/S49.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-092/attempt-01/results/S49.rows.jsonl)；完整：True；SHA256：`78cd759836d514afced8dd5b6ac5087b2e4e9278c8892c59ed5aa432dd1495e5`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "quickbooks__balance_sheet", "kind": "base", "block": null, "base_tables": ["quickbooks__balance_sheet"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |


## S50

类别 `data`；来源 `query_db`；调用 `eb8efdd99b6949bd953152ba53871f69`；状态 `success`。

```sql
SELECT account_type, account_sub_type, COUNT(*) AS n, SUM(amount) AS total_amount
FROM quickbooks__balance_sheet
WHERE account_type LIKE '%Receivable%' OR account_sub_type LIKE '%Receivable%' OR account_type LIKE '%Asset%'
GROUP BY account_type, account_sub_type
ORDER BY total_amount DESC
LIMIT 30
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-092/attempt-01/sql/S50.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-092/attempt-01/sql/S50.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-092/attempt-01/results/S50.rows.jsonl)；完整：True；SHA256：`a172d25917ac46cd1d93529677a429856dd3ca765c5ea7b985fd29f47513724f`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "quickbooks__balance_sheet", "kind": "base", "block": null, "base_tables": ["quickbooks__balance_sheet"]}] | [] | ["account_type", "account_sub_type"] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |
| B1 | SUM(amount) | [{"table": "quickbooks__balance_sheet", "column": "amount"}] | [] | False |


## S51

类别 `data`；来源 `query_db`；调用 `a3328884ef714c49b102fabe22a18019`；状态 `success`。

```sql
SELECT account_sub_type, COUNT(DISTINCT calendar_date) AS n_dates, 
       MIN(calendar_date) AS min_date, MAX(calendar_date) AS max_date,
       SUM(amount) AS total_amount,
       SUM(converted_amount) AS total_converted
FROM quickbooks__balance_sheet
WHERE account_type = 'Accounts Receivable'
GROUP BY account_sub_type
ORDER BY total_amount DESC
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-092/attempt-01/sql/S51.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-092/attempt-01/sql/S51.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-092/attempt-01/results/S51.rows.jsonl)；完整：True；SHA256：`13b4ae161cff7c5d9a2035e45255a53aceb4b9c99a8b43b43175b1bada163130`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "quickbooks__balance_sheet", "kind": "base", "block": null, "base_tables": ["quickbooks__balance_sheet"]}] | [] | ["account_sub_type"] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(DISTINCT calendar_date) | [{"table": "quickbooks__balance_sheet", "column": "calendar_date"}] | [] | False |
| B1 | MIN(calendar_date) | [{"table": "quickbooks__balance_sheet", "column": "calendar_date"}] | [] | False |
| B1 | MAX(calendar_date) | [{"table": "quickbooks__balance_sheet", "column": "calendar_date"}] | [] | False |
| B1 | SUM(amount) | [{"table": "quickbooks__balance_sheet", "column": "amount"}] | [] | False |
| B1 | SUM(converted_amount) | [{"table": "quickbooks__balance_sheet", "column": "converted_amount"}] | [] | False |


## S52

类别 `data`；来源 `query_db`；调用 `65836abfafd441ef901e542ef5d907c6`；状态 `success`。

```sql
SELECT calendar_date, account_sub_type, SUM(amount) AS amount
FROM quickbooks__balance_sheet
WHERE account_type = 'Accounts Receivable'
  AND calendar_date = (SELECT MAX(calendar_date) FROM quickbooks__balance_sheet WHERE account_type = 'Accounts Receivable')
GROUP BY calendar_date, account_sub_type
ORDER BY account_sub_type
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-092/attempt-01/sql/S52.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-092/attempt-01/sql/S52.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-092/attempt-01/results/S52.rows.jsonl)；完整：True；SHA256：`ba568428ef6cd44729d5d394a545efeccb3b155faf358f5307abb799df0f15d2`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "quickbooks__balance_sheet", "kind": "base", "block": null, "base_tables": ["quickbooks__balance_sheet"]}] | [] | [] |
| B2 | [{"alias": "quickbooks__balance_sheet", "kind": "base", "block": null, "base_tables": ["quickbooks__balance_sheet"]}] | [] | ["calendar_date", "account_sub_type"] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | MAX(calendar_date) | [{"table": "quickbooks__balance_sheet", "column": "calendar_date"}] | [] | False |
| B2 | SUM(amount) | [{"table": "quickbooks__balance_sheet", "column": "amount"}] | [] | False |


## S53

类别 `data`；来源 `query_db`；调用 `0a82123883e94610ab047d11a22d8d96`；状态 `success`。

```sql
-- Overall AR aging structure (all snapshots)
SELECT 
  account_sub_type,
  SUM(amount) AS total_amount,
  ROUND(100.0 * SUM(amount) / SUM(SUM(amount)) OVER (), 2) AS pct_of_total
FROM quickbooks__balance_sheet
WHERE account_type = 'Accounts Receivable'
GROUP BY account_sub_type
ORDER BY total_amount DESC
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-092/attempt-01/sql/S53.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-092/attempt-01/sql/S53.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-092/attempt-01/results/S53.rows.jsonl)；完整：True；SHA256：`e86287d8e13fe55ae1434c77c55d3566273ad9ed158aedf3826fee9f15a87986`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "quickbooks__balance_sheet", "kind": "base", "block": null, "base_tables": ["quickbooks__balance_sheet"]}] | [] | ["account_sub_type"] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | SUM(amount) | [{"table": "quickbooks__balance_sheet", "column": "amount"}] | [] | False |
| B1 | SUM(amount) | [{"table": "quickbooks__balance_sheet", "column": "amount"}] | [] | False |
| B1 | SUM(amount) | [{"table": "quickbooks__balance_sheet", "column": "amount"}] | [] | False |


## S54

类别 `data`；来源 `query_db`；调用 `9eff476ed68440eb81ea93cd34ad4114`；状态 `success`。

```sql
-- AR aging trend: past due ratio over time
SELECT 
  calendar_date,
  SUM(CASE WHEN account_sub_type = 'Current (0-30 days)' THEN amount ELSE 0 END) AS current_ar,
  SUM(CASE WHEN account_sub_type != 'Current (0-30 days)' THEN amount ELSE 0 END) AS past_due_ar,
  SUM(amount) AS total_ar,
  ROUND(100.0 * SUM(CASE WHEN account_sub_type != 'Current (0-30 days)' THEN amount ELSE 0 END) / NULLIF(SUM(amount),0), 2) AS past_due_pct
FROM quickbooks__balance_sheet
WHERE account_type = 'Accounts Receivable'
GROUP BY calendar_date
ORDER BY calendar_date
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-092/attempt-01/sql/S54.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-092/attempt-01/sql/S54.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-092/attempt-01/results/S54.rows.jsonl)；完整：True；SHA256：`7b7dd16161eb7522dae80adb780b206bba6724eddf859b75cff3c70490b6dbc9`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "quickbooks__balance_sheet", "kind": "base", "block": null, "base_tables": ["quickbooks__balance_sheet"]}] | [] | ["calendar_date"] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | SUM(CASE WHEN account_sub_type = 'Current (0-30 days)' THEN amount ELSE 0 END) | [{"table": "quickbooks__balance_sheet", "column": "amount"}] | [{"table": "quickbooks__balance_sheet", "column": "account_sub_type"}] | False |
| B1 | SUM(CASE WHEN account_sub_type <> 'Current (0-30 days)' THEN amount ELSE 0 END) | [{"table": "quickbooks__balance_sheet", "column": "amount"}] | [{"table": "quickbooks__balance_sheet", "column": "account_sub_type"}] | False |
| B1 | SUM(amount) | [{"table": "quickbooks__balance_sheet", "column": "amount"}] | [] | False |
| B1 | SUM(CASE WHEN account_sub_type <> 'Current (0-30 days)' THEN amount ELSE 0 END) | [{"table": "quickbooks__balance_sheet", "column": "amount"}] | [{"table": "quickbooks__balance_sheet", "column": "account_sub_type"}] | False |
| B1 | SUM(amount) | [{"table": "quickbooks__balance_sheet", "column": "amount"}] | [] | False |


## S55

类别 `data`；来源 `query_db`；调用 `6f500efbd27f4c1a83d86df28994a678`；状态 `success`。

```sql
-- High-vol customers' outstanding balance snapshot
WITH cust_vol AS (
  SELECT customer_id, AVG(customer_margin_volatility) AS vol
  FROM quickbooks__profitability_analysis
  GROUP BY customer_id
),
ordered AS (
  SELECT customer_id, vol,
    ROW_NUMBER() OVER (ORDER BY vol DESC) AS rn,
    COUNT(*) OVER () AS total
  FROM cust_vol
),
high_vol_cust AS (
  SELECT customer_id FROM ordered WHERE rn <= total * 0.25
)
SELECT 
  CASE WHEN h.customer_id IS NOT NULL THEN 'HighVol' ELSE 'Other' END AS grp,
  SUM(p.outstanding_balance) AS total_outstanding,
  SUM(p.invoice_total) AS total_invoice,
  SUM(p.collected_amount) AS total_collected,
  COUNT(*) AS n_invoices,
  COUNT(DISTINCT p.customer_id) AS n_customers
FROM quickbooks__profitability_analysis p
LEFT JOIN high_vol_cust h ON p.customer_id = h.customer_id
GROUP BY CASE WHEN h.customer_id IS NOT NULL THEN 'HighVol' ELSE 'Other' END
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-092/attempt-01/sql/S55.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-092/attempt-01/sql/S55.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-092/attempt-01/results/S55.rows.jsonl)；完整：True；SHA256：`45bb9056b5e4e261d627a19bf300eb5547bf89aed972df69c18093e076a0635d`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "quickbooks__profitability_analysis", "kind": "base", "block": null, "base_tables": ["quickbooks__profitability_analysis"]}] | [] | ["customer_id"] |
| B2 | [{"alias": "cust_vol", "kind": "derived", "block": "B1", "base_tables": ["quickbooks__profitability_analysis"]}] | [] | [] |
| B3 | [{"alias": "ordered", "kind": "derived", "block": "B2", "base_tables": ["quickbooks__profitability_analysis"]}] | [] | [] |
| B4 | [{"alias": "p", "kind": "base", "block": null, "base_tables": ["quickbooks__profitability_analysis"]}, {"alias": "h", "kind": "derived", "block": "B3", "base_tables": ["quickbooks__profitability_analysis"]}] | [{"type": "LEFT", "right": "high_vol_cust AS h", "on": "p.customer_id = h.customer_id", "using": []}] | ["CASE WHEN NOT h.customer_id IS NULL THEN 'HighVol' ELSE 'Other' END"] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | AVG(customer_margin_volatility) | [{"table": "quickbooks__profitability_analysis", "column": "customer_margin_volatility"}] | [] | False |
| B4 | SUM(p.outstanding_balance) | [{"table": "quickbooks__profitability_analysis", "column": "outstanding_balance"}] | [] | False |
| B4 | SUM(p.invoice_total) | [{"table": "quickbooks__profitability_analysis", "column": "invoice_total"}] | [] | False |
| B4 | SUM(p.collected_amount) | [{"table": "quickbooks__profitability_analysis", "column": "collected_amount"}] | [] | False |
| B4 | COUNT(*) | [] | [] | True |
| B4 | COUNT(DISTINCT p.customer_id) | [{"table": "quickbooks__profitability_analysis", "column": "customer_id"}] | [] | False |


## S56

类别 `data`；来源 `query_db`；调用 `e0f64a4829e940da89fe8e6a69a09057`；状态 `success`。

```sql
-- Outstanding balance by volatility segment
WITH cust_vol AS (
  SELECT customer_id, AVG(customer_margin_volatility) AS vol
  FROM quickbooks__profitability_analysis
  GROUP BY customer_id
),
ordered AS (
  SELECT customer_id, vol,
    ROW_NUMBER() OVER (ORDER BY vol DESC) AS rn,
    COUNT(*) OVER () AS total
  FROM cust_vol
),
seg AS (
  SELECT customer_id, vol,
    CASE WHEN rn <= total * 0.25 THEN 'HighVol'
         WHEN rn > total * 0.75 THEN 'LowVol'
         ELSE 'MidVol' END AS vol_segment
  FROM ordered
)
SELECT 
  s.vol_segment,
  SUM(p.outstanding_balance) AS total_outstanding,
  SUM(p.invoice_total) AS total_invoice,
  SUM(p.collected_amount) AS total_collected,
  ROUND(100.0 * SUM(p.outstanding_balance) / NULLIF(SUM(p.invoice_total), 0), 2) AS outstanding_ratio,
  COUNT(DISTINCT s.customer_id) AS n_customers
FROM seg s
JOIN quickbooks__profitability_analysis p ON s.customer_id = p.customer_id
GROUP BY s.vol_segment
ORDER BY s.vol_segment
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-092/attempt-01/sql/S56.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-092/attempt-01/sql/S56.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-092/attempt-01/results/S56.rows.jsonl)；完整：True；SHA256：`fa2989f362227e53a12d843954197d3351018c2edd2d427cd7960574836566bb`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "quickbooks__profitability_analysis", "kind": "base", "block": null, "base_tables": ["quickbooks__profitability_analysis"]}] | [] | ["customer_id"] |
| B2 | [{"alias": "cust_vol", "kind": "derived", "block": "B1", "base_tables": ["quickbooks__profitability_analysis"]}] | [] | [] |
| B3 | [{"alias": "ordered", "kind": "derived", "block": "B2", "base_tables": ["quickbooks__profitability_analysis"]}] | [] | [] |
| B4 | [{"alias": "s", "kind": "derived", "block": "B3", "base_tables": ["quickbooks__profitability_analysis"]}, {"alias": "p", "kind": "base", "block": null, "base_tables": ["quickbooks__profitability_analysis"]}] | [{"type": "INNER", "right": "quickbooks__profitability_analysis AS p", "on": "s.customer_id = p.customer_id", "using": []}] | ["s.vol_segment"] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | AVG(customer_margin_volatility) | [{"table": "quickbooks__profitability_analysis", "column": "customer_margin_volatility"}] | [] | False |
| B4 | SUM(p.outstanding_balance) | [{"table": "quickbooks__profitability_analysis", "column": "outstanding_balance"}] | [] | False |
| B4 | SUM(p.invoice_total) | [{"table": "quickbooks__profitability_analysis", "column": "invoice_total"}] | [] | False |
| B4 | SUM(p.collected_amount) | [{"table": "quickbooks__profitability_analysis", "column": "collected_amount"}] | [] | False |
| B4 | COUNT(DISTINCT s.customer_id) | [{"table": "quickbooks__profitability_analysis", "column": "customer_id"}] | [] | False |
| B4 | SUM(p.outstanding_balance) | [{"table": "quickbooks__profitability_analysis", "column": "outstanding_balance"}] | [] | False |
| B4 | SUM(p.invoice_total) | [{"table": "quickbooks__profitability_analysis", "column": "invoice_total"}] | [] | False |


## S57

类别 `data`；来源 `query_db`；调用 `9fc1f20e7a4a4da4bf92d5bff19b6662`；状态 `success`。

```sql
-- Multi-dimensional risk scoring model: compute components per customer
WITH cust_vol AS (
  SELECT customer_id, AVG(customer_margin_volatility) AS vol
  FROM quickbooks__profitability_analysis
  GROUP BY customer_id
),
vol_percentile AS (
  SELECT customer_id, vol,
    PERCENT_RANK() OVER (ORDER BY vol) AS vol_pct_rank
  FROM cust_vol
),
fin AS (
  SELECT customer_id,
    SUM(invoice_total) AS total_invoice,
    SUM(outstanding_balance) AS total_outstanding,
    SUM(collected_amount) AS total_collected,
    COUNT(*) AS n_invoices,
    AVG(invoice_gross_margin_pct) AS avg_margin_pct
  FROM quickbooks__profitability_analysis
  GROUP BY customer_id
),
scored AS (
  SELECT 
    v.customer_id,
    v.vol,
    v.vol_pct_rank,
    a.payment_behavior,
    a.rfm_segment,
    a.revenue_trend_correlation,
    a.business_stability_score,
    a.active_months_last_12,
    a.revenue_growth_rate_12m,
    f.total_outstanding,
    f.total_invoice,
    f.n_invoices,
    f.avg_margin_pct,
    -- Dimension scores (each normalized 0-100)
    (v.vol_pct_rank * 100) AS vol_score,
    CASE a.payment_behavior 
      WHEN 'Excellent' THEN 10
      WHEN 'Good' THEN 35
      WHEN 'Average' THEN 65
      WHEN 'Poor' THEN 90
    END AS payment_score,
    CASE a.rfm_segment
      WHEN 'Champions' THEN 10
      WHEN 'Loyal Customers' THEN 25
      WHEN 'Potential Loyalists' THEN 45
      WHEN 'New Customers' THEN 50
      WHEN 'Need Attention' THEN 75
      WHEN 'At Risk' THEN 95
    END AS rfm_score,
    CASE WHEN a.revenue_trend_correlation < 0 THEN 70 ELSE 30 END AS trend_score,
    (100 - a.business_stability_score) AS stability_score
  FROM vol_percentile v
  JOIN quickbooks__customer_analytics a ON v.customer_id = a.customer_id
  JOIN fin f ON v.customer_id = f.customer_id
)
SELECT 
  customer_id, vol, vol_pct_rank, payment_behavior, rfm_segment,
  ROUND(revenue_trend_correlation, 3) AS trend_corr,
  business_stability_score, active_months_last_12,
  ROUND(total_outstanding, 2) AS total_outstanding,
  ROUND(total_invoice, 2) AS total_invoice,
  ROUND(vol_score, 1) AS vol_score,
  payment_score, rfm_score, trend_score, stability_score
FROM scored
ORDER BY vol_pct_rank DESC
LIMIT 15
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-092/attempt-01/sql/S57.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-092/attempt-01/sql/S57.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-092/attempt-01/results/S57.rows.jsonl)；完整：True；SHA256：`270cb9ace1d339c182b189e7b38779a8e331713097ab323872d1608522733e15`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "quickbooks__profitability_analysis", "kind": "base", "block": null, "base_tables": ["quickbooks__profitability_analysis"]}] | [] | ["customer_id"] |
| B2 | [{"alias": "cust_vol", "kind": "derived", "block": "B1", "base_tables": ["quickbooks__profitability_analysis"]}] | [] | [] |
| B3 | [{"alias": "quickbooks__profitability_analysis", "kind": "base", "block": null, "base_tables": ["quickbooks__profitability_analysis"]}] | [] | ["customer_id"] |
| B4 | [{"alias": "v", "kind": "derived", "block": "B2", "base_tables": ["quickbooks__profitability_analysis"]}, {"alias": "a", "kind": "base", "block": null, "base_tables": ["quickbooks__customer_analytics"]}, {"alias": "f", "kind": "derived", "block": "B3", "base_tables": ["quickbooks__profitability_analysis"]}] | [{"type": "INNER", "right": "quickbooks__customer_analytics AS a", "on": "v.customer_id = a.customer_id", "using": []}, {"type": "INNER", "right": "fin AS f", "on": "v.customer_id = f.customer_id", "using": []}] | [] |
| B5 | [{"alias": "scored", "kind": "derived", "block": "B4", "base_tables": ["quickbooks__customer_analytics", "quickbooks__profitability_analysis"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | AVG(customer_margin_volatility) | [{"table": "quickbooks__profitability_analysis", "column": "customer_margin_volatility"}] | [] | False |
| B3 | SUM(invoice_total) | [{"table": "quickbooks__profitability_analysis", "column": "invoice_total"}] | [] | False |
| B3 | SUM(outstanding_balance) | [{"table": "quickbooks__profitability_analysis", "column": "outstanding_balance"}] | [] | False |
| B3 | SUM(collected_amount) | [{"table": "quickbooks__profitability_analysis", "column": "collected_amount"}] | [] | False |
| B3 | COUNT(*) | [] | [] | True |
| B3 | AVG(invoice_gross_margin_pct) | [{"table": "quickbooks__profitability_analysis", "column": "invoice_gross_margin_pct"}] | [] | False |


## S58

类别 `data`；来源 `query_db`；调用 `bbcb916a8e9145c6bed3606a2bc7e3cf`；状态 `success`。

```sql
-- Compute composite risk score for all customers
WITH cust_vol AS (
  SELECT customer_id, AVG(customer_margin_volatility) AS vol
  FROM quickbooks__profitability_analysis
  GROUP BY customer_id
),
vol_percentile AS (
  SELECT customer_id, vol,
    PERCENT_RANK() OVER (ORDER BY vol) AS vol_pct_rank
  FROM cust_vol
),
scored AS (
  SELECT 
    v.customer_id,
    v.vol,
    v.vol_pct_rank,
    a.payment_behavior,
    a.rfm_segment,
    a.revenue_trend_correlation,
    a.business_stability_score,
    a.active_months_last_12,
    a.revenue_growth_rate_12m,
    -- Dimension scores (each 0-100)
    (v.vol_pct_rank * 100) AS vol_score,
    CASE a.payment_behavior 
      WHEN 'Excellent' THEN 10
      WHEN 'Good' THEN 35
      WHEN 'Average' THEN 65
      WHEN 'Poor' THEN 90
    END AS payment_score,
    CASE a.rfm_segment
      WHEN 'Champions' THEN 10
      WHEN 'Loyal Customers' THEN 25
      WHEN 'Potential Loyalists' THEN 45
      WHEN 'New Customers' THEN 50
      WHEN 'Need Attention' THEN 75
      WHEN 'At Risk' THEN 95
    END AS rfm_score,
    CASE WHEN a.revenue_trend_correlation < 0 THEN 70 ELSE 30 END AS trend_score,
    (100.0 - a.business_stability_score) AS stability_score
  FROM vol_percentile v
  JOIN quickbooks__customer_analytics a ON v.customer_id = a.customer_id
)
SELECT 
  customer_id,
  vol_score, payment_score, rfm_score, trend_score, stability_score,
  ROUND(0.25 * vol_score + 0.20 * payment_score + 0.20 * rfm_score + 0.15 * trend_score + 0.20 * stability_score, 1) AS composite_risk,
  ROUND(vol, 4) AS margin_volatility,
  payment_behavior,
  rfm_segment,
  business_stability_score
FROM scored
ORDER BY composite_risk DESC
LIMIT 20
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-092/attempt-01/sql/S58.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-092/attempt-01/sql/S58.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-092/attempt-01/results/S58.rows.jsonl)；完整：True；SHA256：`15b14dbdf329a4355be17d99490b05f3b1772e86410edffab81f7b93680bab62`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "quickbooks__profitability_analysis", "kind": "base", "block": null, "base_tables": ["quickbooks__profitability_analysis"]}] | [] | ["customer_id"] |
| B2 | [{"alias": "cust_vol", "kind": "derived", "block": "B1", "base_tables": ["quickbooks__profitability_analysis"]}] | [] | [] |
| B3 | [{"alias": "v", "kind": "derived", "block": "B2", "base_tables": ["quickbooks__profitability_analysis"]}, {"alias": "a", "kind": "base", "block": null, "base_tables": ["quickbooks__customer_analytics"]}] | [{"type": "INNER", "right": "quickbooks__customer_analytics AS a", "on": "v.customer_id = a.customer_id", "using": []}] | [] |
| B4 | [{"alias": "scored", "kind": "derived", "block": "B3", "base_tables": ["quickbooks__customer_analytics", "quickbooks__profitability_analysis"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | AVG(customer_margin_volatility) | [{"table": "quickbooks__profitability_analysis", "column": "customer_margin_volatility"}] | [] | False |


## S59

类别 `data`；来源 `query_db`；调用 `baa82cc52dd9465f8f44b67fb2572050`；状态 `success`。

```sql
-- Compute composite risk tiers for all customers
WITH cust_vol AS (
  SELECT customer_id, AVG(customer_margin_volatility) AS vol
  FROM quickbooks__profitability_analysis
  GROUP BY customer_id
),
vol_percentile AS (
  SELECT customer_id, vol,
    PERCENT_RANK() OVER (ORDER BY vol) AS vol_pct_rank
  FROM cust_vol
),
scored AS (
  SELECT 
    v.customer_id,
    (v.vol_pct_rank * 100) AS vol_score,
    CASE a.payment_behavior 
      WHEN 'Excellent' THEN 10
      WHEN 'Good' THEN 35
      WHEN 'Average' THEN 65
      WHEN 'Poor' THEN 90
    END AS payment_score,
    CASE a.rfm_segment
      WHEN 'Champions' THEN 10
      WHEN 'Loyal Customers' THEN 25
      WHEN 'Potential Loyalists' THEN 45
      WHEN 'New Customers' THEN 50
      WHEN 'Need Attention' THEN 75
      WHEN 'At Risk' THEN 95
    END AS rfm_score,
    CASE WHEN a.revenue_trend_correlation < 0 THEN 70 ELSE 30 END AS trend_score,
    (100.0 - a.business_stability_score) AS stability_score,
    a.payment_behavior,
    a.rfm_segment,
    a.business_stability_score,
    a.revenue_trend_correlation
  FROM vol_percentile v
  JOIN quickbooks__customer_analytics a ON v.customer_id = a.customer_id
),
risk_rated AS (
  SELECT 
    customer_id,
    ROUND(0.25 * vol_score + 0.20 * payment_score + 0.20 * rfm_score + 0.15 * trend_score + 0.20 * stability_score, 1) AS composite_risk,
    vol_score, payment_score, rfm_score, trend_score, stability_score,
    CASE 
      WHEN 0.25 * vol_score + 0.20 * payment_score + 0.20 * rfm_score + 0.15 * trend_score + 0.20 * stability_score >= 70 THEN 'High Risk'
      WHEN 0.25 * vol_score + 0.20 * payment_score + 0.20 * rfm_score + 0.15 * trend_score + 0.20 * stability_score >= 45 THEN 'Medium Risk'
      ELSE 'Low Risk'
    END AS risk_tier,
    payment_behavior, rfm_segment
  FROM scored
)
-- Risk tier distribution
SELECT 
  risk_tier,
  COUNT(*) AS n_customers,
  ROUND(100.0 * COUNT(*) / 2800, 1) AS pct,
  ROUND(AVG(composite_risk), 1) AS avg_risk_score
FROM risk_rated
GROUP BY risk_tier
ORDER BY avg_risk_score DESC
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-092/attempt-01/sql/S59.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-092/attempt-01/sql/S59.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-092/attempt-01/results/S59.rows.jsonl)；完整：True；SHA256：`5e3f3f7bd4da436b3ec7a8654a857ae8646e6de414c235bec499e70fa37dbc9d`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "quickbooks__profitability_analysis", "kind": "base", "block": null, "base_tables": ["quickbooks__profitability_analysis"]}] | [] | ["customer_id"] |
| B2 | [{"alias": "cust_vol", "kind": "derived", "block": "B1", "base_tables": ["quickbooks__profitability_analysis"]}] | [] | [] |
| B3 | [{"alias": "v", "kind": "derived", "block": "B2", "base_tables": ["quickbooks__profitability_analysis"]}, {"alias": "a", "kind": "base", "block": null, "base_tables": ["quickbooks__customer_analytics"]}] | [{"type": "INNER", "right": "quickbooks__customer_analytics AS a", "on": "v.customer_id = a.customer_id", "using": []}] | [] |
| B4 | [{"alias": "scored", "kind": "derived", "block": "B3", "base_tables": ["quickbooks__customer_analytics", "quickbooks__profitability_analysis"]}] | [] | [] |
| B5 | [{"alias": "risk_rated", "kind": "derived", "block": "B4", "base_tables": ["quickbooks__customer_analytics", "quickbooks__profitability_analysis"]}] | [] | ["risk_tier"] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | AVG(customer_margin_volatility) | [{"table": "quickbooks__profitability_analysis", "column": "customer_margin_volatility"}] | [] | False |
| B5 | COUNT(*) | [] | [] | True |
| B5 | AVG(composite_risk) | [{"table": "quickbooks__customer_analytics", "column": "business_stability_score"}, {"table": "quickbooks__customer_analytics", "column": "revenue_trend_correlation"}, {"table": "quickbooks__customer_analytics", "column": "rfm_segment"}, {"table": "quickbooks__profitability_analysis", "column": "customer_margin_volatility"}, {"table": "quickbooks__customer_analytics", "column": "payment_behavior"}] | [] | False |
| B5 | COUNT(*) | [] | [] | True |


## S60

类别 `data`；来源 `query_db`；调用 `f08763ed0d6f4b81b4306969efa9f883`；状态 `success`。

```sql
-- Cross-tab: volatility segment vs risk tier
WITH cust_vol AS (
  SELECT customer_id, AVG(customer_margin_volatility) AS vol
  FROM quickbooks__profitability_analysis
  GROUP BY customer_id
),
ordered AS (
  SELECT customer_id, vol,
    ROW_NUMBER() OVER (ORDER BY vol DESC) AS rn,
    COUNT(*) OVER () AS total
  FROM cust_vol
),
seg AS (
  SELECT customer_id, vol,
    CASE WHEN rn <= total * 0.25 THEN 'HighVol'
         WHEN rn > total * 0.75 THEN 'LowVol'
         ELSE 'MidVol' END AS vol_segment
  FROM ordered
),
vol_percentile AS (
  SELECT customer_id, vol,
    PERCENT_RANK() OVER (ORDER BY vol) AS vol_pct_rank
  FROM cust_vol
),
scored AS (
  SELECT 
    v.customer_id,
    (v.vol_pct_rank * 100) AS vol_score,
    CASE a.payment_behavior 
      WHEN 'Excellent' THEN 10
      WHEN 'Good' THEN 35
      WHEN 'Average' THEN 65
      WHEN 'Poor' THEN 90
    END AS payment_score,
    CASE a.rfm_segment
      WHEN 'Champions' THEN 10
      WHEN 'Loyal Customers' THEN 25
      WHEN 'Potential Loyalists' THEN 45
      WHEN 'New Customers' THEN 50
      WHEN 'Need Attention' THEN 75
      WHEN 'At Risk' THEN 95
    END AS rfm_score,
    CASE WHEN a.revenue_trend_correlation < 0 THEN 70 ELSE 30 END AS trend_score,
    (100.0 - a.business_stability_score) AS stability_score
  FROM vol_percentile v
  JOIN quickbooks__customer_analytics a ON v.customer_id = a.customer_id
),
risk_rated AS (
  SELECT 
    customer_id,
    CASE 
      WHEN 0.25 * vol_score + 0.20 * payment_score + 0.20 * rfm_score + 0.15 * trend_score + 0.20 * stability_score >= 70 THEN 'High Risk'
      WHEN 0.25 * vol_score + 0.20 * payment_score + 0.20 * rfm_score + 0.15 * trend_score + 0.20 * stability_score >= 45 THEN 'Medium Risk'
      ELSE 'Low Risk'
    END AS risk_tier
  FROM scored
)
SELECT 
  s.vol_segment,
  r.risk_tier,
  COUNT(*) AS n_customers,
  ROUND(100.0 * COUNT(*) / SUM(COUNT(*)) OVER (PARTITION BY s.vol_segment), 1) AS pct_of_segment
FROM seg s
JOIN risk_rated r ON s.customer_id = r.customer_id
GROUP BY s.vol_segment, r.risk_tier
ORDER BY s.vol_segment, r.risk_tier
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-092/attempt-01/sql/S60.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-092/attempt-01/sql/S60.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-092/attempt-01/results/S60.rows.jsonl)；完整：True；SHA256：`3ad652d37c2b66bb8cdc630247a131475b19bcd24a4aaa99c8986cae2f5f3d13`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "quickbooks__profitability_analysis", "kind": "base", "block": null, "base_tables": ["quickbooks__profitability_analysis"]}] | [] | ["customer_id"] |
| B2 | [{"alias": "cust_vol", "kind": "derived", "block": "B1", "base_tables": ["quickbooks__profitability_analysis"]}] | [] | [] |
| B3 | [{"alias": "ordered", "kind": "derived", "block": "B2", "base_tables": ["quickbooks__profitability_analysis"]}] | [] | [] |
| B4 | [{"alias": "cust_vol", "kind": "derived", "block": "B1", "base_tables": ["quickbooks__profitability_analysis"]}] | [] | [] |
| B5 | [{"alias": "v", "kind": "derived", "block": "B4", "base_tables": ["quickbooks__profitability_analysis"]}, {"alias": "a", "kind": "base", "block": null, "base_tables": ["quickbooks__customer_analytics"]}] | [{"type": "INNER", "right": "quickbooks__customer_analytics AS a", "on": "v.customer_id = a.customer_id", "using": []}] | [] |
| B6 | [{"alias": "scored", "kind": "derived", "block": "B5", "base_tables": ["quickbooks__customer_analytics", "quickbooks__profitability_analysis"]}] | [] | [] |
| B7 | [{"alias": "s", "kind": "derived", "block": "B3", "base_tables": ["quickbooks__profitability_analysis"]}, {"alias": "r", "kind": "derived", "block": "B6", "base_tables": ["quickbooks__customer_analytics", "quickbooks__profitability_analysis"]}] | [{"type": "INNER", "right": "risk_rated AS r", "on": "s.customer_id = r.customer_id", "using": []}] | ["s.vol_segment", "r.risk_tier"] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | AVG(customer_margin_volatility) | [{"table": "quickbooks__profitability_analysis", "column": "customer_margin_volatility"}] | [] | False |
| B7 | COUNT(*) | [] | [] | True |
| B7 | COUNT(*) | [] | [] | True |
| B7 | COUNT(*) | [] | [] | True |


## S61

类别 `data`；来源 `query_db`；调用 `9bd90a85134042b88d15b58151ed335c`；状态 `success`。

```sql
-- QoQ growth variance for LOW-vol customers (comparison)
WITH date_range AS (
  SELECT DATE(MAX(transaction_date), '-12 months') AS cutoff_date
  FROM quickbooks__profitability_analysis
),
cust_vol AS (
  SELECT customer_id, AVG(customer_margin_volatility) AS vol
  FROM quickbooks__profitability_analysis
  GROUP BY customer_id
),
ordered AS (
  SELECT customer_id, vol,
    ROW_NUMBER() OVER (ORDER BY vol ASC) AS rn,
    COUNT(*) OVER () AS total
  FROM cust_vol
),
low_vol_cust AS (
  SELECT customer_id, vol
  FROM ordered
  WHERE rn <= total * 0.25
),
quarterly AS (
  SELECT 
    h.customer_id,
    STRFTIME('%Y', p.transaction_date) AS yr,
    CAST((CAST(STRFTIME('%m', p.transaction_date) AS INTEGER) + 2) / 3 AS INTEGER) AS qtr,
    SUM(p.invoice_total) AS qtr_invoice_total
  FROM low_vol_cust h
  JOIN quickbooks__profitability_analysis p ON h.customer_id = p.customer_id
    AND p.transaction_date >= (SELECT cutoff_date FROM date_range)
  GROUP BY h.customer_id, STRFTIME('%Y', p.transaction_date), CAST((CAST(STRFTIME('%m', p.transaction_date) AS INTEGER) + 2) / 3 AS INTEGER)
),
qoqs AS (
  SELECT 
    customer_id, yr, qtr, qtr_invoice_total,
    LAG(qtr_invoice_total) OVER (PARTITION BY customer_id ORDER BY yr, qtr) AS prev_qtr_total
  FROM quarterly
)
SELECT 
  AVG(qoq_growth) AS mean_qoq_growth,
  AVG(qoq_growth * qoq_growth) - AVG(qoq_growth) * AVG(qoq_growth) AS var_qoq_growth,
  SQRT(AVG(qoq_growth * qoq_growth) - AVG(qoq_growth) * AVG(qoq_growth)) AS std_qoq_growth,
  COUNT(*) AS n_obs
FROM (
  SELECT 
    CASE WHEN prev_qtr_total IS NOT NULL AND prev_qtr_total <> 0 
         THEN (qtr_invoice_total - prev_qtr_total) / prev_qtr_total ELSE NULL END AS qoq_growth
  FROM qoqs
  WHERE prev_qtr_total IS NOT NULL
) WHERE qoq_growth IS NOT NULL
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-092/attempt-01/sql/S61.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-092/attempt-01/sql/S61.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-092/attempt-01/results/S61.rows.jsonl)；完整：True；SHA256：`afa839cd097db4e4841d83690307f80141ad232c42552e618e4027aa8e53e1fc`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "quickbooks__profitability_analysis", "kind": "base", "block": null, "base_tables": ["quickbooks__profitability_analysis"]}] | [] | [] |
| B2 | [{"alias": "quickbooks__profitability_analysis", "kind": "base", "block": null, "base_tables": ["quickbooks__profitability_analysis"]}] | [] | ["customer_id"] |
| B3 | [{"alias": "cust_vol", "kind": "derived", "block": "B2", "base_tables": ["quickbooks__profitability_analysis"]}] | [] | [] |
| B4 | [{"alias": "ordered", "kind": "derived", "block": "B3", "base_tables": ["quickbooks__profitability_analysis"]}] | [] | [] |
| B5 | [{"alias": "date_range", "kind": "derived", "block": "B1", "base_tables": ["quickbooks__profitability_analysis"]}] | [] | [] |
| B6 | [{"alias": "h", "kind": "derived", "block": "B4", "base_tables": ["quickbooks__profitability_analysis"]}, {"alias": "p", "kind": "base", "block": null, "base_tables": ["quickbooks__profitability_analysis"]}] | [{"type": "INNER", "right": "quickbooks__profitability_analysis AS p", "on": "h.customer_id = p.customer_id AND p.transaction_date >= (SELECT cutoff_date FROM date_range)", "using": []}] | ["h.customer_id", "STRFTIME('%Y', p.transaction_date)", "CAST((CAST(STRFTIME('%m', p.transaction_date) AS INTEGER) + 2) / 3 AS INTEGER)"] |
| B7 | [{"alias": "quarterly", "kind": "derived", "block": "B6", "base_tables": ["quickbooks__profitability_analysis"]}] | [] | [] |
| B8 | [{"alias": "qoqs", "kind": "derived", "block": "B7", "base_tables": ["quickbooks__profitability_analysis"]}] | [] | [] |
| B9 | [{"alias": "", "kind": "derived", "block": "B8", "base_tables": ["quickbooks__profitability_analysis"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | MAX(transaction_date) | [{"table": "quickbooks__profitability_analysis", "column": "transaction_date"}] | [] | False |
| B2 | AVG(customer_margin_volatility) | [{"table": "quickbooks__profitability_analysis", "column": "customer_margin_volatility"}] | [] | False |
| B6 | SUM(p.invoice_total) | [{"table": "quickbooks__profitability_analysis", "column": "invoice_total"}] | [] | False |
| B9 | AVG(qoq_growth) | [{"table": "quickbooks__profitability_analysis", "column": "customer_id"}, {"table": "quickbooks__profitability_analysis", "column": "invoice_total"}, {"table": "quickbooks__profitability_analysis", "column": "transaction_date"}, {"table": "quickbooks__profitability_analysis", "column": "transaction_date"}, {"table": "quickbooks__profitability_analysis", "column": "customer_id"}, {"table": "quickbooks__profitability_analysis", "column": "invoice_total"}, {"table": "quickbooks__profitability_analysis", "column": "transaction_date"}, {"table": "quickbooks__profitability_analysis", "column": "transaction_date"}, {"table": "quickbooks__profitability_analysis", "column": "customer_id"}, {"table": "quickbooks__profitability_analysis", "column": "invoice_total"}, {"table": "quickbooks__profitability_analysis", "column": "transaction_date"}, {"table": "quickbooks__profitability_analysis", "column": "transaction_date"}, {"table": "quickbooks__profitability_analysis", "column": "invoice_total"}, {"table": "quickbooks__profitability_analysis", "column": "customer_id"}, {"table": "quickbooks__profitability_analysis", "column": "invoice_total"}, {"table": "quickbooks__profitability_analysis", "column": "transaction_date"}, {"table": "quickbooks__profitability_analysis", "column": "transaction_date"}] | [] | False |
| B9 | COUNT(*) | [] | [] | True |
| B9 | AVG(qoq_growth * qoq_growth) | [{"table": "quickbooks__profitability_analysis", "column": "customer_id"}, {"table": "quickbooks__profitability_analysis", "column": "invoice_total"}, {"table": "quickbooks__profitability_analysis", "column": "transaction_date"}, {"table": "quickbooks__profitability_analysis", "column": "transaction_date"}, {"table": "quickbooks__profitability_analysis", "column": "customer_id"}, {"table": "quickbooks__profitability_analysis", "column": "invoice_total"}, {"table": "quickbooks__profitability_analysis", "column": "transaction_date"}, {"table": "quickbooks__profitability_analysis", "column": "transaction_date"}, {"table": "quickbooks__profitability_analysis", "column": "customer_id"}, {"table": "quickbooks__profitability_analysis", "column": "invoice_total"}, {"table": "quickbooks__profitability_analysis", "column": "transaction_date"}, {"table": "quickbooks__profitability_analysis", "column": "transaction_date"}, {"table": "quickbooks__profitability_analysis", "column": "invoice_total"}, {"table": "quickbooks__profitability_analysis", "column": "customer_id"}, {"table": "quickbooks__profitability_analysis", "column": "invoice_total"}, {"table": "quickbooks__profitability_analysis", "column": "transaction_date"}, {"table": "quickbooks__profitability_analysis", "column": "transaction_date"}, {"table": "quickbooks__profitability_analysis", "column": "customer_id"}, {"table": "quickbooks__profitability_analysis", "column": "invoice_total"}, {"table": "quickbooks__profitability_analysis", "column": "transaction_date"}, {"table": "quickbooks__profitability_analysis", "column": "transaction_date"}, {"table": "quickbooks__profitability_analysis", "column": "customer_id"}, {"table": "quickbooks__profitability_analysis", "column": "invoice_total"}, {"table": "quickbooks__profitability_analysis", "column": "transaction_date"}, {"table": "quickbooks__profitability_analysis", "column": "transaction_date"}, {"table": "quickbooks__profitability_analysis", "column": "customer_id"}, {"table": "quickbooks__profitability_analysis", "column": "invoice_total"}, {"table": "quickbooks__profitability_analysis", "column": "transaction_date"}, {"table": "quickbooks__profitability_analysis", "column": "transaction_date"}, {"table": "quickbooks__profitability_analysis", "column": "invoice_total"}, {"table": "quickbooks__profitability_analysis", "column": "customer_id"}, {"table": "quickbooks__profitability_analysis", "column": "invoice_total"}, {"table": "quickbooks__profitability_analysis", "column": "transaction_date"}, {"table": "quickbooks__profitability_analysis", "column": "transaction_date"}] | [] | False |
| B9 | AVG(qoq_growth) | [{"table": "quickbooks__profitability_analysis", "column": "customer_id"}, {"table": "quickbooks__profitability_analysis", "column": "invoice_total"}, {"table": "quickbooks__profitability_analysis", "column": "transaction_date"}, {"table": "quickbooks__profitability_analysis", "column": "transaction_date"}, {"table": "quickbooks__profitability_analysis", "column": "customer_id"}, {"table": "quickbooks__profitability_analysis", "column": "invoice_total"}, {"table": "quickbooks__profitability_analysis", "column": "transaction_date"}, {"table": "quickbooks__profitability_analysis", "column": "transaction_date"}, {"table": "quickbooks__profitability_analysis", "column": "customer_id"}, {"table": "quickbooks__profitability_analysis", "column": "invoice_total"}, {"table": "quickbooks__profitability_analysis", "column": "transaction_date"}, {"table": "quickbooks__profitability_analysis", "column": "transaction_date"}, {"table": "quickbooks__profitability_analysis", "column": "invoice_total"}, {"table": "quickbooks__profitability_analysis", "column": "customer_id"}, {"table": "quickbooks__profitability_analysis", "column": "invoice_total"}, {"table": "quickbooks__profitability_analysis", "column": "transaction_date"}, {"table": "quickbooks__profitability_analysis", "column": "transaction_date"}] | [] | False |
| B9 | AVG(qoq_growth) | [{"table": "quickbooks__profitability_analysis", "column": "customer_id"}, {"table": "quickbooks__profitability_analysis", "column": "invoice_total"}, {"table": "quickbooks__profitability_analysis", "column": "transaction_date"}, {"table": "quickbooks__profitability_analysis", "column": "transaction_date"}, {"table": "quickbooks__profitability_analysis", "column": "customer_id"}, {"table": "quickbooks__profitability_analysis", "column": "invoice_total"}, {"table": "quickbooks__profitability_analysis", "column": "transaction_date"}, {"table": "quickbooks__profitability_analysis", "column": "transaction_date"}, {"table": "quickbooks__profitability_analysis", "column": "customer_id"}, {"table": "quickbooks__profitability_analysis", "column": "invoice_total"}, {"table": "quickbooks__profitability_analysis", "column": "transaction_date"}, {"table": "quickbooks__profitability_analysis", "column": "transaction_date"}, {"table": "quickbooks__profitability_analysis", "column": "invoice_total"}, {"table": "quickbooks__profitability_analysis", "column": "customer_id"}, {"table": "quickbooks__profitability_analysis", "column": "invoice_total"}, {"table": "quickbooks__profitability_analysis", "column": "transaction_date"}, {"table": "quickbooks__profitability_analysis", "column": "transaction_date"}] | [] | False |
| B9 | AVG(qoq_growth * qoq_growth) | [{"table": "quickbooks__profitability_analysis", "column": "customer_id"}, {"table": "quickbooks__profitability_analysis", "column": "invoice_total"}, {"table": "quickbooks__profitability_analysis", "column": "transaction_date"}, {"table": "quickbooks__profitability_analysis", "column": "transaction_date"}, {"table": "quickbooks__profitability_analysis", "column": "customer_id"}, {"table": "quickbooks__profitability_analysis", "column": "invoice_total"}, {"table": "quickbooks__profitability_analysis", "column": "transaction_date"}, {"table": "quickbooks__profitability_analysis", "column": "transaction_date"}, {"table": "quickbooks__profitability_analysis", "column": "customer_id"}, {"table": "quickbooks__profitability_analysis", "column": "invoice_total"}, {"table": "quickbooks__profitability_analysis", "column": "transaction_date"}, {"table": "quickbooks__profitability_analysis", "column": "transaction_date"}, {"table": "quickbooks__profitability_analysis", "column": "invoice_total"}, {"table": "quickbooks__profitability_analysis", "column": "customer_id"}, {"table": "quickbooks__profitability_analysis", "column": "invoice_total"}, {"table": "quickbooks__profitability_analysis", "column": "transaction_date"}, {"table": "quickbooks__profitability_analysis", "column": "transaction_date"}, {"table": "quickbooks__profitability_analysis", "column": "customer_id"}, {"table": "quickbooks__profitability_analysis", "column": "invoice_total"}, {"table": "quickbooks__profitability_analysis", "column": "transaction_date"}, {"table": "quickbooks__profitability_analysis", "column": "transaction_date"}, {"table": "quickbooks__profitability_analysis", "column": "customer_id"}, {"table": "quickbooks__profitability_analysis", "column": "invoice_total"}, {"table": "quickbooks__profitability_analysis", "column": "transaction_date"}, {"table": "quickbooks__profitability_analysis", "column": "transaction_date"}, {"table": "quickbooks__profitability_analysis", "column": "customer_id"}, {"table": "quickbooks__profitability_analysis", "column": "invoice_total"}, {"table": "quickbooks__profitability_analysis", "column": "transaction_date"}, {"table": "quickbooks__profitability_analysis", "column": "transaction_date"}, {"table": "quickbooks__profitability_analysis", "column": "invoice_total"}, {"table": "quickbooks__profitability_analysis", "column": "customer_id"}, {"table": "quickbooks__profitability_analysis", "column": "invoice_total"}, {"table": "quickbooks__profitability_analysis", "column": "transaction_date"}, {"table": "quickbooks__profitability_analysis", "column": "transaction_date"}] | [] | False |
| B9 | AVG(qoq_growth) | [{"table": "quickbooks__profitability_analysis", "column": "customer_id"}, {"table": "quickbooks__profitability_analysis", "column": "invoice_total"}, {"table": "quickbooks__profitability_analysis", "column": "transaction_date"}, {"table": "quickbooks__profitability_analysis", "column": "transaction_date"}, {"table": "quickbooks__profitability_analysis", "column": "customer_id"}, {"table": "quickbooks__profitability_analysis", "column": "invoice_total"}, {"table": "quickbooks__profitability_analysis", "column": "transaction_date"}, {"table": "quickbooks__profitability_analysis", "column": "transaction_date"}, {"table": "quickbooks__profitability_analysis", "column": "customer_id"}, {"table": "quickbooks__profitability_analysis", "column": "invoice_total"}, {"table": "quickbooks__profitability_analysis", "column": "transaction_date"}, {"table": "quickbooks__profitability_analysis", "column": "transaction_date"}, {"table": "quickbooks__profitability_analysis", "column": "invoice_total"}, {"table": "quickbooks__profitability_analysis", "column": "customer_id"}, {"table": "quickbooks__profitability_analysis", "column": "invoice_total"}, {"table": "quickbooks__profitability_analysis", "column": "transaction_date"}, {"table": "quickbooks__profitability_analysis", "column": "transaction_date"}] | [] | False |
| B9 | AVG(qoq_growth) | [{"table": "quickbooks__profitability_analysis", "column": "customer_id"}, {"table": "quickbooks__profitability_analysis", "column": "invoice_total"}, {"table": "quickbooks__profitability_analysis", "column": "transaction_date"}, {"table": "quickbooks__profitability_analysis", "column": "transaction_date"}, {"table": "quickbooks__profitability_analysis", "column": "customer_id"}, {"table": "quickbooks__profitability_analysis", "column": "invoice_total"}, {"table": "quickbooks__profitability_analysis", "column": "transaction_date"}, {"table": "quickbooks__profitability_analysis", "column": "transaction_date"}, {"table": "quickbooks__profitability_analysis", "column": "customer_id"}, {"table": "quickbooks__profitability_analysis", "column": "invoice_total"}, {"table": "quickbooks__profitability_analysis", "column": "transaction_date"}, {"table": "quickbooks__profitability_analysis", "column": "transaction_date"}, {"table": "quickbooks__profitability_analysis", "column": "invoice_total"}, {"table": "quickbooks__profitability_analysis", "column": "customer_id"}, {"table": "quickbooks__profitability_analysis", "column": "invoice_total"}, {"table": "quickbooks__profitability_analysis", "column": "transaction_date"}, {"table": "quickbooks__profitability_analysis", "column": "transaction_date"}] | [] | False |


未解析列血缘：[{"block": "B9", "column": "cutoff_date", "reason": "ambiguous_or_missing_source"}]

## S62

类别 `data`；来源 `query_db`；调用 `d327934185f94aeb98ca7af9b3f753b9`；状态 `success`。

```sql
-- Overall CV of monthly gross profit for LOW-vol customers
WITH date_range AS (
  SELECT DATE(MAX(transaction_date), '-12 months') AS cutoff_date
  FROM quickbooks__profitability_analysis
),
cust_vol AS (
  SELECT customer_id, AVG(customer_margin_volatility) AS vol
  FROM quickbooks__profitability_analysis
  GROUP BY customer_id
),
ordered AS (
  SELECT customer_id, vol,
    ROW_NUMBER() OVER (ORDER BY vol ASC) AS rn,
    COUNT(*) OVER () AS total
  FROM cust_vol
),
low_vol_cust AS (
  SELECT customer_id, vol
  FROM ordered
  WHERE rn <= total * 0.25
),
monthly AS (
  SELECT 
    h.customer_id,
    STRFTIME('%Y-%m', p.transaction_date) AS month,
    SUM(p.gross_profit) AS monthly_gp
  FROM low_vol_cust h
  JOIN quickbooks__profitability_analysis p ON h.customer_id = p.customer_id
    AND p.transaction_date >= (SELECT cutoff_date FROM date_range)
  GROUP BY h.customer_id, STRFTIME('%Y-%m', p.transaction_date)
)
SELECT 
  AVG(monthly_gp) AS overall_mean_gp,
  SQRT(AVG(monthly_gp * monthly_gp) - AVG(monthly_gp) * AVG(monthly_gp)) AS overall_std_gp,
  SQRT(AVG(monthly_gp * monthly_gp) - AVG(monthly_gp) * AVG(monthly_gp)) / ABS(AVG(monthly_gp)) AS overall_cv_gp,
  COUNT(*) AS total_month_obs,
  COUNT(DISTINCT customer_id) AS n_customers_with_data
FROM monthly
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-092/attempt-01/sql/S62.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-092/attempt-01/sql/S62.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-092/attempt-01/results/S62.rows.jsonl)；完整：True；SHA256：`9dbd1346d0956eefac7fd80d239fe54d886291878a3b7c5e9393d499df85b5c8`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "quickbooks__profitability_analysis", "kind": "base", "block": null, "base_tables": ["quickbooks__profitability_analysis"]}] | [] | [] |
| B2 | [{"alias": "quickbooks__profitability_analysis", "kind": "base", "block": null, "base_tables": ["quickbooks__profitability_analysis"]}] | [] | ["customer_id"] |
| B3 | [{"alias": "cust_vol", "kind": "derived", "block": "B2", "base_tables": ["quickbooks__profitability_analysis"]}] | [] | [] |
| B4 | [{"alias": "ordered", "kind": "derived", "block": "B3", "base_tables": ["quickbooks__profitability_analysis"]}] | [] | [] |
| B5 | [{"alias": "date_range", "kind": "derived", "block": "B1", "base_tables": ["quickbooks__profitability_analysis"]}] | [] | [] |
| B6 | [{"alias": "h", "kind": "derived", "block": "B4", "base_tables": ["quickbooks__profitability_analysis"]}, {"alias": "p", "kind": "base", "block": null, "base_tables": ["quickbooks__profitability_analysis"]}] | [{"type": "INNER", "right": "quickbooks__profitability_analysis AS p", "on": "h.customer_id = p.customer_id AND p.transaction_date >= (SELECT cutoff_date FROM date_range)", "using": []}] | ["h.customer_id", "STRFTIME('%Y-%m', p.transaction_date)"] |
| B7 | [{"alias": "monthly", "kind": "derived", "block": "B6", "base_tables": ["quickbooks__profitability_analysis"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | MAX(transaction_date) | [{"table": "quickbooks__profitability_analysis", "column": "transaction_date"}] | [] | False |
| B2 | AVG(customer_margin_volatility) | [{"table": "quickbooks__profitability_analysis", "column": "customer_margin_volatility"}] | [] | False |
| B6 | SUM(p.gross_profit) | [{"table": "quickbooks__profitability_analysis", "column": "gross_profit"}] | [] | False |
| B7 | AVG(monthly_gp) | [{"table": "quickbooks__profitability_analysis", "column": "gross_profit"}] | [] | False |
| B7 | COUNT(*) | [] | [] | True |
| B7 | COUNT(DISTINCT customer_id) | [{"table": "quickbooks__profitability_analysis", "column": "customer_id"}] | [] | False |
| B7 | AVG(monthly_gp * monthly_gp) | [{"table": "quickbooks__profitability_analysis", "column": "gross_profit"}, {"table": "quickbooks__profitability_analysis", "column": "gross_profit"}] | [] | False |
| B7 | AVG(monthly_gp) | [{"table": "quickbooks__profitability_analysis", "column": "gross_profit"}] | [] | False |
| B7 | AVG(monthly_gp) | [{"table": "quickbooks__profitability_analysis", "column": "gross_profit"}] | [] | False |
| B7 | AVG(monthly_gp) | [{"table": "quickbooks__profitability_analysis", "column": "gross_profit"}] | [] | False |
| B7 | AVG(monthly_gp * monthly_gp) | [{"table": "quickbooks__profitability_analysis", "column": "gross_profit"}, {"table": "quickbooks__profitability_analysis", "column": "gross_profit"}] | [] | False |
| B7 | AVG(monthly_gp) | [{"table": "quickbooks__profitability_analysis", "column": "gross_profit"}] | [] | False |
| B7 | AVG(monthly_gp) | [{"table": "quickbooks__profitability_analysis", "column": "gross_profit"}] | [] | False |


未解析列血缘：[{"block": "B7", "column": "cutoff_date", "reason": "ambiguous_or_missing_source"}]

## S63

类别 `data`；来源 `python`；调用 `f8df93bf00e24b4a9d4ecf6b473f937a`；状态 `success`。

```sql

WITH cust_vol AS (
  SELECT customer_id, AVG(customer_margin_volatility) AS vol
  FROM quickbooks__profitability_analysis
  GROUP BY customer_id
),
ordered AS (
  SELECT customer_id, vol,
    ROW_NUMBER() OVER (ORDER BY vol DESC) AS rn,
    COUNT(*) OVER () AS total
  FROM cust_vol
)
SELECT customer_id, vol,
  CASE WHEN rn <= total * 0.25 THEN 'HighVol'
       WHEN rn > total * 0.75 THEN 'LowVol'
       ELSE 'MidVol' END AS vol_segment
FROM ordered

```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-092/attempt-01/sql/S63.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-092/attempt-01/sql/S63.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-092/attempt-01/results/S63.rows.jsonl)；完整：True；SHA256：`bc7b79601ee0daaf82a5f2b594c43d4898202b9de5c49f4684e299abdb365be7`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "quickbooks__profitability_analysis", "kind": "base", "block": null, "base_tables": ["quickbooks__profitability_analysis"]}] | [] | ["customer_id"] |
| B2 | [{"alias": "cust_vol", "kind": "derived", "block": "B1", "base_tables": ["quickbooks__profitability_analysis"]}] | [] | [] |
| B3 | [{"alias": "ordered", "kind": "derived", "block": "B2", "base_tables": ["quickbooks__profitability_analysis"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | AVG(customer_margin_volatility) | [{"table": "quickbooks__profitability_analysis", "column": "customer_margin_volatility"}] | [] | False |


## S64

类别 `data`；来源 `python`；调用 `f8df93bf00e24b4a9d4ecf6b473f937a`；状态 `success`。

```sql

WITH date_range AS (
  SELECT DATE(MAX(transaction_date), '-12 months') AS cutoff_date
  FROM quickbooks__profitability_analysis
)
SELECT customer_id, STRFTIME('%Y-%m', transaction_date) AS month, SUM(gross_profit) AS monthly_gp
FROM quickbooks__profitability_analysis
WHERE transaction_date >= (SELECT cutoff_date FROM date_range)
GROUP BY customer_id, STRFTIME('%Y-%m', transaction_date)

```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-092/attempt-01/sql/S64.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-092/attempt-01/sql/S64.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-092/attempt-01/results/S64.rows.jsonl)；完整：True；SHA256：`4e2d4fdaa0bd211297ff2500ba39a082f76fc67d6ea8af752ce32032dce289c6`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "quickbooks__profitability_analysis", "kind": "base", "block": null, "base_tables": ["quickbooks__profitability_analysis"]}] | [] | [] |
| B2 | [{"alias": "date_range", "kind": "derived", "block": "B1", "base_tables": ["quickbooks__profitability_analysis"]}] | [] | [] |
| B3 | [{"alias": "quickbooks__profitability_analysis", "kind": "base", "block": null, "base_tables": ["quickbooks__profitability_analysis"]}] | [] | ["customer_id", "STRFTIME('%Y-%m', transaction_date)"] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | MAX(transaction_date) | [{"table": "quickbooks__profitability_analysis", "column": "transaction_date"}] | [] | False |
| B3 | SUM(gross_profit) | [{"table": "quickbooks__profitability_analysis", "column": "gross_profit"}] | [] | False |


未解析列血缘：[{"block": "B3", "column": "cutoff_date", "reason": "ambiguous_or_missing_source"}]

## S65

类别 `data`；来源 `python`；调用 `f8df93bf00e24b4a9d4ecf6b473f937a`；状态 `success`。

```sql

SELECT s.vol_segment, a.customer_id, a.revenue_trend_correlation
FROM (
  WITH cust_vol AS (
    SELECT customer_id, AVG(customer_margin_volatility) AS vol
    FROM quickbooks__profitability_analysis
    GROUP BY customer_id
  ),
  ordered AS (
    SELECT customer_id, vol,
      ROW_NUMBER() OVER (ORDER BY vol DESC) AS rn,
      COUNT(*) OVER () AS total
    FROM cust_vol
  )
  SELECT customer_id, vol,
    CASE WHEN rn <= total * 0.25 THEN 'HighVol'
         WHEN rn > total * 0.75 THEN 'LowVol'
         ELSE 'MidVol' END AS vol_segment
  FROM ordered
) s
JOIN quickbooks__customer_analytics a ON s.customer_id = a.customer_id

```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-092/attempt-01/sql/S65.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-092/attempt-01/sql/S65.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-092/attempt-01/results/S65.rows.jsonl)；完整：True；SHA256：`53931f751c0fba88e79a0a065a3114a3d8af4374ff013cc934931a47a8946e6a`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "quickbooks__profitability_analysis", "kind": "base", "block": null, "base_tables": ["quickbooks__profitability_analysis"]}] | [] | ["customer_id"] |
| B2 | [{"alias": "cust_vol", "kind": "derived", "block": "B1", "base_tables": ["quickbooks__profitability_analysis"]}] | [] | [] |
| B3 | [{"alias": "ordered", "kind": "derived", "block": "B2", "base_tables": ["quickbooks__profitability_analysis"]}] | [] | [] |
| B4 | [{"alias": "s", "kind": "derived", "block": "B3", "base_tables": ["quickbooks__profitability_analysis"]}, {"alias": "a", "kind": "base", "block": null, "base_tables": ["quickbooks__customer_analytics"]}] | [{"type": "INNER", "right": "quickbooks__customer_analytics AS a", "on": "s.customer_id = a.customer_id", "using": []}] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | AVG(customer_margin_volatility) | [{"table": "quickbooks__profitability_analysis", "column": "customer_margin_volatility"}] | [] | False |


## S66

类别 `data`；来源 `query_db`；调用 `168b595f23a84d73b07b10942eaf18c8`；状态 `success`。

```sql
-- Profile high-risk tier customers: financial contribution
WITH cust_vol AS (
  SELECT customer_id, AVG(customer_margin_volatility) AS vol
  FROM quickbooks__profitability_analysis
  GROUP BY customer_id
),
vol_percentile AS (
  SELECT customer_id, vol, PERCENT_RANK() OVER (ORDER BY vol) AS vol_pct_rank
  FROM cust_vol
),
scored AS (
  SELECT 
    v.customer_id,
    (v.vol_pct_rank * 100) AS vol_score,
    CASE a.payment_behavior 
      WHEN 'Excellent' THEN 10 WHEN 'Good' THEN 35 WHEN 'Average' THEN 65 WHEN 'Poor' THEN 90
    END AS payment_score,
    CASE a.rfm_segment
      WHEN 'Champions' THEN 10 WHEN 'Loyal Customers' THEN 25 WHEN 'Potential Loyalists' THEN 45
      WHEN 'New Customers' THEN 50 WHEN 'Need Attention' THEN 75 WHEN 'At Risk' THEN 95
    END AS rfm_score,
    CASE WHEN a.revenue_trend_correlation < 0 THEN 70 ELSE 30 END AS trend_score,
    (100.0 - a.business_stability_score) AS stability_score
  FROM vol_percentile v
  JOIN quickbooks__customer_analytics a ON v.customer_id = a.customer_id
),
risk_rated AS (
  SELECT 
    customer_id,
    CASE 
      WHEN 0.25 * vol_score + 0.20 * payment_score + 0.20 * rfm_score + 0.15 * trend_score + 0.20 * stability_score >= 70 THEN 'High Risk'
      WHEN 0.25 * vol_score + 0.20 * payment_score + 0.20 * rfm_score + 0.15 * trend_score + 0.20 * stability_score >= 45 THEN 'Medium Risk'
      ELSE 'Low Risk'
    END AS risk_tier,
    (0.25 * vol_score + 0.20 * payment_score + 0.20 * rfm_score + 0.15 * trend_score + 0.20 * stability_score) AS composite_risk
  FROM scored
)
SELECT 
  r.risk_tier,
  COUNT(DISTINCT r.customer_id) AS n_customers,
  SUM(p.invoice_total) AS total_invoice,
  SUM(p.outstanding_balance) AS total_outstanding,
  SUM(p.gross_profit) AS total_gross_profit,
  ROUND(100.0 * SUM(p.outstanding_balance) / NULLIF((SELECT SUM(outstanding_balance) FROM quickbooks__profitability_analysis), 0), 2) AS outstanding_share_pct
FROM risk_rated r
JOIN quickbooks__profitability_analysis p ON r.customer_id = p.customer_id
GROUP BY r.risk_tier
ORDER BY r.risk_tier
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-092/attempt-01/sql/S66.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-092/attempt-01/sql/S66.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-092/attempt-01/results/S66.rows.jsonl)；完整：True；SHA256：`d53c00f408e5c85ab63ddab515584a6f3b2cd6a231bdfab500da433a868992bc`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "quickbooks__profitability_analysis", "kind": "base", "block": null, "base_tables": ["quickbooks__profitability_analysis"]}] | [] | ["customer_id"] |
| B2 | [{"alias": "cust_vol", "kind": "derived", "block": "B1", "base_tables": ["quickbooks__profitability_analysis"]}] | [] | [] |
| B3 | [{"alias": "v", "kind": "derived", "block": "B2", "base_tables": ["quickbooks__profitability_analysis"]}, {"alias": "a", "kind": "base", "block": null, "base_tables": ["quickbooks__customer_analytics"]}] | [{"type": "INNER", "right": "quickbooks__customer_analytics AS a", "on": "v.customer_id = a.customer_id", "using": []}] | [] |
| B4 | [{"alias": "scored", "kind": "derived", "block": "B3", "base_tables": ["quickbooks__customer_analytics", "quickbooks__profitability_analysis"]}] | [] | [] |
| B5 | [{"alias": "quickbooks__profitability_analysis", "kind": "base", "block": null, "base_tables": ["quickbooks__profitability_analysis"]}] | [] | [] |
| B6 | [{"alias": "r", "kind": "derived", "block": "B4", "base_tables": ["quickbooks__customer_analytics", "quickbooks__profitability_analysis"]}, {"alias": "p", "kind": "base", "block": null, "base_tables": ["quickbooks__profitability_analysis"]}] | [{"type": "INNER", "right": "quickbooks__profitability_analysis AS p", "on": "r.customer_id = p.customer_id", "using": []}] | ["r.risk_tier"] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | AVG(customer_margin_volatility) | [{"table": "quickbooks__profitability_analysis", "column": "customer_margin_volatility"}] | [] | False |
| B5 | SUM(outstanding_balance) | [{"table": "quickbooks__profitability_analysis", "column": "outstanding_balance"}] | [] | False |
| B6 | COUNT(DISTINCT r.customer_id) | [{"table": "quickbooks__profitability_analysis", "column": "customer_id"}] | [] | False |
| B6 | SUM(p.invoice_total) | [{"table": "quickbooks__profitability_analysis", "column": "invoice_total"}] | [] | False |
| B6 | SUM(p.outstanding_balance) | [{"table": "quickbooks__profitability_analysis", "column": "outstanding_balance"}] | [] | False |
| B6 | SUM(p.gross_profit) | [{"table": "quickbooks__profitability_analysis", "column": "gross_profit"}] | [] | False |
| B6 | SUM(p.outstanding_balance) | [{"table": "quickbooks__profitability_analysis", "column": "outstanding_balance"}] | [] | False |


## S67

类别 `data`；来源 `query_db`；调用 `92a6b5517a1e45f18c1c2c55de8ee020`；状态 `success`。

```sql
-- High-risk tier profile details
WITH cust_vol AS (
  SELECT customer_id, AVG(customer_margin_volatility) AS vol
  FROM quickbooks__profitability_analysis
  GROUP BY customer_id
),
vol_percentile AS (
  SELECT customer_id, vol, PERCENT_RANK() OVER (ORDER BY vol) AS vol_pct_rank
  FROM cust_vol
),
scored AS (
  SELECT 
    v.customer_id,
    v.vol,
    (v.vol_pct_rank * 100) AS vol_score,
    CASE a.payment_behavior 
      WHEN 'Excellent' THEN 10 WHEN 'Good' THEN 35 WHEN 'Average' THEN 65 WHEN 'Poor' THEN 90
    END AS payment_score,
    CASE a.rfm_segment
      WHEN 'Champions' THEN 10 WHEN 'Loyal Customers' THEN 25 WHEN 'Potential Loyalists' THEN 45
      WHEN 'New Customers' THEN 50 WHEN 'Need Attention' THEN 75 WHEN 'At Risk' THEN 95
    END AS rfm_score,
    CASE WHEN a.revenue_trend_correlation < 0 THEN 70 ELSE 30 END AS trend_score,
    (100.0 - a.business_stability_score) AS stability_score,
    a.payment_behavior, a.rfm_segment, a.business_stability_score, a.revenue_trend_correlation,
    a.active_months_last_12, a.revenue_growth_rate_12m
  FROM vol_percentile v
  JOIN quickbooks__customer_analytics a ON v.customer_id = a.customer_id
)
SELECT 
  COUNT(*) AS n_high_risk,
  SUM(CASE WHEN payment_behavior = 'Poor' THEN 1 ELSE 0 END) AS n_poor_payment,
  SUM(CASE WHEN rfm_segment = 'At Risk' THEN 1 ELSE 0 END) AS n_at_risk,
  SUM(CASE WHEN revenue_trend_correlation < 0 THEN 1 ELSE 0 END) AS n_negative_trend,
  ROUND(AVG(business_stability_score), 1) AS avg_stability,
  ROUND(AVG(active_months_last_12), 1) AS avg_active_months,
  ROUND(AVG(revenue_growth_rate_12m), 2) AS avg_growth_12m,
  ROUND(AVG(vol), 3) AS avg_margin_vol
FROM scored
WHERE 0.25 * vol_score + 0.20 * payment_score + 0.20 * rfm_score + 0.15 * trend_score + 0.20 * stability_score >= 70
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-092/attempt-01/sql/S67.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-092/attempt-01/sql/S67.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-092/attempt-01/results/S67.rows.jsonl)；完整：True；SHA256：`4b030c211223ede992b3e11e47d2d01f8575739ca78cbe7b05cfa680fdf74fbe`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "quickbooks__profitability_analysis", "kind": "base", "block": null, "base_tables": ["quickbooks__profitability_analysis"]}] | [] | ["customer_id"] |
| B2 | [{"alias": "cust_vol", "kind": "derived", "block": "B1", "base_tables": ["quickbooks__profitability_analysis"]}] | [] | [] |
| B3 | [{"alias": "v", "kind": "derived", "block": "B2", "base_tables": ["quickbooks__profitability_analysis"]}, {"alias": "a", "kind": "base", "block": null, "base_tables": ["quickbooks__customer_analytics"]}] | [{"type": "INNER", "right": "quickbooks__customer_analytics AS a", "on": "v.customer_id = a.customer_id", "using": []}] | [] |
| B4 | [{"alias": "scored", "kind": "derived", "block": "B3", "base_tables": ["quickbooks__customer_analytics", "quickbooks__profitability_analysis"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | AVG(customer_margin_volatility) | [{"table": "quickbooks__profitability_analysis", "column": "customer_margin_volatility"}] | [] | False |
| B4 | COUNT(*) | [] | [] | True |
| B4 | SUM(CASE WHEN payment_behavior = 'Poor' THEN 1 ELSE 0 END) | [] | [{"table": "quickbooks__customer_analytics", "column": "payment_behavior"}] | False |
| B4 | SUM(CASE WHEN rfm_segment = 'At Risk' THEN 1 ELSE 0 END) | [] | [{"table": "quickbooks__customer_analytics", "column": "rfm_segment"}] | False |
| B4 | SUM(CASE WHEN revenue_trend_correlation < 0 THEN 1 ELSE 0 END) | [] | [{"table": "quickbooks__customer_analytics", "column": "revenue_trend_correlation"}] | False |
| B4 | AVG(business_stability_score) | [{"table": "quickbooks__customer_analytics", "column": "business_stability_score"}] | [] | False |
| B4 | AVG(active_months_last_12) | [{"table": "quickbooks__customer_analytics", "column": "active_months_last_12"}] | [] | False |
| B4 | AVG(revenue_growth_rate_12m) | [{"table": "quickbooks__customer_analytics", "column": "revenue_growth_rate_12m"}] | [] | False |
| B4 | AVG(vol) | [{"table": "quickbooks__profitability_analysis", "column": "customer_margin_volatility"}] | [] | False |


## S68

类别 `data`；来源 `query_db`；调用 `821c2c5b81c64763a266b8e6a61ffc97`；状态 `success`。

```sql
SELECT DISTINCT profitability_sustainability FROM quickbooks__profitability_analysis
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-092/attempt-01/sql/S68.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-092/attempt-01/sql/S68.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-092/attempt-01/results/S68.rows.jsonl)；完整：True；SHA256：`9c14d7bececc4587c50185f3acf011c7e481903a1b31210aaae83d9151d456fb`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "quickbooks__profitability_analysis", "kind": "base", "block": null, "base_tables": ["quickbooks__profitability_analysis"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |


## S69

类别 `data`；来源 `query_db`；调用 `d444cfd6ac574ee582f4c68fbfba47e8`；状态 `success`。

```sql
SELECT DISTINCT profitability_tier, customer_tier, relative_performance 
FROM quickbooks__profitability_analysis
LIMIT 20
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-092/attempt-01/sql/S69.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-092/attempt-01/sql/S69.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-092/attempt-01/results/S69.rows.jsonl)；完整：True；SHA256：`0ed2e74868e1699a2e1a058ff86af4644f4cae4dcd6840c6798ac880f4ebcccc`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "quickbooks__profitability_analysis", "kind": "base", "block": null, "base_tables": ["quickbooks__profitability_analysis"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |


## S70

类别 `data`；来源 `query_db`；调用 `060076e43c3e481aa18337077338f01a`；状态 `success`。

```sql
-- Profitability sustainability by volatility segment
WITH cust_vol AS (
  SELECT customer_id, AVG(customer_margin_volatility) AS vol
  FROM quickbooks__profitability_analysis
  GROUP BY customer_id
),
ordered AS (
  SELECT customer_id, vol,
    ROW_NUMBER() OVER (ORDER BY vol DESC) AS rn,
    COUNT(*) OVER () AS total
  FROM cust_vol
),
seg AS (
  SELECT customer_id, vol,
    CASE WHEN rn <= total * 0.25 THEN 'HighVol'
         WHEN rn > total * 0.75 THEN 'LowVol'
         ELSE 'MidVol' END AS vol_segment
  FROM ordered
)
SELECT 
  s.vol_segment,
  p.profitability_sustainability,
  COUNT(*) AS n_rows,
  ROUND(100.0 * COUNT(*) / SUM(COUNT(*)) OVER (PARTITION BY s.vol_segment), 1) AS pct
FROM seg s
JOIN quickbooks__profitability_analysis p ON s.customer_id = p.customer_id
GROUP BY s.vol_segment, p.profitability_sustainability
ORDER BY s.vol_segment, pct DESC
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-092/attempt-01/sql/S70.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-092/attempt-01/sql/S70.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-092/attempt-01/results/S70.rows.jsonl)；完整：True；SHA256：`bebbb3b45f3c4253ea0a1fca2629d07e8f4691bf5ea1ab15987f7a9524a09c49`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "quickbooks__profitability_analysis", "kind": "base", "block": null, "base_tables": ["quickbooks__profitability_analysis"]}] | [] | ["customer_id"] |
| B2 | [{"alias": "cust_vol", "kind": "derived", "block": "B1", "base_tables": ["quickbooks__profitability_analysis"]}] | [] | [] |
| B3 | [{"alias": "ordered", "kind": "derived", "block": "B2", "base_tables": ["quickbooks__profitability_analysis"]}] | [] | [] |
| B4 | [{"alias": "s", "kind": "derived", "block": "B3", "base_tables": ["quickbooks__profitability_analysis"]}, {"alias": "p", "kind": "base", "block": null, "base_tables": ["quickbooks__profitability_analysis"]}] | [{"type": "INNER", "right": "quickbooks__profitability_analysis AS p", "on": "s.customer_id = p.customer_id", "using": []}] | ["s.vol_segment", "p.profitability_sustainability"] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | AVG(customer_margin_volatility) | [{"table": "quickbooks__profitability_analysis", "column": "customer_margin_volatility"}] | [] | False |
| B4 | COUNT(*) | [] | [] | True |
| B4 | COUNT(*) | [] | [] | True |
| B4 | COUNT(*) | [] | [] | True |

