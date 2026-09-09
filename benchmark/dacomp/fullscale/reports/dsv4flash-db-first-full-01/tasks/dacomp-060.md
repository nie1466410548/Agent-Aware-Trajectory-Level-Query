# dacomp-060

It has been observed that some ad groups exhibit a high Click-Through Rate (CTR) but a low…

运行：已提交。官方未评分。全部 SQL 尝试/成功 22/22；数据 SQL 20/20；Python 13 次。

完整原题：

It has been observed that some ad groups exhibit a high Click-Through Rate (CTR) but a low Conversion Rate (CVR), suggesting a potential mismatch between user intent and ad content. Using the `google_ads__ad_group_report` table and related conversion data, identify problematic ad groups based on the criteria of CTR > 75th percentile and CVR < 25th percentile. Analyze the common characteristics of these high-CTR, low-CVR ad groups, with a focus on assessing the Intent Match Ratio (Actual CVR / Expected CVR) and traffic quality. Finally, propose targeted optimization recommendations, including improvements for keyword strategy, audience targeting, and landing page experience.

| 表 | 行数 | 列数 |
| --- | --- | --- |
| google_ads__ad_group_report | 10000 | 17 |
| google_ads__ad_report | 10000 | 20 |
| google_ads__campaign_report | 9976 | 16 |
| google_ads__keyword_report | 10000 | 20 |
| google_ads__search_term_report | 10000 | 20 |
| google_ads__url_report | 2 | 24 |


实际路线（分析者依据 SQL/源码概括，不代表 Agent 自述）：SQL 提取高 CTR 低 CVR 广告组及相关明细 → Python 连接、意图匹配计算和关键词分组 → 流量质量诊断。

数据库大小：12,931,072 字节。

## 数据 SQL

| SQL | 状态 | 基础表 | Join 输入/类型 | GROUP BY | 聚合表达式 | 结果行数 | 数据库 ms |
| --- | --- | --- | --- | --- | --- | --- | --- |
| [S3/Q1](#s3) | success | ["google_ads__ad_group_report"] | 0 / {} | [] | ["COUNT(*)", "COUNT(DISTINCT ad_group_id)", "MIN(date_day)", "MAX(date_day)", "SUM(spend)", "SUM(clicks)", "SUM(impressions)", "SUM(conversions)"] | 1 | 10.399 |
| [S4/Q2](#s4) | success | ["google_ads__keyword_report"] | 0 / {} | [] | ["COUNT(*)", "COUNT(DISTINCT ad_group_id)", "COUNT(DISTINCT keyword_text)"] | 1 | 13.338 |
| [S5/Q3](#s5) | success | ["google_ads__search_term_report"] | 0 / {} | [] | ["COUNT(*)", "COUNT(DISTINCT search_term)", "COUNT(DISTINCT ad_group_id)"] | 1 | 8.095 |
| [S6/Q4](#s6) | success | ["google_ads__ad_group_report"] | 0 / {} | ["ad_group_id"] | ["COUNT(*)"] | 10 | 5.722 |
| [S7/Q5](#s7) | success | ["google_ads__ad_group_report"] | 0 / {} | [] | ["COUNT(DISTINCT date_day)"] | 1 | 5.236 |
| [S8/Q6](#s8) | success | ["google_ads__ad_group_report"] | 0 / {} | ["status", "ad_group_type"] | ["COUNT(DISTINCT ad_group_id)"] | 3 | 10.563 |
| [S9/Q7](#s9) | success | ["google_ads__ad_group_report"] | 0 / {} | ["ad_group_id"] | ["SUM(impressions)", "SUM(clicks)", "SUM(spend)", "SUM(conversions)", "SUM(conversions_value)", "SUM(view_through_conversions)", "COUNT(*)", "SUM(CASE WHEN impressions > 0 AND clicks > 0 THEN 1 ELSE 0 END)", "SUM(CASE WHEN impressions > 0 THEN 1 ELSE 0 END)", "SUM(CASE WHEN clicks > 0 THEN 1 ELSE 0 END)", "SUM(CASE WHEN conversions > 0 THEN 1 ELSE 0 END)"] | 1 | 19.012 |
| [S10/Q8](#s10) | success | ["google_ads__ad_group_report"] | 0 / {} | ["ad_group_id"] | ["SUM(impressions)", "SUM(clicks)", "SUM(conversions)", "MIN(clicks)", "MAX(clicks)", "MIN(impressions)", "MAX(impressions)", "MIN(conversions)", "MAX(conversions)"] | 1 | 9.987 |
| [S11/Q9](#s11) | success | ["google_ads__ad_group_report"] | 0 / {} | ["ad_group_id"] | ["SUM(impressions)", "SUM(clicks)", "SUM(spend)", "SUM(conversions)", "SUM(conversions_value)", "SUM(view_through_conversions)"] | 4324 | 40.314 |
| [S12/Q10](#s12) | success | ["google_ads__ad_group_report"] | 0 / {} | ["campaign_id"] | ["SUM(impressions)", "SUM(clicks)", "SUM(spend)", "SUM(conversions)", "SUM(clicks)", "SUM(conversions)"] | 1000 | 11.84 |
| [S13/Q11](#s13) | success | ["google_ads__campaign_report"] | 0 / {} | [] | [] | 1000 | 9.635 |
| [S14/Q12](#s14) | success | ["google_ads__ad_group_report"] | 0 / {} | [] | ["COUNT(DISTINCT campaign_id)"] | 1 | 7.727 |
| [S15/Q13](#s15) | success | ["google_ads__campaign_report"] | 0 / {} | [] | ["COUNT(DISTINCT campaign_id)", "COUNT(*)"] | 1 | 5.008 |
| [S16/Q14](#s16) | success | ["google_ads__ad_group_report"] | 0 / {} | ["ad_group_id"] | ["SUM(impressions)", "SUM(clicks)", "SUM(spend)", "SUM(conversions)", "SUM(conversions_value)", "SUM(view_through_conversions)", "SUM(impressions)", "SUM(clicks)", "SUM(clicks)", "SUM(conversions)"] | 4324 | 36.853 |
| [S17/Q15](#s17) | success | ["google_ads__campaign_report"] | 0 / {} | ["campaign_id"] | ["SUM(impressions)", "SUM(clicks)", "SUM(spend)", "SUM(conversions)", "SUM(clicks)", "SUM(conversions)"] | 1000 | 13.633 |
| [S18/Q16](#s18) | success | ["google_ads__ad_group_report", "google_ads__keyword_report"] | 2 / {'INNER': 1} | ["ad_group_id", "k.ad_group_id", "k.keyword_text", "k.keyword_match_type"] | ["SUM(impressions)", "SUM(clicks)", "SUM(clicks)", "SUM(conversions)", "SUM(k.impressions)", "SUM(k.clicks)", "SUM(k.spend)", "SUM(k.conversions)"] | 547 | 25.105 |
| [S19/Q17](#s19) | success | ["google_ads__ad_group_report", "google_ads__search_term_report"] | 2 / {'INNER': 1} | ["ad_group_id", "s.ad_group_id", "s.search_term", "s.keyword_text", "s.keyword_match_type", "s.search_term_match_type"] | ["SUM(impressions)", "SUM(clicks)", "SUM(clicks)", "SUM(conversions)", "SUM(s.impressions)", "SUM(s.clicks)", "SUM(s.spend)", "SUM(s.conversions)"] | 532 | 18.03 |
| [S20/Q18](#s20) | success | ["google_ads__ad_group_report", "google_ads__url_report"] | 2 / {'INNER': 1} | ["ad_group_id", "u.ad_group_id", "u.base_url", "u.url_host", "u.url_path"] | ["SUM(impressions)", "SUM(clicks)", "SUM(clicks)", "SUM(conversions)", "SUM(u.impressions)", "SUM(u.clicks)", "SUM(u.spend)", "SUM(u.conversions)"] | 0 | 10.509 |
| [S21/Q19](#s21) | success | ["google_ads__keyword_report"] | 0 / {} | ["k.ad_group_id", "k.keyword_match_type", "k.type", "k.status"] | ["SUM(k.impressions)", "SUM(k.clicks)", "SUM(k.spend)", "SUM(k.conversions)"] | 9177 | 37.058 |
| [S22/Q20](#s22) | success | ["google_ads__search_term_report"] | 0 / {} | ["s.ad_group_id", "s.search_term", "s.keyword_match_type", "s.search_term_match_type"] | ["SUM(s.impressions)", "SUM(s.clicks)", "SUM(s.spend)", "SUM(s.conversions)"] | 9960 | 40.079 |


## 元数据和设置

| SQL | 类别 | 状态 | 内容 |
| --- | --- | --- | --- |
| S1 | connection_setup | success | PRAGMA query_only=ON |
| S2 | metadata | success | SELECT name,sql FROM sqlite_master WHERE type='table' ORDER BY name |


## Python 与执行位置

人工源码审查：**database_first_violation**。Python 多次连接广告组与活动数据，并对关键词、搜索词、匹配类型和渠道执行分组求和、计数、比例及 Top-K。常规均值和阈值比例也在 Python 重算；这些均可在 SQL 内执行。分位数及图表单独评价。 [证据](../reviews/dacomp-060.json)。

P1：Compute percentile thresholds (p75 of CTR, p25 of CVR) across ad groups using numpy percentile, then identify problematic ad groups. This is done in Python because SQLite lacks built-in percentile interpolation functions.

[源码](../../../runs/dsv4flash-db-first-full-01/dacomp-060/attempt-01/python/P1.py)；[输出](../../../runs/dsv4flash-db-first-full-01/dacomp-060/attempt-01/python/P1.stdout)；[错误](../../../runs/dsv4flash-db-first-full-01/dacomp-060/attempt-01/python/P1.stderr)。自动源码筛查未检出预设迁出信号；这不是全面语义合规证明。

P2：Compute percentile thresholds for CTR/CVR and flag problematic ad groups in Python because SQLite lacks percentile interpolation functions.

[源码](../../../runs/dsv4flash-db-first-full-01/dacomp-060/attempt-01/python/P2.py)；[输出](../../../runs/dsv4flash-db-first-full-01/dacomp-060/attempt-01/python/P2.stdout)；[错误](../../../runs/dsv4flash-db-first-full-01/dacomp-060/attempt-01/python/P2.stderr)。自动源码筛查未检出预设迁出信号；这不是全面语义合规证明。

P3：Inspect structure of archived JSONL rows to correctly load into a DataFrame.

[源码](../../../runs/dsv4flash-db-first-full-01/dacomp-060/attempt-01/python/P3.py)；[输出](../../../runs/dsv4flash-db-first-full-01/dacomp-060/attempt-01/python/P3.stdout)；[错误](../../../runs/dsv4flash-db-first-full-01/dacomp-060/attempt-01/python/P3.stderr)。自动源码筛查未检出预设迁出信号；这不是全面语义合规证明。

P4：Compute percentile thresholds and identify problematic ad groups (CTR>p75, CVR<p25). Using Python because SQLite lacks percentile interpolation.

[源码](../../../runs/dsv4flash-db-first-full-01/dacomp-060/attempt-01/python/P4.py)；[输出](../../../runs/dsv4flash-db-first-full-01/dacomp-060/attempt-01/python/P4.stdout)；[错误](../../../runs/dsv4flash-db-first-full-01/dacomp-060/attempt-01/python/P4.stderr)。自动源码筛查未检出预设迁出信号；这不是全面语义合规证明。

P5：Load per-ad-group and campaign aggregates to compute Intent Match Ratio. Need campaign_id to join, so will add via SQL.

[源码](../../../runs/dsv4flash-db-first-full-01/dacomp-060/attempt-01/python/P5.py)；[输出](../../../runs/dsv4flash-db-first-full-01/dacomp-060/attempt-01/python/P5.stdout)；[错误](../../../runs/dsv4flash-db-first-full-01/dacomp-060/attempt-01/python/P5.stderr)。自动源码筛查未检出预设迁出信号；这不是全面语义合规证明。

P6：Compute Intent Match Ratio and analyze channel/status/cost patterns. Python needed for percentile calculations, ratio computations, and comparative statistics not easily done in SQLite.

[源码](../../../runs/dsv4flash-db-first-full-01/dacomp-060/attempt-01/python/P6.py)；[输出](../../../runs/dsv4flash-db-first-full-01/dacomp-060/attempt-01/python/P6.stdout)；[错误](../../../runs/dsv4flash-db-first-full-01/dacomp-060/attempt-01/python/P6.stderr)。检出需人工核验的 SQL 可实现操作：.merge(；不能仅凭理由判为合规。

P7：Analyze keyword match type and keyword text patterns in problematic vs non-problematic ad groups; Python for comparative aggregation and pattern review.

[源码](../../../runs/dsv4flash-db-first-full-01/dacomp-060/attempt-01/python/P7.py)；[输出](../../../runs/dsv4flash-db-first-full-01/dacomp-060/attempt-01/python/P7.stdout)；[错误](../../../runs/dsv4flash-db-first-full-01/dacomp-060/attempt-01/python/P7.stderr)。检出需人工核验的 SQL 可实现操作：groupby(, sort_values(；不能仅凭理由判为合规。

P8：Analyze search term query patterns to understand traffic quality difference between problematic and non-problematic ad groups. Python needed for aggregation by match type and search term text.

[源码](../../../runs/dsv4flash-db-first-full-01/dacomp-060/attempt-01/python/P8.py)；[输出](../../../runs/dsv4flash-db-first-full-01/dacomp-060/attempt-01/python/P8.stdout)；[错误](../../../runs/dsv4flash-db-first-full-01/dacomp-060/attempt-01/python/P8.stderr)。检出需人工核验的 SQL 可实现操作：groupby(, sort_values(；不能仅凭理由判为合规。

P9：Parse campaign name structure and compute traffic-quality metrics (CPC, CPM, ROAS, conversion value) and Intent Match Ratio distributions. Python for string parsing and comparative statistics beyond SQL.

[源码](../../../runs/dsv4flash-db-first-full-01/dacomp-060/attempt-01/python/P9.py)；[输出](../../../runs/dsv4flash-db-first-full-01/dacomp-060/attempt-01/python/P9.stdout)；[错误](../../../runs/dsv4flash-db-first-full-01/dacomp-060/attempt-01/python/P9.stderr)。检出需人工核验的 SQL 可实现操作：groupby(, .merge(, sort_values(；不能仅凭理由判为合规。

P10：Compute Intent Match Ratio distributions, visualize CTR vs CVR scatter and IMR histograms, and analyze campaign patterns. Python for visualization and statistical analysis.

[源码](../../../runs/dsv4flash-db-first-full-01/dacomp-060/attempt-01/python/P10.py)；[输出](../../../runs/dsv4flash-db-first-full-01/dacomp-060/attempt-01/python/P10.stdout)；[错误](../../../runs/dsv4flash-db-first-full-01/dacomp-060/attempt-01/python/P10.stderr)。检出需人工核验的 SQL 可实现操作：.merge(；不能仅凭理由判为合规。

P11：Complete the traffic quality, IMR distribution, and visualization analysis. Python needed for plotting, comprehensive statistics, and campaign name parsing.

[源码](../../../runs/dsv4flash-db-first-full-01/dacomp-060/attempt-01/python/P11.py)；[输出](../../../runs/dsv4flash-db-first-full-01/dacomp-060/attempt-01/python/P11.stdout)；[错误](../../../runs/dsv4flash-db-first-full-01/dacomp-060/attempt-01/python/P11.stderr)。检出需人工核验的 SQL 可实现操作：.merge(, sort_values(；不能仅凭理由判为合规。

P12：Analyze account-level patterns, advertising channel subtypes, and low-intent keyword patterns. Python for text analysis and multi-dimensional grouping.

[源码](../../../runs/dsv4flash-db-first-full-01/dacomp-060/attempt-01/python/P12.py)；[输出](../../../runs/dsv4flash-db-first-full-01/dacomp-060/attempt-01/python/P12.stdout)；[错误](../../../runs/dsv4flash-db-first-full-01/dacomp-060/attempt-01/python/P12.stderr)。检出需人工核验的 SQL 可实现操作：groupby(, .merge(, sort_values(；不能仅凭理由判为合规。

P13：Compute final summary statistics for the report, including total spend impact, per-channel IMR, and zero-conversion rates.

[源码](../../../runs/dsv4flash-db-first-full-01/dacomp-060/attempt-01/python/P13.py)；[输出](../../../runs/dsv4flash-db-first-full-01/dacomp-060/attempt-01/python/P13.stdout)；[错误](../../../runs/dsv4flash-db-first-full-01/dacomp-060/attempt-01/python/P13.stderr)。检出需人工核验的 SQL 可实现操作：.merge(；不能仅凭理由判为合规。

## 优化机会

已验证候选。筛选限于精确 SQL、相同自包含 CTE、相同单表完整过滤、可分解单表聚合；未覆盖任意 Join 等价和一般谓词蕴含。全部候选都是 offline，未测在线预测。

| 候选 | 类型 | 已有结果 | 覆盖 SQL | 后续次数 | 中间行数 | 验证 | 成本 |
| --- | --- | --- | --- | --- | --- | --- | --- |
| C1 | common subexpression | False | ["S9", "S11"] | 1 | 4324 | verified | Not benchmarked; correctness alone does not establish net speedup. |


已验证覆盖（含触发查询、候选并集去重）：2/20 条成功数据 SQL。正确性仅针对当前数据库快照；未测性能的候选不能声称已加速。

[完整 build/rewrite 与比较证据](dacomp-060.analysis.json)。

### C1：common subexpression

Identical self-contained CTE body across queries.

原查询 [S9](#s9), [S11](#s11) → 新增共享状态 C1 → 后续 1 次可复用。该构建点为事后假设，不代表 Agent 当时预知后续。

构建定义：

```sql
SELECT ad_group_id, ad_group_name, campaign_id, campaign_name, account_id, account_name, status, SUM(impressions) AS impressions, SUM(clicks) AS clicks, SUM(spend) AS spend, SUM(conversions) AS conversions, SUM(conversions_value) AS conv_value, SUM(view_through_conversions) AS vtc FROM google_ads__ad_group_report GROUP BY ad_group_id
```

受益查询 S9 的改写示例：

```sql
WITH ag AS (SELECT * FROM temp.reuse_candidate) SELECT COUNT(*) AS n_ag, SUM(CASE WHEN impressions > 0 AND clicks > 0 THEN 1 ELSE 0 END) AS n_usable, SUM(CASE WHEN impressions > 0 THEN 1 ELSE 0 END) AS n_impr, SUM(CASE WHEN clicks > 0 THEN 1 ELSE 0 END) AS n_clicks, SUM(CASE WHEN conversions > 0 THEN 1 ELSE 0 END) AS n_conv FROM ag
```

| 原 SQL | 列名一致 | 结果一致 | 比较方法 |
| --- | --- | --- | --- |
| S9 | True | True | exact_multiset |
| S11 | True | True | ordered_numeric_tolerance |


验证状态：verified；成本结论：Not benchmarked; correctness alone does not establish net speedup.

结果依赖：自动记录 SQL→Python 的接口父调用，以及源码中引用归档文件的消费者；字面值相同不认定因果。模型方向选择需要人工读取消息，尚未做全面因果标注。

[原始报告](../../../runs/dsv4flash-db-first-full-01/dacomp-060/attempt-01/answer.md)；[统一消息](../../../runs/dsv4flash-db-first-full-01/dacomp-060/attempt-01/messages.jsonl)；[原始 OpenCode 事件](../../../runs/dsv4flash-db-first-full-01/dacomp-060/attempt-01/opencode.jsonl)；[SQL 引擎日志](../../../runs/dsv4flash-db-first-full-01/dacomp-060/attempt-01/sql_journal.jsonl)。

[可读报告（本地图片链接规范化）](../answers/dacomp-060.md)。原始回答保留，分析结论未改写。

## S1

类别 `connection_setup`；来源 `connection`；调用 `94b6f246facf43d99fc47fb570f6c354`；状态 `success`。

```sql
PRAGMA query_only=ON
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-060/attempt-01/sql/S1.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-060/attempt-01/sql/S1.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-060/attempt-01/results/S1.rows.jsonl)；完整：True；SHA256：`e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`。

## S2

类别 `metadata`；来源 `list_db`；调用 `94b6f246facf43d99fc47fb570f6c354`；状态 `success`。

```sql
SELECT name,sql FROM sqlite_master WHERE type='table' ORDER BY name
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-060/attempt-01/sql/S2.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-060/attempt-01/sql/S2.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-060/attempt-01/results/S2.rows.jsonl)；完整：True；SHA256：`db989d5650aab70f7fcd857d6317cad6f3ca9c904780466f761f89d49dae3101`。

## S3

类别 `data`；来源 `query_db`；调用 `e70f7beba84e4b789bd51d16c3bf2ea7`；状态 `success`。

```sql
SELECT COUNT(*) AS n_rows, COUNT(DISTINCT ad_group_id) AS n_adgroups, MIN(date_day) AS min_date, MAX(date_day) AS max_date, SUM(spend) AS total_spend, SUM(clicks) AS total_clicks, SUM(impressions) AS total_impr, SUM(conversions) AS total_conv FROM google_ads__ad_group_report
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-060/attempt-01/sql/S3.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-060/attempt-01/sql/S3.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-060/attempt-01/results/S3.rows.jsonl)；完整：True；SHA256：`3f13dc9603600adc6b0e09850900630c8d41dcce0f463d215709860fe3988b2c`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "google_ads__ad_group_report", "kind": "base", "block": null, "base_tables": ["google_ads__ad_group_report"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |
| B1 | COUNT(DISTINCT ad_group_id) | [{"table": "google_ads__ad_group_report", "column": "ad_group_id"}] | [] | False |
| B1 | MIN(date_day) | [{"table": "google_ads__ad_group_report", "column": "date_day"}] | [] | False |
| B1 | MAX(date_day) | [{"table": "google_ads__ad_group_report", "column": "date_day"}] | [] | False |
| B1 | SUM(spend) | [{"table": "google_ads__ad_group_report", "column": "spend"}] | [] | False |
| B1 | SUM(clicks) | [{"table": "google_ads__ad_group_report", "column": "clicks"}] | [] | False |
| B1 | SUM(impressions) | [{"table": "google_ads__ad_group_report", "column": "impressions"}] | [] | False |
| B1 | SUM(conversions) | [{"table": "google_ads__ad_group_report", "column": "conversions"}] | [] | False |


## S4

类别 `data`；来源 `query_db`；调用 `86a2997b1b7f43d39f7e4b1831b44296`；状态 `success`。

```sql
SELECT COUNT(*) AS n_rows, COUNT(DISTINCT ad_group_id) AS n_adgroups, COUNT(DISTINCT keyword_text) AS n_keywords FROM google_ads__keyword_report
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-060/attempt-01/sql/S4.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-060/attempt-01/sql/S4.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-060/attempt-01/results/S4.rows.jsonl)；完整：True；SHA256：`b25e29e02acd1afecb3a1600d571df69a2adbbaf3d54bca41c619de35e31e863`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "google_ads__keyword_report", "kind": "base", "block": null, "base_tables": ["google_ads__keyword_report"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |
| B1 | COUNT(DISTINCT ad_group_id) | [{"table": "google_ads__keyword_report", "column": "ad_group_id"}] | [] | False |
| B1 | COUNT(DISTINCT keyword_text) | [{"table": "google_ads__keyword_report", "column": "keyword_text"}] | [] | False |


## S5

类别 `data`；来源 `query_db`；调用 `8c8aafc480c04bf99ba1b99c83b56b6f`；状态 `success`。

```sql
SELECT COUNT(*) AS n_rows, COUNT(DISTINCT search_term) AS n_search_terms, COUNT(DISTINCT ad_group_id) AS n_adgroups FROM google_ads__search_term_report
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-060/attempt-01/sql/S5.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-060/attempt-01/sql/S5.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-060/attempt-01/results/S5.rows.jsonl)；完整：True；SHA256：`5652452ae0e6cdf4be9f7933afee45420f7565e9ca94c17aa98535583f2631eb`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "google_ads__search_term_report", "kind": "base", "block": null, "base_tables": ["google_ads__search_term_report"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |
| B1 | COUNT(DISTINCT search_term) | [{"table": "google_ads__search_term_report", "column": "search_term"}] | [] | False |
| B1 | COUNT(DISTINCT ad_group_id) | [{"table": "google_ads__search_term_report", "column": "ad_group_id"}] | [] | False |


## S6

类别 `data`；来源 `query_db`；调用 `3f904ad0177745b19f2dfb72e0cb4e38`；状态 `success`。

```sql
SELECT COUNT(*) AS rows_per_ag FROM google_ads__ad_group_report GROUP BY ad_group_id ORDER BY rows_per_ag DESC LIMIT 10
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-060/attempt-01/sql/S6.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-060/attempt-01/sql/S6.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-060/attempt-01/results/S6.rows.jsonl)；完整：True；SHA256：`fec64f4c000854de2d2884d51f8efc44dedcf17abde509910b2cce2c99fbf2ee`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "google_ads__ad_group_report", "kind": "base", "block": null, "base_tables": ["google_ads__ad_group_report"]}] | [] | ["ad_group_id"] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |


## S7

类别 `data`；来源 `query_db`；调用 `53acb4102ddc4a849645cf3dda463338`；状态 `success`。

```sql
SELECT COUNT(DISTINCT date_day) AS n_dates FROM google_ads__ad_group_report
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-060/attempt-01/sql/S7.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-060/attempt-01/sql/S7.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-060/attempt-01/results/S7.rows.jsonl)；完整：True；SHA256：`8d6e3ccaa2960b20f2687b415123e38a65e1093e8169209ed747a6486519f6a2`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "google_ads__ad_group_report", "kind": "base", "block": null, "base_tables": ["google_ads__ad_group_report"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(DISTINCT date_day) | [{"table": "google_ads__ad_group_report", "column": "date_day"}] | [] | False |


## S8

类别 `data`；来源 `query_db`；调用 `f5bb67191ad04614aab3ee9bd5f7ceeb`；状态 `success`。

```sql
SELECT status, ad_group_type, COUNT(DISTINCT ad_group_id) AS n FROM google_ads__ad_group_report GROUP BY status, ad_group_type ORDER BY n DESC LIMIT 20
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-060/attempt-01/sql/S8.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-060/attempt-01/sql/S8.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-060/attempt-01/results/S8.rows.jsonl)；完整：True；SHA256：`aa3b71c68ad51edbc98bb1a9ff3df77ace49264cd3ce916f5e82a5386d240b4f`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "google_ads__ad_group_report", "kind": "base", "block": null, "base_tables": ["google_ads__ad_group_report"]}] | [] | ["status", "ad_group_type"] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(DISTINCT ad_group_id) | [{"table": "google_ads__ad_group_report", "column": "ad_group_id"}] | [] | False |


## S9

类别 `data`；来源 `query_db`；调用 `efaef08b81224de6adbc4dedb63ecb12`；状态 `success`。

```sql
WITH ag AS (
  SELECT ad_group_id, ad_group_name, campaign_id, campaign_name, account_id, account_name, status,
         SUM(impressions) AS impressions, SUM(clicks) AS clicks, SUM(spend) AS spend,
         SUM(conversions) AS conversions, SUM(conversions_value) AS conv_value, SUM(view_through_conversions) AS vtc
  FROM google_ads__ad_group_report
  GROUP BY ad_group_id
)
SELECT 
  COUNT(*) AS n_ag,
  SUM(CASE WHEN impressions>0 AND clicks>0 THEN 1 ELSE 0 END) AS n_usable,
  SUM(CASE WHEN impressions>0 THEN 1 ELSE 0 END) AS n_impr,
  SUM(CASE WHEN clicks>0 THEN 1 ELSE 0 END) AS n_clicks,
  SUM(CASE WHEN conversions>0 THEN 1 ELSE 0 END) AS n_conv
FROM ag
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-060/attempt-01/sql/S9.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-060/attempt-01/sql/S9.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-060/attempt-01/results/S9.rows.jsonl)；完整：True；SHA256：`1b867e9f05c2376a0cf1b514255548c675b168296094d3d1daab079ddcaac01e`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "google_ads__ad_group_report", "kind": "base", "block": null, "base_tables": ["google_ads__ad_group_report"]}] | [] | ["ad_group_id"] |
| B2 | [{"alias": "ag", "kind": "derived", "block": "B1", "base_tables": ["google_ads__ad_group_report"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | SUM(impressions) | [{"table": "google_ads__ad_group_report", "column": "impressions"}] | [] | False |
| B1 | SUM(clicks) | [{"table": "google_ads__ad_group_report", "column": "clicks"}] | [] | False |
| B1 | SUM(spend) | [{"table": "google_ads__ad_group_report", "column": "spend"}] | [] | False |
| B1 | SUM(conversions) | [{"table": "google_ads__ad_group_report", "column": "conversions"}] | [] | False |
| B1 | SUM(conversions_value) | [{"table": "google_ads__ad_group_report", "column": "conversions_value"}] | [] | False |
| B1 | SUM(view_through_conversions) | [{"table": "google_ads__ad_group_report", "column": "view_through_conversions"}] | [] | False |
| B2 | COUNT(*) | [] | [] | True |
| B2 | SUM(CASE WHEN impressions > 0 AND clicks > 0 THEN 1 ELSE 0 END) | [] | [{"table": "google_ads__ad_group_report", "column": "impressions"}, {"table": "google_ads__ad_group_report", "column": "clicks"}] | False |
| B2 | SUM(CASE WHEN impressions > 0 THEN 1 ELSE 0 END) | [] | [{"table": "google_ads__ad_group_report", "column": "impressions"}] | False |
| B2 | SUM(CASE WHEN clicks > 0 THEN 1 ELSE 0 END) | [] | [{"table": "google_ads__ad_group_report", "column": "clicks"}] | False |
| B2 | SUM(CASE WHEN conversions > 0 THEN 1 ELSE 0 END) | [] | [{"table": "google_ads__ad_group_report", "column": "conversions"}] | False |


## S10

类别 `data`；来源 `query_db`；调用 `dd258a635e714b7894d99813be224f60`；状态 `success`。

```sql
WITH ag AS (
  SELECT ad_group_id, SUM(impressions) AS impressions, SUM(clicks) AS clicks, SUM(conversions) AS conversions
  FROM google_ads__ad_group_report GROUP BY ad_group_id
)
SELECT 
  MIN(clicks) AS min_clicks, MAX(clicks) AS max_clicks,
  MIN(impressions) AS min_impr, MAX(impressions) AS max_impr,
  MIN(conversions) AS min_conv, MAX(conversions) AS max_conv
FROM ag
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-060/attempt-01/sql/S10.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-060/attempt-01/sql/S10.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-060/attempt-01/results/S10.rows.jsonl)；完整：True；SHA256：`e6cb09475e7c154ddce05713f7ef53d2329527b31dc70032e66aba55e55a9128`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "google_ads__ad_group_report", "kind": "base", "block": null, "base_tables": ["google_ads__ad_group_report"]}] | [] | ["ad_group_id"] |
| B2 | [{"alias": "ag", "kind": "derived", "block": "B1", "base_tables": ["google_ads__ad_group_report"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | SUM(impressions) | [{"table": "google_ads__ad_group_report", "column": "impressions"}] | [] | False |
| B1 | SUM(clicks) | [{"table": "google_ads__ad_group_report", "column": "clicks"}] | [] | False |
| B1 | SUM(conversions) | [{"table": "google_ads__ad_group_report", "column": "conversions"}] | [] | False |
| B2 | MIN(clicks) | [{"table": "google_ads__ad_group_report", "column": "clicks"}] | [] | False |
| B2 | MAX(clicks) | [{"table": "google_ads__ad_group_report", "column": "clicks"}] | [] | False |
| B2 | MIN(impressions) | [{"table": "google_ads__ad_group_report", "column": "impressions"}] | [] | False |
| B2 | MAX(impressions) | [{"table": "google_ads__ad_group_report", "column": "impressions"}] | [] | False |
| B2 | MIN(conversions) | [{"table": "google_ads__ad_group_report", "column": "conversions"}] | [] | False |
| B2 | MAX(conversions) | [{"table": "google_ads__ad_group_report", "column": "conversions"}] | [] | False |


## S11

类别 `data`；来源 `query_db`；调用 `95ae4fd540f3447dafbe2cca23531e19`；状态 `success`。

```sql
WITH ag AS (
  SELECT ad_group_id, ad_group_name, campaign_id, campaign_name, account_id, account_name, status,
         SUM(impressions) AS impressions, SUM(clicks) AS clicks, SUM(spend) AS spend,
         SUM(conversions) AS conversions, SUM(conversions_value) AS conv_value, SUM(view_through_conversions) AS vtc
  FROM google_ads__ad_group_report
  GROUP BY ad_group_id
)
SELECT ad_group_id, ad_group_name, campaign_name, account_name, status,
       impressions, clicks, spend, conversions, conv_value, vtc,
       ROUND(CAST(clicks AS REAL) / impressions, 6) AS ctr,
       ROUND(CAST(conversions AS REAL) / clicks, 6) AS cvr
FROM ag
ORDER BY ad_group_id
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-060/attempt-01/sql/S11.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-060/attempt-01/sql/S11.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-060/attempt-01/results/S11.rows.jsonl)；完整：True；SHA256：`0e3c59b3fabdd35509c0a347d1447d8cca7642ce81928eb8af44991ee27bc9b9`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "google_ads__ad_group_report", "kind": "base", "block": null, "base_tables": ["google_ads__ad_group_report"]}] | [] | ["ad_group_id"] |
| B2 | [{"alias": "ag", "kind": "derived", "block": "B1", "base_tables": ["google_ads__ad_group_report"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | SUM(impressions) | [{"table": "google_ads__ad_group_report", "column": "impressions"}] | [] | False |
| B1 | SUM(clicks) | [{"table": "google_ads__ad_group_report", "column": "clicks"}] | [] | False |
| B1 | SUM(spend) | [{"table": "google_ads__ad_group_report", "column": "spend"}] | [] | False |
| B1 | SUM(conversions) | [{"table": "google_ads__ad_group_report", "column": "conversions"}] | [] | False |
| B1 | SUM(conversions_value) | [{"table": "google_ads__ad_group_report", "column": "conversions_value"}] | [] | False |
| B1 | SUM(view_through_conversions) | [{"table": "google_ads__ad_group_report", "column": "view_through_conversions"}] | [] | False |


## S12

类别 `data`；来源 `query_db`；调用 `199be95482c849b0b2cd283eea496b24`；状态 `success`。

```sql
-- Get campaign-level aggregates for expected CVR (per campaign)
SELECT campaign_id, campaign_name, account_name,
       SUM(impressions) AS campaign_impressions,
       SUM(clicks) AS campaign_clicks,
       SUM(spend) AS campaign_spend,
       SUM(conversions) AS campaign_conversions,
       ROUND(CAST(SUM(conversions) AS REAL) / SUM(clicks), 6) AS campaign_cvr
FROM google_ads__ad_group_report
GROUP BY campaign_id
ORDER BY campaign_id
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-060/attempt-01/sql/S12.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-060/attempt-01/sql/S12.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-060/attempt-01/results/S12.rows.jsonl)；完整：True；SHA256：`a52e1830eebc9e93685cc2741a4e22d19c95d41bf97dfdb31352dec0def79945`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "google_ads__ad_group_report", "kind": "base", "block": null, "base_tables": ["google_ads__ad_group_report"]}] | [] | ["campaign_id"] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | SUM(impressions) | [{"table": "google_ads__ad_group_report", "column": "impressions"}] | [] | False |
| B1 | SUM(clicks) | [{"table": "google_ads__ad_group_report", "column": "clicks"}] | [] | False |
| B1 | SUM(spend) | [{"table": "google_ads__ad_group_report", "column": "spend"}] | [] | False |
| B1 | SUM(conversions) | [{"table": "google_ads__ad_group_report", "column": "conversions"}] | [] | False |
| B1 | SUM(clicks) | [{"table": "google_ads__ad_group_report", "column": "clicks"}] | [] | False |
| B1 | SUM(conversions) | [{"table": "google_ads__ad_group_report", "column": "conversions"}] | [] | False |


## S13

类别 `data`；来源 `query_db`；调用 `efe9eacc8a8e406882b4dcc09a7a6812`；状态 `success`。

```sql
SELECT DISTINCT c.advertising_channel_type, c.advertising_channel_subtype, c.campaign_name, c.campaign_id, c.status
FROM google_ads__campaign_report c
ORDER BY c.campaign_name
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-060/attempt-01/sql/S13.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-060/attempt-01/sql/S13.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-060/attempt-01/results/S13.rows.jsonl)；完整：True；SHA256：`cd8b244d8397d5b3abde0ee62471688ed29b0a41949b2c89b22ca2a17447e98f`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "c", "kind": "base", "block": null, "base_tables": ["google_ads__campaign_report"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |


## S14

类别 `data`；来源 `query_db`；调用 `40df7252fd19439cb56f5cb74f8bbaff`；状态 `success`。

```sql
SELECT COUNT(DISTINCT campaign_id) AS n_campaigns_ag FROM google_ads__ad_group_report
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-060/attempt-01/sql/S14.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-060/attempt-01/sql/S14.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-060/attempt-01/results/S14.rows.jsonl)；完整：True；SHA256：`e3ed33dc26a723b8481ca677e38dc4a6e8700aeec312afdd02c9dd92374161a2`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "google_ads__ad_group_report", "kind": "base", "block": null, "base_tables": ["google_ads__ad_group_report"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(DISTINCT campaign_id) | [{"table": "google_ads__ad_group_report", "column": "campaign_id"}] | [] | False |


## S15

类别 `data`；来源 `query_db`；调用 `a18841249538447b9cb8cd89d271ec9b`；状态 `success`。

```sql
SELECT COUNT(DISTINCT campaign_id) AS n_campaigns_cr, COUNT(*) AS n_rows FROM google_ads__campaign_report
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-060/attempt-01/sql/S15.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-060/attempt-01/sql/S15.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-060/attempt-01/results/S15.rows.jsonl)；完整：True；SHA256：`cb20e615f515db9e46c41b4fee3facecaaaf8e3e03fb0ee4d6b99631f5f2cadd`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "google_ads__campaign_report", "kind": "base", "block": null, "base_tables": ["google_ads__campaign_report"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(DISTINCT campaign_id) | [{"table": "google_ads__campaign_report", "column": "campaign_id"}] | [] | False |
| B1 | COUNT(*) | [] | [] | True |


## S16

类别 `data`；来源 `query_db`；调用 `0ca1589765e44ae296025b90b834eb36`；状态 `success`。

```sql
-- Per-ad-group aggregates with campaign_id
SELECT ad_group_id, ad_group_name, campaign_id, campaign_name, account_name, status,
       SUM(impressions) AS impressions, SUM(clicks) AS clicks, SUM(spend) AS spend,
       SUM(conversions) AS conversions, SUM(conversions_value) AS conv_value, SUM(view_through_conversions) AS vtc,
       ROUND(CAST(SUM(clicks) AS REAL) / SUM(impressions), 6) AS ctr,
       ROUND(CAST(SUM(conversions) AS REAL) / SUM(clicks), 6) AS cvr
FROM google_ads__ad_group_report
GROUP BY ad_group_id
ORDER BY ad_group_id
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-060/attempt-01/sql/S16.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-060/attempt-01/sql/S16.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-060/attempt-01/results/S16.rows.jsonl)；完整：True；SHA256：`36066d8e4995f440e52c2d628d538ee9f799f12abdd0fe70f0c0fa29ac12ddad`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "google_ads__ad_group_report", "kind": "base", "block": null, "base_tables": ["google_ads__ad_group_report"]}] | [] | ["ad_group_id"] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | SUM(impressions) | [{"table": "google_ads__ad_group_report", "column": "impressions"}] | [] | False |
| B1 | SUM(clicks) | [{"table": "google_ads__ad_group_report", "column": "clicks"}] | [] | False |
| B1 | SUM(spend) | [{"table": "google_ads__ad_group_report", "column": "spend"}] | [] | False |
| B1 | SUM(conversions) | [{"table": "google_ads__ad_group_report", "column": "conversions"}] | [] | False |
| B1 | SUM(conversions_value) | [{"table": "google_ads__ad_group_report", "column": "conversions_value"}] | [] | False |
| B1 | SUM(view_through_conversions) | [{"table": "google_ads__ad_group_report", "column": "view_through_conversions"}] | [] | False |
| B1 | SUM(impressions) | [{"table": "google_ads__ad_group_report", "column": "impressions"}] | [] | False |
| B1 | SUM(clicks) | [{"table": "google_ads__ad_group_report", "column": "clicks"}] | [] | False |
| B1 | SUM(clicks) | [{"table": "google_ads__ad_group_report", "column": "clicks"}] | [] | False |
| B1 | SUM(conversions) | [{"table": "google_ads__ad_group_report", "column": "conversions"}] | [] | False |


## S17

类别 `data`；来源 `query_db`；调用 `f7983a1973994cb299559ae27965284e`；状态 `success`。

```sql
-- Campaign-level aggregates from campaign_report (aggregated per campaign)
SELECT campaign_id, campaign_name, account_name, advertising_channel_type, advertising_channel_subtype, status,
       SUM(impressions) AS campaign_impressions, SUM(clicks) AS campaign_clicks, SUM(spend) AS campaign_spend,
       SUM(conversions) AS campaign_conversions,
       ROUND(CAST(SUM(conversions) AS REAL) / SUM(clicks), 6) AS campaign_cvr
FROM google_ads__campaign_report
GROUP BY campaign_id
ORDER BY campaign_id
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-060/attempt-01/sql/S17.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-060/attempt-01/sql/S17.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-060/attempt-01/results/S17.rows.jsonl)；完整：True；SHA256：`b530952faa88f2013c8bb56b54a5e0ee116a4736f40c53ea8d080310140036f0`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "google_ads__campaign_report", "kind": "base", "block": null, "base_tables": ["google_ads__campaign_report"]}] | [] | ["campaign_id"] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | SUM(impressions) | [{"table": "google_ads__campaign_report", "column": "impressions"}] | [] | False |
| B1 | SUM(clicks) | [{"table": "google_ads__campaign_report", "column": "clicks"}] | [] | False |
| B1 | SUM(spend) | [{"table": "google_ads__campaign_report", "column": "spend"}] | [] | False |
| B1 | SUM(conversions) | [{"table": "google_ads__campaign_report", "column": "conversions"}] | [] | False |
| B1 | SUM(clicks) | [{"table": "google_ads__campaign_report", "column": "clicks"}] | [] | False |
| B1 | SUM(conversions) | [{"table": "google_ads__campaign_report", "column": "conversions"}] | [] | False |


## S18

类别 `data`；来源 `query_db`；调用 `0cbd43a9eda64ff5bd05518c1ccdaa26`；状态 `success`。

```sql
-- Keywords for problematic ad groups: join with problematic list
SELECT k.ad_group_id, k.keyword_text, k.keyword_match_type, k.type, k.status AS kw_status,
       SUM(k.impressions) AS kw_impressions, SUM(k.clicks) AS kw_clicks, SUM(k.spend) AS kw_spend,
       SUM(k.conversions) AS kw_conversions
FROM google_ads__keyword_report k
INNER JOIN (
  SELECT DISTINCT ad_group_id FROM google_ads__ad_group_report
  GROUP BY ad_group_id
  HAVING ROUND(CAST(SUM(clicks) AS REAL) / SUM(impressions), 6) > 0.035876
     AND ROUND(CAST(SUM(conversions) AS REAL) / SUM(clicks), 6) < 0.038462
) p ON k.ad_group_id = p.ad_group_id
GROUP BY k.ad_group_id, k.keyword_text, k.keyword_match_type
ORDER BY k.ad_group_id, kw_impressions DESC
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-060/attempt-01/sql/S18.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-060/attempt-01/sql/S18.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-060/attempt-01/results/S18.rows.jsonl)；完整：True；SHA256：`c6704cda8f2f28a082fa8ee7d6121fd241f89efef2c3a68a3f9386b3e83f531d`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "google_ads__ad_group_report", "kind": "base", "block": null, "base_tables": ["google_ads__ad_group_report"]}] | [] | ["ad_group_id"] |
| B2 | [{"alias": "k", "kind": "base", "block": null, "base_tables": ["google_ads__keyword_report"]}, {"alias": "p", "kind": "derived", "block": "B1", "base_tables": ["google_ads__ad_group_report"]}] | [{"type": "INNER", "right": "(SELECT DISTINCT ad_group_id FROM google_ads__ad_group_report GROUP BY ad_group_id HAVING ROUND(CAST(SUM(clicks) AS REAL) / SUM(impressions), 6) > 0.035876 AND ROUND(CAST(SUM(conversions) AS REAL) / SUM(clicks), 6) < 0.038462) AS p", "on": "k.ad_group_id = p.ad_group_id", "using": []}] | ["k.ad_group_id", "k.keyword_text", "k.keyword_match_type"] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | SUM(impressions) | [{"table": "google_ads__ad_group_report", "column": "impressions"}] | [] | False |
| B1 | SUM(clicks) | [{"table": "google_ads__ad_group_report", "column": "clicks"}] | [] | False |
| B1 | SUM(clicks) | [{"table": "google_ads__ad_group_report", "column": "clicks"}] | [] | False |
| B1 | SUM(conversions) | [{"table": "google_ads__ad_group_report", "column": "conversions"}] | [] | False |
| B2 | SUM(k.impressions) | [{"table": "google_ads__keyword_report", "column": "impressions"}] | [] | False |
| B2 | SUM(k.clicks) | [{"table": "google_ads__keyword_report", "column": "clicks"}] | [] | False |
| B2 | SUM(k.spend) | [{"table": "google_ads__keyword_report", "column": "spend"}] | [] | False |
| B2 | SUM(k.conversions) | [{"table": "google_ads__keyword_report", "column": "conversions"}] | [] | False |


## S19

类别 `data`；来源 `query_db`；调用 `261df9820c794d6692c40eff95bb6d03`；状态 `success`。

```sql
-- Search terms for problematic ad groups
SELECT s.ad_group_id, s.search_term, s.keyword_text, s.keyword_match_type, s.search_term_match_type,
       SUM(s.impressions) AS s_impressions, SUM(s.clicks) AS s_clicks, SUM(s.spend) AS s_spend, SUM(s.conversions) AS s_conversions
FROM google_ads__search_term_report s
INNER JOIN (
  SELECT DISTINCT ad_group_id FROM google_ads__ad_group_report
  GROUP BY ad_group_id
  HAVING ROUND(CAST(SUM(clicks) AS REAL) / SUM(impressions), 6) > 0.035876
     AND ROUND(CAST(SUM(conversions) AS REAL) / SUM(clicks), 6) < 0.038462
) p ON s.ad_group_id = p.ad_group_id
GROUP BY s.ad_group_id, s.search_term, s.keyword_text, s.keyword_match_type, s.search_term_match_type
ORDER BY s.ad_group_id, s_impressions DESC
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-060/attempt-01/sql/S19.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-060/attempt-01/sql/S19.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-060/attempt-01/results/S19.rows.jsonl)；完整：True；SHA256：`db07a1f0b035a641b9bc297a99d32c295bb35343e48479bee61521ded3394586`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "google_ads__ad_group_report", "kind": "base", "block": null, "base_tables": ["google_ads__ad_group_report"]}] | [] | ["ad_group_id"] |
| B2 | [{"alias": "s", "kind": "base", "block": null, "base_tables": ["google_ads__search_term_report"]}, {"alias": "p", "kind": "derived", "block": "B1", "base_tables": ["google_ads__ad_group_report"]}] | [{"type": "INNER", "right": "(SELECT DISTINCT ad_group_id FROM google_ads__ad_group_report GROUP BY ad_group_id HAVING ROUND(CAST(SUM(clicks) AS REAL) / SUM(impressions), 6) > 0.035876 AND ROUND(CAST(SUM(conversions) AS REAL) / SUM(clicks), 6) < 0.038462) AS p", "on": "s.ad_group_id = p.ad_group_id", "using": []}] | ["s.ad_group_id", "s.search_term", "s.keyword_text", "s.keyword_match_type", "s.search_term_match_type"] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | SUM(impressions) | [{"table": "google_ads__ad_group_report", "column": "impressions"}] | [] | False |
| B1 | SUM(clicks) | [{"table": "google_ads__ad_group_report", "column": "clicks"}] | [] | False |
| B1 | SUM(clicks) | [{"table": "google_ads__ad_group_report", "column": "clicks"}] | [] | False |
| B1 | SUM(conversions) | [{"table": "google_ads__ad_group_report", "column": "conversions"}] | [] | False |
| B2 | SUM(s.impressions) | [{"table": "google_ads__search_term_report", "column": "impressions"}] | [] | False |
| B2 | SUM(s.clicks) | [{"table": "google_ads__search_term_report", "column": "clicks"}] | [] | False |
| B2 | SUM(s.spend) | [{"table": "google_ads__search_term_report", "column": "spend"}] | [] | False |
| B2 | SUM(s.conversions) | [{"table": "google_ads__search_term_report", "column": "conversions"}] | [] | False |


## S20

类别 `data`；来源 `query_db`；调用 `91a61dff9acd4cc5be9d72bd254c1c89`；状态 `success`。

```sql
-- URL report for problematic ad groups
SELECT u.ad_group_id, u.base_url, u.url_host, u.url_path,
       SUM(u.impressions) AS u_impressions, SUM(u.clicks) AS u_clicks, SUM(u.spend) AS u_spend, SUM(u.conversions) AS u_conversions
FROM google_ads__url_report u
INNER JOIN (
  SELECT DISTINCT ad_group_id FROM google_ads__ad_group_report
  GROUP BY ad_group_id
  HAVING ROUND(CAST(SUM(clicks) AS REAL) / SUM(impressions), 6) > 0.035876
     AND ROUND(CAST(SUM(conversions) AS REAL) / SUM(clicks), 6) < 0.038462
) p ON u.ad_group_id = p.ad_group_id
GROUP BY u.ad_group_id, u.base_url, u.url_host, u.url_path
ORDER BY u.ad_group_id, u_impressions DESC
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-060/attempt-01/sql/S20.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-060/attempt-01/sql/S20.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-060/attempt-01/results/S20.rows.jsonl)；完整：True；SHA256：`e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "google_ads__ad_group_report", "kind": "base", "block": null, "base_tables": ["google_ads__ad_group_report"]}] | [] | ["ad_group_id"] |
| B2 | [{"alias": "u", "kind": "base", "block": null, "base_tables": ["google_ads__url_report"]}, {"alias": "p", "kind": "derived", "block": "B1", "base_tables": ["google_ads__ad_group_report"]}] | [{"type": "INNER", "right": "(SELECT DISTINCT ad_group_id FROM google_ads__ad_group_report GROUP BY ad_group_id HAVING ROUND(CAST(SUM(clicks) AS REAL) / SUM(impressions), 6) > 0.035876 AND ROUND(CAST(SUM(conversions) AS REAL) / SUM(clicks), 6) < 0.038462) AS p", "on": "u.ad_group_id = p.ad_group_id", "using": []}] | ["u.ad_group_id", "u.base_url", "u.url_host", "u.url_path"] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | SUM(impressions) | [{"table": "google_ads__ad_group_report", "column": "impressions"}] | [] | False |
| B1 | SUM(clicks) | [{"table": "google_ads__ad_group_report", "column": "clicks"}] | [] | False |
| B1 | SUM(clicks) | [{"table": "google_ads__ad_group_report", "column": "clicks"}] | [] | False |
| B1 | SUM(conversions) | [{"table": "google_ads__ad_group_report", "column": "conversions"}] | [] | False |
| B2 | SUM(u.impressions) | [{"table": "google_ads__url_report", "column": "impressions"}] | [] | False |
| B2 | SUM(u.clicks) | [{"table": "google_ads__url_report", "column": "clicks"}] | [] | False |
| B2 | SUM(u.spend) | [{"table": "google_ads__url_report", "column": "spend"}] | [] | False |
| B2 | SUM(u.conversions) | [{"table": "google_ads__url_report", "column": "conversions"}] | [] | False |


## S21

类别 `data`；来源 `query_db`；调用 `6928c9f622684e06b174d6698a49a9c4`；状态 `success`。

```sql
-- All keywords with match type distribution per ad group
SELECT k.ad_group_id, k.keyword_match_type, k.type, k.status AS kw_status,
       SUM(k.impressions) AS kw_impressions, SUM(k.clicks) AS kw_clicks, SUM(k.spend) AS kw_spend, SUM(k.conversions) AS kw_conversions
FROM google_ads__keyword_report k
GROUP BY k.ad_group_id, k.keyword_match_type, k.type, k.status
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-060/attempt-01/sql/S21.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-060/attempt-01/sql/S21.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-060/attempt-01/results/S21.rows.jsonl)；完整：True；SHA256：`8b8756975e6b70f9f4a7482e5d970b64a35d503f661e9a1a143c754f555adf0f`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "k", "kind": "base", "block": null, "base_tables": ["google_ads__keyword_report"]}] | [] | ["k.ad_group_id", "k.keyword_match_type", "k.type", "k.status"] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | SUM(k.impressions) | [{"table": "google_ads__keyword_report", "column": "impressions"}] | [] | False |
| B1 | SUM(k.clicks) | [{"table": "google_ads__keyword_report", "column": "clicks"}] | [] | False |
| B1 | SUM(k.spend) | [{"table": "google_ads__keyword_report", "column": "spend"}] | [] | False |
| B1 | SUM(k.conversions) | [{"table": "google_ads__keyword_report", "column": "conversions"}] | [] | False |


## S22

类别 `data`；来源 `query_db`；调用 `b7c213caae084f33b9ac94cc3675e3ce`；状态 `success`。

```sql
-- All search terms data
SELECT s.ad_group_id, s.search_term, s.keyword_match_type, s.search_term_match_type,
       SUM(s.impressions) AS s_impressions, SUM(s.clicks) AS s_clicks, SUM(s.spend) AS s_spend, SUM(s.conversions) AS s_conversions
FROM google_ads__search_term_report s
GROUP BY s.ad_group_id, s.search_term, s.keyword_match_type, s.search_term_match_type
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-060/attempt-01/sql/S22.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-060/attempt-01/sql/S22.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-060/attempt-01/results/S22.rows.jsonl)；完整：True；SHA256：`8abf86b88f7ba4ec1e556339637950db2cd616a9990822aff65bacab067de146`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "s", "kind": "base", "block": null, "base_tables": ["google_ads__search_term_report"]}] | [] | ["s.ad_group_id", "s.search_term", "s.keyword_match_type", "s.search_term_match_type"] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | SUM(s.impressions) | [{"table": "google_ads__search_term_report", "column": "impressions"}] | [] | False |
| B1 | SUM(s.clicks) | [{"table": "google_ads__search_term_report", "column": "clicks"}] | [] | False |
| B1 | SUM(s.spend) | [{"table": "google_ads__search_term_report", "column": "spend"}] | [] | False |
| B1 | SUM(s.conversions) | [{"table": "google_ads__search_term_report", "column": "conversions"}] | [] | False |

