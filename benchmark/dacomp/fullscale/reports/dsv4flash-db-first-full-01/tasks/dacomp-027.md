# dacomp-027

Across disaster events at different global Disaster Levels, analyze how secondary or casca…

运行：已提交。官方未评分。全部 SQL 尝试/成功 38/38；数据 SQL 36/36；Python 9 次。

完整原题：

Across disaster events at different global Disaster Levels, analyze how secondary or cascading hazards lead to sustained negative impacts on people and the environment. Provide targeted, constructive recommendations based on the analysis results.

| 表 | 行数 | 列数 |
| --- | --- | --- |
| beneficiaries_and_assessments | 999 | 10 |
| coordination_and_evaluation | 999 | 29 |
| disaster_events | 999 | 9 |
| distribution_hubs | 999 | 11 |
| environment_and_health | 999 | 13 |
| financials1 | 999 | 13 |
| human_resources | 999 | 4 |
| operations1 | 999 | 12 |
| supplies1 | 999 | 4 |
| transportation1 | 999 | 18 |


实际路线（分析者依据 SQL/源码概括，不代表 Agent 自述）：关联灾害等级、次生事故、环境健康与运营数据 → 相关及分类关联检验 → 分箱比较疾病、资源缺口和反馈 → 细查交通限制与卫生指标并绘图。

数据库大小：3,694,592 字节。

## 数据 SQL

| SQL | 状态 | 基础表 | Join 输入/类型 | GROUP BY | 聚合表达式 | 结果行数 | 数据库 ms |
| --- | --- | --- | --- | --- | --- | --- | --- |
| [S3/Q1](#s3) | success | ["disaster_events"] | 0 / {} | ["\"Disaster Level\""] | ["COUNT(*)", "COUNT(DISTINCT \"Disaster Event ID\")"] | 5 | 1.308 |
| [S4/Q2](#s4) | success | ["disaster_events"] | 0 / {} | [] | [] | 5 | 0.339 |
| [S5/Q3](#s5) | success | ["coordination_and_evaluation"] | 0 / {} | [] | [] | 5 | 0.4 |
| [S6/Q4](#s6) | success | ["environment_and_health"] | 0 / {} | [] | [] | 5 | 0.354 |
| [S7/Q5](#s7) | success | ["beneficiaries_and_assessments", "coordination_and_evaluation", "disaster_events", "distribution_hubs", "environment_and_health", "financials1", "human_resources", "operations1", "supplies1", "transportation1"] | 0 / {} | [] | ["COUNT(*)", "COUNT(*)", "COUNT(*)", "COUNT(*)", "COUNT(*)", "COUNT(*)", "COUNT(*)", "COUNT(*)", "COUNT(*)", "COUNT(*)"] | 1 | 1.509 |
| [S8/Q6](#s8) | success | ["coordination_and_evaluation", "disaster_events"] | 2 / {'LEFT': 1} | [] | ["COUNT(*)"] | 1 | 1.714 |
| [S9/Q7](#s9) | success | ["coordination_and_evaluation", "disaster_events"] | 2 / {'INNER': 1} | ["d.\"Disaster Level\""] | ["COUNT(*)", "MIN(c.\"Secincident Count\")", "MAX(c.\"Secincident Count\")", "AVG(c.\"Secincident Count\")"] | 5 | 2.138 |
| [S10/Q8](#s10) | success | ["disaster_events"] | 0 / {} | [] | [] | 3 | 0.412 |
| [S11/Q9](#s11) | success | ["disaster_events"] | 0 / {} | ["\"Disaster Type\""] | ["COUNT(*)"] | 5 | 0.692 |
| [S12/Q10](#s12) | success | ["disaster_events"] | 0 / {} | ["\"Disaster Level\""] | ["AVG(JSON_EXTRACT(\"Impact Indicator\", '$.population.affected'))", "AVG(JSON_EXTRACT(\"Impact Indicator\", '$.population.displaced'))", "AVG(JSON_EXTRACT(\"Impact Indicator\", '$.population.casualties'))", "AVG(JSON_EXTRACT(\"Impact Indicator\", '$.population.injured'))", "AVG(JSON_EXTRACT(\"Impact Indicator\", '$.infrastructure.damage_percent'))"] | 5 | 3.061 |
| [S13/Q11](#s13) | success | ["environment_and_health"] | 0 / {} | ["e.\"Environmental Impact Rate\""] | ["COUNT(*)"] | 3 | 0.639 |
| [S14/Q12](#s14) | success | ["environment_and_health"] | 0 / {} | ["e.\"Disease Risk\""] | ["COUNT(*)"] | 3 | 0.65 |
| [S15/Q13](#s15) | success | ["environment_and_health"] | 0 / {} | ["e.\"Mental Health Assistance\""] | ["COUNT(*)"] | 2 | 0.651 |
| [S16/Q14](#s16) | success | ["environment_and_health"] | 0 / {} | ["e.\"Medical Emergency Response Capacity\""] | ["COUNT(*)"] | 3 | 0.678 |
| [S17/Q15](#s17) | success | ["environment_and_health"] | 0 / {} | ["e.\"Waste Management Status\""] | ["COUNT(*)"] | 3 | 0.641 |
| [S18/Q16](#s18) | success | ["coordination_and_evaluation", "disaster_events", "environment_and_health"] | 3 / {'INNER': 2} | ["CASE WHEN c.\"Secincident Count\" < 33 THEN 'Low (0-32)' WHEN c.\"Secincident Count\" < 66 THEN 'Medium (33-65)' ELSE 'High (66-100)' END"] | ["COUNT(*)", "AVG(e.\"Water Quality Index\")", "AVG(e.\"Sanitation Coverage Rate\")", "AVG(e.\"Carbon Emissions (tons)\")", "AVG(e.\"Recycling Rate (%)\")", "AVG(e.\"Renewable Energy Share (%)\")", "AVG(e.\"Vaccination Coverage Rate\")"] | 3 | 4.202 |
| [S19/Q17](#s19) | success | ["coordination_and_evaluation", "disaster_events"] | 2 / {'INNER': 1} | ["CASE WHEN c.\"Secincident Count\" < 33 THEN 'Low (0-32)' WHEN c.\"Secincident Count\" < 66 THEN 'Medium (33-65)' ELSE 'High (66-100)' END"] | ["COUNT(*)", "AVG(JSON_EXTRACT(d.\"Impact Indicator\", '$.population.affected'))", "AVG(JSON_EXTRACT(d.\"Impact Indicator\", '$.population.displaced'))", "AVG(JSON_EXTRACT(d.\"Impact Indicator\", '$.population.casualties'))", "AVG(JSON_EXTRACT(d.\"Impact Indicator\", '$.infrastructure.damage_percent'))", "AVG(JSON_EXTRACT(d.\"Impact Indicator\", '$.infrastructure.power_outage_percent'))"] | 3 | 4.454 |
| [S20/Q18](#s20) | success | ["disaster_events", "environment_and_health"] | 2 / {'INNER': 1} | ["d.\"Disaster Level\"", "e.\"Environmental Impact Rate\""] | ["COUNT(*)"] | 15 | 2.166 |
| [S21/Q19](#s21) | success | ["disaster_events", "environment_and_health"] | 2 / {'INNER': 1} | ["d.\"Disaster Level\"", "e.\"Disease Risk\""] | ["COUNT(*)"] | 15 | 2.225 |
| [S22/Q20](#s22) | success | ["disaster_events", "environment_and_health"] | 2 / {'INNER': 1} | ["d.\"Disaster Level\"", "e.\"Mental Health Assistance\""] | ["COUNT(*)"] | 10 | 2.245 |
| [S23/Q21](#s23) | success | ["disaster_events", "distribution_hubs", "financials1", "operations1", "transportation1"] | 5 / {'INNER': 4} | ["d.\"Disaster Level\""] | ["AVG(o.\"Estimated Duration (days)\")", "AVG(f.\"resourcegaps(USD)\")", "AVG(f.\"fundsutilpct(%)\")", "AVG(f.\"costbene(USD)\")", "AVG(t.\"Delivery Success Rate\")", "AVG(t.\"Average Delivery Time\")", "AVG(h.\"Utilization (%)\")"] | 5 | 8.873 |
| [S24/Q22](#s24) | success | ["coordination_and_evaluation", "disaster_events"] | 2 / {'INNER': 1} | ["d.\"Disaster Level\"", "c.\"evaluationstage\""] | ["COUNT(*)"] | 15 | 2.252 |
| [S25/Q23](#s25) | success | ["coordination_and_evaluation", "disaster_events", "distribution_hubs", "financials1", "operations1", "transportation1"] | 6 / {'INNER': 5} | ["CASE WHEN c.\"Secincident Count\" < 33 THEN 'Low (0-32)' WHEN c.\"Secincident Count\" < 66 THEN 'Medium (33-65)' ELSE 'High (66-100)' END"] | ["AVG(o.\"Estimated Duration (days)\")", "AVG(f.\"resourcegaps(USD)\")", "AVG(f.\"fundsutilpct(%)\")", "AVG(t.\"Delivery Success Rate\")", "AVG(t.\"Average Delivery Time\")", "AVG(h.\"Utilization (%)\")", "AVG(c.\"stakeholdersatisf\")", "AVG(c.\"publicperception\")", "AVG(c.\"reportcompliance\")"] | 3 | 8.084 |
| [S26/Q24](#s26) | success | ["coordination_and_evaluation", "disaster_events", "environment_and_health"] | 3 / {'INNER': 2} | ["CASE WHEN c.\"Secincident Count\" < 33 THEN 'Low (0-32)' WHEN c.\"Secincident Count\" < 66 THEN 'Medium (33-65)' ELSE 'High (66-100)' END", "e.\"Environmental Impact Rate\""] | ["COUNT(*)"] | 9 | 3.418 |
| [S27/Q25](#s27) | success | ["coordination_and_evaluation", "disaster_events", "environment_and_health", "financials1", "operations1", "transportation1"] | 6 / {'INNER': 5} | [] | [] | 999 | 17.834 |
| [S28/Q26](#s28) | success | ["coordination_and_evaluation", "disaster_events", "operations1"] | 3 / {'INNER': 2} | [] | [] | 999 | 8.956 |
| [S29/Q27](#s29) | success | ["coordination_and_evaluation"] | 0 / {} | [] | [] | 5 | 0.314 |
| [S30/Q28](#s30) | success | ["coordination_and_evaluation"] | 0 / {} | [] | [] | 999 | 1.183 |
| [S31/Q29](#s31) | success | ["coordination_and_evaluation"] | 0 / {} | [] | [] | 999 | 0.963 |
| [S32/Q30](#s32) | success | ["disaster_events"] | 0 / {} | [] | [] | 999 | 3.565 |
| [S33/Q31](#s33) | success | ["financials1"] | 0 / {} | ["\"fundingstate\""] | ["COUNT(*)"] | 3 | 0.639 |
| [S34/Q32](#s34) | success | ["coordination_and_evaluation", "financials1"] | 2 / {'INNER': 1} | [] | [] | 999 | 3.089 |
| [S35/Q33](#s35) | success | ["coordination_and_evaluation"] | 0 / {} | [] | [] | 999 | 1.326 |
| [S36/Q34](#s36) | success | ["coordination_and_evaluation"] | 0 / {} | [] | [] | 999 | 1.269 |
| [S37/Q35](#s37) | success | ["disaster_events"] | 0 / {} | ["\"Disaster Level\""] | ["AVG(JSON_EXTRACT(\"Impact Indicator\", '$.infrastructure.damage_percent'))", "AVG(JSON_EXTRACT(\"Impact Indicator\", '$.infrastructure.power_outage_percent'))", "AVG(JSON_EXTRACT(\"Impact Indicator\", '$.infrastructure.water_damage_percent'))"] | 5 | 2.484 |
| [S38/Q36](#s38) | success | ["coordination_and_evaluation", "disaster_events", "environment_and_health"] | 3 / {'INNER': 2} | [] | [] | 999 | 5.374 |


## 元数据和设置

| SQL | 类别 | 状态 | 内容 |
| --- | --- | --- | --- |
| S1 | connection_setup | success | PRAGMA query_only=ON |
| S2 | metadata | success | SELECT name,sql FROM sqlite_master WHERE type='table' ORDER BY name |


## Python 与执行位置

人工源码审查：**database_first_violation**。SQL builds joined disaster/environment/coordination inputs. Python executes legitimate correlation and chi-square tests, but also bins incident counts, merges damage attributes, computes grouped financial/environmental means and normalized contingency summaries for reporting and figures. Those SQL-capable grouping/join/conditional proportions are deviations; chi-square evaluation itself is a statistical exception. [证据](../reviews/dacomp-027.json)。

P1：Statistical correlation analysis (Pearson, Spearman) and categorical association tests (chi-square, ANOVA) are statistical procedures not supported by SQLite. I'll pull only the needed joined columns and test the relationship between secondary-hazard counts and human/environmental impact indicators.

[源码](../../../runs/dsv4flash-db-first-full-01/dacomp-027/attempt-01/python/P1.py)；[输出](../../../runs/dsv4flash-db-first-full-01/dacomp-027/attempt-01/python/P1.stdout)；[错误](../../../runs/dsv4flash-db-first-full-01/dacomp-027/attempt-01/python/P1.stderr)。检出需人工核验的 SQL 可实现操作：.query(；不能仅凭理由判为合规。

P2：Compute Pearson correlation between Secincident Count (secondary hazard measure) and all numeric impact indicators to detect any linear relationships. Also compute ANOVA for categorical outcomes by high/low secondary incident groups. This requires statistical computation not available in SQLite.

[源码](../../../runs/dsv4flash-db-first-full-01/dacomp-027/attempt-01/python/P2.py)；[输出](../../../runs/dsv4flash-db-first-full-01/dacomp-027/attempt-01/python/P2.stdout)；[错误](../../../runs/dsv4flash-db-first-full-01/dacomp-027/attempt-01/python/P2.stderr)。检出需人工核验的 SQL 可实现操作：groupby(, sort_values(；不能仅凭理由判为合规。

P3：Run chi-square tests between secondary-hazard groups and coordination/operational categorical variables (safety, access, coordination level, evaluation stages, response phase, operation status) plus examine disease-risk proportions; these association tests are statistical procedures not supported by SQLite.

[源码](../../../runs/dsv4flash-db-first-full-01/dacomp-027/attempt-01/python/P3.py)；[输出](../../../runs/dsv4flash-db-first-full-01/dacomp-027/attempt-01/python/P3.stdout)；[错误](../../../runs/dsv4flash-db-first-full-01/dacomp-027/attempt-01/python/P3.stderr)。检出需人工核验的 SQL 可实现操作：groupby(, .query(；不能仅凭理由判为合规。

P4：Deep-dive statistical comparisons: t-tests on vaccination and other continuous indicators between secondary-hazard groups, and check interactions with Disaster Level (e.g., high-secondary events at higher levels). These are statistical procedures not available in SQLite.

[源码](../../../runs/dsv4flash-db-first-full-01/dacomp-027/attempt-01/python/P4.py)；[输出](../../../runs/dsv4flash-db-first-full-01/dacomp-027/attempt-01/python/P4.stdout)；[错误](../../../runs/dsv4flash-db-first-full-01/dacomp-027/attempt-01/python/P4.stderr)。检出需人工核验的 SQL 可实现操作：groupby(；不能仅凭理由判为合规。

P5：Create visualizations of key findings: disease risk proportions by secondary incident group, vaccination coverage among high-risk events, monitoring frequency patterns, and audit status. Also check nextreviewdate patterns. Statistical visualization is a Python task.

[源码](../../../runs/dsv4flash-db-first-full-01/dacomp-027/attempt-01/python/P5.py)；[输出](../../../runs/dsv4flash-db-first-full-01/dacomp-027/attempt-01/python/P5.stdout)；[错误](../../../runs/dsv4flash-db-first-full-01/dacomp-027/attempt-01/python/P5.stderr)。检出需人工核验的 SQL 可实现操作：groupby(, .query(；不能仅凭理由判为合规。

P6：Fix the review date analysis and rerun the remaining visualizations (the key figures were saved). Also compute overdue review proportions.

[源码](../../../runs/dsv4flash-db-first-full-01/dacomp-027/attempt-01/python/P6.py)；[输出](../../../runs/dsv4flash-db-first-full-01/dacomp-027/attempt-01/python/P6.stdout)；[错误](../../../runs/dsv4flash-db-first-full-01/dacomp-027/attempt-01/python/P6.stderr)。检出需人工核验的 SQL 可实现操作：groupby(, .query(；不能仅凭理由判为合规。

P7：Examine damage level from impact JSON by secondary-hazard group, compute effect size (Cramer's V) for disease-risk association, and check for interaction patterns (high-secondary events at higher disaster levels). This requires parsing JSON fields and statistical measures outside SQLite's capabilities.

[源码](../../../runs/dsv4flash-db-first-full-01/dacomp-027/attempt-01/python/P7.py)；[输出](../../../runs/dsv4flash-db-first-full-01/dacomp-027/attempt-01/python/P7.stdout)；[错误](../../../runs/dsv4flash-db-first-full-01/dacomp-027/attempt-01/python/P7.stderr)。检出需人工核验的 SQL 可实现操作：groupby(, .merge(, .query(；不能仅凭理由判为合规。

P8：Check funding state vs sec group and other financial patterns. Also summarize the key findings for the report.

[源码](../../../runs/dsv4flash-db-first-full-01/dacomp-027/attempt-01/python/P8.py)；[输出](../../../runs/dsv4flash-db-first-full-01/dacomp-027/attempt-01/python/P8.stdout)；[错误](../../../runs/dsv4flash-db-first-full-01/dacomp-027/attempt-01/python/P8.stderr)。检出需人工核验的 SQL 可实现操作：groupby(, .query(；不能仅凭理由判为合规。

P9：Final analysis: check if events with severe access limitation AND high secondary incidents have amplified negative health outcomes, and compute the interaction between access limitation and disease risk.

[源码](../../../runs/dsv4flash-db-first-full-01/dacomp-027/attempt-01/python/P9.py)；[输出](../../../runs/dsv4flash-db-first-full-01/dacomp-027/attempt-01/python/P9.stdout)；[错误](../../../runs/dsv4flash-db-first-full-01/dacomp-027/attempt-01/python/P9.stderr)。检出需人工核验的 SQL 可实现操作：groupby(, .query(；不能仅凭理由判为合规。

## 优化机会

已验证候选。筛选限于精确 SQL、相同自包含 CTE、相同单表完整过滤、可分解单表聚合；未覆盖任意 Join 等价和一般谓词蕴含。全部候选都是 offline，未测在线预测。

| 候选 | 类型 | 已有结果 | 覆盖 SQL | 后续次数 | 中间行数 | 验证 | 成本 |
| --- | --- | --- | --- | --- | --- | --- | --- |
| C1 | aggregate MV | False | ["S11", "S12", "S37"] | 2 | 25 | verified | Not benchmarked; correctness alone does not establish net speedup. |
| C2 | aggregate MV | False | ["S13", "S14", "S15", "S16", "S17"] | 4 | 159 | verified | Not benchmarked; correctness alone does not establish net speedup. |


已验证覆盖（含触发查询、候选并集去重）：8/36 条成功数据 SQL。正确性仅针对当前数据库快照；未测性能的候选不能声称已加速。

[完整 build/rewrite 与比较证据](dacomp-027.analysis.json)。

### C2：aggregate MV

Union of grouping keys; decomposable aggregate states; AVG uses SUM and non-NULL COUNT.

原查询 [S13](#s13), [S14](#s14), [S15](#s15), [S16](#s16), [S17](#s17) → 新增共享状态 C2 → 后续 4 次可复用。该构建点为事后假设，不代表 Agent 当时预知后续。

构建定义：

```sql
SELECT "Environmental Impact Rate" AS __g0, "Disease Risk" AS __g1, "Mental Health Assistance" AS __g2, "Medical Emergency Response Capacity" AS __g3, "Waste Management Status" AS __g4, COUNT(*) AS __a0 FROM "environment_and_health"  GROUP BY "Environmental Impact Rate", "Disease Risk", "Mental Health Assistance", "Medical Emergency Response Capacity", "Waste Management Status"
```

受益查询 S13 的改写示例：

```sql
SELECT __g0 AS "Environmental Impact Rate", SUM(__a0) AS n FROM temp.reuse_candidate GROUP BY __g0
```

| 原 SQL | 列名一致 | 结果一致 | 比较方法 |
| --- | --- | --- | --- |
| S13 | True | True | exact_multiset |
| S14 | True | True | exact_multiset |
| S15 | True | True | exact_multiset |
| S16 | True | True | exact_multiset |
| S17 | True | True | exact_multiset |


验证状态：verified；成本结论：Not benchmarked; correctness alone does not establish net speedup.

### C1：aggregate MV

Union of grouping keys; decomposable aggregate states; AVG uses SUM and non-NULL COUNT.

原查询 [S11](#s11), [S12](#s12), [S37](#s37) → 新增共享状态 C1 → 后续 2 次可复用。该构建点为事后假设，不代表 Agent 当时预知后续。

构建定义：

```sql
SELECT "Disaster Type" AS __g0, "Disaster Level" AS __g1, COUNT(*) AS __a0, SUM(JSON_EXTRACT("Impact Indicator", '$.population.affected')) AS __a1_sum, COUNT(JSON_EXTRACT("Impact Indicator", '$.population.affected')) AS __a1_n, SUM(JSON_EXTRACT("Impact Indicator", '$.population.displaced')) AS __a2_sum, COUNT(JSON_EXTRACT("Impact Indicator", '$.population.displaced')) AS __a2_n, SUM(JSON_EXTRACT("Impact Indicator", '$.population.casualties')) AS __a3_sum, COUNT(JSON_EXTRACT("Impact Indicator", '$.population.casualties')) AS __a3_n, SUM(JSON_EXTRACT("Impact Indicator", '$.population.injured')) AS __a4_sum, COUNT(JSON_EXTRACT("Impact Indicator", '$.population.injured')) AS __a4_n, SUM(JSON_EXTRACT("Impact Indicator", '$.infrastructure.damage_percent')) AS __a5_sum, COUNT(JSON_EXTRACT("Impact Indicator", '$.infrastructure.damage_percent')) AS __a5_n, SUM(JSON_EXTRACT("Impact Indicator", '$.infrastructure.power_outage_percent')) AS __a6_sum, COUNT(JSON_EXTRACT("Impact Indicator", '$.infrastructure.power_outage_percent')) AS __a6_n, SUM(JSON_EXTRACT("Impact Indicator", '$.infrastructure.water_damage_percent')) AS __a7_sum, COUNT(JSON_EXTRACT("Impact Indicator", '$.infrastructure.water_damage_percent')) AS __a7_n FROM "disaster_events"  GROUP BY "Disaster Type", "Disaster Level"
```

受益查询 S11 的改写示例：

```sql
SELECT __g0 AS "Disaster Type", SUM(__a0) AS n FROM temp.reuse_candidate GROUP BY __g0 ORDER BY n DESC
```

| 原 SQL | 列名一致 | 结果一致 | 比较方法 |
| --- | --- | --- | --- |
| S11 | True | True | ordered_numeric_tolerance |
| S12 | True | True | exact_multiset |
| S37 | True | True | exact_multiset |


验证状态：verified；成本结论：Not benchmarked; correctness alone does not establish net speedup.

结果依赖：自动记录 SQL→Python 的接口父调用，以及源码中引用归档文件的消费者；字面值相同不认定因果。模型方向选择需要人工读取消息，尚未做全面因果标注。

[原始报告](../../../runs/dsv4flash-db-first-full-01/dacomp-027/attempt-01/answer.md)；[统一消息](../../../runs/dsv4flash-db-first-full-01/dacomp-027/attempt-01/messages.jsonl)；[原始 OpenCode 事件](../../../runs/dsv4flash-db-first-full-01/dacomp-027/attempt-01/opencode.jsonl)；[SQL 引擎日志](../../../runs/dsv4flash-db-first-full-01/dacomp-027/attempt-01/sql_journal.jsonl)。

[可读报告（本地图片链接规范化）](../answers/dacomp-027.md)。原始回答保留，分析结论未改写。

## S1

类别 `connection_setup`；来源 `connection`；调用 `196fc7011ed643aa8f535c5ad335bcd1`；状态 `success`。

```sql
PRAGMA query_only=ON
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-027/attempt-01/sql/S1.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-027/attempt-01/sql/S1.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-027/attempt-01/results/S1.rows.jsonl)；完整：True；SHA256：`e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`。

## S2

类别 `metadata`；来源 `list_db`；调用 `196fc7011ed643aa8f535c5ad335bcd1`；状态 `success`。

```sql
SELECT name,sql FROM sqlite_master WHERE type='table' ORDER BY name
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-027/attempt-01/sql/S2.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-027/attempt-01/sql/S2.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-027/attempt-01/results/S2.rows.jsonl)；完整：True；SHA256：`9728992e78f21b2f89952bdf0d9c6ea9d872f70befe43d3a6679e29e2a889e58`。

## S3

类别 `data`；来源 `query_db`；调用 `8b9f4932730548e2b564d7e562c869ca`；状态 `success`。

```sql
SELECT "Disaster Level", COUNT(*) AS n, COUNT(DISTINCT "Disaster Event ID") AS events FROM disaster_events GROUP BY "Disaster Level"
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-027/attempt-01/sql/S3.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-027/attempt-01/sql/S3.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-027/attempt-01/results/S3.rows.jsonl)；完整：True；SHA256：`cde02bee650d288b2d67e46b3c6097cb1c19400c45c5c6962a6171976b0aabfc`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "disaster_events", "kind": "base", "block": null, "base_tables": ["disaster_events"]}] | [] | ["\"Disaster Level\""] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |
| B1 | COUNT(DISTINCT "Disaster Event ID") | [{"table": "disaster_events", "column": "Disaster Event ID"}] | [] | False |


## S4

类别 `data`；来源 `query_db`；调用 `89fc6025dbd74bfe9655bb6fcda2604e`；状态 `success`。

```sql
SELECT * FROM disaster_events LIMIT 5
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-027/attempt-01/sql/S4.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-027/attempt-01/sql/S4.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-027/attempt-01/results/S4.rows.jsonl)；完整：True；SHA256：`4422633ba8befe77c23eb3e2cf988b368585912fdd05782a2b3d1ca33389d723`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "disaster_events", "kind": "base", "block": null, "base_tables": ["disaster_events"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |


## S5

类别 `data`；来源 `query_db`；调用 `b4fe8e6860e743fc9708d4e4ddf7d987`；状态 `success`。

```sql
SELECT * FROM coordination_and_evaluation LIMIT 5
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-027/attempt-01/sql/S5.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-027/attempt-01/sql/S5.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-027/attempt-01/results/S5.rows.jsonl)；完整：True；SHA256：`66887d0711ff40e073922a8cbd0869dd0b24cab9c322ab0f4ee8d513acbf13ae`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "coordination_and_evaluation", "kind": "base", "block": null, "base_tables": ["coordination_and_evaluation"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |


## S6

类别 `data`；来源 `query_db`；调用 `5e85147849d644419800f29687e3f6ed`；状态 `success`。

```sql
SELECT * FROM environment_and_health LIMIT 5
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-027/attempt-01/sql/S6.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-027/attempt-01/sql/S6.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-027/attempt-01/results/S6.rows.jsonl)；完整：True；SHA256：`a754d7dae75ee8ae0925ac0d779a030daaf052d7ada9ac0dece2676641b3852b`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "environment_and_health", "kind": "base", "block": null, "base_tables": ["environment_and_health"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |


## S7

类别 `data`；来源 `query_db`；调用 `93af12ac33994bfcb72749dcce479eaf`；状态 `success`。

```sql
SELECT
 (SELECT COUNT(*) FROM disaster_events) AS events,
 (SELECT COUNT(*) FROM coordination_and_evaluation) AS coord,
 (SELECT COUNT(*) FROM environment_and_health) AS env,
 (SELECT COUNT(*) FROM operations1) AS ops,
 (SELECT COUNT(*) FROM financials1) AS fin,
 (SELECT COUNT(*) FROM distribution_hubs) AS hubs,
 (SELECT COUNT(*) FROM transportation1) AS trans,
 (SELECT COUNT(*) FROM supplies1) AS sup,
 (SELECT COUNT(*) FROM human_resources) AS hr,
 (SELECT COUNT(*) FROM beneficiaries_and_assessments) AS ben
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-027/attempt-01/sql/S7.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-027/attempt-01/sql/S7.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-027/attempt-01/results/S7.rows.jsonl)；完整：True；SHA256：`bf83b2b569ab5b33907df72013f8278967ac696effa1861524f286e1a5afdd5f`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "disaster_events", "kind": "base", "block": null, "base_tables": ["disaster_events"]}] | [] | [] |
| B2 | [{"alias": "coordination_and_evaluation", "kind": "base", "block": null, "base_tables": ["coordination_and_evaluation"]}] | [] | [] |
| B3 | [{"alias": "environment_and_health", "kind": "base", "block": null, "base_tables": ["environment_and_health"]}] | [] | [] |
| B4 | [{"alias": "operations1", "kind": "base", "block": null, "base_tables": ["operations1"]}] | [] | [] |
| B5 | [{"alias": "financials1", "kind": "base", "block": null, "base_tables": ["financials1"]}] | [] | [] |
| B6 | [{"alias": "distribution_hubs", "kind": "base", "block": null, "base_tables": ["distribution_hubs"]}] | [] | [] |
| B7 | [{"alias": "transportation1", "kind": "base", "block": null, "base_tables": ["transportation1"]}] | [] | [] |
| B8 | [{"alias": "supplies1", "kind": "base", "block": null, "base_tables": ["supplies1"]}] | [] | [] |
| B9 | [{"alias": "human_resources", "kind": "base", "block": null, "base_tables": ["human_resources"]}] | [] | [] |
| B10 | [{"alias": "beneficiaries_and_assessments", "kind": "base", "block": null, "base_tables": ["beneficiaries_and_assessments"]}] | [] | [] |
| B11 | [] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |
| B2 | COUNT(*) | [] | [] | True |
| B3 | COUNT(*) | [] | [] | True |
| B4 | COUNT(*) | [] | [] | True |
| B5 | COUNT(*) | [] | [] | True |
| B6 | COUNT(*) | [] | [] | True |
| B7 | COUNT(*) | [] | [] | True |
| B8 | COUNT(*) | [] | [] | True |
| B9 | COUNT(*) | [] | [] | True |
| B10 | COUNT(*) | [] | [] | True |


## S8

类别 `data`；来源 `query_db`；调用 `f43e25102fce42e1a2bc4cb0f1ee808a`；状态 `success`。

```sql
SELECT COUNT(*) AS missing_coord FROM disaster_events d LEFT JOIN coordination_and_evaluation c ON c."Distribution Reference ID" = d."Disaster Event ID" WHERE c."Coordevalregistry ID" IS NULL
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-027/attempt-01/sql/S8.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-027/attempt-01/sql/S8.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-027/attempt-01/results/S8.rows.jsonl)；完整：True；SHA256：`c14196f132c1e9be0508ae80ab52fcb3e1d3fc05880415f3dc980971df207c9e`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "d", "kind": "base", "block": null, "base_tables": ["disaster_events"]}, {"alias": "c", "kind": "base", "block": null, "base_tables": ["coordination_and_evaluation"]}] | [{"type": "LEFT", "right": "coordination_and_evaluation AS c", "on": "c.\"Distribution Reference ID\" = d.\"Disaster Event ID\"", "using": []}] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |


## S9

类别 `data`；来源 `query_db`；调用 `9f7ce3672bd349f2aa466539d93f9bf9`；状态 `success`。

```sql
SELECT d."Disaster Level", COUNT(*) AS n, ROUND(AVG(c."Secincident Count"),1) AS avg_sec, MIN(c."Secincident Count") AS min_sec, MAX(c."Secincident Count") AS max_sec
FROM disaster_events d JOIN coordination_and_evaluation c ON c."Distribution Reference ID" = d."Disaster Event ID"
GROUP BY d."Disaster Level"
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-027/attempt-01/sql/S9.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-027/attempt-01/sql/S9.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-027/attempt-01/results/S9.rows.jsonl)；完整：True；SHA256：`5d3ea0fd3ac0d33d2d32d6fc55a59fec16b3c5127758c9061566b0f51c0525d8`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "d", "kind": "base", "block": null, "base_tables": ["disaster_events"]}, {"alias": "c", "kind": "base", "block": null, "base_tables": ["coordination_and_evaluation"]}] | [{"type": "INNER", "right": "coordination_and_evaluation AS c", "on": "c.\"Distribution Reference ID\" = d.\"Disaster Event ID\"", "using": []}] | ["d.\"Disaster Level\""] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |
| B1 | MIN(c."Secincident Count") | [{"table": "coordination_and_evaluation", "column": "Secincident Count"}] | [] | False |
| B1 | MAX(c."Secincident Count") | [{"table": "coordination_and_evaluation", "column": "Secincident Count"}] | [] | False |
| B1 | AVG(c."Secincident Count") | [{"table": "coordination_and_evaluation", "column": "Secincident Count"}] | [] | False |


## S10

类别 `data`；来源 `query_db`；调用 `8803f7706d0747de87d7a325aed2d5c6`；状态 `success`。

```sql
SELECT "Disaster Event ID",
 json_extract("Impact Indicator", '$.population.affected') AS affected,
 json_extract("Impact Indicator", '$.population.displaced') AS displaced,
 json_extract("Impact Indicator", '$.population.injured') AS injured,
 json_extract("Impact Indicator", '$.population.casualties') AS casualties,
 json_extract("Impact Indicator", '$.population.missing') AS missing,
 json_extract("Impact Indicator", '$.damage_level') AS damage_level,
 json_extract("Impact Indicator", '$.infrastructure.damage_percent') AS damage_pct,
 json_extract("Impact Indicator", '$.infrastructure.power_outage_percent') AS power_pct,
 json_extract("Impact Indicator", '$.infrastructure.water_damage_percent') AS water_pct,
 json_extract("Impact Indicator", '$.communication') AS comm,
 json_extract("Impact Indicator", '$.transportation') AS transp
FROM disaster_events LIMIT 3
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-027/attempt-01/sql/S10.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-027/attempt-01/sql/S10.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-027/attempt-01/results/S10.rows.jsonl)；完整：True；SHA256：`aa784e9b881a59e99d3833b8878d03c14e3009e6a27a03ddbfd28b4c82bda953`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "disaster_events", "kind": "base", "block": null, "base_tables": ["disaster_events"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |


## S11

类别 `data`；来源 `query_db`；调用 `d3b5e38a96ed4b3c8fdbba1b6b51411c`；状态 `success`。

```sql
SELECT "Disaster Type", COUNT(*) n FROM disaster_events GROUP BY "Disaster Type" ORDER BY n DESC
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-027/attempt-01/sql/S11.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-027/attempt-01/sql/S11.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-027/attempt-01/results/S11.rows.jsonl)；完整：True；SHA256：`070545aded3ab80c3cce7fc5e222f62a230895519db12a3d0b150aba6d8459b4`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "disaster_events", "kind": "base", "block": null, "base_tables": ["disaster_events"]}] | [] | ["\"Disaster Type\""] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |


## S12

类别 `data`；来源 `query_db`；调用 `f25c7fb293054a0fb39f365615118891`；状态 `success`。

```sql
SELECT "Disaster Level", ROUND(AVG(json_extract("Impact Indicator",'$.population.affected')),0) avg_affected, ROUND(AVG(json_extract("Impact Indicator",'$.population.displaced')),0) avg_displaced, ROUND(AVG(json_extract("Impact Indicator",'$.population.casualties')),2) avg_casualties, ROUND(AVG(json_extract("Impact Indicator",'$.population.injured')),1) avg_injured, ROUND(AVG(json_extract("Impact Indicator",'$.infrastructure.damage_percent')),1) avg_damage FROM disaster_events GROUP BY "Disaster Level"
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-027/attempt-01/sql/S12.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-027/attempt-01/sql/S12.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-027/attempt-01/results/S12.rows.jsonl)；完整：True；SHA256：`15932067aaa4367a5d5f9f29a31b583e9a8607f74ac45cab1cecd8ab681de1b6`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "disaster_events", "kind": "base", "block": null, "base_tables": ["disaster_events"]}] | [] | ["\"Disaster Level\""] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | AVG(JSON_EXTRACT("Impact Indicator", '$.population.affected')) | [{"table": "disaster_events", "column": "Impact Indicator"}] | [] | False |
| B1 | AVG(JSON_EXTRACT("Impact Indicator", '$.population.displaced')) | [{"table": "disaster_events", "column": "Impact Indicator"}] | [] | False |
| B1 | AVG(JSON_EXTRACT("Impact Indicator", '$.population.casualties')) | [{"table": "disaster_events", "column": "Impact Indicator"}] | [] | False |
| B1 | AVG(JSON_EXTRACT("Impact Indicator", '$.population.injured')) | [{"table": "disaster_events", "column": "Impact Indicator"}] | [] | False |
| B1 | AVG(JSON_EXTRACT("Impact Indicator", '$.infrastructure.damage_percent')) | [{"table": "disaster_events", "column": "Impact Indicator"}] | [] | False |


## S13

类别 `data`；来源 `query_db`；调用 `5eab5c0180d6484e961b48d6df4f464b`；状态 `success`。

```sql
SELECT e."Environmental Impact Rate", COUNT(*) n FROM environment_and_health e GROUP BY e."Environmental Impact Rate"
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-027/attempt-01/sql/S13.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-027/attempt-01/sql/S13.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-027/attempt-01/results/S13.rows.jsonl)；完整：True；SHA256：`8e594dd09f0f31476f4b87e4c2413ba753a89ccb242238166e022f598e3f36e6`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "e", "kind": "base", "block": null, "base_tables": ["environment_and_health"]}] | [] | ["e.\"Environmental Impact Rate\""] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |


## S14

类别 `data`；来源 `query_db`；调用 `e1e6c2169ad64f6d9c866520e0516fd4`；状态 `success`。

```sql
SELECT e."Disease Risk", COUNT(*) n FROM environment_and_health e GROUP BY e."Disease Risk"
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-027/attempt-01/sql/S14.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-027/attempt-01/sql/S14.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-027/attempt-01/results/S14.rows.jsonl)；完整：True；SHA256：`3a37f18080ed0d6cfe7ae5ea1f49ebf101acd41997a931c58479e0c038b76118`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "e", "kind": "base", "block": null, "base_tables": ["environment_and_health"]}] | [] | ["e.\"Disease Risk\""] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |


## S15

类别 `data`；来源 `query_db`；调用 `6ab56a93c147426e84c4bf139c16aeeb`；状态 `success`。

```sql
SELECT e."Mental Health Assistance", COUNT(*) n FROM environment_and_health e GROUP BY e."Mental Health Assistance"
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-027/attempt-01/sql/S15.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-027/attempt-01/sql/S15.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-027/attempt-01/results/S15.rows.jsonl)；完整：True；SHA256：`17607bb53285db913b97af88359366d4c241b3cffb71d0369af5878357ad528f`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "e", "kind": "base", "block": null, "base_tables": ["environment_and_health"]}] | [] | ["e.\"Mental Health Assistance\""] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |


## S16

类别 `data`；来源 `query_db`；调用 `c557a2f80ba647009e68e2a7618ff0b8`；状态 `success`。

```sql
SELECT e."Medical Emergency Response Capacity", COUNT(*) n FROM environment_and_health e GROUP BY e."Medical Emergency Response Capacity"
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-027/attempt-01/sql/S16.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-027/attempt-01/sql/S16.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-027/attempt-01/results/S16.rows.jsonl)；完整：True；SHA256：`f7d871b0e73d456104c5f3434cb03a8ae1a2494c481384d040298abe3413161d`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "e", "kind": "base", "block": null, "base_tables": ["environment_and_health"]}] | [] | ["e.\"Medical Emergency Response Capacity\""] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |


## S17

类别 `data`；来源 `query_db`；调用 `b07ed161a3604c97ae2f8b30ad7e3412`；状态 `success`。

```sql
SELECT e."Waste Management Status", COUNT(*) n FROM environment_and_health e GROUP BY e."Waste Management Status"
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-027/attempt-01/sql/S17.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-027/attempt-01/sql/S17.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-027/attempt-01/results/S17.rows.jsonl)；完整：True；SHA256：`7fa669b17ca2f2deab1b3acaafa34f1e54c48702c1a911b6da5ba8bc61e69403`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "e", "kind": "base", "block": null, "base_tables": ["environment_and_health"]}] | [] | ["e.\"Waste Management Status\""] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |


## S18

类别 `data`；来源 `query_db`；调用 `4d98d170f01f40cb86577cf586cdf7f6`；状态 `success`。

```sql
SELECT
 CASE
   WHEN c."Secincident Count" < 33 THEN 'Low (0-32)'
   WHEN c."Secincident Count" < 66 THEN 'Medium (33-65)'
   ELSE 'High (66-100)'
 END AS sec_group,
 COUNT(*) AS n,
 ROUND(AVG(e."Water Quality Index"),1) AS avg_wqi,
 ROUND(AVG(e."Sanitation Coverage Rate"),1) AS avg_sanitation,
 ROUND(AVG(e."Carbon Emissions (tons)"),1) AS avg_carbon,
 ROUND(AVG(e."Recycling Rate (%)"),1) AS avg_recycling,
 ROUND(AVG(e."Renewable Energy Share (%)"),1) AS avg_renewable,
 ROUND(AVG(e."Vaccination Coverage Rate"),1) AS avg_vaccination
FROM disaster_events d
JOIN coordination_and_evaluation c ON c."Distribution Reference ID" = d."Disaster Event ID"
JOIN environment_and_health e ON e."Disaster Reference ID" = d."Disaster Event ID"
GROUP BY sec_group
ORDER BY sec_group
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-027/attempt-01/sql/S18.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-027/attempt-01/sql/S18.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-027/attempt-01/results/S18.rows.jsonl)；完整：True；SHA256：`f201cbe513a13133facfe90bccdeab51b91264eebb68dea7ee3bfae5b531a484`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "d", "kind": "base", "block": null, "base_tables": ["disaster_events"]}, {"alias": "c", "kind": "base", "block": null, "base_tables": ["coordination_and_evaluation"]}, {"alias": "e", "kind": "base", "block": null, "base_tables": ["environment_and_health"]}] | [{"type": "INNER", "right": "coordination_and_evaluation AS c", "on": "c.\"Distribution Reference ID\" = d.\"Disaster Event ID\"", "using": []}, {"type": "INNER", "right": "environment_and_health AS e", "on": "e.\"Disaster Reference ID\" = d.\"Disaster Event ID\"", "using": []}] | ["CASE WHEN c.\"Secincident Count\" < 33 THEN 'Low (0-32)' WHEN c.\"Secincident Count\" < 66 THEN 'Medium (33-65)' ELSE 'High (66-100)' END"] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |
| B1 | AVG(e."Water Quality Index") | [{"table": "environment_and_health", "column": "Water Quality Index"}] | [] | False |
| B1 | AVG(e."Sanitation Coverage Rate") | [{"table": "environment_and_health", "column": "Sanitation Coverage Rate"}] | [] | False |
| B1 | AVG(e."Carbon Emissions (tons)") | [{"table": "environment_and_health", "column": "Carbon Emissions (tons)"}] | [] | False |
| B1 | AVG(e."Recycling Rate (%)") | [{"table": "environment_and_health", "column": "Recycling Rate (%)"}] | [] | False |
| B1 | AVG(e."Renewable Energy Share (%)") | [{"table": "environment_and_health", "column": "Renewable Energy Share (%)"}] | [] | False |
| B1 | AVG(e."Vaccination Coverage Rate") | [{"table": "environment_and_health", "column": "Vaccination Coverage Rate"}] | [] | False |


## S19

类别 `data`；来源 `query_db`；调用 `3a0bda94fc5b44d1acf0220f62b85f3e`；状态 `success`。

```sql
SELECT
 CASE
   WHEN c."Secincident Count" < 33 THEN 'Low (0-32)'
   WHEN c."Secincident Count" < 66 THEN 'Medium (33-65)'
   ELSE 'High (66-100)'
 END AS sec_group,
 COUNT(*) AS n,
 ROUND(AVG(json_extract(d."Impact Indicator",'$.population.affected')),0) AS avg_affected,
 ROUND(AVG(json_extract(d."Impact Indicator",'$.population.displaced')),0) AS avg_displaced,
 ROUND(AVG(json_extract(d."Impact Indicator",'$.population.casualties')),0) AS avg_casualties,
 ROUND(AVG(json_extract(d."Impact Indicator",'$.infrastructure.damage_percent')),1) AS avg_damage_pct,
 ROUND(AVG(json_extract(d."Impact Indicator",'$.infrastructure.power_outage_percent')),1) AS avg_power_outage
FROM disaster_events d
JOIN coordination_and_evaluation c ON c."Distribution Reference ID" = d."Disaster Event ID"
GROUP BY sec_group
ORDER BY sec_group
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-027/attempt-01/sql/S19.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-027/attempt-01/sql/S19.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-027/attempt-01/results/S19.rows.jsonl)；完整：True；SHA256：`0ecc50485714f988db4c09a2ab8e0d4b209c26c7c6d4dc60ffc8878bda513c08`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "d", "kind": "base", "block": null, "base_tables": ["disaster_events"]}, {"alias": "c", "kind": "base", "block": null, "base_tables": ["coordination_and_evaluation"]}] | [{"type": "INNER", "right": "coordination_and_evaluation AS c", "on": "c.\"Distribution Reference ID\" = d.\"Disaster Event ID\"", "using": []}] | ["CASE WHEN c.\"Secincident Count\" < 33 THEN 'Low (0-32)' WHEN c.\"Secincident Count\" < 66 THEN 'Medium (33-65)' ELSE 'High (66-100)' END"] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |
| B1 | AVG(JSON_EXTRACT(d."Impact Indicator", '$.population.affected')) | [{"table": "disaster_events", "column": "Impact Indicator"}] | [] | False |
| B1 | AVG(JSON_EXTRACT(d."Impact Indicator", '$.population.displaced')) | [{"table": "disaster_events", "column": "Impact Indicator"}] | [] | False |
| B1 | AVG(JSON_EXTRACT(d."Impact Indicator", '$.population.casualties')) | [{"table": "disaster_events", "column": "Impact Indicator"}] | [] | False |
| B1 | AVG(JSON_EXTRACT(d."Impact Indicator", '$.infrastructure.damage_percent')) | [{"table": "disaster_events", "column": "Impact Indicator"}] | [] | False |
| B1 | AVG(JSON_EXTRACT(d."Impact Indicator", '$.infrastructure.power_outage_percent')) | [{"table": "disaster_events", "column": "Impact Indicator"}] | [] | False |


## S20

类别 `data`；来源 `query_db`；调用 `cfb1d1b357474cfbb1f2d74845e79db3`；状态 `success`。

```sql
SELECT d."Disaster Level", e."Environmental Impact Rate", COUNT(*) n
FROM disaster_events d JOIN environment_and_health e ON e."Disaster Reference ID"=d."Disaster Event ID"
GROUP BY d."Disaster Level", e."Environmental Impact Rate" ORDER BY d."Disaster Level", e."Environmental Impact Rate"
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-027/attempt-01/sql/S20.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-027/attempt-01/sql/S20.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-027/attempt-01/results/S20.rows.jsonl)；完整：True；SHA256：`e250fe69d9884b5df520f7bb4a6e6d2aa34c335e7a3f59eaac583114909b891b`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "d", "kind": "base", "block": null, "base_tables": ["disaster_events"]}, {"alias": "e", "kind": "base", "block": null, "base_tables": ["environment_and_health"]}] | [{"type": "INNER", "right": "environment_and_health AS e", "on": "e.\"Disaster Reference ID\" = d.\"Disaster Event ID\"", "using": []}] | ["d.\"Disaster Level\"", "e.\"Environmental Impact Rate\""] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |


## S21

类别 `data`；来源 `query_db`；调用 `96add957a868490db00b7986bc83b2c5`；状态 `success`。

```sql
SELECT d."Disaster Level", e."Disease Risk", COUNT(*) n
FROM disaster_events d JOIN environment_and_health e ON e."Disaster Reference ID"=d."Disaster Event ID"
GROUP BY d."Disaster Level", e."Disease Risk" ORDER BY d."Disaster Level", e."Disease Risk"
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-027/attempt-01/sql/S21.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-027/attempt-01/sql/S21.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-027/attempt-01/results/S21.rows.jsonl)；完整：True；SHA256：`b132e3fedf5545795ba9c9a44832338a4084962afdbb997b145a2fc6ace5d6a0`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "d", "kind": "base", "block": null, "base_tables": ["disaster_events"]}, {"alias": "e", "kind": "base", "block": null, "base_tables": ["environment_and_health"]}] | [{"type": "INNER", "right": "environment_and_health AS e", "on": "e.\"Disaster Reference ID\" = d.\"Disaster Event ID\"", "using": []}] | ["d.\"Disaster Level\"", "e.\"Disease Risk\""] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |


## S22

类别 `data`；来源 `query_db`；调用 `e43f4071fe104d48be79bdf2c608ebe3`；状态 `success`。

```sql
SELECT d."Disaster Level", e."Mental Health Assistance", COUNT(*) n
FROM disaster_events d JOIN environment_and_health e ON e."Disaster Reference ID"=d."Disaster Event ID"
GROUP BY d."Disaster Level", e."Mental Health Assistance" ORDER BY d."Disaster Level"
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-027/attempt-01/sql/S22.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-027/attempt-01/sql/S22.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-027/attempt-01/results/S22.rows.jsonl)；完整：True；SHA256：`7aef8c6b2f2bfa2e729e40e6998192c6f78952974a6a2a978ad14e84ff19c880`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "d", "kind": "base", "block": null, "base_tables": ["disaster_events"]}, {"alias": "e", "kind": "base", "block": null, "base_tables": ["environment_and_health"]}] | [{"type": "INNER", "right": "environment_and_health AS e", "on": "e.\"Disaster Reference ID\" = d.\"Disaster Event ID\"", "using": []}] | ["d.\"Disaster Level\"", "e.\"Mental Health Assistance\""] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |


## S23

类别 `data`；来源 `query_db`；调用 `306b35c11c4a424bb87a7d0c39aec9c1`；状态 `success`。

```sql
SELECT d."Disaster Level",
 ROUND(AVG(o."Estimated Duration (days)"),1) AS avg_duration,
 ROUND(AVG(f."resourcegaps(USD)"),0) AS avg_resourcegap,
 ROUND(AVG(f."fundsutilpct(%)"),1) AS avg_util,
 ROUND(AVG(f."costbene(USD)"),0) AS avg_costbene,
 ROUND(AVG(t."Delivery Success Rate"),1) AS avg_delivery,
 ROUND(AVG(t."Average Delivery Time"),2) AS avg_delivery_time,
 ROUND(AVG(h."Utilization (%)"),1) AS avg_utilization
FROM disaster_events d
JOIN operations1 o ON o."Disaster Reference ID"=d."Disaster Event ID"
JOIN financials1 f ON f."Disaster Reference ID"=d."Disaster Event ID"
JOIN transportation1 t ON t."Disaster Reference ID"=d."Disaster Event ID"
JOIN distribution_hubs h ON h."Disaster Event Reference ID"=d."Disaster Event ID"
GROUP BY d."Disaster Level" ORDER BY d."Disaster Level"
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-027/attempt-01/sql/S23.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-027/attempt-01/sql/S23.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-027/attempt-01/results/S23.rows.jsonl)；完整：True；SHA256：`9e3cfc143511cc00679e9ac3ca7c827b3c2ab33162e4443a35e9a1d7a5c04b59`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "d", "kind": "base", "block": null, "base_tables": ["disaster_events"]}, {"alias": "o", "kind": "base", "block": null, "base_tables": ["operations1"]}, {"alias": "f", "kind": "base", "block": null, "base_tables": ["financials1"]}, {"alias": "t", "kind": "base", "block": null, "base_tables": ["transportation1"]}, {"alias": "h", "kind": "base", "block": null, "base_tables": ["distribution_hubs"]}] | [{"type": "INNER", "right": "operations1 AS o", "on": "o.\"Disaster Reference ID\" = d.\"Disaster Event ID\"", "using": []}, {"type": "INNER", "right": "financials1 AS f", "on": "f.\"Disaster Reference ID\" = d.\"Disaster Event ID\"", "using": []}, {"type": "INNER", "right": "transportation1 AS t", "on": "t.\"Disaster Reference ID\" = d.\"Disaster Event ID\"", "using": []}, {"type": "INNER", "right": "distribution_hubs AS h", "on": "h.\"Disaster Event Reference ID\" = d.\"Disaster Event ID\"", "using": []}] | ["d.\"Disaster Level\""] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | AVG(o."Estimated Duration (days)") | [{"table": "operations1", "column": "Estimated Duration (days)"}] | [] | False |
| B1 | AVG(f."resourcegaps(USD)") | [{"table": "financials1", "column": "resourcegaps(USD)"}] | [] | False |
| B1 | AVG(f."fundsutilpct(%)") | [{"table": "financials1", "column": "fundsutilpct(%)"}] | [] | False |
| B1 | AVG(f."costbene(USD)") | [{"table": "financials1", "column": "costbene(USD)"}] | [] | False |
| B1 | AVG(t."Delivery Success Rate") | [{"table": "transportation1", "column": "Delivery Success Rate"}] | [] | False |
| B1 | AVG(t."Average Delivery Time") | [{"table": "transportation1", "column": "Average Delivery Time"}] | [] | False |
| B1 | AVG(h."Utilization (%)") | [{"table": "distribution_hubs", "column": "Utilization (%)"}] | [] | False |


## S24

类别 `data`；来源 `query_db`；调用 `458e2cd0491e491186ce93c4b0d2ca82`；状态 `success`。

```sql
SELECT d."Disaster Level", c."evaluationstage", COUNT(*) n
FROM disaster_events d JOIN coordination_and_evaluation c ON c."Distribution Reference ID"=d."Disaster Event ID"
GROUP BY d."Disaster Level", c."evaluationstage" ORDER BY d."Disaster Level", n DESC
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-027/attempt-01/sql/S24.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-027/attempt-01/sql/S24.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-027/attempt-01/results/S24.rows.jsonl)；完整：True；SHA256：`efeda7423e13859c8c9bf1a1b87231f0b163da0192b4a983cfabf1cbff37ec58`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "d", "kind": "base", "block": null, "base_tables": ["disaster_events"]}, {"alias": "c", "kind": "base", "block": null, "base_tables": ["coordination_and_evaluation"]}] | [{"type": "INNER", "right": "coordination_and_evaluation AS c", "on": "c.\"Distribution Reference ID\" = d.\"Disaster Event ID\"", "using": []}] | ["d.\"Disaster Level\"", "c.\"evaluationstage\""] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |


## S25

类别 `data`；来源 `query_db`；调用 `625ed1011fe84660ad195e79c216871f`；状态 `success`。

```sql
SELECT
 CASE
   WHEN c."Secincident Count" < 33 THEN 'Low (0-32)'
   WHEN c."Secincident Count" < 66 THEN 'Medium (33-65)'
   ELSE 'High (66-100)'
 END AS sec_group,
 ROUND(AVG(o."Estimated Duration (days)"),1) AS avg_duration,
 ROUND(AVG(f."resourcegaps(USD)"),0) AS avg_resourcegap,
 ROUND(AVG(f."fundsutilpct(%)"),1) AS avg_util,
 ROUND(AVG(t."Delivery Success Rate"),1) AS avg_delivery,
 ROUND(AVG(t."Average Delivery Time"),2) AS avg_delivery_time,
 ROUND(AVG(h."Utilization (%)"),1) AS avg_utilization,
 ROUND(AVG(c."stakeholdersatisf"),2) AS avg_stakeholder_sat,
 ROUND(AVG(c."publicperception"),2) AS avg_public_perception,
 ROUND(AVG(c."reportcompliance"),1) AS avg_report_compliance
FROM disaster_events d
JOIN coordination_and_evaluation c ON c."Distribution Reference ID"=d."Disaster Event ID"
JOIN operations1 o ON o."Disaster Reference ID"=d."Disaster Event ID"
JOIN financials1 f ON f."Disaster Reference ID"=d."Disaster Event ID"
JOIN transportation1 t ON t."Disaster Reference ID"=d."Disaster Event ID"
JOIN distribution_hubs h ON h."Disaster Event Reference ID"=d."Disaster Event ID"
GROUP BY sec_group ORDER BY sec_group
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-027/attempt-01/sql/S25.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-027/attempt-01/sql/S25.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-027/attempt-01/results/S25.rows.jsonl)；完整：True；SHA256：`e868277818f71df65825fdec1578d5a4dc2cd964239e6d226bb6085d42cc0dfe`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "d", "kind": "base", "block": null, "base_tables": ["disaster_events"]}, {"alias": "c", "kind": "base", "block": null, "base_tables": ["coordination_and_evaluation"]}, {"alias": "o", "kind": "base", "block": null, "base_tables": ["operations1"]}, {"alias": "f", "kind": "base", "block": null, "base_tables": ["financials1"]}, {"alias": "t", "kind": "base", "block": null, "base_tables": ["transportation1"]}, {"alias": "h", "kind": "base", "block": null, "base_tables": ["distribution_hubs"]}] | [{"type": "INNER", "right": "coordination_and_evaluation AS c", "on": "c.\"Distribution Reference ID\" = d.\"Disaster Event ID\"", "using": []}, {"type": "INNER", "right": "operations1 AS o", "on": "o.\"Disaster Reference ID\" = d.\"Disaster Event ID\"", "using": []}, {"type": "INNER", "right": "financials1 AS f", "on": "f.\"Disaster Reference ID\" = d.\"Disaster Event ID\"", "using": []}, {"type": "INNER", "right": "transportation1 AS t", "on": "t.\"Disaster Reference ID\" = d.\"Disaster Event ID\"", "using": []}, {"type": "INNER", "right": "distribution_hubs AS h", "on": "h.\"Disaster Event Reference ID\" = d.\"Disaster Event ID\"", "using": []}] | ["CASE WHEN c.\"Secincident Count\" < 33 THEN 'Low (0-32)' WHEN c.\"Secincident Count\" < 66 THEN 'Medium (33-65)' ELSE 'High (66-100)' END"] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | AVG(o."Estimated Duration (days)") | [{"table": "operations1", "column": "Estimated Duration (days)"}] | [] | False |
| B1 | AVG(f."resourcegaps(USD)") | [{"table": "financials1", "column": "resourcegaps(USD)"}] | [] | False |
| B1 | AVG(f."fundsutilpct(%)") | [{"table": "financials1", "column": "fundsutilpct(%)"}] | [] | False |
| B1 | AVG(t."Delivery Success Rate") | [{"table": "transportation1", "column": "Delivery Success Rate"}] | [] | False |
| B1 | AVG(t."Average Delivery Time") | [{"table": "transportation1", "column": "Average Delivery Time"}] | [] | False |
| B1 | AVG(h."Utilization (%)") | [{"table": "distribution_hubs", "column": "Utilization (%)"}] | [] | False |
| B1 | AVG(c."stakeholdersatisf") | [{"table": "coordination_and_evaluation", "column": "stakeholdersatisf"}] | [] | False |
| B1 | AVG(c."publicperception") | [{"table": "coordination_and_evaluation", "column": "publicperception"}] | [] | False |
| B1 | AVG(c."reportcompliance") | [{"table": "coordination_and_evaluation", "column": "reportcompliance"}] | [] | False |


## S26

类别 `data`；来源 `query_db`；调用 `f17f29f02dba410e845ec9a69c7e9b92`；状态 `success`。

```sql
SELECT
 CASE
   WHEN c."Secincident Count" < 33 THEN 'Low (0-32)'
   WHEN c."Secincident Count" < 66 THEN 'Medium (33-65)'
   ELSE 'High (66-100)'
 END AS sec_group,
 e."Environmental Impact Rate", COUNT(*) n
FROM disaster_events d JOIN coordination_and_evaluation c ON c."Distribution Reference ID"=d."Disaster Event ID"
JOIN environment_and_health e ON e."Disaster Reference ID"=d."Disaster Event ID"
GROUP BY sec_group, e."Environmental Impact Rate" ORDER BY sec_group, e."Environmental Impact Rate"
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-027/attempt-01/sql/S26.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-027/attempt-01/sql/S26.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-027/attempt-01/results/S26.rows.jsonl)；完整：True；SHA256：`8bb205b42c9a4da8711629df8cb04cc0f36eccfa1d9212c82f655d92b83fc6c1`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "d", "kind": "base", "block": null, "base_tables": ["disaster_events"]}, {"alias": "c", "kind": "base", "block": null, "base_tables": ["coordination_and_evaluation"]}, {"alias": "e", "kind": "base", "block": null, "base_tables": ["environment_and_health"]}] | [{"type": "INNER", "right": "coordination_and_evaluation AS c", "on": "c.\"Distribution Reference ID\" = d.\"Disaster Event ID\"", "using": []}, {"type": "INNER", "right": "environment_and_health AS e", "on": "e.\"Disaster Reference ID\" = d.\"Disaster Event ID\"", "using": []}] | ["CASE WHEN c.\"Secincident Count\" < 33 THEN 'Low (0-32)' WHEN c.\"Secincident Count\" < 66 THEN 'Medium (33-65)' ELSE 'High (66-100)' END", "e.\"Environmental Impact Rate\""] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |


## S27

类别 `data`；来源 `python`；调用 `ba63cc71a0a146488c62d152b80330f1`；状态 `success`。

```sql

SELECT d."Disaster Event ID", d."Disaster Level", d."Disaster Type",
       c."Secincident Count",
       json_extract(d."Impact Indicator",'$.population.affected') AS affected,
       json_extract(d."Impact Indicator",'$.population.displaced') AS displaced,
       json_extract(d."Impact Indicator",'$.population.injured') AS injured,
       json_extract(d."Impact Indicator",'$.population.casualties') AS casualties,
       json_extract(d."Impact Indicator",'$.population.missing') AS missing,
       json_extract(d."Impact Indicator",'$.infrastructure.damage_percent') AS damage_pct,
       json_extract(d."Impact Indicator",'$.infrastructure.power_outage_percent') AS power_pct,
       json_extract(d."Impact Indicator",'$.infrastructure.water_damage_percent') AS water_pct,
       e."Environmental Impact Rate", e."Waste Management Status", e."Recycling Rate (%)" AS recycling,
       e."Carbon Emissions (tons)" AS carbon, e."Renewable Energy Share (%)" AS renewable,
       e."Water Quality Index" AS wqi, e."Sanitation Coverage Rate" AS sanitation,
       e."Disease Risk", e."Medical Emergency Response Capacity" AS med_cap,
       e."Vaccination Coverage Rate" AS vaccination, e."Mental Health Assistance" AS mental,
       o."Estimated Duration (days)" AS duration, o."Response Phase", o."Operation Status",
       f."fundsutilpct(%)" AS fund_util, f."resourcegaps(USD)" AS resource_gap,
       t."Delivery Success Rate" AS delivery, t."Average Delivery Time" AS deliv_time,
       c."stakeholdersatisf" AS stk_sat, c."publicperception" AS pub_perm,
       c."reportcompliance" AS report_comp
FROM disaster_events d
JOIN coordination_and_evaluation c ON c."Distribution Reference ID"=d."Disaster Event ID"
JOIN environment_and_health e ON e."Disaster Reference ID"=d."Disaster Event ID"
JOIN operations1 o ON o."Disaster Reference ID"=d."Disaster Event ID"
JOIN financials1 f ON f."Disaster Reference ID"=d."Disaster Event ID"
JOIN transportation1 t ON t."Disaster Reference ID"=d."Disaster Event ID"

```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-027/attempt-01/sql/S27.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-027/attempt-01/sql/S27.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-027/attempt-01/results/S27.rows.jsonl)；完整：True；SHA256：`1b754def18d93c8bb6adbf2d11f5ddd305f21fa881356f8a0a5e117dc86b7d1b`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "d", "kind": "base", "block": null, "base_tables": ["disaster_events"]}, {"alias": "c", "kind": "base", "block": null, "base_tables": ["coordination_and_evaluation"]}, {"alias": "e", "kind": "base", "block": null, "base_tables": ["environment_and_health"]}, {"alias": "o", "kind": "base", "block": null, "base_tables": ["operations1"]}, {"alias": "f", "kind": "base", "block": null, "base_tables": ["financials1"]}, {"alias": "t", "kind": "base", "block": null, "base_tables": ["transportation1"]}] | [{"type": "INNER", "right": "coordination_and_evaluation AS c", "on": "c.\"Distribution Reference ID\" = d.\"Disaster Event ID\"", "using": []}, {"type": "INNER", "right": "environment_and_health AS e", "on": "e.\"Disaster Reference ID\" = d.\"Disaster Event ID\"", "using": []}, {"type": "INNER", "right": "operations1 AS o", "on": "o.\"Disaster Reference ID\" = d.\"Disaster Event ID\"", "using": []}, {"type": "INNER", "right": "financials1 AS f", "on": "f.\"Disaster Reference ID\" = d.\"Disaster Event ID\"", "using": []}, {"type": "INNER", "right": "transportation1 AS t", "on": "t.\"Disaster Reference ID\" = d.\"Disaster Event ID\"", "using": []}] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |


## S28

类别 `data`；来源 `python`；调用 `1fdda83ce4d74ddf82e2e5d149a10439`；状态 `success`。

```sql

SELECT c."Secincident Count", c."Safety Ranking", c."Accesslimitation", c."coordeffectlvl",
       c."infosharingstate", c."monitoringfreq", c."evaluationstage", c."lessonslearnedstage",
       c."contingencyplanstage", c."riskmitigationsteps", c."insurancescope", c."compliancestate",
       c."auditstate", c."qualitycontrolsteps", c."mediacoversentiment", c."documentationstate",
       o."Response Phase", o."Operation Status", o."Emergency Level", o."Priority", o."Resource Allocation Status", o."Supply Flow Status",
       d."Disaster Level", d."Disaster Type"
FROM coordination_and_evaluation c
JOIN operations1 o ON o."Disaster Reference ID"=c."Distribution Reference ID"
JOIN disaster_events d ON d."Disaster Event ID"=c."Distribution Reference ID"

```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-027/attempt-01/sql/S28.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-027/attempt-01/sql/S28.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-027/attempt-01/results/S28.rows.jsonl)；完整：True；SHA256：`722737de009281c1c18d710721c1f467bdfa2da5aacf2dda2e1c123372cac7ef`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "c", "kind": "base", "block": null, "base_tables": ["coordination_and_evaluation"]}, {"alias": "o", "kind": "base", "block": null, "base_tables": ["operations1"]}, {"alias": "d", "kind": "base", "block": null, "base_tables": ["disaster_events"]}] | [{"type": "INNER", "right": "operations1 AS o", "on": "o.\"Disaster Reference ID\" = c.\"Distribution Reference ID\"", "using": []}, {"type": "INNER", "right": "disaster_events AS d", "on": "d.\"Disaster Event ID\" = c.\"Distribution Reference ID\"", "using": []}] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |


## S29

类别 `data`；来源 `query_db`；调用 `b9c27767bf914422854af1b1f217c806`；状态 `success`。

```sql
SELECT "Secincident Count", "nextreviewdate" FROM coordination_and_evaluation LIMIT 5
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-027/attempt-01/sql/S29.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-027/attempt-01/sql/S29.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-027/attempt-01/results/S29.rows.jsonl)；完整：True；SHA256：`9ec07a041c904727b67817cfba6c577fe821e5a28bff4806f674daa04abf5902`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "coordination_and_evaluation", "kind": "base", "block": null, "base_tables": ["coordination_and_evaluation"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |


## S30

类别 `data`；来源 `python`；调用 `61f4bc1dc27c4013968367a35db1116c`；状态 `success`。

```sql
SELECT c."Secincident Count", c."nextreviewdate" FROM coordination_and_evaluation c
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-027/attempt-01/sql/S30.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-027/attempt-01/sql/S30.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-027/attempt-01/results/S30.rows.jsonl)；完整：True；SHA256：`4922c9b5485f30e3c879934e7af71f2eca5015418935ed00d7789e072d1dc78b`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "c", "kind": "base", "block": null, "base_tables": ["coordination_and_evaluation"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |


## S31

类别 `data`；来源 `python`；调用 `61f4bc1dc27c4013968367a35db1116c`；状态 `success`。

```sql
SELECT c."Secincident Count", c."contingencyplanstage" FROM coordination_and_evaluation c
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-027/attempt-01/sql/S31.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-027/attempt-01/sql/S31.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-027/attempt-01/results/S31.rows.jsonl)；完整：True；SHA256：`69e9bdcaa0db047a21a3c650fb0f271fc26d157daaf58ca1949b25c6c8257a84`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "c", "kind": "base", "block": null, "base_tables": ["coordination_and_evaluation"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |


## S32

类别 `data`；来源 `python`；调用 `5f11532b5a8f422db222f9d520efd028`；状态 `success`。

```sql
SELECT "Disaster Event ID",
 json_extract("Impact Indicator",'$.damage_level') AS damage_level,
 json_extract("Impact Indicator",'$.communication') AS communication,
 json_extract("Impact Indicator",'$.transportation') AS transportation
FROM disaster_events
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-027/attempt-01/sql/S32.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-027/attempt-01/sql/S32.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-027/attempt-01/results/S32.rows.jsonl)；完整：True；SHA256：`61c17a2996af7bff6771067ce96cee53d6ed1a9c0a2da2d54a0d08544051257b`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "disaster_events", "kind": "base", "block": null, "base_tables": ["disaster_events"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |


## S33

类别 `data`；来源 `query_db`；调用 `407620e84c734758977fc725ceebd6c4`；状态 `success`。

```sql
SELECT "fundingstate", COUNT(*) FROM financials1 GROUP BY "fundingstate"
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-027/attempt-01/sql/S33.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-027/attempt-01/sql/S33.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-027/attempt-01/results/S33.rows.jsonl)；完整：True；SHA256：`c55598b8db3b3d5ef057d5b9b391c65c871667e94d32f77f5458dd22caed7d2a`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "financials1", "kind": "base", "block": null, "base_tables": ["financials1"]}] | [] | ["\"fundingstate\""] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |


## S34

类别 `data`；来源 `python`；调用 `e7ae2b2f35384213946656cc7c361075`；状态 `success`。

```sql

SELECT f."Disaster Reference ID", f."fundingstate", f."costbene(USD)", f."budgetallot(USD)", f."donorcommitments(USD)",
       c."Secincident Count"
FROM financials1 f
JOIN coordination_and_evaluation c ON c."Distribution Reference ID" = f."Disaster Reference ID"

```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-027/attempt-01/sql/S34.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-027/attempt-01/sql/S34.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-027/attempt-01/results/S34.rows.jsonl)；完整：True；SHA256：`85c1bcbb5a0c465ce066a718836aedce86a32e75930de495147960e0f739dac8`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "f", "kind": "base", "block": null, "base_tables": ["financials1"]}, {"alias": "c", "kind": "base", "block": null, "base_tables": ["coordination_and_evaluation"]}] | [{"type": "INNER", "right": "coordination_and_evaluation AS c", "on": "c.\"Distribution Reference ID\" = f.\"Disaster Reference ID\"", "using": []}] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |


## S35

类别 `data`；来源 `python`；调用 `e7ae2b2f35384213946656cc7c361075`；状态 `success`。

```sql

SELECT c."Secincident Count", c."Safety Ranking", c."Accesslimitation", c."coordeffectlvl"
FROM coordination_and_evaluation c

```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-027/attempt-01/sql/S35.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-027/attempt-01/sql/S35.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-027/attempt-01/results/S35.rows.jsonl)；完整：True；SHA256：`7d616b6dfb6177b12740544397ce84f8aa1e8bb0f6a1ad8a0f6fcd06497c5c3c`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "c", "kind": "base", "block": null, "base_tables": ["coordination_and_evaluation"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |


## S36

类别 `data`；来源 `python`；调用 `e7ae2b2f35384213946656cc7c361075`；状态 `success`。

```sql

SELECT c."Secincident Count", c."partnerorgs", c."dataqualityvalue", c."lessonsrecorded", c."bestpracticeslisted", c."improvementrecs"
FROM coordination_and_evaluation c

```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-027/attempt-01/sql/S36.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-027/attempt-01/sql/S36.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-027/attempt-01/results/S36.rows.jsonl)；完整：True；SHA256：`1fe5b4869680a1dc3e0fc4400f4e0b949c18366fa777f3c4aae95f0d17b2660f`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "c", "kind": "base", "block": null, "base_tables": ["coordination_and_evaluation"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |


## S37

类别 `data`；来源 `python`；调用 `e7ae2b2f35384213946656cc7c361075`；状态 `success`。

```sql

SELECT "Disaster Level",
 ROUND(AVG(json_extract("Impact Indicator",'$.infrastructure.damage_percent')),2) AS avg_damage_pct,
 ROUND(AVG(json_extract("Impact Indicator",'$.infrastructure.power_outage_percent')),2) AS avg_power_outage,
 ROUND(AVG(json_extract("Impact Indicator",'$.infrastructure.water_damage_percent')),2) AS avg_water_damage
FROM disaster_events GROUP BY "Disaster Level"

```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-027/attempt-01/sql/S37.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-027/attempt-01/sql/S37.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-027/attempt-01/results/S37.rows.jsonl)；完整：True；SHA256：`9813e104080a9eed379ec750c2cc5988845394a03dc07331cacf5210f3e8d15f`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "disaster_events", "kind": "base", "block": null, "base_tables": ["disaster_events"]}] | [] | ["\"Disaster Level\""] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | AVG(JSON_EXTRACT("Impact Indicator", '$.infrastructure.damage_percent')) | [{"table": "disaster_events", "column": "Impact Indicator"}] | [] | False |
| B1 | AVG(JSON_EXTRACT("Impact Indicator", '$.infrastructure.power_outage_percent')) | [{"table": "disaster_events", "column": "Impact Indicator"}] | [] | False |
| B1 | AVG(JSON_EXTRACT("Impact Indicator", '$.infrastructure.water_damage_percent')) | [{"table": "disaster_events", "column": "Impact Indicator"}] | [] | False |


## S38

类别 `data`；来源 `python`；调用 `2473f0cd72474492824a06520e3178e7`；状态 `success`。

```sql

SELECT c."Secincident Count", c."Accesslimitation", c."Safety Ranking",
       e."Disease Risk", e."Water Quality Index", e."Vaccination Coverage Rate",
       e."Sanitation Coverage Rate", e."Mental Health Assistance",
       d."Disaster Level"
FROM coordination_and_evaluation c
JOIN environment_and_health e ON e."Disaster Reference ID" = c."Distribution Reference ID"
JOIN disaster_events d ON d."Disaster Event ID" = c."Distribution Reference ID"

```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-027/attempt-01/sql/S38.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-027/attempt-01/sql/S38.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-027/attempt-01/results/S38.rows.jsonl)；完整：True；SHA256：`c4022069cafd8079a5d439fdb026ed89e572f061d266aa37b5825c282216557c`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "c", "kind": "base", "block": null, "base_tables": ["coordination_and_evaluation"]}, {"alias": "e", "kind": "base", "block": null, "base_tables": ["environment_and_health"]}, {"alias": "d", "kind": "base", "block": null, "base_tables": ["disaster_events"]}] | [{"type": "INNER", "right": "environment_and_health AS e", "on": "e.\"Disaster Reference ID\" = c.\"Distribution Reference ID\"", "using": []}, {"type": "INNER", "right": "disaster_events AS d", "on": "d.\"Disaster Event ID\" = c.\"Distribution Reference ID\"", "using": []}] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |

