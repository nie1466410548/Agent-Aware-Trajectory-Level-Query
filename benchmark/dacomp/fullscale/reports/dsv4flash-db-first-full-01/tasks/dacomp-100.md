# dacomp-100

For customers whose contracts are due for renewal within the next 90 days, build a renewal…

运行：已提交。官方未评分。全部 SQL 尝试/成功 78/73；数据 SQL 76/71；Python 30 次。

完整原题：

For customers whose contracts are due for renewal within the next 90 days, build a renewal risk prediction framework. Using the provided data marts, define the following features:
- **Communication & Interaction Features**: average number of conversations and the proportion of negative sentiment over the last 30 days.
- **Support Experience Features**: average resolution time for conversations (close time - creation time, averaged at the company level) and the proportion of reopened conversations (number of reopened conversations ÷ total conversations).
- **Product Value Features**: key feature adoption coverage (number of core features used ÷ total number of core features) and time since last value milestone (current date - date of most recent milestone achievement).

Analyze historical renewal cycles to compare the differences in these features between successfully renewed customers and churned customers. Calculate their discriminative power (e.g., using AUC or quantile differences). Finally, provide operational recommendations segmented by **industry and contract size**, such as improving feature coverage, arranging for early consultant intervention, or adjusting communication cadence. The conclusion should focus on **which features are the strongest leading indicators of renewal risk**.

| 表 | 行数 | 列数 |
| --- | --- | --- |
| intercom__company_enhanced | 2509 | 14 |
| intercom__company_metrics | 2509 | 25 |
| intercom__conversation_enhanced | 6703 | 30 |
| intercom__conversation_metrics | 6703 | 40 |


实际路线（分析者依据 SQL/源码概括，不代表 Agent 自述）：SQL 探索与数据提取 → Python 业务准备和统计 → 报告

数据库大小：11,960,320 字节。

## 数据 SQL

| SQL | 状态 | 基础表 | Join 输入/类型 | GROUP BY | 聚合表达式 | 结果行数 | 数据库 ms |
| --- | --- | --- | --- | --- | --- | --- | --- |
| [S3/Q1](#s3) | success | ["intercom__company_enhanced"] | 0 / {} | [] | ["COUNT(*)"] | 1 | 1.777 |
| [S4/Q2](#s4) | success | ["intercom__company_metrics"] | 0 / {} | [] | ["COUNT(*)"] | 1 | 0.481 |
| [S5/Q3](#s5) | success | ["intercom__conversation_metrics"] | 0 / {} | [] | ["COUNT(*)"] | 1 | 1.607 |
| [S6/Q4](#s6) | success | ["intercom__company_enhanced"] | 0 / {} | [] | [] | 5 | 0.394 |
| [S7/Q5](#s7) | failed | ["intercom__company_enhanced"] | 0 / {} | ["renewal_window"] | ["COUNT(*)"] | unknown | 未取得；调用总时长 0.188 ms |
| [S8/Q6](#s8) | success | ["intercom__company_metrics"] | 0 / {} | [] | [] | 3 | 0.398 |
| [S9/Q7](#s9) | success | ["intercom__conversation_metrics"] | 0 / {} | [] | [] | 3 | 0.438 |
| [S10/Q8](#s10) | success | ["intercom__conversation_enhanced"] | 0 / {} | [] | [] | 3 | 0.405 |
| [S11/Q9](#s11) | success | ["intercom__conversation_enhanced"] | 0 / {} | [] | [] | 5 | 0.327 |
| [S12/Q10](#s12) | success | ["intercom__company_enhanced"] | 0 / {} | [] | [] | 2509 | 10.0 |
| [S13/Q11](#s13) | success | ["intercom__company_enhanced"] | 0 / {} | [] | [] | 2509 | 4.043 |
| [S14/Q12](#s14) | success | ["intercom__conversation_enhanced"] | 0 / {} | [] | [] | 6703 | 8.697 |
| [S15/Q13](#s15) | success | ["intercom__company_enhanced"] | 0 / {} | [] | [] | 2509 | 2.647 |
| [S16/Q14](#s16) | success | ["intercom__conversation_enhanced"] | 0 / {} | [] | [] | 6703 | 9.494 |
| [S17/Q15](#s17) | success | ["intercom__company_enhanced"] | 0 / {} | [] | [] | 2509 | 4.594 |
| [S18/Q16](#s18) | success | ["intercom__company_metrics"] | 0 / {} | [] | [] | 2509 | 11.823 |
| [S19/Q17](#s19) | success | ["intercom__company_enhanced"] | 0 / {} | [] | [] | 2509 | 4.832 |
| [S20/Q18](#s20) | failed | ["intercom__conversation_enhanced"] | 0 / {} | [] | [] | unknown | 未取得；调用总时长 0.141 ms |
| [S21/Q19](#s21) | failed | ["intercom__conversation_enhanced"] | 0 / {} | [] | [] | unknown | 未取得；调用总时长 0.165 ms |
| [S22/Q20](#s22) | success | ["intercom__conversation_enhanced"] | 0 / {} | [] | [] | 8 | 3.019 |
| [S23/Q21](#s23) | success | ["intercom__conversation_metrics"] | 0 / {} | [] | [] | 8 | 2.686 |
| [S24/Q22](#s24) | failed | ["intercom__conversation_metrics"] | 0 / {} | [] | [] | unknown | 未取得；调用总时长 0.175 ms |
| [S25/Q23](#s25) | success | ["intercom__conversation_metrics"] | 0 / {} | [] | [] | 5 | 0.38 |
| [S26/Q24](#s26) | success | ["intercom__conversation_metrics"] | 0 / {} | [] | ["COUNT(*)", "COUNT(DISTINCT conversation_id)"] | 1 | 6.007 |
| [S27/Q25](#s27) | success | ["intercom__company_enhanced"] | 0 / {} | [] | [] | 2509 | 3.779 |
| [S28/Q26](#s28) | success | ["intercom__conversation_enhanced"] | 0 / {} | [] | [] | 6703 | 9.51 |
| [S29/Q27](#s29) | success | ["intercom__conversation_metrics"] | 0 / {} | [] | [] | 6703 | 6.296 |
| [S30/Q28](#s30) | success | ["intercom__conversation_enhanced"] | 0 / {} | [] | [] | 75 | 3.88 |
| [S31/Q29](#s31) | success | ["intercom__company_enhanced"] | 0 / {} | [] | [] | 2509 | 1.994 |
| [S32/Q30](#s32) | success | ["intercom__company_enhanced"] | 0 / {} | ["company_name"] | ["COUNT(*)", "COUNT(DISTINCT company_id)"] | 10 | 2.35 |
| [S33/Q31](#s33) | success | ["intercom__company_enhanced"] | 0 / {} | ["company_name"] | ["COUNT(DISTINCT renewal_window)", "GROUP_CONCAT(DISTINCT renewal_window)"] | 5 | 3.91 |
| [S34/Q32](#s34) | success | ["intercom__company_enhanced"] | 0 / {} | [] | [] | 2509 | 3.38 |
| [S35/Q33](#s35) | success | ["intercom__conversation_enhanced"] | 0 / {} | [] | ["MIN(conversation_created_at)", "MAX(conversation_created_at)", "COUNT(*)"] | 1 | 2.835 |
| [S36/Q34](#s36) | success | ["intercom__conversation_enhanced"] | 0 / {} | [] | [] | 6703 | 10.206 |
| [S37/Q35](#s37) | success | ["intercom__company_enhanced"] | 0 / {} | [] | [] | 2509 | 3.688 |
| [S38/Q36](#s38) | success | ["intercom__conversation_enhanced"] | 0 / {} | [] | [] | 6703 | 11.456 |
| [S39/Q37](#s39) | success | ["intercom__conversation_metrics"] | 0 / {} | [] | [] | 6703 | 10.998 |
| [S40/Q38](#s40) | success | ["intercom__company_enhanced"] | 0 / {} | [] | [] | 2509 | 3.56 |
| [S41/Q39](#s41) | success | ["intercom__conversation_enhanced"] | 0 / {} | [] | [] | 6703 | 5.132 |
| [S42/Q40](#s42) | success | ["intercom__conversation_enhanced"] | 0 / {} | [] | [] | 6703 | 10.307 |
| [S43/Q41](#s43) | success | ["intercom__company_enhanced"] | 0 / {} | [] | [] | 2509 | 3.785 |
| [S44/Q42](#s44) | success | ["intercom__conversation_enhanced"] | 0 / {} | [] | [] | 6703 | 9.796 |
| [S45/Q43](#s45) | success | ["intercom__company_enhanced"] | 0 / {} | [] | [] | 2509 | 3.78 |
| [S46/Q44](#s46) | success | ["intercom__company_metrics"] | 0 / {} | [] | [] | 2509 | 11.952 |
| [S47/Q45](#s47) | success | ["intercom__company_enhanced"] | 0 / {} | [] | [] | 2509 | 4.365 |
| [S48/Q46](#s48) | success | ["intercom__company_metrics"] | 0 / {} | [] | [] | 2509 | 11.66 |
| [S49/Q47](#s49) | success | ["intercom__company_enhanced"] | 0 / {} | [] | [] | 2509 | 3.918 |
| [S50/Q48](#s50) | success | ["intercom__conversation_enhanced"] | 0 / {} | [] | [] | 6703 | 9.725 |
| [S51/Q49](#s51) | success | ["intercom__conversation_metrics"] | 0 / {} | [] | [] | 6703 | 10.77 |
| [S52/Q50](#s52) | success | ["intercom__company_enhanced"] | 0 / {} | [] | [] | 2509 | 2.734 |
| [S53/Q51](#s53) | success | ["intercom__company_enhanced"] | 0 / {} | [] | [] | 2509 | 3.371 |
| [S54/Q52](#s54) | success | ["intercom__company_enhanced"] | 0 / {} | [] | [] | 2509 | 4.023 |
| [S55/Q53](#s55) | success | ["intercom__conversation_enhanced"] | 0 / {} | [] | [] | 6703 | 10.735 |
| [S56/Q54](#s56) | success | ["intercom__company_enhanced"] | 0 / {} | [] | [] | 2509 | 4.948 |
| [S57/Q55](#s57) | success | ["intercom__company_metrics"] | 0 / {} | [] | [] | 2509 | 11.868 |
| [S58/Q56](#s58) | success | ["intercom__company_enhanced"] | 0 / {} | [] | [] | 2509 | 4.978 |
| [S59/Q57](#s59) | success | ["intercom__company_metrics"] | 0 / {} | [] | [] | 2509 | 11.732 |
| [S60/Q58](#s60) | success | ["intercom__conversation_enhanced"] | 0 / {} | [] | [] | 6703 | 10.146 |
| [S61/Q59](#s61) | success | ["intercom__conversation_metrics"] | 0 / {} | [] | [] | 6703 | 7.91 |
| [S62/Q60](#s62) | success | ["intercom__company_enhanced"] | 0 / {} | [] | [] | 2509 | 3.946 |
| [S63/Q61](#s63) | failed | ["intercom__conversation_metrics"] | 0 / {} | [] | [] | unknown | 未取得；调用总时长 0.158 ms |
| [S64/Q62](#s64) | success | ["intercom__company_enhanced"] | 0 / {} | [] | [] | 2509 | 3.482 |
| [S65/Q63](#s65) | success | ["intercom__company_enhanced"] | 0 / {} | [] | [] | 2509 | 3.389 |
| [S66/Q64](#s66) | success | ["intercom__conversation_enhanced"] | 0 / {} | [] | [] | 75 | 3.75 |
| [S67/Q65](#s67) | success | ["intercom__company_enhanced"] | 0 / {} | [] | [] | 2509 | 3.778 |
| [S68/Q66](#s68) | success | ["intercom__company_enhanced"] | 0 / {} | [] | [] | 2509 | 3.859 |
| [S69/Q67](#s69) | success | ["intercom__conversation_enhanced"] | 0 / {} | [] | [] | 6703 | 10.651 |
| [S70/Q68](#s70) | success | ["intercom__conversation_metrics"] | 0 / {} | [] | [] | 6703 | 8.685 |
| [S71/Q69](#s71) | success | ["intercom__company_enhanced"] | 0 / {} | [] | [] | 2509 | 4.419 |
| [S72/Q70](#s72) | success | ["intercom__company_metrics"] | 0 / {} | [] | [] | 2509 | 11.749 |
| [S73/Q71](#s73) | success | ["intercom__company_enhanced"] | 0 / {} | [] | [] | 2509 | 4.331 |
| [S74/Q72](#s74) | success | ["intercom__company_metrics"] | 0 / {} | [] | [] | 2509 | 11.698 |
| [S75/Q73](#s75) | success | ["intercom__company_enhanced"] | 0 / {} | [] | ["SUM(CASE WHEN renewal_window = 'inside_90_days' THEN 1 ELSE 0 END)", "SUM(CASE WHEN renewal_window = 'within_30_days_past' THEN 1 ELSE 0 END)", "SUM(CASE WHEN renewal_window = 'future_90_plus' THEN 1 ELSE 0 END)"] | 1 | 13.573 |
| [S76/Q74](#s76) | success | ["intercom__company_enhanced"] | 0 / {} | ["SUBSTRING(all_company_tags, INSTR(all_company_tags, 'expansion_signal=') + 16, INSTR(SUBSTRING(all_company_tags, INSTR(all_company_tags, 'expansion_signal=') + 16), '\|') - 1)", "SUBSTRING(all_company_tags, INSTR(all_company_tags, 'sentiment_trend=') + 16, INSTR(SUBSTRING(all_company_tags, INSTR(all_company_tags, 'sentiment_trend=') + 16), '\|') - 1)"] | ["COUNT(*)"] | 7 | 18.593 |
| [S77/Q75](#s77) | success | ["intercom__company_enhanced"] | 0 / {} | ["SUBSTRING(all_company_tags, INSTR(all_company_tags, 'last_value_milestone=') + 21, INSTR(SUBSTRING(all_company_tags, INSTR(all_company_tags, 'last_value_milestone=') + 21), '\|') - 1)", "SUBSTRING(all_company_tags, INSTR(all_company_tags, 'expansion_signal=') + 16, INSTR(SUBSTRING(all_company_tags, INSTR(all_company_tags, 'expansion_signal=') + 16), '\|') - 1)"] | ["COUNT(*)"] | 12 | 20.483 |
| [S78/Q76](#s78) | success | ["intercom__company_enhanced"] | 0 / {} | ["SUBSTRING(all_company_tags, INSTR(all_company_tags, 'education_focus=') + 17, INSTR(SUBSTRING(all_company_tags, INSTR(all_company_tags, 'education_focus=') + 17), '\|') - 1)", "SUBSTRING(all_company_tags, INSTR(all_company_tags, 'expansion_signal=') + 16, INSTR(SUBSTRING(all_company_tags, INSTR(all_company_tags, 'expansion_signal=') + 16), '\|') - 1)"] | ["COUNT(*)"] | 12 | 20.662 |


## 元数据和设置

| SQL | 类别 | 状态 | 内容 |
| --- | --- | --- | --- |
| S1 | connection_setup | success | PRAGMA query_only=ON |
| S2 | metadata | success | SELECT name,sql FROM sqlite_master WHERE type='table' ORDER BY name |


## Python 与执行位置

人工源码审查：**database_first_violation**。Python 导出公司记录后拆解标签、按标签计数、筛选 churn 行并计算日期最值；常规过滤、计数和最值可在 SQL 完成。标签解析应单独评估 SQLite 字符串或 JSON 表达式的可表达性，不能仅凭解析代码将所有后续聚合都认定为必要例外。 后续 P10 明确在 Python 合并会话表与指标表，再按公司求负面比例、平均解决时长和重开比例；P12 按公司和年份分组。这些进一步提供了可下推关系连接与聚合的证据。 [证据](../reviews/dacomp-100.json)。

P1：Parse the all_company_tags column to extract structured fields like renewal_window, renewal_date, contract_size, industry, etc. since SQLite lacks regex functions.

[源码](../../../runs/dsv4flash-db-first-full-01/dacomp-100/attempt-01/python/P1.py)；[输出](../../../runs/dsv4flash-db-first-full-01/dacomp-100/attempt-01/python/P1.stdout)；[错误](../../../runs/dsv4flash-db-first-full-01/dacomp-100/attempt-01/python/P1.stderr)。检出需人工核验的 SQL 可实现操作：.query(；不能仅凭理由判为合规。

P2：Examine renewal_history field values and date ranges across datasets to understand the current date anchor and possible renewal outcome labels.

[源码](../../../runs/dsv4flash-db-first-full-01/dacomp-100/attempt-01/python/P2.py)；[输出](../../../runs/dsv4flash-db-first-full-01/dacomp-100/attempt-01/python/P2.stdout)；[错误](../../../runs/dsv4flash-db-first-full-01/dacomp-100/attempt-01/python/P2.stderr)。检出需人工核验的 SQL 可实现操作：.query(；不能仅凭理由判为合规。

P3：Extract sentiment values from conversation tags to understand the sentiment classification scheme, and check if there's a way to classify renewal outcomes (renewed vs churned) from the data.

[源码](../../../runs/dsv4flash-db-first-full-01/dacomp-100/attempt-01/python/P3.py)；[输出](../../../runs/dsv4flash-db-first-full-01/dacomp-100/attempt-01/python/P3.stdout)；[错误](../../../runs/dsv4flash-db-first-full-01/dacomp-100/attempt-01/python/P3.stderr)。检出需人工核验的 SQL 可实现操作：groupby(, .query(；不能仅凭理由判为合规。

P4：Determine which companies have conversations, how conversations map to companies, and whether a renewal outcome label exists anywhere in the data.

[源码](../../../runs/dsv4flash-db-first-full-01/dacomp-100/attempt-01/python/P4.py)；[输出](../../../runs/dsv4flash-db-first-full-01/dacomp-100/attempt-01/python/P4.stdout)；[错误](../../../runs/dsv4flash-db-first-full-01/dacomp-100/attempt-01/python/P4.stderr)。检出需人工核验的 SQL 可实现操作：.query(；不能仅凭理由判为合规。

P5：Examine the 75 companies that have conversations and their tags, plus conversation subjects/remarks, to identify any renewal outcome signal.

[源码](../../../runs/dsv4flash-db-first-full-01/dacomp-100/attempt-01/python/P5.py)；[输出](../../../runs/dsv4flash-db-first-full-01/dacomp-100/attempt-01/python/P5.stdout)；[错误](../../../runs/dsv4flash-db-first-full-01/dacomp-100/attempt-01/python/P5.stderr)。检出需人工核验的 SQL 可实现操作：.query(；不能仅凭理由判为合规。

P6：Explore the 75 companies with conversations to understand their renewal windows, and check if conversation remarks can serve as renewal outcome labels. Need to parse tags and join data.

[源码](../../../runs/dsv4flash-db-first-full-01/dacomp-100/attempt-01/python/P6.py)；[输出](../../../runs/dsv4flash-db-first-full-01/dacomp-100/attempt-01/python/P6.stdout)；[错误](../../../runs/dsv4flash-db-first-full-01/dacomp-100/attempt-01/python/P6.stderr)。检出需人工核验的 SQL 可实现操作：.query(；不能仅凭理由判为合规。

P7：Debug the company name matching between conversations and company table - verify which companies actually have conversations.

[源码](../../../runs/dsv4flash-db-first-full-01/dacomp-100/attempt-01/python/P7.py)；[输出](../../../runs/dsv4flash-db-first-full-01/dacomp-100/attempt-01/python/P7.stdout)；[错误](../../../runs/dsv4flash-db-first-full-01/dacomp-100/attempt-01/python/P7.stderr)。检出需人工核验的 SQL 可实现操作：.query(；不能仅凭理由判为合规。

P8：Understand the relationship between renewal windows and renewal dates to determine the 'current date' anchor of the dataset snapshot.

[源码](../../../runs/dsv4flash-db-first-full-01/dacomp-100/attempt-01/python/P8.py)；[输出](../../../runs/dsv4flash-db-first-full-01/dacomp-100/attempt-01/python/P8.stdout)；[错误](../../../runs/dsv4flash-db-first-full-01/dacomp-100/attempt-01/python/P8.stderr)。检出需人工核验的 SQL 可实现操作：groupby(, .query(；不能仅凭理由判为合规。

P9：Examine how conversations for a given company name are distributed across time and how they relate to that account's renewal dates across its company_ids.

[源码](../../../runs/dsv4flash-db-first-full-01/dacomp-100/attempt-01/python/P9.py)；[输出](../../../runs/dsv4flash-db-first-full-01/dacomp-100/attempt-01/python/P9.stdout)；[错误](../../../runs/dsv4flash-db-first-full-01/dacomp-100/attempt-01/python/P9.stderr)。检出需人工核验的 SQL 可实现操作：.query(, sort_values(；不能仅凭理由判为合规。

P10：Use expansion_signal as a proxy for renewal outcome (Upsell Ready = renewed, Risk Mitigation = churned) and compute the core features from conversation data for the 75 companies with conversations.

[源码](../../../runs/dsv4flash-db-first-full-01/dacomp-100/attempt-01/python/P10.py)；[输出](../../../runs/dsv4flash-db-first-full-01/dacomp-100/attempt-01/python/P10.stdout)；[错误](../../../runs/dsv4flash-db-first-full-01/dacomp-100/attempt-01/python/P10.stderr)。检出需人工核验的 SQL 可实现操作：.merge(, .query(；不能仅凭理由判为合规。

P11：Check the conversation date distribution to understand why the 30-day window before renewal has no matching conversations.

[源码](../../../runs/dsv4flash-db-first-full-01/dacomp-100/attempt-01/python/P11.py)；[输出](../../../runs/dsv4flash-db-first-full-01/dacomp-100/attempt-01/python/P11.stdout)；[错误](../../../runs/dsv4flash-db-first-full-01/dacomp-100/attempt-01/python/P11.stderr)。检出需人工核验的 SQL 可实现操作：.query(, sort_values(；不能仅凭理由判为合规。

P12：Examine conversation patterns by company and year, and check correlation between conversation sentiment and company health/expansion signals to identify the renewal outcome signal.

[源码](../../../runs/dsv4flash-db-first-full-01/dacomp-100/attempt-01/python/P12.py)；[输出](../../../runs/dsv4flash-db-first-full-01/dacomp-100/attempt-01/python/P12.stdout)；[错误](../../../runs/dsv4flash-db-first-full-01/dacomp-100/attempt-01/python/P12.stderr)。检出需人工核验的 SQL 可实现操作：groupby(, .query(, sort_values(；不能仅凭理由判为合规。

P13：Check how many conversations fall in the 30-day pre-renewal window for within_30_days_past and inside_90_days companies, using 2023 conversations mapped to renewal dates.

[源码](../../../runs/dsv4flash-db-first-full-01/dacomp-100/attempt-01/python/P13.py)；[输出](../../../runs/dsv4flash-db-first-full-01/dacomp-100/attempt-01/python/P13.stdout)；[错误](../../../runs/dsv4flash-db-first-full-01/dacomp-100/attempt-01/python/P13.stderr)。检出需人工核验的 SQL 可实现操作：.query(；不能仅凭理由判为合规。

P14：Use company_metrics table features (already aggregated) combined with company tags to build the full feature set. The company_metrics provides pre-computed conversation-level stats at company level, which is exactly what we need for the features.

[源码](../../../runs/dsv4flash-db-first-full-01/dacomp-100/attempt-01/python/P14.py)；[输出](../../../runs/dsv4flash-db-first-full-01/dacomp-100/attempt-01/python/P14.stdout)；[错误](../../../runs/dsv4flash-db-first-full-01/dacomp-100/attempt-01/python/P14.stderr)。检出需人工核验的 SQL 可实现操作：.merge(, .query(；不能仅凭理由判为合规。

P15：Fix the created_at column missing from the query and compute the full feature comparison between renewed and churned companies.

[源码](../../../runs/dsv4flash-db-first-full-01/dacomp-100/attempt-01/python/P15.py)；[输出](../../../runs/dsv4flash-db-first-full-01/dacomp-100/attempt-01/python/P15.stdout)；[错误](../../../runs/dsv4flash-db-first-full-01/dacomp-100/attempt-01/python/P15.stderr)。检出需人工核验的 SQL 可实现操作：.merge(, .query(, sort_values(；不能仅凭理由判为合规。

P16：Compute features from raw conversation data for within_30_days_past companies (whose renewal just happened) and compare between renewed (Upsell Ready) and churned (Risk Mitigation) groups.

[源码](../../../runs/dsv4flash-db-first-full-01/dacomp-100/attempt-01/python/P16.py)；[输出](../../../runs/dsv4flash-db-first-full-01/dacomp-100/attempt-01/python/P16.stdout)；[错误](../../../runs/dsv4flash-db-first-full-01/dacomp-100/attempt-01/python/P16.stderr)。检出需人工核验的 SQL 可实现操作：.merge(, .query(；不能仅凭理由判为合规。

P17：Understand the relationship between potential outcome labels (expansion_signal, health_score, sentiment_trend) to establish a defensible renewed vs churned label for the historical cohort.

[源码](../../../runs/dsv4flash-db-first-full-01/dacomp-100/attempt-01/python/P17.py)；[输出](../../../runs/dsv4flash-db-first-full-01/dacomp-100/attempt-01/python/P17.stdout)；[错误](../../../runs/dsv4flash-db-first-full-01/dacomp-100/attempt-01/python/P17.stderr)。检出需人工核验的 SQL 可实现操作：groupby(, .query(；不能仅凭理由判为合规。

P18：Test whether conversation sentiment proportions correlate with company sentiment_trend and expansion_signal, to validate the negative-sentiment definition and feature validity.

[源码](../../../runs/dsv4flash-db-first-full-01/dacomp-100/attempt-01/python/P18.py)；[输出](../../../runs/dsv4flash-db-first-full-01/dacomp-100/attempt-01/python/P18.stdout)；[错误](../../../runs/dsv4flash-db-first-full-01/dacomp-100/attempt-01/python/P18.stderr)。检出需人工核验的 SQL 可实现操作：groupby(, .query(；不能仅凭理由判为合规。

P19：Compute comprehensive feature comparison with AUC/quantile discriminative power for the within_30_days_past historical cohort, using expansion_signal as outcome label. This analysis requires Python for AUC calculation, quantile computation, and visualization.

[源码](../../../runs/dsv4flash-db-first-full-01/dacomp-100/attempt-01/python/P19.py)；[输出](../../../runs/dsv4flash-db-first-full-01/dacomp-100/attempt-01/python/P19.stdout)；[错误](../../../runs/dsv4flash-db-first-full-01/dacomp-100/attempt-01/python/P19.stderr)。检出需人工核验的 SQL 可实现操作：.merge(, .query(, sort_values(；不能仅凭理由判为合规。

P20：Compute AUC manually (no sklearn available) and full feature discriminative power analysis for the within_30_days_past historical cohort.

[源码](../../../runs/dsv4flash-db-first-full-01/dacomp-100/attempt-01/python/P20.py)；[输出](../../../runs/dsv4flash-db-first-full-01/dacomp-100/attempt-01/python/P20.stdout)；[错误](../../../runs/dsv4flash-db-first-full-01/dacomp-100/attempt-01/python/P20.stderr)。检出需人工核验的 SQL 可实现操作：.merge(, .query(, sort_values(；不能仅凭理由判为合规。

P21：Fix company_age_days column source and run the full feature discriminative power analysis with manual AUC.

[源码](../../../runs/dsv4flash-db-first-full-01/dacomp-100/attempt-01/python/P21.py)；[输出](../../../runs/dsv4flash-db-first-full-01/dacomp-100/attempt-01/python/P21.stdout)；[错误](../../../runs/dsv4flash-db-first-full-01/dacomp-100/attempt-01/python/P21.stderr)。检出需人工核验的 SQL 可实现操作：.merge(, .query(, sort_values(；不能仅凭理由判为合规。

P22：Examine whether conversation-level SLA, ratings, and reopen patterns differ between renewed and churned groups, since conversation-derived features appeared weak. Also examine tag-based features like communication_cadence and playbook by outcome.

[源码](../../../runs/dsv4flash-db-first-full-01/dacomp-100/attempt-01/python/P22.py)；[输出](../../../runs/dsv4flash-db-first-full-01/dacomp-100/attempt-01/python/P22.stdout)；[错误](../../../runs/dsv4flash-db-first-full-01/dacomp-100/attempt-01/python/P22.stderr)。检出需人工核验的 SQL 可实现操作：groupby(, .query(, sort_values(；不能仅凭理由判为合规。

P23：Investigate tag-based features more carefully, especially education_focus, communication_cadence, and playbook distributions by outcome, using the within_30_days_past cohort.

[源码](../../../runs/dsv4flash-db-first-full-01/dacomp-100/attempt-01/python/P23.py)；[输出](../../../runs/dsv4flash-db-first-full-01/dacomp-100/attempt-01/python/P23.stdout)；[错误](../../../runs/dsv4flash-db-first-full-01/dacomp-100/attempt-01/python/P23.stderr)。检出需人工核验的 SQL 可实现操作：groupby(, .query(；不能仅凭理由判为合规。

P24：Understand the mapping between company names and outcomes in the historical cohort, since conversations are at name level while outcomes are at company_id level.

[源码](../../../runs/dsv4flash-db-first-full-01/dacomp-100/attempt-01/python/P24.py)；[输出](../../../runs/dsv4flash-db-first-full-01/dacomp-100/attempt-01/python/P24.stdout)；[错误](../../../runs/dsv4flash-db-first-full-01/dacomp-100/attempt-01/python/P24.stderr)。检出需人工核验的 SQL 可实现操作：groupby(, .query(；不能仅凭理由判为合规。

P25：Check whether renewal outcome is consistent within company names (which share conversation data), and evaluate name-level conversation features by outcome.

[源码](../../../runs/dsv4flash-db-first-full-01/dacomp-100/attempt-01/python/P25.py)；[输出](../../../runs/dsv4flash-db-first-full-01/dacomp-100/attempt-01/python/P25.stdout)；[错误](../../../runs/dsv4flash-db-first-full-01/dacomp-100/attempt-01/python/P25.stderr)。检出需人工核验的 SQL 可实现操作：groupby(, .query(, sort_values(；不能仅凭理由判为合规。

P26：Compute name-level conversation features and compare between renewed and churned names in the historical cohort, since outcomes are uniform within company names and conversations are name-level.

[源码](../../../runs/dsv4flash-db-first-full-01/dacomp-100/attempt-01/python/P26.py)；[输出](../../../runs/dsv4flash-db-first-full-01/dacomp-100/attempt-01/python/P26.stdout)；[错误](../../../runs/dsv4flash-db-first-full-01/dacomp-100/attempt-01/python/P26.stderr)。检出需人工核验的 SQL 可实现操作：groupby(, .merge(, .query(；不能仅凭理由判为合规。

P27：Examine full-population relationships between tag-based features (feature adoption, sentiment, communication cadence, education focus, milestone) and renewal outcome proxy to identify strongest leading indicators.

[源码](../../../runs/dsv4flash-db-first-full-01/dacomp-100/attempt-01/python/P27.py)；[输出](../../../runs/dsv4flash-db-first-full-01/dacomp-100/attempt-01/python/P27.stdout)；[错误](../../../runs/dsv4flash-db-first-full-01/dacomp-100/attempt-01/python/P27.stderr)。检出需人工核验的 SQL 可实现操作：groupby(, .merge(, .query(；不能仅凭理由判为合规。

P28：Analyze the inside_90_days target population: risk segmentation by industry and contract size, and identify where risk concentrates for operational recommendations.

[源码](../../../runs/dsv4flash-db-first-full-01/dacomp-100/attempt-01/python/P28.py)；[输出](../../../runs/dsv4flash-db-first-full-01/dacomp-100/attempt-01/python/P28.stdout)；[错误](../../../runs/dsv4flash-db-first-full-01/dacomp-100/attempt-01/python/P28.stderr)。检出需人工核验的 SQL 可实现操作：groupby(, .merge(, .query(, sort_values(；不能仅凭理由判为合规。

P29：Create summary visualizations for the report: feature discriminative power bar chart, industry risk heatmap, and segment-level recommendations.

[源码](../../../runs/dsv4flash-db-first-full-01/dacomp-100/attempt-01/python/P29.py)；[输出](../../../runs/dsv4flash-db-first-full-01/dacomp-100/attempt-01/python/P29.stdout)；[错误](../../../runs/dsv4flash-db-first-full-01/dacomp-100/attempt-01/python/P29.stderr)。自动源码筛查未检出预设迁出信号；这不是全面语义合规证明。

P30：Create a final visualization showing the milestone type vs outcome relationship, and a summary of the at-risk segments for the report.

[源码](../../../runs/dsv4flash-db-first-full-01/dacomp-100/attempt-01/python/P30.py)；[输出](../../../runs/dsv4flash-db-first-full-01/dacomp-100/attempt-01/python/P30.stdout)；[错误](../../../runs/dsv4flash-db-first-full-01/dacomp-100/attempt-01/python/P30.stderr)。自动源码筛查未检出预设迁出信号；这不是全面语义合规证明。

## 优化机会

已验证候选。筛选限于精确 SQL、相同自包含 CTE、相同单表完整过滤、可分解单表聚合；未覆盖任意 Join 等价和一般谓词蕴含。全部候选都是 offline，未测在线预测。

| 候选 | 类型 | 已有结果 | 覆盖 SQL | 后续次数 | 中间行数 | 验证 | 成本 |
| --- | --- | --- | --- | --- | --- | --- | --- |
| C1 | exact-result reuse | True | ["S18", "S46", "S48", "S57", "S59", "S72", "S74"] | 6 | 2509 | verified | Not benchmarked; correctness alone does not establish net speedup. |
| C2 | exact-result reuse | True | ["S27", "S34", "S37", "S40", "S43", "S45", "S49", "S53", "S54", "S62", "S64", "S65", "S67", "S68"] | 13 | 2509 | verified | Not benchmarked; correctness alone does not establish net speedup. |
| C3 | exact-result reuse | True | ["S30", "S66"] | 1 | unknown | not_verified_cap | Not tested |
| C4 | exact-result reuse | True | ["S36", "S42", "S44", "S50", "S55", "S60", "S69"] | 6 | 6703 | verified | Not benchmarked; correctness alone does not establish net speedup. |
| C5 | exact-result reuse | True | ["S47", "S56"] | 1 | unknown | not_verified_cap | Not tested |
| C6 | exact-result reuse | True | ["S61", "S70"] | 1 | unknown | not_verified_cap | Not tested |
| C7 | exact-result reuse | True | ["S71", "S73"] | 1 | unknown | not_verified_cap | Not tested |
| C8 | common filtered view | False | ["S76", "S77", "S78"] | 2 | unknown | not_verified_cap | Not tested |
| C9 | aggregate MV | False | ["S76", "S77", "S78"] | 2 | unknown | not_verified_cap | Not tested |


已验证覆盖（含触发查询、候选并集去重）：28/71 条成功数据 SQL。正确性仅针对当前数据库快照；未测性能的候选不能声称已加速。

[完整 build/rewrite 与比较证据](dacomp-100.analysis.json)。

### C2：exact-result reuse

Identical normalized SQL and parameters; archive equality checked.

原查询 [S27](#s27), [S34](#s34), [S37](#s37), [S40](#s40), [S43](#s43), [S45](#s45), [S49](#s49), [S53](#s53), [S54](#s54), [S62](#s62), [S64](#s64), [S65](#s65), [S67](#s67), [S68](#s68) → 保留前序结果 S27 → 后续 13 次可复用。该构建点为事后假设，不代表 Agent 当时预知后续。

| 原 SQL | 列名一致 | 结果一致 | 比较方法 |
| --- | --- | --- | --- |
| S34 | True | True | exact_multiset |
| S37 | True | True | exact_multiset |
| S40 | True | True | exact_multiset |
| S43 | True | True | exact_multiset |
| S45 | True | True | exact_multiset |
| S49 | True | True | exact_multiset |
| S53 | True | True | exact_multiset |
| S54 | True | True | exact_multiset |
| S62 | True | True | exact_multiset |
| S64 | True | True | exact_multiset |
| S65 | True | True | exact_multiset |
| S67 | True | True | exact_multiset |
| S68 | True | True | exact_multiset |


验证状态：verified；成本结论：Not benchmarked; correctness alone does not establish net speedup.

### C1：exact-result reuse

Identical normalized SQL and parameters; archive equality checked.

原查询 [S18](#s18), [S46](#s46), [S48](#s48), [S57](#s57), [S59](#s59), [S72](#s72), [S74](#s74) → 保留前序结果 S18 → 后续 6 次可复用。该构建点为事后假设，不代表 Agent 当时预知后续。

| 原 SQL | 列名一致 | 结果一致 | 比较方法 |
| --- | --- | --- | --- |
| S46 | True | True | exact_multiset |
| S48 | True | True | exact_multiset |
| S57 | True | True | exact_multiset |
| S59 | True | True | exact_multiset |
| S72 | True | True | exact_multiset |
| S74 | True | True | exact_multiset |


验证状态：verified；成本结论：Not benchmarked; correctness alone does not establish net speedup.

### C4：exact-result reuse

Identical normalized SQL and parameters; archive equality checked.

原查询 [S36](#s36), [S42](#s42), [S44](#s44), [S50](#s50), [S55](#s55), [S60](#s60), [S69](#s69) → 保留前序结果 S36 → 后续 6 次可复用。该构建点为事后假设，不代表 Agent 当时预知后续。

| 原 SQL | 列名一致 | 结果一致 | 比较方法 |
| --- | --- | --- | --- |
| S42 | True | True | exact_multiset |
| S44 | True | True | exact_multiset |
| S50 | True | True | exact_multiset |
| S55 | True | True | exact_multiset |
| S60 | True | True | exact_multiset |
| S69 | True | True | exact_multiset |


验证状态：verified；成本结论：Not benchmarked; correctness alone does not establish net speedup.

结果依赖：自动记录 SQL→Python 的接口父调用，以及源码中引用归档文件的消费者；字面值相同不认定因果。模型方向选择需要人工读取消息，尚未做全面因果标注。

[原始报告](../../../runs/dsv4flash-db-first-full-01/dacomp-100/attempt-01/answer.md)；[统一消息](../../../runs/dsv4flash-db-first-full-01/dacomp-100/attempt-01/messages.jsonl)；[原始 OpenCode 事件](../../../runs/dsv4flash-db-first-full-01/dacomp-100/attempt-01/opencode.jsonl)；[SQL 引擎日志](../../../runs/dsv4flash-db-first-full-01/dacomp-100/attempt-01/sql_journal.jsonl)。

[可读报告（本地图片链接规范化）](../answers/dacomp-100.md)。原始回答保留，分析结论未改写。

## S1

类别 `connection_setup`；来源 `connection`；调用 `24b9d2de160540f787f61b271f6cd426`；状态 `success`。

```sql
PRAGMA query_only=ON
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-100/attempt-01/sql/S1.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-100/attempt-01/sql/S1.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-100/attempt-01/results/S1.rows.jsonl)；完整：True；SHA256：`e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`。

## S2

类别 `metadata`；来源 `list_db`；调用 `24b9d2de160540f787f61b271f6cd426`；状态 `success`。

```sql
SELECT name,sql FROM sqlite_master WHERE type='table' ORDER BY name
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-100/attempt-01/sql/S2.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-100/attempt-01/sql/S2.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-100/attempt-01/results/S2.rows.jsonl)；完整：True；SHA256：`30f2968ede0397045b1cb864675e9a27e4a50f67145a84442aaec161c9970a14`。

## S3

类别 `data`；来源 `query_db`；调用 `3cd4ffed1b094ab0b50572542de4fa1e`；状态 `success`。

```sql
SELECT COUNT(*) AS n_companies FROM intercom__company_enhanced
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-100/attempt-01/sql/S3.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-100/attempt-01/sql/S3.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-100/attempt-01/results/S3.rows.jsonl)；完整：True；SHA256：`b0d6d21a6709824bcb4210d15c142d9b8c0ad2fa9f4299e758bd927ce4d24ff5`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "intercom__company_enhanced", "kind": "base", "block": null, "base_tables": ["intercom__company_enhanced"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |


## S4

类别 `data`；来源 `query_db`；调用 `be971df48b864cc997352d6005ac85b2`；状态 `success`。

```sql
SELECT COUNT(*) AS n_metrics FROM intercom__company_metrics
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-100/attempt-01/sql/S4.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-100/attempt-01/sql/S4.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-100/attempt-01/results/S4.rows.jsonl)；完整：True；SHA256：`b0d6d21a6709824bcb4210d15c142d9b8c0ad2fa9f4299e758bd927ce4d24ff5`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "intercom__company_metrics", "kind": "base", "block": null, "base_tables": ["intercom__company_metrics"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |


## S5

类别 `data`；来源 `query_db`；调用 `b364be6f9ac2490781a84ee1faa0e3b3`；状态 `success`。

```sql
SELECT COUNT(*) AS n_conv FROM intercom__conversation_metrics
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-100/attempt-01/sql/S5.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-100/attempt-01/sql/S5.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-100/attempt-01/results/S5.rows.jsonl)；完整：True；SHA256：`20b1d17818ff06b3c178fb6a083d46fc454d428bcb3a0a8118c827db65a82b2e`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "intercom__conversation_metrics", "kind": "base", "block": null, "base_tables": ["intercom__conversation_metrics"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |


## S6

类别 `data`；来源 `query_db`；调用 `5939eb3401364f3ea42970eeae093eda`；状态 `success`。

```sql
SELECT * FROM intercom__company_enhanced LIMIT 5
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-100/attempt-01/sql/S6.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-100/attempt-01/sql/S6.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-100/attempt-01/results/S6.rows.jsonl)；完整：True；SHA256：`42ccbbf90aaca5b0f054329ad8ac03f2c431abc7833f55ae4c2984901eda0e8f`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "intercom__company_enhanced", "kind": "base", "block": null, "base_tables": ["intercom__company_enhanced"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |


## S7

类别 `data`；来源 `query_db`；调用 `b18928ca8b6e4bb3a63f070e13d4c202`；状态 `failed`。

```sql
SELECT renewal_window, COUNT(*) AS n FROM (
  SELECT *, regexp_replace(all_company_tags, '.*renewal_window=([^|]+).*', '\1') AS renewal_window FROM intercom__company_enhanced
) GROUP BY renewal_window ORDER BY n DESC
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-100/attempt-01/sql/S7.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-100/attempt-01/sql/S7.parameters.json)。

错误：`OperationalError('no such function: regexp_replace')`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "intercom__company_enhanced", "kind": "base", "block": null, "base_tables": ["intercom__company_enhanced"]}] | [] | [] |
| B2 | [{"alias": "", "kind": "derived", "block": "B1", "base_tables": ["intercom__company_enhanced"]}] | [] | ["renewal_window"] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B2 | COUNT(*) | [] | [] | True |


## S8

类别 `data`；来源 `query_db`；调用 `8206956d790a4afbad8cfdb1a4f25da6`；状态 `success`。

```sql
SELECT * FROM intercom__company_metrics LIMIT 3
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-100/attempt-01/sql/S8.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-100/attempt-01/sql/S8.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-100/attempt-01/results/S8.rows.jsonl)；完整：True；SHA256：`a5f1501a9d3640bc51c658deb30131bdf5d010a45c51b36330c49ff5dd918c7b`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "intercom__company_metrics", "kind": "base", "block": null, "base_tables": ["intercom__company_metrics"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |


## S9

类别 `data`；来源 `query_db`；调用 `209c3e24a0bb4fc39eac86cf953c8568`；状态 `success`。

```sql
SELECT * FROM intercom__conversation_metrics LIMIT 3
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-100/attempt-01/sql/S9.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-100/attempt-01/sql/S9.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-100/attempt-01/results/S9.rows.jsonl)；完整：True；SHA256：`4083f92c7f30cf6eba3d122c14ef98e41b3b570e8fb13d9c6b784634a53a46db`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "intercom__conversation_metrics", "kind": "base", "block": null, "base_tables": ["intercom__conversation_metrics"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |


## S10

类别 `data`；来源 `query_db`；调用 `f9087baa01c44fd18a4c7534ec9e4548`；状态 `success`。

```sql
SELECT * FROM intercom__conversation_enhanced LIMIT 3
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-100/attempt-01/sql/S10.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-100/attempt-01/sql/S10.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-100/attempt-01/results/S10.rows.jsonl)；完整：True；SHA256：`a0a787a92075c6339f72fff8b407167b75f93880595df97315ca72cc3c9de1a3`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "intercom__conversation_enhanced", "kind": "base", "block": null, "base_tables": ["intercom__conversation_enhanced"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |


## S11

类别 `data`；来源 `query_db`；调用 `01dfa3754a3a4b468dcec1a1addadd1f`；状态 `success`。

```sql
SELECT conversation_id, all_conversation_tags FROM intercom__conversation_enhanced LIMIT 5
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-100/attempt-01/sql/S11.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-100/attempt-01/sql/S11.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-100/attempt-01/results/S11.rows.jsonl)；完整：True；SHA256：`da98efd3fc8feb494e4e5cf6e30e88bc70b8e11260ecf3527c0bda85e3951888`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "intercom__conversation_enhanced", "kind": "base", "block": null, "base_tables": ["intercom__conversation_enhanced"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |


## S12

类别 `data`；来源 `python`；调用 `0401c6b9a922421c93d441497a5dc563`；状态 `success`。

```sql
SELECT * FROM intercom__company_enhanced
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-100/attempt-01/sql/S12.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-100/attempt-01/sql/S12.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-100/attempt-01/results/S12.rows.jsonl)；完整：True；SHA256：`79dca5b953538e2b52f9ef4834ccb194991320188072996cdb8b7627ac215ab0`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "intercom__company_enhanced", "kind": "base", "block": null, "base_tables": ["intercom__company_enhanced"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |


## S13

类别 `data`；来源 `python`；调用 `f35f7c52bd974aed907703adb58f30ad`；状态 `success`。

```sql
SELECT company_id, all_company_tags, created_at, updated_at FROM intercom__company_enhanced
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-100/attempt-01/sql/S13.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-100/attempt-01/sql/S13.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-100/attempt-01/results/S13.rows.jsonl)；完整：True；SHA256：`2d69982a8d5ff1ae21b3c637938b75af00b96cadb45c446c266654e9ba14141b`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "intercom__company_enhanced", "kind": "base", "block": null, "base_tables": ["intercom__company_enhanced"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |


## S14

类别 `data`；来源 `python`；调用 `d5d9b8934dd04882ae325080796014e7`；状态 `success`。

```sql
SELECT conversation_id, all_conversation_tags, all_contact_company_names FROM intercom__conversation_enhanced
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-100/attempt-01/sql/S14.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-100/attempt-01/sql/S14.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-100/attempt-01/results/S14.rows.jsonl)；完整：True；SHA256：`ef9d535a92c5f31a5f23626aa535212ebb0f2044db663b35d320cf0a604435de`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "intercom__conversation_enhanced", "kind": "base", "block": null, "base_tables": ["intercom__conversation_enhanced"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |


## S15

类别 `data`；来源 `python`；调用 `d5d9b8934dd04882ae325080796014e7`；状态 `success`。

```sql
SELECT all_company_tags FROM intercom__company_enhanced
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-100/attempt-01/sql/S15.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-100/attempt-01/sql/S15.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-100/attempt-01/results/S15.rows.jsonl)；完整：True；SHA256：`9ecd024006e2afe55e49afb468fd7633d9612a38809c9956ce22398cb33f2f87`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "intercom__company_enhanced", "kind": "base", "block": null, "base_tables": ["intercom__company_enhanced"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |


## S16

类别 `data`；来源 `python`；调用 `a452501434a84563b2e87fc4f109da8b`；状态 `success`。

```sql
SELECT conversation_id, all_contact_company_names, conversation_created_at, conversation_state FROM intercom__conversation_enhanced
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-100/attempt-01/sql/S16.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-100/attempt-01/sql/S16.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-100/attempt-01/results/S16.rows.jsonl)；完整：True；SHA256：`4d1e61d2c37de94520fcf6194d1096da6f0f701b91ce3500824f6313040a17d8`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "intercom__conversation_enhanced", "kind": "base", "block": null, "base_tables": ["intercom__conversation_enhanced"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |


## S17

类别 `data`；来源 `python`；调用 `a452501434a84563b2e87fc4f109da8b`；状态 `success`。

```sql
SELECT company_id, company_name, created_at, updated_at, all_company_tags FROM intercom__company_enhanced
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-100/attempt-01/sql/S17.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-100/attempt-01/sql/S17.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-100/attempt-01/results/S17.rows.jsonl)；完整：True；SHA256：`465e9f9be3a4b3cfda53b943d7e66dc16c57960734a62e1ee90b0c88945fbd33`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "intercom__company_enhanced", "kind": "base", "block": null, "base_tables": ["intercom__company_enhanced"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |


## S18

类别 `data`；来源 `python`；调用 `a452501434a84563b2e87fc4f109da8b`；状态 `success`。

```sql
SELECT * FROM intercom__company_metrics
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-100/attempt-01/sql/S18.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-100/attempt-01/sql/S18.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-100/attempt-01/results/S18.rows.jsonl)；完整：True；SHA256：`b76c02be193d729a0c1c0fbaff2eb086166d909b38fccdcc6eb71f1ab6fbe04b`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "intercom__company_metrics", "kind": "base", "block": null, "base_tables": ["intercom__company_metrics"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |


## S19

类别 `data`；来源 `python`；调用 `3f9b124404454fc5909c8837d202813b`；状态 `success`。

```sql
SELECT company_id, company_name, all_company_tags, created_at, updated_at FROM intercom__company_enhanced
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-100/attempt-01/sql/S19.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-100/attempt-01/sql/S19.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-100/attempt-01/results/S19.rows.jsonl)；完整：True；SHA256：`3042800454de7936b639b9e0218e3c398e32243407ca95b96e3e8ef7cf8bfe82`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "intercom__company_enhanced", "kind": "base", "block": null, "base_tables": ["intercom__company_enhanced"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |


## S20

类别 `data`；来源 `python`；调用 `3f9b124404454fc5909c8837d202813b`；状态 `failed`。

```sql
SELECT conversation_id, all_contact_company_names, conversation_created_at, conversation_subject, conversation_rating_remark FROM intercom__conversation_enhanced
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-100/attempt-01/sql/S20.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-100/attempt-01/sql/S20.parameters.json)。

错误：`OperationalError('no such column: conversation_rating_remark')`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "intercom__conversation_enhanced", "kind": "base", "block": null, "base_tables": ["intercom__conversation_enhanced"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |


未解析列血缘：[{"block": "B1", "column": "conversation_rating_remark", "reason": "ambiguous_or_missing_source"}]

## S21

类别 `data`；来源 `query_db`；调用 `a2b69d9c0f854232919975c63b299751`；状态 `failed`。

```sql
SELECT conversation_id, all_contact_company_names, conversation_created_at, conversation_subject, conversation_rating_remark FROM intercom__conversation_enhanced LIMIT 10
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-100/attempt-01/sql/S21.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-100/attempt-01/sql/S21.parameters.json)。

错误：`OperationalError('no such column: conversation_rating_remark')`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "intercom__conversation_enhanced", "kind": "base", "block": null, "base_tables": ["intercom__conversation_enhanced"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |


未解析列血缘：[{"block": "B1", "column": "conversation_rating_remark", "reason": "ambiguous_or_missing_source"}]

## S22

类别 `data`；来源 `query_db`；调用 `1bb48215e8f9447cb7c9b77cbb2f4dab`；状态 `success`。

```sql
SELECT DISTINCT conversation_subject FROM intercom__conversation_enhanced LIMIT 50
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-100/attempt-01/sql/S22.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-100/attempt-01/sql/S22.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-100/attempt-01/results/S22.rows.jsonl)；完整：True；SHA256：`eba094d12bf79939de3773feeecd0e027b822818d2fdd87e6cdfa96b044724cd`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "intercom__conversation_enhanced", "kind": "base", "block": null, "base_tables": ["intercom__conversation_enhanced"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |


## S23

类别 `data`；来源 `query_db`；调用 `82336e19d96849b9a3cf90f11474f59f`；状态 `success`。

```sql
SELECT DISTINCT conversation_rating_remark FROM intercom__conversation_metrics LIMIT 50
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-100/attempt-01/sql/S23.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-100/attempt-01/sql/S23.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-100/attempt-01/results/S23.rows.jsonl)；完整：True；SHA256：`553f02fae288077bb3fcced67a9b9465d59f09ae263281e77ad598a5c5e7164c`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "intercom__conversation_metrics", "kind": "base", "block": null, "base_tables": ["intercom__conversation_metrics"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |


## S24

类别 `data`；来源 `query_db`；调用 `4d9c96876c144cadbcded94d018afe4f`；状态 `failed`。

```sql
SELECT conversation_id, conversation_created_at, conversation_rating, conversation_rating_remark, count_reopens, time_to_last_close_minutes, first_close_at, last_close_at FROM intercom__conversation_metrics LIMIT 10
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-100/attempt-01/sql/S24.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-100/attempt-01/sql/S24.parameters.json)。

错误：`OperationalError('no such column: first_close_at')`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "intercom__conversation_metrics", "kind": "base", "block": null, "base_tables": ["intercom__conversation_metrics"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |


未解析列血缘：[{"block": "B1", "column": "first_close_at", "reason": "ambiguous_or_missing_source"}, {"block": "B1", "column": "last_close_at", "reason": "ambiguous_or_missing_source"}]

## S25

类别 `data`；来源 `query_db`；调用 `9ff6b4519f924f5d8bf44ac605d5c3e7`；状态 `success`。

```sql
SELECT conversation_id, conversation_created_at, conversation_last_updated_at, conversation_type, conversation_rating, count_reopens, count_total_parts, sla_name, sla_status, time_to_first_close_minutes, time_to_last_close_minutes FROM intercom__conversation_metrics LIMIT 5
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-100/attempt-01/sql/S25.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-100/attempt-01/sql/S25.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-100/attempt-01/results/S25.rows.jsonl)；完整：True；SHA256：`7362f3dce104d8a2dca02712b8de8e71e357a525a0e6a4a7cc7ea112bd17da3a`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "intercom__conversation_metrics", "kind": "base", "block": null, "base_tables": ["intercom__conversation_metrics"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |


## S26

类别 `data`；来源 `query_db`；调用 `1ba82b2a266d41b3a91279adc1ba0f1a`；状态 `success`。

```sql
SELECT COUNT(*) AS n, COUNT(DISTINCT conversation_id) AS uniq FROM intercom__conversation_metrics
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-100/attempt-01/sql/S26.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-100/attempt-01/sql/S26.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-100/attempt-01/results/S26.rows.jsonl)；完整：True；SHA256：`a33b5e98afcaa35683f077b9a6ea81b3e47f4af2fffed137cf8e33d6d6016199`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "intercom__conversation_metrics", "kind": "base", "block": null, "base_tables": ["intercom__conversation_metrics"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |
| B1 | COUNT(DISTINCT conversation_id) | [{"table": "intercom__conversation_metrics", "column": "conversation_id"}] | [] | False |


## S27

类别 `data`；来源 `python`；调用 `4a070099321d422da1db54175bd2fa48`；状态 `success`。

```sql
SELECT company_id, company_name, all_company_tags FROM intercom__company_enhanced
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-100/attempt-01/sql/S27.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-100/attempt-01/sql/S27.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-100/attempt-01/results/S27.rows.jsonl)；完整：True；SHA256：`3d7916e1a3810412095b6c71a7fe0d329c0a7026e0ec42ea0cea14d8cc5b5c0f`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "intercom__company_enhanced", "kind": "base", "block": null, "base_tables": ["intercom__company_enhanced"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |


## S28

类别 `data`；来源 `python`；调用 `4a070099321d422da1db54175bd2fa48`；状态 `success`。

```sql
SELECT conversation_id, all_contact_company_names, conversation_created_at, conversation_subject FROM intercom__conversation_enhanced
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-100/attempt-01/sql/S28.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-100/attempt-01/sql/S28.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-100/attempt-01/results/S28.rows.jsonl)；完整：True；SHA256：`def6d7fcb4e35a2096444280eb5664e0df4afb2dc6bd730eaff564c3352d93e1`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "intercom__conversation_enhanced", "kind": "base", "block": null, "base_tables": ["intercom__conversation_enhanced"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |


## S29

类别 `data`；来源 `python`；调用 `4a070099321d422da1db54175bd2fa48`；状态 `success`。

```sql
SELECT conversation_id, conversation_rating_remark FROM intercom__conversation_metrics
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-100/attempt-01/sql/S29.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-100/attempt-01/sql/S29.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-100/attempt-01/results/S29.rows.jsonl)；完整：True；SHA256：`145e00d7d893944e9894b3098327a9cda79e5f6cabe173be2a0c2ba589091e27`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "intercom__conversation_metrics", "kind": "base", "block": null, "base_tables": ["intercom__conversation_metrics"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |


## S30

类别 `data`；来源 `python`；调用 `9c7cf7e69a95423bafaa95081501ef01`；状态 `success`。

```sql
SELECT DISTINCT all_contact_company_names FROM intercom__conversation_enhanced
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-100/attempt-01/sql/S30.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-100/attempt-01/sql/S30.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-100/attempt-01/results/S30.rows.jsonl)；完整：True；SHA256：`da7001d8b748cdb15d11bf59f97f5ffe52339f0f03f4c748c64d8d855f665290`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "intercom__conversation_enhanced", "kind": "base", "block": null, "base_tables": ["intercom__conversation_enhanced"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |


## S31

类别 `data`；来源 `python`；调用 `9c7cf7e69a95423bafaa95081501ef01`；状态 `success`。

```sql
SELECT company_name FROM intercom__company_enhanced
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-100/attempt-01/sql/S31.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-100/attempt-01/sql/S31.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-100/attempt-01/results/S31.rows.jsonl)；完整：True；SHA256：`7ee571170210946183bc46ff69c23307d513d57f0aae11d3caa3b2ddab599097`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "intercom__company_enhanced", "kind": "base", "block": null, "base_tables": ["intercom__company_enhanced"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |


## S32

类别 `data`；来源 `query_db`；调用 `b5637a457ccb4a999382bfca33039509`；状态 `success`。

```sql
SELECT company_name, COUNT(*) AS n, COUNT(DISTINCT company_id) AS n_ids FROM intercom__company_enhanced GROUP BY company_name ORDER BY n DESC LIMIT 10
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-100/attempt-01/sql/S32.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-100/attempt-01/sql/S32.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-100/attempt-01/results/S32.rows.jsonl)；完整：True；SHA256：`5bbacd97a734d955ac343f113e145cde8084d676ecf53b235e57308142cf1d28`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "intercom__company_enhanced", "kind": "base", "block": null, "base_tables": ["intercom__company_enhanced"]}] | [] | ["company_name"] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |
| B1 | COUNT(DISTINCT company_id) | [{"table": "intercom__company_enhanced", "column": "company_id"}] | [] | False |


## S33

类别 `data`；来源 `query_db`；调用 `0975fd6c70094513abc16fccb49e731a`；状态 `success`。

```sql
SELECT company_name, COUNT(DISTINCT renewal_window) AS n_windows, GROUP_CONCAT(DISTINCT renewal_window) AS windows FROM (
  SELECT company_id, company_name, CASE 
    WHEN instr(all_company_tags, 'renewal_window=') > 0 THEN 
      substr(all_company_tags, instr(all_company_tags, 'renewal_window=') + 15, 
        CASE WHEN instr(substr(all_company_tags, instr(all_company_tags, 'renewal_window=') + 15), '|') > 0 
             THEN instr(substr(all_company_tags, instr(all_company_tags, 'renewal_window=') + 15), '|') - 1
             ELSE 100 END)
    ELSE NULL END AS renewal_window
  FROM intercom__company_enhanced
) GROUP BY company_name HAVING n_windows > 1 LIMIT 5
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-100/attempt-01/sql/S33.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-100/attempt-01/sql/S33.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-100/attempt-01/results/S33.rows.jsonl)；完整：True；SHA256：`b69fa2b645ddff3049cca35cca3117477a4ea8ecd59411403853e2b7e46a44c4`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "intercom__company_enhanced", "kind": "base", "block": null, "base_tables": ["intercom__company_enhanced"]}] | [] | [] |
| B2 | [{"alias": "", "kind": "derived", "block": "B1", "base_tables": ["intercom__company_enhanced"]}] | [] | ["company_name"] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B2 | COUNT(DISTINCT renewal_window) | [{"table": "intercom__company_enhanced", "column": "all_company_tags"}, {"table": "intercom__company_enhanced", "column": "all_company_tags"}, {"table": "intercom__company_enhanced", "column": "all_company_tags"}, {"table": "intercom__company_enhanced", "column": "all_company_tags"}, {"table": "intercom__company_enhanced", "column": "all_company_tags"}, {"table": "intercom__company_enhanced", "column": "all_company_tags"}, {"table": "intercom__company_enhanced", "column": "all_company_tags"}] | [] | False |
| B2 | GROUP_CONCAT(DISTINCT renewal_window) | [{"table": "intercom__company_enhanced", "column": "all_company_tags"}, {"table": "intercom__company_enhanced", "column": "all_company_tags"}, {"table": "intercom__company_enhanced", "column": "all_company_tags"}, {"table": "intercom__company_enhanced", "column": "all_company_tags"}, {"table": "intercom__company_enhanced", "column": "all_company_tags"}, {"table": "intercom__company_enhanced", "column": "all_company_tags"}, {"table": "intercom__company_enhanced", "column": "all_company_tags"}] | [] | False |


## S34

类别 `data`；来源 `python`；调用 `4d193ad0e6a44a12ba5c7051ca04a6df`；状态 `success`。

```sql
SELECT company_id, company_name, all_company_tags FROM intercom__company_enhanced
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-100/attempt-01/sql/S34.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-100/attempt-01/sql/S34.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-100/attempt-01/results/S34.rows.jsonl)；完整：True；SHA256：`3d7916e1a3810412095b6c71a7fe0d329c0a7026e0ec42ea0cea14d8cc5b5c0f`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "intercom__company_enhanced", "kind": "base", "block": null, "base_tables": ["intercom__company_enhanced"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |


## S35

类别 `data`；来源 `python`；调用 `4d193ad0e6a44a12ba5c7051ca04a6df`；状态 `success`。

```sql
SELECT MIN(conversation_created_at) AS mn, MAX(conversation_created_at) AS mx, COUNT(*) AS n FROM intercom__conversation_enhanced
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-100/attempt-01/sql/S35.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-100/attempt-01/sql/S35.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-100/attempt-01/results/S35.rows.jsonl)；完整：True；SHA256：`53e93f68ab91097c0e538a22221e964720dd67295efb1ff3f3b6f35dc08b6166`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "intercom__conversation_enhanced", "kind": "base", "block": null, "base_tables": ["intercom__conversation_enhanced"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | MIN(conversation_created_at) | [{"table": "intercom__conversation_enhanced", "column": "conversation_created_at"}] | [] | False |
| B1 | MAX(conversation_created_at) | [{"table": "intercom__conversation_enhanced", "column": "conversation_created_at"}] | [] | False |
| B1 | COUNT(*) | [] | [] | True |


## S36

类别 `data`；来源 `python`；调用 `c5e810102bcc4a708bf3728c63880e48`；状态 `success`。

```sql
SELECT conversation_id, all_contact_company_names, conversation_created_at, all_conversation_tags FROM intercom__conversation_enhanced
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-100/attempt-01/sql/S36.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-100/attempt-01/sql/S36.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-100/attempt-01/results/S36.rows.jsonl)；完整：True；SHA256：`e332a4f4badcda155802b9d108a690ef0793dce2c7369a0d0b83b6e1dcd35f14`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "intercom__conversation_enhanced", "kind": "base", "block": null, "base_tables": ["intercom__conversation_enhanced"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |


## S37

类别 `data`；来源 `python`；调用 `c5e810102bcc4a708bf3728c63880e48`；状态 `success`。

```sql
SELECT company_id, company_name, all_company_tags FROM intercom__company_enhanced
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-100/attempt-01/sql/S37.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-100/attempt-01/sql/S37.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-100/attempt-01/results/S37.rows.jsonl)；完整：True；SHA256：`3d7916e1a3810412095b6c71a7fe0d329c0a7026e0ec42ea0cea14d8cc5b5c0f`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "intercom__company_enhanced", "kind": "base", "block": null, "base_tables": ["intercom__company_enhanced"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |


## S38

类别 `data`；来源 `python`；调用 `3d4753c1aa894c44ba8bf8d8c19a9581`；状态 `success`。

```sql

    SELECT conversation_id, all_contact_company_names, conversation_created_at, 
           all_conversation_tags, conversation_subject
    FROM intercom__conversation_enhanced

```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-100/attempt-01/sql/S38.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-100/attempt-01/sql/S38.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-100/attempt-01/results/S38.rows.jsonl)；完整：True；SHA256：`e2ad22595c3855c5bbfafb7ac692ca18a5768fe82b30bfdc1e74baf081a0e833`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "intercom__conversation_enhanced", "kind": "base", "block": null, "base_tables": ["intercom__conversation_enhanced"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |


## S39

类别 `data`；来源 `python`；调用 `3d4753c1aa894c44ba8bf8d8c19a9581`；状态 `success`。

```sql

    SELECT conversation_id, count_reopens, time_to_last_close_minutes,
           time_to_first_close_minutes, conversation_created_at, conversation_last_updated_at
    FROM intercom__conversation_metrics

```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-100/attempt-01/sql/S39.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-100/attempt-01/sql/S39.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-100/attempt-01/results/S39.rows.jsonl)；完整：True；SHA256：`0107ffaf5f532b4db1e9b5977c57707d41461a5fc609fd7e79100223a5f34edd`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "intercom__conversation_metrics", "kind": "base", "block": null, "base_tables": ["intercom__conversation_metrics"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |


## S40

类别 `data`；来源 `python`；调用 `3d4753c1aa894c44ba8bf8d8c19a9581`；状态 `success`。

```sql
SELECT company_id, company_name, all_company_tags FROM intercom__company_enhanced
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-100/attempt-01/sql/S40.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-100/attempt-01/sql/S40.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-100/attempt-01/results/S40.rows.jsonl)；完整：True；SHA256：`3d7916e1a3810412095b6c71a7fe0d329c0a7026e0ec42ea0cea14d8cc5b5c0f`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "intercom__company_enhanced", "kind": "base", "block": null, "base_tables": ["intercom__company_enhanced"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |


## S41

类别 `data`；来源 `python`；调用 `879953b40f16455eaa6d705c9c35eff5`；状态 `success`。

```sql
SELECT conversation_created_at FROM intercom__conversation_enhanced
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-100/attempt-01/sql/S41.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-100/attempt-01/sql/S41.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-100/attempt-01/results/S41.rows.jsonl)；完整：True；SHA256：`8ad85268a2511aa46d6239a51f04c9268a5359572de2d48d88ee37b2dbeae429`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "intercom__conversation_enhanced", "kind": "base", "block": null, "base_tables": ["intercom__conversation_enhanced"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |


## S42

类别 `data`；来源 `python`；调用 `3ecf2e2bdc534b2497a8992636dee88a`；状态 `success`。

```sql

    SELECT conversation_id, all_contact_company_names, conversation_created_at, all_conversation_tags
    FROM intercom__conversation_enhanced

```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-100/attempt-01/sql/S42.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-100/attempt-01/sql/S42.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-100/attempt-01/results/S42.rows.jsonl)；完整：True；SHA256：`e332a4f4badcda155802b9d108a690ef0793dce2c7369a0d0b83b6e1dcd35f14`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "intercom__conversation_enhanced", "kind": "base", "block": null, "base_tables": ["intercom__conversation_enhanced"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |


## S43

类别 `data`；来源 `python`；调用 `418f64cd5a644896bbfbd1e6d8f2856f`；状态 `success`。

```sql
SELECT company_id, company_name, all_company_tags FROM intercom__company_enhanced
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-100/attempt-01/sql/S43.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-100/attempt-01/sql/S43.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-100/attempt-01/results/S43.rows.jsonl)；完整：True；SHA256：`3d7916e1a3810412095b6c71a7fe0d329c0a7026e0ec42ea0cea14d8cc5b5c0f`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "intercom__company_enhanced", "kind": "base", "block": null, "base_tables": ["intercom__company_enhanced"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |


## S44

类别 `data`；来源 `python`；调用 `418f64cd5a644896bbfbd1e6d8f2856f`；状态 `success`。

```sql

    SELECT conversation_id, all_contact_company_names, conversation_created_at, all_conversation_tags
    FROM intercom__conversation_enhanced

```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-100/attempt-01/sql/S44.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-100/attempt-01/sql/S44.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-100/attempt-01/results/S44.rows.jsonl)；完整：True；SHA256：`e332a4f4badcda155802b9d108a690ef0793dce2c7369a0d0b83b6e1dcd35f14`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "intercom__conversation_enhanced", "kind": "base", "block": null, "base_tables": ["intercom__conversation_enhanced"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |


## S45

类别 `data`；来源 `python`；调用 `3059147ff4e746eda6d8bd1c813d7ff0`；状态 `success`。

```sql
SELECT company_id, company_name, all_company_tags FROM intercom__company_enhanced
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-100/attempt-01/sql/S45.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-100/attempt-01/sql/S45.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-100/attempt-01/results/S45.rows.jsonl)；完整：True；SHA256：`3d7916e1a3810412095b6c71a7fe0d329c0a7026e0ec42ea0cea14d8cc5b5c0f`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "intercom__company_enhanced", "kind": "base", "block": null, "base_tables": ["intercom__company_enhanced"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |


## S46

类别 `data`；来源 `python`；调用 `3059147ff4e746eda6d8bd1c813d7ff0`；状态 `success`。

```sql
SELECT * FROM intercom__company_metrics
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-100/attempt-01/sql/S46.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-100/attempt-01/sql/S46.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-100/attempt-01/results/S46.rows.jsonl)；完整：True；SHA256：`b76c02be193d729a0c1c0fbaff2eb086166d909b38fccdcc6eb71f1ab6fbe04b`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "intercom__company_metrics", "kind": "base", "block": null, "base_tables": ["intercom__company_metrics"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |


## S47

类别 `data`；来源 `python`；调用 `6333deca8433428eb13cf017f81923a7`；状态 `success`。

```sql
SELECT company_id, company_name, created_at, all_company_tags FROM intercom__company_enhanced
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-100/attempt-01/sql/S47.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-100/attempt-01/sql/S47.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-100/attempt-01/results/S47.rows.jsonl)；完整：True；SHA256：`ee9c550d7854b740d96f3cd9c37fcdde5fddf2c5c0f256ec48ca27dd45fdb2d3`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "intercom__company_enhanced", "kind": "base", "block": null, "base_tables": ["intercom__company_enhanced"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |


## S48

类别 `data`；来源 `python`；调用 `6333deca8433428eb13cf017f81923a7`；状态 `success`。

```sql
SELECT * FROM intercom__company_metrics
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-100/attempt-01/sql/S48.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-100/attempt-01/sql/S48.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-100/attempt-01/results/S48.rows.jsonl)；完整：True；SHA256：`b76c02be193d729a0c1c0fbaff2eb086166d909b38fccdcc6eb71f1ab6fbe04b`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "intercom__company_metrics", "kind": "base", "block": null, "base_tables": ["intercom__company_metrics"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |


## S49

类别 `data`；来源 `python`；调用 `1c0370f5019a4ee5be8948a0d00e5ab4`；状态 `success`。

```sql
SELECT company_id, company_name, all_company_tags FROM intercom__company_enhanced
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-100/attempt-01/sql/S49.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-100/attempt-01/sql/S49.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-100/attempt-01/results/S49.rows.jsonl)；完整：True；SHA256：`3d7916e1a3810412095b6c71a7fe0d329c0a7026e0ec42ea0cea14d8cc5b5c0f`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "intercom__company_enhanced", "kind": "base", "block": null, "base_tables": ["intercom__company_enhanced"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |


## S50

类别 `data`；来源 `python`；调用 `1c0370f5019a4ee5be8948a0d00e5ab4`；状态 `success`。

```sql

    SELECT conversation_id, all_contact_company_names, conversation_created_at, all_conversation_tags
    FROM intercom__conversation_enhanced

```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-100/attempt-01/sql/S50.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-100/attempt-01/sql/S50.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-100/attempt-01/results/S50.rows.jsonl)；完整：True；SHA256：`e332a4f4badcda155802b9d108a690ef0793dce2c7369a0d0b83b6e1dcd35f14`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "intercom__conversation_enhanced", "kind": "base", "block": null, "base_tables": ["intercom__conversation_enhanced"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |


## S51

类别 `data`；来源 `python`；调用 `1c0370f5019a4ee5be8948a0d00e5ab4`；状态 `success`。

```sql

    SELECT conversation_id, count_reopens, time_to_first_close_minutes, time_to_last_close_minutes, 
           conversation_created_at, conversation_last_updated_at
    FROM intercom__conversation_metrics

```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-100/attempt-01/sql/S51.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-100/attempt-01/sql/S51.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-100/attempt-01/results/S51.rows.jsonl)；完整：True；SHA256：`76c604284cf2dadca1a2552236443f9cf46f6f87927411026ffb3e371e4e560f`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "intercom__conversation_metrics", "kind": "base", "block": null, "base_tables": ["intercom__conversation_metrics"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |


## S52

类别 `data`；来源 `python`；调用 `1c0370f5019a4ee5be8948a0d00e5ab4`；状态 `success`。

```sql
SELECT company_id, created_at FROM intercom__company_enhanced
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-100/attempt-01/sql/S52.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-100/attempt-01/sql/S52.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-100/attempt-01/results/S52.rows.jsonl)；完整：True；SHA256：`82c610d890ae851223b36ec06bd58d54db01238f014539d92dc1dcd569054cea`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "intercom__company_enhanced", "kind": "base", "block": null, "base_tables": ["intercom__company_enhanced"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |


## S53

类别 `data`；来源 `python`；调用 `58d87a89aee8455883fc325686438159`；状态 `success`。

```sql
SELECT company_id, company_name, all_company_tags FROM intercom__company_enhanced
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-100/attempt-01/sql/S53.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-100/attempt-01/sql/S53.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-100/attempt-01/results/S53.rows.jsonl)；完整：True；SHA256：`3d7916e1a3810412095b6c71a7fe0d329c0a7026e0ec42ea0cea14d8cc5b5c0f`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "intercom__company_enhanced", "kind": "base", "block": null, "base_tables": ["intercom__company_enhanced"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |


## S54

类别 `data`；来源 `python`；调用 `d594c10f929d4c97be3200cff712d468`；状态 `success`。

```sql
SELECT company_id, company_name, all_company_tags FROM intercom__company_enhanced
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-100/attempt-01/sql/S54.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-100/attempt-01/sql/S54.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-100/attempt-01/results/S54.rows.jsonl)；完整：True；SHA256：`3d7916e1a3810412095b6c71a7fe0d329c0a7026e0ec42ea0cea14d8cc5b5c0f`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "intercom__company_enhanced", "kind": "base", "block": null, "base_tables": ["intercom__company_enhanced"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |


## S55

类别 `data`；来源 `python`；调用 `d594c10f929d4c97be3200cff712d468`；状态 `success`。

```sql

    SELECT conversation_id, all_contact_company_names, conversation_created_at, all_conversation_tags
    FROM intercom__conversation_enhanced

```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-100/attempt-01/sql/S55.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-100/attempt-01/sql/S55.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-100/attempt-01/results/S55.rows.jsonl)；完整：True；SHA256：`e332a4f4badcda155802b9d108a690ef0793dce2c7369a0d0b83b6e1dcd35f14`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "intercom__conversation_enhanced", "kind": "base", "block": null, "base_tables": ["intercom__conversation_enhanced"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |


## S56

类别 `data`；来源 `python`；调用 `217474e446be4d36a2bda00e7a501dca`；状态 `success`。

```sql
SELECT company_id, company_name, created_at, all_company_tags FROM intercom__company_enhanced
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-100/attempt-01/sql/S56.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-100/attempt-01/sql/S56.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-100/attempt-01/results/S56.rows.jsonl)；完整：True；SHA256：`ee9c550d7854b740d96f3cd9c37fcdde5fddf2c5c0f256ec48ca27dd45fdb2d3`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "intercom__company_enhanced", "kind": "base", "block": null, "base_tables": ["intercom__company_enhanced"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |


## S57

类别 `data`；来源 `python`；调用 `217474e446be4d36a2bda00e7a501dca`；状态 `success`。

```sql
SELECT * FROM intercom__company_metrics
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-100/attempt-01/sql/S57.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-100/attempt-01/sql/S57.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-100/attempt-01/results/S57.rows.jsonl)；完整：True；SHA256：`b76c02be193d729a0c1c0fbaff2eb086166d909b38fccdcc6eb71f1ab6fbe04b`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "intercom__company_metrics", "kind": "base", "block": null, "base_tables": ["intercom__company_metrics"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |


## S58

类别 `data`；来源 `python`；调用 `5143697f0fb54802a5fc988d57cc418d`；状态 `success`。

```sql
SELECT company_id, company_name, created_at, company_age_days, all_company_tags FROM intercom__company_enhanced
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-100/attempt-01/sql/S58.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-100/attempt-01/sql/S58.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-100/attempt-01/results/S58.rows.jsonl)；完整：True；SHA256：`3dbff1f407baa96acf999ac00fa7519cbd1dc10ae867dd9076142f31ae782e67`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "intercom__company_enhanced", "kind": "base", "block": null, "base_tables": ["intercom__company_enhanced"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |


## S59

类别 `data`；来源 `python`；调用 `5143697f0fb54802a5fc988d57cc418d`；状态 `success`。

```sql
SELECT * FROM intercom__company_metrics
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-100/attempt-01/sql/S59.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-100/attempt-01/sql/S59.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-100/attempt-01/results/S59.rows.jsonl)；完整：True；SHA256：`b76c02be193d729a0c1c0fbaff2eb086166d909b38fccdcc6eb71f1ab6fbe04b`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "intercom__company_metrics", "kind": "base", "block": null, "base_tables": ["intercom__company_metrics"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |


## S60

类别 `data`；来源 `python`；调用 `5143697f0fb54802a5fc988d57cc418d`；状态 `success`。

```sql
SELECT conversation_id, all_contact_company_names, conversation_created_at, all_conversation_tags FROM intercom__conversation_enhanced
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-100/attempt-01/sql/S60.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-100/attempt-01/sql/S60.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-100/attempt-01/results/S60.rows.jsonl)；完整：True；SHA256：`e332a4f4badcda155802b9d108a690ef0793dce2c7369a0d0b83b6e1dcd35f14`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "intercom__conversation_enhanced", "kind": "base", "block": null, "base_tables": ["intercom__conversation_enhanced"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |


## S61

类别 `data`；来源 `python`；调用 `5143697f0fb54802a5fc988d57cc418d`；状态 `success`。

```sql
SELECT conversation_id, count_reopens, time_to_first_close_minutes, time_to_last_close_minutes FROM intercom__conversation_metrics
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-100/attempt-01/sql/S61.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-100/attempt-01/sql/S61.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-100/attempt-01/results/S61.rows.jsonl)；完整：True；SHA256：`b019ae8cf284de44e1b1506c6d87a1a36393465e34426ac6ee20edf82c9bdb48`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "intercom__conversation_metrics", "kind": "base", "block": null, "base_tables": ["intercom__conversation_metrics"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |


## S62

类别 `data`；来源 `python`；调用 `ac6e3861bac04325b3ff4e8d49ae02c4`；状态 `success`。

```sql
SELECT company_id, company_name, all_company_tags FROM intercom__company_enhanced
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-100/attempt-01/sql/S62.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-100/attempt-01/sql/S62.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-100/attempt-01/results/S62.rows.jsonl)；完整：True；SHA256：`3d7916e1a3810412095b6c71a7fe0d329c0a7026e0ec42ea0cea14d8cc5b5c0f`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "intercom__company_enhanced", "kind": "base", "block": null, "base_tables": ["intercom__company_enhanced"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |


## S63

类别 `data`；来源 `python`；调用 `ac6e3861bac04325b3ff4e8d49ae02c4`；状态 `failed`。

```sql
SELECT conversation_id, all_contact_company_names, conversation_created_at, all_conversation_tags, conversation_state, sla_name, sla_status, conversation_rating FROM intercom__conversation_metrics
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-100/attempt-01/sql/S63.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-100/attempt-01/sql/S63.parameters.json)。

错误：`OperationalError('no such column: all_contact_company_names')`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "intercom__conversation_metrics", "kind": "base", "block": null, "base_tables": ["intercom__conversation_metrics"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |


未解析列血缘：[{"block": "B1", "column": "all_contact_company_names", "reason": "ambiguous_or_missing_source"}, {"block": "B1", "column": "all_conversation_tags", "reason": "ambiguous_or_missing_source"}]

## S64

类别 `data`；来源 `python`；调用 `d6a9d4204b8c4d7d8996c546812ccdc8`；状态 `success`。

```sql
SELECT company_id, company_name, all_company_tags FROM intercom__company_enhanced
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-100/attempt-01/sql/S64.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-100/attempt-01/sql/S64.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-100/attempt-01/results/S64.rows.jsonl)；完整：True；SHA256：`3d7916e1a3810412095b6c71a7fe0d329c0a7026e0ec42ea0cea14d8cc5b5c0f`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "intercom__company_enhanced", "kind": "base", "block": null, "base_tables": ["intercom__company_enhanced"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |


## S65

类别 `data`；来源 `python`；调用 `22406832ffc24050885118cc8b2ea3a9`；状态 `success`。

```sql
SELECT company_id, company_name, all_company_tags FROM intercom__company_enhanced
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-100/attempt-01/sql/S65.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-100/attempt-01/sql/S65.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-100/attempt-01/results/S65.rows.jsonl)；完整：True；SHA256：`3d7916e1a3810412095b6c71a7fe0d329c0a7026e0ec42ea0cea14d8cc5b5c0f`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "intercom__company_enhanced", "kind": "base", "block": null, "base_tables": ["intercom__company_enhanced"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |


## S66

类别 `data`；来源 `python`；调用 `22406832ffc24050885118cc8b2ea3a9`；状态 `success`。

```sql
SELECT DISTINCT all_contact_company_names FROM intercom__conversation_enhanced
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-100/attempt-01/sql/S66.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-100/attempt-01/sql/S66.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-100/attempt-01/results/S66.rows.jsonl)；完整：True；SHA256：`da7001d8b748cdb15d11bf59f97f5ffe52339f0f03f4c748c64d8d855f665290`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "intercom__conversation_enhanced", "kind": "base", "block": null, "base_tables": ["intercom__conversation_enhanced"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |


## S67

类别 `data`；来源 `python`；调用 `2d0b27f8c70348b8943a98b7bb52fe7a`；状态 `success`。

```sql
SELECT company_id, company_name, all_company_tags FROM intercom__company_enhanced
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-100/attempt-01/sql/S67.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-100/attempt-01/sql/S67.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-100/attempt-01/results/S67.rows.jsonl)；完整：True；SHA256：`3d7916e1a3810412095b6c71a7fe0d329c0a7026e0ec42ea0cea14d8cc5b5c0f`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "intercom__company_enhanced", "kind": "base", "block": null, "base_tables": ["intercom__company_enhanced"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |


## S68

类别 `data`；来源 `python`；调用 `3da3d40a6e8843fa96bdbdf48f3c296a`；状态 `success`。

```sql
SELECT company_id, company_name, all_company_tags FROM intercom__company_enhanced
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-100/attempt-01/sql/S68.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-100/attempt-01/sql/S68.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-100/attempt-01/results/S68.rows.jsonl)；完整：True；SHA256：`3d7916e1a3810412095b6c71a7fe0d329c0a7026e0ec42ea0cea14d8cc5b5c0f`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "intercom__company_enhanced", "kind": "base", "block": null, "base_tables": ["intercom__company_enhanced"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |


## S69

类别 `data`；来源 `python`；调用 `3da3d40a6e8843fa96bdbdf48f3c296a`；状态 `success`。

```sql
SELECT conversation_id, all_contact_company_names, conversation_created_at, all_conversation_tags FROM intercom__conversation_enhanced
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-100/attempt-01/sql/S69.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-100/attempt-01/sql/S69.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-100/attempt-01/results/S69.rows.jsonl)；完整：True；SHA256：`e332a4f4badcda155802b9d108a690ef0793dce2c7369a0d0b83b6e1dcd35f14`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "intercom__conversation_enhanced", "kind": "base", "block": null, "base_tables": ["intercom__conversation_enhanced"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |


## S70

类别 `data`；来源 `python`；调用 `3da3d40a6e8843fa96bdbdf48f3c296a`；状态 `success`。

```sql
SELECT conversation_id, count_reopens, time_to_first_close_minutes, time_to_last_close_minutes FROM intercom__conversation_metrics
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-100/attempt-01/sql/S70.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-100/attempt-01/sql/S70.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-100/attempt-01/results/S70.rows.jsonl)；完整：True；SHA256：`b019ae8cf284de44e1b1506c6d87a1a36393465e34426ac6ee20edf82c9bdb48`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "intercom__conversation_metrics", "kind": "base", "block": null, "base_tables": ["intercom__conversation_metrics"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |


## S71

类别 `data`；来源 `python`；调用 `39563e92dcd24046900232970d97d93a`；状态 `success`。

```sql
SELECT company_id, company_name, all_company_tags, company_age_days FROM intercom__company_enhanced
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-100/attempt-01/sql/S71.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-100/attempt-01/sql/S71.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-100/attempt-01/results/S71.rows.jsonl)；完整：True；SHA256：`dc4a9f96200718b50d93f38e9b3635f77697a0ce50aba4a4aedab033dd9ad2b9`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "intercom__company_enhanced", "kind": "base", "block": null, "base_tables": ["intercom__company_enhanced"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |


## S72

类别 `data`；来源 `python`；调用 `39563e92dcd24046900232970d97d93a`；状态 `success`。

```sql
SELECT * FROM intercom__company_metrics
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-100/attempt-01/sql/S72.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-100/attempt-01/sql/S72.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-100/attempt-01/results/S72.rows.jsonl)；完整：True；SHA256：`b76c02be193d729a0c1c0fbaff2eb086166d909b38fccdcc6eb71f1ab6fbe04b`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "intercom__company_metrics", "kind": "base", "block": null, "base_tables": ["intercom__company_metrics"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |


## S73

类别 `data`；来源 `python`；调用 `b8fa1472a4a245b38e9aec4aaa22ef06`；状态 `success`。

```sql
SELECT company_id, company_name, all_company_tags, company_age_days FROM intercom__company_enhanced
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-100/attempt-01/sql/S73.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-100/attempt-01/sql/S73.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-100/attempt-01/results/S73.rows.jsonl)；完整：True；SHA256：`dc4a9f96200718b50d93f38e9b3635f77697a0ce50aba4a4aedab033dd9ad2b9`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "intercom__company_enhanced", "kind": "base", "block": null, "base_tables": ["intercom__company_enhanced"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |


## S74

类别 `data`；来源 `python`；调用 `b8fa1472a4a245b38e9aec4aaa22ef06`；状态 `success`。

```sql
SELECT * FROM intercom__company_metrics
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-100/attempt-01/sql/S74.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-100/attempt-01/sql/S74.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-100/attempt-01/results/S74.rows.jsonl)；完整：True；SHA256：`b76c02be193d729a0c1c0fbaff2eb086166d909b38fccdcc6eb71f1ab6fbe04b`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "intercom__company_metrics", "kind": "base", "block": null, "base_tables": ["intercom__company_metrics"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |


## S75

类别 `data`；来源 `query_db`；调用 `1a18ddc3ade64bbf8207bd66a96b297c`；状态 `success`。

```sql
SELECT 
  SUM(CASE WHEN renewal_window='inside_90_days' THEN 1 ELSE 0 END) AS inside_90,
  SUM(CASE WHEN renewal_window='within_30_days_past' THEN 1 ELSE 0 END) AS past_30,
  SUM(CASE WHEN renewal_window='future_90_plus' THEN 1 ELSE 0 END) AS future_90
FROM (
  SELECT company_id, renewal_window FROM (
    SELECT company_id, all_company_tags,
      substr(all_company_tags, instr(all_company_tags, 'renewal_window=')+15, 
        instr(substr(all_company_tags, instr(all_company_tags, 'renewal_window=')+15), '|')-1) AS renewal_window
    FROM intercom__company_enhanced
  )
)
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-100/attempt-01/sql/S75.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-100/attempt-01/sql/S75.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-100/attempt-01/results/S75.rows.jsonl)；完整：True；SHA256：`9870c4f10307a6ac91606763f89a616bc45653f7d4082fa4204552dac80fa0c5`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "intercom__company_enhanced", "kind": "base", "block": null, "base_tables": ["intercom__company_enhanced"]}] | [] | [] |
| B2 | [{"alias": "", "kind": "derived", "block": "B1", "base_tables": ["intercom__company_enhanced"]}] | [] | [] |
| B3 | [{"alias": "", "kind": "derived", "block": "B2", "base_tables": ["intercom__company_enhanced"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B3 | SUM(CASE WHEN renewal_window = 'inside_90_days' THEN 1 ELSE 0 END) | [] | [{"table": "intercom__company_enhanced", "column": "all_company_tags"}, {"table": "intercom__company_enhanced", "column": "all_company_tags"}, {"table": "intercom__company_enhanced", "column": "all_company_tags"}, {"table": "intercom__company_enhanced", "column": "all_company_tags"}] | False |
| B3 | SUM(CASE WHEN renewal_window = 'within_30_days_past' THEN 1 ELSE 0 END) | [] | [{"table": "intercom__company_enhanced", "column": "all_company_tags"}, {"table": "intercom__company_enhanced", "column": "all_company_tags"}, {"table": "intercom__company_enhanced", "column": "all_company_tags"}, {"table": "intercom__company_enhanced", "column": "all_company_tags"}] | False |
| B3 | SUM(CASE WHEN renewal_window = 'future_90_plus' THEN 1 ELSE 0 END) | [] | [{"table": "intercom__company_enhanced", "column": "all_company_tags"}, {"table": "intercom__company_enhanced", "column": "all_company_tags"}, {"table": "intercom__company_enhanced", "column": "all_company_tags"}, {"table": "intercom__company_enhanced", "column": "all_company_tags"}] | False |


## S76

类别 `data`；来源 `query_db`；调用 `862b02d29c764422b807c64fd3e00ebb`；状态 `success`。

```sql
SELECT 
  substr(all_company_tags, instr(all_company_tags, 'expansion_signal=')+16,
    instr(substr(all_company_tags, instr(all_company_tags, 'expansion_signal=')+16), '|')-1) AS expansion_signal,
  substr(all_company_tags, instr(all_company_tags, 'sentiment_trend=')+16,
    instr(substr(all_company_tags, instr(all_company_tags, 'sentiment_trend=')+16), '|')-1) AS sentiment_trend,
  COUNT(*) AS n
FROM intercom__company_enhanced
WHERE all_company_tags LIKE '%expansion_signal=%'
GROUP BY 1, 2
ORDER BY 1, 2
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-100/attempt-01/sql/S76.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-100/attempt-01/sql/S76.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-100/attempt-01/results/S76.rows.jsonl)；完整：True；SHA256：`dbf08a37f630d45573f8c5ef2737727dc231b32df9df0e004d0ebafbef5f59c6`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "intercom__company_enhanced", "kind": "base", "block": null, "base_tables": ["intercom__company_enhanced"]}] | [] | ["SUBSTRING(all_company_tags, INSTR(all_company_tags, 'expansion_signal=') + 16, INSTR(SUBSTRING(all_company_tags, INSTR(all_company_tags, 'expansion_signal=') + 16), '\|') - 1)", "SUBSTRING(all_company_tags, INSTR(all_company_tags, 'sentiment_trend=') + 16, INSTR(SUBSTRING(all_company_tags, INSTR(all_company_tags, 'sentiment_trend=') + 16), '\|') - 1)"] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |


## S77

类别 `data`；来源 `query_db`；调用 `b0070cc073964a7ca2ce301623e48e8d`；状态 `success`。

```sql
SELECT 
  substr(all_company_tags, instr(all_company_tags, 'last_value_milestone=')+21,
    instr(substr(all_company_tags, instr(all_company_tags, 'last_value_milestone=')+21), '|')-1) AS milestone,
  substr(all_company_tags, instr(all_company_tags, 'expansion_signal=')+16,
    instr(substr(all_company_tags, instr(all_company_tags, 'expansion_signal=')+16), '|')-1) AS expansion_signal,
  COUNT(*) AS n
FROM intercom__company_enhanced
WHERE all_company_tags LIKE '%expansion_signal=%'
GROUP BY 1, 2
ORDER BY 1, 2
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-100/attempt-01/sql/S77.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-100/attempt-01/sql/S77.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-100/attempt-01/results/S77.rows.jsonl)；完整：True；SHA256：`75cf361a4d8c95b7172015f8a258c93c9d3623cdfaf219b22ffd7b83a95e85c7`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "intercom__company_enhanced", "kind": "base", "block": null, "base_tables": ["intercom__company_enhanced"]}] | [] | ["SUBSTRING(all_company_tags, INSTR(all_company_tags, 'last_value_milestone=') + 21, INSTR(SUBSTRING(all_company_tags, INSTR(all_company_tags, 'last_value_milestone=') + 21), '\|') - 1)", "SUBSTRING(all_company_tags, INSTR(all_company_tags, 'expansion_signal=') + 16, INSTR(SUBSTRING(all_company_tags, INSTR(all_company_tags, 'expansion_signal=') + 16), '\|') - 1)"] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |


## S78

类别 `data`；来源 `query_db`；调用 `bed25702d8d245ff9559edbf4209f082`；状态 `success`。

```sql
SELECT 
  substr(all_company_tags, instr(all_company_tags, 'education_focus=')+17,
    instr(substr(all_company_tags, instr(all_company_tags, 'education_focus=')+17), '|')-1) AS education_focus,
  substr(all_company_tags, instr(all_company_tags, 'expansion_signal=')+16,
    instr(substr(all_company_tags, instr(all_company_tags, 'expansion_signal=')+16), '|')-1) AS expansion_signal,
  COUNT(*) AS n
FROM intercom__company_enhanced
WHERE all_company_tags LIKE '%expansion_signal=%'
GROUP BY 1, 2
ORDER BY 1, 2
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-100/attempt-01/sql/S78.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-100/attempt-01/sql/S78.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-100/attempt-01/results/S78.rows.jsonl)；完整：True；SHA256：`ce2d362116734d3c94f2fe9825e8231ed444a2577785e9b1630dc7a4fc5ca74a`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "intercom__company_enhanced", "kind": "base", "block": null, "base_tables": ["intercom__company_enhanced"]}] | [] | ["SUBSTRING(all_company_tags, INSTR(all_company_tags, 'education_focus=') + 17, INSTR(SUBSTRING(all_company_tags, INSTR(all_company_tags, 'education_focus=') + 17), '\|') - 1)", "SUBSTRING(all_company_tags, INSTR(all_company_tags, 'expansion_signal=') + 16, INSTR(SUBSTRING(all_company_tags, INSTR(all_company_tags, 'expansion_signal=') + 16), '\|') - 1)"] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |

