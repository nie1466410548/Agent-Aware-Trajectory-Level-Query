# dacomp-032

For customers whose `Contact priority` equals 1 in `customer_contact_table`, analyze how e…

运行：已提交。官方未评分。全部 SQL 尝试/成功 59/58；数据 SQL 54/53；Python 5 次。

完整原题：

For customers whose `Contact priority` equals 1 in `customer_contact_table`, analyze how effectively service staff serve this segment by examining their complaint records in `complaints_table` and their ticket-handling performance in `service_ticket_table`.

| 表 | 行数 | 列数 |
| --- | --- | --- |
| campaign_participation_table | 527 | 11 |
| channel_source_table | 471 | 11 |
| complaints_table | 630 | 11 |
| contracts_table | 527 | 11 |
| customer_account_table | 527 | 10 |
| customer_contact_table | 527 | 8 |
| customer_credit_rating_table | 527 | 11 |
| customer_device_table | 510 | 12 |
| customer_feedback_table | 527 | 10 |
| customer_segments_table | 415 | 10 |
| customer_tag_table | 619 | 11 |
| financials_table | 527 | 12 |
| membership_table | 447 | 11 |
| permissions_table | 527 | 11 |
| product_service_order_table | 435 | 12 |
| sales_follow_up_table | 448 | 10 |
| service_ticket_table | 428 | 10 |
| service_usage_table | 527 | 12 |
| transaction_history_table | 483 | 11 |


实际路线（分析者依据 SQL/源码概括，不代表 Agent 自述）：识别联系优先级为 1 的客户 → 多表关联投诉与工单并核查关系 → 比较响应/解决时间和满意度 → Python 分布检验与紧急程度细分图表。

数据库大小：2,449,408 字节。

## 数据 SQL

| SQL | 状态 | 基础表 | Join 输入/类型 | GROUP BY | 聚合表达式 | 结果行数 | 数据库 ms |
| --- | --- | --- | --- | --- | --- | --- | --- |
| [S3/Q1](#s3) | success | ["customer_contact_table"] | 0 / {} | [] | ["COUNT(*)", "COUNT(DISTINCT \"Customer ID\")", "SUM(CASE WHEN \"Contact priority\" = 1 THEN 1 ELSE 0 END)"] | 1 | 0.655 |
| [S4/Q2](#s4) | success | ["complaints_table"] | 0 / {} | [] | ["COUNT(*)"] | 1 | 0.328 |
| [S5/Q3](#s5) | success | ["service_ticket_table"] | 0 / {} | [] | ["COUNT(*)"] | 1 | 0.324 |
| [S6/Q4](#s6) | success | ["customer_contact_table"] | 0 / {} | [] | [] | 5 | 0.323 |
| [S7/Q5](#s7) | success | ["complaints_table"] | 0 / {} | [] | [] | 5 | 0.347 |
| [S8/Q6](#s8) | success | ["service_ticket_table"] | 0 / {} | [] | [] | 5 | 0.338 |
| [S9/Q7](#s9) | success | ["sales_follow_up_table"] | 0 / {} | [] | ["COUNT(*)", "COUNT(DISTINCT \"Work Order ID\")", "COUNT(DISTINCT \"Customer ID\")"] | 1 | 0.845 |
| [S10/Q8](#s10) | success | ["service_ticket_table"] | 0 / {} | [] | ["COUNT(*)"] | 1 | 0.403 |
| [S11/Q9](#s11) | success | ["complaints_table"] | 0 / {} | [] | ["COUNT(*)", "COUNT(DISTINCT \"Work Order ID\")"] | 1 | 0.684 |
| [S12/Q10](#s12) | success | ["complaints_table", "sales_follow_up_table"] | 0 / {} | [] | ["COUNT(*)"] | 1 | 14.7 |
| [S13/Q11](#s13) | success | ["complaints_table", "service_ticket_table"] | 0 / {} | [] | ["COUNT(*)"] | 1 | 23.079 |
| [S14/Q12](#s14) | success | ["sales_follow_up_table", "service_ticket_table"] | 0 / {} | [] | ["COUNT(*)"] | 1 | 10.962 |
| [S15/Q13](#s15) | success | ["contracts_table", "service_ticket_table"] | 2 / {'INNER': 1} | [] | ["COUNT(*)"] | 1 | 0.877 |
| [S16/Q14](#s16) | failed | ["contracts_table", "customer_contact_table", "service_ticket_table"] | 3 / {'INNER': 2} | [] | ["COUNT(*)"] | unknown | 未取得；调用总时长 0.161 ms |
| [S17/Q15](#s17) | success | ["complaints_table", "contracts_table", "customer_contact_table", "sales_follow_up_table", "service_ticket_table"] | 5 / {'LEFT': 3, 'INNER': 1} | [] | ["COUNT(*)"] | 1 | 2.587 |
| [S18/Q16](#s18) | success | ["contracts_table", "customer_contact_table"] | 2 / {'INNER': 1} | [] | ["COUNT(*)"] | 1 | 0.819 |
| [S22/Q17](#s22) | success | ["contracts_table", "customer_contact_table", "service_ticket_table"] | 3 / {'INNER': 2} | [] | ["COUNT(*)"] | 1 | 1.215 |
| [S23/Q18](#s23) | success | ["complaints_table", "customer_contact_table", "sales_follow_up_table"] | 3 / {'INNER': 2} | [] | ["COUNT(*)"] | 1 | 1.267 |
| [S24/Q19](#s24) | success | ["complaints_table", "contracts_table", "customer_contact_table", "service_ticket_table"] | 4 / {'INNER': 3} | [] | ["COUNT(*)"] | 1 | 1.645 |
| [S25/Q20](#s25) | success | ["contracts_table", "customer_contact_table", "service_ticket_table"] | 3 / {'INNER': 2} | ["cc.\"Contact priority\""] | ["COUNT(DISTINCT t.\"Work Order ID\")", "COUNT(DISTINCT c.\"Customer ID\")", "AVG(t.\"Ticket resolution duration\")", "AVG(t.\"Ticket customer satisfaction score\")", "SUM(CASE WHEN t.\"Whether the ticket had a second follow-up\" = 'Yes' THEN 1 ELSE 0 END)"] | 5 | 1.822 |
| [S26/Q21](#s26) | success | ["service_ticket_table"] | 0 / {} | [] | ["COUNT(*)", "AVG(\"Ticket resolution duration\")", "MIN(\"Ticket resolution duration\")", "MAX(\"Ticket resolution duration\")", "AVG(\"Ticket customer satisfaction score\")", "SUM(CASE WHEN \"Ticket priority\" = 1 THEN 1 ELSE 0 END)"] | 1 | 0.579 |
| [S27/Q22](#s27) | success | ["complaints_table", "customer_contact_table", "sales_follow_up_table"] | 3 / {'INNER': 2} | ["cc.\"Contact priority\""] | ["COUNT(DISTINCT cp.\"Complaint Content ID\")", "COUNT(DISTINCT cc.\"Customer ID\")", "AVG(cp.\"Complaint Customer Satisfaction\")", "SUM(CASE WHEN cp.\"Whether Complaint Was Escalated\" = 'Yes' THEN 1 ELSE 0 END)", "AVG(CAST(REPLACE(REPLACE(cp.\"Complaint Handling Speed\", 'h', ''), ' ', '') AS INTEGER))"] | 5 | 1.965 |
| [S28/Q23](#s28) | success | ["complaints_table"] | 0 / {} | [] | [] | 72 | 0.514 |
| [S29/Q24](#s29) | success | ["contracts_table", "customer_contact_table", "service_ticket_table"] | 3 / {'INNER': 2} | ["CASE WHEN cc.\"Contact priority\" = 1 THEN 'Priority 1' ELSE 'Other Priority' END"] | ["COUNT(DISTINCT t.\"Work Order ID\")", "COUNT(DISTINCT t.\"Ticket handling agent ID\")", "SUM(CASE WHEN t.\"Whether the ticket had a second follow-up\" = 'Yes' THEN 1 ELSE 0 END)", "SUM(CASE WHEN t.\"Ticket priority\" = 1 THEN 1 ELSE 0 END)", "SUM(CASE WHEN t.\"Ticket processing urgency level\" = 'High' THEN 1 ELSE 0 END)", "AVG(t.\"Ticket resolution duration\")", "AVG(t.\"Ticket customer satisfaction score\")", "AVG(CASE WHEN t.\"Ticket priority\" = 1 THEN t.\"Ticket resolution duration\" END)", "COUNT(*)", "SUM(CASE WHEN t.\"Whether the ticket had a second follow-up\" = 'Yes' THEN 1 ELSE 0 END)"] | 2 | 1.886 |
| [S30/Q25](#s30) | success | ["complaints_table", "customer_contact_table", "sales_follow_up_table"] | 3 / {'INNER': 2} | ["CASE WHEN cc.\"Contact priority\" = 1 THEN 'Priority 1' ELSE 'Other Priority' END"] | ["COUNT(DISTINCT cp.\"Complaint Content ID\")", "SUM(CASE WHEN cp.\"Whether Complaint Was Escalated\" = 'Yes' THEN 1 ELSE 0 END)", "COUNT(DISTINCT cp.\"Complaint Handler Employee ID\")", "COUNT(DISTINCT cp.\"Complaint Type Serial Number\")", "AVG(cp.\"Complaint Customer Satisfaction\")", "AVG(CAST(REPLACE(cp.\"Complaint Handling Speed\", 'h', '') AS INTEGER))", "AVG(cp.\"Complaint Type Serial Number\")", "COUNT(*)", "SUM(CASE WHEN cp.\"Whether Complaint Was Escalated\" = 'Yes' THEN 1 ELSE 0 END)"] | 2 | 2.005 |
| [S31/Q26](#s31) | success | ["contracts_table", "customer_contact_table", "service_ticket_table"] | 3 / {'INNER': 2} | ["\"Ticket processing urgency level\""] | ["COUNT(*)", "SUM(CASE WHEN \"Whether the ticket had a second follow-up\" = 'Yes' THEN 1 ELSE 0 END)", "AVG(\"Ticket resolution duration\")", "AVG(\"Ticket customer satisfaction score\")"] | 3 | 1.301 |
| [S32/Q27](#s32) | success | ["complaints_table", "customer_contact_table", "sales_follow_up_table"] | 3 / {'INNER': 2} | ["\"Complaint Type Serial Number\""] | ["COUNT(*)", "SUM(CASE WHEN \"Whether Complaint Was Escalated\" = 'Yes' THEN 1 ELSE 0 END)", "AVG(\"Complaint Customer Satisfaction\")", "AVG(CAST(REPLACE(\"Complaint Handling Speed\", 'h', '') AS INTEGER))"] | 6 | 1.453 |
| [S33/Q28](#s33) | success | ["complaints_table", "customer_contact_table", "sales_follow_up_table"] | 3 / {'INNER': 2} | ["\"Complaint Type Serial Number\""] | ["COUNT(*)", "SUM(CASE WHEN \"Whether Complaint Was Escalated\" = 'Yes' THEN 1 ELSE 0 END)", "AVG(\"Complaint Customer Satisfaction\")", "AVG(CAST(REPLACE(\"Complaint Handling Speed\", 'h', '') AS INTEGER))"] | 6 | 1.713 |
| [S34/Q29](#s34) | success | ["complaints_table", "contracts_table", "customer_contact_table", "sales_follow_up_table", "service_ticket_table"] | 5 / {'LEFT': 4} | ["cc.\"Customer ID\""] | ["COUNT(DISTINCT t.\"Work Order ID\")", "COUNT(DISTINCT cp.\"Complaint Content ID\")", "AVG(t.\"Ticket resolution duration\")", "AVG(t.\"Ticket customer satisfaction score\")", "AVG(cp.\"Complaint Customer Satisfaction\")", "COUNT(DISTINCT t.\"Work Order ID\")", "COUNT(DISTINCT cp.\"Complaint Content ID\")", "COUNT(DISTINCT t.\"Work Order ID\")", "COUNT(DISTINCT cp.\"Complaint Content ID\")"] | 41 | 2.675 |
| [S35/Q30](#s35) | success | ["contracts_table", "customer_contact_table", "service_ticket_table"] | 3 / {'INNER': 2} | ["\"Ticket customer satisfaction score\""] | ["COUNT(*)"] | 5 | 1.724 |
| [S36/Q31](#s36) | success | ["complaints_table", "customer_contact_table", "sales_follow_up_table"] | 3 / {'INNER': 2} | ["\"Complaint Customer Satisfaction\""] | ["COUNT(*)"] | 5 | 1.096 |
| [S37/Q32](#s37) | success | ["contracts_table", "customer_contact_table", "service_ticket_table"] | 3 / {'INNER': 2} | ["\"Ticket customer satisfaction score\""] | ["COUNT(*)"] | 5 | 1.358 |
| [S38/Q33](#s38) | success | ["complaints_table", "customer_contact_table", "sales_follow_up_table"] | 3 / {'INNER': 2} | ["\"Complaint Customer Satisfaction\""] | ["COUNT(*)"] | 5 | 1.413 |
| [S39/Q34](#s39) | success | ["contracts_table", "customer_contact_table", "service_ticket_table"] | 3 / {'INNER': 2} | ["t.\"Ticket handling agent ID\""] | ["COUNT(*)", "SUM(CASE WHEN t.\"Whether the ticket had a second follow-up\" = 'Yes' THEN 1 ELSE 0 END)", "AVG(t.\"Ticket customer satisfaction score\")", "AVG(t.\"Ticket resolution duration\")", "COUNT(*)", "COUNT(*)", "SUM(CASE WHEN t.\"Whether the ticket had a second follow-up\" = 'Yes' THEN 1 ELSE 0 END)"] | 27 | 1.382 |
| [S40/Q35](#s40) | success | ["contracts_table", "customer_contact_table", "service_ticket_table"] | 3 / {'INNER': 2} | [] | [] | 162 | 1.847 |
| [S41/Q36](#s41) | success | ["complaints_table", "customer_contact_table", "sales_follow_up_table"] | 3 / {'INNER': 2} | [] | [] | 149 | 1.701 |
| [S42/Q37](#s42) | success | ["complaints_table", "customer_contact_table", "sales_follow_up_table", "service_ticket_table"] | 4 / {'INNER': 2, 'LEFT': 1} | [] | ["COUNT(DISTINCT cp.\"Work Order ID\")", "COUNT(DISTINCT t.\"Work Order ID\")", "COUNT(DISTINCT CASE WHEN cp.\"Work Order ID\" = t.\"Work Order ID\" THEN cp.\"Work Order ID\" END)"] | 1 | 1.606 |
| [S43/Q38](#s43) | success | ["complaints_table", "customer_contact_table", "sales_follow_up_table"] | 3 / {'INNER': 2} | ["\"Complaint Type Serial Number\""] | ["COUNT(*)", "SUM(CASE WHEN cc.\"Contact priority\" = 1 THEN 1 ELSE 0 END)", "AVG(CASE WHEN cc.\"Contact priority\" = 1 THEN \"Complaint Customer Satisfaction\" END)", "AVG(CASE WHEN cc.\"Contact priority\" <> 1 THEN \"Complaint Customer Satisfaction\" END)"] | 6 | 1.532 |
| [S44/Q39](#s44) | success | ["contracts_table", "customer_contact_table", "service_ticket_table"] | 3 / {'INNER': 2} | [] | [] | 162 | 1.722 |
| [S45/Q40](#s45) | success | ["complaints_table", "customer_contact_table", "sales_follow_up_table"] | 3 / {'INNER': 2} | [] | [] | 149 | 1.596 |
| [S46/Q41](#s46) | success | ["contracts_table", "customer_contact_table", "service_ticket_table"] | 3 / {'INNER': 2} | [] | [] | 162 | 1.7 |
| [S47/Q42](#s47) | success | ["complaints_table", "customer_contact_table", "sales_follow_up_table"] | 3 / {'INNER': 2} | [] | [] | 149 | 1.427 |
| [S48/Q43](#s48) | success | ["contracts_table", "customer_contact_table", "service_ticket_table"] | 3 / {'INNER': 2} | [] | [] | 162 | 1.698 |
| [S49/Q44](#s49) | success | ["complaints_table", "customer_contact_table", "sales_follow_up_table"] | 3 / {'INNER': 2} | [] | [] | 149 | 1.475 |
| [S50/Q45](#s50) | success | ["complaints_table", "contracts_table", "customer_contact_table", "sales_follow_up_table", "service_ticket_table"] | 5 / {'LEFT': 4} | ["cc.\"Contact priority\""] | ["COUNT(DISTINCT cc.\"Customer ID\")", "COUNT(DISTINCT CASE WHEN NOT t.\"Work Order ID\" IS NULL THEN cc.\"Customer ID\" END)", "COUNT(DISTINCT CASE WHEN NOT cp.\"Complaint Content ID\" IS NULL THEN cc.\"Customer ID\" END)", "COUNT(DISTINCT CASE WHEN NOT t.\"Work Order ID\" IS NULL OR NOT cp.\"Complaint Content ID\" IS NULL THEN cc.\"Customer ID\" END)"] | 5 | 3.305 |
| [S51/Q46](#s51) | success | ["complaints_table", "contracts_table", "customer_contact_table", "service_ticket_table"] | 4 / {'INNER': 3} | [] | [] | 18 | 1.773 |
| [S52/Q47](#s52) | success | ["complaints_table", "contracts_table", "customer_contact_table", "service_ticket_table"] | 4 / {'INNER': 3} | [] | [] | 18 | 1.781 |
| [S53/Q48](#s53) | success | ["contracts_table", "customer_contact_table", "service_ticket_table"] | 3 / {'INNER': 2} | [] | [] | 162 | 1.611 |
| [S54/Q49](#s54) | success | ["contracts_table", "customer_contact_table", "service_ticket_table"] | 3 / {'INNER': 2} | ["t.\"Ticket processing urgency level\"", "t.\"Whether the ticket had a second follow-up\""] | ["COUNT(*)"] | 5 | 1.248 |
| [S55/Q50](#s55) | success | ["complaints_table", "customer_contact_table", "sales_follow_up_table"] | 3 / {'INNER': 2} | ["cp.\"Complaint Handler Employee ID\""] | ["COUNT(*)", "SUM(CASE WHEN cp.\"Whether Complaint Was Escalated\" = 'Yes' THEN 1 ELSE 0 END)", "AVG(cp.\"Complaint Customer Satisfaction\")", "AVG(CAST(REPLACE(cp.\"Complaint Handling Speed\", 'h', '') AS INTEGER))"] | 25 | 1.514 |
| [S56/Q51](#s56) | success | ["complaints_table", "customer_contact_table", "sales_follow_up_table", "service_ticket_table"] | 3 / {'INNER': 2} | [] | [] | 3 | 1.636 |
| [S57/Q52](#s57) | success | ["complaints_table", "contracts_table", "customer_contact_table", "service_ticket_table"] | 4 / {'INNER': 2, 'LEFT': 1} | ["CASE WHEN NOT cp.\"Complaint Content ID\" IS NULL THEN 'With complaint' ELSE 'Without complaint' END"] | ["COUNT(*)", "SUM(CASE WHEN t.\"Whether the ticket had a second follow-up\" = 'Yes' THEN 1 ELSE 0 END)", "AVG(t.\"Ticket customer satisfaction score\")", "AVG(t.\"Ticket resolution duration\")"] | 2 | 1.821 |
| [S58/Q53](#s58) | success | ["complaints_table", "service_ticket_table"] | 3 / {'LEFT': 2} | [] | ["AVG(\"Ticket resolution duration\")", "AVG(\"Ticket customer satisfaction score\")", "AVG(CAST(REPLACE(\"Complaint Handling Speed\", 'h', '') AS INTEGER))", "AVG(\"Complaint Customer Satisfaction\")"] | 1 | 79.42 |
| [S59/Q54](#s59) | success | ["complaints_table"] | 0 / {} | [] | ["COUNT(*)", "AVG(CAST(REPLACE(\"Complaint Handling Speed\", 'h', '') AS INTEGER))", "AVG(\"Complaint Customer Satisfaction\")"] | 1 | 0.55 |


## 元数据和设置

| SQL | 类别 | 状态 | 内容 |
| --- | --- | --- | --- |
| S1 | connection_setup | success | PRAGMA query_only=ON |
| S2 | metadata | success | SELECT name,sql FROM sqlite_master WHERE type='table' ORDER BY name |
| S19 | metadata | success | PRAGMA table_info(contracts_table) |
| S20 | metadata | success | PRAGMA table_info(customer_contact_table) |
| S21 | metadata | success | PRAGMA table_info(service_ticket_table) |


## Python 与执行位置

人工源码审查：**partial_violation**。SQL handles customer-segment selection and ticket/complaint joins. Python runs Mann-Whitney, Spearman and Kruskal tests, which justify statistical inputs, but also computes group/urgency count and mean summaries for reports and plots. These SQL-capable groupings are deviations; median and statistical procedures are distinguished from those summaries. [证据](../reviews/dacomp-032.json)。

P1：Run statistical significance tests (Mann-Whitney U, given non-normal ordinal satisfaction data) comparing priority-1 vs other customers on ticket/complaint metrics, and generate comparison visualizations. SQL supports the aggregations but not hypothesis testing or plotting.

[源码](../../../runs/dsv4flash-db-first-full-01/dacomp-032/attempt-01/python/P1.py)；[输出](../../../runs/dsv4flash-db-first-full-01/dacomp-032/attempt-01/python/P1.stdout)；[错误](../../../runs/dsv4flash-db-first-full-01/dacomp-032/attempt-01/python/P1.stderr)。检出需人工核验的 SQL 可实现操作：groupby(, .query(；不能仅凭理由判为合规。

P2：Create comparison visualizations (boxplots, bar charts, satisfaction distributions) for ticket and complaint metrics between priority-1 and other customers; plotting is not supported by SQL.

[源码](../../../runs/dsv4flash-db-first-full-01/dacomp-032/attempt-01/python/P2.py)；[输出](../../../runs/dsv4flash-db-first-full-01/dacomp-032/attempt-01/python/P2.stdout)；[错误](../../../runs/dsv4flash-db-first-full-01/dacomp-032/attempt-01/python/P2.stderr)。检出需人工核验的 SQL 可实现操作：groupby(, .query(；不能仅凭理由判为合规。

P3：Create the work directory for saving figures (the previous save failed because the directory did not exist).

[源码](../../../runs/dsv4flash-db-first-full-01/dacomp-032/attempt-01/python/P3.py)；[输出](../../../runs/dsv4flash-db-first-full-01/dacomp-032/attempt-01/python/P3.stdout)；[错误](../../../runs/dsv4flash-db-first-full-01/dacomp-032/attempt-01/python/P3.stderr)。自动源码筛查未检出预设迁出信号；这不是全面语义合规证明。

P4：Create comparison visualizations (boxplots, bar charts, satisfaction distributions) for ticket and complaint metrics between priority-1 and other customers; plotting is not supported by SQL.

[源码](../../../runs/dsv4flash-db-first-full-01/dacomp-032/attempt-01/python/P4.py)；[输出](../../../runs/dsv4flash-db-first-full-01/dacomp-032/attempt-01/python/P4.stdout)；[错误](../../../runs/dsv4flash-db-first-full-01/dacomp-032/attempt-01/python/P4.stderr)。检出需人工核验的 SQL 可实现操作：groupby(, .query(；不能仅凭理由判为合规。

P5：Analyze the correlation between ticket and complaint satisfaction for overlapping work orders of priority-1 customers, and run more statistical tests on urgency-level performance. These analyses (correlation, non-parametric tests, scatter plots) are not supported by SQL.

[源码](../../../runs/dsv4flash-db-first-full-01/dacomp-032/attempt-01/python/P5.py)；[输出](../../../runs/dsv4flash-db-first-full-01/dacomp-032/attempt-01/python/P5.stdout)；[错误](../../../runs/dsv4flash-db-first-full-01/dacomp-032/attempt-01/python/P5.stderr)。检出需人工核验的 SQL 可实现操作：groupby(, .query(；不能仅凭理由判为合规。

## 优化机会

已验证候选。筛选限于精确 SQL、相同自包含 CTE、相同单表完整过滤、可分解单表聚合；未覆盖任意 Join 等价和一般谓词蕴含。全部候选都是 offline，未测在线预测。

| 候选 | 类型 | 已有结果 | 覆盖 SQL | 后续次数 | 中间行数 | 验证 | 成本 |
| --- | --- | --- | --- | --- | --- | --- | --- |
| C1 | exact-result reuse | True | ["S45", "S47", "S49"] | 2 | 149 | verified | Not benchmarked; correctness alone does not establish net speedup. |
| C2 | exact-result reuse | True | ["S46", "S48"] | 1 | 162 | verified | Not benchmarked; correctness alone does not establish net speedup. |
| C3 | aggregate MV | False | ["S4", "S59"] | 1 | unknown | not_verified_cap | Not tested |
| C4 | aggregate MV | False | ["S5", "S26"] | 1 | 1 | verified | Not benchmarked; correctness alone does not establish net speedup. |


已验证覆盖（含触发查询、候选并集去重）：7/53 条成功数据 SQL。正确性仅针对当前数据库快照；未测性能的候选不能声称已加速。

[完整 build/rewrite 与比较证据](dacomp-032.analysis.json)。

### C1：exact-result reuse

Identical normalized SQL and parameters; archive equality checked.

原查询 [S45](#s45), [S47](#s47), [S49](#s49) → 保留前序结果 S45 → 后续 2 次可复用。该构建点为事后假设，不代表 Agent 当时预知后续。

| 原 SQL | 列名一致 | 结果一致 | 比较方法 |
| --- | --- | --- | --- |
| S47 | True | True | exact_multiset |
| S49 | True | True | exact_multiset |


验证状态：verified；成本结论：Not benchmarked; correctness alone does not establish net speedup.

### C2：exact-result reuse

Identical normalized SQL and parameters; archive equality checked.

原查询 [S46](#s46), [S48](#s48) → 保留前序结果 S46 → 后续 1 次可复用。该构建点为事后假设，不代表 Agent 当时预知后续。

| 原 SQL | 列名一致 | 结果一致 | 比较方法 |
| --- | --- | --- | --- |
| S48 | True | True | exact_multiset |


验证状态：verified；成本结论：Not benchmarked; correctness alone does not establish net speedup.

### C4：aggregate MV

Union of grouping keys; decomposable aggregate states; AVG uses SUM and non-NULL COUNT.

原查询 [S5](#s5), [S26](#s26) → 新增共享状态 C4 → 后续 1 次可复用。该构建点为事后假设，不代表 Agent 当时预知后续。

构建定义：

```sql
SELECT COUNT(*) AS __a0, SUM("Ticket resolution duration") AS __a1_sum, COUNT("Ticket resolution duration") AS __a1_n, MIN("Ticket resolution duration") AS __a2, MAX("Ticket resolution duration") AS __a3, SUM("Ticket customer satisfaction score") AS __a4_sum, COUNT("Ticket customer satisfaction score") AS __a4_n, SUM(CASE WHEN "Ticket priority" = 1 THEN 1 ELSE 0 END) AS __a5 FROM "service_ticket_table" 
```

受益查询 S5 的改写示例：

```sql
SELECT SUM(__a0) AS total_tickets FROM temp.reuse_candidate
```

| 原 SQL | 列名一致 | 结果一致 | 比较方法 |
| --- | --- | --- | --- |
| S5 | True | True | exact_multiset |
| S26 | True | True | exact_multiset |


验证状态：verified；成本结论：Not benchmarked; correctness alone does not establish net speedup.

结果依赖：自动记录 SQL→Python 的接口父调用，以及源码中引用归档文件的消费者；字面值相同不认定因果。模型方向选择需要人工读取消息，尚未做全面因果标注。

[原始报告](../../../runs/dsv4flash-db-first-full-01/dacomp-032/attempt-01/answer.md)；[统一消息](../../../runs/dsv4flash-db-first-full-01/dacomp-032/attempt-01/messages.jsonl)；[原始 OpenCode 事件](../../../runs/dsv4flash-db-first-full-01/dacomp-032/attempt-01/opencode.jsonl)；[SQL 引擎日志](../../../runs/dsv4flash-db-first-full-01/dacomp-032/attempt-01/sql_journal.jsonl)。

[可读报告（本地图片链接规范化）](../answers/dacomp-032.md)。原始回答保留，分析结论未改写。

## S1

类别 `connection_setup`；来源 `connection`；调用 `7d32a5787d4348b88283ffb800da6695`；状态 `success`。

```sql
PRAGMA query_only=ON
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-032/attempt-01/sql/S1.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-032/attempt-01/sql/S1.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-032/attempt-01/results/S1.rows.jsonl)；完整：True；SHA256：`e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`。

## S2

类别 `metadata`；来源 `list_db`；调用 `7d32a5787d4348b88283ffb800da6695`；状态 `success`。

```sql
SELECT name,sql FROM sqlite_master WHERE type='table' ORDER BY name
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-032/attempt-01/sql/S2.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-032/attempt-01/sql/S2.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-032/attempt-01/results/S2.rows.jsonl)；完整：True；SHA256：`2c6faedce06ef30ba1a94a94ce6b11e8835fd623351f785ce3a08d61f286462d`。

## S3

类别 `data`；来源 `query_db`；调用 `e96f09f15b5a4e8b8dd34f50c6e8afe2`；状态 `success`。

```sql
SELECT COUNT(*) AS total, COUNT(DISTINCT "Customer ID") AS distinct_customers, SUM(CASE WHEN "Contact priority" = 1 THEN 1 ELSE 0 END) AS priority_1_contacts FROM customer_contact_table
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-032/attempt-01/sql/S3.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-032/attempt-01/sql/S3.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-032/attempt-01/results/S3.rows.jsonl)；完整：True；SHA256：`116fc62176168ee3df8de8daa50a406006a97acae6f424ce5a356a149486f6c6`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "customer_contact_table", "kind": "base", "block": null, "base_tables": ["customer_contact_table"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |
| B1 | COUNT(DISTINCT "Customer ID") | [{"table": "customer_contact_table", "column": "Customer ID"}] | [] | False |
| B1 | SUM(CASE WHEN "Contact priority" = 1 THEN 1 ELSE 0 END) | [] | [{"table": "customer_contact_table", "column": "Contact priority"}] | False |


## S4

类别 `data`；来源 `query_db`；调用 `5e0565d274d14ee3b0b4a3cb2b4121ce`；状态 `success`。

```sql
SELECT COUNT(*) AS total_complaints FROM complaints_table
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-032/attempt-01/sql/S4.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-032/attempt-01/sql/S4.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-032/attempt-01/results/S4.rows.jsonl)；完整：True；SHA256：`195e0958d0832bbe378774abafb38ae11ce5321cef92e1fcd7a318e76955270d`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "complaints_table", "kind": "base", "block": null, "base_tables": ["complaints_table"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |


## S5

类别 `data`；来源 `query_db`；调用 `c09b81e291e24b2b90e15740a3d032cf`；状态 `success`。

```sql
SELECT COUNT(*) AS total_tickets FROM service_ticket_table
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-032/attempt-01/sql/S5.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-032/attempt-01/sql/S5.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-032/attempt-01/results/S5.rows.jsonl)；完整：True；SHA256：`371273e1b434d5140eb99fe573556dea8e3f8ea66e01b3d9a79f9a0936982603`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "service_ticket_table", "kind": "base", "block": null, "base_tables": ["service_ticket_table"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |


## S6

类别 `data`；来源 `query_db`；调用 `268061b7d8e64ff5b0e92e59df540ca7`；状态 `success`。

```sql
SELECT * FROM customer_contact_table LIMIT 5
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-032/attempt-01/sql/S6.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-032/attempt-01/sql/S6.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-032/attempt-01/results/S6.rows.jsonl)；完整：True；SHA256：`803db3ddbcfb8517d16dad6e3307e36139e59229ff03537b4199ca551100b9ad`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "customer_contact_table", "kind": "base", "block": null, "base_tables": ["customer_contact_table"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |


## S7

类别 `data`；来源 `query_db`；调用 `7d688001e9974dfa8361a0eab604395e`；状态 `success`。

```sql
SELECT * FROM complaints_table LIMIT 5
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-032/attempt-01/sql/S7.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-032/attempt-01/sql/S7.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-032/attempt-01/results/S7.rows.jsonl)；完整：True；SHA256：`e404ff53826c94666d87a322fb61f7ed102823227dc0395412b70e56e5f5b3df`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "complaints_table", "kind": "base", "block": null, "base_tables": ["complaints_table"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |


## S8

类别 `data`；来源 `query_db`；调用 `ddd7ecc3895c4d9d81b843e3f263f789`；状态 `success`。

```sql
SELECT * FROM service_ticket_table LIMIT 5
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-032/attempt-01/sql/S8.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-032/attempt-01/sql/S8.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-032/attempt-01/results/S8.rows.jsonl)；完整：True；SHA256：`76bc2ea2e2e1d654023ddd3a4416aa63da2dfcaff53884792b645f48d1f3ca43`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "service_ticket_table", "kind": "base", "block": null, "base_tables": ["service_ticket_table"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |


## S9

类别 `data`；来源 `query_db`；调用 `405a4c2786fd49a8b48f5373fb0a2bce`；状态 `success`。

```sql
SELECT COUNT(*) AS sales_fu_rows, COUNT(DISTINCT "Work Order ID") AS distinct_wo, COUNT(DISTINCT "Customer ID") AS distinct_cust FROM sales_follow_up_table
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-032/attempt-01/sql/S9.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-032/attempt-01/sql/S9.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-032/attempt-01/results/S9.rows.jsonl)；完整：True；SHA256：`ec4278e00ef39af8dc1138b142a3ebaa5c68f183ffdf035c33b89a30e3bd8933`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "sales_follow_up_table", "kind": "base", "block": null, "base_tables": ["sales_follow_up_table"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |
| B1 | COUNT(DISTINCT "Work Order ID") | [{"table": "sales_follow_up_table", "column": "Work Order ID"}] | [] | False |
| B1 | COUNT(DISTINCT "Customer ID") | [{"table": "sales_follow_up_table", "column": "Customer ID"}] | [] | False |


## S10

类别 `data`；来源 `query_db`；调用 `6099e02326df4041b7caae9977493840`；状态 `success`。

```sql
SELECT COUNT(*) AS tickets_with_contract FROM service_ticket_table WHERE "Contract ID" IS NOT NULL AND "Contract ID" != ''
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-032/attempt-01/sql/S10.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-032/attempt-01/sql/S10.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-032/attempt-01/results/S10.rows.jsonl)；完整：True；SHA256：`371273e1b434d5140eb99fe573556dea8e3f8ea66e01b3d9a79f9a0936982603`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "service_ticket_table", "kind": "base", "block": null, "base_tables": ["service_ticket_table"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |


## S11

类别 `data`；来源 `query_db`；调用 `4d39ad863c0046f5a9d33149b72d39f0`；状态 `success`。

```sql
SELECT COUNT(*) AS total_complaints, COUNT(DISTINCT "Work Order ID") AS distinct_wo FROM complaints_table
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-032/attempt-01/sql/S11.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-032/attempt-01/sql/S11.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-032/attempt-01/results/S11.rows.jsonl)；完整：True；SHA256：`327820ffde5e408b33bf9b7fe1c35b31a14069db43fd23e359dda26d1ad77a99`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "complaints_table", "kind": "base", "block": null, "base_tables": ["complaints_table"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |
| B1 | COUNT(DISTINCT "Work Order ID") | [{"table": "complaints_table", "column": "Work Order ID"}] | [] | False |


## S12

类别 `data`；来源 `query_db`；调用 `b583463006484fcf8d71dae67f9d4d8e`；状态 `success`。

```sql
SELECT COUNT(*) AS complaints_in_sfu FROM complaints_table c WHERE EXISTS (SELECT 1 FROM sales_follow_up_table s WHERE s."Work Order ID" = c."Work Order ID")
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-032/attempt-01/sql/S12.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-032/attempt-01/sql/S12.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-032/attempt-01/results/S12.rows.jsonl)；完整：True；SHA256：`6c81f7ad1075417c8e08394ab238b27dcbc46e652223ca67a920aca6133fcb9a`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "s", "kind": "base", "block": null, "base_tables": ["sales_follow_up_table"]}] | [] | [] |
| B2 | [{"alias": "c", "kind": "base", "block": null, "base_tables": ["complaints_table"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B2 | COUNT(*) | [] | [] | True |


## S13

类别 `data`；来源 `query_db`；调用 `8ef482a0240e4f6299901ebf2ad0288b`；状态 `success`。

```sql
SELECT COUNT(*) AS complaints_in_tickets FROM complaints_table c WHERE EXISTS (SELECT 1 FROM service_ticket_table t WHERE t."Work Order ID" = c."Work Order ID")
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-032/attempt-01/sql/S13.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-032/attempt-01/sql/S13.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-032/attempt-01/results/S13.rows.jsonl)；完整：True；SHA256：`04de87c9cef75ee2b7959b33452fc678bdf8d6e4580f5ea21ae07279c657a3d4`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "t", "kind": "base", "block": null, "base_tables": ["service_ticket_table"]}] | [] | [] |
| B2 | [{"alias": "c", "kind": "base", "block": null, "base_tables": ["complaints_table"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B2 | COUNT(*) | [] | [] | True |


## S14

类别 `data`；来源 `query_db`；调用 `86eecede110341a4af15e0afc282d5f7`；状态 `success`。

```sql
SELECT COUNT(*) AS tickets_in_sfu FROM service_ticket_table t WHERE EXISTS (SELECT 1 FROM sales_follow_up_table s WHERE s."Work Order ID" = t."Work Order ID")
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-032/attempt-01/sql/S14.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-032/attempt-01/sql/S14.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-032/attempt-01/results/S14.rows.jsonl)；完整：True；SHA256：`20925b3495f311756cc5e78d5c75eb6fe77608753458ce42fe932d8ac9a94951`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "s", "kind": "base", "block": null, "base_tables": ["sales_follow_up_table"]}] | [] | [] |
| B2 | [{"alias": "t", "kind": "base", "block": null, "base_tables": ["service_ticket_table"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B2 | COUNT(*) | [] | [] | True |


## S15

类别 `data`；来源 `query_db`；调用 `1c2dcd87543e4a859fc0d0cc91620f8d`；状态 `success`。

```sql
SELECT COUNT(*) AS tickets_with_cust FROM service_ticket_table t JOIN contracts_table ct ON t."Contract ID" = ct."Contract ID"
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-032/attempt-01/sql/S15.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-032/attempt-01/sql/S15.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-032/attempt-01/results/S15.rows.jsonl)；完整：True；SHA256：`cfb371f1a88c3424cb03342a029dd86e04138bb3d91d7648ded0be6c5aaf6210`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "t", "kind": "base", "block": null, "base_tables": ["service_ticket_table"]}, {"alias": "ct", "kind": "base", "block": null, "base_tables": ["contracts_table"]}] | [{"type": "INNER", "right": "contracts_table AS ct", "on": "t.\"Contract ID\" = ct.\"Contract ID\"", "using": []}] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |


## S16

类别 `data`；来源 `query_db`；调用 `16bff72cd4574ceaae461ec5a89b7221`；状态 `failed`。

```sql
SELECT COUNT(*) AS priority1_customers_with_tickets FROM (SELECT DISTINCT ct."Customer ID" FROM service_ticket_table t JOIN contracts_table c ON t."Contract ID" = c."Contract ID" JOIN customer_contact_table cc ON cc."Customer ID" = c."Customer ID" WHERE cc."Contact priority" = 1)
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-032/attempt-01/sql/S16.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-032/attempt-01/sql/S16.parameters.json)。

错误：`OperationalError('no such column: ct.Customer ID')`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "t", "kind": "base", "block": null, "base_tables": ["service_ticket_table"]}, {"alias": "c", "kind": "base", "block": null, "base_tables": ["contracts_table"]}, {"alias": "cc", "kind": "base", "block": null, "base_tables": ["customer_contact_table"]}] | [{"type": "INNER", "right": "contracts_table AS c", "on": "t.\"Contract ID\" = c.\"Contract ID\"", "using": []}, {"type": "INNER", "right": "customer_contact_table AS cc", "on": "cc.\"Customer ID\" = c.\"Customer ID\"", "using": []}] | [] |
| B2 | [{"alias": "", "kind": "derived", "block": "B1", "base_tables": ["contracts_table", "customer_contact_table", "service_ticket_table"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B2 | COUNT(*) | [] | [] | True |


未解析列血缘：[{"block": "B2", "column": "ct.\"Customer ID\"", "reason": "ambiguous_or_missing_source"}]

## S17

类别 `data`；来源 `query_db`；调用 `11e75e4a405b4938ae7047c31c983b8e`；状态 `success`。

```sql
SELECT COUNT(*) AS priority1_customers_with_complaints FROM (SELECT DISTINCT cc."Customer ID" FROM complaints_table cp LEFT JOIN sales_follow_up_table s ON cp."Work Order ID" = s."Work Order ID" LEFT JOIN service_ticket_table t ON cp."Work Order ID" = t."Work Order ID" LEFT JOIN contracts_table ct ON t."Contract ID" = ct."Contract ID" JOIN customer_contact_table cc ON cc."Customer ID" = COALESCE(s."Customer ID", ct."Customer ID") WHERE cc."Contact priority" = 1 AND COALESCE(s."Customer ID", ct."Customer ID") IS NOT NULL)
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-032/attempt-01/sql/S17.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-032/attempt-01/sql/S17.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-032/attempt-01/results/S17.rows.jsonl)；完整：True；SHA256：`fd8d7c613715406a208b525486f17f83b89cd219dbfe3230c9c146d374099fee`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "cp", "kind": "base", "block": null, "base_tables": ["complaints_table"]}, {"alias": "s", "kind": "base", "block": null, "base_tables": ["sales_follow_up_table"]}, {"alias": "t", "kind": "base", "block": null, "base_tables": ["service_ticket_table"]}, {"alias": "ct", "kind": "base", "block": null, "base_tables": ["contracts_table"]}, {"alias": "cc", "kind": "base", "block": null, "base_tables": ["customer_contact_table"]}] | [{"type": "LEFT", "right": "sales_follow_up_table AS s", "on": "cp.\"Work Order ID\" = s.\"Work Order ID\"", "using": []}, {"type": "LEFT", "right": "service_ticket_table AS t", "on": "cp.\"Work Order ID\" = t.\"Work Order ID\"", "using": []}, {"type": "LEFT", "right": "contracts_table AS ct", "on": "t.\"Contract ID\" = ct.\"Contract ID\"", "using": []}, {"type": "INNER", "right": "customer_contact_table AS cc", "on": "cc.\"Customer ID\" = COALESCE(s.\"Customer ID\", ct.\"Customer ID\")", "using": []}] | [] |
| B2 | [{"alias": "", "kind": "derived", "block": "B1", "base_tables": ["complaints_table", "contracts_table", "customer_contact_table", "sales_follow_up_table", "service_ticket_table"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B2 | COUNT(*) | [] | [] | True |


## S18

类别 `data`；来源 `query_db`；调用 `880c3a11bdb94dbfb1f2f6ad0d730c1f`；状态 `success`。

```sql
SELECT COUNT(*) AS priority1_with_contracts FROM (SELECT DISTINCT cc."Customer ID" FROM contracts_table ct JOIN customer_contact_table cc ON cc."Customer ID" = ct."Customer ID" WHERE cc."Contact priority" = 1)
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-032/attempt-01/sql/S18.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-032/attempt-01/sql/S18.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-032/attempt-01/results/S18.rows.jsonl)；完整：True；SHA256：`6c6c3586f150b4626ee909e3d8b3a414e5b7dfb7514005060c23995d75d195cf`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "ct", "kind": "base", "block": null, "base_tables": ["contracts_table"]}, {"alias": "cc", "kind": "base", "block": null, "base_tables": ["customer_contact_table"]}] | [{"type": "INNER", "right": "customer_contact_table AS cc", "on": "cc.\"Customer ID\" = ct.\"Customer ID\"", "using": []}] | [] |
| B2 | [{"alias": "", "kind": "derived", "block": "B1", "base_tables": ["contracts_table", "customer_contact_table"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B2 | COUNT(*) | [] | [] | True |


## S19

类别 `metadata`；来源 `query_db`；调用 `a9ee2760534b41ddba5bc547484de9c0`；状态 `success`。

```sql
PRAGMA table_info(contracts_table)
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-032/attempt-01/sql/S19.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-032/attempt-01/sql/S19.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-032/attempt-01/results/S19.rows.jsonl)；完整：True；SHA256：`90fb70c74b0ba1696d42b87db83aee758b9fdf44f79d6eaeda51ea26b8072e7c`。

## S20

类别 `metadata`；来源 `query_db`；调用 `9837844e6ce748629482b7d30ab170bf`；状态 `success`。

```sql
PRAGMA table_info(customer_contact_table)
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-032/attempt-01/sql/S20.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-032/attempt-01/sql/S20.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-032/attempt-01/results/S20.rows.jsonl)；完整：True；SHA256：`fc3c2b296b3d62db99bacc3e3eae4b7d05034ce56423dd59692076cf88726767`。

## S21

类别 `metadata`；来源 `query_db`；调用 `403dd70fa65546d1a639b345b09f0ad2`；状态 `success`。

```sql
PRAGMA table_info(service_ticket_table)
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-032/attempt-01/sql/S21.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-032/attempt-01/sql/S21.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-032/attempt-01/results/S21.rows.jsonl)；完整：True；SHA256：`1d71e2b85938fcf42b6ab07f33366f13b32fd0e6866f29af9e508d6e75aeb61a`。

## S22

类别 `data`；来源 `query_db`；调用 `e9cb79a2262941e2a196013260e16d0f`；状态 `success`。

```sql
SELECT COUNT(*) AS priority1_customers_with_tickets FROM (SELECT DISTINCT c."Customer ID" FROM service_ticket_table t JOIN contracts_table c ON t."Contract ID" = c."Contract ID" JOIN customer_contact_table cc ON cc."Customer ID" = c."Customer ID" WHERE cc."Contact priority" = 1)
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-032/attempt-01/sql/S22.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-032/attempt-01/sql/S22.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-032/attempt-01/results/S22.rows.jsonl)；完整：True；SHA256：`6fd2826852b6d410507b6e2c2cc4d4fd153d08ececb1ab25543dc5ccfebdff6f`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "t", "kind": "base", "block": null, "base_tables": ["service_ticket_table"]}, {"alias": "c", "kind": "base", "block": null, "base_tables": ["contracts_table"]}, {"alias": "cc", "kind": "base", "block": null, "base_tables": ["customer_contact_table"]}] | [{"type": "INNER", "right": "contracts_table AS c", "on": "t.\"Contract ID\" = c.\"Contract ID\"", "using": []}, {"type": "INNER", "right": "customer_contact_table AS cc", "on": "cc.\"Customer ID\" = c.\"Customer ID\"", "using": []}] | [] |
| B2 | [{"alias": "", "kind": "derived", "block": "B1", "base_tables": ["contracts_table", "customer_contact_table", "service_ticket_table"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B2 | COUNT(*) | [] | [] | True |


## S23

类别 `data`；来源 `query_db`；调用 `fd524aa0a2224fe29d27e967ab52cd62`；状态 `success`。

```sql
SELECT COUNT(*) AS priority1_customers_with_complaints_via_sfu FROM (SELECT DISTINCT cc."Customer ID" FROM complaints_table cp JOIN sales_follow_up_table s ON cp."Work Order ID" = s."Work Order ID" JOIN customer_contact_table cc ON cc."Customer ID" = s."Customer ID" WHERE cc."Contact priority" = 1)
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-032/attempt-01/sql/S23.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-032/attempt-01/sql/S23.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-032/attempt-01/results/S23.rows.jsonl)；完整：True；SHA256：`fd8d7c613715406a208b525486f17f83b89cd219dbfe3230c9c146d374099fee`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "cp", "kind": "base", "block": null, "base_tables": ["complaints_table"]}, {"alias": "s", "kind": "base", "block": null, "base_tables": ["sales_follow_up_table"]}, {"alias": "cc", "kind": "base", "block": null, "base_tables": ["customer_contact_table"]}] | [{"type": "INNER", "right": "sales_follow_up_table AS s", "on": "cp.\"Work Order ID\" = s.\"Work Order ID\"", "using": []}, {"type": "INNER", "right": "customer_contact_table AS cc", "on": "cc.\"Customer ID\" = s.\"Customer ID\"", "using": []}] | [] |
| B2 | [{"alias": "", "kind": "derived", "block": "B1", "base_tables": ["complaints_table", "customer_contact_table", "sales_follow_up_table"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B2 | COUNT(*) | [] | [] | True |


## S24

类别 `data`；来源 `query_db`；调用 `ecc69320c4584cf4863239fc9aef0334`；状态 `success`。

```sql
SELECT COUNT(*) AS priority1_customers_with_complaints_via_ticket FROM (SELECT DISTINCT cc."Customer ID" FROM complaints_table cp JOIN service_ticket_table t ON cp."Work Order ID" = t."Work Order ID" JOIN contracts_table c ON t."Contract ID" = c."Contract ID" JOIN customer_contact_table cc ON cc."Customer ID" = c."Customer ID" WHERE cc."Contact priority" = 1)
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-032/attempt-01/sql/S24.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-032/attempt-01/sql/S24.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-032/attempt-01/results/S24.rows.jsonl)；完整：True；SHA256：`2ca96ff50c281cbfed5343b2d17850eb04f0ab562cd9cff6744d54b4adf2d38a`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "cp", "kind": "base", "block": null, "base_tables": ["complaints_table"]}, {"alias": "t", "kind": "base", "block": null, "base_tables": ["service_ticket_table"]}, {"alias": "c", "kind": "base", "block": null, "base_tables": ["contracts_table"]}, {"alias": "cc", "kind": "base", "block": null, "base_tables": ["customer_contact_table"]}] | [{"type": "INNER", "right": "service_ticket_table AS t", "on": "cp.\"Work Order ID\" = t.\"Work Order ID\"", "using": []}, {"type": "INNER", "right": "contracts_table AS c", "on": "t.\"Contract ID\" = c.\"Contract ID\"", "using": []}, {"type": "INNER", "right": "customer_contact_table AS cc", "on": "cc.\"Customer ID\" = c.\"Customer ID\"", "using": []}] | [] |
| B2 | [{"alias": "", "kind": "derived", "block": "B1", "base_tables": ["complaints_table", "contracts_table", "customer_contact_table", "service_ticket_table"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B2 | COUNT(*) | [] | [] | True |


## S25

类别 `data`；来源 `query_db`；调用 `e1c11dd7de524583b02826e3d8aef2ef`；状态 `success`。

```sql
SELECT cc."Contact priority", COUNT(DISTINCT t."Work Order ID") AS tickets, COUNT(DISTINCT c."Customer ID") AS customers, AVG(t."Ticket resolution duration") AS avg_res_dur_hours, AVG(t."Ticket customer satisfaction score") AS avg_sat, SUM(CASE WHEN t."Whether the ticket had a second follow-up" = 'Yes' THEN 1 ELSE 0 END) AS second_followup FROM service_ticket_table t JOIN contracts_table c ON t."Contract ID" = c."Contract ID" JOIN customer_contact_table cc ON cc."Customer ID" = c."Customer ID" GROUP BY cc."Contact priority" ORDER BY cc."Contact priority"
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-032/attempt-01/sql/S25.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-032/attempt-01/sql/S25.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-032/attempt-01/results/S25.rows.jsonl)；完整：True；SHA256：`aabf399710977ba48e7e45a0d7d70c4d1fb531a36c40772c287a32d7bdaaf4a6`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "t", "kind": "base", "block": null, "base_tables": ["service_ticket_table"]}, {"alias": "c", "kind": "base", "block": null, "base_tables": ["contracts_table"]}, {"alias": "cc", "kind": "base", "block": null, "base_tables": ["customer_contact_table"]}] | [{"type": "INNER", "right": "contracts_table AS c", "on": "t.\"Contract ID\" = c.\"Contract ID\"", "using": []}, {"type": "INNER", "right": "customer_contact_table AS cc", "on": "cc.\"Customer ID\" = c.\"Customer ID\"", "using": []}] | ["cc.\"Contact priority\""] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(DISTINCT t."Work Order ID") | [{"table": "service_ticket_table", "column": "Work Order ID"}] | [] | False |
| B1 | COUNT(DISTINCT c."Customer ID") | [{"table": "contracts_table", "column": "Customer ID"}] | [] | False |
| B1 | AVG(t."Ticket resolution duration") | [{"table": "service_ticket_table", "column": "Ticket resolution duration"}] | [] | False |
| B1 | AVG(t."Ticket customer satisfaction score") | [{"table": "service_ticket_table", "column": "Ticket customer satisfaction score"}] | [] | False |
| B1 | SUM(CASE WHEN t."Whether the ticket had a second follow-up" = 'Yes' THEN 1 ELSE 0 END) | [] | [{"table": "service_ticket_table", "column": "Whether the ticket had a second follow-up"}] | False |


## S26

类别 `data`；来源 `query_db`；调用 `10f858df881145069d14da35503b897e`；状态 `success`。

```sql
SELECT COUNT(*) AS n, AVG("Ticket resolution duration") AS avg_res_h, MIN("Ticket resolution duration") AS min_h, MAX("Ticket resolution duration") AS max_h, AVG("Ticket customer satisfaction score") AS avg_sat, SUM(CASE WHEN "Ticket priority" = 1 THEN 1 ELSE 0 END) AS p1_tickets FROM service_ticket_table
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-032/attempt-01/sql/S26.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-032/attempt-01/sql/S26.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-032/attempt-01/results/S26.rows.jsonl)；完整：True；SHA256：`ba18a1a58025595bed5807ad5054e7c4c1487e8bd7502ab2d955e77f6effa22f`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "service_ticket_table", "kind": "base", "block": null, "base_tables": ["service_ticket_table"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |
| B1 | AVG("Ticket resolution duration") | [{"table": "service_ticket_table", "column": "Ticket resolution duration"}] | [] | False |
| B1 | MIN("Ticket resolution duration") | [{"table": "service_ticket_table", "column": "Ticket resolution duration"}] | [] | False |
| B1 | MAX("Ticket resolution duration") | [{"table": "service_ticket_table", "column": "Ticket resolution duration"}] | [] | False |
| B1 | AVG("Ticket customer satisfaction score") | [{"table": "service_ticket_table", "column": "Ticket customer satisfaction score"}] | [] | False |
| B1 | SUM(CASE WHEN "Ticket priority" = 1 THEN 1 ELSE 0 END) | [] | [{"table": "service_ticket_table", "column": "Ticket priority"}] | False |


## S27

类别 `data`；来源 `query_db`；调用 `aa928e48642b430aabeee923b99cb8b4`；状态 `success`。

```sql
SELECT cc."Contact priority", COUNT(DISTINCT cp."Complaint Content ID") AS complaints, COUNT(DISTINCT cc."Customer ID") AS customers, AVG(cp."Complaint Customer Satisfaction") AS avg_sat, SUM(CASE WHEN cp."Whether Complaint Was Escalated" = 'Yes' THEN 1 ELSE 0 END) AS escalated, AVG(CAST(REPLACE(REPLACE(cp."Complaint Handling Speed", 'h', ''), ' ', '') AS INTEGER)) AS avg_speed_hours FROM complaints_table cp JOIN sales_follow_up_table s ON cp."Work Order ID" = s."Work Order ID" JOIN customer_contact_table cc ON cc."Customer ID" = s."Customer ID" GROUP BY cc."Contact priority" ORDER BY cc."Contact priority"
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-032/attempt-01/sql/S27.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-032/attempt-01/sql/S27.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-032/attempt-01/results/S27.rows.jsonl)；完整：True；SHA256：`20a82f9172e57e5a9d28711cb7880b0903d6cd5c3adb29cc80c39c0acada81ea`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "cp", "kind": "base", "block": null, "base_tables": ["complaints_table"]}, {"alias": "s", "kind": "base", "block": null, "base_tables": ["sales_follow_up_table"]}, {"alias": "cc", "kind": "base", "block": null, "base_tables": ["customer_contact_table"]}] | [{"type": "INNER", "right": "sales_follow_up_table AS s", "on": "cp.\"Work Order ID\" = s.\"Work Order ID\"", "using": []}, {"type": "INNER", "right": "customer_contact_table AS cc", "on": "cc.\"Customer ID\" = s.\"Customer ID\"", "using": []}] | ["cc.\"Contact priority\""] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(DISTINCT cp."Complaint Content ID") | [{"table": "complaints_table", "column": "Complaint Content ID"}] | [] | False |
| B1 | COUNT(DISTINCT cc."Customer ID") | [{"table": "customer_contact_table", "column": "Customer ID"}] | [] | False |
| B1 | AVG(cp."Complaint Customer Satisfaction") | [{"table": "complaints_table", "column": "Complaint Customer Satisfaction"}] | [] | False |
| B1 | SUM(CASE WHEN cp."Whether Complaint Was Escalated" = 'Yes' THEN 1 ELSE 0 END) | [] | [{"table": "complaints_table", "column": "Whether Complaint Was Escalated"}] | False |
| B1 | AVG(CAST(REPLACE(REPLACE(cp."Complaint Handling Speed", 'h', ''), ' ', '') AS INTEGER)) | [{"table": "complaints_table", "column": "Complaint Handling Speed"}] | [] | False |


## S28

类别 `data`；来源 `query_db`；调用 `117b2ede67cb431195b5be6643c2ad3f`；状态 `success`。

```sql
SELECT DISTINCT "Complaint Handling Speed" FROM complaints_table ORDER BY "Complaint Handling Speed"
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-032/attempt-01/sql/S28.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-032/attempt-01/sql/S28.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-032/attempt-01/results/S28.rows.jsonl)；完整：True；SHA256：`16900450a14a5a00af2514868964cbb0849b4ec06e2e0f5ea98a97749751c2ca`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "complaints_table", "kind": "base", "block": null, "base_tables": ["complaints_table"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |


## S29

类别 `data`；来源 `query_db`；调用 `1e755ebb360d4513b6dfdea34c79ce16`；状态 `success`。

```sql
SELECT CASE WHEN cc."Contact priority" = 1 THEN 'Priority 1' ELSE 'Other Priority' END AS priority_group, COUNT(DISTINCT t."Work Order ID") AS total_tickets, ROUND(AVG(t."Ticket resolution duration"), 2) AS avg_resolution_hours, ROUND(AVG(t."Ticket customer satisfaction score"), 2) AS avg_satisfaction, COUNT(DISTINCT t."Ticket handling agent ID") AS distinct_agents, SUM(CASE WHEN t."Whether the ticket had a second follow-up" = 'Yes' THEN 1 ELSE 0 END) AS second_followup_count, ROUND(100.0 * SUM(CASE WHEN t."Whether the ticket had a second follow-up" = 'Yes' THEN 1 ELSE 0 END) / COUNT(*), 1) AS second_followup_pct, SUM(CASE WHEN t."Ticket priority" = 1 THEN 1 ELSE 0 END) AS urgent_tickets, ROUND(AVG(CASE WHEN t."Ticket priority" = 1 THEN t."Ticket resolution duration" END), 2) AS avg_urgent_res_hours, SUM(CASE WHEN t."Ticket processing urgency level" = 'High' THEN 1 ELSE 0 END) AS high_urgency FROM service_ticket_table t JOIN contracts_table c ON t."Contract ID" = c."Contract ID" JOIN customer_contact_table cc ON cc."Customer ID" = c."Customer ID" GROUP BY priority_group
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-032/attempt-01/sql/S29.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-032/attempt-01/sql/S29.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-032/attempt-01/results/S29.rows.jsonl)；完整：True；SHA256：`b7de5dc8d772f0178520edb04ad6883f134895c1f5327c69face556ab425b679`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "t", "kind": "base", "block": null, "base_tables": ["service_ticket_table"]}, {"alias": "c", "kind": "base", "block": null, "base_tables": ["contracts_table"]}, {"alias": "cc", "kind": "base", "block": null, "base_tables": ["customer_contact_table"]}] | [{"type": "INNER", "right": "contracts_table AS c", "on": "t.\"Contract ID\" = c.\"Contract ID\"", "using": []}, {"type": "INNER", "right": "customer_contact_table AS cc", "on": "cc.\"Customer ID\" = c.\"Customer ID\"", "using": []}] | ["CASE WHEN cc.\"Contact priority\" = 1 THEN 'Priority 1' ELSE 'Other Priority' END"] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(DISTINCT t."Work Order ID") | [{"table": "service_ticket_table", "column": "Work Order ID"}] | [] | False |
| B1 | COUNT(DISTINCT t."Ticket handling agent ID") | [{"table": "service_ticket_table", "column": "Ticket handling agent ID"}] | [] | False |
| B1 | SUM(CASE WHEN t."Whether the ticket had a second follow-up" = 'Yes' THEN 1 ELSE 0 END) | [] | [{"table": "service_ticket_table", "column": "Whether the ticket had a second follow-up"}] | False |
| B1 | SUM(CASE WHEN t."Ticket priority" = 1 THEN 1 ELSE 0 END) | [] | [{"table": "service_ticket_table", "column": "Ticket priority"}] | False |
| B1 | SUM(CASE WHEN t."Ticket processing urgency level" = 'High' THEN 1 ELSE 0 END) | [] | [{"table": "service_ticket_table", "column": "Ticket processing urgency level"}] | False |
| B1 | AVG(t."Ticket resolution duration") | [{"table": "service_ticket_table", "column": "Ticket resolution duration"}] | [] | False |
| B1 | AVG(t."Ticket customer satisfaction score") | [{"table": "service_ticket_table", "column": "Ticket customer satisfaction score"}] | [] | False |
| B1 | AVG(CASE WHEN t."Ticket priority" = 1 THEN t."Ticket resolution duration" END) | [{"table": "service_ticket_table", "column": "Ticket resolution duration"}] | [{"table": "service_ticket_table", "column": "Ticket priority"}] | False |
| B1 | COUNT(*) | [] | [] | True |
| B1 | SUM(CASE WHEN t."Whether the ticket had a second follow-up" = 'Yes' THEN 1 ELSE 0 END) | [] | [{"table": "service_ticket_table", "column": "Whether the ticket had a second follow-up"}] | False |


## S30

类别 `data`；来源 `query_db`；调用 `fdeae55e49bf4bda9f77d45e9bdf05ca`；状态 `success`。

```sql
SELECT CASE WHEN cc."Contact priority" = 1 THEN 'Priority 1' ELSE 'Other Priority' END AS priority_group, COUNT(DISTINCT cp."Complaint Content ID") AS total_complaints, ROUND(AVG(cp."Complaint Customer Satisfaction"), 2) AS avg_satisfaction, SUM(CASE WHEN cp."Whether Complaint Was Escalated" = 'Yes' THEN 1 ELSE 0 END) AS escalated_count, ROUND(100.0 * SUM(CASE WHEN cp."Whether Complaint Was Escalated" = 'Yes' THEN 1 ELSE 0 END) / COUNT(*), 1) AS escalated_pct, ROUND(AVG(CAST(REPLACE(cp."Complaint Handling Speed", 'h', '') AS INTEGER)), 2) AS avg_handling_speed_hours, COUNT(DISTINCT cp."Complaint Handler Employee ID") AS distinct_handlers, COUNT(DISTINCT cp."Complaint Type Serial Number") AS distinct_complaint_types, ROUND(AVG(cp."Complaint Type Serial Number"), 2) AS avg_complaint_type FROM complaints_table cp JOIN sales_follow_up_table s ON cp."Work Order ID" = s."Work Order ID" JOIN customer_contact_table cc ON cc."Customer ID" = s."Customer ID" GROUP BY priority_group
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-032/attempt-01/sql/S30.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-032/attempt-01/sql/S30.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-032/attempt-01/results/S30.rows.jsonl)；完整：True；SHA256：`523801f1888ec4ca4bed69c78c08571d26275c2666c893d4fc6c1744cdc4d08c`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "cp", "kind": "base", "block": null, "base_tables": ["complaints_table"]}, {"alias": "s", "kind": "base", "block": null, "base_tables": ["sales_follow_up_table"]}, {"alias": "cc", "kind": "base", "block": null, "base_tables": ["customer_contact_table"]}] | [{"type": "INNER", "right": "sales_follow_up_table AS s", "on": "cp.\"Work Order ID\" = s.\"Work Order ID\"", "using": []}, {"type": "INNER", "right": "customer_contact_table AS cc", "on": "cc.\"Customer ID\" = s.\"Customer ID\"", "using": []}] | ["CASE WHEN cc.\"Contact priority\" = 1 THEN 'Priority 1' ELSE 'Other Priority' END"] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(DISTINCT cp."Complaint Content ID") | [{"table": "complaints_table", "column": "Complaint Content ID"}] | [] | False |
| B1 | SUM(CASE WHEN cp."Whether Complaint Was Escalated" = 'Yes' THEN 1 ELSE 0 END) | [] | [{"table": "complaints_table", "column": "Whether Complaint Was Escalated"}] | False |
| B1 | COUNT(DISTINCT cp."Complaint Handler Employee ID") | [{"table": "complaints_table", "column": "Complaint Handler Employee ID"}] | [] | False |
| B1 | COUNT(DISTINCT cp."Complaint Type Serial Number") | [{"table": "complaints_table", "column": "Complaint Type Serial Number"}] | [] | False |
| B1 | AVG(cp."Complaint Customer Satisfaction") | [{"table": "complaints_table", "column": "Complaint Customer Satisfaction"}] | [] | False |
| B1 | AVG(CAST(REPLACE(cp."Complaint Handling Speed", 'h', '') AS INTEGER)) | [{"table": "complaints_table", "column": "Complaint Handling Speed"}] | [] | False |
| B1 | AVG(cp."Complaint Type Serial Number") | [{"table": "complaints_table", "column": "Complaint Type Serial Number"}] | [] | False |
| B1 | COUNT(*) | [] | [] | True |
| B1 | SUM(CASE WHEN cp."Whether Complaint Was Escalated" = 'Yes' THEN 1 ELSE 0 END) | [] | [{"table": "complaints_table", "column": "Whether Complaint Was Escalated"}] | False |


## S31

类别 `data`；来源 `query_db`；调用 `058f8d51ef574aa8aca6ab425ea2dc78`；状态 `success`。

```sql
SELECT "Ticket processing urgency level", COUNT(*) AS cnt, ROUND(AVG("Ticket resolution duration"), 2) AS avg_res_hours, ROUND(AVG("Ticket customer satisfaction score"), 2) AS avg_sat, SUM(CASE WHEN "Whether the ticket had a second follow-up" = 'Yes' THEN 1 ELSE 0 END) AS sfu FROM service_ticket_table t JOIN contracts_table c ON t."Contract ID" = c."Contract ID" JOIN customer_contact_table cc ON cc."Customer ID" = c."Customer ID" WHERE cc."Contact priority" = 1 GROUP BY "Ticket processing urgency level"
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-032/attempt-01/sql/S31.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-032/attempt-01/sql/S31.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-032/attempt-01/results/S31.rows.jsonl)；完整：True；SHA256：`23aa356bab7afefeac1befa425bc0ef075a57984c5fea3102687d1c79a6e248b`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "t", "kind": "base", "block": null, "base_tables": ["service_ticket_table"]}, {"alias": "c", "kind": "base", "block": null, "base_tables": ["contracts_table"]}, {"alias": "cc", "kind": "base", "block": null, "base_tables": ["customer_contact_table"]}] | [{"type": "INNER", "right": "contracts_table AS c", "on": "t.\"Contract ID\" = c.\"Contract ID\"", "using": []}, {"type": "INNER", "right": "customer_contact_table AS cc", "on": "cc.\"Customer ID\" = c.\"Customer ID\"", "using": []}] | ["\"Ticket processing urgency level\""] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |
| B1 | SUM(CASE WHEN "Whether the ticket had a second follow-up" = 'Yes' THEN 1 ELSE 0 END) | [] | [{"table": "service_ticket_table", "column": "Whether the ticket had a second follow-up"}] | False |
| B1 | AVG("Ticket resolution duration") | [{"table": "service_ticket_table", "column": "Ticket resolution duration"}] | [] | False |
| B1 | AVG("Ticket customer satisfaction score") | [{"table": "service_ticket_table", "column": "Ticket customer satisfaction score"}] | [] | False |


## S32

类别 `data`；来源 `query_db`；调用 `3d58b0e41e9d4956904892c5fa588791`；状态 `success`。

```sql
SELECT "Complaint Type Serial Number", COUNT(*) AS cnt, ROUND(AVG("Complaint Customer Satisfaction"), 2) AS avg_sat, SUM(CASE WHEN "Whether Complaint Was Escalated" = 'Yes' THEN 1 ELSE 0 END) AS escalated, ROUND(AVG(CAST(REPLACE("Complaint Handling Speed", 'h', '') AS INTEGER)), 2) AS avg_speed FROM complaints_table cp JOIN sales_follow_up_table s ON cp."Work Order ID" = s."Work Order ID" JOIN customer_contact_table cc ON cc."Customer ID" = s."Customer ID" WHERE cc."Contact priority" = 1 GROUP BY "Complaint Type Serial Number" ORDER BY "Complaint Type Serial Number"
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-032/attempt-01/sql/S32.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-032/attempt-01/sql/S32.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-032/attempt-01/results/S32.rows.jsonl)；完整：True；SHA256：`9811460b70002f8c79968afc59c2242eeab7edec5cc24274e77fec963c48bd68`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "cp", "kind": "base", "block": null, "base_tables": ["complaints_table"]}, {"alias": "s", "kind": "base", "block": null, "base_tables": ["sales_follow_up_table"]}, {"alias": "cc", "kind": "base", "block": null, "base_tables": ["customer_contact_table"]}] | [{"type": "INNER", "right": "sales_follow_up_table AS s", "on": "cp.\"Work Order ID\" = s.\"Work Order ID\"", "using": []}, {"type": "INNER", "right": "customer_contact_table AS cc", "on": "cc.\"Customer ID\" = s.\"Customer ID\"", "using": []}] | ["\"Complaint Type Serial Number\""] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |
| B1 | SUM(CASE WHEN "Whether Complaint Was Escalated" = 'Yes' THEN 1 ELSE 0 END) | [] | [{"table": "complaints_table", "column": "Whether Complaint Was Escalated"}] | False |
| B1 | AVG("Complaint Customer Satisfaction") | [{"table": "complaints_table", "column": "Complaint Customer Satisfaction"}] | [] | False |
| B1 | AVG(CAST(REPLACE("Complaint Handling Speed", 'h', '') AS INTEGER)) | [{"table": "complaints_table", "column": "Complaint Handling Speed"}] | [] | False |


## S33

类别 `data`；来源 `query_db`；调用 `4a8a3a4e50b24959a7d90f0032655cea`；状态 `success`。

```sql
SELECT "Complaint Type Serial Number", COUNT(*) AS cnt, ROUND(AVG("Complaint Customer Satisfaction"), 2) AS avg_sat, SUM(CASE WHEN "Whether Complaint Was Escalated" = 'Yes' THEN 1 ELSE 0 END) AS escalated, ROUND(AVG(CAST(REPLACE("Complaint Handling Speed", 'h', '') AS INTEGER)), 2) AS avg_speed FROM complaints_table cp JOIN sales_follow_up_table s ON cp."Work Order ID" = s."Work Order ID" JOIN customer_contact_table cc ON cc."Customer ID" = s."Customer ID" WHERE cc."Contact priority" != 1 GROUP BY "Complaint Type Serial Number" ORDER BY "Complaint Type Serial Number"
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-032/attempt-01/sql/S33.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-032/attempt-01/sql/S33.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-032/attempt-01/results/S33.rows.jsonl)；完整：True；SHA256：`a8e25062ee6f6f34896425e0e2a58d679b36d26a5a051b329e98e27e406ffce5`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "cp", "kind": "base", "block": null, "base_tables": ["complaints_table"]}, {"alias": "s", "kind": "base", "block": null, "base_tables": ["sales_follow_up_table"]}, {"alias": "cc", "kind": "base", "block": null, "base_tables": ["customer_contact_table"]}] | [{"type": "INNER", "right": "sales_follow_up_table AS s", "on": "cp.\"Work Order ID\" = s.\"Work Order ID\"", "using": []}, {"type": "INNER", "right": "customer_contact_table AS cc", "on": "cc.\"Customer ID\" = s.\"Customer ID\"", "using": []}] | ["\"Complaint Type Serial Number\""] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |
| B1 | SUM(CASE WHEN "Whether Complaint Was Escalated" = 'Yes' THEN 1 ELSE 0 END) | [] | [{"table": "complaints_table", "column": "Whether Complaint Was Escalated"}] | False |
| B1 | AVG("Complaint Customer Satisfaction") | [{"table": "complaints_table", "column": "Complaint Customer Satisfaction"}] | [] | False |
| B1 | AVG(CAST(REPLACE("Complaint Handling Speed", 'h', '') AS INTEGER)) | [{"table": "complaints_table", "column": "Complaint Handling Speed"}] | [] | False |


## S34

类别 `data`；来源 `query_db`；调用 `41e9e7560d5b4a79867956d9f1f62f38`；状态 `success`。

```sql
SELECT cc."Customer ID", COUNT(DISTINCT t."Work Order ID") AS tickets, ROUND(AVG(t."Ticket resolution duration"),1) AS avg_ticket_res_h, ROUND(AVG(t."Ticket customer satisfaction score"),2) AS avg_ticket_sat, COUNT(DISTINCT cp."Complaint Content ID") AS complaints, ROUND(AVG(cp."Complaint Customer Satisfaction"),2) AS avg_comp_sat FROM customer_contact_table cc LEFT JOIN contracts_table c ON cc."Customer ID" = c."Customer ID" LEFT JOIN service_ticket_table t ON t."Contract ID" = c."Contract ID" LEFT JOIN sales_follow_up_table s ON s."Customer ID" = cc."Customer ID" LEFT JOIN complaints_table cp ON cp."Work Order ID" = s."Work Order ID" WHERE cc."Contact priority" = 1 GROUP BY cc."Customer ID" HAVING COUNT(DISTINCT t."Work Order ID") > 0 OR COUNT(DISTINCT cp."Complaint Content ID") > 0 ORDER BY (COUNT(DISTINCT t."Work Order ID") + COUNT(DISTINCT cp."Complaint Content ID")) DESC
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-032/attempt-01/sql/S34.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-032/attempt-01/sql/S34.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-032/attempt-01/results/S34.rows.jsonl)；完整：True；SHA256：`9170ccebec2eae4c3f115a34806eb045436f252fe8127f14ee85c0511a427c85`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "cc", "kind": "base", "block": null, "base_tables": ["customer_contact_table"]}, {"alias": "c", "kind": "base", "block": null, "base_tables": ["contracts_table"]}, {"alias": "t", "kind": "base", "block": null, "base_tables": ["service_ticket_table"]}, {"alias": "s", "kind": "base", "block": null, "base_tables": ["sales_follow_up_table"]}, {"alias": "cp", "kind": "base", "block": null, "base_tables": ["complaints_table"]}] | [{"type": "LEFT", "right": "contracts_table AS c", "on": "cc.\"Customer ID\" = c.\"Customer ID\"", "using": []}, {"type": "LEFT", "right": "service_ticket_table AS t", "on": "t.\"Contract ID\" = c.\"Contract ID\"", "using": []}, {"type": "LEFT", "right": "sales_follow_up_table AS s", "on": "s.\"Customer ID\" = cc.\"Customer ID\"", "using": []}, {"type": "LEFT", "right": "complaints_table AS cp", "on": "cp.\"Work Order ID\" = s.\"Work Order ID\"", "using": []}] | ["cc.\"Customer ID\""] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(DISTINCT t."Work Order ID") | [{"table": "service_ticket_table", "column": "Work Order ID"}] | [] | False |
| B1 | COUNT(DISTINCT cp."Complaint Content ID") | [{"table": "complaints_table", "column": "Complaint Content ID"}] | [] | False |
| B1 | AVG(t."Ticket resolution duration") | [{"table": "service_ticket_table", "column": "Ticket resolution duration"}] | [] | False |
| B1 | AVG(t."Ticket customer satisfaction score") | [{"table": "service_ticket_table", "column": "Ticket customer satisfaction score"}] | [] | False |
| B1 | AVG(cp."Complaint Customer Satisfaction") | [{"table": "complaints_table", "column": "Complaint Customer Satisfaction"}] | [] | False |
| B1 | COUNT(DISTINCT t."Work Order ID") | [{"table": "service_ticket_table", "column": "Work Order ID"}] | [] | False |
| B1 | COUNT(DISTINCT cp."Complaint Content ID") | [{"table": "complaints_table", "column": "Complaint Content ID"}] | [] | False |
| B1 | COUNT(DISTINCT t."Work Order ID") | [{"table": "service_ticket_table", "column": "Work Order ID"}] | [] | False |
| B1 | COUNT(DISTINCT cp."Complaint Content ID") | [{"table": "complaints_table", "column": "Complaint Content ID"}] | [] | False |


## S35

类别 `data`；来源 `query_db`；调用 `8314dc9d667b4e50a8b5d5daf854edb9`；状态 `success`。

```sql
SELECT "Ticket customer satisfaction score", COUNT(*) AS cnt FROM service_ticket_table t JOIN contracts_table c ON t."Contract ID" = c."Contract ID" JOIN customer_contact_table cc ON cc."Customer ID" = c."Customer ID" WHERE cc."Contact priority" = 1 GROUP BY "Ticket customer satisfaction score" ORDER BY "Ticket customer satisfaction score"
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-032/attempt-01/sql/S35.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-032/attempt-01/sql/S35.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-032/attempt-01/results/S35.rows.jsonl)；完整：True；SHA256：`3e18c5e67a63b358b20462b62311bd557f338ad6ec101306635107de5e6e6289`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "t", "kind": "base", "block": null, "base_tables": ["service_ticket_table"]}, {"alias": "c", "kind": "base", "block": null, "base_tables": ["contracts_table"]}, {"alias": "cc", "kind": "base", "block": null, "base_tables": ["customer_contact_table"]}] | [{"type": "INNER", "right": "contracts_table AS c", "on": "t.\"Contract ID\" = c.\"Contract ID\"", "using": []}, {"type": "INNER", "right": "customer_contact_table AS cc", "on": "cc.\"Customer ID\" = c.\"Customer ID\"", "using": []}] | ["\"Ticket customer satisfaction score\""] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |


## S36

类别 `data`；来源 `query_db`；调用 `5df6c1a1939e483bacd3425b6fc7cec5`；状态 `success`。

```sql
SELECT "Complaint Customer Satisfaction", COUNT(*) AS cnt FROM complaints_table cp JOIN sales_follow_up_table s ON cp."Work Order ID" = s."Work Order ID" JOIN customer_contact_table cc ON cc."Customer ID" = s."Customer ID" WHERE cc."Contact priority" = 1 GROUP BY "Complaint Customer Satisfaction" ORDER BY "Complaint Customer Satisfaction"
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-032/attempt-01/sql/S36.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-032/attempt-01/sql/S36.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-032/attempt-01/results/S36.rows.jsonl)；完整：True；SHA256：`8f6f684cfc3d7c81b7d5a5df5373adb7cd2efeab8103138354214c573f1e0514`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "cp", "kind": "base", "block": null, "base_tables": ["complaints_table"]}, {"alias": "s", "kind": "base", "block": null, "base_tables": ["sales_follow_up_table"]}, {"alias": "cc", "kind": "base", "block": null, "base_tables": ["customer_contact_table"]}] | [{"type": "INNER", "right": "sales_follow_up_table AS s", "on": "cp.\"Work Order ID\" = s.\"Work Order ID\"", "using": []}, {"type": "INNER", "right": "customer_contact_table AS cc", "on": "cc.\"Customer ID\" = s.\"Customer ID\"", "using": []}] | ["\"Complaint Customer Satisfaction\""] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |


## S37

类别 `data`；来源 `query_db`；调用 `a98fd0645b354b1db396bf42ce03b6ca`；状态 `success`。

```sql
SELECT "Ticket customer satisfaction score", COUNT(*) AS cnt FROM service_ticket_table t JOIN contracts_table c ON t."Contract ID" = c."Contract ID" JOIN customer_contact_table cc ON cc."Customer ID" = c."Customer ID" WHERE cc."Contact priority" != 1 GROUP BY "Ticket customer satisfaction score" ORDER BY "Ticket customer satisfaction score"
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-032/attempt-01/sql/S37.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-032/attempt-01/sql/S37.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-032/attempt-01/results/S37.rows.jsonl)；完整：True；SHA256：`cfc21af467072e2b3293a2a24d8b62a4738483613d5a7a447a132c9aedd033c1`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "t", "kind": "base", "block": null, "base_tables": ["service_ticket_table"]}, {"alias": "c", "kind": "base", "block": null, "base_tables": ["contracts_table"]}, {"alias": "cc", "kind": "base", "block": null, "base_tables": ["customer_contact_table"]}] | [{"type": "INNER", "right": "contracts_table AS c", "on": "t.\"Contract ID\" = c.\"Contract ID\"", "using": []}, {"type": "INNER", "right": "customer_contact_table AS cc", "on": "cc.\"Customer ID\" = c.\"Customer ID\"", "using": []}] | ["\"Ticket customer satisfaction score\""] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |


## S38

类别 `data`；来源 `query_db`；调用 `9ae1adfae37a4c68a3c2b782cd1ddb13`；状态 `success`。

```sql
SELECT "Complaint Customer Satisfaction", COUNT(*) AS cnt FROM complaints_table cp JOIN sales_follow_up_table s ON cp."Work Order ID" = s."Work Order ID" JOIN customer_contact_table cc ON cc."Customer ID" = s."Customer ID" WHERE cc."Contact priority" != 1 GROUP BY "Complaint Customer Satisfaction" ORDER BY "Complaint Customer Satisfaction"
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-032/attempt-01/sql/S38.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-032/attempt-01/sql/S38.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-032/attempt-01/results/S38.rows.jsonl)；完整：True；SHA256：`0ad85b06d84f35eac51d02b6abb397663f5f2fa46f9eeb05d56e93a33ed54b1c`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "cp", "kind": "base", "block": null, "base_tables": ["complaints_table"]}, {"alias": "s", "kind": "base", "block": null, "base_tables": ["sales_follow_up_table"]}, {"alias": "cc", "kind": "base", "block": null, "base_tables": ["customer_contact_table"]}] | [{"type": "INNER", "right": "sales_follow_up_table AS s", "on": "cp.\"Work Order ID\" = s.\"Work Order ID\"", "using": []}, {"type": "INNER", "right": "customer_contact_table AS cc", "on": "cc.\"Customer ID\" = s.\"Customer ID\"", "using": []}] | ["\"Complaint Customer Satisfaction\""] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |


## S39

类别 `data`；来源 `query_db`；调用 `72a6a05889e24fa0b8b6fb07b16f9ed4`；状态 `success`。

```sql
SELECT t."Ticket handling agent ID", COUNT(*) AS handled_tickets, ROUND(AVG(t."Ticket customer satisfaction score"),2) AS avg_sat, ROUND(AVG(t."Ticket resolution duration"),1) AS avg_res_hours, SUM(CASE WHEN t."Whether the ticket had a second follow-up" = 'Yes' THEN 1 ELSE 0 END) AS sfu, ROUND(100.0 * SUM(CASE WHEN t."Whether the ticket had a second follow-up" = 'Yes' THEN 1 ELSE 0 END) / COUNT(*), 1) AS sfu_pct FROM service_ticket_table t JOIN contracts_table c ON t."Contract ID" = c."Contract ID" JOIN customer_contact_table cc ON cc."Customer ID" = c."Customer ID" WHERE cc."Contact priority" = 1 GROUP BY t."Ticket handling agent ID" ORDER BY COUNT(*) DESC
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-032/attempt-01/sql/S39.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-032/attempt-01/sql/S39.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-032/attempt-01/results/S39.rows.jsonl)；完整：True；SHA256：`84acdb491ceb374b24089899fb28e064de9ab88442fcd902d3192036d460342c`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "t", "kind": "base", "block": null, "base_tables": ["service_ticket_table"]}, {"alias": "c", "kind": "base", "block": null, "base_tables": ["contracts_table"]}, {"alias": "cc", "kind": "base", "block": null, "base_tables": ["customer_contact_table"]}] | [{"type": "INNER", "right": "contracts_table AS c", "on": "t.\"Contract ID\" = c.\"Contract ID\"", "using": []}, {"type": "INNER", "right": "customer_contact_table AS cc", "on": "cc.\"Customer ID\" = c.\"Customer ID\"", "using": []}] | ["t.\"Ticket handling agent ID\""] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |
| B1 | SUM(CASE WHEN t."Whether the ticket had a second follow-up" = 'Yes' THEN 1 ELSE 0 END) | [] | [{"table": "service_ticket_table", "column": "Whether the ticket had a second follow-up"}] | False |
| B1 | AVG(t."Ticket customer satisfaction score") | [{"table": "service_ticket_table", "column": "Ticket customer satisfaction score"}] | [] | False |
| B1 | AVG(t."Ticket resolution duration") | [{"table": "service_ticket_table", "column": "Ticket resolution duration"}] | [] | False |
| B1 | COUNT(*) | [] | [] | True |
| B1 | COUNT(*) | [] | [] | True |
| B1 | SUM(CASE WHEN t."Whether the ticket had a second follow-up" = 'Yes' THEN 1 ELSE 0 END) | [] | [{"table": "service_ticket_table", "column": "Whether the ticket had a second follow-up"}] | False |


## S40

类别 `data`；来源 `query_db`；调用 `ad6bce9ac4a04f839804fff6112a0cb2`；状态 `success`。

```sql
SELECT cc."Customer ID", CASE WHEN cc."Contact priority" = 1 THEN 'Priority 1' ELSE 'Other' END AS grp, t."Work Order ID", t."Ticket resolution duration", t."Ticket customer satisfaction score", t."Ticket processing urgency level", t."Ticket priority", t."Whether the ticket had a second follow-up" FROM service_ticket_table t JOIN contracts_table c ON t."Contract ID" = c."Contract ID" JOIN customer_contact_table cc ON cc."Customer ID" = c."Customer ID"
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-032/attempt-01/sql/S40.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-032/attempt-01/sql/S40.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-032/attempt-01/results/S40.rows.jsonl)；完整：True；SHA256：`2b9ab8292f7df495fbe344b6e1d5d841ef0310c685df804ab80a5eccb8e30b1f`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "t", "kind": "base", "block": null, "base_tables": ["service_ticket_table"]}, {"alias": "c", "kind": "base", "block": null, "base_tables": ["contracts_table"]}, {"alias": "cc", "kind": "base", "block": null, "base_tables": ["customer_contact_table"]}] | [{"type": "INNER", "right": "contracts_table AS c", "on": "t.\"Contract ID\" = c.\"Contract ID\"", "using": []}, {"type": "INNER", "right": "customer_contact_table AS cc", "on": "cc.\"Customer ID\" = c.\"Customer ID\"", "using": []}] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |


## S41

类别 `data`；来源 `query_db`；调用 `efd17848cf7c42fb93c4c4bdc70e51f1`；状态 `success`。

```sql
SELECT cc."Customer ID", CASE WHEN cc."Contact priority" = 1 THEN 'Priority 1' ELSE 'Other' END AS grp, cp."Work Order ID", cp."Complaint Customer Satisfaction", cp."Whether Complaint Was Escalated", cp."Complaint Type Serial Number", CAST(REPLACE(cp."Complaint Handling Speed", 'h', '') AS INTEGER) AS speed_hours FROM complaints_table cp JOIN sales_follow_up_table s ON cp."Work Order ID" = s."Work Order ID" JOIN customer_contact_table cc ON cc."Customer ID" = s."Customer ID"
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-032/attempt-01/sql/S41.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-032/attempt-01/sql/S41.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-032/attempt-01/results/S41.rows.jsonl)；完整：True；SHA256：`39cead45a54b6cf59602e40688ea50ad73a8061275d15e7c941a88606c9d7d1c`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "cp", "kind": "base", "block": null, "base_tables": ["complaints_table"]}, {"alias": "s", "kind": "base", "block": null, "base_tables": ["sales_follow_up_table"]}, {"alias": "cc", "kind": "base", "block": null, "base_tables": ["customer_contact_table"]}] | [{"type": "INNER", "right": "sales_follow_up_table AS s", "on": "cp.\"Work Order ID\" = s.\"Work Order ID\"", "using": []}, {"type": "INNER", "right": "customer_contact_table AS cc", "on": "cc.\"Customer ID\" = s.\"Customer ID\"", "using": []}] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |


## S42

类别 `data`；来源 `query_db`；调用 `7c15550bdd724364a84462e0052a15bd`；状态 `success`。

```sql
SELECT COUNT(DISTINCT cp."Work Order ID") AS complaint_wo, COUNT(DISTINCT t."Work Order ID") AS ticket_wo, COUNT(DISTINCT CASE WHEN cp."Work Order ID" = t."Work Order ID" THEN cp."Work Order ID" END) AS overlap FROM complaints_table cp JOIN sales_follow_up_table s ON cp."Work Order ID" = s."Work Order ID" JOIN customer_contact_table cc ON cc."Customer ID" = s."Customer ID" AND cc."Contact priority" = 1 LEFT JOIN service_ticket_table t ON cp."Work Order ID" = t."Work Order ID"
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-032/attempt-01/sql/S42.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-032/attempt-01/sql/S42.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-032/attempt-01/results/S42.rows.jsonl)；完整：True；SHA256：`e0e39dc425cbc3edf654ba7bc1b42c0ea858675b4753d0fd29d9dbd1f3d7c671`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "cp", "kind": "base", "block": null, "base_tables": ["complaints_table"]}, {"alias": "s", "kind": "base", "block": null, "base_tables": ["sales_follow_up_table"]}, {"alias": "cc", "kind": "base", "block": null, "base_tables": ["customer_contact_table"]}, {"alias": "t", "kind": "base", "block": null, "base_tables": ["service_ticket_table"]}] | [{"type": "INNER", "right": "sales_follow_up_table AS s", "on": "cp.\"Work Order ID\" = s.\"Work Order ID\"", "using": []}, {"type": "INNER", "right": "customer_contact_table AS cc", "on": "cc.\"Customer ID\" = s.\"Customer ID\" AND cc.\"Contact priority\" = 1", "using": []}, {"type": "LEFT", "right": "service_ticket_table AS t", "on": "cp.\"Work Order ID\" = t.\"Work Order ID\"", "using": []}] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(DISTINCT cp."Work Order ID") | [{"table": "complaints_table", "column": "Work Order ID"}] | [] | False |
| B1 | COUNT(DISTINCT t."Work Order ID") | [{"table": "service_ticket_table", "column": "Work Order ID"}] | [] | False |
| B1 | COUNT(DISTINCT CASE WHEN cp."Work Order ID" = t."Work Order ID" THEN cp."Work Order ID" END) | [{"table": "complaints_table", "column": "Work Order ID"}] | [{"table": "complaints_table", "column": "Work Order ID"}, {"table": "service_ticket_table", "column": "Work Order ID"}] | False |


## S43

类别 `data`；来源 `query_db`；调用 `6cdf10e2774c4dd9b3426e1b40d5aa9c`；状态 `success`。

```sql
SELECT "Complaint Type Serial Number", COUNT(*) AS total_cnt, SUM(CASE WHEN cc."Contact priority" = 1 THEN 1 ELSE 0 END) AS priority1_cnt, ROUND(AVG(CASE WHEN cc."Contact priority" = 1 THEN "Complaint Customer Satisfaction" END),2) AS p1_avg_sat, ROUND(AVG(CASE WHEN cc."Contact priority" != 1 THEN "Complaint Customer Satisfaction" END),2) AS other_avg_sat FROM complaints_table cp JOIN sales_follow_up_table s ON cp."Work Order ID" = s."Work Order ID" JOIN customer_contact_table cc ON cc."Customer ID" = s."Customer ID" GROUP BY "Complaint Type Serial Number" ORDER BY "Complaint Type Serial Number"
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-032/attempt-01/sql/S43.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-032/attempt-01/sql/S43.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-032/attempt-01/results/S43.rows.jsonl)；完整：True；SHA256：`33777f1eebd6b1f5e46c3ca532e135297a0e48cc1d32245ba0d513ed7d165ebd`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "cp", "kind": "base", "block": null, "base_tables": ["complaints_table"]}, {"alias": "s", "kind": "base", "block": null, "base_tables": ["sales_follow_up_table"]}, {"alias": "cc", "kind": "base", "block": null, "base_tables": ["customer_contact_table"]}] | [{"type": "INNER", "right": "sales_follow_up_table AS s", "on": "cp.\"Work Order ID\" = s.\"Work Order ID\"", "using": []}, {"type": "INNER", "right": "customer_contact_table AS cc", "on": "cc.\"Customer ID\" = s.\"Customer ID\"", "using": []}] | ["\"Complaint Type Serial Number\""] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |
| B1 | SUM(CASE WHEN cc."Contact priority" = 1 THEN 1 ELSE 0 END) | [] | [{"table": "customer_contact_table", "column": "Contact priority"}] | False |
| B1 | AVG(CASE WHEN cc."Contact priority" = 1 THEN "Complaint Customer Satisfaction" END) | [{"table": "complaints_table", "column": "Complaint Customer Satisfaction"}] | [{"table": "customer_contact_table", "column": "Contact priority"}] | False |
| B1 | AVG(CASE WHEN cc."Contact priority" <> 1 THEN "Complaint Customer Satisfaction" END) | [{"table": "complaints_table", "column": "Complaint Customer Satisfaction"}] | [{"table": "customer_contact_table", "column": "Contact priority"}] | False |


## S44

类别 `data`；来源 `python`；调用 `0940a065b24045338e8d9f1d88b2f768`；状态 `success`。

```sql

SELECT cc."Customer ID", CASE WHEN cc."Contact priority" = 1 THEN 'Priority 1' ELSE 'Other' END AS grp,
t."Ticket resolution duration" AS res_h, t."Ticket customer satisfaction score" AS sat,
t."Ticket processing urgency level" AS urgency, t."Whether the ticket had a second follow-up" AS sfu
FROM service_ticket_table t
JOIN contracts_table c ON t."Contract ID" = c."Contract ID"
JOIN customer_contact_table cc ON cc."Customer ID" = c."Customer ID"

```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-032/attempt-01/sql/S44.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-032/attempt-01/sql/S44.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-032/attempt-01/results/S44.rows.jsonl)；完整：True；SHA256：`a71258ebd4db6de923dfff5915db519fe7c5191889e771efdb2e00167dee1424`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "t", "kind": "base", "block": null, "base_tables": ["service_ticket_table"]}, {"alias": "c", "kind": "base", "block": null, "base_tables": ["contracts_table"]}, {"alias": "cc", "kind": "base", "block": null, "base_tables": ["customer_contact_table"]}] | [{"type": "INNER", "right": "contracts_table AS c", "on": "t.\"Contract ID\" = c.\"Contract ID\"", "using": []}, {"type": "INNER", "right": "customer_contact_table AS cc", "on": "cc.\"Customer ID\" = c.\"Customer ID\"", "using": []}] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |


## S45

类别 `data`；来源 `python`；调用 `0940a065b24045338e8d9f1d88b2f768`；状态 `success`。

```sql

SELECT cc."Customer ID", CASE WHEN cc."Contact priority" = 1 THEN 'Priority 1' ELSE 'Other' END AS grp,
CAST(REPLACE(cp."Complaint Handling Speed",'h','') AS INTEGER) AS speed_h,
cp."Complaint Customer Satisfaction" AS sat, cp."Whether Complaint Was Escalated" AS escalated,
cp."Complaint Type Serial Number" AS ctype
FROM complaints_table cp
JOIN sales_follow_up_table s ON cp."Work Order ID" = s."Work Order ID"
JOIN customer_contact_table cc ON cc."Customer ID" = s."Customer ID"

```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-032/attempt-01/sql/S45.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-032/attempt-01/sql/S45.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-032/attempt-01/results/S45.rows.jsonl)；完整：True；SHA256：`4cfcbef177cefeccb9d2a067d63e42373cec4612c3bc2bc5d1d049df89a9f4e4`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "cp", "kind": "base", "block": null, "base_tables": ["complaints_table"]}, {"alias": "s", "kind": "base", "block": null, "base_tables": ["sales_follow_up_table"]}, {"alias": "cc", "kind": "base", "block": null, "base_tables": ["customer_contact_table"]}] | [{"type": "INNER", "right": "sales_follow_up_table AS s", "on": "cp.\"Work Order ID\" = s.\"Work Order ID\"", "using": []}, {"type": "INNER", "right": "customer_contact_table AS cc", "on": "cc.\"Customer ID\" = s.\"Customer ID\"", "using": []}] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |


## S46

类别 `data`；来源 `python`；调用 `f49c55096dac4bd3ad143bb1ab7393b6`；状态 `success`。

```sql

SELECT cc."Customer ID", CASE WHEN cc."Contact priority" = 1 THEN 'Priority 1' ELSE 'Other' END AS grp,
t."Ticket resolution duration" AS res_h, t."Ticket customer satisfaction score" AS sat,
t."Ticket processing urgency level" AS urgency, t."Whether the ticket had a second follow-up" AS sfu,
t."Ticket priority" AS tprio
FROM service_ticket_table t
JOIN contracts_table c ON t."Contract ID" = c."Contract ID"
JOIN customer_contact_table cc ON cc."Customer ID" = c."Customer ID"

```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-032/attempt-01/sql/S46.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-032/attempt-01/sql/S46.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-032/attempt-01/results/S46.rows.jsonl)；完整：True；SHA256：`828098b64332cc07b589a1f83f6e3edea4a0f2d7063839d356a1e98394ee8923`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "t", "kind": "base", "block": null, "base_tables": ["service_ticket_table"]}, {"alias": "c", "kind": "base", "block": null, "base_tables": ["contracts_table"]}, {"alias": "cc", "kind": "base", "block": null, "base_tables": ["customer_contact_table"]}] | [{"type": "INNER", "right": "contracts_table AS c", "on": "t.\"Contract ID\" = c.\"Contract ID\"", "using": []}, {"type": "INNER", "right": "customer_contact_table AS cc", "on": "cc.\"Customer ID\" = c.\"Customer ID\"", "using": []}] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |


## S47

类别 `data`；来源 `python`；调用 `f49c55096dac4bd3ad143bb1ab7393b6`；状态 `success`。

```sql

SELECT cc."Customer ID", CASE WHEN cc."Contact priority" = 1 THEN 'Priority 1' ELSE 'Other' END AS grp,
CAST(REPLACE(cp."Complaint Handling Speed",'h','') AS INTEGER) AS speed_h,
cp."Complaint Customer Satisfaction" AS sat, cp."Whether Complaint Was Escalated" AS escalated,
cp."Complaint Type Serial Number" AS ctype
FROM complaints_table cp
JOIN sales_follow_up_table s ON cp."Work Order ID" = s."Work Order ID"
JOIN customer_contact_table cc ON cc."Customer ID" = s."Customer ID"

```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-032/attempt-01/sql/S47.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-032/attempt-01/sql/S47.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-032/attempt-01/results/S47.rows.jsonl)；完整：True；SHA256：`4cfcbef177cefeccb9d2a067d63e42373cec4612c3bc2bc5d1d049df89a9f4e4`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "cp", "kind": "base", "block": null, "base_tables": ["complaints_table"]}, {"alias": "s", "kind": "base", "block": null, "base_tables": ["sales_follow_up_table"]}, {"alias": "cc", "kind": "base", "block": null, "base_tables": ["customer_contact_table"]}] | [{"type": "INNER", "right": "sales_follow_up_table AS s", "on": "cp.\"Work Order ID\" = s.\"Work Order ID\"", "using": []}, {"type": "INNER", "right": "customer_contact_table AS cc", "on": "cc.\"Customer ID\" = s.\"Customer ID\"", "using": []}] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |


## S48

类别 `data`；来源 `python`；调用 `12a901e61ab74e92a054856eaa345dba`；状态 `success`。

```sql

SELECT cc."Customer ID", CASE WHEN cc."Contact priority" = 1 THEN 'Priority 1' ELSE 'Other' END AS grp,
t."Ticket resolution duration" AS res_h, t."Ticket customer satisfaction score" AS sat,
t."Ticket processing urgency level" AS urgency, t."Whether the ticket had a second follow-up" AS sfu,
t."Ticket priority" AS tprio
FROM service_ticket_table t
JOIN contracts_table c ON t."Contract ID" = c."Contract ID"
JOIN customer_contact_table cc ON cc."Customer ID" = c."Customer ID"

```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-032/attempt-01/sql/S48.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-032/attempt-01/sql/S48.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-032/attempt-01/results/S48.rows.jsonl)；完整：True；SHA256：`828098b64332cc07b589a1f83f6e3edea4a0f2d7063839d356a1e98394ee8923`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "t", "kind": "base", "block": null, "base_tables": ["service_ticket_table"]}, {"alias": "c", "kind": "base", "block": null, "base_tables": ["contracts_table"]}, {"alias": "cc", "kind": "base", "block": null, "base_tables": ["customer_contact_table"]}] | [{"type": "INNER", "right": "contracts_table AS c", "on": "t.\"Contract ID\" = c.\"Contract ID\"", "using": []}, {"type": "INNER", "right": "customer_contact_table AS cc", "on": "cc.\"Customer ID\" = c.\"Customer ID\"", "using": []}] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |


## S49

类别 `data`；来源 `python`；调用 `12a901e61ab74e92a054856eaa345dba`；状态 `success`。

```sql

SELECT cc."Customer ID", CASE WHEN cc."Contact priority" = 1 THEN 'Priority 1' ELSE 'Other' END AS grp,
CAST(REPLACE(cp."Complaint Handling Speed",'h','') AS INTEGER) AS speed_h,
cp."Complaint Customer Satisfaction" AS sat, cp."Whether Complaint Was Escalated" AS escalated,
cp."Complaint Type Serial Number" AS ctype
FROM complaints_table cp
JOIN sales_follow_up_table s ON cp."Work Order ID" = s."Work Order ID"
JOIN customer_contact_table cc ON cc."Customer ID" = s."Customer ID"

```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-032/attempt-01/sql/S49.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-032/attempt-01/sql/S49.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-032/attempt-01/results/S49.rows.jsonl)；完整：True；SHA256：`4cfcbef177cefeccb9d2a067d63e42373cec4612c3bc2bc5d1d049df89a9f4e4`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "cp", "kind": "base", "block": null, "base_tables": ["complaints_table"]}, {"alias": "s", "kind": "base", "block": null, "base_tables": ["sales_follow_up_table"]}, {"alias": "cc", "kind": "base", "block": null, "base_tables": ["customer_contact_table"]}] | [{"type": "INNER", "right": "sales_follow_up_table AS s", "on": "cp.\"Work Order ID\" = s.\"Work Order ID\"", "using": []}, {"type": "INNER", "right": "customer_contact_table AS cc", "on": "cc.\"Customer ID\" = s.\"Customer ID\"", "using": []}] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |


## S50

类别 `data`；来源 `query_db`；调用 `a161305bba7141d5a1d22a82b83b90b9`；状态 `success`。

```sql
SELECT cc."Contact priority", COUNT(DISTINCT cc."Customer ID") AS total_customers, COUNT(DISTINCT CASE WHEN t."Work Order ID" IS NOT NULL THEN cc."Customer ID" END) AS with_tickets, COUNT(DISTINCT CASE WHEN cp."Complaint Content ID" IS NOT NULL THEN cc."Customer ID" END) AS with_complaints, COUNT(DISTINCT CASE WHEN t."Work Order ID" IS NOT NULL OR cp."Complaint Content ID" IS NOT NULL THEN cc."Customer ID" END) AS with_either FROM customer_contact_table cc LEFT JOIN contracts_table c ON cc."Customer ID" = c."Customer ID" LEFT JOIN service_ticket_table t ON t."Contract ID" = c."Contract ID" LEFT JOIN sales_follow_up_table s ON s."Customer ID" = cc."Customer ID" LEFT JOIN complaints_table cp ON cp."Work Order ID" = s."Work Order ID" GROUP BY cc."Contact priority" ORDER BY cc."Contact priority"
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-032/attempt-01/sql/S50.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-032/attempt-01/sql/S50.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-032/attempt-01/results/S50.rows.jsonl)；完整：True；SHA256：`72252640b0a943cd1e93e54b3130ccd054755c7732d9c5223e295eb857b84538`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "cc", "kind": "base", "block": null, "base_tables": ["customer_contact_table"]}, {"alias": "c", "kind": "base", "block": null, "base_tables": ["contracts_table"]}, {"alias": "t", "kind": "base", "block": null, "base_tables": ["service_ticket_table"]}, {"alias": "s", "kind": "base", "block": null, "base_tables": ["sales_follow_up_table"]}, {"alias": "cp", "kind": "base", "block": null, "base_tables": ["complaints_table"]}] | [{"type": "LEFT", "right": "contracts_table AS c", "on": "cc.\"Customer ID\" = c.\"Customer ID\"", "using": []}, {"type": "LEFT", "right": "service_ticket_table AS t", "on": "t.\"Contract ID\" = c.\"Contract ID\"", "using": []}, {"type": "LEFT", "right": "sales_follow_up_table AS s", "on": "s.\"Customer ID\" = cc.\"Customer ID\"", "using": []}, {"type": "LEFT", "right": "complaints_table AS cp", "on": "cp.\"Work Order ID\" = s.\"Work Order ID\"", "using": []}] | ["cc.\"Contact priority\""] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(DISTINCT cc."Customer ID") | [{"table": "customer_contact_table", "column": "Customer ID"}] | [] | False |
| B1 | COUNT(DISTINCT CASE WHEN NOT t."Work Order ID" IS NULL THEN cc."Customer ID" END) | [{"table": "customer_contact_table", "column": "Customer ID"}] | [{"table": "service_ticket_table", "column": "Work Order ID"}] | False |
| B1 | COUNT(DISTINCT CASE WHEN NOT cp."Complaint Content ID" IS NULL THEN cc."Customer ID" END) | [{"table": "customer_contact_table", "column": "Customer ID"}] | [{"table": "complaints_table", "column": "Complaint Content ID"}] | False |
| B1 | COUNT(DISTINCT CASE WHEN NOT t."Work Order ID" IS NULL OR NOT cp."Complaint Content ID" IS NULL THEN cc."Customer ID" END) | [{"table": "customer_contact_table", "column": "Customer ID"}] | [{"table": "service_ticket_table", "column": "Work Order ID"}, {"table": "complaints_table", "column": "Complaint Content ID"}] | False |


## S51

类别 `data`；来源 `query_db`；调用 `4788ecd78ef84a88aabee3e423ef41e4`；状态 `success`。

```sql
SELECT t."Work Order ID", t."Ticket customer satisfaction score" AS ticket_sat, t."Ticket resolution duration" AS res_h, cp."Complaint Customer Satisfaction" AS comp_sat, cp."Complaint Type Serial Number" AS ctype, CAST(REPLACE(cp."Complaint Handling Speed",'h','') AS INTEGER) AS comp_speed FROM service_ticket_table t JOIN contracts_table c ON t."Contract ID" = c."Contract ID" JOIN customer_contact_table cc ON cc."Customer ID" = c."Customer ID" JOIN complaints_table cp ON cp."Work Order ID" = t."Work Order ID" WHERE cc."Contact priority" = 1 ORDER BY cp."Complaint Type Serial Number"
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-032/attempt-01/sql/S51.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-032/attempt-01/sql/S51.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-032/attempt-01/results/S51.rows.jsonl)；完整：True；SHA256：`a55d54763ac7a5eecd4c9661750a5daefa599b9a971164f5303c4b168dc59bc4`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "t", "kind": "base", "block": null, "base_tables": ["service_ticket_table"]}, {"alias": "c", "kind": "base", "block": null, "base_tables": ["contracts_table"]}, {"alias": "cc", "kind": "base", "block": null, "base_tables": ["customer_contact_table"]}, {"alias": "cp", "kind": "base", "block": null, "base_tables": ["complaints_table"]}] | [{"type": "INNER", "right": "contracts_table AS c", "on": "t.\"Contract ID\" = c.\"Contract ID\"", "using": []}, {"type": "INNER", "right": "customer_contact_table AS cc", "on": "cc.\"Customer ID\" = c.\"Customer ID\"", "using": []}, {"type": "INNER", "right": "complaints_table AS cp", "on": "cp.\"Work Order ID\" = t.\"Work Order ID\"", "using": []}] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |


## S52

类别 `data`；来源 `python`；调用 `7af1a15a5b644013ae20def011020ff5`；状态 `success`。

```sql

SELECT t."Work Order ID", t."Ticket customer satisfaction score" AS ticket_sat,
t."Ticket resolution duration" AS res_h, cp."Complaint Customer Satisfaction" AS comp_sat,
cp."Complaint Type Serial Number" AS ctype,
CAST(REPLACE(cp."Complaint Handling Speed",'h','') AS INTEGER) AS comp_speed
FROM service_ticket_table t
JOIN contracts_table c ON t."Contract ID" = c."Contract ID"
JOIN customer_contact_table cc ON cc."Customer ID" = c."Customer ID"
JOIN complaints_table cp ON cp."Work Order ID" = t."Work Order ID"
WHERE cc."Contact priority" = 1

```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-032/attempt-01/sql/S52.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-032/attempt-01/sql/S52.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-032/attempt-01/results/S52.rows.jsonl)；完整：True；SHA256：`27e859495fd3e56ef83ac7e803fd621dd2d8fc027bf50bb1f6a8798a52d328ef`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "t", "kind": "base", "block": null, "base_tables": ["service_ticket_table"]}, {"alias": "c", "kind": "base", "block": null, "base_tables": ["contracts_table"]}, {"alias": "cc", "kind": "base", "block": null, "base_tables": ["customer_contact_table"]}, {"alias": "cp", "kind": "base", "block": null, "base_tables": ["complaints_table"]}] | [{"type": "INNER", "right": "contracts_table AS c", "on": "t.\"Contract ID\" = c.\"Contract ID\"", "using": []}, {"type": "INNER", "right": "customer_contact_table AS cc", "on": "cc.\"Customer ID\" = c.\"Customer ID\"", "using": []}, {"type": "INNER", "right": "complaints_table AS cp", "on": "cp.\"Work Order ID\" = t.\"Work Order ID\"", "using": []}] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |


## S53

类别 `data`；来源 `python`；调用 `7af1a15a5b644013ae20def011020ff5`；状态 `success`。

```sql

SELECT CASE WHEN cc."Contact priority" = 1 THEN 'Priority 1' ELSE 'Other' END AS grp,
t."Ticket resolution duration" AS res_h, t."Ticket customer satisfaction score" AS sat,
t."Ticket processing urgency level" AS urgency
FROM service_ticket_table t
JOIN contracts_table c ON t."Contract ID" = c."Contract ID"
JOIN customer_contact_table cc ON cc."Customer ID" = c."Customer ID"

```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-032/attempt-01/sql/S53.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-032/attempt-01/sql/S53.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-032/attempt-01/results/S53.rows.jsonl)；完整：True；SHA256：`9eaf5b524ba5e38a44c6fbc47c77c6392270c99a7eb373060aec9f859be288cb`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "t", "kind": "base", "block": null, "base_tables": ["service_ticket_table"]}, {"alias": "c", "kind": "base", "block": null, "base_tables": ["contracts_table"]}, {"alias": "cc", "kind": "base", "block": null, "base_tables": ["customer_contact_table"]}] | [{"type": "INNER", "right": "contracts_table AS c", "on": "t.\"Contract ID\" = c.\"Contract ID\"", "using": []}, {"type": "INNER", "right": "customer_contact_table AS cc", "on": "cc.\"Customer ID\" = c.\"Customer ID\"", "using": []}] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |


## S54

类别 `data`；来源 `query_db`；调用 `d6b57e2253bf42e4bdfd76af66f02c61`；状态 `success`。

```sql
SELECT t."Ticket processing urgency level", t."Whether the ticket had a second follow-up", COUNT(*) AS cnt FROM service_ticket_table t JOIN contracts_table c ON t."Contract ID" = c."Contract ID" JOIN customer_contact_table cc ON cc."Customer ID" = c."Customer ID" WHERE cc."Contact priority" = 1 GROUP BY t."Ticket processing urgency level", t."Whether the ticket had a second follow-up" ORDER BY t."Ticket processing urgency level", t."Whether the ticket had a second follow-up"
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-032/attempt-01/sql/S54.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-032/attempt-01/sql/S54.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-032/attempt-01/results/S54.rows.jsonl)；完整：True；SHA256：`15652f6f76840fefa0f347af41e1a762810c9bbcf107353a193ba00bbfb96bcf`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "t", "kind": "base", "block": null, "base_tables": ["service_ticket_table"]}, {"alias": "c", "kind": "base", "block": null, "base_tables": ["contracts_table"]}, {"alias": "cc", "kind": "base", "block": null, "base_tables": ["customer_contact_table"]}] | [{"type": "INNER", "right": "contracts_table AS c", "on": "t.\"Contract ID\" = c.\"Contract ID\"", "using": []}, {"type": "INNER", "right": "customer_contact_table AS cc", "on": "cc.\"Customer ID\" = c.\"Customer ID\"", "using": []}] | ["t.\"Ticket processing urgency level\"", "t.\"Whether the ticket had a second follow-up\""] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |


## S55

类别 `data`；来源 `query_db`；调用 `e5044ed6933547fcb249674656921677`；状态 `success`。

```sql
SELECT cp."Complaint Handler Employee ID", COUNT(*) AS cnt, ROUND(AVG(cp."Complaint Customer Satisfaction"),2) AS avg_sat, ROUND(AVG(CAST(REPLACE(cp."Complaint Handling Speed",'h','') AS INTEGER)),2) AS avg_speed, SUM(CASE WHEN cp."Whether Complaint Was Escalated" = 'Yes' THEN 1 ELSE 0 END) AS escalated FROM complaints_table cp JOIN sales_follow_up_table s ON cp."Work Order ID" = s."Work Order ID" JOIN customer_contact_table cc ON cc."Customer ID" = s."Customer ID" WHERE cc."Contact priority" = 1 GROUP BY cp."Complaint Handler Employee ID" ORDER BY cnt DESC
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-032/attempt-01/sql/S55.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-032/attempt-01/sql/S55.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-032/attempt-01/results/S55.rows.jsonl)；完整：True；SHA256：`1c346f6ba4d19bb82f3f498f0a3bbe4dd89a928100b62d019f75f3b84be15fc9`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "cp", "kind": "base", "block": null, "base_tables": ["complaints_table"]}, {"alias": "s", "kind": "base", "block": null, "base_tables": ["sales_follow_up_table"]}, {"alias": "cc", "kind": "base", "block": null, "base_tables": ["customer_contact_table"]}] | [{"type": "INNER", "right": "sales_follow_up_table AS s", "on": "cp.\"Work Order ID\" = s.\"Work Order ID\"", "using": []}, {"type": "INNER", "right": "customer_contact_table AS cc", "on": "cc.\"Customer ID\" = s.\"Customer ID\"", "using": []}] | ["cp.\"Complaint Handler Employee ID\""] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |
| B1 | SUM(CASE WHEN cp."Whether Complaint Was Escalated" = 'Yes' THEN 1 ELSE 0 END) | [] | [{"table": "complaints_table", "column": "Whether Complaint Was Escalated"}] | False |
| B1 | AVG(cp."Complaint Customer Satisfaction") | [{"table": "complaints_table", "column": "Complaint Customer Satisfaction"}] | [] | False |
| B1 | AVG(CAST(REPLACE(cp."Complaint Handling Speed", 'h', '') AS INTEGER)) | [{"table": "complaints_table", "column": "Complaint Handling Speed"}] | [] | False |


## S56

类别 `data`；来源 `query_db`；调用 `40f2250b840d47a2b180be4ecb201a3d`；状态 `success`。

```sql
SELECT cp."Complaint Type Serial Number", cp."Complaint Customer Satisfaction", cp."Complaint Handling Speed", cp."Whether Complaint Was Escalated", s."Customer ID" FROM complaints_table cp JOIN sales_follow_up_table s ON cp."Work Order ID" = s."Work Order ID" JOIN customer_contact_table cc ON cc."Customer ID" = s."Customer ID" WHERE cc."Contact priority" = 1 AND cp."Work Order ID" NOT IN (SELECT "Work Order ID" FROM service_ticket_table)
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-032/attempt-01/sql/S56.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-032/attempt-01/sql/S56.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-032/attempt-01/results/S56.rows.jsonl)；完整：True；SHA256：`f369fa191ea702e2e0f2b599a176270c39506e8d01520ff098947c30b5a1dfa2`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "service_ticket_table", "kind": "base", "block": null, "base_tables": ["service_ticket_table"]}] | [] | [] |
| B2 | [{"alias": "cp", "kind": "base", "block": null, "base_tables": ["complaints_table"]}, {"alias": "s", "kind": "base", "block": null, "base_tables": ["sales_follow_up_table"]}, {"alias": "cc", "kind": "base", "block": null, "base_tables": ["customer_contact_table"]}] | [{"type": "INNER", "right": "sales_follow_up_table AS s", "on": "cp.\"Work Order ID\" = s.\"Work Order ID\"", "using": []}, {"type": "INNER", "right": "customer_contact_table AS cc", "on": "cc.\"Customer ID\" = s.\"Customer ID\"", "using": []}] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |


未解析列血缘：[{"block": "B2", "column": "\"Work Order ID\"", "reason": "ambiguous_or_missing_source"}]

## S57

类别 `data`；来源 `query_db`；调用 `616b289ff1034bedb535b8070812909a`；状态 `success`。

```sql
SELECT CASE WHEN cp."Complaint Content ID" IS NOT NULL THEN 'With complaint' ELSE 'Without complaint' END AS has_complaint, COUNT(*) AS tickets, ROUND(AVG(t."Ticket customer satisfaction score"),2) AS avg_sat, ROUND(AVG(t."Ticket resolution duration"),1) AS avg_res_h, SUM(CASE WHEN t."Whether the ticket had a second follow-up" = 'Yes' THEN 1 ELSE 0 END) AS sfu FROM service_ticket_table t JOIN contracts_table c ON t."Contract ID" = c."Contract ID" JOIN customer_contact_table cc ON cc."Customer ID" = c."Customer ID" LEFT JOIN complaints_table cp ON cp."Work Order ID" = t."Work Order ID" WHERE cc."Contact priority" = 1 GROUP BY has_complaint
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-032/attempt-01/sql/S57.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-032/attempt-01/sql/S57.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-032/attempt-01/results/S57.rows.jsonl)；完整：True；SHA256：`6f264f234983bf35748d9fe7d4be6e5056b8e5638e3cd52954dd2fcc2084ed24`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "t", "kind": "base", "block": null, "base_tables": ["service_ticket_table"]}, {"alias": "c", "kind": "base", "block": null, "base_tables": ["contracts_table"]}, {"alias": "cc", "kind": "base", "block": null, "base_tables": ["customer_contact_table"]}, {"alias": "cp", "kind": "base", "block": null, "base_tables": ["complaints_table"]}] | [{"type": "INNER", "right": "contracts_table AS c", "on": "t.\"Contract ID\" = c.\"Contract ID\"", "using": []}, {"type": "INNER", "right": "customer_contact_table AS cc", "on": "cc.\"Customer ID\" = c.\"Customer ID\"", "using": []}, {"type": "LEFT", "right": "complaints_table AS cp", "on": "cp.\"Work Order ID\" = t.\"Work Order ID\"", "using": []}] | ["CASE WHEN NOT cp.\"Complaint Content ID\" IS NULL THEN 'With complaint' ELSE 'Without complaint' END"] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |
| B1 | SUM(CASE WHEN t."Whether the ticket had a second follow-up" = 'Yes' THEN 1 ELSE 0 END) | [] | [{"table": "service_ticket_table", "column": "Whether the ticket had a second follow-up"}] | False |
| B1 | AVG(t."Ticket customer satisfaction score") | [{"table": "service_ticket_table", "column": "Ticket customer satisfaction score"}] | [] | False |
| B1 | AVG(t."Ticket resolution duration") | [{"table": "service_ticket_table", "column": "Ticket resolution duration"}] | [] | False |


## S58

类别 `data`；来源 `query_db`；调用 `47d5d41bfd8042dda2be059084ec7b56`；状态 `success`。

```sql
SELECT ROUND(AVG("Ticket resolution duration"),1) AS overall_avg_res, ROUND(AVG("Ticket customer satisfaction score"),2) AS overall_avg_sat, ROUND(AVG(CAST(REPLACE("Complaint Handling Speed",'h','') AS INTEGER)),1) AS overall_comp_speed, ROUND(AVG("Complaint Customer Satisfaction"),2) AS overall_comp_sat FROM (SELECT 1) x LEFT JOIN service_ticket_table t ON 1=1 LEFT JOIN complaints_table cp ON 1=1
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-032/attempt-01/sql/S58.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-032/attempt-01/sql/S58.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-032/attempt-01/results/S58.rows.jsonl)；完整：True；SHA256：`5f77da6bdefd164fffde80c45126ed3650351ed84a38fce444e6533b2e050fbf`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [] | [] | [] |
| B2 | [{"alias": "x", "kind": "derived", "block": "B1", "base_tables": []}, {"alias": "t", "kind": "base", "block": null, "base_tables": ["service_ticket_table"]}, {"alias": "cp", "kind": "base", "block": null, "base_tables": ["complaints_table"]}] | [{"type": "LEFT", "right": "service_ticket_table AS t", "on": "1 = 1", "using": []}, {"type": "LEFT", "right": "complaints_table AS cp", "on": "1 = 1", "using": []}] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B2 | AVG("Ticket resolution duration") | [{"table": "service_ticket_table", "column": "Ticket resolution duration"}] | [] | False |
| B2 | AVG("Ticket customer satisfaction score") | [{"table": "service_ticket_table", "column": "Ticket customer satisfaction score"}] | [] | False |
| B2 | AVG(CAST(REPLACE("Complaint Handling Speed", 'h', '') AS INTEGER)) | [{"table": "complaints_table", "column": "Complaint Handling Speed"}] | [] | False |
| B2 | AVG("Complaint Customer Satisfaction") | [{"table": "complaints_table", "column": "Complaint Customer Satisfaction"}] | [] | False |


## S59

类别 `data`；来源 `query_db`；调用 `e5e8482f4a7b45b59b6f8c9ea8fd992a`；状态 `success`。

```sql
SELECT ROUND(AVG(CAST(REPLACE("Complaint Handling Speed",'h','') AS INTEGER)),1) AS overall_comp_speed, ROUND(AVG("Complaint Customer Satisfaction"),2) AS overall_comp_sat, COUNT(*) AS n FROM complaints_table
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-032/attempt-01/sql/S59.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-032/attempt-01/sql/S59.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-032/attempt-01/results/S59.rows.jsonl)；完整：True；SHA256：`cfa01c13f55935f21886aee749185e51fc210893c158ee877c1649c9a40ade30`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "complaints_table", "kind": "base", "block": null, "base_tables": ["complaints_table"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |
| B1 | AVG(CAST(REPLACE("Complaint Handling Speed", 'h', '') AS INTEGER)) | [{"table": "complaints_table", "column": "Complaint Handling Speed"}] | [] | False |
| B1 | AVG("Complaint Customer Satisfaction") | [{"table": "complaints_table", "column": "Complaint Customer Satisfaction"}] | [] | False |

