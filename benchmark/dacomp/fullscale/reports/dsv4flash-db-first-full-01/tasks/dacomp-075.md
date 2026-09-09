# dacomp-075

In the context of increasing uncertainty in the current global supply chain, our company i…

运行：已提交。官方未评分。全部 SQL 尝试/成功 29/29；数据 SQL 27/27；Python 8 次。

完整原题：

In the context of increasing uncertainty in the current global supply chain, our company is facing unprecedented vendor resilience challenges. Please design and implement a multi-dimensional vendor resilience assessment framework, focusing on the group of vendors where `spend_concentration_ratio` exceeds 15% or are classified as 'Mission Critical'/'High Strategic Value'. Your analysis should integrate four core dimensions: Financial Resilience (payment performance, financial health), Operational Resilience (quality performance, cybersecurity capability, innovation capability), Market Resilience (market volatility sensitivity, alternative supplier availability, price volatility risk), and Strategic Resilience (geographic distribution risk, contract expiry risk, environmental sustainability). At the same time, please create a dynamic risk warning mechanism capable of identifying high-risk scenarios of potential supply disruption within the next 12-18 months, and formulate personalized resilience improvement paths and contingency plans for each identified key vendor. Finally, please quantitatively analyze the return on investment (ROI) of different resilience improvement strategies to provide senior management with data-driven recommendations for vendor portfolio optimization.

| 表 | 行数 | 列数 |
| --- | --- | --- |
| netsuite2_vendor_risk_analysis | 93 | 49 |


实际路线（分析者依据 SQL/源码概括，不代表 Agent 自述）：SQL 筛选关键供应商 → Python 构建韧性分数、预警及 ROI 情景并连接策略 → 供应商改进计划。

数据库大小：65,536 字节。

## 数据 SQL

| SQL | 状态 | 基础表 | Join 输入/类型 | GROUP BY | 聚合表达式 | 结果行数 | 数据库 ms |
| --- | --- | --- | --- | --- | --- | --- | --- |
| [S3/Q1](#s3) | success | ["netsuite2_vendor_risk_analysis"] | 0 / {} | [] | ["COUNT(*)", "COUNT(DISTINCT vendor_id)"] | 1 | 0.382 |
| [S4/Q2](#s4) | success | ["netsuite2_vendor_risk_analysis"] | 0 / {} | [] | [] | 5 | 0.69 |
| [S5/Q3](#s5) | success | ["netsuite2_vendor_risk_analysis"] | 0 / {} | [] | [] | 8 | 0.365 |
| [S6/Q4](#s6) | success | ["netsuite2_vendor_risk_analysis"] | 0 / {} | [] | [] | 3 | 0.328 |
| [S7/Q5](#s7) | success | ["netsuite2_vendor_risk_analysis"] | 0 / {} | [] | [] | 4 | 0.325 |
| [S8/Q6](#s8) | success | ["netsuite2_vendor_risk_analysis"] | 0 / {} | [] | [] | 6 | 0.361 |
| [S9/Q7](#s9) | success | ["netsuite2_vendor_risk_analysis"] | 0 / {} | [] | [] | 6 | 0.353 |
| [S10/Q8](#s10) | success | ["netsuite2_vendor_risk_analysis"] | 0 / {} | [] | [] | 1 | 0.345 |
| [S11/Q9](#s11) | success | ["netsuite2_vendor_risk_analysis"] | 0 / {} | [] | [] | 6 | 0.367 |
| [S12/Q10](#s12) | success | ["netsuite2_vendor_risk_analysis"] | 0 / {} | [] | [] | 5 | 0.368 |
| [S13/Q11](#s13) | success | ["netsuite2_vendor_risk_analysis"] | 0 / {} | [] | [] | 6 | 0.364 |
| [S14/Q12](#s14) | success | ["netsuite2_vendor_risk_analysis"] | 0 / {} | [] | ["SUM(CASE WHEN spend_concentration_ratio > 0.15 OR strategic_importance_level IN ('Mission Critical', 'High Strategic Value') THEN 1 ELSE 0 END)", "SUM(CASE WHEN spend_concentration_ratio > 0.15 THEN 1 ELSE 0 END)", "SUM(CASE WHEN strategic_importance_level IN ('Mission Critical', 'High Strategic Value') THEN 1 ELSE 0 END)"] | 1 | 0.416 |
| [S15/Q13](#s15) | success | ["netsuite2_vendor_risk_analysis"] | 0 / {} | ["strategic_importance_level"] | ["COUNT(*)"] | 4 | 0.426 |
| [S16/Q14](#s16) | success | ["netsuite2_vendor_risk_analysis"] | 0 / {} | ["risk_level"] | ["COUNT(*)"] | 3 | 0.411 |
| [S17/Q15](#s17) | success | ["netsuite2_vendor_risk_analysis"] | 0 / {} | [] | ["MIN(analysis_date)", "MAX(analysis_date)", "MIN(contract_expiry_date)", "MAX(contract_expiry_date)", "MIN(first_transaction_date)", "MAX(last_transaction_date)"] | 1 | 0.418 |
| [S18/Q16](#s18) | success | ["netsuite2_vendor_risk_analysis"] | 0 / {} | [] | [] | 91 | 1.443 |
| [S19/Q17](#s19) | success | ["netsuite2_vendor_risk_analysis"] | 0 / {} | [] | ["MIN(quality_score)", "MAX(quality_score)", "AVG(quality_score)", "AVG(CAST(quality_score AS REAL))", "MIN(financial_health_score)", "MAX(financial_health_score)", "AVG(financial_health_score)", "AVG(CAST(financial_health_score AS REAL))", "MIN(innovation_capability_score)", "MAX(innovation_capability_score)", "AVG(innovation_capability_score)", "AVG(CAST(innovation_capability_score AS REAL))", "MIN(cybersecurity_score)", "MAX(cybersecurity_score)", "AVG(cybersecurity_score)", "AVG(CAST(cybersecurity_score AS REAL))", "MIN(market_volatility_index)", "MAX(market_volatility_index)", "AVG(market_volatility_index)", "AVG(CAST(market_volatility_index AS REAL))", "MIN(alternative_suppliers_count)", "MAX(alternative_suppliers_count)", "AVG(alternative_suppliers_count)", "AVG(CAST(alternative_suppliers_count AS REAL))", "MIN(price_volatility_coefficient)", "MAX(price_volatility_coefficient)", "AVG(price_volatility_coefficient)", "AVG(CAST(price_volatility_coefficient AS REAL))", "MIN(avg_payment_delay)", "MAX(avg_payment_delay)", "AVG(avg_payment_delay)", "AVG(CAST(avg_payment_delay AS REAL))", "MIN(overdue_payment_percentage)", "MAX(overdue_payment_percentage)", "AVG(overdue_payment_percentage)", "AVG(CAST(overdue_payment_percentage AS REAL))", "MIN(spend_concentration_ratio)", "MAX(spend_concentration_ratio)", "AVG(spend_concentration_ratio)", "AVG(CAST(spend_concentration_ratio AS REAL))", "MIN(total_vendor_spend)", "MAX(total_vendor_spend)", "AVG(total_vendor_spend)", "AVG(CAST(total_vendor_spend AS REAL))", "MIN(switching_cost_estimate)", "MAX(switching_cost_estimate)", "AVG(switching_cost_estimate)", "AVG(CAST(switching_cost_estimate AS REAL))", "MIN(vendor_relationship_days)", "MAX(vendor_relationship_days)", "AVG(vendor_relationship_days)", "AVG(CAST(vendor_relationship_days AS REAL))", "MIN(days_since_last_transaction)", "MAX(days_since_last_transaction)", "AVG(days_since_last_transaction)", "AVG(CAST(days_since_last_transaction AS REAL))", "MIN(total_transactions)", "MAX(total_transactions)", "AVG(total_transactions)", "AVG(CAST(total_transactions AS REAL))"] | 15 | 1.292 |
| [S20/Q18](#s20) | success | ["netsuite2_vendor_risk_analysis"] | 0 / {} | [] | [] | 15 | 0.565 |
| [S21/Q19](#s21) | success | ["netsuite2_vendor_risk_analysis"] | 0 / {} | ["activity_status"] | ["COUNT(*)"] | 4 | 0.414 |
| [S22/Q20](#s22) | success | ["netsuite2_vendor_risk_analysis"] | 0 / {} | [] | ["SUM(CASE WHEN vendor_name LIKE 'Vendor_%' THEN 1 ELSE 0 END)", "SUM(CASE WHEN vendor_category_name = 'General Supplier' THEN 1 ELSE 0 END)", "SUM(CASE WHEN total_vendor_spend < 1000 THEN 1 ELSE 0 END)", "SUM(CASE WHEN spend_concentration_ratio = 1.0 THEN 1 ELSE 0 END)"] | 1 | 0.438 |
| [S23/Q21](#s23) | success | ["netsuite2_vendor_risk_analysis"] | 0 / {} | ["vendor_name"] | ["COUNT(*)"] | 20 | 0.46 |
| [S24/Q22](#s24) | success | ["netsuite2_vendor_risk_analysis"] | 0 / {} | [] | [] | 91 | 1.161 |
| [S25/Q23](#s25) | success | ["netsuite2_vendor_risk_analysis"] | 0 / {} | [] | [] | 91 | 1.525 |
| [S26/Q24](#s26) | success | ["netsuite2_vendor_risk_analysis"] | 0 / {} | ["geographic_region"] | ["COUNT(*)", "SUM(total_vendor_spend)", "SUM(total_vendor_spend)", "SUM(total_vendor_spend)"] | 6 | 0.57 |
| [S27/Q25](#s27) | success | ["netsuite2_vendor_risk_analysis"] | 0 / {} | ["vendor_category_name"] | ["COUNT(*)", "SUM(total_vendor_spend)", "AVG(avg_payment_delay)", "AVG(overdue_payment_percentage)", "AVG(financial_health_score)", "AVG(cybersecurity_score)", "AVG(quality_score)", "AVG(innovation_capability_score)", "AVG(market_volatility_index)", "AVG(price_volatility_coefficient)"] | 8 | 0.602 |
| [S28/Q26](#s28) | success | ["netsuite2_vendor_risk_analysis"] | 0 / {} | ["contract_type"] | ["COUNT(*)"] | 2 | 0.434 |
| [S29/Q27](#s29) | success | ["netsuite2_vendor_risk_analysis"] | 0 / {} | ["dependency_level"] | ["COUNT(*)"] | 6 | 0.413 |


## 元数据和设置

| SQL | 类别 | 状态 | 内容 |
| --- | --- | --- | --- |
| S1 | connection_setup | success | PRAGMA query_only=ON |
| S2 | metadata | success | SELECT name,sql FROM sqlite_master WHERE type='table' ORDER BY name |


## Python 与执行位置

人工源码审查：**database_first_violation**。Python 对供应商进行最小最大归一化、加权评分、风险阈值分类、策略成本收益求和、分组计数和结果连接。这些属于 SQL 能够支持的常规算术、条件与关系运算，不能因称为风险模型或 ROI 分析就豁免。绘图另行保留。 [证据](../reviews/dacomp-075.json)。

P1：Need to compute normalized multi-dimensional resilience scores across 4 dimensions (Financial, Operational, Market, Strategic) using Min-Max scaling. This requires complex calculations and visualization that go beyond simple SQL aggregations.

[源码](../../../runs/dsv4flash-db-first-full-01/dacomp-075/attempt-01/python/P1.py)；[输出](../../../runs/dsv4flash-db-first-full-01/dacomp-075/attempt-01/python/P1.stdout)；[错误](../../../runs/dsv4flash-db-first-full-01/dacomp-075/attempt-01/python/P1.stderr)。检出需人工核验的 SQL 可实现操作：.query(；不能仅凭理由判为合规。

P2：Building the 4-dimension resilience scoring framework with Min-Max normalization. This requires per-vendor composite score calculations and visualization that cannot be done efficiently in SQL.

[源码](../../../runs/dsv4flash-db-first-full-01/dacomp-075/attempt-01/python/P2.py)；[输出](../../../runs/dsv4flash-db-first-full-01/dacomp-075/attempt-01/python/P2.stdout)；[错误](../../../runs/dsv4flash-db-first-full-01/dacomp-075/attempt-01/python/P2.stderr)。自动源码筛查未检出预设迁出信号；这不是全面语义合规证明。

P3：Creating visualizations of the multi-dimensional resilience scores: heatmap, radar chart, and distribution plots to communicate the framework results.

[源码](../../../runs/dsv4flash-db-first-full-01/dacomp-075/attempt-01/python/P3.py)；[输出](../../../runs/dsv4flash-db-first-full-01/dacomp-075/attempt-01/python/P3.stdout)；[错误](../../../runs/dsv4flash-db-first-full-01/dacomp-075/attempt-01/python/P3.stderr)。检出需人工核验的 SQL 可实现操作：groupby(, sort_values(；不能仅凭理由判为合规。

P4：Building the dynamic risk warning mechanism: computing 12-18 month supply disruption probability from multiple risk indicators (contract expiry, financial distress, operational weakness, market risk, inactivity, concentration). This requires composite probability modeling and scenario calculations not feasible in SQL.

[源码](../../../runs/dsv4flash-db-first-full-01/dacomp-075/attempt-01/python/P4.py)；[输出](../../../runs/dsv4flash-db-first-full-01/dacomp-075/attempt-01/python/P4.stdout)；[错误](../../../runs/dsv4flash-db-first-full-01/dacomp-075/attempt-01/python/P4.stderr)。检出需人工核验的 SQL 可实现操作：sort_values(；不能仅凭理由判为合规。

P5：Building personalized improvement plans and ROI model. ROI requires scenario modeling of disruption loss reduction versus strategy cost, a stochastic/financial calculation better handled in Python with numpy than in SQL.

[源码](../../../runs/dsv4flash-db-first-full-01/dacomp-075/attempt-01/python/P5.py)；[输出](../../../runs/dsv4flash-db-first-full-01/dacomp-075/attempt-01/python/P5.stdout)；[错误](../../../runs/dsv4flash-db-first-full-01/dacomp-075/attempt-01/python/P5.stderr)。检出需人工核验的 SQL 可实现操作：groupby(, sort_values(；不能仅凭理由判为合规。

P6：Refining the ROI model with more realistic assumptions. The previous model had inflated expected losses. Using a more conservative disruption impact model (15% of spend at risk, not 50%) and a 5-year horizon for infrastructure investments, with a more realistic probability calibration.

[源码](../../../runs/dsv4flash-db-first-full-01/dacomp-075/attempt-01/python/P6.py)；[输出](../../../runs/dsv4flash-db-first-full-01/dacomp-075/attempt-01/python/P6.stdout)；[错误](../../../runs/dsv4flash-db-first-full-01/dacomp-075/attempt-01/python/P6.stderr)。检出需人工核验的 SQL 可实现操作：groupby(, sort_values(；不能仅凭理由判为合规。

P7：Generating the final consolidated contingency plans and key vendor summary table. This combines computed scores, optimal strategies, and contingency plan text into an output table - a data assembly task done in Python after SQL-based scoring.

[源码](../../../runs/dsv4flash-db-first-full-01/dacomp-075/attempt-01/python/P7.py)；[输出](../../../runs/dsv4flash-db-first-full-01/dacomp-075/attempt-01/python/P7.stdout)；[错误](../../../runs/dsv4flash-db-first-full-01/dacomp-075/attempt-01/python/P7.stderr)。检出需人工核验的 SQL 可实现操作：.merge(, sort_values(；不能仅凭理由判为合规。

P8：The sensitivity analysis (Figure 12) failed because expected_annual_loss was not persisted. Recomputing it inline in Python to finish the ROI sensitivity figure - this is a financial scenario model better done in Python.

[源码](../../../runs/dsv4flash-db-first-full-01/dacomp-075/attempt-01/python/P8.py)；[输出](../../../runs/dsv4flash-db-first-full-01/dacomp-075/attempt-01/python/P8.stdout)；[错误](../../../runs/dsv4flash-db-first-full-01/dacomp-075/attempt-01/python/P8.stderr)。检出需人工核验的 SQL 可实现操作：groupby(, sort_values(；不能仅凭理由判为合规。

## 优化机会

已验证候选。筛选限于精确 SQL、相同自包含 CTE、相同单表完整过滤、可分解单表聚合；未覆盖任意 Join 等价和一般谓词蕴含。全部候选都是 offline，未测在线预测。

| 候选 | 类型 | 已有结果 | 覆盖 SQL | 后续次数 | 中间行数 | 验证 | 成本 |
| --- | --- | --- | --- | --- | --- | --- | --- |
| C1 | aggregate MV | False | ["S14", "S15", "S16"] | 2 | 6 | verified | Not benchmarked; correctness alone does not establish net speedup. |
| C2 | common filtered view | False | ["S18", "S20", "S21", "S22", "S24", "S25", "S27", "S28", "S29"] | 8 | 91 | verified | Not benchmarked; correctness alone does not establish net speedup. |
| C3 | aggregate MV | False | ["S21", "S22", "S27", "S28", "S29"] | 4 | 16 | verified | Not benchmarked; correctness alone does not establish net speedup. |


已验证覆盖（含触发查询、候选并集去重）：12/27 条成功数据 SQL。正确性仅针对当前数据库快照；未测性能的候选不能声称已加速。

[完整 build/rewrite 与比较证据](dacomp-075.analysis.json)。

### C2：common filtered view

Same single source and complete filter; original filter retained.

原查询 [S18](#s18), [S20](#s20), [S21](#s21), [S22](#s22), [S24](#s24), [S25](#s25), [S27](#s27), [S28](#s28), [S29](#s29) → 新增共享状态 C2 → 后续 8 次可复用。该构建点为事后假设，不代表 Agent 当时预知后续。

构建定义：

```sql
SELECT * FROM "netsuite2_vendor_risk_analysis" WHERE spend_concentration_ratio > 0.15 OR strategic_importance_level IN ('Mission Critical', 'High Strategic Value')
```

受益查询 S18 的改写示例：

```sql
SELECT vendor_id, vendor_name, vendor_category_name, geographic_region, total_vendor_spend, total_payables, total_expenses, avg_payment_delay, overdue_payment_percentage, overdue_invoices, total_payable_invoices, dependency_level, spend_concentration_ratio, relationship_stability, activity_status, vendor_risk_score, risk_level, business_impact_level, supplier_tier, management_priority, days_since_last_transaction, contract_type, contract_expiry_date, quality_score, compliance_rating, financial_health_score, market_volatility_index, alternative_suppliers_count, switching_cost_estimate, strategic_importance_level, innovation_capability_score, environmental_rating, cybersecurity_score, seasonal_demand_factor, price_volatility_coefficient, vendor_relationship_days, active_months, total_transactions, avg_payable_amount, max_transaction_amount FROM temp.reuse_candidate AS netsuite2_vendor_risk_analysis WHERE spend_concentration_ratio > 0.15 OR strategic_importance_level IN ('Mission Critical', 'High Strategic Value') ORDER BY vendor_risk_score DESC
```

| 原 SQL | 列名一致 | 结果一致 | 比较方法 |
| --- | --- | --- | --- |
| S18 | True | True | ordered_numeric_tolerance |
| S20 | True | True | ordered_numeric_tolerance |
| S21 | True | True | ordered_numeric_tolerance |
| S22 | True | True | exact_multiset |
| S24 | True | True | ordered_numeric_tolerance |
| S25 | True | True | ordered_numeric_tolerance |
| S27 | True | True | ordered_numeric_tolerance |
| S28 | True | True | ordered_numeric_tolerance |
| S29 | True | True | ordered_numeric_tolerance |


验证状态：verified；成本结论：Not benchmarked; correctness alone does not establish net speedup.

### C3：aggregate MV

Union of grouping keys; decomposable aggregate states; AVG uses SUM and non-NULL COUNT.

原查询 [S21](#s21), [S22](#s22), [S27](#s27), [S28](#s28), [S29](#s29) → 新增共享状态 C3 → 后续 4 次可复用。该构建点为事后假设，不代表 Agent 当时预知后续。

构建定义：

```sql
SELECT activity_status AS __g0, vendor_category_name AS __g1, contract_type AS __g2, dependency_level AS __g3, COUNT(*) AS __a0, SUM(CASE WHEN vendor_name LIKE 'Vendor_%' THEN 1 ELSE 0 END) AS __a1, SUM(CASE WHEN vendor_category_name = 'General Supplier' THEN 1 ELSE 0 END) AS __a2, SUM(CASE WHEN total_vendor_spend < 1000 THEN 1 ELSE 0 END) AS __a3, SUM(CASE WHEN spend_concentration_ratio = 1.0 THEN 1 ELSE 0 END) AS __a4, SUM(total_vendor_spend) AS __a5, SUM(avg_payment_delay) AS __a6_sum, COUNT(avg_payment_delay) AS __a6_n, SUM(overdue_payment_percentage) AS __a7_sum, COUNT(overdue_payment_percentage) AS __a7_n, SUM(financial_health_score) AS __a8_sum, COUNT(financial_health_score) AS __a8_n, SUM(cybersecurity_score) AS __a9_sum, COUNT(cybersecurity_score) AS __a9_n, SUM(quality_score) AS __a10_sum, COUNT(quality_score) AS __a10_n, SUM(innovation_capability_score) AS __a11_sum, COUNT(innovation_capability_score) AS __a11_n, SUM(market_volatility_index) AS __a12_sum, COUNT(market_volatility_index) AS __a12_n, SUM(price_volatility_coefficient) AS __a13_sum, COUNT(price_volatility_coefficient) AS __a13_n FROM "netsuite2_vendor_risk_analysis" WHERE spend_concentration_ratio > 0.15 OR strategic_importance_level IN ('Mission Critical', 'High Strategic Value') GROUP BY activity_status, vendor_category_name, contract_type, dependency_level
```

受益查询 S21 的改写示例：

```sql
SELECT __g0 AS "activity_status", SUM(__a0) AS n FROM temp.reuse_candidate GROUP BY __g0 ORDER BY n DESC
```

| 原 SQL | 列名一致 | 结果一致 | 比较方法 |
| --- | --- | --- | --- |
| S21 | True | True | ordered_numeric_tolerance |
| S22 | True | True | exact_multiset |
| S27 | True | True | ordered_numeric_tolerance |
| S28 | True | True | ordered_numeric_tolerance |
| S29 | True | True | ordered_numeric_tolerance |


验证状态：verified；成本结论：Not benchmarked; correctness alone does not establish net speedup.

### C1：aggregate MV

Union of grouping keys; decomposable aggregate states; AVG uses SUM and non-NULL COUNT.

原查询 [S14](#s14), [S15](#s15), [S16](#s16) → 新增共享状态 C1 → 后续 2 次可复用。该构建点为事后假设，不代表 Agent 当时预知后续。

构建定义：

```sql
SELECT strategic_importance_level AS __g0, risk_level AS __g1, SUM(CASE WHEN spend_concentration_ratio > 0.15 OR strategic_importance_level IN ('Mission Critical', 'High Strategic Value') THEN 1 ELSE 0 END) AS __a0, SUM(CASE WHEN spend_concentration_ratio > 0.15 THEN 1 ELSE 0 END) AS __a1, SUM(CASE WHEN strategic_importance_level IN ('Mission Critical', 'High Strategic Value') THEN 1 ELSE 0 END) AS __a2, COUNT(*) AS __a3 FROM "netsuite2_vendor_risk_analysis"  GROUP BY strategic_importance_level, risk_level
```

受益查询 S14 的改写示例：

```sql
SELECT SUM(__a0) AS focus_group_count, SUM(__a1) AS conc_gt15, SUM(__a2) AS strat_high FROM temp.reuse_candidate
```

| 原 SQL | 列名一致 | 结果一致 | 比较方法 |
| --- | --- | --- | --- |
| S14 | True | True | exact_multiset |
| S15 | True | True | ordered_numeric_tolerance |
| S16 | True | True | ordered_numeric_tolerance |


验证状态：verified；成本结论：Not benchmarked; correctness alone does not establish net speedup.

结果依赖：自动记录 SQL→Python 的接口父调用，以及源码中引用归档文件的消费者；字面值相同不认定因果。模型方向选择需要人工读取消息，尚未做全面因果标注。

[原始报告](../../../runs/dsv4flash-db-first-full-01/dacomp-075/attempt-01/answer.md)；[统一消息](../../../runs/dsv4flash-db-first-full-01/dacomp-075/attempt-01/messages.jsonl)；[原始 OpenCode 事件](../../../runs/dsv4flash-db-first-full-01/dacomp-075/attempt-01/opencode.jsonl)；[SQL 引擎日志](../../../runs/dsv4flash-db-first-full-01/dacomp-075/attempt-01/sql_journal.jsonl)。

[可读报告（本地图片链接规范化）](../answers/dacomp-075.md)。原始回答保留，分析结论未改写。

## S1

类别 `connection_setup`；来源 `connection`；调用 `abc3a05277cb473285493d74baa0363a`；状态 `success`。

```sql
PRAGMA query_only=ON
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-075/attempt-01/sql/S1.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-075/attempt-01/sql/S1.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-075/attempt-01/results/S1.rows.jsonl)；完整：True；SHA256：`e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`。

## S2

类别 `metadata`；来源 `list_db`；调用 `abc3a05277cb473285493d74baa0363a`；状态 `success`。

```sql
SELECT name,sql FROM sqlite_master WHERE type='table' ORDER BY name
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-075/attempt-01/sql/S2.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-075/attempt-01/sql/S2.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-075/attempt-01/results/S2.rows.jsonl)；完整：True；SHA256：`41ae5bb50f6892f34a74b9bcc35f4b64fcef09ffaa9c7eee10323a104b920c47`。

## S3

类别 `data`；来源 `query_db`；调用 `55e9a7f6b0ec4fc6a316ab9fd21cd2e0`；状态 `success`。

```sql
SELECT COUNT(*) AS total_rows, COUNT(DISTINCT vendor_id) AS total_vendors FROM netsuite2_vendor_risk_analysis
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-075/attempt-01/sql/S3.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-075/attempt-01/sql/S3.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-075/attempt-01/results/S3.rows.jsonl)；完整：True；SHA256：`85a2d2fd390cd8edb479a48b51b64bef6ce42620be81667122b43ca138caffe3`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "netsuite2_vendor_risk_analysis", "kind": "base", "block": null, "base_tables": ["netsuite2_vendor_risk_analysis"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |
| B1 | COUNT(DISTINCT vendor_id) | [{"table": "netsuite2_vendor_risk_analysis", "column": "vendor_id"}] | [] | False |


## S4

类别 `data`；来源 `query_db`；调用 `d4755f8445094a6992c676e9570847d0`；状态 `success`。

```sql
SELECT * FROM netsuite2_vendor_risk_analysis LIMIT 5
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-075/attempt-01/sql/S4.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-075/attempt-01/sql/S4.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-075/attempt-01/results/S4.rows.jsonl)；完整：True；SHA256：`b14c699aa6c25994801c8c3543a978d11d2d90fd0c997c80670e115c3622db04`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "netsuite2_vendor_risk_analysis", "kind": "base", "block": null, "base_tables": ["netsuite2_vendor_risk_analysis"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |


## S5

类别 `data`；来源 `query_db`；调用 `6c77b5b2f20948a8a10a07dcf1bc905f`；状态 `success`。

```sql
SELECT DISTINCT vendor_category_name FROM netsuite2_vendor_risk_analysis
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-075/attempt-01/sql/S5.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-075/attempt-01/sql/S5.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-075/attempt-01/results/S5.rows.jsonl)；完整：True；SHA256：`e7e92ccfd1d2da300d10419f45643c7a191652e69c1345d1634fcb9c662348e5`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "netsuite2_vendor_risk_analysis", "kind": "base", "block": null, "base_tables": ["netsuite2_vendor_risk_analysis"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |


## S6

类别 `data`；来源 `query_db`；调用 `5e4931ec680f4c3594d81ed09f2f37a8`；状态 `success`。

```sql
SELECT DISTINCT risk_level FROM netsuite2_vendor_risk_analysis
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-075/attempt-01/sql/S6.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-075/attempt-01/sql/S6.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-075/attempt-01/results/S6.rows.jsonl)；完整：True；SHA256：`e289269ff1241717bd804f7a8212d850958e5be5d23b49243ba3979734b416a1`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "netsuite2_vendor_risk_analysis", "kind": "base", "block": null, "base_tables": ["netsuite2_vendor_risk_analysis"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |


## S7

类别 `data`；来源 `query_db`；调用 `761cd9a511ba4af4987be45d0b630c1d`；状态 `success`。

```sql
SELECT DISTINCT strategic_importance_level FROM netsuite2_vendor_risk_analysis
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-075/attempt-01/sql/S7.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-075/attempt-01/sql/S7.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-075/attempt-01/results/S7.rows.jsonl)；完整：True；SHA256：`ca9f99f192334d2defb94edd9c4b6ab3d09cee4dc313224cae9357d9a2fb7d93`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "netsuite2_vendor_risk_analysis", "kind": "base", "block": null, "base_tables": ["netsuite2_vendor_risk_analysis"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |


## S8

类别 `data`；来源 `query_db`；调用 `0729040931224f5280db24853bef2df8`；状态 `success`。

```sql
SELECT DISTINCT geographic_region FROM netsuite2_vendor_risk_analysis
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-075/attempt-01/sql/S8.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-075/attempt-01/sql/S8.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-075/attempt-01/results/S8.rows.jsonl)；完整：True；SHA256：`f63cf778640f5818cbbeb98407c5da04a0326c3cb7096db2bed66aa0f810fd69`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "netsuite2_vendor_risk_analysis", "kind": "base", "block": null, "base_tables": ["netsuite2_vendor_risk_analysis"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |


## S9

类别 `data`；来源 `query_db`；调用 `2bb9436291714dd2a6259ce000241756`；状态 `success`。

```sql
SELECT DISTINCT environmental_rating FROM netsuite2_vendor_risk_analysis
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-075/attempt-01/sql/S9.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-075/attempt-01/sql/S9.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-075/attempt-01/results/S9.rows.jsonl)；完整：True；SHA256：`77bcdc00708d1282482f122688d307d5d7f21b255a650c5d03fec945ddcf13b4`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "netsuite2_vendor_risk_analysis", "kind": "base", "block": null, "base_tables": ["netsuite2_vendor_risk_analysis"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |


## S10

类别 `data`；来源 `query_db`；调用 `ac24d2b8c2594ac1aa5728029da0ebb6`；状态 `success`。

```sql
SELECT DISTINCT compliance_rating FROM netsuite2_vendor_risk_analysis
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-075/attempt-01/sql/S10.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-075/attempt-01/sql/S10.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-075/attempt-01/results/S10.rows.jsonl)；完整：True；SHA256：`eff64a4ffd36e4fb57585b36196601deb56f9b9c4a69b47ff04a9bd43c619dc3`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "netsuite2_vendor_risk_analysis", "kind": "base", "block": null, "base_tables": ["netsuite2_vendor_risk_analysis"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |


## S11

类别 `data`；来源 `query_db`；调用 `f170eac8ab8c488c9f61831767d79fe9`；状态 `success`。

```sql
SELECT DISTINCT dependency_level FROM netsuite2_vendor_risk_analysis
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-075/attempt-01/sql/S11.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-075/attempt-01/sql/S11.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-075/attempt-01/results/S11.rows.jsonl)；完整：True；SHA256：`857dd083e9cc3322a004affefcd33aa3ccf5cdc069d68c17b35878234618cbf0`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "netsuite2_vendor_risk_analysis", "kind": "base", "block": null, "base_tables": ["netsuite2_vendor_risk_analysis"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |


## S12

类别 `data`；来源 `query_db`；调用 `d67af79dbe28426b83abdcac80987a1f`；状态 `success`。

```sql
SELECT DISTINCT relationship_stability FROM netsuite2_vendor_risk_analysis
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-075/attempt-01/sql/S12.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-075/attempt-01/sql/S12.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-075/attempt-01/results/S12.rows.jsonl)；完整：True；SHA256：`e868f83d2035a3d5656e7428b4b06072ccef6dab3f04ee332dab0542ff515cef`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "netsuite2_vendor_risk_analysis", "kind": "base", "block": null, "base_tables": ["netsuite2_vendor_risk_analysis"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |


## S13

类别 `data`；来源 `query_db`；调用 `5076913d91e54457b2b5b655b17c9cbc`；状态 `success`。

```sql
SELECT DISTINCT supplier_tier FROM netsuite2_vendor_risk_analysis
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-075/attempt-01/sql/S13.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-075/attempt-01/sql/S13.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-075/attempt-01/results/S13.rows.jsonl)；完整：True；SHA256：`9ba0df669d4337625b089b670b5f1d49577c3968e606f8284e6a4b2b0628ed8c`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "netsuite2_vendor_risk_analysis", "kind": "base", "block": null, "base_tables": ["netsuite2_vendor_risk_analysis"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |


## S14

类别 `data`；来源 `query_db`；调用 `745330c1168e4b20a5c48d3ccf7504d3`；状态 `success`。

```sql
SELECT
  SUM(CASE WHEN spend_concentration_ratio > 0.15 OR strategic_importance_level IN ('Mission Critical','High Strategic Value') THEN 1 ELSE 0 END) AS focus_group_count,
  SUM(CASE WHEN spend_concentration_ratio > 0.15 THEN 1 ELSE 0 END) AS conc_gt15,
  SUM(CASE WHEN strategic_importance_level IN ('Mission Critical','High Strategic Value') THEN 1 ELSE 0 END) AS strat_high
FROM netsuite2_vendor_risk_analysis
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-075/attempt-01/sql/S14.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-075/attempt-01/sql/S14.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-075/attempt-01/results/S14.rows.jsonl)；完整：True；SHA256：`d6cf00acab8d2796cef079de2bbbfb8d0ef1026564019f2a21ed551270a3920c`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "netsuite2_vendor_risk_analysis", "kind": "base", "block": null, "base_tables": ["netsuite2_vendor_risk_analysis"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | SUM(CASE WHEN spend_concentration_ratio > 0.15 OR strategic_importance_level IN ('Mission Critical', 'High Strategic Value') THEN 1 ELSE 0 END) | [] | [{"table": "netsuite2_vendor_risk_analysis", "column": "spend_concentration_ratio"}, {"table": "netsuite2_vendor_risk_analysis", "column": "strategic_importance_level"}] | False |
| B1 | SUM(CASE WHEN spend_concentration_ratio > 0.15 THEN 1 ELSE 0 END) | [] | [{"table": "netsuite2_vendor_risk_analysis", "column": "spend_concentration_ratio"}] | False |
| B1 | SUM(CASE WHEN strategic_importance_level IN ('Mission Critical', 'High Strategic Value') THEN 1 ELSE 0 END) | [] | [{"table": "netsuite2_vendor_risk_analysis", "column": "strategic_importance_level"}] | False |


## S15

类别 `data`；来源 `query_db`；调用 `3b78cf8031ed4119984509ba3eae1bb0`；状态 `success`。

```sql
SELECT strategic_importance_level, COUNT(*) AS n FROM netsuite2_vendor_risk_analysis GROUP BY strategic_importance_level ORDER BY n DESC
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-075/attempt-01/sql/S15.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-075/attempt-01/sql/S15.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-075/attempt-01/results/S15.rows.jsonl)；完整：True；SHA256：`342171c2d0fbbde42ca251bdc68d3820451f2342b7694059f7e743ab11432ee9`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "netsuite2_vendor_risk_analysis", "kind": "base", "block": null, "base_tables": ["netsuite2_vendor_risk_analysis"]}] | [] | ["strategic_importance_level"] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |


## S16

类别 `data`；来源 `query_db`；调用 `28cb097310d843e6bcdf6f02cff2f762`；状态 `success`。

```sql
SELECT risk_level, COUNT(*) AS n FROM netsuite2_vendor_risk_analysis GROUP BY risk_level ORDER BY n DESC
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-075/attempt-01/sql/S16.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-075/attempt-01/sql/S16.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-075/attempt-01/results/S16.rows.jsonl)；完整：True；SHA256：`cee2bb35f2ead796dc98312a39480184349c2b0db9781730d40e42ee39193316`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "netsuite2_vendor_risk_analysis", "kind": "base", "block": null, "base_tables": ["netsuite2_vendor_risk_analysis"]}] | [] | ["risk_level"] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |


## S17

类别 `data`；来源 `query_db`；调用 `21245062a6164e608fa98c51d3b252d0`；状态 `success`。

```sql
SELECT MIN(analysis_date), MAX(analysis_date), MIN(contract_expiry_date), MAX(contract_expiry_date), MIN(first_transaction_date), MAX(last_transaction_date) FROM netsuite2_vendor_risk_analysis
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-075/attempt-01/sql/S17.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-075/attempt-01/sql/S17.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-075/attempt-01/results/S17.rows.jsonl)；完整：True；SHA256：`76f93a36e6a84f657493eade2ae782d216171c94d8ea7f8c672f6bac97e73bab`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "netsuite2_vendor_risk_analysis", "kind": "base", "block": null, "base_tables": ["netsuite2_vendor_risk_analysis"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | MIN(analysis_date) | [{"table": "netsuite2_vendor_risk_analysis", "column": "analysis_date"}] | [] | False |
| B1 | MAX(analysis_date) | [{"table": "netsuite2_vendor_risk_analysis", "column": "analysis_date"}] | [] | False |
| B1 | MIN(contract_expiry_date) | [{"table": "netsuite2_vendor_risk_analysis", "column": "contract_expiry_date"}] | [] | False |
| B1 | MAX(contract_expiry_date) | [{"table": "netsuite2_vendor_risk_analysis", "column": "contract_expiry_date"}] | [] | False |
| B1 | MIN(first_transaction_date) | [{"table": "netsuite2_vendor_risk_analysis", "column": "first_transaction_date"}] | [] | False |
| B1 | MAX(last_transaction_date) | [{"table": "netsuite2_vendor_risk_analysis", "column": "last_transaction_date"}] | [] | False |


## S18

类别 `data`；来源 `query_db`；调用 `46f6920c6c8d4eafa958e12757c388ec`；状态 `success`。

```sql
SELECT
  vendor_id,
  vendor_name,
  vendor_category_name,
  geographic_region,
  total_vendor_spend,
  total_payables,
  total_expenses,
  avg_payment_delay,
  overdue_payment_percentage,
  overdue_invoices,
  total_payable_invoices,
  dependency_level,
  spend_concentration_ratio,
  relationship_stability,
  activity_status,
  vendor_risk_score,
  risk_level,
  business_impact_level,
  supplier_tier,
  management_priority,
  days_since_last_transaction,
  contract_type,
  contract_expiry_date,
  quality_score,
  compliance_rating,
  financial_health_score,
  market_volatility_index,
  alternative_suppliers_count,
  switching_cost_estimate,
  strategic_importance_level,
  innovation_capability_score,
  environmental_rating,
  cybersecurity_score,
  seasonal_demand_factor,
  price_volatility_coefficient,
  vendor_relationship_days,
  active_months,
  total_transactions,
  avg_payable_amount,
  max_transaction_amount
FROM netsuite2_vendor_risk_analysis
WHERE spend_concentration_ratio > 0.15 OR strategic_importance_level IN ('Mission Critical', 'High Strategic Value')
ORDER BY vendor_risk_score DESC
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-075/attempt-01/sql/S18.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-075/attempt-01/sql/S18.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-075/attempt-01/results/S18.rows.jsonl)；完整：True；SHA256：`069a39c57e5bcd9cb7476b9d1a7c7f715712d9976d45eaeb2e34907c6bf4e951`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "netsuite2_vendor_risk_analysis", "kind": "base", "block": null, "base_tables": ["netsuite2_vendor_risk_analysis"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |


## S19

类别 `data`；来源 `query_db`；调用 `c4eea5d6a34f4a2ba05a0e5fca0a18ff`；状态 `success`。

```sql
SELECT
  'Quality Score' AS metric, MIN(quality_score) AS min_val, MAX(quality_score) AS max_val, ROUND(AVG(quality_score),2) AS avg_val, ROUND(AVG(CAST(quality_score AS REAL)),2) AS avg_real FROM netsuite2_vendor_risk_analysis WHERE spend_concentration_ratio > 0.15 OR strategic_importance_level IN ('Mission Critical', 'High Strategic Value')
UNION ALL
SELECT 'Financial Health Score', MIN(financial_health_score), MAX(financial_health_score), ROUND(AVG(financial_health_score),2), ROUND(AVG(CAST(financial_health_score AS REAL)),2) FROM netsuite2_vendor_risk_analysis WHERE spend_concentration_ratio > 0.15 OR strategic_importance_level IN ('Mission Critical', 'High Strategic Value')
UNION ALL
SELECT 'Innovation Capability Score', MIN(innovation_capability_score), MAX(innovation_capability_score), ROUND(AVG(innovation_capability_score),2), ROUND(AVG(CAST(innovation_capability_score AS REAL)),2) FROM netsuite2_vendor_risk_analysis WHERE spend_concentration_ratio > 0.15 OR strategic_importance_level IN ('Mission Critical', 'High Strategic Value')
UNION ALL
SELECT 'Cybersecurity Score', MIN(cybersecurity_score), MAX(cybersecurity_score), ROUND(AVG(cybersecurity_score),2), ROUND(AVG(CAST(cybersecurity_score AS REAL)),2) FROM netsuite2_vendor_risk_analysis WHERE spend_concentration_ratio > 0.15 OR strategic_importance_level IN ('Mission Critical', 'High Strategic Value')
UNION ALL
SELECT 'Market Volatility Index', MIN(market_volatility_index), MAX(market_volatility_index), ROUND(AVG(market_volatility_index),4), ROUND(AVG(CAST(market_volatility_index AS REAL)),4) FROM netsuite2_vendor_risk_analysis WHERE spend_concentration_ratio > 0.15 OR strategic_importance_level IN ('Mission Critical', 'High Strategic Value')
UNION ALL
SELECT 'Alternative Suppliers Count', MIN(alternative_suppliers_count), MAX(alternative_suppliers_count), ROUND(AVG(alternative_suppliers_count),2), ROUND(AVG(CAST(alternative_suppliers_count AS REAL)),2) FROM netsuite2_vendor_risk_analysis WHERE spend_concentration_ratio > 0.15 OR strategic_importance_level IN ('Mission Critical', 'High Strategic Value')
UNION ALL
SELECT 'Price Volatility Coefficient', MIN(price_volatility_coefficient), MAX(price_volatility_coefficient), ROUND(AVG(price_volatility_coefficient),4), ROUND(AVG(CAST(price_volatility_coefficient AS REAL)),4) FROM netsuite2_vendor_risk_analysis WHERE spend_concentration_ratio > 0.15 OR strategic_importance_level IN ('Mission Critical', 'High Strategic Value')
UNION ALL
SELECT 'Avg Payment Delay', MIN(avg_payment_delay), MAX(avg_payment_delay), ROUND(AVG(avg_payment_delay),2), ROUND(AVG(CAST(avg_payment_delay AS REAL)),2) FROM netsuite2_vendor_risk_analysis WHERE spend_concentration_ratio > 0.15 OR strategic_importance_level IN ('Mission Critical', 'High Strategic Value')
UNION ALL
SELECT 'Overdue Payment %', MIN(overdue_payment_percentage), MAX(overdue_payment_percentage), ROUND(AVG(overdue_payment_percentage),2), ROUND(AVG(CAST(overdue_payment_percentage AS REAL)),2) FROM netsuite2_vendor_risk_analysis WHERE spend_concentration_ratio > 0.15 OR strategic_importance_level IN ('Mission Critical', 'High Strategic Value')
UNION ALL
SELECT 'Spend Concentration Ratio', MIN(spend_concentration_ratio), MAX(spend_concentration_ratio), ROUND(AVG(spend_concentration_ratio),4), ROUND(AVG(CAST(spend_concentration_ratio AS REAL)),4) FROM netsuite2_vendor_risk_analysis WHERE spend_concentration_ratio > 0.15 OR strategic_importance_level IN ('Mission Critical', 'High Strategic Value')
UNION ALL
SELECT 'Total Vendor Spend', MIN(total_vendor_spend), MAX(total_vendor_spend), ROUND(AVG(total_vendor_spend),2), ROUND(AVG(CAST(total_vendor_spend AS REAL)),2) FROM netsuite2_vendor_risk_analysis WHERE spend_concentration_ratio > 0.15 OR strategic_importance_level IN ('Mission Critical', 'High Strategic Value')
UNION ALL
SELECT 'Switching Cost Estimate', MIN(switching_cost_estimate), MAX(switching_cost_estimate), ROUND(AVG(switching_cost_estimate),2), ROUND(AVG(CAST(switching_cost_estimate AS REAL)),2) FROM netsuite2_vendor_risk_analysis WHERE spend_concentration_ratio > 0.15 OR strategic_importance_level IN ('Mission Critical', 'High Strategic Value')
UNION ALL
SELECT 'Vendor Relationship Days', MIN(vendor_relationship_days), MAX(vendor_relationship_days), ROUND(AVG(vendor_relationship_days),2), ROUND(AVG(CAST(vendor_relationship_days AS REAL)),2) FROM netsuite2_vendor_risk_analysis WHERE spend_concentration_ratio > 0.15 OR strategic_importance_level IN ('Mission Critical', 'High Strategic Value')
UNION ALL
SELECT 'Days Since Last Transaction', MIN(days_since_last_transaction), MAX(days_since_last_transaction), ROUND(AVG(days_since_last_transaction),2), ROUND(AVG(CAST(days_since_last_transaction AS REAL)),2) FROM netsuite2_vendor_risk_analysis WHERE spend_concentration_ratio > 0.15 OR strategic_importance_level IN ('Mission Critical', 'High Strategic Value')
UNION ALL
SELECT 'Total Transactions', MIN(total_transactions), MAX(total_transactions), ROUND(AVG(total_transactions),2), ROUND(AVG(CAST(total_transactions AS REAL)),2) FROM netsuite2_vendor_risk_analysis WHERE spend_concentration_ratio > 0.15 OR strategic_importance_level IN ('Mission Critical', 'High Strategic Value')
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-075/attempt-01/sql/S19.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-075/attempt-01/sql/S19.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-075/attempt-01/results/S19.rows.jsonl)；完整：True；SHA256：`39d33b859445f73db9a2a71fbdd732e3d5f3ebf4073675a75cb40298517d0bd5`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "netsuite2_vendor_risk_analysis", "kind": "base", "block": null, "base_tables": ["netsuite2_vendor_risk_analysis"]}] | [] | [] |
| B2 | [{"alias": "netsuite2_vendor_risk_analysis", "kind": "base", "block": null, "base_tables": ["netsuite2_vendor_risk_analysis"]}] | [] | [] |
| B3 | [] | [] | [] |
| B4 | [{"alias": "netsuite2_vendor_risk_analysis", "kind": "base", "block": null, "base_tables": ["netsuite2_vendor_risk_analysis"]}] | [] | [] |
| B5 | [] | [] | [] |
| B6 | [{"alias": "netsuite2_vendor_risk_analysis", "kind": "base", "block": null, "base_tables": ["netsuite2_vendor_risk_analysis"]}] | [] | [] |
| B7 | [] | [] | [] |
| B8 | [{"alias": "netsuite2_vendor_risk_analysis", "kind": "base", "block": null, "base_tables": ["netsuite2_vendor_risk_analysis"]}] | [] | [] |
| B9 | [] | [] | [] |
| B10 | [{"alias": "netsuite2_vendor_risk_analysis", "kind": "base", "block": null, "base_tables": ["netsuite2_vendor_risk_analysis"]}] | [] | [] |
| B11 | [] | [] | [] |
| B12 | [{"alias": "netsuite2_vendor_risk_analysis", "kind": "base", "block": null, "base_tables": ["netsuite2_vendor_risk_analysis"]}] | [] | [] |
| B13 | [] | [] | [] |
| B14 | [{"alias": "netsuite2_vendor_risk_analysis", "kind": "base", "block": null, "base_tables": ["netsuite2_vendor_risk_analysis"]}] | [] | [] |
| B15 | [] | [] | [] |
| B16 | [{"alias": "netsuite2_vendor_risk_analysis", "kind": "base", "block": null, "base_tables": ["netsuite2_vendor_risk_analysis"]}] | [] | [] |
| B17 | [] | [] | [] |
| B18 | [{"alias": "netsuite2_vendor_risk_analysis", "kind": "base", "block": null, "base_tables": ["netsuite2_vendor_risk_analysis"]}] | [] | [] |
| B19 | [] | [] | [] |
| B20 | [{"alias": "netsuite2_vendor_risk_analysis", "kind": "base", "block": null, "base_tables": ["netsuite2_vendor_risk_analysis"]}] | [] | [] |
| B21 | [] | [] | [] |
| B22 | [{"alias": "netsuite2_vendor_risk_analysis", "kind": "base", "block": null, "base_tables": ["netsuite2_vendor_risk_analysis"]}] | [] | [] |
| B23 | [] | [] | [] |
| B24 | [{"alias": "netsuite2_vendor_risk_analysis", "kind": "base", "block": null, "base_tables": ["netsuite2_vendor_risk_analysis"]}] | [] | [] |
| B25 | [] | [] | [] |
| B26 | [{"alias": "netsuite2_vendor_risk_analysis", "kind": "base", "block": null, "base_tables": ["netsuite2_vendor_risk_analysis"]}] | [] | [] |
| B27 | [] | [] | [] |
| B28 | [{"alias": "netsuite2_vendor_risk_analysis", "kind": "base", "block": null, "base_tables": ["netsuite2_vendor_risk_analysis"]}] | [] | [] |
| B29 | [] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | MIN(quality_score) | [{"table": "netsuite2_vendor_risk_analysis", "column": "quality_score"}] | [] | False |
| B1 | MAX(quality_score) | [{"table": "netsuite2_vendor_risk_analysis", "column": "quality_score"}] | [] | False |
| B1 | AVG(quality_score) | [{"table": "netsuite2_vendor_risk_analysis", "column": "quality_score"}] | [] | False |
| B1 | AVG(CAST(quality_score AS REAL)) | [{"table": "netsuite2_vendor_risk_analysis", "column": "quality_score"}] | [] | False |
| B2 | MIN(financial_health_score) | [{"table": "netsuite2_vendor_risk_analysis", "column": "financial_health_score"}] | [] | False |
| B2 | MAX(financial_health_score) | [{"table": "netsuite2_vendor_risk_analysis", "column": "financial_health_score"}] | [] | False |
| B2 | AVG(financial_health_score) | [{"table": "netsuite2_vendor_risk_analysis", "column": "financial_health_score"}] | [] | False |
| B2 | AVG(CAST(financial_health_score AS REAL)) | [{"table": "netsuite2_vendor_risk_analysis", "column": "financial_health_score"}] | [] | False |
| B4 | MIN(innovation_capability_score) | [{"table": "netsuite2_vendor_risk_analysis", "column": "innovation_capability_score"}] | [] | False |
| B4 | MAX(innovation_capability_score) | [{"table": "netsuite2_vendor_risk_analysis", "column": "innovation_capability_score"}] | [] | False |
| B4 | AVG(innovation_capability_score) | [{"table": "netsuite2_vendor_risk_analysis", "column": "innovation_capability_score"}] | [] | False |
| B4 | AVG(CAST(innovation_capability_score AS REAL)) | [{"table": "netsuite2_vendor_risk_analysis", "column": "innovation_capability_score"}] | [] | False |
| B6 | MIN(cybersecurity_score) | [{"table": "netsuite2_vendor_risk_analysis", "column": "cybersecurity_score"}] | [] | False |
| B6 | MAX(cybersecurity_score) | [{"table": "netsuite2_vendor_risk_analysis", "column": "cybersecurity_score"}] | [] | False |
| B6 | AVG(cybersecurity_score) | [{"table": "netsuite2_vendor_risk_analysis", "column": "cybersecurity_score"}] | [] | False |
| B6 | AVG(CAST(cybersecurity_score AS REAL)) | [{"table": "netsuite2_vendor_risk_analysis", "column": "cybersecurity_score"}] | [] | False |
| B8 | MIN(market_volatility_index) | [{"table": "netsuite2_vendor_risk_analysis", "column": "market_volatility_index"}] | [] | False |
| B8 | MAX(market_volatility_index) | [{"table": "netsuite2_vendor_risk_analysis", "column": "market_volatility_index"}] | [] | False |
| B8 | AVG(market_volatility_index) | [{"table": "netsuite2_vendor_risk_analysis", "column": "market_volatility_index"}] | [] | False |
| B8 | AVG(CAST(market_volatility_index AS REAL)) | [{"table": "netsuite2_vendor_risk_analysis", "column": "market_volatility_index"}] | [] | False |
| B10 | MIN(alternative_suppliers_count) | [{"table": "netsuite2_vendor_risk_analysis", "column": "alternative_suppliers_count"}] | [] | False |
| B10 | MAX(alternative_suppliers_count) | [{"table": "netsuite2_vendor_risk_analysis", "column": "alternative_suppliers_count"}] | [] | False |
| B10 | AVG(alternative_suppliers_count) | [{"table": "netsuite2_vendor_risk_analysis", "column": "alternative_suppliers_count"}] | [] | False |
| B10 | AVG(CAST(alternative_suppliers_count AS REAL)) | [{"table": "netsuite2_vendor_risk_analysis", "column": "alternative_suppliers_count"}] | [] | False |
| B12 | MIN(price_volatility_coefficient) | [{"table": "netsuite2_vendor_risk_analysis", "column": "price_volatility_coefficient"}] | [] | False |
| B12 | MAX(price_volatility_coefficient) | [{"table": "netsuite2_vendor_risk_analysis", "column": "price_volatility_coefficient"}] | [] | False |
| B12 | AVG(price_volatility_coefficient) | [{"table": "netsuite2_vendor_risk_analysis", "column": "price_volatility_coefficient"}] | [] | False |
| B12 | AVG(CAST(price_volatility_coefficient AS REAL)) | [{"table": "netsuite2_vendor_risk_analysis", "column": "price_volatility_coefficient"}] | [] | False |
| B14 | MIN(avg_payment_delay) | [{"table": "netsuite2_vendor_risk_analysis", "column": "avg_payment_delay"}] | [] | False |
| B14 | MAX(avg_payment_delay) | [{"table": "netsuite2_vendor_risk_analysis", "column": "avg_payment_delay"}] | [] | False |
| B14 | AVG(avg_payment_delay) | [{"table": "netsuite2_vendor_risk_analysis", "column": "avg_payment_delay"}] | [] | False |
| B14 | AVG(CAST(avg_payment_delay AS REAL)) | [{"table": "netsuite2_vendor_risk_analysis", "column": "avg_payment_delay"}] | [] | False |
| B16 | MIN(overdue_payment_percentage) | [{"table": "netsuite2_vendor_risk_analysis", "column": "overdue_payment_percentage"}] | [] | False |
| B16 | MAX(overdue_payment_percentage) | [{"table": "netsuite2_vendor_risk_analysis", "column": "overdue_payment_percentage"}] | [] | False |
| B16 | AVG(overdue_payment_percentage) | [{"table": "netsuite2_vendor_risk_analysis", "column": "overdue_payment_percentage"}] | [] | False |
| B16 | AVG(CAST(overdue_payment_percentage AS REAL)) | [{"table": "netsuite2_vendor_risk_analysis", "column": "overdue_payment_percentage"}] | [] | False |
| B18 | MIN(spend_concentration_ratio) | [{"table": "netsuite2_vendor_risk_analysis", "column": "spend_concentration_ratio"}] | [] | False |
| B18 | MAX(spend_concentration_ratio) | [{"table": "netsuite2_vendor_risk_analysis", "column": "spend_concentration_ratio"}] | [] | False |
| B18 | AVG(spend_concentration_ratio) | [{"table": "netsuite2_vendor_risk_analysis", "column": "spend_concentration_ratio"}] | [] | False |
| B18 | AVG(CAST(spend_concentration_ratio AS REAL)) | [{"table": "netsuite2_vendor_risk_analysis", "column": "spend_concentration_ratio"}] | [] | False |
| B20 | MIN(total_vendor_spend) | [{"table": "netsuite2_vendor_risk_analysis", "column": "total_vendor_spend"}] | [] | False |
| B20 | MAX(total_vendor_spend) | [{"table": "netsuite2_vendor_risk_analysis", "column": "total_vendor_spend"}] | [] | False |
| B20 | AVG(total_vendor_spend) | [{"table": "netsuite2_vendor_risk_analysis", "column": "total_vendor_spend"}] | [] | False |
| B20 | AVG(CAST(total_vendor_spend AS REAL)) | [{"table": "netsuite2_vendor_risk_analysis", "column": "total_vendor_spend"}] | [] | False |
| B22 | MIN(switching_cost_estimate) | [{"table": "netsuite2_vendor_risk_analysis", "column": "switching_cost_estimate"}] | [] | False |
| B22 | MAX(switching_cost_estimate) | [{"table": "netsuite2_vendor_risk_analysis", "column": "switching_cost_estimate"}] | [] | False |
| B22 | AVG(switching_cost_estimate) | [{"table": "netsuite2_vendor_risk_analysis", "column": "switching_cost_estimate"}] | [] | False |
| B22 | AVG(CAST(switching_cost_estimate AS REAL)) | [{"table": "netsuite2_vendor_risk_analysis", "column": "switching_cost_estimate"}] | [] | False |
| B24 | MIN(vendor_relationship_days) | [{"table": "netsuite2_vendor_risk_analysis", "column": "vendor_relationship_days"}] | [] | False |
| B24 | MAX(vendor_relationship_days) | [{"table": "netsuite2_vendor_risk_analysis", "column": "vendor_relationship_days"}] | [] | False |
| B24 | AVG(vendor_relationship_days) | [{"table": "netsuite2_vendor_risk_analysis", "column": "vendor_relationship_days"}] | [] | False |
| B24 | AVG(CAST(vendor_relationship_days AS REAL)) | [{"table": "netsuite2_vendor_risk_analysis", "column": "vendor_relationship_days"}] | [] | False |
| B26 | MIN(days_since_last_transaction) | [{"table": "netsuite2_vendor_risk_analysis", "column": "days_since_last_transaction"}] | [] | False |
| B26 | MAX(days_since_last_transaction) | [{"table": "netsuite2_vendor_risk_analysis", "column": "days_since_last_transaction"}] | [] | False |
| B26 | AVG(days_since_last_transaction) | [{"table": "netsuite2_vendor_risk_analysis", "column": "days_since_last_transaction"}] | [] | False |
| B26 | AVG(CAST(days_since_last_transaction AS REAL)) | [{"table": "netsuite2_vendor_risk_analysis", "column": "days_since_last_transaction"}] | [] | False |
| B28 | MIN(total_transactions) | [{"table": "netsuite2_vendor_risk_analysis", "column": "total_transactions"}] | [] | False |
| B28 | MAX(total_transactions) | [{"table": "netsuite2_vendor_risk_analysis", "column": "total_transactions"}] | [] | False |
| B28 | AVG(total_transactions) | [{"table": "netsuite2_vendor_risk_analysis", "column": "total_transactions"}] | [] | False |
| B28 | AVG(CAST(total_transactions AS REAL)) | [{"table": "netsuite2_vendor_risk_analysis", "column": "total_transactions"}] | [] | False |


## S20

类别 `data`；来源 `query_db`；调用 `6c5c93ef5f6148c09ca04401e8cb038f`；状态 `success`。

```sql
SELECT vendor_id, vendor_name, vendor_category_name, total_vendor_spend, spend_concentration_ratio, strategic_importance_level, dependency_level, activity_status, days_since_last_transaction, contract_expiry_date, risk_level, vendor_risk_score
FROM netsuite2_vendor_risk_analysis
WHERE spend_concentration_ratio > 0.15 OR strategic_importance_level IN ('Mission Critical', 'High Strategic Value')
ORDER BY total_vendor_spend ASC
LIMIT 15
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-075/attempt-01/sql/S20.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-075/attempt-01/sql/S20.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-075/attempt-01/results/S20.rows.jsonl)；完整：True；SHA256：`f8a90f0c6f5a8189a6d2a7f3872f4ab5408ed8a82a90ba66e1e7e79aeb6d423b`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "netsuite2_vendor_risk_analysis", "kind": "base", "block": null, "base_tables": ["netsuite2_vendor_risk_analysis"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |


## S21

类别 `data`；来源 `query_db`；调用 `9de2069ad6504d69af03dd339fb714d2`；状态 `success`。

```sql
SELECT activity_status, COUNT(*) AS n
FROM netsuite2_vendor_risk_analysis
WHERE spend_concentration_ratio > 0.15 OR strategic_importance_level IN ('Mission Critical', 'High Strategic Value')
GROUP BY activity_status ORDER BY n DESC
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-075/attempt-01/sql/S21.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-075/attempt-01/sql/S21.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-075/attempt-01/results/S21.rows.jsonl)；完整：True；SHA256：`a91a483611d1db29e2b4cef9a1d5078987ca3106a15879db45da88720afb8fd6`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "netsuite2_vendor_risk_analysis", "kind": "base", "block": null, "base_tables": ["netsuite2_vendor_risk_analysis"]}] | [] | ["activity_status"] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |


## S22

类别 `data`；来源 `query_db`；调用 `efb47491a23e42ff999348fb7907dbd1`；状态 `success`。

```sql
SELECT
  SUM(CASE WHEN vendor_name LIKE 'Vendor_%' THEN 1 ELSE 0 END) AS synthetic_named,
  SUM(CASE WHEN vendor_category_name = 'General Supplier' THEN 1 ELSE 0 END) AS general_supplier_count,
  SUM(CASE WHEN total_vendor_spend < 1000 THEN 1 ELSE 0 END) AS tiny_spend,
  SUM(CASE WHEN spend_concentration_ratio = 1.0 THEN 1 ELSE 0 END) AS conc_100pct
FROM netsuite2_vendor_risk_analysis
WHERE spend_concentration_ratio > 0.15 OR strategic_importance_level IN ('Mission Critical', 'High Strategic Value')
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-075/attempt-01/sql/S22.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-075/attempt-01/sql/S22.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-075/attempt-01/results/S22.rows.jsonl)；完整：True；SHA256：`23cfa6cdb923b75b1736ce634bc9f00d9517b11e9df8475dcf6709472a39988d`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "netsuite2_vendor_risk_analysis", "kind": "base", "block": null, "base_tables": ["netsuite2_vendor_risk_analysis"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | SUM(CASE WHEN vendor_name LIKE 'Vendor_%' THEN 1 ELSE 0 END) | [] | [{"table": "netsuite2_vendor_risk_analysis", "column": "vendor_name"}] | False |
| B1 | SUM(CASE WHEN vendor_category_name = 'General Supplier' THEN 1 ELSE 0 END) | [] | [{"table": "netsuite2_vendor_risk_analysis", "column": "vendor_category_name"}] | False |
| B1 | SUM(CASE WHEN total_vendor_spend < 1000 THEN 1 ELSE 0 END) | [] | [{"table": "netsuite2_vendor_risk_analysis", "column": "total_vendor_spend"}] | False |
| B1 | SUM(CASE WHEN spend_concentration_ratio = 1.0 THEN 1 ELSE 0 END) | [] | [{"table": "netsuite2_vendor_risk_analysis", "column": "spend_concentration_ratio"}] | False |


## S23

类别 `data`；来源 `query_db`；调用 `b127ee948cc94e398a8a47df02e912ed`；状态 `success`。

```sql
SELECT vendor_name, COUNT(*) AS n FROM netsuite2_vendor_risk_analysis WHERE vendor_name LIKE 'Vendor_%' GROUP BY vendor_name ORDER BY n DESC LIMIT 20
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-075/attempt-01/sql/S23.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-075/attempt-01/sql/S23.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-075/attempt-01/results/S23.rows.jsonl)；完整：True；SHA256：`26156716b3bdbdbd9fd3a1e933729095093bdadd15e1d9d4df9a08c64f385ffa`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "netsuite2_vendor_risk_analysis", "kind": "base", "block": null, "base_tables": ["netsuite2_vendor_risk_analysis"]}] | [] | ["vendor_name"] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |


## S24

类别 `data`；来源 `query_db`；调用 `5d9d159d1a684757a709b5675463dead`；状态 `success`。

```sql
SELECT
  vendor_id, vendor_name, vendor_category_name, geographic_region,
  total_vendor_spend, spend_concentration_ratio, strategic_importance_level,
  -- Financial Resilience Metrics
  avg_payment_delay, overdue_payment_percentage, overdue_invoices, total_payable_invoices, financial_health_score,
  -- Operational Resilience Metrics
  quality_score, cybersecurity_score, innovation_capability_score,
  -- Market Resilience
  market_volatility_index, alternative_suppliers_count, price_volatility_coefficient,
  -- Strategic Resilience
  geographic_region, contract_expiry_date, environmental_rating, vendor_relationship_days, days_since_last_transaction,
  -- Additional
  dependency_level, relationship_stability, activity_status, risk_level, vendor_risk_score, supplier_tier, management_priority,
  switching_cost_estimate, total_payables, total_expenses, total_transactions, active_months
FROM netsuite2_vendor_risk_analysis
WHERE spend_concentration_ratio > 0.15 OR strategic_importance_level IN ('Mission Critical', 'High Strategic Value')
ORDER BY total_vendor_spend DESC
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-075/attempt-01/sql/S24.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-075/attempt-01/sql/S24.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-075/attempt-01/results/S24.rows.jsonl)；完整：True；SHA256：`e6240f8e1faa05026ddfb11359e67193f6a913d52979d3174eae05dc0c4fea4a`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "netsuite2_vendor_risk_analysis", "kind": "base", "block": null, "base_tables": ["netsuite2_vendor_risk_analysis"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |


## S25

类别 `data`；来源 `python`；调用 `1b8b8fb64c9742b2acc7d81706e2052e`；状态 `success`。

```sql

SELECT * FROM netsuite2_vendor_risk_analysis
WHERE spend_concentration_ratio > 0.15 OR strategic_importance_level IN ('Mission Critical', 'High Strategic Value')
ORDER BY total_vendor_spend DESC

```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-075/attempt-01/sql/S25.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-075/attempt-01/sql/S25.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-075/attempt-01/results/S25.rows.jsonl)；完整：True；SHA256：`ae3e5233a89ccab11d7227b3c54d5ae79a066ace0e6516e9cba34c75d07dae9b`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "netsuite2_vendor_risk_analysis", "kind": "base", "block": null, "base_tables": ["netsuite2_vendor_risk_analysis"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |


## S26

类别 `data`；来源 `query_db`；调用 `be83582058324dc6917d8138f2adceda`；状态 `success`。

```sql
SELECT geographic_region, COUNT(*) AS vendor_count, ROUND(SUM(total_vendor_spend),0) AS total_spend,
       ROUND(SUM(total_vendor_spend)/SUM(SUM(total_vendor_spend)) OVER ()*100,1) AS spend_pct
FROM netsuite2_vendor_risk_analysis
WHERE spend_concentration_ratio > 0.15 OR strategic_importance_level IN ('Mission Critical', 'High Strategic Value')
GROUP BY geographic_region
ORDER BY total_spend DESC
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-075/attempt-01/sql/S26.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-075/attempt-01/sql/S26.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-075/attempt-01/results/S26.rows.jsonl)；完整：True；SHA256：`bf259c7a30b05f1e8b3c44b0f6663f1e64a8f1bae7c092a60e46884d52318f6d`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "netsuite2_vendor_risk_analysis", "kind": "base", "block": null, "base_tables": ["netsuite2_vendor_risk_analysis"]}] | [] | ["geographic_region"] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |
| B1 | SUM(total_vendor_spend) | [{"table": "netsuite2_vendor_risk_analysis", "column": "total_vendor_spend"}] | [] | False |
| B1 | SUM(total_vendor_spend) | [{"table": "netsuite2_vendor_risk_analysis", "column": "total_vendor_spend"}] | [] | False |
| B1 | SUM(total_vendor_spend) | [{"table": "netsuite2_vendor_risk_analysis", "column": "total_vendor_spend"}] | [] | False |


## S27

类别 `data`；来源 `query_db`；调用 `f6df63de75a24180b519a9f62fca2acb`；状态 `success`。

```sql
SELECT vendor_category_name, COUNT(*) AS n, ROUND(SUM(total_vendor_spend),0) AS total_spend,
       ROUND(AVG(avg_payment_delay),1) AS avg_delay_days, ROUND(AVG(overdue_payment_percentage),1) AS avg_overdue_pct,
       ROUND(AVG(financial_health_score),1) AS avg_fin_health, ROUND(AVG(cybersecurity_score),1) AS avg_cyber,
       ROUND(AVG(quality_score),1) AS avg_quality, ROUND(AVG(innovation_capability_score),1) AS avg_innovation,
       ROUND(AVG(market_volatility_index),3) AS avg_mkt_vol, ROUND(AVG(price_volatility_coefficient),3) AS avg_price_vol
FROM netsuite2_vendor_risk_analysis
WHERE spend_concentration_ratio > 0.15 OR strategic_importance_level IN ('Mission Critical', 'High Strategic Value')
GROUP BY vendor_category_name
ORDER BY total_spend DESC
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-075/attempt-01/sql/S27.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-075/attempt-01/sql/S27.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-075/attempt-01/results/S27.rows.jsonl)；完整：True；SHA256：`f85610f8ec4255a1256ec434f2bf9b548dbfd5b7793f53574a1ec99b1893af1f`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "netsuite2_vendor_risk_analysis", "kind": "base", "block": null, "base_tables": ["netsuite2_vendor_risk_analysis"]}] | [] | ["vendor_category_name"] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |
| B1 | SUM(total_vendor_spend) | [{"table": "netsuite2_vendor_risk_analysis", "column": "total_vendor_spend"}] | [] | False |
| B1 | AVG(avg_payment_delay) | [{"table": "netsuite2_vendor_risk_analysis", "column": "avg_payment_delay"}] | [] | False |
| B1 | AVG(overdue_payment_percentage) | [{"table": "netsuite2_vendor_risk_analysis", "column": "overdue_payment_percentage"}] | [] | False |
| B1 | AVG(financial_health_score) | [{"table": "netsuite2_vendor_risk_analysis", "column": "financial_health_score"}] | [] | False |
| B1 | AVG(cybersecurity_score) | [{"table": "netsuite2_vendor_risk_analysis", "column": "cybersecurity_score"}] | [] | False |
| B1 | AVG(quality_score) | [{"table": "netsuite2_vendor_risk_analysis", "column": "quality_score"}] | [] | False |
| B1 | AVG(innovation_capability_score) | [{"table": "netsuite2_vendor_risk_analysis", "column": "innovation_capability_score"}] | [] | False |
| B1 | AVG(market_volatility_index) | [{"table": "netsuite2_vendor_risk_analysis", "column": "market_volatility_index"}] | [] | False |
| B1 | AVG(price_volatility_coefficient) | [{"table": "netsuite2_vendor_risk_analysis", "column": "price_volatility_coefficient"}] | [] | False |


## S28

类别 `data`；来源 `query_db`；调用 `39f12ebcb86d4002a7254bfdb15f419b`；状态 `success`。

```sql
SELECT contract_type, COUNT(*) AS n FROM netsuite2_vendor_risk_analysis
WHERE spend_concentration_ratio > 0.15 OR strategic_importance_level IN ('Mission Critical', 'High Strategic Value')
GROUP BY contract_type ORDER BY n DESC
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-075/attempt-01/sql/S28.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-075/attempt-01/sql/S28.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-075/attempt-01/results/S28.rows.jsonl)；完整：True；SHA256：`1ff705b64263239e2a67fb044686a257f2a3c4a86d950c4a5d39f975da390cac`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "netsuite2_vendor_risk_analysis", "kind": "base", "block": null, "base_tables": ["netsuite2_vendor_risk_analysis"]}] | [] | ["contract_type"] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |


## S29

类别 `data`；来源 `query_db`；调用 `bfd3798c0f9e4a8db9ed9ad852a4215e`；状态 `success`。

```sql
SELECT dependency_level, COUNT(*) AS n FROM netsuite2_vendor_risk_analysis
WHERE spend_concentration_ratio > 0.15 OR strategic_importance_level IN ('Mission Critical', 'High Strategic Value')
GROUP BY dependency_level ORDER BY n DESC
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-075/attempt-01/sql/S29.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-075/attempt-01/sql/S29.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-075/attempt-01/results/S29.rows.jsonl)；完整：True；SHA256：`a218076d13efdc45c6b0554ddb6b8065323997a0cdb7be300fc3e9b4fc350b29`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "netsuite2_vendor_risk_analysis", "kind": "base", "block": null, "base_tables": ["netsuite2_vendor_risk_analysis"]}] | [] | ["dependency_level"] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |

