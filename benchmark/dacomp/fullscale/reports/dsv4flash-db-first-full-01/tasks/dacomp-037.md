# dacomp-037

I want to understand what differences exist in health checkup data between people with a m…

运行：已提交。官方未评分。全部 SQL 尝试/成功 37/36；数据 SQL 35/34；Python 10 次。

完整原题：

I want to understand what differences exist in health checkup data between people with a medical history and those with no medical history, and how different medical history categories affect health checkup data.

| 表 | 行数 | 列数 |
| --- | --- | --- |
| health_checkup_indicators | 9972 | 18 |
| health_status | 9972 | 6 |


实际路线（分析者依据 SQL/源码概括，不代表 Agent 自述）：关联病史与体检指标 → SQL 汇总各病史类别 → Python 分布检验和两两比较 → 分性别补充分析并绘图。

数据库大小：2,863,104 字节。

## 数据 SQL

| SQL | 状态 | 基础表 | Join 输入/类型 | GROUP BY | 聚合表达式 | 结果行数 | 数据库 ms |
| --- | --- | --- | --- | --- | --- | --- | --- |
| [S3/Q1](#s3) | success | ["health_status"] | 0 / {} | [] | [] | 20 | 0.383 |
| [S4/Q2](#s4) | success | ["health_checkup_indicators"] | 0 / {} | [] | [] | 20 | 0.402 |
| [S5/Q3](#s5) | success | ["health_checkup_indicators"] | 0 / {} | [] | ["COUNT(*)"] | 1 | 1.304 |
| [S6/Q4](#s6) | success | ["health_status"] | 0 / {} | [] | ["COUNT(*)"] | 1 | 0.762 |
| [S7/Q5](#s7) | success | ["health_status"] | 0 / {} | ["\"Medical history\""] | ["COUNT(*)"] | 4 | 3.581 |
| [S8/Q6](#s8) | success | ["health_status"] | 0 / {} | ["\"Health status\""] | ["COUNT(*)"] | 4 | 3.364 |
| [S9/Q7](#s9) | success | ["health_checkup_indicators"] | 0 / {} | [] | ["COUNT(DISTINCT ID)", "COUNT(*)"] | 1 | 3.029 |
| [S10/Q8](#s10) | success | ["health_checkup_indicators", "health_status"] | 2 / {'LEFT': 1} | [] | [] | 0 | 8.708 |
| [S11/Q9](#s11) | success | ["health_checkup_indicators"] | 0 / {} | ["Gender"] | ["COUNT(*)"] | 2 | 3.164 |
| [S12/Q10](#s12) | success | ["health_checkup_indicators", "health_status"] | 2 / {'INNER': 1} | ["\"Medical history\"", "Gender"] | ["COUNT(*)"] | 8 | 14.429 |
| [S13/Q11](#s13) | success | ["health_checkup_indicators", "health_status"] | 2 / {'INNER': 1} | ["s.\"Medical history\""] | ["COUNT(*)", "AVG(i.Age)", "AVG(i.\"Height (cm)\")", "AVG(i.\"Weight (kg)\")", "AVG(i.\"Blood Pressure (Systolic)\")", "AVG(i.\"Blood Pressure (Diastolic)\")", "AVG(i.\"Heart Rate (bpm)\")", "AVG(i.\"Respiratory Rate (breaths/min)\")", "AVG(i.\"Blood Oxygen Saturation (%)\")", "AVG(i.\"Blood Glucose (mmol/L)\")", "AVG(i.\"Total Cholesterol (mmol/L)\")", "AVG(i.\"Lipoprotein (mmol/L)\")", "AVG(i.\"Triglycerides (mmol/L)\")", "AVG(i.\"Uric Acid (umol/L)\")", "AVG(i.\"Blood Urea Nitrogen (mmol/L)\")", "AVG(i.\"Alanine Aminotransferase (U/L)\")", "AVG(i.\"Serum Potassium (mmol/L)\")"] | 4 | 32.688 |
| [S14/Q12](#s14) | failed | ["health_checkup_indicators", "health_status"] | 2 / {'INNER': 1} | ["s.\"Medical history\""] | ["AVG(i.\"Blood Pressure (Systolic)\")", "STDDEV(i.\"Blood Pressure (Systolic)\")", "AVG(i.\"Blood Pressure (Diastolic)\")", "STDDEV(i.\"Blood Pressure (Diastolic)\")", "AVG(i.\"Blood Glucose (mmol/L)\")", "STDDEV(i.\"Blood Glucose (mmol/L)\")", "AVG(i.\"Total Cholesterol (mmol/L)\")", "STDDEV(i.\"Total Cholesterol (mmol/L)\")", "AVG(i.\"Triglycerides (mmol/L)\")", "STDDEV(i.\"Triglycerides (mmol/L)\")", "AVG(i.\"Uric Acid (umol/L)\")", "STDDEV(i.\"Uric Acid (umol/L)\")", "AVG(i.\"Alanine Aminotransferase (U/L)\")", "STDDEV(i.\"Alanine Aminotransferase (U/L)\")", "AVG(i.\"Serum Potassium (mmol/L)\")", "STDDEV(i.\"Serum Potassium (mmol/L)\")"] | unknown | 未取得；调用总时长 0.207 ms |
| [S15/Q13](#s15) | success | ["health_checkup_indicators", "health_status"] | 2 / {'INNER': 1} | ["s.\"Medical history\""] | ["AVG(i.\"Blood Pressure (Systolic)\")", "AVG(i.\"Blood Pressure (Diastolic)\")", "AVG(i.\"Blood Glucose (mmol/L)\")", "AVG(i.\"Total Cholesterol (mmol/L)\")", "AVG(i.\"Triglycerides (mmol/L)\")", "AVG(i.\"Uric Acid (umol/L)\")", "AVG(i.\"Alanine Aminotransferase (U/L)\")", "AVG(i.\"Blood Pressure (Systolic)\" * i.\"Blood Pressure (Systolic)\")", "AVG(i.\"Blood Pressure (Diastolic)\" * i.\"Blood Pressure (Diastolic)\")", "AVG(i.\"Blood Glucose (mmol/L)\" * i.\"Blood Glucose (mmol/L)\")", "AVG(i.\"Total Cholesterol (mmol/L)\" * i.\"Total Cholesterol (mmol/L)\")", "AVG(i.\"Triglycerides (mmol/L)\" * i.\"Triglycerides (mmol/L)\")", "AVG(i.\"Uric Acid (umol/L)\" * i.\"Uric Acid (umol/L)\")", "AVG(i.\"Alanine Aminotransferase (U/L)\" * i.\"Alanine Aminotransferase (U/L)\")", "AVG(i.\"Blood Pressure (Systolic)\")", "AVG(i.\"Blood Pressure (Systolic)\")", "AVG(i.\"Blood Pressure (Diastolic)\")", "AVG(i.\"Blood Pressure (Diastolic)\")", "AVG(i.\"Blood Glucose (mmol/L)\")", "AVG(i.\"Blood Glucose (mmol/L)\")", "AVG(i.\"Total Cholesterol (mmol/L)\")", "AVG(i.\"Total Cholesterol (mmol/L)\")", "AVG(i.\"Triglycerides (mmol/L)\")", "AVG(i.\"Triglycerides (mmol/L)\")", "AVG(i.\"Uric Acid (umol/L)\")", "AVG(i.\"Uric Acid (umol/L)\")", "AVG(i.\"Alanine Aminotransferase (U/L)\")", "AVG(i.\"Alanine Aminotransferase (U/L)\")"] | 4 | 22.88 |
| [S16/Q14](#s16) | success | ["health_checkup_indicators", "health_status"] | 2 / {'INNER': 1} | ["s.\"Medical history\""] | ["MIN(i.\"Blood Pressure (Systolic)\")", "MAX(i.\"Blood Pressure (Systolic)\")", "MIN(i.\"Blood Pressure (Diastolic)\")", "MAX(i.\"Blood Pressure (Diastolic)\")", "MIN(i.\"Blood Glucose (mmol/L)\")", "MAX(i.\"Blood Glucose (mmol/L)\")", "MIN(i.\"Serum Potassium (mmol/L)\")", "MAX(i.\"Serum Potassium (mmol/L)\")"] | 4 | 17.991 |
| [S17/Q15](#s17) | success | ["health_checkup_indicators", "health_status"] | 2 / {'INNER': 1} | ["s.\"Medical history\"", "s.\"Health status\""] | ["COUNT(*)"] | 16 | 14.754 |
| [S18/Q16](#s18) | success | ["health_status"] | 0 / {} | ["s.\"Medical history\"", "s.\"Health status\""] | ["COUNT(*)"] | 4 | 3.976 |
| [S19/Q17](#s19) | success | ["health_checkup_indicators", "health_status"] | 2 / {'INNER': 1} | ["s.\"Medical history\""] | ["AVG(i.\"Age\")", "AVG(i.\"Weight (kg)\")", "AVG(i.\"Heart Rate (bpm)\")"] | 4 | 14.522 |
| [S20/Q18](#s20) | success | ["health_checkup_indicators", "health_status"] | 2 / {'INNER': 1} | [] | [] | 9972 | 45.472 |
| [S21/Q19](#s21) | success | ["health_checkup_indicators", "health_status"] | 2 / {'INNER': 1} | [] | [] | 9972 | 45.489 |
| [S22/Q20](#s22) | success | ["health_checkup_indicators", "health_status"] | 2 / {'INNER': 1} | [] | [] | 9972 | 43.826 |
| [S23/Q21](#s23) | success | ["health_checkup_indicators", "health_status"] | 2 / {'INNER': 1} | [] | [] | 9972 | 25.674 |
| [S24/Q22](#s24) | success | ["health_checkup_indicators", "health_status"] | 2 / {'INNER': 1} | [] | [] | 9972 | 21.436 |
| [S25/Q23](#s25) | success | ["health_status"] | 0 / {} | ["\"Medical history\"", "\"Smoking status\""] | ["COUNT(*)"] | 12 | 6.544 |
| [S26/Q24](#s26) | success | ["health_status"] | 0 / {} | ["\"Medical history\"", "\"Drinking Status\""] | ["COUNT(*)"] | 12 | 6.392 |
| [S27/Q25](#s27) | success | ["health_checkup_indicators", "health_status"] | 2 / {'INNER': 1} | [] | [] | 9972 | 45.753 |
| [S28/Q26](#s28) | success | ["health_checkup_indicators", "health_status"] | 2 / {'INNER': 1} | [] | [] | 9972 | 17.507 |
| [S29/Q27](#s29) | success | ["health_checkup_indicators", "health_status"] | 2 / {'INNER': 1} | ["s.\"Medical history\"", "i.Gender"] | ["AVG(i.\"Blood Pressure (Systolic)\")", "AVG(i.\"Blood Pressure (Diastolic)\")"] | 8 | 17.077 |
| [S30/Q28](#s30) | success | ["health_checkup_indicators"] | 0 / {} | [] | ["COUNT(*)"] | 1 | 0.391 |
| [S31/Q29](#s31) | success | ["health_checkup_indicators"] | 0 / {} | [] | ["SUM(CASE WHEN Age IS NULL THEN 1 ELSE 0 END)", "SUM(CASE WHEN \"Weight (kg)\" IS NULL THEN 1 ELSE 0 END)", "SUM(CASE WHEN \"Blood Pressure (Systolic)\" IS NULL THEN 1 ELSE 0 END)", "SUM(CASE WHEN \"Blood Glucose (mmol/L)\" IS NULL THEN 1 ELSE 0 END)"] | 1 | 3.009 |
| [S32/Q30](#s32) | success | ["health_status"] | 0 / {} | [] | ["SUM(CASE WHEN \"Medical history\" IS NULL THEN 1 ELSE 0 END)", "SUM(CASE WHEN \"Health status\" IS NULL THEN 1 ELSE 0 END)", "SUM(CASE WHEN ID IS NULL THEN 1 ELSE 0 END)"] | 1 | 2.018 |
| [S33/Q31](#s33) | success | ["health_checkup_indicators", "health_status"] | 2 / {'INNER': 1} | ["s.\"Medical history\""] | ["COUNT(*)", "COUNT(*)", "COUNT(*)", "COUNT(*)", "COUNT(*)", "COUNT(*)", "SUM(CASE WHEN i.\"Blood Pressure (Systolic)\" >= 130 OR i.\"Blood Pressure (Diastolic)\" >= 85 THEN 1 ELSE 0 END)", "SUM(CASE WHEN i.\"Blood Pressure (Systolic)\" >= 140 OR i.\"Blood Pressure (Diastolic)\" >= 90 THEN 1 ELSE 0 END)", "SUM(CASE WHEN i.\"Weight (kg)\" >= 75 THEN 1 ELSE 0 END)", "SUM(CASE WHEN i.\"Blood Glucose (mmol/L)\" >= 5.6 THEN 1 ELSE 0 END)", "SUM(CASE WHEN i.\"Alanine Aminotransferase (U/L)\" >= 40 THEN 1 ELSE 0 END)"] | 4 | 17.201 |
| [S34/Q32](#s34) | success | ["health_checkup_indicators", "health_status"] | 2 / {'INNER': 1} | ["s.\"Medical history\""] | ["COUNT(*)", "COUNT(*)", "COUNT(*)", "SUM(CASE WHEN i.\"Blood Pressure (Systolic)\" >= 130 OR i.\"Blood Pressure (Diastolic)\" >= 85 THEN 1 ELSE 0 END)", "SUM(CASE WHEN i.\"Blood Pressure (Systolic)\" >= 140 OR i.\"Blood Pressure (Diastolic)\" >= 90 THEN 1 ELSE 0 END)"] | 4 | 13.55 |
| [S35/Q33](#s35) | success | ["health_checkup_indicators", "health_status"] | 2 / {'INNER': 1} | ["s.\"Medical history\""] | ["COUNT(*)", "COUNT(*)", "COUNT(*)", "SUM(CASE WHEN i.\"Blood Pressure (Systolic)\" >= 130 OR i.\"Blood Pressure (Diastolic)\" >= 85 THEN 1 ELSE 0 END)", "SUM(CASE WHEN i.\"Blood Pressure (Systolic)\" >= 140 OR i.\"Blood Pressure (Diastolic)\" >= 90 THEN 1 ELSE 0 END)"] | 4 | 13.346 |
| [S36/Q34](#s36) | success | ["health_checkup_indicators", "health_status"] | 2 / {'INNER': 1} | [] | [] | 9972 | 39.486 |
| [S37/Q35](#s37) | success | ["health_checkup_indicators", "health_status"] | 2 / {'INNER': 1} | [] | [] | 9972 | 19.034 |


## 元数据和设置

| SQL | 类别 | 状态 | 内容 |
| --- | --- | --- | --- |
| S1 | connection_setup | success | PRAGMA query_only=ON |
| S2 | metadata | success | SELECT name,sql FROM sqlite_master WHERE type='table' ORDER BY name |


## Python 与执行位置

人工源码审查：**reviewed_with_statistical_exceptions_and_SQL_capable_summaries**。Python 的中位数/分位数、Kruskal、Mann-Whitney 和卡方检验用于病史组间分布比较，属于合理统计补充。P6 额外计算病史×性别均值/计数，P9 先用 pandas 汇总病史组均值再标准化；均值与计数可以先在 SQL 准备。这些部分单独标注，不把统计检验中的组划分一概当作违规。 [证据](../reviews/dacomp-037.json)。

P1：Statistical hypothesis tests (Kruskal-Wallis / ANOVA across medical history groups for each health indicator), medians, IQRs, and effect sizes are not reasonably supported by SQLite. I retrieve only the columns needed for these statistical procedures.

[源码](../../../runs/dsv4flash-db-first-full-01/dacomp-037/attempt-01/python/P1.py)；[输出](../../../runs/dsv4flash-db-first-full-01/dacomp-037/attempt-01/python/P1.stdout)；[错误](../../../runs/dsv4flash-db-first-full-01/dacomp-037/attempt-01/python/P1.stderr)。检出需人工核验的 SQL 可实现操作：groupby(, .query(；不能仅凭理由判为合规。

P2：Statistical hypothesis tests (Kruskal-Wallis) across medical history groups for each health indicator. This is not reasonably supported by SQLite. I retrieve only the joined columns needed.

[源码](../../../runs/dsv4flash-db-first-full-01/dacomp-037/attempt-01/python/P2.py)；[输出](../../../runs/dsv4flash-db-first-full-01/dacomp-037/attempt-01/python/P2.stdout)；[错误](../../../runs/dsv4flash-db-first-full-01/dacomp-037/attempt-01/python/P2.stderr)。检出需人工核验的 SQL 可实现操作：groupby(, .query(；不能仅凭理由判为合规。

P3：Post-hoc pairwise comparisons and effect sizes (rank-biserial, Cohen's d) between medical history categories for the indicators that showed significant overall differences. This is a statistical procedure not supported by SQLite.

[源码](../../../runs/dsv4flash-db-first-full-01/dacomp-037/attempt-01/python/P3.py)；[输出](../../../runs/dsv4flash-db-first-full-01/dacomp-037/attempt-01/python/P3.stdout)；[错误](../../../runs/dsv4flash-db-first-full-01/dacomp-037/attempt-01/python/P3.stderr)。检出需人工核验的 SQL 可实现操作：.query(；不能仅凭理由判为合规。

P4：Visualization: boxplots and summary figures for the report. I need raw data from the joined tables to create these plots.

[源码](../../../runs/dsv4flash-db-first-full-01/dacomp-037/attempt-01/python/P4.py)；[输出](../../../runs/dsv4flash-db-first-full-01/dacomp-037/attempt-01/python/P4.stdout)；[错误](../../../runs/dsv4flash-db-first-full-01/dacomp-037/attempt-01/python/P4.stderr)。检出需人工核验的 SQL 可实现操作：.query(；不能仅凭理由判为合规。

P5：Fix boxplot call (tick_labels instead of labels) for the key-indicator comparison figures.

[源码](../../../runs/dsv4flash-db-first-full-01/dacomp-037/attempt-01/python/P5.py)；[输出](../../../runs/dsv4flash-db-first-full-01/dacomp-037/attempt-01/python/P5.stdout)；[错误](../../../runs/dsv4flash-db-first-full-01/dacomp-037/attempt-01/python/P5.stderr)。检出需人工核验的 SQL 可实现操作：.query(；不能仅凭理由判为合规。

P6：Create a comprehensive effect-size heatmap/figure for all indicators across medical history categories (Cohen's d vs None baseline). This is visualization not supported by SQLite.

[源码](../../../runs/dsv4flash-db-first-full-01/dacomp-037/attempt-01/python/P6.py)；[输出](../../../runs/dsv4flash-db-first-full-01/dacomp-037/attempt-01/python/P6.stdout)；[错误](../../../runs/dsv4flash-db-first-full-01/dacomp-037/attempt-01/python/P6.stderr)。检出需人工核验的 SQL 可实现操作：groupby(, .query(；不能仅凭理由判为合规。

P7：Check gender-specific BP patterns and data quality (nulls) - these are quick verifications; the null count is aggregated in SQL and gender-grouped BP means are aggregated in SQL, but combined verification in Python is simpler.

[源码](../../../runs/dsv4flash-db-first-full-01/dacomp-037/attempt-01/python/P7.py)；[输出](../../../runs/dsv4flash-db-first-full-01/dacomp-037/attempt-01/python/P7.stdout)；[错误](../../../runs/dsv4flash-db-first-full-01/dacomp-037/attempt-01/python/P7.stderr)。检出需人工核验的 SQL 可实现操作：.query(；不能仅凭理由判为合规。

P8：Create a prevalence bar chart (elevated/high blood pressure by medical history group) to illustrate the clinical significance of the differences. This is visualization, not a SQL-supported computation.

[源码](../../../runs/dsv4flash-db-first-full-01/dacomp-037/attempt-01/python/P8.py)；[输出](../../../runs/dsv4flash-db-first-full-01/dacomp-037/attempt-01/python/P8.stdout)；[错误](../../../runs/dsv4flash-db-first-full-01/dacomp-037/attempt-01/python/P8.stderr)。检出需人工核验的 SQL 可实现操作：groupby(, .query(；不能仅凭理由判为合规。

P9：Fix numpy import and create prevalence bar chart and z-score table. This is visualization not supported by SQLite.

[源码](../../../runs/dsv4flash-db-first-full-01/dacomp-037/attempt-01/python/P9.py)；[输出](../../../runs/dsv4flash-db-first-full-01/dacomp-037/attempt-01/python/P9.stdout)；[错误](../../../runs/dsv4flash-db-first-full-01/dacomp-037/attempt-01/python/P9.stderr)。检出需人工核验的 SQL 可实现操作：groupby(, .query(；不能仅凭理由判为合规。

P10：Chi-square tests for categorical associations (health status, smoking, drinking vs medical history). This is a statistical test not supported by SQLite.

[源码](../../../runs/dsv4flash-db-first-full-01/dacomp-037/attempt-01/python/P10.py)；[输出](../../../runs/dsv4flash-db-first-full-01/dacomp-037/attempt-01/python/P10.stdout)；[错误](../../../runs/dsv4flash-db-first-full-01/dacomp-037/attempt-01/python/P10.stderr)。检出需人工核验的 SQL 可实现操作：.query(；不能仅凭理由判为合规。

## 优化机会

已验证候选。筛选限于精确 SQL、相同自包含 CTE、相同单表完整过滤、可分解单表聚合；未覆盖任意 Join 等价和一般谓词蕴含。全部候选都是 offline，未测在线预测。

| 候选 | 类型 | 已有结果 | 覆盖 SQL | 后续次数 | 中间行数 | 验证 | 成本 |
| --- | --- | --- | --- | --- | --- | --- | --- |
| C1 | exact-result reuse | True | ["S20", "S21", "S22", "S27"] | 3 | 9972 | verified | Not benchmarked; correctness alone does not establish net speedup. |
| C2 | exact-result reuse | True | ["S34", "S35"] | 1 | unknown | not_verified_cap | Not tested |
| C3 | aggregate MV | False | ["S6", "S7", "S8", "S25", "S26", "S32"] | 5 | 144 | verified | Not benchmarked; correctness alone does not establish net speedup. |
| C4 | aggregate MV | False | ["S5", "S11", "S30", "S31"] | 3 | 2 | verified | Not benchmarked; correctness alone does not establish net speedup. |


已验证覆盖（含触发查询、候选并集去重）：14/34 条成功数据 SQL。正确性仅针对当前数据库快照；未测性能的候选不能声称已加速。

[完整 build/rewrite 与比较证据](dacomp-037.analysis.json)。

### C3：aggregate MV

Union of grouping keys; decomposable aggregate states; AVG uses SUM and non-NULL COUNT.

原查询 [S6](#s6), [S7](#s7), [S8](#s8), [S25](#s25), [S26](#s26), [S32](#s32) → 新增共享状态 C3 → 后续 5 次可复用。该构建点为事后假设，不代表 Agent 当时预知后续。

构建定义：

```sql
SELECT "Medical history" AS __g0, "Health status" AS __g1, "Smoking status" AS __g2, "Drinking Status" AS __g3, COUNT(*) AS __a0, SUM(CASE WHEN "Medical history" IS NULL THEN 1 ELSE 0 END) AS __a1, SUM(CASE WHEN "Health status" IS NULL THEN 1 ELSE 0 END) AS __a2, SUM(CASE WHEN id IS NULL THEN 1 ELSE 0 END) AS __a3 FROM "health_status"  GROUP BY "Medical history", "Health status", "Smoking status", "Drinking Status"
```

受益查询 S6 的改写示例：

```sql
SELECT SUM(__a0) AS total_rows FROM temp.reuse_candidate
```

| 原 SQL | 列名一致 | 结果一致 | 比较方法 |
| --- | --- | --- | --- |
| S6 | True | True | exact_multiset |
| S7 | True | True | ordered_numeric_tolerance |
| S8 | True | True | ordered_numeric_tolerance |
| S25 | True | True | ordered_numeric_tolerance |
| S26 | True | True | ordered_numeric_tolerance |
| S32 | True | True | exact_multiset |


验证状态：verified；成本结论：Not benchmarked; correctness alone does not establish net speedup.

### C1：exact-result reuse

Identical normalized SQL and parameters; archive equality checked.

原查询 [S20](#s20), [S21](#s21), [S22](#s22), [S27](#s27) → 保留前序结果 S20 → 后续 3 次可复用。该构建点为事后假设，不代表 Agent 当时预知后续。

| 原 SQL | 列名一致 | 结果一致 | 比较方法 |
| --- | --- | --- | --- |
| S21 | True | True | exact_multiset |
| S22 | True | True | exact_multiset |
| S27 | True | True | exact_multiset |


验证状态：verified；成本结论：Not benchmarked; correctness alone does not establish net speedup.

### C4：aggregate MV

Union of grouping keys; decomposable aggregate states; AVG uses SUM and non-NULL COUNT.

原查询 [S5](#s5), [S11](#s11), [S30](#s30), [S31](#s31) → 新增共享状态 C4 → 后续 3 次可复用。该构建点为事后假设，不代表 Agent 当时预知后续。

构建定义：

```sql
SELECT gender AS __g0, COUNT(*) AS __a0, SUM(CASE WHEN age IS NULL THEN 1 ELSE 0 END) AS __a1, SUM(CASE WHEN "Weight (kg)" IS NULL THEN 1 ELSE 0 END) AS __a2, SUM(CASE WHEN "Blood Pressure (Systolic)" IS NULL THEN 1 ELSE 0 END) AS __a3, SUM(CASE WHEN "Blood Glucose (mmol/L)" IS NULL THEN 1 ELSE 0 END) AS __a4 FROM "health_checkup_indicators"  GROUP BY gender
```

受益查询 S5 的改写示例：

```sql
SELECT SUM(__a0) AS total_rows FROM temp.reuse_candidate
```

| 原 SQL | 列名一致 | 结果一致 | 比较方法 |
| --- | --- | --- | --- |
| S5 | True | True | exact_multiset |
| S11 | True | True | exact_multiset |
| S30 | True | True | exact_multiset |
| S31 | True | True | exact_multiset |


验证状态：verified；成本结论：Not benchmarked; correctness alone does not establish net speedup.

结果依赖：自动记录 SQL→Python 的接口父调用，以及源码中引用归档文件的消费者；字面值相同不认定因果。模型方向选择需要人工读取消息，尚未做全面因果标注。

[原始报告](../../../runs/dsv4flash-db-first-full-01/dacomp-037/attempt-01/answer.md)；[统一消息](../../../runs/dsv4flash-db-first-full-01/dacomp-037/attempt-01/messages.jsonl)；[原始 OpenCode 事件](../../../runs/dsv4flash-db-first-full-01/dacomp-037/attempt-01/opencode.jsonl)；[SQL 引擎日志](../../../runs/dsv4flash-db-first-full-01/dacomp-037/attempt-01/sql_journal.jsonl)。

[可读报告（本地图片链接规范化）](../answers/dacomp-037.md)。原始回答保留，分析结论未改写。

## S1

类别 `connection_setup`；来源 `connection`；调用 `9bd4077703de47f9a67a94514f769ef1`；状态 `success`。

```sql
PRAGMA query_only=ON
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-037/attempt-01/sql/S1.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-037/attempt-01/sql/S1.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-037/attempt-01/results/S1.rows.jsonl)；完整：True；SHA256：`e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`。

## S2

类别 `metadata`；来源 `list_db`；调用 `9bd4077703de47f9a67a94514f769ef1`；状态 `success`。

```sql
SELECT name,sql FROM sqlite_master WHERE type='table' ORDER BY name
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-037/attempt-01/sql/S2.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-037/attempt-01/sql/S2.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-037/attempt-01/results/S2.rows.jsonl)；完整：True；SHA256：`6f641bc3651b6aac19afe31ded042d5b300951c9a957bab11510f2a5041cc39a`。

## S3

类别 `data`；来源 `query_db`；调用 `2e1f53fd6054440e98eee2a7c590f419`；状态 `success`。

```sql
SELECT * FROM health_status LIMIT 20
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-037/attempt-01/sql/S3.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-037/attempt-01/sql/S3.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-037/attempt-01/results/S3.rows.jsonl)；完整：True；SHA256：`8cb038afa283fef3faa69bbb3498deb03b65b083024164f88cc7750d657fa70c`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "health_status", "kind": "base", "block": null, "base_tables": ["health_status"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |


## S4

类别 `data`；来源 `query_db`；调用 `197a1f498d3044ef942ce1f8a00822f7`；状态 `success`。

```sql
SELECT * FROM health_checkup_indicators LIMIT 20
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-037/attempt-01/sql/S4.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-037/attempt-01/sql/S4.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-037/attempt-01/results/S4.rows.jsonl)；完整：True；SHA256：`cc8b1f6c42286b9e3cfe53569a3eb80df08bfef9e5b1f62ede3a09c2120e9c35`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "health_checkup_indicators", "kind": "base", "block": null, "base_tables": ["health_checkup_indicators"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |


## S5

类别 `data`；来源 `query_db`；调用 `2b830c339e4e4f95be718b3b0527cbaa`；状态 `success`。

```sql
SELECT COUNT(*) AS total_rows FROM health_checkup_indicators
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-037/attempt-01/sql/S5.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-037/attempt-01/sql/S5.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-037/attempt-01/results/S5.rows.jsonl)；完整：True；SHA256：`3006a434a2e10651d91445b941a2785d48c87aa2797ad73c00b0211e7613fa85`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "health_checkup_indicators", "kind": "base", "block": null, "base_tables": ["health_checkup_indicators"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |


## S6

类别 `data`；来源 `query_db`；调用 `ac3fa90e51044274869bf411e92e26e6`；状态 `success`。

```sql
SELECT COUNT(*) AS total_rows FROM health_status
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-037/attempt-01/sql/S6.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-037/attempt-01/sql/S6.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-037/attempt-01/results/S6.rows.jsonl)；完整：True；SHA256：`3006a434a2e10651d91445b941a2785d48c87aa2797ad73c00b0211e7613fa85`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "health_status", "kind": "base", "block": null, "base_tables": ["health_status"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |


## S7

类别 `data`；来源 `query_db`；调用 `9c0f5071b1a246519babea2058c23c33`；状态 `success`。

```sql
SELECT "Medical history", COUNT(*) AS n FROM health_status GROUP BY "Medical history" ORDER BY n DESC
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-037/attempt-01/sql/S7.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-037/attempt-01/sql/S7.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-037/attempt-01/results/S7.rows.jsonl)；完整：True；SHA256：`3f871db090aba1b440a69190017e8270ab7e5e0c0239f94e8b37b958fa8aeae6`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "health_status", "kind": "base", "block": null, "base_tables": ["health_status"]}] | [] | ["\"Medical history\""] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |


## S8

类别 `data`；来源 `query_db`；调用 `13cee3172bd44b0991fda20c2a778483`；状态 `success`。

```sql
SELECT "Health status", COUNT(*) AS n FROM health_status GROUP BY "Health status" ORDER BY n DESC
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-037/attempt-01/sql/S8.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-037/attempt-01/sql/S8.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-037/attempt-01/results/S8.rows.jsonl)；完整：True；SHA256：`3b3f9118a7c64e79af8cda343145e7b15699cf09f70129c70575e22b33954491`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "health_status", "kind": "base", "block": null, "base_tables": ["health_status"]}] | [] | ["\"Health status\""] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |


## S9

类别 `data`；来源 `query_db`；调用 `2fba6e1df8424e3ba702056edd5ba29c`；状态 `success`。

```sql
SELECT COUNT(DISTINCT ID) AS distinct_ids, COUNT(*) AS total FROM health_checkup_indicators
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-037/attempt-01/sql/S9.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-037/attempt-01/sql/S9.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-037/attempt-01/results/S9.rows.jsonl)；完整：True；SHA256：`6b47252455e4e1ad04ab85a5b3cc9351c12850e26f923d1b4d7a6bfb0144f78b`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "health_checkup_indicators", "kind": "base", "block": null, "base_tables": ["health_checkup_indicators"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(DISTINCT ID) | [{"table": "health_checkup_indicators", "column": "ID"}] | [] | False |
| B1 | COUNT(*) | [] | [] | True |


## S10

类别 `data`；来源 `query_db`；调用 `d04dab799ff6454a88e3b28613017edc`；状态 `success`。

```sql
SELECT h.ID FROM health_status h LEFT JOIN health_checkup_indicators i ON h.ID = i.ID WHERE i.ID IS NULL LIMIT 5
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-037/attempt-01/sql/S10.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-037/attempt-01/sql/S10.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-037/attempt-01/results/S10.rows.jsonl)；完整：True；SHA256：`e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "h", "kind": "base", "block": null, "base_tables": ["health_status"]}, {"alias": "i", "kind": "base", "block": null, "base_tables": ["health_checkup_indicators"]}] | [{"type": "LEFT", "right": "health_checkup_indicators AS i", "on": "h.ID = i.ID", "using": []}] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |


## S11

类别 `data`；来源 `query_db`；调用 `5d735e976bbe4dfb8681c33addb4a598`；状态 `success`。

```sql
SELECT Gender, COUNT(*) AS n FROM health_checkup_indicators GROUP BY Gender
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-037/attempt-01/sql/S11.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-037/attempt-01/sql/S11.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-037/attempt-01/results/S11.rows.jsonl)；完整：True；SHA256：`4588af41bc4ae9736dde857296b241a65afa628e47cf6a8c1cc63af6dc57788e`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "health_checkup_indicators", "kind": "base", "block": null, "base_tables": ["health_checkup_indicators"]}] | [] | ["Gender"] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |


## S12

类别 `data`；来源 `query_db`；调用 `4aa2e8bf63ea40c196437eb333166d9e`；状态 `success`。

```sql
SELECT "Medical history", Gender, COUNT(*) AS n FROM health_status s JOIN health_checkup_indicators i ON s.ID = i.ID GROUP BY "Medical history", Gender ORDER BY "Medical history", Gender
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-037/attempt-01/sql/S12.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-037/attempt-01/sql/S12.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-037/attempt-01/results/S12.rows.jsonl)；完整：True；SHA256：`a493bca395ee7c3cfd0856e306bf0b74802994b29ae85520ed6b0c006a6f9dad`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "s", "kind": "base", "block": null, "base_tables": ["health_status"]}, {"alias": "i", "kind": "base", "block": null, "base_tables": ["health_checkup_indicators"]}] | [{"type": "INNER", "right": "health_checkup_indicators AS i", "on": "s.ID = i.ID", "using": []}] | ["\"Medical history\"", "Gender"] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |


## S13

类别 `data`；来源 `query_db`；调用 `3299e8a7728642fd85127323a511ca11`；状态 `success`。

```sql
SELECT
  s."Medical history",
  COUNT(*) AS n,
  ROUND(AVG(i.Age),2) AS age_mean,
  ROUND(AVG(i."Height (cm)"),2) AS height_mean,
  ROUND(AVG(i."Weight (kg)"),2) AS weight_mean,
  ROUND(AVG(i."Blood Pressure (Systolic)"),2) AS sbp_mean,
  ROUND(AVG(i."Blood Pressure (Diastolic)"),2) AS dbp_mean,
  ROUND(AVG(i."Heart Rate (bpm)"),2) AS hr_mean,
  ROUND(AVG(i."Respiratory Rate (breaths/min)"),2) AS rr_mean,
  ROUND(AVG(i."Blood Oxygen Saturation (%)"),2) AS spo2_mean,
  ROUND(AVG(i."Blood Glucose (mmol/L)"),2) AS glucose_mean,
  ROUND(AVG(i."Total Cholesterol (mmol/L)"),2) AS chol_mean,
  ROUND(AVG(i."Lipoprotein (mmol/L)"),2) AS lipo_mean,
  ROUND(AVG(i."Triglycerides (mmol/L)"),2) AS tg_mean,
  ROUND(AVG(i."Uric Acid (umol/L)"),2) AS uric_mean,
  ROUND(AVG(i."Blood Urea Nitrogen (mmol/L)"),2) AS bun_mean,
  ROUND(AVG(i."Alanine Aminotransferase (U/L)"),2) AS alt_mean,
  ROUND(AVG(i."Serum Potassium (mmol/L)"),2) AS k_mean
FROM health_status s
JOIN health_checkup_indicators i ON s.ID = i.ID
GROUP BY s."Medical history"
ORDER BY s."Medical history"
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-037/attempt-01/sql/S13.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-037/attempt-01/sql/S13.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-037/attempt-01/results/S13.rows.jsonl)；完整：True；SHA256：`a53128de42b2706242c2ec8298efb1c405188bf64fd19a2b41be2ae08cfe01f9`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "s", "kind": "base", "block": null, "base_tables": ["health_status"]}, {"alias": "i", "kind": "base", "block": null, "base_tables": ["health_checkup_indicators"]}] | [{"type": "INNER", "right": "health_checkup_indicators AS i", "on": "s.ID = i.ID", "using": []}] | ["s.\"Medical history\""] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |
| B1 | AVG(i.Age) | [{"table": "health_checkup_indicators", "column": "Age"}] | [] | False |
| B1 | AVG(i."Height (cm)") | [{"table": "health_checkup_indicators", "column": "Height (cm)"}] | [] | False |
| B1 | AVG(i."Weight (kg)") | [{"table": "health_checkup_indicators", "column": "Weight (kg)"}] | [] | False |
| B1 | AVG(i."Blood Pressure (Systolic)") | [{"table": "health_checkup_indicators", "column": "Blood Pressure (Systolic)"}] | [] | False |
| B1 | AVG(i."Blood Pressure (Diastolic)") | [{"table": "health_checkup_indicators", "column": "Blood Pressure (Diastolic)"}] | [] | False |
| B1 | AVG(i."Heart Rate (bpm)") | [{"table": "health_checkup_indicators", "column": "Heart Rate (bpm)"}] | [] | False |
| B1 | AVG(i."Respiratory Rate (breaths/min)") | [{"table": "health_checkup_indicators", "column": "Respiratory Rate (breaths/min)"}] | [] | False |
| B1 | AVG(i."Blood Oxygen Saturation (%)") | [{"table": "health_checkup_indicators", "column": "Blood Oxygen Saturation (%)"}] | [] | False |
| B1 | AVG(i."Blood Glucose (mmol/L)") | [{"table": "health_checkup_indicators", "column": "Blood Glucose (mmol/L)"}] | [] | False |
| B1 | AVG(i."Total Cholesterol (mmol/L)") | [{"table": "health_checkup_indicators", "column": "Total Cholesterol (mmol/L)"}] | [] | False |
| B1 | AVG(i."Lipoprotein (mmol/L)") | [{"table": "health_checkup_indicators", "column": "Lipoprotein (mmol/L)"}] | [] | False |
| B1 | AVG(i."Triglycerides (mmol/L)") | [{"table": "health_checkup_indicators", "column": "Triglycerides (mmol/L)"}] | [] | False |
| B1 | AVG(i."Uric Acid (umol/L)") | [{"table": "health_checkup_indicators", "column": "Uric Acid (umol/L)"}] | [] | False |
| B1 | AVG(i."Blood Urea Nitrogen (mmol/L)") | [{"table": "health_checkup_indicators", "column": "Blood Urea Nitrogen (mmol/L)"}] | [] | False |
| B1 | AVG(i."Alanine Aminotransferase (U/L)") | [{"table": "health_checkup_indicators", "column": "Alanine Aminotransferase (U/L)"}] | [] | False |
| B1 | AVG(i."Serum Potassium (mmol/L)") | [{"table": "health_checkup_indicators", "column": "Serum Potassium (mmol/L)"}] | [] | False |


## S14

类别 `data`；来源 `query_db`；调用 `b05d828e11ba4ba48038fc64217761e9`；状态 `failed`。

```sql
SELECT
  s."Medical history",
  ROUND(AVG(i."Blood Pressure (Systolic)"),2) AS sbp_mean,
  ROUND(stdev(i."Blood Pressure (Systolic)"),2) AS sbp_std,
  ROUND(AVG(i."Blood Pressure (Diastolic)"),2) AS dbp_mean,
  ROUND(stdev(i."Blood Pressure (Diastolic)"),2) AS dbp_std,
  ROUND(AVG(i."Blood Glucose (mmol/L)"),2) AS glucose_mean,
  ROUND(stdev(i."Blood Glucose (mmol/L)"),2) AS glucose_std,
  ROUND(AVG(i."Total Cholesterol (mmol/L)"),2) AS chol_mean,
  ROUND(stdev(i."Total Cholesterol (mmol/L)"),2) AS chol_std,
  ROUND(AVG(i."Triglycerides (mmol/L)"),2) AS tg_mean,
  ROUND(stdev(i."Triglycerides (mmol/L)"),2) AS tg_std,
  ROUND(AVG(i."Uric Acid (umol/L)"),2) AS uric_mean,
  ROUND(stdev(i."Uric Acid (umol/L)"),2) AS uric_std,
  ROUND(AVG(i."Alanine Aminotransferase (U/L)"),2) AS alt_mean,
  ROUND(stdev(i."Alanine Aminotransferase (U/L)"),2) AS alt_std,
  ROUND(AVG(i."Serum Potassium (mmol/L)"),2) AS k_mean,
  ROUND(stdev(i."Serum Potassium (mmol/L)"),2) AS k_std
FROM health_status s
JOIN health_checkup_indicators i ON s.ID = i.ID
GROUP BY s."Medical history"
ORDER BY s."Medical history"
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-037/attempt-01/sql/S14.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-037/attempt-01/sql/S14.parameters.json)。

错误：`OperationalError('no such function: stdev')`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "s", "kind": "base", "block": null, "base_tables": ["health_status"]}, {"alias": "i", "kind": "base", "block": null, "base_tables": ["health_checkup_indicators"]}] | [{"type": "INNER", "right": "health_checkup_indicators AS i", "on": "s.ID = i.ID", "using": []}] | ["s.\"Medical history\""] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | AVG(i."Blood Pressure (Systolic)") | [{"table": "health_checkup_indicators", "column": "Blood Pressure (Systolic)"}] | [] | False |
| B1 | STDDEV(i."Blood Pressure (Systolic)") | [{"table": "health_checkup_indicators", "column": "Blood Pressure (Systolic)"}] | [] | False |
| B1 | AVG(i."Blood Pressure (Diastolic)") | [{"table": "health_checkup_indicators", "column": "Blood Pressure (Diastolic)"}] | [] | False |
| B1 | STDDEV(i."Blood Pressure (Diastolic)") | [{"table": "health_checkup_indicators", "column": "Blood Pressure (Diastolic)"}] | [] | False |
| B1 | AVG(i."Blood Glucose (mmol/L)") | [{"table": "health_checkup_indicators", "column": "Blood Glucose (mmol/L)"}] | [] | False |
| B1 | STDDEV(i."Blood Glucose (mmol/L)") | [{"table": "health_checkup_indicators", "column": "Blood Glucose (mmol/L)"}] | [] | False |
| B1 | AVG(i."Total Cholesterol (mmol/L)") | [{"table": "health_checkup_indicators", "column": "Total Cholesterol (mmol/L)"}] | [] | False |
| B1 | STDDEV(i."Total Cholesterol (mmol/L)") | [{"table": "health_checkup_indicators", "column": "Total Cholesterol (mmol/L)"}] | [] | False |
| B1 | AVG(i."Triglycerides (mmol/L)") | [{"table": "health_checkup_indicators", "column": "Triglycerides (mmol/L)"}] | [] | False |
| B1 | STDDEV(i."Triglycerides (mmol/L)") | [{"table": "health_checkup_indicators", "column": "Triglycerides (mmol/L)"}] | [] | False |
| B1 | AVG(i."Uric Acid (umol/L)") | [{"table": "health_checkup_indicators", "column": "Uric Acid (umol/L)"}] | [] | False |
| B1 | STDDEV(i."Uric Acid (umol/L)") | [{"table": "health_checkup_indicators", "column": "Uric Acid (umol/L)"}] | [] | False |
| B1 | AVG(i."Alanine Aminotransferase (U/L)") | [{"table": "health_checkup_indicators", "column": "Alanine Aminotransferase (U/L)"}] | [] | False |
| B1 | STDDEV(i."Alanine Aminotransferase (U/L)") | [{"table": "health_checkup_indicators", "column": "Alanine Aminotransferase (U/L)"}] | [] | False |
| B1 | AVG(i."Serum Potassium (mmol/L)") | [{"table": "health_checkup_indicators", "column": "Serum Potassium (mmol/L)"}] | [] | False |
| B1 | STDDEV(i."Serum Potassium (mmol/L)") | [{"table": "health_checkup_indicators", "column": "Serum Potassium (mmol/L)"}] | [] | False |


## S15

类别 `data`；来源 `query_db`；调用 `8a018f2313f64f3f9bfaa0152902144e`；状态 `success`。

```sql
SELECT
  s."Medical history",
  ROUND(AVG(i."Blood Pressure (Systolic)"),2) AS sbp_mean,
  ROUND(SQRT(AVG(i."Blood Pressure (Systolic)"*i."Blood Pressure (Systolic)") - AVG(i."Blood Pressure (Systolic)")*AVG(i."Blood Pressure (Systolic)")),2) AS sbp_std,
  ROUND(AVG(i."Blood Pressure (Diastolic)"),2) AS dbp_mean,
  ROUND(SQRT(AVG(i."Blood Pressure (Diastolic)"*i."Blood Pressure (Diastolic)") - AVG(i."Blood Pressure (Diastolic)")*AVG(i."Blood Pressure (Diastolic)")),2) AS dbp_std,
  ROUND(AVG(i."Blood Glucose (mmol/L)"),2) AS glucose_mean,
  ROUND(SQRT(AVG(i."Blood Glucose (mmol/L)"*i."Blood Glucose (mmol/L)") - AVG(i."Blood Glucose (mmol/L)")*AVG(i."Blood Glucose (mmol/L)")),2) AS glucose_std,
  ROUND(AVG(i."Total Cholesterol (mmol/L)"),2) AS chol_mean,
  ROUND(SQRT(AVG(i."Total Cholesterol (mmol/L)"*i."Total Cholesterol (mmol/L)") - AVG(i."Total Cholesterol (mmol/L)")*AVG(i."Total Cholesterol (mmol/L)")),2) AS chol_std,
  ROUND(AVG(i."Triglycerides (mmol/L)"),2) AS tg_mean,
  ROUND(SQRT(AVG(i."Triglycerides (mmol/L)"*i."Triglycerides (mmol/L)") - AVG(i."Triglycerides (mmol/L)")*AVG(i."Triglycerides (mmol/L)")),2) AS tg_std,
  ROUND(AVG(i."Uric Acid (umol/L)"),2) AS uric_mean,
  ROUND(SQRT(AVG(i."Uric Acid (umol/L)"*i."Uric Acid (umol/L)") - AVG(i."Uric Acid (umol/L)")*AVG(i."Uric Acid (umol/L)")),2) AS uric_std,
  ROUND(AVG(i."Alanine Aminotransferase (U/L)"),2) AS alt_mean,
  ROUND(SQRT(AVG(i."Alanine Aminotransferase (U/L)"*i."Alanine Aminotransferase (U/L)") - AVG(i."Alanine Aminotransferase (U/L)")*AVG(i."Alanine Aminotransferase (U/L)")),2) AS alt_std
FROM health_status s
JOIN health_checkup_indicators i ON s.ID = i.ID
GROUP BY s."Medical history"
ORDER BY s."Medical history"
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-037/attempt-01/sql/S15.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-037/attempt-01/sql/S15.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-037/attempt-01/results/S15.rows.jsonl)；完整：True；SHA256：`ca28b0947a6f58eebab3d6fc111a5d8a06f8b1c2b7beb1b46aa97b39f1bb94a6`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "s", "kind": "base", "block": null, "base_tables": ["health_status"]}, {"alias": "i", "kind": "base", "block": null, "base_tables": ["health_checkup_indicators"]}] | [{"type": "INNER", "right": "health_checkup_indicators AS i", "on": "s.ID = i.ID", "using": []}] | ["s.\"Medical history\""] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | AVG(i."Blood Pressure (Systolic)") | [{"table": "health_checkup_indicators", "column": "Blood Pressure (Systolic)"}] | [] | False |
| B1 | AVG(i."Blood Pressure (Diastolic)") | [{"table": "health_checkup_indicators", "column": "Blood Pressure (Diastolic)"}] | [] | False |
| B1 | AVG(i."Blood Glucose (mmol/L)") | [{"table": "health_checkup_indicators", "column": "Blood Glucose (mmol/L)"}] | [] | False |
| B1 | AVG(i."Total Cholesterol (mmol/L)") | [{"table": "health_checkup_indicators", "column": "Total Cholesterol (mmol/L)"}] | [] | False |
| B1 | AVG(i."Triglycerides (mmol/L)") | [{"table": "health_checkup_indicators", "column": "Triglycerides (mmol/L)"}] | [] | False |
| B1 | AVG(i."Uric Acid (umol/L)") | [{"table": "health_checkup_indicators", "column": "Uric Acid (umol/L)"}] | [] | False |
| B1 | AVG(i."Alanine Aminotransferase (U/L)") | [{"table": "health_checkup_indicators", "column": "Alanine Aminotransferase (U/L)"}] | [] | False |
| B1 | AVG(i."Blood Pressure (Systolic)" * i."Blood Pressure (Systolic)") | [{"table": "health_checkup_indicators", "column": "Blood Pressure (Systolic)"}, {"table": "health_checkup_indicators", "column": "Blood Pressure (Systolic)"}] | [] | False |
| B1 | AVG(i."Blood Pressure (Diastolic)" * i."Blood Pressure (Diastolic)") | [{"table": "health_checkup_indicators", "column": "Blood Pressure (Diastolic)"}, {"table": "health_checkup_indicators", "column": "Blood Pressure (Diastolic)"}] | [] | False |
| B1 | AVG(i."Blood Glucose (mmol/L)" * i."Blood Glucose (mmol/L)") | [{"table": "health_checkup_indicators", "column": "Blood Glucose (mmol/L)"}, {"table": "health_checkup_indicators", "column": "Blood Glucose (mmol/L)"}] | [] | False |
| B1 | AVG(i."Total Cholesterol (mmol/L)" * i."Total Cholesterol (mmol/L)") | [{"table": "health_checkup_indicators", "column": "Total Cholesterol (mmol/L)"}, {"table": "health_checkup_indicators", "column": "Total Cholesterol (mmol/L)"}] | [] | False |
| B1 | AVG(i."Triglycerides (mmol/L)" * i."Triglycerides (mmol/L)") | [{"table": "health_checkup_indicators", "column": "Triglycerides (mmol/L)"}, {"table": "health_checkup_indicators", "column": "Triglycerides (mmol/L)"}] | [] | False |
| B1 | AVG(i."Uric Acid (umol/L)" * i."Uric Acid (umol/L)") | [{"table": "health_checkup_indicators", "column": "Uric Acid (umol/L)"}, {"table": "health_checkup_indicators", "column": "Uric Acid (umol/L)"}] | [] | False |
| B1 | AVG(i."Alanine Aminotransferase (U/L)" * i."Alanine Aminotransferase (U/L)") | [{"table": "health_checkup_indicators", "column": "Alanine Aminotransferase (U/L)"}, {"table": "health_checkup_indicators", "column": "Alanine Aminotransferase (U/L)"}] | [] | False |
| B1 | AVG(i."Blood Pressure (Systolic)") | [{"table": "health_checkup_indicators", "column": "Blood Pressure (Systolic)"}] | [] | False |
| B1 | AVG(i."Blood Pressure (Systolic)") | [{"table": "health_checkup_indicators", "column": "Blood Pressure (Systolic)"}] | [] | False |
| B1 | AVG(i."Blood Pressure (Diastolic)") | [{"table": "health_checkup_indicators", "column": "Blood Pressure (Diastolic)"}] | [] | False |
| B1 | AVG(i."Blood Pressure (Diastolic)") | [{"table": "health_checkup_indicators", "column": "Blood Pressure (Diastolic)"}] | [] | False |
| B1 | AVG(i."Blood Glucose (mmol/L)") | [{"table": "health_checkup_indicators", "column": "Blood Glucose (mmol/L)"}] | [] | False |
| B1 | AVG(i."Blood Glucose (mmol/L)") | [{"table": "health_checkup_indicators", "column": "Blood Glucose (mmol/L)"}] | [] | False |
| B1 | AVG(i."Total Cholesterol (mmol/L)") | [{"table": "health_checkup_indicators", "column": "Total Cholesterol (mmol/L)"}] | [] | False |
| B1 | AVG(i."Total Cholesterol (mmol/L)") | [{"table": "health_checkup_indicators", "column": "Total Cholesterol (mmol/L)"}] | [] | False |
| B1 | AVG(i."Triglycerides (mmol/L)") | [{"table": "health_checkup_indicators", "column": "Triglycerides (mmol/L)"}] | [] | False |
| B1 | AVG(i."Triglycerides (mmol/L)") | [{"table": "health_checkup_indicators", "column": "Triglycerides (mmol/L)"}] | [] | False |
| B1 | AVG(i."Uric Acid (umol/L)") | [{"table": "health_checkup_indicators", "column": "Uric Acid (umol/L)"}] | [] | False |
| B1 | AVG(i."Uric Acid (umol/L)") | [{"table": "health_checkup_indicators", "column": "Uric Acid (umol/L)"}] | [] | False |
| B1 | AVG(i."Alanine Aminotransferase (U/L)") | [{"table": "health_checkup_indicators", "column": "Alanine Aminotransferase (U/L)"}] | [] | False |
| B1 | AVG(i."Alanine Aminotransferase (U/L)") | [{"table": "health_checkup_indicators", "column": "Alanine Aminotransferase (U/L)"}] | [] | False |


## S16

类别 `data`；来源 `query_db`；调用 `da202299b4d14ec695886eb25ebda78d`；状态 `success`。

```sql
SELECT
  s."Medical history",
  MIN(i."Blood Pressure (Systolic)") AS sbp_min,
  MAX(i."Blood Pressure (Systolic)") AS sbp_max,
  MIN(i."Blood Pressure (Diastolic)") AS dbp_min,
  MAX(i."Blood Pressure (Diastolic)") AS dbp_max,
  MIN(i."Blood Glucose (mmol/L)") AS glu_min,
  MAX(i."Blood Glucose (mmol/L)") AS glu_max,
  MIN(i."Serum Potassium (mmol/L)") AS k_min,
  MAX(i."Serum Potassium (mmol/L)") AS k_max
FROM health_status s
JOIN health_checkup_indicators i ON s.ID = i.ID
GROUP BY s."Medical history"
ORDER BY s."Medical history"
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-037/attempt-01/sql/S16.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-037/attempt-01/sql/S16.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-037/attempt-01/results/S16.rows.jsonl)；完整：True；SHA256：`a7aaad8e31462c2a11773a60f2c2879b828b7248b3182964c99239fb0feb2247`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "s", "kind": "base", "block": null, "base_tables": ["health_status"]}, {"alias": "i", "kind": "base", "block": null, "base_tables": ["health_checkup_indicators"]}] | [{"type": "INNER", "right": "health_checkup_indicators AS i", "on": "s.ID = i.ID", "using": []}] | ["s.\"Medical history\""] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | MIN(i."Blood Pressure (Systolic)") | [{"table": "health_checkup_indicators", "column": "Blood Pressure (Systolic)"}] | [] | False |
| B1 | MAX(i."Blood Pressure (Systolic)") | [{"table": "health_checkup_indicators", "column": "Blood Pressure (Systolic)"}] | [] | False |
| B1 | MIN(i."Blood Pressure (Diastolic)") | [{"table": "health_checkup_indicators", "column": "Blood Pressure (Diastolic)"}] | [] | False |
| B1 | MAX(i."Blood Pressure (Diastolic)") | [{"table": "health_checkup_indicators", "column": "Blood Pressure (Diastolic)"}] | [] | False |
| B1 | MIN(i."Blood Glucose (mmol/L)") | [{"table": "health_checkup_indicators", "column": "Blood Glucose (mmol/L)"}] | [] | False |
| B1 | MAX(i."Blood Glucose (mmol/L)") | [{"table": "health_checkup_indicators", "column": "Blood Glucose (mmol/L)"}] | [] | False |
| B1 | MIN(i."Serum Potassium (mmol/L)") | [{"table": "health_checkup_indicators", "column": "Serum Potassium (mmol/L)"}] | [] | False |
| B1 | MAX(i."Serum Potassium (mmol/L)") | [{"table": "health_checkup_indicators", "column": "Serum Potassium (mmol/L)"}] | [] | False |


## S17

类别 `data`；来源 `query_db`；调用 `7fd2bfe366974d34a2b5ac0ee0bbf083`；状态 `success`。

```sql
SELECT
  s."Medical history",
  s."Health status",
  COUNT(*) AS n
FROM health_status s
JOIN health_checkup_indicators i ON s.ID = i.ID
GROUP BY s."Medical history", s."Health status"
ORDER BY s."Medical history", s."Health status"
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-037/attempt-01/sql/S17.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-037/attempt-01/sql/S17.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-037/attempt-01/results/S17.rows.jsonl)；完整：True；SHA256：`e4c9e58a007385a128e981c92037ba87ad16f4a51c1a1fb4e5ec0ed9f30e6a1c`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "s", "kind": "base", "block": null, "base_tables": ["health_status"]}, {"alias": "i", "kind": "base", "block": null, "base_tables": ["health_checkup_indicators"]}] | [{"type": "INNER", "right": "health_checkup_indicators AS i", "on": "s.ID = i.ID", "using": []}] | ["s.\"Medical history\"", "s.\"Health status\""] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |


## S18

类别 `data`；来源 `query_db`；调用 `97d9443741154136b63110dc8f8475d0`；状态 `success`。

```sql
SELECT
  s."Medical history",
  s."Health status",
  COUNT(*) AS n
FROM health_status s
WHERE s."Medical history" = 'None'
GROUP BY s."Medical history", s."Health status"
ORDER BY s."Medical history", s."Health status"
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-037/attempt-01/sql/S18.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-037/attempt-01/sql/S18.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-037/attempt-01/results/S18.rows.jsonl)；完整：True；SHA256：`2da0534d210f0d55aaaab03f79d89edddf75e1881353f52e8a31154f31595c22`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "s", "kind": "base", "block": null, "base_tables": ["health_status"]}] | [] | ["s.\"Medical history\"", "s.\"Health status\""] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |


## S19

类别 `data`；来源 `query_db`；调用 `ae4a2b3aa09849a4b9ebebc5660081c0`；状态 `success`。

```sql
SELECT
  s."Medical history",
  ROUND(AVG(i."Age"),2) AS age_mean,
  ROUND(AVG(i."Weight (kg)"),2) AS weight_mean,
  ROUND(AVG(i."Heart Rate (bpm)"),2) AS hr_mean
FROM health_status s
JOIN health_checkup_indicators i ON s.ID = i.ID
GROUP BY s."Medical history"
ORDER BY s."Medical history"
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-037/attempt-01/sql/S19.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-037/attempt-01/sql/S19.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-037/attempt-01/results/S19.rows.jsonl)；完整：True；SHA256：`630967f656c3c6d10dfc190ea411aaaeeca661ae4a998b23df67de70f88b8e26`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "s", "kind": "base", "block": null, "base_tables": ["health_status"]}, {"alias": "i", "kind": "base", "block": null, "base_tables": ["health_checkup_indicators"]}] | [{"type": "INNER", "right": "health_checkup_indicators AS i", "on": "s.ID = i.ID", "using": []}] | ["s.\"Medical history\""] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | AVG(i."Age") | [{"table": "health_checkup_indicators", "column": "Age"}] | [] | False |
| B1 | AVG(i."Weight (kg)") | [{"table": "health_checkup_indicators", "column": "Weight (kg)"}] | [] | False |
| B1 | AVG(i."Heart Rate (bpm)") | [{"table": "health_checkup_indicators", "column": "Heart Rate (bpm)"}] | [] | False |


## S20

类别 `data`；来源 `python`；调用 `6358c574de664176b00654729c4d73f2`；状态 `success`。

```sql

SELECT s."Medical history" AS medhx,
  i.Age, i."Height (cm)" AS height, i."Weight (kg)" AS weight,
  i."Blood Pressure (Systolic)" AS sbp, i."Blood Pressure (Diastolic)" AS dbp,
  i."Heart Rate (bpm)" AS hr, i."Respiratory Rate (breaths/min)" AS rr,
  i."Blood Oxygen Saturation (%)" AS spo2, i."Blood Glucose (mmol/L)" AS glucose,
  i."Total Cholesterol (mmol/L)" AS chol, i."Lipoprotein (mmol/L)" AS lipo,
  i."Triglycerides (mmol/L)" AS tg, i."Uric Acid (umol/L)" AS uric,
  i."Blood Urea Nitrogen (mmol/L)" AS bun, i."Alanine Aminotransferase (U/L)" AS alt,
  i."Serum Potassium (mmol/L)" AS k
FROM health_status s JOIN health_checkup_indicators i ON s.ID = i.ID

```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-037/attempt-01/sql/S20.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-037/attempt-01/sql/S20.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-037/attempt-01/results/S20.rows.jsonl)；完整：True；SHA256：`8d3da52205da7159f9721173b7c9835aa579b264ab03c6f6b552406100e4fb19`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "s", "kind": "base", "block": null, "base_tables": ["health_status"]}, {"alias": "i", "kind": "base", "block": null, "base_tables": ["health_checkup_indicators"]}] | [{"type": "INNER", "right": "health_checkup_indicators AS i", "on": "s.ID = i.ID", "using": []}] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |


## S21

类别 `data`；来源 `python`；调用 `6b1bc79d4de84452ae9e739e8ac6a033`；状态 `success`。

```sql

SELECT s."Medical history" AS medhx,
  i.Age, i."Height (cm)" AS height, i."Weight (kg)" AS weight,
  i."Blood Pressure (Systolic)" AS sbp, i."Blood Pressure (Diastolic)" AS dbp,
  i."Heart Rate (bpm)" AS hr, i."Respiratory Rate (breaths/min)" AS rr,
  i."Blood Oxygen Saturation (%)" AS spo2, i."Blood Glucose (mmol/L)" AS glucose,
  i."Total Cholesterol (mmol/L)" AS chol, i."Lipoprotein (mmol/L)" AS lipo,
  i."Triglycerides (mmol/L)" AS tg, i."Uric Acid (umol/L)" AS uric,
  i."Blood Urea Nitrogen (mmol/L)" AS bun, i."Alanine Aminotransferase (U/L)" AS alt,
  i."Serum Potassium (mmol/L)" AS k
FROM health_status s JOIN health_checkup_indicators i ON s.ID = i.ID

```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-037/attempt-01/sql/S21.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-037/attempt-01/sql/S21.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-037/attempt-01/results/S21.rows.jsonl)；完整：True；SHA256：`8d3da52205da7159f9721173b7c9835aa579b264ab03c6f6b552406100e4fb19`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "s", "kind": "base", "block": null, "base_tables": ["health_status"]}, {"alias": "i", "kind": "base", "block": null, "base_tables": ["health_checkup_indicators"]}] | [{"type": "INNER", "right": "health_checkup_indicators AS i", "on": "s.ID = i.ID", "using": []}] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |


## S22

类别 `data`；来源 `python`；调用 `c5cb07b77e7341c4ad5077d8d061f7f9`；状态 `success`。

```sql

SELECT s."Medical history" AS medhx,
  i.Age, i."Height (cm)" AS height, i."Weight (kg)" AS weight,
  i."Blood Pressure (Systolic)" AS sbp, i."Blood Pressure (Diastolic)" AS dbp,
  i."Heart Rate (bpm)" AS hr, i."Respiratory Rate (breaths/min)" AS rr,
  i."Blood Oxygen Saturation (%)" AS spo2, i."Blood Glucose (mmol/L)" AS glucose,
  i."Total Cholesterol (mmol/L)" AS chol, i."Lipoprotein (mmol/L)" AS lipo,
  i."Triglycerides (mmol/L)" AS tg, i."Uric Acid (umol/L)" AS uric,
  i."Blood Urea Nitrogen (mmol/L)" AS bun, i."Alanine Aminotransferase (U/L)" AS alt,
  i."Serum Potassium (mmol/L)" AS k
FROM health_status s JOIN health_checkup_indicators i ON s.ID = i.ID

```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-037/attempt-01/sql/S22.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-037/attempt-01/sql/S22.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-037/attempt-01/results/S22.rows.jsonl)；完整：True；SHA256：`8d3da52205da7159f9721173b7c9835aa579b264ab03c6f6b552406100e4fb19`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "s", "kind": "base", "block": null, "base_tables": ["health_status"]}, {"alias": "i", "kind": "base", "block": null, "base_tables": ["health_checkup_indicators"]}] | [{"type": "INNER", "right": "health_checkup_indicators AS i", "on": "s.ID = i.ID", "using": []}] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |


## S23

类别 `data`；来源 `python`；调用 `73bba6f38bb246afa649dd142c9c5df8`；状态 `success`。

```sql

SELECT s."Medical history" AS medhx,
  i.Age, i."Height (cm)" AS height, i."Weight (kg)" AS weight,
  i."Blood Pressure (Systolic)" AS sbp, i."Blood Pressure (Diastolic)" AS dbp,
  i."Lipoprotein (mmol/L)" AS lipo
FROM health_status s JOIN health_checkup_indicators i ON s.ID = i.ID

```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-037/attempt-01/sql/S23.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-037/attempt-01/sql/S23.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-037/attempt-01/results/S23.rows.jsonl)；完整：True；SHA256：`1506a5d7a25cea00c9d362d7b08ae21926bc5b888e5c71d1b4a30cb24197f66f`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "s", "kind": "base", "block": null, "base_tables": ["health_status"]}, {"alias": "i", "kind": "base", "block": null, "base_tables": ["health_checkup_indicators"]}] | [{"type": "INNER", "right": "health_checkup_indicators AS i", "on": "s.ID = i.ID", "using": []}] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |


## S24

类别 `data`；来源 `python`；调用 `ffbb7c5525034ea1824634156b779b42`；状态 `success`。

```sql

SELECT s."Medical history" AS medhx,
  i."Weight (kg)" AS weight,
  i."Blood Pressure (Systolic)" AS sbp, i."Blood Pressure (Diastolic)" AS dbp,
  i."Lipoprotein (mmol/L)" AS lipo
FROM health_status s JOIN health_checkup_indicators i ON s.ID = i.ID

```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-037/attempt-01/sql/S24.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-037/attempt-01/sql/S24.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-037/attempt-01/results/S24.rows.jsonl)；完整：True；SHA256：`665218b9351a670b837ec61313fc8ecf8258b9d200a84ab5e1c7f67e6f9ae8f4`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "s", "kind": "base", "block": null, "base_tables": ["health_status"]}, {"alias": "i", "kind": "base", "block": null, "base_tables": ["health_checkup_indicators"]}] | [{"type": "INNER", "right": "health_checkup_indicators AS i", "on": "s.ID = i.ID", "using": []}] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |


## S25

类别 `data`；来源 `query_db`；调用 `a3a934525d024863a89850ae75d2dd97`；状态 `success`。

```sql
SELECT "Medical history", "Smoking status", COUNT(*) AS n
FROM health_status
GROUP BY "Medical history", "Smoking status"
ORDER BY "Medical history", "Smoking status"
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-037/attempt-01/sql/S25.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-037/attempt-01/sql/S25.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-037/attempt-01/results/S25.rows.jsonl)；完整：True；SHA256：`659930da05c67dc49f1c9a677d73fed5064b3c54f7da593490b9e3bc7225dbf4`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "health_status", "kind": "base", "block": null, "base_tables": ["health_status"]}] | [] | ["\"Medical history\"", "\"Smoking status\""] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |


## S26

类别 `data`；来源 `query_db`；调用 `83cdc88333cf4799a27f0f69e62bc677`；状态 `success`。

```sql
SELECT "Medical history", "Drinking Status", COUNT(*) AS n
FROM health_status
GROUP BY "Medical history", "Drinking Status"
ORDER BY "Medical history", "Drinking Status"
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-037/attempt-01/sql/S26.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-037/attempt-01/sql/S26.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-037/attempt-01/results/S26.rows.jsonl)；完整：True；SHA256：`3639273c7ac6d9ce231c3b871287e9e261af90554ec659596a5f1991ac1deed4`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "health_status", "kind": "base", "block": null, "base_tables": ["health_status"]}] | [] | ["\"Medical history\"", "\"Drinking Status\""] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |


## S27

类别 `data`；来源 `python`；调用 `238edbcbbe9541958e83f256b7a0a8f6`；状态 `success`。

```sql

SELECT s."Medical history" AS medhx,
  i.Age, i."Height (cm)" AS height, i."Weight (kg)" AS weight,
  i."Blood Pressure (Systolic)" AS sbp, i."Blood Pressure (Diastolic)" AS dbp,
  i."Heart Rate (bpm)" AS hr, i."Respiratory Rate (breaths/min)" AS rr,
  i."Blood Oxygen Saturation (%)" AS spo2, i."Blood Glucose (mmol/L)" AS glucose,
  i."Total Cholesterol (mmol/L)" AS chol, i."Lipoprotein (mmol/L)" AS lipo,
  i."Triglycerides (mmol/L)" AS tg, i."Uric Acid (umol/L)" AS uric,
  i."Blood Urea Nitrogen (mmol/L)" AS bun, i."Alanine Aminotransferase (U/L)" AS alt,
  i."Serum Potassium (mmol/L)" AS k
FROM health_status s JOIN health_checkup_indicators i ON s.ID = i.ID

```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-037/attempt-01/sql/S27.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-037/attempt-01/sql/S27.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-037/attempt-01/results/S27.rows.jsonl)；完整：True；SHA256：`8d3da52205da7159f9721173b7c9835aa579b264ab03c6f6b552406100e4fb19`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "s", "kind": "base", "block": null, "base_tables": ["health_status"]}, {"alias": "i", "kind": "base", "block": null, "base_tables": ["health_checkup_indicators"]}] | [{"type": "INNER", "right": "health_checkup_indicators AS i", "on": "s.ID = i.ID", "using": []}] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |


## S28

类别 `data`；来源 `python`；调用 `238edbcbbe9541958e83f256b7a0a8f6`；状态 `success`。

```sql

SELECT s."Medical history" AS medhx, i.Gender, i."Weight (kg)" AS weight
FROM health_status s JOIN health_checkup_indicators i ON s.ID = i.ID

```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-037/attempt-01/sql/S28.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-037/attempt-01/sql/S28.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-037/attempt-01/results/S28.rows.jsonl)；完整：True；SHA256：`c607312aab230a123110362654df3c248da5d1b09be7deab2ee666402ac679e6`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "s", "kind": "base", "block": null, "base_tables": ["health_status"]}, {"alias": "i", "kind": "base", "block": null, "base_tables": ["health_checkup_indicators"]}] | [{"type": "INNER", "right": "health_checkup_indicators AS i", "on": "s.ID = i.ID", "using": []}] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |


## S29

类别 `data`；来源 `python`；调用 `67837830536f417aba5842e2aea98170`；状态 `success`。

```sql

SELECT s."Medical history" AS medhx, i.Gender,
  ROUND(AVG(i."Blood Pressure (Systolic)"),2) AS sbp_mean,
  ROUND(AVG(i."Blood Pressure (Diastolic)"),2) AS dbp_mean
FROM health_status s JOIN health_checkup_indicators i ON s.ID = i.ID
GROUP BY s."Medical history", i.Gender
ORDER BY s."Medical history", i.Gender

```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-037/attempt-01/sql/S29.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-037/attempt-01/sql/S29.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-037/attempt-01/results/S29.rows.jsonl)；完整：True；SHA256：`4581adff1b99f52fed59c4fdc8894d481752dbd1abefb7eae44bd7e6fc36dcee`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "s", "kind": "base", "block": null, "base_tables": ["health_status"]}, {"alias": "i", "kind": "base", "block": null, "base_tables": ["health_checkup_indicators"]}] | [{"type": "INNER", "right": "health_checkup_indicators AS i", "on": "s.ID = i.ID", "using": []}] | ["s.\"Medical history\"", "i.Gender"] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | AVG(i."Blood Pressure (Systolic)") | [{"table": "health_checkup_indicators", "column": "Blood Pressure (Systolic)"}] | [] | False |
| B1 | AVG(i."Blood Pressure (Diastolic)") | [{"table": "health_checkup_indicators", "column": "Blood Pressure (Diastolic)"}] | [] | False |


## S30

类别 `data`；来源 `python`；调用 `67837830536f417aba5842e2aea98170`；状态 `success`。

```sql
SELECT COUNT(*) AS total FROM health_checkup_indicators
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-037/attempt-01/sql/S30.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-037/attempt-01/sql/S30.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-037/attempt-01/results/S30.rows.jsonl)；完整：True；SHA256：`3006a434a2e10651d91445b941a2785d48c87aa2797ad73c00b0211e7613fa85`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "health_checkup_indicators", "kind": "base", "block": null, "base_tables": ["health_checkup_indicators"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |


## S31

类别 `data`；来源 `python`；调用 `67837830536f417aba5842e2aea98170`；状态 `success`。

```sql

SELECT
  SUM(CASE WHEN Age IS NULL THEN 1 ELSE 0 END) AS age_null,
  SUM(CASE WHEN "Weight (kg)" IS NULL THEN 1 ELSE 0 END) AS weight_null,
  SUM(CASE WHEN "Blood Pressure (Systolic)" IS NULL THEN 1 ELSE 0 END) AS sbp_null,
  SUM(CASE WHEN "Blood Glucose (mmol/L)" IS NULL THEN 1 ELSE 0 END) AS glu_null
FROM health_checkup_indicators

```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-037/attempt-01/sql/S31.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-037/attempt-01/sql/S31.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-037/attempt-01/results/S31.rows.jsonl)；完整：True；SHA256：`3aa57daa28e035a2491b638cf239f8764af7c73d723f3574fda809410ca00fcb`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "health_checkup_indicators", "kind": "base", "block": null, "base_tables": ["health_checkup_indicators"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | SUM(CASE WHEN Age IS NULL THEN 1 ELSE 0 END) | [] | [{"table": "health_checkup_indicators", "column": "Age"}] | False |
| B1 | SUM(CASE WHEN "Weight (kg)" IS NULL THEN 1 ELSE 0 END) | [] | [{"table": "health_checkup_indicators", "column": "Weight (kg)"}] | False |
| B1 | SUM(CASE WHEN "Blood Pressure (Systolic)" IS NULL THEN 1 ELSE 0 END) | [] | [{"table": "health_checkup_indicators", "column": "Blood Pressure (Systolic)"}] | False |
| B1 | SUM(CASE WHEN "Blood Glucose (mmol/L)" IS NULL THEN 1 ELSE 0 END) | [] | [{"table": "health_checkup_indicators", "column": "Blood Glucose (mmol/L)"}] | False |


## S32

类别 `data`；来源 `python`；调用 `67837830536f417aba5842e2aea98170`；状态 `success`。

```sql

SELECT
  SUM(CASE WHEN "Medical history" IS NULL THEN 1 ELSE 0 END) AS mhx_null,
  SUM(CASE WHEN "Health status" IS NULL THEN 1 ELSE 0 END) AS hs_null,
  SUM(CASE WHEN ID IS NULL THEN 1 ELSE 0 END) AS id_null
FROM health_status

```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-037/attempt-01/sql/S32.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-037/attempt-01/sql/S32.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-037/attempt-01/results/S32.rows.jsonl)；完整：True；SHA256：`32d31f8e37e0790192e2811106c2a3ade88b6cf0ce7061c37a5147424bbcee3c`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "health_status", "kind": "base", "block": null, "base_tables": ["health_status"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | SUM(CASE WHEN "Medical history" IS NULL THEN 1 ELSE 0 END) | [] | [{"table": "health_status", "column": "Medical history"}] | False |
| B1 | SUM(CASE WHEN "Health status" IS NULL THEN 1 ELSE 0 END) | [] | [{"table": "health_status", "column": "Health status"}] | False |
| B1 | SUM(CASE WHEN ID IS NULL THEN 1 ELSE 0 END) | [] | [{"table": "health_status", "column": "ID"}] | False |


## S33

类别 `data`；来源 `query_db`；调用 `33090ffe4de94a37b9dca2027ef94bac`；状态 `success`。

```sql
SELECT
  s."Medical history",
  COUNT(*) AS n,
  ROUND(100.0*SUM(CASE WHEN i."Blood Pressure (Systolic)" >= 130 OR i."Blood Pressure (Diastolic)" >= 85 THEN 1 ELSE 0 END)/COUNT(*),1) AS pct_elevated_bp,
  ROUND(100.0*SUM(CASE WHEN i."Blood Pressure (Systolic)" >= 140 OR i."Blood Pressure (Diastolic)" >= 90 THEN 1 ELSE 0 END)/COUNT(*),1) AS pct_high_bp,
  ROUND(100.0*SUM(CASE WHEN i."Weight (kg)" >= 75 THEN 1 ELSE 0 END)/COUNT(*),1) AS pct_wt_ge75,
  ROUND(100.0*SUM(CASE WHEN i."Blood Glucose (mmol/L)" >= 5.6 THEN 1 ELSE 0 END)/COUNT(*),1) AS pct_glu_ge5_6,
  ROUND(100.0*SUM(CASE WHEN i."Alanine Aminotransferase (U/L)" >= 40 THEN 1 ELSE 0 END)/COUNT(*),1) AS pct_alt_ge40
FROM health_status s
JOIN health_checkup_indicators i ON s.ID = i.ID
GROUP BY s."Medical history"
ORDER BY s."Medical history"
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-037/attempt-01/sql/S33.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-037/attempt-01/sql/S33.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-037/attempt-01/results/S33.rows.jsonl)；完整：True；SHA256：`dd49869af7182370b0255fdd1fb89c9b3e703232acd8cc8ca8bb07e200958cc8`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "s", "kind": "base", "block": null, "base_tables": ["health_status"]}, {"alias": "i", "kind": "base", "block": null, "base_tables": ["health_checkup_indicators"]}] | [{"type": "INNER", "right": "health_checkup_indicators AS i", "on": "s.ID = i.ID", "using": []}] | ["s.\"Medical history\""] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |
| B1 | COUNT(*) | [] | [] | True |
| B1 | COUNT(*) | [] | [] | True |
| B1 | COUNT(*) | [] | [] | True |
| B1 | COUNT(*) | [] | [] | True |
| B1 | COUNT(*) | [] | [] | True |
| B1 | SUM(CASE WHEN i."Blood Pressure (Systolic)" >= 130 OR i."Blood Pressure (Diastolic)" >= 85 THEN 1 ELSE 0 END) | [] | [{"table": "health_checkup_indicators", "column": "Blood Pressure (Systolic)"}, {"table": "health_checkup_indicators", "column": "Blood Pressure (Diastolic)"}] | False |
| B1 | SUM(CASE WHEN i."Blood Pressure (Systolic)" >= 140 OR i."Blood Pressure (Diastolic)" >= 90 THEN 1 ELSE 0 END) | [] | [{"table": "health_checkup_indicators", "column": "Blood Pressure (Systolic)"}, {"table": "health_checkup_indicators", "column": "Blood Pressure (Diastolic)"}] | False |
| B1 | SUM(CASE WHEN i."Weight (kg)" >= 75 THEN 1 ELSE 0 END) | [] | [{"table": "health_checkup_indicators", "column": "Weight (kg)"}] | False |
| B1 | SUM(CASE WHEN i."Blood Glucose (mmol/L)" >= 5.6 THEN 1 ELSE 0 END) | [] | [{"table": "health_checkup_indicators", "column": "Blood Glucose (mmol/L)"}] | False |
| B1 | SUM(CASE WHEN i."Alanine Aminotransferase (U/L)" >= 40 THEN 1 ELSE 0 END) | [] | [{"table": "health_checkup_indicators", "column": "Alanine Aminotransferase (U/L)"}] | False |


## S34

类别 `data`；来源 `python`；调用 `f24afb2b46824c0383eb800002d8f4a3`；状态 `success`。

```sql

SELECT
  s."Medical history" AS medhx,
  COUNT(*) AS n,
  100.0*SUM(CASE WHEN i."Blood Pressure (Systolic)" >= 130 OR i."Blood Pressure (Diastolic)" >= 85 THEN 1 ELSE 0 END)/COUNT(*) AS pct_elev,
  100.0*SUM(CASE WHEN i."Blood Pressure (Systolic)" >= 140 OR i."Blood Pressure (Diastolic)" >= 90 THEN 1 ELSE 0 END)/COUNT(*) AS pct_high
FROM health_status s JOIN health_checkup_indicators i ON s.ID = i.ID
GROUP BY s."Medical history"

```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-037/attempt-01/sql/S34.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-037/attempt-01/sql/S34.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-037/attempt-01/results/S34.rows.jsonl)；完整：True；SHA256：`b447b3f85ac34bc2cd9cc29fda6dbf57ebd88c7c96ce9f528a4f2d00d707c786`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "s", "kind": "base", "block": null, "base_tables": ["health_status"]}, {"alias": "i", "kind": "base", "block": null, "base_tables": ["health_checkup_indicators"]}] | [{"type": "INNER", "right": "health_checkup_indicators AS i", "on": "s.ID = i.ID", "using": []}] | ["s.\"Medical history\""] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |
| B1 | COUNT(*) | [] | [] | True |
| B1 | COUNT(*) | [] | [] | True |
| B1 | SUM(CASE WHEN i."Blood Pressure (Systolic)" >= 130 OR i."Blood Pressure (Diastolic)" >= 85 THEN 1 ELSE 0 END) | [] | [{"table": "health_checkup_indicators", "column": "Blood Pressure (Systolic)"}, {"table": "health_checkup_indicators", "column": "Blood Pressure (Diastolic)"}] | False |
| B1 | SUM(CASE WHEN i."Blood Pressure (Systolic)" >= 140 OR i."Blood Pressure (Diastolic)" >= 90 THEN 1 ELSE 0 END) | [] | [{"table": "health_checkup_indicators", "column": "Blood Pressure (Systolic)"}, {"table": "health_checkup_indicators", "column": "Blood Pressure (Diastolic)"}] | False |


## S35

类别 `data`；来源 `python`；调用 `cff9a1545b3047c78dcd43536f87f4b3`；状态 `success`。

```sql

SELECT
  s."Medical history" AS medhx,
  COUNT(*) AS n,
  100.0*SUM(CASE WHEN i."Blood Pressure (Systolic)" >= 130 OR i."Blood Pressure (Diastolic)" >= 85 THEN 1 ELSE 0 END)/COUNT(*) AS pct_elev,
  100.0*SUM(CASE WHEN i."Blood Pressure (Systolic)" >= 140 OR i."Blood Pressure (Diastolic)" >= 90 THEN 1 ELSE 0 END)/COUNT(*) AS pct_high
FROM health_status s JOIN health_checkup_indicators i ON s.ID = i.ID
GROUP BY s."Medical history"

```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-037/attempt-01/sql/S35.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-037/attempt-01/sql/S35.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-037/attempt-01/results/S35.rows.jsonl)；完整：True；SHA256：`b447b3f85ac34bc2cd9cc29fda6dbf57ebd88c7c96ce9f528a4f2d00d707c786`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "s", "kind": "base", "block": null, "base_tables": ["health_status"]}, {"alias": "i", "kind": "base", "block": null, "base_tables": ["health_checkup_indicators"]}] | [{"type": "INNER", "right": "health_checkup_indicators AS i", "on": "s.ID = i.ID", "using": []}] | ["s.\"Medical history\""] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |
| B1 | COUNT(*) | [] | [] | True |
| B1 | COUNT(*) | [] | [] | True |
| B1 | SUM(CASE WHEN i."Blood Pressure (Systolic)" >= 130 OR i."Blood Pressure (Diastolic)" >= 85 THEN 1 ELSE 0 END) | [] | [{"table": "health_checkup_indicators", "column": "Blood Pressure (Systolic)"}, {"table": "health_checkup_indicators", "column": "Blood Pressure (Diastolic)"}] | False |
| B1 | SUM(CASE WHEN i."Blood Pressure (Systolic)" >= 140 OR i."Blood Pressure (Diastolic)" >= 90 THEN 1 ELSE 0 END) | [] | [{"table": "health_checkup_indicators", "column": "Blood Pressure (Systolic)"}, {"table": "health_checkup_indicators", "column": "Blood Pressure (Diastolic)"}] | False |


## S36

类别 `data`；来源 `python`；调用 `cff9a1545b3047c78dcd43536f87f4b3`；状态 `success`。

```sql

SELECT s."Medical history" AS medhx,
  i.Age, i."Height (cm)" AS height, i."Weight (kg)" AS weight,
  i."Heart Rate (bpm)" AS hr, i."Respiratory Rate (breaths/min)" AS rr,
  i."Blood Oxygen Saturation (%)" AS spo2, i."Blood Glucose (mmol/L)" AS glucose,
  i."Total Cholesterol (mmol/L)" AS chol, i."Lipoprotein (mmol/L)" AS lipo,
  i."Triglycerides (mmol/L)" AS tg, i."Uric Acid (umol/L)" AS uric,
  i."Blood Urea Nitrogen (mmol/L)" AS bun, i."Alanine Aminotransferase (U/L)" AS alt,
  i."Serum Potassium (mmol/L)" AS k
FROM health_status s JOIN health_checkup_indicators i ON s.ID = i.ID

```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-037/attempt-01/sql/S36.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-037/attempt-01/sql/S36.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-037/attempt-01/results/S36.rows.jsonl)；完整：True；SHA256：`4c8a2d7a4375ddfacfd967a8e976149ae8fba526b539b5c6bedd193fa784be1d`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "s", "kind": "base", "block": null, "base_tables": ["health_status"]}, {"alias": "i", "kind": "base", "block": null, "base_tables": ["health_checkup_indicators"]}] | [{"type": "INNER", "right": "health_checkup_indicators AS i", "on": "s.ID = i.ID", "using": []}] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |


## S37

类别 `data`；来源 `python`；调用 `de8104b80dff4bc7a00df3dc419c20b2`；状态 `success`。

```sql

SELECT s."Medical history" AS medhx, s."Health status" AS hs,
  s."Smoking status" AS smoke, s."Drinking Status" AS drink
FROM health_status s JOIN health_checkup_indicators i ON s.ID = i.ID

```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-037/attempt-01/sql/S37.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-037/attempt-01/sql/S37.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-037/attempt-01/results/S37.rows.jsonl)；完整：True；SHA256：`9519283544ebce6c145247e7fda33219e9e988fdf132b10ec30712a622a979d1`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "s", "kind": "base", "block": null, "base_tables": ["health_status"]}, {"alias": "i", "kind": "base", "block": null, "base_tables": ["health_checkup_indicators"]}] | [{"type": "INNER", "right": "health_checkup_indicators AS i", "on": "s.ID = i.ID", "using": []}] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |

