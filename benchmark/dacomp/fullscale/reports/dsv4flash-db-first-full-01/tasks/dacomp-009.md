# dacomp-009

If we produce an integrated ranking that considers Effective Working Hours, overall Units …

运行：已提交。官方未评分。全部 SQL 尝试/成功 36/36；数据 SQL 34/34；Python 8 次。

完整原题：

If we produce an integrated ranking that considers Effective Working Hours, overall Units Produced, and production quality, analyze the characteristics of the current top employees and provide recommendations on the candidate profile we should recruit next.

| 表 | 行数 | 列数 |
| --- | --- | --- |
| sheet1 | 483 | 20 |
| sheet2 | 525 | 20 |
| sheet3 | 503 | 20 |
| sheet4 | 483 | 20 |
| sheet5 | 502 | 20 |
| sheet6 | 537 | 20 |


实际路线（分析者依据 SQL/源码概括，不代表 Agent 自述）：汇总员工产出、工时和合格率并生成初始排名 → 合并薪资与纪律记录 → 比较前十名和其余员工的特征 → 改权重检查排名敏感性 → 绘制群体差异。

数据库大小：995,328 字节。

## 数据 SQL

| SQL | 状态 | 基础表 | Join 输入/类型 | GROUP BY | 聚合表达式 | 结果行数 | 数据库 ms |
| --- | --- | --- | --- | --- | --- | --- | --- |
| [S3/Q1](#s3) | success | ["sheet1", "sheet2", "sheet3", "sheet4", "sheet5", "sheet6"] | 0 / {} | [] | ["COUNT(*)", "COUNT(*)", "COUNT(*)", "COUNT(*)", "COUNT(*)", "COUNT(*)"] | 6 | 0.938 |
| [S4/Q2](#s4) | success | ["sheet1"] | 0 / {} | [] | [] | 10 | 0.387 |
| [S5/Q3](#s5) | success | ["sheet1"] | 0 / {} | [] | [] | 1 | 0.449 |
| [S6/Q4](#s6) | success | ["sheet1", "sheet2", "sheet3", "sheet4", "sheet5", "sheet6"] | 0 / {} | [] | ["MIN(Date)", "MAX(Date)", "COUNT(DISTINCT \"Employee\")", "MIN(Date)", "MAX(Date)", "COUNT(DISTINCT \"Employee\")", "MIN(Date)", "MAX(Date)", "COUNT(DISTINCT \"Employee\")", "MIN(Date)", "MAX(Date)", "COUNT(DISTINCT \"Employee\")", "MIN(Date)", "MAX(Date)", "COUNT(DISTINCT \"Employee\")", "MIN(Date)", "MAX(Date)", "COUNT(DISTINCT \"Employee\")"] | 6 | 1.667 |
| [S7/Q5](#s7) | success | ["sheet1"] | 0 / {} | [] | [] | 4 | 0.427 |
| [S8/Q6](#s8) | success | ["sheet1"] | 0 / {} | [] | [] | 1 | 0.405 |
| [S9/Q7](#s9) | success | ["sheet1"] | 0 / {} | ["\"Employee\""] | ["COUNT(*)", "COUNT(DISTINCT \"Employee ID\")"] | 9 | 0.601 |
| [S10/Q8](#s10) | success | ["sheet1"] | 0 / {} | ["\"Employee ID\"", "\"Employee\"", "Team"] | [] | 24 | 0.621 |
| [S11/Q9](#s11) | success | ["sheet1", "sheet2", "sheet3", "sheet4", "sheet5", "sheet6"] | 0 / {} | [] | ["COUNT(*)", "COUNT(DISTINCT \"Employee ID\")"] | 1 | 1.234 |
| [S12/Q10](#s12) | success | ["sheet1", "sheet2", "sheet3", "sheet4", "sheet5", "sheet6"] | 0 / {} | ["Team"] | ["COUNT(DISTINCT \"Employee ID\")"] | 3 | 1.753 |
| [S13/Q11](#s13) | success | ["sheet2"] | 0 / {} | ["\"Employee\"", "\"Employee ID\"", "Team"] | [] | 22 | 0.741 |
| [S14/Q12](#s14) | success | ["sheet1"] | 0 / {} | ["\"Total Time Away\""] | ["COUNT(*)"] | 30 | 0.681 |
| [S15/Q13](#s15) | success | ["sheet1"] | 0 / {} | ["\"Pass Rate\""] | ["COUNT(*)"] | 8 | 0.53 |
| [S16/Q14](#s16) | success | ["sheet1"] | 0 / {} | ["\"Hire Date\""] | ["COUNT(*)"] | 17 | 0.529 |
| [S17/Q15](#s17) | success | ["sheet1"] | 0 / {} | [] | [] | 0 | 0.41 |
| [S18/Q16](#s18) | success | ["sheet1"] | 0 / {} | ["\"Disciplinary Issue\""] | ["COUNT(*)"] | 2 | 0.467 |
| [S19/Q17](#s19) | success | ["sheet1"] | 0 / {} | ["\"Payment Method\""] | ["COUNT(*)"] | 1 | 0.451 |
| [S20/Q18](#s20) | success | ["sheet1", "sheet2", "sheet3", "sheet4", "sheet5", "sheet6"] | 0 / {} | ["\"Employee ID\"", "\"Employee\"", "Team", "\"Gender\"", "Age", "\"Education Level\"", "\"Hire Date\""] | ["COUNT(*)", "SUM(CASE WHEN \"Disciplinary Issue\" = 'Yes' THEN 1 ELSE 0 END)", "SUM(eff_hours)", "AVG(eff_hours)", "SUM(units)", "AVG(units)", "AVG(pass_pct)"] | 136 | 9.979 |
| [S21/Q19](#s21) | success | ["sheet1", "sheet2", "sheet3", "sheet4", "sheet5", "sheet6"] | 0 / {} | ["\"Employee ID\"", "\"Employee\"", "Team", "\"Gender\"", "Age", "\"Education Level\""] | ["MAX(CAST(REPLACE(\"Hire Date\", ' months', '') AS INTEGER))", "COUNT(*)", "SUM(CASE WHEN \"Disciplinary Issue\" = 'Yes' THEN 1 ELSE 0 END)", "SUM(eff_hours)", "AVG(eff_hours)", "SUM(units)", "AVG(units)", "AVG(pass_pct)"] | 68 | 9.624 |
| [S22/Q20](#s22) | success | ["sheet1", "sheet2", "sheet3", "sheet4", "sheet5", "sheet6"] | 2 / {'CROSS': 1} | ["\"Employee ID\"", "\"Employee\"", "Team", "\"Gender\"", "Age", "\"Education Level\""] | ["MAX(CAST(REPLACE(\"Hire Date\", ' months', '') AS INTEGER))", "COUNT(*)", "SUM(eff_hours)", "SUM(units)", "AVG(pass_pct)", "SUM(CASE WHEN \"Disciplinary Issue\" = 'Yes' THEN 1 ELSE 0 END)", "MIN(total_eff_hours)", "MAX(total_eff_hours)", "MIN(total_units)", "MAX(total_units)", "MIN(avg_pass_rate)", "MAX(avg_pass_rate)"] | 68 | 10.323 |
| [S23/Q21](#s23) | success | ["sheet1", "sheet2", "sheet3", "sheet4", "sheet5", "sheet6"] | 2 / {'CROSS': 1} | ["\"Employee ID\"", "\"Employee\"", "Team", "\"Gender\"", "Age", "\"Education Level\""] | ["MAX(CAST(REPLACE(\"Hire Date\", ' months', '') AS INTEGER))", "COUNT(*)", "SUM(eff_hours)", "SUM(units)", "AVG(units)", "AVG(pass_pct)", "SUM(CASE WHEN \"Disciplinary Issue\" = 'Yes' THEN 1 ELSE 0 END)", "MIN(total_eff_hours)", "MAX(total_eff_hours)", "MIN(total_units)", "MAX(total_units)", "MIN(avg_pass_rate)", "MAX(avg_pass_rate)"] | 25 | 10.678 |
| [S24/Q22](#s24) | success | ["sheet1"] | 0 / {} | ["Gender"] | ["COUNT(*)"] | 2 | 0.493 |
| [S25/Q23](#s25) | success | ["sheet1", "sheet2", "sheet3", "sheet4", "sheet5", "sheet6"] | 0 / {} | ["\"Gender\""] | ["COUNT(DISTINCT \"Employee ID\")"] | 2 | 1.338 |
| [S26/Q24](#s26) | success | ["sheet1", "sheet2", "sheet3", "sheet4", "sheet5", "sheet6"] | 0 / {} | ["Team"] | ["COUNT(DISTINCT \"Employee ID\")"] | 3 | 1.288 |
| [S27/Q25](#s27) | success | ["sheet1", "sheet2", "sheet3", "sheet4", "sheet5", "sheet6"] | 2 / {'CROSS': 1} | ["\"Employee ID\"", "\"Employee\"", "Team", "\"Gender\"", "Age", "\"Education Level\""] | ["MAX(CAST(REPLACE(\"Hire Date\", ' months', '') AS INTEGER))", "COUNT(*)", "SUM(eff_hours)", "SUM(units)", "AVG(units)", "AVG(pass_pct)", "SUM(CASE WHEN \"Disciplinary Issue\" = 'Yes' THEN 1 ELSE 0 END)", "MIN(total_eff_hours)", "MAX(total_eff_hours)", "MIN(total_units)", "MAX(total_units)", "MIN(avg_pass_rate)", "MAX(avg_pass_rate)"] | 68 | 10.793 |
| [S28/Q26](#s28) | success | ["sheet1", "sheet2", "sheet3", "sheet4", "sheet5", "sheet6"] | 2 / {'CROSS': 1} | ["\"Employee ID\"", "\"Employee\"", "Team", "\"Gender\"", "Age", "\"Education Level\"", "\"Gender\""] | ["MAX(CAST(REPLACE(\"Hire Date\", ' months', '') AS INTEGER))", "COUNT(*)", "SUM(eff_hours)", "SUM(units)", "AVG(pass_pct)", "SUM(CASE WHEN \"Disciplinary Issue\" = 'Yes' THEN 1 ELSE 0 END)", "MIN(total_eff_hours)", "MAX(total_eff_hours)", "MIN(total_units)", "MAX(total_units)", "MIN(avg_pass_rate)", "MAX(avg_pass_rate)", "COUNT(*)", "SUM(CASE WHEN rank <= 10 THEN 1 ELSE 0 END)", "SUM(CASE WHEN rank <= 20 THEN 1 ELSE 0 END)", "AVG(rank)"] | 2 | 10.65 |
| [S29/Q27](#s29) | success | ["sheet1", "sheet2", "sheet3", "sheet4", "sheet5", "sheet6"] | 0 / {} | ["\"Employee ID\"", "\"Employee\""] | [] | 68 | 2.976 |
| [S30/Q28](#s30) | success | ["sheet1", "sheet2", "sheet3", "sheet4", "sheet5", "sheet6"] | 0 / {} | ["Team", "\"Gender\""] | ["COUNT(DISTINCT \"Employee ID\")", "AVG(units)"] | 6 | 3.405 |
| [S31/Q29](#s31) | success | ["sheet1", "sheet2", "sheet3", "sheet4", "sheet5", "sheet6"] | 0 / {} | ["\"Workstation ID\""] | ["COUNT(DISTINCT \"Employee ID\")", "MIN(\"Gender\")", "AVG(units)"] | 15 | 3.136 |
| [S32/Q30](#s32) | success | ["sheet1", "sheet2", "sheet3", "sheet4", "sheet5", "sheet6"] | 0 / {} | ["\"Gender\""] | ["COUNT(*)", "AVG(units)", "AVG(eff_hours)", "AVG(away_cnt)", "AVG(8.0 - eff_hours)"] | 2 | 4.194 |
| [S33/Q31](#s33) | success | ["sheet1", "sheet2", "sheet3", "sheet4", "sheet5", "sheet6"] | 0 / {} | ["\"Employee ID\"", "month"] | ["COUNT(*)", "SUM(units)", "AVG(pass_pct)"] | 136 | 3.765 |
| [S34/Q32](#s34) | success | ["sheet1"] | 0 / {} | [] | ["MIN(\"Units Produced\")", "MAX(\"Units Produced\")", "COUNT(*)", "COUNT(CASE WHEN \"Units Produced\" <= 0 THEN 1 END)"] | 1 | 0.511 |
| [S35/Q33](#s35) | success | ["sheet1", "sheet2", "sheet3", "sheet4", "sheet5", "sheet6"] | 0 / {} | ["\"Gender\""] | ["COUNT(*)", "AVG(away_cnt)", "MIN(away_cnt)", "MAX(away_cnt)"] | 2 | 2.309 |
| [S36/Q34](#s36) | success | ["sheet1", "sheet2", "sheet3", "sheet4", "sheet5", "sheet6"] | 0 / {} | ["\"Reason for Infraction\"", "\"Gender\""] | ["COUNT(*)"] | 11 | 1.18 |


## 元数据和设置

| SQL | 类别 | 状态 | 内容 |
| --- | --- | --- | --- |
| S1 | connection_setup | success | PRAGMA query_only=ON |
| S2 | metadata | success | SELECT name,sql FROM sqlite_master WHERE type='table' ORDER BY name |


## Python 与执行位置

人工源码审查：**database_first_violation**。P4/P6 join archived employee results, construct percentile ranks and weighted-score scenarios, and aggregate profiles in pandas. These relational operations are reasonably supported by SQLite. Statistical tests and figure rendering are separate justified Python uses; SQL data retrieval remained logged. [证据](../reviews/dacomp-009.json)。

P1：I need to run statistical comparisons and create visualizations of the top performers' profile versus the rest, which require statistical distributions and plots that go beyond SQL aggregation capabilities.

[源码](../../../runs/dsv4flash-db-first-full-01/dacomp-009/attempt-01/python/P1.py)；[输出](../../../runs/dsv4flash-db-first-full-01/dacomp-009/attempt-01/python/P1.stdout)；[错误](../../../runs/dsv4flash-db-first-full-01/dacomp-009/attempt-01/python/P1.stderr)。自动源码筛查未检出预设迁出信号；这不是全面语义合规证明。

P2：I need to merge salary data with the ranked employee data and perform statistical analysis (t-tests, distribution comparisons, correlation analysis) and create visualizations that cannot be done in SQL alone.

[源码](../../../runs/dsv4flash-db-first-full-01/dacomp-009/attempt-01/python/P2.py)；[输出](../../../runs/dsv4flash-db-first-full-01/dacomp-009/attempt-01/python/P2.stdout)；[错误](../../../runs/dsv4flash-db-first-full-01/dacomp-009/attempt-01/python/P2.stderr)。检出需人工核验的 SQL 可实现操作：groupby(, .merge(, sort_values(；不能仅凭理由判为合规。

P3：I need to compute per-employee productivity ratios (units per effective hour), test the significance of gender differences, and examine tradeoffs between output and quality — statistical computations better done in Python with the already-archived row-level data.

[源码](../../../runs/dsv4flash-db-first-full-01/dacomp-009/attempt-01/python/P3.py)；[输出](../../../runs/dsv4flash-db-first-full-01/dacomp-009/attempt-01/python/P3.stdout)；[错误](../../../runs/dsv4flash-db-first-full-01/dacomp-009/attempt-01/python/P3.stderr)。检出需人工核验的 SQL 可实现操作：groupby(, .merge(, sort_values(；不能仅凭理由判为合规。

P4：Fixing the column access issue (the 'rank' column name shadows pandas' .rank method) and completing the profile analysis and tradeoff examination in Python.

[源码](../../../runs/dsv4flash-db-first-full-01/dacomp-009/attempt-01/python/P4.py)；[输出](../../../runs/dsv4flash-db-first-full-01/dacomp-009/attempt-01/python/P4.stdout)；[错误](../../../runs/dsv4flash-db-first-full-01/dacomp-009/attempt-01/python/P4.stderr)。检出需人工核验的 SQL 可实现操作：groupby(, .merge(, sort_values(；不能仅凭理由判为合规。

P5：I need to verify the robustness of the integrated ranking to different weightings and normalization schemes, and check for confounds (team, education) in the gender effect — this requires iterative statistical computation best done in Python rather than many SQL queries.

[源码](../../../runs/dsv4flash-db-first-full-01/dacomp-009/attempt-01/python/P5.py)；[输出](../../../runs/dsv4flash-db-first-full-01/dacomp-009/attempt-01/python/P5.stdout)；[错误](../../../runs/dsv4flash-db-first-full-01/dacomp-009/attempt-01/python/P5.stderr)。检出需人工核验的 SQL 可实现操作：groupby(, .merge(；不能仅凭理由判为合规。

P6：Fixing a syntax error and completing the sensitivity/robustness analysis of the integrated ranking in Python.

[源码](../../../runs/dsv4flash-db-first-full-01/dacomp-009/attempt-01/python/P6.py)；[输出](../../../runs/dsv4flash-db-first-full-01/dacomp-009/attempt-01/python/P6.stdout)；[错误](../../../runs/dsv4flash-db-first-full-01/dacomp-009/attempt-01/python/P6.stderr)。检出需人工核验的 SQL 可实现操作：groupby(, .merge(, sort_values(；不能仅凭理由判为合规。

P7：I need to compute month-over-month stability of performance for top employees, which requires reshaping the monthly data and computing correlations across months - a Python operation rather than SQL.

[源码](../../../runs/dsv4flash-db-first-full-01/dacomp-009/attempt-01/python/P7.py)；[输出](../../../runs/dsv4flash-db-first-full-01/dacomp-009/attempt-01/python/P7.stdout)；[错误](../../../runs/dsv4flash-db-first-full-01/dacomp-009/attempt-01/python/P7.stderr)。检出需人工核验的 SQL 可实现操作：sort_values(；不能仅凭理由判为合规。

P8：Creating a summary visualization comparing top performers vs the rest on recruitment-relevant attributes (age, tenure, education, accommodation, gender composition, productivity and quality) for the final report.

[源码](../../../runs/dsv4flash-db-first-full-01/dacomp-009/attempt-01/python/P8.py)；[输出](../../../runs/dsv4flash-db-first-full-01/dacomp-009/attempt-01/python/P8.stdout)；[错误](../../../runs/dsv4flash-db-first-full-01/dacomp-009/attempt-01/python/P8.stderr)。检出需人工核验的 SQL 可实现操作：groupby(, .merge(, sort_values(；不能仅凭理由判为合规。

## 优化机会

已验证候选。筛选限于精确 SQL、相同自包含 CTE、相同单表完整过滤、可分解单表聚合；未覆盖任意 Join 等价和一般谓词蕴含。全部候选都是 offline，未测在线预测。

| 候选 | 类型 | 已有结果 | 覆盖 SQL | 后续次数 | 中间行数 | 验证 | 成本 |
| --- | --- | --- | --- | --- | --- | --- | --- |
| C1 | aggregate MV | False | ["S14", "S15", "S16", "S18", "S19", "S34"] | 5 | 479 | verified | Not benchmarked; correctness alone does not establish net speedup. |


已验证覆盖（含触发查询、候选并集去重）：6/34 条成功数据 SQL。正确性仅针对当前数据库快照；未测性能的候选不能声称已加速。

[完整 build/rewrite 与比较证据](dacomp-009.analysis.json)。

### C1：aggregate MV

Union of grouping keys; decomposable aggregate states; AVG uses SUM and non-NULL COUNT.

原查询 [S14](#s14), [S15](#s15), [S16](#s16), [S18](#s18), [S19](#s19), [S34](#s34) → 新增共享状态 C1 → 后续 5 次可复用。该构建点为事后假设，不代表 Agent 当时预知后续。

构建定义：

```sql
SELECT "Total Time Away" AS __g0, "Pass Rate" AS __g1, "Hire Date" AS __g2, "Disciplinary Issue" AS __g3, "Payment Method" AS __g4, COUNT(*) AS __a0, MIN("Units Produced") AS __a1, MAX("Units Produced") AS __a2, COUNT(CASE WHEN "Units Produced" <= 0 THEN 1 END) AS __a3 FROM "sheet1"  GROUP BY "Total Time Away", "Pass Rate", "Hire Date", "Disciplinary Issue", "Payment Method"
```

受益查询 S14 的改写示例：

```sql
SELECT __g0 AS "Total Time Away", SUM(__a0) AS cnt FROM temp.reuse_candidate GROUP BY __g0 ORDER BY cnt DESC LIMIT 30
```

| 原 SQL | 列名一致 | 结果一致 | 比较方法 |
| --- | --- | --- | --- |
| S14 | True | True | ordered_numeric_tolerance |
| S15 | True | True | ordered_numeric_tolerance |
| S16 | True | True | ordered_numeric_tolerance |
| S18 | True | True | exact_multiset |
| S19 | True | True | exact_multiset |
| S34 | True | True | exact_multiset |


验证状态：verified；成本结论：Not benchmarked; correctness alone does not establish net speedup.

结果依赖：自动记录 SQL→Python 的接口父调用，以及源码中引用归档文件的消费者；字面值相同不认定因果。模型方向选择需要人工读取消息，尚未做全面因果标注。

[原始报告](../../../runs/dsv4flash-db-first-full-01/dacomp-009/attempt-01/answer.md)；[统一消息](../../../runs/dsv4flash-db-first-full-01/dacomp-009/attempt-01/messages.jsonl)；[原始 OpenCode 事件](../../../runs/dsv4flash-db-first-full-01/dacomp-009/attempt-01/opencode.jsonl)；[SQL 引擎日志](../../../runs/dsv4flash-db-first-full-01/dacomp-009/attempt-01/sql_journal.jsonl)。

[可读报告（本地图片链接规范化）](../answers/dacomp-009.md)。原始回答保留，分析结论未改写。

## S1

类别 `connection_setup`；来源 `connection`；调用 `1f7c54657f844f5db39d2a4d98fa523e`；状态 `success`。

```sql
PRAGMA query_only=ON
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-009/attempt-01/sql/S1.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-009/attempt-01/sql/S1.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-009/attempt-01/results/S1.rows.jsonl)；完整：True；SHA256：`e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`。

## S2

类别 `metadata`；来源 `list_db`；调用 `1f7c54657f844f5db39d2a4d98fa523e`；状态 `success`。

```sql
SELECT name,sql FROM sqlite_master WHERE type='table' ORDER BY name
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-009/attempt-01/sql/S2.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-009/attempt-01/sql/S2.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-009/attempt-01/results/S2.rows.jsonl)；完整：True；SHA256：`92e5aab3408f0b05d05ddbd75b38698aadbf176454119ebe5a178af89742af33`。

## S3

类别 `data`；来源 `query_db`；调用 `a4c9bf5116ff4b19a50249db27b5522c`；状态 `success`。

```sql
SELECT 'sheet1' AS tbl, COUNT(*) AS n FROM sheet1
UNION ALL SELECT 'sheet2', COUNT(*) FROM sheet2
UNION ALL SELECT 'sheet3', COUNT(*) FROM sheet3
UNION ALL SELECT 'sheet4', COUNT(*) FROM sheet4
UNION ALL SELECT 'sheet5', COUNT(*) FROM sheet5
UNION ALL SELECT 'sheet6', COUNT(*) FROM sheet6
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-009/attempt-01/sql/S3.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-009/attempt-01/sql/S3.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-009/attempt-01/results/S3.rows.jsonl)；完整：True；SHA256：`a0dc7eda7849ce1f0f2482921827eb7af83eaa9998eaf300826f18e3ce1c2a62`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "sheet1", "kind": "base", "block": null, "base_tables": ["sheet1"]}] | [] | [] |
| B2 | [{"alias": "sheet2", "kind": "base", "block": null, "base_tables": ["sheet2"]}] | [] | [] |
| B3 | [] | [] | [] |
| B4 | [{"alias": "sheet3", "kind": "base", "block": null, "base_tables": ["sheet3"]}] | [] | [] |
| B5 | [] | [] | [] |
| B6 | [{"alias": "sheet4", "kind": "base", "block": null, "base_tables": ["sheet4"]}] | [] | [] |
| B7 | [] | [] | [] |
| B8 | [{"alias": "sheet5", "kind": "base", "block": null, "base_tables": ["sheet5"]}] | [] | [] |
| B9 | [] | [] | [] |
| B10 | [{"alias": "sheet6", "kind": "base", "block": null, "base_tables": ["sheet6"]}] | [] | [] |
| B11 | [] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |
| B2 | COUNT(*) | [] | [] | True |
| B4 | COUNT(*) | [] | [] | True |
| B6 | COUNT(*) | [] | [] | True |
| B8 | COUNT(*) | [] | [] | True |
| B10 | COUNT(*) | [] | [] | True |


## S4

类别 `data`；来源 `query_db`；调用 `3c5f38491ff84cb3b64ac94b29a52311`；状态 `success`。

```sql
SELECT * FROM sheet1 LIMIT 10
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-009/attempt-01/sql/S4.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-009/attempt-01/sql/S4.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-009/attempt-01/results/S4.rows.jsonl)；完整：True；SHA256：`0d91da659a18a5fe4cdbdeb554e5f43cd322a2960bf8a3d28bf65ff10b9b4b5f`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "sheet1", "kind": "base", "block": null, "base_tables": ["sheet1"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |


## S5

类别 `data`；来源 `query_db`；调用 `ff549aaf9d7f4e90bd13ac3982cb3b33`；状态 `success`。

```sql
SELECT DISTINCT "Standard Working Hours" FROM sheet1 LIMIT 20
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-009/attempt-01/sql/S5.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-009/attempt-01/sql/S5.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-009/attempt-01/results/S5.rows.jsonl)；完整：True；SHA256：`86b67f7b813d78ed9403debc99dc5aa27c9e980dc6ee3a73fd88da5c138d822f`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "sheet1", "kind": "base", "block": null, "base_tables": ["sheet1"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |


## S6

类别 `data`；来源 `query_db`；调用 `4a7edf72aad6427d8441433e3ab1abf7`；状态 `success`。

```sql
SELECT 'sheet1' AS tbl, MIN(Date) AS min_date, MAX(Date) AS max_date, COUNT(DISTINCT "Employee") AS employees FROM sheet1
UNION ALL
SELECT 'sheet2', MIN(Date), MAX(Date), COUNT(DISTINCT "Employee") FROM sheet2
UNION ALL
SELECT 'sheet3', MIN(Date), MAX(Date), COUNT(DISTINCT "Employee") FROM sheet3
UNION ALL
SELECT 'sheet4', MIN(Date), MAX(Date), COUNT(DISTINCT "Employee") FROM sheet4
UNION ALL
SELECT 'sheet5', MIN(Date), MAX(Date), COUNT(DISTINCT "Employee") FROM sheet5
UNION ALL
SELECT 'sheet6', MIN(Date), MAX(Date), COUNT(DISTINCT "Employee") FROM sheet6
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-009/attempt-01/sql/S6.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-009/attempt-01/sql/S6.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-009/attempt-01/results/S6.rows.jsonl)；完整：True；SHA256：`d73cd2cfcda0840a9d539e0b517e6a29e9a628851fe8e14ab696a29e819bcdc7`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "sheet1", "kind": "base", "block": null, "base_tables": ["sheet1"]}] | [] | [] |
| B2 | [{"alias": "sheet2", "kind": "base", "block": null, "base_tables": ["sheet2"]}] | [] | [] |
| B3 | [] | [] | [] |
| B4 | [{"alias": "sheet3", "kind": "base", "block": null, "base_tables": ["sheet3"]}] | [] | [] |
| B5 | [] | [] | [] |
| B6 | [{"alias": "sheet4", "kind": "base", "block": null, "base_tables": ["sheet4"]}] | [] | [] |
| B7 | [] | [] | [] |
| B8 | [{"alias": "sheet5", "kind": "base", "block": null, "base_tables": ["sheet5"]}] | [] | [] |
| B9 | [] | [] | [] |
| B10 | [{"alias": "sheet6", "kind": "base", "block": null, "base_tables": ["sheet6"]}] | [] | [] |
| B11 | [] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | MIN(Date) | [{"table": "sheet1", "column": "Date"}] | [] | False |
| B1 | MAX(Date) | [{"table": "sheet1", "column": "Date"}] | [] | False |
| B1 | COUNT(DISTINCT "Employee") | [{"table": "sheet1", "column": "Employee"}] | [] | False |
| B2 | MIN(Date) | [{"table": "sheet2", "column": "Date"}] | [] | False |
| B2 | MAX(Date) | [{"table": "sheet2", "column": "Date"}] | [] | False |
| B2 | COUNT(DISTINCT "Employee") | [{"table": "sheet2", "column": "Employee"}] | [] | False |
| B4 | MIN(Date) | [{"table": "sheet3", "column": "Date"}] | [] | False |
| B4 | MAX(Date) | [{"table": "sheet3", "column": "Date"}] | [] | False |
| B4 | COUNT(DISTINCT "Employee") | [{"table": "sheet3", "column": "Employee"}] | [] | False |
| B6 | MIN(Date) | [{"table": "sheet4", "column": "Date"}] | [] | False |
| B6 | MAX(Date) | [{"table": "sheet4", "column": "Date"}] | [] | False |
| B6 | COUNT(DISTINCT "Employee") | [{"table": "sheet4", "column": "Employee"}] | [] | False |
| B8 | MIN(Date) | [{"table": "sheet5", "column": "Date"}] | [] | False |
| B8 | MAX(Date) | [{"table": "sheet5", "column": "Date"}] | [] | False |
| B8 | COUNT(DISTINCT "Employee") | [{"table": "sheet5", "column": "Employee"}] | [] | False |
| B10 | MIN(Date) | [{"table": "sheet6", "column": "Date"}] | [] | False |
| B10 | MAX(Date) | [{"table": "sheet6", "column": "Date"}] | [] | False |
| B10 | COUNT(DISTINCT "Employee") | [{"table": "sheet6", "column": "Employee"}] | [] | False |


## S7

类别 `data`；来源 `query_db`；调用 `dc06df28a4db46a4895ae13900b23acb`；状态 `success`。

```sql
SELECT DISTINCT "Education Level" FROM sheet1
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-009/attempt-01/sql/S7.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-009/attempt-01/sql/S7.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-009/attempt-01/results/S7.rows.jsonl)；完整：True；SHA256：`5bdb9d3fb0834b64d2582a5ef9de3b461c8484b15646e97b28b70e616d3cbd70`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "sheet1", "kind": "base", "block": null, "base_tables": ["sheet1"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |


## S8

类别 `data`；来源 `query_db`；调用 `75c9361f985f40baa080780137c5e9b7`；状态 `success`。

```sql
SELECT DISTINCT Team FROM sheet1
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-009/attempt-01/sql/S8.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-009/attempt-01/sql/S8.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-009/attempt-01/results/S8.rows.jsonl)；完整：True；SHA256：`e292fcadde8943809b18c9c63b5ad56bbc4c29d082a64d10bcada60345e5bc1c`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "sheet1", "kind": "base", "block": null, "base_tables": ["sheet1"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |


## S9

类别 `data`；来源 `query_db`；调用 `7e202b5c64a24369a267dcecf46f549a`；状态 `success`。

```sql
SELECT "Employee", COUNT(*) AS cnt, COUNT(DISTINCT "Employee ID") AS ids FROM sheet1 GROUP BY "Employee" HAVING cnt > 20
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-009/attempt-01/sql/S9.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-009/attempt-01/sql/S9.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-009/attempt-01/results/S9.rows.jsonl)；完整：True；SHA256：`7de74e3e567eefe9ab99f1f315304274371926b7f1be6ab72f1d642069c5a0f1`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "sheet1", "kind": "base", "block": null, "base_tables": ["sheet1"]}] | [] | ["\"Employee\""] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |
| B1 | COUNT(DISTINCT "Employee ID") | [{"table": "sheet1", "column": "Employee ID"}] | [] | False |


## S10

类别 `data`；来源 `query_db`；调用 `2cef8c6f92704d75920593d965bb5f14`；状态 `success`。

```sql
SELECT "Employee ID", "Employee", Team FROM sheet1 GROUP BY "Employee ID", "Employee", Team ORDER BY "Employee ID" LIMIT 30
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-009/attempt-01/sql/S10.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-009/attempt-01/sql/S10.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-009/attempt-01/results/S10.rows.jsonl)；完整：True；SHA256：`372dc39a4e8327e08eb24da085e02ce723bb8b64f421f4919d40cf8d04fc8828`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "sheet1", "kind": "base", "block": null, "base_tables": ["sheet1"]}] | [] | ["\"Employee ID\"", "\"Employee\"", "Team"] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |


## S11

类别 `data`；来源 `query_db`；调用 `85f52f7e84ff45c7a3c3dd52e56235f9`；状态 `success`。

```sql
WITH all_emp AS (
  SELECT "Employee ID", "Employee" FROM sheet1
  UNION SELECT "Employee ID", "Employee" FROM sheet2
  UNION SELECT "Employee ID", "Employee" FROM sheet3
  UNION SELECT "Employee ID", "Employee" FROM sheet4
  UNION SELECT "Employee ID", "Employee" FROM sheet5
  UNION SELECT "Employee ID", "Employee" FROM sheet6
)
SELECT COUNT(*) AS total_employees, COUNT(DISTINCT "Employee ID") AS unique_ids FROM all_emp
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-009/attempt-01/sql/S11.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-009/attempt-01/sql/S11.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-009/attempt-01/results/S11.rows.jsonl)；完整：True；SHA256：`743fc044d020cb4fc3fad78316ebdaf71b6daa1fa0aa68cb33b35af5ffe75b7e`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "sheet1", "kind": "base", "block": null, "base_tables": ["sheet1"]}] | [] | [] |
| B2 | [{"alias": "sheet2", "kind": "base", "block": null, "base_tables": ["sheet2"]}] | [] | [] |
| B3 | [] | [] | [] |
| B4 | [{"alias": "sheet3", "kind": "base", "block": null, "base_tables": ["sheet3"]}] | [] | [] |
| B5 | [] | [] | [] |
| B6 | [{"alias": "sheet4", "kind": "base", "block": null, "base_tables": ["sheet4"]}] | [] | [] |
| B7 | [] | [] | [] |
| B8 | [{"alias": "sheet5", "kind": "base", "block": null, "base_tables": ["sheet5"]}] | [] | [] |
| B9 | [] | [] | [] |
| B10 | [{"alias": "sheet6", "kind": "base", "block": null, "base_tables": ["sheet6"]}] | [] | [] |
| B11 | [] | [] | [] |
| B12 | [{"alias": "all_emp", "kind": "derived", "block": "B11", "base_tables": ["sheet1", "sheet2", "sheet3", "sheet4", "sheet5", "sheet6"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B12 | COUNT(*) | [] | [] | True |
| B12 | COUNT(DISTINCT "Employee ID") | [{"table": "sheet1", "column": "Employee ID"}, {"table": "sheet6", "column": "Employee ID"}] | [] | False |


## S12

类别 `data`；来源 `query_db`；调用 `8d09e984fd6b4e47b3a8841e4123a30a`；状态 `success`。

```sql
SELECT Team, COUNT(DISTINCT "Employee ID") AS emps FROM (
  SELECT "Employee ID", Team FROM sheet1 UNION ALL
  SELECT "Employee ID", Team FROM sheet2 UNION ALL
  SELECT "Employee ID", Team FROM sheet3 UNION ALL
  SELECT "Employee ID", Team FROM sheet4 UNION ALL
  SELECT "Employee ID", Team FROM sheet5 UNION ALL
  SELECT "Employee ID", Team FROM sheet6
) GROUP BY Team ORDER BY emps DESC
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-009/attempt-01/sql/S12.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-009/attempt-01/sql/S12.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-009/attempt-01/results/S12.rows.jsonl)；完整：True；SHA256：`1ee15dafe03aabedabc73db49a70fba0f7392c0be1bb07012ecebd58019de2dd`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "sheet1", "kind": "base", "block": null, "base_tables": ["sheet1"]}] | [] | [] |
| B2 | [{"alias": "sheet2", "kind": "base", "block": null, "base_tables": ["sheet2"]}] | [] | [] |
| B3 | [] | [] | [] |
| B4 | [{"alias": "sheet3", "kind": "base", "block": null, "base_tables": ["sheet3"]}] | [] | [] |
| B5 | [] | [] | [] |
| B6 | [{"alias": "sheet4", "kind": "base", "block": null, "base_tables": ["sheet4"]}] | [] | [] |
| B7 | [] | [] | [] |
| B8 | [{"alias": "sheet5", "kind": "base", "block": null, "base_tables": ["sheet5"]}] | [] | [] |
| B9 | [] | [] | [] |
| B10 | [{"alias": "sheet6", "kind": "base", "block": null, "base_tables": ["sheet6"]}] | [] | [] |
| B11 | [] | [] | [] |
| B12 | [{"alias": "", "kind": "derived", "block": "B11", "base_tables": ["sheet1", "sheet2", "sheet3", "sheet4", "sheet5", "sheet6"]}] | [] | ["Team"] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B12 | COUNT(DISTINCT "Employee ID") | [{"table": "sheet1", "column": "Employee ID"}, {"table": "sheet6", "column": "Employee ID"}] | [] | False |


## S13

类别 `data`；来源 `query_db`；调用 `25b914bbd8af4e65a6326bb206180e6b`；状态 `success`。

```sql
SELECT "Employee", "Employee ID", Team FROM sheet2 GROUP BY "Employee", "Employee ID", Team ORDER BY "Employee" LIMIT 25
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-009/attempt-01/sql/S13.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-009/attempt-01/sql/S13.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-009/attempt-01/results/S13.rows.jsonl)；完整：True；SHA256：`cddfad21740fe1fd65a908be7e14994e5fd5f9498a98ab16e12aea6f43784880`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "sheet2", "kind": "base", "block": null, "base_tables": ["sheet2"]}] | [] | ["\"Employee\"", "\"Employee ID\"", "Team"] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |


## S14

类别 `data`；来源 `query_db`；调用 `612231eebb5c4ae0a3e4170834546b57`；状态 `success`。

```sql
SELECT "Total Time Away", COUNT(*) AS cnt FROM sheet1 GROUP BY "Total Time Away" ORDER BY cnt DESC LIMIT 30
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-009/attempt-01/sql/S14.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-009/attempt-01/sql/S14.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-009/attempt-01/results/S14.rows.jsonl)；完整：True；SHA256：`c341a864d479f3c64a9a7fea4c8c0b096ac415201e253704a6349a23594216ea`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "sheet1", "kind": "base", "block": null, "base_tables": ["sheet1"]}] | [] | ["\"Total Time Away\""] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |


## S15

类别 `data`；来源 `query_db`；调用 `fa9bcb56bd664b0b8176dcd7d916457b`；状态 `success`。

```sql
SELECT "Pass Rate", COUNT(*) AS cnt FROM sheet1 GROUP BY "Pass Rate" ORDER BY cnt DESC LIMIT 20
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-009/attempt-01/sql/S15.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-009/attempt-01/sql/S15.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-009/attempt-01/results/S15.rows.jsonl)；完整：True；SHA256：`4e647ae48e9a81cbb918fd66bbd4a9ee6e0d38c912007f6084327174e9dfc027`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "sheet1", "kind": "base", "block": null, "base_tables": ["sheet1"]}] | [] | ["\"Pass Rate\""] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |


## S16

类别 `data`；来源 `query_db`；调用 `d95f04b31a1140da8d1378969050a2c7`；状态 `success`。

```sql
SELECT "Hire Date", COUNT(*) AS cnt FROM sheet1 GROUP BY "Hire Date" ORDER BY cnt DESC LIMIT 25
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-009/attempt-01/sql/S16.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-009/attempt-01/sql/S16.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-009/attempt-01/results/S16.rows.jsonl)；完整：True；SHA256：`e73805a0f4fc995f654bb07be641c1fe428b11fd8fe6ba6e3fa6f9970efce047`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "sheet1", "kind": "base", "block": null, "base_tables": ["sheet1"]}] | [] | ["\"Hire Date\""] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |


## S17

类别 `data`；来源 `query_db`；调用 `808a2165a919457586a0b84fcc1fd3e4`；状态 `success`。

```sql
SELECT "Total Time Away" FROM sheet1 WHERE "Total Time Away" NOT LIKE '%min%s' LIMIT 10
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-009/attempt-01/sql/S17.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-009/attempt-01/sql/S17.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-009/attempt-01/results/S17.rows.jsonl)；完整：True；SHA256：`e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "sheet1", "kind": "base", "block": null, "base_tables": ["sheet1"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |


## S18

类别 `data`；来源 `query_db`；调用 `2573d729264140e886dfcf6fa1485767`；状态 `success`。

```sql
SELECT "Disciplinary Issue", COUNT(*) AS cnt FROM sheet1 GROUP BY "Disciplinary Issue"
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-009/attempt-01/sql/S18.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-009/attempt-01/sql/S18.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-009/attempt-01/results/S18.rows.jsonl)；完整：True；SHA256：`e6487635f5ad98bad7437dd513afa1f15c0b563f88710c0955291c693a4cd4d2`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "sheet1", "kind": "base", "block": null, "base_tables": ["sheet1"]}] | [] | ["\"Disciplinary Issue\""] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |


## S19

类别 `data`；来源 `query_db`；调用 `480c95d289b644eba30f637fdd5ba791`；状态 `success`。

```sql
SELECT "Payment Method", COUNT(*) AS cnt FROM sheet1 GROUP BY "Payment Method"
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-009/attempt-01/sql/S19.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-009/attempt-01/sql/S19.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-009/attempt-01/results/S19.rows.jsonl)；完整：True；SHA256：`e1c9edf0dc241470f55cb94c50a555df8694e0446720195ef0bc26675bba5aa1`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "sheet1", "kind": "base", "block": null, "base_tables": ["sheet1"]}] | [] | ["\"Payment Method\""] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |


## S20

类别 `data`；来源 `query_db`；调用 `3c246d5271f54ce3b6bd437714c424e6`；状态 `success`。

```sql
WITH all_rows AS (
  SELECT "Date", "Employee", "Employee ID", "Gender", "Age", "Education Level", Team, "Hire Date",
         "Units Produced" AS units,
         CAST(REPLACE("Pass Rate", '%','') AS REAL) AS pass_pct,
         8.0 - (CAST(substr("Total Time Away",1,instr("Total Time Away",'min')-1) AS REAL)
                + CAST(substr("Total Time Away",instr("Total Time Away",'min')+3, instr("Total Time Away",'s')-instr("Total Time Away",'min')-3) AS REAL)/60.0)/60.0 AS eff_hours,
         "Disciplinary Issue"
  FROM sheet1
  UNION ALL
  SELECT "Date", "Employee", "Employee ID", "Gender", "Age", "Education Level", Team, "Hire Date",
         "Units Produced", CAST(REPLACE("Pass Rate", '%','') AS REAL),
         8.0 - (CAST(substr("Total Time Away",1,instr("Total Time Away",'min')-1) AS REAL)
                + CAST(substr("Total Time Away",instr("Total Time Away",'min')+3, instr("Total Time Away",'s')-instr("Total Time Away",'min')-3) AS REAL)/60.0)/60.0,
         "Disciplinary Issue"
  FROM sheet2
  UNION ALL
  SELECT "Date", "Employee", "Employee ID", "Gender", "Age", "Education Level", Team, "Hire Date",
         "Units Produced", CAST(REPLACE("Pass Rate", '%','') AS REAL),
         8.0 - (CAST(substr("Total Time Away",1,instr("Total Time Away",'min')-1) AS REAL)
                + CAST(substr("Total Time Away",instr("Total Time Away",'min')+3, instr("Total Time Away",'s')-instr("Total Time Away",'min')-3) AS REAL)/60.0)/60.0,
         "Disciplinary Issue"
  FROM sheet3
  UNION ALL
  SELECT "Date", "Employee", "Employee ID", "Gender", "Age", "Education Level", Team, "Hire Date",
         "Units Produced", CAST(REPLACE("Pass Rate", '%','') AS REAL),
         8.0 - (CAST(substr("Total Time Away",1,instr("Total Time Away",'min')-1) AS REAL)
                + CAST(substr("Total Time Away",instr("Total Time Away",'min')+3, instr("Total Time Away",'s')-instr("Total Time Away",'min')-3) AS REAL)/60.0)/60.0,
         "Disciplinary Issue"
  FROM sheet4
  UNION ALL
  SELECT "Date", "Employee", "Employee ID", "Gender", "Age", "Education Level", Team, "Hire Date",
         "Units Produced", CAST(REPLACE("Pass Rate", '%','') AS REAL),
         8.0 - (CAST(substr("Total Time Away",1,instr("Total Time Away",'min')-1) AS REAL)
                + CAST(substr("Total Time Away",instr("Total Time Away",'min')+3, instr("Total Time Away",'s')-instr("Total Time Away",'min')-3) AS REAL)/60.0)/60.0,
         "Disciplinary Issue"
  FROM sheet5
  UNION ALL
  SELECT "Date", "Employee", "Employee ID", "Gender", "Age", "Education Level", Team, "Hire Date",
         "Units Produced", CAST(REPLACE("Pass Rate", '%','') AS REAL),
         8.0 - (CAST(substr("Total Time Away",1,instr("Total Time Away",'min')-1) AS REAL)
                + CAST(substr("Total Time Away",instr("Total Time Away",'min')+3, instr("Total Time Away",'s')-instr("Total Time Away",'min')-3) AS REAL)/60.0)/60.0,
         "Disciplinary Issue"
  FROM sheet6
)
SELECT "Employee ID", "Employee", Team, "Gender", Age, "Education Level", "Hire Date",
       COUNT(*) AS days,
       ROUND(SUM(eff_hours),2) AS total_eff_hours,
       ROUND(AVG(eff_hours),3) AS avg_eff_hours,
       ROUND(SUM(units),1) AS total_units,
       ROUND(AVG(units),2) AS avg_units,
       ROUND(AVG(pass_pct),2) AS avg_pass_rate,
       SUM(CASE WHEN "Disciplinary Issue"='Yes' THEN 1 ELSE 0 END) AS discipline_days
FROM all_rows
GROUP BY "Employee ID", "Employee", Team, "Gender", Age, "Education Level", "Hire Date"
ORDER BY total_units DESC
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-009/attempt-01/sql/S20.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-009/attempt-01/sql/S20.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-009/attempt-01/results/S20.rows.jsonl)；完整：True；SHA256：`3555f2f2cb0765eda3756ccad8d94ac8c4aa49244e2edadb9ac2ce36ea461be5`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "sheet1", "kind": "base", "block": null, "base_tables": ["sheet1"]}] | [] | [] |
| B2 | [{"alias": "sheet2", "kind": "base", "block": null, "base_tables": ["sheet2"]}] | [] | [] |
| B3 | [] | [] | [] |
| B4 | [{"alias": "sheet3", "kind": "base", "block": null, "base_tables": ["sheet3"]}] | [] | [] |
| B5 | [] | [] | [] |
| B6 | [{"alias": "sheet4", "kind": "base", "block": null, "base_tables": ["sheet4"]}] | [] | [] |
| B7 | [] | [] | [] |
| B8 | [{"alias": "sheet5", "kind": "base", "block": null, "base_tables": ["sheet5"]}] | [] | [] |
| B9 | [] | [] | [] |
| B10 | [{"alias": "sheet6", "kind": "base", "block": null, "base_tables": ["sheet6"]}] | [] | [] |
| B11 | [] | [] | [] |
| B12 | [{"alias": "all_rows", "kind": "derived", "block": "B11", "base_tables": ["sheet1", "sheet2", "sheet3", "sheet4", "sheet5", "sheet6"]}] | [] | ["\"Employee ID\"", "\"Employee\"", "Team", "\"Gender\"", "Age", "\"Education Level\"", "\"Hire Date\""] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B12 | COUNT(*) | [] | [] | True |
| B12 | SUM(CASE WHEN "Disciplinary Issue" = 'Yes' THEN 1 ELSE 0 END) | [] | [{"table": "sheet1", "column": "Disciplinary Issue"}, {"table": "sheet6", "column": "Disciplinary Issue"}] | False |
| B12 | SUM(eff_hours) | [{"table": "sheet1", "column": "Total Time Away"}, {"table": "sheet1", "column": "Total Time Away"}, {"table": "sheet1", "column": "Total Time Away"}, {"table": "sheet1", "column": "Total Time Away"}, {"table": "sheet1", "column": "Total Time Away"}, {"table": "sheet1", "column": "Total Time Away"}, {"table": "sheet6", "column": "Total Time Away"}, {"table": "sheet6", "column": "Total Time Away"}, {"table": "sheet6", "column": "Total Time Away"}, {"table": "sheet6", "column": "Total Time Away"}, {"table": "sheet6", "column": "Total Time Away"}, {"table": "sheet6", "column": "Total Time Away"}] | [] | False |
| B12 | AVG(eff_hours) | [{"table": "sheet1", "column": "Total Time Away"}, {"table": "sheet1", "column": "Total Time Away"}, {"table": "sheet1", "column": "Total Time Away"}, {"table": "sheet1", "column": "Total Time Away"}, {"table": "sheet1", "column": "Total Time Away"}, {"table": "sheet1", "column": "Total Time Away"}, {"table": "sheet6", "column": "Total Time Away"}, {"table": "sheet6", "column": "Total Time Away"}, {"table": "sheet6", "column": "Total Time Away"}, {"table": "sheet6", "column": "Total Time Away"}, {"table": "sheet6", "column": "Total Time Away"}, {"table": "sheet6", "column": "Total Time Away"}] | [] | False |
| B12 | SUM(units) | [{"table": "sheet1", "column": "Units Produced"}, {"table": "sheet6", "column": "Units Produced"}] | [] | False |
| B12 | AVG(units) | [{"table": "sheet1", "column": "Units Produced"}, {"table": "sheet6", "column": "Units Produced"}] | [] | False |
| B12 | AVG(pass_pct) | [{"table": "sheet1", "column": "Pass Rate"}, {"table": "sheet6", "column": "Pass Rate"}] | [] | False |


## S21

类别 `data`；来源 `query_db`；调用 `8a0fbce4ae1d4eb68f7e5d43527f5bf7`；状态 `success`。

```sql
WITH all_rows AS (
  SELECT "Date", "Employee", "Employee ID", "Gender", "Age", "Education Level", Team, "Hire Date",
         "Units Produced" AS units,
         CAST(REPLACE("Pass Rate", '%','') AS REAL) AS pass_pct,
         8.0 - (CAST(substr("Total Time Away",1,instr("Total Time Away",'min')-1) AS REAL)
                + CAST(substr("Total Time Away",instr("Total Time Away",'min')+3, instr("Total Time Away",'s')-instr("Total Time Away",'min')-3) AS REAL)/60.0)/60.0 AS eff_hours,
         "Disciplinary Issue"
  FROM sheet1 UNION ALL
  SELECT "Date", "Employee", "Employee ID", "Gender", "Age", "Education Level", Team, "Hire Date",
         "Units Produced", CAST(REPLACE("Pass Rate", '%','') AS REAL),
         8.0 - (CAST(substr("Total Time Away",1,instr("Total Time Away",'min')-1) AS REAL)
                + CAST(substr("Total Time Away",instr("Total Time Away",'min')+3, instr("Total Time Away",'s')-instr("Total Time Away",'min')-3) AS REAL)/60.0)/60.0,
         "Disciplinary Issue"
  FROM sheet2 UNION ALL
  SELECT "Date", "Employee", "Employee ID", "Gender", "Age", "Education Level", Team, "Hire Date",
         "Units Produced", CAST(REPLACE("Pass Rate", '%','') AS REAL),
         8.0 - (CAST(substr("Total Time Away",1,instr("Total Time Away",'min')-1) AS REAL)
                + CAST(substr("Total Time Away",instr("Total Time Away",'min')+3, instr("Total Time Away",'s')-instr("Total Time Away",'min')-3) AS REAL)/60.0)/60.0,
         "Disciplinary Issue"
  FROM sheet3 UNION ALL
  SELECT "Date", "Employee", "Employee ID", "Gender", "Age", "Education Level", Team, "Hire Date",
         "Units Produced", CAST(REPLACE("Pass Rate", '%','') AS REAL),
         8.0 - (CAST(substr("Total Time Away",1,instr("Total Time Away",'min')-1) AS REAL)
                + CAST(substr("Total Time Away",instr("Total Time Away",'min')+3, instr("Total Time Away",'s')-instr("Total Time Away",'min')-3) AS REAL)/60.0)/60.0,
         "Disciplinary Issue"
  FROM sheet4 UNION ALL
  SELECT "Date", "Employee", "Employee ID", "Gender", "Age", "Education Level", Team, "Hire Date",
         "Units Produced", CAST(REPLACE("Pass Rate", '%','') AS REAL),
         8.0 - (CAST(substr("Total Time Away",1,instr("Total Time Away",'min')-1) AS REAL)
                + CAST(substr("Total Time Away",instr("Total Time Away",'min')+3, instr("Total Time Away",'s')-instr("Total Time Away",'min')-3) AS REAL)/60.0)/60.0,
         "Disciplinary Issue"
  FROM sheet5 UNION ALL
  SELECT "Date", "Employee", "Employee ID", "Gender", "Age", "Education Level", Team, "Hire Date",
         "Units Produced", CAST(REPLACE("Pass Rate", '%','') AS REAL),
         8.0 - (CAST(substr("Total Time Away",1,instr("Total Time Away",'min')-1) AS REAL)
                + CAST(substr("Total Time Away",instr("Total Time Away",'min')+3, instr("Total Time Away",'s')-instr("Total Time Away",'min')-3) AS REAL)/60.0)/60.0,
         "Disciplinary Issue"
  FROM sheet6
)
SELECT "Employee ID", "Employee", Team, "Gender", Age, "Education Level",
       MAX(CAST(REPLACE("Hire Date",' months','') AS INTEGER)) AS tenure_months,
       COUNT(*) AS days,
       ROUND(SUM(eff_hours),2) AS total_eff_hours,
       ROUND(AVG(eff_hours),3) AS avg_eff_hours,
       ROUND(SUM(units),1) AS total_units,
       ROUND(AVG(units),2) AS avg_units,
       ROUND(AVG(pass_pct),2) AS avg_pass_rate,
       SUM(CASE WHEN "Disciplinary Issue"='Yes' THEN 1 ELSE 0 END) AS discipline_days
FROM all_rows
GROUP BY "Employee ID", "Employee", Team, "Gender", Age, "Education Level"
ORDER BY total_units DESC
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-009/attempt-01/sql/S21.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-009/attempt-01/sql/S21.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-009/attempt-01/results/S21.rows.jsonl)；完整：True；SHA256：`9c0e6ec60e90d9d987e14ea55138cde95086c20c9bb04aa452cdd100c62b8114`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "sheet1", "kind": "base", "block": null, "base_tables": ["sheet1"]}] | [] | [] |
| B2 | [{"alias": "sheet2", "kind": "base", "block": null, "base_tables": ["sheet2"]}] | [] | [] |
| B3 | [] | [] | [] |
| B4 | [{"alias": "sheet3", "kind": "base", "block": null, "base_tables": ["sheet3"]}] | [] | [] |
| B5 | [] | [] | [] |
| B6 | [{"alias": "sheet4", "kind": "base", "block": null, "base_tables": ["sheet4"]}] | [] | [] |
| B7 | [] | [] | [] |
| B8 | [{"alias": "sheet5", "kind": "base", "block": null, "base_tables": ["sheet5"]}] | [] | [] |
| B9 | [] | [] | [] |
| B10 | [{"alias": "sheet6", "kind": "base", "block": null, "base_tables": ["sheet6"]}] | [] | [] |
| B11 | [] | [] | [] |
| B12 | [{"alias": "all_rows", "kind": "derived", "block": "B11", "base_tables": ["sheet1", "sheet2", "sheet3", "sheet4", "sheet5", "sheet6"]}] | [] | ["\"Employee ID\"", "\"Employee\"", "Team", "\"Gender\"", "Age", "\"Education Level\""] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B12 | MAX(CAST(REPLACE("Hire Date", ' months', '') AS INTEGER)) | [{"table": "sheet1", "column": "Hire Date"}, {"table": "sheet6", "column": "Hire Date"}] | [] | False |
| B12 | COUNT(*) | [] | [] | True |
| B12 | SUM(CASE WHEN "Disciplinary Issue" = 'Yes' THEN 1 ELSE 0 END) | [] | [{"table": "sheet1", "column": "Disciplinary Issue"}, {"table": "sheet6", "column": "Disciplinary Issue"}] | False |
| B12 | SUM(eff_hours) | [{"table": "sheet1", "column": "Total Time Away"}, {"table": "sheet1", "column": "Total Time Away"}, {"table": "sheet1", "column": "Total Time Away"}, {"table": "sheet1", "column": "Total Time Away"}, {"table": "sheet1", "column": "Total Time Away"}, {"table": "sheet1", "column": "Total Time Away"}, {"table": "sheet6", "column": "Total Time Away"}, {"table": "sheet6", "column": "Total Time Away"}, {"table": "sheet6", "column": "Total Time Away"}, {"table": "sheet6", "column": "Total Time Away"}, {"table": "sheet6", "column": "Total Time Away"}, {"table": "sheet6", "column": "Total Time Away"}] | [] | False |
| B12 | AVG(eff_hours) | [{"table": "sheet1", "column": "Total Time Away"}, {"table": "sheet1", "column": "Total Time Away"}, {"table": "sheet1", "column": "Total Time Away"}, {"table": "sheet1", "column": "Total Time Away"}, {"table": "sheet1", "column": "Total Time Away"}, {"table": "sheet1", "column": "Total Time Away"}, {"table": "sheet6", "column": "Total Time Away"}, {"table": "sheet6", "column": "Total Time Away"}, {"table": "sheet6", "column": "Total Time Away"}, {"table": "sheet6", "column": "Total Time Away"}, {"table": "sheet6", "column": "Total Time Away"}, {"table": "sheet6", "column": "Total Time Away"}] | [] | False |
| B12 | SUM(units) | [{"table": "sheet1", "column": "Units Produced"}, {"table": "sheet6", "column": "Units Produced"}] | [] | False |
| B12 | AVG(units) | [{"table": "sheet1", "column": "Units Produced"}, {"table": "sheet6", "column": "Units Produced"}] | [] | False |
| B12 | AVG(pass_pct) | [{"table": "sheet1", "column": "Pass Rate"}, {"table": "sheet6", "column": "Pass Rate"}] | [] | False |


## S22

类别 `data`；来源 `query_db`；调用 `7cb50456a10e428199c1e6ce7b7316c3`；状态 `success`。

```sql
WITH all_rows AS (
  SELECT "Date", "Employee", "Employee ID", "Gender", "Age", "Education Level", Team, "Hire Date",
         "Units Produced" AS units,
         CAST(REPLACE("Pass Rate", '%','') AS REAL) AS pass_pct,
         8.0 - (CAST(substr("Total Time Away",1,instr("Total Time Away",'min')-1) AS REAL)
                + CAST(substr("Total Time Away",instr("Total Time Away",'min')+3, instr("Total Time Away",'s')-instr("Total Time Away",'min')-3) AS REAL)/60.0)/60.0 AS eff_hours,
         "Disciplinary Issue"
  FROM sheet1 UNION ALL
  SELECT "Date", "Employee", "Employee ID", "Gender", "Age", "Education Level", Team, "Hire Date",
         "Units Produced", CAST(REPLACE("Pass Rate", '%','') AS REAL),
         8.0 - (CAST(substr("Total Time Away",1,instr("Total Time Away",'min')-1) AS REAL)
                + CAST(substr("Total Time Away",instr("Total Time Away",'min')+3, instr("Total Time Away",'s')-instr("Total Time Away",'min')-3) AS REAL)/60.0)/60.0,
         "Disciplinary Issue"
  FROM sheet2 UNION ALL
  SELECT "Date", "Employee", "Employee ID", "Gender", "Age", "Education Level", Team, "Hire Date",
         "Units Produced", CAST(REPLACE("Pass Rate", '%','') AS REAL),
         8.0 - (CAST(substr("Total Time Away",1,instr("Total Time Away",'min')-1) AS REAL)
                + CAST(substr("Total Time Away",instr("Total Time Away",'min')+3, instr("Total Time Away",'s')-instr("Total Time Away",'min')-3) AS REAL)/60.0)/60.0,
         "Disciplinary Issue"
  FROM sheet3 UNION ALL
  SELECT "Date", "Employee", "Employee ID", "Gender", "Age", "Education Level", Team, "Hire Date",
         "Units Produced", CAST(REPLACE("Pass Rate", '%','') AS REAL),
         8.0 - (CAST(substr("Total Time Away",1,instr("Total Time Away",'min')-1) AS REAL)
                + CAST(substr("Total Time Away",instr("Total Time Away",'min')+3, instr("Total Time Away",'s')-instr("Total Time Away",'min')-3) AS REAL)/60.0)/60.0,
         "Disciplinary Issue"
  FROM sheet4 UNION ALL
  SELECT "Date", "Employee", "Employee ID", "Gender", "Age", "Education Level", Team, "Hire Date",
         "Units Produced", CAST(REPLACE("Pass Rate", '%','') AS REAL),
         8.0 - (CAST(substr("Total Time Away",1,instr("Total Time Away",'min')-1) AS REAL)
                + CAST(substr("Total Time Away",instr("Total Time Away",'min')+3, instr("Total Time Away",'s')-instr("Total Time Away",'min')-3) AS REAL)/60.0)/60.0,
         "Disciplinary Issue"
  FROM sheet5 UNION ALL
  SELECT "Date", "Employee", "Employee ID", "Gender", "Age", "Education Level", Team, "Hire Date",
         "Units Produced", CAST(REPLACE("Pass Rate", '%','') AS REAL),
         8.0 - (CAST(substr("Total Time Away",1,instr("Total Time Away",'min')-1) AS REAL)
                + CAST(substr("Total Time Away",instr("Total Time Away",'min')+3, instr("Total Time Away",'s')-instr("Total Time Away",'min')-3) AS REAL)/60.0)/60.0,
         "Disciplinary Issue"
  FROM sheet6
),
emp_agg AS (
  SELECT "Employee ID", "Employee", Team, "Gender", Age, "Education Level",
         MAX(CAST(REPLACE("Hire Date",' months','') AS INTEGER)) AS tenure_months,
         COUNT(*) AS days,
         SUM(eff_hours) AS total_eff_hours,
         SUM(units) AS total_units,
         AVG(pass_pct) AS avg_pass_rate,
         SUM(CASE WHEN "Disciplinary Issue"='Yes' THEN 1 ELSE 0 END) AS discipline_days
  FROM all_rows
  GROUP BY "Employee ID", "Employee", Team, "Gender", Age, "Education Level"
)
SELECT *,
       ROUND((total_eff_hours - min_eh) / (max_eh - min_eh), 4) AS norm_eff_hours,
       ROUND((total_units - min_tu) / (max_tu - min_tu), 4) AS norm_units,
       ROUND((avg_pass_rate - min_pr) / (max_pr - min_pr), 4) AS norm_pass_rate,
       ROUND(( (total_eff_hours - min_eh) / (max_eh - min_eh) +
               (total_units - min_tu) / (max_tu - min_tu) +
               (avg_pass_rate - min_pr) / (max_pr - min_pr) ) / 3.0, 4) AS composite_score
FROM emp_agg
CROSS JOIN (SELECT MIN(total_eff_hours) AS min_eh, MAX(total_eff_hours) AS max_eh,
                   MIN(total_units) AS min_tu, MAX(total_units) AS max_tu,
                   MIN(avg_pass_rate) AS min_pr, MAX(avg_pass_rate) AS max_pr
            FROM emp_agg)
ORDER BY composite_score DESC
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-009/attempt-01/sql/S22.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-009/attempt-01/sql/S22.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-009/attempt-01/results/S22.rows.jsonl)；完整：True；SHA256：`2f7d374d828aec9b4143d664f0b7cc79f7a6b38fe0dbc6893c73aa7e941f0892`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "sheet1", "kind": "base", "block": null, "base_tables": ["sheet1"]}] | [] | [] |
| B2 | [{"alias": "sheet2", "kind": "base", "block": null, "base_tables": ["sheet2"]}] | [] | [] |
| B3 | [] | [] | [] |
| B4 | [{"alias": "sheet3", "kind": "base", "block": null, "base_tables": ["sheet3"]}] | [] | [] |
| B5 | [] | [] | [] |
| B6 | [{"alias": "sheet4", "kind": "base", "block": null, "base_tables": ["sheet4"]}] | [] | [] |
| B7 | [] | [] | [] |
| B8 | [{"alias": "sheet5", "kind": "base", "block": null, "base_tables": ["sheet5"]}] | [] | [] |
| B9 | [] | [] | [] |
| B10 | [{"alias": "sheet6", "kind": "base", "block": null, "base_tables": ["sheet6"]}] | [] | [] |
| B11 | [] | [] | [] |
| B12 | [{"alias": "all_rows", "kind": "derived", "block": "B11", "base_tables": ["sheet1", "sheet2", "sheet3", "sheet4", "sheet5", "sheet6"]}] | [] | ["\"Employee ID\"", "\"Employee\"", "Team", "\"Gender\"", "Age", "\"Education Level\""] |
| B13 | [{"alias": "emp_agg", "kind": "derived", "block": "B12", "base_tables": ["sheet1", "sheet2", "sheet3", "sheet4", "sheet5", "sheet6"]}] | [] | [] |
| B14 | [{"alias": "emp_agg", "kind": "derived", "block": "B12", "base_tables": ["sheet1", "sheet2", "sheet3", "sheet4", "sheet5", "sheet6"]}, {"alias": "", "kind": "derived", "block": "B13", "base_tables": ["sheet1", "sheet2", "sheet3", "sheet4", "sheet5", "sheet6"]}] | [{"type": "CROSS", "right": "(SELECT MIN(total_eff_hours) AS min_eh, MAX(total_eff_hours) AS max_eh, MIN(total_units) AS min_tu, MAX(total_units) AS max_tu, MIN(avg_pass_rate) AS min_pr, MAX(avg_pass_rate) AS max_pr FROM emp_agg)", "on": null, "using": []}] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B12 | MAX(CAST(REPLACE("Hire Date", ' months', '') AS INTEGER)) | [{"table": "sheet1", "column": "Hire Date"}, {"table": "sheet6", "column": "Hire Date"}] | [] | False |
| B12 | COUNT(*) | [] | [] | True |
| B12 | SUM(eff_hours) | [{"table": "sheet1", "column": "Total Time Away"}, {"table": "sheet1", "column": "Total Time Away"}, {"table": "sheet1", "column": "Total Time Away"}, {"table": "sheet1", "column": "Total Time Away"}, {"table": "sheet1", "column": "Total Time Away"}, {"table": "sheet1", "column": "Total Time Away"}, {"table": "sheet6", "column": "Total Time Away"}, {"table": "sheet6", "column": "Total Time Away"}, {"table": "sheet6", "column": "Total Time Away"}, {"table": "sheet6", "column": "Total Time Away"}, {"table": "sheet6", "column": "Total Time Away"}, {"table": "sheet6", "column": "Total Time Away"}] | [] | False |
| B12 | SUM(units) | [{"table": "sheet1", "column": "Units Produced"}, {"table": "sheet6", "column": "Units Produced"}] | [] | False |
| B12 | AVG(pass_pct) | [{"table": "sheet1", "column": "Pass Rate"}, {"table": "sheet6", "column": "Pass Rate"}] | [] | False |
| B12 | SUM(CASE WHEN "Disciplinary Issue" = 'Yes' THEN 1 ELSE 0 END) | [] | [{"table": "sheet1", "column": "Disciplinary Issue"}, {"table": "sheet6", "column": "Disciplinary Issue"}] | False |
| B13 | MIN(total_eff_hours) | [{"table": "sheet1", "column": "Total Time Away"}, {"table": "sheet1", "column": "Total Time Away"}, {"table": "sheet1", "column": "Total Time Away"}, {"table": "sheet1", "column": "Total Time Away"}, {"table": "sheet1", "column": "Total Time Away"}, {"table": "sheet1", "column": "Total Time Away"}, {"table": "sheet6", "column": "Total Time Away"}, {"table": "sheet6", "column": "Total Time Away"}, {"table": "sheet6", "column": "Total Time Away"}, {"table": "sheet6", "column": "Total Time Away"}, {"table": "sheet6", "column": "Total Time Away"}, {"table": "sheet6", "column": "Total Time Away"}] | [] | False |
| B13 | MAX(total_eff_hours) | [{"table": "sheet1", "column": "Total Time Away"}, {"table": "sheet1", "column": "Total Time Away"}, {"table": "sheet1", "column": "Total Time Away"}, {"table": "sheet1", "column": "Total Time Away"}, {"table": "sheet1", "column": "Total Time Away"}, {"table": "sheet1", "column": "Total Time Away"}, {"table": "sheet6", "column": "Total Time Away"}, {"table": "sheet6", "column": "Total Time Away"}, {"table": "sheet6", "column": "Total Time Away"}, {"table": "sheet6", "column": "Total Time Away"}, {"table": "sheet6", "column": "Total Time Away"}, {"table": "sheet6", "column": "Total Time Away"}] | [] | False |
| B13 | MIN(total_units) | [{"table": "sheet1", "column": "Units Produced"}, {"table": "sheet6", "column": "Units Produced"}] | [] | False |
| B13 | MAX(total_units) | [{"table": "sheet1", "column": "Units Produced"}, {"table": "sheet6", "column": "Units Produced"}] | [] | False |
| B13 | MIN(avg_pass_rate) | [{"table": "sheet1", "column": "Pass Rate"}, {"table": "sheet6", "column": "Pass Rate"}] | [] | False |
| B13 | MAX(avg_pass_rate) | [{"table": "sheet1", "column": "Pass Rate"}, {"table": "sheet6", "column": "Pass Rate"}] | [] | False |


## S23

类别 `data`；来源 `query_db`；调用 `4ac7d011d682497db727529730cb5ae3`；状态 `success`。

```sql
WITH all_rows AS (
  SELECT "Date", "Employee", "Employee ID", "Gender", "Age", "Education Level", Team, "Hire Date",
         "Units Produced" AS units,
         CAST(REPLACE("Pass Rate", '%','') AS REAL) AS pass_pct,
         8.0 - (CAST(substr("Total Time Away",1,instr("Total Time Away",'min')-1) AS REAL)
                + CAST(substr("Total Time Away",instr("Total Time Away",'min')+3, instr("Total Time Away",'s')-instr("Total Time Away",'min')-3) AS REAL)/60.0)/60.0 AS eff_hours,
         "Disciplinary Issue"
  FROM sheet1 UNION ALL
  SELECT "Date", "Employee", "Employee ID", "Gender", "Age", "Education Level", Team, "Hire Date",
         "Units Produced", CAST(REPLACE("Pass Rate", '%','') AS REAL),
         8.0 - (CAST(substr("Total Time Away",1,instr("Total Time Away",'min')-1) AS REAL)
                + CAST(substr("Total Time Away",instr("Total Time Away",'min')+3, instr("Total Time Away",'s')-instr("Total Time Away",'min')-3) AS REAL)/60.0)/60.0,
         "Disciplinary Issue"
  FROM sheet2 UNION ALL
  SELECT "Date", "Employee", "Employee ID", "Gender", "Age", "Education Level", Team, "Hire Date",
         "Units Produced", CAST(REPLACE("Pass Rate", '%','') AS REAL),
         8.0 - (CAST(substr("Total Time Away",1,instr("Total Time Away",'min')-1) AS REAL)
                + CAST(substr("Total Time Away",instr("Total Time Away",'min')+3, instr("Total Time Away",'s')-instr("Total Time Away",'min')-3) AS REAL)/60.0)/60.0,
         "Disciplinary Issue"
  FROM sheet3 UNION ALL
  SELECT "Date", "Employee", "Employee ID", "Gender", "Age", "Education Level", Team, "Hire Date",
         "Units Produced", CAST(REPLACE("Pass Rate", '%','') AS REAL),
         8.0 - (CAST(substr("Total Time Away",1,instr("Total Time Away",'min')-1) AS REAL)
                + CAST(substr("Total Time Away",instr("Total Time Away",'min')+3, instr("Total Time Away",'s')-instr("Total Time Away",'min')-3) AS REAL)/60.0)/60.0,
         "Disciplinary Issue"
  FROM sheet4 UNION ALL
  SELECT "Date", "Employee", "Employee ID", "Gender", "Age", "Education Level", Team, "Hire Date",
         "Units Produced", CAST(REPLACE("Pass Rate", '%','') AS REAL),
         8.0 - (CAST(substr("Total Time Away",1,instr("Total Time Away",'min')-1) AS REAL)
                + CAST(substr("Total Time Away",instr("Total Time Away",'min')+3, instr("Total Time Away",'s')-instr("Total Time Away",'min')-3) AS REAL)/60.0)/60.0,
         "Disciplinary Issue"
  FROM sheet5 UNION ALL
  SELECT "Date", "Employee", "Employee ID", "Gender", "Age", "Education Level", Team, "Hire Date",
         "Units Produced", CAST(REPLACE("Pass Rate", '%','') AS REAL),
         8.0 - (CAST(substr("Total Time Away",1,instr("Total Time Away",'min')-1) AS REAL)
                + CAST(substr("Total Time Away",instr("Total Time Away",'min')+3, instr("Total Time Away",'s')-instr("Total Time Away",'min')-3) AS REAL)/60.0)/60.0,
         "Disciplinary Issue"
  FROM sheet6
),
emp_agg AS (
  SELECT "Employee ID", "Employee", Team, "Gender", Age, "Education Level",
         MAX(CAST(REPLACE("Hire Date",' months','') AS INTEGER)) AS tenure_months,
         COUNT(*) AS days,
         SUM(eff_hours) AS total_eff_hours,
         SUM(units) AS total_units,
         AVG(units) AS avg_units,
         AVG(pass_pct) AS avg_pass_rate,
         SUM(CASE WHEN "Disciplinary Issue"='Yes' THEN 1 ELSE 0 END) AS discipline_days
  FROM all_rows
  GROUP BY "Employee ID", "Employee", Team, "Gender", Age, "Education Level"
)
SELECT *,
       ROUND(( (total_eff_hours - min_eh) / (max_eh - min_eh) +
               (total_units - min_tu) / (max_tu - min_tu) +
               (avg_pass_rate - min_pr) / (max_pr - min_pr) ) / 3.0, 4) AS composite_score,
       RANK() OVER (ORDER BY ( (total_eff_hours - min_eh) / (max_eh - min_eh) +
                               (total_units - min_tu) / (max_tu - min_tu) +
                               (avg_pass_rate - min_pr) / (max_pr - min_pr) ) / 3.0 DESC) AS rank
FROM emp_agg
CROSS JOIN (SELECT MIN(total_eff_hours) AS min_eh, MAX(total_eff_hours) AS max_eh,
                   MIN(total_units) AS min_tu, MAX(total_units) AS max_tu,
                   MIN(avg_pass_rate) AS min_pr, MAX(avg_pass_rate) AS max_pr
            FROM emp_agg)
ORDER BY composite_score DESC
LIMIT 25
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-009/attempt-01/sql/S23.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-009/attempt-01/sql/S23.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-009/attempt-01/results/S23.rows.jsonl)；完整：True；SHA256：`3ecf5a65bc0765723d7cab501edc65382a5bc1f68d377c229efdc094f81ec6c4`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "sheet1", "kind": "base", "block": null, "base_tables": ["sheet1"]}] | [] | [] |
| B2 | [{"alias": "sheet2", "kind": "base", "block": null, "base_tables": ["sheet2"]}] | [] | [] |
| B3 | [] | [] | [] |
| B4 | [{"alias": "sheet3", "kind": "base", "block": null, "base_tables": ["sheet3"]}] | [] | [] |
| B5 | [] | [] | [] |
| B6 | [{"alias": "sheet4", "kind": "base", "block": null, "base_tables": ["sheet4"]}] | [] | [] |
| B7 | [] | [] | [] |
| B8 | [{"alias": "sheet5", "kind": "base", "block": null, "base_tables": ["sheet5"]}] | [] | [] |
| B9 | [] | [] | [] |
| B10 | [{"alias": "sheet6", "kind": "base", "block": null, "base_tables": ["sheet6"]}] | [] | [] |
| B11 | [] | [] | [] |
| B12 | [{"alias": "all_rows", "kind": "derived", "block": "B11", "base_tables": ["sheet1", "sheet2", "sheet3", "sheet4", "sheet5", "sheet6"]}] | [] | ["\"Employee ID\"", "\"Employee\"", "Team", "\"Gender\"", "Age", "\"Education Level\""] |
| B13 | [{"alias": "emp_agg", "kind": "derived", "block": "B12", "base_tables": ["sheet1", "sheet2", "sheet3", "sheet4", "sheet5", "sheet6"]}] | [] | [] |
| B14 | [{"alias": "emp_agg", "kind": "derived", "block": "B12", "base_tables": ["sheet1", "sheet2", "sheet3", "sheet4", "sheet5", "sheet6"]}, {"alias": "", "kind": "derived", "block": "B13", "base_tables": ["sheet1", "sheet2", "sheet3", "sheet4", "sheet5", "sheet6"]}] | [{"type": "CROSS", "right": "(SELECT MIN(total_eff_hours) AS min_eh, MAX(total_eff_hours) AS max_eh, MIN(total_units) AS min_tu, MAX(total_units) AS max_tu, MIN(avg_pass_rate) AS min_pr, MAX(avg_pass_rate) AS max_pr FROM emp_agg)", "on": null, "using": []}] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B12 | MAX(CAST(REPLACE("Hire Date", ' months', '') AS INTEGER)) | [{"table": "sheet1", "column": "Hire Date"}, {"table": "sheet6", "column": "Hire Date"}] | [] | False |
| B12 | COUNT(*) | [] | [] | True |
| B12 | SUM(eff_hours) | [{"table": "sheet1", "column": "Total Time Away"}, {"table": "sheet1", "column": "Total Time Away"}, {"table": "sheet1", "column": "Total Time Away"}, {"table": "sheet1", "column": "Total Time Away"}, {"table": "sheet1", "column": "Total Time Away"}, {"table": "sheet1", "column": "Total Time Away"}, {"table": "sheet6", "column": "Total Time Away"}, {"table": "sheet6", "column": "Total Time Away"}, {"table": "sheet6", "column": "Total Time Away"}, {"table": "sheet6", "column": "Total Time Away"}, {"table": "sheet6", "column": "Total Time Away"}, {"table": "sheet6", "column": "Total Time Away"}] | [] | False |
| B12 | SUM(units) | [{"table": "sheet1", "column": "Units Produced"}, {"table": "sheet6", "column": "Units Produced"}] | [] | False |
| B12 | AVG(units) | [{"table": "sheet1", "column": "Units Produced"}, {"table": "sheet6", "column": "Units Produced"}] | [] | False |
| B12 | AVG(pass_pct) | [{"table": "sheet1", "column": "Pass Rate"}, {"table": "sheet6", "column": "Pass Rate"}] | [] | False |
| B12 | SUM(CASE WHEN "Disciplinary Issue" = 'Yes' THEN 1 ELSE 0 END) | [] | [{"table": "sheet1", "column": "Disciplinary Issue"}, {"table": "sheet6", "column": "Disciplinary Issue"}] | False |
| B13 | MIN(total_eff_hours) | [{"table": "sheet1", "column": "Total Time Away"}, {"table": "sheet1", "column": "Total Time Away"}, {"table": "sheet1", "column": "Total Time Away"}, {"table": "sheet1", "column": "Total Time Away"}, {"table": "sheet1", "column": "Total Time Away"}, {"table": "sheet1", "column": "Total Time Away"}, {"table": "sheet6", "column": "Total Time Away"}, {"table": "sheet6", "column": "Total Time Away"}, {"table": "sheet6", "column": "Total Time Away"}, {"table": "sheet6", "column": "Total Time Away"}, {"table": "sheet6", "column": "Total Time Away"}, {"table": "sheet6", "column": "Total Time Away"}] | [] | False |
| B13 | MAX(total_eff_hours) | [{"table": "sheet1", "column": "Total Time Away"}, {"table": "sheet1", "column": "Total Time Away"}, {"table": "sheet1", "column": "Total Time Away"}, {"table": "sheet1", "column": "Total Time Away"}, {"table": "sheet1", "column": "Total Time Away"}, {"table": "sheet1", "column": "Total Time Away"}, {"table": "sheet6", "column": "Total Time Away"}, {"table": "sheet6", "column": "Total Time Away"}, {"table": "sheet6", "column": "Total Time Away"}, {"table": "sheet6", "column": "Total Time Away"}, {"table": "sheet6", "column": "Total Time Away"}, {"table": "sheet6", "column": "Total Time Away"}] | [] | False |
| B13 | MIN(total_units) | [{"table": "sheet1", "column": "Units Produced"}, {"table": "sheet6", "column": "Units Produced"}] | [] | False |
| B13 | MAX(total_units) | [{"table": "sheet1", "column": "Units Produced"}, {"table": "sheet6", "column": "Units Produced"}] | [] | False |
| B13 | MIN(avg_pass_rate) | [{"table": "sheet1", "column": "Pass Rate"}, {"table": "sheet6", "column": "Pass Rate"}] | [] | False |
| B13 | MAX(avg_pass_rate) | [{"table": "sheet1", "column": "Pass Rate"}, {"table": "sheet6", "column": "Pass Rate"}] | [] | False |


## S24

类别 `data`；来源 `query_db`；调用 `df80a9f1b2d442659156234b5da12f59`；状态 `success`。

```sql
SELECT Gender, COUNT(*) AS cnt FROM (SELECT DISTINCT "Employee ID", Gender FROM sheet1) GROUP BY Gender
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-009/attempt-01/sql/S24.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-009/attempt-01/sql/S24.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-009/attempt-01/results/S24.rows.jsonl)；完整：True；SHA256：`fc42b6de573f6c174ea4bf8d3404d6d302ef7b463487c16d3a646777e7dd4314`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "sheet1", "kind": "base", "block": null, "base_tables": ["sheet1"]}] | [] | [] |
| B2 | [{"alias": "", "kind": "derived", "block": "B1", "base_tables": ["sheet1"]}] | [] | ["Gender"] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B2 | COUNT(*) | [] | [] | True |


## S25

类别 `data`；来源 `query_db`；调用 `9326e159efe44795b0f4d645697ec4a0`；状态 `success`。

```sql
SELECT "Gender", COUNT(DISTINCT "Employee ID") AS cnt FROM (
  SELECT "Employee ID", "Gender" FROM sheet1 UNION
  SELECT "Employee ID", "Gender" FROM sheet2 UNION
  SELECT "Employee ID", "Gender" FROM sheet3 UNION
  SELECT "Employee ID", "Gender" FROM sheet4 UNION
  SELECT "Employee ID", "Gender" FROM sheet5 UNION
  SELECT "Employee ID", "Gender" FROM sheet6
) GROUP BY "Gender"
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-009/attempt-01/sql/S25.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-009/attempt-01/sql/S25.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-009/attempt-01/results/S25.rows.jsonl)；完整：True；SHA256：`0be7f6873504005328ff6dc4b02c25dc8beeb2f72859205f7e359143ee6198f5`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "sheet1", "kind": "base", "block": null, "base_tables": ["sheet1"]}] | [] | [] |
| B2 | [{"alias": "sheet2", "kind": "base", "block": null, "base_tables": ["sheet2"]}] | [] | [] |
| B3 | [] | [] | [] |
| B4 | [{"alias": "sheet3", "kind": "base", "block": null, "base_tables": ["sheet3"]}] | [] | [] |
| B5 | [] | [] | [] |
| B6 | [{"alias": "sheet4", "kind": "base", "block": null, "base_tables": ["sheet4"]}] | [] | [] |
| B7 | [] | [] | [] |
| B8 | [{"alias": "sheet5", "kind": "base", "block": null, "base_tables": ["sheet5"]}] | [] | [] |
| B9 | [] | [] | [] |
| B10 | [{"alias": "sheet6", "kind": "base", "block": null, "base_tables": ["sheet6"]}] | [] | [] |
| B11 | [] | [] | [] |
| B12 | [{"alias": "", "kind": "derived", "block": "B11", "base_tables": ["sheet1", "sheet2", "sheet3", "sheet4", "sheet5", "sheet6"]}] | [] | ["\"Gender\""] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B12 | COUNT(DISTINCT "Employee ID") | [{"table": "sheet1", "column": "Employee ID"}, {"table": "sheet6", "column": "Employee ID"}] | [] | False |


## S26

类别 `data`；来源 `query_db`；调用 `72b95c5815514dbaa6cf8a340a536d57`；状态 `success`。

```sql
SELECT Team, COUNT(DISTINCT "Employee ID") AS cnt FROM (
  SELECT "Employee ID", Team FROM sheet1 UNION
  SELECT "Employee ID", Team FROM sheet2 UNION
  SELECT "Employee ID", Team FROM sheet3 UNION
  SELECT "Employee ID", Team FROM sheet4 UNION
  SELECT "Employee ID", Team FROM sheet5 UNION
  SELECT "Employee ID", Team FROM sheet6
) GROUP BY Team
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-009/attempt-01/sql/S26.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-009/attempt-01/sql/S26.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-009/attempt-01/results/S26.rows.jsonl)；完整：True；SHA256：`5ece0e62bbc40243da2c4fe6f9ba9003c022a0a0346a4b638d996e5e3210b429`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "sheet1", "kind": "base", "block": null, "base_tables": ["sheet1"]}] | [] | [] |
| B2 | [{"alias": "sheet2", "kind": "base", "block": null, "base_tables": ["sheet2"]}] | [] | [] |
| B3 | [] | [] | [] |
| B4 | [{"alias": "sheet3", "kind": "base", "block": null, "base_tables": ["sheet3"]}] | [] | [] |
| B5 | [] | [] | [] |
| B6 | [{"alias": "sheet4", "kind": "base", "block": null, "base_tables": ["sheet4"]}] | [] | [] |
| B7 | [] | [] | [] |
| B8 | [{"alias": "sheet5", "kind": "base", "block": null, "base_tables": ["sheet5"]}] | [] | [] |
| B9 | [] | [] | [] |
| B10 | [{"alias": "sheet6", "kind": "base", "block": null, "base_tables": ["sheet6"]}] | [] | [] |
| B11 | [] | [] | [] |
| B12 | [{"alias": "", "kind": "derived", "block": "B11", "base_tables": ["sheet1", "sheet2", "sheet3", "sheet4", "sheet5", "sheet6"]}] | [] | ["Team"] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B12 | COUNT(DISTINCT "Employee ID") | [{"table": "sheet1", "column": "Employee ID"}, {"table": "sheet6", "column": "Employee ID"}] | [] | False |


## S27

类别 `data`；来源 `query_db`；调用 `4661da65a76c49bebd4d467781bd6444`；状态 `success`。

```sql
WITH all_rows AS (
  SELECT "Date", "Employee", "Employee ID", "Gender", "Age", "Education Level", Team, "Hire Date",
         "Units Produced" AS units,
         CAST(REPLACE("Pass Rate", '%','') AS REAL) AS pass_pct,
         8.0 - (CAST(substr("Total Time Away",1,instr("Total Time Away",'min')-1) AS REAL)
                + CAST(substr("Total Time Away",instr("Total Time Away",'min')+3, instr("Total Time Away",'s')-instr("Total Time Away",'min')-3) AS REAL)/60.0)/60.0 AS eff_hours,
         "Disciplinary Issue"
  FROM sheet1 UNION ALL
  SELECT "Date", "Employee", "Employee ID", "Gender", "Age", "Education Level", Team, "Hire Date",
         "Units Produced", CAST(REPLACE("Pass Rate", '%','') AS REAL),
         8.0 - (CAST(substr("Total Time Away",1,instr("Total Time Away",'min')-1) AS REAL)
                + CAST(substr("Total Time Away",instr("Total Time Away",'min')+3, instr("Total Time Away",'s')-instr("Total Time Away",'min')-3) AS REAL)/60.0)/60.0,
         "Disciplinary Issue"
  FROM sheet2 UNION ALL
  SELECT "Date", "Employee", "Employee ID", "Gender", "Age", "Education Level", Team, "Hire Date",
         "Units Produced", CAST(REPLACE("Pass Rate", '%','') AS REAL),
         8.0 - (CAST(substr("Total Time Away",1,instr("Total Time Away",'min')-1) AS REAL)
                + CAST(substr("Total Time Away",instr("Total Time Away",'min')+3, instr("Total Time Away",'s')-instr("Total Time Away",'min')-3) AS REAL)/60.0)/60.0,
         "Disciplinary Issue"
  FROM sheet3 UNION ALL
  SELECT "Date", "Employee", "Employee ID", "Gender", "Age", "Education Level", Team, "Hire Date",
         "Units Produced", CAST(REPLACE("Pass Rate", '%','') AS REAL),
         8.0 - (CAST(substr("Total Time Away",1,instr("Total Time Away",'min')-1) AS REAL)
                + CAST(substr("Total Time Away",instr("Total Time Away",'min')+3, instr("Total Time Away",'s')-instr("Total Time Away",'min')-3) AS REAL)/60.0)/60.0,
         "Disciplinary Issue"
  FROM sheet4 UNION ALL
  SELECT "Date", "Employee", "Employee ID", "Gender", "Age", "Education Level", Team, "Hire Date",
         "Units Produced", CAST(REPLACE("Pass Rate", '%','') AS REAL),
         8.0 - (CAST(substr("Total Time Away",1,instr("Total Time Away",'min')-1) AS REAL)
                + CAST(substr("Total Time Away",instr("Total Time Away",'min')+3, instr("Total Time Away",'s')-instr("Total Time Away",'min')-3) AS REAL)/60.0)/60.0,
         "Disciplinary Issue"
  FROM sheet5 UNION ALL
  SELECT "Date", "Employee", "Employee ID", "Gender", "Age", "Education Level", Team, "Hire Date",
         "Units Produced", CAST(REPLACE("Pass Rate", '%','') AS REAL),
         8.0 - (CAST(substr("Total Time Away",1,instr("Total Time Away",'min')-1) AS REAL)
                + CAST(substr("Total Time Away",instr("Total Time Away",'min')+3, instr("Total Time Away",'s')-instr("Total Time Away",'min')-3) AS REAL)/60.0)/60.0,
         "Disciplinary Issue"
  FROM sheet6
),
emp_agg AS (
  SELECT "Employee ID", "Employee", Team, "Gender", Age, "Education Level",
         MAX(CAST(REPLACE("Hire Date",' months','') AS INTEGER)) AS tenure_months,
         COUNT(*) AS days,
         SUM(eff_hours) AS total_eff_hours,
         SUM(units) AS total_units,
         AVG(units) AS avg_units,
         AVG(pass_pct) AS avg_pass_rate,
         SUM(CASE WHEN "Disciplinary Issue"='Yes' THEN 1 ELSE 0 END) AS discipline_days
  FROM all_rows
  GROUP BY "Employee ID", "Employee", Team, "Gender", Age, "Education Level"
)
SELECT "Employee ID", "Employee", Team, "Gender", Age, "Education Level", tenure_months, days,
       ROUND(total_eff_hours,1) AS total_eff_hours,
       ROUND(total_units,1) AS total_units,
       ROUND(avg_units,2) AS avg_units,
       ROUND(avg_pass_rate,2) AS avg_pass_rate,
       ROUND(( (total_eff_hours - min_eh) / (max_eh - min_eh) +
               (total_units - min_tu) / (max_tu - min_tu) +
               (avg_pass_rate - min_pr) / (max_pr - min_pr) ) / 3.0, 4) AS composite_score,
       RANK() OVER (ORDER BY ( (total_eff_hours - min_eh) / (max_eh - min_eh) +
                               (total_units - min_tu) / (max_tu - min_tu) +
                               (avg_pass_rate - min_pr) / (max_pr - min_pr) ) / 3.0 DESC) AS rank
FROM emp_agg
CROSS JOIN (SELECT MIN(total_eff_hours) AS min_eh, MAX(total_eff_hours) AS max_eh,
                   MIN(total_units) AS min_tu, MAX(total_units) AS max_tu,
                   MIN(avg_pass_rate) AS min_pr, MAX(avg_pass_rate) AS max_pr
            FROM emp_agg)
ORDER BY composite_score DESC
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-009/attempt-01/sql/S27.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-009/attempt-01/sql/S27.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-009/attempt-01/results/S27.rows.jsonl)；完整：True；SHA256：`16d946894f020d998e3330ea9539f264756b8569e37a872df5ab161ef94cfb6a`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "sheet1", "kind": "base", "block": null, "base_tables": ["sheet1"]}] | [] | [] |
| B2 | [{"alias": "sheet2", "kind": "base", "block": null, "base_tables": ["sheet2"]}] | [] | [] |
| B3 | [] | [] | [] |
| B4 | [{"alias": "sheet3", "kind": "base", "block": null, "base_tables": ["sheet3"]}] | [] | [] |
| B5 | [] | [] | [] |
| B6 | [{"alias": "sheet4", "kind": "base", "block": null, "base_tables": ["sheet4"]}] | [] | [] |
| B7 | [] | [] | [] |
| B8 | [{"alias": "sheet5", "kind": "base", "block": null, "base_tables": ["sheet5"]}] | [] | [] |
| B9 | [] | [] | [] |
| B10 | [{"alias": "sheet6", "kind": "base", "block": null, "base_tables": ["sheet6"]}] | [] | [] |
| B11 | [] | [] | [] |
| B12 | [{"alias": "all_rows", "kind": "derived", "block": "B11", "base_tables": ["sheet1", "sheet2", "sheet3", "sheet4", "sheet5", "sheet6"]}] | [] | ["\"Employee ID\"", "\"Employee\"", "Team", "\"Gender\"", "Age", "\"Education Level\""] |
| B13 | [{"alias": "emp_agg", "kind": "derived", "block": "B12", "base_tables": ["sheet1", "sheet2", "sheet3", "sheet4", "sheet5", "sheet6"]}] | [] | [] |
| B14 | [{"alias": "emp_agg", "kind": "derived", "block": "B12", "base_tables": ["sheet1", "sheet2", "sheet3", "sheet4", "sheet5", "sheet6"]}, {"alias": "", "kind": "derived", "block": "B13", "base_tables": ["sheet1", "sheet2", "sheet3", "sheet4", "sheet5", "sheet6"]}] | [{"type": "CROSS", "right": "(SELECT MIN(total_eff_hours) AS min_eh, MAX(total_eff_hours) AS max_eh, MIN(total_units) AS min_tu, MAX(total_units) AS max_tu, MIN(avg_pass_rate) AS min_pr, MAX(avg_pass_rate) AS max_pr FROM emp_agg)", "on": null, "using": []}] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B12 | MAX(CAST(REPLACE("Hire Date", ' months', '') AS INTEGER)) | [{"table": "sheet1", "column": "Hire Date"}, {"table": "sheet6", "column": "Hire Date"}] | [] | False |
| B12 | COUNT(*) | [] | [] | True |
| B12 | SUM(eff_hours) | [{"table": "sheet1", "column": "Total Time Away"}, {"table": "sheet1", "column": "Total Time Away"}, {"table": "sheet1", "column": "Total Time Away"}, {"table": "sheet1", "column": "Total Time Away"}, {"table": "sheet1", "column": "Total Time Away"}, {"table": "sheet1", "column": "Total Time Away"}, {"table": "sheet6", "column": "Total Time Away"}, {"table": "sheet6", "column": "Total Time Away"}, {"table": "sheet6", "column": "Total Time Away"}, {"table": "sheet6", "column": "Total Time Away"}, {"table": "sheet6", "column": "Total Time Away"}, {"table": "sheet6", "column": "Total Time Away"}] | [] | False |
| B12 | SUM(units) | [{"table": "sheet1", "column": "Units Produced"}, {"table": "sheet6", "column": "Units Produced"}] | [] | False |
| B12 | AVG(units) | [{"table": "sheet1", "column": "Units Produced"}, {"table": "sheet6", "column": "Units Produced"}] | [] | False |
| B12 | AVG(pass_pct) | [{"table": "sheet1", "column": "Pass Rate"}, {"table": "sheet6", "column": "Pass Rate"}] | [] | False |
| B12 | SUM(CASE WHEN "Disciplinary Issue" = 'Yes' THEN 1 ELSE 0 END) | [] | [{"table": "sheet1", "column": "Disciplinary Issue"}, {"table": "sheet6", "column": "Disciplinary Issue"}] | False |
| B13 | MIN(total_eff_hours) | [{"table": "sheet1", "column": "Total Time Away"}, {"table": "sheet1", "column": "Total Time Away"}, {"table": "sheet1", "column": "Total Time Away"}, {"table": "sheet1", "column": "Total Time Away"}, {"table": "sheet1", "column": "Total Time Away"}, {"table": "sheet1", "column": "Total Time Away"}, {"table": "sheet6", "column": "Total Time Away"}, {"table": "sheet6", "column": "Total Time Away"}, {"table": "sheet6", "column": "Total Time Away"}, {"table": "sheet6", "column": "Total Time Away"}, {"table": "sheet6", "column": "Total Time Away"}, {"table": "sheet6", "column": "Total Time Away"}] | [] | False |
| B13 | MAX(total_eff_hours) | [{"table": "sheet1", "column": "Total Time Away"}, {"table": "sheet1", "column": "Total Time Away"}, {"table": "sheet1", "column": "Total Time Away"}, {"table": "sheet1", "column": "Total Time Away"}, {"table": "sheet1", "column": "Total Time Away"}, {"table": "sheet1", "column": "Total Time Away"}, {"table": "sheet6", "column": "Total Time Away"}, {"table": "sheet6", "column": "Total Time Away"}, {"table": "sheet6", "column": "Total Time Away"}, {"table": "sheet6", "column": "Total Time Away"}, {"table": "sheet6", "column": "Total Time Away"}, {"table": "sheet6", "column": "Total Time Away"}] | [] | False |
| B13 | MIN(total_units) | [{"table": "sheet1", "column": "Units Produced"}, {"table": "sheet6", "column": "Units Produced"}] | [] | False |
| B13 | MAX(total_units) | [{"table": "sheet1", "column": "Units Produced"}, {"table": "sheet6", "column": "Units Produced"}] | [] | False |
| B13 | MIN(avg_pass_rate) | [{"table": "sheet1", "column": "Pass Rate"}, {"table": "sheet6", "column": "Pass Rate"}] | [] | False |
| B13 | MAX(avg_pass_rate) | [{"table": "sheet1", "column": "Pass Rate"}, {"table": "sheet6", "column": "Pass Rate"}] | [] | False |


## S28

类别 `data`；来源 `query_db`；调用 `dc31bc14c9294fce997ea193026ed604`；状态 `success`。

```sql
WITH all_rows AS (
  SELECT "Date", "Employee", "Employee ID", "Gender", "Age", "Education Level", Team, "Hire Date",
         "Units Produced" AS units,
         CAST(REPLACE("Pass Rate", '%','') AS REAL) AS pass_pct,
         8.0 - (CAST(substr("Total Time Away",1,instr("Total Time Away",'min')-1) AS REAL)
                + CAST(substr("Total Time Away",instr("Total Time Away",'min')+3, instr("Total Time Away",'s')-instr("Total Time Away",'min')-3) AS REAL)/60.0)/60.0 AS eff_hours,
         "Disciplinary Issue"
  FROM sheet1 UNION ALL
  SELECT "Date", "Employee", "Employee ID", "Gender", "Age", "Education Level", Team, "Hire Date",
         "Units Produced", CAST(REPLACE("Pass Rate", '%','') AS REAL),
         8.0 - (CAST(substr("Total Time Away",1,instr("Total Time Away",'min')-1) AS REAL)
                + CAST(substr("Total Time Away",instr("Total Time Away",'min')+3, instr("Total Time Away",'s')-instr("Total Time Away",'min')-3) AS REAL)/60.0)/60.0,
         "Disciplinary Issue"
  FROM sheet2 UNION ALL
  SELECT "Date", "Employee", "Employee ID", "Gender", "Age", "Education Level", Team, "Hire Date",
         "Units Produced", CAST(REPLACE("Pass Rate", '%','') AS REAL),
         8.0 - (CAST(substr("Total Time Away",1,instr("Total Time Away",'min')-1) AS REAL)
                + CAST(substr("Total Time Away",instr("Total Time Away",'min')+3, instr("Total Time Away",'s')-instr("Total Time Away",'min')-3) AS REAL)/60.0)/60.0,
         "Disciplinary Issue"
  FROM sheet3 UNION ALL
  SELECT "Date", "Employee", "Employee ID", "Gender", "Age", "Education Level", Team, "Hire Date",
         "Units Produced", CAST(REPLACE("Pass Rate", '%','') AS REAL),
         8.0 - (CAST(substr("Total Time Away",1,instr("Total Time Away",'min')-1) AS REAL)
                + CAST(substr("Total Time Away",instr("Total Time Away",'min')+3, instr("Total Time Away",'s')-instr("Total Time Away",'min')-3) AS REAL)/60.0)/60.0,
         "Disciplinary Issue"
  FROM sheet4 UNION ALL
  SELECT "Date", "Employee", "Employee ID", "Gender", "Age", "Education Level", Team, "Hire Date",
         "Units Produced", CAST(REPLACE("Pass Rate", '%','') AS REAL),
         8.0 - (CAST(substr("Total Time Away",1,instr("Total Time Away",'min')-1) AS REAL)
                + CAST(substr("Total Time Away",instr("Total Time Away",'min')+3, instr("Total Time Away",'s')-instr("Total Time Away",'min')-3) AS REAL)/60.0)/60.0,
         "Disciplinary Issue"
  FROM sheet5 UNION ALL
  SELECT "Date", "Employee", "Employee ID", "Gender", "Age", "Education Level", Team, "Hire Date",
         "Units Produced", CAST(REPLACE("Pass Rate", '%','') AS REAL),
         8.0 - (CAST(substr("Total Time Away",1,instr("Total Time Away",'min')-1) AS REAL)
                + CAST(substr("Total Time Away",instr("Total Time Away",'min')+3, instr("Total Time Away",'s')-instr("Total Time Away",'min')-3) AS REAL)/60.0)/60.0,
         "Disciplinary Issue"
  FROM sheet6
),
emp_agg AS (
  SELECT "Employee ID", "Employee", Team, "Gender", Age, "Education Level",
         MAX(CAST(REPLACE("Hire Date",' months','') AS INTEGER)) AS tenure_months,
         COUNT(*) AS days,
         SUM(eff_hours) AS total_eff_hours,
         SUM(units) AS total_units,
         AVG(pass_pct) AS avg_pass_rate,
         SUM(CASE WHEN "Disciplinary Issue"='Yes' THEN 1 ELSE 0 END) AS discipline_days
  FROM all_rows
  GROUP BY "Employee ID", "Employee", Team, "Gender", Age, "Education Level"
),
ranked AS (
  SELECT *,
         RANK() OVER (ORDER BY ( (total_eff_hours - min_eh) / (max_eh - min_eh) +
                                 (total_units - min_tu) / (max_tu - min_tu) +
                                 (avg_pass_rate - min_pr) / (max_pr - min_pr) ) / 3.0 DESC) AS rank
  FROM emp_agg
  CROSS JOIN (SELECT MIN(total_eff_hours) AS min_eh, MAX(total_eff_hours) AS max_eh,
                     MIN(total_units) AS min_tu, MAX(total_units) AS max_tu,
                     MIN(avg_pass_rate) AS min_pr, MAX(avg_pass_rate) AS max_pr
              FROM emp_agg)
)
SELECT "Gender",
       COUNT(*) AS total,
       SUM(CASE WHEN rank <= 10 THEN 1 ELSE 0 END) AS in_top10,
       SUM(CASE WHEN rank <= 20 THEN 1 ELSE 0 END) AS in_top20,
       ROUND(AVG(rank),1) AS avg_rank
FROM ranked GROUP BY "Gender"
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-009/attempt-01/sql/S28.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-009/attempt-01/sql/S28.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-009/attempt-01/results/S28.rows.jsonl)；完整：True；SHA256：`2e4c6070c97898952466906a86fc17213e068534a000a5cba30f835b0b48b98c`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "sheet1", "kind": "base", "block": null, "base_tables": ["sheet1"]}] | [] | [] |
| B2 | [{"alias": "sheet2", "kind": "base", "block": null, "base_tables": ["sheet2"]}] | [] | [] |
| B3 | [] | [] | [] |
| B4 | [{"alias": "sheet3", "kind": "base", "block": null, "base_tables": ["sheet3"]}] | [] | [] |
| B5 | [] | [] | [] |
| B6 | [{"alias": "sheet4", "kind": "base", "block": null, "base_tables": ["sheet4"]}] | [] | [] |
| B7 | [] | [] | [] |
| B8 | [{"alias": "sheet5", "kind": "base", "block": null, "base_tables": ["sheet5"]}] | [] | [] |
| B9 | [] | [] | [] |
| B10 | [{"alias": "sheet6", "kind": "base", "block": null, "base_tables": ["sheet6"]}] | [] | [] |
| B11 | [] | [] | [] |
| B12 | [{"alias": "all_rows", "kind": "derived", "block": "B11", "base_tables": ["sheet1", "sheet2", "sheet3", "sheet4", "sheet5", "sheet6"]}] | [] | ["\"Employee ID\"", "\"Employee\"", "Team", "\"Gender\"", "Age", "\"Education Level\""] |
| B13 | [{"alias": "emp_agg", "kind": "derived", "block": "B12", "base_tables": ["sheet1", "sheet2", "sheet3", "sheet4", "sheet5", "sheet6"]}] | [] | [] |
| B14 | [{"alias": "emp_agg", "kind": "derived", "block": "B12", "base_tables": ["sheet1", "sheet2", "sheet3", "sheet4", "sheet5", "sheet6"]}, {"alias": "", "kind": "derived", "block": "B13", "base_tables": ["sheet1", "sheet2", "sheet3", "sheet4", "sheet5", "sheet6"]}] | [{"type": "CROSS", "right": "(SELECT MIN(total_eff_hours) AS min_eh, MAX(total_eff_hours) AS max_eh, MIN(total_units) AS min_tu, MAX(total_units) AS max_tu, MIN(avg_pass_rate) AS min_pr, MAX(avg_pass_rate) AS max_pr FROM emp_agg)", "on": null, "using": []}] | [] |
| B15 | [{"alias": "ranked", "kind": "derived", "block": "B14", "base_tables": ["sheet1", "sheet2", "sheet3", "sheet4", "sheet5", "sheet6"]}] | [] | ["\"Gender\""] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B12 | MAX(CAST(REPLACE("Hire Date", ' months', '') AS INTEGER)) | [{"table": "sheet1", "column": "Hire Date"}, {"table": "sheet6", "column": "Hire Date"}] | [] | False |
| B12 | COUNT(*) | [] | [] | True |
| B12 | SUM(eff_hours) | [{"table": "sheet1", "column": "Total Time Away"}, {"table": "sheet1", "column": "Total Time Away"}, {"table": "sheet1", "column": "Total Time Away"}, {"table": "sheet1", "column": "Total Time Away"}, {"table": "sheet1", "column": "Total Time Away"}, {"table": "sheet1", "column": "Total Time Away"}, {"table": "sheet6", "column": "Total Time Away"}, {"table": "sheet6", "column": "Total Time Away"}, {"table": "sheet6", "column": "Total Time Away"}, {"table": "sheet6", "column": "Total Time Away"}, {"table": "sheet6", "column": "Total Time Away"}, {"table": "sheet6", "column": "Total Time Away"}] | [] | False |
| B12 | SUM(units) | [{"table": "sheet1", "column": "Units Produced"}, {"table": "sheet6", "column": "Units Produced"}] | [] | False |
| B12 | AVG(pass_pct) | [{"table": "sheet1", "column": "Pass Rate"}, {"table": "sheet6", "column": "Pass Rate"}] | [] | False |
| B12 | SUM(CASE WHEN "Disciplinary Issue" = 'Yes' THEN 1 ELSE 0 END) | [] | [{"table": "sheet1", "column": "Disciplinary Issue"}, {"table": "sheet6", "column": "Disciplinary Issue"}] | False |
| B13 | MIN(total_eff_hours) | [{"table": "sheet1", "column": "Total Time Away"}, {"table": "sheet1", "column": "Total Time Away"}, {"table": "sheet1", "column": "Total Time Away"}, {"table": "sheet1", "column": "Total Time Away"}, {"table": "sheet1", "column": "Total Time Away"}, {"table": "sheet1", "column": "Total Time Away"}, {"table": "sheet6", "column": "Total Time Away"}, {"table": "sheet6", "column": "Total Time Away"}, {"table": "sheet6", "column": "Total Time Away"}, {"table": "sheet6", "column": "Total Time Away"}, {"table": "sheet6", "column": "Total Time Away"}, {"table": "sheet6", "column": "Total Time Away"}] | [] | False |
| B13 | MAX(total_eff_hours) | [{"table": "sheet1", "column": "Total Time Away"}, {"table": "sheet1", "column": "Total Time Away"}, {"table": "sheet1", "column": "Total Time Away"}, {"table": "sheet1", "column": "Total Time Away"}, {"table": "sheet1", "column": "Total Time Away"}, {"table": "sheet1", "column": "Total Time Away"}, {"table": "sheet6", "column": "Total Time Away"}, {"table": "sheet6", "column": "Total Time Away"}, {"table": "sheet6", "column": "Total Time Away"}, {"table": "sheet6", "column": "Total Time Away"}, {"table": "sheet6", "column": "Total Time Away"}, {"table": "sheet6", "column": "Total Time Away"}] | [] | False |
| B13 | MIN(total_units) | [{"table": "sheet1", "column": "Units Produced"}, {"table": "sheet6", "column": "Units Produced"}] | [] | False |
| B13 | MAX(total_units) | [{"table": "sheet1", "column": "Units Produced"}, {"table": "sheet6", "column": "Units Produced"}] | [] | False |
| B13 | MIN(avg_pass_rate) | [{"table": "sheet1", "column": "Pass Rate"}, {"table": "sheet6", "column": "Pass Rate"}] | [] | False |
| B13 | MAX(avg_pass_rate) | [{"table": "sheet1", "column": "Pass Rate"}, {"table": "sheet6", "column": "Pass Rate"}] | [] | False |
| B15 | COUNT(*) | [] | [] | True |
| B15 | SUM(CASE WHEN rank <= 10 THEN 1 ELSE 0 END) | [] | [{"table": "sheet1", "column": "Pass Rate"}, {"table": "sheet6", "column": "Pass Rate"}, {"table": "sheet1", "column": "Pass Rate"}, {"table": "sheet6", "column": "Pass Rate"}, {"table": "sheet1", "column": "Pass Rate"}, {"table": "sheet6", "column": "Pass Rate"}, {"table": "sheet1", "column": "Pass Rate"}, {"table": "sheet6", "column": "Pass Rate"}, {"table": "sheet1", "column": "Total Time Away"}, {"table": "sheet1", "column": "Total Time Away"}, {"table": "sheet1", "column": "Total Time Away"}, {"table": "sheet1", "column": "Total Time Away"}, {"table": "sheet1", "column": "Total Time Away"}, {"table": "sheet1", "column": "Total Time Away"}, {"table": "sheet6", "column": "Total Time Away"}, {"table": "sheet6", "column": "Total Time Away"}, {"table": "sheet6", "column": "Total Time Away"}, {"table": "sheet6", "column": "Total Time Away"}, {"table": "sheet6", "column": "Total Time Away"}, {"table": "sheet6", "column": "Total Time Away"}, {"table": "sheet1", "column": "Total Time Away"}, {"table": "sheet1", "column": "Total Time Away"}, {"table": "sheet1", "column": "Total Time Away"}, {"table": "sheet1", "column": "Total Time Away"}, {"table": "sheet1", "column": "Total Time Away"}, {"table": "sheet1", "column": "Total Time Away"}, {"table": "sheet6", "column": "Total Time Away"}, {"table": "sheet6", "column": "Total Time Away"}, {"table": "sheet6", "column": "Total Time Away"}, {"table": "sheet6", "column": "Total Time Away"}, {"table": "sheet6", "column": "Total Time Away"}, {"table": "sheet6", "column": "Total Time Away"}, {"table": "sheet1", "column": "Total Time Away"}, {"table": "sheet1", "column": "Total Time Away"}, {"table": "sheet1", "column": "Total Time Away"}, {"table": "sheet1", "column": "Total Time Away"}, {"table": "sheet1", "column": "Total Time Away"}, {"table": "sheet1", "column": "Total Time Away"}, {"table": "sheet6", "column": "Total Time Away"}, {"table": "sheet6", "column": "Total Time Away"}, {"table": "sheet6", "column": "Total Time Away"}, {"table": "sheet6", "column": "Total Time Away"}, {"table": "sheet6", "column": "Total Time Away"}, {"table": "sheet6", "column": "Total Time Away"}, {"table": "sheet1", "column": "Total Time Away"}, {"table": "sheet1", "column": "Total Time Away"}, {"table": "sheet1", "column": "Total Time Away"}, {"table": "sheet1", "column": "Total Time Away"}, {"table": "sheet1", "column": "Total Time Away"}, {"table": "sheet1", "column": "Total Time Away"}, {"table": "sheet6", "column": "Total Time Away"}, {"table": "sheet6", "column": "Total Time Away"}, {"table": "sheet6", "column": "Total Time Away"}, {"table": "sheet6", "column": "Total Time Away"}, {"table": "sheet6", "column": "Total Time Away"}, {"table": "sheet6", "column": "Total Time Away"}, {"table": "sheet1", "column": "Units Produced"}, {"table": "sheet6", "column": "Units Produced"}, {"table": "sheet1", "column": "Units Produced"}, {"table": "sheet6", "column": "Units Produced"}, {"table": "sheet1", "column": "Units Produced"}, {"table": "sheet6", "column": "Units Produced"}, {"table": "sheet1", "column": "Units Produced"}, {"table": "sheet6", "column": "Units Produced"}] | False |
| B15 | SUM(CASE WHEN rank <= 20 THEN 1 ELSE 0 END) | [] | [{"table": "sheet1", "column": "Pass Rate"}, {"table": "sheet6", "column": "Pass Rate"}, {"table": "sheet1", "column": "Pass Rate"}, {"table": "sheet6", "column": "Pass Rate"}, {"table": "sheet1", "column": "Pass Rate"}, {"table": "sheet6", "column": "Pass Rate"}, {"table": "sheet1", "column": "Pass Rate"}, {"table": "sheet6", "column": "Pass Rate"}, {"table": "sheet1", "column": "Total Time Away"}, {"table": "sheet1", "column": "Total Time Away"}, {"table": "sheet1", "column": "Total Time Away"}, {"table": "sheet1", "column": "Total Time Away"}, {"table": "sheet1", "column": "Total Time Away"}, {"table": "sheet1", "column": "Total Time Away"}, {"table": "sheet6", "column": "Total Time Away"}, {"table": "sheet6", "column": "Total Time Away"}, {"table": "sheet6", "column": "Total Time Away"}, {"table": "sheet6", "column": "Total Time Away"}, {"table": "sheet6", "column": "Total Time Away"}, {"table": "sheet6", "column": "Total Time Away"}, {"table": "sheet1", "column": "Total Time Away"}, {"table": "sheet1", "column": "Total Time Away"}, {"table": "sheet1", "column": "Total Time Away"}, {"table": "sheet1", "column": "Total Time Away"}, {"table": "sheet1", "column": "Total Time Away"}, {"table": "sheet1", "column": "Total Time Away"}, {"table": "sheet6", "column": "Total Time Away"}, {"table": "sheet6", "column": "Total Time Away"}, {"table": "sheet6", "column": "Total Time Away"}, {"table": "sheet6", "column": "Total Time Away"}, {"table": "sheet6", "column": "Total Time Away"}, {"table": "sheet6", "column": "Total Time Away"}, {"table": "sheet1", "column": "Total Time Away"}, {"table": "sheet1", "column": "Total Time Away"}, {"table": "sheet1", "column": "Total Time Away"}, {"table": "sheet1", "column": "Total Time Away"}, {"table": "sheet1", "column": "Total Time Away"}, {"table": "sheet1", "column": "Total Time Away"}, {"table": "sheet6", "column": "Total Time Away"}, {"table": "sheet6", "column": "Total Time Away"}, {"table": "sheet6", "column": "Total Time Away"}, {"table": "sheet6", "column": "Total Time Away"}, {"table": "sheet6", "column": "Total Time Away"}, {"table": "sheet6", "column": "Total Time Away"}, {"table": "sheet1", "column": "Total Time Away"}, {"table": "sheet1", "column": "Total Time Away"}, {"table": "sheet1", "column": "Total Time Away"}, {"table": "sheet1", "column": "Total Time Away"}, {"table": "sheet1", "column": "Total Time Away"}, {"table": "sheet1", "column": "Total Time Away"}, {"table": "sheet6", "column": "Total Time Away"}, {"table": "sheet6", "column": "Total Time Away"}, {"table": "sheet6", "column": "Total Time Away"}, {"table": "sheet6", "column": "Total Time Away"}, {"table": "sheet6", "column": "Total Time Away"}, {"table": "sheet6", "column": "Total Time Away"}, {"table": "sheet1", "column": "Units Produced"}, {"table": "sheet6", "column": "Units Produced"}, {"table": "sheet1", "column": "Units Produced"}, {"table": "sheet6", "column": "Units Produced"}, {"table": "sheet1", "column": "Units Produced"}, {"table": "sheet6", "column": "Units Produced"}, {"table": "sheet1", "column": "Units Produced"}, {"table": "sheet6", "column": "Units Produced"}] | False |
| B15 | AVG(rank) | [{"table": "sheet1", "column": "Pass Rate"}, {"table": "sheet6", "column": "Pass Rate"}, {"table": "sheet1", "column": "Pass Rate"}, {"table": "sheet6", "column": "Pass Rate"}, {"table": "sheet1", "column": "Pass Rate"}, {"table": "sheet6", "column": "Pass Rate"}, {"table": "sheet1", "column": "Pass Rate"}, {"table": "sheet6", "column": "Pass Rate"}, {"table": "sheet1", "column": "Total Time Away"}, {"table": "sheet1", "column": "Total Time Away"}, {"table": "sheet1", "column": "Total Time Away"}, {"table": "sheet1", "column": "Total Time Away"}, {"table": "sheet1", "column": "Total Time Away"}, {"table": "sheet1", "column": "Total Time Away"}, {"table": "sheet6", "column": "Total Time Away"}, {"table": "sheet6", "column": "Total Time Away"}, {"table": "sheet6", "column": "Total Time Away"}, {"table": "sheet6", "column": "Total Time Away"}, {"table": "sheet6", "column": "Total Time Away"}, {"table": "sheet6", "column": "Total Time Away"}, {"table": "sheet1", "column": "Total Time Away"}, {"table": "sheet1", "column": "Total Time Away"}, {"table": "sheet1", "column": "Total Time Away"}, {"table": "sheet1", "column": "Total Time Away"}, {"table": "sheet1", "column": "Total Time Away"}, {"table": "sheet1", "column": "Total Time Away"}, {"table": "sheet6", "column": "Total Time Away"}, {"table": "sheet6", "column": "Total Time Away"}, {"table": "sheet6", "column": "Total Time Away"}, {"table": "sheet6", "column": "Total Time Away"}, {"table": "sheet6", "column": "Total Time Away"}, {"table": "sheet6", "column": "Total Time Away"}, {"table": "sheet1", "column": "Total Time Away"}, {"table": "sheet1", "column": "Total Time Away"}, {"table": "sheet1", "column": "Total Time Away"}, {"table": "sheet1", "column": "Total Time Away"}, {"table": "sheet1", "column": "Total Time Away"}, {"table": "sheet1", "column": "Total Time Away"}, {"table": "sheet6", "column": "Total Time Away"}, {"table": "sheet6", "column": "Total Time Away"}, {"table": "sheet6", "column": "Total Time Away"}, {"table": "sheet6", "column": "Total Time Away"}, {"table": "sheet6", "column": "Total Time Away"}, {"table": "sheet6", "column": "Total Time Away"}, {"table": "sheet1", "column": "Total Time Away"}, {"table": "sheet1", "column": "Total Time Away"}, {"table": "sheet1", "column": "Total Time Away"}, {"table": "sheet1", "column": "Total Time Away"}, {"table": "sheet1", "column": "Total Time Away"}, {"table": "sheet1", "column": "Total Time Away"}, {"table": "sheet6", "column": "Total Time Away"}, {"table": "sheet6", "column": "Total Time Away"}, {"table": "sheet6", "column": "Total Time Away"}, {"table": "sheet6", "column": "Total Time Away"}, {"table": "sheet6", "column": "Total Time Away"}, {"table": "sheet6", "column": "Total Time Away"}, {"table": "sheet1", "column": "Units Produced"}, {"table": "sheet6", "column": "Units Produced"}, {"table": "sheet1", "column": "Units Produced"}, {"table": "sheet6", "column": "Units Produced"}, {"table": "sheet1", "column": "Units Produced"}, {"table": "sheet6", "column": "Units Produced"}, {"table": "sheet1", "column": "Units Produced"}, {"table": "sheet6", "column": "Units Produced"}] | [] | False |


## S29

类别 `data`；来源 `query_db`；调用 `0f40338a81eb46e69c3baf3e9480a803`；状态 `success`。

```sql
SELECT DISTINCT "Employee ID", "Employee", "Base Salary", "Company Accommodation"
FROM (
  SELECT "Employee ID", "Employee", "Base Salary", "Company Accommodation" FROM sheet1
  UNION ALL
  SELECT "Employee ID", "Employee", "Base Salary", "Company Accommodation" FROM sheet2
  UNION ALL
  SELECT "Employee ID", "Employee", "Base Salary", "Company Accommodation" FROM sheet3
  UNION ALL
  SELECT "Employee ID", "Employee", "Base Salary", "Company Accommodation" FROM sheet4
  UNION ALL
  SELECT "Employee ID", "Employee", "Base Salary", "Company Accommodation" FROM sheet5
  UNION ALL
  SELECT "Employee ID", "Employee", "Base Salary", "Company Accommodation" FROM sheet6
)
GROUP BY "Employee ID", "Employee"
ORDER BY "Base Salary" DESC
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-009/attempt-01/sql/S29.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-009/attempt-01/sql/S29.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-009/attempt-01/results/S29.rows.jsonl)；完整：True；SHA256：`aeb9c7c8761366b40edd9a2f45c50a95f3f5843e14fdff35fc4bf5afdfed1eb1`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "sheet1", "kind": "base", "block": null, "base_tables": ["sheet1"]}] | [] | [] |
| B2 | [{"alias": "sheet2", "kind": "base", "block": null, "base_tables": ["sheet2"]}] | [] | [] |
| B3 | [] | [] | [] |
| B4 | [{"alias": "sheet3", "kind": "base", "block": null, "base_tables": ["sheet3"]}] | [] | [] |
| B5 | [] | [] | [] |
| B6 | [{"alias": "sheet4", "kind": "base", "block": null, "base_tables": ["sheet4"]}] | [] | [] |
| B7 | [] | [] | [] |
| B8 | [{"alias": "sheet5", "kind": "base", "block": null, "base_tables": ["sheet5"]}] | [] | [] |
| B9 | [] | [] | [] |
| B10 | [{"alias": "sheet6", "kind": "base", "block": null, "base_tables": ["sheet6"]}] | [] | [] |
| B11 | [] | [] | [] |
| B12 | [{"alias": "", "kind": "derived", "block": "B11", "base_tables": ["sheet1", "sheet2", "sheet3", "sheet4", "sheet5", "sheet6"]}] | [] | ["\"Employee ID\"", "\"Employee\""] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |


## S30

类别 `data`；来源 `query_db`；调用 `831f56663fd8420dbe207f28d0a435fe`；状态 `success`。

```sql
WITH all_rows AS (
  SELECT "Employee ID", "Gender", Team, "Workstation ID", "Units Produced" AS units FROM sheet1
  UNION ALL SELECT "Employee ID", "Gender", Team, "Workstation ID", "Units Produced" FROM sheet2
  UNION ALL SELECT "Employee ID", "Gender", Team, "Workstation ID", "Units Produced" FROM sheet3
  UNION ALL SELECT "Employee ID", "Gender", Team, "Workstation ID", "Units Produced" FROM sheet4
  UNION ALL SELECT "Employee ID", "Gender", Team, "Workstation ID", "Units Produced" FROM sheet5
  UNION ALL SELECT "Employee ID", "Gender", Team, "Workstation ID", "Units Produced" FROM sheet6
)
SELECT Team, "Gender", COUNT(DISTINCT "Employee ID") AS emps, ROUND(AVG(units),2) AS avg_units_per_day
FROM all_rows
GROUP BY Team, "Gender"
ORDER BY Team, "Gender"
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-009/attempt-01/sql/S30.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-009/attempt-01/sql/S30.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-009/attempt-01/results/S30.rows.jsonl)；完整：True；SHA256：`e32a5535b0c124607c1cf92f87fbcadc162ce0973bcc55a78f82d903df7eebf3`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "sheet1", "kind": "base", "block": null, "base_tables": ["sheet1"]}] | [] | [] |
| B2 | [{"alias": "sheet2", "kind": "base", "block": null, "base_tables": ["sheet2"]}] | [] | [] |
| B3 | [] | [] | [] |
| B4 | [{"alias": "sheet3", "kind": "base", "block": null, "base_tables": ["sheet3"]}] | [] | [] |
| B5 | [] | [] | [] |
| B6 | [{"alias": "sheet4", "kind": "base", "block": null, "base_tables": ["sheet4"]}] | [] | [] |
| B7 | [] | [] | [] |
| B8 | [{"alias": "sheet5", "kind": "base", "block": null, "base_tables": ["sheet5"]}] | [] | [] |
| B9 | [] | [] | [] |
| B10 | [{"alias": "sheet6", "kind": "base", "block": null, "base_tables": ["sheet6"]}] | [] | [] |
| B11 | [] | [] | [] |
| B12 | [{"alias": "all_rows", "kind": "derived", "block": "B11", "base_tables": ["sheet1", "sheet2", "sheet3", "sheet4", "sheet5", "sheet6"]}] | [] | ["Team", "\"Gender\""] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B12 | COUNT(DISTINCT "Employee ID") | [{"table": "sheet1", "column": "Employee ID"}, {"table": "sheet6", "column": "Employee ID"}] | [] | False |
| B12 | AVG(units) | [{"table": "sheet1", "column": "Units Produced"}, {"table": "sheet6", "column": "Units Produced"}] | [] | False |


## S31

类别 `data`；来源 `query_db`；调用 `1bb7f60ccc4d492e84c0a469960f1351`；状态 `success`。

```sql
WITH all_rows AS (
  SELECT "Employee ID", "Gender", "Workstation ID", "Units Produced" AS units FROM sheet1
  UNION ALL SELECT "Employee ID", "Gender", "Workstation ID", "Units Produced" FROM sheet2
  UNION ALL SELECT "Employee ID", "Gender", "Workstation ID", "Units Produced" FROM sheet3
  UNION ALL SELECT "Employee ID", "Gender", "Workstation ID", "Units Produced" FROM sheet4
  UNION ALL SELECT "Employee ID", "Gender", "Workstation ID", "Units Produced" FROM sheet5
  UNION ALL SELECT "Employee ID", "Gender", "Workstation ID", "Units Produced" FROM sheet6
)
SELECT "Workstation ID", COUNT(DISTINCT "Employee ID") AS emps,
       ROUND(AVG(units),2) AS avg_units, MIN("Gender") AS gender_sample
FROM all_rows
GROUP BY "Workstation ID"
ORDER BY avg_units DESC
LIMIT 15
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-009/attempt-01/sql/S31.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-009/attempt-01/sql/S31.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-009/attempt-01/results/S31.rows.jsonl)；完整：True；SHA256：`d0920b55eb28254f68355f57b0acd4640ff33f34ba7a814aefdf3251895dff1e`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "sheet1", "kind": "base", "block": null, "base_tables": ["sheet1"]}] | [] | [] |
| B2 | [{"alias": "sheet2", "kind": "base", "block": null, "base_tables": ["sheet2"]}] | [] | [] |
| B3 | [] | [] | [] |
| B4 | [{"alias": "sheet3", "kind": "base", "block": null, "base_tables": ["sheet3"]}] | [] | [] |
| B5 | [] | [] | [] |
| B6 | [{"alias": "sheet4", "kind": "base", "block": null, "base_tables": ["sheet4"]}] | [] | [] |
| B7 | [] | [] | [] |
| B8 | [{"alias": "sheet5", "kind": "base", "block": null, "base_tables": ["sheet5"]}] | [] | [] |
| B9 | [] | [] | [] |
| B10 | [{"alias": "sheet6", "kind": "base", "block": null, "base_tables": ["sheet6"]}] | [] | [] |
| B11 | [] | [] | [] |
| B12 | [{"alias": "all_rows", "kind": "derived", "block": "B11", "base_tables": ["sheet1", "sheet2", "sheet3", "sheet4", "sheet5", "sheet6"]}] | [] | ["\"Workstation ID\""] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B12 | COUNT(DISTINCT "Employee ID") | [{"table": "sheet1", "column": "Employee ID"}, {"table": "sheet6", "column": "Employee ID"}] | [] | False |
| B12 | MIN("Gender") | [{"table": "sheet1", "column": "Gender"}, {"table": "sheet6", "column": "Gender"}] | [] | False |
| B12 | AVG(units) | [{"table": "sheet1", "column": "Units Produced"}, {"table": "sheet6", "column": "Units Produced"}] | [] | False |


## S32

类别 `data`；来源 `query_db`；调用 `1a790dd44c044855b2380e8a04c9e478`；状态 `success`。

```sql
WITH all_rows AS (
  SELECT "Employee ID", "Gender", "Units Produced" AS units,
         "Away-from-Station Count" AS away_cnt,
         8.0 - (CAST(substr("Total Time Away",1,instr("Total Time Away",'min')-1) AS REAL)
                + CAST(substr("Total Time Away",instr("Total Time Away",'min')+3, instr("Total Time Away",'s')-instr("Total Time Away",'min')-3) AS REAL)/60.0)/60.0 AS eff_hours
  FROM sheet1 UNION ALL
  SELECT "Employee ID", "Gender", "Units Produced",
         "Away-from-Station Count",
         8.0 - (CAST(substr("Total Time Away",1,instr("Total Time Away",'min')-1) AS REAL)
                + CAST(substr("Total Time Away",instr("Total Time Away",'min')+3, instr("Total Time Away",'s')-instr("Total Time Away",'min')-3) AS REAL)/60.0)/60.0
  FROM sheet2 UNION ALL
  SELECT "Employee ID", "Gender", "Units Produced",
         "Away-from-Station Count",
         8.0 - (CAST(substr("Total Time Away",1,instr("Total Time Away",'min')-1) AS REAL)
                + CAST(substr("Total Time Away",instr("Total Time Away",'min')+3, instr("Total Time Away",'s')-instr("Total Time Away",'min')-3) AS REAL)/60.0)/60.0
  FROM sheet3 UNION ALL
  SELECT "Employee ID", "Gender", "Units Produced",
         "Away-from-Station Count",
         8.0 - (CAST(substr("Total Time Away",1,instr("Total Time Away",'min')-1) AS REAL)
                + CAST(substr("Total Time Away",instr("Total Time Away",'min')+3, instr("Total Time Away",'s')-instr("Total Time Away",'min')-3) AS REAL)/60.0)/60.0
  FROM sheet4 UNION ALL
  SELECT "Employee ID", "Gender", "Units Produced",
         "Away-from-Station Count",
         8.0 - (CAST(substr("Total Time Away",1,instr("Total Time Away",'min')-1) AS REAL)
                + CAST(substr("Total Time Away",instr("Total Time Away",'min')+3, instr("Total Time Away",'s')-instr("Total Time Away",'min')-3) AS REAL)/60.0)/60.0
  FROM sheet5 UNION ALL
  SELECT "Employee ID", "Gender", "Units Produced",
         "Away-from-Station Count",
         8.0 - (CAST(substr("Total Time Away",1,instr("Total Time Away",'min')-1) AS REAL)
                + CAST(substr("Total Time Away",instr("Total Time Away",'min')+3, instr("Total Time Away",'s')-instr("Total Time Away",'min')-3) AS REAL)/60.0)/60.0
  FROM sheet6
)
SELECT "Gender",
       ROUND(AVG(units),2) AS avg_units_per_day,
       ROUND(AVG(eff_hours),3) AS avg_eff_hours_per_day,
       ROUND(AVG(away_cnt),2) AS avg_away_count,
       ROUND(AVG(8.0 - eff_hours),2) AS avg_time_away_hours,
       COUNT(*) AS records
FROM all_rows
GROUP BY "Gender"
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-009/attempt-01/sql/S32.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-009/attempt-01/sql/S32.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-009/attempt-01/results/S32.rows.jsonl)；完整：True；SHA256：`d09af79dd5926046e4cb9e27ab979c2eeff8342f871f180b48638cb72e5e7b2c`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "sheet1", "kind": "base", "block": null, "base_tables": ["sheet1"]}] | [] | [] |
| B2 | [{"alias": "sheet2", "kind": "base", "block": null, "base_tables": ["sheet2"]}] | [] | [] |
| B3 | [] | [] | [] |
| B4 | [{"alias": "sheet3", "kind": "base", "block": null, "base_tables": ["sheet3"]}] | [] | [] |
| B5 | [] | [] | [] |
| B6 | [{"alias": "sheet4", "kind": "base", "block": null, "base_tables": ["sheet4"]}] | [] | [] |
| B7 | [] | [] | [] |
| B8 | [{"alias": "sheet5", "kind": "base", "block": null, "base_tables": ["sheet5"]}] | [] | [] |
| B9 | [] | [] | [] |
| B10 | [{"alias": "sheet6", "kind": "base", "block": null, "base_tables": ["sheet6"]}] | [] | [] |
| B11 | [] | [] | [] |
| B12 | [{"alias": "all_rows", "kind": "derived", "block": "B11", "base_tables": ["sheet1", "sheet2", "sheet3", "sheet4", "sheet5", "sheet6"]}] | [] | ["\"Gender\""] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B12 | COUNT(*) | [] | [] | True |
| B12 | AVG(units) | [{"table": "sheet1", "column": "Units Produced"}, {"table": "sheet6", "column": "Units Produced"}] | [] | False |
| B12 | AVG(eff_hours) | [{"table": "sheet1", "column": "Total Time Away"}, {"table": "sheet1", "column": "Total Time Away"}, {"table": "sheet1", "column": "Total Time Away"}, {"table": "sheet1", "column": "Total Time Away"}, {"table": "sheet1", "column": "Total Time Away"}, {"table": "sheet1", "column": "Total Time Away"}, {"table": "sheet6", "column": "Total Time Away"}, {"table": "sheet6", "column": "Total Time Away"}, {"table": "sheet6", "column": "Total Time Away"}, {"table": "sheet6", "column": "Total Time Away"}, {"table": "sheet6", "column": "Total Time Away"}, {"table": "sheet6", "column": "Total Time Away"}] | [] | False |
| B12 | AVG(away_cnt) | [{"table": "sheet1", "column": "Away-from-Station Count"}, {"table": "sheet6", "column": "Away-from-Station Count"}] | [] | False |
| B12 | AVG(8.0 - eff_hours) | [{"table": "sheet1", "column": "Total Time Away"}, {"table": "sheet1", "column": "Total Time Away"}, {"table": "sheet1", "column": "Total Time Away"}, {"table": "sheet1", "column": "Total Time Away"}, {"table": "sheet1", "column": "Total Time Away"}, {"table": "sheet1", "column": "Total Time Away"}, {"table": "sheet6", "column": "Total Time Away"}, {"table": "sheet6", "column": "Total Time Away"}, {"table": "sheet6", "column": "Total Time Away"}, {"table": "sheet6", "column": "Total Time Away"}, {"table": "sheet6", "column": "Total Time Away"}, {"table": "sheet6", "column": "Total Time Away"}] | [] | False |


## S33

类别 `data`；来源 `query_db`；调用 `d142fb787b7346ccbc701499eef9b8f8`；状态 `success`。

```sql
WITH all_rows AS (
  SELECT "Employee ID", "Date",
         substr(Date,1,7) AS month,
         "Units Produced" AS units,
         CAST(REPLACE("Pass Rate", '%','') AS REAL) AS pass_pct
  FROM sheet1 UNION ALL
  SELECT "Employee ID", Date, substr(Date,1,7), "Units Produced", CAST(REPLACE("Pass Rate", '%','') AS REAL) FROM sheet2 UNION ALL
  SELECT "Employee ID", Date, substr(Date,1,7), "Units Produced", CAST(REPLACE("Pass Rate", '%','') AS REAL) FROM sheet3 UNION ALL
  SELECT "Employee ID", Date, substr(Date,1,7), "Units Produced", CAST(REPLACE("Pass Rate", '%','') AS REAL) FROM sheet4 UNION ALL
  SELECT "Employee ID", Date, substr(Date,1,7), "Units Produced", CAST(REPLACE("Pass Rate", '%','') AS REAL) FROM sheet5 UNION ALL
  SELECT "Employee ID", Date, substr(Date,1,7), "Units Produced", CAST(REPLACE("Pass Rate", '%','') AS REAL) FROM sheet6
)
SELECT "Employee ID", month, COUNT(*) AS days, ROUND(SUM(units),1) AS units, ROUND(AVG(pass_pct),2) AS pass_rate
FROM all_rows GROUP BY "Employee ID", month
ORDER BY "Employee ID", month
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-009/attempt-01/sql/S33.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-009/attempt-01/sql/S33.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-009/attempt-01/results/S33.rows.jsonl)；完整：True；SHA256：`deb64cef47fdd3ffbcb28d7c3fd3f995a50fa9018445a31d7a8dd7ded7e02b87`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "sheet1", "kind": "base", "block": null, "base_tables": ["sheet1"]}] | [] | [] |
| B2 | [{"alias": "sheet2", "kind": "base", "block": null, "base_tables": ["sheet2"]}] | [] | [] |
| B3 | [] | [] | [] |
| B4 | [{"alias": "sheet3", "kind": "base", "block": null, "base_tables": ["sheet3"]}] | [] | [] |
| B5 | [] | [] | [] |
| B6 | [{"alias": "sheet4", "kind": "base", "block": null, "base_tables": ["sheet4"]}] | [] | [] |
| B7 | [] | [] | [] |
| B8 | [{"alias": "sheet5", "kind": "base", "block": null, "base_tables": ["sheet5"]}] | [] | [] |
| B9 | [] | [] | [] |
| B10 | [{"alias": "sheet6", "kind": "base", "block": null, "base_tables": ["sheet6"]}] | [] | [] |
| B11 | [] | [] | [] |
| B12 | [{"alias": "all_rows", "kind": "derived", "block": "B11", "base_tables": ["sheet1", "sheet2", "sheet3", "sheet4", "sheet5", "sheet6"]}] | [] | ["\"Employee ID\"", "month"] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B12 | COUNT(*) | [] | [] | True |
| B12 | SUM(units) | [{"table": "sheet1", "column": "Units Produced"}, {"table": "sheet6", "column": "Units Produced"}] | [] | False |
| B12 | AVG(pass_pct) | [{"table": "sheet1", "column": "Pass Rate"}, {"table": "sheet6", "column": "Pass Rate"}] | [] | False |


## S34

类别 `data`；来源 `query_db`；调用 `0205cd7e60914a34a1093f3d9ed8032c`；状态 `success`。

```sql
SELECT MIN("Units Produced") AS min_units, MAX("Units Produced") AS max_units, COUNT(*) AS n, COUNT(CASE WHEN "Units Produced" <= 0 THEN 1 END) AS nonpos FROM sheet1
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-009/attempt-01/sql/S34.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-009/attempt-01/sql/S34.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-009/attempt-01/results/S34.rows.jsonl)；完整：True；SHA256：`44e6681eecd919d08729485939c7d30a3c132e24b88d141a8ed341b43dc1eacc`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "sheet1", "kind": "base", "block": null, "base_tables": ["sheet1"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | MIN("Units Produced") | [{"table": "sheet1", "column": "Units Produced"}] | [] | False |
| B1 | MAX("Units Produced") | [{"table": "sheet1", "column": "Units Produced"}] | [] | False |
| B1 | COUNT(*) | [] | [] | True |
| B1 | COUNT(CASE WHEN "Units Produced" <= 0 THEN 1 END) | [] | [{"table": "sheet1", "column": "Units Produced"}] | False |


## S35

类别 `data`；来源 `query_db`；调用 `7708a88ac9214ce1bc3dd7ca4f37c401`；状态 `success`。

```sql
WITH all_rows AS (
  SELECT "Gender", "Away-from-Station Count" AS away_cnt FROM sheet1
  UNION ALL SELECT "Gender", "Away-from-Station Count" FROM sheet2
  UNION ALL SELECT "Gender", "Away-from-Station Count" FROM sheet3
  UNION ALL SELECT "Gender", "Away-from-Station Count" FROM sheet4
  UNION ALL SELECT "Gender", "Away-from-Station Count" FROM sheet5
  UNION ALL SELECT "Gender", "Away-from-Station Count" FROM sheet6
)
SELECT "Gender", COUNT(*) AS records,
       ROUND(AVG(away_cnt),2) AS avg_away_cnt,
       ROUND(MIN(away_cnt),1) AS min_away,
       ROUND(MAX(away_cnt),1) AS max_away
FROM all_rows GROUP BY "Gender"
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-009/attempt-01/sql/S35.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-009/attempt-01/sql/S35.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-009/attempt-01/results/S35.rows.jsonl)；完整：True；SHA256：`01681f95f49c9be3d09a3481ae09e56df5cb8efb9dc46796f76c4b352bc34d92`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "sheet1", "kind": "base", "block": null, "base_tables": ["sheet1"]}] | [] | [] |
| B2 | [{"alias": "sheet2", "kind": "base", "block": null, "base_tables": ["sheet2"]}] | [] | [] |
| B3 | [] | [] | [] |
| B4 | [{"alias": "sheet3", "kind": "base", "block": null, "base_tables": ["sheet3"]}] | [] | [] |
| B5 | [] | [] | [] |
| B6 | [{"alias": "sheet4", "kind": "base", "block": null, "base_tables": ["sheet4"]}] | [] | [] |
| B7 | [] | [] | [] |
| B8 | [{"alias": "sheet5", "kind": "base", "block": null, "base_tables": ["sheet5"]}] | [] | [] |
| B9 | [] | [] | [] |
| B10 | [{"alias": "sheet6", "kind": "base", "block": null, "base_tables": ["sheet6"]}] | [] | [] |
| B11 | [] | [] | [] |
| B12 | [{"alias": "all_rows", "kind": "derived", "block": "B11", "base_tables": ["sheet1", "sheet2", "sheet3", "sheet4", "sheet5", "sheet6"]}] | [] | ["\"Gender\""] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B12 | COUNT(*) | [] | [] | True |
| B12 | AVG(away_cnt) | [{"table": "sheet1", "column": "Away-from-Station Count"}, {"table": "sheet6", "column": "Away-from-Station Count"}] | [] | False |
| B12 | MIN(away_cnt) | [{"table": "sheet1", "column": "Away-from-Station Count"}, {"table": "sheet6", "column": "Away-from-Station Count"}] | [] | False |
| B12 | MAX(away_cnt) | [{"table": "sheet1", "column": "Away-from-Station Count"}, {"table": "sheet6", "column": "Away-from-Station Count"}] | [] | False |


## S36

类别 `data`；来源 `query_db`；调用 `2c4b59e04c614d1d8f2b3cb60d013dde`；状态 `success`。

```sql
WITH all_rows AS (
  SELECT "Employee ID", "Employee", "Gender", "Age", "Disciplinary Issue", "Reason for Infraction"
  FROM sheet1 UNION ALL
  SELECT "Employee ID", "Employee", "Gender", "Age", "Disciplinary Issue", "Reason for Infraction"
  FROM sheet2 UNION ALL
  SELECT "Employee ID", "Employee", "Gender", "Age", "Disciplinary Issue", "Reason for Infraction"
  FROM sheet3 UNION ALL
  SELECT "Employee ID", "Employee", "Gender", "Age", "Disciplinary Issue", "Reason for Infraction"
  FROM sheet4 UNION ALL
  SELECT "Employee ID", "Employee", "Gender", "Age", "Disciplinary Issue", "Reason for Infraction"
  FROM sheet5 UNION ALL
  SELECT "Employee ID", "Employee", "Gender", "Age", "Disciplinary Issue", "Reason for Infraction"
  FROM sheet6
)
SELECT "Reason for Infraction", COUNT(*) AS cnt, "Gender"
FROM all_rows
WHERE "Disciplinary Issue" = 'Yes'
GROUP BY "Reason for Infraction", "Gender"
ORDER BY cnt DESC
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-009/attempt-01/sql/S36.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-009/attempt-01/sql/S36.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-009/attempt-01/results/S36.rows.jsonl)；完整：True；SHA256：`8ab524a009db0d44171ffaf5dd2cd7337f30bedfff61b4bc7b5c90dfada878e3`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "sheet1", "kind": "base", "block": null, "base_tables": ["sheet1"]}] | [] | [] |
| B2 | [{"alias": "sheet2", "kind": "base", "block": null, "base_tables": ["sheet2"]}] | [] | [] |
| B3 | [] | [] | [] |
| B4 | [{"alias": "sheet3", "kind": "base", "block": null, "base_tables": ["sheet3"]}] | [] | [] |
| B5 | [] | [] | [] |
| B6 | [{"alias": "sheet4", "kind": "base", "block": null, "base_tables": ["sheet4"]}] | [] | [] |
| B7 | [] | [] | [] |
| B8 | [{"alias": "sheet5", "kind": "base", "block": null, "base_tables": ["sheet5"]}] | [] | [] |
| B9 | [] | [] | [] |
| B10 | [{"alias": "sheet6", "kind": "base", "block": null, "base_tables": ["sheet6"]}] | [] | [] |
| B11 | [] | [] | [] |
| B12 | [{"alias": "all_rows", "kind": "derived", "block": "B11", "base_tables": ["sheet1", "sheet2", "sheet3", "sheet4", "sheet5", "sheet6"]}] | [] | ["\"Reason for Infraction\"", "\"Gender\""] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B12 | COUNT(*) | [] | [] | True |

