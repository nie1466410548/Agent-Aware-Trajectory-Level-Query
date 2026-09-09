# dacomp-070

Analyze the decay patterns of user acquisition cost-efficiency for each region and device …

运行：已提交。官方未评分。全部 SQL 尝试/成功 25/25；数据 SQL 23/23；Python 11 次。

完整原题：

Analyze the decay patterns of user acquisition cost-efficiency for each region and device type combination over the past 6 months. Identify the non-linear relationship between `store_listing_conversion_rate` and `quality_score`/`crash_rate_per_1k`. By constructing a multi-dimensional user value decay model, predict optimization strategies for `revenue_per_active_device` under different market maturities. Additionally, quantify the interaction effect of app update frequency on `active_devices_last_30_days` and `rolling_total_average_rating`. Provide data-driven recommendations for formulating differentiated product iteration and market investment strategies.

| 表 | 行数 | 列数 |
| --- | --- | --- |
| google_play__country_report | 12544 | 26 |
| google_play__device_report | 18816 | 17 |
| google_play__os_version_report | 14112 | 19 |
| google_play__time_series_trends | 1568 | 40 |


实际路线（分析者依据 SQL/源码概括，不代表 Agent 自述）：SQL 提取地区设备与应用时序 → Python 再分组、分箱并拟合衰退及交互模型 → 产品和市场建议。

数据库大小：6,406,144 字节。

## 数据 SQL

| SQL | 状态 | 基础表 | Join 输入/类型 | GROUP BY | 聚合表达式 | 结果行数 | 数据库 ms |
| --- | --- | --- | --- | --- | --- | --- | --- |
| [S3/Q1](#s3) | success | ["google_play__time_series_trends"] | 0 / {} | [] | ["MIN(date_day)", "MAX(date_day)", "COUNT(*)"] | 1 | 0.938 |
| [S4/Q2](#s4) | success | ["google_play__country_report"] | 0 / {} | ["region"] | ["COUNT(*)", "COUNT(DISTINCT country_short)", "MIN(date_day)", "MAX(date_day)"] | 4 | 7.75 |
| [S5/Q3](#s5) | success | ["google_play__time_series_trends"] | 0 / {} | ["package_name"] | ["COUNT(*)", "MIN(date_day)", "MAX(date_day)"] | 8 | 1.143 |
| [S6/Q4](#s6) | success | ["google_play__device_report"] | 0 / {} | ["device"] | ["COUNT(*)", "MIN(date_day)", "MAX(date_day)"] | 12 | 8.831 |
| [S7/Q5](#s7) | success | ["google_play__country_report"] | 0 / {} | ["STRFTIME('%Y-%m', date_day)", "region"] | ["COUNT(*)", "SUM(store_listing_visitors)", "SUM(store_listing_acquisitions)", "SUM(device_installs)", "SUM(device_uninstalls)", "SUM(update_events)", "SUM(active_devices_last_30_days)", "SUM(store_listing_acquisitions)", "SUM(store_listing_visitors)"] | 28 | 16.357 |
| [S8/Q6](#s8) | success | ["google_play__time_series_trends"] | 0 / {} | ["STRFTIME('%Y-%m', date_day)", "package_name"] | ["AVG(quality_score)", "AVG(crash_rate_per_1k)", "AVG(anr_rate_per_1k)", "AVG(revenue_per_active_device)", "AVG(active_devices)", "AVG(daily_revenue)", "AVG(daily_churn_rate)", "AVG(daily_install_uninstall_ratio)"] | 56 | 2.865 |
| [S9/Q7](#s9) | success | ["google_play__country_report"] | 0 / {} | ["STRFTIME('%Y-%m', date_day)", "region"] | ["SUM(device_upgrades)", "SUM(update_events)", "SUM(store_listing_acquisitions)", "SUM(store_listing_visitors)", "SUM(store_listing_visitors)", "SUM(store_listing_acquisitions)"] | 28 | 15.017 |
| [S10/Q8](#s10) | success | ["google_play__time_series_trends"] | 0 / {} | ["package_name"] | ["COUNT(*)", "MIN(quality_score)", "MAX(quality_score)", "MIN(crash_rate_per_1k)", "MAX(crash_rate_per_1k)", "MIN(revenue_per_active_device)", "MAX(revenue_per_active_device)", "AVG(revenue_per_active_device)"] | 8 | 1.642 |
| [S11/Q9](#s11) | success | ["google_play__device_report"] | 0 / {} | ["STRFTIME('%Y-%m', date_day)", "device"] | ["SUM(update_events)", "SUM(device_installs)", "SUM(device_uninstalls)", "SUM(active_devices_last_30_days)", "AVG(rolling_total_average_rating)"] | 84 | 25.761 |
| [S12/Q10](#s12) | success | ["google_play__country_report"] | 0 / {} | ["STRFTIME('%Y-%m', date_day)", "region"] | ["SUM(update_events)", "SUM(active_devices_last_30_days)", "AVG(rolling_total_average_rating)", "SUM(store_listing_acquisitions)", "SUM(store_listing_visitors)", "SUM(store_listing_visitors)", "SUM(store_listing_acquisitions)", "SUM(device_installs)", "SUM(store_listing_acquisitions)"] | 28 | 16.47 |
| [S13/Q11](#s13) | success | ["google_play__time_series_trends"] | 0 / {} | ["STRFTIME('%Y-%m', date_day)", "package_name"] | ["AVG(quality_score)", "AVG(crash_rate_per_1k)", "AVG(anr_rate_per_1k)", "AVG(revenue_per_active_device)", "AVG(active_devices)", "AVG(ma_7d_quality)", "AVG(ma_30d_quality)", "AVG(wow_install_growth_rate)", "AVG(wow_revenue_growth_rate)", "AVG(install_volatility_coefficient)", "AVG(revenue_volatility_coefficient)"] | 56 | 3.276 |
| [S14/Q12](#s14) | success | ["google_play__country_report", "google_play__device_report"] | 2 / {'INNER': 1} | ["cr.region", "dr.device", "STRFTIME('%Y-%m', cr.date_day)"] | ["SUM(cr.store_listing_visitors)", "SUM(cr.store_listing_acquisitions)", "SUM(dr.device_installs)", "SUM(dr.device_uninstalls)", "SUM(dr.update_events)", "SUM(dr.active_devices_last_30_days)", "AVG(dr.rolling_total_average_rating)"] | 336 | 333.961 |
| [S15/Q13](#s15) | success | ["google_play__country_report", "google_play__time_series_trends"] | 2 / {'INNER': 1} | ["STRFTIME('%Y-%m', cr.date_day)", "cr.region", "cr.package_name"] | ["SUM(cr.store_listing_visitors)", "SUM(cr.store_listing_acquisitions)", "SUM(cr.device_installs)", "SUM(cr.update_events)", "SUM(cr.active_devices_last_30_days)", "SUM(cr.store_listing_acquisitions)", "AVG(cr.rolling_total_average_rating)", "AVG(ts.quality_score)", "AVG(ts.crash_rate_per_1k)", "AVG(ts.revenue_per_active_device)", "AVG(ts.daily_churn_rate)", "SUM(cr.store_listing_acquisitions)", "SUM(cr.store_listing_visitors)"] | 224 | 36.137 |
| [S16/Q14](#s16) | success | ["google_play__time_series_trends"] | 0 / {} | ["install_trend", "revenue_trend", "install_stability", "performance_momentum", "risk_growth_profile", "anomaly_flag", "daily_performance_vs_baseline"] | ["COUNT(*)"] | 259 | 3.899 |
| [S17/Q15](#s17) | success | ["google_play__os_version_report"] | 0 / {} | ["android_os_version"] | ["COUNT(*)", "SUM(crashes)", "SUM(anrs)", "SUM(device_installs)", "SUM(active_devices_last_30_days)"] | 9 | 7.978 |
| [S18/Q16](#s18) | success | ["google_play__country_report", "google_play__device_report"] | 2 / {'INNER': 1} | ["cr.region", "dr.device", "STRFTIME('%Y-%m', cr.date_day)"] | ["SUM(cr.store_listing_visitors)", "SUM(cr.store_listing_acquisitions)", "SUM(dr.device_installs)", "SUM(dr.device_uninstalls)", "SUM(dr.update_events)", "SUM(dr.active_devices_last_30_days)", "AVG(dr.rolling_total_average_rating)"] | 336 | 331.12 |
| [S19/Q17](#s19) | success | ["google_play__country_report", "google_play__time_series_trends"] | 2 / {'INNER': 1} | ["STRFTIME('%Y-%m', cr.date_day)", "cr.region", "cr.package_name"] | ["SUM(cr.store_listing_visitors)", "SUM(cr.store_listing_acquisitions)", "SUM(cr.device_installs)", "SUM(cr.update_events)", "SUM(cr.active_devices_last_30_days)", "AVG(cr.rolling_total_average_rating)", "AVG(ts.quality_score)", "AVG(ts.crash_rate_per_1k)", "AVG(ts.revenue_per_active_device)", "AVG(ts.daily_churn_rate)"] | 224 | 35.423 |
| [S20/Q18](#s20) | success | ["google_play__time_series_trends"] | 0 / {} | ["STRFTIME('%Y-%m', date_day)", "package_name"] | ["AVG(quality_score)", "AVG(crash_rate_per_1k)", "AVG(anr_rate_per_1k)", "AVG(revenue_per_active_device)", "AVG(active_devices)", "AVG(ma_7d_quality)", "AVG(ma_30d_quality)", "AVG(wow_install_growth_rate)", "AVG(wow_revenue_growth_rate)", "AVG(install_volatility_coefficient)", "AVG(revenue_volatility_coefficient)"] | 56 | 3.209 |
| [S21/Q19](#s21) | success | ["google_play__time_series_trends"] | 0 / {} | [] | [] | 1568 | 9.833 |
| [S22/Q20](#s22) | success | ["google_play__country_report"] | 0 / {} | [] | [] | 12544 | 36.873 |
| [S23/Q21](#s23) | success | ["google_play__device_report"] | 0 / {} | [] | [] | 18816 | 44.058 |
| [S24/Q22](#s24) | success | ["google_play__country_report", "google_play__time_series_trends"] | 2 / {'INNER': 1} | ["cr.date_day", "cr.region", "cr.package_name"] | ["AVG(ts.quality_score)", "AVG(ts.crash_rate_per_1k)", "AVG(ts.revenue_per_active_device)", "SUM(cr.store_listing_visitors)", "SUM(cr.store_listing_acquisitions)", "SUM(cr.store_listing_visitors)"] | 6272 | 36.811 |
| [S25/Q23](#s25) | success | ["google_play__country_report", "google_play__time_series_trends"] | 2 / {'INNER': 1} | ["cr.date_day", "cr.region", "cr.package_name"] | ["SUM(cr.store_listing_visitors)", "SUM(cr.store_listing_acquisitions)", "AVG(ts.quality_score)", "AVG(ts.crash_rate_per_1k)", "AVG(ts.revenue_per_active_device)", "AVG(ts.active_devices)", "AVG(ts.daily_churn_rate)", "SUM(cr.store_listing_acquisitions)", "SUM(cr.store_listing_visitors)"] | 6272 | 44.07 |


## 元数据和设置

| SQL | 类别 | 状态 | 内容 |
| --- | --- | --- | --- |
| S1 | connection_setup | success | PRAGMA query_only=ON |
| S2 | metadata | success | SELECT name,sql FROM sqlite_master WHERE type='table' ORDER BY name |


## Python 与执行位置

人工源码审查：**database_first_violation**。Python 进行线性、非线性和交互效应回归是统计补充；但在其前后按地区、月份、设备、应用及质量分箱计算均值和数量，仍可在 SQL 内完成。模型残差平方和等不作为违规聚合证据。 [证据](../reviews/dacomp-070.json)。

P1：Load all monthly aggregated data for analysis. Cannot do the comprehensive non-linear modeling, decay regression, and interaction analysis in SQL alone - need Python for statistical modeling, polynomial fitting, and visualization.

[源码](../../../runs/dsv4flash-db-first-full-01/dacomp-070/attempt-01/python/P1.py)；[输出](../../../runs/dsv4flash-db-first-full-01/dacomp-070/attempt-01/python/P1.stdout)；[错误](../../../runs/dsv4flash-db-first-full-01/dacomp-070/attempt-01/python/P1.stderr)。自动源码筛查未检出预设迁出信号；这不是全面语义合规证明。

P2：Load monthly aggregate datasets saved from SQL query archives into pandas for statistical analysis and visualization that requires Python (polynomial regression, correlation, interaction models).

[源码](../../../runs/dsv4flash-db-first-full-01/dacomp-070/attempt-01/python/P2.py)；[输出](../../../runs/dsv4flash-db-first-full-01/dacomp-070/attempt-01/python/P2.stdout)；[错误](../../../runs/dsv4flash-db-first-full-01/dacomp-070/attempt-01/python/P2.stderr)。检出需人工核验的 SQL 可实现操作：groupby(；不能仅凭理由判为合规。

P3：Check actual column names from the JSON lines files to debug pandas loading issue.

[源码](../../../runs/dsv4flash-db-first-full-01/dacomp-070/attempt-01/python/P3.py)；[输出](../../../runs/dsv4flash-db-first-full-01/dacomp-070/attempt-01/python/P3.stdout)；[错误](../../../runs/dsv4flash-db-first-full-01/dacomp-070/attempt-01/python/P3.stderr)。自动源码筛查未检出预设迁出信号；这不是全面语义合规证明。

P4：Fetch monthly aggregate datasets through the logged db.query interface (which returns proper column names), for pandas-based statistical modeling and visualization in Python.

[源码](../../../runs/dsv4flash-db-first-full-01/dacomp-070/attempt-01/python/P4.py)；[输出](../../../runs/dsv4flash-db-first-full-01/dacomp-070/attempt-01/python/P4.stdout)；[错误](../../../runs/dsv4flash-db-first-full-01/dacomp-070/attempt-01/python/P4.stderr)。检出需人工核验的 SQL 可实现操作：groupby(, .query(；不能仅凭理由判为合规。

P5：Analyze acquisition cost-efficiency decay patterns by region×device combination using linear regression on conversion rate over time. Python needed for statistical regression and visualization.

[源码](../../../runs/dsv4flash-db-first-full-01/dacomp-070/attempt-01/python/P5.py)；[输出](../../../runs/dsv4flash-db-first-full-01/dacomp-070/attempt-01/python/P5.stdout)；[错误](../../../runs/dsv4flash-db-first-full-01/dacomp-070/attempt-01/python/P5.stderr)。检出需人工核验的 SQL 可实现操作：groupby(, sort_values(；不能仅凭理由判为合规。

P6：Analyze acquisition cost-efficiency decay patterns by region×device combination using linear regression. Python needed for statistical regression and visualization.

[源码](../../../runs/dsv4flash-db-first-full-01/dacomp-070/attempt-01/python/P6.py)；[输出](../../../runs/dsv4flash-db-first-full-01/dacomp-070/attempt-01/python/P6.stdout)；[错误](../../../runs/dsv4flash-db-first-full-01/dacomp-070/attempt-01/python/P6.stderr)。检出需人工核验的 SQL 可实现操作：groupby(, sort_values(；不能仅凭理由判为合规。

P7：Analyze non-linear relationship between store_listing_conversion_rate and quality_score/crash_rate_per_1k using polynomial and log transforms. Python/NumPy needed for polynomial fitting, F-test, and joint non-linear model.

[源码](../../../runs/dsv4flash-db-first-full-01/dacomp-070/attempt-01/python/P7.py)；[输出](../../../runs/dsv4flash-db-first-full-01/dacomp-070/attempt-01/python/P7.stdout)；[错误](../../../runs/dsv4flash-db-first-full-01/dacomp-070/attempt-01/python/P7.stderr)。自动源码筛查未检出预设迁出信号；这不是全面语义合规证明。

P8：Build multi-dimensional user value decay model for revenue_per_active_device. Python needed for regression modeling, market maturity classification, and visualization. Daily-level data fetch enables granular analysis.

[源码](../../../runs/dsv4flash-db-first-full-01/dacomp-070/attempt-01/python/P8.py)；[输出](../../../runs/dsv4flash-db-first-full-01/dacomp-070/attempt-01/python/P8.stdout)；[错误](../../../runs/dsv4flash-db-first-full-01/dacomp-070/attempt-01/python/P8.stderr)。检出需人工核验的 SQL 可实现操作：groupby(, .query(；不能仅凭理由判为合规。

P9：Quantify the interaction effect of app update frequency on active_devices_last_30_days and rolling_total_average_rating. Python needed for regression with interaction terms, F-test for significance, and visualization across regions and devices.

[源码](../../../runs/dsv4flash-db-first-full-01/dacomp-070/attempt-01/python/P9.py)；[输出](../../../runs/dsv4flash-db-first-full-01/dacomp-070/attempt-01/python/P9.stdout)；[错误](../../../runs/dsv4flash-db-first-full-01/dacomp-070/attempt-01/python/P9.stderr)。检出需人工核验的 SQL 可实现操作：groupby(, .query(, sort_values(；不能仅凭理由判为合规。

P10：Perform daily-level analysis of non-linear relationships between conversion rate, quality score, and crash rate. Python needed for granular statistical analysis, polynomial fitting, and threshold analysis by quartile.

[源码](../../../runs/dsv4flash-db-first-full-01/dacomp-070/attempt-01/python/P10.py)；[输出](../../../runs/dsv4flash-db-first-full-01/dacomp-070/attempt-01/python/P10.stdout)；[错误](../../../runs/dsv4flash-db-first-full-01/dacomp-070/attempt-01/python/P10.stderr)。检出需人工核验的 SQL 可实现操作：groupby(, .query(；不能仅凭理由判为合规。

P11：Deep-dive into non-linear relationships using binned means, full model with fixed effects, and value decay curves (rpad vs market scale). Python needed for polynomial/OLS regression with interaction terms and elasticity estimation.

[源码](../../../runs/dsv4flash-db-first-full-01/dacomp-070/attempt-01/python/P11.py)；[输出](../../../runs/dsv4flash-db-first-full-01/dacomp-070/attempt-01/python/P11.stdout)；[错误](../../../runs/dsv4flash-db-first-full-01/dacomp-070/attempt-01/python/P11.stderr)。检出需人工核验的 SQL 可实现操作：groupby(, .query(；不能仅凭理由判为合规。

## 优化机会

已验证候选。筛选限于精确 SQL、相同自包含 CTE、相同单表完整过滤、可分解单表聚合；未覆盖任意 Join 等价和一般谓词蕴含。全部候选都是 offline，未测在线预测。

| 候选 | 类型 | 已有结果 | 覆盖 SQL | 后续次数 | 中间行数 | 验证 | 成本 |
| --- | --- | --- | --- | --- | --- | --- | --- |
| C1 | exact-result reuse | True | ["S13", "S20"] | 1 | unknown | not_verified_cap | Not tested |
| C2 | aggregate MV | False | ["S3", "S5", "S8", "S10", "S13", "S16", "S20"] | 6 | 1128 | verified | Not benchmarked; correctness alone does not establish net speedup. |
| C3 | aggregate MV | False | ["S7", "S9", "S12"] | 2 | 28 | verified | Not benchmarked; correctness alone does not establish net speedup. |
| C4 | aggregate MV | False | ["S6", "S11"] | 1 | 84 | verified | Not benchmarked; correctness alone does not establish net speedup. |


已验证覆盖（含触发查询、候选并集去重）：12/23 条成功数据 SQL。正确性仅针对当前数据库快照；未测性能的候选不能声称已加速。

[完整 build/rewrite 与比较证据](dacomp-070.analysis.json)。

### C2：aggregate MV

Union of grouping keys; decomposable aggregate states; AVG uses SUM and non-NULL COUNT.

原查询 [S3](#s3), [S5](#s5), [S8](#s8), [S10](#s10), [S13](#s13), [S16](#s16), [S20](#s20) → 新增共享状态 C2 → 后续 6 次可复用。该构建点为事后假设，不代表 Agent 当时预知后续。

构建定义：

```sql
SELECT package_name AS __g0, STRFTIME('%Y-%m', date_day) AS __g1, install_trend AS __g2, revenue_trend AS __g3, install_stability AS __g4, performance_momentum AS __g5, risk_growth_profile AS __g6, anomaly_flag AS __g7, daily_performance_vs_baseline AS __g8, MIN(date_day) AS __a0, MAX(date_day) AS __a1, COUNT(*) AS __a2, SUM(quality_score) AS __a3_sum, COUNT(quality_score) AS __a3_n, SUM(crash_rate_per_1k) AS __a4_sum, COUNT(crash_rate_per_1k) AS __a4_n, SUM(anr_rate_per_1k) AS __a5_sum, COUNT(anr_rate_per_1k) AS __a5_n, SUM(revenue_per_active_device) AS __a6_sum, COUNT(revenue_per_active_device) AS __a6_n, SUM(active_devices) AS __a7_sum, COUNT(active_devices) AS __a7_n, SUM(daily_revenue) AS __a8_sum, COUNT(daily_revenue) AS __a8_n, SUM(daily_churn_rate) AS __a9_sum, COUNT(daily_churn_rate) AS __a9_n, SUM(daily_install_uninstall_ratio) AS __a10_sum, COUNT(daily_install_uninstall_ratio) AS __a10_n, MIN(quality_score) AS __a11, MAX(quality_score) AS __a12, MIN(crash_rate_per_1k) AS __a13, MAX(crash_rate_per_1k) AS __a14, MIN(revenue_per_active_device) AS __a15, MAX(revenue_per_active_device) AS __a16, SUM(ma_7d_quality) AS __a17_sum, COUNT(ma_7d_quality) AS __a17_n, SUM(ma_30d_quality) AS __a18_sum, COUNT(ma_30d_quality) AS __a18_n, SUM(wow_install_growth_rate) AS __a19_sum, COUNT(wow_install_growth_rate) AS __a19_n, SUM(wow_revenue_growth_rate) AS __a20_sum, COUNT(wow_revenue_growth_rate) AS __a20_n, SUM(install_volatility_coefficient) AS __a21_sum, COUNT(install_volatility_coefficient) AS __a21_n, SUM(revenue_volatility_coefficient) AS __a22_sum, COUNT(revenue_volatility_coefficient) AS __a22_n FROM "google_play__time_series_trends"  GROUP BY package_name, STRFTIME('%Y-%m', date_day), install_trend, revenue_trend, install_stability, performance_momentum, risk_growth_profile, anomaly_flag, daily_performance_vs_baseline
```

受益查询 S3 的改写示例：

```sql
SELECT MIN(__a0) AS min_date, MAX(__a1) AS max_date, SUM(__a2) AS n_rows FROM temp.reuse_candidate
```

| 原 SQL | 列名一致 | 结果一致 | 比较方法 |
| --- | --- | --- | --- |
| S3 | True | True | exact_multiset |
| S5 | True | True | exact_multiset |
| S8 | True | True | ordered_numeric_tolerance |
| S10 | True | True | exact_multiset |
| S13 | True | True | ordered_numeric_tolerance |
| S16 | True | True | ordered_numeric_tolerance |
| S20 | True | True | ordered_numeric_tolerance |


验证状态：verified；成本结论：Not benchmarked; correctness alone does not establish net speedup.

### C3：aggregate MV

Union of grouping keys; decomposable aggregate states; AVG uses SUM and non-NULL COUNT.

原查询 [S7](#s7), [S9](#s9), [S12](#s12) → 新增共享状态 C3 → 后续 2 次可复用。该构建点为事后假设，不代表 Agent 当时预知后续。

构建定义：

```sql
SELECT STRFTIME('%Y-%m', date_day) AS __g0, region AS __g1, COUNT(*) AS __a0, SUM(store_listing_visitors) AS __a1, SUM(store_listing_acquisitions) AS __a2, SUM(device_installs) AS __a3, SUM(device_uninstalls) AS __a4, SUM(update_events) AS __a5, SUM(active_devices_last_30_days) AS __a6, SUM(device_upgrades) AS __a7, SUM(rolling_total_average_rating) AS __a8_sum, COUNT(rolling_total_average_rating) AS __a8_n FROM "google_play__country_report"  GROUP BY STRFTIME('%Y-%m', date_day), region
```

受益查询 S7 的改写示例：

```sql
SELECT __g0 AS month, __g1 AS "region", SUM(__a0) AS n, SUM(__a1) AS visitors, SUM(__a2) AS acquisitions, ROUND(100.0 * SUM(__a2) / NULLIF(SUM(__a1), 0), 3) AS conv, SUM(__a3) AS installs, SUM(__a4) AS uninstalls, SUM(__a5) AS updates, SUM(__a6) AS actives FROM temp.reuse_candidate GROUP BY __g0, __g1 ORDER BY month, __g1
```

| 原 SQL | 列名一致 | 结果一致 | 比较方法 |
| --- | --- | --- | --- |
| S7 | True | True | ordered_numeric_tolerance |
| S9 | True | True | ordered_numeric_tolerance |
| S12 | True | True | ordered_numeric_tolerance |


验证状态：verified；成本结论：Not benchmarked; correctness alone does not establish net speedup.

### C4：aggregate MV

Union of grouping keys; decomposable aggregate states; AVG uses SUM and non-NULL COUNT.

原查询 [S6](#s6), [S11](#s11) → 新增共享状态 C4 → 后续 1 次可复用。该构建点为事后假设，不代表 Agent 当时预知后续。

构建定义：

```sql
SELECT device AS __g0, STRFTIME('%Y-%m', date_day) AS __g1, COUNT(*) AS __a0, MIN(date_day) AS __a1, MAX(date_day) AS __a2, SUM(update_events) AS __a3, SUM(device_installs) AS __a4, SUM(device_uninstalls) AS __a5, SUM(active_devices_last_30_days) AS __a6, SUM(rolling_total_average_rating) AS __a7_sum, COUNT(rolling_total_average_rating) AS __a7_n FROM "google_play__device_report"  GROUP BY device, STRFTIME('%Y-%m', date_day)
```

受益查询 S6 的改写示例：

```sql
SELECT __g0 AS "device", SUM(__a0) AS n, MIN(__a1) AS min_d, MAX(__a2) AS max_d FROM temp.reuse_candidate GROUP BY __g0 ORDER BY n DESC
```

| 原 SQL | 列名一致 | 结果一致 | 比较方法 |
| --- | --- | --- | --- |
| S6 | True | True | ordered_numeric_tolerance |
| S11 | True | True | ordered_numeric_tolerance |


验证状态：verified；成本结论：Not benchmarked; correctness alone does not establish net speedup.

结果依赖：自动记录 SQL→Python 的接口父调用，以及源码中引用归档文件的消费者；字面值相同不认定因果。模型方向选择需要人工读取消息，尚未做全面因果标注。

[原始报告](../../../runs/dsv4flash-db-first-full-01/dacomp-070/attempt-01/answer.md)；[统一消息](../../../runs/dsv4flash-db-first-full-01/dacomp-070/attempt-01/messages.jsonl)；[原始 OpenCode 事件](../../../runs/dsv4flash-db-first-full-01/dacomp-070/attempt-01/opencode.jsonl)；[SQL 引擎日志](../../../runs/dsv4flash-db-first-full-01/dacomp-070/attempt-01/sql_journal.jsonl)。

[可读报告（本地图片链接规范化）](../answers/dacomp-070.md)。原始回答保留，分析结论未改写。

## S1

类别 `connection_setup`；来源 `connection`；调用 `1f64d4d88ced4ea2bc2fadd6b7ac0b3a`；状态 `success`。

```sql
PRAGMA query_only=ON
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-070/attempt-01/sql/S1.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-070/attempt-01/sql/S1.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-070/attempt-01/results/S1.rows.jsonl)；完整：True；SHA256：`e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`。

## S2

类别 `metadata`；来源 `list_db`；调用 `1f64d4d88ced4ea2bc2fadd6b7ac0b3a`；状态 `success`。

```sql
SELECT name,sql FROM sqlite_master WHERE type='table' ORDER BY name
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-070/attempt-01/sql/S2.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-070/attempt-01/sql/S2.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-070/attempt-01/results/S2.rows.jsonl)；完整：True；SHA256：`ee22f63b69c06aa8a7c9ca52966ff78e4d4f510478d9bf0349ca26aac4b1979b`。

## S3

类别 `data`；来源 `query_db`；调用 `07e54485679a400285ce050b7d3ea4bd`；状态 `success`。

```sql
SELECT MIN(date_day) AS min_date, MAX(date_day) AS max_date, COUNT(*) AS n_rows FROM google_play__time_series_trends
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-070/attempt-01/sql/S3.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-070/attempt-01/sql/S3.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-070/attempt-01/results/S3.rows.jsonl)；完整：True；SHA256：`4aa34c81e6c5c937924f15b7ec67364d3d6fcd08f4e8d56aada247c3060f0202`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "google_play__time_series_trends", "kind": "base", "block": null, "base_tables": ["google_play__time_series_trends"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | MIN(date_day) | [{"table": "google_play__time_series_trends", "column": "date_day"}] | [] | False |
| B1 | MAX(date_day) | [{"table": "google_play__time_series_trends", "column": "date_day"}] | [] | False |
| B1 | COUNT(*) | [] | [] | True |


## S4

类别 `data`；来源 `query_db`；调用 `857e9de4d9964aa88c7bb0db8bacbc56`；状态 `success`。

```sql
SELECT region, COUNT(*) AS n, COUNT(DISTINCT country_short) AS n_countries, MIN(date_day) AS min_d, MAX(date_day) AS max_d FROM google_play__country_report GROUP BY region ORDER BY n DESC
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-070/attempt-01/sql/S4.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-070/attempt-01/sql/S4.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-070/attempt-01/results/S4.rows.jsonl)；完整：True；SHA256：`67dc063764c092582bd5fedb90656fae1bfeb34001c4440b72fe338353eec73f`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "google_play__country_report", "kind": "base", "block": null, "base_tables": ["google_play__country_report"]}] | [] | ["region"] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |
| B1 | COUNT(DISTINCT country_short) | [{"table": "google_play__country_report", "column": "country_short"}] | [] | False |
| B1 | MIN(date_day) | [{"table": "google_play__country_report", "column": "date_day"}] | [] | False |
| B1 | MAX(date_day) | [{"table": "google_play__country_report", "column": "date_day"}] | [] | False |


## S5

类别 `data`；来源 `query_db`；调用 `3cbbd53d4494449493d170aa85a853dc`；状态 `success`。

```sql
SELECT package_name, COUNT(*) AS n, MIN(date_day) AS min_d, MAX(date_day) AS max_d FROM google_play__time_series_trends GROUP BY package_name
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-070/attempt-01/sql/S5.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-070/attempt-01/sql/S5.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-070/attempt-01/results/S5.rows.jsonl)；完整：True；SHA256：`c0271e8082553503a352a34b30359d3a77a1b922a62be091470e43e24ccf5ae0`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "google_play__time_series_trends", "kind": "base", "block": null, "base_tables": ["google_play__time_series_trends"]}] | [] | ["package_name"] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |
| B1 | MIN(date_day) | [{"table": "google_play__time_series_trends", "column": "date_day"}] | [] | False |
| B1 | MAX(date_day) | [{"table": "google_play__time_series_trends", "column": "date_day"}] | [] | False |


## S6

类别 `data`；来源 `query_db`；调用 `4db5cc49e13c40a0a2e5e66eecb6a893`；状态 `success`。

```sql
SELECT device, COUNT(*) AS n, MIN(date_day) AS min_d, MAX(date_day) AS max_d FROM google_play__device_report GROUP BY device ORDER BY n DESC
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-070/attempt-01/sql/S6.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-070/attempt-01/sql/S6.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-070/attempt-01/results/S6.rows.jsonl)；完整：True；SHA256：`22d6e339ced0f8a16ff7d833c20ad246c839314a82604905f6c21b2f4f086715`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "google_play__device_report", "kind": "base", "block": null, "base_tables": ["google_play__device_report"]}] | [] | ["device"] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |
| B1 | MIN(date_day) | [{"table": "google_play__device_report", "column": "date_day"}] | [] | False |
| B1 | MAX(date_day) | [{"table": "google_play__device_report", "column": "date_day"}] | [] | False |


## S7

类别 `data`；来源 `query_db`；调用 `2389a53bd16043eabe827821da705537`；状态 `success`。

```sql
SELECT strftime('%Y-%m', date_day) AS month, region, COUNT(*) AS n,
  SUM(store_listing_visitors) AS visitors, SUM(store_listing_acquisitions) AS acquisitions,
  ROUND(100.0*SUM(store_listing_acquisitions)/NULLIF(SUM(store_listing_visitors),0),3) AS conv,
  SUM(device_installs) AS installs, SUM(device_uninstalls) AS uninstalls,
  SUM(update_events) AS updates, SUM(active_devices_last_30_days) AS actives
FROM google_play__country_report
GROUP BY month, region ORDER BY month, region
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-070/attempt-01/sql/S7.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-070/attempt-01/sql/S7.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-070/attempt-01/results/S7.rows.jsonl)；完整：True；SHA256：`738ee402c2c728d5bac1dd7ff55b352786abdbb68a10ffdd35054109df8d166a`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "google_play__country_report", "kind": "base", "block": null, "base_tables": ["google_play__country_report"]}] | [] | ["STRFTIME('%Y-%m', date_day)", "region"] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |
| B1 | SUM(store_listing_visitors) | [{"table": "google_play__country_report", "column": "store_listing_visitors"}] | [] | False |
| B1 | SUM(store_listing_acquisitions) | [{"table": "google_play__country_report", "column": "store_listing_acquisitions"}] | [] | False |
| B1 | SUM(device_installs) | [{"table": "google_play__country_report", "column": "device_installs"}] | [] | False |
| B1 | SUM(device_uninstalls) | [{"table": "google_play__country_report", "column": "device_uninstalls"}] | [] | False |
| B1 | SUM(update_events) | [{"table": "google_play__country_report", "column": "update_events"}] | [] | False |
| B1 | SUM(active_devices_last_30_days) | [{"table": "google_play__country_report", "column": "active_devices_last_30_days"}] | [] | False |
| B1 | SUM(store_listing_acquisitions) | [{"table": "google_play__country_report", "column": "store_listing_acquisitions"}] | [] | False |
| B1 | SUM(store_listing_visitors) | [{"table": "google_play__country_report", "column": "store_listing_visitors"}] | [] | False |


## S8

类别 `data`；来源 `query_db`；调用 `7e2f32230f73451e837e659777d6547a`；状态 `success`。

```sql
SELECT strftime('%Y-%m', date_day) AS month, package_name,
  AVG(quality_score) AS quality, AVG(crash_rate_per_1k) AS crash, AVG(anr_rate_per_1k) AS anr,
  AVG(revenue_per_active_device) AS rpad, AVG(active_devices) AS active, AVG(daily_revenue) AS rev,
  AVG(daily_churn_rate) AS churn, AVG(daily_install_uninstall_ratio) AS iur
FROM google_play__time_series_trends
GROUP BY month, package_name ORDER BY month, package_name
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-070/attempt-01/sql/S8.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-070/attempt-01/sql/S8.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-070/attempt-01/results/S8.rows.jsonl)；完整：True；SHA256：`6cb085dc65b82104ebb81b1ecb51b3bbda28ceed5f545c632a08e231a957d49d`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "google_play__time_series_trends", "kind": "base", "block": null, "base_tables": ["google_play__time_series_trends"]}] | [] | ["STRFTIME('%Y-%m', date_day)", "package_name"] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | AVG(quality_score) | [{"table": "google_play__time_series_trends", "column": "quality_score"}] | [] | False |
| B1 | AVG(crash_rate_per_1k) | [{"table": "google_play__time_series_trends", "column": "crash_rate_per_1k"}] | [] | False |
| B1 | AVG(anr_rate_per_1k) | [{"table": "google_play__time_series_trends", "column": "anr_rate_per_1k"}] | [] | False |
| B1 | AVG(revenue_per_active_device) | [{"table": "google_play__time_series_trends", "column": "revenue_per_active_device"}] | [] | False |
| B1 | AVG(active_devices) | [{"table": "google_play__time_series_trends", "column": "active_devices"}] | [] | False |
| B1 | AVG(daily_revenue) | [{"table": "google_play__time_series_trends", "column": "daily_revenue"}] | [] | False |
| B1 | AVG(daily_churn_rate) | [{"table": "google_play__time_series_trends", "column": "daily_churn_rate"}] | [] | False |
| B1 | AVG(daily_install_uninstall_ratio) | [{"table": "google_play__time_series_trends", "column": "daily_install_uninstall_ratio"}] | [] | False |


## S9

类别 `data`；来源 `query_db`；调用 `bea7d4465e5e4fc7b2ff433185fe472f`；状态 `success`。

```sql
SELECT strftime('%Y-%m', date_day) AS month, region, ROUND(100.0*SUM(store_listing_acquisitions)/NULLIF(SUM(store_listing_visitors),0),3) AS conv, ROUND(1.0*SUM(store_listing_visitors)/NULLIF(SUM(store_listing_acquisitions),0),1) AS visits_per_acq, SUM(device_upgrades) AS upgrades, SUM(update_events) AS updates FROM google_play__country_report GROUP BY month, region ORDER BY month, region
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-070/attempt-01/sql/S9.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-070/attempt-01/sql/S9.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-070/attempt-01/results/S9.rows.jsonl)；完整：True；SHA256：`5d81beb70bd6c6244999ecf4f4e82454b7208f960882adc7b8f3d7caf2aad827`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "google_play__country_report", "kind": "base", "block": null, "base_tables": ["google_play__country_report"]}] | [] | ["STRFTIME('%Y-%m', date_day)", "region"] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | SUM(device_upgrades) | [{"table": "google_play__country_report", "column": "device_upgrades"}] | [] | False |
| B1 | SUM(update_events) | [{"table": "google_play__country_report", "column": "update_events"}] | [] | False |
| B1 | SUM(store_listing_acquisitions) | [{"table": "google_play__country_report", "column": "store_listing_acquisitions"}] | [] | False |
| B1 | SUM(store_listing_visitors) | [{"table": "google_play__country_report", "column": "store_listing_visitors"}] | [] | False |
| B1 | SUM(store_listing_visitors) | [{"table": "google_play__country_report", "column": "store_listing_visitors"}] | [] | False |
| B1 | SUM(store_listing_acquisitions) | [{"table": "google_play__country_report", "column": "store_listing_acquisitions"}] | [] | False |


## S10

类别 `data`；来源 `query_db`；调用 `16e67d3b99be4eab86b2bcf695cda686`；状态 `success`。

```sql
SELECT package_name, COUNT(*) AS n, ROUND(MIN(quality_score),3) AS min_q, ROUND(MAX(quality_score),3) AS max_q, ROUND(MIN(crash_rate_per_1k),3) AS min_c, ROUND(MAX(crash_rate_per_1k),3) AS max_c, ROUND(MIN(revenue_per_active_device),6) AS min_rpad, ROUND(MAX(revenue_per_active_device),6) AS max_rpad, ROUND(AVG(revenue_per_active_device),6) AS avg_rpad FROM google_play__time_series_trends GROUP BY package_name
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-070/attempt-01/sql/S10.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-070/attempt-01/sql/S10.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-070/attempt-01/results/S10.rows.jsonl)；完整：True；SHA256：`4508bd3d2b8515122ab64b8f770e234e665a48e50d4d95849bad8e935c92e687`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "google_play__time_series_trends", "kind": "base", "block": null, "base_tables": ["google_play__time_series_trends"]}] | [] | ["package_name"] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |
| B1 | MIN(quality_score) | [{"table": "google_play__time_series_trends", "column": "quality_score"}] | [] | False |
| B1 | MAX(quality_score) | [{"table": "google_play__time_series_trends", "column": "quality_score"}] | [] | False |
| B1 | MIN(crash_rate_per_1k) | [{"table": "google_play__time_series_trends", "column": "crash_rate_per_1k"}] | [] | False |
| B1 | MAX(crash_rate_per_1k) | [{"table": "google_play__time_series_trends", "column": "crash_rate_per_1k"}] | [] | False |
| B1 | MIN(revenue_per_active_device) | [{"table": "google_play__time_series_trends", "column": "revenue_per_active_device"}] | [] | False |
| B1 | MAX(revenue_per_active_device) | [{"table": "google_play__time_series_trends", "column": "revenue_per_active_device"}] | [] | False |
| B1 | AVG(revenue_per_active_device) | [{"table": "google_play__time_series_trends", "column": "revenue_per_active_device"}] | [] | False |


## S11

类别 `data`；来源 `query_db`；调用 `bbf8d03626af4b4ea926c75339d599c9`；状态 `success`。

```sql
SELECT strftime('%Y-%m', date_day) AS month, device, SUM(update_events) AS updates, SUM(device_installs) AS installs, SUM(device_uninstalls) AS uninstalls, ROUND(AVG(rolling_total_average_rating),3) AS avg_rating, SUM(active_devices_last_30_days) AS actives FROM google_play__device_report GROUP BY month, device ORDER BY month, device
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-070/attempt-01/sql/S11.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-070/attempt-01/sql/S11.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-070/attempt-01/results/S11.rows.jsonl)；完整：True；SHA256：`2b5aa4c17f708f87ad07e448174e812f7398048e9e17e20a6a84a5b859052177`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "google_play__device_report", "kind": "base", "block": null, "base_tables": ["google_play__device_report"]}] | [] | ["STRFTIME('%Y-%m', date_day)", "device"] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | SUM(update_events) | [{"table": "google_play__device_report", "column": "update_events"}] | [] | False |
| B1 | SUM(device_installs) | [{"table": "google_play__device_report", "column": "device_installs"}] | [] | False |
| B1 | SUM(device_uninstalls) | [{"table": "google_play__device_report", "column": "device_uninstalls"}] | [] | False |
| B1 | SUM(active_devices_last_30_days) | [{"table": "google_play__device_report", "column": "active_devices_last_30_days"}] | [] | False |
| B1 | AVG(rolling_total_average_rating) | [{"table": "google_play__device_report", "column": "rolling_total_average_rating"}] | [] | False |


## S12

类别 `data`；来源 `query_db`；调用 `56fc2fc94d514b1ca8af145d43ffadc8`；状态 `success`。

```sql
SELECT strftime('%Y-%m', date_day) AS month, region, 
  ROUND(100.0*SUM(store_listing_acquisitions)/NULLIF(SUM(store_listing_visitors),0),3) AS conv_rate,
  ROUND(1.0*SUM(store_listing_visitors)/NULLIF(SUM(store_listing_acquisitions),0),2) AS cost_per_acq_visitors,
  ROUND(1.0*SUM(device_installs)/NULLIF(SUM(store_listing_acquisitions),0),3) AS installs_per_acq,
  SUM(update_events) AS updates,
  SUM(active_devices_last_30_days) AS actives,
  ROUND(AVG(rolling_total_average_rating),3) AS avg_rating
FROM google_play__country_report
GROUP BY month, region 
ORDER BY region, month
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-070/attempt-01/sql/S12.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-070/attempt-01/sql/S12.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-070/attempt-01/results/S12.rows.jsonl)；完整：True；SHA256：`84bc2487f3b03a2abffa2e9bf5e01be948d492eb6c066857a4619a0ed68f7a5c`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "google_play__country_report", "kind": "base", "block": null, "base_tables": ["google_play__country_report"]}] | [] | ["STRFTIME('%Y-%m', date_day)", "region"] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | SUM(update_events) | [{"table": "google_play__country_report", "column": "update_events"}] | [] | False |
| B1 | SUM(active_devices_last_30_days) | [{"table": "google_play__country_report", "column": "active_devices_last_30_days"}] | [] | False |
| B1 | AVG(rolling_total_average_rating) | [{"table": "google_play__country_report", "column": "rolling_total_average_rating"}] | [] | False |
| B1 | SUM(store_listing_acquisitions) | [{"table": "google_play__country_report", "column": "store_listing_acquisitions"}] | [] | False |
| B1 | SUM(store_listing_visitors) | [{"table": "google_play__country_report", "column": "store_listing_visitors"}] | [] | False |
| B1 | SUM(store_listing_visitors) | [{"table": "google_play__country_report", "column": "store_listing_visitors"}] | [] | False |
| B1 | SUM(store_listing_acquisitions) | [{"table": "google_play__country_report", "column": "store_listing_acquisitions"}] | [] | False |
| B1 | SUM(device_installs) | [{"table": "google_play__country_report", "column": "device_installs"}] | [] | False |
| B1 | SUM(store_listing_acquisitions) | [{"table": "google_play__country_report", "column": "store_listing_acquisitions"}] | [] | False |


## S13

类别 `data`；来源 `query_db`；调用 `31ad6c2aaa714e46ba690089e2452bfe`；状态 `success`。

```sql
SELECT strftime('%Y-%m', date_day) AS month, package_name, 
  AVG(quality_score) AS quality, AVG(crash_rate_per_1k) AS crash, AVG(anr_rate_per_1k) AS anr,
  AVG(revenue_per_active_device) AS rpad, AVG(active_devices) AS active,
  AVG(ma_7d_quality) AS ma7q, AVG(ma_30d_quality) AS ma30q,
  AVG(wow_install_growth_rate) AS wow_inst, AVG(wow_revenue_growth_rate) AS wow_rev,
  AVG(install_volatility_coefficient) AS inst_vol, AVG(revenue_volatility_coefficient) AS rev_vol
FROM google_play__time_series_trends
GROUP BY month, package_name 
ORDER BY package_name, month
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-070/attempt-01/sql/S13.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-070/attempt-01/sql/S13.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-070/attempt-01/results/S13.rows.jsonl)；完整：True；SHA256：`487195011d3c1f02a48cb3b67df11360768dad5fbcd4aaaa7510185048a9b81d`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "google_play__time_series_trends", "kind": "base", "block": null, "base_tables": ["google_play__time_series_trends"]}] | [] | ["STRFTIME('%Y-%m', date_day)", "package_name"] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | AVG(quality_score) | [{"table": "google_play__time_series_trends", "column": "quality_score"}] | [] | False |
| B1 | AVG(crash_rate_per_1k) | [{"table": "google_play__time_series_trends", "column": "crash_rate_per_1k"}] | [] | False |
| B1 | AVG(anr_rate_per_1k) | [{"table": "google_play__time_series_trends", "column": "anr_rate_per_1k"}] | [] | False |
| B1 | AVG(revenue_per_active_device) | [{"table": "google_play__time_series_trends", "column": "revenue_per_active_device"}] | [] | False |
| B1 | AVG(active_devices) | [{"table": "google_play__time_series_trends", "column": "active_devices"}] | [] | False |
| B1 | AVG(ma_7d_quality) | [{"table": "google_play__time_series_trends", "column": "ma_7d_quality"}] | [] | False |
| B1 | AVG(ma_30d_quality) | [{"table": "google_play__time_series_trends", "column": "ma_30d_quality"}] | [] | False |
| B1 | AVG(wow_install_growth_rate) | [{"table": "google_play__time_series_trends", "column": "wow_install_growth_rate"}] | [] | False |
| B1 | AVG(wow_revenue_growth_rate) | [{"table": "google_play__time_series_trends", "column": "wow_revenue_growth_rate"}] | [] | False |
| B1 | AVG(install_volatility_coefficient) | [{"table": "google_play__time_series_trends", "column": "install_volatility_coefficient"}] | [] | False |
| B1 | AVG(revenue_volatility_coefficient) | [{"table": "google_play__time_series_trends", "column": "revenue_volatility_coefficient"}] | [] | False |


## S14

类别 `data`；来源 `query_db`；调用 `bb9ef909e1084840aacf80df9bee0485`；状态 `success`。

```sql
SELECT cr.region, dr.device, strftime('%Y-%m', cr.date_day) AS month,
  SUM(cr.store_listing_visitors) AS visitors, SUM(cr.store_listing_acquisitions) AS acquisitions,
  SUM(dr.device_installs) AS installs, SUM(dr.device_uninstalls) AS uninstalls,
  SUM(dr.update_events) AS updates, SUM(dr.active_devices_last_30_days) AS actives,
  ROUND(AVG(dr.rolling_total_average_rating),3) AS rating
FROM google_play__country_report cr
JOIN google_play__device_report dr ON cr.date_day = dr.date_day AND cr.package_name = dr.package_name
GROUP BY cr.region, dr.device, month
ORDER BY cr.region, dr.device, month
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-070/attempt-01/sql/S14.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-070/attempt-01/sql/S14.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-070/attempt-01/results/S14.rows.jsonl)；完整：True；SHA256：`2567b372e0bd87473b67e5663799fa83a4d3521d4ab36e5aa2b3ab1413752b82`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "cr", "kind": "base", "block": null, "base_tables": ["google_play__country_report"]}, {"alias": "dr", "kind": "base", "block": null, "base_tables": ["google_play__device_report"]}] | [{"type": "INNER", "right": "google_play__device_report AS dr", "on": "cr.date_day = dr.date_day AND cr.package_name = dr.package_name", "using": []}] | ["cr.region", "dr.device", "STRFTIME('%Y-%m', cr.date_day)"] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | SUM(cr.store_listing_visitors) | [{"table": "google_play__country_report", "column": "store_listing_visitors"}] | [] | False |
| B1 | SUM(cr.store_listing_acquisitions) | [{"table": "google_play__country_report", "column": "store_listing_acquisitions"}] | [] | False |
| B1 | SUM(dr.device_installs) | [{"table": "google_play__device_report", "column": "device_installs"}] | [] | False |
| B1 | SUM(dr.device_uninstalls) | [{"table": "google_play__device_report", "column": "device_uninstalls"}] | [] | False |
| B1 | SUM(dr.update_events) | [{"table": "google_play__device_report", "column": "update_events"}] | [] | False |
| B1 | SUM(dr.active_devices_last_30_days) | [{"table": "google_play__device_report", "column": "active_devices_last_30_days"}] | [] | False |
| B1 | AVG(dr.rolling_total_average_rating) | [{"table": "google_play__device_report", "column": "rolling_total_average_rating"}] | [] | False |


## S15

类别 `data`；来源 `query_db`；调用 `892ad028d0c646f5ba7b420cd8b867b1`；状态 `success`。

```sql
SELECT strftime('%Y-%m', cr.date_day) AS month, cr.region, cr.package_name,
  SUM(cr.store_listing_visitors) AS visitors, SUM(cr.store_listing_acquisitions) AS acquisitions,
  ROUND(100.0*SUM(cr.store_listing_acquisitions)/NULLIF(SUM(cr.store_listing_visitors),0),4) AS conv_rate,
  SUM(cr.device_installs) AS installs, SUM(cr.update_events) AS updates,
  SUM(cr.active_devices_last_30_days) AS actives,
  ROUND(AVG(cr.rolling_total_average_rating),4) AS rating,
  ROUND(AVG(ts.quality_score),4) AS quality, ROUND(AVG(ts.crash_rate_per_1k),4) AS crash,
  ROUND(AVG(ts.revenue_per_active_device),8) AS rpad, ROUND(AVG(ts.daily_churn_rate),5) AS churn,
  SUM(cr.store_listing_acquisitions) AS acq
FROM google_play__country_report cr
JOIN google_play__time_series_trends ts ON cr.date_day = ts.date_day AND cr.package_name = ts.package_name
GROUP BY month, cr.region, cr.package_name
ORDER BY cr.region, cr.package_name, month
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-070/attempt-01/sql/S15.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-070/attempt-01/sql/S15.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-070/attempt-01/results/S15.rows.jsonl)；完整：True；SHA256：`35671fd91ab9d78d020e8a95b6681e3743370364f924694e20184750eaa2ce33`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "cr", "kind": "base", "block": null, "base_tables": ["google_play__country_report"]}, {"alias": "ts", "kind": "base", "block": null, "base_tables": ["google_play__time_series_trends"]}] | [{"type": "INNER", "right": "google_play__time_series_trends AS ts", "on": "cr.date_day = ts.date_day AND cr.package_name = ts.package_name", "using": []}] | ["STRFTIME('%Y-%m', cr.date_day)", "cr.region", "cr.package_name"] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | SUM(cr.store_listing_visitors) | [{"table": "google_play__country_report", "column": "store_listing_visitors"}] | [] | False |
| B1 | SUM(cr.store_listing_acquisitions) | [{"table": "google_play__country_report", "column": "store_listing_acquisitions"}] | [] | False |
| B1 | SUM(cr.device_installs) | [{"table": "google_play__country_report", "column": "device_installs"}] | [] | False |
| B1 | SUM(cr.update_events) | [{"table": "google_play__country_report", "column": "update_events"}] | [] | False |
| B1 | SUM(cr.active_devices_last_30_days) | [{"table": "google_play__country_report", "column": "active_devices_last_30_days"}] | [] | False |
| B1 | SUM(cr.store_listing_acquisitions) | [{"table": "google_play__country_report", "column": "store_listing_acquisitions"}] | [] | False |
| B1 | AVG(cr.rolling_total_average_rating) | [{"table": "google_play__country_report", "column": "rolling_total_average_rating"}] | [] | False |
| B1 | AVG(ts.quality_score) | [{"table": "google_play__time_series_trends", "column": "quality_score"}] | [] | False |
| B1 | AVG(ts.crash_rate_per_1k) | [{"table": "google_play__time_series_trends", "column": "crash_rate_per_1k"}] | [] | False |
| B1 | AVG(ts.revenue_per_active_device) | [{"table": "google_play__time_series_trends", "column": "revenue_per_active_device"}] | [] | False |
| B1 | AVG(ts.daily_churn_rate) | [{"table": "google_play__time_series_trends", "column": "daily_churn_rate"}] | [] | False |
| B1 | SUM(cr.store_listing_acquisitions) | [{"table": "google_play__country_report", "column": "store_listing_acquisitions"}] | [] | False |
| B1 | SUM(cr.store_listing_visitors) | [{"table": "google_play__country_report", "column": "store_listing_visitors"}] | [] | False |


## S16

类别 `data`；来源 `query_db`；调用 `549b7892422f410bb768a9754c802ea2`；状态 `success`。

```sql
SELECT install_trend, revenue_trend, install_stability, performance_momentum, risk_growth_profile, anomaly_flag, daily_performance_vs_baseline, COUNT(*) AS n FROM google_play__time_series_trends GROUP BY install_trend, revenue_trend, install_stability, performance_momentum, risk_growth_profile, anomaly_flag, daily_performance_vs_baseline ORDER BY n DESC
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-070/attempt-01/sql/S16.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-070/attempt-01/sql/S16.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-070/attempt-01/results/S16.rows.jsonl)；完整：True；SHA256：`8c4208d3ed799e8873f20d17c95621ba186e886713a69e890ba7886868bfae98`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "google_play__time_series_trends", "kind": "base", "block": null, "base_tables": ["google_play__time_series_trends"]}] | [] | ["install_trend", "revenue_trend", "install_stability", "performance_momentum", "risk_growth_profile", "anomaly_flag", "daily_performance_vs_baseline"] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |


## S17

类别 `data`；来源 `query_db`；调用 `88bea2d5f3cc41479e83501cd3f91f0a`；状态 `success`。

```sql
SELECT android_os_version, COUNT(*) n, SUM(crashes) crashes, SUM(anrs) anrs, SUM(device_installs) installs, SUM(active_devices_last_30_days) actives FROM google_play__os_version_report GROUP BY android_os_version ORDER BY installs DESC
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-070/attempt-01/sql/S17.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-070/attempt-01/sql/S17.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-070/attempt-01/results/S17.rows.jsonl)；完整：True；SHA256：`8971c280bf9c37e341afaf1ce86b62cb144f5ac28196479347e95b0932f0ac26`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "google_play__os_version_report", "kind": "base", "block": null, "base_tables": ["google_play__os_version_report"]}] | [] | ["android_os_version"] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |
| B1 | SUM(crashes) | [{"table": "google_play__os_version_report", "column": "crashes"}] | [] | False |
| B1 | SUM(anrs) | [{"table": "google_play__os_version_report", "column": "anrs"}] | [] | False |
| B1 | SUM(device_installs) | [{"table": "google_play__os_version_report", "column": "device_installs"}] | [] | False |
| B1 | SUM(active_devices_last_30_days) | [{"table": "google_play__os_version_report", "column": "active_devices_last_30_days"}] | [] | False |


## S18

类别 `data`；来源 `python`；调用 `37c04a5ef4184de49cb0ae8f05875c16`；状态 `success`。

```sql

SELECT cr.region, dr.device, strftime('%Y-%m', cr.date_day) AS month,
  SUM(cr.store_listing_visitors) AS visitors, SUM(cr.store_listing_acquisitions) AS acquisitions,
  SUM(dr.device_installs) AS installs, SUM(dr.device_uninstalls) AS uninstalls,
  SUM(dr.update_events) AS updates, SUM(dr.active_devices_last_30_days) AS actives,
  AVG(dr.rolling_total_average_rating) AS rating
FROM google_play__country_report cr
JOIN google_play__device_report dr ON cr.date_day = dr.date_day AND cr.package_name = dr.package_name
GROUP BY cr.region, dr.device, month
ORDER BY cr.region, dr.device, month

```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-070/attempt-01/sql/S18.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-070/attempt-01/sql/S18.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-070/attempt-01/results/S18.rows.jsonl)；完整：True；SHA256：`add1e35d1defb795bcafc5e0b21c215aa3252df91bc655891c59d39da232b0e6`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "cr", "kind": "base", "block": null, "base_tables": ["google_play__country_report"]}, {"alias": "dr", "kind": "base", "block": null, "base_tables": ["google_play__device_report"]}] | [{"type": "INNER", "right": "google_play__device_report AS dr", "on": "cr.date_day = dr.date_day AND cr.package_name = dr.package_name", "using": []}] | ["cr.region", "dr.device", "STRFTIME('%Y-%m', cr.date_day)"] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | SUM(cr.store_listing_visitors) | [{"table": "google_play__country_report", "column": "store_listing_visitors"}] | [] | False |
| B1 | SUM(cr.store_listing_acquisitions) | [{"table": "google_play__country_report", "column": "store_listing_acquisitions"}] | [] | False |
| B1 | SUM(dr.device_installs) | [{"table": "google_play__device_report", "column": "device_installs"}] | [] | False |
| B1 | SUM(dr.device_uninstalls) | [{"table": "google_play__device_report", "column": "device_uninstalls"}] | [] | False |
| B1 | SUM(dr.update_events) | [{"table": "google_play__device_report", "column": "update_events"}] | [] | False |
| B1 | SUM(dr.active_devices_last_30_days) | [{"table": "google_play__device_report", "column": "active_devices_last_30_days"}] | [] | False |
| B1 | AVG(dr.rolling_total_average_rating) | [{"table": "google_play__device_report", "column": "rolling_total_average_rating"}] | [] | False |


## S19

类别 `data`；来源 `python`；调用 `37c04a5ef4184de49cb0ae8f05875c16`；状态 `success`。

```sql

SELECT strftime('%Y-%m', cr.date_day) AS month, cr.region, cr.package_name,
  SUM(cr.store_listing_visitors) AS visitors, SUM(cr.store_listing_acquisitions) AS acquisitions,
  SUM(cr.device_installs) AS installs, SUM(cr.update_events) AS updates,
  SUM(cr.active_devices_last_30_days) AS actives,
  AVG(cr.rolling_total_average_rating) AS rating,
  AVG(ts.quality_score) AS quality, AVG(ts.crash_rate_per_1k) AS crash,
  AVG(ts.revenue_per_active_device) AS rpad, AVG(ts.daily_churn_rate) AS churn
FROM google_play__country_report cr
JOIN google_play__time_series_trends ts ON cr.date_day = ts.date_day AND cr.package_name = ts.package_name
GROUP BY month, cr.region, cr.package_name
ORDER BY cr.region, cr.package_name, month

```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-070/attempt-01/sql/S19.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-070/attempt-01/sql/S19.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-070/attempt-01/results/S19.rows.jsonl)；完整：True；SHA256：`8279defa9529ac6eecace91d3978d80464e599d93af9b0431a6c3c7ab2d9ff5a`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "cr", "kind": "base", "block": null, "base_tables": ["google_play__country_report"]}, {"alias": "ts", "kind": "base", "block": null, "base_tables": ["google_play__time_series_trends"]}] | [{"type": "INNER", "right": "google_play__time_series_trends AS ts", "on": "cr.date_day = ts.date_day AND cr.package_name = ts.package_name", "using": []}] | ["STRFTIME('%Y-%m', cr.date_day)", "cr.region", "cr.package_name"] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | SUM(cr.store_listing_visitors) | [{"table": "google_play__country_report", "column": "store_listing_visitors"}] | [] | False |
| B1 | SUM(cr.store_listing_acquisitions) | [{"table": "google_play__country_report", "column": "store_listing_acquisitions"}] | [] | False |
| B1 | SUM(cr.device_installs) | [{"table": "google_play__country_report", "column": "device_installs"}] | [] | False |
| B1 | SUM(cr.update_events) | [{"table": "google_play__country_report", "column": "update_events"}] | [] | False |
| B1 | SUM(cr.active_devices_last_30_days) | [{"table": "google_play__country_report", "column": "active_devices_last_30_days"}] | [] | False |
| B1 | AVG(cr.rolling_total_average_rating) | [{"table": "google_play__country_report", "column": "rolling_total_average_rating"}] | [] | False |
| B1 | AVG(ts.quality_score) | [{"table": "google_play__time_series_trends", "column": "quality_score"}] | [] | False |
| B1 | AVG(ts.crash_rate_per_1k) | [{"table": "google_play__time_series_trends", "column": "crash_rate_per_1k"}] | [] | False |
| B1 | AVG(ts.revenue_per_active_device) | [{"table": "google_play__time_series_trends", "column": "revenue_per_active_device"}] | [] | False |
| B1 | AVG(ts.daily_churn_rate) | [{"table": "google_play__time_series_trends", "column": "daily_churn_rate"}] | [] | False |


## S20

类别 `data`；来源 `python`；调用 `37c04a5ef4184de49cb0ae8f05875c16`；状态 `success`。

```sql

SELECT strftime('%Y-%m', date_day) AS month, package_name,
  AVG(quality_score) AS quality, AVG(crash_rate_per_1k) AS crash, AVG(anr_rate_per_1k) AS anr,
  AVG(revenue_per_active_device) AS rpad, AVG(active_devices) AS active,
  AVG(ma_7d_quality) AS ma7q, AVG(ma_30d_quality) AS ma30q,
  AVG(wow_install_growth_rate) AS wow_inst, AVG(wow_revenue_growth_rate) AS wow_rev,
  AVG(install_volatility_coefficient) AS inst_vol, AVG(revenue_volatility_coefficient) AS rev_vol
FROM google_play__time_series_trends
GROUP BY month, package_name
ORDER BY package_name, month

```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-070/attempt-01/sql/S20.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-070/attempt-01/sql/S20.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-070/attempt-01/results/S20.rows.jsonl)；完整：True；SHA256：`487195011d3c1f02a48cb3b67df11360768dad5fbcd4aaaa7510185048a9b81d`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "google_play__time_series_trends", "kind": "base", "block": null, "base_tables": ["google_play__time_series_trends"]}] | [] | ["STRFTIME('%Y-%m', date_day)", "package_name"] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | AVG(quality_score) | [{"table": "google_play__time_series_trends", "column": "quality_score"}] | [] | False |
| B1 | AVG(crash_rate_per_1k) | [{"table": "google_play__time_series_trends", "column": "crash_rate_per_1k"}] | [] | False |
| B1 | AVG(anr_rate_per_1k) | [{"table": "google_play__time_series_trends", "column": "anr_rate_per_1k"}] | [] | False |
| B1 | AVG(revenue_per_active_device) | [{"table": "google_play__time_series_trends", "column": "revenue_per_active_device"}] | [] | False |
| B1 | AVG(active_devices) | [{"table": "google_play__time_series_trends", "column": "active_devices"}] | [] | False |
| B1 | AVG(ma_7d_quality) | [{"table": "google_play__time_series_trends", "column": "ma_7d_quality"}] | [] | False |
| B1 | AVG(ma_30d_quality) | [{"table": "google_play__time_series_trends", "column": "ma_30d_quality"}] | [] | False |
| B1 | AVG(wow_install_growth_rate) | [{"table": "google_play__time_series_trends", "column": "wow_install_growth_rate"}] | [] | False |
| B1 | AVG(wow_revenue_growth_rate) | [{"table": "google_play__time_series_trends", "column": "wow_revenue_growth_rate"}] | [] | False |
| B1 | AVG(install_volatility_coefficient) | [{"table": "google_play__time_series_trends", "column": "install_volatility_coefficient"}] | [] | False |
| B1 | AVG(revenue_volatility_coefficient) | [{"table": "google_play__time_series_trends", "column": "revenue_volatility_coefficient"}] | [] | False |


## S21

类别 `data`；来源 `python`；调用 `1e22158a133149baba456678510d576a`；状态 `success`。

```sql

SELECT date_day, package_name, quality_score, crash_rate_per_1k, anr_rate_per_1k,
       revenue_per_active_device, active_devices, daily_churn_rate,
       daily_install_uninstall_ratio, wow_install_growth_rate, 
       daily_revenue, avg_transaction_value,
       ma_7d_quality, ma_30d_quality, ma_7d_churn,
       install_volatility_coefficient, revenue_volatility_coefficient,
       install_trend, revenue_trend, risk_growth_profile, performance_momentum,
       install_stability
FROM google_play__time_series_trends
ORDER BY package_name, date_day

```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-070/attempt-01/sql/S21.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-070/attempt-01/sql/S21.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-070/attempt-01/results/S21.rows.jsonl)；完整：True；SHA256：`6e3fc068146816205b085ece1035916889840a877f28c17fc431888d02b537bd`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "google_play__time_series_trends", "kind": "base", "block": null, "base_tables": ["google_play__time_series_trends"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |


## S22

类别 `data`；来源 `python`；调用 `fbe9524bd3844449b54c599549152586`；状态 `success`。

```sql

SELECT date_day, country_short, region, package_name,
       update_events, active_devices_last_30_days, 
       rolling_total_average_rating, device_installs, net_device_installs
FROM google_play__country_report
ORDER BY region, package_name, date_day

```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-070/attempt-01/sql/S22.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-070/attempt-01/sql/S22.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-070/attempt-01/results/S22.rows.jsonl)；完整：True；SHA256：`760374f38792a434046e3584d39eef6779249139de3d9633ac4b9f1ac3c19b0f`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "google_play__country_report", "kind": "base", "block": null, "base_tables": ["google_play__country_report"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |


## S23

类别 `data`；来源 `python`；调用 `fbe9524bd3844449b54c599549152586`；状态 `success`。

```sql

SELECT date_day, device, package_name,
       update_events, active_devices_last_30_days,
       rolling_total_average_rating, device_installs, device_uninstalls
FROM google_play__device_report
ORDER BY device, package_name, date_day

```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-070/attempt-01/sql/S23.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-070/attempt-01/sql/S23.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-070/attempt-01/results/S23.rows.jsonl)；完整：True；SHA256：`9d7c3f972dc3798fd82276d5a81e7c3e2589ecde42438a82c3f273ac2ae4738b`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "google_play__device_report", "kind": "base", "block": null, "base_tables": ["google_play__device_report"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |


## S24

类别 `data`；来源 `python`；调用 `50cc2687564a47d6bbbef18eaa404fe1`；状态 `success`。

```sql

SELECT cr.date_day, cr.region, cr.package_name,
       100.0*SUM(cr.store_listing_acquisitions)/NULLIF(SUM(cr.store_listing_visitors),0) AS conv_rate,
       AVG(ts.quality_score) AS quality, AVG(ts.crash_rate_per_1k) AS crash,
       AVG(ts.revenue_per_active_device) AS rpad
FROM google_play__country_report cr
JOIN google_play__time_series_trends ts ON cr.date_day = ts.date_day AND cr.package_name = ts.package_name
GROUP BY cr.date_day, cr.region, cr.package_name
HAVING SUM(cr.store_listing_visitors) > 0
ORDER BY cr.date_day, cr.region, cr.package_name

```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-070/attempt-01/sql/S24.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-070/attempt-01/sql/S24.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-070/attempt-01/results/S24.rows.jsonl)；完整：True；SHA256：`d3260b53aaac7a1510097fc37c1f6a5aa1d30f04918dfb1d6c482162c1d728f6`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "cr", "kind": "base", "block": null, "base_tables": ["google_play__country_report"]}, {"alias": "ts", "kind": "base", "block": null, "base_tables": ["google_play__time_series_trends"]}] | [{"type": "INNER", "right": "google_play__time_series_trends AS ts", "on": "cr.date_day = ts.date_day AND cr.package_name = ts.package_name", "using": []}] | ["cr.date_day", "cr.region", "cr.package_name"] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | AVG(ts.quality_score) | [{"table": "google_play__time_series_trends", "column": "quality_score"}] | [] | False |
| B1 | AVG(ts.crash_rate_per_1k) | [{"table": "google_play__time_series_trends", "column": "crash_rate_per_1k"}] | [] | False |
| B1 | AVG(ts.revenue_per_active_device) | [{"table": "google_play__time_series_trends", "column": "revenue_per_active_device"}] | [] | False |
| B1 | SUM(cr.store_listing_visitors) | [{"table": "google_play__country_report", "column": "store_listing_visitors"}] | [] | False |
| B1 | SUM(cr.store_listing_acquisitions) | [{"table": "google_play__country_report", "column": "store_listing_acquisitions"}] | [] | False |
| B1 | SUM(cr.store_listing_visitors) | [{"table": "google_play__country_report", "column": "store_listing_visitors"}] | [] | False |


## S25

类别 `data`；来源 `python`；调用 `1cf2f6ebe66046c1a906ee523531b88d`；状态 `success`。

```sql

SELECT cr.date_day, cr.region, cr.package_name,
       100.0*SUM(cr.store_listing_acquisitions)/NULLIF(SUM(cr.store_listing_visitors),0) AS conv_rate,
       SUM(cr.store_listing_visitors) AS visitors,
       SUM(cr.store_listing_acquisitions) AS acquisitions,
       AVG(ts.quality_score) AS quality, AVG(ts.crash_rate_per_1k) AS crash,
       AVG(ts.revenue_per_active_device) AS rpad, AVG(ts.active_devices) AS active_devices,
       AVG(ts.daily_churn_rate) AS churn
FROM google_play__country_report cr
JOIN google_play__time_series_trends ts ON cr.date_day = ts.date_day AND cr.package_name = ts.package_name
GROUP BY cr.date_day, cr.region, cr.package_name

```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-070/attempt-01/sql/S25.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-070/attempt-01/sql/S25.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-070/attempt-01/results/S25.rows.jsonl)；完整：True；SHA256：`3053181de80518da50a6a2a29c252c8bf561ebf7eb776893013e7ac8fd77f444`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "cr", "kind": "base", "block": null, "base_tables": ["google_play__country_report"]}, {"alias": "ts", "kind": "base", "block": null, "base_tables": ["google_play__time_series_trends"]}] | [{"type": "INNER", "right": "google_play__time_series_trends AS ts", "on": "cr.date_day = ts.date_day AND cr.package_name = ts.package_name", "using": []}] | ["cr.date_day", "cr.region", "cr.package_name"] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | SUM(cr.store_listing_visitors) | [{"table": "google_play__country_report", "column": "store_listing_visitors"}] | [] | False |
| B1 | SUM(cr.store_listing_acquisitions) | [{"table": "google_play__country_report", "column": "store_listing_acquisitions"}] | [] | False |
| B1 | AVG(ts.quality_score) | [{"table": "google_play__time_series_trends", "column": "quality_score"}] | [] | False |
| B1 | AVG(ts.crash_rate_per_1k) | [{"table": "google_play__time_series_trends", "column": "crash_rate_per_1k"}] | [] | False |
| B1 | AVG(ts.revenue_per_active_device) | [{"table": "google_play__time_series_trends", "column": "revenue_per_active_device"}] | [] | False |
| B1 | AVG(ts.active_devices) | [{"table": "google_play__time_series_trends", "column": "active_devices"}] | [] | False |
| B1 | AVG(ts.daily_churn_rate) | [{"table": "google_play__time_series_trends", "column": "daily_churn_rate"}] | [] | False |
| B1 | SUM(cr.store_listing_acquisitions) | [{"table": "google_play__country_report", "column": "store_listing_acquisitions"}] | [] | False |
| B1 | SUM(cr.store_listing_visitors) | [{"table": "google_play__country_report", "column": "store_listing_visitors"}] | [] | False |

