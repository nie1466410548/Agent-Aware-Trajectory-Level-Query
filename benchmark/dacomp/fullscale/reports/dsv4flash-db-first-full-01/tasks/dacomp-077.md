# dacomp-077

The product team's statistics show that we have 180 different features, but on average, a …

运行：已提交。官方未评分。全部 SQL 尝试/成功 45/41；数据 SQL 43/39；Python 6 次。

完整原题：

The product team's statistics show that we have 180 different features, but on average, a visitor uses only 12 of them. We want to quantify the contribution of different features to Customer Lifecycle Value (CLV), especially identifying "hidden value features"—those with low usage frequency (monthly active visitors < 200) but a significant positive impact on customer value. This analysis will provide data-driven support for next quarter's product investment.

| 表 | 行数 | 列数 |
| --- | --- | --- |
| pendo__account | 1000 | 22 |
| pendo__customer_lifecycle_insights | 8000 | 47 |
| pendo__feature | 180 | 32 |
| pendo__feature_daily_metrics | 16200 | 20 |
| pendo__product_adoption_analytics | 180 | 12 |
| pendo__visitor | 8000 | 24 |
| pendo__visitor_feature | 14283 | 9 |


实际路线（分析者依据 SQL/源码概括，不代表 Agent 自述）：SQL 提取功能与访客价值、采纳特征 → Python 逐功能检验及效应量、连接功能资料 → 隐藏价值功能建议。

数据库大小：8,298,496 字节。

## 数据 SQL

| SQL | 状态 | 基础表 | Join 输入/类型 | GROUP BY | 聚合表达式 | 结果行数 | 数据库 ms |
| --- | --- | --- | --- | --- | --- | --- | --- |
| [S3/Q1](#s3) | success | ["pendo__account", "pendo__customer_lifecycle_insights", "pendo__feature", "pendo__feature_daily_metrics", "pendo__product_adoption_analytics", "pendo__visitor", "pendo__visitor_feature"] | 0 / {} | [] | ["COUNT(*)", "COUNT(*)", "COUNT(*)", "COUNT(*)", "COUNT(*)", "COUNT(*)", "COUNT(*)"] | 1 | 4.067 |
| [S4/Q2](#s4) | success | ["pendo__feature"] | 0 / {} | [] | [] | 15 | 0.435 |
| [S5/Q3](#s5) | success | ["pendo__feature_daily_metrics"] | 0 / {} | [] | ["MIN(date_day)", "MAX(date_day)", "COUNT(DISTINCT date_day)", "COUNT(DISTINCT feature_id)"] | 1 | 6.17 |
| [S6/Q4](#s6) | success | ["pendo__customer_lifecycle_insights"] | 0 / {} | [] | [] | 20 | 0.369 |
| [S7/Q5](#s7) | success | ["pendo__visitor_feature"] | 0 / {} | [] | ["COUNT(*)", "COUNT(DISTINCT visitor_id)", "COUNT(DISTINCT feature_id)"] | 1 | 7.777 |
| [S8/Q6](#s8) | success | ["pendo__customer_lifecycle_insights"] | 0 / {} | [] | ["MIN(comprehensive_customer_value)", "MAX(comprehensive_customer_value)", "AVG(comprehensive_customer_value)", "MIN(user_value_score)", "MAX(user_value_score)", "AVG(user_value_score)", "COUNT(*)", "COUNT(DISTINCT predicted_clv_tier)"] | 1 | 3.74 |
| [S9/Q7](#s9) | success | ["pendo__customer_lifecycle_insights"] | 0 / {} | [] | ["SUM(CASE WHEN predicted_clv_tier IS NULL THEN 1 ELSE 0 END)", "SUM(CASE WHEN predicted_ltv_tier IS NULL THEN 1 ELSE 0 END)", "SUM(CASE WHEN rfm_composite_score IS NULL THEN 1 ELSE 0 END)", "SUM(CASE WHEN customer_value_tier IS NULL THEN 1 ELSE 0 END)", "SUM(CASE WHEN is_valuable_user IS NULL THEN 1 ELSE 0 END)", "SUM(CASE WHEN comprehensive_customer_value IS NULL THEN 1 ELSE 0 END)", "SUM(CASE WHEN user_value_score IS NULL THEN 1 ELSE 0 END)"] | 1 | 4.4 |
| [S10/Q8](#s10) | success | ["pendo__feature", "pendo__visitor_feature"] | 2 / {'LEFT': 1} | ["f.feature_id"] | ["COUNT(vf.visitor_id)", "COUNT(DISTINCT vf.visitor_id)", "SUM(vf.sum_clicks)"] | 15 | 22.979 |
| [S11/Q9](#s11) | success | ["pendo__visitor_feature"] | 0 / {} | [] | ["COUNT(DISTINCT visitor_id)", "COUNT(DISTINCT feature_id)"] | 1 | 7.484 |
| [S12/Q10](#s12) | success | ["pendo__feature"] | 0 / {} | [] | [] | 20 | 0.424 |
| [S13/Q11](#s13) | success | ["pendo__feature_daily_metrics"] | 0 / {} | ["feature_id"] | ["COUNT(DISTINCT STRFTIME('%Y-%m', date_day))", "AVG(count_visitors)", "MAX(count_visitors)", "SUM(count_visitors)"] | 20 | 13.68 |
| [S14/Q12](#s14) | failed | ["pendo__feature_daily_metrics"] | 0 / {} | ["s.strftime_Y_m"] | ["COUNT(DISTINCT date_day)"] | unknown | 未取得；调用总时长 0.184 ms |
| [S15/Q13](#s15) | success | ["pendo__feature_daily_metrics"] | 0 / {} | [] | [] | 4 | 9.625 |
| [S16/Q14](#s16) | success | ["pendo__feature_daily_metrics"] | 0 / {} | ["feature_id"] | ["COUNT(DISTINCT STRFTIME('%Y-%m', date_day))", "AVG(count_visitors)", "MAX(count_visitors)", "SUM(count_visitors)"] | 30 | 13.023 |
| [S17/Q15](#s17) | success | ["pendo__feature"] | 0 / {} | [] | ["COUNT(*)", "SUM(CASE WHEN count_visitors < 200 THEN 1 ELSE 0 END)", "SUM(CASE WHEN count_visitors BETWEEN 200 AND 1000 THEN 1 ELSE 0 END)", "SUM(CASE WHEN count_visitors > 1000 THEN 1 ELSE 0 END)", "MIN(count_visitors)", "MAX(count_visitors)", "AVG(count_visitors)"] | 1 | 0.448 |
| [S18/Q16](#s18) | success | ["pendo__customer_lifecycle_insights", "pendo__visitor_feature"] | 2 / {'INNER': 1} | [] | ["COUNT(*)"] | 1 | 14.679 |
| [S19/Q17](#s19) | success | ["pendo__feature"] | 0 / {} | [] | [] | 47 | 0.551 |
| [S20/Q18](#s20) | success | ["pendo__customer_lifecycle_insights", "pendo__visitor_feature"] | 2 / {'INNER': 1} | [] | [] | 10 | 5.5 |
| [S21/Q19](#s21) | success | ["pendo__customer_lifecycle_insights", "pendo__visitor_feature"] | 2 / {'INNER': 1} | [] | ["AVG(c2.comprehensive_customer_value)", "AVG(comprehensive_customer_value)", "MIN(comprehensive_customer_value)", "MAX(comprehensive_customer_value)"] | 1 | 11.436 |
| [S22/Q20](#s22) | success | ["pendo__customer_lifecycle_insights", "pendo__feature", "pendo__visitor_feature"] | 3 / {'INNER': 2} | ["f.feature_id"] | ["AVG(c2.comprehensive_customer_value)", "AVG(c.comprehensive_customer_value)", "COUNT(DISTINCT vf.visitor_id)"] | 20 | 74452.875 |
| [S23/Q21](#s23) | success | ["pendo__feature", "pendo__feature_daily_metrics"] | 2 / {'INNER': 1} | ["f.feature_id", "dm.month"] | ["SUM(dm.count_visitors)", "MAX(dm.count_visitors)"] | 20 | 8.901 |
| [S24/Q22](#s24) | success | ["pendo__visitor_feature"] | 0 / {} | [] | ["COUNT(*)", "SUM(CASE WHEN NOT first_click_at IS NULL THEN 1 ELSE 0 END)", "SUM(CASE WHEN NOT last_click_at IS NULL THEN 1 ELSE 0 END)"] | 1 | 2.73 |
| [S25/Q23](#s25) | cancelled | ["pendo__customer_lifecycle_insights", "pendo__feature", "pendo__visitor_feature"] | 2 / {'INNER': 1, 'LEFT': 2} | ["fi.feature_id"] | ["AVG(uc2.comprehensive_customer_value)", "COUNT(*)", "COUNT(DISTINCT fi.visitor_id)", "AVG(uc.comprehensive_customer_value)"] | unknown | 未取得；调用总时长 300000.444 ms |
| [S26/Q24](#s26) | success | ["pendo__customer_lifecycle_insights", "pendo__feature", "pendo__visitor_feature"] | 3 / {'INNER': 1, 'LEFT': 2} | ["f.feature_id"] | ["AVG(c.comprehensive_customer_value)", "COUNT(*)", "COUNT(DISTINCT vf.visitor_id)", "AVG(c.comprehensive_customer_value)", "AVG(c.comprehensive_customer_value)"] | 60 | 46.06 |
| [S27/Q25](#s27) | success | ["pendo__customer_lifecycle_insights", "pendo__feature", "pendo__visitor_feature"] | 3 / {'INNER': 1, 'CROSS': 1, 'LEFT': 1} | ["f.feature_id"] | ["COUNT(*)", "COUNT(DISTINCT vf.visitor_id)", "AVG(CASE WHEN NOT vf.visitor_id IS NULL THEN bc.comprehensive_customer_value END)", "AVG(CASE WHEN vf.visitor_id IS NULL THEN bc.comprehensive_customer_value END)", "AVG(CASE WHEN NOT vf.visitor_id IS NULL THEN bc.comprehensive_customer_value END)", "AVG(CASE WHEN vf.visitor_id IS NULL THEN bc.comprehensive_customer_value END)"] | 60 | 371.389 |
| [S28/Q26](#s28) | success | ["pendo__customer_lifecycle_insights", "pendo__feature", "pendo__visitor_feature"] | 3 / {'INNER': 1, 'CROSS': 1, 'LEFT': 1} | ["f.feature_id"] | ["COUNT(DISTINCT vf.visitor_id)", "AVG(CASE WHEN NOT vf.visitor_id IS NULL THEN bc.comprehensive_customer_value END)", "AVG(CASE WHEN vf.visitor_id IS NULL THEN bc.comprehensive_customer_value END)", "COUNT(CASE WHEN NOT vf.visitor_id IS NULL THEN 1 END)", "COUNT(CASE WHEN vf.visitor_id IS NULL THEN 1 END)"] | 180 | 389.405 |
| [S29/Q27](#s29) | success | ["pendo__customer_lifecycle_insights", "pendo__visitor_feature"] | 2 / {'INNER': 1} | [] | [] | 1000 | 11.381 |
| [S30/Q28](#s30) | success | ["pendo__visitor_feature"] | 0 / {} | [] | [] | 14283 | 19.959 |
| [S31/Q29](#s31) | success | ["pendo__customer_lifecycle_insights", "pendo__visitor_feature"] | 2 / {'INNER': 1} | [] | [] | 1000 | 10.13 |
| [S32/Q30](#s32) | success | ["pendo__visitor_feature"] | 0 / {} | [] | [] | 14283 | 18.105 |
| [S33/Q31](#s33) | success | ["pendo__feature"] | 0 / {} | [] | [] | 180 | 0.738 |
| [S34/Q32](#s34) | success | ["pendo__feature", "pendo__feature_daily_metrics"] | 2 / {'INNER': 1} | ["f.feature_id"] | ["AVG(fdm.count_visitors)", "AVG(fdm.count_visitors)"] | 30 | 14.298 |
| [S35/Q33](#s35) | success | ["pendo__product_adoption_analytics"] | 0 / {} | [] | [] | 8 | 0.46 |
| [S36/Q34](#s36) | success | ["pendo__feature"] | 0 / {} | ["CASE WHEN count_visitors < 200 THEN '<200' WHEN count_visitors < 500 THEN '200-500' WHEN count_visitors < 1000 THEN '500-1000' ELSE '>=1000' END"] | ["COUNT(*)", "MIN(count_visitors)"] | 4 | 0.682 |
| [S37/Q35](#s37) | success | ["pendo__feature", "pendo__product_adoption_analytics"] | 2 / {'INNER': 1} | [] | [] | 47 | 0.689 |
| [S38/Q36](#s38) | success | ["pendo__feature", "pendo__product_adoption_analytics"] | 2 / {'INNER': 1} | [] | [] | 180 | 0.902 |
| [S39/Q37](#s39) | success | ["pendo__feature", "pendo__feature_daily_metrics"] | 2 / {'INNER': 1} | ["feature_id", "STRFTIME('%Y-%m', date_day)"] | ["MAX(count_visitors)", "AVG(count_visitors)", "SUM(count_visitors)"] | 20 | 14.631 |
| [S40/Q38](#s40) | success | ["pendo__product_adoption_analytics"] | 0 / {} | [] | [] | 180 | 0.763 |
| [S41/Q39](#s41) | success | ["pendo__feature"] | 0 / {} | [] | [] | 180 | 0.471 |
| [S42/Q40](#s42) | failed | ["pendo__customer_lifecycle_insights"] | 0 / {} | [] | ["AVG(CASE WHEN pct <= 25 THEN comprehensive_customer_value END)", "AVG(CASE WHEN pct <= 50 THEN comprehensive_customer_value END)", "AVG(CASE WHEN pct <= 75 THEN comprehensive_customer_value END)", "AVG(comprehensive_customer_value)", "MIN(comprehensive_customer_value)", "MAX(comprehensive_customer_value)", "STDDEV(comprehensive_customer_value)"] | unknown | 未取得；调用总时长 0.215 ms |
| [S43/Q41](#s43) | failed | ["pendo__visitor_feature"] | 0 / {} | ["visitor_id"] | ["COUNT(*)", "AVG(vf_count)", "MIN(vf_count)", "MAX(vf_count)", "PERCENTILE_CONT(vf_count, 0.5)"] | unknown | 未取得；调用总时长 0.182 ms |
| [S44/Q42](#s44) | success | ["pendo__customer_lifecycle_insights"] | 0 / {} | [] | ["COUNT(*)", "AVG(comprehensive_customer_value)", "MIN(comprehensive_customer_value)", "MAX(comprehensive_customer_value)", "AVG(user_value_score)", "MIN(user_value_score)", "MAX(user_value_score)", "SUM(CASE WHEN comprehensive_customer_value >= 500 THEN 1 ELSE 0 END)"] | 1 | 3.671 |
| [S45/Q43](#s45) | success | ["pendo__visitor_feature"] | 0 / {} | ["visitor_id"] | ["COUNT(*)", "AVG(cnt)", "MIN(cnt)", "MAX(cnt)"] | 1 | 5.24 |


## 元数据和设置

| SQL | 类别 | 状态 | 内容 |
| --- | --- | --- | --- |
| S1 | connection_setup | success | PRAGMA query_only=ON |
| S2 | metadata | success | SELECT name,sql FROM sqlite_master WHERE type='table' ORDER BY name |


## Python 与执行位置

人工源码审查：**database_first_violation**。逐功能 t 检验、效应量与均值差需要统计输入，应与纯分组迁出区别评价。Python 还将统计结果与功能/采纳表多次合并并执行使用人数阈值计数，这些关系和条件聚合可在 SQL 内完成，记录偏离。 [证据](../reviews/dacomp-077.json)。

P1：Compute per-feature t-tests (Welch) comparing comprehensive_customer_value of feature users vs non-users across the 1000 tracked visitors, plus usage thresholds. This requires per-visitor distributions and statistical hypothesis testing not supported by SQLite.

[源码](../../../runs/dsv4flash-db-first-full-01/dacomp-077/attempt-01/python/P1.py)；[输出](../../../runs/dsv4flash-db-first-full-01/dacomp-077/attempt-01/python/P1.stdout)；[错误](../../../runs/dsv4flash-db-first-full-01/dacomp-077/attempt-01/python/P1.stderr)。检出需人工核验的 SQL 可实现操作：groupby(, .merge(, .query(, sort_values(；不能仅凭理由判为合规。

P2：Identify hidden value features: count_visitors < 200 (low monthly active users) with significant positive CCV impact. Also compute effect size (Cohen's d) and usage intensity metrics. Visualize findings.

[源码](../../../runs/dsv4flash-db-first-full-01/dacomp-077/attempt-01/python/P2.py)；[输出](../../../runs/dsv4flash-db-first-full-01/dacomp-077/attempt-01/python/P2.stdout)；[错误](../../../runs/dsv4flash-db-first-full-01/dacomp-077/attempt-01/python/P2.stderr)。检出需人工核验的 SQL 可实现操作：sort_values(；不能仅凭理由判为合规。

P3：Re-run Cohen's d computation and hidden value feature identification using correct /results/ archive paths for per-visitor CLV data and visitor-feature usage data.

[源码](../../../runs/dsv4flash-db-first-full-01/dacomp-077/attempt-01/python/P3.py)；[输出](../../../runs/dsv4flash-db-first-full-01/dacomp-077/attempt-01/python/P3.stdout)；[错误](../../../runs/dsv4flash-db-first-full-01/dacomp-077/attempt-01/python/P3.stderr)。检出需人工核验的 SQL 可实现操作：sort_values(；不能仅凭理由判为合规。

P4：Parse archived query results (JSON arrays per line) to compute Cohen's d and identify hidden value features.

[源码](../../../runs/dsv4flash-db-first-full-01/dacomp-077/attempt-01/python/P4.py)；[输出](../../../runs/dsv4flash-db-first-full-01/dacomp-077/attempt-01/python/P4.stdout)；[错误](../../../runs/dsv4flash-db-first-full-01/dacomp-077/attempt-01/python/P4.stderr)。检出需人工核验的 SQL 可实现操作：sort_values(；不能仅凭理由判为合规。

P5：Cross-validate usage metrics between feature table count_visitors and adoption analytics regular_users to determine the best proxy for 'monthly active visitors'. Compute correlation and thresholds.

[源码](../../../runs/dsv4flash-db-first-full-01/dacomp-077/attempt-01/python/P5.py)；[输出](../../../runs/dsv4flash-db-first-full-01/dacomp-077/attempt-01/python/P5.stdout)；[错误](../../../runs/dsv4flash-db-first-full-01/dacomp-077/attempt-01/python/P5.stderr)。检出需人工核验的 SQL 可实现操作：.merge(, .query(；不能仅凭理由判为合规。

P6：Comprehensive analysis of hidden value features using both usage metrics (count_visitors and regular_users). Create visualizations for the report.

[源码](../../../runs/dsv4flash-db-first-full-01/dacomp-077/attempt-01/python/P6.py)；[输出](../../../runs/dsv4flash-db-first-full-01/dacomp-077/attempt-01/python/P6.stdout)；[错误](../../../runs/dsv4flash-db-first-full-01/dacomp-077/attempt-01/python/P6.stderr)。检出需人工核验的 SQL 可实现操作：.merge(, .query(, sort_values(；不能仅凭理由判为合规。

## 优化机会

已验证候选。筛选限于精确 SQL、相同自包含 CTE、相同单表完整过滤、可分解单表聚合；未覆盖任意 Join 等价和一般谓词蕴含。全部候选都是 offline，未测在线预测。

| 候选 | 类型 | 已有结果 | 覆盖 SQL | 后续次数 | 中间行数 | 验证 | 成本 |
| --- | --- | --- | --- | --- | --- | --- | --- |
| C1 | exact-result reuse | True | ["S29", "S31"] | 1 | 1000 | verified | Not benchmarked; correctness alone does not establish net speedup. |
| C2 | exact-result reuse | True | ["S30", "S32"] | 1 | 14283 | verified | Not benchmarked; correctness alone does not establish net speedup. |
| C3 | common subexpression | False | ["S26", "S27"] | 1 | 1000 | verified | Not benchmarked; correctness alone does not establish net speedup. |
| C4 | aggregate MV | False | ["S17", "S36"] | 1 | unknown | not_verified_cap | Not tested |
| C5 | aggregate MV | False | ["S9", "S44"] | 1 | unknown | not_verified_cap | Not tested |


已验证覆盖（含触发查询、候选并集去重）：6/39 条成功数据 SQL。正确性仅针对当前数据库快照；未测性能的候选不能声称已加速。

[完整 build/rewrite 与比较证据](dacomp-077.analysis.json)。

### C1：exact-result reuse

Identical normalized SQL and parameters; archive equality checked.

原查询 [S29](#s29), [S31](#s31) → 保留前序结果 S29 → 后续 1 次可复用。该构建点为事后假设，不代表 Agent 当时预知后续。

| 原 SQL | 列名一致 | 结果一致 | 比较方法 |
| --- | --- | --- | --- |
| S31 | True | True | exact_multiset |


验证状态：verified；成本结论：Not benchmarked; correctness alone does not establish net speedup.

### C2：exact-result reuse

Identical normalized SQL and parameters; archive equality checked.

原查询 [S30](#s30), [S32](#s32) → 保留前序结果 S30 → 后续 1 次可复用。该构建点为事后假设，不代表 Agent 当时预知后续。

| 原 SQL | 列名一致 | 结果一致 | 比较方法 |
| --- | --- | --- | --- |
| S32 | True | True | exact_multiset |


验证状态：verified；成本结论：Not benchmarked; correctness alone does not establish net speedup.

### C3：common subexpression

Identical self-contained CTE body across queries.

原查询 [S26](#s26), [S27](#s27) → 新增共享状态 C3 → 后续 1 次可复用。该构建点为事后假设，不代表 Agent 当时预知后续。

构建定义：

```sql
SELECT DISTINCT visitor_id FROM pendo__visitor_feature
```

受益查询 S26 的改写示例：

```sql
WITH tracked_visitors AS (SELECT * FROM temp.reuse_candidate), base AS (SELECT AVG(c.comprehensive_customer_value) AS avg_ccv_overall, COUNT(*) AS n_tracked FROM pendo__customer_lifecycle_insights AS c JOIN tracked_visitors AS tv ON c.visitor_id = tv.visitor_id) SELECT f.feature_id, f.feature_name, f.count_visitors AS total_visitors, f.product_area_name, f.is_core_event, COUNT(DISTINCT vf.visitor_id) AS n_tracked_users, AVG(c.comprehensive_customer_value) AS avg_ccv_users, (SELECT avg_ccv_overall FROM base) AS avg_ccv_overall, (SELECT n_tracked FROM base) AS n_tracked FROM pendo__feature AS f LEFT JOIN pendo__visitor_feature AS vf ON vf.feature_id = f.feature_id LEFT JOIN pendo__customer_lifecycle_insights AS c ON vf.visitor_id = c.visitor_id GROUP BY f.feature_id ORDER BY (AVG(c.comprehensive_customer_value) - (SELECT avg_ccv_overall FROM base)) DESC LIMIT 60
```

| 原 SQL | 列名一致 | 结果一致 | 比较方法 |
| --- | --- | --- | --- |
| S26 | True | True | ordered_numeric_tolerance |
| S27 | True | True | ordered_numeric_tolerance |


验证状态：verified；成本结论：Not benchmarked; correctness alone does not establish net speedup.

结果依赖：自动记录 SQL→Python 的接口父调用，以及源码中引用归档文件的消费者；字面值相同不认定因果。模型方向选择需要人工读取消息，尚未做全面因果标注。

[原始报告](../../../runs/dsv4flash-db-first-full-01/dacomp-077/attempt-01/answer.md)；[统一消息](../../../runs/dsv4flash-db-first-full-01/dacomp-077/attempt-01/messages.jsonl)；[原始 OpenCode 事件](../../../runs/dsv4flash-db-first-full-01/dacomp-077/attempt-01/opencode.jsonl)；[SQL 引擎日志](../../../runs/dsv4flash-db-first-full-01/dacomp-077/attempt-01/sql_journal.jsonl)。

[可读报告（本地图片链接规范化）](../answers/dacomp-077.md)。原始回答保留，分析结论未改写。

## S1

类别 `connection_setup`；来源 `connection`；调用 `0fe4e3d615f64ce7b27b4ee177c7961b`；状态 `success`。

```sql
PRAGMA query_only=ON
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-077/attempt-01/sql/S1.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-077/attempt-01/sql/S1.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-077/attempt-01/results/S1.rows.jsonl)；完整：True；SHA256：`e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`。

## S2

类别 `metadata`；来源 `list_db`；调用 `0fe4e3d615f64ce7b27b4ee177c7961b`；状态 `success`。

```sql
SELECT name,sql FROM sqlite_master WHERE type='table' ORDER BY name
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-077/attempt-01/sql/S2.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-077/attempt-01/sql/S2.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-077/attempt-01/results/S2.rows.jsonl)；完整：True；SHA256：`b23ed92ebfc4d1a318a238d618b06ed860cb110f8e34b2d78a0b1580445ef135`。

## S3

类别 `data`；来源 `query_db`；调用 `6999027ada434c6ba07494e591ad58bc`；状态 `success`。

```sql
SELECT
 (SELECT COUNT(*) FROM pendo__feature) AS n_features,
 (SELECT COUNT(*) FROM pendo__visitor) AS n_visitors,
 (SELECT COUNT(*) FROM pendo__visitor_feature) AS n_visitor_feature,
 (SELECT COUNT(*) FROM pendo__feature_daily_metrics) AS n_feature_daily,
 (SELECT COUNT(*) FROM pendo__customer_lifecycle_insights) AS n_clv,
 (SELECT COUNT(*) FROM pendo__product_adoption_analytics) AS n_adoption,
 (SELECT COUNT(*) FROM pendo__account) AS n_accounts
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-077/attempt-01/sql/S3.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-077/attempt-01/sql/S3.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-077/attempt-01/results/S3.rows.jsonl)；完整：True；SHA256：`028e1b3129d8a49357ee70617e605b7f932289ff166a30b628aee3b09a294cc3`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "pendo__feature", "kind": "base", "block": null, "base_tables": ["pendo__feature"]}] | [] | [] |
| B2 | [{"alias": "pendo__visitor", "kind": "base", "block": null, "base_tables": ["pendo__visitor"]}] | [] | [] |
| B3 | [{"alias": "pendo__visitor_feature", "kind": "base", "block": null, "base_tables": ["pendo__visitor_feature"]}] | [] | [] |
| B4 | [{"alias": "pendo__feature_daily_metrics", "kind": "base", "block": null, "base_tables": ["pendo__feature_daily_metrics"]}] | [] | [] |
| B5 | [{"alias": "pendo__customer_lifecycle_insights", "kind": "base", "block": null, "base_tables": ["pendo__customer_lifecycle_insights"]}] | [] | [] |
| B6 | [{"alias": "pendo__product_adoption_analytics", "kind": "base", "block": null, "base_tables": ["pendo__product_adoption_analytics"]}] | [] | [] |
| B7 | [{"alias": "pendo__account", "kind": "base", "block": null, "base_tables": ["pendo__account"]}] | [] | [] |
| B8 | [] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |
| B2 | COUNT(*) | [] | [] | True |
| B3 | COUNT(*) | [] | [] | True |
| B4 | COUNT(*) | [] | [] | True |
| B5 | COUNT(*) | [] | [] | True |
| B6 | COUNT(*) | [] | [] | True |
| B7 | COUNT(*) | [] | [] | True |


## S4

类别 `data`；来源 `query_db`；调用 `aaa4d5a92b1e4de9a8e895e319607d05`；状态 `success`。

```sql
SELECT feature_id, feature_name, product_area_name, page_name, is_core_event, count_visitors, count_accounts, sum_clicks, first_click_at, last_click_at FROM pendo__feature ORDER BY count_visitors DESC LIMIT 15
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-077/attempt-01/sql/S4.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-077/attempt-01/sql/S4.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-077/attempt-01/results/S4.rows.jsonl)；完整：True；SHA256：`8d6f16b7950133c3752d0cd87be4002a831fdaeb48008259ef7ebfa24f4316e3`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "pendo__feature", "kind": "base", "block": null, "base_tables": ["pendo__feature"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |


## S5

类别 `data`；来源 `query_db`；调用 `d59894df3a034347b775f3e18f0883bf`；状态 `success`。

```sql
SELECT MIN(date_day) AS min_day, MAX(date_day) AS max_day, COUNT(DISTINCT date_day) AS n_days, COUNT(DISTINCT feature_id) AS n_features FROM pendo__feature_daily_metrics
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-077/attempt-01/sql/S5.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-077/attempt-01/sql/S5.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-077/attempt-01/results/S5.rows.jsonl)；完整：True；SHA256：`253e348def9dc8555926a08770a0c0f51cb3b235b36e78fffdccc8ae1fd259f7`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "pendo__feature_daily_metrics", "kind": "base", "block": null, "base_tables": ["pendo__feature_daily_metrics"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | MIN(date_day) | [{"table": "pendo__feature_daily_metrics", "column": "date_day"}] | [] | False |
| B1 | MAX(date_day) | [{"table": "pendo__feature_daily_metrics", "column": "date_day"}] | [] | False |
| B1 | COUNT(DISTINCT date_day) | [{"table": "pendo__feature_daily_metrics", "column": "date_day"}] | [] | False |
| B1 | COUNT(DISTINCT feature_id) | [{"table": "pendo__feature_daily_metrics", "column": "feature_id"}] | [] | False |


## S6

类别 `data`；来源 `query_db`；调用 `b80cee8d55524c22b8b4ac87d210eace`；状态 `success`。

```sql
SELECT comprehensive_customer_value, user_value_score, predicted_clv_tier, predicted_ltv_tier, rfm_composite_score, customer_value_tier, is_valuable_user, lifecycle_stage, feature_adoption_rate
FROM pendo__customer_lifecycle_insights LIMIT 20
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-077/attempt-01/sql/S6.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-077/attempt-01/sql/S6.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-077/attempt-01/results/S6.rows.jsonl)；完整：True；SHA256：`dd11cb0e9b2ba6fe6fb51c8105db347f8eae5a00fbd657128f884738ad93c17e`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "pendo__customer_lifecycle_insights", "kind": "base", "block": null, "base_tables": ["pendo__customer_lifecycle_insights"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |


## S7

类别 `data`；来源 `query_db`；调用 `ca8bdeea696f47c9b0e0cf0ba86e560f`；状态 `success`。

```sql
SELECT
  COUNT(*) AS total_vf,
  COUNT(DISTINCT visitor_id) AS n_visitors_used,
  COUNT(DISTINCT feature_id) AS n_features_used
FROM pendo__visitor_feature
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-077/attempt-01/sql/S7.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-077/attempt-01/sql/S7.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-077/attempt-01/results/S7.rows.jsonl)；完整：True；SHA256：`fe71d321d1d21de6d03278e94c93670071dd3e810ba2189643a602c3d9ffe11b`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "pendo__visitor_feature", "kind": "base", "block": null, "base_tables": ["pendo__visitor_feature"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |
| B1 | COUNT(DISTINCT visitor_id) | [{"table": "pendo__visitor_feature", "column": "visitor_id"}] | [] | False |
| B1 | COUNT(DISTINCT feature_id) | [{"table": "pendo__visitor_feature", "column": "feature_id"}] | [] | False |


## S8

类别 `data`；来源 `query_db`；调用 `23a36345430d45a1960c73babffc9fbb`；状态 `success`。

```sql
SELECT
  MIN(comprehensive_customer_value) AS min_ccv,
  MAX(comprehensive_customer_value) AS max_ccv,
  AVG(comprehensive_customer_value) AS avg_ccv,
  MIN(user_value_score) AS min_uvs,
  MAX(user_value_score) AS max_uvs,
  AVG(user_value_score) AS avg_uvs,
  COUNT(*) AS n,
  COUNT(DISTINCT predicted_clv_tier) AS n_tiers
FROM pendo__customer_lifecycle_insights
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-077/attempt-01/sql/S8.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-077/attempt-01/sql/S8.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-077/attempt-01/results/S8.rows.jsonl)；完整：True；SHA256：`5a69529215822d05d7df068cd94871f088793bd66d6231759f8cceb9a424a9ec`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "pendo__customer_lifecycle_insights", "kind": "base", "block": null, "base_tables": ["pendo__customer_lifecycle_insights"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | MIN(comprehensive_customer_value) | [{"table": "pendo__customer_lifecycle_insights", "column": "comprehensive_customer_value"}] | [] | False |
| B1 | MAX(comprehensive_customer_value) | [{"table": "pendo__customer_lifecycle_insights", "column": "comprehensive_customer_value"}] | [] | False |
| B1 | AVG(comprehensive_customer_value) | [{"table": "pendo__customer_lifecycle_insights", "column": "comprehensive_customer_value"}] | [] | False |
| B1 | MIN(user_value_score) | [{"table": "pendo__customer_lifecycle_insights", "column": "user_value_score"}] | [] | False |
| B1 | MAX(user_value_score) | [{"table": "pendo__customer_lifecycle_insights", "column": "user_value_score"}] | [] | False |
| B1 | AVG(user_value_score) | [{"table": "pendo__customer_lifecycle_insights", "column": "user_value_score"}] | [] | False |
| B1 | COUNT(*) | [] | [] | True |
| B1 | COUNT(DISTINCT predicted_clv_tier) | [{"table": "pendo__customer_lifecycle_insights", "column": "predicted_clv_tier"}] | [] | False |


## S9

类别 `data`；来源 `query_db`；调用 `26441cdec8f64a9d9610979622629a94`；状态 `success`。

```sql
SELECT
  SUM(CASE WHEN predicted_clv_tier IS NULL THEN 1 ELSE 0 END) AS clv_tier_null,
  SUM(CASE WHEN predicted_ltv_tier IS NULL THEN 1 ELSE 0 END) AS ltv_tier_null,
  SUM(CASE WHEN rfm_composite_score IS NULL THEN 1 ELSE 0 END) AS rfm_null,
  SUM(CASE WHEN customer_value_tier IS NULL THEN 1 ELSE 0 END) AS cvtier_null,
  SUM(CASE WHEN is_valuable_user IS NULL THEN 1 ELSE 0 END) AS valuable_null,
  SUM(CASE WHEN comprehensive_customer_value IS NULL THEN 1 ELSE 0 END) AS ccv_null,
  SUM(CASE WHEN user_value_score IS NULL THEN 1 ELSE 0 END) AS uvs_null
FROM pendo__customer_lifecycle_insights
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-077/attempt-01/sql/S9.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-077/attempt-01/sql/S9.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-077/attempt-01/results/S9.rows.jsonl)；完整：True；SHA256：`1d86e7720c28e8ee36c3a817b662fe59171a501d2a31aad6e21820422851e908`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "pendo__customer_lifecycle_insights", "kind": "base", "block": null, "base_tables": ["pendo__customer_lifecycle_insights"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | SUM(CASE WHEN predicted_clv_tier IS NULL THEN 1 ELSE 0 END) | [] | [{"table": "pendo__customer_lifecycle_insights", "column": "predicted_clv_tier"}] | False |
| B1 | SUM(CASE WHEN predicted_ltv_tier IS NULL THEN 1 ELSE 0 END) | [] | [{"table": "pendo__customer_lifecycle_insights", "column": "predicted_ltv_tier"}] | False |
| B1 | SUM(CASE WHEN rfm_composite_score IS NULL THEN 1 ELSE 0 END) | [] | [{"table": "pendo__customer_lifecycle_insights", "column": "rfm_composite_score"}] | False |
| B1 | SUM(CASE WHEN customer_value_tier IS NULL THEN 1 ELSE 0 END) | [] | [{"table": "pendo__customer_lifecycle_insights", "column": "customer_value_tier"}] | False |
| B1 | SUM(CASE WHEN is_valuable_user IS NULL THEN 1 ELSE 0 END) | [] | [{"table": "pendo__customer_lifecycle_insights", "column": "is_valuable_user"}] | False |
| B1 | SUM(CASE WHEN comprehensive_customer_value IS NULL THEN 1 ELSE 0 END) | [] | [{"table": "pendo__customer_lifecycle_insights", "column": "comprehensive_customer_value"}] | False |
| B1 | SUM(CASE WHEN user_value_score IS NULL THEN 1 ELSE 0 END) | [] | [{"table": "pendo__customer_lifecycle_insights", "column": "user_value_score"}] | False |


## S10

类别 `data`；来源 `query_db`；调用 `5eaf93d717b04f6fa9684948c8df36a2`；状态 `success`。

```sql
SELECT f.feature_id, f.feature_name, f.count_visitors AS feat_tbl_visitors,
       COUNT(vf.visitor_id) AS vf_rows, COUNT(DISTINCT vf.visitor_id) AS vf_distinct_visitors,
       SUM(vf.sum_clicks) AS vf_clicks
FROM pendo__feature f
LEFT JOIN pendo__visitor_feature vf ON vf.feature_id = f.feature_id
GROUP BY f.feature_id
ORDER BY f.count_visitors DESC
LIMIT 15
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-077/attempt-01/sql/S10.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-077/attempt-01/sql/S10.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-077/attempt-01/results/S10.rows.jsonl)；完整：True；SHA256：`cd30fb635553903bfdd3e9114be1fb6901f8de9fe0bcb18132d8ae2077f95e5c`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "f", "kind": "base", "block": null, "base_tables": ["pendo__feature"]}, {"alias": "vf", "kind": "base", "block": null, "base_tables": ["pendo__visitor_feature"]}] | [{"type": "LEFT", "right": "pendo__visitor_feature AS vf", "on": "vf.feature_id = f.feature_id", "using": []}] | ["f.feature_id"] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(vf.visitor_id) | [{"table": "pendo__visitor_feature", "column": "visitor_id"}] | [] | False |
| B1 | COUNT(DISTINCT vf.visitor_id) | [{"table": "pendo__visitor_feature", "column": "visitor_id"}] | [] | False |
| B1 | SUM(vf.sum_clicks) | [{"table": "pendo__visitor_feature", "column": "sum_clicks"}] | [] | False |


## S11

类别 `data`；来源 `query_db`；调用 `e5202d91b6a741debf16f202b9d482eb`；状态 `success`。

```sql
SELECT COUNT(DISTINCT visitor_id) AS n_vf_visitors, COUNT(DISTINCT feature_id) AS n_vf_features FROM pendo__visitor_feature
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-077/attempt-01/sql/S11.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-077/attempt-01/sql/S11.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-077/attempt-01/results/S11.rows.jsonl)；完整：True；SHA256：`eb5ec47474ea024bcdeee00bc9e5d665a86c04115d4132494e258015e9acdbe1`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "pendo__visitor_feature", "kind": "base", "block": null, "base_tables": ["pendo__visitor_feature"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(DISTINCT visitor_id) | [{"table": "pendo__visitor_feature", "column": "visitor_id"}] | [] | False |
| B1 | COUNT(DISTINCT feature_id) | [{"table": "pendo__visitor_feature", "column": "feature_id"}] | [] | False |


## S12

类别 `data`；来源 `query_db`；调用 `d880147393ac4cf89cf32707b93d833a`；状态 `success`。

```sql
SELECT f.feature_id, f.feature_name, f.count_visitors
FROM pendo__feature f
ORDER BY f.count_visitors ASC
LIMIT 20
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-077/attempt-01/sql/S12.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-077/attempt-01/sql/S12.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-077/attempt-01/results/S12.rows.jsonl)；完整：True；SHA256：`97eb5c11e709f51a30f8170a83e060f30bca18dd42e00fe032e2bd04aa522303`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "f", "kind": "base", "block": null, "base_tables": ["pendo__feature"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |


## S13

类别 `data`；来源 `query_db`；调用 `d078e338909741cc9730b5a59ea54723`；状态 `success`。

```sql
SELECT
  feature_id,
  feature_name,
  COUNT(DISTINCT strftime('%Y-%m', date_day)) AS n_months,
  AVG(count_visitors) AS avg_daily_visitors,
  MAX(count_visitors) AS max_daily_visitors,
  SUM(count_visitors) AS sum_daily_visitors
FROM pendo__feature_daily_metrics
GROUP BY feature_id
ORDER BY avg_daily_visitors ASC
LIMIT 20
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-077/attempt-01/sql/S13.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-077/attempt-01/sql/S13.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-077/attempt-01/results/S13.rows.jsonl)；完整：True；SHA256：`cb92ae6917f3ef7caa8ffe1a2e5d7c49bcb51749425fe886d9fb08edb764cf07`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "pendo__feature_daily_metrics", "kind": "base", "block": null, "base_tables": ["pendo__feature_daily_metrics"]}] | [] | ["feature_id"] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(DISTINCT STRFTIME('%Y-%m', date_day)) | [{"table": "pendo__feature_daily_metrics", "column": "date_day"}] | [] | False |
| B1 | AVG(count_visitors) | [{"table": "pendo__feature_daily_metrics", "column": "count_visitors"}] | [] | False |
| B1 | MAX(count_visitors) | [{"table": "pendo__feature_daily_metrics", "column": "count_visitors"}] | [] | False |
| B1 | SUM(count_visitors) | [{"table": "pendo__feature_daily_metrics", "column": "count_visitors"}] | [] | False |


## S14

类别 `data`；来源 `query_db`；调用 `0a8de4fab6934b33aaf894f16bfff60b`；状态 `failed`。

```sql
SELECT
  s.strftime_Y_m AS month,
  COUNT(DISTINCT date_day) AS days_in_month
FROM (
  SELECT DISTINCT strftime('%Y-%m', date_day) AS strftime_Y_m
  FROM pendo__feature_daily_metrics
) s
GROUP BY s.strftime_Y_m
ORDER BY s.strftime_Y_m
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-077/attempt-01/sql/S14.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-077/attempt-01/sql/S14.parameters.json)。

错误：`OperationalError('no such column: date_day')`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "pendo__feature_daily_metrics", "kind": "base", "block": null, "base_tables": ["pendo__feature_daily_metrics"]}] | [] | [] |
| B2 | [{"alias": "s", "kind": "derived", "block": "B1", "base_tables": ["pendo__feature_daily_metrics"]}] | [] | ["s.strftime_Y_m"] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B2 | COUNT(DISTINCT date_day) | [{"unknown": "date_day"}] | [] | False |


未解析列血缘：[{"block": "B2", "column": "date_day", "reason": "ambiguous_or_missing_source"}, {"block": "B2", "column": "date_day", "reason": "ambiguous_or_missing_source"}]

## S15

类别 `data`；来源 `query_db`；调用 `e4f2517bce9747158b352f3555d49f4c`；状态 `success`。

```sql
SELECT DISTINCT strftime('%Y-%m', date_day) AS month
FROM pendo__feature_daily_metrics
ORDER BY month
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-077/attempt-01/sql/S15.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-077/attempt-01/sql/S15.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-077/attempt-01/results/S15.rows.jsonl)；完整：True；SHA256：`d23d306b1b3f550bca8b43279c645efac9f92ce0e9f60cc1b0373400ac2388e4`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "pendo__feature_daily_metrics", "kind": "base", "block": null, "base_tables": ["pendo__feature_daily_metrics"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |


## S16

类别 `data`；来源 `query_db`；调用 `c6efdfec328f4b649c8c3fe40134d926`；状态 `success`。

```sql
SELECT
  feature_id,
  feature_name,
  COUNT(DISTINCT strftime('%Y-%m', date_day)) AS n_months,
  AVG(count_visitors) AS avg_daily_visitors,
  MAX(count_visitors) AS max_daily_visitors,
  SUM(count_visitors) AS sum_daily_visitors
FROM pendo__feature_daily_metrics
GROUP BY feature_id
HAVING avg_daily_visitors < 200
ORDER BY avg_daily_visitors ASC
LIMIT 30
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-077/attempt-01/sql/S16.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-077/attempt-01/sql/S16.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-077/attempt-01/results/S16.rows.jsonl)；完整：True；SHA256：`126c8572f68806b138b70c0ddd8174805978447f0eba803944813e40af5a0a2a`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "pendo__feature_daily_metrics", "kind": "base", "block": null, "base_tables": ["pendo__feature_daily_metrics"]}] | [] | ["feature_id"] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(DISTINCT STRFTIME('%Y-%m', date_day)) | [{"table": "pendo__feature_daily_metrics", "column": "date_day"}] | [] | False |
| B1 | AVG(count_visitors) | [{"table": "pendo__feature_daily_metrics", "column": "count_visitors"}] | [] | False |
| B1 | MAX(count_visitors) | [{"table": "pendo__feature_daily_metrics", "column": "count_visitors"}] | [] | False |
| B1 | SUM(count_visitors) | [{"table": "pendo__feature_daily_metrics", "column": "count_visitors"}] | [] | False |


## S17

类别 `data`；来源 `query_db`；调用 `5d0a6135c71b4dd6afbc137895c4e927`；状态 `success`。

```sql
SELECT
  COUNT(*) AS n_features,
  SUM(CASE WHEN count_visitors < 200 THEN 1 ELSE 0 END) AS n_below_200,
  SUM(CASE WHEN count_visitors BETWEEN 200 AND 1000 THEN 1 ELSE 0 END) AS n_200_1000,
  SUM(CASE WHEN count_visitors > 1000 THEN 1 ELSE 0 END) AS n_above_1000,
  MIN(count_visitors) AS min_v, MAX(count_visitors) AS max_v, AVG(count_visitors) AS avg_v
FROM pendo__feature
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-077/attempt-01/sql/S17.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-077/attempt-01/sql/S17.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-077/attempt-01/results/S17.rows.jsonl)；完整：True；SHA256：`ffb82cbfccbe710d39ceeaec4cc505f20d727b86cba72c2f9cfe0a7deb66d7ab`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "pendo__feature", "kind": "base", "block": null, "base_tables": ["pendo__feature"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |
| B1 | SUM(CASE WHEN count_visitors < 200 THEN 1 ELSE 0 END) | [] | [{"table": "pendo__feature", "column": "count_visitors"}] | False |
| B1 | SUM(CASE WHEN count_visitors BETWEEN 200 AND 1000 THEN 1 ELSE 0 END) | [] | [{"table": "pendo__feature", "column": "count_visitors"}] | False |
| B1 | SUM(CASE WHEN count_visitors > 1000 THEN 1 ELSE 0 END) | [] | [{"table": "pendo__feature", "column": "count_visitors"}] | False |
| B1 | MIN(count_visitors) | [{"table": "pendo__feature", "column": "count_visitors"}] | [] | False |
| B1 | MAX(count_visitors) | [{"table": "pendo__feature", "column": "count_visitors"}] | [] | False |
| B1 | AVG(count_visitors) | [{"table": "pendo__feature", "column": "count_visitors"}] | [] | False |


## S18

类别 `data`；来源 `query_db`；调用 `74e9c4b4803d4fbb843b5c7b15872b0a`；状态 `success`。

```sql
SELECT COUNT(*) AS n_vf_clv_match FROM pendo__visitor_feature vf JOIN pendo__customer_lifecycle_insights c ON vf.visitor_id = c.visitor_id
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-077/attempt-01/sql/S18.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-077/attempt-01/sql/S18.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-077/attempt-01/results/S18.rows.jsonl)；完整：True；SHA256：`500ca01a1453a54dc6291ac2f5ff131fe1d4369e96ffe6ae348daff44911b63d`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "vf", "kind": "base", "block": null, "base_tables": ["pendo__visitor_feature"]}, {"alias": "c", "kind": "base", "block": null, "base_tables": ["pendo__customer_lifecycle_insights"]}] | [{"type": "INNER", "right": "pendo__customer_lifecycle_insights AS c", "on": "vf.visitor_id = c.visitor_id", "using": []}] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |


## S19

类别 `data`；来源 `query_db`；调用 `efb054c9125346c986343c6c4bb30296`；状态 `success`。

```sql
SELECT f.feature_id, f.feature_name, f.count_visitors, f.is_core_event, f.product_area_name
FROM pendo__feature f
WHERE f.count_visitors < 200
ORDER BY f.count_visitors DESC
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-077/attempt-01/sql/S19.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-077/attempt-01/sql/S19.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-077/attempt-01/results/S19.rows.jsonl)；完整：True；SHA256：`cd28bc75b87a33dcefac9b594bb433ca0922bd8b503b595c701f78acf2a63124`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "f", "kind": "base", "block": null, "base_tables": ["pendo__feature"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |


## S20

类别 `data`；来源 `query_db`；调用 `f9b877526e324155bcba32cefe419520`；状态 `success`。

```sql
SELECT
  c.visitor_id, c.comprehensive_customer_value, c.user_value_score, c.lifecycle_stage,
  c.churn_risk_level, c.engagement_trend, c.feature_adoption_rate
FROM pendo__customer_lifecycle_insights c
JOIN (SELECT DISTINCT visitor_id FROM pendo__visitor_feature) vf ON c.visitor_id = vf.visitor_id
LIMIT 10
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-077/attempt-01/sql/S20.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-077/attempt-01/sql/S20.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-077/attempt-01/results/S20.rows.jsonl)；完整：True；SHA256：`78c387756f2353fbec457e3638141b7cd378d8dec68677c9a7a000f286f725c5`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "pendo__visitor_feature", "kind": "base", "block": null, "base_tables": ["pendo__visitor_feature"]}] | [] | [] |
| B2 | [{"alias": "c", "kind": "base", "block": null, "base_tables": ["pendo__customer_lifecycle_insights"]}, {"alias": "vf", "kind": "derived", "block": "B1", "base_tables": ["pendo__visitor_feature"]}] | [{"type": "INNER", "right": "(SELECT DISTINCT visitor_id FROM pendo__visitor_feature) AS vf", "on": "c.visitor_id = vf.visitor_id", "using": []}] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |


## S21

类别 `data`；来源 `query_db`；调用 `840958d976584deaa41cd704aa7bf260`；状态 `success`。

```sql
SELECT
  AVG(comprehensive_customer_value) AS avg_ccv_all,
  MIN(comprehensive_customer_value) AS min_ccv_all,
  MAX(comprehensive_customer_value) AS max_ccv_all,
  (SELECT AVG(c2.comprehensive_customer_value) FROM pendo__customer_lifecycle_insights c2 JOIN (SELECT DISTINCT visitor_id FROM pendo__visitor_feature) vf2 ON c2.visitor_id = vf2.visitor_id) AS avg_ccv_tracked
FROM pendo__customer_lifecycle_insights
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-077/attempt-01/sql/S21.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-077/attempt-01/sql/S21.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-077/attempt-01/results/S21.rows.jsonl)；完整：True；SHA256：`e8872cb9ad2d050efc586c92b7c68bfbfd78979a577ce19edaa630409e7c12ac`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "pendo__visitor_feature", "kind": "base", "block": null, "base_tables": ["pendo__visitor_feature"]}] | [] | [] |
| B2 | [{"alias": "c2", "kind": "base", "block": null, "base_tables": ["pendo__customer_lifecycle_insights"]}, {"alias": "vf2", "kind": "derived", "block": "B1", "base_tables": ["pendo__visitor_feature"]}] | [{"type": "INNER", "right": "(SELECT DISTINCT visitor_id FROM pendo__visitor_feature) AS vf2", "on": "c2.visitor_id = vf2.visitor_id", "using": []}] | [] |
| B3 | [{"alias": "pendo__customer_lifecycle_insights", "kind": "base", "block": null, "base_tables": ["pendo__customer_lifecycle_insights"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B2 | AVG(c2.comprehensive_customer_value) | [{"table": "pendo__customer_lifecycle_insights", "column": "comprehensive_customer_value"}] | [] | False |
| B3 | AVG(comprehensive_customer_value) | [{"table": "pendo__customer_lifecycle_insights", "column": "comprehensive_customer_value"}] | [] | False |
| B3 | MIN(comprehensive_customer_value) | [{"table": "pendo__customer_lifecycle_insights", "column": "comprehensive_customer_value"}] | [] | False |
| B3 | MAX(comprehensive_customer_value) | [{"table": "pendo__customer_lifecycle_insights", "column": "comprehensive_customer_value"}] | [] | False |


未解析列血缘：[{"block": "B2", "column": "visitor_id", "reason": "ambiguous_or_missing_source"}]

## S22

类别 `data`；来源 `query_db`；调用 `6e18dca7c4e54f8ca658f9c7d53ef6e2`；状态 `success`。

```sql
SELECT
  f.feature_id, f.feature_name, f.count_visitors,
  AVG(c.comprehensive_customer_value) AS avg_ccv_users,
  (SELECT AVG(c2.comprehensive_customer_value) FROM pendo__customer_lifecycle_insights c2 WHERE c2.visitor_id IN (SELECT DISTINCT visitor_id FROM pendo__visitor_feature) AND c2.visitor_id NOT IN (SELECT visitor_id FROM pendo__visitor_feature vf2 WHERE vf2.feature_id = f.feature_id)) AS avg_ccv_nonusers,
  COUNT(DISTINCT vf.visitor_id) AS n_users_in_vf
FROM pendo__feature f
JOIN pendo__visitor_feature vf ON vf.feature_id = f.feature_id
JOIN pendo__customer_lifecycle_insights c ON vf.visitor_id = c.visitor_id
GROUP BY f.feature_id
HAVING f.count_visitors < 200
ORDER BY (avg_ccv_users - avg_ccv_nonusers) DESC
LIMIT 20
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-077/attempt-01/sql/S22.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-077/attempt-01/sql/S22.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-077/attempt-01/results/S22.rows.jsonl)；完整：True；SHA256：`3dcf965268f24ae37e045f4567925925788a891f938262db04fdb3da6a227f5c`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "pendo__visitor_feature", "kind": "base", "block": null, "base_tables": ["pendo__visitor_feature"]}] | [] | [] |
| B2 | [{"alias": "vf2", "kind": "base", "block": null, "base_tables": ["pendo__visitor_feature"]}] | [] | [] |
| B3 | [{"alias": "c2", "kind": "base", "block": null, "base_tables": ["pendo__customer_lifecycle_insights"]}] | [] | [] |
| B4 | [{"alias": "f", "kind": "base", "block": null, "base_tables": ["pendo__feature"]}, {"alias": "vf", "kind": "base", "block": null, "base_tables": ["pendo__visitor_feature"]}, {"alias": "c", "kind": "base", "block": null, "base_tables": ["pendo__customer_lifecycle_insights"]}] | [{"type": "INNER", "right": "pendo__visitor_feature AS vf", "on": "vf.feature_id = f.feature_id", "using": []}, {"type": "INNER", "right": "pendo__customer_lifecycle_insights AS c", "on": "vf.visitor_id = c.visitor_id", "using": []}] | ["f.feature_id"] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B3 | AVG(c2.comprehensive_customer_value) | [{"table": "pendo__customer_lifecycle_insights", "column": "comprehensive_customer_value"}] | [] | False |
| B4 | AVG(c.comprehensive_customer_value) | [{"table": "pendo__customer_lifecycle_insights", "column": "comprehensive_customer_value"}] | [] | False |
| B4 | COUNT(DISTINCT vf.visitor_id) | [{"table": "pendo__visitor_feature", "column": "visitor_id"}] | [] | False |


未解析列血缘：[{"block": "B4", "column": "visitor_id", "reason": "ambiguous_or_missing_source"}, {"block": "B4", "column": "visitor_id", "reason": "ambiguous_or_missing_source"}]

## S23

类别 `data`；来源 `query_db`；调用 `e246a6b5ca604c7d92c942d479ed760f`；状态 `success`。

```sql
SELECT f.feature_id, f.count_visitors,
  dm.month, SUM(dm.count_visitors) AS monthly_visitor_days,
  MAX(dm.count_visitors) AS max_daily_in_month
FROM pendo__feature f
JOIN (
  SELECT feature_id, strftime('%Y-%m', date_day) AS month, count_visitors
  FROM pendo__feature_daily_metrics
) dm ON dm.feature_id = f.feature_id
WHERE f.feature_id IN ('FEAT_00147','FEAT_00081','FEAT_00155','FEAT_00003','FEAT_00109')
GROUP BY f.feature_id, dm.month
ORDER BY f.feature_id, dm.month
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-077/attempt-01/sql/S23.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-077/attempt-01/sql/S23.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-077/attempt-01/results/S23.rows.jsonl)；完整：True；SHA256：`ebc80a2651bda9663123645de98e2c97b39d6baedede764900bac7076eead0b4`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "pendo__feature_daily_metrics", "kind": "base", "block": null, "base_tables": ["pendo__feature_daily_metrics"]}] | [] | [] |
| B2 | [{"alias": "f", "kind": "base", "block": null, "base_tables": ["pendo__feature"]}, {"alias": "dm", "kind": "derived", "block": "B1", "base_tables": ["pendo__feature_daily_metrics"]}] | [{"type": "INNER", "right": "(SELECT feature_id, STRFTIME('%Y-%m', date_day) AS month, count_visitors FROM pendo__feature_daily_metrics) AS dm", "on": "dm.feature_id = f.feature_id", "using": []}] | ["f.feature_id", "dm.month"] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B2 | SUM(dm.count_visitors) | [{"table": "pendo__feature_daily_metrics", "column": "count_visitors"}] | [] | False |
| B2 | MAX(dm.count_visitors) | [{"table": "pendo__feature_daily_metrics", "column": "count_visitors"}] | [] | False |


## S24

类别 `data`；来源 `query_db`；调用 `85cabe0961ae4035a49070bb39bec017`；状态 `success`。

```sql
SELECT COUNT(*) AS n, SUM(CASE WHEN first_click_at IS NOT NULL THEN 1 ELSE 0 END) AS has_first_click,
  SUM(CASE WHEN last_click_at IS NOT NULL THEN 1 ELSE 0 END) AS has_last_click
FROM pendo__visitor_feature
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-077/attempt-01/sql/S24.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-077/attempt-01/sql/S24.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-077/attempt-01/results/S24.rows.jsonl)；完整：True；SHA256：`dbfc9a231881a3206f62e179befa1b8379b3d8dadbb6e9ea37e1db8f6a576a21`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "pendo__visitor_feature", "kind": "base", "block": null, "base_tables": ["pendo__visitor_feature"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |
| B1 | SUM(CASE WHEN NOT first_click_at IS NULL THEN 1 ELSE 0 END) | [] | [{"table": "pendo__visitor_feature", "column": "first_click_at"}] | False |
| B1 | SUM(CASE WHEN NOT last_click_at IS NULL THEN 1 ELSE 0 END) | [] | [{"table": "pendo__visitor_feature", "column": "last_click_at"}] | False |


## S25

类别 `data`；来源 `query_db`；调用 `91d2f29303fc44e29e04ee40172c0cfd`；状态 `cancelled`。

```sql
-- Compute for each feature: avg CCV of users vs non-users, and usage stats
WITH tracked_visitors AS (
  SELECT DISTINCT visitor_id FROM pendo__visitor_feature
),
feature_usage AS (
  SELECT
    f.feature_id,
    f.feature_name,
    f.count_visitors AS total_visitors,
    f.product_area_name,
    f.is_core_event,
    f.page_name
  FROM pendo__feature f
),
user_clv AS (
  SELECT
    c.visitor_id,
    c.comprehensive_customer_value,
    c.user_value_score,
    c.feature_adoption_rate,
    c.lifecycle_stage,
    c.overall_health_score
  FROM pendo__customer_lifecycle_insights c
  JOIN tracked_visitors tv ON c.visitor_id = tv.visitor_id
),
feature_impact AS (
  SELECT
    fu.feature_id,
    fu.feature_name,
    fu.total_visitors,
    fu.product_area_name,
    fu.is_core_event,
    fu.page_name,
    vf.visitor_id
  FROM feature_usage fu
  LEFT JOIN pendo__visitor_feature vf ON vf.feature_id = fu.feature_id
)
SELECT
  fi.feature_id,
  fi.feature_name,
  fi.total_visitors,
  fi.product_area_name,
  fi.is_core_event,
  fi.page_name,
  COUNT(DISTINCT fi.visitor_id) AS n_tracked_users,
  AVG(uc.comprehensive_customer_value) AS avg_ccv_users,
  (SELECT AVG(uc2.comprehensive_customer_value) FROM user_clv uc2
   WHERE uc2.visitor_id NOT IN (SELECT vf2.visitor_id FROM pendo__visitor_feature vf2 WHERE vf2.feature_id = fi.feature_id)
  ) AS avg_ccv_nonusers,
  (SELECT COUNT(*) FROM user_clv) AS n_tracked_total
FROM feature_impact fi
LEFT JOIN user_clv uc ON fi.visitor_id = uc.visitor_id
GROUP BY fi.feature_id
ORDER BY (avg_ccv_users - avg_ccv_nonusers) DESC
LIMIT 50
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-077/attempt-01/sql/S25.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-077/attempt-01/sql/S25.parameters.json)。

错误：`OperationalError('interrupted')`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "pendo__visitor_feature", "kind": "base", "block": null, "base_tables": ["pendo__visitor_feature"]}] | [] | [] |
| B2 | [{"alias": "f", "kind": "base", "block": null, "base_tables": ["pendo__feature"]}] | [] | [] |
| B3 | [{"alias": "c", "kind": "base", "block": null, "base_tables": ["pendo__customer_lifecycle_insights"]}, {"alias": "tv", "kind": "derived", "block": "B1", "base_tables": ["pendo__visitor_feature"]}] | [{"type": "INNER", "right": "tracked_visitors AS tv", "on": "c.visitor_id = tv.visitor_id", "using": []}] | [] |
| B4 | [{"alias": "fu", "kind": "derived", "block": "B2", "base_tables": ["pendo__feature"]}, {"alias": "vf", "kind": "base", "block": null, "base_tables": ["pendo__visitor_feature"]}] | [{"type": "LEFT", "right": "pendo__visitor_feature AS vf", "on": "vf.feature_id = fu.feature_id", "using": []}] | [] |
| B5 | [{"alias": "vf2", "kind": "base", "block": null, "base_tables": ["pendo__visitor_feature"]}] | [] | [] |
| B6 | [{"alias": "uc2", "kind": "derived", "block": "B3", "base_tables": ["pendo__customer_lifecycle_insights", "pendo__visitor_feature"]}] | [] | [] |
| B7 | [{"alias": "user_clv", "kind": "derived", "block": "B3", "base_tables": ["pendo__customer_lifecycle_insights", "pendo__visitor_feature"]}] | [] | [] |
| B8 | [{"alias": "fi", "kind": "derived", "block": "B4", "base_tables": ["pendo__feature", "pendo__visitor_feature"]}, {"alias": "uc", "kind": "derived", "block": "B3", "base_tables": ["pendo__customer_lifecycle_insights", "pendo__visitor_feature"]}] | [{"type": "LEFT", "right": "user_clv AS uc", "on": "fi.visitor_id = uc.visitor_id", "using": []}] | ["fi.feature_id"] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B6 | AVG(uc2.comprehensive_customer_value) | [{"table": "pendo__customer_lifecycle_insights", "column": "comprehensive_customer_value"}] | [] | False |
| B7 | COUNT(*) | [] | [] | True |
| B8 | COUNT(DISTINCT fi.visitor_id) | [{"table": "pendo__visitor_feature", "column": "visitor_id"}] | [] | False |
| B8 | AVG(uc.comprehensive_customer_value) | [{"table": "pendo__customer_lifecycle_insights", "column": "comprehensive_customer_value"}] | [] | False |


## S26

类别 `data`；来源 `query_db`；调用 `27594c93eef3422690f460cbcdd2adef`；状态 `success`。

```sql
WITH tracked_visitors AS (
  SELECT DISTINCT visitor_id FROM pendo__visitor_feature
),
base AS (
  SELECT AVG(c.comprehensive_customer_value) AS avg_ccv_overall,
         COUNT(*) AS n_tracked
  FROM pendo__customer_lifecycle_insights c
  JOIN tracked_visitors tv ON c.visitor_id = tv.visitor_id
)
SELECT
  f.feature_id,
  f.feature_name,
  f.count_visitors AS total_visitors,
  f.product_area_name,
  f.is_core_event,
  COUNT(DISTINCT vf.visitor_id) AS n_tracked_users,
  AVG(c.comprehensive_customer_value) AS avg_ccv_users,
  (SELECT avg_ccv_overall FROM base) AS avg_ccv_overall,
  (SELECT n_tracked FROM base) AS n_tracked
FROM pendo__feature f
LEFT JOIN pendo__visitor_feature vf ON vf.feature_id = f.feature_id
LEFT JOIN pendo__customer_lifecycle_insights c ON vf.visitor_id = c.visitor_id
GROUP BY f.feature_id
ORDER BY (AVG(c.comprehensive_customer_value) - (SELECT avg_ccv_overall FROM base)) DESC
LIMIT 60
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-077/attempt-01/sql/S26.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-077/attempt-01/sql/S26.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-077/attempt-01/results/S26.rows.jsonl)；完整：True；SHA256：`e14c4cfa491ae51b0882e1b5a51bc4d350869089166ef23821ace347ef48a5da`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "pendo__visitor_feature", "kind": "base", "block": null, "base_tables": ["pendo__visitor_feature"]}] | [] | [] |
| B2 | [{"alias": "c", "kind": "base", "block": null, "base_tables": ["pendo__customer_lifecycle_insights"]}, {"alias": "tv", "kind": "derived", "block": "B1", "base_tables": ["pendo__visitor_feature"]}] | [{"type": "INNER", "right": "tracked_visitors AS tv", "on": "c.visitor_id = tv.visitor_id", "using": []}] | [] |
| B3 | [{"alias": "base", "kind": "derived", "block": "B2", "base_tables": ["pendo__customer_lifecycle_insights", "pendo__visitor_feature"]}] | [] | [] |
| B4 | [{"alias": "base", "kind": "derived", "block": "B2", "base_tables": ["pendo__customer_lifecycle_insights", "pendo__visitor_feature"]}] | [] | [] |
| B5 | [{"alias": "base", "kind": "derived", "block": "B2", "base_tables": ["pendo__customer_lifecycle_insights", "pendo__visitor_feature"]}] | [] | [] |
| B6 | [{"alias": "f", "kind": "base", "block": null, "base_tables": ["pendo__feature"]}, {"alias": "vf", "kind": "base", "block": null, "base_tables": ["pendo__visitor_feature"]}, {"alias": "c", "kind": "base", "block": null, "base_tables": ["pendo__customer_lifecycle_insights"]}] | [{"type": "LEFT", "right": "pendo__visitor_feature AS vf", "on": "vf.feature_id = f.feature_id", "using": []}, {"type": "LEFT", "right": "pendo__customer_lifecycle_insights AS c", "on": "vf.visitor_id = c.visitor_id", "using": []}] | ["f.feature_id"] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B2 | AVG(c.comprehensive_customer_value) | [{"table": "pendo__customer_lifecycle_insights", "column": "comprehensive_customer_value"}] | [] | False |
| B2 | COUNT(*) | [] | [] | True |
| B6 | COUNT(DISTINCT vf.visitor_id) | [{"table": "pendo__visitor_feature", "column": "visitor_id"}] | [] | False |
| B6 | AVG(c.comprehensive_customer_value) | [{"table": "pendo__customer_lifecycle_insights", "column": "comprehensive_customer_value"}] | [] | False |
| B6 | AVG(c.comprehensive_customer_value) | [{"table": "pendo__customer_lifecycle_insights", "column": "comprehensive_customer_value"}] | [] | False |


## S27

类别 `data`；来源 `query_db`；调用 `b2ae97353896470c87da0a7882670cdf`；状态 `success`。

```sql
-- Compute ALL features with avg CCV for users and non-users
WITH tracked AS (
  SELECT DISTINCT visitor_id FROM pendo__visitor_feature
),
base_clv AS (
  SELECT c.visitor_id, c.comprehensive_customer_value
  FROM pendo__customer_lifecycle_insights c
  JOIN tracked t ON c.visitor_id = t.visitor_id
)
SELECT
  f.feature_id,
  f.feature_name,
  f.count_visitors AS total_visitors,
  f.product_area_name,
  f.is_core_event,
  COUNT(DISTINCT vf.visitor_id) AS n_tracked_users,
  AVG(CASE WHEN vf.visitor_id IS NOT NULL THEN bc.comprehensive_customer_value END) AS avg_ccv_users,
  AVG(CASE WHEN vf.visitor_id IS NULL THEN bc.comprehensive_customer_value END) AS avg_ccv_nonusers,
  (SELECT COUNT(*) FROM base_clv) AS n_tracked_total
FROM pendo__feature f
CROSS JOIN base_clv bc
LEFT JOIN pendo__visitor_feature vf ON vf.feature_id = f.feature_id AND vf.visitor_id = bc.visitor_id
GROUP BY f.feature_id
ORDER BY (AVG(CASE WHEN vf.visitor_id IS NOT NULL THEN bc.comprehensive_customer_value END) - AVG(CASE WHEN vf.visitor_id IS NULL THEN bc.comprehensive_customer_value END)) DESC
LIMIT 60
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-077/attempt-01/sql/S27.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-077/attempt-01/sql/S27.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-077/attempt-01/results/S27.rows.jsonl)；完整：True；SHA256：`e7be66a501e5aabbc166d7733ae902a16ee1827fbd84f45632192dcfdd4a5a7b`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "pendo__visitor_feature", "kind": "base", "block": null, "base_tables": ["pendo__visitor_feature"]}] | [] | [] |
| B2 | [{"alias": "c", "kind": "base", "block": null, "base_tables": ["pendo__customer_lifecycle_insights"]}, {"alias": "t", "kind": "derived", "block": "B1", "base_tables": ["pendo__visitor_feature"]}] | [{"type": "INNER", "right": "tracked AS t", "on": "c.visitor_id = t.visitor_id", "using": []}] | [] |
| B3 | [{"alias": "base_clv", "kind": "derived", "block": "B2", "base_tables": ["pendo__customer_lifecycle_insights", "pendo__visitor_feature"]}] | [] | [] |
| B4 | [{"alias": "f", "kind": "base", "block": null, "base_tables": ["pendo__feature"]}, {"alias": "bc", "kind": "derived", "block": "B2", "base_tables": ["pendo__customer_lifecycle_insights", "pendo__visitor_feature"]}, {"alias": "vf", "kind": "base", "block": null, "base_tables": ["pendo__visitor_feature"]}] | [{"type": "CROSS", "right": "base_clv AS bc", "on": null, "using": []}, {"type": "LEFT", "right": "pendo__visitor_feature AS vf", "on": "vf.feature_id = f.feature_id AND vf.visitor_id = bc.visitor_id", "using": []}] | ["f.feature_id"] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B3 | COUNT(*) | [] | [] | True |
| B4 | COUNT(DISTINCT vf.visitor_id) | [{"table": "pendo__visitor_feature", "column": "visitor_id"}] | [] | False |
| B4 | AVG(CASE WHEN NOT vf.visitor_id IS NULL THEN bc.comprehensive_customer_value END) | [{"table": "pendo__customer_lifecycle_insights", "column": "comprehensive_customer_value"}] | [{"table": "pendo__visitor_feature", "column": "visitor_id"}] | False |
| B4 | AVG(CASE WHEN vf.visitor_id IS NULL THEN bc.comprehensive_customer_value END) | [{"table": "pendo__customer_lifecycle_insights", "column": "comprehensive_customer_value"}] | [{"table": "pendo__visitor_feature", "column": "visitor_id"}] | False |
| B4 | AVG(CASE WHEN NOT vf.visitor_id IS NULL THEN bc.comprehensive_customer_value END) | [{"table": "pendo__customer_lifecycle_insights", "column": "comprehensive_customer_value"}] | [{"table": "pendo__visitor_feature", "column": "visitor_id"}] | False |
| B4 | AVG(CASE WHEN vf.visitor_id IS NULL THEN bc.comprehensive_customer_value END) | [{"table": "pendo__customer_lifecycle_insights", "column": "comprehensive_customer_value"}] | [{"table": "pendo__visitor_feature", "column": "visitor_id"}] | False |


## S28

类别 `data`；来源 `query_db`；调用 `bd09306991ea41df91e7ca78fa4982c4`；状态 `success`。

```sql
SELECT
  f.feature_id,
  f.feature_name,
  f.count_visitors AS total_visitors,
  f.product_area_name,
  f.is_core_event,
  f.count_accounts,
  f.sum_clicks,
  COUNT(DISTINCT vf.visitor_id) AS n_tracked_users,
  AVG(CASE WHEN vf.visitor_id IS NOT NULL THEN bc.comprehensive_customer_value END) AS avg_ccv_users,
  AVG(CASE WHEN vf.visitor_id IS NULL THEN bc.comprehensive_customer_value END) AS avg_ccv_nonusers,
  COUNT(CASE WHEN vf.visitor_id IS NOT NULL THEN 1 END) AS n_user_obs,
  COUNT(CASE WHEN vf.visitor_id IS NULL THEN 1 END) AS n_nonuser_obs
FROM pendo__feature f
CROSS JOIN (
  SELECT c.visitor_id, c.comprehensive_customer_value
  FROM pendo__customer_lifecycle_insights c
  JOIN (SELECT DISTINCT visitor_id FROM pendo__visitor_feature) t ON c.visitor_id = t.visitor_id
) bc
LEFT JOIN pendo__visitor_feature vf ON vf.feature_id = f.feature_id AND vf.visitor_id = bc.visitor_id
GROUP BY f.feature_id
ORDER BY f.feature_id
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-077/attempt-01/sql/S28.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-077/attempt-01/sql/S28.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-077/attempt-01/results/S28.rows.jsonl)；完整：True；SHA256：`6012a64bd08778fb547d48a9245ecf3ad31c5c2724d65784ca1f49d003e8dc41`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "pendo__visitor_feature", "kind": "base", "block": null, "base_tables": ["pendo__visitor_feature"]}] | [] | [] |
| B2 | [{"alias": "c", "kind": "base", "block": null, "base_tables": ["pendo__customer_lifecycle_insights"]}, {"alias": "t", "kind": "derived", "block": "B1", "base_tables": ["pendo__visitor_feature"]}] | [{"type": "INNER", "right": "(SELECT DISTINCT visitor_id FROM pendo__visitor_feature) AS t", "on": "c.visitor_id = t.visitor_id", "using": []}] | [] |
| B3 | [{"alias": "f", "kind": "base", "block": null, "base_tables": ["pendo__feature"]}, {"alias": "bc", "kind": "derived", "block": "B2", "base_tables": ["pendo__customer_lifecycle_insights", "pendo__visitor_feature"]}, {"alias": "vf", "kind": "base", "block": null, "base_tables": ["pendo__visitor_feature"]}] | [{"type": "CROSS", "right": "(SELECT c.visitor_id, c.comprehensive_customer_value FROM pendo__customer_lifecycle_insights AS c JOIN (SELECT DISTINCT visitor_id FROM pendo__visitor_feature) AS t ON c.visitor_id = t.visitor_id) AS bc", "on": null, "using": []}, {"type": "LEFT", "right": "pendo__visitor_feature AS vf", "on": "vf.feature_id = f.feature_id AND vf.visitor_id = bc.visitor_id", "using": []}] | ["f.feature_id"] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B3 | COUNT(DISTINCT vf.visitor_id) | [{"table": "pendo__visitor_feature", "column": "visitor_id"}] | [] | False |
| B3 | AVG(CASE WHEN NOT vf.visitor_id IS NULL THEN bc.comprehensive_customer_value END) | [{"table": "pendo__customer_lifecycle_insights", "column": "comprehensive_customer_value"}] | [{"table": "pendo__visitor_feature", "column": "visitor_id"}] | False |
| B3 | AVG(CASE WHEN vf.visitor_id IS NULL THEN bc.comprehensive_customer_value END) | [{"table": "pendo__customer_lifecycle_insights", "column": "comprehensive_customer_value"}] | [{"table": "pendo__visitor_feature", "column": "visitor_id"}] | False |
| B3 | COUNT(CASE WHEN NOT vf.visitor_id IS NULL THEN 1 END) | [] | [{"table": "pendo__visitor_feature", "column": "visitor_id"}] | False |
| B3 | COUNT(CASE WHEN vf.visitor_id IS NULL THEN 1 END) | [] | [{"table": "pendo__visitor_feature", "column": "visitor_id"}] | False |


## S29

类别 `data`；来源 `query_db`；调用 `5dc4036f40b14fff8939e0da380de8a4`；状态 `success`。

```sql
SELECT c.visitor_id, c.comprehensive_customer_value, c.user_value_score
FROM pendo__customer_lifecycle_insights c
JOIN (SELECT DISTINCT visitor_id FROM pendo__visitor_feature) t ON c.visitor_id = t.visitor_id
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-077/attempt-01/sql/S29.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-077/attempt-01/sql/S29.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-077/attempt-01/results/S29.rows.jsonl)；完整：True；SHA256：`6c96bec008955cd095320d8580e1e4be4fc42484e0d6ea94c02fe57733c55b23`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "pendo__visitor_feature", "kind": "base", "block": null, "base_tables": ["pendo__visitor_feature"]}] | [] | [] |
| B2 | [{"alias": "c", "kind": "base", "block": null, "base_tables": ["pendo__customer_lifecycle_insights"]}, {"alias": "t", "kind": "derived", "block": "B1", "base_tables": ["pendo__visitor_feature"]}] | [{"type": "INNER", "right": "(SELECT DISTINCT visitor_id FROM pendo__visitor_feature) AS t", "on": "c.visitor_id = t.visitor_id", "using": []}] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |


## S30

类别 `data`；来源 `query_db`；调用 `f60148d32d3b4d33b3b19ed2f818b17c`；状态 `success`。

```sql
SELECT visitor_id, feature_id, sum_clicks, count_active_days, count_click_events, sum_minutes
FROM pendo__visitor_feature
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-077/attempt-01/sql/S30.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-077/attempt-01/sql/S30.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-077/attempt-01/results/S30.rows.jsonl)；完整：True；SHA256：`d684d201b3eb6af39426519e6881f1ebe0ae8fb8b31d65437ff2ddfb92433e37`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "pendo__visitor_feature", "kind": "base", "block": null, "base_tables": ["pendo__visitor_feature"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |


## S31

类别 `data`；来源 `python`；调用 `4534a17d8d114d9bbc124e24d1ab6e3f`；状态 `success`。

```sql

SELECT c.visitor_id, c.comprehensive_customer_value, c.user_value_score
FROM pendo__customer_lifecycle_insights c
JOIN (SELECT DISTINCT visitor_id FROM pendo__visitor_feature) t ON c.visitor_id = t.visitor_id

```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-077/attempt-01/sql/S31.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-077/attempt-01/sql/S31.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-077/attempt-01/results/S31.rows.jsonl)；完整：True；SHA256：`6c96bec008955cd095320d8580e1e4be4fc42484e0d6ea94c02fe57733c55b23`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "pendo__visitor_feature", "kind": "base", "block": null, "base_tables": ["pendo__visitor_feature"]}] | [] | [] |
| B2 | [{"alias": "c", "kind": "base", "block": null, "base_tables": ["pendo__customer_lifecycle_insights"]}, {"alias": "t", "kind": "derived", "block": "B1", "base_tables": ["pendo__visitor_feature"]}] | [{"type": "INNER", "right": "(SELECT DISTINCT visitor_id FROM pendo__visitor_feature) AS t", "on": "c.visitor_id = t.visitor_id", "using": []}] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |


## S32

类别 `data`；来源 `python`；调用 `4534a17d8d114d9bbc124e24d1ab6e3f`；状态 `success`。

```sql

SELECT visitor_id, feature_id, sum_clicks, count_active_days, count_click_events, sum_minutes
FROM pendo__visitor_feature

```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-077/attempt-01/sql/S32.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-077/attempt-01/sql/S32.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-077/attempt-01/results/S32.rows.jsonl)；完整：True；SHA256：`d684d201b3eb6af39426519e6881f1ebe0ae8fb8b31d65437ff2ddfb92433e37`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "pendo__visitor_feature", "kind": "base", "block": null, "base_tables": ["pendo__visitor_feature"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |


## S33

类别 `data`；来源 `python`；调用 `4534a17d8d114d9bbc124e24d1ab6e3f`；状态 `success`。

```sql

SELECT feature_id, feature_name, count_visitors, count_accounts, product_area_name, is_core_event, sum_clicks
FROM pendo__feature

```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-077/attempt-01/sql/S33.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-077/attempt-01/sql/S33.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-077/attempt-01/results/S33.rows.jsonl)；完整：True；SHA256：`04927ef03ac89d13d746233da69e016700c266838be657e33bc555db1d539000`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "pendo__feature", "kind": "base", "block": null, "base_tables": ["pendo__feature"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |


## S34

类别 `data`；来源 `query_db`；调用 `751f19c180324a98a230dc420e9272eb`；状态 `success`。

```sql
SELECT
  f.feature_id,
  f.feature_name,
  f.count_visitors,
  ROUND(AVG(fdm.count_visitors), 1) AS avg_daily_visitors,
  ROUND(AVG(fdm.count_visitors) * 30.4, 1) AS est_monthly_visitors,
  f.product_area_name
FROM pendo__feature f
JOIN pendo__feature_daily_metrics fdm ON fdm.feature_id = f.feature_id
WHERE f.count_visitors < 300
GROUP BY f.feature_id
ORDER BY f.count_visitors DESC
LIMIT 30
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-077/attempt-01/sql/S34.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-077/attempt-01/sql/S34.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-077/attempt-01/results/S34.rows.jsonl)；完整：True；SHA256：`565e440a5c88534f36d96f2d2fe9de9e82f036cb72459a705ae0467e7f751428`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "f", "kind": "base", "block": null, "base_tables": ["pendo__feature"]}, {"alias": "fdm", "kind": "base", "block": null, "base_tables": ["pendo__feature_daily_metrics"]}] | [{"type": "INNER", "right": "pendo__feature_daily_metrics AS fdm", "on": "fdm.feature_id = f.feature_id", "using": []}] | ["f.feature_id"] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | AVG(fdm.count_visitors) | [{"table": "pendo__feature_daily_metrics", "column": "count_visitors"}] | [] | False |
| B1 | AVG(fdm.count_visitors) | [{"table": "pendo__feature_daily_metrics", "column": "count_visitors"}] | [] | False |


## S35

类别 `data`；来源 `query_db`；调用 `d6f72e7050534d508c8703986906ea35`；状态 `success`。

```sql
SELECT feature_id, feature_name, total_users_tried, avg_events_per_user, avg_minutes_per_user, avg_active_days_per_user, regular_users, casual_users
FROM pendo__product_adoption_analytics
WHERE feature_id IN ('FEAT_00155','FEAT_00003','FEAT_00109','FEAT_00121','FEAT_00085','FEAT_00137','FEAT_00036','FEAT_00163')
ORDER BY total_users_tried DESC
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-077/attempt-01/sql/S35.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-077/attempt-01/sql/S35.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-077/attempt-01/results/S35.rows.jsonl)；完整：True；SHA256：`0d79b40fe693c8c560781f5f0fa1d622093f1c23ce82b640b642e27be4292d6c`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "pendo__product_adoption_analytics", "kind": "base", "block": null, "base_tables": ["pendo__product_adoption_analytics"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |


## S36

类别 `data`；来源 `query_db`；调用 `2433bc24e87e48dfbf1f9dc3376e678f`；状态 `success`。

```sql
SELECT
  CASE WHEN count_visitors < 200 THEN '<200'
       WHEN count_visitors < 500 THEN '200-500'
       WHEN count_visitors < 1000 THEN '500-1000'
       ELSE '>=1000' END AS usage_band,
  COUNT(*) AS n_features
FROM pendo__feature
GROUP BY usage_band
ORDER BY MIN(count_visitors)
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-077/attempt-01/sql/S36.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-077/attempt-01/sql/S36.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-077/attempt-01/results/S36.rows.jsonl)；完整：True；SHA256：`ee884bcba8ebc15611b023de62aa9facc51b1d89e25b8b013528d8208ddcbf22`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "pendo__feature", "kind": "base", "block": null, "base_tables": ["pendo__feature"]}] | [] | ["CASE WHEN count_visitors < 200 THEN '<200' WHEN count_visitors < 500 THEN '200-500' WHEN count_visitors < 1000 THEN '500-1000' ELSE '>=1000' END"] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |
| B1 | MIN(count_visitors) | [{"table": "pendo__feature", "column": "count_visitors"}] | [] | False |


## S37

类别 `data`；来源 `query_db`；调用 `822ac114d25a4742926faddc644c327c`；状态 `success`。

```sql
SELECT f.feature_id, f.feature_name, f.count_visitors, a.total_users_tried, a.regular_users, a.casual_users, a.avg_active_days_per_user
FROM pendo__feature f
JOIN pendo__product_adoption_analytics a ON a.feature_id = f.feature_id
WHERE f.count_visitors < 200
ORDER BY f.count_visitors DESC
LIMIT 47
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-077/attempt-01/sql/S37.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-077/attempt-01/sql/S37.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-077/attempt-01/results/S37.rows.jsonl)；完整：True；SHA256：`1276a550ef0de1040390b7e280e6cb178e3c89cc9547d51b50cc0f34decccef1`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "f", "kind": "base", "block": null, "base_tables": ["pendo__feature"]}, {"alias": "a", "kind": "base", "block": null, "base_tables": ["pendo__product_adoption_analytics"]}] | [{"type": "INNER", "right": "pendo__product_adoption_analytics AS a", "on": "a.feature_id = f.feature_id", "using": []}] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |


## S38

类别 `data`；来源 `python`；调用 `d3a1cf693c474acbb58d39921bf54b99`；状态 `success`。

```sql

SELECT f.feature_id, f.count_visitors, a.total_users_tried, a.regular_users, a.casual_users, a.avg_active_days_per_user
FROM pendo__feature f
JOIN pendo__product_adoption_analytics a ON a.feature_id = f.feature_id

```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-077/attempt-01/sql/S38.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-077/attempt-01/sql/S38.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-077/attempt-01/results/S38.rows.jsonl)；完整：True；SHA256：`ec8fad528461f24166f6918dcfa30a8a0c5fcb6fbb47b94346ad973a34ec1ee1`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "f", "kind": "base", "block": null, "base_tables": ["pendo__feature"]}, {"alias": "a", "kind": "base", "block": null, "base_tables": ["pendo__product_adoption_analytics"]}] | [{"type": "INNER", "right": "pendo__product_adoption_analytics AS a", "on": "a.feature_id = f.feature_id", "using": []}] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |


## S39

类别 `data`；来源 `query_db`；调用 `51a71fe0a2de4bcd81d338c4f391d5bd`；状态 `success`。

```sql
WITH monthly AS (
  SELECT feature_id, strftime('%Y-%m', date_day) AS ym,
         MAX(count_visitors) AS max_daily_visitors,
         AVG(count_visitors) AS avg_daily_visitors,
         SUM(count_visitors) AS sum_daily_visitors
  FROM pendo__feature_daily_metrics
  GROUP BY feature_id, strftime('%Y-%m', date_day)
)
SELECT f.feature_id, f.feature_name, f.count_visitors,
       m.ym, m.max_daily_visitors, ROUND(m.avg_daily_visitors,1) AS avg_daily, m.sum_daily_visitors
FROM pendo__feature f
JOIN monthly m ON m.feature_id = f.feature_id
WHERE f.feature_id IN ('FEAT_00155','FEAT_00003','FEAT_00109','FEAT_00121','FEAT_00085')
ORDER BY f.feature_id, m.ym
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-077/attempt-01/sql/S39.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-077/attempt-01/sql/S39.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-077/attempt-01/results/S39.rows.jsonl)；完整：True；SHA256：`7d2d4b9f13dd0aa361c7658579baffe3b9184e8827e53fa1ac00a56de8f8040d`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "pendo__feature_daily_metrics", "kind": "base", "block": null, "base_tables": ["pendo__feature_daily_metrics"]}] | [] | ["feature_id", "STRFTIME('%Y-%m', date_day)"] |
| B2 | [{"alias": "f", "kind": "base", "block": null, "base_tables": ["pendo__feature"]}, {"alias": "m", "kind": "derived", "block": "B1", "base_tables": ["pendo__feature_daily_metrics"]}] | [{"type": "INNER", "right": "monthly AS m", "on": "m.feature_id = f.feature_id", "using": []}] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | MAX(count_visitors) | [{"table": "pendo__feature_daily_metrics", "column": "count_visitors"}] | [] | False |
| B1 | AVG(count_visitors) | [{"table": "pendo__feature_daily_metrics", "column": "count_visitors"}] | [] | False |
| B1 | SUM(count_visitors) | [{"table": "pendo__feature_daily_metrics", "column": "count_visitors"}] | [] | False |


## S40

类别 `data`；来源 `python`；调用 `7b5a9f95b30e49029e27c9f5d69011be`；状态 `success`。

```sql

SELECT a.feature_id, a.total_users_tried, a.regular_users, a.casual_users, a.avg_active_days_per_user, a.avg_events_per_user, a.avg_minutes_per_user
FROM pendo__product_adoption_analytics a

```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-077/attempt-01/sql/S40.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-077/attempt-01/sql/S40.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-077/attempt-01/results/S40.rows.jsonl)；完整：True；SHA256：`f49e63d28e44c425dfaa7112b2a38f90c3ad17596b5df30a2419aea123d897f0`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "a", "kind": "base", "block": null, "base_tables": ["pendo__product_adoption_analytics"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |


## S41

类别 `data`；来源 `python`；调用 `7b5a9f95b30e49029e27c9f5d69011be`；状态 `success`。

```sql
SELECT feature_id, product_area_name, page_name, is_core_event FROM pendo__feature
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-077/attempt-01/sql/S41.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-077/attempt-01/sql/S41.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-077/attempt-01/results/S41.rows.jsonl)；完整：True；SHA256：`e38878b2f2f3a41861f6caae13b85aa1fad3ab8479d56615227a9bea0da1b8e7`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "pendo__feature", "kind": "base", "block": null, "base_tables": ["pendo__feature"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |


## S42

类别 `data`；来源 `query_db`；调用 `0738e72a548f44bf8b639d457e199dc7`；状态 `failed`。

```sql
SELECT
  PERCENTILE_25, PERCENTILE_50, PERCENTILE_75,
  AVG_C, MIN_C, MAX_C, STD_C
FROM (
  SELECT
    AVG(CASE WHEN pct <= 25 THEN comprehensive_customer_value END) AS PERCENTILE_25,
    AVG(CASE WHEN pct <= 50 THEN comprehensive_customer_value END) AS PERCENTILE_50,
    AVG(CASE WHEN pct <= 75 THEN comprehensive_customer_value END) AS PERCENTILE_75,
    AVG(comprehensive_customer_value) AS AVG_C,
    MIN(comprehensive_customer_value) AS MIN_C,
    MAX(comprehensive_customer_value) AS MAX_C,
    STDEV(comprehensive_customer_value) AS STD_C
  FROM (
    SELECT comprehensive_customer_value,
           NTILE(100) OVER (ORDER BY comprehensive_customer_value) AS pct
    FROM pendo__customer_lifecycle_insights
  )
) t
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-077/attempt-01/sql/S42.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-077/attempt-01/sql/S42.parameters.json)。

错误：`OperationalError('no such function: STDEV')`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "pendo__customer_lifecycle_insights", "kind": "base", "block": null, "base_tables": ["pendo__customer_lifecycle_insights"]}] | [] | [] |
| B2 | [{"alias": "", "kind": "derived", "block": "B1", "base_tables": ["pendo__customer_lifecycle_insights"]}] | [] | [] |
| B3 | [{"alias": "t", "kind": "derived", "block": "B2", "base_tables": ["pendo__customer_lifecycle_insights"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B2 | AVG(CASE WHEN pct <= 25 THEN comprehensive_customer_value END) | [{"table": "pendo__customer_lifecycle_insights", "column": "comprehensive_customer_value"}] | [{"table": "pendo__customer_lifecycle_insights", "column": "comprehensive_customer_value"}] | False |
| B2 | AVG(CASE WHEN pct <= 50 THEN comprehensive_customer_value END) | [{"table": "pendo__customer_lifecycle_insights", "column": "comprehensive_customer_value"}] | [{"table": "pendo__customer_lifecycle_insights", "column": "comprehensive_customer_value"}] | False |
| B2 | AVG(CASE WHEN pct <= 75 THEN comprehensive_customer_value END) | [{"table": "pendo__customer_lifecycle_insights", "column": "comprehensive_customer_value"}] | [{"table": "pendo__customer_lifecycle_insights", "column": "comprehensive_customer_value"}] | False |
| B2 | AVG(comprehensive_customer_value) | [{"table": "pendo__customer_lifecycle_insights", "column": "comprehensive_customer_value"}] | [] | False |
| B2 | MIN(comprehensive_customer_value) | [{"table": "pendo__customer_lifecycle_insights", "column": "comprehensive_customer_value"}] | [] | False |
| B2 | MAX(comprehensive_customer_value) | [{"table": "pendo__customer_lifecycle_insights", "column": "comprehensive_customer_value"}] | [] | False |
| B2 | STDDEV(comprehensive_customer_value) | [{"table": "pendo__customer_lifecycle_insights", "column": "comprehensive_customer_value"}] | [] | False |


## S43

类别 `data`；来源 `query_db`；调用 `8ba5dc26ba194d1cb7d8de997ea24931`；状态 `failed`。

```sql
SELECT
  AVG(vf_count) AS avg_features_per_visitor,
  MIN(vf_count) AS min_features,
  MAX(vf_count) AS max_features,
  MEDIAN(vf_count) AS median_features
FROM (
  SELECT visitor_id, COUNT(*) AS vf_count
  FROM pendo__visitor_feature
  GROUP BY visitor_id
) t
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-077/attempt-01/sql/S43.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-077/attempt-01/sql/S43.parameters.json)。

错误：`OperationalError('no such function: MEDIAN')`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "pendo__visitor_feature", "kind": "base", "block": null, "base_tables": ["pendo__visitor_feature"]}] | [] | ["visitor_id"] |
| B2 | [{"alias": "t", "kind": "derived", "block": "B1", "base_tables": ["pendo__visitor_feature"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |
| B2 | AVG(vf_count) | [] | [] | False |
| B2 | MIN(vf_count) | [] | [] | False |
| B2 | MAX(vf_count) | [] | [] | False |
| B2 | PERCENTILE_CONT(vf_count, 0.5) | [] | [] | False |


## S44

类别 `data`；来源 `query_db`；调用 `ff71171d623d460b998ddf54002976fc`；状态 `success`。

```sql
SELECT
  COUNT(*) AS n,
  AVG(comprehensive_customer_value) AS avg_ccv,
  MIN(comprehensive_customer_value) AS min_ccv,
  MAX(comprehensive_customer_value) AS max_ccv,
  AVG(user_value_score) AS avg_uvs,
  MIN(user_value_score) AS min_uvs,
  MAX(user_value_score) AS max_uvs,
  SUM(CASE WHEN comprehensive_customer_value >= 500 THEN 1 ELSE 0 END) AS n_high_value
FROM pendo__customer_lifecycle_insights
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-077/attempt-01/sql/S44.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-077/attempt-01/sql/S44.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-077/attempt-01/results/S44.rows.jsonl)；完整：True；SHA256：`9f414225220c47da53c1c8afcc5d253b98abf58017b548751d71c610aa792237`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "pendo__customer_lifecycle_insights", "kind": "base", "block": null, "base_tables": ["pendo__customer_lifecycle_insights"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |
| B1 | AVG(comprehensive_customer_value) | [{"table": "pendo__customer_lifecycle_insights", "column": "comprehensive_customer_value"}] | [] | False |
| B1 | MIN(comprehensive_customer_value) | [{"table": "pendo__customer_lifecycle_insights", "column": "comprehensive_customer_value"}] | [] | False |
| B1 | MAX(comprehensive_customer_value) | [{"table": "pendo__customer_lifecycle_insights", "column": "comprehensive_customer_value"}] | [] | False |
| B1 | AVG(user_value_score) | [{"table": "pendo__customer_lifecycle_insights", "column": "user_value_score"}] | [] | False |
| B1 | MIN(user_value_score) | [{"table": "pendo__customer_lifecycle_insights", "column": "user_value_score"}] | [] | False |
| B1 | MAX(user_value_score) | [{"table": "pendo__customer_lifecycle_insights", "column": "user_value_score"}] | [] | False |
| B1 | SUM(CASE WHEN comprehensive_customer_value >= 500 THEN 1 ELSE 0 END) | [] | [{"table": "pendo__customer_lifecycle_insights", "column": "comprehensive_customer_value"}] | False |


## S45

类别 `data`；来源 `query_db`；调用 `f34ce45ac53449698fd2555990cbc407`；状态 `success`。

```sql
SELECT AVG(cnt) AS avg_features_per_visitor,
       MIN(cnt) AS min_features,
       MAX(cnt) AS max_features
FROM (SELECT visitor_id, COUNT(*) AS cnt FROM pendo__visitor_feature GROUP BY visitor_id)
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-077/attempt-01/sql/S45.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-077/attempt-01/sql/S45.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-077/attempt-01/results/S45.rows.jsonl)；完整：True；SHA256：`2ac8094f12e5dd4eba37c6f4d14dafc1617b3e9b16f5b3381214a55ee4bddd10`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "pendo__visitor_feature", "kind": "base", "block": null, "base_tables": ["pendo__visitor_feature"]}] | [] | ["visitor_id"] |
| B2 | [{"alias": "", "kind": "derived", "block": "B1", "base_tables": ["pendo__visitor_feature"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |
| B2 | AVG(cnt) | [] | [] | False |
| B2 | MIN(cnt) | [] | [] | False |
| B2 | MAX(cnt) | [] | [] | False |

