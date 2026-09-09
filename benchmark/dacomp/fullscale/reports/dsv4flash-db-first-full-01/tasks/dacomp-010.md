# dacomp-010

Compare the 2024 seasonal trends in Sales Quantity (units) across agricultural product cat…

运行：已提交。官方未评分。全部 SQL 尝试/成功 33/33；数据 SQL 31/31；Python 4 次。

完整原题：

Compare the 2024 seasonal trends in Sales Quantity (units) across agricultural product categories (Agricultural Product Name), identify the Agricultural Product Name with the highest Sales Quantity (units) for each Season label. Then analyze the performance differences of these products across different Sales Channel(s) and propose how to optimize channel strategies to improve sales effectiveness.

| 表 | 行数 | 列数 |
| --- | --- | --- |
| basic_product_information | 646 | 6 |
| core_transaction_information | 646 | 13 |
| market_and_quality_feedback_inf | 646 | 8 |


实际路线（分析者依据 SQL/源码概括，不代表 Agent 自述）：按产品、季节、渠道汇总销量与销售额 → 提取小麦交易明细做渠道检验 → 汇总促销和季节占比 → 绘图及两两统计比较。

数据库大小：397,312 字节。

## 数据 SQL

| SQL | 状态 | 基础表 | Join 输入/类型 | GROUP BY | 聚合表达式 | 结果行数 | 数据库 ms |
| --- | --- | --- | --- | --- | --- | --- | --- |
| [S3/Q1](#s3) | success | ["basic_product_information"] | 0 / {} | [] | [] | 5 | 0.324 |
| [S4/Q2](#s4) | success | ["core_transaction_information"] | 0 / {} | [] | [] | 5 | 0.341 |
| [S5/Q3](#s5) | success | ["market_and_quality_feedback_inf"] | 0 / {} | [] | [] | 5 | 0.311 |
| [S6/Q4](#s6) | success | ["core_transaction_information"] | 0 / {} | [] | ["MIN(\"Transaction Date\")", "MAX(\"Transaction Date\")", "COUNT(*)"] | 1 | 0.498 |
| [S7/Q5](#s7) | success | ["market_and_quality_feedback_inf"] | 0 / {} | ["\"Season label\""] | ["COUNT(*)"] | 4 | 0.547 |
| [S8/Q6](#s8) | success | ["basic_product_information"] | 0 / {} | ["\"Agricultural Product Name\""] | ["COUNT(*)"] | 5 | 0.507 |
| [S9/Q7](#s9) | success | ["core_transaction_information"] | 0 / {} | ["\"Sales Channel\""] | ["COUNT(*)"] | 4 | 0.547 |
| [S10/Q8](#s10) | success | ["core_transaction_information"] | 0 / {} | ["STRFTIME('%Y', \"Transaction Date\")"] | ["COUNT(*)", "SUM(\"Sales Quantity (units)\")"] | 2 | 0.793 |
| [S11/Q9](#s11) | success | ["core_transaction_information", "market_and_quality_feedback_inf"] | 2 / {'INNER': 1} | ["STRFTIME('%Y', c.\"Transaction Date\")", "f.\"Season label\""] | ["COUNT(*)"] | 8 | 1.785 |
| [S12/Q10](#s12) | success | ["core_transaction_information", "market_and_quality_feedback_inf"] | 2 / {'INNER': 1} | ["f.\"Season label\"", "CASE WHEN STRFTIME('%m', c.\"Transaction Date\") IN ('03', '04', '05') THEN 'Spring' WHEN STRFTIME('%m', c.\"Transaction Date\") IN ('06', '07', '08') THEN 'Summer' WHEN STRFTIME('%m', c.\"Transaction Date\") IN ('09', '10', '11') THEN 'Autumn' ELSE 'Winter' END"] | ["COUNT(*)"] | 4 | 2.002 |
| [S13/Q11](#s13) | success | ["basic_product_information", "core_transaction_information", "market_and_quality_feedback_inf"] | 3 / {'INNER': 2} | ["f.\"Season label\"", "b.\"Agricultural Product Name\""] | ["COUNT(*)", "SUM(c.\"Sales Quantity (units)\")", "SUM(c.\"Total Transaction Amount\")", "AVG(c.\"Unit Price (yuan)\")"] | 20 | 2.021 |
| [S14/Q12](#s14) | success | ["basic_product_information", "core_transaction_information", "market_and_quality_feedback_inf"] | 3 / {'INNER': 2} | ["f.\"Season label\"", "b.\"Agricultural Product Name\""] | ["SUM(c.\"Sales Quantity (units)\")", "COUNT(*)", "SUM(c.\"Total Transaction Amount\")"] | 20 | 2.295 |
| [S15/Q13](#s15) | success | ["basic_product_information", "core_transaction_information", "market_and_quality_feedback_inf"] | 3 / {'INNER': 2} | ["c.\"Sales Channel\""] | ["COUNT(*)", "SUM(c.\"Sales Quantity (units)\")", "SUM(CASE WHEN c.\"Promotion\" <> 'None' THEN 1 ELSE 0 END)", "AVG(c.\"Unit Price (yuan)\")", "AVG(c.\"Total Transaction Amount\")", "AVG(c.\"Payment Terms (days)\")"] | 4 | 1.724 |
| [S16/Q14](#s16) | success | ["basic_product_information", "core_transaction_information", "market_and_quality_feedback_inf"] | 3 / {'INNER': 2} | ["f.\"Season label\"", "c.\"Sales Channel\"", "b.\"Agricultural Product Name\""] | ["SUM(c.\"Sales Quantity (units)\")", "COUNT(*)"] | 77 | 2.158 |
| [S17/Q15](#s17) | success | ["basic_product_information", "core_transaction_information", "market_and_quality_feedback_inf"] | 3 / {'INNER': 2} | ["c.\"Sales Channel\"", "c.\"Buyer Type\""] | ["COUNT(*)", "SUM(c.\"Sales Quantity (units)\")", "AVG(c.\"Unit Price (yuan)\")", "AVG(c.\"Total Transaction Amount\")"] | 11 | 1.732 |
| [S18/Q16](#s18) | success | ["core_transaction_information"] | 0 / {} | ["\"Transaction Status\""] | ["COUNT(*)"] | 2 | 0.528 |
| [S19/Q17](#s19) | success | ["basic_product_information", "core_transaction_information", "market_and_quality_feedback_inf"] | 3 / {'INNER': 2} | ["c.\"Sales Channel\""] | ["AVG(f.\"Customer Satisfaction\" <> 'Satisfied')", "AVG(f.\"Repurchase intention\" IN ('Relatively high', 'High'))"] | 4 | 1.704 |
| [S20/Q18](#s20) | success | ["basic_product_information", "core_transaction_information", "market_and_quality_feedback_inf"] | 3 / {'INNER': 2} | ["c.\"Sales Channel\"", "f.\"Customer Satisfaction\""] | ["COUNT(*)"] | 10 | 1.623 |
| [S21/Q19](#s21) | success | ["basic_product_information", "core_transaction_information", "market_and_quality_feedback_inf"] | 3 / {'INNER': 2} | ["c.\"Sales Channel\"", "f.\"Repurchase intention\""] | ["COUNT(*)"] | 12 | 1.647 |
| [S22/Q20](#s22) | success | ["basic_product_information", "core_transaction_information"] | 2 / {'INNER': 1} | ["c.\"Sales Channel\"", "c.\"Promotion\""] | ["COUNT(*)", "SUM(c.\"Sales Quantity (units)\")"] | 12 | 1.158 |
| [S23/Q21](#s23) | success | ["basic_product_information", "core_transaction_information", "market_and_quality_feedback_inf"] | 3 / {'INNER': 2} | ["b.\"Agricultural Product Name\"", "c.\"Sales Channel\""] | ["COUNT(*)", "SUM(c.\"Sales Quantity (units)\")", "AVG(c.\"Unit Price (yuan)\")", "SUM(c.\"Total Transaction Amount\")", "SUM(c.\"Sales Quantity (units)\")"] | 20 | 2.104 |
| [S24/Q22](#s24) | success | ["basic_product_information", "core_transaction_information", "market_and_quality_feedback_inf"] | 3 / {'INNER': 2} | ["b.\"Agricultural Product Name\"", "c.\"Sales Channel\""] | ["COUNT(*)", "COUNT(*)", "COUNT(*)", "SUM(f.\"Customer Satisfaction\" = 'Very satisfied')", "SUM(f.\"Customer Satisfaction\" = 'Satisfied')", "SUM(f.\"Repurchase intention\" IN ('Very high', 'Relatively high'))"] | 20 | 2.177 |
| [S25/Q23](#s25) | success | ["basic_product_information", "core_transaction_information", "market_and_quality_feedback_inf"] | 3 / {'INNER': 2} | ["f.\"Season label\"", "c.\"Sales Channel\""] | ["COUNT(*)", "SUM(c.\"Sales Quantity (units)\")", "AVG(c.\"Unit Price (yuan)\")", "AVG(c.\"Total Transaction Amount\")"] | 16 | 1.75 |
| [S26/Q24](#s26) | success | ["basic_product_information", "core_transaction_information"] | 2 / {'INNER': 1} | ["c.\"Buyer Type\""] | ["COUNT(*)", "SUM(c.\"Sales Quantity (units)\")", "AVG(c.\"Unit Price (yuan)\")"] | 4 | 1.094 |
| [S27/Q25](#s27) | success | ["basic_product_information", "core_transaction_information", "market_and_quality_feedback_inf"] | 3 / {'INNER': 2} | [] | [] | 51 | 1.678 |
| [S28/Q26](#s28) | success | ["basic_product_information", "core_transaction_information", "market_and_quality_feedback_inf"] | 3 / {'INNER': 2} | ["f.\"Season label\"", "b.\"Agricultural Product Name\""] | ["SUM(c.\"Sales Quantity (units)\")"] | 20 | 1.812 |
| [S29/Q27](#s29) | success | ["basic_product_information", "core_transaction_information", "market_and_quality_feedback_inf"] | 3 / {'INNER': 2} | ["c.\"Sales Channel\"", "f.\"Inventory status\""] | ["COUNT(*)", "AVG(f.\"Market price (CNY/kg)\")"] | 10 | 1.769 |
| [S30/Q28](#s30) | success | ["basic_product_information", "core_transaction_information"] | 2 / {'INNER': 1} | ["c.\"Sales Channel\"", "c.\"Payment Method\""] | ["COUNT(*)", "AVG(c.\"Payment Terms (days)\")"] | 14 | 1.185 |
| [S31/Q29](#s31) | success | ["basic_product_information", "core_transaction_information", "market_and_quality_feedback_inf"] | 3 / {'INNER': 2} | ["c.\"Sales Channel\"", "f.\"Quality inspection results\""] | ["COUNT(*)"] | 7 | 1.601 |
| [S32/Q30](#s32) | success | ["basic_product_information", "core_transaction_information"] | 2 / {'INNER': 1} | [] | [] | 51 | 1.01 |
| [S33/Q31](#s33) | success | ["basic_product_information", "core_transaction_information"] | 2 / {'INNER': 1} | [] | [] | 51 | 0.841 |


## 元数据和设置

| SQL | 类别 | 状态 | 内容 |
| --- | --- | --- | --- |
| S1 | connection_setup | success | PRAGMA query_only=ON |
| S2 | metadata | success | SELECT name,sql FROM sqlite_master WHERE type='table' ORDER BY name |


## Python 与执行位置

人工源码审查：**partial_violation**。SQL prepares joins and product/season aggregates. Python performs Kruskal-Wallis and Mann-Whitney tests, which justify statistical inputs, but P2 also computes channel/promotion count, sum, mean and seasonal share summaries outside SQL. Those portions are SQL-capable; plotting/statistical use alone does not make the entire trajectory compliant. [证据](../reviews/dacomp-010.json)。

P1：Create visualizations for seasonal trends and channel analysis. Using Python for plotting (matplotlib/seaborn) which is not supported by SQLite.

[源码](../../../runs/dsv4flash-db-first-full-01/dacomp-010/attempt-01/python/P1.py)；[输出](../../../runs/dsv4flash-db-first-full-01/dacomp-010/attempt-01/python/P1.stdout)；[错误](../../../runs/dsv4flash-db-first-full-01/dacomp-010/attempt-01/python/P1.stderr)。检出需人工核验的 SQL 可实现操作：sort_values(；不能仅凭理由判为合规。

P2：Run statistical tests (Kruskal-Wallis, Mann-Whitney) on Wheat transaction-level channel differences and compute seasonal concentration percentages; these tests are not supported by SQLite.

[源码](../../../runs/dsv4flash-db-first-full-01/dacomp-010/attempt-01/python/P2.py)；[输出](../../../runs/dsv4flash-db-first-full-01/dacomp-010/attempt-01/python/P2.stdout)；[错误](../../../runs/dsv4flash-db-first-full-01/dacomp-010/attempt-01/python/P2.stderr)。检出需人工核验的 SQL 可实现操作：groupby(, .query(；不能仅凭理由判为合规。

P3：Verify the Mann-Whitney results by examining the actual transaction-level quantity values per channel for Wheat.

[源码](../../../runs/dsv4flash-db-first-full-01/dacomp-010/attempt-01/python/P3.py)；[输出](../../../runs/dsv4flash-db-first-full-01/dacomp-010/attempt-01/python/P3.stdout)；[错误](../../../runs/dsv4flash-db-first-full-01/dacomp-010/attempt-01/python/P3.stderr)。检出需人工核验的 SQL 可实现操作：.query(；不能仅凭理由判为合规。

P4：Verify Mann-Whitney results by examining actual transaction quantity distributions for Wheat per channel.

[源码](../../../runs/dsv4flash-db-first-full-01/dacomp-010/attempt-01/python/P4.py)；[输出](../../../runs/dsv4flash-db-first-full-01/dacomp-010/attempt-01/python/P4.stdout)；[错误](../../../runs/dsv4flash-db-first-full-01/dacomp-010/attempt-01/python/P4.stderr)。检出需人工核验的 SQL 可实现操作：.query(；不能仅凭理由判为合规。

## 优化机会

已验证候选。筛选限于精确 SQL、相同自包含 CTE、相同单表完整过滤、可分解单表聚合；未覆盖任意 Join 等价和一般谓词蕴含。全部候选都是 offline，未测在线预测。

| 候选 | 类型 | 已有结果 | 覆盖 SQL | 后续次数 | 中间行数 | 验证 | 成本 |
| --- | --- | --- | --- | --- | --- | --- | --- |
| C1 | exact-result reuse | True | ["S32", "S33"] | 1 | 51 | verified | Not benchmarked; correctness alone does not establish net speedup. |
| C2 | aggregate MV | False | ["S6", "S9", "S10", "S18"] | 3 | 9 | verified | Not benchmarked; correctness alone does not establish net speedup. |


已验证覆盖（含触发查询、候选并集去重）：6/31 条成功数据 SQL。正确性仅针对当前数据库快照；未测性能的候选不能声称已加速。

[完整 build/rewrite 与比较证据](dacomp-010.analysis.json)。

### C2：aggregate MV

Union of grouping keys; decomposable aggregate states; AVG uses SUM and non-NULL COUNT.

原查询 [S6](#s6), [S9](#s9), [S10](#s10), [S18](#s18) → 新增共享状态 C2 → 后续 3 次可复用。该构建点为事后假设，不代表 Agent 当时预知后续。

构建定义：

```sql
SELECT "Sales Channel" AS __g0, STRFTIME('%Y', "Transaction Date") AS __g1, "Transaction Status" AS __g2, MIN("Transaction Date") AS __a0, MAX("Transaction Date") AS __a1, COUNT(*) AS __a2, SUM("Sales Quantity (units)") AS __a3 FROM "core_transaction_information"  GROUP BY "Sales Channel", STRFTIME('%Y', "Transaction Date"), "Transaction Status"
```

受益查询 S6 的改写示例：

```sql
SELECT MIN(__a0) AS min_date, MAX(__a1) AS max_date, SUM(__a2) AS n FROM temp.reuse_candidate
```

| 原 SQL | 列名一致 | 结果一致 | 比较方法 |
| --- | --- | --- | --- |
| S6 | True | True | exact_multiset |
| S9 | True | True | ordered_numeric_tolerance |
| S10 | True | True | exact_multiset |
| S18 | True | True | exact_multiset |


验证状态：verified；成本结论：Not benchmarked; correctness alone does not establish net speedup.

### C1：exact-result reuse

Identical normalized SQL and parameters; archive equality checked.

原查询 [S32](#s32), [S33](#s33) → 保留前序结果 S32 → 后续 1 次可复用。该构建点为事后假设，不代表 Agent 当时预知后续。

| 原 SQL | 列名一致 | 结果一致 | 比较方法 |
| --- | --- | --- | --- |
| S33 | True | True | ordered_numeric_tolerance |


验证状态：verified；成本结论：Not benchmarked; correctness alone does not establish net speedup.

结果依赖：自动记录 SQL→Python 的接口父调用，以及源码中引用归档文件的消费者；字面值相同不认定因果。模型方向选择需要人工读取消息，尚未做全面因果标注。

[原始报告](../../../runs/dsv4flash-db-first-full-01/dacomp-010/attempt-01/answer.md)；[统一消息](../../../runs/dsv4flash-db-first-full-01/dacomp-010/attempt-01/messages.jsonl)；[原始 OpenCode 事件](../../../runs/dsv4flash-db-first-full-01/dacomp-010/attempt-01/opencode.jsonl)；[SQL 引擎日志](../../../runs/dsv4flash-db-first-full-01/dacomp-010/attempt-01/sql_journal.jsonl)。

[可读报告（本地图片链接规范化）](../answers/dacomp-010.md)。原始回答保留，分析结论未改写。

## S1

类别 `connection_setup`；来源 `connection`；调用 `9ff04217826d4523b2babc77f2e331de`；状态 `success`。

```sql
PRAGMA query_only=ON
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-010/attempt-01/sql/S1.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-010/attempt-01/sql/S1.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-010/attempt-01/results/S1.rows.jsonl)；完整：True；SHA256：`e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`。

## S2

类别 `metadata`；来源 `list_db`；调用 `9ff04217826d4523b2babc77f2e331de`；状态 `success`。

```sql
SELECT name,sql FROM sqlite_master WHERE type='table' ORDER BY name
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-010/attempt-01/sql/S2.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-010/attempt-01/sql/S2.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-010/attempt-01/results/S2.rows.jsonl)；完整：True；SHA256：`ecaf13fd4da7929b4d318fe7925e92d24ba0b155d61a73a7c883040ab1ba0ce0`。

## S3

类别 `data`；来源 `query_db`；调用 `217e51de3e9744e18cc8ebfc7d0fb725`；状态 `success`。

```sql
SELECT * FROM basic_product_information LIMIT 5
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-010/attempt-01/sql/S3.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-010/attempt-01/sql/S3.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-010/attempt-01/results/S3.rows.jsonl)；完整：True；SHA256：`c085acd37aba9c12ef9ac17bc7e23a3ec85402df217c85d67fdeb497f2486c53`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "basic_product_information", "kind": "base", "block": null, "base_tables": ["basic_product_information"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |


## S4

类别 `data`；来源 `query_db`；调用 `9d31151515a548e3bcdd532c3f457d85`；状态 `success`。

```sql
SELECT * FROM core_transaction_information LIMIT 5
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-010/attempt-01/sql/S4.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-010/attempt-01/sql/S4.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-010/attempt-01/results/S4.rows.jsonl)；完整：True；SHA256：`d134e69f7e6de019e1decc38fa93b8f05baeaa2d476a87571efa21995a8a6396`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "core_transaction_information", "kind": "base", "block": null, "base_tables": ["core_transaction_information"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |


## S5

类别 `data`；来源 `query_db`；调用 `b0d33648dad14b6fb861428028daee93`；状态 `success`。

```sql
SELECT * FROM market_and_quality_feedback_inf LIMIT 5
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-010/attempt-01/sql/S5.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-010/attempt-01/sql/S5.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-010/attempt-01/results/S5.rows.jsonl)；完整：True；SHA256：`c22edb6737f66d0a4b7ffe00001462c8ceacb1e56b6c36ffcd123e1508300cb6`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "market_and_quality_feedback_inf", "kind": "base", "block": null, "base_tables": ["market_and_quality_feedback_inf"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |


## S6

类别 `data`；来源 `query_db`；调用 `c45fa89b5f43430db2ee81328143e099`；状态 `success`。

```sql
SELECT MIN("Transaction Date") AS min_date, MAX("Transaction Date") AS max_date, COUNT(*) AS n FROM core_transaction_information
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-010/attempt-01/sql/S6.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-010/attempt-01/sql/S6.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-010/attempt-01/results/S6.rows.jsonl)；完整：True；SHA256：`79f164f4007639d90cd66d4e85666d19c99f5dc9899d2b38754bd5e4ed642b3d`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "core_transaction_information", "kind": "base", "block": null, "base_tables": ["core_transaction_information"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | MIN("Transaction Date") | [{"table": "core_transaction_information", "column": "Transaction Date"}] | [] | False |
| B1 | MAX("Transaction Date") | [{"table": "core_transaction_information", "column": "Transaction Date"}] | [] | False |
| B1 | COUNT(*) | [] | [] | True |


## S7

类别 `data`；来源 `query_db`；调用 `3e5f6b06f0f442a9bc557313a9598422`；状态 `success`。

```sql
SELECT "Season label", COUNT(*) AS n FROM market_and_quality_feedback_inf GROUP BY "Season label" ORDER BY n DESC
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-010/attempt-01/sql/S7.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-010/attempt-01/sql/S7.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-010/attempt-01/results/S7.rows.jsonl)；完整：True；SHA256：`230bb81ed53285b229891fb360964524caa59adaa579aec7d8cc8f6e7840e9ba`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "market_and_quality_feedback_inf", "kind": "base", "block": null, "base_tables": ["market_and_quality_feedback_inf"]}] | [] | ["\"Season label\""] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |


## S8

类别 `data`；来源 `query_db`；调用 `3ccbf31c93324a079deadbe8204ecd0f`；状态 `success`。

```sql
SELECT "Agricultural Product Name", COUNT(*) AS n FROM basic_product_information GROUP BY "Agricultural Product Name" ORDER BY n DESC
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-010/attempt-01/sql/S8.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-010/attempt-01/sql/S8.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-010/attempt-01/results/S8.rows.jsonl)；完整：True；SHA256：`a3bdc1364f86664b2df03d81c59e53f63e4ba29a177fcd4c0c48648f2998e94e`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "basic_product_information", "kind": "base", "block": null, "base_tables": ["basic_product_information"]}] | [] | ["\"Agricultural Product Name\""] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |


## S9

类别 `data`；来源 `query_db`；调用 `4217f3cfa2354b98bd653d162d897b22`；状态 `success`。

```sql
SELECT "Sales Channel", COUNT(*) AS n FROM core_transaction_information GROUP BY "Sales Channel" ORDER BY n DESC
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-010/attempt-01/sql/S9.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-010/attempt-01/sql/S9.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-010/attempt-01/results/S9.rows.jsonl)；完整：True；SHA256：`71332af0d84b940bc7c26a49cd9b582882d575d365426c98e7ef9af56875cd56`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "core_transaction_information", "kind": "base", "block": null, "base_tables": ["core_transaction_information"]}] | [] | ["\"Sales Channel\""] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |


## S10

类别 `data`；来源 `query_db`；调用 `6be9a470c5bc4c9aa6abb106bf5ab7ed`；状态 `success`。

```sql
SELECT strftime('%Y', "Transaction Date") AS yr, COUNT(*) AS n, SUM("Sales Quantity (units)") AS total_qty
FROM core_transaction_information
GROUP BY yr
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-010/attempt-01/sql/S10.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-010/attempt-01/sql/S10.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-010/attempt-01/results/S10.rows.jsonl)；完整：True；SHA256：`b373a78729c460472d495a7360935514e8cd2d6036805002e07e827c8c451cce`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "core_transaction_information", "kind": "base", "block": null, "base_tables": ["core_transaction_information"]}] | [] | ["STRFTIME('%Y', \"Transaction Date\")"] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |
| B1 | SUM("Sales Quantity (units)") | [{"table": "core_transaction_information", "column": "Sales Quantity (units)"}] | [] | False |


## S11

类别 `data`；来源 `query_db`；调用 `c8397e62002e411fb78b7d85f06b4a95`；状态 `success`。

```sql
SELECT strftime('%Y', c."Transaction Date") AS yr, f."Season label", COUNT(*) AS n
FROM core_transaction_information c
JOIN market_and_quality_feedback_inf f ON c."Transaction Number" = f."Transaction Number"
GROUP BY yr, f."Season label"
ORDER BY yr, f."Season label"
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-010/attempt-01/sql/S11.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-010/attempt-01/sql/S11.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-010/attempt-01/results/S11.rows.jsonl)；完整：True；SHA256：`e4d7064470825cbb6a3a648890f19fea353914e4bea0b9a7fe48007a161a88b1`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "c", "kind": "base", "block": null, "base_tables": ["core_transaction_information"]}, {"alias": "f", "kind": "base", "block": null, "base_tables": ["market_and_quality_feedback_inf"]}] | [{"type": "INNER", "right": "market_and_quality_feedback_inf AS f", "on": "c.\"Transaction Number\" = f.\"Transaction Number\"", "using": []}] | ["STRFTIME('%Y', c.\"Transaction Date\")", "f.\"Season label\""] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |


## S12

类别 `data`；来源 `query_db`；调用 `aa75f829aaf94691a76419be7ed4ee1b`；状态 `success`。

```sql
SELECT f."Season label",
  CASE WHEN strftime('%m', c."Transaction Date") IN ('03','04','05') THEN 'Spring'
       WHEN strftime('%m', c."Transaction Date") IN ('06','07','08') THEN 'Summer'
       WHEN strftime('%m', c."Transaction Date") IN ('09','10','11') THEN 'Autumn'
       ELSE 'Winter' END AS date_season,
  COUNT(*) AS n
FROM core_transaction_information c
JOIN market_and_quality_feedback_inf f ON c."Transaction Number" = f."Transaction Number"
WHERE strftime('%Y', c."Transaction Date") = '2024'
GROUP BY f."Season label", date_season
ORDER BY f."Season label", date_season
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-010/attempt-01/sql/S12.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-010/attempt-01/sql/S12.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-010/attempt-01/results/S12.rows.jsonl)；完整：True；SHA256：`d6e8e201ac3f17c034c9ff044d86825d7bd0aee0aa863d1de673b6c869890e28`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "c", "kind": "base", "block": null, "base_tables": ["core_transaction_information"]}, {"alias": "f", "kind": "base", "block": null, "base_tables": ["market_and_quality_feedback_inf"]}] | [{"type": "INNER", "right": "market_and_quality_feedback_inf AS f", "on": "c.\"Transaction Number\" = f.\"Transaction Number\"", "using": []}] | ["f.\"Season label\"", "CASE WHEN STRFTIME('%m', c.\"Transaction Date\") IN ('03', '04', '05') THEN 'Spring' WHEN STRFTIME('%m', c.\"Transaction Date\") IN ('06', '07', '08') THEN 'Summer' WHEN STRFTIME('%m', c.\"Transaction Date\") IN ('09', '10', '11') THEN 'Autumn' ELSE 'Winter' END"] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |


## S13

类别 `data`；来源 `query_db`；调用 `cf28b0874ee3442f9a5deb741207e0f0`；状态 `success`。

```sql
SELECT f."Season label", b."Agricultural Product Name",
       COUNT(*) AS n_trans,
       SUM(c."Sales Quantity (units)") AS total_qty,
       ROUND(AVG(c."Unit Price (yuan)"),2) AS avg_unit_price,
       SUM(c."Total Transaction Amount") AS total_amount
FROM core_transaction_information c
JOIN basic_product_information b ON c."Transaction Number" = b."Transaction Number"
JOIN market_and_quality_feedback_inf f ON c."Transaction Number" = f."Transaction Number"
WHERE strftime('%Y', c."Transaction Date") = '2024'
GROUP BY f."Season label", b."Agricultural Product Name"
ORDER BY f."Season label", total_qty DESC
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-010/attempt-01/sql/S13.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-010/attempt-01/sql/S13.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-010/attempt-01/results/S13.rows.jsonl)；完整：True；SHA256：`14b541bbb08cdfc7e4a8a575e1d2a6726ccf043e412626f119bd660ac709b19a`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "c", "kind": "base", "block": null, "base_tables": ["core_transaction_information"]}, {"alias": "b", "kind": "base", "block": null, "base_tables": ["basic_product_information"]}, {"alias": "f", "kind": "base", "block": null, "base_tables": ["market_and_quality_feedback_inf"]}] | [{"type": "INNER", "right": "basic_product_information AS b", "on": "c.\"Transaction Number\" = b.\"Transaction Number\"", "using": []}, {"type": "INNER", "right": "market_and_quality_feedback_inf AS f", "on": "c.\"Transaction Number\" = f.\"Transaction Number\"", "using": []}] | ["f.\"Season label\"", "b.\"Agricultural Product Name\""] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |
| B1 | SUM(c."Sales Quantity (units)") | [{"table": "core_transaction_information", "column": "Sales Quantity (units)"}] | [] | False |
| B1 | SUM(c."Total Transaction Amount") | [{"table": "core_transaction_information", "column": "Total Transaction Amount"}] | [] | False |
| B1 | AVG(c."Unit Price (yuan)") | [{"table": "core_transaction_information", "column": "Unit Price (yuan)"}] | [] | False |


## S14

类别 `data`；来源 `query_db`；调用 `31f0133055a1456492d4db84a164e4ce`；状态 `success`。

```sql
WITH season_prod AS (
  SELECT f."Season label" AS season, b."Agricultural Product Name" AS product,
         SUM(c."Sales Quantity (units)") AS total_qty,
         COUNT(*) AS n_trans,
         SUM(c."Total Transaction Amount") AS total_amount
  FROM core_transaction_information c
  JOIN basic_product_information b ON c."Transaction Number" = b."Transaction Number"
  JOIN market_and_quality_feedback_inf f ON c."Transaction Number" = f."Transaction Number"
  WHERE strftime('%Y', c."Transaction Date") = '2024'
  GROUP BY f."Season label", b."Agricultural Product Name"
)
SELECT season, product, total_qty, n_trans, total_amount,
       ROW_NUMBER() OVER (PARTITION BY season ORDER BY total_qty DESC) AS rnk
FROM season_prod
ORDER BY season, rnk
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-010/attempt-01/sql/S14.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-010/attempt-01/sql/S14.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-010/attempt-01/results/S14.rows.jsonl)；完整：True；SHA256：`201808ac48814a61b4496ed8e6da18bc2c793a295f10a0dd06acfa6a44e68a1a`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "c", "kind": "base", "block": null, "base_tables": ["core_transaction_information"]}, {"alias": "b", "kind": "base", "block": null, "base_tables": ["basic_product_information"]}, {"alias": "f", "kind": "base", "block": null, "base_tables": ["market_and_quality_feedback_inf"]}] | [{"type": "INNER", "right": "basic_product_information AS b", "on": "c.\"Transaction Number\" = b.\"Transaction Number\"", "using": []}, {"type": "INNER", "right": "market_and_quality_feedback_inf AS f", "on": "c.\"Transaction Number\" = f.\"Transaction Number\"", "using": []}] | ["f.\"Season label\"", "b.\"Agricultural Product Name\""] |
| B2 | [{"alias": "season_prod", "kind": "derived", "block": "B1", "base_tables": ["basic_product_information", "core_transaction_information", "market_and_quality_feedback_inf"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | SUM(c."Sales Quantity (units)") | [{"table": "core_transaction_information", "column": "Sales Quantity (units)"}] | [] | False |
| B1 | COUNT(*) | [] | [] | True |
| B1 | SUM(c."Total Transaction Amount") | [{"table": "core_transaction_information", "column": "Total Transaction Amount"}] | [] | False |


## S15

类别 `data`；来源 `query_db`；调用 `088596ead1cc4877bb7343d8f16e8f10`；状态 `success`。

```sql
SELECT c."Sales Channel",
       COUNT(*) AS n_trans,
       SUM(c."Sales Quantity (units)") AS total_qty,
       ROUND(AVG(c."Unit Price (yuan)"),2) AS avg_price,
       ROUND(AVG(c."Total Transaction Amount"),2) AS avg_amount,
       ROUND(AVG(c."Payment Terms (days)"),2) AS avg_terms,
       SUM(CASE WHEN c."Promotion" <> 'None' THEN 1 ELSE 0 END) AS n_promo
FROM core_transaction_information c
JOIN basic_product_information b ON c."Transaction Number" = b."Transaction Number"
JOIN market_and_quality_feedback_inf f ON c."Transaction Number" = f."Transaction Number"
WHERE strftime('%Y', c."Transaction Date") = '2024' AND b."Agricultural Product Name" = 'Wheat'
GROUP BY c."Sales Channel"
ORDER BY total_qty DESC
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-010/attempt-01/sql/S15.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-010/attempt-01/sql/S15.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-010/attempt-01/results/S15.rows.jsonl)；完整：True；SHA256：`a8c977e91e086336bfc047e0e3f43591f3134fc69d1fcaf7f626186765b021fc`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "c", "kind": "base", "block": null, "base_tables": ["core_transaction_information"]}, {"alias": "b", "kind": "base", "block": null, "base_tables": ["basic_product_information"]}, {"alias": "f", "kind": "base", "block": null, "base_tables": ["market_and_quality_feedback_inf"]}] | [{"type": "INNER", "right": "basic_product_information AS b", "on": "c.\"Transaction Number\" = b.\"Transaction Number\"", "using": []}, {"type": "INNER", "right": "market_and_quality_feedback_inf AS f", "on": "c.\"Transaction Number\" = f.\"Transaction Number\"", "using": []}] | ["c.\"Sales Channel\""] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |
| B1 | SUM(c."Sales Quantity (units)") | [{"table": "core_transaction_information", "column": "Sales Quantity (units)"}] | [] | False |
| B1 | SUM(CASE WHEN c."Promotion" <> 'None' THEN 1 ELSE 0 END) | [] | [{"table": "core_transaction_information", "column": "Promotion"}] | False |
| B1 | AVG(c."Unit Price (yuan)") | [{"table": "core_transaction_information", "column": "Unit Price (yuan)"}] | [] | False |
| B1 | AVG(c."Total Transaction Amount") | [{"table": "core_transaction_information", "column": "Total Transaction Amount"}] | [] | False |
| B1 | AVG(c."Payment Terms (days)") | [{"table": "core_transaction_information", "column": "Payment Terms (days)"}] | [] | False |


## S16

类别 `data`；来源 `query_db`；调用 `3e5126f1a49f4575b2401093f99f1da1`；状态 `success`。

```sql
SELECT f."Season label", c."Sales Channel", b."Agricultural Product Name",
       SUM(c."Sales Quantity (units)") AS total_qty, COUNT(*) AS n_trans
FROM core_transaction_information c
JOIN basic_product_information b ON c."Transaction Number" = b."Transaction Number"
JOIN market_and_quality_feedback_inf f ON c."Transaction Number" = f."Transaction Number"
WHERE strftime('%Y', c."Transaction Date") = '2024'
GROUP BY f."Season label", c."Sales Channel", b."Agricultural Product Name"
ORDER BY f."Season label", c."Sales Channel", total_qty DESC
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-010/attempt-01/sql/S16.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-010/attempt-01/sql/S16.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-010/attempt-01/results/S16.rows.jsonl)；完整：True；SHA256：`57019ff76387d7d18f5779a30d2144d0a1707c6121450c1deeb853a9efc96e95`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "c", "kind": "base", "block": null, "base_tables": ["core_transaction_information"]}, {"alias": "b", "kind": "base", "block": null, "base_tables": ["basic_product_information"]}, {"alias": "f", "kind": "base", "block": null, "base_tables": ["market_and_quality_feedback_inf"]}] | [{"type": "INNER", "right": "basic_product_information AS b", "on": "c.\"Transaction Number\" = b.\"Transaction Number\"", "using": []}, {"type": "INNER", "right": "market_and_quality_feedback_inf AS f", "on": "c.\"Transaction Number\" = f.\"Transaction Number\"", "using": []}] | ["f.\"Season label\"", "c.\"Sales Channel\"", "b.\"Agricultural Product Name\""] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | SUM(c."Sales Quantity (units)") | [{"table": "core_transaction_information", "column": "Sales Quantity (units)"}] | [] | False |
| B1 | COUNT(*) | [] | [] | True |


## S17

类别 `data`；来源 `query_db`；调用 `7190a7d39b1548baa70fb5c1ed9f8c56`；状态 `success`。

```sql
SELECT c."Sales Channel", c."Buyer Type", COUNT(*) AS n_trans,
       SUM(c."Sales Quantity (units)") AS total_qty,
       ROUND(AVG(c."Unit Price (yuan)"),2) AS avg_price,
       ROUND(AVG(c."Total Transaction Amount"),2) AS avg_amount
FROM core_transaction_information c
JOIN basic_product_information b ON c."Transaction Number" = b."Transaction Number"
JOIN market_and_quality_feedback_inf f ON c."Transaction Number" = f."Transaction Number"
WHERE strftime('%Y', c."Transaction Date") = '2024' AND b."Agricultural Product Name" = 'Wheat'
GROUP BY c."Sales Channel", c."Buyer Type"
ORDER BY c."Sales Channel", total_qty DESC
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-010/attempt-01/sql/S17.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-010/attempt-01/sql/S17.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-010/attempt-01/results/S17.rows.jsonl)；完整：True；SHA256：`7c77d741d4e5a3ab4ed9d0f3f259ae7e180d373f970cc18d939df940ccb60d00`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "c", "kind": "base", "block": null, "base_tables": ["core_transaction_information"]}, {"alias": "b", "kind": "base", "block": null, "base_tables": ["basic_product_information"]}, {"alias": "f", "kind": "base", "block": null, "base_tables": ["market_and_quality_feedback_inf"]}] | [{"type": "INNER", "right": "basic_product_information AS b", "on": "c.\"Transaction Number\" = b.\"Transaction Number\"", "using": []}, {"type": "INNER", "right": "market_and_quality_feedback_inf AS f", "on": "c.\"Transaction Number\" = f.\"Transaction Number\"", "using": []}] | ["c.\"Sales Channel\"", "c.\"Buyer Type\""] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |
| B1 | SUM(c."Sales Quantity (units)") | [{"table": "core_transaction_information", "column": "Sales Quantity (units)"}] | [] | False |
| B1 | AVG(c."Unit Price (yuan)") | [{"table": "core_transaction_information", "column": "Unit Price (yuan)"}] | [] | False |
| B1 | AVG(c."Total Transaction Amount") | [{"table": "core_transaction_information", "column": "Total Transaction Amount"}] | [] | False |


## S18

类别 `data`；来源 `query_db`；调用 `20a90846aa644330b3f9833df1c66e05`；状态 `success`。

```sql
SELECT "Transaction Status", COUNT(*) AS n FROM core_transaction_information GROUP BY "Transaction Status"
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-010/attempt-01/sql/S18.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-010/attempt-01/sql/S18.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-010/attempt-01/results/S18.rows.jsonl)；完整：True；SHA256：`01b89e8c8722eb8798cb07a6844e02eeef9e92875dd8df3781de353b6bc66c9b`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "core_transaction_information", "kind": "base", "block": null, "base_tables": ["core_transaction_information"]}] | [] | ["\"Transaction Status\""] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |


## S19

类别 `data`；来源 `query_db`；调用 `a5abb384f41e4d7fa8d74df25454b84c`；状态 `success`。

```sql
SELECT c."Sales Channel",
       ROUND(AVG(f."Customer Satisfaction" <> 'Satisfied'),3) AS sat_rate,
       ROUND(AVG(f."Repurchase intention" IN ('Relatively high','High')),3) AS repurchase_rate
FROM core_transaction_information c
JOIN basic_product_information b ON c."Transaction Number" = b."Transaction Number"
JOIN market_and_quality_feedback_inf f ON c."Transaction Number" = f."Transaction Number"
WHERE strftime('%Y', c."Transaction Date") = '2024' AND b."Agricultural Product Name" = 'Wheat'
GROUP BY c."Sales Channel"
ORDER BY repurchase_rate DESC
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-010/attempt-01/sql/S19.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-010/attempt-01/sql/S19.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-010/attempt-01/results/S19.rows.jsonl)；完整：True；SHA256：`271974c698f15f4d2e30257b0495cb8fd7d764c90f77a3816b28b624ed83a561`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "c", "kind": "base", "block": null, "base_tables": ["core_transaction_information"]}, {"alias": "b", "kind": "base", "block": null, "base_tables": ["basic_product_information"]}, {"alias": "f", "kind": "base", "block": null, "base_tables": ["market_and_quality_feedback_inf"]}] | [{"type": "INNER", "right": "basic_product_information AS b", "on": "c.\"Transaction Number\" = b.\"Transaction Number\"", "using": []}, {"type": "INNER", "right": "market_and_quality_feedback_inf AS f", "on": "c.\"Transaction Number\" = f.\"Transaction Number\"", "using": []}] | ["c.\"Sales Channel\""] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | AVG(f."Customer Satisfaction" <> 'Satisfied') | [{"table": "market_and_quality_feedback_inf", "column": "Customer Satisfaction"}] | [] | False |
| B1 | AVG(f."Repurchase intention" IN ('Relatively high', 'High')) | [{"table": "market_and_quality_feedback_inf", "column": "Repurchase intention"}] | [] | False |


## S20

类别 `data`；来源 `query_db`；调用 `d2d0c31815fe422eb6da1251b3d3ed70`；状态 `success`。

```sql
SELECT c."Sales Channel",
       f."Customer Satisfaction",
       COUNT(*) AS n
FROM core_transaction_information c
JOIN basic_product_information b ON c."Transaction Number" = b."Transaction Number"
JOIN market_and_quality_feedback_inf f ON c."Transaction Number" = f."Transaction Number"
WHERE strftime('%Y', c."Transaction Date") = '2024' AND b."Agricultural Product Name" = 'Wheat'
GROUP BY c."Sales Channel", f."Customer Satisfaction"
ORDER BY c."Sales Channel", f."Customer Satisfaction"
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-010/attempt-01/sql/S20.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-010/attempt-01/sql/S20.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-010/attempt-01/results/S20.rows.jsonl)；完整：True；SHA256：`2ad9030f9d458b8ac3919e4e79f5ec4f8227d0eefb3a8cd529f5d66461517e88`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "c", "kind": "base", "block": null, "base_tables": ["core_transaction_information"]}, {"alias": "b", "kind": "base", "block": null, "base_tables": ["basic_product_information"]}, {"alias": "f", "kind": "base", "block": null, "base_tables": ["market_and_quality_feedback_inf"]}] | [{"type": "INNER", "right": "basic_product_information AS b", "on": "c.\"Transaction Number\" = b.\"Transaction Number\"", "using": []}, {"type": "INNER", "right": "market_and_quality_feedback_inf AS f", "on": "c.\"Transaction Number\" = f.\"Transaction Number\"", "using": []}] | ["c.\"Sales Channel\"", "f.\"Customer Satisfaction\""] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |


## S21

类别 `data`；来源 `query_db`；调用 `eb9b771ba6ce4979b8cb48f2829d125b`；状态 `success`。

```sql
SELECT c."Sales Channel",
       f."Repurchase intention",
       COUNT(*) AS n
FROM core_transaction_information c
JOIN basic_product_information b ON c."Transaction Number" = b."Transaction Number"
JOIN market_and_quality_feedback_inf f ON c."Transaction Number" = f."Transaction Number"
WHERE strftime('%Y', c."Transaction Date") = '2024' AND b."Agricultural Product Name" = 'Wheat'
GROUP BY c."Sales Channel", f."Repurchase intention"
ORDER BY c."Sales Channel", f."Repurchase intention"
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-010/attempt-01/sql/S21.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-010/attempt-01/sql/S21.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-010/attempt-01/results/S21.rows.jsonl)；完整：True；SHA256：`a00df8f7dd78f3bcc4384767c5e92bb0a838edb81f305d7484bcb1435c5e00d2`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "c", "kind": "base", "block": null, "base_tables": ["core_transaction_information"]}, {"alias": "b", "kind": "base", "block": null, "base_tables": ["basic_product_information"]}, {"alias": "f", "kind": "base", "block": null, "base_tables": ["market_and_quality_feedback_inf"]}] | [{"type": "INNER", "right": "basic_product_information AS b", "on": "c.\"Transaction Number\" = b.\"Transaction Number\"", "using": []}, {"type": "INNER", "right": "market_and_quality_feedback_inf AS f", "on": "c.\"Transaction Number\" = f.\"Transaction Number\"", "using": []}] | ["c.\"Sales Channel\"", "f.\"Repurchase intention\""] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |


## S22

类别 `data`；来源 `query_db`；调用 `b3a0b40984d84b759777b48a0000b1b7`；状态 `success`。

```sql
SELECT c."Sales Channel", c."Promotion", COUNT(*) AS n,
       SUM(c."Sales Quantity (units)") AS total_qty
FROM core_transaction_information c
JOIN basic_product_information b ON c."Transaction Number" = b."Transaction Number"
WHERE strftime('%Y', c."Transaction Date") = '2024' AND b."Agricultural Product Name" = 'Wheat'
GROUP BY c."Sales Channel", c."Promotion"
ORDER BY c."Sales Channel", c."Promotion"
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-010/attempt-01/sql/S22.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-010/attempt-01/sql/S22.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-010/attempt-01/results/S22.rows.jsonl)；完整：True；SHA256：`adb44ce17a298b5c4dee0977106e738d6432ec3d03f343f552b5034e6b762bca`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "c", "kind": "base", "block": null, "base_tables": ["core_transaction_information"]}, {"alias": "b", "kind": "base", "block": null, "base_tables": ["basic_product_information"]}] | [{"type": "INNER", "right": "basic_product_information AS b", "on": "c.\"Transaction Number\" = b.\"Transaction Number\"", "using": []}] | ["c.\"Sales Channel\"", "c.\"Promotion\""] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |
| B1 | SUM(c."Sales Quantity (units)") | [{"table": "core_transaction_information", "column": "Sales Quantity (units)"}] | [] | False |


## S23

类别 `data`；来源 `query_db`；调用 `9178e6b9af214fa78693459dd9dad609`；状态 `success`。

```sql
SELECT b."Agricultural Product Name", c."Sales Channel",
       COUNT(*) AS n_trans,
       SUM(c."Sales Quantity (units)") AS total_qty,
       ROUND(AVG(c."Unit Price (yuan)"),2) AS avg_price,
       ROUND(SUM(c."Total Transaction Amount")/NULLIF(SUM(c."Sales Quantity (units)"),0),3) AS revenue_per_unit
FROM core_transaction_information c
JOIN basic_product_information b ON c."Transaction Number" = b."Transaction Number"
JOIN market_and_quality_feedback_inf f ON c."Transaction Number" = f."Transaction Number"
WHERE strftime('%Y', c."Transaction Date") = '2024'
GROUP BY b."Agricultural Product Name", c."Sales Channel"
ORDER BY b."Agricultural Product Name", total_qty DESC
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-010/attempt-01/sql/S23.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-010/attempt-01/sql/S23.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-010/attempt-01/results/S23.rows.jsonl)；完整：True；SHA256：`cbe9c532a1ecb5ce687e3f7576a9ddce0d3154dec57735bbde4268f4013a119c`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "c", "kind": "base", "block": null, "base_tables": ["core_transaction_information"]}, {"alias": "b", "kind": "base", "block": null, "base_tables": ["basic_product_information"]}, {"alias": "f", "kind": "base", "block": null, "base_tables": ["market_and_quality_feedback_inf"]}] | [{"type": "INNER", "right": "basic_product_information AS b", "on": "c.\"Transaction Number\" = b.\"Transaction Number\"", "using": []}, {"type": "INNER", "right": "market_and_quality_feedback_inf AS f", "on": "c.\"Transaction Number\" = f.\"Transaction Number\"", "using": []}] | ["b.\"Agricultural Product Name\"", "c.\"Sales Channel\""] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |
| B1 | SUM(c."Sales Quantity (units)") | [{"table": "core_transaction_information", "column": "Sales Quantity (units)"}] | [] | False |
| B1 | AVG(c."Unit Price (yuan)") | [{"table": "core_transaction_information", "column": "Unit Price (yuan)"}] | [] | False |
| B1 | SUM(c."Total Transaction Amount") | [{"table": "core_transaction_information", "column": "Total Transaction Amount"}] | [] | False |
| B1 | SUM(c."Sales Quantity (units)") | [{"table": "core_transaction_information", "column": "Sales Quantity (units)"}] | [] | False |


## S24

类别 `data`；来源 `query_db`；调用 `f97b0976c86446428f22df860be5dab3`；状态 `success`。

```sql
SELECT b."Agricultural Product Name", c."Sales Channel",
       ROUND(SUM(f."Customer Satisfaction"='Very satisfied')*1.0/COUNT(*),3) AS very_sat_rate,
       ROUND(SUM(f."Customer Satisfaction"='Satisfied')*1.0/COUNT(*),3) AS sat_rate,
       ROUND(SUM(f."Repurchase intention" IN ('Very high','Relatively high'))*1.0/COUNT(*),3) AS repurchase_high
FROM core_transaction_information c
JOIN basic_product_information b ON c."Transaction Number" = b."Transaction Number"
JOIN market_and_quality_feedback_inf f ON c."Transaction Number" = f."Transaction Number"
WHERE strftime('%Y', c."Transaction Date") = '2024'
GROUP BY b."Agricultural Product Name", c."Sales Channel"
ORDER BY b."Agricultural Product Name", repurchase_high DESC
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-010/attempt-01/sql/S24.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-010/attempt-01/sql/S24.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-010/attempt-01/results/S24.rows.jsonl)；完整：True；SHA256：`9eaf5ab41bf66299ff1906fd459329a8372ac52b9aafbece80501f69e27eda64`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "c", "kind": "base", "block": null, "base_tables": ["core_transaction_information"]}, {"alias": "b", "kind": "base", "block": null, "base_tables": ["basic_product_information"]}, {"alias": "f", "kind": "base", "block": null, "base_tables": ["market_and_quality_feedback_inf"]}] | [{"type": "INNER", "right": "basic_product_information AS b", "on": "c.\"Transaction Number\" = b.\"Transaction Number\"", "using": []}, {"type": "INNER", "right": "market_and_quality_feedback_inf AS f", "on": "c.\"Transaction Number\" = f.\"Transaction Number\"", "using": []}] | ["b.\"Agricultural Product Name\"", "c.\"Sales Channel\""] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |
| B1 | COUNT(*) | [] | [] | True |
| B1 | COUNT(*) | [] | [] | True |
| B1 | SUM(f."Customer Satisfaction" = 'Very satisfied') | [{"table": "market_and_quality_feedback_inf", "column": "Customer Satisfaction"}] | [] | False |
| B1 | SUM(f."Customer Satisfaction" = 'Satisfied') | [{"table": "market_and_quality_feedback_inf", "column": "Customer Satisfaction"}] | [] | False |
| B1 | SUM(f."Repurchase intention" IN ('Very high', 'Relatively high')) | [{"table": "market_and_quality_feedback_inf", "column": "Repurchase intention"}] | [] | False |


## S25

类别 `data`；来源 `query_db`；调用 `f434f95a51ca465fa88bf25bcaac8ddc`；状态 `success`。

```sql
SELECT f."Season label", c."Sales Channel",
       COUNT(*) AS n_trans,
       SUM(c."Sales Quantity (units)") AS total_qty,
       ROUND(AVG(c."Unit Price (yuan)"),2) AS avg_price,
       ROUND(AVG(c."Total Transaction Amount"),2) AS avg_amount
FROM core_transaction_information c
JOIN basic_product_information b ON c."Transaction Number" = b."Transaction Number"
JOIN market_and_quality_feedback_inf f ON c."Transaction Number" = f."Transaction Number"
WHERE strftime('%Y', c."Transaction Date") = '2024' AND b."Agricultural Product Name" = 'Wheat'
GROUP BY f."Season label", c."Sales Channel"
ORDER BY f."Season label", total_qty DESC
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-010/attempt-01/sql/S25.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-010/attempt-01/sql/S25.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-010/attempt-01/results/S25.rows.jsonl)；完整：True；SHA256：`7597aba205210724310f165b596e77fdd7c7c4ad0c7e4ee38d4ddc1e540e3e06`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "c", "kind": "base", "block": null, "base_tables": ["core_transaction_information"]}, {"alias": "b", "kind": "base", "block": null, "base_tables": ["basic_product_information"]}, {"alias": "f", "kind": "base", "block": null, "base_tables": ["market_and_quality_feedback_inf"]}] | [{"type": "INNER", "right": "basic_product_information AS b", "on": "c.\"Transaction Number\" = b.\"Transaction Number\"", "using": []}, {"type": "INNER", "right": "market_and_quality_feedback_inf AS f", "on": "c.\"Transaction Number\" = f.\"Transaction Number\"", "using": []}] | ["f.\"Season label\"", "c.\"Sales Channel\""] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |
| B1 | SUM(c."Sales Quantity (units)") | [{"table": "core_transaction_information", "column": "Sales Quantity (units)"}] | [] | False |
| B1 | AVG(c."Unit Price (yuan)") | [{"table": "core_transaction_information", "column": "Unit Price (yuan)"}] | [] | False |
| B1 | AVG(c."Total Transaction Amount") | [{"table": "core_transaction_information", "column": "Total Transaction Amount"}] | [] | False |


## S26

类别 `data`；来源 `query_db`；调用 `69b31056dd524aa3ad00849e95475631`；状态 `success`。

```sql
SELECT c."Buyer Type", COUNT(*) AS n_trans,
       SUM(c."Sales Quantity (units)") AS total_qty,
       ROUND(AVG(c."Unit Price (yuan)"),2) AS avg_price
FROM core_transaction_information c
JOIN basic_product_information b ON c."Transaction Number" = b."Transaction Number"
WHERE strftime('%Y', c."Transaction Date") = '2024' AND b."Agricultural Product Name" = 'Wheat'
GROUP BY c."Buyer Type"
ORDER BY total_qty DESC
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-010/attempt-01/sql/S26.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-010/attempt-01/sql/S26.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-010/attempt-01/results/S26.rows.jsonl)；完整：True；SHA256：`3e053dc810084765bbaca89f29b8912777ae92f0fd4bb397278dcd3cc6c4954e`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "c", "kind": "base", "block": null, "base_tables": ["core_transaction_information"]}, {"alias": "b", "kind": "base", "block": null, "base_tables": ["basic_product_information"]}] | [{"type": "INNER", "right": "basic_product_information AS b", "on": "c.\"Transaction Number\" = b.\"Transaction Number\"", "using": []}] | ["c.\"Buyer Type\""] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |
| B1 | SUM(c."Sales Quantity (units)") | [{"table": "core_transaction_information", "column": "Sales Quantity (units)"}] | [] | False |
| B1 | AVG(c."Unit Price (yuan)") | [{"table": "core_transaction_information", "column": "Unit Price (yuan)"}] | [] | False |


## S27

类别 `data`；来源 `python`；调用 `bde55b42201b483398b09486319e011c`；状态 `success`。

```sql

SELECT c."Sales Channel" AS channel,
       c."Sales Quantity (units)" AS qty,
       c."Unit Price (yuan)" AS price,
       c."Total Transaction Amount" AS amount,
       c."Buyer Type" AS buyer,
       c."Promotion" AS promo,
       f."Customer Satisfaction" AS sat,
       f."Repurchase intention" AS repur
FROM core_transaction_information c
JOIN basic_product_information b ON c."Transaction Number" = b."Transaction Number"
JOIN market_and_quality_feedback_inf f ON c."Transaction Number" = f."Transaction Number"
WHERE strftime('%Y', c."Transaction Date") = '2024'
  AND b."Agricultural Product Name" = 'Wheat'
  AND c."Transaction Status" = 'Completed'

```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-010/attempt-01/sql/S27.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-010/attempt-01/sql/S27.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-010/attempt-01/results/S27.rows.jsonl)；完整：True；SHA256：`43bfc02e876885e632cc0fcbce1f5a233e86d6d21d0b566d30cf8bb719ebaa00`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "c", "kind": "base", "block": null, "base_tables": ["core_transaction_information"]}, {"alias": "b", "kind": "base", "block": null, "base_tables": ["basic_product_information"]}, {"alias": "f", "kind": "base", "block": null, "base_tables": ["market_and_quality_feedback_inf"]}] | [{"type": "INNER", "right": "basic_product_information AS b", "on": "c.\"Transaction Number\" = b.\"Transaction Number\"", "using": []}, {"type": "INNER", "right": "market_and_quality_feedback_inf AS f", "on": "c.\"Transaction Number\" = f.\"Transaction Number\"", "using": []}] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |


## S28

类别 `data`；来源 `python`；调用 `bde55b42201b483398b09486319e011c`；状态 `success`。

```sql

SELECT f."Season label" AS season, b."Agricultural Product Name" AS product,
       SUM(c."Sales Quantity (units)") AS total_qty
FROM core_transaction_information c
JOIN basic_product_information b ON c."Transaction Number" = b."Transaction Number"
JOIN market_and_quality_feedback_inf f ON c."Transaction Number" = f."Transaction Number"
WHERE strftime('%Y', c."Transaction Date") = '2024'
GROUP BY f."Season label", b."Agricultural Product Name"

```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-010/attempt-01/sql/S28.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-010/attempt-01/sql/S28.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-010/attempt-01/results/S28.rows.jsonl)；完整：True；SHA256：`f50484512c1c44f17d72078660088187ed7ef45b7c9b6aea202970fefc1c098c`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "c", "kind": "base", "block": null, "base_tables": ["core_transaction_information"]}, {"alias": "b", "kind": "base", "block": null, "base_tables": ["basic_product_information"]}, {"alias": "f", "kind": "base", "block": null, "base_tables": ["market_and_quality_feedback_inf"]}] | [{"type": "INNER", "right": "basic_product_information AS b", "on": "c.\"Transaction Number\" = b.\"Transaction Number\"", "using": []}, {"type": "INNER", "right": "market_and_quality_feedback_inf AS f", "on": "c.\"Transaction Number\" = f.\"Transaction Number\"", "using": []}] | ["f.\"Season label\"", "b.\"Agricultural Product Name\""] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | SUM(c."Sales Quantity (units)") | [{"table": "core_transaction_information", "column": "Sales Quantity (units)"}] | [] | False |


## S29

类别 `data`；来源 `query_db`；调用 `7b31cf9d7b7e48dbac15ff07bac2f7d4`；状态 `success`。

```sql
SELECT c."Sales Channel",
       ROUND(AVG(f."Market price (CNY/kg)"),2) AS avg_market_price,
       f."Inventory status",
       COUNT(*) AS n
FROM core_transaction_information c
JOIN basic_product_information b ON c."Transaction Number" = b."Transaction Number"
JOIN market_and_quality_feedback_inf f ON c."Transaction Number" = f."Transaction Number"
WHERE strftime('%Y', c."Transaction Date") = '2024' AND b."Agricultural Product Name" = 'Wheat'
GROUP BY c."Sales Channel", f."Inventory status"
ORDER BY c."Sales Channel", n DESC
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-010/attempt-01/sql/S29.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-010/attempt-01/sql/S29.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-010/attempt-01/results/S29.rows.jsonl)；完整：True；SHA256：`a9a4824c8cb462b837b69bf9745b705e7df3465d6d59bb7f882665e2cf3b41e2`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "c", "kind": "base", "block": null, "base_tables": ["core_transaction_information"]}, {"alias": "b", "kind": "base", "block": null, "base_tables": ["basic_product_information"]}, {"alias": "f", "kind": "base", "block": null, "base_tables": ["market_and_quality_feedback_inf"]}] | [{"type": "INNER", "right": "basic_product_information AS b", "on": "c.\"Transaction Number\" = b.\"Transaction Number\"", "using": []}, {"type": "INNER", "right": "market_and_quality_feedback_inf AS f", "on": "c.\"Transaction Number\" = f.\"Transaction Number\"", "using": []}] | ["c.\"Sales Channel\"", "f.\"Inventory status\""] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |
| B1 | AVG(f."Market price (CNY/kg)") | [{"table": "market_and_quality_feedback_inf", "column": "Market price (CNY/kg)"}] | [] | False |


## S30

类别 `data`；来源 `query_db`；调用 `bc93f9f40b7c443aa3f7342bb78eb448`；状态 `success`。

```sql
SELECT c."Sales Channel", c."Payment Method",
       COUNT(*) AS n,
       ROUND(AVG(c."Payment Terms (days)"),1) AS avg_terms
FROM core_transaction_information c
JOIN basic_product_information b ON c."Transaction Number" = b."Transaction Number"
WHERE strftime('%Y', c."Transaction Date") = '2024' AND b."Agricultural Product Name" = 'Wheat'
GROUP BY c."Sales Channel", c."Payment Method"
ORDER BY c."Sales Channel", n DESC
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-010/attempt-01/sql/S30.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-010/attempt-01/sql/S30.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-010/attempt-01/results/S30.rows.jsonl)；完整：True；SHA256：`d56d6922ee8f0de361dca349fe53eaa931c4cbac27938069f4b6780186ad5573`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "c", "kind": "base", "block": null, "base_tables": ["core_transaction_information"]}, {"alias": "b", "kind": "base", "block": null, "base_tables": ["basic_product_information"]}] | [{"type": "INNER", "right": "basic_product_information AS b", "on": "c.\"Transaction Number\" = b.\"Transaction Number\"", "using": []}] | ["c.\"Sales Channel\"", "c.\"Payment Method\""] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |
| B1 | AVG(c."Payment Terms (days)") | [{"table": "core_transaction_information", "column": "Payment Terms (days)"}] | [] | False |


## S31

类别 `data`；来源 `query_db`；调用 `9237ceacbb44414483edd1eefec7d5fe`；状态 `success`。

```sql
SELECT c."Sales Channel", f."Quality inspection results",
       COUNT(*) AS n
FROM core_transaction_information c
JOIN basic_product_information b ON c."Transaction Number" = b."Transaction Number"
JOIN market_and_quality_feedback_inf f ON c."Transaction Number" = f."Transaction Number"
WHERE strftime('%Y', c."Transaction Date") = '2024' AND b."Agricultural Product Name" = 'Wheat'
GROUP BY c."Sales Channel", f."Quality inspection results"
ORDER BY c."Sales Channel", n DESC
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-010/attempt-01/sql/S31.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-010/attempt-01/sql/S31.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-010/attempt-01/results/S31.rows.jsonl)；完整：True；SHA256：`0d2b56b93f65e224fdb31d5831fadd4768559c492e7873a1ec07d09dc6ac2473`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "c", "kind": "base", "block": null, "base_tables": ["core_transaction_information"]}, {"alias": "b", "kind": "base", "block": null, "base_tables": ["basic_product_information"]}, {"alias": "f", "kind": "base", "block": null, "base_tables": ["market_and_quality_feedback_inf"]}] | [{"type": "INNER", "right": "basic_product_information AS b", "on": "c.\"Transaction Number\" = b.\"Transaction Number\"", "using": []}, {"type": "INNER", "right": "market_and_quality_feedback_inf AS f", "on": "c.\"Transaction Number\" = f.\"Transaction Number\"", "using": []}] | ["c.\"Sales Channel\"", "f.\"Quality inspection results\""] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |


## S32

类别 `data`；来源 `python`；调用 `e34ec6a82ace413fb01d005f6bb7a07e`；状态 `success`。

```sql

SELECT c."Sales Channel" AS channel,
       c."Sales Quantity (units)" AS qty
FROM core_transaction_information c
JOIN basic_product_information b ON c."Transaction Number" = b."Transaction Number"
WHERE strftime('%Y', c."Transaction Date") = '2024'
  AND b."Agricultural Product Name" = 'Wheat'
  AND c."Transaction Status" = 'Completed'
ORDER BY c."Sales Channel", qty

```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-010/attempt-01/sql/S32.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-010/attempt-01/sql/S32.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-010/attempt-01/results/S32.rows.jsonl)；完整：True；SHA256：`11e7836a6a635a34e8921ddaf3def61fa6a2c977804de0a3227bb2dc54fd6b36`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "c", "kind": "base", "block": null, "base_tables": ["core_transaction_information"]}, {"alias": "b", "kind": "base", "block": null, "base_tables": ["basic_product_information"]}] | [{"type": "INNER", "right": "basic_product_information AS b", "on": "c.\"Transaction Number\" = b.\"Transaction Number\"", "using": []}] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |


## S33

类别 `data`；来源 `python`；调用 `89d684953ea343459614d3a31dcef3df`；状态 `success`。

```sql

SELECT c."Sales Channel" AS channel,
       c."Sales Quantity (units)" AS qty
FROM core_transaction_information c
JOIN basic_product_information b ON c."Transaction Number" = b."Transaction Number"
WHERE strftime('%Y', c."Transaction Date") = '2024'
  AND b."Agricultural Product Name" = 'Wheat'
  AND c."Transaction Status" = 'Completed'
ORDER BY c."Sales Channel", qty

```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-010/attempt-01/sql/S33.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-010/attempt-01/sql/S33.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-010/attempt-01/results/S33.rows.jsonl)；完整：True；SHA256：`11e7836a6a635a34e8921ddaf3def61fa6a2c977804de0a3227bb2dc54fd6b36`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "c", "kind": "base", "block": null, "base_tables": ["core_transaction_information"]}, {"alias": "b", "kind": "base", "block": null, "base_tables": ["basic_product_information"]}] | [{"type": "INNER", "right": "basic_product_information AS b", "on": "c.\"Transaction Number\" = b.\"Transaction Number\"", "using": []}] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |

