# dacomp-078

The existing customer value scoring model primarily relies on two dimensions, usage durati…

运行：已提交。官方未评分。全部 SQL 尝试/成功 50/48；数据 SQL 48/46；Python 28 次。

完整原题：

The existing customer value scoring model primarily relies on two dimensions, usage duration and frequency, but its accuracy in identifying high-value customers is only 68%. We need to rebuild a multi-dimensional value assessment system. The new model is expected to increase the identification accuracy for high-value customers to over 85% and be able to predict the value trend of customers over the next 3-6 months.

| 表 | 行数 | 列数 |
| --- | --- | --- |
| pendo__account | 1000 | 22 |
| pendo__feature | 2000 | 32 |
| pendo__visitor | 38544 | 24 |
| pendo__visitor_daily_metrics | 29057 | 7 |
| pendo__visitor_feature | 24982 | 9 |


实际路线（分析者依据 SQL/源码概括，不代表 Agent 自述）：SQL 提取账户与访客行为 → Python 连接、构造价值模型及交叉验证 → 月趋势预测与画像。

数据库大小：17,858,560 字节。

## 数据 SQL

| SQL | 状态 | 基础表 | Join 输入/类型 | GROUP BY | 聚合表达式 | 结果行数 | 数据库 ms |
| --- | --- | --- | --- | --- | --- | --- | --- |
| [S3/Q1](#s3) | success | ["pendo__account"] | 0 / {} | [] | ["COUNT(*)"] | 1 | 0.489 |
| [S4/Q2](#s4) | success | ["pendo__visitor"] | 0 / {} | [] | ["COUNT(*)"] | 1 | 5.12 |
| [S5/Q3](#s5) | success | ["pendo__visitor_daily_metrics"] | 0 / {} | [] | ["COUNT(*)"] | 1 | 0.789 |
| [S6/Q4](#s6) | success | ["pendo__visitor_feature"] | 0 / {} | [] | ["COUNT(*)"] | 1 | 1.3 |
| [S7/Q5](#s7) | success | ["pendo__feature"] | 0 / {} | [] | ["COUNT(*)"] | 1 | 0.699 |
| [S8/Q6](#s8) | success | ["pendo__account"] | 0 / {} | [] | ["MIN(first_event_on)", "MAX(last_event_on)"] | 1 | 0.555 |
| [S9/Q7](#s9) | success | ["pendo__visitor"] | 0 / {} | [] | ["MIN(first_event_on)", "MAX(last_event_on)"] | 1 | 9.591 |
| [S10/Q8](#s10) | success | ["pendo__visitor_daily_metrics"] | 0 / {} | [] | ["MIN(date_day)", "MAX(date_day)"] | 1 | 3.506 |
| [S11/Q9](#s11) | success | ["pendo__account"] | 0 / {} | [] | [] | 5 | 0.382 |
| [S12/Q10](#s12) | success | ["pendo__visitor"] | 0 / {} | [] | [] | 5 | 0.385 |
| [S13/Q11](#s13) | success | ["pendo__account"] | 0 / {} | ["SUBSTRING(last_event_on, 1, 7)"] | ["COUNT(*)"] | 9 | 0.828 |
| [S14/Q12](#s14) | success | ["pendo__account"] | 0 / {} | ["SUBSTRING(first_event_on, 1, 7)"] | ["COUNT(*)"] | 1 | 0.716 |
| [S15/Q13](#s15) | failed | ["pendo__visitor_daily_metrics"] | 0 / {} | [] | ["COUNT(DISTINCT visitor_id)", "COUNT(DISTINCT account_id)"] | unknown | 未取得；调用总时长 0.184 ms |
| [S16/Q14](#s16) | success | ["pendo__visitor_daily_metrics"] | 0 / {} | ["SUBSTRING(date_day, 1, 7)"] | ["COUNT(*)", "COUNT(DISTINCT visitor_id)"] | 9 | 13.408 |
| [S17/Q15](#s17) | success | ["pendo__visitor_daily_metrics"] | 0 / {} | [] | ["COUNT(DISTINCT visitor_id)"] | 1 | 2.911 |
| [S18/Q16](#s18) | success | ["pendo__visitor", "pendo__visitor_daily_metrics"] | 2 / {'INNER': 1} | [] | ["COUNT(DISTINCT v.visitor_id)"] | 1 | 34.986 |
| [S19/Q17](#s19) | success | ["pendo__account"] | 0 / {} | [] | [] | 10 | 0.442 |
| [S20/Q18](#s20) | success | ["pendo__account"] | 0 / {} | [] | ["MIN(count_active_days)", "AVG(count_active_days)", "MAX(count_active_days)", "MIN(sum_minutes)", "AVG(sum_minutes)", "MAX(sum_minutes)", "MIN(sum_events)", "AVG(sum_events)", "MAX(sum_events)", "MIN(avg_nps_rating)", "AVG(avg_nps_rating)", "MAX(avg_nps_rating)"] | 1 | 1.021 |
| [S21/Q19](#s21) | success | ["pendo__visitor", "pendo__visitor_daily_metrics"] | 2 / {'INNER': 1} | [] | ["COUNT(DISTINCT account_id)"] | 1 | 34.166 |
| [S22/Q20](#s22) | success | ["pendo__account", "pendo__visitor", "pendo__visitor_daily_metrics"] | 3 / {'LEFT': 2} | ["a.account_id"] | ["COUNT(DISTINCT v.visitor_id)", "SUM(CASE WHEN NOT dm.visitor_id IS NULL THEN 1 ELSE 0 END)"] | 10 | 45.154 |
| [S23/Q21](#s23) | success | ["pendo__visitor_feature"] | 0 / {} | [] | ["COUNT(DISTINCT visitor_id)"] | 1 | 14.672 |
| [S24/Q22](#s24) | success | ["pendo__visitor_feature"] | 0 / {} | [] | ["MIN(first_click_at)", "MAX(last_click_at)"] | 1 | 4.087 |
| [S25/Q23](#s25) | success | ["pendo__feature"] | 0 / {} | [] | ["COUNT(DISTINCT feature_id)", "COUNT(DISTINCT product_area_name)"] | 1 | 1.99 |
| [S26/Q24](#s26) | success | ["pendo__account", "pendo__visitor"] | 0 / {} | [] | ["COUNT(*)", "SUM(count_associated_visitors)"] | 1 | 4.495 |
| [S27/Q25](#s27) | success | ["pendo__account", "pendo__visitor"] | 2 / {'LEFT': 1} | ["a.account_id"] | ["COUNT(DISTINCT v.visitor_id)", "COUNT(DISTINCT v.visitor_id)"] | 0 | 36.269 |
| [S28/Q26](#s28) | success | ["pendo__account", "pendo__visitor"] | 2 / {'INNER': 1} | ["a.account_id"] | ["COUNT(DISTINCT v.visitor_id)", "COUNT(DISTINCT v.visitor_id)"] | 10 | 36.684 |
| [S29/Q27](#s29) | success | ["pendo__visitor", "pendo__visitor_feature"] | 2 / {'INNER': 1} | [] | ["COUNT(DISTINCT account_id)"] | 1 | 43.495 |
| [S30/Q28](#s30) | success | ["pendo__visitor", "pendo__visitor_feature"] | 2 / {'LEFT': 1} | [] | ["COUNT(DISTINCT vf.visitor_id)"] | 1 | 44.253 |
| [S31/Q29](#s31) | success | ["pendo__visitor", "pendo__visitor_feature"] | 2 / {'INNER': 1} | [] | ["COUNT(DISTINCT vf.visitor_id)"] | 1 | 29.935 |
| [S32/Q30](#s32) | success | ["pendo__visitor_feature"] | 0 / {} | [] | ["COUNT(DISTINCT vf.feature_id)", "COUNT(DISTINCT vf.visitor_id)"] | 1 | 24.471 |
| [S33/Q31](#s33) | success | ["pendo__feature"] | 0 / {} | [] | ["COUNT(DISTINCT feature_id)"] | 1 | 1.809 |
| [S34/Q32](#s34) | success | ["pendo__feature"] | 0 / {} | [] | [] | 8 | 0.342 |
| [S35/Q33](#s35) | success | ["pendo__account"] | 0 / {} | ["CASE WHEN last_event_on >= '2024-07-01' THEN 'Active_Jul_Oct' WHEN last_event_on >= '2024-04-01' THEN 'Active_Apr_Jun' ELSE 'Active_Jan_Mar' END"] | ["COUNT(*)", "AVG(sum_minutes)", "AVG(sum_events)", "AVG(count_active_days)", "AVG(count_active_months)", "AVG(avg_nps_rating)", "AVG(count_associated_visitors)"] | 3 | 1.288 |
| [S36/Q34](#s36) | success | ["pendo__account"] | 0 / {} | ["SUBSTRING(last_event_on, 1, 7)"] | ["COUNT(*)", "AVG(sum_minutes)", "AVG(sum_events)", "AVG(count_active_days)", "AVG(count_active_months)"] | 9 | 1.069 |
| [S37/Q35](#s37) | success | ["pendo__account"] | 0 / {} | [] | ["MIN(count_associated_visitors)", "AVG(count_associated_visitors)", "MAX(count_associated_visitors)", "MIN(count_active_visitors)", "AVG(count_active_visitors)", "MAX(count_active_visitors)", "MIN(count_page_viewing_visitors)", "AVG(count_page_viewing_visitors)", "MAX(count_page_viewing_visitors)", "MIN(count_feature_clicking_visitors)", "AVG(count_feature_clicking_visitors)", "MAX(count_feature_clicking_visitors)"] | 1 | 0.888 |
| [S38/Q36](#s38) | success | ["pendo__account"] | 0 / {} | [] | ["MIN(average_daily_minutes)", "AVG(average_daily_minutes)", "MAX(average_daily_minutes)", "MIN(average_daily_events)", "AVG(average_daily_events)", "MAX(average_daily_events)", "COUNT(CASE WHEN NOT avg_nps_rating IS NULL THEN 1 END)", "COUNT(CASE WHEN avg_nps_rating IS NULL THEN 1 END)"] | 1 | 0.791 |
| [S39/Q37](#s39) | failed | ["pendo__visitor"] | 0 / {} | ["v.account_id"] | ["COUNT(DISTINCT v.last_browser_name)", "COUNT(DISTINCT v.last_operating_system)", "AVG(v.sum_minutes)", "AVG(v.sum_events)", "STDDEV(v.sum_minutes)", "STDDEV(v.sum_events)", "AVG(v.average_daily_minutes)", "AVG(v.average_daily_events)", "AVG(v.count_active_days)"] | unknown | 未取得；调用总时长 0.174 ms |
| [S40/Q38](#s40) | success | ["pendo__account", "pendo__visitor", "pendo__visitor_daily_metrics"] | 2 / {'INNER': 1} | [] | [] | 11 | 34.511 |
| [S41/Q39](#s41) | success | ["pendo__visitor", "pendo__visitor_daily_metrics"] | 2 / {'INNER': 1} | ["v.account_id"] | ["COUNT(*)", "COUNT(DISTINCT dm.visitor_id)", "MIN(dm.date_day)", "MAX(dm.date_day)"] | 11 | 47.26 |
| [S42/Q40](#s42) | success | ["pendo__account"] | 0 / {} | [] | ["COUNT(*)", "SUM(CASE WHEN min_nps_rating IS NULL THEN 1 ELSE 0 END)", "SUM(CASE WHEN max_nps_rating IS NULL THEN 1 ELSE 0 END)", "SUM(CASE WHEN avg_nps_rating IS NULL THEN 1 ELSE 0 END)", "SUM(CASE WHEN count_active_visitors IS NULL THEN 1 ELSE 0 END)", "SUM(CASE WHEN count_page_viewing_visitors IS NULL THEN 1 ELSE 0 END)", "SUM(CASE WHEN count_feature_clicking_visitors IS NULL THEN 1 ELSE 0 END)"] | 1 | 0.796 |
| [S43/Q41](#s43) | success | ["pendo__account"] | 0 / {} | ["ROUND((count_active_days - 1.0) / 10) * 10"] | ["COUNT(*)", "AVG(sum_minutes)", "AVG(sum_events)", "AVG(avg_nps_rating)", "AVG(count_associated_visitors)"] | 22 | 1.171 |
| [S44/Q42](#s44) | success | ["pendo__account"] | 0 / {} | [] | [] | 1000 | 5.38 |
| [S45/Q43](#s45) | success | ["pendo__account"] | 0 / {} | [] | [] | 1000 | 5.197 |
| [S46/Q44](#s46) | success | ["pendo__account"] | 0 / {} | [] | [] | 1000 | 4.678 |
| [S47/Q45](#s47) | success | ["pendo__visitor"] | 0 / {} | ["v.account_id"] | ["COUNT(DISTINCT v.last_browser_name)", "COUNT(DISTINCT v.last_operating_system)", "AVG(v.sum_minutes)", "AVG(v.sum_events)", "AVG(v.average_daily_minutes)", "AVG(v.average_daily_events)", "AVG(v.count_active_days)", "AVG(v.count_active_months)", "SUM(v.sum_minutes)", "SUM(v.sum_events)"] | 1000 | 50.159 |
| [S48/Q46](#s48) | success | ["pendo__visitor"] | 0 / {} | ["v.account_id"] | ["COUNT(DISTINCT v.last_browser_name)", "COUNT(DISTINCT v.last_operating_system)", "AVG(v.sum_minutes)", "AVG(v.sum_events)", "AVG(v.average_daily_minutes)", "AVG(v.average_daily_events)", "AVG(v.count_active_days)", "AVG(v.count_active_months)", "SUM(v.sum_minutes)", "SUM(v.sum_events)"] | 1000 | 47.959 |
| [S49/Q47](#s49) | success | ["pendo__visitor", "pendo__visitor_daily_metrics"] | 2 / {'INNER': 1} | ["v.account_id", "SUBSTRING(dm.date_day, 1, 7)"] | ["SUM(dm.sum_minutes)", "SUM(dm.sum_events)", "COUNT(DISTINCT dm.visitor_id)", "COUNT(DISTINCT dm.date_day)"] | 50 | 79.536 |
| [S50/Q48](#s50) | success | ["pendo__visitor", "pendo__visitor_daily_metrics"] | 2 / {'INNER': 1} | ["v.account_id", "SUBSTRING(dm.date_day, 1, 7)"] | ["SUM(dm.sum_minutes)", "SUM(dm.sum_events)", "COUNT(DISTINCT dm.visitor_id)", "COUNT(DISTINCT dm.date_day)"] | 50 | 64.523 |


## 元数据和设置

| SQL | 类别 | 状态 | 内容 |
| --- | --- | --- | --- |
| S1 | connection_setup | success | PRAGMA query_only=ON |
| S2 | metadata | success | SELECT name,sql FROM sqlite_master WHERE type='table' ORDER BY name |


## Python 与执行位置

人工源码审查：**database_first_violation**。逻辑回归、交叉验证和预测误差属于建模计算，算法内均值及混淆矩阵不当作迁出明细聚合。Python 仍连接账户与访客结果，按高价值类别计算画像均值、按留存十分位求比例，属于 SQL 可支持的关系和分组操作；据此记录偏离。 [证据](../reviews/dacomp-078.json)。

P1：Model training, cross-validation, and accuracy comparison (logistic regression) are not reasonably supported by SQLite. I load only the 1000-row account feature set from the archived S44 query and compute composite scores, split data, and evaluate both baseline and multi-dimensional models.

[源码](../../../runs/dsv4flash-db-first-full-01/dacomp-078/attempt-01/python/P1.py)；[输出](../../../runs/dsv4flash-db-first-full-01/dacomp-078/attempt-01/python/P1.stdout)；[错误](../../../runs/dsv4flash-db-first-full-01/dacomp-078/attempt-01/python/P1.stderr)。自动源码筛查未检出预设迁出信号；这不是全面语义合规证明。

P2：Locating the archived result files to load the account feature set for model building.

[源码](../../../runs/dsv4flash-db-first-full-01/dacomp-078/attempt-01/python/P2.py)；[输出](../../../runs/dsv4flash-db-first-full-01/dacomp-078/attempt-01/python/P2.stdout)；[错误](../../../runs/dsv4flash-db-first-full-01/dacomp-078/attempt-01/python/P2.stderr)。自动源码筛查未检出预设迁出信号；这不是全面语义合规证明。

P3：Locating result archives at the absolute /results path.

[源码](../../../runs/dsv4flash-db-first-full-01/dacomp-078/attempt-01/python/P3.py)；[输出](../../../runs/dsv4flash-db-first-full-01/dacomp-078/attempt-01/python/P3.stdout)；[错误](../../../runs/dsv4flash-db-first-full-01/dacomp-078/attempt-01/python/P3.stderr)。自动源码筛查未检出预设迁出信号；这不是全面语义合规证明。

P4：Load the 1000-row account feature set into Python for model building and evaluation.

[源码](../../../runs/dsv4flash-db-first-full-01/dacomp-078/attempt-01/python/P4.py)；[输出](../../../runs/dsv4flash-db-first-full-01/dacomp-078/attempt-01/python/P4.stdout)；[错误](../../../runs/dsv4flash-db-first-full-01/dacomp-078/attempt-01/python/P4.stderr)。自动源码筛查未检出预设迁出信号；这不是全面语义合规证明。

P5：Inspect the raw JSONL format of the result archive to parse it correctly.

[源码](../../../runs/dsv4flash-db-first-full-01/dacomp-078/attempt-01/python/P5.py)；[输出](../../../runs/dsv4flash-db-first-full-01/dacomp-078/attempt-01/python/P5.stdout)；[错误](../../../runs/dsv4flash-db-first-full-01/dacomp-078/attempt-01/python/P5.stderr)。自动源码筛查未检出预设迁出信号；这不是全面语义合规证明。

P6：Load account feature set via the logged db interface and db.frame so columns are parsed correctly.

[源码](../../../runs/dsv4flash-db-first-full-01/dacomp-078/attempt-01/python/P6.py)；[输出](../../../runs/dsv4flash-db-first-full-01/dacomp-078/attempt-01/python/P6.stdout)；[错误](../../../runs/dsv4flash-db-first-full-01/dacomp-078/attempt-01/python/P6.stderr)。检出需人工核验的 SQL 可实现操作：.query(；不能仅凭理由判为合规。

P7：Compute the retention-based outcome label (active after mid-year 2024) and prepare the account feature DataFrame for model evaluation.

[源码](../../../runs/dsv4flash-db-first-full-01/dacomp-078/attempt-01/python/P7.py)；[输出](../../../runs/dsv4flash-db-first-full-01/dacomp-078/attempt-01/python/P7.stdout)；[错误](../../../runs/dsv4flash-db-first-full-01/dacomp-078/attempt-01/python/P7.stderr)。检出需人工核验的 SQL 可实现操作：.query(；不能仅凭理由判为合规。

P8：Augment account features with visitor-level diversity and engagement metrics, which add multi-dimensional value signals beyond the account-level aggregates.

[源码](../../../runs/dsv4flash-db-first-full-01/dacomp-078/attempt-01/python/P8.py)；[输出](../../../runs/dsv4flash-db-first-full-01/dacomp-078/attempt-01/python/P8.stdout)；[错误](../../../runs/dsv4flash-db-first-full-01/dacomp-078/attempt-01/python/P8.stderr)。检出需人工核验的 SQL 可实现操作：.merge(, .query(；不能仅凭理由判为合规。

P9：Merge visitor-level diversity and engagement features into the account feature table for the multi-dimensional model.

[源码](../../../runs/dsv4flash-db-first-full-01/dacomp-078/attempt-01/python/P9.py)；[输出](../../../runs/dsv4flash-db-first-full-01/dacomp-078/attempt-01/python/P9.stdout)；[错误](../../../runs/dsv4flash-db-first-full-01/dacomp-078/attempt-01/python/P9.stderr)。检出需人工核验的 SQL 可实现操作：.merge(, .query(；不能仅凭理由判为合规。

P10：Train and evaluate both the baseline 2D model and the multi-dimensional model using 5-fold cross-validation, comparing accuracy, AUC, and feature importance.

[源码](../../../runs/dsv4flash-db-first-full-01/dacomp-078/attempt-01/python/P10.py)；[输出](../../../runs/dsv4flash-db-first-full-01/dacomp-078/attempt-01/python/P10.stdout)；[错误](../../../runs/dsv4flash-db-first-full-01/dacomp-078/attempt-01/python/P10.stderr)。检出需人工核验的 SQL 可实现操作：sort_values(；不能仅凭理由判为合规。

P11：Check which ML packages are available in the environment.

[源码](../../../runs/dsv4flash-db-first-full-01/dacomp-078/attempt-01/python/P11.py)；[输出](../../../runs/dsv4flash-db-first-full-01/dacomp-078/attempt-01/python/P11.stdout)；[错误](../../../runs/dsv4flash-db-first-full-01/dacomp-078/attempt-01/python/P11.stderr)。自动源码筛查未检出预设迁出信号；这不是全面语义合规证明。

P12：Implement manual logistic regression with 5-fold stratified cross-validation in numpy (no sklearn available) to compare baseline 2D vs multi-dimensional model accuracy.

[源码](../../../runs/dsv4flash-db-first-full-01/dacomp-078/attempt-01/python/P12.py)；[输出](../../../runs/dsv4flash-db-first-full-01/dacomp-078/attempt-01/python/P12.stdout)；[错误](../../../runs/dsv4flash-db-first-full-01/dacomp-078/attempt-01/python/P12.stderr)。自动源码筛查未检出预设迁出信号；这不是全面语义合规证明。

P13：Construct a multi-dimensional composite value score as the high-value ground truth and evaluate the existing 2D duration+frequency model against it to reproduce the ~68% accuracy baseline.

[源码](../../../runs/dsv4flash-db-first-full-01/dacomp-078/attempt-01/python/P13.py)；[输出](../../../runs/dsv4flash-db-first-full-01/dacomp-078/attempt-01/python/P13.stdout)；[错误](../../../runs/dsv4flash-db-first-full-01/dacomp-078/attempt-01/python/P13.stderr)。自动源码筛查未检出预设迁出信号；这不是全面语义合规证明。

P14：Explore different ground truth definitions and thresholds to find the setup that reproduces the reported ~68% baseline accuracy for the 2D model.

[源码](../../../runs/dsv4flash-db-first-full-01/dacomp-078/attempt-01/python/P14.py)；[输出](../../../runs/dsv4flash-db-first-full-01/dacomp-078/attempt-01/python/P14.stdout)；[错误](../../../runs/dsv4flash-db-first-full-01/dacomp-078/attempt-01/python/P14.stderr)。自动源码筛查未检出预设迁出信号；这不是全面语义合规证明。

P15：Train logistic regression models comparing 2D (duration+frequency) and multi-dimensional approaches on a non-engagement ground truth to evaluate accuracy improvements.

[源码](../../../runs/dsv4flash-db-first-full-01/dacomp-078/attempt-01/python/P15.py)；[输出](../../../runs/dsv4flash-db-first-full-01/dacomp-078/attempt-01/python/P15.stdout)；[错误](../../../runs/dsv4flash-db-first-full-01/dacomp-078/attempt-01/python/P15.stderr)。自动源码筛查未检出预设迁出信号；这不是全面语义合规证明。

P16：Evaluate the multi-dimensional composite ground truth with both 2D and multi-dim logistic regression models to confirm accuracy improvement over the 85% target.

[源码](../../../runs/dsv4flash-db-first-full-01/dacomp-078/attempt-01/python/P16.py)；[输出](../../../runs/dsv4flash-db-first-full-01/dacomp-078/attempt-01/python/P16.stdout)；[错误](../../../runs/dsv4flash-db-first-full-01/dacomp-078/attempt-01/python/P16.stderr)。自动源码筛查未检出预设迁出信号；这不是全面语义合规证明。

P17：Load and inspect the monthly account-level trend data from daily metrics to understand the temporal patterns for trend prediction.

[源码](../../../runs/dsv4flash-db-first-full-01/dacomp-078/attempt-01/python/P17.py)；[输出](../../../runs/dsv4flash-db-first-full-01/dacomp-078/attempt-01/python/P17.stdout)；[错误](../../../runs/dsv4flash-db-first-full-01/dacomp-078/attempt-01/python/P17.stderr)。检出需人工核验的 SQL 可实现操作：sort_values(；不能仅凭理由判为合规。

P18：Load monthly trend data via db.frame and inspect trends for key accounts to build the trend prediction component.

[源码](../../../runs/dsv4flash-db-first-full-01/dacomp-078/attempt-01/python/P18.py)；[输出](../../../runs/dsv4flash-db-first-full-01/dacomp-078/attempt-01/python/P18.stdout)；[错误](../../../runs/dsv4flash-db-first-full-01/dacomp-078/attempt-01/python/P18.stderr)。检出需人工核验的 SQL 可实现操作：.query(, sort_values(；不能仅凭理由判为合规。

P19：Build and evaluate a simple linear trend model on monthly value series: train on first 3 months, validate direction prediction on next 3-6 months.

[源码](../../../runs/dsv4flash-db-first-full-01/dacomp-078/attempt-01/python/P19.py)；[输出](../../../runs/dsv4flash-db-first-full-01/dacomp-078/attempt-01/python/P19.stdout)；[错误](../../../runs/dsv4flash-db-first-full-01/dacomp-078/attempt-01/python/P19.stderr)。检出需人工核验的 SQL 可实现操作：groupby(, sort_values(；不能仅凭理由判为合规。

P20：Test a momentum-based rule for predicting 3-month value trend from early monthly data, quantifying the correlation between recent momentum and future value change.

[源码](../../../runs/dsv4flash-db-first-full-01/dacomp-078/attempt-01/python/P20.py)；[输出](../../../runs/dsv4flash-db-first-full-01/dacomp-078/attempt-01/python/P20.stdout)；[错误](../../../runs/dsv4flash-db-first-full-01/dacomp-078/attempt-01/python/P20.stderr)。检出需人工核验的 SQL 可实现操作：groupby(, sort_values(；不能仅凭理由判为合规。

P21：Compute feature importance and high-value vs non-high-value profile comparisons for the multi-dimensional value model.

[源码](../../../runs/dsv4flash-db-first-full-01/dacomp-078/attempt-01/python/P21.py)；[输出](../../../runs/dsv4flash-db-first-full-01/dacomp-078/attempt-01/python/P21.stdout)；[错误](../../../runs/dsv4flash-db-first-full-01/dacomp-078/attempt-01/python/P21.stderr)。检出需人工核验的 SQL 可实现操作：groupby(, sort_values(；不能仅凭理由判为合规。

P22：Quantify how the multi-dimensional value score predicts the 3-6 month retention outcome (trend outlook) using correlation, AUC, decile analysis, and CV accuracy.

[源码](../../../runs/dsv4flash-db-first-full-01/dacomp-078/attempt-01/python/P22.py)；[输出](../../../runs/dsv4flash-db-first-full-01/dacomp-078/attempt-01/python/P22.stdout)；[错误](../../../runs/dsv4flash-db-first-full-01/dacomp-078/attempt-01/python/P22.stderr)。检出需人工核验的 SQL 可实现操作：groupby(；不能仅凭理由判为合规。

P23：Create visualization of monthly account value trajectories to illustrate trend patterns over time.

[源码](../../../runs/dsv4flash-db-first-full-01/dacomp-078/attempt-01/python/P23.py)；[输出](../../../runs/dsv4flash-db-first-full-01/dacomp-078/attempt-01/python/P23.stdout)；[错误](../../../runs/dsv4flash-db-first-full-01/dacomp-078/attempt-01/python/P23.stderr)。检出需人工核验的 SQL 可实现操作：groupby(, sort_values(；不能仅凭理由判为合规。

P24：Create the model comparison bar chart (accuracy, precision, recall, F1) for the 2D baseline vs multi-dimensional model.

[源码](../../../runs/dsv4flash-db-first-full-01/dacomp-078/attempt-01/python/P24.py)；[输出](../../../runs/dsv4flash-db-first-full-01/dacomp-078/attempt-01/python/P24.stdout)；[错误](../../../runs/dsv4flash-db-first-full-01/dacomp-078/attempt-01/python/P24.stderr)。自动源码筛查未检出预设迁出信号；这不是全面语义合规证明。

P25：Create feature importance and retention-by-value-decile visualizations for the report.

[源码](../../../runs/dsv4flash-db-first-full-01/dacomp-078/attempt-01/python/P25.py)；[输出](../../../runs/dsv4flash-db-first-full-01/dacomp-078/attempt-01/python/P25.stdout)；[错误](../../../runs/dsv4flash-db-first-full-01/dacomp-078/attempt-01/python/P25.stderr)。检出需人工核验的 SQL 可实现操作：groupby(, sort_values(；不能仅凭理由判为合规。

P26：Search for the ground truth definition and 2D model specification that matches the ~68% accuracy baseline reported in the task.

[源码](../../../runs/dsv4flash-db-first-full-01/dacomp-078/attempt-01/python/P26.py)；[输出](../../../runs/dsv4flash-db-first-full-01/dacomp-078/attempt-01/python/P26.stdout)；[错误](../../../runs/dsv4flash-db-first-full-01/dacomp-078/attempt-01/python/P26.stderr)。自动源码筛查未检出预设迁出信号；这不是全面语义合规证明。

P27：Compute final clean metrics for both models and verify the 85% target is met.

[源码](../../../runs/dsv4flash-db-first-full-01/dacomp-078/attempt-01/python/P27.py)；[输出](../../../runs/dsv4flash-db-first-full-01/dacomp-078/attempt-01/python/P27.stdout)；[错误](../../../runs/dsv4flash-db-first-full-01/dacomp-078/attempt-01/python/P27.stderr)。自动源码筛查未检出预设迁出信号；这不是全面语义合规证明。

P28：Verify all report figures exist in the workspace.

[源码](../../../runs/dsv4flash-db-first-full-01/dacomp-078/attempt-01/python/P28.py)；[输出](../../../runs/dsv4flash-db-first-full-01/dacomp-078/attempt-01/python/P28.stdout)；[错误](../../../runs/dsv4flash-db-first-full-01/dacomp-078/attempt-01/python/P28.stderr)。自动源码筛查未检出预设迁出信号；这不是全面语义合规证明。

## 优化机会

已验证候选。筛选限于精确 SQL、相同自包含 CTE、相同单表完整过滤、可分解单表聚合；未覆盖任意 Join 等价和一般谓词蕴含。全部候选都是 offline，未测在线预测。

| 候选 | 类型 | 已有结果 | 覆盖 SQL | 后续次数 | 中间行数 | 验证 | 成本 |
| --- | --- | --- | --- | --- | --- | --- | --- |
| C1 | exact-result reuse | True | ["S47", "S48"] | 1 | 1000 | verified | Not benchmarked; correctness alone does not establish net speedup. |
| C2 | aggregate MV | False | ["S3", "S8", "S13", "S14", "S20", "S35", "S36", "S37", "S38", "S42", "S43"] | 10 | 101 | rejected_result_mismatch | Not benchmarked; correctness alone does not establish net speedup. |
| C3 | aggregate MV | False | ["S4", "S9"] | 1 | 1 | verified | Not benchmarked; correctness alone does not establish net speedup. |
| C4 | aggregate MV | False | ["S5", "S10"] | 1 | unknown | not_verified_cap | Not tested |
| C5 | aggregate MV | False | ["S6", "S24"] | 1 | unknown | not_verified_cap | Not tested |


已验证覆盖（含触发查询、候选并集去重）：4/46 条成功数据 SQL。正确性仅针对当前数据库快照；未测性能的候选不能声称已加速。

[完整 build/rewrite 与比较证据](dacomp-078.analysis.json)。

### C1：exact-result reuse

Identical normalized SQL and parameters; archive equality checked.

原查询 [S47](#s47), [S48](#s48) → 保留前序结果 S47 → 后续 1 次可复用。该构建点为事后假设，不代表 Agent 当时预知后续。

| 原 SQL | 列名一致 | 结果一致 | 比较方法 |
| --- | --- | --- | --- |
| S48 | True | True | ordered_numeric_tolerance |


验证状态：verified；成本结论：Not benchmarked; correctness alone does not establish net speedup.

### C3：aggregate MV

Union of grouping keys; decomposable aggregate states; AVG uses SUM and non-NULL COUNT.

原查询 [S4](#s4), [S9](#s9) → 新增共享状态 C3 → 后续 1 次可复用。该构建点为事后假设，不代表 Agent 当时预知后续。

构建定义：

```sql
SELECT COUNT(*) AS __a0, MIN(first_event_on) AS __a1, MAX(last_event_on) AS __a2 FROM "pendo__visitor" 
```

受益查询 S4 的改写示例：

```sql
SELECT SUM(__a0) AS cnt FROM temp.reuse_candidate
```

| 原 SQL | 列名一致 | 结果一致 | 比较方法 |
| --- | --- | --- | --- |
| S4 | True | True | exact_multiset |
| S9 | True | True | exact_multiset |


验证状态：verified；成本结论：Not benchmarked; correctness alone does not establish net speedup.

### C2：aggregate MV

Union of grouping keys; decomposable aggregate states; AVG uses SUM and non-NULL COUNT.

原查询 [S3](#s3), [S8](#s8), [S13](#s13), [S14](#s14), [S20](#s20), [S35](#s35), [S36](#s36), [S37](#s37), [S38](#s38), [S42](#s42), [S43](#s43) → 新增共享状态 C2 → 后续 10 次可复用。该构建点为事后假设，不代表 Agent 当时预知后续。

构建定义：

```sql
SELECT SUBSTRING(last_event_on, 1, 7) AS __g0, SUBSTRING(first_event_on, 1, 7) AS __g1, CASE WHEN last_event_on >= '2024-07-01' THEN 'Active_Jul_Oct' WHEN last_event_on >= '2024-04-01' THEN 'Active_Apr_Jun' ELSE 'Active_Jan_Mar' END AS __g2, ROUND((count_active_days - 1.0) / 10) * 10 AS __g3, COUNT(*) AS __a0, MIN(first_event_on) AS __a1, MAX(last_event_on) AS __a2, MIN(count_active_days) AS __a3, SUM(count_active_days) AS __a4_sum, COUNT(count_active_days) AS __a4_n, MAX(count_active_days) AS __a5, MIN(sum_minutes) AS __a6, SUM(sum_minutes) AS __a7_sum, COUNT(sum_minutes) AS __a7_n, MAX(sum_minutes) AS __a8, MIN(sum_events) AS __a9, SUM(sum_events) AS __a10_sum, COUNT(sum_events) AS __a10_n, MAX(sum_events) AS __a11, MIN(avg_nps_rating) AS __a12, SUM(avg_nps_rating) AS __a13_sum, COUNT(avg_nps_rating) AS __a13_n, MAX(avg_nps_rating) AS __a14, SUM(count_active_months) AS __a15_sum, COUNT(count_active_months) AS __a15_n, SUM(count_associated_visitors) AS __a16_sum, COUNT(count_associated_visitors) AS __a16_n, MIN(count_associated_visitors) AS __a17, MAX(count_associated_visitors) AS __a18, MIN(count_active_visitors) AS __a19, SUM(count_active_visitors) AS __a20_sum, COUNT(count_active_visitors) AS __a20_n, MAX(count_active_visitors) AS __a21, MIN(count_page_viewing_visitors) AS __a22, SUM(count_page_viewing_visitors) AS __a23_sum, COUNT(count_page_viewing_visitors) AS __a23_n, MAX(count_page_viewing_visitors) AS __a24, MIN(count_feature_clicking_visitors) AS __a25, SUM(count_feature_clicking_visitors) AS __a26_sum, COUNT(count_feature_clicking_visitors) AS __a26_n, MAX(count_feature_clicking_visitors) AS __a27, MIN(average_daily_minutes) AS __a28, SUM(average_daily_minutes) AS __a29_sum, COUNT(average_daily_minutes) AS __a29_n, MAX(average_daily_minutes) AS __a30, MIN(average_daily_events) AS __a31, SUM(average_daily_events) AS __a32_sum, COUNT(average_daily_events) AS __a32_n, MAX(average_daily_events) AS __a33, COUNT(CASE WHEN NOT avg_nps_rating IS NULL THEN 1 END) AS __a34, COUNT(CASE WHEN avg_nps_rating IS NULL THEN 1 END) AS __a35, SUM(CASE WHEN min_nps_rating IS NULL THEN 1 ELSE 0 END) AS __a36, SUM(CASE WHEN max_nps_rating IS NULL THEN 1 ELSE 0 END) AS __a37, SUM(CASE WHEN avg_nps_rating IS NULL THEN 1 ELSE 0 END) AS __a38, SUM(CASE WHEN count_active_visitors IS NULL THEN 1 ELSE 0 END) AS __a39, SUM(CASE WHEN count_page_viewing_visitors IS NULL THEN 1 ELSE 0 END) AS __a40, SUM(CASE WHEN count_feature_clicking_visitors IS NULL THEN 1 ELSE 0 END) AS __a41 FROM "pendo__account"  GROUP BY SUBSTRING(last_event_on, 1, 7), SUBSTRING(first_event_on, 1, 7), CASE WHEN last_event_on >= '2024-07-01' THEN 'Active_Jul_Oct' WHEN last_event_on >= '2024-04-01' THEN 'Active_Apr_Jun' ELSE 'Active_Jan_Mar' END, ROUND((count_active_days - 1.0) / 10) * 10
```

受益查询 S3 的改写示例：

```sql
SELECT SUM(__a0) AS cnt FROM temp.reuse_candidate
```

| 原 SQL | 列名一致 | 结果一致 | 比较方法 |
| --- | --- | --- | --- |
| S3 | True | True | exact_multiset |
| S8 | True | True | exact_multiset |
| S13 | True | True | ordered_numeric_tolerance |
| S14 | True | True | ordered_numeric_tolerance |
| S20 | True | False | exact_multiset |
| S35 | True | True | ordered_numeric_tolerance |
| S36 | True | True | ordered_numeric_tolerance |
| S37 | True | True | exact_multiset |
| S38 | True | False | exact_multiset |
| S42 | True | True | exact_multiset |
| S43 | True | True | ordered_numeric_tolerance |


验证状态：rejected_result_mismatch；成本结论：Not benchmarked; correctness alone does not establish net speedup.

结果依赖：自动记录 SQL→Python 的接口父调用，以及源码中引用归档文件的消费者；字面值相同不认定因果。模型方向选择需要人工读取消息，尚未做全面因果标注。

[原始报告](../../../runs/dsv4flash-db-first-full-01/dacomp-078/attempt-01/answer.md)；[统一消息](../../../runs/dsv4flash-db-first-full-01/dacomp-078/attempt-01/messages.jsonl)；[原始 OpenCode 事件](../../../runs/dsv4flash-db-first-full-01/dacomp-078/attempt-01/opencode.jsonl)；[SQL 引擎日志](../../../runs/dsv4flash-db-first-full-01/dacomp-078/attempt-01/sql_journal.jsonl)。

[可读报告（本地图片链接规范化）](../answers/dacomp-078.md)。原始回答保留，分析结论未改写。

## S1

类别 `connection_setup`；来源 `connection`；调用 `9d7c92bc1e94448fa0fc0ac52daefb71`；状态 `success`。

```sql
PRAGMA query_only=ON
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-078/attempt-01/sql/S1.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-078/attempt-01/sql/S1.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-078/attempt-01/results/S1.rows.jsonl)；完整：True；SHA256：`e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`。

## S2

类别 `metadata`；来源 `list_db`；调用 `9d7c92bc1e94448fa0fc0ac52daefb71`；状态 `success`。

```sql
SELECT name,sql FROM sqlite_master WHERE type='table' ORDER BY name
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-078/attempt-01/sql/S2.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-078/attempt-01/sql/S2.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-078/attempt-01/results/S2.rows.jsonl)；完整：True；SHA256：`773d52923e938712554cedd13adb64f02d4ca718ef3379fb0da129958b9401dd`。

## S3

类别 `data`；来源 `query_db`；调用 `cb7b0328f9dd4d79a8b05a03d812820f`；状态 `success`。

```sql
SELECT COUNT(*) AS cnt FROM pendo__account
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-078/attempt-01/sql/S3.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-078/attempt-01/sql/S3.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-078/attempt-01/results/S3.rows.jsonl)；完整：True；SHA256：`e3ed33dc26a723b8481ca677e38dc4a6e8700aeec312afdd02c9dd92374161a2`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "pendo__account", "kind": "base", "block": null, "base_tables": ["pendo__account"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |


## S4

类别 `data`；来源 `query_db`；调用 `a9f445367e8a4852899d9f3bf05a7e56`；状态 `success`。

```sql
SELECT COUNT(*) AS cnt FROM pendo__visitor
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-078/attempt-01/sql/S4.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-078/attempt-01/sql/S4.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-078/attempt-01/results/S4.rows.jsonl)；完整：True；SHA256：`a65083e19eebf4a205b458d7a427b11e632492076ca3de1f7bd65f7854be2958`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "pendo__visitor", "kind": "base", "block": null, "base_tables": ["pendo__visitor"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |


## S5

类别 `data`；来源 `query_db`；调用 `fa67b2c86c4e4ed3973b01e2bcf5e8d1`；状态 `success`。

```sql
SELECT COUNT(*) AS cnt FROM pendo__visitor_daily_metrics
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-078/attempt-01/sql/S5.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-078/attempt-01/sql/S5.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-078/attempt-01/results/S5.rows.jsonl)；完整：True；SHA256：`3463208713815b88b3f2a8d2b5580d01d7b66a088c01452cd8fcfe993b815d3f`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "pendo__visitor_daily_metrics", "kind": "base", "block": null, "base_tables": ["pendo__visitor_daily_metrics"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |


## S6

类别 `data`；来源 `query_db`；调用 `ed09f6fc89b740f1a0fd96d48ff4d4dd`；状态 `success`。

```sql
SELECT COUNT(*) AS cnt FROM pendo__visitor_feature
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-078/attempt-01/sql/S6.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-078/attempt-01/sql/S6.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-078/attempt-01/results/S6.rows.jsonl)；完整：True；SHA256：`b542c2a84557627acdf62b6a8e875d59a61f7b3572b91897582fbcd0699df087`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "pendo__visitor_feature", "kind": "base", "block": null, "base_tables": ["pendo__visitor_feature"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |


## S7

类别 `data`；来源 `query_db`；调用 `9d942c461a7e4347b1c9e5bc0d40fc1a`；状态 `success`。

```sql
SELECT COUNT(*) AS cnt FROM pendo__feature
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-078/attempt-01/sql/S7.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-078/attempt-01/sql/S7.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-078/attempt-01/results/S7.rows.jsonl)；完整：True；SHA256：`4b7ebd95b494120f7bc16bef6e23e2f94400ec47439aefa675a0212e533ee170`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "pendo__feature", "kind": "base", "block": null, "base_tables": ["pendo__feature"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |


## S8

类别 `data`；来源 `query_db`；调用 `f59d81e12ba640599ce7ec65ea52ab2a`；状态 `success`。

```sql
SELECT MIN(first_event_on) AS min_date, MAX(last_event_on) AS max_date FROM pendo__account
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-078/attempt-01/sql/S8.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-078/attempt-01/sql/S8.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-078/attempt-01/results/S8.rows.jsonl)；完整：True；SHA256：`4d29c475e87915f00dd86adb0d408a6f04ce195faf481b1fe9489432c33932d8`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "pendo__account", "kind": "base", "block": null, "base_tables": ["pendo__account"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | MIN(first_event_on) | [{"table": "pendo__account", "column": "first_event_on"}] | [] | False |
| B1 | MAX(last_event_on) | [{"table": "pendo__account", "column": "last_event_on"}] | [] | False |


## S9

类别 `data`；来源 `query_db`；调用 `fc1d65e7b438497ab05edbe12a36285a`；状态 `success`。

```sql
SELECT MIN(first_event_on) AS min_date, MAX(last_event_on) AS max_date FROM pendo__visitor
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-078/attempt-01/sql/S9.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-078/attempt-01/sql/S9.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-078/attempt-01/results/S9.rows.jsonl)；完整：True；SHA256：`4d29c475e87915f00dd86adb0d408a6f04ce195faf481b1fe9489432c33932d8`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "pendo__visitor", "kind": "base", "block": null, "base_tables": ["pendo__visitor"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | MIN(first_event_on) | [{"table": "pendo__visitor", "column": "first_event_on"}] | [] | False |
| B1 | MAX(last_event_on) | [{"table": "pendo__visitor", "column": "last_event_on"}] | [] | False |


## S10

类别 `data`；来源 `query_db`；调用 `f99c783a312546f79758e6e9bcc30658`；状态 `success`。

```sql
SELECT MIN(date_day) AS min_date, MAX(date_day) AS max_date FROM pendo__visitor_daily_metrics
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-078/attempt-01/sql/S10.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-078/attempt-01/sql/S10.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-078/attempt-01/results/S10.rows.jsonl)；完整：True；SHA256：`237cca16a89ffbc06e5f335b3d1e236c876108b777eae460858fd6fd51a7079d`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "pendo__visitor_daily_metrics", "kind": "base", "block": null, "base_tables": ["pendo__visitor_daily_metrics"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | MIN(date_day) | [{"table": "pendo__visitor_daily_metrics", "column": "date_day"}] | [] | False |
| B1 | MAX(date_day) | [{"table": "pendo__visitor_daily_metrics", "column": "date_day"}] | [] | False |


## S11

类别 `data`；来源 `query_db`；调用 `c6ce0d8f5bdd4e5ca485ad9f5c0a878b`；状态 `success`。

```sql
SELECT * FROM pendo__account LIMIT 5
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-078/attempt-01/sql/S11.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-078/attempt-01/sql/S11.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-078/attempt-01/results/S11.rows.jsonl)；完整：True；SHA256：`dd4514ebff34f782233948c73142e8789a314fd46fb5652991b4aecd3a880157`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "pendo__account", "kind": "base", "block": null, "base_tables": ["pendo__account"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |


## S12

类别 `data`；来源 `query_db`；调用 `80ea2497140b4584a6c0ce83efc1df31`；状态 `success`。

```sql
SELECT * FROM pendo__visitor LIMIT 5
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-078/attempt-01/sql/S12.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-078/attempt-01/sql/S12.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-078/attempt-01/results/S12.rows.jsonl)；完整：True；SHA256：`91836c1951fcd06fbcbae7abeb364b05c13ef41f0fb785d3a483270e7b22a1f1`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "pendo__visitor", "kind": "base", "block": null, "base_tables": ["pendo__visitor"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |


## S13

类别 `data`；来源 `query_db`；调用 `851adb25324947c5939ca940b44b2ca5`；状态 `success`。

```sql
SELECT substr(last_event_on,1,7) AS month, COUNT(*) AS accounts FROM pendo__account GROUP BY month ORDER BY month
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-078/attempt-01/sql/S13.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-078/attempt-01/sql/S13.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-078/attempt-01/results/S13.rows.jsonl)；完整：True；SHA256：`23c33e8a4258813e2ca4685c9635e89c6131fa85ac4034e82d38e94096ca7774`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "pendo__account", "kind": "base", "block": null, "base_tables": ["pendo__account"]}] | [] | ["SUBSTRING(last_event_on, 1, 7)"] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |


## S14

类别 `data`；来源 `query_db`；调用 `34d071b9086c4a74b4055d892309cf47`；状态 `success`。

```sql
SELECT substr(first_event_on,1,7) AS month, COUNT(*) AS accounts FROM pendo__account GROUP BY month ORDER BY month
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-078/attempt-01/sql/S14.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-078/attempt-01/sql/S14.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-078/attempt-01/results/S14.rows.jsonl)；完整：True；SHA256：`ad82d47953c074fe02fcf2d6f189a58b067228908e7074b227e0e1b8a1bef6fa`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "pendo__account", "kind": "base", "block": null, "base_tables": ["pendo__account"]}] | [] | ["SUBSTRING(first_event_on, 1, 7)"] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |


## S15

类别 `data`；来源 `query_db`；调用 `7d9a4c729dd64760ba069c326cf418a3`；状态 `failed`。

```sql
SELECT COUNT(DISTINCT visitor_id) AS distinct_visitors, COUNT(DISTINCT account_id) AS distinct_accounts FROM pendo__visitor_daily_metrics
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-078/attempt-01/sql/S15.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-078/attempt-01/sql/S15.parameters.json)。

错误：`OperationalError('no such column: account_id')`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "pendo__visitor_daily_metrics", "kind": "base", "block": null, "base_tables": ["pendo__visitor_daily_metrics"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(DISTINCT visitor_id) | [{"table": "pendo__visitor_daily_metrics", "column": "visitor_id"}] | [] | False |
| B1 | COUNT(DISTINCT account_id) | [{"unknown": "account_id"}] | [] | False |


未解析列血缘：[{"block": "B1", "column": "account_id", "reason": "ambiguous_or_missing_source"}, {"block": "B1", "column": "account_id", "reason": "ambiguous_or_missing_source"}]

## S16

类别 `data`；来源 `query_db`；调用 `151581f22c1c408c871127abbdc298b6`；状态 `success`。

```sql
SELECT substr(date_day,1,7) AS month, COUNT(*) AS rows, COUNT(DISTINCT visitor_id) AS visitors FROM pendo__visitor_daily_metrics GROUP BY month ORDER BY month
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-078/attempt-01/sql/S16.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-078/attempt-01/sql/S16.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-078/attempt-01/results/S16.rows.jsonl)；完整：True；SHA256：`bba7f3d30b6a803e5876f5cbc327aeb4a7077640217b3bac552b3541908016f6`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "pendo__visitor_daily_metrics", "kind": "base", "block": null, "base_tables": ["pendo__visitor_daily_metrics"]}] | [] | ["SUBSTRING(date_day, 1, 7)"] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |
| B1 | COUNT(DISTINCT visitor_id) | [{"table": "pendo__visitor_daily_metrics", "column": "visitor_id"}] | [] | False |


## S17

类别 `data`；来源 `query_db`；调用 `0f38d500d1c04399801b74d3653f68c4`；状态 `success`。

```sql
SELECT COUNT(DISTINCT visitor_id) AS distinct_visitors FROM pendo__visitor_daily_metrics
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-078/attempt-01/sql/S17.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-078/attempt-01/sql/S17.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-078/attempt-01/results/S17.rows.jsonl)；完整：True；SHA256：`b95cc485231360cd221bafab8a2a259fde825f811a6e189af03033e24268f136`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "pendo__visitor_daily_metrics", "kind": "base", "block": null, "base_tables": ["pendo__visitor_daily_metrics"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(DISTINCT visitor_id) | [{"table": "pendo__visitor_daily_metrics", "column": "visitor_id"}] | [] | False |


## S18

类别 `data`；来源 `query_db`；调用 `521e42118413493e86f67abc6f22da7d`；状态 `success`。

```sql
SELECT COUNT(DISTINCT v.visitor_id) AS visitors_with_metrics
FROM pendo__visitor v
JOIN pendo__visitor_daily_metrics dm ON v.visitor_id = dm.visitor_id
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-078/attempt-01/sql/S18.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-078/attempt-01/sql/S18.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-078/attempt-01/results/S18.rows.jsonl)；完整：True；SHA256：`b95cc485231360cd221bafab8a2a259fde825f811a6e189af03033e24268f136`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "v", "kind": "base", "block": null, "base_tables": ["pendo__visitor"]}, {"alias": "dm", "kind": "base", "block": null, "base_tables": ["pendo__visitor_daily_metrics"]}] | [{"type": "INNER", "right": "pendo__visitor_daily_metrics AS dm", "on": "v.visitor_id = dm.visitor_id", "using": []}] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(DISTINCT v.visitor_id) | [{"table": "pendo__visitor", "column": "visitor_id"}] | [] | False |


## S19

类别 `data`；来源 `query_db`；调用 `ba27833a13f94a00b51036b1b51ae985`；状态 `success`。

```sql
SELECT a.account_id, a.count_associated_visitors,
       a.count_active_days, a.count_active_months,
       a.sum_minutes, a.sum_events,
       a.average_daily_minutes, a.average_daily_events,
       a.avg_nps_rating,
       a.count_page_viewing_visitors, a.count_feature_clicking_visitors,
       a.last_event_on
FROM pendo__account a
LIMIT 10
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-078/attempt-01/sql/S19.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-078/attempt-01/sql/S19.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-078/attempt-01/results/S19.rows.jsonl)；完整：True；SHA256：`f15937669c00d338ad866c45e068c9125364405ccb4febccc04f3057a3f50df1`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "a", "kind": "base", "block": null, "base_tables": ["pendo__account"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |


## S20

类别 `data`；来源 `query_db`；调用 `56ce332cebe844428be52311ff13d216`；状态 `success`。

```sql
-- Check the distribution of key metrics
SELECT
  MIN(count_active_days) AS min_days, 
  AVG(count_active_days) AS avg_days, 
  MAX(count_active_days) AS max_days,
  MIN(sum_minutes) AS min_min, 
  AVG(sum_minutes) AS avg_min, 
  MAX(sum_minutes) AS max_min,
  MIN(sum_events) AS min_evt, 
  AVG(sum_events) AS avg_evt, 
  MAX(sum_events) AS max_evt,
  MIN(avg_nps_rating) AS min_nps, 
  AVG(avg_nps_rating) AS avg_nps, 
  MAX(avg_nps_rating) AS max_nps
FROM pendo__account
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-078/attempt-01/sql/S20.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-078/attempt-01/sql/S20.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-078/attempt-01/results/S20.rows.jsonl)；完整：True；SHA256：`1c0eb482629f19f75a433856f875663c1f4609435f38bfc0c0e706ffedef8817`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "pendo__account", "kind": "base", "block": null, "base_tables": ["pendo__account"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | MIN(count_active_days) | [{"table": "pendo__account", "column": "count_active_days"}] | [] | False |
| B1 | AVG(count_active_days) | [{"table": "pendo__account", "column": "count_active_days"}] | [] | False |
| B1 | MAX(count_active_days) | [{"table": "pendo__account", "column": "count_active_days"}] | [] | False |
| B1 | MIN(sum_minutes) | [{"table": "pendo__account", "column": "sum_minutes"}] | [] | False |
| B1 | AVG(sum_minutes) | [{"table": "pendo__account", "column": "sum_minutes"}] | [] | False |
| B1 | MAX(sum_minutes) | [{"table": "pendo__account", "column": "sum_minutes"}] | [] | False |
| B1 | MIN(sum_events) | [{"table": "pendo__account", "column": "sum_events"}] | [] | False |
| B1 | AVG(sum_events) | [{"table": "pendo__account", "column": "sum_events"}] | [] | False |
| B1 | MAX(sum_events) | [{"table": "pendo__account", "column": "sum_events"}] | [] | False |
| B1 | MIN(avg_nps_rating) | [{"table": "pendo__account", "column": "avg_nps_rating"}] | [] | False |
| B1 | AVG(avg_nps_rating) | [{"table": "pendo__account", "column": "avg_nps_rating"}] | [] | False |
| B1 | MAX(avg_nps_rating) | [{"table": "pendo__account", "column": "avg_nps_rating"}] | [] | False |


## S21

类别 `data`；来源 `query_db`；调用 `40b00d9d18bf43f0a4822e0bc8c42448`；状态 `success`。

```sql
SELECT COUNT(DISTINCT account_id) AS accts_with_metrics
FROM pendo__visitor v
JOIN pendo__visitor_daily_metrics dm ON v.visitor_id = dm.visitor_id
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-078/attempt-01/sql/S21.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-078/attempt-01/sql/S21.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-078/attempt-01/results/S21.rows.jsonl)；完整：True；SHA256：`66c03021c935d5575384b1505bf582d78516cc55be41a4d3026e9ebbc9c3fef2`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "v", "kind": "base", "block": null, "base_tables": ["pendo__visitor"]}, {"alias": "dm", "kind": "base", "block": null, "base_tables": ["pendo__visitor_daily_metrics"]}] | [{"type": "INNER", "right": "pendo__visitor_daily_metrics AS dm", "on": "v.visitor_id = dm.visitor_id", "using": []}] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(DISTINCT account_id) | [{"table": "pendo__visitor", "column": "account_id"}] | [] | False |


## S22

类别 `data`；来源 `query_db`；调用 `e9c843fb105849f3be71e191a8bcf02f`；状态 `success`。

```sql
SELECT a.account_id,
  COUNT(DISTINCT v.visitor_id) AS visitors_in_account,
  SUM(CASE WHEN dm.visitor_id IS NOT NULL THEN 1 ELSE 0 END) AS visitors_with_metrics
FROM pendo__account a
LEFT JOIN pendo__visitor v ON a.account_id = v.account_id
LEFT JOIN (SELECT DISTINCT visitor_id FROM pendo__visitor_daily_metrics) dm ON v.visitor_id = dm.visitor_id
GROUP BY a.account_id
LIMIT 10
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-078/attempt-01/sql/S22.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-078/attempt-01/sql/S22.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-078/attempt-01/results/S22.rows.jsonl)；完整：True；SHA256：`3e305b05ab0deaba78eb81e9abf408ad5a54559723fbd9a71823a49b2e9ba811`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "pendo__visitor_daily_metrics", "kind": "base", "block": null, "base_tables": ["pendo__visitor_daily_metrics"]}] | [] | [] |
| B2 | [{"alias": "a", "kind": "base", "block": null, "base_tables": ["pendo__account"]}, {"alias": "v", "kind": "base", "block": null, "base_tables": ["pendo__visitor"]}, {"alias": "dm", "kind": "derived", "block": "B1", "base_tables": ["pendo__visitor_daily_metrics"]}] | [{"type": "LEFT", "right": "pendo__visitor AS v", "on": "a.account_id = v.account_id", "using": []}, {"type": "LEFT", "right": "(SELECT DISTINCT visitor_id FROM pendo__visitor_daily_metrics) AS dm", "on": "v.visitor_id = dm.visitor_id", "using": []}] | ["a.account_id"] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B2 | COUNT(DISTINCT v.visitor_id) | [{"table": "pendo__visitor", "column": "visitor_id"}] | [] | False |
| B2 | SUM(CASE WHEN NOT dm.visitor_id IS NULL THEN 1 ELSE 0 END) | [] | [{"table": "pendo__visitor_daily_metrics", "column": "visitor_id"}] | False |


## S23

类别 `data`；来源 `query_db`；调用 `ac7bcd024d3b498a849d30b6c99d3ac3`；状态 `success`。

```sql
SELECT COUNT(DISTINCT visitor_id) AS vf_visitors FROM pendo__visitor_feature
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-078/attempt-01/sql/S23.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-078/attempt-01/sql/S23.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-078/attempt-01/results/S23.rows.jsonl)；完整：True；SHA256：`5c624bc48e7531fa05fed66c36f87ca3c2e8b2f90931f21c652302a6a2fa30e7`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "pendo__visitor_feature", "kind": "base", "block": null, "base_tables": ["pendo__visitor_feature"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(DISTINCT visitor_id) | [{"table": "pendo__visitor_feature", "column": "visitor_id"}] | [] | False |


## S24

类别 `data`；来源 `query_db`；调用 `b010a948c3d84fcf8dffc9eaa8b44c44`；状态 `success`。

```sql
SELECT MIN(first_click_at) AS min_fc, MAX(last_click_at) AS max_fc FROM pendo__visitor_feature
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-078/attempt-01/sql/S24.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-078/attempt-01/sql/S24.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-078/attempt-01/results/S24.rows.jsonl)；完整：True；SHA256：`4f086afa89d58b8e4cc272faffe59a1fb7ef9eb4f996f07ae0472bf6cf88f981`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "pendo__visitor_feature", "kind": "base", "block": null, "base_tables": ["pendo__visitor_feature"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | MIN(first_click_at) | [{"table": "pendo__visitor_feature", "column": "first_click_at"}] | [] | False |
| B1 | MAX(last_click_at) | [{"table": "pendo__visitor_feature", "column": "last_click_at"}] | [] | False |


## S25

类别 `data`；来源 `query_db`；调用 `5243d2fc4179432db627f1ae18dd28c3`；状态 `success`。

```sql
SELECT COUNT(DISTINCT feature_id) AS features, COUNT(DISTINCT product_area_name) AS areas FROM pendo__feature
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-078/attempt-01/sql/S25.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-078/attempt-01/sql/S25.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-078/attempt-01/results/S25.rows.jsonl)；完整：True；SHA256：`2daca090abd98f77b19a9249197e7fb8b69fd757b9480157653e8ea605cb07fa`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "pendo__feature", "kind": "base", "block": null, "base_tables": ["pendo__feature"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(DISTINCT feature_id) | [{"table": "pendo__feature", "column": "feature_id"}] | [] | False |
| B1 | COUNT(DISTINCT product_area_name) | [{"table": "pendo__feature", "column": "product_area_name"}] | [] | False |


## S26

类别 `data`；来源 `query_db`；调用 `66e24a55a7f44e038737dbd14c9e2518`；状态 `success`。

```sql
SELECT SUM(count_associated_visitors) AS sum_associated, (SELECT COUNT(*) FROM pendo__visitor) AS total_visitors FROM pendo__account
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-078/attempt-01/sql/S26.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-078/attempt-01/sql/S26.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-078/attempt-01/results/S26.rows.jsonl)；完整：True；SHA256：`7fe0fe79cb8e0274530d70aee575b0c42fe8ef7991d7e5568e1a55ecae1f9124`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "pendo__visitor", "kind": "base", "block": null, "base_tables": ["pendo__visitor"]}] | [] | [] |
| B2 | [{"alias": "pendo__account", "kind": "base", "block": null, "base_tables": ["pendo__account"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |
| B2 | SUM(count_associated_visitors) | [{"table": "pendo__account", "column": "count_associated_visitors"}] | [] | False |


## S27

类别 `data`；来源 `query_db`；调用 `3125265d6cb34b27a6efe38e78616bd1`；状态 `success`。

```sql
SELECT a.account_id, COUNT(DISTINCT v.visitor_id) AS actual_visitors
FROM pendo__account a LEFT JOIN pendo__visitor v ON a.account_id = v.account_id
GROUP BY a.account_id
HAVING COUNT(DISTINCT v.visitor_id) < a.count_associated_visitors
LIMIT 5
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-078/attempt-01/sql/S27.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-078/attempt-01/sql/S27.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-078/attempt-01/results/S27.rows.jsonl)；完整：True；SHA256：`e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "a", "kind": "base", "block": null, "base_tables": ["pendo__account"]}, {"alias": "v", "kind": "base", "block": null, "base_tables": ["pendo__visitor"]}] | [{"type": "LEFT", "right": "pendo__visitor AS v", "on": "a.account_id = v.account_id", "using": []}] | ["a.account_id"] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(DISTINCT v.visitor_id) | [{"table": "pendo__visitor", "column": "visitor_id"}] | [] | False |
| B1 | COUNT(DISTINCT v.visitor_id) | [{"table": "pendo__visitor", "column": "visitor_id"}] | [] | False |


## S28

类别 `data`；来源 `query_db`；调用 `3de3d1080e3a46439250c95aabaac574`；状态 `success`。

```sql
SELECT a.account_id, a.count_associated_visitors, COUNT(DISTINCT v.visitor_id) AS actual_visitors
FROM pendo__account a JOIN pendo__visitor v ON a.account_id = v.account_id
GROUP BY a.account_id
ORDER BY a.count_associated_visitors - COUNT(DISTINCT v.visitor_id) DESC
LIMIT 10
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-078/attempt-01/sql/S28.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-078/attempt-01/sql/S28.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-078/attempt-01/results/S28.rows.jsonl)；完整：True；SHA256：`8a8cb546d5da32f97bbe61e4f0481a9eea5ef56c85b6898acdb7b9bee364deef`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "a", "kind": "base", "block": null, "base_tables": ["pendo__account"]}, {"alias": "v", "kind": "base", "block": null, "base_tables": ["pendo__visitor"]}] | [{"type": "INNER", "right": "pendo__visitor AS v", "on": "a.account_id = v.account_id", "using": []}] | ["a.account_id"] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(DISTINCT v.visitor_id) | [{"table": "pendo__visitor", "column": "visitor_id"}] | [] | False |
| B1 | COUNT(DISTINCT v.visitor_id) | [{"table": "pendo__visitor", "column": "visitor_id"}] | [] | False |


## S29

类别 `data`；来源 `query_db`；调用 `e691c569e4ab4d8f9b5586bc913b9aa1`；状态 `success`。

```sql
SELECT COUNT(DISTINCT account_id) AS accts_with_vf
FROM pendo__visitor v JOIN pendo__visitor_feature vf ON v.visitor_id = vf.visitor_id
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-078/attempt-01/sql/S29.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-078/attempt-01/sql/S29.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-078/attempt-01/results/S29.rows.jsonl)；完整：True；SHA256：`c14196f132c1e9be0508ae80ab52fcb3e1d3fc05880415f3dc980971df207c9e`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "v", "kind": "base", "block": null, "base_tables": ["pendo__visitor"]}, {"alias": "vf", "kind": "base", "block": null, "base_tables": ["pendo__visitor_feature"]}] | [{"type": "INNER", "right": "pendo__visitor_feature AS vf", "on": "v.visitor_id = vf.visitor_id", "using": []}] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(DISTINCT account_id) | [{"table": "pendo__visitor", "column": "account_id"}] | [] | False |


## S30

类别 `data`；来源 `query_db`；调用 `095f28eed85944dd84bd2c44c38e8f2a`；状态 `success`。

```sql
SELECT COUNT(DISTINCT vf.visitor_id) AS vf_visitors_not_in_visitor
FROM pendo__visitor_feature vf
LEFT JOIN pendo__visitor v ON vf.visitor_id = v.visitor_id
WHERE v.visitor_id IS NULL
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-078/attempt-01/sql/S30.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-078/attempt-01/sql/S30.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-078/attempt-01/results/S30.rows.jsonl)；完整：True；SHA256：`5c624bc48e7531fa05fed66c36f87ca3c2e8b2f90931f21c652302a6a2fa30e7`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "vf", "kind": "base", "block": null, "base_tables": ["pendo__visitor_feature"]}, {"alias": "v", "kind": "base", "block": null, "base_tables": ["pendo__visitor"]}] | [{"type": "LEFT", "right": "pendo__visitor AS v", "on": "vf.visitor_id = v.visitor_id", "using": []}] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(DISTINCT vf.visitor_id) | [{"table": "pendo__visitor_feature", "column": "visitor_id"}] | [] | False |


## S31

类别 `data`；来源 `query_db`；调用 `6258d1e495504a96bc1f4c02b5a2593e`；状态 `success`。

```sql
SELECT COUNT(DISTINCT vf.visitor_id) AS vf_in_visitor
FROM pendo__visitor_feature vf
JOIN pendo__visitor v ON vf.visitor_id = v.visitor_id
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-078/attempt-01/sql/S31.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-078/attempt-01/sql/S31.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-078/attempt-01/results/S31.rows.jsonl)；完整：True；SHA256：`c14196f132c1e9be0508ae80ab52fcb3e1d3fc05880415f3dc980971df207c9e`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "vf", "kind": "base", "block": null, "base_tables": ["pendo__visitor_feature"]}, {"alias": "v", "kind": "base", "block": null, "base_tables": ["pendo__visitor"]}] | [{"type": "INNER", "right": "pendo__visitor AS v", "on": "vf.visitor_id = v.visitor_id", "using": []}] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(DISTINCT vf.visitor_id) | [{"table": "pendo__visitor_feature", "column": "visitor_id"}] | [] | False |


## S32

类别 `data`；来源 `query_db`；调用 `d4711f2d27d64e10ae936840c8613da4`；状态 `success`。

```sql
SELECT COUNT(DISTINCT vf.feature_id) AS vf_features, COUNT(DISTINCT vf.visitor_id) AS vf_visitors FROM pendo__visitor_feature vf
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-078/attempt-01/sql/S32.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-078/attempt-01/sql/S32.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-078/attempt-01/results/S32.rows.jsonl)；完整：True；SHA256：`86fb9aed6bbdb861b43686763cdd7a4480e71263e4b960c3da79129e89ec3bea`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "vf", "kind": "base", "block": null, "base_tables": ["pendo__visitor_feature"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(DISTINCT vf.feature_id) | [{"table": "pendo__visitor_feature", "column": "feature_id"}] | [] | False |
| B1 | COUNT(DISTINCT vf.visitor_id) | [{"table": "pendo__visitor_feature", "column": "visitor_id"}] | [] | False |


## S33

类别 `data`；来源 `query_db`；调用 `f43885d447ee4078bebf663c4d2b48b7`；状态 `success`。

```sql
SELECT COUNT(DISTINCT feature_id) AS feat_ids FROM pendo__feature
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-078/attempt-01/sql/S33.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-078/attempt-01/sql/S33.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-078/attempt-01/results/S33.rows.jsonl)；完整：True；SHA256：`4b7ebd95b494120f7bc16bef6e23e2f94400ec47439aefa675a0212e533ee170`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "pendo__feature", "kind": "base", "block": null, "base_tables": ["pendo__feature"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(DISTINCT feature_id) | [{"table": "pendo__feature", "column": "feature_id"}] | [] | False |


## S34

类别 `data`；来源 `query_db`；调用 `8d08fd79e11242c18af878f6951ea763`；状态 `success`。

```sql
SELECT f.feature_id, f.feature_name, f.page_name, f.app_display_name, f.app_platform, f.is_core_event,
       f.count_visitors, f.count_accounts, f.sum_clicks
FROM pendo__feature f
LIMIT 8
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-078/attempt-01/sql/S34.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-078/attempt-01/sql/S34.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-078/attempt-01/results/S34.rows.jsonl)；完整：True；SHA256：`b40ea435fa833e3db44e4681c26eab059c90f155855c96c2a92123207d5322aa`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "f", "kind": "base", "block": null, "base_tables": ["pendo__feature"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |


## S35

类别 `data`；来源 `query_db`；调用 `a4d31db5cb2b4875af69553b1734c708`；状态 `success`。

```sql
-- Distribution of last_event_on to understand churn patterns
SELECT 
  CASE 
    WHEN last_event_on >= '2024-07-01' THEN 'Active_Jul_Oct'
    WHEN last_event_on >= '2024-04-01' THEN 'Active_Apr_Jun'
    ELSE 'Active_Jan_Mar'
  END AS activity_period,
  COUNT(*) AS accounts,
  AVG(sum_minutes) AS avg_minutes,
  AVG(sum_events) AS avg_events,
  AVG(count_active_days) AS avg_active_days,
  AVG(count_active_months) AS avg_active_months,
  AVG(avg_nps_rating) AS avg_nps,
  AVG(count_associated_visitors) AS avg_visitors
FROM pendo__account
GROUP BY activity_period
ORDER BY activity_period
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-078/attempt-01/sql/S35.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-078/attempt-01/sql/S35.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-078/attempt-01/results/S35.rows.jsonl)；完整：True；SHA256：`b9f5772ecad5131a018284b1d6022d440af96f49966c7ad6a7b1abd68fec644f`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "pendo__account", "kind": "base", "block": null, "base_tables": ["pendo__account"]}] | [] | ["CASE WHEN last_event_on >= '2024-07-01' THEN 'Active_Jul_Oct' WHEN last_event_on >= '2024-04-01' THEN 'Active_Apr_Jun' ELSE 'Active_Jan_Mar' END"] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |
| B1 | AVG(sum_minutes) | [{"table": "pendo__account", "column": "sum_minutes"}] | [] | False |
| B1 | AVG(sum_events) | [{"table": "pendo__account", "column": "sum_events"}] | [] | False |
| B1 | AVG(count_active_days) | [{"table": "pendo__account", "column": "count_active_days"}] | [] | False |
| B1 | AVG(count_active_months) | [{"table": "pendo__account", "column": "count_active_months"}] | [] | False |
| B1 | AVG(avg_nps_rating) | [{"table": "pendo__account", "column": "avg_nps_rating"}] | [] | False |
| B1 | AVG(count_associated_visitors) | [{"table": "pendo__account", "column": "count_associated_visitors"}] | [] | False |


## S36

类别 `data`；来源 `query_db`；调用 `e79aa0064b03495a9df8af20d7fdc3b9`；状态 `success`。

```sql
-- Detailed distribution of last_event_on by month
SELECT substr(last_event_on,1,7) AS last_month, COUNT(*) AS accounts,
  AVG(sum_minutes) AS avg_min, AVG(sum_events) AS avg_events,
  AVG(count_active_days) AS avg_days,
  AVG(count_active_months) AS avg_months
FROM pendo__account
GROUP BY last_month
ORDER BY last_month
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-078/attempt-01/sql/S36.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-078/attempt-01/sql/S36.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-078/attempt-01/results/S36.rows.jsonl)；完整：True；SHA256：`3704c336041d07f2ce24c7ff51bfd11ccc19f74b76d368004eecfdb3e197705a`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "pendo__account", "kind": "base", "block": null, "base_tables": ["pendo__account"]}] | [] | ["SUBSTRING(last_event_on, 1, 7)"] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |
| B1 | AVG(sum_minutes) | [{"table": "pendo__account", "column": "sum_minutes"}] | [] | False |
| B1 | AVG(sum_events) | [{"table": "pendo__account", "column": "sum_events"}] | [] | False |
| B1 | AVG(count_active_days) | [{"table": "pendo__account", "column": "count_active_days"}] | [] | False |
| B1 | AVG(count_active_months) | [{"table": "pendo__account", "column": "count_active_months"}] | [] | False |


## S37

类别 `data`；来源 `query_db`；调用 `db957914949047db8013282ea8eeb592`；状态 `success`。

```sql
-- Check distribution of count_associated_visitors, NPS, etc.
SELECT 
  MIN(count_associated_visitors) AS min_visitors,
  AVG(count_associated_visitors) AS avg_visitors,
  MAX(count_associated_visitors) AS max_visitors,
  MIN(count_active_visitors) AS min_active_vis,
  AVG(count_active_visitors) AS avg_active_vis,
  MAX(count_active_visitors) AS max_active_vis,
  MIN(count_page_viewing_visitors) AS min_pv,
  AVG(count_page_viewing_visitors) AS avg_pv,
  MAX(count_page_viewing_visitors) AS max_pv,
  MIN(count_feature_clicking_visitors) AS min_fc,
  AVG(count_feature_clicking_visitors) AS avg_fc,
  MAX(count_feature_clicking_visitors) AS max_fc
FROM pendo__account
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-078/attempt-01/sql/S37.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-078/attempt-01/sql/S37.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-078/attempt-01/results/S37.rows.jsonl)；完整：True；SHA256：`3f86460e28ae3bd3d3fd50f2fbdf4a957ddb835095edcb48d3f8ca5867935c9c`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "pendo__account", "kind": "base", "block": null, "base_tables": ["pendo__account"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | MIN(count_associated_visitors) | [{"table": "pendo__account", "column": "count_associated_visitors"}] | [] | False |
| B1 | AVG(count_associated_visitors) | [{"table": "pendo__account", "column": "count_associated_visitors"}] | [] | False |
| B1 | MAX(count_associated_visitors) | [{"table": "pendo__account", "column": "count_associated_visitors"}] | [] | False |
| B1 | MIN(count_active_visitors) | [{"table": "pendo__account", "column": "count_active_visitors"}] | [] | False |
| B1 | AVG(count_active_visitors) | [{"table": "pendo__account", "column": "count_active_visitors"}] | [] | False |
| B1 | MAX(count_active_visitors) | [{"table": "pendo__account", "column": "count_active_visitors"}] | [] | False |
| B1 | MIN(count_page_viewing_visitors) | [{"table": "pendo__account", "column": "count_page_viewing_visitors"}] | [] | False |
| B1 | AVG(count_page_viewing_visitors) | [{"table": "pendo__account", "column": "count_page_viewing_visitors"}] | [] | False |
| B1 | MAX(count_page_viewing_visitors) | [{"table": "pendo__account", "column": "count_page_viewing_visitors"}] | [] | False |
| B1 | MIN(count_feature_clicking_visitors) | [{"table": "pendo__account", "column": "count_feature_clicking_visitors"}] | [] | False |
| B1 | AVG(count_feature_clicking_visitors) | [{"table": "pendo__account", "column": "count_feature_clicking_visitors"}] | [] | False |
| B1 | MAX(count_feature_clicking_visitors) | [{"table": "pendo__account", "column": "count_feature_clicking_visitors"}] | [] | False |


## S38

类别 `data`；来源 `query_db`；调用 `ed7316c729444a7fabefd74ef8ed219f`；状态 `success`。

```sql
-- Check feature usage metrics distribution
SELECT 
  MIN(average_daily_minutes) AS min_avg_daily_min,
  AVG(average_daily_minutes) AS avg_avg_daily_min,
  MAX(average_daily_minutes) AS max_avg_daily_min,
  MIN(average_daily_events) AS min_avg_daily_evt,
  AVG(average_daily_events) AS avg_avg_daily_evt,
  MAX(average_daily_events) AS max_avg_daily_evt,
  COUNT(CASE WHEN avg_nps_rating IS NOT NULL THEN 1 END) AS nps_not_null,
  COUNT(CASE WHEN avg_nps_rating IS NULL THEN 1 END) AS nps_null
FROM pendo__account
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-078/attempt-01/sql/S38.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-078/attempt-01/sql/S38.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-078/attempt-01/results/S38.rows.jsonl)；完整：True；SHA256：`98cf607faeffcd1dd297b7f4cf57e80c43c9977caa27ab680d4bfb5d510af5b5`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "pendo__account", "kind": "base", "block": null, "base_tables": ["pendo__account"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | MIN(average_daily_minutes) | [{"table": "pendo__account", "column": "average_daily_minutes"}] | [] | False |
| B1 | AVG(average_daily_minutes) | [{"table": "pendo__account", "column": "average_daily_minutes"}] | [] | False |
| B1 | MAX(average_daily_minutes) | [{"table": "pendo__account", "column": "average_daily_minutes"}] | [] | False |
| B1 | MIN(average_daily_events) | [{"table": "pendo__account", "column": "average_daily_events"}] | [] | False |
| B1 | AVG(average_daily_events) | [{"table": "pendo__account", "column": "average_daily_events"}] | [] | False |
| B1 | MAX(average_daily_events) | [{"table": "pendo__account", "column": "average_daily_events"}] | [] | False |
| B1 | COUNT(CASE WHEN NOT avg_nps_rating IS NULL THEN 1 END) | [] | [{"table": "pendo__account", "column": "avg_nps_rating"}] | False |
| B1 | COUNT(CASE WHEN avg_nps_rating IS NULL THEN 1 END) | [] | [{"table": "pendo__account", "column": "avg_nps_rating"}] | False |


## S39

类别 `data`；来源 `query_db`；调用 `45d5a55b00f441b099c3f66af6e20a4f`；状态 `failed`。

```sql
-- Visitor-level features per account: browser and OS diversity
SELECT 
  v.account_id,
  COUNT(DISTINCT v.last_browser_name) AS browser_diversity,
  COUNT(DISTINCT v.last_operating_system) AS os_diversity,
  AVG(v.sum_minutes) AS avg_visitor_minutes,
  AVG(v.sum_events) AS avg_visitor_events,
  STDDEV(v.sum_minutes) AS std_visitor_minutes,
  STDDEV(v.sum_events) AS std_visitor_events,
  AVG(v.average_daily_minutes) AS avg_visitor_daily_min,
  AVG(v.average_daily_events) AS avg_visitor_daily_events,
  AVG(v.count_active_days) AS avg_visitor_active_days
FROM pendo__visitor v
GROUP BY v.account_id
LIMIT 10
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-078/attempt-01/sql/S39.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-078/attempt-01/sql/S39.parameters.json)。

错误：`OperationalError('no such function: STDDEV')`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "v", "kind": "base", "block": null, "base_tables": ["pendo__visitor"]}] | [] | ["v.account_id"] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(DISTINCT v.last_browser_name) | [{"table": "pendo__visitor", "column": "last_browser_name"}] | [] | False |
| B1 | COUNT(DISTINCT v.last_operating_system) | [{"table": "pendo__visitor", "column": "last_operating_system"}] | [] | False |
| B1 | AVG(v.sum_minutes) | [{"table": "pendo__visitor", "column": "sum_minutes"}] | [] | False |
| B1 | AVG(v.sum_events) | [{"table": "pendo__visitor", "column": "sum_events"}] | [] | False |
| B1 | STDDEV(v.sum_minutes) | [{"table": "pendo__visitor", "column": "sum_minutes"}] | [] | False |
| B1 | STDDEV(v.sum_events) | [{"table": "pendo__visitor", "column": "sum_events"}] | [] | False |
| B1 | AVG(v.average_daily_minutes) | [{"table": "pendo__visitor", "column": "average_daily_minutes"}] | [] | False |
| B1 | AVG(v.average_daily_events) | [{"table": "pendo__visitor", "column": "average_daily_events"}] | [] | False |
| B1 | AVG(v.count_active_days) | [{"table": "pendo__visitor", "column": "count_active_days"}] | [] | False |


## S40

类别 `data`；来源 `query_db`；调用 `179172ad967e44a98afe2e29a4c162bb`；状态 `success`。

```sql
SELECT a.account_id, a.count_associated_visitors, a.count_active_days, a.count_active_months,
       a.sum_minutes, a.sum_events, a.avg_nps_rating, a.last_event_on
FROM pendo__account a
WHERE a.account_id IN (
  SELECT DISTINCT v.account_id
  FROM pendo__visitor v
  JOIN pendo__visitor_daily_metrics dm ON v.visitor_id = dm.visitor_id
)
ORDER BY a.account_id
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-078/attempt-01/sql/S40.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-078/attempt-01/sql/S40.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-078/attempt-01/results/S40.rows.jsonl)；完整：True；SHA256：`101b720833c03d6b2810a5460e0afae985d6de949cd3fc348bf768b83544d34d`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "v", "kind": "base", "block": null, "base_tables": ["pendo__visitor"]}, {"alias": "dm", "kind": "base", "block": null, "base_tables": ["pendo__visitor_daily_metrics"]}] | [{"type": "INNER", "right": "pendo__visitor_daily_metrics AS dm", "on": "v.visitor_id = dm.visitor_id", "using": []}] | [] |
| B2 | [{"alias": "a", "kind": "base", "block": null, "base_tables": ["pendo__account"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |


## S41

类别 `data`；来源 `query_db`；调用 `61e7dda531ef4a779bd043d31e55a3b4`；状态 `success`。

```sql
-- Number of daily metric rows per account
SELECT v.account_id, COUNT(*) AS dm_rows, COUNT(DISTINCT dm.visitor_id) AS dm_visitors,
       MIN(dm.date_day) AS min_day, MAX(dm.date_day) AS max_day
FROM pendo__visitor_daily_metrics dm
JOIN pendo__visitor v ON dm.visitor_id = v.visitor_id
GROUP BY v.account_id
ORDER BY dm_rows DESC
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-078/attempt-01/sql/S41.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-078/attempt-01/sql/S41.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-078/attempt-01/results/S41.rows.jsonl)；完整：True；SHA256：`8aa9b5eaf33ab52bf790926680a134c20facea20bfce1397885be9d8a09078a2`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "dm", "kind": "base", "block": null, "base_tables": ["pendo__visitor_daily_metrics"]}, {"alias": "v", "kind": "base", "block": null, "base_tables": ["pendo__visitor"]}] | [{"type": "INNER", "right": "pendo__visitor AS v", "on": "dm.visitor_id = v.visitor_id", "using": []}] | ["v.account_id"] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |
| B1 | COUNT(DISTINCT dm.visitor_id) | [{"table": "pendo__visitor_daily_metrics", "column": "visitor_id"}] | [] | False |
| B1 | MIN(dm.date_day) | [{"table": "pendo__visitor_daily_metrics", "column": "date_day"}] | [] | False |
| B1 | MAX(dm.date_day) | [{"table": "pendo__visitor_daily_metrics", "column": "date_day"}] | [] | False |


## S42

类别 `data`；来源 `query_db`；调用 `37d4a5fe5f714cc38924b3973a2316df`；状态 `success`。

```sql
-- Check null columns in account table
SELECT COUNT(*) AS total,
  SUM(CASE WHEN min_nps_rating IS NULL THEN 1 ELSE 0 END) AS null_min_nps,
  SUM(CASE WHEN max_nps_rating IS NULL THEN 1 ELSE 0 END) AS null_max_nps,
  SUM(CASE WHEN avg_nps_rating IS NULL THEN 1 ELSE 0 END) AS null_avg_nps,
  SUM(CASE WHEN count_active_visitors IS NULL THEN 1 ELSE 0 END) AS null_active_vis,
  SUM(CASE WHEN count_page_viewing_visitors IS NULL THEN 1 ELSE 0 END) AS null_pv,
  SUM(CASE WHEN count_feature_clicking_visitors IS NULL THEN 1 ELSE 0 END) AS null_fc
FROM pendo__account
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-078/attempt-01/sql/S42.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-078/attempt-01/sql/S42.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-078/attempt-01/results/S42.rows.jsonl)；完整：True；SHA256：`aae036e6200a559fd510bf937cbde340786e6a9d74ff44efa0450178df67a15e`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "pendo__account", "kind": "base", "block": null, "base_tables": ["pendo__account"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |
| B1 | SUM(CASE WHEN min_nps_rating IS NULL THEN 1 ELSE 0 END) | [] | [{"table": "pendo__account", "column": "min_nps_rating"}] | False |
| B1 | SUM(CASE WHEN max_nps_rating IS NULL THEN 1 ELSE 0 END) | [] | [{"table": "pendo__account", "column": "max_nps_rating"}] | False |
| B1 | SUM(CASE WHEN avg_nps_rating IS NULL THEN 1 ELSE 0 END) | [] | [{"table": "pendo__account", "column": "avg_nps_rating"}] | False |
| B1 | SUM(CASE WHEN count_active_visitors IS NULL THEN 1 ELSE 0 END) | [] | [{"table": "pendo__account", "column": "count_active_visitors"}] | False |
| B1 | SUM(CASE WHEN count_page_viewing_visitors IS NULL THEN 1 ELSE 0 END) | [] | [{"table": "pendo__account", "column": "count_page_viewing_visitors"}] | False |
| B1 | SUM(CASE WHEN count_feature_clicking_visitors IS NULL THEN 1 ELSE 0 END) | [] | [{"table": "pendo__account", "column": "count_feature_clicking_visitors"}] | False |


## S43

类别 `data`；来源 `query_db`；调用 `ae0da74d62344a509d5bcdb32989b18c`；状态 `success`。

```sql
-- Check correlation between duration, frequency, and other metrics
-- First, let's see the percentile distribution of key metrics
SELECT
  ROUND((count_active_days - 1.0) / 10) * 10 AS days_bucket,
  COUNT(*) AS cnt,
  AVG(sum_minutes) AS avg_min,
  AVG(sum_events) AS avg_events,
  AVG(avg_nps_rating) AS avg_nps,
  AVG(count_associated_visitors) AS avg_visitors
FROM pendo__account
GROUP BY days_bucket
ORDER BY days_bucket
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-078/attempt-01/sql/S43.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-078/attempt-01/sql/S43.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-078/attempt-01/results/S43.rows.jsonl)；完整：True；SHA256：`9c42354214a74e1359818f35b5d2d74ef2d62d67b09197f4b77a290c676aa6a4`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "pendo__account", "kind": "base", "block": null, "base_tables": ["pendo__account"]}] | [] | ["ROUND((count_active_days - 1.0) / 10) * 10"] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |
| B1 | AVG(sum_minutes) | [{"table": "pendo__account", "column": "sum_minutes"}] | [] | False |
| B1 | AVG(sum_events) | [{"table": "pendo__account", "column": "sum_events"}] | [] | False |
| B1 | AVG(avg_nps_rating) | [{"table": "pendo__account", "column": "avg_nps_rating"}] | [] | False |
| B1 | AVG(count_associated_visitors) | [{"table": "pendo__account", "column": "count_associated_visitors"}] | [] | False |


## S44

类别 `data`；来源 `query_db`；调用 `9c2ac9d90b534048b2541cdefee6b611`；状态 `success`。

```sql
-- Full account-level feature set
SELECT 
  account_id,
  count_associated_visitors,
  min_nps_rating,
  max_nps_rating,
  avg_nps_rating,
  count_active_visitors,
  count_page_viewing_visitors,
  count_feature_clicking_visitors,
  count_active_days,
  count_active_months,
  sum_minutes,
  sum_events,
  count_event_records,
  average_daily_minutes,
  average_daily_events,
  first_event_on,
  last_event_on,
  -- Derived metrics
  CAST(count_active_visitors AS REAL) / NULLIF(count_associated_visitors, 0) AS active_visitor_ratio,
  CAST(count_page_viewing_visitors AS REAL) / NULLIF(count_associated_visitors, 0) AS page_view_ratio,
  CAST(count_feature_clicking_visitors AS REAL) / NULLIF(count_associated_visitors, 0) AS feature_click_ratio,
  CAST(sum_minutes AS REAL) / NULLIF(count_active_days, 0) AS minutes_per_active_day,
  CAST(sum_events AS REAL) / NULLIF(count_active_days, 0) AS events_per_active_day
FROM pendo__account
ORDER BY account_id
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-078/attempt-01/sql/S44.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-078/attempt-01/sql/S44.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-078/attempt-01/results/S44.rows.jsonl)；完整：True；SHA256：`73d5d9ea5d5730695ee20d59e37df9dd3ff9a524b156ce8a5c2863acbb07ab83`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "pendo__account", "kind": "base", "block": null, "base_tables": ["pendo__account"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |


## S45

类别 `data`；来源 `python`；调用 `617fd97ad088491c940d02cc31142770`；状态 `success`。

```sql

SELECT 
  account_id,
  count_associated_visitors,
  min_nps_rating,
  max_nps_rating,
  avg_nps_rating,
  count_active_visitors,
  count_page_viewing_visitors,
  count_feature_clicking_visitors,
  count_active_days,
  count_active_months,
  sum_minutes,
  sum_events,
  count_event_records,
  average_daily_minutes,
  average_daily_events,
  first_event_on,
  last_event_on,
  CAST(count_active_visitors AS REAL) / NULLIF(count_associated_visitors, 0) AS active_visitor_ratio,
  CAST(count_page_viewing_visitors AS REAL) / NULLIF(count_associated_visitors, 0) AS page_view_ratio,
  CAST(count_feature_clicking_visitors AS REAL) / NULLIF(count_associated_visitors, 0) AS feature_click_ratio,
  CAST(sum_minutes AS REAL) / NULLIF(count_active_days, 0) AS minutes_per_active_day,
  CAST(sum_events AS REAL) / NULLIF(count_active_days, 0) AS events_per_active_day
FROM pendo__account
ORDER BY account_id

```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-078/attempt-01/sql/S45.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-078/attempt-01/sql/S45.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-078/attempt-01/results/S45.rows.jsonl)；完整：True；SHA256：`73d5d9ea5d5730695ee20d59e37df9dd3ff9a524b156ce8a5c2863acbb07ab83`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "pendo__account", "kind": "base", "block": null, "base_tables": ["pendo__account"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |


## S46

类别 `data`；来源 `python`；调用 `7960d38870d7466e8adea79f0d0dd632`；状态 `success`。

```sql

SELECT 
  account_id, count_associated_visitors, avg_nps_rating,
  count_active_visitors, count_page_viewing_visitors, count_feature_clicking_visitors,
  count_active_days, count_active_months, sum_minutes, sum_events,
  average_daily_minutes, average_daily_events, first_event_on, last_event_on,
  CAST(count_active_visitors AS REAL) / NULLIF(count_associated_visitors, 0) AS active_visitor_ratio,
  CAST(count_page_viewing_visitors AS REAL) / NULLIF(count_associated_visitors, 0) AS page_view_ratio,
  CAST(count_feature_clicking_visitors AS REAL) / NULLIF(count_associated_visitors, 0) AS feature_click_ratio,
  CAST(sum_minutes AS REAL) / NULLIF(count_active_days, 0) AS minutes_per_active_day,
  CAST(sum_events AS REAL) / NULLIF(count_active_days, 0) AS events_per_active_day
FROM pendo__account ORDER BY account_id

```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-078/attempt-01/sql/S46.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-078/attempt-01/sql/S46.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-078/attempt-01/results/S46.rows.jsonl)；完整：True；SHA256：`edf0f81454bec1bc921b253dde90ca737f360a4002f474273c2904988069e04b`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "pendo__account", "kind": "base", "block": null, "base_tables": ["pendo__account"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |


## S47

类别 `data`；来源 `python`；调用 `1dc73ef35f794d1bb5a466a1159fcace`；状态 `success`。

```sql

SELECT v.account_id,
  COUNT(DISTINCT v.last_browser_name) AS browser_diversity,
  COUNT(DISTINCT v.last_operating_system) AS os_diversity,
  AVG(v.sum_minutes) AS avg_visitor_minutes,
  AVG(v.sum_events) AS avg_visitor_events,
  AVG(v.average_daily_minutes) AS avg_visitor_daily_min,
  AVG(v.average_daily_events) AS avg_visitor_daily_events,
  AVG(v.count_active_days) AS avg_visitor_active_days,
  AVG(v.count_active_months) AS avg_visitor_active_months,
  SUM(v.sum_minutes) AS total_visitor_minutes,
  SUM(v.sum_events) AS total_visitor_events
FROM pendo__visitor v
GROUP BY v.account_id
ORDER BY v.account_id

```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-078/attempt-01/sql/S47.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-078/attempt-01/sql/S47.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-078/attempt-01/results/S47.rows.jsonl)；完整：True；SHA256：`233efbda9f8e7756df37e23f00db89996fde5a5a540edffa2fb6272420c11608`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "v", "kind": "base", "block": null, "base_tables": ["pendo__visitor"]}] | [] | ["v.account_id"] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(DISTINCT v.last_browser_name) | [{"table": "pendo__visitor", "column": "last_browser_name"}] | [] | False |
| B1 | COUNT(DISTINCT v.last_operating_system) | [{"table": "pendo__visitor", "column": "last_operating_system"}] | [] | False |
| B1 | AVG(v.sum_minutes) | [{"table": "pendo__visitor", "column": "sum_minutes"}] | [] | False |
| B1 | AVG(v.sum_events) | [{"table": "pendo__visitor", "column": "sum_events"}] | [] | False |
| B1 | AVG(v.average_daily_minutes) | [{"table": "pendo__visitor", "column": "average_daily_minutes"}] | [] | False |
| B1 | AVG(v.average_daily_events) | [{"table": "pendo__visitor", "column": "average_daily_events"}] | [] | False |
| B1 | AVG(v.count_active_days) | [{"table": "pendo__visitor", "column": "count_active_days"}] | [] | False |
| B1 | AVG(v.count_active_months) | [{"table": "pendo__visitor", "column": "count_active_months"}] | [] | False |
| B1 | SUM(v.sum_minutes) | [{"table": "pendo__visitor", "column": "sum_minutes"}] | [] | False |
| B1 | SUM(v.sum_events) | [{"table": "pendo__visitor", "column": "sum_events"}] | [] | False |


## S48

类别 `data`；来源 `python`；调用 `c4e0f6dc74fb40de9d48c6aa740d5ccf`；状态 `success`。

```sql

SELECT v.account_id,
  COUNT(DISTINCT v.last_browser_name) AS browser_diversity,
  COUNT(DISTINCT v.last_operating_system) AS os_diversity,
  AVG(v.sum_minutes) AS avg_visitor_minutes,
  AVG(v.sum_events) AS avg_visitor_events,
  AVG(v.average_daily_minutes) AS avg_visitor_daily_min,
  AVG(v.average_daily_events) AS avg_visitor_daily_events,
  AVG(v.count_active_days) AS avg_visitor_active_days,
  AVG(v.count_active_months) AS avg_visitor_active_months,
  SUM(v.sum_minutes) AS total_visitor_minutes,
  SUM(v.sum_events) AS total_visitor_events
FROM pendo__visitor v
GROUP BY v.account_id
ORDER BY v.account_id

```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-078/attempt-01/sql/S48.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-078/attempt-01/sql/S48.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-078/attempt-01/results/S48.rows.jsonl)；完整：True；SHA256：`233efbda9f8e7756df37e23f00db89996fde5a5a540edffa2fb6272420c11608`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "v", "kind": "base", "block": null, "base_tables": ["pendo__visitor"]}] | [] | ["v.account_id"] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(DISTINCT v.last_browser_name) | [{"table": "pendo__visitor", "column": "last_browser_name"}] | [] | False |
| B1 | COUNT(DISTINCT v.last_operating_system) | [{"table": "pendo__visitor", "column": "last_operating_system"}] | [] | False |
| B1 | AVG(v.sum_minutes) | [{"table": "pendo__visitor", "column": "sum_minutes"}] | [] | False |
| B1 | AVG(v.sum_events) | [{"table": "pendo__visitor", "column": "sum_events"}] | [] | False |
| B1 | AVG(v.average_daily_minutes) | [{"table": "pendo__visitor", "column": "average_daily_minutes"}] | [] | False |
| B1 | AVG(v.average_daily_events) | [{"table": "pendo__visitor", "column": "average_daily_events"}] | [] | False |
| B1 | AVG(v.count_active_days) | [{"table": "pendo__visitor", "column": "count_active_days"}] | [] | False |
| B1 | AVG(v.count_active_months) | [{"table": "pendo__visitor", "column": "count_active_months"}] | [] | False |
| B1 | SUM(v.sum_minutes) | [{"table": "pendo__visitor", "column": "sum_minutes"}] | [] | False |
| B1 | SUM(v.sum_events) | [{"table": "pendo__visitor", "column": "sum_events"}] | [] | False |


## S49

类别 `data`；来源 `query_db`；调用 `d073cbb0d8e7481c8a7c2f4cd0569720`；状态 `success`。

```sql
-- Monthly account-level value from daily metrics (for trend analysis)
SELECT v.account_id,
       substr(dm.date_day, 1, 7) AS month,
       SUM(dm.sum_minutes) AS month_minutes,
       SUM(dm.sum_events) AS month_events,
       COUNT(DISTINCT dm.visitor_id) AS month_visitors,
       COUNT(DISTINCT dm.date_day) AS month_active_days
FROM pendo__visitor_daily_metrics dm
JOIN pendo__visitor v ON dm.visitor_id = v.visitor_id
GROUP BY v.account_id, substr(dm.date_day, 1, 7)
ORDER BY v.account_id, month
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-078/attempt-01/sql/S49.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-078/attempt-01/sql/S49.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-078/attempt-01/results/S49.rows.jsonl)；完整：True；SHA256：`bc8a25ce85d73b969c4e14f3f94e7b948ce4dca760e238bdf8d133a88719d8cf`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "dm", "kind": "base", "block": null, "base_tables": ["pendo__visitor_daily_metrics"]}, {"alias": "v", "kind": "base", "block": null, "base_tables": ["pendo__visitor"]}] | [{"type": "INNER", "right": "pendo__visitor AS v", "on": "dm.visitor_id = v.visitor_id", "using": []}] | ["v.account_id", "SUBSTRING(dm.date_day, 1, 7)"] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | SUM(dm.sum_minutes) | [{"table": "pendo__visitor_daily_metrics", "column": "sum_minutes"}] | [] | False |
| B1 | SUM(dm.sum_events) | [{"table": "pendo__visitor_daily_metrics", "column": "sum_events"}] | [] | False |
| B1 | COUNT(DISTINCT dm.visitor_id) | [{"table": "pendo__visitor_daily_metrics", "column": "visitor_id"}] | [] | False |
| B1 | COUNT(DISTINCT dm.date_day) | [{"table": "pendo__visitor_daily_metrics", "column": "date_day"}] | [] | False |


## S50

类别 `data`；来源 `python`；调用 `7019d0a8ea864bb6af75eae8e8dd72ca`；状态 `success`。

```sql

SELECT v.account_id,
       substr(dm.date_day, 1, 7) AS month,
       SUM(dm.sum_minutes) AS month_minutes,
       SUM(dm.sum_events) AS month_events,
       COUNT(DISTINCT dm.visitor_id) AS month_visitors,
       COUNT(DISTINCT dm.date_day) AS month_active_days
FROM pendo__visitor_daily_metrics dm
JOIN pendo__visitor v ON dm.visitor_id = v.visitor_id
GROUP BY v.account_id, substr(dm.date_day, 1, 7)
ORDER BY v.account_id, month

```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-078/attempt-01/sql/S50.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-078/attempt-01/sql/S50.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-078/attempt-01/results/S50.rows.jsonl)；完整：True；SHA256：`bc8a25ce85d73b969c4e14f3f94e7b948ce4dca760e238bdf8d133a88719d8cf`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "dm", "kind": "base", "block": null, "base_tables": ["pendo__visitor_daily_metrics"]}, {"alias": "v", "kind": "base", "block": null, "base_tables": ["pendo__visitor"]}] | [{"type": "INNER", "right": "pendo__visitor AS v", "on": "dm.visitor_id = v.visitor_id", "using": []}] | ["v.account_id", "SUBSTRING(dm.date_day, 1, 7)"] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | SUM(dm.sum_minutes) | [{"table": "pendo__visitor_daily_metrics", "column": "sum_minutes"}] | [] | False |
| B1 | SUM(dm.sum_events) | [{"table": "pendo__visitor_daily_metrics", "column": "sum_events"}] | [] | False |
| B1 | COUNT(DISTINCT dm.visitor_id) | [{"table": "pendo__visitor_daily_metrics", "column": "visitor_id"}] | [] | False |
| B1 | COUNT(DISTINCT dm.date_day) | [{"table": "pendo__visitor_daily_metrics", "column": "date_day"}] | [] | False |

