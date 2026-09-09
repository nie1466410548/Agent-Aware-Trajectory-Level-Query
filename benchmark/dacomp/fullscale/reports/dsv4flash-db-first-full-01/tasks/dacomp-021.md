# dacomp-021

Across the full year 2024, do ride bookings exhibit "peaks and troughs" (specific times of…

运行：已提交。官方未评分。全部 SQL 尝试/成功 33/31；数据 SQL 31/29；Python 4 次。

完整原题：

Across the full year 2024, do ride bookings exhibit "peaks and troughs" (specific times of day or specific dates with higher booking volumes)? Analyze those periods across dimensions such as cancellation rate and per-kilometer ride cost, and provide operational recommendations for the Uber platform.

| 表 | 行数 | 列数 |
| --- | --- | --- |
| sheet1 | 150000 | 21 |


实际路线（分析者依据 SQL/源码概括，不代表 Agent 自述）：按小时、日期和星期分析预订量 → 比较取消率与每公里费用 → Python 检验高低峰关联并汇总月份 → 绘制时段热图和趋势。

数据库大小：46,215,168 字节。

## 数据 SQL

| SQL | 状态 | 基础表 | Join 输入/类型 | GROUP BY | 聚合表达式 | 结果行数 | 数据库 ms |
| --- | --- | --- | --- | --- | --- | --- | --- |
| [S3/Q1](#s3) | success | ["sheet1"] | 0 / {} | [] | ["COUNT(*)", "COUNT(DISTINCT \"Booking ID\")", "MIN(\"Date\")", "MAX(\"Date\")", "COUNT(DISTINCT \"Date\")"] | 1 | 229.679 |
| [S4/Q2](#s4) | success | ["sheet1"] | 0 / {} | ["\"Booking Status\""] | ["COUNT(*)"] | 5 | 66.546 |
| [S5/Q3](#s5) | success | ["sheet1"] | 0 / {} | [] | [] | 10 | 0.379 |
| [S6/Q4](#s6) | success | ["sheet1"] | 0 / {} | ["SUBSTRING(\"Date\", 1, 4)"] | ["COUNT(*)"] | 1 | 62.477 |
| [S7/Q5](#s7) | success | ["sheet1"] | 0 / {} | ["\"Date\""] | ["COUNT(*)"] | 20 | 77.38 |
| [S8/Q6](#s8) | success | ["sheet1"] | 0 / {} | [] | ["MIN(LENGTH(\"Time\"))", "MAX(LENGTH(\"Time\"))"] | 1 | 20.399 |
| [S9/Q7](#s9) | success | ["sheet1"] | 0 / {} | ["\"Date\""] | [] | 30 | 80.249 |
| [S10/Q8](#s10) | success | ["sheet1"] | 0 / {} | ["\"Time\""] | [] | 20 | 95.981 |
| [S11/Q9](#s11) | failed | ["sheet1"] | 0 / {} | ["date_key"] | ["COUNT(*)"] | unknown | 未取得；调用总时长 0.191 ms |
| [S12/Q10](#s12) | failed | ["sheet1"] | 0 / {} | ["hour"] | ["COUNT(*)"] | unknown | 未取得；调用总时长 0.184 ms |
| [S13/Q11](#s13) | success | ["sheet1"] | 0 / {} | ["date_key"] | ["COUNT(*)"] | 15 | 277.327 |
| [S14/Q12](#s14) | success | ["sheet1"] | 0 / {} | ["hour"] | ["COUNT(*)"] | 24 | 80.55 |
| [S15/Q13](#s15) | success | ["sheet1"] | 0 / {} | [] | ["MIN(date_key)", "MAX(date_key)", "COUNT(DISTINCT date_key)"] | 1 | 632.527 |
| [S16/Q14](#s16) | success | ["sheet1"] | 0 / {} | ["hour"] | ["COUNT(*)"] | 24 | 79.961 |
| [S17/Q15](#s17) | success | ["sheet1"] | 0 / {} | ["CASE CAST(STRFTIME('%w', date_key) AS INTEGER) WHEN 0 THEN 'Sunday' WHEN 1 THEN 'Monday' WHEN 2 THEN 'Tuesday' WHEN 3 THEN 'Wednesday' WHEN 4 THEN 'Thursday' WHEN 5 THEN 'Friday' WHEN 6 THEN 'Saturday' END"] | ["COUNT(*)", "SUM(CASE WHEN status IN ('Cancelled by Customer', 'Cancelled by Driver') THEN 1 ELSE 0 END)", "SUM(CASE WHEN status = 'No Driver Found' THEN 1 ELSE 0 END)", "SUM(CASE WHEN status = 'Incomplete' THEN 1 ELSE 0 END)", "SUM(CASE WHEN status = 'Completed' THEN 1 ELSE 0 END)", "AVG(CASE WHEN status = 'Completed' AND dist > 0 THEN value / dist END)", "COUNT(*)", "SUM(CASE WHEN status IN ('Cancelled by Customer', 'Cancelled by Driver') THEN 1 ELSE 0 END)"] | 7 | 371.761 |
| [S18/Q16](#s18) | success | ["sheet1"] | 0 / {} | ["CAST(STRFTIME('%m', date_key) AS INTEGER)"] | ["COUNT(*)", "SUM(CASE WHEN status IN ('Cancelled by Customer', 'Cancelled by Driver') THEN 1 ELSE 0 END)", "AVG(CASE WHEN status = 'Completed' AND dist > 0 THEN value / dist END)", "COUNT(*)", "SUM(CASE WHEN status IN ('Cancelled by Customer', 'Cancelled by Driver') THEN 1 ELSE 0 END)"] | 12 | 336.677 |
| [S19/Q17](#s19) | success | ["sheet1"] | 0 / {} | ["hour"] | ["COUNT(*)", "SUM(CASE WHEN status IN ('Cancelled by Customer', 'Cancelled by Driver') THEN 1 ELSE 0 END)", "SUM(CASE WHEN status = 'No Driver Found' THEN 1 ELSE 0 END)", "SUM(CASE WHEN status = 'Incomplete' THEN 1 ELSE 0 END)", "SUM(CASE WHEN status = 'Completed' THEN 1 ELSE 0 END)", "AVG(CASE WHEN status = 'Completed' AND dist > 0 THEN value / dist END)", "AVG(CASE WHEN status = 'Completed' THEN dist END)", "COUNT(*)", "COUNT(*)", "SUM(CASE WHEN status IN ('Cancelled by Customer', 'Cancelled by Driver') THEN 1 ELSE 0 END)", "SUM(CASE WHEN status = 'No Driver Found' THEN 1 ELSE 0 END)"] | 24 | 163.003 |
| [S20/Q18](#s20) | success | ["sheet1"] | 0 / {} | ["hour"] | ["COUNT(*)", "SUM(CASE WHEN status IN ('Cancelled by Customer', 'Cancelled by Driver') THEN 1 ELSE 0 END)", "SUM(CASE WHEN status = 'No Driver Found' THEN 1 ELSE 0 END)", "SUM(CASE WHEN status = 'Incomplete' THEN 1 ELSE 0 END)", "SUM(CASE WHEN status = 'Completed' THEN 1 ELSE 0 END)", "AVG(CASE WHEN status = 'Completed' AND dist > 0 THEN value / dist END)", "AVG(CASE WHEN status = 'Completed' THEN dist END)", "COUNT(*)", "COUNT(*)", "SUM(CASE WHEN status IN ('Cancelled by Customer', 'Cancelled by Driver') THEN 1 ELSE 0 END)", "SUM(CASE WHEN status = 'No Driver Found' THEN 1 ELSE 0 END)"] | 24 | 160.306 |
| [S21/Q19](#s21) | success | ["sheet1"] | 0 / {} | ["hour"] | ["COUNT(*)", "SUM(CASE WHEN status IN ('Cancelled by Customer', 'Cancelled by Driver') THEN 1 ELSE 0 END)", "SUM(CASE WHEN status = 'No Driver Found' THEN 1 ELSE 0 END)", "SUM(CASE WHEN status = 'Incomplete' THEN 1 ELSE 0 END)", "SUM(CASE WHEN status = 'Completed' THEN 1 ELSE 0 END)", "AVG(CASE WHEN status = 'Completed' AND dist > 0 THEN value / dist END)", "AVG(CASE WHEN status = 'Completed' THEN dist END)", "COUNT(*)", "COUNT(*)", "SUM(CASE WHEN status IN ('Cancelled by Customer', 'Cancelled by Driver') THEN 1 ELSE 0 END)", "SUM(CASE WHEN status = 'No Driver Found' THEN 1 ELSE 0 END)"] | 24 | 162.456 |
| [S22/Q20](#s22) | success | ["sheet1"] | 0 / {} | ["date_key"] | ["COUNT(*)"] | 15 | 275.671 |
| [S23/Q21](#s23) | success | ["sheet1"] | 0 / {} | ["date_key"] | ["COUNT(*)", "SUM(CASE WHEN status IN ('Cancelled by Customer', 'Cancelled by Driver') THEN 1 ELSE 0 END)", "SUM(CASE WHEN status = 'No Driver Found' THEN 1 ELSE 0 END)", "SUM(CASE WHEN status = 'Incomplete' THEN 1 ELSE 0 END)", "SUM(CASE WHEN status = 'Completed' THEN 1 ELSE 0 END)", "AVG(CASE WHEN status = 'Completed' AND dist > 0 THEN value / dist END)"] | 365 | 342.162 |
| [S24/Q22](#s24) | success | ["sheet1"] | 0 / {} | ["hour"] | ["COUNT(*)", "SUM(CASE WHEN status IN ('Cancelled by Customer', 'Cancelled by Driver') THEN 1 ELSE 0 END)", "SUM(CASE WHEN status = 'No Driver Found' THEN 1 ELSE 0 END)", "SUM(CASE WHEN status = 'Incomplete' THEN 1 ELSE 0 END)", "SUM(CASE WHEN status = 'Completed' THEN 1 ELSE 0 END)", "AVG(CASE WHEN status = 'Completed' AND dist > 0 THEN value / dist END)"] | 24 | 151.981 |
| [S25/Q23](#s25) | success | ["sheet1"] | 0 / {} | ["dow"] | ["COUNT(*)", "AVG(dist)", "AVG(value)", "AVG(value / NULLIF(dist, 0))", "COUNT(*)", "COUNT(*)"] | 7 | 215.732 |
| [S26/Q24](#s26) | success | ["sheet1"] | 0 / {} | ["dow", "vtype"] | ["COUNT(*)", "AVG(dist)", "AVG(value / NULLIF(dist, 0))"] | 49 | 250.227 |
| [S27/Q25](#s27) | success | ["sheet1"] | 0 / {} | ["CASE WHEN hour BETWEEN 0 AND 4 THEN 'Late-night trough (0-4)' WHEN hour BETWEEN 5 AND 8 THEN 'Early morning (5-8)' WHEN hour BETWEEN 9 AND 11 THEN 'Morning peak (9-11)' WHEN hour BETWEEN 12 AND 14 THEN 'Midday dip (12-14)' WHEN hour BETWEEN 15 AND 16 THEN 'Late afternoon (15-16)' WHEN hour BETWEEN 17 AND 20 THEN 'Evening peak (17-20)' ELSE 'Late evening (21-23)' END"] | ["COUNT(*)", "AVG(CASE WHEN status = 'Completed' AND dist > 0 THEN value / dist END)", "MIN(hour)", "COUNT(*)", "COUNT(*)", "COUNT(*)", "COUNT(*)", "COUNT(*)", "SUM(CASE WHEN status IN ('Cancelled by Customer', 'Cancelled by Driver') THEN 1 ELSE 0 END)", "SUM(CASE WHEN status = 'Cancelled by Customer' THEN 1 ELSE 0 END)", "SUM(CASE WHEN status = 'Cancelled by Driver' THEN 1 ELSE 0 END)", "SUM(CASE WHEN status = 'No Driver Found' THEN 1 ELSE 0 END)", "SUM(CASE WHEN status = 'Incomplete' THEN 1 ELSE 0 END)"] | 7 | 266.289 |
| [S28/Q26](#s28) | success | ["sheet1"] | 0 / {} | ["\"Reason for cancelling by Customer\""] | ["COUNT(*)"] | 5 | 18.695 |
| [S29/Q27](#s29) | success | ["sheet1"] | 0 / {} | ["\"Driver Cancellation Reason\""] | ["COUNT(*)"] | 4 | 23.516 |
| [S30/Q28](#s30) | success | ["sheet1"] | 0 / {} | ["dow", "hour"] | ["COUNT(*)", "AVG(CASE WHEN status = 'Completed' AND dist > 0 THEN value / dist END)", "COUNT(*)", "SUM(CASE WHEN status IN ('Cancelled by Customer', 'Cancelled by Driver') THEN 1 ELSE 0 END)"] | 168 | 404.699 |
| [S31/Q29](#s31) | success | ["sheet1"] | 0 / {} | ["hour"] | ["COUNT(*)", "SUM(CASE WHEN status = 'Cancelled by Customer' THEN 1 ELSE 0 END)", "SUM(CASE WHEN status = 'Cancelled by Driver' THEN 1 ELSE 0 END)"] | 24 | 125.135 |
| [S32/Q30](#s32) | success | ["sheet1"] | 0 / {} | ["date_key"] | ["COUNT(*)", "AVG(CASE WHEN status = 'Completed' AND dist > 0 THEN value / dist END)", "COUNT(*)", "SUM(CASE WHEN status IN ('Cancelled by Customer', 'Cancelled by Driver') THEN 1 ELSE 0 END)"] | 10 | 333.099 |
| [S33/Q31](#s33) | success | ["sheet1"] | 0 / {} | ["date_key"] | ["COUNT(*)", "AVG(CASE WHEN status = 'Completed' AND dist > 0 THEN value / dist END)", "COUNT(*)", "SUM(CASE WHEN status IN ('Cancelled by Customer', 'Cancelled by Driver') THEN 1 ELSE 0 END)"] | 10 | 328.74 |


## 元数据和设置

| SQL | 类别 | 状态 | 内容 |
| --- | --- | --- | --- |
| S1 | connection_setup | success | PRAGMA query_only=ON |
| S2 | metadata | success | SELECT name,sql FROM sqlite_master WHERE type='table' ORDER BY name |


## Python 与执行位置

人工源码审查：**partial_violation**。SQL prepares hourly/daily ride aggregates. Python runs correlations and a t-test and renders plots, which are appropriate supplements. P2/P3 additionally roll daily rows into weekday/monthly means and sums and calculate cancellation ratios; those SQL-capable preparation steps are deviations even though inputs are already aggregated. [证据](../reviews/dacomp-021.json)。

P1：SQLite does not support time-series visualization or statistical summaries (e.g., rolling means, percentiles, regression) needed to quantify peak/trough periods. I will fetch pre-aggregated daily (365 rows) and hourly (24 rows) statistics computed in SQL and create figures in Python.

[源码](../../../runs/dsv4flash-db-first-full-01/dacomp-021/attempt-01/python/P1.py)；[输出](../../../runs/dsv4flash-db-first-full-01/dacomp-021/attempt-01/python/P1.stdout)；[错误](../../../runs/dsv4flash-db-first-full-01/dacomp-021/attempt-01/python/P1.stderr)。检出需人工核验的 SQL 可实现操作：.query(, sort_values(；不能仅凭理由判为合规。

P2：Correlation and t-test statistics are not available in SQLite; this requires scipy. Data was pre-aggregated to one row per day (365 rows) in SQL.

[源码](../../../runs/dsv4flash-db-first-full-01/dacomp-021/attempt-01/python/P2.py)；[输出](../../../runs/dsv4flash-db-first-full-01/dacomp-021/attempt-01/python/P2.stdout)；[错误](../../../runs/dsv4flash-db-first-full-01/dacomp-021/attempt-01/python/P2.stderr)。检出需人工核验的 SQL 可实现操作：groupby(；不能仅凭理由判为合规。

P3：Visualization, heatmaps, and multi-dimensional aggregation (hour×weekday pivot) are not supported by SQLite. The data is pre-aggregated by SQL queries (24 rows hourly, 365 rows daily, 168 rows hour×weekday).

[源码](../../../runs/dsv4flash-db-first-full-01/dacomp-021/attempt-01/python/P3.py)；[输出](../../../runs/dsv4flash-db-first-full-01/dacomp-021/attempt-01/python/P3.stdout)；[错误](../../../runs/dsv4flash-db-first-full-01/dacomp-021/attempt-01/python/P3.stderr)。检出需人工核验的 SQL 可实现操作：groupby(, .query(；不能仅凭理由判为合规。

P4：Final summary statistics computed from pre-aggregated data (365 daily rows, 24 hourly rows) using Python for weighted averages and formatted output.

[源码](../../../runs/dsv4flash-db-first-full-01/dacomp-021/attempt-01/python/P4.py)；[输出](../../../runs/dsv4flash-db-first-full-01/dacomp-021/attempt-01/python/P4.stdout)；[错误](../../../runs/dsv4flash-db-first-full-01/dacomp-021/attempt-01/python/P4.stderr)。自动源码筛查未检出预设迁出信号；这不是全面语义合规证明。

## 优化机会

已验证候选。筛选限于精确 SQL、相同自包含 CTE、相同单表完整过滤、可分解单表聚合；未覆盖任意 Join 等价和一般谓词蕴含。全部候选都是 offline，未测在线预测。

| 候选 | 类型 | 已有结果 | 覆盖 SQL | 后续次数 | 中间行数 | 验证 | 成本 |
| --- | --- | --- | --- | --- | --- | --- | --- |
| C1 | exact-result reuse | True | ["S19", "S20", "S21"] | 2 | 24 | verified | Not benchmarked; correctness alone does not establish net speedup. |
| C2 | common subexpression | False | ["S15", "S22"] | 1 | unknown | not_verified_cap | Not tested |
| C3 | common subexpression | False | ["S17", "S18"] | 1 | unknown | not_verified_cap | Not tested |
| C4 | common subexpression | False | ["S19", "S20", "S21", "S24"] | 3 | 150000 | verified | Not benchmarked; correctness alone does not establish net speedup. |
| C5 | common subexpression | False | ["S23", "S32", "S33"] | 2 | 150000 | verified | Warm-cache baseline 803.313 ms vs build+reuse 555.928 ms, ratio 1.445; five repetitions, see performance evidence. |
| C6 | aggregate MV | False | ["S4", "S6", "S7"] | 2 | unknown | not_verified_cap | Not tested |


已验证覆盖（含触发查询、候选并集去重）：7/29 条成功数据 SQL。正确性仅针对当前数据库快照；未测性能的候选不能声称已加速。

[完整 build/rewrite 与比较证据](dacomp-021.analysis.json)。

### C4：common subexpression

Identical self-contained CTE body across queries.

原查询 [S19](#s19), [S20](#s20), [S21](#s21), [S24](#s24) → 新增共享状态 C4 → 后续 3 次可复用。该构建点为事后假设，不代表 Agent 当时预知后续。

构建定义：

```sql
SELECT CAST(SUBSTRING("Time", 1, INSTR("Time", ':') - 1) AS INTEGER) AS hour, "Booking Status" AS status, "Booking Value" AS value, "Ride Distance" AS dist FROM sheet1
```

受益查询 S19 的改写示例：

```sql
WITH parsed AS (SELECT * FROM temp.reuse_candidate) SELECT hour, COUNT(*) AS bookings, SUM(CASE WHEN status IN ('Cancelled by Customer', 'Cancelled by Driver') THEN 1 ELSE 0 END) AS cancellations, ROUND(100.0 * SUM(CASE WHEN status IN ('Cancelled by Customer', 'Cancelled by Driver') THEN 1 ELSE 0 END) / COUNT(*), 2) AS cancel_pct, SUM(CASE WHEN status = 'No Driver Found' THEN 1 ELSE 0 END) AS no_driver, ROUND(100.0 * SUM(CASE WHEN status = 'No Driver Found' THEN 1 ELSE 0 END) / COUNT(*), 2) AS nodriver_pct, SUM(CASE WHEN status = 'Incomplete' THEN 1 ELSE 0 END) AS incomplete, SUM(CASE WHEN status = 'Completed' THEN 1 ELSE 0 END) AS completed, ROUND(AVG(CASE WHEN status = 'Completed' AND dist > 0 THEN value / dist END), 2) AS avg_cost_per_km, ROUND(AVG(CASE WHEN status = 'Completed' THEN dist END), 2) AS avg_dist_km FROM parsed GROUP BY hour ORDER BY hour
```

| 原 SQL | 列名一致 | 结果一致 | 比较方法 |
| --- | --- | --- | --- |
| S19 | True | True | ordered_numeric_tolerance |
| S20 | True | True | ordered_numeric_tolerance |
| S21 | True | True | ordered_numeric_tolerance |
| S24 | True | True | ordered_numeric_tolerance |


验证状态：verified；成本结论：Not benchmarked; correctness alone does not establish net speedup.

### C1：exact-result reuse

Identical normalized SQL and parameters; archive equality checked.

原查询 [S19](#s19), [S20](#s20), [S21](#s21) → 保留前序结果 S19 → 后续 2 次可复用。该构建点为事后假设，不代表 Agent 当时预知后续。

| 原 SQL | 列名一致 | 结果一致 | 比较方法 |
| --- | --- | --- | --- |
| S20 | True | True | ordered_numeric_tolerance |
| S21 | True | True | ordered_numeric_tolerance |


验证状态：verified；成本结论：Not benchmarked; correctness alone does not establish net speedup.

### C5：common subexpression

Identical self-contained CTE body across queries.

原查询 [S23](#s23), [S32](#s32), [S33](#s33) → 新增共享状态 C5 → 后续 2 次可复用。该构建点为事后假设，不代表 Agent 当时预知后续。

构建定义：

```sql
SELECT PRINTF('%04d-%02d-%02d', CAST(SUBSTRING("Date", 1, 4) AS INTEGER), CAST(SUBSTRING("Date", INSTR("Date", '/') + 1, INSTR(SUBSTRING("Date", INSTR("Date", '/') + 1), '/') - 1) AS INTEGER), CAST(SUBSTRING("Date", INSTR("Date", '/') + INSTR(SUBSTRING("Date", INSTR("Date", '/') + 1), '/') + 1) AS INTEGER)) AS date_key, "Booking Status" AS status, "Booking Value" AS value, "Ride Distance" AS dist FROM sheet1
```

受益查询 S23 的改写示例：

```sql
WITH parsed AS (SELECT * FROM temp.reuse_candidate) SELECT date_key, COUNT(*) AS bookings, SUM(CASE WHEN status IN ('Cancelled by Customer', 'Cancelled by Driver') THEN 1 ELSE 0 END) AS cancellations, SUM(CASE WHEN status = 'No Driver Found' THEN 1 ELSE 0 END) AS no_driver, SUM(CASE WHEN status = 'Incomplete' THEN 1 ELSE 0 END) AS incomplete, SUM(CASE WHEN status = 'Completed' THEN 1 ELSE 0 END) AS completed, ROUND(AVG(CASE WHEN status = 'Completed' AND dist > 0 THEN value / dist END), 4) AS cost_per_km FROM parsed GROUP BY date_key ORDER BY date_key
```

| 原 SQL | 列名一致 | 结果一致 | 比较方法 |
| --- | --- | --- | --- |
| S23 | True | True | ordered_numeric_tolerance |
| S32 | True | True | ordered_numeric_tolerance |
| S33 | True | True | ordered_numeric_tolerance |


验证状态：verified；成本结论：Warm-cache baseline 803.313 ms vs build+reuse 555.928 ms, ratio 1.445; five repetitions, see performance evidence.

[性能证据 C5](dacomp-021.C5.performance.json)：measured。

结果依赖：自动记录 SQL→Python 的接口父调用，以及源码中引用归档文件的消费者；字面值相同不认定因果。模型方向选择需要人工读取消息，尚未做全面因果标注。

[原始报告](../../../runs/dsv4flash-db-first-full-01/dacomp-021/attempt-01/answer.md)；[统一消息](../../../runs/dsv4flash-db-first-full-01/dacomp-021/attempt-01/messages.jsonl)；[原始 OpenCode 事件](../../../runs/dsv4flash-db-first-full-01/dacomp-021/attempt-01/opencode.jsonl)；[SQL 引擎日志](../../../runs/dsv4flash-db-first-full-01/dacomp-021/attempt-01/sql_journal.jsonl)。

[可读报告（本地图片链接规范化）](../answers/dacomp-021.md)。原始回答保留，分析结论未改写。

## S1

类别 `connection_setup`；来源 `connection`；调用 `515d4038514148eeb76c8196d9dde166`；状态 `success`。

```sql
PRAGMA query_only=ON
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-021/attempt-01/sql/S1.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-021/attempt-01/sql/S1.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-021/attempt-01/results/S1.rows.jsonl)；完整：True；SHA256：`e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`。

## S2

类别 `metadata`；来源 `list_db`；调用 `515d4038514148eeb76c8196d9dde166`；状态 `success`。

```sql
SELECT name,sql FROM sqlite_master WHERE type='table' ORDER BY name
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-021/attempt-01/sql/S2.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-021/attempt-01/sql/S2.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-021/attempt-01/results/S2.rows.jsonl)；完整：True；SHA256：`c342ec0fa7df72007bdc6a8a6d4cc9704995ccdcc9eace19d76e76f9a51240ee`。

## S3

类别 `data`；来源 `query_db`；调用 `0da31cec181b433eac871a406e50e9dd`；状态 `success`。

```sql
SELECT COUNT(*) AS total_rows, COUNT(DISTINCT "Booking ID") AS unique_bookings, MIN("Date") AS min_date, MAX("Date") AS max_date, COUNT(DISTINCT "Date") AS distinct_dates FROM sheet1
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-021/attempt-01/sql/S3.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-021/attempt-01/sql/S3.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-021/attempt-01/results/S3.rows.jsonl)；完整：True；SHA256：`a0a9fa4decdadfd837c4e705fabf891f62a433024d310846b798a31875cb59fe`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "sheet1", "kind": "base", "block": null, "base_tables": ["sheet1"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |
| B1 | COUNT(DISTINCT "Booking ID") | [{"table": "sheet1", "column": "Booking ID"}] | [] | False |
| B1 | MIN("Date") | [{"table": "sheet1", "column": "Date"}] | [] | False |
| B1 | MAX("Date") | [{"table": "sheet1", "column": "Date"}] | [] | False |
| B1 | COUNT(DISTINCT "Date") | [{"table": "sheet1", "column": "Date"}] | [] | False |


## S4

类别 `data`；来源 `query_db`；调用 `4bc047af24bf4efabfeece8e601c6e08`；状态 `success`。

```sql
SELECT "Booking Status", COUNT(*) AS n FROM sheet1 GROUP BY "Booking Status" ORDER BY n DESC
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-021/attempt-01/sql/S4.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-021/attempt-01/sql/S4.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-021/attempt-01/results/S4.rows.jsonl)；完整：True；SHA256：`5617ad923ca548d1ee8198ca2197a14b5191646164f5320b5c0448afc0de731c`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "sheet1", "kind": "base", "block": null, "base_tables": ["sheet1"]}] | [] | ["\"Booking Status\""] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |


## S5

类别 `data`；来源 `query_db`；调用 `775df0f437d14369a55da1c3976ffcf5`；状态 `success`。

```sql
SELECT * FROM sheet1 LIMIT 10
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-021/attempt-01/sql/S5.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-021/attempt-01/sql/S5.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-021/attempt-01/results/S5.rows.jsonl)；完整：True；SHA256：`b6089809b1f3d80807f61fc82cdd765ad90070e4efc3ffe266550adda88c02b7`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "sheet1", "kind": "base", "block": null, "base_tables": ["sheet1"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |


## S6

类别 `data`；来源 `query_db`；调用 `134a687c5f124681892e34b847d5675c`；状态 `success`。

```sql
SELECT substr("Date",1,4) AS y, count(*) AS n FROM sheet1 GROUP BY y
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-021/attempt-01/sql/S6.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-021/attempt-01/sql/S6.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-021/attempt-01/results/S6.rows.jsonl)；完整：True；SHA256：`70fb1da015012de5972405a6773d0babbb04742a39fee796be3de264cc83d8a5`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "sheet1", "kind": "base", "block": null, "base_tables": ["sheet1"]}] | [] | ["SUBSTRING(\"Date\", 1, 4)"] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |


## S7

类别 `data`；来源 `query_db`；调用 `b385c0b589ee4b7799da692a2af697d7`；状态 `success`。

```sql
SELECT "Date", count(*) AS n FROM sheet1 GROUP BY "Date" ORDER BY n DESC LIMIT 20
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-021/attempt-01/sql/S7.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-021/attempt-01/sql/S7.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-021/attempt-01/results/S7.rows.jsonl)；完整：True；SHA256：`1acf23c69457eadceef84196643a5314dd3f8446d019fc1495443db627162c6b`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "sheet1", "kind": "base", "block": null, "base_tables": ["sheet1"]}] | [] | ["\"Date\""] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |


## S8

类别 `data`；来源 `query_db`；调用 `f13b7d9165e64ad0a50d9c64d8032f10`；状态 `success`。

```sql
SELECT min(length("Time")) AS min_len, max(length("Time")) AS max_len, "Time" FROM sheet1 WHERE length("Time") != 8 LIMIT 20
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-021/attempt-01/sql/S8.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-021/attempt-01/sql/S8.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-021/attempt-01/results/S8.rows.jsonl)；完整：True；SHA256：`8a7d0ab49361cf19cd7082ca66a64c20f3fe3e25495441847d83dd9aeeaa6d5b`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "sheet1", "kind": "base", "block": null, "base_tables": ["sheet1"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | MIN(LENGTH("Time")) | [{"table": "sheet1", "column": "Time"}] | [] | False |
| B1 | MAX(LENGTH("Time")) | [{"table": "sheet1", "column": "Time"}] | [] | False |


## S9

类别 `data`；来源 `query_db`；调用 `b6754fb7614e40769a68b8c90430cb14`；状态 `success`。

```sql
SELECT "Date", length("Date") AS dlen FROM sheet1 GROUP BY "Date" ORDER BY dlen, "Date" LIMIT 30
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-021/attempt-01/sql/S9.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-021/attempt-01/sql/S9.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-021/attempt-01/results/S9.rows.jsonl)；完整：True；SHA256：`7c2548521ac23800dc69983a4c74abd6bc34371a4731e2cad563bcdd8277eaee`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "sheet1", "kind": "base", "block": null, "base_tables": ["sheet1"]}] | [] | ["\"Date\""] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |


## S10

类别 `data`；来源 `query_db`；调用 `ff370f62f96d4254a60d8eb181829845`；状态 `success`。

```sql
SELECT "Time", length("Time") AS tlen FROM sheet1 GROUP BY "Time" ORDER BY tlen, "Time" LIMIT 20
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-021/attempt-01/sql/S10.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-021/attempt-01/sql/S10.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-021/attempt-01/results/S10.rows.jsonl)；完整：True；SHA256：`85119866f1302aeb46cbd089a93083f969c5888cb2fa5cb5f1ba123be98c08b8`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "sheet1", "kind": "base", "block": null, "base_tables": ["sheet1"]}] | [] | ["\"Time\""] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |


## S11

类别 `data`；来源 `query_db`；调用 `441dd94384a04343bb1e50e799f1e72f`；状态 `failed`。

```sql
WITH parsed AS (
  SELECT
    printf('%04d-%02d-%02d',
           CAST(substr("Date",1,4) AS INTEGER),
           CAST(substr("Date",6, instr("Date",'/')-1) AS INTEGER),
           CAST(substr("Date", instr("Date",'/',6)+1) AS INTEGER)) AS date_key,
    CAST(substr("Time", 1, instr("Time", ':')-1) AS INTEGER) AS hour,
    "Booking Status" AS status
  FROM sheet1
)
SELECT date_key, COUNT(*) AS bookings
FROM parsed
GROUP BY date_key
ORDER BY bookings DESC
LIMIT 15
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-021/attempt-01/sql/S11.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-021/attempt-01/sql/S11.parameters.json)。

错误：`OperationalError('wrong number of arguments to function instr()')`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "sheet1", "kind": "base", "block": null, "base_tables": ["sheet1"]}] | [] | [] |
| B2 | [{"alias": "parsed", "kind": "derived", "block": "B1", "base_tables": ["sheet1"]}] | [] | ["date_key"] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B2 | COUNT(*) | [] | [] | True |


## S12

类别 `data`；来源 `query_db`；调用 `29c8659aef9c44678cae87ebb38597b5`；状态 `failed`。

```sql
WITH parsed AS (
  SELECT
    printf('%04d-%02d-%02d',
           CAST(substr("Date",1,4) AS INTEGER),
           CAST(substr("Date",6, instr("Date",'/')-1) AS INTEGER),
           CAST(substr("Date", instr("Date",'/',6)+1) AS INTEGER)) AS date_key,
    CAST(substr("Time", 1, instr("Time", ':')-1) AS INTEGER) AS hour
  FROM sheet1
)
SELECT hour, COUNT(*) AS bookings
FROM parsed
GROUP BY hour
ORDER BY bookings DESC
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-021/attempt-01/sql/S12.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-021/attempt-01/sql/S12.parameters.json)。

错误：`OperationalError('wrong number of arguments to function instr()')`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "sheet1", "kind": "base", "block": null, "base_tables": ["sheet1"]}] | [] | [] |
| B2 | [{"alias": "parsed", "kind": "derived", "block": "B1", "base_tables": ["sheet1"]}] | [] | ["hour"] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B2 | COUNT(*) | [] | [] | True |


## S13

类别 `data`；来源 `query_db`；调用 `506dd2eb240e4b96b30e93aa4fa79433`；状态 `success`。

```sql
WITH parsed AS (
  SELECT
    printf('%04d-%02d-%02d',
           CAST(substr("Date",1,4) AS INTEGER),
           CAST(substr("Date", instr("Date",'/')+1, instr(substr("Date", instr("Date",'/')+1),'/')-1) AS INTEGER),
           CAST(substr("Date", instr("Date",'/')+instr(substr("Date", instr("Date",'/')+1),'/')+1) AS INTEGER)) AS date_key,
    CAST(substr("Time", 1, instr("Time", ':')-1) AS INTEGER) AS hour,
    "Booking Status" AS status
  FROM sheet1
)
SELECT date_key, COUNT(*) AS bookings
FROM parsed
GROUP BY date_key
ORDER BY bookings DESC
LIMIT 15
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-021/attempt-01/sql/S13.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-021/attempt-01/sql/S13.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-021/attempt-01/results/S13.rows.jsonl)；完整：True；SHA256：`81f8e4dc1808d820d1c2df70db6b5fab59670124100ae58e7871337cfc38e232`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "sheet1", "kind": "base", "block": null, "base_tables": ["sheet1"]}] | [] | [] |
| B2 | [{"alias": "parsed", "kind": "derived", "block": "B1", "base_tables": ["sheet1"]}] | [] | ["date_key"] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B2 | COUNT(*) | [] | [] | True |


## S14

类别 `data`；来源 `query_db`；调用 `46cfcf3b70494b1d92f46a43df06edbf`；状态 `success`。

```sql
WITH parsed AS (
  SELECT
    printf('%04d-%02d-%02d',
           CAST(substr("Date",1,4) AS INTEGER),
           CAST(substr("Date", instr("Date",'/')+1, instr(substr("Date", instr("Date",'/')+1),'/')-1) AS INTEGER),
           CAST(substr("Date", instr("Date",'/')+instr(substr("Date", instr("Date",'/')+1),'/')+1) AS INTEGER)) AS date_key,
    CAST(substr("Time", 1, instr("Time", ':')-1) AS INTEGER) AS hour
  FROM sheet1
)
SELECT hour, COUNT(*) AS bookings
FROM parsed
GROUP BY hour
ORDER BY bookings DESC
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-021/attempt-01/sql/S14.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-021/attempt-01/sql/S14.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-021/attempt-01/results/S14.rows.jsonl)；完整：True；SHA256：`afce28a6b9f5619b6758c1b92558d7e5432d6707015908907340965c28e8d09f`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "sheet1", "kind": "base", "block": null, "base_tables": ["sheet1"]}] | [] | [] |
| B2 | [{"alias": "parsed", "kind": "derived", "block": "B1", "base_tables": ["sheet1"]}] | [] | ["hour"] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B2 | COUNT(*) | [] | [] | True |


## S15

类别 `data`；来源 `query_db`；调用 `fcd74c61db5f41fa89ca684e303b2a0f`；状态 `success`。

```sql
WITH parsed AS (
  SELECT
    printf('%04d-%02d-%02d',
           CAST(substr("Date",1,4) AS INTEGER),
           CAST(substr("Date", instr("Date",'/')+1, instr(substr("Date", instr("Date",'/')+1),'/')-1) AS INTEGER),
           CAST(substr("Date", instr("Date",'/')+instr(substr("Date", instr("Date",'/')+1),'/')+1) AS INTEGER)) AS date_key
  FROM sheet1
)
SELECT MIN(date_key) AS min_date, MAX(date_key) AS max_date, COUNT(DISTINCT date_key) AS days
FROM parsed
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-021/attempt-01/sql/S15.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-021/attempt-01/sql/S15.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-021/attempt-01/results/S15.rows.jsonl)；完整：True；SHA256：`98b4d703e311bbb0c9fab8786a2c100f1af64c4c6fed1ede9f9126894fc33ab0`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "sheet1", "kind": "base", "block": null, "base_tables": ["sheet1"]}] | [] | [] |
| B2 | [{"alias": "parsed", "kind": "derived", "block": "B1", "base_tables": ["sheet1"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B2 | MIN(date_key) | [{"table": "sheet1", "column": "Date"}, {"table": "sheet1", "column": "Date"}, {"table": "sheet1", "column": "Date"}, {"table": "sheet1", "column": "Date"}, {"table": "sheet1", "column": "Date"}, {"table": "sheet1", "column": "Date"}, {"table": "sheet1", "column": "Date"}, {"table": "sheet1", "column": "Date"}, {"table": "sheet1", "column": "Date"}] | [] | False |
| B2 | MAX(date_key) | [{"table": "sheet1", "column": "Date"}, {"table": "sheet1", "column": "Date"}, {"table": "sheet1", "column": "Date"}, {"table": "sheet1", "column": "Date"}, {"table": "sheet1", "column": "Date"}, {"table": "sheet1", "column": "Date"}, {"table": "sheet1", "column": "Date"}, {"table": "sheet1", "column": "Date"}, {"table": "sheet1", "column": "Date"}] | [] | False |
| B2 | COUNT(DISTINCT date_key) | [{"table": "sheet1", "column": "Date"}, {"table": "sheet1", "column": "Date"}, {"table": "sheet1", "column": "Date"}, {"table": "sheet1", "column": "Date"}, {"table": "sheet1", "column": "Date"}, {"table": "sheet1", "column": "Date"}, {"table": "sheet1", "column": "Date"}, {"table": "sheet1", "column": "Date"}, {"table": "sheet1", "column": "Date"}] | [] | False |


## S16

类别 `data`；来源 `query_db`；调用 `2978aa44c3d540e9a842a69eec948477`；状态 `success`。

```sql
WITH parsed AS (
  SELECT
    CAST(substr("Time", 1, instr("Time", ':')-1) AS INTEGER) AS hour
  FROM sheet1
)
SELECT hour, COUNT(*) AS bookings
FROM parsed
GROUP BY hour
ORDER BY hour
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-021/attempt-01/sql/S16.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-021/attempt-01/sql/S16.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-021/attempt-01/results/S16.rows.jsonl)；完整：True；SHA256：`8421d7215a8a4fd454ca0b817191c587b67c97d1d0ea5fae1dab308a01f665d7`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "sheet1", "kind": "base", "block": null, "base_tables": ["sheet1"]}] | [] | [] |
| B2 | [{"alias": "parsed", "kind": "derived", "block": "B1", "base_tables": ["sheet1"]}] | [] | ["hour"] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B2 | COUNT(*) | [] | [] | True |


## S17

类别 `data`；来源 `query_db`；调用 `543ac0dc8fc244ce9b74c2bb99b8ca2c`；状态 `success`。

```sql
WITH parsed AS (
  SELECT
    printf('%04d-%02d-%02d',
           CAST(substr("Date",1,4) AS INTEGER),
           CAST(substr("Date", instr("Date",'/')+1, instr(substr("Date", instr("Date",'/')+1),'/')-1) AS INTEGER),
           CAST(substr("Date", instr("Date",'/')+instr(substr("Date", instr("Date",'/')+1),'/')+1) AS INTEGER)) AS date_key,
    CAST(substr("Time", 1, instr("Time", ':')-1) AS INTEGER) AS hour,
    "Booking Status" AS status,
    "Booking Value" AS value,
    "Ride Distance" AS dist
  FROM sheet1
)
SELECT
  CASE CAST(strftime('%w', date_key) AS INTEGER)
    WHEN 0 THEN 'Sunday'
    WHEN 1 THEN 'Monday'
    WHEN 2 THEN 'Tuesday'
    WHEN 3 THEN 'Wednesday'
    WHEN 4 THEN 'Thursday'
    WHEN 5 THEN 'Friday'
    WHEN 6 THEN 'Saturday'
  END AS weekday,
  COUNT(*) AS bookings,
  SUM(CASE WHEN status IN ('Cancelled by Customer','Cancelled by Driver') THEN 1 ELSE 0 END) AS cancellations,
  ROUND(100.0 * SUM(CASE WHEN status IN ('Cancelled by Customer','Cancelled by Driver') THEN 1 ELSE 0 END) / COUNT(*), 2) AS cancel_pct,
  SUM(CASE WHEN status = 'No Driver Found' THEN 1 ELSE 0 END) AS no_driver,
  SUM(CASE WHEN status = 'Incomplete' THEN 1 ELSE 0 END) AS incomplete,
  SUM(CASE WHEN status = 'Completed' THEN 1 ELSE 0 END) AS completed,
  ROUND(AVG(CASE WHEN status = 'Completed' AND dist > 0 THEN value / dist END), 2) AS avg_cost_per_km
FROM parsed
GROUP BY weekday
ORDER BY bookings DESC
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-021/attempt-01/sql/S17.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-021/attempt-01/sql/S17.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-021/attempt-01/results/S17.rows.jsonl)；完整：True；SHA256：`8ad84e19748283e3b3f9c7ef7ae4127364879be15f36439a6588ebc53903c3d9`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "sheet1", "kind": "base", "block": null, "base_tables": ["sheet1"]}] | [] | [] |
| B2 | [{"alias": "parsed", "kind": "derived", "block": "B1", "base_tables": ["sheet1"]}] | [] | ["CASE CAST(STRFTIME('%w', date_key) AS INTEGER) WHEN 0 THEN 'Sunday' WHEN 1 THEN 'Monday' WHEN 2 THEN 'Tuesday' WHEN 3 THEN 'Wednesday' WHEN 4 THEN 'Thursday' WHEN 5 THEN 'Friday' WHEN 6 THEN 'Saturday' END"] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B2 | COUNT(*) | [] | [] | True |
| B2 | SUM(CASE WHEN status IN ('Cancelled by Customer', 'Cancelled by Driver') THEN 1 ELSE 0 END) | [] | [{"table": "sheet1", "column": "Booking Status"}] | False |
| B2 | SUM(CASE WHEN status = 'No Driver Found' THEN 1 ELSE 0 END) | [] | [{"table": "sheet1", "column": "Booking Status"}] | False |
| B2 | SUM(CASE WHEN status = 'Incomplete' THEN 1 ELSE 0 END) | [] | [{"table": "sheet1", "column": "Booking Status"}] | False |
| B2 | SUM(CASE WHEN status = 'Completed' THEN 1 ELSE 0 END) | [] | [{"table": "sheet1", "column": "Booking Status"}] | False |
| B2 | AVG(CASE WHEN status = 'Completed' AND dist > 0 THEN value / dist END) | [{"table": "sheet1", "column": "Booking Value"}, {"table": "sheet1", "column": "Ride Distance"}] | [{"table": "sheet1", "column": "Booking Status"}, {"table": "sheet1", "column": "Ride Distance"}] | False |
| B2 | COUNT(*) | [] | [] | True |
| B2 | SUM(CASE WHEN status IN ('Cancelled by Customer', 'Cancelled by Driver') THEN 1 ELSE 0 END) | [] | [{"table": "sheet1", "column": "Booking Status"}] | False |


## S18

类别 `data`；来源 `query_db`；调用 `8eb1278a0a79445eba1f1be592d512e0`；状态 `success`。

```sql
WITH parsed AS (
  SELECT
    printf('%04d-%02d-%02d',
           CAST(substr("Date",1,4) AS INTEGER),
           CAST(substr("Date", instr("Date",'/')+1, instr(substr("Date", instr("Date",'/')+1),'/')-1) AS INTEGER),
           CAST(substr("Date", instr("Date",'/')+instr(substr("Date", instr("Date",'/')+1),'/')+1) AS INTEGER)) AS date_key,
    CAST(substr("Time", 1, instr("Time", ':')-1) AS INTEGER) AS hour,
    "Booking Status" AS status,
    "Booking Value" AS value,
    "Ride Distance" AS dist
  FROM sheet1
)
SELECT
  CAST(strftime('%m', date_key) AS INTEGER) AS month,
  COUNT(*) AS bookings,
  SUM(CASE WHEN status IN ('Cancelled by Customer','Cancelled by Driver') THEN 1 ELSE 0 END) AS cancellations,
  ROUND(100.0 * SUM(CASE WHEN status IN ('Cancelled by Customer','Cancelled by Driver') THEN 1 ELSE 0 END) / COUNT(*), 2) AS cancel_pct,
  ROUND(AVG(CASE WHEN status = 'Completed' AND dist > 0 THEN value / dist END), 2) AS avg_cost_per_km
FROM parsed
GROUP BY month
ORDER BY month
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-021/attempt-01/sql/S18.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-021/attempt-01/sql/S18.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-021/attempt-01/results/S18.rows.jsonl)；完整：True；SHA256：`f39d6c9e5fa601d017f57e36ea1696a5f2ae751b6680ae362951134848b0da37`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "sheet1", "kind": "base", "block": null, "base_tables": ["sheet1"]}] | [] | [] |
| B2 | [{"alias": "parsed", "kind": "derived", "block": "B1", "base_tables": ["sheet1"]}] | [] | ["CAST(STRFTIME('%m', date_key) AS INTEGER)"] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B2 | COUNT(*) | [] | [] | True |
| B2 | SUM(CASE WHEN status IN ('Cancelled by Customer', 'Cancelled by Driver') THEN 1 ELSE 0 END) | [] | [{"table": "sheet1", "column": "Booking Status"}] | False |
| B2 | AVG(CASE WHEN status = 'Completed' AND dist > 0 THEN value / dist END) | [{"table": "sheet1", "column": "Booking Value"}, {"table": "sheet1", "column": "Ride Distance"}] | [{"table": "sheet1", "column": "Booking Status"}, {"table": "sheet1", "column": "Ride Distance"}] | False |
| B2 | COUNT(*) | [] | [] | True |
| B2 | SUM(CASE WHEN status IN ('Cancelled by Customer', 'Cancelled by Driver') THEN 1 ELSE 0 END) | [] | [{"table": "sheet1", "column": "Booking Status"}] | False |


## S19

类别 `data`；来源 `query_db`；调用 `e9e70cf8f0f944018c33de1bd8a904f9`；状态 `success`。

```sql
WITH parsed AS (
  SELECT
    CAST(substr("Time", 1, instr("Time", ':')-1) AS INTEGER) AS hour,
    "Booking Status" AS status,
    "Booking Value" AS value,
    "Ride Distance" AS dist
  FROM sheet1
)
SELECT hour,
  COUNT(*) AS bookings,
  SUM(CASE WHEN status IN ('Cancelled by Customer','Cancelled by Driver') THEN 1 ELSE 0 END) AS cancellations,
  ROUND(100.0 * SUM(CASE WHEN status IN ('Cancelled by Customer','Cancelled by Driver') THEN 1 ELSE 0 END) / COUNT(*), 2) AS cancel_pct,
  SUM(CASE WHEN status = 'No Driver Found' THEN 1 ELSE 0 END) AS no_driver,
  ROUND(100.0 * SUM(CASE WHEN status = 'No Driver Found' THEN 1 ELSE 0 END) / COUNT(*), 2) AS nodriver_pct,
  SUM(CASE WHEN status = 'Incomplete' THEN 1 ELSE 0 END) AS incomplete,
  SUM(CASE WHEN status = 'Completed' THEN 1 ELSE 0 END) AS completed,
  ROUND(AVG(CASE WHEN status = 'Completed' AND dist > 0 THEN value / dist END), 2) AS avg_cost_per_km,
  ROUND(AVG(CASE WHEN status = 'Completed' THEN dist END), 2) AS avg_dist_km
FROM parsed
GROUP BY hour
ORDER BY hour
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-021/attempt-01/sql/S19.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-021/attempt-01/sql/S19.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-021/attempt-01/results/S19.rows.jsonl)；完整：True；SHA256：`13030f951c0582cfbe584dc1d580a8e68d9c176454e3d64a8a9427634f3ca885`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "sheet1", "kind": "base", "block": null, "base_tables": ["sheet1"]}] | [] | [] |
| B2 | [{"alias": "parsed", "kind": "derived", "block": "B1", "base_tables": ["sheet1"]}] | [] | ["hour"] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B2 | COUNT(*) | [] | [] | True |
| B2 | SUM(CASE WHEN status IN ('Cancelled by Customer', 'Cancelled by Driver') THEN 1 ELSE 0 END) | [] | [{"table": "sheet1", "column": "Booking Status"}] | False |
| B2 | SUM(CASE WHEN status = 'No Driver Found' THEN 1 ELSE 0 END) | [] | [{"table": "sheet1", "column": "Booking Status"}] | False |
| B2 | SUM(CASE WHEN status = 'Incomplete' THEN 1 ELSE 0 END) | [] | [{"table": "sheet1", "column": "Booking Status"}] | False |
| B2 | SUM(CASE WHEN status = 'Completed' THEN 1 ELSE 0 END) | [] | [{"table": "sheet1", "column": "Booking Status"}] | False |
| B2 | AVG(CASE WHEN status = 'Completed' AND dist > 0 THEN value / dist END) | [{"table": "sheet1", "column": "Booking Value"}, {"table": "sheet1", "column": "Ride Distance"}] | [{"table": "sheet1", "column": "Booking Status"}, {"table": "sheet1", "column": "Ride Distance"}] | False |
| B2 | AVG(CASE WHEN status = 'Completed' THEN dist END) | [{"table": "sheet1", "column": "Ride Distance"}] | [{"table": "sheet1", "column": "Booking Status"}] | False |
| B2 | COUNT(*) | [] | [] | True |
| B2 | COUNT(*) | [] | [] | True |
| B2 | SUM(CASE WHEN status IN ('Cancelled by Customer', 'Cancelled by Driver') THEN 1 ELSE 0 END) | [] | [{"table": "sheet1", "column": "Booking Status"}] | False |
| B2 | SUM(CASE WHEN status = 'No Driver Found' THEN 1 ELSE 0 END) | [] | [{"table": "sheet1", "column": "Booking Status"}] | False |


## S20

类别 `data`；来源 `query_db`；调用 `0358201e6c914a58ade9d0f8fdfdb922`；状态 `success`。

```sql
WITH parsed AS (
  SELECT
    CAST(substr("Time", 1, instr("Time", ':')-1) AS INTEGER) AS hour,
    "Booking Status" AS status,
    "Booking Value" AS value,
    "Ride Distance" AS dist
  FROM sheet1
)
SELECT hour,
  COUNT(*) AS bookings,
  SUM(CASE WHEN status IN ('Cancelled by Customer','Cancelled by Driver') THEN 1 ELSE 0 END) AS cancellations,
  ROUND(100.0 * SUM(CASE WHEN status IN ('Cancelled by Customer','Cancelled by Driver') THEN 1 ELSE 0 END) / COUNT(*), 2) AS cancel_pct,
  SUM(CASE WHEN status = 'No Driver Found' THEN 1 ELSE 0 END) AS no_driver,
  ROUND(100.0 * SUM(CASE WHEN status = 'No Driver Found' THEN 1 ELSE 0 END) / COUNT(*), 2) AS nodriver_pct,
  SUM(CASE WHEN status = 'Incomplete' THEN 1 ELSE 0 END) AS incomplete,
  SUM(CASE WHEN status = 'Completed' THEN 1 ELSE 0 END) AS completed,
  ROUND(AVG(CASE WHEN status = 'Completed' AND dist > 0 THEN value / dist END), 2) AS avg_cost_per_km,
  ROUND(AVG(CASE WHEN status = 'Completed' THEN dist END), 2) AS avg_dist_km
FROM parsed
GROUP BY hour
ORDER BY hour
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-021/attempt-01/sql/S20.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-021/attempt-01/sql/S20.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-021/attempt-01/results/S20.rows.jsonl)；完整：True；SHA256：`13030f951c0582cfbe584dc1d580a8e68d9c176454e3d64a8a9427634f3ca885`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "sheet1", "kind": "base", "block": null, "base_tables": ["sheet1"]}] | [] | [] |
| B2 | [{"alias": "parsed", "kind": "derived", "block": "B1", "base_tables": ["sheet1"]}] | [] | ["hour"] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B2 | COUNT(*) | [] | [] | True |
| B2 | SUM(CASE WHEN status IN ('Cancelled by Customer', 'Cancelled by Driver') THEN 1 ELSE 0 END) | [] | [{"table": "sheet1", "column": "Booking Status"}] | False |
| B2 | SUM(CASE WHEN status = 'No Driver Found' THEN 1 ELSE 0 END) | [] | [{"table": "sheet1", "column": "Booking Status"}] | False |
| B2 | SUM(CASE WHEN status = 'Incomplete' THEN 1 ELSE 0 END) | [] | [{"table": "sheet1", "column": "Booking Status"}] | False |
| B2 | SUM(CASE WHEN status = 'Completed' THEN 1 ELSE 0 END) | [] | [{"table": "sheet1", "column": "Booking Status"}] | False |
| B2 | AVG(CASE WHEN status = 'Completed' AND dist > 0 THEN value / dist END) | [{"table": "sheet1", "column": "Booking Value"}, {"table": "sheet1", "column": "Ride Distance"}] | [{"table": "sheet1", "column": "Booking Status"}, {"table": "sheet1", "column": "Ride Distance"}] | False |
| B2 | AVG(CASE WHEN status = 'Completed' THEN dist END) | [{"table": "sheet1", "column": "Ride Distance"}] | [{"table": "sheet1", "column": "Booking Status"}] | False |
| B2 | COUNT(*) | [] | [] | True |
| B2 | COUNT(*) | [] | [] | True |
| B2 | SUM(CASE WHEN status IN ('Cancelled by Customer', 'Cancelled by Driver') THEN 1 ELSE 0 END) | [] | [{"table": "sheet1", "column": "Booking Status"}] | False |
| B2 | SUM(CASE WHEN status = 'No Driver Found' THEN 1 ELSE 0 END) | [] | [{"table": "sheet1", "column": "Booking Status"}] | False |


## S21

类别 `data`；来源 `query_db`；调用 `4ce90b5ce2ee43f89e4eb4be77819b48`；状态 `success`。

```sql
WITH parsed AS (
  SELECT
    CAST(substr("Time", 1, instr("Time", ':')-1) AS INTEGER) AS hour,
    "Booking Status" AS status,
    "Booking Value" AS value,
    "Ride Distance" AS dist
  FROM sheet1
)
SELECT hour,
  COUNT(*) AS bookings,
  SUM(CASE WHEN status IN ('Cancelled by Customer','Cancelled by Driver') THEN 1 ELSE 0 END) AS cancellations,
  ROUND(100.0 * SUM(CASE WHEN status IN ('Cancelled by Customer','Cancelled by Driver') THEN 1 ELSE 0 END) / COUNT(*), 2) AS cancel_pct,
  SUM(CASE WHEN status = 'No Driver Found' THEN 1 ELSE 0 END) AS no_driver,
  ROUND(100.0 * SUM(CASE WHEN status = 'No Driver Found' THEN 1 ELSE 0 END) / COUNT(*), 2) AS nodriver_pct,
  SUM(CASE WHEN status = 'Incomplete' THEN 1 ELSE 0 END) AS incomplete,
  SUM(CASE WHEN status = 'Completed' THEN 1 ELSE 0 END) AS completed,
  ROUND(AVG(CASE WHEN status = 'Completed' AND dist > 0 THEN value / dist END), 2) AS avg_cost_per_km,
  ROUND(AVG(CASE WHEN status = 'Completed' THEN dist END), 2) AS avg_dist_km
FROM parsed
GROUP BY hour
ORDER BY hour
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-021/attempt-01/sql/S21.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-021/attempt-01/sql/S21.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-021/attempt-01/results/S21.rows.jsonl)；完整：True；SHA256：`13030f951c0582cfbe584dc1d580a8e68d9c176454e3d64a8a9427634f3ca885`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "sheet1", "kind": "base", "block": null, "base_tables": ["sheet1"]}] | [] | [] |
| B2 | [{"alias": "parsed", "kind": "derived", "block": "B1", "base_tables": ["sheet1"]}] | [] | ["hour"] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B2 | COUNT(*) | [] | [] | True |
| B2 | SUM(CASE WHEN status IN ('Cancelled by Customer', 'Cancelled by Driver') THEN 1 ELSE 0 END) | [] | [{"table": "sheet1", "column": "Booking Status"}] | False |
| B2 | SUM(CASE WHEN status = 'No Driver Found' THEN 1 ELSE 0 END) | [] | [{"table": "sheet1", "column": "Booking Status"}] | False |
| B2 | SUM(CASE WHEN status = 'Incomplete' THEN 1 ELSE 0 END) | [] | [{"table": "sheet1", "column": "Booking Status"}] | False |
| B2 | SUM(CASE WHEN status = 'Completed' THEN 1 ELSE 0 END) | [] | [{"table": "sheet1", "column": "Booking Status"}] | False |
| B2 | AVG(CASE WHEN status = 'Completed' AND dist > 0 THEN value / dist END) | [{"table": "sheet1", "column": "Booking Value"}, {"table": "sheet1", "column": "Ride Distance"}] | [{"table": "sheet1", "column": "Booking Status"}, {"table": "sheet1", "column": "Ride Distance"}] | False |
| B2 | AVG(CASE WHEN status = 'Completed' THEN dist END) | [{"table": "sheet1", "column": "Ride Distance"}] | [{"table": "sheet1", "column": "Booking Status"}] | False |
| B2 | COUNT(*) | [] | [] | True |
| B2 | COUNT(*) | [] | [] | True |
| B2 | SUM(CASE WHEN status IN ('Cancelled by Customer', 'Cancelled by Driver') THEN 1 ELSE 0 END) | [] | [{"table": "sheet1", "column": "Booking Status"}] | False |
| B2 | SUM(CASE WHEN status = 'No Driver Found' THEN 1 ELSE 0 END) | [] | [{"table": "sheet1", "column": "Booking Status"}] | False |


## S22

类别 `data`；来源 `query_db`；调用 `b38768528a614d0095386c35b4950301`；状态 `success`。

```sql
WITH parsed AS (
  SELECT
    printf('%04d-%02d-%02d',
           CAST(substr("Date",1,4) AS INTEGER),
           CAST(substr("Date", instr("Date",'/')+1, instr(substr("Date", instr("Date",'/')+1),'/')-1) AS INTEGER),
           CAST(substr("Date", instr("Date",'/')+instr(substr("Date", instr("Date",'/')+1),'/')+1) AS INTEGER)) AS date_key
  FROM sheet1
)
SELECT date_key, COUNT(*) AS bookings
FROM parsed
GROUP BY date_key
ORDER BY bookings ASC
LIMIT 15
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-021/attempt-01/sql/S22.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-021/attempt-01/sql/S22.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-021/attempt-01/results/S22.rows.jsonl)；完整：True；SHA256：`d73524518e23c97d8c26e2e62b00e0f11521f935f3c636bf2aa5dafdac52b30f`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "sheet1", "kind": "base", "block": null, "base_tables": ["sheet1"]}] | [] | [] |
| B2 | [{"alias": "parsed", "kind": "derived", "block": "B1", "base_tables": ["sheet1"]}] | [] | ["date_key"] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B2 | COUNT(*) | [] | [] | True |


## S23

类别 `data`；来源 `python`；调用 `fca9ee3bc7184d6b92a112ff40737e00`；状态 `success`。

```sql

WITH parsed AS (
  SELECT
    printf('%04d-%02d-%02d',
           CAST(substr("Date",1,4) AS INTEGER),
           CAST(substr("Date", instr("Date",'/')+1, instr(substr("Date", instr("Date",'/')+1),'/')-1) AS INTEGER),
           CAST(substr("Date", instr("Date",'/')+instr(substr("Date", instr("Date",'/')+1),'/')+1) AS INTEGER)) AS date_key,
    "Booking Status" AS status,
    "Booking Value" AS value,
    "Ride Distance" AS dist
  FROM sheet1
)
SELECT date_key,
  COUNT(*) AS bookings,
  SUM(CASE WHEN status IN ('Cancelled by Customer','Cancelled by Driver') THEN 1 ELSE 0 END) AS cancellations,
  SUM(CASE WHEN status = 'No Driver Found' THEN 1 ELSE 0 END) AS no_driver,
  SUM(CASE WHEN status = 'Incomplete' THEN 1 ELSE 0 END) AS incomplete,
  SUM(CASE WHEN status = 'Completed' THEN 1 ELSE 0 END) AS completed,
  ROUND(AVG(CASE WHEN status = 'Completed' AND dist > 0 THEN value / dist END), 4) AS cost_per_km
FROM parsed
GROUP BY date_key
ORDER BY date_key

```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-021/attempt-01/sql/S23.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-021/attempt-01/sql/S23.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-021/attempt-01/results/S23.rows.jsonl)；完整：True；SHA256：`2889269ede4b79b87b645f43ddda471465510c24e8db0282ac0a20f49b80b742`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "sheet1", "kind": "base", "block": null, "base_tables": ["sheet1"]}] | [] | [] |
| B2 | [{"alias": "parsed", "kind": "derived", "block": "B1", "base_tables": ["sheet1"]}] | [] | ["date_key"] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B2 | COUNT(*) | [] | [] | True |
| B2 | SUM(CASE WHEN status IN ('Cancelled by Customer', 'Cancelled by Driver') THEN 1 ELSE 0 END) | [] | [{"table": "sheet1", "column": "Booking Status"}] | False |
| B2 | SUM(CASE WHEN status = 'No Driver Found' THEN 1 ELSE 0 END) | [] | [{"table": "sheet1", "column": "Booking Status"}] | False |
| B2 | SUM(CASE WHEN status = 'Incomplete' THEN 1 ELSE 0 END) | [] | [{"table": "sheet1", "column": "Booking Status"}] | False |
| B2 | SUM(CASE WHEN status = 'Completed' THEN 1 ELSE 0 END) | [] | [{"table": "sheet1", "column": "Booking Status"}] | False |
| B2 | AVG(CASE WHEN status = 'Completed' AND dist > 0 THEN value / dist END) | [{"table": "sheet1", "column": "Booking Value"}, {"table": "sheet1", "column": "Ride Distance"}] | [{"table": "sheet1", "column": "Booking Status"}, {"table": "sheet1", "column": "Ride Distance"}] | False |


## S24

类别 `data`；来源 `python`；调用 `fca9ee3bc7184d6b92a112ff40737e00`；状态 `success`。

```sql

WITH parsed AS (
  SELECT
    CAST(substr("Time", 1, instr("Time", ':')-1) AS INTEGER) AS hour,
    "Booking Status" AS status,
    "Booking Value" AS value,
    "Ride Distance" AS dist
  FROM sheet1
)
SELECT hour,
  COUNT(*) AS bookings,
  SUM(CASE WHEN status IN ('Cancelled by Customer','Cancelled by Driver') THEN 1 ELSE 0 END) AS cancellations,
  SUM(CASE WHEN status = 'No Driver Found' THEN 1 ELSE 0 END) AS no_driver,
  SUM(CASE WHEN status = 'Incomplete' THEN 1 ELSE 0 END) AS incomplete,
  SUM(CASE WHEN status = 'Completed' THEN 1 ELSE 0 END) AS completed,
  AVG(CASE WHEN status = 'Completed' AND dist > 0 THEN value / dist END) AS cost_per_km
FROM parsed
GROUP BY hour
ORDER BY hour

```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-021/attempt-01/sql/S24.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-021/attempt-01/sql/S24.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-021/attempt-01/results/S24.rows.jsonl)；完整：True；SHA256：`378421715228c2fefcee52dcade167f62f8b74c8a8f2223c2ab50b36350ba399`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "sheet1", "kind": "base", "block": null, "base_tables": ["sheet1"]}] | [] | [] |
| B2 | [{"alias": "parsed", "kind": "derived", "block": "B1", "base_tables": ["sheet1"]}] | [] | ["hour"] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B2 | COUNT(*) | [] | [] | True |
| B2 | SUM(CASE WHEN status IN ('Cancelled by Customer', 'Cancelled by Driver') THEN 1 ELSE 0 END) | [] | [{"table": "sheet1", "column": "Booking Status"}] | False |
| B2 | SUM(CASE WHEN status = 'No Driver Found' THEN 1 ELSE 0 END) | [] | [{"table": "sheet1", "column": "Booking Status"}] | False |
| B2 | SUM(CASE WHEN status = 'Incomplete' THEN 1 ELSE 0 END) | [] | [{"table": "sheet1", "column": "Booking Status"}] | False |
| B2 | SUM(CASE WHEN status = 'Completed' THEN 1 ELSE 0 END) | [] | [{"table": "sheet1", "column": "Booking Status"}] | False |
| B2 | AVG(CASE WHEN status = 'Completed' AND dist > 0 THEN value / dist END) | [{"table": "sheet1", "column": "Booking Value"}, {"table": "sheet1", "column": "Ride Distance"}] | [{"table": "sheet1", "column": "Booking Status"}, {"table": "sheet1", "column": "Ride Distance"}] | False |


## S25

类别 `data`；来源 `query_db`；调用 `62c7f4cec6d9468fa6a0adb0b6f8ffdc`；状态 `success`。

```sql
WITH parsed AS (
  SELECT
    CAST(strftime('%w', printf('%04d-%02d-%02d',
           CAST(substr("Date",1,4) AS INTEGER),
           CAST(substr("Date", instr("Date",'/')+1, instr(substr("Date", instr("Date",'/')+1),'/')-1) AS INTEGER),
           CAST(substr("Date", instr("Date",'/')+instr(substr("Date", instr("Date",'/')+1),'/')+1) AS INTEGER))) AS INTEGER) AS dow,
    "Vehicle Type" AS vtype,
    "Booking Status" AS status,
    "Booking Value" AS value,
    "Ride Distance" AS dist,
    "Payment Method" AS pay
  FROM sheet1
  WHERE "Booking Status" = 'Completed'
)
SELECT
  CASE dow WHEN 0 THEN 'Sun' WHEN 1 THEN 'Mon' WHEN 2 THEN 'Tue' WHEN 3 THEN 'Wed' WHEN 4 THEN 'Thu' WHEN 5 THEN 'Fri' WHEN 6 THEN 'Sat' END AS weekday,
  ROUND(AVG(dist), 2) AS avg_dist_km,
  ROUND(AVG(value), 2) AS avg_value,
  ROUND(AVG(value / NULLIF(dist, 0)), 2) AS avg_cost_per_km,
  COUNT(*) AS completed_rides,
  ROUND(100.0 * COUNT(*) / SUM(COUNT(*)) OVER (), 2) AS pct_of_completed
FROM parsed
GROUP BY dow
ORDER BY dow
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-021/attempt-01/sql/S25.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-021/attempt-01/sql/S25.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-021/attempt-01/results/S25.rows.jsonl)；完整：True；SHA256：`07e6badf396348855ca0dc98a5c6ede704b721a33ed609bf74ba569aa549223b`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "sheet1", "kind": "base", "block": null, "base_tables": ["sheet1"]}] | [] | [] |
| B2 | [{"alias": "parsed", "kind": "derived", "block": "B1", "base_tables": ["sheet1"]}] | [] | ["dow"] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B2 | COUNT(*) | [] | [] | True |
| B2 | AVG(dist) | [{"table": "sheet1", "column": "Ride Distance"}] | [] | False |
| B2 | AVG(value) | [{"table": "sheet1", "column": "Booking Value"}] | [] | False |
| B2 | AVG(value / NULLIF(dist, 0)) | [{"table": "sheet1", "column": "Booking Value"}, {"table": "sheet1", "column": "Ride Distance"}] | [] | False |
| B2 | COUNT(*) | [] | [] | True |
| B2 | COUNT(*) | [] | [] | True |


## S26

类别 `data`；来源 `query_db`；调用 `cbb2dff326844815b60b675c003185aa`；状态 `success`。

```sql
WITH parsed AS (
  SELECT
    CAST(strftime('%w', printf('%04d-%02d-%02d',
           CAST(substr("Date",1,4) AS INTEGER),
           CAST(substr("Date", instr("Date",'/')+1, instr(substr("Date", instr("Date",'/')+1),'/')-1) AS INTEGER),
           CAST(substr("Date", instr("Date",'/')+instr(substr("Date", instr("Date",'/')+1),'/')+1) AS INTEGER))) AS INTEGER) AS dow,
    "Vehicle Type" AS vtype,
    "Booking Status" AS status,
    "Booking Value" AS value,
    "Ride Distance" AS dist
  FROM sheet1
  WHERE "Booking Status" = 'Completed'
)
SELECT
  CASE dow WHEN 0 THEN 'Sun' WHEN 1 THEN 'Mon' WHEN 2 THEN 'Tue' WHEN 3 THEN 'Wed' WHEN 4 THEN 'Thu' WHEN 5 THEN 'Fri' WHEN 6 THEN 'Sat' END AS weekday,
  vtype,
  COUNT(*) AS n,
  ROUND(AVG(dist), 2) AS avg_dist,
  ROUND(AVG(value / NULLIF(dist, 0)), 2) AS avg_cost_per_km
FROM parsed
GROUP BY dow, vtype
ORDER BY dow, n DESC
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-021/attempt-01/sql/S26.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-021/attempt-01/sql/S26.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-021/attempt-01/results/S26.rows.jsonl)；完整：True；SHA256：`4c2d84fc8b1f78f4b909f455f37540db00198cfcec49532280d01b513e42da57`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "sheet1", "kind": "base", "block": null, "base_tables": ["sheet1"]}] | [] | [] |
| B2 | [{"alias": "parsed", "kind": "derived", "block": "B1", "base_tables": ["sheet1"]}] | [] | ["dow", "vtype"] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B2 | COUNT(*) | [] | [] | True |
| B2 | AVG(dist) | [{"table": "sheet1", "column": "Ride Distance"}] | [] | False |
| B2 | AVG(value / NULLIF(dist, 0)) | [{"table": "sheet1", "column": "Booking Value"}, {"table": "sheet1", "column": "Ride Distance"}] | [] | False |


## S27

类别 `data`；来源 `query_db`；调用 `42b6f0948b03432cbd49b04870eea64c`；状态 `success`。

```sql
WITH parsed AS (
  SELECT
    CAST(substr("Time", 1, instr("Time", ':')-1) AS INTEGER) AS hour,
    "Booking Status" AS status,
    "Booking Value" AS value,
    "Ride Distance" AS dist,
    "Cancelled Rides by Customer" AS cc,
    "Cancelled Rides by Driver" AS cd
  FROM sheet1
)
SELECT
  CASE
    WHEN hour BETWEEN 0 AND 4 THEN 'Late-night trough (0-4)'
    WHEN hour BETWEEN 5 AND 8 THEN 'Early morning (5-8)'
    WHEN hour BETWEEN 9 AND 11 THEN 'Morning peak (9-11)'
    WHEN hour BETWEEN 12 AND 14 THEN 'Midday dip (12-14)'
    WHEN hour BETWEEN 15 AND 16 THEN 'Late afternoon (15-16)'
    WHEN hour BETWEEN 17 AND 20 THEN 'Evening peak (17-20)'
    ELSE 'Late evening (21-23)'
  END AS period,
  COUNT(*) AS bookings,
  ROUND(100.0*SUM(CASE WHEN status IN ('Cancelled by Customer','Cancelled by Driver') THEN 1 ELSE 0 END)/COUNT(*),2) AS cancel_pct,
  ROUND(100.0*SUM(CASE WHEN status='Cancelled by Customer' THEN 1 ELSE 0 END)/COUNT(*),2) AS cust_cancel_pct,
  ROUND(100.0*SUM(CASE WHEN status='Cancelled by Driver' THEN 1 ELSE 0 END)/COUNT(*),2) AS drv_cancel_pct,
  ROUND(100.0*SUM(CASE WHEN status='No Driver Found' THEN 1 ELSE 0 END)/COUNT(*),2) AS no_driver_pct,
  ROUND(100.0*SUM(CASE WHEN status='Incomplete' THEN 1 ELSE 0 END)/COUNT(*),2) AS incomplete_pct,
  ROUND(AVG(CASE WHEN status='Completed' AND dist>0 THEN value/dist END),2) AS cost_per_km
FROM parsed
GROUP BY period
ORDER BY MIN(hour)
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-021/attempt-01/sql/S27.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-021/attempt-01/sql/S27.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-021/attempt-01/results/S27.rows.jsonl)；完整：True；SHA256：`feb6f7d65117407954c1b2e2cad7925e41e65270b549af9641ed5c7031ce449b`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "sheet1", "kind": "base", "block": null, "base_tables": ["sheet1"]}] | [] | [] |
| B2 | [{"alias": "parsed", "kind": "derived", "block": "B1", "base_tables": ["sheet1"]}] | [] | ["CASE WHEN hour BETWEEN 0 AND 4 THEN 'Late-night trough (0-4)' WHEN hour BETWEEN 5 AND 8 THEN 'Early morning (5-8)' WHEN hour BETWEEN 9 AND 11 THEN 'Morning peak (9-11)' WHEN hour BETWEEN 12 AND 14 THEN 'Midday dip (12-14)' WHEN hour BETWEEN 15 AND 16 THEN 'Late afternoon (15-16)' WHEN hour BETWEEN 17 AND 20 THEN 'Evening peak (17-20)' ELSE 'Late evening (21-23)' END"] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B2 | COUNT(*) | [] | [] | True |
| B2 | AVG(CASE WHEN status = 'Completed' AND dist > 0 THEN value / dist END) | [{"table": "sheet1", "column": "Booking Value"}, {"table": "sheet1", "column": "Ride Distance"}] | [{"table": "sheet1", "column": "Booking Status"}, {"table": "sheet1", "column": "Ride Distance"}] | False |
| B2 | MIN(hour) | [{"table": "sheet1", "column": "Time"}, {"table": "sheet1", "column": "Time"}] | [] | False |
| B2 | COUNT(*) | [] | [] | True |
| B2 | COUNT(*) | [] | [] | True |
| B2 | COUNT(*) | [] | [] | True |
| B2 | COUNT(*) | [] | [] | True |
| B2 | COUNT(*) | [] | [] | True |
| B2 | SUM(CASE WHEN status IN ('Cancelled by Customer', 'Cancelled by Driver') THEN 1 ELSE 0 END) | [] | [{"table": "sheet1", "column": "Booking Status"}] | False |
| B2 | SUM(CASE WHEN status = 'Cancelled by Customer' THEN 1 ELSE 0 END) | [] | [{"table": "sheet1", "column": "Booking Status"}] | False |
| B2 | SUM(CASE WHEN status = 'Cancelled by Driver' THEN 1 ELSE 0 END) | [] | [{"table": "sheet1", "column": "Booking Status"}] | False |
| B2 | SUM(CASE WHEN status = 'No Driver Found' THEN 1 ELSE 0 END) | [] | [{"table": "sheet1", "column": "Booking Status"}] | False |
| B2 | SUM(CASE WHEN status = 'Incomplete' THEN 1 ELSE 0 END) | [] | [{"table": "sheet1", "column": "Booking Status"}] | False |


## S28

类别 `data`；来源 `query_db`；调用 `2b96ec090e7448e2aedf798d26977289`；状态 `success`。

```sql
SELECT "Reason for cancelling by Customer" AS reason, COUNT(*) AS n
FROM sheet1
WHERE "Cancelled Rides by Customer" = 1
GROUP BY reason
ORDER BY n DESC
LIMIT 12
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-021/attempt-01/sql/S28.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-021/attempt-01/sql/S28.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-021/attempt-01/results/S28.rows.jsonl)；完整：True；SHA256：`4f212c68cb95af50f671b47d8dea4b8cdcdddf8cf281f7759ebe57fd8fb42e26`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "sheet1", "kind": "base", "block": null, "base_tables": ["sheet1"]}] | [] | ["\"Reason for cancelling by Customer\""] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |


## S29

类别 `data`；来源 `query_db`；调用 `8c80ef4207b846d4a1648f105fd7d1f8`；状态 `success`。

```sql
SELECT "Driver Cancellation Reason" AS reason, COUNT(*) AS n
FROM sheet1
WHERE "Cancelled Rides by Driver" = 1
GROUP BY reason
ORDER BY n DESC
LIMIT 12
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-021/attempt-01/sql/S29.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-021/attempt-01/sql/S29.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-021/attempt-01/results/S29.rows.jsonl)；完整：True；SHA256：`76f27150ff7b7aeabdaec7a8c6136d0b9c75ecd28741d6d14e716ca51aaa518d`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "sheet1", "kind": "base", "block": null, "base_tables": ["sheet1"]}] | [] | ["\"Driver Cancellation Reason\""] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |


## S30

类别 `data`；来源 `python`；调用 `207b0f22ef7246e69fdd8a6ed91b4941`；状态 `success`。

```sql

WITH parsed AS (
  SELECT
    CAST(strftime('%w', printf('%04d-%02d-%02d',
           CAST(substr("Date",1,4) AS INTEGER),
           CAST(substr("Date", instr("Date",'/')+1, instr(substr("Date", instr("Date",'/')+1),'/')-1) AS INTEGER),
           CAST(substr("Date", instr("Date",'/')+instr(substr("Date", instr("Date",'/')+1),'/')+1) AS INTEGER))) AS INTEGER) AS dow,
    CAST(substr("Time", 1, instr("Time", ':')-1) AS INTEGER) AS hour,
    "Booking Status" AS status,
    "Booking Value" AS value,
    "Ride Distance" AS dist
  FROM sheet1
)
SELECT dow, hour, COUNT(*) AS bookings,
  ROUND(100.0 * SUM(CASE WHEN status IN ('Cancelled by Customer','Cancelled by Driver') THEN 1 ELSE 0 END) / COUNT(*), 2) AS cancel_pct,
  ROUND(AVG(CASE WHEN status = 'Completed' AND dist > 0 THEN value / dist END), 2) AS cost_per_km
FROM parsed
GROUP BY dow, hour
ORDER BY dow, hour

```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-021/attempt-01/sql/S30.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-021/attempt-01/sql/S30.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-021/attempt-01/results/S30.rows.jsonl)；完整：True；SHA256：`44375b3f1d33faa92b50de6f82ab348051eeb0da41ce386207db7655d6178031`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "sheet1", "kind": "base", "block": null, "base_tables": ["sheet1"]}] | [] | [] |
| B2 | [{"alias": "parsed", "kind": "derived", "block": "B1", "base_tables": ["sheet1"]}] | [] | ["dow", "hour"] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B2 | COUNT(*) | [] | [] | True |
| B2 | AVG(CASE WHEN status = 'Completed' AND dist > 0 THEN value / dist END) | [{"table": "sheet1", "column": "Booking Value"}, {"table": "sheet1", "column": "Ride Distance"}] | [{"table": "sheet1", "column": "Booking Status"}, {"table": "sheet1", "column": "Ride Distance"}] | False |
| B2 | COUNT(*) | [] | [] | True |
| B2 | SUM(CASE WHEN status IN ('Cancelled by Customer', 'Cancelled by Driver') THEN 1 ELSE 0 END) | [] | [{"table": "sheet1", "column": "Booking Status"}] | False |


## S31

类别 `data`；来源 `python`；调用 `207b0f22ef7246e69fdd8a6ed91b4941`；状态 `success`。

```sql

WITH parsed AS (
  SELECT
    CAST(substr("Time", 1, instr("Time", ':')-1) AS INTEGER) AS hour,
    "Booking Status" AS status
  FROM sheet1
)
SELECT hour,
  COUNT(*) AS total,
  SUM(CASE WHEN status = 'Cancelled by Customer' THEN 1 ELSE 0 END) AS cust_cancel,
  SUM(CASE WHEN status = 'Cancelled by Driver' THEN 1 ELSE 0 END) AS drv_cancel
FROM parsed
GROUP BY hour
ORDER BY hour

```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-021/attempt-01/sql/S31.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-021/attempt-01/sql/S31.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-021/attempt-01/results/S31.rows.jsonl)；完整：True；SHA256：`c1768ddcd74143723c1b989c8cb8f083ccbf5c0e7a3b0b1a8e0c6c79e8c7c9c8`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "sheet1", "kind": "base", "block": null, "base_tables": ["sheet1"]}] | [] | [] |
| B2 | [{"alias": "parsed", "kind": "derived", "block": "B1", "base_tables": ["sheet1"]}] | [] | ["hour"] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B2 | COUNT(*) | [] | [] | True |
| B2 | SUM(CASE WHEN status = 'Cancelled by Customer' THEN 1 ELSE 0 END) | [] | [{"table": "sheet1", "column": "Booking Status"}] | False |
| B2 | SUM(CASE WHEN status = 'Cancelled by Driver' THEN 1 ELSE 0 END) | [] | [{"table": "sheet1", "column": "Booking Status"}] | False |


## S32

类别 `data`；来源 `query_db`；调用 `9f985e7ae48e454296f3c29da42cb7b0`；状态 `success`。

```sql
WITH parsed AS (
  SELECT
    printf('%04d-%02d-%02d',
           CAST(substr("Date",1,4) AS INTEGER),
           CAST(substr("Date", instr("Date",'/')+1, instr(substr("Date", instr("Date",'/')+1),'/')-1) AS INTEGER),
           CAST(substr("Date", instr("Date",'/')+instr(substr("Date", instr("Date",'/')+1),'/')+1) AS INTEGER)) AS date_key,
    "Booking Status" AS status,
    "Booking Value" AS value,
    "Ride Distance" AS dist
  FROM sheet1
),
daily_agg AS (
  SELECT date_key,
    COUNT(*) AS bookings,
    ROUND(100.0*SUM(CASE WHEN status IN ('Cancelled by Customer','Cancelled by Driver') THEN 1 ELSE 0 END)/COUNT(*),2) AS cancel_pct,
    ROUND(AVG(CASE WHEN status='Completed' AND dist>0 THEN value/dist END),2) AS cost_per_km
  FROM parsed
  GROUP BY date_key
)
SELECT date_key,
  CASE CAST(strftime('%w', date_key) AS INTEGER)
    WHEN 0 THEN 'Sun' WHEN 1 THEN 'Mon' WHEN 2 THEN 'Tue' WHEN 3 THEN 'Wed'
    WHEN 4 THEN 'Thu' WHEN 5 THEN 'Fri' WHEN 6 THEN 'Sat' END AS dow,
  bookings, cancel_pct, cost_per_km
FROM daily_agg
ORDER BY bookings DESC
LIMIT 10
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-021/attempt-01/sql/S32.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-021/attempt-01/sql/S32.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-021/attempt-01/results/S32.rows.jsonl)；完整：True；SHA256：`739b65fbfd2db234f72e84fffe10506dee111c9e75f2ae64cae590daf358e506`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "sheet1", "kind": "base", "block": null, "base_tables": ["sheet1"]}] | [] | [] |
| B2 | [{"alias": "parsed", "kind": "derived", "block": "B1", "base_tables": ["sheet1"]}] | [] | ["date_key"] |
| B3 | [{"alias": "daily_agg", "kind": "derived", "block": "B2", "base_tables": ["sheet1"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B2 | COUNT(*) | [] | [] | True |
| B2 | AVG(CASE WHEN status = 'Completed' AND dist > 0 THEN value / dist END) | [{"table": "sheet1", "column": "Booking Value"}, {"table": "sheet1", "column": "Ride Distance"}] | [{"table": "sheet1", "column": "Booking Status"}, {"table": "sheet1", "column": "Ride Distance"}] | False |
| B2 | COUNT(*) | [] | [] | True |
| B2 | SUM(CASE WHEN status IN ('Cancelled by Customer', 'Cancelled by Driver') THEN 1 ELSE 0 END) | [] | [{"table": "sheet1", "column": "Booking Status"}] | False |


## S33

类别 `data`；来源 `query_db`；调用 `749ff51bcd3a468683417c9131e8e948`；状态 `success`。

```sql
WITH parsed AS (
  SELECT
    printf('%04d-%02d-%02d',
           CAST(substr("Date",1,4) AS INTEGER),
           CAST(substr("Date", instr("Date",'/')+1, instr(substr("Date", instr("Date",'/')+1),'/')-1) AS INTEGER),
           CAST(substr("Date", instr("Date",'/')+instr(substr("Date", instr("Date",'/')+1),'/')+1) AS INTEGER)) AS date_key,
    "Booking Status" AS status,
    "Booking Value" AS value,
    "Ride Distance" AS dist
  FROM sheet1
),
daily_agg AS (
  SELECT date_key,
    COUNT(*) AS bookings,
    ROUND(100.0*SUM(CASE WHEN status IN ('Cancelled by Customer','Cancelled by Driver') THEN 1 ELSE 0 END)/COUNT(*),2) AS cancel_pct,
    ROUND(AVG(CASE WHEN status='Completed' AND dist>0 THEN value/dist END),2) AS cost_per_km
  FROM parsed
  GROUP BY date_key
)
SELECT date_key,
  CASE CAST(strftime('%w', date_key) AS INTEGER)
    WHEN 0 THEN 'Sun' WHEN 1 THEN 'Mon' WHEN 2 THEN 'Tue' WHEN 3 THEN 'Wed'
    WHEN 4 THEN 'Thu' WHEN 5 THEN 'Fri' WHEN 6 THEN 'Sat' END AS dow,
  bookings, cancel_pct, cost_per_km
FROM daily_agg
ORDER BY bookings ASC
LIMIT 10
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-021/attempt-01/sql/S33.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-021/attempt-01/sql/S33.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-021/attempt-01/results/S33.rows.jsonl)；完整：True；SHA256：`e57ca9903eeb2efeb413bbb2106caf0401ad4a978d7c65f9bb2a641e065d27b1`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "sheet1", "kind": "base", "block": null, "base_tables": ["sheet1"]}] | [] | [] |
| B2 | [{"alias": "parsed", "kind": "derived", "block": "B1", "base_tables": ["sheet1"]}] | [] | ["date_key"] |
| B3 | [{"alias": "daily_agg", "kind": "derived", "block": "B2", "base_tables": ["sheet1"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B2 | COUNT(*) | [] | [] | True |
| B2 | AVG(CASE WHEN status = 'Completed' AND dist > 0 THEN value / dist END) | [{"table": "sheet1", "column": "Booking Value"}, {"table": "sheet1", "column": "Ride Distance"}] | [{"table": "sheet1", "column": "Booking Status"}, {"table": "sheet1", "column": "Ride Distance"}] | False |
| B2 | COUNT(*) | [] | [] | True |
| B2 | SUM(CASE WHEN status IN ('Cancelled by Customer', 'Cancelled by Driver') THEN 1 ELSE 0 END) | [] | [{"table": "sheet1", "column": "Booking Status"}] | False |

