# dacomp-003

I am studying China’s economic development and water use and have obtained the relevant da…

运行：已提交。官方未评分。全部 SQL 尝试/成功 26/26；数据 SQL 24/24；Python 6 次。

完整原题：

I am studying China’s economic development and water use and have obtained the relevant data. Based on the dataset I provide, please analyze, from China’s overall data, how the overall relationship between the share of Industrial Water Consumption and the level of economic development looks. Does this relationship differ when broken down by different provinces and municipalities?

| 表 | 行数 | 列数 |
| --- | --- | --- |
| economic_indicator_data | 515 | 7 |
| sheet1 | 515 | 13 |


实际路线（分析者依据 SQL/源码概括，不代表 Agent 自述）：S3：economic_indicator_data 查询 → S8：sheet1 查询 → S12：economic_indicator_data 查询 → S17：economic_indicator_data/sheet1 查询 → S21：economic_indicator_data/sheet1 查询 → S26：economic_indicator_data/sheet1 查询（等距列出六个结构节点，全部步骤见下表）

数据库大小：200,704 字节。

## 数据 SQL

| SQL | 状态 | 基础表 | Join 输入/类型 | GROUP BY | 聚合表达式 | 结果行数 | 数据库 ms |
| --- | --- | --- | --- | --- | --- | --- | --- |
| [S3/Q1](#s3) | success | ["economic_indicator_data"] | 0 / {} | [] | ["COUNT(*)"] | 1 | 0.353 |
| [S4/Q2](#s4) | success | ["sheet1"] | 0 / {} | [] | ["COUNT(*)"] | 1 | 0.278 |
| [S5/Q3](#s5) | success | ["sheet1"] | 0 / {} | [] | ["MIN(\"Year\")", "MAX(\"Year\")", "COUNT(DISTINCT \"Year\")"] | 1 | 0.482 |
| [S6/Q4](#s6) | success | ["sheet1"] | 0 / {} | ["\"Region Name\""] | ["COUNT(*)"] | 32 | 0.506 |
| [S7/Q5](#s7) | success | ["sheet1"] | 0 / {} | [] | [] | 0 | 0.424 |
| [S8/Q6](#s8) | success | ["sheet1"] | 0 / {} | [] | [] | 19 | 0.409 |
| [S9/Q7](#s9) | success | ["sheet1"] | 0 / {} | [] | [] | 16 | 0.393 |
| [S10/Q8](#s10) | success | ["sheet1"] | 0 / {} | [] | [] | 0 | 0.415 |
| [S11/Q9](#s11) | success | ["sheet1"] | 0 / {} | ["\"Region Name\""] | ["COUNT(DISTINCT \"Year\")", "MIN(\"Year\")", "MAX(\"Year\")"] | 32 | 0.741 |
| [S12/Q10](#s12) | success | ["economic_indicator_data"] | 0 / {} | [] | ["MIN(\"Year\")", "MAX(\"Year\")", "COUNT(DISTINCT \"Year\")"] | 1 | 0.506 |
| [S13/Q11](#s13) | success | ["economic_indicator_data"] | 0 / {} | [] | ["MIN(\"Year\")", "MAX(\"Year\")", "COUNT(DISTINCT \"Year\")"] | 1 | 0.392 |
| [S14/Q12](#s14) | success | ["economic_indicator_data", "sheet1"] | 2 / {'INNER': 1} | [] | [] | 19 | 0.591 |
| [S15/Q13](#s15) | success | ["economic_indicator_data", "sheet1"] | 2 / {'LEFT': 1} | [] | ["COUNT(*)", "SUM(CASE WHEN s.\"Industrial Water Consumption (100 million m³)\" IS NULL THEN 1 ELSE 0 END)", "SUM(CASE WHEN s.\"Total Water Consumption (100 million m³) \" IS NULL THEN 1 ELSE 0 END)", "SUM(CASE WHEN e.\"Per capita GDP (yuan/person)\" IS NULL THEN 1 ELSE 0 END)"] | 1 | 1.17 |
| [S16/Q14](#s16) | success | ["economic_indicator_data", "sheet1"] | 2 / {'INNER': 1} | [] | [] | 19 | 0.428 |
| [S17/Q15](#s17) | success | ["economic_indicator_data", "sheet1"] | 2 / {'INNER': 1} | [] | [] | 496 | 1.864 |
| [S18/Q16](#s18) | success | ["economic_indicator_data", "sheet1"] | 2 / {'INNER': 1} | [] | [] | 19 | 0.611 |
| [S19/Q17](#s19) | success | ["economic_indicator_data", "sheet1"] | 2 / {'INNER': 1} | [] | [] | 496 | 1.571 |
| [S20/Q18](#s20) | success | ["economic_indicator_data", "sheet1"] | 2 / {'INNER': 1} | [] | [] | 19 | 0.601 |
| [S21/Q19](#s21) | success | ["economic_indicator_data", "sheet1"] | 2 / {'INNER': 1} | [] | [] | 496 | 1.658 |
| [S22/Q20](#s22) | success | ["economic_indicator_data", "sheet1"] | 2 / {'INNER': 1} | [] | [] | 19 | 0.536 |
| [S23/Q21](#s23) | success | ["economic_indicator_data", "sheet1"] | 2 / {'INNER': 1} | [] | [] | 496 | 1.47 |
| [S24/Q22](#s24) | success | ["economic_indicator_data", "sheet1"] | 2 / {'INNER': 1} | [] | [] | 496 | 1.546 |
| [S25/Q23](#s25) | success | ["economic_indicator_data", "sheet1"] | 2 / {'INNER': 1} | [] | [] | 496 | 1.557 |
| [S26/Q24](#s26) | success | ["economic_indicator_data", "sheet1"] | 2 / {'INNER': 1} | [] | [] | 496 | 1.539 |


## 元数据和设置

| SQL | 类别 | 状态 | 内容 |
| --- | --- | --- | --- |
| S1 | connection_setup | success | PRAGMA query_only=ON |
| S2 | metadata | success | SELECT name,sql FROM sqlite_master WHERE type='table' ORDER BY name |


## Python 与执行位置

人工源码审查：**database_first_partial_violation**。Pearson/Spearman tests and polynomial fitting are legitimate Python uses. Per-region mean aggregation and demeaning (P3/P4) can be prepared with SQLite GROUP BY/window arithmetic; these preparation portions were performed in pandas. Group iteration solely to run per-region statistical tests is not itself marked a violation. [证据](../reviews/dacomp-003.json)。

P1：Need to compute Pearson/Spearman correlations and create visualizations for the national-level relationship and province-level relationships. SQLite does not support correlation functions or plotting, so this statistical analysis and visualization step is performed in Python using data already joined/aggregated in SQL.

[源码](../../../runs/dsv4flash-db-first-full-01/dacomp-003/attempt-01/python/P1.py)；[输出](../../../runs/dsv4flash-db-first-full-01/dacomp-003/attempt-01/python/P1.stdout)；[错误](../../../runs/dsv4flash-db-first-full-01/dacomp-003/attempt-01/python/P1.stderr)。检出需人工核验的 SQL 可实现操作：groupby(, .query(, sort_values(；不能仅凭理由判为合规。

P2：Creating national and province-level visualizations (time series, scatters, fitted quadratic) and computing temporal changes. Plotting and curve fitting are not supported by SQLite; the data was already joined/aggregated in SQL.

[源码](../../../runs/dsv4flash-db-first-full-01/dacomp-003/attempt-01/python/P2.py)；[输出](../../../runs/dsv4flash-db-first-full-01/dacomp-003/attempt-01/python/P2.stdout)；[错误](../../../runs/dsv4flash-db-first-full-01/dacomp-003/attempt-01/python/P2.stderr)。检出需人工核验的 SQL 可实现操作：.merge(, .query(, sort_values(；不能仅凭理由判为合规。

P3：Decomposing the pooled correlation into within-province (temporal) and between-province (cross-sectional) components, testing phase-specific national correlations, and examining the convergence pattern (initial share vs change). These are statistical procedures not supported by SQLite.

[源码](../../../runs/dsv4flash-db-first-full-01/dacomp-003/attempt-01/python/P3.py)；[输出](../../../runs/dsv4flash-db-first-full-01/dacomp-003/attempt-01/python/P3.stdout)；[错误](../../../runs/dsv4flash-db-first-full-01/dacomp-003/attempt-01/python/P3.stderr)。检出需人工核验的 SQL 可实现操作：groupby(, .query(；不能仅凭理由判为合规。

P4：Generating the convergence, between-province, and within-province scatter plots. These visualizations are not supported by SQLite.

[源码](../../../runs/dsv4flash-db-first-full-01/dacomp-003/attempt-01/python/P4.py)；[输出](../../../runs/dsv4flash-db-first-full-01/dacomp-003/attempt-01/python/P4.stdout)；[错误](../../../runs/dsv4flash-db-first-full-01/dacomp-003/attempt-01/python/P4.stderr)。检出需人工核验的 SQL 可实现操作：groupby(, .query(；不能仅凭理由判为合规。

P5：Verifying the inverted-U hypothesis with a pooled quadratic fit, computing province-level annual trends, and checking cross-sectional relationships in 2003 vs 2018. These statistics and the trajectory plot are not supported by SQLite.

[源码](../../../runs/dsv4flash-db-first-full-01/dacomp-003/attempt-01/python/P5.py)；[输出](../../../runs/dsv4flash-db-first-full-01/dacomp-003/attempt-01/python/P5.stdout)；[错误](../../../runs/dsv4flash-db-first-full-01/dacomp-003/attempt-01/python/P5.stderr)。检出需人工核验的 SQL 可实现操作：groupby(, .query(, sort_values(；不能仅凭理由判为合规。

P6：Testing whether the initial (2003) income level predicts each province's subsequent change in industrial water share — a hypothesis test not supported by SQLite.

[源码](../../../runs/dsv4flash-db-first-full-01/dacomp-003/attempt-01/python/P6.py)；[输出](../../../runs/dsv4flash-db-first-full-01/dacomp-003/attempt-01/python/P6.stdout)；[错误](../../../runs/dsv4flash-db-first-full-01/dacomp-003/attempt-01/python/P6.stderr)。检出需人工核验的 SQL 可实现操作：.query(, sort_values(；不能仅凭理由判为合规。

## 优化机会

已验证候选。筛选限于精确 SQL、相同自包含 CTE、相同单表完整过滤、可分解单表聚合；未覆盖任意 Join 等价和一般谓词蕴含。全部候选都是 offline，未测在线预测。

| 候选 | 类型 | 已有结果 | 覆盖 SQL | 后续次数 | 中间行数 | 验证 | 成本 |
| --- | --- | --- | --- | --- | --- | --- | --- |
| C1 | exact-result reuse | True | ["S14", "S16"] | 1 | 19 | verified | Not benchmarked; correctness alone does not establish net speedup. |
| C2 | exact-result reuse | True | ["S19", "S21", "S23", "S24", "S25", "S26"] | 5 | 496 | verified | Not benchmarked; correctness alone does not establish net speedup. |
| C3 | exact-result reuse | True | ["S20", "S22"] | 1 | 19 | verified | Not benchmarked; correctness alone does not establish net speedup. |
| C4 | aggregate MV | False | ["S4", "S6"] | 1 | unknown | not_verified_cap | Not tested |


已验证覆盖（含触发查询、候选并集去重）：10/24 条成功数据 SQL。正确性仅针对当前数据库快照；未测性能的候选不能声称已加速。

[完整 build/rewrite 与比较证据](dacomp-003.analysis.json)。

### C2：exact-result reuse

Identical normalized SQL and parameters; archive equality checked.

原查询 [S19](#s19), [S21](#s21), [S23](#s23), [S24](#s24), [S25](#s25), [S26](#s26) → 保留前序结果 S19 → 后续 5 次可复用。该构建点为事后假设，不代表 Agent 当时预知后续。

| 原 SQL | 列名一致 | 结果一致 | 比较方法 |
| --- | --- | --- | --- |
| S21 | True | True | ordered_numeric_tolerance |
| S23 | True | True | ordered_numeric_tolerance |
| S24 | True | True | ordered_numeric_tolerance |
| S25 | True | True | ordered_numeric_tolerance |
| S26 | True | True | ordered_numeric_tolerance |


验证状态：verified；成本结论：Not benchmarked; correctness alone does not establish net speedup.

### C1：exact-result reuse

Identical normalized SQL and parameters; archive equality checked.

原查询 [S14](#s14), [S16](#s16) → 保留前序结果 S14 → 后续 1 次可复用。该构建点为事后假设，不代表 Agent 当时预知后续。

| 原 SQL | 列名一致 | 结果一致 | 比较方法 |
| --- | --- | --- | --- |
| S16 | True | True | ordered_numeric_tolerance |


验证状态：verified；成本结论：Not benchmarked; correctness alone does not establish net speedup.

### C3：exact-result reuse

Identical normalized SQL and parameters; archive equality checked.

原查询 [S20](#s20), [S22](#s22) → 保留前序结果 S20 → 后续 1 次可复用。该构建点为事后假设，不代表 Agent 当时预知后续。

| 原 SQL | 列名一致 | 结果一致 | 比较方法 |
| --- | --- | --- | --- |
| S22 | True | True | ordered_numeric_tolerance |


验证状态：verified；成本结论：Not benchmarked; correctness alone does not establish net speedup.

结果依赖：自动记录 SQL→Python 的接口父调用，以及源码中引用归档文件的消费者；字面值相同不认定因果。模型方向选择需要人工读取消息，尚未做全面因果标注。

[原始报告](../../../runs/dsv4flash-db-first-full-01/dacomp-003/attempt-01/answer.md)；[统一消息](../../../runs/dsv4flash-db-first-full-01/dacomp-003/attempt-01/messages.jsonl)；[原始 OpenCode 事件](../../../runs/dsv4flash-db-first-full-01/dacomp-003/attempt-01/opencode.jsonl)；[SQL 引擎日志](../../../runs/dsv4flash-db-first-full-01/dacomp-003/attempt-01/sql_journal.jsonl)。

[可读报告（本地图片链接规范化）](../answers/dacomp-003.md)。原始回答保留，分析结论未改写。

## S1

类别 `connection_setup`；来源 `connection`；调用 `5fb8fcb23999477a902666c2d6f558f9`；状态 `success`。

```sql
PRAGMA query_only=ON
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-003/attempt-01/sql/S1.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-003/attempt-01/sql/S1.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-003/attempt-01/results/S1.rows.jsonl)；完整：True；SHA256：`e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`。

## S2

类别 `metadata`；来源 `list_db`；调用 `5fb8fcb23999477a902666c2d6f558f9`；状态 `success`。

```sql
SELECT name,sql FROM sqlite_master WHERE type='table' ORDER BY name
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-003/attempt-01/sql/S2.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-003/attempt-01/sql/S2.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-003/attempt-01/results/S2.rows.jsonl)；完整：True；SHA256：`1708f0c1d8309c0cfcc93df68355a7a5ed86a15510c48f896d8bc984ef9fc09d`。

## S3

类别 `data`；来源 `query_db`；调用 `0862b21df7584d1f8225cdf5d56fd17f`；状态 `success`。

```sql
SELECT COUNT(*) AS n FROM economic_indicator_data
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-003/attempt-01/sql/S3.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-003/attempt-01/sql/S3.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-003/attempt-01/results/S3.rows.jsonl)；完整：True；SHA256：`1d9d8bf38a316956dd3c85450e293ae57b99ad3ba6946d74c69eef0405a4a6bf`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "economic_indicator_data", "kind": "base", "block": null, "base_tables": ["economic_indicator_data"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |


## S4

类别 `data`；来源 `query_db`；调用 `37bf07506b5c4221a12e67962475fd52`；状态 `success`。

```sql
SELECT COUNT(*) AS n FROM sheet1
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-003/attempt-01/sql/S4.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-003/attempt-01/sql/S4.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-003/attempt-01/results/S4.rows.jsonl)；完整：True；SHA256：`1d9d8bf38a316956dd3c85450e293ae57b99ad3ba6946d74c69eef0405a4a6bf`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "sheet1", "kind": "base", "block": null, "base_tables": ["sheet1"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |


## S5

类别 `data`；来源 `query_db`；调用 `a54324340db842c88008d04dd3409c6d`；状态 `success`。

```sql
SELECT MIN("Year") AS min_year, MAX("Year") AS max_year, COUNT(DISTINCT "Year") AS n_years FROM sheet1
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-003/attempt-01/sql/S5.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-003/attempt-01/sql/S5.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-003/attempt-01/results/S5.rows.jsonl)；完整：True；SHA256：`1407bfc1fec7e9d1aa84e61807abd025329695d47bb8736d5c132182707adc73`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "sheet1", "kind": "base", "block": null, "base_tables": ["sheet1"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | MIN("Year") | [{"table": "sheet1", "column": "Year"}] | [] | False |
| B1 | MAX("Year") | [{"table": "sheet1", "column": "Year"}] | [] | False |
| B1 | COUNT(DISTINCT "Year") | [{"table": "sheet1", "column": "Year"}] | [] | False |


## S6

类别 `data`；来源 `query_db`；调用 `0d4f6738da454d949562623eeae6e869`；状态 `success`。

```sql
SELECT "Region Name", COUNT(*) AS n FROM sheet1 GROUP BY "Region Name" ORDER BY "Region Name"
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-003/attempt-01/sql/S6.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-003/attempt-01/sql/S6.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-003/attempt-01/results/S6.rows.jsonl)；完整：True；SHA256：`c0bcca42eb29f594b4d0728aeefd2a3ab03cd072d19532db67a2c656b7369fe1`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "sheet1", "kind": "base", "block": null, "base_tables": ["sheet1"]}] | [] | ["\"Region Name\""] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |


## S7

类别 `data`；来源 `query_db`；调用 `1e26cb7e72bd42d7a8a4a644a61f20a2`；状态 `success`。

```sql
SELECT * FROM sheet1 WHERE "Year" = 2020 ORDER BY "Region Name" LIMIT 8
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-003/attempt-01/sql/S7.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-003/attempt-01/sql/S7.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-003/attempt-01/results/S7.rows.jsonl)；完整：True；SHA256：`e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "sheet1", "kind": "base", "block": null, "base_tables": ["sheet1"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |


## S8

类别 `data`；来源 `query_db`；调用 `1fff4602c9454aac859c991229b74b94`；状态 `success`。

```sql
SELECT "Year" FROM sheet1 WHERE "Region Name" = 'China' ORDER BY "Year"
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-003/attempt-01/sql/S8.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-003/attempt-01/sql/S8.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-003/attempt-01/results/S8.rows.jsonl)；完整：True；SHA256：`9460d52f28d56b9a26ad0a5c7e7acfaab595d77d78bb8f5acee075b278b4b495`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "sheet1", "kind": "base", "block": null, "base_tables": ["sheet1"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |


## S9

类别 `data`；来源 `query_db`；调用 `0566bd12e7ae425584101ad271c407e5`；状态 `success`。

```sql
SELECT "Year" FROM sheet1 WHERE "Region Name" = 'Beijing Municipality' ORDER BY "Year"
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-003/attempt-01/sql/S9.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-003/attempt-01/sql/S9.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-003/attempt-01/results/S9.rows.jsonl)；完整：True；SHA256：`c4021fd163e5bc7da58a5857a7fcb7029c7c4b76e63cc5f64ff7c09e9abfbf23`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "sheet1", "kind": "base", "block": null, "base_tables": ["sheet1"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |


## S10

类别 `data`；来源 `query_db`；调用 `d00720531c9e45bd93285981d87ba9ec`；状态 `success`。

```sql
SELECT DISTINCT "Region Name" FROM sheet1 WHERE "Region Name" NOT LIKE '%Province%' AND "Region Name" NOT LIKE '%Municipality%' AND "Region Name" NOT LIKE '%Autonomous Region%' AND "Region Name" != 'China'
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-003/attempt-01/sql/S10.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-003/attempt-01/sql/S10.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-003/attempt-01/results/S10.rows.jsonl)；完整：True；SHA256：`e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "sheet1", "kind": "base", "block": null, "base_tables": ["sheet1"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |


## S11

类别 `data`；来源 `query_db`；调用 `30ab420942084f88be82ecddd91d52ed`；状态 `success`。

```sql
SELECT "Region Name", COUNT(DISTINCT "Year") AS ny, MIN("Year") AS miny, MAX("Year") AS maxy FROM sheet1 GROUP BY "Region Name" ORDER BY "Region Name"
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-003/attempt-01/sql/S11.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-003/attempt-01/sql/S11.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-003/attempt-01/results/S11.rows.jsonl)；完整：True；SHA256：`488e62e2a825ee65b714fc9d2ae66cee3fc98b6b887d30cb54ed08af3e00f598`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "sheet1", "kind": "base", "block": null, "base_tables": ["sheet1"]}] | [] | ["\"Region Name\""] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(DISTINCT "Year") | [{"table": "sheet1", "column": "Year"}] | [] | False |
| B1 | MIN("Year") | [{"table": "sheet1", "column": "Year"}] | [] | False |
| B1 | MAX("Year") | [{"table": "sheet1", "column": "Year"}] | [] | False |


## S12

类别 `data`；来源 `query_db`；调用 `cdf99c18448245d2b0f1817b195d5e2c`；状态 `success`。

```sql
SELECT MIN("Year") AS miny, MAX("Year") AS maxy, COUNT(DISTINCT "Year") AS ny FROM economic_indicator_data WHERE "Region Name" != 'China'
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-003/attempt-01/sql/S12.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-003/attempt-01/sql/S12.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-003/attempt-01/results/S12.rows.jsonl)；完整：True；SHA256：`18ce678e59d119de7c1b448527dd9edd1e74c629c7bd236749be04a141b91f69`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "economic_indicator_data", "kind": "base", "block": null, "base_tables": ["economic_indicator_data"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | MIN("Year") | [{"table": "economic_indicator_data", "column": "Year"}] | [] | False |
| B1 | MAX("Year") | [{"table": "economic_indicator_data", "column": "Year"}] | [] | False |
| B1 | COUNT(DISTINCT "Year") | [{"table": "economic_indicator_data", "column": "Year"}] | [] | False |


## S13

类别 `data`；来源 `query_db`；调用 `274837527cba4c3f939251514385f413`；状态 `success`。

```sql
SELECT MIN("Year") AS miny, MAX("Year") AS maxy, COUNT(DISTINCT "Year") AS ny FROM economic_indicator_data WHERE "Region Name" = 'China'
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-003/attempt-01/sql/S13.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-003/attempt-01/sql/S13.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-003/attempt-01/results/S13.rows.jsonl)；完整：True；SHA256：`1407bfc1fec7e9d1aa84e61807abd025329695d47bb8736d5c132182707adc73`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "economic_indicator_data", "kind": "base", "block": null, "base_tables": ["economic_indicator_data"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | MIN("Year") | [{"table": "economic_indicator_data", "column": "Year"}] | [] | False |
| B1 | MAX("Year") | [{"table": "economic_indicator_data", "column": "Year"}] | [] | False |
| B1 | COUNT(DISTINCT "Year") | [{"table": "economic_indicator_data", "column": "Year"}] | [] | False |


## S14

类别 `data`；来源 `query_db`；调用 `1aacc909b70d42ac88e068a66af6c7b4`；状态 `success`。

```sql
SELECT e."Year",
       e."Per capita GDP (yuan/person)" AS pc_gdp,
       s."Industrial Water Consumption (100 million m³)" AS ind_w,
       s."Total Water Consumption (100 million m³) " AS tot_w,
       ROUND(s."Industrial Water Consumption (100 million m³)" / s."Total Water Consumption (100 million m³) " * 100, 2) AS ind_share_pct
FROM sheet1 s
JOIN economic_indicator_data e ON e."Year" = s."Year" AND e."Region Name" = s."Region Name"
WHERE s."Region Name" = 'China'
ORDER BY e."Year"
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-003/attempt-01/sql/S14.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-003/attempt-01/sql/S14.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-003/attempt-01/results/S14.rows.jsonl)；完整：True；SHA256：`6da116d71316fd7557396033225e0bff04a9858de9647e4aeca256411671ffb1`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "s", "kind": "base", "block": null, "base_tables": ["sheet1"]}, {"alias": "e", "kind": "base", "block": null, "base_tables": ["economic_indicator_data"]}] | [{"type": "INNER", "right": "economic_indicator_data AS e", "on": "e.\"Year\" = s.\"Year\" AND e.\"Region Name\" = s.\"Region Name\"", "using": []}] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |


## S15

类别 `data`；来源 `query_db`；调用 `8caa57ea380c4f929c57b600b811d592`；状态 `success`。

```sql
SELECT COUNT(*) AS n, SUM(CASE WHEN s."Industrial Water Consumption (100 million m³)" IS NULL THEN 1 ELSE 0 END) AS null_ind,
       SUM(CASE WHEN s."Total Water Consumption (100 million m³) " IS NULL THEN 1 ELSE 0 END) AS null_tot,
       SUM(CASE WHEN e."Per capita GDP (yuan/person)" IS NULL THEN 1 ELSE 0 END) AS null_gdp
FROM sheet1 s LEFT JOIN economic_indicator_data e ON e."Year" = s."Year" AND e."Region Name" = s."Region Name"
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-003/attempt-01/sql/S15.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-003/attempt-01/sql/S15.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-003/attempt-01/results/S15.rows.jsonl)；完整：True；SHA256：`b8d578a3057086ac3a35f70bf658445d7c0c6b0f4d915d5f7ec3b00e202d32dd`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "s", "kind": "base", "block": null, "base_tables": ["sheet1"]}, {"alias": "e", "kind": "base", "block": null, "base_tables": ["economic_indicator_data"]}] | [{"type": "LEFT", "right": "economic_indicator_data AS e", "on": "e.\"Year\" = s.\"Year\" AND e.\"Region Name\" = s.\"Region Name\"", "using": []}] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |
| B1 | SUM(CASE WHEN s."Industrial Water Consumption (100 million m³)" IS NULL THEN 1 ELSE 0 END) | [] | [{"table": "sheet1", "column": "Industrial Water Consumption (100 million m³)"}] | False |
| B1 | SUM(CASE WHEN s."Total Water Consumption (100 million m³) " IS NULL THEN 1 ELSE 0 END) | [] | [{"table": "sheet1", "column": "Total Water Consumption (100 million m³) "}] | False |
| B1 | SUM(CASE WHEN e."Per capita GDP (yuan/person)" IS NULL THEN 1 ELSE 0 END) | [] | [{"table": "economic_indicator_data", "column": "Per capita GDP (yuan/person)"}] | False |


## S16

类别 `data`；来源 `query_db`；调用 `1e297f341cfa451081812f19e575687f`；状态 `success`。

```sql
SELECT e."Year",
       e."Per capita GDP (yuan/person)" AS pc_gdp,
       s."Industrial Water Consumption (100 million m³)" AS ind_w,
       s."Total Water Consumption (100 million m³) " AS tot_w,
       ROUND(s."Industrial Water Consumption (100 million m³)" / s."Total Water Consumption (100 million m³) " * 100, 2) AS ind_share_pct
FROM sheet1 s
JOIN economic_indicator_data e ON e."Year" = s."Year" AND e."Region Name" = s."Region Name"
WHERE s."Region Name" = 'China'
ORDER BY e."Year"
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-003/attempt-01/sql/S16.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-003/attempt-01/sql/S16.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-003/attempt-01/results/S16.rows.jsonl)；完整：True；SHA256：`6da116d71316fd7557396033225e0bff04a9858de9647e4aeca256411671ffb1`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "s", "kind": "base", "block": null, "base_tables": ["sheet1"]}, {"alias": "e", "kind": "base", "block": null, "base_tables": ["economic_indicator_data"]}] | [{"type": "INNER", "right": "economic_indicator_data AS e", "on": "e.\"Year\" = s.\"Year\" AND e.\"Region Name\" = s.\"Region Name\"", "using": []}] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |


## S17

类别 `data`；来源 `query_db`；调用 `c2d554146cc745babf7be6143555b2a4`；状态 `success`。

```sql
SELECT e."Region Name",
       e."Year",
       e."Per capita GDP (yuan/person)" AS pc_gdp,
       s."Industrial Water Consumption (100 million m³)" / s."Total Water Consumption (100 million m³) " * 100 AS ind_share_pct
FROM sheet1 s
JOIN economic_indicator_data e ON e."Year" = s."Year" AND e."Region Name" = s."Region Name"
WHERE s."Region Name" != 'China'
ORDER BY e."Region Name", e."Year"
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-003/attempt-01/sql/S17.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-003/attempt-01/sql/S17.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-003/attempt-01/results/S17.rows.jsonl)；完整：True；SHA256：`e116299fa31892babc4dfcf6f6a8d70cd9e1934ec23cf1ddfff97b35bba4f50a`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "s", "kind": "base", "block": null, "base_tables": ["sheet1"]}, {"alias": "e", "kind": "base", "block": null, "base_tables": ["economic_indicator_data"]}] | [{"type": "INNER", "right": "economic_indicator_data AS e", "on": "e.\"Year\" = s.\"Year\" AND e.\"Region Name\" = s.\"Region Name\"", "using": []}] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |


## S18

类别 `data`；来源 `python`；调用 `fb41db46fa694f76aba2fde90faa65a8`；状态 `success`。

```sql

SELECT e."Year" AS year,
       e."Per capita GDP (yuan/person)" AS pc_gdp,
       s."Industrial Water Consumption (100 million m³)" AS ind_w,
       s."Total Water Consumption (100 million m³) " AS tot_w,
       s."Industrial Water Consumption (100 million m³)" / s."Total Water Consumption (100 million m³) " * 100 AS ind_share
FROM sheet1 s
JOIN economic_indicator_data e ON e."Year" = s."Year" AND e."Region Name" = s."Region Name"
WHERE s."Region Name" = 'China'
ORDER BY e."Year"

```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-003/attempt-01/sql/S18.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-003/attempt-01/sql/S18.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-003/attempt-01/results/S18.rows.jsonl)；完整：True；SHA256：`a48eeb425f36d6bb1bdfa239f7cb1db1808bb324ddc5b0961bcab372042da675`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "s", "kind": "base", "block": null, "base_tables": ["sheet1"]}, {"alias": "e", "kind": "base", "block": null, "base_tables": ["economic_indicator_data"]}] | [{"type": "INNER", "right": "economic_indicator_data AS e", "on": "e.\"Year\" = s.\"Year\" AND e.\"Region Name\" = s.\"Region Name\"", "using": []}] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |


## S19

类别 `data`；来源 `python`；调用 `fb41db46fa694f76aba2fde90faa65a8`；状态 `success`。

```sql

SELECT e."Region Name" AS region, e."Year" AS year,
       e."Per capita GDP (yuan/person)" AS pc_gdp,
       s."Industrial Water Consumption (100 million m³)" / s."Total Water Consumption (100 million m³) " * 100 AS ind_share
FROM sheet1 s
JOIN economic_indicator_data e ON e."Year" = s."Year" AND e."Region Name" = s."Region Name"
WHERE s."Region Name" != 'China'
ORDER BY e."Region Name", e."Year"

```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-003/attempt-01/sql/S19.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-003/attempt-01/sql/S19.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-003/attempt-01/results/S19.rows.jsonl)；完整：True；SHA256：`e116299fa31892babc4dfcf6f6a8d70cd9e1934ec23cf1ddfff97b35bba4f50a`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "s", "kind": "base", "block": null, "base_tables": ["sheet1"]}, {"alias": "e", "kind": "base", "block": null, "base_tables": ["economic_indicator_data"]}] | [{"type": "INNER", "right": "economic_indicator_data AS e", "on": "e.\"Year\" = s.\"Year\" AND e.\"Region Name\" = s.\"Region Name\"", "using": []}] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |


## S20

类别 `data`；来源 `python`；调用 `4d65c83b5e124835a0dd85ea7c038956`；状态 `success`。

```sql

SELECT e."Year" AS year, e."Per capita GDP (yuan/person)" AS pc_gdp,
       s."Industrial Water Consumption (100 million m³)" / s."Total Water Consumption (100 million m³) " * 100 AS ind_share
FROM sheet1 s JOIN economic_indicator_data e ON e."Year" = s."Year" AND e."Region Name" = s."Region Name"
WHERE s."Region Name" = 'China' ORDER BY e."Year"

```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-003/attempt-01/sql/S20.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-003/attempt-01/sql/S20.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-003/attempt-01/results/S20.rows.jsonl)；完整：True；SHA256：`a03e94f1b7de269b33318b50c4987b5d0222e2b9bc9661d21f0dd21ad228965b`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "s", "kind": "base", "block": null, "base_tables": ["sheet1"]}, {"alias": "e", "kind": "base", "block": null, "base_tables": ["economic_indicator_data"]}] | [{"type": "INNER", "right": "economic_indicator_data AS e", "on": "e.\"Year\" = s.\"Year\" AND e.\"Region Name\" = s.\"Region Name\"", "using": []}] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |


## S21

类别 `data`；来源 `python`；调用 `4d65c83b5e124835a0dd85ea7c038956`；状态 `success`。

```sql

SELECT e."Region Name" AS region, e."Year" AS year,
       e."Per capita GDP (yuan/person)" AS pc_gdp,
       s."Industrial Water Consumption (100 million m³)" / s."Total Water Consumption (100 million m³) " * 100 AS ind_share
FROM sheet1 s JOIN economic_indicator_data e ON e."Year" = s."Year" AND e."Region Name" = s."Region Name"
WHERE s."Region Name" != 'China' ORDER BY e."Region Name", e."Year"

```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-003/attempt-01/sql/S21.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-003/attempt-01/sql/S21.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-003/attempt-01/results/S21.rows.jsonl)；完整：True；SHA256：`e116299fa31892babc4dfcf6f6a8d70cd9e1934ec23cf1ddfff97b35bba4f50a`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "s", "kind": "base", "block": null, "base_tables": ["sheet1"]}, {"alias": "e", "kind": "base", "block": null, "base_tables": ["economic_indicator_data"]}] | [{"type": "INNER", "right": "economic_indicator_data AS e", "on": "e.\"Year\" = s.\"Year\" AND e.\"Region Name\" = s.\"Region Name\"", "using": []}] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |


## S22

类别 `data`；来源 `python`；调用 `c9ac6f9dbcba49198e1f278b8a6e5815`；状态 `success`。

```sql

SELECT e."Year" AS year, e."Per capita GDP (yuan/person)" AS pc_gdp,
       s."Industrial Water Consumption (100 million m³)" / s."Total Water Consumption (100 million m³) " * 100 AS ind_share
FROM sheet1 s JOIN economic_indicator_data e ON e."Year" = s."Year" AND e."Region Name" = s."Region Name"
WHERE s."Region Name" = 'China' ORDER BY e."Year"

```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-003/attempt-01/sql/S22.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-003/attempt-01/sql/S22.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-003/attempt-01/results/S22.rows.jsonl)；完整：True；SHA256：`a03e94f1b7de269b33318b50c4987b5d0222e2b9bc9661d21f0dd21ad228965b`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "s", "kind": "base", "block": null, "base_tables": ["sheet1"]}, {"alias": "e", "kind": "base", "block": null, "base_tables": ["economic_indicator_data"]}] | [{"type": "INNER", "right": "economic_indicator_data AS e", "on": "e.\"Year\" = s.\"Year\" AND e.\"Region Name\" = s.\"Region Name\"", "using": []}] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |


## S23

类别 `data`；来源 `python`；调用 `c9ac6f9dbcba49198e1f278b8a6e5815`；状态 `success`。

```sql

SELECT e."Region Name" AS region, e."Year" AS year,
       e."Per capita GDP (yuan/person)" AS pc_gdp,
       s."Industrial Water Consumption (100 million m³)" / s."Total Water Consumption (100 million m³) " * 100 AS ind_share
FROM sheet1 s JOIN economic_indicator_data e ON e."Year" = s."Year" AND e."Region Name" = s."Region Name"
WHERE s."Region Name" != 'China' ORDER BY e."Region Name", e."Year"

```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-003/attempt-01/sql/S23.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-003/attempt-01/sql/S23.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-003/attempt-01/results/S23.rows.jsonl)；完整：True；SHA256：`e116299fa31892babc4dfcf6f6a8d70cd9e1934ec23cf1ddfff97b35bba4f50a`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "s", "kind": "base", "block": null, "base_tables": ["sheet1"]}, {"alias": "e", "kind": "base", "block": null, "base_tables": ["economic_indicator_data"]}] | [{"type": "INNER", "right": "economic_indicator_data AS e", "on": "e.\"Year\" = s.\"Year\" AND e.\"Region Name\" = s.\"Region Name\"", "using": []}] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |


## S24

类别 `data`；来源 `python`；调用 `a5e30831daac44d2a62a17ea3620d04f`；状态 `success`。

```sql

SELECT e."Region Name" AS region, e."Year" AS year,
       e."Per capita GDP (yuan/person)" AS pc_gdp,
       s."Industrial Water Consumption (100 million m³)" / s."Total Water Consumption (100 million m³) " * 100 AS ind_share
FROM sheet1 s JOIN economic_indicator_data e ON e."Year" = s."Year" AND e."Region Name" = s."Region Name"
WHERE s."Region Name" != 'China' ORDER BY e."Region Name", e."Year"

```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-003/attempt-01/sql/S24.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-003/attempt-01/sql/S24.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-003/attempt-01/results/S24.rows.jsonl)；完整：True；SHA256：`e116299fa31892babc4dfcf6f6a8d70cd9e1934ec23cf1ddfff97b35bba4f50a`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "s", "kind": "base", "block": null, "base_tables": ["sheet1"]}, {"alias": "e", "kind": "base", "block": null, "base_tables": ["economic_indicator_data"]}] | [{"type": "INNER", "right": "economic_indicator_data AS e", "on": "e.\"Year\" = s.\"Year\" AND e.\"Region Name\" = s.\"Region Name\"", "using": []}] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |


## S25

类别 `data`；来源 `python`；调用 `b28d95bebd7d48e6ab2c1ebbdbb7dbb6`；状态 `success`。

```sql

SELECT e."Region Name" AS region, e."Year" AS year,
       e."Per capita GDP (yuan/person)" AS pc_gdp,
       s."Industrial Water Consumption (100 million m³)" / s."Total Water Consumption (100 million m³) " * 100 AS ind_share
FROM sheet1 s JOIN economic_indicator_data e ON e."Year" = s."Year" AND e."Region Name" = s."Region Name"
WHERE s."Region Name" != 'China' ORDER BY e."Region Name", e."Year"

```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-003/attempt-01/sql/S25.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-003/attempt-01/sql/S25.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-003/attempt-01/results/S25.rows.jsonl)；完整：True；SHA256：`e116299fa31892babc4dfcf6f6a8d70cd9e1934ec23cf1ddfff97b35bba4f50a`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "s", "kind": "base", "block": null, "base_tables": ["sheet1"]}, {"alias": "e", "kind": "base", "block": null, "base_tables": ["economic_indicator_data"]}] | [{"type": "INNER", "right": "economic_indicator_data AS e", "on": "e.\"Year\" = s.\"Year\" AND e.\"Region Name\" = s.\"Region Name\"", "using": []}] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |


## S26

类别 `data`；来源 `python`；调用 `07fa85b0fe98499da1f1b6ee36b8c85f`；状态 `success`。

```sql

SELECT e."Region Name" AS region, e."Year" AS year,
       e."Per capita GDP (yuan/person)" AS pc_gdp,
       s."Industrial Water Consumption (100 million m³)" / s."Total Water Consumption (100 million m³) " * 100 AS ind_share
FROM sheet1 s JOIN economic_indicator_data e ON e."Year" = s."Year" AND e."Region Name" = s."Region Name"
WHERE s."Region Name" != 'China' ORDER BY e."Region Name", e."Year"

```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-003/attempt-01/sql/S26.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-003/attempt-01/sql/S26.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-003/attempt-01/results/S26.rows.jsonl)；完整：True；SHA256：`e116299fa31892babc4dfcf6f6a8d70cd9e1934ec23cf1ddfff97b35bba4f50a`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "s", "kind": "base", "block": null, "base_tables": ["sheet1"]}, {"alias": "e", "kind": "base", "block": null, "base_tables": ["economic_indicator_data"]}] | [{"type": "INNER", "right": "economic_indicator_data AS e", "on": "e.\"Year\" = s.\"Year\" AND e.\"Region Name\" = s.\"Region Name\"", "using": []}] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |

