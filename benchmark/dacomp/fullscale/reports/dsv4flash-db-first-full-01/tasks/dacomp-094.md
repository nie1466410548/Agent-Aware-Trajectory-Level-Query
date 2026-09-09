# dacomp-094

Based on the behavioral data from `klaviyo__campaigns` and `klaviyo__persons`, design an a…

运行：已提交。官方未评分。全部 SQL 尝试/成功 22/18；数据 SQL 20/16；Python 3 次。

完整原题：

Based on the behavioral data from `klaviyo__campaigns` and `klaviyo__persons`, design an analysis to evaluate the interactive impact of different email delivery timing windows and subject line themes on `open_rate`, `click_rate`, and subsequent active retention (`active_retention_rate_week`, `active_retention_rate_month`).

The analysis should focus on the combined effect of:
- **Sending Time Windows**, specifically segmented into: ① Weekdays vs. Weekends, ② Morning (0-12h) vs. Afternoon (12-24h), and ③ 3 days before a holiday vs. 3 days after a holiday.
- **Subject Line Content**, grouped by keywords in the subject: discount-related / new product launch / storytelling.

| 表 | 行数 | 列数 |
| --- | --- | --- |
| klaviyo__events | 4 | 48 |
| klaviyo__person_campaign_flow | 4 | 32 |
| klaviyo__persons | 1192 | 49 |


实际路线（分析者依据 SQL/源码概括，不代表 Agent 自述）：SQL 连接和活动指标提取 → Python 分组均值及图表 → 提交

数据库大小：507,904 字节。

## 数据 SQL

| SQL | 状态 | 基础表 | Join 输入/类型 | GROUP BY | 聚合表达式 | 结果行数 | 数据库 ms |
| --- | --- | --- | --- | --- | --- | --- | --- |
| [S3/Q1](#s3) | success | ["klaviyo__events"] | 0 / {} | [] | [] | 4 | 0.664 |
| [S4/Q2](#s4) | success | ["klaviyo__persons"] | 0 / {} | [] | [] | 5 | 0.536 |
| [S5/Q3](#s5) | success | ["klaviyo__person_campaign_flow"] | 0 / {} | [] | [] | 4 | 0.397 |
| [S6/Q4](#s6) | success | ["klaviyo__events"] | 0 / {} | ["campaign_name", "campaign_subject_line"] | ["COUNT(*)", "COUNT(DISTINCT person_id)", "MIN(occurred_at)", "MAX(occurred_at)"] | 3 | 0.451 |
| [S7/Q5](#s7) | success | ["klaviyo__events"] | 0 / {} | ["type"] | ["COUNT(*)", "COUNT(DISTINCT metric_id)"] | 2 | 0.325 |
| [S8/Q6](#s8) | success | ["klaviyo__events"] | 0 / {} | [] | ["COUNT(*)"] | 1 | 0.302 |
| [S9/Q7](#s9) | success | ["klaviyo__persons"] | 0 / {} | [] | ["COUNT(*)"] | 1 | 0.617 |
| [S10/Q8](#s10) | success | ["klaviyo__person_campaign_flow"] | 0 / {} | [] | ["COUNT(*)"] | 1 | 0.287 |
| [S11/Q9](#s11) | success | ["klaviyo__events"] | 0 / {} | [] | [] | 2 | 0.36 |
| [S12/Q10](#s12) | success | ["klaviyo__person_campaign_flow"] | 0 / {} | [] | [] | 4 | 0.369 |
| [S13/Q11](#s13) | success | ["klaviyo__events"] | 0 / {} | [] | [] | 4 | 0.366 |
| [S14/Q12](#s14) | success | ["klaviyo__persons"] | 0 / {} | [] | [] | 2 | 0.58 |
| [S15/Q13](#s15) | success | ["klaviyo__events"] | 0 / {} | [] | [] | 3 | 0.363 |
| [S16/Q14](#s16) | failed | ["klaviyo__events", "klaviyo__person_campaign_flow", "klaviyo__persons"] | 3 / {'LEFT': 1, 'INNER': 1} | [] | ["MIN(ABS(JULIANDAY(SUBSTRING(t.send_at, 1, 10)) - JULIANDAY(h.d)))"] | unknown | 未取得；调用总时长 0.403 ms |
| [S17/Q15](#s17) | failed | ["klaviyo__events", "klaviyo__person_campaign_flow", "klaviyo__persons"] | 3 / {'LEFT': 1, 'INNER': 1} | [] | ["MIN(ABS(JULIANDAY(SUBSTRING(t2.send_at, 1, 10)) - JULIANDAY(h.d)))"] | unknown | 未取得；调用总时长 0.383 ms |
| [S18/Q16](#s18) | failed | ["klaviyo__events", "klaviyo__person_campaign_flow", "klaviyo__persons"] | 3 / {'LEFT': 1, 'INNER': 2} | [] | ["MIN(ABS(JULIANDAY(SUBSTRING(t3.send_at, 1, 10)) - JULIANDAY(h.d)))"] | unknown | 未取得；调用总时长 0.488 ms |
| [S19/Q17](#s19) | failed | ["klaviyo__events", "klaviyo__person_campaign_flow", "klaviyo__persons"] | 3 / {'LEFT': 1, 'INNER': 1, 'CROSS': 1} | [] | [] | unknown | 未取得；调用总时长 0.388 ms |
| [S20/Q18](#s20) | success | ["klaviyo__events", "klaviyo__person_campaign_flow", "klaviyo__persons"] | 3 / {'LEFT': 1, 'INNER': 1, 'CROSS': 1} | [] | [] | 4 | 3.414 |
| [S21/Q19](#s21) | success | ["klaviyo__persons"] | 0 / {} | [] | ["COUNT(*)", "AVG(active_retention_rate_week)", "AVG(active_retention_rate_month)", "AVG(email_open_rate)", "MIN(active_retention_rate_week)", "MAX(active_retention_rate_week)", "MIN(active_retention_rate_month)", "MAX(active_retention_rate_month)"] | 1 | 1.056 |
| [S22/Q20](#s22) | success | ["klaviyo__events"] | 0 / {} | ["campaign_name", "campaign_subject_line"] | ["COUNT(*)"] | 3 | 0.364 |


## 元数据和设置

| SQL | 类别 | 状态 | 内容 |
| --- | --- | --- | --- |
| S1 | connection_setup | success | PRAGMA query_only=ON |
| S2 | metadata | success | SELECT name,sql FROM sqlite_master WHERE type='table' ORDER BY name |


## Python 与执行位置

人工源码审查：**database_first_violation**。Python 读取 S20 结果后按日间时段、月份半段、主题及交互组求打开率、点击率和留存率均值；pivot_table 同时再次聚合。分组均值和图表输入汇总可以通过 SQL GROUP BY 完成。 [证据](../reviews/dacomp-094.json)。

P1：The dataset is very small (N=4 campaign-person touches). I need to compute cross-tabulations, create visualizations for interaction effects, and compute descriptive statistics. SQLite lacks the statistical capabilities for ANOVA and the plotting tools needed for interaction plots. Python with pandas, scipy, and matplotlib is necessary for these analytic and visual tasks.

[源码](../../../runs/dsv4flash-db-first-full-01/dacomp-094/attempt-01/python/P1.py)；[输出](../../../runs/dsv4flash-db-first-full-01/dacomp-094/attempt-01/python/P1.stdout)；[错误](../../../runs/dsv4flash-db-first-full-01/dacomp-094/attempt-01/python/P1.stderr)。检出需人工核验的 SQL 可实现操作：groupby(；不能仅凭理由判为合规。

P2：I need to inspect the raw format of the archived SQL results to correctly load the analysis dataset into pandas. This is a data loading/debugging step required before any statistical analysis.

[源码](../../../runs/dsv4flash-db-first-full-01/dacomp-094/attempt-01/python/P2.py)；[输出](../../../runs/dsv4flash-db-first-full-01/dacomp-094/attempt-01/python/P2.stdout)；[错误](../../../runs/dsv4flash-db-first-full-01/dacomp-094/attempt-01/python/P2.stderr)。自动源码筛查未检出预设迁出信号；这不是全面语义合规证明。

P3：Loading the dataset from the archived JSON lines (arrays) with proper column names from the SQL query result, then performing the full analysis: cross-tabulation, descriptive statistics, and visualization. This is done in Python because SQLite lacks statistical and plotting capabilities.

[源码](../../../runs/dsv4flash-db-first-full-01/dacomp-094/attempt-01/python/P3.py)；[输出](../../../runs/dsv4flash-db-first-full-01/dacomp-094/attempt-01/python/P3.stdout)；[错误](../../../runs/dsv4flash-db-first-full-01/dacomp-094/attempt-01/python/P3.stderr)。检出需人工核验的 SQL 可实现操作：groupby(；不能仅凭理由判为合规。

## 优化机会

已验证候选。筛选限于精确 SQL、相同自包含 CTE、相同单表完整过滤、可分解单表聚合；未覆盖任意 Join 等价和一般谓词蕴含。全部候选都是 offline，未测在线预测。

| 候选 | 类型 | 已有结果 | 覆盖 SQL | 后续次数 | 中间行数 | 验证 | 成本 |
| --- | --- | --- | --- | --- | --- | --- | --- |
| C1 | aggregate MV | False | ["S8", "S22"] | 1 | 3 | verified | Not benchmarked; correctness alone does not establish net speedup. |
| C2 | aggregate MV | False | ["S9", "S21"] | 1 | 1 | verified | Not benchmarked; correctness alone does not establish net speedup. |


已验证覆盖（含触发查询、候选并集去重）：4/16 条成功数据 SQL。正确性仅针对当前数据库快照；未测性能的候选不能声称已加速。

[完整 build/rewrite 与比较证据](dacomp-094.analysis.json)。

### C1：aggregate MV

Union of grouping keys; decomposable aggregate states; AVG uses SUM and non-NULL COUNT.

原查询 [S8](#s8), [S22](#s22) → 新增共享状态 C1 → 后续 1 次可复用。该构建点为事后假设，不代表 Agent 当时预知后续。

构建定义：

```sql
SELECT campaign_name AS __g0, campaign_subject_line AS __g1, COUNT(*) AS __a0 FROM "klaviyo__events"  GROUP BY campaign_name, campaign_subject_line
```

受益查询 S8 的改写示例：

```sql
SELECT SUM(__a0) AS total_events FROM temp.reuse_candidate
```

| 原 SQL | 列名一致 | 结果一致 | 比较方法 |
| --- | --- | --- | --- |
| S8 | True | True | exact_multiset |
| S22 | True | True | exact_multiset |


验证状态：verified；成本结论：Not benchmarked; correctness alone does not establish net speedup.

### C2：aggregate MV

Union of grouping keys; decomposable aggregate states; AVG uses SUM and non-NULL COUNT.

原查询 [S9](#s9), [S21](#s21) → 新增共享状态 C2 → 后续 1 次可复用。该构建点为事后假设，不代表 Agent 当时预知后续。

构建定义：

```sql
SELECT COUNT(*) AS __a0, SUM(active_retention_rate_week) AS __a1_sum, COUNT(active_retention_rate_week) AS __a1_n, SUM(active_retention_rate_month) AS __a2_sum, COUNT(active_retention_rate_month) AS __a2_n, SUM(email_open_rate) AS __a3_sum, COUNT(email_open_rate) AS __a3_n, MIN(active_retention_rate_week) AS __a4, MAX(active_retention_rate_week) AS __a5, MIN(active_retention_rate_month) AS __a6, MAX(active_retention_rate_month) AS __a7 FROM "klaviyo__persons" 
```

受益查询 S9 的改写示例：

```sql
SELECT SUM(__a0) AS total_persons FROM temp.reuse_candidate
```

| 原 SQL | 列名一致 | 结果一致 | 比较方法 |
| --- | --- | --- | --- |
| S9 | True | True | exact_multiset |
| S21 | True | True | exact_multiset |


验证状态：verified；成本结论：Not benchmarked; correctness alone does not establish net speedup.

结果依赖：自动记录 SQL→Python 的接口父调用，以及源码中引用归档文件的消费者；字面值相同不认定因果。模型方向选择需要人工读取消息，尚未做全面因果标注。

[原始报告](../../../runs/dsv4flash-db-first-full-01/dacomp-094/attempt-01/answer.md)；[统一消息](../../../runs/dsv4flash-db-first-full-01/dacomp-094/attempt-01/messages.jsonl)；[原始 OpenCode 事件](../../../runs/dsv4flash-db-first-full-01/dacomp-094/attempt-01/opencode.jsonl)；[SQL 引擎日志](../../../runs/dsv4flash-db-first-full-01/dacomp-094/attempt-01/sql_journal.jsonl)。

[可读报告（本地图片链接规范化）](../answers/dacomp-094.md)。原始回答保留，分析结论未改写。

## S1

类别 `connection_setup`；来源 `connection`；调用 `c7a2b0bfd0204daea758689a48189217`；状态 `success`。

```sql
PRAGMA query_only=ON
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-094/attempt-01/sql/S1.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-094/attempt-01/sql/S1.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-094/attempt-01/results/S1.rows.jsonl)；完整：True；SHA256：`e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`。

## S2

类别 `metadata`；来源 `list_db`；调用 `c7a2b0bfd0204daea758689a48189217`；状态 `success`。

```sql
SELECT name,sql FROM sqlite_master WHERE type='table' ORDER BY name
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-094/attempt-01/sql/S2.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-094/attempt-01/sql/S2.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-094/attempt-01/results/S2.rows.jsonl)；完整：True；SHA256：`6b5c1efa76cd72ada2ef664a70c3b2863ccd506839c1ee6262063358020515de`。

## S3

类别 `data`；来源 `query_db`；调用 `48cbce49bd5549ed874d3ddc8c14e790`；状态 `success`。

```sql
SELECT * FROM klaviyo__events LIMIT 5
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-094/attempt-01/sql/S3.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-094/attempt-01/sql/S3.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-094/attempt-01/results/S3.rows.jsonl)；完整：True；SHA256：`da940f4aebf704bf143bd829d521be714c563bcac6a366b4f6ec68ef4017c5b2`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "klaviyo__events", "kind": "base", "block": null, "base_tables": ["klaviyo__events"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |


## S4

类别 `data`；来源 `query_db`；调用 `315045aa26764a8b89b5059909e34e1b`；状态 `success`。

```sql
SELECT * FROM klaviyo__persons LIMIT 5
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-094/attempt-01/sql/S4.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-094/attempt-01/sql/S4.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-094/attempt-01/results/S4.rows.jsonl)；完整：True；SHA256：`0a7acc20fbb8c57fbd2829e0378a11d48bd748fac575c29a2652ab7fc7d3d083`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "klaviyo__persons", "kind": "base", "block": null, "base_tables": ["klaviyo__persons"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |


## S5

类别 `data`；来源 `query_db`；调用 `c0db0b7094e242e9957dfcb4ce2e5bde`；状态 `success`。

```sql
SELECT * FROM klaviyo__person_campaign_flow LIMIT 5
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-094/attempt-01/sql/S5.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-094/attempt-01/sql/S5.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-094/attempt-01/results/S5.rows.jsonl)；完整：True；SHA256：`794cdb63a723f0ea5033b6d3032ca06e5c3db8114ce62e3f0fe06367d6b5a3a0`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "klaviyo__person_campaign_flow", "kind": "base", "block": null, "base_tables": ["klaviyo__person_campaign_flow"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |


## S6

类别 `data`；来源 `query_db`；调用 `f7fa077457c24189a5f0f986ab72d2e1`；状态 `success`。

```sql
SELECT campaign_name, campaign_subject_line, COUNT(*) AS n_events, COUNT(DISTINCT person_id) AS n_persons, MIN(occurred_at) AS min_ts, MAX(occurred_at) AS max_ts FROM klaviyo__events WHERE CAMPAIGN_TYPE='email' GROUP BY campaign_name, campaign_subject_line ORDER BY n_events DESC
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-094/attempt-01/sql/S6.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-094/attempt-01/sql/S6.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-094/attempt-01/results/S6.rows.jsonl)；完整：True；SHA256：`8a4cfd51a33e5496c832b3ea10c75686821ebdf724e09c7df159a252c03601a9`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "klaviyo__events", "kind": "base", "block": null, "base_tables": ["klaviyo__events"]}] | [] | ["campaign_name", "campaign_subject_line"] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |
| B1 | COUNT(DISTINCT person_id) | [{"table": "klaviyo__events", "column": "person_id"}] | [] | False |
| B1 | MIN(occurred_at) | [{"table": "klaviyo__events", "column": "occurred_at"}] | [] | False |
| B1 | MAX(occurred_at) | [{"table": "klaviyo__events", "column": "occurred_at"}] | [] | False |


## S7

类别 `data`；来源 `query_db`；调用 `a7436896330a4ee3b7b5a714edb09795`；状态 `success`。

```sql
SELECT type, COUNT(*) AS n, COUNT(DISTINCT metric_id) AS n_metrics FROM klaviyo__events GROUP BY type ORDER BY n DESC
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-094/attempt-01/sql/S7.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-094/attempt-01/sql/S7.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-094/attempt-01/results/S7.rows.jsonl)；完整：True；SHA256：`14245fe2e71096e13375893fccd387bd3b76c23f585b11caf8f4d3131874f099`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "klaviyo__events", "kind": "base", "block": null, "base_tables": ["klaviyo__events"]}] | [] | ["type"] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |
| B1 | COUNT(DISTINCT metric_id) | [{"table": "klaviyo__events", "column": "metric_id"}] | [] | False |


## S8

类别 `data`；来源 `query_db`；调用 `ce419f16fde64cc485e84c3b95e2ba66`；状态 `success`。

```sql
SELECT COUNT(*) AS total_events FROM klaviyo__events
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-094/attempt-01/sql/S8.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-094/attempt-01/sql/S8.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-094/attempt-01/results/S8.rows.jsonl)；完整：True；SHA256：`9d1f4e3a2170ce5f947bcdfa249a77885875b0d9d7af88ad3fbc7f7cd7a224fa`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "klaviyo__events", "kind": "base", "block": null, "base_tables": ["klaviyo__events"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |


## S9

类别 `data`；来源 `query_db`；调用 `46785786a9884ad09a6bc54a45cc7a49`；状态 `success`。

```sql
SELECT COUNT(*) AS total_persons FROM klaviyo__persons
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-094/attempt-01/sql/S9.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-094/attempt-01/sql/S9.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-094/attempt-01/results/S9.rows.jsonl)；完整：True；SHA256：`9f08c25dc6cbc1e501f18da20f78731cfb845e17d1f8840fdab7d95b83e87cb8`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "klaviyo__persons", "kind": "base", "block": null, "base_tables": ["klaviyo__persons"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |


## S10

类别 `data`；来源 `query_db`；调用 `dec7e5df8bd94c12bbac885071c02f9b`；状态 `success`。

```sql
SELECT COUNT(*) AS total_pcf FROM klaviyo__person_campaign_flow
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-094/attempt-01/sql/S10.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-094/attempt-01/sql/S10.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-094/attempt-01/results/S10.rows.jsonl)；完整：True；SHA256：`9d1f4e3a2170ce5f947bcdfa249a77885875b0d9d7af88ad3fbc7f7cd7a224fa`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "klaviyo__person_campaign_flow", "kind": "base", "block": null, "base_tables": ["klaviyo__person_campaign_flow"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |


## S11

类别 `data`；来源 `query_db`；调用 `9357c676f9fe4773aaf68a1ec3fec171`；状态 `success`。

```sql
SELECT DISTINCT campaign_subject_line FROM klaviyo__events
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-094/attempt-01/sql/S11.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-094/attempt-01/sql/S11.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-094/attempt-01/results/S11.rows.jsonl)；完整：True；SHA256：`30cc17c0a19b6a75f80682ca3ec83f4382fe909abd1d5500c4db5ace521f9cd4`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "klaviyo__events", "kind": "base", "block": null, "base_tables": ["klaviyo__events"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |


## S12

类别 `data`；来源 `query_db`；调用 `8bf0615965cd4e9e8feaa26be81bf9c4`；状态 `success`。

```sql
SELECT person_id, last_touch_campaign_id, last_touch_flow_id, variation_id, first_event_at, last_event_at, touch_span_days, count_received_email, count_opened_email, count_clicked_email, email_open_rate_touch, email_click_to_open_rate_touch, net_revenue_touch, has_converted FROM klaviyo__person_campaign_flow
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-094/attempt-01/sql/S12.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-094/attempt-01/sql/S12.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-094/attempt-01/results/S12.rows.jsonl)；完整：True；SHA256：`09294ef3fa66dca47f77a6d877a58fd94659d5b79046a432b2c1d24c157ef94d`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "klaviyo__person_campaign_flow", "kind": "base", "block": null, "base_tables": ["klaviyo__person_campaign_flow"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |


## S13

类别 `data`；来源 `query_db`；调用 `607106e7946747d9bc618c00d6022351`；状态 `success`。

```sql
SELECT person_id, event_id, type, occurred_at, campaign_name, campaign_subject_line, last_touch_campaign_id, is_attributed, day_opened_email, day_clicked_email, day_click_to_open_rate FROM klaviyo__events ORDER BY occurred_at
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-094/attempt-01/sql/S13.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-094/attempt-01/sql/S13.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-094/attempt-01/results/S13.rows.jsonl)；完整：True；SHA256：`46b91b1863b6fce4c56de83ffbb8088c27d7b56cb11c0158f5a1404d88694b1d`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "klaviyo__events", "kind": "base", "block": null, "base_tables": ["klaviyo__events"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |


## S14

类别 `data`；来源 `query_db`；调用 `0254f6bb29494970b0bf8663cbd0ccc5`；状态 `success`。

```sql
SELECT person_id, email_open_rate, active_retention_rate_week, active_retention_rate_month, active_days, active_weeks, active_months, days_span, weeks_span, months_span, count_received_email, count_opened_email, count_clicked_email FROM klaviyo__persons WHERE person_id IN ('01F366M1ZERT4HM2Z9R2V9G7BY','59bc0505-cb93-40a1-9524-437521d13454')
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-094/attempt-01/sql/S14.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-094/attempt-01/sql/S14.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-094/attempt-01/results/S14.rows.jsonl)；完整：True；SHA256：`960ccd94c4f1ed50e44535b36de84a6c615b1cb7dda33e105fdba6d16def8e0f`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "klaviyo__persons", "kind": "base", "block": null, "base_tables": ["klaviyo__persons"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |


## S15

类别 `data`；来源 `query_db`；调用 `93e99606f6ea4737b210475f2dade851`；状态 `success`。

```sql
SELECT DISTINCT last_touch_campaign_id, campaign_name, campaign_subject_line FROM klaviyo__events ORDER BY last_touch_campaign_id
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-094/attempt-01/sql/S15.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-094/attempt-01/sql/S15.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-094/attempt-01/results/S15.rows.jsonl)；完整：True；SHA256：`e84b48b6bf54c1e89c611386a92fd3e281c91b0a91590917a40e5e873aedf360`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "klaviyo__events", "kind": "base", "block": null, "base_tables": ["klaviyo__events"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |


## S16

类别 `data`；来源 `query_db`；调用 `d4c745aba61d4a0ca2018a9575b84100`；状态 `failed`。

```sql
WITH holidays(d) AS (
  SELECT '2022-01-01' UNION SELECT '2022-01-17' UNION SELECT '2022-02-21' UNION SELECT '2022-05-30' UNION SELECT '2022-06-20' UNION SELECT '2022-07-04' UNION SELECT '2022-09-05' UNION SELECT '2022-10-10' UNION SELECT '2022-11-11' UNION SELECT '2022-11-24' UNION SELECT '2022-12-26'
  UNION SELECT '2023-01-02' UNION SELECT '2023-01-16' UNION SELECT '2023-02-20' UNION SELECT '2023-05-29' UNION SELECT '2023-06-19' UNION SELECT '2023-07-04' UNION SELECT '2023-09-04' UNION SELECT '2023-10-09' UNION SELECT '2023-11-10' UNION SELECT '2023-11-23' UNION SELECT '2023-12-25'
  UNION SELECT '2024-01-01' UNION SELECT '2024-01-15' UNION SELECT '2024-02-19'
),
camp AS (
  SELECT DISTINCT last_touch_campaign_id AS campaign_id, campaign_name, campaign_subject_line FROM klaviyo__events
),
t AS (
  SELECT pcf.person_id,
         pcf.last_touch_campaign_id AS campaign_id,
         camp.campaign_name,
         camp.campaign_subject_line,
         pcf.first_event_at AS send_at,
         pcf.email_open_rate_touch AS open_rate,
         pcf.email_click_to_open_rate_touch AS click_rate,
         pcf.count_received_email, pcf.count_opened_email, pcf.count_clicked_email,
         pcf.net_revenue_touch,
         p.active_retention_rate_week, p.active_retention_rate_month,
         p.email_open_rate AS person_email_open_rate,
         CAST(strftime('%w', pcf.first_event_at) AS INTEGER) AS dow,
         CAST(strftime('%H', pcf.first_event_at) AS INTEGER) AS hour
  FROM klaviyo__person_campaign_flow pcf
  LEFT JOIN camp ON camp.campaign_id = pcf.last_touch_campaign_id
  JOIN klaviyo__persons p ON p.person_id = pcf.person_id
)
SELECT t.*,
       CASE WHEN t.dow IN (0,6) THEN 'weekend' ELSE 'weekday' END AS day_part,
       CASE WHEN t.hour < 12 THEN 'morning' ELSE 'afternoon' END AS time_half,
       CASE WHEN lower(t.campaign_subject_line) LIKE '%launch%' THEN 'new_product_launch'
            WHEN lower(t.campaign_subject_line) LIKE '%offer%' OR lower(t.campaign_subject_line) LIKE '%sale%' OR lower(t.campaign_subject_line) LIKE '%discount%' OR lower(t.campaign_subject_line) LIKE '%deal%' OR lower(t.campaign_subject_line) LIKE '%save%' THEN 'discount'
            WHEN lower(t.campaign_subject_line) LIKE '%story%' OR lower(t.campaign_subject_line) LIKE '%journey%' OR lower(t.campaign_subject_line) LIKE '%behind%' THEN 'storytelling'
            ELSE 'unknown' END AS theme,
       (SELECT MIN(ABS(julianday(substr(t.send_at,1,10)) - julianday(h.d))) FROM holidays h) AS days_to_holiday,
       (SELECT julianday(substr(t.send_at,1,10)) - julianday(h.d) FROM holidays h ORDER BY ABS(julianday(substr(t.send_at,1,10)) - julianday(h.d)) LIMIT 1) AS signed_holiday_diff
FROM t
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-094/attempt-01/sql/S16.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-094/attempt-01/sql/S16.parameters.json)。

错误：`OperationalError('no such column: t.send_at')`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [] | [] | [] |
| B2 | [] | [] | [] |
| B3 | [] | [] | [] |
| B4 | [] | [] | [] |
| B5 | [] | [] | [] |
| B6 | [] | [] | [] |
| B7 | [] | [] | [] |
| B8 | [] | [] | [] |
| B9 | [] | [] | [] |
| B10 | [] | [] | [] |
| B11 | [] | [] | [] |
| B12 | [] | [] | [] |
| B13 | [] | [] | [] |
| B14 | [] | [] | [] |
| B15 | [] | [] | [] |
| B16 | [] | [] | [] |
| B17 | [] | [] | [] |
| B18 | [] | [] | [] |
| B19 | [] | [] | [] |
| B20 | [] | [] | [] |
| B21 | [] | [] | [] |
| B22 | [] | [] | [] |
| B23 | [] | [] | [] |
| B24 | [] | [] | [] |
| B25 | [] | [] | [] |
| B26 | [] | [] | [] |
| B27 | [] | [] | [] |
| B28 | [] | [] | [] |
| B29 | [] | [] | [] |
| B30 | [] | [] | [] |
| B31 | [] | [] | [] |
| B32 | [] | [] | [] |
| B33 | [] | [] | [] |
| B34 | [] | [] | [] |
| B35 | [] | [] | [] |
| B36 | [] | [] | [] |
| B37 | [] | [] | [] |
| B38 | [] | [] | [] |
| B39 | [] | [] | [] |
| B40 | [] | [] | [] |
| B41 | [] | [] | [] |
| B42 | [] | [] | [] |
| B43 | [] | [] | [] |
| B44 | [] | [] | [] |
| B45 | [] | [] | [] |
| B46 | [] | [] | [] |
| B47 | [] | [] | [] |
| B48 | [] | [] | [] |
| B49 | [] | [] | [] |
| B50 | [{"alias": "klaviyo__events", "kind": "base", "block": null, "base_tables": ["klaviyo__events"]}] | [] | [] |
| B51 | [{"alias": "camp", "kind": "derived", "block": "B50", "base_tables": ["klaviyo__events"]}, {"alias": "pcf", "kind": "base", "block": null, "base_tables": ["klaviyo__person_campaign_flow"]}, {"alias": "p", "kind": "base", "block": null, "base_tables": ["klaviyo__persons"]}] | [{"type": "LEFT", "right": "camp", "on": "camp.campaign_id = pcf.last_touch_campaign_id", "using": []}, {"type": "INNER", "right": "klaviyo__persons AS p", "on": "p.person_id = pcf.person_id", "using": []}] | [] |
| B52 | [{"alias": "h", "kind": "derived", "block": "B49", "base_tables": []}] | [] | [] |
| B53 | [{"alias": "h", "kind": "derived", "block": "B49", "base_tables": []}] | [] | [] |
| B54 | [{"alias": "t", "kind": "derived", "block": "B51", "base_tables": ["klaviyo__events", "klaviyo__person_campaign_flow", "klaviyo__persons"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B52 | MIN(ABS(JULIANDAY(SUBSTRING(t.send_at, 1, 10)) - JULIANDAY(h.d))) | [{"unknown": "h.d"}, {"table": "klaviyo__person_campaign_flow", "column": "first_event_at"}] | [] | False |


未解析列血缘：[{"column": "h.d", "reason": "derived_star_or_missing_output"}, {"column": "h.d", "reason": "derived_star_or_missing_output"}, {"column": "h.d", "reason": "derived_star_or_missing_output"}, {"column": "h.d", "reason": "derived_star_or_missing_output"}]

## S17

类别 `data`；来源 `query_db`；调用 `134f14c1c44245078daec067cb23d80e`；状态 `failed`。

```sql
WITH holidays(d) AS (
  SELECT '2022-01-01' UNION SELECT '2022-01-17' UNION SELECT '2022-02-21' UNION SELECT '2022-05-30' UNION SELECT '2022-06-20' UNION SELECT '2022-07-04' UNION SELECT '2022-09-05' UNION SELECT '2022-10-10' UNION SELECT '2022-11-11' UNION SELECT '2022-11-24' UNION SELECT '2022-12-26'
  UNION SELECT '2023-01-02' UNION SELECT '2023-01-16' UNION SELECT '2023-02-20' UNION SELECT '2023-05-29' UNION SELECT '2023-06-19' UNION SELECT '2023-07-04' UNION SELECT '2023-09-04' UNION SELECT '2023-10-09' UNION SELECT '2023-11-10' UNION SELECT '2023-11-23' UNION SELECT '2023-12-25'
  UNION SELECT '2024-01-01' UNION SELECT '2024-01-15' UNION SELECT '2024-02-19'
),
camp AS (
  SELECT DISTINCT last_touch_campaign_id AS campaign_id, campaign_name, campaign_subject_line FROM klaviyo__events
),
t AS (
  SELECT pcf.person_id,
         pcf.last_touch_campaign_id AS campaign_id,
         camp.campaign_name,
         camp.campaign_subject_line,
         pcf.first_event_at AS send_at,
         pcf.email_open_rate_touch AS open_rate,
         pcf.email_click_to_open_rate_touch AS click_rate,
         pcf.count_received_email, pcf.count_opened_email, pcf.count_clicked_email,
         pcf.net_revenue_touch,
         p.active_retention_rate_week, p.active_retention_rate_month,
         p.email_open_rate AS person_email_open_rate,
         CAST(strftime('%w', pcf.first_event_at) AS INTEGER) AS dow,
         CAST(strftime('%H', pcf.first_event_at) AS INTEGER) AS hour
  FROM klaviyo__person_campaign_flow pcf
  LEFT JOIN camp ON camp.campaign_id = pcf.last_touch_campaign_id
  JOIN klaviyo__persons p ON p.person_id = pcf.person_id
)
SELECT t.person_id, t.campaign_id, t.campaign_name, t.campaign_subject_line, t.send_at,
       t.open_rate, t.click_rate, t.count_received_email, t.count_opened_email, t.count_clicked_email,
       t.net_revenue_touch, t.active_retention_rate_week, t.active_retention_rate_month,
       t.person_email_open_rate, t.dow, t.hour,
       CASE WHEN t.dow IN (0,6) THEN 'weekend' ELSE 'weekday' END AS day_part,
       CASE WHEN t.hour < 12 THEN 'morning' ELSE 'afternoon' END AS time_half,
       CASE WHEN lower(COALESCE(t.campaign_subject_line,'')) LIKE '%launch%' THEN 'new_product_launch'
            WHEN lower(COALESCE(t.campaign_subject_line,'')) LIKE '%offer%' OR lower(COALESCE(t.campaign_subject_line,'')) LIKE '%sale%' OR lower(COALESCE(t.campaign_subject_line,'')) LIKE '%discount%' OR lower(COALESCE(t.campaign_subject_line,'')) LIKE '%deal%' OR lower(COALESCE(t.campaign_subject_line,'')) LIKE '%save%' THEN 'discount'
            WHEN lower(COALESCE(t.campaign_subject_line,'')) LIKE '%story%' OR lower(COALESCE(t.campaign_subject_line,'')) LIKE '%journey%' OR lower(COALESCE(t.campaign_subject_line,'')) LIKE '%behind%' THEN 'storytelling'
            ELSE 'unknown' END AS theme,
       (SELECT MIN(ABS(julianday(substr(t2.send_at,1,10)) - julianday(h.d))) FROM holidays h) AS days_to_holiday,
       (SELECT julianday(substr(t2.send_at,1,10)) - julianday(h.d) FROM holidays h ORDER BY ABS(julianday(substr(t2.send_at,1,10)) - julianday(h.d)) LIMIT 1) AS signed_holiday_diff
FROM t t2
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-094/attempt-01/sql/S17.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-094/attempt-01/sql/S17.parameters.json)。

错误：`OperationalError('no such column: t.person_id')`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [] | [] | [] |
| B2 | [] | [] | [] |
| B3 | [] | [] | [] |
| B4 | [] | [] | [] |
| B5 | [] | [] | [] |
| B6 | [] | [] | [] |
| B7 | [] | [] | [] |
| B8 | [] | [] | [] |
| B9 | [] | [] | [] |
| B10 | [] | [] | [] |
| B11 | [] | [] | [] |
| B12 | [] | [] | [] |
| B13 | [] | [] | [] |
| B14 | [] | [] | [] |
| B15 | [] | [] | [] |
| B16 | [] | [] | [] |
| B17 | [] | [] | [] |
| B18 | [] | [] | [] |
| B19 | [] | [] | [] |
| B20 | [] | [] | [] |
| B21 | [] | [] | [] |
| B22 | [] | [] | [] |
| B23 | [] | [] | [] |
| B24 | [] | [] | [] |
| B25 | [] | [] | [] |
| B26 | [] | [] | [] |
| B27 | [] | [] | [] |
| B28 | [] | [] | [] |
| B29 | [] | [] | [] |
| B30 | [] | [] | [] |
| B31 | [] | [] | [] |
| B32 | [] | [] | [] |
| B33 | [] | [] | [] |
| B34 | [] | [] | [] |
| B35 | [] | [] | [] |
| B36 | [] | [] | [] |
| B37 | [] | [] | [] |
| B38 | [] | [] | [] |
| B39 | [] | [] | [] |
| B40 | [] | [] | [] |
| B41 | [] | [] | [] |
| B42 | [] | [] | [] |
| B43 | [] | [] | [] |
| B44 | [] | [] | [] |
| B45 | [] | [] | [] |
| B46 | [] | [] | [] |
| B47 | [] | [] | [] |
| B48 | [] | [] | [] |
| B49 | [] | [] | [] |
| B50 | [{"alias": "klaviyo__events", "kind": "base", "block": null, "base_tables": ["klaviyo__events"]}] | [] | [] |
| B51 | [{"alias": "camp", "kind": "derived", "block": "B50", "base_tables": ["klaviyo__events"]}, {"alias": "pcf", "kind": "base", "block": null, "base_tables": ["klaviyo__person_campaign_flow"]}, {"alias": "p", "kind": "base", "block": null, "base_tables": ["klaviyo__persons"]}] | [{"type": "LEFT", "right": "camp", "on": "camp.campaign_id = pcf.last_touch_campaign_id", "using": []}, {"type": "INNER", "right": "klaviyo__persons AS p", "on": "p.person_id = pcf.person_id", "using": []}] | [] |
| B52 | [{"alias": "h", "kind": "derived", "block": "B49", "base_tables": []}] | [] | [] |
| B53 | [{"alias": "h", "kind": "derived", "block": "B49", "base_tables": []}] | [] | [] |
| B54 | [{"alias": "t2", "kind": "derived", "block": "B51", "base_tables": ["klaviyo__events", "klaviyo__person_campaign_flow", "klaviyo__persons"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B52 | MIN(ABS(JULIANDAY(SUBSTRING(t2.send_at, 1, 10)) - JULIANDAY(h.d))) | [{"unknown": "h.d"}, {"table": "klaviyo__person_campaign_flow", "column": "first_event_at"}] | [] | False |


未解析列血缘：[{"column": "h.d", "reason": "derived_star_or_missing_output"}, {"column": "h.d", "reason": "derived_star_or_missing_output"}, {"column": "h.d", "reason": "derived_star_or_missing_output"}, {"column": "h.d", "reason": "derived_star_or_missing_output"}, {"block": "B54", "column": "t.dow", "reason": "ambiguous_or_missing_source"}, {"block": "B54", "column": "t.hour", "reason": "ambiguous_or_missing_source"}, {"block": "B54", "column": "t.campaign_subject_line", "reason": "ambiguous_or_missing_source"}, {"block": "B54", "column": "t.campaign_subject_line", "reason": "ambiguous_or_missing_source"}, {"block": "B54", "column": "t.campaign_subject_line", "reason": "ambiguous_or_missing_source"}, {"block": "B54", "column": "t.campaign_subject_line", "reason": "ambiguous_or_missing_source"}, {"block": "B54", "column": "t.campaign_subject_line", "reason": "ambiguous_or_missing_source"}, {"block": "B54", "column": "t.campaign_subject_line", "reason": "ambiguous_or_missing_source"}, {"block": "B54", "column": "t.campaign_subject_line", "reason": "ambiguous_or_missing_source"}, {"block": "B54", "column": "t.campaign_subject_line", "reason": "ambiguous_or_missing_source"}, {"block": "B54", "column": "t.campaign_subject_line", "reason": "ambiguous_or_missing_source"}, {"block": "B54", "column": "t.person_id", "reason": "ambiguous_or_missing_source"}, {"block": "B54", "column": "t.campaign_id", "reason": "ambiguous_or_missing_source"}, {"block": "B54", "column": "t.campaign_name", "reason": "ambiguous_or_missing_source"}, {"block": "B54", "column": "t.campaign_subject_line", "reason": "ambiguous_or_missing_source"}, {"block": "B54", "column": "t.send_at", "reason": "ambiguous_or_missing_source"}, {"block": "B54", "column": "t.open_rate", "reason": "ambiguous_or_missing_source"}, {"block": "B54", "column": "t.click_rate", "reason": "ambiguous_or_missing_source"}, {"block": "B54", "column": "t.count_received_email", "reason": "ambiguous_or_missing_source"}, {"block": "B54", "column": "t.count_opened_email", "reason": "ambiguous_or_missing_source"}, {"block": "B54", "column": "t.count_clicked_email", "reason": "ambiguous_or_missing_source"}, {"block": "B54", "column": "t.net_revenue_touch", "reason": "ambiguous_or_missing_source"}, {"block": "B54", "column": "t.active_retention_rate_week", "reason": "ambiguous_or_missing_source"}, {"block": "B54", "column": "t.active_retention_rate_month", "reason": "ambiguous_or_missing_source"}, {"block": "B54", "column": "t.person_email_open_rate", "reason": "ambiguous_or_missing_source"}, {"block": "B54", "column": "t.dow", "reason": "ambiguous_or_missing_source"}, {"block": "B54", "column": "t.hour", "reason": "ambiguous_or_missing_source"}, {"block": "B54", "column": "t.dow", "reason": "ambiguous_or_missing_source"}, {"block": "B54", "column": "t.hour", "reason": "ambiguous_or_missing_source"}, {"block": "B54", "column": "t.campaign_subject_line", "reason": "ambiguous_or_missing_source"}, {"block": "B54", "column": "t.campaign_subject_line", "reason": "ambiguous_or_missing_source"}, {"block": "B54", "column": "t.campaign_subject_line", "reason": "ambiguous_or_missing_source"}, {"block": "B54", "column": "t.campaign_subject_line", "reason": "ambiguous_or_missing_source"}, {"block": "B54", "column": "t.campaign_subject_line", "reason": "ambiguous_or_missing_source"}, {"block": "B54", "column": "t.campaign_subject_line", "reason": "ambiguous_or_missing_source"}, {"block": "B54", "column": "t.campaign_subject_line", "reason": "ambiguous_or_missing_source"}, {"block": "B54", "column": "t.campaign_subject_line", "reason": "ambiguous_or_missing_source"}, {"block": "B54", "column": "t.campaign_subject_line", "reason": "ambiguous_or_missing_source"}]

## S18

类别 `data`；来源 `query_db`；调用 `36bf8badb5da4ed4a6dd5d476e8a81e7`；状态 `failed`。

```sql
WITH holidays(d) AS (
  SELECT '2022-01-01' UNION SELECT '2022-01-17' UNION SELECT '2022-02-21' UNION SELECT '2022-05-30' UNION SELECT '2022-06-20' UNION SELECT '2022-07-04' UNION SELECT '2022-09-05' UNION SELECT '2022-10-10' UNION SELECT '2022-11-11' UNION SELECT '2022-11-24' UNION SELECT '2022-12-26'
  UNION SELECT '2023-01-02' UNION SELECT '2023-01-16' UNION SELECT '2023-02-20' UNION SELECT '2023-05-29' UNION SELECT '2023-06-19' UNION SELECT '2023-07-04' UNION SELECT '2023-09-04' UNION SELECT '2023-10-09' UNION SELECT '2023-11-10' UNION SELECT '2023-11-23' UNION SELECT '2023-12-25'
  UNION SELECT '2024-01-01' UNION SELECT '2024-01-15' UNION SELECT '2024-02-19'
),
camp AS (
  SELECT DISTINCT last_touch_campaign_id AS campaign_id, campaign_name, campaign_subject_line FROM klaviyo__events
),
t AS (
  SELECT pcf.person_id,
         pcf.last_touch_campaign_id AS campaign_id,
         camp.campaign_name,
         camp.campaign_subject_line,
         pcf.first_event_at AS send_at,
         pcf.email_open_rate_touch AS open_rate,
         pcf.email_click_to_open_rate_touch AS click_rate,
         pcf.count_received_email, pcf.count_opened_email, pcf.count_clicked_email,
         pcf.net_revenue_touch,
         p.active_retention_rate_week, p.active_retention_rate_month,
         p.email_open_rate AS person_email_open_rate,
         CAST(strftime('%w', pcf.first_event_at) AS INTEGER) AS dow,
         CAST(strftime('%H', pcf.first_event_at) AS INTEGER) AS hour
  FROM klaviyo__person_campaign_flow pcf
  LEFT JOIN camp ON camp.campaign_id = pcf.last_touch_campaign_id
  JOIN klaviyo__persons p ON p.person_id = pcf.person_id
)
SELECT t2.person_id, t2.campaign_id, t2.campaign_name, t2.campaign_subject_line, t2.send_at,
       t2.open_rate, t2.click_rate, t2.count_received_email, t2.count_opened_email, t2.count_clicked_email,
       t2.net_revenue_touch, t2.active_retention_rate_week, t2.active_retention_rate_month,
       t2.person_email_open_rate, t2.dow, t2.hour,
       CASE WHEN t2.dow IN (0,6) THEN 'weekend' ELSE 'weekday' END AS day_part,
       CASE WHEN t2.hour < 12 THEN 'morning' ELSE 'afternoon' END AS time_half,
       CASE WHEN lower(COALESCE(t2.campaign_subject_line,'')) LIKE '%launch%' THEN 'new_product_launch'
            WHEN lower(COALESCE(t2.campaign_subject_line,'')) LIKE '%offer%' OR lower(COALESCE(t2.campaign_subject_line,'')) LIKE '%sale%' OR lower(COALESCE(t2.campaign_subject_line,'')) LIKE '%discount%' OR lower(COALESCE(t2.campaign_subject_line,'')) LIKE '%deal%' OR lower(COALESCE(t2.campaign_subject_line,'')) LIKE '%save%' THEN 'discount'
            WHEN lower(COALESCE(t2.campaign_subject_line,'')) LIKE '%story%' OR lower(COALESCE(t2.campaign_subject_line,'')) LIKE '%journey%' OR lower(COALESCE(t2.campaign_subject_line,'')) LIKE '%behind%' THEN 'storytelling'
            ELSE 'unknown' END AS theme,
       (SELECT MIN(ABS(julianday(substr(t3.send_at,1,10)) - julianday(h.d))) FROM holidays h) AS days_to_holiday,
       (SELECT julianday(substr(t3.send_at,1,10)) - julianday(h.d) FROM holidays h ORDER BY ABS(julianday(substr(t3.send_at,1,10)) - julianday(h.d)) LIMIT 1) AS signed_holiday_diff
FROM t t2
JOIN (SELECT send_at FROM t) t3 ON t3.send_at = t2.send_at
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-094/attempt-01/sql/S18.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-094/attempt-01/sql/S18.parameters.json)。

错误：`OperationalError('no such column: t3.send_at')`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [] | [] | [] |
| B2 | [] | [] | [] |
| B3 | [] | [] | [] |
| B4 | [] | [] | [] |
| B5 | [] | [] | [] |
| B6 | [] | [] | [] |
| B7 | [] | [] | [] |
| B8 | [] | [] | [] |
| B9 | [] | [] | [] |
| B10 | [] | [] | [] |
| B11 | [] | [] | [] |
| B12 | [] | [] | [] |
| B13 | [] | [] | [] |
| B14 | [] | [] | [] |
| B15 | [] | [] | [] |
| B16 | [] | [] | [] |
| B17 | [] | [] | [] |
| B18 | [] | [] | [] |
| B19 | [] | [] | [] |
| B20 | [] | [] | [] |
| B21 | [] | [] | [] |
| B22 | [] | [] | [] |
| B23 | [] | [] | [] |
| B24 | [] | [] | [] |
| B25 | [] | [] | [] |
| B26 | [] | [] | [] |
| B27 | [] | [] | [] |
| B28 | [] | [] | [] |
| B29 | [] | [] | [] |
| B30 | [] | [] | [] |
| B31 | [] | [] | [] |
| B32 | [] | [] | [] |
| B33 | [] | [] | [] |
| B34 | [] | [] | [] |
| B35 | [] | [] | [] |
| B36 | [] | [] | [] |
| B37 | [] | [] | [] |
| B38 | [] | [] | [] |
| B39 | [] | [] | [] |
| B40 | [] | [] | [] |
| B41 | [] | [] | [] |
| B42 | [] | [] | [] |
| B43 | [] | [] | [] |
| B44 | [] | [] | [] |
| B45 | [] | [] | [] |
| B46 | [] | [] | [] |
| B47 | [] | [] | [] |
| B48 | [] | [] | [] |
| B49 | [] | [] | [] |
| B50 | [{"alias": "klaviyo__events", "kind": "base", "block": null, "base_tables": ["klaviyo__events"]}] | [] | [] |
| B51 | [{"alias": "camp", "kind": "derived", "block": "B50", "base_tables": ["klaviyo__events"]}, {"alias": "pcf", "kind": "base", "block": null, "base_tables": ["klaviyo__person_campaign_flow"]}, {"alias": "p", "kind": "base", "block": null, "base_tables": ["klaviyo__persons"]}] | [{"type": "LEFT", "right": "camp", "on": "camp.campaign_id = pcf.last_touch_campaign_id", "using": []}, {"type": "INNER", "right": "klaviyo__persons AS p", "on": "p.person_id = pcf.person_id", "using": []}] | [] |
| B52 | [{"alias": "t", "kind": "derived", "block": "B51", "base_tables": ["klaviyo__events", "klaviyo__person_campaign_flow", "klaviyo__persons"]}] | [] | [] |
| B53 | [{"alias": "h", "kind": "derived", "block": "B49", "base_tables": []}] | [] | [] |
| B54 | [{"alias": "h", "kind": "derived", "block": "B49", "base_tables": []}] | [] | [] |
| B55 | [{"alias": "t2", "kind": "derived", "block": "B51", "base_tables": ["klaviyo__events", "klaviyo__person_campaign_flow", "klaviyo__persons"]}, {"alias": "t3", "kind": "derived", "block": "B52", "base_tables": ["klaviyo__events", "klaviyo__person_campaign_flow", "klaviyo__persons"]}] | [{"type": "INNER", "right": "(SELECT send_at FROM t) AS t3", "on": "t3.send_at = t2.send_at", "using": []}] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B53 | MIN(ABS(JULIANDAY(SUBSTRING(t3.send_at, 1, 10)) - JULIANDAY(h.d))) | [{"unknown": "h.d"}, {"table": "klaviyo__person_campaign_flow", "column": "first_event_at"}] | [] | False |


未解析列血缘：[{"column": "h.d", "reason": "derived_star_or_missing_output"}, {"column": "h.d", "reason": "derived_star_or_missing_output"}, {"column": "h.d", "reason": "derived_star_or_missing_output"}, {"column": "h.d", "reason": "derived_star_or_missing_output"}]

## S19

类别 `data`；来源 `query_db`；调用 `44a6acbbbe9243c4be1e97a0f0693849`；状态 `failed`。

```sql
WITH holidays(d) AS (
  SELECT '2022-01-01' UNION SELECT '2022-01-17' UNION SELECT '2022-02-21' UNION SELECT '2022-05-30' UNION SELECT '2022-06-20' UNION SELECT '2022-07-04' UNION SELECT '2022-09-05' UNION SELECT '2022-10-10' UNION SELECT '2022-11-11' UNION SELECT '2022-11-24' UNION SELECT '2022-12-26'
  UNION SELECT '2023-01-02' UNION SELECT '2023-01-16' UNION SELECT '2023-02-20' UNION SELECT '2023-05-29' UNION SELECT '2023-06-19' UNION SELECT '2023-07-04' UNION SELECT '2023-09-04' UNION SELECT '2023-10-09' UNION SELECT '2023-11-10' UNION SELECT '2023-11-23' UNION SELECT '2023-12-25'
  UNION SELECT '2024-01-01' UNION SELECT '2024-01-15' UNION SELECT '2024-02-19'
),
camp AS (
  SELECT DISTINCT last_touch_campaign_id AS campaign_id, campaign_name, campaign_subject_line FROM klaviyo__events
),
t AS (
  SELECT pcf.person_id,
         pcf.last_touch_campaign_id AS campaign_id,
         camp.campaign_name,
         camp.campaign_subject_line,
         pcf.first_event_at AS send_at,
         pcf.email_open_rate_touch AS open_rate,
         pcf.email_click_to_open_rate_touch AS click_rate,
         pcf.count_received_email, pcf.count_opened_email, pcf.count_clicked_email,
         pcf.net_revenue_touch,
         p.active_retention_rate_week, p.active_retention_rate_month,
         p.email_open_rate AS person_email_open_rate,
         CAST(strftime('%w', pcf.first_event_at) AS INTEGER) AS dow,
         CAST(strftime('%H', pcf.first_event_at) AS INTEGER) AS hour
  FROM klaviyo__person_campaign_flow pcf
  LEFT JOIN camp ON camp.campaign_id = pcf.last_touch_campaign_id
  JOIN klaviyo__persons p ON p.person_id = pcf.person_id
)
SELECT person_id, campaign_id, campaign_name, campaign_subject_line, send_at, open_rate, click_rate,
       count_received_email, count_opened_email, count_clicked_email, net_revenue_touch,
       active_retention_rate_week, active_retention_rate_month, person_email_open_rate,
       dow, hour, day_part, time_half, theme, holiday, hol_diff
FROM (
  SELECT t2.*,
         h.d AS holiday,
         CAST(julianday(substr(t2.send_at,1,10)) - julianday(h.d) AS INTEGER) AS hol_diff,
         ROW_NUMBER() OVER (PARTITION BY t2.person_id, t2.campaign_id ORDER BY ABS(julianday(substr(t2.send_at,1,10)) - julianday(h.d)), julianday(h.d)) AS rn
  FROM t t2
  CROSS JOIN holidays h
) WHERE rn = 1
ORDER BY send_at
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-094/attempt-01/sql/S19.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-094/attempt-01/sql/S19.parameters.json)。

错误：`OperationalError('no such column: day_part')`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [] | [] | [] |
| B2 | [] | [] | [] |
| B3 | [] | [] | [] |
| B4 | [] | [] | [] |
| B5 | [] | [] | [] |
| B6 | [] | [] | [] |
| B7 | [] | [] | [] |
| B8 | [] | [] | [] |
| B9 | [] | [] | [] |
| B10 | [] | [] | [] |
| B11 | [] | [] | [] |
| B12 | [] | [] | [] |
| B13 | [] | [] | [] |
| B14 | [] | [] | [] |
| B15 | [] | [] | [] |
| B16 | [] | [] | [] |
| B17 | [] | [] | [] |
| B18 | [] | [] | [] |
| B19 | [] | [] | [] |
| B20 | [] | [] | [] |
| B21 | [] | [] | [] |
| B22 | [] | [] | [] |
| B23 | [] | [] | [] |
| B24 | [] | [] | [] |
| B25 | [] | [] | [] |
| B26 | [] | [] | [] |
| B27 | [] | [] | [] |
| B28 | [] | [] | [] |
| B29 | [] | [] | [] |
| B30 | [] | [] | [] |
| B31 | [] | [] | [] |
| B32 | [] | [] | [] |
| B33 | [] | [] | [] |
| B34 | [] | [] | [] |
| B35 | [] | [] | [] |
| B36 | [] | [] | [] |
| B37 | [] | [] | [] |
| B38 | [] | [] | [] |
| B39 | [] | [] | [] |
| B40 | [] | [] | [] |
| B41 | [] | [] | [] |
| B42 | [] | [] | [] |
| B43 | [] | [] | [] |
| B44 | [] | [] | [] |
| B45 | [] | [] | [] |
| B46 | [] | [] | [] |
| B47 | [] | [] | [] |
| B48 | [] | [] | [] |
| B49 | [] | [] | [] |
| B50 | [{"alias": "klaviyo__events", "kind": "base", "block": null, "base_tables": ["klaviyo__events"]}] | [] | [] |
| B51 | [{"alias": "camp", "kind": "derived", "block": "B50", "base_tables": ["klaviyo__events"]}, {"alias": "pcf", "kind": "base", "block": null, "base_tables": ["klaviyo__person_campaign_flow"]}, {"alias": "p", "kind": "base", "block": null, "base_tables": ["klaviyo__persons"]}] | [{"type": "LEFT", "right": "camp", "on": "camp.campaign_id = pcf.last_touch_campaign_id", "using": []}, {"type": "INNER", "right": "klaviyo__persons AS p", "on": "p.person_id = pcf.person_id", "using": []}] | [] |
| B52 | [{"alias": "t2", "kind": "derived", "block": "B51", "base_tables": ["klaviyo__events", "klaviyo__person_campaign_flow", "klaviyo__persons"]}, {"alias": "h", "kind": "derived", "block": "B49", "base_tables": []}] | [{"type": "CROSS", "right": "holidays AS h", "on": null, "using": []}] | [] |
| B53 | [{"alias": "", "kind": "derived", "block": "B52", "base_tables": ["klaviyo__events", "klaviyo__person_campaign_flow", "klaviyo__persons"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |


未解析列血缘：[{"column": "h.d", "reason": "derived_star_or_missing_output"}, {"column": "h.d", "reason": "derived_star_or_missing_output"}, {"column": "h.d", "reason": "derived_star_or_missing_output"}, {"column": "h.d", "reason": "derived_star_or_missing_output"}, {"column": "h.d", "reason": "derived_star_or_missing_output"}, {"column": "h.d", "reason": "derived_star_or_missing_output"}, {"column": "h.d", "reason": "derived_star_or_missing_output"}, {"column": "h.d", "reason": "derived_star_or_missing_output"}, {"column": "h.d", "reason": "derived_star_or_missing_output"}, {"column": "h.d", "reason": "derived_star_or_missing_output"}, {"column": "h.d", "reason": "derived_star_or_missing_output"}, {"column": "h.d", "reason": "derived_star_or_missing_output"}]

## S20

类别 `data`；来源 `query_db`；调用 `d4f4e315f91d4049b347481560fb8b60`；状态 `success`。

```sql
WITH holidays(d) AS (
  SELECT '2022-01-01' UNION SELECT '2022-01-17' UNION SELECT '2022-02-21' UNION SELECT '2022-05-30' UNION SELECT '2022-06-20' UNION SELECT '2022-07-04' UNION SELECT '2022-09-05' UNION SELECT '2022-10-10' UNION SELECT '2022-11-11' UNION SELECT '2022-11-24' UNION SELECT '2022-12-26'
  UNION SELECT '2023-01-02' UNION SELECT '2023-01-16' UNION SELECT '2023-02-20' UNION SELECT '2023-05-29' UNION SELECT '2023-06-19' UNION SELECT '2023-07-04' UNION SELECT '2023-09-04' UNION SELECT '2023-10-09' UNION SELECT '2023-11-10' UNION SELECT '2023-11-23' UNION SELECT '2023-12-25'
  UNION SELECT '2024-01-01' UNION SELECT '2024-01-15' UNION SELECT '2024-02-19'
),
camp AS (
  SELECT DISTINCT last_touch_campaign_id AS campaign_id, campaign_name, campaign_subject_line FROM klaviyo__events
),
t AS (
  SELECT pcf.person_id,
         pcf.last_touch_campaign_id AS campaign_id,
         camp.campaign_name,
         camp.campaign_subject_line,
         pcf.first_event_at AS send_at,
         pcf.email_open_rate_touch AS open_rate,
         pcf.email_click_to_open_rate_touch AS click_rate,
         pcf.count_received_email, pcf.count_opened_email, pcf.count_clicked_email,
         pcf.net_revenue_touch,
         p.active_retention_rate_week, p.active_retention_rate_month,
         p.email_open_rate AS person_email_open_rate,
         CAST(strftime('%w', pcf.first_event_at) AS INTEGER) AS dow,
         CAST(strftime('%H', pcf.first_event_at) AS INTEGER) AS hour,
         CASE WHEN CAST(strftime('%w', pcf.first_event_at) AS INTEGER) IN (0,6) THEN 'weekend' ELSE 'weekday' END AS day_part,
         CASE WHEN CAST(strftime('%H', pcf.first_event_at) AS INTEGER) < 12 THEN 'morning' ELSE 'afternoon' END AS time_half,
         CASE WHEN lower(COALESCE(camp.campaign_subject_line,'')) LIKE '%launch%' THEN 'new_product_launch'
              WHEN lower(COALESCE(camp.campaign_subject_line,'')) LIKE '%offer%' OR lower(COALESCE(camp.campaign_subject_line,'')) LIKE '%sale%' OR lower(COALESCE(camp.campaign_subject_line,'')) LIKE '%discount%' OR lower(COALESCE(camp.campaign_subject_line,'')) LIKE '%deal%' OR lower(COALESCE(camp.campaign_subject_line,'')) LIKE '%save%' THEN 'discount'
              WHEN lower(COALESCE(camp.campaign_subject_line,'')) LIKE '%story%' OR lower(COALESCE(camp.campaign_subject_line,'')) LIKE '%journey%' OR lower(COALESCE(camp.campaign_subject_line,'')) LIKE '%behind%' THEN 'storytelling'
              ELSE 'unknown' END AS theme
  FROM klaviyo__person_campaign_flow pcf
  LEFT JOIN camp ON camp.campaign_id = pcf.last_touch_campaign_id
  JOIN klaviyo__persons p ON p.person_id = pcf.person_id
)
SELECT person_id, campaign_id, campaign_name, campaign_subject_line, send_at,
       open_rate, click_rate, count_received_email, count_opened_email, count_clicked_email,
       net_revenue_touch, active_retention_rate_week, active_retention_rate_month,
       person_email_open_rate, dow, hour, day_part, time_half, theme,
       holiday, hol_diff,
       CASE WHEN hol_diff BETWEEN -3 AND -1 THEN 'pre_holiday'
            WHEN hol_diff BETWEEN 0 AND 3 THEN 'post_holiday'
            ELSE 'neutral' END AS holiday_window
FROM (
  SELECT t2.*,
         h.d AS holiday,
         CAST(julianday(substr(t2.send_at,1,10)) - julianday(h.d) AS INTEGER) AS hol_diff,
         ROW_NUMBER() OVER (PARTITION BY t2.person_id, t2.campaign_id ORDER BY ABS(julianday(substr(t2.send_at,1,10)) - julianday(h.d)), julianday(h.d)) AS rn
  FROM t t2
  CROSS JOIN holidays h
) ranked
WHERE rn = 1
ORDER BY send_at
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-094/attempt-01/sql/S20.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-094/attempt-01/sql/S20.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-094/attempt-01/results/S20.rows.jsonl)；完整：True；SHA256：`5368590a482a6a5aa13cf63e0c7c7f52a96b1541f4bdc683243d2bdf80e0c9b4`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [] | [] | [] |
| B2 | [] | [] | [] |
| B3 | [] | [] | [] |
| B4 | [] | [] | [] |
| B5 | [] | [] | [] |
| B6 | [] | [] | [] |
| B7 | [] | [] | [] |
| B8 | [] | [] | [] |
| B9 | [] | [] | [] |
| B10 | [] | [] | [] |
| B11 | [] | [] | [] |
| B12 | [] | [] | [] |
| B13 | [] | [] | [] |
| B14 | [] | [] | [] |
| B15 | [] | [] | [] |
| B16 | [] | [] | [] |
| B17 | [] | [] | [] |
| B18 | [] | [] | [] |
| B19 | [] | [] | [] |
| B20 | [] | [] | [] |
| B21 | [] | [] | [] |
| B22 | [] | [] | [] |
| B23 | [] | [] | [] |
| B24 | [] | [] | [] |
| B25 | [] | [] | [] |
| B26 | [] | [] | [] |
| B27 | [] | [] | [] |
| B28 | [] | [] | [] |
| B29 | [] | [] | [] |
| B30 | [] | [] | [] |
| B31 | [] | [] | [] |
| B32 | [] | [] | [] |
| B33 | [] | [] | [] |
| B34 | [] | [] | [] |
| B35 | [] | [] | [] |
| B36 | [] | [] | [] |
| B37 | [] | [] | [] |
| B38 | [] | [] | [] |
| B39 | [] | [] | [] |
| B40 | [] | [] | [] |
| B41 | [] | [] | [] |
| B42 | [] | [] | [] |
| B43 | [] | [] | [] |
| B44 | [] | [] | [] |
| B45 | [] | [] | [] |
| B46 | [] | [] | [] |
| B47 | [] | [] | [] |
| B48 | [] | [] | [] |
| B49 | [] | [] | [] |
| B50 | [{"alias": "klaviyo__events", "kind": "base", "block": null, "base_tables": ["klaviyo__events"]}] | [] | [] |
| B51 | [{"alias": "camp", "kind": "derived", "block": "B50", "base_tables": ["klaviyo__events"]}, {"alias": "pcf", "kind": "base", "block": null, "base_tables": ["klaviyo__person_campaign_flow"]}, {"alias": "p", "kind": "base", "block": null, "base_tables": ["klaviyo__persons"]}] | [{"type": "LEFT", "right": "camp", "on": "camp.campaign_id = pcf.last_touch_campaign_id", "using": []}, {"type": "INNER", "right": "klaviyo__persons AS p", "on": "p.person_id = pcf.person_id", "using": []}] | [] |
| B52 | [{"alias": "t2", "kind": "derived", "block": "B51", "base_tables": ["klaviyo__events", "klaviyo__person_campaign_flow", "klaviyo__persons"]}, {"alias": "h", "kind": "derived", "block": "B49", "base_tables": []}] | [{"type": "CROSS", "right": "holidays AS h", "on": null, "using": []}] | [] |
| B53 | [{"alias": "ranked", "kind": "derived", "block": "B52", "base_tables": ["klaviyo__events", "klaviyo__person_campaign_flow", "klaviyo__persons"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |


未解析列血缘：[{"column": "h.d", "reason": "derived_star_or_missing_output"}, {"column": "h.d", "reason": "derived_star_or_missing_output"}, {"column": "h.d", "reason": "derived_star_or_missing_output"}, {"column": "h.d", "reason": "derived_star_or_missing_output"}, {"column": "h.d", "reason": "derived_star_or_missing_output"}, {"column": "h.d", "reason": "derived_star_or_missing_output"}, {"column": "h.d", "reason": "derived_star_or_missing_output"}, {"column": "h.d", "reason": "derived_star_or_missing_output"}, {"column": "h.d", "reason": "derived_star_or_missing_output"}, {"column": "h.d", "reason": "derived_star_or_missing_output"}, {"column": "h.d", "reason": "derived_star_or_missing_output"}, {"column": "h.d", "reason": "derived_star_or_missing_output"}, {"column": "h.d", "reason": "derived_star_or_missing_output"}, {"column": "h.d", "reason": "derived_star_or_missing_output"}, {"column": "h.d", "reason": "derived_star_or_missing_output"}, {"column": "h.d", "reason": "derived_star_or_missing_output"}]

## S21

类别 `data`；来源 `query_db`；调用 `f034bff213b94d049f675a3a8d2ad6a9`；状态 `success`。

```sql
SELECT 
  COUNT(*) AS n_persons,
  AVG(active_retention_rate_week) AS avg_ret_week,
  AVG(active_retention_rate_month) AS avg_ret_month,
  AVG(email_open_rate) AS avg_email_open,
  MIN(active_retention_rate_week) AS min_ret_week,
  MAX(active_retention_rate_week) AS max_ret_week,
  MIN(active_retention_rate_month) AS min_ret_month,
  MAX(active_retention_rate_month) AS max_ret_month
FROM klaviyo__persons
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-094/attempt-01/sql/S21.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-094/attempt-01/sql/S21.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-094/attempt-01/results/S21.rows.jsonl)；完整：True；SHA256：`abc1bcd147b01bdc16aa90c9606847dc470235bd7f1d97290a33d3e927930df0`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "klaviyo__persons", "kind": "base", "block": null, "base_tables": ["klaviyo__persons"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |
| B1 | AVG(active_retention_rate_week) | [{"table": "klaviyo__persons", "column": "active_retention_rate_week"}] | [] | False |
| B1 | AVG(active_retention_rate_month) | [{"table": "klaviyo__persons", "column": "active_retention_rate_month"}] | [] | False |
| B1 | AVG(email_open_rate) | [{"table": "klaviyo__persons", "column": "email_open_rate"}] | [] | False |
| B1 | MIN(active_retention_rate_week) | [{"table": "klaviyo__persons", "column": "active_retention_rate_week"}] | [] | False |
| B1 | MAX(active_retention_rate_week) | [{"table": "klaviyo__persons", "column": "active_retention_rate_week"}] | [] | False |
| B1 | MIN(active_retention_rate_month) | [{"table": "klaviyo__persons", "column": "active_retention_rate_month"}] | [] | False |
| B1 | MAX(active_retention_rate_month) | [{"table": "klaviyo__persons", "column": "active_retention_rate_month"}] | [] | False |


## S22

类别 `data`；来源 `query_db`；调用 `5e7ef771d3fe4fd9aa90b38c9e096bd1`；状态 `success`。

```sql
SELECT campaign_name, campaign_subject_line, COUNT(*) AS n_events_by_campaign
FROM klaviyo__events 
GROUP BY campaign_name, campaign_subject_line
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-094/attempt-01/sql/S22.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-094/attempt-01/sql/S22.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-094/attempt-01/results/S22.rows.jsonl)；完整：True；SHA256：`8c3c06466e60a7009176477a0ceb02dea6818cdece28fa84541d0f3f0b82ea4d`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "klaviyo__events", "kind": "base", "block": null, "base_tables": ["klaviyo__events"]}] | [] | ["campaign_name", "campaign_subject_line"] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |

