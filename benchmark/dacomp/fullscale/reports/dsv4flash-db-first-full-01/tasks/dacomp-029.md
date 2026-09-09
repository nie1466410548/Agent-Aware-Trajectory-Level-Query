# dacomp-029

I am a used car dealer. Based on the data in this table, analyze which models or configura…

运行：已提交。官方未评分。全部 SQL 尝试/成功 52/51；数据 SQL 50/49；Python 8 次。

完整原题：

I am a used car dealer. Based on the data in this table, analyze which models or configurations have higher buyback value, and give me some specific vehicle buyback recommendations.

| 表 | 行数 | 列数 |
| --- | --- | --- |
| autohome | 675 | 25 |


实际路线（分析者依据 SQL/源码概括，不代表 Agent 自述）：检查车型与价格字段 → Python 清洗里程、新车价和日期 → 计算保值率并排除可疑记录 → 按车型/能源/车龄/配置汇总和绘图。

数据库大小：487,424 字节。

## 数据 SQL

| SQL | 状态 | 基础表 | Join 输入/类型 | GROUP BY | 聚合表达式 | 结果行数 | 数据库 ms |
| --- | --- | --- | --- | --- | --- | --- | --- |
| [S3/Q1](#s3) | success | ["autohome"] | 0 / {} | [] | [] | 10 | 0.378 |
| [S4/Q2](#s4) | success | ["autohome"] | 0 / {} | [] | ["COUNT(*)"] | 1 | 0.58 |
| [S5/Q3](#s5) | success | ["autohome"] | 0 / {} | [] | ["MIN(Price)", "MAX(Price)", "AVG(Price)"] | 1 | 0.489 |
| [S6/Q4](#s6) | success | ["autohome"] | 0 / {} | ["\"New Car Price (incl. tax)\""] | ["COUNT(*)"] | 20 | 0.745 |
| [S7/Q5](#s7) | success | ["autohome"] | 0 / {} | ["Title"] | ["COUNT(*)"] | 20 | 0.776 |
| [S8/Q6](#s8) | success | ["autohome"] | 0 / {} | [] | [] | 13 | 0.539 |
| [S9/Q7](#s9) | success | ["autohome"] | 0 / {} | [] | [] | 3 | 0.494 |
| [S10/Q8](#s10) | success | ["autohome"] | 0 / {} | ["STRFTIME('%Y', \"Registration Date\")"] | ["COUNT(*)"] | 7 | 0.859 |
| [S11/Q9](#s11) | success | ["autohome"] | 0 / {} | [] | [] | 209 | 0.683 |
| [S12/Q10](#s12) | success | ["autohome"] | 0 / {} | [] | [] | 30 | 0.282 |
| [S13/Q11](#s13) | success | ["autohome"] | 0 / {} | [] | [] | 6 | 0.504 |
| [S14/Q12](#s14) | success | ["autohome"] | 0 / {} | [] | [] | 3 | 0.643 |
| [S15/Q13](#s15) | success | ["autohome"] | 0 / {} | [] | [] | 82 | 0.603 |
| [S16/Q14](#s16) | success | ["autohome"] | 0 / {} | [] | [] | 82 | 0.61 |
| [S17/Q15](#s17) | success | ["autohome"] | 0 / {} | [] | [] | 15 | 0.5 |
| [S18/Q16](#s18) | success | ["autohome"] | 0 / {} | [] | [] | 20 | 0.631 |
| [S19/Q17](#s19) | success | ["autohome"] | 0 / {} | [] | ["COUNT(*)", "AVG(retention)", "MIN(retention)", "MAX(retention)"] | 1 | 2.926 |
| [S20/Q18](#s20) | success | ["autohome"] | 0 / {} | ["\"Fuel Type\""] | ["COUNT(*)", "AVG(Price)", "AVG(Price * 10000 / CAST(REPLACE(REPLACE(REPLACE(REPLACE(REPLACE(REPLACE(\"New Car Price (incl. tax)\", ',', ''), ' yuan', ''), ' (variant)', ''), ' (no space)', ''), ' (with space)', ''), ' yuan ', '') AS REAL))", "AVG(JULIANDAY(\"Posting Date\") - JULIANDAY(\"Registration Date\"))"] | 3 | 1.76 |
| [S21/Q19](#s21) | success | ["autohome"] | 0 / {} | ["\"Vehicle Class\""] | ["COUNT(*)", "AVG(Price)", "AVG(Price * 10000 / CAST(REPLACE(REPLACE(REPLACE(REPLACE(REPLACE(REPLACE(\"New Car Price (incl. tax)\", ',', ''), ' yuan', ''), ' (variant)', ''), ' (no space)', ''), ' (with space)', ''), ' yuan ', '') AS REAL))", "AVG(JULIANDAY(\"Posting Date\") - JULIANDAY(\"Registration Date\"))"] | 13 | 1.738 |
| [S22/Q20](#s22) | success | ["autohome"] | 0 / {} | ["\"Vehicle Class\""] | ["COUNT(*)", "COUNT(\"Registration Date\")", "AVG(Price * 10000 / CAST(REPLACE(REPLACE(REPLACE(REPLACE(REPLACE(REPLACE(\"New Car Price (incl. tax)\", ',', ''), ' yuan', ''), ' (variant)', ''), ' (no space)', ''), ' (with space)', ''), ' yuan ', '') AS REAL))"] | 13 | 1.829 |
| [S23/Q21](#s23) | success | ["autohome"] | 0 / {} | [] | [] | 20 | 0.392 |
| [S24/Q22](#s24) | success | ["autohome"] | 0 / {} | ["\"Vehicle Class\""] | ["COUNT(*)", "COUNT(\"Registration Date\")", "COUNT(\"Posting Date\")", "AVG(JULIANDAY(\"Posting Date\") - JULIANDAY(\"Registration Date\"))"] | 13 | 0.927 |
| [S25/Q23](#s25) | success | ["autohome"] | 0 / {} | [] | [] | 0 | 0.465 |
| [S26/Q24](#s26) | success | ["autohome"] | 0 / {} | [] | [] | 0 | 0.478 |
| [S27/Q25](#s27) | success | ["autohome"] | 0 / {} | [] | [] | 5 | 0.378 |
| [S28/Q26](#s28) | success | ["autohome"] | 0 / {} | [] | [] | 5 | 0.356 |
| [S29/Q27](#s29) | success | ["autohome"] | 0 / {} | [] | [] | 5 | 0.379 |
| [S30/Q28](#s30) | success | ["autohome"] | 0 / {} | ["Title"] | ["COUNT(*)", "AVG((JULIANDAY(TRIM(\"Posting Date\")) - JULIANDAY(\"Registration Date\")) / 365.25)", "AVG(Price)", "AVG(CASE WHEN Mileage LIKE '%ten thousand km%' THEN CAST(REPLACE(Mileage, ' ten thousand km', '') AS REAL) * 10000 WHEN Mileage LIKE '%km%' THEN CAST(REPLACE(REPLACE(Mileage, ',', ''), ' km', '') AS REAL) END)", "COUNT(*)", "AVG(Price * 10000 / CAST(REPLACE(REPLACE(REPLACE(REPLACE(REPLACE(REPLACE(\"New Car Price (incl. tax)\", ',', ''), ' yuan', ''), ' (variant)', ''), ' (no space)', ''), ' (with space)', ''), ' yuan ', '') AS REAL))"] | 20 | 2.788 |
| [S31/Q29](#s31) | success | ["autohome"] | 0 / {} | ["Title"] | ["COUNT(*)", "AVG((JULIANDAY(TRIM(\"Posting Date\")) - JULIANDAY(\"Registration Date\")) / 365.25)", "COUNT(*)", "AVG(Price * 10000 / CAST(REPLACE(REPLACE(REPLACE(REPLACE(REPLACE(REPLACE(\"New Car Price (incl. tax)\", ',', ''), ' yuan', ''), ' (variant)', ''), ' (no space)', ''), ' (with space)', ''), ' yuan ', '') AS REAL))"] | 20 | 2.355 |
| [S32/Q30](#s32) | failed | unknown | None / None | [] | [] | unknown | 未取得；调用总时长 0.166 ms |
| [S33/Q31](#s33) | success | ["autohome"] | 0 / {} | ["CASE WHEN (JULIANDAY(TRIM(\"Posting Date\")) - JULIANDAY(\"Registration Date\")) / 365.25 < 1 THEN '0-1y' WHEN (JULIANDAY(TRIM(\"Posting Date\")) - JULIANDAY(\"Registration Date\")) / 365.25 < 1.5 THEN '1-1.5y' WHEN (JULIANDAY(TRIM(\"Posting Date\")) - JULIANDAY(\"Registration Date\")) / 365.25 < 2 THEN '1.5-2y' WHEN (JULIANDAY(TRIM(\"Posting Date\")) - JULIANDAY(\"Registration Date\")) / 365.25 < 3 THEN '2-3y' ELSE '3y+' END"] | ["COUNT(*)", "AVG(Price * 10000 / np)"] | 5 | 2.372 |
| [S34/Q32](#s34) | success | ["autohome"] | 0 / {} | ["Transmission"] | ["COUNT(*)", "AVG(Price * 10000 / np)"] | 3 | 1.608 |
| [S35/Q33](#s35) | success | ["autohome"] | 0 / {} | ["Drivetrain"] | ["COUNT(*)", "AVG(Price * 10000 / np)"] | 7 | 1.813 |
| [S36/Q34](#s36) | success | ["autohome"] | 0 / {} | ["Color"] | ["COUNT(*)", "AVG(Price * 10000 / np)"] | 329 | 2.203 |
| [S37/Q35](#s37) | success | ["autohome"] | 0 / {} | ["\"Registration Restrictions\""] | ["COUNT(*)", "AVG(Price * 10000 / np)"] | 6 | 1.534 |
| [S38/Q36](#s38) | success | ["autohome"] | 0 / {} | [] | [] | 3 | 0.689 |
| [S39/Q37](#s39) | success | ["autohome"] | 0 / {} | [] | [] | 7 | 0.79 |
| [S40/Q38](#s40) | success | ["autohome"] | 0 / {} | [] | [] | 3 | 0.732 |
| [S41/Q39](#s41) | success | ["autohome"] | 0 / {} | [] | [] | 675 | 3.377 |
| [S42/Q40](#s42) | success | ["autohome"] | 0 / {} | [] | [] | 675 | 2.842 |
| [S43/Q41](#s43) | success | ["autohome"] | 0 / {} | [] | [] | 675 | 2.842 |
| [S44/Q42](#s44) | success | ["autohome"] | 0 / {} | [] | [] | 675 | 2.943 |
| [S45/Q43](#s45) | success | ["autohome"] | 0 / {} | [] | [] | 4 | 0.732 |
| [S46/Q44](#s46) | success | ["autohome"] | 0 / {} | [] | [] | 6 | 0.603 |
| [S47/Q45](#s47) | success | ["autohome"] | 0 / {} | [] | [] | 675 | 2.158 |
| [S48/Q46](#s48) | success | ["autohome"] | 0 / {} | [] | [] | 675 | 2.999 |
| [S49/Q47](#s49) | success | ["autohome"] | 0 / {} | [] | [] | 675 | 2.951 |
| [S50/Q48](#s50) | success | ["autohome"] | 0 / {} | [] | [] | 675 | 2.807 |
| [S51/Q49](#s51) | success | ["autohome"] | 0 / {} | ["TRIM(\"Transmission\")"] | ["COUNT(*)", "AVG(Price * 10000 / np)"] | 3 | 1.578 |
| [S52/Q50](#s52) | success | ["autohome"] | 0 / {} | ["CASE WHEN \"WLTC Electric Range (km)\" = '/' OR \"WLTC Electric Range (km)\" IS NULL OR \"WLTC Electric Range (km)\" = '' THEN 'unknown' WHEN CAST(\"WLTC Electric Range (km)\" AS REAL) >= 300 THEN '300+ km' WHEN CAST(\"WLTC Electric Range (km)\" AS REAL) >= 200 THEN '200-300 km' WHEN CAST(\"WLTC Electric Range (km)\" AS REAL) >= 100 THEN '100-200 km' ELSE '0-100 km' END"] | ["COUNT(*)", "AVG(Price * 10000 / np)"] | 4 | 1.769 |


## 元数据和设置

| SQL | 类别 | 状态 | 内容 |
| --- | --- | --- | --- |
| S1 | connection_setup | success | PRAGMA query_only=ON |
| S2 | metadata | success | SELECT name,sql FROM sqlite_master WHERE type='table' ORDER BY name |


## Python 与执行位置

人工源码审查：**database_first_violation**。Python parses listing fields, computes age/retention ratios, filters suspect records, and groups model/fuel/class/owner/price-band summaries repeatedly. Flexible malformed-string parsing may benefit from Python, but the subsequent filtering, arithmetic, mean/count and Top-K preparation can reasonably run in SQLite. Plot rendering and dispersion summaries are distinguished from those relational operations. [证据](../reviews/dacomp-029.json)。

P1：Need to pull full parsed dataset into Python for visualization of retention distributions by model, configuration, and to create figures for the report. The analysis requires multiple groupby operations and plotting that is more efficient in Python with pandas/matplotlib.

[源码](../../../runs/dsv4flash-db-first-full-01/dacomp-029/attempt-01/python/P1.py)；[输出](../../../runs/dsv4flash-db-first-full-01/dacomp-029/attempt-01/python/P1.stdout)；[错误](../../../runs/dsv4flash-db-first-full-01/dacomp-029/attempt-01/python/P1.stderr)。检出需人工核验的 SQL 可实现操作：groupby(, .query(, sort_values(；不能仅凭理由判为合规。

P2：Need to pull full parsed dataset into Python for analysis of retention distributions and create visualization figures. Parquet not available, using CSV instead.

[源码](../../../runs/dsv4flash-db-first-full-01/dacomp-029/attempt-01/python/P2.py)；[输出](../../../runs/dsv4flash-db-first-full-01/dacomp-029/attempt-01/python/P2.stdout)；[错误](../../../runs/dsv4flash-db-first-full-01/dacomp-029/attempt-01/python/P2.stderr)。检出需人工核验的 SQL 可实现操作：groupby(, .query(, sort_values(；不能仅凭理由判为合规。

P3：Need to check how many models have n>=3, then create more detailed analysis figures including age-adjusted retention, color analysis, and buyback recommendations.

[源码](../../../runs/dsv4flash-db-first-full-01/dacomp-029/attempt-01/python/P3.py)；[输出](../../../runs/dsv4flash-db-first-full-01/dacomp-029/attempt-01/python/P3.stdout)；[错误](../../../runs/dsv4flash-db-first-full-01/dacomp-029/attempt-01/python/P3.stderr)。检出需人工核验的 SQL 可实现操作：groupby(, .query(, sort_values(；不能仅凭理由判为合规。

P4：Need to analyze luxury/premium models separately and provide specific buyback recommendations. Also creating summary statistics and final visualization.

[源码](../../../runs/dsv4flash-db-first-full-01/dacomp-029/attempt-01/python/P4.py)；[输出](../../../runs/dsv4flash-db-first-full-01/dacomp-029/attempt-01/python/P4.stdout)；[错误](../../../runs/dsv4flash-db-first-full-01/dacomp-029/attempt-01/python/P4.stderr)。检出需人工核验的 SQL 可实现操作：groupby(, .query(, sort_values(；不能仅凭理由判为合规。

P5：Need to quantify data quality issues: rows where Title suggests an expensive model but Price is very low (likely title contamination). This affects the reliability of conclusions, so I'll identify and quantify these rows.

[源码](../../../runs/dsv4flash-db-first-full-01/dacomp-029/attempt-01/python/P5.py)；[输出](../../../runs/dsv4flash-db-first-full-01/dacomp-029/attempt-01/python/P5.stdout)；[错误](../../../runs/dsv4flash-db-first-full-01/dacomp-029/attempt-01/python/P5.stderr)。检出需人工核验的 SQL 可实现操作：.query(；不能仅凭理由判为合规。

P6：Creating final comprehensive visualization with clean data (excluding title-contaminated rows). Will produce three figures for the report: retention heatmap by model, age-adjusted analysis, and buyback recommendation matrix.

[源码](../../../runs/dsv4flash-db-first-full-01/dacomp-029/attempt-01/python/P6.py)；[输出](../../../runs/dsv4flash-db-first-full-01/dacomp-029/attempt-01/python/P6.stdout)；[错误](../../../runs/dsv4flash-db-first-full-01/dacomp-029/attempt-01/python/P6.stderr)。检出需人工核验的 SQL 可实现操作：groupby(, .query(, sort_values(；不能仅凭理由判为合规。

P7：Fixing the owners grouping error - the Number of Previous Owners is text, not numeric. Need to handle properly.

[源码](../../../runs/dsv4flash-db-first-full-01/dacomp-029/attempt-01/python/P7.py)；[输出](../../../runs/dsv4flash-db-first-full-01/dacomp-029/attempt-01/python/P7.stdout)；[错误](../../../runs/dsv4flash-db-first-full-01/dacomp-029/attempt-01/python/P7.stderr)。检出需人工核验的 SQL 可实现操作：groupby(, .query(, sort_values(；不能仅凭理由判为合规。

P8：Regenerating figures with ASCII-only labels since CJK glyphs are missing from the font, causing blank characters in saved figures.

[源码](../../../runs/dsv4flash-db-first-full-01/dacomp-029/attempt-01/python/P8.py)；[输出](../../../runs/dsv4flash-db-first-full-01/dacomp-029/attempt-01/python/P8.stdout)；[错误](../../../runs/dsv4flash-db-first-full-01/dacomp-029/attempt-01/python/P8.stderr)。检出需人工核验的 SQL 可实现操作：groupby(, .query(, sort_values(；不能仅凭理由判为合规。

## 优化机会

已验证候选。筛选限于精确 SQL、相同自包含 CTE、相同单表完整过滤、可分解单表聚合；未覆盖任意 Join 等价和一般谓词蕴含。全部候选都是 offline，未测在线预测。

| 候选 | 类型 | 已有结果 | 覆盖 SQL | 后续次数 | 中间行数 | 验证 | 成本 |
| --- | --- | --- | --- | --- | --- | --- | --- |
| C1 | exact-result reuse | True | ["S41", "S42", "S43", "S44", "S48", "S49", "S50"] | 6 | 675 | verified | Not benchmarked; correctness alone does not establish net speedup. |
| C2 | aggregate MV | False | ["S4", "S5", "S6", "S7"] | 3 | unknown | not_verified_cap | Not tested |
| C3 | common filtered view | False | ["S20", "S21", "S24", "S30", "S31"] | 4 | 675 | verified | Not benchmarked; correctness alone does not establish net speedup. |
| C4 | aggregate MV | False | ["S20", "S21", "S24", "S30", "S31"] | 4 | 647 | verified | Not benchmarked; correctness alone does not establish net speedup. |
| C5 | common filtered view | False | ["S27", "S29"] | 1 | unknown | not_verified_cap | Not tested |


已验证覆盖（含触发查询、候选并集去重）：12/49 条成功数据 SQL。正确性仅针对当前数据库快照；未测性能的候选不能声称已加速。

[完整 build/rewrite 与比较证据](dacomp-029.analysis.json)。

### C1：exact-result reuse

Identical normalized SQL and parameters; archive equality checked.

原查询 [S41](#s41), [S42](#s42), [S43](#s43), [S44](#s44), [S48](#s48), [S49](#s49), [S50](#s50) → 保留前序结果 S41 → 后续 6 次可复用。该构建点为事后假设，不代表 Agent 当时预知后续。

| 原 SQL | 列名一致 | 结果一致 | 比较方法 |
| --- | --- | --- | --- |
| S42 | True | True | exact_multiset |
| S43 | True | True | exact_multiset |
| S44 | True | True | exact_multiset |
| S48 | True | True | exact_multiset |
| S49 | True | True | exact_multiset |
| S50 | True | True | exact_multiset |


验证状态：verified；成本结论：Not benchmarked; correctness alone does not establish net speedup.

### C3：common filtered view

Same single source and complete filter; original filter retained.

原查询 [S20](#s20), [S21](#s21), [S24](#s24), [S30](#s30), [S31](#s31) → 新增共享状态 C3 → 后续 4 次可复用。该构建点为事后假设，不代表 Agent 当时预知后续。

构建定义：

```sql
SELECT * FROM "autohome" WHERE NOT "New Car Price (incl. tax)" IS NULL AND NOT price IS NULL
```

受益查询 S20 的改写示例：

```sql
SELECT "Fuel Type", ROUND(AVG(Price * 10000 / CAST(REPLACE(REPLACE(REPLACE(REPLACE(REPLACE(REPLACE("New Car Price (incl. tax)", ',', ''), ' yuan', ''), ' (variant)', ''), ' (no space)', ''), ' (with space)', ''), ' yuan ', '') AS REAL)) * 100, 2) AS avg_retention_pct, ROUND(AVG(JULIANDAY("Posting Date") - JULIANDAY("Registration Date")) / 365.25, 2) AS avg_age, ROUND(AVG(Price), 2) AS avg_price_wan, COUNT(*) AS cnt FROM temp.reuse_candidate AS autohome WHERE NOT "New Car Price (incl. tax)" IS NULL AND NOT Price IS NULL GROUP BY "Fuel Type" ORDER BY avg_retention_pct DESC
```

| 原 SQL | 列名一致 | 结果一致 | 比较方法 |
| --- | --- | --- | --- |
| S20 | True | True | ordered_numeric_tolerance |
| S21 | True | True | ordered_numeric_tolerance |
| S24 | True | True | ordered_numeric_tolerance |
| S30 | True | True | ordered_numeric_tolerance |
| S31 | True | True | ordered_numeric_tolerance |


验证状态：verified；成本结论：Not benchmarked; correctness alone does not establish net speedup.

### C4：aggregate MV

Union of grouping keys; decomposable aggregate states; AVG uses SUM and non-NULL COUNT.

原查询 [S20](#s20), [S21](#s21), [S24](#s24), [S30](#s30), [S31](#s31) → 新增共享状态 C4 → 后续 4 次可复用。该构建点为事后假设，不代表 Agent 当时预知后续。

构建定义：

```sql
SELECT "Fuel Type" AS __g0, "Vehicle Class" AS __g1, title AS __g2, COUNT(*) AS __a0, SUM(price) AS __a1_sum, COUNT(price) AS __a1_n, SUM(price * 10000 / CAST(REPLACE(REPLACE(REPLACE(REPLACE(REPLACE(REPLACE("New Car Price (incl. tax)", ',', ''), ' yuan', ''), ' (variant)', ''), ' (no space)', ''), ' (with space)', ''), ' yuan ', '') AS REAL)) AS __a2_sum, COUNT(price * 10000 / CAST(REPLACE(REPLACE(REPLACE(REPLACE(REPLACE(REPLACE("New Car Price (incl. tax)", ',', ''), ' yuan', ''), ' (variant)', ''), ' (no space)', ''), ' (with space)', ''), ' yuan ', '') AS REAL)) AS __a2_n, SUM(JULIANDAY("Posting Date") - JULIANDAY("Registration Date")) AS __a3_sum, COUNT(JULIANDAY("Posting Date") - JULIANDAY("Registration Date")) AS __a3_n, COUNT("Registration Date") AS __a4, COUNT("Posting Date") AS __a5, SUM((JULIANDAY(TRIM("Posting Date")) - JULIANDAY("Registration Date")) / 365.25) AS __a6_sum, COUNT((JULIANDAY(TRIM("Posting Date")) - JULIANDAY("Registration Date")) / 365.25) AS __a6_n, SUM(CASE WHEN mileage LIKE '%ten thousand km%' THEN CAST(REPLACE(mileage, ' ten thousand km', '') AS REAL) * 10000 WHEN mileage LIKE '%km%' THEN CAST(REPLACE(REPLACE(mileage, ',', ''), ' km', '') AS REAL) END) AS __a7_sum, COUNT(CASE WHEN mileage LIKE '%ten thousand km%' THEN CAST(REPLACE(mileage, ' ten thousand km', '') AS REAL) * 10000 WHEN mileage LIKE '%km%' THEN CAST(REPLACE(REPLACE(mileage, ',', ''), ' km', '') AS REAL) END) AS __a7_n FROM "autohome" WHERE NOT "New Car Price (incl. tax)" IS NULL AND NOT price IS NULL GROUP BY "Fuel Type", "Vehicle Class", title
```

受益查询 S20 的改写示例：

```sql
SELECT __g0 AS "Fuel Type", ROUND((1.0 * SUM(__a2_sum) / NULLIF(SUM(__a2_n), 0)) * 100, 2) AS avg_retention_pct, ROUND((1.0 * SUM(__a3_sum) / NULLIF(SUM(__a3_n), 0)) / 365.25, 2) AS avg_age, ROUND((1.0 * SUM(__a1_sum) / NULLIF(SUM(__a1_n), 0)), 2) AS avg_price_wan, SUM(__a0) AS cnt FROM temp.reuse_candidate GROUP BY __g0 ORDER BY avg_retention_pct DESC
```

| 原 SQL | 列名一致 | 结果一致 | 比较方法 |
| --- | --- | --- | --- |
| S20 | True | True | ordered_numeric_tolerance |
| S21 | True | True | ordered_numeric_tolerance |
| S24 | True | True | ordered_numeric_tolerance |
| S30 | True | True | ordered_numeric_tolerance |
| S31 | True | True | ordered_numeric_tolerance |


验证状态：verified；成本结论：Not benchmarked; correctness alone does not establish net speedup.

结果依赖：自动记录 SQL→Python 的接口父调用，以及源码中引用归档文件的消费者；字面值相同不认定因果。模型方向选择需要人工读取消息，尚未做全面因果标注。

[原始报告](../../../runs/dsv4flash-db-first-full-01/dacomp-029/attempt-01/answer.md)；[统一消息](../../../runs/dsv4flash-db-first-full-01/dacomp-029/attempt-01/messages.jsonl)；[原始 OpenCode 事件](../../../runs/dsv4flash-db-first-full-01/dacomp-029/attempt-01/opencode.jsonl)；[SQL 引擎日志](../../../runs/dsv4flash-db-first-full-01/dacomp-029/attempt-01/sql_journal.jsonl)。

[可读报告（本地图片链接规范化）](../answers/dacomp-029.md)。原始回答保留，分析结论未改写。

## S1

类别 `connection_setup`；来源 `connection`；调用 `7b040458949b4f6e9e0c41856408256d`；状态 `success`。

```sql
PRAGMA query_only=ON
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-029/attempt-01/sql/S1.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-029/attempt-01/sql/S1.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-029/attempt-01/results/S1.rows.jsonl)；完整：True；SHA256：`e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`。

## S2

类别 `metadata`；来源 `list_db`；调用 `7b040458949b4f6e9e0c41856408256d`；状态 `success`。

```sql
SELECT name,sql FROM sqlite_master WHERE type='table' ORDER BY name
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-029/attempt-01/sql/S2.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-029/attempt-01/sql/S2.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-029/attempt-01/results/S2.rows.jsonl)；完整：True；SHA256：`9eea0905f6c7acef500062444f8f06a42c1444e8bc972b884b644a0d54247fbf`。

## S3

类别 `data`；来源 `query_db`；调用 `3a10e8a53ae44e5893d4c04f98a69a6f`；状态 `success`。

```sql
SELECT * FROM autohome LIMIT 10
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-029/attempt-01/sql/S3.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-029/attempt-01/sql/S3.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-029/attempt-01/results/S3.rows.jsonl)；完整：True；SHA256：`1315d4e75108983c8957d01924f5aeeee94b717d109802d546980a02acce4536`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "autohome", "kind": "base", "block": null, "base_tables": ["autohome"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |


## S4

类别 `data`；来源 `query_db`；调用 `53a29ee911f149129c2ded3c4a10729d`；状态 `success`。

```sql
SELECT COUNT(*) AS total_rows FROM autohome
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-029/attempt-01/sql/S4.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-029/attempt-01/sql/S4.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-029/attempt-01/results/S4.rows.jsonl)；完整：True；SHA256：`e2efe0709c0ad53d3609e10a43a3d9c669d705848f54e9bde5465e635bdb7f85`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "autohome", "kind": "base", "block": null, "base_tables": ["autohome"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |


## S5

类别 `data`；来源 `query_db`；调用 `4a91321ab5d848d88e92cd30f7acdae3`；状态 `success`。

```sql
SELECT MIN(Price) AS min_price, MAX(Price) AS max_price, AVG(Price) AS avg_price FROM autohome
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-029/attempt-01/sql/S5.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-029/attempt-01/sql/S5.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-029/attempt-01/results/S5.rows.jsonl)；完整：True；SHA256：`b6d5c849f0975f8f244255e1ceda629dadf62ae0d637d302147bfcce73eb9684`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "autohome", "kind": "base", "block": null, "base_tables": ["autohome"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | MIN(Price) | [{"table": "autohome", "column": "Price"}] | [] | False |
| B1 | MAX(Price) | [{"table": "autohome", "column": "Price"}] | [] | False |
| B1 | AVG(Price) | [{"table": "autohome", "column": "Price"}] | [] | False |


## S6

类别 `data`；来源 `query_db`；调用 `666e7d851fcc4263a7205524b2aee3ca`；状态 `success`。

```sql
SELECT "New Car Price (incl. tax)" AS np, COUNT(*) AS cnt FROM autohome GROUP BY np ORDER BY cnt DESC LIMIT 20
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-029/attempt-01/sql/S6.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-029/attempt-01/sql/S6.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-029/attempt-01/results/S6.rows.jsonl)；完整：True；SHA256：`9c6b8fa351e2ba08fdedcfa639d9e094da54b3d9ed61947db5c1a5413825be44`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "autohome", "kind": "base", "block": null, "base_tables": ["autohome"]}] | [] | ["\"New Car Price (incl. tax)\""] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |


## S7

类别 `data`；来源 `query_db`；调用 `beab1e39c7494709a92e50cb65bd3d56`；状态 `success`。

```sql
SELECT Title, COUNT(*) AS cnt FROM autohome GROUP BY Title ORDER BY cnt DESC LIMIT 20
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-029/attempt-01/sql/S7.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-029/attempt-01/sql/S7.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-029/attempt-01/results/S7.rows.jsonl)；完整：True；SHA256：`c1d7cf008220f7bb658c992f8dbdbfc99e87c7dd98ca57301860e10463d55b28`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "autohome", "kind": "base", "block": null, "base_tables": ["autohome"]}] | [] | ["Title"] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |


## S8

类别 `data`；来源 `query_db`；调用 `d1c0df0f430f4c5cb5b6c6afe1361deb`；状态 `success`。

```sql
SELECT DISTINCT "Vehicle Class" FROM autohome
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-029/attempt-01/sql/S8.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-029/attempt-01/sql/S8.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-029/attempt-01/results/S8.rows.jsonl)；完整：True；SHA256：`758e296801ab4ba6e6e25aa62955082510ebf356eb4ab77153e2dd805d847c65`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "autohome", "kind": "base", "block": null, "base_tables": ["autohome"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |


## S9

类别 `data`；来源 `query_db`；调用 `15932d4cc83247468e17d876cd4c629e`；状态 `success`。

```sql
SELECT DISTINCT "Fuel Type" FROM autohome
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-029/attempt-01/sql/S9.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-029/attempt-01/sql/S9.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-029/attempt-01/results/S9.rows.jsonl)；完整：True；SHA256：`691c2d61e55bfc7cbb4bf461b158db93953dbda6cfe2750477b178359add0ad0`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "autohome", "kind": "base", "block": null, "base_tables": ["autohome"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |


## S10

类别 `data`；来源 `query_db`；调用 `2283c850e0e4400a8fb759b76e53fc6e`；状态 `success`。

```sql
SELECT "Registration Date", COUNT(*) AS cnt FROM autohome GROUP BY strftime('%Y', "Registration Date") ORDER BY strftime('%Y', "Registration Date")
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-029/attempt-01/sql/S10.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-029/attempt-01/sql/S10.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-029/attempt-01/results/S10.rows.jsonl)；完整：True；SHA256：`6a0ff9f068d4b3d12e2f4facc6e86bfcd53487de208df51b8a6d194109dcb018`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "autohome", "kind": "base", "block": null, "base_tables": ["autohome"]}] | [] | ["STRFTIME('%Y', \"Registration Date\")"] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |


## S11

类别 `data`；来源 `query_db`；调用 `f4f90f4c04124ca4b24e13bf7109ffab`；状态 `success`。

```sql
SELECT DISTINCT "New Car Price (incl. tax)" AS np FROM autohome
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-029/attempt-01/sql/S11.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-029/attempt-01/sql/S11.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-029/attempt-01/results/S11.rows.jsonl)；完整：True；SHA256：`225c9cc4a546d6db52b80855f973d57bde8de38e5cc9f08fab6eeec921da0e18`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "autohome", "kind": "base", "block": null, "base_tables": ["autohome"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |


## S12

类别 `data`；来源 `query_db`；调用 `716bbea5d63844079a6bd267d5769ace`；状态 `success`。

```sql
SELECT DISTINCT Mileage FROM autohome LIMIT 30
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-029/attempt-01/sql/S12.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-029/attempt-01/sql/S12.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-029/attempt-01/results/S12.rows.jsonl)；完整：True；SHA256：`7a93ed916def95a143ca9fae232a5bbd7f16bcd0120e876f22f24b069c8e4a8c`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "autohome", "kind": "base", "block": null, "base_tables": ["autohome"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |


## S13

类别 `data`；来源 `query_db`；调用 `0c3d396ebb904babaf036a6de5e34f20`；状态 `success`。

```sql
SELECT DISTINCT "Number of Previous Owners" FROM autohome
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-029/attempt-01/sql/S13.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-029/attempt-01/sql/S13.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-029/attempt-01/results/S13.rows.jsonl)；完整：True；SHA256：`3df1848ffe6a805473c7d863fcd7d3053dd76d5c85ed27c9b624c8ac1582224b`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "autohome", "kind": "base", "block": null, "base_tables": ["autohome"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |


## S14

类别 `data`；来源 `query_db`；调用 `e8d3444d08534039a89c6f41ca52ee1a`；状态 `success`。

```sql
SELECT DISTINCT strftime('%Y-%m', "Posting Date") AS pd FROM autohome
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-029/attempt-01/sql/S14.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-029/attempt-01/sql/S14.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-029/attempt-01/results/S14.rows.jsonl)；完整：True；SHA256：`5d03f4768e96c10b592fce39c04b7643e7ab004814ad19d8def3e70051cd1f16`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "autohome", "kind": "base", "block": null, "base_tables": ["autohome"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |


## S15

类别 `data`；来源 `query_db`；调用 `81e5be44edd04909bfce3f042ded97eb`；状态 `success`。

```sql
SELECT DISTINCT "New Car Price (incl. tax)" AS np 
FROM autohome 
WHERE "New Car Price (incl. tax)" LIKE '%variant%' 
   OR "New Car Price (incl. tax)" NOT LIKE '%yuan'
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-029/attempt-01/sql/S15.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-029/attempt-01/sql/S15.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-029/attempt-01/results/S15.rows.jsonl)；完整：True；SHA256：`72809c7c0ce73646d22ad30ba975aa302dfce5e3c4da2b49c92df946ddcb9d07`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "autohome", "kind": "base", "block": null, "base_tables": ["autohome"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |


## S16

类别 `data`；来源 `query_db`；调用 `b6d23fcc257b43a991920d363bd6e0ce`；状态 `success`。

```sql
SELECT DISTINCT "New Car Price (incl. tax)" AS np
FROM autohome
WHERE "New Car Price (incl. tax)" NOT LIKE '%yuan'
ORDER BY np
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-029/attempt-01/sql/S16.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-029/attempt-01/sql/S16.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-029/attempt-01/results/S16.rows.jsonl)；完整：True；SHA256：`6ea4e22c89ac76ae71c7526ccc8f0508c2c9fa9eaf905bb39de67e77cc372dcb`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "autohome", "kind": "base", "block": null, "base_tables": ["autohome"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |


## S17

类别 `data`；来源 `query_db`；调用 `25aeb9080edd4963b2ae94899137f1fb`；状态 `success`。

```sql
SELECT 
  "New Car Price (incl. tax)" AS np_raw,
  CAST(REPLACE(REPLACE(REPLACE(REPLACE(REPLACE(REPLACE("New Car Price (incl. tax)", ',', ''), ' yuan', ''), ' (variant)', ''), ' (no space)', ''), ' (with space)', ''), ' yuan ', '') AS REAL) AS np_parsed,
  Mileage,
  CASE WHEN Mileage LIKE '%ten thousand km%' THEN CAST(REPLACE(Mileage, ' ten thousand km','') AS REAL)*10000 
       WHEN Mileage LIKE '%km%' THEN CAST(REPLACE(REPLACE(Mileage, ',',''), ' km','') AS REAL)
       ELSE NULL END AS mileage_km,
  CAST(substr("Number of Previous Owners",1,1) AS INTEGER) AS owners
FROM autohome
LIMIT 15
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-029/attempt-01/sql/S17.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-029/attempt-01/sql/S17.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-029/attempt-01/results/S17.rows.jsonl)；完整：True；SHA256：`ce3b7bf46d81e6a3f5f241309a4cf7d2906038e026ccf153a4fe05d87a2ef81c`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "autohome", "kind": "base", "block": null, "base_tables": ["autohome"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |


## S18

类别 `data`；来源 `query_db`；调用 `b82d4dc55ff14ed08fdbf14de0d181a6`；状态 `success`。

```sql
SELECT 
  Title,
  Price,
  Price*10000 AS price_yuan,
  CAST(REPLACE(REPLACE(REPLACE(REPLACE(REPLACE(REPLACE("New Car Price (incl. tax)", ',', ''), ' yuan', ''), ' (variant)', ''), ' (no space)', ''), ' (with space)', ''), ' yuan ', '') AS REAL) AS np_yuan,
  ROUND(Price*10000 / CAST(REPLACE(REPLACE(REPLACE(REPLACE(REPLACE(REPLACE("New Car Price (incl. tax)", ',', ''), ' yuan', ''), ' (variant)', ''), ' (no space)', ''), ' (with space)', ''), ' yuan ', '') AS REAL) * 100, 2) AS retention_pct,
  (julianday("Posting Date") - julianday("Registration Date"))/365.25 AS age_years,
  CASE WHEN Mileage LIKE '%ten thousand km%' THEN CAST(REPLACE(Mileage, ' ten thousand km','') AS REAL)*10000 
       WHEN Mileage LIKE '%km%' THEN CAST(REPLACE(REPLACE(Mileage, ',',''), ' km','') AS REAL)
       ELSE NULL END AS mileage_km,
  CAST(substr("Number of Previous Owners",1,1) AS INTEGER) AS owners,
  "Fuel Type",
  "Vehicle Class",
  "Engine",
  "Transmission",
  "Drivetrain",
  "Color",
  "Tags",
  "Location"
FROM autohome
LIMIT 20
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-029/attempt-01/sql/S18.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-029/attempt-01/sql/S18.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-029/attempt-01/results/S18.rows.jsonl)；完整：True；SHA256：`d3e028accf5b909934a38b72f95e55e413a3589e95f5b36fcf2741f772210b23`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "autohome", "kind": "base", "block": null, "base_tables": ["autohome"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |


## S19

类别 `data`；来源 `query_db`；调用 `cc0c832ba19f4d13aee3d6d712c573f6`；状态 `success`。

```sql
SELECT 
  ROUND(AVG(retention),2) AS avg_retention,
  ROUND(MIN(retention),2) AS min_retention,
  ROUND(MAX(retention),2) AS max_retention,
  COUNT(*) AS cnt
FROM (
  SELECT 
    Price*10000 / CAST(REPLACE(REPLACE(REPLACE(REPLACE(REPLACE(REPLACE("New Car Price (incl. tax)", ',', ''), ' yuan', ''), ' (variant)', ''), ' (no space)', ''), ' (with space)', ''), ' yuan ', '') AS REAL) AS retention
  FROM autohome
  WHERE "New Car Price (incl. tax)" IS NOT NULL AND Price IS NOT NULL
)
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-029/attempt-01/sql/S19.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-029/attempt-01/sql/S19.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-029/attempt-01/results/S19.rows.jsonl)；完整：True；SHA256：`39ba4bd8c19f80548b2a9ce9b9822f16f2772e64245096a4e308d748f09f94a6`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "autohome", "kind": "base", "block": null, "base_tables": ["autohome"]}] | [] | [] |
| B2 | [{"alias": "", "kind": "derived", "block": "B1", "base_tables": ["autohome"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B2 | COUNT(*) | [] | [] | True |
| B2 | AVG(retention) | [{"table": "autohome", "column": "Price"}, {"table": "autohome", "column": "New Car Price (incl. tax)"}] | [] | False |
| B2 | MIN(retention) | [{"table": "autohome", "column": "Price"}, {"table": "autohome", "column": "New Car Price (incl. tax)"}] | [] | False |
| B2 | MAX(retention) | [{"table": "autohome", "column": "Price"}, {"table": "autohome", "column": "New Car Price (incl. tax)"}] | [] | False |


## S20

类别 `data`；来源 `query_db`；调用 `82dbb307a0e246ef84b47621fa1dede0`；状态 `success`。

```sql
SELECT 
  "Fuel Type",
  ROUND(AVG(Price*10000 / CAST(REPLACE(REPLACE(REPLACE(REPLACE(REPLACE(REPLACE("New Car Price (incl. tax)", ',', ''), ' yuan', ''), ' (variant)', ''), ' (no space)', ''), ' (with space)', ''), ' yuan ', '') AS REAL))*100,2) AS avg_retention_pct,
  ROUND(AVG(julianday("Posting Date") - julianday("Registration Date"))/365.25, 2) AS avg_age,
  ROUND(AVG(Price),2) AS avg_price_wan,
  COUNT(*) AS cnt
FROM autohome
WHERE "New Car Price (incl. tax)" IS NOT NULL AND Price IS NOT NULL
GROUP BY "Fuel Type"
ORDER BY avg_retention_pct DESC
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-029/attempt-01/sql/S20.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-029/attempt-01/sql/S20.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-029/attempt-01/results/S20.rows.jsonl)；完整：True；SHA256：`31d9b390d3129c190311719d0f6fc2d3a3e2b0cf9d796c0c684b0125779d24e8`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "autohome", "kind": "base", "block": null, "base_tables": ["autohome"]}] | [] | ["\"Fuel Type\""] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |
| B1 | AVG(Price) | [{"table": "autohome", "column": "Price"}] | [] | False |
| B1 | AVG(Price * 10000 / CAST(REPLACE(REPLACE(REPLACE(REPLACE(REPLACE(REPLACE("New Car Price (incl. tax)", ',', ''), ' yuan', ''), ' (variant)', ''), ' (no space)', ''), ' (with space)', ''), ' yuan ', '') AS REAL)) | [{"table": "autohome", "column": "Price"}, {"table": "autohome", "column": "New Car Price (incl. tax)"}] | [] | False |
| B1 | AVG(JULIANDAY("Posting Date") - JULIANDAY("Registration Date")) | [{"table": "autohome", "column": "Posting Date"}, {"table": "autohome", "column": "Registration Date"}] | [] | False |


## S21

类别 `data`；来源 `query_db`；调用 `f397809ee63b4d369123a0d3caeb878a`；状态 `success`。

```sql
SELECT 
  "Vehicle Class",
  ROUND(AVG(Price*10000 / CAST(REPLACE(REPLACE(REPLACE(REPLACE(REPLACE(REPLACE("New Car Price (incl. tax)", ',', ''), ' yuan', ''), ' (variant)', ''), ' (no space)', ''), ' (with space)', ''), ' yuan ', '') AS REAL))*100,2) AS avg_retention_pct,
  ROUND(AVG(julianday("Posting Date") - julianday("Registration Date"))/365.25, 2) AS avg_age,
  ROUND(AVG(Price),2) AS avg_price_wan,
  COUNT(*) AS cnt
FROM autohome
WHERE "New Car Price (incl. tax)" IS NOT NULL AND Price IS NOT NULL
GROUP BY "Vehicle Class"
ORDER BY avg_retention_pct DESC
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-029/attempt-01/sql/S21.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-029/attempt-01/sql/S21.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-029/attempt-01/results/S21.rows.jsonl)；完整：True；SHA256：`e20ff3140f29dbe92c1fbd5cf81d7aefc3aefeeca29f8052b5322ddbba64b074`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "autohome", "kind": "base", "block": null, "base_tables": ["autohome"]}] | [] | ["\"Vehicle Class\""] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |
| B1 | AVG(Price) | [{"table": "autohome", "column": "Price"}] | [] | False |
| B1 | AVG(Price * 10000 / CAST(REPLACE(REPLACE(REPLACE(REPLACE(REPLACE(REPLACE("New Car Price (incl. tax)", ',', ''), ' yuan', ''), ' (variant)', ''), ' (no space)', ''), ' (with space)', ''), ' yuan ', '') AS REAL)) | [{"table": "autohome", "column": "Price"}, {"table": "autohome", "column": "New Car Price (incl. tax)"}] | [] | False |
| B1 | AVG(JULIANDAY("Posting Date") - JULIANDAY("Registration Date")) | [{"table": "autohome", "column": "Posting Date"}, {"table": "autohome", "column": "Registration Date"}] | [] | False |


## S22

类别 `data`；来源 `query_db`；调用 `b017fb4d69bd427cbf210cdc79f3285b`；状态 `success`。

```sql
SELECT 
  "Vehicle Class",
  COUNT(*) AS cnt,
  COUNT("Registration Date") AS cnt_reg,
  ROUND(AVG(Price*10000 / CAST(REPLACE(REPLACE(REPLACE(REPLACE(REPLACE(REPLACE("New Car Price (incl. tax)", ',', ''), ' yuan', ''), ' (variant)', ''), ' (no space)', ''), ' (with space)', ''), ' yuan ', '') AS REAL))*100,2) AS avg_retention_pct
FROM autohome
WHERE "New Car Price (incl. tax)" IS NOT NULL AND Price IS NOT NULL
  AND "Registration Date" IS NOT NULL
GROUP BY "Vehicle Class"
ORDER BY avg_retention_pct DESC
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-029/attempt-01/sql/S22.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-029/attempt-01/sql/S22.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-029/attempt-01/results/S22.rows.jsonl)；完整：True；SHA256：`6db231f78084b6d40a9e81c59bd935078cb0b6757b75680adb6e61173076b918`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "autohome", "kind": "base", "block": null, "base_tables": ["autohome"]}] | [] | ["\"Vehicle Class\""] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |
| B1 | COUNT("Registration Date") | [{"table": "autohome", "column": "Registration Date"}] | [] | False |
| B1 | AVG(Price * 10000 / CAST(REPLACE(REPLACE(REPLACE(REPLACE(REPLACE(REPLACE("New Car Price (incl. tax)", ',', ''), ' yuan', ''), ' (variant)', ''), ' (no space)', ''), ' (with space)', ''), ' yuan ', '') AS REAL)) | [{"table": "autohome", "column": "Price"}, {"table": "autohome", "column": "New Car Price (incl. tax)"}] | [] | False |


## S23

类别 `data`；来源 `query_db`；调用 `d5230364a5a14757b3a9fbfce41a4395`；状态 `success`。

```sql
SELECT DISTINCT Title FROM autohome WHERE "Vehicle Class" = 'Microcar' OR "Vehicle Class" = 'Microcar (with space)' OR "Vehicle Class" = 'Mini Car' LIMIT 20
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-029/attempt-01/sql/S23.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-029/attempt-01/sql/S23.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-029/attempt-01/results/S23.rows.jsonl)；完整：True；SHA256：`9a7d72743d275969da49e96c4c4f53f99ab457a620869d647bcd28ab27658153`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "autohome", "kind": "base", "block": null, "base_tables": ["autohome"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |


## S24

类别 `data`；来源 `query_db`；调用 `98dea29343cd40328bb27dca5f7ed4cc`；状态 `success`。

```sql
SELECT 
  "Vehicle Class",
  COUNT(*) AS cnt,
  COUNT("Registration Date") AS cnt_reg,
  COUNT("Posting Date") AS cnt_post,
  ROUND(AVG(julianday("Posting Date") - julianday("Registration Date"))/365.25, 2) AS avg_age
FROM autohome
WHERE "New Car Price (incl. tax)" IS NOT NULL AND Price IS NOT NULL
GROUP BY "Vehicle Class"
ORDER BY avg_age DESC
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-029/attempt-01/sql/S24.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-029/attempt-01/sql/S24.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-029/attempt-01/results/S24.rows.jsonl)；完整：True；SHA256：`7a2df6b1ead5ad9706ca1dbbd587720753a1c6171ba208903626c5f9a7679021`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "autohome", "kind": "base", "block": null, "base_tables": ["autohome"]}] | [] | ["\"Vehicle Class\""] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |
| B1 | COUNT("Registration Date") | [{"table": "autohome", "column": "Registration Date"}] | [] | False |
| B1 | COUNT("Posting Date") | [{"table": "autohome", "column": "Posting Date"}] | [] | False |
| B1 | AVG(JULIANDAY("Posting Date") - JULIANDAY("Registration Date")) | [{"table": "autohome", "column": "Posting Date"}, {"table": "autohome", "column": "Registration Date"}] | [] | False |


## S25

类别 `data`；来源 `query_db`；调用 `0aa9182d059a4532986c9f98cadc8803`；状态 `success`。

```sql
SELECT "Registration Date", "Posting Date", "Inspection Expiry", Title FROM autohome WHERE "Vehicle Class" = 'Microcar' AND "Posting Date" IS NULL LIMIT 5
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-029/attempt-01/sql/S25.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-029/attempt-01/sql/S25.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-029/attempt-01/results/S25.rows.jsonl)；完整：True；SHA256：`e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "autohome", "kind": "base", "block": null, "base_tables": ["autohome"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |


## S26

类别 `data`；来源 `query_db`；调用 `917c4f2d09bd4a26b83ea66f4b71413c`；状态 `success`。

```sql
SELECT "Registration Date", "Posting Date", "Inspection Expiry", Title FROM autohome WHERE "Vehicle Class" = 'Microcar (with space)' AND "Posting Date" IS NULL LIMIT 5
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-029/attempt-01/sql/S26.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-029/attempt-01/sql/S26.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-029/attempt-01/results/S26.rows.jsonl)；完整：True；SHA256：`e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "autohome", "kind": "base", "block": null, "base_tables": ["autohome"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |


## S27

类别 `data`；来源 `query_db`；调用 `51caa6dab4d841ac9920c5ca5c626c81`；状态 `success`。

```sql
SELECT "Registration Date", "Posting Date", "Inspection Expiry", Title, Price, "New Car Price (incl. tax)" FROM autohome WHERE "Vehicle Class" = 'Microcar' LIMIT 5
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-029/attempt-01/sql/S27.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-029/attempt-01/sql/S27.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-029/attempt-01/results/S27.rows.jsonl)；完整：True；SHA256：`6c67ac8877d033b0687d030c8fca8b89e5eb464cfd90170df9a3bf1d0a093091`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "autohome", "kind": "base", "block": null, "base_tables": ["autohome"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |


## S28

类别 `data`；来源 `query_db`；调用 `6fbeb89d31f74071848ec4a380a88701`；状态 `success`。

```sql
SELECT "Posting Date", typeof("Posting Date"), length("Posting Date") FROM autohome WHERE "Vehicle Class" = 'Microcar (with space)' LIMIT 5
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-029/attempt-01/sql/S28.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-029/attempt-01/sql/S28.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-029/attempt-01/results/S28.rows.jsonl)；完整：True；SHA256：`b4c6355d9e7e30ce19fd195e7afe3a7d135ccaaf82f3b8448997db676083b0fa`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "autohome", "kind": "base", "block": null, "base_tables": ["autohome"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |


## S29

类别 `data`；来源 `query_db`；调用 `88db049e79ba4c46b0cdd1ceafb80431`；状态 `success`。

```sql
SELECT "Posting Date", typeof("Posting Date"), length("Posting Date") FROM autohome WHERE "Vehicle Class" = 'Microcar' LIMIT 5
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-029/attempt-01/sql/S29.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-029/attempt-01/sql/S29.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-029/attempt-01/results/S29.rows.jsonl)；完整：True；SHA256：`9c0050e17aeed2208df23da4e9ed522586c4101bd455fcae48afae58db4f8a7e`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "autohome", "kind": "base", "block": null, "base_tables": ["autohome"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |


## S30

类别 `data`；来源 `query_db`；调用 `e5de0409ded546adb2ebef3057cf263b`；状态 `success`。

```sql
SELECT 
  Title,
  COUNT(*) AS cnt,
  ROUND(AVG(Price*10000 / CAST(REPLACE(REPLACE(REPLACE(REPLACE(REPLACE(REPLACE("New Car Price (incl. tax)", ',', ''), ' yuan', ''), ' (variant)', ''), ' (no space)', ''), ' (with space)', ''), ' yuan ', '') AS REAL))*100, 2) AS avg_retention_pct,
  ROUND(AVG((julianday(TRIM("Posting Date")) - julianday("Registration Date"))/365.25), 2) AS avg_age,
  ROUND(AVG(Price), 2) AS avg_price_wan,
  ROUND(AVG(CASE WHEN Mileage LIKE '%ten thousand km%' THEN CAST(REPLACE(Mileage, ' ten thousand km','') AS REAL)*10000 
       WHEN Mileage LIKE '%km%' THEN CAST(REPLACE(REPLACE(Mileage, ',',''), ' km','') AS REAL) END), 0) AS avg_mileage_km
FROM autohome
WHERE "New Car Price (incl. tax)" IS NOT NULL AND Price IS NOT NULL
GROUP BY Title
HAVING COUNT(*) >= 3
ORDER BY avg_retention_pct DESC
LIMIT 25
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-029/attempt-01/sql/S30.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-029/attempt-01/sql/S30.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-029/attempt-01/results/S30.rows.jsonl)；完整：True；SHA256：`ca64a61d98b6e151ea40161f681d1ebaf5fc80ebd31d9a103fcfb25eeb0fa04c`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "autohome", "kind": "base", "block": null, "base_tables": ["autohome"]}] | [] | ["Title"] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |
| B1 | AVG((JULIANDAY(TRIM("Posting Date")) - JULIANDAY("Registration Date")) / 365.25) | [{"table": "autohome", "column": "Registration Date"}, {"table": "autohome", "column": "Posting Date"}] | [] | False |
| B1 | AVG(Price) | [{"table": "autohome", "column": "Price"}] | [] | False |
| B1 | AVG(CASE WHEN Mileage LIKE '%ten thousand km%' THEN CAST(REPLACE(Mileage, ' ten thousand km', '') AS REAL) * 10000 WHEN Mileage LIKE '%km%' THEN CAST(REPLACE(REPLACE(Mileage, ',', ''), ' km', '') AS REAL) END) | [{"table": "autohome", "column": "Mileage"}, {"table": "autohome", "column": "Mileage"}] | [{"table": "autohome", "column": "Mileage"}, {"table": "autohome", "column": "Mileage"}] | False |
| B1 | COUNT(*) | [] | [] | True |
| B1 | AVG(Price * 10000 / CAST(REPLACE(REPLACE(REPLACE(REPLACE(REPLACE(REPLACE("New Car Price (incl. tax)", ',', ''), ' yuan', ''), ' (variant)', ''), ' (no space)', ''), ' (with space)', ''), ' yuan ', '') AS REAL)) | [{"table": "autohome", "column": "Price"}, {"table": "autohome", "column": "New Car Price (incl. tax)"}] | [] | False |


## S31

类别 `data`；来源 `query_db`；调用 `204fb51b12fb495fb8d1cff291489dcf`；状态 `success`。

```sql
SELECT 
  Title,
  COUNT(*) AS cnt,
  ROUND(AVG(Price*10000 / CAST(REPLACE(REPLACE(REPLACE(REPLACE(REPLACE(REPLACE("New Car Price (incl. tax)", ',', ''), ' yuan', ''), ' (variant)', ''), ' (no space)', ''), ' (with space)', ''), ' yuan ', '') AS REAL))*100, 2) AS avg_retention_pct,
  ROUND(AVG((julianday(TRIM("Posting Date")) - julianday("Registration Date"))/365.25), 2) AS avg_age
FROM autohome
WHERE "New Car Price (incl. tax)" IS NOT NULL AND Price IS NOT NULL
GROUP BY Title
HAVING COUNT(*) >= 3
ORDER BY avg_retention_pct ASC
LIMIT 25
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-029/attempt-01/sql/S31.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-029/attempt-01/sql/S31.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-029/attempt-01/results/S31.rows.jsonl)；完整：True；SHA256：`89a7642a7126ce2c2c903f460621a7ac46360b006a475db37251685435eec048`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "autohome", "kind": "base", "block": null, "base_tables": ["autohome"]}] | [] | ["Title"] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |
| B1 | AVG((JULIANDAY(TRIM("Posting Date")) - JULIANDAY("Registration Date")) / 365.25) | [{"table": "autohome", "column": "Registration Date"}, {"table": "autohome", "column": "Posting Date"}] | [] | False |
| B1 | COUNT(*) | [] | [] | True |
| B1 | AVG(Price * 10000 / CAST(REPLACE(REPLACE(REPLACE(REPLACE(REPLACE(REPLACE("New Car Price (incl. tax)", ',', ''), ' yuan', ''), ' (variant)', ''), ' (no space)', ''), ' (with space)', ''), ' yuan ', '') AS REAL)) | [{"table": "autohome", "column": "Price"}, {"table": "autohome", "column": "New Car Price (incl. tax)"}] | [] | False |


## S32

类别 `data`；来源 `query_db`；调用 `fcd4a32addeb4ccb812d9b32811cf333`；状态 `failed`。

```sql
SELECT 
  CASE 
    WHEN (julianday(TRIM("Posting Date")) - julianday("Registration Date"))/365.25 < 1 THEN '0-1y'
    WHEN (julianday(TRIM("Posting Date")) - julianday("Registration Date"))/365.25 < 1.5 THEN '1-1.5y'
    WHEN (julianday(TRIM("Posting Date")) - julianday("Registration Date"))/365.25 < 2 THEN '1.5-2y'
    WHEN (julianday(TRIM("Posting Date")) - julianday("Registration Date"))/365.25 < 3 THEN '2-3y'
    ELSE '3y+' END AS age_bucket,
  ROUND(AVG(Price*10000 / CAST(REPLACE(REPLACE(REPLACE(REPLACE(REPLACE(REPLACE("New Car Price (incl. tax)", ',', ''), ' yuan', ''), ' (variant)', ''), ' (no space)', ''), ' (with space)', ''), ' yuan ', '') AS REAL))*100, 2) AS avg_retention_pct,
  ROUND(AVG(Price*10000 / CAST(REPLACE(REPLACE(REPLACE(REPLACE(REPLACE(REPLACE("New Car Price (incl. tax)", ',', ''), ' yuan', ''), ' (variant)', ''), ' (no space)', ''), ' (with space)', ''), ' yuan ', '') AS REAL) / ((julianday(TRIM("Posting Date")) - julianday("Registration Date"))/365.25), 2) AS retention_per_year,
  COUNT(*) AS cnt
FROM autohome
WHERE "New Car Price (incl. tax)" IS NOT NULL AND Price IS NOT NULL
  AND "Registration Date" IS NOT NULL AND "Posting Date" IS NOT NULL
GROUP BY age_bucket
ORDER BY age_bucket
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-029/attempt-01/sql/S32.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-029/attempt-01/sql/S32.parameters.json)。

错误：`OperationalError('near "AS": syntax error')`。

## S33

类别 `data`；来源 `query_db`；调用 `7e87cd1223c74803b791ab45a25e0a1d`；状态 `success`。

```sql
SELECT 
  CASE 
    WHEN (julianday(TRIM("Posting Date")) - julianday("Registration Date"))/365.25 < 1 THEN '0-1y'
    WHEN (julianday(TRIM("Posting Date")) - julianday("Registration Date"))/365.25 < 1.5 THEN '1-1.5y'
    WHEN (julianday(TRIM("Posting Date")) - julianday("Registration Date"))/365.25 < 2 THEN '1.5-2y'
    WHEN (julianday(TRIM("Posting Date")) - julianday("Registration Date"))/365.25 < 3 THEN '2-3y'
    ELSE '3y+' END AS age_bucket,
  ROUND(AVG(Price*10000 / np), 2) AS avg_retention_pct,
  COUNT(*) AS cnt
FROM (
  SELECT *, 
    CAST(REPLACE(REPLACE(REPLACE(REPLACE(REPLACE(REPLACE("New Car Price (incl. tax)", ',', ''), ' yuan', ''), ' (variant)', ''), ' (no space)', ''), ' (with space)', ''), ' yuan ', '') AS REAL) AS np
  FROM autohome
  WHERE "New Car Price (incl. tax)" IS NOT NULL AND Price IS NOT NULL
    AND "Registration Date" IS NOT NULL AND "Posting Date" IS NOT NULL
)
GROUP BY age_bucket
ORDER BY age_bucket
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-029/attempt-01/sql/S33.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-029/attempt-01/sql/S33.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-029/attempt-01/results/S33.rows.jsonl)；完整：True；SHA256：`3c7138c92f2265c9671f60bbc3da92e1c76d36a9b53a783d2148e0135a1cc0f1`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "autohome", "kind": "base", "block": null, "base_tables": ["autohome"]}] | [] | [] |
| B2 | [{"alias": "", "kind": "derived", "block": "B1", "base_tables": ["autohome"]}] | [] | ["CASE WHEN (JULIANDAY(TRIM(\"Posting Date\")) - JULIANDAY(\"Registration Date\")) / 365.25 < 1 THEN '0-1y' WHEN (JULIANDAY(TRIM(\"Posting Date\")) - JULIANDAY(\"Registration Date\")) / 365.25 < 1.5 THEN '1-1.5y' WHEN (JULIANDAY(TRIM(\"Posting Date\")) - JULIANDAY(\"Registration Date\")) / 365.25 < 2 THEN '1.5-2y' WHEN (JULIANDAY(TRIM(\"Posting Date\")) - JULIANDAY(\"Registration Date\")) / 365.25 < 3 THEN '2-3y' ELSE '3y+' END"] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B2 | COUNT(*) | [] | [] | True |
| B2 | AVG(Price * 10000 / np) | [{"table": "autohome", "column": "New Car Price (incl. tax)"}, {"table": "autohome", "column": "Price"}] | [] | False |


## S34

类别 `data`；来源 `query_db`；调用 `98dc9a22cf0643209ad59b6280df48d8`；状态 `success`。

```sql
SELECT 
  Transmission,
  ROUND(AVG(Price*10000 / np)*100, 2) AS avg_retention_pct,
  COUNT(*) AS cnt
FROM (
  SELECT *, CAST(REPLACE(REPLACE(REPLACE(REPLACE(REPLACE(REPLACE("New Car Price (incl. tax)", ',', ''), ' yuan', ''), ' (variant)', ''), ' (no space)', ''), ' (with space)', ''), ' yuan ', '') AS REAL) AS np
  FROM autohome WHERE "New Car Price (incl. tax)" IS NOT NULL AND Price IS NOT NULL
)
GROUP BY Transmission
ORDER BY avg_retention_pct DESC
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-029/attempt-01/sql/S34.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-029/attempt-01/sql/S34.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-029/attempt-01/results/S34.rows.jsonl)；完整：True；SHA256：`80dafef4fe7568bbe4ebbfb8e3220f44bfa63e272ef09e5e44beb56a0c9c5938`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "autohome", "kind": "base", "block": null, "base_tables": ["autohome"]}] | [] | [] |
| B2 | [{"alias": "", "kind": "derived", "block": "B1", "base_tables": ["autohome"]}] | [] | ["Transmission"] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B2 | COUNT(*) | [] | [] | True |
| B2 | AVG(Price * 10000 / np) | [{"table": "autohome", "column": "New Car Price (incl. tax)"}, {"table": "autohome", "column": "Price"}] | [] | False |


## S35

类别 `data`；来源 `query_db`；调用 `d59930b924804967b8732703c232a4a6`；状态 `success`。

```sql
SELECT 
  Drivetrain,
  ROUND(AVG(Price*10000 / np)*100, 2) AS avg_retention_pct,
  COUNT(*) AS cnt
FROM (
  SELECT *, CAST(REPLACE(REPLACE(REPLACE(REPLACE(REPLACE(REPLACE("New Car Price (incl. tax)", ',', ''), ' yuan', ''), ' (variant)', ''), ' (no space)', ''), ' (with space)', ''), ' yuan ', '') AS REAL) AS np
  FROM autohome WHERE "New Car Price (incl. tax)" IS NOT NULL AND Price IS NOT NULL
)
GROUP BY Drivetrain
ORDER BY avg_retention_pct DESC
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-029/attempt-01/sql/S35.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-029/attempt-01/sql/S35.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-029/attempt-01/results/S35.rows.jsonl)；完整：True；SHA256：`00a7cbc3ff312d76a50c03ea69442d7a89a8fb8a1ef34e64c8c32e8a67904798`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "autohome", "kind": "base", "block": null, "base_tables": ["autohome"]}] | [] | [] |
| B2 | [{"alias": "", "kind": "derived", "block": "B1", "base_tables": ["autohome"]}] | [] | ["Drivetrain"] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B2 | COUNT(*) | [] | [] | True |
| B2 | AVG(Price * 10000 / np) | [{"table": "autohome", "column": "New Car Price (incl. tax)"}, {"table": "autohome", "column": "Price"}] | [] | False |


## S36

类别 `data`；来源 `query_db`；调用 `1c8fad77a973424abaaf98c54b4e808f`；状态 `success`。

```sql
SELECT 
  Color,
  ROUND(AVG(Price*10000 / np)*100, 2) AS avg_retention_pct,
  COUNT(*) AS cnt
FROM (
  SELECT *, CAST(REPLACE(REPLACE(REPLACE(REPLACE(REPLACE(REPLACE("New Car Price (incl. tax)", ',', ''), ' yuan', ''), ' (variant)', ''), ' (no space)', ''), ' (with space)', ''), ' yuan ', '') AS REAL) AS np
  FROM autohome WHERE "New Car Price (incl. tax)" IS NOT NULL AND Price IS NOT NULL
)
GROUP BY Color
ORDER BY avg_retention_pct DESC
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-029/attempt-01/sql/S36.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-029/attempt-01/sql/S36.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-029/attempt-01/results/S36.rows.jsonl)；完整：True；SHA256：`7a84f79c98bf308c0f847390a964ba1fcb3ac451fe62b6effa6c53980734fd66`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "autohome", "kind": "base", "block": null, "base_tables": ["autohome"]}] | [] | [] |
| B2 | [{"alias": "", "kind": "derived", "block": "B1", "base_tables": ["autohome"]}] | [] | ["Color"] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B2 | COUNT(*) | [] | [] | True |
| B2 | AVG(Price * 10000 / np) | [{"table": "autohome", "column": "New Car Price (incl. tax)"}, {"table": "autohome", "column": "Price"}] | [] | False |


## S37

类别 `data`；来源 `query_db`；调用 `1ffbd17a2bbe4a19ac8995757a75253c`；状态 `success`。

```sql
SELECT 
  "Registration Restrictions",
  ROUND(AVG(Price*10000 / np)*100, 2) AS avg_retention_pct,
  COUNT(*) AS cnt
FROM (
  SELECT *, CAST(REPLACE(REPLACE(REPLACE(REPLACE(REPLACE(REPLACE("New Car Price (incl. tax)", ',', ''), ' yuan', ''), ' (variant)', ''), ' (no space)', ''), ' (with space)', ''), ' yuan ', '') AS REAL) AS np
  FROM autohome WHERE "New Car Price (incl. tax)" IS NOT NULL AND Price IS NOT NULL
)
GROUP BY "Registration Restrictions"
ORDER BY avg_retention_pct DESC
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-029/attempt-01/sql/S37.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-029/attempt-01/sql/S37.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-029/attempt-01/results/S37.rows.jsonl)；完整：True；SHA256：`c6f1e80eb4833414c1d1cf6bf99d9900a689e804167b86f91f1335ef3a883c36`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "autohome", "kind": "base", "block": null, "base_tables": ["autohome"]}] | [] | [] |
| B2 | [{"alias": "", "kind": "derived", "block": "B1", "base_tables": ["autohome"]}] | [] | ["\"Registration Restrictions\""] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B2 | COUNT(*) | [] | [] | True |
| B2 | AVG(Price * 10000 / np) | [{"table": "autohome", "column": "New Car Price (incl. tax)"}, {"table": "autohome", "column": "Price"}] | [] | False |


## S38

类别 `data`；来源 `query_db`；调用 `f57040fead51466787fca72ce8780879`；状态 `success`。

```sql
SELECT DISTINCT '"' || Transmission || '"' AS t FROM autohome ORDER BY t
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-029/attempt-01/sql/S38.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-029/attempt-01/sql/S38.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-029/attempt-01/results/S38.rows.jsonl)；完整：True；SHA256：`d5ac75ca23910e0e129f05e44db9b378dee2a75e59be435bdd2c6a75d689138e`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "autohome", "kind": "base", "block": null, "base_tables": ["autohome"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |


## S39

类别 `data`；来源 `query_db`；调用 `0d13d52216b1433bb513f6a571c5667e`；状态 `success`。

```sql
SELECT DISTINCT '"' || Drivetrain || '"' AS d FROM autohome ORDER BY d
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-029/attempt-01/sql/S39.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-029/attempt-01/sql/S39.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-029/attempt-01/results/S39.rows.jsonl)；完整：True；SHA256：`372eaef3f949e529e9ed7564183febcbca578fe4b436a2b584fd636d18641317`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "autohome", "kind": "base", "block": null, "base_tables": ["autohome"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |


## S40

类别 `data`；来源 `query_db`；调用 `0dc4361915d4455092b77dae0bddf765`；状态 `success`。

```sql
SELECT DISTINCT '"' || "Fuel Type" || '"' AS f FROM autohome ORDER BY f
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-029/attempt-01/sql/S40.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-029/attempt-01/sql/S40.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-029/attempt-01/results/S40.rows.jsonl)；完整：True；SHA256：`531b103e7bc49a73807b87cb042115a093c5520f431cf6e70fa506df51e8ae6a`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "autohome", "kind": "base", "block": null, "base_tables": ["autohome"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |


## S41

类别 `data`；来源 `python`；调用 `19b206cabe2e4faf9040d3ed352f891f`；状态 `success`。

```sql

  SELECT 
    Title, Price, "New Car Price (incl. tax)" as np_raw, "Fuel Type", "Vehicle Class",
    "Transmission", "Drivetrain", "Color", "Mileage", "Registration Date",
    "Posting Date", "Number of Previous Owners", "Registration Restrictions",
    "Engine", "Tags", "Location"
  FROM autohome

```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-029/attempt-01/sql/S41.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-029/attempt-01/sql/S41.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-029/attempt-01/results/S41.rows.jsonl)；完整：True；SHA256：`fb75047090bcd6cc58fb68522cccc67581523722105ad873c31230bf4d847ef1`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "autohome", "kind": "base", "block": null, "base_tables": ["autohome"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |


## S42

类别 `data`；来源 `python`；调用 `83ad184c5f5c47a6a37e1719b9fae838`；状态 `success`。

```sql

  SELECT 
    Title, Price, "New Car Price (incl. tax)" as np_raw, "Fuel Type", "Vehicle Class",
    "Transmission", "Drivetrain", "Color", "Mileage", "Registration Date",
    "Posting Date", "Number of Previous Owners", "Registration Restrictions",
    "Engine", "Tags", "Location"
  FROM autohome

```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-029/attempt-01/sql/S42.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-029/attempt-01/sql/S42.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-029/attempt-01/results/S42.rows.jsonl)；完整：True；SHA256：`fb75047090bcd6cc58fb68522cccc67581523722105ad873c31230bf4d847ef1`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "autohome", "kind": "base", "block": null, "base_tables": ["autohome"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |


## S43

类别 `data`；来源 `python`；调用 `17a83b8d4b7a4d7fb6e9f2fc47997bb9`；状态 `success`。

```sql

  SELECT 
    Title, Price, "New Car Price (incl. tax)" as np_raw, "Fuel Type", "Vehicle Class",
    "Transmission", "Drivetrain", "Color", "Mileage", "Registration Date",
    "Posting Date", "Number of Previous Owners", "Registration Restrictions",
    "Engine", "Tags", "Location"
  FROM autohome

```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-029/attempt-01/sql/S43.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-029/attempt-01/sql/S43.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-029/attempt-01/results/S43.rows.jsonl)；完整：True；SHA256：`fb75047090bcd6cc58fb68522cccc67581523722105ad873c31230bf4d847ef1`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "autohome", "kind": "base", "block": null, "base_tables": ["autohome"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |


## S44

类别 `data`；来源 `python`；调用 `fa2b90d5530a41c887ea0c2343e1bfdc`；状态 `success`。

```sql

  SELECT 
    Title, Price, "New Car Price (incl. tax)" as np_raw, "Fuel Type", "Vehicle Class",
    "Transmission", "Drivetrain", "Color", "Mileage", "Registration Date",
    "Posting Date", "Number of Previous Owners", "Registration Restrictions",
    "Engine", "Tags", "Location"
  FROM autohome

```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-029/attempt-01/sql/S44.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-029/attempt-01/sql/S44.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-029/attempt-01/results/S44.rows.jsonl)；完整：True；SHA256：`fb75047090bcd6cc58fb68522cccc67581523722105ad873c31230bf4d847ef1`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "autohome", "kind": "base", "block": null, "base_tables": ["autohome"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |


## S45

类别 `data`；来源 `query_db`；调用 `4aabc254877148828179aad56adacc9a`；状态 `success`。

```sql
SELECT Title, Price, "New Car Price (incl. tax)", "Vehicle Class", "Registration Date", "Posting Date" FROM autohome WHERE Title LIKE '%Zeekr 009%' OR Title LIKE '%Li Xiang L9%' OR Title LIKE '%Gaohe HiPhi Z%' OR Title LIKE '%Xpeng G9%'
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-029/attempt-01/sql/S45.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-029/attempt-01/sql/S45.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-029/attempt-01/results/S45.rows.jsonl)；完整：True；SHA256：`d0d56d4f6fe4cd39bc698ed573888e09851ff59a61eaedfd9c97f5871fd649a2`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "autohome", "kind": "base", "block": null, "base_tables": ["autohome"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |


## S46

类别 `data`；来源 `query_db`；调用 `c9654e75b5854868b9b4faa86bd49012`；状态 `success`。

```sql
SELECT Title, Price, "New Car Price (incl. tax)", "Vehicle Class" FROM autohome WHERE Title LIKE '%Cadillac LYRIQ%' OR Title LIKE '%Mercedes%' OR Title LIKE '%Model Y%'
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-029/attempt-01/sql/S46.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-029/attempt-01/sql/S46.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-029/attempt-01/results/S46.rows.jsonl)；完整：True；SHA256：`fceacd2ed2b11dff27f1a8a36f5661199a9588ec213261c3259eb4ddf9f3a101`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "autohome", "kind": "base", "block": null, "base_tables": ["autohome"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |


## S47

类别 `data`；来源 `python`；调用 `dde4ca1da09147b8a1796cd2768e0fe4`；状态 `success`。

```sql

  SELECT 
    Title, Price, "New Car Price (incl. tax)" as np_raw, "Fuel Type", "Vehicle Class",
    "Mileage", "Registration Date", "Posting Date", "Number of Previous Owners"
  FROM autohome

```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-029/attempt-01/sql/S47.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-029/attempt-01/sql/S47.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-029/attempt-01/results/S47.rows.jsonl)；完整：True；SHA256：`28d2e8cb0ccea7c3cbc86de9a69ff5ea20a686524a68ccc5e0f18e2cfe9e8ee8`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "autohome", "kind": "base", "block": null, "base_tables": ["autohome"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |


## S48

类别 `data`；来源 `python`；调用 `e30027942efa4eac8de40fa250949bd8`；状态 `success`。

```sql

  SELECT 
    Title, Price, "New Car Price (incl. tax)" as np_raw, "Fuel Type", "Vehicle Class",
    "Transmission", "Drivetrain", "Color", "Mileage", "Registration Date",
    "Posting Date", "Number of Previous Owners", "Registration Restrictions",
    "Engine", "Tags", "Location"
  FROM autohome

```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-029/attempt-01/sql/S48.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-029/attempt-01/sql/S48.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-029/attempt-01/results/S48.rows.jsonl)；完整：True；SHA256：`fb75047090bcd6cc58fb68522cccc67581523722105ad873c31230bf4d847ef1`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "autohome", "kind": "base", "block": null, "base_tables": ["autohome"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |


## S49

类别 `data`；来源 `python`；调用 `bf296be3561542dab4ce190c992ace72`；状态 `success`。

```sql

  SELECT 
    Title, Price, "New Car Price (incl. tax)" as np_raw, "Fuel Type", "Vehicle Class",
    "Transmission", "Drivetrain", "Color", "Mileage", "Registration Date",
    "Posting Date", "Number of Previous Owners", "Registration Restrictions",
    "Engine", "Tags", "Location"
  FROM autohome

```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-029/attempt-01/sql/S49.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-029/attempt-01/sql/S49.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-029/attempt-01/results/S49.rows.jsonl)；完整：True；SHA256：`fb75047090bcd6cc58fb68522cccc67581523722105ad873c31230bf4d847ef1`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "autohome", "kind": "base", "block": null, "base_tables": ["autohome"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |


## S50

类别 `data`；来源 `python`；调用 `f7c80dfeadf444fdb5cbd98fd9997a0a`；状态 `success`。

```sql

  SELECT 
    Title, Price, "New Car Price (incl. tax)" as np_raw, "Fuel Type", "Vehicle Class",
    "Transmission", "Drivetrain", "Color", "Mileage", "Registration Date",
    "Posting Date", "Number of Previous Owners", "Registration Restrictions",
    "Engine", "Tags", "Location"
  FROM autohome

```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-029/attempt-01/sql/S50.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-029/attempt-01/sql/S50.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-029/attempt-01/results/S50.rows.jsonl)；完整：True；SHA256：`fb75047090bcd6cc58fb68522cccc67581523722105ad873c31230bf4d847ef1`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "autohome", "kind": "base", "block": null, "base_tables": ["autohome"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |


## S51

类别 `data`；来源 `query_db`；调用 `cc3a63a6b29e4dfd897ad447bf877098`；状态 `success`。

```sql
SELECT 
  TRIM("Transmission") AS trans,
  COUNT(*) AS cnt,
  ROUND(AVG(Price*10000 / np)*100, 2) AS avg_retention_pct
FROM (
  SELECT *, CAST(REPLACE(REPLACE(REPLACE(REPLACE(REPLACE(REPLACE("New Car Price (incl. tax)", ',', ''), ' yuan', ''), ' (variant)', ''), ' (no space)', ''), ' (with space)', ''), ' yuan ', '') AS REAL) AS np
  FROM autohome WHERE "New Car Price (incl. tax)" IS NOT NULL AND Price IS NOT NULL
)
GROUP BY trans
ORDER BY avg_retention_pct DESC
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-029/attempt-01/sql/S51.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-029/attempt-01/sql/S51.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-029/attempt-01/results/S51.rows.jsonl)；完整：True；SHA256：`4003df9632cf0b705177e6e1a9378fb3379d2ed3595d16ea1ebd10530f4bc844`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "autohome", "kind": "base", "block": null, "base_tables": ["autohome"]}] | [] | [] |
| B2 | [{"alias": "", "kind": "derived", "block": "B1", "base_tables": ["autohome"]}] | [] | ["TRIM(\"Transmission\")"] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B2 | COUNT(*) | [] | [] | True |
| B2 | AVG(Price * 10000 / np) | [{"table": "autohome", "column": "New Car Price (incl. tax)"}, {"table": "autohome", "column": "Price"}] | [] | False |


## S52

类别 `data`；来源 `query_db`；调用 `a27826f69bea4546ab600852371f9920`；状态 `success`。

```sql
SELECT 
  CASE 
    WHEN "WLTC Electric Range (km)" = '/' OR "WLTC Electric Range (km)" IS NULL OR "WLTC Electric Range (km)" = '' THEN 'unknown'
    WHEN CAST("WLTC Electric Range (km)" AS REAL) >= 300 THEN '300+ km'
    WHEN CAST("WLTC Electric Range (km)" AS REAL) >= 200 THEN '200-300 km'
    WHEN CAST("WLTC Electric Range (km)" AS REAL) >= 100 THEN '100-200 km'
    ELSE '0-100 km' END AS range_bucket,
  COUNT(*) AS cnt,
  ROUND(AVG(Price*10000 / np)*100, 2) AS avg_retention_pct
FROM (
  SELECT *, CAST(REPLACE(REPLACE(REPLACE(REPLACE(REPLACE(REPLACE("New Car Price (incl. tax)", ',', ''), ' yuan', ''), ' (variant)', ''), ' (no space)', ''), ' (with space)', ''), ' yuan ', '') AS REAL) AS np
  FROM autohome WHERE "New Car Price (incl. tax)" IS NOT NULL AND Price IS NOT NULL
)
GROUP BY range_bucket
ORDER BY avg_retention_pct DESC
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-029/attempt-01/sql/S52.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-029/attempt-01/sql/S52.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-029/attempt-01/results/S52.rows.jsonl)；完整：True；SHA256：`59e1b44a1609c52bb28a4c617063a79f87b74411d74a0a04f51747456c0e69b2`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "autohome", "kind": "base", "block": null, "base_tables": ["autohome"]}] | [] | [] |
| B2 | [{"alias": "", "kind": "derived", "block": "B1", "base_tables": ["autohome"]}] | [] | ["CASE WHEN \"WLTC Electric Range (km)\" = '/' OR \"WLTC Electric Range (km)\" IS NULL OR \"WLTC Electric Range (km)\" = '' THEN 'unknown' WHEN CAST(\"WLTC Electric Range (km)\" AS REAL) >= 300 THEN '300+ km' WHEN CAST(\"WLTC Electric Range (km)\" AS REAL) >= 200 THEN '200-300 km' WHEN CAST(\"WLTC Electric Range (km)\" AS REAL) >= 100 THEN '100-200 km' ELSE '0-100 km' END"] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B2 | COUNT(*) | [] | [] | True |
| B2 | AVG(Price * 10000 / np) | [{"table": "autohome", "column": "New Car Price (incl. tax)"}, {"table": "autohome", "column": "Price"}] | [] | False |

