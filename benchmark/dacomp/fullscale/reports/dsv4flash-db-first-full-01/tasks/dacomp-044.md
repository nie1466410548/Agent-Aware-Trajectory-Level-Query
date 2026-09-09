# dacomp-044

Please summarize the health education campaign formats and locations for students that are…

运行：已提交。官方未评分。全部 SQL 尝试/成功 32/32；数据 SQL 30/30；Python 5 次。

完整原题：

Please summarize the health education campaign formats and locations for students that are capable of delivering long-term effectiveness and behavioral improvement.

| 表 | 行数 | 列数 |
| --- | --- | --- |
| basic_medical_record_informatio | 400 | 26 |
| clinical_manifestations | 400 | 20 |
| complication_management | 400 | 18 |
| diagnosis_and_classification | 400 | 18 |
| epidemic_analysis | 400 | 19 |
| epidemiological_investigation | 400 | 13 |
| health_education | 400 | 20 |
| healthcare_resources | 400 | 21 |
| immunization_management | 400 | 28 |
| isolation_and_disinfection | 400 | 19 |


实际路线（分析者依据 SQL/源码概括，不代表 Agent 自述）：筛选学生健康教育活动 → 比较形式与地点的长期/行为效果 → Python 计算效果交集、组比例及检验 → 绘制活动组合对比。

数据库大小：1,613,824 字节。

## 数据 SQL

| SQL | 状态 | 基础表 | Join 输入/类型 | GROUP BY | 聚合表达式 | 结果行数 | 数据库 ms |
| --- | --- | --- | --- | --- | --- | --- | --- |
| [S3/Q1](#s3) | success | ["health_education"] | 0 / {} | [] | [] | 20 | 0.506 |
| [S4/Q2](#s4) | success | ["basic_medical_record_informatio"] | 0 / {} | [] | [] | 3 | 0.508 |
| [S5/Q3](#s5) | success | ["health_education"] | 0 / {} | [] | [] | 5 | 0.681 |
| [S6/Q4](#s6) | success | ["health_education"] | 0 / {} | [] | [] | 3 | 0.41 |
| [S7/Q5](#s7) | success | ["health_education"] | 0 / {} | [] | [] | 3 | 0.421 |
| [S8/Q6](#s8) | success | ["health_education"] | 0 / {} | [] | [] | 3 | 0.493 |
| [S9/Q7](#s9) | success | ["health_education"] | 0 / {} | [] | [] | 3 | 0.403 |
| [S10/Q8](#s10) | success | ["health_education"] | 0 / {} | [] | [] | 3 | 0.429 |
| [S11/Q9](#s11) | success | ["health_education"] | 0 / {} | [] | ["COUNT(*)"] | 1 | 0.305 |
| [S12/Q10](#s12) | success | ["health_education"] | 0 / {} | [] | [] | 75 | 0.792 |
| [S13/Q11](#s13) | success | ["health_education"] | 0 / {} | ["\"Campaign Format (Poster/Video/Lecture)\"", "\"Key Locations (School/Hospital/Community)\""] | ["COUNT(*)", "SUM(CASE WHEN \"Behavioral Change Assessment\" = 'Significant' THEN 1 ELSE 0 END)", "SUM(CASE WHEN \"Effectiveness Tracking\" = 'Significant' THEN 1 ELSE 0 END)", "SUM(CASE WHEN \"Effectiveness Assessment\" = 'Significant' THEN 1 ELSE 0 END)"] | 9 | 0.622 |
| [S14/Q12](#s14) | success | ["health_education"] | 0 / {} | ["\"Campaign Format (Poster/Video/Lecture)\""] | ["COUNT(*)", "SUM(CASE WHEN \"Behavioral Change Assessment\" = 'Significant' THEN 1 ELSE 0 END)", "SUM(CASE WHEN \"Effectiveness Tracking\" = 'Significant' THEN 1 ELSE 0 END)"] | 3 | 0.47 |
| [S15/Q13](#s15) | success | ["health_education"] | 0 / {} | ["\"Campaign Format (Poster/Video/Lecture)\"", "\"Key Locations (School/Hospital/Community)\""] | ["COUNT(*)", "SUM(CASE WHEN \"Behavioral Change Assessment\" = 'Significant' AND \"Effectiveness Tracking\" = 'Significant' THEN 1 ELSE 0 END)"] | 9 | 0.534 |
| [S16/Q14](#s16) | success | ["health_education"] | 0 / {} | ["\"Key Locations (School/Hospital/Community)\""] | ["COUNT(*)", "SUM(CASE WHEN \"Behavioral Change Assessment\" = 'Significant' THEN 1 ELSE 0 END)", "SUM(CASE WHEN \"Effectiveness Tracking\" = 'Significant' THEN 1 ELSE 0 END)", "SUM(CASE WHEN \"Behavioral Change Assessment\" = 'Significant' AND \"Effectiveness Tracking\" = 'Significant' THEN 1 ELSE 0 END)"] | 3 | 0.497 |
| [S17/Q15](#s17) | success | ["health_education"] | 0 / {} | [] | [] | 7 | 0.479 |
| [S18/Q16](#s18) | success | ["health_education"] | 0 / {} | ["\"Campaign Format (Poster/Video/Lecture)\"", "\"Key Locations (School/Hospital/Community)\""] | ["COUNT(*)", "SUM(CASE WHEN \"Behavioral Change Assessment\" = 'Significant' THEN 1 ELSE 0 END)", "SUM(CASE WHEN \"Effectiveness Tracking\" = 'Significant' THEN 1 ELSE 0 END)", "SUM(CASE WHEN \"Behavioral Change Assessment\" = 'Significant' AND \"Effectiveness Tracking\" = 'Significant' THEN 1 ELSE 0 END)", "COUNT(*)", "COUNT(*)", "COUNT(*)", "SUM(CASE WHEN \"Behavioral Change Assessment\" = 'Significant' THEN 1 ELSE 0 END)", "SUM(CASE WHEN \"Effectiveness Tracking\" = 'Significant' THEN 1 ELSE 0 END)", "SUM(CASE WHEN \"Behavioral Change Assessment\" = 'Significant' AND \"Effectiveness Tracking\" = 'Significant' THEN 1 ELSE 0 END)"] | 9 | 0.627 |
| [S19/Q17](#s19) | success | ["health_education"] | 0 / {} | ["\"Campaign Format (Poster/Video/Lecture)\"", "\"Key Locations (School/Hospital/Community)\"", "\"Campaign Content (Prevention/Treatment/Policy)\""] | ["COUNT(*)", "SUM(CASE WHEN \"Behavioral Change Assessment\" = 'Significant' AND \"Effectiveness Tracking\" = 'Significant' THEN 1 ELSE 0 END)"] | 25 | 0.691 |
| [S20/Q18](#s20) | success | ["health_education"] | 0 / {} | ["\"Campaign Format (Poster/Video/Lecture)\"", "\"Key Locations (School/Hospital/Community)\""] | ["AVG(\"Campaign Frequency (times/month)\")", "AVG(\"Distribution Quantity\")", "AVG(CAST(REPLACE(\"Knowledge Assessment\", '%', '') AS REAL))"] | 9 | 0.542 |
| [S21/Q19](#s21) | success | ["health_education"] | 0 / {} | [] | [] | 75 | 0.637 |
| [S22/Q20](#s22) | success | ["health_education"] | 0 / {} | ["\"Campaign Format (Poster/Video/Lecture)\"", "\"Key Locations (School/Hospital/Community)\""] | ["COUNT(*)", "SUM(CASE WHEN \"Behavioral Change Assessment\" = 'Significant' THEN 1 ELSE 0 END)", "SUM(CASE WHEN \"Effectiveness Tracking\" = 'Significant' THEN 1 ELSE 0 END)", "SUM(CASE WHEN \"Behavioral Change Assessment\" = 'Significant' AND \"Effectiveness Tracking\" = 'Significant' THEN 1 ELSE 0 END)", "SUM(CASE WHEN \"Effectiveness Assessment\" = 'Significant' THEN 1 ELSE 0 END)"] | 9 | 0.705 |
| [S23/Q21](#s23) | success | ["health_education"] | 0 / {} | ["\"Campaign Format (Poster/Video/Lecture)\"", "\"Key Locations (School/Hospital/Community)\"", "\"Campaign Content (Prevention/Treatment/Policy)\""] | ["COUNT(*)", "SUM(CASE WHEN \"Behavioral Change Assessment\" = 'Significant' AND \"Effectiveness Tracking\" = 'Significant' THEN 1 ELSE 0 END)"] | 6 | 0.557 |
| [S24/Q22](#s24) | success | ["health_education"] | 0 / {} | ["\"Campaign Format (Poster/Video/Lecture)\"", "\"Key Locations (School/Hospital/Community)\""] | ["COUNT(*)", "COUNT(*)", "SUM(CASE WHEN \"Behavioral Change Assessment\" = 'Significant' AND \"Effectiveness Tracking\" = 'Significant' THEN 1 ELSE 0 END)"] | 9 | 0.804 |
| [S25/Q23](#s25) | success | ["health_education"] | 0 / {} | [] | [] | 7 | 0.564 |
| [S26/Q24](#s26) | success | ["health_education"] | 0 / {} | [] | [] | 75 | 0.738 |
| [S27/Q25](#s27) | success | ["health_education"] | 0 / {} | [] | [] | 325 | 0.933 |
| [S28/Q26](#s28) | success | ["health_education"] | 0 / {} | [] | [] | 75 | 0.722 |
| [S29/Q27](#s29) | success | ["health_education"] | 0 / {} | ["\"Campaign Format (Poster/Video/Lecture)\"", "\"Key Locations (School/Hospital/Community)\""] | ["COUNT(*)", "COUNT(*)", "COUNT(*)", "COUNT(*)", "COUNT(*)", "SUM(CASE WHEN \"Behavioral Change Assessment\" = 'Significant' THEN 1 ELSE 0 END)", "SUM(CASE WHEN \"Effectiveness Tracking\" = 'Significant' THEN 1 ELSE 0 END)", "SUM(CASE WHEN \"Effectiveness Assessment\" = 'Significant' THEN 1 ELSE 0 END)", "SUM(CASE WHEN \"Behavioral Change Assessment\" = 'Significant' AND \"Effectiveness Tracking\" = 'Significant' THEN 1 ELSE 0 END)"] | 9 | 0.612 |
| [S30/Q28](#s30) | success | ["health_education"] | 0 / {} | ["\"Campaign Format (Poster/Video/Lecture)\""] | ["COUNT(*)", "SUM(CASE WHEN \"Behavioral Change Assessment\" = 'Significant' AND \"Effectiveness Tracking\" = 'Significant' THEN 1 ELSE 0 END)", "COUNT(*)", "SUM(CASE WHEN \"Behavioral Change Assessment\" = 'Significant' AND \"Effectiveness Tracking\" = 'Significant' THEN 1 ELSE 0 END)"] | 3 | 0.51 |
| [S31/Q29](#s31) | success | ["health_education"] | 0 / {} | ["\"Key Locations (School/Hospital/Community)\""] | ["COUNT(*)", "SUM(CASE WHEN \"Behavioral Change Assessment\" = 'Significant' AND \"Effectiveness Tracking\" = 'Significant' THEN 1 ELSE 0 END)", "COUNT(*)", "SUM(CASE WHEN \"Behavioral Change Assessment\" = 'Significant' AND \"Effectiveness Tracking\" = 'Significant' THEN 1 ELSE 0 END)"] | 3 | 0.522 |
| [S32/Q30](#s32) | success | ["health_education"] | 0 / {} | [] | [] | 75 | 0.56 |


## 元数据和设置

| SQL | 类别 | 状态 | 内容 |
| --- | --- | --- | --- |
| S1 | connection_setup | success | PRAGMA query_only=ON |
| S2 | metadata | success | SELECT name,sql FROM sqlite_master WHERE type='table' ORDER BY name |


## Python 与执行位置

人工源码审查：**database_first_violation**。Python 在学生宣传活动明细上构造显著改善标志，并按形式×地点计算数量、比例和效果交集；这些可在 SQL 中完成。卡方/t 检验、置信区间与绘图是单独的合理统计补充，不能作为全部分组计数迁出数据库的理由。 [证据](../reviews/dacomp-044.json)。

P1：Compute exact rates, Wilson confidence intervals, and chi-square/Fisher tests for student-targeted health education campaigns by format and location. This requires statistical procedures (CIs, hypothesis tests) not reasonably supported by SQLite, and visualization.

[源码](../../../runs/dsv4flash-db-first-full-01/dacomp-044/attempt-01/python/P1.py)；[输出](../../../runs/dsv4flash-db-first-full-01/dacomp-044/attempt-01/python/P1.stdout)；[错误](../../../runs/dsv4flash-db-first-full-01/dacomp-044/attempt-01/python/P1.stderr)。检出需人工核验的 SQL 可实现操作：groupby(, .query(, sort_values(；不能仅凭理由判为合规。

P2：Create heatmaps and bar charts to visualize the rates of behavioral change, effectiveness tracking, and combined effectiveness for student campaigns by format and location. These visualizations are not supported by SQL.

[源码](../../../runs/dsv4flash-db-first-full-01/dacomp-044/attempt-01/python/P2.py)；[输出](../../../runs/dsv4flash-db-first-full-01/dacomp-044/attempt-01/python/P2.stdout)；[错误](../../../runs/dsv4flash-db-first-full-01/dacomp-044/attempt-01/python/P2.stderr)。检出需人工核验的 SQL 可实现操作：.query(, sort_values(；不能仅凭理由判为合规。

P3：Compare awareness rates, knowledge scores, and new media engagement between campaigns that achieved both behavioral change and long-term tracking vs those that didn't, for students. This requires statistical tests not available in SQL.

[源码](../../../runs/dsv4flash-db-first-full-01/dacomp-044/attempt-01/python/P3.py)；[输出](../../../runs/dsv4flash-db-first-full-01/dacomp-044/attempt-01/python/P3.stdout)；[错误](../../../runs/dsv4flash-db-first-full-01/dacomp-044/attempt-01/python/P3.stderr)。检出需人工核验的 SQL 可实现操作：.query(；不能仅凭理由判为合规。

P4：Analyze correlations between effectiveness metrics and compute the combined analysis for both interpretations of 'long-term effectiveness'. Also compute format × location rankings using a composite capability score.

[源码](../../../runs/dsv4flash-db-first-full-01/dacomp-044/attempt-01/python/P4.py)；[输出](../../../runs/dsv4flash-db-first-full-01/dacomp-044/attempt-01/python/P4.stdout)；[错误](../../../runs/dsv4flash-db-first-full-01/dacomp-044/attempt-01/python/P4.stderr)。检出需人工核验的 SQL 可实现操作：groupby(, .query(, sort_values(；不能仅凭理由判为合规。

P5：Create final comprehensive visualization: a bubble chart showing format × location combinations for student campaigns, with bubble size representing sample size and color indicating both_sig rate. Also a grouped bar chart of the top performers.

[源码](../../../runs/dsv4flash-db-first-full-01/dacomp-044/attempt-01/python/P5.py)；[输出](../../../runs/dsv4flash-db-first-full-01/dacomp-044/attempt-01/python/P5.stdout)；[错误](../../../runs/dsv4flash-db-first-full-01/dacomp-044/attempt-01/python/P5.stderr)。检出需人工核验的 SQL 可实现操作：groupby(, .query(, sort_values(；不能仅凭理由判为合规。

## 优化机会

已验证候选。筛选限于精确 SQL、相同自包含 CTE、相同单表完整过滤、可分解单表聚合；未覆盖任意 Join 等价和一般谓词蕴含。全部候选都是 offline，未测在线预测。

| 候选 | 类型 | 已有结果 | 覆盖 SQL | 后续次数 | 中间行数 | 验证 | 成本 |
| --- | --- | --- | --- | --- | --- | --- | --- |
| C1 | common filtered view | False | ["S12", "S13", "S14", "S15", "S16", "S18", "S19", "S20", "S21", "S22", "S23", "S26", "S28", "S29", "S30", "S31", "S32"] | 16 | 75 | verified | Not benchmarked; correctness alone does not establish net speedup. |
| C2 | aggregate MV | False | ["S13", "S14", "S15", "S16", "S18", "S19", "S20", "S22", "S29", "S30", "S31"] | 10 | 25 | verified | Not benchmarked; correctness alone does not establish net speedup. |
| C3 | common filtered view | False | ["S17", "S25"] | 1 | unknown | not_verified_cap | Not tested |
| C4 | common filtered view | False | ["S24", "S27"] | 1 | 325 | verified | Not benchmarked; correctness alone does not establish net speedup. |


已验证覆盖（含触发查询、候选并集去重）：19/30 条成功数据 SQL。正确性仅针对当前数据库快照；未测性能的候选不能声称已加速。

[完整 build/rewrite 与比较证据](dacomp-044.analysis.json)。

### C1：common filtered view

Same single source and complete filter; original filter retained.

原查询 [S12](#s12), [S13](#s13), [S14](#s14), [S15](#s15), [S16](#s16), [S18](#s18), [S19](#s19), [S20](#s20), [S21](#s21), [S22](#s22), [S23](#s23), [S26](#s26), [S28](#s28), [S29](#s29), [S30](#s30), [S31](#s31), [S32](#s32) → 新增共享状态 C1 → 后续 16 次可复用。该构建点为事后假设，不代表 Agent 当时预知后续。

构建定义：

```sql
SELECT * FROM "health_education" WHERE "Population Covered" = 'Student'
```

受益查询 S12 的改写示例：

```sql
SELECT * FROM temp.reuse_candidate AS health_education WHERE "Population Covered" = 'Student'
```

| 原 SQL | 列名一致 | 结果一致 | 比较方法 |
| --- | --- | --- | --- |
| S12 | True | True | exact_multiset |
| S13 | True | True | ordered_numeric_tolerance |
| S14 | True | True | ordered_numeric_tolerance |
| S15 | True | True | ordered_numeric_tolerance |
| S16 | True | True | ordered_numeric_tolerance |
| S18 | True | True | ordered_numeric_tolerance |
| S19 | True | True | ordered_numeric_tolerance |
| S20 | True | True | ordered_numeric_tolerance |
| S21 | True | True | exact_multiset |
| S22 | True | True | ordered_numeric_tolerance |
| S23 | True | True | ordered_numeric_tolerance |
| S26 | True | True | exact_multiset |
| S28 | True | True | exact_multiset |
| S29 | True | True | ordered_numeric_tolerance |
| S30 | True | True | ordered_numeric_tolerance |
| S31 | True | True | ordered_numeric_tolerance |
| S32 | True | True | exact_multiset |


验证状态：verified；成本结论：Not benchmarked; correctness alone does not establish net speedup.

### C2：aggregate MV

Union of grouping keys; decomposable aggregate states; AVG uses SUM and non-NULL COUNT.

原查询 [S13](#s13), [S14](#s14), [S15](#s15), [S16](#s16), [S18](#s18), [S19](#s19), [S20](#s20), [S22](#s22), [S29](#s29), [S30](#s30), [S31](#s31) → 新增共享状态 C2 → 后续 10 次可复用。该构建点为事后假设，不代表 Agent 当时预知后续。

构建定义：

```sql
SELECT "Campaign Format (Poster/Video/Lecture)" AS __g0, "Key Locations (School/Hospital/Community)" AS __g1, "Campaign Content (Prevention/Treatment/Policy)" AS __g2, COUNT(*) AS __a0, SUM(CASE WHEN "Behavioral Change Assessment" = 'Significant' THEN 1 ELSE 0 END) AS __a1, SUM(CASE WHEN "Effectiveness Tracking" = 'Significant' THEN 1 ELSE 0 END) AS __a2, SUM(CASE WHEN "Effectiveness Assessment" = 'Significant' THEN 1 ELSE 0 END) AS __a3, SUM(CASE WHEN "Behavioral Change Assessment" = 'Significant' AND "Effectiveness Tracking" = 'Significant' THEN 1 ELSE 0 END) AS __a4, SUM("Campaign Frequency (times/month)") AS __a5_sum, COUNT("Campaign Frequency (times/month)") AS __a5_n, SUM("Distribution Quantity") AS __a6_sum, COUNT("Distribution Quantity") AS __a6_n, SUM(CAST(REPLACE("Knowledge Assessment", '%', '') AS REAL)) AS __a7_sum, COUNT(CAST(REPLACE("Knowledge Assessment", '%', '') AS REAL)) AS __a7_n FROM "health_education" WHERE "Population Covered" = 'Student' GROUP BY "Campaign Format (Poster/Video/Lecture)", "Key Locations (School/Hospital/Community)", "Campaign Content (Prevention/Treatment/Policy)"
```

受益查询 S13 的改写示例：

```sql
SELECT __g0 AS format, __g1 AS location, SUM(__a0) AS n, SUM(__a1) AS behav_sig, SUM(__a2) AS track_sig, SUM(__a3) AS eff_sig FROM temp.reuse_candidate GROUP BY __g0, __g1 ORDER BY format, location
```

| 原 SQL | 列名一致 | 结果一致 | 比较方法 |
| --- | --- | --- | --- |
| S13 | True | True | ordered_numeric_tolerance |
| S14 | True | True | ordered_numeric_tolerance |
| S15 | True | True | ordered_numeric_tolerance |
| S16 | True | True | ordered_numeric_tolerance |
| S18 | True | True | ordered_numeric_tolerance |
| S19 | True | True | ordered_numeric_tolerance |
| S20 | True | True | ordered_numeric_tolerance |
| S22 | True | True | ordered_numeric_tolerance |
| S29 | True | True | ordered_numeric_tolerance |
| S30 | True | True | ordered_numeric_tolerance |
| S31 | True | True | ordered_numeric_tolerance |


验证状态：verified；成本结论：Not benchmarked; correctness alone does not establish net speedup.

### C4：common filtered view

Same single source and complete filter; original filter retained.

原查询 [S24](#s24), [S27](#s27) → 新增共享状态 C4 → 后续 1 次可复用。该构建点为事后假设，不代表 Agent 当时预知后续。

构建定义：

```sql
SELECT * FROM "health_education" WHERE "Population Covered" <> 'Student'
```

受益查询 S24 的改写示例：

```sql
SELECT "Campaign Format (Poster/Video/Lecture)" AS format, "Key Locations (School/Hospital/Community)" AS location, COUNT(*) AS n, ROUND(100.0 * SUM(CASE WHEN "Behavioral Change Assessment" = 'Significant' AND "Effectiveness Tracking" = 'Significant' THEN 1 ELSE 0 END) / COUNT(*), 1) AS both_pct FROM temp.reuse_candidate AS health_education WHERE "Population Covered" <> 'Student' GROUP BY format, location ORDER BY both_pct DESC
```

| 原 SQL | 列名一致 | 结果一致 | 比较方法 |
| --- | --- | --- | --- |
| S24 | True | True | ordered_numeric_tolerance |
| S27 | True | True | exact_multiset |


验证状态：verified；成本结论：Not benchmarked; correctness alone does not establish net speedup.

结果依赖：自动记录 SQL→Python 的接口父调用，以及源码中引用归档文件的消费者；字面值相同不认定因果。模型方向选择需要人工读取消息，尚未做全面因果标注。

[原始报告](../../../runs/dsv4flash-db-first-full-01/dacomp-044/attempt-01/answer.md)；[统一消息](../../../runs/dsv4flash-db-first-full-01/dacomp-044/attempt-01/messages.jsonl)；[原始 OpenCode 事件](../../../runs/dsv4flash-db-first-full-01/dacomp-044/attempt-01/opencode.jsonl)；[SQL 引擎日志](../../../runs/dsv4flash-db-first-full-01/dacomp-044/attempt-01/sql_journal.jsonl)。

[可读报告（本地图片链接规范化）](../answers/dacomp-044.md)。原始回答保留，分析结论未改写。

## S1

类别 `connection_setup`；来源 `connection`；调用 `c098e36f2384432c980126225e243ec0`；状态 `success`。

```sql
PRAGMA query_only=ON
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-044/attempt-01/sql/S1.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-044/attempt-01/sql/S1.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-044/attempt-01/results/S1.rows.jsonl)；完整：True；SHA256：`e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`。

## S2

类别 `metadata`；来源 `list_db`；调用 `c098e36f2384432c980126225e243ec0`；状态 `success`。

```sql
SELECT name,sql FROM sqlite_master WHERE type='table' ORDER BY name
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-044/attempt-01/sql/S2.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-044/attempt-01/sql/S2.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-044/attempt-01/results/S2.rows.jsonl)；完整：True；SHA256：`c548ad4f315de20491a71f91a29b1d8355ac2bf7ba3cc21416097448947ce71e`。

## S3

类别 `data`；来源 `query_db`；调用 `c611481a45e54f87b2c86f7ee3529268`；状态 `success`。

```sql
SELECT * FROM health_education LIMIT 20
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-044/attempt-01/sql/S3.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-044/attempt-01/sql/S3.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-044/attempt-01/results/S3.rows.jsonl)；完整：True；SHA256：`75256ec827a231d244ecdb1b931f5037fdc05ea5863c13ea7d0717c77611a1ef`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "health_education", "kind": "base", "block": null, "base_tables": ["health_education"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |


## S4

类别 `data`；来源 `query_db`；调用 `e0bee5e567be4bf4a522be22862685f0`；状态 `success`。

```sql
SELECT DISTINCT "Occupation/Role (Childcare/Student/Teacher)" FROM basic_medical_record_informatio
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-044/attempt-01/sql/S4.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-044/attempt-01/sql/S4.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-044/attempt-01/results/S4.rows.jsonl)；完整：True；SHA256：`a244347410153e7491c952dba72ec95e9f99aca5f9be290b7b55813250040ecd`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "basic_medical_record_informatio", "kind": "base", "block": null, "base_tables": ["basic_medical_record_informatio"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |


## S5

类别 `data`；来源 `query_db`；调用 `b6e4345cffba4afa99c4897fd5a179a3`；状态 `success`。

```sql
SELECT DISTINCT "Population Covered" FROM health_education
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-044/attempt-01/sql/S5.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-044/attempt-01/sql/S5.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-044/attempt-01/results/S5.rows.jsonl)；完整：True；SHA256：`e84b650be67cbf8c2fb2faed7307431ad6c6f27844bace77ba1f8818ada81ec5`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "health_education", "kind": "base", "block": null, "base_tables": ["health_education"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |


## S6

类别 `data`；来源 `query_db`；调用 `367c4e2f9ea64d729b440f47c42294ce`；状态 `success`。

```sql
SELECT DISTINCT "Key Locations (School/Hospital/Community)" FROM health_education
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-044/attempt-01/sql/S6.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-044/attempt-01/sql/S6.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-044/attempt-01/results/S6.rows.jsonl)；完整：True；SHA256：`443a665d0cfeda8f53bddda36915a8290664e99c41a606282872ef94b95e301b`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "health_education", "kind": "base", "block": null, "base_tables": ["health_education"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |


## S7

类别 `data`；来源 `query_db`；调用 `6c7375282aea436c9d5cc298fa95f1c3`；状态 `success`。

```sql
SELECT DISTINCT "Campaign Format (Poster/Video/Lecture)" FROM health_education
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-044/attempt-01/sql/S7.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-044/attempt-01/sql/S7.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-044/attempt-01/results/S7.rows.jsonl)；完整：True；SHA256：`92f186f5ced824a4077c88af58272a289b903561dffd7f62ee1c34b6239f59be`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "health_education", "kind": "base", "block": null, "base_tables": ["health_education"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |


## S8

类别 `data`；来源 `query_db`；调用 `e6ce32718b1748be8d38ecce88002b21`；状态 `success`。

```sql
SELECT DISTINCT "Effectiveness Assessment" FROM health_education
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-044/attempt-01/sql/S8.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-044/attempt-01/sql/S8.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-044/attempt-01/results/S8.rows.jsonl)；完整：True；SHA256：`d499f36120bb0c88e2b3f2ac6b0e67b695b085ebef46c0580d1b644ab2f1a329`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "health_education", "kind": "base", "block": null, "base_tables": ["health_education"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |


## S9

类别 `data`；来源 `query_db`；调用 `f077f101488b4e3080c41de630644132`；状态 `success`。

```sql
SELECT DISTINCT "Behavioral Change Assessment" FROM health_education
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-044/attempt-01/sql/S9.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-044/attempt-01/sql/S9.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-044/attempt-01/results/S9.rows.jsonl)；完整：True；SHA256：`e0db4f5885c9871a9fe8eae8d4376ad7c19e850a81ebc160b86fd6a402ec5b79`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "health_education", "kind": "base", "block": null, "base_tables": ["health_education"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |


## S10

类别 `data`；来源 `query_db`；调用 `5efe0972381349d39cf7cc400f593df9`；状态 `success`。

```sql
SELECT DISTINCT "Effectiveness Tracking" FROM health_education
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-044/attempt-01/sql/S10.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-044/attempt-01/sql/S10.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-044/attempt-01/results/S10.rows.jsonl)；完整：True；SHA256：`64589f9bc6a6697478fa5d5d8ed084fa12702572c161e80dd13a7f20f1e5cbac`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "health_education", "kind": "base", "block": null, "base_tables": ["health_education"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |


## S11

类别 `data`；来源 `query_db`；调用 `5a350334e0d74be99f91e22a8fd3efb6`；状态 `success`。

```sql
SELECT COUNT(*) AS total_rows FROM health_education
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-044/attempt-01/sql/S11.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-044/attempt-01/sql/S11.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-044/attempt-01/results/S11.rows.jsonl)；完整：True；SHA256：`1f401dcea8166bb67574bf1b38efbffe97c53f87f3cc03a17777a80dae86b48a`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "health_education", "kind": "base", "block": null, "base_tables": ["health_education"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |


## S12

类别 `data`；来源 `query_db`；调用 `3dafd1f1ebdd4b89b43c126967cdd613`；状态 `success`。

```sql
SELECT * FROM health_education WHERE "Population Covered" = 'Student'
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-044/attempt-01/sql/S12.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-044/attempt-01/sql/S12.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-044/attempt-01/results/S12.rows.jsonl)；完整：True；SHA256：`a339e6cc2f0aff9e33d3e995e6524052b2c3c0a92b700def3b4ba8c7db2e33ef`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "health_education", "kind": "base", "block": null, "base_tables": ["health_education"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |


## S13

类别 `data`；来源 `query_db`；调用 `b45a5738d2364f45be0190b617903540`；状态 `success`。

```sql
SELECT
  "Campaign Format (Poster/Video/Lecture)" AS format,
  "Key Locations (School/Hospital/Community)" AS location,
  COUNT(*) AS n,
  SUM(CASE WHEN "Behavioral Change Assessment"='Significant' THEN 1 ELSE 0 END) AS behav_sig,
  SUM(CASE WHEN "Effectiveness Tracking"='Significant' THEN 1 ELSE 0 END) AS track_sig,
  SUM(CASE WHEN "Effectiveness Assessment"='Significant' THEN 1 ELSE 0 END) AS eff_sig
FROM health_education
WHERE "Population Covered" = 'Student'
GROUP BY format, location
ORDER BY format, location
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-044/attempt-01/sql/S13.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-044/attempt-01/sql/S13.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-044/attempt-01/results/S13.rows.jsonl)；完整：True；SHA256：`babc602509e11ef002bb9cd6521f2732fb4efffcf8377404be8d58dd88f71ba4`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "health_education", "kind": "base", "block": null, "base_tables": ["health_education"]}] | [] | ["\"Campaign Format (Poster/Video/Lecture)\"", "\"Key Locations (School/Hospital/Community)\""] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |
| B1 | SUM(CASE WHEN "Behavioral Change Assessment" = 'Significant' THEN 1 ELSE 0 END) | [] | [{"table": "health_education", "column": "Behavioral Change Assessment"}] | False |
| B1 | SUM(CASE WHEN "Effectiveness Tracking" = 'Significant' THEN 1 ELSE 0 END) | [] | [{"table": "health_education", "column": "Effectiveness Tracking"}] | False |
| B1 | SUM(CASE WHEN "Effectiveness Assessment" = 'Significant' THEN 1 ELSE 0 END) | [] | [{"table": "health_education", "column": "Effectiveness Assessment"}] | False |


## S14

类别 `data`；来源 `query_db`；调用 `c934f769adad44648e72765a1e39772a`；状态 `success`。

```sql
SELECT
  "Campaign Format (Poster/Video/Lecture)" AS format,
  COUNT(*) AS n,
  SUM(CASE WHEN "Behavioral Change Assessment"='Significant' THEN 1 ELSE 0 END) AS behav_sig,
  SUM(CASE WHEN "Effectiveness Tracking"='Significant' THEN 1 ELSE 0 END) AS track_sig
FROM health_education
WHERE "Population Covered" = 'Student'
GROUP BY format
ORDER BY n DESC
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-044/attempt-01/sql/S14.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-044/attempt-01/sql/S14.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-044/attempt-01/results/S14.rows.jsonl)；完整：True；SHA256：`c1d217779eeefc2249337328d74826c8fbf4f0691d06f38592ab3fd12efd01fa`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "health_education", "kind": "base", "block": null, "base_tables": ["health_education"]}] | [] | ["\"Campaign Format (Poster/Video/Lecture)\""] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |
| B1 | SUM(CASE WHEN "Behavioral Change Assessment" = 'Significant' THEN 1 ELSE 0 END) | [] | [{"table": "health_education", "column": "Behavioral Change Assessment"}] | False |
| B1 | SUM(CASE WHEN "Effectiveness Tracking" = 'Significant' THEN 1 ELSE 0 END) | [] | [{"table": "health_education", "column": "Effectiveness Tracking"}] | False |


## S15

类别 `data`；来源 `query_db`；调用 `a576925a77224006ac9f158cccb92a00`；状态 `success`。

```sql
SELECT
  "Campaign Format (Poster/Video/Lecture)" AS format,
  "Key Locations (School/Hospital/Community)" AS location,
  COUNT(*) AS n,
  SUM(CASE WHEN "Behavioral Change Assessment"='Significant' AND "Effectiveness Tracking"='Significant' THEN 1 ELSE 0 END) AS both_sig
FROM health_education
WHERE "Population Covered" = 'Student'
GROUP BY format, location
ORDER BY both_sig DESC, n DESC
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-044/attempt-01/sql/S15.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-044/attempt-01/sql/S15.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-044/attempt-01/results/S15.rows.jsonl)；完整：True；SHA256：`dfb843a63f5590bd996a889ae0c12c6138bc806d767de6e281ac9b2248f8109b`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "health_education", "kind": "base", "block": null, "base_tables": ["health_education"]}] | [] | ["\"Campaign Format (Poster/Video/Lecture)\"", "\"Key Locations (School/Hospital/Community)\""] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |
| B1 | SUM(CASE WHEN "Behavioral Change Assessment" = 'Significant' AND "Effectiveness Tracking" = 'Significant' THEN 1 ELSE 0 END) | [] | [{"table": "health_education", "column": "Behavioral Change Assessment"}, {"table": "health_education", "column": "Effectiveness Tracking"}] | False |


## S16

类别 `data`；来源 `query_db`；调用 `e2be8a146fe04df8be0da7c4b25b9407`；状态 `success`。

```sql
SELECT
  "Key Locations (School/Hospital/Community)" AS location,
  COUNT(*) AS n,
  SUM(CASE WHEN "Behavioral Change Assessment"='Significant' THEN 1 ELSE 0 END) AS behav_sig,
  SUM(CASE WHEN "Effectiveness Tracking"='Significant' THEN 1 ELSE 0 END) AS track_sig,
  SUM(CASE WHEN "Behavioral Change Assessment"='Significant' AND "Effectiveness Tracking"='Significant' THEN 1 ELSE 0 END) AS both_sig
FROM health_education
WHERE "Population Covered" = 'Student'
GROUP BY location
ORDER BY n DESC
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-044/attempt-01/sql/S16.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-044/attempt-01/sql/S16.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-044/attempt-01/results/S16.rows.jsonl)；完整：True；SHA256：`0a25af3448c478a3c7547773614dc8243314ff023525123199a03013857a3146`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "health_education", "kind": "base", "block": null, "base_tables": ["health_education"]}] | [] | ["\"Key Locations (School/Hospital/Community)\""] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |
| B1 | SUM(CASE WHEN "Behavioral Change Assessment" = 'Significant' THEN 1 ELSE 0 END) | [] | [{"table": "health_education", "column": "Behavioral Change Assessment"}] | False |
| B1 | SUM(CASE WHEN "Effectiveness Tracking" = 'Significant' THEN 1 ELSE 0 END) | [] | [{"table": "health_education", "column": "Effectiveness Tracking"}] | False |
| B1 | SUM(CASE WHEN "Behavioral Change Assessment" = 'Significant' AND "Effectiveness Tracking" = 'Significant' THEN 1 ELSE 0 END) | [] | [{"table": "health_education", "column": "Behavioral Change Assessment"}, {"table": "health_education", "column": "Effectiveness Tracking"}] | False |


## S17

类别 `data`；来源 `query_db`；调用 `7f25a025dcec437bba2489d5d2461594`；状态 `success`。

```sql
SELECT *
FROM health_education
WHERE "Population Covered" = 'Student'
  AND "Behavioral Change Assessment" = 'Significant'
  AND "Effectiveness Tracking" = 'Significant'
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-044/attempt-01/sql/S17.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-044/attempt-01/sql/S17.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-044/attempt-01/results/S17.rows.jsonl)；完整：True；SHA256：`c0e2a267535265cbe5c0ca6905b9c71b923764df7d892d83476a395f172d14f9`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "health_education", "kind": "base", "block": null, "base_tables": ["health_education"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |


## S18

类别 `data`；来源 `query_db`；调用 `1618f5cb7e58441f95a5210dcb918fd7`；状态 `success`。

```sql
SELECT
  "Campaign Format (Poster/Video/Lecture)" AS format,
  "Key Locations (School/Hospital/Community)" AS location,
  COUNT(*) AS n,
  SUM(CASE WHEN "Behavioral Change Assessment"='Significant' THEN 1 ELSE 0 END) AS behav_sig,
  ROUND(100.0 * SUM(CASE WHEN "Behavioral Change Assessment"='Significant' THEN 1 ELSE 0 END) / COUNT(*), 1) AS behav_sig_pct,
  SUM(CASE WHEN "Effectiveness Tracking"='Significant' THEN 1 ELSE 0 END) AS track_sig,
  ROUND(100.0 * SUM(CASE WHEN "Effectiveness Tracking"='Significant' THEN 1 ELSE 0 END) / COUNT(*), 1) AS track_sig_pct,
  SUM(CASE WHEN "Behavioral Change Assessment"='Significant' AND "Effectiveness Tracking"='Significant' THEN 1 ELSE 0 END) AS both_sig,
  ROUND(100.0 * SUM(CASE WHEN "Behavioral Change Assessment"='Significant' AND "Effectiveness Tracking"='Significant' THEN 1 ELSE 0 END) / COUNT(*), 1) AS both_sig_pct
FROM health_education
WHERE "Population Covered" = 'Student'
GROUP BY format, location
ORDER BY both_sig_pct DESC, n DESC
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-044/attempt-01/sql/S18.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-044/attempt-01/sql/S18.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-044/attempt-01/results/S18.rows.jsonl)；完整：True；SHA256：`e049b24852093d851042476172e8dc85631a85c7242fb882e1f84d115c3b3639`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "health_education", "kind": "base", "block": null, "base_tables": ["health_education"]}] | [] | ["\"Campaign Format (Poster/Video/Lecture)\"", "\"Key Locations (School/Hospital/Community)\""] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |
| B1 | SUM(CASE WHEN "Behavioral Change Assessment" = 'Significant' THEN 1 ELSE 0 END) | [] | [{"table": "health_education", "column": "Behavioral Change Assessment"}] | False |
| B1 | SUM(CASE WHEN "Effectiveness Tracking" = 'Significant' THEN 1 ELSE 0 END) | [] | [{"table": "health_education", "column": "Effectiveness Tracking"}] | False |
| B1 | SUM(CASE WHEN "Behavioral Change Assessment" = 'Significant' AND "Effectiveness Tracking" = 'Significant' THEN 1 ELSE 0 END) | [] | [{"table": "health_education", "column": "Behavioral Change Assessment"}, {"table": "health_education", "column": "Effectiveness Tracking"}] | False |
| B1 | COUNT(*) | [] | [] | True |
| B1 | COUNT(*) | [] | [] | True |
| B1 | COUNT(*) | [] | [] | True |
| B1 | SUM(CASE WHEN "Behavioral Change Assessment" = 'Significant' THEN 1 ELSE 0 END) | [] | [{"table": "health_education", "column": "Behavioral Change Assessment"}] | False |
| B1 | SUM(CASE WHEN "Effectiveness Tracking" = 'Significant' THEN 1 ELSE 0 END) | [] | [{"table": "health_education", "column": "Effectiveness Tracking"}] | False |
| B1 | SUM(CASE WHEN "Behavioral Change Assessment" = 'Significant' AND "Effectiveness Tracking" = 'Significant' THEN 1 ELSE 0 END) | [] | [{"table": "health_education", "column": "Behavioral Change Assessment"}, {"table": "health_education", "column": "Effectiveness Tracking"}] | False |


## S19

类别 `data`；来源 `query_db`；调用 `112278bc6d904425ad9eecd847a9e483`；状态 `success`。

```sql
SELECT
  "Campaign Format (Poster/Video/Lecture)" AS format,
  "Key Locations (School/Hospital/Community)" AS location,
  "Campaign Content (Prevention/Treatment/Policy)" AS content,
  COUNT(*) AS n,
  SUM(CASE WHEN "Behavioral Change Assessment"='Significant' AND "Effectiveness Tracking"='Significant' THEN 1 ELSE 0 END) AS both_sig
FROM health_education
WHERE "Population Covered" = 'Student'
GROUP BY format, location, content
ORDER BY format, location
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-044/attempt-01/sql/S19.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-044/attempt-01/sql/S19.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-044/attempt-01/results/S19.rows.jsonl)；完整：True；SHA256：`849d977e2b413324dfaf31024fcf13cf3e57c538e287df530f0ab3267cb897e2`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "health_education", "kind": "base", "block": null, "base_tables": ["health_education"]}] | [] | ["\"Campaign Format (Poster/Video/Lecture)\"", "\"Key Locations (School/Hospital/Community)\"", "\"Campaign Content (Prevention/Treatment/Policy)\""] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |
| B1 | SUM(CASE WHEN "Behavioral Change Assessment" = 'Significant' AND "Effectiveness Tracking" = 'Significant' THEN 1 ELSE 0 END) | [] | [{"table": "health_education", "column": "Behavioral Change Assessment"}, {"table": "health_education", "column": "Effectiveness Tracking"}] | False |


## S20

类别 `data`；来源 `query_db`；调用 `fd6c63056b7b41378d63b1ef0efde0a0`；状态 `success`。

```sql
SELECT
  "Campaign Format (Poster/Video/Lecture)" AS format,
  "Key Locations (School/Hospital/Community)" AS location,
  ROUND(AVG("Campaign Frequency (times/month)"),1) AS avg_freq,
  ROUND(AVG("Distribution Quantity"),0) AS avg_qty,
  ROUND(AVG(CAST(REPLACE("Knowledge Assessment",'%','') AS REAL)),1) AS avg_knowledge
FROM health_education
WHERE "Population Covered" = 'Student'
GROUP BY format, location
ORDER BY format, location
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-044/attempt-01/sql/S20.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-044/attempt-01/sql/S20.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-044/attempt-01/results/S20.rows.jsonl)；完整：True；SHA256：`5597fbcaaa341e583ea35c5811d0d142f7b62124909c08de29170567d6e946c0`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "health_education", "kind": "base", "block": null, "base_tables": ["health_education"]}] | [] | ["\"Campaign Format (Poster/Video/Lecture)\"", "\"Key Locations (School/Hospital/Community)\""] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | AVG("Campaign Frequency (times/month)") | [{"table": "health_education", "column": "Campaign Frequency (times/month)"}] | [] | False |
| B1 | AVG("Distribution Quantity") | [{"table": "health_education", "column": "Distribution Quantity"}] | [] | False |
| B1 | AVG(CAST(REPLACE("Knowledge Assessment", '%', '') AS REAL)) | [{"table": "health_education", "column": "Knowledge Assessment"}] | [] | False |


## S21

类别 `data`；来源 `python`；调用 `a6efc767ccb64f18929f9502cb60f69b`；状态 `success`。

```sql

SELECT "Campaign Format (Poster/Video/Lecture)" AS format,
       "Key Locations (School/Hospital/Community)" AS location,
       "Campaign Content (Prevention/Treatment/Policy)" AS content,
       "Behavioral Change Assessment" AS behav,
       "Effectiveness Tracking" AS track,
       "Effectiveness Assessment" AS eff,
       "Awareness Rate Survey" AS awareness,
       "Knowledge Assessment" AS knowledge,
       "Campaign Frequency (times/month)" AS freq,
       "Distribution Quantity" AS qty
FROM health_education
WHERE "Population Covered" = 'Student'

```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-044/attempt-01/sql/S21.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-044/attempt-01/sql/S21.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-044/attempt-01/results/S21.rows.jsonl)；完整：True；SHA256：`0ced53559c5c879b472461bc3d0f275605dcdc6c684b53ad12102dcbddfc69dc`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "health_education", "kind": "base", "block": null, "base_tables": ["health_education"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |


## S22

类别 `data`；来源 `python`；调用 `928a6e909b52416ab0f1284cfa958d04`；状态 `success`。

```sql

SELECT "Campaign Format (Poster/Video/Lecture)" AS format,
       "Key Locations (School/Hospital/Community)" AS location,
       COUNT(*) AS n,
       SUM(CASE WHEN "Behavioral Change Assessment"='Significant' THEN 1 ELSE 0 END) AS behav_sig,
       SUM(CASE WHEN "Effectiveness Tracking"='Significant' THEN 1 ELSE 0 END) AS track_sig,
       SUM(CASE WHEN "Behavioral Change Assessment"='Significant' AND "Effectiveness Tracking"='Significant' THEN 1 ELSE 0 END) AS both_sig,
       SUM(CASE WHEN "Effectiveness Assessment"='Significant' THEN 1 ELSE 0 END) AS eff_sig
FROM health_education
WHERE "Population Covered" = 'Student'
GROUP BY format, location
ORDER BY format, location

```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-044/attempt-01/sql/S22.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-044/attempt-01/sql/S22.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-044/attempt-01/results/S22.rows.jsonl)；完整：True；SHA256：`134eef24fda93e3e3d65acdc8e7cd0391d5199ebedceb3f07a41a86820f9133a`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "health_education", "kind": "base", "block": null, "base_tables": ["health_education"]}] | [] | ["\"Campaign Format (Poster/Video/Lecture)\"", "\"Key Locations (School/Hospital/Community)\""] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |
| B1 | SUM(CASE WHEN "Behavioral Change Assessment" = 'Significant' THEN 1 ELSE 0 END) | [] | [{"table": "health_education", "column": "Behavioral Change Assessment"}] | False |
| B1 | SUM(CASE WHEN "Effectiveness Tracking" = 'Significant' THEN 1 ELSE 0 END) | [] | [{"table": "health_education", "column": "Effectiveness Tracking"}] | False |
| B1 | SUM(CASE WHEN "Behavioral Change Assessment" = 'Significant' AND "Effectiveness Tracking" = 'Significant' THEN 1 ELSE 0 END) | [] | [{"table": "health_education", "column": "Behavioral Change Assessment"}, {"table": "health_education", "column": "Effectiveness Tracking"}] | False |
| B1 | SUM(CASE WHEN "Effectiveness Assessment" = 'Significant' THEN 1 ELSE 0 END) | [] | [{"table": "health_education", "column": "Effectiveness Assessment"}] | False |


## S23

类别 `data`；来源 `query_db`；调用 `e0b82963913449338336bd932ffb0844`；状态 `success`。

```sql
SELECT "Campaign Format (Poster/Video/Lecture)" AS format,
       "Key Locations (School/Hospital/Community)" AS location,
       "Campaign Content (Prevention/Treatment/Policy)" AS content,
       COUNT(*) AS n,
       SUM(CASE WHEN "Behavioral Change Assessment"='Significant' AND "Effectiveness Tracking"='Significant' THEN 1 ELSE 0 END) AS both_sig
FROM health_education
WHERE "Population Covered" = 'Student'
GROUP BY format, location, content
HAVING both_sig > 0
ORDER BY both_sig DESC
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-044/attempt-01/sql/S23.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-044/attempt-01/sql/S23.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-044/attempt-01/results/S23.rows.jsonl)；完整：True；SHA256：`0c6842a7d6d36d1dd315aeb55781e0b2200c0bb9aa6e5daba758bb70e52e4d1e`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "health_education", "kind": "base", "block": null, "base_tables": ["health_education"]}] | [] | ["\"Campaign Format (Poster/Video/Lecture)\"", "\"Key Locations (School/Hospital/Community)\"", "\"Campaign Content (Prevention/Treatment/Policy)\""] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |
| B1 | SUM(CASE WHEN "Behavioral Change Assessment" = 'Significant' AND "Effectiveness Tracking" = 'Significant' THEN 1 ELSE 0 END) | [] | [{"table": "health_education", "column": "Behavioral Change Assessment"}, {"table": "health_education", "column": "Effectiveness Tracking"}] | False |


## S24

类别 `data`；来源 `query_db`；调用 `2de5497b767a4122b7d069abdd967943`；状态 `success`。

```sql
SELECT
  "Campaign Format (Poster/Video/Lecture)" AS format,
  "Key Locations (School/Hospital/Community)" AS location,
  COUNT(*) AS n,
  ROUND(100.0*SUM(CASE WHEN "Behavioral Change Assessment"='Significant' AND "Effectiveness Tracking"='Significant' THEN 1 ELSE 0 END)/COUNT(*),1) AS both_pct
FROM health_education
WHERE "Population Covered" != 'Student'
GROUP BY format, location
ORDER BY both_pct DESC
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-044/attempt-01/sql/S24.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-044/attempt-01/sql/S24.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-044/attempt-01/results/S24.rows.jsonl)；完整：True；SHA256：`68ba7b81cbf001560d28ebd0e322ff435641abb1b8f2a71926631030c68b3b09`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "health_education", "kind": "base", "block": null, "base_tables": ["health_education"]}] | [] | ["\"Campaign Format (Poster/Video/Lecture)\"", "\"Key Locations (School/Hospital/Community)\""] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |
| B1 | COUNT(*) | [] | [] | True |
| B1 | SUM(CASE WHEN "Behavioral Change Assessment" = 'Significant' AND "Effectiveness Tracking" = 'Significant' THEN 1 ELSE 0 END) | [] | [{"table": "health_education", "column": "Behavioral Change Assessment"}, {"table": "health_education", "column": "Effectiveness Tracking"}] | False |


## S25

类别 `data`；来源 `query_db`；调用 `fd30ee8ba6854f6482bf488def716306`；状态 `success`。

```sql
SELECT
  CASE WHEN instr("New Media Metrics (Views/Shares)",'/')>0
       THEN CAST(substr("New Media Metrics (Views/Shares)",1,instr("New Media Metrics (Views/Shares)",'/')-1) AS INTEGER) END AS views,
  "Campaign Format (Poster/Video/Lecture)" AS format,
  "Key Locations (School/Hospital/Community)" AS location,
  "Behavioral Change Assessment" AS behav,
  "Effectiveness Tracking" AS track
FROM health_education
WHERE "Population Covered" = 'Student'
  AND "Behavioral Change Assessment"='Significant' AND "Effectiveness Tracking"='Significant'
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-044/attempt-01/sql/S25.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-044/attempt-01/sql/S25.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-044/attempt-01/results/S25.rows.jsonl)；完整：True；SHA256：`ac0324135eb71a04a4c7ef76dc37ea9c94e06be57542c48757450a0df61e3f5c`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "health_education", "kind": "base", "block": null, "base_tables": ["health_education"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |


## S26

类别 `data`；来源 `python`；调用 `22a9348a4050437ea6c9b38d10145e97`；状态 `success`。

```sql

SELECT "Campaign Format (Poster/Video/Lecture)" AS format,
       "Key Locations (School/Hospital/Community)" AS location,
       "Campaign Content (Prevention/Treatment/Policy)" AS content,
       "Behavioral Change Assessment" AS behav,
       "Effectiveness Tracking" AS track,
       "Effectiveness Assessment" AS eff,
       "Campaign Frequency (times/month)" AS freq,
       "Distribution Quantity" AS qty,
       "Awareness Rate Survey" AS awareness,
       "Knowledge Assessment" AS knowledge,
       "New Media Metrics (Views/Shares)" AS new_media
FROM health_education
WHERE "Population Covered" = 'Student'

```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-044/attempt-01/sql/S26.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-044/attempt-01/sql/S26.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-044/attempt-01/results/S26.rows.jsonl)；完整：True；SHA256：`432282dc9211f519c0ecfffc2c24c7c0a33acccd89f1dc30017637d894135d6d`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "health_education", "kind": "base", "block": null, "base_tables": ["health_education"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |


## S27

类别 `data`；来源 `python`；调用 `22a9348a4050437ea6c9b38d10145e97`；状态 `success`。

```sql

SELECT "Campaign Format (Poster/Video/Lecture)" AS format,
       "Key Locations (School/Hospital/Community)" AS location,
       "Population Covered" AS pop,
       "Behavioral Change Assessment" AS behav,
       "Effectiveness Tracking" AS track
FROM health_education
WHERE "Population Covered" != 'Student'

```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-044/attempt-01/sql/S27.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-044/attempt-01/sql/S27.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-044/attempt-01/results/S27.rows.jsonl)；完整：True；SHA256：`5b1a727d1787067775406325bbd66955d20657075d3cc0c823e1cc8a92485a28`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "health_education", "kind": "base", "block": null, "base_tables": ["health_education"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |


## S28

类别 `data`；来源 `python`；调用 `59dcfc8904b043a69e7ad2b8e091df3d`；状态 `success`。

```sql

SELECT "Campaign Format (Poster/Video/Lecture)" AS format,
       "Key Locations (School/Hospital/Community)" AS location,
       "Campaign Content (Prevention/Treatment/Policy)" AS content,
       "Behavioral Change Assessment" AS behav,
       "Effectiveness Tracking" AS track,
       "Effectiveness Assessment" AS eff,
       "Campaign Frequency (times/month)" AS freq,
       "Distribution Quantity" AS qty,
       "Awareness Rate Survey" AS awareness,
       "Knowledge Assessment" AS knowledge
FROM health_education
WHERE "Population Covered" = 'Student'

```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-044/attempt-01/sql/S28.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-044/attempt-01/sql/S28.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-044/attempt-01/results/S28.rows.jsonl)；完整：True；SHA256：`d8781c6ee637545e61ac02740a19aec73fa7b7aec29f3d65c8ec85029f3bfcc0`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "health_education", "kind": "base", "block": null, "base_tables": ["health_education"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |


## S29

类别 `data`；来源 `query_db`；调用 `d35b62b05e05462a9ff21f01842101e9`；状态 `success`。

```sql
SELECT
  "Campaign Format (Poster/Video/Lecture)" AS format,
  "Key Locations (School/Hospital/Community)" AS location,
  COUNT(*) AS n,
  ROUND(100.0 * SUM(CASE WHEN "Behavioral Change Assessment"='Significant' THEN 1 ELSE 0 END)/COUNT(*),1) AS behav_sig_pct,
  ROUND(100.0 * SUM(CASE WHEN "Effectiveness Tracking"='Significant' THEN 1 ELSE 0 END)/COUNT(*),1) AS track_sig_pct,
  ROUND(100.0 * SUM(CASE WHEN "Effectiveness Assessment"='Significant' THEN 1 ELSE 0 END)/COUNT(*),1) AS eff_sig_pct,
  ROUND(100.0 * SUM(CASE WHEN "Behavioral Change Assessment"='Significant' AND "Effectiveness Tracking"='Significant' THEN 1 ELSE 0 END)/COUNT(*),1) AS both_sig_pct
FROM health_education
WHERE "Population Covered" = 'Student'
GROUP BY format, location
ORDER BY format, location
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-044/attempt-01/sql/S29.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-044/attempt-01/sql/S29.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-044/attempt-01/results/S29.rows.jsonl)；完整：True；SHA256：`c6131a2c0528f3c1b88bda590d456576d7cffb0a90b5dfed6e8bd6f16baf903c`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "health_education", "kind": "base", "block": null, "base_tables": ["health_education"]}] | [] | ["\"Campaign Format (Poster/Video/Lecture)\"", "\"Key Locations (School/Hospital/Community)\""] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |
| B1 | COUNT(*) | [] | [] | True |
| B1 | COUNT(*) | [] | [] | True |
| B1 | COUNT(*) | [] | [] | True |
| B1 | COUNT(*) | [] | [] | True |
| B1 | SUM(CASE WHEN "Behavioral Change Assessment" = 'Significant' THEN 1 ELSE 0 END) | [] | [{"table": "health_education", "column": "Behavioral Change Assessment"}] | False |
| B1 | SUM(CASE WHEN "Effectiveness Tracking" = 'Significant' THEN 1 ELSE 0 END) | [] | [{"table": "health_education", "column": "Effectiveness Tracking"}] | False |
| B1 | SUM(CASE WHEN "Effectiveness Assessment" = 'Significant' THEN 1 ELSE 0 END) | [] | [{"table": "health_education", "column": "Effectiveness Assessment"}] | False |
| B1 | SUM(CASE WHEN "Behavioral Change Assessment" = 'Significant' AND "Effectiveness Tracking" = 'Significant' THEN 1 ELSE 0 END) | [] | [{"table": "health_education", "column": "Behavioral Change Assessment"}, {"table": "health_education", "column": "Effectiveness Tracking"}] | False |


## S30

类别 `data`；来源 `query_db`；调用 `aebc5aa9400340cda9af2f47be0c31c9`；状态 `success`。

```sql
SELECT
  "Campaign Format (Poster/Video/Lecture)" AS format,
  COUNT(*) AS n,
  ROUND(100.0 * SUM(CASE WHEN "Behavioral Change Assessment"='Significant' AND "Effectiveness Tracking"='Significant' THEN 1 ELSE 0 END)/COUNT(*),1) AS both_sig_pct,
  SUM(CASE WHEN "Behavioral Change Assessment"='Significant' AND "Effectiveness Tracking"='Significant' THEN 1 ELSE 0 END) AS both_sig_n
FROM health_education
WHERE "Population Covered" = 'Student'
GROUP BY format
ORDER BY both_sig_pct DESC
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-044/attempt-01/sql/S30.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-044/attempt-01/sql/S30.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-044/attempt-01/results/S30.rows.jsonl)；完整：True；SHA256：`41c7530b5368e2d7ea32ebbb09d75ec124ed31f4f4002f184bcfefe109386cc6`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "health_education", "kind": "base", "block": null, "base_tables": ["health_education"]}] | [] | ["\"Campaign Format (Poster/Video/Lecture)\""] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |
| B1 | SUM(CASE WHEN "Behavioral Change Assessment" = 'Significant' AND "Effectiveness Tracking" = 'Significant' THEN 1 ELSE 0 END) | [] | [{"table": "health_education", "column": "Behavioral Change Assessment"}, {"table": "health_education", "column": "Effectiveness Tracking"}] | False |
| B1 | COUNT(*) | [] | [] | True |
| B1 | SUM(CASE WHEN "Behavioral Change Assessment" = 'Significant' AND "Effectiveness Tracking" = 'Significant' THEN 1 ELSE 0 END) | [] | [{"table": "health_education", "column": "Behavioral Change Assessment"}, {"table": "health_education", "column": "Effectiveness Tracking"}] | False |


## S31

类别 `data`；来源 `query_db`；调用 `401c9d1982d04360a326c882cd339f0a`；状态 `success`。

```sql
SELECT
  "Key Locations (School/Hospital/Community)" AS location,
  COUNT(*) AS n,
  ROUND(100.0 * SUM(CASE WHEN "Behavioral Change Assessment"='Significant' AND "Effectiveness Tracking"='Significant' THEN 1 ELSE 0 END)/COUNT(*),1) AS both_sig_pct,
  SUM(CASE WHEN "Behavioral Change Assessment"='Significant' AND "Effectiveness Tracking"='Significant' THEN 1 ELSE 0 END) AS both_sig_n
FROM health_education
WHERE "Population Covered" = 'Student'
GROUP BY location
ORDER BY both_sig_pct DESC
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-044/attempt-01/sql/S31.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-044/attempt-01/sql/S31.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-044/attempt-01/results/S31.rows.jsonl)；完整：True；SHA256：`aa401b5344b9ccf292e60f687f2a9cbea8978c36a456f0cedb4bbb5f4ce3e1ca`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "health_education", "kind": "base", "block": null, "base_tables": ["health_education"]}] | [] | ["\"Key Locations (School/Hospital/Community)\""] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |
| B1 | SUM(CASE WHEN "Behavioral Change Assessment" = 'Significant' AND "Effectiveness Tracking" = 'Significant' THEN 1 ELSE 0 END) | [] | [{"table": "health_education", "column": "Behavioral Change Assessment"}, {"table": "health_education", "column": "Effectiveness Tracking"}] | False |
| B1 | COUNT(*) | [] | [] | True |
| B1 | SUM(CASE WHEN "Behavioral Change Assessment" = 'Significant' AND "Effectiveness Tracking" = 'Significant' THEN 1 ELSE 0 END) | [] | [{"table": "health_education", "column": "Behavioral Change Assessment"}, {"table": "health_education", "column": "Effectiveness Tracking"}] | False |


## S32

类别 `data`；来源 `python`；调用 `39246dbbb82e45d1948aef9763c12911`；状态 `success`。

```sql

SELECT "Campaign Format (Poster/Video/Lecture)" AS format,
       "Key Locations (School/Hospital/Community)" AS location,
       "Behavioral Change Assessment" AS behav,
       "Effectiveness Tracking" AS track,
       "Effectiveness Assessment" AS eff,
       "Campaign Frequency (times/month)" AS freq,
       "Distribution Quantity" AS qty
FROM health_education
WHERE "Population Covered" = 'Student'

```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-044/attempt-01/sql/S32.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-044/attempt-01/sql/S32.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-044/attempt-01/results/S32.rows.jsonl)；完整：True；SHA256：`94799bb68f4dbb610a3e9655c2f490a60251cf7ff7809cf6990052ec1f76204b`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "health_education", "kind": "base", "block": null, "base_tables": ["health_education"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |

