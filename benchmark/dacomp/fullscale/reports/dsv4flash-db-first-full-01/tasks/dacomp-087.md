# dacomp-087

A sales team reorganization is imminent, requiring the design of a data-driven customer re…

运行：已提交。官方未评分。全部 SQL 尝试/成功 22/22；数据 SQL 20/20；Python 14 次。

完整原题：

A sales team reorganization is imminent, requiring the design of a data-driven customer reallocation plan. First, calculate a workload score for each sales representative using the following fixed formula: Workload Score = Number of Customers*0.3 + Total Annual Revenue (in millions)/10*0.4 + Contact Coverage Rate (Number of Contacts / Number of Customers)*0.2 + Geographic Complexity Factor*0.1, where the Geographic Complexity Factor = DISTINCT(Number of States)*2 + DISTINCT(Number of Cities)*0.5, and the Contact Coverage Rate is capped at 5; then calculate a sales efficiency metric: Efficiency Score = Win Rate*0.4 + (Average Deal Size / 100,000)*0.3 + (120 / Average Sales Cycle Days)*0.2 + Opportunity Conversion Rate*0.1; based on the workload score, identify representatives with an uneven workload distribution (standard deviation > 0.3 * average), use a data science method you deem appropriate to design a customer reallocation algorithm. This algorithm must incorporate constraints such as geographic proximity (prioritize allocating customers within the same state), industry expertise match (at least 60% of a rep's customers should be in their top 3 industries), and customer size suitability. Propose a concrete customer transfer plan and quantify its expected impact. The final objective is to maximize the expected improvement in the overall team's efficiency score and customer retention probability, while ensuring the workload score for each rep is controlled within a ±15% variance range.

| 表 | 行数 | 列数 |
| --- | --- | --- |
| salesforce__advanced_opportunity_analytics | 47758 | 39 |
| salesforce__contact_enhanced | 25000 | 55 |
| salesforce__customer_360_view | 10000 | 54 |
| salesforce__manager_performance | 381 | 25 |
| salesforce__opportunity_enhanced | 20000 | 65 |
| salesforce__revenue_forecasting | 24 | 33 |
| salesforce__sales_performance_dashboard | 1000 | 48 |


实际路线（分析者依据 SQL/源码概括，不代表 Agent 自述）：SQL 销售负荷与客户提取 → Python 重分配搜索 → 服务中断后同会话继续图表与方案汇总 → 提交。

数据库大小：55,074,816 字节。

## 数据 SQL

| SQL | 状态 | 基础表 | Join 输入/类型 | GROUP BY | 聚合表达式 | 结果行数 | 数据库 ms |
| --- | --- | --- | --- | --- | --- | --- | --- |
| [S3/Q1](#s3) | success | ["salesforce__customer_360_view"] | 0 / {} | [] | ["COUNT(*)"] | 1 | 2.485 |
| [S4/Q2](#s4) | success | ["salesforce__sales_performance_dashboard"] | 0 / {} | [] | ["COUNT(*)"] | 1 | 0.362 |
| [S5/Q3](#s5) | success | ["salesforce__sales_performance_dashboard"] | 0 / {} | [] | [] | 20 | 0.427 |
| [S6/Q4](#s6) | success | ["salesforce__sales_performance_dashboard"] | 0 / {} | [] | ["COUNT(DISTINCT owner_id)"] | 1 | 0.998 |
| [S7/Q5](#s7) | success | ["salesforce__customer_360_view"] | 0 / {} | [] | ["COUNT(DISTINCT owner_id)", "COUNT(DISTINCT account_id)"] | 1 | 13.185 |
| [S8/Q6](#s8) | success | ["salesforce__customer_360_view"] | 0 / {} | ["owner_id"] | ["COUNT(*)", "SUM(annual_revenue)", "SUM(total_contacts)", "SUM(total_opportunities)", "AVG(annual_revenue)"] | 20 | 8.93 |
| [S9/Q7](#s9) | success | ["salesforce__customer_360_view"] | 0 / {} | [] | [] | 20 | 0.445 |
| [S10/Q8](#s10) | success | ["salesforce__customer_360_view"] | 0 / {} | ["industry_normalized"] | ["COUNT(*)"] | 16 | 5.021 |
| [S11/Q9](#s11) | success | ["salesforce__customer_360_view"] | 0 / {} | ["owner_id"] | ["COUNT(*)", "SUM(annual_revenue)", "SUM(total_contacts)", "SUM(total_opportunities)", "SUM(won_opportunities)", "AVG(annual_revenue)"] | 10 | 9.606 |
| [S12/Q10](#s12) | success | ["salesforce__customer_360_view"] | 0 / {} | ["owner_id"] | ["COUNT(DISTINCT billing_state)", "COUNT(DISTINCT billing_city)"] | 10 | 10.835 |
| [S13/Q11](#s13) | success | ["salesforce__customer_360_view"] | 2 / {'INNER': 1} | ["owner_id", "owner_id"] | ["COUNT(DISTINCT billing_state)", "COUNT(DISTINCT billing_city)", "COUNT(*)", "SUM(annual_revenue)", "SUM(total_contacts)"] | 20 | 19.854 |
| [S14/Q12](#s14) | success | ["salesforce__customer_360_view"] | 2 / {'INNER': 1} | ["owner_id", "owner_id"] | ["COUNT(DISTINCT billing_state)", "COUNT(DISTINCT billing_city)", "COUNT(*)", "SUM(annual_revenue)", "SUM(total_contacts)", "AVG(workload_score)", "AVG(workload_score)", "AVG(workload_score)", "AVG(workload_score)", "AVG(workload_score)", "COUNT(*)", "AVG(workload_score)", "MIN(workload_score)", "MAX(workload_score)", "AVG(workload_score)", "SUM((workload_score - (SELECT AVG(workload_score) FROM scores)) * (workload_score - (SELECT AVG(workload_score) FROM scores)))", "SUM((workload_score - (SELECT AVG(workload_score) FROM scores)) * (workload_score - (SELECT AVG(workload_score) FROM scores)))", "COUNT(*)", "COUNT(*)"] | 1 | 27.591 |
| [S15/Q13](#s15) | success | ["salesforce__sales_performance_dashboard"] | 0 / {} | [] | [] | 10 | 0.363 |
| [S16/Q14](#s16) | success | ["salesforce__sales_performance_dashboard"] | 0 / {} | [] | ["MIN(win_rate_pct)", "AVG(win_rate_pct)", "MAX(win_rate_pct)", "MIN(avg_deal_size_usd)", "AVG(avg_deal_size_usd)", "MAX(avg_deal_size_usd)", "MIN(avg_sales_cycle_days)", "AVG(avg_sales_cycle_days)", "MAX(avg_sales_cycle_days)", "MIN(close_rate_pct)", "AVG(close_rate_pct)", "MAX(close_rate_pct)"] | 1 | 1.1 |
| [S17/Q15](#s17) | success | ["salesforce__customer_360_view", "salesforce__sales_performance_dashboard"] | 3 / {'INNER': 3} | ["owner_id", "owner_id"] | ["COUNT(DISTINCT billing_state)", "COUNT(DISTINCT billing_city)", "COUNT(*)", "SUM(annual_revenue)", "SUM(total_contacts)"] | 20 | 22.705 |
| [S18/Q16](#s18) | success | ["salesforce__customer_360_view", "salesforce__sales_performance_dashboard"] | 4 / {'INNER': 2, 'CROSS': 2} | ["owner_id", "owner_id"] | ["COUNT(DISTINCT billing_state)", "COUNT(DISTINCT billing_city)", "COUNT(*)", "SUM(annual_revenue)", "SUM(total_contacts)", "AVG(workload_score)", "AVG(efficiency_score)", "AVG(ws.workload_score)", "AVG(es.efficiency_score)", "AVG(ws.workload_score)", "AVG(ws.workload_score)", "SUM((ws.workload_score - avg_sub.avg_ws) * (ws.workload_score - avg_sub.avg_ws))", "SUM((es.efficiency_score - avg_sub2.avg_es) * (es.efficiency_score - avg_sub2.avg_es))", "COUNT(*)", "COUNT(*)"] | 1 | 24.34 |
| [S19/Q17](#s19) | success | ["salesforce__customer_360_view", "salesforce__sales_performance_dashboard"] | 3 / {'INNER': 3} | ["owner_id", "owner_id"] | ["COUNT(DISTINCT billing_state)", "COUNT(DISTINCT billing_city)", "COUNT(*)", "SUM(annual_revenue)", "SUM(total_contacts)"] | 1000 | 26.563 |
| [S20/Q18](#s20) | success | ["salesforce__customer_360_view"] | 0 / {} | [] | [] | 20 | 0.447 |
| [S21/Q19](#s21) | success | ["salesforce__customer_360_view"] | 0 / {} | [] | ["COUNT(DISTINCT owner_id)", "COUNT(DISTINCT account_id)"] | 1 | 13.412 |
| [S22/Q20](#s22) | success | ["salesforce__customer_360_view"] | 0 / {} | [] | [] | 10000 | 28.542 |


## 元数据和设置

| SQL | 类别 | 状态 | 内容 |
| --- | --- | --- | --- |
| S1 | connection_setup | success | PRAGMA query_only=ON |
| S2 | metadata | success | SELECT name,sql FROM sqlite_master WHERE type='table' ORDER BY name |


## Python 与执行位置

人工源码审查：**database_first_violation**。同一会话续接后已提交。原轨迹按销售代表进行客户收入、联系人及行业分布聚合可下推 SQL；续接还在 Python 内求基线均值、行业合规计数。重分配搜索及其生成方案的内存状态处理属于算法补充，不能一概判为原库可下推操作。 [证据](../reviews/dacomp-087.json)。

P1：Load rep-level workload/efficiency scores (S19 archive) and all customer rows into Python to design and simulate the reallocation algorithm. The optimization/balancing logic (assignment between donors and receivers, feasibility search, impact simulation) is not reasonably supported by SQLite, so it is done in Python.

[源码](../../../runs/dsv4flash-db-first-full-01/dacomp-087/attempt-01/python/P1.py)；[输出](../../../runs/dsv4flash-db-first-full-01/dacomp-087/attempt-01/python/P1.stdout)；[错误](../../../runs/dsv4flash-db-first-full-01/dacomp-087/attempt-01/python/P1.stderr)。检出需人工核验的 SQL 可实现操作：.query(；不能仅凭理由判为合规。

P2：Fix column names for rep dataframe and compute the summary statistics.

[源码](../../../runs/dsv4flash-db-first-full-01/dacomp-087/attempt-01/python/P2.py)；[输出](../../../runs/dsv4flash-db-first-full-01/dacomp-087/attempt-01/python/P2.stdout)；[错误](../../../runs/dsv4flash-db-first-full-01/dacomp-087/attempt-01/python/P2.stderr)。自动源码筛查未检出预设迁出信号；这不是全面语义合规证明。

P3：Investigate the discrepancy: check duplicate rows in rep data, the opp_conversion_rate outlier (max 13), and null efficiency scores.

[源码](../../../runs/dsv4flash-db-first-full-01/dacomp-087/attempt-01/python/P3.py)；[输出](../../../runs/dsv4flash-db-first-full-01/dacomp-087/attempt-01/python/P3.stdout)；[错误](../../../runs/dsv4flash-db-first-full-01/dacomp-087/attempt-01/python/P3.stderr)。自动源码筛查未检出预设迁出信号；这不是全面语义合规证明。

P4：Design and implement the customer reallocation algorithm. The algorithm uses optimization logic (donor/receiver identification, matching based on geographic proximity, industry expertise, and size suitability) that is not feasible in SQLite. This simulates the reallocation and computes the expected impact.

[源码](../../../runs/dsv4flash-db-first-full-01/dacomp-087/attempt-01/python/P4.py)；[输出](../../../runs/dsv4flash-db-first-full-01/dacomp-087/attempt-01/python/P4.stdout)；[错误](../../../runs/dsv4flash-db-first-full-01/dacomp-087/attempt-01/python/P4.stderr)。检出需人工核验的 SQL 可实现操作：groupby(, sort_values(；不能仅凭理由判为合规。

P5：Refine the reallocation to better handle remaining underloaded reps, and compute the expected impact on efficiency score and customer retention. The optimization and impact simulation are not feasible in SQLite.

[源码](../../../runs/dsv4flash-db-first-full-01/dacomp-087/attempt-01/python/P5.py)；[输出](../../../runs/dsv4flash-db-first-full-01/dacomp-087/attempt-01/python/P5.stdout)；[错误](../../../runs/dsv4flash-db-first-full-01/dacomp-087/attempt-01/python/P5.stderr)。自动源码筛查未检出预设迁出信号；这不是全面语义合规证明。

P6：Check baseline compliance of the 60% top-3-industries rule across all reps, and examine how feasible it is to satisfy. This informs how the reallocation algorithm should enforce the constraint.

[源码](../../../runs/dsv4flash-db-first-full-01/dacomp-087/attempt-01/python/P6.py)；[输出](../../../runs/dsv4flash-db-first-full-01/dacomp-087/attempt-01/python/P6.stdout)；[错误](../../../runs/dsv4flash-db-first-full-01/dacomp-087/attempt-01/python/P6.stderr)。检出需人工核验的 SQL 可实现操作：groupby(；不能仅凭理由判为合规。

P7：Design a refined reallocation algorithm that properly handles the three constraints (geographic proximity, industry expertise match, customer size suitability) and computes impact correctly. This optimization is not feasible in SQL.

[源码](../../../runs/dsv4flash-db-first-full-01/dacomp-087/attempt-01/python/P7.py)；[输出](../../../runs/dsv4flash-db-first-full-01/dacomp-087/attempt-01/python/P7.stdout)；[错误](../../../runs/dsv4flash-db-first-full-01/dacomp-087/attempt-01/python/P7.stderr)。检出需人工核验的 SQL 可实现操作：groupby(, sort_values(；不能仅凭理由判为合规。

P8：Fix data type issues in the reallocation algorithm. The account_id was being read as integer while the transferred account_id is string.

[源码](../../../runs/dsv4flash-db-first-full-01/dacomp-087/attempt-01/python/P8.py)；[输出](../../../runs/dsv4flash-db-first-full-01/dacomp-087/attempt-01/python/P8.stdout)；[错误](../../../runs/dsv4flash-db-first-full-01/dacomp-087/attempt-01/python/P8.stderr)。检出需人工核验的 SQL 可实现操作：groupby(, sort_values(；不能仅凭理由判为合规。

P9：Optimize the reallocation algorithm using precomputed dictionaries instead of repeated DataFrame filtering to avoid timeout.

[源码](../../../runs/dsv4flash-db-first-full-01/dacomp-087/attempt-01/python/P9.py)；[输出](../../../runs/dsv4flash-db-first-full-01/dacomp-087/attempt-01/python/P9.stdout)；[错误](../../../runs/dsv4flash-db-first-full-01/dacomp-087/attempt-01/python/P9.stderr)。检出需人工核验的 SQL 可实现操作：groupby(, sort_values(；不能仅凭理由判为合规。

P10：Evaluate the final portfolio after the proposed transfers: recompute workload scores, check the ±15% constraint, industry compliance, and quantify the efficiency and retention impact.

[源码](../../../runs/dsv4flash-db-first-full-01/dacomp-087/attempt-01/python/P10.py)；[输出](../../../runs/dsv4flash-db-first-full-01/dacomp-087/attempt-01/python/P10.stdout)；[错误](../../../runs/dsv4flash-db-first-full-01/dacomp-087/attempt-01/python/P10.stderr)。检出需人工核验的 SQL 可实现操作：groupby(；不能仅凭理由判为合规。

P11：Fix the evaluation code (clean portfolio construction per rep after transfers) and compute final metrics for the report.

[源码](../../../runs/dsv4flash-db-first-full-01/dacomp-087/attempt-01/python/P11.py)；[输出](../../../runs/dsv4flash-db-first-full-01/dacomp-087/attempt-01/python/P11.stdout)；[错误](../../../runs/dsv4flash-db-first-full-01/dacomp-087/attempt-01/python/P11.stderr)。检出需人工核验的 SQL 可实现操作：groupby(；不能仅凭理由判为合规。

P12：Create a visualization comparing baseline vs final workload distribution for the report.

[源码](../../../runs/dsv4flash-db-first-full-01/dacomp-087/attempt-01/python/P12.py)；[输出](../../../runs/dsv4flash-db-first-full-01/dacomp-087/attempt-01/python/P12.stdout)；[错误](../../../runs/dsv4flash-db-first-full-01/dacomp-087/attempt-01/python/P12.stderr)。自动源码筛查未检出预设迁出信号；这不是全面语义合规证明。

P13：Fix the compliance CSV loading (squeeze is deprecated) and generate the industry compliance figure.

[源码](../../../runs/dsv4flash-db-first-full-01/dacomp-087/attempt-01/python/P13.py)；[输出](../../../runs/dsv4flash-db-first-full-01/dacomp-087/attempt-01/python/P13.stdout)；[错误](../../../runs/dsv4flash-db-first-full-01/dacomp-087/attempt-01/python/P13.stderr)。自动源码筛查未检出预设迁出信号；这不是全面语义合规证明。

P14：Produce a concrete excerpt of the transfer plan (top transfers and summary tables) for the report, plus final workload summary table for a few representative reps.

[源码](../../../runs/dsv4flash-db-first-full-01/dacomp-087/attempt-01/python/P14.py)；[输出](../../../runs/dsv4flash-db-first-full-01/dacomp-087/attempt-01/python/P14.stdout)；[错误](../../../runs/dsv4flash-db-first-full-01/dacomp-087/attempt-01/python/P14.stderr)。检出需人工核验的 SQL 可实现操作：groupby(, sort_values(；不能仅凭理由判为合规。

## 优化机会

已验证候选; original verified selection retained across continuation。筛选限于精确 SQL、相同自包含 CTE、相同单表完整过滤、可分解单表聚合；未覆盖任意 Join 等价和一般谓词蕴含。全部候选都是 offline，未测在线预测。

| 候选 | 类型 | 已有结果 | 覆盖 SQL | 后续次数 | 中间行数 | 验证 | 成本 |
| --- | --- | --- | --- | --- | --- | --- | --- |
| C1 | exact-result reuse | True | ["S7", "S21"] | 1 | unknown | not_verified_cap | Not tested |
| C2 | common subexpression | False | ["S13", "S14", "S17", "S18", "S19"] | 4 | 1000 | verified | Not benchmarked; correctness alone does not establish net speedup. |
| C3 | common subexpression | False | ["S13", "S14", "S17", "S18", "S19"] | 4 | 1000 | verified | Not benchmarked; correctness alone does not establish net speedup. |
| C4 | aggregate MV | False | ["S3", "S10", "S11"] | 2 | 7432 | verified | Not benchmarked; correctness alone does not establish net speedup. |


已验证覆盖（含触发查询、候选并集去重）：8/20 条成功数据 SQL。正确性仅针对当前数据库快照；未测性能的候选不能声称已加速。

[完整 build/rewrite 与比较证据](dacomp-087.analysis.json)。

### C2：common subexpression

Identical self-contained CTE body across queries.

原查询 [S13](#s13), [S14](#s14), [S17](#s17), [S18](#s18), [S19](#s19) → 新增共享状态 C2 → 后续 4 次可复用。该构建点为事后假设，不代表 Agent 当时预知后续。

构建定义：

```sql
SELECT owner_id, COUNT(DISTINCT billing_state) AS distinct_states, COUNT(DISTINCT billing_city) AS distinct_cities FROM salesforce__customer_360_view GROUP BY owner_id
```

受益查询 S13 的改写示例：

```sql
WITH rep_geo AS (SELECT * FROM temp.reuse_candidate), rep_cust AS (SELECT owner_id, COUNT(*) AS num_customers, SUM(annual_revenue) AS total_annual_revenue, SUM(total_contacts) AS total_contacts FROM salesforce__customer_360_view GROUP BY owner_id) SELECT rc.owner_id, rc.num_customers, rc.total_annual_revenue, rc.total_contacts, rg.distinct_states, rg.distinct_cities, rc.num_customers * 0.3 AS term1, (rc.total_annual_revenue / 1000000.0) / 10 * 0.4 AS term2, CASE WHEN CAST(rc.total_contacts AS REAL) / NULLIF(rc.num_customers, 0) > 5 THEN 5 * 0.2 ELSE (CAST(rc.total_contacts AS REAL) / NULLIF(rc.num_customers, 0)) * 0.2 END AS term3, (rg.distinct_states * 2.0 + rg.distinct_cities * 0.5) * 0.1 AS term4, rc.num_customers * 0.3 + (rc.total_annual_revenue / 1000000.0) / 10 * 0.4 + CASE WHEN CAST(rc.total_contacts AS REAL) / NULLIF(rc.num_customers, 0) > 5 THEN 5 * 0.2 ELSE (CAST(rc.total_contacts AS REAL) / NULLIF(rc.num_customers, 0)) * 0.2 END + (rg.distinct_states * 2.0 + rg.distinct_cities * 0.5) * 0.1 AS workload_score FROM rep_cust AS rc JOIN rep_geo AS rg ON rc.owner_id = rg.owner_id ORDER BY workload_score DESC LIMIT 20
```

| 原 SQL | 列名一致 | 结果一致 | 比较方法 |
| --- | --- | --- | --- |
| S13 | True | True | ordered_numeric_tolerance |
| S14 | True | True | exact_multiset |
| S17 | True | True | ordered_numeric_tolerance |
| S18 | True | True | exact_multiset |
| S19 | True | True | ordered_numeric_tolerance |


验证状态：verified；成本结论：Not benchmarked; correctness alone does not establish net speedup.

### C3：common subexpression

Identical self-contained CTE body across queries.

原查询 [S13](#s13), [S14](#s14), [S17](#s17), [S18](#s18), [S19](#s19) → 新增共享状态 C3 → 后续 4 次可复用。该构建点为事后假设，不代表 Agent 当时预知后续。

构建定义：

```sql
SELECT owner_id, COUNT(*) AS num_customers, SUM(annual_revenue) AS total_annual_revenue, SUM(total_contacts) AS total_contacts FROM salesforce__customer_360_view GROUP BY owner_id
```

受益查询 S13 的改写示例：

```sql
WITH rep_geo AS (SELECT owner_id, COUNT(DISTINCT billing_state) AS distinct_states, COUNT(DISTINCT billing_city) AS distinct_cities FROM salesforce__customer_360_view GROUP BY owner_id), rep_cust AS (SELECT * FROM temp.reuse_candidate) SELECT rc.owner_id, rc.num_customers, rc.total_annual_revenue, rc.total_contacts, rg.distinct_states, rg.distinct_cities, rc.num_customers * 0.3 AS term1, (rc.total_annual_revenue / 1000000.0) / 10 * 0.4 AS term2, CASE WHEN CAST(rc.total_contacts AS REAL) / NULLIF(rc.num_customers, 0) > 5 THEN 5 * 0.2 ELSE (CAST(rc.total_contacts AS REAL) / NULLIF(rc.num_customers, 0)) * 0.2 END AS term3, (rg.distinct_states * 2.0 + rg.distinct_cities * 0.5) * 0.1 AS term4, rc.num_customers * 0.3 + (rc.total_annual_revenue / 1000000.0) / 10 * 0.4 + CASE WHEN CAST(rc.total_contacts AS REAL) / NULLIF(rc.num_customers, 0) > 5 THEN 5 * 0.2 ELSE (CAST(rc.total_contacts AS REAL) / NULLIF(rc.num_customers, 0)) * 0.2 END + (rg.distinct_states * 2.0 + rg.distinct_cities * 0.5) * 0.1 AS workload_score FROM rep_cust AS rc JOIN rep_geo AS rg ON rc.owner_id = rg.owner_id ORDER BY workload_score DESC LIMIT 20
```

| 原 SQL | 列名一致 | 结果一致 | 比较方法 |
| --- | --- | --- | --- |
| S13 | True | True | ordered_numeric_tolerance |
| S14 | True | True | exact_multiset |
| S17 | True | True | ordered_numeric_tolerance |
| S18 | True | True | exact_multiset |
| S19 | True | True | ordered_numeric_tolerance |


验证状态：verified；成本结论：Not benchmarked; correctness alone does not establish net speedup.

### C4：aggregate MV

Union of grouping keys; decomposable aggregate states; AVG uses SUM and non-NULL COUNT.

原查询 [S3](#s3), [S10](#s10), [S11](#s11) → 新增共享状态 C4 → 后续 2 次可复用。该构建点为事后假设，不代表 Agent 当时预知后续。

构建定义：

```sql
SELECT industry_normalized AS __g0, owner_id AS __g1, COUNT(*) AS __a0, SUM(annual_revenue) AS __a1, SUM(total_contacts) AS __a2, SUM(total_opportunities) AS __a3, SUM(won_opportunities) AS __a4, SUM(annual_revenue) AS __a5_sum, COUNT(annual_revenue) AS __a5_n FROM "salesforce__customer_360_view"  GROUP BY industry_normalized, owner_id
```

受益查询 S3 的改写示例：

```sql
SELECT SUM(__a0) AS n FROM temp.reuse_candidate
```

| 原 SQL | 列名一致 | 结果一致 | 比较方法 |
| --- | --- | --- | --- |
| S3 | True | True | exact_multiset |
| S10 | True | True | ordered_numeric_tolerance |
| S11 | True | True | ordered_numeric_tolerance |


验证状态：verified；成本结论：Not benchmarked; correctness alone does not establish net speedup.

结果依赖：自动记录 SQL→Python 的接口父调用，以及源码中引用归档文件的消费者；字面值相同不认定因果。模型方向选择需要人工读取消息，尚未做全面因果标注。

[原始报告](../../../runs/dsv4flash-db-first-full-01/dacomp-087/attempt-01/answer.md)；[统一消息](../../../runs/dsv4flash-db-first-full-01/dacomp-087/attempt-01/messages.jsonl)；[原始 OpenCode 事件](../../../runs/dsv4flash-db-first-full-01/dacomp-087/attempt-01/opencode.jsonl)；[SQL 引擎日志](../../../runs/dsv4flash-db-first-full-01/dacomp-087/attempt-01/sql_journal.jsonl)。

[可读报告（本地图片链接规范化）](../answers/dacomp-087.md)。原始回答保留，分析结论未改写。

## S1

类别 `connection_setup`；来源 `connection`；调用 `b00b97e2f4634ac88d27d0043d87d7d6`；状态 `success`。

```sql
PRAGMA query_only=ON
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-087/attempt-01/sql/S1.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-087/attempt-01/sql/S1.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-087/attempt-01/results/S1.rows.jsonl)；完整：True；SHA256：`e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`。

## S2

类别 `metadata`；来源 `list_db`；调用 `b00b97e2f4634ac88d27d0043d87d7d6`；状态 `success`。

```sql
SELECT name,sql FROM sqlite_master WHERE type='table' ORDER BY name
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-087/attempt-01/sql/S2.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-087/attempt-01/sql/S2.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-087/attempt-01/results/S2.rows.jsonl)；完整：True；SHA256：`2479293d93354092294a270d40b60aec6dc40479a519ad0663b950b0d6ca45fa`。

## S3

类别 `data`；来源 `query_db`；调用 `b1784a8bd2d34e6da226c65ade3857db`；状态 `success`。

```sql
SELECT COUNT(*) AS n FROM salesforce__customer_360_view
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-087/attempt-01/sql/S3.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-087/attempt-01/sql/S3.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-087/attempt-01/results/S3.rows.jsonl)；完整：True；SHA256：`aa6d6ae6ca30e188ae245d117135dedb1eec9e98797ddc3dad4f9cec745e2f6d`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "salesforce__customer_360_view", "kind": "base", "block": null, "base_tables": ["salesforce__customer_360_view"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |


## S4

类别 `data`；来源 `query_db`；调用 `0df2ceab7bc3431ea7d02058f7d4b7af`；状态 `success`。

```sql
SELECT COUNT(*) AS n FROM salesforce__sales_performance_dashboard
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-087/attempt-01/sql/S4.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-087/attempt-01/sql/S4.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-087/attempt-01/results/S4.rows.jsonl)；完整：True；SHA256：`e3ed33dc26a723b8481ca677e38dc4a6e8700aeec312afdd02c9dd92374161a2`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "salesforce__sales_performance_dashboard", "kind": "base", "block": null, "base_tables": ["salesforce__sales_performance_dashboard"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |


## S5

类别 `data`；来源 `query_db`；调用 `70584eb33e8843dc951e3dc627a57dda`；状态 `success`。

```sql
SELECT owner_id, rep_name, rep_is_active, rep_role, manager_id, total_revenue_usd, avg_deal_size_usd, win_rate_pct, close_rate_pct, avg_sales_cycle_days, unique_accounts, total_opportunities, won_opportunities, high_value_accounts, territory_coverage FROM salesforce__sales_performance_dashboard LIMIT 20
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-087/attempt-01/sql/S5.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-087/attempt-01/sql/S5.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-087/attempt-01/results/S5.rows.jsonl)；完整：True；SHA256：`d27002dc8d7ce11d9f1ffda570c3046d7c592774376c8e892b614ff1229e1b21`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "salesforce__sales_performance_dashboard", "kind": "base", "block": null, "base_tables": ["salesforce__sales_performance_dashboard"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |


## S6

类别 `data`；来源 `query_db`；调用 `85edb0c6113c4164a37a648d18238558`；状态 `success`。

```sql
SELECT COUNT(DISTINCT owner_id) AS n_reps FROM salesforce__sales_performance_dashboard
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-087/attempt-01/sql/S6.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-087/attempt-01/sql/S6.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-087/attempt-01/results/S6.rows.jsonl)；完整：True；SHA256：`e3ed33dc26a723b8481ca677e38dc4a6e8700aeec312afdd02c9dd92374161a2`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "salesforce__sales_performance_dashboard", "kind": "base", "block": null, "base_tables": ["salesforce__sales_performance_dashboard"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(DISTINCT owner_id) | [{"table": "salesforce__sales_performance_dashboard", "column": "owner_id"}] | [] | False |


## S7

类别 `data`；来源 `query_db`；调用 `276c20daa0a04e41b351894a6bbf31af`；状态 `success`。

```sql
SELECT COUNT(DISTINCT owner_id) AS n_owners, COUNT(DISTINCT account_id) AS n_accts FROM salesforce__customer_360_view
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-087/attempt-01/sql/S7.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-087/attempt-01/sql/S7.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-087/attempt-01/results/S7.rows.jsonl)；完整：True；SHA256：`67768b36ce81296415fcc8f1afd9ef1761e96dc7389de27ca55111b1eeeaaddd`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "salesforce__customer_360_view", "kind": "base", "block": null, "base_tables": ["salesforce__customer_360_view"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(DISTINCT owner_id) | [{"table": "salesforce__customer_360_view", "column": "owner_id"}] | [] | False |
| B1 | COUNT(DISTINCT account_id) | [{"table": "salesforce__customer_360_view", "column": "account_id"}] | [] | False |


## S8

类别 `data`；来源 `query_db`；调用 `3c3cdf4d29984aa199739d7fba8cb402`；状态 `success`。

```sql
SELECT owner_id, account_owner_name, COUNT(*) AS num_customers, 
  SUM(annual_revenue) AS total_revenue,
  ROUND(AVG(annual_revenue), 2) AS avg_revenue,
  SUM(total_contacts) AS total_contacts,
  SUM(total_opportunities) AS total_opps
FROM salesforce__customer_360_view
GROUP BY owner_id
ORDER BY num_customers DESC
LIMIT 20
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-087/attempt-01/sql/S8.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-087/attempt-01/sql/S8.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-087/attempt-01/results/S8.rows.jsonl)；完整：True；SHA256：`60036b8ad492c8a743fea9fc3af73382373d90c54618e2075cec926eeaeef59c`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "salesforce__customer_360_view", "kind": "base", "block": null, "base_tables": ["salesforce__customer_360_view"]}] | [] | ["owner_id"] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |
| B1 | SUM(annual_revenue) | [{"table": "salesforce__customer_360_view", "column": "annual_revenue"}] | [] | False |
| B1 | SUM(total_contacts) | [{"table": "salesforce__customer_360_view", "column": "total_contacts"}] | [] | False |
| B1 | SUM(total_opportunities) | [{"table": "salesforce__customer_360_view", "column": "total_opportunities"}] | [] | False |
| B1 | AVG(annual_revenue) | [{"table": "salesforce__customer_360_view", "column": "annual_revenue"}] | [] | False |


## S9

类别 `data`；来源 `query_db`；调用 `a3bba486d40e40a3bd894a6104b1a32c`；状态 `success`。

```sql
SELECT DISTINCT billing_state FROM salesforce__customer_360_view LIMIT 20
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-087/attempt-01/sql/S9.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-087/attempt-01/sql/S9.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-087/attempt-01/results/S9.rows.jsonl)；完整：True；SHA256：`0f56d0ca677881d696354b025fa90de7bcf21a9c50c42b477109172faa80fe74`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "salesforce__customer_360_view", "kind": "base", "block": null, "base_tables": ["salesforce__customer_360_view"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |


## S10

类别 `data`；来源 `query_db`；调用 `8aea42c0bee14b2da3b9639d0b629af7`；状态 `success`。

```sql
SELECT DISTINCT industry_normalized, COUNT(*) as cnt FROM salesforce__customer_360_view GROUP BY industry_normalized ORDER BY cnt DESC LIMIT 20
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-087/attempt-01/sql/S10.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-087/attempt-01/sql/S10.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-087/attempt-01/results/S10.rows.jsonl)；完整：True；SHA256：`97737f5da193e9ef9ab963cf5a82cdc840874bea82bf52aea26b3163df7ae314`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "salesforce__customer_360_view", "kind": "base", "block": null, "base_tables": ["salesforce__customer_360_view"]}] | [] | ["industry_normalized"] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |


## S11

类别 `data`；来源 `query_db`；调用 `2165620e5beb46da8674bb24c9cfe7ee`；状态 `success`。

```sql
SELECT owner_id, COUNT(*) AS num_customers,
  SUM(annual_revenue) AS total_annual_revenue,
  SUM(total_contacts) AS total_contacts,
  SUM(total_opportunities) AS total_opps,
  SUM(won_opportunities) AS won_opps,
  ROUND(AVG(annual_revenue), 2) AS avg_revenue
FROM salesforce__customer_360_view
GROUP BY owner_id
ORDER BY num_customers DESC
LIMIT 10
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-087/attempt-01/sql/S11.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-087/attempt-01/sql/S11.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-087/attempt-01/results/S11.rows.jsonl)；完整：True；SHA256：`77bf59b99b99053d7a4d9a1f829c4c8b05c16970a8ef0b7ddd904b20d833f5c3`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "salesforce__customer_360_view", "kind": "base", "block": null, "base_tables": ["salesforce__customer_360_view"]}] | [] | ["owner_id"] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |
| B1 | SUM(annual_revenue) | [{"table": "salesforce__customer_360_view", "column": "annual_revenue"}] | [] | False |
| B1 | SUM(total_contacts) | [{"table": "salesforce__customer_360_view", "column": "total_contacts"}] | [] | False |
| B1 | SUM(total_opportunities) | [{"table": "salesforce__customer_360_view", "column": "total_opportunities"}] | [] | False |
| B1 | SUM(won_opportunities) | [{"table": "salesforce__customer_360_view", "column": "won_opportunities"}] | [] | False |
| B1 | AVG(annual_revenue) | [{"table": "salesforce__customer_360_view", "column": "annual_revenue"}] | [] | False |


## S12

类别 `data`；来源 `query_db`；调用 `534bc22a77b64b018f88668dd7cee240`；状态 `success`。

```sql
SELECT owner_id, COUNT(DISTINCT billing_state) AS distinct_states, COUNT(DISTINCT billing_city) AS distinct_cities
FROM salesforce__customer_360_view
GROUP BY owner_id
ORDER BY distinct_states DESC
LIMIT 10
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-087/attempt-01/sql/S12.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-087/attempt-01/sql/S12.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-087/attempt-01/results/S12.rows.jsonl)；完整：True；SHA256：`8a0c918e72cc188aea9de3c96723cdfb8f84b66bce1c4db8dd8c5f38aa67b2db`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "salesforce__customer_360_view", "kind": "base", "block": null, "base_tables": ["salesforce__customer_360_view"]}] | [] | ["owner_id"] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(DISTINCT billing_state) | [{"table": "salesforce__customer_360_view", "column": "billing_state"}] | [] | False |
| B1 | COUNT(DISTINCT billing_city) | [{"table": "salesforce__customer_360_view", "column": "billing_city"}] | [] | False |


## S13

类别 `data`；来源 `query_db`；调用 `3f0391d8b4a3403b948c38d3eaeab04f`；状态 `success`。

```sql
WITH rep_geo AS (
  SELECT owner_id,
    COUNT(DISTINCT billing_state) AS distinct_states,
    COUNT(DISTINCT billing_city) AS distinct_cities
  FROM salesforce__customer_360_view
  GROUP BY owner_id
),
rep_cust AS (
  SELECT owner_id,
    COUNT(*) AS num_customers,
    SUM(annual_revenue) AS total_annual_revenue,
    SUM(total_contacts) AS total_contacts
  FROM salesforce__customer_360_view
  GROUP BY owner_id
)
SELECT rc.owner_id,
  rc.num_customers,
  rc.total_annual_revenue,
  rc.total_contacts,
  rg.distinct_states,
  rg.distinct_cities,
  rc.num_customers * 0.3 AS term1,
  (rc.total_annual_revenue / 1000000.0) / 10 * 0.4 AS term2,
  CASE WHEN CAST(rc.total_contacts AS REAL) / NULLIF(rc.num_customers, 0) > 5 THEN 5 * 0.2
       ELSE (CAST(rc.total_contacts AS REAL) / NULLIF(rc.num_customers, 0)) * 0.2 END AS term3,
  (rg.distinct_states * 2.0 + rg.distinct_cities * 0.5) * 0.1 AS term4,
  rc.num_customers * 0.3 + (rc.total_annual_revenue / 1000000.0) / 10 * 0.4 +
  CASE WHEN CAST(rc.total_contacts AS REAL) / NULLIF(rc.num_customers, 0) > 5 THEN 5 * 0.2
       ELSE (CAST(rc.total_contacts AS REAL) / NULLIF(rc.num_customers, 0)) * 0.2 END +
  (rg.distinct_states * 2.0 + rg.distinct_cities * 0.5) * 0.1 AS workload_score
FROM rep_cust rc
JOIN rep_geo rg ON rc.owner_id = rg.owner_id
ORDER BY workload_score DESC
LIMIT 20
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-087/attempt-01/sql/S13.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-087/attempt-01/sql/S13.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-087/attempt-01/results/S13.rows.jsonl)；完整：True；SHA256：`57bcd110b969f373b76d983044a538a77b44cf2c9cbc760aa5b436b84ec2fbcc`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "salesforce__customer_360_view", "kind": "base", "block": null, "base_tables": ["salesforce__customer_360_view"]}] | [] | ["owner_id"] |
| B2 | [{"alias": "salesforce__customer_360_view", "kind": "base", "block": null, "base_tables": ["salesforce__customer_360_view"]}] | [] | ["owner_id"] |
| B3 | [{"alias": "rc", "kind": "derived", "block": "B2", "base_tables": ["salesforce__customer_360_view"]}, {"alias": "rg", "kind": "derived", "block": "B1", "base_tables": ["salesforce__customer_360_view"]}] | [{"type": "INNER", "right": "rep_geo AS rg", "on": "rc.owner_id = rg.owner_id", "using": []}] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(DISTINCT billing_state) | [{"table": "salesforce__customer_360_view", "column": "billing_state"}] | [] | False |
| B1 | COUNT(DISTINCT billing_city) | [{"table": "salesforce__customer_360_view", "column": "billing_city"}] | [] | False |
| B2 | COUNT(*) | [] | [] | True |
| B2 | SUM(annual_revenue) | [{"table": "salesforce__customer_360_view", "column": "annual_revenue"}] | [] | False |
| B2 | SUM(total_contacts) | [{"table": "salesforce__customer_360_view", "column": "total_contacts"}] | [] | False |


## S14

类别 `data`；来源 `query_db`；调用 `5926311f0403410381a77727a0d455ee`；状态 `success`。

```sql
WITH rep_geo AS (
  SELECT owner_id,
    COUNT(DISTINCT billing_state) AS distinct_states,
    COUNT(DISTINCT billing_city) AS distinct_cities
  FROM salesforce__customer_360_view
  GROUP BY owner_id
),
rep_cust AS (
  SELECT owner_id,
    COUNT(*) AS num_customers,
    SUM(annual_revenue) AS total_annual_revenue,
    SUM(total_contacts) AS total_contacts
  FROM salesforce__customer_360_view
  GROUP BY owner_id
),
scores AS (
  SELECT rc.owner_id,
    rc.num_customers,
    rc.total_annual_revenue,
    rc.total_contacts,
    rg.distinct_states,
    rg.distinct_cities,
    CASE WHEN CAST(rc.total_contacts AS REAL) / NULLIF(rc.num_customers, 0) > 5 THEN 5.0
         ELSE CAST(rc.total_contacts AS REAL) / NULLIF(rc.num_customers, 0) END AS coverage_rate,
    rc.num_customers * 0.3 + (rc.total_annual_revenue / 1000000.0) / 10 * 0.4 +
    CASE WHEN CAST(rc.total_contacts AS REAL) / NULLIF(rc.num_customers, 0) > 5 THEN 5 * 0.2
         ELSE (CAST(rc.total_contacts AS REAL) / NULLIF(rc.num_customers, 0)) * 0.2 END +
    (rg.distinct_states * 2.0 + rg.distinct_cities * 0.5) * 0.1 AS workload_score
  FROM rep_cust rc
  JOIN rep_geo rg ON rc.owner_id = rg.owner_id
)
SELECT 
  COUNT(*) AS n,
  ROUND(AVG(workload_score), 4) AS avg_ws,
  ROUND(AVG(workload_score) * 1.0, 4) AS mean_ws,
  ROUND(SUM((workload_score - (SELECT AVG(workload_score) FROM scores)) * (workload_score - (SELECT AVG(workload_score) FROM scores))) / (COUNT(*) - 1.0), 4) AS variance_ws,
  ROUND(SQRT(SUM((workload_score - (SELECT AVG(workload_score) FROM scores)) * (workload_score - (SELECT AVG(workload_score) FROM scores))) / (COUNT(*) - 1.0)), 4) AS stddev_ws,
  ROUND(MIN(workload_score), 4) AS min_ws,
  ROUND(MAX(workload_score), 4) AS max_ws,
  ROUND((SELECT AVG(workload_score) FROM scores) * 0.3, 4) AS threshold
FROM scores
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-087/attempt-01/sql/S14.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-087/attempt-01/sql/S14.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-087/attempt-01/results/S14.rows.jsonl)；完整：True；SHA256：`59a10ecbce2b909fff33b85fa19d9e20e1950238a0859eb36b36d0502eca8828`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "salesforce__customer_360_view", "kind": "base", "block": null, "base_tables": ["salesforce__customer_360_view"]}] | [] | ["owner_id"] |
| B2 | [{"alias": "salesforce__customer_360_view", "kind": "base", "block": null, "base_tables": ["salesforce__customer_360_view"]}] | [] | ["owner_id"] |
| B3 | [{"alias": "rc", "kind": "derived", "block": "B2", "base_tables": ["salesforce__customer_360_view"]}, {"alias": "rg", "kind": "derived", "block": "B1", "base_tables": ["salesforce__customer_360_view"]}] | [{"type": "INNER", "right": "rep_geo AS rg", "on": "rc.owner_id = rg.owner_id", "using": []}] | [] |
| B4 | [{"alias": "scores", "kind": "derived", "block": "B3", "base_tables": ["salesforce__customer_360_view"]}] | [] | [] |
| B5 | [{"alias": "scores", "kind": "derived", "block": "B3", "base_tables": ["salesforce__customer_360_view"]}] | [] | [] |
| B6 | [{"alias": "scores", "kind": "derived", "block": "B3", "base_tables": ["salesforce__customer_360_view"]}] | [] | [] |
| B7 | [{"alias": "scores", "kind": "derived", "block": "B3", "base_tables": ["salesforce__customer_360_view"]}] | [] | [] |
| B8 | [{"alias": "scores", "kind": "derived", "block": "B3", "base_tables": ["salesforce__customer_360_view"]}] | [] | [] |
| B9 | [{"alias": "scores", "kind": "derived", "block": "B3", "base_tables": ["salesforce__customer_360_view"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(DISTINCT billing_state) | [{"table": "salesforce__customer_360_view", "column": "billing_state"}] | [] | False |
| B1 | COUNT(DISTINCT billing_city) | [{"table": "salesforce__customer_360_view", "column": "billing_city"}] | [] | False |
| B2 | COUNT(*) | [] | [] | True |
| B2 | SUM(annual_revenue) | [{"table": "salesforce__customer_360_view", "column": "annual_revenue"}] | [] | False |
| B2 | SUM(total_contacts) | [{"table": "salesforce__customer_360_view", "column": "total_contacts"}] | [] | False |
| B4 | AVG(workload_score) | [{"table": "salesforce__customer_360_view", "column": "billing_state"}, {"table": "salesforce__customer_360_view", "column": "billing_city"}, {"table": "salesforce__customer_360_view", "column": "annual_revenue"}, {"table": "salesforce__customer_360_view", "column": "total_contacts"}, {"table": "salesforce__customer_360_view", "column": "total_contacts"}] | [] | False |
| B5 | AVG(workload_score) | [{"table": "salesforce__customer_360_view", "column": "billing_state"}, {"table": "salesforce__customer_360_view", "column": "billing_city"}, {"table": "salesforce__customer_360_view", "column": "annual_revenue"}, {"table": "salesforce__customer_360_view", "column": "total_contacts"}, {"table": "salesforce__customer_360_view", "column": "total_contacts"}] | [] | False |
| B6 | AVG(workload_score) | [{"table": "salesforce__customer_360_view", "column": "billing_state"}, {"table": "salesforce__customer_360_view", "column": "billing_city"}, {"table": "salesforce__customer_360_view", "column": "annual_revenue"}, {"table": "salesforce__customer_360_view", "column": "total_contacts"}, {"table": "salesforce__customer_360_view", "column": "total_contacts"}] | [] | False |
| B7 | AVG(workload_score) | [{"table": "salesforce__customer_360_view", "column": "billing_state"}, {"table": "salesforce__customer_360_view", "column": "billing_city"}, {"table": "salesforce__customer_360_view", "column": "annual_revenue"}, {"table": "salesforce__customer_360_view", "column": "total_contacts"}, {"table": "salesforce__customer_360_view", "column": "total_contacts"}] | [] | False |
| B8 | AVG(workload_score) | [{"table": "salesforce__customer_360_view", "column": "billing_state"}, {"table": "salesforce__customer_360_view", "column": "billing_city"}, {"table": "salesforce__customer_360_view", "column": "annual_revenue"}, {"table": "salesforce__customer_360_view", "column": "total_contacts"}, {"table": "salesforce__customer_360_view", "column": "total_contacts"}] | [] | False |
| B9 | COUNT(*) | [] | [] | True |
| B9 | AVG(workload_score) | [{"table": "salesforce__customer_360_view", "column": "billing_state"}, {"table": "salesforce__customer_360_view", "column": "billing_city"}, {"table": "salesforce__customer_360_view", "column": "annual_revenue"}, {"table": "salesforce__customer_360_view", "column": "total_contacts"}, {"table": "salesforce__customer_360_view", "column": "total_contacts"}] | [] | False |
| B9 | MIN(workload_score) | [{"table": "salesforce__customer_360_view", "column": "billing_state"}, {"table": "salesforce__customer_360_view", "column": "billing_city"}, {"table": "salesforce__customer_360_view", "column": "annual_revenue"}, {"table": "salesforce__customer_360_view", "column": "total_contacts"}, {"table": "salesforce__customer_360_view", "column": "total_contacts"}] | [] | False |
| B9 | MAX(workload_score) | [{"table": "salesforce__customer_360_view", "column": "billing_state"}, {"table": "salesforce__customer_360_view", "column": "billing_city"}, {"table": "salesforce__customer_360_view", "column": "annual_revenue"}, {"table": "salesforce__customer_360_view", "column": "total_contacts"}, {"table": "salesforce__customer_360_view", "column": "total_contacts"}] | [] | False |
| B9 | AVG(workload_score) | [{"table": "salesforce__customer_360_view", "column": "billing_state"}, {"table": "salesforce__customer_360_view", "column": "billing_city"}, {"table": "salesforce__customer_360_view", "column": "annual_revenue"}, {"table": "salesforce__customer_360_view", "column": "total_contacts"}, {"table": "salesforce__customer_360_view", "column": "total_contacts"}] | [] | False |
| B9 | SUM((workload_score - (SELECT AVG(workload_score) FROM scores)) * (workload_score - (SELECT AVG(workload_score) FROM scores))) | [{"table": "salesforce__customer_360_view", "column": "billing_state"}, {"table": "salesforce__customer_360_view", "column": "billing_city"}, {"table": "salesforce__customer_360_view", "column": "annual_revenue"}, {"table": "salesforce__customer_360_view", "column": "total_contacts"}, {"table": "salesforce__customer_360_view", "column": "total_contacts"}, {"table": "salesforce__customer_360_view", "column": "billing_state"}, {"table": "salesforce__customer_360_view", "column": "billing_city"}, {"table": "salesforce__customer_360_view", "column": "annual_revenue"}, {"table": "salesforce__customer_360_view", "column": "total_contacts"}, {"table": "salesforce__customer_360_view", "column": "total_contacts"}, {"table": "salesforce__customer_360_view", "column": "billing_state"}, {"table": "salesforce__customer_360_view", "column": "billing_city"}, {"table": "salesforce__customer_360_view", "column": "annual_revenue"}, {"table": "salesforce__customer_360_view", "column": "total_contacts"}, {"table": "salesforce__customer_360_view", "column": "total_contacts"}, {"table": "salesforce__customer_360_view", "column": "billing_state"}, {"table": "salesforce__customer_360_view", "column": "billing_city"}, {"table": "salesforce__customer_360_view", "column": "annual_revenue"}, {"table": "salesforce__customer_360_view", "column": "total_contacts"}, {"table": "salesforce__customer_360_view", "column": "total_contacts"}] | [] | False |
| B9 | SUM((workload_score - (SELECT AVG(workload_score) FROM scores)) * (workload_score - (SELECT AVG(workload_score) FROM scores))) | [{"table": "salesforce__customer_360_view", "column": "billing_state"}, {"table": "salesforce__customer_360_view", "column": "billing_city"}, {"table": "salesforce__customer_360_view", "column": "annual_revenue"}, {"table": "salesforce__customer_360_view", "column": "total_contacts"}, {"table": "salesforce__customer_360_view", "column": "total_contacts"}, {"table": "salesforce__customer_360_view", "column": "billing_state"}, {"table": "salesforce__customer_360_view", "column": "billing_city"}, {"table": "salesforce__customer_360_view", "column": "annual_revenue"}, {"table": "salesforce__customer_360_view", "column": "total_contacts"}, {"table": "salesforce__customer_360_view", "column": "total_contacts"}, {"table": "salesforce__customer_360_view", "column": "billing_state"}, {"table": "salesforce__customer_360_view", "column": "billing_city"}, {"table": "salesforce__customer_360_view", "column": "annual_revenue"}, {"table": "salesforce__customer_360_view", "column": "total_contacts"}, {"table": "salesforce__customer_360_view", "column": "total_contacts"}, {"table": "salesforce__customer_360_view", "column": "billing_state"}, {"table": "salesforce__customer_360_view", "column": "billing_city"}, {"table": "salesforce__customer_360_view", "column": "annual_revenue"}, {"table": "salesforce__customer_360_view", "column": "total_contacts"}, {"table": "salesforce__customer_360_view", "column": "total_contacts"}] | [] | False |
| B9 | COUNT(*) | [] | [] | True |
| B9 | COUNT(*) | [] | [] | True |


## S15

类别 `data`；来源 `query_db`；调用 `efd8f16805b54cf49e7028d29364a398`；状态 `success`。

```sql
SELECT owner_id, rep_name, manager_id, win_rate_pct, avg_deal_size_usd, avg_sales_cycle_days, close_rate_pct, won_opportunities, total_opportunities
FROM salesforce__sales_performance_dashboard
LIMIT 10
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-087/attempt-01/sql/S15.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-087/attempt-01/sql/S15.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-087/attempt-01/results/S15.rows.jsonl)；完整：True；SHA256：`6d0a56a8bd8f84cd7bc15357a20be270b65e2b638e90c058b5cd0c7880b4643e`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "salesforce__sales_performance_dashboard", "kind": "base", "block": null, "base_tables": ["salesforce__sales_performance_dashboard"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |


## S16

类别 `data`；来源 `query_db`；调用 `1f2d17f21ade4bb6bdbfb972dcd50db1`；状态 `success`。

```sql
SELECT MIN(win_rate_pct), AVG(win_rate_pct), MAX(win_rate_pct), MIN(avg_deal_size_usd), AVG(avg_deal_size_usd), MAX(avg_deal_size_usd), MIN(avg_sales_cycle_days), AVG(avg_sales_cycle_days), MAX(avg_sales_cycle_days), MIN(close_rate_pct), AVG(close_rate_pct), MAX(close_rate_pct) FROM salesforce__sales_performance_dashboard
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-087/attempt-01/sql/S16.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-087/attempt-01/sql/S16.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-087/attempt-01/results/S16.rows.jsonl)；完整：True；SHA256：`433f11533ce14c3bd8bc2f579a2d5bb4ab6e7152d3034641e54ac70b4d8d9326`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "salesforce__sales_performance_dashboard", "kind": "base", "block": null, "base_tables": ["salesforce__sales_performance_dashboard"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | MIN(win_rate_pct) | [{"table": "salesforce__sales_performance_dashboard", "column": "win_rate_pct"}] | [] | False |
| B1 | AVG(win_rate_pct) | [{"table": "salesforce__sales_performance_dashboard", "column": "win_rate_pct"}] | [] | False |
| B1 | MAX(win_rate_pct) | [{"table": "salesforce__sales_performance_dashboard", "column": "win_rate_pct"}] | [] | False |
| B1 | MIN(avg_deal_size_usd) | [{"table": "salesforce__sales_performance_dashboard", "column": "avg_deal_size_usd"}] | [] | False |
| B1 | AVG(avg_deal_size_usd) | [{"table": "salesforce__sales_performance_dashboard", "column": "avg_deal_size_usd"}] | [] | False |
| B1 | MAX(avg_deal_size_usd) | [{"table": "salesforce__sales_performance_dashboard", "column": "avg_deal_size_usd"}] | [] | False |
| B1 | MIN(avg_sales_cycle_days) | [{"table": "salesforce__sales_performance_dashboard", "column": "avg_sales_cycle_days"}] | [] | False |
| B1 | AVG(avg_sales_cycle_days) | [{"table": "salesforce__sales_performance_dashboard", "column": "avg_sales_cycle_days"}] | [] | False |
| B1 | MAX(avg_sales_cycle_days) | [{"table": "salesforce__sales_performance_dashboard", "column": "avg_sales_cycle_days"}] | [] | False |
| B1 | MIN(close_rate_pct) | [{"table": "salesforce__sales_performance_dashboard", "column": "close_rate_pct"}] | [] | False |
| B1 | AVG(close_rate_pct) | [{"table": "salesforce__sales_performance_dashboard", "column": "close_rate_pct"}] | [] | False |
| B1 | MAX(close_rate_pct) | [{"table": "salesforce__sales_performance_dashboard", "column": "close_rate_pct"}] | [] | False |


## S17

类别 `data`；来源 `query_db`；调用 `64d152ed46fb48c385d71aceaea0a99f`；状态 `success`。

```sql
WITH rep_geo AS (
  SELECT owner_id,
    COUNT(DISTINCT billing_state) AS distinct_states,
    COUNT(DISTINCT billing_city) AS distinct_cities
  FROM salesforce__customer_360_view
  GROUP BY owner_id
),
rep_cust AS (
  SELECT owner_id,
    COUNT(*) AS num_customers,
    SUM(annual_revenue) AS total_annual_revenue,
    SUM(total_contacts) AS total_contacts
  FROM salesforce__customer_360_view
  GROUP BY owner_id
),
workload_scores AS (
  SELECT rc.owner_id,
    rc.num_customers,
    rc.total_annual_revenue,
    rc.total_contacts,
    rg.distinct_states,
    rg.distinct_cities,
    CASE WHEN CAST(rc.total_contacts AS REAL) / NULLIF(rc.num_customers, 0) > 5 THEN 5.0
         ELSE CAST(rc.total_contacts AS REAL) / NULLIF(rc.num_customers, 0) END AS coverage_rate_capped,
    rc.num_customers * 0.3 + (rc.total_annual_revenue / 1000000.0) / 10 * 0.4 +
    CASE WHEN CAST(rc.total_contacts AS REAL) / NULLIF(rc.num_customers, 0) > 5 THEN 5 * 0.2
         ELSE (CAST(rc.total_contacts AS REAL) / NULLIF(rc.num_customers, 0)) * 0.2 END +
    (rg.distinct_states * 2.0 + rg.distinct_cities * 0.5) * 0.1 AS workload_score
  FROM rep_cust rc
  JOIN rep_geo rg ON rc.owner_id = rg.owner_id
),
efficiency_scores AS (
  SELECT spd.owner_id,
    spd.rep_name,
    spd.win_rate_pct / 100.0 AS win_rate,
    spd.avg_deal_size_usd,
    spd.avg_sales_cycle_days,
    spd.close_rate_pct / 100.0 AS opp_conversion_rate,
    spd.win_rate_pct / 100.0 * 0.4 + (spd.avg_deal_size_usd / 100000.0) * 0.3 + 
    (120.0 / NULLIF(spd.avg_sales_cycle_days, 0)) * 0.2 + (spd.close_rate_pct / 100.0) * 0.1 AS efficiency_score
  FROM salesforce__sales_performance_dashboard spd
)
SELECT ws.owner_id, spd.rep_name,
  ws.workload_score,
  es.efficiency_score,
  es.win_rate, es.avg_deal_size_usd, es.avg_sales_cycle_days, es.opp_conversion_rate,
  ws.num_customers, ws.total_annual_revenue, ws.coverage_rate_capped,
  ws.distinct_states, ws.distinct_cities
FROM workload_scores ws
JOIN efficiency_scores es ON ws.owner_id = es.owner_id
JOIN salesforce__sales_performance_dashboard spd ON ws.owner_id = spd.owner_id
ORDER BY ws.workload_score DESC
LIMIT 20
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-087/attempt-01/sql/S17.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-087/attempt-01/sql/S17.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-087/attempt-01/results/S17.rows.jsonl)；完整：True；SHA256：`077c7c73b102e4f81373a12488827e934702bc48d156079f1de9d93bfcbc1a6a`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "salesforce__customer_360_view", "kind": "base", "block": null, "base_tables": ["salesforce__customer_360_view"]}] | [] | ["owner_id"] |
| B2 | [{"alias": "salesforce__customer_360_view", "kind": "base", "block": null, "base_tables": ["salesforce__customer_360_view"]}] | [] | ["owner_id"] |
| B3 | [{"alias": "rc", "kind": "derived", "block": "B2", "base_tables": ["salesforce__customer_360_view"]}, {"alias": "rg", "kind": "derived", "block": "B1", "base_tables": ["salesforce__customer_360_view"]}] | [{"type": "INNER", "right": "rep_geo AS rg", "on": "rc.owner_id = rg.owner_id", "using": []}] | [] |
| B4 | [{"alias": "spd", "kind": "base", "block": null, "base_tables": ["salesforce__sales_performance_dashboard"]}] | [] | [] |
| B5 | [{"alias": "ws", "kind": "derived", "block": "B3", "base_tables": ["salesforce__customer_360_view"]}, {"alias": "es", "kind": "derived", "block": "B4", "base_tables": ["salesforce__sales_performance_dashboard"]}, {"alias": "spd", "kind": "base", "block": null, "base_tables": ["salesforce__sales_performance_dashboard"]}] | [{"type": "INNER", "right": "efficiency_scores AS es", "on": "ws.owner_id = es.owner_id", "using": []}, {"type": "INNER", "right": "salesforce__sales_performance_dashboard AS spd", "on": "ws.owner_id = spd.owner_id", "using": []}] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(DISTINCT billing_state) | [{"table": "salesforce__customer_360_view", "column": "billing_state"}] | [] | False |
| B1 | COUNT(DISTINCT billing_city) | [{"table": "salesforce__customer_360_view", "column": "billing_city"}] | [] | False |
| B2 | COUNT(*) | [] | [] | True |
| B2 | SUM(annual_revenue) | [{"table": "salesforce__customer_360_view", "column": "annual_revenue"}] | [] | False |
| B2 | SUM(total_contacts) | [{"table": "salesforce__customer_360_view", "column": "total_contacts"}] | [] | False |


## S18

类别 `data`；来源 `query_db`；调用 `68f862848f094638bf7b80bec5a5218c`；状态 `success`。

```sql
WITH rep_geo AS (
  SELECT owner_id,
    COUNT(DISTINCT billing_state) AS distinct_states,
    COUNT(DISTINCT billing_city) AS distinct_cities
  FROM salesforce__customer_360_view
  GROUP BY owner_id
),
rep_cust AS (
  SELECT owner_id,
    COUNT(*) AS num_customers,
    SUM(annual_revenue) AS total_annual_revenue,
    SUM(total_contacts) AS total_contacts
  FROM salesforce__customer_360_view
  GROUP BY owner_id
),
workload_scores AS (
  SELECT rc.owner_id,
    rc.num_customers,
    rc.total_annual_revenue,
    rc.total_contacts,
    rg.distinct_states,
    rg.distinct_cities,
    CASE WHEN CAST(rc.total_contacts AS REAL) / NULLIF(rc.num_customers, 0) > 5 THEN 5.0
         ELSE CAST(rc.total_contacts AS REAL) / NULLIF(rc.num_customers, 0) END AS coverage_rate_capped,
    rc.num_customers * 0.3 + (rc.total_annual_revenue / 1000000.0) / 10 * 0.4 +
    CASE WHEN CAST(rc.total_contacts AS REAL) / NULLIF(rc.num_customers, 0) > 5 THEN 5 * 0.2
         ELSE (CAST(rc.total_contacts AS REAL) / NULLIF(rc.num_customers, 0)) * 0.2 END +
    (rg.distinct_states * 2.0 + rg.distinct_cities * 0.5) * 0.1 AS workload_score
  FROM rep_cust rc
  JOIN rep_geo rg ON rc.owner_id = rg.owner_id
),
efficiency_scores AS (
  SELECT spd.owner_id,
    spd.win_rate_pct / 100.0 * 0.4 + (spd.avg_deal_size_usd / 100000.0) * 0.3 + 
    (120.0 / NULLIF(spd.avg_sales_cycle_days, 0)) * 0.2 + (spd.close_rate_pct / 100.0) * 0.1 AS efficiency_score
  FROM salesforce__sales_performance_dashboard spd
)
SELECT 
  ROUND(AVG(ws.workload_score), 4) AS avg_workload,
  ROUND(SQRT(SUM((ws.workload_score - avg_sub.avg_ws) * (ws.workload_score - avg_sub.avg_ws)) / (COUNT(*) - 1.0)), 4) AS std_workload,
  ROUND(AVG(es.efficiency_score), 4) AS avg_efficiency,
  ROUND(SQRT(SUM((es.efficiency_score - avg_sub2.avg_es) * (es.efficiency_score - avg_sub2.avg_es)) / (COUNT(*) - 1.0)), 4) AS std_efficiency,
  ROUND(AVG(ws.workload_score) * 0.3, 4) AS ws_threshold,
  ROUND(AVG(ws.workload_score) * 0.15, 4) AS ws_15pct
FROM workload_scores ws
CROSS JOIN (SELECT AVG(workload_score) AS avg_ws FROM workload_scores) avg_sub
CROSS JOIN (SELECT AVG(efficiency_score) AS avg_es FROM efficiency_scores) avg_sub2
JOIN efficiency_scores es ON ws.owner_id = es.owner_id
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-087/attempt-01/sql/S18.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-087/attempt-01/sql/S18.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-087/attempt-01/results/S18.rows.jsonl)；完整：True；SHA256：`9d673f8f659f554b1b49d64ed7e614b2c831923be009e32e1f5d82884eb295e7`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "salesforce__customer_360_view", "kind": "base", "block": null, "base_tables": ["salesforce__customer_360_view"]}] | [] | ["owner_id"] |
| B2 | [{"alias": "salesforce__customer_360_view", "kind": "base", "block": null, "base_tables": ["salesforce__customer_360_view"]}] | [] | ["owner_id"] |
| B3 | [{"alias": "rc", "kind": "derived", "block": "B2", "base_tables": ["salesforce__customer_360_view"]}, {"alias": "rg", "kind": "derived", "block": "B1", "base_tables": ["salesforce__customer_360_view"]}] | [{"type": "INNER", "right": "rep_geo AS rg", "on": "rc.owner_id = rg.owner_id", "using": []}] | [] |
| B4 | [{"alias": "spd", "kind": "base", "block": null, "base_tables": ["salesforce__sales_performance_dashboard"]}] | [] | [] |
| B5 | [{"alias": "workload_scores", "kind": "derived", "block": "B3", "base_tables": ["salesforce__customer_360_view"]}] | [] | [] |
| B6 | [{"alias": "efficiency_scores", "kind": "derived", "block": "B4", "base_tables": ["salesforce__sales_performance_dashboard"]}] | [] | [] |
| B7 | [{"alias": "ws", "kind": "derived", "block": "B3", "base_tables": ["salesforce__customer_360_view"]}, {"alias": "avg_sub", "kind": "derived", "block": "B5", "base_tables": ["salesforce__customer_360_view"]}, {"alias": "avg_sub2", "kind": "derived", "block": "B6", "base_tables": ["salesforce__sales_performance_dashboard"]}, {"alias": "es", "kind": "derived", "block": "B4", "base_tables": ["salesforce__sales_performance_dashboard"]}] | [{"type": "CROSS", "right": "(SELECT AVG(workload_score) AS avg_ws FROM workload_scores) AS avg_sub", "on": null, "using": []}, {"type": "CROSS", "right": "(SELECT AVG(efficiency_score) AS avg_es FROM efficiency_scores) AS avg_sub2", "on": null, "using": []}, {"type": "INNER", "right": "efficiency_scores AS es", "on": "ws.owner_id = es.owner_id", "using": []}] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(DISTINCT billing_state) | [{"table": "salesforce__customer_360_view", "column": "billing_state"}] | [] | False |
| B1 | COUNT(DISTINCT billing_city) | [{"table": "salesforce__customer_360_view", "column": "billing_city"}] | [] | False |
| B2 | COUNT(*) | [] | [] | True |
| B2 | SUM(annual_revenue) | [{"table": "salesforce__customer_360_view", "column": "annual_revenue"}] | [] | False |
| B2 | SUM(total_contacts) | [{"table": "salesforce__customer_360_view", "column": "total_contacts"}] | [] | False |
| B5 | AVG(workload_score) | [{"table": "salesforce__customer_360_view", "column": "billing_state"}, {"table": "salesforce__customer_360_view", "column": "billing_city"}, {"table": "salesforce__customer_360_view", "column": "annual_revenue"}, {"table": "salesforce__customer_360_view", "column": "total_contacts"}, {"table": "salesforce__customer_360_view", "column": "total_contacts"}] | [] | False |
| B6 | AVG(efficiency_score) | [{"table": "salesforce__sales_performance_dashboard", "column": "close_rate_pct"}, {"table": "salesforce__sales_performance_dashboard", "column": "win_rate_pct"}, {"table": "salesforce__sales_performance_dashboard", "column": "avg_deal_size_usd"}, {"table": "salesforce__sales_performance_dashboard", "column": "avg_sales_cycle_days"}] | [] | False |
| B7 | AVG(ws.workload_score) | [{"table": "salesforce__customer_360_view", "column": "billing_state"}, {"table": "salesforce__customer_360_view", "column": "billing_city"}, {"table": "salesforce__customer_360_view", "column": "annual_revenue"}, {"table": "salesforce__customer_360_view", "column": "total_contacts"}, {"table": "salesforce__customer_360_view", "column": "total_contacts"}] | [] | False |
| B7 | AVG(es.efficiency_score) | [{"table": "salesforce__sales_performance_dashboard", "column": "close_rate_pct"}, {"table": "salesforce__sales_performance_dashboard", "column": "win_rate_pct"}, {"table": "salesforce__sales_performance_dashboard", "column": "avg_deal_size_usd"}, {"table": "salesforce__sales_performance_dashboard", "column": "avg_sales_cycle_days"}] | [] | False |
| B7 | AVG(ws.workload_score) | [{"table": "salesforce__customer_360_view", "column": "billing_state"}, {"table": "salesforce__customer_360_view", "column": "billing_city"}, {"table": "salesforce__customer_360_view", "column": "annual_revenue"}, {"table": "salesforce__customer_360_view", "column": "total_contacts"}, {"table": "salesforce__customer_360_view", "column": "total_contacts"}] | [] | False |
| B7 | AVG(ws.workload_score) | [{"table": "salesforce__customer_360_view", "column": "billing_state"}, {"table": "salesforce__customer_360_view", "column": "billing_city"}, {"table": "salesforce__customer_360_view", "column": "annual_revenue"}, {"table": "salesforce__customer_360_view", "column": "total_contacts"}, {"table": "salesforce__customer_360_view", "column": "total_contacts"}] | [] | False |
| B7 | SUM((ws.workload_score - avg_sub.avg_ws) * (ws.workload_score - avg_sub.avg_ws)) | [{"table": "salesforce__customer_360_view", "column": "billing_state"}, {"table": "salesforce__customer_360_view", "column": "billing_city"}, {"table": "salesforce__customer_360_view", "column": "annual_revenue"}, {"table": "salesforce__customer_360_view", "column": "total_contacts"}, {"table": "salesforce__customer_360_view", "column": "total_contacts"}, {"table": "salesforce__customer_360_view", "column": "billing_state"}, {"table": "salesforce__customer_360_view", "column": "billing_city"}, {"table": "salesforce__customer_360_view", "column": "annual_revenue"}, {"table": "salesforce__customer_360_view", "column": "total_contacts"}, {"table": "salesforce__customer_360_view", "column": "total_contacts"}, {"table": "salesforce__customer_360_view", "column": "billing_state"}, {"table": "salesforce__customer_360_view", "column": "billing_city"}, {"table": "salesforce__customer_360_view", "column": "annual_revenue"}, {"table": "salesforce__customer_360_view", "column": "total_contacts"}, {"table": "salesforce__customer_360_view", "column": "total_contacts"}, {"table": "salesforce__customer_360_view", "column": "billing_state"}, {"table": "salesforce__customer_360_view", "column": "billing_city"}, {"table": "salesforce__customer_360_view", "column": "annual_revenue"}, {"table": "salesforce__customer_360_view", "column": "total_contacts"}, {"table": "salesforce__customer_360_view", "column": "total_contacts"}] | [] | False |
| B7 | SUM((es.efficiency_score - avg_sub2.avg_es) * (es.efficiency_score - avg_sub2.avg_es)) | [{"table": "salesforce__sales_performance_dashboard", "column": "close_rate_pct"}, {"table": "salesforce__sales_performance_dashboard", "column": "win_rate_pct"}, {"table": "salesforce__sales_performance_dashboard", "column": "avg_deal_size_usd"}, {"table": "salesforce__sales_performance_dashboard", "column": "avg_sales_cycle_days"}, {"table": "salesforce__sales_performance_dashboard", "column": "close_rate_pct"}, {"table": "salesforce__sales_performance_dashboard", "column": "win_rate_pct"}, {"table": "salesforce__sales_performance_dashboard", "column": "avg_deal_size_usd"}, {"table": "salesforce__sales_performance_dashboard", "column": "avg_sales_cycle_days"}, {"table": "salesforce__sales_performance_dashboard", "column": "close_rate_pct"}, {"table": "salesforce__sales_performance_dashboard", "column": "win_rate_pct"}, {"table": "salesforce__sales_performance_dashboard", "column": "avg_deal_size_usd"}, {"table": "salesforce__sales_performance_dashboard", "column": "avg_sales_cycle_days"}, {"table": "salesforce__sales_performance_dashboard", "column": "close_rate_pct"}, {"table": "salesforce__sales_performance_dashboard", "column": "win_rate_pct"}, {"table": "salesforce__sales_performance_dashboard", "column": "avg_deal_size_usd"}, {"table": "salesforce__sales_performance_dashboard", "column": "avg_sales_cycle_days"}] | [] | False |
| B7 | COUNT(*) | [] | [] | True |
| B7 | COUNT(*) | [] | [] | True |


## S19

类别 `data`；来源 `query_db`；调用 `2bf5f5b7cde54b629f0c231bf6e5e205`；状态 `success`。

```sql
WITH rep_geo AS (
  SELECT owner_id,
    COUNT(DISTINCT billing_state) AS distinct_states,
    COUNT(DISTINCT billing_city) AS distinct_cities
  FROM salesforce__customer_360_view
  GROUP BY owner_id
),
rep_cust AS (
  SELECT owner_id,
    COUNT(*) AS num_customers,
    SUM(annual_revenue) AS total_annual_revenue,
    SUM(total_contacts) AS total_contacts
  FROM salesforce__customer_360_view
  GROUP BY owner_id
),
workload_scores AS (
  SELECT rc.owner_id,
    rc.num_customers,
    rc.total_annual_revenue,
    rc.total_contacts,
    rg.distinct_states,
    rg.distinct_cities,
    CASE WHEN CAST(rc.total_contacts AS REAL) / NULLIF(rc.num_customers, 0) > 5 THEN 5.0
         ELSE CAST(rc.total_contacts AS REAL) / NULLIF(rc.num_customers, 0) END AS coverage_rate_capped,
    rc.num_customers * 0.3 + (rc.total_annual_revenue / 1000000.0) / 10 * 0.4 +
    CASE WHEN CAST(rc.total_contacts AS REAL) / NULLIF(rc.num_customers, 0) > 5 THEN 5 * 0.2
         ELSE (CAST(rc.total_contacts AS REAL) / NULLIF(rc.num_customers, 0)) * 0.2 END +
    (rg.distinct_states * 2.0 + rg.distinct_cities * 0.5) * 0.1 AS workload_score
  FROM rep_cust rc
  JOIN rep_geo rg ON rc.owner_id = rg.owner_id
),
efficiency_scores AS (
  SELECT spd.owner_id, spd.rep_name, spd.manager_id,
    spd.win_rate_pct / 100.0 AS win_rate,
    spd.avg_deal_size_usd,
    spd.avg_sales_cycle_days,
    spd.close_rate_pct / 100.0 AS opp_conversion_rate,
    spd.win_rate_pct / 100.0 * 0.4 + (spd.avg_deal_size_usd / 100000.0) * 0.3 + 
    (120.0 / NULLIF(spd.avg_sales_cycle_days, 0)) * 0.2 + (spd.close_rate_pct / 100.0) * 0.1 AS efficiency_score
  FROM salesforce__sales_performance_dashboard spd
)
SELECT ws.owner_id, spd.rep_name, spd.manager_id,
  ws.workload_score, es.efficiency_score,
  ws.num_customers, ws.total_annual_revenue, ws.coverage_rate_capped,
  ws.distinct_states, ws.distinct_cities,
  es.win_rate, es.avg_deal_size_usd, es.avg_sales_cycle_days, es.opp_conversion_rate
FROM workload_scores ws
JOIN efficiency_scores es ON ws.owner_id = es.owner_id
JOIN salesforce__sales_performance_dashboard spd ON ws.owner_id = spd.owner_id
ORDER BY ws.workload_score DESC
LIMIT 1000
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-087/attempt-01/sql/S19.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-087/attempt-01/sql/S19.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-087/attempt-01/results/S19.rows.jsonl)；完整：True；SHA256：`72fdbd68b02c5dd74b93f51e87f982e074290aa5e017ec8c84a6bf10a7bd7dd5`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "salesforce__customer_360_view", "kind": "base", "block": null, "base_tables": ["salesforce__customer_360_view"]}] | [] | ["owner_id"] |
| B2 | [{"alias": "salesforce__customer_360_view", "kind": "base", "block": null, "base_tables": ["salesforce__customer_360_view"]}] | [] | ["owner_id"] |
| B3 | [{"alias": "rc", "kind": "derived", "block": "B2", "base_tables": ["salesforce__customer_360_view"]}, {"alias": "rg", "kind": "derived", "block": "B1", "base_tables": ["salesforce__customer_360_view"]}] | [{"type": "INNER", "right": "rep_geo AS rg", "on": "rc.owner_id = rg.owner_id", "using": []}] | [] |
| B4 | [{"alias": "spd", "kind": "base", "block": null, "base_tables": ["salesforce__sales_performance_dashboard"]}] | [] | [] |
| B5 | [{"alias": "ws", "kind": "derived", "block": "B3", "base_tables": ["salesforce__customer_360_view"]}, {"alias": "es", "kind": "derived", "block": "B4", "base_tables": ["salesforce__sales_performance_dashboard"]}, {"alias": "spd", "kind": "base", "block": null, "base_tables": ["salesforce__sales_performance_dashboard"]}] | [{"type": "INNER", "right": "efficiency_scores AS es", "on": "ws.owner_id = es.owner_id", "using": []}, {"type": "INNER", "right": "salesforce__sales_performance_dashboard AS spd", "on": "ws.owner_id = spd.owner_id", "using": []}] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(DISTINCT billing_state) | [{"table": "salesforce__customer_360_view", "column": "billing_state"}] | [] | False |
| B1 | COUNT(DISTINCT billing_city) | [{"table": "salesforce__customer_360_view", "column": "billing_city"}] | [] | False |
| B2 | COUNT(*) | [] | [] | True |
| B2 | SUM(annual_revenue) | [{"table": "salesforce__customer_360_view", "column": "annual_revenue"}] | [] | False |
| B2 | SUM(total_contacts) | [{"table": "salesforce__customer_360_view", "column": "total_contacts"}] | [] | False |


## S20

类别 `data`；来源 `query_db`；调用 `b11ae0537a43445080e271f0f16a2e4a`；状态 `success`。

```sql
SELECT c.owner_id, c.account_id, c.account_name, c.annual_revenue, c.billing_state, c.billing_city, c.industry_normalized, c.account_size_segment, c.total_contacts, c.number_of_employees, c.total_opportunities, c.won_opportunities, c.win_rate_percentage
FROM salesforce__customer_360_view c
LIMIT 20
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-087/attempt-01/sql/S20.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-087/attempt-01/sql/S20.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-087/attempt-01/results/S20.rows.jsonl)；完整：True；SHA256：`f8ebb6f50fd521059ec2727e03670ceb770a7dcdffe89e6fbebcdb71dd3cbb11`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "c", "kind": "base", "block": null, "base_tables": ["salesforce__customer_360_view"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |


## S21

类别 `data`；来源 `query_db`；调用 `3b2156c4949a4381b13e4e1eccb120ac`；状态 `success`。

```sql
SELECT COUNT(DISTINCT owner_id) AS n_owners, COUNT(DISTINCT account_id) AS n_accts FROM salesforce__customer_360_view
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-087/attempt-01/sql/S21.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-087/attempt-01/sql/S21.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-087/attempt-01/results/S21.rows.jsonl)；完整：True；SHA256：`67768b36ce81296415fcc8f1afd9ef1761e96dc7389de27ca55111b1eeeaaddd`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "salesforce__customer_360_view", "kind": "base", "block": null, "base_tables": ["salesforce__customer_360_view"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(DISTINCT owner_id) | [{"table": "salesforce__customer_360_view", "column": "owner_id"}] | [] | False |
| B1 | COUNT(DISTINCT account_id) | [{"table": "salesforce__customer_360_view", "column": "account_id"}] | [] | False |


## S22

类别 `data`；来源 `python`；调用 `e9becb3764034a9282e3f745afa48cda`；状态 `success`。

```sql
SELECT owner_id, account_id, account_name, annual_revenue, billing_state, billing_city, industry_normalized, account_size_segment, total_contacts, number_of_employees, total_opportunities, won_opportunities, win_rate_percentage FROM salesforce__customer_360_view
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-087/attempt-01/sql/S22.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-087/attempt-01/sql/S22.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-087/attempt-01/results/S22.rows.jsonl)；完整：True；SHA256：`2f30f01c45f9e54edb4c6d6dc10cff2197d7dc277c0c13a7565836deef8cc22c`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "salesforce__customer_360_view", "kind": "base", "block": null, "base_tables": ["salesforce__customer_360_view"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |

