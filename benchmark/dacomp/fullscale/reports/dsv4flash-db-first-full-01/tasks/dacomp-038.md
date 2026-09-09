# dacomp-038

Starting from July 5, we gray-released a new version of strategies such as Search Strategy…

运行：已提交。官方未评分。全部 SQL 尝试/成功 37/37；数据 SQL 35/35；Python 7 次。

完整原题：

Starting from July 5, we gray-released a new version of strategies such as Search Strategy and Guess You Like strategy. Analyze the performance of the new strategy version and determine which can proceed to full rollout.

| 表 | 行数 | 列数 |
| --- | --- | --- |
| sheet1 | 511 | 16 |
| sheet2 | 511 | 8 |


实际路线（分析者依据 SQL/源码概括，不代表 Agent 自述）：分别查询两张策略报表 → Python 按日期和推广类别合并 → 按策略家族/版本/前后期计算流量与订单指标 → 比较新旧变化并做检验、绘图。

数据库大小：270,336 字节。

## 数据 SQL

| SQL | 状态 | 基础表 | Join 输入/类型 | GROUP BY | 聚合表达式 | 结果行数 | 数据库 ms |
| --- | --- | --- | --- | --- | --- | --- | --- |
| [S3/Q1](#s3) | success | ["sheet1"] | 0 / {} | [] | [] | 10 | 0.572 |
| [S4/Q2](#s4) | success | ["sheet2"] | 0 / {} | [] | [] | 10 | 0.359 |
| [S5/Q3](#s5) | success | ["sheet1"] | 0 / {} | [] | [] | 8 | 0.567 |
| [S6/Q4](#s6) | success | ["sheet1"] | 0 / {} | [] | [] | 7 | 0.51 |
| [S7/Q5](#s7) | success | ["sheet2"] | 0 / {} | [] | [] | 7 | 0.511 |
| [S8/Q6](#s8) | success | ["sheet1"] | 0 / {} | ["\"Promotion Date\"", "Strategy"] | ["COUNT(*)"] | 44 | 0.677 |
| [S9/Q7](#s9) | success | ["sheet2"] | 0 / {} | ["\"Promotion Date\""] | ["COUNT(*)", "COUNT(DISTINCT \"Promotion Tertiary Category\")"] | 7 | 0.703 |
| [S10/Q8](#s10) | success | ["sheet1"] | 0 / {} | ["\"Promotion Date\"", "Strategy"] | ["COUNT(*)"] | 44 | 0.682 |
| [S11/Q9](#s11) | success | ["sheet1"] | 0 / {} | ["\"Promotion Date\"", "Strategy"] | ["COUNT(*)"] | 20 | 0.711 |
| [S12/Q10](#s12) | success | ["sheet1"] | 0 / {} | ["\"Promotion Date\"", "Strategy"] | ["COUNT(*)"] | 14 | 0.686 |
| [S13/Q11](#s13) | success | ["sheet1"] | 0 / {} | ["\"Promotion Date\"", "Strategy"] | ["COUNT(*)"] | 4 | 0.77 |
| [S14/Q12](#s14) | success | ["sheet1"] | 0 / {} | ["\"Promotion Date\"", "Strategy"] | ["COUNT(*)"] | 11 | 0.487 |
| [S15/Q13](#s15) | success | ["sheet1"] | 0 / {} | ["s.\"Promotion Date\"", "s.\"Promotion Tertiary Category\""] | ["MAX(CASE WHEN s.Strategy = 'Search Strategy v3.6' THEN 1 ELSE 0 END)", "MAX(CASE WHEN s.Strategy = 'Search Strategy v3.7' THEN 1 ELSE 0 END)"] | 124 | 0.768 |
| [S16/Q14](#s16) | success | ["sheet1"] | 0 / {} | ["s.\"Promotion Date\""] | ["COUNT(DISTINCT \"Promotion Tertiary Category\")", "COUNT(DISTINCT s.\"Promotion Tertiary Category\")"] | 3 | 0.65 |
| [S17/Q15](#s17) | success | ["sheet1"] | 0 / {} | ["CASE WHEN \"Promotion Date\" <= '2025-07-03' THEN 'pre' ELSE 'gray' END", "Strategy"] | ["COUNT(*)", "SUM(Impressions)", "SUM(Clicks)", "SUM(\"Spend (Yuan)\")", "AVG(\"Budget Utilization Rate\")", "SUM(Impressions)", "SUM(Clicks)", "SUM(Impressions)", "SUM(Clicks)", "SUM(\"Spend (Yuan)\")", "SUM(\"Spend (Yuan)\")"] | 12 | 0.962 |
| [S18/Q16](#s18) | success | ["sheet1"] | 0 / {} | ["s.\"Promotion Tertiary Category\""] | ["MAX(CASE WHEN s.\"Promotion Date\" <= '2025-07-03' THEN 1 ELSE 0 END)", "MAX(CASE WHEN s.\"Promotion Date\" >= '2025-07-04' AND s.Strategy = 'Search Strategy v3.6' THEN 1 ELSE 0 END)", "MAX(CASE WHEN s.\"Promotion Date\" >= '2025-07-04' AND s.Strategy = 'Search Strategy v3.7' THEN 1 ELSE 0 END)"] | 31 | 0.678 |
| [S19/Q17](#s19) | success | ["sheet1"] | 0 / {} | ["s.\"Promotion Tertiary Category\""] | ["MAX(CASE WHEN s.\"Promotion Date\" <= '2025-07-03' THEN 1 ELSE 0 END)", "MAX(CASE WHEN s.\"Promotion Date\" >= '2025-07-04' AND s.Strategy = 'Caixi Strategy v4.8' THEN 1 ELSE 0 END)", "MAX(CASE WHEN s.\"Promotion Date\" >= '2025-07-04' AND s.Strategy = 'Caixi Strategy v4.9' THEN 1 ELSE 0 END)"] | 23 | 0.651 |
| [S20/Q18](#s20) | success | ["sheet1"] | 0 / {} | ["s.\"Promotion Tertiary Category\""] | ["MAX(CASE WHEN s.\"Promotion Date\" <= '2025-07-03' THEN 1 ELSE 0 END)", "MAX(CASE WHEN s.\"Promotion Date\" >= '2025-07-04' AND s.Strategy = 'Popup Strategy v2.9' THEN 1 ELSE 0 END)", "MAX(CASE WHEN s.\"Promotion Date\" >= '2025-07-04' AND s.Strategy = 'Popup Strategy v2.9.1' THEN 1 ELSE 0 END)"] | 10 | 0.571 |
| [S21/Q19](#s21) | success | ["sheet1"] | 0 / {} | ["s.\"Promotion Tertiary Category\""] | ["MAX(CASE WHEN s.\"Promotion Date\" <= '2025-07-03' THEN 1 ELSE 0 END)", "MAX(CASE WHEN s.\"Promotion Date\" >= '2025-07-04' AND s.Strategy = 'Renqun Dongcha Strategy v3.2' THEN 1 ELSE 0 END)", "MAX(CASE WHEN s.\"Promotion Date\" >= '2025-07-04' AND s.Strategy = 'Renqun Dongcha Strategy v3.2.1' THEN 1 ELSE 0 END)"] | 9 | 0.55 |
| [S22/Q20](#s22) | success | ["sheet1"] | 0 / {} | [] | ["COUNT(*)"] | 1 | 0.321 |
| [S23/Q21](#s23) | success | ["sheet2"] | 0 / {} | [] | ["COUNT(*)"] | 1 | 0.321 |
| [S24/Q22](#s24) | success | ["sheet1"] | 0 / {} | ["\"Day of the Week\""] | ["COUNT(*)"] | 7 | 0.496 |
| [S25/Q23](#s25) | success | ["sheet1"] | 0 / {} | [] | [] | 511 | 2.933 |
| [S26/Q24](#s26) | success | ["sheet2"] | 0 / {} | [] | [] | 511 | 1.565 |
| [S27/Q25](#s27) | success | ["sheet1"] | 0 / {} | [] | [] | 511 | 2.524 |
| [S28/Q26](#s28) | success | ["sheet2"] | 0 / {} | [] | [] | 511 | 1.397 |
| [S29/Q27](#s29) | success | ["sheet1"] | 0 / {} | ["\"Promotion Date\"", "Strategy"] | ["COUNT(*)", "SUM(\"Spend (Yuan)\")"] | 11 | 0.605 |
| [S30/Q28](#s30) | success | ["sheet1"] | 0 / {} | ["\"Promotion Date\""] | ["COUNT(*)", "COUNT(DISTINCT \"Promotion Tertiary Category\")"] | 7 | 0.694 |
| [S31/Q29](#s31) | success | ["sheet1"] | 0 / {} | [] | [] | 511 | 2.317 |
| [S32/Q30](#s32) | success | ["sheet2"] | 0 / {} | [] | [] | 511 | 1.508 |
| [S33/Q31](#s33) | success | ["sheet1"] | 0 / {} | [] | [] | 511 | 2.133 |
| [S34/Q32](#s34) | success | ["sheet2"] | 0 / {} | [] | [] | 511 | 1.232 |
| [S35/Q33](#s35) | success | ["sheet1"] | 0 / {} | [] | [] | 511 | 2.079 |
| [S36/Q34](#s36) | success | ["sheet1"] | 0 / {} | [] | [] | 511 | 2.093 |
| [S37/Q35](#s37) | success | ["sheet2"] | 0 / {} | [] | [] | 511 | 1.189 |


## 元数据和设置

| SQL | 类别 | 状态 | 内容 |
| --- | --- | --- | --- |
| S1 | connection_setup | success | PRAGMA query_only=ON |
| S2 | metadata | success | SELECT name,sql FROM sqlite_master WHERE type='table' ORDER BY name |


## Python 与执行位置

人工源码审查：**database_first_violation**。Python 连续合并两个来源结果，按策略版本和前后期汇总曝光、点击、花费、订单和交易额，并计算 CTR/CPC/CPM 与变化量。这些可在 SQLite 中合理完成。Mann-Whitney、t 检验和绘图本身是允许的补充；没有 SQL Join 不意味着实际分析没有连接，因为连接发生在 Python。 [证据](../reviews/dacomp-038.json)。

P1：Need to join sheet1 and sheet2 on date+category, compute per-strategy-family controlled comparisons (old vs new across pre and gray periods), and perform statistical tests which are not suitable for SQL. Also need to generate visualizations.

[源码](../../../runs/dsv4flash-db-first-full-01/dacomp-038/attempt-01/python/P1.py)；[输出](../../../runs/dsv4flash-db-first-full-01/dacomp-038/attempt-01/python/P1.stdout)；[错误](../../../runs/dsv4flash-db-first-full-01/dacomp-038/attempt-01/python/P1.stderr)。检出需人工核验的 SQL 可实现操作：groupby(, .merge(, .query(；不能仅凭理由判为合规。

P2：Join sheet1+sheet2, compute per-category paired pre/gray metrics for categories moved to new version vs control categories staying on old version, and run non-parametric tests in Python.

[源码](../../../runs/dsv4flash-db-first-full-01/dacomp-038/attempt-01/python/P2.py)；[输出](../../../runs/dsv4flash-db-first-full-01/dacomp-038/attempt-01/python/P2.stdout)；[错误](../../../runs/dsv4flash-db-first-full-01/dacomp-038/attempt-01/python/P2.stderr)。检出需人工核验的 SQL 可实现操作：.merge(, .query(；不能仅凭理由判为合规。

P3：Inspect daily market-wide trends (all categories from sheet2 and aggregate sheet1) to understand background seasonality/day-of-week effects that may confound the strategy comparison.

[源码](../../../runs/dsv4flash-db-first-full-01/dacomp-038/attempt-01/python/P3.py)；[输出](../../../runs/dsv4flash-db-first-full-01/dacomp-038/attempt-01/python/P3.stdout)；[错误](../../../runs/dsv4flash-db-first-full-01/dacomp-038/attempt-01/python/P3.stderr)。检出需人工核验的 SQL 可实现操作：groupby(, .query(；不能仅凭理由判为合规。

P4：Recompute aggregate metrics with correct period boundaries (Jul 1-3 pre vs Jul 4-7 gray), do direct old-vs-new comparison within the gray period, and check confounders (target audience, delivery status, daily trends).

[源码](../../../runs/dsv4flash-db-first-full-01/dacomp-038/attempt-01/python/P4.py)；[输出](../../../runs/dsv4flash-db-first-full-01/dacomp-038/attempt-01/python/P4.stdout)；[错误](../../../runs/dsv4flash-db-first-full-01/dacomp-038/attempt-01/python/P4.stderr)。检出需人工核验的 SQL 可实现操作：groupby(, .merge(, .query(；不能仅凭理由判为合规。

P5：Recompute category-level weighted metrics (clicks/impressions sum) for the controlled comparison, ensuring proper per-category deltas are tested, and generate visualizations.

[源码](../../../runs/dsv4flash-db-first-full-01/dacomp-038/attempt-01/python/P5.py)；[输出](../../../runs/dsv4flash-db-first-full-01/dacomp-038/attempt-01/python/P5.stdout)；[错误](../../../runs/dsv4flash-db-first-full-01/dacomp-038/attempt-01/python/P5.stderr)。检出需人工核验的 SQL 可实现操作：groupby(, .merge(, .query(；不能仅凭理由判为合规。

P6：Verify the discrepancy between the two computations for Caixi new-category CTR by directly computing clicks/impressions for Caixi v4.9 categories.

[源码](../../../runs/dsv4flash-db-first-full-01/dacomp-038/attempt-01/python/P6.py)；[输出](../../../runs/dsv4flash-db-first-full-01/dacomp-038/attempt-01/python/P6.stdout)；[错误](../../../runs/dsv4flash-db-first-full-01/dacomp-038/attempt-01/python/P6.stderr)。检出需人工核验的 SQL 可实现操作：groupby(, .query(；不能仅凭理由判为合规。

P7：Generate final summary table and comprehensive visualizations: per-family comparison bar chart, market context, and a summary table of all findings.

[源码](../../../runs/dsv4flash-db-first-full-01/dacomp-038/attempt-01/python/P7.py)；[输出](../../../runs/dsv4flash-db-first-full-01/dacomp-038/attempt-01/python/P7.stdout)；[错误](../../../runs/dsv4flash-db-first-full-01/dacomp-038/attempt-01/python/P7.stderr)。检出需人工核验的 SQL 可实现操作：groupby(, .merge(, .query(；不能仅凭理由判为合规。

## 优化机会

已验证候选。筛选限于精确 SQL、相同自包含 CTE、相同单表完整过滤、可分解单表聚合；未覆盖任意 Join 等价和一般谓词蕴含。全部候选都是 offline，未测在线预测。

| 候选 | 类型 | 已有结果 | 覆盖 SQL | 后续次数 | 中间行数 | 验证 | 成本 |
| --- | --- | --- | --- | --- | --- | --- | --- |
| C1 | exact-result reuse | True | ["S27", "S31"] | 1 | 511 | verified | Not benchmarked; correctness alone does not establish net speedup. |
| C2 | exact-result reuse | True | ["S28", "S32"] | 1 | unknown | not_verified_cap | Not tested |
| C3 | exact-result reuse | True | ["S33", "S35", "S36"] | 2 | 511 | verified | Not benchmarked; correctness alone does not establish net speedup. |
| C4 | exact-result reuse | True | ["S34", "S37"] | 1 | unknown | not_verified_cap | Not tested |
| C5 | aggregate MV | False | ["S8", "S10", "S11", "S12", "S13", "S17", "S22", "S24"] | 7 | 45 | verified | Not benchmarked; correctness alone does not establish net speedup. |


已验证覆盖（含触发查询、候选并集去重）：13/35 条成功数据 SQL。正确性仅针对当前数据库快照；未测性能的候选不能声称已加速。

[完整 build/rewrite 与比较证据](dacomp-038.analysis.json)。

### C5：aggregate MV

Union of grouping keys; decomposable aggregate states; AVG uses SUM and non-NULL COUNT.

原查询 [S8](#s8), [S10](#s10), [S11](#s11), [S12](#s12), [S13](#s13), [S17](#s17), [S22](#s22), [S24](#s24) → 新增共享状态 C5 → 后续 7 次可复用。该构建点为事后假设，不代表 Agent 当时预知后续。

构建定义：

```sql
SELECT "Promotion Date" AS __g0, strategy AS __g1, CASE WHEN "Promotion Date" <= '2025-07-03' THEN 'pre' ELSE 'gray' END AS __g2, "Day of the Week" AS __g3, COUNT(*) AS __a0, SUM(impressions) AS __a1, SUM(clicks) AS __a2, SUM("Spend (Yuan)") AS __a3, SUM("Budget Utilization Rate") AS __a4_sum, COUNT("Budget Utilization Rate") AS __a4_n FROM "sheet1"  GROUP BY "Promotion Date", strategy, CASE WHEN "Promotion Date" <= '2025-07-03' THEN 'pre' ELSE 'gray' END, "Day of the Week"
```

受益查询 S8 的改写示例：

```sql
SELECT __g0 AS "Promotion Date", __g1 AS "Strategy", SUM(__a0) AS n_rows FROM temp.reuse_candidate GROUP BY __g0, __g1 ORDER BY __g0, __g1
```

| 原 SQL | 列名一致 | 结果一致 | 比较方法 |
| --- | --- | --- | --- |
| S8 | True | True | ordered_numeric_tolerance |
| S10 | True | True | ordered_numeric_tolerance |
| S11 | True | True | ordered_numeric_tolerance |
| S12 | True | True | ordered_numeric_tolerance |
| S13 | True | True | ordered_numeric_tolerance |
| S17 | True | True | ordered_numeric_tolerance |
| S22 | True | True | exact_multiset |
| S24 | True | True | ordered_numeric_tolerance |


验证状态：verified；成本结论：Not benchmarked; correctness alone does not establish net speedup.

### C3：exact-result reuse

Identical normalized SQL and parameters; archive equality checked.

原查询 [S33](#s33), [S35](#s35), [S36](#s36) → 保留前序结果 S33 → 后续 2 次可复用。该构建点为事后假设，不代表 Agent 当时预知后续。

| 原 SQL | 列名一致 | 结果一致 | 比较方法 |
| --- | --- | --- | --- |
| S35 | True | True | exact_multiset |
| S36 | True | True | exact_multiset |


验证状态：verified；成本结论：Not benchmarked; correctness alone does not establish net speedup.

### C1：exact-result reuse

Identical normalized SQL and parameters; archive equality checked.

原查询 [S27](#s27), [S31](#s31) → 保留前序结果 S27 → 后续 1 次可复用。该构建点为事后假设，不代表 Agent 当时预知后续。

| 原 SQL | 列名一致 | 结果一致 | 比较方法 |
| --- | --- | --- | --- |
| S31 | True | True | ordered_numeric_tolerance |


验证状态：verified；成本结论：Not benchmarked; correctness alone does not establish net speedup.

结果依赖：自动记录 SQL→Python 的接口父调用，以及源码中引用归档文件的消费者；字面值相同不认定因果。模型方向选择需要人工读取消息，尚未做全面因果标注。

[原始报告](../../../runs/dsv4flash-db-first-full-01/dacomp-038/attempt-01/answer.md)；[统一消息](../../../runs/dsv4flash-db-first-full-01/dacomp-038/attempt-01/messages.jsonl)；[原始 OpenCode 事件](../../../runs/dsv4flash-db-first-full-01/dacomp-038/attempt-01/opencode.jsonl)；[SQL 引擎日志](../../../runs/dsv4flash-db-first-full-01/dacomp-038/attempt-01/sql_journal.jsonl)。

[可读报告（本地图片链接规范化）](../answers/dacomp-038.md)。原始回答保留，分析结论未改写。

## S1

类别 `connection_setup`；来源 `connection`；调用 `b7d8d7bcd53645a8a48335f948747859`；状态 `success`。

```sql
PRAGMA query_only=ON
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-038/attempt-01/sql/S1.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-038/attempt-01/sql/S1.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-038/attempt-01/results/S1.rows.jsonl)；完整：True；SHA256：`e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`。

## S2

类别 `metadata`；来源 `list_db`；调用 `b7d8d7bcd53645a8a48335f948747859`；状态 `success`。

```sql
SELECT name,sql FROM sqlite_master WHERE type='table' ORDER BY name
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-038/attempt-01/sql/S2.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-038/attempt-01/sql/S2.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-038/attempt-01/results/S2.rows.jsonl)；完整：True；SHA256：`fe4da93e379031195e7d6daf347af6324a1f32d87304f7f1986769320d2ebb24`。

## S3

类别 `data`；来源 `query_db`；调用 `7defe5b4ec0d4b6d85c049b5089c9404`；状态 `success`。

```sql
SELECT * FROM sheet1 LIMIT 10
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-038/attempt-01/sql/S3.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-038/attempt-01/sql/S3.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-038/attempt-01/results/S3.rows.jsonl)；完整：True；SHA256：`d725170b915c15ef1bb5c52dbbf2d574324563df0756fcb7ef21875736ed8471`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "sheet1", "kind": "base", "block": null, "base_tables": ["sheet1"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |


## S4

类别 `data`；来源 `query_db`；调用 `105816894e7e48c0897a1479f0185198`；状态 `success`。

```sql
SELECT * FROM sheet2 LIMIT 10
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-038/attempt-01/sql/S4.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-038/attempt-01/sql/S4.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-038/attempt-01/results/S4.rows.jsonl)；完整：True；SHA256：`88c40c60fe87f121fc5b149f5e08abd9c37cc45230ce7dc09fde44aaab2d78c4`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "sheet2", "kind": "base", "block": null, "base_tables": ["sheet2"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |


## S5

类别 `data`；来源 `query_db`；调用 `5c634176b00c4e31907cfda8f397ee70`；状态 `success`。

```sql
SELECT DISTINCT Strategy FROM sheet1 ORDER BY Strategy
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-038/attempt-01/sql/S5.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-038/attempt-01/sql/S5.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-038/attempt-01/results/S5.rows.jsonl)；完整：True；SHA256：`4ffae46ed66778865ce0c43975cad512709a5a465d343a9ff5258356e4466fab`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "sheet1", "kind": "base", "block": null, "base_tables": ["sheet1"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |


## S6

类别 `data`；来源 `query_db`；调用 `3d6cbc6c1c974af780f1a71745443995`；状态 `success`。

```sql
SELECT DISTINCT "Promotion Date" FROM sheet1 ORDER BY "Promotion Date"
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-038/attempt-01/sql/S6.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-038/attempt-01/sql/S6.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-038/attempt-01/results/S6.rows.jsonl)；完整：True；SHA256：`088753085fa71f34ea0c67829e77c70bbdfc2ea04ef4a65adedf79cc54773ea7`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "sheet1", "kind": "base", "block": null, "base_tables": ["sheet1"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |


## S7

类别 `data`；来源 `query_db`；调用 `c5ba497e3d074e568af99c2d64270d95`；状态 `success`。

```sql
SELECT DISTINCT "Promotion Date" FROM sheet2 ORDER BY "Promotion Date"
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-038/attempt-01/sql/S7.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-038/attempt-01/sql/S7.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-038/attempt-01/results/S7.rows.jsonl)；完整：True；SHA256：`088753085fa71f34ea0c67829e77c70bbdfc2ea04ef4a65adedf79cc54773ea7`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "sheet2", "kind": "base", "block": null, "base_tables": ["sheet2"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |


## S8

类别 `data`；来源 `query_db`；调用 `b2e75e8d1814443bb416d7e172338e5c`；状态 `success`。

```sql
SELECT "Promotion Date", Strategy, COUNT(*) AS n_rows FROM sheet1 GROUP BY "Promotion Date", Strategy ORDER BY "Promotion Date", Strategy
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-038/attempt-01/sql/S8.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-038/attempt-01/sql/S8.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-038/attempt-01/results/S8.rows.jsonl)；完整：True；SHA256：`9e4d27ccca53e1a7220e189c1ecc95d78aa74f9cac36306dea137f7ed30c9027`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "sheet1", "kind": "base", "block": null, "base_tables": ["sheet1"]}] | [] | ["\"Promotion Date\"", "Strategy"] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |


## S9

类别 `data`；来源 `query_db`；调用 `a5a8faf735c449a2acd692b9ebeb25d6`；状态 `success`。

```sql
SELECT "Promotion Date", COUNT(*) AS n_rows, COUNT(DISTINCT "Promotion Tertiary Category") AS n_cat FROM sheet2 GROUP BY "Promotion Date" ORDER BY "Promotion Date"
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-038/attempt-01/sql/S9.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-038/attempt-01/sql/S9.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-038/attempt-01/results/S9.rows.jsonl)；完整：True；SHA256：`36ac83360c372d0b2bc7cdd2051d5f8e23575965f39740d4f36e564fc864944b`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "sheet2", "kind": "base", "block": null, "base_tables": ["sheet2"]}] | [] | ["\"Promotion Date\""] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |
| B1 | COUNT(DISTINCT "Promotion Tertiary Category") | [{"table": "sheet2", "column": "Promotion Tertiary Category"}] | [] | False |


## S10

类别 `data`；来源 `query_db`；调用 `d17f2acfa0364756879307ec4f082011`；状态 `success`。

```sql
SELECT "Promotion Date", Strategy, COUNT(*) AS n_rows FROM sheet1 GROUP BY "Promotion Date", Strategy ORDER BY Strategy, "Promotion Date"
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-038/attempt-01/sql/S10.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-038/attempt-01/sql/S10.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-038/attempt-01/results/S10.rows.jsonl)；完整：True；SHA256：`c0fc22632bc525447b41580beb0e9ac0cd85aecf4f4f0f5f5b68129c86b4dec3`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "sheet1", "kind": "base", "block": null, "base_tables": ["sheet1"]}] | [] | ["\"Promotion Date\"", "Strategy"] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |


## S11

类别 `data`；来源 `query_db`；调用 `21c42ee5ce5e41bfb504d59011f85846`；状态 `success`。

```sql
SELECT "Promotion Date", Strategy, COUNT(*) AS n_rows FROM sheet1 GROUP BY "Promotion Date", Strategy ORDER BY Strategy, "Promotion Date" LIMIT 20 OFFSET 10
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-038/attempt-01/sql/S11.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-038/attempt-01/sql/S11.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-038/attempt-01/results/S11.rows.jsonl)；完整：True；SHA256：`eaf28f3c897aac0e4263a2837192c27c65052e1b93e0c9dcf3d6f445a40d6bea`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "sheet1", "kind": "base", "block": null, "base_tables": ["sheet1"]}] | [] | ["\"Promotion Date\"", "Strategy"] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |


## S12

类别 `data`；来源 `query_db`；调用 `483a47f8f6a042baacf14595a7ec8b5c`；状态 `success`。

```sql
SELECT "Promotion Date", Strategy, COUNT(*) AS n_rows FROM sheet1 GROUP BY "Promotion Date", Strategy ORDER BY Strategy, "Promotion Date" LIMIT 20 OFFSET 30
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-038/attempt-01/sql/S12.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-038/attempt-01/sql/S12.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-038/attempt-01/results/S12.rows.jsonl)；完整：True；SHA256：`9fe6603f3e8e913a7ae91c1786648ade85738b44a529ba7de705b7019f5e34e5`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "sheet1", "kind": "base", "block": null, "base_tables": ["sheet1"]}] | [] | ["\"Promotion Date\"", "Strategy"] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |


## S13

类别 `data`；来源 `query_db`；调用 `d232834333a54bd6af824dcbddc7d21d`；状态 `success`。

```sql
SELECT "Promotion Date", Strategy, COUNT(*) AS n_rows FROM sheet1 GROUP BY "Promotion Date", Strategy ORDER BY Strategy, "Promotion Date" LIMIT 10 OFFSET 40
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-038/attempt-01/sql/S13.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-038/attempt-01/sql/S13.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-038/attempt-01/results/S13.rows.jsonl)；完整：True；SHA256：`b0721695f04012592e795da5313815d99501d67dc556df2f577aec40815885dc`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "sheet1", "kind": "base", "block": null, "base_tables": ["sheet1"]}] | [] | ["\"Promotion Date\"", "Strategy"] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |


## S14

类别 `data`；来源 `query_db`；调用 `1ed85bbedea34ecbbd9e92e210f02329`；状态 `success`。

```sql
SELECT "Promotion Date", Strategy, COUNT(*) AS n_rows FROM sheet1 WHERE Strategy LIKE 'Renqun%' GROUP BY "Promotion Date", Strategy ORDER BY Strategy, "Promotion Date"
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-038/attempt-01/sql/S14.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-038/attempt-01/sql/S14.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-038/attempt-01/results/S14.rows.jsonl)；完整：True；SHA256：`332afc095f58a25801c1e849b1881d18d9ac67123f66b0da4bc41cfe01788071`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "sheet1", "kind": "base", "block": null, "base_tables": ["sheet1"]}] | [] | ["\"Promotion Date\"", "Strategy"] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |


## S15

类别 `data`；来源 `query_db`；调用 `757dac9e23a24ea8a5cc25f865aaaeaa`；状态 `success`。

```sql
SELECT s."Promotion Date", s."Promotion Tertiary Category",
  MAX(CASE WHEN s.Strategy='Search Strategy v3.6' THEN 1 ELSE 0 END) AS has_old,
  MAX(CASE WHEN s.Strategy='Search Strategy v3.7' THEN 1 ELSE 0 END) AS has_new
FROM sheet1 s
WHERE s.Strategy IN ('Search Strategy v3.6','Search Strategy v3.7') AND s."Promotion Date" >= '2025-07-04'
GROUP BY s."Promotion Date", s."Promotion Tertiary Category"
ORDER BY s."Promotion Date", s."Promotion Tertiary Category"
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-038/attempt-01/sql/S15.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-038/attempt-01/sql/S15.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-038/attempt-01/results/S15.rows.jsonl)；完整：True；SHA256：`aa2801318ffe4060a8eaf5773b43f2ba98106acdc7f472b475ff442c51f1f942`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "s", "kind": "base", "block": null, "base_tables": ["sheet1"]}] | [] | ["s.\"Promotion Date\"", "s.\"Promotion Tertiary Category\""] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | MAX(CASE WHEN s.Strategy = 'Search Strategy v3.6' THEN 1 ELSE 0 END) | [] | [{"table": "sheet1", "column": "Strategy"}] | False |
| B1 | MAX(CASE WHEN s.Strategy = 'Search Strategy v3.7' THEN 1 ELSE 0 END) | [] | [{"table": "sheet1", "column": "Strategy"}] | False |


## S16

类别 `data`；来源 `query_db`；调用 `d4064fdcaaa34af481434b220ac4a037`；状态 `success`。

```sql
SELECT s."Promotion Date",
  COUNT(DISTINCT s."Promotion Tertiary Category") AS n_cats_old,
  (SELECT COUNT(DISTINCT "Promotion Tertiary Category") FROM sheet1 WHERE Strategy='Search Strategy v3.6' AND "Promotion Date"='2025-07-01') AS n_cats_jul1
FROM sheet1 s WHERE s.Strategy='Search Strategy v3.6' AND s."Promotion Date" BETWEEN '2025-07-04' AND '2025-07-07'
GROUP BY s."Promotion Date"
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-038/attempt-01/sql/S16.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-038/attempt-01/sql/S16.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-038/attempt-01/results/S16.rows.jsonl)；完整：True；SHA256：`5bd65a72605e18e3bb865049aa4bbb5232491bc3fcaea5f848645e6308acea7d`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "sheet1", "kind": "base", "block": null, "base_tables": ["sheet1"]}] | [] | [] |
| B2 | [{"alias": "s", "kind": "base", "block": null, "base_tables": ["sheet1"]}] | [] | ["s.\"Promotion Date\""] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(DISTINCT "Promotion Tertiary Category") | [{"table": "sheet1", "column": "Promotion Tertiary Category"}] | [] | False |
| B2 | COUNT(DISTINCT s."Promotion Tertiary Category") | [{"table": "sheet1", "column": "Promotion Tertiary Category"}] | [] | False |


## S17

类别 `data`；来源 `query_db`；调用 `f02fa7a1b1e54a7ebf60761ecce0c8d7`；状态 `success`。

```sql
SELECT
  CASE WHEN "Promotion Date" <= '2025-07-03' THEN 'pre' ELSE 'gray' END AS period,
  Strategy,
  COUNT(*) AS rows,
  ROUND(SUM("Spend (Yuan)"),0) AS spend,
  SUM(Impressions) AS impressions,
  SUM(Clicks) AS clicks,
  ROUND(SUM(Clicks)*1.0/SUM(Impressions),4) AS ctr_w,
  ROUND(SUM("Spend (Yuan)")*1.0/SUM(Clicks),3) AS cpc_w,
  ROUND(SUM("Spend (Yuan)")*1000.0/SUM(Impressions),3) AS cpm_w,
  ROUND(AVG("Budget Utilization Rate"),4) AS budutil_avg
FROM sheet1
GROUP BY period, Strategy
ORDER BY Strategy, period
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-038/attempt-01/sql/S17.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-038/attempt-01/sql/S17.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-038/attempt-01/results/S17.rows.jsonl)；完整：True；SHA256：`7465512a181b73ff8362b7ef364fbecd2e0ed927af0436c8faceb98b8e41c2b0`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "sheet1", "kind": "base", "block": null, "base_tables": ["sheet1"]}] | [] | ["CASE WHEN \"Promotion Date\" <= '2025-07-03' THEN 'pre' ELSE 'gray' END", "Strategy"] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |
| B1 | SUM(Impressions) | [{"table": "sheet1", "column": "Impressions"}] | [] | False |
| B1 | SUM(Clicks) | [{"table": "sheet1", "column": "Clicks"}] | [] | False |
| B1 | SUM("Spend (Yuan)") | [{"table": "sheet1", "column": "Spend (Yuan)"}] | [] | False |
| B1 | AVG("Budget Utilization Rate") | [{"table": "sheet1", "column": "Budget Utilization Rate"}] | [] | False |
| B1 | SUM(Impressions) | [{"table": "sheet1", "column": "Impressions"}] | [] | False |
| B1 | SUM(Clicks) | [{"table": "sheet1", "column": "Clicks"}] | [] | False |
| B1 | SUM(Impressions) | [{"table": "sheet1", "column": "Impressions"}] | [] | False |
| B1 | SUM(Clicks) | [{"table": "sheet1", "column": "Clicks"}] | [] | False |
| B1 | SUM("Spend (Yuan)") | [{"table": "sheet1", "column": "Spend (Yuan)"}] | [] | False |
| B1 | SUM("Spend (Yuan)") | [{"table": "sheet1", "column": "Spend (Yuan)"}] | [] | False |


## S18

类别 `data`；来源 `query_db`；调用 `876400e909d1400d8d5979c3d05cb968`；状态 `success`。

```sql
SELECT
  s."Promotion Tertiary Category",
  MAX(CASE WHEN s."Promotion Date" <= '2025-07-03' THEN 1 ELSE 0 END) AS in_pre,
  MAX(CASE WHEN s."Promotion Date" >= '2025-07-04' AND s.Strategy='Search Strategy v3.6' THEN 1 ELSE 0 END) AS in_old_gray,
  MAX(CASE WHEN s."Promotion Date" >= '2025-07-04' AND s.Strategy='Search Strategy v3.7' THEN 1 ELSE 0 END) AS in_new_gray
FROM sheet1 s
WHERE s.Strategy IN ('Search Strategy v3.6','Search Strategy v3.7')
GROUP BY s."Promotion Tertiary Category"
ORDER BY s."Promotion Tertiary Category"
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-038/attempt-01/sql/S18.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-038/attempt-01/sql/S18.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-038/attempt-01/results/S18.rows.jsonl)；完整：True；SHA256：`0f16509f53451b65a91c8cb1fd209fc725f2dda84c2e68f0ab36bf47d5d6b146`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "s", "kind": "base", "block": null, "base_tables": ["sheet1"]}] | [] | ["s.\"Promotion Tertiary Category\""] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | MAX(CASE WHEN s."Promotion Date" <= '2025-07-03' THEN 1 ELSE 0 END) | [] | [{"table": "sheet1", "column": "Promotion Date"}] | False |
| B1 | MAX(CASE WHEN s."Promotion Date" >= '2025-07-04' AND s.Strategy = 'Search Strategy v3.6' THEN 1 ELSE 0 END) | [] | [{"table": "sheet1", "column": "Promotion Date"}, {"table": "sheet1", "column": "Strategy"}] | False |
| B1 | MAX(CASE WHEN s."Promotion Date" >= '2025-07-04' AND s.Strategy = 'Search Strategy v3.7' THEN 1 ELSE 0 END) | [] | [{"table": "sheet1", "column": "Promotion Date"}, {"table": "sheet1", "column": "Strategy"}] | False |


## S19

类别 `data`；来源 `query_db`；调用 `5742c7e4d34246fdb82909cec5f01bd3`；状态 `success`。

```sql
-- Caixi Strategy
SELECT
  s."Promotion Tertiary Category",
  MAX(CASE WHEN s."Promotion Date" <= '2025-07-03' THEN 1 ELSE 0 END) AS in_pre,
  MAX(CASE WHEN s."Promotion Date" >= '2025-07-04' AND s.Strategy='Caixi Strategy v4.8' THEN 1 ELSE 0 END) AS in_old_gray,
  MAX(CASE WHEN s."Promotion Date" >= '2025-07-04' AND s.Strategy='Caixi Strategy v4.9' THEN 1 ELSE 0 END) AS in_new_gray
FROM sheet1 s
WHERE s.Strategy IN ('Caixi Strategy v4.8','Caixi Strategy v4.9')
GROUP BY s."Promotion Tertiary Category"
ORDER BY s."Promotion Tertiary Category"
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-038/attempt-01/sql/S19.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-038/attempt-01/sql/S19.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-038/attempt-01/results/S19.rows.jsonl)；完整：True；SHA256：`abd6a5cc160ac9854358ad61aaafd7e56cd94076ebff2b160667be04f63b837f`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "s", "kind": "base", "block": null, "base_tables": ["sheet1"]}] | [] | ["s.\"Promotion Tertiary Category\""] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | MAX(CASE WHEN s."Promotion Date" <= '2025-07-03' THEN 1 ELSE 0 END) | [] | [{"table": "sheet1", "column": "Promotion Date"}] | False |
| B1 | MAX(CASE WHEN s."Promotion Date" >= '2025-07-04' AND s.Strategy = 'Caixi Strategy v4.8' THEN 1 ELSE 0 END) | [] | [{"table": "sheet1", "column": "Promotion Date"}, {"table": "sheet1", "column": "Strategy"}] | False |
| B1 | MAX(CASE WHEN s."Promotion Date" >= '2025-07-04' AND s.Strategy = 'Caixi Strategy v4.9' THEN 1 ELSE 0 END) | [] | [{"table": "sheet1", "column": "Promotion Date"}, {"table": "sheet1", "column": "Strategy"}] | False |


## S20

类别 `data`；来源 `query_db`；调用 `93baca72ef5f4815bfe8b7c55315052f`；状态 `success`。

```sql
-- Popup Strategy
SELECT
  s."Promotion Tertiary Category",
  MAX(CASE WHEN s."Promotion Date" <= '2025-07-03' THEN 1 ELSE 0 END) AS in_pre,
  MAX(CASE WHEN s."Promotion Date" >= '2025-07-04' AND s.Strategy='Popup Strategy v2.9' THEN 1 ELSE 0 END) AS in_old_gray,
  MAX(CASE WHEN s."Promotion Date" >= '2025-07-04' AND s.Strategy='Popup Strategy v2.9.1' THEN 1 ELSE 0 END) AS in_new_gray
FROM sheet1 s
WHERE s.Strategy IN ('Popup Strategy v2.9','Popup Strategy v2.9.1')
GROUP BY s."Promotion Tertiary Category"
ORDER BY s."Promotion Tertiary Category"
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-038/attempt-01/sql/S20.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-038/attempt-01/sql/S20.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-038/attempt-01/results/S20.rows.jsonl)；完整：True；SHA256：`392cd761fd46861d3e123cb64fdca8137f847b834ba64d6a63d9181e6f9dd6d7`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "s", "kind": "base", "block": null, "base_tables": ["sheet1"]}] | [] | ["s.\"Promotion Tertiary Category\""] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | MAX(CASE WHEN s."Promotion Date" <= '2025-07-03' THEN 1 ELSE 0 END) | [] | [{"table": "sheet1", "column": "Promotion Date"}] | False |
| B1 | MAX(CASE WHEN s."Promotion Date" >= '2025-07-04' AND s.Strategy = 'Popup Strategy v2.9' THEN 1 ELSE 0 END) | [] | [{"table": "sheet1", "column": "Promotion Date"}, {"table": "sheet1", "column": "Strategy"}] | False |
| B1 | MAX(CASE WHEN s."Promotion Date" >= '2025-07-04' AND s.Strategy = 'Popup Strategy v2.9.1' THEN 1 ELSE 0 END) | [] | [{"table": "sheet1", "column": "Promotion Date"}, {"table": "sheet1", "column": "Strategy"}] | False |


## S21

类别 `data`；来源 `query_db`；调用 `c5dc9862d53e49e79a30fc920357096e`；状态 `success`。

```sql
-- Renqun Dongcha Strategy
SELECT
  s."Promotion Tertiary Category",
  MAX(CASE WHEN s."Promotion Date" <= '2025-07-03' THEN 1 ELSE 0 END) AS in_pre,
  MAX(CASE WHEN s."Promotion Date" >= '2025-07-04' AND s.Strategy='Renqun Dongcha Strategy v3.2' THEN 1 ELSE 0 END) AS in_old_gray,
  MAX(CASE WHEN s."Promotion Date" >= '2025-07-04' AND s.Strategy='Renqun Dongcha Strategy v3.2.1' THEN 1 ELSE 0 END) AS in_new_gray
FROM sheet1 s
WHERE s.Strategy IN ('Renqun Dongcha Strategy v3.2','Renqun Dongcha Strategy v3.2.1')
GROUP BY s."Promotion Tertiary Category"
ORDER BY s."Promotion Tertiary Category"
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-038/attempt-01/sql/S21.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-038/attempt-01/sql/S21.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-038/attempt-01/results/S21.rows.jsonl)；完整：True；SHA256：`53ef58bf41caf50e0f4184a4b83d59ef4c15fae350480f3eaf649f7ed5fbe9a0`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "s", "kind": "base", "block": null, "base_tables": ["sheet1"]}] | [] | ["s.\"Promotion Tertiary Category\""] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | MAX(CASE WHEN s."Promotion Date" <= '2025-07-03' THEN 1 ELSE 0 END) | [] | [{"table": "sheet1", "column": "Promotion Date"}] | False |
| B1 | MAX(CASE WHEN s."Promotion Date" >= '2025-07-04' AND s.Strategy = 'Renqun Dongcha Strategy v3.2' THEN 1 ELSE 0 END) | [] | [{"table": "sheet1", "column": "Promotion Date"}, {"table": "sheet1", "column": "Strategy"}] | False |
| B1 | MAX(CASE WHEN s."Promotion Date" >= '2025-07-04' AND s.Strategy = 'Renqun Dongcha Strategy v3.2.1' THEN 1 ELSE 0 END) | [] | [{"table": "sheet1", "column": "Promotion Date"}, {"table": "sheet1", "column": "Strategy"}] | False |


## S22

类别 `data`；来源 `query_db`；调用 `3e6c37496ee6484895208f24b1ce6d88`；状态 `success`。

```sql
SELECT COUNT(*) AS n FROM sheet1
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-038/attempt-01/sql/S22.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-038/attempt-01/sql/S22.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-038/attempt-01/results/S22.rows.jsonl)；完整：True；SHA256：`f144cb81e4029db5f7c64a4fe6841dc884e0cde201eb20d36144b5ecc65aa45c`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "sheet1", "kind": "base", "block": null, "base_tables": ["sheet1"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |


## S23

类别 `data`；来源 `query_db`；调用 `c438de09bfab42089473c39345c8fcf7`；状态 `success`。

```sql
SELECT COUNT(*) AS n FROM sheet2
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-038/attempt-01/sql/S23.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-038/attempt-01/sql/S23.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-038/attempt-01/results/S23.rows.jsonl)；完整：True；SHA256：`f144cb81e4029db5f7c64a4fe6841dc884e0cde201eb20d36144b5ecc65aa45c`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "sheet2", "kind": "base", "block": null, "base_tables": ["sheet2"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |


## S24

类别 `data`；来源 `query_db`；调用 `d2fd8ba4303343d8b25fa8f1a676922d`；状态 `success`。

```sql
SELECT "Day of the Week", COUNT(*) AS n FROM sheet1 GROUP BY "Day of the Week" ORDER BY "Promotion Date"
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-038/attempt-01/sql/S24.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-038/attempt-01/sql/S24.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-038/attempt-01/results/S24.rows.jsonl)；完整：True；SHA256：`3d06c73549f11954c32f5489a3c0aeb87c50df6f634090469eb5e6bf3d4f4f33`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "sheet1", "kind": "base", "block": null, "base_tables": ["sheet1"]}] | [] | ["\"Day of the Week\""] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |


## S25

类别 `data`；来源 `python`；调用 `14bf08e9a8714a979a97c420f43c040d`；状态 `success`。

```sql
SELECT * FROM sheet1 ORDER BY "Promotion Date", "Promotion Tertiary Category", Strategy
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-038/attempt-01/sql/S25.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-038/attempt-01/sql/S25.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-038/attempt-01/results/S25.rows.jsonl)；完整：True；SHA256：`de7eafe7f93c6cd4ae7ede537b9ab024df8ae909170168b8ff49b0703c0b6881`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "sheet1", "kind": "base", "block": null, "base_tables": ["sheet1"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |


## S26

类别 `data`；来源 `python`；调用 `14bf08e9a8714a979a97c420f43c040d`；状态 `success`。

```sql
SELECT * FROM sheet2 ORDER BY "Promotion Date", "Promotion Tertiary Category"
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-038/attempt-01/sql/S26.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-038/attempt-01/sql/S26.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-038/attempt-01/results/S26.rows.jsonl)；完整：True；SHA256：`e343970cb984f878befc749ba997908581ff10e9fedbae6d903ed943cb4eba68`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "sheet2", "kind": "base", "block": null, "base_tables": ["sheet2"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |


## S27

类别 `data`；来源 `python`；调用 `402ea4c8f18644428432da196eaea0fb`；状态 `success`。

```sql
SELECT * FROM sheet1 ORDER BY "Promotion Date"
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-038/attempt-01/sql/S27.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-038/attempt-01/sql/S27.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-038/attempt-01/results/S27.rows.jsonl)；完整：True；SHA256：`0023aa9afcddca4eccb7bcdcc09853de01b055a54c0f7cb12208e4837edbaf99`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "sheet1", "kind": "base", "block": null, "base_tables": ["sheet1"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |


## S28

类别 `data`；来源 `python`；调用 `402ea4c8f18644428432da196eaea0fb`；状态 `success`。

```sql
SELECT * FROM sheet2 ORDER BY "Promotion Date"
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-038/attempt-01/sql/S28.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-038/attempt-01/sql/S28.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-038/attempt-01/results/S28.rows.jsonl)；完整：True；SHA256：`613308747797105b0db4d52320a26aa2d1783cdb60ad6a62d867d77e37d3dcd3`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "sheet2", "kind": "base", "block": null, "base_tables": ["sheet2"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |


## S29

类别 `data`；来源 `query_db`；调用 `52961f4ba6c64a9ab89695fa2d233222`；状态 `success`。

```sql
SELECT "Promotion Date", Strategy, COUNT(*) AS n, ROUND(SUM("Spend (Yuan)"),1) AS spend
FROM sheet1 WHERE Strategy LIKE 'Search%'
GROUP BY "Promotion Date", Strategy ORDER BY "Promotion Date", Strategy
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-038/attempt-01/sql/S29.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-038/attempt-01/sql/S29.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-038/attempt-01/results/S29.rows.jsonl)；完整：True；SHA256：`c2f06b6cc133df23d6328e47e0656add0801740afedf5ba26e019e59104cf9f9`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "sheet1", "kind": "base", "block": null, "base_tables": ["sheet1"]}] | [] | ["\"Promotion Date\"", "Strategy"] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |
| B1 | SUM("Spend (Yuan)") | [{"table": "sheet1", "column": "Spend (Yuan)"}] | [] | False |


## S30

类别 `data`；来源 `query_db`；调用 `09a82c00764a4d1a86bb645d475fcc61`；状态 `success`。

```sql
SELECT "Promotion Date", COUNT(*) AS n, COUNT(DISTINCT "Promotion Tertiary Category") AS n_cat
FROM sheet1 WHERE Strategy='Search Strategy v3.6'
GROUP BY "Promotion Date" ORDER BY "Promotion Date"
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-038/attempt-01/sql/S30.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-038/attempt-01/sql/S30.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-038/attempt-01/results/S30.rows.jsonl)；完整：True；SHA256：`470b42f2812e75c38be9653b4f0c248c6d3bc1a2fdbd6a4d9d3dfb0c99c3258d`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "sheet1", "kind": "base", "block": null, "base_tables": ["sheet1"]}] | [] | ["\"Promotion Date\""] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |
| B1 | COUNT(DISTINCT "Promotion Tertiary Category") | [{"table": "sheet1", "column": "Promotion Tertiary Category"}] | [] | False |


## S31

类别 `data`；来源 `python`；调用 `ccc75fbded9d4227b1cbcdd352c8c300`；状态 `success`。

```sql
SELECT * FROM sheet1 ORDER BY "Promotion Date"
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-038/attempt-01/sql/S31.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-038/attempt-01/sql/S31.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-038/attempt-01/results/S31.rows.jsonl)；完整：True；SHA256：`0023aa9afcddca4eccb7bcdcc09853de01b055a54c0f7cb12208e4837edbaf99`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "sheet1", "kind": "base", "block": null, "base_tables": ["sheet1"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |


## S32

类别 `data`；来源 `python`；调用 `ccc75fbded9d4227b1cbcdd352c8c300`；状态 `success`。

```sql
SELECT * FROM sheet2 ORDER BY "Promotion Date"
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-038/attempt-01/sql/S32.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-038/attempt-01/sql/S32.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-038/attempt-01/results/S32.rows.jsonl)；完整：True；SHA256：`613308747797105b0db4d52320a26aa2d1783cdb60ad6a62d867d77e37d3dcd3`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "sheet2", "kind": "base", "block": null, "base_tables": ["sheet2"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |


## S33

类别 `data`；来源 `python`；调用 `dd855877975744e4937c5ce32534feb8`；状态 `success`。

```sql
SELECT * FROM sheet1
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-038/attempt-01/sql/S33.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-038/attempt-01/sql/S33.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-038/attempt-01/results/S33.rows.jsonl)；完整：True；SHA256：`f525377f8a273107a0a021f624ee0c08347cb5bce4d2ff2cb95b6340fd81b6fa`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "sheet1", "kind": "base", "block": null, "base_tables": ["sheet1"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |


## S34

类别 `data`；来源 `python`；调用 `dd855877975744e4937c5ce32534feb8`；状态 `success`。

```sql
SELECT * FROM sheet2
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-038/attempt-01/sql/S34.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-038/attempt-01/sql/S34.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-038/attempt-01/results/S34.rows.jsonl)；完整：True；SHA256：`1d3749ce2216cad55513877461ab74ea72e94529616f6ebc10d59142692c12f2`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "sheet2", "kind": "base", "block": null, "base_tables": ["sheet2"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |


## S35

类别 `data`；来源 `python`；调用 `8df1f950c0b24edcb707fad650edb262`；状态 `success`。

```sql
SELECT * FROM sheet1
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-038/attempt-01/sql/S35.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-038/attempt-01/sql/S35.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-038/attempt-01/results/S35.rows.jsonl)；完整：True；SHA256：`f525377f8a273107a0a021f624ee0c08347cb5bce4d2ff2cb95b6340fd81b6fa`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "sheet1", "kind": "base", "block": null, "base_tables": ["sheet1"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |


## S36

类别 `data`；来源 `python`；调用 `633130d189ef4878a8ad30edc7b05f8f`；状态 `success`。

```sql
SELECT * FROM sheet1
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-038/attempt-01/sql/S36.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-038/attempt-01/sql/S36.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-038/attempt-01/results/S36.rows.jsonl)；完整：True；SHA256：`f525377f8a273107a0a021f624ee0c08347cb5bce4d2ff2cb95b6340fd81b6fa`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "sheet1", "kind": "base", "block": null, "base_tables": ["sheet1"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |


## S37

类别 `data`；来源 `python`；调用 `633130d189ef4878a8ad30edc7b05f8f`；状态 `success`。

```sql
SELECT * FROM sheet2
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-038/attempt-01/sql/S37.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-038/attempt-01/sql/S37.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-038/attempt-01/results/S37.rows.jsonl)；完整：True；SHA256：`1d3749ce2216cad55513877461ab74ea72e94529616f6ebc10d59142692c12f2`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "sheet2", "kind": "base", "block": null, "base_tables": ["sheet2"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |

