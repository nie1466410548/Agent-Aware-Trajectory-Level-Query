# dacomp-030

As Coca-Cola’s sales lead, which Outlet Types should I increase or reduce the contract sig…

运行：已提交。官方未评分。全部 SQL 尝试/成功 38/37；数据 SQL 32/31；Python 3 次。

完整原题：

As Coca-Cola’s sales lead, which Outlet Types should I increase or reduce the contract signing volume for? Please provide recommendations after conducting a comprehensive analysis of key data such as Target Achievement Rate, customer complaint issues, and Sales, along with other key metrics.

| 表 | 行数 | 列数 |
| --- | --- | --- |
| activity_information_table | 615 | 14 |
| agreement_workflow_table | 409 | 12 |
| allowance_issuance_table | 242 | 13 |
| allowance_rule_table | 535 | 11 |
| appeal_record_table | 268 | 16 |
| assessment_result_table | 373 | 14 |
| assessment_standard_table | 586 | 14 |
| contract_information_table | 577 | 12 |
| coupon_information_table | 449 | 13 |
| customer_information_table | 615 | 11 |
| customer_management_table | 582 | 16 |
| device_information_table | 500 | 15 |
| expense_allocation_table | 577 | 13 |
| photo_information_table | 326 | 15 |
| point_of_sale_(pos)_information | 583 | 13 |
| sales_data_table | 628 | 12 |


实际路线（分析者依据 SQL/源码概括，不代表 Agent 自述）：SQL 汇总终端类型的达标、销售、投诉与合同指标 → Python 将手工转录的汇总值转为百分位评分 → 计算增减签约建议及合同效率 → 绘图。

数据库大小：2,064,384 字节。

## 数据 SQL

| SQL | 状态 | 基础表 | Join 输入/类型 | GROUP BY | 聚合表达式 | 结果行数 | 数据库 ms |
| --- | --- | --- | --- | --- | --- | --- | --- |
| [S4/Q1](#s4) | success | ["\"point_of_sale_(pos)_information\""] | 0 / {} | [] | [] | 20 | 0.411 |
| [S5/Q2](#s5) | success | ["sales_data_table"] | 0 / {} | [] | [] | 20 | 0.381 |
| [S6/Q3](#s6) | success | ["contract_information_table"] | 0 / {} | [] | [] | 20 | 0.301 |
| [S7/Q4](#s7) | success | ["customer_information_table"] | 0 / {} | [] | [] | 20 | 0.372 |
| [S8/Q5](#s8) | success | ["\"point_of_sale_(pos)_information\""] | 0 / {} | ["\"Outlet Type\""] | ["COUNT(*)", "COUNT(DISTINCT \"Outlet ID\")"] | 10 | 0.818 |
| [S9/Q6](#s9) | success | ["\"point_of_sale_(pos)_information\"", "appeal_record_table", "assessment_result_table", "contract_information_table", "customer_information_table", "customer_management_table", "device_information_table", "sales_data_table"] | 0 / {} | [] | ["COUNT(*)", "COUNT(*)", "COUNT(*)", "COUNT(*)", "COUNT(*)", "COUNT(*)", "COUNT(*)", "COUNT(*)"] | 1 | 0.77 |
| [S10/Q7](#s10) | success | ["appeal_record_table"] | 0 / {} | [] | [] | 10 | 0.392 |
| [S11/Q8](#s11) | success | ["customer_management_table"] | 0 / {} | ["\"Warning Record\""] | ["COUNT(*)"] | 1 | 0.499 |
| [S12/Q9](#s12) | success | ["customer_management_table"] | 0 / {} | [] | [] | 10 | 0.369 |
| [S13/Q10](#s13) | success | ["customer_management_table"] | 0 / {} | ["\"Warning Record\""] | ["COUNT(*)"] | 1 | 0.433 |
| [S14/Q11](#s14) | success | ["customer_management_table"] | 0 / {} | ["\"Renewal Likelihood\""] | ["COUNT(*)"] | 3 | 0.582 |
| [S15/Q12](#s15) | success | ["customer_management_table"] | 0 / {} | ["\"Exclusion Flag\""] | ["COUNT(*)"] | 1 | 0.416 |
| [S16/Q13](#s16) | success | ["customer_information_table"] | 0 / {} | ["\"Contract Status\""] | ["COUNT(*)"] | 2 | 0.511 |
| [S17/Q14](#s17) | success | ["sales_data_table"] | 0 / {} | ["\"Data Status\""] | ["COUNT(*)"] | 2 | 0.516 |
| [S20/Q15](#s20) | success | ["customer_management_table"] | 0 / {} | ["\" Warning Record\""] | ["COUNT(*)"] | 3 | 0.528 |
| [S21/Q16](#s21) | success | ["customer_management_table"] | 0 / {} | ["\" Exclusion Flag\""] | ["COUNT(*)"] | 2 | 0.526 |
| [S22/Q17](#s22) | failed | ["\"point_of_sale_(pos)_information\"", "sales_data_table"] | 2 / {'LEFT': 1} | ["p.\"Outlet Type\""] | ["COUNT(DISTINCT p.\"Outlet ID\")", "AVG(p.\"Actual Sales (cases)\")", "AVG(p.\"Sales Target\")", "AVG(p.\"VPO Value\")", "AVG(p.\"PC Value\")", "AVG(s.\"Target Achievement Rate\")", "AVG(s.\"Sales Volume (Units)\")", "AVG(s.\"Sales (Value)\")", "SUM(s.\"Sales Volume (Units)\")", "SUM(s.\"Sales (Value)\")", "AVG(s.\"YoY Growth Rate\")", "AVG(s.\"MoM Growth Rate\")", "SUM(p.\"Actual Sales (cases)\")", "SUM(p.\"Sales Target\")"] | unknown | 未取得；调用总时长 0.231 ms |
| [S24/Q18](#s24) | success | ["\"point_of_sale_(pos)_information\"", "sales_data_table"] | 2 / {'LEFT': 1} | ["p.\"Outlet Type\""] | ["COUNT(DISTINCT p.\"Outlet ID\")", "AVG(p.\"Actual Sales (cases)\")", "AVG(p.\"Sales Target\")", "AVG(p.\"VPO Value\")", "AVG(p.\"PC Value\")", "AVG(s.\" Target Achievement Rate\")", "AVG(s.\"Sales Volume (Units)\")", "AVG(s.\"Sales (Value)\")", "SUM(s.\"Sales Volume (Units)\")", "SUM(s.\"Sales (Value)\")", "AVG(s.\" YoY Growth Rate\")", "AVG(s.\"MoM Growth Rate\")", "SUM(p.\"Actual Sales (cases)\")", "SUM(p.\"Sales Target\")"] | 10 | 2.313 |
| [S25/Q19](#s25) | success | ["\"point_of_sale_(pos)_information\"", "contract_information_table"] | 2 / {'LEFT': 1} | ["p.\"Outlet Type\""] | ["COUNT(c.\"Agreement ID\")", "COUNT(DISTINCT p.\"Outlet ID\")", "SUM(CASE WHEN c.\"Renewal Flag\" = 'Yes' THEN 1 ELSE 0 END)", "AVG(c.\"Signing Amount (CNY)\")", "SUM(c.\"Signing Amount (CNY)\")", "AVG(c.\"Same-store Ratio\")", "AVG(CASE WHEN c.\"Renewal Flag\" = 'Yes' THEN 1.0 ELSE 0 END)", "COUNT(DISTINCT p.\"Outlet ID\")", "COUNT(c.\"Agreement ID\")"] | 10 | 1.907 |
| [S26/Q20](#s26) | success | ["\"point_of_sale_(pos)_information\"", "customer_management_table"] | 2 / {'LEFT': 1} | ["p.\"Outlet Type\""] | ["COUNT(cm.\"Management ID\")", "SUM(CASE WHEN cm.\" Warning Record\" = 'Complaint Record' THEN 1 ELSE 0 END)", "SUM(CASE WHEN cm.\" Warning Record\" = 'Quality Issue' THEN 1 ELSE 0 END)", "SUM(CASE WHEN cm.\"Renewal Likelihood\" = 'High' THEN 1 ELSE 0 END)", "SUM(CASE WHEN cm.\"Renewal Likelihood\" = 'Low' THEN 1 ELSE 0 END)", "AVG(cm.\"Training Count\")", "COUNT(cm.\"Management ID\")", "SUM(CASE WHEN cm.\" Warning Record\" = 'Complaint Record' THEN 1 ELSE 0 END)"] | 10 | 1.869 |
| [S27/Q21](#s27) | success | ["\"point_of_sale_(pos)_information\"", "assessment_result_table"] | 2 / {'LEFT': 1} | ["p.\"Outlet Type\""] | ["COUNT(a.\"Assessment ID\")", "AVG(a.\"Score\")", "AVG(a.\"Assessment pass rate\")", "AVG(a.\"Historical pass trend (%)\")", "AVG(a.\"Photo upload count\")", "AVG(a.\"Qualified photo count\")", "AVG(a.\"Qualified photo count\" * 1.0 / NULLIF(a.\"Photo upload count\", 0))"] | 10 | 1.527 |
| [S28/Q22](#s28) | success | ["\"point_of_sale_(pos)_information\"", "appeal_record_table"] | 2 / {'LEFT': 1} | ["p.\"Outlet Type\""] | ["COUNT(ap.\"Appeal ID\")", "SUM(CASE WHEN ap.\"Handling Status\" = 'Completed' THEN 1 ELSE 0 END)", "SUM(CASE WHEN ap.\"Processing Result\" = 'Modify score' THEN 1 ELSE 0 END)", "COUNT(DISTINCT p.\"Outlet ID\")", "COUNT(ap.\"Appeal ID\")"] | 10 | 1.428 |
| [S29/Q23](#s29) | success | ["\"point_of_sale_(pos)_information\"", "customer_information_table"] | 2 / {'LEFT': 1} | ["p.\"Outlet Type\""] | ["COUNT(DISTINCT p.\"Customer ID\")", "SUM(CASE WHEN ci.\"Customer Level\" = 'A' THEN 1 ELSE 0 END)", "SUM(CASE WHEN ci.\"Customer Level\" = 'B' THEN 1 ELSE 0 END)", "SUM(CASE WHEN ci.\"Customer Level\" = 'C' THEN 1 ELSE 0 END)", "SUM(CASE WHEN ci.\"Customer Level\" = 'D' THEN 1 ELSE 0 END)", "AVG(ci.\"Sales History\")"] | 10 | 1.757 |
| [S30/Q24](#s30) | success | ["\"point_of_sale_(pos)_information\"", "contract_information_table"] | 2 / {'INNER': 1} | ["p.\"Outlet Type\"", "c.\"Signing Type (GSB/Spark)\""] | ["COUNT(*)", "AVG(c.\"Signing Amount (CNY)\")"] | 20 | 1.435 |
| [S31/Q25](#s31) | success | ["\"point_of_sale_(pos)_information\"", "device_information_table"] | 2 / {'LEFT': 1} | ["p.\"Outlet Type\""] | ["COUNT(d.\"Equipment record code\")", "SUM(d.\"Number of failures\")", "AVG(d.\"Number of failures\")"] | 10 | 1.343 |
| [S32/Q26](#s32) | success | ["\"point_of_sale_(pos)_information\""] | 0 / {} | [] | [] | 20 | 0.271 |
| [S33/Q27](#s33) | success | ["\"point_of_sale_(pos)_information\"", "appeal_record_table", "assessment_result_table", "contract_information_table", "customer_management_table", "sales_data_table"] | 6 / {'INNER': 1, 'LEFT': 9} | ["p.\"Outlet Type\"", "p.\"Outlet Type\"", "p.\"Outlet Type\"", "p.\"Outlet Type\"", "p.\"Outlet Type\"", "p.\"Outlet Type\""] | ["COUNT(DISTINCT p.\"Outlet ID\")", "AVG(p.\"VPO Value\")", "AVG(p.\"PC Value\")", "AVG(CAST(REPLACE(p.\"Qualification Rate\", '%', '') AS REAL))", "SUM(p.\"Actual Sales (cases)\")", "SUM(p.\"Sales Target\")", "AVG(s.\" Target Achievement Rate\")", "AVG(s.\" YoY Growth Rate\")", "AVG(s.\"MoM Growth Rate\")", "SUM(s.\"Sales (Value)\")", "AVG(s.\"Sales (Value)\")", "COUNT(c.\"Agreement ID\")", "SUM(c.\"Signing Amount (CNY)\")", "AVG(c.\"Signing Amount (CNY)\")", "AVG(CASE WHEN c.\"Renewal Flag\" = 'Yes' THEN 1.0 ELSE 0 END)", "COUNT(cm.\"Management ID\")", "COUNT(cm.\"Management ID\")", "COUNT(cm.\"Management ID\")", "SUM(CASE WHEN cm.\"Renewal Likelihood\" = 'High' THEN 1 ELSE 0 END)", "SUM(CASE WHEN cm.\" Warning Record\" = 'Complaint Record' THEN 1 ELSE 0 END)", "SUM(CASE WHEN cm.\" Warning Record\" = 'Quality Issue' THEN 1 ELSE 0 END)", "AVG(a.\"Assessment pass rate\")", "AVG(a.\"Score\")", "COUNT(DISTINCT p.\"Outlet ID\")", "COUNT(ap.\"Appeal ID\")"] | 10 | 6.816 |
| [S34/Q28](#s34) | success | ["\"point_of_sale_(pos)_information\"", "expense_allocation_table"] | 2 / {'LEFT': 1} | ["p.\"Outlet Type\""] | ["AVG(e.\"Annual Budget\")", "AVG(e.\"Monthly Allocation\")", "AVG(e.\"Amount Used\")", "AVG(e.\"Remaining Amount\")", "SUM(e.\"Amount Used\")", "SUM(e.\"Annual Budget\")"] | 10 | 1.595 |
| [S35/Q29](#s35) | success | ["\"point_of_sale_(pos)_information\"", "device_information_table"] | 2 / {'LEFT': 1} | ["p.\"Outlet Type\""] | ["COUNT(d.\"Equipment record code\")", "AVG(d.\"Number of failures\")"] | 10 | 1.294 |
| [S36/Q30](#s36) | success | ["\"point_of_sale_(pos)_information\"", "assessment_result_table", "contract_information_table", "customer_management_table", "sales_data_table"] | 5 / {'LEFT': 4} | ["p.\"Outlet Type\""] | ["COUNT(DISTINCT s.\"Data Record ID\")", "COUNT(DISTINCT c.\"Agreement ID\")", "COUNT(DISTINCT cm.\"Management ID\")", "COUNT(DISTINCT a.\"Assessment ID\")"] | 10 | 3.953 |
| [S37/Q31](#s37) | success | ["\"point_of_sale_(pos)_information\"", "sales_data_table"] | 2 / {'INNER': 1} | ["p.\"Outlet Type\""] | ["MIN(s.\" Target Achievement Rate\")", "AVG(s.\" Target Achievement Rate\")", "MAX(s.\" Target Achievement Rate\")", "AVG(s.\"Sales (Value)\")", "COUNT(s.\"Data Record ID\")"] | 10 | 1.407 |
| [S38/Q32](#s38) | success | ["\"point_of_sale_(pos)_information\"", "photo_information_table"] | 2 / {'LEFT': 1} | ["p.\"Outlet Type\""] | ["COUNT(ph.\"Photo ID\")", "SUM(CASE WHEN ph.\"Review Status\" = 'Failed' OR ph.\"Review Status\" = 'Rejected' THEN 1 ELSE 0 END)", "COUNT(ph.\"Photo ID\")", "SUM(CASE WHEN ph.\"Review Status\" = 'Failed' OR ph.\"Review Status\" = 'Rejected' THEN 1 ELSE 0 END)"] | 10 | 1.211 |


## 元数据和设置

| SQL | 类别 | 状态 | 内容 |
| --- | --- | --- | --- |
| S1 | connection_setup | success | PRAGMA query_only=ON |
| S2 | metadata | success | SELECT name,sql FROM sqlite_master WHERE type='table' ORDER BY name |
| S3 | metadata | success | SELECT name FROM sqlite_master WHERE type='table' ORDER BY name |
| S18 | metadata | success | PRAGMA table_info(customer_management_table) |
| S19 | metadata | success | PRAGMA table_info("point_of_sale_(pos)_information") |
| S23 | metadata | success | PRAGMA table_info(sales_data_table) |


## Python 与执行位置

人工源码审查：**database_first_violation**。Python scores outlet types using percentile ranks, weighted arithmetic, threshold classification and contract-efficiency ratios. These SQL-capable calculations deviate from database-first, even though the input is a small summary. P1/P2 explicitly label their literal arrays as data from S33; literal transcription is retained in code, not automatically treated as a proven exact result-dependency edge. Figure rendering is allowed. The only generated MV candidate failed comparison and contributes zero verified coverage. [证据](../reviews/dacomp-030.json)。

P1：I have already aggregated all key metrics per outlet type in SQL (S33). Python is needed to build a composite performance/risk scoring model, rank outlet types, and generate the recommendation matrix and charts - these statistical/scoring computations and visualizations are not reasonably supported by SQLite.

[源码](../../../runs/dsv4flash-db-first-full-01/dacomp-030/attempt-01/python/P1.py)；[输出](../../../runs/dsv4flash-db-first-full-01/dacomp-030/attempt-01/python/P1.stdout)；[错误](../../../runs/dsv4flash-db-first-full-01/dacomp-030/attempt-01/python/P1.stderr)。检出需人工核验的 SQL 可实现操作：sort_values(；不能仅凭理由判为合规。

P2：Creating the recommendation matrix chart (performance vs risk scatter plot), a bar chart of composite scores, and a heatmap of key metrics. This requires matplotlib for visualization which is outside SQL capabilities.

[源码](../../../runs/dsv4flash-db-first-full-01/dacomp-030/attempt-01/python/P2.py)；[输出](../../../runs/dsv4flash-db-first-full-01/dacomp-030/attempt-01/python/P2.stdout)；[错误](../../../runs/dsv4flash-db-first-full-01/dacomp-030/attempt-01/python/P2.stderr)。检出需人工核验的 SQL 可实现操作：sort_values(；不能仅凭理由判为合规。

P3：Creating a final contract-efficiency chart (sales value generated per CNY of contract signing amount) per outlet type, which quantifies how efficiently each outlet type converts contract investment into sales - a visualization not supported by SQL.

[源码](../../../runs/dsv4flash-db-first-full-01/dacomp-030/attempt-01/python/P3.py)；[输出](../../../runs/dsv4flash-db-first-full-01/dacomp-030/attempt-01/python/P3.stdout)；[错误](../../../runs/dsv4flash-db-first-full-01/dacomp-030/attempt-01/python/P3.stderr)。检出需人工核验的 SQL 可实现操作：sort_values(；不能仅凭理由判为合规。

## 优化机会

有候选待验证/受限或已拒绝。筛选限于精确 SQL、相同自包含 CTE、相同单表完整过滤、可分解单表聚合；未覆盖任意 Join 等价和一般谓词蕴含。全部候选都是 offline，未测在线预测。

| 候选 | 类型 | 已有结果 | 覆盖 SQL | 后续次数 | 中间行数 | 验证 | 成本 |
| --- | --- | --- | --- | --- | --- | --- | --- |
| C1 | aggregate MV | False | ["S11", "S13", "S14", "S15", "S20", "S21"] | 5 | 18 | rejected_result_mismatch | Not benchmarked; correctness alone does not establish net speedup. |


已验证覆盖（含触发查询、候选并集去重）：0/31 条成功数据 SQL。正确性仅针对当前数据库快照；未测性能的候选不能声称已加速。

[完整 build/rewrite 与比较证据](dacomp-030.analysis.json)。

### C1：aggregate MV

Union of grouping keys; decomposable aggregate states; AVG uses SUM and non-NULL COUNT.

原查询 [S11](#s11), [S13](#s13), [S14](#s14), [S15](#s15), [S20](#s20), [S21](#s21) → 新增共享状态 C1 → 后续 5 次可复用。该构建点为事后假设，不代表 Agent 当时预知后续。

构建定义：

```sql
SELECT "Warning Record" AS __g0, "Renewal Likelihood" AS __g1, "Exclusion Flag" AS __g2, " Warning Record" AS __g3, " Exclusion Flag" AS __g4, COUNT(*) AS __a0 FROM "customer_management_table"  GROUP BY "Warning Record", "Renewal Likelihood", "Exclusion Flag", " Warning Record", " Exclusion Flag"
```

受益查询 S11 的改写示例：

```sql
SELECT __g0 AS "Warning Record", SUM(__a0) AS n FROM temp.reuse_candidate GROUP BY __g0 ORDER BY n DESC LIMIT 20
```

| 原 SQL | 列名一致 | 结果一致 | 比较方法 |
| --- | --- | --- | --- |
| S11 | False | True | ordered_numeric_tolerance |
| S13 | False | True | exact_multiset |
| S14 | True | True | exact_multiset |
| S15 | False | True | exact_multiset |
| S20 | True | True | exact_multiset |
| S21 | True | True | exact_multiset |


验证状态：rejected_result_mismatch；成本结论：Not benchmarked; correctness alone does not establish net speedup.

结果依赖：自动记录 SQL→Python 的接口父调用，以及源码中引用归档文件的消费者；字面值相同不认定因果。模型方向选择需要人工读取消息，尚未做全面因果标注。

[原始报告](../../../runs/dsv4flash-db-first-full-01/dacomp-030/attempt-01/answer.md)；[统一消息](../../../runs/dsv4flash-db-first-full-01/dacomp-030/attempt-01/messages.jsonl)；[原始 OpenCode 事件](../../../runs/dsv4flash-db-first-full-01/dacomp-030/attempt-01/opencode.jsonl)；[SQL 引擎日志](../../../runs/dsv4flash-db-first-full-01/dacomp-030/attempt-01/sql_journal.jsonl)。

[可读报告（本地图片链接规范化）](../answers/dacomp-030.md)。原始回答保留，分析结论未改写。

## S1

类别 `connection_setup`；来源 `connection`；调用 `c09219e5143c49249b9db50ab51e38e1`；状态 `success`。

```sql
PRAGMA query_only=ON
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-030/attempt-01/sql/S1.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-030/attempt-01/sql/S1.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-030/attempt-01/results/S1.rows.jsonl)；完整：True；SHA256：`e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`。

## S2

类别 `metadata`；来源 `list_db`；调用 `c09219e5143c49249b9db50ab51e38e1`；状态 `success`。

```sql
SELECT name,sql FROM sqlite_master WHERE type='table' ORDER BY name
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-030/attempt-01/sql/S2.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-030/attempt-01/sql/S2.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-030/attempt-01/results/S2.rows.jsonl)；完整：True；SHA256：`4ff7e76a6a408694c727e4a7aafb948a105f0decd898a8801d007658a903ab4c`。

## S3

类别 `metadata`；来源 `query_db`；调用 `b81c9afbb57e40dc94c37bee8a601b85`；状态 `success`。

```sql
SELECT name FROM sqlite_master WHERE type='table' ORDER BY name
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-030/attempt-01/sql/S3.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-030/attempt-01/sql/S3.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-030/attempt-01/results/S3.rows.jsonl)；完整：True；SHA256：`4c099b84ea3511a6227369106f82c178c595251d64182b33319950364838a6a0`。

## S4

类别 `data`；来源 `query_db`；调用 `a344effe797d4b7cadabf84644b27bd7`；状态 `success`。

```sql
SELECT * FROM "point_of_sale_(pos)_information" LIMIT 20
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-030/attempt-01/sql/S4.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-030/attempt-01/sql/S4.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-030/attempt-01/results/S4.rows.jsonl)；完整：True；SHA256：`5eafd80ae081d3f4b49b1d2e459839e48ca6b8d2bb3dacf0b76d41175cc8ae54`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "point_of_sale_(pos)_information", "kind": "base", "block": null, "base_tables": ["\"point_of_sale_(pos)_information\""]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |


## S5

类别 `data`；来源 `query_db`；调用 `90d87330c82a48fd97c40fe722827f29`；状态 `success`。

```sql
SELECT * FROM sales_data_table LIMIT 20
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-030/attempt-01/sql/S5.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-030/attempt-01/sql/S5.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-030/attempt-01/results/S5.rows.jsonl)；完整：True；SHA256：`50343a2aab24e8c76d0a42dd376f4b11a97486d5ca539ca0a19be4e9b7c1839c`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "sales_data_table", "kind": "base", "block": null, "base_tables": ["sales_data_table"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |


## S6

类别 `data`；来源 `query_db`；调用 `1011dfc1b6a44ce0a3648169bafc2580`；状态 `success`。

```sql
SELECT * FROM contract_information_table LIMIT 20
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-030/attempt-01/sql/S6.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-030/attempt-01/sql/S6.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-030/attempt-01/results/S6.rows.jsonl)；完整：True；SHA256：`5807865a77ee833955309ba2455f0979826e75dd1b3e7ea932900e8b45d982fb`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "contract_information_table", "kind": "base", "block": null, "base_tables": ["contract_information_table"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |


## S7

类别 `data`；来源 `query_db`；调用 `9093958303754d35a037b12ede529f5a`；状态 `success`。

```sql
SELECT * FROM customer_information_table LIMIT 20
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-030/attempt-01/sql/S7.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-030/attempt-01/sql/S7.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-030/attempt-01/results/S7.rows.jsonl)；完整：True；SHA256：`de201f6d71d23888f25250da3c8ae585a31b55f2ea28873ec1ece101ee3594f4`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "customer_information_table", "kind": "base", "block": null, "base_tables": ["customer_information_table"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |


## S8

类别 `data`；来源 `query_db`；调用 `96adad61790d4798be11e8f80c6394f8`；状态 `success`。

```sql
SELECT "Outlet Type", COUNT(*) AS n_outlets, COUNT(DISTINCT "Outlet ID") AS n_unique FROM "point_of_sale_(pos)_information" GROUP BY "Outlet Type" ORDER BY n_outlets DESC
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-030/attempt-01/sql/S8.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-030/attempt-01/sql/S8.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-030/attempt-01/results/S8.rows.jsonl)；完整：True；SHA256：`056e3f56e892c7abb53400d4a253f8460988a0517612b7488b296ddaf5f378c5`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "point_of_sale_(pos)_information", "kind": "base", "block": null, "base_tables": ["\"point_of_sale_(pos)_information\""]}] | [] | ["\"Outlet Type\""] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |
| B1 | COUNT(DISTINCT "Outlet ID") | [{"table": "\"point_of_sale_(pos)_information\"", "column": "Outlet ID"}] | [] | False |


## S9

类别 `data`；来源 `query_db`；调用 `dd84f9416a8449d8bb32b3b24bed7f0a`；状态 `success`。

```sql
SELECT (SELECT COUNT(*) FROM "point_of_sale_(pos)_information") AS pos, (SELECT COUNT(*) FROM sales_data_table) AS sales, (SELECT COUNT(*) FROM contract_information_table) AS contracts, (SELECT COUNT(*) FROM customer_information_table) AS customers, (SELECT COUNT(*) FROM appeal_record_table) AS appeals, (SELECT COUNT(*) FROM assessment_result_table) AS assessments, (SELECT COUNT(*) FROM customer_management_table) AS mgmt, (SELECT COUNT(*) FROM device_information_table) AS devices
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-030/attempt-01/sql/S9.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-030/attempt-01/sql/S9.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-030/attempt-01/results/S9.rows.jsonl)；完整：True；SHA256：`ac7052752692968f211c6ecbdc7fdab62151f4d63bf52abc0a78f96d39e6cb28`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "point_of_sale_(pos)_information", "kind": "base", "block": null, "base_tables": ["\"point_of_sale_(pos)_information\""]}] | [] | [] |
| B2 | [{"alias": "sales_data_table", "kind": "base", "block": null, "base_tables": ["sales_data_table"]}] | [] | [] |
| B3 | [{"alias": "contract_information_table", "kind": "base", "block": null, "base_tables": ["contract_information_table"]}] | [] | [] |
| B4 | [{"alias": "customer_information_table", "kind": "base", "block": null, "base_tables": ["customer_information_table"]}] | [] | [] |
| B5 | [{"alias": "appeal_record_table", "kind": "base", "block": null, "base_tables": ["appeal_record_table"]}] | [] | [] |
| B6 | [{"alias": "assessment_result_table", "kind": "base", "block": null, "base_tables": ["assessment_result_table"]}] | [] | [] |
| B7 | [{"alias": "customer_management_table", "kind": "base", "block": null, "base_tables": ["customer_management_table"]}] | [] | [] |
| B8 | [{"alias": "device_information_table", "kind": "base", "block": null, "base_tables": ["device_information_table"]}] | [] | [] |
| B9 | [] | [] | [] |


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


## S10

类别 `data`；来源 `query_db`；调用 `1d40c8042b394711a98e7ca96625fe75`；状态 `success`。

```sql
SELECT * FROM appeal_record_table LIMIT 10
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-030/attempt-01/sql/S10.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-030/attempt-01/sql/S10.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-030/attempt-01/results/S10.rows.jsonl)；完整：True；SHA256：`e0598648bd345664403cc838f52a32f6271d16e37149b32f289b8dc3229d9420`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "appeal_record_table", "kind": "base", "block": null, "base_tables": ["appeal_record_table"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |


## S11

类别 `data`；来源 `query_db`；调用 `30080060a3c3495ab912019ca2f8a3d0`；状态 `success`。

```sql
SELECT "Warning Record", COUNT(*) AS n FROM customer_management_table GROUP BY "Warning Record" ORDER BY n DESC LIMIT 20
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-030/attempt-01/sql/S11.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-030/attempt-01/sql/S11.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-030/attempt-01/results/S11.rows.jsonl)；完整：True；SHA256：`f65411bfc9ed37f298eb12a441e3ef10fefd794265af70fbf6ecfc3d4f84234f`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "customer_management_table", "kind": "base", "block": null, "base_tables": ["customer_management_table"]}] | [] | ["\"Warning Record\""] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |


未解析列血缘：[{"block": "B1", "column": "\"Warning Record\"", "reason": "ambiguous_or_missing_source"}, {"block": "B1", "column": "\"Warning Record\"", "reason": "ambiguous_or_missing_source"}, {"block": "B1", "column": "\"Warning Record\"", "reason": "ambiguous_or_missing_source"}]

## S12

类别 `data`；来源 `query_db`；调用 `f3b2067ed67a45bb8b6b372429ac18cc`；状态 `success`。

```sql
SELECT * FROM customer_management_table LIMIT 10
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-030/attempt-01/sql/S12.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-030/attempt-01/sql/S12.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-030/attempt-01/results/S12.rows.jsonl)；完整：True；SHA256：`4313748c144fb766b60329348d2ee85e42a238507639e508cbd540ba628bb4bf`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "customer_management_table", "kind": "base", "block": null, "base_tables": ["customer_management_table"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |


## S13

类别 `data`；来源 `query_db`；调用 `7b26be93adb94dd2be79edab76a21e6f`；状态 `success`。

```sql
SELECT "Warning Record", COUNT(*) n FROM customer_management_table GROUP BY "Warning Record"
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-030/attempt-01/sql/S13.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-030/attempt-01/sql/S13.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-030/attempt-01/results/S13.rows.jsonl)；完整：True；SHA256：`f65411bfc9ed37f298eb12a441e3ef10fefd794265af70fbf6ecfc3d4f84234f`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "customer_management_table", "kind": "base", "block": null, "base_tables": ["customer_management_table"]}] | [] | ["\"Warning Record\""] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |


未解析列血缘：[{"block": "B1", "column": "\"Warning Record\"", "reason": "ambiguous_or_missing_source"}, {"block": "B1", "column": "\"Warning Record\"", "reason": "ambiguous_or_missing_source"}, {"block": "B1", "column": "\"Warning Record\"", "reason": "ambiguous_or_missing_source"}]

## S14

类别 `data`；来源 `query_db`；调用 `3f14c491c6c84cddbaa4fcdc6b2b650a`；状态 `success`。

```sql
SELECT "Renewal Likelihood", COUNT(*) n FROM customer_management_table GROUP BY "Renewal Likelihood"
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-030/attempt-01/sql/S14.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-030/attempt-01/sql/S14.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-030/attempt-01/results/S14.rows.jsonl)；完整：True；SHA256：`9cf6402381f09e96d7a2c5f6a4d032e2b7ae0bff2a9db20809dedcb3cd39df47`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "customer_management_table", "kind": "base", "block": null, "base_tables": ["customer_management_table"]}] | [] | ["\"Renewal Likelihood\""] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |


## S15

类别 `data`；来源 `query_db`；调用 `3ef084535f1e47d68240c2fd67e733e7`；状态 `success`。

```sql
SELECT "Exclusion Flag", COUNT(*) n FROM customer_management_table GROUP BY "Exclusion Flag"
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-030/attempt-01/sql/S15.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-030/attempt-01/sql/S15.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-030/attempt-01/results/S15.rows.jsonl)；完整：True；SHA256：`faa4ab8a5a07acbeaf73531f6214deee2995b98ad6dab0126e16f456c0df76c4`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "customer_management_table", "kind": "base", "block": null, "base_tables": ["customer_management_table"]}] | [] | ["\"Exclusion Flag\""] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |


未解析列血缘：[{"block": "B1", "column": "\"Exclusion Flag\"", "reason": "ambiguous_or_missing_source"}, {"block": "B1", "column": "\"Exclusion Flag\"", "reason": "ambiguous_or_missing_source"}, {"block": "B1", "column": "\"Exclusion Flag\"", "reason": "ambiguous_or_missing_source"}]

## S16

类别 `data`；来源 `query_db`；调用 `fb99191456b4485caf8c2c3f1ae00660`；状态 `success`。

```sql
SELECT "Contract Status", COUNT(*) n FROM customer_information_table GROUP BY "Contract Status"
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-030/attempt-01/sql/S16.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-030/attempt-01/sql/S16.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-030/attempt-01/results/S16.rows.jsonl)；完整：True；SHA256：`a815e91475c5cb286505360afdabbe62d9edbbd4c28ea0092348e132e3641491`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "customer_information_table", "kind": "base", "block": null, "base_tables": ["customer_information_table"]}] | [] | ["\"Contract Status\""] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |


## S17

类别 `data`；来源 `query_db`；调用 `2ed31eeb058944779111d5f55dca730f`；状态 `success`。

```sql
SELECT "Data Status", COUNT(*) n FROM sales_data_table GROUP BY "Data Status"
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-030/attempt-01/sql/S17.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-030/attempt-01/sql/S17.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-030/attempt-01/results/S17.rows.jsonl)；完整：True；SHA256：`4ef2fd73b93f847f88590e2ff1b17a897e62c35dae119acce8e539e61c5ee3e9`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "sales_data_table", "kind": "base", "block": null, "base_tables": ["sales_data_table"]}] | [] | ["\"Data Status\""] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |


## S18

类别 `metadata`；来源 `query_db`；调用 `2dfbe45bb41349cd87030d05447bda6f`；状态 `success`。

```sql
PRAGMA table_info(customer_management_table)
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-030/attempt-01/sql/S18.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-030/attempt-01/sql/S18.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-030/attempt-01/results/S18.rows.jsonl)；完整：True；SHA256：`fbf01b9f2c08bd2498900886f9fd12d44341a6d3a3906df2c1382b3f4d36c2ee`。

## S19

类别 `metadata`；来源 `query_db`；调用 `cd6da7f8dde248188c74680b6eb849b9`；状态 `success`。

```sql
PRAGMA table_info("point_of_sale_(pos)_information")
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-030/attempt-01/sql/S19.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-030/attempt-01/sql/S19.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-030/attempt-01/results/S19.rows.jsonl)；完整：True；SHA256：`1ce01c950f12bbcc5a47050c5e0471401cfa2afd4c8fb67b6692adb48f01d9ec`。

## S20

类别 `data`；来源 `query_db`；调用 `96feb378c7e54befa2d7877b0b11e911`；状态 `success`。

```sql
SELECT " Warning Record" AS warning, COUNT(*) n FROM customer_management_table GROUP BY warning
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-030/attempt-01/sql/S20.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-030/attempt-01/sql/S20.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-030/attempt-01/results/S20.rows.jsonl)；完整：True；SHA256：`2701abc76f1c927906c6dbd01c7120179a12c0ba27ffff4c00e7053ab9548e76`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "customer_management_table", "kind": "base", "block": null, "base_tables": ["customer_management_table"]}] | [] | ["\" Warning Record\""] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |


## S21

类别 `data`；来源 `query_db`；调用 `d791bd8fcae74bd3a1464ca4abcea3ad`；状态 `success`。

```sql
SELECT " Exclusion Flag" AS flag, COUNT(*) n FROM customer_management_table GROUP BY flag
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-030/attempt-01/sql/S21.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-030/attempt-01/sql/S21.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-030/attempt-01/results/S21.rows.jsonl)；完整：True；SHA256：`ba730e9c39fd57ec365a0b3f3cbe3a99b278278fb90e0f5680cbfd2b56175ac8`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "customer_management_table", "kind": "base", "block": null, "base_tables": ["customer_management_table"]}] | [] | ["\" Exclusion Flag\""] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |


## S22

类别 `data`；来源 `query_db`；调用 `779b9a96f6ed4a83b1de99eb8ea2ffc8`；状态 `failed`。

```sql
SELECT p."Outlet Type",
  COUNT(DISTINCT p."Outlet ID") AS num_outlets,
  -- Sales targets and actuals
  ROUND(AVG(p."Actual Sales (cases)"), 1) AS avg_actual_sales,
  ROUND(AVG(p."Sales Target"), 1) AS avg_sales_target,
  ROUND(SUM(p."Actual Sales (cases)") * 1.0 / NULLIF(SUM(p."Sales Target"), 0), 4) AS sales_target_achievement_pct,
  ROUND(AVG(p."VPO Value"), 2) AS avg_vpo,
  ROUND(AVG(p."PC Value"), 1) AS avg_pc_value,
  -- Sales data metrics
  ROUND(AVG(s."Target Achievement Rate"), 4) AS avg_target_achievement_rate,
  ROUND(AVG(s."Sales Volume (Units)"), 1) AS avg_sales_volume,
  ROUND(AVG(s."Sales (Value)"), 1) AS avg_sales_value,
  ROUND(SUM(s."Sales Volume (Units)"), 0) AS total_sales_volume,
  ROUND(SUM(s."Sales (Value)"), 0) AS total_sales_value,
  ROUND(AVG(s."YoY Growth Rate"), 2) AS avg_yoy_growth,
  ROUND(AVG(s."MoM Growth Rate"), 2) AS avg_mom_growth
FROM "point_of_sale_(pos)_information" p
LEFT JOIN sales_data_table s ON p."Customer ID" = s."Customer ID" AND s."Data Status" = 'Valid'
GROUP BY p."Outlet Type"
ORDER BY num_outlets DESC
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-030/attempt-01/sql/S22.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-030/attempt-01/sql/S22.parameters.json)。

错误：`OperationalError('no such column: s.Target Achievement Rate')`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "p", "kind": "base", "block": null, "base_tables": ["\"point_of_sale_(pos)_information\""]}, {"alias": "s", "kind": "base", "block": null, "base_tables": ["sales_data_table"]}] | [{"type": "LEFT", "right": "sales_data_table AS s", "on": "p.\"Customer ID\" = s.\"Customer ID\" AND s.\"Data Status\" = 'Valid'", "using": []}] | ["p.\"Outlet Type\""] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(DISTINCT p."Outlet ID") | [{"table": "\"point_of_sale_(pos)_information\"", "column": "Outlet ID"}] | [] | False |
| B1 | AVG(p."Actual Sales (cases)") | [{"table": "\"point_of_sale_(pos)_information\"", "column": "Actual Sales (cases)"}] | [] | False |
| B1 | AVG(p."Sales Target") | [{"table": "\"point_of_sale_(pos)_information\"", "column": "Sales Target"}] | [] | False |
| B1 | AVG(p."VPO Value") | [{"table": "\"point_of_sale_(pos)_information\"", "column": "VPO Value"}] | [] | False |
| B1 | AVG(p."PC Value") | [{"table": "\"point_of_sale_(pos)_information\"", "column": "PC Value"}] | [] | False |
| B1 | AVG(s."Target Achievement Rate") | [{"table": "sales_data_table", "column": "Target Achievement Rate"}] | [] | False |
| B1 | AVG(s."Sales Volume (Units)") | [{"table": "sales_data_table", "column": "Sales Volume (Units)"}] | [] | False |
| B1 | AVG(s."Sales (Value)") | [{"table": "sales_data_table", "column": "Sales (Value)"}] | [] | False |
| B1 | SUM(s."Sales Volume (Units)") | [{"table": "sales_data_table", "column": "Sales Volume (Units)"}] | [] | False |
| B1 | SUM(s."Sales (Value)") | [{"table": "sales_data_table", "column": "Sales (Value)"}] | [] | False |
| B1 | AVG(s."YoY Growth Rate") | [{"table": "sales_data_table", "column": "YoY Growth Rate"}] | [] | False |
| B1 | AVG(s."MoM Growth Rate") | [{"table": "sales_data_table", "column": "MoM Growth Rate"}] | [] | False |
| B1 | SUM(p."Actual Sales (cases)") | [{"table": "\"point_of_sale_(pos)_information\"", "column": "Actual Sales (cases)"}] | [] | False |
| B1 | SUM(p."Sales Target") | [{"table": "\"point_of_sale_(pos)_information\"", "column": "Sales Target"}] | [] | False |


## S23

类别 `metadata`；来源 `query_db`；调用 `6076d45154ec4e2e920952a2b66a9cd7`；状态 `success`。

```sql
PRAGMA table_info(sales_data_table)
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-030/attempt-01/sql/S23.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-030/attempt-01/sql/S23.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-030/attempt-01/results/S23.rows.jsonl)；完整：True；SHA256：`c2ae064518aef99eea4253ab1888150d94aaf41f219ac111303acff735de47e0`。

## S24

类别 `data`；来源 `query_db`；调用 `d5c487173eeb4dc5aafe7ed425f8e30e`；状态 `success`。

```sql
SELECT p."Outlet Type",
  COUNT(DISTINCT p."Outlet ID") AS num_outlets,
  -- Sales targets and actuals
  ROUND(AVG(p."Actual Sales (cases)"), 1) AS avg_actual_sales,
  ROUND(AVG(p."Sales Target"), 1) AS avg_sales_target,
  ROUND(SUM(p."Actual Sales (cases)") * 1.0 / NULLIF(SUM(p."Sales Target"), 0), 4) AS sales_target_achievement_pct,
  ROUND(AVG(p."VPO Value"), 2) AS avg_vpo,
  ROUND(AVG(p."PC Value"), 1) AS avg_pc_value,
  -- Sales data metrics
  ROUND(AVG(s." Target Achievement Rate"), 4) AS avg_target_achievement_rate,
  ROUND(AVG(s."Sales Volume (Units)"), 1) AS avg_sales_volume,
  ROUND(AVG(s."Sales (Value)"), 1) AS avg_sales_value,
  ROUND(SUM(s."Sales Volume (Units)"), 0) AS total_sales_volume,
  ROUND(SUM(s."Sales (Value)"), 0) AS total_sales_value,
  ROUND(AVG(s." YoY Growth Rate"), 2) AS avg_yoy_growth,
  ROUND(AVG(s."MoM Growth Rate"), 2) AS avg_mom_growth
FROM "point_of_sale_(pos)_information" p
LEFT JOIN sales_data_table s ON p."Customer ID" = s."Customer ID" AND s."Data Status" = 'Valid'
GROUP BY p."Outlet Type"
ORDER BY num_outlets DESC
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-030/attempt-01/sql/S24.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-030/attempt-01/sql/S24.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-030/attempt-01/results/S24.rows.jsonl)；完整：True；SHA256：`c4997fd1cc20291d0d2cb7af1483be38a8a6a3f855e20181f0fc38367e64b601`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "p", "kind": "base", "block": null, "base_tables": ["\"point_of_sale_(pos)_information\""]}, {"alias": "s", "kind": "base", "block": null, "base_tables": ["sales_data_table"]}] | [{"type": "LEFT", "right": "sales_data_table AS s", "on": "p.\"Customer ID\" = s.\"Customer ID\" AND s.\"Data Status\" = 'Valid'", "using": []}] | ["p.\"Outlet Type\""] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(DISTINCT p."Outlet ID") | [{"table": "\"point_of_sale_(pos)_information\"", "column": "Outlet ID"}] | [] | False |
| B1 | AVG(p."Actual Sales (cases)") | [{"table": "\"point_of_sale_(pos)_information\"", "column": "Actual Sales (cases)"}] | [] | False |
| B1 | AVG(p."Sales Target") | [{"table": "\"point_of_sale_(pos)_information\"", "column": "Sales Target"}] | [] | False |
| B1 | AVG(p."VPO Value") | [{"table": "\"point_of_sale_(pos)_information\"", "column": "VPO Value"}] | [] | False |
| B1 | AVG(p."PC Value") | [{"table": "\"point_of_sale_(pos)_information\"", "column": "PC Value"}] | [] | False |
| B1 | AVG(s." Target Achievement Rate") | [{"table": "sales_data_table", "column": " Target Achievement Rate"}] | [] | False |
| B1 | AVG(s."Sales Volume (Units)") | [{"table": "sales_data_table", "column": "Sales Volume (Units)"}] | [] | False |
| B1 | AVG(s."Sales (Value)") | [{"table": "sales_data_table", "column": "Sales (Value)"}] | [] | False |
| B1 | SUM(s."Sales Volume (Units)") | [{"table": "sales_data_table", "column": "Sales Volume (Units)"}] | [] | False |
| B1 | SUM(s."Sales (Value)") | [{"table": "sales_data_table", "column": "Sales (Value)"}] | [] | False |
| B1 | AVG(s." YoY Growth Rate") | [{"table": "sales_data_table", "column": " YoY Growth Rate"}] | [] | False |
| B1 | AVG(s."MoM Growth Rate") | [{"table": "sales_data_table", "column": "MoM Growth Rate"}] | [] | False |
| B1 | SUM(p."Actual Sales (cases)") | [{"table": "\"point_of_sale_(pos)_information\"", "column": "Actual Sales (cases)"}] | [] | False |
| B1 | SUM(p."Sales Target") | [{"table": "\"point_of_sale_(pos)_information\"", "column": "Sales Target"}] | [] | False |


## S25

类别 `data`；来源 `query_db`；调用 `4ebeb7bd1ba5429e92d4cbc5f5210ec1`；状态 `success`。

```sql
SELECT p."Outlet Type",
  COUNT(c."Agreement ID") AS num_contracts,
  COUNT(DISTINCT p."Outlet ID") AS num_outlets,
  ROUND(COUNT(c."Agreement ID") * 1.0 / COUNT(DISTINCT p."Outlet ID"), 2) AS contracts_per_outlet,
  ROUND(AVG(c."Signing Amount (CNY)"), 1) AS avg_signing_amount,
  ROUND(SUM(c."Signing Amount (CNY)"), 0) AS total_signing_amount,
  ROUND(AVG(c."Same-store Ratio"), 3) AS avg_same_store_ratio,
  SUM(CASE WHEN c."Renewal Flag" = 'Yes' THEN 1 ELSE 0 END) AS renewal_cnt,
  ROUND(AVG(CASE WHEN c."Renewal Flag" = 'Yes' THEN 1.0 ELSE 0 END), 3) AS renewal_ratio
FROM "point_of_sale_(pos)_information" p
LEFT JOIN contract_information_table c ON p."Outlet ID" = c."Outlet ID"
GROUP BY p."Outlet Type"
ORDER BY num_contracts DESC
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-030/attempt-01/sql/S25.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-030/attempt-01/sql/S25.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-030/attempt-01/results/S25.rows.jsonl)；完整：True；SHA256：`eb94f00e54097b17145fc5e50167ca4445c2d7ca91636837d281358900738ba1`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "p", "kind": "base", "block": null, "base_tables": ["\"point_of_sale_(pos)_information\""]}, {"alias": "c", "kind": "base", "block": null, "base_tables": ["contract_information_table"]}] | [{"type": "LEFT", "right": "contract_information_table AS c", "on": "p.\"Outlet ID\" = c.\"Outlet ID\"", "using": []}] | ["p.\"Outlet Type\""] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(c."Agreement ID") | [{"table": "contract_information_table", "column": "Agreement ID"}] | [] | False |
| B1 | COUNT(DISTINCT p."Outlet ID") | [{"table": "\"point_of_sale_(pos)_information\"", "column": "Outlet ID"}] | [] | False |
| B1 | SUM(CASE WHEN c."Renewal Flag" = 'Yes' THEN 1 ELSE 0 END) | [] | [{"table": "contract_information_table", "column": "Renewal Flag"}] | False |
| B1 | AVG(c."Signing Amount (CNY)") | [{"table": "contract_information_table", "column": "Signing Amount (CNY)"}] | [] | False |
| B1 | SUM(c."Signing Amount (CNY)") | [{"table": "contract_information_table", "column": "Signing Amount (CNY)"}] | [] | False |
| B1 | AVG(c."Same-store Ratio") | [{"table": "contract_information_table", "column": "Same-store Ratio"}] | [] | False |
| B1 | AVG(CASE WHEN c."Renewal Flag" = 'Yes' THEN 1.0 ELSE 0 END) | [] | [{"table": "contract_information_table", "column": "Renewal Flag"}] | False |
| B1 | COUNT(DISTINCT p."Outlet ID") | [{"table": "\"point_of_sale_(pos)_information\"", "column": "Outlet ID"}] | [] | False |
| B1 | COUNT(c."Agreement ID") | [{"table": "contract_information_table", "column": "Agreement ID"}] | [] | False |


## S26

类别 `data`；来源 `query_db`；调用 `9b97b4d5e4ec4a8b99d10fc832af46dd`；状态 `success`。

```sql
SELECT p."Outlet Type",
  COUNT(cm."Management ID") AS mgmt_records,
  SUM(CASE WHEN cm." Warning Record" = 'Complaint Record' THEN 1 ELSE 0 END) AS complaint_cnt,
  SUM(CASE WHEN cm." Warning Record" = 'Quality Issue' THEN 1 ELSE 0 END) AS quality_cnt,
  ROUND(SUM(CASE WHEN cm." Warning Record" = 'Complaint Record' THEN 1 ELSE 0 END) * 1.0 / COUNT(cm."Management ID"), 3) AS complaint_ratio,
  SUM(CASE WHEN cm."Renewal Likelihood" = 'High' THEN 1 ELSE 0 END) AS renew_high,
  SUM(CASE WHEN cm."Renewal Likelihood" = 'Low' THEN 1 ELSE 0 END) AS renew_low,
  ROUND(AVG(cm."Training Count"), 2) AS avg_training
FROM "point_of_sale_(pos)_information" p
LEFT JOIN customer_management_table cm ON p."Customer ID" = cm."Customer ID"
GROUP BY p."Outlet Type"
ORDER BY complaint_ratio DESC
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-030/attempt-01/sql/S26.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-030/attempt-01/sql/S26.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-030/attempt-01/results/S26.rows.jsonl)；完整：True；SHA256：`035bbb0f5d3ab560eff7c1376c881eef035a2413e66e19ef0aee9353272f80bd`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "p", "kind": "base", "block": null, "base_tables": ["\"point_of_sale_(pos)_information\""]}, {"alias": "cm", "kind": "base", "block": null, "base_tables": ["customer_management_table"]}] | [{"type": "LEFT", "right": "customer_management_table AS cm", "on": "p.\"Customer ID\" = cm.\"Customer ID\"", "using": []}] | ["p.\"Outlet Type\""] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(cm."Management ID") | [{"table": "customer_management_table", "column": "Management ID"}] | [] | False |
| B1 | SUM(CASE WHEN cm." Warning Record" = 'Complaint Record' THEN 1 ELSE 0 END) | [] | [{"table": "customer_management_table", "column": " Warning Record"}] | False |
| B1 | SUM(CASE WHEN cm." Warning Record" = 'Quality Issue' THEN 1 ELSE 0 END) | [] | [{"table": "customer_management_table", "column": " Warning Record"}] | False |
| B1 | SUM(CASE WHEN cm."Renewal Likelihood" = 'High' THEN 1 ELSE 0 END) | [] | [{"table": "customer_management_table", "column": "Renewal Likelihood"}] | False |
| B1 | SUM(CASE WHEN cm."Renewal Likelihood" = 'Low' THEN 1 ELSE 0 END) | [] | [{"table": "customer_management_table", "column": "Renewal Likelihood"}] | False |
| B1 | AVG(cm."Training Count") | [{"table": "customer_management_table", "column": "Training Count"}] | [] | False |
| B1 | COUNT(cm."Management ID") | [{"table": "customer_management_table", "column": "Management ID"}] | [] | False |
| B1 | SUM(CASE WHEN cm." Warning Record" = 'Complaint Record' THEN 1 ELSE 0 END) | [] | [{"table": "customer_management_table", "column": " Warning Record"}] | False |


## S27

类别 `data`；来源 `query_db`；调用 `49cc10a4b2a74106b101bc88cd13c336`；状态 `success`。

```sql
SELECT p."Outlet Type",
  COUNT(a."Assessment ID") AS n_assessments,
  ROUND(AVG(a."Score"), 2) AS avg_score,
  ROUND(AVG(a."Assessment pass rate"), 4) AS avg_pass_rate,
  ROUND(AVG(a."Historical pass trend (%)"), 2) AS avg_hist_pass_trend,
  ROUND(AVG(a."Photo upload count"), 2) AS avg_photo_upload,
  ROUND(AVG(a."Qualified photo count"), 2) AS avg_qualified_photo,
  ROUND(AVG(a."Qualified photo count" * 1.0 / NULLIF(a."Photo upload count", 0)), 4) AS photo_qual_rate
FROM "point_of_sale_(pos)_information" p
LEFT JOIN assessment_result_table a ON p."Outlet ID" = a."Outlet ID"
GROUP BY p."Outlet Type"
ORDER BY avg_pass_rate
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-030/attempt-01/sql/S27.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-030/attempt-01/sql/S27.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-030/attempt-01/results/S27.rows.jsonl)；完整：True；SHA256：`ad42d379b736b7e1501cc45e3c334f359e85a374093024baac92919ec31acbd9`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "p", "kind": "base", "block": null, "base_tables": ["\"point_of_sale_(pos)_information\""]}, {"alias": "a", "kind": "base", "block": null, "base_tables": ["assessment_result_table"]}] | [{"type": "LEFT", "right": "assessment_result_table AS a", "on": "p.\"Outlet ID\" = a.\"Outlet ID\"", "using": []}] | ["p.\"Outlet Type\""] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(a."Assessment ID") | [{"table": "assessment_result_table", "column": "Assessment ID"}] | [] | False |
| B1 | AVG(a."Score") | [{"table": "assessment_result_table", "column": "Score"}] | [] | False |
| B1 | AVG(a."Assessment pass rate") | [{"table": "assessment_result_table", "column": "Assessment pass rate"}] | [] | False |
| B1 | AVG(a."Historical pass trend (%)") | [{"table": "assessment_result_table", "column": "Historical pass trend (%)"}] | [] | False |
| B1 | AVG(a."Photo upload count") | [{"table": "assessment_result_table", "column": "Photo upload count"}] | [] | False |
| B1 | AVG(a."Qualified photo count") | [{"table": "assessment_result_table", "column": "Qualified photo count"}] | [] | False |
| B1 | AVG(a."Qualified photo count" * 1.0 / NULLIF(a."Photo upload count", 0)) | [{"table": "assessment_result_table", "column": "Qualified photo count"}, {"table": "assessment_result_table", "column": "Photo upload count"}] | [] | False |


## S28

类别 `data`；来源 `query_db`；调用 `406343eaaac841febaf6f72efde3f575`；状态 `success`。

```sql
SELECT p."Outlet Type",
  COUNT(ap."Appeal ID") AS n_appeals,
  SUM(CASE WHEN ap."Handling Status" = 'Completed' THEN 1 ELSE 0 END) AS completed_appeals,
  SUM(CASE WHEN ap."Processing Result" = 'Modify score' THEN 1 ELSE 0 END) AS modified_scores,
  ROUND(COUNT(ap."Appeal ID") * 1.0 / COUNT(DISTINCT p."Outlet ID"), 2) AS appeals_per_outlet
FROM "point_of_sale_(pos)_information" p
LEFT JOIN appeal_record_table ap ON p."Outlet ID" = ap."Outlet ID"
GROUP BY p."Outlet Type"
ORDER BY n_appeals DESC
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-030/attempt-01/sql/S28.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-030/attempt-01/sql/S28.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-030/attempt-01/results/S28.rows.jsonl)；完整：True；SHA256：`893673b0d61be34cb00c676064a826b6b8e7563a7f81b3008077dd0969fca180`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "p", "kind": "base", "block": null, "base_tables": ["\"point_of_sale_(pos)_information\""]}, {"alias": "ap", "kind": "base", "block": null, "base_tables": ["appeal_record_table"]}] | [{"type": "LEFT", "right": "appeal_record_table AS ap", "on": "p.\"Outlet ID\" = ap.\"Outlet ID\"", "using": []}] | ["p.\"Outlet Type\""] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(ap."Appeal ID") | [{"table": "appeal_record_table", "column": "Appeal ID"}] | [] | False |
| B1 | SUM(CASE WHEN ap."Handling Status" = 'Completed' THEN 1 ELSE 0 END) | [] | [{"table": "appeal_record_table", "column": "Handling Status"}] | False |
| B1 | SUM(CASE WHEN ap."Processing Result" = 'Modify score' THEN 1 ELSE 0 END) | [] | [{"table": "appeal_record_table", "column": "Processing Result"}] | False |
| B1 | COUNT(DISTINCT p."Outlet ID") | [{"table": "\"point_of_sale_(pos)_information\"", "column": "Outlet ID"}] | [] | False |
| B1 | COUNT(ap."Appeal ID") | [{"table": "appeal_record_table", "column": "Appeal ID"}] | [] | False |


## S29

类别 `data`；来源 `query_db`；调用 `d2e95488897d43b8b74bef4610b83395`；状态 `success`。

```sql
SELECT p."Outlet Type",
  COUNT(DISTINCT p."Customer ID") AS n_customers,
  ROUND(AVG(ci."Sales History"), 1) AS avg_sales_history,
  SUM(CASE WHEN ci."Customer Level" = 'A' THEN 1 ELSE 0 END) AS level_A,
  SUM(CASE WHEN ci."Customer Level" = 'B' THEN 1 ELSE 0 END) AS level_B,
  SUM(CASE WHEN ci."Customer Level" = 'C' THEN 1 ELSE 0 END) AS level_C,
  SUM(CASE WHEN ci."Customer Level" = 'D' THEN 1 ELSE 0 END) AS level_D
FROM "point_of_sale_(pos)_information" p
LEFT JOIN customer_information_table ci ON p."Customer ID" = ci."Customer ID"
GROUP BY p."Outlet Type"
ORDER BY n_customers DESC
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-030/attempt-01/sql/S29.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-030/attempt-01/sql/S29.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-030/attempt-01/results/S29.rows.jsonl)；完整：True；SHA256：`29f2b56da837a5cb8190faf5de206cea7bc556ddb353b2f0a2c4febfcfcbeb11`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "p", "kind": "base", "block": null, "base_tables": ["\"point_of_sale_(pos)_information\""]}, {"alias": "ci", "kind": "base", "block": null, "base_tables": ["customer_information_table"]}] | [{"type": "LEFT", "right": "customer_information_table AS ci", "on": "p.\"Customer ID\" = ci.\"Customer ID\"", "using": []}] | ["p.\"Outlet Type\""] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(DISTINCT p."Customer ID") | [{"table": "\"point_of_sale_(pos)_information\"", "column": "Customer ID"}] | [] | False |
| B1 | SUM(CASE WHEN ci."Customer Level" = 'A' THEN 1 ELSE 0 END) | [] | [{"table": "customer_information_table", "column": "Customer Level"}] | False |
| B1 | SUM(CASE WHEN ci."Customer Level" = 'B' THEN 1 ELSE 0 END) | [] | [{"table": "customer_information_table", "column": "Customer Level"}] | False |
| B1 | SUM(CASE WHEN ci."Customer Level" = 'C' THEN 1 ELSE 0 END) | [] | [{"table": "customer_information_table", "column": "Customer Level"}] | False |
| B1 | SUM(CASE WHEN ci."Customer Level" = 'D' THEN 1 ELSE 0 END) | [] | [{"table": "customer_information_table", "column": "Customer Level"}] | False |
| B1 | AVG(ci."Sales History") | [{"table": "customer_information_table", "column": "Sales History"}] | [] | False |


## S30

类别 `data`；来源 `query_db`；调用 `97fad17cbcfb4e27a19a97ec841ca232`；状态 `success`。

```sql
SELECT p."Outlet Type",
  c."Signing Type (GSB/Spark)" AS signing_type,
  COUNT(*) AS n_contracts,
  ROUND(AVG(c."Signing Amount (CNY)"), 1) AS avg_amt
FROM "point_of_sale_(pos)_information" p
JOIN contract_information_table c ON p."Outlet ID" = c."Outlet ID"
GROUP BY p."Outlet Type", signing_type
ORDER BY p."Outlet Type", signing_type
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-030/attempt-01/sql/S30.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-030/attempt-01/sql/S30.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-030/attempt-01/results/S30.rows.jsonl)；完整：True；SHA256：`ceee1299f6a51800e2eee09bd9cf8956316e982f87446e882a9e7411fb2c6dc8`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "p", "kind": "base", "block": null, "base_tables": ["\"point_of_sale_(pos)_information\""]}, {"alias": "c", "kind": "base", "block": null, "base_tables": ["contract_information_table"]}] | [{"type": "INNER", "right": "contract_information_table AS c", "on": "p.\"Outlet ID\" = c.\"Outlet ID\"", "using": []}] | ["p.\"Outlet Type\"", "c.\"Signing Type (GSB/Spark)\""] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |
| B1 | AVG(c."Signing Amount (CNY)") | [{"table": "contract_information_table", "column": "Signing Amount (CNY)"}] | [] | False |


## S31

类别 `data`；来源 `query_db`；调用 `dbdcbd69e25348bc870e5df5b5018815`；状态 `success`。

```sql
SELECT p."Outlet Type",
  COUNT(d."Equipment record code") AS n_devices,
  SUM(d."Number of failures") AS total_failures,
  ROUND(AVG(d."Number of failures"), 2) AS avg_failures
FROM "point_of_sale_(pos)_information" p
LEFT JOIN device_information_table d ON p."Outlet ID" = d."Outlet ID"
GROUP BY p."Outlet Type"
ORDER BY avg_failures DESC
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-030/attempt-01/sql/S31.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-030/attempt-01/sql/S31.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-030/attempt-01/results/S31.rows.jsonl)；完整：True；SHA256：`b51674875023cc603d339f5ea1344f4d0be5474ae04313b1c26807840ad5b184`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "p", "kind": "base", "block": null, "base_tables": ["\"point_of_sale_(pos)_information\""]}, {"alias": "d", "kind": "base", "block": null, "base_tables": ["device_information_table"]}] | [{"type": "LEFT", "right": "device_information_table AS d", "on": "p.\"Outlet ID\" = d.\"Outlet ID\"", "using": []}] | ["p.\"Outlet Type\""] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(d."Equipment record code") | [{"table": "device_information_table", "column": "Equipment record code"}] | [] | False |
| B1 | SUM(d."Number of failures") | [{"table": "device_information_table", "column": "Number of failures"}] | [] | False |
| B1 | AVG(d."Number of failures") | [{"table": "device_information_table", "column": "Number of failures"}] | [] | False |


## S32

类别 `data`；来源 `query_db`；调用 `732db083249d418c89626650db3ac955`；状态 `success`。

```sql
SELECT "Outlet Type",
  CAST(REPLACE("Qualification Rate", '%', '') AS REAL) AS qual_pct
FROM "point_of_sale_(pos)_information"
WHERE "Qualification Rate" IS NOT NULL AND "Qualification Rate" != ''
LIMIT 20
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-030/attempt-01/sql/S32.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-030/attempt-01/sql/S32.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-030/attempt-01/results/S32.rows.jsonl)；完整：True；SHA256：`ebb5c8fd7fff0152ecb5737721aa185ac9ee7740e49ebacec697993d84c2f62c`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "point_of_sale_(pos)_information", "kind": "base", "block": null, "base_tables": ["\"point_of_sale_(pos)_information\""]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |


## S33

类别 `data`；来源 `query_db`；调用 `716131700f7249f9878c7019a8d0b4bc`；状态 `success`。

```sql
WITH pos_agg AS (
  SELECT p."Outlet Type",
    COUNT(DISTINCT p."Outlet ID") AS num_outlets,
    ROUND(SUM(p."Actual Sales (cases)") * 1.0 / NULLIF(SUM(p."Sales Target"), 0), 4) AS pos_target_ach,
    ROUND(AVG(p."VPO Value"), 3) AS avg_vpo,
    ROUND(AVG(p."PC Value"), 1) AS avg_pc,
    ROUND(AVG(CAST(REPLACE(p."Qualification Rate", '%', '') AS REAL)), 2) AS avg_qual_rate
  FROM "point_of_sale_(pos)_information" p
  GROUP BY p."Outlet Type"
),
sales_agg AS (
  SELECT p."Outlet Type",
    ROUND(AVG(s." Target Achievement Rate"), 4) AS avg_tar,
    ROUND(AVG(s." YoY Growth Rate"), 2) AS avg_yoy,
    ROUND(AVG(s."MoM Growth Rate"), 2) AS avg_mom,
    ROUND(SUM(s."Sales (Value)"), 0) AS total_sales_value,
    ROUND(AVG(s."Sales (Value)"), 1) AS avg_sales_value
  FROM "point_of_sale_(pos)_information" p
  JOIN sales_data_table s ON p."Customer ID" = s."Customer ID" AND s."Data Status" = 'Valid'
  GROUP BY p."Outlet Type"
),
contract_agg AS (
  SELECT p."Outlet Type",
    COUNT(c."Agreement ID") AS num_contracts,
    ROUND(SUM(c."Signing Amount (CNY)"), 0) AS total_signing_amount,
    ROUND(AVG(c."Signing Amount (CNY)"), 1) AS avg_signing_amount,
    ROUND(AVG(CASE WHEN c."Renewal Flag" = 'Yes' THEN 1.0 ELSE 0 END), 3) AS renewal_ratio
  FROM "point_of_sale_(pos)_information" p
  LEFT JOIN contract_information_table c ON p."Outlet ID" = c."Outlet ID"
  GROUP BY p."Outlet Type"
),
mgmt_agg AS (
  SELECT p."Outlet Type",
    ROUND(SUM(CASE WHEN cm." Warning Record" = 'Complaint Record' THEN 1 ELSE 0 END) * 1.0 / COUNT(cm."Management ID"), 3) AS complaint_ratio,
    ROUND(SUM(CASE WHEN cm." Warning Record" = 'Quality Issue' THEN 1 ELSE 0 END) * 1.0 / COUNT(cm."Management ID"), 3) AS quality_ratio,
    SUM(CASE WHEN cm."Renewal Likelihood" = 'High' THEN 1 ELSE 0 END) * 1.0 / COUNT(cm."Management ID") AS renew_high_ratio
  FROM "point_of_sale_(pos)_information" p
  LEFT JOIN customer_management_table cm ON p."Customer ID" = cm."Customer ID"
  GROUP BY p."Outlet Type"
),
assess_agg AS (
  SELECT p."Outlet Type",
    ROUND(AVG(a."Assessment pass rate"), 4) AS avg_pass_rate,
    ROUND(AVG(a."Score"), 2) AS avg_score
  FROM "point_of_sale_(pos)_information" p
  LEFT JOIN assessment_result_table a ON p."Outlet ID" = a."Outlet ID"
  GROUP BY p."Outlet Type"
),
appeal_agg AS (
  SELECT p."Outlet Type",
    COUNT(ap."Appeal ID") * 1.0 / COUNT(DISTINCT p."Outlet ID") AS appeals_per_outlet
  FROM "point_of_sale_(pos)_information" p
  LEFT JOIN appeal_record_table ap ON p."Outlet ID" = ap."Outlet ID"
  GROUP BY p."Outlet Type"
)
SELECT pa."Outlet Type", pa.num_outlets, pa.pos_target_ach, pa.avg_vpo, pa.avg_pc, pa.avg_qual_rate,
  sa.avg_tar, sa.avg_yoy, sa.avg_mom, sa.total_sales_value, sa.avg_sales_value,
  ca.num_contracts, ca.total_signing_amount, ca.avg_signing_amount, ca.renewal_ratio,
  ma.complaint_ratio, ma.quality_ratio, ma.renew_high_ratio,
  aa.avg_pass_rate, aa.avg_score, ap.appeals_per_outlet
FROM pos_agg pa
LEFT JOIN sales_agg sa ON pa."Outlet Type" = sa."Outlet Type"
LEFT JOIN contract_agg ca ON pa."Outlet Type" = ca."Outlet Type"
LEFT JOIN mgmt_agg ma ON pa."Outlet Type" = ma."Outlet Type"
LEFT JOIN assess_agg aa ON pa."Outlet Type" = aa."Outlet Type"
LEFT JOIN appeal_agg ap ON pa."Outlet Type" = ap."Outlet Type"
ORDER BY pa.num_outlets DESC
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-030/attempt-01/sql/S33.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-030/attempt-01/sql/S33.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-030/attempt-01/results/S33.rows.jsonl)；完整：True；SHA256：`ba121d3c349358fdb34cf88be10bb943dfb915b27dcb689a27aa7037f359b76b`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "p", "kind": "base", "block": null, "base_tables": ["\"point_of_sale_(pos)_information\""]}] | [] | ["p.\"Outlet Type\""] |
| B2 | [{"alias": "p", "kind": "base", "block": null, "base_tables": ["\"point_of_sale_(pos)_information\""]}, {"alias": "s", "kind": "base", "block": null, "base_tables": ["sales_data_table"]}] | [{"type": "INNER", "right": "sales_data_table AS s", "on": "p.\"Customer ID\" = s.\"Customer ID\" AND s.\"Data Status\" = 'Valid'", "using": []}] | ["p.\"Outlet Type\""] |
| B3 | [{"alias": "p", "kind": "base", "block": null, "base_tables": ["\"point_of_sale_(pos)_information\""]}, {"alias": "c", "kind": "base", "block": null, "base_tables": ["contract_information_table"]}] | [{"type": "LEFT", "right": "contract_information_table AS c", "on": "p.\"Outlet ID\" = c.\"Outlet ID\"", "using": []}] | ["p.\"Outlet Type\""] |
| B4 | [{"alias": "p", "kind": "base", "block": null, "base_tables": ["\"point_of_sale_(pos)_information\""]}, {"alias": "cm", "kind": "base", "block": null, "base_tables": ["customer_management_table"]}] | [{"type": "LEFT", "right": "customer_management_table AS cm", "on": "p.\"Customer ID\" = cm.\"Customer ID\"", "using": []}] | ["p.\"Outlet Type\""] |
| B5 | [{"alias": "p", "kind": "base", "block": null, "base_tables": ["\"point_of_sale_(pos)_information\""]}, {"alias": "a", "kind": "base", "block": null, "base_tables": ["assessment_result_table"]}] | [{"type": "LEFT", "right": "assessment_result_table AS a", "on": "p.\"Outlet ID\" = a.\"Outlet ID\"", "using": []}] | ["p.\"Outlet Type\""] |
| B6 | [{"alias": "p", "kind": "base", "block": null, "base_tables": ["\"point_of_sale_(pos)_information\""]}, {"alias": "ap", "kind": "base", "block": null, "base_tables": ["appeal_record_table"]}] | [{"type": "LEFT", "right": "appeal_record_table AS ap", "on": "p.\"Outlet ID\" = ap.\"Outlet ID\"", "using": []}] | ["p.\"Outlet Type\""] |
| B7 | [{"alias": "pa", "kind": "derived", "block": "B1", "base_tables": ["\"point_of_sale_(pos)_information\""]}, {"alias": "sa", "kind": "derived", "block": "B2", "base_tables": ["\"point_of_sale_(pos)_information\"", "sales_data_table"]}, {"alias": "ca", "kind": "derived", "block": "B3", "base_tables": ["\"point_of_sale_(pos)_information\"", "contract_information_table"]}, {"alias": "ma", "kind": "derived", "block": "B4", "base_tables": ["\"point_of_sale_(pos)_information\"", "customer_management_table"]}, {"alias": "aa", "kind": "derived", "block": "B5", "base_tables": ["\"point_of_sale_(pos)_information\"", "assessment_result_table"]}, {"alias": "ap", "kind": "derived", "block": "B6", "base_tables": ["\"point_of_sale_(pos)_information\"", "appeal_record_table"]}] | [{"type": "LEFT", "right": "sales_agg AS sa", "on": "pa.\"Outlet Type\" = sa.\"Outlet Type\"", "using": []}, {"type": "LEFT", "right": "contract_agg AS ca", "on": "pa.\"Outlet Type\" = ca.\"Outlet Type\"", "using": []}, {"type": "LEFT", "right": "mgmt_agg AS ma", "on": "pa.\"Outlet Type\" = ma.\"Outlet Type\"", "using": []}, {"type": "LEFT", "right": "assess_agg AS aa", "on": "pa.\"Outlet Type\" = aa.\"Outlet Type\"", "using": []}, {"type": "LEFT", "right": "appeal_agg AS ap", "on": "pa.\"Outlet Type\" = ap.\"Outlet Type\"", "using": []}] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(DISTINCT p."Outlet ID") | [{"table": "\"point_of_sale_(pos)_information\"", "column": "Outlet ID"}] | [] | False |
| B1 | AVG(p."VPO Value") | [{"table": "\"point_of_sale_(pos)_information\"", "column": "VPO Value"}] | [] | False |
| B1 | AVG(p."PC Value") | [{"table": "\"point_of_sale_(pos)_information\"", "column": "PC Value"}] | [] | False |
| B1 | AVG(CAST(REPLACE(p."Qualification Rate", '%', '') AS REAL)) | [{"table": "\"point_of_sale_(pos)_information\"", "column": "Qualification Rate"}] | [] | False |
| B1 | SUM(p."Actual Sales (cases)") | [{"table": "\"point_of_sale_(pos)_information\"", "column": "Actual Sales (cases)"}] | [] | False |
| B1 | SUM(p."Sales Target") | [{"table": "\"point_of_sale_(pos)_information\"", "column": "Sales Target"}] | [] | False |
| B2 | AVG(s." Target Achievement Rate") | [{"table": "sales_data_table", "column": " Target Achievement Rate"}] | [] | False |
| B2 | AVG(s." YoY Growth Rate") | [{"table": "sales_data_table", "column": " YoY Growth Rate"}] | [] | False |
| B2 | AVG(s."MoM Growth Rate") | [{"table": "sales_data_table", "column": "MoM Growth Rate"}] | [] | False |
| B2 | SUM(s."Sales (Value)") | [{"table": "sales_data_table", "column": "Sales (Value)"}] | [] | False |
| B2 | AVG(s."Sales (Value)") | [{"table": "sales_data_table", "column": "Sales (Value)"}] | [] | False |
| B3 | COUNT(c."Agreement ID") | [{"table": "contract_information_table", "column": "Agreement ID"}] | [] | False |
| B3 | SUM(c."Signing Amount (CNY)") | [{"table": "contract_information_table", "column": "Signing Amount (CNY)"}] | [] | False |
| B3 | AVG(c."Signing Amount (CNY)") | [{"table": "contract_information_table", "column": "Signing Amount (CNY)"}] | [] | False |
| B3 | AVG(CASE WHEN c."Renewal Flag" = 'Yes' THEN 1.0 ELSE 0 END) | [] | [{"table": "contract_information_table", "column": "Renewal Flag"}] | False |
| B4 | COUNT(cm."Management ID") | [{"table": "customer_management_table", "column": "Management ID"}] | [] | False |
| B4 | COUNT(cm."Management ID") | [{"table": "customer_management_table", "column": "Management ID"}] | [] | False |
| B4 | COUNT(cm."Management ID") | [{"table": "customer_management_table", "column": "Management ID"}] | [] | False |
| B4 | SUM(CASE WHEN cm."Renewal Likelihood" = 'High' THEN 1 ELSE 0 END) | [] | [{"table": "customer_management_table", "column": "Renewal Likelihood"}] | False |
| B4 | SUM(CASE WHEN cm." Warning Record" = 'Complaint Record' THEN 1 ELSE 0 END) | [] | [{"table": "customer_management_table", "column": " Warning Record"}] | False |
| B4 | SUM(CASE WHEN cm." Warning Record" = 'Quality Issue' THEN 1 ELSE 0 END) | [] | [{"table": "customer_management_table", "column": " Warning Record"}] | False |
| B5 | AVG(a."Assessment pass rate") | [{"table": "assessment_result_table", "column": "Assessment pass rate"}] | [] | False |
| B5 | AVG(a."Score") | [{"table": "assessment_result_table", "column": "Score"}] | [] | False |
| B6 | COUNT(DISTINCT p."Outlet ID") | [{"table": "\"point_of_sale_(pos)_information\"", "column": "Outlet ID"}] | [] | False |
| B6 | COUNT(ap."Appeal ID") | [{"table": "appeal_record_table", "column": "Appeal ID"}] | [] | False |


## S34

类别 `data`；来源 `query_db`；调用 `82c50a98366546c18feec9a9bed8599c`；状态 `success`。

```sql
SELECT p."Outlet Type",
  ROUND(AVG(e."Annual Budget"), 1) AS avg_annual_budget,
  ROUND(AVG(e."Monthly Allocation"), 1) AS avg_monthly_alloc,
  ROUND(AVG(e."Amount Used"), 1) AS avg_amount_used,
  ROUND(AVG(e."Remaining Amount"), 1) AS avg_remaining,
  ROUND(SUM(e."Amount Used") * 1.0 / NULLIF(SUM(e."Annual Budget"), 0), 4) AS budget_utilization
FROM "point_of_sale_(pos)_information" p
LEFT JOIN expense_allocation_table e ON p."Outlet ID" = e."Outlet ID"
GROUP BY p."Outlet Type"
ORDER BY avg_annual_budget DESC
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-030/attempt-01/sql/S34.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-030/attempt-01/sql/S34.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-030/attempt-01/results/S34.rows.jsonl)；完整：True；SHA256：`f13cfd35072227d4e29aaee523d5ec4d982884b609cef2f35d52f384c520d86d`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "p", "kind": "base", "block": null, "base_tables": ["\"point_of_sale_(pos)_information\""]}, {"alias": "e", "kind": "base", "block": null, "base_tables": ["expense_allocation_table"]}] | [{"type": "LEFT", "right": "expense_allocation_table AS e", "on": "p.\"Outlet ID\" = e.\"Outlet ID\"", "using": []}] | ["p.\"Outlet Type\""] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | AVG(e."Annual Budget") | [{"table": "expense_allocation_table", "column": "Annual Budget"}] | [] | False |
| B1 | AVG(e."Monthly Allocation") | [{"table": "expense_allocation_table", "column": "Monthly Allocation"}] | [] | False |
| B1 | AVG(e."Amount Used") | [{"table": "expense_allocation_table", "column": "Amount Used"}] | [] | False |
| B1 | AVG(e."Remaining Amount") | [{"table": "expense_allocation_table", "column": "Remaining Amount"}] | [] | False |
| B1 | SUM(e."Amount Used") | [{"table": "expense_allocation_table", "column": "Amount Used"}] | [] | False |
| B1 | SUM(e."Annual Budget") | [{"table": "expense_allocation_table", "column": "Annual Budget"}] | [] | False |


## S35

类别 `data`；来源 `query_db`；调用 `4e601e017ed54858bf80066042d5bb62`；状态 `success`。

```sql
SELECT p."Outlet Type",
  ROUND(AVG(d."Number of failures"), 2) AS avg_failures,
  COUNT(d."Equipment record code") AS n_devices
FROM "point_of_sale_(pos)_information" p
LEFT JOIN device_information_table d ON p."Outlet ID" = d."Outlet ID"
GROUP BY p."Outlet Type"
ORDER BY avg_failures DESC
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-030/attempt-01/sql/S35.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-030/attempt-01/sql/S35.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-030/attempt-01/results/S35.rows.jsonl)；完整：True；SHA256：`91ff3dcb7eb761bf71b8c6833793f9ab12ce8096e3a42be759a3820dae8f2560`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "p", "kind": "base", "block": null, "base_tables": ["\"point_of_sale_(pos)_information\""]}, {"alias": "d", "kind": "base", "block": null, "base_tables": ["device_information_table"]}] | [{"type": "LEFT", "right": "device_information_table AS d", "on": "p.\"Outlet ID\" = d.\"Outlet ID\"", "using": []}] | ["p.\"Outlet Type\""] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(d."Equipment record code") | [{"table": "device_information_table", "column": "Equipment record code"}] | [] | False |
| B1 | AVG(d."Number of failures") | [{"table": "device_information_table", "column": "Number of failures"}] | [] | False |


## S36

类别 `data`；来源 `query_db`；调用 `12c994e7bb2445fc983ea2e1bed8a305`；状态 `success`。

```sql
SELECT p."Outlet Type",
  COUNT(DISTINCT s."Data Record ID") AS valid_sales_records,
  COUNT(DISTINCT c."Agreement ID") AS contracts,
  COUNT(DISTINCT cm."Management ID") AS mgmt_records,
  COUNT(DISTINCT a."Assessment ID") AS assessments
FROM "point_of_sale_(pos)_information" p
LEFT JOIN sales_data_table s ON p."Customer ID" = s."Customer ID" AND s."Data Status" = 'Valid'
LEFT JOIN contract_information_table c ON p."Outlet ID" = c."Outlet ID"
LEFT JOIN customer_management_table cm ON p."Customer ID" = cm."Customer ID"
LEFT JOIN assessment_result_table a ON p."Outlet ID" = a."Outlet ID"
GROUP BY p."Outlet Type"
ORDER BY p."Outlet Type"
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-030/attempt-01/sql/S36.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-030/attempt-01/sql/S36.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-030/attempt-01/results/S36.rows.jsonl)；完整：True；SHA256：`5b4338445e17d0b8762796e7941dfd4cffafe2259b307975a92f20605c7a42c6`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "p", "kind": "base", "block": null, "base_tables": ["\"point_of_sale_(pos)_information\""]}, {"alias": "s", "kind": "base", "block": null, "base_tables": ["sales_data_table"]}, {"alias": "c", "kind": "base", "block": null, "base_tables": ["contract_information_table"]}, {"alias": "cm", "kind": "base", "block": null, "base_tables": ["customer_management_table"]}, {"alias": "a", "kind": "base", "block": null, "base_tables": ["assessment_result_table"]}] | [{"type": "LEFT", "right": "sales_data_table AS s", "on": "p.\"Customer ID\" = s.\"Customer ID\" AND s.\"Data Status\" = 'Valid'", "using": []}, {"type": "LEFT", "right": "contract_information_table AS c", "on": "p.\"Outlet ID\" = c.\"Outlet ID\"", "using": []}, {"type": "LEFT", "right": "customer_management_table AS cm", "on": "p.\"Customer ID\" = cm.\"Customer ID\"", "using": []}, {"type": "LEFT", "right": "assessment_result_table AS a", "on": "p.\"Outlet ID\" = a.\"Outlet ID\"", "using": []}] | ["p.\"Outlet Type\""] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(DISTINCT s."Data Record ID") | [{"table": "sales_data_table", "column": "Data Record ID"}] | [] | False |
| B1 | COUNT(DISTINCT c."Agreement ID") | [{"table": "contract_information_table", "column": "Agreement ID"}] | [] | False |
| B1 | COUNT(DISTINCT cm."Management ID") | [{"table": "customer_management_table", "column": "Management ID"}] | [] | False |
| B1 | COUNT(DISTINCT a."Assessment ID") | [{"table": "assessment_result_table", "column": "Assessment ID"}] | [] | False |


## S37

类别 `data`；来源 `query_db`；调用 `305debdf22074301b09d5571d907a1c8`；状态 `success`。

```sql
SELECT p."Outlet Type",
  ROUND(MIN(s." Target Achievement Rate"), 4) AS min_tar,
  ROUND(AVG(s." Target Achievement Rate"), 4) AS avg_tar,
  ROUND(MAX(s." Target Achievement Rate"), 4) AS max_tar,
  ROUND(AVG(s."Sales (Value)"), 1) AS avg_sales_value,
  ROUND(COUNT(s."Data Record ID"), 0) AS n
FROM "point_of_sale_(pos)_information" p
JOIN sales_data_table s ON p."Customer ID" = s."Customer ID" AND s."Data Status" = 'Valid'
GROUP BY p."Outlet Type"
ORDER BY avg_tar DESC
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-030/attempt-01/sql/S37.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-030/attempt-01/sql/S37.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-030/attempt-01/results/S37.rows.jsonl)；完整：True；SHA256：`5a1f49cc8238714d39b4572f3243827de5e047292e9ed97064d7b1662b15263c`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "p", "kind": "base", "block": null, "base_tables": ["\"point_of_sale_(pos)_information\""]}, {"alias": "s", "kind": "base", "block": null, "base_tables": ["sales_data_table"]}] | [{"type": "INNER", "right": "sales_data_table AS s", "on": "p.\"Customer ID\" = s.\"Customer ID\" AND s.\"Data Status\" = 'Valid'", "using": []}] | ["p.\"Outlet Type\""] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | MIN(s." Target Achievement Rate") | [{"table": "sales_data_table", "column": " Target Achievement Rate"}] | [] | False |
| B1 | AVG(s." Target Achievement Rate") | [{"table": "sales_data_table", "column": " Target Achievement Rate"}] | [] | False |
| B1 | MAX(s." Target Achievement Rate") | [{"table": "sales_data_table", "column": " Target Achievement Rate"}] | [] | False |
| B1 | AVG(s."Sales (Value)") | [{"table": "sales_data_table", "column": "Sales (Value)"}] | [] | False |
| B1 | COUNT(s."Data Record ID") | [{"table": "sales_data_table", "column": "Data Record ID"}] | [] | False |


## S38

类别 `data`；来源 `query_db`；调用 `5040b2ecdcec4a45b4ff1aa4d2106f2b`；状态 `success`。

```sql
SELECT p."Outlet Type",
  COUNT(ph."Photo ID") AS n_photos,
  SUM(CASE WHEN ph."Review Status" = 'Failed' OR ph."Review Status" = 'Rejected' THEN 1 ELSE 0 END) AS failed_photos,
  ROUND(SUM(CASE WHEN ph."Review Status" = 'Failed' OR ph."Review Status" = 'Rejected' THEN 1 ELSE 0 END) * 1.0 / COUNT(ph."Photo ID"), 4) AS photo_fail_ratio
FROM "point_of_sale_(pos)_information" p
LEFT JOIN photo_information_table ph ON p."Outlet ID" = ph."Outlet ID"
GROUP BY p."Outlet Type"
ORDER BY photo_fail_ratio DESC
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-030/attempt-01/sql/S38.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-030/attempt-01/sql/S38.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-030/attempt-01/results/S38.rows.jsonl)；完整：True；SHA256：`7d3221bb730c052c49f069130e5e92f35ac72cb1db348dfcf5653df6f13d1d56`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "p", "kind": "base", "block": null, "base_tables": ["\"point_of_sale_(pos)_information\""]}, {"alias": "ph", "kind": "base", "block": null, "base_tables": ["photo_information_table"]}] | [{"type": "LEFT", "right": "photo_information_table AS ph", "on": "p.\"Outlet ID\" = ph.\"Outlet ID\"", "using": []}] | ["p.\"Outlet Type\""] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(ph."Photo ID") | [{"table": "photo_information_table", "column": "Photo ID"}] | [] | False |
| B1 | SUM(CASE WHEN ph."Review Status" = 'Failed' OR ph."Review Status" = 'Rejected' THEN 1 ELSE 0 END) | [] | [{"table": "photo_information_table", "column": "Review Status"}, {"table": "photo_information_table", "column": "Review Status"}] | False |
| B1 | COUNT(ph."Photo ID") | [{"table": "photo_information_table", "column": "Photo ID"}] | [] | False |
| B1 | SUM(CASE WHEN ph."Review Status" = 'Failed' OR ph."Review Status" = 'Rejected' THEN 1 ELSE 0 END) | [] | [{"table": "photo_information_table", "column": "Review Status"}, {"table": "photo_information_table", "column": "Review Status"}] | False |

