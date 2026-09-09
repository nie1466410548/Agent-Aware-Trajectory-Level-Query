# dacomp-008

Analyze the average cost deviation (Budget Amount − Actual Cost) and its distribution acro…

运行：已提交。官方未评分。全部 SQL 尝试/成功 27/27；数据 SQL 25/25；Python 6 次。

完整原题：

Analyze the average cost deviation (Budget Amount − Actual Cost) and its distribution across different Project Types, and, incorporating fields such as Team Size, Risk Level, Customer Satisfaction, etc., explore how these factors are related to cost deviation.

| 表 | 行数 | 列数 |
| --- | --- | --- |
| sheet1 | 299 | 16 |


实际路线（分析者依据 SQL/源码概括，不代表 Agent 自述）：S3：sheet1 查询 → S8：sheet1 查询 → S13：sheet1 分组聚合 → S17：sheet1 分组聚合 → S22：sheet1 分组聚合 → S27：sheet1 查询（等距列出六个结构节点，全部步骤见下表）

数据库大小：110,592 字节。

## 数据 SQL

| SQL | 状态 | 基础表 | Join 输入/类型 | GROUP BY | 聚合表达式 | 结果行数 | 数据库 ms |
| --- | --- | --- | --- | --- | --- | --- | --- |
| [S3/Q1](#s3) | success | ["sheet1"] | 0 / {} | [] | [] | 10 | 0.591 |
| [S4/Q2](#s4) | success | ["sheet1"] | 0 / {} | [] | ["COUNT(*)"] | 1 | 0.353 |
| [S5/Q3](#s5) | success | ["sheet1"] | 0 / {} | [] | [] | 3 | 0.408 |
| [S6/Q4](#s6) | success | ["sheet1"] | 0 / {} | [] | [] | 3 | 0.383 |
| [S7/Q5](#s7) | success | ["sheet1"] | 0 / {} | [] | [] | 4 | 0.373 |
| [S8/Q6](#s8) | success | ["sheet1"] | 0 / {} | [] | [] | 3 | 0.377 |
| [S9/Q7](#s9) | success | ["sheet1"] | 0 / {} | ["\"Project Type\""] | ["COUNT(*)", "AVG(\"Budget Amount\" - \"Actual Cost\")", "AVG(\"Budget Amount\")", "AVG(\"Actual Cost\")", "MIN(\"Budget Amount\" - \"Actual Cost\")", "MAX(\"Budget Amount\" - \"Actual Cost\")", "AVG(\"Team Size\")", "AVG(\"Customer Satisfaction\")"] | 3 | 1.007 |
| [S10/Q8](#s10) | success | ["sheet1"] | 0 / {} | ["\"Risk Level\""] | ["COUNT(*)", "AVG(\"Budget Amount\" - \"Actual Cost\")", "AVG(\"Budget Amount\")", "AVG(\"Actual Cost\")", "MIN(\"Budget Amount\" - \"Actual Cost\")", "MAX(\"Budget Amount\" - \"Actual Cost\")"] | 3 | 0.6 |
| [S11/Q9](#s11) | success | ["sheet1"] | 0 / {} | ["\"Project Status\""] | ["COUNT(*)", "AVG(\"Budget Amount\" - \"Actual Cost\")", "AVG(\"Budget Amount\")", "AVG(\"Actual Cost\")"] | 4 | 0.611 |
| [S12/Q10](#s12) | success | ["sheet1"] | 0 / {} | ["\"Project Type\"", "\"Risk Level\""] | ["COUNT(*)", "AVG(\"Budget Amount\" - \"Actual Cost\")", "AVG(\"Team Size\")", "AVG(\"Customer Satisfaction\")"] | 9 | 0.69 |
| [S13/Q11](#s13) | success | ["sheet1"] | 0 / {} | ["\"Project Type\"", "\"Priority\""] | ["COUNT(*)", "AVG(\"Budget Amount\" - \"Actual Cost\")"] | 9 | 0.609 |
| [S14/Q12](#s14) | success | ["sheet1"] | 0 / {} | ["\"Project Type\""] | ["COUNT(*)", "AVG(\"Budget Amount\" - \"Actual Cost\")", "AVG((\"Budget Amount\" - \"Actual Cost\") * (\"Budget Amount\" - \"Actual Cost\"))", "AVG(\"Budget Amount\" - \"Actual Cost\")", "AVG(\"Budget Amount\" - \"Actual Cost\")", "AVG((\"Budget Amount\" - \"Actual Cost\") * (\"Budget Amount\" - \"Actual Cost\"))", "AVG(\"Budget Amount\" - \"Actual Cost\")", "AVG(\"Budget Amount\" - \"Actual Cost\")"] | 3 | 0.64 |
| [S15/Q13](#s15) | success | ["sheet1"] | 0 / {} | ["\"Risk Level\""] | ["AVG(\"Budget Amount\" - \"Actual Cost\")", "AVG(\"Budget Amount\")", "AVG(\"Actual Cost\")", "AVG((\"Budget Amount\" - \"Actual Cost\") * (\"Budget Amount\" - \"Actual Cost\"))", "AVG(\"Budget Amount\" - \"Actual Cost\")", "AVG(\"Budget Amount\" - \"Actual Cost\")"] | 3 | 0.648 |
| [S16/Q14](#s16) | success | ["sheet1"] | 0 / {} | [] | [] | 15 | 0.467 |
| [S17/Q15](#s17) | success | ["sheet1"] | 0 / {} | ["\"Project Type\""] | ["COUNT(CASE WHEN \"Project Status\" = 'Completed' THEN 1 END)", "COUNT(CASE WHEN \"Project Status\" = 'In Progress' THEN 1 END)", "COUNT(CASE WHEN \"Project Status\" = 'Delayed' THEN 1 END)", "AVG(CASE WHEN \"Project Status\" = 'Completed' THEN \"Budget Amount\" - \"Actual Cost\" END)", "AVG(CASE WHEN \"Project Status\" = 'In Progress' THEN \"Budget Amount\" - \"Actual Cost\" END)", "AVG(CASE WHEN \"Project Status\" = 'Delayed' THEN \"Budget Amount\" - \"Actual Cost\" END)"] | 3 | 0.693 |
| [S18/Q16](#s18) | success | ["sheet1"] | 0 / {} | ["\"Project Type\"", "\"Project Status\""] | ["COUNT(*)", "AVG(\"Budget Amount\" - \"Actual Cost\")", "AVG((\"Budget Amount\" - \"Actual Cost\") * 100.0 / \"Budget Amount\")"] | 12 | 0.662 |
| [S19/Q17](#s19) | success | ["sheet1"] | 0 / {} | ["\"Project Type\""] | ["MAX(CASE WHEN rn <= CAST(cnt * 0.10 AS INTEGER) THEN deviation END)", "MAX(CASE WHEN rn <= CAST(cnt * 0.25 AS INTEGER) THEN deviation END)", "MAX(CASE WHEN rn <= CAST(cnt * 0.50 AS INTEGER) THEN deviation END)", "MAX(CASE WHEN rn <= CAST(cnt * 0.75 AS INTEGER) THEN deviation END)", "MAX(CASE WHEN rn <= CAST(cnt * 0.90 AS INTEGER) THEN deviation END)"] | 3 | 1.542 |
| [S20/Q18](#s20) | success | ["sheet1"] | 0 / {} | [] | ["SUM(dev * team)", "SUM(dev * sat)", "SUM(dev * budget)", "COUNT(*)", "COUNT(*)", "COUNT(*)", "SUM(dev)", "SUM(team)", "SUM(dev)", "SUM(sat)", "SUM(dev)", "SUM(budget)", "SUM(dev * dev)", "SUM(team * team)", "SUM(dev * dev)", "SUM(sat * sat)", "SUM(dev * dev)", "SUM(budget * budget)", "COUNT(*)", "COUNT(*)", "COUNT(*)", "COUNT(*)", "COUNT(*)", "COUNT(*)", "SUM(dev)", "SUM(dev)", "SUM(team)", "SUM(team)", "SUM(dev)", "SUM(dev)", "SUM(sat)", "SUM(sat)", "SUM(dev)", "SUM(dev)", "SUM(budget)", "SUM(budget)"] | 1 | 0.774 |
| [S21/Q19](#s21) | success | ["sheet1"] | 0 / {} | [] | ["SUM(dev * team)", "SUM(dev * sat)", "SUM(dev * budget)", "COUNT(*)", "COUNT(*)", "COUNT(*)", "SUM(dev)", "SUM(team)", "SUM(dev)", "SUM(sat)", "SUM(dev)", "SUM(budget)", "SUM(dev * dev)", "SUM(team * team)", "SUM(dev * dev)", "SUM(sat * sat)", "SUM(dev * dev)", "SUM(budget * budget)", "COUNT(*)", "COUNT(*)", "COUNT(*)", "COUNT(*)", "COUNT(*)", "COUNT(*)", "SUM(dev)", "SUM(dev)", "SUM(team)", "SUM(team)", "SUM(dev)", "SUM(dev)", "SUM(sat)", "SUM(sat)", "SUM(dev)", "SUM(dev)", "SUM(budget)", "SUM(budget)"] | 1 | 0.873 |
| [S22/Q20](#s22) | success | ["sheet1"] | 0 / {} | ["\"Risk Level\""] | ["COUNT(*)", "AVG(\"Budget Amount\" - \"Actual Cost\")"] | 2 | 0.503 |
| [S23/Q21](#s23) | success | ["sheet1"] | 0 / {} | ["\"Project Type\"", "\"Risk Level\""] | ["COUNT(*)", "AVG(\"Budget Amount\" - \"Actual Cost\")", "AVG((\"Budget Amount\" - \"Actual Cost\") * 100.0 / \"Budget Amount\")"] | 6 | 0.546 |
| [S24/Q22](#s24) | success | ["sheet1"] | 0 / {} | ["\"Project Status\""] | ["COUNT(*)", "AVG(\"Budget Amount\" - \"Actual Cost\")", "AVG((\"Budget Amount\" - \"Actual Cost\") * 100.0 / \"Budget Amount\")", "AVG(\"Customer Satisfaction\")"] | 4 | 0.617 |
| [S25/Q23](#s25) | success | ["sheet1"] | 0 / {} | ["\"Priority\""] | ["COUNT(*)", "AVG(\"Budget Amount\" - \"Actual Cost\")", "AVG((\"Budget Amount\" - \"Actual Cost\") * 100.0 / \"Budget Amount\")"] | 3 | 0.523 |
| [S26/Q24](#s26) | success | ["sheet1"] | 0 / {} | ["\"Project Type\"", "\"Priority\""] | ["COUNT(*)", "AVG(\"Budget Amount\" - \"Actual Cost\")", "AVG((\"Budget Amount\" - \"Actual Cost\") * 100.0 / \"Budget Amount\")"] | 9 | 0.456 |
| [S27/Q25](#s27) | success | ["sheet1"] | 0 / {} | [] | [] | 299 | 1.02 |


## 元数据和设置

| SQL | 类别 | 状态 | 内容 |
| --- | --- | --- | --- |
| S1 | connection_setup | success | PRAGMA query_only=ON |
| S2 | metadata | success | SELECT name,sql FROM sqlite_master WHERE type='table' ORDER BY name |


## Python 与执行位置

人工源码审查：**reviewed_with_statistical_exceptions_and_SQL_capable_summaries**。Python groups raw inputs for statistical tests and renders figures; those statistical procedures justify Python inputs. P3–P5 also calculate count/mean/median summaries outside SQL. Count/mean portions are SQL-capable and are disclosed separately; median and tests are statistical exceptions. This trajectory is not labeled strictly SQL-only or fully strict database-first. [证据](../reviews/dacomp-008.json)。

P1：SQLite lacks built-in hypothesis tests (ANOVA/Kruskal-Wallis), percentiles beyond manual computation, and plotting. I need the core numeric/categorical columns to build distribution plots, run group-difference significance tests, and compute Spearman correlations that are not available in SQL.

[源码](../../../runs/dsv4flash-db-first-full-01/dacomp-008/attempt-01/python/P1.py)；[输出](../../../runs/dsv4flash-db-first-full-01/dacomp-008/attempt-01/python/P1.stdout)；[错误](../../../runs/dsv4flash-db-first-full-01/dacomp-008/attempt-01/python/P1.stderr)。检出需人工核验的 SQL 可实现操作：.query(；不能仅凭理由判为合规。

P2：Creating distribution visualizations (box plots, histograms) of cost deviation by Project Type, and scatter plots of deviation vs Team Size/Satisfaction. These are purely visual outputs not supported by SQLite.

[源码](../../../runs/dsv4flash-db-first-full-01/dacomp-008/attempt-01/python/P2.py)；[输出](../../../runs/dsv4flash-db-first-full-01/dacomp-008/attempt-01/python/P2.stdout)；[错误](../../../runs/dsv4flash-db-first-full-01/dacomp-008/attempt-01/python/P2.stderr)。自动源码筛查未检出预设迁出信号；这不是全面语义合规证明。

P3：Running Kruskal-Wallis (non-parametric ANOVA) tests to compare cost deviation distributions across Project Types and Risk Levels, because the deviation data is non-normal (skewed). SQLite cannot perform these tests.

[源码](../../../runs/dsv4flash-db-first-full-01/dacomp-008/attempt-01/python/P3.py)；[输出](../../../runs/dsv4flash-db-first-full-01/dacomp-008/attempt-01/python/P3.stdout)；[错误](../../../runs/dsv4flash-db-first-full-01/dacomp-008/attempt-01/python/P3.stderr)。检出需人工核验的 SQL 可实现操作：groupby(；不能仅凭理由判为合规。

P4：Computing OLS regression coefficients (via numpy lstsq, since SQLite can't do regression) to quantify how Team Size, Risk Level, Customer Satisfaction, and Budget relate to cost deviation; also a cross-tab of risk by status to understand composition of in-progress bias.

[源码](../../../runs/dsv4flash-db-first-full-01/dacomp-008/attempt-01/python/P4.py)；[输出](../../../runs/dsv4flash-db-first-full-01/dacomp-008/attempt-01/python/P4.stdout)；[错误](../../../runs/dsv4flash-db-first-full-01/dacomp-008/attempt-01/python/P4.stderr)。检出需人工核验的 SQL 可实现操作：groupby(；不能仅凭理由判为合规。

P5：Analyzing whether in-progress deviation is simply a function of completion percentage (unspent budget), and producing a final grouped bar chart of mean deviation by Project Type x Risk Level. This is visualization plus a correlation check not supported by SQLite.

[源码](../../../runs/dsv4flash-db-first-full-01/dacomp-008/attempt-01/python/P5.py)；[输出](../../../runs/dsv4flash-db-first-full-01/dacomp-008/attempt-01/python/P5.stdout)；[错误](../../../runs/dsv4flash-db-first-full-01/dacomp-008/attempt-01/python/P5.stderr)。检出需人工核验的 SQL 可实现操作：groupby(；不能仅凭理由判为合规。

P6：Summarizing the distribution statistics for the final report, computing the exact decile/percentile values for the distribution summary table by project type.

[源码](../../../runs/dsv4flash-db-first-full-01/dacomp-008/attempt-01/python/P6.py)；[输出](../../../runs/dsv4flash-db-first-full-01/dacomp-008/attempt-01/python/P6.stdout)；[错误](../../../runs/dsv4flash-db-first-full-01/dacomp-008/attempt-01/python/P6.stderr)。自动源码筛查未检出预设迁出信号；这不是全面语义合规证明。

## 优化机会

已验证候选。筛选限于精确 SQL、相同自包含 CTE、相同单表完整过滤、可分解单表聚合；未覆盖任意 Join 等价和一般谓词蕴含。全部候选都是 offline，未测在线预测。

| 候选 | 类型 | 已有结果 | 覆盖 SQL | 后续次数 | 中间行数 | 验证 | 成本 |
| --- | --- | --- | --- | --- | --- | --- | --- |
| C1 | aggregate MV | False | ["S4", "S9", "S10", "S11", "S12", "S13", "S14", "S15", "S17", "S18", "S24"] | 10 | 49 | verified | Not benchmarked; correctness alone does not establish net speedup. |
| C2 | common filtered view | False | ["S22", "S23", "S25", "S26"] | 3 | 129 | verified | Not benchmarked; correctness alone does not establish net speedup. |
| C3 | aggregate MV | False | ["S23", "S25", "S26"] | 2 | 16 | verified | Not benchmarked; correctness alone does not establish net speedup. |


已验证覆盖（含触发查询、候选并集去重）：15/25 条成功数据 SQL。正确性仅针对当前数据库快照；未测性能的候选不能声称已加速。

[完整 build/rewrite 与比较证据](dacomp-008.analysis.json)。

### C1：aggregate MV

Union of grouping keys; decomposable aggregate states; AVG uses SUM and non-NULL COUNT.

原查询 [S4](#s4), [S9](#s9), [S10](#s10), [S11](#s11), [S12](#s12), [S13](#s13), [S14](#s14), [S15](#s15), [S17](#s17), [S18](#s18), [S24](#s24) → 新增共享状态 C1 → 后续 10 次可复用。该构建点为事后假设，不代表 Agent 当时预知后续。

构建定义：

```sql
SELECT "Project Type" AS __g0, "Risk Level" AS __g1, "Project Status" AS __g2, "Priority" AS __g3, COUNT(*) AS __a0, SUM("Budget Amount" - "Actual Cost") AS __a1_sum, COUNT("Budget Amount" - "Actual Cost") AS __a1_n, SUM("Budget Amount") AS __a2_sum, COUNT("Budget Amount") AS __a2_n, SUM("Actual Cost") AS __a3_sum, COUNT("Actual Cost") AS __a3_n, MIN("Budget Amount" - "Actual Cost") AS __a4, MAX("Budget Amount" - "Actual Cost") AS __a5, SUM("Team Size") AS __a6_sum, COUNT("Team Size") AS __a6_n, SUM("Customer Satisfaction") AS __a7_sum, COUNT("Customer Satisfaction") AS __a7_n, SUM(("Budget Amount" - "Actual Cost") * ("Budget Amount" - "Actual Cost")) AS __a8_sum, COUNT(("Budget Amount" - "Actual Cost") * ("Budget Amount" - "Actual Cost")) AS __a8_n, COUNT(CASE WHEN "Project Status" = 'Completed' THEN 1 END) AS __a9, COUNT(CASE WHEN "Project Status" = 'In Progress' THEN 1 END) AS __a10, COUNT(CASE WHEN "Project Status" = 'Delayed' THEN 1 END) AS __a11, SUM(CASE WHEN "Project Status" = 'Completed' THEN "Budget Amount" - "Actual Cost" END) AS __a12_sum, COUNT(CASE WHEN "Project Status" = 'Completed' THEN "Budget Amount" - "Actual Cost" END) AS __a12_n, SUM(CASE WHEN "Project Status" = 'In Progress' THEN "Budget Amount" - "Actual Cost" END) AS __a13_sum, COUNT(CASE WHEN "Project Status" = 'In Progress' THEN "Budget Amount" - "Actual Cost" END) AS __a13_n, SUM(CASE WHEN "Project Status" = 'Delayed' THEN "Budget Amount" - "Actual Cost" END) AS __a14_sum, COUNT(CASE WHEN "Project Status" = 'Delayed' THEN "Budget Amount" - "Actual Cost" END) AS __a14_n, SUM(("Budget Amount" - "Actual Cost") * 100.0 / "Budget Amount") AS __a15_sum, COUNT(("Budget Amount" - "Actual Cost") * 100.0 / "Budget Amount") AS __a15_n FROM "sheet1"  GROUP BY "Project Type", "Risk Level", "Project Status", "Priority"
```

受益查询 S4 的改写示例：

```sql
SELECT SUM(__a0) AS total_rows FROM temp.reuse_candidate
```

| 原 SQL | 列名一致 | 结果一致 | 比较方法 |
| --- | --- | --- | --- |
| S4 | True | True | exact_multiset |
| S9 | True | True | ordered_numeric_tolerance |
| S10 | True | True | ordered_numeric_tolerance |
| S11 | True | True | ordered_numeric_tolerance |
| S12 | True | True | ordered_numeric_tolerance |
| S13 | True | True | ordered_numeric_tolerance |
| S14 | True | True | exact_multiset |
| S15 | True | True | exact_multiset |
| S17 | True | True | ordered_numeric_tolerance |
| S18 | True | True | ordered_numeric_tolerance |
| S24 | True | True | ordered_numeric_tolerance |


验证状态：verified；成本结论：Not benchmarked; correctness alone does not establish net speedup.

### C2：common filtered view

Same single source and complete filter; original filter retained.

原查询 [S22](#s22), [S23](#s23), [S25](#s25), [S26](#s26) → 新增共享状态 C2 → 后续 3 次可复用。该构建点为事后假设，不代表 Agent 当时预知后续。

构建定义：

```sql
SELECT * FROM "sheet1" WHERE "Project Status" = 'Completed'
```

受益查询 S22 的改写示例：

```sql
SELECT "Risk Level", "Project Status", COUNT(*) AS n, ROUND(AVG("Budget Amount" - "Actual Cost"), 2) AS avg_dev FROM temp.reuse_candidate AS sheet1 WHERE "Project Status" = 'Completed' GROUP BY "Risk Level" ORDER BY avg_dev DESC
```

| 原 SQL | 列名一致 | 结果一致 | 比较方法 |
| --- | --- | --- | --- |
| S22 | True | True | ordered_numeric_tolerance |
| S23 | True | True | ordered_numeric_tolerance |
| S25 | True | True | ordered_numeric_tolerance |
| S26 | True | True | ordered_numeric_tolerance |


验证状态：verified；成本结论：Not benchmarked; correctness alone does not establish net speedup.

### C3：aggregate MV

Union of grouping keys; decomposable aggregate states; AVG uses SUM and non-NULL COUNT.

原查询 [S23](#s23), [S25](#s25), [S26](#s26) → 新增共享状态 C3 → 后续 2 次可复用。该构建点为事后假设，不代表 Agent 当时预知后续。

构建定义：

```sql
SELECT "Project Type" AS __g0, "Risk Level" AS __g1, "Priority" AS __g2, COUNT(*) AS __a0, SUM("Budget Amount" - "Actual Cost") AS __a1_sum, COUNT("Budget Amount" - "Actual Cost") AS __a1_n, SUM(("Budget Amount" - "Actual Cost") * 100.0 / "Budget Amount") AS __a2_sum, COUNT(("Budget Amount" - "Actual Cost") * 100.0 / "Budget Amount") AS __a2_n FROM "sheet1" WHERE "Project Status" = 'Completed' GROUP BY "Project Type", "Risk Level", "Priority"
```

受益查询 S23 的改写示例：

```sql
SELECT __g0 AS "Project Type", __g1 AS "Risk Level", SUM(__a0) AS n, ROUND((1.0 * SUM(__a1_sum) / NULLIF(SUM(__a1_n), 0)), 2) AS avg_dev, ROUND((1.0 * SUM(__a2_sum) / NULLIF(SUM(__a2_n), 0)), 2) AS avg_dev_pct FROM temp.reuse_candidate GROUP BY __g0, __g1 ORDER BY __g0, __g1
```

| 原 SQL | 列名一致 | 结果一致 | 比较方法 |
| --- | --- | --- | --- |
| S23 | True | True | ordered_numeric_tolerance |
| S25 | True | True | ordered_numeric_tolerance |
| S26 | True | True | ordered_numeric_tolerance |


验证状态：verified；成本结论：Not benchmarked; correctness alone does not establish net speedup.

结果依赖：自动记录 SQL→Python 的接口父调用，以及源码中引用归档文件的消费者；字面值相同不认定因果。模型方向选择需要人工读取消息，尚未做全面因果标注。

[原始报告](../../../runs/dsv4flash-db-first-full-01/dacomp-008/attempt-01/answer.md)；[统一消息](../../../runs/dsv4flash-db-first-full-01/dacomp-008/attempt-01/messages.jsonl)；[原始 OpenCode 事件](../../../runs/dsv4flash-db-first-full-01/dacomp-008/attempt-01/opencode.jsonl)；[SQL 引擎日志](../../../runs/dsv4flash-db-first-full-01/dacomp-008/attempt-01/sql_journal.jsonl)。

[可读报告（本地图片链接规范化）](../answers/dacomp-008.md)。原始回答保留，分析结论未改写。

## S1

类别 `connection_setup`；来源 `connection`；调用 `a4071453002e4022b9e2932a83671849`；状态 `success`。

```sql
PRAGMA query_only=ON
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-008/attempt-01/sql/S1.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-008/attempt-01/sql/S1.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-008/attempt-01/results/S1.rows.jsonl)；完整：True；SHA256：`e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`。

## S2

类别 `metadata`；来源 `list_db`；调用 `a4071453002e4022b9e2932a83671849`；状态 `success`。

```sql
SELECT name,sql FROM sqlite_master WHERE type='table' ORDER BY name
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-008/attempt-01/sql/S2.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-008/attempt-01/sql/S2.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-008/attempt-01/results/S2.rows.jsonl)；完整：True；SHA256：`52e7c675c40627f5a34c4cbf201516d171f78d071a7d18608129b48e2d0787e6`。

## S3

类别 `data`；来源 `query_db`；调用 `4493adfa251a40de8d1c1962ed6d088d`；状态 `success`。

```sql
SELECT * FROM sheet1 LIMIT 10
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-008/attempt-01/sql/S3.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-008/attempt-01/sql/S3.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-008/attempt-01/results/S3.rows.jsonl)；完整：True；SHA256：`d8bfa099ba40d25857bcc4db4fa1ec379cb79f18b0f4b5cc9a1c925a3f9f16a4`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "sheet1", "kind": "base", "block": null, "base_tables": ["sheet1"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |


## S4

类别 `data`；来源 `query_db`；调用 `fd3f2a89b6c8416f858ef11095f6a45c`；状态 `success`。

```sql
SELECT COUNT(*) as total_rows FROM sheet1
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-008/attempt-01/sql/S4.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-008/attempt-01/sql/S4.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-008/attempt-01/results/S4.rows.jsonl)；完整：True；SHA256：`e4f467596919dc82d0b055c6a6a9528e769c051459d1e9263fc33a5d17d20731`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "sheet1", "kind": "base", "block": null, "base_tables": ["sheet1"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |


## S5

类别 `data`；来源 `query_db`；调用 `a8696c9dca5448848bb12f7f4b04d903`；状态 `success`。

```sql
SELECT DISTINCT "Project Type" FROM sheet1
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-008/attempt-01/sql/S5.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-008/attempt-01/sql/S5.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-008/attempt-01/results/S5.rows.jsonl)；完整：True；SHA256：`29b7aed3f1cba3d5127f3b8b0706e5b92a3ad8ef6ab9e7b32a5c021eea2714f4`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "sheet1", "kind": "base", "block": null, "base_tables": ["sheet1"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |


## S6

类别 `data`；来源 `query_db`；调用 `c2dff963412741e6acfe1508e8e5e607`；状态 `success`。

```sql
SELECT DISTINCT "Risk Level" FROM sheet1
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-008/attempt-01/sql/S6.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-008/attempt-01/sql/S6.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-008/attempt-01/results/S6.rows.jsonl)；完整：True；SHA256：`db5aac6e5ec0ceb3494b1330a100152d4b70ecc6cd1bd7f28b9ed50208ad5151`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "sheet1", "kind": "base", "block": null, "base_tables": ["sheet1"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |


## S7

类别 `data`；来源 `query_db`；调用 `e27f0768e7b6407bbf9cb0f773670a33`；状态 `success`。

```sql
SELECT DISTINCT "Project Status" FROM sheet1
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-008/attempt-01/sql/S7.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-008/attempt-01/sql/S7.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-008/attempt-01/results/S7.rows.jsonl)；完整：True；SHA256：`71c0820d5dbfeeffbe6f3329a40786ae63dcca8f7517b60bb6bf5c61d8637df7`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "sheet1", "kind": "base", "block": null, "base_tables": ["sheet1"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |


## S8

类别 `data`；来源 `query_db`；调用 `2e405ae7a911440aac3b00e1e04917d7`；状态 `success`。

```sql
SELECT DISTINCT "Priority" FROM sheet1
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-008/attempt-01/sql/S8.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-008/attempt-01/sql/S8.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-008/attempt-01/results/S8.rows.jsonl)；完整：True；SHA256：`6920439bdd032fd951cf5916834e120c2493edd979281f0b7587f18a49949857`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "sheet1", "kind": "base", "block": null, "base_tables": ["sheet1"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |


## S9

类别 `data`；来源 `query_db`；调用 `b62628841b9543b2bcbe6463f280b6a7`；状态 `success`。

```sql
SELECT 
  "Project Type",
  COUNT(*) as count,
  ROUND(AVG("Budget Amount" - "Actual Cost"), 2) as avg_cost_deviation,
  ROUND(AVG("Budget Amount"), 2) as avg_budget,
  ROUND(AVG("Actual Cost"), 2) as avg_actual_cost,
  ROUND(MIN("Budget Amount" - "Actual Cost"), 2) as min_deviation,
  ROUND(MAX("Budget Amount" - "Actual Cost"), 2) as max_deviation,
  ROUND(AVG("Team Size"), 1) as avg_team_size,
  ROUND(AVG("Customer Satisfaction"), 2) as avg_customer_satisfaction
FROM sheet1
GROUP BY "Project Type"
ORDER BY avg_cost_deviation DESC
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-008/attempt-01/sql/S9.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-008/attempt-01/sql/S9.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-008/attempt-01/results/S9.rows.jsonl)；完整：True；SHA256：`d44f7376ab24a0664915faae8ff49e424a14ef9316e5cc247298c7d7129d7737`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "sheet1", "kind": "base", "block": null, "base_tables": ["sheet1"]}] | [] | ["\"Project Type\""] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |
| B1 | AVG("Budget Amount" - "Actual Cost") | [{"table": "sheet1", "column": "Budget Amount"}, {"table": "sheet1", "column": "Actual Cost"}] | [] | False |
| B1 | AVG("Budget Amount") | [{"table": "sheet1", "column": "Budget Amount"}] | [] | False |
| B1 | AVG("Actual Cost") | [{"table": "sheet1", "column": "Actual Cost"}] | [] | False |
| B1 | MIN("Budget Amount" - "Actual Cost") | [{"table": "sheet1", "column": "Budget Amount"}, {"table": "sheet1", "column": "Actual Cost"}] | [] | False |
| B1 | MAX("Budget Amount" - "Actual Cost") | [{"table": "sheet1", "column": "Budget Amount"}, {"table": "sheet1", "column": "Actual Cost"}] | [] | False |
| B1 | AVG("Team Size") | [{"table": "sheet1", "column": "Team Size"}] | [] | False |
| B1 | AVG("Customer Satisfaction") | [{"table": "sheet1", "column": "Customer Satisfaction"}] | [] | False |


## S10

类别 `data`；来源 `query_db`；调用 `b14ddf1a3d3345bd8e1b8751b56c3d60`；状态 `success`。

```sql
SELECT 
  "Risk Level",
  COUNT(*) as count,
  ROUND(AVG("Budget Amount" - "Actual Cost"), 2) as avg_cost_deviation,
  ROUND(AVG("Budget Amount"), 2) as avg_budget,
  ROUND(AVG("Actual Cost"), 2) as avg_actual_cost,
  ROUND(MIN("Budget Amount" - "Actual Cost"), 2) as min_deviation,
  ROUND(MAX("Budget Amount" - "Actual Cost"), 2) as max_deviation
FROM sheet1
GROUP BY "Risk Level"
ORDER BY avg_cost_deviation DESC
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-008/attempt-01/sql/S10.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-008/attempt-01/sql/S10.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-008/attempt-01/results/S10.rows.jsonl)；完整：True；SHA256：`c94b17fdf78eca26d79682217f0a03625ae57f2f0fb574f6ed4ebd003e0aa3bc`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "sheet1", "kind": "base", "block": null, "base_tables": ["sheet1"]}] | [] | ["\"Risk Level\""] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |
| B1 | AVG("Budget Amount" - "Actual Cost") | [{"table": "sheet1", "column": "Budget Amount"}, {"table": "sheet1", "column": "Actual Cost"}] | [] | False |
| B1 | AVG("Budget Amount") | [{"table": "sheet1", "column": "Budget Amount"}] | [] | False |
| B1 | AVG("Actual Cost") | [{"table": "sheet1", "column": "Actual Cost"}] | [] | False |
| B1 | MIN("Budget Amount" - "Actual Cost") | [{"table": "sheet1", "column": "Budget Amount"}, {"table": "sheet1", "column": "Actual Cost"}] | [] | False |
| B1 | MAX("Budget Amount" - "Actual Cost") | [{"table": "sheet1", "column": "Budget Amount"}, {"table": "sheet1", "column": "Actual Cost"}] | [] | False |


## S11

类别 `data`；来源 `query_db`；调用 `916af0a18d6f40ddbdf12e33254aaf8c`；状态 `success`。

```sql
SELECT 
  "Project Status",
  COUNT(*) as count,
  ROUND(AVG("Budget Amount" - "Actual Cost"), 2) as avg_cost_deviation,
  ROUND(AVG("Budget Amount"), 2) as avg_budget,  
  ROUND(AVG("Actual Cost"), 2) as avg_actual_cost
FROM sheet1
GROUP BY "Project Status"
ORDER BY avg_cost_deviation DESC
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-008/attempt-01/sql/S11.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-008/attempt-01/sql/S11.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-008/attempt-01/results/S11.rows.jsonl)；完整：True；SHA256：`95500d7fee25d0614bef553653f3645a1fb34160c474f2a388809c33f73c6181`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "sheet1", "kind": "base", "block": null, "base_tables": ["sheet1"]}] | [] | ["\"Project Status\""] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |
| B1 | AVG("Budget Amount" - "Actual Cost") | [{"table": "sheet1", "column": "Budget Amount"}, {"table": "sheet1", "column": "Actual Cost"}] | [] | False |
| B1 | AVG("Budget Amount") | [{"table": "sheet1", "column": "Budget Amount"}] | [] | False |
| B1 | AVG("Actual Cost") | [{"table": "sheet1", "column": "Actual Cost"}] | [] | False |


## S12

类别 `data`；来源 `query_db`；调用 `e0b4e0d9ce88438299897eee4a6c1873`；状态 `success`。

```sql
SELECT 
  "Project Type",
  "Risk Level",
  COUNT(*) as count,
  ROUND(AVG("Budget Amount" - "Actual Cost"), 2) as avg_cost_deviation,
  ROUND(AVG("Team Size"), 1) as avg_team_size,
  ROUND(AVG("Customer Satisfaction"), 2) as avg_satisfaction
FROM sheet1
GROUP BY "Project Type", "Risk Level"
ORDER BY "Project Type", "Risk Level"
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-008/attempt-01/sql/S12.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-008/attempt-01/sql/S12.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-008/attempt-01/results/S12.rows.jsonl)；完整：True；SHA256：`00cf5c0460d6b9795dbdd8aabe243f8b7f2b0f2d1014be1f2c99817db8c3b3f0`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "sheet1", "kind": "base", "block": null, "base_tables": ["sheet1"]}] | [] | ["\"Project Type\"", "\"Risk Level\""] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |
| B1 | AVG("Budget Amount" - "Actual Cost") | [{"table": "sheet1", "column": "Budget Amount"}, {"table": "sheet1", "column": "Actual Cost"}] | [] | False |
| B1 | AVG("Team Size") | [{"table": "sheet1", "column": "Team Size"}] | [] | False |
| B1 | AVG("Customer Satisfaction") | [{"table": "sheet1", "column": "Customer Satisfaction"}] | [] | False |


## S13

类别 `data`；来源 `query_db`；调用 `79dc8b3165ca46caa9918a751cb5343a`；状态 `success`。

```sql
SELECT 
  "Project Type",
  "Priority",
  COUNT(*) as count,
  ROUND(AVG("Budget Amount" - "Actual Cost"), 2) as avg_cost_deviation
FROM sheet1
GROUP BY "Project Type", "Priority"
ORDER BY "Project Type", "Priority"
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-008/attempt-01/sql/S13.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-008/attempt-01/sql/S13.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-008/attempt-01/results/S13.rows.jsonl)；完整：True；SHA256：`a51c64ca78e99016464688022fc576554b391b1ab610913d81940a0d8315fd2a`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "sheet1", "kind": "base", "block": null, "base_tables": ["sheet1"]}] | [] | ["\"Project Type\"", "\"Priority\""] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |
| B1 | AVG("Budget Amount" - "Actual Cost") | [{"table": "sheet1", "column": "Budget Amount"}, {"table": "sheet1", "column": "Actual Cost"}] | [] | False |


## S14

类别 `data`；来源 `query_db`；调用 `4cca4081c61e44a2b0d42168960611b0`；状态 `success`。

```sql
SELECT
  "Project Type",
  COUNT(*) as count,
  ROUND(AVG("Budget Amount" - "Actual Cost"), 2) as mean_dev,
  ROUND(AVG(("Budget Amount" - "Actual Cost") * ("Budget Amount" - "Actual Cost")) - AVG("Budget Amount" - "Actual Cost") * AVG("Budget Amount" - "Actual Cost"), 2) as variance_dev,
  ROUND(SQRT(MAX(0, AVG(("Budget Amount" - "Actual Cost") * ("Budget Amount" - "Actual Cost")) - AVG("Budget Amount" - "Actual Cost") * AVG("Budget Amount" - "Actual Cost"))), 2) as stddev_dev
FROM sheet1
GROUP BY "Project Type"
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-008/attempt-01/sql/S14.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-008/attempt-01/sql/S14.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-008/attempt-01/results/S14.rows.jsonl)；完整：True；SHA256：`83ce8accb61a8bf091b321d0a96df1cf9acfbd265a0ce3a039bf020e971146d7`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "sheet1", "kind": "base", "block": null, "base_tables": ["sheet1"]}] | [] | ["\"Project Type\""] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |
| B1 | AVG("Budget Amount" - "Actual Cost") | [{"table": "sheet1", "column": "Budget Amount"}, {"table": "sheet1", "column": "Actual Cost"}] | [] | False |
| B1 | AVG(("Budget Amount" - "Actual Cost") * ("Budget Amount" - "Actual Cost")) | [{"table": "sheet1", "column": "Budget Amount"}, {"table": "sheet1", "column": "Actual Cost"}, {"table": "sheet1", "column": "Budget Amount"}, {"table": "sheet1", "column": "Actual Cost"}] | [] | False |
| B1 | AVG("Budget Amount" - "Actual Cost") | [{"table": "sheet1", "column": "Budget Amount"}, {"table": "sheet1", "column": "Actual Cost"}] | [] | False |
| B1 | AVG("Budget Amount" - "Actual Cost") | [{"table": "sheet1", "column": "Budget Amount"}, {"table": "sheet1", "column": "Actual Cost"}] | [] | False |
| B1 | AVG(("Budget Amount" - "Actual Cost") * ("Budget Amount" - "Actual Cost")) | [{"table": "sheet1", "column": "Budget Amount"}, {"table": "sheet1", "column": "Actual Cost"}, {"table": "sheet1", "column": "Budget Amount"}, {"table": "sheet1", "column": "Actual Cost"}] | [] | False |
| B1 | AVG("Budget Amount" - "Actual Cost") | [{"table": "sheet1", "column": "Budget Amount"}, {"table": "sheet1", "column": "Actual Cost"}] | [] | False |
| B1 | AVG("Budget Amount" - "Actual Cost") | [{"table": "sheet1", "column": "Budget Amount"}, {"table": "sheet1", "column": "Actual Cost"}] | [] | False |


## S15

类别 `data`；来源 `query_db`；调用 `474af0fa56e040e9b969c89479a274f7`；状态 `success`。

```sql
SELECT
  "Risk Level",
  ROUND(AVG("Budget Amount" - "Actual Cost"), 2) as mean_dev,
  ROUND(SQRT(MAX(0, AVG(("Budget Amount" - "Actual Cost") * ("Budget Amount" - "Actual Cost")) - AVG("Budget Amount" - "Actual Cost") * AVG("Budget Amount" - "Actual Cost"))), 2) as stddev_dev,
  ROUND(AVG("Budget Amount"), 2) as avg_budget,
  ROUND(AVG("Actual Cost"), 2) as avg_actual
FROM sheet1
GROUP BY "Risk Level"
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-008/attempt-01/sql/S15.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-008/attempt-01/sql/S15.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-008/attempt-01/results/S15.rows.jsonl)；完整：True；SHA256：`875bc6044535cf93e6d760c7640ea8b481cc0b8682f2e0fdc5f9cfa433b1f098`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "sheet1", "kind": "base", "block": null, "base_tables": ["sheet1"]}] | [] | ["\"Risk Level\""] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | AVG("Budget Amount" - "Actual Cost") | [{"table": "sheet1", "column": "Budget Amount"}, {"table": "sheet1", "column": "Actual Cost"}] | [] | False |
| B1 | AVG("Budget Amount") | [{"table": "sheet1", "column": "Budget Amount"}] | [] | False |
| B1 | AVG("Actual Cost") | [{"table": "sheet1", "column": "Actual Cost"}] | [] | False |
| B1 | AVG(("Budget Amount" - "Actual Cost") * ("Budget Amount" - "Actual Cost")) | [{"table": "sheet1", "column": "Budget Amount"}, {"table": "sheet1", "column": "Actual Cost"}, {"table": "sheet1", "column": "Budget Amount"}, {"table": "sheet1", "column": "Actual Cost"}] | [] | False |
| B1 | AVG("Budget Amount" - "Actual Cost") | [{"table": "sheet1", "column": "Budget Amount"}, {"table": "sheet1", "column": "Actual Cost"}] | [] | False |
| B1 | AVG("Budget Amount" - "Actual Cost") | [{"table": "sheet1", "column": "Budget Amount"}, {"table": "sheet1", "column": "Actual Cost"}] | [] | False |


## S16

类别 `data`；来源 `query_db`；调用 `6cb7f685db6e4d40899ac3225368fd45`；状态 `success`。

```sql
SELECT 
  ROUND(("Budget Amount" - "Actual Cost") / NULLIF("Budget Amount", 0) * 100, 1) as deviation_pct,
  "Budget Amount" - "Actual Cost" as deviation,
  "Project Type", "Risk Level", "Team Size", "Customer Satisfaction", "Project Status"
FROM sheet1
ORDER BY deviation DESC
LIMIT 15
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-008/attempt-01/sql/S16.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-008/attempt-01/sql/S16.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-008/attempt-01/results/S16.rows.jsonl)；完整：True；SHA256：`e9d344adfc58bf42539864380b9b9c4ad108fe73f2a7f3b0ee77481dc9700847`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "sheet1", "kind": "base", "block": null, "base_tables": ["sheet1"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |


## S17

类别 `data`；来源 `query_db`；调用 `78ee95be83fe45c0adb04bd672f4de8e`；状态 `success`。

```sql
SELECT
  "Project Type",
  ROUND(AVG(CASE WHEN "Project Status" = 'Completed' THEN "Budget Amount" - "Actual Cost" END), 2) as completed_avg_dev,
  COUNT(CASE WHEN "Project Status" = 'Completed' THEN 1 END) as completed_n,
  ROUND(AVG(CASE WHEN "Project Status" = 'In Progress' THEN "Budget Amount" - "Actual Cost" END), 2) as inprogress_avg_dev,
  COUNT(CASE WHEN "Project Status" = 'In Progress' THEN 1 END) as inprogress_n,
  ROUND(AVG(CASE WHEN "Project Status" = 'Delayed' THEN "Budget Amount" - "Actual Cost" END), 2) as delayed_avg_dev,
  COUNT(CASE WHEN "Project Status" = 'Delayed' THEN 1 END) as delayed_n
FROM sheet1
GROUP BY "Project Type"
ORDER BY "Project Type"
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-008/attempt-01/sql/S17.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-008/attempt-01/sql/S17.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-008/attempt-01/results/S17.rows.jsonl)；完整：True；SHA256：`f5ad3f97370c44ff66fedf1ea7b65b1b7b92445b85f19f304c260b9f205d5cd3`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "sheet1", "kind": "base", "block": null, "base_tables": ["sheet1"]}] | [] | ["\"Project Type\""] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(CASE WHEN "Project Status" = 'Completed' THEN 1 END) | [] | [{"table": "sheet1", "column": "Project Status"}] | False |
| B1 | COUNT(CASE WHEN "Project Status" = 'In Progress' THEN 1 END) | [] | [{"table": "sheet1", "column": "Project Status"}] | False |
| B1 | COUNT(CASE WHEN "Project Status" = 'Delayed' THEN 1 END) | [] | [{"table": "sheet1", "column": "Project Status"}] | False |
| B1 | AVG(CASE WHEN "Project Status" = 'Completed' THEN "Budget Amount" - "Actual Cost" END) | [{"table": "sheet1", "column": "Budget Amount"}, {"table": "sheet1", "column": "Actual Cost"}] | [{"table": "sheet1", "column": "Project Status"}] | False |
| B1 | AVG(CASE WHEN "Project Status" = 'In Progress' THEN "Budget Amount" - "Actual Cost" END) | [{"table": "sheet1", "column": "Budget Amount"}, {"table": "sheet1", "column": "Actual Cost"}] | [{"table": "sheet1", "column": "Project Status"}] | False |
| B1 | AVG(CASE WHEN "Project Status" = 'Delayed' THEN "Budget Amount" - "Actual Cost" END) | [{"table": "sheet1", "column": "Budget Amount"}, {"table": "sheet1", "column": "Actual Cost"}] | [{"table": "sheet1", "column": "Project Status"}] | False |


## S18

类别 `data`；来源 `query_db`；调用 `cb2e40ac467745d5b1822600ed57dc78`；状态 `success`。

```sql
SELECT
  "Project Type",
  "Project Status",
  COUNT(*) as n,
  ROUND(AVG("Budget Amount" - "Actual Cost"), 2) as avg_dev,
  ROUND(AVG(("Budget Amount" - "Actual Cost") * 100.0 / "Budget Amount"), 2) as avg_dev_pct
FROM sheet1
GROUP BY "Project Type", "Project Status"
ORDER BY "Project Type", "Project Status"
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-008/attempt-01/sql/S18.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-008/attempt-01/sql/S18.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-008/attempt-01/results/S18.rows.jsonl)；完整：True；SHA256：`d86ce19f8dc9001833127d41798f90d77acafd8f6fda9382b3c03e204adedd28`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "sheet1", "kind": "base", "block": null, "base_tables": ["sheet1"]}] | [] | ["\"Project Type\"", "\"Project Status\""] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |
| B1 | AVG("Budget Amount" - "Actual Cost") | [{"table": "sheet1", "column": "Budget Amount"}, {"table": "sheet1", "column": "Actual Cost"}] | [] | False |
| B1 | AVG(("Budget Amount" - "Actual Cost") * 100.0 / "Budget Amount") | [{"table": "sheet1", "column": "Budget Amount"}, {"table": "sheet1", "column": "Budget Amount"}, {"table": "sheet1", "column": "Actual Cost"}] | [] | False |


## S19

类别 `data`；来源 `query_db`；调用 `180fab26302d45a695e2a7622d907294`；状态 `success`。

```sql
WITH dev AS (
  SELECT 
    "Project Type",
    "Budget Amount" - "Actual Cost" AS deviation
  FROM sheet1
),
ranked AS (
  SELECT 
    "Project Type",
    deviation,
    ROW_NUMBER() OVER (PARTITION BY "Project Type" ORDER BY deviation) as rn,
    COUNT(*) OVER (PARTITION BY "Project Type") as cnt
  FROM dev
)
SELECT 
  "Project Type",
  MAX(CASE WHEN rn <= CAST(cnt*0.10 AS INTEGER) THEN deviation END) as p10,
  MAX(CASE WHEN rn <= CAST(cnt*0.25 AS INTEGER) THEN deviation END) as p25,
  MAX(CASE WHEN rn <= CAST(cnt*0.50 AS INTEGER) THEN deviation END) as p50,
  MAX(CASE WHEN rn <= CAST(cnt*0.75 AS INTEGER) THEN deviation END) as p75,
  MAX(CASE WHEN rn <= CAST(cnt*0.90 AS INTEGER) THEN deviation END) as p90
FROM ranked
GROUP BY "Project Type"
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-008/attempt-01/sql/S19.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-008/attempt-01/sql/S19.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-008/attempt-01/results/S19.rows.jsonl)；完整：True；SHA256：`703074b429b6c2028979b7cd83441a83f9e26f00c9af830baadfdd2e6811b102`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "sheet1", "kind": "base", "block": null, "base_tables": ["sheet1"]}] | [] | [] |
| B2 | [{"alias": "dev", "kind": "derived", "block": "B1", "base_tables": ["sheet1"]}] | [] | [] |
| B3 | [{"alias": "ranked", "kind": "derived", "block": "B2", "base_tables": ["sheet1"]}] | [] | ["\"Project Type\""] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B3 | MAX(CASE WHEN rn <= CAST(cnt * 0.10 AS INTEGER) THEN deviation END) | [{"table": "sheet1", "column": "Budget Amount"}, {"table": "sheet1", "column": "Actual Cost"}] | [{"table": "sheet1", "column": "Project Type"}, {"table": "sheet1", "column": "Budget Amount"}, {"table": "sheet1", "column": "Actual Cost"}, {"table": "sheet1", "column": "Project Type"}] | False |
| B3 | MAX(CASE WHEN rn <= CAST(cnt * 0.25 AS INTEGER) THEN deviation END) | [{"table": "sheet1", "column": "Budget Amount"}, {"table": "sheet1", "column": "Actual Cost"}] | [{"table": "sheet1", "column": "Project Type"}, {"table": "sheet1", "column": "Budget Amount"}, {"table": "sheet1", "column": "Actual Cost"}, {"table": "sheet1", "column": "Project Type"}] | False |
| B3 | MAX(CASE WHEN rn <= CAST(cnt * 0.50 AS INTEGER) THEN deviation END) | [{"table": "sheet1", "column": "Budget Amount"}, {"table": "sheet1", "column": "Actual Cost"}] | [{"table": "sheet1", "column": "Project Type"}, {"table": "sheet1", "column": "Budget Amount"}, {"table": "sheet1", "column": "Actual Cost"}, {"table": "sheet1", "column": "Project Type"}] | False |
| B3 | MAX(CASE WHEN rn <= CAST(cnt * 0.75 AS INTEGER) THEN deviation END) | [{"table": "sheet1", "column": "Budget Amount"}, {"table": "sheet1", "column": "Actual Cost"}] | [{"table": "sheet1", "column": "Project Type"}, {"table": "sheet1", "column": "Budget Amount"}, {"table": "sheet1", "column": "Actual Cost"}, {"table": "sheet1", "column": "Project Type"}] | False |
| B3 | MAX(CASE WHEN rn <= CAST(cnt * 0.90 AS INTEGER) THEN deviation END) | [{"table": "sheet1", "column": "Budget Amount"}, {"table": "sheet1", "column": "Actual Cost"}] | [{"table": "sheet1", "column": "Project Type"}, {"table": "sheet1", "column": "Budget Amount"}, {"table": "sheet1", "column": "Actual Cost"}, {"table": "sheet1", "column": "Project Type"}] | False |


## S20

类别 `data`；来源 `query_db`；调用 `81260e1f078a41a6a3c4ea05feafcdf9`；状态 `success`。

```sql
SELECT
  ROUND((SUM(dev * team) - SUM(dev)*SUM(team)/COUNT(*)) / 
    NULLIF(SQRT((SUM(dev*dev) - SUM(dev)*SUM(dev)/COUNT(*)) * (SUM(team*team) - SUM(team)*SUM(team)/COUNT(*))), 0), 4) as corr_dev_team,
  ROUND((SUM(dev * sat) - SUM(dev)*SUM(sat)/COUNT(*)) / 
    NULLIF(SQRT((SUM(dev*dev) - SUM(dev)*SUM(dev)/COUNT(*)) * (SUM(sat*sat) - SUM(sat)*SUM(sat)/COUNT(*))), 0), 4) as corr_dev_sat,
  ROUND((SUM(dev * budget) - SUM(dev)*SUM(budget)/COUNT(*)) / 
    NULLIF(SQRT((SUM(dev*dev) - SUM(dev)*SUM(dev)/COUNT(*)) * (SUM(budget*budget) - SUM(budget)*SUM(budget)/COUNT(*))), 0), 4) as corr_dev_budget
FROM (
  SELECT 
    "Budget Amount" - "Actual Cost" as dev,
    "Team Size" as team,
    "Customer Satisfaction" as sat,
    "Budget Amount" as budget
  FROM sheet1
)
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-008/attempt-01/sql/S20.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-008/attempt-01/sql/S20.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-008/attempt-01/results/S20.rows.jsonl)；完整：True；SHA256：`3d767cae301870b7b43536d2aeebbe676be627c764b51ef53850d5a5975e92eb`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "sheet1", "kind": "base", "block": null, "base_tables": ["sheet1"]}] | [] | [] |
| B2 | [{"alias": "", "kind": "derived", "block": "B1", "base_tables": ["sheet1"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B2 | SUM(dev * team) | [{"table": "sheet1", "column": "Budget Amount"}, {"table": "sheet1", "column": "Actual Cost"}, {"table": "sheet1", "column": "Team Size"}] | [] | False |
| B2 | SUM(dev * sat) | [{"table": "sheet1", "column": "Budget Amount"}, {"table": "sheet1", "column": "Actual Cost"}, {"table": "sheet1", "column": "Customer Satisfaction"}] | [] | False |
| B2 | SUM(dev * budget) | [{"table": "sheet1", "column": "Budget Amount"}, {"table": "sheet1", "column": "Actual Cost"}, {"table": "sheet1", "column": "Budget Amount"}] | [] | False |
| B2 | COUNT(*) | [] | [] | True |
| B2 | COUNT(*) | [] | [] | True |
| B2 | COUNT(*) | [] | [] | True |
| B2 | SUM(dev) | [{"table": "sheet1", "column": "Budget Amount"}, {"table": "sheet1", "column": "Actual Cost"}] | [] | False |
| B2 | SUM(team) | [{"table": "sheet1", "column": "Team Size"}] | [] | False |
| B2 | SUM(dev) | [{"table": "sheet1", "column": "Budget Amount"}, {"table": "sheet1", "column": "Actual Cost"}] | [] | False |
| B2 | SUM(sat) | [{"table": "sheet1", "column": "Customer Satisfaction"}] | [] | False |
| B2 | SUM(dev) | [{"table": "sheet1", "column": "Budget Amount"}, {"table": "sheet1", "column": "Actual Cost"}] | [] | False |
| B2 | SUM(budget) | [{"table": "sheet1", "column": "Budget Amount"}] | [] | False |
| B2 | SUM(dev * dev) | [{"table": "sheet1", "column": "Budget Amount"}, {"table": "sheet1", "column": "Actual Cost"}, {"table": "sheet1", "column": "Budget Amount"}, {"table": "sheet1", "column": "Actual Cost"}] | [] | False |
| B2 | SUM(team * team) | [{"table": "sheet1", "column": "Team Size"}, {"table": "sheet1", "column": "Team Size"}] | [] | False |
| B2 | SUM(dev * dev) | [{"table": "sheet1", "column": "Budget Amount"}, {"table": "sheet1", "column": "Actual Cost"}, {"table": "sheet1", "column": "Budget Amount"}, {"table": "sheet1", "column": "Actual Cost"}] | [] | False |
| B2 | SUM(sat * sat) | [{"table": "sheet1", "column": "Customer Satisfaction"}, {"table": "sheet1", "column": "Customer Satisfaction"}] | [] | False |
| B2 | SUM(dev * dev) | [{"table": "sheet1", "column": "Budget Amount"}, {"table": "sheet1", "column": "Actual Cost"}, {"table": "sheet1", "column": "Budget Amount"}, {"table": "sheet1", "column": "Actual Cost"}] | [] | False |
| B2 | SUM(budget * budget) | [{"table": "sheet1", "column": "Budget Amount"}, {"table": "sheet1", "column": "Budget Amount"}] | [] | False |
| B2 | COUNT(*) | [] | [] | True |
| B2 | COUNT(*) | [] | [] | True |
| B2 | COUNT(*) | [] | [] | True |
| B2 | COUNT(*) | [] | [] | True |
| B2 | COUNT(*) | [] | [] | True |
| B2 | COUNT(*) | [] | [] | True |
| B2 | SUM(dev) | [{"table": "sheet1", "column": "Budget Amount"}, {"table": "sheet1", "column": "Actual Cost"}] | [] | False |
| B2 | SUM(dev) | [{"table": "sheet1", "column": "Budget Amount"}, {"table": "sheet1", "column": "Actual Cost"}] | [] | False |
| B2 | SUM(team) | [{"table": "sheet1", "column": "Team Size"}] | [] | False |
| B2 | SUM(team) | [{"table": "sheet1", "column": "Team Size"}] | [] | False |
| B2 | SUM(dev) | [{"table": "sheet1", "column": "Budget Amount"}, {"table": "sheet1", "column": "Actual Cost"}] | [] | False |
| B2 | SUM(dev) | [{"table": "sheet1", "column": "Budget Amount"}, {"table": "sheet1", "column": "Actual Cost"}] | [] | False |
| B2 | SUM(sat) | [{"table": "sheet1", "column": "Customer Satisfaction"}] | [] | False |
| B2 | SUM(sat) | [{"table": "sheet1", "column": "Customer Satisfaction"}] | [] | False |
| B2 | SUM(dev) | [{"table": "sheet1", "column": "Budget Amount"}, {"table": "sheet1", "column": "Actual Cost"}] | [] | False |
| B2 | SUM(dev) | [{"table": "sheet1", "column": "Budget Amount"}, {"table": "sheet1", "column": "Actual Cost"}] | [] | False |
| B2 | SUM(budget) | [{"table": "sheet1", "column": "Budget Amount"}] | [] | False |
| B2 | SUM(budget) | [{"table": "sheet1", "column": "Budget Amount"}] | [] | False |


## S21

类别 `data`；来源 `query_db`；调用 `0f2be26a26ce4a06a6b847e182f0a365`；状态 `success`。

```sql
SELECT
  ROUND((SUM(dev * team) - SUM(dev)*SUM(team)/COUNT(*)) / 
    NULLIF(SQRT((SUM(dev*dev) - SUM(dev)*SUM(dev)/COUNT(*)) * (SUM(team*team) - SUM(team)*SUM(team)/COUNT(*))), 0), 4) as corr_dev_team,
  ROUND((SUM(dev * sat) - SUM(dev)*SUM(sat)/COUNT(*)) / 
    NULLIF(SQRT((SUM(dev*dev) - SUM(dev)*SUM(dev)/COUNT(*)) * (SUM(sat*sat) - SUM(sat)*SUM(sat)/COUNT(*))), 0), 4) as corr_dev_sat,
  ROUND((SUM(dev * budget) - SUM(dev)*SUM(budget)/COUNT(*)) / 
    NULLIF(SQRT((SUM(dev*dev) - SUM(dev)*SUM(dev)/COUNT(*)) * (SUM(budget*budget) - SUM(budget)*SUM(budget)/COUNT(*))), 0), 4) as corr_dev_budget
FROM (
  SELECT 
    "Budget Amount" - "Actual Cost" as dev,
    "Team Size" as team,
    "Customer Satisfaction" as sat,
    "Budget Amount" as budget
  FROM sheet1
  WHERE "Project Status" = 'Completed'
)
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-008/attempt-01/sql/S21.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-008/attempt-01/sql/S21.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-008/attempt-01/results/S21.rows.jsonl)；完整：True；SHA256：`1bd3fee90933ccc51beb8e38cb3b038470381be46c553402e0dfcf8bfe4f3a9a`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "sheet1", "kind": "base", "block": null, "base_tables": ["sheet1"]}] | [] | [] |
| B2 | [{"alias": "", "kind": "derived", "block": "B1", "base_tables": ["sheet1"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B2 | SUM(dev * team) | [{"table": "sheet1", "column": "Budget Amount"}, {"table": "sheet1", "column": "Actual Cost"}, {"table": "sheet1", "column": "Team Size"}] | [] | False |
| B2 | SUM(dev * sat) | [{"table": "sheet1", "column": "Budget Amount"}, {"table": "sheet1", "column": "Actual Cost"}, {"table": "sheet1", "column": "Customer Satisfaction"}] | [] | False |
| B2 | SUM(dev * budget) | [{"table": "sheet1", "column": "Budget Amount"}, {"table": "sheet1", "column": "Actual Cost"}, {"table": "sheet1", "column": "Budget Amount"}] | [] | False |
| B2 | COUNT(*) | [] | [] | True |
| B2 | COUNT(*) | [] | [] | True |
| B2 | COUNT(*) | [] | [] | True |
| B2 | SUM(dev) | [{"table": "sheet1", "column": "Budget Amount"}, {"table": "sheet1", "column": "Actual Cost"}] | [] | False |
| B2 | SUM(team) | [{"table": "sheet1", "column": "Team Size"}] | [] | False |
| B2 | SUM(dev) | [{"table": "sheet1", "column": "Budget Amount"}, {"table": "sheet1", "column": "Actual Cost"}] | [] | False |
| B2 | SUM(sat) | [{"table": "sheet1", "column": "Customer Satisfaction"}] | [] | False |
| B2 | SUM(dev) | [{"table": "sheet1", "column": "Budget Amount"}, {"table": "sheet1", "column": "Actual Cost"}] | [] | False |
| B2 | SUM(budget) | [{"table": "sheet1", "column": "Budget Amount"}] | [] | False |
| B2 | SUM(dev * dev) | [{"table": "sheet1", "column": "Budget Amount"}, {"table": "sheet1", "column": "Actual Cost"}, {"table": "sheet1", "column": "Budget Amount"}, {"table": "sheet1", "column": "Actual Cost"}] | [] | False |
| B2 | SUM(team * team) | [{"table": "sheet1", "column": "Team Size"}, {"table": "sheet1", "column": "Team Size"}] | [] | False |
| B2 | SUM(dev * dev) | [{"table": "sheet1", "column": "Budget Amount"}, {"table": "sheet1", "column": "Actual Cost"}, {"table": "sheet1", "column": "Budget Amount"}, {"table": "sheet1", "column": "Actual Cost"}] | [] | False |
| B2 | SUM(sat * sat) | [{"table": "sheet1", "column": "Customer Satisfaction"}, {"table": "sheet1", "column": "Customer Satisfaction"}] | [] | False |
| B2 | SUM(dev * dev) | [{"table": "sheet1", "column": "Budget Amount"}, {"table": "sheet1", "column": "Actual Cost"}, {"table": "sheet1", "column": "Budget Amount"}, {"table": "sheet1", "column": "Actual Cost"}] | [] | False |
| B2 | SUM(budget * budget) | [{"table": "sheet1", "column": "Budget Amount"}, {"table": "sheet1", "column": "Budget Amount"}] | [] | False |
| B2 | COUNT(*) | [] | [] | True |
| B2 | COUNT(*) | [] | [] | True |
| B2 | COUNT(*) | [] | [] | True |
| B2 | COUNT(*) | [] | [] | True |
| B2 | COUNT(*) | [] | [] | True |
| B2 | COUNT(*) | [] | [] | True |
| B2 | SUM(dev) | [{"table": "sheet1", "column": "Budget Amount"}, {"table": "sheet1", "column": "Actual Cost"}] | [] | False |
| B2 | SUM(dev) | [{"table": "sheet1", "column": "Budget Amount"}, {"table": "sheet1", "column": "Actual Cost"}] | [] | False |
| B2 | SUM(team) | [{"table": "sheet1", "column": "Team Size"}] | [] | False |
| B2 | SUM(team) | [{"table": "sheet1", "column": "Team Size"}] | [] | False |
| B2 | SUM(dev) | [{"table": "sheet1", "column": "Budget Amount"}, {"table": "sheet1", "column": "Actual Cost"}] | [] | False |
| B2 | SUM(dev) | [{"table": "sheet1", "column": "Budget Amount"}, {"table": "sheet1", "column": "Actual Cost"}] | [] | False |
| B2 | SUM(sat) | [{"table": "sheet1", "column": "Customer Satisfaction"}] | [] | False |
| B2 | SUM(sat) | [{"table": "sheet1", "column": "Customer Satisfaction"}] | [] | False |
| B2 | SUM(dev) | [{"table": "sheet1", "column": "Budget Amount"}, {"table": "sheet1", "column": "Actual Cost"}] | [] | False |
| B2 | SUM(dev) | [{"table": "sheet1", "column": "Budget Amount"}, {"table": "sheet1", "column": "Actual Cost"}] | [] | False |
| B2 | SUM(budget) | [{"table": "sheet1", "column": "Budget Amount"}] | [] | False |
| B2 | SUM(budget) | [{"table": "sheet1", "column": "Budget Amount"}] | [] | False |


## S22

类别 `data`；来源 `query_db`；调用 `1eaebe5895af4cd99f977ca214bab694`；状态 `success`。

```sql
SELECT
  "Risk Level",
  "Project Status",
  COUNT(*) as n,
  ROUND(AVG("Budget Amount" - "Actual Cost"), 2) as avg_dev
FROM sheet1
WHERE "Project Status" = 'Completed'
GROUP BY "Risk Level"
ORDER BY avg_dev DESC
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-008/attempt-01/sql/S22.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-008/attempt-01/sql/S22.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-008/attempt-01/results/S22.rows.jsonl)；完整：True；SHA256：`13ed6fd8e29f79e46b35ab9e09129bd9ecbaa2a0058cbb2d873503a3121c0b0c`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "sheet1", "kind": "base", "block": null, "base_tables": ["sheet1"]}] | [] | ["\"Risk Level\""] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |
| B1 | AVG("Budget Amount" - "Actual Cost") | [{"table": "sheet1", "column": "Budget Amount"}, {"table": "sheet1", "column": "Actual Cost"}] | [] | False |


## S23

类别 `data`；来源 `query_db`；调用 `55551df151ea412d900ababe0154b72f`；状态 `success`。

```sql
SELECT
  "Project Type",
  "Risk Level",
  COUNT(*) as n,
  ROUND(AVG("Budget Amount" - "Actual Cost"), 2) as avg_dev,
  ROUND(AVG(("Budget Amount" - "Actual Cost")*100.0/"Budget Amount"), 2) as avg_dev_pct
FROM sheet1
WHERE "Project Status" = 'Completed'
GROUP BY "Project Type", "Risk Level"
ORDER BY "Project Type", "Risk Level"
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-008/attempt-01/sql/S23.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-008/attempt-01/sql/S23.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-008/attempt-01/results/S23.rows.jsonl)；完整：True；SHA256：`6470031bbc460d1eb49dbb5de55de72800f1111798e347c10a43ac8df6a294e7`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "sheet1", "kind": "base", "block": null, "base_tables": ["sheet1"]}] | [] | ["\"Project Type\"", "\"Risk Level\""] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |
| B1 | AVG("Budget Amount" - "Actual Cost") | [{"table": "sheet1", "column": "Budget Amount"}, {"table": "sheet1", "column": "Actual Cost"}] | [] | False |
| B1 | AVG(("Budget Amount" - "Actual Cost") * 100.0 / "Budget Amount") | [{"table": "sheet1", "column": "Budget Amount"}, {"table": "sheet1", "column": "Budget Amount"}, {"table": "sheet1", "column": "Actual Cost"}] | [] | False |


## S24

类别 `data`；来源 `query_db`；调用 `073c01539bcd4a3fb18d662a380bd40b`；状态 `success`。

```sql
SELECT
  "Project Status",
  COUNT(*) as n,
  ROUND(AVG("Budget Amount" - "Actual Cost"), 2) as avg_dev,
  ROUND(AVG(("Budget Amount" - "Actual Cost")*100.0/"Budget Amount"), 2) as avg_dev_pct,
  ROUND(AVG("Customer Satisfaction"), 2) as avg_sat
FROM sheet1
GROUP BY "Project Status"
ORDER BY avg_dev DESC
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-008/attempt-01/sql/S24.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-008/attempt-01/sql/S24.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-008/attempt-01/results/S24.rows.jsonl)；完整：True；SHA256：`303feba8b4d853db68dd2a6e183fcc33f85815fdb6b85e9ca67423dc7f5a31d6`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "sheet1", "kind": "base", "block": null, "base_tables": ["sheet1"]}] | [] | ["\"Project Status\""] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |
| B1 | AVG("Budget Amount" - "Actual Cost") | [{"table": "sheet1", "column": "Budget Amount"}, {"table": "sheet1", "column": "Actual Cost"}] | [] | False |
| B1 | AVG(("Budget Amount" - "Actual Cost") * 100.0 / "Budget Amount") | [{"table": "sheet1", "column": "Budget Amount"}, {"table": "sheet1", "column": "Budget Amount"}, {"table": "sheet1", "column": "Actual Cost"}] | [] | False |
| B1 | AVG("Customer Satisfaction") | [{"table": "sheet1", "column": "Customer Satisfaction"}] | [] | False |


## S25

类别 `data`；来源 `query_db`；调用 `fa34c39ead394ed6807242bf7d7524e6`；状态 `success`。

```sql
SELECT
  "Priority",
  COUNT(*) as n,
  ROUND(AVG("Budget Amount" - "Actual Cost"), 2) as avg_dev,
  ROUND(AVG(("Budget Amount" - "Actual Cost")*100.0/"Budget Amount"), 2) as avg_dev_pct
FROM sheet1
WHERE "Project Status" = 'Completed'
GROUP BY "Priority"
ORDER BY avg_dev DESC
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-008/attempt-01/sql/S25.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-008/attempt-01/sql/S25.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-008/attempt-01/results/S25.rows.jsonl)；完整：True；SHA256：`b4149590d3b9e94bc054ef424b777d6c9db8bf2538af2d2680f6aa88f8d46375`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "sheet1", "kind": "base", "block": null, "base_tables": ["sheet1"]}] | [] | ["\"Priority\""] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |
| B1 | AVG("Budget Amount" - "Actual Cost") | [{"table": "sheet1", "column": "Budget Amount"}, {"table": "sheet1", "column": "Actual Cost"}] | [] | False |
| B1 | AVG(("Budget Amount" - "Actual Cost") * 100.0 / "Budget Amount") | [{"table": "sheet1", "column": "Budget Amount"}, {"table": "sheet1", "column": "Budget Amount"}, {"table": "sheet1", "column": "Actual Cost"}] | [] | False |


## S26

类别 `data`；来源 `query_db`；调用 `d24075b334184124a48b4ca73c31ddad`；状态 `success`。

```sql
SELECT
  "Project Type",
  "Priority",
  COUNT(*) as n,
  ROUND(AVG("Budget Amount" - "Actual Cost"), 2) as avg_dev,
  ROUND(AVG(("Budget Amount" - "Actual Cost")*100.0/"Budget Amount"), 2) as avg_dev_pct
FROM sheet1
WHERE "Project Status" = 'Completed'
GROUP BY "Project Type", "Priority"
ORDER BY "Project Type", "Priority"
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-008/attempt-01/sql/S26.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-008/attempt-01/sql/S26.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-008/attempt-01/results/S26.rows.jsonl)；完整：True；SHA256：`481877ab90cafb88852af2580853d45f8cf641462ab0ac68e91798897c3aeecb`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "sheet1", "kind": "base", "block": null, "base_tables": ["sheet1"]}] | [] | ["\"Project Type\"", "\"Priority\""] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |
| B1 | AVG("Budget Amount" - "Actual Cost") | [{"table": "sheet1", "column": "Budget Amount"}, {"table": "sheet1", "column": "Actual Cost"}] | [] | False |
| B1 | AVG(("Budget Amount" - "Actual Cost") * 100.0 / "Budget Amount") | [{"table": "sheet1", "column": "Budget Amount"}, {"table": "sheet1", "column": "Budget Amount"}, {"table": "sheet1", "column": "Actual Cost"}] | [] | False |


## S27

类别 `data`；来源 `python`；调用 `de7a49954d564ea08ccc58e8e16d875f`；状态 `success`。

```sql

SELECT "Project Type", "Budget Amount" AS budget, "Actual Cost" AS actual,
       "Team Size" AS team, "Risk Level" AS risk, "Customer Satisfaction" AS sat,
       "Project Status" AS status, "Priority", "Completion Percentage" AS comp
FROM sheet1

```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-008/attempt-01/sql/S27.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-008/attempt-01/sql/S27.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-008/attempt-01/results/S27.rows.jsonl)；完整：True；SHA256：`8cdaeecdf37199f51a8a3750b18550b117635549c2c9139e105a432c819cf1d6`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "sheet1", "kind": "base", "block": null, "base_tables": ["sheet1"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |

