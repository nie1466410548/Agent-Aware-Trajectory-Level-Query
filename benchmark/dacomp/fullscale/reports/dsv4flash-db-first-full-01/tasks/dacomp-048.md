# dacomp-048

Please separately compute the starting salary distribution and the benefits distribution f…

运行：已提交。官方未评分。全部 SQL 尝试/成功 37/37；数据 SQL 35/35；Python 10 次。

完整原题：

Please separately compute the starting salary distribution and the benefits distribution for vocational school graduates. Which qualities can significantly increase their starting salaries?

| 表 | 行数 | 列数 |
| --- | --- | --- |
| sheet1 | 100077 | 19 |


实际路线（分析者依据 SQL/源码概括，不代表 Agent 自述）：SQL 筛选职业教育岗位并汇总 → Python 清洗薪资、分组均值和福利比较 → 统计检验与图表。

数据库大小：317,820,928 字节。

## 数据 SQL

| SQL | 状态 | 基础表 | Join 输入/类型 | GROUP BY | 聚合表达式 | 结果行数 | 数据库 ms |
| --- | --- | --- | --- | --- | --- | --- | --- |
| [S3/Q1](#s3) | success | ["sheet1"] | 0 / {} | [] | [] | 10 | 0.378 |
| [S4/Q2](#s4) | success | ["sheet1"] | 0 / {} | [] | [] | 9 | 79.638 |
| [S5/Q3](#s5) | success | ["sheet1"] | 0 / {} | [] | ["COUNT(*)"] | 1 | 65.848 |
| [S6/Q4](#s6) | success | ["sheet1"] | 0 / {} | ["\"Education Requirement\""] | ["COUNT(*)"] | 9 | 110.173 |
| [S7/Q5](#s7) | success | ["sheet1"] | 0 / {} | [] | ["COUNT(*)"] | 1 | 84.945 |
| [S8/Q6](#s8) | success | ["sheet1"] | 0 / {} | ["\"Salary Range\""] | ["COUNT(*)"] | 30 | 78.685 |
| [S9/Q7](#s9) | success | ["sheet1"] | 0 / {} | ["\"Benefits\""] | ["COUNT(*)"] | 30 | 81.979 |
| [S10/Q8](#s10) | success | ["sheet1"] | 0 / {} | [] | ["COUNT(*)", "SUM(CASE WHEN NOT \"Salary Range\" IS NULL AND \"Salary Range\" <> '' THEN 1 ELSE 0 END)", "SUM(CASE WHEN NOT \"Benefits\" IS NULL AND \"Benefits\" <> '' THEN 1 ELSE 0 END)"] | 1 | 76.052 |
| [S11/Q9](#s11) | success | ["sheet1"] | 0 / {} | ["\"Salary Range\""] | ["COUNT(*)"] | 0 | 75.719 |
| [S12/Q10](#s12) | success | ["sheet1"] | 0 / {} | ["\"Salary Range\""] | ["COUNT(*)"] | 50 | 78.988 |
| [S13/Q11](#s13) | success | ["sheet1"] | 0 / {} | ["\"Salary Range\""] | ["COUNT(*)"] | 0 | 78.116 |
| [S14/Q12](#s14) | success | ["sheet1"] | 0 / {} | ["\"Salary Range\""] | ["COUNT(*)"] | 0 | 75.93 |
| [S15/Q13](#s15) | success | ["sheet1"] | 0 / {} | ["\"Salary Range\""] | ["COUNT(*)"] | 20 | 77.068 |
| [S16/Q14](#s16) | success | ["sheet1"] | 0 / {} | ["\"Salary Range\""] | ["COUNT(*)"] | 0 | 75.251 |
| [S17/Q15](#s17) | success | ["sheet1"] | 0 / {} | [] | ["COUNT(DISTINCT \"Salary Range\")"] | 1 | 79.682 |
| [S18/Q16](#s18) | success | ["sheet1"] | 0 / {} | [] | [] | 20 | 0.699 |
| [S19/Q17](#s19) | success | ["sheet1"] | 0 / {} | [] | [] | 20 | 0.465 |
| [S20/Q18](#s20) | success | ["sheet1"] | 0 / {} | [] | [] | 0 | 75.283 |
| [S21/Q19](#s21) | success | ["sheet1"] | 0 / {} | [] | ["COUNT(*)", "SUM(CASE WHEN salary_min IS NULL OR salary_max IS NULL THEN 1 ELSE 0 END)", "MIN(salary_min)", "MAX(salary_max)", "AVG(salary_min)", "AVG(salary_max)", "AVG((salary_min + salary_max) / 2.0)"] | 1 | 107.473 |
| [S22/Q20](#s22) | success | ["sheet1"] | 0 / {} | [] | [] | 3 | 79.637 |
| [S23/Q21](#s23) | success | ["sheet1"] | 0 / {} | [] | [] | 2 | 80.048 |
| [S24/Q22](#s24) | success | ["sheet1"] | 0 / {} | ["\"Work Experience Requirement\""] | ["COUNT(*)", "AVG((salary_min + salary_max) / 2.0)", "MIN(salary_min)", "MAX(salary_max)", "AVG(salary_min)", "AVG(salary_max)"] | 19 | 101.681 |
| [S25/Q23](#s25) | success | ["sheet1"] | 0 / {} | ["\"Foreign Language Requirement\""] | ["COUNT(*)", "AVG((salary_min + salary_max) / 2.0)"] | 20 | 84.226 |
| [S26/Q24](#s26) | success | ["sheet1"] | 0 / {} | ["\"Work Experience Requirement\""] | ["COUNT(*)", "AVG((salary_min + salary_max) / 2.0)"] | 19 | 84.739 |
| [S27/Q25](#s27) | success | ["sheet1"] | 0 / {} | ["\"Gender Requirement\""] | ["COUNT(*)", "AVG((salary_min + salary_max) / 2.0)", "AVG(salary_min)", "AVG(salary_max)"] | 3 | 93.334 |
| [S28/Q26](#s28) | success | ["sheet1"] | 0 / {} | ["\"Employment Type\""] | ["COUNT(*)", "AVG((salary_min + salary_max) / 2.0)"] | 1 | 85.729 |
| [S29/Q27](#s29) | success | ["sheet1"] | 0 / {} | ["\"Company Type\""] | ["COUNT(*)", "AVG((salary_min + salary_max) / 2.0)"] | 15 | 86.284 |
| [S30/Q28](#s30) | success | ["sheet1"] | 0 / {} | [] | ["COUNT(DISTINCT \"Benefits\")"] | 1 | 101.188 |
| [S31/Q29](#s31) | success | ["sheet1"] | 0 / {} | ["\"Industry\""] | ["COUNT(*)", "AVG((salary_min + salary_max) / 2.0)"] | 25 | 99.082 |
| [S32/Q30](#s32) | success | ["sheet1"] | 0 / {} | [] | ["SUM(CASE WHEN \"Benefits\" LIKE '%Five social insurances%' THEN 1 ELSE 0 END)", "SUM(CASE WHEN \"Benefits\" LIKE '%housing provident fund%' OR \"Benefits\" LIKE '%housing fund%' THEN 1 ELSE 0 END)", "SUM(CASE WHEN \"Benefits\" LIKE '%commercial insurance%' THEN 1 ELSE 0 END)", "SUM(CASE WHEN \"Benefits\" LIKE '%paid annual leave%' THEN 1 ELSE 0 END)", "SUM(CASE WHEN \"Benefits\" LIKE '%double pay at the end%' OR \"Benefits\" LIKE '%double salary at the end%' THEN 1 ELSE 0 END)", "SUM(CASE WHEN \"Benefits\" LIKE '%performance bonus%' THEN 1 ELSE 0 END)", "SUM(CASE WHEN \"Benefits\" LIKE '%year-end bonus%' OR \"Benefits\" LIKE '%year end bonus%' THEN 1 ELSE 0 END)", "SUM(CASE WHEN \"Benefits\" LIKE '%meal allowance%' OR \"Benefits\" LIKE '%meal subsidy%' OR \"Benefits\" LIKE '%food allowance%' THEN 1 ELSE 0 END)", "SUM(CASE WHEN \"Benefits\" LIKE '%accommodation%' OR \"Benefits\" LIKE '%housing%' THEN 1 ELSE 0 END)", "SUM(CASE WHEN \"Benefits\" LIKE '%meals provided%' OR \"Benefits\" LIKE '%meals and accommodation provided%' THEN 1 ELSE 0 END)", "SUM(CASE WHEN \"Benefits\" LIKE '%overtime pay%' THEN 1 ELSE 0 END)", "SUM(CASE WHEN \"Benefits\" LIKE '%holiday benefits%' THEN 1 ELSE 0 END)", "SUM(CASE WHEN \"Benefits\" LIKE '%training%' THEN 1 ELSE 0 END)", "SUM(CASE WHEN \"Benefits\" LIKE '%travel%' THEN 1 ELSE 0 END)", "SUM(CASE WHEN \"Benefits\" LIKE '%communication allowance%' OR \"Benefits\" LIKE '%communication subsidy%' THEN 1 ELSE 0 END)", "SUM(CASE WHEN \"Benefits\" LIKE '%full attendance bonus%' OR \"Benefits\" LIKE '%attendance bonus%' THEN 1 ELSE 0 END)", "SUM(CASE WHEN \"Benefits\" LIKE '%high-temperature%' OR \"Benefits\" LIKE '%high temperature%' THEN 1 ELSE 0 END)", "SUM(CASE WHEN \"Benefits\" LIKE '%shuttle%' THEN 1 ELSE 0 END)", "SUM(CASE WHEN \"Benefits\" LIKE '%medical checkup%' OR \"Benefits\" LIKE '%physical examination%' THEN 1 ELSE 0 END)", "SUM(CASE WHEN \"Benefits\" LIKE '%work uniform%' OR \"Benefits\" LIKE '%uniform%' THEN 1 ELSE 0 END)", "SUM(CASE WHEN \"Benefits\" LIKE '%flexible working hours%' THEN 1 ELSE 0 END)"] | 1 | 137.001 |
| [S33/Q31](#s33) | success | ["sheet1"] | 0 / {} | ["\"Working Hours\""] | ["COUNT(*)", "AVG((salary_min + salary_max) / 2.0)"] | 20 | 103.487 |
| [S34/Q32](#s34) | success | ["sheet1"] | 0 / {} | ["\"Work Location\""] | ["COUNT(*)", "AVG((salary_min + salary_max) / 2.0)"] | 20 | 99.712 |
| [S35/Q33](#s35) | success | ["sheet1"] | 0 / {} | [] | [] | 7936 | 115.139 |
| [S36/Q34](#s36) | success | ["sheet1"] | 0 / {} | [] | [] | 7936 | 119.679 |
| [S37/Q35](#s37) | success | ["sheet1"] | 0 / {} | [] | [] | 3 | 0.583 |


## 元数据和设置

| SQL | 类别 | 状态 | 内容 |
| --- | --- | --- | --- |
| S1 | connection_setup | success | PRAGMA query_only=ON |
| S2 | metadata | success | SELECT name,sql FROM sqlite_master WHERE type='table' ORDER BY name |


## Python 与执行位置

人工源码审查：**database_first_violation**。Python 在招聘明细上计算福利关键词计数，按经验、公司、行业等维度求数量与均薪，并重算薪资区间比例，属于数据库内可执行的清洗与聚合。ANOVA、t 检验、相关分析及绘图是另外的统计补充。 [证据](../reviews/dacomp-048.json)。

P1：Need to parse salary data, compute distributions, and create visualizations. SQLite cannot easily handle the complex salary format parsing, benefit keyword extraction, or create charts. Will use Python to compute salary distribution histogram, benefits distribution bar chart, and analyze which qualities (experience, language, gender, industry, company type) significantly affect salary.

[源码](../../../runs/dsv4flash-db-first-full-01/dacomp-048/attempt-01/python/P1.py)；[输出](../../../runs/dsv4flash-db-first-full-01/dacomp-048/attempt-01/python/P1.stdout)；[错误](../../../runs/dsv4flash-db-first-full-01/dacomp-048/attempt-01/python/P1.stderr)。检出需人工核验的 SQL 可实现操作：groupby(, .query(, sort_values(；不能仅凭理由判为合规。

P2：Check the format of the query result to properly load data into pandas.

[源码](../../../runs/dsv4flash-db-first-full-01/dacomp-048/attempt-01/python/P2.py)；[输出](../../../runs/dsv4flash-db-first-full-01/dacomp-048/attempt-01/python/P2.stdout)；[错误](../../../runs/dsv4flash-db-first-full-01/dacomp-048/attempt-01/python/P2.stderr)。检出需人工核验的 SQL 可实现操作：.query(；不能仅凭理由判为合规。

P3：Need to load data from the JSON Lines result file since result_complete is a boolean flag. Read the file row by row.

[源码](../../../runs/dsv4flash-db-first-full-01/dacomp-048/attempt-01/python/P3.py)；[输出](../../../runs/dsv4flash-db-first-full-01/dacomp-048/attempt-01/python/P3.stdout)；[错误](../../../runs/dsv4flash-db-first-full-01/dacomp-048/attempt-01/python/P3.stderr)。自动源码筛查未检出预设迁出信号；这不是全面语义合规证明。

P4：Check the format of the JSON Lines file to understand how to parse it.

[源码](../../../runs/dsv4flash-db-first-full-01/dacomp-048/attempt-01/python/P4.py)；[输出](../../../runs/dsv4flash-db-first-full-01/dacomp-048/attempt-01/python/P4.stdout)；[错误](../../../runs/dsv4flash-db-first-full-01/dacomp-048/attempt-01/python/P4.stderr)。检出需人工核验的 SQL 可实现操作：.query(；不能仅凭理由判为合规。

P5：Load JSON Lines data correctly as arrays with column names. The rows are lists, not dicts.

[源码](../../../runs/dsv4flash-db-first-full-01/dacomp-048/attempt-01/python/P5.py)；[输出](../../../runs/dsv4flash-db-first-full-01/dacomp-048/attempt-01/python/P5.stdout)；[错误](../../../runs/dsv4flash-db-first-full-01/dacomp-048/attempt-01/python/P5.stderr)。检出需人工核验的 SQL 可实现操作：groupby(, sort_values(；不能仅凭理由判为合规。

P6：Fix the boxplot API issue and complete the full analysis: salary distribution, benefits distribution, and factor impact on salary.

[源码](../../../runs/dsv4flash-db-first-full-01/dacomp-048/attempt-01/python/P6.py)；[输出](../../../runs/dsv4flash-db-first-full-01/dacomp-048/attempt-01/python/P6.stdout)；[错误](../../../runs/dsv4flash-db-first-full-01/dacomp-048/attempt-01/python/P6.stderr)。检出需人工核验的 SQL 可实现操作：groupby(, sort_values(；不能仅凭理由判为合规。

P7：Create the salary factor comparison chart and benefit-impact-on-salary chart using the cleaned data saved to CSV. Also run ANOVA/t-tests to determine statistical significance of factors (work experience, foreign language, company type) on starting salary - these statistical tests are not supported by SQLite.

[源码](../../../runs/dsv4flash-db-first-full-01/dacomp-048/attempt-01/python/P7.py)；[输出](../../../runs/dsv4flash-db-first-full-01/dacomp-048/attempt-01/python/P7.stdout)；[错误](../../../runs/dsv4flash-db-first-full-01/dacomp-048/attempt-01/python/P7.stderr)。检出需人工核验的 SQL 可实现操作：groupby(, sort_values(；不能仅凭理由判为合规。

P8：Compute salary band distribution table and verify the English proficiency finding with a targeted t-test. Also compute an ordinal correlation between years of experience and salary. These statistics are not supported by SQLite.

[源码](../../../runs/dsv4flash-db-first-full-01/dacomp-048/attempt-01/python/P8.py)；[输出](../../../runs/dsv4flash-db-first-full-01/dacomp-048/attempt-01/python/P8.stdout)；[错误](../../../runs/dsv4flash-db-first-full-01/dacomp-048/attempt-01/python/P8.stderr)。自动源码筛查未检出预设迁出信号；这不是全面语义合规证明。

P9：Verify that the generated figures exist in the work directory so they can be referenced in the report.

[源码](../../../runs/dsv4flash-db-first-full-01/dacomp-048/attempt-01/python/P9.py)；[输出](../../../runs/dsv4flash-db-first-full-01/dacomp-048/attempt-01/python/P9.stdout)；[错误](../../../runs/dsv4flash-db-first-full-01/dacomp-048/attempt-01/python/P9.stderr)。自动源码筛查未检出预设迁出信号；这不是全面语义合规证明。

P10：Get the full industry breakdown with primary industry (first tag) for the report table.

[源码](../../../runs/dsv4flash-db-first-full-01/dacomp-048/attempt-01/python/P10.py)；[输出](../../../runs/dsv4flash-db-first-full-01/dacomp-048/attempt-01/python/P10.stdout)；[错误](../../../runs/dsv4flash-db-first-full-01/dacomp-048/attempt-01/python/P10.stderr)。检出需人工核验的 SQL 可实现操作：groupby(, sort_values(；不能仅凭理由判为合规。

## 优化机会

已验证候选。筛选限于精确 SQL、相同自包含 CTE、相同单表完整过滤、可分解单表聚合；未覆盖任意 Join 等价和一般谓词蕴含。全部候选都是 offline，未测在线预测。

| 候选 | 类型 | 已有结果 | 覆盖 SQL | 后续次数 | 中间行数 | 验证 | 成本 |
| --- | --- | --- | --- | --- | --- | --- | --- |
| C1 | exact-result reuse | True | ["S35", "S36"] | 1 | 7936 | verified | Not benchmarked; correctness alone does not establish net speedup. |
| C2 | aggregate MV | False | ["S5", "S6"] | 1 | unknown | not_verified_cap | Not tested |
| C3 | common filtered view | False | ["S8", "S17", "S18", "S35", "S36", "S37"] | 5 | 7936 | verified | Not benchmarked; correctness alone does not establish net speedup. |
| C4 | common filtered view | False | ["S9", "S30", "S32"] | 2 | 8055 | verified | Not benchmarked; correctness alone does not establish net speedup. |
| C5 | aggregate MV | False | ["S9", "S32"] | 1 | unknown | not_verified_cap | Not tested |


已验证覆盖（含触发查询、候选并集去重）：9/35 条成功数据 SQL。正确性仅针对当前数据库快照；未测性能的候选不能声称已加速。

[完整 build/rewrite 与比较证据](dacomp-048.analysis.json)。

### C3：common filtered view

Same single source and complete filter; original filter retained.

原查询 [S8](#s8), [S17](#s17), [S18](#s18), [S35](#s35), [S36](#s36), [S37](#s37) → 新增共享状态 C3 → 后续 5 次可复用。该构建点为事后假设，不代表 Agent 当时预知后续。

构建定义：

```sql
SELECT * FROM "sheet1" WHERE "Education Requirement" = 'Vocational school or above' AND NOT "Salary Range" IS NULL AND "Salary Range" <> ''
```

受益查询 S8 的改写示例：

```sql
SELECT "Salary Range", COUNT(*) AS cnt FROM temp.reuse_candidate AS sheet1 WHERE "Education Requirement" = 'Vocational school or above' AND NOT "Salary Range" IS NULL AND "Salary Range" <> '' GROUP BY "Salary Range" ORDER BY cnt DESC LIMIT 30
```

| 原 SQL | 列名一致 | 结果一致 | 比较方法 |
| --- | --- | --- | --- |
| S8 | True | True | ordered_numeric_tolerance |
| S17 | True | True | exact_multiset |
| S18 | True | True | exact_multiset |
| S35 | True | True | exact_multiset |
| S36 | True | True | exact_multiset |
| S37 | True | True | exact_multiset |


验证状态：verified；成本结论：Not benchmarked; correctness alone does not establish net speedup.

### C4：common filtered view

Same single source and complete filter; original filter retained.

原查询 [S9](#s9), [S30](#s30), [S32](#s32) → 新增共享状态 C4 → 后续 2 次可复用。该构建点为事后假设，不代表 Agent 当时预知后续。

构建定义：

```sql
SELECT * FROM "sheet1" WHERE "Education Requirement" = 'Vocational school or above' AND NOT "Benefits" IS NULL AND "Benefits" <> ''
```

受益查询 S9 的改写示例：

```sql
SELECT "Benefits", COUNT(*) AS cnt FROM temp.reuse_candidate AS sheet1 WHERE "Education Requirement" = 'Vocational school or above' AND NOT "Benefits" IS NULL AND "Benefits" <> '' GROUP BY "Benefits" ORDER BY cnt DESC LIMIT 30
```

| 原 SQL | 列名一致 | 结果一致 | 比较方法 |
| --- | --- | --- | --- |
| S9 | True | True | ordered_numeric_tolerance |
| S30 | True | True | exact_multiset |
| S32 | True | True | exact_multiset |


验证状态：verified；成本结论：Not benchmarked; correctness alone does not establish net speedup.

### C1：exact-result reuse

Identical normalized SQL and parameters; archive equality checked.

原查询 [S35](#s35), [S36](#s36) → 保留前序结果 S35 → 后续 1 次可复用。该构建点为事后假设，不代表 Agent 当时预知后续。

| 原 SQL | 列名一致 | 结果一致 | 比较方法 |
| --- | --- | --- | --- |
| S36 | True | True | exact_multiset |


验证状态：verified；成本结论：Not benchmarked; correctness alone does not establish net speedup.

结果依赖：自动记录 SQL→Python 的接口父调用，以及源码中引用归档文件的消费者；字面值相同不认定因果。模型方向选择需要人工读取消息，尚未做全面因果标注。

[原始报告](../../../runs/dsv4flash-db-first-full-01/dacomp-048/attempt-01/answer.md)；[统一消息](../../../runs/dsv4flash-db-first-full-01/dacomp-048/attempt-01/messages.jsonl)；[原始 OpenCode 事件](../../../runs/dsv4flash-db-first-full-01/dacomp-048/attempt-01/opencode.jsonl)；[SQL 引擎日志](../../../runs/dsv4flash-db-first-full-01/dacomp-048/attempt-01/sql_journal.jsonl)。

[可读报告（本地图片链接规范化）](../answers/dacomp-048.md)。原始回答保留，分析结论未改写。

## S1

类别 `connection_setup`；来源 `connection`；调用 `85975d6e502e4cc48e8161c5c3c7eed7`；状态 `success`。

```sql
PRAGMA query_only=ON
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-048/attempt-01/sql/S1.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-048/attempt-01/sql/S1.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-048/attempt-01/results/S1.rows.jsonl)；完整：True；SHA256：`e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`。

## S2

类别 `metadata`；来源 `list_db`；调用 `85975d6e502e4cc48e8161c5c3c7eed7`；状态 `success`。

```sql
SELECT name,sql FROM sqlite_master WHERE type='table' ORDER BY name
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-048/attempt-01/sql/S2.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-048/attempt-01/sql/S2.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-048/attempt-01/results/S2.rows.jsonl)；完整：True；SHA256：`8c9ad6fdec530f5865b919eec34d33bfdb0c4ad756e9b8790f38b123d074eca9`。

## S3

类别 `data`；来源 `query_db`；调用 `3a918e2ba33a4de7b1a51cf8404a9d69`；状态 `success`。

```sql
SELECT * FROM sheet1 LIMIT 10
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-048/attempt-01/sql/S3.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-048/attempt-01/sql/S3.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-048/attempt-01/results/S3.rows.jsonl)；完整：True；SHA256：`46ea1c39ec6561621b27877549910cef0169f6ece534096b45db31791dd3cba4`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "sheet1", "kind": "base", "block": null, "base_tables": ["sheet1"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |


## S4

类别 `data`；来源 `query_db`；调用 `7d473015adb34da694d0333e6199ec13`；状态 `success`。

```sql
SELECT DISTINCT "Education Requirement" FROM sheet1
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-048/attempt-01/sql/S4.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-048/attempt-01/sql/S4.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-048/attempt-01/results/S4.rows.jsonl)；完整：True；SHA256：`2e8c742fc91293166f0ec11b1bde33e05043ce8d5ed763a91e830b83e3b51725`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "sheet1", "kind": "base", "block": null, "base_tables": ["sheet1"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |


## S5

类别 `data`；来源 `query_db`；调用 `1a50c61036304580b78d4e9c7fb5dddb`；状态 `success`。

```sql
SELECT COUNT(*) AS total_rows FROM sheet1
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-048/attempt-01/sql/S5.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-048/attempt-01/sql/S5.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-048/attempt-01/results/S5.rows.jsonl)；完整：True；SHA256：`af8a8c20017a0200a12cccde943b9b7d094fbef334a5e1bd3a9c64d85519db16`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "sheet1", "kind": "base", "block": null, "base_tables": ["sheet1"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |


## S6

类别 `data`；来源 `query_db`；调用 `32e400d97a714a5a99bb8ef82176728f`；状态 `success`。

```sql
SELECT "Education Requirement", COUNT(*) AS cnt FROM sheet1 GROUP BY "Education Requirement" ORDER BY cnt DESC
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-048/attempt-01/sql/S6.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-048/attempt-01/sql/S6.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-048/attempt-01/results/S6.rows.jsonl)；完整：True；SHA256：`498b3596bb569ffe23583a0dcfd3131c46ea0315a1c675f52da4fec481184929`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "sheet1", "kind": "base", "block": null, "base_tables": ["sheet1"]}] | [] | ["\"Education Requirement\""] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |


## S7

类别 `data`；来源 `query_db`；调用 `501c598fe87646c3b041a272ae4546e0`；状态 `success`。

```sql
SELECT COUNT(*) AS vocational_edu FROM sheet1 WHERE "Education Requirement" LIKE '%vocational%' OR "Education Requirement" LIKE '%Vocational%'
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-048/attempt-01/sql/S7.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-048/attempt-01/sql/S7.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-048/attempt-01/results/S7.rows.jsonl)；完整：True；SHA256：`f4a565203483f48cf5e369a737a107a7cb6c5d5602d535612aef1d06910e2850`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "sheet1", "kind": "base", "block": null, "base_tables": ["sheet1"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |


## S8

类别 `data`；来源 `query_db`；调用 `761b42b6876648ac86277d47f86c334f`；状态 `success`。

```sql
SELECT "Salary Range", COUNT(*) AS cnt FROM sheet1 WHERE "Education Requirement" = 'Vocational school or above' AND "Salary Range" IS NOT NULL AND "Salary Range" != '' GROUP BY "Salary Range" ORDER BY cnt DESC LIMIT 30
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-048/attempt-01/sql/S8.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-048/attempt-01/sql/S8.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-048/attempt-01/results/S8.rows.jsonl)；完整：True；SHA256：`8b3aca2cd42818927e1dafcb19a222a8c8c3ec1405b02ec4d5be764843377b63`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "sheet1", "kind": "base", "block": null, "base_tables": ["sheet1"]}] | [] | ["\"Salary Range\""] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |


## S9

类别 `data`；来源 `query_db`；调用 `e4450f567a2a4e3c9e611ec05484446a`；状态 `success`。

```sql
SELECT "Benefits", COUNT(*) AS cnt FROM sheet1 WHERE "Education Requirement" = 'Vocational school or above' AND "Benefits" IS NOT NULL AND "Benefits" != '' GROUP BY "Benefits" ORDER BY cnt DESC LIMIT 30
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-048/attempt-01/sql/S9.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-048/attempt-01/sql/S9.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-048/attempt-01/results/S9.rows.jsonl)；完整：True；SHA256：`8141fde75ea2a1a20715d2d6e5e6313f2f1b3892337790daa292758ad76d6d01`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "sheet1", "kind": "base", "block": null, "base_tables": ["sheet1"]}] | [] | ["\"Benefits\""] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |


## S10

类别 `data`；来源 `query_db`；调用 `fc2bac6e99484673a61e33ac26d9b82e`；状态 `success`。

```sql
SELECT COUNT(*) AS total_voc, SUM(CASE WHEN "Salary Range" IS NOT NULL AND "Salary Range" != '' THEN 1 ELSE 0 END) AS with_salary, SUM(CASE WHEN "Benefits" IS NOT NULL AND "Benefits" != '' THEN 1 ELSE 0 END) AS with_benefits FROM sheet1 WHERE "Education Requirement" = 'Vocational school or above'
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-048/attempt-01/sql/S10.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-048/attempt-01/sql/S10.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-048/attempt-01/results/S10.rows.jsonl)；完整：True；SHA256：`e580f0e27883a251e6897eb48af9685261fdecb0592d40df48570ed22721b9ed`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "sheet1", "kind": "base", "block": null, "base_tables": ["sheet1"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |
| B1 | SUM(CASE WHEN NOT "Salary Range" IS NULL AND "Salary Range" <> '' THEN 1 ELSE 0 END) | [] | [{"table": "sheet1", "column": "Salary Range"}, {"table": "sheet1", "column": "Salary Range"}] | False |
| B1 | SUM(CASE WHEN NOT "Benefits" IS NULL AND "Benefits" <> '' THEN 1 ELSE 0 END) | [] | [{"table": "sheet1", "column": "Benefits"}, {"table": "sheet1", "column": "Benefits"}] | False |


## S11

类别 `data`；来源 `query_db`；调用 `8530045dab154c8a886f6ca5cc881850`；状态 `success`。

```sql
SELECT "Salary Range", COUNT(*) AS cnt FROM sheet1 WHERE "Education Requirement" = 'Vocational school or above' AND "Salary Range" IS NOT NULL AND "Salary Range" != '' AND "Salary Range" NOT LIKE '%-%' GROUP BY "Salary Range" ORDER BY cnt DESC LIMIT 40
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-048/attempt-01/sql/S11.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-048/attempt-01/sql/S11.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-048/attempt-01/results/S11.rows.jsonl)；完整：True；SHA256：`e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "sheet1", "kind": "base", "block": null, "base_tables": ["sheet1"]}] | [] | ["\"Salary Range\""] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |


## S12

类别 `data`；来源 `query_db`；调用 `32020120aee54717ab29c89b9c13b1c5`；状态 `success`。

```sql
SELECT "Salary Range", COUNT(*) AS cnt FROM sheet1 WHERE "Education Requirement" = 'Vocational school or above' AND "Salary Range" IS NOT NULL AND "Salary Range" != '' AND ("Salary Range" LIKE '%(%' OR "Salary Range" LIKE '%day%' OR "Salary Range" LIKE '%hour%' OR "Salary Range" LIKE '%面议%' OR "Salary Range" LIKE '%negotiable%') GROUP BY "Salary Range" ORDER BY cnt DESC LIMIT 50
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-048/attempt-01/sql/S12.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-048/attempt-01/sql/S12.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-048/attempt-01/results/S12.rows.jsonl)；完整：True；SHA256：`11d69323ad755b5d3267086b1cc847d30354b93d2271cd3c12a8f4abc9636fd9`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "sheet1", "kind": "base", "block": null, "base_tables": ["sheet1"]}] | [] | ["\"Salary Range\""] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |


## S13

类别 `data`；来源 `query_db`；调用 `e812709d651147dabfa789e669504676`；状态 `success`。

```sql
SELECT "Salary Range", COUNT(*) AS cnt FROM sheet1 WHERE "Education Requirement" = 'Vocational school or above' AND "Salary Range" LIKE '%negotiable%' OR ("Education Requirement" = 'Vocational school or above' AND "Salary Range" LIKE '%negotiable%') GROUP BY "Salary Range" ORDER BY cnt DESC LIMIT 10
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-048/attempt-01/sql/S13.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-048/attempt-01/sql/S13.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-048/attempt-01/results/S13.rows.jsonl)；完整：True；SHA256：`e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "sheet1", "kind": "base", "block": null, "base_tables": ["sheet1"]}] | [] | ["\"Salary Range\""] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |


## S14

类别 `data`；来源 `query_db`；调用 `ddaa98032ac644da932f2e4cb48cac2a`；状态 `success`。

```sql
SELECT "Salary Range", COUNT(*) AS cnt FROM sheet1 WHERE "Education Requirement" = 'Vocational school or above' AND "Salary Range" NOT LIKE '%yuan/month%' AND "Salary Range" NOT LIKE '%RMB/month%' AND "Salary Range" NOT LIKE '%天%' AND "Salary Range" NOT LIKE '%小时%' GROUP BY "Salary Range" ORDER BY cnt DESC LIMIT 30
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-048/attempt-01/sql/S14.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-048/attempt-01/sql/S14.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-048/attempt-01/results/S14.rows.jsonl)；完整：True；SHA256：`e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "sheet1", "kind": "base", "block": null, "base_tables": ["sheet1"]}] | [] | ["\"Salary Range\""] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |


## S15

类别 `data`；来源 `query_db`；调用 `2e1517c099894cffab2c5d611346f469`；状态 `success`。

```sql
SELECT "Salary Range", COUNT(*) AS cnt FROM sheet1 WHERE "Education Requirement" = 'Vocational school or above' AND "Salary Range" LIKE '%yuan%' GROUP BY "Salary Range" ORDER BY cnt DESC LIMIT 20
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-048/attempt-01/sql/S15.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-048/attempt-01/sql/S15.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-048/attempt-01/results/S15.rows.jsonl)；完整：True；SHA256：`a2cd37d69fde6d1a9a2d9388ac1fd367120468f60d7de1e6b5bde1ace4adc860`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "sheet1", "kind": "base", "block": null, "base_tables": ["sheet1"]}] | [] | ["\"Salary Range\""] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |


## S16

类别 `data`；来源 `query_db`；调用 `08aeacbf5a444acfbfcb74b5ffb20a0e`；状态 `success`。

```sql
SELECT "Salary Range", COUNT(*) AS cnt FROM sheet1 WHERE "Education Requirement" = 'Vocational school or above' AND "Salary Range" NOT LIKE '%month%' GROUP BY "Salary Range" ORDER BY cnt DESC LIMIT 30
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-048/attempt-01/sql/S16.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-048/attempt-01/sql/S16.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-048/attempt-01/results/S16.rows.jsonl)；完整：True；SHA256：`e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "sheet1", "kind": "base", "block": null, "base_tables": ["sheet1"]}] | [] | ["\"Salary Range\""] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |


## S17

类别 `data`；来源 `query_db`；调用 `55d84317d4a4491dac2b1c514e110717`；状态 `success`。

```sql
SELECT COUNT(DISTINCT "Salary Range") AS distinct_salary_formats FROM sheet1 WHERE "Education Requirement" = 'Vocational school or above' AND "Salary Range" IS NOT NULL AND "Salary Range" != ''
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-048/attempt-01/sql/S17.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-048/attempt-01/sql/S17.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-048/attempt-01/results/S17.rows.jsonl)；完整：True；SHA256：`ceb2ae058da01866cc1d4e00a55cb53e17ee4c818aad429db1a1be5837f31181`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "sheet1", "kind": "base", "block": null, "base_tables": ["sheet1"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(DISTINCT "Salary Range") | [{"table": "sheet1", "column": "Salary Range"}] | [] | False |


## S18

类别 `data`；来源 `query_db`；调用 `4401f71505164a16afaeea86d0fe4cff`；状态 `success`。

```sql
SELECT 
  "Salary Range",
  CAST(REPLACE(SUBSTR("Salary Range", 1, INSTR("Salary Range", '-') - 1), ',', '') AS INTEGER) AS salary_min_raw,
  CAST(REPLACE(SUBSTR("Salary Range", INSTR("Salary Range", '-') + 1, INSTR("Salary Range", ' ') - INSTR("Salary Range", '-') - 1), ',', '') AS INTEGER) AS salary_max_raw
FROM sheet1 
WHERE "Education Requirement" = 'Vocational school or above' 
  AND "Salary Range" IS NOT NULL AND "Salary Range" != ''
LIMIT 20
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-048/attempt-01/sql/S18.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-048/attempt-01/sql/S18.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-048/attempt-01/results/S18.rows.jsonl)；完整：True；SHA256：`13b8a1995a7f00ba8b6d38fbbf8811baacbdea2e8958d4162cc6b22b92482636`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "sheet1", "kind": "base", "block": null, "base_tables": ["sheet1"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |


## S19

类别 `data`；来源 `query_db`；调用 `fa879b5a342c42b1b18edaff2673107e`；状态 `success`。

```sql
SELECT "Salary Range" FROM sheet1 WHERE "Education Requirement" = 'Vocational school or above' AND "Salary Range" LIKE '%-%' AND "Salary Range" NOT LIKE '% - %' LIMIT 20
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-048/attempt-01/sql/S19.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-048/attempt-01/sql/S19.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-048/attempt-01/results/S19.rows.jsonl)；完整：True；SHA256：`a94460aa6a90ab2b13182ba12181af5c688dd65bf720bcd5bdc175dd7634819e`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "sheet1", "kind": "base", "block": null, "base_tables": ["sheet1"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |


## S20

类别 `data`；来源 `query_db`；调用 `218becca2125426eb16711ee08fbf2c2`；状态 `success`。

```sql
SELECT "Salary Range" FROM sheet1 WHERE "Education Requirement" = 'Vocational school or above' AND "Salary Range" NOT LIKE '% %' AND "Salary Range" IS NOT NULL LIMIT 20
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-048/attempt-01/sql/S20.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-048/attempt-01/sql/S20.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-048/attempt-01/results/S20.rows.jsonl)；完整：True；SHA256：`e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "sheet1", "kind": "base", "block": null, "base_tables": ["sheet1"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |


## S21

类别 `data`；来源 `query_db`；调用 `8652f7bcd24c4c8b85f23cda11234b45`；状态 `success`。

```sql
WITH parsed AS (
  SELECT 
    "Job Title",
    "Work Experience Requirement",
    "Foreign Language Requirement",
    "Age Requirement",
    "Gender Requirement",
    "Employment Type",
    "Company Type",
    "Industry",
    "Work Location",
    "Working Hours",
    "Benefits",
    CAST(REPLACE(SUBSTR("Salary Range", 1, INSTR("Salary Range", '-') - 1), ',', '') AS INTEGER) AS salary_min,
    CAST(REPLACE(SUBSTR("Salary Range", INSTR("Salary Range", '-') + 1, INSTR("Salary Range", ' ') - INSTR("Salary Range", '-') - 1), ',', '') AS INTEGER) AS salary_max
  FROM sheet1 
  WHERE "Education Requirement" = 'Vocational school or above' 
    AND "Salary Range" IS NOT NULL AND "Salary Range" != ''
)
SELECT 
  COUNT(*) AS n,
  SUM(CASE WHEN salary_min IS NULL OR salary_max IS NULL THEN 1 ELSE 0 END) AS parse_fail,
  ROUND(AVG(salary_min),1) AS avg_min,
  ROUND(AVG(salary_max),1) AS avg_max,
  ROUND(AVG((salary_min + salary_max) / 2.0),1) AS avg_mid,
  MIN(salary_min) AS min_salary,
  MAX(salary_max) AS max_salary
FROM parsed
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-048/attempt-01/sql/S21.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-048/attempt-01/sql/S21.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-048/attempt-01/results/S21.rows.jsonl)；完整：True；SHA256：`08728aed71e5b105da0b1830585496069a5b47d01119d069aa9a3fe068d2d14b`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "sheet1", "kind": "base", "block": null, "base_tables": ["sheet1"]}] | [] | [] |
| B2 | [{"alias": "parsed", "kind": "derived", "block": "B1", "base_tables": ["sheet1"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B2 | COUNT(*) | [] | [] | True |
| B2 | SUM(CASE WHEN salary_min IS NULL OR salary_max IS NULL THEN 1 ELSE 0 END) | [] | [{"table": "sheet1", "column": "Salary Range"}, {"table": "sheet1", "column": "Salary Range"}, {"table": "sheet1", "column": "Salary Range"}, {"table": "sheet1", "column": "Salary Range"}, {"table": "sheet1", "column": "Salary Range"}, {"table": "sheet1", "column": "Salary Range"}] | False |
| B2 | MIN(salary_min) | [{"table": "sheet1", "column": "Salary Range"}, {"table": "sheet1", "column": "Salary Range"}] | [] | False |
| B2 | MAX(salary_max) | [{"table": "sheet1", "column": "Salary Range"}, {"table": "sheet1", "column": "Salary Range"}, {"table": "sheet1", "column": "Salary Range"}, {"table": "sheet1", "column": "Salary Range"}] | [] | False |
| B2 | AVG(salary_min) | [{"table": "sheet1", "column": "Salary Range"}, {"table": "sheet1", "column": "Salary Range"}] | [] | False |
| B2 | AVG(salary_max) | [{"table": "sheet1", "column": "Salary Range"}, {"table": "sheet1", "column": "Salary Range"}, {"table": "sheet1", "column": "Salary Range"}, {"table": "sheet1", "column": "Salary Range"}] | [] | False |
| B2 | AVG((salary_min + salary_max) / 2.0) | [{"table": "sheet1", "column": "Salary Range"}, {"table": "sheet1", "column": "Salary Range"}, {"table": "sheet1", "column": "Salary Range"}, {"table": "sheet1", "column": "Salary Range"}, {"table": "sheet1", "column": "Salary Range"}, {"table": "sheet1", "column": "Salary Range"}] | [] | False |


## S22

类别 `data`；来源 `query_db`；调用 `ad2c109ef9b74182aaf9374ddd011f5e`；状态 `success`。

```sql
SELECT "Salary Range", salary_min, salary_max FROM (
  SELECT 
    "Salary Range",
    CAST(REPLACE(SUBSTR("Salary Range", 1, INSTR("Salary Range", '-') - 1), ',', '') AS INTEGER) AS salary_min,
    CAST(REPLACE(SUBSTR("Salary Range", INSTR("Salary Range", '-') + 1, INSTR("Salary Range", ' ') - INSTR("Salary Range", '-') - 1), ',', '') AS INTEGER) AS salary_max
  FROM sheet1 
  WHERE "Education Requirement" = 'Vocational school or above' 
    AND "Salary Range" IS NOT NULL AND "Salary Range" != ''
) 
WHERE salary_min < 1000
ORDER BY salary_min
LIMIT 20
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-048/attempt-01/sql/S22.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-048/attempt-01/sql/S22.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-048/attempt-01/results/S22.rows.jsonl)；完整：True；SHA256：`55ad6d48f03d6a1a64b393a5de077029c6b32fd5dde08b50bd6f802057a63ba5`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "sheet1", "kind": "base", "block": null, "base_tables": ["sheet1"]}] | [] | [] |
| B2 | [{"alias": "", "kind": "derived", "block": "B1", "base_tables": ["sheet1"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |


## S23

类别 `data`；来源 `query_db`；调用 `02f8286b650a4f0ab53a315c8aa68dfc`；状态 `success`。

```sql
SELECT "Salary Range", salary_min, salary_max FROM (
  SELECT 
    "Salary Range",
    CAST(REPLACE(SUBSTR("Salary Range", 1, INSTR("Salary Range", '-') - 1), ',', '') AS INTEGER) AS salary_min,
    CAST(REPLACE(SUBSTR("Salary Range", INSTR("Salary Range", '-') + 1, INSTR("Salary Range", ' ') - INSTR("Salary Range", '-') - 1), ',', '') AS INTEGER) AS salary_max
  FROM sheet1 
  WHERE "Education Requirement" = 'Vocational school or above' 
    AND "Salary Range" IS NOT NULL AND "Salary Range" != ''
) 
WHERE salary_min > 20000
ORDER BY salary_min DESC
LIMIT 20
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-048/attempt-01/sql/S23.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-048/attempt-01/sql/S23.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-048/attempt-01/results/S23.rows.jsonl)；完整：True；SHA256：`5552cca5dc259973a90356a65ae6c886d9d47f31207bdd3134843484073dc6a3`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "sheet1", "kind": "base", "block": null, "base_tables": ["sheet1"]}] | [] | [] |
| B2 | [{"alias": "", "kind": "derived", "block": "B1", "base_tables": ["sheet1"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |


## S24

类别 `data`；来源 `query_db`；调用 `d899d7188c1641b78060d30c310a5242`；状态 `success`。

```sql
WITH parsed AS (
  SELECT 
    "Work Experience Requirement",
    "Foreign Language Requirement",
    "Gender Requirement",
    "Employment Type",
    "Company Type",
    CAST(REPLACE(SUBSTR("Salary Range", 1, INSTR("Salary Range", '-') - 1), ',', '') AS INTEGER) AS salary_min,
    CAST(REPLACE(SUBSTR("Salary Range", INSTR("Salary Range", '-') + 1, INSTR("Salary Range", ' ') - INSTR("Salary Range", '-') - 1), ',', '') AS INTEGER) AS salary_max
  FROM sheet1 
  WHERE "Education Requirement" = 'Vocational school or above' 
    AND "Salary Range" IS NOT NULL AND "Salary Range" != ''
)
SELECT "Work Experience Requirement", COUNT(*) AS n, 
  ROUND(AVG((salary_min + salary_max)/2.0),1) AS avg_salary,
  ROUND(MIN(salary_min),0) AS min_salary,
  ROUND(MAX(salary_max),0) AS max_salary,
  ROUND(AVG(salary_min),1) AS avg_min,
  ROUND(AVG(salary_max),1) AS avg_max
FROM parsed
GROUP BY "Work Experience Requirement"
ORDER BY avg_salary DESC
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-048/attempt-01/sql/S24.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-048/attempt-01/sql/S24.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-048/attempt-01/results/S24.rows.jsonl)；完整：True；SHA256：`5a8c4396f16bdd226a7215141cad145eea651f8b07bfd30ca4e756e8d8f9595b`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "sheet1", "kind": "base", "block": null, "base_tables": ["sheet1"]}] | [] | [] |
| B2 | [{"alias": "parsed", "kind": "derived", "block": "B1", "base_tables": ["sheet1"]}] | [] | ["\"Work Experience Requirement\""] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B2 | COUNT(*) | [] | [] | True |
| B2 | AVG((salary_min + salary_max) / 2.0) | [{"table": "sheet1", "column": "Salary Range"}, {"table": "sheet1", "column": "Salary Range"}, {"table": "sheet1", "column": "Salary Range"}, {"table": "sheet1", "column": "Salary Range"}, {"table": "sheet1", "column": "Salary Range"}, {"table": "sheet1", "column": "Salary Range"}] | [] | False |
| B2 | MIN(salary_min) | [{"table": "sheet1", "column": "Salary Range"}, {"table": "sheet1", "column": "Salary Range"}] | [] | False |
| B2 | MAX(salary_max) | [{"table": "sheet1", "column": "Salary Range"}, {"table": "sheet1", "column": "Salary Range"}, {"table": "sheet1", "column": "Salary Range"}, {"table": "sheet1", "column": "Salary Range"}] | [] | False |
| B2 | AVG(salary_min) | [{"table": "sheet1", "column": "Salary Range"}, {"table": "sheet1", "column": "Salary Range"}] | [] | False |
| B2 | AVG(salary_max) | [{"table": "sheet1", "column": "Salary Range"}, {"table": "sheet1", "column": "Salary Range"}, {"table": "sheet1", "column": "Salary Range"}, {"table": "sheet1", "column": "Salary Range"}] | [] | False |


## S25

类别 `data`；来源 `query_db`；调用 `11dc5ece828f4fbb8038fc90db6a559e`；状态 `success`。

```sql
WITH parsed AS (
  SELECT 
    "Foreign Language Requirement",
    CAST(REPLACE(SUBSTR("Salary Range", 1, INSTR("Salary Range", '-') - 1), ',', '') AS INTEGER) AS salary_min,
    CAST(REPLACE(SUBSTR("Salary Range", INSTR("Salary Range", '-') + 1, INSTR("Salary Range", ' ') - INSTR("Salary Range", '-') - 1), ',', '') AS INTEGER) AS salary_max
  FROM sheet1 
  WHERE "Education Requirement" = 'Vocational school or above' 
    AND "Salary Range" IS NOT NULL AND "Salary Range" != ''
)
SELECT "Foreign Language Requirement", COUNT(*) AS n, 
  ROUND(AVG((salary_min + salary_max)/2.0),1) AS avg_salary
FROM parsed
GROUP BY "Foreign Language Requirement"
ORDER BY avg_salary DESC
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-048/attempt-01/sql/S25.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-048/attempt-01/sql/S25.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-048/attempt-01/results/S25.rows.jsonl)；完整：True；SHA256：`0e09761bd1bcae120b09fa4fc4b555893625ba67f6dec238c5d01a5655b7b17b`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "sheet1", "kind": "base", "block": null, "base_tables": ["sheet1"]}] | [] | [] |
| B2 | [{"alias": "parsed", "kind": "derived", "block": "B1", "base_tables": ["sheet1"]}] | [] | ["\"Foreign Language Requirement\""] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B2 | COUNT(*) | [] | [] | True |
| B2 | AVG((salary_min + salary_max) / 2.0) | [{"table": "sheet1", "column": "Salary Range"}, {"table": "sheet1", "column": "Salary Range"}, {"table": "sheet1", "column": "Salary Range"}, {"table": "sheet1", "column": "Salary Range"}, {"table": "sheet1", "column": "Salary Range"}, {"table": "sheet1", "column": "Salary Range"}] | [] | False |


## S26

类别 `data`；来源 `query_db`；调用 `1121d98345cd4b64937567d01259021e`；状态 `success`。

```sql
WITH parsed AS (
  SELECT 
    "Work Experience Requirement",
    CAST(REPLACE(SUBSTR("Salary Range", 1, INSTR("Salary Range", '-') - 1), ',', '') AS INTEGER) AS salary_min,
    CAST(REPLACE(SUBSTR("Salary Range", INSTR("Salary Range", '-') + 1, INSTR("Salary Range", ' ') - INSTR("Salary Range", '-') - 1), ',', '') AS INTEGER) AS salary_max
  FROM sheet1 
  WHERE "Education Requirement" = 'Vocational school or above' 
    AND "Salary Range" IS NOT NULL AND "Salary Range" != ''
)
SELECT "Work Experience Requirement", COUNT(*) AS n, 
  ROUND(AVG((salary_min + salary_max)/2.0),1) AS avg_salary
FROM parsed
GROUP BY "Work Experience Requirement"
ORDER BY n DESC
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-048/attempt-01/sql/S26.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-048/attempt-01/sql/S26.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-048/attempt-01/results/S26.rows.jsonl)；完整：True；SHA256：`7207d789c695c8e05c40734d74bc1e9da4f401f8219c7b0c843df98185daf8e4`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "sheet1", "kind": "base", "block": null, "base_tables": ["sheet1"]}] | [] | [] |
| B2 | [{"alias": "parsed", "kind": "derived", "block": "B1", "base_tables": ["sheet1"]}] | [] | ["\"Work Experience Requirement\""] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B2 | COUNT(*) | [] | [] | True |
| B2 | AVG((salary_min + salary_max) / 2.0) | [{"table": "sheet1", "column": "Salary Range"}, {"table": "sheet1", "column": "Salary Range"}, {"table": "sheet1", "column": "Salary Range"}, {"table": "sheet1", "column": "Salary Range"}, {"table": "sheet1", "column": "Salary Range"}, {"table": "sheet1", "column": "Salary Range"}] | [] | False |


## S27

类别 `data`；来源 `query_db`；调用 `2616cfd7be2642ddb59f58e16f7e1dc3`；状态 `success`。

```sql
WITH parsed AS (
  SELECT 
    "Gender Requirement",
    CAST(REPLACE(SUBSTR("Salary Range", 1, INSTR("Salary Range", '-') - 1), ',', '') AS INTEGER) AS salary_min,
    CAST(REPLACE(SUBSTR("Salary Range", INSTR("Salary Range", '-') + 1, INSTR("Salary Range", ' ') - INSTR("Salary Range", '-') - 1), ',', '') AS INTEGER) AS salary_max
  FROM sheet1 
  WHERE "Education Requirement" = 'Vocational school or above' 
    AND "Salary Range" IS NOT NULL AND "Salary Range" != ''
)
SELECT "Gender Requirement", COUNT(*) AS n, 
  ROUND(AVG((salary_min + salary_max)/2.0),1) AS avg_salary,
  ROUND(AVG(salary_min),1) AS avg_min,
  ROUND(AVG(salary_max),1) AS avg_max
FROM parsed
GROUP BY "Gender Requirement"
ORDER BY avg_salary DESC
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-048/attempt-01/sql/S27.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-048/attempt-01/sql/S27.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-048/attempt-01/results/S27.rows.jsonl)；完整：True；SHA256：`0dd7f08e5e14d2811de2b28f2b77812f91706b966d35ebc9e9eeb077682a3bde`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "sheet1", "kind": "base", "block": null, "base_tables": ["sheet1"]}] | [] | [] |
| B2 | [{"alias": "parsed", "kind": "derived", "block": "B1", "base_tables": ["sheet1"]}] | [] | ["\"Gender Requirement\""] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B2 | COUNT(*) | [] | [] | True |
| B2 | AVG((salary_min + salary_max) / 2.0) | [{"table": "sheet1", "column": "Salary Range"}, {"table": "sheet1", "column": "Salary Range"}, {"table": "sheet1", "column": "Salary Range"}, {"table": "sheet1", "column": "Salary Range"}, {"table": "sheet1", "column": "Salary Range"}, {"table": "sheet1", "column": "Salary Range"}] | [] | False |
| B2 | AVG(salary_min) | [{"table": "sheet1", "column": "Salary Range"}, {"table": "sheet1", "column": "Salary Range"}] | [] | False |
| B2 | AVG(salary_max) | [{"table": "sheet1", "column": "Salary Range"}, {"table": "sheet1", "column": "Salary Range"}, {"table": "sheet1", "column": "Salary Range"}, {"table": "sheet1", "column": "Salary Range"}] | [] | False |


## S28

类别 `data`；来源 `query_db`；调用 `3218f5c85ee2401d86fff61fe60f36d6`；状态 `success`。

```sql
WITH parsed AS (
  SELECT 
    "Employment Type",
    CAST(REPLACE(SUBSTR("Salary Range", 1, INSTR("Salary Range", '-') - 1), ',', '') AS INTEGER) AS salary_min,
    CAST(REPLACE(SUBSTR("Salary Range", INSTR("Salary Range", '-') + 1, INSTR("Salary Range", ' ') - INSTR("Salary Range", '-') - 1), ',', '') AS INTEGER) AS salary_max
  FROM sheet1 
  WHERE "Education Requirement" = 'Vocational school or above' 
    AND "Salary Range" IS NOT NULL AND "Salary Range" != ''
)
SELECT "Employment Type", COUNT(*) AS n, 
  ROUND(AVG((salary_min + salary_max)/2.0),1) AS avg_salary
FROM parsed
GROUP BY "Employment Type"
ORDER BY avg_salary DESC
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-048/attempt-01/sql/S28.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-048/attempt-01/sql/S28.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-048/attempt-01/results/S28.rows.jsonl)；完整：True；SHA256：`799c92d5f3c8236e70e193c825252f165b82c002011ee7308fb687e2e7392560`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "sheet1", "kind": "base", "block": null, "base_tables": ["sheet1"]}] | [] | [] |
| B2 | [{"alias": "parsed", "kind": "derived", "block": "B1", "base_tables": ["sheet1"]}] | [] | ["\"Employment Type\""] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B2 | COUNT(*) | [] | [] | True |
| B2 | AVG((salary_min + salary_max) / 2.0) | [{"table": "sheet1", "column": "Salary Range"}, {"table": "sheet1", "column": "Salary Range"}, {"table": "sheet1", "column": "Salary Range"}, {"table": "sheet1", "column": "Salary Range"}, {"table": "sheet1", "column": "Salary Range"}, {"table": "sheet1", "column": "Salary Range"}] | [] | False |


## S29

类别 `data`；来源 `query_db`；调用 `93e345260bbf47d8b0202b09279cf1e3`；状态 `success`。

```sql
WITH parsed AS (
  SELECT 
    "Company Type",
    CAST(REPLACE(SUBSTR("Salary Range", 1, INSTR("Salary Range", '-') - 1), ',', '') AS INTEGER) AS salary_min,
    CAST(REPLACE(SUBSTR("Salary Range", INSTR("Salary Range", '-') + 1, INSTR("Salary Range", ' ') - INSTR("Salary Range", '-') - 1), ',', '') AS INTEGER) AS salary_max
  FROM sheet1 
  WHERE "Education Requirement" = 'Vocational school or above' 
    AND "Salary Range" IS NOT NULL AND "Salary Range" != ''
)
SELECT "Company Type", COUNT(*) AS n, 
  ROUND(AVG((salary_min + salary_max)/2.0),1) AS avg_salary
FROM parsed
GROUP BY "Company Type"
ORDER BY avg_salary DESC
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-048/attempt-01/sql/S29.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-048/attempt-01/sql/S29.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-048/attempt-01/results/S29.rows.jsonl)；完整：True；SHA256：`675716ffd5692e068c1332af12010fab089878c4fc73fac15af39e9b7e99fcd3`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "sheet1", "kind": "base", "block": null, "base_tables": ["sheet1"]}] | [] | [] |
| B2 | [{"alias": "parsed", "kind": "derived", "block": "B1", "base_tables": ["sheet1"]}] | [] | ["\"Company Type\""] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B2 | COUNT(*) | [] | [] | True |
| B2 | AVG((salary_min + salary_max) / 2.0) | [{"table": "sheet1", "column": "Salary Range"}, {"table": "sheet1", "column": "Salary Range"}, {"table": "sheet1", "column": "Salary Range"}, {"table": "sheet1", "column": "Salary Range"}, {"table": "sheet1", "column": "Salary Range"}, {"table": "sheet1", "column": "Salary Range"}] | [] | False |


## S30

类别 `data`；来源 `query_db`；调用 `ba2f29c52a3647cc90289eef0a4bf6b0`；状态 `success`。

```sql
SELECT COUNT(DISTINCT "Benefits") AS distinct_benefits FROM sheet1 WHERE "Education Requirement" = 'Vocational school or above' AND "Benefits" IS NOT NULL AND "Benefits" != ''
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-048/attempt-01/sql/S30.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-048/attempt-01/sql/S30.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-048/attempt-01/results/S30.rows.jsonl)；完整：True；SHA256：`1280635b7e454ce676c12a16d1103d638a56ee12cee7227a4b7c7f02e875586f`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "sheet1", "kind": "base", "block": null, "base_tables": ["sheet1"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(DISTINCT "Benefits") | [{"table": "sheet1", "column": "Benefits"}] | [] | False |


## S31

类别 `data`；来源 `query_db`；调用 `5b7eb77d94fa49ab9feea62ac5419493`；状态 `success`。

```sql
WITH parsed AS (
  SELECT 
    "Industry",
    CAST(REPLACE(SUBSTR("Salary Range", 1, INSTR("Salary Range", '-') - 1), ',', '') AS INTEGER) AS salary_min,
    CAST(REPLACE(SUBSTR("Salary Range", INSTR("Salary Range", '-') + 1, INSTR("Salary Range", ' ') - INSTR("Salary Range", '-') - 1), ',', '') AS INTEGER) AS salary_max
  FROM sheet1 
  WHERE "Education Requirement" = 'Vocational school or above' 
    AND "Salary Range" IS NOT NULL AND "Salary Range" != ''
)
SELECT "Industry", COUNT(*) AS n, 
  ROUND(AVG((salary_min + salary_max)/2.0),1) AS avg_salary
FROM parsed
GROUP BY "Industry"
ORDER BY n DESC
LIMIT 25
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-048/attempt-01/sql/S31.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-048/attempt-01/sql/S31.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-048/attempt-01/results/S31.rows.jsonl)；完整：True；SHA256：`7809f6531b635af2c9bfbc428b1480a69f2587110108acef488f138bddc10455`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "sheet1", "kind": "base", "block": null, "base_tables": ["sheet1"]}] | [] | [] |
| B2 | [{"alias": "parsed", "kind": "derived", "block": "B1", "base_tables": ["sheet1"]}] | [] | ["\"Industry\""] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B2 | COUNT(*) | [] | [] | True |
| B2 | AVG((salary_min + salary_max) / 2.0) | [{"table": "sheet1", "column": "Salary Range"}, {"table": "sheet1", "column": "Salary Range"}, {"table": "sheet1", "column": "Salary Range"}, {"table": "sheet1", "column": "Salary Range"}, {"table": "sheet1", "column": "Salary Range"}, {"table": "sheet1", "column": "Salary Range"}] | [] | False |


## S32

类别 `data`；来源 `query_db`；调用 `8930e7ad1d904c4a8bcfd5bf152dd919`；状态 `success`。

```sql
SELECT 
  SUM(CASE WHEN "Benefits" LIKE '%Five social insurances%' THEN 1 ELSE 0 END) AS five_social,
  SUM(CASE WHEN "Benefits" LIKE '%housing provident fund%' OR "Benefits" LIKE '%housing fund%' THEN 1 ELSE 0 END) AS housing_fund,
  SUM(CASE WHEN "Benefits" LIKE '%commercial insurance%' THEN 1 ELSE 0 END) AS commercial_ins,
  SUM(CASE WHEN "Benefits" LIKE '%paid annual leave%' THEN 1 ELSE 0 END) AS annual_leave,
  SUM(CASE WHEN "Benefits" LIKE '%double pay at the end%' OR "Benefits" LIKE '%double salary at the end%' THEN 1 ELSE 0 END) AS double_pay,
  SUM(CASE WHEN "Benefits" LIKE '%performance bonus%' THEN 1 ELSE 0 END) AS perf_bonus,
  SUM(CASE WHEN "Benefits" LIKE '%year-end bonus%' OR "Benefits" LIKE '%year end bonus%' THEN 1 ELSE 0 END) AS year_end_bonus,
  SUM(CASE WHEN "Benefits" LIKE '%meal allowance%' OR "Benefits" LIKE '%meal subsidy%' OR "Benefits" LIKE '%food allowance%' THEN 1 ELSE 0 END) AS meal_allowance,
  SUM(CASE WHEN "Benefits" LIKE '%accommodation%' OR "Benefits" LIKE '%housing%' THEN 1 ELSE 0 END) AS accommodation,
  SUM(CASE WHEN "Benefits" LIKE '%meals provided%' OR "Benefits" LIKE '%meals and accommodation provided%' THEN 1 ELSE 0 END) AS meals_provided,
  SUM(CASE WHEN "Benefits" LIKE '%overtime pay%' THEN 1 ELSE 0 END) AS overtime_pay,
  SUM(CASE WHEN "Benefits" LIKE '%holiday benefits%' THEN 1 ELSE 0 END) AS holiday_benefits,
  SUM(CASE WHEN "Benefits" LIKE '%training%' THEN 1 ELSE 0 END) AS training,
  SUM(CASE WHEN "Benefits" LIKE '%travel%' THEN 1 ELSE 0 END) AS travel,
  SUM(CASE WHEN "Benefits" LIKE '%communication allowance%' OR "Benefits" LIKE '%communication subsidy%' THEN 1 ELSE 0 END) AS comm_allowance,
  SUM(CASE WHEN "Benefits" LIKE '%full attendance bonus%' OR "Benefits" LIKE '%attendance bonus%' THEN 1 ELSE 0 END) AS attendance_bonus,
  SUM(CASE WHEN "Benefits" LIKE '%high-temperature%' OR "Benefits" LIKE '%high temperature%' THEN 1 ELSE 0 END) AS high_temp,
  SUM(CASE WHEN "Benefits" LIKE '%shuttle%' THEN 1 ELSE 0 END) AS shuttle,
  SUM(CASE WHEN "Benefits" LIKE '%medical checkup%' OR "Benefits" LIKE '%physical examination%' THEN 1 ELSE 0 END) AS checkup,
  SUM(CASE WHEN "Benefits" LIKE '%work uniform%' OR "Benefits" LIKE '%uniform%' THEN 1 ELSE 0 END) AS uniform,
  SUM(CASE WHEN "Benefits" LIKE '%flexible working hours%' THEN 1 ELSE 0 END) AS flexible_hours
FROM sheet1 
WHERE "Education Requirement" = 'Vocational school or above' AND "Benefits" IS NOT NULL AND "Benefits" != ''
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-048/attempt-01/sql/S32.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-048/attempt-01/sql/S32.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-048/attempt-01/results/S32.rows.jsonl)；完整：True；SHA256：`a2caadf245bf72cd6df3eef01f777fc9c70f354c24766243c42e97f60a7c29f6`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "sheet1", "kind": "base", "block": null, "base_tables": ["sheet1"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | SUM(CASE WHEN "Benefits" LIKE '%Five social insurances%' THEN 1 ELSE 0 END) | [] | [{"table": "sheet1", "column": "Benefits"}] | False |
| B1 | SUM(CASE WHEN "Benefits" LIKE '%housing provident fund%' OR "Benefits" LIKE '%housing fund%' THEN 1 ELSE 0 END) | [] | [{"table": "sheet1", "column": "Benefits"}, {"table": "sheet1", "column": "Benefits"}] | False |
| B1 | SUM(CASE WHEN "Benefits" LIKE '%commercial insurance%' THEN 1 ELSE 0 END) | [] | [{"table": "sheet1", "column": "Benefits"}] | False |
| B1 | SUM(CASE WHEN "Benefits" LIKE '%paid annual leave%' THEN 1 ELSE 0 END) | [] | [{"table": "sheet1", "column": "Benefits"}] | False |
| B1 | SUM(CASE WHEN "Benefits" LIKE '%double pay at the end%' OR "Benefits" LIKE '%double salary at the end%' THEN 1 ELSE 0 END) | [] | [{"table": "sheet1", "column": "Benefits"}, {"table": "sheet1", "column": "Benefits"}] | False |
| B1 | SUM(CASE WHEN "Benefits" LIKE '%performance bonus%' THEN 1 ELSE 0 END) | [] | [{"table": "sheet1", "column": "Benefits"}] | False |
| B1 | SUM(CASE WHEN "Benefits" LIKE '%year-end bonus%' OR "Benefits" LIKE '%year end bonus%' THEN 1 ELSE 0 END) | [] | [{"table": "sheet1", "column": "Benefits"}, {"table": "sheet1", "column": "Benefits"}] | False |
| B1 | SUM(CASE WHEN "Benefits" LIKE '%meal allowance%' OR "Benefits" LIKE '%meal subsidy%' OR "Benefits" LIKE '%food allowance%' THEN 1 ELSE 0 END) | [] | [{"table": "sheet1", "column": "Benefits"}, {"table": "sheet1", "column": "Benefits"}, {"table": "sheet1", "column": "Benefits"}] | False |
| B1 | SUM(CASE WHEN "Benefits" LIKE '%accommodation%' OR "Benefits" LIKE '%housing%' THEN 1 ELSE 0 END) | [] | [{"table": "sheet1", "column": "Benefits"}, {"table": "sheet1", "column": "Benefits"}] | False |
| B1 | SUM(CASE WHEN "Benefits" LIKE '%meals provided%' OR "Benefits" LIKE '%meals and accommodation provided%' THEN 1 ELSE 0 END) | [] | [{"table": "sheet1", "column": "Benefits"}, {"table": "sheet1", "column": "Benefits"}] | False |
| B1 | SUM(CASE WHEN "Benefits" LIKE '%overtime pay%' THEN 1 ELSE 0 END) | [] | [{"table": "sheet1", "column": "Benefits"}] | False |
| B1 | SUM(CASE WHEN "Benefits" LIKE '%holiday benefits%' THEN 1 ELSE 0 END) | [] | [{"table": "sheet1", "column": "Benefits"}] | False |
| B1 | SUM(CASE WHEN "Benefits" LIKE '%training%' THEN 1 ELSE 0 END) | [] | [{"table": "sheet1", "column": "Benefits"}] | False |
| B1 | SUM(CASE WHEN "Benefits" LIKE '%travel%' THEN 1 ELSE 0 END) | [] | [{"table": "sheet1", "column": "Benefits"}] | False |
| B1 | SUM(CASE WHEN "Benefits" LIKE '%communication allowance%' OR "Benefits" LIKE '%communication subsidy%' THEN 1 ELSE 0 END) | [] | [{"table": "sheet1", "column": "Benefits"}, {"table": "sheet1", "column": "Benefits"}] | False |
| B1 | SUM(CASE WHEN "Benefits" LIKE '%full attendance bonus%' OR "Benefits" LIKE '%attendance bonus%' THEN 1 ELSE 0 END) | [] | [{"table": "sheet1", "column": "Benefits"}, {"table": "sheet1", "column": "Benefits"}] | False |
| B1 | SUM(CASE WHEN "Benefits" LIKE '%high-temperature%' OR "Benefits" LIKE '%high temperature%' THEN 1 ELSE 0 END) | [] | [{"table": "sheet1", "column": "Benefits"}, {"table": "sheet1", "column": "Benefits"}] | False |
| B1 | SUM(CASE WHEN "Benefits" LIKE '%shuttle%' THEN 1 ELSE 0 END) | [] | [{"table": "sheet1", "column": "Benefits"}] | False |
| B1 | SUM(CASE WHEN "Benefits" LIKE '%medical checkup%' OR "Benefits" LIKE '%physical examination%' THEN 1 ELSE 0 END) | [] | [{"table": "sheet1", "column": "Benefits"}, {"table": "sheet1", "column": "Benefits"}] | False |
| B1 | SUM(CASE WHEN "Benefits" LIKE '%work uniform%' OR "Benefits" LIKE '%uniform%' THEN 1 ELSE 0 END) | [] | [{"table": "sheet1", "column": "Benefits"}, {"table": "sheet1", "column": "Benefits"}] | False |
| B1 | SUM(CASE WHEN "Benefits" LIKE '%flexible working hours%' THEN 1 ELSE 0 END) | [] | [{"table": "sheet1", "column": "Benefits"}] | False |


## S33

类别 `data`；来源 `query_db`；调用 `b1e11b942bdd409188e0a4f368f8086b`；状态 `success`。

```sql
WITH parsed AS (
  SELECT 
    "Working Hours",
    CAST(REPLACE(SUBSTR("Salary Range", 1, INSTR("Salary Range", '-') - 1), ',', '') AS INTEGER) AS salary_min,
    CAST(REPLACE(SUBSTR("Salary Range", INSTR("Salary Range", '-') + 1, INSTR("Salary Range", ' ') - INSTR("Salary Range", '-') - 1), ',', '') AS INTEGER) AS salary_max
  FROM sheet1 
  WHERE "Education Requirement" = 'Vocational school or above' 
    AND "Salary Range" IS NOT NULL AND "Salary Range" != ''
)
SELECT "Working Hours", COUNT(*) AS n, 
  ROUND(AVG((salary_min + salary_max)/2.0),1) AS avg_salary
FROM parsed
GROUP BY "Working Hours"
ORDER BY n DESC
LIMIT 20
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-048/attempt-01/sql/S33.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-048/attempt-01/sql/S33.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-048/attempt-01/results/S33.rows.jsonl)；完整：True；SHA256：`d47e7296266161489d12e1ac0f52aedde3c19ceb649adb8447fd9afd28875682`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "sheet1", "kind": "base", "block": null, "base_tables": ["sheet1"]}] | [] | [] |
| B2 | [{"alias": "parsed", "kind": "derived", "block": "B1", "base_tables": ["sheet1"]}] | [] | ["\"Working Hours\""] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B2 | COUNT(*) | [] | [] | True |
| B2 | AVG((salary_min + salary_max) / 2.0) | [{"table": "sheet1", "column": "Salary Range"}, {"table": "sheet1", "column": "Salary Range"}, {"table": "sheet1", "column": "Salary Range"}, {"table": "sheet1", "column": "Salary Range"}, {"table": "sheet1", "column": "Salary Range"}, {"table": "sheet1", "column": "Salary Range"}] | [] | False |


## S34

类别 `data`；来源 `query_db`；调用 `721588379ebb4988b149a68e868a24e3`；状态 `success`。

```sql
WITH parsed AS (
  SELECT 
    "Work Location",
    CAST(REPLACE(SUBSTR("Salary Range", 1, INSTR("Salary Range", '-') - 1), ',', '') AS INTEGER) AS salary_min,
    CAST(REPLACE(SUBSTR("Salary Range", INSTR("Salary Range", '-') + 1, INSTR("Salary Range", ' ') - INSTR("Salary Range", '-') - 1), ',', '') AS INTEGER) AS salary_max
  FROM sheet1 
  WHERE "Education Requirement" = 'Vocational school or above' 
    AND "Salary Range" IS NOT NULL AND "Salary Range" != ''
)
SELECT "Work Location", COUNT(*) AS n, 
  ROUND(AVG((salary_min + salary_max)/2.0),1) AS avg_salary
FROM parsed
GROUP BY "Work Location"
ORDER BY n DESC
LIMIT 20
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-048/attempt-01/sql/S34.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-048/attempt-01/sql/S34.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-048/attempt-01/results/S34.rows.jsonl)；完整：True；SHA256：`85c9281099035797c1c32d2a67139b9ffe62cf7328b426723375a5e0ff1de999`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "sheet1", "kind": "base", "block": null, "base_tables": ["sheet1"]}] | [] | [] |
| B2 | [{"alias": "parsed", "kind": "derived", "block": "B1", "base_tables": ["sheet1"]}] | [] | ["\"Work Location\""] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B2 | COUNT(*) | [] | [] | True |
| B2 | AVG((salary_min + salary_max) / 2.0) | [{"table": "sheet1", "column": "Salary Range"}, {"table": "sheet1", "column": "Salary Range"}, {"table": "sheet1", "column": "Salary Range"}, {"table": "sheet1", "column": "Salary Range"}, {"table": "sheet1", "column": "Salary Range"}, {"table": "sheet1", "column": "Salary Range"}] | [] | False |


## S35

类别 `data`；来源 `python`；调用 `5e3cab5a2a2b4f0bb04dc3d63f9f67c9`；状态 `success`。

```sql

  SELECT 
    "Job Title", "Work Experience Requirement", "Foreign Language Requirement",
    "Gender Requirement", "Company Type", "Industry", "Work Location",
    "Working Hours", "Benefits", "Salary Range",
    CAST(REPLACE(SUBSTR("Salary Range", 1, INSTR("Salary Range", '-') - 1), ',', '') AS INTEGER) AS salary_min,
    CAST(REPLACE(SUBSTR("Salary Range", INSTR("Salary Range", '-') + 1, INSTR("Salary Range", ' ') - INSTR("Salary Range", '-') - 1), ',', '') AS INTEGER) AS salary_max
  FROM sheet1 
  WHERE "Education Requirement" = 'Vocational school or above' 
    AND "Salary Range" IS NOT NULL AND "Salary Range" != ''

```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-048/attempt-01/sql/S35.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-048/attempt-01/sql/S35.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-048/attempt-01/results/S35.rows.jsonl)；完整：True；SHA256：`06c40c089bd76d95bba0e6452854fcf957e9e7aef9d78b71487ba01991eca7db`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "sheet1", "kind": "base", "block": null, "base_tables": ["sheet1"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |


## S36

类别 `data`；来源 `python`；调用 `6422622a18874156b1a39301f3da473a`；状态 `success`。

```sql

  SELECT 
    "Job Title", "Work Experience Requirement", "Foreign Language Requirement",
    "Gender Requirement", "Company Type", "Industry", "Work Location",
    "Working Hours", "Benefits", "Salary Range",
    CAST(REPLACE(SUBSTR("Salary Range", 1, INSTR("Salary Range", '-') - 1), ',', '') AS INTEGER) AS salary_min,
    CAST(REPLACE(SUBSTR("Salary Range", INSTR("Salary Range", '-') + 1, INSTR("Salary Range", ' ') - INSTR("Salary Range", '-') - 1), ',', '') AS INTEGER) AS salary_max
  FROM sheet1 
  WHERE "Education Requirement" = 'Vocational school or above' 
    AND "Salary Range" IS NOT NULL AND "Salary Range" != ''

```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-048/attempt-01/sql/S36.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-048/attempt-01/sql/S36.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-048/attempt-01/results/S36.rows.jsonl)；完整：True；SHA256：`06c40c089bd76d95bba0e6452854fcf957e9e7aef9d78b71487ba01991eca7db`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "sheet1", "kind": "base", "block": null, "base_tables": ["sheet1"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |


## S37

类别 `data`；来源 `python`；调用 `a7eb1bac98604b82afa1ea302ceb4984`；状态 `success`。

```sql

  SELECT 
    "Job Title", "Work Experience Requirement", "Foreign Language Requirement",
    "Gender Requirement", "Company Type", "Industry", "Work Location",
    "Working Hours", "Benefits", "Salary Range",
    CAST(REPLACE(SUBSTR("Salary Range", 1, INSTR("Salary Range", '-') - 1), ',', '') AS INTEGER) AS salary_min,
    CAST(REPLACE(SUBSTR("Salary Range", INSTR("Salary Range", '-') + 1, INSTR("Salary Range", ' ') - INSTR("Salary Range", '-') - 1), ',', '') AS INTEGER) AS salary_max
  FROM sheet1 
  WHERE "Education Requirement" = 'Vocational school or above' 
    AND "Salary Range" IS NOT NULL AND "Salary Range" != ''
  LIMIT 3

```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-048/attempt-01/sql/S37.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-048/attempt-01/sql/S37.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-048/attempt-01/results/S37.rows.jsonl)；完整：True；SHA256：`9196a83f963142b6b491c24c64e7894d6674fc3223f8aa7c094b30d9f04cb231`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "sheet1", "kind": "base", "block": null, "base_tables": ["sheet1"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |

