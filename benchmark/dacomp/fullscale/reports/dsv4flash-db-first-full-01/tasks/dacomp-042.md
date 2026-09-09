# dacomp-042

Compare and analyze how the primary barrier factors to treatment adherence differ across p…

运行：已提交。官方未评分。全部 SQL 尝试/成功 60/60；数据 SQL 58/58；Python 5 次。

完整原题：

Compare and analyze how the primary barrier factors to treatment adherence differ across patient age groups (recommended groupings: young adults 18–44, middle-aged 45–59, older adults 60+), and how the impact of these barriers on the degree of symptom improvement differs across age groups. Based on the distinct challenges of each age group, propose targeted intervention strategies for each group, and set quantifiable monitoring indicators for each strategy to evaluate its applicability and effectiveness across different populations.

| 表 | 行数 | 列数 |
| --- | --- | --- |
| assessmentbasics | 999 | 9 |
| assessmentsocialanddiagnosis | 999 | 20 |
| assessmentsymptomsandrisk | 999 | 9 |
| clinicians | 941 | 11 |
| encounters | 999 | 11 |
| facilities | 595 | 8 |
| patients | 1000 | 16 |
| treatmentbasics | 1000 | 8 |
| treatmentoutcomes | 1000 | 15 |


实际路线（分析者依据 SQL/源码概括，不代表 Agent 自述）：按年龄分组关联障碍、依从性和症状改善 → SQL 交叉汇总 → Python 逻辑回归、比例/满意度摘要 → 绘制年龄组差异。

数据库大小：2,531,328 字节。

## 数据 SQL

| SQL | 状态 | 基础表 | Join 输入/类型 | GROUP BY | 聚合表达式 | 结果行数 | 数据库 ms |
| --- | --- | --- | --- | --- | --- | --- | --- |
| [S3/Q1](#s3) | success | ["patients"] | 0 / {} | [] | [] | 5 | 0.332 |
| [S4/Q2](#s4) | success | ["encounters"] | 0 / {} | [] | [] | 5 | 0.321 |
| [S5/Q3](#s5) | success | ["encounters"] | 0 / {} | [] | [] | 4 | 0.575 |
| [S6/Q4](#s6) | success | ["treatmentoutcomes"] | 0 / {} | [] | [] | 3 | 0.568 |
| [S7/Q5](#s7) | success | ["treatmentoutcomes"] | 0 / {} | [] | [] | 4 | 0.489 |
| [S8/Q6](#s8) | success | ["patients"] | 0 / {} | [] | ["MIN(Age)", "MAX(Age)", "AVG(Age)"] | 1 | 0.545 |
| [S9/Q7](#s9) | success | ["encounters", "patients"] | 2 / {'INNER': 1} | [] | [] | 20 | 1.205 |
| [S10/Q8](#s10) | success | ["patients"] | 0 / {} | [] | ["COUNT(*)"] | 1 | 0.391 |
| [S11/Q9](#s11) | success | ["encounters"] | 0 / {} | [] | ["COUNT(*)"] | 1 | 0.296 |
| [S12/Q10](#s12) | success | ["treatmentoutcomes"] | 0 / {} | [] | [] | 5 | 0.45 |
| [S13/Q11](#s13) | success | ["treatmentbasics"] | 0 / {} | [] | [] | 5 | 0.329 |
| [S14/Q12](#s14) | success | ["encounters"] | 0 / {} | [] | ["COUNT(DISTINCT e.\"Visit Record Number\")"] | 1 | 0.931 |
| [S15/Q13](#s15) | success | ["treatmentoutcomes"] | 0 / {} | [] | ["COUNT(*)"] | 1 | 0.279 |
| [S16/Q14](#s16) | success | ["treatmentbasics"] | 0 / {} | [] | ["MIN(\"Treatment ID\")", "MAX(\"Treatment ID\")", "COUNT(*)"] | 1 | 0.582 |
| [S17/Q15](#s17) | success | ["treatmentbasics"] | 0 / {} | [] | ["COUNT(DISTINCT tb.\"Visit Reference\")"] | 1 | 0.92 |
| [S18/Q16](#s18) | success | ["treatmentoutcomes"] | 0 / {} | [] | ["COUNT(DISTINCT o.\"Treatment reference\")"] | 1 | 0.546 |
| [S19/Q17](#s19) | success | ["treatmentoutcomes"] | 0 / {} | [] | ["MIN(o.\"Treatment reference\")", "MAX(o.\"Treatment reference\")"] | 1 | 0.457 |
| [S20/Q18](#s20) | success | ["encounters"] | 0 / {} | ["e.\"Treatment Barriers\""] | ["COUNT(*)"] | 4 | 0.663 |
| [S21/Q19](#s21) | success | ["treatmentoutcomes"] | 0 / {} | ["o.\"Symptom improvement\""] | ["COUNT(*)"] | 3 | 0.806 |
| [S22/Q20](#s22) | success | ["encounters", "patients"] | 2 / {'LEFT': 1} | ["CASE WHEN p.Age BETWEEN 18 AND 44 THEN 'young_18-44' WHEN p.Age BETWEEN 45 AND 59 THEN 'middle_45-59' ELSE 'older_60+' END"] | ["COUNT(DISTINCT p.\"Patient number\")", "COUNT(DISTINCT e.\"Visit Record Number\")"] | 3 | 2.956 |
| [S23/Q21](#s23) | success | ["encounters", "patients"] | 2 / {'INNER': 1} | ["CASE WHEN p.Age BETWEEN 18 AND 44 THEN 'young_18-44' WHEN p.Age BETWEEN 45 AND 59 THEN 'middle_45-59' ELSE 'older_60+' END", "e.\"Treatment Barriers\""] | ["COUNT(*)"] | 12 | 2.278 |
| [S24/Q22](#s24) | success | ["encounters", "patients", "treatmentbasics", "treatmentoutcomes"] | 4 / {'INNER': 3} | ["CASE WHEN p.Age BETWEEN 18 AND 44 THEN 'young_18-44' WHEN p.Age BETWEEN 45 AND 59 THEN 'middle_45-59' ELSE 'older_60+' END", "o.\"Symptom improvement\""] | ["COUNT(*)"] | 9 | 4.246 |
| [S25/Q23](#s25) | success | ["encounters", "patients", "treatmentbasics", "treatmentoutcomes"] | 4 / {'INNER': 3} | ["CASE WHEN p.Age BETWEEN 18 AND 44 THEN 'young_18-44' WHEN p.Age BETWEEN 45 AND 59 THEN 'middle_45-59' ELSE 'older_60+' END", "e.\"Treatment Barriers\"", "o.\"Symptom improvement\""] | ["COUNT(*)"] | 36 | 4.786 |
| [S26/Q24](#s26) | success | ["encounters", "patients", "treatmentbasics", "treatmentoutcomes"] | 4 / {'INNER': 3} | [] | ["COUNT(*)"] | 1 | 3.643 |
| [S27/Q25](#s27) | success | ["encounters", "patients", "treatmentbasics", "treatmentoutcomes"] | 4 / {'INNER': 3} | ["age_group", "barrier", "improvement"] | ["COUNT(*)"] | 36 | 4.656 |
| [S28/Q26](#s28) | success | ["encounters", "patients", "treatmentbasics", "treatmentoutcomes"] | 4 / {'INNER': 3} | ["age_group", "adherence"] | ["COUNT(*)"] | 12 | 4.321 |
| [S29/Q27](#s29) | success | ["encounters", "patients", "treatmentbasics", "treatmentoutcomes"] | 4 / {'INNER': 3} | ["age_group", "barrier"] | ["AVG(missed)", "COUNT(*)"] | 12 | 4.675 |
| [S30/Q28](#s30) | success | ["encounters", "patients", "treatmentbasics", "treatmentoutcomes"] | 4 / {'INNER': 3} | ["age_group", "\"Financial stress\""] | ["COUNT(*)"] | 9 | 4.465 |
| [S31/Q29](#s31) | success | ["encounters", "patients", "treatmentbasics", "treatmentoutcomes"] | 4 / {'INNER': 3} | ["age_group", "\"Stigma effect\""] | ["COUNT(*)"] | 9 | 4.334 |
| [S32/Q30](#s32) | success | ["encounters", "patients", "treatmentbasics", "treatmentoutcomes"] | 4 / {'INNER': 3} | ["age_group", "\"Housing stability\""] | ["COUNT(*)"] | 12 | 4.372 |
| [S33/Q31](#s33) | success | ["encounters", "patients", "treatmentbasics", "treatmentoutcomes"] | 4 / {'INNER': 3} | ["age_group", "\"Employment status\""] | ["COUNT(*)"] | 15 | 4.492 |
| [S34/Q32](#s34) | success | ["encounters", "patients", "treatmentbasics", "treatmentoutcomes"] | 4 / {'INNER': 3} | ["age_group", "\"Insurance status\""] | ["COUNT(*)"] | 9 | 4.365 |
| [S35/Q33](#s35) | success | ["encounters", "patients", "treatmentbasics", "treatmentoutcomes"] | 4 / {'INNER': 3} | ["CASE WHEN p.Age BETWEEN 18 AND 44 THEN 'young_18-44' WHEN p.Age BETWEEN 45 AND 59 THEN 'middle_45-59' ELSE 'older_60+' END", "e.\"Treatment Barriers\""] | ["COUNT(*)"] | 12 | 4.448 |
| [S36/Q34](#s36) | success | ["encounters", "patients", "treatmentbasics", "treatmentoutcomes"] | 4 / {'INNER': 3} | ["CASE WHEN p.Age BETWEEN 18 AND 44 THEN 'young_18-44' WHEN p.Age BETWEEN 45 AND 59 THEN 'middle_45-59' ELSE 'older_60+' END", "o.\"Symptom improvement\""] | ["COUNT(*)"] | 9 | 4.059 |
| [S37/Q35](#s37) | success | ["encounters", "patients", "treatmentbasics", "treatmentoutcomes"] | 4 / {'INNER': 3} | ["CASE WHEN p.Age BETWEEN 18 AND 44 THEN 'young_18-44' WHEN p.Age BETWEEN 45 AND 59 THEN 'middle_45-59' ELSE 'older_60+' END", "e.\"Treatment Barriers\"", "o.\"Symptom improvement\""] | ["COUNT(*)"] | 36 | 4.174 |
| [S38/Q36](#s38) | success | ["encounters", "patients", "treatmentbasics", "treatmentoutcomes"] | 4 / {'INNER': 3} | ["CASE WHEN p.Age BETWEEN 18 AND 44 THEN 'Young Adults (18-44)' WHEN p.Age BETWEEN 45 AND 59 THEN 'Middle-aged (45-59)' ELSE 'Older Adults (60+)' END", "e.\"Treatment Barriers\""] | ["COUNT(*)"] | 12 | 4.508 |
| [S39/Q37](#s39) | success | ["encounters", "patients", "treatmentbasics", "treatmentoutcomes"] | 4 / {'INNER': 3} | ["CASE WHEN p.Age BETWEEN 18 AND 44 THEN 'Young Adults (18-44)' WHEN p.Age BETWEEN 45 AND 59 THEN 'Middle-aged (45-59)' ELSE 'Older Adults (60+)' END", "o.\"Symptom improvement\""] | ["COUNT(*)"] | 9 | 4.384 |
| [S40/Q38](#s40) | success | ["encounters", "patients", "treatmentbasics", "treatmentoutcomes"] | 4 / {'INNER': 3} | ["CASE WHEN p.Age BETWEEN 18 AND 44 THEN 'Young Adults (18-44)' WHEN p.Age BETWEEN 45 AND 59 THEN 'Middle-aged (45-59)' ELSE 'Older Adults (60+)' END", "e.\"Treatment Barriers\"", "o.\"Symptom improvement\""] | ["COUNT(*)"] | 36 | 4.699 |
| [S41/Q39](#s41) | success | ["encounters", "patients", "treatmentbasics", "treatmentoutcomes"] | 4 / {'INNER': 3} | ["CASE WHEN p.Age BETWEEN 18 AND 44 THEN 'Young Adults (18-44)' WHEN p.Age BETWEEN 45 AND 59 THEN 'Middle-aged (45-59)' ELSE 'Older Adults (60+)' END", "p.\"Financial stress\""] | ["COUNT(*)"] | 9 | 4.478 |
| [S42/Q40](#s42) | success | ["encounters", "patients", "treatmentbasics", "treatmentoutcomes"] | 4 / {'INNER': 3} | ["CASE WHEN p.Age BETWEEN 18 AND 44 THEN 'Young Adults (18-44)' WHEN p.Age BETWEEN 45 AND 59 THEN 'Middle-aged (45-59)' ELSE 'Older Adults (60+)' END", "p.\"Stigma effect\""] | ["COUNT(*)"] | 9 | 4.297 |
| [S43/Q41](#s43) | success | ["encounters", "patients", "treatmentbasics", "treatmentoutcomes"] | 4 / {'INNER': 3} | ["CASE WHEN p.Age BETWEEN 18 AND 44 THEN 'Young Adults (18-44)' WHEN p.Age BETWEEN 45 AND 59 THEN 'Middle-aged (45-59)' ELSE 'Older Adults (60+)' END", "p.\"Housing stability\""] | ["COUNT(*)"] | 12 | 4.228 |
| [S44/Q42](#s44) | success | ["encounters", "patients", "treatmentbasics", "treatmentoutcomes"] | 4 / {'INNER': 3} | ["CASE WHEN p.Age BETWEEN 18 AND 44 THEN 'Young Adults (18-44)' WHEN p.Age BETWEEN 45 AND 59 THEN 'Middle-aged (45-59)' ELSE 'Older Adults (60+)' END", "p.\"Employment status\""] | ["COUNT(*)"] | 15 | 4.332 |
| [S45/Q43](#s45) | success | ["encounters", "patients", "treatmentbasics", "treatmentoutcomes"] | 4 / {'INNER': 3} | ["CASE WHEN p.Age BETWEEN 18 AND 44 THEN 'Young Adults (18-44)' WHEN p.Age BETWEEN 45 AND 59 THEN 'Middle-aged (45-59)' ELSE 'Older Adults (60+)' END", "p.\"Insurance status\""] | ["COUNT(*)"] | 9 | 4.389 |
| [S46/Q44](#s46) | success | ["encounters", "patients", "treatmentbasics", "treatmentoutcomes"] | 4 / {'INNER': 3} | ["CASE WHEN p.Age BETWEEN 18 AND 44 THEN 'Young Adults (18-44)' WHEN p.Age BETWEEN 45 AND 59 THEN 'Middle-aged (45-59)' ELSE 'Older Adults (60+)' END", "o.\"Treatment adherence\""] | ["COUNT(*)"] | 12 | 4.227 |
| [S47/Q45](#s47) | success | ["encounters", "patients", "treatmentbasics", "treatmentoutcomes"] | 4 / {'INNER': 3} | [] | [] | 1000 | 5.571 |
| [S48/Q46](#s48) | success | ["encounters", "patients", "treatmentbasics", "treatmentoutcomes"] | 4 / {'INNER': 3} | [] | [] | 1000 | 5.845 |
| [S49/Q47](#s49) | success | ["encounters", "patients", "treatmentbasics", "treatmentoutcomes"] | 4 / {'INNER': 3} | [] | [] | 1000 | 4.973 |
| [S50/Q48](#s50) | success | ["assessmentbasics", "assessmentsocialanddiagnosis", "encounters", "patients"] | 4 / {'INNER': 3} | ["CASE WHEN p.Age BETWEEN 18 AND 44 THEN 'young_18-44' WHEN p.Age BETWEEN 45 AND 59 THEN 'middle_45-59' ELSE 'older_60+' END", "d.\"Primary Diagnosis\""] | ["COUNT(*)"] | 15 | 4.783 |
| [S51/Q49](#s51) | success | ["assessmentsocialanddiagnosis"] | 0 / {} | [] | [] | 5 | 0.409 |
| [S52/Q50](#s52) | success | ["assessmentbasics", "assessmentsocialanddiagnosis", "encounters", "patients"] | 4 / {'INNER': 3} | ["CASE WHEN p.Age BETWEEN 18 AND 44 THEN 'young_18-44' WHEN p.Age BETWEEN 45 AND 59 THEN 'middle_45-59' ELSE 'older_60+' END", "d.\"Primary Diagnosis\""] | ["COUNT(*)"] | 15 | 4.461 |
| [S53/Q51](#s53) | success | ["encounters", "patients", "treatmentbasics", "treatmentoutcomes"] | 4 / {'INNER': 3} | ["age_group", "\"Medication Adherence\""] | ["COUNT(*)"] | 3 | 4.13 |
| [S54/Q52](#s54) | success | ["encounters", "patients", "treatmentbasics", "treatmentoutcomes"] | 4 / {'INNER': 3} | ["age_group", "\"Medication Side Effects\""] | ["COUNT(*)"] | 3 | 4.039 |
| [S55/Q53](#s55) | success | ["treatmentbasics"] | 0 / {} | [] | [] | 4 | 0.897 |
| [S56/Q54](#s56) | success | ["treatmentbasics"] | 0 / {} | [] | [] | 3 | 0.557 |
| [S57/Q55](#s57) | success | ["encounters", "patients", "treatmentbasics", "treatmentoutcomes"] | 4 / {'INNER': 3} | ["age_group", "med_adh"] | ["COUNT(*)"] | 12 | 4.31 |
| [S58/Q56](#s58) | success | ["encounters", "patients", "treatmentbasics", "treatmentoutcomes"] | 4 / {'INNER': 3} | ["age_group", "side_eff"] | ["COUNT(*)"] | 9 | 4.159 |
| [S59/Q57](#s59) | success | ["assessmentbasics", "assessmentsocialanddiagnosis", "encounters", "patients"] | 4 / {'INNER': 3} | ["CASE WHEN p.Age BETWEEN 18 AND 44 THEN 'young_18-44' WHEN p.Age BETWEEN 45 AND 59 THEN 'middle_45-59' ELSE 'older_60+' END", "d.\"Primary Diagnosis\""] | ["COUNT(*)"] | 15 | 4.322 |
| [S60/Q58](#s60) | success | ["assessmentbasics", "assessmentsocialanddiagnosis", "encounters", "patients"] | 4 / {'INNER': 3} | ["CASE WHEN p.Age BETWEEN 18 AND 44 THEN 'young_18-44' WHEN p.Age BETWEEN 45 AND 59 THEN 'middle_45-59' ELSE 'older_60+' END", "d.\"Primary Diagnosis\""] | ["COUNT(*)"] | 15 | 4.538 |


## 元数据和设置

| SQL | 类别 | 状态 | 内容 |
| --- | --- | --- | --- |
| S1 | connection_setup | success | PRAGMA query_only=ON |
| S2 | metadata | success | SELECT name,sql FROM sqlite_master WHERE type='table' ORDER BY name |


## Python 与执行位置

人工源码审查：**database_first_violation**。SQL 关联患者年龄、依从性障碍、症状改善等字段并做多维汇总。Python 拟合逻辑回归属于合理数值补充；但 P1/P2 重算分母并合并，P4/P5 按年龄×障碍汇总不依从/改善比例和满意度，这些可以在 SQL 完成。这里仅审查计算位置，不评判临床建议是否正确。 [证据](../reviews/dacomp-042.json)。

P1：Chi-square tests and visualizations: The statistical tests (chi-square of independence) and visualizations (stacked bar charts, heatmaps) are best done in Python with scipy and matplotlib. SQLite cannot compute chi-square p-values or produce publication-quality figures.

[源码](../../../runs/dsv4flash-db-first-full-01/dacomp-042/attempt-01/python/P1.py)；[输出](../../../runs/dsv4flash-db-first-full-01/dacomp-042/attempt-01/python/P1.stdout)；[错误](../../../runs/dsv4flash-db-first-full-01/dacomp-042/attempt-01/python/P1.stderr)。检出需人工核验的 SQL 可实现操作：groupby(, .merge(, .query(；不能仅凭理由判为合规。

P2：Create visualizations to show barrier distribution, symptom improvement patterns, and patient characteristics across age groups. These are best created in Python with matplotlib/seaborn.

[源码](../../../runs/dsv4flash-db-first-full-01/dacomp-042/attempt-01/python/P2.py)；[输出](../../../runs/dsv4flash-db-first-full-01/dacomp-042/attempt-01/python/P2.stdout)；[错误](../../../runs/dsv4flash-db-first-full-01/dacomp-042/attempt-01/python/P2.stderr)。检出需人工核验的 SQL 可实现操作：groupby(, .query(；不能仅凭理由判为合规。

P3：Test whether barrier type affects improvement overall, and run a binomial/logistic-style regression to test the barrier-by-age interaction on the odds of minimal (vs better) improvement. SQLite lacks regression and interaction testing; scipy/statsmodels via numpy is appropriate. I will implement a simple logit manually with scipy.

[源码](../../../runs/dsv4flash-db-first-full-01/dacomp-042/attempt-01/python/P3.py)；[输出](../../../runs/dsv4flash-db-first-full-01/dacomp-042/attempt-01/python/P3.stdout)；[错误](../../../runs/dsv4flash-db-first-full-01/dacomp-042/attempt-01/python/P3.stderr)。检出需人工核验的 SQL 可实现操作：groupby(, .query(；不能仅凭理由判为合规。

P4：Quantify non-compliance rates and minimal-improvement rates per barrier within each age group, run post-hoc significance tests, and create final figures. These statistical contrasts and figures are better handled in Python than SQLite.

[源码](../../../runs/dsv4flash-db-first-full-01/dacomp-042/attempt-01/python/P4.py)；[输出](../../../runs/dsv4flash-db-first-full-01/dacomp-042/attempt-01/python/P4.stdout)；[错误](../../../runs/dsv4flash-db-first-full-01/dacomp-042/attempt-01/python/P4.stderr)。检出需人工核验的 SQL 可实现操作：groupby(, .query(；不能仅凭理由判为合规。

P5：Fix the figure creation for significant improvement and satisfaction rates. The pivot column ordering issue is best handled in Python with explicit column selection.

[源码](../../../runs/dsv4flash-db-first-full-01/dacomp-042/attempt-01/python/P5.py)；[输出](../../../runs/dsv4flash-db-first-full-01/dacomp-042/attempt-01/python/P5.stdout)；[错误](../../../runs/dsv4flash-db-first-full-01/dacomp-042/attempt-01/python/P5.stderr)。检出需人工核验的 SQL 可实现操作：groupby(, .query(；不能仅凭理由判为合规。

## 优化机会

已验证候选。筛选限于精确 SQL、相同自包含 CTE、相同单表完整过滤、可分解单表聚合；未覆盖任意 Join 等价和一般谓词蕴含。全部候选都是 offline，未测在线预测。

| 候选 | 类型 | 已有结果 | 覆盖 SQL | 后续次数 | 中间行数 | 验证 | 成本 |
| --- | --- | --- | --- | --- | --- | --- | --- |
| C1 | exact-result reuse | True | ["S24", "S36"] | 1 | 9 | verified | Not benchmarked; correctness alone does not establish net speedup. |
| C2 | exact-result reuse | True | ["S25", "S37"] | 1 | 36 | verified | Not benchmarked; correctness alone does not establish net speedup. |
| C3 | exact-result reuse | True | ["S50", "S52", "S59"] | 2 | 15 | verified | Not benchmarked; correctness alone does not establish net speedup. |
| C4 | aggregate MV | False | ["S11", "S20"] | 1 | unknown | not_verified_cap | Not tested |
| C5 | aggregate MV | False | ["S15", "S21"] | 1 | unknown | not_verified_cap | Not tested |


已验证覆盖（含触发查询、候选并集去重）：7/58 条成功数据 SQL。正确性仅针对当前数据库快照；未测性能的候选不能声称已加速。

[完整 build/rewrite 与比较证据](dacomp-042.analysis.json)。

### C3：exact-result reuse

Identical normalized SQL and parameters; archive equality checked.

原查询 [S50](#s50), [S52](#s52), [S59](#s59) → 保留前序结果 S50 → 后续 2 次可复用。该构建点为事后假设，不代表 Agent 当时预知后续。

| 原 SQL | 列名一致 | 结果一致 | 比较方法 |
| --- | --- | --- | --- |
| S52 | True | True | ordered_numeric_tolerance |
| S59 | True | True | ordered_numeric_tolerance |


验证状态：verified；成本结论：Not benchmarked; correctness alone does not establish net speedup.

### C1：exact-result reuse

Identical normalized SQL and parameters; archive equality checked.

原查询 [S24](#s24), [S36](#s36) → 保留前序结果 S24 → 后续 1 次可复用。该构建点为事后假设，不代表 Agent 当时预知后续。

| 原 SQL | 列名一致 | 结果一致 | 比较方法 |
| --- | --- | --- | --- |
| S36 | True | True | ordered_numeric_tolerance |


验证状态：verified；成本结论：Not benchmarked; correctness alone does not establish net speedup.

### C2：exact-result reuse

Identical normalized SQL and parameters; archive equality checked.

原查询 [S25](#s25), [S37](#s37) → 保留前序结果 S25 → 后续 1 次可复用。该构建点为事后假设，不代表 Agent 当时预知后续。

| 原 SQL | 列名一致 | 结果一致 | 比较方法 |
| --- | --- | --- | --- |
| S37 | True | True | ordered_numeric_tolerance |


验证状态：verified；成本结论：Not benchmarked; correctness alone does not establish net speedup.

结果依赖：自动记录 SQL→Python 的接口父调用，以及源码中引用归档文件的消费者；字面值相同不认定因果。模型方向选择需要人工读取消息，尚未做全面因果标注。

[原始报告](../../../runs/dsv4flash-db-first-full-01/dacomp-042/attempt-01/answer.md)；[统一消息](../../../runs/dsv4flash-db-first-full-01/dacomp-042/attempt-01/messages.jsonl)；[原始 OpenCode 事件](../../../runs/dsv4flash-db-first-full-01/dacomp-042/attempt-01/opencode.jsonl)；[SQL 引擎日志](../../../runs/dsv4flash-db-first-full-01/dacomp-042/attempt-01/sql_journal.jsonl)。

[可读报告（本地图片链接规范化）](../answers/dacomp-042.md)。原始回答保留，分析结论未改写。

## S1

类别 `connection_setup`；来源 `connection`；调用 `f42d18545ad84d96ab0da7d67478f6fb`；状态 `success`。

```sql
PRAGMA query_only=ON
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-042/attempt-01/sql/S1.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-042/attempt-01/sql/S1.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-042/attempt-01/results/S1.rows.jsonl)；完整：True；SHA256：`e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`。

## S2

类别 `metadata`；来源 `list_db`；调用 `f42d18545ad84d96ab0da7d67478f6fb`；状态 `success`。

```sql
SELECT name,sql FROM sqlite_master WHERE type='table' ORDER BY name
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-042/attempt-01/sql/S2.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-042/attempt-01/sql/S2.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-042/attempt-01/results/S2.rows.jsonl)；完整：True；SHA256：`4dac64a578482a9c307597fd63a804db12fb862d7bf31e3a2fcf2f8659e7cdd1`。

## S3

类别 `data`；来源 `query_db`；调用 `f841274e4b6247af9fc956023b6c13eb`；状态 `success`。

```sql
SELECT * FROM patients LIMIT 5
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-042/attempt-01/sql/S3.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-042/attempt-01/sql/S3.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-042/attempt-01/results/S3.rows.jsonl)；完整：True；SHA256：`11de47f2e686a874a8dd6eaef9954a8b120f0531be030250aa65c3ca6bc66d19`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "patients", "kind": "base", "block": null, "base_tables": ["patients"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |


## S4

类别 `data`；来源 `query_db`；调用 `7229407ab4fb4e46a74a7ad4e003fafe`；状态 `success`。

```sql
SELECT * FROM encounters LIMIT 5
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-042/attempt-01/sql/S4.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-042/attempt-01/sql/S4.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-042/attempt-01/results/S4.rows.jsonl)；完整：True；SHA256：`f521030f776454c731b8a3d15fa14b523f25658ed3fe07cecae768bd1270ab9a`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "encounters", "kind": "base", "block": null, "base_tables": ["encounters"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |


## S5

类别 `data`；来源 `query_db`；调用 `68bbcfcfd42d4b538f950393ef19d110`；状态 `success`。

```sql
SELECT DISTINCT "Treatment Barriers" FROM encounters
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-042/attempt-01/sql/S5.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-042/attempt-01/sql/S5.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-042/attempt-01/results/S5.rows.jsonl)；完整：True；SHA256：`a178f5ad5b40b7e586d30e09313d52eb815ee7a88aa7f9c879464d5ac0d651e9`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "encounters", "kind": "base", "block": null, "base_tables": ["encounters"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |


## S6

类别 `data`；来源 `query_db`；调用 `1a9b67c1898545e38b240c258841f541`；状态 `success`。

```sql
SELECT DISTINCT "Symptom improvement" FROM treatmentoutcomes
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-042/attempt-01/sql/S6.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-042/attempt-01/sql/S6.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-042/attempt-01/results/S6.rows.jsonl)；完整：True；SHA256：`43102403c47de2d0ceeb460016337eeb9ed46dc9e4f09c954f84c2123348f0fa`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "treatmentoutcomes", "kind": "base", "block": null, "base_tables": ["treatmentoutcomes"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |


## S7

类别 `data`；来源 `query_db`；调用 `b573428a4bf443b68d17718f25af440d`；状态 `success`。

```sql
SELECT DISTINCT "Treatment adherence" FROM treatmentoutcomes
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-042/attempt-01/sql/S7.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-042/attempt-01/sql/S7.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-042/attempt-01/results/S7.rows.jsonl)；完整：True；SHA256：`17ecbff287121226eff1e6dac3d6c77e6d36377a21aee1764292dfef6da06aed`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "treatmentoutcomes", "kind": "base", "block": null, "base_tables": ["treatmentoutcomes"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |


## S8

类别 `data`；来源 `query_db`；调用 `4e2da85c78db4b868f734f83da359b63`；状态 `success`。

```sql
SELECT MIN(Age), MAX(Age), AVG(Age) FROM patients
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-042/attempt-01/sql/S8.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-042/attempt-01/sql/S8.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-042/attempt-01/results/S8.rows.jsonl)；完整：True；SHA256：`ec287c1af22f10fd6eec884fbf7cfb5549ee85372afba5329327ad16e4b7a208`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "patients", "kind": "base", "block": null, "base_tables": ["patients"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | MIN(Age) | [{"table": "patients", "column": "Age"}] | [] | False |
| B1 | MAX(Age) | [{"table": "patients", "column": "Age"}] | [] | False |
| B1 | AVG(Age) | [{"table": "patients", "column": "Age"}] | [] | False |


## S9

类别 `data`；来源 `query_db`；调用 `a71e6f48e47747d29e8e566802978ce1`；状态 `success`。

```sql
SELECT p.Age, e."Treatment Barriers", e."Patient Reference Number"
FROM encounters e
JOIN patients p ON e."Patient Reference Number" = p."Patient number"
LIMIT 20
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-042/attempt-01/sql/S9.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-042/attempt-01/sql/S9.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-042/attempt-01/results/S9.rows.jsonl)；完整：True；SHA256：`787b60e9eba9bf6451f227c02e629c8292a90439dbf56423d2581ae7d3b2f3dd`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "e", "kind": "base", "block": null, "base_tables": ["encounters"]}, {"alias": "p", "kind": "base", "block": null, "base_tables": ["patients"]}] | [{"type": "INNER", "right": "patients AS p", "on": "e.\"Patient Reference Number\" = p.\"Patient number\"", "using": []}] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |


## S10

类别 `data`；来源 `query_db`；调用 `40e03a8c6d3b43289a8183a85c9945de`；状态 `success`。

```sql
SELECT COUNT(*) as total_patients FROM patients
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-042/attempt-01/sql/S10.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-042/attempt-01/sql/S10.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-042/attempt-01/results/S10.rows.jsonl)；完整：True；SHA256：`e3ed33dc26a723b8481ca677e38dc4a6e8700aeec312afdd02c9dd92374161a2`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "patients", "kind": "base", "block": null, "base_tables": ["patients"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |


## S11

类别 `data`；来源 `query_db`；调用 `409c7f8cdee0490bbbb9ad1a71e39a17`；状态 `success`。

```sql
SELECT COUNT(*) as total_encounters FROM encounters
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-042/attempt-01/sql/S11.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-042/attempt-01/sql/S11.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-042/attempt-01/results/S11.rows.jsonl)；完整：True；SHA256：`b95cc485231360cd221bafab8a2a259fde825f811a6e189af03033e24268f136`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "encounters", "kind": "base", "block": null, "base_tables": ["encounters"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |


## S12

类别 `data`；来源 `query_db`；调用 `d8e2d055a8c84dc6ac9bbd84da462dd6`；状态 `success`。

```sql
SELECT * FROM treatmentoutcomes LIMIT 5
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-042/attempt-01/sql/S12.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-042/attempt-01/sql/S12.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-042/attempt-01/results/S12.rows.jsonl)；完整：True；SHA256：`749e8540749060dc6f11bc5cca816055caa8a8152eb000105ab6c6676628b596`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "treatmentoutcomes", "kind": "base", "block": null, "base_tables": ["treatmentoutcomes"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |


## S13

类别 `data`；来源 `query_db`；调用 `28a3886641e74984b4ef3d37fc0d65e4`；状态 `success`。

```sql
SELECT * FROM treatmentbasics LIMIT 5
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-042/attempt-01/sql/S13.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-042/attempt-01/sql/S13.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-042/attempt-01/results/S13.rows.jsonl)；完整：True；SHA256：`ac8df9db452b9e472f256c733f40006998dfc3d3f9b1bca4f443eebedde4a8a4`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "treatmentbasics", "kind": "base", "block": null, "base_tables": ["treatmentbasics"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |


## S14

类别 `data`；来源 `query_db`；调用 `184b49ea14c045858f6d17142677f03a`；状态 `success`。

```sql
SELECT COUNT(DISTINCT e."Visit Record Number") FROM encounters e
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-042/attempt-01/sql/S14.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-042/attempt-01/sql/S14.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-042/attempt-01/results/S14.rows.jsonl)；完整：True；SHA256：`b95cc485231360cd221bafab8a2a259fde825f811a6e189af03033e24268f136`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "e", "kind": "base", "block": null, "base_tables": ["encounters"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(DISTINCT e."Visit Record Number") | [{"table": "encounters", "column": "Visit Record Number"}] | [] | False |


## S15

类别 `data`；来源 `query_db`；调用 `838e9c466d54482e8f9f877c5462810b`；状态 `success`。

```sql
SELECT COUNT(*) FROM treatmentoutcomes
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-042/attempt-01/sql/S15.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-042/attempt-01/sql/S15.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-042/attempt-01/results/S15.rows.jsonl)；完整：True；SHA256：`e3ed33dc26a723b8481ca677e38dc4a6e8700aeec312afdd02c9dd92374161a2`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "treatmentoutcomes", "kind": "base", "block": null, "base_tables": ["treatmentoutcomes"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |


## S16

类别 `data`；来源 `query_db`；调用 `b084db331aa643c883906d2147a83c31`；状态 `success`。

```sql
SELECT MIN("Treatment ID") min_id, MAX("Treatment ID") max_id, COUNT(*) cnt FROM treatmentbasics
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-042/attempt-01/sql/S16.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-042/attempt-01/sql/S16.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-042/attempt-01/results/S16.rows.jsonl)；完整：True；SHA256：`b361854fae21ae9913670c870b923a8c1b64ceaec055788a845a6f7371da4d2a`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "treatmentbasics", "kind": "base", "block": null, "base_tables": ["treatmentbasics"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | MIN("Treatment ID") | [{"table": "treatmentbasics", "column": "Treatment ID"}] | [] | False |
| B1 | MAX("Treatment ID") | [{"table": "treatmentbasics", "column": "Treatment ID"}] | [] | False |
| B1 | COUNT(*) | [] | [] | True |


## S17

类别 `data`；来源 `query_db`；调用 `27b15cf6133b489c94ed8335d5fdff11`；状态 `success`。

```sql
SELECT COUNT(DISTINCT tb."Visit Reference") FROM treatmentbasics tb
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-042/attempt-01/sql/S17.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-042/attempt-01/sql/S17.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-042/attempt-01/results/S17.rows.jsonl)；完整：True；SHA256：`b95cc485231360cd221bafab8a2a259fde825f811a6e189af03033e24268f136`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "tb", "kind": "base", "block": null, "base_tables": ["treatmentbasics"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(DISTINCT tb."Visit Reference") | [{"table": "treatmentbasics", "column": "Visit Reference"}] | [] | False |


## S18

类别 `data`；来源 `query_db`；调用 `f265330b11194747b042d51157f55291`；状态 `success`。

```sql
SELECT COUNT(DISTINCT o."Treatment reference") FROM treatmentoutcomes o
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-042/attempt-01/sql/S18.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-042/attempt-01/sql/S18.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-042/attempt-01/results/S18.rows.jsonl)；完整：True；SHA256：`e3ed33dc26a723b8481ca677e38dc4a6e8700aeec312afdd02c9dd92374161a2`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "o", "kind": "base", "block": null, "base_tables": ["treatmentoutcomes"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(DISTINCT o."Treatment reference") | [{"table": "treatmentoutcomes", "column": "Treatment reference"}] | [] | False |


## S19

类别 `data`；来源 `query_db`；调用 `23bd75b37bc34b0bb5bb52e7cb26bdec`；状态 `success`。

```sql
SELECT MIN(o."Treatment reference"), MAX(o."Treatment reference") FROM treatmentoutcomes o
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-042/attempt-01/sql/S19.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-042/attempt-01/sql/S19.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-042/attempt-01/results/S19.rows.jsonl)；完整：True；SHA256：`f5dbe6c8c557cd458b2119fa0b785a55fcd6bec1d35739107481ccba6c8a8fbd`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "o", "kind": "base", "block": null, "base_tables": ["treatmentoutcomes"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | MIN(o."Treatment reference") | [{"table": "treatmentoutcomes", "column": "Treatment reference"}] | [] | False |
| B1 | MAX(o."Treatment reference") | [{"table": "treatmentoutcomes", "column": "Treatment reference"}] | [] | False |


## S20

类别 `data`；来源 `query_db`；调用 `c35da9c7d44d49fabaac52c8db9e93f6`；状态 `success`。

```sql
SELECT e."Treatment Barriers", COUNT(*) cnt
FROM encounters e
GROUP BY e."Treatment Barriers"
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-042/attempt-01/sql/S20.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-042/attempt-01/sql/S20.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-042/attempt-01/results/S20.rows.jsonl)；完整：True；SHA256：`c382eba9498177da401d434445120f7859e0e726016b3c64abef881a1f9e7c98`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "e", "kind": "base", "block": null, "base_tables": ["encounters"]}] | [] | ["e.\"Treatment Barriers\""] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |


## S21

类别 `data`；来源 `query_db`；调用 `6c25f017202546d3b9ace65ac4d7280b`；状态 `success`。

```sql
SELECT o."Symptom improvement", COUNT(*) cnt
FROM treatmentoutcomes o
GROUP BY o."Symptom improvement"
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-042/attempt-01/sql/S21.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-042/attempt-01/sql/S21.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-042/attempt-01/results/S21.rows.jsonl)；完整：True；SHA256：`590cf1cd2aedee6df9cc8a8e86c0ce85f5a8c2196f5b3d0fdde22336abe06588`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "o", "kind": "base", "block": null, "base_tables": ["treatmentoutcomes"]}] | [] | ["o.\"Symptom improvement\""] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |


## S22

类别 `data`；来源 `query_db`；调用 `07187950e5c44d008788577fc076af85`；状态 `success`。

```sql
SELECT
  CASE WHEN p.Age BETWEEN 18 AND 44 THEN 'young_18-44'
       WHEN p.Age BETWEEN 45 AND 59 THEN 'middle_45-59'
       ELSE 'older_60+' END AS age_group,
  COUNT(DISTINCT p."Patient number") as n_patients,
  COUNT(DISTINCT e."Visit Record Number") as n_visits
FROM patients p
LEFT JOIN encounters e ON e."Patient Reference Number" = p."Patient number"
GROUP BY age_group
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-042/attempt-01/sql/S22.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-042/attempt-01/sql/S22.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-042/attempt-01/results/S22.rows.jsonl)；完整：True；SHA256：`688cc5402f9770325508c33b11e325eca05bc9c875e9cd0f76c7adbb26128987`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "p", "kind": "base", "block": null, "base_tables": ["patients"]}, {"alias": "e", "kind": "base", "block": null, "base_tables": ["encounters"]}] | [{"type": "LEFT", "right": "encounters AS e", "on": "e.\"Patient Reference Number\" = p.\"Patient number\"", "using": []}] | ["CASE WHEN p.Age BETWEEN 18 AND 44 THEN 'young_18-44' WHEN p.Age BETWEEN 45 AND 59 THEN 'middle_45-59' ELSE 'older_60+' END"] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(DISTINCT p."Patient number") | [{"table": "patients", "column": "Patient number"}] | [] | False |
| B1 | COUNT(DISTINCT e."Visit Record Number") | [{"table": "encounters", "column": "Visit Record Number"}] | [] | False |


## S23

类别 `data`；来源 `query_db`；调用 `79411f3b026a443da86c2130f9f4c9a8`；状态 `success`。

```sql
SELECT
  CASE WHEN p.Age BETWEEN 18 AND 44 THEN 'young_18-44'
       WHEN p.Age BETWEEN 45 AND 59 THEN 'middle_45-59'
       ELSE 'older_60+' END AS age_group,
  e."Treatment Barriers" AS barrier,
  COUNT(*) AS n
FROM encounters e
JOIN patients p ON e."Patient Reference Number" = p."Patient number"
GROUP BY age_group, barrier
ORDER BY age_group, n DESC
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-042/attempt-01/sql/S23.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-042/attempt-01/sql/S23.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-042/attempt-01/results/S23.rows.jsonl)；完整：True；SHA256：`33ada59be5dd31f23500caa00577b540df077ffce61850e96e7e04ad13ad5131`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "e", "kind": "base", "block": null, "base_tables": ["encounters"]}, {"alias": "p", "kind": "base", "block": null, "base_tables": ["patients"]}] | [{"type": "INNER", "right": "patients AS p", "on": "e.\"Patient Reference Number\" = p.\"Patient number\"", "using": []}] | ["CASE WHEN p.Age BETWEEN 18 AND 44 THEN 'young_18-44' WHEN p.Age BETWEEN 45 AND 59 THEN 'middle_45-59' ELSE 'older_60+' END", "e.\"Treatment Barriers\""] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |


## S24

类别 `data`；来源 `query_db`；调用 `71131eaebcb949f790c2b85782ef2b4a`；状态 `success`。

```sql
SELECT
  CASE WHEN p.Age BETWEEN 18 AND 44 THEN 'young_18-44'
       WHEN p.Age BETWEEN 45 AND 59 THEN 'middle_45-59'
       ELSE 'older_60+' END AS age_group,
  o."Symptom improvement" AS improvement,
  COUNT(*) AS n
FROM treatmentoutcomes o
JOIN treatmentbasics tb ON tb."Treatment ID" = o."Treatment reference"
JOIN encounters e ON e."Visit Record Number" = tb."Visit Reference"
JOIN patients p ON e."Patient Reference Number" = p."Patient number"
GROUP BY age_group, improvement
ORDER BY age_group, improvement
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-042/attempt-01/sql/S24.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-042/attempt-01/sql/S24.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-042/attempt-01/results/S24.rows.jsonl)；完整：True；SHA256：`288170516a86f6bdd608ac663c73ca3b3477704300da0989e8cc53deec6fc53c`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "o", "kind": "base", "block": null, "base_tables": ["treatmentoutcomes"]}, {"alias": "tb", "kind": "base", "block": null, "base_tables": ["treatmentbasics"]}, {"alias": "e", "kind": "base", "block": null, "base_tables": ["encounters"]}, {"alias": "p", "kind": "base", "block": null, "base_tables": ["patients"]}] | [{"type": "INNER", "right": "treatmentbasics AS tb", "on": "tb.\"Treatment ID\" = o.\"Treatment reference\"", "using": []}, {"type": "INNER", "right": "encounters AS e", "on": "e.\"Visit Record Number\" = tb.\"Visit Reference\"", "using": []}, {"type": "INNER", "right": "patients AS p", "on": "e.\"Patient Reference Number\" = p.\"Patient number\"", "using": []}] | ["CASE WHEN p.Age BETWEEN 18 AND 44 THEN 'young_18-44' WHEN p.Age BETWEEN 45 AND 59 THEN 'middle_45-59' ELSE 'older_60+' END", "o.\"Symptom improvement\""] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |


## S25

类别 `data`；来源 `query_db`；调用 `ca59b3fad0ce47ac920c6f6aab78212f`；状态 `success`。

```sql
SELECT
  CASE WHEN p.Age BETWEEN 18 AND 44 THEN 'young_18-44'
       WHEN p.Age BETWEEN 45 AND 59 THEN 'middle_45-59'
       ELSE 'older_60+' END AS age_group,
  e."Treatment Barriers" AS barrier,
  o."Symptom improvement" AS improvement,
  COUNT(*) AS n
FROM treatmentoutcomes o
JOIN treatmentbasics tb ON tb."Treatment ID" = o."Treatment reference"
JOIN encounters e ON e."Visit Record Number" = tb."Visit Reference"
JOIN patients p ON e."Patient Reference Number" = p."Patient number"
GROUP BY age_group, barrier, improvement
ORDER BY age_group, barrier, improvement
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-042/attempt-01/sql/S25.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-042/attempt-01/sql/S25.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-042/attempt-01/results/S25.rows.jsonl)；完整：True；SHA256：`bee4062079a5742431f92e466b2f6b1eb301eed9f39afc9ce011dae0875bebe8`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "o", "kind": "base", "block": null, "base_tables": ["treatmentoutcomes"]}, {"alias": "tb", "kind": "base", "block": null, "base_tables": ["treatmentbasics"]}, {"alias": "e", "kind": "base", "block": null, "base_tables": ["encounters"]}, {"alias": "p", "kind": "base", "block": null, "base_tables": ["patients"]}] | [{"type": "INNER", "right": "treatmentbasics AS tb", "on": "tb.\"Treatment ID\" = o.\"Treatment reference\"", "using": []}, {"type": "INNER", "right": "encounters AS e", "on": "e.\"Visit Record Number\" = tb.\"Visit Reference\"", "using": []}, {"type": "INNER", "right": "patients AS p", "on": "e.\"Patient Reference Number\" = p.\"Patient number\"", "using": []}] | ["CASE WHEN p.Age BETWEEN 18 AND 44 THEN 'young_18-44' WHEN p.Age BETWEEN 45 AND 59 THEN 'middle_45-59' ELSE 'older_60+' END", "e.\"Treatment Barriers\"", "o.\"Symptom improvement\""] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |


## S26

类别 `data`；来源 `query_db`；调用 `dc284c0a9e5344ad8f80e80a7e9b2c1f`；状态 `success`。

```sql
SELECT COUNT(*) AS joined_rows
FROM treatmentoutcomes o
JOIN treatmentbasics tb ON tb."Treatment ID" = o."Treatment reference"
JOIN encounters e ON e."Visit Record Number" = tb."Visit Reference"
JOIN patients p ON e."Patient Reference Number" = p."Patient number"
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-042/attempt-01/sql/S26.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-042/attempt-01/sql/S26.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-042/attempt-01/results/S26.rows.jsonl)；完整：True；SHA256：`e3ed33dc26a723b8481ca677e38dc4a6e8700aeec312afdd02c9dd92374161a2`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "o", "kind": "base", "block": null, "base_tables": ["treatmentoutcomes"]}, {"alias": "tb", "kind": "base", "block": null, "base_tables": ["treatmentbasics"]}, {"alias": "e", "kind": "base", "block": null, "base_tables": ["encounters"]}, {"alias": "p", "kind": "base", "block": null, "base_tables": ["patients"]}] | [{"type": "INNER", "right": "treatmentbasics AS tb", "on": "tb.\"Treatment ID\" = o.\"Treatment reference\"", "using": []}, {"type": "INNER", "right": "encounters AS e", "on": "e.\"Visit Record Number\" = tb.\"Visit Reference\"", "using": []}, {"type": "INNER", "right": "patients AS p", "on": "e.\"Patient Reference Number\" = p.\"Patient number\"", "using": []}] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |


## S27

类别 `data`；来源 `query_db`；调用 `d1de331157c7456ba400b089cf876813`；状态 `success`。

```sql
WITH joined AS (
  SELECT p.Age,
    CASE WHEN p.Age BETWEEN 18 AND 44 THEN 'young_18-44'
         WHEN p.Age BETWEEN 45 AND 59 THEN 'middle_45-59'
         ELSE 'older_60+' END AS age_group,
    e."Treatment Barriers" AS barrier,
    o."Symptom improvement" AS improvement,
    o."Treatment adherence" AS adherence,
    e."Missed Appointment" AS missed,
    p."Financial stress", p."Stigma effect", p."Housing stability", p."Insurance status",
    p."Employment status", p."Living situation", p."Disability status"
  FROM treatmentoutcomes o
  JOIN treatmentbasics tb ON tb."Treatment ID" = o."Treatment reference"
  JOIN encounters e ON e."Visit Record Number" = tb."Visit Reference"
  JOIN patients p ON e."Patient Reference Number" = p."Patient number"
)
SELECT age_group, barrier, improvement, COUNT(*) AS n
FROM joined
GROUP BY age_group, barrier, improvement
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-042/attempt-01/sql/S27.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-042/attempt-01/sql/S27.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-042/attempt-01/results/S27.rows.jsonl)；完整：True；SHA256：`bee4062079a5742431f92e466b2f6b1eb301eed9f39afc9ce011dae0875bebe8`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "o", "kind": "base", "block": null, "base_tables": ["treatmentoutcomes"]}, {"alias": "tb", "kind": "base", "block": null, "base_tables": ["treatmentbasics"]}, {"alias": "e", "kind": "base", "block": null, "base_tables": ["encounters"]}, {"alias": "p", "kind": "base", "block": null, "base_tables": ["patients"]}] | [{"type": "INNER", "right": "treatmentbasics AS tb", "on": "tb.\"Treatment ID\" = o.\"Treatment reference\"", "using": []}, {"type": "INNER", "right": "encounters AS e", "on": "e.\"Visit Record Number\" = tb.\"Visit Reference\"", "using": []}, {"type": "INNER", "right": "patients AS p", "on": "e.\"Patient Reference Number\" = p.\"Patient number\"", "using": []}] | [] |
| B2 | [{"alias": "joined", "kind": "derived", "block": "B1", "base_tables": ["encounters", "patients", "treatmentbasics", "treatmentoutcomes"]}] | [] | ["age_group", "barrier", "improvement"] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B2 | COUNT(*) | [] | [] | True |


## S28

类别 `data`；来源 `query_db`；调用 `d27abee84bbc4263a45f9436e8ab729e`；状态 `success`。

```sql
WITH joined AS (
  SELECT p.Age,
    CASE WHEN p.Age BETWEEN 18 AND 44 THEN 'young_18-44'
         WHEN p.Age BETWEEN 45 AND 59 THEN 'middle_45-59'
         ELSE 'older_60+' END AS age_group,
    e."Treatment Barriers" AS barrier,
    o."Symptom improvement" AS improvement,
    o."Treatment adherence" AS adherence,
    o."Treatment response" AS response,
    o."Treatment engagement" AS engagement,
    o."Therapeutic alliance" AS alliance,
    e."Missed Appointment" AS missed,
    p."Financial stress", p."Stigma effect", p."Housing stability", p."Insurance status",
    p."Employment status", p."Living situation", p."Disability status",
    p."Education level", p."Marital Status"
  FROM treatmentoutcomes o
  JOIN treatmentbasics tb ON tb."Treatment ID" = o."Treatment reference"
  JOIN encounters e ON e."Visit Record Number" = tb."Visit Reference"
  JOIN patients p ON e."Patient Reference Number" = p."Patient number"
)
SELECT age_group, adherence, COUNT(*) n FROM joined GROUP BY age_group, adherence ORDER BY age_group, n DESC
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-042/attempt-01/sql/S28.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-042/attempt-01/sql/S28.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-042/attempt-01/results/S28.rows.jsonl)；完整：True；SHA256：`21195142ec8afb9afe42ab6cab3c89d8ec077b73fabeb0ba13d97935eab94d1d`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "o", "kind": "base", "block": null, "base_tables": ["treatmentoutcomes"]}, {"alias": "tb", "kind": "base", "block": null, "base_tables": ["treatmentbasics"]}, {"alias": "e", "kind": "base", "block": null, "base_tables": ["encounters"]}, {"alias": "p", "kind": "base", "block": null, "base_tables": ["patients"]}] | [{"type": "INNER", "right": "treatmentbasics AS tb", "on": "tb.\"Treatment ID\" = o.\"Treatment reference\"", "using": []}, {"type": "INNER", "right": "encounters AS e", "on": "e.\"Visit Record Number\" = tb.\"Visit Reference\"", "using": []}, {"type": "INNER", "right": "patients AS p", "on": "e.\"Patient Reference Number\" = p.\"Patient number\"", "using": []}] | [] |
| B2 | [{"alias": "joined", "kind": "derived", "block": "B1", "base_tables": ["encounters", "patients", "treatmentbasics", "treatmentoutcomes"]}] | [] | ["age_group", "adherence"] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B2 | COUNT(*) | [] | [] | True |


## S29

类别 `data`；来源 `query_db`；调用 `5c4b89c7489943ee8bed9985c35fa07f`；状态 `success`。

```sql
WITH joined AS (
  SELECT p.Age,
    CASE WHEN p.Age BETWEEN 18 AND 44 THEN 'young_18-44'
         WHEN p.Age BETWEEN 45 AND 59 THEN 'middle_45-59'
         ELSE 'older_60+' END AS age_group,
    e."Treatment Barriers" AS barrier,
    e."Missed Appointment" AS missed
  FROM treatmentoutcomes o
  JOIN treatmentbasics tb ON tb."Treatment ID" = o."Treatment reference"
  JOIN encounters e ON e."Visit Record Number" = tb."Visit Reference"
  JOIN patients p ON e."Patient Reference Number" = p."Patient number"
)
SELECT age_group, barrier, AVG(missed) AS avg_missed, COUNT(*) n
FROM joined GROUP BY age_group, barrier ORDER BY age_group, barrier
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-042/attempt-01/sql/S29.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-042/attempt-01/sql/S29.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-042/attempt-01/results/S29.rows.jsonl)；完整：True；SHA256：`4945177acabb7f874a116be5ad34ce77788c0bca7c3eeb1321c2a83c013b6cae`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "o", "kind": "base", "block": null, "base_tables": ["treatmentoutcomes"]}, {"alias": "tb", "kind": "base", "block": null, "base_tables": ["treatmentbasics"]}, {"alias": "e", "kind": "base", "block": null, "base_tables": ["encounters"]}, {"alias": "p", "kind": "base", "block": null, "base_tables": ["patients"]}] | [{"type": "INNER", "right": "treatmentbasics AS tb", "on": "tb.\"Treatment ID\" = o.\"Treatment reference\"", "using": []}, {"type": "INNER", "right": "encounters AS e", "on": "e.\"Visit Record Number\" = tb.\"Visit Reference\"", "using": []}, {"type": "INNER", "right": "patients AS p", "on": "e.\"Patient Reference Number\" = p.\"Patient number\"", "using": []}] | [] |
| B2 | [{"alias": "joined", "kind": "derived", "block": "B1", "base_tables": ["encounters", "patients", "treatmentbasics", "treatmentoutcomes"]}] | [] | ["age_group", "barrier"] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B2 | AVG(missed) | [{"table": "encounters", "column": "Missed Appointment"}] | [] | False |
| B2 | COUNT(*) | [] | [] | True |


## S30

类别 `data`；来源 `query_db`；调用 `b2bf8539d889409fa175d94980222a32`；状态 `success`。

```sql
WITH joined AS (
  SELECT p.Age,
    CASE WHEN p.Age BETWEEN 18 AND 44 THEN 'young_18-44'
         WHEN p.Age BETWEEN 45 AND 59 THEN 'middle_45-59'
         ELSE 'older_60+' END AS age_group,
    p."Financial stress", p."Stigma effect", p."Housing stability", p."Insurance status",
    p."Employment status", p."Living situation", p."Disability status", p."Education level", p."Marital Status"
  FROM treatmentoutcomes o
  JOIN treatmentbasics tb ON tb."Treatment ID" = o."Treatment reference"
  JOIN encounters e ON e."Visit Record Number" = tb."Visit Reference"
  JOIN patients p ON e."Patient Reference Number" = p."Patient number"
)
SELECT age_group, "Financial stress", COUNT(*) n FROM joined GROUP BY age_group, "Financial stress" ORDER BY age_group, n DESC
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-042/attempt-01/sql/S30.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-042/attempt-01/sql/S30.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-042/attempt-01/results/S30.rows.jsonl)；完整：True；SHA256：`e0861b529bf051b7066ada0370040a9b3e860188e4ce4d2f481b3a92ae42c21c`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "o", "kind": "base", "block": null, "base_tables": ["treatmentoutcomes"]}, {"alias": "tb", "kind": "base", "block": null, "base_tables": ["treatmentbasics"]}, {"alias": "e", "kind": "base", "block": null, "base_tables": ["encounters"]}, {"alias": "p", "kind": "base", "block": null, "base_tables": ["patients"]}] | [{"type": "INNER", "right": "treatmentbasics AS tb", "on": "tb.\"Treatment ID\" = o.\"Treatment reference\"", "using": []}, {"type": "INNER", "right": "encounters AS e", "on": "e.\"Visit Record Number\" = tb.\"Visit Reference\"", "using": []}, {"type": "INNER", "right": "patients AS p", "on": "e.\"Patient Reference Number\" = p.\"Patient number\"", "using": []}] | [] |
| B2 | [{"alias": "joined", "kind": "derived", "block": "B1", "base_tables": ["encounters", "patients", "treatmentbasics", "treatmentoutcomes"]}] | [] | ["age_group", "\"Financial stress\""] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B2 | COUNT(*) | [] | [] | True |


## S31

类别 `data`；来源 `query_db`；调用 `87e8d33d43054339b7aab24eddad2845`；状态 `success`。

```sql
WITH joined AS (
  SELECT p.Age,
    CASE WHEN p.Age BETWEEN 18 AND 44 THEN 'young_18-44'
         WHEN p.Age BETWEEN 45 AND 59 THEN 'middle_45-59'
         ELSE 'older_60+' END AS age_group,
    p."Stigma effect", p."Housing stability", p."Insurance status",
    p."Employment status", p."Living situation", p."Disability status", p."Education level", p."Marital Status"
  FROM treatmentoutcomes o
  JOIN treatmentbasics tb ON tb."Treatment ID" = o."Treatment reference"
  JOIN encounters e ON e."Visit Record Number" = tb."Visit Reference"
  JOIN patients p ON e."Patient Reference Number" = p."Patient number"
)
SELECT age_group, "Stigma effect", COUNT(*) n FROM joined GROUP BY age_group, "Stigma effect" ORDER BY age_group, n DESC
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-042/attempt-01/sql/S31.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-042/attempt-01/sql/S31.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-042/attempt-01/results/S31.rows.jsonl)；完整：True；SHA256：`5a4f6cce8e1bd195549cb1e27ba63422bd4b3d789dfe11a244ee51203f2f8831`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "o", "kind": "base", "block": null, "base_tables": ["treatmentoutcomes"]}, {"alias": "tb", "kind": "base", "block": null, "base_tables": ["treatmentbasics"]}, {"alias": "e", "kind": "base", "block": null, "base_tables": ["encounters"]}, {"alias": "p", "kind": "base", "block": null, "base_tables": ["patients"]}] | [{"type": "INNER", "right": "treatmentbasics AS tb", "on": "tb.\"Treatment ID\" = o.\"Treatment reference\"", "using": []}, {"type": "INNER", "right": "encounters AS e", "on": "e.\"Visit Record Number\" = tb.\"Visit Reference\"", "using": []}, {"type": "INNER", "right": "patients AS p", "on": "e.\"Patient Reference Number\" = p.\"Patient number\"", "using": []}] | [] |
| B2 | [{"alias": "joined", "kind": "derived", "block": "B1", "base_tables": ["encounters", "patients", "treatmentbasics", "treatmentoutcomes"]}] | [] | ["age_group", "\"Stigma effect\""] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B2 | COUNT(*) | [] | [] | True |


## S32

类别 `data`；来源 `query_db`；调用 `4e53fc97545c4112b23ec72b8d01c705`；状态 `success`。

```sql
WITH joined AS (
  SELECT p.Age,
    CASE WHEN p.Age BETWEEN 18 AND 44 THEN 'young_18-44'
         WHEN p.Age BETWEEN 45 AND 59 THEN 'middle_45-59'
         ELSE 'older_60+' END AS age_group,
    p."Housing stability"
  FROM treatmentoutcomes o
  JOIN treatmentbasics tb ON tb."Treatment ID" = o."Treatment reference"
  JOIN encounters e ON e."Visit Record Number" = tb."Visit Reference"
  JOIN patients p ON e."Patient Reference Number" = p."Patient number"
)
SELECT age_group, "Housing stability", COUNT(*) n FROM joined GROUP BY age_group, "Housing stability" ORDER BY age_group, n DESC
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-042/attempt-01/sql/S32.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-042/attempt-01/sql/S32.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-042/attempt-01/results/S32.rows.jsonl)；完整：True；SHA256：`ed4c4ea412022222bbba9a70a4ebfa551b93234886072bdd80d62d70d276dc46`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "o", "kind": "base", "block": null, "base_tables": ["treatmentoutcomes"]}, {"alias": "tb", "kind": "base", "block": null, "base_tables": ["treatmentbasics"]}, {"alias": "e", "kind": "base", "block": null, "base_tables": ["encounters"]}, {"alias": "p", "kind": "base", "block": null, "base_tables": ["patients"]}] | [{"type": "INNER", "right": "treatmentbasics AS tb", "on": "tb.\"Treatment ID\" = o.\"Treatment reference\"", "using": []}, {"type": "INNER", "right": "encounters AS e", "on": "e.\"Visit Record Number\" = tb.\"Visit Reference\"", "using": []}, {"type": "INNER", "right": "patients AS p", "on": "e.\"Patient Reference Number\" = p.\"Patient number\"", "using": []}] | [] |
| B2 | [{"alias": "joined", "kind": "derived", "block": "B1", "base_tables": ["encounters", "patients", "treatmentbasics", "treatmentoutcomes"]}] | [] | ["age_group", "\"Housing stability\""] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B2 | COUNT(*) | [] | [] | True |


## S33

类别 `data`；来源 `query_db`；调用 `cb34e77149cc4366a70e46810a797cf9`；状态 `success`。

```sql
WITH joined AS (
  SELECT p.Age,
    CASE WHEN p.Age BETWEEN 18 AND 44 THEN 'young_18-44'
         WHEN p.Age BETWEEN 45 AND 59 THEN 'middle_45-59'
         ELSE 'older_60+' END AS age_group,
    p."Employment status", p."Insurance status"
  FROM treatmentoutcomes o
  JOIN treatmentbasics tb ON tb."Treatment ID" = o."Treatment reference"
  JOIN encounters e ON e."Visit Record Number" = tb."Visit Reference"
  JOIN patients p ON e."Patient Reference Number" = p."Patient number"
)
SELECT age_group, "Employment status", COUNT(*) n FROM joined GROUP BY age_group, "Employment status" ORDER BY age_group, n DESC
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-042/attempt-01/sql/S33.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-042/attempt-01/sql/S33.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-042/attempt-01/results/S33.rows.jsonl)；完整：True；SHA256：`8ff7fef06a5e5104946868695aad04000dfafd0136f434cdcddbb60ab680ffc8`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "o", "kind": "base", "block": null, "base_tables": ["treatmentoutcomes"]}, {"alias": "tb", "kind": "base", "block": null, "base_tables": ["treatmentbasics"]}, {"alias": "e", "kind": "base", "block": null, "base_tables": ["encounters"]}, {"alias": "p", "kind": "base", "block": null, "base_tables": ["patients"]}] | [{"type": "INNER", "right": "treatmentbasics AS tb", "on": "tb.\"Treatment ID\" = o.\"Treatment reference\"", "using": []}, {"type": "INNER", "right": "encounters AS e", "on": "e.\"Visit Record Number\" = tb.\"Visit Reference\"", "using": []}, {"type": "INNER", "right": "patients AS p", "on": "e.\"Patient Reference Number\" = p.\"Patient number\"", "using": []}] | [] |
| B2 | [{"alias": "joined", "kind": "derived", "block": "B1", "base_tables": ["encounters", "patients", "treatmentbasics", "treatmentoutcomes"]}] | [] | ["age_group", "\"Employment status\""] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B2 | COUNT(*) | [] | [] | True |


## S34

类别 `data`；来源 `query_db`；调用 `e2f0c430639d43529efb762f7a57e62e`；状态 `success`。

```sql
WITH joined AS (
  SELECT p.Age,
    CASE WHEN p.Age BETWEEN 18 AND 44 THEN 'young_18-44'
         WHEN p.Age BETWEEN 45 AND 59 THEN 'middle_45-59'
         ELSE 'older_60+' END AS age_group,
    p."Insurance status"
  FROM treatmentoutcomes o
  JOIN treatmentbasics tb ON tb."Treatment ID" = o."Treatment reference"
  JOIN encounters e ON e."Visit Record Number" = tb."Visit Reference"
  JOIN patients p ON e."Patient Reference Number" = p."Patient number"
)
SELECT age_group, "Insurance status", COUNT(*) n FROM joined GROUP BY age_group, "Insurance status" ORDER BY age_group, n DESC
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-042/attempt-01/sql/S34.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-042/attempt-01/sql/S34.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-042/attempt-01/results/S34.rows.jsonl)；完整：True；SHA256：`1bd2ceb5d0ca116caaaa5f7f0532fe6a5cc3d3c789f7b1b73ad11c47465537da`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "o", "kind": "base", "block": null, "base_tables": ["treatmentoutcomes"]}, {"alias": "tb", "kind": "base", "block": null, "base_tables": ["treatmentbasics"]}, {"alias": "e", "kind": "base", "block": null, "base_tables": ["encounters"]}, {"alias": "p", "kind": "base", "block": null, "base_tables": ["patients"]}] | [{"type": "INNER", "right": "treatmentbasics AS tb", "on": "tb.\"Treatment ID\" = o.\"Treatment reference\"", "using": []}, {"type": "INNER", "right": "encounters AS e", "on": "e.\"Visit Record Number\" = tb.\"Visit Reference\"", "using": []}, {"type": "INNER", "right": "patients AS p", "on": "e.\"Patient Reference Number\" = p.\"Patient number\"", "using": []}] | [] |
| B2 | [{"alias": "joined", "kind": "derived", "block": "B1", "base_tables": ["encounters", "patients", "treatmentbasics", "treatmentoutcomes"]}] | [] | ["age_group", "\"Insurance status\""] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B2 | COUNT(*) | [] | [] | True |


## S35

类别 `data`；来源 `python`；调用 `813dbdf363c6480490d4cb67cabf5004`；状态 `success`。

```sql

SELECT
  CASE WHEN p.Age BETWEEN 18 AND 44 THEN 'young_18-44'
       WHEN p.Age BETWEEN 45 AND 59 THEN 'middle_45-59'
       ELSE 'older_60+' END AS age_group,
  e."Treatment Barriers" AS barrier,
  COUNT(*) AS n
FROM treatmentoutcomes o
JOIN treatmentbasics tb ON tb."Treatment ID" = o."Treatment reference"
JOIN encounters e ON e."Visit Record Number" = tb."Visit Reference"
JOIN patients p ON e."Patient Reference Number" = p."Patient number"
GROUP BY age_group, barrier
ORDER BY age_group, barrier

```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-042/attempt-01/sql/S35.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-042/attempt-01/sql/S35.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-042/attempt-01/results/S35.rows.jsonl)；完整：True；SHA256：`96bbfc0519249e5ade2e77b298c822bfd0b8b070c97b3c1fbc912ececde13b99`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "o", "kind": "base", "block": null, "base_tables": ["treatmentoutcomes"]}, {"alias": "tb", "kind": "base", "block": null, "base_tables": ["treatmentbasics"]}, {"alias": "e", "kind": "base", "block": null, "base_tables": ["encounters"]}, {"alias": "p", "kind": "base", "block": null, "base_tables": ["patients"]}] | [{"type": "INNER", "right": "treatmentbasics AS tb", "on": "tb.\"Treatment ID\" = o.\"Treatment reference\"", "using": []}, {"type": "INNER", "right": "encounters AS e", "on": "e.\"Visit Record Number\" = tb.\"Visit Reference\"", "using": []}, {"type": "INNER", "right": "patients AS p", "on": "e.\"Patient Reference Number\" = p.\"Patient number\"", "using": []}] | ["CASE WHEN p.Age BETWEEN 18 AND 44 THEN 'young_18-44' WHEN p.Age BETWEEN 45 AND 59 THEN 'middle_45-59' ELSE 'older_60+' END", "e.\"Treatment Barriers\""] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |


## S36

类别 `data`；来源 `python`；调用 `813dbdf363c6480490d4cb67cabf5004`；状态 `success`。

```sql

SELECT
  CASE WHEN p.Age BETWEEN 18 AND 44 THEN 'young_18-44'
       WHEN p.Age BETWEEN 45 AND 59 THEN 'middle_45-59'
       ELSE 'older_60+' END AS age_group,
  o."Symptom improvement" AS improvement,
  COUNT(*) AS n
FROM treatmentoutcomes o
JOIN treatmentbasics tb ON tb."Treatment ID" = o."Treatment reference"
JOIN encounters e ON e."Visit Record Number" = tb."Visit Reference"
JOIN patients p ON e."Patient Reference Number" = p."Patient number"
GROUP BY age_group, improvement
ORDER BY age_group, improvement

```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-042/attempt-01/sql/S36.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-042/attempt-01/sql/S36.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-042/attempt-01/results/S36.rows.jsonl)；完整：True；SHA256：`288170516a86f6bdd608ac663c73ca3b3477704300da0989e8cc53deec6fc53c`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "o", "kind": "base", "block": null, "base_tables": ["treatmentoutcomes"]}, {"alias": "tb", "kind": "base", "block": null, "base_tables": ["treatmentbasics"]}, {"alias": "e", "kind": "base", "block": null, "base_tables": ["encounters"]}, {"alias": "p", "kind": "base", "block": null, "base_tables": ["patients"]}] | [{"type": "INNER", "right": "treatmentbasics AS tb", "on": "tb.\"Treatment ID\" = o.\"Treatment reference\"", "using": []}, {"type": "INNER", "right": "encounters AS e", "on": "e.\"Visit Record Number\" = tb.\"Visit Reference\"", "using": []}, {"type": "INNER", "right": "patients AS p", "on": "e.\"Patient Reference Number\" = p.\"Patient number\"", "using": []}] | ["CASE WHEN p.Age BETWEEN 18 AND 44 THEN 'young_18-44' WHEN p.Age BETWEEN 45 AND 59 THEN 'middle_45-59' ELSE 'older_60+' END", "o.\"Symptom improvement\""] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |


## S37

类别 `data`；来源 `python`；调用 `813dbdf363c6480490d4cb67cabf5004`；状态 `success`。

```sql

SELECT
  CASE WHEN p.Age BETWEEN 18 AND 44 THEN 'young_18-44'
       WHEN p.Age BETWEEN 45 AND 59 THEN 'middle_45-59'
       ELSE 'older_60+' END AS age_group,
  e."Treatment Barriers" AS barrier,
  o."Symptom improvement" AS improvement,
  COUNT(*) AS n
FROM treatmentoutcomes o
JOIN treatmentbasics tb ON tb."Treatment ID" = o."Treatment reference"
JOIN encounters e ON e."Visit Record Number" = tb."Visit Reference"
JOIN patients p ON e."Patient Reference Number" = p."Patient number"
GROUP BY age_group, barrier, improvement
ORDER BY age_group, barrier, improvement

```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-042/attempt-01/sql/S37.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-042/attempt-01/sql/S37.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-042/attempt-01/results/S37.rows.jsonl)；完整：True；SHA256：`bee4062079a5742431f92e466b2f6b1eb301eed9f39afc9ce011dae0875bebe8`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "o", "kind": "base", "block": null, "base_tables": ["treatmentoutcomes"]}, {"alias": "tb", "kind": "base", "block": null, "base_tables": ["treatmentbasics"]}, {"alias": "e", "kind": "base", "block": null, "base_tables": ["encounters"]}, {"alias": "p", "kind": "base", "block": null, "base_tables": ["patients"]}] | [{"type": "INNER", "right": "treatmentbasics AS tb", "on": "tb.\"Treatment ID\" = o.\"Treatment reference\"", "using": []}, {"type": "INNER", "right": "encounters AS e", "on": "e.\"Visit Record Number\" = tb.\"Visit Reference\"", "using": []}, {"type": "INNER", "right": "patients AS p", "on": "e.\"Patient Reference Number\" = p.\"Patient number\"", "using": []}] | ["CASE WHEN p.Age BETWEEN 18 AND 44 THEN 'young_18-44' WHEN p.Age BETWEEN 45 AND 59 THEN 'middle_45-59' ELSE 'older_60+' END", "e.\"Treatment Barriers\"", "o.\"Symptom improvement\""] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |


## S38

类别 `data`；来源 `python`；调用 `0183a2d24c544e87bf19e09f2190504b`；状态 `success`。

```sql

SELECT
  CASE WHEN p.Age BETWEEN 18 AND 44 THEN 'Young Adults (18-44)'
       WHEN p.Age BETWEEN 45 AND 59 THEN 'Middle-aged (45-59)'
       ELSE 'Older Adults (60+)' END AS age_group,
  e."Treatment Barriers" AS barrier,
  COUNT(*) AS n
FROM treatmentoutcomes o
JOIN treatmentbasics tb ON tb."Treatment ID" = o."Treatment reference"
JOIN encounters e ON e."Visit Record Number" = tb."Visit Reference"
JOIN patients p ON e."Patient Reference Number" = p."Patient number"
GROUP BY age_group, barrier
ORDER BY age_group, barrier

```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-042/attempt-01/sql/S38.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-042/attempt-01/sql/S38.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-042/attempt-01/results/S38.rows.jsonl)；完整：True；SHA256：`06b3fa08b980f036d48a3fa1a897fced8d2c257aaeef3fe03598a57cd9a80a45`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "o", "kind": "base", "block": null, "base_tables": ["treatmentoutcomes"]}, {"alias": "tb", "kind": "base", "block": null, "base_tables": ["treatmentbasics"]}, {"alias": "e", "kind": "base", "block": null, "base_tables": ["encounters"]}, {"alias": "p", "kind": "base", "block": null, "base_tables": ["patients"]}] | [{"type": "INNER", "right": "treatmentbasics AS tb", "on": "tb.\"Treatment ID\" = o.\"Treatment reference\"", "using": []}, {"type": "INNER", "right": "encounters AS e", "on": "e.\"Visit Record Number\" = tb.\"Visit Reference\"", "using": []}, {"type": "INNER", "right": "patients AS p", "on": "e.\"Patient Reference Number\" = p.\"Patient number\"", "using": []}] | ["CASE WHEN p.Age BETWEEN 18 AND 44 THEN 'Young Adults (18-44)' WHEN p.Age BETWEEN 45 AND 59 THEN 'Middle-aged (45-59)' ELSE 'Older Adults (60+)' END", "e.\"Treatment Barriers\""] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |


## S39

类别 `data`；来源 `python`；调用 `0183a2d24c544e87bf19e09f2190504b`；状态 `success`。

```sql

SELECT
  CASE WHEN p.Age BETWEEN 18 AND 44 THEN 'Young Adults (18-44)'
       WHEN p.Age BETWEEN 45 AND 59 THEN 'Middle-aged (45-59)'
       ELSE 'Older Adults (60+)' END AS age_group,
  o."Symptom improvement" AS improvement,
  COUNT(*) AS n
FROM treatmentoutcomes o
JOIN treatmentbasics tb ON tb."Treatment ID" = o."Treatment reference"
JOIN encounters e ON e."Visit Record Number" = tb."Visit Reference"
JOIN patients p ON e."Patient Reference Number" = p."Patient number"
GROUP BY age_group, improvement
ORDER BY age_group, improvement

```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-042/attempt-01/sql/S39.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-042/attempt-01/sql/S39.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-042/attempt-01/results/S39.rows.jsonl)；完整：True；SHA256：`7890c2778b44c3806d163dd5bdc82a91b213fa8a87ff5a7b51c90fb4bccf203a`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "o", "kind": "base", "block": null, "base_tables": ["treatmentoutcomes"]}, {"alias": "tb", "kind": "base", "block": null, "base_tables": ["treatmentbasics"]}, {"alias": "e", "kind": "base", "block": null, "base_tables": ["encounters"]}, {"alias": "p", "kind": "base", "block": null, "base_tables": ["patients"]}] | [{"type": "INNER", "right": "treatmentbasics AS tb", "on": "tb.\"Treatment ID\" = o.\"Treatment reference\"", "using": []}, {"type": "INNER", "right": "encounters AS e", "on": "e.\"Visit Record Number\" = tb.\"Visit Reference\"", "using": []}, {"type": "INNER", "right": "patients AS p", "on": "e.\"Patient Reference Number\" = p.\"Patient number\"", "using": []}] | ["CASE WHEN p.Age BETWEEN 18 AND 44 THEN 'Young Adults (18-44)' WHEN p.Age BETWEEN 45 AND 59 THEN 'Middle-aged (45-59)' ELSE 'Older Adults (60+)' END", "o.\"Symptom improvement\""] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |


## S40

类别 `data`；来源 `python`；调用 `0183a2d24c544e87bf19e09f2190504b`；状态 `success`。

```sql

SELECT
  CASE WHEN p.Age BETWEEN 18 AND 44 THEN 'Young Adults (18-44)'
       WHEN p.Age BETWEEN 45 AND 59 THEN 'Middle-aged (45-59)'
       ELSE 'Older Adults (60+)' END AS age_group,
  e."Treatment Barriers" AS barrier,
  o."Symptom improvement" AS improvement,
  COUNT(*) AS n
FROM treatmentoutcomes o
JOIN treatmentbasics tb ON tb."Treatment ID" = o."Treatment reference"
JOIN encounters e ON e."Visit Record Number" = tb."Visit Reference"
JOIN patients p ON e."Patient Reference Number" = p."Patient number"
GROUP BY age_group, barrier, improvement
ORDER BY age_group, barrier, improvement

```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-042/attempt-01/sql/S40.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-042/attempt-01/sql/S40.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-042/attempt-01/results/S40.rows.jsonl)；完整：True；SHA256：`2155c7cbfd899ca7a0fb53315157215a9f79e310ca3820ecd71194f48a367905`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "o", "kind": "base", "block": null, "base_tables": ["treatmentoutcomes"]}, {"alias": "tb", "kind": "base", "block": null, "base_tables": ["treatmentbasics"]}, {"alias": "e", "kind": "base", "block": null, "base_tables": ["encounters"]}, {"alias": "p", "kind": "base", "block": null, "base_tables": ["patients"]}] | [{"type": "INNER", "right": "treatmentbasics AS tb", "on": "tb.\"Treatment ID\" = o.\"Treatment reference\"", "using": []}, {"type": "INNER", "right": "encounters AS e", "on": "e.\"Visit Record Number\" = tb.\"Visit Reference\"", "using": []}, {"type": "INNER", "right": "patients AS p", "on": "e.\"Patient Reference Number\" = p.\"Patient number\"", "using": []}] | ["CASE WHEN p.Age BETWEEN 18 AND 44 THEN 'Young Adults (18-44)' WHEN p.Age BETWEEN 45 AND 59 THEN 'Middle-aged (45-59)' ELSE 'Older Adults (60+)' END", "e.\"Treatment Barriers\"", "o.\"Symptom improvement\""] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |


## S41

类别 `data`；来源 `python`；调用 `0183a2d24c544e87bf19e09f2190504b`；状态 `success`。

```sql

SELECT
  CASE WHEN p.Age BETWEEN 18 AND 44 THEN 'Young Adults (18-44)'
       WHEN p.Age BETWEEN 45 AND 59 THEN 'Middle-aged (45-59)'
       ELSE 'Older Adults (60+)' END AS age_group,
  p."Financial stress" AS val,
  COUNT(*) AS n
FROM treatmentoutcomes o
JOIN treatmentbasics tb ON tb."Treatment ID" = o."Treatment reference"
JOIN encounters e ON e."Visit Record Number" = tb."Visit Reference"
JOIN patients p ON e."Patient Reference Number" = p."Patient number"
GROUP BY age_group, val
ORDER BY age_group, val

```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-042/attempt-01/sql/S41.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-042/attempt-01/sql/S41.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-042/attempt-01/results/S41.rows.jsonl)；完整：True；SHA256：`b3078e54884fccee7892267c25a8d10bb11381dfff06938551d8b328188950bf`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "o", "kind": "base", "block": null, "base_tables": ["treatmentoutcomes"]}, {"alias": "tb", "kind": "base", "block": null, "base_tables": ["treatmentbasics"]}, {"alias": "e", "kind": "base", "block": null, "base_tables": ["encounters"]}, {"alias": "p", "kind": "base", "block": null, "base_tables": ["patients"]}] | [{"type": "INNER", "right": "treatmentbasics AS tb", "on": "tb.\"Treatment ID\" = o.\"Treatment reference\"", "using": []}, {"type": "INNER", "right": "encounters AS e", "on": "e.\"Visit Record Number\" = tb.\"Visit Reference\"", "using": []}, {"type": "INNER", "right": "patients AS p", "on": "e.\"Patient Reference Number\" = p.\"Patient number\"", "using": []}] | ["CASE WHEN p.Age BETWEEN 18 AND 44 THEN 'Young Adults (18-44)' WHEN p.Age BETWEEN 45 AND 59 THEN 'Middle-aged (45-59)' ELSE 'Older Adults (60+)' END", "p.\"Financial stress\""] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |


## S42

类别 `data`；来源 `python`；调用 `0183a2d24c544e87bf19e09f2190504b`；状态 `success`。

```sql

SELECT
  CASE WHEN p.Age BETWEEN 18 AND 44 THEN 'Young Adults (18-44)'
       WHEN p.Age BETWEEN 45 AND 59 THEN 'Middle-aged (45-59)'
       ELSE 'Older Adults (60+)' END AS age_group,
  p."Stigma effect" AS val,
  COUNT(*) AS n
FROM treatmentoutcomes o
JOIN treatmentbasics tb ON tb."Treatment ID" = o."Treatment reference"
JOIN encounters e ON e."Visit Record Number" = tb."Visit Reference"
JOIN patients p ON e."Patient Reference Number" = p."Patient number"
GROUP BY age_group, val
ORDER BY age_group, val

```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-042/attempt-01/sql/S42.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-042/attempt-01/sql/S42.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-042/attempt-01/results/S42.rows.jsonl)；完整：True；SHA256：`24b871f44536001c50b08def9bfd9c16816381e59403325b0e86a074d26b572b`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "o", "kind": "base", "block": null, "base_tables": ["treatmentoutcomes"]}, {"alias": "tb", "kind": "base", "block": null, "base_tables": ["treatmentbasics"]}, {"alias": "e", "kind": "base", "block": null, "base_tables": ["encounters"]}, {"alias": "p", "kind": "base", "block": null, "base_tables": ["patients"]}] | [{"type": "INNER", "right": "treatmentbasics AS tb", "on": "tb.\"Treatment ID\" = o.\"Treatment reference\"", "using": []}, {"type": "INNER", "right": "encounters AS e", "on": "e.\"Visit Record Number\" = tb.\"Visit Reference\"", "using": []}, {"type": "INNER", "right": "patients AS p", "on": "e.\"Patient Reference Number\" = p.\"Patient number\"", "using": []}] | ["CASE WHEN p.Age BETWEEN 18 AND 44 THEN 'Young Adults (18-44)' WHEN p.Age BETWEEN 45 AND 59 THEN 'Middle-aged (45-59)' ELSE 'Older Adults (60+)' END", "p.\"Stigma effect\""] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |


## S43

类别 `data`；来源 `python`；调用 `0183a2d24c544e87bf19e09f2190504b`；状态 `success`。

```sql

SELECT
  CASE WHEN p.Age BETWEEN 18 AND 44 THEN 'Young Adults (18-44)'
       WHEN p.Age BETWEEN 45 AND 59 THEN 'Middle-aged (45-59)'
       ELSE 'Older Adults (60+)' END AS age_group,
  p."Housing stability" AS val,
  COUNT(*) AS n
FROM treatmentoutcomes o
JOIN treatmentbasics tb ON tb."Treatment ID" = o."Treatment reference"
JOIN encounters e ON e."Visit Record Number" = tb."Visit Reference"
JOIN patients p ON e."Patient Reference Number" = p."Patient number"
GROUP BY age_group, val
ORDER BY age_group, val

```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-042/attempt-01/sql/S43.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-042/attempt-01/sql/S43.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-042/attempt-01/results/S43.rows.jsonl)；完整：True；SHA256：`5bac1003975a94997ef02514a2103c7c43c3ca1d94f738de069d34b614a7d57e`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "o", "kind": "base", "block": null, "base_tables": ["treatmentoutcomes"]}, {"alias": "tb", "kind": "base", "block": null, "base_tables": ["treatmentbasics"]}, {"alias": "e", "kind": "base", "block": null, "base_tables": ["encounters"]}, {"alias": "p", "kind": "base", "block": null, "base_tables": ["patients"]}] | [{"type": "INNER", "right": "treatmentbasics AS tb", "on": "tb.\"Treatment ID\" = o.\"Treatment reference\"", "using": []}, {"type": "INNER", "right": "encounters AS e", "on": "e.\"Visit Record Number\" = tb.\"Visit Reference\"", "using": []}, {"type": "INNER", "right": "patients AS p", "on": "e.\"Patient Reference Number\" = p.\"Patient number\"", "using": []}] | ["CASE WHEN p.Age BETWEEN 18 AND 44 THEN 'Young Adults (18-44)' WHEN p.Age BETWEEN 45 AND 59 THEN 'Middle-aged (45-59)' ELSE 'Older Adults (60+)' END", "p.\"Housing stability\""] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |


## S44

类别 `data`；来源 `python`；调用 `0183a2d24c544e87bf19e09f2190504b`；状态 `success`。

```sql

SELECT
  CASE WHEN p.Age BETWEEN 18 AND 44 THEN 'Young Adults (18-44)'
       WHEN p.Age BETWEEN 45 AND 59 THEN 'Middle-aged (45-59)'
       ELSE 'Older Adults (60+)' END AS age_group,
  p."Employment status" AS val,
  COUNT(*) AS n
FROM treatmentoutcomes o
JOIN treatmentbasics tb ON tb."Treatment ID" = o."Treatment reference"
JOIN encounters e ON e."Visit Record Number" = tb."Visit Reference"
JOIN patients p ON e."Patient Reference Number" = p."Patient number"
GROUP BY age_group, val
ORDER BY age_group, val

```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-042/attempt-01/sql/S44.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-042/attempt-01/sql/S44.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-042/attempt-01/results/S44.rows.jsonl)；完整：True；SHA256：`a66a53da974899af933f19eab3dcb073d73df16b6eb759cc6ee8d998f3af9643`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "o", "kind": "base", "block": null, "base_tables": ["treatmentoutcomes"]}, {"alias": "tb", "kind": "base", "block": null, "base_tables": ["treatmentbasics"]}, {"alias": "e", "kind": "base", "block": null, "base_tables": ["encounters"]}, {"alias": "p", "kind": "base", "block": null, "base_tables": ["patients"]}] | [{"type": "INNER", "right": "treatmentbasics AS tb", "on": "tb.\"Treatment ID\" = o.\"Treatment reference\"", "using": []}, {"type": "INNER", "right": "encounters AS e", "on": "e.\"Visit Record Number\" = tb.\"Visit Reference\"", "using": []}, {"type": "INNER", "right": "patients AS p", "on": "e.\"Patient Reference Number\" = p.\"Patient number\"", "using": []}] | ["CASE WHEN p.Age BETWEEN 18 AND 44 THEN 'Young Adults (18-44)' WHEN p.Age BETWEEN 45 AND 59 THEN 'Middle-aged (45-59)' ELSE 'Older Adults (60+)' END", "p.\"Employment status\""] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |


## S45

类别 `data`；来源 `python`；调用 `0183a2d24c544e87bf19e09f2190504b`；状态 `success`。

```sql

SELECT
  CASE WHEN p.Age BETWEEN 18 AND 44 THEN 'Young Adults (18-44)'
       WHEN p.Age BETWEEN 45 AND 59 THEN 'Middle-aged (45-59)'
       ELSE 'Older Adults (60+)' END AS age_group,
  p."Insurance status" AS val,
  COUNT(*) AS n
FROM treatmentoutcomes o
JOIN treatmentbasics tb ON tb."Treatment ID" = o."Treatment reference"
JOIN encounters e ON e."Visit Record Number" = tb."Visit Reference"
JOIN patients p ON e."Patient Reference Number" = p."Patient number"
GROUP BY age_group, val
ORDER BY age_group, val

```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-042/attempt-01/sql/S45.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-042/attempt-01/sql/S45.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-042/attempt-01/results/S45.rows.jsonl)；完整：True；SHA256：`868685358c883c1457ac8dfeee62f54d338a6029505df56e8a265c23c560fec5`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "o", "kind": "base", "block": null, "base_tables": ["treatmentoutcomes"]}, {"alias": "tb", "kind": "base", "block": null, "base_tables": ["treatmentbasics"]}, {"alias": "e", "kind": "base", "block": null, "base_tables": ["encounters"]}, {"alias": "p", "kind": "base", "block": null, "base_tables": ["patients"]}] | [{"type": "INNER", "right": "treatmentbasics AS tb", "on": "tb.\"Treatment ID\" = o.\"Treatment reference\"", "using": []}, {"type": "INNER", "right": "encounters AS e", "on": "e.\"Visit Record Number\" = tb.\"Visit Reference\"", "using": []}, {"type": "INNER", "right": "patients AS p", "on": "e.\"Patient Reference Number\" = p.\"Patient number\"", "using": []}] | ["CASE WHEN p.Age BETWEEN 18 AND 44 THEN 'Young Adults (18-44)' WHEN p.Age BETWEEN 45 AND 59 THEN 'Middle-aged (45-59)' ELSE 'Older Adults (60+)' END", "p.\"Insurance status\""] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |


## S46

类别 `data`；来源 `python`；调用 `0183a2d24c544e87bf19e09f2190504b`；状态 `success`。

```sql

SELECT
  CASE WHEN p.Age BETWEEN 18 AND 44 THEN 'Young Adults (18-44)'
       WHEN p.Age BETWEEN 45 AND 59 THEN 'Middle-aged (45-59)'
       ELSE 'Older Adults (60+)' END AS age_group,
  o."Treatment adherence" AS val,
  COUNT(*) AS n
FROM treatmentoutcomes o
JOIN treatmentbasics tb ON tb."Treatment ID" = o."Treatment reference"
JOIN encounters e ON e."Visit Record Number" = tb."Visit Reference"
JOIN patients p ON e."Patient Reference Number" = p."Patient number"
GROUP BY age_group, val
ORDER BY age_group, val

```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-042/attempt-01/sql/S46.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-042/attempt-01/sql/S46.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-042/attempt-01/results/S46.rows.jsonl)；完整：True；SHA256：`b1a12ecd3979a61fdaf66ca90c1543b70de9f836ddc51dbb844698c7862c92cb`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "o", "kind": "base", "block": null, "base_tables": ["treatmentoutcomes"]}, {"alias": "tb", "kind": "base", "block": null, "base_tables": ["treatmentbasics"]}, {"alias": "e", "kind": "base", "block": null, "base_tables": ["encounters"]}, {"alias": "p", "kind": "base", "block": null, "base_tables": ["patients"]}] | [{"type": "INNER", "right": "treatmentbasics AS tb", "on": "tb.\"Treatment ID\" = o.\"Treatment reference\"", "using": []}, {"type": "INNER", "right": "encounters AS e", "on": "e.\"Visit Record Number\" = tb.\"Visit Reference\"", "using": []}, {"type": "INNER", "right": "patients AS p", "on": "e.\"Patient Reference Number\" = p.\"Patient number\"", "using": []}] | ["CASE WHEN p.Age BETWEEN 18 AND 44 THEN 'Young Adults (18-44)' WHEN p.Age BETWEEN 45 AND 59 THEN 'Middle-aged (45-59)' ELSE 'Older Adults (60+)' END", "o.\"Treatment adherence\""] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |


## S47

类别 `data`；来源 `python`；调用 `537414f566614bd384f1df0a3a8777e7`；状态 `success`。

```sql

SELECT
  CASE WHEN p.Age BETWEEN 18 AND 44 THEN 'young'
       WHEN p.Age BETWEEN 45 AND 59 THEN 'middle'
       ELSE 'older' END AS age_group,
  e."Treatment Barriers" AS barrier,
  o."Symptom improvement" AS improvement,
  o."Treatment adherence" AS adherence,
  e."Missed Appointment" AS missed
FROM treatmentoutcomes o
JOIN treatmentbasics tb ON tb."Treatment ID" = o."Treatment reference"
JOIN encounters e ON e."Visit Record Number" = tb."Visit Reference"
JOIN patients p ON e."Patient Reference Number" = p."Patient number"

```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-042/attempt-01/sql/S47.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-042/attempt-01/sql/S47.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-042/attempt-01/results/S47.rows.jsonl)；完整：True；SHA256：`1c583333aaf41fdc1ceab8feb2df03b58af5b18f6ed39a35d223b82f1765c1de`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "o", "kind": "base", "block": null, "base_tables": ["treatmentoutcomes"]}, {"alias": "tb", "kind": "base", "block": null, "base_tables": ["treatmentbasics"]}, {"alias": "e", "kind": "base", "block": null, "base_tables": ["encounters"]}, {"alias": "p", "kind": "base", "block": null, "base_tables": ["patients"]}] | [{"type": "INNER", "right": "treatmentbasics AS tb", "on": "tb.\"Treatment ID\" = o.\"Treatment reference\"", "using": []}, {"type": "INNER", "right": "encounters AS e", "on": "e.\"Visit Record Number\" = tb.\"Visit Reference\"", "using": []}, {"type": "INNER", "right": "patients AS p", "on": "e.\"Patient Reference Number\" = p.\"Patient number\"", "using": []}] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |


## S48

类别 `data`；来源 `python`；调用 `6e5b04e34d4a47199069391d76fa0c80`；状态 `success`。

```sql

SELECT
  CASE WHEN p.Age BETWEEN 18 AND 44 THEN 'Young (18-44)'
       WHEN p.Age BETWEEN 45 AND 59 THEN 'Middle (45-59)'
       ELSE 'Older (60+)' END AS age_group,
  e."Treatment Barriers" AS barrier,
  o."Symptom improvement" AS improvement,
  o."Treatment adherence" AS adherence,
  o."Treatment response" AS response,
  o."Treatment engagement" AS engagement,
  o."Satisfaction Rating" AS satisfaction,
  e."Missed Appointment" AS missed
FROM treatmentoutcomes o
JOIN treatmentbasics tb ON tb."Treatment ID" = o."Treatment reference"
JOIN encounters e ON e."Visit Record Number" = tb."Visit Reference"
JOIN patients p ON e."Patient Reference Number" = p."Patient number"

```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-042/attempt-01/sql/S48.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-042/attempt-01/sql/S48.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-042/attempt-01/results/S48.rows.jsonl)；完整：True；SHA256：`98e5494d1ea46f52fdbd6792ea8977ce14d7e876b21f6c05077c7fe0bbf9c6c9`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "o", "kind": "base", "block": null, "base_tables": ["treatmentoutcomes"]}, {"alias": "tb", "kind": "base", "block": null, "base_tables": ["treatmentbasics"]}, {"alias": "e", "kind": "base", "block": null, "base_tables": ["encounters"]}, {"alias": "p", "kind": "base", "block": null, "base_tables": ["patients"]}] | [{"type": "INNER", "right": "treatmentbasics AS tb", "on": "tb.\"Treatment ID\" = o.\"Treatment reference\"", "using": []}, {"type": "INNER", "right": "encounters AS e", "on": "e.\"Visit Record Number\" = tb.\"Visit Reference\"", "using": []}, {"type": "INNER", "right": "patients AS p", "on": "e.\"Patient Reference Number\" = p.\"Patient number\"", "using": []}] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |


## S49

类别 `data`；来源 `python`；调用 `3945fc24592d4f21bd55478648f1a2d9`；状态 `success`。

```sql

SELECT
  CASE WHEN p.Age BETWEEN 18 AND 44 THEN 'Young (18-44)'
       WHEN p.Age BETWEEN 45 AND 59 THEN 'Middle (45-59)'
       ELSE 'Older (60+)' END AS age_group,
  e."Treatment Barriers" AS barrier,
  o."Symptom improvement" AS improvement,
  o."Treatment adherence" AS adherence,
  o."Satisfaction Rating" AS satisfaction
FROM treatmentoutcomes o
JOIN treatmentbasics tb ON tb."Treatment ID" = o."Treatment reference"
JOIN encounters e ON e."Visit Record Number" = tb."Visit Reference"
JOIN patients p ON e."Patient Reference Number" = p."Patient number"

```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-042/attempt-01/sql/S49.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-042/attempt-01/sql/S49.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-042/attempt-01/results/S49.rows.jsonl)；完整：True；SHA256：`d623f10bfbaa7441e5fae382c87d15de343dfee831041278e14ccf7d32a00d1a`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "o", "kind": "base", "block": null, "base_tables": ["treatmentoutcomes"]}, {"alias": "tb", "kind": "base", "block": null, "base_tables": ["treatmentbasics"]}, {"alias": "e", "kind": "base", "block": null, "base_tables": ["encounters"]}, {"alias": "p", "kind": "base", "block": null, "base_tables": ["patients"]}] | [{"type": "INNER", "right": "treatmentbasics AS tb", "on": "tb.\"Treatment ID\" = o.\"Treatment reference\"", "using": []}, {"type": "INNER", "right": "encounters AS e", "on": "e.\"Visit Record Number\" = tb.\"Visit Reference\"", "using": []}, {"type": "INNER", "right": "patients AS p", "on": "e.\"Patient Reference Number\" = p.\"Patient number\"", "using": []}] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |


## S50

类别 `data`；来源 `query_db`；调用 `d73b8d416f7543149a3e407854d1ff1d`；状态 `success`。

```sql
SELECT
  CASE WHEN p.Age BETWEEN 18 AND 44 THEN 'young_18-44'
       WHEN p.Age BETWEEN 45 AND 59 THEN 'middle_45-59'
       ELSE 'older_60+' END AS age_group,
  d."Primary Diagnosis" AS diagnosis,
  COUNT(*) AS n
FROM assessmentsocialanddiagnosis d
JOIN assessmentbasics a ON a."Assessment ID" = d."Social Diagnosis Assessment ID"
JOIN encounters e ON e."Assessment Reference" = a."Assessment ID"
JOIN patients p ON e."Patient Reference Number" = p."Patient number"
GROUP BY age_group, diagnosis
ORDER BY age_group, n DESC
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-042/attempt-01/sql/S50.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-042/attempt-01/sql/S50.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-042/attempt-01/results/S50.rows.jsonl)；完整：True；SHA256：`71d1173407b3e82cc2abd84939249b6243206223d212b89c0422d5f2e0368a59`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "d", "kind": "base", "block": null, "base_tables": ["assessmentsocialanddiagnosis"]}, {"alias": "a", "kind": "base", "block": null, "base_tables": ["assessmentbasics"]}, {"alias": "e", "kind": "base", "block": null, "base_tables": ["encounters"]}, {"alias": "p", "kind": "base", "block": null, "base_tables": ["patients"]}] | [{"type": "INNER", "right": "assessmentbasics AS a", "on": "a.\"Assessment ID\" = d.\"Social Diagnosis Assessment ID\"", "using": []}, {"type": "INNER", "right": "encounters AS e", "on": "e.\"Assessment Reference\" = a.\"Assessment ID\"", "using": []}, {"type": "INNER", "right": "patients AS p", "on": "e.\"Patient Reference Number\" = p.\"Patient number\"", "using": []}] | ["CASE WHEN p.Age BETWEEN 18 AND 44 THEN 'young_18-44' WHEN p.Age BETWEEN 45 AND 59 THEN 'middle_45-59' ELSE 'older_60+' END", "d.\"Primary Diagnosis\""] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |


## S51

类别 `data`；来源 `query_db`；调用 `7ba3613b845845cb996d5701509517ec`；状态 `success`。

```sql
SELECT DISTINCT "Primary Diagnosis" FROM assessmentsocialanddiagnosis
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-042/attempt-01/sql/S51.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-042/attempt-01/sql/S51.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-042/attempt-01/results/S51.rows.jsonl)；完整：True；SHA256：`16e489476c831c4d305ce523b36a484e32f5ce95b1e5ac1f6e4eebff2020667a`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "assessmentsocialanddiagnosis", "kind": "base", "block": null, "base_tables": ["assessmentsocialanddiagnosis"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |


## S52

类别 `data`；来源 `query_db`；调用 `2bd779a28f284fc6888089b6729a7558`；状态 `success`。

```sql
SELECT
  CASE WHEN p.Age BETWEEN 18 AND 44 THEN 'young_18-44'
       WHEN p.Age BETWEEN 45 AND 59 THEN 'middle_45-59'
       ELSE 'older_60+' END AS age_group,
  d."Primary Diagnosis" AS diagnosis,
  COUNT(*) AS n
FROM assessmentsocialanddiagnosis d
JOIN assessmentbasics a ON a."Assessment ID" = d."Social Diagnosis Assessment ID"
JOIN encounters e ON e."Assessment Reference" = a."Assessment ID"
JOIN patients p ON e."Patient Reference Number" = p."Patient number"
GROUP BY age_group, diagnosis
ORDER BY age_group, n DESC
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-042/attempt-01/sql/S52.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-042/attempt-01/sql/S52.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-042/attempt-01/results/S52.rows.jsonl)；完整：True；SHA256：`71d1173407b3e82cc2abd84939249b6243206223d212b89c0422d5f2e0368a59`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "d", "kind": "base", "block": null, "base_tables": ["assessmentsocialanddiagnosis"]}, {"alias": "a", "kind": "base", "block": null, "base_tables": ["assessmentbasics"]}, {"alias": "e", "kind": "base", "block": null, "base_tables": ["encounters"]}, {"alias": "p", "kind": "base", "block": null, "base_tables": ["patients"]}] | [{"type": "INNER", "right": "assessmentbasics AS a", "on": "a.\"Assessment ID\" = d.\"Social Diagnosis Assessment ID\"", "using": []}, {"type": "INNER", "right": "encounters AS e", "on": "e.\"Assessment Reference\" = a.\"Assessment ID\"", "using": []}, {"type": "INNER", "right": "patients AS p", "on": "e.\"Patient Reference Number\" = p.\"Patient number\"", "using": []}] | ["CASE WHEN p.Age BETWEEN 18 AND 44 THEN 'young_18-44' WHEN p.Age BETWEEN 45 AND 59 THEN 'middle_45-59' ELSE 'older_60+' END", "d.\"Primary Diagnosis\""] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |


## S53

类别 `data`；来源 `query_db`；调用 `673681659d954c46ba1d9838bae565e9`；状态 `success`。

```sql
WITH joined AS (
  SELECT p.Age,
    CASE WHEN p.Age BETWEEN 18 AND 44 THEN 'young_18-44'
         WHEN p.Age BETWEEN 45 AND 59 THEN 'middle_45-59'
         ELSE 'older_60+' END AS age_group,
    tb."Medication Adherence" AS med_adherence,
    tb."Medication Side Effects" AS side_effects
  FROM treatmentoutcomes o
  JOIN treatmentbasics tb ON tb."Treatment ID" = o."Treatment reference"
  JOIN encounters e ON e."Visit Record Number" = tb."Visit Reference"
  JOIN patients p ON e."Patient Reference Number" = p."Patient number"
)
SELECT age_group, "Medication Adherence", COUNT(*) n
FROM joined GROUP BY age_group, "Medication Adherence" ORDER BY age_group, n DESC
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-042/attempt-01/sql/S53.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-042/attempt-01/sql/S53.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-042/attempt-01/results/S53.rows.jsonl)；完整：True；SHA256：`7024241cd1612402653eeeb2ef636fa85338b52ee9641e59324d46f1a13895ae`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "o", "kind": "base", "block": null, "base_tables": ["treatmentoutcomes"]}, {"alias": "tb", "kind": "base", "block": null, "base_tables": ["treatmentbasics"]}, {"alias": "e", "kind": "base", "block": null, "base_tables": ["encounters"]}, {"alias": "p", "kind": "base", "block": null, "base_tables": ["patients"]}] | [{"type": "INNER", "right": "treatmentbasics AS tb", "on": "tb.\"Treatment ID\" = o.\"Treatment reference\"", "using": []}, {"type": "INNER", "right": "encounters AS e", "on": "e.\"Visit Record Number\" = tb.\"Visit Reference\"", "using": []}, {"type": "INNER", "right": "patients AS p", "on": "e.\"Patient Reference Number\" = p.\"Patient number\"", "using": []}] | [] |
| B2 | [{"alias": "joined", "kind": "derived", "block": "B1", "base_tables": ["encounters", "patients", "treatmentbasics", "treatmentoutcomes"]}] | [] | ["age_group", "\"Medication Adherence\""] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B2 | COUNT(*) | [] | [] | True |


未解析列血缘：[{"block": "B2", "column": "\"Medication Adherence\"", "reason": "ambiguous_or_missing_source"}, {"block": "B2", "column": "\"Medication Adherence\"", "reason": "ambiguous_or_missing_source"}, {"block": "B2", "column": "\"Medication Adherence\"", "reason": "ambiguous_or_missing_source"}]

## S54

类别 `data`；来源 `query_db`；调用 `b48167bcf97b4b109d0367807b26c617`；状态 `success`。

```sql
WITH joined AS (
  SELECT p.Age,
    CASE WHEN p.Age BETWEEN 18 AND 44 THEN 'young_18-44'
         WHEN p.Age BETWEEN 45 AND 59 THEN 'middle_45-59'
         ELSE 'older_60+' END AS age_group,
    tb."Medication Side Effects" AS side_effects
  FROM treatmentoutcomes o
  JOIN treatmentbasics tb ON tb."Treatment ID" = o."Treatment reference"
  JOIN encounters e ON e."Visit Record Number" = tb."Visit Reference"
  JOIN patients p ON e."Patient Reference Number" = p."Patient number"
)
SELECT age_group, "Medication Side Effects", COUNT(*) n
FROM joined GROUP BY age_group, "Medication Side Effects" ORDER BY age_group, n DESC
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-042/attempt-01/sql/S54.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-042/attempt-01/sql/S54.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-042/attempt-01/results/S54.rows.jsonl)；完整：True；SHA256：`4da1c66117fdcb55c30c6bb809b39f6952923630f741018a78c953e549382102`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "o", "kind": "base", "block": null, "base_tables": ["treatmentoutcomes"]}, {"alias": "tb", "kind": "base", "block": null, "base_tables": ["treatmentbasics"]}, {"alias": "e", "kind": "base", "block": null, "base_tables": ["encounters"]}, {"alias": "p", "kind": "base", "block": null, "base_tables": ["patients"]}] | [{"type": "INNER", "right": "treatmentbasics AS tb", "on": "tb.\"Treatment ID\" = o.\"Treatment reference\"", "using": []}, {"type": "INNER", "right": "encounters AS e", "on": "e.\"Visit Record Number\" = tb.\"Visit Reference\"", "using": []}, {"type": "INNER", "right": "patients AS p", "on": "e.\"Patient Reference Number\" = p.\"Patient number\"", "using": []}] | [] |
| B2 | [{"alias": "joined", "kind": "derived", "block": "B1", "base_tables": ["encounters", "patients", "treatmentbasics", "treatmentoutcomes"]}] | [] | ["age_group", "\"Medication Side Effects\""] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B2 | COUNT(*) | [] | [] | True |


未解析列血缘：[{"block": "B2", "column": "\"Medication Side Effects\"", "reason": "ambiguous_or_missing_source"}, {"block": "B2", "column": "\"Medication Side Effects\"", "reason": "ambiguous_or_missing_source"}, {"block": "B2", "column": "\"Medication Side Effects\"", "reason": "ambiguous_or_missing_source"}]

## S55

类别 `data`；来源 `query_db`；调用 `5f1119e163e7484aa57985403a4069f2`；状态 `success`。

```sql
SELECT DISTINCT "Medication Adherence" FROM treatmentbasics
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-042/attempt-01/sql/S55.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-042/attempt-01/sql/S55.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-042/attempt-01/results/S55.rows.jsonl)；完整：True；SHA256：`1c9d3c7009e34293d85dce390cca8a16814e005da01517f0318e12a05fa1befb`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "treatmentbasics", "kind": "base", "block": null, "base_tables": ["treatmentbasics"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |


## S56

类别 `data`；来源 `query_db`；调用 `1c359f2e912b4f70af291d7f89e74e95`；状态 `success`。

```sql
SELECT DISTINCT "Medication Side Effects" FROM treatmentbasics
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-042/attempt-01/sql/S56.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-042/attempt-01/sql/S56.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-042/attempt-01/results/S56.rows.jsonl)；完整：True；SHA256：`d509fd04e86af9bafca3c0aba9eca381000b83dd78cc05ca5a6526a6e8935eb5`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "treatmentbasics", "kind": "base", "block": null, "base_tables": ["treatmentbasics"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |


## S57

类别 `data`；来源 `query_db`；调用 `00b3193a42b641a9af9ca1939ac77013`；状态 `success`。

```sql
WITH joined AS (
  SELECT p.Age,
    CASE WHEN p.Age BETWEEN 18 AND 44 THEN 'young_18-44'
         WHEN p.Age BETWEEN 45 AND 59 THEN 'middle_45-59'
         ELSE 'older_60+' END AS age_group,
    tb."Medication Adherence" AS med_adh
  FROM treatmentoutcomes o
  JOIN treatmentbasics tb ON tb."Treatment ID" = o."Treatment reference"
  JOIN encounters e ON e."Visit Record Number" = tb."Visit Reference"
  JOIN patients p ON e."Patient Reference Number" = p."Patient number"
)
SELECT age_group, med_adh, COUNT(*) n
FROM joined GROUP BY age_group, med_adh ORDER BY age_group, n DESC
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-042/attempt-01/sql/S57.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-042/attempt-01/sql/S57.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-042/attempt-01/results/S57.rows.jsonl)；完整：True；SHA256：`5f7eac64eb52efea96f221aecf6411b95f242279ccdff4821d64d747af3bc70c`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "o", "kind": "base", "block": null, "base_tables": ["treatmentoutcomes"]}, {"alias": "tb", "kind": "base", "block": null, "base_tables": ["treatmentbasics"]}, {"alias": "e", "kind": "base", "block": null, "base_tables": ["encounters"]}, {"alias": "p", "kind": "base", "block": null, "base_tables": ["patients"]}] | [{"type": "INNER", "right": "treatmentbasics AS tb", "on": "tb.\"Treatment ID\" = o.\"Treatment reference\"", "using": []}, {"type": "INNER", "right": "encounters AS e", "on": "e.\"Visit Record Number\" = tb.\"Visit Reference\"", "using": []}, {"type": "INNER", "right": "patients AS p", "on": "e.\"Patient Reference Number\" = p.\"Patient number\"", "using": []}] | [] |
| B2 | [{"alias": "joined", "kind": "derived", "block": "B1", "base_tables": ["encounters", "patients", "treatmentbasics", "treatmentoutcomes"]}] | [] | ["age_group", "med_adh"] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B2 | COUNT(*) | [] | [] | True |


## S58

类别 `data`；来源 `query_db`；调用 `efe1d74cabe04567b525affab3f4259a`；状态 `success`。

```sql
WITH joined AS (
  SELECT p.Age,
    CASE WHEN p.Age BETWEEN 18 AND 44 THEN 'young_18-44'
         WHEN p.Age BETWEEN 45 AND 59 THEN 'middle_45-59'
         ELSE 'older_60+' END AS age_group,
    tb."Medication Side Effects" AS side_eff
  FROM treatmentoutcomes o
  JOIN treatmentbasics tb ON tb."Treatment ID" = o."Treatment reference"
  JOIN encounters e ON e."Visit Record Number" = tb."Visit Reference"
  JOIN patients p ON e."Patient Reference Number" = p."Patient number"
)
SELECT age_group, side_eff, COUNT(*) n
FROM joined GROUP BY age_group, side_eff ORDER BY age_group, n DESC
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-042/attempt-01/sql/S58.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-042/attempt-01/sql/S58.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-042/attempt-01/results/S58.rows.jsonl)；完整：True；SHA256：`24f8d5e5aa49eb48d4ce84a39c7b26f6ea78597341a71764042e1f4a105d58f8`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "o", "kind": "base", "block": null, "base_tables": ["treatmentoutcomes"]}, {"alias": "tb", "kind": "base", "block": null, "base_tables": ["treatmentbasics"]}, {"alias": "e", "kind": "base", "block": null, "base_tables": ["encounters"]}, {"alias": "p", "kind": "base", "block": null, "base_tables": ["patients"]}] | [{"type": "INNER", "right": "treatmentbasics AS tb", "on": "tb.\"Treatment ID\" = o.\"Treatment reference\"", "using": []}, {"type": "INNER", "right": "encounters AS e", "on": "e.\"Visit Record Number\" = tb.\"Visit Reference\"", "using": []}, {"type": "INNER", "right": "patients AS p", "on": "e.\"Patient Reference Number\" = p.\"Patient number\"", "using": []}] | [] |
| B2 | [{"alias": "joined", "kind": "derived", "block": "B1", "base_tables": ["encounters", "patients", "treatmentbasics", "treatmentoutcomes"]}] | [] | ["age_group", "side_eff"] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B2 | COUNT(*) | [] | [] | True |


## S59

类别 `data`；来源 `query_db`；调用 `ce8db93ffcbb42559a9f56f54981aa4e`；状态 `success`。

```sql
SELECT
  CASE WHEN p.Age BETWEEN 18 AND 44 THEN 'young_18-44'
       WHEN p.Age BETWEEN 45 AND 59 THEN 'middle_45-59'
       ELSE 'older_60+' END AS age_group,
  d."Primary Diagnosis" AS diagnosis,
  COUNT(*) AS n
FROM assessmentsocialanddiagnosis d
JOIN assessmentbasics a ON a."Assessment ID" = d."Social Diagnosis Assessment ID"
JOIN encounters e ON e."Assessment Reference" = a."Assessment ID"
JOIN patients p ON e."Patient Reference Number" = p."Patient number"
GROUP BY age_group, diagnosis
ORDER BY age_group, n DESC
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-042/attempt-01/sql/S59.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-042/attempt-01/sql/S59.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-042/attempt-01/results/S59.rows.jsonl)；完整：True；SHA256：`71d1173407b3e82cc2abd84939249b6243206223d212b89c0422d5f2e0368a59`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "d", "kind": "base", "block": null, "base_tables": ["assessmentsocialanddiagnosis"]}, {"alias": "a", "kind": "base", "block": null, "base_tables": ["assessmentbasics"]}, {"alias": "e", "kind": "base", "block": null, "base_tables": ["encounters"]}, {"alias": "p", "kind": "base", "block": null, "base_tables": ["patients"]}] | [{"type": "INNER", "right": "assessmentbasics AS a", "on": "a.\"Assessment ID\" = d.\"Social Diagnosis Assessment ID\"", "using": []}, {"type": "INNER", "right": "encounters AS e", "on": "e.\"Assessment Reference\" = a.\"Assessment ID\"", "using": []}, {"type": "INNER", "right": "patients AS p", "on": "e.\"Patient Reference Number\" = p.\"Patient number\"", "using": []}] | ["CASE WHEN p.Age BETWEEN 18 AND 44 THEN 'young_18-44' WHEN p.Age BETWEEN 45 AND 59 THEN 'middle_45-59' ELSE 'older_60+' END", "d.\"Primary Diagnosis\""] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |


## S60

类别 `data`；来源 `query_db`；调用 `e87609111baf46d7b1a79c05a6398e11`；状态 `success`。

```sql
SELECT
  CASE WHEN p.Age BETWEEN 18 AND 44 THEN 'young_18-44'
       WHEN p.Age BETWEEN 45 AND 59 THEN 'middle_45-59'
       ELSE 'older_60+' END AS age_group,
  d."Primary Diagnosis" AS diagnosis,
  COUNT(*) AS n
FROM assessmentsocialanddiagnosis d
JOIN assessmentbasics a ON a."Assessment ID" = d."Social Diagnosis Assessment ID"
JOIN encounters e ON e."Assessment Reference" = a."Assessment ID"
JOIN patients p ON e."Patient Reference Number" = p."Patient number"
GROUP BY age_group, diagnosis
ORDER BY age_group, n DESC
LIMIT 20
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-042/attempt-01/sql/S60.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-042/attempt-01/sql/S60.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-042/attempt-01/results/S60.rows.jsonl)；完整：True；SHA256：`71d1173407b3e82cc2abd84939249b6243206223d212b89c0422d5f2e0368a59`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "d", "kind": "base", "block": null, "base_tables": ["assessmentsocialanddiagnosis"]}, {"alias": "a", "kind": "base", "block": null, "base_tables": ["assessmentbasics"]}, {"alias": "e", "kind": "base", "block": null, "base_tables": ["encounters"]}, {"alias": "p", "kind": "base", "block": null, "base_tables": ["patients"]}] | [{"type": "INNER", "right": "assessmentbasics AS a", "on": "a.\"Assessment ID\" = d.\"Social Diagnosis Assessment ID\"", "using": []}, {"type": "INNER", "right": "encounters AS e", "on": "e.\"Assessment Reference\" = a.\"Assessment ID\"", "using": []}, {"type": "INNER", "right": "patients AS p", "on": "e.\"Patient Reference Number\" = p.\"Patient number\"", "using": []}] | ["CASE WHEN p.Age BETWEEN 18 AND 44 THEN 'young_18-44' WHEN p.Age BETWEEN 45 AND 59 THEN 'middle_45-59' ELSE 'older_60+' END", "d.\"Primary Diagnosis\""] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |

