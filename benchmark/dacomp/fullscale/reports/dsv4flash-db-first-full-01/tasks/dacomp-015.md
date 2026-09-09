# dacomp-015

Based on Floor Plan, Decoration, Floor, and Orientation, analyze which combinations of hom…

运行：已提交。官方未评分。全部 SQL 尝试/成功 29/29；数据 SQL 27/27；Python 9 次。

完整原题：

Based on Floor Plan, Decoration, Floor, and Orientation, analyze which combinations of homes have higher Watch Count in the market (provide the top 10), and study which factors affect their Showings.

| 表 | 行数 | 列数 |
| --- | --- | --- |
| data | 29975 | 14 |


实际路线（分析者依据 SQL/源码概括，不代表 Agent 自述）：检查户型、装修、楼层、朝向和看房数据 → 解析字段 → 四因素组合汇总并取 Top-10 → 对带看量做回归/方差分析 → 绘图与分组摘要。

数据库大小：12,038,144 字节。

## 数据 SQL

| SQL | 状态 | 基础表 | Join 输入/类型 | GROUP BY | 聚合表达式 | 结果行数 | 数据库 ms |
| --- | --- | --- | --- | --- | --- | --- | --- |
| [S3/Q1](#s3) | success | ["data"] | 0 / {} | [] | [] | 10 | 0.283 |
| [S4/Q2](#s4) | success | ["data"] | 0 / {} | [] | ["COUNT(*)"] | 1 | 4.484 |
| [S5/Q3](#s5) | success | ["data"] | 0 / {} | [] | [] | 44 | 13.891 |
| [S6/Q4](#s6) | success | ["data"] | 0 / {} | [] | [] | 5 | 18.586 |
| [S7/Q5](#s7) | success | ["data"] | 0 / {} | [] | [] | 52 | 19.824 |
| [S8/Q6](#s8) | success | ["data"] | 0 / {} | [] | [] | 9 | 18.046 |
| [S9/Q7](#s9) | success | ["data"] | 0 / {} | ["\"Floor Plan\""] | ["COUNT(*)"] | 44 | 13.554 |
| [S10/Q8](#s10) | success | ["data"] | 0 / {} | ["Floor"] | ["COUNT(*)"] | 52 | 20.011 |
| [S11/Q9](#s11) | success | ["data"] | 0 / {} | ["Decoration"] | ["COUNT(*)"] | 5 | 15.939 |
| [S12/Q10](#s12) | success | ["data"] | 0 / {} | ["Orientation"] | ["COUNT(*)"] | 9 | 18.315 |
| [S13/Q11](#s13) | success | ["data"] | 0 / {} | ["Floor"] | ["COUNT(*)"] | 52 | 20.05 |
| [S14/Q12](#s14) | success | ["data"] | 0 / {} | ["Floor"] | ["COUNT(*)"] | 5 | 12.143 |
| [S15/Q13](#s15) | success | ["data"] | 0 / {} | ["Floor"] | ["COUNT(*)"] | 52 | 20.18 |
| [S16/Q14](#s16) | success | ["data"] | 0 / {} | [] | ["GROUP_CONCAT(Floor, ' \| ')"] | 1 | 19.774 |
| [S17/Q15](#s17) | success | ["data"] | 0 / {} | ["\"Floor Plan\""] | ["COUNT(*)"] | 44 | 13.755 |
| [S18/Q16](#s18) | success | ["data"] | 0 / {} | [] | ["COUNT(*)", "SUM(CASE WHEN \"Watch Count\" > 0 THEN 1 ELSE 0 END)", "SUM(CASE WHEN \"Watch Count\" = 0 THEN 1 ELSE 0 END)", "SUM(CASE WHEN \"Watch Count\" > 50 THEN 1 ELSE 0 END)", "SUM(CASE WHEN \"Showings\" > 0 THEN 1 ELSE 0 END)", "SUM(CASE WHEN \"Showings\" = 0 THEN 1 ELSE 0 END)", "SUM(CASE WHEN \"Showings\" > 10 THEN 1 ELSE 0 END)", "AVG(\"Watch Count\")", "AVG(Showings)", "MAX(\"Watch Count\")", "MAX(Showings)", "MIN(\"Watch Count\")", "MIN(Showings)"] | 1 | 20.292 |
| [S19/Q17](#s19) | success | ["data"] | 0 / {} | ["\"Watch Count\""] | ["COUNT(*)"] | 20 | 9.707 |
| [S20/Q18](#s20) | success | ["data"] | 0 / {} | [] | [] | 46 | 12.914 |
| [S21/Q19](#s21) | success | ["data"] | 0 / {} | [] | [] | 5 | 15.966 |
| [S22/Q20](#s22) | success | ["data"] | 0 / {} | [] | [] | 29975 | 98.728 |
| [S23/Q21](#s23) | success | ["data"] | 0 / {} | [] | [] | 29975 | 98.92 |
| [S24/Q22](#s24) | success | ["data"] | 0 / {} | ["\"Floor Plan\"", "Decoration", "Floor", "Orientation"] | ["COUNT(*)", "AVG(\"Watch Count\")", "SUM(\"Watch Count\")", "MAX(\"Watch Count\")"] | 10 | 51.041 |
| [S25/Q23](#s25) | success | ["data"] | 0 / {} | ["\"Floor Plan\"", "Decoration", "Floor", "Orientation"] | ["COUNT(*)", "AVG(\"Watch Count\")", "SUM(\"Watch Count\")", "MAX(\"Watch Count\")"] | 10 | 51.143 |
| [S26/Q24](#s26) | success | ["data"] | 0 / {} | ["\"Floor Plan\"", "Decoration", "Floor", "Orientation"] | ["COUNT(*)", "MAX(\"Watch Count\")", "SUM(CASE WHEN \"Watch Count\" >= 20 THEN 1 ELSE 0 END)", "AVG(\"Watch Count\")"] | 25 | 51.61 |
| [S27/Q25](#s27) | success | ["data"] | 0 / {} | [] | [] | 6 | 6.135 |
| [S28/Q26](#s28) | success | ["data"] | 0 / {} | ["Featured"] | ["COUNT(*)", "AVG(\"Watch Count\")", "AVG(Showings)"] | 2 | 14.631 |
| [S29/Q27](#s29) | success | ["data"] | 0 / {} | ["\"Date Published\""] | ["COUNT(*)", "AVG(\"Watch Count\")", "AVG(Showings)"] | 5 | 21.722 |


## 元数据和设置

| SQL | 类别 | 状态 | 内容 |
| --- | --- | --- | --- |
| S1 | connection_setup | success | PRAGMA query_only=ON |
| S2 | metadata | success | SELECT name,sql FROM sqlite_master WHERE type='table' ORDER BY name |


## Python 与执行位置

人工源码审查：**database_first_violation**。P3 computes the four-factor housing combinations and count/mean/max/Top-10 ranking in pandas; P4/P9 calculate additional grouped summaries and P8 plot-order means. SQLite can reasonably perform these operations. Quantiles, OLS/ANOVA and rendering are distinguished as statistical/visual uses, not a blanket exemption for groupby. [证据](../reviews/dacomp-015.json)。

P1：Need to parse Floor field into numeric floor level and categorize it, and parse Floor Plan into bedroom/living room counts. This requires complex string parsing that is more manageable in Python than SQLite.

[源码](../../../runs/dsv4flash-db-first-full-01/dacomp-015/attempt-01/python/P1.py)；[输出](../../../runs/dsv4flash-db-first-full-01/dacomp-015/attempt-01/python/P1.stdout)；[错误](../../../runs/dsv4flash-db-first-full-01/dacomp-015/attempt-01/python/P1.stderr)。检出需人工核验的 SQL 可实现操作：.query(, sort_values(；不能仅凭理由判为合规。

P2：Fix regex to parse "6-story building" (hyphenated) and save parsed data as CSV for later analysis steps.

[源码](../../../runs/dsv4flash-db-first-full-01/dacomp-015/attempt-01/python/P2.py)；[输出](../../../runs/dsv4flash-db-first-full-01/dacomp-015/attempt-01/python/P2.stdout)；[错误](../../../runs/dsv4flash-db-first-full-01/dacomp-015/attempt-01/python/P2.stderr)。检出需人工核验的 SQL 可实现操作：.query(, sort_values(；不能仅凭理由判为合规。

P3：Compute median-based combination rankings for Watch Count, which requires percentile/median computation per group that is cumbersome in SQLite; also start examining Showings factors.

[源码](../../../runs/dsv4flash-db-first-full-01/dacomp-015/attempt-01/python/P3.py)；[输出](../../../runs/dsv4flash-db-first-full-01/dacomp-015/attempt-01/python/P3.stdout)；[错误](../../../runs/dsv4flash-db-first-full-01/dacomp-015/attempt-01/python/P3.stderr)。检出需人工核验的 SQL 可实现操作：groupby(, sort_values(；不能仅凭理由判为合规。

P4：Analyze factors affecting Showings: compute univariate mean Showings by each factor (Floor Plan/bedrooms, Decoration, Floor, Orientation) and their correlations. This requires statistical aggregation and correlation computation better handled in Python.

[源码](../../../runs/dsv4flash-db-first-full-01/dacomp-015/attempt-01/python/P4.py)；[输出](../../../runs/dsv4flash-db-first-full-01/dacomp-015/attempt-01/python/P4.stdout)；[错误](../../../runs/dsv4flash-db-first-full-01/dacomp-015/attempt-01/python/P4.stderr)。检出需人工核验的 SQL 可实现操作：groupby(, sort_values(；不能仅凭理由判为合规。

P5：Parse Price and Area into numeric values to use as control variables in the Showings regression model; SQLite string parsing of mixed currency formats is complex, so this is done in Python.

[源码](../../../runs/dsv4flash-db-first-full-01/dacomp-015/attempt-01/python/P5.py)；[输出](../../../runs/dsv4flash-db-first-full-01/dacomp-015/attempt-01/python/P5.stdout)；[错误](../../../runs/dsv4flash-db-first-full-01/dacomp-015/attempt-01/python/P5.stderr)。自动源码筛查未检出预设迁出信号；这不是全面语义合规证明。

P6：Build an OLS-style regression model (via numpy lstsq) to quantify which factors affect Showings, since scipy/numpy are available but multivariate regression with categorical dummies is not supported by SQLite.

[源码](../../../runs/dsv4flash-db-first-full-01/dacomp-015/attempt-01/python/P6.py)；[输出](../../../runs/dsv4flash-db-first-full-01/dacomp-015/attempt-01/python/P6.stdout)；[错误](../../../runs/dsv4flash-db-first-full-01/dacomp-015/attempt-01/python/P6.stderr)。自动源码筛查未检出预设迁出信号；这不是全面语义合规证明。

P7：Fix the OLS regression alignment issue by properly aligning y and X after dropping NaN values.

[源码](../../../runs/dsv4flash-db-first-full-01/dacomp-015/attempt-01/python/P7.py)；[输出](../../../runs/dsv4flash-db-first-full-01/dacomp-015/attempt-01/python/P7.stdout)；[错误](../../../runs/dsv4flash-db-first-full-01/dacomp-015/attempt-01/python/P7.stderr)。自动源码筛查未检出预设迁出信号；这不是全面语义合规证明。

P8：Create visualizations: bar charts of top 10 combinations by Watch Count, and factor effects on Showings, using matplotlib/seaborn.

[源码](../../../runs/dsv4flash-db-first-full-01/dacomp-015/attempt-01/python/P8.py)；[输出](../../../runs/dsv4flash-db-first-full-01/dacomp-015/attempt-01/python/P8.stdout)；[错误](../../../runs/dsv4flash-db-first-full-01/dacomp-015/attempt-01/python/P8.stderr)。检出需人工核验的 SQL 可实现操作：groupby(, sort_values(；不能仅凭理由判为合规。

P9：Compile the final formatted results: top 10 combination table with full stats and Showings factor summary, to be included in the report.

[源码](../../../runs/dsv4flash-db-first-full-01/dacomp-015/attempt-01/python/P9.py)；[输出](../../../runs/dsv4flash-db-first-full-01/dacomp-015/attempt-01/python/P9.stdout)；[错误](../../../runs/dsv4flash-db-first-full-01/dacomp-015/attempt-01/python/P9.stderr)。检出需人工核验的 SQL 可实现操作：groupby(；不能仅凭理由判为合规。

## 优化机会

已验证候选。筛选限于精确 SQL、相同自包含 CTE、相同单表完整过滤、可分解单表聚合；未覆盖任意 Join 等价和一般谓词蕴含。全部候选都是 offline，未测在线预测。

| 候选 | 类型 | 已有结果 | 覆盖 SQL | 后续次数 | 中间行数 | 验证 | 成本 |
| --- | --- | --- | --- | --- | --- | --- | --- |
| C1 | exact-result reuse | True | ["S9", "S17"] | 1 | unknown | not_verified_cap | Not tested |
| C2 | exact-result reuse | True | ["S13", "S15"] | 1 | unknown | not_verified_cap | Not tested |
| C3 | exact-result reuse | True | ["S22", "S23"] | 1 | 29975 | verified | Not benchmarked; correctness alone does not establish net speedup. |
| C4 | aggregate MV | False | ["S4", "S9", "S10", "S11", "S12", "S13", "S15", "S17", "S18", "S19", "S28", "S29"] | 11 | 17452 | rejected_result_mismatch | Not benchmarked; correctness alone does not establish net speedup. |
| C5 | common filtered view | False | ["S24", "S25", "S26"] | 2 | 29972 | verified | Not benchmarked; correctness alone does not establish net speedup. |


已验证覆盖（含触发查询、候选并集去重）：5/27 条成功数据 SQL。正确性仅针对当前数据库快照；未测性能的候选不能声称已加速。

[完整 build/rewrite 与比较证据](dacomp-015.analysis.json)。

### C5：common filtered view

Same single source and complete filter; original filter retained.

原查询 [S24](#s24), [S25](#s25), [S26](#s26) → 新增共享状态 C5 → 后续 2 次可复用。该构建点为事后假设，不代表 Agent 当时预知后续。

构建定义：

```sql
SELECT * FROM "data" WHERE NOT "Floor Plan" IS NULL AND NOT decoration IS NULL AND NOT floor IS NULL AND NOT orientation IS NULL
```

受益查询 S24 的改写示例：

```sql
SELECT "Floor Plan", Decoration, Floor, Orientation, COUNT(*) AS cnt, AVG("Watch Count") AS avg_watch_count, SUM("Watch Count") AS total_watch_count, MAX("Watch Count") AS max_watch_count FROM temp.reuse_candidate AS data WHERE NOT "Floor Plan" IS NULL AND NOT Decoration IS NULL AND NOT Floor IS NULL AND NOT Orientation IS NULL GROUP BY "Floor Plan", Decoration, Floor, Orientation HAVING cnt >= 5 ORDER BY avg_watch_count DESC LIMIT 10
```

| 原 SQL | 列名一致 | 结果一致 | 比较方法 |
| --- | --- | --- | --- |
| S24 | True | True | ordered_numeric_tolerance |
| S25 | True | True | ordered_numeric_tolerance |
| S26 | True | True | ordered_numeric_tolerance |


验证状态：verified；成本结论：Not benchmarked; correctness alone does not establish net speedup.

### C3：exact-result reuse

Identical normalized SQL and parameters; archive equality checked.

原查询 [S22](#s22), [S23](#s23) → 保留前序结果 S22 → 后续 1 次可复用。该构建点为事后假设，不代表 Agent 当时预知后续。

| 原 SQL | 列名一致 | 结果一致 | 比较方法 |
| --- | --- | --- | --- |
| S23 | True | True | exact_multiset |


验证状态：verified；成本结论：Not benchmarked; correctness alone does not establish net speedup.

### C4：aggregate MV

Union of grouping keys; decomposable aggregate states; AVG uses SUM and non-NULL COUNT.

原查询 [S4](#s4), [S9](#s9), [S10](#s10), [S11](#s11), [S12](#s12), [S13](#s13), [S15](#s15), [S17](#s17), [S18](#s18), [S19](#s19), [S28](#s28), [S29](#s29) → 新增共享状态 C4 → 后续 11 次可复用。该构建点为事后假设，不代表 Agent 当时预知后续。

构建定义：

```sql
SELECT "Floor Plan" AS __g0, floor AS __g1, decoration AS __g2, orientation AS __g3, "Watch Count" AS __g4, featured AS __g5, "Date Published" AS __g6, COUNT(*) AS __a0, SUM(CASE WHEN "Watch Count" > 0 THEN 1 ELSE 0 END) AS __a1, SUM(CASE WHEN "Watch Count" = 0 THEN 1 ELSE 0 END) AS __a2, SUM(CASE WHEN "Watch Count" > 50 THEN 1 ELSE 0 END) AS __a3, SUM(CASE WHEN "Showings" > 0 THEN 1 ELSE 0 END) AS __a4, SUM(CASE WHEN "Showings" = 0 THEN 1 ELSE 0 END) AS __a5, SUM(CASE WHEN "Showings" > 10 THEN 1 ELSE 0 END) AS __a6, SUM("Watch Count") AS __a7_sum, COUNT("Watch Count") AS __a7_n, SUM(showings) AS __a8_sum, COUNT(showings) AS __a8_n, MAX("Watch Count") AS __a9, MAX(showings) AS __a10, MIN("Watch Count") AS __a11, MIN(showings) AS __a12 FROM "data"  GROUP BY "Floor Plan", floor, decoration, orientation, "Watch Count", featured, "Date Published"
```

受益查询 S4 的改写示例：

```sql
SELECT SUM(__a0) FROM temp.reuse_candidate
```

| 原 SQL | 列名一致 | 结果一致 | 比较方法 |
| --- | --- | --- | --- |
| S4 | False | True | exact_multiset |
| S9 | True | True | ordered_numeric_tolerance |
| S10 | True | True | ordered_numeric_tolerance |
| S11 | True | True | ordered_numeric_tolerance |
| S12 | True | True | ordered_numeric_tolerance |
| S13 | True | True | ordered_numeric_tolerance |
| S15 | True | True | ordered_numeric_tolerance |
| S17 | True | True | ordered_numeric_tolerance |
| S18 | True | True | exact_multiset |
| S19 | True | True | ordered_numeric_tolerance |
| S28 | True | True | exact_multiset |
| S29 | True | True | ordered_numeric_tolerance |


验证状态：rejected_result_mismatch；成本结论：Not benchmarked; correctness alone does not establish net speedup.

结果依赖：自动记录 SQL→Python 的接口父调用，以及源码中引用归档文件的消费者；字面值相同不认定因果。模型方向选择需要人工读取消息，尚未做全面因果标注。

[原始报告](../../../runs/dsv4flash-db-first-full-01/dacomp-015/attempt-01/answer.md)；[统一消息](../../../runs/dsv4flash-db-first-full-01/dacomp-015/attempt-01/messages.jsonl)；[原始 OpenCode 事件](../../../runs/dsv4flash-db-first-full-01/dacomp-015/attempt-01/opencode.jsonl)；[SQL 引擎日志](../../../runs/dsv4flash-db-first-full-01/dacomp-015/attempt-01/sql_journal.jsonl)。

[可读报告（本地图片链接规范化）](../answers/dacomp-015.md)。原始回答保留，分析结论未改写。

## S1

类别 `connection_setup`；来源 `connection`；调用 `6ba0e8532a6e46eab9ea066bafcba7ed`；状态 `success`。

```sql
PRAGMA query_only=ON
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-015/attempt-01/sql/S1.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-015/attempt-01/sql/S1.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-015/attempt-01/results/S1.rows.jsonl)；完整：True；SHA256：`e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`。

## S2

类别 `metadata`；来源 `list_db`；调用 `6ba0e8532a6e46eab9ea066bafcba7ed`；状态 `success`。

```sql
SELECT name,sql FROM sqlite_master WHERE type='table' ORDER BY name
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-015/attempt-01/sql/S2.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-015/attempt-01/sql/S2.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-015/attempt-01/results/S2.rows.jsonl)；完整：True；SHA256：`e3493737ef63dce91cabef5a4a20728c1b7f86e62fe5e92de587961efa5e5790`。

## S3

类别 `data`；来源 `query_db`；调用 `9276c2be6e224f9dbe1f837e4030f93d`；状态 `success`。

```sql
SELECT * FROM data LIMIT 10
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-015/attempt-01/sql/S3.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-015/attempt-01/sql/S3.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-015/attempt-01/results/S3.rows.jsonl)；完整：True；SHA256：`eff2e27ac0e256da8a62e9bbae8773858bc0f4a1436be0429e7a32ba1727c83e`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "data", "kind": "base", "block": null, "base_tables": ["data"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |


## S4

类别 `data`；来源 `query_db`；调用 `c5a1c771988e4d15974205f9d193a98c`；状态 `success`。

```sql
SELECT COUNT(*) FROM data
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-015/attempt-01/sql/S4.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-015/attempt-01/sql/S4.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-015/attempt-01/results/S4.rows.jsonl)；完整：True；SHA256：`56fd430cc1a8b279b29857e7fe1b96a7886c1f2d4c6cd2b5cf5903e3b24019f3`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "data", "kind": "base", "block": null, "base_tables": ["data"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |


## S5

类别 `data`；来源 `query_db`；调用 `0343cbbf78b549c38975081bf482dda2`；状态 `success`。

```sql
SELECT DISTINCT "Floor Plan" FROM data ORDER BY "Floor Plan"
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-015/attempt-01/sql/S5.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-015/attempt-01/sql/S5.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-015/attempt-01/results/S5.rows.jsonl)；完整：True；SHA256：`f31c1fb66a9ee143c09348c67823c66668f5f593ad25525775382a468a4d6242`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "data", "kind": "base", "block": null, "base_tables": ["data"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |


## S6

类别 `data`；来源 `query_db`；调用 `e162ad50367a4158b40162ac31e4ee9c`；状态 `success`。

```sql
SELECT DISTINCT Decoration FROM data ORDER BY Decoration
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-015/attempt-01/sql/S6.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-015/attempt-01/sql/S6.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-015/attempt-01/results/S6.rows.jsonl)；完整：True；SHA256：`24e202f50033fff85f74250977b6ab5a35b9d48e6439722e4c15d11e24568403`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "data", "kind": "base", "block": null, "base_tables": ["data"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |


## S7

类别 `data`；来源 `query_db`；调用 `5d8a8a0281d14f6eac16582b06e5d568`；状态 `success`。

```sql
SELECT DISTINCT Floor FROM data ORDER BY Floor
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-015/attempt-01/sql/S7.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-015/attempt-01/sql/S7.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-015/attempt-01/results/S7.rows.jsonl)；完整：True；SHA256：`562fe2ea77db3aec71c835d0a85eba7885953119d65e6efd2410ca76d9d5c447`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "data", "kind": "base", "block": null, "base_tables": ["data"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |


## S8

类别 `data`；来源 `query_db`；调用 `02ace76440794e14933fbed4fd9d9c87`；状态 `success`。

```sql
SELECT DISTINCT Orientation FROM data ORDER BY Orientation
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-015/attempt-01/sql/S8.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-015/attempt-01/sql/S8.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-015/attempt-01/results/S8.rows.jsonl)；完整：True；SHA256：`e91b4f3458c3afe13c2362c464cb409525e3205be6272bd577f6d0821d79e25e`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "data", "kind": "base", "block": null, "base_tables": ["data"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |


## S9

类别 `data`；来源 `query_db`；调用 `a0c46afd2626444d94ad10b25a92bef7`；状态 `success`。

```sql
SELECT "Floor Plan", COUNT(*) AS cnt FROM data GROUP BY "Floor Plan" ORDER BY cnt DESC
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-015/attempt-01/sql/S9.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-015/attempt-01/sql/S9.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-015/attempt-01/results/S9.rows.jsonl)；完整：True；SHA256：`0c83b4270f65d2410be703a396244182935d3b28a28fce6852a7e7d5ee1f50e6`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "data", "kind": "base", "block": null, "base_tables": ["data"]}] | [] | ["\"Floor Plan\""] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |


## S10

类别 `data`；来源 `query_db`；调用 `ec9fc40a981a4dbc8fc8b3a1e5fff135`；状态 `success`。

```sql
SELECT Floor, COUNT(*) AS cnt FROM data GROUP BY Floor ORDER BY cnt DESC
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-015/attempt-01/sql/S10.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-015/attempt-01/sql/S10.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-015/attempt-01/results/S10.rows.jsonl)；完整：True；SHA256：`615e3daf326a5b8971d4d3a4b74bea4dc6e0420ba8643522b1238beda0c7a523`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "data", "kind": "base", "block": null, "base_tables": ["data"]}] | [] | ["Floor"] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |


## S11

类别 `data`；来源 `query_db`；调用 `06e5f1d70a7f40189df3e67c8b828463`；状态 `success`。

```sql
SELECT Decoration, COUNT(*) AS cnt FROM data GROUP BY Decoration ORDER BY cnt DESC
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-015/attempt-01/sql/S11.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-015/attempt-01/sql/S11.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-015/attempt-01/results/S11.rows.jsonl)；完整：True；SHA256：`062aaa343a31bae3f588b74e91665a066addededf1647c5faf8039db02a08945`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "data", "kind": "base", "block": null, "base_tables": ["data"]}] | [] | ["Decoration"] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |


## S12

类别 `data`；来源 `query_db`；调用 `68368ceb39da467cb12c2e585b7c8199`；状态 `success`。

```sql
SELECT Orientation, COUNT(*) AS cnt FROM data GROUP BY Orientation ORDER BY cnt DESC
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-015/attempt-01/sql/S12.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-015/attempt-01/sql/S12.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-015/attempt-01/results/S12.rows.jsonl)；完整：True；SHA256：`0ce6252d94d85f866d7d54fef8b26080e664ed180ea8c21a61ba71d35f4ef6b3`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "data", "kind": "base", "block": null, "base_tables": ["data"]}] | [] | ["Orientation"] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |


## S13

类别 `data`；来源 `query_db`；调用 `8d46f0b24bca4373aed7a98ce33054bc`；状态 `success`。

```sql
SELECT Floor, COUNT(*) AS cnt FROM data GROUP BY Floor ORDER BY Floor
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-015/attempt-01/sql/S13.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-015/attempt-01/sql/S13.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-015/attempt-01/results/S13.rows.jsonl)；完整：True；SHA256：`5cb5b6194c14d0e9ee62ec9ff3881fb5c65e27e287599e5f55035e6177f0a4bc`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "data", "kind": "base", "block": null, "base_tables": ["data"]}] | [] | ["Floor"] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |


## S14

类别 `data`；来源 `query_db`；调用 `73e98589b4284200b1225b34130b8969`；状态 `success`。

```sql
SELECT Floor, COUNT(*) AS cnt FROM data WHERE Floor LIKE '%story%' OR Floor LIKE '%floors%' OR Floor LIKE '%floor building%' GROUP BY Floor ORDER BY cnt DESC
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-015/attempt-01/sql/S14.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-015/attempt-01/sql/S14.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-015/attempt-01/results/S14.rows.jsonl)；完整：True；SHA256：`53465579c76b7f2b864d4ced639bc2cc976fc69f0999c71ee931c2146abe86cf`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "data", "kind": "base", "block": null, "base_tables": ["data"]}] | [] | ["Floor"] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |


## S15

类别 `data`；来源 `query_db`；调用 `66c978dc22ce45e08eba449ebe03f4f5`；状态 `success`。

```sql
SELECT Floor, COUNT(*) AS cnt FROM data GROUP BY Floor ORDER BY Floor
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-015/attempt-01/sql/S15.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-015/attempt-01/sql/S15.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-015/attempt-01/results/S15.rows.jsonl)；完整：True；SHA256：`5cb5b6194c14d0e9ee62ec9ff3881fb5c65e27e287599e5f55035e6177f0a4bc`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "data", "kind": "base", "block": null, "base_tables": ["data"]}] | [] | ["Floor"] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |


## S16

类别 `data`；来源 `query_db`；调用 `9e601295195d4a25ad367a0a1b93ff9c`；状态 `success`。

```sql
SELECT GROUP_CONCAT(Floor, ' | ') AS all_floors FROM (SELECT DISTINCT Floor FROM data ORDER BY Floor)
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-015/attempt-01/sql/S16.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-015/attempt-01/sql/S16.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-015/attempt-01/results/S16.rows.jsonl)；完整：True；SHA256：`11e7f4c81c39e529fe256560e60c4c66a7cb0224a076cf3adac4a550ac3c8d9a`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "data", "kind": "base", "block": null, "base_tables": ["data"]}] | [] | [] |
| B2 | [{"alias": "", "kind": "derived", "block": "B1", "base_tables": ["data"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B2 | GROUP_CONCAT(Floor, ' \| ') | [{"table": "data", "column": "Floor"}] | [] | False |


## S17

类别 `data`；来源 `query_db`；调用 `8dd3c40910014a7b864e07aa97384e40`；状态 `success`。

```sql
SELECT "Floor Plan", COUNT(*) AS cnt FROM data GROUP BY "Floor Plan" ORDER BY cnt DESC
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-015/attempt-01/sql/S17.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-015/attempt-01/sql/S17.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-015/attempt-01/results/S17.rows.jsonl)；完整：True；SHA256：`0c83b4270f65d2410be703a396244182935d3b28a28fce6852a7e7d5ee1f50e6`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "data", "kind": "base", "block": null, "base_tables": ["data"]}] | [] | ["\"Floor Plan\""] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |


## S18

类别 `data`；来源 `query_db`；调用 `a7358958be534335a25b8a275a6ff893`；状态 `success`。

```sql
SELECT COUNT(*) AS total,
  SUM(CASE WHEN "Watch Count" > 0 THEN 1 ELSE 0 END) AS watch_gt0,
  SUM(CASE WHEN "Watch Count" = 0 THEN 1 ELSE 0 END) AS watch_eq0,
  SUM(CASE WHEN "Watch Count" > 50 THEN 1 ELSE 0 END) AS watch_gt50,
  SUM(CASE WHEN "Showings" > 0 THEN 1 ELSE 0 END) AS show_gt0,
  SUM(CASE WHEN "Showings" = 0 THEN 1 ELSE 0 END) AS show_eq0,
  SUM(CASE WHEN "Showings" > 10 THEN 1 ELSE 0 END) AS show_gt10,
  AVG("Watch Count") AS avg_watch, AVG(Showings) AS avg_show,
  MAX("Watch Count") AS max_watch, MAX(Showings) AS max_show,
  MIN("Watch Count") AS min_watch, MIN(Showings) AS min_show
FROM data
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-015/attempt-01/sql/S18.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-015/attempt-01/sql/S18.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-015/attempt-01/results/S18.rows.jsonl)；完整：True；SHA256：`ade05527d0808eb30eb562760150f2181ca33eaa9e44b04fea106bea1bd83b90`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "data", "kind": "base", "block": null, "base_tables": ["data"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |
| B1 | SUM(CASE WHEN "Watch Count" > 0 THEN 1 ELSE 0 END) | [] | [{"table": "data", "column": "Watch Count"}] | False |
| B1 | SUM(CASE WHEN "Watch Count" = 0 THEN 1 ELSE 0 END) | [] | [{"table": "data", "column": "Watch Count"}] | False |
| B1 | SUM(CASE WHEN "Watch Count" > 50 THEN 1 ELSE 0 END) | [] | [{"table": "data", "column": "Watch Count"}] | False |
| B1 | SUM(CASE WHEN "Showings" > 0 THEN 1 ELSE 0 END) | [] | [{"table": "data", "column": "Showings"}] | False |
| B1 | SUM(CASE WHEN "Showings" = 0 THEN 1 ELSE 0 END) | [] | [{"table": "data", "column": "Showings"}] | False |
| B1 | SUM(CASE WHEN "Showings" > 10 THEN 1 ELSE 0 END) | [] | [{"table": "data", "column": "Showings"}] | False |
| B1 | AVG("Watch Count") | [{"table": "data", "column": "Watch Count"}] | [] | False |
| B1 | AVG(Showings) | [{"table": "data", "column": "Showings"}] | [] | False |
| B1 | MAX("Watch Count") | [{"table": "data", "column": "Watch Count"}] | [] | False |
| B1 | MAX(Showings) | [{"table": "data", "column": "Showings"}] | [] | False |
| B1 | MIN("Watch Count") | [{"table": "data", "column": "Watch Count"}] | [] | False |
| B1 | MIN(Showings) | [{"table": "data", "column": "Showings"}] | [] | False |


## S19

类别 `data`；来源 `query_db`；调用 `3ef7b3c5606542f7b689ce620febe41f`；状态 `success`。

```sql
SELECT "Watch Count", COUNT(*) AS cnt FROM data GROUP BY "Watch Count" ORDER BY "Watch Count" DESC LIMIT 20
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-015/attempt-01/sql/S19.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-015/attempt-01/sql/S19.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-015/attempt-01/results/S19.rows.jsonl)；完整：True；SHA256：`def1f5128ad15778c97b07b7aed103d451603be363a750627ac98a5f3609c1b1`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "data", "kind": "base", "block": null, "base_tables": ["data"]}] | [] | ["\"Watch Count\""] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |


## S20

类别 `data`；来源 `query_db`；调用 `d3868327eda64691abbd9f3941f9f4c6`；状态 `success`。

```sql
SELECT DISTINCT Floor FROM data WHERE Floor LIKE '%th floor%' OR Floor LIKE '%st floor%' OR Floor LIKE '%nd floor%' OR Floor LIKE '%rd floor%' OR Floor LIKE 'Floor %'
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-015/attempt-01/sql/S20.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-015/attempt-01/sql/S20.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-015/attempt-01/results/S20.rows.jsonl)；完整：True；SHA256：`57edb33efa1ed67dfefa07e13db98201465928932d8305fcf1d2f88e3326d562`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "data", "kind": "base", "block": null, "base_tables": ["data"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |


## S21

类别 `data`；来源 `query_db`；调用 `b037c1b0a2574cc9a5db5fc8c3ed4cb8`；状态 `success`。

```sql
SELECT DISTINCT Floor FROM data WHERE Floor LIKE '%floors%' OR Floor LIKE '%story%' OR Floor LIKE '%Floors%'
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-015/attempt-01/sql/S21.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-015/attempt-01/sql/S21.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-015/attempt-01/results/S21.rows.jsonl)；完整：True；SHA256：`46702ee9dce2cd6602c16f8fc8ad0777ca1d5855351a3f65646578901db4b4be`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "data", "kind": "base", "block": null, "base_tables": ["data"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |


## S22

类别 `data`；来源 `python`；调用 `e6f911fc31b9497ba03df129f64e9d97`；状态 `success`。

```sql
SELECT * FROM data
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-015/attempt-01/sql/S22.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-015/attempt-01/sql/S22.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-015/attempt-01/results/S22.rows.jsonl)；完整：True；SHA256：`5743f0583802dfba3d55e2f32c574be17079ba3199d058032da60367cad8d996`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "data", "kind": "base", "block": null, "base_tables": ["data"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |


## S23

类别 `data`；来源 `python`；调用 `b32aa753312542ecb0615c09fbe40b90`；状态 `success`。

```sql
SELECT * FROM data
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-015/attempt-01/sql/S23.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-015/attempt-01/sql/S23.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-015/attempt-01/results/S23.rows.jsonl)；完整：True；SHA256：`5743f0583802dfba3d55e2f32c574be17079ba3199d058032da60367cad8d996`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "data", "kind": "base", "block": null, "base_tables": ["data"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |


## S24

类别 `data`；来源 `query_db`；调用 `b523b79c1870404993e7e5916be905fd`；状态 `success`。

```sql
SELECT "Floor Plan", Decoration, Floor, Orientation, 
  COUNT(*) AS cnt,
  AVG("Watch Count") AS avg_watch_count,
  SUM("Watch Count") AS total_watch_count,
  MAX("Watch Count") AS max_watch_count
FROM data
WHERE "Floor Plan" IS NOT NULL 
  AND Decoration IS NOT NULL 
  AND Floor IS NOT NULL 
  AND Orientation IS NOT NULL
GROUP BY "Floor Plan", Decoration, Floor, Orientation
HAVING cnt >= 5
ORDER BY avg_watch_count DESC
LIMIT 10
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-015/attempt-01/sql/S24.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-015/attempt-01/sql/S24.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-015/attempt-01/results/S24.rows.jsonl)；完整：True；SHA256：`f0343159b68d33946ce43d1c0571900efeec12e7c59d919945163efcd4f65e50`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "data", "kind": "base", "block": null, "base_tables": ["data"]}] | [] | ["\"Floor Plan\"", "Decoration", "Floor", "Orientation"] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |
| B1 | AVG("Watch Count") | [{"table": "data", "column": "Watch Count"}] | [] | False |
| B1 | SUM("Watch Count") | [{"table": "data", "column": "Watch Count"}] | [] | False |
| B1 | MAX("Watch Count") | [{"table": "data", "column": "Watch Count"}] | [] | False |


## S25

类别 `data`；来源 `query_db`；调用 `48a70c40c1be4b19a993cbbfeefcd79a`；状态 `success`。

```sql
SELECT "Floor Plan", Decoration, Floor, Orientation, 
  COUNT(*) AS cnt,
  AVG("Watch Count") AS avg_watch_count,
  SUM("Watch Count") AS total_watch_count,
  MAX("Watch Count") AS max_watch_count
FROM data
WHERE "Floor Plan" IS NOT NULL 
  AND Decoration IS NOT NULL 
  AND Floor IS NOT NULL 
  AND Orientation IS NOT NULL
GROUP BY "Floor Plan", Decoration, Floor, Orientation
HAVING cnt >= 3
ORDER BY avg_watch_count DESC
LIMIT 10
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-015/attempt-01/sql/S25.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-015/attempt-01/sql/S25.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-015/attempt-01/results/S25.rows.jsonl)；完整：True；SHA256：`884798f1c2a3e342d97d3d3230d3fc939ef94f6bc69cbd493ae09dfbfd9f14dd`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "data", "kind": "base", "block": null, "base_tables": ["data"]}] | [] | ["\"Floor Plan\"", "Decoration", "Floor", "Orientation"] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |
| B1 | AVG("Watch Count") | [{"table": "data", "column": "Watch Count"}] | [] | False |
| B1 | SUM("Watch Count") | [{"table": "data", "column": "Watch Count"}] | [] | False |
| B1 | MAX("Watch Count") | [{"table": "data", "column": "Watch Count"}] | [] | False |


## S26

类别 `data`；来源 `query_db`；调用 `3c9297442ff74b32b3163fad1bace84b`；状态 `success`。

```sql
SELECT "Floor Plan", Decoration, Floor, Orientation, 
  COUNT(*) AS cnt,
  ROUND(AVG("Watch Count"),1) AS avg_watch,
  MAX("Watch Count") AS max_watch,
  SUM(CASE WHEN "Watch Count" >= 20 THEN 1 ELSE 0 END) AS n_ge20
FROM data
WHERE "Floor Plan" IS NOT NULL AND Decoration IS NOT NULL AND Floor IS NOT NULL AND Orientation IS NOT NULL
GROUP BY "Floor Plan", Decoration, Floor, Orientation
HAVING cnt >= 5
ORDER BY avg_watch DESC
LIMIT 25
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-015/attempt-01/sql/S26.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-015/attempt-01/sql/S26.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-015/attempt-01/results/S26.rows.jsonl)；完整：True；SHA256：`1289644e62e68cfec688780e12caf7598e8cfd72580d13822089e927d10389be`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "data", "kind": "base", "block": null, "base_tables": ["data"]}] | [] | ["\"Floor Plan\"", "Decoration", "Floor", "Orientation"] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |
| B1 | MAX("Watch Count") | [{"table": "data", "column": "Watch Count"}] | [] | False |
| B1 | SUM(CASE WHEN "Watch Count" >= 20 THEN 1 ELSE 0 END) | [] | [{"table": "data", "column": "Watch Count"}] | False |
| B1 | AVG("Watch Count") | [{"table": "data", "column": "Watch Count"}] | [] | False |


## S27

类别 `data`；来源 `query_db`；调用 `a23383b689dd49769bffa3a14a43e350`；状态 `success`。

```sql
SELECT "Floor Plan", Decoration, Floor, Orientation, "Watch Count", Showings
FROM data
WHERE "Floor Plan" = '4 bedrooms, 2 living rooms' AND Decoration = 'High-quality renovation' AND Floor = '18th floor' AND Orientation = 'North'
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-015/attempt-01/sql/S27.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-015/attempt-01/sql/S27.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-015/attempt-01/results/S27.rows.jsonl)；完整：True；SHA256：`d0d189b60e34043b112f756e5f9ee13ee70c0348f90f4c01938f72f2ea5078e7`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "data", "kind": "base", "block": null, "base_tables": ["data"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |


## S28

类别 `data`；来源 `query_db`；调用 `e00f36535b6441b3b328b2902052bf44`；状态 `success`。

```sql
SELECT Featured, COUNT(*) AS cnt, AVG("Watch Count") AS avg_watch, AVG(Showings) AS avg_show FROM data GROUP BY Featured
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-015/attempt-01/sql/S28.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-015/attempt-01/sql/S28.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-015/attempt-01/results/S28.rows.jsonl)；完整：True；SHA256：`a0dde3822a4d9b8db8677134806ab658b4ed4a857303c4514326ed7d883d3bf4`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "data", "kind": "base", "block": null, "base_tables": ["data"]}] | [] | ["Featured"] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |
| B1 | AVG("Watch Count") | [{"table": "data", "column": "Watch Count"}] | [] | False |
| B1 | AVG(Showings) | [{"table": "data", "column": "Showings"}] | [] | False |


## S29

类别 `data`；来源 `query_db`；调用 `d4466bdfd1b9478da6806e17d0927574`；状态 `success`。

```sql
SELECT "Date Published", COUNT(*) AS cnt, AVG("Watch Count") AS avg_watch, AVG(Showings) AS avg_show FROM data GROUP BY "Date Published" ORDER BY cnt DESC
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-015/attempt-01/sql/S29.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-015/attempt-01/sql/S29.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-015/attempt-01/results/S29.rows.jsonl)；完整：True；SHA256：`c335e1b816dba12913afe76467f07a3afedcb848c836e1726fa8ae1b5928bf5c`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "data", "kind": "base", "block": null, "base_tables": ["data"]}] | [] | ["\"Date Published\""] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |
| B1 | AVG("Watch Count") | [{"table": "data", "column": "Watch Count"}] | [] | False |
| B1 | AVG(Showings) | [{"table": "data", "column": "Showings"}] | [] | False |

