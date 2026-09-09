# dacomp-076

We need to re-examine the effectiveness of our customer segmentation strategy. Please anal…

运行：已提交。官方未评分。全部 SQL 尝试/成功 23/23；数据 SQL 21/21；Python 12 次。

完整原题：

We need to re-examine the effectiveness of our customer segmentation strategy. Please analyze whether the current `profitability_segment` classifications align with actual customer performance, with a special focus on customer groups where the `retention_probability` deviates by more than 0.15 (i.e., the difference from the segment's average retention rate is greater than 15 percentage points). The analysis should focus on the characteristics of these "classification anomaly" customers across the following dimensions: transactional behavior (consistency between `transaction_count` and `avg_transactions_per_month`, and the level of `transaction_value_volatility`), seasonal patterns (the balance of transaction distribution across Q1-Q4), and value realization path (the alignment between `comprehensive_customer_score` and `total_revenue`). Using cluster analysis and decision tree methods, explore whether new dimensions such as transaction stability, seasonal preference, or customer lifecycle stage should be introduced into the existing segmentation model to improve segmentation precision and predictive accuracy.

| 表 | 行数 | 列数 |
| --- | --- | --- |
| netsuite2_customer_analytics | 149 | 28 |


实际路线（分析者依据 SQL/源码概括，不代表 Agent 自述）：SQL 识别细分留存异常 → Python 季节特征、聚类与决策树并再次分组汇总 → 客户细分改进分析。

数据库大小：57,344 字节。

## 数据 SQL

| SQL | 状态 | 基础表 | Join 输入/类型 | GROUP BY | 聚合表达式 | 结果行数 | 数据库 ms |
| --- | --- | --- | --- | --- | --- | --- | --- |
| [S3/Q1](#s3) | success | ["netsuite2_customer_analytics"] | 0 / {} | ["profitability_segment"] | ["COUNT(*)", "AVG(retention_probability)", "AVG(total_revenue)", "AVG(comprehensive_customer_score)", "AVG(transaction_count)", "AVG(avg_transactions_per_month)"] | 5 | 0.705 |
| [S4/Q2](#s4) | success | ["netsuite2_customer_analytics"] | 0 / {} | [] | ["COUNT(*)", "COUNT(DISTINCT profitability_segment)", "COUNT(DISTINCT value_tier)", "COUNT(DISTINCT lifecycle_stage)", "COUNT(DISTINCT seasonal_preference)", "COUNT(DISTINCT transaction_consistency)", "COUNT(DISTINCT growth_potential)", "COUNT(DISTINCT activity_status)", "COUNT(DISTINCT retention_category)", "COUNT(DISTINCT recommended_action)", "COUNT(DISTINCT engagement_frequency)", "COUNT(DISTINCT subsidiary_id)"] | 1 | 1.009 |
| [S5/Q3](#s5) | success | ["netsuite2_customer_analytics"] | 0 / {} | [] | [] | 20 | 0.355 |
| [S6/Q4](#s6) | success | ["netsuite2_customer_analytics"] | 0 / {} | [] | [] | 5 | 0.413 |
| [S7/Q5](#s7) | success | ["netsuite2_customer_analytics"] | 0 / {} | [] | [] | 3 | 0.34 |
| [S8/Q6](#s8) | success | ["netsuite2_customer_analytics"] | 0 / {} | [] | [] | 4 | 0.351 |
| [S9/Q7](#s9) | success | ["netsuite2_customer_analytics"] | 0 / {} | [] | [] | 4 | 0.353 |
| [S10/Q8](#s10) | success | ["netsuite2_customer_analytics"] | 0 / {} | [] | [] | 4 | 0.352 |
| [S11/Q9](#s11) | success | ["netsuite2_customer_analytics"] | 0 / {} | [] | [] | 4 | 0.352 |
| [S12/Q10](#s12) | success | ["netsuite2_customer_analytics"] | 0 / {} | [] | [] | 1 | 0.617 |
| [S13/Q11](#s13) | success | ["netsuite2_customer_analytics"] | 2 / {'INNER': 1} | ["profitability_segment"] | ["AVG(retention_probability)", "COUNT(*)"] | 47 | 0.938 |
| [S14/Q12](#s14) | success | ["netsuite2_customer_analytics"] | 0 / {} | ["customer_id"] | ["COUNT(*)"] | 6 | 0.479 |
| [S15/Q13](#s15) | success | ["netsuite2_customer_analytics"] | 0 / {} | [] | ["COUNT(*)", "COUNT(DISTINCT customer_id)"] | 1 | 0.445 |
| [S16/Q14](#s16) | success | ["netsuite2_customer_analytics"] | 0 / {} | [] | [] | 8 | 0.439 |
| [S17/Q15](#s17) | success | ["netsuite2_customer_analytics"] | 0 / {} | ["profitability_segment"] | ["COUNT(*)", "COUNT(DISTINCT customer_id)", "MIN(retention_probability)", "MAX(retention_probability)", "AVG(retention_probability)", "AVG(transaction_value_volatility)", "AVG(customer_age_days)", "AVG(net_profit)"] | 5 | 0.641 |
| [S18/Q16](#s18) | success | ["netsuite2_customer_analytics"] | 0 / {} | [] | ["MIN(retention_probability)", "MAX(retention_probability)", "AVG(retention_probability)", "COUNT(*) FILTER(WHERE retention_probability > 0.7)", "COUNT(*) FILTER(WHERE retention_probability < 0.3)"] | 1 | 0.422 |
| [S19/Q17](#s19) | success | ["netsuite2_customer_analytics"] | 2 / {'INNER': 1} | ["profitability_segment"] | ["AVG(retention_probability)", "COUNT(*)", "COUNT(DISTINCT customer_id)", "COUNT(*) FILTER(WHERE ABS(c.retention_probability - s.avg_retention) > 0.15)", "COUNT(DISTINCT c.customer_id) FILTER(WHERE ABS(c.retention_probability - s.avg_retention) > 0.15)"] | 1 | 0.759 |
| [S20/Q18](#s20) | success | ["netsuite2_customer_analytics"] | 2 / {'INNER': 1} | ["profitability_segment"] | ["AVG(retention_probability)"] | 149 | 1.772 |
| [S21/Q19](#s21) | success | ["netsuite2_customer_analytics"] | 2 / {'INNER': 1} | ["profitability_segment", "c.profitability_segment"] | ["AVG(retention_probability)", "COUNT(*)", "SUM(CASE WHEN ABS(c.retention_probability - s.avg_retention) > 0.15 THEN 1 ELSE 0 END)", "SUM(CASE WHEN (c.retention_probability - s.avg_retention) > 0.15 THEN 1 ELSE 0 END)", "SUM(CASE WHEN (s.avg_retention - c.retention_probability) > 0.15 THEN 1 ELSE 0 END)", "AVG(CASE WHEN ABS(c.retention_probability - s.avg_retention) > 0.15 THEN c.transaction_value_volatility END)", "AVG(CASE WHEN ABS(c.retention_probability - s.avg_retention) <= 0.15 THEN c.transaction_value_volatility END)", "AVG(CASE WHEN ABS(c.retention_probability - s.avg_retention) > 0.15 THEN c.comprehensive_customer_score END)", "AVG(CASE WHEN ABS(c.retention_probability - s.avg_retention) > 0.15 THEN c.total_revenue END)"] | 5 | 0.926 |
| [S22/Q20](#s22) | success | ["netsuite2_customer_analytics"] | 2 / {'INNER': 1} | ["profitability_segment", "c.profitability_segment", "CASE WHEN (c.retention_probability - s.avg_retention) > 0.15 THEN 'HighRetention' WHEN (s.avg_retention - c.retention_probability) > 0.15 THEN 'LowRetention' ELSE 'Normal' END"] | ["AVG(retention_probability)", "COUNT(*)", "AVG(c.retention_probability)", "AVG(c.transaction_value_volatility)", "AVG(c.total_revenue)", "AVG(c.comprehensive_customer_score)", "AVG(c.transaction_count)", "AVG(c.avg_transactions_per_month)", "AVG((c.q1_transactions + c.q2_transactions + c.q3_transactions + c.q4_transactions) * 1.0 / NULLIF(c.transaction_count, 0))", "AVG(CASE WHEN c.q4_transactions >= c.q1_transactions AND c.q4_transactions >= c.q2_transactions AND c.q4_transactions >= c.q3_transactions THEN 1 ELSE 0 END)"] | 11 | 1.02 |
| [S23/Q21](#s23) | success | ["netsuite2_customer_analytics"] | 2 / {'INNER': 1} | ["profitability_segment", "c.profitability_segment"] | ["AVG(retention_probability)", "AVG(CASE WHEN (c.retention_probability - s.avg_retention) > 0.15 THEN c.total_revenue END)", "AVG(CASE WHEN (s.avg_retention - c.retention_probability) > 0.15 THEN c.total_revenue END)", "AVG(CASE WHEN (c.retention_probability - s.avg_retention) > 0.15 THEN c.transaction_count END)", "AVG(CASE WHEN (s.avg_retention - c.retention_probability) > 0.15 THEN c.transaction_count END)", "AVG(CASE WHEN (c.retention_probability - s.avg_retention) > 0.15 THEN c.comprehensive_customer_score END)", "AVG(CASE WHEN (s.avg_retention - c.retention_probability) > 0.15 THEN c.comprehensive_customer_score END)", "AVG(CASE WHEN (c.retention_probability - s.avg_retention) > 0.15 THEN c.transaction_value_volatility END)", "AVG(CASE WHEN (s.avg_retention - c.retention_probability) > 0.15 THEN c.transaction_value_volatility END)"] | 5 | 1.238 |


## 元数据和设置

| SQL | 类别 | 状态 | 内容 |
| --- | --- | --- | --- |
| S1 | connection_setup | success | PRAGMA query_only=ON |
| S2 | metadata | success | SELECT name,sql FROM sqlite_master WHERE type='table' ORDER BY name |


## Python 与执行位置

人工源码审查：**database_first_violation**。聚类和决策树为题目要求的数值分析，算法内距离、中心均值和树节点计数不当作数据库优先违规。独立的盈利分组季度均值/比例、评分分箱留存均值、异常计数和季节偏好分布可由 SQL 完成，仍构成分组聚合偏离。 [证据](../reviews/dacomp-076.json)。

P1：Check availability of sklearn for clustering/decision trees and load the analysis dataset from the archived query results.

[源码](../../../runs/dsv4flash-db-first-full-01/dacomp-076/attempt-01/python/P1.py)；[输出](../../../runs/dsv4flash-db-first-full-01/dacomp-076/attempt-01/python/P1.stdout)；[错误](../../../runs/dsv4flash-db-first-full-01/dacomp-076/attempt-01/python/P1.stderr)。自动源码筛查未检出预设迁出信号；这不是全面语义合规证明。

P2：Load the full dataset with the anomaly flag (from archived SQL S20) into pandas for cluster analysis and decision-tree modeling, which SQLite cannot perform (no clustering/ML algorithms in SQLite).

[源码](../../../runs/dsv4flash-db-first-full-01/dacomp-076/attempt-01/python/P2.py)；[输出](../../../runs/dsv4flash-db-first-full-01/dacomp-076/attempt-01/python/P2.stdout)；[错误](../../../runs/dsv4flash-db-first-full-01/dacomp-076/attempt-01/python/P2.stderr)。自动源码筛查未检出预设迁出信号；这不是全面语义合规证明。

P3：Locate the archived result files for the analysis dataset in the Python environment.

[源码](../../../runs/dsv4flash-db-first-full-01/dacomp-076/attempt-01/python/P3.py)；[输出](../../../runs/dsv4flash-db-first-full-01/dacomp-076/attempt-01/python/P3.stdout)；[错误](../../../runs/dsv4flash-db-first-full-01/dacomp-076/attempt-01/python/P3.stderr)。自动源码筛查未检出预设迁出信号；这不是全面语义合规证明。

P4：Load full annotated dataset from archived SQL results for cluster analysis, decision tree, and visualization - tasks SQLite cannot perform.

[源码](../../../runs/dsv4flash-db-first-full-01/dacomp-076/attempt-01/python/P4.py)；[输出](../../../runs/dsv4flash-db-first-full-01/dacomp-076/attempt-01/python/P4.stdout)；[错误](../../../runs/dsv4flash-db-first-full-01/dacomp-076/attempt-01/python/P4.stderr)。自动源码筛查未检出预设迁出信号；这不是全面语义合规证明。

P5：Compute derived transactional, seasonal, and value-alignment features and compare anomaly vs non-anomaly groups - this involves derived arithmetic, residual regression and statistical tests that go beyond SQLite's aggregation.

[源码](../../../runs/dsv4flash-db-first-full-01/dacomp-076/attempt-01/python/P5.py)；[输出](../../../runs/dsv4flash-db-first-full-01/dacomp-076/attempt-01/python/P5.stdout)；[错误](../../../runs/dsv4flash-db-first-full-01/dacomp-076/attempt-01/python/P5.stderr)。自动源码筛查未检出预设迁出信号；这不是全面语义合规证明。

P6：Compare anomaly vs non-anomaly customers across transactional, seasonal, and value-alignment dimensions using statistical tests, since SQLite cannot perform these tests.

[源码](../../../runs/dsv4flash-db-first-full-01/dacomp-076/attempt-01/python/P6.py)；[输出](../../../runs/dsv4flash-db-first-full-01/dacomp-076/attempt-01/python/P6.stdout)；[错误](../../../runs/dsv4flash-db-first-full-01/dacomp-076/attempt-01/python/P6.stderr)。自动源码筛查未检出预设迁出信号；这不是全面语义合规证明。

P7：Perform k-means clustering (not available in SQLite) on the key derived features to discover new latent dimensions that could improve segmentation.

[源码](../../../runs/dsv4flash-db-first-full-01/dacomp-076/attempt-01/python/P7.py)；[输出](../../../runs/dsv4flash-db-first-full-01/dacomp-076/attempt-01/python/P7.stdout)；[错误](../../../runs/dsv4flash-db-first-full-01/dacomp-076/attempt-01/python/P7.stderr)。自动源码筛查未检出预设迁出信号；这不是全面语义合规证明。

P8：Build a decision tree classifier (not available in SQLite) to predict anomaly status and identify which dimensions best discriminate classification anomalies.

[源码](../../../runs/dsv4flash-db-first-full-01/dacomp-076/attempt-01/python/P8.py)；[输出](../../../runs/dsv4flash-db-first-full-01/dacomp-076/attempt-01/python/P8.stdout)；[错误](../../../runs/dsv4flash-db-first-full-01/dacomp-076/attempt-01/python/P8.stderr)。检出需人工核验的 SQL 可实现操作：groupby(；不能仅凭理由判为合规。

P9：Re-run the decision tree analysis with one-hot encoded categorical features (without the unavailable sklearn import) to find which segmentation dimensions best separate classification anomalies.

[源码](../../../runs/dsv4flash-db-first-full-01/dacomp-076/attempt-01/python/P9.py)；[输出](../../../runs/dsv4flash-db-first-full-01/dacomp-076/attempt-01/python/P9.stdout)；[错误](../../../runs/dsv4flash-db-first-full-01/dacomp-076/attempt-01/python/P9.stderr)。自动源码筛查未检出预设迁出信号；这不是全面语义合规证明。

P10：Create comprehensive visualization figures for the report, showing anomaly patterns, cluster characteristics, seasonal distributions, and decision tree insights.

[源码](../../../runs/dsv4flash-db-first-full-01/dacomp-076/attempt-01/python/P10.py)；[输出](../../../runs/dsv4flash-db-first-full-01/dacomp-076/attempt-01/python/P10.stdout)；[错误](../../../runs/dsv4flash-db-first-full-01/dacomp-076/attempt-01/python/P10.stderr)。检出需人工核验的 SQL 可实现操作：groupby(；不能仅凭理由判为合规。

P11：Compute correlations between retention_probability and candidate new segmentation dimensions (transaction stability, seasonal concentration, lifecycle) to quantify alignment, and run a regression to quantify how much of retention variance is unexplained by existing value metrics.

[源码](../../../runs/dsv4flash-db-first-full-01/dacomp-076/attempt-01/python/P11.py)；[输出](../../../runs/dsv4flash-db-first-full-01/dacomp-076/attempt-01/python/P11.stdout)；[错误](../../../runs/dsv4flash-db-first-full-01/dacomp-076/attempt-01/python/P11.stderr)。检出需人工核验的 SQL 可实现操作：groupby(；不能仅凭理由判为合规。

P12：Create final report figures: retention deviation distribution, retention vs segment with anomaly bands, and the seasonal concentration effect on retention in anomaly-prone segments.

[源码](../../../runs/dsv4flash-db-first-full-01/dacomp-076/attempt-01/python/P12.py)；[输出](../../../runs/dsv4flash-db-first-full-01/dacomp-076/attempt-01/python/P12.stdout)；[错误](../../../runs/dsv4flash-db-first-full-01/dacomp-076/attempt-01/python/P12.stderr)。检出需人工核验的 SQL 可实现操作：groupby(；不能仅凭理由判为合规。

## 优化机会

已验证候选。筛选限于精确 SQL、相同自包含 CTE、相同单表完整过滤、可分解单表聚合；未覆盖任意 Join 等价和一般谓词蕴含。全部候选都是 offline，未测在线预测。

| 候选 | 类型 | 已有结果 | 覆盖 SQL | 后续次数 | 中间行数 | 验证 | 成本 |
| --- | --- | --- | --- | --- | --- | --- | --- |
| C1 | common subexpression | False | ["S19", "S20", "S21", "S22", "S23"] | 4 | 5 | verified | Not benchmarked; correctness alone does not establish net speedup. |


已验证覆盖（含触发查询、候选并集去重）：5/21 条成功数据 SQL。正确性仅针对当前数据库快照；未测性能的候选不能声称已加速。

[完整 build/rewrite 与比较证据](dacomp-076.analysis.json)。

### C1：common subexpression

Identical self-contained CTE body across queries.

原查询 [S19](#s19), [S20](#s20), [S21](#s21), [S22](#s22), [S23](#s23) → 新增共享状态 C1 → 后续 4 次可复用。该构建点为事后假设，不代表 Agent 当时预知后续。

构建定义：

```sql
SELECT profitability_segment, AVG(retention_probability) AS avg_retention FROM netsuite2_customer_analytics GROUP BY profitability_segment
```

受益查询 S19 的改写示例：

```sql
WITH segment_stats AS (SELECT * FROM temp.reuse_candidate) SELECT COUNT(*) AS total_rows, COUNT(DISTINCT customer_id) AS unique_customers, COUNT(*) FILTER(WHERE ABS(c.retention_probability - s.avg_retention) > 0.15) AS anomaly_rows, COUNT(DISTINCT c.customer_id) FILTER(WHERE ABS(c.retention_probability - s.avg_retention) > 0.15) AS anomaly_customers FROM netsuite2_customer_analytics AS c JOIN segment_stats AS s ON c.profitability_segment = s.profitability_segment
```

| 原 SQL | 列名一致 | 结果一致 | 比较方法 |
| --- | --- | --- | --- |
| S19 | True | True | exact_multiset |
| S20 | True | True | exact_multiset |
| S21 | True | True | ordered_numeric_tolerance |
| S22 | True | True | ordered_numeric_tolerance |
| S23 | True | True | exact_multiset |


验证状态：verified；成本结论：Not benchmarked; correctness alone does not establish net speedup.

结果依赖：自动记录 SQL→Python 的接口父调用，以及源码中引用归档文件的消费者；字面值相同不认定因果。模型方向选择需要人工读取消息，尚未做全面因果标注。

[原始报告](../../../runs/dsv4flash-db-first-full-01/dacomp-076/attempt-01/answer.md)；[统一消息](../../../runs/dsv4flash-db-first-full-01/dacomp-076/attempt-01/messages.jsonl)；[原始 OpenCode 事件](../../../runs/dsv4flash-db-first-full-01/dacomp-076/attempt-01/opencode.jsonl)；[SQL 引擎日志](../../../runs/dsv4flash-db-first-full-01/dacomp-076/attempt-01/sql_journal.jsonl)。

[可读报告（本地图片链接规范化）](../answers/dacomp-076.md)。原始回答保留，分析结论未改写。

## S1

类别 `connection_setup`；来源 `connection`；调用 `3222eff0357548e49a412a64051d1ecb`；状态 `success`。

```sql
PRAGMA query_only=ON
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-076/attempt-01/sql/S1.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-076/attempt-01/sql/S1.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-076/attempt-01/results/S1.rows.jsonl)；完整：True；SHA256：`e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`。

## S2

类别 `metadata`；来源 `list_db`；调用 `3222eff0357548e49a412a64051d1ecb`；状态 `success`。

```sql
SELECT name,sql FROM sqlite_master WHERE type='table' ORDER BY name
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-076/attempt-01/sql/S2.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-076/attempt-01/sql/S2.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-076/attempt-01/results/S2.rows.jsonl)；完整：True；SHA256：`f62385ee2e056f369cae0a08c0376e8a84fba5c21b2f75c4211ca2acc2f5f48c`。

## S3

类别 `data`；来源 `query_db`；调用 `e1a57c85701145dc8eb83ad1ba8c315e`；状态 `success`。

```sql
SELECT profitability_segment, COUNT(*) as cnt, 
       AVG(retention_probability) as avg_retention, 
       AVG(total_revenue) as avg_revenue,
       AVG(comprehensive_customer_score) as avg_score,
       AVG(transaction_count) as avg_tx_count,
       AVG(avg_transactions_per_month) as avg_tx_month
FROM netsuite2_customer_analytics
GROUP BY profitability_segment
ORDER BY cnt DESC
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-076/attempt-01/sql/S3.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-076/attempt-01/sql/S3.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-076/attempt-01/results/S3.rows.jsonl)；完整：True；SHA256：`eddd2026fa94f4637ed0c4f5ae7d4a62609cf1e03553669a145ed1acd849550b`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "netsuite2_customer_analytics", "kind": "base", "block": null, "base_tables": ["netsuite2_customer_analytics"]}] | [] | ["profitability_segment"] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |
| B1 | AVG(retention_probability) | [{"table": "netsuite2_customer_analytics", "column": "retention_probability"}] | [] | False |
| B1 | AVG(total_revenue) | [{"table": "netsuite2_customer_analytics", "column": "total_revenue"}] | [] | False |
| B1 | AVG(comprehensive_customer_score) | [{"table": "netsuite2_customer_analytics", "column": "comprehensive_customer_score"}] | [] | False |
| B1 | AVG(transaction_count) | [{"table": "netsuite2_customer_analytics", "column": "transaction_count"}] | [] | False |
| B1 | AVG(avg_transactions_per_month) | [{"table": "netsuite2_customer_analytics", "column": "avg_transactions_per_month"}] | [] | False |


## S4

类别 `data`；来源 `query_db`；调用 `b7e2e60298f94539871e06bbdfdb6c5c`；状态 `success`。

```sql
SELECT COUNT(*) AS total_customers,
       COUNT(DISTINCT profitability_segment) AS n_segments,
       COUNT(DISTINCT value_tier) AS n_tiers,
       COUNT(DISTINCT lifecycle_stage) AS n_lifecycle,
       COUNT(DISTINCT seasonal_preference) AS n_seasonal,
       COUNT(DISTINCT transaction_consistency) AS n_tx_consistency,
       COUNT(DISTINCT growth_potential) AS n_growth,
       COUNT(DISTINCT activity_status) AS n_activity,
       COUNT(DISTINCT retention_category) AS n_retention_cat,
       COUNT(DISTINCT recommended_action) AS n_rec_action,
       COUNT(DISTINCT engagement_frequency) AS n_engagement,
       COUNT(DISTINCT subsidiary_id) AS n_subsidiary
FROM netsuite2_customer_analytics
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-076/attempt-01/sql/S4.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-076/attempt-01/sql/S4.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-076/attempt-01/results/S4.rows.jsonl)；完整：True；SHA256：`118e84f194316d7a8d8bc9a80ba3fc0fa36b62ba9412f75ebf7db150b4510c83`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "netsuite2_customer_analytics", "kind": "base", "block": null, "base_tables": ["netsuite2_customer_analytics"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |
| B1 | COUNT(DISTINCT profitability_segment) | [{"table": "netsuite2_customer_analytics", "column": "profitability_segment"}] | [] | False |
| B1 | COUNT(DISTINCT value_tier) | [{"table": "netsuite2_customer_analytics", "column": "value_tier"}] | [] | False |
| B1 | COUNT(DISTINCT lifecycle_stage) | [{"table": "netsuite2_customer_analytics", "column": "lifecycle_stage"}] | [] | False |
| B1 | COUNT(DISTINCT seasonal_preference) | [{"table": "netsuite2_customer_analytics", "column": "seasonal_preference"}] | [] | False |
| B1 | COUNT(DISTINCT transaction_consistency) | [{"table": "netsuite2_customer_analytics", "column": "transaction_consistency"}] | [] | False |
| B1 | COUNT(DISTINCT growth_potential) | [{"table": "netsuite2_customer_analytics", "column": "growth_potential"}] | [] | False |
| B1 | COUNT(DISTINCT activity_status) | [{"table": "netsuite2_customer_analytics", "column": "activity_status"}] | [] | False |
| B1 | COUNT(DISTINCT retention_category) | [{"table": "netsuite2_customer_analytics", "column": "retention_category"}] | [] | False |
| B1 | COUNT(DISTINCT recommended_action) | [{"table": "netsuite2_customer_analytics", "column": "recommended_action"}] | [] | False |
| B1 | COUNT(DISTINCT engagement_frequency) | [{"table": "netsuite2_customer_analytics", "column": "engagement_frequency"}] | [] | False |
| B1 | COUNT(DISTINCT subsidiary_id) | [{"table": "netsuite2_customer_analytics", "column": "subsidiary_id"}] | [] | False |


## S5

类别 `data`；来源 `query_db`；调用 `ba03180000b646aba80e73689931d0a7`；状态 `success`。

```sql
SELECT value_tier, lifecycle_stage, seasonal_preference, transaction_consistency, 
       growth_potential, activity_status, retention_category, engagement_frequency
FROM netsuite2_customer_analytics
LIMIT 20
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-076/attempt-01/sql/S5.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-076/attempt-01/sql/S5.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-076/attempt-01/results/S5.rows.jsonl)；完整：True；SHA256：`8c05decde47d33fbfc59e2a33cb1166bc5d7164b5e03aeb9ea87529d5f35cc4e`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "netsuite2_customer_analytics", "kind": "base", "block": null, "base_tables": ["netsuite2_customer_analytics"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |


## S6

类别 `data`；来源 `query_db`；调用 `ffb5dd0b2bc94cc7a4dcd1b4e6fada6a`；状态 `success`。

```sql
SELECT DISTINCT value_tier FROM netsuite2_customer_analytics ORDER BY value_tier
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-076/attempt-01/sql/S6.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-076/attempt-01/sql/S6.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-076/attempt-01/results/S6.rows.jsonl)；完整：True；SHA256：`0247280cee89907e617e0bf91816fd7b470c0f7c042bae332cbeda2b75c5b59b`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "netsuite2_customer_analytics", "kind": "base", "block": null, "base_tables": ["netsuite2_customer_analytics"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |


## S7

类别 `data`；来源 `query_db`；调用 `7d062462686d49d9a509e2e11e1b7d96`；状态 `success`。

```sql
SELECT DISTINCT lifecycle_stage FROM netsuite2_customer_analytics ORDER BY lifecycle_stage
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-076/attempt-01/sql/S7.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-076/attempt-01/sql/S7.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-076/attempt-01/results/S7.rows.jsonl)；完整：True；SHA256：`58f3dfb44da472c53ae41c8ca07eacc3599c1c24cfce4ae829fab45f3bf8b125`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "netsuite2_customer_analytics", "kind": "base", "block": null, "base_tables": ["netsuite2_customer_analytics"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |


## S8

类别 `data`；来源 `query_db`；调用 `1db89b11bfba435985bcadad6e7c8573`；状态 `success`。

```sql
SELECT DISTINCT seasonal_preference FROM netsuite2_customer_analytics ORDER BY seasonal_preference
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-076/attempt-01/sql/S8.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-076/attempt-01/sql/S8.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-076/attempt-01/results/S8.rows.jsonl)；完整：True；SHA256：`da15c468fd1dbdcf431defef3108ef8de634e2110f20da0e26449796f0165ea0`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "netsuite2_customer_analytics", "kind": "base", "block": null, "base_tables": ["netsuite2_customer_analytics"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |


## S9

类别 `data`；来源 `query_db`；调用 `c55b484d44254cd8834016c29cf82930`；状态 `success`。

```sql
SELECT DISTINCT transaction_consistency FROM netsuite2_customer_analytics ORDER BY transaction_consistency
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-076/attempt-01/sql/S9.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-076/attempt-01/sql/S9.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-076/attempt-01/results/S9.rows.jsonl)；完整：True；SHA256：`dada16c05ba4efc58129f46c02ec00214931b701edc6d6f3aeabacd46da5c862`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "netsuite2_customer_analytics", "kind": "base", "block": null, "base_tables": ["netsuite2_customer_analytics"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |


## S10

类别 `data`；来源 `query_db`；调用 `a605409bed3f42b9978c1dae244bd933`；状态 `success`。

```sql
SELECT DISTINCT activity_status FROM netsuite2_customer_analytics ORDER BY activity_status
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-076/attempt-01/sql/S10.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-076/attempt-01/sql/S10.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-076/attempt-01/results/S10.rows.jsonl)；完整：True；SHA256：`a215925227aafa53cced287b4fc222f734d3b920bf33040553f60a41634703ce`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "netsuite2_customer_analytics", "kind": "base", "block": null, "base_tables": ["netsuite2_customer_analytics"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |


## S11

类别 `data`；来源 `query_db`；调用 `1312171d53a2441f856734ca559276f4`；状态 `success`。

```sql
SELECT DISTINCT engagement_frequency FROM netsuite2_customer_analytics ORDER BY engagement_frequency
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-076/attempt-01/sql/S11.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-076/attempt-01/sql/S11.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-076/attempt-01/results/S11.rows.jsonl)；完整：True；SHA256：`8d2cedf415b5fee046d8589c016badbf53e6297ed5383fb1960c19c76639d3d8`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "netsuite2_customer_analytics", "kind": "base", "block": null, "base_tables": ["netsuite2_customer_analytics"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |


## S12

类别 `data`；来源 `query_db`；调用 `bbafb1330c75407ea5fac5c7ea99f3c0`；状态 `success`。

```sql
SELECT DISTINCT retention_category FROM netsuite2_customer_analytics ORDER BY retention_category
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-076/attempt-01/sql/S12.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-076/attempt-01/sql/S12.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-076/attempt-01/results/S12.rows.jsonl)；完整：True；SHA256：`be98a5e250abda6d47df275015a0ef0fea8f3d177ca79244952f8ab2b29a19bf`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "netsuite2_customer_analytics", "kind": "base", "block": null, "base_tables": ["netsuite2_customer_analytics"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |


## S13

类别 `data`；来源 `query_db`；调用 `6c7b7790433a4c25af957ab0ce015754`；状态 `success`。

```sql
WITH segment_stats AS (
    SELECT profitability_segment, 
           AVG(retention_probability) AS avg_retention,
           COUNT(*) AS seg_count
    FROM netsuite2_customer_analytics
    GROUP BY profitability_segment
)
SELECT c.customer_id, c.customer_name, c.profitability_segment, 
       c.retention_probability, s.avg_retention,
       c.retention_probability - s.avg_retention AS deviation,
       c.total_revenue, c.transaction_count, c.avg_transactions_per_month,
       c.comprehensive_customer_score, c.transaction_value_volatility,
       c.lifecycle_stage, c.value_tier, c.seasonal_preference,
       c.transaction_consistency, c.activity_status, c.engagement_frequency,
       c.q1_transactions, c.q2_transactions, c.q3_transactions, c.q4_transactions,
       c.customer_age_days, c.growth_potential
FROM netsuite2_customer_analytics c
JOIN segment_stats s ON c.profitability_segment = s.profitability_segment
WHERE ABS(c.retention_probability - s.avg_retention) > 0.15
ORDER BY ABS(c.retention_probability - s.avg_retention) DESC
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-076/attempt-01/sql/S13.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-076/attempt-01/sql/S13.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-076/attempt-01/results/S13.rows.jsonl)；完整：True；SHA256：`a26a4ff34ae916f7fa0ded0c8f697969741f4fcf10abae354ffe807a9706d4f8`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "netsuite2_customer_analytics", "kind": "base", "block": null, "base_tables": ["netsuite2_customer_analytics"]}] | [] | ["profitability_segment"] |
| B2 | [{"alias": "c", "kind": "base", "block": null, "base_tables": ["netsuite2_customer_analytics"]}, {"alias": "s", "kind": "derived", "block": "B1", "base_tables": ["netsuite2_customer_analytics"]}] | [{"type": "INNER", "right": "segment_stats AS s", "on": "c.profitability_segment = s.profitability_segment", "using": []}] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | AVG(retention_probability) | [{"table": "netsuite2_customer_analytics", "column": "retention_probability"}] | [] | False |
| B1 | COUNT(*) | [] | [] | True |


## S14

类别 `data`；来源 `query_db`；调用 `97b373b908e341f097c0c55327faf998`；状态 `success`。

```sql
SELECT customer_id, COUNT(*) AS cnt
FROM netsuite2_customer_analytics
GROUP BY customer_id
HAVING cnt > 1
ORDER BY cnt DESC
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-076/attempt-01/sql/S14.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-076/attempt-01/sql/S14.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-076/attempt-01/results/S14.rows.jsonl)；完整：True；SHA256：`70958d36f4d26c0e4b067502d68a470020c76b7b407037fcc430d8fdb1351584`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "netsuite2_customer_analytics", "kind": "base", "block": null, "base_tables": ["netsuite2_customer_analytics"]}] | [] | ["customer_id"] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |


## S15

类别 `data`；来源 `query_db`；调用 `35674d4d41a640839898d661f85ea236`；状态 `success`。

```sql
SELECT COUNT(*) AS total_rows, COUNT(DISTINCT customer_id) AS unique_customers
FROM netsuite2_customer_analytics
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-076/attempt-01/sql/S15.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-076/attempt-01/sql/S15.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-076/attempt-01/results/S15.rows.jsonl)；完整：True；SHA256：`8b802bdcf1121169d8fb8531de519ee9333388c7181c7d230cac7aef62629b29`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "netsuite2_customer_analytics", "kind": "base", "block": null, "base_tables": ["netsuite2_customer_analytics"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |
| B1 | COUNT(DISTINCT customer_id) | [{"table": "netsuite2_customer_analytics", "column": "customer_id"}] | [] | False |


## S16

类别 `data`；来源 `query_db`；调用 `6701c675869e437eb06e5aa87555d723`；状态 `success`。

```sql
SELECT customer_id, customer_name, profitability_segment, retention_probability, total_revenue, transaction_count, comprehensive_customer_score, lifecycle_stage, value_tier, seasonal_preference, transaction_consistency, customer_analytics_id
FROM netsuite2_customer_analytics
WHERE customer_id = 'NET01146543590'
ORDER BY retention_probability
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-076/attempt-01/sql/S16.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-076/attempt-01/sql/S16.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-076/attempt-01/results/S16.rows.jsonl)；完整：True；SHA256：`44c6c57e4dd8b5ea6fd96c3e584b98ea40828a6054ec7ce85a3b0e616b564dfa`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "netsuite2_customer_analytics", "kind": "base", "block": null, "base_tables": ["netsuite2_customer_analytics"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |


## S17

类别 `data`；来源 `query_db`；调用 `80da7c59c628444da36b82494dd61670`；状态 `success`。

```sql
SELECT profitability_segment,
       COUNT(*) AS n_rows,
       COUNT(DISTINCT customer_id) AS n_customers,
       MIN(retention_probability) AS min_ret,
       MAX(retention_probability) AS max_ret,
       AVG(retention_probability) AS avg_ret,
       AVG(transaction_value_volatility) AS avg_volatility,
       AVG(customer_age_days) AS avg_age,
       AVG(net_profit) AS avg_net_profit
FROM netsuite2_customer_analytics
GROUP BY profitability_segment
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-076/attempt-01/sql/S17.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-076/attempt-01/sql/S17.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-076/attempt-01/results/S17.rows.jsonl)；完整：True；SHA256：`8a5a3640fe1afed6448f393ececfe8261fddc4240c28713d4bb9701501a593c1`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "netsuite2_customer_analytics", "kind": "base", "block": null, "base_tables": ["netsuite2_customer_analytics"]}] | [] | ["profitability_segment"] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |
| B1 | COUNT(DISTINCT customer_id) | [{"table": "netsuite2_customer_analytics", "column": "customer_id"}] | [] | False |
| B1 | MIN(retention_probability) | [{"table": "netsuite2_customer_analytics", "column": "retention_probability"}] | [] | False |
| B1 | MAX(retention_probability) | [{"table": "netsuite2_customer_analytics", "column": "retention_probability"}] | [] | False |
| B1 | AVG(retention_probability) | [{"table": "netsuite2_customer_analytics", "column": "retention_probability"}] | [] | False |
| B1 | AVG(transaction_value_volatility) | [{"table": "netsuite2_customer_analytics", "column": "transaction_value_volatility"}] | [] | False |
| B1 | AVG(customer_age_days) | [{"table": "netsuite2_customer_analytics", "column": "customer_age_days"}] | [] | False |
| B1 | AVG(net_profit) | [{"table": "netsuite2_customer_analytics", "column": "net_profit"}] | [] | False |


## S18

类别 `data`；来源 `query_db`；调用 `2e48ebd212454867a1c288eb8ec9c5ea`；状态 `success`。

```sql
SELECT MIN(retention_probability) AS min_ret, MAX(retention_probability) AS max_ret,
       AVG(retention_probability) AS avg_ret, 
       COUNT(*) FILTER (WHERE retention_probability > 0.7) AS high_ret,
       COUNT(*) FILTER (WHERE retention_probability < 0.3) AS low_ret
FROM netsuite2_customer_analytics
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-076/attempt-01/sql/S18.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-076/attempt-01/sql/S18.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-076/attempt-01/results/S18.rows.jsonl)；完整：True；SHA256：`7937044de8a1da835c9ff1df0aef2108696a790551ce706666f7ada2476d3be6`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "netsuite2_customer_analytics", "kind": "base", "block": null, "base_tables": ["netsuite2_customer_analytics"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | MIN(retention_probability) | [{"table": "netsuite2_customer_analytics", "column": "retention_probability"}] | [] | False |
| B1 | MAX(retention_probability) | [{"table": "netsuite2_customer_analytics", "column": "retention_probability"}] | [] | False |
| B1 | AVG(retention_probability) | [{"table": "netsuite2_customer_analytics", "column": "retention_probability"}] | [] | False |
| B1 | COUNT(*) FILTER(WHERE retention_probability > 0.7) | [] | [{"table": "netsuite2_customer_analytics", "column": "retention_probability"}] | True |
| B1 | COUNT(*) FILTER(WHERE retention_probability < 0.3) | [] | [{"table": "netsuite2_customer_analytics", "column": "retention_probability"}] | True |


## S19

类别 `data`；来源 `query_db`；调用 `6eb2acd87eac4730b1c2f7c3576b9381`；状态 `success`。

```sql
WITH segment_stats AS (
    SELECT profitability_segment, 
           AVG(retention_probability) AS avg_retention
    FROM netsuite2_customer_analytics
    GROUP BY profitability_segment
)
SELECT COUNT(*) AS total_rows,
       COUNT(DISTINCT customer_id) AS unique_customers,
       COUNT(*) FILTER (WHERE ABS(c.retention_probability - s.avg_retention) > 0.15) AS anomaly_rows,
       COUNT(DISTINCT c.customer_id) FILTER (WHERE ABS(c.retention_probability - s.avg_retention) > 0.15) AS anomaly_customers
FROM netsuite2_customer_analytics c
JOIN segment_stats s ON c.profitability_segment = s.profitability_segment
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-076/attempt-01/sql/S19.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-076/attempt-01/sql/S19.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-076/attempt-01/results/S19.rows.jsonl)；完整：True；SHA256：`04592272f389121793d8a67d92efdb3d5d8d282ca1710313d6933455ffb075ea`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "netsuite2_customer_analytics", "kind": "base", "block": null, "base_tables": ["netsuite2_customer_analytics"]}] | [] | ["profitability_segment"] |
| B2 | [{"alias": "c", "kind": "base", "block": null, "base_tables": ["netsuite2_customer_analytics"]}, {"alias": "s", "kind": "derived", "block": "B1", "base_tables": ["netsuite2_customer_analytics"]}] | [{"type": "INNER", "right": "segment_stats AS s", "on": "c.profitability_segment = s.profitability_segment", "using": []}] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | AVG(retention_probability) | [{"table": "netsuite2_customer_analytics", "column": "retention_probability"}] | [] | False |
| B2 | COUNT(*) | [] | [] | True |
| B2 | COUNT(DISTINCT customer_id) | [{"table": "netsuite2_customer_analytics", "column": "customer_id"}] | [] | False |
| B2 | COUNT(*) FILTER(WHERE ABS(c.retention_probability - s.avg_retention) > 0.15) | [] | [{"table": "netsuite2_customer_analytics", "column": "retention_probability"}, {"table": "netsuite2_customer_analytics", "column": "retention_probability"}] | True |
| B2 | COUNT(DISTINCT c.customer_id) FILTER(WHERE ABS(c.retention_probability - s.avg_retention) > 0.15) | [{"table": "netsuite2_customer_analytics", "column": "customer_id"}] | [{"table": "netsuite2_customer_analytics", "column": "retention_probability"}, {"table": "netsuite2_customer_analytics", "column": "retention_probability"}] | False |


## S20

类别 `data`；来源 `query_db`；调用 `a6cd58d75e3049248579b8d236c85cd1`；状态 `success`。

```sql
WITH segment_stats AS (
    SELECT profitability_segment, 
           AVG(retention_probability) AS avg_retention
    FROM netsuite2_customer_analytics
    GROUP BY profitability_segment
)
SELECT c.*, 
       s.avg_retention,
       c.retention_probability - s.avg_retention AS deviation,
       CASE WHEN ABS(c.retention_probability - s.avg_retention) > 0.15 THEN 1 ELSE 0 END AS is_anomaly,
       CASE WHEN c.retention_probability > s.avg_retention THEN 1 ELSE 0 END AS is_above_avg
FROM netsuite2_customer_analytics c
JOIN segment_stats s ON c.profitability_segment = s.profitability_segment
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-076/attempt-01/sql/S20.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-076/attempt-01/sql/S20.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-076/attempt-01/results/S20.rows.jsonl)；完整：True；SHA256：`0408b3e0982e34e10304fd80db86ee3b30aa0eb1e03bde75ec4ed1afb51e8fc5`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "netsuite2_customer_analytics", "kind": "base", "block": null, "base_tables": ["netsuite2_customer_analytics"]}] | [] | ["profitability_segment"] |
| B2 | [{"alias": "c", "kind": "base", "block": null, "base_tables": ["netsuite2_customer_analytics"]}, {"alias": "s", "kind": "derived", "block": "B1", "base_tables": ["netsuite2_customer_analytics"]}] | [{"type": "INNER", "right": "segment_stats AS s", "on": "c.profitability_segment = s.profitability_segment", "using": []}] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | AVG(retention_probability) | [{"table": "netsuite2_customer_analytics", "column": "retention_probability"}] | [] | False |


## S21

类别 `data`；来源 `query_db`；调用 `07991c6983bc4cb8b2fa0ae8543e4129`；状态 `success`。

```sql
WITH segment_stats AS (
    SELECT profitability_segment, AVG(retention_probability) AS avg_retention
    FROM netsuite2_customer_analytics
    GROUP BY profitability_segment
)
SELECT c.profitability_segment,
       COUNT(*) AS n_rows,
       SUM(CASE WHEN ABS(c.retention_probability - s.avg_retention) > 0.15 THEN 1 ELSE 0 END) AS anomaly_rows,
       SUM(CASE WHEN (c.retention_probability - s.avg_retention) > 0.15 THEN 1 ELSE 0 END) AS high_anomaly,
       SUM(CASE WHEN (s.avg_retention - c.retention_probability) > 0.15 THEN 1 ELSE 0 END) AS low_anomaly,
       ROUND(AVG(CASE WHEN ABS(c.retention_probability - s.avg_retention) > 0.15 THEN c.transaction_value_volatility END), 3) AS anomaly_volatility,
       ROUND(AVG(CASE WHEN ABS(c.retention_probability - s.avg_retention) <= 0.15 THEN c.transaction_value_volatility END), 3) AS normal_volatility,
       ROUND(AVG(CASE WHEN ABS(c.retention_probability - s.avg_retention) > 0.15 THEN c.comprehensive_customer_score END), 1) AS anomaly_score,
       ROUND(AVG(CASE WHEN ABS(c.retention_probability - s.avg_retention) > 0.15 THEN c.total_revenue END), 1) AS anomaly_revenue
FROM netsuite2_customer_analytics c
JOIN segment_stats s ON c.profitability_segment = s.profitability_segment
GROUP BY c.profitability_segment
ORDER BY anomaly_rows DESC
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-076/attempt-01/sql/S21.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-076/attempt-01/sql/S21.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-076/attempt-01/results/S21.rows.jsonl)；完整：True；SHA256：`e74b57423863ee72d6a714e835aee4d2fe136b9f4506d2443d01d89710225ec8`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "netsuite2_customer_analytics", "kind": "base", "block": null, "base_tables": ["netsuite2_customer_analytics"]}] | [] | ["profitability_segment"] |
| B2 | [{"alias": "c", "kind": "base", "block": null, "base_tables": ["netsuite2_customer_analytics"]}, {"alias": "s", "kind": "derived", "block": "B1", "base_tables": ["netsuite2_customer_analytics"]}] | [{"type": "INNER", "right": "segment_stats AS s", "on": "c.profitability_segment = s.profitability_segment", "using": []}] | ["c.profitability_segment"] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | AVG(retention_probability) | [{"table": "netsuite2_customer_analytics", "column": "retention_probability"}] | [] | False |
| B2 | COUNT(*) | [] | [] | True |
| B2 | SUM(CASE WHEN ABS(c.retention_probability - s.avg_retention) > 0.15 THEN 1 ELSE 0 END) | [] | [{"table": "netsuite2_customer_analytics", "column": "retention_probability"}, {"table": "netsuite2_customer_analytics", "column": "retention_probability"}] | False |
| B2 | SUM(CASE WHEN (c.retention_probability - s.avg_retention) > 0.15 THEN 1 ELSE 0 END) | [] | [{"table": "netsuite2_customer_analytics", "column": "retention_probability"}, {"table": "netsuite2_customer_analytics", "column": "retention_probability"}] | False |
| B2 | SUM(CASE WHEN (s.avg_retention - c.retention_probability) > 0.15 THEN 1 ELSE 0 END) | [] | [{"table": "netsuite2_customer_analytics", "column": "retention_probability"}, {"table": "netsuite2_customer_analytics", "column": "retention_probability"}] | False |
| B2 | AVG(CASE WHEN ABS(c.retention_probability - s.avg_retention) > 0.15 THEN c.transaction_value_volatility END) | [{"table": "netsuite2_customer_analytics", "column": "transaction_value_volatility"}] | [{"table": "netsuite2_customer_analytics", "column": "retention_probability"}, {"table": "netsuite2_customer_analytics", "column": "retention_probability"}] | False |
| B2 | AVG(CASE WHEN ABS(c.retention_probability - s.avg_retention) <= 0.15 THEN c.transaction_value_volatility END) | [{"table": "netsuite2_customer_analytics", "column": "transaction_value_volatility"}] | [{"table": "netsuite2_customer_analytics", "column": "retention_probability"}, {"table": "netsuite2_customer_analytics", "column": "retention_probability"}] | False |
| B2 | AVG(CASE WHEN ABS(c.retention_probability - s.avg_retention) > 0.15 THEN c.comprehensive_customer_score END) | [{"table": "netsuite2_customer_analytics", "column": "comprehensive_customer_score"}] | [{"table": "netsuite2_customer_analytics", "column": "retention_probability"}, {"table": "netsuite2_customer_analytics", "column": "retention_probability"}] | False |
| B2 | AVG(CASE WHEN ABS(c.retention_probability - s.avg_retention) > 0.15 THEN c.total_revenue END) | [{"table": "netsuite2_customer_analytics", "column": "total_revenue"}] | [{"table": "netsuite2_customer_analytics", "column": "retention_probability"}, {"table": "netsuite2_customer_analytics", "column": "retention_probability"}] | False |


## S22

类别 `data`；来源 `query_db`；调用 `1a0ebad9a9fe400aa30ff910ac8d3b50`；状态 `success`。

```sql
WITH segment_stats AS (
    SELECT profitability_segment, AVG(retention_probability) AS avg_retention
    FROM netsuite2_customer_analytics
    GROUP BY profitability_segment
)
SELECT c.profitability_segment,
       CASE WHEN (c.retention_probability - s.avg_retention) > 0.15 THEN 'HighRetention' 
            WHEN (s.avg_retention - c.retention_probability) > 0.15 THEN 'LowRetention'
            ELSE 'Normal' END AS anomaly_dir,
       COUNT(*) AS n,
       ROUND(AVG(c.retention_probability), 3) AS avg_ret,
       ROUND(AVG(c.transaction_value_volatility), 3) AS avg_volatility,
       ROUND(AVG(c.total_revenue), 1) AS avg_rev,
       ROUND(AVG(c.comprehensive_customer_score), 1) AS avg_score,
       ROUND(AVG(c.transaction_count), 1) AS avg_tx,
       ROUND(AVG(c.avg_transactions_per_month), 2) AS avg_tx_month,
       ROUND(AVG((c.q1_transactions+c.q2_transactions+c.q3_transactions+c.q4_transactions)*1.0/NULLIF(c.transaction_count,0)), 3) AS avg_q_total_tx_ratio,
       ROUND(AVG(CASE WHEN c.q4_transactions >= c.q1_transactions AND c.q4_transactions >= c.q2_transactions AND c.q4_transactions >= c.q3_transactions THEN 1 ELSE 0 END), 3) AS q4_dominant_share
FROM netsuite2_customer_analytics c
JOIN segment_stats s ON c.profitability_segment = s.profitability_segment
GROUP BY c.profitability_segment, anomaly_dir
ORDER BY c.profitability_segment, anomaly_dir
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-076/attempt-01/sql/S22.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-076/attempt-01/sql/S22.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-076/attempt-01/results/S22.rows.jsonl)；完整：True；SHA256：`0f5df29f63f00dd88ad25f0685cd3093a17a182ebab7353fc3ca5487af6aee8d`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "netsuite2_customer_analytics", "kind": "base", "block": null, "base_tables": ["netsuite2_customer_analytics"]}] | [] | ["profitability_segment"] |
| B2 | [{"alias": "c", "kind": "base", "block": null, "base_tables": ["netsuite2_customer_analytics"]}, {"alias": "s", "kind": "derived", "block": "B1", "base_tables": ["netsuite2_customer_analytics"]}] | [{"type": "INNER", "right": "segment_stats AS s", "on": "c.profitability_segment = s.profitability_segment", "using": []}] | ["c.profitability_segment", "CASE WHEN (c.retention_probability - s.avg_retention) > 0.15 THEN 'HighRetention' WHEN (s.avg_retention - c.retention_probability) > 0.15 THEN 'LowRetention' ELSE 'Normal' END"] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | AVG(retention_probability) | [{"table": "netsuite2_customer_analytics", "column": "retention_probability"}] | [] | False |
| B2 | COUNT(*) | [] | [] | True |
| B2 | AVG(c.retention_probability) | [{"table": "netsuite2_customer_analytics", "column": "retention_probability"}] | [] | False |
| B2 | AVG(c.transaction_value_volatility) | [{"table": "netsuite2_customer_analytics", "column": "transaction_value_volatility"}] | [] | False |
| B2 | AVG(c.total_revenue) | [{"table": "netsuite2_customer_analytics", "column": "total_revenue"}] | [] | False |
| B2 | AVG(c.comprehensive_customer_score) | [{"table": "netsuite2_customer_analytics", "column": "comprehensive_customer_score"}] | [] | False |
| B2 | AVG(c.transaction_count) | [{"table": "netsuite2_customer_analytics", "column": "transaction_count"}] | [] | False |
| B2 | AVG(c.avg_transactions_per_month) | [{"table": "netsuite2_customer_analytics", "column": "avg_transactions_per_month"}] | [] | False |
| B2 | AVG((c.q1_transactions + c.q2_transactions + c.q3_transactions + c.q4_transactions) * 1.0 / NULLIF(c.transaction_count, 0)) | [{"table": "netsuite2_customer_analytics", "column": "transaction_count"}, {"table": "netsuite2_customer_analytics", "column": "q4_transactions"}, {"table": "netsuite2_customer_analytics", "column": "q3_transactions"}, {"table": "netsuite2_customer_analytics", "column": "q1_transactions"}, {"table": "netsuite2_customer_analytics", "column": "q2_transactions"}] | [] | False |
| B2 | AVG(CASE WHEN c.q4_transactions >= c.q1_transactions AND c.q4_transactions >= c.q2_transactions AND c.q4_transactions >= c.q3_transactions THEN 1 ELSE 0 END) | [] | [{"table": "netsuite2_customer_analytics", "column": "q4_transactions"}, {"table": "netsuite2_customer_analytics", "column": "q3_transactions"}, {"table": "netsuite2_customer_analytics", "column": "q4_transactions"}, {"table": "netsuite2_customer_analytics", "column": "q1_transactions"}, {"table": "netsuite2_customer_analytics", "column": "q4_transactions"}, {"table": "netsuite2_customer_analytics", "column": "q2_transactions"}] | False |


## S23

类别 `data`；来源 `query_db`；调用 `e405512f306948559ab4828e6042a66a`；状态 `success`。

```sql
WITH segment_stats AS (
    SELECT profitability_segment, AVG(retention_probability) AS avg_retention
    FROM netsuite2_customer_analytics
    GROUP BY profitability_segment
)
SELECT c.profitability_segment,
       ROUND(AVG(CASE WHEN (c.retention_probability - s.avg_retention) > 0.15 THEN c.total_revenue END),1) AS high_ret_avg_rev,
       ROUND(AVG(CASE WHEN (s.avg_retention - c.retention_probability) > 0.15 THEN c.total_revenue END),1) AS low_ret_avg_rev,
       ROUND(AVG(CASE WHEN (c.retention_probability - s.avg_retention) > 0.15 THEN c.transaction_count END),2) AS high_ret_avg_tx,
       ROUND(AVG(CASE WHEN (s.avg_retention - c.retention_probability) > 0.15 THEN c.transaction_count END),2) AS low_ret_avg_tx,
       ROUND(AVG(CASE WHEN (c.retention_probability - s.avg_retention) > 0.15 THEN c.comprehensive_customer_score END),1) AS high_ret_avg_score,
       ROUND(AVG(CASE WHEN (s.avg_retention - c.retention_probability) > 0.15 THEN c.comprehensive_customer_score END),1) AS low_ret_avg_score,
       ROUND(AVG(CASE WHEN (c.retention_probability - s.avg_retention) > 0.15 THEN c.transaction_value_volatility END),3) AS high_ret_avg_vol,
       ROUND(AVG(CASE WHEN (s.avg_retention - c.retention_probability) > 0.15 THEN c.transaction_value_volatility END),3) AS low_ret_avg_vol
FROM netsuite2_customer_analytics c
JOIN segment_stats s ON c.profitability_segment = s.profitability_segment
GROUP BY c.profitability_segment
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-076/attempt-01/sql/S23.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-076/attempt-01/sql/S23.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-076/attempt-01/results/S23.rows.jsonl)；完整：True；SHA256：`3770562c7c1c3d7239fd14f9c38b93b87a69dd100f1bdbbfa4cf918d7f13bce3`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "netsuite2_customer_analytics", "kind": "base", "block": null, "base_tables": ["netsuite2_customer_analytics"]}] | [] | ["profitability_segment"] |
| B2 | [{"alias": "c", "kind": "base", "block": null, "base_tables": ["netsuite2_customer_analytics"]}, {"alias": "s", "kind": "derived", "block": "B1", "base_tables": ["netsuite2_customer_analytics"]}] | [{"type": "INNER", "right": "segment_stats AS s", "on": "c.profitability_segment = s.profitability_segment", "using": []}] | ["c.profitability_segment"] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | AVG(retention_probability) | [{"table": "netsuite2_customer_analytics", "column": "retention_probability"}] | [] | False |
| B2 | AVG(CASE WHEN (c.retention_probability - s.avg_retention) > 0.15 THEN c.total_revenue END) | [{"table": "netsuite2_customer_analytics", "column": "total_revenue"}] | [{"table": "netsuite2_customer_analytics", "column": "retention_probability"}, {"table": "netsuite2_customer_analytics", "column": "retention_probability"}] | False |
| B2 | AVG(CASE WHEN (s.avg_retention - c.retention_probability) > 0.15 THEN c.total_revenue END) | [{"table": "netsuite2_customer_analytics", "column": "total_revenue"}] | [{"table": "netsuite2_customer_analytics", "column": "retention_probability"}, {"table": "netsuite2_customer_analytics", "column": "retention_probability"}] | False |
| B2 | AVG(CASE WHEN (c.retention_probability - s.avg_retention) > 0.15 THEN c.transaction_count END) | [{"table": "netsuite2_customer_analytics", "column": "transaction_count"}] | [{"table": "netsuite2_customer_analytics", "column": "retention_probability"}, {"table": "netsuite2_customer_analytics", "column": "retention_probability"}] | False |
| B2 | AVG(CASE WHEN (s.avg_retention - c.retention_probability) > 0.15 THEN c.transaction_count END) | [{"table": "netsuite2_customer_analytics", "column": "transaction_count"}] | [{"table": "netsuite2_customer_analytics", "column": "retention_probability"}, {"table": "netsuite2_customer_analytics", "column": "retention_probability"}] | False |
| B2 | AVG(CASE WHEN (c.retention_probability - s.avg_retention) > 0.15 THEN c.comprehensive_customer_score END) | [{"table": "netsuite2_customer_analytics", "column": "comprehensive_customer_score"}] | [{"table": "netsuite2_customer_analytics", "column": "retention_probability"}, {"table": "netsuite2_customer_analytics", "column": "retention_probability"}] | False |
| B2 | AVG(CASE WHEN (s.avg_retention - c.retention_probability) > 0.15 THEN c.comprehensive_customer_score END) | [{"table": "netsuite2_customer_analytics", "column": "comprehensive_customer_score"}] | [{"table": "netsuite2_customer_analytics", "column": "retention_probability"}, {"table": "netsuite2_customer_analytics", "column": "retention_probability"}] | False |
| B2 | AVG(CASE WHEN (c.retention_probability - s.avg_retention) > 0.15 THEN c.transaction_value_volatility END) | [{"table": "netsuite2_customer_analytics", "column": "transaction_value_volatility"}] | [{"table": "netsuite2_customer_analytics", "column": "retention_probability"}, {"table": "netsuite2_customer_analytics", "column": "retention_probability"}] | False |
| B2 | AVG(CASE WHEN (s.avg_retention - c.retention_probability) > 0.15 THEN c.transaction_value_volatility END) | [{"table": "netsuite2_customer_analytics", "column": "transaction_value_volatility"}] | [{"table": "netsuite2_customer_analytics", "column": "retention_probability"}, {"table": "netsuite2_customer_analytics", "column": "retention_probability"}] | False |

