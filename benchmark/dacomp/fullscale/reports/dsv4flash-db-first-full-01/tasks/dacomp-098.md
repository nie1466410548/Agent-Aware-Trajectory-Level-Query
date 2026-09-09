# dacomp-098

Evaluate the impact of a bot-led first response strategy on various stages of the sales fu…

运行：已提交。官方未评分。全部 SQL 尝试/成功 47/45；数据 SQL 44/42；Python 12 次。

完整原题：

Evaluate the impact of a bot-led first response strategy on various stages of the sales funnel. Using data from the mart layer on conversations (e.g., initiated_at, first_response_at, responder_type), leads (e.g., lead_source, industry, region), and conversions (e.g., demo_booked_at, trial_activated_at, paid_at), segment customers into two categories: those with a bot first response and those with a human first response. For the comparison, the definition of conversion rate is as follows: the percentage of customers who book a demo after starting a conversation, the percentage of customers who activate a trial after booking a demo, and the percentage of customers who ultimately pay after activating a trial. The definition of stage duration is the average time interval (in days) between first response and booking, booking and activation, and activation and payment. The analysis must also incorporate conversation content features (e.g., conversation_template_id, intent_label) to explain any observed differences. The conclusion should focus on identifying scenarios where the bot strategy is effective and scenarios where human intervention is more necessary.

| 表 | 行数 | 列数 |
| --- | --- | --- |
| intercom__company_enhanced | 2509 | 14 |
| intercom__company_metrics | 2509 | 25 |
| intercom__contact_enhanced | 2707 | 22 |
| intercom__conversation_enhanced | 6703 | 30 |
| intercom__conversation_metrics | 6703 | 40 |


实际路线（分析者依据 SQL/源码概括，不代表 Agent 自述）：SQL 探索与数据提取 → Python 业务准备和统计 → 报告

数据库大小：10,530,816 字节。

## 数据 SQL

| SQL | 状态 | 基础表 | Join 输入/类型 | GROUP BY | 聚合表达式 | 结果行数 | 数据库 ms |
| --- | --- | --- | --- | --- | --- | --- | --- |
| [S4/Q1](#s4) | success | ["intercom__conversation_enhanced"] | 0 / {} | [] | [] | 5 | 0.418 |
| [S5/Q2](#s5) | success | ["intercom__conversation_metrics"] | 0 / {} | [] | [] | 5 | 0.438 |
| [S6/Q3](#s6) | success | ["intercom__company_enhanced"] | 0 / {} | [] | [] | 5 | 0.344 |
| [S7/Q4](#s7) | success | ["intercom__company_metrics"] | 0 / {} | [] | [] | 5 | 0.412 |
| [S8/Q5](#s8) | success | ["intercom__contact_enhanced"] | 0 / {} | [] | [] | 5 | 0.372 |
| [S9/Q6](#s9) | success | ["intercom__conversation_enhanced"] | 0 / {} | ["conversation_initiated_type"] | ["COUNT(*)"] | 2 | 4.308 |
| [S10/Q7](#s10) | success | ["intercom__conversation_enhanced"] | 0 / {} | [] | ["COUNT(*)"] | 1 | 1.735 |
| [S11/Q8](#s11) | success | ["intercom__contact_enhanced"] | 0 / {} | [] | ["COUNT(*)"] | 1 | 0.745 |
| [S12/Q9](#s12) | success | ["intercom__company_enhanced"] | 0 / {} | [] | ["COUNT(*)"] | 1 | 0.537 |
| [S13/Q10](#s13) | success | ["intercom__conversation_metrics"] | 0 / {} | [] | ["COUNT(*)"] | 1 | 1.542 |
| [S14/Q11](#s14) | success | ["intercom__conversation_enhanced"] | 0 / {} | [] | [] | 1 | 2.434 |
| [S15/Q12](#s15) | success | ["intercom__conversation_enhanced"] | 0 / {} | [] | [] | 40 | 0.427 |
| [S16/Q13](#s16) | success | ["intercom__conversation_enhanced"] | 0 / {} | [] | [] | 10 | 2.616 |
| [S17/Q14](#s17) | success | ["intercom__company_enhanced"] | 0 / {} | [] | [] | 20 | 0.316 |
| [S18/Q15](#s18) | success | ["intercom__contact_enhanced"] | 0 / {} | [] | [] | 20 | 0.254 |
| [S19/Q16](#s19) | success | ["intercom__conversation_enhanced"] | 0 / {} | ["CASE WHEN INSTR(all_conversation_tags, 'stage:') > 0 THEN SUBSTRING(all_conversation_tags, INSTR(all_conversation_tags, 'stage:') + 6, CASE WHEN INSTR(SUBSTRING(all_conversation_tags, INSTR(all_conversation_tags, 'stage:') + 6), '\|') > 0 THEN INSTR(SUBSTRING(all_conversation_tags, INSTR(all_conversation_tags, 'stage:') + 6), '\|') - 1 ELSE LENGTH(SUBSTRING(all_conversation_tags, INSTR(all_conversation_tags, 'stage:') + 6)) END) END"] | ["COUNT(*)"] | 9 | 15.31 |
| [S20/Q17](#s20) | success | ["intercom__conversation_enhanced"] | 0 / {} | ["CASE WHEN INSTR(all_conversation_tags, 'intent:') > 0 THEN SUBSTRING(all_conversation_tags, INSTR(all_conversation_tags, 'intent:') + 7, CASE WHEN INSTR(SUBSTRING(all_conversation_tags, INSTR(all_conversation_tags, 'intent:') + 7), '\|') > 0 THEN INSTR(SUBSTRING(all_conversation_tags, INSTR(all_conversation_tags, 'intent:') + 7), '\|') - 1 ELSE LENGTH(SUBSTRING(all_conversation_tags, INSTR(all_conversation_tags, 'intent:') + 7)) END) END"] | ["COUNT(*)"] | 8 | 12.166 |
| [S21/Q18](#s21) | success | ["intercom__conversation_enhanced"] | 0 / {} | ["CASE WHEN INSTR(all_conversation_tags, 'topic:') > 0 THEN SUBSTRING(all_conversation_tags, INSTR(all_conversation_tags, 'topic:') + 6, CASE WHEN INSTR(SUBSTRING(all_conversation_tags, INSTR(all_conversation_tags, 'topic:') + 6), '\|') > 0 THEN INSTR(SUBSTRING(all_conversation_tags, INSTR(all_conversation_tags, 'topic:') + 6), '\|') - 1 ELSE LENGTH(SUBSTRING(all_conversation_tags, INSTR(all_conversation_tags, 'topic:') + 6)) END) END"] | ["COUNT(*)"] | 6 | 13.425 |
| [S22/Q19](#s22) | success | ["intercom__conversation_enhanced"] | 0 / {} | ["CASE WHEN INSTR(all_conversation_tags, 'region:') > 0 THEN SUBSTRING(all_conversation_tags, INSTR(all_conversation_tags, 'region:') + 7, CASE WHEN INSTR(SUBSTRING(all_conversation_tags, INSTR(all_conversation_tags, 'region:') + 7), '\|') > 0 THEN INSTR(SUBSTRING(all_conversation_tags, INSTR(all_conversation_tags, 'region:') + 7), '\|') - 1 ELSE LENGTH(SUBSTRING(all_conversation_tags, INSTR(all_conversation_tags, 'region:') + 7)) END) END"] | ["COUNT(*)"] | 5 | 16.658 |
| [S23/Q20](#s23) | success | ["intercom__conversation_enhanced"] | 0 / {} | [] | [] | 10 | 0.371 |
| [S24/Q21](#s24) | success | ["intercom__contact_enhanced"] | 0 / {} | [] | [] | 10 | 0.325 |
| [S25/Q22](#s25) | success | ["intercom__conversation_enhanced"] | 0 / {} | ["all_conversation_contacts"] | ["COUNT(*)"] | 20 | 4.969 |
| [S26/Q23](#s26) | success | ["intercom__conversation_enhanced"] | 0 / {} | [] | ["COUNT(DISTINCT all_conversation_contacts)"] | 1 | 5.283 |
| [S27/Q24](#s27) | success | ["intercom__conversation_enhanced"] | 0 / {} | ["all_conversation_contacts"] | ["COUNT(*)"] | 3 | 5.713 |
| [S28/Q25](#s28) | success | ["intercom__conversation_enhanced"] | 0 / {} | ["all_conversation_contacts"] | ["COUNT(*)", "COUNT(*)"] | 1 | 4.911 |
| [S29/Q26](#s29) | success | ["intercom__conversation_enhanced"] | 0 / {} | ["all_conversation_contacts"] | ["COUNT(*)", "COUNT(*)"] | 1 | 4.613 |
| [S30/Q27](#s30) | failed | ["intercom__conversation_enhanced", "intercom__conversation_metrics"] | 0 / {} | [] | [] | unknown | 未取得；调用总时长 0.178 ms |
| [S31/Q28](#s31) | failed | ["intercom__conversation_metrics"] | 0 / {} | [] | [] | unknown | 未取得；调用总时长 0.16 ms |
| [S32/Q29](#s32) | success | ["intercom__conversation_enhanced", "intercom__conversation_metrics"] | 2 / {'INNER': 1} | [] | [] | 3 | 9.595 |
| [S33/Q30](#s33) | success | ["intercom__conversation_enhanced"] | 0 / {} | ["CASE WHEN INSTR(all_conversation_tags, 'path:') > 0 THEN SUBSTRING(all_conversation_tags, INSTR(all_conversation_tags, 'path:') + 5, CASE WHEN INSTR(SUBSTRING(all_conversation_tags, INSTR(all_conversation_tags, 'path:') + 5), '\|') > 0 THEN INSTR(SUBSTRING(all_conversation_tags, INSTR(all_conversation_tags, 'path:') + 5), '\|') - 1 ELSE LENGTH(SUBSTRING(all_conversation_tags, INSTR(all_conversation_tags, 'path:') + 5)) END) END", "CASE WHEN INSTR(all_conversation_tags, 'lifecycle:') > 0 THEN SUBSTRING(all_conversation_tags, INSTR(all_conversation_tags, 'lifecycle:') + 10, CASE WHEN INSTR(SUBSTRING(all_conversation_tags, INSTR(all_conversation_tags, 'lifecycle:') + 10), '\|') > 0 THEN INSTR(SUBSTRING(all_conversation_tags, INSTR(all_conversation_tags, 'lifecycle:') + 10), '\|') - 1 ELSE LENGTH(SUBSTRING(all_conversation_tags, INSTR(all_conversation_tags, 'lifecycle:') + 10)) END) END"] | ["COUNT(*)"] | 14 | 27.693 |
| [S34/Q31](#s34) | success | ["intercom__conversation_enhanced"] | 0 / {} | ["CASE WHEN INSTR(all_conversation_tags, 'segment:') > 0 THEN SUBSTRING(all_conversation_tags, INSTR(all_conversation_tags, 'segment:') + 8, CASE WHEN INSTR(SUBSTRING(all_conversation_tags, INSTR(all_conversation_tags, 'segment:') + 8), '\|') > 0 THEN INSTR(SUBSTRING(all_conversation_tags, INSTR(all_conversation_tags, 'segment:') + 8), '\|') - 1 ELSE LENGTH(SUBSTRING(all_conversation_tags, INSTR(all_conversation_tags, 'segment:') + 8)) END) END"] | ["COUNT(*)"] | 4 | 14.87 |
| [S35/Q32](#s35) | success | ["intercom__conversation_enhanced"] | 0 / {} | ["conversation_initiated_type", "CASE WHEN INSTR(all_conversation_tags, 'path:') > 0 THEN SUBSTRING(all_conversation_tags, INSTR(all_conversation_tags, 'path:') + 5, CASE WHEN INSTR(SUBSTRING(all_conversation_tags, INSTR(all_conversation_tags, 'path:') + 5), '\|') > 0 THEN INSTR(SUBSTRING(all_conversation_tags, INSTR(all_conversation_tags, 'path:') + 5), '\|') - 1 ELSE LENGTH(SUBSTRING(all_conversation_tags, INSTR(all_conversation_tags, 'path:') + 5)) END) END"] | ["COUNT(*)"] | 2 | 11.264 |
| [S36/Q33](#s36) | success | ["intercom__conversation_enhanced"] | 0 / {} | ["CASE WHEN INSTR(all_conversation_tags, 'lifecycle:') > 0 THEN SUBSTRING(all_conversation_tags, INSTR(all_conversation_tags, 'lifecycle:') + 10, CASE WHEN INSTR(SUBSTRING(all_conversation_tags, INSTR(all_conversation_tags, 'lifecycle:') + 10), '\|') > 0 THEN INSTR(SUBSTRING(all_conversation_tags, INSTR(all_conversation_tags, 'lifecycle:') + 10), '\|') - 1 ELSE LENGTH(SUBSTRING(all_conversation_tags, INSTR(all_conversation_tags, 'lifecycle:') + 10)) END) END"] | ["COUNT(*)"] | 7 | 19.316 |
| [S37/Q34](#s37) | success | ["intercom__conversation_enhanced", "intercom__conversation_metrics"] | 2 / {'INNER': 1} | ["contact_id"] | ["MIN(CASE WHEN stage_rank >= 1 AND stage_rank < 99 THEN stage_rank END)", "MAX(CASE WHEN stage_rank >= 1 AND stage_rank < 99 THEN stage_rank END)", "MIN(CASE WHEN stage_rank = 99 THEN 1 ELSE 0 END)", "COUNT(*)"] | 15 | 14.233 |
| [S38/Q35](#s38) | success | ["intercom__conversation_enhanced", "intercom__conversation_metrics"] | 2 / {'INNER': 1, 'LEFT': 1} | ["contact_id"] | ["MAX(CASE WHEN stage_rank >= 1 AND stage_rank < 99 THEN stage_rank END)", "MIN(CASE WHEN stage_rank >= 4 AND stage_rank < 99 THEN conversation_created_at END)", "MIN(CASE WHEN stage_rank >= 5 AND stage_rank < 99 THEN conversation_created_at END)", "MIN(CASE WHEN stage_rank >= 7 AND stage_rank < 99 THEN conversation_created_at END)"] | 2707 | 203.159 |
| [S39/Q36](#s39) | success | ["intercom__conversation_enhanced", "intercom__conversation_metrics"] | 2 / {'INNER': 1, 'LEFT': 1} | ["contact_id"] | ["MAX(CASE WHEN stage_rank >= 1 AND stage_rank < 99 THEN stage_rank END)", "MIN(CASE WHEN stage_rank >= 4 AND stage_rank < 99 THEN conversation_created_at END)", "MIN(CASE WHEN stage_rank >= 5 AND stage_rank < 99 THEN conversation_created_at END)", "MIN(CASE WHEN stage_rank >= 7 AND stage_rank < 99 THEN conversation_created_at END)"] | 2707 | 202.246 |
| [S40/Q37](#s40) | success | ["intercom__conversation_enhanced", "intercom__conversation_metrics"] | 2 / {'INNER': 1, 'LEFT': 1} | ["contact_id"] | ["MAX(CASE WHEN stage_rank >= 1 AND stage_rank < 99 THEN stage_rank END)", "MIN(CASE WHEN stage_rank >= 4 AND stage_rank < 99 THEN conversation_created_at END)", "MIN(CASE WHEN stage_rank >= 5 AND stage_rank < 99 THEN conversation_created_at END)", "MIN(CASE WHEN stage_rank >= 7 AND stage_rank < 99 THEN conversation_created_at END)"] | 2707 | 205.548 |
| [S41/Q38](#s41) | success | ["intercom__conversation_enhanced", "intercom__conversation_metrics"] | 2 / {'INNER': 1} | [] | [] | 6703 | 53.131 |
| [S42/Q39](#s42) | success | ["intercom__conversation_enhanced", "intercom__conversation_metrics"] | 2 / {'INNER': 1} | [] | [] | 6703 | 21.283 |
| [S43/Q40](#s43) | success | ["intercom__company_enhanced", "intercom__contact_enhanced", "intercom__conversation_enhanced"] | 3 / {'LEFT': 2} | [] | [] | 10 | 5.952 |
| [S44/Q41](#s44) | success | ["intercom__company_enhanced", "intercom__contact_enhanced"] | 2 / {'LEFT': 1} | [] | [] | 20 | 3.073 |
| [S45/Q42](#s45) | success | ["intercom__company_enhanced", "intercom__contact_enhanced"] | 2 / {'LEFT': 1} | [] | ["COUNT(*)", "SUM(CASE WHEN NOT c.company_id IS NULL THEN 1 ELSE 0 END)"] | 1 | 3.578 |
| [S46/Q43](#s46) | success | ["intercom__company_enhanced", "intercom__contact_enhanced"] | 2 / {'LEFT': 1} | [] | [] | 49051 | 85.405 |
| [S47/Q44](#s47) | success | ["intercom__contact_enhanced"] | 0 / {} | [] | [] | 2707 | 7.696 |


## 元数据和设置

| SQL | 类别 | 状态 | 内容 |
| --- | --- | --- | --- |
| S1 | connection_setup | success | PRAGMA query_only=ON |
| S2 | metadata | success | SELECT name,sql FROM sqlite_master WHERE type='table' ORDER BY name |
| S3 | metadata | success | SELECT name FROM sqlite_master WHERE type='table' ORDER BY name |


## Python 与执行位置

人工源码审查：**database_first_violation**。Python 导出联系人漏斗后按首次响应类型、意向、话题、地区和客户段筛选并求阶段转化计数、比例、平均耗时；这些 WHERE、条件 SUM、日期差及 GROUP BY 可在 SQL 内完成。卡方和 Mann–Whitney 检验为统计补充，不能把其前置的业务计数一并列为例外。 [证据](../reviews/dacomp-098.json)。

P1：Compute conversion rates, stage durations, and segment-level breakdowns from the contact-level journey data. SQL cannot easily do the multi-step conditional aggregation and statistical calculations needed for this analysis, especially the duration calculations and segment breakdowns.

[源码](../../../runs/dsv4flash-db-first-full-01/dacomp-098/attempt-01/python/P1.py)；[输出](../../../runs/dsv4flash-db-first-full-01/dacomp-098/attempt-01/python/P1.stdout)；[错误](../../../runs/dsv4flash-db-first-full-01/dacomp-098/attempt-01/python/P1.stderr)。检出需人工核验的 SQL 可实现操作：groupby(, sort_values(；不能仅凭理由判为合规。

P2：Check column names in the JSONL result file to ensure correct DataFrame construction.

[源码](../../../runs/dsv4flash-db-first-full-01/dacomp-098/attempt-01/python/P2.py)；[输出](../../../runs/dsv4flash-db-first-full-01/dacomp-098/attempt-01/python/P2.stdout)；[错误](../../../runs/dsv4flash-db-first-full-01/dacomp-098/attempt-01/python/P2.stderr)。自动源码筛查未检出预设迁出信号；这不是全面语义合规证明。

P3：Check the actual format of the JSONL result file - whether it's a list of arrays or dicts

[源码](../../../runs/dsv4flash-db-first-full-01/dacomp-098/attempt-01/python/P3.py)；[输出](../../../runs/dsv4flash-db-first-full-01/dacomp-098/attempt-01/python/P3.stdout)；[错误](../../../runs/dsv4flash-db-first-full-01/dacomp-098/attempt-01/python/P3.stderr)。自动源码筛查未检出预设迁出信号；这不是全面语义合规证明。

P4：Use db.frame() to get the contact-level data with proper column names for the funnel analysis

[源码](../../../runs/dsv4flash-db-first-full-01/dacomp-098/attempt-01/python/P4.py)；[输出](../../../runs/dsv4flash-db-first-full-01/dacomp-098/attempt-01/python/P4.stdout)；[错误](../../../runs/dsv4flash-db-first-full-01/dacomp-098/attempt-01/python/P4.stderr)。检出需人工核验的 SQL 可实现操作：.query(；不能仅凭理由判为合规。

P5：Compute conversion rates, stage durations, and cross-tabulations for the bot vs human funnel comparison. These conditional probability and duration calculations are easier and clearer in Python, though the data was assembled in SQL.

[源码](../../../runs/dsv4flash-db-first-full-01/dacomp-098/attempt-01/python/P5.py)；[输出](../../../runs/dsv4flash-db-first-full-01/dacomp-098/attempt-01/python/P5.stdout)；[错误](../../../runs/dsv4flash-db-first-full-01/dacomp-098/attempt-01/python/P5.stderr)。检出需人工核验的 SQL 可实现操作：.query(；不能仅凭理由判为合规。

P6：Compute cross-tabulations of conversion rates by intent, topic, region, and segment to identify scenarios where bot vs human first response performs differently.

[源码](../../../runs/dsv4flash-db-first-full-01/dacomp-098/attempt-01/python/P6.py)；[输出](../../../runs/dsv4flash-db-first-full-01/dacomp-098/attempt-01/python/P6.stdout)；[错误](../../../runs/dsv4flash-db-first-full-01/dacomp-098/attempt-01/python/P6.stderr)。自动源码筛查未检出预设迁出信号；这不是全面语义合规证明。

P7：Run statistical significance tests (chi-square for conversion rates, Mann-Whitney for durations) and examine conversation quality metrics (rating, reopens, parts, close rates) by bot vs human first response, to determine which observed differences are meaningful.

[源码](../../../runs/dsv4flash-db-first-full-01/dacomp-098/attempt-01/python/P7.py)；[输出](../../../runs/dsv4flash-db-first-full-01/dacomp-098/attempt-01/python/P7.stdout)；[错误](../../../runs/dsv4flash-db-first-full-01/dacomp-098/attempt-01/python/P7.stderr)。自动源码筛查未检出预设迁出信号；这不是全面语义合规证明。

P8：Examine conversation-level quality metrics (rating, reopens, parts, SLA, subjects) and the funnel-stage distribution of first conversations by first-response type to identify content-feature drivers and any selection effects.

[源码](../../../runs/dsv4flash-db-first-full-01/dacomp-098/attempt-01/python/P8.py)；[输出](../../../runs/dsv4flash-db-first-full-01/dacomp-098/attempt-01/python/P8.stdout)；[错误](../../../runs/dsv4flash-db-first-full-01/dacomp-098/attempt-01/python/P8.stderr)。检出需人工核验的 SQL 可实现操作：.query(；不能仅凭理由判为合规。

P9：Examine SLA name, conversation rating remark (sentiment), and company-industry breakdowns to identify content-driven differences in bot vs human performance.

[源码](../../../runs/dsv4flash-db-first-full-01/dacomp-098/attempt-01/python/P9.py)；[输出](../../../runs/dsv4flash-db-first-full-01/dacomp-098/attempt-01/python/P9.stdout)；[错误](../../../runs/dsv4flash-db-first-full-01/dacomp-098/attempt-01/python/P9.stderr)。检出需人工核验的 SQL 可实现操作：.query(；不能仅凭理由判为合规。

P10：Join contact funnel data to company industry/plan data via the contact-to-company name mapping, then compute conversion rates by industry and plan to explain differences at the company level.

[源码](../../../runs/dsv4flash-db-first-full-01/dacomp-098/attempt-01/python/P10.py)；[输出](../../../runs/dsv4flash-db-first-full-01/dacomp-098/attempt-01/python/P10.stdout)；[错误](../../../runs/dsv4flash-db-first-full-01/dacomp-098/attempt-01/python/P10.stderr)。检出需人工核验的 SQL 可实现操作：.merge(, .query(；不能仅凭理由判为合规。

P11：Parse lead source from contact tags and compute conversion rates by lead source × first response type, and run significance tests on key industry differences.

[源码](../../../runs/dsv4flash-db-first-full-01/dacomp-098/attempt-01/python/P11.py)；[输出](../../../runs/dsv4flash-db-first-full-01/dacomp-098/attempt-01/python/P11.stdout)；[错误](../../../runs/dsv4flash-db-first-full-01/dacomp-098/attempt-01/python/P11.stderr)。检出需人工核验的 SQL 可实现操作：.merge(, .query(；不能仅凭理由判为合规。

P12：Create publication-quality visualizations of the funnel comparison, stage durations, and segment-level differences for the report.

[源码](../../../runs/dsv4flash-db-first-full-01/dacomp-098/attempt-01/python/P12.py)；[输出](../../../runs/dsv4flash-db-first-full-01/dacomp-098/attempt-01/python/P12.stdout)；[错误](../../../runs/dsv4flash-db-first-full-01/dacomp-098/attempt-01/python/P12.stderr)。自动源码筛查未检出预设迁出信号；这不是全面语义合规证明。

## 优化机会

已验证候选。筛选限于精确 SQL、相同自包含 CTE、相同单表完整过滤、可分解单表聚合；未覆盖任意 Join 等价和一般谓词蕴含。全部候选都是 offline，未测在线预测。

| 候选 | 类型 | 已有结果 | 覆盖 SQL | 后续次数 | 中间行数 | 验证 | 成本 |
| --- | --- | --- | --- | --- | --- | --- | --- |
| C1 | exact-result reuse | True | ["S39", "S40"] | 1 | 2707 | verified | Not benchmarked; correctness alone does not establish net speedup. |
| C2 | common subexpression | False | ["S38", "S39", "S40"] | 2 | 6703 | verified | Not benchmarked; correctness alone does not establish net speedup. |
| C3 | aggregate MV | False | ["S9", "S10", "S19", "S20", "S21", "S22", "S25", "S33", "S34", "S35", "S36"] | 10 | 6701 | verified | Not benchmarked; correctness alone does not establish net speedup. |


已验证覆盖（含触发查询、候选并集去重）：14/42 条成功数据 SQL。正确性仅针对当前数据库快照；未测性能的候选不能声称已加速。

[完整 build/rewrite 与比较证据](dacomp-098.analysis.json)。

### C3：aggregate MV

Union of grouping keys; decomposable aggregate states; AVG uses SUM and non-NULL COUNT.

原查询 [S9](#s9), [S10](#s10), [S19](#s19), [S20](#s20), [S21](#s21), [S22](#s22), [S25](#s25), [S33](#s33), [S34](#s34), [S35](#s35), [S36](#s36) → 新增共享状态 C3 → 后续 10 次可复用。该构建点为事后假设，不代表 Agent 当时预知后续。

构建定义：

```sql
SELECT conversation_initiated_type AS __g0, CASE WHEN INSTR(all_conversation_tags, 'stage:') > 0 THEN SUBSTRING(all_conversation_tags, INSTR(all_conversation_tags, 'stage:') + 6, CASE WHEN INSTR(SUBSTRING(all_conversation_tags, INSTR(all_conversation_tags, 'stage:') + 6), '|') > 0 THEN INSTR(SUBSTRING(all_conversation_tags, INSTR(all_conversation_tags, 'stage:') + 6), '|') - 1 ELSE LENGTH(SUBSTRING(all_conversation_tags, INSTR(all_conversation_tags, 'stage:') + 6)) END) END AS __g1, CASE WHEN INSTR(all_conversation_tags, 'intent:') > 0 THEN SUBSTRING(all_conversation_tags, INSTR(all_conversation_tags, 'intent:') + 7, CASE WHEN INSTR(SUBSTRING(all_conversation_tags, INSTR(all_conversation_tags, 'intent:') + 7), '|') > 0 THEN INSTR(SUBSTRING(all_conversation_tags, INSTR(all_conversation_tags, 'intent:') + 7), '|') - 1 ELSE LENGTH(SUBSTRING(all_conversation_tags, INSTR(all_conversation_tags, 'intent:') + 7)) END) END AS __g2, CASE WHEN INSTR(all_conversation_tags, 'topic:') > 0 THEN SUBSTRING(all_conversation_tags, INSTR(all_conversation_tags, 'topic:') + 6, CASE WHEN INSTR(SUBSTRING(all_conversation_tags, INSTR(all_conversation_tags, 'topic:') + 6), '|') > 0 THEN INSTR(SUBSTRING(all_conversation_tags, INSTR(all_conversation_tags, 'topic:') + 6), '|') - 1 ELSE LENGTH(SUBSTRING(all_conversation_tags, INSTR(all_conversation_tags, 'topic:') + 6)) END) END AS __g3, CASE WHEN INSTR(all_conversation_tags, 'region:') > 0 THEN SUBSTRING(all_conversation_tags, INSTR(all_conversation_tags, 'region:') + 7, CASE WHEN INSTR(SUBSTRING(all_conversation_tags, INSTR(all_conversation_tags, 'region:') + 7), '|') > 0 THEN INSTR(SUBSTRING(all_conversation_tags, INSTR(all_conversation_tags, 'region:') + 7), '|') - 1 ELSE LENGTH(SUBSTRING(all_conversation_tags, INSTR(all_conversation_tags, 'region:') + 7)) END) END AS __g4, all_conversation_contacts AS __g5, CASE WHEN INSTR(all_conversation_tags, 'path:') > 0 THEN SUBSTRING(all_conversation_tags, INSTR(all_conversation_tags, 'path:') + 5, CASE WHEN INSTR(SUBSTRING(all_conversation_tags, INSTR(all_conversation_tags, 'path:') + 5), '|') > 0 THEN INSTR(SUBSTRING(all_conversation_tags, INSTR(all_conversation_tags, 'path:') + 5), '|') - 1 ELSE LENGTH(SUBSTRING(all_conversation_tags, INSTR(all_conversation_tags, 'path:') + 5)) END) END AS __g6, CASE WHEN INSTR(all_conversation_tags, 'lifecycle:') > 0 THEN SUBSTRING(all_conversation_tags, INSTR(all_conversation_tags, 'lifecycle:') + 10, CASE WHEN INSTR(SUBSTRING(all_conversation_tags, INSTR(all_conversation_tags, 'lifecycle:') + 10), '|') > 0 THEN INSTR(SUBSTRING(all_conversation_tags, INSTR(all_conversation_tags, 'lifecycle:') + 10), '|') - 1 ELSE LENGTH(SUBSTRING(all_conversation_tags, INSTR(all_conversation_tags, 'lifecycle:') + 10)) END) END AS __g7, CASE WHEN INSTR(all_conversation_tags, 'segment:') > 0 THEN SUBSTRING(all_conversation_tags, INSTR(all_conversation_tags, 'segment:') + 8, CASE WHEN INSTR(SUBSTRING(all_conversation_tags, INSTR(all_conversation_tags, 'segment:') + 8), '|') > 0 THEN INSTR(SUBSTRING(all_conversation_tags, INSTR(all_conversation_tags, 'segment:') + 8), '|') - 1 ELSE LENGTH(SUBSTRING(all_conversation_tags, INSTR(all_conversation_tags, 'segment:') + 8)) END) END AS __g8, COUNT(*) AS __a0 FROM "intercom__conversation_enhanced"  GROUP BY conversation_initiated_type, CASE WHEN INSTR(all_conversation_tags, 'stage:') > 0 THEN SUBSTRING(all_conversation_tags, INSTR(all_conversation_tags, 'stage:') + 6, CASE WHEN INSTR(SUBSTRING(all_conversation_tags, INSTR(all_conversation_tags, 'stage:') + 6), '|') > 0 THEN INSTR(SUBSTRING(all_conversation_tags, INSTR(all_conversation_tags, 'stage:') + 6), '|') - 1 ELSE LENGTH(SUBSTRING(all_conversation_tags, INSTR(all_conversation_tags, 'stage:') + 6)) END) END, CASE WHEN INSTR(all_conversation_tags, 'intent:') > 0 THEN SUBSTRING(all_conversation_tags, INSTR(all_conversation_tags, 'intent:') + 7, CASE WHEN INSTR(SUBSTRING(all_conversation_tags, INSTR(all_conversation_tags, 'intent:') + 7), '|') > 0 THEN INSTR(SUBSTRING(all_conversation_tags, INSTR(all_conversation_tags, 'intent:') + 7), '|') - 1 ELSE LENGTH(SUBSTRING(all_conversation_tags, INSTR(all_conversation_tags, 'intent:') + 7)) END) END, CASE WHEN INSTR(all_conversation_tags, 'topic:') > 0 THEN SUBSTRING(all_conversation_tags, INSTR(all_conversation_tags, 'topic:') + 6, CASE WHEN INSTR(SUBSTRING(all_conversation_tags, INSTR(all_conversation_tags, 'topic:') + 6), '|') > 0 THEN INSTR(SUBSTRING(all_conversation_tags, INSTR(all_conversation_tags, 'topic:') + 6), '|') - 1 ELSE LENGTH(SUBSTRING(all_conversation_tags, INSTR(all_conversation_tags, 'topic:') + 6)) END) END, CASE WHEN INSTR(all_conversation_tags, 'region:') > 0 THEN SUBSTRING(all_conversation_tags, INSTR(all_conversation_tags, 'region:') + 7, CASE WHEN INSTR(SUBSTRING(all_conversation_tags, INSTR(all_conversation_tags, 'region:') + 7), '|') > 0 THEN INSTR(SUBSTRING(all_conversation_tags, INSTR(all_conversation_tags, 'region:') + 7), '|') - 1 ELSE LENGTH(SUBSTRING(all_conversation_tags, INSTR(all_conversation_tags, 'region:') + 7)) END) END, all_conversation_contacts, CASE WHEN INSTR(all_conversation_tags, 'path:') > 0 THEN SUBSTRING(all_conversation_tags, INSTR(all_conversation_tags, 'path:') + 5, CASE WHEN INSTR(SUBSTRING(all_conversation_tags, INSTR(all_conversation_tags, 'path:') + 5), '|') > 0 THEN INSTR(SUBSTRING(all_conversation_tags, INSTR(all_conversation_tags, 'path:') + 5), '|') - 1 ELSE LENGTH(SUBSTRING(all_conversation_tags, INSTR(all_conversation_tags, 'path:') + 5)) END) END, CASE WHEN INSTR(all_conversation_tags, 'lifecycle:') > 0 THEN SUBSTRING(all_conversation_tags, INSTR(all_conversation_tags, 'lifecycle:') + 10, CASE WHEN INSTR(SUBSTRING(all_conversation_tags, INSTR(all_conversation_tags, 'lifecycle:') + 10), '|') > 0 THEN INSTR(SUBSTRING(all_conversation_tags, INSTR(all_conversation_tags, 'lifecycle:') + 10), '|') - 1 ELSE LENGTH(SUBSTRING(all_conversation_tags, INSTR(all_conversation_tags, 'lifecycle:') + 10)) END) END, CASE WHEN INSTR(all_conversation_tags, 'segment:') > 0 THEN SUBSTRING(all_conversation_tags, INSTR(all_conversation_tags, 'segment:') + 8, CASE WHEN INSTR(SUBSTRING(all_conversation_tags, INSTR(all_conversation_tags, 'segment:') + 8), '|') > 0 THEN INSTR(SUBSTRING(all_conversation_tags, INSTR(all_conversation_tags, 'segment:') + 8), '|') - 1 ELSE LENGTH(SUBSTRING(all_conversation_tags, INSTR(all_conversation_tags, 'segment:') + 8)) END) END
```

受益查询 S9 的改写示例：

```sql
SELECT __g0 AS "conversation_initiated_type", SUM(__a0) AS cnt FROM temp.reuse_candidate GROUP BY __g0
```

| 原 SQL | 列名一致 | 结果一致 | 比较方法 |
| --- | --- | --- | --- |
| S9 | True | True | exact_multiset |
| S10 | True | True | exact_multiset |
| S19 | True | True | ordered_numeric_tolerance |
| S20 | True | True | ordered_numeric_tolerance |
| S21 | True | True | ordered_numeric_tolerance |
| S22 | True | True | ordered_numeric_tolerance |
| S25 | True | True | ordered_numeric_tolerance |
| S33 | True | True | ordered_numeric_tolerance |
| S34 | True | True | ordered_numeric_tolerance |
| S35 | True | True | exact_multiset |
| S36 | True | True | ordered_numeric_tolerance |


验证状态：verified；成本结论：Not benchmarked; correctness alone does not establish net speedup.

### C2：common subexpression

Identical self-contained CTE body across queries.

原查询 [S38](#s38), [S39](#s39), [S40](#s40) → 新增共享状态 C2 → 后续 2 次可复用。该构建点为事后假设，不代表 Agent 当时预知后续。

构建定义：

```sql
SELECT ce.all_conversation_contacts AS contact_id, ce.conversation_id, ce.conversation_created_at, ce.conversation_initiated_type, cm.first_admin_response_at, cm.time_to_first_response_minutes, CASE WHEN INSTR(ce.all_conversation_tags, 'stage:') > 0 THEN SUBSTRING(ce.all_conversation_tags, INSTR(ce.all_conversation_tags, 'stage:') + 6, CASE WHEN INSTR(SUBSTRING(ce.all_conversation_tags, INSTR(ce.all_conversation_tags, 'stage:') + 6), '|') > 0 THEN INSTR(SUBSTRING(ce.all_conversation_tags, INSTR(ce.all_conversation_tags, 'stage:') + 6), '|') - 1 ELSE LENGTH(SUBSTRING(ce.all_conversation_tags, INSTR(ce.all_conversation_tags, 'stage:') + 6)) END) END AS stage, CASE WHEN INSTR(ce.all_conversation_tags, 'intent:') > 0 THEN SUBSTRING(ce.all_conversation_tags, INSTR(ce.all_conversation_tags, 'intent:') + 7, CASE WHEN INSTR(SUBSTRING(ce.all_conversation_tags, INSTR(ce.all_conversation_tags, 'intent:') + 7), '|') > 0 THEN INSTR(SUBSTRING(ce.all_conversation_tags, INSTR(ce.all_conversation_tags, 'intent:') + 7), '|') - 1 ELSE LENGTH(SUBSTRING(ce.all_conversation_tags, INSTR(ce.all_conversation_tags, 'intent:') + 7)) END) END AS intent, CASE WHEN INSTR(ce.all_conversation_tags, 'topic:') > 0 THEN SUBSTRING(ce.all_conversation_tags, INSTR(ce.all_conversation_tags, 'topic:') + 6, CASE WHEN INSTR(SUBSTRING(ce.all_conversation_tags, INSTR(ce.all_conversation_tags, 'topic:') + 6), '|') > 0 THEN INSTR(SUBSTRING(ce.all_conversation_tags, INSTR(ce.all_conversation_tags, 'topic:') + 6), '|') - 1 ELSE LENGTH(SUBSTRING(ce.all_conversation_tags, INSTR(ce.all_conversation_tags, 'topic:') + 6)) END) END AS topic, CASE WHEN INSTR(ce.all_conversation_tags, 'region:') > 0 THEN SUBSTRING(ce.all_conversation_tags, INSTR(ce.all_conversation_tags, 'region:') + 7, CASE WHEN INSTR(SUBSTRING(ce.all_conversation_tags, INSTR(ce.all_conversation_tags, 'region:') + 7), '|') > 0 THEN INSTR(SUBSTRING(ce.all_conversation_tags, INSTR(ce.all_conversation_tags, 'region:') + 7), '|') - 1 ELSE LENGTH(SUBSTRING(ce.all_conversation_tags, INSTR(ce.all_conversation_tags, 'region:') + 7)) END) END AS region, CASE WHEN INSTR(ce.all_conversation_tags, 'segment:') > 0 THEN SUBSTRING(ce.all_conversation_tags, INSTR(ce.all_conversation_tags, 'segment:') + 8, CASE WHEN INSTR(SUBSTRING(ce.all_conversation_tags, INSTR(ce.all_conversation_tags, 'segment:') + 8), '|') > 0 THEN INSTR(SUBSTRING(ce.all_conversation_tags, INSTR(ce.all_conversation_tags, 'segment:') + 8), '|') - 1 ELSE LENGTH(SUBSTRING(ce.all_conversation_tags, INSTR(ce.all_conversation_tags, 'segment:') + 8)) END) END AS segment FROM intercom__conversation_enhanced AS ce JOIN intercom__conversation_metrics AS cm ON ce.conversation_id = cm.conversation_id
```

受益查询 S38 的改写示例（截取前 1600 字符，完整版本见证据 JSON）：

```sql
WITH conv AS (SELECT * FROM temp.reuse_candidate), staged AS (SELECT *, CASE stage WHEN 'contacted' THEN 1 WHEN 'marketing_qualified' THEN 2 WHEN 'trial_started' THEN 3 WHEN 'demo_booked' THEN 4 WHEN 'trial_activated' THEN 5 WHEN 'proposal_sent' THEN 6 WHEN 'closed_won' THEN 7 WHEN 'expansion_in_flight' THEN 8 WHEN 'closed_lost' THEN 99 ELSE 0 END AS stage_rank FROM conv), first_contact AS (SELECT contact_id, ROW_NUMBER() OVER (PARTITION BY contact_id ORDER BY conversation_created_at) AS rn, conversation_created_at AS first_conv_at, conversation_initiated_type AS first_type, first_admin_response_at AS first_response_at, time_to_first_response_minutes AS first_response_mins, stage, stage_rank, intent, topic, region, segment FROM staged), first_conv AS (SELECT * FROM first_contact WHERE rn = 1), milestones AS (SELECT contact_id, MAX(CASE WHEN stage_rank >= 1 AND stage_rank < 99 THEN stage_rank END) AS max_stage_rank, MIN(CASE WHEN stage_rank >= 4 AND stage_rank < 99 THEN conversation_created_at END) AS demo_booked_at, MIN(CASE WHEN stage_rank >= 5 AND stage_rank < 99 THEN conversation_created_at END) AS trial_activated_at, MIN(CASE WHEN stage_rank >= 7 AND stage_rank < 99 THEN conversation_created_at END) AS paid_at FROM staged GROUP BY contact_id) SELECT fc.contact_id, fc.first_type, fc.first_conv_at, fc.first_response_at, fc.first_response_mins, fc.intent, fc.topic, fc.region, fc.segment, fc.stage AS first_stage, fc.stage_rank AS first_stage_rank, ms.max_stage_rank, ms.demo_booked_at, ms.trial_activated_at, ms.paid_at, CASE WHEN NOT ms.demo_booked_at IS NULL THEN 1 ELSE 0 E
```

| 原 SQL | 列名一致 | 结果一致 | 比较方法 |
| --- | --- | --- | --- |
| S38 | True | True | ordered_numeric_tolerance |
| S39 | True | True | ordered_numeric_tolerance |
| S40 | True | True | ordered_numeric_tolerance |


验证状态：verified；成本结论：Not benchmarked; correctness alone does not establish net speedup.

### C1：exact-result reuse

Identical normalized SQL and parameters; archive equality checked.

原查询 [S39](#s39), [S40](#s40) → 保留前序结果 S39 → 后续 1 次可复用。该构建点为事后假设，不代表 Agent 当时预知后续。

| 原 SQL | 列名一致 | 结果一致 | 比较方法 |
| --- | --- | --- | --- |
| S40 | True | True | ordered_numeric_tolerance |


验证状态：verified；成本结论：Not benchmarked; correctness alone does not establish net speedup.

结果依赖：自动记录 SQL→Python 的接口父调用，以及源码中引用归档文件的消费者；字面值相同不认定因果。模型方向选择需要人工读取消息，尚未做全面因果标注。

[原始报告](../../../runs/dsv4flash-db-first-full-01/dacomp-098/attempt-01/answer.md)；[统一消息](../../../runs/dsv4flash-db-first-full-01/dacomp-098/attempt-01/messages.jsonl)；[原始 OpenCode 事件](../../../runs/dsv4flash-db-first-full-01/dacomp-098/attempt-01/opencode.jsonl)；[SQL 引擎日志](../../../runs/dsv4flash-db-first-full-01/dacomp-098/attempt-01/sql_journal.jsonl)。

[可读报告（本地图片链接规范化）](../answers/dacomp-098.md)。原始回答保留，分析结论未改写。

## S1

类别 `connection_setup`；来源 `connection`；调用 `16d184a569f44293943a12c0ef53f61a`；状态 `success`。

```sql
PRAGMA query_only=ON
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-098/attempt-01/sql/S1.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-098/attempt-01/sql/S1.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-098/attempt-01/results/S1.rows.jsonl)；完整：True；SHA256：`e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`。

## S2

类别 `metadata`；来源 `list_db`；调用 `16d184a569f44293943a12c0ef53f61a`；状态 `success`。

```sql
SELECT name,sql FROM sqlite_master WHERE type='table' ORDER BY name
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-098/attempt-01/sql/S2.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-098/attempt-01/sql/S2.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-098/attempt-01/results/S2.rows.jsonl)；完整：True；SHA256：`dc8fc5e6224d4d2ddf161e83630a3e0976d5a9bf5828f563f927ed9f63e4681b`。

## S3

类别 `metadata`；来源 `query_db`；调用 `1be92c1b0b124283ba5b19e73c3437fa`；状态 `success`。

```sql
SELECT name FROM sqlite_master WHERE type='table' ORDER BY name
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-098/attempt-01/sql/S3.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-098/attempt-01/sql/S3.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-098/attempt-01/results/S3.rows.jsonl)；完整：True；SHA256：`fa2b56eeca32debabe3deebfafca416bcacc5016d4daeb25443ec439b0061384`。

## S4

类别 `data`；来源 `query_db`；调用 `52522d3ab9eb485ab69be85b6913017a`；状态 `success`。

```sql
SELECT * FROM intercom__conversation_enhanced LIMIT 5
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-098/attempt-01/sql/S4.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-098/attempt-01/sql/S4.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-098/attempt-01/results/S4.rows.jsonl)；完整：True；SHA256：`0a62727b8b9621704da933dbd049542b8847198e167e61ab509d5ad83bfaf251`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "intercom__conversation_enhanced", "kind": "base", "block": null, "base_tables": ["intercom__conversation_enhanced"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |


## S5

类别 `data`；来源 `query_db`；调用 `436d7ee5aa294a0c8a6cc50c6a838971`；状态 `success`。

```sql
SELECT * FROM intercom__conversation_metrics LIMIT 5
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-098/attempt-01/sql/S5.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-098/attempt-01/sql/S5.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-098/attempt-01/results/S5.rows.jsonl)；完整：True；SHA256：`157e702a675838bc6f52d9977195eca6510e350a42ceecf0b522ae3701599028`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "intercom__conversation_metrics", "kind": "base", "block": null, "base_tables": ["intercom__conversation_metrics"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |


## S6

类别 `data`；来源 `query_db`；调用 `40a6b85db1864cb988352027e80951c0`；状态 `success`。

```sql
SELECT * FROM intercom__company_enhanced LIMIT 5
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-098/attempt-01/sql/S6.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-098/attempt-01/sql/S6.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-098/attempt-01/results/S6.rows.jsonl)；完整：True；SHA256：`e58c8c20f2bf3478574f6b3ca41a7fa8f77dfbe29f090eb21d6a1cf6bdc6139c`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "intercom__company_enhanced", "kind": "base", "block": null, "base_tables": ["intercom__company_enhanced"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |


## S7

类别 `data`；来源 `query_db`；调用 `bfe3ec75afef487f9afc4fcd6c2a1288`；状态 `success`。

```sql
SELECT * FROM intercom__company_metrics LIMIT 5
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-098/attempt-01/sql/S7.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-098/attempt-01/sql/S7.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-098/attempt-01/results/S7.rows.jsonl)；完整：True；SHA256：`88e36bbc785c5c8b342911f9263b0d1e281243afc8cc64452118a972c0ddbd20`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "intercom__company_metrics", "kind": "base", "block": null, "base_tables": ["intercom__company_metrics"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |


## S8

类别 `data`；来源 `query_db`；调用 `72157d5046384315abcce2ad4c23f78c`；状态 `success`。

```sql
SELECT * FROM intercom__contact_enhanced LIMIT 5
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-098/attempt-01/sql/S8.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-098/attempt-01/sql/S8.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-098/attempt-01/results/S8.rows.jsonl)；完整：True；SHA256：`f94f92f42ff9ccae18937583d11859fe5afd6d3ddb25fb1bdc44085daa5e7791`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "intercom__contact_enhanced", "kind": "base", "block": null, "base_tables": ["intercom__contact_enhanced"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |


## S9

类别 `data`；来源 `query_db`；调用 `4e0e3378b2a841a798105af3287de04f`；状态 `success`。

```sql
SELECT conversation_initiated_type, COUNT(*) as cnt FROM intercom__conversation_enhanced GROUP BY conversation_initiated_type
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-098/attempt-01/sql/S9.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-098/attempt-01/sql/S9.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-098/attempt-01/results/S9.rows.jsonl)；完整：True；SHA256：`0d123a7f57e55f21cc6b857d9571a3c524258a4567f7fa06abc8ccc8700e514b`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "intercom__conversation_enhanced", "kind": "base", "block": null, "base_tables": ["intercom__conversation_enhanced"]}] | [] | ["conversation_initiated_type"] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |


## S10

类别 `data`；来源 `query_db`；调用 `001111ff58794dd79ae10b6a8e7a538f`；状态 `success`。

```sql
SELECT COUNT(*) as total FROM intercom__conversation_enhanced
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-098/attempt-01/sql/S10.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-098/attempt-01/sql/S10.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-098/attempt-01/results/S10.rows.jsonl)；完整：True；SHA256：`20b1d17818ff06b3c178fb6a083d46fc454d428bcb3a0a8118c827db65a82b2e`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "intercom__conversation_enhanced", "kind": "base", "block": null, "base_tables": ["intercom__conversation_enhanced"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |


## S11

类别 `data`；来源 `query_db`；调用 `4048e9085ea449e686d53c82c1ed7140`；状态 `success`。

```sql
SELECT COUNT(*) as total FROM intercom__contact_enhanced
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-098/attempt-01/sql/S11.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-098/attempt-01/sql/S11.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-098/attempt-01/results/S11.rows.jsonl)；完整：True；SHA256：`e6ef327750d6d237be817363b86068bf72f60af77b8a3aa971b6f453a3ed6813`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "intercom__contact_enhanced", "kind": "base", "block": null, "base_tables": ["intercom__contact_enhanced"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |


## S12

类别 `data`；来源 `query_db`；调用 `4fb2039011a242639c2344e2aa81461c`；状态 `success`。

```sql
SELECT COUNT(*) as total FROM intercom__company_enhanced
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-098/attempt-01/sql/S12.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-098/attempt-01/sql/S12.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-098/attempt-01/results/S12.rows.jsonl)；完整：True；SHA256：`b0d6d21a6709824bcb4210d15c142d9b8c0ad2fa9f4299e758bd927ce4d24ff5`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "intercom__company_enhanced", "kind": "base", "block": null, "base_tables": ["intercom__company_enhanced"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |


## S13

类别 `data`；来源 `query_db`；调用 `e778688a5e1e40ff9fd032ace43a351a`；状态 `success`。

```sql
SELECT COUNT(*) as total FROM intercom__conversation_metrics
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-098/attempt-01/sql/S13.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-098/attempt-01/sql/S13.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-098/attempt-01/results/S13.rows.jsonl)；完整：True；SHA256：`20b1d17818ff06b3c178fb6a083d46fc454d428bcb3a0a8118c827db65a82b2e`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "intercom__conversation_metrics", "kind": "base", "block": null, "base_tables": ["intercom__conversation_metrics"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |


## S14

类别 `data`；来源 `query_db`；调用 `cb957f410f134e54a42a50518454c527`；状态 `success`。

```sql
SELECT DISTINCT conversation_author_type FROM intercom__conversation_enhanced
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-098/attempt-01/sql/S14.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-098/attempt-01/sql/S14.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-098/attempt-01/results/S14.rows.jsonl)；完整：True；SHA256：`51c9f98d8b25fd5a584a829811f1a569f6afc3086aba0da8f8bbca9f492ae9f5`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "intercom__conversation_enhanced", "kind": "base", "block": null, "base_tables": ["intercom__conversation_enhanced"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |


## S15

类别 `data`；来源 `query_db`；调用 `fa91253a234242509108972df4d13dff`；状态 `success`。

```sql
SELECT DISTINCT all_conversation_tags FROM intercom__conversation_enhanced LIMIT 40
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-098/attempt-01/sql/S15.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-098/attempt-01/sql/S15.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-098/attempt-01/results/S15.rows.jsonl)；完整：True；SHA256：`3b14f038a3ea033b16a08f0a7ed4a2e55405554c796ceb2b2368903ff12847cf`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "intercom__conversation_enhanced", "kind": "base", "block": null, "base_tables": ["intercom__conversation_enhanced"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |


## S16

类别 `data`；来源 `query_db`；调用 `d0d95b82848f4fe5910e9f15b559f2e7`；状态 `success`。

```sql
SELECT DISTINCT conversation_subject FROM intercom__conversation_enhanced
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-098/attempt-01/sql/S16.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-098/attempt-01/sql/S16.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-098/attempt-01/results/S16.rows.jsonl)；完整：True；SHA256：`b3341e6e062356d11f3d598362844fc609bb71cf6fe0c95d76f8c7c3147f9b06`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "intercom__conversation_enhanced", "kind": "base", "block": null, "base_tables": ["intercom__conversation_enhanced"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |


## S17

类别 `data`；来源 `query_db`；调用 `83707dedbd0a40e4adc4810ff3af1033`；状态 `success`。

```sql
SELECT DISTINCT all_company_tags FROM intercom__company_enhanced LIMIT 20
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-098/attempt-01/sql/S17.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-098/attempt-01/sql/S17.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-098/attempt-01/results/S17.rows.jsonl)；完整：True；SHA256：`e03b0ab2dd68dd1d0f53d723986a60e4f6b9e5165b54b9f1e38561718b62f06b`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "intercom__company_enhanced", "kind": "base", "block": null, "base_tables": ["intercom__company_enhanced"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |


## S18

类别 `data`；来源 `query_db`；调用 `1f86023376f54e1390c5025ddc723cff`；状态 `success`。

```sql
SELECT DISTINCT all_contact_tags FROM intercom__contact_enhanced LIMIT 20
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-098/attempt-01/sql/S18.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-098/attempt-01/sql/S18.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-098/attempt-01/results/S18.rows.jsonl)；完整：True；SHA256：`f6a396389adb5db03892c7ab78da5ddc5dc304d233d35fb6ad860096c62343cd`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "intercom__contact_enhanced", "kind": "base", "block": null, "base_tables": ["intercom__contact_enhanced"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |


## S19

类别 `data`；来源 `query_db`；调用 `7a3016477e514a46acfb3984ccdffdf5`；状态 `success`。

```sql
SELECT DISTINCT 
  CASE WHEN instr(all_conversation_tags,'stage:')>0 THEN
    substr(all_conversation_tags, instr(all_conversation_tags,'stage:')+6, CASE WHEN instr(substr(all_conversation_tags,instr(all_conversation_tags,'stage:')+6),'|')>0 THEN instr(substr(all_conversation_tags,instr(all_conversation_tags,'stage:')+6),'|')-1 ELSE length(substr(all_conversation_tags,instr(all_conversation_tags,'stage:')+6)) END)
  END AS stage,
  COUNT(*) AS cnt
FROM intercom__conversation_enhanced
GROUP BY stage ORDER BY cnt DESC
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-098/attempt-01/sql/S19.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-098/attempt-01/sql/S19.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-098/attempt-01/results/S19.rows.jsonl)；完整：True；SHA256：`1904f1a298ba75db45c3750b261c69296c9b843d8d4149526caf3f692f845c7a`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "intercom__conversation_enhanced", "kind": "base", "block": null, "base_tables": ["intercom__conversation_enhanced"]}] | [] | ["CASE WHEN INSTR(all_conversation_tags, 'stage:') > 0 THEN SUBSTRING(all_conversation_tags, INSTR(all_conversation_tags, 'stage:') + 6, CASE WHEN INSTR(SUBSTRING(all_conversation_tags, INSTR(all_conversation_tags, 'stage:') + 6), '\|') > 0 THEN INSTR(SUBSTRING(all_conversation_tags, INSTR(all_conversation_tags, 'stage:') + 6), '\|') - 1 ELSE LENGTH(SUBSTRING(all_conversation_tags, INSTR(all_conversation_tags, 'stage:') + 6)) END) END"] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |


## S20

类别 `data`；来源 `query_db`；调用 `2084761accaa4d5f9fe9bf4ec19a11dc`；状态 `success`。

```sql
SELECT DISTINCT 
  CASE WHEN instr(all_conversation_tags,'intent:')>0 THEN
    substr(all_conversation_tags, instr(all_conversation_tags,'intent:')+7, CASE WHEN instr(substr(all_conversation_tags,instr(all_conversation_tags,'intent:')+7),'|')>0 THEN instr(substr(all_conversation_tags,instr(all_conversation_tags,'intent:')+7),'|')-1 ELSE length(substr(all_conversation_tags,instr(all_conversation_tags,'intent:')+7)) END)
  END AS intent,
  COUNT(*) AS cnt
FROM intercom__conversation_enhanced
GROUP BY intent ORDER BY cnt DESC
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-098/attempt-01/sql/S20.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-098/attempt-01/sql/S20.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-098/attempt-01/results/S20.rows.jsonl)；完整：True；SHA256：`7f2261d95235bc55b752e63a42bcdb67b400aed9e2f200dfcf2d7933cfb51225`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "intercom__conversation_enhanced", "kind": "base", "block": null, "base_tables": ["intercom__conversation_enhanced"]}] | [] | ["CASE WHEN INSTR(all_conversation_tags, 'intent:') > 0 THEN SUBSTRING(all_conversation_tags, INSTR(all_conversation_tags, 'intent:') + 7, CASE WHEN INSTR(SUBSTRING(all_conversation_tags, INSTR(all_conversation_tags, 'intent:') + 7), '\|') > 0 THEN INSTR(SUBSTRING(all_conversation_tags, INSTR(all_conversation_tags, 'intent:') + 7), '\|') - 1 ELSE LENGTH(SUBSTRING(all_conversation_tags, INSTR(all_conversation_tags, 'intent:') + 7)) END) END"] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |


## S21

类别 `data`；来源 `query_db`；调用 `23ed8b5f626d4072a3135dc7ff3e4f9d`；状态 `success`。

```sql
SELECT DISTINCT 
  CASE WHEN instr(all_conversation_tags,'topic:')>0 THEN
    substr(all_conversation_tags, instr(all_conversation_tags,'topic:')+6, CASE WHEN instr(substr(all_conversation_tags,instr(all_conversation_tags,'topic:')+6),'|')>0 THEN instr(substr(all_conversation_tags,instr(all_conversation_tags,'topic:')+6),'|')-1 ELSE length(substr(all_conversation_tags,instr(all_conversation_tags,'topic:')+6)) END)
  END AS topic,
  COUNT(*) AS cnt
FROM intercom__conversation_enhanced
GROUP BY topic ORDER BY cnt DESC
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-098/attempt-01/sql/S21.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-098/attempt-01/sql/S21.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-098/attempt-01/results/S21.rows.jsonl)；完整：True；SHA256：`01645b35cb21f171bce0ae205a66005083caab1b351c268174920b3a5c2e0efc`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "intercom__conversation_enhanced", "kind": "base", "block": null, "base_tables": ["intercom__conversation_enhanced"]}] | [] | ["CASE WHEN INSTR(all_conversation_tags, 'topic:') > 0 THEN SUBSTRING(all_conversation_tags, INSTR(all_conversation_tags, 'topic:') + 6, CASE WHEN INSTR(SUBSTRING(all_conversation_tags, INSTR(all_conversation_tags, 'topic:') + 6), '\|') > 0 THEN INSTR(SUBSTRING(all_conversation_tags, INSTR(all_conversation_tags, 'topic:') + 6), '\|') - 1 ELSE LENGTH(SUBSTRING(all_conversation_tags, INSTR(all_conversation_tags, 'topic:') + 6)) END) END"] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |


## S22

类别 `data`；来源 `query_db`；调用 `3dfc84d413a14e669cea02efcb76c940`；状态 `success`。

```sql
SELECT DISTINCT 
  CASE WHEN instr(all_conversation_tags,'region:')>0 THEN
    substr(all_conversation_tags, instr(all_conversation_tags,'region:')+7, CASE WHEN instr(substr(all_conversation_tags,instr(all_conversation_tags,'region:')+7),'|')>0 THEN instr(substr(all_conversation_tags,instr(all_conversation_tags,'region:')+7),'|')-1 ELSE length(substr(all_conversation_tags,instr(all_conversation_tags,'region:')+7)) END)
  END AS region,
  COUNT(*) AS cnt
FROM intercom__conversation_enhanced
GROUP BY region ORDER BY cnt DESC
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-098/attempt-01/sql/S22.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-098/attempt-01/sql/S22.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-098/attempt-01/results/S22.rows.jsonl)；完整：True；SHA256：`1a2372b3dfe831b9cdd86fc3833269189e2345d531c1fa42952ddd9761095ca7`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "intercom__conversation_enhanced", "kind": "base", "block": null, "base_tables": ["intercom__conversation_enhanced"]}] | [] | ["CASE WHEN INSTR(all_conversation_tags, 'region:') > 0 THEN SUBSTRING(all_conversation_tags, INSTR(all_conversation_tags, 'region:') + 7, CASE WHEN INSTR(SUBSTRING(all_conversation_tags, INSTR(all_conversation_tags, 'region:') + 7), '\|') > 0 THEN INSTR(SUBSTRING(all_conversation_tags, INSTR(all_conversation_tags, 'region:') + 7), '\|') - 1 ELSE LENGTH(SUBSTRING(all_conversation_tags, INSTR(all_conversation_tags, 'region:') + 7)) END) END"] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |


## S23

类别 `data`；来源 `query_db`；调用 `5260935269514793862e33765bd0a59d`；状态 `success`。

```sql
SELECT all_conversation_contacts, all_contact_company_names, conversation_created_at, conversation_initiated_type, all_conversation_tags FROM intercom__conversation_enhanced LIMIT 10
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-098/attempt-01/sql/S23.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-098/attempt-01/sql/S23.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-098/attempt-01/results/S23.rows.jsonl)；完整：True；SHA256：`0d157931ce02afe092c04832c23d1a8e0e42527f15369515162d490fecf0e089`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "intercom__conversation_enhanced", "kind": "base", "block": null, "base_tables": ["intercom__conversation_enhanced"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |


## S24

类别 `data`；来源 `query_db`；调用 `afe94a1e34bc4bc7b4e564ac9b51d720`；状态 `success`。

```sql
SELECT contact_id, all_contact_company_names, all_contact_tags FROM intercom__contact_enhanced LIMIT 10
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-098/attempt-01/sql/S24.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-098/attempt-01/sql/S24.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-098/attempt-01/results/S24.rows.jsonl)；完整：True；SHA256：`821a507fd44ea16c9ff2c32bba630d7ad36d045eb4ad7a380c7d228a59a04af6`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "intercom__contact_enhanced", "kind": "base", "block": null, "base_tables": ["intercom__contact_enhanced"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |


## S25

类别 `data`；来源 `query_db`；调用 `a08843b5e18a47debf26b710e54cd888`；状态 `success`。

```sql
SELECT all_conversation_contacts, COUNT(*) as cnt FROM intercom__conversation_enhanced GROUP BY all_conversation_contacts ORDER BY cnt DESC LIMIT 20
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-098/attempt-01/sql/S25.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-098/attempt-01/sql/S25.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-098/attempt-01/results/S25.rows.jsonl)；完整：True；SHA256：`5cbfa282747246ce3685fab286735549002822e2597e1ce65240be4a80f61890`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "intercom__conversation_enhanced", "kind": "base", "block": null, "base_tables": ["intercom__conversation_enhanced"]}] | [] | ["all_conversation_contacts"] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |


## S26

类别 `data`；来源 `query_db`；调用 `8d3992b884264a4ba0d527e93415a116`；状态 `success`。

```sql
SELECT COUNT(DISTINCT all_conversation_contacts) as unique_contacts FROM intercom__conversation_enhanced
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-098/attempt-01/sql/S26.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-098/attempt-01/sql/S26.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-098/attempt-01/results/S26.rows.jsonl)；完整：True；SHA256：`e6ef327750d6d237be817363b86068bf72f60af77b8a3aa971b6f453a3ed6813`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "intercom__conversation_enhanced", "kind": "base", "block": null, "base_tables": ["intercom__conversation_enhanced"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(DISTINCT all_conversation_contacts) | [{"table": "intercom__conversation_enhanced", "column": "all_conversation_contacts"}] | [] | False |


## S27

类别 `data`；来源 `query_db`；调用 `0447c610764549818455d7d387417994`；状态 `success`。

```sql
SELECT conversation_id, conversation_created_at, conversation_initiated_type, all_conversation_tags, all_contact_company_names
FROM intercom__conversation_enhanced
WHERE all_conversation_contacts IN (
  SELECT all_conversation_contacts FROM intercom__conversation_enhanced GROUP BY all_conversation_contacts HAVING COUNT(*)=3 LIMIT 1
)
ORDER BY conversation_created_at
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-098/attempt-01/sql/S27.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-098/attempt-01/sql/S27.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-098/attempt-01/results/S27.rows.jsonl)；完整：True；SHA256：`5db1e588690d5d54e34940d0f78e73bc6dcd3dbbeb7d598bbc8bb9f1e52b30fd`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "intercom__conversation_enhanced", "kind": "base", "block": null, "base_tables": ["intercom__conversation_enhanced"]}] | [] | ["all_conversation_contacts"] |
| B2 | [{"alias": "intercom__conversation_enhanced", "kind": "base", "block": null, "base_tables": ["intercom__conversation_enhanced"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |


## S28

类别 `data`；来源 `query_db`；调用 `aeddde5a45e847bab83c0983eb80d8d2`；状态 `success`。

```sql
SELECT COUNT(*) as cnt FROM (
  SELECT all_conversation_contacts FROM intercom__conversation_enhanced GROUP BY all_conversation_contacts HAVING COUNT(*)>1
)
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-098/attempt-01/sql/S28.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-098/attempt-01/sql/S28.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-098/attempt-01/results/S28.rows.jsonl)；完整：True；SHA256：`e6ef327750d6d237be817363b86068bf72f60af77b8a3aa971b6f453a3ed6813`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "intercom__conversation_enhanced", "kind": "base", "block": null, "base_tables": ["intercom__conversation_enhanced"]}] | [] | ["all_conversation_contacts"] |
| B2 | [{"alias": "", "kind": "derived", "block": "B1", "base_tables": ["intercom__conversation_enhanced"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |
| B2 | COUNT(*) | [] | [] | True |


## S29

类别 `data`；来源 `query_db`；调用 `c8721958252e4bd4b26aa517134334e2`；状态 `success`。

```sql
SELECT COUNT(*) as cnt FROM (
  SELECT all_conversation_contacts FROM intercom__conversation_enhanced GROUP BY all_conversation_contacts HAVING COUNT(*)=1
)
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-098/attempt-01/sql/S29.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-098/attempt-01/sql/S29.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-098/attempt-01/results/S29.rows.jsonl)；完整：True；SHA256：`c14196f132c1e9be0508ae80ab52fcb3e1d3fc05880415f3dc980971df207c9e`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "intercom__conversation_enhanced", "kind": "base", "block": null, "base_tables": ["intercom__conversation_enhanced"]}] | [] | ["all_conversation_contacts"] |
| B2 | [{"alias": "", "kind": "derived", "block": "B1", "base_tables": ["intercom__conversation_enhanced"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |
| B2 | COUNT(*) | [] | [] | True |


## S30

类别 `data`；来源 `query_db`；调用 `d7a7280a77f64913b87d1a5b3cb4f9ef`；状态 `failed`。

```sql
SELECT conversation_id, conversation_created_at, first_admin_response_at, time_to_first_response_minutes, all_conversation_tags
FROM intercom__conversation_metrics
WHERE conversation_id IN (
  SELECT conversation_id FROM intercom__conversation_enhanced 
  WHERE all_conversation_contacts = 'ffab45627106488abe488ad9'
)
ORDER BY conversation_created_at
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-098/attempt-01/sql/S30.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-098/attempt-01/sql/S30.parameters.json)。

错误：`OperationalError('no such column: all_conversation_tags')`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "intercom__conversation_enhanced", "kind": "base", "block": null, "base_tables": ["intercom__conversation_enhanced"]}] | [] | [] |
| B2 | [{"alias": "intercom__conversation_metrics", "kind": "base", "block": null, "base_tables": ["intercom__conversation_metrics"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |


未解析列血缘：[{"block": "B2", "column": "all_conversation_tags", "reason": "ambiguous_or_missing_source"}, {"block": "B2", "column": "all_conversation_contacts", "reason": "ambiguous_or_missing_source"}]

## S31

类别 `data`；来源 `query_db`；调用 `59e53c0d4c2447928a7e54e60189b12f`；状态 `failed`。

```sql
SELECT conversation_id, conversation_created_at, first_admin_response_at, time_to_first_response_minutes, all_conversation_tags
FROM intercom__conversation_metrics LIMIT 5
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-098/attempt-01/sql/S31.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-098/attempt-01/sql/S31.parameters.json)。

错误：`OperationalError('no such column: all_conversation_tags')`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "intercom__conversation_metrics", "kind": "base", "block": null, "base_tables": ["intercom__conversation_metrics"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |


未解析列血缘：[{"block": "B1", "column": "all_conversation_tags", "reason": "ambiguous_or_missing_source"}]

## S32

类别 `data`；来源 `query_db`；调用 `09d7d0744ad84003a3ac9f084e279b42`；状态 `success`。

```sql
SELECT ce.conversation_id, ce.conversation_created_at, ce.conversation_initiated_type, ce.all_conversation_tags,
       cm.first_admin_response_at, cm.time_to_first_response_minutes
FROM intercom__conversation_enhanced ce
JOIN intercom__conversation_metrics cm ON ce.conversation_id = cm.conversation_id
WHERE ce.all_conversation_contacts = 'ffab45627106488abe488ad9'
ORDER BY ce.conversation_created_at
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-098/attempt-01/sql/S32.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-098/attempt-01/sql/S32.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-098/attempt-01/results/S32.rows.jsonl)；完整：True；SHA256：`daf27ffc31b67f2e309b4abe6d4f8eaeb3fee0d5675c5ca8f6dfea66d28e0e19`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "ce", "kind": "base", "block": null, "base_tables": ["intercom__conversation_enhanced"]}, {"alias": "cm", "kind": "base", "block": null, "base_tables": ["intercom__conversation_metrics"]}] | [{"type": "INNER", "right": "intercom__conversation_metrics AS cm", "on": "ce.conversation_id = cm.conversation_id", "using": []}] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |


## S33

类别 `data`；来源 `query_db`；调用 `a5b968c8a08c4589afde9fffa72c64d2`；状态 `success`。

```sql
SELECT DISTINCT
  CASE WHEN instr(all_conversation_tags,'path:')>0 THEN
    substr(all_conversation_tags, instr(all_conversation_tags,'path:')+5, CASE WHEN instr(substr(all_conversation_tags,instr(all_conversation_tags,'path:')+5),'|')>0 THEN instr(substr(all_conversation_tags,instr(all_conversation_tags,'path:')+5),'|')-1 ELSE length(substr(all_conversation_tags,instr(all_conversation_tags,'path:')+5)) END)
  END AS path,
  CASE WHEN instr(all_conversation_tags,'lifecycle:')>0 THEN
    substr(all_conversation_tags, instr(all_conversation_tags,'lifecycle:')+10, CASE WHEN instr(substr(all_conversation_tags,instr(all_conversation_tags,'lifecycle:')+10),'|')>0 THEN instr(substr(all_conversation_tags,instr(all_conversation_tags,'lifecycle:')+10),'|')-1 ELSE length(substr(all_conversation_tags,instr(all_conversation_tags,'lifecycle:')+10)) END)
  END AS lifecycle,
  COUNT(*) as cnt
FROM intercom__conversation_enhanced
GROUP BY path, lifecycle ORDER BY cnt DESC
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-098/attempt-01/sql/S33.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-098/attempt-01/sql/S33.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-098/attempt-01/results/S33.rows.jsonl)；完整：True；SHA256：`eeb04a0561617c9caf55722588e4e30014097555c8e3dade391965903ed029ca`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "intercom__conversation_enhanced", "kind": "base", "block": null, "base_tables": ["intercom__conversation_enhanced"]}] | [] | ["CASE WHEN INSTR(all_conversation_tags, 'path:') > 0 THEN SUBSTRING(all_conversation_tags, INSTR(all_conversation_tags, 'path:') + 5, CASE WHEN INSTR(SUBSTRING(all_conversation_tags, INSTR(all_conversation_tags, 'path:') + 5), '\|') > 0 THEN INSTR(SUBSTRING(all_conversation_tags, INSTR(all_conversation_tags, 'path:') + 5), '\|') - 1 ELSE LENGTH(SUBSTRING(all_conversation_tags, INSTR(all_conversation_tags, 'path:') + 5)) END) END", "CASE WHEN INSTR(all_conversation_tags, 'lifecycle:') > 0 THEN SUBSTRING(all_conversation_tags, INSTR(all_conversation_tags, 'lifecycle:') + 10, CASE WHEN INSTR(SUBSTRING(all_conversation_tags, INSTR(all_conversation_tags, 'lifecycle:') + 10), '\|') > 0 THEN INSTR(SUBSTRING(all_conversation_tags, INSTR(all_conversation_tags, 'lifecycle:') + 10), '\|') - 1 ELSE LENGTH(SUBSTRING(all_conversation_tags, INSTR(all_conversation_tags, 'lifecycle:') + 10)) END) END"] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |


## S34

类别 `data`；来源 `query_db`；调用 `77b318c185554ce696d743a2cc8c1420`；状态 `success`。

```sql
SELECT DISTINCT
  CASE WHEN instr(all_conversation_tags,'segment:')>0 THEN
    substr(all_conversation_tags, instr(all_conversation_tags,'segment:')+8, CASE WHEN instr(substr(all_conversation_tags,instr(all_conversation_tags,'segment:')+8),'|')>0 THEN instr(substr(all_conversation_tags,instr(all_conversation_tags,'segment:')+8),'|')-1 ELSE length(substr(all_conversation_tags,instr(all_conversation_tags,'segment:')+8)) END)
  END AS segment,
  COUNT(*) as cnt
FROM intercom__conversation_enhanced
GROUP BY segment ORDER BY cnt DESC
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-098/attempt-01/sql/S34.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-098/attempt-01/sql/S34.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-098/attempt-01/results/S34.rows.jsonl)；完整：True；SHA256：`975adb76394a4e628acc766f5eeace0dfa0d9b0a1a6f90e9e76bdfd7f64a45d0`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "intercom__conversation_enhanced", "kind": "base", "block": null, "base_tables": ["intercom__conversation_enhanced"]}] | [] | ["CASE WHEN INSTR(all_conversation_tags, 'segment:') > 0 THEN SUBSTRING(all_conversation_tags, INSTR(all_conversation_tags, 'segment:') + 8, CASE WHEN INSTR(SUBSTRING(all_conversation_tags, INSTR(all_conversation_tags, 'segment:') + 8), '\|') > 0 THEN INSTR(SUBSTRING(all_conversation_tags, INSTR(all_conversation_tags, 'segment:') + 8), '\|') - 1 ELSE LENGTH(SUBSTRING(all_conversation_tags, INSTR(all_conversation_tags, 'segment:') + 8)) END) END"] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |


## S35

类别 `data`；来源 `query_db`；调用 `201b6379c9b14cf09646da6ce0093b9c`；状态 `success`。

```sql
SELECT conversation_initiated_type, 
  CASE WHEN instr(all_conversation_tags,'path:')>0 THEN
    substr(all_conversation_tags, instr(all_conversation_tags,'path:')+5, CASE WHEN instr(substr(all_conversation_tags,instr(all_conversation_tags,'path:')+5),'|')>0 THEN instr(substr(all_conversation_tags,instr(all_conversation_tags,'path:')+5),'|')-1 ELSE length(substr(all_conversation_tags,instr(all_conversation_tags,'path:')+5)) END)
  END AS path_tag,
  COUNT(*) as cnt
FROM intercom__conversation_enhanced
GROUP BY conversation_initiated_type, path_tag
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-098/attempt-01/sql/S35.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-098/attempt-01/sql/S35.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-098/attempt-01/results/S35.rows.jsonl)；完整：True；SHA256：`5b0f5f2a769b73d1c042967ceeb9fc923d0fbcdbaf9f4d8161960c46933cd953`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "intercom__conversation_enhanced", "kind": "base", "block": null, "base_tables": ["intercom__conversation_enhanced"]}] | [] | ["conversation_initiated_type", "CASE WHEN INSTR(all_conversation_tags, 'path:') > 0 THEN SUBSTRING(all_conversation_tags, INSTR(all_conversation_tags, 'path:') + 5, CASE WHEN INSTR(SUBSTRING(all_conversation_tags, INSTR(all_conversation_tags, 'path:') + 5), '\|') > 0 THEN INSTR(SUBSTRING(all_conversation_tags, INSTR(all_conversation_tags, 'path:') + 5), '\|') - 1 ELSE LENGTH(SUBSTRING(all_conversation_tags, INSTR(all_conversation_tags, 'path:') + 5)) END) END"] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |


## S36

类别 `data`；来源 `query_db`；调用 `b36c840f6de848909bc5eaed1ff8e055`；状态 `success`。

```sql
SELECT 
  CASE WHEN instr(all_conversation_tags,'lifecycle:')>0 THEN
    substr(all_conversation_tags, instr(all_conversation_tags,'lifecycle:')+10, CASE WHEN instr(substr(all_conversation_tags,instr(all_conversation_tags,'lifecycle:')+10),'|')>0 THEN instr(substr(all_conversation_tags,instr(all_conversation_tags,'lifecycle:')+10),'|')-1 ELSE length(substr(all_conversation_tags,instr(all_conversation_tags,'lifecycle:')+10)) END)
  END AS lifecycle,
  COUNT(*) as cnt
FROM intercom__conversation_enhanced
GROUP BY lifecycle ORDER BY cnt DESC
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-098/attempt-01/sql/S36.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-098/attempt-01/sql/S36.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-098/attempt-01/results/S36.rows.jsonl)；完整：True；SHA256：`b94c7a4e7cdbb5c3fd4bc0252e2bae8dc8b3c7ec666d880cd0236bd3f288adc8`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "intercom__conversation_enhanced", "kind": "base", "block": null, "base_tables": ["intercom__conversation_enhanced"]}] | [] | ["CASE WHEN INSTR(all_conversation_tags, 'lifecycle:') > 0 THEN SUBSTRING(all_conversation_tags, INSTR(all_conversation_tags, 'lifecycle:') + 10, CASE WHEN INSTR(SUBSTRING(all_conversation_tags, INSTR(all_conversation_tags, 'lifecycle:') + 10), '\|') > 0 THEN INSTR(SUBSTRING(all_conversation_tags, INSTR(all_conversation_tags, 'lifecycle:') + 10), '\|') - 1 ELSE LENGTH(SUBSTRING(all_conversation_tags, INSTR(all_conversation_tags, 'lifecycle:') + 10)) END) END"] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |


## S37

类别 `data`；来源 `query_db`；调用 `fbf7128e96274f5f9e2c85b731fd23a6`；状态 `success`。

```sql
WITH conv AS (
  SELECT 
    ce.all_conversation_contacts AS contact_id,
    ce.conversation_id,
    ce.conversation_created_at,
    ce.conversation_initiated_type,
    cm.first_admin_response_at,
    cm.time_to_first_response_minutes,
    CASE WHEN instr(ce.all_conversation_tags,'stage:')>0 THEN
      substr(ce.all_conversation_tags, instr(ce.all_conversation_tags,'stage:')+6,
        CASE WHEN instr(substr(ce.all_conversation_tags,instr(ce.all_conversation_tags,'stage:')+6),'|')>0
          THEN instr(substr(ce.all_conversation_tags,instr(ce.all_conversation_tags,'stage:')+6),'|')-1
          ELSE length(substr(ce.all_conversation_tags,instr(ce.all_conversation_tags,'stage:')+6)) END)
    END AS stage,
    CASE WHEN instr(ce.all_conversation_tags,'intent:')>0 THEN
      substr(ce.all_conversation_tags, instr(ce.all_conversation_tags,'intent:')+7,
        CASE WHEN instr(substr(ce.all_conversation_tags,instr(ce.all_conversation_tags,'intent:')+7),'|')>0
          THEN instr(substr(ce.all_conversation_tags,instr(ce.all_conversation_tags,'intent:')+7),'|')-1
          ELSE length(substr(ce.all_conversation_tags,instr(ce.all_conversation_tags,'intent:')+7)) END)
    END AS intent,
    CASE WHEN instr(ce.all_conversation_tags,'topic:')>0 THEN
      substr(ce.all_conversation_tags, instr(ce.all_conversation_tags,'topic:')+6,
        CASE WHEN instr(substr(ce.all_conversation_tags,instr(ce.all_conversation_tags,'topic:')+6),'|')>0
          THEN instr(substr(ce.all_conversation_tags,instr(ce.all_conversation_tags,'topic:')+6),'|')-1
          ELSE length(substr(ce.all_conversation_tags,instr(ce.all_conversation_tags,'topic:')+6)) END)
    END AS topic,
    CASE WHEN instr(ce.all_conversation_tags,'region:')>0 THEN
      substr(ce.all_conversation_tags, instr(ce.all_conversation_tags,'region:')+7,
        CASE WHEN instr(substr(ce.all_conversation_tags,instr(ce.all_conversation_tags,'region:')+7),'|')>0
          THEN instr(substr(ce.all_conversation_tags,instr(ce.all_conversation_tags,'region:')+7),'|')-1
          ELSE length(substr(ce.all_conversation_tags,instr(ce.all_conversation_tags,'region:')+7)) END)
    END AS region
  FROM intercom__conversation_enhanced ce
  JOIN intercom__conversation_metrics cm ON ce.conversation_id = cm.conversation_id
),
staged AS (
  SELECT *,
    CASE stage
      WHEN 'contacted' THEN 1
      WHEN 'marketing_qualified' THEN 2
      WHEN 'trial_started' THEN 3
      WHEN 'demo_booked' THEN 4
      WHEN 'trial_activated' THEN 5
      WHEN 'proposal_sent' THEN 6
      WHEN 'closed_won' THEN 7
      WHEN 'expansion_in_flight' THEN 8
      WHEN 'closed_lost' THEN 99
      ELSE 0
    END AS stage_rank
  FROM conv
)
SELECT contact_id,
  MIN(CASE WHEN stage_rank>=1 AND stage_rank<99 THEN stage_rank END) AS min_reached,
  MAX(CASE WHEN stage_rank>=1 AND stage_rank<99 THEN stage_rank END) AS max_reached,
  MIN(CASE WHEN stage_rank=99 THEN 1 ELSE 0 END) AS has_lost,
  COUNT(*) AS n_conv
FROM staged
GROUP BY contact_id
LIMIT 15
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-098/attempt-01/sql/S37.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-098/attempt-01/sql/S37.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-098/attempt-01/results/S37.rows.jsonl)；完整：True；SHA256：`c15f2cf470c601669426cbc632967e62f293ba5a75a5863e0b53230e975ab7cf`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "ce", "kind": "base", "block": null, "base_tables": ["intercom__conversation_enhanced"]}, {"alias": "cm", "kind": "base", "block": null, "base_tables": ["intercom__conversation_metrics"]}] | [{"type": "INNER", "right": "intercom__conversation_metrics AS cm", "on": "ce.conversation_id = cm.conversation_id", "using": []}] | [] |
| B2 | [{"alias": "conv", "kind": "derived", "block": "B1", "base_tables": ["intercom__conversation_enhanced", "intercom__conversation_metrics"]}] | [] | [] |
| B3 | [{"alias": "staged", "kind": "derived", "block": "B2", "base_tables": ["intercom__conversation_enhanced", "intercom__conversation_metrics"]}] | [] | ["contact_id"] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B3 | MIN(CASE WHEN stage_rank >= 1 AND stage_rank < 99 THEN stage_rank END) | [{"table": "intercom__conversation_enhanced", "column": "all_conversation_tags"}, {"table": "intercom__conversation_enhanced", "column": "all_conversation_tags"}, {"table": "intercom__conversation_enhanced", "column": "all_conversation_tags"}, {"table": "intercom__conversation_enhanced", "column": "all_conversation_tags"}, {"table": "intercom__conversation_enhanced", "column": "all_conversation_tags"}, {"table": "intercom__conversation_enhanced", "column": "all_conversation_tags"}, {"table": "intercom__conversation_enhanced", "column": "all_conversation_tags"}, {"table": "intercom__conversation_enhanced", "column": "all_conversation_tags"}, {"table": "intercom__conversation_enhanced", "column": "all_conversation_tags"}] | [{"table": "intercom__conversation_enhanced", "column": "all_conversation_tags"}, {"table": "intercom__conversation_enhanced", "column": "all_conversation_tags"}, {"table": "intercom__conversation_enhanced", "column": "all_conversation_tags"}, {"table": "intercom__conversation_enhanced", "column": "all_conversation_tags"}, {"table": "intercom__conversation_enhanced", "column": "all_conversation_tags"}, {"table": "intercom__conversation_enhanced", "column": "all_conversation_tags"}, {"table": "intercom__conversation_enhanced", "column": "all_conversation_tags"}, {"table": "intercom__conversation_enhanced", "column": "all_conversation_tags"}, {"table": "intercom__conversation_enhanced", "column": "all_conversation_tags"}, {"table": "intercom__conversation_enhanced", "column": "all_conversation_tags"}, {"table": "intercom__conversation_enhanced", "column": "all_conversation_tags"}, {"table": "intercom__conversation_enhanced", "column": "all_conversation_tags"}, {"table": "intercom__conversation_enhanced", "column": "all_conversation_tags"}, {"table": "intercom__conversation_enhanced", "column": "all_conversation_tags"}, {"table": "intercom__conversation_enhanced", "column": "all_conversation_tags"}, {"table": "intercom__conversation_enhanced", "column": "all_conversation_tags"}, {"table": "intercom__conversation_enhanced", "column": "all_conversation_tags"}, {"table": "intercom__conversation_enhanced", "column": "all_conversation_tags"}] | False |
| B3 | MAX(CASE WHEN stage_rank >= 1 AND stage_rank < 99 THEN stage_rank END) | [{"table": "intercom__conversation_enhanced", "column": "all_conversation_tags"}, {"table": "intercom__conversation_enhanced", "column": "all_conversation_tags"}, {"table": "intercom__conversation_enhanced", "column": "all_conversation_tags"}, {"table": "intercom__conversation_enhanced", "column": "all_conversation_tags"}, {"table": "intercom__conversation_enhanced", "column": "all_conversation_tags"}, {"table": "intercom__conversation_enhanced", "column": "all_conversation_tags"}, {"table": "intercom__conversation_enhanced", "column": "all_conversation_tags"}, {"table": "intercom__conversation_enhanced", "column": "all_conversation_tags"}, {"table": "intercom__conversation_enhanced", "column": "all_conversation_tags"}] | [{"table": "intercom__conversation_enhanced", "column": "all_conversation_tags"}, {"table": "intercom__conversation_enhanced", "column": "all_conversation_tags"}, {"table": "intercom__conversation_enhanced", "column": "all_conversation_tags"}, {"table": "intercom__conversation_enhanced", "column": "all_conversation_tags"}, {"table": "intercom__conversation_enhanced", "column": "all_conversation_tags"}, {"table": "intercom__conversation_enhanced", "column": "all_conversation_tags"}, {"table": "intercom__conversation_enhanced", "column": "all_conversation_tags"}, {"table": "intercom__conversation_enhanced", "column": "all_conversation_tags"}, {"table": "intercom__conversation_enhanced", "column": "all_conversation_tags"}, {"table": "intercom__conversation_enhanced", "column": "all_conversation_tags"}, {"table": "intercom__conversation_enhanced", "column": "all_conversation_tags"}, {"table": "intercom__conversation_enhanced", "column": "all_conversation_tags"}, {"table": "intercom__conversation_enhanced", "column": "all_conversation_tags"}, {"table": "intercom__conversation_enhanced", "column": "all_conversation_tags"}, {"table": "intercom__conversation_enhanced", "column": "all_conversation_tags"}, {"table": "intercom__conversation_enhanced", "column": "all_conversation_tags"}, {"table": "intercom__conversation_enhanced", "column": "all_conversation_tags"}, {"table": "intercom__conversation_enhanced", "column": "all_conversation_tags"}] | False |
| B3 | MIN(CASE WHEN stage_rank = 99 THEN 1 ELSE 0 END) | [] | [{"table": "intercom__conversation_enhanced", "column": "all_conversation_tags"}, {"table": "intercom__conversation_enhanced", "column": "all_conversation_tags"}, {"table": "intercom__conversation_enhanced", "column": "all_conversation_tags"}, {"table": "intercom__conversation_enhanced", "column": "all_conversation_tags"}, {"table": "intercom__conversation_enhanced", "column": "all_conversation_tags"}, {"table": "intercom__conversation_enhanced", "column": "all_conversation_tags"}, {"table": "intercom__conversation_enhanced", "column": "all_conversation_tags"}, {"table": "intercom__conversation_enhanced", "column": "all_conversation_tags"}, {"table": "intercom__conversation_enhanced", "column": "all_conversation_tags"}] | False |
| B3 | COUNT(*) | [] | [] | True |


## S38

类别 `data`；来源 `query_db`；调用 `a9417957f0264258855ac499347f1517`；状态 `success`。

```sql
WITH conv AS (
  SELECT 
    ce.all_conversation_contacts AS contact_id,
    ce.conversation_id,
    ce.conversation_created_at,
    ce.conversation_initiated_type,
    cm.first_admin_response_at,
    cm.time_to_first_response_minutes,
    CASE WHEN instr(ce.all_conversation_tags,'stage:')>0 THEN
      substr(ce.all_conversation_tags, instr(ce.all_conversation_tags,'stage:')+6,
        CASE WHEN instr(substr(ce.all_conversation_tags,instr(ce.all_conversation_tags,'stage:')+6),'|')>0
          THEN instr(substr(ce.all_conversation_tags,instr(ce.all_conversation_tags,'stage:')+6),'|')-1
          ELSE length(substr(ce.all_conversation_tags,instr(ce.all_conversation_tags,'stage:')+6)) END)
    END AS stage,
    CASE WHEN instr(ce.all_conversation_tags,'intent:')>0 THEN
      substr(ce.all_conversation_tags, instr(ce.all_conversation_tags,'intent:')+7,
        CASE WHEN instr(substr(ce.all_conversation_tags,instr(ce.all_conversation_tags,'intent:')+7),'|')>0
          THEN instr(substr(ce.all_conversation_tags,instr(ce.all_conversation_tags,'intent:')+7),'|')-1
          ELSE length(substr(ce.all_conversation_tags,instr(ce.all_conversation_tags,'intent:')+7)) END)
    END AS intent,
    CASE WHEN instr(ce.all_conversation_tags,'topic:')>0 THEN
      substr(ce.all_conversation_tags, instr(ce.all_conversation_tags,'topic:')+6,
        CASE WHEN instr(substr(ce.all_conversation_tags,instr(ce.all_conversation_tags,'topic:')+6),'|')>0
          THEN instr(substr(ce.all_conversation_tags,instr(ce.all_conversation_tags,'topic:')+6),'|')-1
          ELSE length(substr(ce.all_conversation_tags,instr(ce.all_conversation_tags,'topic:')+6)) END)
    END AS topic,
    CASE WHEN instr(ce.all_conversation_tags,'region:')>0 THEN
      substr(ce.all_conversation_tags, instr(ce.all_conversation_tags,'region:')+7,
        CASE WHEN instr(substr(ce.all_conversation_tags,instr(ce.all_conversation_tags,'region:')+7),'|')>0
          THEN instr(substr(ce.all_conversation_tags,instr(ce.all_conversation_tags,'region:')+7),'|')-1
          ELSE length(substr(ce.all_conversation_tags,instr(ce.all_conversation_tags,'region:')+7)) END)
    END AS region,
    CASE WHEN instr(ce.all_conversation_tags,'segment:')>0 THEN
      substr(ce.all_conversation_tags, instr(ce.all_conversation_tags,'segment:')+8,
        CASE WHEN instr(substr(ce.all_conversation_tags,instr(ce.all_conversation_tags,'segment:')+8),'|')>0
          THEN instr(substr(ce.all_conversation_tags,instr(ce.all_conversation_tags,'segment:')+8),'|')-1
          ELSE length(substr(ce.all_conversation_tags,instr(ce.all_conversation_tags,'segment:')+8)) END)
    END AS segment
  FROM intercom__conversation_enhanced ce
  JOIN intercom__conversation_metrics cm ON ce.conversation_id = cm.conversation_id
),
staged AS (
  SELECT *,
    CASE stage
      WHEN 'contacted' THEN 1
      WHEN 'marketing_qualified' THEN 2
      WHEN 'trial_started' THEN 3
      WHEN 'demo_booked' THEN 4
      WHEN 'trial_activated' THEN 5
      WHEN 'proposal_sent' THEN 6
      WHEN 'closed_won' THEN 7
      WHEN 'expansion_in_flight' THEN 8
      WHEN 'closed_lost' THEN 99
      ELSE 0
    END AS stage_rank
  FROM conv
),
first_contact AS (
  SELECT contact_id, ROW_NUMBER() OVER (PARTITION BY contact_id ORDER BY conversation_created_at) AS rn,
    conversation_created_at AS first_conv_at,
    conversation_initiated_type AS first_type,
    first_admin_response_at AS first_response_at,
    time_to_first_response_minutes AS first_response_mins,
    stage, stage_rank, intent, topic, region, segment
  FROM staged
),
first_conv AS (
  SELECT * FROM first_contact WHERE rn = 1
),
milestones AS (
  SELECT contact_id,
    MAX(CASE WHEN stage_rank>=1 AND stage_rank<99 THEN stage_rank END) AS max_stage_rank,
    MIN(CASE WHEN stage_rank>=4 AND stage_rank<99 THEN conversation_created_at END) AS demo_booked_at,
    MIN(CASE WHEN stage_rank>=5 AND stage_rank<99 THEN conversation_created_at END) AS trial_activated_at,
    MIN(CASE WHEN stage_rank>=7 AND stage_rank<99 THEN conversation_created_at END) AS paid_at
  FROM staged
  GROUP BY contact_id
)
SELECT 
  fc.contact_id,
  fc.first_type,
  fc.first_conv_at,
  fc.first_response_at,
  fc.first_response_mins,
  fc.intent,
  fc.topic,
  fc.region,
  fc.segment,
  fc.stage AS first_stage,
  fc.stage_rank AS first_stage_rank,
  ms.max_stage_rank,
  ms.demo_booked_at,
  ms.trial_activated_at,
  ms.paid_at,
  CASE WHEN ms.demo_booked_at IS NOT NULL THEN 1 ELSE 0 END AS reached_demo,
  CASE WHEN ms.trial_activated_at IS NOT NULL THEN 1 ELSE 0 END AS reached_trial,
  CASE WHEN ms.paid_at IS NOT NULL THEN 1 ELSE 0 END AS reached_paid
FROM first_conv fc
LEFT JOIN milestones ms ON fc.contact_id = ms.contact_id
ORDER BY fc.contact_id
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-098/attempt-01/sql/S38.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-098/attempt-01/sql/S38.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-098/attempt-01/results/S38.rows.jsonl)；完整：True；SHA256：`e5b1af3aa64d3e43bcfa0659b167953ab4945a6d56b9e29eb43ebdaa13b444af`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "ce", "kind": "base", "block": null, "base_tables": ["intercom__conversation_enhanced"]}, {"alias": "cm", "kind": "base", "block": null, "base_tables": ["intercom__conversation_metrics"]}] | [{"type": "INNER", "right": "intercom__conversation_metrics AS cm", "on": "ce.conversation_id = cm.conversation_id", "using": []}] | [] |
| B2 | [{"alias": "conv", "kind": "derived", "block": "B1", "base_tables": ["intercom__conversation_enhanced", "intercom__conversation_metrics"]}] | [] | [] |
| B3 | [{"alias": "staged", "kind": "derived", "block": "B2", "base_tables": ["intercom__conversation_enhanced", "intercom__conversation_metrics"]}] | [] | [] |
| B4 | [{"alias": "first_contact", "kind": "derived", "block": "B3", "base_tables": ["intercom__conversation_enhanced", "intercom__conversation_metrics"]}] | [] | [] |
| B5 | [{"alias": "staged", "kind": "derived", "block": "B2", "base_tables": ["intercom__conversation_enhanced", "intercom__conversation_metrics"]}] | [] | ["contact_id"] |
| B6 | [{"alias": "fc", "kind": "derived", "block": "B4", "base_tables": ["intercom__conversation_enhanced", "intercom__conversation_metrics"]}, {"alias": "ms", "kind": "derived", "block": "B5", "base_tables": ["intercom__conversation_enhanced", "intercom__conversation_metrics"]}] | [{"type": "LEFT", "right": "milestones AS ms", "on": "fc.contact_id = ms.contact_id", "using": []}] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B5 | MAX(CASE WHEN stage_rank >= 1 AND stage_rank < 99 THEN stage_rank END) | [{"table": "intercom__conversation_enhanced", "column": "all_conversation_tags"}, {"table": "intercom__conversation_enhanced", "column": "all_conversation_tags"}, {"table": "intercom__conversation_enhanced", "column": "all_conversation_tags"}, {"table": "intercom__conversation_enhanced", "column": "all_conversation_tags"}, {"table": "intercom__conversation_enhanced", "column": "all_conversation_tags"}, {"table": "intercom__conversation_enhanced", "column": "all_conversation_tags"}, {"table": "intercom__conversation_enhanced", "column": "all_conversation_tags"}, {"table": "intercom__conversation_enhanced", "column": "all_conversation_tags"}, {"table": "intercom__conversation_enhanced", "column": "all_conversation_tags"}] | [{"table": "intercom__conversation_enhanced", "column": "all_conversation_tags"}, {"table": "intercom__conversation_enhanced", "column": "all_conversation_tags"}, {"table": "intercom__conversation_enhanced", "column": "all_conversation_tags"}, {"table": "intercom__conversation_enhanced", "column": "all_conversation_tags"}, {"table": "intercom__conversation_enhanced", "column": "all_conversation_tags"}, {"table": "intercom__conversation_enhanced", "column": "all_conversation_tags"}, {"table": "intercom__conversation_enhanced", "column": "all_conversation_tags"}, {"table": "intercom__conversation_enhanced", "column": "all_conversation_tags"}, {"table": "intercom__conversation_enhanced", "column": "all_conversation_tags"}, {"table": "intercom__conversation_enhanced", "column": "all_conversation_tags"}, {"table": "intercom__conversation_enhanced", "column": "all_conversation_tags"}, {"table": "intercom__conversation_enhanced", "column": "all_conversation_tags"}, {"table": "intercom__conversation_enhanced", "column": "all_conversation_tags"}, {"table": "intercom__conversation_enhanced", "column": "all_conversation_tags"}, {"table": "intercom__conversation_enhanced", "column": "all_conversation_tags"}, {"table": "intercom__conversation_enhanced", "column": "all_conversation_tags"}, {"table": "intercom__conversation_enhanced", "column": "all_conversation_tags"}, {"table": "intercom__conversation_enhanced", "column": "all_conversation_tags"}] | False |
| B5 | MIN(CASE WHEN stage_rank >= 4 AND stage_rank < 99 THEN conversation_created_at END) | [{"table": "intercom__conversation_enhanced", "column": "conversation_created_at"}] | [{"table": "intercom__conversation_enhanced", "column": "all_conversation_tags"}, {"table": "intercom__conversation_enhanced", "column": "all_conversation_tags"}, {"table": "intercom__conversation_enhanced", "column": "all_conversation_tags"}, {"table": "intercom__conversation_enhanced", "column": "all_conversation_tags"}, {"table": "intercom__conversation_enhanced", "column": "all_conversation_tags"}, {"table": "intercom__conversation_enhanced", "column": "all_conversation_tags"}, {"table": "intercom__conversation_enhanced", "column": "all_conversation_tags"}, {"table": "intercom__conversation_enhanced", "column": "all_conversation_tags"}, {"table": "intercom__conversation_enhanced", "column": "all_conversation_tags"}, {"table": "intercom__conversation_enhanced", "column": "all_conversation_tags"}, {"table": "intercom__conversation_enhanced", "column": "all_conversation_tags"}, {"table": "intercom__conversation_enhanced", "column": "all_conversation_tags"}, {"table": "intercom__conversation_enhanced", "column": "all_conversation_tags"}, {"table": "intercom__conversation_enhanced", "column": "all_conversation_tags"}, {"table": "intercom__conversation_enhanced", "column": "all_conversation_tags"}, {"table": "intercom__conversation_enhanced", "column": "all_conversation_tags"}, {"table": "intercom__conversation_enhanced", "column": "all_conversation_tags"}, {"table": "intercom__conversation_enhanced", "column": "all_conversation_tags"}] | False |
| B5 | MIN(CASE WHEN stage_rank >= 5 AND stage_rank < 99 THEN conversation_created_at END) | [{"table": "intercom__conversation_enhanced", "column": "conversation_created_at"}] | [{"table": "intercom__conversation_enhanced", "column": "all_conversation_tags"}, {"table": "intercom__conversation_enhanced", "column": "all_conversation_tags"}, {"table": "intercom__conversation_enhanced", "column": "all_conversation_tags"}, {"table": "intercom__conversation_enhanced", "column": "all_conversation_tags"}, {"table": "intercom__conversation_enhanced", "column": "all_conversation_tags"}, {"table": "intercom__conversation_enhanced", "column": "all_conversation_tags"}, {"table": "intercom__conversation_enhanced", "column": "all_conversation_tags"}, {"table": "intercom__conversation_enhanced", "column": "all_conversation_tags"}, {"table": "intercom__conversation_enhanced", "column": "all_conversation_tags"}, {"table": "intercom__conversation_enhanced", "column": "all_conversation_tags"}, {"table": "intercom__conversation_enhanced", "column": "all_conversation_tags"}, {"table": "intercom__conversation_enhanced", "column": "all_conversation_tags"}, {"table": "intercom__conversation_enhanced", "column": "all_conversation_tags"}, {"table": "intercom__conversation_enhanced", "column": "all_conversation_tags"}, {"table": "intercom__conversation_enhanced", "column": "all_conversation_tags"}, {"table": "intercom__conversation_enhanced", "column": "all_conversation_tags"}, {"table": "intercom__conversation_enhanced", "column": "all_conversation_tags"}, {"table": "intercom__conversation_enhanced", "column": "all_conversation_tags"}] | False |
| B5 | MIN(CASE WHEN stage_rank >= 7 AND stage_rank < 99 THEN conversation_created_at END) | [{"table": "intercom__conversation_enhanced", "column": "conversation_created_at"}] | [{"table": "intercom__conversation_enhanced", "column": "all_conversation_tags"}, {"table": "intercom__conversation_enhanced", "column": "all_conversation_tags"}, {"table": "intercom__conversation_enhanced", "column": "all_conversation_tags"}, {"table": "intercom__conversation_enhanced", "column": "all_conversation_tags"}, {"table": "intercom__conversation_enhanced", "column": "all_conversation_tags"}, {"table": "intercom__conversation_enhanced", "column": "all_conversation_tags"}, {"table": "intercom__conversation_enhanced", "column": "all_conversation_tags"}, {"table": "intercom__conversation_enhanced", "column": "all_conversation_tags"}, {"table": "intercom__conversation_enhanced", "column": "all_conversation_tags"}, {"table": "intercom__conversation_enhanced", "column": "all_conversation_tags"}, {"table": "intercom__conversation_enhanced", "column": "all_conversation_tags"}, {"table": "intercom__conversation_enhanced", "column": "all_conversation_tags"}, {"table": "intercom__conversation_enhanced", "column": "all_conversation_tags"}, {"table": "intercom__conversation_enhanced", "column": "all_conversation_tags"}, {"table": "intercom__conversation_enhanced", "column": "all_conversation_tags"}, {"table": "intercom__conversation_enhanced", "column": "all_conversation_tags"}, {"table": "intercom__conversation_enhanced", "column": "all_conversation_tags"}, {"table": "intercom__conversation_enhanced", "column": "all_conversation_tags"}] | False |


## S39

类别 `data`；来源 `python`；调用 `220e6179c41b4d2598d7a1526a6ec8a1`；状态 `success`。

```sql

WITH conv AS (
  SELECT 
    ce.all_conversation_contacts AS contact_id,
    ce.conversation_id,
    ce.conversation_created_at,
    ce.conversation_initiated_type,
    cm.first_admin_response_at,
    cm.time_to_first_response_minutes,
    CASE WHEN instr(ce.all_conversation_tags,'stage:')>0 THEN
      substr(ce.all_conversation_tags, instr(ce.all_conversation_tags,'stage:')+6,
        CASE WHEN instr(substr(ce.all_conversation_tags,instr(ce.all_conversation_tags,'stage:')+6),'|')>0
          THEN instr(substr(ce.all_conversation_tags,instr(ce.all_conversation_tags,'stage:')+6),'|')-1
          ELSE length(substr(ce.all_conversation_tags,instr(ce.all_conversation_tags,'stage:')+6)) END)
    END AS stage,
    CASE WHEN instr(ce.all_conversation_tags,'intent:')>0 THEN
      substr(ce.all_conversation_tags, instr(ce.all_conversation_tags,'intent:')+7,
        CASE WHEN instr(substr(ce.all_conversation_tags,instr(ce.all_conversation_tags,'intent:')+7),'|')>0
          THEN instr(substr(ce.all_conversation_tags,instr(ce.all_conversation_tags,'intent:')+7),'|')-1
          ELSE length(substr(ce.all_conversation_tags,instr(ce.all_conversation_tags,'intent:')+7)) END)
    END AS intent,
    CASE WHEN instr(ce.all_conversation_tags,'topic:')>0 THEN
      substr(ce.all_conversation_tags, instr(ce.all_conversation_tags,'topic:')+6,
        CASE WHEN instr(substr(ce.all_conversation_tags,instr(ce.all_conversation_tags,'topic:')+6),'|')>0
          THEN instr(substr(ce.all_conversation_tags,instr(ce.all_conversation_tags,'topic:')+6),'|')-1
          ELSE length(substr(ce.all_conversation_tags,instr(ce.all_conversation_tags,'topic:')+6)) END)
    END AS topic,
    CASE WHEN instr(ce.all_conversation_tags,'region:')>0 THEN
      substr(ce.all_conversation_tags, instr(ce.all_conversation_tags,'region:')+7,
        CASE WHEN instr(substr(ce.all_conversation_tags,instr(ce.all_conversation_tags,'region:')+7),'|')>0
          THEN instr(substr(ce.all_conversation_tags,instr(ce.all_conversation_tags,'region:')+7),'|')-1
          ELSE length(substr(ce.all_conversation_tags,instr(ce.all_conversation_tags,'region:')+7)) END)
    END AS region,
    CASE WHEN instr(ce.all_conversation_tags,'segment:')>0 THEN
      substr(ce.all_conversation_tags, instr(ce.all_conversation_tags,'segment:')+8,
        CASE WHEN instr(substr(ce.all_conversation_tags,instr(ce.all_conversation_tags,'segment:')+8),'|')>0
          THEN instr(substr(ce.all_conversation_tags,instr(ce.all_conversation_tags,'segment:')+8),'|')-1
          ELSE length(substr(ce.all_conversation_tags,instr(ce.all_conversation_tags,'segment:')+8)) END)
    END AS segment
  FROM intercom__conversation_enhanced ce
  JOIN intercom__conversation_metrics cm ON ce.conversation_id = cm.conversation_id
),
staged AS (
  SELECT *,
    CASE stage
      WHEN 'contacted' THEN 1
      WHEN 'marketing_qualified' THEN 2
      WHEN 'trial_started' THEN 3
      WHEN 'demo_booked' THEN 4
      WHEN 'trial_activated' THEN 5
      WHEN 'proposal_sent' THEN 6
      WHEN 'closed_won' THEN 7
      WHEN 'expansion_in_flight' THEN 8
      WHEN 'closed_lost' THEN 99
      ELSE 0
    END AS stage_rank
  FROM conv
),
first_ranked AS (
  SELECT contact_id, ROW_NUMBER() OVER (PARTITION BY contact_id ORDER BY conversation_created_at) AS rn,
    conversation_created_at AS first_conv_at,
    conversation_initiated_type AS first_type,
    first_admin_response_at AS first_response_at,
    time_to_first_response_minutes AS first_response_mins,
    stage, stage_rank, intent, topic, region, segment
  FROM staged
),
first_conv AS (
  SELECT * FROM first_ranked WHERE rn = 1
),
milestones AS (
  SELECT contact_id,
    MAX(CASE WHEN stage_rank>=1 AND stage_rank<99 THEN stage_rank END) AS max_stage_rank,
    MIN(CASE WHEN stage_rank>=4 AND stage_rank<99 THEN conversation_created_at END) AS demo_booked_at,
    MIN(CASE WHEN stage_rank>=5 AND stage_rank<99 THEN conversation_created_at END) AS trial_activated_at,
    MIN(CASE WHEN stage_rank>=7 AND stage_rank<99 THEN conversation_created_at END) AS paid_at
  FROM staged
  GROUP BY contact_id
)
SELECT 
  fc.contact_id,
  fc.first_type,
  fc.first_conv_at,
  fc.first_response_at,
  fc.first_response_mins,
  fc.intent,
  fc.topic,
  fc.region,
  fc.segment,
  fc.stage AS first_stage,
  fc.stage_rank AS first_stage_rank,
  ms.max_stage_rank,
  ms.demo_booked_at,
  ms.trial_activated_at,
  ms.paid_at,
  CASE WHEN ms.demo_booked_at IS NOT NULL THEN 1 ELSE 0 END AS reached_demo,
  CASE WHEN ms.trial_activated_at IS NOT NULL THEN 1 ELSE 0 END AS reached_trial,
  CASE WHEN ms.paid_at IS NOT NULL THEN 1 ELSE 0 END AS reached_paid
FROM first_conv fc
LEFT JOIN milestones ms ON fc.contact_id = ms.contact_id
ORDER BY fc.contact_id

```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-098/attempt-01/sql/S39.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-098/attempt-01/sql/S39.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-098/attempt-01/results/S39.rows.jsonl)；完整：True；SHA256：`e5b1af3aa64d3e43bcfa0659b167953ab4945a6d56b9e29eb43ebdaa13b444af`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "ce", "kind": "base", "block": null, "base_tables": ["intercom__conversation_enhanced"]}, {"alias": "cm", "kind": "base", "block": null, "base_tables": ["intercom__conversation_metrics"]}] | [{"type": "INNER", "right": "intercom__conversation_metrics AS cm", "on": "ce.conversation_id = cm.conversation_id", "using": []}] | [] |
| B2 | [{"alias": "conv", "kind": "derived", "block": "B1", "base_tables": ["intercom__conversation_enhanced", "intercom__conversation_metrics"]}] | [] | [] |
| B3 | [{"alias": "staged", "kind": "derived", "block": "B2", "base_tables": ["intercom__conversation_enhanced", "intercom__conversation_metrics"]}] | [] | [] |
| B4 | [{"alias": "first_ranked", "kind": "derived", "block": "B3", "base_tables": ["intercom__conversation_enhanced", "intercom__conversation_metrics"]}] | [] | [] |
| B5 | [{"alias": "staged", "kind": "derived", "block": "B2", "base_tables": ["intercom__conversation_enhanced", "intercom__conversation_metrics"]}] | [] | ["contact_id"] |
| B6 | [{"alias": "fc", "kind": "derived", "block": "B4", "base_tables": ["intercom__conversation_enhanced", "intercom__conversation_metrics"]}, {"alias": "ms", "kind": "derived", "block": "B5", "base_tables": ["intercom__conversation_enhanced", "intercom__conversation_metrics"]}] | [{"type": "LEFT", "right": "milestones AS ms", "on": "fc.contact_id = ms.contact_id", "using": []}] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B5 | MAX(CASE WHEN stage_rank >= 1 AND stage_rank < 99 THEN stage_rank END) | [{"table": "intercom__conversation_enhanced", "column": "all_conversation_tags"}, {"table": "intercom__conversation_enhanced", "column": "all_conversation_tags"}, {"table": "intercom__conversation_enhanced", "column": "all_conversation_tags"}, {"table": "intercom__conversation_enhanced", "column": "all_conversation_tags"}, {"table": "intercom__conversation_enhanced", "column": "all_conversation_tags"}, {"table": "intercom__conversation_enhanced", "column": "all_conversation_tags"}, {"table": "intercom__conversation_enhanced", "column": "all_conversation_tags"}, {"table": "intercom__conversation_enhanced", "column": "all_conversation_tags"}, {"table": "intercom__conversation_enhanced", "column": "all_conversation_tags"}] | [{"table": "intercom__conversation_enhanced", "column": "all_conversation_tags"}, {"table": "intercom__conversation_enhanced", "column": "all_conversation_tags"}, {"table": "intercom__conversation_enhanced", "column": "all_conversation_tags"}, {"table": "intercom__conversation_enhanced", "column": "all_conversation_tags"}, {"table": "intercom__conversation_enhanced", "column": "all_conversation_tags"}, {"table": "intercom__conversation_enhanced", "column": "all_conversation_tags"}, {"table": "intercom__conversation_enhanced", "column": "all_conversation_tags"}, {"table": "intercom__conversation_enhanced", "column": "all_conversation_tags"}, {"table": "intercom__conversation_enhanced", "column": "all_conversation_tags"}, {"table": "intercom__conversation_enhanced", "column": "all_conversation_tags"}, {"table": "intercom__conversation_enhanced", "column": "all_conversation_tags"}, {"table": "intercom__conversation_enhanced", "column": "all_conversation_tags"}, {"table": "intercom__conversation_enhanced", "column": "all_conversation_tags"}, {"table": "intercom__conversation_enhanced", "column": "all_conversation_tags"}, {"table": "intercom__conversation_enhanced", "column": "all_conversation_tags"}, {"table": "intercom__conversation_enhanced", "column": "all_conversation_tags"}, {"table": "intercom__conversation_enhanced", "column": "all_conversation_tags"}, {"table": "intercom__conversation_enhanced", "column": "all_conversation_tags"}] | False |
| B5 | MIN(CASE WHEN stage_rank >= 4 AND stage_rank < 99 THEN conversation_created_at END) | [{"table": "intercom__conversation_enhanced", "column": "conversation_created_at"}] | [{"table": "intercom__conversation_enhanced", "column": "all_conversation_tags"}, {"table": "intercom__conversation_enhanced", "column": "all_conversation_tags"}, {"table": "intercom__conversation_enhanced", "column": "all_conversation_tags"}, {"table": "intercom__conversation_enhanced", "column": "all_conversation_tags"}, {"table": "intercom__conversation_enhanced", "column": "all_conversation_tags"}, {"table": "intercom__conversation_enhanced", "column": "all_conversation_tags"}, {"table": "intercom__conversation_enhanced", "column": "all_conversation_tags"}, {"table": "intercom__conversation_enhanced", "column": "all_conversation_tags"}, {"table": "intercom__conversation_enhanced", "column": "all_conversation_tags"}, {"table": "intercom__conversation_enhanced", "column": "all_conversation_tags"}, {"table": "intercom__conversation_enhanced", "column": "all_conversation_tags"}, {"table": "intercom__conversation_enhanced", "column": "all_conversation_tags"}, {"table": "intercom__conversation_enhanced", "column": "all_conversation_tags"}, {"table": "intercom__conversation_enhanced", "column": "all_conversation_tags"}, {"table": "intercom__conversation_enhanced", "column": "all_conversation_tags"}, {"table": "intercom__conversation_enhanced", "column": "all_conversation_tags"}, {"table": "intercom__conversation_enhanced", "column": "all_conversation_tags"}, {"table": "intercom__conversation_enhanced", "column": "all_conversation_tags"}] | False |
| B5 | MIN(CASE WHEN stage_rank >= 5 AND stage_rank < 99 THEN conversation_created_at END) | [{"table": "intercom__conversation_enhanced", "column": "conversation_created_at"}] | [{"table": "intercom__conversation_enhanced", "column": "all_conversation_tags"}, {"table": "intercom__conversation_enhanced", "column": "all_conversation_tags"}, {"table": "intercom__conversation_enhanced", "column": "all_conversation_tags"}, {"table": "intercom__conversation_enhanced", "column": "all_conversation_tags"}, {"table": "intercom__conversation_enhanced", "column": "all_conversation_tags"}, {"table": "intercom__conversation_enhanced", "column": "all_conversation_tags"}, {"table": "intercom__conversation_enhanced", "column": "all_conversation_tags"}, {"table": "intercom__conversation_enhanced", "column": "all_conversation_tags"}, {"table": "intercom__conversation_enhanced", "column": "all_conversation_tags"}, {"table": "intercom__conversation_enhanced", "column": "all_conversation_tags"}, {"table": "intercom__conversation_enhanced", "column": "all_conversation_tags"}, {"table": "intercom__conversation_enhanced", "column": "all_conversation_tags"}, {"table": "intercom__conversation_enhanced", "column": "all_conversation_tags"}, {"table": "intercom__conversation_enhanced", "column": "all_conversation_tags"}, {"table": "intercom__conversation_enhanced", "column": "all_conversation_tags"}, {"table": "intercom__conversation_enhanced", "column": "all_conversation_tags"}, {"table": "intercom__conversation_enhanced", "column": "all_conversation_tags"}, {"table": "intercom__conversation_enhanced", "column": "all_conversation_tags"}] | False |
| B5 | MIN(CASE WHEN stage_rank >= 7 AND stage_rank < 99 THEN conversation_created_at END) | [{"table": "intercom__conversation_enhanced", "column": "conversation_created_at"}] | [{"table": "intercom__conversation_enhanced", "column": "all_conversation_tags"}, {"table": "intercom__conversation_enhanced", "column": "all_conversation_tags"}, {"table": "intercom__conversation_enhanced", "column": "all_conversation_tags"}, {"table": "intercom__conversation_enhanced", "column": "all_conversation_tags"}, {"table": "intercom__conversation_enhanced", "column": "all_conversation_tags"}, {"table": "intercom__conversation_enhanced", "column": "all_conversation_tags"}, {"table": "intercom__conversation_enhanced", "column": "all_conversation_tags"}, {"table": "intercom__conversation_enhanced", "column": "all_conversation_tags"}, {"table": "intercom__conversation_enhanced", "column": "all_conversation_tags"}, {"table": "intercom__conversation_enhanced", "column": "all_conversation_tags"}, {"table": "intercom__conversation_enhanced", "column": "all_conversation_tags"}, {"table": "intercom__conversation_enhanced", "column": "all_conversation_tags"}, {"table": "intercom__conversation_enhanced", "column": "all_conversation_tags"}, {"table": "intercom__conversation_enhanced", "column": "all_conversation_tags"}, {"table": "intercom__conversation_enhanced", "column": "all_conversation_tags"}, {"table": "intercom__conversation_enhanced", "column": "all_conversation_tags"}, {"table": "intercom__conversation_enhanced", "column": "all_conversation_tags"}, {"table": "intercom__conversation_enhanced", "column": "all_conversation_tags"}] | False |


## S40

类别 `data`；来源 `python`；调用 `e2f16b09d3144313b82551ebf3ff1b5b`；状态 `success`。

```sql

WITH conv AS (
  SELECT 
    ce.all_conversation_contacts AS contact_id,
    ce.conversation_id,
    ce.conversation_created_at,
    ce.conversation_initiated_type,
    cm.first_admin_response_at,
    cm.time_to_first_response_minutes,
    CASE WHEN instr(ce.all_conversation_tags,'stage:')>0 THEN
      substr(ce.all_conversation_tags, instr(ce.all_conversation_tags,'stage:')+6,
        CASE WHEN instr(substr(ce.all_conversation_tags,instr(ce.all_conversation_tags,'stage:')+6),'|')>0
          THEN instr(substr(ce.all_conversation_tags,instr(ce.all_conversation_tags,'stage:')+6),'|')-1
          ELSE length(substr(ce.all_conversation_tags,instr(ce.all_conversation_tags,'stage:')+6)) END)
    END AS stage,
    CASE WHEN instr(ce.all_conversation_tags,'intent:')>0 THEN
      substr(ce.all_conversation_tags, instr(ce.all_conversation_tags,'intent:')+7,
        CASE WHEN instr(substr(ce.all_conversation_tags,instr(ce.all_conversation_tags,'intent:')+7),'|')>0
          THEN instr(substr(ce.all_conversation_tags,instr(ce.all_conversation_tags,'intent:')+7),'|')-1
          ELSE length(substr(ce.all_conversation_tags,instr(ce.all_conversation_tags,'intent:')+7)) END)
    END AS intent,
    CASE WHEN instr(ce.all_conversation_tags,'topic:')>0 THEN
      substr(ce.all_conversation_tags, instr(ce.all_conversation_tags,'topic:')+6,
        CASE WHEN instr(substr(ce.all_conversation_tags,instr(ce.all_conversation_tags,'topic:')+6),'|')>0
          THEN instr(substr(ce.all_conversation_tags,instr(ce.all_conversation_tags,'topic:')+6),'|')-1
          ELSE length(substr(ce.all_conversation_tags,instr(ce.all_conversation_tags,'topic:')+6)) END)
    END AS topic,
    CASE WHEN instr(ce.all_conversation_tags,'region:')>0 THEN
      substr(ce.all_conversation_tags, instr(ce.all_conversation_tags,'region:')+7,
        CASE WHEN instr(substr(ce.all_conversation_tags,instr(ce.all_conversation_tags,'region:')+7),'|')>0
          THEN instr(substr(ce.all_conversation_tags,instr(ce.all_conversation_tags,'region:')+7),'|')-1
          ELSE length(substr(ce.all_conversation_tags,instr(ce.all_conversation_tags,'region:')+7)) END)
    END AS region,
    CASE WHEN instr(ce.all_conversation_tags,'segment:')>0 THEN
      substr(ce.all_conversation_tags, instr(ce.all_conversation_tags,'segment:')+8,
        CASE WHEN instr(substr(ce.all_conversation_tags,instr(ce.all_conversation_tags,'segment:')+8),'|')>0
          THEN instr(substr(ce.all_conversation_tags,instr(ce.all_conversation_tags,'segment:')+8),'|')-1
          ELSE length(substr(ce.all_conversation_tags,instr(ce.all_conversation_tags,'segment:')+8)) END)
    END AS segment
  FROM intercom__conversation_enhanced ce
  JOIN intercom__conversation_metrics cm ON ce.conversation_id = cm.conversation_id
),
staged AS (
  SELECT *,
    CASE stage
      WHEN 'contacted' THEN 1
      WHEN 'marketing_qualified' THEN 2
      WHEN 'trial_started' THEN 3
      WHEN 'demo_booked' THEN 4
      WHEN 'trial_activated' THEN 5
      WHEN 'proposal_sent' THEN 6
      WHEN 'closed_won' THEN 7
      WHEN 'expansion_in_flight' THEN 8
      WHEN 'closed_lost' THEN 99
      ELSE 0
    END AS stage_rank
  FROM conv
),
first_ranked AS (
  SELECT contact_id, ROW_NUMBER() OVER (PARTITION BY contact_id ORDER BY conversation_created_at) AS rn,
    conversation_created_at AS first_conv_at,
    conversation_initiated_type AS first_type,
    first_admin_response_at AS first_response_at,
    time_to_first_response_minutes AS first_response_mins,
    stage, stage_rank, intent, topic, region, segment
  FROM staged
),
first_conv AS (
  SELECT * FROM first_ranked WHERE rn = 1
),
milestones AS (
  SELECT contact_id,
    MAX(CASE WHEN stage_rank>=1 AND stage_rank<99 THEN stage_rank END) AS max_stage_rank,
    MIN(CASE WHEN stage_rank>=4 AND stage_rank<99 THEN conversation_created_at END) AS demo_booked_at,
    MIN(CASE WHEN stage_rank>=5 AND stage_rank<99 THEN conversation_created_at END) AS trial_activated_at,
    MIN(CASE WHEN stage_rank>=7 AND stage_rank<99 THEN conversation_created_at END) AS paid_at
  FROM staged
  GROUP BY contact_id
)
SELECT 
  fc.contact_id, fc.first_type, fc.first_conv_at, fc.first_response_at,
  fc.first_response_mins, fc.intent, fc.topic, fc.region, fc.segment,
  fc.stage AS first_stage, fc.stage_rank AS first_stage_rank,
  ms.max_stage_rank, ms.demo_booked_at, ms.trial_activated_at, ms.paid_at,
  CASE WHEN ms.demo_booked_at IS NOT NULL THEN 1 ELSE 0 END AS reached_demo,
  CASE WHEN ms.trial_activated_at IS NOT NULL THEN 1 ELSE 0 END AS reached_trial,
  CASE WHEN ms.paid_at IS NOT NULL THEN 1 ELSE 0 END AS reached_paid
FROM first_conv fc
LEFT JOIN milestones ms ON fc.contact_id = ms.contact_id
ORDER BY fc.contact_id

```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-098/attempt-01/sql/S40.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-098/attempt-01/sql/S40.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-098/attempt-01/results/S40.rows.jsonl)；完整：True；SHA256：`e5b1af3aa64d3e43bcfa0659b167953ab4945a6d56b9e29eb43ebdaa13b444af`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "ce", "kind": "base", "block": null, "base_tables": ["intercom__conversation_enhanced"]}, {"alias": "cm", "kind": "base", "block": null, "base_tables": ["intercom__conversation_metrics"]}] | [{"type": "INNER", "right": "intercom__conversation_metrics AS cm", "on": "ce.conversation_id = cm.conversation_id", "using": []}] | [] |
| B2 | [{"alias": "conv", "kind": "derived", "block": "B1", "base_tables": ["intercom__conversation_enhanced", "intercom__conversation_metrics"]}] | [] | [] |
| B3 | [{"alias": "staged", "kind": "derived", "block": "B2", "base_tables": ["intercom__conversation_enhanced", "intercom__conversation_metrics"]}] | [] | [] |
| B4 | [{"alias": "first_ranked", "kind": "derived", "block": "B3", "base_tables": ["intercom__conversation_enhanced", "intercom__conversation_metrics"]}] | [] | [] |
| B5 | [{"alias": "staged", "kind": "derived", "block": "B2", "base_tables": ["intercom__conversation_enhanced", "intercom__conversation_metrics"]}] | [] | ["contact_id"] |
| B6 | [{"alias": "fc", "kind": "derived", "block": "B4", "base_tables": ["intercom__conversation_enhanced", "intercom__conversation_metrics"]}, {"alias": "ms", "kind": "derived", "block": "B5", "base_tables": ["intercom__conversation_enhanced", "intercom__conversation_metrics"]}] | [{"type": "LEFT", "right": "milestones AS ms", "on": "fc.contact_id = ms.contact_id", "using": []}] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B5 | MAX(CASE WHEN stage_rank >= 1 AND stage_rank < 99 THEN stage_rank END) | [{"table": "intercom__conversation_enhanced", "column": "all_conversation_tags"}, {"table": "intercom__conversation_enhanced", "column": "all_conversation_tags"}, {"table": "intercom__conversation_enhanced", "column": "all_conversation_tags"}, {"table": "intercom__conversation_enhanced", "column": "all_conversation_tags"}, {"table": "intercom__conversation_enhanced", "column": "all_conversation_tags"}, {"table": "intercom__conversation_enhanced", "column": "all_conversation_tags"}, {"table": "intercom__conversation_enhanced", "column": "all_conversation_tags"}, {"table": "intercom__conversation_enhanced", "column": "all_conversation_tags"}, {"table": "intercom__conversation_enhanced", "column": "all_conversation_tags"}] | [{"table": "intercom__conversation_enhanced", "column": "all_conversation_tags"}, {"table": "intercom__conversation_enhanced", "column": "all_conversation_tags"}, {"table": "intercom__conversation_enhanced", "column": "all_conversation_tags"}, {"table": "intercom__conversation_enhanced", "column": "all_conversation_tags"}, {"table": "intercom__conversation_enhanced", "column": "all_conversation_tags"}, {"table": "intercom__conversation_enhanced", "column": "all_conversation_tags"}, {"table": "intercom__conversation_enhanced", "column": "all_conversation_tags"}, {"table": "intercom__conversation_enhanced", "column": "all_conversation_tags"}, {"table": "intercom__conversation_enhanced", "column": "all_conversation_tags"}, {"table": "intercom__conversation_enhanced", "column": "all_conversation_tags"}, {"table": "intercom__conversation_enhanced", "column": "all_conversation_tags"}, {"table": "intercom__conversation_enhanced", "column": "all_conversation_tags"}, {"table": "intercom__conversation_enhanced", "column": "all_conversation_tags"}, {"table": "intercom__conversation_enhanced", "column": "all_conversation_tags"}, {"table": "intercom__conversation_enhanced", "column": "all_conversation_tags"}, {"table": "intercom__conversation_enhanced", "column": "all_conversation_tags"}, {"table": "intercom__conversation_enhanced", "column": "all_conversation_tags"}, {"table": "intercom__conversation_enhanced", "column": "all_conversation_tags"}] | False |
| B5 | MIN(CASE WHEN stage_rank >= 4 AND stage_rank < 99 THEN conversation_created_at END) | [{"table": "intercom__conversation_enhanced", "column": "conversation_created_at"}] | [{"table": "intercom__conversation_enhanced", "column": "all_conversation_tags"}, {"table": "intercom__conversation_enhanced", "column": "all_conversation_tags"}, {"table": "intercom__conversation_enhanced", "column": "all_conversation_tags"}, {"table": "intercom__conversation_enhanced", "column": "all_conversation_tags"}, {"table": "intercom__conversation_enhanced", "column": "all_conversation_tags"}, {"table": "intercom__conversation_enhanced", "column": "all_conversation_tags"}, {"table": "intercom__conversation_enhanced", "column": "all_conversation_tags"}, {"table": "intercom__conversation_enhanced", "column": "all_conversation_tags"}, {"table": "intercom__conversation_enhanced", "column": "all_conversation_tags"}, {"table": "intercom__conversation_enhanced", "column": "all_conversation_tags"}, {"table": "intercom__conversation_enhanced", "column": "all_conversation_tags"}, {"table": "intercom__conversation_enhanced", "column": "all_conversation_tags"}, {"table": "intercom__conversation_enhanced", "column": "all_conversation_tags"}, {"table": "intercom__conversation_enhanced", "column": "all_conversation_tags"}, {"table": "intercom__conversation_enhanced", "column": "all_conversation_tags"}, {"table": "intercom__conversation_enhanced", "column": "all_conversation_tags"}, {"table": "intercom__conversation_enhanced", "column": "all_conversation_tags"}, {"table": "intercom__conversation_enhanced", "column": "all_conversation_tags"}] | False |
| B5 | MIN(CASE WHEN stage_rank >= 5 AND stage_rank < 99 THEN conversation_created_at END) | [{"table": "intercom__conversation_enhanced", "column": "conversation_created_at"}] | [{"table": "intercom__conversation_enhanced", "column": "all_conversation_tags"}, {"table": "intercom__conversation_enhanced", "column": "all_conversation_tags"}, {"table": "intercom__conversation_enhanced", "column": "all_conversation_tags"}, {"table": "intercom__conversation_enhanced", "column": "all_conversation_tags"}, {"table": "intercom__conversation_enhanced", "column": "all_conversation_tags"}, {"table": "intercom__conversation_enhanced", "column": "all_conversation_tags"}, {"table": "intercom__conversation_enhanced", "column": "all_conversation_tags"}, {"table": "intercom__conversation_enhanced", "column": "all_conversation_tags"}, {"table": "intercom__conversation_enhanced", "column": "all_conversation_tags"}, {"table": "intercom__conversation_enhanced", "column": "all_conversation_tags"}, {"table": "intercom__conversation_enhanced", "column": "all_conversation_tags"}, {"table": "intercom__conversation_enhanced", "column": "all_conversation_tags"}, {"table": "intercom__conversation_enhanced", "column": "all_conversation_tags"}, {"table": "intercom__conversation_enhanced", "column": "all_conversation_tags"}, {"table": "intercom__conversation_enhanced", "column": "all_conversation_tags"}, {"table": "intercom__conversation_enhanced", "column": "all_conversation_tags"}, {"table": "intercom__conversation_enhanced", "column": "all_conversation_tags"}, {"table": "intercom__conversation_enhanced", "column": "all_conversation_tags"}] | False |
| B5 | MIN(CASE WHEN stage_rank >= 7 AND stage_rank < 99 THEN conversation_created_at END) | [{"table": "intercom__conversation_enhanced", "column": "conversation_created_at"}] | [{"table": "intercom__conversation_enhanced", "column": "all_conversation_tags"}, {"table": "intercom__conversation_enhanced", "column": "all_conversation_tags"}, {"table": "intercom__conversation_enhanced", "column": "all_conversation_tags"}, {"table": "intercom__conversation_enhanced", "column": "all_conversation_tags"}, {"table": "intercom__conversation_enhanced", "column": "all_conversation_tags"}, {"table": "intercom__conversation_enhanced", "column": "all_conversation_tags"}, {"table": "intercom__conversation_enhanced", "column": "all_conversation_tags"}, {"table": "intercom__conversation_enhanced", "column": "all_conversation_tags"}, {"table": "intercom__conversation_enhanced", "column": "all_conversation_tags"}, {"table": "intercom__conversation_enhanced", "column": "all_conversation_tags"}, {"table": "intercom__conversation_enhanced", "column": "all_conversation_tags"}, {"table": "intercom__conversation_enhanced", "column": "all_conversation_tags"}, {"table": "intercom__conversation_enhanced", "column": "all_conversation_tags"}, {"table": "intercom__conversation_enhanced", "column": "all_conversation_tags"}, {"table": "intercom__conversation_enhanced", "column": "all_conversation_tags"}, {"table": "intercom__conversation_enhanced", "column": "all_conversation_tags"}, {"table": "intercom__conversation_enhanced", "column": "all_conversation_tags"}, {"table": "intercom__conversation_enhanced", "column": "all_conversation_tags"}] | False |


## S41

类别 `data`；来源 `python`；调用 `23639f47c6c247eea13dab276ab99069`；状态 `success`。

```sql

SELECT 
  ce.all_conversation_contacts AS contact_id,
  ce.conversation_id,
  ce.conversation_created_at,
  ce.conversation_initiated_type,
  ce.conversation_subject,
  ce.sla_name,
  ce.sla_status,
  ce.conversation_rating,
  ce.conversation_state,
  ce.all_conversation_tags,
  cm.count_total_parts,
  cm.count_reopens,
  cm.time_to_first_response_minutes,
  CASE WHEN instr(ce.all_conversation_tags,'stage:')>0 THEN
    substr(ce.all_conversation_tags, instr(ce.all_conversation_tags,'stage:')+6,
      CASE WHEN instr(substr(ce.all_conversation_tags,instr(ce.all_conversation_tags,'stage:')+6),'|')>0
        THEN instr(substr(ce.all_conversation_tags,instr(ce.all_conversation_tags,'stage:')+6),'|')-1
        ELSE length(substr(ce.all_conversation_tags,instr(ce.all_conversation_tags,'stage:')+6)) END)
  END AS stage,
  CASE WHEN instr(ce.all_conversation_tags,'intent:')>0 THEN
    substr(ce.all_conversation_tags, instr(ce.all_conversation_tags,'intent:')+7,
      CASE WHEN instr(substr(ce.all_conversation_tags,instr(ce.all_conversation_tags,'intent:')+7),'|')>0
        THEN instr(substr(ce.all_conversation_tags,instr(ce.all_conversation_tags,'intent:')+7),'|')-1
        ELSE length(substr(ce.all_conversation_tags,instr(ce.all_conversation_tags,'intent:')+7)) END)
  END AS intent
FROM intercom__conversation_enhanced ce
JOIN intercom__conversation_metrics cm ON ce.conversation_id = cm.conversation_id

```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-098/attempt-01/sql/S41.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-098/attempt-01/sql/S41.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-098/attempt-01/results/S41.rows.jsonl)；完整：True；SHA256：`9842e735ef5e6be828dde3acef88d0f4fbd63bfebc3be48d91f149b1f0272549`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "ce", "kind": "base", "block": null, "base_tables": ["intercom__conversation_enhanced"]}, {"alias": "cm", "kind": "base", "block": null, "base_tables": ["intercom__conversation_metrics"]}] | [{"type": "INNER", "right": "intercom__conversation_metrics AS cm", "on": "ce.conversation_id = cm.conversation_id", "using": []}] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |


## S42

类别 `data`；来源 `python`；调用 `ea6d2b58d8854b78a2becb16492409bd`；状态 `success`。

```sql

SELECT ce.conversation_initiated_type, ce.sla_name, ce.sla_status, ce.conversation_rating, 
       ce.conversation_remark, cm.time_to_first_response_minutes
FROM intercom__conversation_enhanced ce
JOIN intercom__conversation_metrics cm ON ce.conversation_id = cm.conversation_id

```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-098/attempt-01/sql/S42.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-098/attempt-01/sql/S42.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-098/attempt-01/results/S42.rows.jsonl)；完整：True；SHA256：`a9684fb09ccd51c240f60aaf71d531b282d6e99a85879ba0f941985ea0bc6e30`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "ce", "kind": "base", "block": null, "base_tables": ["intercom__conversation_enhanced"]}, {"alias": "cm", "kind": "base", "block": null, "base_tables": ["intercom__conversation_metrics"]}] | [{"type": "INNER", "right": "intercom__conversation_metrics AS cm", "on": "ce.conversation_id = cm.conversation_id", "using": []}] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |


## S43

类别 `data`；来源 `python`；调用 `ea6d2b58d8854b78a2becb16492409bd`；状态 `success`。

```sql

SELECT ce.all_conversation_contacts AS contact_id, 
       ce.conversation_initiated_type,
       c.industry,
       c.plan_name
FROM intercom__conversation_enhanced ce
LEFT JOIN intercom__contact_enhanced ct ON ce.all_conversation_contacts = ct.contact_id
LEFT JOIN intercom__company_enhanced c ON ct.all_contact_company_names = c.company_name
LIMIT 10

```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-098/attempt-01/sql/S43.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-098/attempt-01/sql/S43.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-098/attempt-01/results/S43.rows.jsonl)；完整：True；SHA256：`ed6ace697ef36c32164675eaa97914028a46b82adbd5e75306da118098dcfa49`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "ce", "kind": "base", "block": null, "base_tables": ["intercom__conversation_enhanced"]}, {"alias": "ct", "kind": "base", "block": null, "base_tables": ["intercom__contact_enhanced"]}, {"alias": "c", "kind": "base", "block": null, "base_tables": ["intercom__company_enhanced"]}] | [{"type": "LEFT", "right": "intercom__contact_enhanced AS ct", "on": "ce.all_conversation_contacts = ct.contact_id", "using": []}, {"type": "LEFT", "right": "intercom__company_enhanced AS c", "on": "ct.all_contact_company_names = c.company_name", "using": []}] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |


## S44

类别 `data`；来源 `python`；调用 `ea6d2b58d8854b78a2becb16492409bd`；状态 `success`。

```sql

SELECT DISTINCT ct.all_contact_company_names, c.company_id, c.industry, c.plan_name
FROM intercom__contact_enhanced ct
LEFT JOIN intercom__company_enhanced c ON ct.all_contact_company_names = c.company_name
LIMIT 20

```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-098/attempt-01/sql/S44.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-098/attempt-01/sql/S44.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-098/attempt-01/results/S44.rows.jsonl)；完整：True；SHA256：`fa590cea10ae29c6aa9d82c89f55e348770f439d8e3c790181b67523d84c40b1`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "ct", "kind": "base", "block": null, "base_tables": ["intercom__contact_enhanced"]}, {"alias": "c", "kind": "base", "block": null, "base_tables": ["intercom__company_enhanced"]}] | [{"type": "LEFT", "right": "intercom__company_enhanced AS c", "on": "ct.all_contact_company_names = c.company_name", "using": []}] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |


## S45

类别 `data`；来源 `python`；调用 `ea6d2b58d8854b78a2becb16492409bd`；状态 `success`。

```sql

SELECT COUNT(*) as total,
       SUM(CASE WHEN c.company_id IS NOT NULL THEN 1 ELSE 0 END) as matched
FROM (
  SELECT DISTINCT all_contact_company_names as company_name
  FROM intercom__contact_enhanced
) ct
LEFT JOIN intercom__company_enhanced c ON ct.company_name = c.company_name

```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-098/attempt-01/sql/S45.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-098/attempt-01/sql/S45.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-098/attempt-01/results/S45.rows.jsonl)；完整：True；SHA256：`ecb363345c1e5a670755ca3fccce243a715f531015b4f857a6c0db59a24a1fd1`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "intercom__contact_enhanced", "kind": "base", "block": null, "base_tables": ["intercom__contact_enhanced"]}] | [] | [] |
| B2 | [{"alias": "ct", "kind": "derived", "block": "B1", "base_tables": ["intercom__contact_enhanced"]}, {"alias": "c", "kind": "base", "block": null, "base_tables": ["intercom__company_enhanced"]}] | [{"type": "LEFT", "right": "intercom__company_enhanced AS c", "on": "ct.company_name = c.company_name", "using": []}] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B2 | COUNT(*) | [] | [] | True |
| B2 | SUM(CASE WHEN NOT c.company_id IS NULL THEN 1 ELSE 0 END) | [] | [{"table": "intercom__company_enhanced", "column": "company_id"}] | False |


## S46

类别 `data`；来源 `python`；调用 `0d98bf9f078e4a669d84cbd8afdaeac9`；状态 `success`。

```sql

SELECT ct.contact_id, ct.all_contact_company_names AS company_name,
       c.company_id, c.industry, c.plan_name, c.plan_id, c.monthly_spend
FROM intercom__contact_enhanced ct
LEFT JOIN intercom__company_enhanced c ON ct.all_contact_company_names = c.company_name

```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-098/attempt-01/sql/S46.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-098/attempt-01/sql/S46.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-098/attempt-01/results/S46.rows.jsonl)；完整：True；SHA256：`c7cfa4c2698ca01882ff88b099e24a28ba370594bcc44bf5e58a7aa080e2f554`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "ct", "kind": "base", "block": null, "base_tables": ["intercom__contact_enhanced"]}, {"alias": "c", "kind": "base", "block": null, "base_tables": ["intercom__company_enhanced"]}] | [{"type": "LEFT", "right": "intercom__company_enhanced AS c", "on": "ct.all_contact_company_names = c.company_name", "using": []}] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |


## S47

类别 `data`；来源 `python`；调用 `04ac08a7af77484bbbea27081bf00a21`；状态 `success`。

```sql

SELECT contact_id, all_contact_tags,
  CASE WHEN instr(all_contact_tags,'source:')>0 THEN
    substr(all_contact_tags, instr(all_contact_tags,'source:')+7,
      CASE WHEN instr(substr(all_contact_tags,instr(all_contact_tags,'source:')+7),'|')>0
        THEN instr(substr(all_contact_tags,instr(all_contact_tags,'source:')+7),'|')-1
        ELSE length(substr(all_contact_tags,instr(all_contact_tags,'source:')+7)) END)
  END AS lead_source
FROM intercom__contact_enhanced

```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-098/attempt-01/sql/S47.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-098/attempt-01/sql/S47.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-098/attempt-01/results/S47.rows.jsonl)；完整：True；SHA256：`843a232db9f998b4ecc47d4c6f69770c93efa77a75763732b0441e10bf130252`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "intercom__contact_enhanced", "kind": "base", "block": null, "base_tables": ["intercom__contact_enhanced"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |

