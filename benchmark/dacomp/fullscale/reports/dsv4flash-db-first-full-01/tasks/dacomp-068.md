# dacomp-068

The finance department has allocated a Q4 marketing budget of $5,000,000, which needs to b…

运行：已提交。官方未评分。全部 SQL 尝试/成功 41/40；数据 SQL 38/37；Python 8 次。

完整原题：

The finance department has allocated a Q4 marketing budget of $5,000,000, which needs to be reallocated among 8 apps. Please analyze markets with a `store_conversion_rate` greater than 15% but an `avg_daily_revenue` below $5, as well as markets with an `avg_daily_revenue` over $7 but a `store_conversion_rate` below 10%. Based on this analysis, develop specific budget allocation recommendations for each app, with a required expected ROI of no less than 25%.

| 表 | 行数 | 列数 |
| --- | --- | --- |
| google_play__comprehensive_performance_dashboard | 15732 | 37 |
| google_play__geo_market_analysis | 13 | 39 |
| google_play__product_portfolio_analysis | 8 | 24 |


实际路线（分析者依据 SQL/源码概括，不代表 Agent 自述）：SQL 筛选转化与收入错配市场 → Python 地域汇总、连接及预算评分情景 → 应用投资分配建议。

数据库大小：2,510,848 字节。

## 数据 SQL

| SQL | 状态 | 基础表 | Join 输入/类型 | GROUP BY | 聚合表达式 | 结果行数 | 数据库 ms |
| --- | --- | --- | --- | --- | --- | --- | --- |
| [S4/Q1](#s4) | success | ["google_play__geo_market_analysis"] | 0 / {} | [] | [] | 8 | 0.306 |
| [S5/Q2](#s5) | success | ["google_play__product_portfolio_analysis"] | 0 / {} | [] | [] | 8 | 0.302 |
| [S6/Q3](#s6) | success | ["google_play__comprehensive_performance_dashboard"] | 0 / {} | [] | [] | 8 | 6.515 |
| [S7/Q4](#s7) | success | ["google_play__geo_market_analysis"] | 0 / {} | [] | ["COUNT(*)", "COUNT(DISTINCT package_name)", "COUNT(DISTINCT country)"] | 1 | 0.441 |
| [S8/Q5](#s8) | success | ["google_play__comprehensive_performance_dashboard"] | 0 / {} | [] | ["MIN(date_day)", "MAX(date_day)", "COUNT(*)"] | 1 | 2.973 |
| [S9/Q6](#s9) | success | ["google_play__product_portfolio_analysis"] | 0 / {} | [] | [] | 8 | 0.354 |
| [S10/Q7](#s10) | success | ["google_play__geo_market_analysis"] | 0 / {} | [] | [] | 13 | 0.392 |
| [S11/Q8](#s11) | success | ["google_play__geo_market_analysis"] | 0 / {} | [] | [] | 13 | 0.509 |
| [S12/Q9](#s12) | success | ["google_play__geo_market_analysis"] | 0 / {} | [] | [] | 3 | 0.385 |
| [S13/Q10](#s13) | success | ["google_play__geo_market_analysis"] | 0 / {} | ["package_name"] | ["COUNT(*)", "SUM(CASE WHEN store_conversion_rate > 15 AND avg_daily_revenue < 5 THEN 1 ELSE 0 END)", "SUM(CASE WHEN avg_daily_revenue > 7 AND store_conversion_rate < 10 THEN 1 ELSE 0 END)"] | 8 | 0.378 |
| [S14/Q11](#s14) | success | ["google_play__comprehensive_performance_dashboard"] | 0 / {} | ["package_name"] | ["COUNT(*)", "MIN(date_day)", "MAX(date_day)", "SUM(daily_net_revenue)", "AVG(daily_net_revenue)", "SUM(daily_installs)", "SUM(store_acquisitions)", "SUM(store_visitors)"] | 8 | 13.805 |
| [S15/Q12](#s15) | success | ["google_play__comprehensive_performance_dashboard"] | 0 / {} | [] | [] | 30 | 4.204 |
| [S16/Q13](#s16) | success | ["google_play__comprehensive_performance_dashboard"] | 0 / {} | [] | ["COUNT(*)", "SUM(CASE WHEN store_visitors > 0 THEN 1 ELSE 0 END)", "SUM(CASE WHEN store_acquisitions > 0 THEN 1 ELSE 0 END)", "SUM(CASE WHEN NOT store_conversion_rate IS NULL THEN 1 ELSE 0 END)", "SUM(store_visitors)", "SUM(store_acquisitions)"] | 1 | 5.868 |
| [S17/Q14](#s17) | success | ["google_play__comprehensive_performance_dashboard"] | 0 / {} | ["package_name"] | ["COUNT(*)", "SUM(CASE WHEN store_visitors > 0 THEN 1 ELSE 0 END)", "SUM(store_visitors)", "SUM(store_acquisitions)", "SUM(daily_net_revenue)"] | 8 | 9.928 |
| [S18/Q15](#s18) | success | ["google_play__comprehensive_performance_dashboard"] | 0 / {} | ["package_name"] | ["SUM(daily_net_revenue)", "SUM(store_visitors)", "SUM(store_acquisitions)", "SUM(daily_installs)", "SUM(daily_net_revenue)", "SUM(store_acquisitions)", "SUM(store_acquisitions)", "SUM(store_visitors)"] | 8 | 4.25 |
| [S19/Q16](#s19) | success | ["google_play__geo_market_analysis"] | 0 / {} | ["package_name"] | ["AVG(avg_daily_revenue)", "AVG(store_conversion_rate)", "AVG(revenue_last_30_days)", "SUM(store_visitors_30d)", "SUM(store_installs_30d)"] | 8 | 0.444 |
| [S20/Q17](#s20) | success | ["google_play__comprehensive_performance_dashboard"] | 0 / {} | ["STRFTIME('%Y-%m', date_day)"] | ["COUNT(*)", "SUM(store_visitors)", "SUM(store_acquisitions)", "SUM(daily_net_revenue)"] | 60 | 13.615 |
| [S21/Q18](#s21) | success | ["google_play__comprehensive_performance_dashboard"] | 0 / {} | [] | ["MAX(date_day)"] | 8 | 24650.679 |
| [S22/Q19](#s22) | success | ["google_play__geo_market_analysis"] | 0 / {} | ["package_name"] | ["SUM(revenue_opportunity_score)", "AVG(revenue_opportunity_score)", "SUM(growth_potential_score)", "AVG(growth_potential_score)", "SUM(user_quality_score)", "AVG(user_quality_score)", "SUM(store_performance_score)", "AVG(store_performance_score)", "SUM(overall_market_score)", "AVG(overall_market_score)"] | 8 | 0.423 |
| [S23/Q20](#s23) | success | ["google_play__product_portfolio_analysis"] | 0 / {} | [] | [] | 8 | 0.419 |
| [S24/Q21](#s24) | success | ["google_play__geo_market_analysis"] | 0 / {} | [] | [] | 13 | 0.419 |
| [S25/Q22](#s25) | success | ["google_play__product_portfolio_analysis"] | 0 / {} | [] | [] | 8 | 0.295 |
| [S26/Q23](#s26) | success | ["google_play__comprehensive_performance_dashboard"] | 0 / {} | ["package_name"] | ["SUM(daily_net_revenue)", "SUM(store_visitors)", "SUM(store_acquisitions)", "SUM(daily_net_revenue)", "SUM(store_acquisitions)", "SUM(store_acquisitions)", "SUM(store_visitors)"] | 8 | 4.104 |
| [S27/Q24](#s27) | success | ["google_play__geo_market_analysis"] | 0 / {} | [] | [] | 13 | 0.508 |
| [S28/Q25](#s28) | success | ["google_play__product_portfolio_analysis"] | 0 / {} | [] | [] | 8 | 0.336 |
| [S29/Q26](#s29) | success | ["google_play__comprehensive_performance_dashboard"] | 0 / {} | ["package_name"] | ["SUM(daily_net_revenue)", "SUM(store_visitors)", "SUM(store_acquisitions)"] | 8 | 4.038 |
| [S30/Q27](#s30) | success | ["google_play__geo_market_analysis"] | 0 / {} | [] | [] | 13 | 0.372 |
| [S31/Q28](#s31) | success | ["google_play__product_portfolio_analysis"] | 0 / {} | [] | [] | 8 | 0.258 |
| [S32/Q29](#s32) | success | ["google_play__geo_market_analysis"] | 0 / {} | [] | [] | 13 | 0.433 |
| [S33/Q30](#s33) | success | ["google_play__product_portfolio_analysis"] | 0 / {} | [] | [] | 8 | 0.266 |
| [S34/Q31](#s34) | success | ["google_play__geo_market_analysis"] | 0 / {} | [] | [] | 13 | 0.368 |
| [S35/Q32](#s35) | success | ["google_play__product_portfolio_analysis"] | 0 / {} | [] | [] | 8 | 0.259 |
| [S36/Q33](#s36) | success | ["google_play__geo_market_analysis"] | 0 / {} | [] | [] | 13 | 0.461 |
| [S37/Q34](#s37) | success | ["google_play__geo_market_analysis"] | 0 / {} | [] | [] | 2 | 0.345 |
| [S38/Q35](#s38) | success | ["google_play__geo_market_analysis"] | 0 / {} | [] | [] | 2 | 0.312 |
| [S39/Q36](#s39) | failed | ["google_play__geo_market_analysis"] | 2 / {'INNER': 1} | ["seg"] | ["COUNT(*)", "COUNT(DISTINCT package_name)", "SUM(g.store_visitors_30d)", "SUM(g.store_installs_30d)", "SUM(g.revenue_last_30_days)", "AVG(g.store_conversion_rate)", "AVG(g.avg_daily_revenue)"] | unknown | 未取得；调用总时长 0.212 ms |
| [S40/Q37](#s40) | success | ["google_play__product_portfolio_analysis"] | 0 / {} | [] | [] | 8 | 0.388 |
| [S41/Q38](#s41) | success | ["google_play__geo_market_analysis"] | 2 / {'INNER': 1} | ["s.seg"] | ["COUNT(*)", "COUNT(DISTINCT g.package_name)", "SUM(g.store_visitors_30d)", "SUM(g.store_installs_30d)", "SUM(g.revenue_last_30_days)", "AVG(g.store_conversion_rate)", "AVG(g.avg_daily_revenue)"] | 3 | 0.527 |


## 元数据和设置

| SQL | 类别 | 状态 | 内容 |
| --- | --- | --- | --- |
| S1 | connection_setup | success | PRAGMA query_only=ON |
| S2 | metadata | success | SELECT name,sql FROM sqlite_master WHERE type='table' ORDER BY name |
| S3 | metadata | success | SELECT name FROM sqlite_master WHERE type='table' |


## Python 与执行位置

人工源码审查：**database_first_violation**。Python 对应用地域数据分组、连接组合与看板数据，并进行常规评分、预算份额和预期 ROI 情景计算。协议明确要求这些数据库可支持的运算优先在 SQL 完成；图表并非全部迁出的理由。 [证据](../reviews/dacomp-068.json)。

P1：I need to aggregate the geo market analysis data with the product portfolio data to build a comprehensive analysis of the two market segments, compute weighted scores, and produce a budget allocation model. I also need to generate visualizations. This is a complex multi-step aggregation and scoring that benefits from Python's flexibility for the final model.

[源码](../../../runs/dsv4flash-db-first-full-01/dacomp-068/attempt-01/python/P1.py)；[输出](../../../runs/dsv4flash-db-first-full-01/dacomp-068/attempt-01/python/P1.stdout)；[错误](../../../runs/dsv4flash-db-first-full-01/dacomp-068/attempt-01/python/P1.stderr)。检出需人工核验的 SQL 可实现操作：groupby(, .query(；不能仅凭理由判为合规。

P2：Build the budget allocation model using Python for flexibility in scoring and weighting. I will compute a composite opportunity score per app from geo market scores and portfolio metrics, then allocate $5M proportionally, and estimate the expected ROI using the relationship between store visitors, conversion rate, and revenue per user.

[源码](../../../runs/dsv4flash-db-first-full-01/dacomp-068/attempt-01/python/P2.py)；[输出](../../../runs/dsv4flash-db-first-full-01/dacomp-068/attempt-01/python/P2.stdout)；[错误](../../../runs/dsv4flash-db-first-full-01/dacomp-068/attempt-01/python/P2.stderr)。检出需人工核验的 SQL 可实现操作：groupby(, .merge(, .query(, sort_values(；不能仅凭理由判为合规。

P3：The sklearn module is not available, so I will implement min-max normalization manually in pandas/numpy for the budget allocation scoring model.

[源码](../../../runs/dsv4flash-db-first-full-01/dacomp-068/attempt-01/python/P3.py)；[输出](../../../runs/dsv4flash-db-first-full-01/dacomp-068/attempt-01/python/P3.stdout)；[错误](../../../runs/dsv4flash-db-first-full-01/dacomp-068/attempt-01/python/P3.stderr)。检出需人工核验的 SQL 可实现操作：groupby(, .merge(, .query(, sort_values(；不能仅凭理由判为合规。

P4：Check the column names after merging portfolio and geo_agg to resolve the KeyError in the previous execution.

[源码](../../../runs/dsv4flash-db-first-full-01/dacomp-068/attempt-01/python/P4.py)；[输出](../../../runs/dsv4flash-db-first-full-01/dacomp-068/attempt-01/python/P4.stdout)；[错误](../../../runs/dsv4flash-db-first-full-01/dacomp-068/attempt-01/python/P4.stderr)。检出需人工核验的 SQL 可实现操作：groupby(, .merge(, .query(；不能仅凭理由判为合规。

P5：Build the final budget allocation and expected ROI model. The scoring, weighting, ROI computation, and visualization steps require flexible data manipulation that is clearer in Python. The SQL engine already provided the base aggregates; here I combine them into the final deliverable model.

[源码](../../../runs/dsv4flash-db-first-full-01/dacomp-068/attempt-01/python/P5.py)；[输出](../../../runs/dsv4flash-db-first-full-01/dacomp-068/attempt-01/python/P5.stdout)；[错误](../../../runs/dsv4flash-db-first-full-01/dacomp-068/attempt-01/python/P5.stderr)。检出需人工核验的 SQL 可实现操作：groupby(, .merge(, .query(, sort_values(；不能仅凭理由判为合规。

P6：Create visualizations: scatter plot of conversion rate vs revenue (segment coloring), budget allocation bar chart, and expected ROI bar chart. These visualizations help communicate the analysis clearly.

[源码](../../../runs/dsv4flash-db-first-full-01/dacomp-068/attempt-01/python/P6.py)；[输出](../../../runs/dsv4flash-db-first-full-01/dacomp-068/attempt-01/python/P6.stdout)；[错误](../../../runs/dsv4flash-db-first-full-01/dacomp-068/attempt-01/python/P6.stderr)。自动源码筛查未检出预设迁出信号；这不是全面语义合规证明。

P7：Fix the matplotlib math text issue by escaping dollar signs in labels, and recreate the three main figures.

[源码](../../../runs/dsv4flash-db-first-full-01/dacomp-068/attempt-01/python/P7.py)；[输出](../../../runs/dsv4flash-db-first-full-01/dacomp-068/attempt-01/python/P7.stdout)；[错误](../../../runs/dsv4flash-db-first-full-01/dacomp-068/attempt-01/python/P7.stderr)。自动源码筛查未检出预设迁出信号；这不是全面语义合规证明。

P8：Load the final allocation data and format it into a clean summary table for the report. Also compute the per-app details for the segmentation analysis.

[源码](../../../runs/dsv4flash-db-first-full-01/dacomp-068/attempt-01/python/P8.py)；[输出](../../../runs/dsv4flash-db-first-full-01/dacomp-068/attempt-01/python/P8.stdout)；[错误](../../../runs/dsv4flash-db-first-full-01/dacomp-068/attempt-01/python/P8.stderr)。自动源码筛查未检出预设迁出信号；这不是全面语义合规证明。

## 优化机会

已验证候选。筛选限于精确 SQL、相同自包含 CTE、相同单表完整过滤、可分解单表聚合；未覆盖任意 Join 等价和一般谓词蕴含。全部候选都是 offline，未测在线预测。

| 候选 | 类型 | 已有结果 | 覆盖 SQL | 后续次数 | 中间行数 | 验证 | 成本 |
| --- | --- | --- | --- | --- | --- | --- | --- |
| C1 | exact-result reuse | True | ["S11", "S24"] | 1 | unknown | not_verified_cap | Not tested |
| C2 | exact-result reuse | True | ["S23", "S25"] | 1 | unknown | not_verified_cap | Not tested |
| C3 | exact-result reuse | True | ["S27", "S30", "S32", "S34"] | 3 | 13 | verified | Not benchmarked; correctness alone does not establish net speedup. |
| C4 | exact-result reuse | True | ["S28", "S31", "S33", "S35"] | 3 | 8 | verified | Not benchmarked; correctness alone does not establish net speedup. |
| C5 | aggregate MV | False | ["S13", "S19", "S22"] | 2 | unknown | not_verified_cap | Not tested |
| C6 | aggregate MV | False | ["S8", "S14", "S16", "S17", "S20"] | 4 | 480 | verified | Not benchmarked; correctness alone does not establish net speedup. |
| C7 | common filtered view | False | ["S18", "S26", "S29"] | 2 | unknown | not_verified_cap | Not tested |
| C8 | aggregate MV | False | ["S18", "S26", "S29"] | 2 | unknown | not_verified_cap | Not tested |
| C9 | common filtered view | False | ["S37", "S38"] | 1 | unknown | not_verified_cap | Not tested |


已验证覆盖（含触发查询、候选并集去重）：13/37 条成功数据 SQL。正确性仅针对当前数据库快照；未测性能的候选不能声称已加速。

[完整 build/rewrite 与比较证据](dacomp-068.analysis.json)。

### C6：aggregate MV

Union of grouping keys; decomposable aggregate states; AVG uses SUM and non-NULL COUNT.

原查询 [S8](#s8), [S14](#s14), [S16](#s16), [S17](#s17), [S20](#s20) → 新增共享状态 C6 → 后续 4 次可复用。该构建点为事后假设，不代表 Agent 当时预知后续。

构建定义：

```sql
SELECT package_name AS __g0, STRFTIME('%Y-%m', date_day) AS __g1, MIN(date_day) AS __a0, MAX(date_day) AS __a1, COUNT(*) AS __a2, SUM(daily_net_revenue) AS __a3, SUM(daily_net_revenue) AS __a4_sum, COUNT(daily_net_revenue) AS __a4_n, SUM(daily_installs) AS __a5, SUM(store_acquisitions) AS __a6, SUM(store_visitors) AS __a7, SUM(CASE WHEN store_visitors > 0 THEN 1 ELSE 0 END) AS __a8, SUM(CASE WHEN store_acquisitions > 0 THEN 1 ELSE 0 END) AS __a9, SUM(CASE WHEN NOT store_conversion_rate IS NULL THEN 1 ELSE 0 END) AS __a10 FROM "google_play__comprehensive_performance_dashboard"  GROUP BY package_name, STRFTIME('%Y-%m', date_day)
```

受益查询 S8 的改写示例：

```sql
SELECT MIN(__a0) AS min_d, MAX(__a1) AS max_d, SUM(__a2) AS n FROM temp.reuse_candidate
```

| 原 SQL | 列名一致 | 结果一致 | 比较方法 |
| --- | --- | --- | --- |
| S8 | True | True | exact_multiset |
| S14 | True | True | ordered_numeric_tolerance |
| S16 | True | True | exact_multiset |
| S17 | True | True | ordered_numeric_tolerance |
| S20 | True | True | ordered_numeric_tolerance |


验证状态：verified；成本结论：Not benchmarked; correctness alone does not establish net speedup.

### C3：exact-result reuse

Identical normalized SQL and parameters; archive equality checked.

原查询 [S27](#s27), [S30](#s30), [S32](#s32), [S34](#s34) → 保留前序结果 S27 → 后续 3 次可复用。该构建点为事后假设，不代表 Agent 当时预知后续。

| 原 SQL | 列名一致 | 结果一致 | 比较方法 |
| --- | --- | --- | --- |
| S30 | True | True | exact_multiset |
| S32 | True | True | exact_multiset |
| S34 | True | True | exact_multiset |


验证状态：verified；成本结论：Not benchmarked; correctness alone does not establish net speedup.

### C4：exact-result reuse

Identical normalized SQL and parameters; archive equality checked.

原查询 [S28](#s28), [S31](#s31), [S33](#s33), [S35](#s35) → 保留前序结果 S28 → 后续 3 次可复用。该构建点为事后假设，不代表 Agent 当时预知后续。

| 原 SQL | 列名一致 | 结果一致 | 比较方法 |
| --- | --- | --- | --- |
| S31 | True | True | exact_multiset |
| S33 | True | True | exact_multiset |
| S35 | True | True | exact_multiset |


验证状态：verified；成本结论：Not benchmarked; correctness alone does not establish net speedup.

结果依赖：自动记录 SQL→Python 的接口父调用，以及源码中引用归档文件的消费者；字面值相同不认定因果。模型方向选择需要人工读取消息，尚未做全面因果标注。

[原始报告](../../../runs/dsv4flash-db-first-full-01/dacomp-068/attempt-01/answer.md)；[统一消息](../../../runs/dsv4flash-db-first-full-01/dacomp-068/attempt-01/messages.jsonl)；[原始 OpenCode 事件](../../../runs/dsv4flash-db-first-full-01/dacomp-068/attempt-01/opencode.jsonl)；[SQL 引擎日志](../../../runs/dsv4flash-db-first-full-01/dacomp-068/attempt-01/sql_journal.jsonl)。

[可读报告（本地图片链接规范化）](../answers/dacomp-068.md)。原始回答保留，分析结论未改写。

## S1

类别 `connection_setup`；来源 `connection`；调用 `a594f3c9768a49c294f3676840ddad91`；状态 `success`。

```sql
PRAGMA query_only=ON
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-068/attempt-01/sql/S1.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-068/attempt-01/sql/S1.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-068/attempt-01/results/S1.rows.jsonl)；完整：True；SHA256：`e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`。

## S2

类别 `metadata`；来源 `list_db`；调用 `a594f3c9768a49c294f3676840ddad91`；状态 `success`。

```sql
SELECT name,sql FROM sqlite_master WHERE type='table' ORDER BY name
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-068/attempt-01/sql/S2.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-068/attempt-01/sql/S2.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-068/attempt-01/results/S2.rows.jsonl)；完整：True；SHA256：`e48f18966f0e6a07e8d66eedfebd56ebc67ac0ef691bbfe654440c321d4c3794`。

## S3

类别 `metadata`；来源 `query_db`；调用 `49c827978f614df2be53f4ce866f121e`；状态 `success`。

```sql
SELECT name FROM sqlite_master WHERE type='table'
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-068/attempt-01/sql/S3.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-068/attempt-01/sql/S3.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-068/attempt-01/results/S3.rows.jsonl)；完整：True；SHA256：`db4c9bc028aebafa2521931f1272b66f5a7995ac7bef261ec01f358e2a231d80`。

## S4

类别 `data`；来源 `query_db`；调用 `150de888b5d9438bbc46fbd7cf54f78f`；状态 `success`。

```sql
SELECT DISTINCT package_name FROM google_play__geo_market_analysis ORDER BY package_name
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-068/attempt-01/sql/S4.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-068/attempt-01/sql/S4.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-068/attempt-01/results/S4.rows.jsonl)；完整：True；SHA256：`0302491c5d02c3d8abba5041594164026f8dd02913af29884ed81ead3921de61`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "google_play__geo_market_analysis", "kind": "base", "block": null, "base_tables": ["google_play__geo_market_analysis"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |


## S5

类别 `data`；来源 `query_db`；调用 `81a0affac2c34ea4b11b7fb038a3993e`；状态 `success`。

```sql
SELECT DISTINCT package_name FROM google_play__product_portfolio_analysis ORDER BY package_name
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-068/attempt-01/sql/S5.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-068/attempt-01/sql/S5.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-068/attempt-01/results/S5.rows.jsonl)；完整：True；SHA256：`0302491c5d02c3d8abba5041594164026f8dd02913af29884ed81ead3921de61`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "google_play__product_portfolio_analysis", "kind": "base", "block": null, "base_tables": ["google_play__product_portfolio_analysis"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |


## S6

类别 `data`；来源 `query_db`；调用 `85a6ea8214ef4404bd9eef7fe0c1618b`；状态 `success`。

```sql
SELECT DISTINCT package_name FROM google_play__comprehensive_performance_dashboard ORDER BY package_name
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-068/attempt-01/sql/S6.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-068/attempt-01/sql/S6.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-068/attempt-01/results/S6.rows.jsonl)；完整：True；SHA256：`0302491c5d02c3d8abba5041594164026f8dd02913af29884ed81ead3921de61`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "google_play__comprehensive_performance_dashboard", "kind": "base", "block": null, "base_tables": ["google_play__comprehensive_performance_dashboard"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |


## S7

类别 `data`；来源 `query_db`；调用 `cbf53145e9e641819b7285b2130c7a74`；状态 `success`。

```sql
SELECT COUNT(*) AS n_rows, COUNT(DISTINCT package_name) AS n_apps, COUNT(DISTINCT country) AS n_countries FROM google_play__geo_market_analysis
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-068/attempt-01/sql/S7.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-068/attempt-01/sql/S7.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-068/attempt-01/results/S7.rows.jsonl)；完整：True；SHA256：`67137ef747af589d002750459d6c4dfcb26da4ea874cc0e7f98f878475e1bece`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "google_play__geo_market_analysis", "kind": "base", "block": null, "base_tables": ["google_play__geo_market_analysis"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |
| B1 | COUNT(DISTINCT package_name) | [{"table": "google_play__geo_market_analysis", "column": "package_name"}] | [] | False |
| B1 | COUNT(DISTINCT country) | [{"table": "google_play__geo_market_analysis", "column": "country"}] | [] | False |


## S8

类别 `data`；来源 `query_db`；调用 `6e36bccdb9f94754b73b886251c2b955`；状态 `success`。

```sql
SELECT MIN(date_day) AS min_d, MAX(date_day) AS max_d, COUNT(*) AS n FROM google_play__comprehensive_performance_dashboard
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-068/attempt-01/sql/S8.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-068/attempt-01/sql/S8.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-068/attempt-01/results/S8.rows.jsonl)；完整：True；SHA256：`49d025d9194f37cdb08e2e1e3c5bb44bb9cda1069b345a2e3e7af8918439a721`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "google_play__comprehensive_performance_dashboard", "kind": "base", "block": null, "base_tables": ["google_play__comprehensive_performance_dashboard"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | MIN(date_day) | [{"table": "google_play__comprehensive_performance_dashboard", "column": "date_day"}] | [] | False |
| B1 | MAX(date_day) | [{"table": "google_play__comprehensive_performance_dashboard", "column": "date_day"}] | [] | False |
| B1 | COUNT(*) | [] | [] | True |


## S9

类别 `data`；来源 `query_db`；调用 `6512d1c90c034c1a8cd5bf6e4de48896`；状态 `success`。

```sql
SELECT package_name, total_products, total_revenue_30d, avg_daily_revenue, total_installs_30d, avg_active_devices, total_markets, portfolio_health_score, bcg_matrix_category, investment_priority, growth_stage FROM google_play__product_portfolio_analysis ORDER BY avg_daily_revenue DESC
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-068/attempt-01/sql/S9.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-068/attempt-01/sql/S9.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-068/attempt-01/results/S9.rows.jsonl)；完整：True；SHA256：`4cf6c7af0b5240e3d123299feeb9d3beb3578e2b0d6f374941e3fee1f7213eda`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "google_play__product_portfolio_analysis", "kind": "base", "block": null, "base_tables": ["google_play__product_portfolio_analysis"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |


## S10

类别 `data`；来源 `query_db`；调用 `ae36e4ae4819473fbfab42590c4e3061`；状态 `success`。

```sql
SELECT package_name, country, country_name, region, sub_region, avg_daily_revenue, store_conversion_rate, revenue_last_30_days, store_visitors_30d, store_installs_30d, market_tier, opportunity_type, investment_recommendation, overall_market_score, revenue_opportunity_score, growth_potential_score FROM google_play__geo_market_analysis ORDER BY package_name, country
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-068/attempt-01/sql/S10.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-068/attempt-01/sql/S10.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-068/attempt-01/results/S10.rows.jsonl)；完整：True；SHA256：`4c28c853659e416b13b36ec2706164e1e2fe87b59dc17457d6f0e87dac69e0ea`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "google_play__geo_market_analysis", "kind": "base", "block": null, "base_tables": ["google_play__geo_market_analysis"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |


## S11

类别 `data`；来源 `query_db`；调用 `7d71e2e539d94c14a32ab28c1c2e5e8b`；状态 `success`。

```sql
SELECT * FROM google_play__geo_market_analysis ORDER BY package_name, country
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-068/attempt-01/sql/S11.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-068/attempt-01/sql/S11.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-068/attempt-01/results/S11.rows.jsonl)；完整：True；SHA256：`04036eb6e0435a4947fae341e76c9e86bb18b1abe3044d157aa8bb76c727f04a`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "google_play__geo_market_analysis", "kind": "base", "block": null, "base_tables": ["google_play__geo_market_analysis"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |


## S12

类别 `data`；来源 `query_db`；调用 `f4db6b5ea4da4cd7a1651a5b2da53186`；状态 `success`。

```sql
SELECT package_name, country, country_name, avg_daily_revenue, store_conversion_rate, revenue_last_30_days, store_visitors_30d, store_installs_30d, market_tier, opportunity_type, investment_recommendation, overall_market_score FROM google_play__geo_market_analysis WHERE package_name IN ('com.trial.education','com.dev.photoeditor','com.test.fitness') ORDER BY package_name
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-068/attempt-01/sql/S12.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-068/attempt-01/sql/S12.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-068/attempt-01/results/S12.rows.jsonl)；完整：True；SHA256：`28d6b8ed362489e7f80178fe98b8f6baf8521cc6582eab2bbb432b2290671ffe`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "google_play__geo_market_analysis", "kind": "base", "block": null, "base_tables": ["google_play__geo_market_analysis"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |


## S13

类别 `data`；来源 `query_db`；调用 `d6b82e98c90b46ef9a30111b92f70218`；状态 `success`。

```sql
SELECT package_name, COUNT(*) AS n_markets, SUM(CASE WHEN store_conversion_rate > 15 AND avg_daily_revenue < 5 THEN 1 ELSE 0 END) AS seg_high_conv_low_rev, SUM(CASE WHEN avg_daily_revenue > 7 AND store_conversion_rate < 10 THEN 1 ELSE 0 END) AS seg_high_rev_low_conv FROM google_play__geo_market_analysis GROUP BY package_name ORDER BY package_name
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-068/attempt-01/sql/S13.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-068/attempt-01/sql/S13.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-068/attempt-01/results/S13.rows.jsonl)；完整：True；SHA256：`4865d438f7089917e443e5b8d91ca944d46dd94739491f5d8433d07d0b1b9a83`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "google_play__geo_market_analysis", "kind": "base", "block": null, "base_tables": ["google_play__geo_market_analysis"]}] | [] | ["package_name"] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |
| B1 | SUM(CASE WHEN store_conversion_rate > 15 AND avg_daily_revenue < 5 THEN 1 ELSE 0 END) | [] | [{"table": "google_play__geo_market_analysis", "column": "store_conversion_rate"}, {"table": "google_play__geo_market_analysis", "column": "avg_daily_revenue"}] | False |
| B1 | SUM(CASE WHEN avg_daily_revenue > 7 AND store_conversion_rate < 10 THEN 1 ELSE 0 END) | [] | [{"table": "google_play__geo_market_analysis", "column": "avg_daily_revenue"}, {"table": "google_play__geo_market_analysis", "column": "store_conversion_rate"}] | False |


## S14

类别 `data`；来源 `query_db`；调用 `6373280ad3f64b908d8561d709262957`；状态 `success`。

```sql
SELECT package_name, COUNT(*) AS n_days, MIN(date_day) AS first_day, MAX(date_day) AS last_day, SUM(daily_net_revenue) AS total_rev, AVG(daily_net_revenue) AS avg_daily_rev, SUM(daily_installs) AS total_installs, SUM(store_acquisitions) AS total_acq, SUM(store_visitors) AS total_visitors FROM google_play__comprehensive_performance_dashboard GROUP BY package_name ORDER BY avg_daily_rev DESC
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-068/attempt-01/sql/S14.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-068/attempt-01/sql/S14.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-068/attempt-01/results/S14.rows.jsonl)；完整：True；SHA256：`65c6500ac5e70b070e02e5f86155229b7860e3d0923d8f5503015dbc73a465a3`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "google_play__comprehensive_performance_dashboard", "kind": "base", "block": null, "base_tables": ["google_play__comprehensive_performance_dashboard"]}] | [] | ["package_name"] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |
| B1 | MIN(date_day) | [{"table": "google_play__comprehensive_performance_dashboard", "column": "date_day"}] | [] | False |
| B1 | MAX(date_day) | [{"table": "google_play__comprehensive_performance_dashboard", "column": "date_day"}] | [] | False |
| B1 | SUM(daily_net_revenue) | [{"table": "google_play__comprehensive_performance_dashboard", "column": "daily_net_revenue"}] | [] | False |
| B1 | AVG(daily_net_revenue) | [{"table": "google_play__comprehensive_performance_dashboard", "column": "daily_net_revenue"}] | [] | False |
| B1 | SUM(daily_installs) | [{"table": "google_play__comprehensive_performance_dashboard", "column": "daily_installs"}] | [] | False |
| B1 | SUM(store_acquisitions) | [{"table": "google_play__comprehensive_performance_dashboard", "column": "store_acquisitions"}] | [] | False |
| B1 | SUM(store_visitors) | [{"table": "google_play__comprehensive_performance_dashboard", "column": "store_visitors"}] | [] | False |


## S15

类别 `data`；来源 `query_db`；调用 `5fa39ecbd8c244c084bf832b21b25e39`；状态 `success`。

```sql
SELECT date_day, package_name, daily_net_revenue, daily_installs, store_acquisitions, store_visitors, store_conversion_rate FROM google_play__comprehensive_performance_dashboard WHERE date_day >= '2024-01-01' ORDER BY date_day, package_name LIMIT 30
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-068/attempt-01/sql/S15.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-068/attempt-01/sql/S15.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-068/attempt-01/results/S15.rows.jsonl)；完整：True；SHA256：`b2953bd8aac7ef98c59205e8b8c2f933f4c2d60b73d8bf824bc61179005eba52`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "google_play__comprehensive_performance_dashboard", "kind": "base", "block": null, "base_tables": ["google_play__comprehensive_performance_dashboard"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |


## S16

类别 `data`；来源 `query_db`；调用 `7090e8194ac84222a928fa7d2ec875c3`；状态 `success`。

```sql
SELECT COUNT(*) AS n, SUM(CASE WHEN store_visitors > 0 THEN 1 ELSE 0 END) AS vis_pos, SUM(CASE WHEN store_acquisitions > 0 THEN 1 ELSE 0 END) AS acq_pos, SUM(CASE WHEN store_conversion_rate IS NOT NULL THEN 1 ELSE 0 END) AS conv_notnull, SUM(store_visitors) AS sum_vis, SUM(store_acquisitions) AS sum_acq FROM google_play__comprehensive_performance_dashboard
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-068/attempt-01/sql/S16.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-068/attempt-01/sql/S16.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-068/attempt-01/results/S16.rows.jsonl)；完整：True；SHA256：`c3ea31458978dfab54b2c0dec00bbd30936439779728d4fcc29c9cb79428e8ae`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "google_play__comprehensive_performance_dashboard", "kind": "base", "block": null, "base_tables": ["google_play__comprehensive_performance_dashboard"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |
| B1 | SUM(CASE WHEN store_visitors > 0 THEN 1 ELSE 0 END) | [] | [{"table": "google_play__comprehensive_performance_dashboard", "column": "store_visitors"}] | False |
| B1 | SUM(CASE WHEN store_acquisitions > 0 THEN 1 ELSE 0 END) | [] | [{"table": "google_play__comprehensive_performance_dashboard", "column": "store_acquisitions"}] | False |
| B1 | SUM(CASE WHEN NOT store_conversion_rate IS NULL THEN 1 ELSE 0 END) | [] | [{"table": "google_play__comprehensive_performance_dashboard", "column": "store_conversion_rate"}] | False |
| B1 | SUM(store_visitors) | [{"table": "google_play__comprehensive_performance_dashboard", "column": "store_visitors"}] | [] | False |
| B1 | SUM(store_acquisitions) | [{"table": "google_play__comprehensive_performance_dashboard", "column": "store_acquisitions"}] | [] | False |


## S17

类别 `data`；来源 `query_db`；调用 `fd283f3bf48e4432bc4d11819cc6f9c8`；状态 `success`。

```sql
SELECT package_name, COUNT(*) AS n, SUM(CASE WHEN store_visitors > 0 THEN 1 ELSE 0 END) AS vis_pos, SUM(store_visitors) AS sum_vis, SUM(store_acquisitions) AS sum_acq, SUM(daily_net_revenue) AS sum_rev FROM google_play__comprehensive_performance_dashboard GROUP BY package_name ORDER BY package_name
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-068/attempt-01/sql/S17.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-068/attempt-01/sql/S17.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-068/attempt-01/results/S17.rows.jsonl)；完整：True；SHA256：`6c43a1d43d02288b67951f02d21da632c47a834d30a1493a27308691be56c6d7`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "google_play__comprehensive_performance_dashboard", "kind": "base", "block": null, "base_tables": ["google_play__comprehensive_performance_dashboard"]}] | [] | ["package_name"] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |
| B1 | SUM(CASE WHEN store_visitors > 0 THEN 1 ELSE 0 END) | [] | [{"table": "google_play__comprehensive_performance_dashboard", "column": "store_visitors"}] | False |
| B1 | SUM(store_visitors) | [{"table": "google_play__comprehensive_performance_dashboard", "column": "store_visitors"}] | [] | False |
| B1 | SUM(store_acquisitions) | [{"table": "google_play__comprehensive_performance_dashboard", "column": "store_acquisitions"}] | [] | False |
| B1 | SUM(daily_net_revenue) | [{"table": "google_play__comprehensive_performance_dashboard", "column": "daily_net_revenue"}] | [] | False |


## S18

类别 `data`；来源 `query_db`；调用 `d4197bc26560428d8bf13cc82fd370be`；状态 `success`。

```sql
SELECT package_name, SUM(daily_net_revenue) AS rev2024, SUM(store_visitors) AS vis2024, SUM(store_acquisitions) AS acq2024, SUM(daily_installs) AS inst2024, SUM(daily_net_revenue)/NULLIF(SUM(store_acquisitions),0) AS rev_per_acq, SUM(store_acquisitions)*1.0/NULLIF(SUM(store_visitors),0) AS conv FROM google_play__comprehensive_performance_dashboard WHERE date_day >= '2024-01-01' AND date_day < '2025-01-01' GROUP BY package_name ORDER BY package_name
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-068/attempt-01/sql/S18.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-068/attempt-01/sql/S18.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-068/attempt-01/results/S18.rows.jsonl)；完整：True；SHA256：`8960bafc1feb63800659c9cd53048ed0fd523574fc716d03730dfc570c59e3bc`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "google_play__comprehensive_performance_dashboard", "kind": "base", "block": null, "base_tables": ["google_play__comprehensive_performance_dashboard"]}] | [] | ["package_name"] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | SUM(daily_net_revenue) | [{"table": "google_play__comprehensive_performance_dashboard", "column": "daily_net_revenue"}] | [] | False |
| B1 | SUM(store_visitors) | [{"table": "google_play__comprehensive_performance_dashboard", "column": "store_visitors"}] | [] | False |
| B1 | SUM(store_acquisitions) | [{"table": "google_play__comprehensive_performance_dashboard", "column": "store_acquisitions"}] | [] | False |
| B1 | SUM(daily_installs) | [{"table": "google_play__comprehensive_performance_dashboard", "column": "daily_installs"}] | [] | False |
| B1 | SUM(daily_net_revenue) | [{"table": "google_play__comprehensive_performance_dashboard", "column": "daily_net_revenue"}] | [] | False |
| B1 | SUM(store_acquisitions) | [{"table": "google_play__comprehensive_performance_dashboard", "column": "store_acquisitions"}] | [] | False |
| B1 | SUM(store_acquisitions) | [{"table": "google_play__comprehensive_performance_dashboard", "column": "store_acquisitions"}] | [] | False |
| B1 | SUM(store_visitors) | [{"table": "google_play__comprehensive_performance_dashboard", "column": "store_visitors"}] | [] | False |


## S19

类别 `data`；来源 `query_db`；调用 `44d3352a4bf549a59e246a8caf13a786`；状态 `success`。

```sql
SELECT package_name, AVG(avg_daily_revenue) AS avg_dr, AVG(store_conversion_rate) AS avg_cr, AVG(revenue_last_30_days) AS avg_rev30, SUM(store_visitors_30d) AS vis30, SUM(store_installs_30d) AS inst30 FROM google_play__geo_market_analysis GROUP BY package_name ORDER BY package_name
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-068/attempt-01/sql/S19.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-068/attempt-01/sql/S19.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-068/attempt-01/results/S19.rows.jsonl)；完整：True；SHA256：`da223ce1622ef778fcb660c65aa29427111b310737cac707880a7ac28c9bce15`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "google_play__geo_market_analysis", "kind": "base", "block": null, "base_tables": ["google_play__geo_market_analysis"]}] | [] | ["package_name"] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | AVG(avg_daily_revenue) | [{"table": "google_play__geo_market_analysis", "column": "avg_daily_revenue"}] | [] | False |
| B1 | AVG(store_conversion_rate) | [{"table": "google_play__geo_market_analysis", "column": "store_conversion_rate"}] | [] | False |
| B1 | AVG(revenue_last_30_days) | [{"table": "google_play__geo_market_analysis", "column": "revenue_last_30_days"}] | [] | False |
| B1 | SUM(store_visitors_30d) | [{"table": "google_play__geo_market_analysis", "column": "store_visitors_30d"}] | [] | False |
| B1 | SUM(store_installs_30d) | [{"table": "google_play__geo_market_analysis", "column": "store_installs_30d"}] | [] | False |


## S20

类别 `data`；来源 `query_db`；调用 `faac9228881a4d4db1d530e1c6181f60`；状态 `success`。

```sql
SELECT strftime('%Y-%m', date_day) AS ym, COUNT(*) AS n, SUM(store_visitors) AS vis, SUM(store_acquisitions) AS acq, SUM(daily_net_revenue) AS rev FROM google_play__comprehensive_performance_dashboard GROUP BY ym ORDER BY ym
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-068/attempt-01/sql/S20.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-068/attempt-01/sql/S20.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-068/attempt-01/results/S20.rows.jsonl)；完整：True；SHA256：`f87bd8c7b61d59620ac78b95768187a101f295f86239f1cc1731567eff71c6ef`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "google_play__comprehensive_performance_dashboard", "kind": "base", "block": null, "base_tables": ["google_play__comprehensive_performance_dashboard"]}] | [] | ["STRFTIME('%Y-%m', date_day)"] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |
| B1 | SUM(store_visitors) | [{"table": "google_play__comprehensive_performance_dashboard", "column": "store_visitors"}] | [] | False |
| B1 | SUM(store_acquisitions) | [{"table": "google_play__comprehensive_performance_dashboard", "column": "store_acquisitions"}] | [] | False |
| B1 | SUM(daily_net_revenue) | [{"table": "google_play__comprehensive_performance_dashboard", "column": "daily_net_revenue"}] | [] | False |


## S21

类别 `data`；来源 `query_db`；调用 `522f8269bc064381841d34ae2d62cef6`；状态 `success`。

```sql
SELECT package_name, quality_score, average_rating, business_health_status, overall_performance_score, growth_trend, primary_risk_flag, recommended_action, avg_transaction_value, average_revenue_per_user FROM google_play__comprehensive_performance_dashboard WHERE date_day = (SELECT MAX(date_day) FROM google_play__comprehensive_performance_dashboard d2 WHERE d2.package_name = google_play__comprehensive_performance_dashboard.package_name) ORDER BY package_name
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-068/attempt-01/sql/S21.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-068/attempt-01/sql/S21.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-068/attempt-01/results/S21.rows.jsonl)；完整：True；SHA256：`eb3b07bd6d102a4d777a24b83542cfddba2a5a5210e42f7fbea524add252bd0c`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "d2", "kind": "base", "block": null, "base_tables": ["google_play__comprehensive_performance_dashboard"]}] | [] | [] |
| B2 | [{"alias": "google_play__comprehensive_performance_dashboard", "kind": "base", "block": null, "base_tables": ["google_play__comprehensive_performance_dashboard"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | MAX(date_day) | [{"table": "google_play__comprehensive_performance_dashboard", "column": "date_day"}] | [] | False |


## S22

类别 `data`；来源 `query_db`；调用 `bf371ce9dc614bfe888ef53f9070d4e2`；状态 `success`。

```sql
SELECT package_name, SUM(revenue_opportunity_score) AS total_ros, AVG(revenue_opportunity_score) AS avg_ros, SUM(growth_potential_score) AS total_gps, AVG(growth_potential_score) AS avg_gps, SUM(user_quality_score) AS total_uqs, AVG(user_quality_score) AS avg_uqs, SUM(store_performance_score) AS total_sps, AVG(store_performance_score) AS avg_sps, SUM(overall_market_score) AS total_oms, AVG(overall_market_score) AS avg_oms FROM google_play__geo_market_analysis GROUP BY package_name ORDER BY package_name
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-068/attempt-01/sql/S22.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-068/attempt-01/sql/S22.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-068/attempt-01/results/S22.rows.jsonl)；完整：True；SHA256：`c1dabe868f072971fe2b12b188c8fdf298bc23db4884fd765b734e5ff0d9f7d4`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "google_play__geo_market_analysis", "kind": "base", "block": null, "base_tables": ["google_play__geo_market_analysis"]}] | [] | ["package_name"] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | SUM(revenue_opportunity_score) | [{"table": "google_play__geo_market_analysis", "column": "revenue_opportunity_score"}] | [] | False |
| B1 | AVG(revenue_opportunity_score) | [{"table": "google_play__geo_market_analysis", "column": "revenue_opportunity_score"}] | [] | False |
| B1 | SUM(growth_potential_score) | [{"table": "google_play__geo_market_analysis", "column": "growth_potential_score"}] | [] | False |
| B1 | AVG(growth_potential_score) | [{"table": "google_play__geo_market_analysis", "column": "growth_potential_score"}] | [] | False |
| B1 | SUM(user_quality_score) | [{"table": "google_play__geo_market_analysis", "column": "user_quality_score"}] | [] | False |
| B1 | AVG(user_quality_score) | [{"table": "google_play__geo_market_analysis", "column": "user_quality_score"}] | [] | False |
| B1 | SUM(store_performance_score) | [{"table": "google_play__geo_market_analysis", "column": "store_performance_score"}] | [] | False |
| B1 | AVG(store_performance_score) | [{"table": "google_play__geo_market_analysis", "column": "store_performance_score"}] | [] | False |
| B1 | SUM(overall_market_score) | [{"table": "google_play__geo_market_analysis", "column": "overall_market_score"}] | [] | False |
| B1 | AVG(overall_market_score) | [{"table": "google_play__geo_market_analysis", "column": "overall_market_score"}] | [] | False |


## S23

类别 `data`；来源 `query_db`；调用 `316b734afd2f4fd2b2258c39eceeda5d`；状态 `success`。

```sql
SELECT * FROM google_play__product_portfolio_analysis ORDER BY package_name
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-068/attempt-01/sql/S23.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-068/attempt-01/sql/S23.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-068/attempt-01/results/S23.rows.jsonl)；完整：True；SHA256：`d73c8019e11e05aa86dc1f3260bfa0ab4dfa9f35f7a2a84140f2cd86339d08c9`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "google_play__product_portfolio_analysis", "kind": "base", "block": null, "base_tables": ["google_play__product_portfolio_analysis"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |


## S24

类别 `data`；来源 `python`；调用 `4c393631c7164ff3b5972d9134ea3ebe`；状态 `success`。

```sql
SELECT * FROM google_play__geo_market_analysis ORDER BY package_name, country
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-068/attempt-01/sql/S24.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-068/attempt-01/sql/S24.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-068/attempt-01/results/S24.rows.jsonl)；完整：True；SHA256：`04036eb6e0435a4947fae341e76c9e86bb18b1abe3044d157aa8bb76c727f04a`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "google_play__geo_market_analysis", "kind": "base", "block": null, "base_tables": ["google_play__geo_market_analysis"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |


## S25

类别 `data`；来源 `python`；调用 `4c393631c7164ff3b5972d9134ea3ebe`；状态 `success`。

```sql
SELECT * FROM google_play__product_portfolio_analysis ORDER BY package_name
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-068/attempt-01/sql/S25.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-068/attempt-01/sql/S25.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-068/attempt-01/results/S25.rows.jsonl)；完整：True；SHA256：`d73c8019e11e05aa86dc1f3260bfa0ab4dfa9f35f7a2a84140f2cd86339d08c9`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "google_play__product_portfolio_analysis", "kind": "base", "block": null, "base_tables": ["google_play__product_portfolio_analysis"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |


## S26

类别 `data`；来源 `python`；调用 `4c393631c7164ff3b5972d9134ea3ebe`；状态 `success`。

```sql

SELECT package_name,
       SUM(daily_net_revenue) AS rev2024,
       SUM(store_visitors) AS vis2024,
       SUM(store_acquisitions) AS acq2024,
       SUM(daily_net_revenue)/NULLIF(SUM(store_acquisitions),0) AS rev_per_acq,
       SUM(store_acquisitions)*1.0/NULLIF(SUM(store_visitors),0) AS conv_rate
FROM google_play__comprehensive_performance_dashboard
WHERE date_day >= '2024-01-01' AND date_day < '2025-01-01'
GROUP BY package_name
ORDER BY package_name

```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-068/attempt-01/sql/S26.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-068/attempt-01/sql/S26.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-068/attempt-01/results/S26.rows.jsonl)；完整：True；SHA256：`17949d9a16306e9b861aceaf549a7a1b8de6085035377b487997300f5cca305a`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "google_play__comprehensive_performance_dashboard", "kind": "base", "block": null, "base_tables": ["google_play__comprehensive_performance_dashboard"]}] | [] | ["package_name"] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | SUM(daily_net_revenue) | [{"table": "google_play__comprehensive_performance_dashboard", "column": "daily_net_revenue"}] | [] | False |
| B1 | SUM(store_visitors) | [{"table": "google_play__comprehensive_performance_dashboard", "column": "store_visitors"}] | [] | False |
| B1 | SUM(store_acquisitions) | [{"table": "google_play__comprehensive_performance_dashboard", "column": "store_acquisitions"}] | [] | False |
| B1 | SUM(daily_net_revenue) | [{"table": "google_play__comprehensive_performance_dashboard", "column": "daily_net_revenue"}] | [] | False |
| B1 | SUM(store_acquisitions) | [{"table": "google_play__comprehensive_performance_dashboard", "column": "store_acquisitions"}] | [] | False |
| B1 | SUM(store_acquisitions) | [{"table": "google_play__comprehensive_performance_dashboard", "column": "store_acquisitions"}] | [] | False |
| B1 | SUM(store_visitors) | [{"table": "google_play__comprehensive_performance_dashboard", "column": "store_visitors"}] | [] | False |


## S27

类别 `data`；来源 `python`；调用 `62105f26baa645efb441c61b45e7506c`；状态 `success`。

```sql
SELECT * FROM google_play__geo_market_analysis
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-068/attempt-01/sql/S27.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-068/attempt-01/sql/S27.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-068/attempt-01/results/S27.rows.jsonl)；完整：True；SHA256：`f87a7b588e49eff798c9e0bf018a5d3ce2e3bc2fc9b886bf4729d6ed877f0054`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "google_play__geo_market_analysis", "kind": "base", "block": null, "base_tables": ["google_play__geo_market_analysis"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |


## S28

类别 `data`；来源 `python`；调用 `62105f26baa645efb441c61b45e7506c`；状态 `success`。

```sql
SELECT * FROM google_play__product_portfolio_analysis
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-068/attempt-01/sql/S28.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-068/attempt-01/sql/S28.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-068/attempt-01/results/S28.rows.jsonl)；完整：True；SHA256：`6d7af4697153e060ec00af89e78ee335fc36303c016a75472123ace7842ab25d`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "google_play__product_portfolio_analysis", "kind": "base", "block": null, "base_tables": ["google_play__product_portfolio_analysis"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |


## S29

类别 `data`；来源 `python`；调用 `62105f26baa645efb441c61b45e7506c`；状态 `success`。

```sql

SELECT package_name,
       SUM(daily_net_revenue) AS rev2024,
       SUM(store_visitors) AS vis2024,
       SUM(store_acquisitions) AS acq2024
FROM google_play__comprehensive_performance_dashboard
WHERE date_day >= '2024-01-01' AND date_day < '2025-01-01'
GROUP BY package_name

```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-068/attempt-01/sql/S29.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-068/attempt-01/sql/S29.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-068/attempt-01/results/S29.rows.jsonl)；完整：True；SHA256：`33421e97ea584cd0cb1e707742c97998ef91ae3c5a44dfcec48a1f5dea811602`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "google_play__comprehensive_performance_dashboard", "kind": "base", "block": null, "base_tables": ["google_play__comprehensive_performance_dashboard"]}] | [] | ["package_name"] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | SUM(daily_net_revenue) | [{"table": "google_play__comprehensive_performance_dashboard", "column": "daily_net_revenue"}] | [] | False |
| B1 | SUM(store_visitors) | [{"table": "google_play__comprehensive_performance_dashboard", "column": "store_visitors"}] | [] | False |
| B1 | SUM(store_acquisitions) | [{"table": "google_play__comprehensive_performance_dashboard", "column": "store_acquisitions"}] | [] | False |


## S30

类别 `data`；来源 `python`；调用 `661496c3fac84403bf882c21cc1df650`；状态 `success`。

```sql
SELECT * FROM google_play__geo_market_analysis
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-068/attempt-01/sql/S30.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-068/attempt-01/sql/S30.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-068/attempt-01/results/S30.rows.jsonl)；完整：True；SHA256：`f87a7b588e49eff798c9e0bf018a5d3ce2e3bc2fc9b886bf4729d6ed877f0054`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "google_play__geo_market_analysis", "kind": "base", "block": null, "base_tables": ["google_play__geo_market_analysis"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |


## S31

类别 `data`；来源 `python`；调用 `661496c3fac84403bf882c21cc1df650`；状态 `success`。

```sql
SELECT * FROM google_play__product_portfolio_analysis
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-068/attempt-01/sql/S31.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-068/attempt-01/sql/S31.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-068/attempt-01/results/S31.rows.jsonl)；完整：True；SHA256：`6d7af4697153e060ec00af89e78ee335fc36303c016a75472123ace7842ab25d`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "google_play__product_portfolio_analysis", "kind": "base", "block": null, "base_tables": ["google_play__product_portfolio_analysis"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |


## S32

类别 `data`；来源 `python`；调用 `97a794e000c748beaec6d049b589f2cb`；状态 `success`。

```sql
SELECT * FROM google_play__geo_market_analysis
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-068/attempt-01/sql/S32.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-068/attempt-01/sql/S32.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-068/attempt-01/results/S32.rows.jsonl)；完整：True；SHA256：`f87a7b588e49eff798c9e0bf018a5d3ce2e3bc2fc9b886bf4729d6ed877f0054`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "google_play__geo_market_analysis", "kind": "base", "block": null, "base_tables": ["google_play__geo_market_analysis"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |


## S33

类别 `data`；来源 `python`；调用 `97a794e000c748beaec6d049b589f2cb`；状态 `success`。

```sql
SELECT * FROM google_play__product_portfolio_analysis
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-068/attempt-01/sql/S33.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-068/attempt-01/sql/S33.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-068/attempt-01/results/S33.rows.jsonl)；完整：True；SHA256：`6d7af4697153e060ec00af89e78ee335fc36303c016a75472123ace7842ab25d`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "google_play__product_portfolio_analysis", "kind": "base", "block": null, "base_tables": ["google_play__product_portfolio_analysis"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |


## S34

类别 `data`；来源 `python`；调用 `096f0f4665944b7295b2504ea124c813`；状态 `success`。

```sql
SELECT * FROM google_play__geo_market_analysis
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-068/attempt-01/sql/S34.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-068/attempt-01/sql/S34.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-068/attempt-01/results/S34.rows.jsonl)；完整：True；SHA256：`f87a7b588e49eff798c9e0bf018a5d3ce2e3bc2fc9b886bf4729d6ed877f0054`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "google_play__geo_market_analysis", "kind": "base", "block": null, "base_tables": ["google_play__geo_market_analysis"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |


## S35

类别 `data`；来源 `python`；调用 `096f0f4665944b7295b2504ea124c813`；状态 `success`。

```sql
SELECT * FROM google_play__product_portfolio_analysis
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-068/attempt-01/sql/S35.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-068/attempt-01/sql/S35.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-068/attempt-01/results/S35.rows.jsonl)；完整：True；SHA256：`6d7af4697153e060ec00af89e78ee335fc36303c016a75472123ace7842ab25d`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "google_play__product_portfolio_analysis", "kind": "base", "block": null, "base_tables": ["google_play__product_portfolio_analysis"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |


## S36

类别 `data`；来源 `query_db`；调用 `b8a87d90b37e42bcb5b0345b08576f50`；状态 `success`。

```sql
-- Full market segment analysis
SELECT 
  g.package_name,
  g.country,
  g.country_name,
  g.region,
  g.sub_region,
  g.avg_daily_revenue,
  g.store_conversion_rate,
  g.revenue_last_30_days,
  g.store_visitors_30d,
  g.store_installs_30d,
  g.avg_transaction_value,
  g.average_revenue_per_user,
  g.market_tier,
  g.opportunity_type,
  g.investment_recommendation,
  g.revenue_opportunity_score,
  g.growth_potential_score,
  g.overall_market_score,
  CASE 
    WHEN g.store_conversion_rate > 15 AND g.avg_daily_revenue < 5 THEN 'Segment A: High Conv, Low Rev'
    WHEN g.avg_daily_revenue > 7 AND g.store_conversion_rate < 10 THEN 'Segment B: High Rev, Low Conv'
    ELSE 'Other'
  END AS market_segment
FROM google_play__geo_market_analysis g
ORDER BY market_segment, g.package_name, g.country
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-068/attempt-01/sql/S36.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-068/attempt-01/sql/S36.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-068/attempt-01/results/S36.rows.jsonl)；完整：True；SHA256：`a5eafaab44e12b2afa64e04859f537f0c5495eb0f9d0e3f1b819e4b7c3fe34da`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "g", "kind": "base", "block": null, "base_tables": ["google_play__geo_market_analysis"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |


## S37

类别 `data`；来源 `query_db`；调用 `d09c75624acd4feeb5e5758bb6d9d2f6`；状态 `success`。

```sql
SELECT package_name, country, avg_daily_revenue, store_conversion_rate,
  CASE 
    WHEN store_conversion_rate > 15 AND avg_daily_revenue < 5 THEN 'Segment A'
    WHEN avg_daily_revenue > 7 AND store_conversion_rate < 10 THEN 'Segment B'
    ELSE 'Other'
  END AS market_segment
FROM google_play__geo_market_analysis
WHERE package_name = 'com.studio.videostreaming'
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-068/attempt-01/sql/S37.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-068/attempt-01/sql/S37.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-068/attempt-01/results/S37.rows.jsonl)；完整：True；SHA256：`6c8b330e87df88e0ae7428e86910bff796ceca818b889fd44abd8ee0fa73c355`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "google_play__geo_market_analysis", "kind": "base", "block": null, "base_tables": ["google_play__geo_market_analysis"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |


## S38

类别 `data`；来源 `query_db`；调用 `4118703a74354f56a545de6a9c0599bb`；状态 `success`。

```sql
SELECT package_name, country, avg_daily_revenue, store_conversion_rate FROM google_play__geo_market_analysis WHERE package_name = 'com.studio.videostreaming'
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-068/attempt-01/sql/S38.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-068/attempt-01/sql/S38.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-068/attempt-01/results/S38.rows.jsonl)；完整：True；SHA256：`cf6cac5cd5d0be0e5f2ea1402b63c2ba797de5f3b3b4354b5e92588d8e328f3b`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "google_play__geo_market_analysis", "kind": "base", "block": null, "base_tables": ["google_play__geo_market_analysis"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |


## S39

类别 `data`；来源 `query_db`；调用 `85c31386e3fb41cfbe7cd1942d64136d`；状态 `failed`。

```sql
-- Segment-level summary
WITH seg AS (
  SELECT package_name, country,
    CASE 
      WHEN store_conversion_rate > 15 AND avg_daily_revenue < 5 THEN 'A_HighConv_LowRev'
      WHEN avg_daily_revenue > 7 AND store_conversion_rate < 10 THEN 'B_HighRev_LowConv'
      ELSE 'Other'
    END AS seg
  FROM google_play__geo_market_analysis
)
SELECT seg,
  COUNT(*) AS n_markets,
  COUNT(DISTINCT package_name) AS n_apps,
  SUM(g.store_visitors_30d) AS total_visitors,
  SUM(g.store_installs_30d) AS total_installs,
  SUM(g.revenue_last_30_days) AS total_rev_30d,
  ROUND(AVG(g.store_conversion_rate), 2) AS avg_conv,
  ROUND(AVG(g.avg_daily_revenue), 2) AS avg_daily_rev
FROM seg s JOIN google_play__geo_market_analysis g ON s.package_name = g.package_name AND s.country = g.country
GROUP BY seg
ORDER BY seg
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-068/attempt-01/sql/S39.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-068/attempt-01/sql/S39.parameters.json)。

错误：`OperationalError('ambiguous column name: package_name')`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "google_play__geo_market_analysis", "kind": "base", "block": null, "base_tables": ["google_play__geo_market_analysis"]}] | [] | [] |
| B2 | [{"alias": "s", "kind": "derived", "block": "B1", "base_tables": ["google_play__geo_market_analysis"]}, {"alias": "g", "kind": "base", "block": null, "base_tables": ["google_play__geo_market_analysis"]}] | [{"type": "INNER", "right": "google_play__geo_market_analysis AS g", "on": "s.package_name = g.package_name AND s.country = g.country", "using": []}] | ["seg"] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B2 | COUNT(*) | [] | [] | True |
| B2 | COUNT(DISTINCT package_name) | [{"unknown": "package_name"}] | [] | False |
| B2 | SUM(g.store_visitors_30d) | [{"table": "google_play__geo_market_analysis", "column": "store_visitors_30d"}] | [] | False |
| B2 | SUM(g.store_installs_30d) | [{"table": "google_play__geo_market_analysis", "column": "store_installs_30d"}] | [] | False |
| B2 | SUM(g.revenue_last_30_days) | [{"table": "google_play__geo_market_analysis", "column": "revenue_last_30_days"}] | [] | False |
| B2 | AVG(g.store_conversion_rate) | [{"table": "google_play__geo_market_analysis", "column": "store_conversion_rate"}] | [] | False |
| B2 | AVG(g.avg_daily_revenue) | [{"table": "google_play__geo_market_analysis", "column": "avg_daily_revenue"}] | [] | False |


未解析列血缘：[{"block": "B2", "column": "package_name", "reason": "ambiguous_or_missing_source"}, {"block": "B2", "column": "package_name", "reason": "ambiguous_or_missing_source"}]

## S40

类别 `data`；来源 `query_db`；调用 `80663084886c483fbf2eb15a2274029d`；状态 `success`。

```sql
SELECT package_name, total_revenue_30d, avg_daily_revenue, total_installs_30d, avg_active_devices, total_markets, revenue_score, engagement_score, portfolio_health_score, bcg_matrix_category, investment_priority, growth_stage, high_engagement_markets, strong_retention_markets FROM google_play__product_portfolio_analysis ORDER BY package_name
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-068/attempt-01/sql/S40.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-068/attempt-01/sql/S40.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-068/attempt-01/results/S40.rows.jsonl)；完整：True；SHA256：`06e25f610f72ba0b701ecb6163065e7eb6d27dd3093ced54ec3a20f132064daa`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "google_play__product_portfolio_analysis", "kind": "base", "block": null, "base_tables": ["google_play__product_portfolio_analysis"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |


## S41

类别 `data`；来源 `query_db`；调用 `b1cd1722806d4c52bce7e80ac4d61d62`；状态 `success`。

```sql
WITH seg AS (
  SELECT package_name AS pkg, country AS ctry,
    CASE 
      WHEN store_conversion_rate > 15 AND avg_daily_revenue < 5 THEN 'A_HighConv_LowRev'
      WHEN avg_daily_revenue > 7 AND store_conversion_rate < 10 THEN 'B_HighRev_LowConv'
      ELSE 'Other'
    END AS seg
  FROM google_play__geo_market_analysis
)
SELECT s.seg,
  COUNT(*) AS n_markets,
  COUNT(DISTINCT g.package_name) AS n_apps,
  SUM(g.store_visitors_30d) AS total_visitors,
  SUM(g.store_installs_30d) AS total_installs,
  SUM(g.revenue_last_30_days) AS total_rev_30d,
  ROUND(AVG(g.store_conversion_rate), 2) AS avg_conv,
  ROUND(AVG(g.avg_daily_revenue), 2) AS avg_daily_rev
FROM seg s JOIN google_play__geo_market_analysis g ON s.pkg = g.package_name AND s.ctry = g.country
GROUP BY s.seg
ORDER BY s.seg
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-068/attempt-01/sql/S41.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-068/attempt-01/sql/S41.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-068/attempt-01/results/S41.rows.jsonl)；完整：True；SHA256：`28f230b0057b22f36993ef6671650fa78dcbf580888974f1fdf8334214a62187`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "google_play__geo_market_analysis", "kind": "base", "block": null, "base_tables": ["google_play__geo_market_analysis"]}] | [] | [] |
| B2 | [{"alias": "s", "kind": "derived", "block": "B1", "base_tables": ["google_play__geo_market_analysis"]}, {"alias": "g", "kind": "base", "block": null, "base_tables": ["google_play__geo_market_analysis"]}] | [{"type": "INNER", "right": "google_play__geo_market_analysis AS g", "on": "s.pkg = g.package_name AND s.ctry = g.country", "using": []}] | ["s.seg"] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B2 | COUNT(*) | [] | [] | True |
| B2 | COUNT(DISTINCT g.package_name) | [{"table": "google_play__geo_market_analysis", "column": "package_name"}] | [] | False |
| B2 | SUM(g.store_visitors_30d) | [{"table": "google_play__geo_market_analysis", "column": "store_visitors_30d"}] | [] | False |
| B2 | SUM(g.store_installs_30d) | [{"table": "google_play__geo_market_analysis", "column": "store_installs_30d"}] | [] | False |
| B2 | SUM(g.revenue_last_30_days) | [{"table": "google_play__geo_market_analysis", "column": "revenue_last_30_days"}] | [] | False |
| B2 | AVG(g.store_conversion_rate) | [{"table": "google_play__geo_market_analysis", "column": "store_conversion_rate"}] | [] | False |
| B2 | AVG(g.avg_daily_revenue) | [{"table": "google_play__geo_market_analysis", "column": "avg_daily_revenue"}] | [] | False |

