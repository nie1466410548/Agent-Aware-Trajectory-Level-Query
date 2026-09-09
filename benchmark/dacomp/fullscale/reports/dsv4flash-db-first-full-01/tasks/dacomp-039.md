# dacomp-039

For levels launched in 2024, compare how Churn Rate and Level Rating change across combina…

运行：已提交。官方未评分。全部 SQL 尝试/成功 29/27；数据 SQL 27/25；Python 9 次。

完整原题：

For levels launched in 2024, compare how Churn Rate and Level Rating change across combinations of Difficulty Level and Level Type. How can we use these patterns to optimize levels?

| 表 | 行数 | 列数 |
| --- | --- | --- |
| game_game_level_content_data_ta | 6379 | 15 |


实际路线（分析者依据 SQL/源码概括，不代表 Agent 自述）：筛选 2024 年上线关卡 → 按难度与类型比较流失和评分 → Python 方差分解、回归与检验 → 绘制组合摘要和分布。

数据库大小：1,634,304 字节。

## 数据 SQL

| SQL | 状态 | 基础表 | Join 输入/类型 | GROUP BY | 聚合表达式 | 结果行数 | 数据库 ms |
| --- | --- | --- | --- | --- | --- | --- | --- |
| [S3/Q1](#s3) | success | ["game_game_level_content_data_ta"] | 0 / {} | [] | [] | 4 | 2.908 |
| [S4/Q2](#s4) | success | ["game_game_level_content_data_ta"] | 0 / {} | [] | [] | 5 | 2.479 |
| [S5/Q3](#s5) | success | ["game_game_level_content_data_ta"] | 0 / {} | [] | ["MIN(\"Launch Time\")", "MAX(\"Launch Time\")"] | 1 | 1.552 |
| [S6/Q4](#s6) | success | ["game_game_level_content_data_ta"] | 0 / {} | [] | ["COUNT(*)"] | 1 | 4.471 |
| [S7/Q5](#s7) | success | ["game_game_level_content_data_ta"] | 0 / {} | ["\"Difficulty Level\"", "\"Level Type\""] | ["COUNT(*)", "AVG(\"Churn Rate\")", "AVG(\"Level Rating\")", "AVG(\"Clear Rate\")", "AVG(\"Average Retry Count\")"] | 16 | 5.22 |
| [S8/Q6](#s8) | success | ["game_game_level_content_data_ta"] | 0 / {} | ["\"Difficulty Level\""] | ["COUNT(*)", "AVG(\"Churn Rate\")", "AVG(\"Level Rating\")"] | 4 | 4.06 |
| [S9/Q7](#s9) | success | ["game_game_level_content_data_ta"] | 0 / {} | ["\"Level Type\""] | ["COUNT(*)", "AVG(\"Churn Rate\")", "AVG(\"Level Rating\")"] | 5 | 4.041 |
| [S10/Q8](#s10) | failed | ["game_game_level_content_data_ta"] | 0 / {} | [] | ["CORR(\"Churn Rate\", \"Level Rating\")", "CORR(\"Churn Rate\", \"Clear Rate\")", "CORR(\"Level Rating\", \"Clear Rate\")", "CORR(\"Churn Rate\", \"Average Retry Count\")"] | unknown | 未取得；调用总时长 0.163 ms |
| [S11/Q9](#s11) | success | ["game_game_level_content_data_ta"] | 0 / {} | [] | [] | 3142 | 12.467 |
| [S12/Q10](#s12) | failed | ["game_game_level_content_data_ta"] | 0 / {} | ["\"Difficulty Level\"", "\"Level Type\""] | ["COUNT(*)", "AVG(\"Churn Rate\")", "STDDEV(\"Churn Rate\")", "AVG(\"Level Rating\")", "STDDEV(\"Level Rating\")", "AVG(\"Clear Rate\")", "AVG(\"Average Retry Count\")"] | unknown | 未取得；调用总时长 0.183 ms |
| [S13/Q11](#s13) | success | ["game_game_level_content_data_ta"] | 0 / {} | [] | [] | 3142 | 12.1 |
| [S14/Q12](#s14) | success | ["game_game_level_content_data_ta"] | 0 / {} | [] | [] | 3142 | 12.024 |
| [S15/Q13](#s15) | success | ["game_game_level_content_data_ta"] | 0 / {} | [] | [] | 3142 | 12.01 |
| [S16/Q14](#s16) | success | ["game_game_level_content_data_ta"] | 0 / {} | ["\"Difficulty Level\""] | ["COUNT(*)", "MIN(\"Churn Rate\")", "AVG(\"Churn Rate\")", "MAX(\"Churn Rate\")", "AVG(\"Level Rating\")", "AVG(\"Clear Rate\")", "AVG(\"Average Retry Count\")", "AVG(\"Level Completion Rate\")"] | 4 | 5.179 |
| [S17/Q15](#s17) | success | ["game_game_level_content_data_ta"] | 0 / {} | ["STRFTIME('%Y-%m', \"Launch Time\")"] | ["COUNT(*)", "AVG(\"Churn Rate\")", "AVG(\"Level Rating\")"] | 12 | 5.233 |
| [S18/Q16](#s18) | success | ["game_game_level_content_data_ta"] | 0 / {} | ["\"Reward Type\""] | ["COUNT(*)", "AVG(\"Churn Rate\")", "AVG(\"Level Rating\")"] | 4 | 4.352 |
| [S19/Q17](#s19) | success | ["game_game_level_content_data_ta"] | 2 / {'INNER': 1} | ["\"Difficulty Level\"", "\"Difficulty Level\"", "\"Level Type\""] | ["AVG(\"Churn Rate\")", "AVG(\"Level Rating\")", "COUNT(*)", "AVG(\"Churn Rate\")", "AVG(\"Level Rating\")"] | 16 | 9.456 |
| [S20/Q18](#s20) | success | ["game_game_level_content_data_ta"] | 0 / {} | ["\"Difficulty Level\"", "\"Reward Type\""] | ["COUNT(*)"] | 16 | 4.795 |
| [S21/Q19](#s21) | success | ["game_game_level_content_data_ta"] | 0 / {} | ["\"Difficulty Level\""] | ["MIN(\"Reward Value\")", "MAX(\"Reward Value\")", "AVG(\"Reward Value\")"] | 4 | 4.449 |
| [S22/Q20](#s22) | success | ["game_game_level_content_data_ta"] | 0 / {} | [] | [] | 3142 | 15.088 |
| [S23/Q21](#s23) | success | ["game_game_level_content_data_ta"] | 0 / {} | [] | [] | 3142 | 12.121 |
| [S24/Q22](#s24) | success | ["game_game_level_content_data_ta"] | 0 / {} | ["\"Difficulty Level\"", "\"Level Type\""] | ["COUNT(*)", "AVG(\"Churn Rate\")", "AVG(\"Level Rating\")"] | 17 | 5.612 |
| [S25/Q23](#s25) | success | ["game_game_level_content_data_ta"] | 0 / {} | ["STRFTIME('%Y', \"Launch Time\")", "\"Difficulty Level\""] | ["COUNT(*)", "AVG(\"Churn Rate\")", "AVG(\"Level Rating\")"] | 12 | 9.564 |
| [S26/Q24](#s26) | success | ["game_game_level_content_data_ta"] | 0 / {} | [] | [] | 3142 | 12.192 |
| [S27/Q25](#s27) | success | ["game_game_level_content_data_ta"] | 0 / {} | [] | ["MIN(\"Level Completion Rate\" + \"Churn Rate\")", "MAX(\"Level Completion Rate\" + \"Churn Rate\")", "AVG(\"Level Completion Rate\" + \"Churn Rate\")"] | 1 | 3.707 |
| [S28/Q26](#s28) | success | ["game_game_level_content_data_ta"] | 0 / {} | ["STRFTIME('%Y', \"Launch Time\")", "\"Difficulty Level\""] | ["COUNT(*)"] | 12 | 6.613 |
| [S29/Q27](#s29) | success | ["game_game_level_content_data_ta"] | 0 / {} | [] | [] | 3142 | 12.131 |


## 元数据和设置

| SQL | 类别 | 状态 | 内容 |
| --- | --- | --- | --- |
| S1 | connection_setup | success | PRAGMA query_only=ON |
| S2 | metadata | success | SELECT name,sql FROM sqlite_master WHERE type='table' ORDER BY name |


## Python 与执行位置

人工源码审查：**partial_violation**。SQL 筛选 2024 年关卡并汇总部分难度/类型指标。Python 回归、t 检验及方差分解属于统计程序；P8 和其他绘图调用另外用 pandas 重算难度×类型的计数/平均流失率/评分，P9 做难度均值，这些是可在 SQL 完成的绘图前准备，需标为偏离。 [证据](../reviews/dacomp-039.json)。

P1：SQLite lacks a CORR function; need Python to compute Pearson correlations between Churn Rate, Level Rating, Clear Rate, and Retry Count for 2024 data.

[源码](../../../runs/dsv4flash-db-first-full-01/dacomp-039/attempt-01/python/P1.py)；[输出](../../../runs/dsv4flash-db-first-full-01/dacomp-039/attempt-01/python/P1.stdout)；[错误](../../../runs/dsv4flash-db-first-full-01/dacomp-039/attempt-01/python/P1.stderr)。检出需人工核验的 SQL 可实现操作：.query(；不能仅凭理由判为合规。

P2：SQLite lacks STDEV; Python will compute per-group standard deviations and build visualizations comparing Churn Rate and Level Rating across Difficulty x Level Type for 2024.

[源码](../../../runs/dsv4flash-db-first-full-01/dacomp-039/attempt-01/python/P2.py)；[输出](../../../runs/dsv4flash-db-first-full-01/dacomp-039/attempt-01/python/P2.stdout)；[错误](../../../runs/dsv4flash-db-first-full-01/dacomp-039/attempt-01/python/P2.stderr)。检出需人工核验的 SQL 可实现操作：groupby(, .query(, sort_values(；不能仅凭理由判为合规。

P3：Fix the heatmap plotting code that failed due to NaN values in the pivot table for missing combinations.

[源码](../../../runs/dsv4flash-db-first-full-01/dacomp-039/attempt-01/python/P3.py)；[输出](../../../runs/dsv4flash-db-first-full-01/dacomp-039/attempt-01/python/P3.stdout)；[错误](../../../runs/dsv4flash-db-first-full-01/dacomp-039/attempt-01/python/P3.stderr)。检出需人工核验的 SQL 可实现操作：groupby(, .query(, sort_values(；不能仅凭理由判为合规。

P4：The work directory does not exist; create it and rerun figure generation for the 2024 Difficulty x Level Type analysis.

[源码](../../../runs/dsv4flash-db-first-full-01/dacomp-039/attempt-01/python/P4.py)；[输出](../../../runs/dsv4flash-db-first-full-01/dacomp-039/attempt-01/python/P4.stdout)；[错误](../../../runs/dsv4flash-db-first-full-01/dacomp-039/attempt-01/python/P4.stderr)。自动源码筛查未检出预设迁出信号；这不是全面语义合规证明。

P5：Rerun figure generation (heatmaps, scatter, bar charts) for Churn Rate and Level Rating across Difficulty x Level Type for 2024 levels after creating the work directory.

[源码](../../../runs/dsv4flash-db-first-full-01/dacomp-039/attempt-01/python/P5.py)；[输出](../../../runs/dsv4flash-db-first-full-01/dacomp-039/attempt-01/python/P5.stdout)；[错误](../../../runs/dsv4flash-db-first-full-01/dacomp-039/attempt-01/python/P5.stderr)。检出需人工核验的 SQL 可实现操作：groupby(, .query(, sort_values(；不能仅凭理由判为合规。

P6：Compute variance decomposition (ANOVA-like) to quantify how much Churn Rate variance is explained by Difficulty Level vs Level Type, and examine within-difficulty effects of Reward Value, since SQL cannot do these statistical procedures.

[源码](../../../runs/dsv4flash-db-first-full-01/dacomp-039/attempt-01/python/P6.py)；[输出](../../../runs/dsv4flash-db-first-full-01/dacomp-039/attempt-01/python/P6.stdout)；[错误](../../../runs/dsv4flash-db-first-full-01/dacomp-039/attempt-01/python/P6.stderr)。检出需人工核验的 SQL 可实现操作：groupby(, .query(；不能仅凭理由判为合规。

P7：The unbalanced design makes ANOVA SS non-additive; use linear model R2 decomposition instead to quantify how much Churn Rate / Level Rating variance Difficulty and Level Type explain.

[源码](../../../runs/dsv4flash-db-first-full-01/dacomp-039/attempt-01/python/P7.py)；[输出](../../../runs/dsv4flash-db-first-full-01/dacomp-039/attempt-01/python/P7.stdout)；[错误](../../../runs/dsv4flash-db-first-full-01/dacomp-039/attempt-01/python/P7.stderr)。检出需人工核验的 SQL 可实现操作：.query(；不能仅凭理由判为合规。

P8：SQLite lacks correlation functions; compute additional correlations for 2024 (participation, clear time, completion rate) and build a final summary figure of combination performance.

[源码](../../../runs/dsv4flash-db-first-full-01/dacomp-039/attempt-01/python/P8.py)；[输出](../../../runs/dsv4flash-db-first-full-01/dacomp-039/attempt-01/python/P8.stdout)；[错误](../../../runs/dsv4flash-db-first-full-01/dacomp-039/attempt-01/python/P8.stderr)。检出需人工核验的 SQL 可实现操作：groupby(, .query(；不能仅凭理由判为合规。

P9：Generate a final summary figure showing marginal Churn/Rating by Difficulty and the trade-off curve for the 2024 report.

[源码](../../../runs/dsv4flash-db-first-full-01/dacomp-039/attempt-01/python/P9.py)；[输出](../../../runs/dsv4flash-db-first-full-01/dacomp-039/attempt-01/python/P9.stdout)；[错误](../../../runs/dsv4flash-db-first-full-01/dacomp-039/attempt-01/python/P9.stderr)。检出需人工核验的 SQL 可实现操作：groupby(, .query(；不能仅凭理由判为合规。

## 优化机会

已验证候选。筛选限于精确 SQL、相同自包含 CTE、相同单表完整过滤、可分解单表聚合；未覆盖任意 Join 等价和一般谓词蕴含。全部候选都是 offline，未测在线预测。

| 候选 | 类型 | 已有结果 | 覆盖 SQL | 后续次数 | 中间行数 | 验证 | 成本 |
| --- | --- | --- | --- | --- | --- | --- | --- |
| C1 | exact-result reuse | True | ["S11", "S13", "S14", "S15", "S22", "S23", "S26", "S29"] | 7 | 3142 | verified | Not benchmarked; correctness alone does not establish net speedup. |
| C2 | common filtered view | False | ["S6", "S7", "S8", "S9", "S11", "S13", "S14", "S15", "S16", "S17", "S18", "S20", "S21", "S22", "S23", "S26", "S27", "S29"] | 17 | 3142 | verified | Not benchmarked; correctness alone does not establish net speedup. |
| C3 | aggregate MV | False | ["S6", "S7", "S8", "S9", "S16", "S17", "S18", "S20", "S21", "S27"] | 9 | 341 | verified | Not benchmarked; correctness alone does not establish net speedup. |
| C4 | common filtered view | False | ["S25", "S28"] | 1 | unknown | not_verified_cap | Not tested |
| C5 | aggregate MV | False | ["S25", "S28"] | 1 | unknown | not_verified_cap | Not tested |


已验证覆盖（含触发查询、候选并集去重）：18/25 条成功数据 SQL。正确性仅针对当前数据库快照；未测性能的候选不能声称已加速。

[完整 build/rewrite 与比较证据](dacomp-039.analysis.json)。

### C2：common filtered view

Same single source and complete filter; original filter retained.

原查询 [S6](#s6), [S7](#s7), [S8](#s8), [S9](#s9), [S11](#s11), [S13](#s13), [S14](#s14), [S15](#s15), [S16](#s16), [S17](#s17), [S18](#s18), [S20](#s20), [S21](#s21), [S22](#s22), [S23](#s23), [S26](#s26), [S27](#s27), [S29](#s29) → 新增共享状态 C2 → 后续 17 次可复用。该构建点为事后假设，不代表 Agent 当时预知后续。

构建定义：

```sql
SELECT * FROM "game_game_level_content_data_ta" WHERE STRFTIME('%Y', "Launch Time") = '2024'
```

受益查询 S6 的改写示例：

```sql
SELECT COUNT(*) AS total_2024 FROM temp.reuse_candidate AS game_game_level_content_data_ta WHERE STRFTIME('%Y', "Launch Time") = '2024'
```

| 原 SQL | 列名一致 | 结果一致 | 比较方法 |
| --- | --- | --- | --- |
| S6 | True | True | exact_multiset |
| S7 | True | True | ordered_numeric_tolerance |
| S8 | True | True | ordered_numeric_tolerance |
| S9 | True | True | ordered_numeric_tolerance |
| S11 | True | True | exact_multiset |
| S13 | True | True | exact_multiset |
| S14 | True | True | exact_multiset |
| S15 | True | True | exact_multiset |
| S16 | True | True | ordered_numeric_tolerance |
| S17 | True | True | ordered_numeric_tolerance |
| S18 | True | True | ordered_numeric_tolerance |
| S20 | True | True | ordered_numeric_tolerance |
| S21 | True | True | ordered_numeric_tolerance |
| S22 | True | True | exact_multiset |
| S23 | True | True | exact_multiset |
| S26 | True | True | exact_multiset |
| S27 | True | True | exact_multiset |
| S29 | True | True | exact_multiset |


验证状态：verified；成本结论：Not benchmarked; correctness alone does not establish net speedup.

### C3：aggregate MV

Union of grouping keys; decomposable aggregate states; AVG uses SUM and non-NULL COUNT.

原查询 [S6](#s6), [S7](#s7), [S8](#s8), [S9](#s9), [S16](#s16), [S17](#s17), [S18](#s18), [S20](#s20), [S21](#s21), [S27](#s27) → 新增共享状态 C3 → 后续 9 次可复用。该构建点为事后假设，不代表 Agent 当时预知后续。

构建定义：

```sql
SELECT "Difficulty Level" AS __g0, "Level Type" AS __g1, STRFTIME('%Y-%m', "Launch Time") AS __g2, "Reward Type" AS __g3, COUNT(*) AS __a0, SUM("Churn Rate") AS __a1_sum, COUNT("Churn Rate") AS __a1_n, SUM("Level Rating") AS __a2_sum, COUNT("Level Rating") AS __a2_n, SUM("Clear Rate") AS __a3_sum, COUNT("Clear Rate") AS __a3_n, SUM("Average Retry Count") AS __a4_sum, COUNT("Average Retry Count") AS __a4_n, MIN("Churn Rate") AS __a5, MAX("Churn Rate") AS __a6, SUM("Level Completion Rate") AS __a7_sum, COUNT("Level Completion Rate") AS __a7_n, MIN("Reward Value") AS __a8, MAX("Reward Value") AS __a9, SUM("Reward Value") AS __a10_sum, COUNT("Reward Value") AS __a10_n, MIN("Level Completion Rate" + "Churn Rate") AS __a11, MAX("Level Completion Rate" + "Churn Rate") AS __a12, SUM("Level Completion Rate" + "Churn Rate") AS __a13_sum, COUNT("Level Completion Rate" + "Churn Rate") AS __a13_n FROM "game_game_level_content_data_ta" WHERE STRFTIME('%Y', "Launch Time") = '2024' GROUP BY "Difficulty Level", "Level Type", STRFTIME('%Y-%m', "Launch Time"), "Reward Type"
```

受益查询 S6 的改写示例：

```sql
SELECT SUM(__a0) AS total_2024 FROM temp.reuse_candidate
```

| 原 SQL | 列名一致 | 结果一致 | 比较方法 |
| --- | --- | --- | --- |
| S6 | True | True | exact_multiset |
| S7 | True | True | ordered_numeric_tolerance |
| S8 | True | True | ordered_numeric_tolerance |
| S9 | True | True | ordered_numeric_tolerance |
| S16 | True | True | ordered_numeric_tolerance |
| S17 | True | True | ordered_numeric_tolerance |
| S18 | True | True | ordered_numeric_tolerance |
| S20 | True | True | ordered_numeric_tolerance |
| S21 | True | True | ordered_numeric_tolerance |
| S27 | True | True | exact_multiset |


验证状态：verified；成本结论：Not benchmarked; correctness alone does not establish net speedup.

### C1：exact-result reuse

Identical normalized SQL and parameters; archive equality checked.

原查询 [S11](#s11), [S13](#s13), [S14](#s14), [S15](#s15), [S22](#s22), [S23](#s23), [S26](#s26), [S29](#s29) → 保留前序结果 S11 → 后续 7 次可复用。该构建点为事后假设，不代表 Agent 当时预知后续。

| 原 SQL | 列名一致 | 结果一致 | 比较方法 |
| --- | --- | --- | --- |
| S13 | True | True | exact_multiset |
| S14 | True | True | exact_multiset |
| S15 | True | True | exact_multiset |
| S22 | True | True | exact_multiset |
| S23 | True | True | exact_multiset |
| S26 | True | True | exact_multiset |
| S29 | True | True | exact_multiset |


验证状态：verified；成本结论：Not benchmarked; correctness alone does not establish net speedup.

结果依赖：自动记录 SQL→Python 的接口父调用，以及源码中引用归档文件的消费者；字面值相同不认定因果。模型方向选择需要人工读取消息，尚未做全面因果标注。

[原始报告](../../../runs/dsv4flash-db-first-full-01/dacomp-039/attempt-01/answer.md)；[统一消息](../../../runs/dsv4flash-db-first-full-01/dacomp-039/attempt-01/messages.jsonl)；[原始 OpenCode 事件](../../../runs/dsv4flash-db-first-full-01/dacomp-039/attempt-01/opencode.jsonl)；[SQL 引擎日志](../../../runs/dsv4flash-db-first-full-01/dacomp-039/attempt-01/sql_journal.jsonl)。

[可读报告（本地图片链接规范化）](../answers/dacomp-039.md)。原始回答保留，分析结论未改写。

## S1

类别 `connection_setup`；来源 `connection`；调用 `8085f74645b24c44aacc5f005b7f8381`；状态 `success`。

```sql
PRAGMA query_only=ON
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-039/attempt-01/sql/S1.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-039/attempt-01/sql/S1.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-039/attempt-01/results/S1.rows.jsonl)；完整：True；SHA256：`e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`。

## S2

类别 `metadata`；来源 `list_db`；调用 `8085f74645b24c44aacc5f005b7f8381`；状态 `success`。

```sql
SELECT name,sql FROM sqlite_master WHERE type='table' ORDER BY name
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-039/attempt-01/sql/S2.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-039/attempt-01/sql/S2.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-039/attempt-01/results/S2.rows.jsonl)；完整：True；SHA256：`1a2056ee6579fb3fcf0ff1e9bc50535a342f080b2f0adf884cb9b0c92fc79f51`。

## S3

类别 `data`；来源 `query_db`；调用 `ad1fc7ce50074644b027b2c6889e012d`；状态 `success`。

```sql
SELECT DISTINCT "Difficulty Level" FROM game_game_level_content_data_ta ORDER BY 1
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-039/attempt-01/sql/S3.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-039/attempt-01/sql/S3.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-039/attempt-01/results/S3.rows.jsonl)；完整：True；SHA256：`aede21aacdf4d4444fbbf3eaabe4546573b1e0a731658c7d7a149b478b702088`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "game_game_level_content_data_ta", "kind": "base", "block": null, "base_tables": ["game_game_level_content_data_ta"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |


## S4

类别 `data`；来源 `query_db`；调用 `383f05a4f331440483099ac56e75bbe6`；状态 `success`。

```sql
SELECT DISTINCT "Level Type" FROM game_game_level_content_data_ta ORDER BY 1
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-039/attempt-01/sql/S4.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-039/attempt-01/sql/S4.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-039/attempt-01/results/S4.rows.jsonl)；完整：True；SHA256：`4b561ceb7724b7a3006f287143b9326319ec18dba6e312b2fbad16719a6dfb23`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "game_game_level_content_data_ta", "kind": "base", "block": null, "base_tables": ["game_game_level_content_data_ta"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |


## S5

类别 `data`；来源 `query_db`；调用 `85d609c796e44b099e686742a1784f18`；状态 `success`。

```sql
SELECT MIN("Launch Time"), MAX("Launch Time") FROM game_game_level_content_data_ta
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-039/attempt-01/sql/S5.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-039/attempt-01/sql/S5.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-039/attempt-01/results/S5.rows.jsonl)；完整：True；SHA256：`055da577f04f2d2a9d915a87816f3a15ac48a5b63c1ed4d6e98d218572d1d5fd`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "game_game_level_content_data_ta", "kind": "base", "block": null, "base_tables": ["game_game_level_content_data_ta"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | MIN("Launch Time") | [{"table": "game_game_level_content_data_ta", "column": "Launch Time"}] | [] | False |
| B1 | MAX("Launch Time") | [{"table": "game_game_level_content_data_ta", "column": "Launch Time"}] | [] | False |


## S6

类别 `data`；来源 `query_db`；调用 `c5d13d9eb23348f794cf1384355bb51a`；状态 `success`。

```sql
SELECT COUNT(*) as total_2024 FROM game_game_level_content_data_ta
WHERE strftime('%Y', "Launch Time") = '2024'
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-039/attempt-01/sql/S6.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-039/attempt-01/sql/S6.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-039/attempt-01/results/S6.rows.jsonl)；完整：True；SHA256：`d7a7342db76ae566a457298fbe42377f7f7476126521385b81726116f7bc75c9`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "game_game_level_content_data_ta", "kind": "base", "block": null, "base_tables": ["game_game_level_content_data_ta"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |


## S7

类别 `data`；来源 `query_db`；调用 `9e7d3b8b44524d79bdbdf58dfab51d48`；状态 `success`。

```sql
SELECT 
  "Difficulty Level",
  "Level Type",
  COUNT(*) as level_count,
  ROUND(AVG("Churn Rate"), 4) as avg_churn,
  ROUND(AVG("Level Rating"), 4) as avg_rating,
  ROUND(AVG("Clear Rate"), 4) as avg_clear_rate,
  ROUND(AVG("Average Retry Count"), 2) as avg_retries
FROM game_game_level_content_data_ta
WHERE strftime('%Y', "Launch Time") = '2024'
GROUP BY "Difficulty Level", "Level Type"
ORDER BY "Difficulty Level", "Level Type"
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-039/attempt-01/sql/S7.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-039/attempt-01/sql/S7.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-039/attempt-01/results/S7.rows.jsonl)；完整：True；SHA256：`a7ef5d0351a987323128a07b251535fb7a5658fb31690acfeea91396dac3995d`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "game_game_level_content_data_ta", "kind": "base", "block": null, "base_tables": ["game_game_level_content_data_ta"]}] | [] | ["\"Difficulty Level\"", "\"Level Type\""] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |
| B1 | AVG("Churn Rate") | [{"table": "game_game_level_content_data_ta", "column": "Churn Rate"}] | [] | False |
| B1 | AVG("Level Rating") | [{"table": "game_game_level_content_data_ta", "column": "Level Rating"}] | [] | False |
| B1 | AVG("Clear Rate") | [{"table": "game_game_level_content_data_ta", "column": "Clear Rate"}] | [] | False |
| B1 | AVG("Average Retry Count") | [{"table": "game_game_level_content_data_ta", "column": "Average Retry Count"}] | [] | False |


## S8

类别 `data`；来源 `query_db`；调用 `1b4c4f90371d4f6f89dc6c4dc6b2b72e`；状态 `success`。

```sql
SELECT "Difficulty Level", COUNT(*) as cnt, ROUND(AVG("Churn Rate"),4) as avg_churn, ROUND(AVG("Level Rating"),4) as avg_rating
FROM game_game_level_content_data_ta
WHERE strftime('%Y', "Launch Time") = '2024'
GROUP BY "Difficulty Level" ORDER BY avg_churn DESC
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-039/attempt-01/sql/S8.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-039/attempt-01/sql/S8.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-039/attempt-01/results/S8.rows.jsonl)；完整：True；SHA256：`79356fe8d2bfaf6610d3f0f49f78e5d6819c900625a1fc639ba95b8458211c4e`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "game_game_level_content_data_ta", "kind": "base", "block": null, "base_tables": ["game_game_level_content_data_ta"]}] | [] | ["\"Difficulty Level\""] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |
| B1 | AVG("Churn Rate") | [{"table": "game_game_level_content_data_ta", "column": "Churn Rate"}] | [] | False |
| B1 | AVG("Level Rating") | [{"table": "game_game_level_content_data_ta", "column": "Level Rating"}] | [] | False |


## S9

类别 `data`；来源 `query_db`；调用 `3a572ad6a3dd48cba1d7c8c9183fb88e`；状态 `success`。

```sql
SELECT "Level Type", COUNT(*) as cnt, ROUND(AVG("Churn Rate"),4) as avg_churn, ROUND(AVG("Level Rating"),4) as avg_rating
FROM game_game_level_content_data_ta
WHERE strftime('%Y', "Launch Time") = '2024'
GROUP BY "Level Type" ORDER BY avg_churn DESC
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-039/attempt-01/sql/S9.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-039/attempt-01/sql/S9.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-039/attempt-01/results/S9.rows.jsonl)；完整：True；SHA256：`1e829e3b47c16e32cf34f5942d04581f244b12b6b6b1a886051408e6501e0311`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "game_game_level_content_data_ta", "kind": "base", "block": null, "base_tables": ["game_game_level_content_data_ta"]}] | [] | ["\"Level Type\""] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |
| B1 | AVG("Churn Rate") | [{"table": "game_game_level_content_data_ta", "column": "Churn Rate"}] | [] | False |
| B1 | AVG("Level Rating") | [{"table": "game_game_level_content_data_ta", "column": "Level Rating"}] | [] | False |


## S10

类别 `data`；来源 `query_db`；调用 `b9ba0cad793b479a85489727eb473931`；状态 `failed`。

```sql
SELECT 
  ROUND(CORR("Churn Rate", "Level Rating"), 4) as corr_churn_rating,
  ROUND(CORR("Churn Rate", "Clear Rate"), 4) as corr_churn_clear,
  ROUND(CORR("Level Rating", "Clear Rate"), 4) as corr_rating_clear,
  ROUND(CORR("Churn Rate", "Average Retry Count"), 4) as corr_churn_retry
FROM game_game_level_content_data_ta
WHERE strftime('%Y', "Launch Time") = '2024'
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-039/attempt-01/sql/S10.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-039/attempt-01/sql/S10.parameters.json)。

错误：`OperationalError('no such function: CORR')`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "game_game_level_content_data_ta", "kind": "base", "block": null, "base_tables": ["game_game_level_content_data_ta"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | CORR("Churn Rate", "Level Rating") | [{"table": "game_game_level_content_data_ta", "column": "Churn Rate"}, {"table": "game_game_level_content_data_ta", "column": "Level Rating"}] | [] | False |
| B1 | CORR("Churn Rate", "Clear Rate") | [{"table": "game_game_level_content_data_ta", "column": "Churn Rate"}, {"table": "game_game_level_content_data_ta", "column": "Clear Rate"}] | [] | False |
| B1 | CORR("Level Rating", "Clear Rate") | [{"table": "game_game_level_content_data_ta", "column": "Level Rating"}, {"table": "game_game_level_content_data_ta", "column": "Clear Rate"}] | [] | False |
| B1 | CORR("Churn Rate", "Average Retry Count") | [{"table": "game_game_level_content_data_ta", "column": "Churn Rate"}, {"table": "game_game_level_content_data_ta", "column": "Average Retry Count"}] | [] | False |


## S11

类别 `data`；来源 `python`；调用 `d1043e1603b8489890f6c24819bdd391`；状态 `success`。

```sql
SELECT * FROM game_game_level_content_data_ta WHERE strftime('%Y', "Launch Time") = '2024'
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-039/attempt-01/sql/S11.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-039/attempt-01/sql/S11.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-039/attempt-01/results/S11.rows.jsonl)；完整：True；SHA256：`35cdab886ec53d3e02a0fd6a6dadd9f579cc5d385e651b5632226242faa38d08`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "game_game_level_content_data_ta", "kind": "base", "block": null, "base_tables": ["game_game_level_content_data_ta"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |


## S12

类别 `data`；来源 `query_db`；调用 `4e104b33094d4963a004413c19abca13`；状态 `failed`。

```sql
SELECT 
  "Difficulty Level",
  "Level Type",
  COUNT(*) as level_count,
  ROUND(AVG("Churn Rate"), 4) as avg_churn,
  ROUND(STDEV("Churn Rate"), 4) as std_churn,
  ROUND(AVG("Level Rating"), 4) as avg_rating,
  ROUND(STDEV("Level Rating"), 4) as std_rating,
  ROUND(AVG("Clear Rate"), 4) as avg_clear_rate,
  ROUND(AVG("Average Retry Count"), 2) as avg_retries
FROM game_game_level_content_data_ta
WHERE strftime('%Y', "Launch Time") = '2024'
GROUP BY "Difficulty Level", "Level Type"
ORDER BY "Difficulty Level", "Level Type"
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-039/attempt-01/sql/S12.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-039/attempt-01/sql/S12.parameters.json)。

错误：`OperationalError('no such function: STDEV')`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "game_game_level_content_data_ta", "kind": "base", "block": null, "base_tables": ["game_game_level_content_data_ta"]}] | [] | ["\"Difficulty Level\"", "\"Level Type\""] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |
| B1 | AVG("Churn Rate") | [{"table": "game_game_level_content_data_ta", "column": "Churn Rate"}] | [] | False |
| B1 | STDDEV("Churn Rate") | [{"table": "game_game_level_content_data_ta", "column": "Churn Rate"}] | [] | False |
| B1 | AVG("Level Rating") | [{"table": "game_game_level_content_data_ta", "column": "Level Rating"}] | [] | False |
| B1 | STDDEV("Level Rating") | [{"table": "game_game_level_content_data_ta", "column": "Level Rating"}] | [] | False |
| B1 | AVG("Clear Rate") | [{"table": "game_game_level_content_data_ta", "column": "Clear Rate"}] | [] | False |
| B1 | AVG("Average Retry Count") | [{"table": "game_game_level_content_data_ta", "column": "Average Retry Count"}] | [] | False |


## S13

类别 `data`；来源 `python`；调用 `1d3e23d6c2d04fafa8ea8723e3edf547`；状态 `success`。

```sql
SELECT * FROM game_game_level_content_data_ta WHERE strftime('%Y', "Launch Time") = '2024'
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-039/attempt-01/sql/S13.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-039/attempt-01/sql/S13.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-039/attempt-01/results/S13.rows.jsonl)；完整：True；SHA256：`35cdab886ec53d3e02a0fd6a6dadd9f579cc5d385e651b5632226242faa38d08`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "game_game_level_content_data_ta", "kind": "base", "block": null, "base_tables": ["game_game_level_content_data_ta"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |


## S14

类别 `data`；来源 `python`；调用 `8797a4369ea947559e4112fbbb6e9028`；状态 `success`。

```sql
SELECT * FROM game_game_level_content_data_ta WHERE strftime('%Y', "Launch Time") = '2024'
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-039/attempt-01/sql/S14.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-039/attempt-01/sql/S14.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-039/attempt-01/results/S14.rows.jsonl)；完整：True；SHA256：`35cdab886ec53d3e02a0fd6a6dadd9f579cc5d385e651b5632226242faa38d08`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "game_game_level_content_data_ta", "kind": "base", "block": null, "base_tables": ["game_game_level_content_data_ta"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |


## S15

类别 `data`；来源 `python`；调用 `47286a70f461425b9e7fd8344236aa39`；状态 `success`。

```sql
SELECT * FROM game_game_level_content_data_ta WHERE strftime('%Y', "Launch Time") = '2024'
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-039/attempt-01/sql/S15.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-039/attempt-01/sql/S15.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-039/attempt-01/results/S15.rows.jsonl)；完整：True；SHA256：`35cdab886ec53d3e02a0fd6a6dadd9f579cc5d385e651b5632226242faa38d08`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "game_game_level_content_data_ta", "kind": "base", "block": null, "base_tables": ["game_game_level_content_data_ta"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |


## S16

类别 `data`；来源 `query_db`；调用 `61cb873befa94942a31522412aaf6d4a`；状态 `success`。

```sql
-- Stat summary by difficulty for 2024
SELECT 
  "Difficulty Level",
  COUNT(*) as cnt,
  ROUND(MIN("Churn Rate"), 4) as min_churn,
  ROUND(AVG("Churn Rate"), 4) as avg_churn,
  ROUND(MAX("Churn Rate"), 4) as max_churn,
  ROUND(AVG("Level Rating"), 4) as avg_rating,
  ROUND(AVG("Clear Rate"), 4) as avg_clear,
  ROUND(AVG("Average Retry Count"), 2) as avg_retries,
  ROUND(AVG("Level Completion Rate"), 4) as avg_completion
FROM game_game_level_content_data_ta
WHERE strftime('%Y', "Launch Time") = '2024'
GROUP BY "Difficulty Level"
ORDER BY avg_churn DESC
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-039/attempt-01/sql/S16.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-039/attempt-01/sql/S16.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-039/attempt-01/results/S16.rows.jsonl)；完整：True；SHA256：`726f202ad2f91aa33a491788c50a3014ca6f0d785f6dea800176c72bfc85125d`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "game_game_level_content_data_ta", "kind": "base", "block": null, "base_tables": ["game_game_level_content_data_ta"]}] | [] | ["\"Difficulty Level\""] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |
| B1 | MIN("Churn Rate") | [{"table": "game_game_level_content_data_ta", "column": "Churn Rate"}] | [] | False |
| B1 | AVG("Churn Rate") | [{"table": "game_game_level_content_data_ta", "column": "Churn Rate"}] | [] | False |
| B1 | MAX("Churn Rate") | [{"table": "game_game_level_content_data_ta", "column": "Churn Rate"}] | [] | False |
| B1 | AVG("Level Rating") | [{"table": "game_game_level_content_data_ta", "column": "Level Rating"}] | [] | False |
| B1 | AVG("Clear Rate") | [{"table": "game_game_level_content_data_ta", "column": "Clear Rate"}] | [] | False |
| B1 | AVG("Average Retry Count") | [{"table": "game_game_level_content_data_ta", "column": "Average Retry Count"}] | [] | False |
| B1 | AVG("Level Completion Rate") | [{"table": "game_game_level_content_data_ta", "column": "Level Completion Rate"}] | [] | False |


## S17

类别 `data`；来源 `query_db`；调用 `03d7595dfda14bb591ece5e97bc8f217`；状态 `success`。

```sql
-- Monthly trends in 2024
SELECT 
  strftime('%Y-%m', "Launch Time") as launch_month,
  COUNT(*) as level_count,
  ROUND(AVG("Churn Rate"), 4) as avg_churn,
  ROUND(AVG("Level Rating"), 4) as avg_rating
FROM game_game_level_content_data_ta
WHERE strftime('%Y', "Launch Time") = '2024'
GROUP BY launch_month
ORDER BY launch_month
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-039/attempt-01/sql/S17.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-039/attempt-01/sql/S17.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-039/attempt-01/results/S17.rows.jsonl)；完整：True；SHA256：`7df17d59c8856e6117964181b932943c2db9a9e1388d8b6a75eac152c435a2bd`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "game_game_level_content_data_ta", "kind": "base", "block": null, "base_tables": ["game_game_level_content_data_ta"]}] | [] | ["STRFTIME('%Y-%m', \"Launch Time\")"] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |
| B1 | AVG("Churn Rate") | [{"table": "game_game_level_content_data_ta", "column": "Churn Rate"}] | [] | False |
| B1 | AVG("Level Rating") | [{"table": "game_game_level_content_data_ta", "column": "Level Rating"}] | [] | False |


## S18

类别 `data`；来源 `query_db`；调用 `0ccbc4ef172a46bf933073d985a90c62`；状态 `success`。

```sql
SELECT "Reward Type", COUNT(*) as cnt,
  ROUND(AVG("Churn Rate"),4) as avg_churn,
  ROUND(AVG("Level Rating"),4) as avg_rating
FROM game_game_level_content_data_ta
WHERE strftime('%Y', "Launch Time") = '2024'
GROUP BY "Reward Type" ORDER BY avg_churn DESC
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-039/attempt-01/sql/S18.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-039/attempt-01/sql/S18.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-039/attempt-01/results/S18.rows.jsonl)；完整：True；SHA256：`a4b38bdc186a7d58a6da4fd091a900d6304c4f9013d2e0e965c9b48cd88f826e`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "game_game_level_content_data_ta", "kind": "base", "block": null, "base_tables": ["game_game_level_content_data_ta"]}] | [] | ["\"Reward Type\""] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |
| B1 | AVG("Churn Rate") | [{"table": "game_game_level_content_data_ta", "column": "Churn Rate"}] | [] | False |
| B1 | AVG("Level Rating") | [{"table": "game_game_level_content_data_ta", "column": "Level Rating"}] | [] | False |


## S19

类别 `data`；来源 `query_db`；调用 `62d7b6f0dda344fdb46e131be3eb2ee6`；状态 `success`。

```sql
-- Deviation of each Difficulty x Type combo from its Difficulty baseline (2024)
WITH base AS (
  SELECT "Difficulty Level", AVG("Churn Rate") AS d_churn, AVG("Level Rating") AS d_rating
  FROM game_game_level_content_data_ta
  WHERE strftime('%Y', "Launch Time") = '2024'
  GROUP BY "Difficulty Level"
),
comb AS (
  SELECT "Difficulty Level", "Level Type", COUNT(*) as cnt,
    AVG("Churn Rate") as c_churn, AVG("Level Rating") as c_rating
  FROM game_game_level_content_data_ta
  WHERE strftime('%Y', "Launch Time") = '2024'
  GROUP BY "Difficulty Level", "Level Type"
)
SELECT comb."Difficulty Level", comb."Level Type", comb.cnt,
  ROUND(comb.c_churn, 4) as combo_churn, ROUND(base.d_churn, 4) as diff_avg_churn,
  ROUND(comb.c_churn - base.d_churn, 4) as churn_dev,
  ROUND(comb.c_rating, 2) as combo_rating, ROUND(base.d_rating, 2) as diff_avg_rating,
  ROUND(comb.c_rating - base.d_rating, 2) as rating_dev
FROM comb JOIN base ON comb."Difficulty Level" = base."Difficulty Level"
ORDER BY churn_dev DESC
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-039/attempt-01/sql/S19.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-039/attempt-01/sql/S19.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-039/attempt-01/results/S19.rows.jsonl)；完整：True；SHA256：`3064bc3cce30d6c915c75f6074cd9e558d1de0e56c5e31387f438460546f23e4`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "game_game_level_content_data_ta", "kind": "base", "block": null, "base_tables": ["game_game_level_content_data_ta"]}] | [] | ["\"Difficulty Level\""] |
| B2 | [{"alias": "game_game_level_content_data_ta", "kind": "base", "block": null, "base_tables": ["game_game_level_content_data_ta"]}] | [] | ["\"Difficulty Level\"", "\"Level Type\""] |
| B3 | [{"alias": "base", "kind": "derived", "block": "B1", "base_tables": ["game_game_level_content_data_ta"]}, {"alias": "comb", "kind": "derived", "block": "B2", "base_tables": ["game_game_level_content_data_ta"]}] | [{"type": "INNER", "right": "base", "on": "comb.\"Difficulty Level\" = base.\"Difficulty Level\"", "using": []}] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | AVG("Churn Rate") | [{"table": "game_game_level_content_data_ta", "column": "Churn Rate"}] | [] | False |
| B1 | AVG("Level Rating") | [{"table": "game_game_level_content_data_ta", "column": "Level Rating"}] | [] | False |
| B2 | COUNT(*) | [] | [] | True |
| B2 | AVG("Churn Rate") | [{"table": "game_game_level_content_data_ta", "column": "Churn Rate"}] | [] | False |
| B2 | AVG("Level Rating") | [{"table": "game_game_level_content_data_ta", "column": "Level Rating"}] | [] | False |


## S20

类别 `data`；来源 `query_db`；调用 `3bd3814210ba423e88eb267bf69fedda`；状态 `success`。

```sql
-- Cross-tab Difficulty x Reward Type for 2024
SELECT "Difficulty Level", "Reward Type", COUNT(*) as cnt
FROM game_game_level_content_data_ta
WHERE strftime('%Y', "Launch Time") = '2024'
GROUP BY "Difficulty Level", "Reward Type"
ORDER BY "Difficulty Level", cnt DESC
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-039/attempt-01/sql/S20.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-039/attempt-01/sql/S20.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-039/attempt-01/results/S20.rows.jsonl)；完整：True；SHA256：`808bdab6fd382541d5718152c688a66379b361bd764801c94978fd0b2d2ffa84`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "game_game_level_content_data_ta", "kind": "base", "block": null, "base_tables": ["game_game_level_content_data_ta"]}] | [] | ["\"Difficulty Level\"", "\"Reward Type\""] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |


## S21

类别 `data`；来源 `query_db`；调用 `cdff81d7c7bf41d39f52a73198a98b23`；状态 `success`。

```sql
-- Correlation proxy: reward value ranges by difficulty
SELECT "Difficulty Level", MIN("Reward Value") as min_rw, MAX("Reward Value") as max_rw, ROUND(AVG("Reward Value"),2) as avg_rw
FROM game_game_level_content_data_ta
WHERE strftime('%Y', "Launch Time") = '2024'
GROUP BY "Difficulty Level" ORDER BY avg_rw DESC
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-039/attempt-01/sql/S21.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-039/attempt-01/sql/S21.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-039/attempt-01/results/S21.rows.jsonl)；完整：True；SHA256：`375fae830ee8c6e02a9e59f37a2d8da758d3023f9db67a9e7452fec69b0af3fe`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "game_game_level_content_data_ta", "kind": "base", "block": null, "base_tables": ["game_game_level_content_data_ta"]}] | [] | ["\"Difficulty Level\""] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | MIN("Reward Value") | [{"table": "game_game_level_content_data_ta", "column": "Reward Value"}] | [] | False |
| B1 | MAX("Reward Value") | [{"table": "game_game_level_content_data_ta", "column": "Reward Value"}] | [] | False |
| B1 | AVG("Reward Value") | [{"table": "game_game_level_content_data_ta", "column": "Reward Value"}] | [] | False |


## S22

类别 `data`；来源 `python`；调用 `ee3468502c004237ab1a7d0faff1424e`；状态 `success`。

```sql
SELECT * FROM game_game_level_content_data_ta WHERE strftime('%Y', "Launch Time") = '2024'
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-039/attempt-01/sql/S22.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-039/attempt-01/sql/S22.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-039/attempt-01/results/S22.rows.jsonl)；完整：True；SHA256：`35cdab886ec53d3e02a0fd6a6dadd9f579cc5d385e651b5632226242faa38d08`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "game_game_level_content_data_ta", "kind": "base", "block": null, "base_tables": ["game_game_level_content_data_ta"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |


## S23

类别 `data`；来源 `python`；调用 `612185ccd53148f5bd97f28943aef830`；状态 `success`。

```sql
SELECT * FROM game_game_level_content_data_ta WHERE strftime('%Y', "Launch Time") = '2024'
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-039/attempt-01/sql/S23.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-039/attempt-01/sql/S23.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-039/attempt-01/results/S23.rows.jsonl)；完整：True；SHA256：`35cdab886ec53d3e02a0fd6a6dadd9f579cc5d385e651b5632226242faa38d08`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "game_game_level_content_data_ta", "kind": "base", "block": null, "base_tables": ["game_game_level_content_data_ta"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |


## S24

类别 `data`；来源 `query_db`；调用 `4360dc3dc41844e7b444e3ff0d842b49`；状态 `success`。

```sql
-- Same combination analysis for ALL years (context for 2024 patterns)
SELECT 
  "Difficulty Level", "Level Type", COUNT(*) as cnt,
  ROUND(AVG("Churn Rate"), 4) as avg_churn,
  ROUND(AVG("Level Rating"), 4) as avg_rating
FROM game_game_level_content_data_ta
GROUP BY "Difficulty Level", "Level Type"
ORDER BY avg_churn DESC
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-039/attempt-01/sql/S24.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-039/attempt-01/sql/S24.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-039/attempt-01/results/S24.rows.jsonl)；完整：True；SHA256：`fb530bc530c849eaf0d451972988a6beea81bb8575cc2bb41e086853b5024f92`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "game_game_level_content_data_ta", "kind": "base", "block": null, "base_tables": ["game_game_level_content_data_ta"]}] | [] | ["\"Difficulty Level\"", "\"Level Type\""] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |
| B1 | AVG("Churn Rate") | [{"table": "game_game_level_content_data_ta", "column": "Churn Rate"}] | [] | False |
| B1 | AVG("Level Rating") | [{"table": "game_game_level_content_data_ta", "column": "Level Rating"}] | [] | False |


## S25

类别 `data`；来源 `query_db`；调用 `6a48d5ac823e49d8a9d738f1ce737934`；状态 `success`。

```sql
-- Yearly trend of churn and rating by difficulty to check stability
SELECT strftime('%Y', "Launch Time") as yr, "Difficulty Level",
  COUNT(*) as cnt, ROUND(AVG("Churn Rate"), 4) as avg_churn, ROUND(AVG("Level Rating"), 4) as avg_rating
FROM game_game_level_content_data_ta
WHERE strftime('%Y', "Launch Time") IN ('2022','2023','2024')
GROUP BY yr, "Difficulty Level"
ORDER BY yr, avg_churn DESC
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-039/attempt-01/sql/S25.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-039/attempt-01/sql/S25.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-039/attempt-01/results/S25.rows.jsonl)；完整：True；SHA256：`b666521729a683a1696c32e057dece433863625c44cb243813da1d0b294ea9f0`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "game_game_level_content_data_ta", "kind": "base", "block": null, "base_tables": ["game_game_level_content_data_ta"]}] | [] | ["STRFTIME('%Y', \"Launch Time\")", "\"Difficulty Level\""] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |
| B1 | AVG("Churn Rate") | [{"table": "game_game_level_content_data_ta", "column": "Churn Rate"}] | [] | False |
| B1 | AVG("Level Rating") | [{"table": "game_game_level_content_data_ta", "column": "Level Rating"}] | [] | False |


## S26

类别 `data`；来源 `python`；调用 `6ad28f0b488642bb9480c6cbe37f606a`；状态 `success`。

```sql
SELECT * FROM game_game_level_content_data_ta WHERE strftime('%Y', "Launch Time") = '2024'
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-039/attempt-01/sql/S26.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-039/attempt-01/sql/S26.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-039/attempt-01/results/S26.rows.jsonl)；完整：True；SHA256：`35cdab886ec53d3e02a0fd6a6dadd9f579cc5d385e651b5632226242faa38d08`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "game_game_level_content_data_ta", "kind": "base", "block": null, "base_tables": ["game_game_level_content_data_ta"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |


## S27

类别 `data`；来源 `query_db`；调用 `d887c21713d54d439011eb4a140404ac`；状态 `success`。

```sql
SELECT MIN("Level Completion Rate" + "Churn Rate") as min_sum,
       MAX("Level Completion Rate" + "Churn Rate") as max_sum,
       ROUND(AVG("Level Completion Rate" + "Churn Rate"), 4) as avg_sum
FROM game_game_level_content_data_ta
WHERE strftime('%Y', "Launch Time") = '2024'
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-039/attempt-01/sql/S27.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-039/attempt-01/sql/S27.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-039/attempt-01/results/S27.rows.jsonl)；完整：True；SHA256：`2b2d3e5699c2f028d32fbe3a6862844e06403aa857622cc32a3663ed87596b21`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "game_game_level_content_data_ta", "kind": "base", "block": null, "base_tables": ["game_game_level_content_data_ta"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | MIN("Level Completion Rate" + "Churn Rate") | [{"table": "game_game_level_content_data_ta", "column": "Level Completion Rate"}, {"table": "game_game_level_content_data_ta", "column": "Churn Rate"}] | [] | False |
| B1 | MAX("Level Completion Rate" + "Churn Rate") | [{"table": "game_game_level_content_data_ta", "column": "Level Completion Rate"}, {"table": "game_game_level_content_data_ta", "column": "Churn Rate"}] | [] | False |
| B1 | AVG("Level Completion Rate" + "Churn Rate") | [{"table": "game_game_level_content_data_ta", "column": "Level Completion Rate"}, {"table": "game_game_level_content_data_ta", "column": "Churn Rate"}] | [] | False |


## S28

类别 `data`；来源 `query_db`；调用 `54912b1d17424b1da94d08c8a294d4de`；状态 `success`。

```sql
-- Difficulty mix by year (share of levels)
SELECT strftime('%Y', "Launch Time") as yr, "Difficulty Level", COUNT(*) as cnt
FROM game_game_level_content_data_ta
WHERE strftime('%Y', "Launch Time") IN ('2022','2023','2024')
GROUP BY yr, "Difficulty Level"
ORDER BY yr, cnt DESC
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-039/attempt-01/sql/S28.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-039/attempt-01/sql/S28.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-039/attempt-01/results/S28.rows.jsonl)；完整：True；SHA256：`aad637989b89a130131a92ed206b4a9b6e2c090d8070ac3a704fb0416734ba2a`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "game_game_level_content_data_ta", "kind": "base", "block": null, "base_tables": ["game_game_level_content_data_ta"]}] | [] | ["STRFTIME('%Y', \"Launch Time\")", "\"Difficulty Level\""] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |


## S29

类别 `data`；来源 `python`；调用 `74f4d98144a74440b01cbbeaea9564f1`；状态 `success`。

```sql
SELECT * FROM game_game_level_content_data_ta WHERE strftime('%Y', "Launch Time") = '2024'
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-039/attempt-01/sql/S29.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-039/attempt-01/sql/S29.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-039/attempt-01/results/S29.rows.jsonl)；完整：True；SHA256：`35cdab886ec53d3e02a0fd6a6dadd9f579cc5d385e651b5632226242faa38d08`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "game_game_level_content_data_ta", "kind": "base", "block": null, "base_tables": ["game_game_level_content_data_ta"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |

