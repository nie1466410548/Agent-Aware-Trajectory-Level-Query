# dacomp-019

Analyze, from the perspectives of inventory backlog, supply interruption, and risk of qual…

运行：已提交。官方未评分。全部 SQL 尝试/成功 41/40；数据 SQL 39/38；Python 12 次。

完整原题：

Analyze, from the perspectives of inventory backlog, supply interruption, and risk of quality issues, which imported and joint-venture (JV) drugs require prioritized supervision.

| 表 | 行数 | 列数 |
| --- | --- | --- |
| basic_drug_information | 427 | 23 |
| inventory_management | 428 | 20 |
| pricing_system | 428 | 20 |


实际路线（分析者依据 SQL/源码概括，不代表 Agent 自述）：检查药品来源、库存及质量字段 → SQL 关联进口/合资药品明细 → Python 构造积压、断供、质量风险评分及加权优先级 → 筛选高优先级药品并绘图。

数据库大小：499,712 字节。

## 数据 SQL

| SQL | 状态 | 基础表 | Join 输入/类型 | GROUP BY | 聚合表达式 | 结果行数 | 数据库 ms |
| --- | --- | --- | --- | --- | --- | --- | --- |
| [S3/Q1](#s3) | success | ["basic_drug_information"] | 0 / {} | [] | [] | 5 | 0.34 |
| [S4/Q2](#s4) | success | ["inventory_management"] | 0 / {} | [] | [] | 5 | 0.383 |
| [S5/Q3](#s5) | success | ["pricing_system"] | 0 / {} | [] | [] | 5 | 0.364 |
| [S6/Q4](#s6) | success | ["basic_drug_information"] | 0 / {} | [] | ["COUNT(*)", "COUNT(DISTINCT \"Drug ID\")"] | 1 | 0.661 |
| [S7/Q5](#s7) | success | ["basic_drug_information"] | 0 / {} | ["\"Origin / Tier (Domestic/Imported/JV)\""] | ["COUNT(*)"] | 3 | 0.478 |
| [S8/Q6](#s8) | success | ["inventory_management"] | 0 / {} | [] | ["COUNT(*)", "COUNT(DISTINCT \"Drug ID\")"] | 1 | 0.568 |
| [S9/Q7](#s9) | success | ["inventory_management"] | 0 / {} | ["\"Inventory Status (Normal/Frozen/Scrapped)\""] | ["COUNT(*)"] | 3 | 0.446 |
| [S10/Q8](#s10) | success | ["inventory_management"] | 0 / {} | ["\"Inventory Alert Status\""] | ["COUNT(*)"] | 3 | 0.437 |
| [S11/Q9](#s11) | success | ["basic_drug_information", "inventory_management"] | 2 / {'LEFT': 1} | [] | ["COUNT(*)"] | 1 | 0.974 |
| [S12/Q10](#s12) | success | ["basic_drug_information", "pricing_system"] | 2 / {'LEFT': 1} | [] | ["COUNT(*)"] | 1 | 0.885 |
| [S13/Q11](#s13) | success | ["basic_drug_information", "inventory_management", "pricing_system"] | 3 / {'LEFT': 2} | ["b.\"Drug ID\""] | ["COUNT(i.\"Inventory ID\")", "COUNT(p.\"Price ID\")"] | 0 | 1.74 |
| [S14/Q12](#s14) | success | ["basic_drug_information"] | 0 / {} | [] | [] | 10 | 0.391 |
| [S15/Q13](#s15) | success | ["basic_drug_information", "inventory_management"] | 2 / {'INNER': 1} | ["b.\"Origin / Tier (Domestic/Imported/JV)\""] | ["COUNT(CASE WHEN i.\"Inventory Status (Normal/Frozen/Scrapped)\" IN ('Frozen', 'Scrapped') THEN 1 END)", "COUNT(*)", "COUNT(*)", "COUNT(CASE WHEN i.\"Inventory Status (Normal/Frozen/Scrapped)\" IN ('Frozen', 'Scrapped') THEN 1 END)"] | 3 | 1.076 |
| [S16/Q14](#s16) | success | ["basic_drug_information", "inventory_management"] | 2 / {'INNER': 1} | ["b.\"Origin / Tier (Domestic/Imported/JV)\""] | ["COUNT(CASE WHEN i.\"Inventory Alert Status\" = 'Severe' THEN 1 END)", "COUNT(CASE WHEN i.\"Inventory Alert Status\" = 'Alert' THEN 1 END)", "COUNT(*)", "COUNT(*)", "COUNT(CASE WHEN i.\"Inventory Alert Status\" IN ('Alert', 'Severe') THEN 1 END)"] | 3 | 1.116 |
| [S17/Q15](#s17) | success | ["basic_drug_information", "inventory_management"] | 2 / {'INNER': 1} | ["b.\"Origin / Tier (Domestic/Imported/JV)\""] | ["AVG(i.\"Near-expiry Quantity\")", "AVG(i.\"Expired Quantity\")", "AVG(i.\"Damaged Quantity\")", "AVG(i.\"Returned Quantity\")", "AVG(i.\"Pest/Mold Damage Quantity\")", "AVG(i.\"Rodent Contamination Quantity\")", "AVG(i.\"Air Contamination Quantity\")", "AVG(i.\"Temp/Humidity Excursion Record\")"] | 3 | 1.475 |
| [S18/Q16](#s18) | success | ["basic_drug_information", "inventory_management"] | 2 / {'LEFT': 1} | ["i.\"Drug ID\""] | ["COUNT(*)"] | 1 | 0.877 |
| [S19/Q17](#s19) | success | ["basic_drug_information", "inventory_management"] | 2 / {'INNER': 1} | ["i.\"Drug ID\""] | ["COUNT(*)", "COUNT(*)"] | 0 | 1.059 |
| [S20/Q18](#s20) | success | ["inventory_management"] | 0 / {} | [] | ["MIN(\"Last Inbound Date\")", "MAX(\"Last Inbound Date\")", "MIN(\"Last Outbound Date\")", "MAX(\"Last Outbound Date\")"] | 1 | 0.535 |
| [S21/Q19](#s21) | success | ["basic_drug_information"] | 0 / {} | ["\"GSP Certification Status\""] | ["COUNT(*)"] | 2 | 0.384 |
| [S22/Q20](#s22) | success | ["basic_drug_information"] | 0 / {} | ["\"Storage conditions (room temperature/cool/refrigerated)\""] | ["COUNT(*)"] | 3 | 0.392 |
| [S23/Q21](#s23) | success | ["basic_drug_information"] | 0 / {} | ["\"Transportation mode (land/cold chain)\""] | ["COUNT(*)"] | 2 | 0.457 |
| [S24/Q22](#s24) | success | ["basic_drug_information", "inventory_management"] | 2 / {'INNER': 1} | ["b.\"Origin / Tier (Domestic/Imported/JV)\""] | ["AVG(1.0 * (i.\"Qualified Quantity\" + i.\"Near-expiry Quantity\" + i.\"Quarantine Quantity\") / NULLIF(b.\"Max Inventory Threshold\", 0))", "MAX(1.0 * (i.\"Qualified Quantity\" + i.\"Near-expiry Quantity\" + i.\"Quarantine Quantity\") / NULLIF(b.\"Max Inventory Threshold\", 0))", "AVG(1.0 * i.\"Qualified Quantity\" / NULLIF(b.\"Max Inventory Threshold\", 0))"] | 3 | 1.257 |
| [S25/Q23](#s25) | success | ["basic_drug_information", "inventory_management"] | 2 / {'INNER': 1} | ["b.\"Origin / Tier (Domestic/Imported/JV)\""] | ["COUNT(CASE WHEN JULIANDAY('2024-12-31') - JULIANDAY(i.\"Last Outbound Date\") > 180 THEN 1 END)", "COUNT(CASE WHEN JULIANDAY('2024-12-31') - JULIANDAY(i.\"Last Inbound Date\") > 180 THEN 1 END)", "COUNT(CASE WHEN i.\"Qualified Quantity\" = 0 THEN 1 END)", "COUNT(CASE WHEN i.\"Quarantine Quantity\" > 0 THEN 1 END)", "COUNT(*)"] | 3 | 1.35 |
| [S26/Q24](#s26) | success | ["inventory_management"] | 0 / {} | ["\"Inventory Discrepancy Rate\""] | ["COUNT(*)"] | 15 | 0.555 |
| [S27/Q25](#s27) | success | ["inventory_management"] | 0 / {} | [] | [] | 10 | 0.414 |
| [S28/Q26](#s28) | success | ["inventory_management"] | 0 / {} | [] | [] | 10 | 0.437 |
| [S29/Q27](#s29) | success | ["basic_drug_information", "inventory_management"] | 2 / {'INNER': 1} | [] | [] | 264 | 3.098 |
| [S30/Q28](#s30) | failed | ["dummy"] | 0 / {} | [] | [] | unknown | 未取得；调用总时长 0.159 ms |
| [S31/Q29](#s31) | success | ["basic_drug_information", "inventory_management"] | 2 / {'INNER': 1} | [] | [] | 264 | 2.963 |
| [S32/Q30](#s32) | success | ["basic_drug_information", "inventory_management"] | 2 / {'INNER': 1} | [] | [] | 264 | 2.608 |
| [S33/Q31](#s33) | success | ["basic_drug_information", "inventory_management"] | 2 / {'INNER': 1} | [] | [] | 264 | 2.732 |
| [S34/Q32](#s34) | success | ["basic_drug_information", "inventory_management"] | 2 / {'INNER': 1} | [] | [] | 264 | 2.734 |
| [S35/Q33](#s35) | success | ["basic_drug_information", "inventory_management"] | 2 / {'INNER': 1} | ["b.\"Origin / Tier (Domestic/Imported/JV)\""] | ["AVG(i.\"Qualified Quantity\" + i.\"Near-expiry Quantity\" + i.\"Quarantine Quantity\")", "AVG(1.0 * (i.\"Qualified Quantity\" + i.\"Near-expiry Quantity\" + i.\"Quarantine Quantity\") / b.\"Max Inventory Threshold\")", "AVG(i.\"Near-expiry Quantity\")", "AVG(i.\"Expired Quantity\")", "AVG(CASE WHEN i.\"Quarantine Quantity\" > 0 THEN 1 ELSE 0 END)", "AVG(CASE WHEN i.\"Qualified Quantity\" = 0 THEN 1 ELSE 0 END)", "AVG(CASE WHEN i.\"Inventory Status (Normal/Frozen/Scrapped)\" = 'Frozen' THEN 1 ELSE 0 END)", "AVG(CASE WHEN i.\"Inventory Status (Normal/Frozen/Scrapped)\" = 'Scrapped' THEN 1 ELSE 0 END)"] | 2 | 1.414 |
| [S36/Q34](#s36) | success | ["basic_drug_information", "pricing_system"] | 2 / {'INNER': 1} | ["b.\"Origin / Tier (Domestic/Imported/JV)\""] | ["COUNT(CASE WHEN p.\"Abnormal Price Fluctuation Flag\" = 'Yes' THEN 1 END)", "COUNT(*)"] | 2 | 0.969 |
| [S37/Q35](#s37) | success | ["basic_drug_information"] | 0 / {} | ["b.\"Origin / Tier (Domestic/Imported/JV)\""] | ["COUNT(CASE WHEN b.\"GSP Certification Status\" = 'Not certified' THEN 1 END)", "COUNT(CASE WHEN b.\"Storage conditions (room temperature/cool/refrigerated)\" = 'Refrigerated' THEN 1 END)", "COUNT(CASE WHEN b.\"Transportation mode (land/cold chain)\" = 'Cold-chain' THEN 1 END)", "COUNT(*)"] | 2 | 0.621 |
| [S38/Q36](#s38) | success | ["basic_drug_information", "inventory_management"] | 2 / {'INNER': 1} | ["CASE WHEN i.\"Inventory Status (Normal/Frozen/Scrapped)\" IN ('Frozen', 'Scrapped') AND i.\"Qualified Quantity\" = 0 THEN 'Dual risk (frozen/scrapped + zero qualified)' WHEN i.\"Inventory Status (Normal/Frozen/Scrapped)\" IN ('Frozen', 'Scrapped') THEN 'Status frozen/scrapped' WHEN i.\"Qualified Quantity\" = 0 THEN 'Zero qualified only' ELSE 'Normal' END", "b.\"Origin / Tier (Domestic/Imported/JV)\""] | ["COUNT(*)", "AVG(i.\"Near-expiry Quantity\")", "AVG(i.\"Expired Quantity\")", "AVG(i.\"Temp/Humidity Excursion Record\")"] | 7 | 1.283 |
| [S39/Q37](#s39) | success | ["basic_drug_information", "inventory_management"] | 2 / {'INNER': 1} | ["b.\"Origin / Tier (Domestic/Imported/JV)\""] | ["COUNT(CASE WHEN i.\"Inventory Alert Status\" = 'Severe' AND i.\"Inventory Status (Normal/Frozen/Scrapped)\" = 'Frozen' THEN 1 END)", "COUNT(CASE WHEN i.\"Inventory Alert Status\" = 'Severe' AND i.\"Inventory Status (Normal/Frozen/Scrapped)\" = 'Scrapped' THEN 1 END)", "COUNT(CASE WHEN i.\"Inventory Alert Status\" = 'Severe' AND i.\"Qualified Quantity\" = 0 THEN 1 END)", "COUNT(*)"] | 2 | 1.094 |
| [S40/Q38](#s40) | success | ["basic_drug_information", "inventory_management"] | 2 / {'INNER': 1} | [] | [] | 13 | 1.101 |
| [S41/Q39](#s41) | success | ["basic_drug_information", "inventory_management"] | 2 / {'INNER': 1} | ["b.\"Origin / Tier (Domestic/Imported/JV)\""] | ["COUNT(*)", "AVG(i.\"Expired Quantity\" + i.\"Damaged Quantity\" + i.\"Returned Quantity\" + i.\"Pest/Mold Damage Quantity\" + i.\"Rodent Contamination Quantity\" + i.\"Air Contamination Quantity\" + i.\"Temp/Humidity Excursion Record\")", "AVG(1.0 * (i.\"Expired Quantity\" + i.\"Damaged Quantity\" + i.\"Returned Quantity\" + i.\"Pest/Mold Damage Quantity\" + i.\"Rodent Contamination Quantity\" + i.\"Air Contamination Quantity\") / NULLIF(i.\"Qualified Quantity\" + i.\"Near-expiry Quantity\" + i.\"Quarantine Quantity\", 0) * 100)"] | 2 | 1.451 |


## 元数据和设置

| SQL | 类别 | 状态 | 内容 |
| --- | --- | --- | --- |
| S1 | connection_setup | success | PRAGMA query_only=ON |
| S2 | metadata | success | SELECT name,sql FROM sqlite_master WHERE type='table' ORDER BY name |


## Python 与执行位置

人工源码审查：**database_first_violation**。P9 computes date differences, stock ratios, conditional risk flags and weighted priority scores, then Top-20 selection in Python; P10 computes origin/tier grouped summaries. These are SQL-capable arithmetic, CASE/ranking and aggregation. Quantile clipping and rendering are distinguished from that relational preparation. Earlier Python calls also show archive-path/column-shape errors; repeated SQL in this trajectory partly reflects tool-interface adaptation and cannot be attributed solely to intentional analytical refinement. [证据](../reviews/dacomp-019.json)。

P1：Composite risk scoring requires parsing mixed-format discrepancy rates (some "X%", some decimal), converting timestamps to staleness days, and combining many heterogeneous indicators into normalized sub-scores (backlog, supply interruption, quality). These data-cleaning and scoring steps are not cleanly expressible in SQLite, so the pre-joined 264-row extract (Imported/JV only) is processed here.

[源码](../../../runs/dsv4flash-db-first-full-01/dacomp-019/attempt-01/python/P1.py)；[输出](../../../runs/dsv4flash-db-first-full-01/dacomp-019/attempt-01/python/P1.stdout)；[错误](../../../runs/dsv4flash-db-first-full-01/dacomp-019/attempt-01/python/P1.stderr)。检出需人工核验的 SQL 可实现操作：.query(；不能仅凭理由判为合规。

P2：Load the pre-joined 264-row extract of Imported/JV drugs from the archived result file into pandas for composite scoring and visualization.

[源码](../../../runs/dsv4flash-db-first-full-01/dacomp-019/attempt-01/python/P2.py)；[输出](../../../runs/dsv4flash-db-first-full-01/dacomp-019/attempt-01/python/P2.stdout)；[错误](../../../runs/dsv4flash-db-first-full-01/dacomp-019/attempt-01/python/P2.stderr)。自动源码筛查未检出预设迁出信号；这不是全面语义合规证明。

P3：Inspect the JSONL file format to understand how to parse it correctly.

[源码](../../../runs/dsv4flash-db-first-full-01/dacomp-019/attempt-01/python/P3.py)；[输出](../../../runs/dsv4flash-db-first-full-01/dacomp-019/attempt-01/python/P3.stdout)；[错误](../../../runs/dsv4flash-db-first-full-01/dacomp-019/attempt-01/python/P3.stderr)。自动源码筛查未检出预设迁出信号；这不是全面语义合规证明。

P4：Find the working directory structure to locate result files.

[源码](../../../runs/dsv4flash-db-first-full-01/dacomp-019/attempt-01/python/P4.py)；[输出](../../../runs/dsv4flash-db-first-full-01/dacomp-019/attempt-01/python/P4.stdout)；[错误](../../../runs/dsv4flash-db-first-full-01/dacomp-019/attempt-01/python/P4.stderr)。自动源码筛查未检出预设迁出信号；这不是全面语义合规证明。

P5：Locate the results directory inside the workspace to access archived query results.

[源码](../../../runs/dsv4flash-db-first-full-01/dacomp-019/attempt-01/python/P5.py)；[输出](../../../runs/dsv4flash-db-first-full-01/dacomp-019/attempt-01/python/P5.stdout)；[错误](../../../runs/dsv4flash-db-first-full-01/dacomp-019/attempt-01/python/P5.stderr)。自动源码筛查未检出预设迁出信号；这不是全面语义合规证明。

P6：Use the logged Python interface to retrieve the Imported/JV extract as a DataFrame for composite scoring.

[源码](../../../runs/dsv4flash-db-first-full-01/dacomp-019/attempt-01/python/P6.py)；[输出](../../../runs/dsv4flash-db-first-full-01/dacomp-019/attempt-01/python/P6.stdout)；[错误](../../../runs/dsv4flash-db-first-full-01/dacomp-019/attempt-01/python/P6.stderr)。检出需人工核验的 SQL 可实现操作：.query(；不能仅凭理由判为合规。

P7：Inspect the structure of the returned rows to understand how to build the DataFrame properly.

[源码](../../../runs/dsv4flash-db-first-full-01/dacomp-019/attempt-01/python/P7.py)；[输出](../../../runs/dsv4flash-db-first-full-01/dacomp-019/attempt-01/python/P7.stdout)；[错误](../../../runs/dsv4flash-db-first-full-01/dacomp-019/attempt-01/python/P7.stderr)。检出需人工核验的 SQL 可实现操作：.query(；不能仅凭理由判为合规。

P8：Build the DataFrame using the columns metadata from the query result execution object.

[源码](../../../runs/dsv4flash-db-first-full-01/dacomp-019/attempt-01/python/P8.py)；[输出](../../../runs/dsv4flash-db-first-full-01/dacomp-019/attempt-01/python/P8.stdout)；[错误](../../../runs/dsv4flash-db-first-full-01/dacomp-019/attempt-01/python/P8.stderr)。检出需人工核验的 SQL 可实现操作：.query(；不能仅凭理由判为合规。

P9：Composite scoring of Imported/JV drugs across three risk dimensions. The scoring involves normalization of heterogeneous metrics, log-transforms for skewed distributions, and weighted combination of categorical/continuous indicators. This is not feasibly done in SQLite due to the parsing of mixed-format discrepancy rates and the iterative score calibration.

[源码](../../../runs/dsv4flash-db-first-full-01/dacomp-019/attempt-01/python/P9.py)；[输出](../../../runs/dsv4flash-db-first-full-01/dacomp-019/attempt-01/python/P9.stdout)；[错误](../../../runs/dsv4flash-db-first-full-01/dacomp-019/attempt-01/python/P9.stderr)。检出需人工核验的 SQL 可实现操作：.query(；不能仅凭理由判为合规。

P10：Visualize the composite scoring results: box/violin distributions by origin, top-15 priority ranking, and a multi-dimensional bubble scatter to communicate findings clearly. This is a visualization step outside SQL.

[源码](../../../runs/dsv4flash-db-first-full-01/dacomp-019/attempt-01/python/P10.py)；[输出](../../../runs/dsv4flash-db-first-full-01/dacomp-019/attempt-01/python/P10.stdout)；[错误](../../../runs/dsv4flash-db-first-full-01/dacomp-019/attempt-01/python/P10.stderr)。检出需人工核验的 SQL 可实现操作：groupby(；不能仅凭理由判为合规。

P11：Extract the detailed risk profile of the top-priority Imported/JV drugs to substantiate which specific indicators drive their priority ranking.

[源码](../../../runs/dsv4flash-db-first-full-01/dacomp-019/attempt-01/python/P11.py)；[输出](../../../runs/dsv4flash-db-first-full-01/dacomp-019/attempt-01/python/P11.stdout)；[错误](../../../runs/dsv4flash-db-first-full-01/dacomp-019/attempt-01/python/P11.stderr)。检出需人工核验的 SQL 可实现操作：groupby(, sort_values(；不能仅凭理由判为合规。

P12：Generate supplementary visualizations: heatmap of top-15 risk profiles, histogram of priority scores for each origin, and a bar chart comparing key risk indicators between Imported and JV drugs.

[源码](../../../runs/dsv4flash-db-first-full-01/dacomp-019/attempt-01/python/P12.py)；[输出](../../../runs/dsv4flash-db-first-full-01/dacomp-019/attempt-01/python/P12.stdout)；[错误](../../../runs/dsv4flash-db-first-full-01/dacomp-019/attempt-01/python/P12.stderr)。自动源码筛查未检出预设迁出信号；这不是全面语义合规证明。

## 优化机会

已验证候选。筛选限于精确 SQL、相同自包含 CTE、相同单表完整过滤、可分解单表聚合；未覆盖任意 Join 等价和一般谓词蕴含。全部候选都是 offline，未测在线预测。

| 候选 | 类型 | 已有结果 | 覆盖 SQL | 后续次数 | 中间行数 | 验证 | 成本 |
| --- | --- | --- | --- | --- | --- | --- | --- |
| C1 | exact-result reuse | True | ["S31", "S32", "S33", "S34"] | 3 | 264 | verified | Not benchmarked; correctness alone does not establish net speedup. |
| C2 | aggregate MV | False | ["S7", "S21", "S22", "S23"] | 3 | 36 | verified | Not benchmarked; correctness alone does not establish net speedup. |
| C3 | aggregate MV | False | ["S9", "S10", "S20", "S26"] | 3 | 401 | verified | Not benchmarked; correctness alone does not establish net speedup. |


已验证覆盖（含触发查询、候选并集去重）：12/38 条成功数据 SQL。正确性仅针对当前数据库快照；未测性能的候选不能声称已加速。

[完整 build/rewrite 与比较证据](dacomp-019.analysis.json)。

### C1：exact-result reuse

Identical normalized SQL and parameters; archive equality checked.

原查询 [S31](#s31), [S32](#s32), [S33](#s33), [S34](#s34) → 保留前序结果 S31 → 后续 3 次可复用。该构建点为事后假设，不代表 Agent 当时预知后续。

| 原 SQL | 列名一致 | 结果一致 | 比较方法 |
| --- | --- | --- | --- |
| S32 | True | True | ordered_numeric_tolerance |
| S33 | True | True | ordered_numeric_tolerance |
| S34 | True | True | ordered_numeric_tolerance |


验证状态：verified；成本结论：Not benchmarked; correctness alone does not establish net speedup.

### C2：aggregate MV

Union of grouping keys; decomposable aggregate states; AVG uses SUM and non-NULL COUNT.

原查询 [S7](#s7), [S21](#s21), [S22](#s22), [S23](#s23) → 新增共享状态 C2 → 后续 3 次可复用。该构建点为事后假设，不代表 Agent 当时预知后续。

构建定义：

```sql
SELECT "Origin / Tier (Domestic/Imported/JV)" AS __g0, "GSP Certification Status" AS __g1, "Storage conditions (room temperature/cool/refrigerated)" AS __g2, "Transportation mode (land/cold chain)" AS __g3, COUNT(*) AS __a0 FROM "basic_drug_information"  GROUP BY "Origin / Tier (Domestic/Imported/JV)", "GSP Certification Status", "Storage conditions (room temperature/cool/refrigerated)", "Transportation mode (land/cold chain)"
```

受益查询 S7 的改写示例：

```sql
SELECT __g0 AS origin, SUM(__a0) AS cnt FROM temp.reuse_candidate GROUP BY __g0
```

| 原 SQL | 列名一致 | 结果一致 | 比较方法 |
| --- | --- | --- | --- |
| S7 | True | True | exact_multiset |
| S21 | True | True | exact_multiset |
| S22 | True | True | exact_multiset |
| S23 | True | True | exact_multiset |


验证状态：verified；成本结论：Not benchmarked; correctness alone does not establish net speedup.

### C3：aggregate MV

Union of grouping keys; decomposable aggregate states; AVG uses SUM and non-NULL COUNT.

原查询 [S9](#s9), [S10](#s10), [S20](#s20), [S26](#s26) → 新增共享状态 C3 → 后续 3 次可复用。该构建点为事后假设，不代表 Agent 当时预知后续。

构建定义：

```sql
SELECT "Inventory Status (Normal/Frozen/Scrapped)" AS __g0, "Inventory Alert Status" AS __g1, "Inventory Discrepancy Rate" AS __g2, COUNT(*) AS __a0, MIN("Last Inbound Date") AS __a1, MAX("Last Inbound Date") AS __a2, MIN("Last Outbound Date") AS __a3, MAX("Last Outbound Date") AS __a4 FROM "inventory_management"  GROUP BY "Inventory Status (Normal/Frozen/Scrapped)", "Inventory Alert Status", "Inventory Discrepancy Rate"
```

受益查询 S9 的改写示例：

```sql
SELECT __g0 AS status, SUM(__a0) AS cnt FROM temp.reuse_candidate GROUP BY __g0
```

| 原 SQL | 列名一致 | 结果一致 | 比较方法 |
| --- | --- | --- | --- |
| S9 | True | True | exact_multiset |
| S10 | True | True | exact_multiset |
| S20 | True | True | exact_multiset |
| S26 | True | True | ordered_numeric_tolerance |


验证状态：verified；成本结论：Not benchmarked; correctness alone does not establish net speedup.

结果依赖：自动记录 SQL→Python 的接口父调用，以及源码中引用归档文件的消费者；字面值相同不认定因果。模型方向选择需要人工读取消息，尚未做全面因果标注。

[原始报告](../../../runs/dsv4flash-db-first-full-01/dacomp-019/attempt-01/answer.md)；[统一消息](../../../runs/dsv4flash-db-first-full-01/dacomp-019/attempt-01/messages.jsonl)；[原始 OpenCode 事件](../../../runs/dsv4flash-db-first-full-01/dacomp-019/attempt-01/opencode.jsonl)；[SQL 引擎日志](../../../runs/dsv4flash-db-first-full-01/dacomp-019/attempt-01/sql_journal.jsonl)。

[可读报告（本地图片链接规范化）](../answers/dacomp-019.md)。原始回答保留，分析结论未改写。

## S1

类别 `connection_setup`；来源 `connection`；调用 `12e49f7e992f4b83ac7f452533af1e08`；状态 `success`。

```sql
PRAGMA query_only=ON
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-019/attempt-01/sql/S1.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-019/attempt-01/sql/S1.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-019/attempt-01/results/S1.rows.jsonl)；完整：True；SHA256：`e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`。

## S2

类别 `metadata`；来源 `list_db`；调用 `12e49f7e992f4b83ac7f452533af1e08`；状态 `success`。

```sql
SELECT name,sql FROM sqlite_master WHERE type='table' ORDER BY name
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-019/attempt-01/sql/S2.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-019/attempt-01/sql/S2.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-019/attempt-01/results/S2.rows.jsonl)；完整：True；SHA256：`e1d493f8bfe9476f857c56da53c5696a09bbd41e291ee239ab37313bea86bcfd`。

## S3

类别 `data`；来源 `query_db`；调用 `966c0c09c16c49c79dbd400d5cbb9068`；状态 `success`。

```sql
SELECT * FROM basic_drug_information LIMIT 5
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-019/attempt-01/sql/S3.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-019/attempt-01/sql/S3.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-019/attempt-01/results/S3.rows.jsonl)；完整：True；SHA256：`6a57f2f7289cfcc769bb19a4fd4d978207160e7b93d0b5206fea21189a068816`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "basic_drug_information", "kind": "base", "block": null, "base_tables": ["basic_drug_information"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |


## S4

类别 `data`；来源 `query_db`；调用 `f0d61d99270b463ab3bcc767c901fab7`；状态 `success`。

```sql
SELECT * FROM inventory_management LIMIT 5
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-019/attempt-01/sql/S4.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-019/attempt-01/sql/S4.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-019/attempt-01/results/S4.rows.jsonl)；完整：True；SHA256：`1569016b1441d624c323bba576f9cbc4a0e09abe91eadcc7ccf7a7074bf201f4`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "inventory_management", "kind": "base", "block": null, "base_tables": ["inventory_management"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |


## S5

类别 `data`；来源 `query_db`；调用 `f63a45fbeb0a4555a36743e55e5b2f9b`；状态 `success`。

```sql
SELECT * FROM pricing_system LIMIT 5
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-019/attempt-01/sql/S5.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-019/attempt-01/sql/S5.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-019/attempt-01/results/S5.rows.jsonl)；完整：True；SHA256：`e492788d6c57df2081201407be8b46bb848789729aa4a79e05b212a99c22ada6`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "pricing_system", "kind": "base", "block": null, "base_tables": ["pricing_system"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |


## S6

类别 `data`；来源 `query_db`；调用 `800060d70245410aa05ea544b812c91e`；状态 `success`。

```sql
SELECT COUNT(*) AS total_drugs, COUNT(DISTINCT "Drug ID") AS unique_drugs FROM basic_drug_information
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-019/attempt-01/sql/S6.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-019/attempt-01/sql/S6.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-019/attempt-01/results/S6.rows.jsonl)；完整：True；SHA256：`81987d86a5612ea4ae8b4f180971ac1e29e8418c1c3e0a82f82fbc5e9910b236`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "basic_drug_information", "kind": "base", "block": null, "base_tables": ["basic_drug_information"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |
| B1 | COUNT(DISTINCT "Drug ID") | [{"table": "basic_drug_information", "column": "Drug ID"}] | [] | False |


## S7

类别 `data`；来源 `query_db`；调用 `a52c55470251407fb321a019479893a2`；状态 `success`。

```sql
SELECT "Origin / Tier (Domestic/Imported/JV)" AS origin, COUNT(*) AS cnt FROM basic_drug_information GROUP BY 1
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-019/attempt-01/sql/S7.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-019/attempt-01/sql/S7.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-019/attempt-01/results/S7.rows.jsonl)；完整：True；SHA256：`8b8651e548b4e5fead15358f011da90ba555f28d55901f212ed20037e683d550`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "basic_drug_information", "kind": "base", "block": null, "base_tables": ["basic_drug_information"]}] | [] | ["\"Origin / Tier (Domestic/Imported/JV)\""] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |


## S8

类别 `data`；来源 `query_db`；调用 `2af8a8853d294d2990702aaffd437ee5`；状态 `success`。

```sql
SELECT COUNT(*) AS total_inv, COUNT(DISTINCT "Drug ID") AS unique_drugs FROM inventory_management
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-019/attempt-01/sql/S8.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-019/attempt-01/sql/S8.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-019/attempt-01/results/S8.rows.jsonl)；完整：True；SHA256：`68eb15aaa3bc6d42f54d2322c699ec332f023c8596bb31039d08c9ecc4a0d1a7`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "inventory_management", "kind": "base", "block": null, "base_tables": ["inventory_management"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |
| B1 | COUNT(DISTINCT "Drug ID") | [{"table": "inventory_management", "column": "Drug ID"}] | [] | False |


## S9

类别 `data`；来源 `query_db`；调用 `34036b69c3d3420589b2e503fcb14abc`；状态 `success`。

```sql
SELECT "Inventory Status (Normal/Frozen/Scrapped)" AS status, COUNT(*) AS cnt FROM inventory_management GROUP BY 1
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-019/attempt-01/sql/S9.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-019/attempt-01/sql/S9.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-019/attempt-01/results/S9.rows.jsonl)；完整：True；SHA256：`f027e651a296d63a8926761afcd374a7b57d88f8f9956426cc6d045a3cb64a83`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "inventory_management", "kind": "base", "block": null, "base_tables": ["inventory_management"]}] | [] | ["\"Inventory Status (Normal/Frozen/Scrapped)\""] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |


## S10

类别 `data`；来源 `query_db`；调用 `2ad0148be01e46b1beb3b516ea20e829`；状态 `success`。

```sql
SELECT "Inventory Alert Status" AS alert, COUNT(*) AS cnt FROM inventory_management GROUP BY 1
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-019/attempt-01/sql/S10.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-019/attempt-01/sql/S10.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-019/attempt-01/results/S10.rows.jsonl)；完整：True；SHA256：`af75320e3e645536318a509b8ccda9b64b8f649a836b125eb43d0434eba13ba6`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "inventory_management", "kind": "base", "block": null, "base_tables": ["inventory_management"]}] | [] | ["\"Inventory Alert Status\""] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |


## S11

类别 `data`；来源 `query_db`；调用 `9e3c3e52dc13437f99ae592390214ed7`；状态 `success`。

```sql
SELECT COUNT(*) AS missing_inv FROM basic_drug_information b LEFT JOIN inventory_management i ON b."Drug ID" = i."Drug ID" WHERE i."Drug ID" IS NULL
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-019/attempt-01/sql/S11.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-019/attempt-01/sql/S11.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-019/attempt-01/results/S11.rows.jsonl)；完整：True；SHA256：`c14196f132c1e9be0508ae80ab52fcb3e1d3fc05880415f3dc980971df207c9e`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "b", "kind": "base", "block": null, "base_tables": ["basic_drug_information"]}, {"alias": "i", "kind": "base", "block": null, "base_tables": ["inventory_management"]}] | [{"type": "LEFT", "right": "inventory_management AS i", "on": "b.\"Drug ID\" = i.\"Drug ID\"", "using": []}] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |


## S12

类别 `data`；来源 `query_db`；调用 `0cb05dfc2c0a4f10b0064abc8924b0e6`；状态 `success`。

```sql
SELECT COUNT(*) AS missing_price FROM basic_drug_information b LEFT JOIN pricing_system p ON b."Drug ID" = p."Drug ID" WHERE p."Drug ID" IS NULL
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-019/attempt-01/sql/S12.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-019/attempt-01/sql/S12.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-019/attempt-01/results/S12.rows.jsonl)；完整：True；SHA256：`acc07b62f23f458923737c4cd4a66bd05d1e71eb4f384003baaf2dcc760d6349`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "b", "kind": "base", "block": null, "base_tables": ["basic_drug_information"]}, {"alias": "p", "kind": "base", "block": null, "base_tables": ["pricing_system"]}] | [{"type": "LEFT", "right": "pricing_system AS p", "on": "b.\"Drug ID\" = p.\"Drug ID\"", "using": []}] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |


## S13

类别 `data`；来源 `query_db`；调用 `85ae28561b384704965b691bab1a1890`；状态 `success`。

```sql
SELECT b."Drug ID", COUNT(i."Inventory ID") AS inv_cnt, COUNT(p."Price ID") AS price_cnt FROM basic_drug_information b LEFT JOIN inventory_management i ON b."Drug ID" = i."Drug ID" LEFT JOIN pricing_system p ON b."Drug ID" = p."Drug ID" GROUP BY b."Drug ID" HAVING inv_cnt > 1 OR price_cnt > 1 LIMIT 10
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-019/attempt-01/sql/S13.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-019/attempt-01/sql/S13.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-019/attempt-01/results/S13.rows.jsonl)；完整：True；SHA256：`e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "b", "kind": "base", "block": null, "base_tables": ["basic_drug_information"]}, {"alias": "i", "kind": "base", "block": null, "base_tables": ["inventory_management"]}, {"alias": "p", "kind": "base", "block": null, "base_tables": ["pricing_system"]}] | [{"type": "LEFT", "right": "inventory_management AS i", "on": "b.\"Drug ID\" = i.\"Drug ID\"", "using": []}, {"type": "LEFT", "right": "pricing_system AS p", "on": "b.\"Drug ID\" = p.\"Drug ID\"", "using": []}] | ["b.\"Drug ID\""] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(i."Inventory ID") | [{"table": "inventory_management", "column": "Inventory ID"}] | [] | False |
| B1 | COUNT(p."Price ID") | [{"table": "pricing_system", "column": "Price ID"}] | [] | False |


## S14

类别 `data`；来源 `query_db`；调用 `f4fc8eb4efb14d63ba1d4eae56f4246c`；状态 `success`。

```sql
SELECT "Max Inventory Threshold" AS thresh, "Expiry Alert Days" AS alert_days FROM basic_drug_information LIMIT 10
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-019/attempt-01/sql/S14.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-019/attempt-01/sql/S14.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-019/attempt-01/results/S14.rows.jsonl)；完整：True；SHA256：`282d8b674e19bae1dfd2cf3e8dd17799c6d5da1c2a71bf2ae477a3c10101abb2`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "basic_drug_information", "kind": "base", "block": null, "base_tables": ["basic_drug_information"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |


## S15

类别 `data`；来源 `query_db`；调用 `c0e11f111bb34edf8f2f6bfcc0cba17e`；状态 `success`。

```sql
SELECT b."Origin / Tier (Domestic/Imported/JV)" AS origin, 
       COUNT(CASE WHEN i."Inventory Status (Normal/Frozen/Scrapped)" IN ('Frozen', 'Scrapped') THEN 1 END) AS problem_status_cnt,
       COUNT(*) AS total_cnt,
       ROUND(100.0 * COUNT(CASE WHEN i."Inventory Status (Normal/Frozen/Scrapped)" IN ('Frozen', 'Scrapped') THEN 1 END) / COUNT(*), 1) AS pct_problem
FROM basic_drug_information b
JOIN inventory_management i ON b."Drug ID" = i."Drug ID"
GROUP BY 1
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-019/attempt-01/sql/S15.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-019/attempt-01/sql/S15.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-019/attempt-01/results/S15.rows.jsonl)；完整：True；SHA256：`f0e283e569dca0252472c4721565548a2ea417e97285ee390083deddc6df8482`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "b", "kind": "base", "block": null, "base_tables": ["basic_drug_information"]}, {"alias": "i", "kind": "base", "block": null, "base_tables": ["inventory_management"]}] | [{"type": "INNER", "right": "inventory_management AS i", "on": "b.\"Drug ID\" = i.\"Drug ID\"", "using": []}] | ["b.\"Origin / Tier (Domestic/Imported/JV)\""] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(CASE WHEN i."Inventory Status (Normal/Frozen/Scrapped)" IN ('Frozen', 'Scrapped') THEN 1 END) | [] | [{"table": "inventory_management", "column": "Inventory Status (Normal/Frozen/Scrapped)"}] | False |
| B1 | COUNT(*) | [] | [] | True |
| B1 | COUNT(*) | [] | [] | True |
| B1 | COUNT(CASE WHEN i."Inventory Status (Normal/Frozen/Scrapped)" IN ('Frozen', 'Scrapped') THEN 1 END) | [] | [{"table": "inventory_management", "column": "Inventory Status (Normal/Frozen/Scrapped)"}] | False |


## S16

类别 `data`；来源 `query_db`；调用 `704918602f3c4a9988b44bf680896e56`；状态 `success`。

```sql
SELECT b."Origin / Tier (Domestic/Imported/JV)" AS origin,
       COUNT(CASE WHEN i."Inventory Alert Status" = 'Severe' THEN 1 END) AS severe_cnt,
       COUNT(CASE WHEN i."Inventory Alert Status" = 'Alert' THEN 1 END) AS alert_cnt,
       COUNT(*) AS total_cnt,
       ROUND(100.0 * COUNT(CASE WHEN i."Inventory Alert Status" IN ('Alert', 'Severe') THEN 1 END) / COUNT(*), 1) AS pct_alert
FROM basic_drug_information b
JOIN inventory_management i ON b."Drug ID" = i."Drug ID"
GROUP BY 1
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-019/attempt-01/sql/S16.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-019/attempt-01/sql/S16.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-019/attempt-01/results/S16.rows.jsonl)；完整：True；SHA256：`4a14a02e89fb63e88f4e6368d2842f396c4ed457a3accf6876500d213f7b3f03`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "b", "kind": "base", "block": null, "base_tables": ["basic_drug_information"]}, {"alias": "i", "kind": "base", "block": null, "base_tables": ["inventory_management"]}] | [{"type": "INNER", "right": "inventory_management AS i", "on": "b.\"Drug ID\" = i.\"Drug ID\"", "using": []}] | ["b.\"Origin / Tier (Domestic/Imported/JV)\""] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(CASE WHEN i."Inventory Alert Status" = 'Severe' THEN 1 END) | [] | [{"table": "inventory_management", "column": "Inventory Alert Status"}] | False |
| B1 | COUNT(CASE WHEN i."Inventory Alert Status" = 'Alert' THEN 1 END) | [] | [{"table": "inventory_management", "column": "Inventory Alert Status"}] | False |
| B1 | COUNT(*) | [] | [] | True |
| B1 | COUNT(*) | [] | [] | True |
| B1 | COUNT(CASE WHEN i."Inventory Alert Status" IN ('Alert', 'Severe') THEN 1 END) | [] | [{"table": "inventory_management", "column": "Inventory Alert Status"}] | False |


## S17

类别 `data`；来源 `query_db`；调用 `8c5cf7cd75b141d99df39ad196d367e5`；状态 `success`。

```sql
SELECT b."Origin / Tier (Domestic/Imported/JV)" AS origin,
       ROUND(AVG(i."Near-expiry Quantity"), 1) AS avg_near_expiry,
       ROUND(AVG(i."Expired Quantity"), 1) AS avg_expired,
       ROUND(AVG(i."Damaged Quantity"), 1) AS avg_damaged,
       ROUND(AVG(i."Returned Quantity"), 1) AS avg_returned,
       ROUND(AVG(i."Pest/Mold Damage Quantity"), 1) AS avg_pest_mold,
       ROUND(AVG(i."Rodent Contamination Quantity"), 1) AS avg_rodent,
       ROUND(AVG(i."Air Contamination Quantity"), 1) AS avg_air_contam,
       ROUND(AVG(i."Temp/Humidity Excursion Record"), 1) AS avg_temp_humidity
FROM basic_drug_information b
JOIN inventory_management i ON b."Drug ID" = i."Drug ID"
GROUP BY 1
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-019/attempt-01/sql/S17.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-019/attempt-01/sql/S17.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-019/attempt-01/results/S17.rows.jsonl)；完整：True；SHA256：`9f8e0956fa296335301efd9e3573ba6eb192b83e55731ba15368dfc0df7bd189`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "b", "kind": "base", "block": null, "base_tables": ["basic_drug_information"]}, {"alias": "i", "kind": "base", "block": null, "base_tables": ["inventory_management"]}] | [{"type": "INNER", "right": "inventory_management AS i", "on": "b.\"Drug ID\" = i.\"Drug ID\"", "using": []}] | ["b.\"Origin / Tier (Domestic/Imported/JV)\""] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | AVG(i."Near-expiry Quantity") | [{"table": "inventory_management", "column": "Near-expiry Quantity"}] | [] | False |
| B1 | AVG(i."Expired Quantity") | [{"table": "inventory_management", "column": "Expired Quantity"}] | [] | False |
| B1 | AVG(i."Damaged Quantity") | [{"table": "inventory_management", "column": "Damaged Quantity"}] | [] | False |
| B1 | AVG(i."Returned Quantity") | [{"table": "inventory_management", "column": "Returned Quantity"}] | [] | False |
| B1 | AVG(i."Pest/Mold Damage Quantity") | [{"table": "inventory_management", "column": "Pest/Mold Damage Quantity"}] | [] | False |
| B1 | AVG(i."Rodent Contamination Quantity") | [{"table": "inventory_management", "column": "Rodent Contamination Quantity"}] | [] | False |
| B1 | AVG(i."Air Contamination Quantity") | [{"table": "inventory_management", "column": "Air Contamination Quantity"}] | [] | False |
| B1 | AVG(i."Temp/Humidity Excursion Record") | [{"table": "inventory_management", "column": "Temp/Humidity Excursion Record"}] | [] | False |


## S18

类别 `data`；来源 `query_db`；调用 `a5b096b8c28c483ea612cf147565e13b`；状态 `success`。

```sql
SELECT i."Drug ID", COUNT(*) AS cnt FROM inventory_management i LEFT JOIN basic_drug_information b ON i."Drug ID" = b."Drug ID" WHERE b."Drug ID" IS NULL GROUP BY i."Drug ID"
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-019/attempt-01/sql/S18.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-019/attempt-01/sql/S18.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-019/attempt-01/results/S18.rows.jsonl)；完整：True；SHA256：`3d273e8f6019752c0086b99de346f4f83f7a1252052deee811f0191a43f16ece`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "i", "kind": "base", "block": null, "base_tables": ["inventory_management"]}, {"alias": "b", "kind": "base", "block": null, "base_tables": ["basic_drug_information"]}] | [{"type": "LEFT", "right": "basic_drug_information AS b", "on": "i.\"Drug ID\" = b.\"Drug ID\"", "using": []}] | ["i.\"Drug ID\""] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |


## S19

类别 `data`；来源 `query_db`；调用 `ba98214a4d3c4e14adb1dcb2125a2862`；状态 `success`。

```sql
SELECT i."Drug ID", COUNT(*) AS cnt FROM inventory_management i JOIN basic_drug_information b ON i."Drug ID" = b."Drug ID" GROUP BY i."Drug ID" HAVING COUNT(*) > 1
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-019/attempt-01/sql/S19.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-019/attempt-01/sql/S19.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-019/attempt-01/results/S19.rows.jsonl)；完整：True；SHA256：`e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "i", "kind": "base", "block": null, "base_tables": ["inventory_management"]}, {"alias": "b", "kind": "base", "block": null, "base_tables": ["basic_drug_information"]}] | [{"type": "INNER", "right": "basic_drug_information AS b", "on": "i.\"Drug ID\" = b.\"Drug ID\"", "using": []}] | ["i.\"Drug ID\""] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |
| B1 | COUNT(*) | [] | [] | True |


## S20

类别 `data`；来源 `query_db`；调用 `1c9a5823186047fb90a3621972ac251d`；状态 `success`。

```sql
SELECT MIN("Last Inbound Date") AS min_in, MAX("Last Inbound Date") AS max_in, MIN("Last Outbound Date") AS min_out, MAX("Last Outbound Date") AS max_out FROM inventory_management
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-019/attempt-01/sql/S20.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-019/attempt-01/sql/S20.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-019/attempt-01/results/S20.rows.jsonl)；完整：True；SHA256：`132ce46ef378406bce817fb9956445c7483c2cd76ed65ff857029f7b8f6bd266`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "inventory_management", "kind": "base", "block": null, "base_tables": ["inventory_management"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | MIN("Last Inbound Date") | [{"table": "inventory_management", "column": "Last Inbound Date"}] | [] | False |
| B1 | MAX("Last Inbound Date") | [{"table": "inventory_management", "column": "Last Inbound Date"}] | [] | False |
| B1 | MIN("Last Outbound Date") | [{"table": "inventory_management", "column": "Last Outbound Date"}] | [] | False |
| B1 | MAX("Last Outbound Date") | [{"table": "inventory_management", "column": "Last Outbound Date"}] | [] | False |


## S21

类别 `data`；来源 `query_db`；调用 `90e3e2df3c574d4d8a195698a566cc01`；状态 `success`。

```sql
SELECT "GSP Certification Status" AS gsp, COUNT(*) AS cnt FROM basic_drug_information GROUP BY 1
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-019/attempt-01/sql/S21.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-019/attempt-01/sql/S21.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-019/attempt-01/results/S21.rows.jsonl)；完整：True；SHA256：`85e1513fb15da4878fdf1c96a64b3f5baa7d11b041149e2ec93e079ea9bcfc6e`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "basic_drug_information", "kind": "base", "block": null, "base_tables": ["basic_drug_information"]}] | [] | ["\"GSP Certification Status\""] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |


## S22

类别 `data`；来源 `query_db`；调用 `1f0c941059ea4cf2a3be0b6805572a88`；状态 `success`。

```sql
SELECT "Storage conditions (room temperature/cool/refrigerated)" AS storage, COUNT(*) AS cnt FROM basic_drug_information GROUP BY 1
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-019/attempt-01/sql/S22.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-019/attempt-01/sql/S22.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-019/attempt-01/results/S22.rows.jsonl)；完整：True；SHA256：`8c376242aeb6f69956a676384da8c405c7a407d89615f1cb055f1e88d81c4997`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "basic_drug_information", "kind": "base", "block": null, "base_tables": ["basic_drug_information"]}] | [] | ["\"Storage conditions (room temperature/cool/refrigerated)\""] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |


## S23

类别 `data`；来源 `query_db`；调用 `e4ca305f576f45589035d55c18222720`；状态 `success`。

```sql
SELECT "Transportation mode (land/cold chain)" AS transport, COUNT(*) AS cnt FROM basic_drug_information GROUP BY 1
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-019/attempt-01/sql/S23.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-019/attempt-01/sql/S23.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-019/attempt-01/results/S23.rows.jsonl)；完整：True；SHA256：`b94838a3cea774cc67aab00dd4d33f47eed4eb985ef254e9ced0946d0125dbf3`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "basic_drug_information", "kind": "base", "block": null, "base_tables": ["basic_drug_information"]}] | [] | ["\"Transportation mode (land/cold chain)\""] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |


## S24

类别 `data`；来源 `query_db`；调用 `3812bb0f3b594b26a835683e40337c20`；状态 `success`。

```sql
SELECT 
  b."Origin / Tier (Domestic/Imported/JV)" AS origin,
  ROUND(AVG(1.0*(i."Qualified Quantity" + i."Near-expiry Quantity" + i."Quarantine Quantity") / NULLIF(b."Max Inventory Threshold",0)), 2) AS avg_stock_to_threshold,
  ROUND(MAX(1.0*(i."Qualified Quantity" + i."Near-expiry Quantity" + i."Quarantine Quantity") / NULLIF(b."Max Inventory Threshold",0)), 2) AS max_stock_to_threshold,
  ROUND(AVG(1.0*i."Qualified Quantity" / NULLIF(b."Max Inventory Threshold",0)), 2) AS avg_qualified_to_threshold
FROM basic_drug_information b JOIN inventory_management i ON b."Drug ID" = i."Drug ID"
GROUP BY 1
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-019/attempt-01/sql/S24.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-019/attempt-01/sql/S24.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-019/attempt-01/results/S24.rows.jsonl)；完整：True；SHA256：`766b9fd6b06dacd9a1b67a92cbbb11cee1de8680565331c5f1c77e68beb73dc6`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "b", "kind": "base", "block": null, "base_tables": ["basic_drug_information"]}, {"alias": "i", "kind": "base", "block": null, "base_tables": ["inventory_management"]}] | [{"type": "INNER", "right": "inventory_management AS i", "on": "b.\"Drug ID\" = i.\"Drug ID\"", "using": []}] | ["b.\"Origin / Tier (Domestic/Imported/JV)\""] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | AVG(1.0 * (i."Qualified Quantity" + i."Near-expiry Quantity" + i."Quarantine Quantity") / NULLIF(b."Max Inventory Threshold", 0)) | [{"table": "basic_drug_information", "column": "Max Inventory Threshold"}, {"table": "inventory_management", "column": "Quarantine Quantity"}, {"table": "inventory_management", "column": "Qualified Quantity"}, {"table": "inventory_management", "column": "Near-expiry Quantity"}] | [] | False |
| B1 | MAX(1.0 * (i."Qualified Quantity" + i."Near-expiry Quantity" + i."Quarantine Quantity") / NULLIF(b."Max Inventory Threshold", 0)) | [{"table": "basic_drug_information", "column": "Max Inventory Threshold"}, {"table": "inventory_management", "column": "Quarantine Quantity"}, {"table": "inventory_management", "column": "Qualified Quantity"}, {"table": "inventory_management", "column": "Near-expiry Quantity"}] | [] | False |
| B1 | AVG(1.0 * i."Qualified Quantity" / NULLIF(b."Max Inventory Threshold", 0)) | [{"table": "inventory_management", "column": "Qualified Quantity"}, {"table": "basic_drug_information", "column": "Max Inventory Threshold"}] | [] | False |


## S25

类别 `data`；来源 `query_db`；调用 `8d9c8e730fea4fb1a04b74431cf4f15b`；状态 `success`。

```sql
SELECT 
  b."Origin / Tier (Domestic/Imported/JV)" AS origin,
  COUNT(CASE WHEN julianday('2024-12-31') - julianday(i."Last Outbound Date") > 180 THEN 1 END) AS no_outbound_6m,
  COUNT(CASE WHEN julianday('2024-12-31') - julianday(i."Last Inbound Date") > 180 THEN 1 END) AS no_inbound_6m,
  COUNT(CASE WHEN i."Qualified Quantity" = 0 THEN 1 END) AS zero_qualified,
  COUNT(CASE WHEN i."Quarantine Quantity" > 0 THEN 1 END) AS has_quarantine,
  COUNT(*) AS total
FROM basic_drug_information b JOIN inventory_management i ON b."Drug ID" = i."Drug ID"
GROUP BY 1
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-019/attempt-01/sql/S25.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-019/attempt-01/sql/S25.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-019/attempt-01/results/S25.rows.jsonl)；完整：True；SHA256：`625ddfa2be0ff928bfcbd6061b95bd504b00ed61a5e66ad1e308ee21e8b86653`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "b", "kind": "base", "block": null, "base_tables": ["basic_drug_information"]}, {"alias": "i", "kind": "base", "block": null, "base_tables": ["inventory_management"]}] | [{"type": "INNER", "right": "inventory_management AS i", "on": "b.\"Drug ID\" = i.\"Drug ID\"", "using": []}] | ["b.\"Origin / Tier (Domestic/Imported/JV)\""] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(CASE WHEN JULIANDAY('2024-12-31') - JULIANDAY(i."Last Outbound Date") > 180 THEN 1 END) | [] | [{"table": "inventory_management", "column": "Last Outbound Date"}] | False |
| B1 | COUNT(CASE WHEN JULIANDAY('2024-12-31') - JULIANDAY(i."Last Inbound Date") > 180 THEN 1 END) | [] | [{"table": "inventory_management", "column": "Last Inbound Date"}] | False |
| B1 | COUNT(CASE WHEN i."Qualified Quantity" = 0 THEN 1 END) | [] | [{"table": "inventory_management", "column": "Qualified Quantity"}] | False |
| B1 | COUNT(CASE WHEN i."Quarantine Quantity" > 0 THEN 1 END) | [] | [{"table": "inventory_management", "column": "Quarantine Quantity"}] | False |
| B1 | COUNT(*) | [] | [] | True |


## S26

类别 `data`；来源 `query_db`；调用 `1f115abbdee640319ca93fd4f2109cd2`；状态 `success`。

```sql
SELECT "Inventory Discrepancy Rate", COUNT(*) AS cnt FROM inventory_management GROUP BY 1 ORDER BY cnt DESC LIMIT 15
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-019/attempt-01/sql/S26.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-019/attempt-01/sql/S26.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-019/attempt-01/results/S26.rows.jsonl)；完整：True；SHA256：`4193a3cf1c6368dee94eb793e61c9e735c729672a6dc97cd97db7cd6fbd242e2`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "inventory_management", "kind": "base", "block": null, "base_tables": ["inventory_management"]}] | [] | ["\"Inventory Discrepancy Rate\""] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |


## S27

类别 `data`；来源 `query_db`；调用 `a8baa78dffa1433e977cda5dbc3a66b4`；状态 `success`。

```sql
SELECT "Inventory Discrepancy Rate" FROM inventory_management WHERE "Inventory Discrepancy Rate" LIKE '%0.0%' LIMIT 10
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-019/attempt-01/sql/S27.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-019/attempt-01/sql/S27.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-019/attempt-01/results/S27.rows.jsonl)；完整：True；SHA256：`baf4b4af90dd1f896046418d55a6ba9e1899a4aa61754da6f3a0dde89d028158`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "inventory_management", "kind": "base", "block": null, "base_tables": ["inventory_management"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |


## S28

类别 `data`；来源 `query_db`；调用 `4d7a0719ecbf44759d9675e1013cc664`；状态 `success`。

```sql
SELECT DISTINCT "Inventory Discrepancy Rate" FROM inventory_management ORDER BY 1 LIMIT 10
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-019/attempt-01/sql/S28.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-019/attempt-01/sql/S28.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-019/attempt-01/results/S28.rows.jsonl)；完整：True；SHA256：`d8d21902a98d1e46350ea32cb7ae1cc06287391d807424c5bca8a368796d3c81`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "inventory_management", "kind": "base", "block": null, "base_tables": ["inventory_management"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |


## S29

类别 `data`；来源 `query_db`；调用 `20699d597d6249b5b05ce5c74576a372`；状态 `success`。

```sql
SELECT b."Drug ID", b."Origin / Tier (Domestic/Imported/JV)" AS origin,
       b."Max Inventory Threshold" AS max_threshold,
       b."Expiry Alert Days" AS expiry_alert_days,
       b."GSP Certification Status" AS gsp_status,
       b."Storage conditions (room temperature/cool/refrigerated)" AS storage_condition,
       b."Transportation mode (land/cold chain)" AS transport_mode,
       b."Adverse Reaction Code" AS adr_code,
       b."Contraindication Code" AS ci_code,
       b."Use in Special Populations" AS special_pop,
       i."Inventory Status (Normal/Frozen/Scrapped)" AS inv_status,
       i."Inventory Alert Status" AS alert_status,
       i."Near-expiry Quantity" AS near_expiry,
       i."Quarantine Quantity" AS quarantine,
       i."Qualified Quantity" AS qualified,
       i."Last Inbound Date" AS last_inbound,
       i."Last Outbound Date" AS last_outbound,
       i."Inventory Discrepancy Rate" AS disc_rate,
       i."Near-expiry Quantity.1" AS near_expiry2,
       i."Expired Quantity" AS expired,
       i."Returned Quantity" AS returned,
       i."Damaged Quantity" AS damaged,
       i."Pest/Mold Damage Quantity" AS pest_mold,
       i."Rodent Contamination Quantity" AS rodent,
       i."Air Contamination Quantity" AS air_contam,
       i."Temp/Humidity Excursion Record" AS temp_humidity
FROM basic_drug_information b JOIN inventory_management i ON b."Drug ID" = i."Drug ID"
WHERE b."Origin / Tier (Domestic/Imported/JV)" IN ('Imported', 'Joint-venture')
ORDER BY b."Origin / Tier (Domestic/Imported/JV)", b."Drug ID"
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-019/attempt-01/sql/S29.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-019/attempt-01/sql/S29.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-019/attempt-01/results/S29.rows.jsonl)；完整：True；SHA256：`b5b77a8b7d5956e19a437c606374931e3594f09a530635c4ac1c803d9b12ae8b`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "b", "kind": "base", "block": null, "base_tables": ["basic_drug_information"]}, {"alias": "i", "kind": "base", "block": null, "base_tables": ["inventory_management"]}] | [{"type": "INNER", "right": "inventory_management AS i", "on": "b.\"Drug ID\" = i.\"Drug ID\"", "using": []}] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |


## S30

类别 `data`；来源 `python`；调用 `4938ff73b8d4470896c1f73e00c17718`；状态 `failed`。

```sql
SELECT * FROM dummy LIMIT 1
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-019/attempt-01/sql/S30.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-019/attempt-01/sql/S30.parameters.json)。

错误：`OperationalError('no such table: dummy')`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "dummy", "kind": "base", "block": null, "base_tables": ["dummy"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |


未解析列血缘：[{"block": "B1", "column": "*", "reason": "wildcard_output_names_unresolved"}]

## S31

类别 `data`；来源 `python`；调用 `91e8de61f3d543a78f383c4ce21c119d`；状态 `success`。

```sql
SELECT b."Drug ID" AS drug_id, b."Origin / Tier (Domestic/Imported/JV)" AS origin,
       b."Max Inventory Threshold" AS max_threshold, b."Expiry Alert Days" AS expiry_alert_days,
       b."GSP Certification Status" AS gsp_status,
       b."Storage conditions (room temperature/cool/refrigerated)" AS storage_condition,
       b."Transportation mode (land/cold chain)" AS transport_mode,
       i."Inventory Status (Normal/Frozen/Scrapped)" AS inv_status,
       i."Inventory Alert Status" AS alert_status,
       i."Near-expiry Quantity" AS near_expiry, i."Quarantine Quantity" AS quarantine,
       i."Qualified Quantity" AS qualified, i."Last Inbound Date" AS last_inbound,
       i."Last Outbound Date" AS last_outbound, i."Inventory Discrepancy Rate" AS disc_rate,
       i."Near-expiry Quantity.1" AS near_expiry2, i."Expired Quantity" AS expired,
       i."Returned Quantity" AS returned, i."Damaged Quantity" AS damaged,
       i."Pest/Mold Damage Quantity" AS pest_mold, i."Rodent Contamination Quantity" AS rodent,
       i."Air Contamination Quantity" AS air_contam, i."Temp/Humidity Excursion Record" AS temp_humidity
FROM basic_drug_information b JOIN inventory_management i ON b."Drug ID" = i."Drug ID"
WHERE b."Origin / Tier (Domestic/Imported/JV)" IN ('Imported', 'Joint-venture')
ORDER BY b."Origin / Tier (Domestic/Imported/JV)", b."Drug ID"
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-019/attempt-01/sql/S31.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-019/attempt-01/sql/S31.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-019/attempt-01/results/S31.rows.jsonl)；完整：True；SHA256：`b1b4939fd12b758555a120ffe43cfe239a2864486acc68a85fd95b7f776bad6a`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "b", "kind": "base", "block": null, "base_tables": ["basic_drug_information"]}, {"alias": "i", "kind": "base", "block": null, "base_tables": ["inventory_management"]}] | [{"type": "INNER", "right": "inventory_management AS i", "on": "b.\"Drug ID\" = i.\"Drug ID\"", "using": []}] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |


## S32

类别 `data`；来源 `python`；调用 `8bfb56e4e388427ca6244107d0bcc59a`；状态 `success`。

```sql
SELECT b."Drug ID" AS drug_id, b."Origin / Tier (Domestic/Imported/JV)" AS origin,
       b."Max Inventory Threshold" AS max_threshold, b."Expiry Alert Days" AS expiry_alert_days,
       b."GSP Certification Status" AS gsp_status,
       b."Storage conditions (room temperature/cool/refrigerated)" AS storage_condition,
       b."Transportation mode (land/cold chain)" AS transport_mode,
       i."Inventory Status (Normal/Frozen/Scrapped)" AS inv_status,
       i."Inventory Alert Status" AS alert_status,
       i."Near-expiry Quantity" AS near_expiry, i."Quarantine Quantity" AS quarantine,
       i."Qualified Quantity" AS qualified, i."Last Inbound Date" AS last_inbound,
       i."Last Outbound Date" AS last_outbound, i."Inventory Discrepancy Rate" AS disc_rate,
       i."Near-expiry Quantity.1" AS near_expiry2, i."Expired Quantity" AS expired,
       i."Returned Quantity" AS returned, i."Damaged Quantity" AS damaged,
       i."Pest/Mold Damage Quantity" AS pest_mold, i."Rodent Contamination Quantity" AS rodent,
       i."Air Contamination Quantity" AS air_contam, i."Temp/Humidity Excursion Record" AS temp_humidity
FROM basic_drug_information b JOIN inventory_management i ON b."Drug ID" = i."Drug ID"
WHERE b."Origin / Tier (Domestic/Imported/JV)" IN ('Imported', 'Joint-venture')
ORDER BY b."Origin / Tier (Domestic/Imported/JV)", b."Drug ID"
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-019/attempt-01/sql/S32.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-019/attempt-01/sql/S32.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-019/attempt-01/results/S32.rows.jsonl)；完整：True；SHA256：`b1b4939fd12b758555a120ffe43cfe239a2864486acc68a85fd95b7f776bad6a`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "b", "kind": "base", "block": null, "base_tables": ["basic_drug_information"]}, {"alias": "i", "kind": "base", "block": null, "base_tables": ["inventory_management"]}] | [{"type": "INNER", "right": "inventory_management AS i", "on": "b.\"Drug ID\" = i.\"Drug ID\"", "using": []}] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |


## S33

类别 `data`；来源 `python`；调用 `e7418fce50a3458e939672bb228864c5`；状态 `success`。

```sql
SELECT b."Drug ID" AS drug_id, b."Origin / Tier (Domestic/Imported/JV)" AS origin,
       b."Max Inventory Threshold" AS max_threshold, b."Expiry Alert Days" AS expiry_alert_days,
       b."GSP Certification Status" AS gsp_status,
       b."Storage conditions (room temperature/cool/refrigerated)" AS storage_condition,
       b."Transportation mode (land/cold chain)" AS transport_mode,
       i."Inventory Status (Normal/Frozen/Scrapped)" AS inv_status,
       i."Inventory Alert Status" AS alert_status,
       i."Near-expiry Quantity" AS near_expiry, i."Quarantine Quantity" AS quarantine,
       i."Qualified Quantity" AS qualified, i."Last Inbound Date" AS last_inbound,
       i."Last Outbound Date" AS last_outbound, i."Inventory Discrepancy Rate" AS disc_rate,
       i."Near-expiry Quantity.1" AS near_expiry2, i."Expired Quantity" AS expired,
       i."Returned Quantity" AS returned, i."Damaged Quantity" AS damaged,
       i."Pest/Mold Damage Quantity" AS pest_mold, i."Rodent Contamination Quantity" AS rodent,
       i."Air Contamination Quantity" AS air_contam, i."Temp/Humidity Excursion Record" AS temp_humidity
FROM basic_drug_information b JOIN inventory_management i ON b."Drug ID" = i."Drug ID"
WHERE b."Origin / Tier (Domestic/Imported/JV)" IN ('Imported', 'Joint-venture')
ORDER BY b."Origin / Tier (Domestic/Imported/JV)", b."Drug ID"
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-019/attempt-01/sql/S33.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-019/attempt-01/sql/S33.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-019/attempt-01/results/S33.rows.jsonl)；完整：True；SHA256：`b1b4939fd12b758555a120ffe43cfe239a2864486acc68a85fd95b7f776bad6a`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "b", "kind": "base", "block": null, "base_tables": ["basic_drug_information"]}, {"alias": "i", "kind": "base", "block": null, "base_tables": ["inventory_management"]}] | [{"type": "INNER", "right": "inventory_management AS i", "on": "b.\"Drug ID\" = i.\"Drug ID\"", "using": []}] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |


## S34

类别 `data`；来源 `python`；调用 `61721c74329642088cc66ec21a4a73d3`；状态 `success`。

```sql
SELECT b."Drug ID" AS drug_id, b."Origin / Tier (Domestic/Imported/JV)" AS origin,
       b."Max Inventory Threshold" AS max_threshold, b."Expiry Alert Days" AS expiry_alert_days,
       b."GSP Certification Status" AS gsp_status,
       b."Storage conditions (room temperature/cool/refrigerated)" AS storage_condition,
       b."Transportation mode (land/cold chain)" AS transport_mode,
       i."Inventory Status (Normal/Frozen/Scrapped)" AS inv_status,
       i."Inventory Alert Status" AS alert_status,
       i."Near-expiry Quantity" AS near_expiry, i."Quarantine Quantity" AS quarantine,
       i."Qualified Quantity" AS qualified, i."Last Inbound Date" AS last_inbound,
       i."Last Outbound Date" AS last_outbound, i."Inventory Discrepancy Rate" AS disc_rate,
       i."Near-expiry Quantity.1" AS near_expiry2, i."Expired Quantity" AS expired,
       i."Returned Quantity" AS returned, i."Damaged Quantity" AS damaged,
       i."Pest/Mold Damage Quantity" AS pest_mold, i."Rodent Contamination Quantity" AS rodent,
       i."Air Contamination Quantity" AS air_contam, i."Temp/Humidity Excursion Record" AS temp_humidity
FROM basic_drug_information b JOIN inventory_management i ON b."Drug ID" = i."Drug ID"
WHERE b."Origin / Tier (Domestic/Imported/JV)" IN ('Imported', 'Joint-venture')
ORDER BY b."Origin / Tier (Domestic/Imported/JV)", b."Drug ID"
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-019/attempt-01/sql/S34.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-019/attempt-01/sql/S34.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-019/attempt-01/results/S34.rows.jsonl)；完整：True；SHA256：`b1b4939fd12b758555a120ffe43cfe239a2864486acc68a85fd95b7f776bad6a`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "b", "kind": "base", "block": null, "base_tables": ["basic_drug_information"]}, {"alias": "i", "kind": "base", "block": null, "base_tables": ["inventory_management"]}] | [{"type": "INNER", "right": "inventory_management AS i", "on": "b.\"Drug ID\" = i.\"Drug ID\"", "using": []}] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |


## S35

类别 `data`；来源 `query_db`；调用 `4dd5c69beb80447b86de85188d904b6e`；状态 `success`。

```sql
SELECT b."Origin / Tier (Domestic/Imported/JV)" AS origin,
       ROUND(AVG(i."Qualified Quantity" + i."Near-expiry Quantity" + i."Quarantine Quantity"), 0) AS avg_total_stock,
       ROUND(AVG(1.0*(i."Qualified Quantity" + i."Near-expiry Quantity" + i."Quarantine Quantity") / b."Max Inventory Threshold"), 2) AS avg_stock_ratio,
       ROUND(AVG(i."Near-expiry Quantity"), 0) AS avg_near_expiry,
       ROUND(AVG(i."Expired Quantity"), 0) AS avg_expired,
       ROUND(AVG(CASE WHEN i."Quarantine Quantity" > 0 THEN 1 ELSE 0 END)*100, 1) AS pct_quarantined,
       ROUND(AVG(CASE WHEN i."Qualified Quantity" = 0 THEN 1 ELSE 0 END)*100, 1) AS pct_zero_qualified,
       ROUND(AVG(CASE WHEN i."Inventory Status (Normal/Frozen/Scrapped)" = 'Frozen' THEN 1 ELSE 0 END)*100, 1) AS pct_frozen,
       ROUND(AVG(CASE WHEN i."Inventory Status (Normal/Frozen/Scrapped)" = 'Scrapped' THEN 1 ELSE 0 END)*100, 1) AS pct_scrapped
FROM basic_drug_information b JOIN inventory_management i ON b."Drug ID" = i."Drug ID"
WHERE b."Origin / Tier (Domestic/Imported/JV)" IN ('Imported', 'Joint-venture')
GROUP BY 1
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-019/attempt-01/sql/S35.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-019/attempt-01/sql/S35.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-019/attempt-01/results/S35.rows.jsonl)；完整：True；SHA256：`ced6831b50ce122931cc104ff628a5279cfe8d71897c9abeddeb961c76e0fe6f`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "b", "kind": "base", "block": null, "base_tables": ["basic_drug_information"]}, {"alias": "i", "kind": "base", "block": null, "base_tables": ["inventory_management"]}] | [{"type": "INNER", "right": "inventory_management AS i", "on": "b.\"Drug ID\" = i.\"Drug ID\"", "using": []}] | ["b.\"Origin / Tier (Domestic/Imported/JV)\""] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | AVG(i."Qualified Quantity" + i."Near-expiry Quantity" + i."Quarantine Quantity") | [{"table": "inventory_management", "column": "Quarantine Quantity"}, {"table": "inventory_management", "column": "Qualified Quantity"}, {"table": "inventory_management", "column": "Near-expiry Quantity"}] | [] | False |
| B1 | AVG(1.0 * (i."Qualified Quantity" + i."Near-expiry Quantity" + i."Quarantine Quantity") / b."Max Inventory Threshold") | [{"table": "basic_drug_information", "column": "Max Inventory Threshold"}, {"table": "inventory_management", "column": "Quarantine Quantity"}, {"table": "inventory_management", "column": "Qualified Quantity"}, {"table": "inventory_management", "column": "Near-expiry Quantity"}] | [] | False |
| B1 | AVG(i."Near-expiry Quantity") | [{"table": "inventory_management", "column": "Near-expiry Quantity"}] | [] | False |
| B1 | AVG(i."Expired Quantity") | [{"table": "inventory_management", "column": "Expired Quantity"}] | [] | False |
| B1 | AVG(CASE WHEN i."Quarantine Quantity" > 0 THEN 1 ELSE 0 END) | [] | [{"table": "inventory_management", "column": "Quarantine Quantity"}] | False |
| B1 | AVG(CASE WHEN i."Qualified Quantity" = 0 THEN 1 ELSE 0 END) | [] | [{"table": "inventory_management", "column": "Qualified Quantity"}] | False |
| B1 | AVG(CASE WHEN i."Inventory Status (Normal/Frozen/Scrapped)" = 'Frozen' THEN 1 ELSE 0 END) | [] | [{"table": "inventory_management", "column": "Inventory Status (Normal/Frozen/Scrapped)"}] | False |
| B1 | AVG(CASE WHEN i."Inventory Status (Normal/Frozen/Scrapped)" = 'Scrapped' THEN 1 ELSE 0 END) | [] | [{"table": "inventory_management", "column": "Inventory Status (Normal/Frozen/Scrapped)"}] | False |


## S36

类别 `data`；来源 `query_db`；调用 `db223202207241e0bc3f56a133cdeedf`；状态 `success`。

```sql
SELECT b."Origin / Tier (Domestic/Imported/JV)" AS origin,
       COUNT(CASE WHEN p."Abnormal Price Fluctuation Flag" = 'Yes' THEN 1 END) AS abnormal_price_cnt,
       COUNT(*) AS total
FROM basic_drug_information b JOIN pricing_system p ON b."Drug ID" = p."Drug ID"
WHERE b."Origin / Tier (Domestic/Imported/JV)" IN ('Imported', 'Joint-venture')
GROUP BY 1
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-019/attempt-01/sql/S36.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-019/attempt-01/sql/S36.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-019/attempt-01/results/S36.rows.jsonl)；完整：True；SHA256：`545bc0d7ef450b9118f40f5476800b8072fae07d6e1e5d5a7dad28d897cb69f6`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "b", "kind": "base", "block": null, "base_tables": ["basic_drug_information"]}, {"alias": "p", "kind": "base", "block": null, "base_tables": ["pricing_system"]}] | [{"type": "INNER", "right": "pricing_system AS p", "on": "b.\"Drug ID\" = p.\"Drug ID\"", "using": []}] | ["b.\"Origin / Tier (Domestic/Imported/JV)\""] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(CASE WHEN p."Abnormal Price Fluctuation Flag" = 'Yes' THEN 1 END) | [] | [{"table": "pricing_system", "column": "Abnormal Price Fluctuation Flag"}] | False |
| B1 | COUNT(*) | [] | [] | True |


## S37

类别 `data`；来源 `query_db`；调用 `e7e00e5d615d40fa96d9cd7d5c4f7157`；状态 `success`。

```sql
SELECT b."Origin / Tier (Domestic/Imported/JV)" AS origin,
       COUNT(CASE WHEN b."GSP Certification Status" = 'Not certified' THEN 1 END) AS gsp_not_certified,
       COUNT(CASE WHEN b."Storage conditions (room temperature/cool/refrigerated)" = 'Refrigerated' THEN 1 END) AS refrigerated,
       COUNT(CASE WHEN b."Transportation mode (land/cold chain)" = 'Cold-chain' THEN 1 END) AS cold_chain,
       COUNT(*) AS total
FROM basic_drug_information b
WHERE b."Origin / Tier (Domestic/Imported/JV)" IN ('Imported', 'Joint-venture')
GROUP BY 1
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-019/attempt-01/sql/S37.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-019/attempt-01/sql/S37.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-019/attempt-01/results/S37.rows.jsonl)；完整：True；SHA256：`b774a49490a37f3a23a044839878349409e8a12c438af85d7c123ae245b84326`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "b", "kind": "base", "block": null, "base_tables": ["basic_drug_information"]}] | [] | ["b.\"Origin / Tier (Domestic/Imported/JV)\""] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(CASE WHEN b."GSP Certification Status" = 'Not certified' THEN 1 END) | [] | [{"table": "basic_drug_information", "column": "GSP Certification Status"}] | False |
| B1 | COUNT(CASE WHEN b."Storage conditions (room temperature/cool/refrigerated)" = 'Refrigerated' THEN 1 END) | [] | [{"table": "basic_drug_information", "column": "Storage conditions (room temperature/cool/refrigerated)"}] | False |
| B1 | COUNT(CASE WHEN b."Transportation mode (land/cold chain)" = 'Cold-chain' THEN 1 END) | [] | [{"table": "basic_drug_information", "column": "Transportation mode (land/cold chain)"}] | False |
| B1 | COUNT(*) | [] | [] | True |


## S38

类别 `data`；来源 `query_db`；调用 `219bbecc10384f7a8ab6915adb931672`；状态 `success`。

```sql
SELECT 
  CASE WHEN i."Inventory Status (Normal/Frozen/Scrapped)" IN ('Frozen','Scrapped') AND i."Qualified Quantity" = 0 THEN 'Dual risk (frozen/scrapped + zero qualified)' 
       WHEN i."Inventory Status (Normal/Frozen/Scrapped)" IN ('Frozen','Scrapped') THEN 'Status frozen/scrapped'
       WHEN i."Qualified Quantity" = 0 THEN 'Zero qualified only'
       ELSE 'Normal' END AS risk_category,
  b."Origin / Tier (Domestic/Imported/JV)" AS origin,
  COUNT(*) AS cnt,
  ROUND(AVG(i."Near-expiry Quantity")) AS avg_near_expiry,
  ROUND(AVG(i."Expired Quantity")) AS avg_expired,
  ROUND(AVG(i."Temp/Humidity Excursion Record"), 1) AS avg_temp_humidity
FROM basic_drug_information b JOIN inventory_management i ON b."Drug ID" = i."Drug ID"
WHERE b."Origin / Tier (Domestic/Imported/JV)" IN ('Imported', 'Joint-venture')
GROUP BY 1, 2
ORDER BY 1, 2
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-019/attempt-01/sql/S38.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-019/attempt-01/sql/S38.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-019/attempt-01/results/S38.rows.jsonl)；完整：True；SHA256：`0ba70a9cd4bd00b0792e439c3b0707c24cf3508d31a6319eae9c193828a92412`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "b", "kind": "base", "block": null, "base_tables": ["basic_drug_information"]}, {"alias": "i", "kind": "base", "block": null, "base_tables": ["inventory_management"]}] | [{"type": "INNER", "right": "inventory_management AS i", "on": "b.\"Drug ID\" = i.\"Drug ID\"", "using": []}] | ["CASE WHEN i.\"Inventory Status (Normal/Frozen/Scrapped)\" IN ('Frozen', 'Scrapped') AND i.\"Qualified Quantity\" = 0 THEN 'Dual risk (frozen/scrapped + zero qualified)' WHEN i.\"Inventory Status (Normal/Frozen/Scrapped)\" IN ('Frozen', 'Scrapped') THEN 'Status frozen/scrapped' WHEN i.\"Qualified Quantity\" = 0 THEN 'Zero qualified only' ELSE 'Normal' END", "b.\"Origin / Tier (Domestic/Imported/JV)\""] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |
| B1 | AVG(i."Near-expiry Quantity") | [{"table": "inventory_management", "column": "Near-expiry Quantity"}] | [] | False |
| B1 | AVG(i."Expired Quantity") | [{"table": "inventory_management", "column": "Expired Quantity"}] | [] | False |
| B1 | AVG(i."Temp/Humidity Excursion Record") | [{"table": "inventory_management", "column": "Temp/Humidity Excursion Record"}] | [] | False |


## S39

类别 `data`；来源 `query_db`；调用 `7950fd50dcef4d3985d56b7c204c4ac0`；状态 `success`。

```sql
SELECT 
  b."Origin / Tier (Domestic/Imported/JV)" AS origin,
  COUNT(CASE WHEN i."Inventory Alert Status" = 'Severe' AND i."Inventory Status (Normal/Frozen/Scrapped)" = 'Frozen' THEN 1 END) AS severe_frozen,
  COUNT(CASE WHEN i."Inventory Alert Status" = 'Severe' AND i."Inventory Status (Normal/Frozen/Scrapped)" = 'Scrapped' THEN 1 END) AS severe_scrapped,
  COUNT(CASE WHEN i."Inventory Alert Status" = 'Severe' AND i."Qualified Quantity" = 0 THEN 1 END) AS severe_zero_qualified,
  COUNT(*) AS total
FROM basic_drug_information b JOIN inventory_management i ON b."Drug ID" = i."Drug ID"
WHERE b."Origin / Tier (Domestic/Imported/JV)" IN ('Imported', 'Joint-venture')
GROUP BY 1
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-019/attempt-01/sql/S39.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-019/attempt-01/sql/S39.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-019/attempt-01/results/S39.rows.jsonl)；完整：True；SHA256：`4e68576225587a4814bdc62aa1f9a7cd29a10319097b20f72201e344f2251caf`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "b", "kind": "base", "block": null, "base_tables": ["basic_drug_information"]}, {"alias": "i", "kind": "base", "block": null, "base_tables": ["inventory_management"]}] | [{"type": "INNER", "right": "inventory_management AS i", "on": "b.\"Drug ID\" = i.\"Drug ID\"", "using": []}] | ["b.\"Origin / Tier (Domestic/Imported/JV)\""] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(CASE WHEN i."Inventory Alert Status" = 'Severe' AND i."Inventory Status (Normal/Frozen/Scrapped)" = 'Frozen' THEN 1 END) | [] | [{"table": "inventory_management", "column": "Inventory Alert Status"}, {"table": "inventory_management", "column": "Inventory Status (Normal/Frozen/Scrapped)"}] | False |
| B1 | COUNT(CASE WHEN i."Inventory Alert Status" = 'Severe' AND i."Inventory Status (Normal/Frozen/Scrapped)" = 'Scrapped' THEN 1 END) | [] | [{"table": "inventory_management", "column": "Inventory Alert Status"}, {"table": "inventory_management", "column": "Inventory Status (Normal/Frozen/Scrapped)"}] | False |
| B1 | COUNT(CASE WHEN i."Inventory Alert Status" = 'Severe' AND i."Qualified Quantity" = 0 THEN 1 END) | [] | [{"table": "inventory_management", "column": "Inventory Alert Status"}, {"table": "inventory_management", "column": "Qualified Quantity"}] | False |
| B1 | COUNT(*) | [] | [] | True |


## S40

类别 `data`；来源 `query_db`；调用 `32a5c7a759224821aa8d73e801938650`；状态 `success`。

```sql
SELECT b."Drug ID", b."Origin / Tier (Domestic/Imported/JV)" AS origin,
       b."Manufacturer", b."Registered Trademark",
       b."GSP Certification Status", b."Storage conditions (room temperature/cool/refrigerated)",
       i."Inventory Status (Normal/Frozen/Scrapped)" AS inv_status,
       i."Inventory Alert Status",
       i."Qualified Quantity", i."Near-expiry Quantity", i."Quarantine Quantity",
       (i."Qualified Quantity" + i."Near-expiry Quantity" + i."Quarantine Quantity") AS total_stock,
       i."Expired Quantity", i."Damaged Quantity",
       (i."Pest/Mold Damage Quantity" + i."Rodent Contamination Quantity" + i."Air Contamination Quantity") AS contamination,
       i."Temp/Humidity Excursion Record",
       i."Last Inbound Date", i."Last Outbound Date"
FROM basic_drug_information b JOIN inventory_management i ON b."Drug ID" = i."Drug ID"
WHERE b."Origin / Tier (Domestic/Imported/JV)" IN ('Imported', 'Joint-venture')
  AND i."Inventory Status (Normal/Frozen/Scrapped)" IN ('Frozen', 'Scrapped')
  AND i."Qualified Quantity" = 0
ORDER BY i."Expired Quantity" DESC
LIMIT 20
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-019/attempt-01/sql/S40.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-019/attempt-01/sql/S40.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-019/attempt-01/results/S40.rows.jsonl)；完整：True；SHA256：`789ae0c98949f843697f534ec053af528ea1c91ba562bad3a4fac6566b061bac`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "b", "kind": "base", "block": null, "base_tables": ["basic_drug_information"]}, {"alias": "i", "kind": "base", "block": null, "base_tables": ["inventory_management"]}] | [{"type": "INNER", "right": "inventory_management AS i", "on": "b.\"Drug ID\" = i.\"Drug ID\"", "using": []}] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |


## S41

类别 `data`；来源 `query_db`；调用 `b555e59e3988407c98b8d156ed375694`；状态 `success`。

```sql
SELECT b."Origin / Tier (Domestic/Imported/JV)" AS origin,
       COUNT(*) AS total_drugs,
       ROUND(AVG(i."Expired Quantity" + i."Damaged Quantity" + i."Returned Quantity" + 
                 i."Pest/Mold Damage Quantity" + i."Rodent Contamination Quantity" + 
                 i."Air Contamination Quantity" + i."Temp/Humidity Excursion Record"), 1) AS avg_quality_issues,
       ROUND(AVG(1.0 * (i."Expired Quantity" + i."Damaged Quantity" + i."Returned Quantity" + 
                 i."Pest/Mold Damage Quantity" + i."Rodent Contamination Quantity" + 
                 i."Air Contamination Quantity") / NULLIF(i."Qualified Quantity" + i."Near-expiry Quantity" + i."Quarantine Quantity", 0) * 100), 2) AS quality_issue_rate
FROM basic_drug_information b JOIN inventory_management i ON b."Drug ID" = i."Drug ID"
WHERE b."Origin / Tier (Domestic/Imported/JV)" IN ('Imported', 'Joint-venture')
GROUP BY 1
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-019/attempt-01/sql/S41.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-019/attempt-01/sql/S41.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-019/attempt-01/results/S41.rows.jsonl)；完整：True；SHA256：`ac40c7a5f3508ea2bd12a7f50e9280f94e4f3ccf51f73d5bf4b48de19a8d592e`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "b", "kind": "base", "block": null, "base_tables": ["basic_drug_information"]}, {"alias": "i", "kind": "base", "block": null, "base_tables": ["inventory_management"]}] | [{"type": "INNER", "right": "inventory_management AS i", "on": "b.\"Drug ID\" = i.\"Drug ID\"", "using": []}] | ["b.\"Origin / Tier (Domestic/Imported/JV)\""] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |
| B1 | AVG(i."Expired Quantity" + i."Damaged Quantity" + i."Returned Quantity" + i."Pest/Mold Damage Quantity" + i."Rodent Contamination Quantity" + i."Air Contamination Quantity" + i."Temp/Humidity Excursion Record") | [{"table": "inventory_management", "column": "Temp/Humidity Excursion Record"}, {"table": "inventory_management", "column": "Air Contamination Quantity"}, {"table": "inventory_management", "column": "Rodent Contamination Quantity"}, {"table": "inventory_management", "column": "Pest/Mold Damage Quantity"}, {"table": "inventory_management", "column": "Returned Quantity"}, {"table": "inventory_management", "column": "Expired Quantity"}, {"table": "inventory_management", "column": "Damaged Quantity"}] | [] | False |
| B1 | AVG(1.0 * (i."Expired Quantity" + i."Damaged Quantity" + i."Returned Quantity" + i."Pest/Mold Damage Quantity" + i."Rodent Contamination Quantity" + i."Air Contamination Quantity") / NULLIF(i."Qualified Quantity" + i."Near-expiry Quantity" + i."Quarantine Quantity", 0) * 100) | [{"table": "inventory_management", "column": "Quarantine Quantity"}, {"table": "inventory_management", "column": "Air Contamination Quantity"}, {"table": "inventory_management", "column": "Qualified Quantity"}, {"table": "inventory_management", "column": "Near-expiry Quantity"}, {"table": "inventory_management", "column": "Rodent Contamination Quantity"}, {"table": "inventory_management", "column": "Pest/Mold Damage Quantity"}, {"table": "inventory_management", "column": "Returned Quantity"}, {"table": "inventory_management", "column": "Expired Quantity"}, {"table": "inventory_management", "column": "Damaged Quantity"}] | [] | False |

