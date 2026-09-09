# dacomp-034

At the Level 1 Category level, analyze the relationship between discount depth and sales f…

运行：已提交。官方未评分。全部 SQL 尝试/成功 35/34；数据 SQL 33/32；Python 13 次。

完整原题：

At the Level 1 Category level, analyze the relationship between discount depth and sales for single-item direct price reduction promotions, assess differences in promotion effectiveness across categories, and, based on the findings, propose recommendations to optimize promotion resource allocation and discount strategies.

| 表 | 行数 | 列数 |
| --- | --- | --- |
| attachment_1 | 611200 | 10 |
| attachment_1_&_attachment_2_fie | 12 | 8 |
| attachment_2 | 610655 | 10 |
| attachment_3 | 1048575 | 27 |
| attachment_3_field_description | 38 | 3 |
| attachment_4 | 6570 | 8 |
| attachment_4_field_description | 8 | 2 |


实际路线（分析者依据 SQL/源码概括，不代表 Agent 自述）：关联单品直降促销与一级品类 → 提取折扣和销量 → Python 相关/回归、折扣分箱和品类对比 → 绘图及细分品类分析。

数据库大小：349,499,392 字节。

## 数据 SQL

| SQL | 状态 | 基础表 | Join 输入/类型 | GROUP BY | 聚合表达式 | 结果行数 | 数据库 ms |
| --- | --- | --- | --- | --- | --- | --- | --- |
| [S3/Q1](#s3) | success | ["attachment_1"] | 0 / {} | [] | [] | 5 | 0.353 |
| [S4/Q2](#s4) | success | ["attachment_3"] | 0 / {} | [] | [] | 5 | 0.399 |
| [S5/Q3](#s5) | success | ["attachment_4"] | 0 / {} | [] | [] | 5 | 0.333 |
| [S6/Q4](#s6) | success | ["attachment_3_field_description"] | 0 / {} | [] | [] | 38 | 0.341 |
| [S7/Q5](#s7) | success | ["\"attachment_1_&_attachment_2_fie\""] | 0 / {} | [] | [] | 12 | 0.339 |
| [S8/Q6](#s8) | success | ["attachment_4_field_description"] | 0 / {} | [] | [] | 8 | 0.406 |
| [S9/Q7](#s9) | success | ["attachment_3"] | 0 / {} | ["promotion_type"] | ["COUNT(*)"] | 4 | 383.179 |
| [S10/Q8](#s10) | success | ["attachment_3"] | 0 / {} | ["state"] | ["COUNT(*)"] | 3 | 356.539 |
| [S11/Q9](#s11) | success | ["attachment_1"] | 0 / {} | [] | ["COUNT(*)"] | 1 | 24.279 |
| [S12/Q10](#s12) | success | ["attachment_2"] | 0 / {} | [] | ["COUNT(*)"] | 1 | 24.201 |
| [S13/Q11](#s13) | success | ["attachment_3"] | 0 / {} | [] | ["COUNT(*)"] | 1 | 10.871 |
| [S14/Q12](#s14) | success | ["attachment_4"] | 0 / {} | [] | ["COUNT(*)", "COUNT(DISTINCT sku_id)"] | 1 | 3.135 |
| [S15/Q13](#s15) | success | ["attachment_4"] | 0 / {} | [] | [] | 29 | 1.883 |
| [S16/Q14](#s16) | success | ["attachment_1"] | 0 / {} | [] | ["COUNT(*)"] | 1 | 66.989 |
| [S17/Q15](#s17) | success | ["attachment_2"] | 0 / {} | [] | ["COUNT(*)"] | 1 | 66.85 |
| [S18/Q16](#s18) | success | ["attachment_3"] | 0 / {} | [] | [] | 5 | 0.363 |
| [S19/Q17](#s19) | success | ["attachment_1"] | 0 / {} | [] | ["MIN(create_dt)", "MAX(create_dt)"] | 1 | 84.783 |
| [S20/Q18](#s20) | success | ["attachment_3"] | 0 / {} | [] | ["MIN(create_dt)", "MAX(create_dt)"] | 1 | 123.736 |
| [S21/Q19](#s21) | success | ["attachment_3"] | 0 / {} | ["validation"] | ["COUNT(*)"] | 1 | 88.706 |
| [S22/Q20](#s22) | success | ["attachment_3"] | 0 / {} | ["promotion_type", "state"] | ["COUNT(*)", "SUM(sale_count)"] | 5 | 91.168 |
| [S23/Q21](#s23) | success | ["attachment_3"] | 0 / {} | [] | ["COUNT(DISTINCT sku_id)"] | 1 | 93.405 |
| [S24/Q22](#s24) | success | ["attachment_1", "attachment_3"] | 2 / {'LEFT': 1} | [] | ["COUNT(DISTINCT a3.sku_id)", "COUNT(DISTINCT CASE WHEN NOT a1.sku_id IS NULL THEN a3.sku_id END)"] | 1 | 281.578 |
| [S25/Q23](#s25) | success | ["attachment_3"] | 0 / {} | ["promotion_type"] | ["COUNT(*)", "AVG(1.0 - promotion_price / pdj_price)", "SUM(sale_count)"] | 3 | 92.695 |
| [S26/Q24](#s26) | success | ["attachment_3"] | 0 / {} | [] | ["MIN(pdj_price)", "MAX(pdj_price)", "MIN(promotion_price)", "MAX(promotion_price)", "MIN(1.0 - promotion_price / pdj_price)", "MAX(1.0 - promotion_price / pdj_price)", "AVG(1.0 - promotion_price / pdj_price)"] | 1 | 93.925 |
| [S27/Q25](#s27) | success | ["attachment_3", "attachment_4"] | 2 / {'INNER': 1} | ["a4.\"Level 1 Category Name\""] | ["COUNT(*)", "SUM(a3.sale_count)", "AVG(1.0 - a3.promotion_price / a3.pdj_price)", "AVG(a3.sale_count)"] | 17 | 103.847 |
| [S28/Q26](#s28) | success | ["attachment_3", "attachment_4"] | 2 / {'INNER': 1} | [] | [] | 5620 | 110.29 |
| [S29/Q27](#s29) | success | ["attachment_1", "attachment_3"] | 2 / {'INNER': 1} | [] | ["COUNT(*)"] | 1 | 1802.224 |
| [S30/Q28](#s30) | success | ["attachment_1", "attachment_3"] | 2 / {'INNER': 1} | [] | [] | 5 | 1253.432 |
| [S31/Q29](#s31) | success | ["attachment_3", "attachment_4"] | 2 / {'INNER': 1} | [] | [] | 5620 | 111.324 |
| [S32/Q30](#s32) | failed | ["attachment_1", "attachment_2"] | 2 / {'CROSS': 1} | [] | ["COUNT(DISTINCT sku_id)", "COUNT(DISTINCT sku_id)"] | unknown | 未取得；调用总时长 0.169 ms |
| [S33/Q31](#s33) | success | ["attachment_1", "attachment_2"] | 0 / {} | [] | ["MIN(create_dt)", "MAX(create_dt)", "MIN(create_dt)", "MAX(create_dt)"] | 2 | 168.578 |
| [S34/Q32](#s34) | success | ["attachment_1", "attachment_2"] | 2 / {'INNER': 1} | [] | ["COUNT(*)"] | 1 | 1776.106 |
| [S35/Q33](#s35) | success | ["attachment_1", "attachment_2"] | 0 / {} | [] | ["COUNT(*)", "SUM(CASE WHEN \"SKU Cost Price\" > 0 THEN 1 ELSE 0 END)", "COUNT(*)", "SUM(CASE WHEN \"SKU Cost Price\" > 0 THEN 1 ELSE 0 END)", "COUNT(*)", "SUM(CASE WHEN \"SKU Cost Price\" > 0 THEN 1 ELSE 0 END)", "COUNT(*)", "SUM(CASE WHEN \"SKU Cost Price\" > 0 THEN 1 ELSE 0 END)"] | 2 | 164.446 |


## 元数据和设置

| SQL | 类别 | 状态 | 内容 |
| --- | --- | --- | --- |
| S1 | connection_setup | success | PRAGMA query_only=ON |
| S2 | metadata | success | SELECT name,sql FROM sqlite_master WHERE type='table' ORDER BY name |


## Python 与执行位置

人工源码审查：**database_first_violation**。SQL 提取促销、商品和品类数据；Python 的相关、回归与 Kruskal 检验有合理统计用途。但 P8–P11 还按折扣深度分箱，汇总销量/销售额并筛选头部品类，这些可由 SQLite CASE、GROUP BY 和排序完成。绘图不能作为将这些准备计算整体移出数据库的理由。 [证据](../reviews/dacomp-034.json)。

P1：Statistical analysis (correlations, regressions, binned comparisons) is not well supported by SQLite, so I load the 5620 promotion-level records (already filtered/joined in SQL) into pandas for analysis and visualization.

[源码](../../../runs/dsv4flash-db-first-full-01/dacomp-034/attempt-01/python/P1.py)；[输出](../../../runs/dsv4flash-db-first-full-01/dacomp-034/attempt-01/python/P1.stdout)；[错误](../../../runs/dsv4flash-db-first-full-01/dacomp-034/attempt-01/python/P1.stderr)。检出需人工核验的 SQL 可实现操作：groupby(；不能仅凭理由判为合规。

P2：Loading the promotion-level data from the JSON Lines file produced by SQL query S28 for statistical analysis and visualization.

[源码](../../../runs/dsv4flash-db-first-full-01/dacomp-034/attempt-01/python/P2.py)；[输出](../../../runs/dsv4flash-db-first-full-01/dacomp-034/attempt-01/python/P2.stdout)；[错误](../../../runs/dsv4flash-db-first-full-01/dacomp-034/attempt-01/python/P2.stderr)。自动源码筛查未检出预设迁出信号；这不是全面语义合规证明。

P3：Locating the results archive directory from the Python environment (which runs in /work) so I can read the promotion-level rows produced by SQL.

[源码](../../../runs/dsv4flash-db-first-full-01/dacomp-034/attempt-01/python/P3.py)；[输出](../../../runs/dsv4flash-db-first-full-01/dacomp-034/attempt-01/python/P3.stdout)；[错误](../../../runs/dsv4flash-db-first-full-01/dacomp-034/attempt-01/python/P3.stderr)。自动源码筛查未检出预设迁出信号；这不是全面语义合规证明。

P4：Loading the promotion-level data from /results/S28.rows.jsonl for statistical analysis (correlations, binned sales, per-category elasticity) and visualization.

[源码](../../../runs/dsv4flash-db-first-full-01/dacomp-034/attempt-01/python/P4.py)；[输出](../../../runs/dsv4flash-db-first-full-01/dacomp-034/attempt-01/python/P4.stdout)；[错误](../../../runs/dsv4flash-db-first-full-01/dacomp-034/attempt-01/python/P4.stderr)。检出需人工核验的 SQL 可实现操作：groupby(；不能仅凭理由判为合规。

P5：Per-category correlation and regression analysis to assess differences in promotion effectiveness across Level 1 categories.

[源码](../../../runs/dsv4flash-db-first-full-01/dacomp-034/attempt-01/python/P5.py)；[输出](../../../runs/dsv4flash-db-first-full-01/dacomp-034/attempt-01/python/P5.stdout)；[错误](../../../runs/dsv4flash-db-first-full-01/dacomp-034/attempt-01/python/P5.stderr)。检出需人工核验的 SQL 可实现操作：sort_values(；不能仅凭理由判为合规。

P6：Per-category correlation and regression analysis, handling categories with <2 records by skipping correlation for those.

[源码](../../../runs/dsv4flash-db-first-full-01/dacomp-034/attempt-01/python/P6.py)；[输出](../../../runs/dsv4flash-db-first-full-01/dacomp-034/attempt-01/python/P6.stdout)；[错误](../../../runs/dsv4flash-db-first-full-01/dacomp-034/attempt-01/python/P6.stderr)。检出需人工核验的 SQL 可实现操作：sort_values(；不能仅凭理由判为合规。

P7：Checking capacity-constraint (sale_count vs limit_count) patterns which may confound the discount-sales relationship, using the already-loaded promotion data.

[源码](../../../runs/dsv4flash-db-first-full-01/dacomp-034/attempt-01/python/P7.py)；[输出](../../../runs/dsv4flash-db-first-full-01/dacomp-034/attempt-01/python/P7.stdout)；[错误](../../../runs/dsv4flash-db-first-full-01/dacomp-034/attempt-01/python/P7.stderr)。检出需人工核验的 SQL 可实现操作：groupby(, sort_values(；不能仅凭理由判为合规。

P8：Creating visualizations: overall scatter with regression, binned bar chart, categorized scatter plots, and per-category comparison to illustrate the discount-sales relationship and category differences.

[源码](../../../runs/dsv4flash-db-first-full-01/dacomp-034/attempt-01/python/P8.py)；[输出](../../../runs/dsv4flash-db-first-full-01/dacomp-034/attempt-01/python/P8.stdout)；[错误](../../../runs/dsv4flash-db-first-full-01/dacomp-034/attempt-01/python/P8.stderr)。检出需人工核验的 SQL 可实现操作：groupby(, sort_values(；不能仅凭理由判为合规。

P9：Analyzing revenue and margin implications of discount depth (needs per-record arithmetic on promotion price/cost/allowance) and testing for category-level differences in sales effectiveness with nonparametric ANOVA.

[源码](../../../runs/dsv4flash-db-first-full-01/dacomp-034/attempt-01/python/P9.py)；[输出](../../../runs/dsv4flash-db-first-full-01/dacomp-034/attempt-01/python/P9.stdout)；[错误](../../../runs/dsv4flash-db-first-full-01/dacomp-034/attempt-01/python/P9.stderr)。检出需人工核验的 SQL 可实现操作：groupby(；不能仅凭理由判为合规。

P10：Constructing a per-category x discount-depth matrix of promotion effectiveness (avg units, revenue) to identify category-specific sweet spots and where deep discounts pay off vs. destroy revenue.

[源码](../../../runs/dsv4flash-db-first-full-01/dacomp-034/attempt-01/python/P10.py)；[输出](../../../runs/dsv4flash-db-first-full-01/dacomp-034/attempt-01/python/P10.stdout)；[错误](../../../runs/dsv4flash-db-first-full-01/dacomp-034/attempt-01/python/P10.stderr)。检出需人工核验的 SQL 可实现操作：groupby(；不能仅凭理由判为合规。

P11：Creating a heatmap of category x discount depth effectiveness (average units per promotion) to visually highlight category differences and optimal discount strategies.

[源码](../../../runs/dsv4flash-db-first-full-01/dacomp-034/attempt-01/python/P11.py)；[输出](../../../runs/dsv4flash-db-first-full-01/dacomp-034/attempt-01/python/P11.stdout)；[错误](../../../runs/dsv4flash-db-first-full-01/dacomp-034/attempt-01/python/P11.stderr)。检出需人工核验的 SQL 可实现操作：groupby(, sort_values(；不能仅凭理由判为合规。

P12：Fixing the per-category correlation bar chart by converting the correlation values to numeric (handling N/A strings).

[源码](../../../runs/dsv4flash-db-first-full-01/dacomp-034/attempt-01/python/P12.py)；[输出](../../../runs/dsv4flash-db-first-full-01/dacomp-034/attempt-01/python/P12.stdout)；[错误](../../../runs/dsv4flash-db-first-full-01/dacomp-034/attempt-01/python/P12.stderr)。检出需人工核验的 SQL 可实现操作：groupby(, sort_values(；不能仅凭理由判为合规。

P13：Investigating why Meat shows a negative discount-sales correlation: checking whether deep discounts are applied to higher-priced items (a confound) via correlation and partial analysis.

[源码](../../../runs/dsv4flash-db-first-full-01/dacomp-034/attempt-01/python/P13.py)；[输出](../../../runs/dsv4flash-db-first-full-01/dacomp-034/attempt-01/python/P13.stdout)；[错误](../../../runs/dsv4flash-db-first-full-01/dacomp-034/attempt-01/python/P13.stderr)。检出需人工核验的 SQL 可实现操作：groupby(；不能仅凭理由判为合规。

## 优化机会

已验证候选。筛选限于精确 SQL、相同自包含 CTE、相同单表完整过滤、可分解单表聚合；未覆盖任意 Join 等价和一般谓词蕴含。全部候选都是 offline，未测在线预测。

| 候选 | 类型 | 已有结果 | 覆盖 SQL | 后续次数 | 中间行数 | 验证 | 成本 |
| --- | --- | --- | --- | --- | --- | --- | --- |
| C1 | aggregate MV | False | ["S11", "S19"] | 1 | unknown | not_verified_cap | Not tested |
| C2 | aggregate MV | False | ["S9", "S10", "S13", "S20"] | 3 | 6 | verified | Warm-cache baseline 866.009 ms vs build+reuse 599.216 ms, ratio 1.445; five repetitions, see performance evidence. |
| C3 | common filtered view | False | ["S18", "S23"] | 1 | unknown | not_verified_cap | Not tested |
| C4 | common filtered view | False | ["S21", "S22"] | 1 | 11420 | verified | Not benchmarked; correctness alone does not establish net speedup. |
| C5 | aggregate MV | False | ["S21", "S22"] | 1 | 5 | verified | Not benchmarked; correctness alone does not establish net speedup. |


已验证覆盖（含触发查询、候选并集去重）：6/32 条成功数据 SQL。正确性仅针对当前数据库快照；未测性能的候选不能声称已加速。

[完整 build/rewrite 与比较证据](dacomp-034.analysis.json)。

### C2：aggregate MV

Union of grouping keys; decomposable aggregate states; AVG uses SUM and non-NULL COUNT.

原查询 [S9](#s9), [S10](#s10), [S13](#s13), [S20](#s20) → 新增共享状态 C2 → 后续 3 次可复用。该构建点为事后假设，不代表 Agent 当时预知后续。

构建定义：

```sql
SELECT promotion_type AS __g0, state AS __g1, COUNT(*) AS __a0, MIN(create_dt) AS __a1, MAX(create_dt) AS __a2 FROM "attachment_3"  GROUP BY promotion_type, state
```

受益查询 S9 的改写示例：

```sql
SELECT __g0 AS "promotion_type", SUM(__a0) AS cnt FROM temp.reuse_candidate GROUP BY __g0 ORDER BY cnt DESC
```

| 原 SQL | 列名一致 | 结果一致 | 比较方法 |
| --- | --- | --- | --- |
| S9 | True | True | ordered_numeric_tolerance |
| S10 | True | True | ordered_numeric_tolerance |
| S13 | True | True | exact_multiset |
| S20 | True | True | exact_multiset |


验证状态：verified；成本结论：Warm-cache baseline 866.009 ms vs build+reuse 599.216 ms, ratio 1.445; five repetitions, see performance evidence.

### C4：common filtered view

Same single source and complete filter; original filter retained.

原查询 [S21](#s21), [S22](#s22) → 新增共享状态 C4 → 后续 1 次可复用。该构建点为事后假设，不代表 Agent 当时预知后续。

构建定义：

```sql
SELECT * FROM "attachment_3" WHERE NOT promotion_type IS NULL
```

受益查询 S21 的改写示例：

```sql
SELECT validation, COUNT(*) AS cnt FROM temp.reuse_candidate AS attachment_3 WHERE NOT promotion_type IS NULL GROUP BY validation
```

| 原 SQL | 列名一致 | 结果一致 | 比较方法 |
| --- | --- | --- | --- |
| S21 | True | True | exact_multiset |
| S22 | True | True | exact_multiset |


验证状态：verified；成本结论：Not benchmarked; correctness alone does not establish net speedup.

### C5：aggregate MV

Union of grouping keys; decomposable aggregate states; AVG uses SUM and non-NULL COUNT.

原查询 [S21](#s21), [S22](#s22) → 新增共享状态 C5 → 后续 1 次可复用。该构建点为事后假设，不代表 Agent 当时预知后续。

构建定义：

```sql
SELECT validation AS __g0, promotion_type AS __g1, state AS __g2, COUNT(*) AS __a0, SUM(sale_count) AS __a1 FROM "attachment_3" WHERE NOT promotion_type IS NULL GROUP BY validation, promotion_type, state
```

受益查询 S21 的改写示例：

```sql
SELECT __g0 AS "validation", SUM(__a0) AS cnt FROM temp.reuse_candidate GROUP BY __g0
```

| 原 SQL | 列名一致 | 结果一致 | 比较方法 |
| --- | --- | --- | --- |
| S21 | True | True | exact_multiset |
| S22 | True | True | exact_multiset |


验证状态：verified；成本结论：Not benchmarked; correctness alone does not establish net speedup.

[性能证据 C2](dacomp-034.C2.performance.json)：measured。

结果依赖：自动记录 SQL→Python 的接口父调用，以及源码中引用归档文件的消费者；字面值相同不认定因果。模型方向选择需要人工读取消息，尚未做全面因果标注。

[原始报告](../../../runs/dsv4flash-db-first-full-01/dacomp-034/attempt-01/answer.md)；[统一消息](../../../runs/dsv4flash-db-first-full-01/dacomp-034/attempt-01/messages.jsonl)；[原始 OpenCode 事件](../../../runs/dsv4flash-db-first-full-01/dacomp-034/attempt-01/opencode.jsonl)；[SQL 引擎日志](../../../runs/dsv4flash-db-first-full-01/dacomp-034/attempt-01/sql_journal.jsonl)。

[可读报告（本地图片链接规范化）](../answers/dacomp-034.md)。原始回答保留，分析结论未改写。

## S1

类别 `connection_setup`；来源 `connection`；调用 `345a38d88b9045fc966ae055c504b9c5`；状态 `success`。

```sql
PRAGMA query_only=ON
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-034/attempt-01/sql/S1.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-034/attempt-01/sql/S1.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-034/attempt-01/results/S1.rows.jsonl)；完整：True；SHA256：`e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`。

## S2

类别 `metadata`；来源 `list_db`；调用 `345a38d88b9045fc966ae055c504b9c5`；状态 `success`。

```sql
SELECT name,sql FROM sqlite_master WHERE type='table' ORDER BY name
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-034/attempt-01/sql/S2.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-034/attempt-01/sql/S2.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-034/attempt-01/results/S2.rows.jsonl)；完整：True；SHA256：`fa751514b6a9b307e8a587046dd43c08f560e7d9f90f6581f5394e315c1093bb`。

## S3

类别 `data`；来源 `query_db`；调用 `4f293681597347d494e1b385c2dc2091`；状态 `success`。

```sql
SELECT * FROM attachment_1 LIMIT 5
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-034/attempt-01/sql/S3.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-034/attempt-01/sql/S3.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-034/attempt-01/results/S3.rows.jsonl)；完整：True；SHA256：`8a54ade09e995008edd8bf4d8695d59f7505e8fd9ab8b623c60b446318977b7a`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "attachment_1", "kind": "base", "block": null, "base_tables": ["attachment_1"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |


## S4

类别 `data`；来源 `query_db`；调用 `bb6884ae387945fc94c511afbbed868e`；状态 `success`。

```sql
SELECT * FROM attachment_3 LIMIT 5
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-034/attempt-01/sql/S4.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-034/attempt-01/sql/S4.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-034/attempt-01/results/S4.rows.jsonl)；完整：True；SHA256：`63f428648b0c9c7121261946d7bfeeeb9bc459925be96d15fc84fb0d4ee0a207`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "attachment_3", "kind": "base", "block": null, "base_tables": ["attachment_3"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |


## S5

类别 `data`；来源 `query_db`；调用 `293a160fb44549a4a1b0786ddc86ea28`；状态 `success`。

```sql
SELECT * FROM attachment_4 LIMIT 5
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-034/attempt-01/sql/S5.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-034/attempt-01/sql/S5.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-034/attempt-01/results/S5.rows.jsonl)；完整：True；SHA256：`f968c8fe40cbb25959dfa741df84203ee657871f75f1c5d45dc78ed6a6a2b5d9`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "attachment_4", "kind": "base", "block": null, "base_tables": ["attachment_4"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |


## S6

类别 `data`；来源 `query_db`；调用 `0cf7c62937a04bea877e43425ae038de`；状态 `success`。

```sql
SELECT * FROM attachment_3_field_description
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-034/attempt-01/sql/S6.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-034/attempt-01/sql/S6.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-034/attempt-01/results/S6.rows.jsonl)；完整：True；SHA256：`deddbda05b3083345682e0220bd1ed5e8765d47fbdfd5fbb2751fe612d828693`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "attachment_3_field_description", "kind": "base", "block": null, "base_tables": ["attachment_3_field_description"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |


## S7

类别 `data`；来源 `query_db`；调用 `56b27a32352f466688191cac684bdc0d`；状态 `success`。

```sql
SELECT * FROM "attachment_1_&_attachment_2_fie"
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-034/attempt-01/sql/S7.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-034/attempt-01/sql/S7.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-034/attempt-01/results/S7.rows.jsonl)；完整：True；SHA256：`4687ed1e53ac2bf448e87d9f90af9f772ecf9cc2835dd2d3802199941dac9190`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "attachment_1_&_attachment_2_fie", "kind": "base", "block": null, "base_tables": ["\"attachment_1_&_attachment_2_fie\""]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |


## S8

类别 `data`；来源 `query_db`；调用 `ed2219ffc8404ec5920376d4494e1638`；状态 `success`。

```sql
SELECT * FROM attachment_4_field_description
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-034/attempt-01/sql/S8.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-034/attempt-01/sql/S8.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-034/attempt-01/results/S8.rows.jsonl)；完整：True；SHA256：`662206b8bc408b5eb42f17179fe2770c5d137f5d59172a52ceffb9a7b0bbfe99`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "attachment_4_field_description", "kind": "base", "block": null, "base_tables": ["attachment_4_field_description"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |


## S9

类别 `data`；来源 `query_db`；调用 `849b5e4ef59f4ea0aeea01e883243a24`；状态 `success`。

```sql
SELECT promotion_type, COUNT(*) AS cnt FROM attachment_3 GROUP BY promotion_type ORDER BY cnt DESC
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-034/attempt-01/sql/S9.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-034/attempt-01/sql/S9.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-034/attempt-01/results/S9.rows.jsonl)；完整：True；SHA256：`c7a226d19467885e9fe401add65324acd6a15b63b443f5215b59fd22be878efd`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "attachment_3", "kind": "base", "block": null, "base_tables": ["attachment_3"]}] | [] | ["promotion_type"] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |


## S10

类别 `data`；来源 `query_db`；调用 `13898a39198541f0afe8f927208dabb1`；状态 `success`。

```sql
SELECT state, COUNT(*) AS cnt FROM attachment_3 GROUP BY state ORDER BY cnt DESC
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-034/attempt-01/sql/S10.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-034/attempt-01/sql/S10.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-034/attempt-01/results/S10.rows.jsonl)；完整：True；SHA256：`dcc906ff4940941384cc450f5d77ae7c1cdc82fff0813a2f0fd4306d10443e9c`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "attachment_3", "kind": "base", "block": null, "base_tables": ["attachment_3"]}] | [] | ["state"] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |


## S11

类别 `data`；来源 `query_db`；调用 `7a992e4a94a147a1bb40f44164ffed46`；状态 `success`。

```sql
SELECT COUNT(*) AS n FROM attachment_1
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-034/attempt-01/sql/S11.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-034/attempt-01/sql/S11.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-034/attempt-01/results/S11.rows.jsonl)；完整：True；SHA256：`9f43d9124b9f84cd2cf4ef89f6c9505ed2f906239a5ad1b2a3fd45075d7a9dcd`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "attachment_1", "kind": "base", "block": null, "base_tables": ["attachment_1"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |


## S12

类别 `data`；来源 `query_db`；调用 `6c493d45a7a643de8c4a0e1dfe154c90`；状态 `success`。

```sql
SELECT COUNT(*) AS n FROM attachment_2
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-034/attempt-01/sql/S12.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-034/attempt-01/sql/S12.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-034/attempt-01/results/S12.rows.jsonl)；完整：True；SHA256：`a1e02df65f77ed0d776d00386c8005ddd2ecd16357b9da1fa8846deebd903afc`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "attachment_2", "kind": "base", "block": null, "base_tables": ["attachment_2"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |


## S13

类别 `data`；来源 `query_db`；调用 `102fc389176a4684b93ee490a859d495`；状态 `success`。

```sql
SELECT COUNT(*) AS n FROM attachment_3
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-034/attempt-01/sql/S13.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-034/attempt-01/sql/S13.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-034/attempt-01/results/S13.rows.jsonl)；完整：True；SHA256：`c081c1644d9948df33ee32e6b98f0521aa6c4cedf6b0f5386c44716631ffb4b4`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "attachment_3", "kind": "base", "block": null, "base_tables": ["attachment_3"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |


## S14

类别 `data`；来源 `query_db`；调用 `223fcec9581646819ece34b66f7573a5`；状态 `success`。

```sql
SELECT COUNT(*) AS n, COUNT(DISTINCT sku_id) AS skus FROM attachment_4
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-034/attempt-01/sql/S14.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-034/attempt-01/sql/S14.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-034/attempt-01/results/S14.rows.jsonl)；完整：True；SHA256：`aaa14bad9e5ff02f8397bd70c0f8b8f2de90e71d4c4e7b712d186613684c5c81`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "attachment_4", "kind": "base", "block": null, "base_tables": ["attachment_4"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |
| B1 | COUNT(DISTINCT sku_id) | [{"table": "attachment_4", "column": "sku_id"}] | [] | False |


## S15

类别 `data`；来源 `query_db`；调用 `bdff504b12744247ab57713d84fd210b`；状态 `success`。

```sql
SELECT DISTINCT "Level 1 Category Name", "Level 1 Category ID" FROM attachment_4 ORDER BY "Level 1 Category Name"
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-034/attempt-01/sql/S15.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-034/attempt-01/sql/S15.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-034/attempt-01/results/S15.rows.jsonl)；完整：True；SHA256：`1305d457ed6c80978ac33ebb1e1a5626fe702f49a4043da7d48f8f9a670ea7e5`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "attachment_4", "kind": "base", "block": null, "base_tables": ["attachment_4"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |


## S16

类别 `data`；来源 `query_db`；调用 `030024bcb98b4a25b5316a62d627b5b1`；状态 `success`。

```sql
SELECT COUNT(*) AS single_discount_items FROM attachment_1 WHERE "SKU Cost Price" > 0
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-034/attempt-01/sql/S16.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-034/attempt-01/sql/S16.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-034/attempt-01/results/S16.rows.jsonl)；完整：True；SHA256：`4be25c04b605ef73f8ec83e414112a9651bb709cf02985bb2951ad04e22dfd3f`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "attachment_1", "kind": "base", "block": null, "base_tables": ["attachment_1"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |


## S17

类别 `data`；来源 `query_db`；调用 `9a797ba919b84354b3f617c4262bd8bf`；状态 `success`。

```sql
SELECT COUNT(*) AS single_discount_items FROM attachment_2 WHERE "SKU Cost Price" > 0
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-034/attempt-01/sql/S17.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-034/attempt-01/sql/S17.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-034/attempt-01/results/S17.rows.jsonl)；完整：True；SHA256：`a183ad4290632b9904c171435f797f63ca4103221153aea44da0351a9bbe9208`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "attachment_2", "kind": "base", "block": null, "base_tables": ["attachment_2"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |


## S18

类别 `data`；来源 `query_db`；调用 `986e8b27d9fd4ddb8dacdf334d14a98d`；状态 `success`。

```sql
SELECT * FROM attachment_3 WHERE promotion_type = 4 LIMIT 5
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-034/attempt-01/sql/S18.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-034/attempt-01/sql/S18.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-034/attempt-01/results/S18.rows.jsonl)；完整：True；SHA256：`63f428648b0c9c7121261946d7bfeeeb9bc459925be96d15fc84fb0d4ee0a207`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "attachment_3", "kind": "base", "block": null, "base_tables": ["attachment_3"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |


## S19

类别 `data`；来源 `query_db`；调用 `4b67a0df9f734551abde692466c5593d`；状态 `success`。

```sql
SELECT MIN(create_dt) AS mn, MAX(create_dt) AS mx FROM attachment_1
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-034/attempt-01/sql/S19.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-034/attempt-01/sql/S19.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-034/attempt-01/results/S19.rows.jsonl)；完整：True；SHA256：`a28ec9207f4c0f6a3a6687bdd8b16cd7dee6966f078d58d12630dadb99d68565`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "attachment_1", "kind": "base", "block": null, "base_tables": ["attachment_1"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | MIN(create_dt) | [{"table": "attachment_1", "column": "create_dt"}] | [] | False |
| B1 | MAX(create_dt) | [{"table": "attachment_1", "column": "create_dt"}] | [] | False |


## S20

类别 `data`；来源 `query_db`；调用 `0b9518d838764bf9a965ed39f928c108`；状态 `success`。

```sql
SELECT MIN(create_dt) AS mn, MAX(create_dt) AS mx FROM attachment_3
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-034/attempt-01/sql/S20.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-034/attempt-01/sql/S20.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-034/attempt-01/results/S20.rows.jsonl)；完整：True；SHA256：`7957f2e2a26ca351b875503d0d7fa371dfaf4fb5201aa03f2c26a431f3c4a776`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "attachment_3", "kind": "base", "block": null, "base_tables": ["attachment_3"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | MIN(create_dt) | [{"table": "attachment_3", "column": "create_dt"}] | [] | False |
| B1 | MAX(create_dt) | [{"table": "attachment_3", "column": "create_dt"}] | [] | False |


## S21

类别 `data`；来源 `query_db`；调用 `50115c5781554b74bafc9ad27b240e20`；状态 `success`。

```sql
SELECT validation, COUNT(*) AS cnt FROM attachment_3 WHERE promotion_type IS NOT NULL GROUP BY validation
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-034/attempt-01/sql/S21.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-034/attempt-01/sql/S21.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-034/attempt-01/results/S21.rows.jsonl)；完整：True；SHA256：`e4c1605ecaa20aba98d54b7f18ee9cf76588fe288dbddb1b1cc344bf199a02a2`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "attachment_3", "kind": "base", "block": null, "base_tables": ["attachment_3"]}] | [] | ["validation"] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |


## S22

类别 `data`；来源 `query_db`；调用 `c8ca7e1503c64ed08a4b34d109b4026e`；状态 `success`。

```sql
SELECT promotion_type, state, COUNT(*) AS cnt, SUM(sale_count) AS tot_sales FROM attachment_3 WHERE promotion_type IS NOT NULL GROUP BY promotion_type, state
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-034/attempt-01/sql/S22.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-034/attempt-01/sql/S22.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-034/attempt-01/results/S22.rows.jsonl)；完整：True；SHA256：`1ae73aa989678754680c1785cdc90edb799373438972827d040e5b52f4c52239`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "attachment_3", "kind": "base", "block": null, "base_tables": ["attachment_3"]}] | [] | ["promotion_type", "state"] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |
| B1 | SUM(sale_count) | [{"table": "attachment_3", "column": "sale_count"}] | [] | False |


## S23

类别 `data`；来源 `query_db`；调用 `9bd9e1dfac9641e6bae1debcd89a48fb`；状态 `success`。

```sql
SELECT COUNT(DISTINCT sku_id) AS n_skus FROM attachment_3 WHERE promotion_type = 4
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-034/attempt-01/sql/S23.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-034/attempt-01/sql/S23.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-034/attempt-01/results/S23.rows.jsonl)；完整：True；SHA256：`2dc1fb89128facb6509a512b1fc7832952aad16299c3a640479d16869b31a9e8`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "attachment_3", "kind": "base", "block": null, "base_tables": ["attachment_3"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(DISTINCT sku_id) | [{"table": "attachment_3", "column": "sku_id"}] | [] | False |


## S24

类别 `data`；来源 `query_db`；调用 `67c947286317494299378a9632d421fc`；状态 `success`。

```sql
SELECT COUNT(DISTINCT a3.sku_id) AS skus_in_promo,
       COUNT(DISTINCT CASE WHEN a1.sku_id IS NOT NULL THEN a3.sku_id END) AS skus_in_orders
FROM (SELECT DISTINCT sku_id FROM attachment_3 WHERE promotion_type = 4 AND state = 5) a3
LEFT JOIN (SELECT DISTINCT sku_id FROM attachment_1) a1 ON a3.sku_id = a1.sku_id
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-034/attempt-01/sql/S24.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-034/attempt-01/sql/S24.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-034/attempt-01/results/S24.rows.jsonl)；完整：True；SHA256：`33e2ab6c25f63680b07242e123425512e021d16349f38961fdbc63d4bed71f00`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "attachment_3", "kind": "base", "block": null, "base_tables": ["attachment_3"]}] | [] | [] |
| B2 | [{"alias": "attachment_1", "kind": "base", "block": null, "base_tables": ["attachment_1"]}] | [] | [] |
| B3 | [{"alias": "a3", "kind": "derived", "block": "B1", "base_tables": ["attachment_3"]}, {"alias": "a1", "kind": "derived", "block": "B2", "base_tables": ["attachment_1"]}] | [{"type": "LEFT", "right": "(SELECT DISTINCT sku_id FROM attachment_1) AS a1", "on": "a3.sku_id = a1.sku_id", "using": []}] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B3 | COUNT(DISTINCT a3.sku_id) | [{"table": "attachment_3", "column": "sku_id"}] | [] | False |
| B3 | COUNT(DISTINCT CASE WHEN NOT a1.sku_id IS NULL THEN a3.sku_id END) | [{"table": "attachment_3", "column": "sku_id"}] | [{"table": "attachment_1", "column": "sku_id"}] | False |


## S25

类别 `data`；来源 `query_db`；调用 `13c1a6f7b6c34c7d9159eff7f5d22869`；状态 `success`。

```sql
SELECT 
  promotion_type,
  ROUND(AVG(1.0 - promotion_price / pdj_price), 4) AS avg_discount_depth,
  ROUND(SUM(sale_count), 0) AS total_sales,
  COUNT(*) AS n_promos
FROM attachment_3 
WHERE promotion_type IS NOT NULL 
  AND state = 5
  AND pdj_price > 0
  AND promotion_price > 0
GROUP BY promotion_type
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-034/attempt-01/sql/S25.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-034/attempt-01/sql/S25.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-034/attempt-01/results/S25.rows.jsonl)；完整：True；SHA256：`6bd628b0f02894f4ed6956907ab31f49864c981d7e60409ce72efa676403dfc3`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "attachment_3", "kind": "base", "block": null, "base_tables": ["attachment_3"]}] | [] | ["promotion_type"] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |
| B1 | AVG(1.0 - promotion_price / pdj_price) | [{"table": "attachment_3", "column": "promotion_price"}, {"table": "attachment_3", "column": "pdj_price"}] | [] | False |
| B1 | SUM(sale_count) | [{"table": "attachment_3", "column": "sale_count"}] | [] | False |


## S26

类别 `data`；来源 `query_db`；调用 `42fc942dedeb4e56a0bf82fba5e1ecf6`；状态 `success`。

```sql
SELECT 
  MIN(pdj_price) AS min_pdj, 
  MAX(pdj_price) AS max_pdj, 
  MIN(promotion_price) AS min_promo, 
  MAX(promotion_price) AS max_promo,
  MIN(1.0 - promotion_price / pdj_price) AS min_dd,
  MAX(1.0 - promotion_price / pdj_price) AS max_dd,
  AVG(1.0 - promotion_price / pdj_price) AS avg_dd
FROM attachment_3 
WHERE promotion_type = 4 AND state = 5 AND pdj_price > 0
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-034/attempt-01/sql/S26.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-034/attempt-01/sql/S26.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-034/attempt-01/results/S26.rows.jsonl)；完整：True；SHA256：`81c6aa7a0fe1de0a68f0b2731bff18d7248f1a3bd6966f99c8bb121d245380e5`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "attachment_3", "kind": "base", "block": null, "base_tables": ["attachment_3"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | MIN(pdj_price) | [{"table": "attachment_3", "column": "pdj_price"}] | [] | False |
| B1 | MAX(pdj_price) | [{"table": "attachment_3", "column": "pdj_price"}] | [] | False |
| B1 | MIN(promotion_price) | [{"table": "attachment_3", "column": "promotion_price"}] | [] | False |
| B1 | MAX(promotion_price) | [{"table": "attachment_3", "column": "promotion_price"}] | [] | False |
| B1 | MIN(1.0 - promotion_price / pdj_price) | [{"table": "attachment_3", "column": "promotion_price"}, {"table": "attachment_3", "column": "pdj_price"}] | [] | False |
| B1 | MAX(1.0 - promotion_price / pdj_price) | [{"table": "attachment_3", "column": "promotion_price"}, {"table": "attachment_3", "column": "pdj_price"}] | [] | False |
| B1 | AVG(1.0 - promotion_price / pdj_price) | [{"table": "attachment_3", "column": "promotion_price"}, {"table": "attachment_3", "column": "pdj_price"}] | [] | False |


## S27

类别 `data`；来源 `query_db`；调用 `dec3832bf42244d1a53526820d528804`；状态 `success`。

```sql
SELECT 
  a4."Level 1 Category Name" AS cat_name,
  a4."Level 1 Category ID" AS cat_id,
  COUNT(*) AS n_promos,
  SUM(a3.sale_count) AS total_sales,
  ROUND(AVG(1.0 - a3.promotion_price / a3.pdj_price), 4) AS avg_discount_depth,
  ROUND(AVG(a3.sale_count), 2) AS avg_sales_per_promo
FROM attachment_3 a3
JOIN attachment_4 a4 ON a3.sku_id = a4.sku_id
WHERE a3.promotion_type = 4 
  AND a3.state = 5 
  AND a3.pdj_price > 0
  AND a3.promotion_price > 0
GROUP BY a4."Level 1 Category Name"
ORDER BY total_sales DESC
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-034/attempt-01/sql/S27.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-034/attempt-01/sql/S27.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-034/attempt-01/results/S27.rows.jsonl)；完整：True；SHA256：`cd5d0e85141b0197e931eea85e07e7057242d9984095287c9ecbe7405ef7a288`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "a3", "kind": "base", "block": null, "base_tables": ["attachment_3"]}, {"alias": "a4", "kind": "base", "block": null, "base_tables": ["attachment_4"]}] | [{"type": "INNER", "right": "attachment_4 AS a4", "on": "a3.sku_id = a4.sku_id", "using": []}] | ["a4.\"Level 1 Category Name\""] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |
| B1 | SUM(a3.sale_count) | [{"table": "attachment_3", "column": "sale_count"}] | [] | False |
| B1 | AVG(1.0 - a3.promotion_price / a3.pdj_price) | [{"table": "attachment_3", "column": "promotion_price"}, {"table": "attachment_3", "column": "pdj_price"}] | [] | False |
| B1 | AVG(a3.sale_count) | [{"table": "attachment_3", "column": "sale_count"}] | [] | False |


## S28

类别 `data`；来源 `query_db`；调用 `32b0c18f89414539bc55867aacfd9113`；状态 `success`。

```sql
SELECT 
  a4."Level 1 Category Name" AS cat_name,
  a3.sale_count,
  ROUND(1.0 - a3.promotion_price / a3.pdj_price, 4) AS discount_depth,
  a3.promotion_price,
  a3.pdj_price,
  a3.limit_count
FROM attachment_3 a3
JOIN attachment_4 a4 ON a3.sku_id = a4.sku_id
WHERE a3.promotion_type = 4 
  AND a3.state = 5 
  AND a3.pdj_price > 0
  AND a3.promotion_price > 0
  AND a3.sale_count > 0
ORDER BY a4."Level 1 Category Name", a3.id
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-034/attempt-01/sql/S28.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-034/attempt-01/sql/S28.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-034/attempt-01/results/S28.rows.jsonl)；完整：True；SHA256：`2d932c10bdf9222bbc4fc1c63c705667bc063b156682f8738cc69f1dd0606b97`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "a3", "kind": "base", "block": null, "base_tables": ["attachment_3"]}, {"alias": "a4", "kind": "base", "block": null, "base_tables": ["attachment_4"]}] | [{"type": "INNER", "right": "attachment_4 AS a4", "on": "a3.sku_id = a4.sku_id", "using": []}] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |


## S29

类别 `data`；来源 `query_db`；调用 `7bdd21181b914826b44a90e67c50292c`；状态 `success`。

```sql
-- Check if we can find corresponding orders for promotion skus
-- How many promotions have orders in the same time period?
SELECT COUNT(*) AS n_matches
FROM attachment_3 a3
JOIN attachment_1 a1 
  ON a3.sku_id = a1.sku_id
  AND a1.create_dt >= a3.begin_time
  AND a1.create_dt <= a3.end_time
WHERE a3.promotion_type = 4 
  AND a3.state = 5
  AND a3.pdj_price > 0
  AND a3.sale_count > 0
  AND a3.sku_id IN (SELECT DISTINCT sku_id FROM attachment_1)
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-034/attempt-01/sql/S29.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-034/attempt-01/sql/S29.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-034/attempt-01/results/S29.rows.jsonl)；完整：True；SHA256：`cd698eef2cb30b9c123b0a47031d93307b91ee6a6664cc784a79562cad38478a`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "attachment_1", "kind": "base", "block": null, "base_tables": ["attachment_1"]}] | [] | [] |
| B2 | [{"alias": "a3", "kind": "base", "block": null, "base_tables": ["attachment_3"]}, {"alias": "a1", "kind": "base", "block": null, "base_tables": ["attachment_1"]}] | [{"type": "INNER", "right": "attachment_1 AS a1", "on": "a3.sku_id = a1.sku_id AND a1.create_dt >= a3.begin_time AND a1.create_dt <= a3.end_time", "using": []}] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B2 | COUNT(*) | [] | [] | True |


未解析列血缘：[{"block": "B2", "column": "sku_id", "reason": "ambiguous_or_missing_source"}]

## S30

类别 `data`；来源 `query_db`；调用 `61adbb9e09e64a65bc85911714ec8ed9`；状态 `success`。

```sql
-- Check the format of begin_time and create_dt
SELECT a3.begin_time, a3.end_time, a1.create_dt
FROM attachment_3 a3
JOIN attachment_1 a1 ON a3.sku_id = a1.sku_id
WHERE a3.promotion_type = 4 AND a3.state = 5
LIMIT 5
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-034/attempt-01/sql/S30.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-034/attempt-01/sql/S30.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-034/attempt-01/results/S30.rows.jsonl)；完整：True；SHA256：`f968716ade50f4435389958097c790cd9f19e279f38f724058f00256e428a832`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "a3", "kind": "base", "block": null, "base_tables": ["attachment_3"]}, {"alias": "a1", "kind": "base", "block": null, "base_tables": ["attachment_1"]}] | [{"type": "INNER", "right": "attachment_1 AS a1", "on": "a3.sku_id = a1.sku_id", "using": []}] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |


## S31

类别 `data`；来源 `query_db`；调用 `e55d661b6038480198172cf408c8e2bd`；状态 `success`。

```sql
SELECT 
  a4."Level 1 Category Name" AS cat_name,
  a3.sale_count,
  ROUND(1.0 - a3.promotion_price / a3.pdj_price, 4) AS discount_depth,
  a3.promotion_price,
  a3.pdj_price,
  a3.cost_price,
  a3.allowance,
  a3.limit_count
FROM attachment_3 a3
JOIN attachment_4 a4 ON a3.sku_id = a4.sku_id
WHERE a3.promotion_type = 4 
  AND a3.state = 5 
  AND a3.pdj_price > 0
  AND a3.promotion_price > 0
  AND a3.sale_count > 0
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-034/attempt-01/sql/S31.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-034/attempt-01/sql/S31.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-034/attempt-01/results/S31.rows.jsonl)；完整：True；SHA256：`f9f47d2ddde17e588319ea73c45c6dab5385b90abc1d17314a2814ebbe49c5ae`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "a3", "kind": "base", "block": null, "base_tables": ["attachment_3"]}, {"alias": "a4", "kind": "base", "block": null, "base_tables": ["attachment_4"]}] | [{"type": "INNER", "right": "attachment_4 AS a4", "on": "a3.sku_id = a4.sku_id", "using": []}] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |


## S32

类别 `data`；来源 `query_db`；调用 `f8912b9a0a1644aeb635390a2e393715`；状态 `failed`。

```sql
SELECT COUNT(DISTINCT sku_id) AS skus_1, COUNT(DISTINCT sku_id) AS skus_2 FROM attachment_1, attachment_2
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-034/attempt-01/sql/S32.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-034/attempt-01/sql/S32.parameters.json)。

错误：`OperationalError('ambiguous column name: sku_id')`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "attachment_1", "kind": "base", "block": null, "base_tables": ["attachment_1"]}, {"alias": "attachment_2", "kind": "base", "block": null, "base_tables": ["attachment_2"]}] | [{"type": "CROSS", "right": "attachment_2", "on": null, "using": []}] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(DISTINCT sku_id) | [{"unknown": "sku_id"}] | [] | False |
| B1 | COUNT(DISTINCT sku_id) | [{"unknown": "sku_id"}] | [] | False |


未解析列血缘：[{"block": "B1", "column": "sku_id", "reason": "ambiguous_or_missing_source"}, {"block": "B1", "column": "sku_id", "reason": "ambiguous_or_missing_source"}, {"block": "B1", "column": "sku_id", "reason": "ambiguous_or_missing_source"}, {"block": "B1", "column": "sku_id", "reason": "ambiguous_or_missing_source"}]

## S33

类别 `data`；来源 `query_db`；调用 `3fde726f62574848bb37cf53e026428e`；状态 `success`。

```sql
-- Check attachment_1 and attachment_2 data ranges
SELECT MIN(create_dt) AS m1, MAX(create_dt) AS m2 FROM attachment_1
UNION ALL
SELECT MIN(create_dt), MAX(create_dt) FROM attachment_2
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-034/attempt-01/sql/S33.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-034/attempt-01/sql/S33.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-034/attempt-01/results/S33.rows.jsonl)；完整：True；SHA256：`0828093c968b4b994ebb2131c857e338fc3d0a2e2b08705604b794427edad8ce`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "attachment_1", "kind": "base", "block": null, "base_tables": ["attachment_1"]}] | [] | [] |
| B2 | [{"alias": "attachment_2", "kind": "base", "block": null, "base_tables": ["attachment_2"]}] | [] | [] |
| B3 | [] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | MIN(create_dt) | [{"table": "attachment_1", "column": "create_dt"}] | [] | False |
| B1 | MAX(create_dt) | [{"table": "attachment_1", "column": "create_dt"}] | [] | False |
| B2 | MIN(create_dt) | [{"table": "attachment_2", "column": "create_dt"}] | [] | False |
| B2 | MAX(create_dt) | [{"table": "attachment_2", "column": "create_dt"}] | [] | False |


## S34

类别 `data`；来源 `query_db`；调用 `6e4d761f3f0f4beea7a082be762df062`；状态 `success`。

```sql
-- Check if attachment_1 and attachment_2 have overlapping data
SELECT COUNT(*) AS overlap FROM attachment_1 a1
JOIN attachment_2 a2 ON a1."Order ID" = a2."Order ID" AND a1.sku_id = a2.sku_id
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-034/attempt-01/sql/S34.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-034/attempt-01/sql/S34.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-034/attempt-01/results/S34.rows.jsonl)；完整：True；SHA256：`c14196f132c1e9be0508ae80ab52fcb3e1d3fc05880415f3dc980971df207c9e`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "a1", "kind": "base", "block": null, "base_tables": ["attachment_1"]}, {"alias": "a2", "kind": "base", "block": null, "base_tables": ["attachment_2"]}] | [{"type": "INNER", "right": "attachment_2 AS a2", "on": "a1.\"Order ID\" = a2.\"Order ID\" AND a1.sku_id = a2.sku_id", "using": []}] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |


## S35

类别 `data`；来源 `query_db`；调用 `07ded023a5ce47fca7ddee6d476425ec`；状态 `success`。

```sql
-- Check fraction of SKU orders that are at a discount (SKU Cost Price > 0)
SELECT 'attachment_1' AS src,
       COUNT(*) AS total_orders,
       SUM(CASE WHEN "SKU Cost Price" > 0 THEN 1 ELSE 0 END) AS discounted_orders,
       ROUND(100.0 * SUM(CASE WHEN "SKU Cost Price" > 0 THEN 1 ELSE 0 END) / COUNT(*), 1) AS pct_discounted
FROM attachment_1
UNION ALL
SELECT 'attachment_2',
       COUNT(*),
       SUM(CASE WHEN "SKU Cost Price" > 0 THEN 1 ELSE 0 END),
       ROUND(100.0 * SUM(CASE WHEN "SKU Cost Price" > 0 THEN 1 ELSE 0 END) / COUNT(*), 1)
FROM attachment_2
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-034/attempt-01/sql/S35.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-034/attempt-01/sql/S35.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-034/attempt-01/results/S35.rows.jsonl)；完整：True；SHA256：`48d5982cc5ab81c44db8fe59ca0bba8b0cdec466811ab2bd6e1fbeca283c6bb4`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "attachment_1", "kind": "base", "block": null, "base_tables": ["attachment_1"]}] | [] | [] |
| B2 | [{"alias": "attachment_2", "kind": "base", "block": null, "base_tables": ["attachment_2"]}] | [] | [] |
| B3 | [] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |
| B1 | SUM(CASE WHEN "SKU Cost Price" > 0 THEN 1 ELSE 0 END) | [] | [{"table": "attachment_1", "column": "SKU Cost Price"}] | False |
| B1 | COUNT(*) | [] | [] | True |
| B1 | SUM(CASE WHEN "SKU Cost Price" > 0 THEN 1 ELSE 0 END) | [] | [{"table": "attachment_1", "column": "SKU Cost Price"}] | False |
| B2 | COUNT(*) | [] | [] | True |
| B2 | SUM(CASE WHEN "SKU Cost Price" > 0 THEN 1 ELSE 0 END) | [] | [{"table": "attachment_2", "column": "SKU Cost Price"}] | False |
| B2 | COUNT(*) | [] | [] | True |
| B2 | SUM(CASE WHEN "SKU Cost Price" > 0 THEN 1 ELSE 0 END) | [] | [{"table": "attachment_2", "column": "SKU Cost Price"}] | False |

