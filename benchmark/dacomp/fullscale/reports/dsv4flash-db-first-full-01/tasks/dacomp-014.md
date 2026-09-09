# dacomp-014

I'm just starting out as a video creator. Please analyze the data from the monthly ranking…

运行：已提交。官方未评分。全部 SQL 尝试/成功 51/51；数据 SQL 49/49；Python 15 次。

完整原题：

I'm just starting out as a video creator. Please analyze the data from the monthly rankings and tell me how to make videos that are more likely to go viral.

| 表 | 行数 | 列数 |
| --- | --- | --- |
| sheet1 | 5200 | 21 |


实际路线（分析者依据 SQL/源码概括，不代表 Agent 自述）：检查月榜与重复视频 → 分析类别、播放和互动指标 → 拟合播放量回归 → 筛选新手作者并比较类别表现 → 绘制互动与播放分布。

数据库大小：3,022,848 字节。

## 数据 SQL

| SQL | 状态 | 基础表 | Join 输入/类型 | GROUP BY | 聚合表达式 | 结果行数 | 数据库 ms |
| --- | --- | --- | --- | --- | --- | --- | --- |
| [S3/Q1](#s3) | success | ["sheet1"] | 0 / {} | [] | [] | 20 | 0.447 |
| [S4/Q2](#s4) | success | ["sheet1"] | 0 / {} | [] | ["COUNT(*)"] | 1 | 1.87 |
| [S5/Q3](#s5) | success | ["sheet1"] | 0 / {} | [] | [] | 61 | 2.77 |
| [S6/Q4](#s6) | success | ["sheet1"] | 0 / {} | [] | [] | 13 | 2.428 |
| [S7/Q5](#s7) | success | ["sheet1"] | 0 / {} | [] | [] | 3 | 2.565 |
| [S8/Q6](#s8) | success | ["sheet1"] | 0 / {} | [] | [] | 246 | 3.652 |
| [S9/Q7](#s9) | success | ["sheet1"] | 0 / {} | [] | ["MIN(\"Rank\")", "MAX(\"Rank\")"] | 1 | 1.501 |
| [S10/Q8](#s10) | success | ["sheet1"] | 0 / {} | [] | [] | 10 | 0.344 |
| [S11/Q9](#s11) | success | ["sheet1"] | 0 / {} | [] | ["MIN(\"Views\")", "AVG(\"Views\")", "MAX(\"Views\")", "MIN(\"Likes\")", "AVG(\"Likes\")", "MAX(\"Likes\")", "MIN(\"Coins\")", "AVG(\"Coins\")", "MAX(\"Coins\")", "MIN(\"Favorites\")", "AVG(\"Favorites\")", "MAX(\"Favorites\")", "MIN(\"Shares\")", "AVG(\"Shares\")", "MAX(\"Shares\")", "MIN(\"Comments\")", "AVG(\"Comments\")", "MAX(\"Comments\")", "MIN(\"Danmaku Count\")", "AVG(\"Danmaku Count\")", "MAX(\"Danmaku Count\")"] | 1 | 5.088 |
| [S12/Q10](#s12) | success | ["sheet1"] | 0 / {} | ["\"Video Category\""] | ["COUNT(*)", "AVG(\"Views\")", "AVG(\"Likes\")", "AVG(\"Coins\")", "AVG(\"Favorites\")", "AVG(\"Shares\")", "AVG(\"Comments\")", "AVG(\"Danmaku Count\")", "AVG(\"Overall Score\")"] | 20 | 5.526 |
| [S13/Q11](#s13) | success | ["sheet1"] | 0 / {} | ["\"Main Category\""] | ["COUNT(*)", "AVG(\"Views\")", "AVG(\"Likes\")", "AVG(\"Coins\")", "AVG(\"Favorites\")", "AVG(\"Shares\")", "AVG(\"Overall Score\")", "AVG(\"Rank\")"] | 13 | 4.481 |
| [S14/Q12](#s14) | success | ["sheet1"] | 0 / {} | ["\"Creator Gender\""] | ["COUNT(*)", "AVG(\"Views\")", "AVG(\"Likes\")", "AVG(\"Coins\")", "AVG(\"Favorites\")", "AVG(\"Shares\")", "AVG(\"Overall Score\")", "AVG(\"Creator Followers\")", "AVG(\"Creator Video Count\")"] | 3 | 5.11 |
| [S15/Q13](#s15) | success | ["sheet1"] | 0 / {} | ["CASE WHEN NOT \"Bilibili Personal Verification\" IS NULL THEN 'Verified' ELSE 'Not Verified' END"] | ["COUNT(*)", "AVG(\"Views\")", "AVG(\"Likes\")", "AVG(\"Coins\")", "AVG(\"Favorites\")", "AVG(\"Shares\")", "AVG(\"Overall Score\")", "AVG(\"Creator Followers\")"] | 2 | 4.929 |
| [S16/Q14](#s16) | success | ["sheet1"] | 0 / {} | ["\"Creator Video Count\""] | ["COUNT(*)", "AVG(\"Views\")", "AVG(\"Likes\")", "AVG(\"Coins\")", "AVG(\"Favorites\")", "AVG(\"Shares\")"] | 20 | 3.376 |
| [S17/Q15](#s17) | success | ["sheet1"] | 0 / {} | ["\"Video Category\""] | ["COUNT(*)", "AVG(\"Views\")", "AVG(\"Likes\")", "AVG(\"Coins\")", "AVG(\"Favorites\")", "AVG(\"Shares\")", "AVG(\"Comments\")", "AVG(\"Danmaku Count\")", "AVG(\"Overall Score\")", "AVG(\"Views\")", "AVG(\"Views\")", "AVG(\"Views\")", "AVG(\"Views\")", "AVG(\"Likes\")", "AVG(\"Coins\")", "AVG(\"Favorites\")", "AVG(\"Shares\")"] | 20 | 5.4 |
| [S18/Q16](#s18) | success | ["sheet1"] | 0 / {} | ["\"Video Category\""] | ["COUNT(*)", "AVG(\"Views\")", "AVG(\"Views\")", "AVG(\"Views\")", "AVG(\"Views\")", "AVG(\"Views\")", "AVG(\"Views\")", "AVG(\"Views\")", "AVG(\"Likes\")", "AVG(\"Coins\")", "AVG(\"Favorites\")", "AVG(\"Shares\")", "AVG(\"Comments\")", "AVG(\"Danmaku Count\")"] | 20 | 5.123 |
| [S19/Q17](#s19) | success | ["sheet1"] | 0 / {} | ["CASE WHEN \"Rank\" <= 10 THEN 'Top 10' WHEN \"Rank\" <= 30 THEN '11-30' WHEN \"Rank\" <= 50 THEN '31-50' WHEN \"Rank\" <= 70 THEN '51-70' ELSE '71-100' END", "\"Main Category\""] | ["COUNT(*)"] | 65 | 3.978 |
| [S20/Q18](#s20) | success | ["sheet1"] | 0 / {} | [] | [] | 20 | 1.51 |
| [S21/Q19](#s21) | success | ["sheet1"] | 0 / {} | [] | ["AVG(\"Overall Score\")", "AVG(\"Views\")", "AVG(\"Likes\")", "AVG(\"Coins\")", "AVG(\"Favorites\")", "AVG(\"Shares\")", "AVG(\"Danmaku Count\")", "AVG(\"Comments\")", "AVG(\"Creator Followers\")", "AVG(\"Creator Total Views\")", "AVG(\"Creator Total Likes\")", "AVG(\"Creator Video Count\")"] | 1 | 1.636 |
| [S22/Q20](#s22) | success | ["sheet1"] | 0 / {} | [] | ["AVG(\"Overall Score\")", "AVG(\"Views\")", "AVG(\"Likes\")", "AVG(\"Coins\")", "AVG(\"Favorites\")", "AVG(\"Shares\")", "AVG(\"Danmaku Count\")", "AVG(\"Comments\")", "AVG(\"Creator Followers\")", "AVG(\"Creator Total Views\")", "AVG(\"Creator Total Likes\")", "AVG(\"Creator Video Count\")"] | 1 | 1.662 |
| [S23/Q21](#s23) | success | ["sheet1"] | 0 / {} | ["\"Main Category\""] | ["COUNT(*)", "SUM(CASE WHEN \"Rank\" <= 10 THEN 1 ELSE 0 END)", "SUM(CASE WHEN \"Rank\" <= 30 THEN 1 ELSE 0 END)", "AVG(\"Views\")", "AVG(\"Overall Score\")", "SUM(CASE WHEN \"Rank\" <= 10 THEN 1 ELSE 0 END)", "SUM(CASE WHEN \"Rank\" <= 30 THEN 1 ELSE 0 END)"] | 13 | 3.594 |
| [S24/Q22](#s24) | success | ["sheet1"] | 0 / {} | ["\"Video Category\""] | ["COUNT(*)", "SUM(CASE WHEN \"Rank\" <= 10 THEN 1 ELSE 0 END)", "AVG(\"Views\")", "AVG(\"Overall Score\")", "COUNT(*)", "COUNT(*)", "SUM(CASE WHEN \"Rank\" <= 10 THEN 1 ELSE 0 END)"] | 20 | 3.825 |
| [S25/Q23](#s25) | success | ["sheet1"] | 0 / {} | ["SUBSTRING(_id, 1, 8)"] | ["COUNT(*)"] | 5191 | 8.046 |
| [S26/Q24](#s26) | success | ["sheet1"] | 0 / {} | [] | ["COUNT(*)", "COUNT(DISTINCT \"Creator\")", "COUNT(DISTINCT \"Title\")", "COUNT(DISTINCT \"Video Category\")"] | 1 | 9.198 |
| [S27/Q25](#s27) | success | ["sheet1"] | 0 / {} | ["SUBSTRING(_id, 1, 4)"] | ["COUNT(*)"] | 1 | 2.467 |
| [S28/Q26](#s28) | success | ["sheet1"] | 0 / {} | ["\"Creator Video Count\""] | ["COUNT(*)", "AVG(\"Views\")", "AVG(\"Overall Score\")"] | 98 | 3.256 |
| [S29/Q27](#s29) | success | ["sheet1"] | 0 / {} | ["\"Creator\""] | ["COUNT(*)", "AVG(\"Rank\")", "AVG(\"Views\")", "AVG(\"Overall Score\")", "AVG(\"Creator Followers\")", "AVG(\"Creator Video Count\")", "COUNT(*)"] | 12 | 7.152 |
| [S30/Q28](#s30) | success | ["sheet1"] | 0 / {} | ["\"Creator\""] | ["COUNT(*)", "AVG(\"Rank\")", "AVG(\"Views\")", "AVG(\"Creator Followers\")", "AVG(\"Creator Video Count\")", "COUNT(*)"] | 20 | 6.939 |
| [S31/Q29](#s31) | success | ["sheet1"] | 0 / {} | ["CASE WHEN \"Creator Followers\" < 10000 THEN '1. <10k' WHEN \"Creator Followers\" < 100000 THEN '2. 10k-100k' WHEN \"Creator Followers\" < 1000000 THEN '3. 100k-1M' ELSE '4. >1M' END"] | ["COUNT(*)", "AVG(\"Views\")", "AVG(\"Overall Score\")", "AVG(\"Likes\")", "AVG(\"Shares\")", "AVG(\"Coins\")"] | 4 | 4.572 |
| [S32/Q30](#s32) | success | ["sheet1"] | 0 / {} | ["CASE WHEN \"Creator Video Count\" = 100 THEN '100 (full)' WHEN \"Creator Video Count\" < 10 THEN '1-9' WHEN \"Creator Video Count\" < 50 THEN '10-49' ELSE '50-99' END"] | ["COUNT(*)", "AVG(\"Views\")", "AVG(\"Overall Score\")", "AVG(\"Rank\")"] | 4 | 3.916 |
| [S33/Q31](#s33) | success | ["sheet1"] | 0 / {} | [] | ["COUNT(*)", "COUNT(*)", "SUM(CASE WHEN \"Views\" >= 5000000 THEN 1 ELSE 0 END)", "SUM(CASE WHEN \"Views\" >= 2000000 THEN 1 ELSE 0 END)"] | 1 | 1.91 |
| [S34/Q32](#s34) | success | ["sheet1"] | 0 / {} | ["\"Video Category\""] | ["COUNT(*)", "AVG(\"Views\")", "COUNT(*)", "SUM(CASE WHEN \"Views\" >= 2000000 THEN 1 ELSE 0 END)"] | 15 | 3.411 |
| [S35/Q33](#s35) | success | ["sheet1"] | 0 / {} | [] | [] | 326 | 3.455 |
| [S36/Q34](#s36) | success | ["sheet1"] | 0 / {} | [] | [] | 5200 | 22.985 |
| [S37/Q35](#s37) | success | ["sheet1"] | 0 / {} | ["\"Main Category\""] | ["COUNT(*)", "MIN(\"Rank\")", "MAX(\"Rank\")", "COUNT(DISTINCT \"Rank\")"] | 13 | 3.447 |
| [S38/Q36](#s38) | success | ["sheet1"] | 0 / {} | [] | ["COUNT(*)", "COUNT(DISTINCT \"Title\" \|\| '\|' \|\| \"Creator\")"] | 1 | 6.778 |
| [S39/Q37](#s39) | success | ["sheet1"] | 0 / {} | [] | [] | 5200 | 5.614 |
| [S40/Q38](#s40) | success | ["sheet1"] | 0 / {} | [] | [] | 5200 | 22.677 |
| [S41/Q39](#s41) | success | ["sheet1"] | 0 / {} | [] | [] | 5200 | 23.561 |
| [S42/Q40](#s42) | success | ["sheet1"] | 0 / {} | [] | [] | 5200 | 22.715 |
| [S43/Q41](#s43) | success | ["sheet1"] | 0 / {} | [] | [] | 5200 | 22.634 |
| [S44/Q42](#s44) | success | ["sheet1"] | 0 / {} | [] | [] | 5200 | 21.811 |
| [S45/Q43](#s45) | success | ["sheet1"] | 0 / {} | [] | [] | 5200 | 21.88 |
| [S46/Q44](#s46) | success | ["sheet1"] | 0 / {} | [] | [] | 5200 | 21.849 |
| [S47/Q45](#s47) | success | ["sheet1"] | 0 / {} | [] | [] | 5200 | 21.745 |
| [S48/Q46](#s48) | success | ["sheet1"] | 0 / {} | [] | [] | 5200 | 21.888 |
| [S49/Q47](#s49) | success | ["sheet1"] | 0 / {} | [] | [] | 5200 | 22.405 |
| [S50/Q48](#s50) | success | ["sheet1"] | 0 / {} | ["CASE WHEN NOT \"Bilibili Personal Verification\" IS NULL THEN 'Verified' ELSE 'Not Verified' END"] | ["COUNT(*)", "AVG(\"Rank\")", "COUNT(*)", "COUNT(*)", "SUM(CASE WHEN \"Views\" >= 2000000 THEN 1 ELSE 0 END)", "SUM(CASE WHEN \"Views\" >= 1000000 THEN 1 ELSE 0 END)"] | 2 | 3.732 |
| [S51/Q49](#s51) | success | ["sheet1"] | 0 / {} | ["\"Video Category\""] | ["AVG(\"Views\")", "AVG(\"Likes\")", "AVG(\"Coins\")", "AVG(\"Shares\")", "AVG(\"Favorites\")", "AVG(\"Comments\")", "AVG(\"Danmaku Count\")", "COUNT(*)"] | 15 | 2.098 |


## 元数据和设置

| SQL | 类别 | 状态 | 内容 |
| --- | --- | --- | --- |
| S1 | connection_setup | success | PRAGMA query_only=ON |
| S2 | metadata | success | SELECT name,sql FROM sqlite_master WHERE type='table' ORDER BY name |


## Python 与执行位置

人工源码审查：**database_first_violation**。P8 exports SELECT * and performs deduplication, beginner filtering, category counts/means/maxima and engagement ratios in pandas. Other calls repeat group summaries for plotting. Median/regression/plot rendering may justify Python, but do not justify moving these SQL-capable relational computations out of the database. [证据](../reviews/dacomp-014.json)。

P1：Analyze video tags to find common themes in top-performing videos. This is a text analysis task best done in Python rather than SQL.

[源码](../../../runs/dsv4flash-db-first-full-01/dacomp-014/attempt-01/python/P1.py)；[输出](../../../runs/dsv4flash-db-first-full-01/dacomp-014/attempt-01/python/P1.stdout)；[错误](../../../runs/dsv4flash-db-first-full-01/dacomp-014/attempt-01/python/P1.stderr)。检出需人工核验的 SQL 可实现操作：.query(；不能仅凭理由判为合规。

P2：Check for duplicate videos (same title+creator appearing multiple times) to understand data structure (monthly ranking snapshots).

[源码](../../../runs/dsv4flash-db-first-full-01/dacomp-014/attempt-01/python/P2.py)；[输出](../../../runs/dsv4flash-db-first-full-01/dacomp-014/attempt-01/python/P2.stdout)；[错误](../../../runs/dsv4flash-db-first-full-01/dacomp-014/attempt-01/python/P2.stderr)。检出需人工核验的 SQL 可实现操作：groupby(, .query(, sort_values(；不能仅凭理由判为合规。

P3：Decode MongoDB-style ObjectId timestamps from _id to identify the months covered by the monthly rankings, and check the number of distinct periods.

[源码](../../../runs/dsv4flash-db-first-full-01/dacomp-014/attempt-01/python/P3.py)；[输出](../../../runs/dsv4flash-db-first-full-01/dacomp-014/attempt-01/python/P3.stdout)；[错误](../../../runs/dsv4flash-db-first-full-01/dacomp-014/attempt-01/python/P3.stderr)。检出需人工核验的 SQL 可实现操作：groupby(, .query(；不能仅凭理由判为合规。

P4：Compute correlation matrix between engagement metrics and views using pandas since it is a statistical procedure not directly supported by SQLite.

[源码](../../../runs/dsv4flash-db-first-full-01/dacomp-014/attempt-01/python/P4.py)；[输出](../../../runs/dsv4flash-db-first-full-01/dacomp-014/attempt-01/python/P4.stdout)；[错误](../../../runs/dsv4flash-db-first-full-01/dacomp-014/attempt-01/python/P4.stderr)。检出需人工核验的 SQL 可实现操作：.query(, sort_values(；不能仅凭理由判为合规。

P5：Analyze creators with few followers who achieved viral success, and find the top categories with high engagement rates - this requires complex filtering and is best done in Python for visualization prep.

[源码](../../../runs/dsv4flash-db-first-full-01/dacomp-014/attempt-01/python/P5.py)；[输出](../../../runs/dsv4flash-db-first-full-01/dacomp-014/attempt-01/python/P5.stdout)；[错误](../../../runs/dsv4flash-db-first-full-01/dacomp-014/attempt-01/python/P5.stderr)。检出需人工核验的 SQL 可实现操作：groupby(, .query(, sort_values(；不能仅凭理由判为合规。

P6：Analyze what drives the Overall Score (ranking) by computing correlations between Overall Score and engagement metrics, and examine top-ranked videos. This is a regression-style statistical analysis done in Python.

[源码](../../../runs/dsv4flash-db-first-full-01/dacomp-014/attempt-01/python/P6.py)；[输出](../../../runs/dsv4flash-db-first-full-01/dacomp-014/attempt-01/python/P6.stdout)；[错误](../../../runs/dsv4flash-db-first-full-01/dacomp-014/attempt-01/python/P6.stderr)。检出需人工核验的 SQL 可实现操作：.query(, sort_values(；不能仅凭理由判为合规。

P7：statsmodels is unavailable; use numpy least squares for a simple regression to see which metrics best predict Overall Score.

[源码](../../../runs/dsv4flash-db-first-full-01/dacomp-014/attempt-01/python/P7.py)；[输出](../../../runs/dsv4flash-db-first-full-01/dacomp-014/attempt-01/python/P7.stdout)；[错误](../../../runs/dsv4flash-db-first-full-01/dacomp-014/attempt-01/python/P7.stderr)。检出需人工核验的 SQL 可实现操作：.query(, sort_values(；不能仅凭理由判为合规。

P8：Analyze the most accessible categories for beginners by looking at categories where small creators (few followers, few videos) succeed, and find categories with high engagement rates. This requires filtering and grouping.

[源码](../../../runs/dsv4flash-db-first-full-01/dacomp-014/attempt-01/python/P8.py)；[输出](../../../runs/dsv4flash-db-first-full-01/dacomp-014/attempt-01/python/P8.stdout)；[错误](../../../runs/dsv4flash-db-first-full-01/dacomp-014/attempt-01/python/P8.stderr)。检出需人工核验的 SQL 可实现操作：groupby(, .query(, sort_values(；不能仅凭理由判为合规。

P9：Analyze common tags/themes in top-ranked and viral videos to identify content themes that drive success. Text analysis is best done in Python.

[源码](../../../runs/dsv4flash-db-first-full-01/dacomp-014/attempt-01/python/P9.py)；[输出](../../../runs/dsv4flash-db-first-full-01/dacomp-014/attempt-01/python/P9.stdout)；[错误](../../../runs/dsv4flash-db-first-full-01/dacomp-014/attempt-01/python/P9.stderr)。检出需人工核验的 SQL 可实现操作：.query(；不能仅凭理由判为合规。

P10：Analyze the 'star' category (where beginners succeed most) and examine the relationship between video count and viral success. Also analyze the title characteristics of viral videos.

[源码](../../../runs/dsv4flash-db-first-full-01/dacomp-014/attempt-01/python/P10.py)；[输出](../../../runs/dsv4flash-db-first-full-01/dacomp-014/attempt-01/python/P10.stdout)；[错误](../../../runs/dsv4flash-db-first-full-01/dacomp-014/attempt-01/python/P10.stderr)。检出需人工核验的 SQL 可实现操作：.query(, sort_values(；不能仅凭理由判为合规。

P11：Create visualizations for the report: 1) Top categories by average views, 2) Engagement rate comparison between viral and non-viral videos, 3) Small creators' success, 4) Correlation heatmap. These are visualizations best done in Python.

[源码](../../../runs/dsv4flash-db-first-full-01/dacomp-014/attempt-01/python/P11.py)；[输出](../../../runs/dsv4flash-db-first-full-01/dacomp-014/attempt-01/python/P11.stdout)；[错误](../../../runs/dsv4flash-db-first-full-01/dacomp-014/attempt-01/python/P11.stderr)。检出需人工核验的 SQL 可实现操作：groupby(, .query(, sort_values(；不能仅凭理由判为合规。

P12：Fix the syntax error in the f-string and re-run the visualization code.

[源码](../../../runs/dsv4flash-db-first-full-01/dacomp-014/attempt-01/python/P12.py)；[输出](../../../runs/dsv4flash-db-first-full-01/dacomp-014/attempt-01/python/P12.stdout)；[错误](../../../runs/dsv4flash-db-first-full-01/dacomp-014/attempt-01/python/P12.stderr)。检出需人工核验的 SQL 可实现操作：groupby(, .query(, sort_values(；不能仅凭理由判为合规。

P13：Analyze which main categories produce viral videos, verify the accessibility of viral success for small creators, and examine the top-ranked videos for common patterns.

[源码](../../../runs/dsv4flash-db-first-full-01/dacomp-014/attempt-01/python/P13.py)；[输出](../../../runs/dsv4flash-db-first-full-01/dacomp-014/attempt-01/python/P13.stdout)；[错误](../../../runs/dsv4flash-db-first-full-01/dacomp-014/attempt-01/python/P13.stderr)。检出需人工核验的 SQL 可实现操作：groupby(, .query(, sort_values(；不能仅凭理由判为合规。

P14：Examine what tags/content themes drive shares (the strongest driver of virality), and identify common patterns in beginner-viral videos to give concrete recommendations.

[源码](../../../runs/dsv4flash-db-first-full-01/dacomp-014/attempt-01/python/P14.py)；[输出](../../../runs/dsv4flash-db-first-full-01/dacomp-014/attempt-01/python/P14.stdout)；[错误](../../../runs/dsv4flash-db-first-full-01/dacomp-014/attempt-01/python/P14.stderr)。检出需人工核验的 SQL 可实现操作：groupby(, .query(, sort_values(；不能仅凭理由判为合规。

P15：Find the actual location of saved figure files.

[源码](../../../runs/dsv4flash-db-first-full-01/dacomp-014/attempt-01/python/P15.py)；[输出](../../../runs/dsv4flash-db-first-full-01/dacomp-014/attempt-01/python/P15.stdout)；[错误](../../../runs/dsv4flash-db-first-full-01/dacomp-014/attempt-01/python/P15.stderr)。自动源码筛查未检出预设迁出信号；这不是全面语义合规证明。

## 优化机会

已验证候选。筛选限于精确 SQL、相同自包含 CTE、相同单表完整过滤、可分解单表聚合；未覆盖任意 Join 等价和一般谓词蕴含。全部候选都是 offline，未测在线预测。

| 候选 | 类型 | 已有结果 | 覆盖 SQL | 后续次数 | 中间行数 | 验证 | 成本 |
| --- | --- | --- | --- | --- | --- | --- | --- |
| C1 | exact-result reuse | True | ["S36", "S40", "S41", "S42", "S43", "S44", "S45", "S46", "S47", "S48", "S49"] | 10 | 5200 | verified | Not benchmarked; correctness alone does not establish net speedup. |
| C2 | aggregate MV | False | ["S4", "S9", "S11", "S12", "S13", "S14", "S15", "S16", "S19", "S23", "S24", "S25", "S27", "S29", "S30", "S31", "S32", "S33", "S50"] | 18 | 5200 | verified | Not benchmarked; correctness alone does not establish net speedup. |


已验证覆盖（含触发查询、候选并集去重）：30/49 条成功数据 SQL。正确性仅针对当前数据库快照；未测性能的候选不能声称已加速。

[完整 build/rewrite 与比较证据](dacomp-014.analysis.json)。

### C2：aggregate MV

Union of grouping keys; decomposable aggregate states; AVG uses SUM and non-NULL COUNT.

原查询 [S4](#s4), [S9](#s9), [S11](#s11), [S12](#s12), [S13](#s13), [S14](#s14), [S15](#s15), [S16](#s16), [S19](#s19), [S23](#s23), [S24](#s24), [S25](#s25), [S27](#s27), [S29](#s29), [S30](#s30), [S31](#s31), [S32](#s32), [S33](#s33), [S50](#s50) → 新增共享状态 C2 → 后续 18 次可复用。该构建点为事后假设，不代表 Agent 当时预知后续。

构建定义：

```sql
SELECT "Video Category" AS __g0, "Main Category" AS __g1, "Creator Gender" AS __g2, CASE WHEN NOT "Bilibili Personal Verification" IS NULL THEN 'Verified' ELSE 'Not Verified' END AS __g3, "Creator Video Count" AS __g4, CASE WHEN "Rank" <= 10 THEN 'Top 10' WHEN "Rank" <= 30 THEN '11-30' WHEN "Rank" <= 50 THEN '31-50' WHEN "Rank" <= 70 THEN '51-70' ELSE '71-100' END AS __g5, SUBSTRING(_id, 1, 8) AS __g6, SUBSTRING(_id, 1, 4) AS __g7, "Creator" AS __g8, CASE WHEN "Creator Followers" < 10000 THEN '1. <10k' WHEN "Creator Followers" < 100000 THEN '2. 10k-100k' WHEN "Creator Followers" < 1000000 THEN '3. 100k-1M' ELSE '4. >1M' END AS __g9, CASE WHEN "Creator Video Count" = 100 THEN '100 (full)' WHEN "Creator Video Count" < 10 THEN '1-9' WHEN "Creator Video Count" < 50 THEN '10-49' ELSE '50-99' END AS __g10, COUNT(*) AS __a0, MIN("Rank") AS __a1, MAX("Rank") AS __a2, MIN("Views") AS __a3, SUM("Views") AS __a4_sum, COUNT("Views") AS __a4_n, MAX("Views") AS __a5, MIN("Likes") AS __a6, SUM("Likes") AS __a7_sum, COUNT("Likes") AS __a7_n, MAX("Likes") AS __a8, MIN("Coins") AS __a9, SUM("Coins") AS __a10_sum, COUNT("Coins") AS __a10_n, MAX("Coins") AS __a11, MIN("Favorites") AS __a12, SUM("Favorites") AS __a13_sum, COUNT("Favorites") AS __a13_n, MAX("Favorites") AS __a14, MIN("Shares") AS __a15, SUM("Shares") AS __a16_sum, COUNT("Shares") AS __a16_n, MAX("Shares") AS __a17, MIN("Comments") AS __a18, SUM("Comments") AS __a19_sum, COUNT("Comments") AS __a19_n, MAX("Comments") AS __a20, MIN("Danmaku Count") AS __a21, SUM("Danmaku Count") AS __a22_sum, COUNT("Danmaku Count") AS __a22_n, MAX("Danmaku Count") AS __a23, SUM("Overall Score") AS __a24_sum, COUNT("Overall Score") AS __a24_n, SUM("Rank") AS __a25_sum, COUNT("Rank") AS __a25_n, SUM("Creator Followers") AS __a26_sum, COUNT("Creator Followers") AS __a26_n, SUM("Creator Video Count") AS __a27_sum, COUNT("Creator Video Count") AS __a27_n, SUM(CASE WHEN "Rank" <= 10 THEN 1 ELSE 0 END) AS __a28, SUM(CASE WHEN "Rank" <= 30 THEN 1 ELSE 0 END) AS __a29, SUM(CASE WHEN "Views" >= 5000000 THEN 1 ELSE 0 END) AS __a30, SUM(CASE WHEN "Views" >= 2000000 THEN 1 ELSE 0 END) AS __a31, SUM(CASE WHEN "Views" >= 1000000 THEN 1 ELSE 0 END) AS __a32 FROM "sheet1"  GROUP BY "Video Category", "Main Category", "Creator Gender", CASE WHEN NOT "Bilibili Personal Verification" IS NULL THEN 'Verified' ELSE 'Not Verified' END, "Creator Video Count", CASE WHEN "Rank" <= 10 THEN 'Top 10' WHEN "Rank" <= 30 THEN '11-30' WHEN "Rank" <= 50 THEN '31-50' WHEN "Rank" <= 70 THEN '51-70' ELSE '71-100' END, SUBSTRING(_id, 1, 8), SUBSTRING(_id, 1, 4), "Creator", CASE WHEN "Creator Followers" < 10000 THEN '1. <10k' WHEN "Creator Followers" < 100000 THEN '2. 10k-100k' WHEN "Creator Followers" < 1000000 THEN '3. 100k-1M' ELSE '4. >1M' END, CASE WHEN "Creator Video Count" = 100 THEN '100 (full)' WHEN "Creator Video Count" < 10 THEN '1-9' WHEN "Creator Video Count" < 50 THEN '10-49' ELSE '50-99' END
```

受益查询 S4 的改写示例：

```sql
SELECT SUM(__a0) AS total_rows FROM temp.reuse_candidate
```

| 原 SQL | 列名一致 | 结果一致 | 比较方法 |
| --- | --- | --- | --- |
| S4 | True | True | exact_multiset |
| S9 | True | True | exact_multiset |
| S11 | True | True | exact_multiset |
| S12 | True | True | ordered_numeric_tolerance |
| S13 | True | True | ordered_numeric_tolerance |
| S14 | True | True | exact_multiset |
| S15 | True | True | exact_multiset |
| S16 | True | True | ordered_numeric_tolerance |
| S19 | True | True | ordered_numeric_tolerance |
| S23 | True | True | ordered_numeric_tolerance |
| S24 | True | True | ordered_numeric_tolerance |
| S25 | True | True | ordered_numeric_tolerance |
| S27 | True | True | ordered_numeric_tolerance |
| S29 | True | True | ordered_numeric_tolerance |
| S30 | True | True | ordered_numeric_tolerance |
| S31 | True | True | ordered_numeric_tolerance |
| S32 | True | True | ordered_numeric_tolerance |
| S33 | True | True | exact_multiset |
| S50 | True | True | exact_multiset |


验证状态：verified；成本结论：Not benchmarked; correctness alone does not establish net speedup.

### C1：exact-result reuse

Identical normalized SQL and parameters; archive equality checked.

原查询 [S36](#s36), [S40](#s40), [S41](#s41), [S42](#s42), [S43](#s43), [S44](#s44), [S45](#s45), [S46](#s46), [S47](#s47), [S48](#s48), [S49](#s49) → 保留前序结果 S36 → 后续 10 次可复用。该构建点为事后假设，不代表 Agent 当时预知后续。

| 原 SQL | 列名一致 | 结果一致 | 比较方法 |
| --- | --- | --- | --- |
| S40 | True | True | exact_multiset |
| S41 | True | True | exact_multiset |
| S42 | True | True | exact_multiset |
| S43 | True | True | exact_multiset |
| S44 | True | True | exact_multiset |
| S45 | True | True | exact_multiset |
| S46 | True | True | exact_multiset |
| S47 | True | True | exact_multiset |
| S48 | True | True | exact_multiset |
| S49 | True | True | exact_multiset |


验证状态：verified；成本结论：Not benchmarked; correctness alone does not establish net speedup.

结果依赖：自动记录 SQL→Python 的接口父调用，以及源码中引用归档文件的消费者；字面值相同不认定因果。模型方向选择需要人工读取消息，尚未做全面因果标注。

[原始报告](../../../runs/dsv4flash-db-first-full-01/dacomp-014/attempt-01/answer.md)；[统一消息](../../../runs/dsv4flash-db-first-full-01/dacomp-014/attempt-01/messages.jsonl)；[原始 OpenCode 事件](../../../runs/dsv4flash-db-first-full-01/dacomp-014/attempt-01/opencode.jsonl)；[SQL 引擎日志](../../../runs/dsv4flash-db-first-full-01/dacomp-014/attempt-01/sql_journal.jsonl)。

[可读报告（本地图片链接规范化）](../answers/dacomp-014.md)。原始回答保留，分析结论未改写。

## S1

类别 `connection_setup`；来源 `connection`；调用 `a852ece6ee664d6d9255115aa8885fa1`；状态 `success`。

```sql
PRAGMA query_only=ON
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-014/attempt-01/sql/S1.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-014/attempt-01/sql/S1.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-014/attempt-01/results/S1.rows.jsonl)；完整：True；SHA256：`e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`。

## S2

类别 `metadata`；来源 `list_db`；调用 `a852ece6ee664d6d9255115aa8885fa1`；状态 `success`。

```sql
SELECT name,sql FROM sqlite_master WHERE type='table' ORDER BY name
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-014/attempt-01/sql/S2.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-014/attempt-01/sql/S2.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-014/attempt-01/results/S2.rows.jsonl)；完整：True；SHA256：`e87e461a1ea469876f34e52a2e7cd837c71da70caa78cf559b43c8c89af1a25f`。

## S3

类别 `data`；来源 `query_db`；调用 `cf3baac1a27f40b8bded0de8c171a6b6`；状态 `success`。

```sql
SELECT * FROM sheet1 LIMIT 20
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-014/attempt-01/sql/S3.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-014/attempt-01/sql/S3.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-014/attempt-01/results/S3.rows.jsonl)；完整：True；SHA256：`0e3613959a99e9be69325917067919f2b252e3e3bfd2f88e6a7deeaa3e2e9cc4`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "sheet1", "kind": "base", "block": null, "base_tables": ["sheet1"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |


## S4

类别 `data`；来源 `query_db`；调用 `02c700d92ac54168850733f3e7df1df3`；状态 `success`。

```sql
SELECT COUNT(*) as total_rows FROM sheet1
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-014/attempt-01/sql/S4.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-014/attempt-01/sql/S4.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-014/attempt-01/results/S4.rows.jsonl)；完整：True；SHA256：`ba5f09df141b82faad10adef3616f1a722b6ba61014c4a2e710a5b90355b8de6`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "sheet1", "kind": "base", "block": null, "base_tables": ["sheet1"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |


## S5

类别 `data`；来源 `query_db`；调用 `a746a74e240342719cf3530588e0960a`；状态 `success`。

```sql
SELECT DISTINCT "Video Category" FROM sheet1 ORDER BY "Video Category"
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-014/attempt-01/sql/S5.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-014/attempt-01/sql/S5.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-014/attempt-01/results/S5.rows.jsonl)；完整：True；SHA256：`d5ec94e8fef8053cb8c190a546e6614e6864791120fe486832d017be7fb0d7b2`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "sheet1", "kind": "base", "block": null, "base_tables": ["sheet1"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |


## S6

类别 `data`；来源 `query_db`；调用 `5472138645dd403fa61aca33b5d26742`；状态 `success`。

```sql
SELECT DISTINCT "Main Category" FROM sheet1 ORDER BY "Main Category"
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-014/attempt-01/sql/S6.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-014/attempt-01/sql/S6.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-014/attempt-01/results/S6.rows.jsonl)；完整：True；SHA256：`255d6b5bd1dc3afe2076ee2abb3b24fb278f025a6fbaae9e1f750374b55a248a`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "sheet1", "kind": "base", "block": null, "base_tables": ["sheet1"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |


## S7

类别 `data`；来源 `query_db`；调用 `f3ee7158a12f423eaaecd28a42fb63d9`；状态 `success`。

```sql
SELECT DISTINCT "Creator Gender" FROM sheet1 ORDER BY "Creator Gender"
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-014/attempt-01/sql/S7.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-014/attempt-01/sql/S7.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-014/attempt-01/results/S7.rows.jsonl)；完整：True；SHA256：`bdbd4eeface9f7ebdbbe778c7b509adc7f2dc0c67720a99dd44851e73d245346`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "sheet1", "kind": "base", "block": null, "base_tables": ["sheet1"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |


## S8

类别 `data`；来源 `query_db`；调用 `57716a526ff9420592e4b2f449d25160`；状态 `success`。

```sql
SELECT DISTINCT "Bilibili Personal Verification" FROM sheet1 ORDER BY "Bilibili Personal Verification"
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-014/attempt-01/sql/S8.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-014/attempt-01/sql/S8.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-014/attempt-01/results/S8.rows.jsonl)；完整：True；SHA256：`baba5439904dd33d09cd94d1e49d30077a64332aff776e39aee495ceca710c7b`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "sheet1", "kind": "base", "block": null, "base_tables": ["sheet1"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |


## S9

类别 `data`；来源 `query_db`；调用 `1bd5acf845a14569b654e133457e0d4e`；状态 `success`。

```sql
SELECT MIN("Rank") as min_rank, MAX("Rank") as max_rank FROM sheet1
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-014/attempt-01/sql/S9.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-014/attempt-01/sql/S9.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-014/attempt-01/results/S9.rows.jsonl)；完整：True；SHA256：`42da5fa50f17028aab9ced4798dc84a07ff8555892850714c98c6c16a17bdc00`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "sheet1", "kind": "base", "block": null, "base_tables": ["sheet1"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | MIN("Rank") | [{"table": "sheet1", "column": "Rank"}] | [] | False |
| B1 | MAX("Rank") | [{"table": "sheet1", "column": "Rank"}] | [] | False |


## S10

类别 `data`；来源 `query_db`；调用 `85bdf5f6e0424d86a6fca627d85a1965`；状态 `success`。

```sql
SELECT DISTINCT _id FROM sheet1 LIMIT 10
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-014/attempt-01/sql/S10.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-014/attempt-01/sql/S10.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-014/attempt-01/results/S10.rows.jsonl)；完整：True；SHA256：`922a0d32e649ed59e192149b5de6453bb99fdb4f6270d5191b4e3f6bf0cb77ae`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "sheet1", "kind": "base", "block": null, "base_tables": ["sheet1"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |


## S11

类别 `data`；来源 `query_db`；调用 `7ef0783ff6fa44f6987b059830c9d72d`；状态 `success`。

```sql
SELECT 
  MIN("Views") as min_views, 
  AVG("Views") as avg_views, 
  MAX("Views") as max_views,
  MIN("Likes") as min_likes,
  AVG("Likes") as avg_likes,
  MAX("Likes") as max_likes,
  MIN("Coins") as min_coins,
  AVG("Coins") as avg_coins,
  MAX("Coins") as max_coins,
  MIN("Favorites") as min_fav,
  AVG("Favorites") as avg_fav,
  MAX("Favorites") as max_fav,
  MIN("Shares") as min_shares,
  AVG("Shares") as avg_shares,
  MAX("Shares") as max_shares,
  MIN("Comments") as min_comments,
  AVG("Comments") as avg_comments,
  MAX("Comments") as max_comments,
  MIN("Danmaku Count") as min_danmaku,
  AVG("Danmaku Count") as avg_danmaku,
  MAX("Danmaku Count") as max_danmaku
FROM sheet1
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-014/attempt-01/sql/S11.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-014/attempt-01/sql/S11.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-014/attempt-01/results/S11.rows.jsonl)；完整：True；SHA256：`c5e1f47cf7570ce4da7be1415c50da28c83226cb535e5a1f5a8078653e8fe482`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "sheet1", "kind": "base", "block": null, "base_tables": ["sheet1"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | MIN("Views") | [{"table": "sheet1", "column": "Views"}] | [] | False |
| B1 | AVG("Views") | [{"table": "sheet1", "column": "Views"}] | [] | False |
| B1 | MAX("Views") | [{"table": "sheet1", "column": "Views"}] | [] | False |
| B1 | MIN("Likes") | [{"table": "sheet1", "column": "Likes"}] | [] | False |
| B1 | AVG("Likes") | [{"table": "sheet1", "column": "Likes"}] | [] | False |
| B1 | MAX("Likes") | [{"table": "sheet1", "column": "Likes"}] | [] | False |
| B1 | MIN("Coins") | [{"table": "sheet1", "column": "Coins"}] | [] | False |
| B1 | AVG("Coins") | [{"table": "sheet1", "column": "Coins"}] | [] | False |
| B1 | MAX("Coins") | [{"table": "sheet1", "column": "Coins"}] | [] | False |
| B1 | MIN("Favorites") | [{"table": "sheet1", "column": "Favorites"}] | [] | False |
| B1 | AVG("Favorites") | [{"table": "sheet1", "column": "Favorites"}] | [] | False |
| B1 | MAX("Favorites") | [{"table": "sheet1", "column": "Favorites"}] | [] | False |
| B1 | MIN("Shares") | [{"table": "sheet1", "column": "Shares"}] | [] | False |
| B1 | AVG("Shares") | [{"table": "sheet1", "column": "Shares"}] | [] | False |
| B1 | MAX("Shares") | [{"table": "sheet1", "column": "Shares"}] | [] | False |
| B1 | MIN("Comments") | [{"table": "sheet1", "column": "Comments"}] | [] | False |
| B1 | AVG("Comments") | [{"table": "sheet1", "column": "Comments"}] | [] | False |
| B1 | MAX("Comments") | [{"table": "sheet1", "column": "Comments"}] | [] | False |
| B1 | MIN("Danmaku Count") | [{"table": "sheet1", "column": "Danmaku Count"}] | [] | False |
| B1 | AVG("Danmaku Count") | [{"table": "sheet1", "column": "Danmaku Count"}] | [] | False |
| B1 | MAX("Danmaku Count") | [{"table": "sheet1", "column": "Danmaku Count"}] | [] | False |


## S12

类别 `data`；来源 `query_db`；调用 `27f5664b4c764b9592ca861bdb3ee6bd`；状态 `success`。

```sql
SELECT 
  "Video Category",
  COUNT(*) as count,
  ROUND(AVG("Views")) as avg_views,
  ROUND(AVG("Likes")) as avg_likes,
  ROUND(AVG("Coins")) as avg_coins,
  ROUND(AVG("Favorites")) as avg_favorites,
  ROUND(AVG("Shares")) as avg_shares,
  ROUND(AVG("Comments")) as avg_comments,
  ROUND(AVG("Danmaku Count")) as avg_danmaku,
  ROUND(AVG("Overall Score")) as avg_score
FROM sheet1
GROUP BY "Video Category"
ORDER BY avg_views DESC
LIMIT 20
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-014/attempt-01/sql/S12.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-014/attempt-01/sql/S12.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-014/attempt-01/results/S12.rows.jsonl)；完整：True；SHA256：`3ff622571cff5e55896125a9303c749c688ed4b4865d663c6b12036fac5f26e2`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "sheet1", "kind": "base", "block": null, "base_tables": ["sheet1"]}] | [] | ["\"Video Category\""] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |
| B1 | AVG("Views") | [{"table": "sheet1", "column": "Views"}] | [] | False |
| B1 | AVG("Likes") | [{"table": "sheet1", "column": "Likes"}] | [] | False |
| B1 | AVG("Coins") | [{"table": "sheet1", "column": "Coins"}] | [] | False |
| B1 | AVG("Favorites") | [{"table": "sheet1", "column": "Favorites"}] | [] | False |
| B1 | AVG("Shares") | [{"table": "sheet1", "column": "Shares"}] | [] | False |
| B1 | AVG("Comments") | [{"table": "sheet1", "column": "Comments"}] | [] | False |
| B1 | AVG("Danmaku Count") | [{"table": "sheet1", "column": "Danmaku Count"}] | [] | False |
| B1 | AVG("Overall Score") | [{"table": "sheet1", "column": "Overall Score"}] | [] | False |


## S13

类别 `data`；来源 `query_db`；调用 `db375c73083f4cc69d99bb78604a4ece`；状态 `success`。

```sql
SELECT 
  "Main Category",
  COUNT(*) as count,
  ROUND(AVG("Views")) as avg_views,
  ROUND(AVG("Likes")) as avg_likes,
  ROUND(AVG("Coins")) as avg_coins,
  ROUND(AVG("Favorites")) as avg_favorites,
  ROUND(AVG("Shares")) as avg_shares,
  ROUND(AVG("Overall Score")) as avg_score,
  ROUND(AVG("Rank")) as avg_rank
FROM sheet1
GROUP BY "Main Category"
ORDER BY avg_views DESC
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-014/attempt-01/sql/S13.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-014/attempt-01/sql/S13.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-014/attempt-01/results/S13.rows.jsonl)；完整：True；SHA256：`fef801b08d571c6b88e40c1f525ddd8335d72482dcaf1c1c04c3a567a1a9dcd5`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "sheet1", "kind": "base", "block": null, "base_tables": ["sheet1"]}] | [] | ["\"Main Category\""] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |
| B1 | AVG("Views") | [{"table": "sheet1", "column": "Views"}] | [] | False |
| B1 | AVG("Likes") | [{"table": "sheet1", "column": "Likes"}] | [] | False |
| B1 | AVG("Coins") | [{"table": "sheet1", "column": "Coins"}] | [] | False |
| B1 | AVG("Favorites") | [{"table": "sheet1", "column": "Favorites"}] | [] | False |
| B1 | AVG("Shares") | [{"table": "sheet1", "column": "Shares"}] | [] | False |
| B1 | AVG("Overall Score") | [{"table": "sheet1", "column": "Overall Score"}] | [] | False |
| B1 | AVG("Rank") | [{"table": "sheet1", "column": "Rank"}] | [] | False |


## S14

类别 `data`；来源 `query_db`；调用 `5088e877ddc74217826304fe22cd031a`；状态 `success`。

```sql
SELECT 
  "Creator Gender",
  COUNT(*) as count,
  ROUND(AVG("Views")) as avg_views,
  ROUND(AVG("Likes")) as avg_likes,
  ROUND(AVG("Coins")) as avg_coins,
  ROUND(AVG("Favorites")) as avg_favorites,
  ROUND(AVG("Shares")) as avg_shares,
  ROUND(AVG("Overall Score")) as avg_score,
  ROUND(AVG("Creator Followers")) as avg_followers,
  ROUND(AVG("Creator Video Count")) as avg_video_count
FROM sheet1
GROUP BY "Creator Gender"
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-014/attempt-01/sql/S14.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-014/attempt-01/sql/S14.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-014/attempt-01/results/S14.rows.jsonl)；完整：True；SHA256：`7d9406e69fba8fb8d26744cd2f32173579a76de0a2b19e071eec0bb103d0f2ef`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "sheet1", "kind": "base", "block": null, "base_tables": ["sheet1"]}] | [] | ["\"Creator Gender\""] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |
| B1 | AVG("Views") | [{"table": "sheet1", "column": "Views"}] | [] | False |
| B1 | AVG("Likes") | [{"table": "sheet1", "column": "Likes"}] | [] | False |
| B1 | AVG("Coins") | [{"table": "sheet1", "column": "Coins"}] | [] | False |
| B1 | AVG("Favorites") | [{"table": "sheet1", "column": "Favorites"}] | [] | False |
| B1 | AVG("Shares") | [{"table": "sheet1", "column": "Shares"}] | [] | False |
| B1 | AVG("Overall Score") | [{"table": "sheet1", "column": "Overall Score"}] | [] | False |
| B1 | AVG("Creator Followers") | [{"table": "sheet1", "column": "Creator Followers"}] | [] | False |
| B1 | AVG("Creator Video Count") | [{"table": "sheet1", "column": "Creator Video Count"}] | [] | False |


## S15

类别 `data`；来源 `query_db`；调用 `38637d2ad68a4107addfcc0af75fe14f`；状态 `success`。

```sql
SELECT 
  CASE WHEN "Bilibili Personal Verification" IS NOT NULL THEN 'Verified' ELSE 'Not Verified' END as verification_status,
  COUNT(*) as count,
  ROUND(AVG("Views")) as avg_views,
  ROUND(AVG("Likes")) as avg_likes,
  ROUND(AVG("Coins")) as avg_coins,
  ROUND(AVG("Favorites")) as avg_favorites,
  ROUND(AVG("Shares")) as avg_shares,
  ROUND(AVG("Overall Score")) as avg_score,
  ROUND(AVG("Creator Followers")) as avg_followers
FROM sheet1
GROUP BY verification_status
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-014/attempt-01/sql/S15.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-014/attempt-01/sql/S15.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-014/attempt-01/results/S15.rows.jsonl)；完整：True；SHA256：`39220e7c19958fb651f612392bc735c4c211322d5744641a9e973f95be94557c`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "sheet1", "kind": "base", "block": null, "base_tables": ["sheet1"]}] | [] | ["CASE WHEN NOT \"Bilibili Personal Verification\" IS NULL THEN 'Verified' ELSE 'Not Verified' END"] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |
| B1 | AVG("Views") | [{"table": "sheet1", "column": "Views"}] | [] | False |
| B1 | AVG("Likes") | [{"table": "sheet1", "column": "Likes"}] | [] | False |
| B1 | AVG("Coins") | [{"table": "sheet1", "column": "Coins"}] | [] | False |
| B1 | AVG("Favorites") | [{"table": "sheet1", "column": "Favorites"}] | [] | False |
| B1 | AVG("Shares") | [{"table": "sheet1", "column": "Shares"}] | [] | False |
| B1 | AVG("Overall Score") | [{"table": "sheet1", "column": "Overall Score"}] | [] | False |
| B1 | AVG("Creator Followers") | [{"table": "sheet1", "column": "Creator Followers"}] | [] | False |


## S16

类别 `data`；来源 `query_db`；调用 `523c83efa1514ab883e339398e6ec289`；状态 `success`。

```sql
SELECT 
  "Creator Video Count",
  COUNT(*) as count,
  ROUND(AVG("Views")) as avg_views,
  ROUND(AVG("Likes")) as avg_likes,
  ROUND(AVG("Coins")) as avg_coins,
  ROUND(AVG("Favorites")) as avg_favorites,
  ROUND(AVG("Shares")) as avg_shares
FROM sheet1
GROUP BY "Creator Video Count"
ORDER BY "Creator Video Count" DESC
LIMIT 20
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-014/attempt-01/sql/S16.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-014/attempt-01/sql/S16.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-014/attempt-01/results/S16.rows.jsonl)；完整：True；SHA256：`6b889a623445ccb74f0a6f574314271268ac5b4324ab646a1ab5c4b31aced940`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "sheet1", "kind": "base", "block": null, "base_tables": ["sheet1"]}] | [] | ["\"Creator Video Count\""] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |
| B1 | AVG("Views") | [{"table": "sheet1", "column": "Views"}] | [] | False |
| B1 | AVG("Likes") | [{"table": "sheet1", "column": "Likes"}] | [] | False |
| B1 | AVG("Coins") | [{"table": "sheet1", "column": "Coins"}] | [] | False |
| B1 | AVG("Favorites") | [{"table": "sheet1", "column": "Favorites"}] | [] | False |
| B1 | AVG("Shares") | [{"table": "sheet1", "column": "Shares"}] | [] | False |


## S17

类别 `data`；来源 `query_db`；调用 `87edb407cd13473e91fe4d76c7a76973`；状态 `success`。

```sql
SELECT 
  "Video Category",
  COUNT(*) as count,
  ROUND(AVG("Views")) as avg_views,
  ROUND(AVG("Likes")) as avg_likes,
  ROUND(AVG("Coins")) as avg_coins,
  ROUND(AVG("Favorites")) as avg_favorites,
  ROUND(AVG("Shares")) as avg_shares,
  ROUND(AVG("Comments")) as avg_comments,
  ROUND(AVG("Danmaku Count")) as avg_danmaku,
  ROUND(AVG("Overall Score")) as avg_score,
  ROUND(1.0*AVG("Likes")/AVG("Views")*100, 2) as like_rate,
  ROUND(1.0*AVG("Coins")/AVG("Views")*100, 2) as coin_rate,
  ROUND(1.0*AVG("Favorites")/AVG("Views")*100, 2) as fav_rate,
  ROUND(1.0*AVG("Shares")/AVG("Views")*100, 2) as share_rate
FROM sheet1
GROUP BY "Video Category"
HAVING count >= 10
ORDER BY avg_views DESC
LIMIT 20
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-014/attempt-01/sql/S17.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-014/attempt-01/sql/S17.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-014/attempt-01/results/S17.rows.jsonl)；完整：True；SHA256：`11d69ea2bbc47f141923fa025d7a1e24c6ccf2b2eb27b7d8c761dd3dfe6f4742`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "sheet1", "kind": "base", "block": null, "base_tables": ["sheet1"]}] | [] | ["\"Video Category\""] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |
| B1 | AVG("Views") | [{"table": "sheet1", "column": "Views"}] | [] | False |
| B1 | AVG("Likes") | [{"table": "sheet1", "column": "Likes"}] | [] | False |
| B1 | AVG("Coins") | [{"table": "sheet1", "column": "Coins"}] | [] | False |
| B1 | AVG("Favorites") | [{"table": "sheet1", "column": "Favorites"}] | [] | False |
| B1 | AVG("Shares") | [{"table": "sheet1", "column": "Shares"}] | [] | False |
| B1 | AVG("Comments") | [{"table": "sheet1", "column": "Comments"}] | [] | False |
| B1 | AVG("Danmaku Count") | [{"table": "sheet1", "column": "Danmaku Count"}] | [] | False |
| B1 | AVG("Overall Score") | [{"table": "sheet1", "column": "Overall Score"}] | [] | False |
| B1 | AVG("Views") | [{"table": "sheet1", "column": "Views"}] | [] | False |
| B1 | AVG("Views") | [{"table": "sheet1", "column": "Views"}] | [] | False |
| B1 | AVG("Views") | [{"table": "sheet1", "column": "Views"}] | [] | False |
| B1 | AVG("Views") | [{"table": "sheet1", "column": "Views"}] | [] | False |
| B1 | AVG("Likes") | [{"table": "sheet1", "column": "Likes"}] | [] | False |
| B1 | AVG("Coins") | [{"table": "sheet1", "column": "Coins"}] | [] | False |
| B1 | AVG("Favorites") | [{"table": "sheet1", "column": "Favorites"}] | [] | False |
| B1 | AVG("Shares") | [{"table": "sheet1", "column": "Shares"}] | [] | False |


## S18

类别 `data`；来源 `query_db`；调用 `d79520a4a0ec40d59efc819ff2e0f741`；状态 `success`。

```sql
SELECT 
  "Video Category",
  COUNT(*) as count,
  ROUND(AVG("Views")) as avg_views,
  ROUND(1.0*AVG("Likes")/AVG("Views")*100, 2) as like_rate,
  ROUND(1.0*AVG("Coins")/AVG("Views")*100, 2) as coin_rate,
  ROUND(1.0*AVG("Favorites")/AVG("Views")*100, 2) as fav_rate,
  ROUND(1.0*AVG("Shares")/AVG("Views")*100, 2) as share_rate,
  ROUND(1.0*AVG("Comments")/AVG("Views")*100, 2) as comment_rate,
  ROUND(1.0*AVG("Danmaku Count")/AVG("Views")*100, 2) as danmaku_rate
FROM sheet1
GROUP BY "Video Category"
HAVING count >= 10
ORDER BY like_rate DESC
LIMIT 20
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-014/attempt-01/sql/S18.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-014/attempt-01/sql/S18.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-014/attempt-01/results/S18.rows.jsonl)；完整：True；SHA256：`e7a7331c20edf0a7bdd36b029c0a6e3f03be01ac15922eed8512b5a82cc15046`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "sheet1", "kind": "base", "block": null, "base_tables": ["sheet1"]}] | [] | ["\"Video Category\""] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |
| B1 | AVG("Views") | [{"table": "sheet1", "column": "Views"}] | [] | False |
| B1 | AVG("Views") | [{"table": "sheet1", "column": "Views"}] | [] | False |
| B1 | AVG("Views") | [{"table": "sheet1", "column": "Views"}] | [] | False |
| B1 | AVG("Views") | [{"table": "sheet1", "column": "Views"}] | [] | False |
| B1 | AVG("Views") | [{"table": "sheet1", "column": "Views"}] | [] | False |
| B1 | AVG("Views") | [{"table": "sheet1", "column": "Views"}] | [] | False |
| B1 | AVG("Views") | [{"table": "sheet1", "column": "Views"}] | [] | False |
| B1 | AVG("Likes") | [{"table": "sheet1", "column": "Likes"}] | [] | False |
| B1 | AVG("Coins") | [{"table": "sheet1", "column": "Coins"}] | [] | False |
| B1 | AVG("Favorites") | [{"table": "sheet1", "column": "Favorites"}] | [] | False |
| B1 | AVG("Shares") | [{"table": "sheet1", "column": "Shares"}] | [] | False |
| B1 | AVG("Comments") | [{"table": "sheet1", "column": "Comments"}] | [] | False |
| B1 | AVG("Danmaku Count") | [{"table": "sheet1", "column": "Danmaku Count"}] | [] | False |


## S19

类别 `data`；来源 `query_db`；调用 `83f8839548754e6fb8a09b60bcce764e`；状态 `success`。

```sql
SELECT 
  CASE WHEN "Rank" <= 10 THEN 'Top 10'
       WHEN "Rank" <= 30 THEN '11-30'
       WHEN "Rank" <= 50 THEN '31-50'
       WHEN "Rank" <= 70 THEN '51-70'
       ELSE '71-100' END as rank_band,
  "Main Category",
  COUNT(*) as count
FROM sheet1
GROUP BY rank_band, "Main Category"
ORDER BY rank_band, count DESC
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-014/attempt-01/sql/S19.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-014/attempt-01/sql/S19.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-014/attempt-01/results/S19.rows.jsonl)；完整：True；SHA256：`59b4725216bc3e81f9bdf81858700f6b4d6782e9b853e181bbb7400d16221d81`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "sheet1", "kind": "base", "block": null, "base_tables": ["sheet1"]}] | [] | ["CASE WHEN \"Rank\" <= 10 THEN 'Top 10' WHEN \"Rank\" <= 30 THEN '11-30' WHEN \"Rank\" <= 50 THEN '31-50' WHEN \"Rank\" <= 70 THEN '51-70' ELSE '71-100' END", "\"Main Category\""] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |


## S20

类别 `data`；来源 `query_db`；调用 `ac1f880c52264c20b85e3dc9581624b8`；状态 `success`。

```sql
SELECT "Title", "Creator", "Views", "Likes", "Coins", "Shares", "Favorites", "Danmaku Count", "Comments", "Overall Score", "Video Category", "Creator Followers"
FROM sheet1
ORDER BY "Views" DESC
LIMIT 20
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-014/attempt-01/sql/S20.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-014/attempt-01/sql/S20.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-014/attempt-01/results/S20.rows.jsonl)；完整：True；SHA256：`3a2990d10a6fda4eead47ca48a127bef7eb0bfae70190e381434eee5b1cd5d08`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "sheet1", "kind": "base", "block": null, "base_tables": ["sheet1"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |


## S21

类别 `data`；来源 `query_db`；调用 `d6fcf9954dc44b8c926876c379586faf`；状态 `success`。

```sql
SELECT 
  ROUND(AVG("Overall Score")) as avg_overall_score,
  ROUND(AVG("Views")) as avg_views,
  ROUND(AVG("Likes")) as avg_likes,
  ROUND(AVG("Coins")) as avg_coins,
  ROUND(AVG("Favorites")) as avg_favorites,
  ROUND(AVG("Shares")) as avg_shares,
  ROUND(AVG("Danmaku Count")) as avg_danmaku,
  ROUND(AVG("Comments")) as avg_comments,
  ROUND(AVG("Creator Followers")) as avg_followers,
  ROUND(AVG("Creator Total Views")) as avg_creator_views,
  ROUND(AVG("Creator Total Likes")) as avg_creator_likes,
  ROUND(AVG("Creator Video Count")) as avg_creator_videos
FROM sheet1
WHERE "Rank" <= 10
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-014/attempt-01/sql/S21.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-014/attempt-01/sql/S21.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-014/attempt-01/results/S21.rows.jsonl)；完整：True；SHA256：`c0ff3fdffd378cf37b885f3b38e7bd3a97a17e508e03c024ac5f5f71b06f349f`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "sheet1", "kind": "base", "block": null, "base_tables": ["sheet1"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | AVG("Overall Score") | [{"table": "sheet1", "column": "Overall Score"}] | [] | False |
| B1 | AVG("Views") | [{"table": "sheet1", "column": "Views"}] | [] | False |
| B1 | AVG("Likes") | [{"table": "sheet1", "column": "Likes"}] | [] | False |
| B1 | AVG("Coins") | [{"table": "sheet1", "column": "Coins"}] | [] | False |
| B1 | AVG("Favorites") | [{"table": "sheet1", "column": "Favorites"}] | [] | False |
| B1 | AVG("Shares") | [{"table": "sheet1", "column": "Shares"}] | [] | False |
| B1 | AVG("Danmaku Count") | [{"table": "sheet1", "column": "Danmaku Count"}] | [] | False |
| B1 | AVG("Comments") | [{"table": "sheet1", "column": "Comments"}] | [] | False |
| B1 | AVG("Creator Followers") | [{"table": "sheet1", "column": "Creator Followers"}] | [] | False |
| B1 | AVG("Creator Total Views") | [{"table": "sheet1", "column": "Creator Total Views"}] | [] | False |
| B1 | AVG("Creator Total Likes") | [{"table": "sheet1", "column": "Creator Total Likes"}] | [] | False |
| B1 | AVG("Creator Video Count") | [{"table": "sheet1", "column": "Creator Video Count"}] | [] | False |


## S22

类别 `data`；来源 `query_db`；调用 `9444ba16f5ff4efb922f21038058b53a`；状态 `success`。

```sql
SELECT 
  ROUND(AVG("Overall Score")) as avg_overall_score,
  ROUND(AVG("Views")) as avg_views,
  ROUND(AVG("Likes")) as avg_likes,
  ROUND(AVG("Coins")) as avg_coins,
  ROUND(AVG("Favorites")) as avg_favorites,
  ROUND(AVG("Shares")) as avg_shares,
  ROUND(AVG("Danmaku Count")) as avg_danmaku,
  ROUND(AVG("Comments")) as avg_comments,
  ROUND(AVG("Creator Followers")) as avg_followers,
  ROUND(AVG("Creator Total Views")) as avg_creator_views,
  ROUND(AVG("Creator Total Likes")) as avg_creator_likes,
  ROUND(AVG("Creator Video Count")) as avg_creator_videos
FROM sheet1
WHERE "Rank" >= 90
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-014/attempt-01/sql/S22.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-014/attempt-01/sql/S22.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-014/attempt-01/results/S22.rows.jsonl)；完整：True；SHA256：`3fbba256068ca24f2747294d26f17278965db6597b42ab6e260f259dd064108c`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "sheet1", "kind": "base", "block": null, "base_tables": ["sheet1"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | AVG("Overall Score") | [{"table": "sheet1", "column": "Overall Score"}] | [] | False |
| B1 | AVG("Views") | [{"table": "sheet1", "column": "Views"}] | [] | False |
| B1 | AVG("Likes") | [{"table": "sheet1", "column": "Likes"}] | [] | False |
| B1 | AVG("Coins") | [{"table": "sheet1", "column": "Coins"}] | [] | False |
| B1 | AVG("Favorites") | [{"table": "sheet1", "column": "Favorites"}] | [] | False |
| B1 | AVG("Shares") | [{"table": "sheet1", "column": "Shares"}] | [] | False |
| B1 | AVG("Danmaku Count") | [{"table": "sheet1", "column": "Danmaku Count"}] | [] | False |
| B1 | AVG("Comments") | [{"table": "sheet1", "column": "Comments"}] | [] | False |
| B1 | AVG("Creator Followers") | [{"table": "sheet1", "column": "Creator Followers"}] | [] | False |
| B1 | AVG("Creator Total Views") | [{"table": "sheet1", "column": "Creator Total Views"}] | [] | False |
| B1 | AVG("Creator Total Likes") | [{"table": "sheet1", "column": "Creator Total Likes"}] | [] | False |
| B1 | AVG("Creator Video Count") | [{"table": "sheet1", "column": "Creator Video Count"}] | [] | False |


## S23

类别 `data`；来源 `query_db`；调用 `a14e8ec64b44409690ce0b5dc9f8fc40`；状态 `success`。

```sql
SELECT 
  "Main Category",
  COUNT(*) as total_videos,
  SUM(CASE WHEN "Rank" <= 10 THEN 1 ELSE 0 END) as top10_count,
  ROUND(100.0 * SUM(CASE WHEN "Rank" <= 10 THEN 1 ELSE 0 END) / 520, 1) as top10_pct,
  SUM(CASE WHEN "Rank" <= 30 THEN 1 ELSE 0 END) as top30_count,
  ROUND(100.0 * SUM(CASE WHEN "Rank" <= 30 THEN 1 ELSE 0 END) / 1560, 1) as top30_pct,
  ROUND(AVG("Views")) as avg_views,
  ROUND(AVG("Overall Score")) as avg_score
FROM sheet1
GROUP BY "Main Category"
ORDER BY top10_count DESC
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-014/attempt-01/sql/S23.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-014/attempt-01/sql/S23.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-014/attempt-01/results/S23.rows.jsonl)；完整：True；SHA256：`3950d7cbfab1fb0f4b6b9b47a51c6b8c886c58016470fdebee2defabd61f936f`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "sheet1", "kind": "base", "block": null, "base_tables": ["sheet1"]}] | [] | ["\"Main Category\""] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |
| B1 | SUM(CASE WHEN "Rank" <= 10 THEN 1 ELSE 0 END) | [] | [{"table": "sheet1", "column": "Rank"}] | False |
| B1 | SUM(CASE WHEN "Rank" <= 30 THEN 1 ELSE 0 END) | [] | [{"table": "sheet1", "column": "Rank"}] | False |
| B1 | AVG("Views") | [{"table": "sheet1", "column": "Views"}] | [] | False |
| B1 | AVG("Overall Score") | [{"table": "sheet1", "column": "Overall Score"}] | [] | False |
| B1 | SUM(CASE WHEN "Rank" <= 10 THEN 1 ELSE 0 END) | [] | [{"table": "sheet1", "column": "Rank"}] | False |
| B1 | SUM(CASE WHEN "Rank" <= 30 THEN 1 ELSE 0 END) | [] | [{"table": "sheet1", "column": "Rank"}] | False |


## S24

类别 `data`；来源 `query_db`；调用 `2226e501040c4bbb94b4108ddf1a5709`；状态 `success`。

```sql
SELECT 
  "Video Category",
  COUNT(*) as total_videos,
  SUM(CASE WHEN "Rank" <= 10 THEN 1 ELSE 0 END) as top10_count,
  ROUND(100.0 * SUM(CASE WHEN "Rank" <= 10 THEN 1 ELSE 0 END) / COUNT(*), 1) as top10_pct,
  ROUND(AVG("Views")) as avg_views,
  ROUND(AVG("Overall Score")) as avg_score
FROM sheet1
GROUP BY "Video Category"
HAVING COUNT(*) >= 15
ORDER BY top10_pct DESC
LIMIT 20
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-014/attempt-01/sql/S24.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-014/attempt-01/sql/S24.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-014/attempt-01/results/S24.rows.jsonl)；完整：True；SHA256：`b538782e775f23eeb444e326f09037608161dc4358ba940f9d470858737fc0fc`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "sheet1", "kind": "base", "block": null, "base_tables": ["sheet1"]}] | [] | ["\"Video Category\""] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |
| B1 | SUM(CASE WHEN "Rank" <= 10 THEN 1 ELSE 0 END) | [] | [{"table": "sheet1", "column": "Rank"}] | False |
| B1 | AVG("Views") | [{"table": "sheet1", "column": "Views"}] | [] | False |
| B1 | AVG("Overall Score") | [{"table": "sheet1", "column": "Overall Score"}] | [] | False |
| B1 | COUNT(*) | [] | [] | True |
| B1 | COUNT(*) | [] | [] | True |
| B1 | SUM(CASE WHEN "Rank" <= 10 THEN 1 ELSE 0 END) | [] | [{"table": "sheet1", "column": "Rank"}] | False |


## S25

类别 `data`；来源 `query_db`；调用 `ffeaa721a4b24f2494fc871a29af4b15`；状态 `success`。

```sql
SELECT SUBSTR(_id, 1, 8) as id_prefix, COUNT(*) as cnt FROM sheet1 GROUP BY SUBSTR(_id, 1, 8) ORDER BY cnt DESC
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-014/attempt-01/sql/S25.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-014/attempt-01/sql/S25.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-014/attempt-01/results/S25.rows.jsonl)；完整：True；SHA256：`a122e2a9f21b95c1f30dc28fae7d50146970746b695216214cea902ce564aa9c`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "sheet1", "kind": "base", "block": null, "base_tables": ["sheet1"]}] | [] | ["SUBSTRING(_id, 1, 8)"] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |


## S26

类别 `data`；来源 `query_db`；调用 `a348ee5c428c4fdcb202cbd858bc89a0`；状态 `success`。

```sql
SELECT COUNT(*) as total, COUNT(DISTINCT "Creator") as distinct_creators, COUNT(DISTINCT "Title") as distinct_titles, COUNT(DISTINCT "Video Category") as distinct_categories FROM sheet1
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-014/attempt-01/sql/S26.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-014/attempt-01/sql/S26.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-014/attempt-01/results/S26.rows.jsonl)；完整：True；SHA256：`5fee7e4530eab76d86fc452eeb83aad096e31d3d4b250c3bf8c4a90f40b1ac87`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "sheet1", "kind": "base", "block": null, "base_tables": ["sheet1"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |
| B1 | COUNT(DISTINCT "Creator") | [{"table": "sheet1", "column": "Creator"}] | [] | False |
| B1 | COUNT(DISTINCT "Title") | [{"table": "sheet1", "column": "Title"}] | [] | False |
| B1 | COUNT(DISTINCT "Video Category") | [{"table": "sheet1", "column": "Video Category"}] | [] | False |


## S27

类别 `data`；来源 `query_db`；调用 `34f26724acc5462c91b62a072100e930`；状态 `success`。

```sql
SELECT SUBSTR(_id, 1, 4) as id_prefix, COUNT(*) as cnt FROM sheet1 GROUP BY SUBSTR(_id, 1, 4) ORDER BY cnt DESC
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-014/attempt-01/sql/S27.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-014/attempt-01/sql/S27.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-014/attempt-01/results/S27.rows.jsonl)；完整：True；SHA256：`2ffa7205b234c697974f6e0f42617c75b4b26aada15bd306cc8d740b03b0767b`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "sheet1", "kind": "base", "block": null, "base_tables": ["sheet1"]}] | [] | ["SUBSTRING(_id, 1, 4)"] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |


## S28

类别 `data`；来源 `query_db`；调用 `72b678dea6414a5f872ee030e0fa9e51`；状态 `success`。

```sql
SELECT 
  "Creator Video Count",
  COUNT(*) as cnt,
  ROUND(AVG("Views")) as avg_views,
  ROUND(AVG("Overall Score")) as avg_score
FROM sheet1
GROUP BY "Creator Video Count"
HAVING cnt >= 10
ORDER BY "Creator Video Count"
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-014/attempt-01/sql/S28.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-014/attempt-01/sql/S28.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-014/attempt-01/results/S28.rows.jsonl)；完整：True；SHA256：`05af2cabe1b3ed09257e09dcd9291c7d04af767d860c67a6c6d17257bfac94fa`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "sheet1", "kind": "base", "block": null, "base_tables": ["sheet1"]}] | [] | ["\"Creator Video Count\""] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |
| B1 | AVG("Views") | [{"table": "sheet1", "column": "Views"}] | [] | False |
| B1 | AVG("Overall Score") | [{"table": "sheet1", "column": "Overall Score"}] | [] | False |


## S29

类别 `data`；来源 `query_db`；调用 `16687ffa2a364544a98b890ce0070635`；状态 `success`。

```sql
SELECT 
  "Creator",
  COUNT(*) as num_videos_in_ranking,
  ROUND(AVG("Rank")) as avg_rank,
  ROUND(AVG("Views")) as avg_views,
  ROUND(AVG("Overall Score")) as avg_score,
  ROUND(AVG("Creator Followers")) as avg_followers,
  ROUND(AVG("Creator Video Count")) as avg_video_count
FROM sheet1
GROUP BY "Creator"
HAVING COUNT(*) >= 10
ORDER BY avg_rank ASC
LIMIT 20
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-014/attempt-01/sql/S29.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-014/attempt-01/sql/S29.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-014/attempt-01/results/S29.rows.jsonl)；完整：True；SHA256：`bf2d0f1f6f276a6aa3a6603be558eddfb49aea51540cfb64b787e3c0a544a40a`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "sheet1", "kind": "base", "block": null, "base_tables": ["sheet1"]}] | [] | ["\"Creator\""] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |
| B1 | AVG("Rank") | [{"table": "sheet1", "column": "Rank"}] | [] | False |
| B1 | AVG("Views") | [{"table": "sheet1", "column": "Views"}] | [] | False |
| B1 | AVG("Overall Score") | [{"table": "sheet1", "column": "Overall Score"}] | [] | False |
| B1 | AVG("Creator Followers") | [{"table": "sheet1", "column": "Creator Followers"}] | [] | False |
| B1 | AVG("Creator Video Count") | [{"table": "sheet1", "column": "Creator Video Count"}] | [] | False |
| B1 | COUNT(*) | [] | [] | True |


## S30

类别 `data`；来源 `query_db`；调用 `d9bf2718ca534e19a9cd2b9dff11e8e0`；状态 `success`。

```sql
SELECT 
  "Creator",
  COUNT(*) as num_videos_in_ranking,
  ROUND(AVG("Rank")) as avg_rank,
  ROUND(AVG("Views")) as avg_views,
  ROUND(AVG("Creator Followers")) as avg_followers,
  ROUND(AVG("Creator Video Count")) as avg_video_count
FROM sheet1
GROUP BY "Creator"
HAVING COUNT(*) >= 5
ORDER BY avg_views DESC
LIMIT 20
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-014/attempt-01/sql/S30.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-014/attempt-01/sql/S30.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-014/attempt-01/results/S30.rows.jsonl)；完整：True；SHA256：`5a1ae0a63f81a8c2e5cf5f70273870511a4c5bda134822c7edc018a3a8c7eba6`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "sheet1", "kind": "base", "block": null, "base_tables": ["sheet1"]}] | [] | ["\"Creator\""] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |
| B1 | AVG("Rank") | [{"table": "sheet1", "column": "Rank"}] | [] | False |
| B1 | AVG("Views") | [{"table": "sheet1", "column": "Views"}] | [] | False |
| B1 | AVG("Creator Followers") | [{"table": "sheet1", "column": "Creator Followers"}] | [] | False |
| B1 | AVG("Creator Video Count") | [{"table": "sheet1", "column": "Creator Video Count"}] | [] | False |
| B1 | COUNT(*) | [] | [] | True |


## S31

类别 `data`；来源 `query_db`；调用 `5c624520c85749aa8dadad28be08d659`；状态 `success`。

```sql
SELECT 
  CASE 
    WHEN "Creator Followers" < 10000 THEN '1. <10k'
    WHEN "Creator Followers" < 100000 THEN '2. 10k-100k'
    WHEN "Creator Followers" < 1000000 THEN '3. 100k-1M'
    ELSE '4. >1M' 
  END as follower_band,
  COUNT(*) as cnt,
  ROUND(AVG("Views")) as avg_views,
  ROUND(AVG("Overall Score")) as avg_score,
  ROUND(AVG("Likes")) as avg_likes,
  ROUND(AVG("Shares")) as avg_shares,
  ROUND(AVG("Coins")) as avg_coins
FROM sheet1
GROUP BY follower_band
ORDER BY follower_band
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-014/attempt-01/sql/S31.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-014/attempt-01/sql/S31.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-014/attempt-01/results/S31.rows.jsonl)；完整：True；SHA256：`0039bff358ef0cfe03462d8a00ada1ef9ea33ea8a2a69a085e93fb4f870ffe94`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "sheet1", "kind": "base", "block": null, "base_tables": ["sheet1"]}] | [] | ["CASE WHEN \"Creator Followers\" < 10000 THEN '1. <10k' WHEN \"Creator Followers\" < 100000 THEN '2. 10k-100k' WHEN \"Creator Followers\" < 1000000 THEN '3. 100k-1M' ELSE '4. >1M' END"] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |
| B1 | AVG("Views") | [{"table": "sheet1", "column": "Views"}] | [] | False |
| B1 | AVG("Overall Score") | [{"table": "sheet1", "column": "Overall Score"}] | [] | False |
| B1 | AVG("Likes") | [{"table": "sheet1", "column": "Likes"}] | [] | False |
| B1 | AVG("Shares") | [{"table": "sheet1", "column": "Shares"}] | [] | False |
| B1 | AVG("Coins") | [{"table": "sheet1", "column": "Coins"}] | [] | False |


## S32

类别 `data`；来源 `query_db`；调用 `8908e5c5a612441585736f8d02c29121`；状态 `success`。

```sql
SELECT 
  CASE 
    WHEN "Creator Video Count" = 100 THEN '100 (full)'
    WHEN "Creator Video Count" < 10 THEN '1-9'
    WHEN "Creator Video Count" < 50 THEN '10-49'
    ELSE '50-99'
  END as video_count_band,
  COUNT(*) as cnt,
  ROUND(AVG("Views")) as avg_views,
  ROUND(AVG("Overall Score")) as avg_score,
  ROUND(AVG("Rank")) as avg_rank
FROM sheet1
GROUP BY video_count_band
ORDER BY video_count_band
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-014/attempt-01/sql/S32.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-014/attempt-01/sql/S32.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-014/attempt-01/results/S32.rows.jsonl)；完整：True；SHA256：`7810b9083048eee003debda42af02677e99cef04dbfca3ae7b8d538d490d773c`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "sheet1", "kind": "base", "block": null, "base_tables": ["sheet1"]}] | [] | ["CASE WHEN \"Creator Video Count\" = 100 THEN '100 (full)' WHEN \"Creator Video Count\" < 10 THEN '1-9' WHEN \"Creator Video Count\" < 50 THEN '10-49' ELSE '50-99' END"] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |
| B1 | AVG("Views") | [{"table": "sheet1", "column": "Views"}] | [] | False |
| B1 | AVG("Overall Score") | [{"table": "sheet1", "column": "Overall Score"}] | [] | False |
| B1 | AVG("Rank") | [{"table": "sheet1", "column": "Rank"}] | [] | False |


## S33

类别 `data`；来源 `query_db`；调用 `485f0caf43ea406681a316a79cd87cb5`；状态 `success`。

```sql
SELECT 
  ROUND(1.0 * SUM(CASE WHEN "Views" >= 5000000 THEN 1 ELSE 0 END) / COUNT(*) * 100, 1) as pct_viral_5m,
  ROUND(1.0 * SUM(CASE WHEN "Views" >= 2000000 THEN 1 ELSE 0 END) / COUNT(*) * 100, 1) as pct_viral_2m
FROM sheet1
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-014/attempt-01/sql/S33.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-014/attempt-01/sql/S33.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-014/attempt-01/results/S33.rows.jsonl)；完整：True；SHA256：`a3b6275b344e30defb8c103063af0f48fa56242993573eef76152fd9dc0629f6`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "sheet1", "kind": "base", "block": null, "base_tables": ["sheet1"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |
| B1 | COUNT(*) | [] | [] | True |
| B1 | SUM(CASE WHEN "Views" >= 5000000 THEN 1 ELSE 0 END) | [] | [{"table": "sheet1", "column": "Views"}] | False |
| B1 | SUM(CASE WHEN "Views" >= 2000000 THEN 1 ELSE 0 END) | [] | [{"table": "sheet1", "column": "Views"}] | False |


## S34

类别 `data`；来源 `query_db`；调用 `b1cf7146381f4344b563e263176eb268`；状态 `success`。

```sql
SELECT 
  "Video Category",
  COUNT(*) as cnt,
  ROUND(100.0 * SUM(CASE WHEN "Views" >= 2000000 THEN 1 ELSE 0 END) / COUNT(*), 1) as pct_viral_2m,
  ROUND(AVG("Views")) as avg_views
FROM sheet1
GROUP BY "Video Category"
HAVING cnt >= 15
ORDER BY pct_viral_2m DESC
LIMIT 15
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-014/attempt-01/sql/S34.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-014/attempt-01/sql/S34.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-014/attempt-01/results/S34.rows.jsonl)；完整：True；SHA256：`b50c06b7154f827e11a50b60cd0cae00f0aa59a690dcbf0ffe41630d796bf36e`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "sheet1", "kind": "base", "block": null, "base_tables": ["sheet1"]}] | [] | ["\"Video Category\""] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |
| B1 | AVG("Views") | [{"table": "sheet1", "column": "Views"}] | [] | False |
| B1 | COUNT(*) | [] | [] | True |
| B1 | SUM(CASE WHEN "Views" >= 2000000 THEN 1 ELSE 0 END) | [] | [{"table": "sheet1", "column": "Views"}] | False |


## S35

类别 `data`；来源 `python`；调用 `8aa3b8c759a24ca486025d82039205bb`；状态 `success`。

```sql
SELECT * FROM sheet1 WHERE Views >= 5000000 ORDER BY Views DESC
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-014/attempt-01/sql/S35.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-014/attempt-01/sql/S35.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-014/attempt-01/results/S35.rows.jsonl)；完整：True；SHA256：`1f6cdc9d05d35427306e1ea3cac2e9d6cd6884f5d09e06d1e6c198bd15e5a6e6`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "sheet1", "kind": "base", "block": null, "base_tables": ["sheet1"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |


## S36

类别 `data`；来源 `python`；调用 `be6209b44f8d401bbb3ef4777d6f35b0`；状态 `success`。

```sql
SELECT * FROM sheet1
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-014/attempt-01/sql/S36.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-014/attempt-01/sql/S36.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-014/attempt-01/results/S36.rows.jsonl)；完整：True；SHA256：`32e75fb7897fb80a00528734d7f3e798dc6949f79a2e6912632fab9f18756903`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "sheet1", "kind": "base", "block": null, "base_tables": ["sheet1"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |


## S37

类别 `data`；来源 `query_db`；调用 `9549a6084bed4527bc6e3efcdeb3cd3e`；状态 `success`。

```sql
SELECT "Main Category", COUNT(*) as cnt, MIN("Rank") as min_rank, MAX("Rank") as max_rank, COUNT(DISTINCT "Rank") as distinct_ranks
FROM sheet1
GROUP BY "Main Category"
ORDER BY cnt DESC
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-014/attempt-01/sql/S37.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-014/attempt-01/sql/S37.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-014/attempt-01/results/S37.rows.jsonl)；完整：True；SHA256：`6c3195b4e1b3c667c6a4acdd760e777644db58eb82dbdb39db2b038e8c47bfdb`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "sheet1", "kind": "base", "block": null, "base_tables": ["sheet1"]}] | [] | ["\"Main Category\""] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |
| B1 | MIN("Rank") | [{"table": "sheet1", "column": "Rank"}] | [] | False |
| B1 | MAX("Rank") | [{"table": "sheet1", "column": "Rank"}] | [] | False |
| B1 | COUNT(DISTINCT "Rank") | [{"table": "sheet1", "column": "Rank"}] | [] | False |


## S38

类别 `data`；来源 `query_db`；调用 `45dad9546ad14ebab364c86f2aefb1ba`；状态 `success`。

```sql
SELECT COUNT(*) as cnt, COUNT(DISTINCT "Title" || '|' || "Creator") as unique_videos FROM sheet1
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-014/attempt-01/sql/S38.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-014/attempt-01/sql/S38.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-014/attempt-01/results/S38.rows.jsonl)；完整：True；SHA256：`a986847bfb2e98f3c6173385eb49219b36608727d4108e138ba5e2d35dd6233a`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "sheet1", "kind": "base", "block": null, "base_tables": ["sheet1"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |
| B1 | COUNT(DISTINCT "Title" \|\| '\|' \|\| "Creator") | [{"table": "sheet1", "column": "Creator"}, {"table": "sheet1", "column": "Title"}] | [] | False |


## S39

类别 `data`；来源 `python`；调用 `6bcbb5961ff84a8cbd5c612c765e01db`；状态 `success`。

```sql
SELECT _id, "Main Category", "Rank" FROM sheet1
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-014/attempt-01/sql/S39.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-014/attempt-01/sql/S39.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-014/attempt-01/results/S39.rows.jsonl)；完整：True；SHA256：`6d395e77cbad0f9743b48e51c305da87529185cee499ef39876c46ae7fd6df56`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "sheet1", "kind": "base", "block": null, "base_tables": ["sheet1"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |


## S40

类别 `data`；来源 `python`；调用 `29b97c35a11148db827afe99012d7ff8`；状态 `success`。

```sql
SELECT * FROM sheet1
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-014/attempt-01/sql/S40.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-014/attempt-01/sql/S40.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-014/attempt-01/results/S40.rows.jsonl)；完整：True；SHA256：`32e75fb7897fb80a00528734d7f3e798dc6949f79a2e6912632fab9f18756903`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "sheet1", "kind": "base", "block": null, "base_tables": ["sheet1"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |


## S41

类别 `data`；来源 `python`；调用 `38db8700b9674c31bfc83f8d4b39a533`；状态 `success`。

```sql
SELECT * FROM sheet1
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-014/attempt-01/sql/S41.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-014/attempt-01/sql/S41.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-014/attempt-01/results/S41.rows.jsonl)；完整：True；SHA256：`32e75fb7897fb80a00528734d7f3e798dc6949f79a2e6912632fab9f18756903`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "sheet1", "kind": "base", "block": null, "base_tables": ["sheet1"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |


## S42

类别 `data`；来源 `python`；调用 `ae204872cca048fa98db51994826939c`；状态 `success`。

```sql
SELECT * FROM sheet1
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-014/attempt-01/sql/S42.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-014/attempt-01/sql/S42.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-014/attempt-01/results/S42.rows.jsonl)；完整：True；SHA256：`32e75fb7897fb80a00528734d7f3e798dc6949f79a2e6912632fab9f18756903`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "sheet1", "kind": "base", "block": null, "base_tables": ["sheet1"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |


## S43

类别 `data`；来源 `python`；调用 `05bd5db636d94f948477f48eb6042db6`；状态 `success`。

```sql
SELECT * FROM sheet1
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-014/attempt-01/sql/S43.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-014/attempt-01/sql/S43.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-014/attempt-01/results/S43.rows.jsonl)；完整：True；SHA256：`32e75fb7897fb80a00528734d7f3e798dc6949f79a2e6912632fab9f18756903`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "sheet1", "kind": "base", "block": null, "base_tables": ["sheet1"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |


## S44

类别 `data`；来源 `python`；调用 `55ea61cbc2aa4830bf05daba4c25d767`；状态 `success`。

```sql
SELECT * FROM sheet1
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-014/attempt-01/sql/S44.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-014/attempt-01/sql/S44.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-014/attempt-01/results/S44.rows.jsonl)；完整：True；SHA256：`32e75fb7897fb80a00528734d7f3e798dc6949f79a2e6912632fab9f18756903`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "sheet1", "kind": "base", "block": null, "base_tables": ["sheet1"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |


## S45

类别 `data`；来源 `python`；调用 `d91e45ac599e4bb084e07b8988f39344`；状态 `success`。

```sql
SELECT * FROM sheet1
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-014/attempt-01/sql/S45.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-014/attempt-01/sql/S45.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-014/attempt-01/results/S45.rows.jsonl)；完整：True；SHA256：`32e75fb7897fb80a00528734d7f3e798dc6949f79a2e6912632fab9f18756903`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "sheet1", "kind": "base", "block": null, "base_tables": ["sheet1"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |


## S46

类别 `data`；来源 `python`；调用 `ce885ad106804e6fa4c8e3e93834f752`；状态 `success`。

```sql
SELECT * FROM sheet1
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-014/attempt-01/sql/S46.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-014/attempt-01/sql/S46.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-014/attempt-01/results/S46.rows.jsonl)；完整：True；SHA256：`32e75fb7897fb80a00528734d7f3e798dc6949f79a2e6912632fab9f18756903`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "sheet1", "kind": "base", "block": null, "base_tables": ["sheet1"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |


## S47

类别 `data`；来源 `python`；调用 `301eac4474204103839de3dd21e0c934`；状态 `success`。

```sql
SELECT * FROM sheet1
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-014/attempt-01/sql/S47.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-014/attempt-01/sql/S47.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-014/attempt-01/results/S47.rows.jsonl)；完整：True；SHA256：`32e75fb7897fb80a00528734d7f3e798dc6949f79a2e6912632fab9f18756903`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "sheet1", "kind": "base", "block": null, "base_tables": ["sheet1"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |


## S48

类别 `data`；来源 `python`；调用 `856048ec668a4c1eb9d1587fe8a2da02`；状态 `success`。

```sql
SELECT * FROM sheet1
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-014/attempt-01/sql/S48.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-014/attempt-01/sql/S48.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-014/attempt-01/results/S48.rows.jsonl)；完整：True；SHA256：`32e75fb7897fb80a00528734d7f3e798dc6949f79a2e6912632fab9f18756903`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "sheet1", "kind": "base", "block": null, "base_tables": ["sheet1"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |


## S49

类别 `data`；来源 `python`；调用 `f9ab7310ebf948729573068caf6cc614`；状态 `success`。

```sql
SELECT * FROM sheet1
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-014/attempt-01/sql/S49.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-014/attempt-01/sql/S49.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-014/attempt-01/results/S49.rows.jsonl)；完整：True；SHA256：`32e75fb7897fb80a00528734d7f3e798dc6949f79a2e6912632fab9f18756903`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "sheet1", "kind": "base", "block": null, "base_tables": ["sheet1"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |


## S50

类别 `data`；来源 `query_db`；调用 `2dc2fe8b5add49e0889aacdc4138fbbc`；状态 `success`。

```sql
SELECT 
  CASE WHEN "Bilibili Personal Verification" IS NOT NULL THEN 'Verified' ELSE 'Not Verified' END as vstatus,
  COUNT(*) as cnt,
  ROUND(100.0*SUM(CASE WHEN "Views" >= 2000000 THEN 1 ELSE 0 END)/COUNT(*),1) as pct_viral_2m,
  ROUND(100.0*SUM(CASE WHEN "Views" >= 1000000 THEN 1 ELSE 0 END)/COUNT(*),1) as pct_viral_1m,
  ROUND(AVG("Rank")) as avg_rank
FROM sheet1
GROUP BY vstatus
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-014/attempt-01/sql/S50.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-014/attempt-01/sql/S50.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-014/attempt-01/results/S50.rows.jsonl)；完整：True；SHA256：`a87dc13878673de0ca4f04fd5b8d27129fb12303ed41dd3f72d7ce47e57b4a55`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "sheet1", "kind": "base", "block": null, "base_tables": ["sheet1"]}] | [] | ["CASE WHEN NOT \"Bilibili Personal Verification\" IS NULL THEN 'Verified' ELSE 'Not Verified' END"] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |
| B1 | AVG("Rank") | [{"table": "sheet1", "column": "Rank"}] | [] | False |
| B1 | COUNT(*) | [] | [] | True |
| B1 | COUNT(*) | [] | [] | True |
| B1 | SUM(CASE WHEN "Views" >= 2000000 THEN 1 ELSE 0 END) | [] | [{"table": "sheet1", "column": "Views"}] | False |
| B1 | SUM(CASE WHEN "Views" >= 1000000 THEN 1 ELSE 0 END) | [] | [{"table": "sheet1", "column": "Views"}] | False |


## S51

类别 `data`；来源 `query_db`；调用 `1d3e1ca491d54a8692ea0f86e77b278e`；状态 `success`。

```sql
SELECT 
  "Video Category",
  ROUND(AVG("Views")) as avg_views,
  ROUND(AVG("Likes")) as avg_likes,
  ROUND(AVG("Coins")) as avg_coins,
  ROUND(AVG("Shares")) as avg_shares,
  ROUND(AVG("Favorites")) as avg_fav,
  ROUND(AVG("Comments")) as avg_comments,
  ROUND(AVG("Danmaku Count")) as avg_danmaku
FROM sheet1
WHERE "Main Category" = 'Whole site'
GROUP BY "Video Category"
HAVING COUNT(*) >= 3
ORDER BY avg_views DESC
LIMIT 15
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-014/attempt-01/sql/S51.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-014/attempt-01/sql/S51.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-014/attempt-01/results/S51.rows.jsonl)；完整：True；SHA256：`a819c7ed30afbe9ab2b090aed7fae0ebb3e92b2762d3f6f5774e0df84dfc4b76`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "sheet1", "kind": "base", "block": null, "base_tables": ["sheet1"]}] | [] | ["\"Video Category\""] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | AVG("Views") | [{"table": "sheet1", "column": "Views"}] | [] | False |
| B1 | AVG("Likes") | [{"table": "sheet1", "column": "Likes"}] | [] | False |
| B1 | AVG("Coins") | [{"table": "sheet1", "column": "Coins"}] | [] | False |
| B1 | AVG("Shares") | [{"table": "sheet1", "column": "Shares"}] | [] | False |
| B1 | AVG("Favorites") | [{"table": "sheet1", "column": "Favorites"}] | [] | False |
| B1 | AVG("Comments") | [{"table": "sheet1", "column": "Comments"}] | [] | False |
| B1 | AVG("Danmaku Count") | [{"table": "sheet1", "column": "Danmaku Count"}] | [] | False |
| B1 | COUNT(*) | [] | [] | True |

