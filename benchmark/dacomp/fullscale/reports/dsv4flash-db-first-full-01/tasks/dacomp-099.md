# dacomp-099

Identify the key factors that lead customers to upgrade or downgrade. On a per-customer ba…

运行：已提交。官方未评分。全部 SQL 尝试/成功 74/72；数据 SQL 72/70；Python 15 次。

完整原题：

Identify the key factors that lead customers to upgrade or downgrade. On a per-customer basis, construct an event timeline based on subscription change times (hypothetical `upgrade_at`, `downgrade_at`). Within a 30-day observation window before and after the change, compare changes in feature usage intensity (e.g., call counts, frequency changes relative to a baseline) with the occurrence of support incidents (e.g., outages, Bug tickets, support conversations). The goal is to analyze which experiences best explain the occurrence of upgrades or downgrades and to provide actionable business recommendations.

| 表 | 行数 | 列数 |
| --- | --- | --- |
| intercom__company_enhanced | 2509 | 14 |
| intercom__company_metrics | 2509 | 25 |
| intercom__conversation_enhanced | 6703 | 30 |
| intercom__conversation_metrics | 6703 | 40 |


实际路线（分析者依据 SQL/源码概括，不代表 Agent 自述）：SQL 连接、窗口和指标提取 → Python 业务聚合、统计检验与图表 → 报告

数据库大小：8,978,432 字节。

## 数据 SQL

| SQL | 状态 | 基础表 | Join 输入/类型 | GROUP BY | 聚合表达式 | 结果行数 | 数据库 ms |
| --- | --- | --- | --- | --- | --- | --- | --- |
| [S3/Q1](#s3) | success | ["intercom__company_enhanced"] | 0 / {} | [] | [] | 4 | 1.233 |
| [S4/Q2](#s4) | success | ["intercom__company_metrics"] | 0 / {} | [] | [] | 4 | 1.259 |
| [S5/Q3](#s5) | success | ["intercom__company_enhanced"] | 0 / {} | [] | [] | 10 | 0.387 |
| [S6/Q4](#s6) | success | ["intercom__company_enhanced"] | 0 / {} | ["company_id"] | ["COUNT(*)"] | 0 | 1.803 |
| [S7/Q5](#s7) | success | ["intercom__company_metrics"] | 0 / {} | ["company_id"] | ["COUNT(*)"] | 0 | 1.735 |
| [S8/Q6](#s8) | success | ["intercom__company_metrics"] | 0 / {} | [] | [] | 10 | 0.509 |
| [S9/Q7](#s9) | success | ["intercom__company_enhanced"] | 0 / {} | [] | ["COUNT(*)", "COUNT(DISTINCT company_id)"] | 1 | 2.269 |
| [S10/Q8](#s10) | success | ["intercom__conversation_metrics"] | 0 / {} | [] | ["COUNT(*)", "COUNT(DISTINCT conversation_id)"] | 1 | 7.033 |
| [S11/Q9](#s11) | success | ["intercom__conversation_enhanced"] | 0 / {} | ["all_conversation_tags"] | ["COUNT(*)"] | 50 | 6.383 |
| [S12/Q10](#s12) | success | ["intercom__conversation_enhanced"] | 0 / {} | [] | [] | 1 | 2.479 |
| [S13/Q11](#s13) | success | ["intercom__conversation_enhanced"] | 0 / {} | [] | [] | 2 | 2.023 |
| [S14/Q12](#s14) | success | ["intercom__conversation_enhanced"] | 0 / {} | [] | [] | 3 | 1.859 |
| [S15/Q13](#s15) | success | ["intercom__conversation_enhanced"] | 0 / {} | ["all_conversation_tags"] | ["COUNT(*)"] | 100 | 6.03 |
| [S16/Q14](#s16) | success | ["JSON_EACH('[\"' \|\| REPLACE(all_conversation_tags, ', ', '\",\"') \|\| '\"]')", "intercom__conversation_enhanced"] | 2 / {'CROSS': 1} | ["tag"] | ["COUNT(*)"] | 20 | 14.944 |
| [S17/Q15](#s17) | success | ["intercom__company_enhanced"] | 0 / {} | ["all_company_tags"] | ["COUNT(*)"] | 100 | 2.294 |
| [S18/Q16](#s18) | success | ["JSON_EACH('[\"' \|\| REPLACE(all_company_tags, ', ', '\",\"') \|\| '\"]')", "intercom__company_enhanced"] | 2 / {'CROSS': 1} | ["tag"] | ["COUNT(*)"] | 20 | 5.102 |
| [S19/Q17](#s19) | success | ["intercom__conversation_enhanced"] | 0 / {} | [] | [] | 10 | 0.513 |
| [S20/Q18](#s20) | success | ["JSON_EACH('[\"' \|\| REPLACE(all_conversation_tags, ', ', '\",\"') \|\| '\"]')", "intercom__conversation_enhanced"] | 2 / {'CROSS': 1} | ["tag"] | ["COUNT(*)"] | 20 | 14.488 |
| [S21/Q19](#s21) | success | ["intercom__conversation_metrics"] | 0 / {} | [] | ["MIN(conversation_created_at)", "MAX(conversation_created_at)"] | 1 | 2.788 |
| [S22/Q20](#s22) | success | ["intercom__company_enhanced"] | 0 / {} | [] | ["MIN(created_at)", "MAX(created_at)", "MIN(updated_at)", "MAX(updated_at)"] | 1 | 1.206 |
| [S23/Q21](#s23) | success | ["intercom__conversation_enhanced"] | 0 / {} | [] | ["COUNT(*)"] | 1 | 3.079 |
| [S24/Q22](#s24) | success | ["intercom__conversation_enhanced"] | 0 / {} | [] | ["COUNT(*)"] | 1 | 2.998 |
| [S25/Q23](#s25) | success | ["intercom__conversation_enhanced"] | 0 / {} | [] | ["COUNT(DISTINCT all_contact_company_names)"] | 1 | 3.227 |
| [S26/Q24](#s26) | success | ["intercom__conversation_enhanced"] | 0 / {} | [] | ["COUNT(DISTINCT all_contact_company_names)"] | 1 | 3.164 |
| [S27/Q25](#s27) | success | ["intercom__conversation_enhanced"] | 0 / {} | ["all_contact_company_names"] | ["COUNT(*)"] | 22 | 3.473 |
| [S28/Q26](#s28) | success | ["intercom__conversation_enhanced"] | 0 / {} | ["all_contact_company_names"] | ["COUNT(*)"] | 23 | 3.286 |
| [S29/Q27](#s29) | success | ["intercom__company_enhanced", "intercom__conversation_enhanced"] | 0 / {} | [] | [] | 109 | 4.218 |
| [S30/Q28](#s30) | success | ["intercom__company_enhanced", "intercom__conversation_enhanced"] | 0 / {} | [] | [] | 122 | 4.2 |
| [S31/Q29](#s31) | success | ["intercom__company_enhanced"] | 0 / {} | ["company_name"] | ["COUNT(DISTINCT company_id)", "COUNT(DISTINCT plan_name)", "GROUP_CONCAT(DISTINCT plan_name)", "GROUP_CONCAT(DISTINCT monthly_spend)"] | 30 | 4.547 |
| [S32/Q30](#s32) | success | ["intercom__company_enhanced"] | 0 / {} | [] | [] | 9 | 0.827 |
| [S33/Q31](#s33) | success | ["intercom__company_enhanced"] | 0 / {} | ["company_name"] | ["COUNT(DISTINCT company_id)", "COUNT(DISTINCT plan_name)"] | 551 | 3.412 |
| [S34/Q32](#s34) | success | ["intercom__conversation_enhanced"] | 0 / {} | [] | ["COUNT(*)", "COUNT(DISTINCT all_contact_company_names)"] | 1 | 3.616 |
| [S35/Q33](#s35) | success | ["intercom__company_enhanced"] | 0 / {} | [] | ["COUNT(DISTINCT company_name)"] | 1 | 1.507 |
| [S36/Q34](#s36) | success | ["intercom__company_enhanced", "intercom__conversation_enhanced"] | 2 / {'INNER': 1} | [] | ["COUNT(*)"] | 1 | 8.415 |
| [S37/Q35](#s37) | success | ["intercom__conversation_enhanced"] | 0 / {} | ["all_contact_company_names"] | ["COUNT(*)"] | 31 | 4.314 |
| [S38/Q36](#s38) | success | ["intercom__company_enhanced", "intercom__conversation_enhanced"] | 0 / {} | ["ce.company_name"] | ["COUNT(*)", "COUNT(DISTINCT ce.plan_name)", "GROUP_CONCAT(DISTINCT ce.plan_name)"] | 31 | 4.331 |
| [S39/Q37](#s39) | success | ["intercom__company_enhanced"] | 0 / {} | ["plan_name"] | ["COUNT(*)", "AVG(monthly_spend)", "MIN(monthly_spend)", "MAX(monthly_spend)", "AVG(session_count)", "AVG(user_count)"] | 4 | 1.987 |
| [S40/Q38](#s40) | success | ["intercom__company_enhanced"] | 0 / {} | [] | [] | 6 | 0.772 |
| [S41/Q39](#s41) | success | ["intercom__company_enhanced"] | 0 / {} | ["CASE WHEN tier > prev_tier THEN 'upgrade' WHEN tier < prev_tier THEN 'downgrade' ELSE 'no_change' END"] | ["COUNT(*)"] | 3 | 8.932 |
| [S42/Q40](#s42) | success | ["intercom__company_enhanced", "intercom__conversation_enhanced"] | 0 / {} | [] | [] | 101 | 12.073 |
| [S43/Q41](#s43) | success | ["intercom__company_enhanced", "intercom__conversation_enhanced", "intercom__conversation_metrics"] | 3 / {'INNER': 1, 'LEFT': 1} | ["event_type", "period"] | ["COUNT(*)", "SUM(is_bug)", "SUM(is_outage)", "SUM(is_escalation)", "SUM(is_upgrade_opp)", "SUM(is_downgrade_risk)", "SUM(CASE WHEN sla_status = 'breached' THEN 1 ELSE 0 END)", "AVG(count_total_parts)", "AVG(CASE WHEN conversation_rating > 0 THEN conversation_rating END)"] | 4 | 43.725 |
| [S44/Q42](#s44) | success | ["intercom__company_enhanced", "intercom__conversation_enhanced"] | 0 / {} | ["event_type"] | ["COUNT(*)", "COUNT(DISTINCT company_name)"] | 2 | 10.926 |
| [S45/Q43](#s45) | success | ["intercom__company_enhanced", "intercom__conversation_enhanced", "intercom__conversation_metrics"] | 3 / {'INNER': 1, 'LEFT': 1} | [] | [] | 567 | 46.558 |
| [S46/Q44](#s46) | success | ["intercom__company_enhanced", "intercom__conversation_enhanced", "intercom__conversation_metrics"] | 3 / {'INNER': 1, 'LEFT': 1} | [] | [] | 567 | 46.314 |
| [S47/Q45](#s47) | success | ["intercom__company_enhanced", "intercom__conversation_enhanced", "intercom__conversation_metrics"] | 3 / {'INNER': 1, 'LEFT': 1} | [] | [] | 567 | 45.69 |
| [S48/Q46](#s48) | success | ["intercom__company_enhanced", "intercom__conversation_enhanced", "intercom__conversation_metrics"] | 3 / {'INNER': 1, 'LEFT': 1} | [] | [] | 567 | 45.406 |
| [S49/Q47](#s49) | success | ["intercom__company_enhanced", "intercom__conversation_enhanced"] | 2 / {'LEFT': 1} | ["e.company_name", "e.event_at", "e.event_type", "e.prev_plan", "e.new_plan"] | ["SUM(CASE WHEN c.conversation_created_at < e.event_at THEN 1 ELSE 0 END)", "SUM(CASE WHEN c.conversation_created_at > e.event_at THEN 1 ELSE 0 END)", "SUM(CASE WHEN c.conversation_created_at < e.event_at AND c.all_conversation_tags LIKE '%Bug%' THEN 1 ELSE 0 END)", "SUM(CASE WHEN c.conversation_created_at > e.event_at AND c.all_conversation_tags LIKE '%Bug%' THEN 1 ELSE 0 END)", "SUM(CASE WHEN c.conversation_created_at < e.event_at AND c.all_conversation_tags LIKE '%Outage%' THEN 1 ELSE 0 END)", "SUM(CASE WHEN c.conversation_created_at > e.event_at AND c.all_conversation_tags LIKE '%Outage%' THEN 1 ELSE 0 END)", "SUM(CASE WHEN c.conversation_created_at < e.event_at AND c.all_conversation_tags LIKE '%Escalation%' THEN 1 ELSE 0 END)", "SUM(CASE WHEN c.conversation_created_at > e.event_at AND c.all_conversation_tags LIKE '%Escalation%' THEN 1 ELSE 0 END)", "SUM(CASE WHEN c.conversation_created_at < e.event_at AND c.sla_status = 'breached' THEN 1 ELSE 0 END)", "SUM(CASE WHEN c.conversation_created_at > e.event_at AND c.sla_status = 'breached' THEN 1 ELSE 0 END)"] | 101 | 35.855 |
| [S50/Q48](#s50) | success | ["intercom__company_enhanced", "intercom__conversation_enhanced"] | 0 / {} | ["e.event_type"] | ["MIN(conversation_created_at)", "MAX(conversation_created_at)", "COUNT(*)", "SUM(CASE WHEN e.event_at >= (SELECT MIN(conversation_created_at) FROM intercom__conversation_enhanced WHERE all_contact_company_names = e.company_name) + 30 AND e.event_at <= (SELECT MAX(conversation_created_at) FROM intercom__conversation_enhanced WHERE all_contact_company_names = e.company_name) - 30 THEN 1 ELSE 0 END)"] | 2 | 375.709 |
| [S51/Q49](#s51) | success | ["intercom__company_enhanced", "intercom__conversation_enhanced"] | 2 / {'LEFT': 1} | ["all_contact_company_names", "cr.company_name"] | ["MIN(conversation_created_at)", "MAX(conversation_created_at)", "COUNT(*)", "SUM(CASE WHEN e.event_type = 'upgrade' THEN 1 ELSE 0 END)", "SUM(CASE WHEN e.event_type = 'downgrade' THEN 1 ELSE 0 END)"] | 31 | 14.011 |
| [S52/Q50](#s52) | success | ["intercom__company_enhanced", "intercom__conversation_enhanced"] | 2 / {'INNER': 1} | ["all_contact_company_names", "e.event_type"] | ["MIN(conversation_created_at)", "MAX(conversation_created_at)", "COUNT(*)", "SUM(CASE WHEN e.event_at >= DATETIME(cr.min_c, '+30 days') AND e.event_at <= DATETIME(cr.max_c, '-30 days') THEN 1 ELSE 0 END)"] | 2 | 15.381 |
| [S53/Q51](#s53) | success | ["intercom__company_enhanced"] | 0 / {} | [] | [] | 5 | 0.729 |
| [S54/Q52](#s54) | success | ["intercom__conversation_enhanced"] | 0 / {} | [] | [] | 40 | 2.695 |
| [S55/Q53](#s55) | failed | ["intercom__conversation_enhanced", "intercom__conversation_metrics"] | 2 / {'LEFT': 1} | [] | [] | unknown | 未取得；调用总时长 0.238 ms |
| [S56/Q54](#s56) | failed | ["intercom__conversation_enhanced", "intercom__conversation_metrics"] | 2 / {'LEFT': 1} | [] | [] | unknown | 未取得；调用总时长 0.165 ms |
| [S57/Q55](#s57) | success | ["intercom__conversation_enhanced"] | 0 / {} | [] | ["COUNT(*)"] | 1 | 1.651 |
| [S58/Q56](#s58) | success | ["intercom__conversation_enhanced"] | 0 / {} | [] | [] | 587 | 3.564 |
| [S59/Q57](#s59) | success | ["intercom__conversation_metrics"] | 0 / {} | [] | [] | 100 | 0.356 |
| [S60/Q58](#s60) | success | ["intercom__conversation_enhanced"] | 0 / {} | ["conversation_id"] | ["COUNT(*)"] | 0 | 4.596 |
| [S61/Q59](#s61) | success | ["intercom__conversation_enhanced"] | 0 / {} | [] | [] | 6703 | 12.266 |
| [S62/Q60](#s62) | success | ["intercom__conversation_metrics"] | 0 / {} | [] | [] | 6703 | 8.476 |
| [S63/Q61](#s63) | success | ["intercom__company_enhanced"] | 0 / {} | [] | [] | 1426 | 9.94 |
| [S64/Q62](#s64) | success | ["intercom__conversation_enhanced"] | 0 / {} | ["event_type"] | ["COUNT(*)", "COUNT(DISTINCT company_name)"] | 2 | 5.029 |
| [S65/Q63](#s65) | success | ["intercom__conversation_enhanced"] | 0 / {} | [] | [] | 20 | 5.392 |
| [S66/Q64](#s66) | success | ["intercom__conversation_enhanced"] | 0 / {} | ["company_name", "event_type"] | ["MIN(conversation_created_at)", "COUNT(*)"] | 45 | 5.461 |
| [S67/Q65](#s67) | success | ["intercom__company_enhanced"] | 0 / {} | [] | [] | 1426 | 15.599 |
| [S68/Q66](#s68) | success | ["intercom__conversation_enhanced"] | 0 / {} | [] | [] | 6703 | 10.845 |
| [S69/Q67](#s69) | success | ["intercom__company_enhanced", "intercom__company_metrics"] | 2 / {'INNER': 1} | [] | [] | 2509 | 21.493 |
| [S70/Q68](#s70) | success | ["intercom__company_enhanced", "intercom__company_metrics"] | 2 / {'INNER': 1} | [] | [] | 2509 | 11.854 |
| [S71/Q69](#s71) | success | ["intercom__company_enhanced"] | 0 / {} | [] | [] | 1426 | 15.148 |
| [S72/Q70](#s72) | success | ["intercom__conversation_enhanced"] | 0 / {} | [] | [] | 6703 | 12.018 |
| [S73/Q71](#s73) | success | ["intercom__conversation_enhanced"] | 0 / {} | [] | [] | 6703 | 6.897 |
| [S74/Q72](#s74) | success | ["intercom__company_enhanced"] | 0 / {} | ["company_name"] | ["SUM(delta)", "COUNT(*)"] | 520 | 7.974 |


## 元数据和设置

| SQL | 类别 | 状态 | 内容 |
| --- | --- | --- | --- |
| S1 | connection_setup | success | PRAGMA query_only=ON |
| S2 | metadata | success | SELECT name,sql FROM sqlite_master WHERE type='table' ORDER BY name |


## Python 与执行位置

人工源码审查：**database_first_violation**。Python 将事件窗口内会话明细按事件和前后期聚合计数、金额及标签数，再 pivot、计算前后差值和变化率并按升级降级求均值。这些 GROUP BY、条件聚合和算术可在 SQL 中完成。配对及组间 t 检验为统计补充。 [证据](../reviews/dacomp-099.json)。

P1：Compute per-event aggregate metrics (conversation count, bug rate, outage rate, SLA breach rate, etc.) per period (before/after) for each event, then compare upgrade vs downgrade events using statistical tests. This requires reshaping data and computing statistics that are more naturally done in Python.

[源码](../../../runs/dsv4flash-db-first-full-01/dacomp-099/attempt-01/python/P1.py)；[输出](../../../runs/dsv4flash-db-first-full-01/dacomp-099/attempt-01/python/P1.stdout)；[错误](../../../runs/dsv4flash-db-first-full-01/dacomp-099/attempt-01/python/P1.stderr)。检出需人工核验的 SQL 可实现操作：.query(；不能仅凭理由判为合规。

P2：Retry loading the per-event conversation-level dataset using db.frame so column names are preserved, for subsequent per-event aggregation and statistical comparison in Python.

[源码](../../../runs/dsv4flash-db-first-full-01/dacomp-099/attempt-01/python/P2.py)；[输出](../../../runs/dsv4flash-db-first-full-01/dacomp-099/attempt-01/python/P2.stdout)；[错误](../../../runs/dsv4flash-db-first-full-01/dacomp-099/attempt-01/python/P2.stderr)。检出需人工核验的 SQL 可实现操作：.query(；不能仅凭理由判为合规。

P3：Aggregate per-event metrics across 30-day windows before/after each subscription change, compute deltas, and perform paired t-tests to compare before vs after within upgrade and downgrade event groups. This reshaping and statistical testing is more natural in Python than SQL.

[源码](../../../runs/dsv4flash-db-first-full-01/dacomp-099/attempt-01/python/P3.py)；[输出](../../../runs/dsv4flash-db-first-full-01/dacomp-099/attempt-01/python/P3.stdout)；[错误](../../../runs/dsv4flash-db-first-full-01/dacomp-099/attempt-01/python/P3.stderr)。检出需人工核验的 SQL 可实现操作：groupby(；不能仅凭理由判为合规。

P4：Load the event-conversation dataset, aggregate per-event metrics for 30-day before/after windows, and run paired t-tests (within group) and independent t-tests (between upgrade/downgrade groups) since statistical hypothesis testing is not a core SQLite capability.

[源码](../../../runs/dsv4flash-db-first-full-01/dacomp-099/attempt-01/python/P4.py)；[输出](../../../runs/dsv4flash-db-first-full-01/dacomp-099/attempt-01/python/P4.stdout)；[错误](../../../runs/dsv4flash-db-first-full-01/dacomp-099/attempt-01/python/P4.stderr)。检出需人工核验的 SQL 可实现操作：groupby(, .query(；不能仅凭理由判为合规。

P5：Build the per-event 30-day window dataset in Python because it requires datetime arithmetic, per-window aggregation, and handling of truncated windows (events at the edge of a company's observed conversation history). This is beyond SQLite's simpler date operations and needs flexible per-event iteration.

[源码](../../../runs/dsv4flash-db-first-full-01/dacomp-099/attempt-01/python/P5.py)；[输出](../../../runs/dsv4flash-db-first-full-01/dacomp-099/attempt-01/python/P5.stdout)；[错误](../../../runs/dsv4flash-db-first-full-01/dacomp-099/attempt-01/python/P5.stderr)。检出需人工核验的 SQL 可实现操作：.query(；不能仅凭理由判为合规。

P6：Diagnose why the previous full-conversation query was marked incomplete, testing a smaller filtered query for one company.

[源码](../../../runs/dsv4flash-db-first-full-01/dacomp-099/attempt-01/python/P6.py)；[输出](../../../runs/dsv4flash-db-first-full-01/dacomp-099/attempt-01/python/P6.stdout)；[错误](../../../runs/dsv4flash-db-first-full-01/dacomp-099/attempt-01/python/P6.stderr)。检出需人工核验的 SQL 可实现操作：.query(；不能仅凭理由判为合规。

P7：Diagnose result completeness: test whether the JOIN caused incompleteness or whether conversation_enhanced itself has issues (e.g., duplicate ids) making the result flagged incomplete.

[源码](../../../runs/dsv4flash-db-first-full-01/dacomp-099/attempt-01/python/P7.py)；[输出](../../../runs/dsv4flash-db-first-full-01/dacomp-099/attempt-01/python/P7.stdout)；[错误](../../../runs/dsv4flash-db-first-full-01/dacomp-099/attempt-01/python/P7.stderr)。检出需人工核验的 SQL 可实现操作：.query(；不能仅凭理由判为合规。

P8：Load conversation and metrics data separately (avoiding SQL incomplete-result issue), merge in Python, then compute per-event 30-day window metrics including per-day rates to handle truncated windows, and run statistical tests (paired t-tests for within-group, independent t-tests for between-group comparisons).

[源码](../../../runs/dsv4flash-db-first-full-01/dacomp-099/attempt-01/python/P8.py)；[输出](../../../runs/dsv4flash-db-first-full-01/dacomp-099/attempt-01/python/P8.stdout)；[错误](../../../runs/dsv4flash-db-first-full-01/dacomp-099/attempt-01/python/P8.stderr)。检出需人工核验的 SQL 可实现操作：.merge(, .query(；不能仅凭理由判为合规。

P9：Inspect which specific events have conversation data in their 30-day windows to understand the data coverage and validate the analysis sample.

[源码](../../../runs/dsv4flash-db-first-full-01/dacomp-099/attempt-01/python/P9.py)；[输出](../../../runs/dsv4flash-db-first-full-01/dacomp-099/attempt-01/python/P9.stdout)；[错误](../../../runs/dsv4flash-db-first-full-01/dacomp-099/attempt-01/python/P9.stderr)。自动源码筛查未检出预设迁出信号；这不是全面语义合规证明。

P10：Try a broader approach: for each plan-change event, use the full plan period (from previous snapshot created_at to next snapshot created_at) as the before/after window instead of strictly 30 days. This captures more conversation data and provides richer per-event metrics for statistical comparison.

[源码](../../../runs/dsv4flash-db-first-full-01/dacomp-099/attempt-01/python/P10.py)；[输出](../../../runs/dsv4flash-db-first-full-01/dacomp-099/attempt-01/python/P10.stdout)；[错误](../../../runs/dsv4flash-db-first-full-01/dacomp-099/attempt-01/python/P10.stderr)。检出需人工核验的 SQL 可实现操作：.query(；不能仅凭理由判为合规。

P11：Perform between-group statistical comparisons (upgrade vs downgrade events) on before-period, after-period, and delta metrics using independent t-tests. Also create visualizations (scatter plots and bar charts) to illustrate the patterns. These statistical tests and matplotlib visualizations are not supported in SQLite.

[源码](../../../runs/dsv4flash-db-first-full-01/dacomp-099/attempt-01/python/P11.py)；[输出](../../../runs/dsv4flash-db-first-full-01/dacomp-099/attempt-01/python/P11.stdout)；[错误](../../../runs/dsv4flash-db-first-full-01/dacomp-099/attempt-01/python/P11.stderr)。检出需人工核验的 SQL 可实现操作：.merge(, .query(, sort_values(；不能仅凭理由判为合规。

P12：Merge per-event analysis with company-level metrics (aggregated by company name) and compare company characteristics between upgrade and downgrade events using independent t-tests. Also examine plan transition patterns and pre-event incident ratios. These comparisons and aggregations are more naturally done in Python.

[源码](../../../runs/dsv4flash-db-first-full-01/dacomp-099/attempt-01/python/P12.py)；[输出](../../../runs/dsv4flash-db-first-full-01/dacomp-099/attempt-01/python/P12.stdout)；[错误](../../../runs/dsv4flash-db-first-full-01/dacomp-099/attempt-01/python/P12.stderr)。检出需人工核验的 SQL 可实现操作：groupby(, .merge(, .query(；不能仅凭理由判为合规。

P13：Analyze the composition of conversation tags (incident and signal types) before vs after each plan change event, comparing upgrade and downgrade events. This requires per-conversation tag matching, aggregation, and pivot operations best done in Python.

[源码](../../../runs/dsv4flash-db-first-full-01/dacomp-099/attempt-01/python/P13.py)；[输出](../../../runs/dsv4flash-db-first-full-01/dacomp-099/attempt-01/python/P13.stdout)；[错误](../../../runs/dsv4flash-db-first-full-01/dacomp-099/attempt-01/python/P13.stderr)。检出需人工核验的 SQL 可实现操作：groupby(, .query(, sort_values(；不能仅凭理由判为合规。

P14：Create final summary visualizations comparing usage intensity and support incident metrics before/after plan changes, for upgrade vs downgrade events. Producing publication-ready charts and consolidating statistics requires matplotlib and scipy, which are not available in SQLite.

[源码](../../../runs/dsv4flash-db-first-full-01/dacomp-099/attempt-01/python/P14.py)；[输出](../../../runs/dsv4flash-db-first-full-01/dacomp-099/attempt-01/python/P14.stdout)；[错误](../../../runs/dsv4flash-db-first-full-01/dacomp-099/attempt-01/python/P14.stderr)。自动源码筛查未检出预设迁出信号；这不是全面语义合规证明。

P15：Compute company-level baseline conversation rates to contextualize event-window intensities (frequency changes relative to baseline), and summarize the net plan-change direction per company. This is the final consolidation step before writing the report.

[源码](../../../runs/dsv4flash-db-first-full-01/dacomp-099/attempt-01/python/P15.py)；[输出](../../../runs/dsv4flash-db-first-full-01/dacomp-099/attempt-01/python/P15.stdout)；[错误](../../../runs/dsv4flash-db-first-full-01/dacomp-099/attempt-01/python/P15.stderr)。检出需人工核验的 SQL 可实现操作：groupby(, .merge(, .query(, sort_values(；不能仅凭理由判为合规。

## 优化机会

已验证候选。筛选限于精确 SQL、相同自包含 CTE、相同单表完整过滤、可分解单表聚合；未覆盖任意 Join 等价和一般谓词蕴含。全部候选都是 offline，未测在线预测。

| 候选 | 类型 | 已有结果 | 覆盖 SQL | 后续次数 | 中间行数 | 验证 | 成本 |
| --- | --- | --- | --- | --- | --- | --- | --- |
| C1 | exact-result reuse | True | ["S16", "S20"] | 1 | unknown | not_verified_cap | Not tested |
| C2 | exact-result reuse | True | ["S46", "S47", "S48"] | 2 | 567 | verified | Not benchmarked; correctness alone does not establish net speedup. |
| C3 | common subexpression | False | ["S16", "S20"] | 1 | unknown | not_verified_cap | Not tested |
| C4 | common subexpression | False | ["S41", "S42", "S43", "S44", "S45", "S46", "S47", "S48", "S49", "S50", "S51", "S52", "S63", "S67", "S71"] | 14 | 2509 | verified | Not benchmarked; correctness alone does not establish net speedup. |
| C5 | aggregate MV | False | ["S17", "S22", "S39"] | 2 | unknown | not_verified_cap | Not tested |
| C6 | aggregate MV | False | ["S11", "S37", "S57"] | 2 | 6474 | verified | Not benchmarked; correctness alone does not establish net speedup. |
| C7 | common filtered view | False | ["S23", "S25", "S27"] | 2 | unknown | not_verified_cap | Not tested |
| C8 | aggregate MV | False | ["S23", "S27"] | 1 | unknown | not_verified_cap | Not tested |
| C9 | common filtered view | False | ["S24", "S26", "S28"] | 2 | unknown | not_verified_cap | Not tested |
| C10 | aggregate MV | False | ["S24", "S28"] | 1 | unknown | not_verified_cap | Not tested |
| C11 | common filtered view | False | ["S54", "S58"] | 1 | unknown | not_verified_cap | Not tested |


已验证覆盖（含触发查询、候选并集去重）：18/70 条成功数据 SQL。正确性仅针对当前数据库快照；未测性能的候选不能声称已加速。

[完整 build/rewrite 与比较证据](dacomp-099.analysis.json)。

### C4：common subexpression

Identical self-contained CTE body across queries.

原查询 [S41](#s41), [S42](#s42), [S43](#s43), [S44](#s44), [S45](#s45), [S46](#s46), [S47](#s47), [S48](#s48), [S49](#s49), [S50](#s50), [S51](#s51), [S52](#s52), [S63](#s63), [S67](#s67), [S71](#s71) → 新增共享状态 C4 → 后续 14 次可复用。该构建点为事后假设，不代表 Agent 当时预知后续。

构建定义：

```sql
SELECT company_id, company_name, plan_name, created_at, monthly_spend, CASE plan_name WHEN 'Starter' THEN 1 WHEN 'Growth' THEN 2 WHEN 'Scale' THEN 3 WHEN 'Enterprise' THEN 4 END AS tier FROM intercom__company_enhanced
```

受益查询 S41 的改写示例：

```sql
WITH tiers AS (SELECT * FROM temp.reuse_candidate), ordered AS (SELECT *, LAG(tier) OVER (PARTITION BY company_name ORDER BY created_at) AS prev_tier, LAG(plan_name) OVER (PARTITION BY company_name ORDER BY created_at) AS prev_plan FROM tiers) SELECT CASE WHEN tier > prev_tier THEN 'upgrade' WHEN tier < prev_tier THEN 'downgrade' ELSE 'no_change' END AS event_type, COUNT(*) AS events FROM ordered WHERE NOT prev_tier IS NULL GROUP BY event_type
```

| 原 SQL | 列名一致 | 结果一致 | 比较方法 |
| --- | --- | --- | --- |
| S41 | True | True | exact_multiset |
| S42 | True | True | ordered_numeric_tolerance |
| S43 | True | True | ordered_numeric_tolerance |
| S44 | True | True | exact_multiset |
| S45 | True | True | ordered_numeric_tolerance |
| S46 | True | True | ordered_numeric_tolerance |
| S47 | True | True | ordered_numeric_tolerance |
| S48 | True | True | ordered_numeric_tolerance |
| S49 | True | True | ordered_numeric_tolerance |
| S50 | True | True | exact_multiset |
| S51 | True | True | ordered_numeric_tolerance |
| S52 | True | True | exact_multiset |
| S63 | True | True | exact_multiset |
| S67 | True | True | exact_multiset |
| S71 | True | True | exact_multiset |


验证状态：verified；成本结论：Not benchmarked; correctness alone does not establish net speedup.

### C2：exact-result reuse

Identical normalized SQL and parameters; archive equality checked.

原查询 [S46](#s46), [S47](#s47), [S48](#s48) → 保留前序结果 S46 → 后续 2 次可复用。该构建点为事后假设，不代表 Agent 当时预知后续。

| 原 SQL | 列名一致 | 结果一致 | 比较方法 |
| --- | --- | --- | --- |
| S47 | True | True | ordered_numeric_tolerance |
| S48 | True | True | ordered_numeric_tolerance |


验证状态：verified；成本结论：Not benchmarked; correctness alone does not establish net speedup.

### C6：aggregate MV

Union of grouping keys; decomposable aggregate states; AVG uses SUM and non-NULL COUNT.

原查询 [S11](#s11), [S37](#s37), [S57](#s57) → 新增共享状态 C6 → 后续 2 次可复用。该构建点为事后假设，不代表 Agent 当时预知后续。

构建定义：

```sql
SELECT all_conversation_tags AS __g0, all_contact_company_names AS __g1, COUNT(*) AS __a0 FROM "intercom__conversation_enhanced"  GROUP BY all_conversation_tags, all_contact_company_names
```

受益查询 S11 的改写示例：

```sql
SELECT __g0 AS "all_conversation_tags", SUM(__a0) AS cnt FROM temp.reuse_candidate GROUP BY __g0 ORDER BY cnt DESC LIMIT 50
```

| 原 SQL | 列名一致 | 结果一致 | 比较方法 |
| --- | --- | --- | --- |
| S11 | True | True | ordered_numeric_tolerance |
| S37 | True | True | ordered_numeric_tolerance |
| S57 | True | True | exact_multiset |


验证状态：verified；成本结论：Not benchmarked; correctness alone does not establish net speedup.

结果依赖：自动记录 SQL→Python 的接口父调用，以及源码中引用归档文件的消费者；字面值相同不认定因果。模型方向选择需要人工读取消息，尚未做全面因果标注。

[原始报告](../../../runs/dsv4flash-db-first-full-01/dacomp-099/attempt-01/answer.md)；[统一消息](../../../runs/dsv4flash-db-first-full-01/dacomp-099/attempt-01/messages.jsonl)；[原始 OpenCode 事件](../../../runs/dsv4flash-db-first-full-01/dacomp-099/attempt-01/opencode.jsonl)；[SQL 引擎日志](../../../runs/dsv4flash-db-first-full-01/dacomp-099/attempt-01/sql_journal.jsonl)。

[可读报告（本地图片链接规范化）](../answers/dacomp-099.md)。原始回答保留，分析结论未改写。

## S1

类别 `connection_setup`；来源 `connection`；调用 `f7bf9e277212467886d860e280c480c2`；状态 `success`。

```sql
PRAGMA query_only=ON
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-099/attempt-01/sql/S1.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-099/attempt-01/sql/S1.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-099/attempt-01/results/S1.rows.jsonl)；完整：True；SHA256：`e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`。

## S2

类别 `metadata`；来源 `list_db`；调用 `f7bf9e277212467886d860e280c480c2`；状态 `success`。

```sql
SELECT name,sql FROM sqlite_master WHERE type='table' ORDER BY name
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-099/attempt-01/sql/S2.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-099/attempt-01/sql/S2.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-099/attempt-01/results/S2.rows.jsonl)；完整：True；SHA256：`30f2968ede0397045b1cb864675e9a27e4a50f67145a84442aaec161c9970a14`。

## S3

类别 `data`；来源 `query_db`；调用 `d498ee57d0c547899abfe577222ac9fa`；状态 `success`。

```sql
SELECT DISTINCT plan_name, plan_id FROM intercom__company_enhanced ORDER BY plan_name
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-099/attempt-01/sql/S3.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-099/attempt-01/sql/S3.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-099/attempt-01/results/S3.rows.jsonl)；完整：True；SHA256：`7169c772616363a162ccb2e65c1979c2070fbf2fbf77de2dfcedaa7ee809a673`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "intercom__company_enhanced", "kind": "base", "block": null, "base_tables": ["intercom__company_enhanced"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |


## S4

类别 `data`；来源 `query_db`；调用 `5e3021133a7a4ee59e03db0fb382f140`；状态 `success`。

```sql
SELECT DISTINCT plan_name, plan_id FROM intercom__company_metrics ORDER BY plan_name
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-099/attempt-01/sql/S4.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-099/attempt-01/sql/S4.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-099/attempt-01/results/S4.rows.jsonl)；完整：True；SHA256：`7169c772616363a162ccb2e65c1979c2070fbf2fbf77de2dfcedaa7ee809a673`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "intercom__company_metrics", "kind": "base", "block": null, "base_tables": ["intercom__company_metrics"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |


## S5

类别 `data`；来源 `query_db`；调用 `ba2ee6477de049bfb85db5bb3967af3a`；状态 `success`。

```sql
SELECT * FROM intercom__company_enhanced LIMIT 10
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-099/attempt-01/sql/S5.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-099/attempt-01/sql/S5.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-099/attempt-01/results/S5.rows.jsonl)；完整：True；SHA256：`630fc056683c73ed213751d47b00a37eba92e4b66cf9112ccb2b33a0cb63c87f`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "intercom__company_enhanced", "kind": "base", "block": null, "base_tables": ["intercom__company_enhanced"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |


## S6

类别 `data`；来源 `query_db`；调用 `6c4f6d1f080548deb36771656a1b0ecd`；状态 `success`。

```sql
SELECT company_id, COUNT(*) as cnt FROM intercom__company_enhanced GROUP BY company_id HAVING cnt > 1 ORDER BY cnt DESC LIMIT 20
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-099/attempt-01/sql/S6.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-099/attempt-01/sql/S6.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-099/attempt-01/results/S6.rows.jsonl)；完整：True；SHA256：`e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "intercom__company_enhanced", "kind": "base", "block": null, "base_tables": ["intercom__company_enhanced"]}] | [] | ["company_id"] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |


## S7

类别 `data`；来源 `query_db`；调用 `e790ee37e7a7406698907abe6c04826f`；状态 `success`。

```sql
SELECT company_id, COUNT(*) as cnt FROM intercom__company_metrics GROUP BY company_id HAVING cnt > 1 ORDER BY cnt DESC LIMIT 20
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-099/attempt-01/sql/S7.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-099/attempt-01/sql/S7.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-099/attempt-01/results/S7.rows.jsonl)；完整：True；SHA256：`e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "intercom__company_metrics", "kind": "base", "block": null, "base_tables": ["intercom__company_metrics"]}] | [] | ["company_id"] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |


## S8

类别 `data`；来源 `query_db`；调用 `272a786d548c4ff3acd7b20df54402d9`；状态 `success`。

```sql
SELECT * FROM intercom__company_metrics LIMIT 10
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-099/attempt-01/sql/S8.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-099/attempt-01/sql/S8.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-099/attempt-01/results/S8.rows.jsonl)；完整：True；SHA256：`d1b8bc6b41b069d10bcfc5edd6948a3fe48df9b83e6d3f30fb2efcd61780989c`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "intercom__company_metrics", "kind": "base", "block": null, "base_tables": ["intercom__company_metrics"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |


## S9

类别 `data`；来源 `query_db`；调用 `959b2fa231de4e1996842d3ec99af191`；状态 `success`。

```sql
SELECT COUNT(*) as total, COUNT(DISTINCT company_id) as companies FROM intercom__company_enhanced
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-099/attempt-01/sql/S9.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-099/attempt-01/sql/S9.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-099/attempt-01/results/S9.rows.jsonl)；完整：True；SHA256：`3075983bad26844b4798018501dc3aff97512786eb2fefbb52d3a5ab217284fa`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "intercom__company_enhanced", "kind": "base", "block": null, "base_tables": ["intercom__company_enhanced"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |
| B1 | COUNT(DISTINCT company_id) | [{"table": "intercom__company_enhanced", "column": "company_id"}] | [] | False |


## S10

类别 `data`；来源 `query_db`；调用 `73c32682c76d494fba610dfbba8a76b7`；状态 `success`。

```sql
SELECT COUNT(*) as total_convs, COUNT(DISTINCT conversation_id) as uniq_convs FROM intercom__conversation_metrics
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-099/attempt-01/sql/S10.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-099/attempt-01/sql/S10.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-099/attempt-01/results/S10.rows.jsonl)；完整：True；SHA256：`a33b5e98afcaa35683f077b9a6ea81b3e47f4af2fffed137cf8e33d6d6016199`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "intercom__conversation_metrics", "kind": "base", "block": null, "base_tables": ["intercom__conversation_metrics"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |
| B1 | COUNT(DISTINCT conversation_id) | [{"table": "intercom__conversation_metrics", "column": "conversation_id"}] | [] | False |


## S11

类别 `data`；来源 `query_db`；调用 `76b2671eb86a4390900105723dad90ab`；状态 `success`。

```sql
SELECT all_conversation_tags, COUNT(*) as cnt FROM intercom__conversation_enhanced GROUP BY all_conversation_tags ORDER BY cnt DESC LIMIT 50
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-099/attempt-01/sql/S11.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-099/attempt-01/sql/S11.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-099/attempt-01/results/S11.rows.jsonl)；完整：True；SHA256：`746dacc7e79b8aafaaf7539bc896e8ecd9dbd7777e931d5dbddb05c9990449e1`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "intercom__conversation_enhanced", "kind": "base", "block": null, "base_tables": ["intercom__conversation_enhanced"]}] | [] | ["all_conversation_tags"] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |


## S12

类别 `data`；来源 `query_db`；调用 `727cbe0297c74408ac2c2a47a56463a0`；状态 `success`。

```sql
SELECT DISTINCT conversation_type FROM intercom__conversation_enhanced
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-099/attempt-01/sql/S12.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-099/attempt-01/sql/S12.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-099/attempt-01/results/S12.rows.jsonl)；完整：True；SHA256：`6c9ac48932ce26a8f95a198091f88042aae756c4ddf3bee35378a73792969207`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "intercom__conversation_enhanced", "kind": "base", "block": null, "base_tables": ["intercom__conversation_enhanced"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |


## S13

类别 `data`；来源 `query_db`；调用 `2ca5683b10684b4ab290da9c18e4bc42`；状态 `success`。

```sql
SELECT DISTINCT conversation_initiated_type FROM intercom__conversation_enhanced
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-099/attempt-01/sql/S13.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-099/attempt-01/sql/S13.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-099/attempt-01/results/S13.rows.jsonl)；完整：True；SHA256：`f0eecbfa143202628a36290548ef8eedff9018babaa451b588661798f7b8df1b`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "intercom__conversation_enhanced", "kind": "base", "block": null, "base_tables": ["intercom__conversation_enhanced"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |


## S14

类别 `data`；来源 `query_db`；调用 `b5709e0cbfa8474ab2989014b35606e5`；状态 `success`。

```sql
SELECT DISTINCT conversation_state FROM intercom__conversation_enhanced
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-099/attempt-01/sql/S14.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-099/attempt-01/sql/S14.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-099/attempt-01/results/S14.rows.jsonl)；完整：True；SHA256：`c984d8d0d5acc8b1633b5bb0c06f4ff0ff3e31368bb1ebd6629f25928297f7ee`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "intercom__conversation_enhanced", "kind": "base", "block": null, "base_tables": ["intercom__conversation_enhanced"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |


## S15

类别 `data`；来源 `query_db`；调用 `9900e14a7a5d474387b2211e92571b55`；状态 `success`。

```sql
SELECT all_conversation_tags, COUNT(*) as cnt FROM intercom__conversation_enhanced WHERE all_conversation_tags IS NOT NULL AND all_conversation_tags != '' GROUP BY all_conversation_tags ORDER BY cnt DESC LIMIT 100
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-099/attempt-01/sql/S15.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-099/attempt-01/sql/S15.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-099/attempt-01/results/S15.rows.jsonl)；完整：True；SHA256：`1346ccb9ed5c980e1267f68ab5cd44cd8f9a459fb26db0fc7ef16bf5e61d8260`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "intercom__conversation_enhanced", "kind": "base", "block": null, "base_tables": ["intercom__conversation_enhanced"]}] | [] | ["all_conversation_tags"] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |


## S16

类别 `data`；来源 `query_db`；调用 `196d6edc070f4656910f883a710e1c2c`；状态 `success`。

```sql
WITH split AS (
  SELECT conversation_id, value as tag FROM intercom__conversation_enhanced, json_each('["' || replace(all_conversation_tags, ', ', '","') || '"]') WHERE all_conversation_tags IS NOT NULL AND all_conversation_tags != ''
)
SELECT tag, COUNT(*) as cnt FROM split GROUP BY tag ORDER BY cnt DESC
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-099/attempt-01/sql/S16.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-099/attempt-01/sql/S16.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-099/attempt-01/results/S16.rows.jsonl)；完整：True；SHA256：`73202d33f4ee85334b77587a7d8a4401d2da31b40254281a9c713d59457e0df2`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "intercom__conversation_enhanced", "kind": "base", "block": null, "base_tables": ["intercom__conversation_enhanced"]}, {"alias": "", "kind": "base", "block": null, "base_tables": ["JSON_EACH('[\"' \|\| REPLACE(all_conversation_tags, ', ', '\",\"') \|\| '\"]')"]}] | [{"type": "CROSS", "right": "JSON_EACH('[\"' \|\| REPLACE(all_conversation_tags, ', ', '\",\"') \|\| '\"]')", "on": null, "using": []}] | [] |
| B2 | [{"alias": "split", "kind": "derived", "block": "B1", "base_tables": ["JSON_EACH('[\"' \|\| REPLACE(all_conversation_tags, ', ', '\",\"') \|\| '\"]')", "intercom__conversation_enhanced"]}] | [] | ["tag"] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B2 | COUNT(*) | [] | [] | True |


未解析列血缘：[{"block": "B2", "column": "value", "reason": "ambiguous_or_missing_source"}, {"block": "B2", "column": "value", "reason": "ambiguous_or_missing_source"}, {"block": "B2", "column": "value", "reason": "ambiguous_or_missing_source"}, {"block": "B2", "column": "value", "reason": "ambiguous_or_missing_source"}]

## S17

类别 `data`；来源 `query_db`；调用 `907ef13768d44ae9b3d022ed8579695e`；状态 `success`。

```sql
SELECT all_company_tags, COUNT(*) as cnt FROM intercom__company_enhanced GROUP BY all_company_tags ORDER BY cnt DESC LIMIT 100
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-099/attempt-01/sql/S17.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-099/attempt-01/sql/S17.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-099/attempt-01/results/S17.rows.jsonl)；完整：True；SHA256：`31196b13de1a8a0db226f51e7d1df9c021643fa10671b6d83caf67e332aa0a57`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "intercom__company_enhanced", "kind": "base", "block": null, "base_tables": ["intercom__company_enhanced"]}] | [] | ["all_company_tags"] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |


## S18

类别 `data`；来源 `query_db`；调用 `f9cd164c64854cce86960acc24d526c7`；状态 `success`。

```sql
WITH split AS (
  SELECT company_id, value as tag FROM intercom__company_enhanced, json_each('["' || replace(all_company_tags, ', ', '","') || '"]') WHERE all_company_tags IS NOT NULL AND all_company_tags != ''
)
SELECT tag, COUNT(*) as cnt FROM split GROUP BY tag ORDER BY cnt DESC
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-099/attempt-01/sql/S18.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-099/attempt-01/sql/S18.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-099/attempt-01/results/S18.rows.jsonl)；完整：True；SHA256：`726f169418849fd853e9439c648b4676d2dae57efa1fdf8938b113e3c1878090`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "intercom__company_enhanced", "kind": "base", "block": null, "base_tables": ["intercom__company_enhanced"]}, {"alias": "", "kind": "base", "block": null, "base_tables": ["JSON_EACH('[\"' \|\| REPLACE(all_company_tags, ', ', '\",\"') \|\| '\"]')"]}] | [{"type": "CROSS", "right": "JSON_EACH('[\"' \|\| REPLACE(all_company_tags, ', ', '\",\"') \|\| '\"]')", "on": null, "using": []}] | [] |
| B2 | [{"alias": "split", "kind": "derived", "block": "B1", "base_tables": ["JSON_EACH('[\"' \|\| REPLACE(all_company_tags, ', ', '\",\"') \|\| '\"]')", "intercom__company_enhanced"]}] | [] | ["tag"] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B2 | COUNT(*) | [] | [] | True |


未解析列血缘：[{"block": "B2", "column": "value", "reason": "ambiguous_or_missing_source"}, {"block": "B2", "column": "value", "reason": "ambiguous_or_missing_source"}, {"block": "B2", "column": "value", "reason": "ambiguous_or_missing_source"}, {"block": "B2", "column": "value", "reason": "ambiguous_or_missing_source"}]

## S19

类别 `data`；来源 `query_db`；调用 `7964c4f947e5495e841fb66ebd7155e2`；状态 `success`。

```sql
SELECT * FROM intercom__conversation_enhanced WHERE all_conversation_tags LIKE '%Bug%' OR all_conversation_tags LIKE '%Outage%' OR all_conversation_tags LIKE '%Downgrade%' OR all_conversation_tags LIKE '%Upgrade%' LIMIT 10
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-099/attempt-01/sql/S19.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-099/attempt-01/sql/S19.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-099/attempt-01/results/S19.rows.jsonl)；完整：True；SHA256：`ba4d12c05b30312015a621c1206a8544068d8fac25f9f7105f1c0ca715ed870c`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "intercom__conversation_enhanced", "kind": "base", "block": null, "base_tables": ["intercom__conversation_enhanced"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |


## S20

类别 `data`；来源 `query_db`；调用 `578ac202cbb2429eb492046004a2b7af`；状态 `success`。

```sql
WITH split AS (
  SELECT conversation_id, value as tag FROM intercom__conversation_enhanced, json_each('["' || replace(all_conversation_tags, ', ', '","') || '"]') WHERE all_conversation_tags IS NOT NULL AND all_conversation_tags != ''
)
SELECT tag, COUNT(*) as cnt FROM split GROUP BY tag ORDER BY cnt DESC
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-099/attempt-01/sql/S20.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-099/attempt-01/sql/S20.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-099/attempt-01/results/S20.rows.jsonl)；完整：True；SHA256：`73202d33f4ee85334b77587a7d8a4401d2da31b40254281a9c713d59457e0df2`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "intercom__conversation_enhanced", "kind": "base", "block": null, "base_tables": ["intercom__conversation_enhanced"]}, {"alias": "", "kind": "base", "block": null, "base_tables": ["JSON_EACH('[\"' \|\| REPLACE(all_conversation_tags, ', ', '\",\"') \|\| '\"]')"]}] | [{"type": "CROSS", "right": "JSON_EACH('[\"' \|\| REPLACE(all_conversation_tags, ', ', '\",\"') \|\| '\"]')", "on": null, "using": []}] | [] |
| B2 | [{"alias": "split", "kind": "derived", "block": "B1", "base_tables": ["JSON_EACH('[\"' \|\| REPLACE(all_conversation_tags, ', ', '\",\"') \|\| '\"]')", "intercom__conversation_enhanced"]}] | [] | ["tag"] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B2 | COUNT(*) | [] | [] | True |


未解析列血缘：[{"block": "B2", "column": "value", "reason": "ambiguous_or_missing_source"}, {"block": "B2", "column": "value", "reason": "ambiguous_or_missing_source"}, {"block": "B2", "column": "value", "reason": "ambiguous_or_missing_source"}, {"block": "B2", "column": "value", "reason": "ambiguous_or_missing_source"}]

## S21

类别 `data`；来源 `query_db`；调用 `b657e8ee0cae481a9d67140dc2c59779`；状态 `success`。

```sql
SELECT MIN(conversation_created_at) as min_c, MAX(conversation_created_at) as max_c FROM intercom__conversation_metrics
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-099/attempt-01/sql/S21.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-099/attempt-01/sql/S21.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-099/attempt-01/results/S21.rows.jsonl)；完整：True；SHA256：`755daaa7848a0fc0e2ae9c2233140f6ac8824294db89c8e2db9a44cdf66de319`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "intercom__conversation_metrics", "kind": "base", "block": null, "base_tables": ["intercom__conversation_metrics"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | MIN(conversation_created_at) | [{"table": "intercom__conversation_metrics", "column": "conversation_created_at"}] | [] | False |
| B1 | MAX(conversation_created_at) | [{"table": "intercom__conversation_metrics", "column": "conversation_created_at"}] | [] | False |


## S22

类别 `data`；来源 `query_db`；调用 `2a86544f005948efb91ce41b00bf4de3`；状态 `success`。

```sql
SELECT MIN(created_at) as min_c, MAX(created_at) as max_c, MIN(updated_at) as min_u, MAX(updated_at) as max_u FROM intercom__company_enhanced
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-099/attempt-01/sql/S22.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-099/attempt-01/sql/S22.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-099/attempt-01/results/S22.rows.jsonl)；完整：True；SHA256：`a1542159abbbc565552c2aed98471a623915df62c72bb91030e0dc2cf27ee266`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "intercom__company_enhanced", "kind": "base", "block": null, "base_tables": ["intercom__company_enhanced"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | MIN(created_at) | [{"table": "intercom__company_enhanced", "column": "created_at"}] | [] | False |
| B1 | MAX(created_at) | [{"table": "intercom__company_enhanced", "column": "created_at"}] | [] | False |
| B1 | MIN(updated_at) | [{"table": "intercom__company_enhanced", "column": "updated_at"}] | [] | False |
| B1 | MAX(updated_at) | [{"table": "intercom__company_enhanced", "column": "updated_at"}] | [] | False |


## S23

类别 `data`；来源 `query_db`；调用 `799ae62febdf49978d7b7b99088365b9`；状态 `success`。

```sql
SELECT COUNT(*) as total_tags FROM intercom__conversation_enhanced WHERE all_conversation_tags LIKE '%Upgrade Opportunity%'
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-099/attempt-01/sql/S23.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-099/attempt-01/sql/S23.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-099/attempt-01/results/S23.rows.jsonl)；完整：True；SHA256：`0c9b3005f133404d63191f49770e8a78fdf1e991d3f71b695d701a23c41b4eb1`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "intercom__conversation_enhanced", "kind": "base", "block": null, "base_tables": ["intercom__conversation_enhanced"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |


## S24

类别 `data`；来源 `query_db`；调用 `c4d3597368bf4f8dafecc5ab3a590f5f`；状态 `success`。

```sql
SELECT COUNT(*) as total_tags FROM intercom__conversation_enhanced WHERE all_conversation_tags LIKE '%Downgrade Risk%'
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-099/attempt-01/sql/S24.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-099/attempt-01/sql/S24.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-099/attempt-01/results/S24.rows.jsonl)；完整：True；SHA256：`6934c412e806182f091a56b50236e0e841a4ac940f4261a27c81e7e907f0853c`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "intercom__conversation_enhanced", "kind": "base", "block": null, "base_tables": ["intercom__conversation_enhanced"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |


## S25

类别 `data`；来源 `query_db`；调用 `31fb2d75d6ce490185130ec04d7784d1`；状态 `success`。

```sql
SELECT COUNT(DISTINCT all_contact_company_names) as companies_with_upgrade FROM intercom__conversation_enhanced WHERE all_conversation_tags LIKE '%Upgrade Opportunity%'
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-099/attempt-01/sql/S25.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-099/attempt-01/sql/S25.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-099/attempt-01/results/S25.rows.jsonl)；完整：True；SHA256：`741451fddea5a4c87ab16f573c86fe57287c9883428ecdfe0289c645e17ffbe2`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "intercom__conversation_enhanced", "kind": "base", "block": null, "base_tables": ["intercom__conversation_enhanced"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(DISTINCT all_contact_company_names) | [{"table": "intercom__conversation_enhanced", "column": "all_contact_company_names"}] | [] | False |


## S26

类别 `data`；来源 `query_db`；调用 `a600ed6e3e4247a1bc9c8f85b4ea5c8c`；状态 `success`。

```sql
SELECT COUNT(DISTINCT all_contact_company_names) as companies_with_downgrade FROM intercom__conversation_enhanced WHERE all_conversation_tags LIKE '%Downgrade Risk%'
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-099/attempt-01/sql/S26.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-099/attempt-01/sql/S26.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-099/attempt-01/results/S26.rows.jsonl)；完整：True；SHA256：`f956c525e57c2f0c72fdbed45067192af2d8601d308149b3dc068fecb266a1f3`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "intercom__conversation_enhanced", "kind": "base", "block": null, "base_tables": ["intercom__conversation_enhanced"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(DISTINCT all_contact_company_names) | [{"table": "intercom__conversation_enhanced", "column": "all_contact_company_names"}] | [] | False |


## S27

类别 `data`；来源 `query_db`；调用 `452adde744344c94b2a71d56c090baef`；状态 `success`。

```sql
SELECT all_contact_company_names, COUNT(*) as cnt FROM intercom__conversation_enhanced WHERE all_conversation_tags LIKE '%Upgrade Opportunity%' GROUP BY all_contact_company_names ORDER BY cnt DESC
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-099/attempt-01/sql/S27.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-099/attempt-01/sql/S27.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-099/attempt-01/results/S27.rows.jsonl)；完整：True；SHA256：`ef3c51c9f7dcfc8b8ee6dbc10e1c71b4f544f07123faed3285589264d54c0a17`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "intercom__conversation_enhanced", "kind": "base", "block": null, "base_tables": ["intercom__conversation_enhanced"]}] | [] | ["all_contact_company_names"] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |


## S28

类别 `data`；来源 `query_db`；调用 `1d41a95ae34648d1aa9d700d7d9fe4eb`；状态 `success`。

```sql
SELECT all_contact_company_names, COUNT(*) as cnt FROM intercom__conversation_enhanced WHERE all_conversation_tags LIKE '%Downgrade Risk%' GROUP BY all_contact_company_names ORDER BY cnt DESC
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-099/attempt-01/sql/S28.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-099/attempt-01/sql/S28.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-099/attempt-01/results/S28.rows.jsonl)；完整：True；SHA256：`d75d4568f9651d13787b1a20d5f51d8354c3308e0da993ad978c09673aaa85be`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "intercom__conversation_enhanced", "kind": "base", "block": null, "base_tables": ["intercom__conversation_enhanced"]}] | [] | ["all_contact_company_names"] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |


## S29

类别 `data`；来源 `query_db`；调用 `9dec382dfc2a4ac2b961be99af8b639c`；状态 `success`。

```sql
SELECT ce.company_id, ce.company_name, ce.plan_name, ce.monthly_spend, ce.user_count, ce.session_count, ce.all_company_tags
FROM intercom__company_enhanced ce
WHERE ce.company_name IN (
  SELECT all_contact_company_names FROM intercom__conversation_enhanced WHERE all_conversation_tags LIKE '%Upgrade Opportunity%'
)
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-099/attempt-01/sql/S29.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-099/attempt-01/sql/S29.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-099/attempt-01/results/S29.rows.jsonl)；完整：True；SHA256：`e0f9497fbd8c793369f6b8b7a8834e2f97233ee8f10376ec4901ee1fcb6a59b4`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "intercom__conversation_enhanced", "kind": "base", "block": null, "base_tables": ["intercom__conversation_enhanced"]}] | [] | [] |
| B2 | [{"alias": "ce", "kind": "base", "block": null, "base_tables": ["intercom__company_enhanced"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |


未解析列血缘：[{"block": "B2", "column": "all_contact_company_names", "reason": "ambiguous_or_missing_source"}, {"block": "B2", "column": "all_conversation_tags", "reason": "ambiguous_or_missing_source"}]

## S30

类别 `data`；来源 `query_db`；调用 `847afdecb10a47f0935e9eba48bce2c7`；状态 `success`。

```sql
SELECT ce.company_id, ce.company_name, ce.plan_name, ce.monthly_spend, ce.user_count, ce.session_count, ce.all_company_tags
FROM intercom__company_enhanced ce
WHERE ce.company_name IN (
  SELECT all_contact_company_names FROM intercom__conversation_enhanced WHERE all_conversation_tags LIKE '%Downgrade Risk%'
)
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-099/attempt-01/sql/S30.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-099/attempt-01/sql/S30.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-099/attempt-01/results/S30.rows.jsonl)；完整：True；SHA256：`49ecadfc0674927b22b14562258c1c90c56ab426b949f7ffb670fade007b4fa8`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "intercom__conversation_enhanced", "kind": "base", "block": null, "base_tables": ["intercom__conversation_enhanced"]}] | [] | [] |
| B2 | [{"alias": "ce", "kind": "base", "block": null, "base_tables": ["intercom__company_enhanced"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |


未解析列血缘：[{"block": "B2", "column": "all_contact_company_names", "reason": "ambiguous_or_missing_source"}, {"block": "B2", "column": "all_conversation_tags", "reason": "ambiguous_or_missing_source"}]

## S31

类别 `data`；来源 `query_db`；调用 `f85550a76cef45478ba344979538f953`；状态 `success`。

```sql
SELECT company_name, COUNT(DISTINCT company_id) as cnt, COUNT(DISTINCT plan_name) as plan_cnt, GROUP_CONCAT(DISTINCT plan_name) as plans, GROUP_CONCAT(DISTINCT monthly_spend) as spends
FROM intercom__company_enhanced
GROUP BY company_name
HAVING cnt > 1
ORDER BY cnt DESC
LIMIT 30
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-099/attempt-01/sql/S31.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-099/attempt-01/sql/S31.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-099/attempt-01/results/S31.rows.jsonl)；完整：True；SHA256：`de6ea07c64e6ec8931f04f183b7ce5bb595b77e5771835dafd00b2d63110d8ba`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "intercom__company_enhanced", "kind": "base", "block": null, "base_tables": ["intercom__company_enhanced"]}] | [] | ["company_name"] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(DISTINCT company_id) | [{"table": "intercom__company_enhanced", "column": "company_id"}] | [] | False |
| B1 | COUNT(DISTINCT plan_name) | [{"table": "intercom__company_enhanced", "column": "plan_name"}] | [] | False |
| B1 | GROUP_CONCAT(DISTINCT plan_name) | [{"table": "intercom__company_enhanced", "column": "plan_name"}] | [] | False |
| B1 | GROUP_CONCAT(DISTINCT monthly_spend) | [{"table": "intercom__company_enhanced", "column": "monthly_spend"}] | [] | False |


## S32

类别 `data`；来源 `query_db`；调用 `18c8b784ee16473e90abe0d4ea669a95`；状态 `success`。

```sql
SELECT company_name, company_id, plan_name, monthly_spend, created_at, updated_at, user_count, session_count
FROM intercom__company_enhanced
WHERE company_name = 'Pioneer Group'
ORDER BY created_at
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-099/attempt-01/sql/S32.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-099/attempt-01/sql/S32.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-099/attempt-01/results/S32.rows.jsonl)；完整：True；SHA256：`16faa95ba02e02ccecb77c0d247bb83e2d128054b6a8f9d9db56c5741a4a681b`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "intercom__company_enhanced", "kind": "base", "block": null, "base_tables": ["intercom__company_enhanced"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |


## S33

类别 `data`；来源 `query_db`；调用 `b4b98cd28c4449aa873afdac55ac6f31`；状态 `success`。

```sql
SELECT company_name, COUNT(DISTINCT company_id) as cnt, COUNT(DISTINCT plan_name) as plan_cnt
FROM intercom__company_enhanced
GROUP BY company_name
HAVING cnt > 1
ORDER BY cnt DESC
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-099/attempt-01/sql/S33.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-099/attempt-01/sql/S33.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-099/attempt-01/results/S33.rows.jsonl)；完整：True；SHA256：`1b2fd56e12eab97ecb738086763538993c6874e6f2ef4496f20913efe894edd3`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "intercom__company_enhanced", "kind": "base", "block": null, "base_tables": ["intercom__company_enhanced"]}] | [] | ["company_name"] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(DISTINCT company_id) | [{"table": "intercom__company_enhanced", "column": "company_id"}] | [] | False |
| B1 | COUNT(DISTINCT plan_name) | [{"table": "intercom__company_enhanced", "column": "plan_name"}] | [] | False |


## S34

类别 `data`；来源 `query_db`；调用 `ad93421a283f494dbe5d19d7856cf516`；状态 `success`。

```sql
SELECT COUNT(*) as total_convs, COUNT(DISTINCT all_contact_company_names) as companies_in_convs FROM intercom__conversation_enhanced
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-099/attempt-01/sql/S34.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-099/attempt-01/sql/S34.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-099/attempt-01/results/S34.rows.jsonl)；完整：True；SHA256：`635ea6cd99e13ec2a51e2a7fd977ee6e57648718550c5f7ccdba4e287f9bfb6c`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "intercom__conversation_enhanced", "kind": "base", "block": null, "base_tables": ["intercom__conversation_enhanced"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |
| B1 | COUNT(DISTINCT all_contact_company_names) | [{"table": "intercom__conversation_enhanced", "column": "all_contact_company_names"}] | [] | False |


## S35

类别 `data`；来源 `query_db`；调用 `3162421211314da984e665c235afb25a`；状态 `success`。

```sql
SELECT COUNT(DISTINCT company_name) as total_customer_names FROM intercom__company_enhanced
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-099/attempt-01/sql/S35.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-099/attempt-01/sql/S35.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-099/attempt-01/results/S35.rows.jsonl)；完整：True；SHA256：`93ecbf2c3012db9534888e8517b1d74592c85173084d660927c1608a7f868674`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "intercom__company_enhanced", "kind": "base", "block": null, "base_tables": ["intercom__company_enhanced"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(DISTINCT company_name) | [{"table": "intercom__company_enhanced", "column": "company_name"}] | [] | False |


## S36

类别 `data`；来源 `query_db`；调用 `b68e34647f184001bbb2bba65ecde24f`；状态 `success`。

```sql
SELECT COUNT(*) as matched FROM intercom__conversation_enhanced c INNER JOIN intercom__company_enhanced ce ON ce.company_name = c.all_contact_company_names
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-099/attempt-01/sql/S36.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-099/attempt-01/sql/S36.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-099/attempt-01/results/S36.rows.jsonl)；完整：True；SHA256：`38c5b785288cc41f897a8b78e0810d2f00ca2d31e486200f5c5f1204be9a33a9`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "c", "kind": "base", "block": null, "base_tables": ["intercom__conversation_enhanced"]}, {"alias": "ce", "kind": "base", "block": null, "base_tables": ["intercom__company_enhanced"]}] | [{"type": "INNER", "right": "intercom__company_enhanced AS ce", "on": "ce.company_name = c.all_contact_company_names", "using": []}] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |


## S37

类别 `data`；来源 `query_db`；调用 `59d451d5d3394ceeb4dd2b36ca2a0f9d`；状态 `success`。

```sql
SELECT all_contact_company_names, COUNT(*) as cnt FROM intercom__conversation_enhanced GROUP BY all_contact_company_names ORDER BY cnt DESC
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-099/attempt-01/sql/S37.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-099/attempt-01/sql/S37.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-099/attempt-01/results/S37.rows.jsonl)；完整：True；SHA256：`b9fe51f0a8fd8c1f7ec2b2726af7a5ef624ace235cfdb71410fd858cdf2f991b`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "intercom__conversation_enhanced", "kind": "base", "block": null, "base_tables": ["intercom__conversation_enhanced"]}] | [] | ["all_contact_company_names"] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |


## S38

类别 `data`；来源 `query_db`；调用 `224083f73ceb4806aebb07e55e500db3`；状态 `success`。

```sql
SELECT ce.company_name, COUNT(*) as snapshots, COUNT(DISTINCT ce.plan_name) as plans, GROUP_CONCAT(DISTINCT ce.plan_name) as plan_list
FROM intercom__company_enhanced ce
WHERE ce.company_name IN (SELECT DISTINCT all_contact_company_names FROM intercom__conversation_enhanced)
GROUP BY ce.company_name
ORDER BY snapshots DESC
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-099/attempt-01/sql/S38.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-099/attempt-01/sql/S38.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-099/attempt-01/results/S38.rows.jsonl)；完整：True；SHA256：`dd3c254b97fd2f78ac1814990cc70fcbaaaa855c24fb2ac74ef8c05838e09198`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "intercom__conversation_enhanced", "kind": "base", "block": null, "base_tables": ["intercom__conversation_enhanced"]}] | [] | [] |
| B2 | [{"alias": "ce", "kind": "base", "block": null, "base_tables": ["intercom__company_enhanced"]}] | [] | ["ce.company_name"] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B2 | COUNT(*) | [] | [] | True |
| B2 | COUNT(DISTINCT ce.plan_name) | [{"table": "intercom__company_enhanced", "column": "plan_name"}] | [] | False |
| B2 | GROUP_CONCAT(DISTINCT ce.plan_name) | [{"table": "intercom__company_enhanced", "column": "plan_name"}] | [] | False |


未解析列血缘：[{"block": "B2", "column": "all_contact_company_names", "reason": "ambiguous_or_missing_source"}]

## S39

类别 `data`；来源 `query_db`；调用 `7f3accd96f8d40d098734d44766ef0b8`；状态 `success`。

```sql
SELECT plan_name, COUNT(*) as n, ROUND(AVG(monthly_spend),0) as avg_spend, ROUND(MIN(monthly_spend),0) as min_spend, ROUND(MAX(monthly_spend),0) as max_spend, ROUND(AVG(session_count),0) as avg_sessions, ROUND(AVG(user_count),0) as avg_users
FROM intercom__company_enhanced
GROUP BY plan_name
ORDER BY avg_spend
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-099/attempt-01/sql/S39.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-099/attempt-01/sql/S39.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-099/attempt-01/results/S39.rows.jsonl)；完整：True；SHA256：`0b8d1eca4bf43af1b770f6dcf964c6892996d5dc2c05b74a4f8b956cdacb6b5e`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "intercom__company_enhanced", "kind": "base", "block": null, "base_tables": ["intercom__company_enhanced"]}] | [] | ["plan_name"] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |
| B1 | AVG(monthly_spend) | [{"table": "intercom__company_enhanced", "column": "monthly_spend"}] | [] | False |
| B1 | MIN(monthly_spend) | [{"table": "intercom__company_enhanced", "column": "monthly_spend"}] | [] | False |
| B1 | MAX(monthly_spend) | [{"table": "intercom__company_enhanced", "column": "monthly_spend"}] | [] | False |
| B1 | AVG(session_count) | [{"table": "intercom__company_enhanced", "column": "session_count"}] | [] | False |
| B1 | AVG(user_count) | [{"table": "intercom__company_enhanced", "column": "user_count"}] | [] | False |


## S40

类别 `data`；来源 `query_db`；调用 `483b609e79d341a190c4dd163962d641`；状态 `success`。

```sql
SELECT ce.company_name, ce.plan_name, ce.monthly_spend, ce.created_at
FROM intercom__company_enhanced ce
WHERE ce.company_name = 'River Analytics'
ORDER BY ce.created_at
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-099/attempt-01/sql/S40.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-099/attempt-01/sql/S40.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-099/attempt-01/results/S40.rows.jsonl)；完整：True；SHA256：`f1bcefe3a9df6195592b71eb744cdcc758f9c21dd0f864d2e3bcc948ede13ad5`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "ce", "kind": "base", "block": null, "base_tables": ["intercom__company_enhanced"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |


## S41

类别 `data`；来源 `query_db`；调用 `2686f5195a814adbb09edfbef44385f1`；状态 `success`。

```sql
WITH tiers AS (
  SELECT company_id, company_name, plan_name, created_at, monthly_spend,
    CASE plan_name WHEN 'Starter' THEN 1 WHEN 'Growth' THEN 2 WHEN 'Scale' THEN 3 WHEN 'Enterprise' THEN 4 END AS tier
  FROM intercom__company_enhanced
),
ordered AS (
  SELECT *, LAG(tier) OVER (PARTITION BY company_name ORDER BY created_at) AS prev_tier,
         LAG(plan_name) OVER (PARTITION BY company_name ORDER BY created_at) AS prev_plan
  FROM tiers
)
SELECT 
  CASE WHEN tier > prev_tier THEN 'upgrade' WHEN tier < prev_tier THEN 'downgrade' ELSE 'no_change' END AS event_type,
  COUNT(*) AS events
FROM ordered
WHERE prev_tier IS NOT NULL
GROUP BY event_type
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-099/attempt-01/sql/S41.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-099/attempt-01/sql/S41.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-099/attempt-01/results/S41.rows.jsonl)；完整：True；SHA256：`036b5e6837928b07feb62c943f9ec852a25d9e604fd2be29c87bf08ade440f3c`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "intercom__company_enhanced", "kind": "base", "block": null, "base_tables": ["intercom__company_enhanced"]}] | [] | [] |
| B2 | [{"alias": "tiers", "kind": "derived", "block": "B1", "base_tables": ["intercom__company_enhanced"]}] | [] | [] |
| B3 | [{"alias": "ordered", "kind": "derived", "block": "B2", "base_tables": ["intercom__company_enhanced"]}] | [] | ["CASE WHEN tier > prev_tier THEN 'upgrade' WHEN tier < prev_tier THEN 'downgrade' ELSE 'no_change' END"] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B3 | COUNT(*) | [] | [] | True |


## S42

类别 `data`；来源 `query_db`；调用 `49689b81e64e4a808074cb504e67becb`；状态 `success`。

```sql
WITH tiers AS (
  SELECT company_id, company_name, plan_name, created_at, monthly_spend,
    CASE plan_name WHEN 'Starter' THEN 1 WHEN 'Growth' THEN 2 WHEN 'Scale' THEN 3 WHEN 'Enterprise' THEN 4 END AS tier
  FROM intercom__company_enhanced
),
ordered AS (
  SELECT *, LAG(tier) OVER (PARTITION BY company_name ORDER BY created_at) AS prev_tier,
         LAG(plan_name) OVER (PARTITION BY company_name ORDER BY created_at) AS prev_plan,
         LAG(created_at) OVER (PARTITION BY company_name ORDER BY created_at) AS prev_time
  FROM tiers
)
SELECT company_name, created_at AS event_at, prev_plan, plan_name AS new_plan, prev_tier, tier,
       CASE WHEN tier > prev_tier THEN 'upgrade' ELSE 'downgrade' END AS event_type
FROM ordered
WHERE prev_tier IS NOT NULL AND tier <> prev_tier
  AND company_name IN (SELECT DISTINCT all_contact_company_names FROM intercom__conversation_enhanced)
ORDER BY company_name, event_at
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-099/attempt-01/sql/S42.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-099/attempt-01/sql/S42.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-099/attempt-01/results/S42.rows.jsonl)；完整：True；SHA256：`95720117efde00684c4fb2e1a4bf1dcb3395a67d2fe0ed75dcb7512f36daae37`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "intercom__company_enhanced", "kind": "base", "block": null, "base_tables": ["intercom__company_enhanced"]}] | [] | [] |
| B2 | [{"alias": "tiers", "kind": "derived", "block": "B1", "base_tables": ["intercom__company_enhanced"]}] | [] | [] |
| B3 | [{"alias": "intercom__conversation_enhanced", "kind": "base", "block": null, "base_tables": ["intercom__conversation_enhanced"]}] | [] | [] |
| B4 | [{"alias": "ordered", "kind": "derived", "block": "B2", "base_tables": ["intercom__company_enhanced"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |


## S43

类别 `data`；来源 `query_db`；调用 `3797a63372d141639dfa1f2002229fd2`；状态 `success`。

```sql
-- Get events with conversation counts in 30-day windows
WITH tiers AS (
  SELECT company_id, company_name, plan_name, created_at, monthly_spend,
    CASE plan_name WHEN 'Starter' THEN 1 WHEN 'Growth' THEN 2 WHEN 'Scale' THEN 3 WHEN 'Enterprise' THEN 4 END AS tier
  FROM intercom__company_enhanced
),
ordered AS (
  SELECT *, LAG(tier) OVER (PARTITION BY company_name ORDER BY created_at) AS prev_tier,
         LAG(plan_name) OVER (PARTITION BY company_name ORDER BY created_at) AS prev_plan,
         LAG(created_at) OVER (PARTITION BY company_name ORDER BY created_at) AS prev_time
  FROM tiers
),
events AS (
  SELECT company_name, created_at AS event_at, prev_plan, plan_name AS new_plan, prev_tier, tier,
         CASE WHEN tier > prev_tier THEN 'upgrade' ELSE 'downgrade' END AS event_type
  FROM ordered
  WHERE prev_tier IS NOT NULL AND tier <> prev_tier
    AND company_name IN (SELECT DISTINCT all_contact_company_names FROM intercom__conversation_enhanced)
),
-- For each event, get conversations in the before window and after window
event_convs AS (
  SELECT e.company_name, e.event_at, e.event_type,
         c.conversation_created_at,
         CASE WHEN c.conversation_created_at < e.event_at THEN 'before' ELSE 'after' END AS period,
         cm.count_total_parts,
         CASE WHEN c.all_conversation_tags LIKE '%Bug%' THEN 1 ELSE 0 END AS is_bug,
         CASE WHEN c.all_conversation_tags LIKE '%Outage%' THEN 1 ELSE 0 END AS is_outage,
         CASE WHEN c.all_conversation_tags LIKE '%Escalation%' THEN 1 ELSE 0 END AS is_escalation,
         CASE WHEN c.all_conversation_tags LIKE '%Downgrade Risk%' THEN 1 ELSE 0 END AS is_downgrade_risk,
         CASE WHEN c.all_conversation_tags LIKE '%Upgrade Opportunity%' THEN 1 ELSE 0 END AS is_upgrade_opp,
         c.sla_status,
         c.conversation_rating
  FROM events e
  JOIN intercom__conversation_enhanced c ON c.all_contact_company_names = e.company_name
  LEFT JOIN intercom__conversation_metrics cm ON cm.conversation_id = c.conversation_id
  WHERE c.conversation_created_at >= datetime(e.event_at, '-30 days')
    AND c.conversation_created_at <= datetime(e.event_at, '+30 days')
    AND c.conversation_created_at != e.event_at
)
SELECT event_type, period, 
  COUNT(*) AS total_convs,
  ROUND(AVG(count_total_parts), 2) AS avg_parts,
  SUM(is_bug) AS bug_count,
  SUM(is_outage) AS outage_count,
  SUM(is_escalation) AS escalation_count,
  SUM(is_upgrade_opp) AS upgrade_opp_count,
  SUM(is_downgrade_risk) AS downgrade_risk_count,
  ROUND(AVG(CASE WHEN conversation_rating > 0 THEN conversation_rating END), 2) AS avg_rating,
  SUM(CASE WHEN sla_status = 'breached' THEN 1 ELSE 0 END) AS sla_breaches
FROM event_convs
GROUP BY event_type, period
ORDER BY event_type, period
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-099/attempt-01/sql/S43.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-099/attempt-01/sql/S43.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-099/attempt-01/results/S43.rows.jsonl)；完整：True；SHA256：`b9dcb11c47dd5fde29d316e57a55e0d3f18402203dde2bb804dd40fd9b4ac17f`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "intercom__company_enhanced", "kind": "base", "block": null, "base_tables": ["intercom__company_enhanced"]}] | [] | [] |
| B2 | [{"alias": "tiers", "kind": "derived", "block": "B1", "base_tables": ["intercom__company_enhanced"]}] | [] | [] |
| B3 | [{"alias": "intercom__conversation_enhanced", "kind": "base", "block": null, "base_tables": ["intercom__conversation_enhanced"]}] | [] | [] |
| B4 | [{"alias": "ordered", "kind": "derived", "block": "B2", "base_tables": ["intercom__company_enhanced"]}] | [] | [] |
| B5 | [{"alias": "e", "kind": "derived", "block": "B4", "base_tables": ["intercom__company_enhanced"]}, {"alias": "c", "kind": "base", "block": null, "base_tables": ["intercom__conversation_enhanced"]}, {"alias": "cm", "kind": "base", "block": null, "base_tables": ["intercom__conversation_metrics"]}] | [{"type": "INNER", "right": "intercom__conversation_enhanced AS c", "on": "c.all_contact_company_names = e.company_name", "using": []}, {"type": "LEFT", "right": "intercom__conversation_metrics AS cm", "on": "cm.conversation_id = c.conversation_id", "using": []}] | [] |
| B6 | [{"alias": "event_convs", "kind": "derived", "block": "B5", "base_tables": ["intercom__company_enhanced", "intercom__conversation_enhanced", "intercom__conversation_metrics"]}] | [] | ["event_type", "period"] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B6 | COUNT(*) | [] | [] | True |
| B6 | SUM(is_bug) | [{"table": "intercom__conversation_enhanced", "column": "all_conversation_tags"}] | [] | False |
| B6 | SUM(is_outage) | [{"table": "intercom__conversation_enhanced", "column": "all_conversation_tags"}] | [] | False |
| B6 | SUM(is_escalation) | [{"table": "intercom__conversation_enhanced", "column": "all_conversation_tags"}] | [] | False |
| B6 | SUM(is_upgrade_opp) | [{"table": "intercom__conversation_enhanced", "column": "all_conversation_tags"}] | [] | False |
| B6 | SUM(is_downgrade_risk) | [{"table": "intercom__conversation_enhanced", "column": "all_conversation_tags"}] | [] | False |
| B6 | SUM(CASE WHEN sla_status = 'breached' THEN 1 ELSE 0 END) | [] | [{"table": "intercom__conversation_enhanced", "column": "sla_status"}] | False |
| B6 | AVG(count_total_parts) | [{"table": "intercom__conversation_metrics", "column": "count_total_parts"}] | [] | False |
| B6 | AVG(CASE WHEN conversation_rating > 0 THEN conversation_rating END) | [{"table": "intercom__conversation_enhanced", "column": "conversation_rating"}] | [{"table": "intercom__conversation_enhanced", "column": "conversation_rating"}] | False |


未解析列血缘：[{"block": "B6", "column": "all_contact_company_names", "reason": "ambiguous_or_missing_source"}]

## S44

类别 `data`；来源 `query_db`；调用 `9568e6b658004e769d30d7571667bd0d`；状态 `success`。

```sql
WITH tiers AS (
  SELECT company_id, company_name, plan_name, created_at, monthly_spend,
    CASE plan_name WHEN 'Starter' THEN 1 WHEN 'Growth' THEN 2 WHEN 'Scale' THEN 3 WHEN 'Enterprise' THEN 4 END AS tier
  FROM intercom__company_enhanced
),
ordered AS (
  SELECT *, LAG(tier) OVER (PARTITION BY company_name ORDER BY created_at) AS prev_tier,
         LAG(plan_name) OVER (PARTITION BY company_name ORDER BY created_at) AS prev_plan
  FROM tiers
),
events AS (
  SELECT company_name, created_at AS event_at, prev_plan, plan_name AS new_plan, prev_tier, tier,
         CASE WHEN tier > prev_tier THEN 'upgrade' ELSE 'downgrade' END AS event_type
  FROM ordered
  WHERE prev_tier IS NOT NULL AND tier <> prev_tier
    AND company_name IN (SELECT DISTINCT all_contact_company_names FROM intercom__conversation_enhanced)
)
SELECT event_type, COUNT(*) AS event_count, COUNT(DISTINCT company_name) AS companies
FROM events
GROUP BY event_type
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-099/attempt-01/sql/S44.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-099/attempt-01/sql/S44.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-099/attempt-01/results/S44.rows.jsonl)；完整：True；SHA256：`0919a9b17ea0a779d7ab4a3c4619a89d3ca86c396b7f74979f54470b70122f9d`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "intercom__company_enhanced", "kind": "base", "block": null, "base_tables": ["intercom__company_enhanced"]}] | [] | [] |
| B2 | [{"alias": "tiers", "kind": "derived", "block": "B1", "base_tables": ["intercom__company_enhanced"]}] | [] | [] |
| B3 | [{"alias": "intercom__conversation_enhanced", "kind": "base", "block": null, "base_tables": ["intercom__conversation_enhanced"]}] | [] | [] |
| B4 | [{"alias": "ordered", "kind": "derived", "block": "B2", "base_tables": ["intercom__company_enhanced"]}] | [] | [] |
| B5 | [{"alias": "events", "kind": "derived", "block": "B4", "base_tables": ["intercom__company_enhanced"]}] | [] | ["event_type"] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B5 | COUNT(*) | [] | [] | True |
| B5 | COUNT(DISTINCT company_name) | [{"table": "intercom__company_enhanced", "column": "company_name"}] | [] | False |


未解析列血缘：[{"block": "B5", "column": "all_contact_company_names", "reason": "ambiguous_or_missing_source"}]

## S45

类别 `data`；来源 `query_db`；调用 `113a3edcabdf49959f6f56d7adce8bb2`；状态 `success`。

```sql
-- Per-event detailed metrics
WITH tiers AS (
  SELECT company_id, company_name, plan_name, created_at, monthly_spend,
    CASE plan_name WHEN 'Starter' THEN 1 WHEN 'Growth' THEN 2 WHEN 'Scale' THEN 3 WHEN 'Enterprise' THEN 4 END AS tier
  FROM intercom__company_enhanced
),
ordered AS (
  SELECT *, LAG(tier) OVER (PARTITION BY company_name ORDER BY created_at) AS prev_tier,
         LAG(plan_name) OVER (PARTITION BY company_name ORDER BY created_at) AS prev_plan
  FROM tiers
),
events AS (
  SELECT company_name, created_at AS event_at, prev_plan, plan_name AS new_plan, prev_tier, tier,
         CASE WHEN tier > prev_tier THEN 'upgrade' ELSE 'downgrade' END AS event_type,
         ROW_NUMBER() OVER (PARTITION BY company_name ORDER BY created_at) AS event_seq
  FROM ordered
  WHERE prev_tier IS NOT NULL AND tier <> prev_tier
    AND company_name IN (SELECT DISTINCT all_contact_company_names FROM intercom__conversation_enhanced)
),
event_metrics AS (
  SELECT e.company_name, e.event_at, e.event_type, e.prev_plan, e.new_plan,
         c.conversation_id, c.conversation_created_at,
         CASE WHEN c.conversation_created_at < e.event_at THEN 'before' ELSE 'after' END AS period,
         cm.count_total_parts,
         CASE WHEN c.all_conversation_tags LIKE '%Bug%' THEN 1 ELSE 0 END AS is_bug,
         CASE WHEN c.all_conversation_tags LIKE '%Outage%' THEN 1 ELSE 0 END AS is_outage,
         CASE WHEN c.all_conversation_tags LIKE '%Escalation%' THEN 1 ELSE 0 END AS is_escalation,
         CASE WHEN c.all_conversation_tags LIKE '%Renewal%' THEN 1 ELSE 0 END AS is_renewal,
         CASE WHEN c.sla_status = 'breached' THEN 1 ELSE 0 END AS is_sla_breach,
         CASE WHEN c.conversation_initiated_type = 'customer_initiated' THEN 1 ELSE 0 END AS is_customer_initiated,
         c.conversation_rating
  FROM events e
  JOIN intercom__conversation_enhanced c ON c.all_contact_company_names = e.company_name
  LEFT JOIN intercom__conversation_metrics cm ON cm.conversation_id = c.conversation_id
  WHERE c.conversation_created_at >= datetime(e.event_at, '-30 days')
    AND c.conversation_created_at <= datetime(e.event_at, '+30 days')
    AND c.conversation_created_at != e.event_at
)
SELECT * FROM event_metrics
ORDER BY company_name, event_at, conversation_created_at
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-099/attempt-01/sql/S45.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-099/attempt-01/sql/S45.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-099/attempt-01/results/S45.rows.jsonl)；完整：True；SHA256：`e2593f06ab9d75dda9987b16d0eab5c5a67833e05a60965a3a018e5d237469df`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "intercom__company_enhanced", "kind": "base", "block": null, "base_tables": ["intercom__company_enhanced"]}] | [] | [] |
| B2 | [{"alias": "tiers", "kind": "derived", "block": "B1", "base_tables": ["intercom__company_enhanced"]}] | [] | [] |
| B3 | [{"alias": "intercom__conversation_enhanced", "kind": "base", "block": null, "base_tables": ["intercom__conversation_enhanced"]}] | [] | [] |
| B4 | [{"alias": "ordered", "kind": "derived", "block": "B2", "base_tables": ["intercom__company_enhanced"]}] | [] | [] |
| B5 | [{"alias": "e", "kind": "derived", "block": "B4", "base_tables": ["intercom__company_enhanced"]}, {"alias": "c", "kind": "base", "block": null, "base_tables": ["intercom__conversation_enhanced"]}, {"alias": "cm", "kind": "base", "block": null, "base_tables": ["intercom__conversation_metrics"]}] | [{"type": "INNER", "right": "intercom__conversation_enhanced AS c", "on": "c.all_contact_company_names = e.company_name", "using": []}, {"type": "LEFT", "right": "intercom__conversation_metrics AS cm", "on": "cm.conversation_id = c.conversation_id", "using": []}] | [] |
| B6 | [{"alias": "event_metrics", "kind": "derived", "block": "B5", "base_tables": ["intercom__company_enhanced", "intercom__conversation_enhanced", "intercom__conversation_metrics"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |


未解析列血缘：[{"block": "B6", "column": "all_contact_company_names", "reason": "ambiguous_or_missing_source"}]

## S46

类别 `data`；来源 `python`；调用 `2ca2975d8a7d402ebaa053e8ff730aa7`；状态 `success`。

```sql

WITH tiers AS (
  SELECT company_id, company_name, plan_name, created_at, monthly_spend,
    CASE plan_name WHEN 'Starter' THEN 1 WHEN 'Growth' THEN 2 WHEN 'Scale' THEN 3 WHEN 'Enterprise' THEN 4 END AS tier
  FROM intercom__company_enhanced
),
ordered AS (
  SELECT *, LAG(tier) OVER (PARTITION BY company_name ORDER BY created_at) AS prev_tier,
         LAG(plan_name) OVER (PARTITION BY company_name ORDER BY created_at) AS prev_plan
  FROM tiers
),
events AS (
  SELECT company_name, created_at AS event_at, prev_plan, plan_name AS new_plan, prev_tier, tier,
         CASE WHEN tier > prev_tier THEN 'upgrade' ELSE 'downgrade' END AS event_type
  FROM ordered
  WHERE prev_tier IS NOT NULL AND tier <> prev_tier
    AND company_name IN (SELECT DISTINCT all_contact_company_names FROM intercom__conversation_enhanced)
),
event_metrics AS (
  SELECT e.company_name, e.event_at, e.event_type, e.prev_plan, e.new_plan,
         c.conversation_id, c.conversation_created_at,
         CASE WHEN c.conversation_created_at < e.event_at THEN 'before' ELSE 'after' END AS period,
         cm.count_total_parts,
         CASE WHEN c.all_conversation_tags LIKE '%Bug%' THEN 1 ELSE 0 END AS is_bug,
         CASE WHEN c.all_conversation_tags LIKE '%Outage%' THEN 1 ELSE 0 END AS is_outage,
         CASE WHEN c.all_conversation_tags LIKE '%Escalation%' THEN 1 ELSE 0 END AS is_escalation,
         CASE WHEN c.all_conversation_tags LIKE '%Renewal%' THEN 1 ELSE 0 END AS is_renewal,
         CASE WHEN c.sla_status = 'breached' THEN 1 ELSE 0 END AS is_sla_breach,
         CASE WHEN c.conversation_initiated_type = 'customer_initiated' THEN 1 ELSE 0 END AS is_customer_initiated,
         c.conversation_rating
  FROM events e
  JOIN intercom__conversation_enhanced c ON c.all_contact_company_names = e.company_name
  LEFT JOIN intercom__conversation_metrics cm ON cm.conversation_id = c.conversation_id
  WHERE c.conversation_created_at >= datetime(e.event_at, '-30 days')
    AND c.conversation_created_at <= datetime(e.event_at, '+30 days')
    AND c.conversation_created_at != e.event_at
)
SELECT * FROM event_metrics
ORDER BY company_name, event_at, conversation_created_at

```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-099/attempt-01/sql/S46.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-099/attempt-01/sql/S46.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-099/attempt-01/results/S46.rows.jsonl)；完整：True；SHA256：`e2593f06ab9d75dda9987b16d0eab5c5a67833e05a60965a3a018e5d237469df`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "intercom__company_enhanced", "kind": "base", "block": null, "base_tables": ["intercom__company_enhanced"]}] | [] | [] |
| B2 | [{"alias": "tiers", "kind": "derived", "block": "B1", "base_tables": ["intercom__company_enhanced"]}] | [] | [] |
| B3 | [{"alias": "intercom__conversation_enhanced", "kind": "base", "block": null, "base_tables": ["intercom__conversation_enhanced"]}] | [] | [] |
| B4 | [{"alias": "ordered", "kind": "derived", "block": "B2", "base_tables": ["intercom__company_enhanced"]}] | [] | [] |
| B5 | [{"alias": "e", "kind": "derived", "block": "B4", "base_tables": ["intercom__company_enhanced"]}, {"alias": "c", "kind": "base", "block": null, "base_tables": ["intercom__conversation_enhanced"]}, {"alias": "cm", "kind": "base", "block": null, "base_tables": ["intercom__conversation_metrics"]}] | [{"type": "INNER", "right": "intercom__conversation_enhanced AS c", "on": "c.all_contact_company_names = e.company_name", "using": []}, {"type": "LEFT", "right": "intercom__conversation_metrics AS cm", "on": "cm.conversation_id = c.conversation_id", "using": []}] | [] |
| B6 | [{"alias": "event_metrics", "kind": "derived", "block": "B5", "base_tables": ["intercom__company_enhanced", "intercom__conversation_enhanced", "intercom__conversation_metrics"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |


未解析列血缘：[{"block": "B6", "column": "all_contact_company_names", "reason": "ambiguous_or_missing_source"}]

## S47

类别 `data`；来源 `python`；调用 `d120601a2cfb45ccbe1f4785166a0abc`；状态 `success`。

```sql

WITH tiers AS (
  SELECT company_id, company_name, plan_name, created_at, monthly_spend,
    CASE plan_name WHEN 'Starter' THEN 1 WHEN 'Growth' THEN 2 WHEN 'Scale' THEN 3 WHEN 'Enterprise' THEN 4 END AS tier
  FROM intercom__company_enhanced
),
ordered AS (
  SELECT *, LAG(tier) OVER (PARTITION BY company_name ORDER BY created_at) AS prev_tier,
         LAG(plan_name) OVER (PARTITION BY company_name ORDER BY created_at) AS prev_plan
  FROM tiers
),
events AS (
  SELECT company_name, created_at AS event_at, prev_plan, plan_name AS new_plan, prev_tier, tier,
         CASE WHEN tier > prev_tier THEN 'upgrade' ELSE 'downgrade' END AS event_type
  FROM ordered
  WHERE prev_tier IS NOT NULL AND tier <> prev_tier
    AND company_name IN (SELECT DISTINCT all_contact_company_names FROM intercom__conversation_enhanced)
),
event_metrics AS (
  SELECT e.company_name, e.event_at, e.event_type, e.prev_plan, e.new_plan,
         c.conversation_id, c.conversation_created_at,
         CASE WHEN c.conversation_created_at < e.event_at THEN 'before' ELSE 'after' END AS period,
         cm.count_total_parts,
         CASE WHEN c.all_conversation_tags LIKE '%Bug%' THEN 1 ELSE 0 END AS is_bug,
         CASE WHEN c.all_conversation_tags LIKE '%Outage%' THEN 1 ELSE 0 END AS is_outage,
         CASE WHEN c.all_conversation_tags LIKE '%Escalation%' THEN 1 ELSE 0 END AS is_escalation,
         CASE WHEN c.all_conversation_tags LIKE '%Renewal%' THEN 1 ELSE 0 END AS is_renewal,
         CASE WHEN c.sla_status = 'breached' THEN 1 ELSE 0 END AS is_sla_breach,
         CASE WHEN c.conversation_initiated_type = 'customer_initiated' THEN 1 ELSE 0 END AS is_customer_initiated,
         c.conversation_rating
  FROM events e
  JOIN intercom__conversation_enhanced c ON c.all_contact_company_names = e.company_name
  LEFT JOIN intercom__conversation_metrics cm ON cm.conversation_id = c.conversation_id
  WHERE c.conversation_created_at >= datetime(e.event_at, '-30 days')
    AND c.conversation_created_at <= datetime(e.event_at, '+30 days')
    AND c.conversation_created_at != e.event_at
)
SELECT * FROM event_metrics
ORDER BY company_name, event_at, conversation_created_at

```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-099/attempt-01/sql/S47.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-099/attempt-01/sql/S47.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-099/attempt-01/results/S47.rows.jsonl)；完整：True；SHA256：`e2593f06ab9d75dda9987b16d0eab5c5a67833e05a60965a3a018e5d237469df`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "intercom__company_enhanced", "kind": "base", "block": null, "base_tables": ["intercom__company_enhanced"]}] | [] | [] |
| B2 | [{"alias": "tiers", "kind": "derived", "block": "B1", "base_tables": ["intercom__company_enhanced"]}] | [] | [] |
| B3 | [{"alias": "intercom__conversation_enhanced", "kind": "base", "block": null, "base_tables": ["intercom__conversation_enhanced"]}] | [] | [] |
| B4 | [{"alias": "ordered", "kind": "derived", "block": "B2", "base_tables": ["intercom__company_enhanced"]}] | [] | [] |
| B5 | [{"alias": "e", "kind": "derived", "block": "B4", "base_tables": ["intercom__company_enhanced"]}, {"alias": "c", "kind": "base", "block": null, "base_tables": ["intercom__conversation_enhanced"]}, {"alias": "cm", "kind": "base", "block": null, "base_tables": ["intercom__conversation_metrics"]}] | [{"type": "INNER", "right": "intercom__conversation_enhanced AS c", "on": "c.all_contact_company_names = e.company_name", "using": []}, {"type": "LEFT", "right": "intercom__conversation_metrics AS cm", "on": "cm.conversation_id = c.conversation_id", "using": []}] | [] |
| B6 | [{"alias": "event_metrics", "kind": "derived", "block": "B5", "base_tables": ["intercom__company_enhanced", "intercom__conversation_enhanced", "intercom__conversation_metrics"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |


未解析列血缘：[{"block": "B6", "column": "all_contact_company_names", "reason": "ambiguous_or_missing_source"}]

## S48

类别 `data`；来源 `python`；调用 `b385f90462674b7b8cc7470f644b3c40`；状态 `success`。

```sql

WITH tiers AS (
  SELECT company_id, company_name, plan_name, created_at, monthly_spend,
    CASE plan_name WHEN 'Starter' THEN 1 WHEN 'Growth' THEN 2 WHEN 'Scale' THEN 3 WHEN 'Enterprise' THEN 4 END AS tier
  FROM intercom__company_enhanced
),
ordered AS (
  SELECT *, LAG(tier) OVER (PARTITION BY company_name ORDER BY created_at) AS prev_tier,
         LAG(plan_name) OVER (PARTITION BY company_name ORDER BY created_at) AS prev_plan
  FROM tiers
),
events AS (
  SELECT company_name, created_at AS event_at, prev_plan, plan_name AS new_plan, prev_tier, tier,
         CASE WHEN tier > prev_tier THEN 'upgrade' ELSE 'downgrade' END AS event_type
  FROM ordered
  WHERE prev_tier IS NOT NULL AND tier <> prev_tier
    AND company_name IN (SELECT DISTINCT all_contact_company_names FROM intercom__conversation_enhanced)
),
event_metrics AS (
  SELECT e.company_name, e.event_at, e.event_type, e.prev_plan, e.new_plan,
         c.conversation_id, c.conversation_created_at,
         CASE WHEN c.conversation_created_at < e.event_at THEN 'before' ELSE 'after' END AS period,
         cm.count_total_parts,
         CASE WHEN c.all_conversation_tags LIKE '%Bug%' THEN 1 ELSE 0 END AS is_bug,
         CASE WHEN c.all_conversation_tags LIKE '%Outage%' THEN 1 ELSE 0 END AS is_outage,
         CASE WHEN c.all_conversation_tags LIKE '%Escalation%' THEN 1 ELSE 0 END AS is_escalation,
         CASE WHEN c.all_conversation_tags LIKE '%Renewal%' THEN 1 ELSE 0 END AS is_renewal,
         CASE WHEN c.sla_status = 'breached' THEN 1 ELSE 0 END AS is_sla_breach,
         CASE WHEN c.conversation_initiated_type = 'customer_initiated' THEN 1 ELSE 0 END AS is_customer_initiated,
         c.conversation_rating
  FROM events e
  JOIN intercom__conversation_enhanced c ON c.all_contact_company_names = e.company_name
  LEFT JOIN intercom__conversation_metrics cm ON cm.conversation_id = c.conversation_id
  WHERE c.conversation_created_at >= datetime(e.event_at, '-30 days')
    AND c.conversation_created_at <= datetime(e.event_at, '+30 days')
    AND c.conversation_created_at != e.event_at
)
SELECT * FROM event_metrics
ORDER BY company_name, event_at, conversation_created_at

```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-099/attempt-01/sql/S48.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-099/attempt-01/sql/S48.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-099/attempt-01/results/S48.rows.jsonl)；完整：True；SHA256：`e2593f06ab9d75dda9987b16d0eab5c5a67833e05a60965a3a018e5d237469df`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "intercom__company_enhanced", "kind": "base", "block": null, "base_tables": ["intercom__company_enhanced"]}] | [] | [] |
| B2 | [{"alias": "tiers", "kind": "derived", "block": "B1", "base_tables": ["intercom__company_enhanced"]}] | [] | [] |
| B3 | [{"alias": "intercom__conversation_enhanced", "kind": "base", "block": null, "base_tables": ["intercom__conversation_enhanced"]}] | [] | [] |
| B4 | [{"alias": "ordered", "kind": "derived", "block": "B2", "base_tables": ["intercom__company_enhanced"]}] | [] | [] |
| B5 | [{"alias": "e", "kind": "derived", "block": "B4", "base_tables": ["intercom__company_enhanced"]}, {"alias": "c", "kind": "base", "block": null, "base_tables": ["intercom__conversation_enhanced"]}, {"alias": "cm", "kind": "base", "block": null, "base_tables": ["intercom__conversation_metrics"]}] | [{"type": "INNER", "right": "intercom__conversation_enhanced AS c", "on": "c.all_contact_company_names = e.company_name", "using": []}, {"type": "LEFT", "right": "intercom__conversation_metrics AS cm", "on": "cm.conversation_id = c.conversation_id", "using": []}] | [] |
| B6 | [{"alias": "event_metrics", "kind": "derived", "block": "B5", "base_tables": ["intercom__company_enhanced", "intercom__conversation_enhanced", "intercom__conversation_metrics"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |


未解析列血缘：[{"block": "B6", "column": "all_contact_company_names", "reason": "ambiguous_or_missing_source"}]

## S49

类别 `data`；来源 `query_db`；调用 `c9adcb9dcb164188a299bb79a80f7807`；状态 `success`。

```sql
-- Per-event before/after counts including zero-conversation windows
WITH tiers AS (
  SELECT company_id, company_name, plan_name, created_at, monthly_spend,
    CASE plan_name WHEN 'Starter' THEN 1 WHEN 'Growth' THEN 2 WHEN 'Scale' THEN 3 WHEN 'Enterprise' THEN 4 END AS tier
  FROM intercom__company_enhanced
),
ordered AS (
  SELECT *, LAG(tier) OVER (PARTITION BY company_name ORDER BY created_at) AS prev_tier,
         LAG(plan_name) OVER (PARTITION BY company_name ORDER BY created_at) AS prev_plan
  FROM tiers
),
events AS (
  SELECT company_name, created_at AS event_at, prev_plan, plan_name AS new_plan, prev_tier, tier,
         CASE WHEN tier > prev_tier THEN 'upgrade' ELSE 'downgrade' END AS event_type
  FROM ordered
  WHERE prev_tier IS NOT NULL AND tier <> prev_tier
    AND company_name IN (SELECT DISTINCT all_contact_company_names FROM intercom__conversation_enhanced)
)
SELECT e.company_name, e.event_at, e.event_type, e.prev_plan, e.new_plan,
  SUM(CASE WHEN c.conversation_created_at < e.event_at THEN 1 ELSE 0 END) AS before_convs,
  SUM(CASE WHEN c.conversation_created_at > e.event_at THEN 1 ELSE 0 END) AS after_convs,
  SUM(CASE WHEN c.conversation_created_at < e.event_at AND c.all_conversation_tags LIKE '%Bug%' THEN 1 ELSE 0 END) AS before_bugs,
  SUM(CASE WHEN c.conversation_created_at > e.event_at AND c.all_conversation_tags LIKE '%Bug%' THEN 1 ELSE 0 END) AS after_bugs,
  SUM(CASE WHEN c.conversation_created_at < e.event_at AND c.all_conversation_tags LIKE '%Outage%' THEN 1 ELSE 0 END) AS before_outages,
  SUM(CASE WHEN c.conversation_created_at > e.event_at AND c.all_conversation_tags LIKE '%Outage%' THEN 1 ELSE 0 END) AS after_outages,
  SUM(CASE WHEN c.conversation_created_at < e.event_at AND c.all_conversation_tags LIKE '%Escalation%' THEN 1 ELSE 0 END) AS before_esc,
  SUM(CASE WHEN c.conversation_created_at > e.event_at AND c.all_conversation_tags LIKE '%Escalation%' THEN 1 ELSE 0 END) AS after_esc,
  SUM(CASE WHEN c.conversation_created_at < e.event_at AND c.sla_status='breached' THEN 1 ELSE 0 END) AS before_sla,
  SUM(CASE WHEN c.conversation_created_at > e.event_at AND c.sla_status='breached' THEN 1 ELSE 0 END) AS after_sla
FROM events e
LEFT JOIN intercom__conversation_enhanced c 
  ON c.all_contact_company_names = e.company_name
  AND c.conversation_created_at >= datetime(e.event_at, '-30 days')
  AND c.conversation_created_at <= datetime(e.event_at, '+30 days')
  AND c.conversation_created_at != e.event_at
GROUP BY e.company_name, e.event_at, e.event_type, e.prev_plan, e.new_plan
ORDER BY e.event_type, e.company_name, e.event_at
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-099/attempt-01/sql/S49.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-099/attempt-01/sql/S49.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-099/attempt-01/results/S49.rows.jsonl)；完整：True；SHA256：`21e03a8b73859c4b385a2b7906cde0f9732aa162a34f17bf717569751e41ba6e`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "intercom__company_enhanced", "kind": "base", "block": null, "base_tables": ["intercom__company_enhanced"]}] | [] | [] |
| B2 | [{"alias": "tiers", "kind": "derived", "block": "B1", "base_tables": ["intercom__company_enhanced"]}] | [] | [] |
| B3 | [{"alias": "intercom__conversation_enhanced", "kind": "base", "block": null, "base_tables": ["intercom__conversation_enhanced"]}] | [] | [] |
| B4 | [{"alias": "ordered", "kind": "derived", "block": "B2", "base_tables": ["intercom__company_enhanced"]}] | [] | [] |
| B5 | [{"alias": "e", "kind": "derived", "block": "B4", "base_tables": ["intercom__company_enhanced"]}, {"alias": "c", "kind": "base", "block": null, "base_tables": ["intercom__conversation_enhanced"]}] | [{"type": "LEFT", "right": "intercom__conversation_enhanced AS c", "on": "c.all_contact_company_names = e.company_name AND c.conversation_created_at >= DATETIME(e.event_at, '-30 days') AND c.conversation_created_at <= DATETIME(e.event_at, '+30 days') AND c.conversation_created_at <> e.event_at", "using": []}] | ["e.company_name", "e.event_at", "e.event_type", "e.prev_plan", "e.new_plan"] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B5 | SUM(CASE WHEN c.conversation_created_at < e.event_at THEN 1 ELSE 0 END) | [] | [{"table": "intercom__conversation_enhanced", "column": "conversation_created_at"}, {"table": "intercom__company_enhanced", "column": "created_at"}] | False |
| B5 | SUM(CASE WHEN c.conversation_created_at > e.event_at THEN 1 ELSE 0 END) | [] | [{"table": "intercom__conversation_enhanced", "column": "conversation_created_at"}, {"table": "intercom__company_enhanced", "column": "created_at"}] | False |
| B5 | SUM(CASE WHEN c.conversation_created_at < e.event_at AND c.all_conversation_tags LIKE '%Bug%' THEN 1 ELSE 0 END) | [] | [{"table": "intercom__conversation_enhanced", "column": "conversation_created_at"}, {"table": "intercom__company_enhanced", "column": "created_at"}, {"table": "intercom__conversation_enhanced", "column": "all_conversation_tags"}] | False |
| B5 | SUM(CASE WHEN c.conversation_created_at > e.event_at AND c.all_conversation_tags LIKE '%Bug%' THEN 1 ELSE 0 END) | [] | [{"table": "intercom__conversation_enhanced", "column": "conversation_created_at"}, {"table": "intercom__company_enhanced", "column": "created_at"}, {"table": "intercom__conversation_enhanced", "column": "all_conversation_tags"}] | False |
| B5 | SUM(CASE WHEN c.conversation_created_at < e.event_at AND c.all_conversation_tags LIKE '%Outage%' THEN 1 ELSE 0 END) | [] | [{"table": "intercom__conversation_enhanced", "column": "conversation_created_at"}, {"table": "intercom__company_enhanced", "column": "created_at"}, {"table": "intercom__conversation_enhanced", "column": "all_conversation_tags"}] | False |
| B5 | SUM(CASE WHEN c.conversation_created_at > e.event_at AND c.all_conversation_tags LIKE '%Outage%' THEN 1 ELSE 0 END) | [] | [{"table": "intercom__conversation_enhanced", "column": "conversation_created_at"}, {"table": "intercom__company_enhanced", "column": "created_at"}, {"table": "intercom__conversation_enhanced", "column": "all_conversation_tags"}] | False |
| B5 | SUM(CASE WHEN c.conversation_created_at < e.event_at AND c.all_conversation_tags LIKE '%Escalation%' THEN 1 ELSE 0 END) | [] | [{"table": "intercom__conversation_enhanced", "column": "conversation_created_at"}, {"table": "intercom__company_enhanced", "column": "created_at"}, {"table": "intercom__conversation_enhanced", "column": "all_conversation_tags"}] | False |
| B5 | SUM(CASE WHEN c.conversation_created_at > e.event_at AND c.all_conversation_tags LIKE '%Escalation%' THEN 1 ELSE 0 END) | [] | [{"table": "intercom__conversation_enhanced", "column": "conversation_created_at"}, {"table": "intercom__company_enhanced", "column": "created_at"}, {"table": "intercom__conversation_enhanced", "column": "all_conversation_tags"}] | False |
| B5 | SUM(CASE WHEN c.conversation_created_at < e.event_at AND c.sla_status = 'breached' THEN 1 ELSE 0 END) | [] | [{"table": "intercom__conversation_enhanced", "column": "conversation_created_at"}, {"table": "intercom__company_enhanced", "column": "created_at"}, {"table": "intercom__conversation_enhanced", "column": "sla_status"}] | False |
| B5 | SUM(CASE WHEN c.conversation_created_at > e.event_at AND c.sla_status = 'breached' THEN 1 ELSE 0 END) | [] | [{"table": "intercom__conversation_enhanced", "column": "conversation_created_at"}, {"table": "intercom__company_enhanced", "column": "created_at"}, {"table": "intercom__conversation_enhanced", "column": "sla_status"}] | False |


## S50

类别 `data`；来源 `query_db`；调用 `218a95d10083456ead0ae07873dfc684`；状态 `success`。

```sql
-- Check which events have conversations in the 30-day window
WITH tiers AS (
  SELECT company_id, company_name, plan_name, created_at, monthly_spend,
    CASE plan_name WHEN 'Starter' THEN 1 WHEN 'Growth' THEN 2 WHEN 'Scale' THEN 3 WHEN 'Enterprise' THEN 4 END AS tier
  FROM intercom__company_enhanced
),
ordered AS (
  SELECT *, LAG(tier) OVER (PARTITION BY company_name ORDER BY created_at) AS prev_tier,
         LAG(plan_name) OVER (PARTITION BY company_name ORDER BY created_at) AS prev_plan
  FROM tiers
),
events AS (
  SELECT company_name, created_at AS event_at, prev_plan, plan_name AS new_plan, prev_tier, tier,
         CASE WHEN tier > prev_tier THEN 'upgrade' ELSE 'downgrade' END AS event_type
  FROM ordered
  WHERE prev_tier IS NOT NULL AND tier <> prev_tier
    AND company_name IN (SELECT DISTINCT all_contact_company_names FROM intercom__conversation_enhanced)
)
SELECT e.event_type, 
  COUNT(*) as total_events,
  SUM(CASE WHEN e.event_at >= (SELECT MIN(conversation_created_at) FROM intercom__conversation_enhanced WHERE all_contact_company_names = e.company_name) + 30
           AND e.event_at <= (SELECT MAX(conversation_created_at) FROM intercom__conversation_enhanced WHERE all_contact_company_names = e.company_name) - 30 THEN 1 ELSE 0 END) as events_with_30d_buffer
FROM events e
GROUP BY e.event_type
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-099/attempt-01/sql/S50.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-099/attempt-01/sql/S50.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-099/attempt-01/results/S50.rows.jsonl)；完整：True；SHA256：`6e54e063f49f3542797bfed959ed7e77f21e16ad6ac2be7968877fa65451897a`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "intercom__company_enhanced", "kind": "base", "block": null, "base_tables": ["intercom__company_enhanced"]}] | [] | [] |
| B2 | [{"alias": "tiers", "kind": "derived", "block": "B1", "base_tables": ["intercom__company_enhanced"]}] | [] | [] |
| B3 | [{"alias": "intercom__conversation_enhanced", "kind": "base", "block": null, "base_tables": ["intercom__conversation_enhanced"]}] | [] | [] |
| B4 | [{"alias": "ordered", "kind": "derived", "block": "B2", "base_tables": ["intercom__company_enhanced"]}] | [] | [] |
| B5 | [{"alias": "intercom__conversation_enhanced", "kind": "base", "block": null, "base_tables": ["intercom__conversation_enhanced"]}] | [] | [] |
| B6 | [{"alias": "intercom__conversation_enhanced", "kind": "base", "block": null, "base_tables": ["intercom__conversation_enhanced"]}] | [] | [] |
| B7 | [{"alias": "e", "kind": "derived", "block": "B4", "base_tables": ["intercom__company_enhanced"]}] | [] | ["e.event_type"] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B5 | MIN(conversation_created_at) | [{"table": "intercom__conversation_enhanced", "column": "conversation_created_at"}] | [] | False |
| B6 | MAX(conversation_created_at) | [{"table": "intercom__conversation_enhanced", "column": "conversation_created_at"}] | [] | False |
| B7 | COUNT(*) | [] | [] | True |
| B7 | SUM(CASE WHEN e.event_at >= (SELECT MIN(conversation_created_at) FROM intercom__conversation_enhanced WHERE all_contact_company_names = e.company_name) + 30 AND e.event_at <= (SELECT MAX(conversation_created_at) FROM intercom__conversation_enhanced WHERE all_contact_company_names = e.company_name) - 30 THEN 1 ELSE 0 END) | [] | [{"table": "intercom__company_enhanced", "column": "created_at"}, {"table": "intercom__company_enhanced", "column": "created_at"}, {"table": "intercom__conversation_enhanced", "column": "conversation_created_at"}, {"table": "intercom__conversation_enhanced", "column": "conversation_created_at"}, {"table": "intercom__conversation_enhanced", "column": "all_contact_company_names"}, {"table": "intercom__company_enhanced", "column": "company_name"}, {"table": "intercom__conversation_enhanced", "column": "all_contact_company_names"}, {"table": "intercom__company_enhanced", "column": "company_name"}] | False |


未解析列血缘：[{"block": "B7", "column": "all_contact_company_names", "reason": "ambiguous_or_missing_source"}, {"block": "B7", "column": "conversation_created_at", "reason": "ambiguous_or_missing_source"}, {"block": "B7", "column": "all_contact_company_names", "reason": "ambiguous_or_missing_source"}, {"block": "B7", "column": "conversation_created_at", "reason": "ambiguous_or_missing_source"}, {"block": "B7", "column": "all_contact_company_names", "reason": "ambiguous_or_missing_source"}]

## S51

类别 `data`；来源 `query_db`；调用 `5286f0b433f34ea896744bf73cc5c36f`；状态 `success`。

```sql
-- Check per-company conversation time ranges and event counts in window
WITH conv_range AS (
  SELECT all_contact_company_names as company_name, 
         MIN(conversation_created_at) as min_c, MAX(conversation_created_at) as max_c,
         COUNT(*) as n_convs
  FROM intercom__conversation_enhanced
  GROUP BY all_contact_company_names
),
tiers AS (
  SELECT company_id, company_name, plan_name, created_at, monthly_spend,
    CASE plan_name WHEN 'Starter' THEN 1 WHEN 'Growth' THEN 2 WHEN 'Scale' THEN 3 WHEN 'Enterprise' THEN 4 END AS tier
  FROM intercom__company_enhanced
),
ordered AS (
  SELECT *, LAG(tier) OVER (PARTITION BY company_name ORDER BY created_at) AS prev_tier,
         LAG(plan_name) OVER (PARTITION BY company_name ORDER BY created_at) AS prev_plan
  FROM tiers
),
events AS (
  SELECT company_name, created_at AS event_at, prev_plan, plan_name AS new_plan, prev_tier, tier,
         CASE WHEN tier > prev_tier THEN 'upgrade' ELSE 'downgrade' END AS event_type
  FROM ordered
  WHERE prev_tier IS NOT NULL AND tier <> prev_tier
)
SELECT cr.company_name, cr.min_c, cr.max_c, cr.n_convs,
       SUM(CASE WHEN e.event_type='upgrade' THEN 1 ELSE 0 END) as n_upgrade,
       SUM(CASE WHEN e.event_type='downgrade' THEN 1 ELSE 0 END) as n_downgrade
FROM conv_range cr
LEFT JOIN events e ON e.company_name = cr.company_name
GROUP BY cr.company_name
ORDER BY cr.n_convs DESC
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-099/attempt-01/sql/S51.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-099/attempt-01/sql/S51.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-099/attempt-01/results/S51.rows.jsonl)；完整：True；SHA256：`5d1b418ac8dee6334b550463e7135c1c072a4c58fbc720245a01396f1bc5ac90`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "intercom__conversation_enhanced", "kind": "base", "block": null, "base_tables": ["intercom__conversation_enhanced"]}] | [] | ["all_contact_company_names"] |
| B2 | [{"alias": "intercom__company_enhanced", "kind": "base", "block": null, "base_tables": ["intercom__company_enhanced"]}] | [] | [] |
| B3 | [{"alias": "tiers", "kind": "derived", "block": "B2", "base_tables": ["intercom__company_enhanced"]}] | [] | [] |
| B4 | [{"alias": "ordered", "kind": "derived", "block": "B3", "base_tables": ["intercom__company_enhanced"]}] | [] | [] |
| B5 | [{"alias": "cr", "kind": "derived", "block": "B1", "base_tables": ["intercom__conversation_enhanced"]}, {"alias": "e", "kind": "derived", "block": "B4", "base_tables": ["intercom__company_enhanced"]}] | [{"type": "LEFT", "right": "events AS e", "on": "e.company_name = cr.company_name", "using": []}] | ["cr.company_name"] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | MIN(conversation_created_at) | [{"table": "intercom__conversation_enhanced", "column": "conversation_created_at"}] | [] | False |
| B1 | MAX(conversation_created_at) | [{"table": "intercom__conversation_enhanced", "column": "conversation_created_at"}] | [] | False |
| B1 | COUNT(*) | [] | [] | True |
| B5 | SUM(CASE WHEN e.event_type = 'upgrade' THEN 1 ELSE 0 END) | [] | [{"table": "intercom__company_enhanced", "column": "plan_name"}, {"table": "intercom__company_enhanced", "column": "company_name"}, {"table": "intercom__company_enhanced", "column": "plan_name"}, {"table": "intercom__company_enhanced", "column": "created_at"}] | False |
| B5 | SUM(CASE WHEN e.event_type = 'downgrade' THEN 1 ELSE 0 END) | [] | [{"table": "intercom__company_enhanced", "column": "plan_name"}, {"table": "intercom__company_enhanced", "column": "company_name"}, {"table": "intercom__company_enhanced", "column": "plan_name"}, {"table": "intercom__company_enhanced", "column": "created_at"}] | False |


## S52

类别 `data`；来源 `query_db`；调用 `849b7729c0d1468289f730f71cb7ca17`；状态 `success`。

```sql
-- For each event, check if it has 30-day buffer for conversations
WITH conv_range AS (
  SELECT all_contact_company_names as company_name, 
         MIN(conversation_created_at) as min_c, MAX(conversation_created_at) as max_c
  FROM intercom__conversation_enhanced
  GROUP BY all_contact_company_names
),
tiers AS (
  SELECT company_id, company_name, plan_name, created_at, monthly_spend,
    CASE plan_name WHEN 'Starter' THEN 1 WHEN 'Growth' THEN 2 WHEN 'Scale' THEN 3 WHEN 'Enterprise' THEN 4 END AS tier
  FROM intercom__company_enhanced
),
ordered AS (
  SELECT *, LAG(tier) OVER (PARTITION BY company_name ORDER BY created_at) AS prev_tier,
         LAG(plan_name) OVER (PARTITION BY company_name ORDER BY created_at) AS prev_plan
  FROM tiers
),
events AS (
  SELECT company_name, created_at AS event_at, prev_plan, plan_name AS new_plan, prev_tier, tier,
         CASE WHEN tier > prev_tier THEN 'upgrade' ELSE 'downgrade' END AS event_type
  FROM ordered
  WHERE prev_tier IS NOT NULL AND tier <> prev_tier
    AND company_name IN (SELECT DISTINCT all_contact_company_names FROM intercom__conversation_enhanced)
)
SELECT e.event_type, COUNT(*) as total,
  SUM(CASE WHEN e.event_at >= datetime(cr.min_c, '+30 days') AND e.event_at <= datetime(cr.max_c, '-30 days') THEN 1 ELSE 0 END) as has_30d_buffer
FROM events e
JOIN conv_range cr ON cr.company_name = e.company_name
GROUP BY e.event_type
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-099/attempt-01/sql/S52.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-099/attempt-01/sql/S52.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-099/attempt-01/results/S52.rows.jsonl)；完整：True；SHA256：`324acfdd8b9f8d90b2ca202888084d0b20ebf582168a14241b7dab44b5954fd0`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "intercom__conversation_enhanced", "kind": "base", "block": null, "base_tables": ["intercom__conversation_enhanced"]}] | [] | ["all_contact_company_names"] |
| B2 | [{"alias": "intercom__company_enhanced", "kind": "base", "block": null, "base_tables": ["intercom__company_enhanced"]}] | [] | [] |
| B3 | [{"alias": "tiers", "kind": "derived", "block": "B2", "base_tables": ["intercom__company_enhanced"]}] | [] | [] |
| B4 | [{"alias": "intercom__conversation_enhanced", "kind": "base", "block": null, "base_tables": ["intercom__conversation_enhanced"]}] | [] | [] |
| B5 | [{"alias": "ordered", "kind": "derived", "block": "B3", "base_tables": ["intercom__company_enhanced"]}] | [] | [] |
| B6 | [{"alias": "e", "kind": "derived", "block": "B5", "base_tables": ["intercom__company_enhanced"]}, {"alias": "cr", "kind": "derived", "block": "B1", "base_tables": ["intercom__conversation_enhanced"]}] | [{"type": "INNER", "right": "conv_range AS cr", "on": "cr.company_name = e.company_name", "using": []}] | ["e.event_type"] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | MIN(conversation_created_at) | [{"table": "intercom__conversation_enhanced", "column": "conversation_created_at"}] | [] | False |
| B1 | MAX(conversation_created_at) | [{"table": "intercom__conversation_enhanced", "column": "conversation_created_at"}] | [] | False |
| B6 | COUNT(*) | [] | [] | True |
| B6 | SUM(CASE WHEN e.event_at >= DATETIME(cr.min_c, '+30 days') AND e.event_at <= DATETIME(cr.max_c, '-30 days') THEN 1 ELSE 0 END) | [] | [{"table": "intercom__company_enhanced", "column": "created_at"}, {"table": "intercom__company_enhanced", "column": "created_at"}, {"table": "intercom__conversation_enhanced", "column": "conversation_created_at"}, {"table": "intercom__conversation_enhanced", "column": "conversation_created_at"}] | False |


未解析列血缘：[{"block": "B6", "column": "all_contact_company_names", "reason": "ambiguous_or_missing_source"}]

## S53

类别 `data`；来源 `query_db`；调用 `ae0e6b4e0d8745b2b1b5ccc6a4c0b3ba`；状态 `success`。

```sql
SELECT ce.company_name, ce.plan_name, ce.created_at, ce.updated_at, ce.monthly_spend, ce.user_count, ce.session_count
FROM intercom__company_enhanced ce
WHERE ce.company_name = 'Edge Platforms'
ORDER BY ce.created_at
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-099/attempt-01/sql/S53.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-099/attempt-01/sql/S53.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-099/attempt-01/results/S53.rows.jsonl)；完整：True；SHA256：`f4ae05a368380454387901c4d27a54276560fa190a878a4a8e152f4dfdce34bf`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "ce", "kind": "base", "block": null, "base_tables": ["intercom__company_enhanced"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |


## S54

类别 `data`；来源 `query_db`；调用 `9010b00371bc42b49256143672f7749e`；状态 `success`。

```sql
SELECT conversation_id, conversation_created_at, all_conversation_tags FROM intercom__conversation_enhanced WHERE all_contact_company_names = 'Edge Platforms' ORDER BY conversation_created_at LIMIT 40
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-099/attempt-01/sql/S54.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-099/attempt-01/sql/S54.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-099/attempt-01/results/S54.rows.jsonl)；完整：True；SHA256：`d297cbd8359825b28d29935672b85a4b6d3c2dfdd967f531ae4edca6b4893a7a`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "intercom__conversation_enhanced", "kind": "base", "block": null, "base_tables": ["intercom__conversation_enhanced"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |


## S55

类别 `data`；来源 `python`；调用 `ed9feb6d805f4ccba1a454b90b264b53`；状态 `failed`。

```sql

SELECT all_contact_company_names as company_name, conversation_created_at, 
       all_conversation_tags, sla_status, conversation_initiated_type,
       cm.count_total_parts, cm.time_to_first_response_minutes
FROM intercom__conversation_enhanced c
LEFT JOIN intercom__conversation_metrics cm ON cm.conversation_id = c.conversation_id

```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-099/attempt-01/sql/S55.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-099/attempt-01/sql/S55.parameters.json)。

错误：`OperationalError('ambiguous column name: conversation_created_at')`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "c", "kind": "base", "block": null, "base_tables": ["intercom__conversation_enhanced"]}, {"alias": "cm", "kind": "base", "block": null, "base_tables": ["intercom__conversation_metrics"]}] | [{"type": "LEFT", "right": "intercom__conversation_metrics AS cm", "on": "cm.conversation_id = c.conversation_id", "using": []}] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |


未解析列血缘：[{"block": "B1", "column": "conversation_created_at", "reason": "ambiguous_or_missing_source"}, {"block": "B1", "column": "sla_status", "reason": "ambiguous_or_missing_source"}, {"block": "B1", "column": "conversation_initiated_type", "reason": "ambiguous_or_missing_source"}]

## S56

类别 `data`；来源 `python`；调用 `707a76f264e548058265b54baece40fb`；状态 `failed`。

```sql

SELECT all_contact_company_names as company_name, conversation_created_at, 
       all_conversation_tags, sla_status, conversation_initiated_type,
       count_total_parts
FROM intercom__conversation_enhanced c
LEFT JOIN intercom__conversation_metrics cm ON cm.conversation_id = c.conversation_id
WHERE c.all_contact_company_names = 'Edge Platforms'

```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-099/attempt-01/sql/S56.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-099/attempt-01/sql/S56.parameters.json)。

错误：`OperationalError('ambiguous column name: conversation_created_at')`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "c", "kind": "base", "block": null, "base_tables": ["intercom__conversation_enhanced"]}, {"alias": "cm", "kind": "base", "block": null, "base_tables": ["intercom__conversation_metrics"]}] | [{"type": "LEFT", "right": "intercom__conversation_metrics AS cm", "on": "cm.conversation_id = c.conversation_id", "using": []}] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |


未解析列血缘：[{"block": "B1", "column": "conversation_created_at", "reason": "ambiguous_or_missing_source"}, {"block": "B1", "column": "sla_status", "reason": "ambiguous_or_missing_source"}, {"block": "B1", "column": "conversation_initiated_type", "reason": "ambiguous_or_missing_source"}]

## S57

类别 `data`；来源 `python`；调用 `707a76f264e548058265b54baece40fb`；状态 `success`。

```sql
SELECT COUNT(*) as n FROM intercom__conversation_enhanced
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-099/attempt-01/sql/S57.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-099/attempt-01/sql/S57.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-099/attempt-01/results/S57.rows.jsonl)；完整：True；SHA256：`20b1d17818ff06b3c178fb6a083d46fc454d428bcb3a0a8118c827db65a82b2e`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "intercom__conversation_enhanced", "kind": "base", "block": null, "base_tables": ["intercom__conversation_enhanced"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |


## S58

类别 `data`；来源 `python`；调用 `27d26cb956ce4180960805faa5be95ff`；状态 `success`。

```sql

SELECT all_contact_company_names as company_name, conversation_created_at, 
       all_conversation_tags, sla_status, conversation_initiated_type
FROM intercom__conversation_enhanced
WHERE all_contact_company_names = 'Edge Platforms'

```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-099/attempt-01/sql/S58.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-099/attempt-01/sql/S58.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-099/attempt-01/results/S58.rows.jsonl)；完整：True；SHA256：`7bfe5933ed24490aae2c20df9386681dbc4821f136fa2aaea48182b3dbaaf2fa`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "intercom__conversation_enhanced", "kind": "base", "block": null, "base_tables": ["intercom__conversation_enhanced"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |


## S59

类别 `data`；来源 `python`；调用 `27d26cb956ce4180960805faa5be95ff`；状态 `success`。

```sql

SELECT conversation_id, count_total_parts
FROM intercom__conversation_metrics
LIMIT 100

```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-099/attempt-01/sql/S59.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-099/attempt-01/sql/S59.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-099/attempt-01/results/S59.rows.jsonl)；完整：True；SHA256：`0a6a681273af461a33de2f9d489e7d6d30ffda74a56b8abaa73eb9f6851fbd7a`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "intercom__conversation_metrics", "kind": "base", "block": null, "base_tables": ["intercom__conversation_metrics"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |


## S60

类别 `data`；来源 `python`；调用 `27d26cb956ce4180960805faa5be95ff`；状态 `success`。

```sql
SELECT conversation_id, COUNT(*) as n FROM intercom__conversation_enhanced GROUP BY conversation_id HAVING n > 1 LIMIT 5
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-099/attempt-01/sql/S60.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-099/attempt-01/sql/S60.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-099/attempt-01/results/S60.rows.jsonl)；完整：True；SHA256：`e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "intercom__conversation_enhanced", "kind": "base", "block": null, "base_tables": ["intercom__conversation_enhanced"]}] | [] | ["conversation_id"] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |


## S61

类别 `data`；来源 `python`；调用 `bda7116be3f842629a18232f82a33656`；状态 `success`。

```sql

SELECT all_contact_company_names as company_name, conversation_created_at, 
       all_conversation_tags, sla_status, conversation_initiated_type, conversation_id
FROM intercom__conversation_enhanced

```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-099/attempt-01/sql/S61.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-099/attempt-01/sql/S61.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-099/attempt-01/results/S61.rows.jsonl)；完整：True；SHA256：`c81d10b06b06e163cf7a0e4dce984ca7df55880b0abd552b40e9f06fe05b1d4c`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "intercom__conversation_enhanced", "kind": "base", "block": null, "base_tables": ["intercom__conversation_enhanced"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |


## S62

类别 `data`；来源 `python`；调用 `bda7116be3f842629a18232f82a33656`；状态 `success`。

```sql

SELECT conversation_id, count_total_parts, time_to_first_response_minutes, conversation_rating
FROM intercom__conversation_metrics

```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-099/attempt-01/sql/S62.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-099/attempt-01/sql/S62.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-099/attempt-01/results/S62.rows.jsonl)；完整：True；SHA256：`05e166f792bb46a2ade69dcb665aa347d73c6201c40007de239068871edf5576`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "intercom__conversation_metrics", "kind": "base", "block": null, "base_tables": ["intercom__conversation_metrics"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |


## S63

类别 `data`；来源 `python`；调用 `bda7116be3f842629a18232f82a33656`；状态 `success`。

```sql

WITH tiers AS (
  SELECT company_id, company_name, plan_name, created_at, monthly_spend,
    CASE plan_name WHEN 'Starter' THEN 1 WHEN 'Growth' THEN 2 WHEN 'Scale' THEN 3 WHEN 'Enterprise' THEN 4 END AS tier
  FROM intercom__company_enhanced
),
ordered AS (
  SELECT *, LAG(tier) OVER (PARTITION BY company_name ORDER BY created_at) AS prev_tier,
         LAG(plan_name) OVER (PARTITION BY company_name ORDER BY created_at) AS prev_plan
  FROM tiers
)
SELECT company_name, created_at AS event_at, prev_plan, plan_name AS new_plan,
       CASE WHEN tier > prev_tier THEN 'upgrade' ELSE 'downgrade' END AS event_type
FROM ordered
WHERE prev_tier IS NOT NULL AND tier <> prev_tier

```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-099/attempt-01/sql/S63.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-099/attempt-01/sql/S63.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-099/attempt-01/results/S63.rows.jsonl)；完整：True；SHA256：`b0ce9eb3b70cfb5c58220fe95acdd611d1a25084454e52bb517b8b50f3e81b80`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "intercom__company_enhanced", "kind": "base", "block": null, "base_tables": ["intercom__company_enhanced"]}] | [] | [] |
| B2 | [{"alias": "tiers", "kind": "derived", "block": "B1", "base_tables": ["intercom__company_enhanced"]}] | [] | [] |
| B3 | [{"alias": "ordered", "kind": "derived", "block": "B2", "base_tables": ["intercom__company_enhanced"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |


## S64

类别 `data`；来源 `query_db`；调用 `edb20a43dabe4abcb97cb96971d66d15`；状态 `success`。

```sql
-- Use Upgrade Opportunity / Downgrade Risk conversation tags as event markers
SELECT event_type, COUNT(*) as total_convs, COUNT(DISTINCT company_name) as companies
FROM (
  SELECT all_contact_company_names as company_name, conversation_created_at,
         CASE WHEN all_conversation_tags LIKE '%Upgrade Opportunity%' THEN 'upgrade'
              WHEN all_conversation_tags LIKE '%Downgrade Risk%' THEN 'downgrade'
              ELSE NULL END as event_type
  FROM intercom__conversation_enhanced
  WHERE all_conversation_tags LIKE '%Upgrade Opportunity%' OR all_conversation_tags LIKE '%Downgrade Risk%'
)
WHERE event_type IS NOT NULL
GROUP BY event_type
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-099/attempt-01/sql/S64.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-099/attempt-01/sql/S64.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-099/attempt-01/results/S64.rows.jsonl)；完整：True；SHA256：`9d624fdfc09499d8cac19dce3917892fe67f1d889b6b40268deb364251aa741e`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "intercom__conversation_enhanced", "kind": "base", "block": null, "base_tables": ["intercom__conversation_enhanced"]}] | [] | [] |
| B2 | [{"alias": "", "kind": "derived", "block": "B1", "base_tables": ["intercom__conversation_enhanced"]}] | [] | ["event_type"] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B2 | COUNT(*) | [] | [] | True |
| B2 | COUNT(DISTINCT company_name) | [{"table": "intercom__conversation_enhanced", "column": "all_contact_company_names"}] | [] | False |


## S65

类别 `data`；来源 `query_db`；调用 `655d01521ba249cbae51ef9325585119`；状态 `success`。

```sql
SELECT company_name FROM (
  SELECT DISTINCT all_contact_company_names as company_name FROM intercom__conversation_enhanced WHERE all_conversation_tags LIKE '%Upgrade Opportunity%'
  INTERSECT
  SELECT DISTINCT all_contact_company_names as company_name FROM intercom__conversation_enhanced WHERE all_conversation_tags LIKE '%Downgrade Risk%'
) ORDER BY company_name
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-099/attempt-01/sql/S65.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-099/attempt-01/sql/S65.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-099/attempt-01/results/S65.rows.jsonl)；完整：True；SHA256：`8d24e4d2e5e67ca9573ff3238ba26489e7fb0494c9e36bb605dfc4889d71dd59`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "intercom__conversation_enhanced", "kind": "base", "block": null, "base_tables": ["intercom__conversation_enhanced"]}] | [] | [] |
| B2 | [{"alias": "intercom__conversation_enhanced", "kind": "base", "block": null, "base_tables": ["intercom__conversation_enhanced"]}] | [] | [] |
| B3 | [] | [] | [] |
| B4 | [{"alias": "", "kind": "derived", "block": "B3", "base_tables": ["intercom__conversation_enhanced"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |


## S66

类别 `data`；来源 `query_db`；调用 `7e3bfce3c2b74908b2b85dd86bfbeb3d`；状态 `success`。

```sql
-- First "Upgrade Opportunity" conversation per company (as hypothetical upgrade_at)
-- and first "Downgrade Risk" conversation per company (as hypothetical downgrade_at)
SELECT company_name, event_type, MIN(conversation_created_at) as first_event_at, COUNT(*) as tag_count
FROM (
  SELECT all_contact_company_names as company_name, conversation_created_at,
         CASE WHEN all_conversation_tags LIKE '%Upgrade Opportunity%' THEN 'upgrade'
              WHEN all_conversation_tags LIKE '%Downgrade Risk%' THEN 'downgrade' END as event_type
  FROM intercom__conversation_enhanced
  WHERE all_conversation_tags LIKE '%Upgrade Opportunity%' OR all_conversation_tags LIKE '%Downgrade Risk%'
)
WHERE event_type IS NOT NULL
GROUP BY company_name, event_type
ORDER BY company_name, event_type
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-099/attempt-01/sql/S66.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-099/attempt-01/sql/S66.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-099/attempt-01/results/S66.rows.jsonl)；完整：True；SHA256：`a2fb3c6eb34c0390faf6162f00a2560d7fabea5dc3d7c1ba48a0b484be0b335e`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "intercom__conversation_enhanced", "kind": "base", "block": null, "base_tables": ["intercom__conversation_enhanced"]}] | [] | [] |
| B2 | [{"alias": "", "kind": "derived", "block": "B1", "base_tables": ["intercom__conversation_enhanced"]}] | [] | ["company_name", "event_type"] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B2 | MIN(conversation_created_at) | [{"table": "intercom__conversation_enhanced", "column": "conversation_created_at"}] | [] | False |
| B2 | COUNT(*) | [] | [] | True |


## S67

类别 `data`；来源 `python`；调用 `ffc734d7d940473cbc301d29bd423ffe`；状态 `success`。

```sql

WITH tiers AS (
  SELECT company_id, company_name, plan_name, created_at, monthly_spend,
    CASE plan_name WHEN 'Starter' THEN 1 WHEN 'Growth' THEN 2 WHEN 'Scale' THEN 3 WHEN 'Enterprise' THEN 4 END AS tier
  FROM intercom__company_enhanced
),
ordered AS (
  SELECT *, LAG(tier) OVER (PARTITION BY company_name ORDER BY created_at) AS prev_tier,
         LAG(plan_name) OVER (PARTITION BY company_name ORDER BY created_at) AS prev_plan,
         LAG(created_at) OVER (PARTITION BY company_name ORDER BY created_at) AS prev_created_at,
         LEAD(created_at) OVER (PARTITION BY company_name ORDER BY created_at) AS next_created_at
  FROM tiers
)
SELECT company_name, created_at AS event_at, prev_created_at, next_created_at,
       prev_plan, plan_name AS new_plan, prev_tier, tier,
       CASE WHEN tier > prev_tier THEN 'upgrade' ELSE 'downgrade' END AS event_type
FROM ordered
WHERE prev_tier IS NOT NULL AND tier <> prev_tier

```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-099/attempt-01/sql/S67.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-099/attempt-01/sql/S67.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-099/attempt-01/results/S67.rows.jsonl)；完整：True；SHA256：`27c61714115561740a82391b82830808ed8c512cb28fa1ff1408412374549cda`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "intercom__company_enhanced", "kind": "base", "block": null, "base_tables": ["intercom__company_enhanced"]}] | [] | [] |
| B2 | [{"alias": "tiers", "kind": "derived", "block": "B1", "base_tables": ["intercom__company_enhanced"]}] | [] | [] |
| B3 | [{"alias": "ordered", "kind": "derived", "block": "B2", "base_tables": ["intercom__company_enhanced"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |


## S68

类别 `data`；来源 `python`；调用 `ffc734d7d940473cbc301d29bd423ffe`；状态 `success`。

```sql

SELECT all_contact_company_names as company_name, conversation_created_at, 
       all_conversation_tags, sla_status, conversation_initiated_type
FROM intercom__conversation_enhanced

```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-099/attempt-01/sql/S68.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-099/attempt-01/sql/S68.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-099/attempt-01/results/S68.rows.jsonl)；完整：True；SHA256：`304634fda14bd70a96ddbc972ba47a4ee3f9028290ead88ad22406e12f58565e`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "intercom__conversation_enhanced", "kind": "base", "block": null, "base_tables": ["intercom__conversation_enhanced"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |


## S69

类别 `data`；来源 `python`；调用 `2c4a73521e624c4c906b308bd5dd38df`；状态 `success`。

```sql

SELECT ce.company_name, ce.plan_name, ce.monthly_spend, cm.*
FROM intercom__company_enhanced ce
JOIN intercom__company_metrics cm ON ce.company_id = cm.company_id

```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-099/attempt-01/sql/S69.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-099/attempt-01/sql/S69.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-099/attempt-01/results/S69.rows.jsonl)；完整：True；SHA256：`ad523f83b77e1a6c7c9cb7be9d281c8178a1266533a4b7218b65824f47a5ff97`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "ce", "kind": "base", "block": null, "base_tables": ["intercom__company_enhanced"]}, {"alias": "cm", "kind": "base", "block": null, "base_tables": ["intercom__company_metrics"]}] | [{"type": "INNER", "right": "intercom__company_metrics AS cm", "on": "ce.company_id = cm.company_id", "using": []}] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |


## S70

类别 `data`；来源 `python`；调用 `ad40739d40944b2cb1de0cf0f4c0f1dd`；状态 `success`。

```sql

SELECT ce.company_name, ce.plan_name, ce.monthly_spend, ce.user_count, ce.session_count,
       cm.total_conversations, cm.avg_conversation_rating, cm.p50_time_to_first_response_min,
       cm.p50_reopens, cm.registration_retention_7d, cm.registration_retention_30d,
       cm.contacts_active_7d, cm.contacts_active_30d, cm.contacts_total
FROM intercom__company_enhanced ce
JOIN intercom__company_metrics cm ON ce.company_id = cm.company_id

```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-099/attempt-01/sql/S70.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-099/attempt-01/sql/S70.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-099/attempt-01/results/S70.rows.jsonl)；完整：True；SHA256：`2d7c06cd15e6d0013ff6dbbf21a13ab1e55502d0e17ee103f1eabed9888aed55`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "ce", "kind": "base", "block": null, "base_tables": ["intercom__company_enhanced"]}, {"alias": "cm", "kind": "base", "block": null, "base_tables": ["intercom__company_metrics"]}] | [{"type": "INNER", "right": "intercom__company_metrics AS cm", "on": "ce.company_id = cm.company_id", "using": []}] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |


## S71

类别 `data`；来源 `python`；调用 `ac6bcb61e17e4ad5a28dbcc26f57dcd7`；状态 `success`。

```sql

WITH tiers AS (
  SELECT company_id, company_name, plan_name, created_at, monthly_spend,
    CASE plan_name WHEN 'Starter' THEN 1 WHEN 'Growth' THEN 2 WHEN 'Scale' THEN 3 WHEN 'Enterprise' THEN 4 END AS tier
  FROM intercom__company_enhanced
),
ordered AS (
  SELECT *, LAG(tier) OVER (PARTITION BY company_name ORDER BY created_at) AS prev_tier,
         LAG(plan_name) OVER (PARTITION BY company_name ORDER BY created_at) AS prev_plan,
         LAG(created_at) OVER (PARTITION BY company_name ORDER BY created_at) AS prev_created_at,
         LEAD(created_at) OVER (PARTITION BY company_name ORDER BY created_at) AS next_created_at
  FROM tiers
)
SELECT company_name, created_at AS event_at, prev_created_at, next_created_at,
       prev_plan, plan_name AS new_plan,
       CASE WHEN tier > prev_tier THEN 'upgrade' ELSE 'downgrade' END AS event_type
FROM ordered
WHERE prev_tier IS NOT NULL AND tier <> prev_tier

```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-099/attempt-01/sql/S71.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-099/attempt-01/sql/S71.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-099/attempt-01/results/S71.rows.jsonl)；完整：True；SHA256：`2cd3a9d5876621b3c66ef1afc04a4dbf8a77f47bffe73f827d155a97e8fa2c1a`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "intercom__company_enhanced", "kind": "base", "block": null, "base_tables": ["intercom__company_enhanced"]}] | [] | [] |
| B2 | [{"alias": "tiers", "kind": "derived", "block": "B1", "base_tables": ["intercom__company_enhanced"]}] | [] | [] |
| B3 | [{"alias": "ordered", "kind": "derived", "block": "B2", "base_tables": ["intercom__company_enhanced"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |


## S72

类别 `data`；来源 `python`；调用 `ac6bcb61e17e4ad5a28dbcc26f57dcd7`；状态 `success`。

```sql

SELECT all_contact_company_names as company_name, conversation_created_at, all_conversation_tags,
       sla_status, conversation_rating, conversation_subject
FROM intercom__conversation_enhanced

```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-099/attempt-01/sql/S72.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-099/attempt-01/sql/S72.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-099/attempt-01/results/S72.rows.jsonl)；完整：True；SHA256：`71f4fee344a062a99a4225aecec6a4470066765e64b4d9c2b262957c3798aa5a`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "intercom__conversation_enhanced", "kind": "base", "block": null, "base_tables": ["intercom__conversation_enhanced"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |


## S73

类别 `data`；来源 `python`；调用 `0f70aee966d54e4c8925f90d80f96106`；状态 `success`。

```sql

SELECT all_contact_company_names as company_name, conversation_created_at
FROM intercom__conversation_enhanced

```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-099/attempt-01/sql/S73.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-099/attempt-01/sql/S73.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-099/attempt-01/results/S73.rows.jsonl)；完整：True；SHA256：`3e7a5caaf39906b692fb2ed72c81c584d14e3275c26d026fa6af8233a3b60ba1`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "intercom__conversation_enhanced", "kind": "base", "block": null, "base_tables": ["intercom__conversation_enhanced"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |


## S74

类别 `data`；来源 `python`；调用 `0f70aee966d54e4c8925f90d80f96106`；状态 `success`。

```sql

WITH tiers AS (
  SELECT company_id, company_name, plan_name, created_at,
    CASE plan_name WHEN 'Starter' THEN 1 WHEN 'Growth' THEN 2 WHEN 'Scale' THEN 3 WHEN 'Enterprise' THEN 4 END AS tier
  FROM intercom__company_enhanced
),
ordered AS (
  SELECT *, LAG(tier) OVER (PARTITION BY company_name ORDER BY created_at) AS prev_tier,
         LAG(plan_name) OVER (PARTITION BY company_name ORDER BY created_at) AS prev_plan
  FROM tiers
),
events AS (
  SELECT company_name, created_at AS event_at, prev_plan, plan_name AS new_plan, prev_tier, tier,
         CASE WHEN tier > prev_tier THEN 1 ELSE -1 END AS delta
  FROM ordered
  WHERE prev_tier IS NOT NULL AND tier <> prev_tier
)
SELECT company_name, SUM(delta) AS net_direction, COUNT(*) as n_changes
FROM events
GROUP BY company_name

```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-099/attempt-01/sql/S74.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-099/attempt-01/sql/S74.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-099/attempt-01/results/S74.rows.jsonl)；完整：True；SHA256：`b6b2e95917cc81ffa430a2e7a60670f178395cfa8817e6b99663c01e78644492`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "intercom__company_enhanced", "kind": "base", "block": null, "base_tables": ["intercom__company_enhanced"]}] | [] | [] |
| B2 | [{"alias": "tiers", "kind": "derived", "block": "B1", "base_tables": ["intercom__company_enhanced"]}] | [] | [] |
| B3 | [{"alias": "ordered", "kind": "derived", "block": "B2", "base_tables": ["intercom__company_enhanced"]}] | [] | [] |
| B4 | [{"alias": "events", "kind": "derived", "block": "B3", "base_tables": ["intercom__company_enhanced"]}] | [] | ["company_name"] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B4 | SUM(delta) | [{"table": "intercom__company_enhanced", "column": "plan_name"}, {"table": "intercom__company_enhanced", "column": "company_name"}, {"table": "intercom__company_enhanced", "column": "plan_name"}, {"table": "intercom__company_enhanced", "column": "created_at"}] | [] | False |
| B4 | COUNT(*) | [] | [] | True |

