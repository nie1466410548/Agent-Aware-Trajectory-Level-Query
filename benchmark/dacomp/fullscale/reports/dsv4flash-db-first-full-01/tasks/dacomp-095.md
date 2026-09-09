# dacomp-095

Based on `klaviyo__persons`, `klaviyo__person_campaign_flow`, and `marts.klaviyo__events`,…

运行：已提交。官方未评分。全部 SQL 尝试/成功 60/55；数据 SQL 57/52；Python 3 次。

完整原题：

Based on `klaviyo__persons`, `klaviyo__person_campaign_flow`, and `marts.klaviyo__events`, segment users into lifecycle stages (Cold Start: first touch with no prior activity; Win-back: re-engaged after 90 days of inactivity). Use `days_span`, `active_months`, `paid_retained_month_count`, and `paid_retention_rate_month` to measure the speed from first touch to peak activity and its relationship with long-term retention/payment. Compare touchpoint efficiency by incorporating `email_open_rate`, `email_open_rate_touch`, `email_click_to_open_rate_touch`, and `has_converted`. Additionally, explore the impact of typical touchpoint paths on retention and payment based on `touch_type` sequences, and propose optimization recommendations for frequency, cooling periods, and content cadence.

| 表 | 行数 | 列数 |
| --- | --- | --- |
| klaviyo__campaigns | 184 | 35 |
| klaviyo__flows | 79 | 27 |
| klaviyo__person_campaign_flow | 4 | 32 |
| klaviyo__persons | 1192 | 49 |


实际路线（分析者依据 SQL/源码概括，不代表 Agent 自述）：SQL 数据探索、指标及分组 → Python 准备、统计和图表 → 报告

数据库大小：602,112 字节。

## 数据 SQL

| SQL | 状态 | 基础表 | Join 输入/类型 | GROUP BY | 聚合表达式 | 结果行数 | 数据库 ms |
| --- | --- | --- | --- | --- | --- | --- | --- |
| [S3/Q1](#s3) | success | ["klaviyo__persons"] | 0 / {} | [] | ["COUNT(*)"] | 1 | 0.723 |
| [S4/Q2](#s4) | success | ["klaviyo__person_campaign_flow"] | 0 / {} | [] | ["COUNT(*)"] | 1 | 0.223 |
| [S5/Q3](#s5) | success | ["klaviyo__persons"] | 0 / {} | [] | [] | 5 | 0.447 |
| [S6/Q4](#s6) | success | ["klaviyo__person_campaign_flow"] | 0 / {} | [] | [] | 4 | 0.38 |
| [S7/Q5](#s7) | success | ["klaviyo__campaigns"] | 0 / {} | [] | ["COUNT(*)"] | 1 | 0.359 |
| [S8/Q6](#s8) | success | ["klaviyo__flows"] | 0 / {} | [] | ["COUNT(*)"] | 1 | 0.308 |
| [S10/Q7](#s10) | success | ["klaviyo__person_campaign_flow"] | 0 / {} | [] | ["COUNT(DISTINCT person_id)"] | 1 | 0.348 |
| [S11/Q8](#s11) | success | ["klaviyo__campaigns"] | 0 / {} | ["CAMPAIGN_TYPE"] | ["COUNT(*)", "AVG(email_open_rate)", "AVG(email_click_to_open_rate)"] | 10 | 0.535 |
| [S12/Q9](#s12) | success | ["klaviyo__flows"] | 0 / {} | ["trigger_type"] | ["COUNT(*)", "AVG(email_open_rate)", "AVG(email_click_to_open_rate)"] | 4 | 0.42 |
| [S13/Q10](#s13) | success | ["klaviyo__persons"] | 0 / {} | [] | ["MIN(days_span)", "MAX(days_span)", "AVG(days_span)", "MIN(active_months)", "MAX(active_months)", "AVG(active_months)", "MIN(paid_retained_month_count)", "MAX(paid_retained_month_count)", "AVG(paid_retained_month_count)"] | 1 | 1.027 |
| [S14/Q11](#s14) | success | ["klaviyo__person_campaign_flow"] | 0 / {} | ["has_converted"] | ["COUNT(*)"] | 2 | 0.359 |
| [S15/Q12](#s15) | success | ["klaviyo__persons"] | 0 / {} | [] | ["COUNT(*)", "SUM(CASE WHEN days_span - active_days >= 90 THEN 1 ELSE 0 END)", "SUM(CASE WHEN days_span - active_days >= 60 THEN 1 ELSE 0 END)", "SUM(CASE WHEN days_span - active_days >= 30 THEN 1 ELSE 0 END)", "AVG(days_span - active_days)"] | 1 | 0.924 |
| [S16/Q13](#s16) | success | ["klaviyo__persons"] | 0 / {} | ["CASE WHEN JULIANDAY(first_event_on) - JULIANDAY(created_at) <= 7 THEN 'cold_start_like' ELSE 'delayed_first_touch' END"] | ["COUNT(*)", "AVG(paid_retained_month_count)", "AVG(paid_retention_rate_month)", "AVG(email_open_rate)"] | 1 | 1.437 |
| [S17/Q14](#s17) | success | ["klaviyo__persons"] | 0 / {} | ["active_months"] | ["COUNT(*)", "AVG(paid_retained_month_count)", "AVG(paid_retention_rate_month)", "AVG(days_span)", "AVG(active_retention_rate_month)"] | 4 | 0.987 |
| [S18/Q15](#s18) | success | ["klaviyo__persons"] | 0 / {} | ["has_30day_retention"] | ["COUNT(*)", "AVG(paid_retention_rate_month)", "AVG(days_span)", "AVG(email_open_rate)", "AVG(count_placed_order)"] | 1 | 1.035 |
| [S19/Q16](#s19) | success | ["klaviyo__persons"] | 0 / {} | ["paid_retention_rate_month"] | ["COUNT(*)", "AVG(active_months)", "AVG(days_span)", "AVG(email_open_rate)"] | 4 | 1.079 |
| [S20/Q17](#s20) | success | ["klaviyo__persons"] | 0 / {} | ["CASE WHEN days_span <= 60 THEN 'fast_ramp' WHEN days_span <= 100 THEN 'medium_ramp' WHEN days_span <= 140 THEN 'slow_ramp' ELSE 'very_slow_ramp' END"] | ["COUNT(*)", "AVG(paid_retention_rate_month)", "AVG(paid_retained_month_count)", "AVG(email_open_rate)", "AVG(count_placed_order)"] | 4 | 1.189 |
| [S21/Q18](#s21) | failed | ["klaviyo__persons"] | 0 / {} | ["CASE WHEN email_open_rate >= 0.5 THEN 'high_open' WHEN email_open_rate >= 0.3 THEN 'medium_open' ELSE 'low_open' END"] | ["COUNT(*)", "AVG(paid_retention_rate_month)", "AVG(paid_retained_month_count)", "AVG(days_span)", "AVG(count_placed_order)", "AVG(has_converted)"] | unknown | 未取得；调用总时长 0.193 ms |
| [S22/Q19](#s22) | success | ["klaviyo__persons"] | 0 / {} | ["months_span - active_months"] | ["COUNT(*)", "AVG(paid_retention_rate_month)", "AVG(days_span)"] | 2 | 0.931 |
| [S23/Q20](#s23) | failed | ["klaviyo__persons"] | 0 / {} | ["CASE WHEN count_received_email <= 50 THEN 'low_freq' WHEN count_received_email <= 70 THEN 'med_freq' WHEN count_received_email <= 90 THEN 'high_freq' ELSE 'very_high_freq' END"] | ["COUNT(*)", "AVG(paid_retention_rate_month)", "AVG(paid_retained_month_count)", "AVG(count_placed_order)", "AVG(email_open_rate)", "AVG(count_unsubscribed)"] | unknown | 未取得；调用总时长 0.178 ms |
| [S24/Q21](#s24) | success | ["klaviyo__persons"] | 0 / {} | ["CASE WHEN count_clicked_email = 0 THEN 'no_clicks' WHEN count_clicked_email <= 5 THEN 'few_clicks' WHEN count_clicked_email <= 10 THEN 'some_clicks' ELSE 'many_clicks' END"] | ["COUNT(*)", "AVG(paid_retention_rate_month)", "AVG(count_placed_order)", "AVG(email_open_rate)"] | 3 | 1.158 |
| [S25/Q22](#s25) | success | ["klaviyo__persons"] | 0 / {} | ["CASE WHEN count_received_email <= 50 THEN 'low_freq' WHEN count_received_email <= 70 THEN 'med_freq' WHEN count_received_email <= 90 THEN 'high_freq' ELSE 'very_high_freq' END"] | ["COUNT(*)", "AVG(paid_retention_rate_month)", "AVG(paid_retained_month_count)", "AVG(count_placed_order)", "AVG(email_open_rate)"] | 4 | 1.247 |
| [S26/Q23](#s26) | success | ["klaviyo__persons"] | 0 / {} | ["active_months"] | ["AVG(count_placed_order)", "AVG(count_received_email)", "AVG(count_opened_email)", "AVG(count_clicked_email)", "AVG(email_open_rate)", "AVG(days_span)", "AVG(paid_retention_rate_month)"] | 4 | 1.265 |
| [S27/Q24](#s27) | success | ["klaviyo__campaigns"] | 0 / {} | ["CAMPAIGN_TYPE"] | ["COUNT(*)", "AVG(email_open_rate)", "AVG(email_click_to_open_rate)", "AVG(total_count_unique_people)", "AVG(count_placed_order)", "AVG(gmv_net)", "AVG(count_clicked_email)", "AVG(count_received_email)"] | 10 | 0.663 |
| [S28/Q25](#s28) | success | ["klaviyo__flows"] | 0 / {} | ["trigger_type"] | ["COUNT(*)", "AVG(email_open_rate)", "AVG(email_click_to_open_rate)", "AVG(total_count_unique_people)", "AVG(count_placed_order)", "AVG(gmv_net)"] | 4 | 0.415 |
| [S29/Q26](#s29) | success | ["klaviyo__persons"] | 0 / {} | ["CASE WHEN active_months <= 2 THEN 'Cold Start' WHEN active_months = 3 THEN 'Growth' WHEN active_months = 4 THEN 'Mature' ELSE 'Peak' END"] | ["COUNT(*)", "AVG(days_span)", "AVG(active_months)", "AVG(paid_retained_month_count)", "AVG(paid_retention_rate_month)", "AVG(count_placed_order)", "AVG(sum_revenue_placed_order)", "AVG(email_open_rate)", "AVG(count_received_email)", "AVG(count_clicked_email)", "AVG(active_retention_rate_month)"] | 4 | 1.768 |
| [S30/Q27](#s30) | success | ["klaviyo__persons"] | 0 / {} | ["ret_segment", "lifecycle_stage"] | ["COUNT(*)", "AVG(count_placed_order)", "AVG(sum_revenue_placed_order)", "AVG(email_open_rate)", "AVG(count_received_email)"] | 7 | 1.722 |
| [S31/Q28](#s31) | success | ["klaviyo__persons"] | 0 / {} | ["density_segment"] | ["COUNT(*)", "AVG(activity_density)", "AVG(paid_retention_rate_month)", "AVG(paid_retained_month_count)", "AVG(count_placed_order)", "AVG(sum_revenue_placed_order)", "AVG(email_open_rate)", "AVG(days_span)", "AVG(active_months)"] | 2 | 1.701 |
| [S32/Q29](#s32) | success | ["klaviyo__person_campaign_flow"] | 0 / {} | [] | [] | 4 | 0.413 |
| [S33/Q30](#s33) | success | ["klaviyo__campaigns"] | 0 / {} | ["CAMPAIGN_TYPE"] | ["MIN(scheduled_to_send_at)", "MAX(scheduled_to_send_at)", "AVG(CASE WHEN count_placed_order > 0 THEN 1.0 ELSE 0 END)"] | 10 | 0.492 |
| [S34/Q31](#s34) | success | ["klaviyo__campaigns"] | 0 / {} | ["CAMPAIGN_TYPE"] | ["AVG(count_placed_order / NULLIF(count_received_email, 0))", "AVG(count_opened_email / NULLIF(count_received_email, 0))", "AVG(count_clicked_email / NULLIF(count_received_email, 0))", "AVG(gmv_net / NULLIF(count_received_email, 0))", "AVG(gmv_net / NULLIF(count_placed_order, 0))"] | 10 | 0.58 |
| [S35/Q32](#s35) | success | ["klaviyo__campaigns", "klaviyo__person_campaign_flow"] | 2 / {'LEFT': 1} | [] | [] | 4 | 0.487 |
| [S36/Q33](#s36) | success | ["klaviyo__persons"] | 0 / {} | ["CASE WHEN days_span <= 60 THEN 'Fast (≤60d)' WHEN days_span <= 90 THEN 'Medium (61-90d)' WHEN days_span <= 120 THEN 'Slow (91-120d)' ELSE 'Very Slow (>120d)' END"] | ["COUNT(*)", "AVG(paid_retention_rate_month)", "AVG(paid_retained_month_count)", "AVG(count_placed_order)", "AVG(sum_revenue_placed_order)", "AVG(email_open_rate)", "AVG(count_received_email)", "AVG(active_days * 1.0 / days_span)"] | 4 | 1.602 |
| [S37/Q34](#s37) | failed | ["klaviyo__persons"] | 0 / {} | ["CASE WHEN count_placed_order = 0 THEN 'No Orders' WHEN count_placed_order = 1 THEN '1 Order' WHEN count_placed_order <= 3 THEN '2-3 Orders' ELSE '4+ Orders' END"] | ["COUNT(*)", "AVG(days_span)", "AVG(active_months)", "AVG(email_open_rate)", "AVG(count_received_email)", "AVG(paid_retention_rate_month)"] | unknown | 未取得；调用总时长 0.189 ms |
| [S38/Q35](#s38) | success | ["klaviyo__persons"] | 0 / {} | ["CASE WHEN count_placed_order = 0 THEN 'No Orders' WHEN count_placed_order = 1 THEN '1 Order' WHEN count_placed_order <= 3 THEN '2-3 Orders' ELSE '4+ Orders' END"] | ["COUNT(*)", "AVG(days_span)", "AVG(active_months)", "AVG(email_open_rate)", "AVG(count_received_email)", "AVG(paid_retention_rate_month)", "AVG(count_clicked_email)"] | 4 | 1.402 |
| [S39/Q36](#s39) | success | ["klaviyo__person_campaign_flow"] | 0 / {} | ["has_converted"] | ["AVG(email_open_rate_touch)", "AVG(email_click_to_open_rate_touch)", "AVG(touch_span_days)", "AVG(count_received_email)", "AVG(net_revenue_touch)"] | 2 | 0.334 |
| [S40/Q37](#s40) | success | ["klaviyo__campaigns"] | 0 / {} | ["campaign_variation_key"] | ["COUNT(*)", "AVG(email_open_rate)", "AVG(gmv_net)"] | 1 | 0.405 |
| [S41/Q38](#s41) | success | ["klaviyo__campaigns"] | 0 / {} | ["STRFTIME('%Y-%m', scheduled_to_send_at)"] | ["COUNT(*)", "AVG(email_open_rate)", "AVG(gmv_net)"] | 10 | 0.521 |
| [S42/Q39](#s42) | success | ["klaviyo__campaigns"] | 0 / {} | ["CAMPAIGN_TYPE"] | ["COUNT(*)", "SUM(CASE WHEN STATUS = 'sent' THEN 1 ELSE 0 END)"] | 10 | 0.417 |
| [S43/Q40](#s43) | success | ["klaviyo__persons"] | 0 / {} | ["CASE WHEN sum_revenue_placed_order > 0 THEN 'Paying' ELSE 'Non-Paying' END"] | ["COUNT(*)", "AVG(days_span)", "AVG(active_months)", "AVG(email_open_rate)", "AVG(count_received_email)", "AVG(paid_retention_rate_month)"] | 2 | 1.239 |
| [S44/Q41](#s44) | success | ["klaviyo__campaigns"] | 0 / {} | [] | [] | 5 | 0.359 |
| [S45/Q42](#s45) | success | ["klaviyo__campaigns", "klaviyo__flows"] | 0 / {} | ["NAME", "STATUS"] | ["COUNT(*)"] | 9 | 0.518 |
| [S46/Q43](#s46) | success | ["klaviyo__campaigns"] | 0 / {} | ["CAMPAIGN_TYPE"] | ["COUNT(*)", "SUM(count_placed_order)", "SUM(gmv_net)"] | 10 | 0.45 |
| [S47/Q44](#s47) | success | ["klaviyo__campaigns"] | 0 / {} | ["CAMPAIGN_TYPE", "STATUS"] | ["COUNT(*)"] | 12 | 0.428 |
| [S48/Q45](#s48) | failed | ["klaviyo__campaigns"] | 0 / {} | ["CAMPAIGN_TYPE"] | ["AVG(email_open_rate)", "AVG(email_click_to_open_rate)", "AVG(gmv_net / NULLIF(count_placed_order, 0))", "AVG(count_clicked_email / NULLIF(count_received_email, 0))"] | unknown | 未取得；调用总时长 0.18 ms |
| [S49/Q46](#s49) | success | ["klaviyo__campaigns"] | 0 / {} | ["CAMPAIGN_TYPE"] | ["AVG(email_open_rate)", "AVG(email_click_to_open_rate)", "AVG(gmv_net / NULLIF(count_placed_order, 0))", "AVG(count_clicked_email / NULLIF(count_received_email, 0))", "AVG(count_placed_order / NULLIF(count_received_email, 0))", "AVG(gmv_net / NULLIF(count_received_email, 0))"] | 8 | 0.546 |
| [S50/Q47](#s50) | success | ["klaviyo__flows"] | 0 / {} | [] | [] | 15 | 0.44 |
| [S51/Q48](#s51) | success | ["klaviyo__persons"] | 0 / {} | [] | [] | 1192 | 4.105 |
| [S52/Q49](#s52) | success | ["klaviyo__persons"] | 0 / {} | [] | [] | 1192 | 1.772 |
| [S53/Q50](#s53) | success | ["klaviyo__campaigns"] | 0 / {} | ["CAMPAIGN_TYPE"] | ["AVG(product_view_to_order_rate_campaign)", "AVG(count_ordered_product / NULLIF(count_placed_order, 0))", "AVG(gmv_net / NULLIF(total_count_unique_people, 0))"] | 8 | 0.532 |
| [S54/Q51](#s54) | success | ["klaviyo__campaigns"] | 0 / {} | [] | [] | 30 | 0.495 |
| [S55/Q52](#s55) | success | ["klaviyo__campaigns"] | 2 / {'INNER': 1} | ["type"] | ["COUNT(*)", "AVG(gap_days)", "MIN(gap_days)", "MAX(gap_days)"] | 8 | 1.118 |
| [S56/Q53](#s56) | failed | ["klaviyo__campaigns"] | 0 / {} | ["CAMPAIGN_TYPE"] | ["COUNT(*)", "AVG(count_placed_order / NULLIF(total_count_unique_people, 0))", "AVG(count_opened_email / NULLIF(total_count_unique_people, 0))", "AVG(count_clicked_email / NULLIF(total_count_unique_people, 0))"] | unknown | 未取得；调用总时长 0.184 ms |
| [S57/Q54](#s57) | success | ["klaviyo__campaigns"] | 2 / {'INNER': 1} | ["type"] | ["COUNT(*)", "AVG(gap_days)", "MIN(gap_days)", "MAX(gap_days)"] | 8 | 10.562 |
| [S58/Q55](#s58) | success | ["klaviyo__campaigns"] | 0 / {} | [] | [] | 40 | 0.644 |
| [S59/Q56](#s59) | success | ["klaviyo__persons"] | 0 / {} | [] | ["MAX(days_span - active_days)", "AVG(count_received_email)", "MAX(count_received_email)", "SUM(CASE WHEN email_open_rate < 0.3 THEN 1 ELSE 0 END)", "SUM(CASE WHEN email_open_rate >= 0.3 AND email_open_rate < 0.5 THEN 1 ELSE 0 END)", "SUM(CASE WHEN email_open_rate >= 0.5 THEN 1 ELSE 0 END)"] | 1 | 1.043 |
| [S60/Q57](#s60) | success | ["klaviyo__persons"] | 0 / {} | ["CASE WHEN count_received_email * 1.0 / active_months < 20 THEN '<20 emails/mo' WHEN count_received_email * 1.0 / active_months < 30 THEN '20-30 emails/mo' WHEN count_received_email * 1.0 / active_months < 40 THEN '30-40 emails/mo' ELSE '40+ emails/mo' END"] | ["COUNT(*)", "AVG(email_open_rate)", "AVG(count_placed_order)", "AVG(paid_retention_rate_month)"] | 4 | 1.281 |


## 元数据和设置

| SQL | 类别 | 状态 | 内容 |
| --- | --- | --- | --- |
| S1 | connection_setup | success | PRAGMA query_only=ON |
| S2 | metadata | success | SELECT name,sql FROM sqlite_master WHERE type='table' ORDER BY name |
| S9 | metadata | success | SELECT name FROM sqlite_master WHERE type='table' |


## Python 与执行位置

人工源码审查：**partial_violation**。主体生命周期分组和业务汇总在 SQL；Python 承担 Pearson 检验、相关矩阵和图表。P1 在导出人员数据后计算活跃密度、月均收件数、客单金额并删除缺失行，这些算术和过滤可在 SQL 中准备，因此不记为完全遵守数据库内优先。 [证据](../reviews/dacomp-095.json)。

P1：Correlation analysis and lifecycle/speed/campaign visualizations require statistical computation (Pearson correlations, p-values) and chart rendering, which SQLite cannot do natively. I will retrieve only the aggregated person-level metrics and campaign aggregates already computed in SQL.

[源码](../../../runs/dsv4flash-db-first-full-01/dacomp-095/attempt-01/python/P1.py)；[输出](../../../runs/dsv4flash-db-first-full-01/dacomp-095/attempt-01/python/P1.stdout)；[错误](../../../runs/dsv4flash-db-first-full-01/dacomp-095/attempt-01/python/P1.stderr)。检出需人工核验的 SQL 可实现操作：.query(；不能仅凭理由判为合规。

P2：Creating visualizations for the report: lifecycle stage comparison, speed group analysis, campaign efficiency, and density-frequency scatter plots. These require matplotlib rendering.

[源码](../../../runs/dsv4flash-db-first-full-01/dacomp-095/attempt-01/python/P2.py)；[输出](../../../runs/dsv4flash-db-first-full-01/dacomp-095/attempt-01/python/P2.stdout)；[错误](../../../runs/dsv4flash-db-first-full-01/dacomp-095/attempt-01/python/P2.stderr)。检出需人工核验的 SQL 可实现操作：.query(；不能仅凭理由判为合规。

P3：Creating final visualizations for email intensity analysis and the touchpoint path/cadence, which require chart rendering not available in SQL.

[源码](../../../runs/dsv4flash-db-first-full-01/dacomp-095/attempt-01/python/P3.py)；[输出](../../../runs/dsv4flash-db-first-full-01/dacomp-095/attempt-01/python/P3.stdout)；[错误](../../../runs/dsv4flash-db-first-full-01/dacomp-095/attempt-01/python/P3.stderr)。自动源码筛查未检出预设迁出信号；这不是全面语义合规证明。

## 优化机会

已验证候选。筛选限于精确 SQL、相同自包含 CTE、相同单表完整过滤、可分解单表聚合；未覆盖任意 Join 等价和一般谓词蕴含。全部候选都是 offline，未测在线预测。

| 候选 | 类型 | 已有结果 | 覆盖 SQL | 后续次数 | 中间行数 | 验证 | 成本 |
| --- | --- | --- | --- | --- | --- | --- | --- |
| C1 | aggregate MV | False | ["S3", "S13", "S15", "S16", "S17", "S18", "S19", "S20", "S22", "S24", "S25", "S26", "S29", "S36", "S38", "S43", "S59", "S60"] | 17 | 81 | rejected_result_mismatch | Not benchmarked; correctness alone does not establish net speedup. |
| C2 | aggregate MV | False | ["S4", "S14", "S39"] | 2 | unknown | not_verified_cap | Not tested |
| C3 | aggregate MV | False | ["S7", "S11", "S27", "S33", "S34", "S40", "S41", "S42", "S46", "S47"] | 9 | 112 | rejected_result_mismatch | Not benchmarked; correctness alone does not establish net speedup. |
| C4 | aggregate MV | False | ["S8", "S12", "S28"] | 2 | unknown | not_verified_cap | Not tested |
| C5 | common filtered view | False | ["S49", "S53", "S54"] | 2 | 124 | verified | Not benchmarked; correctness alone does not establish net speedup. |
| C6 | aggregate MV | False | ["S49", "S53"] | 1 | unknown | not_verified_cap | Not tested |


已验证覆盖（含触发查询、候选并集去重）：3/52 条成功数据 SQL。正确性仅针对当前数据库快照；未测性能的候选不能声称已加速。

[完整 build/rewrite 与比较证据](dacomp-095.analysis.json)。

### C5：common filtered view

Same single source and complete filter; original filter retained.

原查询 [S49](#s49), [S53](#s53), [S54](#s54) → 新增共享状态 C5 → 后续 2 次可复用。该构建点为事后假设，不代表 Agent 当时预知后续。

构建定义：

```sql
SELECT * FROM "klaviyo__campaigns" WHERE status = 'SENT'
```

受益查询 S49 的改写示例：

```sql
SELECT CAMPAIGN_TYPE, AVG(email_open_rate) AS avg_open, AVG(email_click_to_open_rate) AS avg_ctr, AVG(gmv_net / NULLIF(count_placed_order, 0)) AS aov, AVG(count_clicked_email / NULLIF(count_received_email, 0)) AS click_rate_received, AVG(count_placed_order / NULLIF(count_received_email, 0)) AS orders_per_recv, AVG(gmv_net / NULLIF(count_received_email, 0)) AS gmv_per_recv FROM temp.reuse_candidate AS klaviyo__campaigns WHERE STATUS = 'SENT' GROUP BY CAMPAIGN_TYPE ORDER BY gmv_per_recv DESC
```

| 原 SQL | 列名一致 | 结果一致 | 比较方法 |
| --- | --- | --- | --- |
| S49 | True | True | ordered_numeric_tolerance |
| S53 | True | True | ordered_numeric_tolerance |
| S54 | True | True | ordered_numeric_tolerance |


验证状态：verified；成本结论：Not benchmarked; correctness alone does not establish net speedup.

### C1：aggregate MV

Union of grouping keys; decomposable aggregate states; AVG uses SUM and non-NULL COUNT.

原查询 [S3](#s3), [S13](#s13), [S15](#s15), [S16](#s16), [S17](#s17), [S18](#s18), [S19](#s19), [S20](#s20), [S22](#s22), [S24](#s24), [S25](#s25), [S26](#s26), [S29](#s29), [S36](#s36), [S38](#s38), [S43](#s43), [S59](#s59), [S60](#s60) → 新增共享状态 C1 → 后续 17 次可复用。该构建点为事后假设，不代表 Agent 当时预知后续。

构建定义：

```sql
SELECT CASE WHEN JULIANDAY(first_event_on) - JULIANDAY(created_at) <= 7 THEN 'cold_start_like' ELSE 'delayed_first_touch' END AS __g0, active_months AS __g1, has_30day_retention AS __g2, paid_retention_rate_month AS __g3, CASE WHEN days_span <= 60 THEN 'fast_ramp' WHEN days_span <= 100 THEN 'medium_ramp' WHEN days_span <= 140 THEN 'slow_ramp' ELSE 'very_slow_ramp' END AS __g4, months_span - active_months AS __g5, CASE WHEN count_clicked_email = 0 THEN 'no_clicks' WHEN count_clicked_email <= 5 THEN 'few_clicks' WHEN count_clicked_email <= 10 THEN 'some_clicks' ELSE 'many_clicks' END AS __g6, CASE WHEN count_received_email <= 50 THEN 'low_freq' WHEN count_received_email <= 70 THEN 'med_freq' WHEN count_received_email <= 90 THEN 'high_freq' ELSE 'very_high_freq' END AS __g7, CASE WHEN active_months <= 2 THEN 'Cold Start' WHEN active_months = 3 THEN 'Growth' WHEN active_months = 4 THEN 'Mature' ELSE 'Peak' END AS __g8, CASE WHEN days_span <= 60 THEN 'Fast (≤60d)' WHEN days_span <= 90 THEN 'Medium (61-90d)' WHEN days_span <= 120 THEN 'Slow (91-120d)' ELSE 'Very Slow (>120d)' END AS __g9, CASE WHEN count_placed_order = 0 THEN 'No Orders' WHEN count_placed_order = 1 THEN '1 Order' WHEN count_placed_order <= 3 THEN '2-3 Orders' ELSE '4+ Orders' END AS __g10, CASE WHEN sum_revenue_placed_order > 0 THEN 'Paying' ELSE 'Non-Paying' END AS __g11, CASE WHEN count_received_email * 1.0 / active_months < 20 THEN '<20 emails/mo' WHEN count_received_email * 1.0 / active_months < 30 THEN '20-30 emails/mo' WHEN count_received_email * 1.0 / active_months < 40 THEN '30-40 emails/mo' ELSE '40+ emails/mo' END AS __g12, COUNT(*) AS __a0, MIN(days_span) AS __a1, MAX(days_span) AS __a2, SUM(days_span) AS __a3_sum, COUNT(days_span) AS __a3_n, MIN(active_months) AS __a4, MAX(active_months) AS __a5, SUM(active_months) AS __a6_sum, COUNT(active_months) AS __a6_n, MIN(paid_retained_month_count) AS __a7, MAX(paid_retained_month_count) AS __a8, SUM(paid_retained_month_count) AS __a9_sum, COUNT(paid_retained_month_count) AS __a9_n, SUM(CASE WHEN days_span - active_days >= 90 THEN 1 ELSE 0 END) AS __a10, SUM(CASE WHEN days_span - active_days >= 60 THEN 1 ELSE 0 END) AS __a11, SUM(CASE WHEN days_span - active_days >= 30 THEN 1 ELSE 0 END) AS __a12, SUM(days_span - active_days) AS __a13_sum, COUNT(days_span - active_days) AS __a13_n, SUM(paid_retention_rate_month) AS __a14_sum, COUNT(paid_retention_rate_month) AS __a14_n, SUM(email_open_rate) AS __a15_sum, COUNT(email_open_rate) AS __a15_n, SUM(active_retention_rate_month) AS __a16_sum, COUNT(active_retention_rate_month) AS __a16_n, SUM(count_placed_order) AS __a17_sum, COUNT(count_placed_order) AS __a17_n, SUM(count_received_email) AS __a18_sum, COUNT(count_received_email) AS __a18_n, SUM(count_opened_email) AS __a19_sum, COUNT(count_opened_email) AS __a19_n, SUM(count_clicked_email) AS __a20_sum, COUNT(count_clicked_email) AS __a20_n, SUM(sum_revenue_placed_order) AS __a21_sum, COUNT(sum_revenue_placed_order) AS __a21_n, SUM(active_days * 1.0 / days_span) AS __a22_sum, COUNT(active_days * 1.0 / days_span) AS __a22_n, MAX(days_span - active_days) AS __a23, MAX(count_received_email) AS __a24, SUM(CASE WHEN email_open_rate < 0.3 THEN 1 ELSE 0 END) AS __a25, SUM(CASE WHEN email_open_rate >= 0.3 AND email_open_rate < 0.5 THEN 1 ELSE 0 END) AS __a26, SUM(CASE WHEN email_open_rate >= 0.5 THEN 1 ELSE 0 END) AS __a27 FROM "klaviyo__persons"  GROUP BY CASE WHEN JULIANDAY(first_event_on) - JULIANDAY(created_at) <= 7 THEN 'cold_start_like' ELSE 'delayed_first_touch' END, active_months, has_30day_retention, paid_retention_rate_month, CASE WHEN days_span <= 60 THEN 'fast_ramp' WHEN days_span <= 100 THEN 'medium_ramp' WHEN days_span <= 140 THEN 'slow_ramp' ELSE 'very_slow_ramp' END, months_span - active_months, CASE WHEN count_clicked_email = 0 THEN 'no_clicks' WHEN count_clicked_email <= 5 THEN 'few_clicks' WHEN count_clicked_email <= 10 THEN 'some_clicks' ELSE 'many_clicks' END, CASE WHEN count_received_email <= 50 THEN 'low_freq' WHEN count_received_email <= 70 THEN 'med_freq' WHEN count_received_email <= 90 THEN 'high_freq' ELSE 'very_high_freq' END, CASE WHEN active_months <= 2 THEN 'Cold Start' WHEN active_months = 3 THEN 'Growth' WHEN active_months = 4 THEN 'Mature' ELSE 'Peak' END, CASE WHEN days_span <= 60 THEN 'Fast (≤60d)' WHEN days_span <= 90 THEN 'Medium (61-90d)' WHEN days_span <= 120 THEN 'Slow (91-120d)' ELSE 'Very Slow (>120d)' END, CASE WHEN count_placed_order = 0 THEN 'No Orders' WHEN count_placed_order = 1 THEN '1 Order' WHEN count_placed_order <= 3 THEN '2-3 Orders' ELSE '4+ Orders' END, CASE WHEN sum_revenue_placed_order > 0 THEN 'Paying' ELSE 'Non-Paying' END, CASE WHEN count_received_email * 1.0 / active_months < 20 THEN '<20 emails/mo' WHEN count_received_email * 1.0 / active_months < 30 THEN '20-30 emails/mo' WHEN count_received_email * 1.0 / active_months < 40 THEN '30-40 emails/mo' ELSE '40+ emails/mo' END
```

受益查询 S3 的改写示例：

```sql
SELECT SUM(__a0) AS total_persons FROM temp.reuse_candidate
```

| 原 SQL | 列名一致 | 结果一致 | 比较方法 |
| --- | --- | --- | --- |
| S3 | True | True | exact_multiset |
| S13 | True | True | exact_multiset |
| S15 | True | True | exact_multiset |
| S16 | True | False | exact_multiset |
| S17 | True | True | ordered_numeric_tolerance |
| S18 | True | False | exact_multiset |
| S19 | True | True | ordered_numeric_tolerance |
| S20 | True | True | ordered_numeric_tolerance |
| S22 | True | True | ordered_numeric_tolerance |
| S24 | True | True | ordered_numeric_tolerance |
| S25 | True | True | ordered_numeric_tolerance |
| S26 | True | True | ordered_numeric_tolerance |
| S29 | True | True | ordered_numeric_tolerance |
| S36 | True | True | ordered_numeric_tolerance |
| S38 | True | False | exact_multiset |
| S43 | True | False | exact_multiset |
| S59 | True | True | exact_multiset |
| S60 | True | True | ordered_numeric_tolerance |


验证状态：rejected_result_mismatch；成本结论：Not benchmarked; correctness alone does not establish net speedup.

### C3：aggregate MV

Union of grouping keys; decomposable aggregate states; AVG uses SUM and non-NULL COUNT.

原查询 [S7](#s7), [S11](#s11), [S27](#s27), [S33](#s33), [S34](#s34), [S40](#s40), [S41](#s41), [S42](#s42), [S46](#s46), [S47](#s47) → 新增共享状态 C3 → 后续 9 次可复用。该构建点为事后假设，不代表 Agent 当时预知后续。

构建定义：

```sql
SELECT campaign_type AS __g0, campaign_variation_key AS __g1, STRFTIME('%Y-%m', scheduled_to_send_at) AS __g2, status AS __g3, COUNT(*) AS __a0, SUM(email_open_rate) AS __a1_sum, COUNT(email_open_rate) AS __a1_n, SUM(email_click_to_open_rate) AS __a2_sum, COUNT(email_click_to_open_rate) AS __a2_n, SUM(total_count_unique_people) AS __a3_sum, COUNT(total_count_unique_people) AS __a3_n, SUM(count_placed_order) AS __a4_sum, COUNT(count_placed_order) AS __a4_n, SUM(gmv_net) AS __a5_sum, COUNT(gmv_net) AS __a5_n, SUM(count_clicked_email) AS __a6_sum, COUNT(count_clicked_email) AS __a6_n, SUM(count_received_email) AS __a7_sum, COUNT(count_received_email) AS __a7_n, MIN(scheduled_to_send_at) AS __a8, MAX(scheduled_to_send_at) AS __a9, SUM(CASE WHEN count_placed_order > 0 THEN 1.0 ELSE 0 END) AS __a10_sum, COUNT(CASE WHEN count_placed_order > 0 THEN 1.0 ELSE 0 END) AS __a10_n, SUM(count_placed_order / NULLIF(count_received_email, 0)) AS __a11_sum, COUNT(count_placed_order / NULLIF(count_received_email, 0)) AS __a11_n, SUM(count_opened_email / NULLIF(count_received_email, 0)) AS __a12_sum, COUNT(count_opened_email / NULLIF(count_received_email, 0)) AS __a12_n, SUM(count_clicked_email / NULLIF(count_received_email, 0)) AS __a13_sum, COUNT(count_clicked_email / NULLIF(count_received_email, 0)) AS __a13_n, SUM(gmv_net / NULLIF(count_received_email, 0)) AS __a14_sum, COUNT(gmv_net / NULLIF(count_received_email, 0)) AS __a14_n, SUM(gmv_net / NULLIF(count_placed_order, 0)) AS __a15_sum, COUNT(gmv_net / NULLIF(count_placed_order, 0)) AS __a15_n, SUM(CASE WHEN status = 'sent' THEN 1 ELSE 0 END) AS __a16, SUM(count_placed_order) AS __a17, SUM(gmv_net) AS __a18 FROM "klaviyo__campaigns"  GROUP BY campaign_type, campaign_variation_key, STRFTIME('%Y-%m', scheduled_to_send_at), status
```

受益查询 S7 的改写示例：

```sql
SELECT SUM(__a0) AS n FROM temp.reuse_candidate
```

| 原 SQL | 列名一致 | 结果一致 | 比较方法 |
| --- | --- | --- | --- |
| S7 | True | True | exact_multiset |
| S11 | True | True | ordered_numeric_tolerance |
| S27 | True | True | ordered_numeric_tolerance |
| S33 | True | True | ordered_numeric_tolerance |
| S34 | True | True | ordered_numeric_tolerance |
| S40 | True | False | exact_multiset |
| S41 | True | True | ordered_numeric_tolerance |
| S42 | True | True | exact_multiset |
| S46 | True | True | ordered_numeric_tolerance |
| S47 | True | True | ordered_numeric_tolerance |


验证状态：rejected_result_mismatch；成本结论：Not benchmarked; correctness alone does not establish net speedup.

结果依赖：自动记录 SQL→Python 的接口父调用，以及源码中引用归档文件的消费者；字面值相同不认定因果。模型方向选择需要人工读取消息，尚未做全面因果标注。

[原始报告](../../../runs/dsv4flash-db-first-full-01/dacomp-095/attempt-01/answer.md)；[统一消息](../../../runs/dsv4flash-db-first-full-01/dacomp-095/attempt-01/messages.jsonl)；[原始 OpenCode 事件](../../../runs/dsv4flash-db-first-full-01/dacomp-095/attempt-01/opencode.jsonl)；[SQL 引擎日志](../../../runs/dsv4flash-db-first-full-01/dacomp-095/attempt-01/sql_journal.jsonl)。

[可读报告（本地图片链接规范化）](../answers/dacomp-095.md)。原始回答保留，分析结论未改写。

## S1

类别 `connection_setup`；来源 `connection`；调用 `e9bce4785476400884e81206ebdbeec9`；状态 `success`。

```sql
PRAGMA query_only=ON
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-095/attempt-01/sql/S1.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-095/attempt-01/sql/S1.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-095/attempt-01/results/S1.rows.jsonl)；完整：True；SHA256：`e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`。

## S2

类别 `metadata`；来源 `list_db`；调用 `e9bce4785476400884e81206ebdbeec9`；状态 `success`。

```sql
SELECT name,sql FROM sqlite_master WHERE type='table' ORDER BY name
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-095/attempt-01/sql/S2.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-095/attempt-01/sql/S2.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-095/attempt-01/results/S2.rows.jsonl)；完整：True；SHA256：`5488407dde22cfc4870f82317907d216934f1ce5c14ca4977abbca8f4ea4e978`。

## S3

类别 `data`；来源 `query_db`；调用 `0f0159b4e117488c874e6b419f18cee8`；状态 `success`。

```sql
SELECT COUNT(*) as total_persons FROM klaviyo__persons
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-095/attempt-01/sql/S3.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-095/attempt-01/sql/S3.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-095/attempt-01/results/S3.rows.jsonl)；完整：True；SHA256：`9f08c25dc6cbc1e501f18da20f78731cfb845e17d1f8840fdab7d95b83e87cb8`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "klaviyo__persons", "kind": "base", "block": null, "base_tables": ["klaviyo__persons"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |


## S4

类别 `data`；来源 `query_db`；调用 `780306ab0c714a398fd3808ccf17aab1`；状态 `success`。

```sql
SELECT COUNT(*) as total_touches FROM klaviyo__person_campaign_flow
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-095/attempt-01/sql/S4.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-095/attempt-01/sql/S4.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-095/attempt-01/results/S4.rows.jsonl)；完整：True；SHA256：`9d1f4e3a2170ce5f947bcdfa249a77885875b0d9d7af88ad3fbc7f7cd7a224fa`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "klaviyo__person_campaign_flow", "kind": "base", "block": null, "base_tables": ["klaviyo__person_campaign_flow"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |


## S5

类别 `data`；来源 `query_db`；调用 `45f4af42c4464b09892cb023cfe37289`；状态 `success`。

```sql
SELECT * FROM klaviyo__persons LIMIT 5
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-095/attempt-01/sql/S5.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-095/attempt-01/sql/S5.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-095/attempt-01/results/S5.rows.jsonl)；完整：True；SHA256：`6c8262cb9403d66b6421c2dba966fab2750f2d3c1778aad3e04e6e36e59a5052`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "klaviyo__persons", "kind": "base", "block": null, "base_tables": ["klaviyo__persons"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |


## S6

类别 `data`；来源 `query_db`；调用 `90e976de256945ae86283665fce7bc63`；状态 `success`。

```sql
SELECT * FROM klaviyo__person_campaign_flow LIMIT 5
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-095/attempt-01/sql/S6.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-095/attempt-01/sql/S6.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-095/attempt-01/results/S6.rows.jsonl)；完整：True；SHA256：`85f76e3e10a894a658042a15b78bc4ba0c89e3579936b7e84447e8df8337de90`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "klaviyo__person_campaign_flow", "kind": "base", "block": null, "base_tables": ["klaviyo__person_campaign_flow"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |


## S7

类别 `data`；来源 `query_db`；调用 `4739e1afeead4b1890d0882cad242bd3`；状态 `success`。

```sql
SELECT COUNT(*) as n FROM klaviyo__campaigns
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-095/attempt-01/sql/S7.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-095/attempt-01/sql/S7.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-095/attempt-01/results/S7.rows.jsonl)；完整：True；SHA256：`f83d3a8ea27d26acfa36ad980fa698f7127c066a1017eeeadab628468cc00438`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "klaviyo__campaigns", "kind": "base", "block": null, "base_tables": ["klaviyo__campaigns"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |


## S8

类别 `data`；来源 `query_db`；调用 `8b50c70126bd4cedaa2e823712492e88`；状态 `success`。

```sql
SELECT COUNT(*) as n FROM klaviyo__flows
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-095/attempt-01/sql/S8.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-095/attempt-01/sql/S8.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-095/attempt-01/results/S8.rows.jsonl)；完整：True；SHA256：`7a76fa25eba033be620944006773908f801368d892db8c78cd12ad171501456e`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "klaviyo__flows", "kind": "base", "block": null, "base_tables": ["klaviyo__flows"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |


## S9

类别 `metadata`；来源 `query_db`；调用 `3fac4c5036a0424eb813dbb091e3dbea`；状态 `success`。

```sql
SELECT name FROM sqlite_master WHERE type='table'
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-095/attempt-01/sql/S9.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-095/attempt-01/sql/S9.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-095/attempt-01/results/S9.rows.jsonl)；完整：True；SHA256：`ac5c19f11ecfaf4aecf1192ed7bbec94f4f34228c46c2d5ea47d4e28d0ace4e8`。

## S10

类别 `data`；来源 `query_db`；调用 `c09cdefb8efd47669bfc5fa841fcc556`；状态 `success`。

```sql
SELECT COUNT(DISTINCT person_id) as distinct_persons FROM klaviyo__person_campaign_flow
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-095/attempt-01/sql/S10.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-095/attempt-01/sql/S10.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-095/attempt-01/results/S10.rows.jsonl)；完整：True；SHA256：`9d1f4e3a2170ce5f947bcdfa249a77885875b0d9d7af88ad3fbc7f7cd7a224fa`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "klaviyo__person_campaign_flow", "kind": "base", "block": null, "base_tables": ["klaviyo__person_campaign_flow"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(DISTINCT person_id) | [{"table": "klaviyo__person_campaign_flow", "column": "person_id"}] | [] | False |


## S11

类别 `data`；来源 `query_db`；调用 `d3755614e7044d6ba03346747687cd29`；状态 `success`。

```sql
SELECT CAMPAIGN_TYPE, COUNT(*) as n, AVG(email_open_rate) as avg_open_rate, AVG(email_click_to_open_rate) as avg_ctr FROM klaviyo__campaigns GROUP BY CAMPAIGN_TYPE ORDER BY n DESC
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-095/attempt-01/sql/S11.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-095/attempt-01/sql/S11.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-095/attempt-01/results/S11.rows.jsonl)；完整：True；SHA256：`fc8b191c4ebb2e7332d974f2269a150324ae26145747972e52c024e232a08b19`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "klaviyo__campaigns", "kind": "base", "block": null, "base_tables": ["klaviyo__campaigns"]}] | [] | ["CAMPAIGN_TYPE"] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |
| B1 | AVG(email_open_rate) | [{"table": "klaviyo__campaigns", "column": "email_open_rate"}] | [] | False |
| B1 | AVG(email_click_to_open_rate) | [{"table": "klaviyo__campaigns", "column": "email_click_to_open_rate"}] | [] | False |


## S12

类别 `data`；来源 `query_db`；调用 `f260c0c8f7aa425aaa562705b8ce363f`；状态 `success`。

```sql
SELECT trigger_type, COUNT(*) as n, AVG(email_open_rate) as avg_open_rate, AVG(email_click_to_open_rate) as avg_ctr FROM klaviyo__flows GROUP BY trigger_type ORDER BY n DESC
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-095/attempt-01/sql/S12.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-095/attempt-01/sql/S12.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-095/attempt-01/results/S12.rows.jsonl)；完整：True；SHA256：`6a31769345de3ddd80cc7bb52065eb4ec755239b1b67e8f8a34ec745858b5938`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "klaviyo__flows", "kind": "base", "block": null, "base_tables": ["klaviyo__flows"]}] | [] | ["trigger_type"] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |
| B1 | AVG(email_open_rate) | [{"table": "klaviyo__flows", "column": "email_open_rate"}] | [] | False |
| B1 | AVG(email_click_to_open_rate) | [{"table": "klaviyo__flows", "column": "email_click_to_open_rate"}] | [] | False |


## S13

类别 `data`；来源 `query_db`；调用 `03b7bf7763364b0fa3ed600cd8e6380d`；状态 `success`。

```sql
SELECT MIN(days_span) as min_ds, MAX(days_span) as max_ds, AVG(days_span) as avg_ds, MIN(active_months) as min_am, MAX(active_months) as max_am, AVG(active_months) as avg_am, MIN(paid_retained_month_count) as min_prm, MAX(paid_retained_month_count) as max_prm, AVG(paid_retained_month_count) as avg_prm FROM klaviyo__persons
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-095/attempt-01/sql/S13.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-095/attempt-01/sql/S13.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-095/attempt-01/results/S13.rows.jsonl)；完整：True；SHA256：`5399a0414dcd9757f2973a2ac35eebdccfea120f6fe45680d2620e0de68b55f3`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "klaviyo__persons", "kind": "base", "block": null, "base_tables": ["klaviyo__persons"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | MIN(days_span) | [{"table": "klaviyo__persons", "column": "days_span"}] | [] | False |
| B1 | MAX(days_span) | [{"table": "klaviyo__persons", "column": "days_span"}] | [] | False |
| B1 | AVG(days_span) | [{"table": "klaviyo__persons", "column": "days_span"}] | [] | False |
| B1 | MIN(active_months) | [{"table": "klaviyo__persons", "column": "active_months"}] | [] | False |
| B1 | MAX(active_months) | [{"table": "klaviyo__persons", "column": "active_months"}] | [] | False |
| B1 | AVG(active_months) | [{"table": "klaviyo__persons", "column": "active_months"}] | [] | False |
| B1 | MIN(paid_retained_month_count) | [{"table": "klaviyo__persons", "column": "paid_retained_month_count"}] | [] | False |
| B1 | MAX(paid_retained_month_count) | [{"table": "klaviyo__persons", "column": "paid_retained_month_count"}] | [] | False |
| B1 | AVG(paid_retained_month_count) | [{"table": "klaviyo__persons", "column": "paid_retained_month_count"}] | [] | False |


## S14

类别 `data`；来源 `query_db`；调用 `5dc49eb7d948410d81534ef8ddcb5c46`；状态 `success`。

```sql
SELECT has_converted, COUNT(*) as n FROM klaviyo__person_campaign_flow GROUP BY has_converted
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-095/attempt-01/sql/S14.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-095/attempt-01/sql/S14.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-095/attempt-01/results/S14.rows.jsonl)；完整：True；SHA256：`5146455846c32dc84745ec0c505b50ec5947e82461a297a1e739fdccae71316d`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "klaviyo__person_campaign_flow", "kind": "base", "block": null, "base_tables": ["klaviyo__person_campaign_flow"]}] | [] | ["has_converted"] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |


## S15

类别 `data`；来源 `query_db`；调用 `804fd632f3c941b9981564c7a1db0854`；状态 `success`。

```sql
SELECT 
  COUNT(*) as n,
  SUM(CASE WHEN days_span - active_days >= 90 THEN 1 ELSE 0 END) as inactive_90plus,
  SUM(CASE WHEN days_span - active_days >= 60 THEN 1 ELSE 0 END) as inactive_60plus,
  SUM(CASE WHEN days_span - active_days >= 30 THEN 1 ELSE 0 END) as inactive_30plus,
  AVG(days_span - active_days) as avg_inactive_days
FROM klaviyo__persons
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-095/attempt-01/sql/S15.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-095/attempt-01/sql/S15.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-095/attempt-01/results/S15.rows.jsonl)；完整：True；SHA256：`728b7484d3600ba886e385b3530c6f4aee142bdb28c54b68557e32357d52c0b9`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "klaviyo__persons", "kind": "base", "block": null, "base_tables": ["klaviyo__persons"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |
| B1 | SUM(CASE WHEN days_span - active_days >= 90 THEN 1 ELSE 0 END) | [] | [{"table": "klaviyo__persons", "column": "days_span"}, {"table": "klaviyo__persons", "column": "active_days"}] | False |
| B1 | SUM(CASE WHEN days_span - active_days >= 60 THEN 1 ELSE 0 END) | [] | [{"table": "klaviyo__persons", "column": "days_span"}, {"table": "klaviyo__persons", "column": "active_days"}] | False |
| B1 | SUM(CASE WHEN days_span - active_days >= 30 THEN 1 ELSE 0 END) | [] | [{"table": "klaviyo__persons", "column": "days_span"}, {"table": "klaviyo__persons", "column": "active_days"}] | False |
| B1 | AVG(days_span - active_days) | [{"table": "klaviyo__persons", "column": "days_span"}, {"table": "klaviyo__persons", "column": "active_days"}] | [] | False |


## S16

类别 `data`；来源 `query_db`；调用 `387306ad7d754622b5e6a1f3554b7fee`；状态 `success`。

```sql
SELECT 
  CASE WHEN julianday(first_event_on) - julianday(created_at) <= 7 THEN 'cold_start_like' ELSE 'delayed_first_touch' END as first_touch_seg,
  COUNT(*) as n,
  AVG(paid_retained_month_count) as avg_prm,
  AVG(paid_retention_rate_month) as avg_prr,
  AVG(email_open_rate) as avg_open
FROM klaviyo__persons
GROUP BY first_touch_seg
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-095/attempt-01/sql/S16.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-095/attempt-01/sql/S16.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-095/attempt-01/results/S16.rows.jsonl)；完整：True；SHA256：`abb4462bb022794cb36efc439b935355d28967a7b018f6f338aa8399efe9a797`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "klaviyo__persons", "kind": "base", "block": null, "base_tables": ["klaviyo__persons"]}] | [] | ["CASE WHEN JULIANDAY(first_event_on) - JULIANDAY(created_at) <= 7 THEN 'cold_start_like' ELSE 'delayed_first_touch' END"] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |
| B1 | AVG(paid_retained_month_count) | [{"table": "klaviyo__persons", "column": "paid_retained_month_count"}] | [] | False |
| B1 | AVG(paid_retention_rate_month) | [{"table": "klaviyo__persons", "column": "paid_retention_rate_month"}] | [] | False |
| B1 | AVG(email_open_rate) | [{"table": "klaviyo__persons", "column": "email_open_rate"}] | [] | False |


## S17

类别 `data`；来源 `query_db`；调用 `f900af99715b4567aa0d65d1636f1aef`；状态 `success`。

```sql
SELECT 
  active_months,
  COUNT(*) as n,
  AVG(paid_retained_month_count) as avg_prm,
  AVG(paid_retention_rate_month) as avg_prr,
  AVG(days_span) as avg_ds,
  AVG(active_retention_rate_month) as avg_arm
FROM klaviyo__persons
GROUP BY active_months
ORDER BY active_months
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-095/attempt-01/sql/S17.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-095/attempt-01/sql/S17.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-095/attempt-01/results/S17.rows.jsonl)；完整：True；SHA256：`c9b48fe50a90b62433353a33ad702c34cfec31d871075b841acb927c2bcbfd13`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "klaviyo__persons", "kind": "base", "block": null, "base_tables": ["klaviyo__persons"]}] | [] | ["active_months"] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |
| B1 | AVG(paid_retained_month_count) | [{"table": "klaviyo__persons", "column": "paid_retained_month_count"}] | [] | False |
| B1 | AVG(paid_retention_rate_month) | [{"table": "klaviyo__persons", "column": "paid_retention_rate_month"}] | [] | False |
| B1 | AVG(days_span) | [{"table": "klaviyo__persons", "column": "days_span"}] | [] | False |
| B1 | AVG(active_retention_rate_month) | [{"table": "klaviyo__persons", "column": "active_retention_rate_month"}] | [] | False |


## S18

类别 `data`；来源 `query_db`；调用 `88cbe58b05a948578eb12e755e30ad9d`；状态 `success`。

```sql
SELECT 
  has_30day_retention,
  COUNT(*) as n,
  AVG(paid_retention_rate_month) as avg_prr,
  AVG(days_span) as avg_ds,
  AVG(email_open_rate) as avg_open,
  AVG(count_placed_order) as avg_orders
FROM klaviyo__persons
GROUP BY has_30day_retention
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-095/attempt-01/sql/S18.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-095/attempt-01/sql/S18.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-095/attempt-01/results/S18.rows.jsonl)；完整：True；SHA256：`efcfb6f20e6d3c6b6a73d2d70124bb3b1745a45dc342f60e1a2da19cc439775c`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "klaviyo__persons", "kind": "base", "block": null, "base_tables": ["klaviyo__persons"]}] | [] | ["has_30day_retention"] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |
| B1 | AVG(paid_retention_rate_month) | [{"table": "klaviyo__persons", "column": "paid_retention_rate_month"}] | [] | False |
| B1 | AVG(days_span) | [{"table": "klaviyo__persons", "column": "days_span"}] | [] | False |
| B1 | AVG(email_open_rate) | [{"table": "klaviyo__persons", "column": "email_open_rate"}] | [] | False |
| B1 | AVG(count_placed_order) | [{"table": "klaviyo__persons", "column": "count_placed_order"}] | [] | False |


## S19

类别 `data`；来源 `query_db`；调用 `4dd46f18e1a14087a4c3f382b8c25947`；状态 `success`。

```sql
SELECT 
  paid_retention_rate_month,
  COUNT(*) as n,
  AVG(active_months) as avg_am,
  AVG(days_span) as avg_ds,
  AVG(email_open_rate) as avg_open
FROM klaviyo__persons
GROUP BY paid_retention_rate_month
ORDER BY paid_retention_rate_month
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-095/attempt-01/sql/S19.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-095/attempt-01/sql/S19.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-095/attempt-01/results/S19.rows.jsonl)；完整：True；SHA256：`2a92dc0272e7f2138bfed4a7eabad6ffd6fe9c8074875584275bca3a205896ab`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "klaviyo__persons", "kind": "base", "block": null, "base_tables": ["klaviyo__persons"]}] | [] | ["paid_retention_rate_month"] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |
| B1 | AVG(active_months) | [{"table": "klaviyo__persons", "column": "active_months"}] | [] | False |
| B1 | AVG(days_span) | [{"table": "klaviyo__persons", "column": "days_span"}] | [] | False |
| B1 | AVG(email_open_rate) | [{"table": "klaviyo__persons", "column": "email_open_rate"}] | [] | False |


## S20

类别 `data`；来源 `query_db`；调用 `b3de28a3ae8d4c5eaae896d7895122cb`；状态 `success`。

```sql
SELECT 
  CASE 
    WHEN days_span <= 60 THEN 'fast_ramp'
    WHEN days_span <= 100 THEN 'medium_ramp' 
    WHEN days_span <= 140 THEN 'slow_ramp'
    ELSE 'very_slow_ramp'
  END as ramp_speed,
  COUNT(*) as n,
  AVG(paid_retention_rate_month) as avg_prr,
  AVG(paid_retained_month_count) as avg_prm,
  AVG(email_open_rate) as avg_open,
  AVG(count_placed_order) as avg_orders
FROM klaviyo__persons
GROUP BY ramp_speed
ORDER BY ramp_speed
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-095/attempt-01/sql/S20.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-095/attempt-01/sql/S20.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-095/attempt-01/results/S20.rows.jsonl)；完整：True；SHA256：`42a63eb828a2ad78aecc6898db0d6a3fda5673b0c680a48fce0e7f62963456e6`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "klaviyo__persons", "kind": "base", "block": null, "base_tables": ["klaviyo__persons"]}] | [] | ["CASE WHEN days_span <= 60 THEN 'fast_ramp' WHEN days_span <= 100 THEN 'medium_ramp' WHEN days_span <= 140 THEN 'slow_ramp' ELSE 'very_slow_ramp' END"] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |
| B1 | AVG(paid_retention_rate_month) | [{"table": "klaviyo__persons", "column": "paid_retention_rate_month"}] | [] | False |
| B1 | AVG(paid_retained_month_count) | [{"table": "klaviyo__persons", "column": "paid_retained_month_count"}] | [] | False |
| B1 | AVG(email_open_rate) | [{"table": "klaviyo__persons", "column": "email_open_rate"}] | [] | False |
| B1 | AVG(count_placed_order) | [{"table": "klaviyo__persons", "column": "count_placed_order"}] | [] | False |


## S21

类别 `data`；来源 `query_db`；调用 `21e11b5fb48b4c79af3c569c8deca951`；状态 `failed`。

```sql
SELECT 
  CASE 
    WHEN email_open_rate >= 0.5 THEN 'high_open'
    WHEN email_open_rate >= 0.3 THEN 'medium_open'
    ELSE 'low_open'
  END as open_segment,
  COUNT(*) as n,
  AVG(paid_retention_rate_month) as avg_prr,
  AVG(paid_retained_month_count) as avg_prm,
  AVG(days_span) as avg_ds,
  AVG(count_placed_order) as avg_orders,
  AVG(has_converted) as avg_converted
FROM klaviyo__persons
GROUP BY open_segment
ORDER BY avg_prr DESC
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-095/attempt-01/sql/S21.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-095/attempt-01/sql/S21.parameters.json)。

错误：`OperationalError('no such column: has_converted')`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "klaviyo__persons", "kind": "base", "block": null, "base_tables": ["klaviyo__persons"]}] | [] | ["CASE WHEN email_open_rate >= 0.5 THEN 'high_open' WHEN email_open_rate >= 0.3 THEN 'medium_open' ELSE 'low_open' END"] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |
| B1 | AVG(paid_retention_rate_month) | [{"table": "klaviyo__persons", "column": "paid_retention_rate_month"}] | [] | False |
| B1 | AVG(paid_retained_month_count) | [{"table": "klaviyo__persons", "column": "paid_retained_month_count"}] | [] | False |
| B1 | AVG(days_span) | [{"table": "klaviyo__persons", "column": "days_span"}] | [] | False |
| B1 | AVG(count_placed_order) | [{"table": "klaviyo__persons", "column": "count_placed_order"}] | [] | False |
| B1 | AVG(has_converted) | [{"unknown": "has_converted"}] | [] | False |


未解析列血缘：[{"block": "B1", "column": "has_converted", "reason": "ambiguous_or_missing_source"}, {"block": "B1", "column": "has_converted", "reason": "ambiguous_or_missing_source"}]

## S22

类别 `data`；来源 `query_db`；调用 `a53d8b7cf2534ba58645c7c0018d316f`；状态 `success`。

```sql
SELECT 
  months_span - active_months as inactive_months,
  COUNT(*) as n,
  AVG(paid_retention_rate_month) as avg_prr,
  AVG(days_span) as avg_ds
FROM klaviyo__persons
GROUP BY inactive_months
ORDER BY inactive_months
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-095/attempt-01/sql/S22.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-095/attempt-01/sql/S22.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-095/attempt-01/results/S22.rows.jsonl)；完整：True；SHA256：`fc3681dd895e6d8e3d67ba33331732877c02b3d84478f2345727c78597cf54e7`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "klaviyo__persons", "kind": "base", "block": null, "base_tables": ["klaviyo__persons"]}] | [] | ["months_span - active_months"] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |
| B1 | AVG(paid_retention_rate_month) | [{"table": "klaviyo__persons", "column": "paid_retention_rate_month"}] | [] | False |
| B1 | AVG(days_span) | [{"table": "klaviyo__persons", "column": "days_span"}] | [] | False |


## S23

类别 `data`；来源 `query_db`；调用 `3967827c5d9c4ee6bd319682522195c6`；状态 `failed`。

```sql
SELECT 
  CASE 
    WHEN count_received_email <= 50 THEN 'low_freq'
    WHEN count_received_email <= 70 THEN 'med_freq'
    WHEN count_received_email <= 90 THEN 'high_freq'
    ELSE 'very_high_freq'
  END as freq_segment,
  COUNT(*) as n,
  AVG(paid_retention_rate_month) as avg_prr,
  AVG(paid_retained_month_count) as avg_prm,
  AVG(count_placed_order) as avg_orders,
  AVG(email_open_rate) as avg_open,
  AVG(count_unsubscribed) as avg_unsub
FROM klaviyo__persons
GROUP BY freq_segment
ORDER BY avg_orders DESC
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-095/attempt-01/sql/S23.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-095/attempt-01/sql/S23.parameters.json)。

错误：`OperationalError('no such column: count_unsubscribed')`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "klaviyo__persons", "kind": "base", "block": null, "base_tables": ["klaviyo__persons"]}] | [] | ["CASE WHEN count_received_email <= 50 THEN 'low_freq' WHEN count_received_email <= 70 THEN 'med_freq' WHEN count_received_email <= 90 THEN 'high_freq' ELSE 'very_high_freq' END"] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |
| B1 | AVG(paid_retention_rate_month) | [{"table": "klaviyo__persons", "column": "paid_retention_rate_month"}] | [] | False |
| B1 | AVG(paid_retained_month_count) | [{"table": "klaviyo__persons", "column": "paid_retained_month_count"}] | [] | False |
| B1 | AVG(count_placed_order) | [{"table": "klaviyo__persons", "column": "count_placed_order"}] | [] | False |
| B1 | AVG(email_open_rate) | [{"table": "klaviyo__persons", "column": "email_open_rate"}] | [] | False |
| B1 | AVG(count_unsubscribed) | [{"unknown": "count_unsubscribed"}] | [] | False |


未解析列血缘：[{"block": "B1", "column": "count_unsubscribed", "reason": "ambiguous_or_missing_source"}, {"block": "B1", "column": "count_unsubscribed", "reason": "ambiguous_or_missing_source"}]

## S24

类别 `data`；来源 `query_db`；调用 `e1e6daf48fdc4fb99271b5f51c7fcc9f`；状态 `success`。

```sql
SELECT 
  CASE 
    WHEN count_clicked_email = 0 THEN 'no_clicks'
    WHEN count_clicked_email <= 5 THEN 'few_clicks'
    WHEN count_clicked_email <= 10 THEN 'some_clicks'
    ELSE 'many_clicks'
  END as click_segment,
  COUNT(*) as n,
  AVG(paid_retention_rate_month) as avg_prr,
  AVG(count_placed_order) as avg_orders,
  AVG(email_open_rate) as avg_open
FROM klaviyo__persons
GROUP BY click_segment
ORDER BY avg_orders DESC
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-095/attempt-01/sql/S24.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-095/attempt-01/sql/S24.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-095/attempt-01/results/S24.rows.jsonl)；完整：True；SHA256：`467407afa2ad05936fe160083a983a6d42e6262f2db989f93ff8c9dfc9bc76d1`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "klaviyo__persons", "kind": "base", "block": null, "base_tables": ["klaviyo__persons"]}] | [] | ["CASE WHEN count_clicked_email = 0 THEN 'no_clicks' WHEN count_clicked_email <= 5 THEN 'few_clicks' WHEN count_clicked_email <= 10 THEN 'some_clicks' ELSE 'many_clicks' END"] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |
| B1 | AVG(paid_retention_rate_month) | [{"table": "klaviyo__persons", "column": "paid_retention_rate_month"}] | [] | False |
| B1 | AVG(count_placed_order) | [{"table": "klaviyo__persons", "column": "count_placed_order"}] | [] | False |
| B1 | AVG(email_open_rate) | [{"table": "klaviyo__persons", "column": "email_open_rate"}] | [] | False |


## S25

类别 `data`；来源 `query_db`；调用 `5670cf63805447c8a4ae107c90f2be90`；状态 `success`。

```sql
SELECT 
  CASE 
    WHEN count_received_email <= 50 THEN 'low_freq'
    WHEN count_received_email <= 70 THEN 'med_freq'
    WHEN count_received_email <= 90 THEN 'high_freq'
    ELSE 'very_high_freq'
  END as freq_segment,
  COUNT(*) as n,
  AVG(paid_retention_rate_month) as avg_prr,
  AVG(paid_retained_month_count) as avg_prm,
  AVG(count_placed_order) as avg_orders,
  AVG(email_open_rate) as avg_open
FROM klaviyo__persons
GROUP BY freq_segment
ORDER BY avg_orders DESC
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-095/attempt-01/sql/S25.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-095/attempt-01/sql/S25.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-095/attempt-01/results/S25.rows.jsonl)；完整：True；SHA256：`00220a4ba2588c6d2373221fb372936fb5c6c0ac95ad2e900301eacd6990e693`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "klaviyo__persons", "kind": "base", "block": null, "base_tables": ["klaviyo__persons"]}] | [] | ["CASE WHEN count_received_email <= 50 THEN 'low_freq' WHEN count_received_email <= 70 THEN 'med_freq' WHEN count_received_email <= 90 THEN 'high_freq' ELSE 'very_high_freq' END"] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |
| B1 | AVG(paid_retention_rate_month) | [{"table": "klaviyo__persons", "column": "paid_retention_rate_month"}] | [] | False |
| B1 | AVG(paid_retained_month_count) | [{"table": "klaviyo__persons", "column": "paid_retained_month_count"}] | [] | False |
| B1 | AVG(count_placed_order) | [{"table": "klaviyo__persons", "column": "count_placed_order"}] | [] | False |
| B1 | AVG(email_open_rate) | [{"table": "klaviyo__persons", "column": "email_open_rate"}] | [] | False |


## S26

类别 `data`；来源 `query_db`；调用 `0e86174a5d124e779b54404da3c99de2`；状态 `success`。

```sql
SELECT 
  active_months,
  AVG(count_placed_order) as avg_orders,
  AVG(count_received_email) as avg_emails,
  AVG(count_opened_email) as avg_opens,
  AVG(count_clicked_email) as avg_clicks,
  AVG(email_open_rate) as avg_open_rate,
  AVG(days_span) as avg_days_span,
  AVG(paid_retention_rate_month) as avg_prr
FROM klaviyo__persons
GROUP BY active_months
ORDER BY active_months
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-095/attempt-01/sql/S26.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-095/attempt-01/sql/S26.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-095/attempt-01/results/S26.rows.jsonl)；完整：True；SHA256：`486efd47e74c0264f7f1b082362082974991aba9e88c70fa71572be7cde00ac6`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "klaviyo__persons", "kind": "base", "block": null, "base_tables": ["klaviyo__persons"]}] | [] | ["active_months"] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | AVG(count_placed_order) | [{"table": "klaviyo__persons", "column": "count_placed_order"}] | [] | False |
| B1 | AVG(count_received_email) | [{"table": "klaviyo__persons", "column": "count_received_email"}] | [] | False |
| B1 | AVG(count_opened_email) | [{"table": "klaviyo__persons", "column": "count_opened_email"}] | [] | False |
| B1 | AVG(count_clicked_email) | [{"table": "klaviyo__persons", "column": "count_clicked_email"}] | [] | False |
| B1 | AVG(email_open_rate) | [{"table": "klaviyo__persons", "column": "email_open_rate"}] | [] | False |
| B1 | AVG(days_span) | [{"table": "klaviyo__persons", "column": "days_span"}] | [] | False |
| B1 | AVG(paid_retention_rate_month) | [{"table": "klaviyo__persons", "column": "paid_retention_rate_month"}] | [] | False |


## S27

类别 `data`；来源 `query_db`；调用 `f49f01e88b8245cabe15608b75b3ec9e`；状态 `success`。

```sql
SELECT 
  CAMPAIGN_TYPE,
  COUNT(*) as n_campaigns,
  AVG(email_open_rate) as avg_open_rate,
  AVG(email_click_to_open_rate) as avg_ctr,
  AVG(total_count_unique_people) as avg_audience,
  AVG(count_placed_order) as avg_orders,
  AVG(gmv_net) as avg_gmv_net,
  AVG(count_clicked_email) as avg_clicks,
  AVG(count_received_email) as avg_received
FROM klaviyo__campaigns
GROUP BY CAMPAIGN_TYPE
ORDER BY avg_gmv_net DESC
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-095/attempt-01/sql/S27.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-095/attempt-01/sql/S27.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-095/attempt-01/results/S27.rows.jsonl)；完整：True；SHA256：`28d7b513d85b6d943856feac01d76c51fc843f50319efda315108d38771f6190`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "klaviyo__campaigns", "kind": "base", "block": null, "base_tables": ["klaviyo__campaigns"]}] | [] | ["CAMPAIGN_TYPE"] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |
| B1 | AVG(email_open_rate) | [{"table": "klaviyo__campaigns", "column": "email_open_rate"}] | [] | False |
| B1 | AVG(email_click_to_open_rate) | [{"table": "klaviyo__campaigns", "column": "email_click_to_open_rate"}] | [] | False |
| B1 | AVG(total_count_unique_people) | [{"table": "klaviyo__campaigns", "column": "total_count_unique_people"}] | [] | False |
| B1 | AVG(count_placed_order) | [{"table": "klaviyo__campaigns", "column": "count_placed_order"}] | [] | False |
| B1 | AVG(gmv_net) | [{"table": "klaviyo__campaigns", "column": "gmv_net"}] | [] | False |
| B1 | AVG(count_clicked_email) | [{"table": "klaviyo__campaigns", "column": "count_clicked_email"}] | [] | False |
| B1 | AVG(count_received_email) | [{"table": "klaviyo__campaigns", "column": "count_received_email"}] | [] | False |


## S28

类别 `data`；来源 `query_db`；调用 `12d6f5a39abc406b8f3b362a465457d6`；状态 `success`。

```sql
SELECT 
  trigger_type,
  COUNT(*) as n_flows,
  AVG(email_open_rate) as avg_open_rate,
  AVG(email_click_to_open_rate) as avg_ctr,
  AVG(total_count_unique_people) as avg_audience,
  AVG(count_placed_order) as avg_orders,
  AVG(gmv_net) as avg_gmv_net
FROM klaviyo__flows
GROUP BY trigger_type
ORDER BY avg_gmv_net DESC
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-095/attempt-01/sql/S28.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-095/attempt-01/sql/S28.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-095/attempt-01/results/S28.rows.jsonl)；完整：True；SHA256：`f77153fe9b9a60465a4c7d73e78437ea913c3177ca76b7518aabb6cc46630857`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "klaviyo__flows", "kind": "base", "block": null, "base_tables": ["klaviyo__flows"]}] | [] | ["trigger_type"] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |
| B1 | AVG(email_open_rate) | [{"table": "klaviyo__flows", "column": "email_open_rate"}] | [] | False |
| B1 | AVG(email_click_to_open_rate) | [{"table": "klaviyo__flows", "column": "email_click_to_open_rate"}] | [] | False |
| B1 | AVG(total_count_unique_people) | [{"table": "klaviyo__flows", "column": "total_count_unique_people"}] | [] | False |
| B1 | AVG(count_placed_order) | [{"table": "klaviyo__flows", "column": "count_placed_order"}] | [] | False |
| B1 | AVG(gmv_net) | [{"table": "klaviyo__flows", "column": "gmv_net"}] | [] | False |


## S29

类别 `data`；来源 `query_db`；调用 `b748b6b7aae74fabba37dc401751eb11`；状态 `success`。

```sql
SELECT 
  CASE 
    WHEN active_months <= 2 THEN 'Cold Start'
    WHEN active_months = 3 THEN 'Growth'
    WHEN active_months = 4 THEN 'Mature'
    ELSE 'Peak'
  END as lifecycle_stage,
  COUNT(*) as n_persons,
  AVG(days_span) as avg_days_span,
  AVG(active_months) as avg_active_months,
  AVG(paid_retained_month_count) as avg_paid_retained_months,
  AVG(paid_retention_rate_month) as avg_paid_retention_rate,
  AVG(count_placed_order) as avg_orders,
  AVG(sum_revenue_placed_order) as avg_revenue,
  AVG(email_open_rate) as avg_open_rate,
  AVG(count_received_email) as avg_emails_received,
  AVG(count_clicked_email) as avg_clicks,
  AVG(active_retention_rate_month) as avg_active_ret_rate
FROM klaviyo__persons
GROUP BY lifecycle_stage
ORDER BY avg_active_months
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-095/attempt-01/sql/S29.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-095/attempt-01/sql/S29.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-095/attempt-01/results/S29.rows.jsonl)；完整：True；SHA256：`e30896a04930b8912109e7a559930bf111e78b388cb75d923b6f450ed72acc3a`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "klaviyo__persons", "kind": "base", "block": null, "base_tables": ["klaviyo__persons"]}] | [] | ["CASE WHEN active_months <= 2 THEN 'Cold Start' WHEN active_months = 3 THEN 'Growth' WHEN active_months = 4 THEN 'Mature' ELSE 'Peak' END"] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |
| B1 | AVG(days_span) | [{"table": "klaviyo__persons", "column": "days_span"}] | [] | False |
| B1 | AVG(active_months) | [{"table": "klaviyo__persons", "column": "active_months"}] | [] | False |
| B1 | AVG(paid_retained_month_count) | [{"table": "klaviyo__persons", "column": "paid_retained_month_count"}] | [] | False |
| B1 | AVG(paid_retention_rate_month) | [{"table": "klaviyo__persons", "column": "paid_retention_rate_month"}] | [] | False |
| B1 | AVG(count_placed_order) | [{"table": "klaviyo__persons", "column": "count_placed_order"}] | [] | False |
| B1 | AVG(sum_revenue_placed_order) | [{"table": "klaviyo__persons", "column": "sum_revenue_placed_order"}] | [] | False |
| B1 | AVG(email_open_rate) | [{"table": "klaviyo__persons", "column": "email_open_rate"}] | [] | False |
| B1 | AVG(count_received_email) | [{"table": "klaviyo__persons", "column": "count_received_email"}] | [] | False |
| B1 | AVG(count_clicked_email) | [{"table": "klaviyo__persons", "column": "count_clicked_email"}] | [] | False |
| B1 | AVG(active_retention_rate_month) | [{"table": "klaviyo__persons", "column": "active_retention_rate_month"}] | [] | False |


## S30

类别 `data`；来源 `query_db`；调用 `9316e3fffdca43e79ed91bd6b60ee4be`；状态 `success`。

```sql
WITH at_risk AS (
  SELECT *, 
    CASE WHEN paid_retention_rate_month < 1.0 THEN 'At_Risk_Winback' ELSE 'Retained' END as ret_segment
  FROM klaviyo__persons
)
SELECT 
  ret_segment,
  lifecycle_stage,
  COUNT(*) as n,
  AVG(count_placed_order) as avg_orders,
  AVG(sum_revenue_placed_order) as avg_revenue,
  AVG(email_open_rate) as avg_open,
  AVG(count_received_email) as avg_emails
FROM (
  SELECT *,
    CASE 
      WHEN active_months <= 2 THEN 'Cold Start'
      WHEN active_months = 3 THEN 'Growth'
      WHEN active_months = 4 THEN 'Mature'
      ELSE 'Peak'
    END as lifecycle_stage,
    CASE WHEN paid_retention_rate_month < 1.0 THEN 'At_Risk_Winback' ELSE 'Retained' END as ret_segment
  FROM klaviyo__persons
) sub
GROUP BY ret_segment, lifecycle_stage
ORDER BY lifecycle_stage, ret_segment
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-095/attempt-01/sql/S30.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-095/attempt-01/sql/S30.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-095/attempt-01/results/S30.rows.jsonl)；完整：True；SHA256：`d4e68a3380c77e50f7f42071ca4e0350a8dd089a68d77ded5b6f304f443bf847`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "klaviyo__persons", "kind": "base", "block": null, "base_tables": ["klaviyo__persons"]}] | [] | [] |
| B2 | [{"alias": "klaviyo__persons", "kind": "base", "block": null, "base_tables": ["klaviyo__persons"]}] | [] | [] |
| B3 | [{"alias": "sub", "kind": "derived", "block": "B2", "base_tables": ["klaviyo__persons"]}] | [] | ["ret_segment", "lifecycle_stage"] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B3 | COUNT(*) | [] | [] | True |
| B3 | AVG(count_placed_order) | [{"table": "klaviyo__persons", "column": "count_placed_order"}] | [] | False |
| B3 | AVG(sum_revenue_placed_order) | [{"table": "klaviyo__persons", "column": "sum_revenue_placed_order"}] | [] | False |
| B3 | AVG(email_open_rate) | [{"table": "klaviyo__persons", "column": "email_open_rate"}] | [] | False |
| B3 | AVG(count_received_email) | [{"table": "klaviyo__persons", "column": "count_received_email"}] | [] | False |


## S31

类别 `data`；来源 `query_db`；调用 `0f05dfa81da4490691495f64d242d624`；状态 `success`。

```sql
WITH speed_tiers AS (
  SELECT *,
    active_days * 1.0 / days_span as activity_density,
    months_span - active_months as gap_months,
    CASE 
      WHEN active_days * 1.0 / days_span >= 0.95 THEN 'Very High Density'
      WHEN active_days * 1.0 / days_span >= 0.85 THEN 'High Density'
      WHEN active_days * 1.0 / days_span >= 0.75 THEN 'Medium Density'
      ELSE 'Low Density'
    END as density_segment
  FROM klaviyo__persons
)
SELECT 
  density_segment,
  COUNT(*) as n,
  AVG(activity_density) as avg_density,
  AVG(paid_retention_rate_month) as avg_prr,
  AVG(paid_retained_month_count) as avg_prm,
  AVG(count_placed_order) as avg_orders,
  AVG(sum_revenue_placed_order) as avg_revenue,
  AVG(email_open_rate) as avg_open,
  AVG(days_span) as avg_days_span,
  AVG(active_months) as avg_active_months
FROM speed_tiers
GROUP BY density_segment
ORDER BY avg_density DESC
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-095/attempt-01/sql/S31.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-095/attempt-01/sql/S31.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-095/attempt-01/results/S31.rows.jsonl)；完整：True；SHA256：`7caefc61e7078303e524a2d99f307928ca6cf9af1ad9d78b3cee9366e584c6e4`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "klaviyo__persons", "kind": "base", "block": null, "base_tables": ["klaviyo__persons"]}] | [] | [] |
| B2 | [{"alias": "speed_tiers", "kind": "derived", "block": "B1", "base_tables": ["klaviyo__persons"]}] | [] | ["density_segment"] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B2 | COUNT(*) | [] | [] | True |
| B2 | AVG(activity_density) | [{"table": "klaviyo__persons", "column": "days_span"}, {"table": "klaviyo__persons", "column": "active_days"}] | [] | False |
| B2 | AVG(paid_retention_rate_month) | [{"table": "klaviyo__persons", "column": "paid_retention_rate_month"}] | [] | False |
| B2 | AVG(paid_retained_month_count) | [{"table": "klaviyo__persons", "column": "paid_retained_month_count"}] | [] | False |
| B2 | AVG(count_placed_order) | [{"table": "klaviyo__persons", "column": "count_placed_order"}] | [] | False |
| B2 | AVG(sum_revenue_placed_order) | [{"table": "klaviyo__persons", "column": "sum_revenue_placed_order"}] | [] | False |
| B2 | AVG(email_open_rate) | [{"table": "klaviyo__persons", "column": "email_open_rate"}] | [] | False |
| B2 | AVG(days_span) | [{"table": "klaviyo__persons", "column": "days_span"}] | [] | False |
| B2 | AVG(active_months) | [{"table": "klaviyo__persons", "column": "active_months"}] | [] | False |


## S32

类别 `data`；来源 `query_db`；调用 `5ff2a35bfdee47c58e7c450f1afd22ed`；状态 `success`。

```sql
SELECT * FROM klaviyo__person_campaign_flow
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-095/attempt-01/sql/S32.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-095/attempt-01/sql/S32.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-095/attempt-01/results/S32.rows.jsonl)；完整：True；SHA256：`85f76e3e10a894a658042a15b78bc4ba0c89e3579936b7e84447e8df8337de90`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "klaviyo__person_campaign_flow", "kind": "base", "block": null, "base_tables": ["klaviyo__person_campaign_flow"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |


## S33

类别 `data`；来源 `query_db`；调用 `a4771cf356494ead8bf50bff43e8cda3`；状态 `success`。

```sql
SELECT 
  CAMPAIGN_TYPE,
  MIN(scheduled_to_send_at) as first_sent,
  MAX(scheduled_to_send_at) as last_sent,
  AVG(CASE WHEN count_placed_order > 0 THEN 1.0 ELSE 0 END) as conversion_rate
FROM klaviyo__campaigns
GROUP BY CAMPAIGN_TYPE
ORDER BY first_sent
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-095/attempt-01/sql/S33.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-095/attempt-01/sql/S33.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-095/attempt-01/results/S33.rows.jsonl)；完整：True；SHA256：`41215ffbf86199448930207faee389afc43792f1941383eda2ec571b6dfc9f3a`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "klaviyo__campaigns", "kind": "base", "block": null, "base_tables": ["klaviyo__campaigns"]}] | [] | ["CAMPAIGN_TYPE"] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | MIN(scheduled_to_send_at) | [{"table": "klaviyo__campaigns", "column": "scheduled_to_send_at"}] | [] | False |
| B1 | MAX(scheduled_to_send_at) | [{"table": "klaviyo__campaigns", "column": "scheduled_to_send_at"}] | [] | False |
| B1 | AVG(CASE WHEN count_placed_order > 0 THEN 1.0 ELSE 0 END) | [] | [{"table": "klaviyo__campaigns", "column": "count_placed_order"}] | False |


## S34

类别 `data`；来源 `query_db`；调用 `3a70aa29f11f40288152e5c40c0a11f2`；状态 `success`。

```sql
SELECT 
  CAMPAIGN_TYPE,
  AVG(count_placed_order / NULLIF(count_received_email, 0)) as orders_per_received,
  AVG(count_opened_email / NULLIF(count_received_email, 0)) as open_per_received,
  AVG(count_clicked_email / NULLIF(count_received_email, 0)) as click_per_received,
  AVG(gmv_net / NULLIF(count_received_email, 0)) as gmv_per_received,
  AVG(gmv_net / NULLIF(count_placed_order, 0)) as aov
FROM klaviyo__campaigns
GROUP BY CAMPAIGN_TYPE
ORDER BY gmv_per_received DESC
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-095/attempt-01/sql/S34.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-095/attempt-01/sql/S34.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-095/attempt-01/results/S34.rows.jsonl)；完整：True；SHA256：`e43c0d771bfb30c7eeff4f547ae566bbb515079dab73c737bf9774802300768b`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "klaviyo__campaigns", "kind": "base", "block": null, "base_tables": ["klaviyo__campaigns"]}] | [] | ["CAMPAIGN_TYPE"] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | AVG(count_placed_order / NULLIF(count_received_email, 0)) | [{"table": "klaviyo__campaigns", "column": "count_placed_order"}, {"table": "klaviyo__campaigns", "column": "count_received_email"}] | [] | False |
| B1 | AVG(count_opened_email / NULLIF(count_received_email, 0)) | [{"table": "klaviyo__campaigns", "column": "count_opened_email"}, {"table": "klaviyo__campaigns", "column": "count_received_email"}] | [] | False |
| B1 | AVG(count_clicked_email / NULLIF(count_received_email, 0)) | [{"table": "klaviyo__campaigns", "column": "count_clicked_email"}, {"table": "klaviyo__campaigns", "column": "count_received_email"}] | [] | False |
| B1 | AVG(gmv_net / NULLIF(count_received_email, 0)) | [{"table": "klaviyo__campaigns", "column": "gmv_net"}, {"table": "klaviyo__campaigns", "column": "count_received_email"}] | [] | False |
| B1 | AVG(gmv_net / NULLIF(count_placed_order, 0)) | [{"table": "klaviyo__campaigns", "column": "gmv_net"}, {"table": "klaviyo__campaigns", "column": "count_placed_order"}] | [] | False |


## S35

类别 `data`；来源 `query_db`；调用 `d4af4355b39a4a9eb739cc7bb286c32d`；状态 `success`。

```sql
SELECT pcf.person_id, pcf.last_touch_campaign_id, c.CAMPAIGN_TYPE, pcf.has_converted, pcf.email_open_rate_touch, pcf.email_click_to_open_rate_touch, pcf.net_revenue_touch
FROM klaviyo__person_campaign_flow pcf
LEFT JOIN klaviyo__campaigns c ON pcf.last_touch_campaign_id = c.campaign_id
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-095/attempt-01/sql/S35.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-095/attempt-01/sql/S35.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-095/attempt-01/results/S35.rows.jsonl)；完整：True；SHA256：`d769c4819f3a31f3b42b5abec64faf742d9d977b1eaf546bf5a05a8cc8955b1a`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "pcf", "kind": "base", "block": null, "base_tables": ["klaviyo__person_campaign_flow"]}, {"alias": "c", "kind": "base", "block": null, "base_tables": ["klaviyo__campaigns"]}] | [{"type": "LEFT", "right": "klaviyo__campaigns AS c", "on": "pcf.last_touch_campaign_id = c.campaign_id", "using": []}] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |


## S36

类别 `data`；来源 `query_db`；调用 `a8664de1c8ef4809a7e9224c4b67d7d5`；状态 `success`。

```sql
SELECT 
  CASE 
    WHEN days_span <= 60 THEN 'Fast (≤60d)'
    WHEN days_span <= 90 THEN 'Medium (61-90d)'
    WHEN days_span <= 120 THEN 'Slow (91-120d)'
    ELSE 'Very Slow (>120d)'
  END as speed_group,
  COUNT(*) as n,
  AVG(paid_retention_rate_month) as avg_prr,
  AVG(paid_retained_month_count) as avg_prm,
  AVG(count_placed_order) as avg_orders,
  AVG(sum_revenue_placed_order) as avg_revenue,
  AVG(email_open_rate) as avg_open,
  AVG(count_received_email) as avg_emails,
  AVG(active_days * 1.0 / days_span) as avg_density
FROM klaviyo__persons
GROUP BY speed_group
ORDER BY speed_group
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-095/attempt-01/sql/S36.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-095/attempt-01/sql/S36.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-095/attempt-01/results/S36.rows.jsonl)；完整：True；SHA256：`20b9c97d2553b234338d75dce0017e3457503490e5e0071dadebe79e2089f8d1`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "klaviyo__persons", "kind": "base", "block": null, "base_tables": ["klaviyo__persons"]}] | [] | ["CASE WHEN days_span <= 60 THEN 'Fast (≤60d)' WHEN days_span <= 90 THEN 'Medium (61-90d)' WHEN days_span <= 120 THEN 'Slow (91-120d)' ELSE 'Very Slow (>120d)' END"] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |
| B1 | AVG(paid_retention_rate_month) | [{"table": "klaviyo__persons", "column": "paid_retention_rate_month"}] | [] | False |
| B1 | AVG(paid_retained_month_count) | [{"table": "klaviyo__persons", "column": "paid_retained_month_count"}] | [] | False |
| B1 | AVG(count_placed_order) | [{"table": "klaviyo__persons", "column": "count_placed_order"}] | [] | False |
| B1 | AVG(sum_revenue_placed_order) | [{"table": "klaviyo__persons", "column": "sum_revenue_placed_order"}] | [] | False |
| B1 | AVG(email_open_rate) | [{"table": "klaviyo__persons", "column": "email_open_rate"}] | [] | False |
| B1 | AVG(count_received_email) | [{"table": "klaviyo__persons", "column": "count_received_email"}] | [] | False |
| B1 | AVG(active_days * 1.0 / days_span) | [{"table": "klaviyo__persons", "column": "days_span"}, {"table": "klaviyo__persons", "column": "active_days"}] | [] | False |


## S37

类别 `data`；来源 `query_db`；调用 `659c934080124a83b0ae8b128f4550c1`；状态 `failed`。

```sql
SELECT 
  CASE 
    WHEN count_placed_order = 0 THEN 'No Orders'
    WHEN count_placed_order = 1 THEN '1 Order'
    WHEN count_placed_order <= 3 THEN '2-3 Orders'
    ELSE '4+ Orders'
  END as order_tier,
  COUNT(*) as n,
  AVG(days_span) as avg_days_span,
  AVG(active_months) as avg_am,
  AVG(email_open_rate) as avg_open,
  AVG(count_received_email) as avg_emails,
  AVG(paid_retention_rate_month) as avg_prr
FROM klaviyo__persons
GROUP BY order_tier
ORDER BY avg_orders DESC
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-095/attempt-01/sql/S37.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-095/attempt-01/sql/S37.parameters.json)。

错误：`OperationalError('no such column: avg_orders')`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "klaviyo__persons", "kind": "base", "block": null, "base_tables": ["klaviyo__persons"]}] | [] | ["CASE WHEN count_placed_order = 0 THEN 'No Orders' WHEN count_placed_order = 1 THEN '1 Order' WHEN count_placed_order <= 3 THEN '2-3 Orders' ELSE '4+ Orders' END"] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |
| B1 | AVG(days_span) | [{"table": "klaviyo__persons", "column": "days_span"}] | [] | False |
| B1 | AVG(active_months) | [{"table": "klaviyo__persons", "column": "active_months"}] | [] | False |
| B1 | AVG(email_open_rate) | [{"table": "klaviyo__persons", "column": "email_open_rate"}] | [] | False |
| B1 | AVG(count_received_email) | [{"table": "klaviyo__persons", "column": "count_received_email"}] | [] | False |
| B1 | AVG(paid_retention_rate_month) | [{"table": "klaviyo__persons", "column": "paid_retention_rate_month"}] | [] | False |


未解析列血缘：[{"block": "B1", "column": "avg_orders", "reason": "ambiguous_or_missing_source"}]

## S38

类别 `data`；来源 `query_db`；调用 `3f7d691135134f84ae6f1bc4573b4da6`；状态 `success`。

```sql
SELECT 
  CASE 
    WHEN count_placed_order = 0 THEN 'No Orders'
    WHEN count_placed_order = 1 THEN '1 Order'
    WHEN count_placed_order <= 3 THEN '2-3 Orders'
    ELSE '4+ Orders'
  END as order_tier,
  COUNT(*) as n,
  AVG(days_span) as avg_days_span,
  AVG(active_months) as avg_am,
  AVG(email_open_rate) as avg_open,
  AVG(count_received_email) as avg_emails,
  AVG(paid_retention_rate_month) as avg_prr,
  AVG(count_clicked_email) as avg_clicks
FROM klaviyo__persons
GROUP BY order_tier
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-095/attempt-01/sql/S38.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-095/attempt-01/sql/S38.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-095/attempt-01/results/S38.rows.jsonl)；完整：True；SHA256：`aff9be21d0b02218ffdea4a3fa4bc7366ad9496e3fd54e557c7da021665f1bf7`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "klaviyo__persons", "kind": "base", "block": null, "base_tables": ["klaviyo__persons"]}] | [] | ["CASE WHEN count_placed_order = 0 THEN 'No Orders' WHEN count_placed_order = 1 THEN '1 Order' WHEN count_placed_order <= 3 THEN '2-3 Orders' ELSE '4+ Orders' END"] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |
| B1 | AVG(days_span) | [{"table": "klaviyo__persons", "column": "days_span"}] | [] | False |
| B1 | AVG(active_months) | [{"table": "klaviyo__persons", "column": "active_months"}] | [] | False |
| B1 | AVG(email_open_rate) | [{"table": "klaviyo__persons", "column": "email_open_rate"}] | [] | False |
| B1 | AVG(count_received_email) | [{"table": "klaviyo__persons", "column": "count_received_email"}] | [] | False |
| B1 | AVG(paid_retention_rate_month) | [{"table": "klaviyo__persons", "column": "paid_retention_rate_month"}] | [] | False |
| B1 | AVG(count_clicked_email) | [{"table": "klaviyo__persons", "column": "count_clicked_email"}] | [] | False |


## S39

类别 `data`；来源 `query_db`；调用 `21c6f7f6905d4e11a6519e19c940773e`；状态 `success`。

```sql
SELECT 
  has_converted,
  AVG(email_open_rate_touch) as avg_open_touch,
  AVG(email_click_to_open_rate_touch) as avg_ctr_touch,
  AVG(touch_span_days) as avg_touch_span,
  AVG(count_received_email) as avg_emails,
  AVG(net_revenue_touch) as avg_net_rev
FROM klaviyo__person_campaign_flow
GROUP BY has_converted
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-095/attempt-01/sql/S39.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-095/attempt-01/sql/S39.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-095/attempt-01/results/S39.rows.jsonl)；完整：True；SHA256：`665c980f31ad15ee9e5c25cc3d0cc54bf25a00ce7213d4a629c6466e8dc3d627`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "klaviyo__person_campaign_flow", "kind": "base", "block": null, "base_tables": ["klaviyo__person_campaign_flow"]}] | [] | ["has_converted"] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | AVG(email_open_rate_touch) | [{"table": "klaviyo__person_campaign_flow", "column": "email_open_rate_touch"}] | [] | False |
| B1 | AVG(email_click_to_open_rate_touch) | [{"table": "klaviyo__person_campaign_flow", "column": "email_click_to_open_rate_touch"}] | [] | False |
| B1 | AVG(touch_span_days) | [{"table": "klaviyo__person_campaign_flow", "column": "touch_span_days"}] | [] | False |
| B1 | AVG(count_received_email) | [{"table": "klaviyo__person_campaign_flow", "column": "count_received_email"}] | [] | False |
| B1 | AVG(net_revenue_touch) | [{"table": "klaviyo__person_campaign_flow", "column": "net_revenue_touch"}] | [] | False |


## S40

类别 `data`；来源 `query_db`；调用 `9f80f1ed618e4b3ab29182675b5a4806`；状态 `success`。

```sql
SELECT 
  campaign_variation_key,
  COUNT(*) as n,
  AVG(email_open_rate) as avg_open,
  AVG(gmv_net) as avg_gmv
FROM klaviyo__campaigns
GROUP BY campaign_variation_key
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-095/attempt-01/sql/S40.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-095/attempt-01/sql/S40.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-095/attempt-01/results/S40.rows.jsonl)；完整：True；SHA256：`85e1f37a95853003123e9d0eedad12ee051cebf689bea477c75cf60ba649530a`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "klaviyo__campaigns", "kind": "base", "block": null, "base_tables": ["klaviyo__campaigns"]}] | [] | ["campaign_variation_key"] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |
| B1 | AVG(email_open_rate) | [{"table": "klaviyo__campaigns", "column": "email_open_rate"}] | [] | False |
| B1 | AVG(gmv_net) | [{"table": "klaviyo__campaigns", "column": "gmv_net"}] | [] | False |


## S41

类别 `data`；来源 `query_db`；调用 `73c0d459d1aa420dae1516893480ba54`；状态 `success`。

```sql
SELECT 
  strftime('%Y-%m', scheduled_to_send_at) as month,
  COUNT(*) as n_campaigns,
  AVG(email_open_rate) as avg_open,
  AVG(gmv_net) as avg_gmv
FROM klaviyo__campaigns
GROUP BY month
ORDER BY month
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-095/attempt-01/sql/S41.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-095/attempt-01/sql/S41.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-095/attempt-01/results/S41.rows.jsonl)；完整：True；SHA256：`ebc1b2b561cc9adbe57495b2cc85a78e850b08b34262d23282da8692edada307`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "klaviyo__campaigns", "kind": "base", "block": null, "base_tables": ["klaviyo__campaigns"]}] | [] | ["STRFTIME('%Y-%m', scheduled_to_send_at)"] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |
| B1 | AVG(email_open_rate) | [{"table": "klaviyo__campaigns", "column": "email_open_rate"}] | [] | False |
| B1 | AVG(gmv_net) | [{"table": "klaviyo__campaigns", "column": "gmv_net"}] | [] | False |


## S42

类别 `data`；来源 `query_db`；调用 `3348e442d9f04c5db3ce171df42c446e`；状态 `success`。

```sql
SELECT 
  CAMPAIGN_TYPE,
  COUNT(*) as n,
  SUM(CASE WHEN STATUS='sent' THEN 1 ELSE 0 END) as n_sent
FROM klaviyo__campaigns
GROUP BY CAMPAIGN_TYPE
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-095/attempt-01/sql/S42.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-095/attempt-01/sql/S42.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-095/attempt-01/results/S42.rows.jsonl)；完整：True；SHA256：`9f81dfaaf541dabffabb709a1a792c7c9b11f2838a3546c5b8225403878d4dd7`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "klaviyo__campaigns", "kind": "base", "block": null, "base_tables": ["klaviyo__campaigns"]}] | [] | ["CAMPAIGN_TYPE"] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |
| B1 | SUM(CASE WHEN STATUS = 'sent' THEN 1 ELSE 0 END) | [] | [{"table": "klaviyo__campaigns", "column": "STATUS"}] | False |


## S43

类别 `data`；来源 `query_db`；调用 `ff11f8cf749243a0b5f573b29debc555`；状态 `success`。

```sql
SELECT
  CASE WHEN sum_revenue_placed_order > 0 THEN 'Paying' ELSE 'Non-Paying' END as paying,
  COUNT(*) as n,
  AVG(days_span) as avg_ds,
  AVG(active_months) as avg_am,
  AVG(email_open_rate) as avg_open,
  AVG(count_received_email) as avg_emails,
  AVG(paid_retention_rate_month) as avg_prr
FROM klaviyo__persons
GROUP BY paying
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-095/attempt-01/sql/S43.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-095/attempt-01/sql/S43.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-095/attempt-01/results/S43.rows.jsonl)；完整：True；SHA256：`ad378660268572b8514bf88bd0ccb0112dfd002284abf8b139fe44f0e3e0846a`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "klaviyo__persons", "kind": "base", "block": null, "base_tables": ["klaviyo__persons"]}] | [] | ["CASE WHEN sum_revenue_placed_order > 0 THEN 'Paying' ELSE 'Non-Paying' END"] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |
| B1 | AVG(days_span) | [{"table": "klaviyo__persons", "column": "days_span"}] | [] | False |
| B1 | AVG(active_months) | [{"table": "klaviyo__persons", "column": "active_months"}] | [] | False |
| B1 | AVG(email_open_rate) | [{"table": "klaviyo__persons", "column": "email_open_rate"}] | [] | False |
| B1 | AVG(count_received_email) | [{"table": "klaviyo__persons", "column": "count_received_email"}] | [] | False |
| B1 | AVG(paid_retention_rate_month) | [{"table": "klaviyo__persons", "column": "paid_retention_rate_month"}] | [] | False |


## S44

类别 `data`；来源 `query_db`；调用 `914fd4231a6c439ab4f295684551cb81`；状态 `success`。

```sql
SELECT DISTINCT STATUS FROM klaviyo__campaigns
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-095/attempt-01/sql/S44.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-095/attempt-01/sql/S44.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-095/attempt-01/results/S44.rows.jsonl)；完整：True；SHA256：`e9431774ca472a84c6abc235a135825f7812389dd2bf28d7609773cb10d44e20`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "klaviyo__campaigns", "kind": "base", "block": null, "base_tables": ["klaviyo__campaigns"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |


## S45

类别 `data`；来源 `query_db`；调用 `39705b5eda014347a24a29a433805431`；状态 `success`。

```sql
SELECT NAME, STATUS, COUNT(*) as n FROM (SELECT 'campaigns' as NAME, STATUS FROM klaviyo__campaigns UNION ALL SELECT 'flows' as NAME, status FROM klaviyo__flows) GROUP BY NAME, STATUS
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-095/attempt-01/sql/S45.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-095/attempt-01/sql/S45.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-095/attempt-01/results/S45.rows.jsonl)；完整：True；SHA256：`02999b2c7a25d6b3995233b9cca9ae3a9ad3905536539877c0f8bda2263f8ded`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "klaviyo__campaigns", "kind": "base", "block": null, "base_tables": ["klaviyo__campaigns"]}] | [] | [] |
| B2 | [{"alias": "klaviyo__flows", "kind": "base", "block": null, "base_tables": ["klaviyo__flows"]}] | [] | [] |
| B3 | [] | [] | [] |
| B4 | [{"alias": "", "kind": "derived", "block": "B3", "base_tables": ["klaviyo__campaigns", "klaviyo__flows"]}] | [] | ["NAME", "STATUS"] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B4 | COUNT(*) | [] | [] | True |


## S46

类别 `data`；来源 `query_db`；调用 `4c99c2be1d464d9aa28340d9a81cc40c`；状态 `success`。

```sql
SELECT CAMPAIGN_TYPE, COUNT(*) as n, SUM(count_placed_order) as total_orders, SUM(gmv_net) as total_gmv FROM klaviyo__campaigns GROUP BY CAMPAIGN_TYPE ORDER BY total_gmv DESC
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-095/attempt-01/sql/S46.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-095/attempt-01/sql/S46.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-095/attempt-01/results/S46.rows.jsonl)；完整：True；SHA256：`6af516071d08f08223bf8f5fe79143840c94d0ee4e5c7fa6e7fb084ce9d1ef24`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "klaviyo__campaigns", "kind": "base", "block": null, "base_tables": ["klaviyo__campaigns"]}] | [] | ["CAMPAIGN_TYPE"] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |
| B1 | SUM(count_placed_order) | [{"table": "klaviyo__campaigns", "column": "count_placed_order"}] | [] | False |
| B1 | SUM(gmv_net) | [{"table": "klaviyo__campaigns", "column": "gmv_net"}] | [] | False |


## S47

类别 `data`；来源 `query_db`；调用 `0f98fc1de08a4323b3e090e3007460d1`；状态 `success`。

```sql
SELECT CAMPAIGN_TYPE, STATUS, COUNT(*) as n FROM klaviyo__campaigns GROUP BY CAMPAIGN_TYPE, STATUS ORDER BY CAMPAIGN_TYPE, STATUS
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-095/attempt-01/sql/S47.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-095/attempt-01/sql/S47.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-095/attempt-01/results/S47.rows.jsonl)；完整：True；SHA256：`744ab43cb8a51650f95367d4a82d5bbe3106a23ff575729cf0803900f3dd6813`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "klaviyo__campaigns", "kind": "base", "block": null, "base_tables": ["klaviyo__campaigns"]}] | [] | ["CAMPAIGN_TYPE", "STATUS"] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |


## S48

类别 `data`；来源 `query_db`；调用 `968c761b4988446fb82659aff18733da`；状态 `failed`。

```sql
SELECT 
  CAMPAIGN_TYPE,
  AVG(email_open_rate) as avg_open,
  AVG(email_click_to_open_rate) as avg_ctr,
  AVG(gmv_net / NULLIF(count_placed_order,0)) as aov,
  AVG(count_clicked_email / NULLIF(count_received_email,0)) as click_rate_received
FROM klaviyo__campaigns
WHERE STATUS = 'SENT'
GROUP BY CAMPAIGN_TYPE
ORDER BY avg_gmv_per_recv DESC
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-095/attempt-01/sql/S48.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-095/attempt-01/sql/S48.parameters.json)。

错误：`OperationalError('no such column: avg_gmv_per_recv')`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "klaviyo__campaigns", "kind": "base", "block": null, "base_tables": ["klaviyo__campaigns"]}] | [] | ["CAMPAIGN_TYPE"] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | AVG(email_open_rate) | [{"table": "klaviyo__campaigns", "column": "email_open_rate"}] | [] | False |
| B1 | AVG(email_click_to_open_rate) | [{"table": "klaviyo__campaigns", "column": "email_click_to_open_rate"}] | [] | False |
| B1 | AVG(gmv_net / NULLIF(count_placed_order, 0)) | [{"table": "klaviyo__campaigns", "column": "gmv_net"}, {"table": "klaviyo__campaigns", "column": "count_placed_order"}] | [] | False |
| B1 | AVG(count_clicked_email / NULLIF(count_received_email, 0)) | [{"table": "klaviyo__campaigns", "column": "count_clicked_email"}, {"table": "klaviyo__campaigns", "column": "count_received_email"}] | [] | False |


未解析列血缘：[{"block": "B1", "column": "avg_gmv_per_recv", "reason": "ambiguous_or_missing_source"}]

## S49

类别 `data`；来源 `query_db`；调用 `6572fa3bf64d4530a7508ff04ff2364a`；状态 `success`。

```sql
SELECT 
  CAMPAIGN_TYPE,
  AVG(email_open_rate) as avg_open,
  AVG(email_click_to_open_rate) as avg_ctr,
  AVG(gmv_net / NULLIF(count_placed_order,0)) as aov,
  AVG(count_clicked_email / NULLIF(count_received_email,0)) as click_rate_received,
  AVG(count_placed_order / NULLIF(count_received_email,0)) as orders_per_recv,
  AVG(gmv_net / NULLIF(count_received_email,0)) as gmv_per_recv
FROM klaviyo__campaigns
WHERE STATUS = 'SENT'
GROUP BY CAMPAIGN_TYPE
ORDER BY gmv_per_recv DESC
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-095/attempt-01/sql/S49.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-095/attempt-01/sql/S49.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-095/attempt-01/results/S49.rows.jsonl)；完整：True；SHA256：`a8a63f54d4f069c3384c03a7bd78d3332eeac731f76a8ecb2c5b7d66ca4c6d3e`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "klaviyo__campaigns", "kind": "base", "block": null, "base_tables": ["klaviyo__campaigns"]}] | [] | ["CAMPAIGN_TYPE"] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | AVG(email_open_rate) | [{"table": "klaviyo__campaigns", "column": "email_open_rate"}] | [] | False |
| B1 | AVG(email_click_to_open_rate) | [{"table": "klaviyo__campaigns", "column": "email_click_to_open_rate"}] | [] | False |
| B1 | AVG(gmv_net / NULLIF(count_placed_order, 0)) | [{"table": "klaviyo__campaigns", "column": "gmv_net"}, {"table": "klaviyo__campaigns", "column": "count_placed_order"}] | [] | False |
| B1 | AVG(count_clicked_email / NULLIF(count_received_email, 0)) | [{"table": "klaviyo__campaigns", "column": "count_clicked_email"}, {"table": "klaviyo__campaigns", "column": "count_received_email"}] | [] | False |
| B1 | AVG(count_placed_order / NULLIF(count_received_email, 0)) | [{"table": "klaviyo__campaigns", "column": "count_placed_order"}, {"table": "klaviyo__campaigns", "column": "count_received_email"}] | [] | False |
| B1 | AVG(gmv_net / NULLIF(count_received_email, 0)) | [{"table": "klaviyo__campaigns", "column": "gmv_net"}, {"table": "klaviyo__campaigns", "column": "count_received_email"}] | [] | False |


## S50

类别 `data`；来源 `query_db`；调用 `34649d22cbdb4412848db78eb52e9e01`；状态 `success`。

```sql
SELECT 
  flow_name,
  trigger_type,
  email_open_rate,
  email_click_to_open_rate,
  total_count_unique_people,
  count_placed_order,
  gmv_net
FROM klaviyo__flows
WHERE status = 'LIVE'
ORDER BY gmv_net DESC
LIMIT 15
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-095/attempt-01/sql/S50.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-095/attempt-01/sql/S50.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-095/attempt-01/results/S50.rows.jsonl)；完整：True；SHA256：`f244a63d29d7a65fa6b4e78c9e0d913df739b5ba77b49b281f10413d63e82522`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "klaviyo__flows", "kind": "base", "block": null, "base_tables": ["klaviyo__flows"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |


## S51

类别 `data`；来源 `python`；调用 `9a59c76e88d049f5a187809a83b8eec0`；状态 `success`。

```sql

SELECT person_id, days_span, active_days, active_months, months_span,
       paid_retained_month_count, paid_retention_rate_month,
       active_retention_rate_month, email_open_rate, count_received_email,
       count_opened_email, count_clicked_email, count_placed_order,
       sum_revenue_placed_order, count_viewed_product, has_7day_retention, has_30day_retention
FROM klaviyo__persons

```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-095/attempt-01/sql/S51.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-095/attempt-01/sql/S51.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-095/attempt-01/results/S51.rows.jsonl)；完整：True；SHA256：`77ce0712e51b46044587a0e418c327f8e2562762b3e70865c80eccbd2a186530`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "klaviyo__persons", "kind": "base", "block": null, "base_tables": ["klaviyo__persons"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |


## S52

类别 `data`；来源 `python`；调用 `3a3e9876e4704d0880d3f3cc887d20ab`；状态 `success`。

```sql
SELECT count_received_email, email_open_rate, count_placed_order, days_span FROM klaviyo__persons
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-095/attempt-01/sql/S52.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-095/attempt-01/sql/S52.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-095/attempt-01/results/S52.rows.jsonl)；完整：True；SHA256：`196965ef239a9495afbbdfb915fdcbbe0595164bd3a7fbde9ec1ba662bb73801`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "klaviyo__persons", "kind": "base", "block": null, "base_tables": ["klaviyo__persons"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |


## S53

类别 `data`；来源 `query_db`；调用 `bf99f59296114056bfee9cc8468da45e`；状态 `success`。

```sql
SELECT 
  CAMPAIGN_TYPE,
  AVG(product_view_to_order_rate_campaign) as avg_pv_to_order,
  AVG(count_ordered_product / NULLIF(count_placed_order,0)) as items_per_order,
  AVG(gmv_net / NULLIF(total_count_unique_people,0)) as gmv_per_person
FROM klaviyo__campaigns
WHERE STATUS = 'SENT'
GROUP BY CAMPAIGN_TYPE
ORDER BY gmv_per_person DESC
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-095/attempt-01/sql/S53.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-095/attempt-01/sql/S53.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-095/attempt-01/results/S53.rows.jsonl)；完整：True；SHA256：`7a635a4ceb0b692bd98899911c5eba144ab9bca3a4b95dc856c13ea260bf1bd8`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "klaviyo__campaigns", "kind": "base", "block": null, "base_tables": ["klaviyo__campaigns"]}] | [] | ["CAMPAIGN_TYPE"] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | AVG(product_view_to_order_rate_campaign) | [{"table": "klaviyo__campaigns", "column": "product_view_to_order_rate_campaign"}] | [] | False |
| B1 | AVG(count_ordered_product / NULLIF(count_placed_order, 0)) | [{"table": "klaviyo__campaigns", "column": "count_ordered_product"}, {"table": "klaviyo__campaigns", "column": "count_placed_order"}] | [] | False |
| B1 | AVG(gmv_net / NULLIF(total_count_unique_people, 0)) | [{"table": "klaviyo__campaigns", "column": "gmv_net"}, {"table": "klaviyo__campaigns", "column": "total_count_unique_people"}] | [] | False |


## S54

类别 `data`；来源 `query_db`；调用 `eb2a122c3e7141c895a335d784ff921b`；状态 `success`。

```sql
SELECT 
  strftime('%Y-%m-%d', scheduled_to_send_at) as send_date,
  CAMPAIGN_TYPE,
  campaign_name
FROM klaviyo__campaigns
WHERE STATUS = 'SENT'
ORDER BY send_date
LIMIT 30
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-095/attempt-01/sql/S54.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-095/attempt-01/sql/S54.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-095/attempt-01/results/S54.rows.jsonl)；完整：True；SHA256：`04887267ccb5012930dcc6345cc3eb553985a35f9130d3b53988b3c577ac90f2`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "klaviyo__campaigns", "kind": "base", "block": null, "base_tables": ["klaviyo__campaigns"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |


## S55

类别 `data`；来源 `query_db`；调用 `f09d2b25f7f742aa9640901ad05fd003`；状态 `success`。

```sql
WITH sent AS (
  SELECT campaign_id, CAMPAIGN_TYPE, scheduled_to_send_at,
         ROW_NUMBER() OVER (ORDER BY scheduled_to_send_at) as seq
  FROM klaviyo__campaigns
  WHERE STATUS = 'SENT'
),
gaps AS (
  SELECT s1.CAMPAIGN_TYPE as type,
         CAST(julianday(s2.scheduled_to_send_at) - julianday(s1.scheduled_to_send_at) AS INTEGER) as gap_days
  FROM sent s1
  JOIN sent s2 ON s2.seq = s1.seq + 1
)
SELECT type, COUNT(*) as n_sends, AVG(gap_days) as avg_gap_days, MIN(gap_days) as min_gap, MAX(gap_days) as max_gap
FROM gaps
GROUP BY type
ORDER BY n_sends DESC
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-095/attempt-01/sql/S55.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-095/attempt-01/sql/S55.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-095/attempt-01/results/S55.rows.jsonl)；完整：True；SHA256：`5ab12b3dd8a2f01801ca5cd3aa3212f3f84f5327770034b06cc2b216d99468e5`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "klaviyo__campaigns", "kind": "base", "block": null, "base_tables": ["klaviyo__campaigns"]}] | [] | [] |
| B2 | [{"alias": "s1", "kind": "derived", "block": "B1", "base_tables": ["klaviyo__campaigns"]}, {"alias": "s2", "kind": "derived", "block": "B1", "base_tables": ["klaviyo__campaigns"]}] | [{"type": "INNER", "right": "sent AS s2", "on": "s2.seq = s1.seq + 1", "using": []}] | [] |
| B3 | [{"alias": "gaps", "kind": "derived", "block": "B2", "base_tables": ["klaviyo__campaigns"]}] | [] | ["type"] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B3 | COUNT(*) | [] | [] | True |
| B3 | AVG(gap_days) | [{"table": "klaviyo__campaigns", "column": "scheduled_to_send_at"}, {"table": "klaviyo__campaigns", "column": "scheduled_to_send_at"}] | [] | False |
| B3 | MIN(gap_days) | [{"table": "klaviyo__campaigns", "column": "scheduled_to_send_at"}, {"table": "klaviyo__campaigns", "column": "scheduled_to_send_at"}] | [] | False |
| B3 | MAX(gap_days) | [{"table": "klaviyo__campaigns", "column": "scheduled_to_send_at"}, {"table": "klaviyo__campaigns", "column": "scheduled_to_send_at"}] | [] | False |


## S56

类别 `data`；来源 `query_db`；调用 `c68aa077cbdc4da2a2cc2dc026c9c8de`；状态 `failed`。

```sql
WITH sent AS (
  SELECT campaign_id, CAMPAIGN_TYPE, scheduled_to_send_at
  FROM klaviyo__campaigns
  WHERE STATUS = 'SENT'
)
SELECT CAMPAIGN_TYPE, 
       COUNT(*) as n,
       AVG(count_placed_order / NULLIF(total_count_unique_people,0)) as conv_per_person,
       AVG(count_opened_email / NULLIF(total_count_unique_people,0)) as open_per_person,
       AVG(count_clicked_email / NULLIF(total_count_unique_people,0)) as click_per_person
FROM sent
GROUP BY CAMPAIGN_TYPE
ORDER BY conv_per_person DESC
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-095/attempt-01/sql/S56.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-095/attempt-01/sql/S56.parameters.json)。

错误：`OperationalError('no such column: count_placed_order')`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "klaviyo__campaigns", "kind": "base", "block": null, "base_tables": ["klaviyo__campaigns"]}] | [] | [] |
| B2 | [{"alias": "sent", "kind": "derived", "block": "B1", "base_tables": ["klaviyo__campaigns"]}] | [] | ["CAMPAIGN_TYPE"] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B2 | COUNT(*) | [] | [] | True |
| B2 | AVG(count_placed_order / NULLIF(total_count_unique_people, 0)) | [{"unknown": "count_placed_order"}, {"unknown": "total_count_unique_people"}] | [] | False |
| B2 | AVG(count_opened_email / NULLIF(total_count_unique_people, 0)) | [{"unknown": "count_opened_email"}, {"unknown": "total_count_unique_people"}] | [] | False |
| B2 | AVG(count_clicked_email / NULLIF(total_count_unique_people, 0)) | [{"unknown": "count_clicked_email"}, {"unknown": "total_count_unique_people"}] | [] | False |


未解析列血缘：[{"block": "B2", "column": "count_placed_order", "reason": "ambiguous_or_missing_source"}, {"block": "B2", "column": "total_count_unique_people", "reason": "ambiguous_or_missing_source"}, {"block": "B2", "column": "count_opened_email", "reason": "ambiguous_or_missing_source"}, {"block": "B2", "column": "total_count_unique_people", "reason": "ambiguous_or_missing_source"}, {"block": "B2", "column": "count_clicked_email", "reason": "ambiguous_or_missing_source"}, {"block": "B2", "column": "total_count_unique_people", "reason": "ambiguous_or_missing_source"}, {"block": "B2", "column": "count_placed_order", "reason": "ambiguous_or_missing_source"}, {"block": "B2", "column": "total_count_unique_people", "reason": "ambiguous_or_missing_source"}, {"block": "B2", "column": "count_opened_email", "reason": "ambiguous_or_missing_source"}, {"block": "B2", "column": "total_count_unique_people", "reason": "ambiguous_or_missing_source"}, {"block": "B2", "column": "count_clicked_email", "reason": "ambiguous_or_missing_source"}, {"block": "B2", "column": "total_count_unique_people", "reason": "ambiguous_or_missing_source"}]

## S57

类别 `data`；来源 `query_db`；调用 `9d6b0c2c67e64e73933a27cb4cbaa039`；状态 `success`。

```sql
WITH sent AS (
  SELECT campaign_id, CAMPAIGN_TYPE, 
         CAST(julianday(scheduled_to_send_at) AS INTEGER) as send_day
  FROM klaviyo__campaigns
  WHERE STATUS = 'SENT'
),
same_type_gaps AS (
  SELECT s1.CAMPAIGN_TYPE as type,
         s2.send_day - s1.send_day as gap_days
  FROM sent s1
  JOIN sent s2 ON s1.CAMPAIGN_TYPE = s2.CAMPAIGN_TYPE 
              AND s2.send_day > s1.send_day
  WHERE NOT EXISTS (
    SELECT 1 FROM sent s3 
    WHERE s3.CAMPAIGN_TYPE = s1.CAMPAIGN_TYPE 
      AND s3.send_day > s1.send_day 
      AND s3.send_day < s2.send_day
  )
)
SELECT type, COUNT(*) as n_intervals, AVG(gap_days) as avg_gap, MIN(gap_days) as min_gap, MAX(gap_days) as max_gap
FROM same_type_gaps
GROUP BY type
ORDER BY avg_gap
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-095/attempt-01/sql/S57.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-095/attempt-01/sql/S57.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-095/attempt-01/results/S57.rows.jsonl)；完整：True；SHA256：`da0fcaa5872e32f3cdf02f1b3d91dd81bd048ce329e2cb7f574d2134ad1797ab`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "klaviyo__campaigns", "kind": "base", "block": null, "base_tables": ["klaviyo__campaigns"]}] | [] | [] |
| B2 | [{"alias": "s3", "kind": "derived", "block": "B1", "base_tables": ["klaviyo__campaigns"]}] | [] | [] |
| B3 | [{"alias": "s1", "kind": "derived", "block": "B1", "base_tables": ["klaviyo__campaigns"]}, {"alias": "s2", "kind": "derived", "block": "B1", "base_tables": ["klaviyo__campaigns"]}] | [{"type": "INNER", "right": "sent AS s2", "on": "s1.CAMPAIGN_TYPE = s2.CAMPAIGN_TYPE AND s2.send_day > s1.send_day", "using": []}] | [] |
| B4 | [{"alias": "same_type_gaps", "kind": "derived", "block": "B3", "base_tables": ["klaviyo__campaigns"]}] | [] | ["type"] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B4 | COUNT(*) | [] | [] | True |
| B4 | AVG(gap_days) | [{"table": "klaviyo__campaigns", "column": "scheduled_to_send_at"}, {"table": "klaviyo__campaigns", "column": "scheduled_to_send_at"}] | [] | False |
| B4 | MIN(gap_days) | [{"table": "klaviyo__campaigns", "column": "scheduled_to_send_at"}, {"table": "klaviyo__campaigns", "column": "scheduled_to_send_at"}] | [] | False |
| B4 | MAX(gap_days) | [{"table": "klaviyo__campaigns", "column": "scheduled_to_send_at"}, {"table": "klaviyo__campaigns", "column": "scheduled_to_send_at"}] | [] | False |


## S58

类别 `data`；来源 `query_db`；调用 `c55aaa2311704f6698950c4dcb76a467`；状态 `success`。

```sql
-- Touchpoint path: typical sequence of campaign types
WITH sent AS (
  SELECT CAMPAIGN_TYPE, scheduled_to_send_at,
         ROW_NUMBER() OVER (ORDER BY scheduled_to_send_at) as seq
  FROM klaviyo__campaigns
  WHERE STATUS = 'SENT'
)
SELECT seq, scheduled_to_send_at, CAMPAIGN_TYPE
FROM sent
ORDER BY seq
LIMIT 40
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-095/attempt-01/sql/S58.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-095/attempt-01/sql/S58.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-095/attempt-01/results/S58.rows.jsonl)；完整：True；SHA256：`033a3672ef7c5a82383d2fcc1a5094185801f12e709264f0c7d6b98aa39b7070`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "klaviyo__campaigns", "kind": "base", "block": null, "base_tables": ["klaviyo__campaigns"]}] | [] | [] |
| B2 | [{"alias": "sent", "kind": "derived", "block": "B1", "base_tables": ["klaviyo__campaigns"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |


## S59

类别 `data`；来源 `query_db`；调用 `9ef822b5d3924edf8b461e10af0597b0`；状态 `success`。

```sql
SELECT MAX(days_span - active_days) as max_inactive_days,
       AVG(count_received_email) as avg_emails,
       MAX(count_received_email) as max_emails,
       SUM(CASE WHEN email_open_rate < 0.3 THEN 1 ELSE 0 END) as low_open_n,
       SUM(CASE WHEN email_open_rate >= 0.3 AND email_open_rate < 0.5 THEN 1 ELSE 0 END) as mid_open_n,
       SUM(CASE WHEN email_open_rate >= 0.5 THEN 1 ELSE 0 END) as high_open_n
FROM klaviyo__persons
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-095/attempt-01/sql/S59.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-095/attempt-01/sql/S59.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-095/attempt-01/results/S59.rows.jsonl)；完整：True；SHA256：`4d2c2aca6ca4e0267622a7395785a2a8f47fd7940f770f8f256e5e89f2eb696e`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "klaviyo__persons", "kind": "base", "block": null, "base_tables": ["klaviyo__persons"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | MAX(days_span - active_days) | [{"table": "klaviyo__persons", "column": "days_span"}, {"table": "klaviyo__persons", "column": "active_days"}] | [] | False |
| B1 | AVG(count_received_email) | [{"table": "klaviyo__persons", "column": "count_received_email"}] | [] | False |
| B1 | MAX(count_received_email) | [{"table": "klaviyo__persons", "column": "count_received_email"}] | [] | False |
| B1 | SUM(CASE WHEN email_open_rate < 0.3 THEN 1 ELSE 0 END) | [] | [{"table": "klaviyo__persons", "column": "email_open_rate"}] | False |
| B1 | SUM(CASE WHEN email_open_rate >= 0.3 AND email_open_rate < 0.5 THEN 1 ELSE 0 END) | [] | [{"table": "klaviyo__persons", "column": "email_open_rate"}, {"table": "klaviyo__persons", "column": "email_open_rate"}] | False |
| B1 | SUM(CASE WHEN email_open_rate >= 0.5 THEN 1 ELSE 0 END) | [] | [{"table": "klaviyo__persons", "column": "email_open_rate"}] | False |


## S60

类别 `data`；来源 `query_db`；调用 `a3a1ec34607e4f6ea9a08b5763298cea`；状态 `success`。

```sql
-- Emails per month distribution to inform frequency recommendations
SELECT 
  CASE 
    WHEN count_received_email * 1.0 / active_months < 20 THEN '<20 emails/mo'
    WHEN count_received_email * 1.0 / active_months < 30 THEN '20-30 emails/mo'
    WHEN count_received_email * 1.0 / active_months < 40 THEN '30-40 emails/mo'
    ELSE '40+ emails/mo'
  END as intensity,
  COUNT(*) as n,
  AVG(email_open_rate) as avg_open,
  AVG(count_placed_order) as avg_orders,
  AVG(paid_retention_rate_month) as avg_prr
FROM klaviyo__persons
GROUP BY intensity
ORDER BY intensity
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-095/attempt-01/sql/S60.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-095/attempt-01/sql/S60.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-095/attempt-01/results/S60.rows.jsonl)；完整：True；SHA256：`4ba988ef25a353b40d49c601c9eb02ddcbe309e66810fab8063b396a5e3f7f4c`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "klaviyo__persons", "kind": "base", "block": null, "base_tables": ["klaviyo__persons"]}] | [] | ["CASE WHEN count_received_email * 1.0 / active_months < 20 THEN '<20 emails/mo' WHEN count_received_email * 1.0 / active_months < 30 THEN '20-30 emails/mo' WHEN count_received_email * 1.0 / active_months < 40 THEN '30-40 emails/mo' ELSE '40+ emails/mo' END"] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |
| B1 | AVG(email_open_rate) | [{"table": "klaviyo__persons", "column": "email_open_rate"}] | [] | False |
| B1 | AVG(count_placed_order) | [{"table": "klaviyo__persons", "column": "count_placed_order"}] | [] | False |
| B1 | AVG(paid_retention_rate_month) | [{"table": "klaviyo__persons", "column": "paid_retention_rate_month"}] | [] | False |

