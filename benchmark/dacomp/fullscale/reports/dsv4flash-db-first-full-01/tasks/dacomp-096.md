# dacomp-096

Based on `klaviyo__campaigns` (with columns like `STATUS`/`STATUS_ID`, `SENT_AT`, `schedul…

运行：已提交。官方未评分。全部 SQL 尝试/成功 24/24；数据 SQL 22/22；Python 9 次。

完整原题：

Based on `klaviyo__campaigns` (with columns like `STATUS`/`STATUS_ID`, `SENT_AT`, `scheduled_to_send_at`, `EMAIL_TEMPLATE_ID`, `source_relation`, `count_received`, `count_opened`, `count_clicked`) and combined with activity metrics from `marts.klaviyo__persons`, build a campaign health framework.

Use Open Rate = `count_opened` ÷ `count_received` and Click-to-Open Rate = `count_clicked` ÷ `count_opened` as core metrics. Group the data by Campaign Type (e.g., Promotional/New Product/Storytelling) and audience size quantiles (< 10k, 10k–100k, > 100k, based on `count_received`). Calculate the mean and standard deviation of historical data from the last 6 months.

Set rules for anomaly detection: if a single campaign's metric falls below mean − 2σ or exceeds mean + 2σ, it should be flagged as an anomaly. Additionally, if the interval between a campaign's `updated_at` and the previous campaign's is < 24 hours, it should be identified as a high-frequency update anomaly. The analysis must trace the specific causes of anomalous campaigns, including sending time slot (weekday/weekend, morning/afternoon), template reuse frequency (percentage of the same `EMAIL_TEMPLATE_ID`), and copy theme (categorized by `source_relation`).

Finally, produce a diagnostic report that clearly outlines improvement directions for template governance (e.g., reduce reuse of templates with a >50% share), theme optimization (e.g., for theme types with low click-to-open rates), and sending cadence (e.g., avoid deployments with <24 hours between them). Propose at least one actionable A/B test plan (such as adjusting send time or replacing a template) and provide an estimated range for potential gains (e.g., projected 5–10% increase in open rate, 2–5% increase in click-to-open rate).

| 表 | 行数 | 列数 |
| --- | --- | --- |
| klaviyo__flows | 79 | 27 |
| klaviyo__person_campaign_flow | 4 | 32 |


实际路线（分析者依据 SQL/源码概括，不代表 Agent 自述）：SQL 数据探索、指标及分组 → Python 准备、统计和图表 → 报告

数据库大小：28,672 字节。

## 数据 SQL

| SQL | 状态 | 基础表 | Join 输入/类型 | GROUP BY | 聚合表达式 | 结果行数 | 数据库 ms |
| --- | --- | --- | --- | --- | --- | --- | --- |
| [S3/Q1](#s3) | success | ["klaviyo__flows"] | 0 / {} | [] | [] | 20 | 0.469 |
| [S4/Q2](#s4) | success | ["klaviyo__person_campaign_flow"] | 0 / {} | [] | [] | 4 | 0.382 |
| [S5/Q3](#s5) | success | ["klaviyo__flows"] | 0 / {} | [] | ["COUNT(*)", "MIN(created_at)", "MAX(created_at)", "MIN(updated_at)", "MAX(updated_at)", "COUNT(DISTINCT flow_id)", "COUNT(DISTINCT variation_id)"] | 1 | 0.483 |
| [S6/Q4](#s6) | success | ["klaviyo__flows"] | 0 / {} | ["status", "trigger_type", "source_relation"] | ["COUNT(*)"] | 17 | 0.449 |
| [S7/Q5](#s7) | success | ["klaviyo__flows"] | 0 / {} | ["flow_name"] | ["COUNT(*)"] | 24 | 0.462 |
| [S8/Q6](#s8) | success | ["klaviyo__flows"] | 0 / {} | ["flow_name"] | ["COUNT(*)"] | 24 | 0.385 |
| [S9/Q7](#s9) | success | ["klaviyo__flows"] | 0 / {} | [] | [] | 24 | 0.286 |
| [S10/Q8](#s10) | success | ["klaviyo__flows"] | 0 / {} | [] | [] | 79 | 1.035 |
| [S11/Q9](#s11) | success | ["klaviyo__flows"] | 0 / {} | [] | [] | 24 | 0.55 |
| [S12/Q10](#s12) | success | ["klaviyo__flows"] | 0 / {} | ["campaign_type", "category_3", "audience_bucket"] | ["COUNT(*)", "MIN(count_received_email)", "MAX(count_received_email)", "AVG(or_calc)", "AVG(ctor_calc)"] | 8 | 1.127 |
| [S13/Q11](#s13) | success | ["klaviyo__flows"] | 0 / {} | [] | ["MAX(created_at)"] | 1 | 0.359 |
| [S14/Q12](#s14) | success | ["klaviyo__flows"] | 0 / {} | [] | ["COUNT(*)", "SUM(CASE WHEN created_at >= '2023-02-27' THEN 1 ELSE 0 END)"] | 1 | 0.347 |
| [S15/Q13](#s15) | success | ["klaviyo__flows"] | 0 / {} | ["campaign_type", "audience_bucket"] | ["COUNT(*)", "AVG(or_calc)", "AVG(ctor_calc)", "SUM(or_calc * or_calc)", "COUNT(*)", "SUM(ctor_calc * ctor_calc)", "COUNT(*)", "COUNT(*)", "COUNT(*)", "SUM(or_calc)", "SUM(or_calc)", "SUM(ctor_calc)", "SUM(ctor_calc)"] | 8 | 0.816 |
| [S16/Q14](#s16) | success | ["klaviyo__flows"] | 2 / {'LEFT': 1} | ["campaign_type", "audience_bucket"] | ["AVG(or_calc)", "AVG(ctor_calc)", "SUM(or_calc * or_calc)", "COUNT(*)", "SUM(ctor_calc * ctor_calc)", "COUNT(*)", "COUNT(*)", "COUNT(*)", "SUM(or_calc)", "SUM(or_calc)", "SUM(ctor_calc)", "SUM(ctor_calc)"] | 79 | 2.468 |
| [S17/Q15](#s17) | success | ["klaviyo__flows"] | 0 / {} | ["variation_id", "campaign_type"] | ["COUNT(*)", "COUNT(*)", "COUNT(*)"] | 24 | 0.891 |
| [S18/Q16](#s18) | success | ["klaviyo__flows"] | 0 / {} | ["weekday_flag", "daypart"] | ["COUNT(*)", "AVG(or_calc)", "AVG(ctor_calc)"] | 4 | 0.783 |
| [S19/Q17](#s19) | success | ["klaviyo__flows"] | 0 / {} | ["campaign_type", "weekday_flag", "daypart"] | ["COUNT(*)", "AVG(or_calc)", "AVG(ctor_calc)"] | 22 | 0.917 |
| [S20/Q18](#s20) | success | ["klaviyo__flows"] | 0 / {} | ["variation_id", "campaign_type"] | ["COUNT(*)", "AVG(or_calc)", "AVG(ctor_calc)", "COUNT(*)", "COUNT(*)"] | 24 | 1.155 |
| [S21/Q19](#s21) | success | ["klaviyo__person_campaign_flow"] | 0 / {} | [] | ["COUNT(*)", "COUNT(DISTINCT last_touch_flow_id)", "COUNT(DISTINCT last_touch_campaign_id)", "COUNT(DISTINCT variation_id)", "MIN(last_event_at)", "MAX(last_event_at)", "SUM(has_converted)"] | 1 | 0.524 |
| [S22/Q20](#s22) | success | ["klaviyo__person_campaign_flow"] | 0 / {} | ["variation_id"] | ["COUNT(*)", "AVG(count_viewed_product)", "AVG(count_placed_order)", "AVG(net_revenue_touch)", "AVG(email_open_rate_touch)", "AVG(email_click_to_open_rate_touch)", "COUNT(*)", "SUM(has_converted)"] | 4 | 0.469 |
| [S23/Q21](#s23) | success | ["klaviyo__flows"] | 0 / {} | ["variant_letter"] | ["COUNT(*)", "AVG(or_calc)", "AVG(ctor_calc)", "MIN(or_calc)", "MAX(or_calc)", "MIN(ctor_calc)", "MAX(ctor_calc)"] | 3 | 0.729 |
| [S24/Q22](#s24) | success | ["klaviyo__flows"] | 0 / {} | ["campaign_type", "variant_letter"] | ["COUNT(*)", "AVG(or_calc)", "AVG(ctor_calc)"] | 24 | 0.928 |


## 元数据和设置

| SQL | 类别 | 状态 | 内容 |
| --- | --- | --- | --- |
| S1 | connection_setup | success | PRAGMA query_only=ON |
| S2 | metadata | success | SELECT name,sql FROM sqlite_master WHERE type='table' ORDER BY name |


## Python 与执行位置

人工源码审查：**database_first_violation**。SQL 已计算异常标志和基础分组，Python 仍对异常标志求和、筛选异常、按活动类型和时段再聚合、合计模板使用次数；这些 SUM、WHERE、GROUP BY 和排序可在 SQL 完成。绘图及统计相关分析单独视为补充。 [证据](../reviews/dacomp-096.json)。

P1：Read the full flows data from the archive to analyze campaign types, audience size ranges, and date distributions.

[源码](../../../runs/dsv4flash-db-first-full-01/dacomp-096/attempt-01/python/P1.py)；[输出](../../../runs/dsv4flash-db-first-full-01/dacomp-096/attempt-01/python/P1.stdout)；[错误](../../../runs/dsv4flash-db-first-full-01/dacomp-096/attempt-01/python/P1.stderr)。自动源码筛查未检出预设迁出信号；这不是全面语义合规证明。

P2：Read the full 79-row flows data from the archive to map campaign types, template (variation) IDs, audience size range and date spans for the health framework.

[源码](../../../runs/dsv4flash-db-first-full-01/dacomp-096/attempt-01/python/P2.py)；[输出](../../../runs/dsv4flash-db-first-full-01/dacomp-096/attempt-01/python/P2.stdout)；[错误](../../../runs/dsv4flash-db-first-full-01/dacomp-096/attempt-01/python/P2.stderr)。自动源码筛查未检出预设迁出信号；这不是全面语义合规证明。

P3：Check the raw format of the JSONL archive file to understand the data structure.

[源码](../../../runs/dsv4flash-db-first-full-01/dacomp-096/attempt-01/python/P3.py)；[输出](../../../runs/dsv4flash-db-first-full-01/dacomp-096/attempt-01/python/P3.stdout)；[错误](../../../runs/dsv4flash-db-first-full-01/dacomp-096/attempt-01/python/P3.stderr)。自动源码筛查未检出预设迁出信号；这不是全面语义合规证明。

P4：Build a proper DataFrame from the JSON-array archive rows to inspect the campaign dataset structure and distributions.

[源码](../../../runs/dsv4flash-db-first-full-01/dacomp-096/attempt-01/python/P4.py)；[输出](../../../runs/dsv4flash-db-first-full-01/dacomp-096/attempt-01/python/P4.stdout)；[错误](../../../runs/dsv4flash-db-first-full-01/dacomp-096/attempt-01/python/P4.stderr)。自动源码筛查未检出预设迁出信号；这不是全面语义合规证明。

P5：Load the full anomaly detection results from the archive to identify which campaigns are flagged as anomalies.

[源码](../../../runs/dsv4flash-db-first-full-01/dacomp-096/attempt-01/python/P5.py)；[输出](../../../runs/dsv4flash-db-first-full-01/dacomp-096/attempt-01/python/P5.stdout)；[错误](../../../runs/dsv4flash-db-first-full-01/dacomp-096/attempt-01/python/P5.stderr)。自动源码筛查未检出预设迁出信号；这不是全面语义合规证明。

P6：Examine the z-score distributions to see how close campaigns get to the ±2σ anomaly threshold and the hours_since_prev gaps.

[源码](../../../runs/dsv4flash-db-first-full-01/dacomp-096/attempt-01/python/P6.py)；[输出](../../../runs/dsv4flash-db-first-full-01/dacomp-096/attempt-01/python/P6.stdout)；[错误](../../../runs/dsv4flash-db-first-full-01/dacomp-096/attempt-01/python/P6.stderr)。自动源码筛查未检出预设迁出信号；这不是全面语义合规证明。

P7：Comprehensive analysis of template reuse, campaign-type performance, near-anomaly campaigns, and correlation analysis to build the diagnostic report.

[源码](../../../runs/dsv4flash-db-first-full-01/dacomp-096/attempt-01/python/P7.py)；[输出](../../../runs/dsv4flash-db-first-full-01/dacomp-096/attempt-01/python/P7.stdout)；[错误](../../../runs/dsv4flash-db-first-full-01/dacomp-096/attempt-01/python/P7.stderr)。检出需人工核验的 SQL 可实现操作：groupby(, sort_values(；不能仅凭理由判为合规。

P8：Create visualizations for campaign type performance comparison, template reuse vs performance scatter, send time slot heatmap, and near-anomaly scatter plot using Python's matplotlib/seaborn.

[源码](../../../runs/dsv4flash-db-first-full-01/dacomp-096/attempt-01/python/P8.py)；[输出](../../../runs/dsv4flash-db-first-full-01/dacomp-096/attempt-01/python/P8.stdout)；[错误](../../../runs/dsv4flash-db-first-full-01/dacomp-096/attempt-01/python/P8.stderr)。检出需人工核验的 SQL 可实现操作：groupby(；不能仅凭理由判为合规。

P9：Analyze root causes of near-anomaly campaigns and quantify the copy theme (variant) performance gap to inform the diagnostic report.

[源码](../../../runs/dsv4flash-db-first-full-01/dacomp-096/attempt-01/python/P9.py)；[输出](../../../runs/dsv4flash-db-first-full-01/dacomp-096/attempt-01/python/P9.stdout)；[错误](../../../runs/dsv4flash-db-first-full-01/dacomp-096/attempt-01/python/P9.stderr)。检出需人工核验的 SQL 可实现操作：groupby(, sort_values(；不能仅凭理由判为合规。

## 优化机会

已验证候选。筛选限于精确 SQL、相同自包含 CTE、相同单表完整过滤、可分解单表聚合；未覆盖任意 Join 等价和一般谓词蕴含。全部候选都是 offline，未测在线预测。

| 候选 | 类型 | 已有结果 | 覆盖 SQL | 后续次数 | 中间行数 | 验证 | 成本 |
| --- | --- | --- | --- | --- | --- | --- | --- |
| C1 | common subexpression | False | ["S18", "S19"] | 1 | 79 | verified | Not benchmarked; correctness alone does not establish net speedup. |
| C2 | common subexpression | False | ["S23", "S24"] | 1 | 79 | verified | Not benchmarked; correctness alone does not establish net speedup. |
| C3 | aggregate MV | False | ["S6", "S7", "S8", "S13", "S14"] | 4 | 46 | verified | Not benchmarked; correctness alone does not establish net speedup. |


已验证覆盖（含触发查询、候选并集去重）：9/22 条成功数据 SQL。正确性仅针对当前数据库快照；未测性能的候选不能声称已加速。

[完整 build/rewrite 与比较证据](dacomp-096.analysis.json)。

### C3：aggregate MV

Union of grouping keys; decomposable aggregate states; AVG uses SUM and non-NULL COUNT.

原查询 [S6](#s6), [S7](#s7), [S8](#s8), [S13](#s13), [S14](#s14) → 新增共享状态 C3 → 后续 4 次可复用。该构建点为事后假设，不代表 Agent 当时预知后续。

构建定义：

```sql
SELECT status AS __g0, trigger_type AS __g1, source_relation AS __g2, flow_name AS __g3, COUNT(*) AS __a0, MAX(created_at) AS __a1, SUM(CASE WHEN created_at >= '2023-02-27' THEN 1 ELSE 0 END) AS __a2 FROM "klaviyo__flows"  GROUP BY status, trigger_type, source_relation, flow_name
```

受益查询 S6 的改写示例：

```sql
SELECT __g0 AS "status", __g1 AS "trigger_type", __g2 AS "source_relation", SUM(__a0) AS n FROM temp.reuse_candidate GROUP BY __g0, __g1, __g2 ORDER BY n DESC
```

| 原 SQL | 列名一致 | 结果一致 | 比较方法 |
| --- | --- | --- | --- |
| S6 | True | True | ordered_numeric_tolerance |
| S7 | True | True | ordered_numeric_tolerance |
| S8 | True | True | ordered_numeric_tolerance |
| S13 | True | True | exact_multiset |
| S14 | True | True | exact_multiset |


验证状态：verified；成本结论：Not benchmarked; correctness alone does not establish net speedup.

### C1：common subexpression

Identical self-contained CTE body across queries.

原查询 [S18](#s18), [S19](#s19) → 新增共享状态 C1 → 后续 1 次可复用。该构建点为事后假设，不代表 Agent 当时预知后续。

构建定义：

```sql
SELECT *, CASE WHEN flow_name LIKE 'Welcome%' THEN 'Onboarding' WHEN flow_name LIKE 'Cart Recovery%' THEN 'Cart Recovery' WHEN flow_name LIKE 'Browse Abandonment%' THEN 'Browse Abandonment' WHEN flow_name LIKE 'Post-Purchase%' THEN 'Post-Purchase' WHEN flow_name LIKE 'Product Discovery%' THEN 'Product Discovery' WHEN flow_name LIKE 'Seasonal%' THEN 'Seasonal' WHEN flow_name LIKE 'VIP Loyalty%' THEN 'VIP Loyalty' WHEN flow_name LIKE 'Winback%' THEN 'Winback' END AS campaign_type, CASE WHEN CAST(STRFTIME('%w', created_at) AS INTEGER) IN (0, 6) THEN 'Weekend' ELSE 'Weekday' END AS weekday_flag, CASE WHEN CAST(STRFTIME('%H', created_at) AS INTEGER) < 12 THEN 'Morning' ELSE 'Afternoon' END AS daypart, count_opened_email / NULLIF(count_received_email, 0) AS or_calc, count_clicked_email / NULLIF(count_opened_email, 0) AS ctor_calc FROM klaviyo__flows
```

受益查询 S18 的改写示例：

```sql
WITH base AS (SELECT * FROM temp.reuse_candidate) SELECT weekday_flag, daypart, COUNT(*) AS n, ROUND(AVG(or_calc), 4) AS mean_or, ROUND(AVG(ctor_calc), 4) AS mean_ctor FROM base GROUP BY weekday_flag, daypart ORDER BY weekday_flag, daypart
```

| 原 SQL | 列名一致 | 结果一致 | 比较方法 |
| --- | --- | --- | --- |
| S18 | True | True | ordered_numeric_tolerance |
| S19 | True | True | ordered_numeric_tolerance |


验证状态：verified；成本结论：Not benchmarked; correctness alone does not establish net speedup.

### C2：common subexpression

Identical self-contained CTE body across queries.

原查询 [S23](#s23), [S24](#s24) → 新增共享状态 C2 → 后续 1 次可复用。该构建点为事后假设，不代表 Agent 当时预知后续。

构建定义：

```sql
SELECT *, CASE WHEN flow_name LIKE 'Welcome%' THEN 'Onboarding' WHEN flow_name LIKE 'Cart Recovery%' THEN 'Cart Recovery' WHEN flow_name LIKE 'Browse Abandonment%' THEN 'Browse Abandonment' WHEN flow_name LIKE 'Post-Purchase%' THEN 'Post-Purchase' WHEN flow_name LIKE 'Product Discovery%' THEN 'Product Discovery' WHEN flow_name LIKE 'Seasonal%' THEN 'Seasonal' WHEN flow_name LIKE 'VIP Loyalty%' THEN 'VIP Loyalty' WHEN flow_name LIKE 'Winback%' THEN 'Winback' END AS campaign_type, SUBSTRING(flow_name, INSTR(flow_name, 'Variant ') + 8, 1) AS variant_letter, count_opened_email / NULLIF(count_received_email, 0) AS or_calc, count_clicked_email / NULLIF(count_opened_email, 0) AS ctor_calc FROM klaviyo__flows
```

受益查询 S23 的改写示例：

```sql
WITH base AS (SELECT * FROM temp.reuse_candidate) SELECT variant_letter, COUNT(*) AS n, ROUND(AVG(or_calc), 4) AS mean_or, ROUND(AVG(ctor_calc), 4) AS mean_ctor, ROUND(MIN(or_calc), 4) AS min_or, ROUND(MAX(or_calc), 4) AS max_or, ROUND(MIN(ctor_calc), 4) AS min_ctor, ROUND(MAX(ctor_calc), 4) AS max_ctor FROM base GROUP BY variant_letter ORDER BY variant_letter
```

| 原 SQL | 列名一致 | 结果一致 | 比较方法 |
| --- | --- | --- | --- |
| S23 | True | True | ordered_numeric_tolerance |
| S24 | True | True | ordered_numeric_tolerance |


验证状态：verified；成本结论：Not benchmarked; correctness alone does not establish net speedup.

结果依赖：自动记录 SQL→Python 的接口父调用，以及源码中引用归档文件的消费者；字面值相同不认定因果。模型方向选择需要人工读取消息，尚未做全面因果标注。

[原始报告](../../../runs/dsv4flash-db-first-full-01/dacomp-096/attempt-01/answer.md)；[统一消息](../../../runs/dsv4flash-db-first-full-01/dacomp-096/attempt-01/messages.jsonl)；[原始 OpenCode 事件](../../../runs/dsv4flash-db-first-full-01/dacomp-096/attempt-01/opencode.jsonl)；[SQL 引擎日志](../../../runs/dsv4flash-db-first-full-01/dacomp-096/attempt-01/sql_journal.jsonl)。

[可读报告（本地图片链接规范化）](../answers/dacomp-096.md)。原始回答保留，分析结论未改写。

## S1

类别 `connection_setup`；来源 `connection`；调用 `792a314a0fae4bd5867d60cc90be4215`；状态 `success`。

```sql
PRAGMA query_only=ON
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-096/attempt-01/sql/S1.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-096/attempt-01/sql/S1.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-096/attempt-01/results/S1.rows.jsonl)；完整：True；SHA256：`e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`。

## S2

类别 `metadata`；来源 `list_db`；调用 `792a314a0fae4bd5867d60cc90be4215`；状态 `success`。

```sql
SELECT name,sql FROM sqlite_master WHERE type='table' ORDER BY name
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-096/attempt-01/sql/S2.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-096/attempt-01/sql/S2.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-096/attempt-01/results/S2.rows.jsonl)；完整：True；SHA256：`a160fcbf20d09c6a8e74017fa90287215350d1f2975e447ce98b192a65773398`。

## S3

类别 `data`；来源 `query_db`；调用 `bef8ee7cc32745908859083e5c7bf539`；状态 `success`。

```sql
SELECT * FROM klaviyo__flows LIMIT 20
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-096/attempt-01/sql/S3.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-096/attempt-01/sql/S3.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-096/attempt-01/results/S3.rows.jsonl)；完整：True；SHA256：`8d6114b66f273e7da600353f159d9614b506fdaa1f4676a73790ec03793038a1`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "klaviyo__flows", "kind": "base", "block": null, "base_tables": ["klaviyo__flows"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |


## S4

类别 `data`；来源 `query_db`；调用 `9241f11337fe4ebe8a875f9986612fc4`；状态 `success`。

```sql
SELECT * FROM klaviyo__person_campaign_flow LIMIT 20
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-096/attempt-01/sql/S4.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-096/attempt-01/sql/S4.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-096/attempt-01/results/S4.rows.jsonl)；完整：True；SHA256：`68c84282544bd15bf701054a8593cb73c2c900849a74cd60ebf29c8673cd8616`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "klaviyo__person_campaign_flow", "kind": "base", "block": null, "base_tables": ["klaviyo__person_campaign_flow"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |


## S5

类别 `data`；来源 `query_db`；调用 `09dc098722b84ec3985b239462aebc49`；状态 `success`。

```sql
SELECT COUNT(*) AS n_rows,
       MIN(created_at) AS min_created, MAX(created_at) AS max_created,
       MIN(updated_at) AS min_updated, MAX(updated_at) AS max_updated,
       COUNT(DISTINCT flow_id) AS n_flows,
       COUNT(DISTINCT variation_id) AS n_variations
FROM klaviyo__flows
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-096/attempt-01/sql/S5.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-096/attempt-01/sql/S5.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-096/attempt-01/results/S5.rows.jsonl)；完整：True；SHA256：`5671b7c49f56fd5803cff0dfbf62c6dd2e8c94a4241cda56b37f059919e6b6a7`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "klaviyo__flows", "kind": "base", "block": null, "base_tables": ["klaviyo__flows"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |
| B1 | MIN(created_at) | [{"table": "klaviyo__flows", "column": "created_at"}] | [] | False |
| B1 | MAX(created_at) | [{"table": "klaviyo__flows", "column": "created_at"}] | [] | False |
| B1 | MIN(updated_at) | [{"table": "klaviyo__flows", "column": "updated_at"}] | [] | False |
| B1 | MAX(updated_at) | [{"table": "klaviyo__flows", "column": "updated_at"}] | [] | False |
| B1 | COUNT(DISTINCT flow_id) | [{"table": "klaviyo__flows", "column": "flow_id"}] | [] | False |
| B1 | COUNT(DISTINCT variation_id) | [{"table": "klaviyo__flows", "column": "variation_id"}] | [] | False |


## S6

类别 `data`；来源 `query_db`；调用 `84a23e678c2548a8b1d89b6f2f506239`；状态 `success`。

```sql
SELECT status, trigger_type, source_relation, COUNT(*) AS n
FROM klaviyo__flows
GROUP BY status, trigger_type, source_relation
ORDER BY n DESC
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-096/attempt-01/sql/S6.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-096/attempt-01/sql/S6.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-096/attempt-01/results/S6.rows.jsonl)；完整：True；SHA256：`1ec53df2576e47accc42b4c18c78906a601f5d7fb17b437d85848f975ffe46a1`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "klaviyo__flows", "kind": "base", "block": null, "base_tables": ["klaviyo__flows"]}] | [] | ["status", "trigger_type", "source_relation"] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |


## S7

类别 `data`；来源 `query_db`；调用 `885dd26de8e74fb889be78ba25c802f3`；状态 `success`。

```sql
SELECT flow_name, COUNT(*) AS n
FROM klaviyo__flows
GROUP BY flow_name
ORDER BY n DESC
LIMIT 50
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-096/attempt-01/sql/S7.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-096/attempt-01/sql/S7.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-096/attempt-01/results/S7.rows.jsonl)；完整：True；SHA256：`68d3f0069ed04eef1deb54eab65418d5c059e95b4bb7fbda6ff065ef1a2059a4`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "klaviyo__flows", "kind": "base", "block": null, "base_tables": ["klaviyo__flows"]}] | [] | ["flow_name"] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |


## S8

类别 `data`；来源 `query_db`；调用 `54d437b927544d1fa3a9c0745a907216`；状态 `success`。

```sql
SELECT flow_name, COUNT(*) AS n
FROM klaviyo__flows
GROUP BY flow_name
ORDER BY n DESC
LIMIT 100
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-096/attempt-01/sql/S8.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-096/attempt-01/sql/S8.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-096/attempt-01/results/S8.rows.jsonl)；完整：True；SHA256：`68d3f0069ed04eef1deb54eab65418d5c059e95b4bb7fbda6ff065ef1a2059a4`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "klaviyo__flows", "kind": "base", "block": null, "base_tables": ["klaviyo__flows"]}] | [] | ["flow_name"] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |


## S9

类别 `data`；来源 `query_db`；调用 `4193b0d013d34d0abfccc44eb37e0d65`；状态 `success`。

```sql
SELECT DISTINCT variation_id FROM klaviyo__flows
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-096/attempt-01/sql/S9.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-096/attempt-01/sql/S9.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-096/attempt-01/results/S9.rows.jsonl)；完整：True；SHA256：`9c429674d0e72f9e3346b93264cc98b0c6e5b235a831877a26d55b429d4384ce`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "klaviyo__flows", "kind": "base", "block": null, "base_tables": ["klaviyo__flows"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |


## S10

类别 `data`；来源 `query_db`；调用 `1bde33c2bc924a00bc5a843af437c7bb`；状态 `success`。

```sql
SELECT * FROM klaviyo__flows LIMIT 79
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-096/attempt-01/sql/S10.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-096/attempt-01/sql/S10.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-096/attempt-01/results/S10.rows.jsonl)；完整：True；SHA256：`d27c93ae7fdec11b99bdbdce2e23373f72cbc01cefd646e5d880ac38f0d8aba5`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "klaviyo__flows", "kind": "base", "block": null, "base_tables": ["klaviyo__flows"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |


## S11

类别 `data`；来源 `query_db`；调用 `2a29899936bd4cf58753345160a9607e`；状态 `success`。

```sql
SELECT DISTINCT flow_name,
  CASE 
    WHEN flow_name LIKE 'Welcome%' THEN 'Onboarding'
    WHEN flow_name LIKE 'Cart Recovery%' THEN 'Cart Recovery'
    WHEN flow_name LIKE 'Browse Abandonment%' THEN 'Browse Abandonment'
    WHEN flow_name LIKE 'Post-Purchase%' THEN 'Post-Purchase'
    WHEN flow_name LIKE 'Product Discovery%' THEN 'Product Discovery'
    WHEN flow_name LIKE 'Seasonal%' THEN 'Seasonal'
    WHEN flow_name LIKE 'VIP Loyalty%' THEN 'VIP Loyalty'
    WHEN flow_name LIKE 'Winback%' THEN 'Winback'
  END AS campaign_type
FROM klaviyo__flows
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-096/attempt-01/sql/S11.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-096/attempt-01/sql/S11.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-096/attempt-01/results/S11.rows.jsonl)；完整：True；SHA256：`90533bf4b5faa7034cfb5e485a468f5a352609536fc0d33a24bc9e247acf9161`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "klaviyo__flows", "kind": "base", "block": null, "base_tables": ["klaviyo__flows"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |


## S12

类别 `data`；来源 `query_db`；调用 `f5d20852cb934093967d5813e086d3fd`；状态 `success`。

```sql
WITH base AS (
  SELECT *,
    CASE 
      WHEN flow_name LIKE 'Welcome%' THEN 'Onboarding'
      WHEN flow_name LIKE 'Cart Recovery%' THEN 'Cart Recovery'
      WHEN flow_name LIKE 'Browse Abandonment%' THEN 'Browse Abandonment'
      WHEN flow_name LIKE 'Post-Purchase%' THEN 'Post-Purchase'
      WHEN flow_name LIKE 'Product Discovery%' THEN 'Product Discovery'
      WHEN flow_name LIKE 'Seasonal%' THEN 'Seasonal'
      WHEN flow_name LIKE 'VIP Loyalty%' THEN 'VIP Loyalty'
      WHEN flow_name LIKE 'Winback%' THEN 'Winback'
    END AS campaign_type,
    CASE
      WHEN flow_name IN ('Cart Recovery Series - Variant A','Cart Recovery Series - Variant B','Cart Recovery Series - Variant C',
                         'Seasonal Warmup Flow - Variant A','Seasonal Warmup Flow - Variant B','Seasonal Warmup Flow - Variant C',
                         'Winback Journey - Variant A','Winback Journey - Variant B','Winback Journey - Variant C',
                         'Browse Abandonment - Variant A','Browse Abandonment - Variant B','Browse Abandonment - Variant C') THEN 'Promotional'
      WHEN flow_name LIKE 'Product Discovery%' OR flow_name LIKE 'Welcome%' THEN 'New Product'
      WHEN flow_name LIKE 'Post-Purchase%' OR flow_name LIKE 'VIP Loyalty%' THEN 'Storytelling'
      ELSE 'Other'
    END AS category_3,
    CASE WHEN count_received_email < 10000 THEN '<10k'
         WHEN count_received_email <= 100000 THEN '10k-100k'
         ELSE '>100k' END AS audience_bucket,
    CAST(strftime('%Y-%m-%d', created_at) AS TEXT) AS sent_date,
    strftime('%H', created_at) AS hour_sent,
    CAST(julianday(created_at) - julianday('2023-01-01') AS INT) % 7 AS day_of_week,
    count_opened_email / NULLIF(count_received_email,0) AS or_calc,
    count_clicked_email / NULLIF(count_opened_email,0) AS ctor_calc
  FROM klaviyo__flows
)
SELECT campaign_type, category_3, audience_bucket, COUNT(*) AS n,
  MIN(count_received_email) AS min_aud, MAX(count_received_email) AS max_aud,
  ROUND(AVG(or_calc),4) AS mean_or, ROUND(AVG(ctor_calc),4) AS mean_ctor
FROM base
GROUP BY campaign_type, category_3, audience_bucket
ORDER BY category_3, campaign_type
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-096/attempt-01/sql/S12.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-096/attempt-01/sql/S12.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-096/attempt-01/results/S12.rows.jsonl)；完整：True；SHA256：`eec5478cbb81d990309e06ecd36fd507dc3b35a6311af51b3857b2f220577cf6`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "klaviyo__flows", "kind": "base", "block": null, "base_tables": ["klaviyo__flows"]}] | [] | [] |
| B2 | [{"alias": "base", "kind": "derived", "block": "B1", "base_tables": ["klaviyo__flows"]}] | [] | ["campaign_type", "category_3", "audience_bucket"] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B2 | COUNT(*) | [] | [] | True |
| B2 | MIN(count_received_email) | [{"table": "klaviyo__flows", "column": "count_received_email"}] | [] | False |
| B2 | MAX(count_received_email) | [{"table": "klaviyo__flows", "column": "count_received_email"}] | [] | False |
| B2 | AVG(or_calc) | [{"table": "klaviyo__flows", "column": "count_opened_email"}, {"table": "klaviyo__flows", "column": "count_received_email"}] | [] | False |
| B2 | AVG(ctor_calc) | [{"table": "klaviyo__flows", "column": "count_clicked_email"}, {"table": "klaviyo__flows", "column": "count_opened_email"}] | [] | False |


## S13

类别 `data`；来源 `query_db`；调用 `cd8c6b9a42b4476d9b24896807c0acb8`；状态 `success`。

```sql
SELECT MAX(created_at) AS max_sent FROM klaviyo__flows
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-096/attempt-01/sql/S13.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-096/attempt-01/sql/S13.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-096/attempt-01/results/S13.rows.jsonl)；完整：True；SHA256：`213ab6246ebed918a543ff9bfb154a27398762d88f5b44701d4ee6c874c77c3d`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "klaviyo__flows", "kind": "base", "block": null, "base_tables": ["klaviyo__flows"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | MAX(created_at) | [{"table": "klaviyo__flows", "column": "created_at"}] | [] | False |


## S14

类别 `data`；来源 `query_db`；调用 `3487d7469ec1411cb90277a56083eed8`；状态 `success`。

```sql
SELECT COUNT(*) AS n_total,
  SUM(CASE WHEN created_at >= '2023-02-27' THEN 1 ELSE 0 END) AS n_last6mo
FROM klaviyo__flows
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-096/attempt-01/sql/S14.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-096/attempt-01/sql/S14.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-096/attempt-01/results/S14.rows.jsonl)；完整：True；SHA256：`3c34989e4ae57506f3e2009d9bacd0e20ebc9727547fbd9f649368af2b85cea0`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "klaviyo__flows", "kind": "base", "block": null, "base_tables": ["klaviyo__flows"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |
| B1 | SUM(CASE WHEN created_at >= '2023-02-27' THEN 1 ELSE 0 END) | [] | [{"table": "klaviyo__flows", "column": "created_at"}] | False |


## S15

类别 `data`；来源 `query_db`；调用 `0345500c56b64b21bac59dd5cc985d9d`；状态 `success`。

```sql
WITH base AS (
  SELECT *, 
    CASE 
      WHEN flow_name LIKE 'Welcome%' THEN 'Onboarding'
      WHEN flow_name LIKE 'Cart Recovery%' THEN 'Cart Recovery'
      WHEN flow_name LIKE 'Browse Abandonment%' THEN 'Browse Abandonment'
      WHEN flow_name LIKE 'Post-Purchase%' THEN 'Post-Purchase'
      WHEN flow_name LIKE 'Product Discovery%' THEN 'Product Discovery'
      WHEN flow_name LIKE 'Seasonal%' THEN 'Seasonal'
      WHEN flow_name LIKE 'VIP Loyalty%' THEN 'VIP Loyalty'
      WHEN flow_name LIKE 'Winback%' THEN 'Winback'
    END AS campaign_type,
    CASE WHEN count_received_email < 10000 THEN '<10k'
         WHEN count_received_email <= 100000 THEN '10k-100k'
         ELSE '>100k' END AS audience_bucket,
    count_opened_email / NULLIF(count_received_email,0) AS or_calc,
    count_clicked_email / NULLIF(count_opened_email,0) AS ctor_calc
  FROM klaviyo__flows
  WHERE created_at >= '2023-02-27'
),
stats AS (
  SELECT campaign_type, audience_bucket, COUNT(*) AS n_hist,
    AVG(or_calc) AS mu_or,
    AVG(ctor_calc) AS mu_ctor,
    SQRT( (SUM(or_calc*or_calc) - SUM(or_calc)*SUM(or_calc)/COUNT(*)) / MAX(1,COUNT(*)-1) ) AS sd_or,
    SQRT( (SUM(ctor_calc*ctor_calc) - SUM(ctor_calc)*SUM(ctor_calc)/COUNT(*)) / MAX(1,COUNT(*)-1) ) AS sd_ctor
  FROM base
  GROUP BY campaign_type, audience_bucket
)
SELECT * FROM stats ORDER BY campaign_type
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-096/attempt-01/sql/S15.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-096/attempt-01/sql/S15.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-096/attempt-01/results/S15.rows.jsonl)；完整：True；SHA256：`b1f6bb376e5c99089b22b3d8f42804d79617563609d663cd63db4f74694c87b2`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "klaviyo__flows", "kind": "base", "block": null, "base_tables": ["klaviyo__flows"]}] | [] | [] |
| B2 | [{"alias": "base", "kind": "derived", "block": "B1", "base_tables": ["klaviyo__flows"]}] | [] | ["campaign_type", "audience_bucket"] |
| B3 | [{"alias": "stats", "kind": "derived", "block": "B2", "base_tables": ["klaviyo__flows"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B2 | COUNT(*) | [] | [] | True |
| B2 | AVG(or_calc) | [{"table": "klaviyo__flows", "column": "count_opened_email"}, {"table": "klaviyo__flows", "column": "count_received_email"}] | [] | False |
| B2 | AVG(ctor_calc) | [{"table": "klaviyo__flows", "column": "count_clicked_email"}, {"table": "klaviyo__flows", "column": "count_opened_email"}] | [] | False |
| B2 | SUM(or_calc * or_calc) | [{"table": "klaviyo__flows", "column": "count_opened_email"}, {"table": "klaviyo__flows", "column": "count_received_email"}, {"table": "klaviyo__flows", "column": "count_opened_email"}, {"table": "klaviyo__flows", "column": "count_received_email"}] | [] | False |
| B2 | COUNT(*) | [] | [] | True |
| B2 | SUM(ctor_calc * ctor_calc) | [{"table": "klaviyo__flows", "column": "count_clicked_email"}, {"table": "klaviyo__flows", "column": "count_opened_email"}, {"table": "klaviyo__flows", "column": "count_clicked_email"}, {"table": "klaviyo__flows", "column": "count_opened_email"}] | [] | False |
| B2 | COUNT(*) | [] | [] | True |
| B2 | COUNT(*) | [] | [] | True |
| B2 | COUNT(*) | [] | [] | True |
| B2 | SUM(or_calc) | [{"table": "klaviyo__flows", "column": "count_opened_email"}, {"table": "klaviyo__flows", "column": "count_received_email"}] | [] | False |
| B2 | SUM(or_calc) | [{"table": "klaviyo__flows", "column": "count_opened_email"}, {"table": "klaviyo__flows", "column": "count_received_email"}] | [] | False |
| B2 | SUM(ctor_calc) | [{"table": "klaviyo__flows", "column": "count_clicked_email"}, {"table": "klaviyo__flows", "column": "count_opened_email"}] | [] | False |
| B2 | SUM(ctor_calc) | [{"table": "klaviyo__flows", "column": "count_clicked_email"}, {"table": "klaviyo__flows", "column": "count_opened_email"}] | [] | False |


## S16

类别 `data`；来源 `query_db`；调用 `f9939942a07b4018b81f98201c59bd2d`；状态 `success`。

```sql
WITH base_all AS (
  SELECT *, 
    CASE 
      WHEN flow_name LIKE 'Welcome%' THEN 'Onboarding'
      WHEN flow_name LIKE 'Cart Recovery%' THEN 'Cart Recovery'
      WHEN flow_name LIKE 'Browse Abandonment%' THEN 'Browse Abandonment'
      WHEN flow_name LIKE 'Post-Purchase%' THEN 'Post-Purchase'
      WHEN flow_name LIKE 'Product Discovery%' THEN 'Product Discovery'
      WHEN flow_name LIKE 'Seasonal%' THEN 'Seasonal'
      WHEN flow_name LIKE 'VIP Loyalty%' THEN 'VIP Loyalty'
      WHEN flow_name LIKE 'Winback%' THEN 'Winback'
    END AS campaign_type,
    CASE WHEN count_received_email < 10000 THEN '<10k'
         WHEN count_received_email <= 100000 THEN '10k-100k'
         ELSE '>100k' END AS audience_bucket,
    count_opened_email / NULLIF(count_received_email,0) AS or_calc,
    count_clicked_email / NULLIF(count_opened_email,0) AS ctor_calc
  FROM klaviyo__flows
),
stats AS (
  SELECT campaign_type, audience_bucket,
    AVG(or_calc) AS mu_or,
    AVG(ctor_calc) AS mu_ctor,
    SQRT( (SUM(or_calc*or_calc) - SUM(or_calc)*SUM(or_calc)/COUNT(*)) / MAX(1,COUNT(*)-1) ) AS sd_or,
    SQRT( (SUM(ctor_calc*ctor_calc) - SUM(ctor_calc)*SUM(ctor_calc)/COUNT(*)) / MAX(1,COUNT(*)-1) ) AS sd_ctor
  FROM base_all
  WHERE created_at >= '2023-02-27'
  GROUP BY campaign_type, audience_bucket
),
prev_updated AS (
  SELECT flow_id, flow_name, campaign_type, audience_bucket, created_at, updated_at,
    status, variation_id, source_relation, or_calc, ctor_calc,
    LAG(updated_at) OVER (ORDER BY updated_at) AS prev_updated_at
  FROM base_all
),
anomalies AS (
  SELECT p.*, s.mu_or, s.mu_ctor, s.sd_or, s.sd_ctor,
    CASE WHEN p.or_calc < s.mu_or - 2*s.sd_or OR p.or_calc > s.mu_or + 2*s.sd_or THEN 1 ELSE 0 END AS or_anomaly,
    CASE WHEN p.ctor_calc < s.mu_ctor - 2*s.sd_ctor OR p.ctor_calc > s.mu_ctor + 2*s.sd_ctor THEN 1 ELSE 0 END AS ctor_anomaly,
    CASE WHEN prev_updated_at IS NOT NULL AND (julianday(p.updated_at) - julianday(p.prev_updated_at))*24 < 24 THEN 1 ELSE 0 END AS freq_anomaly
  FROM prev_updated p
  LEFT JOIN stats s ON p.campaign_type = s.campaign_type AND p.audience_bucket = s.audience_bucket
)
SELECT flow_id, flow_name, campaign_type, audience_bucket, 
  created_at, updated_at, prev_updated_at,
  ROUND(CAST((julianday(updated_at) - julianday(prev_updated_at))*24 AS REAL),2) AS hours_since_prev,
  or_calc, mu_or, sd_or, or_anomaly,
  ctor_calc, mu_ctor, sd_ctor, ctor_anomaly,
  freq_anomaly,
  CASE WHEN or_anomaly=1 OR ctor_anomaly=1 OR freq_anomaly=1 THEN 1 ELSE 0 END AS any_anomaly
FROM anomalies
ORDER BY any_anomaly DESC, freq_anomaly DESC, or_anomaly DESC, ctor_anomaly DESC
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-096/attempt-01/sql/S16.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-096/attempt-01/sql/S16.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-096/attempt-01/results/S16.rows.jsonl)；完整：True；SHA256：`abe860a9b02a2132112769e3083148e39b0abd3ff5cfa02ce430e5cc35206d41`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "klaviyo__flows", "kind": "base", "block": null, "base_tables": ["klaviyo__flows"]}] | [] | [] |
| B2 | [{"alias": "base_all", "kind": "derived", "block": "B1", "base_tables": ["klaviyo__flows"]}] | [] | ["campaign_type", "audience_bucket"] |
| B3 | [{"alias": "base_all", "kind": "derived", "block": "B1", "base_tables": ["klaviyo__flows"]}] | [] | [] |
| B4 | [{"alias": "p", "kind": "derived", "block": "B3", "base_tables": ["klaviyo__flows"]}, {"alias": "s", "kind": "derived", "block": "B2", "base_tables": ["klaviyo__flows"]}] | [{"type": "LEFT", "right": "stats AS s", "on": "p.campaign_type = s.campaign_type AND p.audience_bucket = s.audience_bucket", "using": []}] | [] |
| B5 | [{"alias": "anomalies", "kind": "derived", "block": "B4", "base_tables": ["klaviyo__flows"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B2 | AVG(or_calc) | [{"table": "klaviyo__flows", "column": "count_opened_email"}, {"table": "klaviyo__flows", "column": "count_received_email"}] | [] | False |
| B2 | AVG(ctor_calc) | [{"table": "klaviyo__flows", "column": "count_clicked_email"}, {"table": "klaviyo__flows", "column": "count_opened_email"}] | [] | False |
| B2 | SUM(or_calc * or_calc) | [{"table": "klaviyo__flows", "column": "count_opened_email"}, {"table": "klaviyo__flows", "column": "count_received_email"}, {"table": "klaviyo__flows", "column": "count_opened_email"}, {"table": "klaviyo__flows", "column": "count_received_email"}] | [] | False |
| B2 | COUNT(*) | [] | [] | True |
| B2 | SUM(ctor_calc * ctor_calc) | [{"table": "klaviyo__flows", "column": "count_clicked_email"}, {"table": "klaviyo__flows", "column": "count_opened_email"}, {"table": "klaviyo__flows", "column": "count_clicked_email"}, {"table": "klaviyo__flows", "column": "count_opened_email"}] | [] | False |
| B2 | COUNT(*) | [] | [] | True |
| B2 | COUNT(*) | [] | [] | True |
| B2 | COUNT(*) | [] | [] | True |
| B2 | SUM(or_calc) | [{"table": "klaviyo__flows", "column": "count_opened_email"}, {"table": "klaviyo__flows", "column": "count_received_email"}] | [] | False |
| B2 | SUM(or_calc) | [{"table": "klaviyo__flows", "column": "count_opened_email"}, {"table": "klaviyo__flows", "column": "count_received_email"}] | [] | False |
| B2 | SUM(ctor_calc) | [{"table": "klaviyo__flows", "column": "count_clicked_email"}, {"table": "klaviyo__flows", "column": "count_opened_email"}] | [] | False |
| B2 | SUM(ctor_calc) | [{"table": "klaviyo__flows", "column": "count_clicked_email"}, {"table": "klaviyo__flows", "column": "count_opened_email"}] | [] | False |


未解析列血缘：[{"block": "B4", "column": "campaign_type", "reason": "ambiguous_or_missing_source"}, {"block": "B4", "column": "audience_bucket", "reason": "ambiguous_or_missing_source"}]

## S17

类别 `data`；来源 `query_db`；调用 `b06c4a87807e4b1d988e982fb6e0cc3d`；状态 `success`。

```sql
WITH base AS (
  SELECT *,
    CASE 
      WHEN flow_name LIKE 'Welcome%' THEN 'Onboarding'
      WHEN flow_name LIKE 'Cart Recovery%' THEN 'Cart Recovery'
      WHEN flow_name LIKE 'Browse Abandonment%' THEN 'Browse Abandonment'
      WHEN flow_name LIKE 'Post-Purchase%' THEN 'Post-Purchase'
      WHEN flow_name LIKE 'Product Discovery%' THEN 'Product Discovery'
      WHEN flow_name LIKE 'Seasonal%' THEN 'Seasonal'
      WHEN flow_name LIKE 'VIP Loyalty%' THEN 'VIP Loyalty'
      WHEN flow_name LIKE 'Winback%' THEN 'Winback'
    END AS campaign_type
  FROM klaviyo__flows
),
template_stats AS (
  SELECT variation_id, campaign_type, COUNT(*) AS n_uses,
    ROUND(100.0 * COUNT(*) / SUM(COUNT(*)) OVER (PARTITION BY campaign_type), 1) AS pct_of_type
  FROM base
  GROUP BY variation_id, campaign_type
)
SELECT * FROM template_stats ORDER BY campaign_type, n_uses DESC
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-096/attempt-01/sql/S17.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-096/attempt-01/sql/S17.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-096/attempt-01/results/S17.rows.jsonl)；完整：True；SHA256：`55a050dbe03e5f76d741bf4b722a50770b9db4b4c85259e381ced7eb10fdcfbd`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "klaviyo__flows", "kind": "base", "block": null, "base_tables": ["klaviyo__flows"]}] | [] | [] |
| B2 | [{"alias": "base", "kind": "derived", "block": "B1", "base_tables": ["klaviyo__flows"]}] | [] | ["variation_id", "campaign_type"] |
| B3 | [{"alias": "template_stats", "kind": "derived", "block": "B2", "base_tables": ["klaviyo__flows"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B2 | COUNT(*) | [] | [] | True |
| B2 | COUNT(*) | [] | [] | True |
| B2 | COUNT(*) | [] | [] | True |


## S18

类别 `data`；来源 `query_db`；调用 `0bcc07c0581046f2b304fa34023e6be1`；状态 `success`。

```sql
WITH base AS (
  SELECT *,
    CASE 
      WHEN flow_name LIKE 'Welcome%' THEN 'Onboarding'
      WHEN flow_name LIKE 'Cart Recovery%' THEN 'Cart Recovery'
      WHEN flow_name LIKE 'Browse Abandonment%' THEN 'Browse Abandonment'
      WHEN flow_name LIKE 'Post-Purchase%' THEN 'Post-Purchase'
      WHEN flow_name LIKE 'Product Discovery%' THEN 'Product Discovery'
      WHEN flow_name LIKE 'Seasonal%' THEN 'Seasonal'
      WHEN flow_name LIKE 'VIP Loyalty%' THEN 'VIP Loyalty'
      WHEN flow_name LIKE 'Winback%' THEN 'Winback'
    END AS campaign_type,
    CASE WHEN CAST(strftime('%w', created_at) AS INT) IN (0,6) THEN 'Weekend' ELSE 'Weekday' END AS weekday_flag,
    CASE WHEN CAST(strftime('%H', created_at) AS INT) < 12 THEN 'Morning' ELSE 'Afternoon' END AS daypart,
    count_opened_email / NULLIF(count_received_email,0) AS or_calc,
    count_clicked_email / NULLIF(count_opened_email,0) AS ctor_calc
  FROM klaviyo__flows
)
SELECT weekday_flag, daypart, COUNT(*) AS n,
  ROUND(AVG(or_calc),4) AS mean_or,
  ROUND(AVG(ctor_calc),4) AS mean_ctor
FROM base
GROUP BY weekday_flag, daypart
ORDER BY weekday_flag, daypart
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-096/attempt-01/sql/S18.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-096/attempt-01/sql/S18.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-096/attempt-01/results/S18.rows.jsonl)；完整：True；SHA256：`da4abad942e331733a8c7cb63288c12b0da28373333fccbe0720ca1e4b833185`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "klaviyo__flows", "kind": "base", "block": null, "base_tables": ["klaviyo__flows"]}] | [] | [] |
| B2 | [{"alias": "base", "kind": "derived", "block": "B1", "base_tables": ["klaviyo__flows"]}] | [] | ["weekday_flag", "daypart"] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B2 | COUNT(*) | [] | [] | True |
| B2 | AVG(or_calc) | [{"table": "klaviyo__flows", "column": "count_opened_email"}, {"table": "klaviyo__flows", "column": "count_received_email"}] | [] | False |
| B2 | AVG(ctor_calc) | [{"table": "klaviyo__flows", "column": "count_clicked_email"}, {"table": "klaviyo__flows", "column": "count_opened_email"}] | [] | False |


## S19

类别 `data`；来源 `query_db`；调用 `265ffb75b6e7446dbfb79580a89bda85`；状态 `success`。

```sql
WITH base AS (
  SELECT *,
    CASE 
      WHEN flow_name LIKE 'Welcome%' THEN 'Onboarding'
      WHEN flow_name LIKE 'Cart Recovery%' THEN 'Cart Recovery'
      WHEN flow_name LIKE 'Browse Abandonment%' THEN 'Browse Abandonment'
      WHEN flow_name LIKE 'Post-Purchase%' THEN 'Post-Purchase'
      WHEN flow_name LIKE 'Product Discovery%' THEN 'Product Discovery'
      WHEN flow_name LIKE 'Seasonal%' THEN 'Seasonal'
      WHEN flow_name LIKE 'VIP Loyalty%' THEN 'VIP Loyalty'
      WHEN flow_name LIKE 'Winback%' THEN 'Winback'
    END AS campaign_type,
    CASE WHEN CAST(strftime('%w', created_at) AS INT) IN (0,6) THEN 'Weekend' ELSE 'Weekday' END AS weekday_flag,
    CASE WHEN CAST(strftime('%H', created_at) AS INT) < 12 THEN 'Morning' ELSE 'Afternoon' END AS daypart,
    count_opened_email / NULLIF(count_received_email,0) AS or_calc,
    count_clicked_email / NULLIF(count_opened_email,0) AS ctor_calc
  FROM klaviyo__flows
)
SELECT campaign_type, weekday_flag, daypart, COUNT(*) AS n,
  ROUND(AVG(or_calc),4) AS mean_or,
  ROUND(AVG(ctor_calc),4) AS mean_ctor
FROM base
GROUP BY campaign_type, weekday_flag, daypart
ORDER BY campaign_type, weekday_flag, daypart
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-096/attempt-01/sql/S19.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-096/attempt-01/sql/S19.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-096/attempt-01/results/S19.rows.jsonl)；完整：True；SHA256：`964b470010c0c481d0c0e812aaff0347ceb6bcd976d0a39316f62d7600c80cb9`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "klaviyo__flows", "kind": "base", "block": null, "base_tables": ["klaviyo__flows"]}] | [] | [] |
| B2 | [{"alias": "base", "kind": "derived", "block": "B1", "base_tables": ["klaviyo__flows"]}] | [] | ["campaign_type", "weekday_flag", "daypart"] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B2 | COUNT(*) | [] | [] | True |
| B2 | AVG(or_calc) | [{"table": "klaviyo__flows", "column": "count_opened_email"}, {"table": "klaviyo__flows", "column": "count_received_email"}] | [] | False |
| B2 | AVG(ctor_calc) | [{"table": "klaviyo__flows", "column": "count_clicked_email"}, {"table": "klaviyo__flows", "column": "count_opened_email"}] | [] | False |


## S20

类别 `data`；来源 `query_db`；调用 `16801ce3ff7240b2ad4bd81d560e5106`；状态 `success`。

```sql
WITH base AS (
  SELECT *,
    CASE 
      WHEN flow_name LIKE 'Welcome%' THEN 'Onboarding'
      WHEN flow_name LIKE 'Cart Recovery%' THEN 'Cart Recovery'
      WHEN flow_name LIKE 'Browse Abandonment%' THEN 'Browse Abandonment'
      WHEN flow_name LIKE 'Post-Purchase%' THEN 'Post-Purchase'
      WHEN flow_name LIKE 'Product Discovery%' THEN 'Product Discovery'
      WHEN flow_name LIKE 'Seasonal%' THEN 'Seasonal'
      WHEN flow_name LIKE 'VIP Loyalty%' THEN 'VIP Loyalty'
      WHEN flow_name LIKE 'Winback%' THEN 'Winback'
    END AS campaign_type,
    count_opened_email / NULLIF(count_received_email,0) AS or_calc,
    count_clicked_email / NULLIF(count_opened_email,0) AS ctor_calc
  FROM klaviyo__flows
)
SELECT variation_id, campaign_type, COUNT(*) AS n_uses,
  ROUND(100.0 * COUNT(*) / SUM(COUNT(*)) OVER (PARTITION BY campaign_type), 1) AS pct_of_type,
  ROUND(AVG(or_calc),4) AS avg_or,
  ROUND(AVG(ctor_calc),4) AS avg_ctor
FROM base
GROUP BY variation_id, campaign_type
ORDER BY pct_of_type DESC, avg_ctor DESC
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-096/attempt-01/sql/S20.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-096/attempt-01/sql/S20.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-096/attempt-01/results/S20.rows.jsonl)；完整：True；SHA256：`ca2c3610c8204f1d057f81418f6b713976bd4e0ff70870213be91418f723a43a`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "klaviyo__flows", "kind": "base", "block": null, "base_tables": ["klaviyo__flows"]}] | [] | [] |
| B2 | [{"alias": "base", "kind": "derived", "block": "B1", "base_tables": ["klaviyo__flows"]}] | [] | ["variation_id", "campaign_type"] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B2 | COUNT(*) | [] | [] | True |
| B2 | AVG(or_calc) | [{"table": "klaviyo__flows", "column": "count_opened_email"}, {"table": "klaviyo__flows", "column": "count_received_email"}] | [] | False |
| B2 | AVG(ctor_calc) | [{"table": "klaviyo__flows", "column": "count_clicked_email"}, {"table": "klaviyo__flows", "column": "count_opened_email"}] | [] | False |
| B2 | COUNT(*) | [] | [] | True |
| B2 | COUNT(*) | [] | [] | True |


## S21

类别 `data`；来源 `query_db`；调用 `ebb7f0252bc54c6eb4dfcce128f26335`；状态 `success`。

```sql
SELECT COUNT(*) AS n_persons,
       COUNT(DISTINCT last_touch_flow_id) AS n_flows_touched,
       COUNT(DISTINCT last_touch_campaign_id) AS n_camps_touched,
       COUNT(DISTINCT variation_id) AS n_variations,
       MIN(last_event_at) AS min_last_event, MAX(last_event_at) AS max_last_event,
       SUM(has_converted) AS n_converted
FROM klaviyo__person_campaign_flow
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-096/attempt-01/sql/S21.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-096/attempt-01/sql/S21.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-096/attempt-01/results/S21.rows.jsonl)；完整：True；SHA256：`dbb42baee0b5f5ae9bb87fa0cb3b419d9b2d1d68392aeb7be68696f244f9b679`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "klaviyo__person_campaign_flow", "kind": "base", "block": null, "base_tables": ["klaviyo__person_campaign_flow"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |
| B1 | COUNT(DISTINCT last_touch_flow_id) | [{"table": "klaviyo__person_campaign_flow", "column": "last_touch_flow_id"}] | [] | False |
| B1 | COUNT(DISTINCT last_touch_campaign_id) | [{"table": "klaviyo__person_campaign_flow", "column": "last_touch_campaign_id"}] | [] | False |
| B1 | COUNT(DISTINCT variation_id) | [{"table": "klaviyo__person_campaign_flow", "column": "variation_id"}] | [] | False |
| B1 | MIN(last_event_at) | [{"table": "klaviyo__person_campaign_flow", "column": "last_event_at"}] | [] | False |
| B1 | MAX(last_event_at) | [{"table": "klaviyo__person_campaign_flow", "column": "last_event_at"}] | [] | False |
| B1 | SUM(has_converted) | [{"table": "klaviyo__person_campaign_flow", "column": "has_converted"}] | [] | False |


## S22

类别 `data`；来源 `query_db`；调用 `ebda09cad90145be92e2596eb28847e6`；状态 `success`。

```sql
SELECT variation_id, COUNT(*) AS n_persons,
       ROUND(AVG(count_viewed_product),2) AS avg_views,
       ROUND(AVG(count_placed_order),2) AS avg_orders,
       ROUND(AVG(net_revenue_touch),2) AS avg_net_rev,
       ROUND(AVG(email_open_rate_touch),4) AS avg_open_touch,
       ROUND(AVG(email_click_to_open_rate_touch),4) AS avg_ctor_touch,
       ROUND(SUM(has_converted)*100.0/COUNT(*),2) AS conv_pct
FROM klaviyo__person_campaign_flow
GROUP BY variation_id
ORDER BY variation_id
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-096/attempt-01/sql/S22.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-096/attempt-01/sql/S22.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-096/attempt-01/results/S22.rows.jsonl)；完整：True；SHA256：`2c9bef12867cb039e9a282b8b4d030c8a13438f7479204e1edd259db9a74b21a`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "klaviyo__person_campaign_flow", "kind": "base", "block": null, "base_tables": ["klaviyo__person_campaign_flow"]}] | [] | ["variation_id"] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |
| B1 | AVG(count_viewed_product) | [{"table": "klaviyo__person_campaign_flow", "column": "count_viewed_product"}] | [] | False |
| B1 | AVG(count_placed_order) | [{"table": "klaviyo__person_campaign_flow", "column": "count_placed_order"}] | [] | False |
| B1 | AVG(net_revenue_touch) | [{"table": "klaviyo__person_campaign_flow", "column": "net_revenue_touch"}] | [] | False |
| B1 | AVG(email_open_rate_touch) | [{"table": "klaviyo__person_campaign_flow", "column": "email_open_rate_touch"}] | [] | False |
| B1 | AVG(email_click_to_open_rate_touch) | [{"table": "klaviyo__person_campaign_flow", "column": "email_click_to_open_rate_touch"}] | [] | False |
| B1 | COUNT(*) | [] | [] | True |
| B1 | SUM(has_converted) | [{"table": "klaviyo__person_campaign_flow", "column": "has_converted"}] | [] | False |


## S23

类别 `data`；来源 `query_db`；调用 `c5b1501674684c0db3de3297a8d306d9`；状态 `success`。

```sql
WITH base AS (
  SELECT *,
    CASE 
      WHEN flow_name LIKE 'Welcome%' THEN 'Onboarding'
      WHEN flow_name LIKE 'Cart Recovery%' THEN 'Cart Recovery'
      WHEN flow_name LIKE 'Browse Abandonment%' THEN 'Browse Abandonment'
      WHEN flow_name LIKE 'Post-Purchase%' THEN 'Post-Purchase'
      WHEN flow_name LIKE 'Product Discovery%' THEN 'Product Discovery'
      WHEN flow_name LIKE 'Seasonal%' THEN 'Seasonal'
      WHEN flow_name LIKE 'VIP Loyalty%' THEN 'VIP Loyalty'
      WHEN flow_name LIKE 'Winback%' THEN 'Winback'
    END AS campaign_type,
    SUBSTR(flow_name, INSTR(flow_name,'Variant ')+8, 1) AS variant_letter,
    count_opened_email / NULLIF(count_received_email,0) AS or_calc,
    count_clicked_email / NULLIF(count_opened_email,0) AS ctor_calc
  FROM klaviyo__flows
)
SELECT variant_letter, COUNT(*) AS n,
  ROUND(AVG(or_calc),4) AS mean_or,
  ROUND(AVG(ctor_calc),4) AS mean_ctor,
  ROUND(MIN(or_calc),4) AS min_or, ROUND(MAX(or_calc),4) AS max_or,
  ROUND(MIN(ctor_calc),4) AS min_ctor, ROUND(MAX(ctor_calc),4) AS max_ctor
FROM base
GROUP BY variant_letter
ORDER BY variant_letter
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-096/attempt-01/sql/S23.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-096/attempt-01/sql/S23.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-096/attempt-01/results/S23.rows.jsonl)；完整：True；SHA256：`c9a45d510586d450a07e3b9dd54023cc701d1d53a3935cb564b715c0e6cfef42`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "klaviyo__flows", "kind": "base", "block": null, "base_tables": ["klaviyo__flows"]}] | [] | [] |
| B2 | [{"alias": "base", "kind": "derived", "block": "B1", "base_tables": ["klaviyo__flows"]}] | [] | ["variant_letter"] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B2 | COUNT(*) | [] | [] | True |
| B2 | AVG(or_calc) | [{"table": "klaviyo__flows", "column": "count_opened_email"}, {"table": "klaviyo__flows", "column": "count_received_email"}] | [] | False |
| B2 | AVG(ctor_calc) | [{"table": "klaviyo__flows", "column": "count_clicked_email"}, {"table": "klaviyo__flows", "column": "count_opened_email"}] | [] | False |
| B2 | MIN(or_calc) | [{"table": "klaviyo__flows", "column": "count_opened_email"}, {"table": "klaviyo__flows", "column": "count_received_email"}] | [] | False |
| B2 | MAX(or_calc) | [{"table": "klaviyo__flows", "column": "count_opened_email"}, {"table": "klaviyo__flows", "column": "count_received_email"}] | [] | False |
| B2 | MIN(ctor_calc) | [{"table": "klaviyo__flows", "column": "count_clicked_email"}, {"table": "klaviyo__flows", "column": "count_opened_email"}] | [] | False |
| B2 | MAX(ctor_calc) | [{"table": "klaviyo__flows", "column": "count_clicked_email"}, {"table": "klaviyo__flows", "column": "count_opened_email"}] | [] | False |


## S24

类别 `data`；来源 `query_db`；调用 `8f18cdb6a68f40a1acfd04611867f1f7`；状态 `success`。

```sql
WITH base AS (
  SELECT *,
    CASE 
      WHEN flow_name LIKE 'Welcome%' THEN 'Onboarding'
      WHEN flow_name LIKE 'Cart Recovery%' THEN 'Cart Recovery'
      WHEN flow_name LIKE 'Browse Abandonment%' THEN 'Browse Abandonment'
      WHEN flow_name LIKE 'Post-Purchase%' THEN 'Post-Purchase'
      WHEN flow_name LIKE 'Product Discovery%' THEN 'Product Discovery'
      WHEN flow_name LIKE 'Seasonal%' THEN 'Seasonal'
      WHEN flow_name LIKE 'VIP Loyalty%' THEN 'VIP Loyalty'
      WHEN flow_name LIKE 'Winback%' THEN 'Winback'
    END AS campaign_type,
    SUBSTR(flow_name, INSTR(flow_name,'Variant ')+8, 1) AS variant_letter,
    count_opened_email / NULLIF(count_received_email,0) AS or_calc,
    count_clicked_email / NULLIF(count_opened_email,0) AS ctor_calc
  FROM klaviyo__flows
)
SELECT campaign_type, variant_letter, COUNT(*) AS n,
  ROUND(AVG(or_calc),4) AS mean_or,
  ROUND(AVG(ctor_calc),4) AS mean_ctor
FROM base
GROUP BY campaign_type, variant_letter
ORDER BY campaign_type, variant_letter
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-096/attempt-01/sql/S24.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-096/attempt-01/sql/S24.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-096/attempt-01/results/S24.rows.jsonl)；完整：True；SHA256：`1f7dd6fe7971698f47b39af059da79fc4ac8c0dd692b92795f9c5e7627905ffc`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "klaviyo__flows", "kind": "base", "block": null, "base_tables": ["klaviyo__flows"]}] | [] | [] |
| B2 | [{"alias": "base", "kind": "derived", "block": "B1", "base_tables": ["klaviyo__flows"]}] | [] | ["campaign_type", "variant_letter"] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B2 | COUNT(*) | [] | [] | True |
| B2 | AVG(or_calc) | [{"table": "klaviyo__flows", "column": "count_opened_email"}, {"table": "klaviyo__flows", "column": "count_received_email"}] | [] | False |
| B2 | AVG(ctor_calc) | [{"table": "klaviyo__flows", "column": "count_clicked_email"}, {"table": "klaviyo__flows", "column": "count_opened_email"}] | [] | False |

