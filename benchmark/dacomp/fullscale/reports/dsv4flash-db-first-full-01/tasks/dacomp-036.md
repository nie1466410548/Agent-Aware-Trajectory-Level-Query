# dacomp-036

Analyze the weak points present in 2024 scenarios that combine different Login Methods and…

运行：已提交。官方未评分。全部 SQL 尝试/成功 40/40；数据 SQL 38/38；Python 2 次。

完整原题：

Analyze the weak points present in 2024 scenarios that combine different Login Methods and Authentication Methods, and recommend which Login - Authentication methods should be adopted subsequently.

| 表 | 行数 | 列数 |
| --- | --- | --- |
| abnormal_logins_table | 414 | 12 |
| authentication_methods_table | 692 | 16 |
| ip_address_information_table | 474 | 12 |
| login_records_table | 487 | 17 |
| menu_access_table | 375 | 13 |
| network_connections_table | 416 | 13 |
| security_events_table | 350 | 13 |
| system_logs_table | 416 | 12 |
| user_accounts_table | 307 | 15 |
| user_information_table | 661 | 14 |
| user_operations_table | 471 | 10 |
| user_permissions_table | 416 | 9 |


实际路线（分析者依据 SQL/源码概括，不代表 Agent 自述）：SQL 比较登录×认证组合的失败、异常与安全事件 → Python 加权评分和排名 → 绘制组合弱点图。

数据库大小：1,777,664 字节。

## 数据 SQL

| SQL | 状态 | 基础表 | Join 输入/类型 | GROUP BY | 聚合表达式 | 结果行数 | 数据库 ms |
| --- | --- | --- | --- | --- | --- | --- | --- |
| [S3/Q1](#s3) | success | ["login_records_table"] | 0 / {} | [] | [] | 5 | 0.377 |
| [S4/Q2](#s4) | success | ["authentication_methods_table"] | 0 / {} | [] | [] | 5 | 0.356 |
| [S5/Q3](#s5) | success | ["login_records_table"] | 0 / {} | ["\"Login Method\"", "\"Authentication Status\"", "\"Authentication Level\"", "\"Two-Factor Authentication Status\"", "\"Two-Factor Authentication Method\""] | ["COUNT(*)"] | 106 | 0.893 |
| [S6/Q4](#s6) | success | ["login_records_table"] | 0 / {} | [] | ["COUNT(*)", "SUM(CASE WHEN SUBSTRING(\"Login Time\", 1, 4) = '2024' THEN 1 ELSE 0 END)"] | 1 | 0.521 |
| [S7/Q5](#s7) | success | ["abnormal_logins_table"] | 0 / {} | [] | [] | 30 | 0.483 |
| [S8/Q6](#s8) | success | ["login_records_table"] | 0 / {} | [] | [] | 4 | 0.524 |
| [S9/Q7](#s9) | success | ["login_records_table"] | 0 / {} | [] | [] | 3 | 0.518 |
| [S10/Q8](#s10) | success | ["login_records_table"] | 0 / {} | [] | [] | 3 | 0.504 |
| [S11/Q9](#s11) | success | ["authentication_methods_table"] | 0 / {} | [] | [] | 10 | 0.602 |
| [S12/Q10](#s12) | success | ["login_records_table"] | 0 / {} | ["\"Login Method\"", "\"Authentication Status\""] | ["COUNT(*)", "COUNT(*)", "COUNT(*)"] | 8 | 0.734 |
| [S13/Q11](#s13) | success | ["login_records_table"] | 0 / {} | ["\"Login Method\"", "\"Two-Factor Authentication Status\"", "\"Two-Factor Authentication Method\"", "\"Authentication Status\""] | ["COUNT(*)"] | 48 | 0.753 |
| [S14/Q12](#s14) | success | ["abnormal_logins_table", "login_records_table"] | 2 / {'INNER': 1} | ["lr.\"Login Method\"", "lr.\"Two-Factor Authentication Method\""] | ["COUNT(DISTINCT al.\"Anomaly ID\")", "SUM(al.\"Device Anomaly Indicators\")", "SUM(al.\"Network Anomaly Indicators\")", "SUM(al.\"Behavior Anomaly Indicators\")", "AVG(al.\"Anomaly Score\")"] | 12 | 1.299 |
| [S15/Q13](#s15) | success | ["login_records_table", "security_events_table"] | 2 / {'INNER': 1} | ["lr.\"Login Method\""] | ["COUNT(DISTINCT se.\"Event ID\")", "SUM(se.\"Risk Score\")", "COUNT(DISTINCT CASE WHEN se.\"Severity\" IN ('High', 'Critical', 'Severe') THEN se.\"Event ID\" END)"] | 4 | 1.145 |
| [S16/Q14](#s16) | success | ["abnormal_logins_table", "login_records_table"] | 2 / {'INNER': 1} | ["lr.\"Login Method\"", "lr.\"Two-Factor Authentication Method\"", "lr.\"Two-Factor Authentication Status\""] | ["COUNT(DISTINCT al.\"Anomaly ID\")", "COUNT(DISTINCT lr.\"Login Record ID\")", "COUNT(DISTINCT lr.\"Login Record ID\")", "COUNT(DISTINCT al.\"Anomaly ID\")"] | 24 | 1.21 |
| [S17/Q15](#s17) | success | ["abnormal_logins_table", "login_records_table"] | 2 / {'INNER': 1} | ["al.\"Anomaly Type\"", "lr.\"Login Method\"", "lr.\"Two-Factor Authentication Method\""] | ["COUNT(*)"] | 46 | 1.207 |
| [S18/Q16](#s18) | success | ["abnormal_logins_table", "login_records_table"] | 2 / {'LEFT': 1} | [] | ["COUNT(*)", "COUNT(DISTINCT CASE WHEN NOT al.\"Anomaly ID\" IS NULL THEN lr.\"Login Record ID\" END)"] | 1 | 1.034 |
| [S19/Q17](#s19) | success | ["abnormal_logins_table", "login_records_table"] | 2 / {'INNER': 1} | ["al.\"Anomaly Type\"", "al.\"Risk Level\""] | ["COUNT(*)"] | 16 | 0.985 |
| [S20/Q18](#s20) | success | ["login_records_table", "security_events_table"] | 2 / {'INNER': 1} | ["se.\"Type\"", "se.\"Severity\""] | ["COUNT(*)"] | 16 | 0.908 |
| [S21/Q19](#s21) | success | ["authentication_methods_table"] | 0 / {} | [] | [] | 692 | 2.046 |
| [S22/Q20](#s22) | success | ["abnormal_logins_table", "login_records_table", "security_events_table"] | 3 / {'LEFT': 2} | ["lr.\"Login Method\"", "lr.\"Two-Factor Authentication Method\""] | ["COUNT(DISTINCT lr.\"Login Record ID\")", "SUM(CASE WHEN lr.\"Authentication Status\" = 'Failure' THEN 1 ELSE 0 END)", "COUNT(DISTINCT al.\"Anomaly ID\")", "COUNT(DISTINCT se.\"Event ID\")", "SUM(se.\"Risk Score\")", "COUNT(DISTINCT CASE WHEN se.\"Severity\" IN ('High', 'Severe') THEN se.\"Event ID\" END)", "AVG(al.\"Anomaly Score\")"] | 12 | 1.913 |
| [S23/Q21](#s23) | success | ["abnormal_logins_table", "login_records_table", "security_events_table"] | 3 / {'LEFT': 2} | ["lr.\"Login Method\"", "lr.\"Two-Factor Authentication Status\"", "lr.\"Two-Factor Authentication Method\""] | ["COUNT(DISTINCT lr.\"Login Record ID\")", "SUM(CASE WHEN lr.\"Authentication Status\" = 'Failure' THEN 1 ELSE 0 END)", "COUNT(DISTINCT al.\"Anomaly ID\")", "COUNT(DISTINCT se.\"Event ID\")", "SUM(se.\"Risk Score\")", "AVG(al.\"Anomaly Score\")", "COUNT(DISTINCT lr.\"Login Record ID\")", "COUNT(DISTINCT lr.\"Login Record ID\")", "SUM(CASE WHEN lr.\"Authentication Status\" = 'Failure' THEN 1 ELSE 0 END)", "COUNT(DISTINCT al.\"Anomaly ID\")"] | 24 | 1.829 |
| [S24/Q22](#s24) | success | ["login_records_table"] | 0 / {} | ["lr.\"Login Method\"", "lr.\"Two-Factor Authentication Status\"", "lr.\"Two-Factor Authentication Method\"", "lr.\"Authentication Level\""] | ["COUNT(*)", "SUM(CASE WHEN lr.\"Authentication Status\" = 'Failure' THEN 1 ELSE 0 END)"] | 67 | 0.83 |
| [S25/Q23](#s25) | success | ["abnormal_logins_table", "login_records_table"] | 2 / {'INNER': 1} | ["lr.\"Login Method\"", "lr.\"Two-Factor Authentication Method\"", "al.\"Anomaly Type\""] | ["COUNT(*)", "AVG(al.\"Anomaly Score\")", "AVG(al.\"Device Anomaly Indicators\")", "AVG(al.\"Network Anomaly Indicators\")", "AVG(al.\"Behavior Anomaly Indicators\")"] | 46 | 1.406 |
| [S26/Q24](#s26) | success | ["login_records_table", "security_events_table"] | 2 / {'INNER': 1} | ["lr.\"Login Method\"", "lr.\"Two-Factor Authentication Method\"", "se.\"Type\"", "se.\"Severity\""] | ["COUNT(*)", "AVG(se.\"Risk Score\")"] | 96 | 1.739 |
| [S27/Q25](#s27) | success | ["login_records_table"] | 0 / {} | ["\"Login Method\""] | ["COUNT(*)", "SUM(CASE WHEN \"Authentication Status\" = 'Failure' THEN 1 ELSE 0 END)", "COUNT(DISTINCT \"Two-Factor Authentication Method\")", "COUNT(*)", "SUM(CASE WHEN \"Authentication Status\" = 'Failure' THEN 1 ELSE 0 END)"] | 4 | 0.638 |
| [S28/Q26](#s28) | success | ["login_records_table"] | 0 / {} | ["\"Two-Factor Authentication Status\""] | ["COUNT(*)", "SUM(CASE WHEN \"Authentication Status\" = 'Failure' THEN 1 ELSE 0 END)", "COUNT(*)", "SUM(CASE WHEN \"Authentication Status\" = 'Failure' THEN 1 ELSE 0 END)"] | 2 | 0.564 |
| [S29/Q27](#s29) | success | ["login_records_table"] | 0 / {} | ["\"Two-Factor Authentication Method\""] | ["COUNT(*)", "SUM(CASE WHEN \"Authentication Status\" = 'Failure' THEN 1 ELSE 0 END)", "COUNT(*)", "SUM(CASE WHEN \"Authentication Status\" = 'Failure' THEN 1 ELSE 0 END)"] | 3 | 0.589 |
| [S30/Q28](#s30) | success | ["authentication_methods_table"] | 0 / {} | ["\"Authentication Method Name\""] | ["COUNT(*)", "SUM(CASE WHEN \"Enabled\" = 'Enabled' THEN 1 ELSE 0 END)", "AVG(\"security level\")", "AVG(\"Authentication Priority\")", "AVG(\"Maximum Attempts\")", "AVG(\"Lockout Duration\")"] | 6 | 0.87 |
| [S31/Q29](#s31) | success | ["login_records_table", "security_events_table"] | 2 / {'INNER': 1} | ["se.\"Severity\""] | ["COUNT(*)", "AVG(se.\"Risk Score\")"] | 4 | 0.883 |
| [S32/Q30](#s32) | success | ["login_records_table", "system_logs_table"] | 2 / {'INNER': 1} | ["lr.\"Login Method\"", "lr.\"Two-Factor Authentication Method\"", "sl.\"Log Level\""] | ["COUNT(*)"] | 36 | 1.083 |
| [S33/Q31](#s33) | success | ["ip_address_information_table", "login_records_table"] | 2 / {'INNER': 1} | ["lr.\"Login Method\"", "lr.\"Two-Factor Authentication Method\""] | ["COUNT(DISTINCT ip.\"IP Record ID\")", "COUNT(DISTINCT ip.\"IP Address\")", "COUNT(DISTINCT ip.\"Province\")"] | 12 | 1.408 |
| [S34/Q32](#s34) | success | ["abnormal_logins_table", "login_records_table", "security_events_table", "system_logs_table"] | 4 / {'LEFT': 3} | ["lr.\"Login Method\"", "lr.\"Two-Factor Authentication Method\""] | ["COUNT(DISTINCT lr.\"Login Record ID\")", "SUM(CASE WHEN lr.\"Authentication Status\" = 'Failure' THEN 1 ELSE 0 END)", "COUNT(DISTINCT al.\"Anomaly ID\")", "COUNT(DISTINCT se.\"Event ID\")", "COUNT(DISTINCT CASE WHEN se.\"Severity\" IN ('High', 'Severe') THEN se.\"Event ID\" END)", "COUNT(DISTINCT CASE WHEN se.\"Severity\" = 'Severe' THEN se.\"Event ID\" END)", "COUNT(DISTINCT sl.\"Log ID\")", "COUNT(DISTINCT CASE WHEN sl.\"Log Level\" = 'ERROR' THEN sl.\"Log ID\" END)", "SUM(al.\"Device Anomaly Indicators\")", "SUM(al.\"Network Anomaly Indicators\")", "SUM(al.\"Behavior Anomaly Indicators\")", "SUM(se.\"Risk Score\")", "AVG(al.\"Anomaly Score\")"] | 12 | 2.98 |
| [S35/Q33](#s35) | success | ["login_records_table", "security_events_table"] | 2 / {'INNER': 1} | ["lr.\"Login Method\"", "lr.\"Two-Factor Authentication Method\"", "se.\"Severity\""] | ["COUNT(*)"] | 45 | 1.004 |
| [S36/Q34](#s36) | success | ["abnormal_logins_table", "login_records_table", "security_events_table"] | 3 / {'LEFT': 2} | ["lr.\"Two-Factor Authentication Status\""] | ["COUNT(DISTINCT lr.\"Login Record ID\")", "COUNT(DISTINCT al.\"Anomaly ID\")", "COUNT(DISTINCT se.\"Event ID\")", "SUM(se.\"Risk Score\")", "COUNT(DISTINCT CASE WHEN se.\"Severity\" IN ('High', 'Severe') THEN se.\"Event ID\" END)", "AVG(al.\"Anomaly Score\")", "COUNT(DISTINCT lr.\"Login Record ID\")", "COUNT(DISTINCT al.\"Anomaly ID\")"] | 2 | 1.72 |
| [S37/Q35](#s37) | success | ["abnormal_logins_table", "login_records_table", "security_events_table"] | 3 / {'LEFT': 2} | ["lr.\"Login Method\"", "lr.\"Two-Factor Authentication Status\""] | ["COUNT(DISTINCT al.\"Anomaly ID\")", "COUNT(DISTINCT se.\"Event ID\")", "SUM(se.\"Risk Score\")"] | 8 | 1.462 |
| [S38/Q36](#s38) | success | ["abnormal_logins_table", "login_records_table", "security_events_table"] | 3 / {'LEFT': 2} | ["lr.\"Login Method\"", "lr.\"Two-Factor Authentication Status\""] | ["COUNT(DISTINCT lr.\"Login Record ID\")", "COUNT(DISTINCT al.\"Anomaly ID\")", "COUNT(DISTINCT se.\"Event ID\")", "SUM(se.\"Risk Score\")", "COUNT(DISTINCT lr.\"Login Record ID\")", "COUNT(DISTINCT lr.\"Login Record ID\")", "COUNT(DISTINCT al.\"Anomaly ID\")", "SUM(se.\"Risk Score\")"] | 8 | 1.61 |
| [S39/Q37](#s39) | success | ["abnormal_logins_table", "login_records_table", "security_events_table"] | 3 / {'LEFT': 2} | ["lr.\"Login Method\"", "lr.\"Two-Factor Authentication Status\""] | ["COUNT(DISTINCT lr.\"Login Record ID\")", "COUNT(DISTINCT al.\"Anomaly ID\")", "COUNT(DISTINCT se.\"Event ID\")", "SUM(se.\"Risk Score\")", "COUNT(DISTINCT lr.\"Login Record ID\")", "COUNT(DISTINCT lr.\"Login Record ID\")", "COUNT(DISTINCT al.\"Anomaly ID\")", "SUM(se.\"Risk Score\")"] | 8 | 1.762 |
| [S40/Q38](#s40) | success | ["abnormal_logins_table", "login_records_table", "security_events_table"] | 3 / {'LEFT': 2} | ["lr.\"Login Method\"", "lr.\"Two-Factor Authentication Method\""] | ["COUNT(DISTINCT lr.\"Login Record ID\")", "SUM(CASE WHEN lr.\"Authentication Status\" = 'Failure' THEN 1 ELSE 0 END)", "COUNT(DISTINCT al.\"Anomaly ID\")", "COUNT(DISTINCT se.\"Event ID\")", "SUM(se.\"Risk Score\")", "COUNT(DISTINCT CASE WHEN se.\"Severity\" IN ('High', 'Severe') THEN se.\"Event ID\" END)", "AVG(al.\"Anomaly Score\")"] | 12 | 1.823 |


## 元数据和设置

| SQL | 类别 | 状态 | 内容 |
| --- | --- | --- | --- |
| S1 | connection_setup | success | PRAGMA query_only=ON |
| S2 | metadata | success | SELECT name,sql FROM sqlite_master WHERE type='table' ORDER BY name |


## Python 与执行位置

人工源码审查：**database_first_violation**。SQL 已完成登录/认证组合的异常指标关联与汇总，P1 随后在 Python 中做 min-max 归一化、加权薄弱度、排名和失败率。这些可由 SQLite 聚合、窗口和算术完成；P2 图形渲染另行允许。 [证据](../reviews/dacomp-036.json)。

P1：Need to compute a composite weakness score and create visualizations. SQLite handles aggregation but the multi-dimensional scoring (normalization, weighting, ranking) and visualization are better done in Python with matplotlib/seaborn.

[源码](../../../runs/dsv4flash-db-first-full-01/dacomp-036/attempt-01/python/P1.py)；[输出](../../../runs/dsv4flash-db-first-full-01/dacomp-036/attempt-01/python/P1.stdout)；[错误](../../../runs/dsv4flash-db-first-full-01/dacomp-036/attempt-01/python/P1.stderr)。检出需人工核验的 SQL 可实现操作：.query(, sort_values(；不能仅凭理由判为合规。

P2：Creating visualizations for 2FA status effect and final ranking of login-2FA combinations. These are plotting/statistical steps done in Python after SQL aggregation.

[源码](../../../runs/dsv4flash-db-first-full-01/dacomp-036/attempt-01/python/P2.py)；[输出](../../../runs/dsv4flash-db-first-full-01/dacomp-036/attempt-01/python/P2.stdout)；[错误](../../../runs/dsv4flash-db-first-full-01/dacomp-036/attempt-01/python/P2.stderr)。检出需人工核验的 SQL 可实现操作：.query(, sort_values(；不能仅凭理由判为合规。

## 优化机会

已验证候选。筛选限于精确 SQL、相同自包含 CTE、相同单表完整过滤、可分解单表聚合；未覆盖任意 Join 等价和一般谓词蕴含。全部候选都是 offline，未测在线预测。

| 候选 | 类型 | 已有结果 | 覆盖 SQL | 后续次数 | 中间行数 | 验证 | 成本 |
| --- | --- | --- | --- | --- | --- | --- | --- |
| C1 | common filtered view | False | ["S5", "S8", "S9", "S10", "S13", "S24", "S27", "S28", "S29"] | 8 | 177 | verified | Not benchmarked; correctness alone does not establish net speedup. |
| C2 | aggregate MV | False | ["S5", "S13", "S24", "S28", "S29"] | 4 | 106 | verified | Not benchmarked; correctness alone does not establish net speedup. |


已验证覆盖（含触发查询、候选并集去重）：9/38 条成功数据 SQL。正确性仅针对当前数据库快照；未测性能的候选不能声称已加速。

[完整 build/rewrite 与比较证据](dacomp-036.analysis.json)。

### C1：common filtered view

Same single source and complete filter; original filter retained.

原查询 [S5](#s5), [S8](#s8), [S9](#s9), [S10](#s10), [S13](#s13), [S24](#s24), [S27](#s27), [S28](#s28), [S29](#s29) → 新增共享状态 C1 → 后续 8 次可复用。该构建点为事后假设，不代表 Agent 当时预知后续。

构建定义：

```sql
SELECT * FROM "login_records_table" WHERE SUBSTRING("Login Time", 1, 4) = '2024'
```

受益查询 S5 的改写示例：

```sql
SELECT "Login Method", "Authentication Status", "Authentication Level", "Two-Factor Authentication Status", "Two-Factor Authentication Method", COUNT(*) AS cnt FROM temp.reuse_candidate AS login_records_table WHERE SUBSTRING("Login Time", 1, 4) = '2024' GROUP BY 1, 2, 3, 4, 5 ORDER BY cnt DESC
```

| 原 SQL | 列名一致 | 结果一致 | 比较方法 |
| --- | --- | --- | --- |
| S5 | True | True | ordered_numeric_tolerance |
| S8 | True | True | exact_multiset |
| S9 | True | True | exact_multiset |
| S10 | True | True | exact_multiset |
| S13 | True | True | ordered_numeric_tolerance |
| S24 | True | True | ordered_numeric_tolerance |
| S27 | True | True | ordered_numeric_tolerance |
| S28 | True | True | exact_multiset |
| S29 | True | True | ordered_numeric_tolerance |


验证状态：verified；成本结论：Not benchmarked; correctness alone does not establish net speedup.

### C2：aggregate MV

Union of grouping keys; decomposable aggregate states; AVG uses SUM and non-NULL COUNT.

原查询 [S5](#s5), [S13](#s13), [S24](#s24), [S28](#s28), [S29](#s29) → 新增共享状态 C2 → 后续 4 次可复用。该构建点为事后假设，不代表 Agent 当时预知后续。

构建定义：

```sql
SELECT "Login Method" AS __g0, "Authentication Status" AS __g1, "Authentication Level" AS __g2, "Two-Factor Authentication Status" AS __g3, "Two-Factor Authentication Method" AS __g4, COUNT(*) AS __a0, SUM(CASE WHEN "Authentication Status" = 'Failure' THEN 1 ELSE 0 END) AS __a1 FROM "login_records_table" WHERE SUBSTRING("Login Time", 1, 4) = '2024' GROUP BY "Login Method", "Authentication Status", "Authentication Level", "Two-Factor Authentication Status", "Two-Factor Authentication Method"
```

受益查询 S5 的改写示例：

```sql
SELECT __g0 AS "Login Method", __g1 AS "Authentication Status", __g2 AS "Authentication Level", __g3 AS "Two-Factor Authentication Status", __g4 AS "Two-Factor Authentication Method", SUM(__a0) AS cnt FROM temp.reuse_candidate GROUP BY __g0, __g1, __g2, __g3, __g4 ORDER BY cnt DESC
```

| 原 SQL | 列名一致 | 结果一致 | 比较方法 |
| --- | --- | --- | --- |
| S5 | True | True | ordered_numeric_tolerance |
| S13 | True | True | ordered_numeric_tolerance |
| S24 | True | True | ordered_numeric_tolerance |
| S28 | True | True | exact_multiset |
| S29 | True | True | ordered_numeric_tolerance |


验证状态：verified；成本结论：Not benchmarked; correctness alone does not establish net speedup.

结果依赖：自动记录 SQL→Python 的接口父调用，以及源码中引用归档文件的消费者；字面值相同不认定因果。模型方向选择需要人工读取消息，尚未做全面因果标注。

[原始报告](../../../runs/dsv4flash-db-first-full-01/dacomp-036/attempt-01/answer.md)；[统一消息](../../../runs/dsv4flash-db-first-full-01/dacomp-036/attempt-01/messages.jsonl)；[原始 OpenCode 事件](../../../runs/dsv4flash-db-first-full-01/dacomp-036/attempt-01/opencode.jsonl)；[SQL 引擎日志](../../../runs/dsv4flash-db-first-full-01/dacomp-036/attempt-01/sql_journal.jsonl)。

[可读报告（本地图片链接规范化）](../answers/dacomp-036.md)。原始回答保留，分析结论未改写。

## S1

类别 `connection_setup`；来源 `connection`；调用 `03ff517c1bd4430499b7d262c18cfaa6`；状态 `success`。

```sql
PRAGMA query_only=ON
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-036/attempt-01/sql/S1.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-036/attempt-01/sql/S1.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-036/attempt-01/results/S1.rows.jsonl)；完整：True；SHA256：`e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`。

## S2

类别 `metadata`；来源 `list_db`；调用 `03ff517c1bd4430499b7d262c18cfaa6`；状态 `success`。

```sql
SELECT name,sql FROM sqlite_master WHERE type='table' ORDER BY name
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-036/attempt-01/sql/S2.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-036/attempt-01/sql/S2.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-036/attempt-01/results/S2.rows.jsonl)；完整：True；SHA256：`feefd8394e510ca9e58d530ac97f2b5255b1b82d07ba67e636ade04103531d66`。

## S3

类别 `data`；来源 `query_db`；调用 `331b648d43d64c10904df15031f1154b`；状态 `success`。

```sql
SELECT * FROM login_records_table LIMIT 5
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-036/attempt-01/sql/S3.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-036/attempt-01/sql/S3.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-036/attempt-01/results/S3.rows.jsonl)；完整：True；SHA256：`34b010320385b3804c8f0017b205a7606df79f48eeafe8a4f18de2b35caf4f89`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "login_records_table", "kind": "base", "block": null, "base_tables": ["login_records_table"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |


## S4

类别 `data`；来源 `query_db`；调用 `f832aafa9f1a40a49a6007c6c7a0109f`；状态 `success`。

```sql
SELECT * FROM authentication_methods_table LIMIT 5
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-036/attempt-01/sql/S4.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-036/attempt-01/sql/S4.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-036/attempt-01/results/S4.rows.jsonl)；完整：True；SHA256：`6495e4fd426d5bbf969cf53a9551884c258363bab393c819e8bbd6ea02bce125`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "authentication_methods_table", "kind": "base", "block": null, "base_tables": ["authentication_methods_table"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |


## S5

类别 `data`；来源 `query_db`；调用 `f5da5f956b0d435cb4cc9546d6bb9e56`；状态 `success`。

```sql
SELECT "Login Method", "Authentication Status", "Authentication Level", "Two-Factor Authentication Status", "Two-Factor Authentication Method", COUNT(*) AS cnt
FROM login_records_table
WHERE substr("Login Time",1,4)='2024'
GROUP BY 1,2,3,4,5
ORDER BY cnt DESC
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-036/attempt-01/sql/S5.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-036/attempt-01/sql/S5.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-036/attempt-01/results/S5.rows.jsonl)；完整：True；SHA256：`71de0267683b7ef9b4373ba8b9e09c38180dd30d2ca159f9666c48505f8e5875`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "login_records_table", "kind": "base", "block": null, "base_tables": ["login_records_table"]}] | [] | ["\"Login Method\"", "\"Authentication Status\"", "\"Authentication Level\"", "\"Two-Factor Authentication Status\"", "\"Two-Factor Authentication Method\""] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |


## S6

类别 `data`；来源 `query_db`；调用 `584cbedf6f0d41ad98ccb0e2731af95e`；状态 `success`。

```sql
SELECT COUNT(*) AS total, SUM(CASE WHEN substr("Login Time",1,4)='2024' THEN 1 ELSE 0 END) AS cnt_2024 FROM login_records_table
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-036/attempt-01/sql/S6.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-036/attempt-01/sql/S6.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-036/attempt-01/results/S6.rows.jsonl)；完整：True；SHA256：`ae6ea8b9fccfdd98493cb7c1420a29a2e70b414df3837053e0d5cdd28c7e1dcc`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "login_records_table", "kind": "base", "block": null, "base_tables": ["login_records_table"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |
| B1 | SUM(CASE WHEN SUBSTRING("Login Time", 1, 4) = '2024' THEN 1 ELSE 0 END) | [] | [{"table": "login_records_table", "column": "Login Time"}] | False |


## S7

类别 `data`；来源 `query_db`；调用 `b9f1c4dd864a4f21ac8ad71aa9d9b958`；状态 `success`。

```sql
SELECT DISTINCT "Anomaly Type", "Risk Level", "Confirmation Status" FROM abnormal_logins_table LIMIT 30
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-036/attempt-01/sql/S7.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-036/attempt-01/sql/S7.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-036/attempt-01/results/S7.rows.jsonl)；完整：True；SHA256：`4a0a3debbe8914671b32db89c2ec53000ca3622c52a480d94bf0ddc2a9ad44f1`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "abnormal_logins_table", "kind": "base", "block": null, "base_tables": ["abnormal_logins_table"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |


## S8

类别 `data`；来源 `query_db`；调用 `4ca54b7b6fb549fea0ea803a270c9a28`；状态 `success`。

```sql
SELECT DISTINCT "Login Method" FROM login_records_table WHERE substr("Login Time",1,4)='2024'
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-036/attempt-01/sql/S8.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-036/attempt-01/sql/S8.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-036/attempt-01/results/S8.rows.jsonl)；完整：True；SHA256：`4c4960c6c5d480723586ba32a0ce69632e086aa9b42fbd09ffcf3cb21e2be35d`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "login_records_table", "kind": "base", "block": null, "base_tables": ["login_records_table"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |


## S9

类别 `data`；来源 `query_db`；调用 `f0377695bb7e4f12927b52b48d3615c4`；状态 `success`。

```sql
SELECT DISTINCT "Two-Factor Authentication Method" FROM login_records_table WHERE substr("Login Time",1,4)='2024'
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-036/attempt-01/sql/S9.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-036/attempt-01/sql/S9.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-036/attempt-01/results/S9.rows.jsonl)；完整：True；SHA256：`034f0a2c0b5d75cf544dcd739684237ff4984fb8fd158179fea2da6a39561458`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "login_records_table", "kind": "base", "block": null, "base_tables": ["login_records_table"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |


## S10

类别 `data`；来源 `query_db`；调用 `0642f9c880684f2493933b901cadbb7f`；状态 `success`。

```sql
SELECT DISTINCT "Authentication Level" FROM login_records_table WHERE substr("Login Time",1,4)='2024'
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-036/attempt-01/sql/S10.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-036/attempt-01/sql/S10.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-036/attempt-01/results/S10.rows.jsonl)；完整：True；SHA256：`6920439bdd032fd951cf5916834e120c2493edd979281f0b7587f18a49949857`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "login_records_table", "kind": "base", "block": null, "base_tables": ["login_records_table"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |


## S11

类别 `data`；来源 `query_db`；调用 `28e2d0875d6f4872b2b7f93c674c2e2f`；状态 `success`。

```sql
SELECT DISTINCT "Authentication Method Name" FROM authentication_methods_table
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-036/attempt-01/sql/S11.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-036/attempt-01/sql/S11.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-036/attempt-01/results/S11.rows.jsonl)；完整：True；SHA256：`82d04811c9a5f6826be1f5c84233f22689ed7d4cf9369fd965e01f4fe6b9df38`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "authentication_methods_table", "kind": "base", "block": null, "base_tables": ["authentication_methods_table"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |


## S12

类别 `data`；来源 `query_db`；调用 `b648921b446c40cab726976145dd8b1f`；状态 `success`。

```sql
SELECT "Login Method", 
       "Authentication Status", 
       COUNT(*) AS cnt,
       ROUND(100.0 * COUNT(*) / SUM(COUNT(*)) OVER (PARTITION BY "Login Method"), 1) AS pct
FROM login_records_table
WHERE substr("Login Time",1,4)='2024'
GROUP BY "Login Method", "Authentication Status"
ORDER BY "Login Method", cnt DESC
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-036/attempt-01/sql/S12.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-036/attempt-01/sql/S12.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-036/attempt-01/results/S12.rows.jsonl)；完整：True；SHA256：`11df98a5a00bc0a1cbe52c3d8f0693aa190369950e15c51130ebac8cfd9cad9f`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "login_records_table", "kind": "base", "block": null, "base_tables": ["login_records_table"]}] | [] | ["\"Login Method\"", "\"Authentication Status\""] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |
| B1 | COUNT(*) | [] | [] | True |
| B1 | COUNT(*) | [] | [] | True |


## S13

类别 `data`；来源 `query_db`；调用 `cb9a066c3b6246ce92d1b275b87148ae`；状态 `success`。

```sql
SELECT "Login Method",
       "Two-Factor Authentication Status",
       "Two-Factor Authentication Method",
       "Authentication Status",
       COUNT(*) AS cnt
FROM login_records_table
WHERE substr("Login Time",1,4)='2024'
GROUP BY 1,2,3,4
ORDER BY "Login Method", "Two-Factor Authentication Status", "Authentication Status"
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-036/attempt-01/sql/S13.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-036/attempt-01/sql/S13.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-036/attempt-01/results/S13.rows.jsonl)；完整：True；SHA256：`ff15d615f8008c135704b0f84c87edab5b9a61d84a132a1da35479e945e55eb5`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "login_records_table", "kind": "base", "block": null, "base_tables": ["login_records_table"]}] | [] | ["\"Login Method\"", "\"Two-Factor Authentication Status\"", "\"Two-Factor Authentication Method\"", "\"Authentication Status\""] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |


## S14

类别 `data`；来源 `query_db`；调用 `08c41d300bb845fd90db7955bb7ed8db`；状态 `success`。

```sql
SELECT lr."Login Method",
       lr."Two-Factor Authentication Method",
       COUNT(DISTINCT al."Anomaly ID") AS anomaly_cnt,
       ROUND(AVG(al."Anomaly Score"),1) AS avg_score,
       SUM(al."Device Anomaly Indicators") AS dev_ind,
       SUM(al."Network Anomaly Indicators") AS net_ind,
       SUM(al."Behavior Anomaly Indicators") AS beh_ind
FROM abnormal_logins_table al
JOIN login_records_table lr ON al."Login Record ID" = lr."Login Record ID"
WHERE substr(lr."Login Time",1,4)='2024'
GROUP BY 1,2
ORDER BY anomaly_cnt DESC
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-036/attempt-01/sql/S14.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-036/attempt-01/sql/S14.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-036/attempt-01/results/S14.rows.jsonl)；完整：True；SHA256：`be25353583c7062c9668abbc86b81da36800a6b0e0073ad91a782077bda5d3b7`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "al", "kind": "base", "block": null, "base_tables": ["abnormal_logins_table"]}, {"alias": "lr", "kind": "base", "block": null, "base_tables": ["login_records_table"]}] | [{"type": "INNER", "right": "login_records_table AS lr", "on": "al.\"Login Record ID\" = lr.\"Login Record ID\"", "using": []}] | ["lr.\"Login Method\"", "lr.\"Two-Factor Authentication Method\""] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(DISTINCT al."Anomaly ID") | [{"table": "abnormal_logins_table", "column": "Anomaly ID"}] | [] | False |
| B1 | SUM(al."Device Anomaly Indicators") | [{"table": "abnormal_logins_table", "column": "Device Anomaly Indicators"}] | [] | False |
| B1 | SUM(al."Network Anomaly Indicators") | [{"table": "abnormal_logins_table", "column": "Network Anomaly Indicators"}] | [] | False |
| B1 | SUM(al."Behavior Anomaly Indicators") | [{"table": "abnormal_logins_table", "column": "Behavior Anomaly Indicators"}] | [] | False |
| B1 | AVG(al."Anomaly Score") | [{"table": "abnormal_logins_table", "column": "Anomaly Score"}] | [] | False |


## S15

类别 `data`；来源 `query_db`；调用 `071d08cfcb6e4a2faf192f8aa1d2a251`；状态 `success`。

```sql
SELECT lr."Login Method",
       COUNT(DISTINCT se."Event ID") AS sev_evt,
       SUM(se."Risk Score") AS risk_sum,
       COUNT(DISTINCT CASE WHEN se."Severity" IN ('High','Critical','Severe') THEN se."Event ID" END) AS high_sev
FROM security_events_table se
JOIN login_records_table lr ON se."Login Record ID" = lr."Login Record ID"
WHERE substr(lr."Login Time",1,4)='2024'
GROUP BY 1
ORDER BY sev_evt DESC
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-036/attempt-01/sql/S15.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-036/attempt-01/sql/S15.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-036/attempt-01/results/S15.rows.jsonl)；完整：True；SHA256：`140d8ac433329a1a8fd8d93027680d0c69582304c87d00b12313a041d516d5a0`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "se", "kind": "base", "block": null, "base_tables": ["security_events_table"]}, {"alias": "lr", "kind": "base", "block": null, "base_tables": ["login_records_table"]}] | [{"type": "INNER", "right": "login_records_table AS lr", "on": "se.\"Login Record ID\" = lr.\"Login Record ID\"", "using": []}] | ["lr.\"Login Method\""] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(DISTINCT se."Event ID") | [{"table": "security_events_table", "column": "Event ID"}] | [] | False |
| B1 | SUM(se."Risk Score") | [{"table": "security_events_table", "column": "Risk Score"}] | [] | False |
| B1 | COUNT(DISTINCT CASE WHEN se."Severity" IN ('High', 'Critical', 'Severe') THEN se."Event ID" END) | [{"table": "security_events_table", "column": "Event ID"}] | [{"table": "security_events_table", "column": "Severity"}] | False |


## S16

类别 `data`；来源 `query_db`；调用 `323b327f8aa54d619f2f60ff6cb47568`；状态 `success`。

```sql
SELECT lr."Login Method", lr."Two-Factor Authentication Method", lr."Two-Factor Authentication Status",
       COUNT(DISTINCT al."Anomaly ID") AS anomalies,
       COUNT(DISTINCT lr."Login Record ID") AS logins,
       ROUND(1.0*COUNT(DISTINCT al."Anomaly ID")/COUNT(DISTINCT lr."Login Record ID"),2) AS anomaly_per_login
FROM abnormal_logins_table al
JOIN login_records_table lr ON al."Login Record ID" = lr."Login Record ID"
WHERE substr(lr."Login Time",1,4)='2024'
GROUP BY 1,2,3
ORDER BY anomaly_per_login DESC
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-036/attempt-01/sql/S16.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-036/attempt-01/sql/S16.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-036/attempt-01/results/S16.rows.jsonl)；完整：True；SHA256：`959c35736eab2ffa9fb17fabdcd7067acc6783935a0078d3257e54f68b3e4ba7`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "al", "kind": "base", "block": null, "base_tables": ["abnormal_logins_table"]}, {"alias": "lr", "kind": "base", "block": null, "base_tables": ["login_records_table"]}] | [{"type": "INNER", "right": "login_records_table AS lr", "on": "al.\"Login Record ID\" = lr.\"Login Record ID\"", "using": []}] | ["lr.\"Login Method\"", "lr.\"Two-Factor Authentication Method\"", "lr.\"Two-Factor Authentication Status\""] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(DISTINCT al."Anomaly ID") | [{"table": "abnormal_logins_table", "column": "Anomaly ID"}] | [] | False |
| B1 | COUNT(DISTINCT lr."Login Record ID") | [{"table": "login_records_table", "column": "Login Record ID"}] | [] | False |
| B1 | COUNT(DISTINCT lr."Login Record ID") | [{"table": "login_records_table", "column": "Login Record ID"}] | [] | False |
| B1 | COUNT(DISTINCT al."Anomaly ID") | [{"table": "abnormal_logins_table", "column": "Anomaly ID"}] | [] | False |


## S17

类别 `data`；来源 `query_db`；调用 `e650e0a450b14a0db80d0ad47b73a1cd`；状态 `success`。

```sql
SELECT al."Anomaly Type", lr."Login Method", lr."Two-Factor Authentication Method", COUNT(*) AS cnt
FROM abnormal_logins_table al
JOIN login_records_table lr ON al."Login Record ID" = lr."Login Record ID"
WHERE substr(lr."Login Time",1,4)='2024'
GROUP BY 1,2,3
ORDER BY cnt DESC
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-036/attempt-01/sql/S17.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-036/attempt-01/sql/S17.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-036/attempt-01/results/S17.rows.jsonl)；完整：True；SHA256：`ae55ae5a3a161278b4cff6a9653c929f5ab6551ba1d8052adb834919509b2bb0`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "al", "kind": "base", "block": null, "base_tables": ["abnormal_logins_table"]}, {"alias": "lr", "kind": "base", "block": null, "base_tables": ["login_records_table"]}] | [{"type": "INNER", "right": "login_records_table AS lr", "on": "al.\"Login Record ID\" = lr.\"Login Record ID\"", "using": []}] | ["al.\"Anomaly Type\"", "lr.\"Login Method\"", "lr.\"Two-Factor Authentication Method\""] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |


## S18

类别 `data`；来源 `query_db`；调用 `1b5322bb984848cd9dd7074b972541d7`；状态 `success`。

```sql
SELECT COUNT(*) AS total_2024,
       COUNT(DISTINCT CASE WHEN al."Anomaly ID" IS NOT NULL THEN lr."Login Record ID" END) AS with_anomaly
FROM login_records_table lr
LEFT JOIN abnormal_logins_table al ON al."Login Record ID" = lr."Login Record ID"
WHERE substr(lr."Login Time",1,4)='2024'
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-036/attempt-01/sql/S18.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-036/attempt-01/sql/S18.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-036/attempt-01/results/S18.rows.jsonl)；完整：True；SHA256：`90bd5eca76ead09d04014384c2c5b76eb50ebbffab567ebaf25a549a53f428a1`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "lr", "kind": "base", "block": null, "base_tables": ["login_records_table"]}, {"alias": "al", "kind": "base", "block": null, "base_tables": ["abnormal_logins_table"]}] | [{"type": "LEFT", "right": "abnormal_logins_table AS al", "on": "al.\"Login Record ID\" = lr.\"Login Record ID\"", "using": []}] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |
| B1 | COUNT(DISTINCT CASE WHEN NOT al."Anomaly ID" IS NULL THEN lr."Login Record ID" END) | [{"table": "login_records_table", "column": "Login Record ID"}] | [{"table": "abnormal_logins_table", "column": "Anomaly ID"}] | False |


## S19

类别 `data`；来源 `query_db`；调用 `1561a76b5b784b70b18f441d64b401bf`；状态 `success`。

```sql
SELECT al."Anomaly Type", al."Risk Level", COUNT(*) AS cnt
FROM abnormal_logins_table al
JOIN login_records_table lr ON al."Login Record ID" = lr."Login Record ID"
WHERE substr(lr."Login Time",1,4)='2024'
GROUP BY 1,2
ORDER BY cnt DESC
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-036/attempt-01/sql/S19.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-036/attempt-01/sql/S19.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-036/attempt-01/results/S19.rows.jsonl)；完整：True；SHA256：`71f63b0935f8f7ca215dbdb59a603c42e486e9ea5967debc3af74b0777a09e6d`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "al", "kind": "base", "block": null, "base_tables": ["abnormal_logins_table"]}, {"alias": "lr", "kind": "base", "block": null, "base_tables": ["login_records_table"]}] | [{"type": "INNER", "right": "login_records_table AS lr", "on": "al.\"Login Record ID\" = lr.\"Login Record ID\"", "using": []}] | ["al.\"Anomaly Type\"", "al.\"Risk Level\""] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |


## S20

类别 `data`；来源 `query_db`；调用 `009dfb95b4344cc1a6cddfb87c2eb1fa`；状态 `success`。

```sql
SELECT se."Type", se."Severity", COUNT(*) AS cnt
FROM security_events_table se
JOIN login_records_table lr ON se."Login Record ID" = lr."Login Record ID"
WHERE substr(lr."Login Time",1,4)='2024'
GROUP BY 1,2
ORDER BY cnt DESC
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-036/attempt-01/sql/S20.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-036/attempt-01/sql/S20.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-036/attempt-01/results/S20.rows.jsonl)；完整：True；SHA256：`791e1da86aeb843713e12523cc19c590239e92be7eb1ffa9a6d2e6d5c8ca7a0b`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "se", "kind": "base", "block": null, "base_tables": ["security_events_table"]}, {"alias": "lr", "kind": "base", "block": null, "base_tables": ["login_records_table"]}] | [{"type": "INNER", "right": "login_records_table AS lr", "on": "se.\"Login Record ID\" = lr.\"Login Record ID\"", "using": []}] | ["se.\"Type\"", "se.\"Severity\""] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |


## S21

类别 `data`；来源 `query_db`；调用 `ccc6cbd6c73040a7897728d2321dad32`；状态 `success`。

```sql
SELECT "Authentication Method Name", "security level", "Enabled", "Maximum Attempts", "Lockout Duration", "Applicable User Types", "Authentication Protocol", "Encryption Method"
FROM authentication_methods_table
ORDER BY "security level" DESC
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-036/attempt-01/sql/S21.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-036/attempt-01/sql/S21.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-036/attempt-01/results/S21.rows.jsonl)；完整：True；SHA256：`0d176befc4655be88adcdee540fba84cb18e9b020056a5275cc1a666f1dc3476`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "authentication_methods_table", "kind": "base", "block": null, "base_tables": ["authentication_methods_table"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |


## S22

类别 `data`；来源 `query_db`；调用 `7c249ea642314360a2cce7eb274a7d03`；状态 `success`。

```sql
SELECT lr."Login Method", lr."Two-Factor Authentication Method",
       COUNT(DISTINCT lr."Login Record ID") AS logins,
       SUM(CASE WHEN lr."Authentication Status"='Failure' THEN 1 ELSE 0 END) AS failures,
       COUNT(DISTINCT al."Anomaly ID") AS anomalies,
       ROUND(AVG(al."Anomaly Score"),1) AS avg_anom_score,
       COUNT(DISTINCT se."Event ID") AS events,
       SUM(se."Risk Score") AS risk_sum,
       COUNT(DISTINCT CASE WHEN se."Severity" IN ('High','Severe') THEN se."Event ID" END) AS high_events
FROM login_records_table lr
LEFT JOIN abnormal_logins_table al ON al."Login Record ID"=lr."Login Record ID"
LEFT JOIN security_events_table se ON se."Login Record ID"=lr."Login Record ID"
WHERE substr(lr."Login Time",1,4)='2024'
GROUP BY 1,2
ORDER BY anomalies DESC
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-036/attempt-01/sql/S22.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-036/attempt-01/sql/S22.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-036/attempt-01/results/S22.rows.jsonl)；完整：True；SHA256：`69698639a4ecad76f76ecae30f43843d0679284fbaa666779b67dbb9f4ad2951`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "lr", "kind": "base", "block": null, "base_tables": ["login_records_table"]}, {"alias": "al", "kind": "base", "block": null, "base_tables": ["abnormal_logins_table"]}, {"alias": "se", "kind": "base", "block": null, "base_tables": ["security_events_table"]}] | [{"type": "LEFT", "right": "abnormal_logins_table AS al", "on": "al.\"Login Record ID\" = lr.\"Login Record ID\"", "using": []}, {"type": "LEFT", "right": "security_events_table AS se", "on": "se.\"Login Record ID\" = lr.\"Login Record ID\"", "using": []}] | ["lr.\"Login Method\"", "lr.\"Two-Factor Authentication Method\""] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(DISTINCT lr."Login Record ID") | [{"table": "login_records_table", "column": "Login Record ID"}] | [] | False |
| B1 | SUM(CASE WHEN lr."Authentication Status" = 'Failure' THEN 1 ELSE 0 END) | [] | [{"table": "login_records_table", "column": "Authentication Status"}] | False |
| B1 | COUNT(DISTINCT al."Anomaly ID") | [{"table": "abnormal_logins_table", "column": "Anomaly ID"}] | [] | False |
| B1 | COUNT(DISTINCT se."Event ID") | [{"table": "security_events_table", "column": "Event ID"}] | [] | False |
| B1 | SUM(se."Risk Score") | [{"table": "security_events_table", "column": "Risk Score"}] | [] | False |
| B1 | COUNT(DISTINCT CASE WHEN se."Severity" IN ('High', 'Severe') THEN se."Event ID" END) | [{"table": "security_events_table", "column": "Event ID"}] | [{"table": "security_events_table", "column": "Severity"}] | False |
| B1 | AVG(al."Anomaly Score") | [{"table": "abnormal_logins_table", "column": "Anomaly Score"}] | [] | False |


## S23

类别 `data`；来源 `query_db`；调用 `cea805cc5fe24b7aaebdfc7125c36911`；状态 `success`。

```sql
SELECT lr."Login Method", lr."Two-Factor Authentication Status", lr."Two-Factor Authentication Method",
       COUNT(DISTINCT lr."Login Record ID") AS logins,
       SUM(CASE WHEN lr."Authentication Status"='Failure' THEN 1 ELSE 0 END) AS failures,
       ROUND(100.0*SUM(CASE WHEN lr."Authentication Status"='Failure' THEN 1 ELSE 0 END)/COUNT(DISTINCT lr."Login Record ID"),1) AS fail_pct,
       COUNT(DISTINCT al."Anomaly ID") AS anomalies,
       ROUND(1.0*COUNT(DISTINCT al."Anomaly ID")/COUNT(DISTINCT lr."Login Record ID"),2) AS anom_rate,
       ROUND(AVG(al."Anomaly Score"),1) AS avg_anom_score,
       COUNT(DISTINCT se."Event ID") AS events,
       SUM(se."Risk Score") AS risk_sum
FROM login_records_table lr
LEFT JOIN abnormal_logins_table al ON al."Login Record ID"=lr."Login Record ID"
LEFT JOIN security_events_table se ON se."Login Record ID"=lr."Login Record ID"
WHERE substr(lr."Login Time",1,4)='2024'
GROUP BY 1,2,3
ORDER BY logins DESC
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-036/attempt-01/sql/S23.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-036/attempt-01/sql/S23.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-036/attempt-01/results/S23.rows.jsonl)；完整：True；SHA256：`3860f106170ea25ecb7af2bbdbe63cfdd1d5ece6ab8b06b88ddbc8dd78b62647`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "lr", "kind": "base", "block": null, "base_tables": ["login_records_table"]}, {"alias": "al", "kind": "base", "block": null, "base_tables": ["abnormal_logins_table"]}, {"alias": "se", "kind": "base", "block": null, "base_tables": ["security_events_table"]}] | [{"type": "LEFT", "right": "abnormal_logins_table AS al", "on": "al.\"Login Record ID\" = lr.\"Login Record ID\"", "using": []}, {"type": "LEFT", "right": "security_events_table AS se", "on": "se.\"Login Record ID\" = lr.\"Login Record ID\"", "using": []}] | ["lr.\"Login Method\"", "lr.\"Two-Factor Authentication Status\"", "lr.\"Two-Factor Authentication Method\""] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(DISTINCT lr."Login Record ID") | [{"table": "login_records_table", "column": "Login Record ID"}] | [] | False |
| B1 | SUM(CASE WHEN lr."Authentication Status" = 'Failure' THEN 1 ELSE 0 END) | [] | [{"table": "login_records_table", "column": "Authentication Status"}] | False |
| B1 | COUNT(DISTINCT al."Anomaly ID") | [{"table": "abnormal_logins_table", "column": "Anomaly ID"}] | [] | False |
| B1 | COUNT(DISTINCT se."Event ID") | [{"table": "security_events_table", "column": "Event ID"}] | [] | False |
| B1 | SUM(se."Risk Score") | [{"table": "security_events_table", "column": "Risk Score"}] | [] | False |
| B1 | AVG(al."Anomaly Score") | [{"table": "abnormal_logins_table", "column": "Anomaly Score"}] | [] | False |
| B1 | COUNT(DISTINCT lr."Login Record ID") | [{"table": "login_records_table", "column": "Login Record ID"}] | [] | False |
| B1 | COUNT(DISTINCT lr."Login Record ID") | [{"table": "login_records_table", "column": "Login Record ID"}] | [] | False |
| B1 | SUM(CASE WHEN lr."Authentication Status" = 'Failure' THEN 1 ELSE 0 END) | [] | [{"table": "login_records_table", "column": "Authentication Status"}] | False |
| B1 | COUNT(DISTINCT al."Anomaly ID") | [{"table": "abnormal_logins_table", "column": "Anomaly ID"}] | [] | False |


## S24

类别 `data`；来源 `query_db`；调用 `dab9c3356b7742818d6923eed6d8d1ad`；状态 `success`。

```sql
SELECT lr."Login Method", lr."Two-Factor Authentication Status", lr."Two-Factor Authentication Method",
       lr."Authentication Level",
       COUNT(*) AS cnt,
       SUM(CASE WHEN lr."Authentication Status"='Failure' THEN 1 ELSE 0 END) AS failures
FROM login_records_table lr
WHERE substr(lr."Login Time",1,4)='2024'
GROUP BY 1,2,3,4
ORDER BY 1,2,3,4
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-036/attempt-01/sql/S24.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-036/attempt-01/sql/S24.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-036/attempt-01/results/S24.rows.jsonl)；完整：True；SHA256：`3f1b7bd4ad4d2de282b0c15da2d46551fc51b69a1f828f35d6bc82f367918b09`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "lr", "kind": "base", "block": null, "base_tables": ["login_records_table"]}] | [] | ["lr.\"Login Method\"", "lr.\"Two-Factor Authentication Status\"", "lr.\"Two-Factor Authentication Method\"", "lr.\"Authentication Level\""] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |
| B1 | SUM(CASE WHEN lr."Authentication Status" = 'Failure' THEN 1 ELSE 0 END) | [] | [{"table": "login_records_table", "column": "Authentication Status"}] | False |


## S25

类别 `data`；来源 `query_db`；调用 `59cfed23cbf44d178b740ba05ec186f8`；状态 `success`。

```sql
SELECT lr."Login Method", lr."Two-Factor Authentication Method",
       al."Anomaly Type",
       COUNT(*) AS cnt,
       ROUND(AVG(al."Anomaly Score"),1) AS avg_score,
       ROUND(AVG(al."Device Anomaly Indicators"),2) AS avg_dev,
       ROUND(AVG(al."Network Anomaly Indicators"),2) AS avg_net,
       ROUND(AVG(al."Behavior Anomaly Indicators"),2) AS avg_beh
FROM abnormal_logins_table al
JOIN login_records_table lr ON al."Login Record ID"=lr."Login Record ID"
WHERE substr(lr."Login Time",1,4)='2024'
GROUP BY 1,2,3
ORDER BY 1,2,3
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-036/attempt-01/sql/S25.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-036/attempt-01/sql/S25.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-036/attempt-01/results/S25.rows.jsonl)；完整：True；SHA256：`64a3de30398cb89688752c63d94f1b5fe2e7f34d7aa8b8d45b76c693a64ba4d3`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "al", "kind": "base", "block": null, "base_tables": ["abnormal_logins_table"]}, {"alias": "lr", "kind": "base", "block": null, "base_tables": ["login_records_table"]}] | [{"type": "INNER", "right": "login_records_table AS lr", "on": "al.\"Login Record ID\" = lr.\"Login Record ID\"", "using": []}] | ["lr.\"Login Method\"", "lr.\"Two-Factor Authentication Method\"", "al.\"Anomaly Type\""] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |
| B1 | AVG(al."Anomaly Score") | [{"table": "abnormal_logins_table", "column": "Anomaly Score"}] | [] | False |
| B1 | AVG(al."Device Anomaly Indicators") | [{"table": "abnormal_logins_table", "column": "Device Anomaly Indicators"}] | [] | False |
| B1 | AVG(al."Network Anomaly Indicators") | [{"table": "abnormal_logins_table", "column": "Network Anomaly Indicators"}] | [] | False |
| B1 | AVG(al."Behavior Anomaly Indicators") | [{"table": "abnormal_logins_table", "column": "Behavior Anomaly Indicators"}] | [] | False |


## S26

类别 `data`；来源 `query_db`；调用 `1917f5a22c44480eb257e27d86d10dd0`；状态 `success`。

```sql
SELECT lr."Login Method", lr."Two-Factor Authentication Method",
       se."Type", se."Severity",
       COUNT(*) AS cnt,
       ROUND(AVG(se."Risk Score"),1) AS avg_risk
FROM security_events_table se
JOIN login_records_table lr ON se."Login Record ID"=lr."Login Record ID"
WHERE substr(lr."Login Time",1,4)='2024'
GROUP BY 1,2,3,4
ORDER BY 1,2,3,4
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-036/attempt-01/sql/S26.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-036/attempt-01/sql/S26.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-036/attempt-01/results/S26.rows.jsonl)；完整：True；SHA256：`685f7cda9edb1c41f4506e65e01146f01efd09ee4acc9fe4aa93db9f703ec32c`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "se", "kind": "base", "block": null, "base_tables": ["security_events_table"]}, {"alias": "lr", "kind": "base", "block": null, "base_tables": ["login_records_table"]}] | [{"type": "INNER", "right": "login_records_table AS lr", "on": "se.\"Login Record ID\" = lr.\"Login Record ID\"", "using": []}] | ["lr.\"Login Method\"", "lr.\"Two-Factor Authentication Method\"", "se.\"Type\"", "se.\"Severity\""] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |
| B1 | AVG(se."Risk Score") | [{"table": "security_events_table", "column": "Risk Score"}] | [] | False |


## S27

类别 `data`；来源 `query_db`；调用 `83578b87502e45679adbdeadb48c01fd`；状态 `success`。

```sql
SELECT "Login Method", COUNT(*) AS total_2024,
       SUM(CASE WHEN "Authentication Status"='Failure' THEN 1 ELSE 0 END) AS failures,
       ROUND(100.0*SUM(CASE WHEN "Authentication Status"='Failure' THEN 1 ELSE 0 END)/COUNT(*),1) AS fail_pct,
       COUNT(DISTINCT "Two-Factor Authentication Method") AS num_2fa_types
FROM login_records_table
WHERE substr("Login Time",1,4)='2024'
GROUP BY 1
ORDER BY total_2024 DESC
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-036/attempt-01/sql/S27.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-036/attempt-01/sql/S27.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-036/attempt-01/results/S27.rows.jsonl)；完整：True；SHA256：`081d8dc40e6213ab29122030d4565c4d7da985c43ca89d40829fce7c7ddca40c`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "login_records_table", "kind": "base", "block": null, "base_tables": ["login_records_table"]}] | [] | ["\"Login Method\""] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |
| B1 | SUM(CASE WHEN "Authentication Status" = 'Failure' THEN 1 ELSE 0 END) | [] | [{"table": "login_records_table", "column": "Authentication Status"}] | False |
| B1 | COUNT(DISTINCT "Two-Factor Authentication Method") | [{"table": "login_records_table", "column": "Two-Factor Authentication Method"}] | [] | False |
| B1 | COUNT(*) | [] | [] | True |
| B1 | SUM(CASE WHEN "Authentication Status" = 'Failure' THEN 1 ELSE 0 END) | [] | [{"table": "login_records_table", "column": "Authentication Status"}] | False |


## S28

类别 `data`；来源 `query_db`；调用 `844f5d9757f6463a9aebf658840b0ed1`；状态 `success`。

```sql
SELECT "Two-Factor Authentication Status", COUNT(*) AS total_2024,
       SUM(CASE WHEN "Authentication Status"='Failure' THEN 1 ELSE 0 END) AS failures,
       ROUND(100.0*SUM(CASE WHEN "Authentication Status"='Failure' THEN 1 ELSE 0 END)/COUNT(*),1) AS fail_pct
FROM login_records_table
WHERE substr("Login Time",1,4)='2024'
GROUP BY 1
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-036/attempt-01/sql/S28.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-036/attempt-01/sql/S28.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-036/attempt-01/results/S28.rows.jsonl)；完整：True；SHA256：`fa972ba6c42c76e50ec529554325b28373f05bbd664d0d4bbbe4e027f227ad9c`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "login_records_table", "kind": "base", "block": null, "base_tables": ["login_records_table"]}] | [] | ["\"Two-Factor Authentication Status\""] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |
| B1 | SUM(CASE WHEN "Authentication Status" = 'Failure' THEN 1 ELSE 0 END) | [] | [{"table": "login_records_table", "column": "Authentication Status"}] | False |
| B1 | COUNT(*) | [] | [] | True |
| B1 | SUM(CASE WHEN "Authentication Status" = 'Failure' THEN 1 ELSE 0 END) | [] | [{"table": "login_records_table", "column": "Authentication Status"}] | False |


## S29

类别 `data`；来源 `query_db`；调用 `a503f2c99f384eae89383a651523a08a`；状态 `success`。

```sql
SELECT "Two-Factor Authentication Method", COUNT(*) AS total_2024,
       SUM(CASE WHEN "Authentication Status"='Failure' THEN 1 ELSE 0 END) AS failures,
       ROUND(100.0*SUM(CASE WHEN "Authentication Status"='Failure' THEN 1 ELSE 0 END)/COUNT(*),1) AS fail_pct
FROM login_records_table
WHERE substr("Login Time",1,4)='2024'
GROUP BY 1
ORDER BY total_2024 DESC
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-036/attempt-01/sql/S29.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-036/attempt-01/sql/S29.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-036/attempt-01/results/S29.rows.jsonl)；完整：True；SHA256：`00e055dd63f3a85847f8ce1f98ac9af8ab300e10278e7ad052d269559caf2f7c`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "login_records_table", "kind": "base", "block": null, "base_tables": ["login_records_table"]}] | [] | ["\"Two-Factor Authentication Method\""] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |
| B1 | SUM(CASE WHEN "Authentication Status" = 'Failure' THEN 1 ELSE 0 END) | [] | [{"table": "login_records_table", "column": "Authentication Status"}] | False |
| B1 | COUNT(*) | [] | [] | True |
| B1 | SUM(CASE WHEN "Authentication Status" = 'Failure' THEN 1 ELSE 0 END) | [] | [{"table": "login_records_table", "column": "Authentication Status"}] | False |


## S30

类别 `data`；来源 `query_db`；调用 `508ffaf51af043a88d3d550d50b2bf80`；状态 `success`。

```sql
SELECT "Authentication Method Name",
       COUNT(*) AS n,
       ROUND(AVG("security level"),1) AS avg_sec_level,
       ROUND(AVG("Authentication Priority"),1) AS avg_priority,
       SUM(CASE WHEN "Enabled"='Enabled' THEN 1 ELSE 0 END) AS enabled_count,
       ROUND(AVG("Maximum Attempts"),1) AS avg_max_attempts,
       ROUND(AVG("Lockout Duration"),1) AS avg_lockout
FROM authentication_methods_table
WHERE "Authentication Method Name" IN ('SMS verification code','Email verification code','Dynamic Token','Fingerprint recognition','QR Code Scanning','Password Login')
GROUP BY 1
ORDER BY avg_sec_level DESC
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-036/attempt-01/sql/S30.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-036/attempt-01/sql/S30.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-036/attempt-01/results/S30.rows.jsonl)；完整：True；SHA256：`6f3d2f7b70239b3859433f87680bda0fc76bce977f232b672632dc5b5c18e91b`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "authentication_methods_table", "kind": "base", "block": null, "base_tables": ["authentication_methods_table"]}] | [] | ["\"Authentication Method Name\""] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |
| B1 | SUM(CASE WHEN "Enabled" = 'Enabled' THEN 1 ELSE 0 END) | [] | [{"table": "authentication_methods_table", "column": "Enabled"}] | False |
| B1 | AVG("security level") | [{"table": "authentication_methods_table", "column": "security level"}] | [] | False |
| B1 | AVG("Authentication Priority") | [{"table": "authentication_methods_table", "column": "Authentication Priority"}] | [] | False |
| B1 | AVG("Maximum Attempts") | [{"table": "authentication_methods_table", "column": "Maximum Attempts"}] | [] | False |
| B1 | AVG("Lockout Duration") | [{"table": "authentication_methods_table", "column": "Lockout Duration"}] | [] | False |


## S31

类别 `data`；来源 `query_db`；调用 `78e90681acbf4e448c8b3e327f30d0bc`；状态 `success`。

```sql
SELECT se."Severity", COUNT(*) AS cnt, ROUND(AVG(se."Risk Score"),1) AS avg_risk
FROM security_events_table se
JOIN login_records_table lr ON se."Login Record ID"=lr."Login Record ID"
WHERE substr(lr."Login Time",1,4)='2024'
GROUP BY 1
ORDER BY avg_risk DESC
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-036/attempt-01/sql/S31.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-036/attempt-01/sql/S31.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-036/attempt-01/results/S31.rows.jsonl)；完整：True；SHA256：`38874fa7e665c4fd4b5e0295bc682ea5601494eb5136da7c264f1141357b6a40`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "se", "kind": "base", "block": null, "base_tables": ["security_events_table"]}, {"alias": "lr", "kind": "base", "block": null, "base_tables": ["login_records_table"]}] | [{"type": "INNER", "right": "login_records_table AS lr", "on": "se.\"Login Record ID\" = lr.\"Login Record ID\"", "using": []}] | ["se.\"Severity\""] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |
| B1 | AVG(se."Risk Score") | [{"table": "security_events_table", "column": "Risk Score"}] | [] | False |


## S32

类别 `data`；来源 `query_db`；调用 `78e0111ba16a46d8be8dec396725ee55`；状态 `success`。

```sql
SELECT lr."Login Method", lr."Two-Factor Authentication Method",
       sl."Log Level", COUNT(*) AS cnt
FROM system_logs_table sl
JOIN login_records_table lr ON sl."Login Record ID"=lr."Login Record ID"
WHERE substr(lr."Login Time",1,4)='2024'
GROUP BY 1,2,3
ORDER BY cnt DESC
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-036/attempt-01/sql/S32.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-036/attempt-01/sql/S32.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-036/attempt-01/results/S32.rows.jsonl)；完整：True；SHA256：`0764d8e0ebc592528c20b190a3c7c9f7fcd325891298f82026479e3ba7b562b9`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "sl", "kind": "base", "block": null, "base_tables": ["system_logs_table"]}, {"alias": "lr", "kind": "base", "block": null, "base_tables": ["login_records_table"]}] | [{"type": "INNER", "right": "login_records_table AS lr", "on": "sl.\"Login Record ID\" = lr.\"Login Record ID\"", "using": []}] | ["lr.\"Login Method\"", "lr.\"Two-Factor Authentication Method\"", "sl.\"Log Level\""] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |


## S33

类别 `data`；来源 `query_db`；调用 `8931d19ac1cc4ed9ae82534ed205aeb9`；状态 `success`。

```sql
SELECT lr."Login Method", lr."Two-Factor Authentication Method",
       COUNT(DISTINCT ip."IP Record ID") AS ip_records,
       COUNT(DISTINCT ip."IP Address") AS distinct_ips,
       COUNT(DISTINCT ip."Province") AS provinces
FROM ip_address_information_table ip
JOIN login_records_table lr ON ip."Login record ID"=lr."Login Record ID"
WHERE substr(lr."Login Time",1,4)='2024'
GROUP BY 1,2
ORDER BY distinct_ips DESC
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-036/attempt-01/sql/S33.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-036/attempt-01/sql/S33.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-036/attempt-01/results/S33.rows.jsonl)；完整：True；SHA256：`fc3b6546d7b7c4b8d9ab0a27ada4c4c8afaa1276d8c4ceffc4c625a0ede20ef8`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "ip", "kind": "base", "block": null, "base_tables": ["ip_address_information_table"]}, {"alias": "lr", "kind": "base", "block": null, "base_tables": ["login_records_table"]}] | [{"type": "INNER", "right": "login_records_table AS lr", "on": "ip.\"Login record ID\" = lr.\"Login Record ID\"", "using": []}] | ["lr.\"Login Method\"", "lr.\"Two-Factor Authentication Method\""] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(DISTINCT ip."IP Record ID") | [{"table": "ip_address_information_table", "column": "IP Record ID"}] | [] | False |
| B1 | COUNT(DISTINCT ip."IP Address") | [{"table": "ip_address_information_table", "column": "IP Address"}] | [] | False |
| B1 | COUNT(DISTINCT ip."Province") | [{"table": "ip_address_information_table", "column": "Province"}] | [] | False |


## S34

类别 `data`；来源 `python`；调用 `6de256f933df491f9b73f0f4e032d44e`；状态 `success`。

```sql

SELECT lr."Login Method" AS login_method,
       lr."Two-Factor Authentication Method" AS tfa_method,
       COUNT(DISTINCT lr."Login Record ID") AS logins,
       SUM(CASE WHEN lr."Authentication Status"='Failure' THEN 1 ELSE 0 END) AS failures,
       COUNT(DISTINCT al."Anomaly ID") AS anomalies,
       COALESCE(ROUND(AVG(al."Anomaly Score"),1),0) AS avg_anom_score,
       COALESCE(SUM(al."Device Anomaly Indicators"),0) AS device_ind,
       COALESCE(SUM(al."Network Anomaly Indicators"),0) AS net_ind,
       COALESCE(SUM(al."Behavior Anomaly Indicators"),0) AS beh_ind,
       COUNT(DISTINCT se."Event ID") AS events,
       COALESCE(SUM(se."Risk Score"),0) AS risk_sum,
       COUNT(DISTINCT CASE WHEN se."Severity" IN ('High','Severe') THEN se."Event ID" END) AS high_events,
       COUNT(DISTINCT CASE WHEN se."Severity"='Severe' THEN se."Event ID" END) AS severe_events,
       COUNT(DISTINCT sl."Log ID") AS logs,
       COUNT(DISTINCT CASE WHEN sl."Log Level"='ERROR' THEN sl."Log ID" END) AS error_logs
FROM login_records_table lr
LEFT JOIN abnormal_logins_table al ON al."Login Record ID"=lr."Login Record ID"
LEFT JOIN security_events_table se ON se."Login Record ID"=lr."Login Record ID"
LEFT JOIN system_logs_table sl ON sl."Login Record ID"=lr."Login Record ID"
WHERE substr(lr."Login Time",1,4)='2024'
GROUP BY 1,2
ORDER BY anomalies DESC

```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-036/attempt-01/sql/S34.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-036/attempt-01/sql/S34.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-036/attempt-01/results/S34.rows.jsonl)；完整：True；SHA256：`752892e0fdcb75c3284ffb9044ea9b594dfb5d533c2606f8345158d72b0590a7`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "lr", "kind": "base", "block": null, "base_tables": ["login_records_table"]}, {"alias": "al", "kind": "base", "block": null, "base_tables": ["abnormal_logins_table"]}, {"alias": "se", "kind": "base", "block": null, "base_tables": ["security_events_table"]}, {"alias": "sl", "kind": "base", "block": null, "base_tables": ["system_logs_table"]}] | [{"type": "LEFT", "right": "abnormal_logins_table AS al", "on": "al.\"Login Record ID\" = lr.\"Login Record ID\"", "using": []}, {"type": "LEFT", "right": "security_events_table AS se", "on": "se.\"Login Record ID\" = lr.\"Login Record ID\"", "using": []}, {"type": "LEFT", "right": "system_logs_table AS sl", "on": "sl.\"Login Record ID\" = lr.\"Login Record ID\"", "using": []}] | ["lr.\"Login Method\"", "lr.\"Two-Factor Authentication Method\""] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(DISTINCT lr."Login Record ID") | [{"table": "login_records_table", "column": "Login Record ID"}] | [] | False |
| B1 | SUM(CASE WHEN lr."Authentication Status" = 'Failure' THEN 1 ELSE 0 END) | [] | [{"table": "login_records_table", "column": "Authentication Status"}] | False |
| B1 | COUNT(DISTINCT al."Anomaly ID") | [{"table": "abnormal_logins_table", "column": "Anomaly ID"}] | [] | False |
| B1 | COUNT(DISTINCT se."Event ID") | [{"table": "security_events_table", "column": "Event ID"}] | [] | False |
| B1 | COUNT(DISTINCT CASE WHEN se."Severity" IN ('High', 'Severe') THEN se."Event ID" END) | [{"table": "security_events_table", "column": "Event ID"}] | [{"table": "security_events_table", "column": "Severity"}] | False |
| B1 | COUNT(DISTINCT CASE WHEN se."Severity" = 'Severe' THEN se."Event ID" END) | [{"table": "security_events_table", "column": "Event ID"}] | [{"table": "security_events_table", "column": "Severity"}] | False |
| B1 | COUNT(DISTINCT sl."Log ID") | [{"table": "system_logs_table", "column": "Log ID"}] | [] | False |
| B1 | COUNT(DISTINCT CASE WHEN sl."Log Level" = 'ERROR' THEN sl."Log ID" END) | [{"table": "system_logs_table", "column": "Log ID"}] | [{"table": "system_logs_table", "column": "Log Level"}] | False |
| B1 | SUM(al."Device Anomaly Indicators") | [{"table": "abnormal_logins_table", "column": "Device Anomaly Indicators"}] | [] | False |
| B1 | SUM(al."Network Anomaly Indicators") | [{"table": "abnormal_logins_table", "column": "Network Anomaly Indicators"}] | [] | False |
| B1 | SUM(al."Behavior Anomaly Indicators") | [{"table": "abnormal_logins_table", "column": "Behavior Anomaly Indicators"}] | [] | False |
| B1 | SUM(se."Risk Score") | [{"table": "security_events_table", "column": "Risk Score"}] | [] | False |
| B1 | AVG(al."Anomaly Score") | [{"table": "abnormal_logins_table", "column": "Anomaly Score"}] | [] | False |


## S35

类别 `data`；来源 `python`；调用 `6de256f933df491f9b73f0f4e032d44e`；状态 `success`。

```sql

SELECT lr."Login Method" AS login_method,
       lr."Two-Factor Authentication Method" AS tfa_method,
       se."Severity",
       COUNT(*) AS cnt
FROM security_events_table se
JOIN login_records_table lr ON se."Login Record ID"=lr."Login Record ID"
WHERE substr(lr."Login Time",1,4)='2024'
GROUP BY 1,2,3
ORDER BY 1,2,3

```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-036/attempt-01/sql/S35.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-036/attempt-01/sql/S35.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-036/attempt-01/results/S35.rows.jsonl)；完整：True；SHA256：`e0f2c01188299088fa7cb7874e65ede9eff8afd17aabad39618f1118850518b3`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "se", "kind": "base", "block": null, "base_tables": ["security_events_table"]}, {"alias": "lr", "kind": "base", "block": null, "base_tables": ["login_records_table"]}] | [{"type": "INNER", "right": "login_records_table AS lr", "on": "se.\"Login Record ID\" = lr.\"Login Record ID\"", "using": []}] | ["lr.\"Login Method\"", "lr.\"Two-Factor Authentication Method\"", "se.\"Severity\""] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |


## S36

类别 `data`；来源 `query_db`；调用 `fd41aaff9c1042c2b9bf4355a3ceea52`；状态 `success`。

```sql
SELECT lr."Two-Factor Authentication Status",
       COUNT(DISTINCT lr."Login Record ID") AS logins,
       COUNT(DISTINCT al."Anomaly ID") AS anomalies,
       ROUND(1.0*COUNT(DISTINCT al."Anomaly ID")/COUNT(DISTINCT lr."Login Record ID"),2) AS anom_rate,
       ROUND(AVG(al."Anomaly Score"),1) AS avg_score,
       COUNT(DISTINCT se."Event ID") AS events,
       SUM(se."Risk Score") AS risk_sum,
       COUNT(DISTINCT CASE WHEN se."Severity" IN ('High','Severe') THEN se."Event ID" END) AS high_events
FROM login_records_table lr
LEFT JOIN abnormal_logins_table al ON al."Login Record ID"=lr."Login Record ID"
LEFT JOIN security_events_table se ON se."Login Record ID"=lr."Login Record ID"
WHERE substr(lr."Login Time",1,4)='2024'
GROUP BY 1
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-036/attempt-01/sql/S36.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-036/attempt-01/sql/S36.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-036/attempt-01/results/S36.rows.jsonl)；完整：True；SHA256：`272f4ab2ef451490a75e1335e5eb1ace0bfd99562f5d1f8d1fa9d3dae462c1f1`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "lr", "kind": "base", "block": null, "base_tables": ["login_records_table"]}, {"alias": "al", "kind": "base", "block": null, "base_tables": ["abnormal_logins_table"]}, {"alias": "se", "kind": "base", "block": null, "base_tables": ["security_events_table"]}] | [{"type": "LEFT", "right": "abnormal_logins_table AS al", "on": "al.\"Login Record ID\" = lr.\"Login Record ID\"", "using": []}, {"type": "LEFT", "right": "security_events_table AS se", "on": "se.\"Login Record ID\" = lr.\"Login Record ID\"", "using": []}] | ["lr.\"Two-Factor Authentication Status\""] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(DISTINCT lr."Login Record ID") | [{"table": "login_records_table", "column": "Login Record ID"}] | [] | False |
| B1 | COUNT(DISTINCT al."Anomaly ID") | [{"table": "abnormal_logins_table", "column": "Anomaly ID"}] | [] | False |
| B1 | COUNT(DISTINCT se."Event ID") | [{"table": "security_events_table", "column": "Event ID"}] | [] | False |
| B1 | SUM(se."Risk Score") | [{"table": "security_events_table", "column": "Risk Score"}] | [] | False |
| B1 | COUNT(DISTINCT CASE WHEN se."Severity" IN ('High', 'Severe') THEN se."Event ID" END) | [{"table": "security_events_table", "column": "Event ID"}] | [{"table": "security_events_table", "column": "Severity"}] | False |
| B1 | AVG(al."Anomaly Score") | [{"table": "abnormal_logins_table", "column": "Anomaly Score"}] | [] | False |
| B1 | COUNT(DISTINCT lr."Login Record ID") | [{"table": "login_records_table", "column": "Login Record ID"}] | [] | False |
| B1 | COUNT(DISTINCT al."Anomaly ID") | [{"table": "abnormal_logins_table", "column": "Anomaly ID"}] | [] | False |


## S37

类别 `data`；来源 `query_db`；调用 `0d7b1eeb64b149f3a782f62db35e7151`；状态 `success`。

```sql
SELECT lr."Login Method", lr."Two-Factor Authentication Status",
       COUNT(DISTINCT al."Anomaly ID") AS anomalies,
       COUNT(DISTINCT se."Event ID") AS events,
       SUM(se."Risk Score") AS risk_sum
FROM login_records_table lr
LEFT JOIN abnormal_logins_table al ON al."Login Record ID"=lr."Login Record ID"
LEFT JOIN security_events_table se ON se."Login Record ID"=lr."Login Record ID"
WHERE substr(lr."Login Time",1,4)='2024'
GROUP BY 1,2
ORDER BY 1,2
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-036/attempt-01/sql/S37.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-036/attempt-01/sql/S37.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-036/attempt-01/results/S37.rows.jsonl)；完整：True；SHA256：`cd335a58835ec40bccd6d441d357ce575293827a75b49a18cfc08bba353d1424`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "lr", "kind": "base", "block": null, "base_tables": ["login_records_table"]}, {"alias": "al", "kind": "base", "block": null, "base_tables": ["abnormal_logins_table"]}, {"alias": "se", "kind": "base", "block": null, "base_tables": ["security_events_table"]}] | [{"type": "LEFT", "right": "abnormal_logins_table AS al", "on": "al.\"Login Record ID\" = lr.\"Login Record ID\"", "using": []}, {"type": "LEFT", "right": "security_events_table AS se", "on": "se.\"Login Record ID\" = lr.\"Login Record ID\"", "using": []}] | ["lr.\"Login Method\"", "lr.\"Two-Factor Authentication Status\""] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(DISTINCT al."Anomaly ID") | [{"table": "abnormal_logins_table", "column": "Anomaly ID"}] | [] | False |
| B1 | COUNT(DISTINCT se."Event ID") | [{"table": "security_events_table", "column": "Event ID"}] | [] | False |
| B1 | SUM(se."Risk Score") | [{"table": "security_events_table", "column": "Risk Score"}] | [] | False |


## S38

类别 `data`；来源 `query_db`；调用 `f3cddd2bfb1f4b37a92621a8e3dfebe7`；状态 `success`。

```sql
SELECT lr."Login Method", lr."Two-Factor Authentication Status",
       COUNT(DISTINCT lr."Login Record ID") AS logins,
       COUNT(DISTINCT al."Anomaly ID") AS anomalies,
       ROUND(1.0*COUNT(DISTINCT al."Anomaly ID")/COUNT(DISTINCT lr."Login Record ID"),3) AS anom_per_login,
       COUNT(DISTINCT se."Event ID") AS events,
       SUM(se."Risk Score") AS risk_sum,
       ROUND(1.0*SUM(se."Risk Score")/COUNT(DISTINCT lr."Login Record ID"),1) AS risk_per_login
FROM login_records_table lr
LEFT JOIN abnormal_logins_table al ON al."Login Record ID"=lr."Login Record ID"
LEFT JOIN security_events_table se ON se."Login Record ID"=lr."Login Record ID"
WHERE substr(lr."Login Time",1,4)='2024'
GROUP BY 1,2
ORDER BY 1,2
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-036/attempt-01/sql/S38.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-036/attempt-01/sql/S38.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-036/attempt-01/results/S38.rows.jsonl)；完整：True；SHA256：`6bb8a15897e3a91afd1947b7a1c513f9f58aae155ecdf1417d25b536a8bc853a`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "lr", "kind": "base", "block": null, "base_tables": ["login_records_table"]}, {"alias": "al", "kind": "base", "block": null, "base_tables": ["abnormal_logins_table"]}, {"alias": "se", "kind": "base", "block": null, "base_tables": ["security_events_table"]}] | [{"type": "LEFT", "right": "abnormal_logins_table AS al", "on": "al.\"Login Record ID\" = lr.\"Login Record ID\"", "using": []}, {"type": "LEFT", "right": "security_events_table AS se", "on": "se.\"Login Record ID\" = lr.\"Login Record ID\"", "using": []}] | ["lr.\"Login Method\"", "lr.\"Two-Factor Authentication Status\""] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(DISTINCT lr."Login Record ID") | [{"table": "login_records_table", "column": "Login Record ID"}] | [] | False |
| B1 | COUNT(DISTINCT al."Anomaly ID") | [{"table": "abnormal_logins_table", "column": "Anomaly ID"}] | [] | False |
| B1 | COUNT(DISTINCT se."Event ID") | [{"table": "security_events_table", "column": "Event ID"}] | [] | False |
| B1 | SUM(se."Risk Score") | [{"table": "security_events_table", "column": "Risk Score"}] | [] | False |
| B1 | COUNT(DISTINCT lr."Login Record ID") | [{"table": "login_records_table", "column": "Login Record ID"}] | [] | False |
| B1 | COUNT(DISTINCT lr."Login Record ID") | [{"table": "login_records_table", "column": "Login Record ID"}] | [] | False |
| B1 | COUNT(DISTINCT al."Anomaly ID") | [{"table": "abnormal_logins_table", "column": "Anomaly ID"}] | [] | False |
| B1 | SUM(se."Risk Score") | [{"table": "security_events_table", "column": "Risk Score"}] | [] | False |


## S39

类别 `data`；来源 `python`；调用 `85c887d3bc504e4891fb8e0f8184d592`；状态 `success`。

```sql

SELECT lr."Login Method" AS login_method,
       lr."Two-Factor Authentication Status" AS tfa_status,
       COUNT(DISTINCT lr."Login Record ID") AS logins,
       COUNT(DISTINCT al."Anomaly ID") AS anomalies,
       ROUND(1.0*COUNT(DISTINCT al."Anomaly ID")/COUNT(DISTINCT lr."Login Record ID"),3) AS anom_per_login,
       COUNT(DISTINCT se."Event ID") AS events,
       SUM(se."Risk Score") AS risk_sum,
       ROUND(1.0*SUM(se."Risk Score")/COUNT(DISTINCT lr."Login Record ID"),1) AS risk_per_login
FROM login_records_table lr
LEFT JOIN abnormal_logins_table al ON al."Login Record ID"=lr."Login Record ID"
LEFT JOIN security_events_table se ON se."Login Record ID"=lr."Login Record ID"
WHERE substr(lr."Login Time",1,4)='2024'
GROUP BY 1,2
ORDER BY 1,2

```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-036/attempt-01/sql/S39.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-036/attempt-01/sql/S39.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-036/attempt-01/results/S39.rows.jsonl)；完整：True；SHA256：`6bb8a15897e3a91afd1947b7a1c513f9f58aae155ecdf1417d25b536a8bc853a`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "lr", "kind": "base", "block": null, "base_tables": ["login_records_table"]}, {"alias": "al", "kind": "base", "block": null, "base_tables": ["abnormal_logins_table"]}, {"alias": "se", "kind": "base", "block": null, "base_tables": ["security_events_table"]}] | [{"type": "LEFT", "right": "abnormal_logins_table AS al", "on": "al.\"Login Record ID\" = lr.\"Login Record ID\"", "using": []}, {"type": "LEFT", "right": "security_events_table AS se", "on": "se.\"Login Record ID\" = lr.\"Login Record ID\"", "using": []}] | ["lr.\"Login Method\"", "lr.\"Two-Factor Authentication Status\""] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(DISTINCT lr."Login Record ID") | [{"table": "login_records_table", "column": "Login Record ID"}] | [] | False |
| B1 | COUNT(DISTINCT al."Anomaly ID") | [{"table": "abnormal_logins_table", "column": "Anomaly ID"}] | [] | False |
| B1 | COUNT(DISTINCT se."Event ID") | [{"table": "security_events_table", "column": "Event ID"}] | [] | False |
| B1 | SUM(se."Risk Score") | [{"table": "security_events_table", "column": "Risk Score"}] | [] | False |
| B1 | COUNT(DISTINCT lr."Login Record ID") | [{"table": "login_records_table", "column": "Login Record ID"}] | [] | False |
| B1 | COUNT(DISTINCT lr."Login Record ID") | [{"table": "login_records_table", "column": "Login Record ID"}] | [] | False |
| B1 | COUNT(DISTINCT al."Anomaly ID") | [{"table": "abnormal_logins_table", "column": "Anomaly ID"}] | [] | False |
| B1 | SUM(se."Risk Score") | [{"table": "security_events_table", "column": "Risk Score"}] | [] | False |


## S40

类别 `data`；来源 `python`；调用 `85c887d3bc504e4891fb8e0f8184d592`；状态 `success`。

```sql

SELECT lr."Login Method" AS login_method,
       lr."Two-Factor Authentication Method" AS tfa_method,
       COUNT(DISTINCT lr."Login Record ID") AS logins,
       SUM(CASE WHEN lr."Authentication Status"='Failure' THEN 1 ELSE 0 END) AS failures,
       COUNT(DISTINCT al."Anomaly ID") AS anomalies,
       ROUND(AVG(al."Anomaly Score"),1) AS avg_anom_score,
       COUNT(DISTINCT se."Event ID") AS events,
       SUM(se."Risk Score") AS risk_sum,
       COUNT(DISTINCT CASE WHEN se."Severity" IN ('High','Severe') THEN se."Event ID" END) AS high_events
FROM login_records_table lr
LEFT JOIN abnormal_logins_table al ON al."Login Record ID"=lr."Login Record ID"
LEFT JOIN security_events_table se ON se."Login Record ID"=lr."Login Record ID"
WHERE substr(lr."Login Time",1,4)='2024'
GROUP BY 1,2

```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-036/attempt-01/sql/S40.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-036/attempt-01/sql/S40.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-036/attempt-01/results/S40.rows.jsonl)；完整：True；SHA256：`0924492326a6a139890abd087083faf3133d23a2ce5c6b7e395f9cfb555e75ea`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "lr", "kind": "base", "block": null, "base_tables": ["login_records_table"]}, {"alias": "al", "kind": "base", "block": null, "base_tables": ["abnormal_logins_table"]}, {"alias": "se", "kind": "base", "block": null, "base_tables": ["security_events_table"]}] | [{"type": "LEFT", "right": "abnormal_logins_table AS al", "on": "al.\"Login Record ID\" = lr.\"Login Record ID\"", "using": []}, {"type": "LEFT", "right": "security_events_table AS se", "on": "se.\"Login Record ID\" = lr.\"Login Record ID\"", "using": []}] | ["lr.\"Login Method\"", "lr.\"Two-Factor Authentication Method\""] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(DISTINCT lr."Login Record ID") | [{"table": "login_records_table", "column": "Login Record ID"}] | [] | False |
| B1 | SUM(CASE WHEN lr."Authentication Status" = 'Failure' THEN 1 ELSE 0 END) | [] | [{"table": "login_records_table", "column": "Authentication Status"}] | False |
| B1 | COUNT(DISTINCT al."Anomaly ID") | [{"table": "abnormal_logins_table", "column": "Anomaly ID"}] | [] | False |
| B1 | COUNT(DISTINCT se."Event ID") | [{"table": "security_events_table", "column": "Event ID"}] | [] | False |
| B1 | SUM(se."Risk Score") | [{"table": "security_events_table", "column": "Risk Score"}] | [] | False |
| B1 | COUNT(DISTINCT CASE WHEN se."Severity" IN ('High', 'Severe') THEN se."Event ID" END) | [{"table": "security_events_table", "column": "Event ID"}] | [{"table": "security_events_table", "column": "Severity"}] | False |
| B1 | AVG(al."Anomaly Score") | [{"table": "abnormal_logins_table", "column": "Anomaly Score"}] | [] | False |

