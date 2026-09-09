# dacomp-093

Using behavioral data from klaviyo__campaigns and klaviyo__persons, design an analysis on …

运行：已提交。官方未评分。全部 SQL 尝试/成功 41/40；数据 SQL 38/37；Python 5 次。

完整原题：

Using behavioral data from klaviyo__campaigns and klaviyo__persons, design an analysis on the combined effects of email send timing and subject. Evaluate how different send time windows (weekday/weekend, morning/afternoon, before/after holidays) and subject copy (SUBJECT keyword grouping such as discount, new, storytelling) interact to influence open rate, click rate, and subsequent active retention (active_retention_rate_week/month). Break down results by is_archived (archived vs non-archived) and variation_id (single send vs variant send), control for audience size (total_count_unique_people), and apply de-noising (for example, exclude anomalous spikes in count_received_email). Conclude with actionable recommendations and potential risks for different brand communication strategies.

| 表 | 行数 | 列数 |
| --- | --- | --- |
| klaviyo__campaigns | 184 | 35 |
| klaviyo__persons | 1192 | 49 |


实际路线（分析者依据 SQL/源码概括，不代表 Agent 自述）：SQL 结构探索和初步汇总 → 同会话续接 → Python 清洗、分组统计、检验和图表 → 提交

数据库大小：700,416 字节。

## 数据 SQL

| SQL | 状态 | 基础表 | Join 输入/类型 | GROUP BY | 聚合表达式 | 结果行数 | 数据库 ms |
| --- | --- | --- | --- | --- | --- | --- | --- |
| [S4/Q1](#s4) | success | ["klaviyo__campaigns"] | 0 / {} | [] | ["COUNT(*)", "COUNT(DISTINCT campaign_id)", "COUNT(DISTINCT variation_id)", "MIN(SENT_AT)", "MAX(SENT_AT)", "COUNT(*) FILTER(WHERE SENT_AT IS NULL)"] | 1 | 0.711 |
| [S5/Q2](#s5) | success | ["klaviyo__campaigns"] | 0 / {} | ["is_archived", "NOT variation_id IS NULL"] | ["COUNT(*)", "COUNT(DISTINCT SUBJECT)", "AVG(email_open_rate)", "AVG(email_click_to_open_rate)", "AVG(total_count_unique_people)"] | 2 | 0.581 |
| [S6/Q3](#s6) | success | ["klaviyo__campaigns"] | 0 / {} | ["SUBJECT"] | ["COUNT(*)", "AVG(email_open_rate)", "AVG(email_click_to_open_rate)", "MIN(SUBJECT)"] | 24 | 0.586 |
| [S7/Q4](#s7) | success | ["klaviyo__campaigns"] | 0 / {} | ["variation_id"] | ["COUNT(*)", "AVG(email_open_rate)", "AVG(email_click_to_open_rate)"] | 3 | 0.467 |
| [S8/Q5](#s8) | success | ["klaviyo__campaigns"] | 0 / {} | ["CAMPAIGN_TYPE"] | ["COUNT(*)"] | 4 | 0.434 |
| [S9/Q6](#s9) | success | ["klaviyo__campaigns"] | 0 / {} | ["SUBJECT"] | ["COUNT(*)"] | 24 | 0.513 |
| [S10/Q7](#s10) | success | ["klaviyo__campaigns"] | 0 / {} | ["STRFTIME('%w', SENT_AT)"] | ["COUNT(*)", "AVG(email_open_rate)", "AVG(email_click_to_open_rate)"] | 7 | 0.551 |
| [S11/Q8](#s11) | success | ["klaviyo__campaigns"] | 0 / {} | ["SUBJECT"] | ["COUNT(*)", "MIN(STRFTIME('%Y-%m-%d %H:%M', SENT_AT))", "MAX(STRFTIME('%Y-%m-%d %H:%M', SENT_AT))"] | 24 | 0.81 |
| [S12/Q9](#s12) | success | ["klaviyo__campaigns"] | 0 / {} | ["campaign_name"] | ["COUNT(*)"] | 18 | 0.443 |
| [S13/Q10](#s13) | success | ["klaviyo__campaigns"] | 0 / {} | ["campaign_name"] | ["COUNT(*)"] | 18 | 0.419 |
| [S14/Q11](#s14) | success | ["klaviyo__campaigns"] | 0 / {} | [] | [] | 18 | 0.453 |
| [S15/Q12](#s15) | success | ["klaviyo__persons"] | 0 / {} | [] | ["COUNT(*)", "COUNT(DISTINCT person_id)", "AVG(active_retention_rate_week)", "AVG(active_retention_rate_month)", "AVG(count_received_email)", "MIN(first_event_on)", "MAX(last_event_on)"] | 1 | 1.421 |
| [S16/Q13](#s16) | success | ["klaviyo__campaigns"] | 0 / {} | [] | ["COUNT(DISTINCT campaign_id)", "COUNT(*)", "COUNT(DISTINCT source_relation)"] | 1 | 0.508 |
| [S17/Q14](#s17) | success | ["klaviyo__persons"] | 0 / {} | [] | [] | 20 | 0.629 |
| [S18/Q15](#s18) | success | ["klaviyo__campaigns"] | 0 / {} | [] | [] | 10 | 0.35 |
| [S19/Q16](#s19) | success | ["klaviyo__campaigns"] | 0 / {} | [] | [] | 5 | 0.565 |
| [S20/Q17](#s20) | success | ["klaviyo__campaigns"] | 0 / {} | [] | [] | 10 | 0.586 |
| [S21/Q18](#s21) | success | ["klaviyo__campaigns"] | 0 / {} | ["planned_timing"] | ["COUNT(*)", "AVG(email_open_rate)", "AVG(email_click_to_open_rate)", "AVG(total_placed_orders)", "AVG(gmv_net)"] | 6 | 0.799 |
| [S22/Q19](#s22) | success | ["klaviyo__campaigns"] | 0 / {} | ["subject_keyword"] | ["COUNT(*)", "AVG(email_open_rate)", "AVG(email_click_to_open_rate)", "AVG(total_placed_orders)", "AVG(gmv_net)"] | 3 | 0.656 |
| [S23/Q20](#s23) | success | ["klaviyo__campaigns"] | 0 / {} | ["planned_timing", "subject_keyword"] | ["COUNT(*)", "AVG(email_open_rate)", "AVG(email_click_to_open_rate)", "AVG(total_placed_orders)", "AVG(gmv_net)", "AVG(product_view_to_order_rate_campaign)"] | 18 | 1.036 |
| [S24/Q21](#s24) | success | ["klaviyo__campaigns"] | 0 / {} | ["is_archived", "planned_timing", "subject_keyword"] | ["COUNT(*)", "AVG(email_open_rate)", "AVG(email_click_to_open_rate)"] | 18 | 0.922 |
| [S25/Q22](#s25) | success | ["klaviyo__campaigns"] | 0 / {} | ["variation_id", "planned_timing", "subject_keyword"] | ["COUNT(*)", "AVG(email_open_rate)", "AVG(email_click_to_open_rate)", "AVG(total_count_unique_people)"] | 36 | 1.116 |
| [S26/Q23](#s26) | success | ["klaviyo__campaigns"] | 0 / {} | [] | ["MIN(count_received_email)", "MAX(count_received_email)", "AVG(email_open_rate)", "AVG(email_click_to_open_rate)", "AVG(count_received_email)", "AVG(total_count_unique_people)", "AVG(count_received_email)", "AVG(total_count_unique_people)"] | 1 | 0.486 |
| [S27/Q24](#s27) | success | ["klaviyo__campaigns"] | 0 / {} | [] | [] | 7 | 0.965 |
| [S28/Q25](#s28) | failed | ["klaviyo__campaigns"] | 0 / {} | [] | [] | unknown | 未取得；调用总时长 0.204 ms |
| [S29/Q26](#s29) | success | ["klaviyo__campaigns"] | 0 / {} | [] | ["AVG(CASE WHEN row_num <= CAST(0.25 * total AS INTEGER) THEN count_received_email END)", "AVG(CASE WHEN row_num <= CAST(0.75 * total AS INTEGER) THEN count_received_email END)"] | 1 | 0.836 |
| [S30/Q27](#s30) | success | ["klaviyo__campaigns"] | 0 / {} | [] | ["MIN(count_received_email)", "MAX(count_received_email)", "AVG(count_received_email)"] | 1 | 0.514 |
| [S31/Q28](#s31) | success | ["klaviyo__persons"] | 0 / {} | ["timezone"] | ["COUNT(*)", "AVG(active_retention_rate_week)", "AVG(active_retention_rate_month)", "AVG(email_open_rate)", "AVG(count_received_email)", "AVG(count_opened_email)"] | 3 | 2.046 |
| [S32/Q29](#s32) | success | ["klaviyo__persons"] | 0 / {} | ["CASE WHEN count_received_email < 100 THEN 'low (<100)' WHEN count_received_email < 150 THEN 'medium (100-150)' ELSE 'high (150+)' END"] | ["COUNT(*)", "AVG(active_retention_rate_week)", "AVG(active_retention_rate_month)", "AVG(email_open_rate)", "AVG(active_retention_rate_week)"] | 3 | 1.223 |
| [S33/Q30](#s33) | success | ["klaviyo__campaigns", "klaviyo__persons"] | 0 / {} | [] | ["COUNT(*)", "SUM(count_received_email)", "AVG(count_received_email)", "COUNT(*)", "SUM(count_opened_email)", "AVG(count_opened_email)"] | 1 | 1.225 |
| [S34/Q31](#s34) | success | ["klaviyo__campaigns"] | 0 / {} | [] | [] | 8 | 0.562 |
| [S35/Q32](#s35) | success | ["klaviyo__campaigns"] | 0 / {} | [] | [] | 184 | 2.041 |
| [S36/Q33](#s36) | success | ["klaviyo__campaigns"] | 0 / {} | [] | [] | 184 | 1.529 |
| [S37/Q34](#s37) | success | ["klaviyo__persons"] | 0 / {} | [] | [] | 1192 | 5.831 |
| [S38/Q35](#s38) | success | ["klaviyo__campaigns"] | 0 / {} | ["planned_timing", "CASE WHEN CAST(STRFTIME('%w', SENT_AT) AS INTEGER) BETWEEN 1 AND 5 THEN 'weekday' ELSE 'weekend' END", "CASE WHEN CAST(STRFTIME('%H', SENT_AT) AS INTEGER) BETWEEN 6 AND 11 THEN 'morning' WHEN CAST(STRFTIME('%H', SENT_AT) AS INTEGER) BETWEEN 12 AND 17 THEN 'afternoon' WHEN CAST(STRFTIME('%H', SENT_AT) AS INTEGER) BETWEEN 18 AND 23 THEN 'evening' ELSE 'night' END"] | ["COUNT(*)", "AVG(email_open_rate)", "AVG(email_click_to_open_rate)"] | 12 | 1.045 |
| [S39/Q36](#s39) | success | ["klaviyo__campaigns"] | 0 / {} | [] | [] | 30 | 0.589 |
| [S40/Q37](#s40) | success | ["klaviyo__campaigns"] | 0 / {} | [] | [] | 184 | 1.035 |
| [S41/Q38](#s41) | success | ["klaviyo__campaigns"] | 0 / {} | [] | [] | 184 | 0.964 |


## 元数据和设置

| SQL | 类别 | 状态 | 内容 |
| --- | --- | --- | --- |
| S1 | connection_setup | success | PRAGMA query_only=ON |
| S2 | metadata | success | SELECT name,sql FROM sqlite_master WHERE type='table' ORDER BY name |
| S3 | connection_setup | success | PRAGMA query_only=ON |


## Python 与执行位置

人工源码审查：**database_first_violation**。Python 读取活动和人员级数据后按时段、主题、时区、分箱组重复计算均值、计数，pivot_table 也进行均值聚合；这些数据库可完成的准备工作未留在 SQL。ANOVA 与秩相关检验允许作为统计补充，不抵消前述执行位置偏离。 [证据](../reviews/dacomp-093.json)。

P1：Statistical analysis and visualization of campaign timing × subject keyword interaction effects on open rates and CTOR. This requires ANOVA, multiple regression, and custom visualizations that go beyond SQL's aggregation capabilities.

[源码](../../../runs/dsv4flash-db-first-full-01/dacomp-093/attempt-01/python/P1.py)；[输出](../../../runs/dsv4flash-db-first-full-01/dacomp-093/attempt-01/python/P1.stdout)；[错误](../../../runs/dsv4flash-db-first-full-01/dacomp-093/attempt-01/python/P1.stderr)。检出需人工核验的 SQL 可实现操作：groupby(, .query(；不能仅凭理由判为合规。

P2：Statistical analysis and visualization of campaign timing × subject keyword interaction effects. Using scipy for ANOVA since statsmodels is not available.

[源码](../../../runs/dsv4flash-db-first-full-01/dacomp-093/attempt-01/python/P2.py)；[输出](../../../runs/dsv4flash-db-first-full-01/dacomp-093/attempt-01/python/P2.stdout)；[错误](../../../runs/dsv4flash-db-first-full-01/dacomp-093/attempt-01/python/P2.stderr)。检出需人工核验的 SQL 可实现操作：groupby(, .query(；不能仅凭理由判为合规。

P3：Person-level retention analysis. This requires statistical testing and visualization of retention patterns by timezone and email engagement, which cannot be done with SQL aggregation alone.

[源码](../../../runs/dsv4flash-db-first-full-01/dacomp-093/attempt-01/python/P3.py)；[输出](../../../runs/dsv4flash-db-first-full-01/dacomp-093/attempt-01/python/P3.stdout)；[错误](../../../runs/dsv4flash-db-first-full-01/dacomp-093/attempt-01/python/P3.stderr)。检出需人工核验的 SQL 可实现操作：groupby(, .query(, sort_values(；不能仅凭理由判为合规。

P4：Generate a combined visualization showing the key interaction effects - timing vs subject group on open rates and CTOR in a single figure for the report.

[源码](../../../runs/dsv4flash-db-first-full-01/dacomp-093/attempt-01/python/P4.py)；[输出](../../../runs/dsv4flash-db-first-full-01/dacomp-093/attempt-01/python/P4.stdout)；[错误](../../../runs/dsv4flash-db-first-full-01/dacomp-093/attempt-01/python/P4.stderr)。检出需人工核验的 SQL 可实现操作：groupby(, .query(；不能仅凭理由判为合规。

P5：Final analysis pass: archived/variation breakdown, audience-size-controlled regression, and regenerate subject bar chart with English labels (CJK glyphs missing in default font).

[源码](../../../runs/dsv4flash-db-first-full-01/dacomp-093/attempt-01/python/P5.py)；[输出](../../../runs/dsv4flash-db-first-full-01/dacomp-093/attempt-01/python/P5.stdout)；[错误](../../../runs/dsv4flash-db-first-full-01/dacomp-093/attempt-01/python/P5.stderr)。检出需人工核验的 SQL 可实现操作：groupby(, .query(；不能仅凭理由判为合规。

## 优化机会

已验证候选; original verified selection retained across continuation。筛选限于精确 SQL、相同自包含 CTE、相同单表完整过滤、可分解单表聚合；未覆盖任意 Join 等价和一般谓词蕴含。全部候选都是 offline，未测在线预测。

| 候选 | 类型 | 已有结果 | 覆盖 SQL | 后续次数 | 中间行数 | 验证 | 成本 |
| --- | --- | --- | --- | --- | --- | --- | --- |
| C1 | aggregate MV | False | ["S6", "S7", "S8", "S9", "S10", "S11", "S12", "S13", "S26", "S30"] | 9 | 180 | rejected_result_mismatch | Not benchmarked; correctness alone does not establish net speedup. |
| C2 | aggregate MV | False | ["S31", "S32"] | 1 | 8 | verified | Not benchmarked; correctness alone does not establish net speedup. |


已验证覆盖（含触发查询、候选并集去重）：2/37 条成功数据 SQL。正确性仅针对当前数据库快照；未测性能的候选不能声称已加速。

[完整 build/rewrite 与比较证据](dacomp-093.analysis.json)。

### C2：aggregate MV

Union of grouping keys; decomposable aggregate states; AVG uses SUM and non-NULL COUNT.

原查询 [S31](#s31), [S32](#s32) → 新增共享状态 C2 → 后续 1 次可复用。该构建点为事后假设，不代表 Agent 当时预知后续。

构建定义：

```sql
SELECT timezone AS __g0, CASE WHEN count_received_email < 100 THEN 'low (<100)' WHEN count_received_email < 150 THEN 'medium (100-150)' ELSE 'high (150+)' END AS __g1, COUNT(*) AS __a0, SUM(active_retention_rate_week) AS __a1_sum, COUNT(active_retention_rate_week) AS __a1_n, SUM(active_retention_rate_month) AS __a2_sum, COUNT(active_retention_rate_month) AS __a2_n, SUM(email_open_rate) AS __a3_sum, COUNT(email_open_rate) AS __a3_n, SUM(count_received_email) AS __a4_sum, COUNT(count_received_email) AS __a4_n, SUM(count_opened_email) AS __a5_sum, COUNT(count_opened_email) AS __a5_n FROM "klaviyo__persons"  GROUP BY timezone, CASE WHEN count_received_email < 100 THEN 'low (<100)' WHEN count_received_email < 150 THEN 'medium (100-150)' ELSE 'high (150+)' END
```

受益查询 S31 的改写示例：

```sql
SELECT __g0 AS "timezone", SUM(__a0) AS n, ROUND((1.0 * SUM(__a1_sum) / NULLIF(SUM(__a1_n), 0)), 4) AS avg_ret_week, ROUND((1.0 * SUM(__a2_sum) / NULLIF(SUM(__a2_n), 0)), 4) AS avg_ret_month, ROUND((1.0 * SUM(__a3_sum) / NULLIF(SUM(__a3_n), 0)), 4) AS avg_open_rate, ROUND((1.0 * SUM(__a4_sum) / NULLIF(SUM(__a4_n), 0)), 0) AS avg_received, ROUND((1.0 * SUM(__a5_sum) / NULLIF(SUM(__a5_n), 0)), 0) AS avg_opened FROM temp.reuse_candidate GROUP BY __g0 ORDER BY n DESC
```

| 原 SQL | 列名一致 | 结果一致 | 比较方法 |
| --- | --- | --- | --- |
| S31 | True | True | ordered_numeric_tolerance |
| S32 | True | True | ordered_numeric_tolerance |


验证状态：verified；成本结论：Not benchmarked; correctness alone does not establish net speedup.

### C1：aggregate MV

Union of grouping keys; decomposable aggregate states; AVG uses SUM and non-NULL COUNT.

原查询 [S6](#s6), [S7](#s7), [S8](#s8), [S9](#s9), [S10](#s10), [S11](#s11), [S12](#s12), [S13](#s13), [S26](#s26), [S30](#s30) → 新增共享状态 C1 → 后续 9 次可复用。该构建点为事后假设，不代表 Agent 当时预知后续。

构建定义：

```sql
SELECT subject AS __g0, variation_id AS __g1, campaign_type AS __g2, STRFTIME('%w', sent_at) AS __g3, campaign_name AS __g4, COUNT(*) AS __a0, SUM(email_open_rate) AS __a1_sum, COUNT(email_open_rate) AS __a1_n, SUM(email_click_to_open_rate) AS __a2_sum, COUNT(email_click_to_open_rate) AS __a2_n, MIN(subject) AS __a3, MIN(STRFTIME('%Y-%m-%d %H:%M', sent_at)) AS __a4, MAX(STRFTIME('%Y-%m-%d %H:%M', sent_at)) AS __a5, MIN(count_received_email) AS __a6, MAX(count_received_email) AS __a7, SUM(count_received_email) AS __a8_sum, COUNT(count_received_email) AS __a8_n, SUM(total_count_unique_people) AS __a9_sum, COUNT(total_count_unique_people) AS __a9_n FROM "klaviyo__campaigns"  GROUP BY subject, variation_id, campaign_type, STRFTIME('%w', sent_at), campaign_name
```

受益查询 S6 的改写示例：

```sql
SELECT __g0 AS "SUBJECT", SUM(__a0) AS n, (1.0 * SUM(__a1_sum) / NULLIF(SUM(__a1_n), 0)) AS avg_open_rate, (1.0 * SUM(__a2_sum) / NULLIF(SUM(__a2_n), 0)) AS avg_ctor, MIN(__a3) AS sample_subject FROM temp.reuse_candidate GROUP BY __g0 ORDER BY n DESC
```

| 原 SQL | 列名一致 | 结果一致 | 比较方法 |
| --- | --- | --- | --- |
| S6 | True | True | ordered_numeric_tolerance |
| S7 | True | False | exact_multiset |
| S8 | True | True | exact_multiset |
| S9 | True | True | ordered_numeric_tolerance |
| S10 | True | True | ordered_numeric_tolerance |
| S11 | True | True | ordered_numeric_tolerance |
| S12 | True | True | ordered_numeric_tolerance |
| S13 | True | True | ordered_numeric_tolerance |
| S26 | True | False | exact_multiset |
| S30 | True | True | exact_multiset |


验证状态：rejected_result_mismatch；成本结论：Not benchmarked; correctness alone does not establish net speedup.

结果依赖：自动记录 SQL→Python 的接口父调用，以及源码中引用归档文件的消费者；字面值相同不认定因果。模型方向选择需要人工读取消息，尚未做全面因果标注。

[原始报告](../../../runs/dsv4flash-db-first-full-01/dacomp-093/attempt-01/answer.md)；[统一消息](../../../runs/dsv4flash-db-first-full-01/dacomp-093/attempt-01/messages.jsonl)；[原始 OpenCode 事件](../../../runs/dsv4flash-db-first-full-01/dacomp-093/attempt-01/opencode.jsonl)；[SQL 引擎日志](../../../runs/dsv4flash-db-first-full-01/dacomp-093/attempt-01/sql_journal.jsonl)。

[可读报告（本地图片链接规范化）](../answers/dacomp-093.md)。原始回答保留，分析结论未改写。

## S1

类别 `connection_setup`；来源 `connection`；调用 `86bdd4354b0841f5abe14845447c0620`；状态 `success`。

```sql
PRAGMA query_only=ON
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-093/attempt-01/sql/S1.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-093/attempt-01/sql/S1.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-093/attempt-01/results/S1.rows.jsonl)；完整：True；SHA256：`e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`。

## S2

类别 `metadata`；来源 `list_db`；调用 `86bdd4354b0841f5abe14845447c0620`；状态 `success`。

```sql
SELECT name,sql FROM sqlite_master WHERE type='table' ORDER BY name
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-093/attempt-01/sql/S2.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-093/attempt-01/sql/S2.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-093/attempt-01/results/S2.rows.jsonl)；完整：True；SHA256：`c7c8e2ec04a98170982bb1dc93e82c9d0fa0a01fd36f041951dcc9aec2942080`。

## S3

类别 `connection_setup`；来源 `connection`；调用 `6cebe9e7e39343e08bfb2be6ef68bcfc`；状态 `success`。

```sql
PRAGMA query_only=ON
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-093/attempt-01/sql/S3.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-093/attempt-01/sql/S3.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-093/attempt-01/results/S3.rows.jsonl)；完整：True；SHA256：`e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`。

## S4

类别 `data`；来源 `query_db`；调用 `6cebe9e7e39343e08bfb2be6ef68bcfc`；状态 `success`。

```sql
SELECT COUNT(*) AS n_campaigns,
       COUNT(DISTINCT campaign_id) AS n_campaign_ids,
       COUNT(DISTINCT variation_id) AS n_variations,
       MIN(SENT_AT) AS min_sent, MAX(SENT_AT) AS max_sent,
       COUNT(*) FILTER (WHERE SENT_AT IS NULL) AS null_sent
FROM klaviyo__campaigns
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-093/attempt-01/sql/S4.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-093/attempt-01/sql/S4.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-093/attempt-01/results/S4.rows.jsonl)；完整：True；SHA256：`5fdba45f594eda84dc854de4e9c1a431ab2e165c07c2a6ea6941f7c7b1693c1f`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "klaviyo__campaigns", "kind": "base", "block": null, "base_tables": ["klaviyo__campaigns"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |
| B1 | COUNT(DISTINCT campaign_id) | [{"table": "klaviyo__campaigns", "column": "campaign_id"}] | [] | False |
| B1 | COUNT(DISTINCT variation_id) | [{"table": "klaviyo__campaigns", "column": "variation_id"}] | [] | False |
| B1 | MIN(SENT_AT) | [{"table": "klaviyo__campaigns", "column": "SENT_AT"}] | [] | False |
| B1 | MAX(SENT_AT) | [{"table": "klaviyo__campaigns", "column": "SENT_AT"}] | [] | False |
| B1 | COUNT(*) FILTER(WHERE SENT_AT IS NULL) | [] | [{"table": "klaviyo__campaigns", "column": "SENT_AT"}] | True |


## S5

类别 `data`；来源 `query_db`；调用 `ae550ec367fa43b38c10d91b992ce8cb`；状态 `success`。

```sql
SELECT is_archived, variation_id IS NOT NULL AS has_variation, COUNT(*) AS n,
       COUNT(DISTINCT SUBJECT) AS n_subjects,
       AVG(email_open_rate) AS avg_open_rate,
       AVG(email_click_to_open_rate) AS avg_ctor,
       AVG(total_count_unique_people) AS avg_audience
FROM klaviyo__campaigns
GROUP BY 1,2
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-093/attempt-01/sql/S5.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-093/attempt-01/sql/S5.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-093/attempt-01/results/S5.rows.jsonl)；完整：True；SHA256：`349e0c8f1369875319607a51ffb92869433ba3c7093ec8b618deaa626a5bde6f`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "klaviyo__campaigns", "kind": "base", "block": null, "base_tables": ["klaviyo__campaigns"]}] | [] | ["is_archived", "NOT variation_id IS NULL"] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |
| B1 | COUNT(DISTINCT SUBJECT) | [{"table": "klaviyo__campaigns", "column": "SUBJECT"}] | [] | False |
| B1 | AVG(email_open_rate) | [{"table": "klaviyo__campaigns", "column": "email_open_rate"}] | [] | False |
| B1 | AVG(email_click_to_open_rate) | [{"table": "klaviyo__campaigns", "column": "email_click_to_open_rate"}] | [] | False |
| B1 | AVG(total_count_unique_people) | [{"table": "klaviyo__campaigns", "column": "total_count_unique_people"}] | [] | False |


## S6

类别 `data`；来源 `query_db`；调用 `d3d0062ef5b6431d89b7b5590b769fa8`；状态 `success`。

```sql
SELECT SUBJECT, COUNT(*) AS n, 
       AVG(email_open_rate) AS avg_open_rate,
       AVG(email_click_to_open_rate) AS avg_ctor,
       MIN(SUBJECT) AS sample_subject
FROM klaviyo__campaigns
GROUP BY SUBJECT
ORDER BY n DESC
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-093/attempt-01/sql/S6.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-093/attempt-01/sql/S6.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-093/attempt-01/results/S6.rows.jsonl)；完整：True；SHA256：`7dd7333fb70d01a44b539d6b2bad654a229ef4578013ef81cbdfc9f47ffa6ad9`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "klaviyo__campaigns", "kind": "base", "block": null, "base_tables": ["klaviyo__campaigns"]}] | [] | ["SUBJECT"] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |
| B1 | AVG(email_open_rate) | [{"table": "klaviyo__campaigns", "column": "email_open_rate"}] | [] | False |
| B1 | AVG(email_click_to_open_rate) | [{"table": "klaviyo__campaigns", "column": "email_click_to_open_rate"}] | [] | False |
| B1 | MIN(SUBJECT) | [{"table": "klaviyo__campaigns", "column": "SUBJECT"}] | [] | False |


## S7

类别 `data`；来源 `query_db`；调用 `a8e3657744c54a44943633ada784cc47`；状态 `success`。

```sql
SELECT variation_id, COUNT(*) AS n, AVG(email_open_rate) AS avg_open_rate, AVG(email_click_to_open_rate) AS avg_ctor
FROM klaviyo__campaigns
GROUP BY variation_id
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-093/attempt-01/sql/S7.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-093/attempt-01/sql/S7.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-093/attempt-01/results/S7.rows.jsonl)；完整：True；SHA256：`11dca120d1bccf0cba0a1622dcd658c2f2e0d90a92a357bc54059760b3a908d1`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "klaviyo__campaigns", "kind": "base", "block": null, "base_tables": ["klaviyo__campaigns"]}] | [] | ["variation_id"] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |
| B1 | AVG(email_open_rate) | [{"table": "klaviyo__campaigns", "column": "email_open_rate"}] | [] | False |
| B1 | AVG(email_click_to_open_rate) | [{"table": "klaviyo__campaigns", "column": "email_click_to_open_rate"}] | [] | False |


## S8

类别 `data`；来源 `query_db`；调用 `7079bd51490645dbb5e98b3a9227a25b`；状态 `success`。

```sql
SELECT DISTINCT CAMPAIGN_TYPE, COUNT(*) AS n
FROM klaviyo__campaigns
GROUP BY CAMPAIGN_TYPE
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-093/attempt-01/sql/S8.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-093/attempt-01/sql/S8.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-093/attempt-01/results/S8.rows.jsonl)；完整：True；SHA256：`1070b6d2e03e7c5adfad9c1c093e5e65f9edf301b12acf120ff21518be8c84cf`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "klaviyo__campaigns", "kind": "base", "block": null, "base_tables": ["klaviyo__campaigns"]}] | [] | ["CAMPAIGN_TYPE"] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |


## S9

类别 `data`；来源 `query_db`；调用 `ab332aacca074265b0b8d47aeef0c36d`；状态 `success`。

```sql
SELECT SUBJECT, COUNT(*) AS n
FROM klaviyo__campaigns
GROUP BY SUBJECT
ORDER BY n DESC
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-093/attempt-01/sql/S9.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-093/attempt-01/sql/S9.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-093/attempt-01/results/S9.rows.jsonl)；完整：True；SHA256：`677c951cba24a698b3fdd746a46b4bd7c36912dcf92b8ba332bd1bf659b7716c`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "klaviyo__campaigns", "kind": "base", "block": null, "base_tables": ["klaviyo__campaigns"]}] | [] | ["SUBJECT"] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |


## S10

类别 `data`；来源 `query_db`；调用 `16ceab2d75c349abb12e740e718c8190`；状态 `success`。

```sql
SELECT strftime('%w', SENT_AT) AS dow, COUNT(*) AS n,
       AVG(email_open_rate) AS avg_open, AVG(email_click_to_open_rate) AS avg_ctor
FROM klaviyo__campaigns
GROUP BY dow ORDER BY dow
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-093/attempt-01/sql/S10.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-093/attempt-01/sql/S10.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-093/attempt-01/results/S10.rows.jsonl)；完整：True；SHA256：`9ac6881ff8c1b0a617ca0bb7d5671603a293410adf4f382d2ddf5ab1c64e6611`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "klaviyo__campaigns", "kind": "base", "block": null, "base_tables": ["klaviyo__campaigns"]}] | [] | ["STRFTIME('%w', SENT_AT)"] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |
| B1 | AVG(email_open_rate) | [{"table": "klaviyo__campaigns", "column": "email_open_rate"}] | [] | False |
| B1 | AVG(email_click_to_open_rate) | [{"table": "klaviyo__campaigns", "column": "email_click_to_open_rate"}] | [] | False |


## S11

类别 `data`；来源 `query_db`；调用 `6660d5378bb14346955e1d5f109d0252`；状态 `success`。

```sql
SELECT SUBJECT, COUNT(*) AS n, MIN(strftime('%Y-%m-%d %H:%M', SENT_AT)) AS first_sent, MAX(strftime('%Y-%m-%d %H:%M', SENT_AT)) AS last_sent
FROM klaviyo__campaigns
GROUP BY SUBJECT
ORDER BY SUBJECT
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-093/attempt-01/sql/S11.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-093/attempt-01/sql/S11.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-093/attempt-01/results/S11.rows.jsonl)；完整：True；SHA256：`d2be8c47c1e539fdce6d4b9a254c013144f5e7b62a56ff69832516c32e5cbd51`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "klaviyo__campaigns", "kind": "base", "block": null, "base_tables": ["klaviyo__campaigns"]}] | [] | ["SUBJECT"] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |
| B1 | MIN(STRFTIME('%Y-%m-%d %H:%M', SENT_AT)) | [{"table": "klaviyo__campaigns", "column": "SENT_AT"}] | [] | False |
| B1 | MAX(STRFTIME('%Y-%m-%d %H:%M', SENT_AT)) | [{"table": "klaviyo__campaigns", "column": "SENT_AT"}] | [] | False |


## S12

类别 `data`；来源 `query_db`；调用 `f160591e2d974570a5e8533049742a0c`；状态 `success`。

```sql
SELECT campaign_name, COUNT(*) AS n
FROM klaviyo__campaigns
GROUP BY campaign_name ORDER BY n DESC LIMIT 30
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-093/attempt-01/sql/S12.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-093/attempt-01/sql/S12.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-093/attempt-01/results/S12.rows.jsonl)；完整：True；SHA256：`03cdd7666829619e7d69a6419d03a09ba6248dbd369777c0866089fd81496fe3`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "klaviyo__campaigns", "kind": "base", "block": null, "base_tables": ["klaviyo__campaigns"]}] | [] | ["campaign_name"] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |


## S13

类别 `data`；来源 `query_db`；调用 `a933553738eb47fd81d9a32f1017349e`；状态 `success`。

```sql
SELECT campaign_name, COUNT(*) AS n
FROM klaviyo__campaigns
GROUP BY campaign_name ORDER BY campaign_name
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-093/attempt-01/sql/S13.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-093/attempt-01/sql/S13.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-093/attempt-01/results/S13.rows.jsonl)；完整：True；SHA256：`77e6c58ff8b7650d6b029396ae32ed7d4026aff6e7c4ab3dbf9a4d11b2ec1ccd`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "klaviyo__campaigns", "kind": "base", "block": null, "base_tables": ["klaviyo__campaigns"]}] | [] | ["campaign_name"] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |


## S14

类别 `data`；来源 `query_db`；调用 `17b8e1fe23ad4d79b09330764df6a0c1`；状态 `success`。

```sql
SELECT DISTINCT campaign_name
FROM klaviyo__campaigns
ORDER BY campaign_name
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-093/attempt-01/sql/S14.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-093/attempt-01/sql/S14.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-093/attempt-01/results/S14.rows.jsonl)；完整：True；SHA256：`34ba611c9bf1d78b51a777bad77e6c6095673aa9ea9587e8c7e74d2332557d3e`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "klaviyo__campaigns", "kind": "base", "block": null, "base_tables": ["klaviyo__campaigns"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |


## S15

类别 `data`；来源 `query_db`；调用 `413401ac92f54f8e803cc55a0da4fddb`；状态 `success`。

```sql
SELECT COUNT(*) AS n_persons,
       COUNT(DISTINCT person_id) AS n_ids,
       AVG(active_retention_rate_week) AS avg_ret_week,
       AVG(active_retention_rate_month) AS avg_ret_month,
       AVG(count_received_email) AS avg_received,
       MIN(first_event_on) AS min_first, MAX(last_event_on) AS max_last
FROM klaviyo__persons
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-093/attempt-01/sql/S15.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-093/attempt-01/sql/S15.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-093/attempt-01/results/S15.rows.jsonl)；完整：True；SHA256：`e3f1076c69f9d6db6669ddab3de3d1b1272d95b9c7feee331b3ba18488a1d11d`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "klaviyo__persons", "kind": "base", "block": null, "base_tables": ["klaviyo__persons"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |
| B1 | COUNT(DISTINCT person_id) | [{"table": "klaviyo__persons", "column": "person_id"}] | [] | False |
| B1 | AVG(active_retention_rate_week) | [{"table": "klaviyo__persons", "column": "active_retention_rate_week"}] | [] | False |
| B1 | AVG(active_retention_rate_month) | [{"table": "klaviyo__persons", "column": "active_retention_rate_month"}] | [] | False |
| B1 | AVG(count_received_email) | [{"table": "klaviyo__persons", "column": "count_received_email"}] | [] | False |
| B1 | MIN(first_event_on) | [{"table": "klaviyo__persons", "column": "first_event_on"}] | [] | False |
| B1 | MAX(last_event_on) | [{"table": "klaviyo__persons", "column": "last_event_on"}] | [] | False |


## S16

类别 `data`；来源 `query_db`；调用 `389434383a3e4774b11c09431c5e3a61`；状态 `success`。

```sql
SELECT COUNT(DISTINCT campaign_id) AS n_camp, COUNT(*) AS n_rows, COUNT(DISTINCT source_relation) AS n_src
FROM klaviyo__campaigns
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-093/attempt-01/sql/S16.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-093/attempt-01/sql/S16.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-093/attempt-01/results/S16.rows.jsonl)；完整：True；SHA256：`05a40f49fae396e433746d9a100b9341afe6b19aedfae387a7f5d88f64eb8994`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "klaviyo__campaigns", "kind": "base", "block": null, "base_tables": ["klaviyo__campaigns"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(DISTINCT campaign_id) | [{"table": "klaviyo__campaigns", "column": "campaign_id"}] | [] | False |
| B1 | COUNT(*) | [] | [] | True |
| B1 | COUNT(DISTINCT source_relation) | [{"table": "klaviyo__campaigns", "column": "source_relation"}] | [] | False |


## S17

类别 `data`；来源 `query_db`；调用 `26123b01f268419da99d2dd3acc51486`；状态 `success`。

```sql
SELECT person_id, timezone, count_received_email, count_opened_email, email_open_rate, active_retention_rate_week, active_retention_rate_month, first_event_on, last_event_on, active_weeks, weeks_span
FROM klaviyo__persons
ORDER BY person_id LIMIT 20
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-093/attempt-01/sql/S17.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-093/attempt-01/sql/S17.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-093/attempt-01/results/S17.rows.jsonl)；完整：True；SHA256：`634f456002ccf0c775aefcbf065775d98770a15196d20de84b39286e2325cb82`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "klaviyo__persons", "kind": "base", "block": null, "base_tables": ["klaviyo__persons"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |


## S18

类别 `data`；来源 `query_db`；调用 `8f6128ea67624a4c90c8552b46aec469`；状态 `success`。

```sql
SELECT campaign_name, active_days, total_placed_orders, total_amount_positive, email_open_rate, email_click_to_open_rate, product_view_to_order_rate_campaign, gmv_net_campaign
FROM klaviyo__campaigns
LIMIT 10
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-093/attempt-01/sql/S18.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-093/attempt-01/sql/S18.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-093/attempt-01/results/S18.rows.jsonl)；完整：True；SHA256：`dd79442332d5abbb120e3a0b7cdc6f5ddeb92d4146f9e119aefd5a0830b4f719`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "klaviyo__campaigns", "kind": "base", "block": null, "base_tables": ["klaviyo__campaigns"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |


## S19

类别 `data`；来源 `query_db`；调用 `72d317a0266b4c8f91507249857de37c`；状态 `success`。

```sql
SELECT
  campaign_id,
  campaign_name,
  SUBJECT,
  is_archived,
  variation_id,
  total_count_unique_people,
  count_received_email,
  count_opened_email,
  count_clicked_email,
  email_open_rate,
  email_click_to_open_rate,
  SENT_AT,
  strftime('%w', SENT_AT) AS dow,
  strftime('%H', SENT_AT) AS hour,
  CASE 
    WHEN CAST(strftime('%w', SENT_AT) AS INTEGER) BETWEEN 1 AND 5 THEN 'weekday'
    WHEN CAST(strftime('%w', SENT_AT) AS INTEGER) IN (0,6) THEN 'weekend'
  END AS actual_day_type,
  CASE 
    WHEN CAST(strftime('%H', SENT_AT) AS INTEGER) BETWEEN 6 AND 11 THEN 'morning'
    WHEN CAST(strftime('%H', SENT_AT) AS INTEGER) BETWEEN 12 AND 17 THEN 'afternoon'
    WHEN CAST(strftime('%H', SENT_AT) AS INTEGER) BETWEEN 18 AND 23 THEN 'evening'
    ELSE 'night'
  END AS actual_time_of_day,
  active_days,
  total_placed_orders,
  gmv_net,
  product_view_to_order_rate_campaign
FROM klaviyo__campaigns
ORDER BY campaign_id
LIMIT 5
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-093/attempt-01/sql/S19.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-093/attempt-01/sql/S19.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-093/attempt-01/results/S19.rows.jsonl)；完整：True；SHA256：`aa275ca724210630800fddc517614c5c228335a33fadc576dcab2501667dcc03`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "klaviyo__campaigns", "kind": "base", "block": null, "base_tables": ["klaviyo__campaigns"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |


## S20

类别 `data`；来源 `query_db`；调用 `58123f7b4cd14f429a9743ec83fc22e5`；状态 `success`。

```sql
SELECT
  campaign_id,
  campaign_name,
  SUBJECT,
  CASE 
    WHEN campaign_name LIKE '%工作日-上午%' THEN 'weekday_morning'
    WHEN campaign_name LIKE '%工作日-下午%' THEN 'weekday_afternoon'
    WHEN campaign_name LIKE '%工作日-晚间%' THEN 'weekday_evening'
    WHEN campaign_name LIKE '%周末-上午%' THEN 'weekend_morning'
    WHEN campaign_name LIKE '%周末-晚间%' THEN 'weekend_evening'
    WHEN campaign_name LIKE '%节前-下午%' THEN 'pre_holiday_afternoon'
    ELSE 'other'
  END AS planned_timing,
  CASE 
    WHEN SUBJECT LIKE '%折扣%' THEN 'discount'
    WHEN SUBJECT LIKE '%新品%' THEN 'new_product'
    WHEN SUBJECT LIKE '%品牌%' OR SUBJECT LIKE '%故事%' THEN 'storytelling'
    ELSE 'other'
  END AS subject_keyword,
  SENT_AT,
  strftime('%w', SENT_AT) AS dow,
  strftime('%H', SENT_AT) AS hour,
  is_archived,
  variation_id,
  total_count_unique_people,
  count_received_email,
  email_open_rate,
  email_click_to_open_rate,
  total_placed_orders,
  gmv_net,
  product_view_to_order_rate_campaign,
  active_days
FROM klaviyo__campaigns
ORDER BY campaign_id
LIMIT 10
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-093/attempt-01/sql/S20.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-093/attempt-01/sql/S20.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-093/attempt-01/results/S20.rows.jsonl)；完整：True；SHA256：`155e25b5d78fdc78076880fc37719dd974f2dd717cac4d34543148442c99bc45`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "klaviyo__campaigns", "kind": "base", "block": null, "base_tables": ["klaviyo__campaigns"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |


## S21

类别 `data`；来源 `query_db`；调用 `a9640b5dae3c49f3be8a69fb218ccb83`；状态 `success`。

```sql
SELECT planned_timing, 
       ROUND(AVG(email_open_rate), 4) AS avg_open,
       ROUND(AVG(email_click_to_open_rate), 4) AS avg_ctor,
       ROUND(AVG(total_placed_orders), 1) AS avg_orders,
       ROUND(AVG(gmv_net), 1) AS avg_gmv,
       COUNT(*) AS n
FROM (
  SELECT
    CASE 
      WHEN campaign_name LIKE '%工作日-上午%' THEN 'weekday_morning'
      WHEN campaign_name LIKE '%工作日-下午%' THEN 'weekday_afternoon'
      WHEN campaign_name LIKE '%工作日-晚间%' THEN 'weekday_evening'
      WHEN campaign_name LIKE '%周末-上午%' THEN 'weekend_morning'
      WHEN campaign_name LIKE '%周末-晚间%' THEN 'weekend_evening'
      WHEN campaign_name LIKE '%节前-下午%' THEN 'pre_holiday_afternoon'
      ELSE 'other'
    END AS planned_timing,
    email_open_rate, email_click_to_open_rate, total_placed_orders, gmv_net
  FROM klaviyo__campaigns
)
GROUP BY planned_timing
ORDER BY avg_open DESC
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-093/attempt-01/sql/S21.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-093/attempt-01/sql/S21.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-093/attempt-01/results/S21.rows.jsonl)；完整：True；SHA256：`83a39c73a291890fd6314f5d536ff90fe4107d1e6b858d252e7988b7dc277e49`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "klaviyo__campaigns", "kind": "base", "block": null, "base_tables": ["klaviyo__campaigns"]}] | [] | [] |
| B2 | [{"alias": "", "kind": "derived", "block": "B1", "base_tables": ["klaviyo__campaigns"]}] | [] | ["planned_timing"] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B2 | COUNT(*) | [] | [] | True |
| B2 | AVG(email_open_rate) | [{"table": "klaviyo__campaigns", "column": "email_open_rate"}] | [] | False |
| B2 | AVG(email_click_to_open_rate) | [{"table": "klaviyo__campaigns", "column": "email_click_to_open_rate"}] | [] | False |
| B2 | AVG(total_placed_orders) | [{"table": "klaviyo__campaigns", "column": "total_placed_orders"}] | [] | False |
| B2 | AVG(gmv_net) | [{"table": "klaviyo__campaigns", "column": "gmv_net"}] | [] | False |


## S22

类别 `data`；来源 `query_db`；调用 `db49b962ea1e43e285f025ec973188ed`；状态 `success`。

```sql
SELECT subject_keyword, 
       ROUND(AVG(email_open_rate), 4) AS avg_open,
       ROUND(AVG(email_click_to_open_rate), 4) AS avg_ctor,
       ROUND(AVG(total_placed_orders), 1) AS avg_orders,
       ROUND(AVG(gmv_net), 1) AS avg_gmv,
       COUNT(*) AS n
FROM (
  SELECT
    CASE 
      WHEN SUBJECT LIKE '%折扣%' THEN 'discount'
      WHEN SUBJECT LIKE '%新品%' THEN 'new_product'
      WHEN SUBJECT LIKE '%故事%' OR SUBJECT LIKE '%品牌%' THEN 'storytelling'
      ELSE 'other'
    END AS subject_keyword,
    email_open_rate, email_click_to_open_rate, total_placed_orders, gmv_net
  FROM klaviyo__campaigns
)
GROUP BY subject_keyword
ORDER BY avg_open DESC
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-093/attempt-01/sql/S22.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-093/attempt-01/sql/S22.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-093/attempt-01/results/S22.rows.jsonl)；完整：True；SHA256：`854010949536356102480d97e3c2b25de52668d46044977ae244317b14d0824c`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "klaviyo__campaigns", "kind": "base", "block": null, "base_tables": ["klaviyo__campaigns"]}] | [] | [] |
| B2 | [{"alias": "", "kind": "derived", "block": "B1", "base_tables": ["klaviyo__campaigns"]}] | [] | ["subject_keyword"] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B2 | COUNT(*) | [] | [] | True |
| B2 | AVG(email_open_rate) | [{"table": "klaviyo__campaigns", "column": "email_open_rate"}] | [] | False |
| B2 | AVG(email_click_to_open_rate) | [{"table": "klaviyo__campaigns", "column": "email_click_to_open_rate"}] | [] | False |
| B2 | AVG(total_placed_orders) | [{"table": "klaviyo__campaigns", "column": "total_placed_orders"}] | [] | False |
| B2 | AVG(gmv_net) | [{"table": "klaviyo__campaigns", "column": "gmv_net"}] | [] | False |


## S23

类别 `data`；来源 `query_db`；调用 `dcd6ac03cc3e4604ac4e4841f098a9eb`；状态 `success`。

```sql
SELECT planned_timing, subject_keyword,
       ROUND(AVG(email_open_rate), 4) AS avg_open,
       ROUND(AVG(email_click_to_open_rate), 4) AS avg_ctor,
       ROUND(AVG(total_placed_orders), 1) AS avg_orders,
       ROUND(AVG(gmv_net), 1) AS avg_gmv,
       ROUND(AVG(product_view_to_order_rate_campaign), 4) AS avg_conv,
       COUNT(*) AS n
FROM (
  SELECT
    CASE 
      WHEN campaign_name LIKE '%工作日-上午%' THEN 'weekday_morning'
      WHEN campaign_name LIKE '%工作日-下午%' THEN 'weekday_afternoon'
      WHEN campaign_name LIKE '%工作日-晚间%' THEN 'weekday_evening'
      WHEN campaign_name LIKE '%周末-上午%' THEN 'weekend_morning'
      WHEN campaign_name LIKE '%周末-晚间%' THEN 'weekend_evening'
      WHEN campaign_name LIKE '%节前-下午%' THEN 'pre_holiday_afternoon'
      ELSE 'other'
    END AS planned_timing,
    CASE 
      WHEN SUBJECT LIKE '%折扣%' THEN 'discount'
      WHEN SUBJECT LIKE '%新品%' THEN 'new_product'
      WHEN SUBJECT LIKE '%故事%' OR SUBJECT LIKE '%品牌%' THEN 'storytelling'
      ELSE 'other'
    END AS subject_keyword,
    email_open_rate, email_click_to_open_rate, total_placed_orders, gmv_net, product_view_to_order_rate_campaign
  FROM klaviyo__campaigns
)
GROUP BY planned_timing, subject_keyword
ORDER BY avg_open DESC
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-093/attempt-01/sql/S23.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-093/attempt-01/sql/S23.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-093/attempt-01/results/S23.rows.jsonl)；完整：True；SHA256：`c6813317067bf7f9ce6ed2719a9c29b125fc47d43d46606608bab2b4ecfccdef`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "klaviyo__campaigns", "kind": "base", "block": null, "base_tables": ["klaviyo__campaigns"]}] | [] | [] |
| B2 | [{"alias": "", "kind": "derived", "block": "B1", "base_tables": ["klaviyo__campaigns"]}] | [] | ["planned_timing", "subject_keyword"] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B2 | COUNT(*) | [] | [] | True |
| B2 | AVG(email_open_rate) | [{"table": "klaviyo__campaigns", "column": "email_open_rate"}] | [] | False |
| B2 | AVG(email_click_to_open_rate) | [{"table": "klaviyo__campaigns", "column": "email_click_to_open_rate"}] | [] | False |
| B2 | AVG(total_placed_orders) | [{"table": "klaviyo__campaigns", "column": "total_placed_orders"}] | [] | False |
| B2 | AVG(gmv_net) | [{"table": "klaviyo__campaigns", "column": "gmv_net"}] | [] | False |
| B2 | AVG(product_view_to_order_rate_campaign) | [{"table": "klaviyo__campaigns", "column": "product_view_to_order_rate_campaign"}] | [] | False |


## S24

类别 `data`；来源 `query_db`；调用 `57bfdf2c080d4ca68a8234dd18902342`；状态 `success`。

```sql
SELECT is_archived, planned_timing, subject_keyword,
       ROUND(AVG(email_open_rate), 4) AS avg_open,
       ROUND(AVG(email_click_to_open_rate), 4) AS avg_ctor,
       COUNT(*) AS n
FROM (
  SELECT
    is_archived,
    CASE 
      WHEN campaign_name LIKE '%工作日-上午%' THEN 'weekday_morning'
      WHEN campaign_name LIKE '%工作日-下午%' THEN 'weekday_afternoon'
      WHEN campaign_name LIKE '%工作日-晚间%' THEN 'weekday_evening'
      WHEN campaign_name LIKE '%周末-上午%' THEN 'weekend_morning'
      WHEN campaign_name LIKE '%周末-晚间%' THEN 'weekend_evening'
      WHEN campaign_name LIKE '%节前-下午%' THEN 'pre_holiday_afternoon'
      ELSE 'other'
    END AS planned_timing,
    CASE 
      WHEN SUBJECT LIKE '%折扣%' THEN 'discount'
      WHEN SUBJECT LIKE '%新品%' THEN 'new_product'
      WHEN SUBJECT LIKE '%故事%' OR SUBJECT LIKE '%品牌%' THEN 'storytelling'
      ELSE 'other'
    END AS subject_keyword,
    email_open_rate, email_click_to_open_rate
  FROM klaviyo__campaigns
)
GROUP BY is_archived, planned_timing, subject_keyword
ORDER BY is_archived, avg_open DESC
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-093/attempt-01/sql/S24.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-093/attempt-01/sql/S24.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-093/attempt-01/results/S24.rows.jsonl)；完整：True；SHA256：`baa3b2a426568f09ce127c6f6a6aa3423f51b8bea24aacb11c4742a87799ec3a`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "klaviyo__campaigns", "kind": "base", "block": null, "base_tables": ["klaviyo__campaigns"]}] | [] | [] |
| B2 | [{"alias": "", "kind": "derived", "block": "B1", "base_tables": ["klaviyo__campaigns"]}] | [] | ["is_archived", "planned_timing", "subject_keyword"] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B2 | COUNT(*) | [] | [] | True |
| B2 | AVG(email_open_rate) | [{"table": "klaviyo__campaigns", "column": "email_open_rate"}] | [] | False |
| B2 | AVG(email_click_to_open_rate) | [{"table": "klaviyo__campaigns", "column": "email_click_to_open_rate"}] | [] | False |


## S25

类别 `data`；来源 `query_db`；调用 `e5e728f795c8466f83704fa1b4ded76e`；状态 `success`。

```sql
SELECT variation_id, planned_timing, subject_keyword,
       ROUND(AVG(email_open_rate), 4) AS avg_open,
       ROUND(AVG(email_click_to_open_rate), 4) AS avg_ctor,
       ROUND(AVG(total_count_unique_people), 0) AS avg_audience,
       COUNT(*) AS n
FROM (
  SELECT
    variation_id,
    CASE 
      WHEN campaign_name LIKE '%工作日-上午%' THEN 'weekday_morning'
      WHEN campaign_name LIKE '%工作日-下午%' THEN 'weekday_afternoon'
      WHEN campaign_name LIKE '%工作日-晚间%' THEN 'weekday_evening'
      WHEN campaign_name LIKE '%周末-上午%' THEN 'weekend_morning'
      WHEN campaign_name LIKE '%周末-晚间%' THEN 'weekend_evening'
      WHEN campaign_name LIKE '%节前-下午%' THEN 'pre_holiday_afternoon'
      ELSE 'other'
    END AS planned_timing,
    CASE 
      WHEN SUBJECT LIKE '%折扣%' THEN 'discount'
      WHEN SUBJECT LIKE '%新品%' THEN 'new_product'
      WHEN SUBJECT LIKE '%故事%' OR SUBJECT LIKE '%品牌%' THEN 'storytelling'
      ELSE 'other'
    END AS subject_keyword,
    email_open_rate, email_click_to_open_rate, total_count_unique_people
  FROM klaviyo__campaigns
)
GROUP BY variation_id, planned_timing, subject_keyword
ORDER BY variation_id, avg_open DESC
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-093/attempt-01/sql/S25.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-093/attempt-01/sql/S25.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-093/attempt-01/results/S25.rows.jsonl)；完整：True；SHA256：`01d7822dea875e2ab5d832830ed575f9e26cb23d616777fbda1adf4219020232`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "klaviyo__campaigns", "kind": "base", "block": null, "base_tables": ["klaviyo__campaigns"]}] | [] | [] |
| B2 | [{"alias": "", "kind": "derived", "block": "B1", "base_tables": ["klaviyo__campaigns"]}] | [] | ["variation_id", "planned_timing", "subject_keyword"] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B2 | COUNT(*) | [] | [] | True |
| B2 | AVG(email_open_rate) | [{"table": "klaviyo__campaigns", "column": "email_open_rate"}] | [] | False |
| B2 | AVG(email_click_to_open_rate) | [{"table": "klaviyo__campaigns", "column": "email_click_to_open_rate"}] | [] | False |
| B2 | AVG(total_count_unique_people) | [{"table": "klaviyo__campaigns", "column": "total_count_unique_people"}] | [] | False |


## S26

类别 `data`；来源 `query_db`；调用 `56d19123e86b4b428288200a69e25802`；状态 `success`。

```sql
SELECT
  ROUND(AVG(count_received_email), 0) AS avg_received,
  ROUND(AVG(total_count_unique_people), 0) AS avg_audience,
  ROUND(AVG(count_received_email) / NULLIF(AVG(total_count_unique_people), 0), 2) AS received_ratio,
  MIN(count_received_email) AS min_rec,
  MAX(count_received_email) AS max_rec,
  AVG(email_open_rate) AS avg_open,
  AVG(email_click_to_open_rate) AS avg_ctor
FROM klaviyo__campaigns
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-093/attempt-01/sql/S26.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-093/attempt-01/sql/S26.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-093/attempt-01/results/S26.rows.jsonl)；完整：True；SHA256：`697a2d66a92aff3fda854e37baca907b0bebf412908efe74b1cdafbb56ebcd5e`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "klaviyo__campaigns", "kind": "base", "block": null, "base_tables": ["klaviyo__campaigns"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | MIN(count_received_email) | [{"table": "klaviyo__campaigns", "column": "count_received_email"}] | [] | False |
| B1 | MAX(count_received_email) | [{"table": "klaviyo__campaigns", "column": "count_received_email"}] | [] | False |
| B1 | AVG(email_open_rate) | [{"table": "klaviyo__campaigns", "column": "email_open_rate"}] | [] | False |
| B1 | AVG(email_click_to_open_rate) | [{"table": "klaviyo__campaigns", "column": "email_click_to_open_rate"}] | [] | False |
| B1 | AVG(count_received_email) | [{"table": "klaviyo__campaigns", "column": "count_received_email"}] | [] | False |
| B1 | AVG(total_count_unique_people) | [{"table": "klaviyo__campaigns", "column": "total_count_unique_people"}] | [] | False |
| B1 | AVG(count_received_email) | [{"table": "klaviyo__campaigns", "column": "count_received_email"}] | [] | False |
| B1 | AVG(total_count_unique_people) | [{"table": "klaviyo__campaigns", "column": "total_count_unique_people"}] | [] | False |


## S27

类别 `data`；来源 `query_db`；调用 `24c36bc1d3b348689f685a2cfc1b83dd`；状态 `success`。

```sql
SELECT * FROM (
  SELECT
    count_received_email,
    total_count_unique_people,
    count_received_email / NULLIF(total_count_unique_people, 0) AS ratio,
    email_open_rate,
    email_click_to_open_rate,
    campaign_name,
    is_archived,
    variation_id,
    NTILE(100) OVER (ORDER BY count_received_email) AS pct
  FROM klaviyo__campaigns
)
WHERE pct >= 98 OR pct <= 2
ORDER BY count_received_email DESC
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-093/attempt-01/sql/S27.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-093/attempt-01/sql/S27.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-093/attempt-01/results/S27.rows.jsonl)；完整：True；SHA256：`7705c57cccc3f1695222896afda4d3a24ed8969670dafe99bd9cfff9107fa9ab`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "klaviyo__campaigns", "kind": "base", "block": null, "base_tables": ["klaviyo__campaigns"]}] | [] | [] |
| B2 | [{"alias": "", "kind": "derived", "block": "B1", "base_tables": ["klaviyo__campaigns"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |


## S28

类别 `data`；来源 `query_db`；调用 `256f5c04ab084ba2bff674ce68cc67b5`；状态 `failed`。

```sql
SELECT
  PERCENTILE_25(count_received_email) OVER() AS p25,
  PERCENTILE_75(count_received_email) OVER() AS p75,
  MIN(count_received_email) OVER() AS min_val,
  MAX(count_received_email) OVER() AS max_val,
  AVG(count_received_email) OVER() AS mean_val
FROM klaviyo__campaigns
LIMIT 1
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-093/attempt-01/sql/S28.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-093/attempt-01/sql/S28.parameters.json)。

错误：`OperationalError('no such function: PERCENTILE_25')`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "klaviyo__campaigns", "kind": "base", "block": null, "base_tables": ["klaviyo__campaigns"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |


## S29

类别 `data`；来源 `query_db`；调用 `76fd201001514166a40c583f3419b5ce`；状态 `success`。

```sql
SELECT
  ROUND(AVG(CASE WHEN row_num <= CAST(0.25 * total AS INTEGER) THEN count_received_email END), 0) AS p25,
  ROUND(AVG(CASE WHEN row_num <= CAST(0.75 * total AS INTEGER) THEN count_received_email END), 0) AS p75
FROM (
  SELECT count_received_email,
         ROW_NUMBER() OVER (ORDER BY count_received_email) AS row_num,
         COUNT(*) OVER () AS total
  FROM klaviyo__campaigns
)
LIMIT 1
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-093/attempt-01/sql/S29.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-093/attempt-01/sql/S29.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-093/attempt-01/results/S29.rows.jsonl)；完整：True；SHA256：`f29ddb701f524cac16d43b3a4c9bc181a21810b9fd36eb82a98af9cd45b83754`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "klaviyo__campaigns", "kind": "base", "block": null, "base_tables": ["klaviyo__campaigns"]}] | [] | [] |
| B2 | [{"alias": "", "kind": "derived", "block": "B1", "base_tables": ["klaviyo__campaigns"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B2 | AVG(CASE WHEN row_num <= CAST(0.25 * total AS INTEGER) THEN count_received_email END) | [{"table": "klaviyo__campaigns", "column": "count_received_email"}] | [{"table": "klaviyo__campaigns", "column": "count_received_email"}] | False |
| B2 | AVG(CASE WHEN row_num <= CAST(0.75 * total AS INTEGER) THEN count_received_email END) | [{"table": "klaviyo__campaigns", "column": "count_received_email"}] | [{"table": "klaviyo__campaigns", "column": "count_received_email"}] | False |


## S30

类别 `data`；来源 `query_db`；调用 `39c2cc0bcd4e4ef3a3a4a5efc59cf3c2`；状态 `success`。

```sql
SELECT
  MIN(count_received_email) AS min_val,
  ROUND(AVG(count_received_email), 0) AS mean_val,
  MAX(count_received_email) AS max_val
FROM klaviyo__campaigns
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-093/attempt-01/sql/S30.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-093/attempt-01/sql/S30.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-093/attempt-01/results/S30.rows.jsonl)；完整：True；SHA256：`a1e62efc54edfdb041d7acaee5f15837e9a891897e4c5058943f443fc034c025`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "klaviyo__campaigns", "kind": "base", "block": null, "base_tables": ["klaviyo__campaigns"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | MIN(count_received_email) | [{"table": "klaviyo__campaigns", "column": "count_received_email"}] | [] | False |
| B1 | MAX(count_received_email) | [{"table": "klaviyo__campaigns", "column": "count_received_email"}] | [] | False |
| B1 | AVG(count_received_email) | [{"table": "klaviyo__campaigns", "column": "count_received_email"}] | [] | False |


## S31

类别 `data`；来源 `query_db`；调用 `c6ed222a218c4187a713bfd2c3159ff5`；状态 `success`。

```sql
SELECT timezone, COUNT(*) AS n,
       ROUND(AVG(active_retention_rate_week), 4) AS avg_ret_week,
       ROUND(AVG(active_retention_rate_month), 4) AS avg_ret_month,
       ROUND(AVG(email_open_rate), 4) AS avg_open_rate,
       ROUND(AVG(count_received_email), 0) AS avg_received,
       ROUND(AVG(count_opened_email), 0) AS avg_opened
FROM klaviyo__persons
GROUP BY timezone
ORDER BY n DESC
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-093/attempt-01/sql/S31.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-093/attempt-01/sql/S31.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-093/attempt-01/results/S31.rows.jsonl)；完整：True；SHA256：`7c007261cfc08eb66aadae9711937037ae3e547e5a95d8cac05240eb925920f4`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "klaviyo__persons", "kind": "base", "block": null, "base_tables": ["klaviyo__persons"]}] | [] | ["timezone"] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |
| B1 | AVG(active_retention_rate_week) | [{"table": "klaviyo__persons", "column": "active_retention_rate_week"}] | [] | False |
| B1 | AVG(active_retention_rate_month) | [{"table": "klaviyo__persons", "column": "active_retention_rate_month"}] | [] | False |
| B1 | AVG(email_open_rate) | [{"table": "klaviyo__persons", "column": "email_open_rate"}] | [] | False |
| B1 | AVG(count_received_email) | [{"table": "klaviyo__persons", "column": "count_received_email"}] | [] | False |
| B1 | AVG(count_opened_email) | [{"table": "klaviyo__persons", "column": "count_opened_email"}] | [] | False |


## S32

类别 `data`；来源 `query_db`；调用 `57d1a38b0f334d258d51ca726238fc01`；状态 `success`。

```sql
SELECT
  CASE 
    WHEN count_received_email < 100 THEN 'low (<100)'
    WHEN count_received_email < 150 THEN 'medium (100-150)'
    ELSE 'high (150+)'
  END AS email_volume_group,
  COUNT(*) AS n,
  ROUND(AVG(active_retention_rate_week), 4) AS avg_ret_week,
  ROUND(AVG(active_retention_rate_month), 4) AS avg_ret_month,
  ROUND(AVG(email_open_rate), 4) AS avg_open_rate
FROM klaviyo__persons
GROUP BY 1
ORDER BY AVG(active_retention_rate_week) DESC
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-093/attempt-01/sql/S32.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-093/attempt-01/sql/S32.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-093/attempt-01/results/S32.rows.jsonl)；完整：True；SHA256：`edf73d2ddfe3b7b467d4261e24f9d15ffd4b65ab249b88426bc788c15f747a5b`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "klaviyo__persons", "kind": "base", "block": null, "base_tables": ["klaviyo__persons"]}] | [] | ["CASE WHEN count_received_email < 100 THEN 'low (<100)' WHEN count_received_email < 150 THEN 'medium (100-150)' ELSE 'high (150+)' END"] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |
| B1 | AVG(active_retention_rate_week) | [{"table": "klaviyo__persons", "column": "active_retention_rate_week"}] | [] | False |
| B1 | AVG(active_retention_rate_month) | [{"table": "klaviyo__persons", "column": "active_retention_rate_month"}] | [] | False |
| B1 | AVG(email_open_rate) | [{"table": "klaviyo__persons", "column": "email_open_rate"}] | [] | False |
| B1 | AVG(active_retention_rate_week) | [{"table": "klaviyo__persons", "column": "active_retention_rate_week"}] | [] | False |


## S33

类别 `data`；来源 `query_db`；调用 `e3e89ae70b0e4319b613477f3dba88d4`；状态 `success`。

```sql
SELECT
  (SELECT COUNT(*) FROM klaviyo__persons) AS n_persons,
  (SELECT ROUND(SUM(count_received_email),0) FROM klaviyo__persons) AS sum_person_received,
  (SELECT ROUND(AVG(count_received_email),0) FROM klaviyo__campaigns) AS avg_campaign_received,
  (SELECT COUNT(*) FROM klaviyo__campaigns) AS n_campaigns,
  (SELECT ROUND(SUM(count_opened_email),0) FROM klaviyo__persons) AS sum_person_opened,
  (SELECT ROUND(AVG(count_opened_email),0) FROM klaviyo__campaigns) AS avg_campaign_opened
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-093/attempt-01/sql/S33.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-093/attempt-01/sql/S33.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-093/attempt-01/results/S33.rows.jsonl)；完整：True；SHA256：`cde770e2c836f4e8d0c56165e17fb1c60cf03313250681b99a17d122a9a86bc9`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "klaviyo__persons", "kind": "base", "block": null, "base_tables": ["klaviyo__persons"]}] | [] | [] |
| B2 | [{"alias": "klaviyo__persons", "kind": "base", "block": null, "base_tables": ["klaviyo__persons"]}] | [] | [] |
| B3 | [{"alias": "klaviyo__campaigns", "kind": "base", "block": null, "base_tables": ["klaviyo__campaigns"]}] | [] | [] |
| B4 | [{"alias": "klaviyo__campaigns", "kind": "base", "block": null, "base_tables": ["klaviyo__campaigns"]}] | [] | [] |
| B5 | [{"alias": "klaviyo__persons", "kind": "base", "block": null, "base_tables": ["klaviyo__persons"]}] | [] | [] |
| B6 | [{"alias": "klaviyo__campaigns", "kind": "base", "block": null, "base_tables": ["klaviyo__campaigns"]}] | [] | [] |
| B7 | [] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |
| B2 | SUM(count_received_email) | [{"table": "klaviyo__persons", "column": "count_received_email"}] | [] | False |
| B3 | AVG(count_received_email) | [{"table": "klaviyo__campaigns", "column": "count_received_email"}] | [] | False |
| B4 | COUNT(*) | [] | [] | True |
| B5 | SUM(count_opened_email) | [{"table": "klaviyo__persons", "column": "count_opened_email"}] | [] | False |
| B6 | AVG(count_opened_email) | [{"table": "klaviyo__campaigns", "column": "count_opened_email"}] | [] | False |


未解析列血缘：[{"block": "B7", "column": "count_received_email", "reason": "ambiguous_or_missing_source"}, {"block": "B7", "column": "count_received_email", "reason": "ambiguous_or_missing_source"}, {"block": "B7", "column": "count_opened_email", "reason": "ambiguous_or_missing_source"}, {"block": "B7", "column": "count_opened_email", "reason": "ambiguous_or_missing_source"}]

## S34

类别 `data`；来源 `query_db`；调用 `ddf3e59106984924aabeea4c5a04e665`；状态 `success`。

```sql
SELECT campaign_id, variation_id, campaign_name, SUBJECT, SENT_AT,
       strftime('%Y-%m', SENT_AT) AS sent_month
FROM klaviyo__campaigns
ORDER BY SENT_AT
LIMIT 8
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-093/attempt-01/sql/S34.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-093/attempt-01/sql/S34.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-093/attempt-01/results/S34.rows.jsonl)；完整：True；SHA256：`27a1e0b7019d46906760db53e4d33a1cded09fb5285cc82203d1020fcab9e888`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "klaviyo__campaigns", "kind": "base", "block": null, "base_tables": ["klaviyo__campaigns"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |


## S35

类别 `data`；来源 `query_db`；调用 `b5d3303ea80140fea1049649a0e69ba6`；状态 `success`。

```sql
SELECT
  campaign_id,
  campaign_name,
  SUBJECT,
  is_archived,
  variation_id,
  SENT_AT,
  total_count_unique_people,
  count_received_email,
  count_opened_email,
  count_clicked_email,
  email_open_rate,
  email_click_to_open_rate,
  count_placed_order,
  count_placed_order / NULLIF(total_count_unique_people, 0) AS order_per_person,
  gmv_net,
  gmv_net / NULLIF(total_count_unique_people, 0) AS gmv_per_person,
  product_view_to_order_rate_campaign,
  active_days,
  total_placed_orders,
  CASE 
    WHEN campaign_name LIKE '%工作日-上午%' THEN 'weekday_morning'
    WHEN campaign_name LIKE '%工作日-下午%' THEN 'weekday_afternoon'
    WHEN campaign_name LIKE '%工作日-晚间%' THEN 'weekday_evening'
    WHEN campaign_name LIKE '%周末-上午%' THEN 'weekend_morning'
    WHEN campaign_name LIKE '%周末-晚间%' THEN 'weekend_evening'
    WHEN campaign_name LIKE '%节前-下午%' THEN 'pre_holiday_afternoon'
    ELSE 'other'
  END AS timing,
  CASE 
    WHEN campaign_name LIKE '%工作日%' THEN 'weekday'
    WHEN campaign_name LIKE '%周末%' THEN 'weekend'
    WHEN campaign_name LIKE '%节前%' THEN 'pre_holiday'
    ELSE 'other'
  END AS day_context,
  CASE 
    WHEN campaign_name LIKE '%-上午%' THEN 'morning'
    WHEN campaign_name LIKE '%-下午%' THEN 'afternoon'
    WHEN campaign_name LIKE '%-晚间%' THEN 'evening'
    ELSE 'other'
  END AS time_of_day,
  CASE 
    WHEN SUBJECT LIKE '%折扣%' THEN 'discount'
    WHEN SUBJECT LIKE '%新品%' THEN 'new_product'
    WHEN SUBJECT LIKE '%故事%' THEN 'storytelling'
    ELSE 'other'
  END AS subject_group,
  strftime('%Y-%m', SENT_AT) AS sent_month,
  strftime('%w', SENT_AT) AS dow,
  CAST(strftime('%H', SENT_AT) AS INTEGER) AS hour
FROM klaviyo__campaigns
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-093/attempt-01/sql/S35.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-093/attempt-01/sql/S35.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-093/attempt-01/results/S35.rows.jsonl)；完整：True；SHA256：`6620631948882d736d646dacecd67a0fe2ba176e21abf54443cb73eb87a800d8`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "klaviyo__campaigns", "kind": "base", "block": null, "base_tables": ["klaviyo__campaigns"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |


## S36

类别 `data`；来源 `python`；调用 `f7365532ffe34c239ecaf69554b16c55`；状态 `success`。

```sql

  SELECT
    campaign_id, campaign_name, SUBJECT, is_archived, variation_id,
    SENT_AT, total_count_unique_people, count_received_email,
    count_opened_email, count_clicked_email, email_open_rate,
    email_click_to_open_rate, count_placed_order, gmv_net,
    product_view_to_order_rate_campaign, active_days, total_placed_orders,
    CASE 
      WHEN campaign_name LIKE '%工作日-上午%' THEN 'weekday_morning'
      WHEN campaign_name LIKE '%工作日-下午%' THEN 'weekday_afternoon'
      WHEN campaign_name LIKE '%工作日-晚间%' THEN 'weekday_evening'
      WHEN campaign_name LIKE '%周末-上午%' THEN 'weekend_morning'
      WHEN campaign_name LIKE '%周末-晚间%' THEN 'weekend_evening'
      WHEN campaign_name LIKE '%节前-下午%' THEN 'pre_holiday_afternoon'
      ELSE 'other'
    END AS timing,
    CASE 
      WHEN SUBJECT LIKE '%折扣%' THEN 'discount'
      WHEN SUBJECT LIKE '%新品%' THEN 'new_product'
      WHEN SUBJECT LIKE '%故事%' THEN 'storytelling'
      ELSE 'other'
    END AS subject_group,
    strftime('%Y-%m', SENT_AT) AS sent_month
  FROM klaviyo__campaigns

```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-093/attempt-01/sql/S36.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-093/attempt-01/sql/S36.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-093/attempt-01/results/S36.rows.jsonl)；完整：True；SHA256：`83449e52bec2e8971b1a3c9e31854515afd5df37d075feea64a466ca7e84ab12`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "klaviyo__campaigns", "kind": "base", "block": null, "base_tables": ["klaviyo__campaigns"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |


## S37

类别 `data`；来源 `python`；调用 `cb64c3e10cde466b81b2d2bf149c2436`；状态 `success`。

```sql

  SELECT person_id, timezone, 
         count_received_email, count_opened_email, count_clicked_email,
         email_open_rate, 
         active_retention_rate_week, active_retention_rate_month,
         active_days, active_weeks, active_months,
         days_span, weeks_span, months_span,
         has_7day_retention, has_30day_retention,
         count_placed_order, count_ordered_product,
         sum_revenue_placed_order, sum_revenue_ordered_product,
         first_event_on, last_event_on
  FROM klaviyo__persons

```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-093/attempt-01/sql/S37.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-093/attempt-01/sql/S37.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-093/attempt-01/results/S37.rows.jsonl)；完整：True；SHA256：`270cad8e8614b6fb58d1fae78eaf42c05db6dc94078090694ef22fa89608d0ac`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "klaviyo__persons", "kind": "base", "block": null, "base_tables": ["klaviyo__persons"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |


## S38

类别 `data`；来源 `query_db`；调用 `b50653d789b040769f0a8ac60fc56b7d`；状态 `success`。

```sql
SELECT
  planned_timing,
  CASE 
    WHEN CAST(strftime('%w', SENT_AT) AS INTEGER) BETWEEN 1 AND 5 THEN 'weekday'
    ELSE 'weekend'
  END AS actual_day_type,
  CASE 
    WHEN CAST(strftime('%H', SENT_AT) AS INTEGER) BETWEEN 6 AND 11 THEN 'morning'
    WHEN CAST(strftime('%H', SENT_AT) AS INTEGER) BETWEEN 12 AND 17 THEN 'afternoon'
    WHEN CAST(strftime('%H', SENT_AT) AS INTEGER) BETWEEN 18 AND 23 THEN 'evening'
    ELSE 'night'
  END AS actual_time,
  COUNT(*) AS n,
  ROUND(AVG(email_open_rate), 4) AS avg_open,
  ROUND(AVG(email_click_to_open_rate), 4) AS avg_ctor
FROM (
  SELECT
    CASE 
      WHEN campaign_name LIKE '%工作日-上午%' THEN 'weekday_morning'
      WHEN campaign_name LIKE '%工作日-下午%' THEN 'weekday_afternoon'
      WHEN campaign_name LIKE '%工作日-晚间%' THEN 'weekday_evening'
      WHEN campaign_name LIKE '%周末-上午%' THEN 'weekend_morning'
      WHEN campaign_name LIKE '%周末-晚间%' THEN 'weekend_evening'
      WHEN campaign_name LIKE '%节前-下午%' THEN 'pre_holiday_afternoon'
      ELSE 'other'
    END AS planned_timing,
    SENT_AT, email_open_rate, email_click_to_open_rate
  FROM klaviyo__campaigns
)
GROUP BY planned_timing, actual_day_type, actual_time
ORDER BY planned_timing, actual_day_type, actual_time
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-093/attempt-01/sql/S38.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-093/attempt-01/sql/S38.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-093/attempt-01/results/S38.rows.jsonl)；完整：True；SHA256：`b109435484e009a94150b53c51c9d4174255e7599aa5b6af849171592a96c5cb`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "klaviyo__campaigns", "kind": "base", "block": null, "base_tables": ["klaviyo__campaigns"]}] | [] | [] |
| B2 | [{"alias": "", "kind": "derived", "block": "B1", "base_tables": ["klaviyo__campaigns"]}] | [] | ["planned_timing", "CASE WHEN CAST(STRFTIME('%w', SENT_AT) AS INTEGER) BETWEEN 1 AND 5 THEN 'weekday' ELSE 'weekend' END", "CASE WHEN CAST(STRFTIME('%H', SENT_AT) AS INTEGER) BETWEEN 6 AND 11 THEN 'morning' WHEN CAST(STRFTIME('%H', SENT_AT) AS INTEGER) BETWEEN 12 AND 17 THEN 'afternoon' WHEN CAST(STRFTIME('%H', SENT_AT) AS INTEGER) BETWEEN 18 AND 23 THEN 'evening' ELSE 'night' END"] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B2 | COUNT(*) | [] | [] | True |
| B2 | AVG(email_open_rate) | [{"table": "klaviyo__campaigns", "column": "email_open_rate"}] | [] | False |
| B2 | AVG(email_click_to_open_rate) | [{"table": "klaviyo__campaigns", "column": "email_click_to_open_rate"}] | [] | False |


## S39

类别 `data`；来源 `query_db`；调用 `012609d12c3e4ffcb7c8a9f65a7cba15`；状态 `success`。

```sql
SELECT strftime('%Y-%m-%d', SENT_AT) AS send_date, strftime('%w', SENT_AT) AS dow,
       campaign_name, subject_group, email_open_rate, email_click_to_open_rate,
       total_count_unique_people, count_received_email
FROM (
  SELECT SENT_AT, campaign_name,
    CASE 
      WHEN SUBJECT LIKE '%折扣%' THEN 'discount'
      WHEN SUBJECT LIKE '%新品%' THEN 'new_product'
      WHEN SUBJECT LIKE '%故事%' THEN 'storytelling'
      ELSE 'other'
    END AS subject_group,
    email_open_rate, email_click_to_open_rate, total_count_unique_people, count_received_email
  FROM klaviyo__campaigns
  WHERE campaign_name LIKE '%节前%'
)
ORDER BY SENT_AT
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-093/attempt-01/sql/S39.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-093/attempt-01/sql/S39.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-093/attempt-01/results/S39.rows.jsonl)；完整：True；SHA256：`3779caf2155370af53d57e83b99d83ccf04d4e3c3a9b1119242a3c1ca8c20789`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "klaviyo__campaigns", "kind": "base", "block": null, "base_tables": ["klaviyo__campaigns"]}] | [] | [] |
| B2 | [{"alias": "", "kind": "derived", "block": "B1", "base_tables": ["klaviyo__campaigns"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |


## S40

类别 `data`；来源 `python`；调用 `4d88f868504740a9a28628824336aa20`；状态 `success`。

```sql

  SELECT
    CASE 
      WHEN campaign_name LIKE '%工作日-上午%' THEN 'weekday_morning'
      WHEN campaign_name LIKE '%工作日-下午%' THEN 'weekday_afternoon'
      WHEN campaign_name LIKE '%工作日-晚间%' THEN 'weekday_evening'
      WHEN campaign_name LIKE '%周末-上午%' THEN 'weekend_morning'
      WHEN campaign_name LIKE '%周末-晚间%' THEN 'weekend_evening'
      WHEN campaign_name LIKE '%节前-下午%' THEN 'pre_holiday_afternoon'
      ELSE 'other'
    END AS timing,
    CASE 
      WHEN SUBJECT LIKE '%折扣%' THEN 'discount'
      WHEN SUBJECT LIKE '%新品%' THEN 'new_product'
      WHEN SUBJECT LIKE '%故事%' THEN 'storytelling'
      ELSE 'other'
    END AS subject_group,
    email_open_rate, email_click_to_open_rate, gmv_net,
    total_count_unique_people, is_archived, variation_id
  FROM klaviyo__campaigns

```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-093/attempt-01/sql/S40.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-093/attempt-01/sql/S40.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-093/attempt-01/results/S40.rows.jsonl)；完整：True；SHA256：`02b126d1ccb4b1b5d7e89825a790f85aa0b2241ab0249cc59d206453aaa55655`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "klaviyo__campaigns", "kind": "base", "block": null, "base_tables": ["klaviyo__campaigns"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |


## S41

类别 `data`；来源 `python`；调用 `29e8d5dbc8f64ce18639cf8780f9c855`；状态 `success`。

```sql

  SELECT
    CASE 
      WHEN campaign_name LIKE '%工作日-上午%' THEN 'weekday_morning'
      WHEN campaign_name LIKE '%工作日-下午%' THEN 'weekday_afternoon'
      WHEN campaign_name LIKE '%工作日-晚间%' THEN 'weekday_evening'
      WHEN campaign_name LIKE '%周末-上午%' THEN 'weekend_morning'
      WHEN campaign_name LIKE '%周末-晚间%' THEN 'weekend_evening'
      WHEN campaign_name LIKE '%节前-下午%' THEN 'pre_holiday_afternoon'
      ELSE 'other'
    END AS timing,
    CASE 
      WHEN SUBJECT LIKE '%折扣%' THEN 'discount'
      WHEN SUBJECT LIKE '%新品%' THEN 'new_product'
      WHEN SUBJECT LIKE '%故事%' THEN 'storytelling'
      ELSE 'other'
    END AS subject_group,
    email_open_rate, email_click_to_open_rate, gmv_net,
    total_count_unique_people, count_received_email, is_archived, variation_id
  FROM klaviyo__campaigns

```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-093/attempt-01/sql/S41.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-093/attempt-01/sql/S41.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-093/attempt-01/results/S41.rows.jsonl)；完整：True；SHA256：`25d9bef9b8e832452f5b829e1148bd8301bba498975bc32a36fa12bcc0c3f4a0`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "klaviyo__campaigns", "kind": "base", "block": null, "base_tables": ["klaviyo__campaigns"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |

