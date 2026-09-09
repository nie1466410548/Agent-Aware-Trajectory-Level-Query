# dacomp-079

We have observed that the proportion of users with more than 60 active days but who have c…

运行：已提交。官方未评分。全部 SQL 尝试/成功 38/37；数据 SQL 32/31；Python 7 次。

完整原题：

We have observed that the proportion of users with more than 60 active days but who have clicked on fewer than 5 distinct features has reached 15%. The average NPS rating for these users is 0.8 points lower than that of normal users. Please conduct an in-depth analysis of the behavioral characteristics of this "single-feature-use" user segment, including which features they primarily focus on, whether their `average_daily_minutes` is anomalous, and the impact of this usage pattern on long-term retention.

| 表 | 行数 | 列数 |
| --- | --- | --- |
| pendo__account | 1000 | 22 |
| pendo__feature | 2000 | 32 |
| pendo__visitor | 8000 | 24 |
| pendo__visitor_feature | 62077 | 9 |


实际路线（分析者依据 SQL/源码概括，不代表 Agent 自述）：SQL 识别单功能用户并连接功能行为 → Python 再聚合功能集中度与留存指标、检验 → 使用模式建议。

数据库大小：10,838,016 字节。

## 数据 SQL

| SQL | 状态 | 基础表 | Join 输入/类型 | GROUP BY | 聚合表达式 | 结果行数 | 数据库 ms |
| --- | --- | --- | --- | --- | --- | --- | --- |
| [S3/Q1](#s3) | success | ["pendo__visitor_feature"] | 0 / {} | [] | ["COUNT(*)"] | 1 | 3.139 |
| [S4/Q2](#s4) | success | ["pendo__visitor"] | 0 / {} | [] | ["COUNT(*)"] | 1 | 1.288 |
| [S5/Q3](#s5) | success | ["pendo__feature"] | 0 / {} | [] | ["COUNT(*)"] | 1 | 0.638 |
| [S6/Q4](#s6) | success | ["pendo__account"] | 0 / {} | [] | ["COUNT(*)"] | 1 | 0.431 |
| [S7/Q5](#s7) | failed | ["pendo__visitor", "pendo__visitor_feature"] | 2 / {'LEFT': 1} | ["visitor_id", "CASE WHEN v.count_active_days > 60 AND fv.distinct_features < 5 THEN 'single_feature_heavy' ELSE 'normal' END"] | ["COUNT(DISTINCT feature_id)", "COUNT(*)", "AVG(v.avg_nps_rating)"] | unknown | 未取得；调用总时长 0.206 ms |
| [S8/Q6](#s8) | success | ["pendo__visitor", "pendo__visitor_feature"] | 0 / {} | [] | ["COUNT(DISTINCT feature_id)", "COUNT(*)", "SUM(CASE WHEN count_active_days > 60 THEN 1 ELSE 0 END)", "SUM(CASE WHEN count_active_days > 60 AND (SELECT COUNT(DISTINCT feature_id) FROM pendo__visitor_feature AS vf WHERE vf.visitor_id = v.visitor_id) < 5 THEN 1 ELSE 0 END)"] | 1 | 18816.172 |
| [S13/Q7](#s13) | success | ["pendo__visitor"] | 0 / {} | [] | [] | 3 | 0.656 |
| [S14/Q8](#s14) | success | ["pendo__visitor", "pendo__visitor_feature"] | 2 / {'LEFT': 1} | ["visitor_id", "CASE WHEN v.count_active_days > 60 AND fv.distinct_features < 5 THEN 'single_feature_heavy' ELSE 'normal' END"] | ["COUNT(DISTINCT feature_id)", "COUNT(*)", "AVG(v.latest_nps_rating)", "AVG(v.average_daily_minutes)", "AVG(v.average_daily_events)", "AVG(v.count_active_days)", "AVG(fv.distinct_features)"] | 2 | 57.677 |
| [S15/Q9](#s15) | success | ["pendo__account", "pendo__visitor", "pendo__visitor_feature"] | 3 / {'LEFT': 2} | ["visitor_id", "CASE WHEN v.count_active_days > 60 AND fv.distinct_features < 5 THEN 'single_feature_heavy' ELSE 'normal' END"] | ["COUNT(DISTINCT feature_id)", "COUNT(*)", "AVG(a.avg_nps_rating)"] | 2 | 102.832 |
| [S16/Q10](#s16) | success | ["pendo__visitor", "pendo__visitor_feature"] | 2 / {'LEFT': 1} | ["visitor_id", "CASE WHEN v.count_active_days > 60 AND COALESCE(fv.distinct_features, 0) < 5 THEN 'single_feature_heavy' ELSE 'normal' END"] | ["COUNT(DISTINCT feature_id)", "COUNT(*)", "AVG(v.latest_nps_rating)", "AVG(v.average_daily_minutes)", "AVG(v.average_daily_events)"] | 2 | 95.907 |
| [S17/Q11](#s17) | success | ["pendo__visitor", "pendo__visitor_feature"] | 0 / {} | [] | ["COUNT(*)"] | 1 | 20420.363 |
| [S18/Q12](#s18) | success | ["pendo__visitor", "pendo__visitor_feature"] | 2 / {'INNER': 1} | ["visitor_id", "fv.distinct_features"] | ["COUNT(DISTINCT feature_id)", "COUNT(*)"] | 4 | 41.911 |
| [S19/Q13](#s19) | success | ["pendo__feature", "pendo__visitor", "pendo__visitor_feature"] | 3 / {'INNER': 2} | ["f.feature_id"] | ["COUNT(DISTINCT vf2.feature_id)", "COUNT(DISTINCT vf.visitor_id)", "SUM(vf.sum_clicks)", "AVG(vf.sum_clicks)"] | 20 | 15704.31 |
| [S20/Q14](#s20) | success | ["pendo__feature", "pendo__visitor", "pendo__visitor_feature"] | 3 / {'INNER': 2} | ["f.product_area_name"] | ["COUNT(DISTINCT vf2.feature_id)", "COUNT(DISTINCT f.feature_id)", "COUNT(DISTINCT vf.visitor_id)", "SUM(vf.sum_clicks)", "AVG(vf.sum_clicks)"] | 10 | 15586.853 |
| [S21/Q15](#s21) | success | ["pendo__visitor", "pendo__visitor_feature"] | 2 / {'LEFT': 1} | ["visitor_id", "CASE WHEN v.count_active_days > 60 AND fv.distinct_features < 5 THEN 'single_feature_heavy' ELSE 'normal' END"] | ["COUNT(DISTINCT feature_id)", "MIN(v.average_daily_minutes)", "AVG(v.average_daily_minutes)", "MAX(v.average_daily_minutes)", "AVG(v.average_daily_events)", "AVG(v.sum_minutes)", "AVG(v.sum_events)", "AVG(v.count_active_days)"] | 2 | 51.747 |
| [S22/Q16](#s22) | success | ["pendo__visitor", "pendo__visitor_feature"] | 2 / {'LEFT': 1} | ["visitor_id", "CASE WHEN v.count_active_days > 60 AND fv.distinct_features < 5 THEN 'single_feature_heavy' ELSE 'normal' END"] | ["COUNT(DISTINCT feature_id)", "AVG(v.count_active_months)", "AVG(CAST(JULIANDAY(COALESCE(v.last_event_on, v.last_visit)) - JULIANDAY(COALESCE(v.first_event_on, v.first_visit_at)) AS REAL))", "AVG(CASE WHEN JULIANDAY(COALESCE(v.last_event_on, v.last_visit)) < JULIANDAY('2025-10-14') - 90 THEN 1 ELSE 0 END)"] | 2 | 56.681 |
| [S23/Q17](#s23) | success | ["pendo__visitor"] | 0 / {} | [] | ["MIN(first_event_on)", "MAX(last_event_on)", "MIN(last_visit)", "MAX(last_visit)", "MIN(first_visit_at)", "MAX(last_updated_at)"] | 1 | 4.388 |
| [S24/Q18](#s24) | success | ["pendo__visitor", "pendo__visitor_feature"] | 2 / {'LEFT': 1} | ["visitor_id", "CASE WHEN v.count_active_days > 60 AND fv.distinct_features < 5 THEN 'single_feature_heavy' ELSE 'normal' END"] | ["COUNT(DISTINCT feature_id)", "AVG(v.count_active_months)", "AVG(JULIANDAY(v.last_event_on) - JULIANDAY(v.first_event_on))", "AVG(v.count_active_months * 1.0 / NULLIF(ROUND((JULIANDAY(v.last_event_on) - JULIANDAY(v.first_event_on)) / 30.0), 0))"] | 2 | 56.899 |
| [S25/Q19](#s25) | success | ["pendo__visitor", "pendo__visitor_feature"] | 2 / {'LEFT': 1} | ["visitor_id", "CASE WHEN v.count_active_days > 60 AND fv.distinct_features < 5 THEN 'single_feature_heavy' ELSE 'normal' END", "v.count_active_months"] | ["COUNT(DISTINCT feature_id)", "COUNT(*)"] | 11 | 52.684 |
| [S26/Q20](#s26) | success | ["pendo__visitor", "pendo__visitor_feature"] | 3 / {'INNER': 4} | ["visitor_id", "visitor_id", "visitor_id", "uf.distinct_features"] | ["COUNT(DISTINCT feature_id)", "SUM(sum_clicks)", "MAX(sum_clicks)", "COUNT(DISTINCT uf.visitor_id)", "AVG(um.max_feature_clicks * 1.0 / ut.total_clicks)", "AVG(ut.total_clicks)"] | 4 | 652.788 |
| [S27/Q21](#s27) | success | ["pendo__visitor", "pendo__visitor_feature"] | 2 / {'LEFT': 1} | ["visitor_id", "CASE WHEN v.count_active_days > 60 AND fv.distinct_features < 5 THEN 'single_feature_heavy' ELSE 'normal' END"] | ["COUNT(DISTINCT feature_id)", "AVG(JULIANDAY('2025-10-14') - JULIANDAY(v.last_event_on))", "AVG(JULIANDAY('2025-10-14') - JULIANDAY(v.first_event_on))"] | 2 | 54.583 |
| [S28/Q22](#s28) | success | ["pendo__visitor"] | 0 / {} | ["last_event_on"] | ["COUNT(*)"] | 1 | 3.92 |
| [S29/Q23](#s29) | success | ["pendo__visitor"] | 0 / {} | [] | ["COUNT(*)", "MIN(last_event_on)", "MAX(last_event_on)"] | 1 | 2.952 |
| [S30/Q24](#s30) | success | ["pendo__account", "pendo__visitor", "pendo__visitor_feature"] | 3 / {'INNER': 1, 'LEFT': 1} | ["visitor_id", "CASE WHEN fv.distinct_features < 5 THEN 'single_feature_heavy' ELSE 'multi_feature_heavy' END"] | ["COUNT(DISTINCT feature_id)", "COUNT(*)", "AVG(v.count_active_days)", "AVG(v.count_active_months)", "AVG(JULIANDAY(v.last_event_on) - JULIANDAY(v.first_event_on))", "AVG(v.average_daily_minutes)", "AVG(v.average_daily_events)", "AVG(v.latest_nps_rating)", "AVG(a.avg_nps_rating)"] | 2 | 53.798 |
| [S31/Q25](#s31) | success | ["pendo__visitor", "pendo__visitor_feature"] | 2 / {'INNER': 1} | ["visitor_id", "CASE WHEN fv.distinct_features < 5 THEN 'single_feature_heavy' ELSE 'multi_feature_heavy' END"] | ["COUNT(DISTINCT feature_id)", "COUNT(*)", "MIN(v.latest_nps_rating)", "AVG(v.latest_nps_rating)", "MAX(v.latest_nps_rating)"] | 2 | 45.952 |
| [S32/Q26](#s32) | success | ["pendo__feature", "pendo__visitor", "pendo__visitor_feature"] | 3 / {'INNER': 2} | ["f.product_area_name", "f.feature_name"] | ["COUNT(DISTINCT vf2.feature_id)", "COUNT(DISTINCT vf.visitor_id)", "SUM(vf.sum_clicks)", "AVG(vf.avg_daily_minutes)", "AVG(vf.count_click_events)"] | 20 | 16748.189 |
| [S33/Q27](#s33) | success | ["pendo__visitor", "pendo__visitor_feature"] | 2 / {'LEFT': 1} | ["visitor_id", "CASE WHEN v.count_active_days > 60 AND fv.distinct_features < 5 THEN 'single_feature_heavy' ELSE 'normal' END"] | ["COUNT(DISTINCT feature_id)", "AVG(v.average_daily_minutes)", "AVG(CASE WHEN v.count_active_days > 60 THEN v.average_daily_minutes END)"] | 2 | 50.139 |
| [S34/Q28](#s34) | success | ["pendo__account", "pendo__visitor", "pendo__visitor_feature"] | 3 / {'LEFT': 2} | ["visitor_id"] | ["COUNT(DISTINCT feature_id)"] | 8000 | 69.61 |
| [S35/Q29](#s35) | success | ["pendo__feature", "pendo__visitor", "pendo__visitor_feature"] | 2 / {'INNER': 2} | ["visitor_id"] | ["COUNT(DISTINCT feature_id)"] | 3028 | 62.233 |
| [S36/Q30](#s36) | success | ["pendo__visitor", "pendo__visitor_feature"] | 2 / {'LEFT': 1} | ["visitor_id", "CASE WHEN v.count_active_days > 60 AND fv.distinct_features < 5 THEN 'single_feature_heavy' ELSE 'normal' END", "v.last_browser_name", "v.last_operating_system"] | ["COUNT(DISTINCT feature_id)", "COUNT(*)", "AVG(v.average_daily_minutes)"] | 20 | 55.122 |
| [S37/Q31](#s37) | success | ["pendo__feature", "pendo__visitor", "pendo__visitor_feature"] | 3 / {'INNER': 2} | ["f.app_display_name", "f.app_platform"] | ["COUNT(DISTINCT vf2.feature_id)", "COUNT(DISTINCT vf.visitor_id)", "AVG(v.average_daily_minutes)"] | 15 | 16400.969 |
| [S38/Q32](#s38) | success | ["pendo__visitor", "pendo__visitor_feature"] | 2 / {'INNER': 1} | ["visitor_id", "fv.distinct_features"] | ["COUNT(DISTINCT feature_id)", "COUNT(*)", "AVG(v.average_daily_minutes)", "AVG(v.latest_nps_rating)", "AVG(v.count_active_days)", "AVG(v.count_active_months)"] | 20 | 45.874 |


## 元数据和设置

| SQL | 类别 | 状态 | 内容 |
| --- | --- | --- | --- |
| S1 | connection_setup | success | PRAGMA query_only=ON |
| S2 | metadata | success | SELECT name,sql FROM sqlite_master WHERE type='table' ORDER BY name |
| S9 | metadata | success | PRAGMA table_info(pendo__visitor) |
| S10 | metadata | success | PRAGMA table_info(pendo__account) |
| S11 | metadata | success | SELECT cid, name, type FROM pragma_table_info('pendo__visitor') |
| S12 | metadata | success | SELECT cid, name, type FROM pragma_table_info('pendo__account') |


## Python 与执行位置

人工源码审查：**database_first_violation**。Python 对功能、产品区域和用户执行求和、最大值、去重数量及分箱均值，计算主导功能占比和留存画像。这些可在 SQL 内完成；Mann–Whitney 与 t 检验是独立统计补充。 [证据](../reviews/dacomp-079.json)。

P1：Statistical hypothesis tests (Mann-Whitney U / t-test) and distributions are not supported by SQLite; plotting also requires matplotlib/seaborn. Loads only the aggregated per-user metrics already retrieved from SQL (S34/S35 results) and the feature rows for single-feature users.

[源码](../../../runs/dsv4flash-db-first-full-01/dacomp-079/attempt-01/python/P1.py)；[输出](../../../runs/dsv4flash-db-first-full-01/dacomp-079/attempt-01/python/P1.stdout)；[错误](../../../runs/dsv4flash-db-first-full-01/dacomp-079/attempt-01/python/P1.stderr)。自动源码筛查未检出预设迁出信号；这不是全面语义合规证明。

P2：Check actual column names from the JSONL file to debug the KeyError.

[源码](../../../runs/dsv4flash-db-first-full-01/dacomp-079/attempt-01/python/P2.py)；[输出](../../../runs/dsv4flash-db-first-full-01/dacomp-079/attempt-01/python/P2.stdout)；[错误](../../../runs/dsv4flash-db-first-full-01/dacomp-079/attempt-01/python/P2.stderr)。自动源码筛查未检出预设迁出信号；这不是全面语义合规证明。

P3：Inspect JSONL row structure to map columns correctly.

[源码](../../../runs/dsv4flash-db-first-full-01/dacomp-079/attempt-01/python/P3.py)；[输出](../../../runs/dsv4flash-db-first-full-01/dacomp-079/attempt-01/python/P3.stdout)；[错误](../../../runs/dsv4flash-db-first-full-01/dacomp-079/attempt-01/python/P3.stderr)。自动源码筛查未检出预设迁出信号；这不是全面语义合规证明。

P4：Reload user-level metrics with correct column mapping (JSONL rows are positional arrays), then run statistical tests and create visualizations.

[源码](../../../runs/dsv4flash-db-first-full-01/dacomp-079/attempt-01/python/P4.py)；[输出](../../../runs/dsv4flash-db-first-full-01/dacomp-079/attempt-01/python/P4.stdout)；[错误](../../../runs/dsv4flash-db-first-full-01/dacomp-079/attempt-01/python/P4.stderr)。自动源码筛查未检出预设迁出信号；这不是全面语义合规证明。

P5：Generate figures: daily-minutes and NPS distributions by segment, top features of the single-feature segment, retention metrics, and feature-concentration. Uses only the previously retrieved user-level (S34) and feature-level (S35) data.

[源码](../../../runs/dsv4flash-db-first-full-01/dacomp-079/attempt-01/python/P5.py)；[输出](../../../runs/dsv4flash-db-first-full-01/dacomp-079/attempt-01/python/P5.stdout)；[错误](../../../runs/dsv4flash-db-first-full-01/dacomp-079/attempt-01/python/P5.stderr)。检出需人工核验的 SQL 可实现操作：groupby(, sort_values(；不能仅凭理由判为合规。

P6：Correlation and retention-depth analysis beyond SQL: check whether the daily-minutes deficit persists after binning by active days (confounder control), and quantify retention correlations with distinct-feature count.

[源码](../../../runs/dsv4flash-db-first-full-01/dacomp-079/attempt-01/python/P6.py)；[输出](../../../runs/dsv4flash-db-first-full-01/dacomp-079/attempt-01/python/P6.stdout)；[错误](../../../runs/dsv4flash-db-first-full-01/dacomp-079/attempt-01/python/P6.stderr)。检出需人工核验的 SQL 可实现操作：groupby(；不能仅凭理由判为合规。

P7：Fix the heavy-only retention analysis: tenure_days was not persisted in CSV. Recompute within the same script.

[源码](../../../runs/dsv4flash-db-first-full-01/dacomp-079/attempt-01/python/P7.py)；[输出](../../../runs/dsv4flash-db-first-full-01/dacomp-079/attempt-01/python/P7.stdout)；[错误](../../../runs/dsv4flash-db-first-full-01/dacomp-079/attempt-01/python/P7.stderr)。检出需人工核验的 SQL 可实现操作：groupby(；不能仅凭理由判为合规。

## 优化机会

已验证候选。筛选限于精确 SQL、相同自包含 CTE、相同单表完整过滤、可分解单表聚合；未覆盖任意 Join 等价和一般谓词蕴含。全部候选都是 offline，未测在线预测。

| 候选 | 类型 | 已有结果 | 覆盖 SQL | 后续次数 | 中间行数 | 验证 | 成本 |
| --- | --- | --- | --- | --- | --- | --- | --- |
| C1 | aggregate MV | False | ["S4", "S23", "S28", "S29"] | 3 | 1 | verified | Not benchmarked; correctness alone does not establish net speedup. |


已验证覆盖（含触发查询、候选并集去重）：4/31 条成功数据 SQL。正确性仅针对当前数据库快照；未测性能的候选不能声称已加速。

[完整 build/rewrite 与比较证据](dacomp-079.analysis.json)。

### C1：aggregate MV

Union of grouping keys; decomposable aggregate states; AVG uses SUM and non-NULL COUNT.

原查询 [S4](#s4), [S23](#s23), [S28](#s28), [S29](#s29) → 新增共享状态 C1 → 后续 3 次可复用。该构建点为事后假设，不代表 Agent 当时预知后续。

构建定义：

```sql
SELECT last_event_on AS __g0, COUNT(*) AS __a0, MIN(first_event_on) AS __a1, MAX(last_event_on) AS __a2, MIN(last_visit) AS __a3, MAX(last_visit) AS __a4, MIN(first_visit_at) AS __a5, MAX(last_updated_at) AS __a6, MIN(last_event_on) AS __a7 FROM "pendo__visitor"  GROUP BY last_event_on
```

受益查询 S4 的改写示例：

```sql
SELECT SUM(__a0) AS n FROM temp.reuse_candidate
```

| 原 SQL | 列名一致 | 结果一致 | 比较方法 |
| --- | --- | --- | --- |
| S4 | True | True | exact_multiset |
| S23 | True | True | exact_multiset |
| S28 | True | True | ordered_numeric_tolerance |
| S29 | True | True | exact_multiset |


验证状态：verified；成本结论：Not benchmarked; correctness alone does not establish net speedup.

结果依赖：自动记录 SQL→Python 的接口父调用，以及源码中引用归档文件的消费者；字面值相同不认定因果。模型方向选择需要人工读取消息，尚未做全面因果标注。

[原始报告](../../../runs/dsv4flash-db-first-full-01/dacomp-079/attempt-01/answer.md)；[统一消息](../../../runs/dsv4flash-db-first-full-01/dacomp-079/attempt-01/messages.jsonl)；[原始 OpenCode 事件](../../../runs/dsv4flash-db-first-full-01/dacomp-079/attempt-01/opencode.jsonl)；[SQL 引擎日志](../../../runs/dsv4flash-db-first-full-01/dacomp-079/attempt-01/sql_journal.jsonl)。

[可读报告（本地图片链接规范化）](../answers/dacomp-079.md)。原始回答保留，分析结论未改写。

## S1

类别 `connection_setup`；来源 `connection`；调用 `3eb9d8ad734f44d5bd6b2385a90bf322`；状态 `success`。

```sql
PRAGMA query_only=ON
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-079/attempt-01/sql/S1.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-079/attempt-01/sql/S1.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-079/attempt-01/results/S1.rows.jsonl)；完整：True；SHA256：`e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`。

## S2

类别 `metadata`；来源 `list_db`；调用 `3eb9d8ad734f44d5bd6b2385a90bf322`；状态 `success`。

```sql
SELECT name,sql FROM sqlite_master WHERE type='table' ORDER BY name
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-079/attempt-01/sql/S2.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-079/attempt-01/sql/S2.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-079/attempt-01/results/S2.rows.jsonl)；完整：True；SHA256：`58a1e54daafd0a854fdd935ad1d024504733738193f48cc658ff32931fb83332`。

## S3

类别 `data`；来源 `query_db`；调用 `40cac5cbf8f94f0bb8ab92588b5cac0e`；状态 `success`。

```sql
SELECT COUNT(*) AS n FROM pendo__visitor_feature
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-079/attempt-01/sql/S3.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-079/attempt-01/sql/S3.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-079/attempt-01/results/S3.rows.jsonl)；完整：True；SHA256：`1752de5537da1c1505f5606e1e1393e77c3c9e59f71b093e095d7932f4e2b00b`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "pendo__visitor_feature", "kind": "base", "block": null, "base_tables": ["pendo__visitor_feature"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |


## S4

类别 `data`；来源 `query_db`；调用 `7695fc3134a54e239ab3718701ddb6a1`；状态 `success`。

```sql
SELECT COUNT(*) AS n FROM pendo__visitor
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-079/attempt-01/sql/S4.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-079/attempt-01/sql/S4.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-079/attempt-01/results/S4.rows.jsonl)；完整：True；SHA256：`ca5d97f4dab69813055999493cfea8f56e91e334c1465da9867b484a21b0a9bd`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "pendo__visitor", "kind": "base", "block": null, "base_tables": ["pendo__visitor"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |


## S5

类别 `data`；来源 `query_db`；调用 `adfdb931a6ed4520ae974f3c84dea7dd`；状态 `success`。

```sql
SELECT COUNT(*) AS n FROM pendo__feature
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-079/attempt-01/sql/S5.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-079/attempt-01/sql/S5.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-079/attempt-01/results/S5.rows.jsonl)；完整：True；SHA256：`4b7ebd95b494120f7bc16bef6e23e2f94400ec47439aefa675a0212e533ee170`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "pendo__feature", "kind": "base", "block": null, "base_tables": ["pendo__feature"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |


## S6

类别 `data`；来源 `query_db`；调用 `07e4dd71c48d427290cdff03ff392065`；状态 `success`。

```sql
SELECT COUNT(*) AS n FROM pendo__account
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-079/attempt-01/sql/S6.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-079/attempt-01/sql/S6.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-079/attempt-01/results/S6.rows.jsonl)；完整：True；SHA256：`e3ed33dc26a723b8481ca677e38dc4a6e8700aeec312afdd02c9dd92374161a2`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "pendo__account", "kind": "base", "block": null, "base_tables": ["pendo__account"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |


## S7

类别 `data`；来源 `query_db`；调用 `c530d12a775642b7a62d391aec385a8a`；状态 `failed`。

```sql
SELECT
  CASE WHEN v.count_active_days > 60 AND fv.distinct_features < 5 THEN 'single_feature_heavy' ELSE 'normal' END AS segment,
  COUNT(*) AS n_users,
  AVG(v.avg_nps_rating) AS avg_nps
FROM pendo__visitor v
LEFT JOIN (
  SELECT visitor_id, COUNT(DISTINCT feature_id) AS distinct_features
  FROM pendo__visitor_feature
  GROUP BY visitor_id
) fv ON fv.visitor_id = v.visitor_id
GROUP BY segment
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-079/attempt-01/sql/S7.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-079/attempt-01/sql/S7.parameters.json)。

错误：`OperationalError('no such column: v.avg_nps_rating')`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "pendo__visitor_feature", "kind": "base", "block": null, "base_tables": ["pendo__visitor_feature"]}] | [] | ["visitor_id"] |
| B2 | [{"alias": "v", "kind": "base", "block": null, "base_tables": ["pendo__visitor"]}, {"alias": "fv", "kind": "derived", "block": "B1", "base_tables": ["pendo__visitor_feature"]}] | [{"type": "LEFT", "right": "(SELECT visitor_id, COUNT(DISTINCT feature_id) AS distinct_features FROM pendo__visitor_feature GROUP BY visitor_id) AS fv", "on": "fv.visitor_id = v.visitor_id", "using": []}] | ["CASE WHEN v.count_active_days > 60 AND fv.distinct_features < 5 THEN 'single_feature_heavy' ELSE 'normal' END"] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(DISTINCT feature_id) | [{"table": "pendo__visitor_feature", "column": "feature_id"}] | [] | False |
| B2 | COUNT(*) | [] | [] | True |
| B2 | AVG(v.avg_nps_rating) | [{"table": "pendo__visitor", "column": "avg_nps_rating"}] | [] | False |


## S8

类别 `data`；来源 `query_db`；调用 `bc484dd93ccc4deab84a25a00341e016`；状态 `success`。

```sql
SELECT COUNT(*) AS total_visitors,
  SUM(CASE WHEN count_active_days > 60 THEN 1 ELSE 0 END) AS active_gt_60,
  SUM(CASE WHEN count_active_days > 60 AND (SELECT COUNT(DISTINCT feature_id) FROM pendo__visitor_feature vf WHERE vf.visitor_id = v.visitor_id) < 5 THEN 1 ELSE 0 END) AS segment_candidates
FROM pendo__visitor v
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-079/attempt-01/sql/S8.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-079/attempt-01/sql/S8.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-079/attempt-01/results/S8.rows.jsonl)；完整：True；SHA256：`e333002fdb8d122f98e24115f81565721da519e3c9e046323219c47ddac3526d`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "vf", "kind": "base", "block": null, "base_tables": ["pendo__visitor_feature"]}] | [] | [] |
| B2 | [{"alias": "v", "kind": "base", "block": null, "base_tables": ["pendo__visitor"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(DISTINCT feature_id) | [{"table": "pendo__visitor_feature", "column": "feature_id"}] | [] | False |
| B2 | COUNT(*) | [] | [] | True |
| B2 | SUM(CASE WHEN count_active_days > 60 THEN 1 ELSE 0 END) | [] | [{"table": "pendo__visitor", "column": "count_active_days"}] | False |
| B2 | SUM(CASE WHEN count_active_days > 60 AND (SELECT COUNT(DISTINCT feature_id) FROM pendo__visitor_feature AS vf WHERE vf.visitor_id = v.visitor_id) < 5 THEN 1 ELSE 0 END) | [] | [{"table": "pendo__visitor", "column": "count_active_days"}, {"table": "pendo__visitor_feature", "column": "feature_id"}, {"table": "pendo__visitor_feature", "column": "visitor_id"}, {"table": "pendo__visitor", "column": "visitor_id"}] | False |


未解析列血缘：[{"block": "B2", "column": "feature_id", "reason": "ambiguous_or_missing_source"}]

## S9

类别 `metadata`；来源 `query_db`；调用 `2e95ab1f903044ff8352597133f4d532`；状态 `success`。

```sql
PRAGMA table_info(pendo__visitor)
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-079/attempt-01/sql/S9.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-079/attempt-01/sql/S9.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-079/attempt-01/results/S9.rows.jsonl)；完整：True；SHA256：`5a3fd35e584e112bed2f9a2da663373a03838165eeb9475ed4fb18269ec961be`。

## S10

类别 `metadata`；来源 `query_db`；调用 `f187844062064259a853efcef90c2568`；状态 `success`。

```sql
PRAGMA table_info(pendo__account)
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-079/attempt-01/sql/S10.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-079/attempt-01/sql/S10.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-079/attempt-01/results/S10.rows.jsonl)；完整：True；SHA256：`6a7f5c1584bf25ffa7527ab084cdb9a9d182ba01c391be084855a9e1765af9ba`。

## S11

类别 `metadata`；来源 `query_db`；调用 `7f26f77fde804b7289cc1d0089ef6b40`；状态 `success`。

```sql
SELECT cid, name, type FROM pragma_table_info('pendo__visitor')
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-079/attempt-01/sql/S11.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-079/attempt-01/sql/S11.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-079/attempt-01/results/S11.rows.jsonl)；完整：True；SHA256：`9a7db96e582f08d14fc84ca5d71185783b89976be49c42c6063f2b2b7e0eac89`。

## S12

类别 `metadata`；来源 `query_db`；调用 `5b5bdd0c10cb41578285a7a6cc6643da`；状态 `success`。

```sql
SELECT cid, name, type FROM pragma_table_info('pendo__account')
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-079/attempt-01/sql/S12.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-079/attempt-01/sql/S12.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-079/attempt-01/results/S12.rows.jsonl)；完整：True；SHA256：`68f92f59b116b20b960eae4a10a3fa3432aa9752f4684344f3b95d9bcaa49385`。

## S13

类别 `data`；来源 `query_db`；调用 `36aa207e9a21480fb381a9e1a9ac4993`；状态 `success`。

```sql
SELECT * FROM pendo__visitor LIMIT 3
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-079/attempt-01/sql/S13.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-079/attempt-01/sql/S13.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-079/attempt-01/results/S13.rows.jsonl)；完整：True；SHA256：`141df1da37fdc5a98fb8c3e59ca0c47673f5a43d69783588e044ef101544cf52`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "pendo__visitor", "kind": "base", "block": null, "base_tables": ["pendo__visitor"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |


## S14

类别 `data`；来源 `query_db`；调用 `3f8f2a9cee564342971e50696dd989e6`；状态 `success`。

```sql
SELECT
  CASE WHEN v.count_active_days > 60 AND fv.distinct_features < 5 THEN 'single_feature_heavy' ELSE 'normal' END AS segment,
  COUNT(*) AS n_users,
  ROUND(AVG(v.latest_nps_rating), 4) AS avg_nps,
  ROUND(AVG(v.average_daily_minutes), 4) AS avg_daily_minutes,
  ROUND(AVG(v.average_daily_events), 4) AS avg_daily_events,
  ROUND(AVG(v.count_active_days), 2) AS avg_active_days,
  ROUND(AVG(fv.distinct_features), 2) AS avg_distinct_features
FROM pendo__visitor v
LEFT JOIN (
  SELECT visitor_id, COUNT(DISTINCT feature_id) AS distinct_features
  FROM pendo__visitor_feature
  GROUP BY visitor_id
) fv ON fv.visitor_id = v.visitor_id
GROUP BY segment
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-079/attempt-01/sql/S14.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-079/attempt-01/sql/S14.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-079/attempt-01/results/S14.rows.jsonl)；完整：True；SHA256：`c59776c431717e737ff94cf68c073a8fd587a257fac898357282bbc25bd42b86`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "pendo__visitor_feature", "kind": "base", "block": null, "base_tables": ["pendo__visitor_feature"]}] | [] | ["visitor_id"] |
| B2 | [{"alias": "v", "kind": "base", "block": null, "base_tables": ["pendo__visitor"]}, {"alias": "fv", "kind": "derived", "block": "B1", "base_tables": ["pendo__visitor_feature"]}] | [{"type": "LEFT", "right": "(SELECT visitor_id, COUNT(DISTINCT feature_id) AS distinct_features FROM pendo__visitor_feature GROUP BY visitor_id) AS fv", "on": "fv.visitor_id = v.visitor_id", "using": []}] | ["CASE WHEN v.count_active_days > 60 AND fv.distinct_features < 5 THEN 'single_feature_heavy' ELSE 'normal' END"] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(DISTINCT feature_id) | [{"table": "pendo__visitor_feature", "column": "feature_id"}] | [] | False |
| B2 | COUNT(*) | [] | [] | True |
| B2 | AVG(v.latest_nps_rating) | [{"table": "pendo__visitor", "column": "latest_nps_rating"}] | [] | False |
| B2 | AVG(v.average_daily_minutes) | [{"table": "pendo__visitor", "column": "average_daily_minutes"}] | [] | False |
| B2 | AVG(v.average_daily_events) | [{"table": "pendo__visitor", "column": "average_daily_events"}] | [] | False |
| B2 | AVG(v.count_active_days) | [{"table": "pendo__visitor", "column": "count_active_days"}] | [] | False |
| B2 | AVG(fv.distinct_features) | [{"table": "pendo__visitor_feature", "column": "feature_id"}] | [] | False |


## S15

类别 `data`；来源 `query_db`；调用 `fe3853734faf42b498f5d741e61f7a67`；状态 `success`。

```sql
SELECT
  CASE WHEN v.count_active_days > 60 AND fv.distinct_features < 5 THEN 'single_feature_heavy' ELSE 'normal' END AS segment,
  ROUND(AVG(a.avg_nps_rating), 4) AS avg_account_nps,
  COUNT(*) AS n_users
FROM pendo__visitor v
LEFT JOIN (
  SELECT visitor_id, COUNT(DISTINCT feature_id) AS distinct_features
  FROM pendo__visitor_feature
  GROUP BY visitor_id
) fv ON fv.visitor_id = v.visitor_id
LEFT JOIN pendo__account a ON a.account_id = v.account_id
GROUP BY segment
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-079/attempt-01/sql/S15.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-079/attempt-01/sql/S15.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-079/attempt-01/results/S15.rows.jsonl)；完整：True；SHA256：`cb1867f605d24b889a00dc664e1302a729a5c899745445d137d1dba5c01c34df`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "pendo__visitor_feature", "kind": "base", "block": null, "base_tables": ["pendo__visitor_feature"]}] | [] | ["visitor_id"] |
| B2 | [{"alias": "v", "kind": "base", "block": null, "base_tables": ["pendo__visitor"]}, {"alias": "fv", "kind": "derived", "block": "B1", "base_tables": ["pendo__visitor_feature"]}, {"alias": "a", "kind": "base", "block": null, "base_tables": ["pendo__account"]}] | [{"type": "LEFT", "right": "(SELECT visitor_id, COUNT(DISTINCT feature_id) AS distinct_features FROM pendo__visitor_feature GROUP BY visitor_id) AS fv", "on": "fv.visitor_id = v.visitor_id", "using": []}, {"type": "LEFT", "right": "pendo__account AS a", "on": "a.account_id = v.account_id", "using": []}] | ["CASE WHEN v.count_active_days > 60 AND fv.distinct_features < 5 THEN 'single_feature_heavy' ELSE 'normal' END"] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(DISTINCT feature_id) | [{"table": "pendo__visitor_feature", "column": "feature_id"}] | [] | False |
| B2 | COUNT(*) | [] | [] | True |
| B2 | AVG(a.avg_nps_rating) | [{"table": "pendo__account", "column": "avg_nps_rating"}] | [] | False |


## S16

类别 `data`；来源 `query_db`；调用 `e917573b04d948f984706ac8ca62a568`；状态 `success`。

```sql
SELECT
  CASE WHEN v.count_active_days > 60 AND COALESCE(fv.distinct_features, 0) < 5 THEN 'single_feature_heavy' ELSE 'normal' END AS segment,
  ROUND(AVG(v.latest_nps_rating), 4) AS avg_nps,
  ROUND(AVG(v.average_daily_minutes), 4) AS avg_daily_minutes,
  ROUND(AVG(v.average_daily_events), 4) AS avg_daily_events,
  COUNT(*) AS n_users
FROM pendo__visitor v
LEFT JOIN (
  SELECT visitor_id, COUNT(DISTINCT feature_id) AS distinct_features
  FROM pendo__visitor_feature
  GROUP BY visitor_id
) fv ON fv.visitor_id = v.visitor_id
GROUP BY segment
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-079/attempt-01/sql/S16.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-079/attempt-01/sql/S16.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-079/attempt-01/results/S16.rows.jsonl)；完整：True；SHA256：`47e6502eb09d21afdc9e2171ae559da2d1edb7ccf4af44fe4e5663199f6f4929`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "pendo__visitor_feature", "kind": "base", "block": null, "base_tables": ["pendo__visitor_feature"]}] | [] | ["visitor_id"] |
| B2 | [{"alias": "v", "kind": "base", "block": null, "base_tables": ["pendo__visitor"]}, {"alias": "fv", "kind": "derived", "block": "B1", "base_tables": ["pendo__visitor_feature"]}] | [{"type": "LEFT", "right": "(SELECT visitor_id, COUNT(DISTINCT feature_id) AS distinct_features FROM pendo__visitor_feature GROUP BY visitor_id) AS fv", "on": "fv.visitor_id = v.visitor_id", "using": []}] | ["CASE WHEN v.count_active_days > 60 AND COALESCE(fv.distinct_features, 0) < 5 THEN 'single_feature_heavy' ELSE 'normal' END"] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(DISTINCT feature_id) | [{"table": "pendo__visitor_feature", "column": "feature_id"}] | [] | False |
| B2 | COUNT(*) | [] | [] | True |
| B2 | AVG(v.latest_nps_rating) | [{"table": "pendo__visitor", "column": "latest_nps_rating"}] | [] | False |
| B2 | AVG(v.average_daily_minutes) | [{"table": "pendo__visitor", "column": "average_daily_minutes"}] | [] | False |
| B2 | AVG(v.average_daily_events) | [{"table": "pendo__visitor", "column": "average_daily_events"}] | [] | False |


## S17

类别 `data`；来源 `query_db`；调用 `f05a029af3044a90862fb31ab8b974c0`；状态 `success`。

```sql
SELECT COUNT(*) AS no_feature_visitors
FROM pendo__visitor v
WHERE NOT EXISTS (SELECT 1 FROM pendo__visitor_feature vf WHERE vf.visitor_id = v.visitor_id)
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-079/attempt-01/sql/S17.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-079/attempt-01/sql/S17.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-079/attempt-01/results/S17.rows.jsonl)；完整：True；SHA256：`c14196f132c1e9be0508ae80ab52fcb3e1d3fc05880415f3dc980971df207c9e`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "vf", "kind": "base", "block": null, "base_tables": ["pendo__visitor_feature"]}] | [] | [] |
| B2 | [{"alias": "v", "kind": "base", "block": null, "base_tables": ["pendo__visitor"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B2 | COUNT(*) | [] | [] | True |


## S18

类别 `data`；来源 `query_db`；调用 `d71a19798d53481b9886e523b8629cfe`；状态 `success`。

```sql
SELECT
  fv.distinct_features,
  COUNT(*) AS n_visitors
FROM pendo__visitor v
JOIN (
  SELECT visitor_id, COUNT(DISTINCT feature_id) AS distinct_features
  FROM pendo__visitor_feature
  GROUP BY visitor_id
) fv ON fv.visitor_id = v.visitor_id
WHERE v.count_active_days > 60 AND fv.distinct_features < 5
GROUP BY fv.distinct_features
ORDER BY fv.distinct_features
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-079/attempt-01/sql/S18.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-079/attempt-01/sql/S18.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-079/attempt-01/results/S18.rows.jsonl)；完整：True；SHA256：`05400b6f0eeffd1f55adb4a0a19caa710784f77ee5590d4dc6ed1832adf81597`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "pendo__visitor_feature", "kind": "base", "block": null, "base_tables": ["pendo__visitor_feature"]}] | [] | ["visitor_id"] |
| B2 | [{"alias": "v", "kind": "base", "block": null, "base_tables": ["pendo__visitor"]}, {"alias": "fv", "kind": "derived", "block": "B1", "base_tables": ["pendo__visitor_feature"]}] | [{"type": "INNER", "right": "(SELECT visitor_id, COUNT(DISTINCT feature_id) AS distinct_features FROM pendo__visitor_feature GROUP BY visitor_id) AS fv", "on": "fv.visitor_id = v.visitor_id", "using": []}] | ["fv.distinct_features"] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(DISTINCT feature_id) | [{"table": "pendo__visitor_feature", "column": "feature_id"}] | [] | False |
| B2 | COUNT(*) | [] | [] | True |


## S19

类别 `data`；来源 `query_db`；调用 `590b6825e3d74991b7955271cde050da`；状态 `success`。

```sql
-- Top features used by single-feature-heavy users
SELECT
  f.feature_id,
  f.feature_name,
  f.product_area_name,
  f.page_name,
  f.app_display_name,
  f.app_platform,
  COUNT(DISTINCT vf.visitor_id) AS n_single_feature_users,
  SUM(vf.sum_clicks) AS total_clicks,
  ROUND(AVG(vf.sum_clicks), 2) AS avg_clicks_per_user
FROM pendo__visitor_feature vf
JOIN pendo__feature f ON f.feature_id = vf.feature_id
JOIN pendo__visitor v ON v.visitor_id = vf.visitor_id
WHERE v.count_active_days > 60
  AND (SELECT COUNT(DISTINCT vf2.feature_id) FROM pendo__visitor_feature vf2 WHERE vf2.visitor_id = v.visitor_id) < 5
GROUP BY f.feature_id
ORDER BY n_single_feature_users DESC
LIMIT 20
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-079/attempt-01/sql/S19.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-079/attempt-01/sql/S19.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-079/attempt-01/results/S19.rows.jsonl)；完整：True；SHA256：`0cc95587b07aca11d94f2b693fd28bef507a74a9de37c13f94c7947e6f5f987c`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "vf2", "kind": "base", "block": null, "base_tables": ["pendo__visitor_feature"]}] | [] | [] |
| B2 | [{"alias": "vf", "kind": "base", "block": null, "base_tables": ["pendo__visitor_feature"]}, {"alias": "f", "kind": "base", "block": null, "base_tables": ["pendo__feature"]}, {"alias": "v", "kind": "base", "block": null, "base_tables": ["pendo__visitor"]}] | [{"type": "INNER", "right": "pendo__feature AS f", "on": "f.feature_id = vf.feature_id", "using": []}, {"type": "INNER", "right": "pendo__visitor AS v", "on": "v.visitor_id = vf.visitor_id", "using": []}] | ["f.feature_id"] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(DISTINCT vf2.feature_id) | [{"table": "pendo__visitor_feature", "column": "feature_id"}] | [] | False |
| B2 | COUNT(DISTINCT vf.visitor_id) | [{"table": "pendo__visitor_feature", "column": "visitor_id"}] | [] | False |
| B2 | SUM(vf.sum_clicks) | [{"table": "pendo__visitor_feature", "column": "sum_clicks"}] | [] | False |
| B2 | AVG(vf.sum_clicks) | [{"table": "pendo__visitor_feature", "column": "sum_clicks"}] | [] | False |


## S20

类别 `data`；来源 `query_db`；调用 `a8d44c92f92f460fa1247e68d3b3d0b9`；状态 `success`。

```sql
-- Which product areas are most popular among single-feature-heavy users?
SELECT
  f.product_area_name,
  COUNT(DISTINCT f.feature_id) AS n_features,
  COUNT(DISTINCT vf.visitor_id) AS n_single_feature_users,
  SUM(vf.sum_clicks) AS total_clicks,
  ROUND(AVG(vf.sum_clicks), 2) AS avg_clicks_per_user
FROM pendo__visitor_feature vf
JOIN pendo__feature f ON f.feature_id = vf.feature_id
JOIN pendo__visitor v ON v.visitor_id = vf.visitor_id
WHERE v.count_active_days > 60
  AND (SELECT COUNT(DISTINCT vf2.feature_id) FROM pendo__visitor_feature vf2 WHERE vf2.visitor_id = v.visitor_id) < 5
GROUP BY f.product_area_name
ORDER BY n_single_feature_users DESC
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-079/attempt-01/sql/S20.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-079/attempt-01/sql/S20.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-079/attempt-01/results/S20.rows.jsonl)；完整：True；SHA256：`8374bf21c809874b3330da87fdd88e475f476af103e7ad918a07cc1666446b48`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "vf2", "kind": "base", "block": null, "base_tables": ["pendo__visitor_feature"]}] | [] | [] |
| B2 | [{"alias": "vf", "kind": "base", "block": null, "base_tables": ["pendo__visitor_feature"]}, {"alias": "f", "kind": "base", "block": null, "base_tables": ["pendo__feature"]}, {"alias": "v", "kind": "base", "block": null, "base_tables": ["pendo__visitor"]}] | [{"type": "INNER", "right": "pendo__feature AS f", "on": "f.feature_id = vf.feature_id", "using": []}, {"type": "INNER", "right": "pendo__visitor AS v", "on": "v.visitor_id = vf.visitor_id", "using": []}] | ["f.product_area_name"] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(DISTINCT vf2.feature_id) | [{"table": "pendo__visitor_feature", "column": "feature_id"}] | [] | False |
| B2 | COUNT(DISTINCT f.feature_id) | [{"table": "pendo__feature", "column": "feature_id"}] | [] | False |
| B2 | COUNT(DISTINCT vf.visitor_id) | [{"table": "pendo__visitor_feature", "column": "visitor_id"}] | [] | False |
| B2 | SUM(vf.sum_clicks) | [{"table": "pendo__visitor_feature", "column": "sum_clicks"}] | [] | False |
| B2 | AVG(vf.sum_clicks) | [{"table": "pendo__visitor_feature", "column": "sum_clicks"}] | [] | False |


## S21

类别 `data`；来源 `query_db`；调用 `d1f3a7a604d74271bba45fb61a2eaf45`；状态 `success`。

```sql
-- Compare the average_daily_minutes distributions
SELECT
  CASE WHEN v.count_active_days > 60 AND fv.distinct_features < 5 THEN 'single_feature_heavy' ELSE 'normal' END AS segment,
  ROUND(MIN(v.average_daily_minutes), 2) AS min_daily_min,
  ROUND(AVG(v.average_daily_minutes), 2) AS avg_daily_min,
  ROUND(MAX(v.average_daily_minutes), 2) AS max_daily_min,
  ROUND(AVG(v.average_daily_events), 2) AS avg_daily_events,
  ROUND(AVG(v.sum_minutes), 2) AS avg_total_minutes,
  ROUND(AVG(v.sum_events), 2) AS avg_total_events,
  ROUND(AVG(v.count_active_days), 2) AS avg_active_days
FROM pendo__visitor v
LEFT JOIN (
  SELECT visitor_id, COUNT(DISTINCT feature_id) AS distinct_features
  FROM pendo__visitor_feature
  GROUP BY visitor_id
) fv ON fv.visitor_id = v.visitor_id
GROUP BY segment
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-079/attempt-01/sql/S21.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-079/attempt-01/sql/S21.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-079/attempt-01/results/S21.rows.jsonl)；完整：True；SHA256：`fc25076b79cf3d3ab7dabaf9c66a5bf941a1696148608fdf2ca884b4e589ae10`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "pendo__visitor_feature", "kind": "base", "block": null, "base_tables": ["pendo__visitor_feature"]}] | [] | ["visitor_id"] |
| B2 | [{"alias": "v", "kind": "base", "block": null, "base_tables": ["pendo__visitor"]}, {"alias": "fv", "kind": "derived", "block": "B1", "base_tables": ["pendo__visitor_feature"]}] | [{"type": "LEFT", "right": "(SELECT visitor_id, COUNT(DISTINCT feature_id) AS distinct_features FROM pendo__visitor_feature GROUP BY visitor_id) AS fv", "on": "fv.visitor_id = v.visitor_id", "using": []}] | ["CASE WHEN v.count_active_days > 60 AND fv.distinct_features < 5 THEN 'single_feature_heavy' ELSE 'normal' END"] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(DISTINCT feature_id) | [{"table": "pendo__visitor_feature", "column": "feature_id"}] | [] | False |
| B2 | MIN(v.average_daily_minutes) | [{"table": "pendo__visitor", "column": "average_daily_minutes"}] | [] | False |
| B2 | AVG(v.average_daily_minutes) | [{"table": "pendo__visitor", "column": "average_daily_minutes"}] | [] | False |
| B2 | MAX(v.average_daily_minutes) | [{"table": "pendo__visitor", "column": "average_daily_minutes"}] | [] | False |
| B2 | AVG(v.average_daily_events) | [{"table": "pendo__visitor", "column": "average_daily_events"}] | [] | False |
| B2 | AVG(v.sum_minutes) | [{"table": "pendo__visitor", "column": "sum_minutes"}] | [] | False |
| B2 | AVG(v.sum_events) | [{"table": "pendo__visitor", "column": "sum_events"}] | [] | False |
| B2 | AVG(v.count_active_days) | [{"table": "pendo__visitor", "column": "count_active_days"}] | [] | False |


## S22

类别 `data`；来源 `query_db`；调用 `a82629685d77440fb2e35f2511580f72`；状态 `success`。

```sql
SELECT
  CASE WHEN v.count_active_days > 60 AND fv.distinct_features < 5 THEN 'single_feature_heavy' ELSE 'normal' END AS segment,
  ROUND(AVG(v.count_active_months), 2) AS avg_active_months,
  ROUND(AVG(CAST(julianday(COALESCE(v.last_event_on, v.last_visit)) - julianday(COALESCE(v.first_event_on, v.first_visit_at)) AS REAL)), 1) AS avg_tenure_days,
  ROUND(AVG(CASE WHEN julianday(COALESCE(v.last_event_on, v.last_visit)) < julianday('2025-10-14') - 90 THEN 1 ELSE 0 END), 4) AS churn_rate_90d
FROM pendo__visitor v
LEFT JOIN (
  SELECT visitor_id, COUNT(DISTINCT feature_id) AS distinct_features
  FROM pendo__visitor_feature
  GROUP BY visitor_id
) fv ON fv.visitor_id = v.visitor_id
GROUP BY segment
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-079/attempt-01/sql/S22.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-079/attempt-01/sql/S22.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-079/attempt-01/results/S22.rows.jsonl)；完整：True；SHA256：`72160ac1671f00329ec1b539785f51df97469b02f191385165383ea46ed4bcb9`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "pendo__visitor_feature", "kind": "base", "block": null, "base_tables": ["pendo__visitor_feature"]}] | [] | ["visitor_id"] |
| B2 | [{"alias": "v", "kind": "base", "block": null, "base_tables": ["pendo__visitor"]}, {"alias": "fv", "kind": "derived", "block": "B1", "base_tables": ["pendo__visitor_feature"]}] | [{"type": "LEFT", "right": "(SELECT visitor_id, COUNT(DISTINCT feature_id) AS distinct_features FROM pendo__visitor_feature GROUP BY visitor_id) AS fv", "on": "fv.visitor_id = v.visitor_id", "using": []}] | ["CASE WHEN v.count_active_days > 60 AND fv.distinct_features < 5 THEN 'single_feature_heavy' ELSE 'normal' END"] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(DISTINCT feature_id) | [{"table": "pendo__visitor_feature", "column": "feature_id"}] | [] | False |
| B2 | AVG(v.count_active_months) | [{"table": "pendo__visitor", "column": "count_active_months"}] | [] | False |
| B2 | AVG(CAST(JULIANDAY(COALESCE(v.last_event_on, v.last_visit)) - JULIANDAY(COALESCE(v.first_event_on, v.first_visit_at)) AS REAL)) | [{"table": "pendo__visitor", "column": "last_event_on"}, {"table": "pendo__visitor", "column": "last_visit"}, {"table": "pendo__visitor", "column": "first_event_on"}, {"table": "pendo__visitor", "column": "first_visit_at"}] | [] | False |
| B2 | AVG(CASE WHEN JULIANDAY(COALESCE(v.last_event_on, v.last_visit)) < JULIANDAY('2025-10-14') - 90 THEN 1 ELSE 0 END) | [] | [{"table": "pendo__visitor", "column": "last_event_on"}, {"table": "pendo__visitor", "column": "last_visit"}] | False |


## S23

类别 `data`；来源 `query_db`；调用 `d70cd5ca8d5247908f8050945ddf8a6a`；状态 `success`。

```sql
SELECT MIN(first_event_on) AS min_first, MAX(last_event_on) AS max_last,
  MIN(last_visit) AS min_last_visit, MAX(last_visit) AS max_last_visit,
  MIN(first_visit_at) AS min_first_visit, MAX(last_updated_at) AS max_updated
FROM pendo__visitor
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-079/attempt-01/sql/S23.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-079/attempt-01/sql/S23.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-079/attempt-01/results/S23.rows.jsonl)；完整：True；SHA256：`6ae6409449118f2a52ce5976bcc07e8bff88280351b163121ffeacf13a45726b`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "pendo__visitor", "kind": "base", "block": null, "base_tables": ["pendo__visitor"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | MIN(first_event_on) | [{"table": "pendo__visitor", "column": "first_event_on"}] | [] | False |
| B1 | MAX(last_event_on) | [{"table": "pendo__visitor", "column": "last_event_on"}] | [] | False |
| B1 | MIN(last_visit) | [{"table": "pendo__visitor", "column": "last_visit"}] | [] | False |
| B1 | MAX(last_visit) | [{"table": "pendo__visitor", "column": "last_visit"}] | [] | False |
| B1 | MIN(first_visit_at) | [{"table": "pendo__visitor", "column": "first_visit_at"}] | [] | False |
| B1 | MAX(last_updated_at) | [{"table": "pendo__visitor", "column": "last_updated_at"}] | [] | False |


## S24

类别 `data`；来源 `query_db`；调用 `f0f404e22b6e4e2f9091ef1eccb06ca3`；状态 `success`。

```sql
SELECT
  CASE WHEN v.count_active_days > 60 AND fv.distinct_features < 5 THEN 'single_feature_heavy' ELSE 'normal' END AS segment,
  ROUND(AVG(v.count_active_months), 2) AS avg_active_months,
  ROUND(AVG(julianday(v.last_event_on) - julianday(v.first_event_on)), 1) AS avg_span_days,
  ROUND(AVG(v.count_active_months * 1.0 / NULLIF(ROUND((julianday(v.last_event_on) - julianday(v.first_event_on)) / 30.0), 0)), 4) AS avg_months_coverage_ratio
FROM pendo__visitor v
LEFT JOIN (
  SELECT visitor_id, COUNT(DISTINCT feature_id) AS distinct_features
  FROM pendo__visitor_feature
  GROUP BY visitor_id
) fv ON fv.visitor_id = v.visitor_id
GROUP BY segment
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-079/attempt-01/sql/S24.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-079/attempt-01/sql/S24.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-079/attempt-01/results/S24.rows.jsonl)；完整：True；SHA256：`768ed56713cb815171898d35c230efa368a06a4658319eea152e206f9f31a56a`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "pendo__visitor_feature", "kind": "base", "block": null, "base_tables": ["pendo__visitor_feature"]}] | [] | ["visitor_id"] |
| B2 | [{"alias": "v", "kind": "base", "block": null, "base_tables": ["pendo__visitor"]}, {"alias": "fv", "kind": "derived", "block": "B1", "base_tables": ["pendo__visitor_feature"]}] | [{"type": "LEFT", "right": "(SELECT visitor_id, COUNT(DISTINCT feature_id) AS distinct_features FROM pendo__visitor_feature GROUP BY visitor_id) AS fv", "on": "fv.visitor_id = v.visitor_id", "using": []}] | ["CASE WHEN v.count_active_days > 60 AND fv.distinct_features < 5 THEN 'single_feature_heavy' ELSE 'normal' END"] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(DISTINCT feature_id) | [{"table": "pendo__visitor_feature", "column": "feature_id"}] | [] | False |
| B2 | AVG(v.count_active_months) | [{"table": "pendo__visitor", "column": "count_active_months"}] | [] | False |
| B2 | AVG(JULIANDAY(v.last_event_on) - JULIANDAY(v.first_event_on)) | [{"table": "pendo__visitor", "column": "last_event_on"}, {"table": "pendo__visitor", "column": "first_event_on"}] | [] | False |
| B2 | AVG(v.count_active_months * 1.0 / NULLIF(ROUND((JULIANDAY(v.last_event_on) - JULIANDAY(v.first_event_on)) / 30.0), 0)) | [{"table": "pendo__visitor", "column": "count_active_months"}, {"table": "pendo__visitor", "column": "last_event_on"}, {"table": "pendo__visitor", "column": "first_event_on"}] | [] | False |


## S25

类别 `data`；来源 `query_db`；调用 `6fe2870c73fe4d7fa17a0b4b202dd533`；状态 `success`。

```sql
-- Distribution of count_active_months
SELECT
  CASE WHEN v.count_active_days > 60 AND fv.distinct_features < 5 THEN 'single_feature_heavy' ELSE 'normal' END AS segment,
  v.count_active_months,
  COUNT(*) AS n_users
FROM pendo__visitor v
LEFT JOIN (
  SELECT visitor_id, COUNT(DISTINCT feature_id) AS distinct_features
  FROM pendo__visitor_feature
  GROUP BY visitor_id
) fv ON fv.visitor_id = v.visitor_id
GROUP BY segment, v.count_active_months
ORDER BY segment, v.count_active_months
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-079/attempt-01/sql/S25.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-079/attempt-01/sql/S25.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-079/attempt-01/results/S25.rows.jsonl)；完整：True；SHA256：`2e9d6bd57d7ef2cca6c94a21ff592a8102f253e52f0cbfe860d1220af47a5a7b`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "pendo__visitor_feature", "kind": "base", "block": null, "base_tables": ["pendo__visitor_feature"]}] | [] | ["visitor_id"] |
| B2 | [{"alias": "v", "kind": "base", "block": null, "base_tables": ["pendo__visitor"]}, {"alias": "fv", "kind": "derived", "block": "B1", "base_tables": ["pendo__visitor_feature"]}] | [{"type": "LEFT", "right": "(SELECT visitor_id, COUNT(DISTINCT feature_id) AS distinct_features FROM pendo__visitor_feature GROUP BY visitor_id) AS fv", "on": "fv.visitor_id = v.visitor_id", "using": []}] | ["CASE WHEN v.count_active_days > 60 AND fv.distinct_features < 5 THEN 'single_feature_heavy' ELSE 'normal' END", "v.count_active_months"] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(DISTINCT feature_id) | [{"table": "pendo__visitor_feature", "column": "feature_id"}] | [] | False |
| B2 | COUNT(*) | [] | [] | True |


## S26

类别 `data`；来源 `query_db`；调用 `82bef37c353f461c88802318f066eb89`；状态 `success`。

```sql
-- Concentration: share of clicks on the dominant feature per user
WITH user_feature AS (
  SELECT vf.visitor_id, fv.distinct_features,
    vf.feature_id, vf.sum_clicks
  FROM pendo__visitor_feature vf
  JOIN pendo__visitor v ON v.visitor_id = vf.visitor_id
  JOIN (SELECT visitor_id, COUNT(DISTINCT feature_id) AS distinct_features
        FROM pendo__visitor_feature GROUP BY visitor_id) fv ON fv.visitor_id = v.visitor_id
  WHERE v.count_active_days > 60 AND fv.distinct_features < 5
),
user_totals AS (
  SELECT visitor_id, distinct_features, SUM(sum_clicks) AS total_clicks
  FROM user_feature GROUP BY visitor_id
),
user_max AS (
  SELECT visitor_id, MAX(sum_clicks) AS max_feature_clicks
  FROM user_feature GROUP BY visitor_id
)
SELECT
  uf.distinct_features,
  COUNT(DISTINCT uf.visitor_id) AS n_users,
  ROUND(AVG(um.max_feature_clicks * 1.0 / ut.total_clicks), 4) AS avg_dominant_share,
  ROUND(AVG(ut.total_clicks), 1) AS avg_total_clicks
FROM user_feature uf
JOIN user_totals ut ON ut.visitor_id = uf.visitor_id
JOIN user_max um ON um.visitor_id = uf.visitor_id
GROUP BY uf.distinct_features
ORDER BY uf.distinct_features
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-079/attempt-01/sql/S26.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-079/attempt-01/sql/S26.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-079/attempt-01/results/S26.rows.jsonl)；完整：True；SHA256：`a8289801afcc05e50b25eb33ceae838fe8d32801a0604405d524b6545dce993f`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "pendo__visitor_feature", "kind": "base", "block": null, "base_tables": ["pendo__visitor_feature"]}] | [] | ["visitor_id"] |
| B2 | [{"alias": "vf", "kind": "base", "block": null, "base_tables": ["pendo__visitor_feature"]}, {"alias": "v", "kind": "base", "block": null, "base_tables": ["pendo__visitor"]}, {"alias": "fv", "kind": "derived", "block": "B1", "base_tables": ["pendo__visitor_feature"]}] | [{"type": "INNER", "right": "pendo__visitor AS v", "on": "v.visitor_id = vf.visitor_id", "using": []}, {"type": "INNER", "right": "(SELECT visitor_id, COUNT(DISTINCT feature_id) AS distinct_features FROM pendo__visitor_feature GROUP BY visitor_id) AS fv", "on": "fv.visitor_id = v.visitor_id", "using": []}] | [] |
| B3 | [{"alias": "user_feature", "kind": "derived", "block": "B2", "base_tables": ["pendo__visitor", "pendo__visitor_feature"]}] | [] | ["visitor_id"] |
| B4 | [{"alias": "user_feature", "kind": "derived", "block": "B2", "base_tables": ["pendo__visitor", "pendo__visitor_feature"]}] | [] | ["visitor_id"] |
| B5 | [{"alias": "uf", "kind": "derived", "block": "B2", "base_tables": ["pendo__visitor", "pendo__visitor_feature"]}, {"alias": "ut", "kind": "derived", "block": "B3", "base_tables": ["pendo__visitor", "pendo__visitor_feature"]}, {"alias": "um", "kind": "derived", "block": "B4", "base_tables": ["pendo__visitor", "pendo__visitor_feature"]}] | [{"type": "INNER", "right": "user_totals AS ut", "on": "ut.visitor_id = uf.visitor_id", "using": []}, {"type": "INNER", "right": "user_max AS um", "on": "um.visitor_id = uf.visitor_id", "using": []}] | ["uf.distinct_features"] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(DISTINCT feature_id) | [{"table": "pendo__visitor_feature", "column": "feature_id"}] | [] | False |
| B3 | SUM(sum_clicks) | [{"table": "pendo__visitor_feature", "column": "sum_clicks"}] | [] | False |
| B4 | MAX(sum_clicks) | [{"table": "pendo__visitor_feature", "column": "sum_clicks"}] | [] | False |
| B5 | COUNT(DISTINCT uf.visitor_id) | [{"table": "pendo__visitor_feature", "column": "visitor_id"}] | [] | False |
| B5 | AVG(um.max_feature_clicks * 1.0 / ut.total_clicks) | [{"table": "pendo__visitor_feature", "column": "sum_clicks"}, {"table": "pendo__visitor_feature", "column": "sum_clicks"}] | [] | False |
| B5 | AVG(ut.total_clicks) | [{"table": "pendo__visitor_feature", "column": "sum_clicks"}] | [] | False |


## S27

类别 `data`；来源 `query_db`；调用 `ccb28a722d444f578caefbb06928629a`；状态 `success`。

```sql
-- Retention proxy: recency of last event
SELECT
  CASE WHEN v.count_active_days > 60 AND fv.distinct_features < 5 THEN 'single_feature_heavy' ELSE 'normal' END AS segment,
  ROUND(AVG(julianday('2025-10-14') - julianday(v.last_event_on)), 1) AS avg_days_since_last_event,
  ROUND(AVG(julianday('2025-10-14') - julianday(v.first_event_on)), 1) AS avg_days_since_first_event
FROM pendo__visitor v
LEFT JOIN (
  SELECT visitor_id, COUNT(DISTINCT feature_id) AS distinct_features
  FROM pendo__visitor_feature
  GROUP BY visitor_id
) fv ON fv.visitor_id = v.visitor_id
GROUP BY segment
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-079/attempt-01/sql/S27.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-079/attempt-01/sql/S27.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-079/attempt-01/results/S27.rows.jsonl)；完整：True；SHA256：`f9d41306cab2f5c212ac00193b05110e93dd250c6dd0b9ad5ffb855cb5a6a49b`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "pendo__visitor_feature", "kind": "base", "block": null, "base_tables": ["pendo__visitor_feature"]}] | [] | ["visitor_id"] |
| B2 | [{"alias": "v", "kind": "base", "block": null, "base_tables": ["pendo__visitor"]}, {"alias": "fv", "kind": "derived", "block": "B1", "base_tables": ["pendo__visitor_feature"]}] | [{"type": "LEFT", "right": "(SELECT visitor_id, COUNT(DISTINCT feature_id) AS distinct_features FROM pendo__visitor_feature GROUP BY visitor_id) AS fv", "on": "fv.visitor_id = v.visitor_id", "using": []}] | ["CASE WHEN v.count_active_days > 60 AND fv.distinct_features < 5 THEN 'single_feature_heavy' ELSE 'normal' END"] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(DISTINCT feature_id) | [{"table": "pendo__visitor_feature", "column": "feature_id"}] | [] | False |
| B2 | AVG(JULIANDAY('2025-10-14') - JULIANDAY(v.last_event_on)) | [{"table": "pendo__visitor", "column": "last_event_on"}] | [] | False |
| B2 | AVG(JULIANDAY('2025-10-14') - JULIANDAY(v.first_event_on)) | [{"table": "pendo__visitor", "column": "first_event_on"}] | [] | False |


## S28

类别 `data`；来源 `query_db`；调用 `91511a255d684738a68f158a4abe2b0e`；状态 `success`。

```sql
SELECT last_event_on, COUNT(*) AS n
FROM pendo__visitor
GROUP BY last_event_on
ORDER BY n DESC
LIMIT 10
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-079/attempt-01/sql/S28.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-079/attempt-01/sql/S28.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-079/attempt-01/results/S28.rows.jsonl)；完整：True；SHA256：`73b7c82b99a1b2830b845f91aec13230a712749165eb4700f026118e1959a1f4`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "pendo__visitor", "kind": "base", "block": null, "base_tables": ["pendo__visitor"]}] | [] | ["last_event_on"] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |


## S29

类别 `data`；来源 `query_db`；调用 `aa7a4d27103046ffa87c69d47a8c65a8`；状态 `success`。

```sql
SELECT COUNT(*) AS n, MIN(last_event_on) AS min_last, MAX(last_event_on) AS max_last
FROM pendo__visitor
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-079/attempt-01/sql/S29.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-079/attempt-01/sql/S29.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-079/attempt-01/results/S29.rows.jsonl)；完整：True；SHA256：`c907b8cc890481b4c315fedc7f929102873f687056bc8c287edaef2ba88dd78e`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "pendo__visitor", "kind": "base", "block": null, "base_tables": ["pendo__visitor"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |
| B1 | MIN(last_event_on) | [{"table": "pendo__visitor", "column": "last_event_on"}] | [] | False |
| B1 | MAX(last_event_on) | [{"table": "pendo__visitor", "column": "last_event_on"}] | [] | False |


## S30

类别 `data`；来源 `query_db`；调用 `d41cf53501ad4080abb518ed28de9a73`；状态 `success`。

```sql
-- Fair comparison within the >60 active-day population
SELECT
  CASE WHEN fv.distinct_features < 5 THEN 'single_feature_heavy' ELSE 'multi_feature_heavy' END AS segment,
  COUNT(*) AS n_users,
  ROUND(AVG(v.count_active_days), 1) AS avg_active_days,
  ROUND(AVG(v.count_active_months), 2) AS avg_active_months,
  ROUND(AVG(julianday(v.last_event_on) - julianday(v.first_event_on)), 1) AS avg_span_days,
  ROUND(AVG(v.average_daily_minutes), 2) AS avg_daily_minutes,
  ROUND(AVG(v.average_daily_events), 2) AS avg_daily_events,
  ROUND(AVG(v.latest_nps_rating), 3) AS avg_nps,
  ROUND(AVG(a.avg_nps_rating), 3) AS avg_account_nps
FROM pendo__visitor v
JOIN (
  SELECT visitor_id, COUNT(DISTINCT feature_id) AS distinct_features
  FROM pendo__visitor_feature
  GROUP BY visitor_id
) fv ON fv.visitor_id = v.visitor_id
LEFT JOIN pendo__account a ON a.account_id = v.account_id
WHERE v.count_active_days > 60
GROUP BY segment
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-079/attempt-01/sql/S30.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-079/attempt-01/sql/S30.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-079/attempt-01/results/S30.rows.jsonl)；完整：True；SHA256：`465da95af0560047d70a203adc59de516e230c68fa22824e0e1aed64731b96f4`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "pendo__visitor_feature", "kind": "base", "block": null, "base_tables": ["pendo__visitor_feature"]}] | [] | ["visitor_id"] |
| B2 | [{"alias": "v", "kind": "base", "block": null, "base_tables": ["pendo__visitor"]}, {"alias": "fv", "kind": "derived", "block": "B1", "base_tables": ["pendo__visitor_feature"]}, {"alias": "a", "kind": "base", "block": null, "base_tables": ["pendo__account"]}] | [{"type": "INNER", "right": "(SELECT visitor_id, COUNT(DISTINCT feature_id) AS distinct_features FROM pendo__visitor_feature GROUP BY visitor_id) AS fv", "on": "fv.visitor_id = v.visitor_id", "using": []}, {"type": "LEFT", "right": "pendo__account AS a", "on": "a.account_id = v.account_id", "using": []}] | ["CASE WHEN fv.distinct_features < 5 THEN 'single_feature_heavy' ELSE 'multi_feature_heavy' END"] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(DISTINCT feature_id) | [{"table": "pendo__visitor_feature", "column": "feature_id"}] | [] | False |
| B2 | COUNT(*) | [] | [] | True |
| B2 | AVG(v.count_active_days) | [{"table": "pendo__visitor", "column": "count_active_days"}] | [] | False |
| B2 | AVG(v.count_active_months) | [{"table": "pendo__visitor", "column": "count_active_months"}] | [] | False |
| B2 | AVG(JULIANDAY(v.last_event_on) - JULIANDAY(v.first_event_on)) | [{"table": "pendo__visitor", "column": "last_event_on"}, {"table": "pendo__visitor", "column": "first_event_on"}] | [] | False |
| B2 | AVG(v.average_daily_minutes) | [{"table": "pendo__visitor", "column": "average_daily_minutes"}] | [] | False |
| B2 | AVG(v.average_daily_events) | [{"table": "pendo__visitor", "column": "average_daily_events"}] | [] | False |
| B2 | AVG(v.latest_nps_rating) | [{"table": "pendo__visitor", "column": "latest_nps_rating"}] | [] | False |
| B2 | AVG(a.avg_nps_rating) | [{"table": "pendo__account", "column": "avg_nps_rating"}] | [] | False |


## S31

类别 `data`；来源 `query_db`；调用 `6cd18f3dd0614b469ccf6cca04a41ff5`；状态 `success`。

```sql
-- NPS distributions for the two within-heavy segments
SELECT
  CASE WHEN fv.distinct_features < 5 THEN 'single_feature_heavy' ELSE 'multi_feature_heavy' END AS segment,
  ROUND(MIN(v.latest_nps_rating), 1) AS min_nps,
  ROUND(AVG(v.latest_nps_rating), 3) AS avg_nps,
  ROUND(MAX(v.latest_nps_rating), 1) AS max_nps,
  COUNT(*) AS n
FROM pendo__visitor v
JOIN (
  SELECT visitor_id, COUNT(DISTINCT feature_id) AS distinct_features
  FROM pendo__visitor_feature
  GROUP BY visitor_id
) fv ON fv.visitor_id = v.visitor_id
WHERE v.count_active_days > 60
GROUP BY segment
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-079/attempt-01/sql/S31.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-079/attempt-01/sql/S31.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-079/attempt-01/results/S31.rows.jsonl)；完整：True；SHA256：`7e4b7f8cdadd97422a1df65871381f3b3d8df1cc9cd1da5a4e806497feebdcfd`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "pendo__visitor_feature", "kind": "base", "block": null, "base_tables": ["pendo__visitor_feature"]}] | [] | ["visitor_id"] |
| B2 | [{"alias": "v", "kind": "base", "block": null, "base_tables": ["pendo__visitor"]}, {"alias": "fv", "kind": "derived", "block": "B1", "base_tables": ["pendo__visitor_feature"]}] | [{"type": "INNER", "right": "(SELECT visitor_id, COUNT(DISTINCT feature_id) AS distinct_features FROM pendo__visitor_feature GROUP BY visitor_id) AS fv", "on": "fv.visitor_id = v.visitor_id", "using": []}] | ["CASE WHEN fv.distinct_features < 5 THEN 'single_feature_heavy' ELSE 'multi_feature_heavy' END"] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(DISTINCT feature_id) | [{"table": "pendo__visitor_feature", "column": "feature_id"}] | [] | False |
| B2 | COUNT(*) | [] | [] | True |
| B2 | MIN(v.latest_nps_rating) | [{"table": "pendo__visitor", "column": "latest_nps_rating"}] | [] | False |
| B2 | AVG(v.latest_nps_rating) | [{"table": "pendo__visitor", "column": "latest_nps_rating"}] | [] | False |
| B2 | MAX(v.latest_nps_rating) | [{"table": "pendo__visitor", "column": "latest_nps_rating"}] | [] | False |


## S32

类别 `data`；来源 `query_db`；调用 `332534d3a60f418abc9d34227291e80b`；状态 `success`。

```sql
-- For single-feature users, what's the distribution of their main feature's product area?
SELECT
  f.product_area_name,
  f.feature_name,
  COUNT(DISTINCT vf.visitor_id) AS n_users,
  SUM(vf.sum_clicks) AS total_clicks,
  ROUND(AVG(vf.avg_daily_minutes), 2) AS avg_daily_minutes_in_feature,
  ROUND(AVG(vf.count_click_events), 1) AS avg_click_events
FROM pendo__visitor_feature vf
JOIN pendo__feature f ON f.feature_id = vf.feature_id
JOIN pendo__visitor v ON v.visitor_id = vf.visitor_id
WHERE v.count_active_days > 60
  AND (SELECT COUNT(DISTINCT vf2.feature_id) FROM pendo__visitor_feature vf2 WHERE vf2.visitor_id = v.visitor_id) < 5
GROUP BY f.product_area_name, f.feature_name
ORDER BY n_users DESC
LIMIT 20
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-079/attempt-01/sql/S32.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-079/attempt-01/sql/S32.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-079/attempt-01/results/S32.rows.jsonl)；完整：True；SHA256：`3cdc5b2d027a3b45dbc32b479472ac9aa679fccf5e866e97bb3e5eaa5ebec5ed`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "vf2", "kind": "base", "block": null, "base_tables": ["pendo__visitor_feature"]}] | [] | [] |
| B2 | [{"alias": "vf", "kind": "base", "block": null, "base_tables": ["pendo__visitor_feature"]}, {"alias": "f", "kind": "base", "block": null, "base_tables": ["pendo__feature"]}, {"alias": "v", "kind": "base", "block": null, "base_tables": ["pendo__visitor"]}] | [{"type": "INNER", "right": "pendo__feature AS f", "on": "f.feature_id = vf.feature_id", "using": []}, {"type": "INNER", "right": "pendo__visitor AS v", "on": "v.visitor_id = vf.visitor_id", "using": []}] | ["f.product_area_name", "f.feature_name"] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(DISTINCT vf2.feature_id) | [{"table": "pendo__visitor_feature", "column": "feature_id"}] | [] | False |
| B2 | COUNT(DISTINCT vf.visitor_id) | [{"table": "pendo__visitor_feature", "column": "visitor_id"}] | [] | False |
| B2 | SUM(vf.sum_clicks) | [{"table": "pendo__visitor_feature", "column": "sum_clicks"}] | [] | False |
| B2 | AVG(vf.avg_daily_minutes) | [{"table": "pendo__visitor_feature", "column": "avg_daily_minutes"}] | [] | False |
| B2 | AVG(vf.count_click_events) | [{"table": "pendo__visitor_feature", "column": "count_click_events"}] | [] | False |


## S33

类别 `data`；来源 `query_db`；调用 `506581da0c0a44d497783eacfe33098e`；状态 `success`。

```sql
-- Compare average_daily_minutes by segment through distribution quantiles
SELECT
  CASE WHEN v.count_active_days > 60 AND fv.distinct_features < 5 THEN 'single_feature_heavy' ELSE 'normal' END AS segment,
  ROUND(AVG(v.average_daily_minutes), 2) AS mean,
  ROUND(AVG(CASE WHEN v.count_active_days > 60 THEN v.average_daily_minutes END), 2) AS mean_among_active
FROM pendo__visitor v
LEFT JOIN (
  SELECT visitor_id, COUNT(DISTINCT feature_id) AS distinct_features
  FROM pendo__visitor_feature
  GROUP BY visitor_id
) fv ON fv.visitor_id = v.visitor_id
GROUP BY segment
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-079/attempt-01/sql/S33.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-079/attempt-01/sql/S33.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-079/attempt-01/results/S33.rows.jsonl)；完整：True；SHA256：`c6cd07023a5a525ac210cdf336ed1ea1fda67de34b05713a4ac52a72693e41c7`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "pendo__visitor_feature", "kind": "base", "block": null, "base_tables": ["pendo__visitor_feature"]}] | [] | ["visitor_id"] |
| B2 | [{"alias": "v", "kind": "base", "block": null, "base_tables": ["pendo__visitor"]}, {"alias": "fv", "kind": "derived", "block": "B1", "base_tables": ["pendo__visitor_feature"]}] | [{"type": "LEFT", "right": "(SELECT visitor_id, COUNT(DISTINCT feature_id) AS distinct_features FROM pendo__visitor_feature GROUP BY visitor_id) AS fv", "on": "fv.visitor_id = v.visitor_id", "using": []}] | ["CASE WHEN v.count_active_days > 60 AND fv.distinct_features < 5 THEN 'single_feature_heavy' ELSE 'normal' END"] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(DISTINCT feature_id) | [{"table": "pendo__visitor_feature", "column": "feature_id"}] | [] | False |
| B2 | AVG(v.average_daily_minutes) | [{"table": "pendo__visitor", "column": "average_daily_minutes"}] | [] | False |
| B2 | AVG(CASE WHEN v.count_active_days > 60 THEN v.average_daily_minutes END) | [{"table": "pendo__visitor", "column": "average_daily_minutes"}] | [{"table": "pendo__visitor", "column": "count_active_days"}] | False |


## S34

类别 `data`；来源 `query_db`；调用 `3480bdf8c1674cbfb30fab6201132326`；状态 `success`。

```sql
-- Get data for Python visualization: per-user metrics with segment
SELECT
  v.visitor_id,
  v.count_active_days,
  v.count_active_months,
  v.average_daily_minutes,
  v.average_daily_events,
  v.latest_nps_rating,
  v.sum_minutes,
  v.sum_events,
  v.first_event_on,
  v.last_event_on,
  a.avg_nps_rating AS account_avg_nps,
  COALESCE(fv.distinct_features, 0) AS distinct_features
FROM pendo__visitor v
LEFT JOIN (
  SELECT visitor_id, COUNT(DISTINCT feature_id) AS distinct_features
  FROM pendo__visitor_feature
  GROUP BY visitor_id
) fv ON fv.visitor_id = v.visitor_id
LEFT JOIN pendo__account a ON a.account_id = v.account_id
LIMIT 8000
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-079/attempt-01/sql/S34.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-079/attempt-01/sql/S34.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-079/attempt-01/results/S34.rows.jsonl)；完整：True；SHA256：`3eb1a59b3cd59f37413b0114e8c5576a699110d24ab696149a2e39ab8e996f9f`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "pendo__visitor_feature", "kind": "base", "block": null, "base_tables": ["pendo__visitor_feature"]}] | [] | ["visitor_id"] |
| B2 | [{"alias": "v", "kind": "base", "block": null, "base_tables": ["pendo__visitor"]}, {"alias": "fv", "kind": "derived", "block": "B1", "base_tables": ["pendo__visitor_feature"]}, {"alias": "a", "kind": "base", "block": null, "base_tables": ["pendo__account"]}] | [{"type": "LEFT", "right": "(SELECT visitor_id, COUNT(DISTINCT feature_id) AS distinct_features FROM pendo__visitor_feature GROUP BY visitor_id) AS fv", "on": "fv.visitor_id = v.visitor_id", "using": []}, {"type": "LEFT", "right": "pendo__account AS a", "on": "a.account_id = v.account_id", "using": []}] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(DISTINCT feature_id) | [{"table": "pendo__visitor_feature", "column": "feature_id"}] | [] | False |


## S35

类别 `data`；来源 `query_db`；调用 `616c46008d604e60a5cf2121904e0486`；状态 `success`。

```sql
-- Feature concentration data for Python
WITH single_feature_users AS (
  SELECT v.visitor_id
  FROM pendo__visitor v
  JOIN (SELECT visitor_id, COUNT(DISTINCT feature_id) AS distinct_features
        FROM pendo__visitor_feature GROUP BY visitor_id) fv ON fv.visitor_id = v.visitor_id
  WHERE v.count_active_days > 60 AND fv.distinct_features < 5
)
SELECT
  vf.visitor_id,
  vf.feature_id,
  f.feature_name,
  f.product_area_name,
  f.page_name,
  f.app_display_name,
  vf.sum_clicks,
  vf.sum_minutes,
  vf.avg_daily_minutes,
  vf.count_click_events
FROM pendo__visitor_feature vf
JOIN pendo__feature f ON f.feature_id = vf.feature_id
WHERE vf.visitor_id IN (SELECT visitor_id FROM single_feature_users)
ORDER BY vf.visitor_id, vf.sum_clicks DESC
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-079/attempt-01/sql/S35.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-079/attempt-01/sql/S35.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-079/attempt-01/results/S35.rows.jsonl)；完整：True；SHA256：`50b411757a857d98514b20deeb8274e5d065d8afea62aaed024932182ba22729`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "pendo__visitor_feature", "kind": "base", "block": null, "base_tables": ["pendo__visitor_feature"]}] | [] | ["visitor_id"] |
| B2 | [{"alias": "v", "kind": "base", "block": null, "base_tables": ["pendo__visitor"]}, {"alias": "fv", "kind": "derived", "block": "B1", "base_tables": ["pendo__visitor_feature"]}] | [{"type": "INNER", "right": "(SELECT visitor_id, COUNT(DISTINCT feature_id) AS distinct_features FROM pendo__visitor_feature GROUP BY visitor_id) AS fv", "on": "fv.visitor_id = v.visitor_id", "using": []}] | [] |
| B3 | [{"alias": "single_feature_users", "kind": "derived", "block": "B2", "base_tables": ["pendo__visitor", "pendo__visitor_feature"]}] | [] | [] |
| B4 | [{"alias": "vf", "kind": "base", "block": null, "base_tables": ["pendo__visitor_feature"]}, {"alias": "f", "kind": "base", "block": null, "base_tables": ["pendo__feature"]}] | [{"type": "INNER", "right": "pendo__feature AS f", "on": "f.feature_id = vf.feature_id", "using": []}] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(DISTINCT feature_id) | [{"table": "pendo__visitor_feature", "column": "feature_id"}] | [] | False |


## S36

类别 `data`；来源 `query_db`；调用 `dba8eb70afc846f6ac57190cb7136cb1`；状态 `success`。

```sql
-- Browser and OS breakdown for single-feature vs normal users
SELECT
  CASE WHEN v.count_active_days > 60 AND fv.distinct_features < 5 THEN 'single_feature_heavy' ELSE 'normal' END AS segment,
  v.last_browser_name,
  v.last_operating_system,
  COUNT(*) AS n_users,
  ROUND(AVG(v.average_daily_minutes), 2) AS avg_daily_min
FROM pendo__visitor v
LEFT JOIN (
  SELECT visitor_id, COUNT(DISTINCT feature_id) AS distinct_features
  FROM pendo__visitor_feature
  GROUP BY visitor_id
) fv ON fv.visitor_id = v.visitor_id
GROUP BY segment, v.last_browser_name, v.last_operating_system
ORDER BY segment, n_users DESC
LIMIT 20
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-079/attempt-01/sql/S36.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-079/attempt-01/sql/S36.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-079/attempt-01/results/S36.rows.jsonl)；完整：True；SHA256：`e3b9c88c8d532b77710f55670ac28600a71ca2a79f1bb36d0d45819d952db01a`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "pendo__visitor_feature", "kind": "base", "block": null, "base_tables": ["pendo__visitor_feature"]}] | [] | ["visitor_id"] |
| B2 | [{"alias": "v", "kind": "base", "block": null, "base_tables": ["pendo__visitor"]}, {"alias": "fv", "kind": "derived", "block": "B1", "base_tables": ["pendo__visitor_feature"]}] | [{"type": "LEFT", "right": "(SELECT visitor_id, COUNT(DISTINCT feature_id) AS distinct_features FROM pendo__visitor_feature GROUP BY visitor_id) AS fv", "on": "fv.visitor_id = v.visitor_id", "using": []}] | ["CASE WHEN v.count_active_days > 60 AND fv.distinct_features < 5 THEN 'single_feature_heavy' ELSE 'normal' END", "v.last_browser_name", "v.last_operating_system"] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(DISTINCT feature_id) | [{"table": "pendo__visitor_feature", "column": "feature_id"}] | [] | False |
| B2 | COUNT(*) | [] | [] | True |
| B2 | AVG(v.average_daily_minutes) | [{"table": "pendo__visitor", "column": "average_daily_minutes"}] | [] | False |


## S37

类别 `data`；来源 `query_db`；调用 `02649e1f379c4470b05fe431062a03d1`；状态 `success`。

```sql
-- App/platform breakdown: which app do single-feature users primarily use?
SELECT
  f.app_display_name,
  f.app_platform,
  COUNT(DISTINCT vf.visitor_id) AS n_single_feature_users,
  ROUND(AVG(v.average_daily_minutes), 2) AS avg_daily_min
FROM pendo__visitor_feature vf
JOIN pendo__feature f ON f.feature_id = vf.feature_id
JOIN pendo__visitor v ON v.visitor_id = vf.visitor_id
WHERE v.count_active_days > 60
  AND (SELECT COUNT(DISTINCT vf2.feature_id) FROM pendo__visitor_feature vf2 WHERE vf2.visitor_id = v.visitor_id) < 5
  AND f.app_display_name IS NOT NULL
GROUP BY f.app_display_name, f.app_platform
ORDER BY n_single_feature_users DESC
LIMIT 15
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-079/attempt-01/sql/S37.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-079/attempt-01/sql/S37.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-079/attempt-01/results/S37.rows.jsonl)；完整：True；SHA256：`5284a5be73339cb1a5c0252aad86d50313287ef4d56266614747879fc86fdc51`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "vf2", "kind": "base", "block": null, "base_tables": ["pendo__visitor_feature"]}] | [] | [] |
| B2 | [{"alias": "vf", "kind": "base", "block": null, "base_tables": ["pendo__visitor_feature"]}, {"alias": "f", "kind": "base", "block": null, "base_tables": ["pendo__feature"]}, {"alias": "v", "kind": "base", "block": null, "base_tables": ["pendo__visitor"]}] | [{"type": "INNER", "right": "pendo__feature AS f", "on": "f.feature_id = vf.feature_id", "using": []}, {"type": "INNER", "right": "pendo__visitor AS v", "on": "v.visitor_id = vf.visitor_id", "using": []}] | ["f.app_display_name", "f.app_platform"] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(DISTINCT vf2.feature_id) | [{"table": "pendo__visitor_feature", "column": "feature_id"}] | [] | False |
| B2 | COUNT(DISTINCT vf.visitor_id) | [{"table": "pendo__visitor_feature", "column": "visitor_id"}] | [] | False |
| B2 | AVG(v.average_daily_minutes) | [{"table": "pendo__visitor", "column": "average_daily_minutes"}] | [] | False |


## S38

类别 `data`；来源 `query_db`；调用 `3e717c0f19db43df9bc259761be45316`；状态 `success`。

```sql
-- Final check: is there a correlation between distinct features and daily minutes for the heavy users?
-- This helps understand the "dose-response" relationship
SELECT
  fv.distinct_features,
  COUNT(*) AS n_users,
  ROUND(AVG(v.average_daily_minutes), 2) AS avg_daily_min,
  ROUND(AVG(v.latest_nps_rating), 3) AS avg_nps,
  ROUND(AVG(v.count_active_days), 1) AS avg_active_days,
  ROUND(AVG(v.count_active_months), 2) AS avg_active_months
FROM pendo__visitor v
JOIN (
  SELECT visitor_id, COUNT(DISTINCT feature_id) AS distinct_features
  FROM pendo__visitor_feature
  GROUP BY visitor_id
) fv ON fv.visitor_id = v.visitor_id
WHERE v.count_active_days > 60
GROUP BY fv.distinct_features
ORDER BY fv.distinct_features
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-079/attempt-01/sql/S38.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-079/attempt-01/sql/S38.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-079/attempt-01/results/S38.rows.jsonl)；完整：True；SHA256：`207dbd81ee4fa48da2a4b3c144a916a9808415597edf567f7657bd3ba45311b2`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "pendo__visitor_feature", "kind": "base", "block": null, "base_tables": ["pendo__visitor_feature"]}] | [] | ["visitor_id"] |
| B2 | [{"alias": "v", "kind": "base", "block": null, "base_tables": ["pendo__visitor"]}, {"alias": "fv", "kind": "derived", "block": "B1", "base_tables": ["pendo__visitor_feature"]}] | [{"type": "INNER", "right": "(SELECT visitor_id, COUNT(DISTINCT feature_id) AS distinct_features FROM pendo__visitor_feature GROUP BY visitor_id) AS fv", "on": "fv.visitor_id = v.visitor_id", "using": []}] | ["fv.distinct_features"] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(DISTINCT feature_id) | [{"table": "pendo__visitor_feature", "column": "feature_id"}] | [] | False |
| B2 | COUNT(*) | [] | [] | True |
| B2 | AVG(v.average_daily_minutes) | [{"table": "pendo__visitor", "column": "average_daily_minutes"}] | [] | False |
| B2 | AVG(v.latest_nps_rating) | [{"table": "pendo__visitor", "column": "latest_nps_rating"}] | [] | False |
| B2 | AVG(v.count_active_days) | [{"table": "pendo__visitor", "column": "count_active_days"}] | [] | False |
| B2 | AVG(v.count_active_months) | [{"table": "pendo__visitor", "column": "count_active_months"}] | [] | False |

