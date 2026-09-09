# dacomp-020

Analyze the dataset in `sheet1` to answer the following three questions: (1) What is the o…

运行：已提交。官方未评分。全部 SQL 尝试/成功 18/17；数据 SQL 16/15；Python 15 次。

完整原题：

Analyze the dataset in `sheet1` to answer the following three questions: (1) What is the overall relationship between `Mental health score` and `Exam score`? Use data-driven smoothing, grouping, or modeling approaches to describe whether the trend is monotonic, linear, or exhibits inflection points, and defend your conclusion with statistical evidence and interpretable effect sizes. (2) After controlling for learning habit and lifestyle factors captured in columns such as `Daily study time`, `Social media usage time`, `Attendance rate`, `Sleep duration`, `Exercise frequency`, `Diet quality`, `Part-time job`, `Internet quality`, and `Parents' education level`, assess whether `Mental health score` maintains a statistically significant marginal effect on `Exam score`, and quantify its coefficient, confidence intervals, p-values, and delta-`R²` (or alternative robust measures). (3) Identify which additional variables (learning habits, lifestyle factors, or demographics) interact with `Mental health score` to amplify or dampen its effect size, explaining the mechanistic implications of those interactions. Keep every explanation precise, cite the English column names, and preserve the original rubric’s emphasis on trend shape, statistical rigor, and policy-relevant implications.

| 表 | 行数 | 列数 |
| --- | --- | --- |
| sheet1 | 1000 | 15 |


实际路线（分析者依据 SQL/源码概括，不代表 Agent 自述）：SQL 检查心理健康与考试数据并汇总均值 → Python 比较线性、多项式和分段趋势 → 拟合控制变量与交互项模型 → 检查边际效应并绘图。

数据库大小：200,704 字节。

## 数据 SQL

| SQL | 状态 | 基础表 | Join 输入/类型 | GROUP BY | 聚合表达式 | 结果行数 | 数据库 ms |
| --- | --- | --- | --- | --- | --- | --- | --- |
| [S3/Q1](#s3) | success | ["sheet1"] | 0 / {} | [] | [] | 10 | 0.636 |
| [S4/Q2](#s4) | success | ["sheet1"] | 0 / {} | [] | ["COUNT(*)"] | 1 | 0.372 |
| [S5/Q3](#s5) | success | ["sheet1"] | 0 / {} | [] | ["MIN(\"Mental health score\")", "MAX(\"Mental health score\")", "AVG(\"Mental health score\")", "MIN(\"Exam score\")", "MAX(\"Exam score\")", "AVG(\"Exam score\")"] | 1 | 0.66 |
| [S6/Q4](#s6) | failed | ["sheet1"] | 0 / {} | ["\"Mental health score\""] | ["COUNT(*)", "AVG(\"Exam score\")", "STDDEV(\"Exam score\")"] | unknown | 未取得；调用总时长 0.18 ms |
| [S7/Q5](#s7) | success | ["sheet1"] | 0 / {} | ["\"Mental health score\""] | ["COUNT(*)", "AVG(\"Exam score\")", "AVG(\"Exam score\" * \"Exam score\")", "AVG(\"Exam score\")", "AVG(\"Exam score\")"] | 10 | 0.846 |
| [S8/Q6](#s8) | success | ["sheet1"] | 2 / {'CROSS': 1} | [] | ["AVG(\"Mental health score\")", "AVG(\"Exam score\")", "SUM((\"Mental health score\" - mh_mean) * (\"Exam score\" - exam_mean))", "SUM((\"Mental health score\" - mh_mean) * (\"Mental health score\" - mh_mean))", "SUM((\"Exam score\" - exam_mean) * (\"Exam score\" - exam_mean))", "COUNT(*)", "COUNT(*)", "COUNT(*)"] | 1 | 0.957 |
| [S9/Q7](#s9) | success | ["sheet1"] | 0 / {} | ["\"Gender\""] | ["COUNT(*)"] | 3 | 0.763 |
| [S10/Q8](#s10) | success | ["sheet1"] | 0 / {} | ["\"Part-time job\""] | ["COUNT(*)"] | 2 | 0.626 |
| [S11/Q9](#s11) | success | ["sheet1"] | 0 / {} | ["\"Diet quality\""] | ["COUNT(*)"] | 3 | 0.661 |
| [S12/Q10](#s12) | success | ["sheet1"] | 0 / {} | ["\"Parents' education level\""] | ["COUNT(*)"] | 4 | 0.791 |
| [S13/Q11](#s13) | success | ["sheet1"] | 0 / {} | ["\"Internet quality\""] | ["COUNT(*)"] | 3 | 0.684 |
| [S14/Q12](#s14) | success | ["sheet1"] | 0 / {} | ["\"Extracurricular activity participation\""] | ["COUNT(*)"] | 2 | 0.64 |
| [S15/Q13](#s15) | success | ["sheet1"] | 0 / {} | [] | ["SUM(CASE WHEN \"Age\" IS NULL THEN 1 ELSE 0 END)", "SUM(CASE WHEN \"Daily study time\" IS NULL THEN 1 ELSE 0 END)", "SUM(CASE WHEN \"Social media usage time\" IS NULL THEN 1 ELSE 0 END)", "SUM(CASE WHEN \"Attendance rate\" IS NULL THEN 1 ELSE 0 END)", "SUM(CASE WHEN \"Sleep duration\" IS NULL THEN 1 ELSE 0 END)", "SUM(CASE WHEN \"Exercise frequency\" IS NULL THEN 1 ELSE 0 END)", "SUM(CASE WHEN \"Mental health score\" IS NULL THEN 1 ELSE 0 END)", "SUM(CASE WHEN \"Exam score\" IS NULL THEN 1 ELSE 0 END)", "SUM(CASE WHEN \"Part-time job\" IS NULL THEN 1 ELSE 0 END)", "SUM(CASE WHEN \"Gender\" IS NULL THEN 1 ELSE 0 END)", "SUM(CASE WHEN \"Internet quality\" IS NULL THEN 1 ELSE 0 END)", "SUM(CASE WHEN \"Diet quality\" IS NULL THEN 1 ELSE 0 END)"] | 1 | 0.987 |
| [S16/Q14](#s16) | success | ["sheet1"] | 0 / {} | [] | ["MIN(\"Daily study time\")", "MAX(\"Daily study time\")", "AVG(\"Daily study time\")", "MIN(\"Social media usage time\")", "MAX(\"Social media usage time\")", "AVG(\"Social media usage time\")", "MIN(\"Attendance rate\")", "MAX(\"Attendance rate\")", "AVG(\"Attendance rate\")", "MIN(\"Sleep duration\")", "MAX(\"Sleep duration\")", "AVG(\"Sleep duration\")", "MIN(\"Exercise frequency\")", "MAX(\"Exercise frequency\")", "AVG(\"Exercise frequency\")", "MIN(\"Age\")", "MAX(\"Age\")", "AVG(\"Age\")"] | 1 | 1.232 |
| [S17/Q15](#s17) | success | ["sheet1"] | 0 / {} | [] | [] | 1000 | 3.868 |
| [S18/Q16](#s18) | success | ["sheet1"] | 0 / {} | [] | [] | 1000 | 3.22 |


## 元数据和设置

| SQL | 类别 | 状态 | 内容 |
| --- | --- | --- | --- |
| S1 | connection_setup | success | PRAGMA query_only=ON |
| S2 | metadata | success | SELECT name,sql FROM sqlite_master WHERE type='table' ORDER BY name |


## Python 与执行位置

人工源码审查：**reviewed_with_statistical_exceptions_and_SQL_capable_summaries**。The task explicitly requests regression, significance, confidence intervals and interactions, which justify Python numerical/statistical procedures and relevant row-level inputs. Matrix arithmetic and prediction curves are parts of those procedures. P4/P5/P15 additionally calculate per-score count/mean summaries and adjacent mean changes in pandas; these can reasonably be prepared in SQL and are disclosed as execution-location deviations. The statistical calls are not wholesale labeled violations merely for using arrays. [证据](../reviews/dacomp-020.json)。

P1：SQLite lacks regression, hypothesis testing, and model comparison capabilities. I need to load all rows (1000) once to run OLS regression, polynomial trend-shape tests, delta-R2 tests, and interaction analysis in Python.

[源码](../../../runs/dsv4flash-db-first-full-01/dacomp-020/attempt-01/python/P1.py)；[输出](../../../runs/dsv4flash-db-first-full-01/dacomp-020/attempt-01/python/P1.stdout)；[错误](../../../runs/dsv4flash-db-first-full-01/dacomp-020/attempt-01/python/P1.stderr)。自动源码筛查未检出预设迁出信号；这不是全面语义合规证明。

P2：Load the full dataset into Python via the logged db interface for regression and interaction modeling not supported by SQLite.

[源码](../../../runs/dsv4flash-db-first-full-01/dacomp-020/attempt-01/python/P2.py)；[输出](../../../runs/dsv4flash-db-first-full-01/dacomp-020/attempt-01/python/P2.stdout)；[错误](../../../runs/dsv4flash-db-first-full-01/dacomp-020/attempt-01/python/P2.stderr)。检出需人工核验的 SQL 可实现操作：.query(；不能仅凭理由判为合规。

P3：Persist the loaded dataset for subsequent analysis steps in the workspace.

[源码](../../../runs/dsv4flash-db-first-full-01/dacomp-020/attempt-01/python/P3.py)；[输出](../../../runs/dsv4flash-db-first-full-01/dacomp-020/attempt-01/python/P3.stdout)；[错误](../../../runs/dsv4flash-db-first-full-01/dacomp-020/attempt-01/python/P3.stderr)。检出需人工核验的 SQL 可实现操作：.query(；不能仅凭理由判为合规。

P4：Statistical trend-shape analysis (correlations, polynomial fits, F-tests, group means with CIs) requires hypothesis tests and model comparison not available in SQLite.

[源码](../../../runs/dsv4flash-db-first-full-01/dacomp-020/attempt-01/python/P4.py)；[输出](../../../runs/dsv4flash-db-first-full-01/dacomp-020/attempt-01/python/P4.stdout)；[错误](../../../runs/dsv4flash-db-first-full-01/dacomp-020/attempt-01/python/P4.stderr)。检出需人工核验的 SQL 可实现操作：groupby(；不能仅凭理由判为合规。

P5：Visualization of the trend shape (scatter, group means, linear fit, cubic smooth with inflection point) to support the trend-shape analysis.

[源码](../../../runs/dsv4flash-db-first-full-01/dacomp-020/attempt-01/python/P5.py)；[输出](../../../runs/dsv4flash-db-first-full-01/dacomp-020/attempt-01/python/P5.stdout)；[错误](../../../runs/dsv4flash-db-first-full-01/dacomp-020/attempt-01/python/P5.stderr)。检出需人工核验的 SQL 可实现操作：groupby(；不能仅凭理由判为合规。

P6：Multiple OLS regression with controls, delta-R2, partial F-test, and standardized effect sizes require matrix algebra and t/F distributions not available in SQLite.

[源码](../../../runs/dsv4flash-db-first-full-01/dacomp-020/attempt-01/python/P6.py)；[输出](../../../runs/dsv4flash-db-first-full-01/dacomp-020/attempt-01/python/P6.stdout)；[错误](../../../runs/dsv4flash-db-first-full-01/dacomp-020/attempt-01/python/P6.stderr)。自动源码筛查未检出预设迁出信号；这不是全面语义合规证明。

P7：Interaction analysis requires fitting multiple regression models with product terms, computing partial F-tests, and evaluating significance - all outside SQLite's capabilities.

[源码](../../../runs/dsv4flash-db-first-full-01/dacomp-020/attempt-01/python/P7.py)；[输出](../../../runs/dsv4flash-db-first-full-01/dacomp-020/attempt-01/python/P7.stdout)；[错误](../../../runs/dsv4flash-db-first-full-01/dacomp-020/attempt-01/python/P7.stderr)。自动源码筛查未检出预设迁出信号；这不是全面语义合规证明。

P8：Robustness check of the Mental health score coefficient when additional demographics (age, gender, extracurricular) are included as controls.

[源码](../../../runs/dsv4flash-db-first-full-01/dacomp-020/attempt-01/python/P8.py)；[输出](../../../runs/dsv4flash-db-first-full-01/dacomp-020/attempt-01/python/P8.stdout)；[错误](../../../runs/dsv4flash-db-first-full-01/dacomp-020/attempt-01/python/P8.stderr)。自动源码筛查未检出预设迁出信号；这不是全面语义合规证明。

P9：Visualize and quantify the two significant interactions (MH×Attendance, MH×Social media) by computing predicted exam scores and marginal MH slopes at moderator levels - prediction and visualization outside SQLite scope.

[源码](../../../runs/dsv4flash-db-first-full-01/dacomp-020/attempt-01/python/P9.py)；[输出](../../../runs/dsv4flash-db-first-full-01/dacomp-020/attempt-01/python/P9.stdout)；[错误](../../../runs/dsv4flash-db-first-full-01/dacomp-020/attempt-01/python/P9.stderr)。自动源码筛查未检出预设迁出信号；这不是全面语义合规证明。

P10：Correct the interaction figure using single-interaction models with the other moderator held at its mean, and quantify marginal MH slopes at moderator levels.

[源码](../../../runs/dsv4flash-db-first-full-01/dacomp-020/attempt-01/python/P10.py)；[输出](../../../runs/dsv4flash-db-first-full-01/dacomp-020/attempt-01/python/P10.stdout)；[错误](../../../runs/dsv4flash-db-first-full-01/dacomp-020/attempt-01/python/P10.stderr)。自动源码筛查未检出预设迁出信号；这不是全面语义合规证明。

P11：Corrected interaction figure using single-interaction models with proper variable naming, and quantify marginal MH slopes at moderator levels.

[源码](../../../runs/dsv4flash-db-first-full-01/dacomp-020/attempt-01/python/P11.py)；[输出](../../../runs/dsv4flash-db-first-full-01/dacomp-020/attempt-01/python/P11.stdout)；[错误](../../../runs/dsv4flash-db-first-full-01/dacomp-020/attempt-01/python/P11.stderr)。自动源码筛查未检出预设迁出信号；这不是全面语义合规证明。

P12：Diagnostic checks: variance inflation factors for multicollinearity, descriptive statistics, and residual normality assessment.

[源码](../../../runs/dsv4flash-db-first-full-01/dacomp-020/attempt-01/python/P12.py)；[输出](../../../runs/dsv4flash-db-first-full-01/dacomp-020/attempt-01/python/P12.stdout)；[错误](../../../runs/dsv4flash-db-first-full-01/dacomp-020/attempt-01/python/P12.stderr)。自动源码筛查未检出预设迁出信号；这不是全面语义合规证明。

P13：Compute robust (HC1/HC3) standard errors for the Mental health coefficient and precise p-values and SEs for the interaction terms, as robust measures requested by the task.

[源码](../../../runs/dsv4flash-db-first-full-01/dacomp-020/attempt-01/python/P13.py)；[输出](../../../runs/dsv4flash-db-first-full-01/dacomp-020/attempt-01/python/P13.stdout)；[错误](../../../runs/dsv4flash-db-first-full-01/dacomp-020/attempt-01/python/P13.stderr)。自动源码筛查未检出预设迁出信号；这不是全面语义合规证明。

P14：Compute robust standard errors, partial R², and precise inferential statistics for the Mental health coefficient and interactions.

[源码](../../../runs/dsv4flash-db-first-full-01/dacomp-020/attempt-01/python/P14.py)；[输出](../../../runs/dsv4flash-db-first-full-01/dacomp-020/attempt-01/python/P14.stdout)；[错误](../../../runs/dsv4flash-db-first-full-01/dacomp-020/attempt-01/python/P14.stderr)。自动源码筛查未检出预设迁出信号；这不是全面语义合规证明。

P15：Test the trend shape with piecewise linear (segmented) regression to check whether the slope changes significantly around an inflection point, and verify monotonicity of group means.

[源码](../../../runs/dsv4flash-db-first-full-01/dacomp-020/attempt-01/python/P15.py)；[输出](../../../runs/dsv4flash-db-first-full-01/dacomp-020/attempt-01/python/P15.stdout)；[错误](../../../runs/dsv4flash-db-first-full-01/dacomp-020/attempt-01/python/P15.stderr)。检出需人工核验的 SQL 可实现操作：groupby(；不能仅凭理由判为合规。

## 优化机会

已验证候选。筛选限于精确 SQL、相同自包含 CTE、相同单表完整过滤、可分解单表聚合；未覆盖任意 Join 等价和一般谓词蕴含。全部候选都是 offline，未测在线预测。

| 候选 | 类型 | 已有结果 | 覆盖 SQL | 后续次数 | 中间行数 | 验证 | 成本 |
| --- | --- | --- | --- | --- | --- | --- | --- |
| C1 | exact-result reuse | True | ["S17", "S18"] | 1 | 1000 | verified | Not benchmarked; correctness alone does not establish net speedup. |
| C2 | aggregate MV | False | ["S4", "S5", "S7", "S9", "S10", "S11", "S12", "S13", "S14", "S15", "S16"] | 10 | 724 | rejected_result_mismatch | Not benchmarked; correctness alone does not establish net speedup. |


已验证覆盖（含触发查询、候选并集去重）：2/15 条成功数据 SQL。正确性仅针对当前数据库快照；未测性能的候选不能声称已加速。

[完整 build/rewrite 与比较证据](dacomp-020.analysis.json)。

### C1：exact-result reuse

Identical normalized SQL and parameters; archive equality checked.

原查询 [S17](#s17), [S18](#s18) → 保留前序结果 S17 → 后续 1 次可复用。该构建点为事后假设，不代表 Agent 当时预知后续。

| 原 SQL | 列名一致 | 结果一致 | 比较方法 |
| --- | --- | --- | --- |
| S18 | True | True | exact_multiset |


验证状态：verified；成本结论：Not benchmarked; correctness alone does not establish net speedup.

### C2：aggregate MV

Union of grouping keys; decomposable aggregate states; AVG uses SUM and non-NULL COUNT.

原查询 [S4](#s4), [S5](#s5), [S7](#s7), [S9](#s9), [S10](#s10), [S11](#s11), [S12](#s12), [S13](#s13), [S14](#s14), [S15](#s15), [S16](#s16) → 新增共享状态 C2 → 后续 10 次可复用。该构建点为事后假设，不代表 Agent 当时预知后续。

构建定义：

```sql
SELECT "Mental health score" AS __g0, "Gender" AS __g1, "Part-time job" AS __g2, "Diet quality" AS __g3, "Parents' education level" AS __g4, "Internet quality" AS __g5, "Extracurricular activity participation" AS __g6, COUNT(*) AS __a0, MIN("Mental health score") AS __a1, MAX("Mental health score") AS __a2, SUM("Mental health score") AS __a3_sum, COUNT("Mental health score") AS __a3_n, MIN("Exam score") AS __a4, MAX("Exam score") AS __a5, SUM("Exam score") AS __a6_sum, COUNT("Exam score") AS __a6_n, SUM("Exam score" * "Exam score") AS __a7_sum, COUNT("Exam score" * "Exam score") AS __a7_n, SUM(CASE WHEN "Age" IS NULL THEN 1 ELSE 0 END) AS __a8, SUM(CASE WHEN "Daily study time" IS NULL THEN 1 ELSE 0 END) AS __a9, SUM(CASE WHEN "Social media usage time" IS NULL THEN 1 ELSE 0 END) AS __a10, SUM(CASE WHEN "Attendance rate" IS NULL THEN 1 ELSE 0 END) AS __a11, SUM(CASE WHEN "Sleep duration" IS NULL THEN 1 ELSE 0 END) AS __a12, SUM(CASE WHEN "Exercise frequency" IS NULL THEN 1 ELSE 0 END) AS __a13, SUM(CASE WHEN "Mental health score" IS NULL THEN 1 ELSE 0 END) AS __a14, SUM(CASE WHEN "Exam score" IS NULL THEN 1 ELSE 0 END) AS __a15, SUM(CASE WHEN "Part-time job" IS NULL THEN 1 ELSE 0 END) AS __a16, SUM(CASE WHEN "Gender" IS NULL THEN 1 ELSE 0 END) AS __a17, SUM(CASE WHEN "Internet quality" IS NULL THEN 1 ELSE 0 END) AS __a18, SUM(CASE WHEN "Diet quality" IS NULL THEN 1 ELSE 0 END) AS __a19, MIN("Daily study time") AS __a20, MAX("Daily study time") AS __a21, SUM("Daily study time") AS __a22_sum, COUNT("Daily study time") AS __a22_n, MIN("Social media usage time") AS __a23, MAX("Social media usage time") AS __a24, SUM("Social media usage time") AS __a25_sum, COUNT("Social media usage time") AS __a25_n, MIN("Attendance rate") AS __a26, MAX("Attendance rate") AS __a27, SUM("Attendance rate") AS __a28_sum, COUNT("Attendance rate") AS __a28_n, MIN("Sleep duration") AS __a29, MAX("Sleep duration") AS __a30, SUM("Sleep duration") AS __a31_sum, COUNT("Sleep duration") AS __a31_n, MIN("Exercise frequency") AS __a32, MAX("Exercise frequency") AS __a33, SUM("Exercise frequency") AS __a34_sum, COUNT("Exercise frequency") AS __a34_n, MIN("Age") AS __a35, MAX("Age") AS __a36, SUM("Age") AS __a37_sum, COUNT("Age") AS __a37_n FROM "sheet1"  GROUP BY "Mental health score", "Gender", "Part-time job", "Diet quality", "Parents' education level", "Internet quality", "Extracurricular activity participation"
```

受益查询 S4 的改写示例：

```sql
SELECT SUM(__a0) AS total_rows FROM temp.reuse_candidate
```

| 原 SQL | 列名一致 | 结果一致 | 比较方法 |
| --- | --- | --- | --- |
| S4 | True | True | exact_multiset |
| S5 | True | False | exact_multiset |
| S7 | True | True | ordered_numeric_tolerance |
| S9 | True | True | exact_multiset |
| S10 | True | True | exact_multiset |
| S11 | True | True | exact_multiset |
| S12 | True | True | exact_multiset |
| S13 | True | True | exact_multiset |
| S14 | True | True | exact_multiset |
| S15 | True | True | exact_multiset |
| S16 | True | False | exact_multiset |


验证状态：rejected_result_mismatch；成本结论：Not benchmarked; correctness alone does not establish net speedup.

结果依赖：自动记录 SQL→Python 的接口父调用，以及源码中引用归档文件的消费者；字面值相同不认定因果。模型方向选择需要人工读取消息，尚未做全面因果标注。

[原始报告](../../../runs/dsv4flash-db-first-full-01/dacomp-020/attempt-01/answer.md)；[统一消息](../../../runs/dsv4flash-db-first-full-01/dacomp-020/attempt-01/messages.jsonl)；[原始 OpenCode 事件](../../../runs/dsv4flash-db-first-full-01/dacomp-020/attempt-01/opencode.jsonl)；[SQL 引擎日志](../../../runs/dsv4flash-db-first-full-01/dacomp-020/attempt-01/sql_journal.jsonl)。

[可读报告（本地图片链接规范化）](../answers/dacomp-020.md)。原始回答保留，分析结论未改写。

## S1

类别 `connection_setup`；来源 `connection`；调用 `bf2ea79a898f4a2eb20201d3e94cbfed`；状态 `success`。

```sql
PRAGMA query_only=ON
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-020/attempt-01/sql/S1.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-020/attempt-01/sql/S1.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-020/attempt-01/results/S1.rows.jsonl)；完整：True；SHA256：`e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`。

## S2

类别 `metadata`；来源 `list_db`；调用 `bf2ea79a898f4a2eb20201d3e94cbfed`；状态 `success`。

```sql
SELECT name,sql FROM sqlite_master WHERE type='table' ORDER BY name
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-020/attempt-01/sql/S2.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-020/attempt-01/sql/S2.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-020/attempt-01/results/S2.rows.jsonl)；完整：True；SHA256：`943fe944781c972aaf1e9f6c08d288804a0621264afd085297f3ea3fc70817b4`。

## S3

类别 `data`；来源 `query_db`；调用 `bfbb58861ec54729a1f055b22b979f47`；状态 `success`。

```sql
SELECT * FROM sheet1 LIMIT 10
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-020/attempt-01/sql/S3.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-020/attempt-01/sql/S3.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-020/attempt-01/results/S3.rows.jsonl)；完整：True；SHA256：`bb94c27ad41ba1177b1ba3a7d2e7038ca65f7a766c55b5bf6e25eb6d69db9b8f`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "sheet1", "kind": "base", "block": null, "base_tables": ["sheet1"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |


## S4

类别 `data`；来源 `query_db`；调用 `eaf389c3001a472fa7a04b937713588d`；状态 `success`。

```sql
SELECT COUNT(*) as total_rows FROM sheet1
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-020/attempt-01/sql/S4.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-020/attempt-01/sql/S4.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-020/attempt-01/results/S4.rows.jsonl)；完整：True；SHA256：`e3ed33dc26a723b8481ca677e38dc4a6e8700aeec312afdd02c9dd92374161a2`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "sheet1", "kind": "base", "block": null, "base_tables": ["sheet1"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |


## S5

类别 `data`；来源 `query_db`；调用 `e023608b50e14949826026deef786718`；状态 `success`。

```sql
SELECT MIN("Mental health score") as min_mh, MAX("Mental health score") as max_mh, AVG("Mental health score") as avg_mh, 
       MIN("Exam score") as min_exam, MAX("Exam score") as max_exam, AVG("Exam score") as avg_exam
FROM sheet1
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-020/attempt-01/sql/S5.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-020/attempt-01/sql/S5.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-020/attempt-01/results/S5.rows.jsonl)；完整：True；SHA256：`d8bfef9b77d628f834137a3a88b244dcf7dffab8e667db06813c0df9dd34db18`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "sheet1", "kind": "base", "block": null, "base_tables": ["sheet1"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | MIN("Mental health score") | [{"table": "sheet1", "column": "Mental health score"}] | [] | False |
| B1 | MAX("Mental health score") | [{"table": "sheet1", "column": "Mental health score"}] | [] | False |
| B1 | AVG("Mental health score") | [{"table": "sheet1", "column": "Mental health score"}] | [] | False |
| B1 | MIN("Exam score") | [{"table": "sheet1", "column": "Exam score"}] | [] | False |
| B1 | MAX("Exam score") | [{"table": "sheet1", "column": "Exam score"}] | [] | False |
| B1 | AVG("Exam score") | [{"table": "sheet1", "column": "Exam score"}] | [] | False |


## S6

类别 `data`；来源 `query_db`；调用 `2f800079f077492ab8b586450dfb7909`；状态 `failed`。

```sql
SELECT "Mental health score", COUNT(*) as n, AVG("Exam score") as avg_exam, STDDEV("Exam score") as std_exam
FROM sheet1
GROUP BY "Mental health score"
ORDER BY "Mental health score"
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-020/attempt-01/sql/S6.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-020/attempt-01/sql/S6.parameters.json)。

错误：`OperationalError('no such function: STDDEV')`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "sheet1", "kind": "base", "block": null, "base_tables": ["sheet1"]}] | [] | ["\"Mental health score\""] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |
| B1 | AVG("Exam score") | [{"table": "sheet1", "column": "Exam score"}] | [] | False |
| B1 | STDDEV("Exam score") | [{"table": "sheet1", "column": "Exam score"}] | [] | False |


## S7

类别 `data`；来源 `query_db`；调用 `2c59120515a94c7f8dc91aa6280b993e`；状态 `success`。

```sql
SELECT "Mental health score" as mh, COUNT(*) as n, ROUND(AVG("Exam score"),3) as avg_exam,
       ROUND(AVG("Exam score"*"Exam score") - AVG("Exam score")*AVG("Exam score"),3) as var_exam
FROM sheet1
GROUP BY mh
ORDER BY mh
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-020/attempt-01/sql/S7.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-020/attempt-01/sql/S7.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-020/attempt-01/results/S7.rows.jsonl)；完整：True；SHA256：`bc1605164e8a1cb77813de8a5f1d49760baa4ccbca303e47e12db9b33950693e`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "sheet1", "kind": "base", "block": null, "base_tables": ["sheet1"]}] | [] | ["\"Mental health score\""] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |
| B1 | AVG("Exam score") | [{"table": "sheet1", "column": "Exam score"}] | [] | False |
| B1 | AVG("Exam score" * "Exam score") | [{"table": "sheet1", "column": "Exam score"}, {"table": "sheet1", "column": "Exam score"}] | [] | False |
| B1 | AVG("Exam score") | [{"table": "sheet1", "column": "Exam score"}] | [] | False |
| B1 | AVG("Exam score") | [{"table": "sheet1", "column": "Exam score"}] | [] | False |


## S8

类别 `data`；来源 `query_db`；调用 `28c24b678890422a80bd28a1237bed69`；状态 `success`。

```sql
SELECT 
  SUM(("Mental health score" - mh_mean) * ("Exam score" - exam_mean)) / (COUNT(*) - 1) as cov,
  SQRT(SUM(("Mental health score" - mh_mean)*("Mental health score" - mh_mean))/(COUNT(*)-1)) as sd_mh,
  SQRT(SUM(("Exam score" - exam_mean)*("Exam score" - exam_mean))/(COUNT(*)-1)) as sd_exam
FROM sheet1, (SELECT AVG("Mental health score") as mh_mean, AVG("Exam score") as exam_mean FROM sheet1)
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-020/attempt-01/sql/S8.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-020/attempt-01/sql/S8.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-020/attempt-01/results/S8.rows.jsonl)；完整：True；SHA256：`2a31815c27fdb2dc8a8d30127d3760146e4f9b03815d6735cd61ead0f05416cb`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "sheet1", "kind": "base", "block": null, "base_tables": ["sheet1"]}] | [] | [] |
| B2 | [{"alias": "sheet1", "kind": "base", "block": null, "base_tables": ["sheet1"]}, {"alias": "", "kind": "derived", "block": "B1", "base_tables": ["sheet1"]}] | [{"type": "CROSS", "right": "(SELECT AVG(\"Mental health score\") AS mh_mean, AVG(\"Exam score\") AS exam_mean FROM sheet1)", "on": null, "using": []}] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | AVG("Mental health score") | [{"table": "sheet1", "column": "Mental health score"}] | [] | False |
| B1 | AVG("Exam score") | [{"table": "sheet1", "column": "Exam score"}] | [] | False |
| B2 | SUM(("Mental health score" - mh_mean) * ("Exam score" - exam_mean)) | [{"table": "sheet1", "column": "Mental health score"}, {"table": "sheet1", "column": "Mental health score"}, {"table": "sheet1", "column": "Exam score"}, {"table": "sheet1", "column": "Exam score"}] | [] | False |
| B2 | SUM(("Mental health score" - mh_mean) * ("Mental health score" - mh_mean)) | [{"table": "sheet1", "column": "Mental health score"}, {"table": "sheet1", "column": "Mental health score"}, {"table": "sheet1", "column": "Mental health score"}, {"table": "sheet1", "column": "Mental health score"}] | [] | False |
| B2 | SUM(("Exam score" - exam_mean) * ("Exam score" - exam_mean)) | [{"table": "sheet1", "column": "Exam score"}, {"table": "sheet1", "column": "Exam score"}, {"table": "sheet1", "column": "Exam score"}, {"table": "sheet1", "column": "Exam score"}] | [] | False |
| B2 | COUNT(*) | [] | [] | True |
| B2 | COUNT(*) | [] | [] | True |
| B2 | COUNT(*) | [] | [] | True |


## S9

类别 `data`；来源 `query_db`；调用 `09285abf365e4843875a667f6eea924d`；状态 `success`。

```sql
SELECT "Gender", COUNT(*) as n FROM sheet1 GROUP BY "Gender"
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-020/attempt-01/sql/S9.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-020/attempt-01/sql/S9.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-020/attempt-01/results/S9.rows.jsonl)；完整：True；SHA256：`caa3d9edc5cc903af362b09fcc73c7c575013dddca27cf46f6c1a6b4dbcb675d`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "sheet1", "kind": "base", "block": null, "base_tables": ["sheet1"]}] | [] | ["\"Gender\""] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |


## S10

类别 `data`；来源 `query_db`；调用 `7a00820f66344d499bad21a2ec46cccf`；状态 `success`。

```sql
SELECT "Part-time job", COUNT(*) as n FROM sheet1 GROUP BY "Part-time job"
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-020/attempt-01/sql/S10.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-020/attempt-01/sql/S10.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-020/attempt-01/results/S10.rows.jsonl)；完整：True；SHA256：`c31ce52e56735dddc07510cedeab09e472dffcbc44f2734e29b10886305b9318`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "sheet1", "kind": "base", "block": null, "base_tables": ["sheet1"]}] | [] | ["\"Part-time job\""] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |


## S11

类别 `data`；来源 `query_db`；调用 `03a4220984f84de492bdc151d216121b`；状态 `success`。

```sql
SELECT "Diet quality", COUNT(*) as n FROM sheet1 GROUP BY "Diet quality"
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-020/attempt-01/sql/S11.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-020/attempt-01/sql/S11.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-020/attempt-01/results/S11.rows.jsonl)；完整：True；SHA256：`36f3e92622a80f06101e713f3c43b63cbc98d3be4da00911ee0ddaef63c3472d`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "sheet1", "kind": "base", "block": null, "base_tables": ["sheet1"]}] | [] | ["\"Diet quality\""] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |


## S12

类别 `data`；来源 `query_db`；调用 `fb1d885d5bdd45c093006683dcb3daec`；状态 `success`。

```sql
SELECT "Parents' education level", COUNT(*) as n FROM sheet1 GROUP BY "Parents' education level"
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-020/attempt-01/sql/S12.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-020/attempt-01/sql/S12.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-020/attempt-01/results/S12.rows.jsonl)；完整：True；SHA256：`3bada230213effc39a44ab73816b004e7496066d4f5e3411303b307c54f78453`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "sheet1", "kind": "base", "block": null, "base_tables": ["sheet1"]}] | [] | ["\"Parents' education level\""] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |


## S13

类别 `data`；来源 `query_db`；调用 `558ac022ea0048d19e9ed4fcd1efeced`；状态 `success`。

```sql
SELECT "Internet quality", COUNT(*) as n FROM sheet1 GROUP BY "Internet quality"
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-020/attempt-01/sql/S13.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-020/attempt-01/sql/S13.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-020/attempt-01/results/S13.rows.jsonl)；完整：True；SHA256：`fdedc689f38c63231b8bdefa3dfef2a33848c80d5fe0f562ad4dd32e49b83e2f`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "sheet1", "kind": "base", "block": null, "base_tables": ["sheet1"]}] | [] | ["\"Internet quality\""] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |


## S14

类别 `data`；来源 `query_db`；调用 `a3e31658857f4bdb8632887931a18b07`；状态 `success`。

```sql
SELECT "Extracurricular activity participation", COUNT(*) as n FROM sheet1 GROUP BY "Extracurricular activity participation"
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-020/attempt-01/sql/S14.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-020/attempt-01/sql/S14.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-020/attempt-01/results/S14.rows.jsonl)；完整：True；SHA256：`409cef507c11ec9d9c73041b0abb85c7271fea2629e28e1aec8d3123f73ab5be`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "sheet1", "kind": "base", "block": null, "base_tables": ["sheet1"]}] | [] | ["\"Extracurricular activity participation\""] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |


## S15

类别 `data`；来源 `query_db`；调用 `51330300b5f74985a3c6a2fd6b1656fd`；状态 `success`。

```sql
SELECT 
  SUM(CASE WHEN "Age" IS NULL THEN 1 ELSE 0 END) as age_null,
  SUM(CASE WHEN "Daily study time" IS NULL THEN 1 ELSE 0 END) as study_null,
  SUM(CASE WHEN "Social media usage time" IS NULL THEN 1 ELSE 0 END) as sm_null,
  SUM(CASE WHEN "Attendance rate" IS NULL THEN 1 ELSE 0 END) as att_null,
  SUM(CASE WHEN "Sleep duration" IS NULL THEN 1 ELSE 0 END) as sleep_null,
  SUM(CASE WHEN "Exercise frequency" IS NULL THEN 1 ELSE 0 END) as ex_null,
  SUM(CASE WHEN "Mental health score" IS NULL THEN 1 ELSE 0 END) as mh_null,
  SUM(CASE WHEN "Exam score" IS NULL THEN 1 ELSE 0 END) as exam_null,
  SUM(CASE WHEN "Part-time job" IS NULL THEN 1 ELSE 0 END) as pt_null,
  SUM(CASE WHEN "Gender" IS NULL THEN 1 ELSE 0 END) as gender_null,
  SUM(CASE WHEN "Internet quality" IS NULL THEN 1 ELSE 0 END) as iq_null,
  SUM(CASE WHEN "Diet quality" IS NULL THEN 1 ELSE 0 END) as diet_null
FROM sheet1
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-020/attempt-01/sql/S15.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-020/attempt-01/sql/S15.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-020/attempt-01/results/S15.rows.jsonl)；完整：True；SHA256：`e4bc3fed442a2f6a329149a9dd4a11049a7fa0cd88fbadb2dab1dcadd33fcccb`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "sheet1", "kind": "base", "block": null, "base_tables": ["sheet1"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | SUM(CASE WHEN "Age" IS NULL THEN 1 ELSE 0 END) | [] | [{"table": "sheet1", "column": "Age"}] | False |
| B1 | SUM(CASE WHEN "Daily study time" IS NULL THEN 1 ELSE 0 END) | [] | [{"table": "sheet1", "column": "Daily study time"}] | False |
| B1 | SUM(CASE WHEN "Social media usage time" IS NULL THEN 1 ELSE 0 END) | [] | [{"table": "sheet1", "column": "Social media usage time"}] | False |
| B1 | SUM(CASE WHEN "Attendance rate" IS NULL THEN 1 ELSE 0 END) | [] | [{"table": "sheet1", "column": "Attendance rate"}] | False |
| B1 | SUM(CASE WHEN "Sleep duration" IS NULL THEN 1 ELSE 0 END) | [] | [{"table": "sheet1", "column": "Sleep duration"}] | False |
| B1 | SUM(CASE WHEN "Exercise frequency" IS NULL THEN 1 ELSE 0 END) | [] | [{"table": "sheet1", "column": "Exercise frequency"}] | False |
| B1 | SUM(CASE WHEN "Mental health score" IS NULL THEN 1 ELSE 0 END) | [] | [{"table": "sheet1", "column": "Mental health score"}] | False |
| B1 | SUM(CASE WHEN "Exam score" IS NULL THEN 1 ELSE 0 END) | [] | [{"table": "sheet1", "column": "Exam score"}] | False |
| B1 | SUM(CASE WHEN "Part-time job" IS NULL THEN 1 ELSE 0 END) | [] | [{"table": "sheet1", "column": "Part-time job"}] | False |
| B1 | SUM(CASE WHEN "Gender" IS NULL THEN 1 ELSE 0 END) | [] | [{"table": "sheet1", "column": "Gender"}] | False |
| B1 | SUM(CASE WHEN "Internet quality" IS NULL THEN 1 ELSE 0 END) | [] | [{"table": "sheet1", "column": "Internet quality"}] | False |
| B1 | SUM(CASE WHEN "Diet quality" IS NULL THEN 1 ELSE 0 END) | [] | [{"table": "sheet1", "column": "Diet quality"}] | False |


## S16

类别 `data`；来源 `query_db`；调用 `b70977701380403399db82d9eb393abd`；状态 `success`。

```sql
SELECT 
  MIN("Daily study time") as mn_study, MAX("Daily study time") as mx_study, AVG("Daily study time") as avg_study,
  MIN("Social media usage time") as mn_sm, MAX("Social media usage time") as mx_sm, AVG("Social media usage time") as avg_sm,
  MIN("Attendance rate") as mn_att, MAX("Attendance rate") as mx_att, AVG("Attendance rate") as avg_att,
  MIN("Sleep duration") as mn_sleep, MAX("Sleep duration") as mx_sleep, AVG("Sleep duration") as avg_sleep,
  MIN("Exercise frequency") as mn_ex, MAX("Exercise frequency") as mx_ex, AVG("Exercise frequency") as avg_ex,
  MIN("Age") as mn_age, MAX("Age") as mx_age, AVG("Age") as avg_age
FROM sheet1
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-020/attempt-01/sql/S16.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-020/attempt-01/sql/S16.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-020/attempt-01/results/S16.rows.jsonl)；完整：True；SHA256：`99a834b4acfa53eac651a44d9d3d91430b0689dea3486f140fd56636bff008ac`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "sheet1", "kind": "base", "block": null, "base_tables": ["sheet1"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | MIN("Daily study time") | [{"table": "sheet1", "column": "Daily study time"}] | [] | False |
| B1 | MAX("Daily study time") | [{"table": "sheet1", "column": "Daily study time"}] | [] | False |
| B1 | AVG("Daily study time") | [{"table": "sheet1", "column": "Daily study time"}] | [] | False |
| B1 | MIN("Social media usage time") | [{"table": "sheet1", "column": "Social media usage time"}] | [] | False |
| B1 | MAX("Social media usage time") | [{"table": "sheet1", "column": "Social media usage time"}] | [] | False |
| B1 | AVG("Social media usage time") | [{"table": "sheet1", "column": "Social media usage time"}] | [] | False |
| B1 | MIN("Attendance rate") | [{"table": "sheet1", "column": "Attendance rate"}] | [] | False |
| B1 | MAX("Attendance rate") | [{"table": "sheet1", "column": "Attendance rate"}] | [] | False |
| B1 | AVG("Attendance rate") | [{"table": "sheet1", "column": "Attendance rate"}] | [] | False |
| B1 | MIN("Sleep duration") | [{"table": "sheet1", "column": "Sleep duration"}] | [] | False |
| B1 | MAX("Sleep duration") | [{"table": "sheet1", "column": "Sleep duration"}] | [] | False |
| B1 | AVG("Sleep duration") | [{"table": "sheet1", "column": "Sleep duration"}] | [] | False |
| B1 | MIN("Exercise frequency") | [{"table": "sheet1", "column": "Exercise frequency"}] | [] | False |
| B1 | MAX("Exercise frequency") | [{"table": "sheet1", "column": "Exercise frequency"}] | [] | False |
| B1 | AVG("Exercise frequency") | [{"table": "sheet1", "column": "Exercise frequency"}] | [] | False |
| B1 | MIN("Age") | [{"table": "sheet1", "column": "Age"}] | [] | False |
| B1 | MAX("Age") | [{"table": "sheet1", "column": "Age"}] | [] | False |
| B1 | AVG("Age") | [{"table": "sheet1", "column": "Age"}] | [] | False |


## S17

类别 `data`；来源 `python`；调用 `e1837e17e8454336b9dffd001b12e215`；状态 `success`。

```sql
SELECT * FROM sheet1
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-020/attempt-01/sql/S17.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-020/attempt-01/sql/S17.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-020/attempt-01/results/S17.rows.jsonl)；完整：True；SHA256：`47bacbf2bf6a25252df3be44c0386eb9f5f28ea5fc1de4c783dba912c7df332f`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "sheet1", "kind": "base", "block": null, "base_tables": ["sheet1"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |


## S18

类别 `data`；来源 `python`；调用 `777cac440a1241aba9945ce6c666d5f1`；状态 `success`。

```sql
SELECT * FROM sheet1
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-020/attempt-01/sql/S18.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-020/attempt-01/sql/S18.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-020/attempt-01/results/S18.rows.jsonl)；完整：True；SHA256：`47bacbf2bf6a25252df3be44c0386eb9f5f28ea5fc1de4c783dba912c7df332f`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "sheet1", "kind": "base", "block": null, "base_tables": ["sheet1"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |

