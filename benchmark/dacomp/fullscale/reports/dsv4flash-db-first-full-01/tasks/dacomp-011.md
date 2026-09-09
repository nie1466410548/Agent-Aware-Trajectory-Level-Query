# dacomp-011

Some people believe that the higher the parents' level of education, the better their chil…

运行：已提交。官方未评分。全部 SQL 尝试/成功 30/27；数据 SQL 28/25；Python 4 次。

完整原题：

Some people believe that the higher the parents' level of education, the better their children's academic performance. Do the survey data in the table support this view? Using the data in the table, which factors can be analyzed as having a larger impact on students' academic performance?

| 表 | 行数 | 列数 |
| --- | --- | --- |
| sheet1 | 1000 | 15 |


实际路线（分析者依据 SQL/源码概括，不代表 Agent 自述）：检查学习与考试数据 → 比较父母教育背景对应的考试分数 → 多变量回归 → 按学习、社交、睡眠等分箱绘图。

数据库大小：200,704 字节。

## 数据 SQL

| SQL | 状态 | 基础表 | Join 输入/类型 | GROUP BY | 聚合表达式 | 结果行数 | 数据库 ms |
| --- | --- | --- | --- | --- | --- | --- | --- |
| [S3/Q1](#s3) | success | ["sheet1"] | 0 / {} | [] | ["COUNT(*)"] | 1 | 0.354 |
| [S4/Q2](#s4) | success | ["sheet1"] | 0 / {} | ["\"Parents' education level\""] | ["COUNT(*)", "AVG(\"Exam score\")", "MIN(\"Exam score\")", "MAX(\"Exam score\")"] | 4 | 0.988 |
| [S5/Q3](#s5) | success | ["sheet1"] | 0 / {} | ["Gender", "\"Part-time job\"", "\"Diet quality\"", "\"Internet quality\"", "\"Extracurricular activity participation\""] | ["COUNT(*)", "COUNT(*)", "COUNT(*)", "COUNT(*)", "COUNT(*)"] | 13 | 1.75 |
| [S6/Q4](#s6) | success | ["sheet1"] | 0 / {} | [] | ["AVG(\"Exam score\")", "MIN(\"Exam score\")", "MAX(\"Exam score\")", "AVG(\"Daily study time\")", "AVG(\"Social media usage time\")", "AVG(\"Attendance rate\")", "AVG(\"Sleep duration\")", "AVG(\"Exercise frequency\")", "AVG(\"Mental health score\")"] | 1 | 0.786 |
| [S7/Q5](#s7) | failed | ["sheet1"] | 0 / {} | ["\"Parents' education level\""] | ["COUNT(*)", "AVG(\"Exam score\")", "STDDEV(\"Exam score\")"] | unknown | 未取得；调用总时长 0.153 ms |
| [S8/Q6](#s8) | success | ["sheet1"] | 0 / {} | ["\"Parents' education level\"", "Gender"] | ["COUNT(*)", "AVG(\"Exam score\")"] | 12 | 1.067 |
| [S9/Q7](#s9) | success | ["sheet1"] | 0 / {} | ["\"Parents' education level\""] | ["AVG(\"Daily study time\")", "AVG(\"Social media usage time\")", "AVG(\"Attendance rate\")", "AVG(\"Sleep duration\")", "AVG(\"Exercise frequency\")", "AVG(\"Mental health score\")"] | 4 | 1.273 |
| [S10/Q8](#s10) | failed | ["sheet1"] | 0 / {} | [] | ["SUM((\"Exam score\" - avg_e) * (\"Daily study time\" - avg_s))", "COUNT(*)"] | unknown | 未取得；调用总时长 0.171 ms |
| [S11/Q9](#s11) | success | ["sheet1"] | 0 / {} | [] | ["COUNT(*)", "AVG(\"Exam score\")", "MIN(\"Exam score\")", "MAX(\"Exam score\")"] | 1 | 0.572 |
| [S12/Q10](#s12) | success | ["sheet1"] | 2 / {'CROSS': 1} | [] | ["COUNT(*)", "AVG(\"Exam score\")", "AVG(\"Daily study time\")", "AVG(\"Social media usage time\")", "AVG(\"Attendance rate\")", "AVG(\"Sleep duration\")", "AVG(\"Exercise frequency\")", "AVG(\"Mental health score\")", "AVG(Age)", "SUM((\"Exam score\" - m_e) * (\"Daily study time\" - m_s))", "SUM((\"Exam score\" - m_e) * (\"Social media usage time\" - m_so))", "SUM((\"Exam score\" - m_e) * (\"Attendance rate\" - m_a))", "SUM((\"Exam score\" - m_e) * (\"Sleep duration\" - m_sl))", "SUM((\"Exam score\" - m_e) * (\"Exercise frequency\" - m_ex))", "SUM((\"Exam score\" - m_e) * (\"Mental health score\" - m_mh))", "SUM((\"Exam score\" - m_e) * (Age - m_age))", "SUM((\"Exam score\" - m_e) * (\"Exam score\" - m_e))", "SUM((\"Daily study time\" - m_s) * (\"Daily study time\" - m_s))", "SUM((\"Exam score\" - m_e) * (\"Exam score\" - m_e))", "SUM((\"Social media usage time\" - m_so) * (\"Social media usage time\" - m_so))", "SUM((\"Exam score\" - m_e) * (\"Exam score\" - m_e))", "SUM((\"Attendance rate\" - m_a) * (\"Attendance rate\" - m_a))", "SUM((\"Exam score\" - m_e) * (\"Exam score\" - m_e))", "SUM((\"Sleep duration\" - m_sl) * (\"Sleep duration\" - m_sl))", "SUM((\"Exam score\" - m_e) * (\"Exam score\" - m_e))", "SUM((\"Exercise frequency\" - m_ex) * (\"Exercise frequency\" - m_ex))", "SUM((\"Exam score\" - m_e) * (\"Exam score\" - m_e))", "SUM((\"Mental health score\" - m_mh) * (\"Mental health score\" - m_mh))", "SUM((\"Exam score\" - m_e) * (\"Exam score\" - m_e))", "SUM((Age - m_age) * (Age - m_age))"] | 1 | 2.462 |
| [S13/Q11](#s13) | success | ["sheet1"] | 0 / {} | ["\"Parents' education level\""] | ["COUNT(*)", "AVG(\"Exam score\")", "SUM(\"Exam score\" * \"Exam score\")", "COUNT(*)", "COUNT(*)", "SUM(\"Exam score\")", "SUM(\"Exam score\")"] | 4 | 1.046 |
| [S14/Q12](#s14) | failed | ["sheet1"] | 0 / {} | ["\"Part-time job\""] | ["COUNT(*)", "AVG(\"Exam score\")", "STDDEV(\"Exam score\")"] | unknown | 未取得；调用总时长 0.152 ms |
| [S15/Q13](#s15) | success | ["sheet1"] | 0 / {} | ["\"Diet quality\""] | ["COUNT(*)", "AVG(\"Exam score\")"] | 3 | 0.807 |
| [S16/Q14](#s16) | success | ["sheet1"] | 0 / {} | ["\"Internet quality\""] | ["COUNT(*)", "AVG(\"Exam score\")"] | 3 | 0.728 |
| [S17/Q15](#s17) | success | ["sheet1"] | 0 / {} | ["\"Extracurricular activity participation\""] | ["COUNT(*)", "AVG(\"Exam score\")"] | 2 | 0.735 |
| [S18/Q16](#s18) | success | ["sheet1"] | 0 / {} | ["Gender"] | ["COUNT(*)", "AVG(\"Exam score\")"] | 3 | 0.66 |
| [S19/Q17](#s19) | success | ["sheet1"] | 0 / {} | ["CASE WHEN \"Daily study time\" < 2 THEN '<2h' WHEN \"Daily study time\" < 4 THEN '2-4h' WHEN \"Daily study time\" < 6 THEN '4-6h' ELSE '6h+' END"] | ["COUNT(*)", "AVG(\"Exam score\")", "AVG(\"Social media usage time\")", "AVG(\"Attendance rate\")", "AVG(\"Mental health score\")"] | 4 | 1.046 |
| [S20/Q18](#s20) | success | ["sheet1"] | 0 / {} | ["CASE WHEN \"Mental health score\" <= 3 THEN 'Low (0-3)' WHEN \"Mental health score\" <= 6 THEN 'Medium (4-6)' ELSE 'High (7-10)' END"] | ["COUNT(*)", "AVG(\"Exam score\")", "AVG(\"Daily study time\")"] | 3 | 0.883 |
| [S21/Q19](#s21) | success | ["sheet1"] | 0 / {} | ["CASE WHEN \"Attendance rate\" < 70 THEN '<70%' WHEN \"Attendance rate\" < 85 THEN '70-85%' WHEN \"Attendance rate\" < 95 THEN '85-95%' ELSE '95%+' END"] | ["COUNT(*)", "AVG(\"Exam score\")", "AVG(\"Daily study time\")"] | 4 | 0.949 |
| [S22/Q20](#s22) | success | ["sheet1"] | 0 / {} | ["\"Parents' education level\"", "CASE WHEN \"Daily study time\" < 2 THEN '<2h' WHEN \"Daily study time\" < 4 THEN '2-4h' WHEN \"Daily study time\" < 6 THEN '4-6h' ELSE '6h+' END"] | ["COUNT(*)", "AVG(\"Exam score\")"] | 16 | 1.32 |
| [S23/Q21](#s23) | success | ["sheet1"] | 0 / {} | ["\"Parents' education level\"", "\"Part-time job\""] | ["COUNT(*)", "AVG(\"Exam score\")"] | 8 | 1.057 |
| [S24/Q22](#s24) | success | ["sheet1"] | 0 / {} | ["\"Parents' education level\"", "\"Diet quality\""] | ["COUNT(*)", "AVG(\"Exam score\")"] | 12 | 1.216 |
| [S25/Q23](#s25) | success | ["sheet1"] | 0 / {} | [] | [] | 1000 | 3.563 |
| [S26/Q24](#s26) | success | ["sheet1"] | 0 / {} | [] | [] | 1000 | 3.151 |
| [S27/Q25](#s27) | success | ["sheet1"] | 0 / {} | [] | [] | 1000 | 3.199 |
| [S28/Q26](#s28) | success | ["sheet1"] | 0 / {} | [] | [] | 1000 | 3.225 |
| [S29/Q27](#s29) | success | ["sheet1"] | 0 / {} | ["CASE WHEN \"Parents' education level\" IS NULL THEN 'Missing' ELSE \"Parents' education level\" END"] | ["COUNT(*)", "AVG(\"Exam score\")", "AVG(\"Daily study time\")", "AVG(\"Social media usage time\")", "AVG(\"Attendance rate\")", "AVG(\"Sleep duration\")", "AVG(\"Exercise frequency\")", "AVG(\"Mental health score\")"] | 4 | 1.311 |
| [S30/Q28](#s30) | success | ["sheet1"] | 0 / {} | ["CASE WHEN \"Parents' education level\" IS NULL THEN 'Missing' ELSE \"Parents' education level\" END", "\"Diet quality\""] | ["COUNT(*)", "AVG(\"Exam score\")"] | 12 | 1.065 |


## 元数据和设置

| SQL | 类别 | 状态 | 内容 |
| --- | --- | --- | --- |
| S1 | connection_setup | success | PRAGMA query_only=ON |
| S2 | metadata | success | SELECT name,sql FROM sqlite_master WHERE type='table' ORDER BY name |


## Python 与执行位置

人工源码审查：**reviewed_with_statistical_exceptions_and_SQL_capable_preparation**。Python implements ANOVA, Kruskal-Wallis, pairwise tests and multiple regression, and renders figures. Intermediate matrix reductions belong to those statistical procedures. Separate null-count checks and categorical binning for plots are SQL-capable preparation performed in Python; this is not labeled fully strict database-first. [证据](../reviews/dacomp-011.json)。

P1：SQLite doesn't support ANOVA, Kruskal-Wallis tests, or multiple regression. I need to load the data into Python to perform statistical hypothesis testing and regression analysis to determine the significance and relative importance of various factors on exam scores.

[源码](../../../runs/dsv4flash-db-first-full-01/dacomp-011/attempt-01/python/P1.py)；[输出](../../../runs/dsv4flash-db-first-full-01/dacomp-011/attempt-01/python/P1.stdout)；[错误](../../../runs/dsv4flash-db-first-full-01/dacomp-011/attempt-01/python/P1.stderr)。检出需人工核验的 SQL 可实现操作：.query(；不能仅凭理由判为合规。

P2：SQLite cannot compute non-parametric hypothesis tests (Kruskal-Wallis, Mann-Whitney U) or ANOVA effect sizes. These statistical procedures require scipy in Python, so I load only the needed Exam score data by parent education group.

[源码](../../../runs/dsv4flash-db-first-full-01/dacomp-011/attempt-01/python/P2.py)；[输出](../../../runs/dsv4flash-db-first-full-01/dacomp-011/attempt-01/python/P2.stdout)；[错误](../../../runs/dsv4flash-db-first-full-01/dacomp-011/attempt-01/python/P2.stderr)。检出需人工核验的 SQL 可实现操作：.query(；不能仅凭理由判为合规。

P3：SQLite cannot perform multiple regression, standardized coefficients, or significance testing for regression coefficients. This requires matrix operations from numpy and scipy distributions.

[源码](../../../runs/dsv4flash-db-first-full-01/dacomp-011/attempt-01/python/P3.py)；[输出](../../../runs/dsv4flash-db-first-full-01/dacomp-011/attempt-01/python/P3.stdout)；[错误](../../../runs/dsv4flash-db-first-full-01/dacomp-011/attempt-01/python/P3.stderr)。检出需人工核验的 SQL 可实现操作：.query(；不能仅凭理由判为合规。

P4：SQLite cannot create visualizations. I need matplotlib/seaborn to produce the boxplots, scatter plots, and bar chart that illustrate the relationships between various factors and exam scores.

[源码](../../../runs/dsv4flash-db-first-full-01/dacomp-011/attempt-01/python/P4.py)；[输出](../../../runs/dsv4flash-db-first-full-01/dacomp-011/attempt-01/python/P4.stdout)；[错误](../../../runs/dsv4flash-db-first-full-01/dacomp-011/attempt-01/python/P4.stderr)。检出需人工核验的 SQL 可实现操作：.query(；不能仅凭理由判为合规。

## 优化机会

已验证候选。筛选限于精确 SQL、相同自包含 CTE、相同单表完整过滤、可分解单表聚合；未覆盖任意 Join 等价和一般谓词蕴含。全部候选都是 offline，未测在线预测。

| 候选 | 类型 | 已有结果 | 覆盖 SQL | 后续次数 | 中间行数 | 验证 | 成本 |
| --- | --- | --- | --- | --- | --- | --- | --- |
| C1 | exact-result reuse | True | ["S25", "S26", "S27", "S28"] | 3 | 1000 | verified | Not benchmarked; correctness alone does not establish net speedup. |
| C2 | aggregate MV | False | ["S3", "S4", "S6", "S8", "S9", "S13", "S15", "S16", "S17", "S18", "S19", "S20", "S21", "S22", "S23", "S24", "S29", "S30"] | 17 | 875 | verified | Not benchmarked; correctness alone does not establish net speedup. |


已验证覆盖（含触发查询、候选并集去重）：22/25 条成功数据 SQL。正确性仅针对当前数据库快照；未测性能的候选不能声称已加速。

[完整 build/rewrite 与比较证据](dacomp-011.analysis.json)。

### C2：aggregate MV

Union of grouping keys; decomposable aggregate states; AVG uses SUM and non-NULL COUNT.

原查询 [S3](#s3), [S4](#s4), [S6](#s6), [S8](#s8), [S9](#s9), [S13](#s13), [S15](#s15), [S16](#s16), [S17](#s17), [S18](#s18), [S19](#s19), [S20](#s20), [S21](#s21), [S22](#s22), [S23](#s23), [S24](#s24), [S29](#s29), [S30](#s30) → 新增共享状态 C2 → 后续 17 次可复用。该构建点为事后假设，不代表 Agent 当时预知后续。

构建定义：

```sql
SELECT "Parents' education level" AS __g0, gender AS __g1, "Diet quality" AS __g2, "Internet quality" AS __g3, "Extracurricular activity participation" AS __g4, CASE WHEN "Daily study time" < 2 THEN '<2h' WHEN "Daily study time" < 4 THEN '2-4h' WHEN "Daily study time" < 6 THEN '4-6h' ELSE '6h+' END AS __g5, CASE WHEN "Mental health score" <= 3 THEN 'Low (0-3)' WHEN "Mental health score" <= 6 THEN 'Medium (4-6)' ELSE 'High (7-10)' END AS __g6, CASE WHEN "Attendance rate" < 70 THEN '<70%' WHEN "Attendance rate" < 85 THEN '70-85%' WHEN "Attendance rate" < 95 THEN '85-95%' ELSE '95%+' END AS __g7, "Part-time job" AS __g8, CASE WHEN "Parents' education level" IS NULL THEN 'Missing' ELSE "Parents' education level" END AS __g9, COUNT(*) AS __a0, SUM("Exam score") AS __a1_sum, COUNT("Exam score") AS __a1_n, MIN("Exam score") AS __a2, MAX("Exam score") AS __a3, SUM("Daily study time") AS __a4_sum, COUNT("Daily study time") AS __a4_n, SUM("Social media usage time") AS __a5_sum, COUNT("Social media usage time") AS __a5_n, SUM("Attendance rate") AS __a6_sum, COUNT("Attendance rate") AS __a6_n, SUM("Sleep duration") AS __a7_sum, COUNT("Sleep duration") AS __a7_n, SUM("Exercise frequency") AS __a8_sum, COUNT("Exercise frequency") AS __a8_n, SUM("Mental health score") AS __a9_sum, COUNT("Mental health score") AS __a9_n, SUM("Exam score" * "Exam score") AS __a10, SUM("Exam score") AS __a11 FROM "sheet1"  GROUP BY "Parents' education level", gender, "Diet quality", "Internet quality", "Extracurricular activity participation", CASE WHEN "Daily study time" < 2 THEN '<2h' WHEN "Daily study time" < 4 THEN '2-4h' WHEN "Daily study time" < 6 THEN '4-6h' ELSE '6h+' END, CASE WHEN "Mental health score" <= 3 THEN 'Low (0-3)' WHEN "Mental health score" <= 6 THEN 'Medium (4-6)' ELSE 'High (7-10)' END, CASE WHEN "Attendance rate" < 70 THEN '<70%' WHEN "Attendance rate" < 85 THEN '70-85%' WHEN "Attendance rate" < 95 THEN '85-95%' ELSE '95%+' END, "Part-time job", CASE WHEN "Parents' education level" IS NULL THEN 'Missing' ELSE "Parents' education level" END
```

受益查询 S3 的改写示例：

```sql
SELECT SUM(__a0) AS total_rows FROM temp.reuse_candidate
```

| 原 SQL | 列名一致 | 结果一致 | 比较方法 |
| --- | --- | --- | --- |
| S3 | True | True | exact_multiset |
| S4 | True | True | ordered_numeric_tolerance |
| S6 | True | True | exact_multiset |
| S8 | True | True | ordered_numeric_tolerance |
| S9 | True | True | ordered_numeric_tolerance |
| S13 | True | True | ordered_numeric_tolerance |
| S15 | True | True | ordered_numeric_tolerance |
| S16 | True | True | ordered_numeric_tolerance |
| S17 | True | True | ordered_numeric_tolerance |
| S18 | True | True | ordered_numeric_tolerance |
| S19 | True | True | ordered_numeric_tolerance |
| S20 | True | True | ordered_numeric_tolerance |
| S21 | True | True | ordered_numeric_tolerance |
| S22 | True | True | ordered_numeric_tolerance |
| S23 | True | True | ordered_numeric_tolerance |
| S24 | True | True | ordered_numeric_tolerance |
| S29 | True | True | ordered_numeric_tolerance |
| S30 | True | True | ordered_numeric_tolerance |


验证状态：verified；成本结论：Not benchmarked; correctness alone does not establish net speedup.

### C1：exact-result reuse

Identical normalized SQL and parameters; archive equality checked.

原查询 [S25](#s25), [S26](#s26), [S27](#s27), [S28](#s28) → 保留前序结果 S25 → 后续 3 次可复用。该构建点为事后假设，不代表 Agent 当时预知后续。

| 原 SQL | 列名一致 | 结果一致 | 比较方法 |
| --- | --- | --- | --- |
| S26 | True | True | exact_multiset |
| S27 | True | True | exact_multiset |
| S28 | True | True | exact_multiset |


验证状态：verified；成本结论：Not benchmarked; correctness alone does not establish net speedup.

结果依赖：自动记录 SQL→Python 的接口父调用，以及源码中引用归档文件的消费者；字面值相同不认定因果。模型方向选择需要人工读取消息，尚未做全面因果标注。

[原始报告](../../../runs/dsv4flash-db-first-full-01/dacomp-011/attempt-01/answer.md)；[统一消息](../../../runs/dsv4flash-db-first-full-01/dacomp-011/attempt-01/messages.jsonl)；[原始 OpenCode 事件](../../../runs/dsv4flash-db-first-full-01/dacomp-011/attempt-01/opencode.jsonl)；[SQL 引擎日志](../../../runs/dsv4flash-db-first-full-01/dacomp-011/attempt-01/sql_journal.jsonl)。

[可读报告（本地图片链接规范化）](../answers/dacomp-011.md)。原始回答保留，分析结论未改写。

## S1

类别 `connection_setup`；来源 `connection`；调用 `717318da5fe84d67bcbe683b2dbf7d6a`；状态 `success`。

```sql
PRAGMA query_only=ON
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-011/attempt-01/sql/S1.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-011/attempt-01/sql/S1.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-011/attempt-01/results/S1.rows.jsonl)；完整：True；SHA256：`e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`。

## S2

类别 `metadata`；来源 `list_db`；调用 `717318da5fe84d67bcbe683b2dbf7d6a`；状态 `success`。

```sql
SELECT name,sql FROM sqlite_master WHERE type='table' ORDER BY name
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-011/attempt-01/sql/S2.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-011/attempt-01/sql/S2.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-011/attempt-01/results/S2.rows.jsonl)；完整：True；SHA256：`943fe944781c972aaf1e9f6c08d288804a0621264afd085297f3ea3fc70817b4`。

## S3

类别 `data`；来源 `query_db`；调用 `972760ab2e8d4d3db2d1863ff961f076`；状态 `success`。

```sql
SELECT COUNT(*) AS total_rows FROM sheet1
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-011/attempt-01/sql/S3.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-011/attempt-01/sql/S3.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-011/attempt-01/results/S3.rows.jsonl)；完整：True；SHA256：`e3ed33dc26a723b8481ca677e38dc4a6e8700aeec312afdd02c9dd92374161a2`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "sheet1", "kind": "base", "block": null, "base_tables": ["sheet1"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |


## S4

类别 `data`；来源 `query_db`；调用 `967fbe0f4a8a42309e1dcdd3c929eed9`；状态 `success`。

```sql
SELECT "Parents' education level" AS parent_edu, COUNT(*) AS n, ROUND(AVG("Exam score"),2) AS avg_exam, ROUND(MIN("Exam score"),2) AS min_exam, ROUND(MAX("Exam score"),2) AS max_exam FROM sheet1 GROUP BY "Parents' education level" ORDER BY avg_exam DESC
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-011/attempt-01/sql/S4.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-011/attempt-01/sql/S4.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-011/attempt-01/results/S4.rows.jsonl)；完整：True；SHA256：`a9b16f4946a4e3be12fc848fc0f1937d12a72d2ce2368fbbbeaef1cf427cfa0d`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "sheet1", "kind": "base", "block": null, "base_tables": ["sheet1"]}] | [] | ["\"Parents' education level\""] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |
| B1 | AVG("Exam score") | [{"table": "sheet1", "column": "Exam score"}] | [] | False |
| B1 | MIN("Exam score") | [{"table": "sheet1", "column": "Exam score"}] | [] | False |
| B1 | MAX("Exam score") | [{"table": "sheet1", "column": "Exam score"}] | [] | False |


## S5

类别 `data`；来源 `query_db`；调用 `04425d0aa44242ce8f5cb5c8bcbc7797`；状态 `success`。

```sql
SELECT 'Gender' AS col, Gender AS val, COUNT(*) AS n FROM sheet1 GROUP BY Gender
UNION ALL
SELECT 'Part-time job', "Part-time job", COUNT(*) FROM sheet1 GROUP BY "Part-time job"
UNION ALL
SELECT 'Diet quality', "Diet quality", COUNT(*) FROM sheet1 GROUP BY "Diet quality"
UNION ALL
SELECT 'Internet quality', "Internet quality", COUNT(*) FROM sheet1 GROUP BY "Internet quality"
UNION ALL
SELECT 'Extracurricular', "Extracurricular activity participation", COUNT(*) FROM sheet1 GROUP BY "Extracurricular activity participation"
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-011/attempt-01/sql/S5.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-011/attempt-01/sql/S5.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-011/attempt-01/results/S5.rows.jsonl)；完整：True；SHA256：`97e9e6005bada25ebedf771bb0599ec894b31d124902e2493ac7968ce26e3261`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "sheet1", "kind": "base", "block": null, "base_tables": ["sheet1"]}] | [] | ["Gender"] |
| B2 | [{"alias": "sheet1", "kind": "base", "block": null, "base_tables": ["sheet1"]}] | [] | ["\"Part-time job\""] |
| B3 | [] | [] | [] |
| B4 | [{"alias": "sheet1", "kind": "base", "block": null, "base_tables": ["sheet1"]}] | [] | ["\"Diet quality\""] |
| B5 | [] | [] | [] |
| B6 | [{"alias": "sheet1", "kind": "base", "block": null, "base_tables": ["sheet1"]}] | [] | ["\"Internet quality\""] |
| B7 | [] | [] | [] |
| B8 | [{"alias": "sheet1", "kind": "base", "block": null, "base_tables": ["sheet1"]}] | [] | ["\"Extracurricular activity participation\""] |
| B9 | [] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |
| B2 | COUNT(*) | [] | [] | True |
| B4 | COUNT(*) | [] | [] | True |
| B6 | COUNT(*) | [] | [] | True |
| B8 | COUNT(*) | [] | [] | True |


## S6

类别 `data`；来源 `query_db`；调用 `40482e221fe04457a7d9ef5c80b7c551`；状态 `success`。

```sql
SELECT ROUND(AVG("Exam score"),2) AS avg_exam, ROUND(MIN("Exam score"),2) AS min_exam, ROUND(MAX("Exam score"),2) AS max_exam, ROUND(AVG("Daily study time"),2) AS avg_study, ROUND(AVG("Social media usage time"),2) AS avg_social, ROUND(AVG("Attendance rate"),2) AS avg_attendance, ROUND(AVG("Sleep duration"),2) AS avg_sleep, ROUND(AVG("Exercise frequency"),2) AS avg_exercise, ROUND(AVG("Mental health score"),2) AS avg_mh FROM sheet1
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-011/attempt-01/sql/S6.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-011/attempt-01/sql/S6.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-011/attempt-01/results/S6.rows.jsonl)；完整：True；SHA256：`a306b2434c667819ad08212300c93d47aa8b6e89a59a9443c946653c51887bd2`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "sheet1", "kind": "base", "block": null, "base_tables": ["sheet1"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | AVG("Exam score") | [{"table": "sheet1", "column": "Exam score"}] | [] | False |
| B1 | MIN("Exam score") | [{"table": "sheet1", "column": "Exam score"}] | [] | False |
| B1 | MAX("Exam score") | [{"table": "sheet1", "column": "Exam score"}] | [] | False |
| B1 | AVG("Daily study time") | [{"table": "sheet1", "column": "Daily study time"}] | [] | False |
| B1 | AVG("Social media usage time") | [{"table": "sheet1", "column": "Social media usage time"}] | [] | False |
| B1 | AVG("Attendance rate") | [{"table": "sheet1", "column": "Attendance rate"}] | [] | False |
| B1 | AVG("Sleep duration") | [{"table": "sheet1", "column": "Sleep duration"}] | [] | False |
| B1 | AVG("Exercise frequency") | [{"table": "sheet1", "column": "Exercise frequency"}] | [] | False |
| B1 | AVG("Mental health score") | [{"table": "sheet1", "column": "Mental health score"}] | [] | False |


## S7

类别 `data`；来源 `query_db`；调用 `a873664c59394ec8bd6f550658e40937`；状态 `failed`。

```sql
SELECT "Parents' education level" AS parent_edu, ROUND(AVG("Exam score"),2) AS avg_exam, ROUND(STDEV("Exam score"),2) AS std_exam, COUNT(*) AS n FROM sheet1 GROUP BY "Parents' education level" ORDER BY parent_edu
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-011/attempt-01/sql/S7.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-011/attempt-01/sql/S7.parameters.json)。

错误：`OperationalError('no such function: STDEV')`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "sheet1", "kind": "base", "block": null, "base_tables": ["sheet1"]}] | [] | ["\"Parents' education level\""] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |
| B1 | AVG("Exam score") | [{"table": "sheet1", "column": "Exam score"}] | [] | False |
| B1 | STDDEV("Exam score") | [{"table": "sheet1", "column": "Exam score"}] | [] | False |


## S8

类别 `data`；来源 `query_db`；调用 `0a7256772d884742b50e5ae63fc17d3c`；状态 `success`。

```sql
SELECT "Parents' education level" AS parent_edu, Gender, ROUND(AVG("Exam score"),2) AS avg_exam, COUNT(*) AS n FROM sheet1 GROUP BY "Parents' education level", Gender ORDER BY parent_edu, Gender
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-011/attempt-01/sql/S8.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-011/attempt-01/sql/S8.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-011/attempt-01/results/S8.rows.jsonl)；完整：True；SHA256：`46e85b1ccab979f873becf46a67a3ecd5b5590d52d61704839b1523d4c7a71ac`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "sheet1", "kind": "base", "block": null, "base_tables": ["sheet1"]}] | [] | ["\"Parents' education level\"", "Gender"] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |
| B1 | AVG("Exam score") | [{"table": "sheet1", "column": "Exam score"}] | [] | False |


## S9

类别 `data`；来源 `query_db`；调用 `e0c27c819de34f8f87f4efd90c6d03e4`；状态 `success`。

```sql
SELECT "Parents' education level" AS parent_edu, 
  ROUND(AVG("Daily study time"),2) AS avg_study,
  ROUND(AVG("Social media usage time"),2) AS avg_social,
  ROUND(AVG("Attendance rate"),2) AS avg_attendance,
  ROUND(AVG("Sleep duration"),2) AS avg_sleep,
  ROUND(AVG("Exercise frequency"),2) AS avg_exercise,
  ROUND(AVG("Mental health score"),2) AS avg_mh
FROM sheet1 GROUP BY "Parents' education level" ORDER BY parent_edu
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-011/attempt-01/sql/S9.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-011/attempt-01/sql/S9.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-011/attempt-01/results/S9.rows.jsonl)；完整：True；SHA256：`222cfec725c19f1355f4307307f89550d5bd6c2fc095876c37241153cd049b94`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "sheet1", "kind": "base", "block": null, "base_tables": ["sheet1"]}] | [] | ["\"Parents' education level\""] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | AVG("Daily study time") | [{"table": "sheet1", "column": "Daily study time"}] | [] | False |
| B1 | AVG("Social media usage time") | [{"table": "sheet1", "column": "Social media usage time"}] | [] | False |
| B1 | AVG("Attendance rate") | [{"table": "sheet1", "column": "Attendance rate"}] | [] | False |
| B1 | AVG("Sleep duration") | [{"table": "sheet1", "column": "Sleep duration"}] | [] | False |
| B1 | AVG("Exercise frequency") | [{"table": "sheet1", "column": "Exercise frequency"}] | [] | False |
| B1 | AVG("Mental health score") | [{"table": "sheet1", "column": "Mental health score"}] | [] | False |


## S10

类别 `data`；来源 `query_db`；调用 `6b96b2ba6eb64680b375630214f14f8b`；状态 `failed`。

```sql
SELECT 
  ROUND(SUM(("Exam score"-avg_e)*("Daily study time"-avg_s))/ (COUNT(*)*STDDEV_agg("Exam score")*STDDEV_agg("Daily study time")),4) AS corr_study
FROM sheet1
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-011/attempt-01/sql/S10.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-011/attempt-01/sql/S10.parameters.json)。

错误：`OperationalError('no such column: avg_e')`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "sheet1", "kind": "base", "block": null, "base_tables": ["sheet1"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | SUM(("Exam score" - avg_e) * ("Daily study time" - avg_s)) | [{"table": "sheet1", "column": "Exam score"}, {"unknown": "avg_e"}, {"table": "sheet1", "column": "Daily study time"}, {"unknown": "avg_s"}] | [] | False |
| B1 | COUNT(*) | [] | [] | True |


未解析列血缘：[{"block": "B1", "column": "avg_e", "reason": "ambiguous_or_missing_source"}, {"block": "B1", "column": "avg_s", "reason": "ambiguous_or_missing_source"}, {"block": "B1", "column": "avg_e", "reason": "ambiguous_or_missing_source"}, {"block": "B1", "column": "avg_s", "reason": "ambiguous_or_missing_source"}]

## S11

类别 `data`；来源 `query_db`；调用 `df74765410eb4a6fab7956d1fddbacf5`；状态 `success`。

```sql
SELECT COUNT(*) AS n, ROUND(AVG("Exam score"),2) AS avg_exam, ROUND(MIN("Exam score"),2) AS min_exam, ROUND(MAX("Exam score"),2) AS max_exam FROM sheet1 WHERE "Parents' education level" IS NOT NULL
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-011/attempt-01/sql/S11.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-011/attempt-01/sql/S11.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-011/attempt-01/results/S11.rows.jsonl)；完整：True；SHA256：`527cfd7fe5d87dcbbbd5c835825801bc975dd0a63165e1a0e62e4273bff0b2bb`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "sheet1", "kind": "base", "block": null, "base_tables": ["sheet1"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |
| B1 | AVG("Exam score") | [{"table": "sheet1", "column": "Exam score"}] | [] | False |
| B1 | MIN("Exam score") | [{"table": "sheet1", "column": "Exam score"}] | [] | False |
| B1 | MAX("Exam score") | [{"table": "sheet1", "column": "Exam score"}] | [] | False |


## S12

类别 `data`；来源 `query_db`；调用 `2edc3937a74a42ab8a1964b8766aef6e`；状态 `success`。

```sql
WITH stats AS (
  SELECT 
    COUNT(*) AS n,
    AVG("Exam score") AS m_e,
    AVG("Daily study time") AS m_s,
    AVG("Social media usage time") AS m_so,
    AVG("Attendance rate") AS m_a,
    AVG("Sleep duration") AS m_sl,
    AVG("Exercise frequency") AS m_ex,
    AVG("Mental health score") AS m_mh,
    AVG(Age) AS m_age
  FROM sheet1
)
SELECT
  ROUND(SUM(("Exam score"-m_e)*("Daily study time"-m_s))/SQRT(SUM(("Exam score"-m_e)*("Exam score"-m_e))*SUM(("Daily study time"-m_s)*("Daily study time"-m_s))),4) AS corr_study,
  ROUND(SUM(("Exam score"-m_e)*("Social media usage time"-m_so))/SQRT(SUM(("Exam score"-m_e)*("Exam score"-m_e))*SUM(("Social media usage time"-m_so)*("Social media usage time"-m_so))),4) AS corr_social,
  ROUND(SUM(("Exam score"-m_e)*("Attendance rate"-m_a))/SQRT(SUM(("Exam score"-m_e)*("Exam score"-m_e))*SUM(("Attendance rate"-m_a)*("Attendance rate"-m_a))),4) AS corr_attendance,
  ROUND(SUM(("Exam score"-m_e)*("Sleep duration"-m_sl))/SQRT(SUM(("Exam score"-m_e)*("Exam score"-m_e))*SUM(("Sleep duration"-m_sl)*("Sleep duration"-m_sl))),4) AS corr_sleep,
  ROUND(SUM(("Exam score"-m_e)*("Exercise frequency"-m_ex))/SQRT(SUM(("Exam score"-m_e)*("Exam score"-m_e))*SUM(("Exercise frequency"-m_ex)*("Exercise frequency"-m_ex))),4) AS corr_exercise,
  ROUND(SUM(("Exam score"-m_e)*("Mental health score"-m_mh))/SQRT(SUM(("Exam score"-m_e)*("Exam score"-m_e))*SUM(("Mental health score"-m_mh)*("Mental health score"-m_mh))),4) AS corr_mh,
  ROUND(SUM(("Exam score"-m_e)*(Age-m_age))/SQRT(SUM(("Exam score"-m_e)*("Exam score"-m_e))*SUM((Age-m_age)*(Age-m_age))),4) AS corr_age
FROM sheet1, stats
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-011/attempt-01/sql/S12.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-011/attempt-01/sql/S12.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-011/attempt-01/results/S12.rows.jsonl)；完整：True；SHA256：`6961a5221f976e59815f285bec12a1591d45e62af04e9f212f6ff7a4633814c5`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "sheet1", "kind": "base", "block": null, "base_tables": ["sheet1"]}] | [] | [] |
| B2 | [{"alias": "stats", "kind": "derived", "block": "B1", "base_tables": ["sheet1"]}, {"alias": "sheet1", "kind": "base", "block": null, "base_tables": ["sheet1"]}] | [{"type": "CROSS", "right": "stats", "on": null, "using": []}] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |
| B1 | AVG("Exam score") | [{"table": "sheet1", "column": "Exam score"}] | [] | False |
| B1 | AVG("Daily study time") | [{"table": "sheet1", "column": "Daily study time"}] | [] | False |
| B1 | AVG("Social media usage time") | [{"table": "sheet1", "column": "Social media usage time"}] | [] | False |
| B1 | AVG("Attendance rate") | [{"table": "sheet1", "column": "Attendance rate"}] | [] | False |
| B1 | AVG("Sleep duration") | [{"table": "sheet1", "column": "Sleep duration"}] | [] | False |
| B1 | AVG("Exercise frequency") | [{"table": "sheet1", "column": "Exercise frequency"}] | [] | False |
| B1 | AVG("Mental health score") | [{"table": "sheet1", "column": "Mental health score"}] | [] | False |
| B1 | AVG(Age) | [{"table": "sheet1", "column": "Age"}] | [] | False |
| B2 | SUM(("Exam score" - m_e) * ("Daily study time" - m_s)) | [{"table": "sheet1", "column": "Exam score"}, {"table": "sheet1", "column": "Exam score"}, {"table": "sheet1", "column": "Daily study time"}, {"table": "sheet1", "column": "Daily study time"}] | [] | False |
| B2 | SUM(("Exam score" - m_e) * ("Social media usage time" - m_so)) | [{"table": "sheet1", "column": "Exam score"}, {"table": "sheet1", "column": "Exam score"}, {"table": "sheet1", "column": "Social media usage time"}, {"table": "sheet1", "column": "Social media usage time"}] | [] | False |
| B2 | SUM(("Exam score" - m_e) * ("Attendance rate" - m_a)) | [{"table": "sheet1", "column": "Exam score"}, {"table": "sheet1", "column": "Exam score"}, {"table": "sheet1", "column": "Attendance rate"}, {"table": "sheet1", "column": "Attendance rate"}] | [] | False |
| B2 | SUM(("Exam score" - m_e) * ("Sleep duration" - m_sl)) | [{"table": "sheet1", "column": "Exam score"}, {"table": "sheet1", "column": "Exam score"}, {"table": "sheet1", "column": "Sleep duration"}, {"table": "sheet1", "column": "Sleep duration"}] | [] | False |
| B2 | SUM(("Exam score" - m_e) * ("Exercise frequency" - m_ex)) | [{"table": "sheet1", "column": "Exam score"}, {"table": "sheet1", "column": "Exam score"}, {"table": "sheet1", "column": "Exercise frequency"}, {"table": "sheet1", "column": "Exercise frequency"}] | [] | False |
| B2 | SUM(("Exam score" - m_e) * ("Mental health score" - m_mh)) | [{"table": "sheet1", "column": "Exam score"}, {"table": "sheet1", "column": "Exam score"}, {"table": "sheet1", "column": "Mental health score"}, {"table": "sheet1", "column": "Mental health score"}] | [] | False |
| B2 | SUM(("Exam score" - m_e) * (Age - m_age)) | [{"table": "sheet1", "column": "Exam score"}, {"table": "sheet1", "column": "Exam score"}, {"table": "sheet1", "column": "Age"}, {"table": "sheet1", "column": "Age"}] | [] | False |
| B2 | SUM(("Exam score" - m_e) * ("Exam score" - m_e)) | [{"table": "sheet1", "column": "Exam score"}, {"table": "sheet1", "column": "Exam score"}, {"table": "sheet1", "column": "Exam score"}, {"table": "sheet1", "column": "Exam score"}] | [] | False |
| B2 | SUM(("Daily study time" - m_s) * ("Daily study time" - m_s)) | [{"table": "sheet1", "column": "Daily study time"}, {"table": "sheet1", "column": "Daily study time"}, {"table": "sheet1", "column": "Daily study time"}, {"table": "sheet1", "column": "Daily study time"}] | [] | False |
| B2 | SUM(("Exam score" - m_e) * ("Exam score" - m_e)) | [{"table": "sheet1", "column": "Exam score"}, {"table": "sheet1", "column": "Exam score"}, {"table": "sheet1", "column": "Exam score"}, {"table": "sheet1", "column": "Exam score"}] | [] | False |
| B2 | SUM(("Social media usage time" - m_so) * ("Social media usage time" - m_so)) | [{"table": "sheet1", "column": "Social media usage time"}, {"table": "sheet1", "column": "Social media usage time"}, {"table": "sheet1", "column": "Social media usage time"}, {"table": "sheet1", "column": "Social media usage time"}] | [] | False |
| B2 | SUM(("Exam score" - m_e) * ("Exam score" - m_e)) | [{"table": "sheet1", "column": "Exam score"}, {"table": "sheet1", "column": "Exam score"}, {"table": "sheet1", "column": "Exam score"}, {"table": "sheet1", "column": "Exam score"}] | [] | False |
| B2 | SUM(("Attendance rate" - m_a) * ("Attendance rate" - m_a)) | [{"table": "sheet1", "column": "Attendance rate"}, {"table": "sheet1", "column": "Attendance rate"}, {"table": "sheet1", "column": "Attendance rate"}, {"table": "sheet1", "column": "Attendance rate"}] | [] | False |
| B2 | SUM(("Exam score" - m_e) * ("Exam score" - m_e)) | [{"table": "sheet1", "column": "Exam score"}, {"table": "sheet1", "column": "Exam score"}, {"table": "sheet1", "column": "Exam score"}, {"table": "sheet1", "column": "Exam score"}] | [] | False |
| B2 | SUM(("Sleep duration" - m_sl) * ("Sleep duration" - m_sl)) | [{"table": "sheet1", "column": "Sleep duration"}, {"table": "sheet1", "column": "Sleep duration"}, {"table": "sheet1", "column": "Sleep duration"}, {"table": "sheet1", "column": "Sleep duration"}] | [] | False |
| B2 | SUM(("Exam score" - m_e) * ("Exam score" - m_e)) | [{"table": "sheet1", "column": "Exam score"}, {"table": "sheet1", "column": "Exam score"}, {"table": "sheet1", "column": "Exam score"}, {"table": "sheet1", "column": "Exam score"}] | [] | False |
| B2 | SUM(("Exercise frequency" - m_ex) * ("Exercise frequency" - m_ex)) | [{"table": "sheet1", "column": "Exercise frequency"}, {"table": "sheet1", "column": "Exercise frequency"}, {"table": "sheet1", "column": "Exercise frequency"}, {"table": "sheet1", "column": "Exercise frequency"}] | [] | False |
| B2 | SUM(("Exam score" - m_e) * ("Exam score" - m_e)) | [{"table": "sheet1", "column": "Exam score"}, {"table": "sheet1", "column": "Exam score"}, {"table": "sheet1", "column": "Exam score"}, {"table": "sheet1", "column": "Exam score"}] | [] | False |
| B2 | SUM(("Mental health score" - m_mh) * ("Mental health score" - m_mh)) | [{"table": "sheet1", "column": "Mental health score"}, {"table": "sheet1", "column": "Mental health score"}, {"table": "sheet1", "column": "Mental health score"}, {"table": "sheet1", "column": "Mental health score"}] | [] | False |
| B2 | SUM(("Exam score" - m_e) * ("Exam score" - m_e)) | [{"table": "sheet1", "column": "Exam score"}, {"table": "sheet1", "column": "Exam score"}, {"table": "sheet1", "column": "Exam score"}, {"table": "sheet1", "column": "Exam score"}] | [] | False |
| B2 | SUM((Age - m_age) * (Age - m_age)) | [{"table": "sheet1", "column": "Age"}, {"table": "sheet1", "column": "Age"}, {"table": "sheet1", "column": "Age"}, {"table": "sheet1", "column": "Age"}] | [] | False |


## S13

类别 `data`；来源 `query_db`；调用 `368ae34c2cbc43378fb6d128bcdd785b`；状态 `success`。

```sql
SELECT "Parents' education level" AS parent_edu, COUNT(*) AS n, ROUND(AVG("Exam score"),2) AS avg_exam,
  ROUND((SUM("Exam score"*"Exam score") - SUM("Exam score")*SUM("Exam score")/COUNT(*)) / (COUNT(*)-1), 2) AS var_exam
FROM sheet1 GROUP BY "Parents' education level" ORDER BY parent_edu
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-011/attempt-01/sql/S13.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-011/attempt-01/sql/S13.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-011/attempt-01/results/S13.rows.jsonl)；完整：True；SHA256：`44e20b3666aa06678a6df47048b181fd6582ebcb8889074be6a5ab24d0cd1567`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "sheet1", "kind": "base", "block": null, "base_tables": ["sheet1"]}] | [] | ["\"Parents' education level\""] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |
| B1 | AVG("Exam score") | [{"table": "sheet1", "column": "Exam score"}] | [] | False |
| B1 | SUM("Exam score" * "Exam score") | [{"table": "sheet1", "column": "Exam score"}, {"table": "sheet1", "column": "Exam score"}] | [] | False |
| B1 | COUNT(*) | [] | [] | True |
| B1 | COUNT(*) | [] | [] | True |
| B1 | SUM("Exam score") | [{"table": "sheet1", "column": "Exam score"}] | [] | False |
| B1 | SUM("Exam score") | [{"table": "sheet1", "column": "Exam score"}] | [] | False |


## S14

类别 `data`；来源 `query_db`；调用 `a0a9f65468c341acaee73be1bb3f256c`；状态 `failed`。

```sql
SELECT "Part-time job" AS val, COUNT(*) AS n, ROUND(AVG("Exam score"),2) AS avg_exam, ROUND(STDEV("Exam score"),2) AS std_exam FROM sheet1 GROUP BY "Part-time job"
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-011/attempt-01/sql/S14.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-011/attempt-01/sql/S14.parameters.json)。

错误：`OperationalError('no such function: STDEV')`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "sheet1", "kind": "base", "block": null, "base_tables": ["sheet1"]}] | [] | ["\"Part-time job\""] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |
| B1 | AVG("Exam score") | [{"table": "sheet1", "column": "Exam score"}] | [] | False |
| B1 | STDDEV("Exam score") | [{"table": "sheet1", "column": "Exam score"}] | [] | False |


## S15

类别 `data`；来源 `query_db`；调用 `6bf33f58d5be4cb1b37588f90ecf15e9`；状态 `success`。

```sql
SELECT "Diet quality" AS val, COUNT(*) AS n, ROUND(AVG("Exam score"),2) AS avg_exam FROM sheet1 GROUP BY "Diet quality" ORDER BY avg_exam DESC
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-011/attempt-01/sql/S15.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-011/attempt-01/sql/S15.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-011/attempt-01/results/S15.rows.jsonl)；完整：True；SHA256：`3371a3203773ea4c3de3056b8a469cf67b73d9598a93cd1296b6e0eb6045e28a`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "sheet1", "kind": "base", "block": null, "base_tables": ["sheet1"]}] | [] | ["\"Diet quality\""] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |
| B1 | AVG("Exam score") | [{"table": "sheet1", "column": "Exam score"}] | [] | False |


## S16

类别 `data`；来源 `query_db`；调用 `ddb3319a121d4d37bd1bb2ecfe11da4d`；状态 `success`。

```sql
SELECT "Internet quality" AS val, COUNT(*) AS n, ROUND(AVG("Exam score"),2) AS avg_exam FROM sheet1 GROUP BY "Internet quality" ORDER BY avg_exam DESC
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-011/attempt-01/sql/S16.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-011/attempt-01/sql/S16.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-011/attempt-01/results/S16.rows.jsonl)；完整：True；SHA256：`439df1e508cd885993021237c11505b8579ebd1b4fe86ae25728ff85966bd0cf`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "sheet1", "kind": "base", "block": null, "base_tables": ["sheet1"]}] | [] | ["\"Internet quality\""] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |
| B1 | AVG("Exam score") | [{"table": "sheet1", "column": "Exam score"}] | [] | False |


## S17

类别 `data`；来源 `query_db`；调用 `ebc7b2d525f54c40acb34c1181aed36e`；状态 `success`。

```sql
SELECT "Extracurricular activity participation" AS val, COUNT(*) AS n, ROUND(AVG("Exam score"),2) AS avg_exam FROM sheet1 GROUP BY "Extracurricular activity participation" ORDER BY avg_exam DESC
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-011/attempt-01/sql/S17.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-011/attempt-01/sql/S17.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-011/attempt-01/results/S17.rows.jsonl)；完整：True；SHA256：`ab38511129ae839fba3b231b321fb55bd5561be1adcdb82dd11350011f2b7bf8`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "sheet1", "kind": "base", "block": null, "base_tables": ["sheet1"]}] | [] | ["\"Extracurricular activity participation\""] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |
| B1 | AVG("Exam score") | [{"table": "sheet1", "column": "Exam score"}] | [] | False |


## S18

类别 `data`；来源 `query_db`；调用 `098a564868364c8883928867d23dae8d`；状态 `success`。

```sql
SELECT Gender AS val, COUNT(*) AS n, ROUND(AVG("Exam score"),2) AS avg_exam FROM sheet1 GROUP BY Gender ORDER BY avg_exam DESC
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-011/attempt-01/sql/S18.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-011/attempt-01/sql/S18.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-011/attempt-01/results/S18.rows.jsonl)；完整：True；SHA256：`2afafc5a6f3871acf6663299e4fb667c7973b9bcfc210b23ed152482d5ffb694`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "sheet1", "kind": "base", "block": null, "base_tables": ["sheet1"]}] | [] | ["Gender"] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |
| B1 | AVG("Exam score") | [{"table": "sheet1", "column": "Exam score"}] | [] | False |


## S19

类别 `data`；来源 `query_db`；调用 `206f279576194b1288838de0d7d52462`；状态 `success`。

```sql
SELECT 
  CASE 
    WHEN "Daily study time" < 2 THEN '<2h'
    WHEN "Daily study time" < 4 THEN '2-4h'
    WHEN "Daily study time" < 6 THEN '4-6h'
    ELSE '6h+'
  END AS study_cat,
  COUNT(*) AS n,
  ROUND(AVG("Exam score"),2) AS avg_exam,
  ROUND(AVG("Social media usage time"),2) AS avg_social,
  ROUND(AVG("Attendance rate"),2) AS avg_attendance,
  ROUND(AVG("Mental health score"),2) AS avg_mh
FROM sheet1
GROUP BY study_cat
ORDER BY avg_exam DESC
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-011/attempt-01/sql/S19.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-011/attempt-01/sql/S19.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-011/attempt-01/results/S19.rows.jsonl)；完整：True；SHA256：`defb5bcaea585f190c686bcc9451f39392b692ad3c9dc519aeddb0ea0e20e0da`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "sheet1", "kind": "base", "block": null, "base_tables": ["sheet1"]}] | [] | ["CASE WHEN \"Daily study time\" < 2 THEN '<2h' WHEN \"Daily study time\" < 4 THEN '2-4h' WHEN \"Daily study time\" < 6 THEN '4-6h' ELSE '6h+' END"] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |
| B1 | AVG("Exam score") | [{"table": "sheet1", "column": "Exam score"}] | [] | False |
| B1 | AVG("Social media usage time") | [{"table": "sheet1", "column": "Social media usage time"}] | [] | False |
| B1 | AVG("Attendance rate") | [{"table": "sheet1", "column": "Attendance rate"}] | [] | False |
| B1 | AVG("Mental health score") | [{"table": "sheet1", "column": "Mental health score"}] | [] | False |


## S20

类别 `data`；来源 `query_db`；调用 `6349b190c06840b990959e539ad348da`；状态 `success`。

```sql
SELECT 
  CASE 
    WHEN "Mental health score" <= 3 THEN 'Low (0-3)'
    WHEN "Mental health score" <= 6 THEN 'Medium (4-6)'
    ELSE 'High (7-10)'
  END AS mh_cat,
  COUNT(*) AS n,
  ROUND(AVG("Exam score"),2) AS avg_exam,
  ROUND(AVG("Daily study time"),2) AS avg_study
FROM sheet1
GROUP BY mh_cat
ORDER BY avg_exam DESC
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-011/attempt-01/sql/S20.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-011/attempt-01/sql/S20.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-011/attempt-01/results/S20.rows.jsonl)；完整：True；SHA256：`a00460ec65476e6b5bd8e00df3a9a0d7a97b4e3ccc2599f66810c044a2668e44`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "sheet1", "kind": "base", "block": null, "base_tables": ["sheet1"]}] | [] | ["CASE WHEN \"Mental health score\" <= 3 THEN 'Low (0-3)' WHEN \"Mental health score\" <= 6 THEN 'Medium (4-6)' ELSE 'High (7-10)' END"] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |
| B1 | AVG("Exam score") | [{"table": "sheet1", "column": "Exam score"}] | [] | False |
| B1 | AVG("Daily study time") | [{"table": "sheet1", "column": "Daily study time"}] | [] | False |


## S21

类别 `data`；来源 `query_db`；调用 `f1eafabb1984436daf1e76e51802dd70`；状态 `success`。

```sql
SELECT 
  CASE 
    WHEN "Attendance rate" < 70 THEN '<70%'
    WHEN "Attendance rate" < 85 THEN '70-85%'
    WHEN "Attendance rate" < 95 THEN '85-95%'
    ELSE '95%+'
  END AS attendance_cat,
  COUNT(*) AS n,
  ROUND(AVG("Exam score"),2) AS avg_exam,
  ROUND(AVG("Daily study time"),2) AS avg_study
FROM sheet1
GROUP BY attendance_cat
ORDER BY avg_exam DESC
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-011/attempt-01/sql/S21.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-011/attempt-01/sql/S21.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-011/attempt-01/results/S21.rows.jsonl)；完整：True；SHA256：`9c3aa5186e0c09f1e1f461fd88bb2d73bb64a4067f544f002359903cffa274cd`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "sheet1", "kind": "base", "block": null, "base_tables": ["sheet1"]}] | [] | ["CASE WHEN \"Attendance rate\" < 70 THEN '<70%' WHEN \"Attendance rate\" < 85 THEN '70-85%' WHEN \"Attendance rate\" < 95 THEN '85-95%' ELSE '95%+' END"] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |
| B1 | AVG("Exam score") | [{"table": "sheet1", "column": "Exam score"}] | [] | False |
| B1 | AVG("Daily study time") | [{"table": "sheet1", "column": "Daily study time"}] | [] | False |


## S22

类别 `data`；来源 `query_db`；调用 `0e00adece85d4010bba413d3b3c512c2`；状态 `success`。

```sql
SELECT "Parents' education level" AS parent_edu,
  CASE 
    WHEN "Daily study time" < 2 THEN '<2h'
    WHEN "Daily study time" < 4 THEN '2-4h'
    WHEN "Daily study time" < 6 THEN '4-6h'
    ELSE '6h+'
  END AS study_cat,
  COUNT(*) AS n,
  ROUND(AVG("Exam score"),2) AS avg_exam
FROM sheet1
GROUP BY parent_edu, study_cat
ORDER BY parent_edu, study_cat
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-011/attempt-01/sql/S22.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-011/attempt-01/sql/S22.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-011/attempt-01/results/S22.rows.jsonl)；完整：True；SHA256：`7a652a0b00bfb2c383d91c9d88eb41a24a8adaa10fe522a1523f9ecd524efa0d`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "sheet1", "kind": "base", "block": null, "base_tables": ["sheet1"]}] | [] | ["\"Parents' education level\"", "CASE WHEN \"Daily study time\" < 2 THEN '<2h' WHEN \"Daily study time\" < 4 THEN '2-4h' WHEN \"Daily study time\" < 6 THEN '4-6h' ELSE '6h+' END"] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |
| B1 | AVG("Exam score") | [{"table": "sheet1", "column": "Exam score"}] | [] | False |


## S23

类别 `data`；来源 `query_db`；调用 `30bead9b99224597afe01ef31da68ba0`；状态 `success`。

```sql
SELECT "Parents' education level" AS parent_edu,
  "Part-time job" AS pt_job,
  COUNT(*) AS n,
  ROUND(AVG("Exam score"),2) AS avg_exam
FROM sheet1
GROUP BY parent_edu, pt_job
ORDER BY parent_edu, pt_job
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-011/attempt-01/sql/S23.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-011/attempt-01/sql/S23.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-011/attempt-01/results/S23.rows.jsonl)；完整：True；SHA256：`ebf8c3053337f1cf183063b343d235cdd3b87cd6c2880bed22341f6dfd4cc5b3`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "sheet1", "kind": "base", "block": null, "base_tables": ["sheet1"]}] | [] | ["\"Parents' education level\"", "\"Part-time job\""] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |
| B1 | AVG("Exam score") | [{"table": "sheet1", "column": "Exam score"}] | [] | False |


## S24

类别 `data`；来源 `query_db`；调用 `a8c36b2f2e9a48f39ca8509216dcabac`；状态 `success`。

```sql
SELECT "Parents' education level" AS parent_edu,
  "Diet quality" AS diet,
  COUNT(*) AS n,
  ROUND(AVG("Exam score"),2) AS avg_exam
FROM sheet1
GROUP BY parent_edu, diet
ORDER BY parent_edu, diet
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-011/attempt-01/sql/S24.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-011/attempt-01/sql/S24.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-011/attempt-01/results/S24.rows.jsonl)；完整：True；SHA256：`33000bf6b5e2afc151032874e30fa9b7d1061d26334916c1e1a6104f5fff640a`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "sheet1", "kind": "base", "block": null, "base_tables": ["sheet1"]}] | [] | ["\"Parents' education level\"", "\"Diet quality\""] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |
| B1 | AVG("Exam score") | [{"table": "sheet1", "column": "Exam score"}] | [] | False |


## S25

类别 `data`；来源 `python`；调用 `ccd97b4c60bb4c01bb219c0443830524`；状态 `success`。

```sql
SELECT * FROM sheet1
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-011/attempt-01/sql/S25.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-011/attempt-01/sql/S25.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-011/attempt-01/results/S25.rows.jsonl)；完整：True；SHA256：`47bacbf2bf6a25252df3be44c0386eb9f5f28ea5fc1de4c783dba912c7df332f`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "sheet1", "kind": "base", "block": null, "base_tables": ["sheet1"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |


## S26

类别 `data`；来源 `python`；调用 `2a123c35226249ba869ac7e6511467ec`；状态 `success`。

```sql
SELECT * FROM sheet1
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-011/attempt-01/sql/S26.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-011/attempt-01/sql/S26.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-011/attempt-01/results/S26.rows.jsonl)；完整：True；SHA256：`47bacbf2bf6a25252df3be44c0386eb9f5f28ea5fc1de4c783dba912c7df332f`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "sheet1", "kind": "base", "block": null, "base_tables": ["sheet1"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |


## S27

类别 `data`；来源 `python`；调用 `ee8920b4c6e24d3ca1003c2cd4172d42`；状态 `success`。

```sql
SELECT * FROM sheet1
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-011/attempt-01/sql/S27.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-011/attempt-01/sql/S27.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-011/attempt-01/results/S27.rows.jsonl)；完整：True；SHA256：`47bacbf2bf6a25252df3be44c0386eb9f5f28ea5fc1de4c783dba912c7df332f`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "sheet1", "kind": "base", "block": null, "base_tables": ["sheet1"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |


## S28

类别 `data`；来源 `python`；调用 `728e333cbcfb4f3d99f6078f8f1e310f`；状态 `success`。

```sql
SELECT * FROM sheet1
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-011/attempt-01/sql/S28.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-011/attempt-01/sql/S28.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-011/attempt-01/results/S28.rows.jsonl)；完整：True；SHA256：`47bacbf2bf6a25252df3be44c0386eb9f5f28ea5fc1de4c783dba912c7df332f`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "sheet1", "kind": "base", "block": null, "base_tables": ["sheet1"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |


## S29

类别 `data`；来源 `query_db`；调用 `b22d320dc75446978578bdb7d1a03f5f`；状态 `success`。

```sql
SELECT 
  CASE WHEN "Parents' education level" IS NULL THEN 'Missing' ELSE "Parents' education level" END AS parent_edu,
  COUNT(*) AS n,
  ROUND(AVG("Exam score"),2) AS avg_exam,
  ROUND(AVG("Daily study time"),2) AS avg_study,
  ROUND(AVG("Social media usage time"),2) AS avg_social,
  ROUND(AVG("Attendance rate"),2) AS avg_att,
  ROUND(AVG("Sleep duration"),2) AS avg_sleep,
  ROUND(AVG("Exercise frequency"),2) AS avg_ex,
  ROUND(AVG("Mental health score"),2) AS avg_mh
FROM sheet1
GROUP BY parent_edu
ORDER BY avg_exam DESC
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-011/attempt-01/sql/S29.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-011/attempt-01/sql/S29.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-011/attempt-01/results/S29.rows.jsonl)；完整：True；SHA256：`a6bc41400466563e5e8605b92eb3d497e8632b9a8b1a9ffe0d9c3ba578bb8ad8`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "sheet1", "kind": "base", "block": null, "base_tables": ["sheet1"]}] | [] | ["CASE WHEN \"Parents' education level\" IS NULL THEN 'Missing' ELSE \"Parents' education level\" END"] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |
| B1 | AVG("Exam score") | [{"table": "sheet1", "column": "Exam score"}] | [] | False |
| B1 | AVG("Daily study time") | [{"table": "sheet1", "column": "Daily study time"}] | [] | False |
| B1 | AVG("Social media usage time") | [{"table": "sheet1", "column": "Social media usage time"}] | [] | False |
| B1 | AVG("Attendance rate") | [{"table": "sheet1", "column": "Attendance rate"}] | [] | False |
| B1 | AVG("Sleep duration") | [{"table": "sheet1", "column": "Sleep duration"}] | [] | False |
| B1 | AVG("Exercise frequency") | [{"table": "sheet1", "column": "Exercise frequency"}] | [] | False |
| B1 | AVG("Mental health score") | [{"table": "sheet1", "column": "Mental health score"}] | [] | False |


## S30

类别 `data`；来源 `query_db`；调用 `2ceb1092fe1c4bf7b9259c9858579f14`；状态 `success`。

```sql
SELECT 
  CASE WHEN "Parents' education level" IS NULL THEN 'Missing' ELSE "Parents' education level" END AS parent_edu,
  "Diet quality" AS diet,
  COUNT(*) AS n,
  ROUND(AVG("Exam score"),2) AS avg_exam
FROM sheet1
GROUP BY parent_edu, diet
ORDER BY parent_edu, diet
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-011/attempt-01/sql/S30.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-011/attempt-01/sql/S30.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-011/attempt-01/results/S30.rows.jsonl)；完整：True；SHA256：`ae8888c9a8245cdd6afbbf551285fd42e7b21826ee8f1a8c7c8b6d662d7bf831`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "sheet1", "kind": "base", "block": null, "base_tables": ["sheet1"]}] | [] | ["CASE WHEN \"Parents' education level\" IS NULL THEN 'Missing' ELSE \"Parents' education level\" END", "\"Diet quality\""] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |
| B1 | AVG("Exam score") | [{"table": "sheet1", "column": "Exam score"}] | [] | False |

