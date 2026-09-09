# dacomp-002

Please analyze the growth trend of Sales Amount for each Major Category from January to Ap…

运行：已提交。官方未评分。全部 SQL 尝试/成功 28/28；数据 SQL 26/26；Python 8 次。

完整原题：

Please analyze the growth trend of Sales Amount for each Major Category from January to April. How have customers’ purchasing preferences changed? How should product categories and inventory be adjusted for May–August?

| 表 | 行数 | 列数 |
| --- | --- | --- |
| sheet1 | 42816 | 16 |


实际路线（分析者依据 SQL/源码概括，不代表 Agent 自述）：S3：sheet1 查询 → S8：sheet1 分组聚合 → S13：sheet1 分组聚合 → S18：sheet1 分组聚合 → S23：sheet1 分组聚合 → S28：sheet1 分组聚合（等距列出六个结构节点，全部步骤见下表）

数据库大小：9,408,512 字节。

## 数据 SQL

| SQL | 状态 | 基础表 | Join 输入/类型 | GROUP BY | 聚合表达式 | 结果行数 | 数据库 ms |
| --- | --- | --- | --- | --- | --- | --- | --- |
| [S3/Q1](#s3) | success | ["sheet1"] | 0 / {} | [] | ["COUNT(*)", "MIN(\"Sales Date\")", "MAX(\"Sales Date\")", "MIN(\"Sales Month\")", "MAX(\"Sales Month\")"] | 1 | 11.265 |
| [S4/Q2](#s4) | success | ["sheet1"] | 0 / {} | ["\"Major Category Code\"", "\"Major Category Name\""] | ["COUNT(*)", "SUM(\"Sales Amount\")", "SUM(\"Sales Quantity\")"] | 15 | 32.19 |
| [S5/Q3](#s5) | success | ["sheet1"] | 0 / {} | ["\"Major Category Name\""] | ["SUM(\"Sales Amount\")"] | 15 | 20.766 |
| [S6/Q4](#s6) | success | ["sheet1"] | 0 / {} | ["\"Sales Month\""] | ["COUNT(*)", "SUM(\"Sales Amount\")", "SUM(\"Sales Quantity\")"] | 4 | 16.47 |
| [S7/Q5](#s7) | success | ["sheet1"] | 0 / {} | [] | [] | 15 | 15.671 |
| [S8/Q6](#s8) | success | ["sheet1"] | 0 / {} | ["\"Major Category Name\"", "\"Sales Month\""] | ["SUM(\"Sales Quantity\")", "COUNT(*)", "SUM(\"Sales Amount\")"] | 59 | 30.995 |
| [S9/Q7](#s9) | success | ["sheet1"] | 0 / {} | [] | [] | 15 | 16.606 |
| [S10/Q8](#s10) | success | ["sheet1"] | 0 / {} | ["\"Major Category Name\"", "\"Sales Month\""] | ["SUM(\"Sales Quantity\")", "COUNT(*)", "SUM(\"Sales Amount\")"] | 59 | 31.435 |
| [S11/Q9](#s11) | success | ["sheet1"] | 0 / {} | ["\"Is Promotional\""] | ["COUNT(*)", "SUM(\"Sales Amount\")"] | 6 | 18.706 |
| [S12/Q10](#s12) | success | ["sheet1"] | 0 / {} | ["\"Sales Month\"", "\"Is Promotional\""] | ["COUNT(*)", "SUM(\"Sales Amount\")"] | 24 | 33.956 |
| [S13/Q11](#s13) | success | ["sheet1"] | 0 / {} | ["\"Major Category Name\"", "\"Intermediate Category Name\""] | ["SUM(\"Sales Amount\")", "AVG(\"Sales Amount\" * 1.0 / \"Sales Quantity\")"] | 177 | 36.486 |
| [S14/Q12](#s14) | success | ["sheet1"] | 0 / {} | ["\"Major Category Name\"", "\"Sales Month\""] | ["SUM(\"Sales Quantity\")", "COUNT(*)", "SUM(\"Sales Amount\")"] | 59 | 32.181 |
| [S15/Q13](#s15) | success | ["sheet1"] | 0 / {} | ["\"Major Category Name\"", "\"Intermediate Category Name\"", "\"Sales Month\""] | ["SUM(\"Sales Quantity\")", "SUM(\"Sales Amount\")"] | 315 | 47.24 |
| [S16/Q14](#s16) | success | ["sheet1"] | 0 / {} | ["\"Major Category Name\"", "\"Is Promotional\""] | ["COUNT(*)", "SUM(\"Sales Amount\")"] | 59 | 36.326 |
| [S17/Q15](#s17) | success | ["sheet1"] | 0 / {} | ["\"Major Category Name\"", "\"Intermediate Category Name\"", "\"Sales Month\""] | ["SUM(\"Sales Quantity\")", "SUM(\"Sales Amount\")"] | 283 | 13.391 |
| [S18/Q16](#s18) | success | ["sheet1"] | 0 / {} | ["\"Sales Date\""] | ["COUNT(*)", "SUM(\"Sales Amount\")"] | 117 | 14.943 |
| [S19/Q17](#s19) | success | ["sheet1"] | 0 / {} | ["\"Sales Date\""] | ["COUNT(*)", "SUM(\"Sales Amount\")"] | 117 | 15.505 |
| [S20/Q18](#s20) | success | ["sheet1"] | 0 / {} | [] | [] | 10 | 9.616 |
| [S21/Q19](#s21) | success | ["sheet1"] | 0 / {} | ["\"Sales Date\""] | [] | 20 | 9.593 |
| [S22/Q20](#s22) | success | ["sheet1"] | 0 / {} | ["\"Sales Date\""] | ["COUNT(*)"] | 0 | 9.144 |
| [S23/Q21](#s23) | success | ["sheet1"] | 0 / {} | ["\"Sales Date\""] | ["COUNT(*)"] | 0 | 9.1 |
| [S24/Q22](#s24) | success | ["sheet1"] | 0 / {} | ["\"Sales Month\""] | ["MIN(\"Sales Date\")", "MAX(\"Sales Date\")", "COUNT(DISTINCT \"Sales Date\")"] | 4 | 15.958 |
| [S25/Q23](#s25) | success | ["sheet1"] | 0 / {} | [] | ["MIN(\"Sales Date\")", "MAX(\"Sales Date\")"] | 1 | 6.527 |
| [S26/Q24](#s26) | success | ["sheet1"] | 0 / {} | ["\"Sales Date\""] | ["COUNT(*)", "SUM(\"Sales Amount\")"] | 117 | 14.827 |
| [S27/Q25](#s27) | success | ["sheet1"] | 0 / {} | ["\"Major Category Name\"", "\"Sales Month\""] | ["SUM(\"Sales Quantity\")", "SUM(\"Sales Amount\")", "SUM(\"Sales Amount\")", "SUM(\"Sales Quantity\")"] | 58 | 22.245 |
| [S28/Q26](#s28) | success | ["sheet1"] | 0 / {} | ["\"Sales Month\""] | ["COUNT(DISTINCT \"Customer ID\")", "COUNT(*)"] | 4 | 18.994 |


## 元数据和设置

| SQL | 类别 | 状态 | 内容 |
| --- | --- | --- | --- |
| S1 | connection_setup | success | PRAGMA query_only=ON |
| S2 | metadata | success | SELECT name,sql FROM sqlite_master WHERE type='table' ORDER BY name |


## Python 与执行位置

人工源码审查：**database_first_violation**。Python performs category/month groupby sums, ranking and shift-based growth calculations that SQLite GROUP BY and window functions support. Plot rendering is allowed; these preparations violate database_first_v1. Preserve failed Python attempts and the single main session. [证据](../reviews/dacomp-002.json)。

P1：Creating visualizations: (1) line chart of monthly sales amount by major category, (2) category share changes, (3) growth rate heatmap. These are best done with matplotlib/seaborn in Python.

[源码](../../../runs/dsv4flash-db-first-full-01/dacomp-002/attempt-01/python/P1.py)；[输出](../../../runs/dsv4flash-db-first-full-01/dacomp-002/attempt-01/python/P1.stdout)；[错误](../../../runs/dsv4flash-db-first-full-01/dacomp-002/attempt-01/python/P1.stderr)。检出需人工核验的 SQL 可实现操作：groupby(, sort_values(；不能仅凭理由判为合规。

P2：Creating visualizations: line chart of monthly sales amount by major category, market share changes, and growth rate heatmap. Using matplotlib/seaborn in Python as these are visualization tasks not supported by SQL.

[源码](../../../runs/dsv4flash-db-first-full-01/dacomp-002/attempt-01/python/P2.py)；[输出](../../../runs/dsv4flash-db-first-full-01/dacomp-002/attempt-01/python/P2.stdout)；[错误](../../../runs/dsv4flash-db-first-full-01/dacomp-002/attempt-01/python/P2.stderr)。检出需人工核验的 SQL 可实现操作：groupby(, sort_values(；不能仅凭理由判为合规。

P3：Analyzing intermediate category trends to understand what subcategories are driving the changes in major categories. This requires pivot/melt operations that are more natural in pandas.

[源码](../../../runs/dsv4flash-db-first-full-01/dacomp-002/attempt-01/python/P3.py)；[输出](../../../runs/dsv4flash-db-first-full-01/dacomp-002/attempt-01/python/P3.stdout)；[错误](../../../runs/dsv4flash-db-first-full-01/dacomp-002/attempt-01/python/P3.stderr)。检出需人工核验的 SQL 可实现操作：groupby(, sort_values(；不能仅凭理由判为合规。

P4：The previous attempt to read S1.rows.jsonl failed because that file corresponds to the schema listing (empty). I need the promotional-mix data, so I'll pull it via the logged db interface inside Python and analyze it in pandas for visualization.

[源码](../../../runs/dsv4flash-db-first-full-01/dacomp-002/attempt-01/python/P4.py)；[输出](../../../runs/dsv4flash-db-first-full-01/dacomp-002/attempt-01/python/P4.stdout)；[错误](../../../runs/dsv4flash-db-first-full-01/dacomp-002/attempt-01/python/P4.stderr)。检出需人工核验的 SQL 可实现操作：.query(, sort_values(；不能仅凭理由判为合规。

P5：Analyzing intermediate category level trends to understand what subcategories are driving changes in major categories. This data was already queried from S15, but I need to visualize it properly.

[源码](../../../runs/dsv4flash-db-first-full-01/dacomp-002/attempt-01/python/P5.py)；[输出](../../../runs/dsv4flash-db-first-full-01/dacomp-002/attempt-01/python/P5.stdout)；[错误](../../../runs/dsv4flash-db-first-full-01/dacomp-002/attempt-01/python/P5.stderr)。检出需人工核验的 SQL 可实现操作：groupby(, sort_values(；不能仅凭理由判为合规。

P6：Combining intermediate-category data from two SQL queries (S15 and S17) to analyze subcategory trends for all major categories, then saving a summary figure. Pivot/merge operations are more natural in pandas.

[源码](../../../runs/dsv4flash-db-first-full-01/dacomp-002/attempt-01/python/P6.py)；[输出](../../../runs/dsv4flash-db-first-full-01/dacomp-002/attempt-01/python/P6.stdout)；[错误](../../../runs/dsv4flash-db-first-full-01/dacomp-002/attempt-01/python/P6.stderr)。检出需人工核验的 SQL 可实现操作：groupby(, .query(, sort_values(；不能仅凭理由判为合规。

P7：Getting daily sales data to identify seasonal patterns (like Spring Festival). Using SQL for this and parsing dates correctly.

[源码](../../../runs/dsv4flash-db-first-full-01/dacomp-002/attempt-01/python/P7.py)；[输出](../../../runs/dsv4flash-db-first-full-01/dacomp-002/attempt-01/python/P7.stdout)；[错误](../../../runs/dsv4flash-db-first-full-01/dacomp-002/attempt-01/python/P7.stderr)。检出需人工核验的 SQL 可实现操作：.query(；不能仅凭理由判为合规。

P8：Visualizing daily sales data and computing unit price trends. The date parsing issue was due to format; using errors='coerce' to handle it.

[源码](../../../runs/dsv4flash-db-first-full-01/dacomp-002/attempt-01/python/P8.py)；[输出](../../../runs/dsv4flash-db-first-full-01/dacomp-002/attempt-01/python/P8.stdout)；[错误](../../../runs/dsv4flash-db-first-full-01/dacomp-002/attempt-01/python/P8.stderr)。检出需人工核验的 SQL 可实现操作：.query(；不能仅凭理由判为合规。

## 优化机会

已验证候选。筛选限于精确 SQL、相同自包含 CTE、相同单表完整过滤、可分解单表聚合；未覆盖任意 Join 等价和一般谓词蕴含。全部候选都是 offline，未测在线预测。

| 候选 | 类型 | 已有结果 | 覆盖 SQL | 后续次数 | 中间行数 | 验证 | 成本 |
| --- | --- | --- | --- | --- | --- | --- | --- |
| C1 | exact-result reuse | True | ["S7", "S9"] | 1 | unknown | not_verified_cap | Not tested |
| C2 | exact-result reuse | True | ["S8", "S10"] | 1 | 59 | verified | Not benchmarked; correctness alone does not establish net speedup. |
| C3 | exact-result reuse | True | ["S18", "S19", "S26"] | 2 | 117 | verified | Not benchmarked; correctness alone does not establish net speedup. |
| C4 | aggregate MV | False | ["S3", "S4", "S5", "S6", "S8", "S10", "S11", "S12", "S16", "S18", "S19", "S23", "S25", "S26"] | 13 | 3482 | verified | Not benchmarked; correctness alone does not establish net speedup. |
| C5 | common filtered view | False | ["S13", "S27"] | 1 | unknown | not_verified_cap | Not tested |
| C6 | aggregate MV | False | ["S13", "S27"] | 1 | unknown | not_verified_cap | Not tested |


已验证覆盖（含触发查询、候选并集去重）：14/26 条成功数据 SQL。正确性仅针对当前数据库快照；未测性能的候选不能声称已加速。

[完整 build/rewrite 与比较证据](dacomp-002.analysis.json)。

### C4：aggregate MV

Union of grouping keys; decomposable aggregate states; AVG uses SUM and non-NULL COUNT.

原查询 [S3](#s3), [S4](#s4), [S5](#s5), [S6](#s6), [S8](#s8), [S10](#s10), [S11](#s11), [S12](#s12), [S16](#s16), [S18](#s18), [S19](#s19), [S23](#s23), [S25](#s25), [S26](#s26) → 新增共享状态 C4 → 后续 13 次可复用。该构建点为事后假设，不代表 Agent 当时预知后续。

构建定义：

```sql
SELECT "Major Category Code" AS __g0, "Major Category Name" AS __g1, "Sales Month" AS __g2, "Is Promotional" AS __g3, "Sales Date" AS __g4, COUNT(*) AS __a0, MIN("Sales Date") AS __a1, MAX("Sales Date") AS __a2, MIN("Sales Month") AS __a3, MAX("Sales Month") AS __a4, SUM("Sales Amount") AS __a5, SUM("Sales Quantity") AS __a6 FROM "sheet1"  GROUP BY "Major Category Code", "Major Category Name", "Sales Month", "Is Promotional", "Sales Date"
```

受益查询 S3 的改写示例：

```sql
SELECT SUM(__a0) AS n_rows, MIN(__a1) AS min_date, MAX(__a2) AS max_date, MIN(__a3) AS min_month, MAX(__a4) AS max_month FROM temp.reuse_candidate
```

| 原 SQL | 列名一致 | 结果一致 | 比较方法 |
| --- | --- | --- | --- |
| S3 | True | True | exact_multiset |
| S4 | True | True | ordered_numeric_tolerance |
| S5 | True | True | ordered_numeric_tolerance |
| S6 | True | True | ordered_numeric_tolerance |
| S8 | True | True | ordered_numeric_tolerance |
| S10 | True | True | ordered_numeric_tolerance |
| S11 | True | True | exact_multiset |
| S12 | True | True | ordered_numeric_tolerance |
| S16 | True | True | exact_multiset |
| S18 | True | True | ordered_numeric_tolerance |
| S19 | True | True | ordered_numeric_tolerance |
| S23 | True | True | ordered_numeric_tolerance |
| S25 | True | True | exact_multiset |
| S26 | True | True | ordered_numeric_tolerance |


验证状态：verified；成本结论：Not benchmarked; correctness alone does not establish net speedup.

### C3：exact-result reuse

Identical normalized SQL and parameters; archive equality checked.

原查询 [S18](#s18), [S19](#s19), [S26](#s26) → 保留前序结果 S18 → 后续 2 次可复用。该构建点为事后假设，不代表 Agent 当时预知后续。

| 原 SQL | 列名一致 | 结果一致 | 比较方法 |
| --- | --- | --- | --- |
| S19 | True | True | ordered_numeric_tolerance |
| S26 | True | True | ordered_numeric_tolerance |


验证状态：verified；成本结论：Not benchmarked; correctness alone does not establish net speedup.

### C2：exact-result reuse

Identical normalized SQL and parameters; archive equality checked.

原查询 [S8](#s8), [S10](#s10) → 保留前序结果 S8 → 后续 1 次可复用。该构建点为事后假设，不代表 Agent 当时预知后续。

| 原 SQL | 列名一致 | 结果一致 | 比较方法 |
| --- | --- | --- | --- |
| S10 | True | True | ordered_numeric_tolerance |


验证状态：verified；成本结论：Not benchmarked; correctness alone does not establish net speedup.

结果依赖：自动记录 SQL→Python 的接口父调用，以及源码中引用归档文件的消费者；字面值相同不认定因果。模型方向选择需要人工读取消息，尚未做全面因果标注。

[原始报告](../../../runs/dsv4flash-db-first-full-01/dacomp-002/attempt-01/answer.md)；[统一消息](../../../runs/dsv4flash-db-first-full-01/dacomp-002/attempt-01/messages.jsonl)；[原始 OpenCode 事件](../../../runs/dsv4flash-db-first-full-01/dacomp-002/attempt-01/opencode.jsonl)；[SQL 引擎日志](../../../runs/dsv4flash-db-first-full-01/dacomp-002/attempt-01/sql_journal.jsonl)。

[可读报告（本地图片链接规范化）](../answers/dacomp-002.md)。原始回答保留，分析结论未改写。

## S1

类别 `connection_setup`；来源 `connection`；调用 `e7b3f041611147c0a6cd4d0691e1d2a7`；状态 `success`。

```sql
PRAGMA query_only=ON
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-002/attempt-01/sql/S1.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-002/attempt-01/sql/S1.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-002/attempt-01/results/S1.rows.jsonl)；完整：True；SHA256：`e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`。

## S2

类别 `metadata`；来源 `list_db`；调用 `e7b3f041611147c0a6cd4d0691e1d2a7`；状态 `success`。

```sql
SELECT name,sql FROM sqlite_master WHERE type='table' ORDER BY name
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-002/attempt-01/sql/S2.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-002/attempt-01/sql/S2.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-002/attempt-01/results/S2.rows.jsonl)；完整：True；SHA256：`52d2fc94a6aaa4111475f28a39f128c1fde4444a317c3431c5ee7e3aea96b090`。

## S3

类别 `data`；来源 `query_db`；调用 `be6956ed014e4db599294748471dfe26`；状态 `success`。

```sql
SELECT COUNT(*) AS n_rows, MIN("Sales Date") AS min_date, MAX("Sales Date") AS max_date, MIN("Sales Month") AS min_month, MAX("Sales Month") AS max_month FROM sheet1
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-002/attempt-01/sql/S3.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-002/attempt-01/sql/S3.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-002/attempt-01/results/S3.rows.jsonl)；完整：True；SHA256：`8614fe7d1708c688361441fd1f4786c91737a9c554719a893d9002837c8a74a6`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "sheet1", "kind": "base", "block": null, "base_tables": ["sheet1"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |
| B1 | MIN("Sales Date") | [{"table": "sheet1", "column": "Sales Date"}] | [] | False |
| B1 | MAX("Sales Date") | [{"table": "sheet1", "column": "Sales Date"}] | [] | False |
| B1 | MIN("Sales Month") | [{"table": "sheet1", "column": "Sales Month"}] | [] | False |
| B1 | MAX("Sales Month") | [{"table": "sheet1", "column": "Sales Month"}] | [] | False |


## S4

类别 `data`；来源 `query_db`；调用 `d90e448c0b2a4e6981b76c1c47f06be6`；状态 `success`。

```sql
SELECT "Major Category Code", "Major Category Name", COUNT(*) AS n, SUM("Sales Amount") AS total_amount, SUM("Sales Quantity") AS total_qty FROM sheet1 GROUP BY "Major Category Code", "Major Category Name" ORDER BY total_amount DESC
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-002/attempt-01/sql/S4.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-002/attempt-01/sql/S4.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-002/attempt-01/results/S4.rows.jsonl)；完整：True；SHA256：`6b50e3c91ade2a88d9879b7880118c7a1892f9b05161886918620977d836f03f`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "sheet1", "kind": "base", "block": null, "base_tables": ["sheet1"]}] | [] | ["\"Major Category Code\"", "\"Major Category Name\""] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |
| B1 | SUM("Sales Amount") | [{"table": "sheet1", "column": "Sales Amount"}] | [] | False |
| B1 | SUM("Sales Quantity") | [{"table": "sheet1", "column": "Sales Quantity"}] | [] | False |


## S5

类别 `data`；来源 `query_db`；调用 `9f08d7029fcf452aa1a806e35a21fd52`；状态 `success`。

```sql
SELECT "Major Category Name", ROUND(SUM("Sales Amount"),2) AS total_amount FROM sheet1 GROUP BY "Major Category Name" ORDER BY total_amount DESC
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-002/attempt-01/sql/S5.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-002/attempt-01/sql/S5.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-002/attempt-01/results/S5.rows.jsonl)；完整：True；SHA256：`b366871d125842ea34308e2de3c53479fb7f5f69c86091a10172e97dd1058024`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "sheet1", "kind": "base", "block": null, "base_tables": ["sheet1"]}] | [] | ["\"Major Category Name\""] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | SUM("Sales Amount") | [{"table": "sheet1", "column": "Sales Amount"}] | [] | False |


## S6

类别 `data`；来源 `query_db`；调用 `6b572dec585b4f00914f585671f71706`；状态 `success`。

```sql
SELECT "Sales Month", COUNT(*) AS n_rows, ROUND(SUM("Sales Amount"),2) AS total_amount, ROUND(SUM("Sales Quantity"),0) AS total_qty FROM sheet1 GROUP BY "Sales Month" ORDER BY "Sales Month"
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-002/attempt-01/sql/S6.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-002/attempt-01/sql/S6.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-002/attempt-01/results/S6.rows.jsonl)；完整：True；SHA256：`3e56d45da3c908b2c6c56a63a7702fb231ae200b0369b3d8fdf0106739b846d7`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "sheet1", "kind": "base", "block": null, "base_tables": ["sheet1"]}] | [] | ["\"Sales Month\""] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |
| B1 | SUM("Sales Amount") | [{"table": "sheet1", "column": "Sales Amount"}] | [] | False |
| B1 | SUM("Sales Quantity") | [{"table": "sheet1", "column": "Sales Quantity"}] | [] | False |


## S7

类别 `data`；来源 `query_db`；调用 `80e3e933a5c847049aa052ecf7537601`；状态 `success`。

```sql
SELECT DISTINCT "Major Category Name" FROM sheet1 ORDER BY "Major Category Name"
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-002/attempt-01/sql/S7.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-002/attempt-01/sql/S7.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-002/attempt-01/results/S7.rows.jsonl)；完整：True；SHA256：`c1657f8584695839ff133e09ad86156cca1faa36c7c5783fde9b5108af421019`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "sheet1", "kind": "base", "block": null, "base_tables": ["sheet1"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |


## S8

类别 `data`；来源 `query_db`；调用 `244fbe1c13a04363af50f851f910cb01`；状态 `success`。

```sql
SELECT "Major Category Name", "Sales Month", ROUND(SUM("Sales Amount"),2) AS monthly_amount, SUM("Sales Quantity") AS monthly_qty, COUNT(*) AS trans_count FROM sheet1 GROUP BY "Major Category Name", "Sales Month" ORDER BY "Major Category Name", "Sales Month"
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-002/attempt-01/sql/S8.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-002/attempt-01/sql/S8.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-002/attempt-01/results/S8.rows.jsonl)；完整：True；SHA256：`39cd7af00050e8c647c9459c1658d54f58e30feb913418bd512ceadc152a77c1`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "sheet1", "kind": "base", "block": null, "base_tables": ["sheet1"]}] | [] | ["\"Major Category Name\"", "\"Sales Month\""] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | SUM("Sales Quantity") | [{"table": "sheet1", "column": "Sales Quantity"}] | [] | False |
| B1 | COUNT(*) | [] | [] | True |
| B1 | SUM("Sales Amount") | [{"table": "sheet1", "column": "Sales Amount"}] | [] | False |


## S9

类别 `data`；来源 `query_db`；调用 `ae03fdc7682449b2b65b031dfe410df2`；状态 `success`。

```sql
SELECT DISTINCT "Major Category Name" FROM sheet1 ORDER BY "Major Category Name"
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-002/attempt-01/sql/S9.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-002/attempt-01/sql/S9.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-002/attempt-01/results/S9.rows.jsonl)；完整：True；SHA256：`c1657f8584695839ff133e09ad86156cca1faa36c7c5783fde9b5108af421019`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "sheet1", "kind": "base", "block": null, "base_tables": ["sheet1"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |


## S10

类别 `data`；来源 `query_db`；调用 `5c0bf6df2a154caf91c4d640a880eba8`；状态 `success`。

```sql
SELECT "Major Category Name", "Sales Month", ROUND(SUM("Sales Amount"),2) AS monthly_amount, SUM("Sales Quantity") AS monthly_qty, COUNT(*) AS trans_count FROM sheet1 GROUP BY "Major Category Name", "Sales Month" ORDER BY "Major Category Name", "Sales Month"
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-002/attempt-01/sql/S10.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-002/attempt-01/sql/S10.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-002/attempt-01/results/S10.rows.jsonl)；完整：True；SHA256：`39cd7af00050e8c647c9459c1658d54f58e30feb913418bd512ceadc152a77c1`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "sheet1", "kind": "base", "block": null, "base_tables": ["sheet1"]}] | [] | ["\"Major Category Name\"", "\"Sales Month\""] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | SUM("Sales Quantity") | [{"table": "sheet1", "column": "Sales Quantity"}] | [] | False |
| B1 | COUNT(*) | [] | [] | True |
| B1 | SUM("Sales Amount") | [{"table": "sheet1", "column": "Sales Amount"}] | [] | False |


## S11

类别 `data`；来源 `query_db`；调用 `11e1d823946942389b12b0586f44577a`；状态 `success`。

```sql
SELECT "Is Promotional", COUNT(*) AS n, ROUND(SUM("Sales Amount"),2) AS total_amount FROM sheet1 GROUP BY "Is Promotional"
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-002/attempt-01/sql/S11.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-002/attempt-01/sql/S11.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-002/attempt-01/results/S11.rows.jsonl)；完整：True；SHA256：`f3356ffa66e8fce40a1d278b0d47a91c549ab5e2053fc702b6dae767093aba18`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "sheet1", "kind": "base", "block": null, "base_tables": ["sheet1"]}] | [] | ["\"Is Promotional\""] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |
| B1 | SUM("Sales Amount") | [{"table": "sheet1", "column": "Sales Amount"}] | [] | False |


## S12

类别 `data`；来源 `query_db`；调用 `02c6264e7d7d4b7291dca456c7803b8f`；状态 `success`。

```sql
SELECT "Sales Month", "Is Promotional", COUNT(*) AS n, ROUND(SUM("Sales Amount"),2) AS total_amount FROM sheet1 GROUP BY "Sales Month", "Is Promotional" ORDER BY "Sales Month", "Is Promotional"
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-002/attempt-01/sql/S12.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-002/attempt-01/sql/S12.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-002/attempt-01/results/S12.rows.jsonl)；完整：True；SHA256：`132b4fc5daaea40f7d80da9679c108b7b85ca3dd0cd3d73afc060ed09aeadc4c`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "sheet1", "kind": "base", "block": null, "base_tables": ["sheet1"]}] | [] | ["\"Sales Month\"", "\"Is Promotional\""] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |
| B1 | SUM("Sales Amount") | [{"table": "sheet1", "column": "Sales Amount"}] | [] | False |


## S13

类别 `data`；来源 `query_db`；调用 `1c17f679473a48ea9b541c20e89365cb`；状态 `success`。

```sql
SELECT "Major Category Name", "Intermediate Category Name", ROUND(SUM("Sales Amount"),2) AS total_amount, ROUND(AVG("Sales Amount" * 1.0 / "Sales Quantity"),2) AS avg_unit_price FROM sheet1 WHERE "Sales Quantity" > 0 GROUP BY "Major Category Name", "Intermediate Category Name" ORDER BY "Major Category Name", total_amount DESC
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-002/attempt-01/sql/S13.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-002/attempt-01/sql/S13.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-002/attempt-01/results/S13.rows.jsonl)；完整：True；SHA256：`ebf28095a3263f786f5f38da5bc2f1593fcea41b830f3475cd51dce63a1ff578`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "sheet1", "kind": "base", "block": null, "base_tables": ["sheet1"]}] | [] | ["\"Major Category Name\"", "\"Intermediate Category Name\""] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | SUM("Sales Amount") | [{"table": "sheet1", "column": "Sales Amount"}] | [] | False |
| B1 | AVG("Sales Amount" * 1.0 / "Sales Quantity") | [{"table": "sheet1", "column": "Sales Quantity"}, {"table": "sheet1", "column": "Sales Amount"}] | [] | False |


## S14

类别 `data`；来源 `query_db`；调用 `de6992ac519e488bb7ca99eaaab9a6b4`；状态 `success`。

```sql
-- Monthly sales amount and quantity for top 5 major categories with growth rate
WITH monthly AS (
  SELECT 
    "Major Category Name",
    "Sales Month",
    ROUND(SUM("Sales Amount"), 2) AS monthly_amount,
    SUM("Sales Quantity") AS monthly_qty,
    COUNT(*) AS trans_count
  FROM sheet1
  GROUP BY "Major Category Name", "Sales Month"
),
with_growth AS (
  SELECT *,
    LAG(monthly_amount) OVER (PARTITION BY "Major Category Name" ORDER BY "Sales Month") AS prev_amount,
    ROUND((monthly_amount - LAG(monthly_amount) OVER (PARTITION BY "Major Category Name" ORDER BY "Sales Month")) * 100.0 / NULLIF(LAG(monthly_amount) OVER (PARTITION BY "Major Category Name" ORDER BY "Sales Month"), 0), 1) AS growth_pct
  FROM monthly
)
SELECT * FROM with_growth ORDER BY "Major Category Name", "Sales Month"
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-002/attempt-01/sql/S14.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-002/attempt-01/sql/S14.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-002/attempt-01/results/S14.rows.jsonl)；完整：True；SHA256：`0de93790775aebc742871b99513f24c325b879fd9caacb3d1c983cf97893d936`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "sheet1", "kind": "base", "block": null, "base_tables": ["sheet1"]}] | [] | ["\"Major Category Name\"", "\"Sales Month\""] |
| B2 | [{"alias": "monthly", "kind": "derived", "block": "B1", "base_tables": ["sheet1"]}] | [] | [] |
| B3 | [{"alias": "with_growth", "kind": "derived", "block": "B2", "base_tables": ["sheet1"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | SUM("Sales Quantity") | [{"table": "sheet1", "column": "Sales Quantity"}] | [] | False |
| B1 | COUNT(*) | [] | [] | True |
| B1 | SUM("Sales Amount") | [{"table": "sheet1", "column": "Sales Amount"}] | [] | False |


## S15

类别 `data`；来源 `query_db`；调用 `2d540e2dfabe4c6eab13b63cfbef67e4`；状态 `success`。

```sql
-- Monthly breakdown at intermediate category level for top major categories
SELECT "Major Category Name", "Intermediate Category Name", "Sales Month", ROUND(SUM("Sales Amount"),2) AS monthly_amount, SUM("Sales Quantity") AS monthly_qty
FROM sheet1
WHERE "Major Category Name" IN ('Vegetables and fruits','Daily fresh products','Leisure','Grain and oil','Alcoholic beverages','Household & Personal Care')
GROUP BY "Major Category Name", "Intermediate Category Name", "Sales Month"
ORDER BY "Major Category Name", "Intermediate Category Name", "Sales Month"
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-002/attempt-01/sql/S15.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-002/attempt-01/sql/S15.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-002/attempt-01/results/S15.rows.jsonl)；完整：True；SHA256：`098a6535bcac06807e5bf7d67a3ac3e2cfac1390eb63e4b4d73de627dbab1e55`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "sheet1", "kind": "base", "block": null, "base_tables": ["sheet1"]}] | [] | ["\"Major Category Name\"", "\"Intermediate Category Name\"", "\"Sales Month\""] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | SUM("Sales Quantity") | [{"table": "sheet1", "column": "Sales Quantity"}] | [] | False |
| B1 | SUM("Sales Amount") | [{"table": "sheet1", "column": "Sales Amount"}] | [] | False |


## S16

类别 `data`；来源 `python`；调用 `0be6d6a95ec14f2a8a9c2e3b347c2948`；状态 `success`。

```sql

SELECT "Major Category Name", "Is Promotional", ROUND(SUM("Sales Amount"),2) AS total_amount, COUNT(*) AS n
FROM sheet1
GROUP BY "Major Category Name", "Is Promotional"

```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-002/attempt-01/sql/S16.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-002/attempt-01/sql/S16.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-002/attempt-01/results/S16.rows.jsonl)；完整：True；SHA256：`4b2c1468942633c9a4b6206ac6a03abefd49d8e34d483c84081a6f048fff9f71`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "sheet1", "kind": "base", "block": null, "base_tables": ["sheet1"]}] | [] | ["\"Major Category Name\"", "\"Is Promotional\""] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |
| B1 | SUM("Sales Amount") | [{"table": "sheet1", "column": "Sales Amount"}] | [] | False |


## S17

类别 `data`；来源 `query_db`；调用 `d62de81c3f10464ca004d57f1c820eda`；状态 `success`。

```sql
SELECT "Major Category Name", "Intermediate Category Name", "Sales Month", ROUND(SUM("Sales Amount"),2) AS monthly_amount, SUM("Sales Quantity") AS monthly_qty
FROM sheet1
WHERE "Major Category Name" IN ('Meat and poultry', 'Instant mixes', 'Cooked food', 'Aquatic Products', 'Knitwear', 'Stationery and Sports', 'Home appliances', 'Baking', 'Household')
GROUP BY "Major Category Name", "Intermediate Category Name", "Sales Month"
ORDER BY "Major Category Name", "Intermediate Category Name", "Sales Month"
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-002/attempt-01/sql/S17.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-002/attempt-01/sql/S17.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-002/attempt-01/results/S17.rows.jsonl)；完整：True；SHA256：`08698f49d616b8f71a3eb69e90aa4b6cc97a27ef3e62d1bb90c55cdf32fd018a`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "sheet1", "kind": "base", "block": null, "base_tables": ["sheet1"]}] | [] | ["\"Major Category Name\"", "\"Intermediate Category Name\"", "\"Sales Month\""] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | SUM("Sales Quantity") | [{"table": "sheet1", "column": "Sales Quantity"}] | [] | False |
| B1 | SUM("Sales Amount") | [{"table": "sheet1", "column": "Sales Amount"}] | [] | False |


## S18

类别 `data`；来源 `python`；调用 `75f28c76444641d7af63292ae01e2659`；状态 `success`。

```sql

SELECT "Sales Date", ROUND(SUM("Sales Amount"),2) AS total, COUNT(*) AS n
FROM sheet1
GROUP BY "Sales Date" ORDER BY "Sales Date"

```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-002/attempt-01/sql/S18.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-002/attempt-01/sql/S18.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-002/attempt-01/results/S18.rows.jsonl)；完整：True；SHA256：`182af482a8399e005ced2f38883f451d076ef1f087711e954453ced2d15cafeb`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "sheet1", "kind": "base", "block": null, "base_tables": ["sheet1"]}] | [] | ["\"Sales Date\""] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |
| B1 | SUM("Sales Amount") | [{"table": "sheet1", "column": "Sales Amount"}] | [] | False |


## S19

类别 `data`；来源 `python`；调用 `ad1d5b74ac694113b598a4fcd6e30533`；状态 `success`。

```sql

SELECT "Sales Date", ROUND(SUM("Sales Amount"),2) AS total, COUNT(*) AS n
FROM sheet1
GROUP BY "Sales Date" ORDER BY "Sales Date"

```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-002/attempt-01/sql/S19.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-002/attempt-01/sql/S19.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-002/attempt-01/results/S19.rows.jsonl)；完整：True；SHA256：`182af482a8399e005ced2f38883f451d076ef1f087711e954453ced2d15cafeb`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "sheet1", "kind": "base", "block": null, "base_tables": ["sheet1"]}] | [] | ["\"Sales Date\""] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |
| B1 | SUM("Sales Amount") | [{"table": "sheet1", "column": "Sales Amount"}] | [] | False |


## S20

类别 `data`；来源 `query_db`；调用 `48546f49495341cfa2b6f54d4e7260e3`；状态 `success`。

```sql
SELECT DISTINCT "Sales Date" FROM sheet1 ORDER BY "Sales Date" LIMIT 10
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-002/attempt-01/sql/S20.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-002/attempt-01/sql/S20.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-002/attempt-01/results/S20.rows.jsonl)；完整：True；SHA256：`5b73a5640cd321e3a0befc08b426e1505ee7e417d932c534156a601834f90236`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "sheet1", "kind": "base", "block": null, "base_tables": ["sheet1"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |


## S21

类别 `data`；来源 `query_db`；调用 `8f800652cd2f4e99859f4579b4a24550`；状态 `success`。

```sql
SELECT "Sales Date", LENGTH(CAST("Sales Date" AS TEXT)) AS len_date FROM sheet1 GROUP BY "Sales Date" ORDER BY "Sales Date" LIMIT 20
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-002/attempt-01/sql/S21.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-002/attempt-01/sql/S21.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-002/attempt-01/results/S21.rows.jsonl)；完整：True；SHA256：`e1f5b68ed9dd2b955110c88937dd7efa50a6b5bee412300f4f4e5e3337ddc90b`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "sheet1", "kind": "base", "block": null, "base_tables": ["sheet1"]}] | [] | ["\"Sales Date\""] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |


## S22

类别 `data`；来源 `query_db`；调用 `1107637a93e94dc5b445d6e7e1926697`；状态 `success`。

```sql
SELECT "Sales Date", COUNT(*) AS n FROM sheet1 WHERE CAST(SUBSTR(CAST("Sales Date" AS TEXT), 7, 2) AS INTEGER) > 31 GROUP BY "Sales Date" ORDER BY "Sales Date" LIMIT 5
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-002/attempt-01/sql/S22.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-002/attempt-01/sql/S22.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-002/attempt-01/results/S22.rows.jsonl)；完整：True；SHA256：`e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "sheet1", "kind": "base", "block": null, "base_tables": ["sheet1"]}] | [] | ["\"Sales Date\""] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |


## S23

类别 `data`；来源 `query_db`；调用 `153c95160fd84a3aa7fa8395d2b720c6`；状态 `success`。

```sql
SELECT "Sales Date", COUNT(*) AS n FROM sheet1 GROUP BY "Sales Date" HAVING CAST(SUBSTR(CAST("Sales Date" AS TEXT), 7, 2) AS INTEGER) > 31 ORDER BY "Sales Date"
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-002/attempt-01/sql/S23.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-002/attempt-01/sql/S23.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-002/attempt-01/results/S23.rows.jsonl)；完整：True；SHA256：`e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "sheet1", "kind": "base", "block": null, "base_tables": ["sheet1"]}] | [] | ["\"Sales Date\""] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |


## S24

类别 `data`；来源 `query_db`；调用 `a1538b9b704b42a0b8af979987793d74`；状态 `success`。

```sql
SELECT "Sales Month", MIN("Sales Date") AS min_date, MAX("Sales Date") AS max_date, COUNT(DISTINCT "Sales Date") AS n_days FROM sheet1 GROUP BY "Sales Month" ORDER BY "Sales Month"
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-002/attempt-01/sql/S24.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-002/attempt-01/sql/S24.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-002/attempt-01/results/S24.rows.jsonl)；完整：True；SHA256：`82e7605d47ad674c4b3f00854c7e2faa9418b5efac90b589cd0d2db79da56fd6`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "sheet1", "kind": "base", "block": null, "base_tables": ["sheet1"]}] | [] | ["\"Sales Month\""] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | MIN("Sales Date") | [{"table": "sheet1", "column": "Sales Date"}] | [] | False |
| B1 | MAX("Sales Date") | [{"table": "sheet1", "column": "Sales Date"}] | [] | False |
| B1 | COUNT(DISTINCT "Sales Date") | [{"table": "sheet1", "column": "Sales Date"}] | [] | False |


## S25

类别 `data`；来源 `query_db`；调用 `4582335759bb4b92891b7a75ce335d75`；状态 `success`。

```sql
SELECT MIN("Sales Date") AS min_d, MAX("Sales Date") AS max_d FROM sheet1
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-002/attempt-01/sql/S25.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-002/attempt-01/sql/S25.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-002/attempt-01/results/S25.rows.jsonl)；完整：True；SHA256：`1b5fd5140df20c9f5e161a81489021174e4cf508915dc3c25564a29b8f63a4a4`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "sheet1", "kind": "base", "block": null, "base_tables": ["sheet1"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | MIN("Sales Date") | [{"table": "sheet1", "column": "Sales Date"}] | [] | False |
| B1 | MAX("Sales Date") | [{"table": "sheet1", "column": "Sales Date"}] | [] | False |


## S26

类别 `data`；来源 `python`；调用 `8398d087726a4c309f245c7ad394f45e`；状态 `success`。

```sql

SELECT "Sales Date", ROUND(SUM("Sales Amount"),2) AS total, COUNT(*) AS n
FROM sheet1
GROUP BY "Sales Date" ORDER BY "Sales Date"

```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-002/attempt-01/sql/S26.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-002/attempt-01/sql/S26.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-002/attempt-01/results/S26.rows.jsonl)；完整：True；SHA256：`182af482a8399e005ced2f38883f451d076ef1f087711e954453ced2d15cafeb`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "sheet1", "kind": "base", "block": null, "base_tables": ["sheet1"]}] | [] | ["\"Sales Date\""] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |
| B1 | SUM("Sales Amount") | [{"table": "sheet1", "column": "Sales Amount"}] | [] | False |


## S27

类别 `data`；来源 `python`；调用 `8398d087726a4c309f245c7ad394f45e`；状态 `success`。

```sql

SELECT "Major Category Name", "Sales Month", 
       ROUND(SUM("Sales Amount"), 2) AS total_amount,
       SUM("Sales Quantity") AS total_qty,
       ROUND(SUM("Sales Amount") * 1.0 / NULLIF(SUM("Sales Quantity"), 0), 2) AS avg_unit_price
FROM sheet1
WHERE "Sales Quantity" > 0
GROUP BY "Major Category Name", "Sales Month"
ORDER BY "Major Category Name", "Sales Month"

```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-002/attempt-01/sql/S27.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-002/attempt-01/sql/S27.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-002/attempt-01/results/S27.rows.jsonl)；完整：True；SHA256：`751d025a388e1ffcc45657323e2e7ba03c6da5a071e5b8fd6df03f3f0ccd2c73`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "sheet1", "kind": "base", "block": null, "base_tables": ["sheet1"]}] | [] | ["\"Major Category Name\"", "\"Sales Month\""] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | SUM("Sales Quantity") | [{"table": "sheet1", "column": "Sales Quantity"}] | [] | False |
| B1 | SUM("Sales Amount") | [{"table": "sheet1", "column": "Sales Amount"}] | [] | False |
| B1 | SUM("Sales Amount") | [{"table": "sheet1", "column": "Sales Amount"}] | [] | False |
| B1 | SUM("Sales Quantity") | [{"table": "sheet1", "column": "Sales Quantity"}] | [] | False |


## S28

类别 `data`；来源 `python`；调用 `8398d087726a4c309f245c7ad394f45e`；状态 `success`。

```sql

SELECT "Sales Month", COUNT(DISTINCT "Customer ID") AS customer_count, COUNT(*) AS trans_count
FROM sheet1
GROUP BY "Sales Month" ORDER BY "Sales Month"

```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-002/attempt-01/sql/S28.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-002/attempt-01/sql/S28.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-002/attempt-01/results/S28.rows.jsonl)；完整：True；SHA256：`c53e787dc92cdbbd8ad8e6995ec4563a25235d9fb26aad85fe53e28ce1bd2e89`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "sheet1", "kind": "base", "block": null, "base_tables": ["sheet1"]}] | [] | ["\"Sales Month\""] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(DISTINCT "Customer ID") | [{"table": "sheet1", "column": "Customer ID"}] | [] | False |
| B1 | COUNT(*) | [] | [] | True |

