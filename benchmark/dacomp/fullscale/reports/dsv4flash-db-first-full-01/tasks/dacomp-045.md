# dacomp-045

To enhance user stickiness and overall revenue, analyze and compare high-value users (Diam…

运行：已提交。官方未评分。全部 SQL 尝试/成功 37/37；数据 SQL 35/35；Python 2 次。

完整原题：

To enhance user stickiness and overall revenue, analyze and compare high-value users (Diamond/Platinum members) versus regular users in Category/Brand preferences in Search and Favorites, as well as differences in Search active time, and provide targeted tiered user operations strategies and optimized product recommendation plans.

| 表 | 行数 | 列数 |
| --- | --- | --- |
| browsing_behavior_records_table | 491 | 15 |
| device_information_table | 491 | 7 |
| network_environment_information | 561 | 13 |
| product_basic_information_table | 491 | 25 |
| product_favorites_table | 426 | 11 |
| search_behavior_records_table | 451 | 18 |
| user_basic_information_table | 491 | 16 |
| user_geolocation_information_ta | 468 | 11 |


实际路线（分析者依据 SQL/源码概括，不代表 Agent 自述）：SQL 比较高价值与普通会员的搜索、收藏偏好及时段 → Python 卡方检验、占比转换与图表。

数据库大小：1,089,536 字节。

## 数据 SQL

| SQL | 状态 | 基础表 | Join 输入/类型 | GROUP BY | 聚合表达式 | 结果行数 | 数据库 ms |
| --- | --- | --- | --- | --- | --- | --- | --- |
| [S3/Q1](#s3) | success | ["user_basic_information_table"] | 0 / {} | ["\"Membership Level\""] | ["COUNT(*)"] | 4 | 0.53 |
| [S4/Q2](#s4) | success | ["user_basic_information_table"] | 0 / {} | [] | ["COUNT(*)", "COUNT(DISTINCT \"User ID\")"] | 1 | 0.623 |
| [S5/Q3](#s5) | success | ["search_behavior_records_table"] | 0 / {} | [] | ["COUNT(*)", "COUNT(DISTINCT \"User ID\")"] | 1 | 0.586 |
| [S6/Q4](#s6) | success | ["product_favorites_table"] | 0 / {} | [] | ["COUNT(*)", "COUNT(DISTINCT \"User ID\")"] | 1 | 0.554 |
| [S7/Q5](#s7) | success | ["product_basic_information_table"] | 0 / {} | [] | [] | 7 | 0.589 |
| [S8/Q6](#s8) | success | ["product_basic_information_table"] | 0 / {} | [] | [] | 6 | 0.517 |
| [S9/Q7](#s9) | success | ["product_basic_information_table"] | 0 / {} | [] | ["COUNT(*)", "COUNT(DISTINCT \"Category ID\")", "COUNT(DISTINCT \"Brand ID\")"] | 1 | 0.748 |
| [S10/Q8](#s10) | success | ["search_behavior_records_table"] | 0 / {} | ["\"Search Keyword\""] | ["COUNT(*)"] | 13 | 0.535 |
| [S11/Q9](#s11) | success | ["search_behavior_records_table"] | 0 / {} | ["\"Search Box Location\""] | ["COUNT(*)"] | 3 | 0.475 |
| [S12/Q10](#s12) | success | ["product_favorites_table"] | 0 / {} | ["\"Favorites Folder Name\""] | ["COUNT(*)"] | 5 | 0.487 |
| [S13/Q11](#s13) | success | ["product_basic_information_table"] | 0 / {} | [] | [] | 20 | 0.441 |
| [S14/Q12](#s14) | success | ["product_basic_information_table"] | 0 / {} | ["\"Category Name\""] | ["COUNT(*)"] | 7 | 0.53 |
| [S15/Q13](#s15) | success | ["user_basic_information_table"] | 0 / {} | [] | [] | 491 | 0.841 |
| [S16/Q14](#s16) | success | ["search_behavior_records_table", "user_basic_information_table"] | 2 / {'INNER': 1} | ["ug.user_group", "s.\"Search Keyword\""] | ["COUNT(*)"] | 39 | 1.448 |
| [S17/Q15](#s17) | success | ["search_behavior_records_table", "user_basic_information_table"] | 2 / {'INNER': 1} | ["ug.user_group", "s.\"Search Keyword\""] | ["COUNT(*)", "COUNT(*)", "COUNT(*)"] | 39 | 1.572 |
| [S18/Q16](#s18) | success | ["product_basic_information_table", "product_favorites_table", "user_basic_information_table"] | 3 / {'INNER': 2} | ["ug.user_group", "p.\"Category Name\""] | ["COUNT(*)", "COUNT(*)", "COUNT(*)"] | 21 | 2.125 |
| [S19/Q17](#s19) | success | ["product_basic_information_table", "product_favorites_table", "user_basic_information_table"] | 3 / {'INNER': 2} | ["ug.user_group", "p.\"Brand Name\""] | ["COUNT(*)", "COUNT(*)", "COUNT(*)"] | 18 | 2.049 |
| [S20/Q18](#s20) | success | ["product_basic_information_table"] | 0 / {} | ["\"Product Name\""] | ["COUNT(*)"] | 10 | 0.846 |
| [S21/Q19](#s21) | success | ["search_behavior_records_table", "user_basic_information_table"] | 2 / {'INNER': 1} | ["ug.user_group", "CAST(STRFTIME('%H', s.\"Search Time\") AS INTEGER)"] | ["COUNT(*)"] | 70 | 1.553 |
| [S22/Q20](#s22) | success | ["search_behavior_records_table"] | 0 / {} | [] | [] | 10 | 0.336 |
| [S23/Q21](#s23) | success | ["search_behavior_records_table", "user_basic_information_table"] | 2 / {'INNER': 1} | ["ug.user_group"] | ["COUNT(*)", "AVG(s.\"Input Duration\")", "AVG(s.\"Viewed Result Count\")", "AVG(s.\"Clicked Result Count\")", "AVG(s.\"Search Conversion Rate\")", "AVG(s.\"Suggestion Count\")", "SUM(s.\"No Result Search Count\")", "AVG(s.\"Used Autocomplete\" = 'Yes')"] | 3 | 1.675 |
| [S24/Q22](#s24) | success | ["browsing_behavior_records_table", "user_basic_information_table"] | 2 / {'INNER': 1} | ["ug.user_group"] | ["COUNT(*)", "AVG(b.\"Time on Page\")", "AVG(b.\"View Count\")", "AVG(b.\"Scroll Distance\")", "AVG(b.\"Zoom Count\")", "AVG(b.\"Time on Detail Page\")", "AVG(b.\"Time on Review Page\")", "COUNT(*)", "AVG(b.\"Has Swiped\" = 'Yes')", "AVG(b.\"Has Zoomed\" = 'Yes')", "AVG(b.\"Viewed Specifications\" = 'Yes')", "SUM(b.\"Product Link Share Count\")"] | 3 | 1.957 |
| [S25/Q23](#s25) | success | ["search_behavior_records_table", "user_basic_information_table"] | 2 / {'INNER': 1} | ["ug.user_group", "CAST(STRFTIME('%w', s.\"Search Time\") AS INTEGER)"] | ["COUNT(*)"] | 21 | 1.54 |
| [S26/Q24](#s26) | success | ["search_behavior_records_table", "user_basic_information_table"] | 2 / {'INNER': 1} | ["ug.user_group", "CAST(STRFTIME('%m', s.\"Search Time\") AS INTEGER)"] | ["COUNT(*)"] | 36 | 1.615 |
| [S27/Q25](#s27) | success | ["user_basic_information_table"] | 2 / {'INNER': 1} | ["ug.user_group"] | ["COUNT(*)", "AVG(u.\"Login Count\")", "AVG(u.\"Device count\")", "COUNT(*)", "COUNT(*)", "SUM(CASE WHEN u.\"Payment enabled\" = 'Yes' THEN 1 ELSE 0 END)", "SUM(CASE WHEN u.\"Real-name verification status\" = 'Verified' THEN 1 ELSE 0 END)"] | 3 | 1.444 |
| [S28/Q26](#s28) | success | ["user_basic_information_table"] | 2 / {'INNER': 1} | ["ug.user_group", "u.\"Age group\""] | ["COUNT(*)"] | 12 | 1.265 |
| [S29/Q27](#s29) | success | ["user_basic_information_table"] | 2 / {'INNER': 1} | ["ug.user_group", "u.\"Income level\""] | ["COUNT(*)"] | 12 | 1.302 |
| [S30/Q28](#s30) | success | ["browsing_behavior_records_table", "product_basic_information_table", "user_basic_information_table"] | 3 / {'INNER': 2} | ["ug.user_group", "p.\"Category Name\""] | ["COUNT(*)", "COUNT(*)", "COUNT(*)"] | 21 | 2.144 |
| [S31/Q29](#s31) | success | ["browsing_behavior_records_table", "product_basic_information_table", "user_basic_information_table"] | 3 / {'INNER': 2} | ["ug.user_group", "p.\"Brand Name\""] | ["COUNT(*)", "COUNT(*)", "COUNT(*)"] | 18 | 2.176 |
| [S32/Q30](#s32) | success | ["browsing_behavior_records_table", "product_basic_information_table", "user_basic_information_table"] | 3 / {'INNER': 2} | ["ug.user_group"] | ["AVG(p.\"Price\")", "AVG(p.\"Sale Price\")", "AVG(p.\"Original Price\")"] | 3 | 2.004 |
| [S33/Q31](#s33) | success | ["product_basic_information_table", "product_favorites_table", "user_basic_information_table"] | 3 / {'INNER': 2} | ["ug.user_group"] | ["AVG(p.\"Price\")", "AVG(p.\"Sale Price\")", "AVG(p.\"Original Price\")"] | 3 | 2.007 |
| [S34/Q32](#s34) | success | ["user_basic_information_table"] | 2 / {'INNER': 1} | ["ug.user_group", "u.\"Gender\""] | ["COUNT(*)"] | 6 | 1.265 |
| [S35/Q33](#s35) | success | ["user_basic_information_table"] | 2 / {'INNER': 1} | ["ug.user_group", "u.\"Occupation\""] | ["COUNT(*)"] | 60 | 1.435 |
| [S36/Q34](#s36) | success | ["user_basic_information_table"] | 2 / {'INNER': 1} | ["ug.user_group", "u.\"Education Level\""] | ["COUNT(*)"] | 12 | 1.415 |
| [S37/Q35](#s37) | success | ["search_behavior_records_table", "user_basic_information_table"] | 2 / {'INNER': 1} | ["ug.user_group", "s.\"Search Keyword\""] | ["COUNT(*)", "COUNT(*)", "COUNT(*)"] | 26 | 1.476 |


## 元数据和设置

| SQL | 类别 | 状态 | 内容 |
| --- | --- | --- | --- |
| S1 | connection_setup | success | PRAGMA query_only=ON |
| S2 | metadata | success | SELECT name,sql FROM sqlite_master WHERE type='table' ORDER BY name |


## Python 与执行位置

人工源码审查：**reviewed_SQL_dominant_with_statistical_and_chart_exceptions**。主要连接、分类汇总和时段计数在 SQL 中完成。Python 使用字面量汇总计数进行卡方检验与绘图；占比及加权平均小时仍可由 SQL 完成，不能认定为完全遵守数据库内计算协议。字面量与 SQL 输出的因果关系不作自动断言。 [证据](../reviews/dacomp-045.json)。

P1：Run chi-square tests for category/brand preference differences between high-value and regular users, and analyze search active-time distributions. These statistical tests (scipy chi2) and the construction of category mappings from search keywords go beyond basic SQL aggregation; SQL already produced the grouped counts.

[源码](../../../runs/dsv4flash-db-first-full-01/dacomp-045/attempt-01/python/P1.py)；[输出](../../../runs/dsv4flash-db-first-full-01/dacomp-045/attempt-01/python/P1.stdout)；[错误](../../../runs/dsv4flash-db-first-full-01/dacomp-045/attempt-01/python/P1.stderr)。自动源码筛查未检出预设迁出信号；这不是全面语义合规证明。

P2：Create comparative visualizations of category/brand preferences (favorites, browsing, search) and search active-time distributions between high-value and regular users. These charts require matplotlib which is not in SQL.

[源码](../../../runs/dsv4flash-db-first-full-01/dacomp-045/attempt-01/python/P2.py)；[输出](../../../runs/dsv4flash-db-first-full-01/dacomp-045/attempt-01/python/P2.stdout)；[错误](../../../runs/dsv4flash-db-first-full-01/dacomp-045/attempt-01/python/P2.stderr)。自动源码筛查未检出预设迁出信号；这不是全面语义合规证明。

## 优化机会

已验证候选。筛选限于精确 SQL、相同自包含 CTE、相同单表完整过滤、可分解单表聚合；未覆盖任意 Join 等价和一般谓词蕴含。全部候选都是 offline，未测在线预测。

| 候选 | 类型 | 已有结果 | 覆盖 SQL | 后续次数 | 中间行数 | 验证 | 成本 |
| --- | --- | --- | --- | --- | --- | --- | --- |
| C1 | common subexpression | False | ["S16", "S17", "S18", "S19", "S21", "S23", "S24", "S25", "S26", "S27", "S28", "S29", "S30", "S31", "S32", "S33", "S34", "S35", "S36", "S37"] | 19 | 491 | verified | Not benchmarked; correctness alone does not establish net speedup. |
| C2 | aggregate MV | False | ["S10", "S11"] | 1 | 39 | verified | Not benchmarked; correctness alone does not establish net speedup. |
| C3 | aggregate MV | False | ["S14", "S20"] | 1 | 70 | verified | Not benchmarked; correctness alone does not establish net speedup. |


已验证覆盖（含触发查询、候选并集去重）：24/35 条成功数据 SQL。正确性仅针对当前数据库快照；未测性能的候选不能声称已加速。

[完整 build/rewrite 与比较证据](dacomp-045.analysis.json)。

### C1：common subexpression

Identical self-contained CTE body across queries.

原查询 [S16](#s16), [S17](#s17), [S18](#s18), [S19](#s19), [S21](#s21), [S23](#s23), [S24](#s24), [S25](#s25), [S26](#s26), [S27](#s27), [S28](#s28), [S29](#s29), [S30](#s30), [S31](#s31), [S32](#s32), [S33](#s33), [S34](#s34), [S35](#s35), [S36](#s36), [S37](#s37) → 新增共享状态 C1 → 后续 19 次可复用。该构建点为事后假设，不代表 Agent 当时预知后续。

构建定义：

```sql
SELECT "User ID", CASE WHEN "Membership Level" IN ('Diamond', 'Platinum') THEN 'High-Value' WHEN "Membership Level" = 'Regular' THEN 'Regular' ELSE 'Gold' END AS user_group FROM user_basic_information_table
```

受益查询 S16 的改写示例：

```sql
/* Analyze search keyword preferences by user group */ WITH user_groups AS (SELECT * FROM temp.reuse_candidate) SELECT ug.user_group, s."Search Keyword", COUNT(*) AS search_count FROM user_groups AS ug JOIN search_behavior_records_table AS s ON ug."User ID" = s."User ID" GROUP BY ug.user_group, s."Search Keyword" ORDER BY ug.user_group, search_count DESC
```

| 原 SQL | 列名一致 | 结果一致 | 比较方法 |
| --- | --- | --- | --- |
| S16 | True | True | ordered_numeric_tolerance |
| S17 | True | True | ordered_numeric_tolerance |
| S18 | True | True | ordered_numeric_tolerance |
| S19 | True | True | ordered_numeric_tolerance |
| S21 | True | True | ordered_numeric_tolerance |
| S23 | True | True | ordered_numeric_tolerance |
| S24 | True | True | ordered_numeric_tolerance |
| S25 | True | True | ordered_numeric_tolerance |
| S26 | True | True | ordered_numeric_tolerance |
| S27 | True | True | ordered_numeric_tolerance |
| S28 | True | True | ordered_numeric_tolerance |
| S29 | True | True | ordered_numeric_tolerance |
| S30 | True | True | ordered_numeric_tolerance |
| S31 | True | True | ordered_numeric_tolerance |
| S32 | True | True | ordered_numeric_tolerance |
| S33 | True | True | ordered_numeric_tolerance |
| S34 | True | True | ordered_numeric_tolerance |
| S35 | True | True | ordered_numeric_tolerance |
| S36 | True | True | ordered_numeric_tolerance |
| S37 | True | True | ordered_numeric_tolerance |


验证状态：verified；成本结论：Not benchmarked; correctness alone does not establish net speedup.

### C2：aggregate MV

Union of grouping keys; decomposable aggregate states; AVG uses SUM and non-NULL COUNT.

原查询 [S10](#s10), [S11](#s11) → 新增共享状态 C2 → 后续 1 次可复用。该构建点为事后假设，不代表 Agent 当时预知后续。

构建定义：

```sql
SELECT "Search Keyword" AS __g0, "Search Box Location" AS __g1, COUNT(*) AS __a0 FROM "search_behavior_records_table"  GROUP BY "Search Keyword", "Search Box Location"
```

受益查询 S10 的改写示例：

```sql
SELECT __g0 AS "Search Keyword", SUM(__a0) AS cnt FROM temp.reuse_candidate GROUP BY __g0 ORDER BY cnt DESC LIMIT 40
```

| 原 SQL | 列名一致 | 结果一致 | 比较方法 |
| --- | --- | --- | --- |
| S10 | True | True | ordered_numeric_tolerance |
| S11 | True | True | ordered_numeric_tolerance |


验证状态：verified；成本结论：Not benchmarked; correctness alone does not establish net speedup.

### C3：aggregate MV

Union of grouping keys; decomposable aggregate states; AVG uses SUM and non-NULL COUNT.

原查询 [S14](#s14), [S20](#s20) → 新增共享状态 C3 → 后续 1 次可复用。该构建点为事后假设，不代表 Agent 当时预知后续。

构建定义：

```sql
SELECT "Category Name" AS __g0, "Product Name" AS __g1, COUNT(*) AS __a0 FROM "product_basic_information_table"  GROUP BY "Category Name", "Product Name"
```

受益查询 S14 的改写示例：

```sql
SELECT __g0 AS "Category Name", SUM(__a0) AS cnt FROM temp.reuse_candidate GROUP BY __g0 ORDER BY cnt DESC
```

| 原 SQL | 列名一致 | 结果一致 | 比较方法 |
| --- | --- | --- | --- |
| S14 | True | True | ordered_numeric_tolerance |
| S20 | True | True | ordered_numeric_tolerance |


验证状态：verified；成本结论：Not benchmarked; correctness alone does not establish net speedup.

结果依赖：自动记录 SQL→Python 的接口父调用，以及源码中引用归档文件的消费者；字面值相同不认定因果。模型方向选择需要人工读取消息，尚未做全面因果标注。

[原始报告](../../../runs/dsv4flash-db-first-full-01/dacomp-045/attempt-01/answer.md)；[统一消息](../../../runs/dsv4flash-db-first-full-01/dacomp-045/attempt-01/messages.jsonl)；[原始 OpenCode 事件](../../../runs/dsv4flash-db-first-full-01/dacomp-045/attempt-01/opencode.jsonl)；[SQL 引擎日志](../../../runs/dsv4flash-db-first-full-01/dacomp-045/attempt-01/sql_journal.jsonl)。

[可读报告（本地图片链接规范化）](../answers/dacomp-045.md)。原始回答保留，分析结论未改写。

## S1

类别 `connection_setup`；来源 `connection`；调用 `14758364ba574282ac564a21cbba3678`；状态 `success`。

```sql
PRAGMA query_only=ON
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-045/attempt-01/sql/S1.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-045/attempt-01/sql/S1.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-045/attempt-01/results/S1.rows.jsonl)；完整：True；SHA256：`e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`。

## S2

类别 `metadata`；来源 `list_db`；调用 `14758364ba574282ac564a21cbba3678`；状态 `success`。

```sql
SELECT name,sql FROM sqlite_master WHERE type='table' ORDER BY name
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-045/attempt-01/sql/S2.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-045/attempt-01/sql/S2.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-045/attempt-01/results/S2.rows.jsonl)；完整：True；SHA256：`708236b00545661040dc351c428513c65594ef9d084a7d1fa73ed4857e0aff3b`。

## S3

类别 `data`；来源 `query_db`；调用 `2c82feb203424b0c899008ed31e2a9f1`；状态 `success`。

```sql
SELECT "Membership Level", COUNT(*) AS user_count FROM user_basic_information_table GROUP BY "Membership Level" ORDER BY user_count DESC
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-045/attempt-01/sql/S3.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-045/attempt-01/sql/S3.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-045/attempt-01/results/S3.rows.jsonl)；完整：True；SHA256：`ef727cbb2014c6e1c0819887b180551a5c0dd70ad5e2eba051b3945e56b2a441`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "user_basic_information_table", "kind": "base", "block": null, "base_tables": ["user_basic_information_table"]}] | [] | ["\"Membership Level\""] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |


## S4

类别 `data`；来源 `query_db`；调用 `15b263d9040440369e9711827843d7e7`；状态 `success`。

```sql
SELECT COUNT(*) AS total_users, COUNT(DISTINCT "User ID") AS distinct_users FROM user_basic_information_table
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-045/attempt-01/sql/S4.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-045/attempt-01/sql/S4.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-045/attempt-01/results/S4.rows.jsonl)；完整：True；SHA256：`b53d57cd356c8bdf033f4003810501d7e35642a22138d786577eed9a52b10770`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "user_basic_information_table", "kind": "base", "block": null, "base_tables": ["user_basic_information_table"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |
| B1 | COUNT(DISTINCT "User ID") | [{"table": "user_basic_information_table", "column": "User ID"}] | [] | False |


## S5

类别 `data`；来源 `query_db`；调用 `95adf7653a754102b5cbe7ce0967b974`；状态 `success`。

```sql
SELECT COUNT(*) AS total_searches, COUNT(DISTINCT "User ID") AS search_users FROM search_behavior_records_table
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-045/attempt-01/sql/S5.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-045/attempt-01/sql/S5.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-045/attempt-01/results/S5.rows.jsonl)；完整：True；SHA256：`0192f8651e3ec995bf4d76158f4141ce72bf1b65db360a8d7223301334a70d4b`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "search_behavior_records_table", "kind": "base", "block": null, "base_tables": ["search_behavior_records_table"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |
| B1 | COUNT(DISTINCT "User ID") | [{"table": "search_behavior_records_table", "column": "User ID"}] | [] | False |


## S6

类别 `data`；来源 `query_db`；调用 `166f69f8b4c14bf192b95ddabd656e08`；状态 `success`。

```sql
SELECT COUNT(*) AS total_favs, COUNT(DISTINCT "User ID") AS fav_users FROM product_favorites_table
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-045/attempt-01/sql/S6.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-045/attempt-01/sql/S6.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-045/attempt-01/results/S6.rows.jsonl)；完整：True；SHA256：`87aa7f8a5bdc80d10abd2a903ed83fa5065cdc83982d20997c0f5d27b9a0744e`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "product_favorites_table", "kind": "base", "block": null, "base_tables": ["product_favorites_table"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |
| B1 | COUNT(DISTINCT "User ID") | [{"table": "product_favorites_table", "column": "User ID"}] | [] | False |


## S7

类别 `data`；来源 `query_db`；调用 `18e65f30209f4dfb99f0ef71115b49cf`；状态 `success`。

```sql
SELECT DISTINCT "Category Name" FROM product_basic_information_table ORDER BY "Category Name"
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-045/attempt-01/sql/S7.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-045/attempt-01/sql/S7.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-045/attempt-01/results/S7.rows.jsonl)；完整：True；SHA256：`fa9850d3d617d8861f286360da7caa26fcef77f1470c2e31c24e7abafe8f70fe`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "product_basic_information_table", "kind": "base", "block": null, "base_tables": ["product_basic_information_table"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |


## S8

类别 `data`；来源 `query_db`；调用 `4b1a3c54278749ddb900d36cf764a445`；状态 `success`。

```sql
SELECT DISTINCT "Brand Name" FROM product_basic_information_table ORDER BY "Brand Name"
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-045/attempt-01/sql/S8.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-045/attempt-01/sql/S8.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-045/attempt-01/results/S8.rows.jsonl)；完整：True；SHA256：`c630fae42edc30f49cf807c3a3bef8def0a9b4eb2e94d3d2048eb46d7e0324c7`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "product_basic_information_table", "kind": "base", "block": null, "base_tables": ["product_basic_information_table"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |


## S9

类别 `data`；来源 `query_db`；调用 `0f3e4e0aac8147628832796e43741450`；状态 `success`。

```sql
SELECT COUNT(*) AS total_products, COUNT(DISTINCT "Category ID") AS categories, COUNT(DISTINCT "Brand ID") AS brands FROM product_basic_information_table
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-045/attempt-01/sql/S9.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-045/attempt-01/sql/S9.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-045/attempt-01/results/S9.rows.jsonl)；完整：True；SHA256：`5a29817651b3182a2faa5137a440dcaa957ea6b2c91aa3fd7bd7b872e5f119e1`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "product_basic_information_table", "kind": "base", "block": null, "base_tables": ["product_basic_information_table"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |
| B1 | COUNT(DISTINCT "Category ID") | [{"table": "product_basic_information_table", "column": "Category ID"}] | [] | False |
| B1 | COUNT(DISTINCT "Brand ID") | [{"table": "product_basic_information_table", "column": "Brand ID"}] | [] | False |


## S10

类别 `data`；来源 `query_db`；调用 `2a5516ef8f3249e58c2144f3e1324b68`；状态 `success`。

```sql
SELECT "Search Keyword", COUNT(*) AS cnt FROM search_behavior_records_table GROUP BY "Search Keyword" ORDER BY cnt DESC LIMIT 40
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-045/attempt-01/sql/S10.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-045/attempt-01/sql/S10.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-045/attempt-01/results/S10.rows.jsonl)；完整：True；SHA256：`30aad51d148a7801a961395ce1a5eac9fd3eac86d4e1561ac88959e02a8ececb`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "search_behavior_records_table", "kind": "base", "block": null, "base_tables": ["search_behavior_records_table"]}] | [] | ["\"Search Keyword\""] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |


## S11

类别 `data`；来源 `query_db`；调用 `f71bc05c1a334f079a860870bfc5f279`；状态 `success`。

```sql
SELECT "Search Box Location", COUNT(*) AS cnt FROM search_behavior_records_table GROUP BY "Search Box Location" ORDER BY cnt DESC
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-045/attempt-01/sql/S11.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-045/attempt-01/sql/S11.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-045/attempt-01/results/S11.rows.jsonl)；完整：True；SHA256：`362e72953b27d718569b6276c0a8195cfbfd72e440b56cee3ccb801f7f98c2ac`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "search_behavior_records_table", "kind": "base", "block": null, "base_tables": ["search_behavior_records_table"]}] | [] | ["\"Search Box Location\""] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |


## S12

类别 `data`；来源 `query_db`；调用 `96f03f2853c748b49bce4e119becd0ad`；状态 `success`。

```sql
SELECT "Favorites Folder Name", COUNT(*) AS cnt FROM product_favorites_table GROUP BY "Favorites Folder Name" ORDER BY cnt DESC LIMIT 30
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-045/attempt-01/sql/S12.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-045/attempt-01/sql/S12.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-045/attempt-01/results/S12.rows.jsonl)；完整：True；SHA256：`c4a0a7eb80d36451672fec92a38c60ba0cf111bb6735a4fb21feec27c20ead04`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "product_favorites_table", "kind": "base", "block": null, "base_tables": ["product_favorites_table"]}] | [] | ["\"Favorites Folder Name\""] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |


## S13

类别 `data`；来源 `query_db`；调用 `ed1efd1e212e4f9e8be53d8e33eaa35a`；状态 `success`。

```sql
SELECT "Product Name", "Category Name", "Brand Name" FROM product_basic_information_table LIMIT 20
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-045/attempt-01/sql/S13.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-045/attempt-01/sql/S13.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-045/attempt-01/results/S13.rows.jsonl)；完整：True；SHA256：`6b54b05a624b111fdf77dbd88b9973cd349e4c1408762f81390a12c31f71ced5`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "product_basic_information_table", "kind": "base", "block": null, "base_tables": ["product_basic_information_table"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |


## S14

类别 `data`；来源 `query_db`；调用 `5d63ce8fdd6b4a04a43313ca73f27b92`；状态 `success`。

```sql
SELECT "Category Name", COUNT(*) AS cnt FROM product_basic_information_table GROUP BY "Category Name" ORDER BY cnt DESC
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-045/attempt-01/sql/S14.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-045/attempt-01/sql/S14.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-045/attempt-01/results/S14.rows.jsonl)；完整：True；SHA256：`ff9fb578de30f66c3f765beb3cd8110d3812b7ff8cf10c03a6eff42286f6819e`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "product_basic_information_table", "kind": "base", "block": null, "base_tables": ["product_basic_information_table"]}] | [] | ["\"Category Name\""] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |


## S15

类别 `data`；来源 `query_db`；调用 `d571129c1f994a90b8188a6710ea4f7a`；状态 `success`。

```sql
-- Assign user groups: High-value (Diamond/Platinum), Regular, and Gold (intermediate)
SELECT u."User ID",
  CASE 
    WHEN u."Membership Level" IN ('Diamond', 'Platinum') THEN 'High-Value'
    WHEN u."Membership Level" = 'Regular' THEN 'Regular'
    ELSE 'Gold'
  END AS user_group
FROM user_basic_information_table u
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-045/attempt-01/sql/S15.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-045/attempt-01/sql/S15.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-045/attempt-01/results/S15.rows.jsonl)；完整：True；SHA256：`913c058ca7d8474e4503c2b90702034b28a11eecbabf426c48ac748a9d09c46f`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "u", "kind": "base", "block": null, "base_tables": ["user_basic_information_table"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |


## S16

类别 `data`；来源 `query_db`；调用 `64620e213d21469aaa04fa1fbc1ec80c`；状态 `success`。

```sql
-- Analyze search keyword preferences by user group
WITH user_groups AS (
  SELECT "User ID",
    CASE 
      WHEN "Membership Level" IN ('Diamond', 'Platinum') THEN 'High-Value'
      WHEN "Membership Level" = 'Regular' THEN 'Regular'
      ELSE 'Gold'
    END AS user_group
  FROM user_basic_information_table
)
SELECT ug.user_group, s."Search Keyword", COUNT(*) AS search_count
FROM user_groups ug
JOIN search_behavior_records_table s ON ug."User ID" = s."User ID"
GROUP BY ug.user_group, s."Search Keyword"
ORDER BY ug.user_group, search_count DESC
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-045/attempt-01/sql/S16.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-045/attempt-01/sql/S16.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-045/attempt-01/results/S16.rows.jsonl)；完整：True；SHA256：`68d90f008dc76016eeff0e6e3ac0f70a72191f0271cd7ad0a786481c26f90e68`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "user_basic_information_table", "kind": "base", "block": null, "base_tables": ["user_basic_information_table"]}] | [] | [] |
| B2 | [{"alias": "ug", "kind": "derived", "block": "B1", "base_tables": ["user_basic_information_table"]}, {"alias": "s", "kind": "base", "block": null, "base_tables": ["search_behavior_records_table"]}] | [{"type": "INNER", "right": "search_behavior_records_table AS s", "on": "ug.\"User ID\" = s.\"User ID\"", "using": []}] | ["ug.user_group", "s.\"Search Keyword\""] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B2 | COUNT(*) | [] | [] | True |


## S17

类别 `data`；来源 `query_db`；调用 `26e3b6913e204b7b9f7cc1e5dd631117`；状态 `success`。

```sql
-- Get full search keyword distribution by user group
WITH user_groups AS (
  SELECT "User ID",
    CASE 
      WHEN "Membership Level" IN ('Diamond', 'Platinum') THEN 'High-Value'
      WHEN "Membership Level" = 'Regular' THEN 'Regular'
      ELSE 'Gold'
    END AS user_group
  FROM user_basic_information_table
)
SELECT ug.user_group, s."Search Keyword", COUNT(*) AS search_count,
  ROUND(COUNT(*) * 100.0 / SUM(COUNT(*)) OVER (PARTITION BY ug.user_group), 1) AS pct
FROM user_groups ug
JOIN search_behavior_records_table s ON ug."User ID" = s."User ID"
GROUP BY ug.user_group, s."Search Keyword"
ORDER BY ug.user_group, search_count DESC
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-045/attempt-01/sql/S17.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-045/attempt-01/sql/S17.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-045/attempt-01/results/S17.rows.jsonl)；完整：True；SHA256：`d8455b5c7bfdba4163d9d27fb70add462ca755b755d15cfcc2aa88a5096a9dcf`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "user_basic_information_table", "kind": "base", "block": null, "base_tables": ["user_basic_information_table"]}] | [] | [] |
| B2 | [{"alias": "ug", "kind": "derived", "block": "B1", "base_tables": ["user_basic_information_table"]}, {"alias": "s", "kind": "base", "block": null, "base_tables": ["search_behavior_records_table"]}] | [{"type": "INNER", "right": "search_behavior_records_table AS s", "on": "ug.\"User ID\" = s.\"User ID\"", "using": []}] | ["ug.user_group", "s.\"Search Keyword\""] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B2 | COUNT(*) | [] | [] | True |
| B2 | COUNT(*) | [] | [] | True |
| B2 | COUNT(*) | [] | [] | True |


## S18

类别 `data`；来源 `query_db`；调用 `b4567ff6d6244f38b746ecd1535031f6`；状态 `success`。

```sql
-- Favorites by category and user group
WITH user_groups AS (
  SELECT "User ID",
    CASE 
      WHEN "Membership Level" IN ('Diamond', 'Platinum') THEN 'High-Value'
      WHEN "Membership Level" = 'Regular' THEN 'Regular'
      ELSE 'Gold'
    END AS user_group
  FROM user_basic_information_table
)
SELECT ug.user_group, p."Category Name", COUNT(*) AS fav_count,
  ROUND(COUNT(*) * 100.0 / SUM(COUNT(*)) OVER (PARTITION BY ug.user_group), 1) AS pct
FROM user_groups ug
JOIN product_favorites_table f ON ug."User ID" = f."User ID"
JOIN product_basic_information_table p ON f."Product ID" = p."Product ID"
GROUP BY ug.user_group, p."Category Name"
ORDER BY ug.user_group, fav_count DESC
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-045/attempt-01/sql/S18.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-045/attempt-01/sql/S18.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-045/attempt-01/results/S18.rows.jsonl)；完整：True；SHA256：`c6e302704cf02611e03b6c82dd279242e1bf490686406d201bb907c803f9a07f`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "user_basic_information_table", "kind": "base", "block": null, "base_tables": ["user_basic_information_table"]}] | [] | [] |
| B2 | [{"alias": "ug", "kind": "derived", "block": "B1", "base_tables": ["user_basic_information_table"]}, {"alias": "f", "kind": "base", "block": null, "base_tables": ["product_favorites_table"]}, {"alias": "p", "kind": "base", "block": null, "base_tables": ["product_basic_information_table"]}] | [{"type": "INNER", "right": "product_favorites_table AS f", "on": "ug.\"User ID\" = f.\"User ID\"", "using": []}, {"type": "INNER", "right": "product_basic_information_table AS p", "on": "f.\"Product ID\" = p.\"Product ID\"", "using": []}] | ["ug.user_group", "p.\"Category Name\""] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B2 | COUNT(*) | [] | [] | True |
| B2 | COUNT(*) | [] | [] | True |
| B2 | COUNT(*) | [] | [] | True |


## S19

类别 `data`；来源 `query_db`；调用 `66e0296490274319827b2e683fde44ac`；状态 `success`。

```sql
-- Favorites by brand and user group
WITH user_groups AS (
  SELECT "User ID",
    CASE 
      WHEN "Membership Level" IN ('Diamond', 'Platinum') THEN 'High-Value'
      WHEN "Membership Level" = 'Regular' THEN 'Regular'
      ELSE 'Gold'
    END AS user_group
  FROM user_basic_information_table
)
SELECT ug.user_group, p."Brand Name", COUNT(*) AS fav_count,
  ROUND(COUNT(*) * 100.0 / SUM(COUNT(*)) OVER (PARTITION BY ug.user_group), 1) AS pct
FROM user_groups ug
JOIN product_favorites_table f ON ug."User ID" = f."User ID"
JOIN product_basic_information_table p ON f."Product ID" = p."Product ID"
GROUP BY ug.user_group, p."Brand Name"
ORDER BY ug.user_group, fav_count DESC
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-045/attempt-01/sql/S19.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-045/attempt-01/sql/S19.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-045/attempt-01/results/S19.rows.jsonl)；完整：True；SHA256：`0a9bddcafa8e2a53af1abbec08f57026d9b2c28674db5866740663a534b0f340`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "user_basic_information_table", "kind": "base", "block": null, "base_tables": ["user_basic_information_table"]}] | [] | [] |
| B2 | [{"alias": "ug", "kind": "derived", "block": "B1", "base_tables": ["user_basic_information_table"]}, {"alias": "f", "kind": "base", "block": null, "base_tables": ["product_favorites_table"]}, {"alias": "p", "kind": "base", "block": null, "base_tables": ["product_basic_information_table"]}] | [{"type": "INNER", "right": "product_favorites_table AS f", "on": "ug.\"User ID\" = f.\"User ID\"", "using": []}, {"type": "INNER", "right": "product_basic_information_table AS p", "on": "f.\"Product ID\" = p.\"Product ID\"", "using": []}] | ["ug.user_group", "p.\"Brand Name\""] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B2 | COUNT(*) | [] | [] | True |
| B2 | COUNT(*) | [] | [] | True |
| B2 | COUNT(*) | [] | [] | True |


## S20

类别 `data`；来源 `query_db`；调用 `633cdbba5cfd4b1a9cd63707ca6b17fa`；状态 `success`。

```sql
SELECT DISTINCT "Product Name", COUNT(*) AS cnt FROM product_basic_information_table GROUP BY "Product Name" ORDER BY cnt DESC
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-045/attempt-01/sql/S20.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-045/attempt-01/sql/S20.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-045/attempt-01/results/S20.rows.jsonl)；完整：True；SHA256：`3e237edfdbe76401d5cd76f27a71c05d180cb8fc2da170b1b5f8633e8759117c`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "product_basic_information_table", "kind": "base", "block": null, "base_tables": ["product_basic_information_table"]}] | [] | ["\"Product Name\""] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |


## S21

类别 `data`；来源 `query_db`；调用 `6e74e44724304825aa9efecd768e6953`；状态 `success`。

```sql
-- Search time distribution: hour of day, by user group
WITH user_groups AS (
  SELECT "User ID",
    CASE 
      WHEN "Membership Level" IN ('Diamond', 'Platinum') THEN 'High-Value'
      WHEN "Membership Level" = 'Regular' THEN 'Regular'
      ELSE 'Gold'
    END AS user_group
  FROM user_basic_information_table
)
SELECT ug.user_group, CAST(strftime('%H', s."Search Time") AS INTEGER) AS search_hour, COUNT(*) AS search_count
FROM user_groups ug
JOIN search_behavior_records_table s ON ug."User ID" = s."User ID"
GROUP BY ug.user_group, search_hour
ORDER BY ug.user_group, search_hour
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-045/attempt-01/sql/S21.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-045/attempt-01/sql/S21.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-045/attempt-01/results/S21.rows.jsonl)；完整：True；SHA256：`6b8600f7f873bb0c3cc906400fd743faf744c35be7fedc214b42099ce8721c14`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "user_basic_information_table", "kind": "base", "block": null, "base_tables": ["user_basic_information_table"]}] | [] | [] |
| B2 | [{"alias": "ug", "kind": "derived", "block": "B1", "base_tables": ["user_basic_information_table"]}, {"alias": "s", "kind": "base", "block": null, "base_tables": ["search_behavior_records_table"]}] | [{"type": "INNER", "right": "search_behavior_records_table AS s", "on": "ug.\"User ID\" = s.\"User ID\"", "using": []}] | ["ug.user_group", "CAST(STRFTIME('%H', s.\"Search Time\") AS INTEGER)"] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B2 | COUNT(*) | [] | [] | True |


## S22

类别 `data`；来源 `query_db`；调用 `ac796150375d45bfae1d74da49f9d128`；状态 `success`。

```sql
-- Check search time range and sample
SELECT "Search Time", "Search Keyword", "User ID" FROM search_behavior_records_table LIMIT 10
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-045/attempt-01/sql/S22.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-045/attempt-01/sql/S22.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-045/attempt-01/results/S22.rows.jsonl)；完整：True；SHA256：`6e446517a08038bd576b8696fbb077877e0477cea69dffece3af72ec74f6cbda`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "search_behavior_records_table", "kind": "base", "block": null, "base_tables": ["search_behavior_records_table"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |


## S23

类别 `data`；来源 `query_db`；调用 `8c9ab4d338c647ec93f37f0245408acc`；状态 `success`。

```sql
-- Search quality metrics by user group
WITH user_groups AS (
  SELECT "User ID",
    CASE 
      WHEN "Membership Level" IN ('Diamond', 'Platinum') THEN 'High-Value'
      WHEN "Membership Level" = 'Regular' THEN 'Regular'
      ELSE 'Gold'
    END AS user_group
  FROM user_basic_information_table
)
SELECT ug.user_group,
  COUNT(*) AS searches,
  ROUND(AVG(s."Input Duration"),1) AS avg_input_duration,
  ROUND(AVG(s."Viewed Result Count"),1) AS avg_viewed_results,
  ROUND(AVG(s."Clicked Result Count"),1) AS avg_clicked_results,
  ROUND(AVG(s."Search Conversion Rate"),3) AS avg_conv_rate,
  ROUND(AVG(s."Suggestion Count"),1) AS avg_suggestions,
  ROUND(SUM(s."No Result Search Count"),0) AS no_result_total,
  ROUND(AVG(s."Used Autocomplete" = 'Yes')*100,1) AS autocomplete_pct
FROM user_groups ug
JOIN search_behavior_records_table s ON ug."User ID" = s."User ID"
GROUP BY ug.user_group
ORDER BY ug.user_group
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-045/attempt-01/sql/S23.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-045/attempt-01/sql/S23.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-045/attempt-01/results/S23.rows.jsonl)；完整：True；SHA256：`19923c08d3aaeffd8ed9b4e81a1db9002f0a30014788fc2d407bb9ec44350eed`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "user_basic_information_table", "kind": "base", "block": null, "base_tables": ["user_basic_information_table"]}] | [] | [] |
| B2 | [{"alias": "ug", "kind": "derived", "block": "B1", "base_tables": ["user_basic_information_table"]}, {"alias": "s", "kind": "base", "block": null, "base_tables": ["search_behavior_records_table"]}] | [{"type": "INNER", "right": "search_behavior_records_table AS s", "on": "ug.\"User ID\" = s.\"User ID\"", "using": []}] | ["ug.user_group"] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B2 | COUNT(*) | [] | [] | True |
| B2 | AVG(s."Input Duration") | [{"table": "search_behavior_records_table", "column": "Input Duration"}] | [] | False |
| B2 | AVG(s."Viewed Result Count") | [{"table": "search_behavior_records_table", "column": "Viewed Result Count"}] | [] | False |
| B2 | AVG(s."Clicked Result Count") | [{"table": "search_behavior_records_table", "column": "Clicked Result Count"}] | [] | False |
| B2 | AVG(s."Search Conversion Rate") | [{"table": "search_behavior_records_table", "column": "Search Conversion Rate"}] | [] | False |
| B2 | AVG(s."Suggestion Count") | [{"table": "search_behavior_records_table", "column": "Suggestion Count"}] | [] | False |
| B2 | SUM(s."No Result Search Count") | [{"table": "search_behavior_records_table", "column": "No Result Search Count"}] | [] | False |
| B2 | AVG(s."Used Autocomplete" = 'Yes') | [{"table": "search_behavior_records_table", "column": "Used Autocomplete"}] | [] | False |


## S24

类别 `data`；来源 `query_db`；调用 `914b6c761f004ee2a98f0fe5aca4efca`；状态 `success`。

```sql
-- Browsing behavior metrics by user group
WITH user_groups AS (
  SELECT "User ID",
    CASE 
      WHEN "Membership Level" IN ('Diamond', 'Platinum') THEN 'High-Value'
      WHEN "Membership Level" = 'Regular' THEN 'Regular'
      ELSE 'Gold'
    END AS user_group
  FROM user_basic_information_table
)
SELECT ug.user_group,
  COUNT(*) AS browsing_events,
  ROUND(AVG(b."Time on Page"),1) AS avg_time_on_page,
  ROUND(AVG(b."View Count"),1) AS avg_view_count,
  ROUND(AVG(b."Scroll Distance"),1) AS avg_scroll,
  ROUND(AVG(b."Zoom Count"),1) AS avg_zoom_count,
  ROUND(AVG(b."Time on Detail Page"),1) AS avg_detail_time,
  ROUND(AVG(b."Time on Review Page"),1) AS avg_review_time,
  ROUND(SUM(b."Product Link Share Count")*1.0/COUNT(*),3) AS avg_share_per_view,
  ROUND(AVG(b."Has Swiped" = 'Yes')*100,1) AS swiped_pct,
  ROUND(AVG(b."Has Zoomed" = 'Yes')*100,1) AS zoomed_pct,
  ROUND(AVG(b."Viewed Specifications" = 'Yes')*100,1) AS specs_pct
FROM user_groups ug
JOIN browsing_behavior_records_table b ON ug."User ID" = b."User ID"
GROUP BY ug.user_group
ORDER BY ug.user_group
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-045/attempt-01/sql/S24.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-045/attempt-01/sql/S24.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-045/attempt-01/results/S24.rows.jsonl)；完整：True；SHA256：`87f8588075d6b338f96e01b43fcb8f4fe694d8577a15a2da7f9b265053c47d2b`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "user_basic_information_table", "kind": "base", "block": null, "base_tables": ["user_basic_information_table"]}] | [] | [] |
| B2 | [{"alias": "ug", "kind": "derived", "block": "B1", "base_tables": ["user_basic_information_table"]}, {"alias": "b", "kind": "base", "block": null, "base_tables": ["browsing_behavior_records_table"]}] | [{"type": "INNER", "right": "browsing_behavior_records_table AS b", "on": "ug.\"User ID\" = b.\"User ID\"", "using": []}] | ["ug.user_group"] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B2 | COUNT(*) | [] | [] | True |
| B2 | AVG(b."Time on Page") | [{"table": "browsing_behavior_records_table", "column": "Time on Page"}] | [] | False |
| B2 | AVG(b."View Count") | [{"table": "browsing_behavior_records_table", "column": "View Count"}] | [] | False |
| B2 | AVG(b."Scroll Distance") | [{"table": "browsing_behavior_records_table", "column": "Scroll Distance"}] | [] | False |
| B2 | AVG(b."Zoom Count") | [{"table": "browsing_behavior_records_table", "column": "Zoom Count"}] | [] | False |
| B2 | AVG(b."Time on Detail Page") | [{"table": "browsing_behavior_records_table", "column": "Time on Detail Page"}] | [] | False |
| B2 | AVG(b."Time on Review Page") | [{"table": "browsing_behavior_records_table", "column": "Time on Review Page"}] | [] | False |
| B2 | COUNT(*) | [] | [] | True |
| B2 | AVG(b."Has Swiped" = 'Yes') | [{"table": "browsing_behavior_records_table", "column": "Has Swiped"}] | [] | False |
| B2 | AVG(b."Has Zoomed" = 'Yes') | [{"table": "browsing_behavior_records_table", "column": "Has Zoomed"}] | [] | False |
| B2 | AVG(b."Viewed Specifications" = 'Yes') | [{"table": "browsing_behavior_records_table", "column": "Viewed Specifications"}] | [] | False |
| B2 | SUM(b."Product Link Share Count") | [{"table": "browsing_behavior_records_table", "column": "Product Link Share Count"}] | [] | False |


## S25

类别 `data`；来源 `query_db`；调用 `0805841bdc0347b5afc32f18d0a66b81`；状态 `success`。

```sql
-- Search behavior by day of week (0=Sunday, 6=Saturday)
WITH user_groups AS (
  SELECT "User ID",
    CASE 
      WHEN "Membership Level" IN ('Diamond', 'Platinum') THEN 'High-Value'
      WHEN "Membership Level" = 'Regular' THEN 'Regular'
      ELSE 'Gold'
    END AS user_group
  FROM user_basic_information_table
)
SELECT ug.user_group, CAST(strftime('%w', s."Search Time") AS INTEGER) AS day_of_week, COUNT(*) AS search_count
FROM user_groups ug
JOIN search_behavior_records_table s ON ug."User ID" = s."User ID"
GROUP BY ug.user_group, day_of_week
ORDER BY ug.user_group, day_of_week
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-045/attempt-01/sql/S25.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-045/attempt-01/sql/S25.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-045/attempt-01/results/S25.rows.jsonl)；完整：True；SHA256：`0cc4922af2ef2899a4f33c1fad7056671534e00f60556bbb2746c54d046dc905`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "user_basic_information_table", "kind": "base", "block": null, "base_tables": ["user_basic_information_table"]}] | [] | [] |
| B2 | [{"alias": "ug", "kind": "derived", "block": "B1", "base_tables": ["user_basic_information_table"]}, {"alias": "s", "kind": "base", "block": null, "base_tables": ["search_behavior_records_table"]}] | [{"type": "INNER", "right": "search_behavior_records_table AS s", "on": "ug.\"User ID\" = s.\"User ID\"", "using": []}] | ["ug.user_group", "CAST(STRFTIME('%w', s.\"Search Time\") AS INTEGER)"] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B2 | COUNT(*) | [] | [] | True |


## S26

类别 `data`；来源 `query_db`；调用 `85742e443aa543e6b1a2951fe5c600b9`；状态 `success`。

```sql
-- Search by month to see seasonal patterns
WITH user_groups AS (
  SELECT "User ID",
    CASE 
      WHEN "Membership Level" IN ('Diamond', 'Platinum') THEN 'High-Value'
      WHEN "Membership Level" = 'Regular' THEN 'Regular'
      ELSE 'Gold'
    END AS user_group
  FROM user_basic_information_table
)
SELECT ug.user_group, CAST(strftime('%m', s."Search Time") AS INTEGER) AS search_month, COUNT(*) AS search_count
FROM user_groups ug
JOIN search_behavior_records_table s ON ug."User ID" = s."User ID"
GROUP BY ug.user_group, search_month
ORDER BY ug.user_group, search_month
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-045/attempt-01/sql/S26.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-045/attempt-01/sql/S26.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-045/attempt-01/results/S26.rows.jsonl)；完整：True；SHA256：`a2579c175d38d9d00dab605cb2253099ae8745c42125658c813fe9f4c983ba09`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "user_basic_information_table", "kind": "base", "block": null, "base_tables": ["user_basic_information_table"]}] | [] | [] |
| B2 | [{"alias": "ug", "kind": "derived", "block": "B1", "base_tables": ["user_basic_information_table"]}, {"alias": "s", "kind": "base", "block": null, "base_tables": ["search_behavior_records_table"]}] | [{"type": "INNER", "right": "search_behavior_records_table AS s", "on": "ug.\"User ID\" = s.\"User ID\"", "using": []}] | ["ug.user_group", "CAST(STRFTIME('%m', s.\"Search Time\") AS INTEGER)"] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B2 | COUNT(*) | [] | [] | True |


## S27

类别 `data`；来源 `query_db`；调用 `764e7186ed1046eea864debe8e939ed6`；状态 `success`。

```sql
-- User demographics by membership level
WITH user_groups AS (
  SELECT "User ID",
    CASE 
      WHEN "Membership Level" IN ('Diamond', 'Platinum') THEN 'High-Value'
      WHEN "Membership Level" = 'Regular' THEN 'Regular'
      ELSE 'Gold'
    END AS user_group
  FROM user_basic_information_table
)
SELECT ug.user_group,
  COUNT(*) AS user_count,
  ROUND(AVG(u."Login Count"),1) AS avg_login_count,
  ROUND(AVG(u."Device count"),1) AS avg_device_count,
  ROUND(SUM(CASE WHEN u."Payment enabled" = 'Yes' THEN 1 ELSE 0 END)*100.0/COUNT(*),1) AS payment_pct,
  ROUND(SUM(CASE WHEN u."Real-name verification status" = 'Verified' THEN 1 ELSE 0 END)*100.0/COUNT(*),1) AS verified_pct
FROM user_groups ug
JOIN user_basic_information_table u ON ug."User ID" = u."User ID"
GROUP BY ug.user_group
ORDER BY ug.user_group
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-045/attempt-01/sql/S27.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-045/attempt-01/sql/S27.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-045/attempt-01/results/S27.rows.jsonl)；完整：True；SHA256：`58f342523a066dc27fae1fbe17ecaa5a532728031527f9dea67e66b456ae1328`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "user_basic_information_table", "kind": "base", "block": null, "base_tables": ["user_basic_information_table"]}] | [] | [] |
| B2 | [{"alias": "ug", "kind": "derived", "block": "B1", "base_tables": ["user_basic_information_table"]}, {"alias": "u", "kind": "base", "block": null, "base_tables": ["user_basic_information_table"]}] | [{"type": "INNER", "right": "user_basic_information_table AS u", "on": "ug.\"User ID\" = u.\"User ID\"", "using": []}] | ["ug.user_group"] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B2 | COUNT(*) | [] | [] | True |
| B2 | AVG(u."Login Count") | [{"table": "user_basic_information_table", "column": "Login Count"}] | [] | False |
| B2 | AVG(u."Device count") | [{"table": "user_basic_information_table", "column": "Device count"}] | [] | False |
| B2 | COUNT(*) | [] | [] | True |
| B2 | COUNT(*) | [] | [] | True |
| B2 | SUM(CASE WHEN u."Payment enabled" = 'Yes' THEN 1 ELSE 0 END) | [] | [{"table": "user_basic_information_table", "column": "Payment enabled"}] | False |
| B2 | SUM(CASE WHEN u."Real-name verification status" = 'Verified' THEN 1 ELSE 0 END) | [] | [{"table": "user_basic_information_table", "column": "Real-name verification status"}] | False |


## S28

类别 `data`；来源 `query_db`；调用 `8151e3c0b0a941328160752d41092c39`；状态 `success`。

```sql
-- Age group distribution by user group
WITH user_groups AS (
  SELECT "User ID",
    CASE 
      WHEN "Membership Level" IN ('Diamond', 'Platinum') THEN 'High-Value'
      WHEN "Membership Level" = 'Regular' THEN 'Regular'
      ELSE 'Gold'
    END AS user_group
  FROM user_basic_information_table
)
SELECT ug.user_group, u."Age group", COUNT(*) AS cnt
FROM user_groups ug
JOIN user_basic_information_table u ON ug."User ID" = u."User ID"
GROUP BY ug.user_group, u."Age group"
ORDER BY ug.user_group, cnt DESC
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-045/attempt-01/sql/S28.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-045/attempt-01/sql/S28.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-045/attempt-01/results/S28.rows.jsonl)；完整：True；SHA256：`08c4dddc4d3d0912355bc22def117fad577d900bff210c4fd6dc88cf3781c1c1`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "user_basic_information_table", "kind": "base", "block": null, "base_tables": ["user_basic_information_table"]}] | [] | [] |
| B2 | [{"alias": "ug", "kind": "derived", "block": "B1", "base_tables": ["user_basic_information_table"]}, {"alias": "u", "kind": "base", "block": null, "base_tables": ["user_basic_information_table"]}] | [{"type": "INNER", "right": "user_basic_information_table AS u", "on": "ug.\"User ID\" = u.\"User ID\"", "using": []}] | ["ug.user_group", "u.\"Age group\""] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B2 | COUNT(*) | [] | [] | True |


## S29

类别 `data`；来源 `query_db`；调用 `3ac2c638afd944bea6d1f119646b33b3`；状态 `success`。

```sql
-- Income level distribution by user group
WITH user_groups AS (
  SELECT "User ID",
    CASE 
      WHEN "Membership Level" IN ('Diamond', 'Platinum') THEN 'High-Value'
      WHEN "Membership Level" = 'Regular' THEN 'Regular'
      ELSE 'Gold'
    END AS user_group
  FROM user_basic_information_table
)
SELECT ug.user_group, u."Income level", COUNT(*) AS cnt
FROM user_groups ug
JOIN user_basic_information_table u ON ug."User ID" = u."User ID"
GROUP BY ug.user_group, u."Income level"
ORDER BY ug.user_group, cnt DESC
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-045/attempt-01/sql/S29.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-045/attempt-01/sql/S29.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-045/attempt-01/results/S29.rows.jsonl)；完整：True；SHA256：`d43a9a5d5f36682477c74112412ee63f344a8339da678fe8da9f061c338f5f1c`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "user_basic_information_table", "kind": "base", "block": null, "base_tables": ["user_basic_information_table"]}] | [] | [] |
| B2 | [{"alias": "ug", "kind": "derived", "block": "B1", "base_tables": ["user_basic_information_table"]}, {"alias": "u", "kind": "base", "block": null, "base_tables": ["user_basic_information_table"]}] | [{"type": "INNER", "right": "user_basic_information_table AS u", "on": "ug.\"User ID\" = u.\"User ID\"", "using": []}] | ["ug.user_group", "u.\"Income level\""] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B2 | COUNT(*) | [] | [] | True |


## S30

类别 `data`；来源 `query_db`；调用 `4273116582044c7e8039ea2355a81c35`；状态 `success`。

```sql
-- Browsing categories by user group (views)
WITH user_groups AS (
  SELECT "User ID",
    CASE 
      WHEN "Membership Level" IN ('Diamond', 'Platinum') THEN 'High-Value'
      WHEN "Membership Level" = 'Regular' THEN 'Regular'
      ELSE 'Gold'
    END AS user_group
  FROM user_basic_information_table
)
SELECT ug.user_group, p."Category Name", COUNT(*) AS views,
  ROUND(COUNT(*) * 100.0 / SUM(COUNT(*)) OVER (PARTITION BY ug.user_group), 1) AS pct
FROM user_groups ug
JOIN browsing_behavior_records_table b ON ug."User ID" = b."User ID"
JOIN product_basic_information_table p ON b."Product ID" = p."Product ID"
GROUP BY ug.user_group, p."Category Name"
ORDER BY ug.user_group, views DESC
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-045/attempt-01/sql/S30.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-045/attempt-01/sql/S30.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-045/attempt-01/results/S30.rows.jsonl)；完整：True；SHA256：`c4f069793920da52fcbf230f87ff4160731eff35593c8de484705b29eb9bf731`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "user_basic_information_table", "kind": "base", "block": null, "base_tables": ["user_basic_information_table"]}] | [] | [] |
| B2 | [{"alias": "ug", "kind": "derived", "block": "B1", "base_tables": ["user_basic_information_table"]}, {"alias": "b", "kind": "base", "block": null, "base_tables": ["browsing_behavior_records_table"]}, {"alias": "p", "kind": "base", "block": null, "base_tables": ["product_basic_information_table"]}] | [{"type": "INNER", "right": "browsing_behavior_records_table AS b", "on": "ug.\"User ID\" = b.\"User ID\"", "using": []}, {"type": "INNER", "right": "product_basic_information_table AS p", "on": "b.\"Product ID\" = p.\"Product ID\"", "using": []}] | ["ug.user_group", "p.\"Category Name\""] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B2 | COUNT(*) | [] | [] | True |
| B2 | COUNT(*) | [] | [] | True |
| B2 | COUNT(*) | [] | [] | True |


## S31

类别 `data`；来源 `query_db`；调用 `eb5a48bead1b460f83f4cfb54d858f1c`；状态 `success`。

```sql
-- Browsing brands by user group (views)
WITH user_groups AS (
  SELECT "User ID",
    CASE 
      WHEN "Membership Level" IN ('Diamond', 'Platinum') THEN 'High-Value'
      WHEN "Membership Level" = 'Regular' THEN 'Regular'
      ELSE 'Gold'
    END AS user_group
  FROM user_basic_information_table
)
SELECT ug.user_group, p."Brand Name", COUNT(*) AS views,
  ROUND(COUNT(*) * 100.0 / SUM(COUNT(*)) OVER (PARTITION BY ug.user_group), 1) AS pct
FROM user_groups ug
JOIN browsing_behavior_records_table b ON ug."User ID" = b."User ID"
JOIN product_basic_information_table p ON b."Product ID" = p."Product ID"
GROUP BY ug.user_group, p."Brand Name"
ORDER BY ug.user_group, views DESC
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-045/attempt-01/sql/S31.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-045/attempt-01/sql/S31.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-045/attempt-01/results/S31.rows.jsonl)；完整：True；SHA256：`515da9d787bfb7c90be1b0f1077889219e9aaae6f93a3b1d7360479384e74d6a`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "user_basic_information_table", "kind": "base", "block": null, "base_tables": ["user_basic_information_table"]}] | [] | [] |
| B2 | [{"alias": "ug", "kind": "derived", "block": "B1", "base_tables": ["user_basic_information_table"]}, {"alias": "b", "kind": "base", "block": null, "base_tables": ["browsing_behavior_records_table"]}, {"alias": "p", "kind": "base", "block": null, "base_tables": ["product_basic_information_table"]}] | [{"type": "INNER", "right": "browsing_behavior_records_table AS b", "on": "ug.\"User ID\" = b.\"User ID\"", "using": []}, {"type": "INNER", "right": "product_basic_information_table AS p", "on": "b.\"Product ID\" = p.\"Product ID\"", "using": []}] | ["ug.user_group", "p.\"Brand Name\""] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B2 | COUNT(*) | [] | [] | True |
| B2 | COUNT(*) | [] | [] | True |
| B2 | COUNT(*) | [] | [] | True |


## S32

类别 `data`；来源 `query_db`；调用 `04443eb56012497e9e02f08df288b40e`；状态 `success`。

```sql
-- Average price of browsed/favorited products by user group
WITH user_groups AS (
  SELECT "User ID",
    CASE 
      WHEN "Membership Level" IN ('Diamond', 'Platinum') THEN 'High-Value'
      WHEN "Membership Level" = 'Regular' THEN 'Regular'
      ELSE 'Gold'
    END AS user_group
  FROM user_basic_information_table
)
SELECT ug.user_group,
  ROUND(AVG(p."Price"),2) AS avg_browsed_price,
  ROUND(AVG(p."Sale Price"),2) AS avg_browsed_sale_price,
  ROUND(AVG(p."Original Price"),2) AS avg_browsed_original_price
FROM user_groups ug
JOIN browsing_behavior_records_table b ON ug."User ID" = b."User ID"
JOIN product_basic_information_table p ON b."Product ID" = p."Product ID"
GROUP BY ug.user_group
ORDER BY ug.user_group
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-045/attempt-01/sql/S32.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-045/attempt-01/sql/S32.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-045/attempt-01/results/S32.rows.jsonl)；完整：True；SHA256：`72c02b28a6edcdb200c33e50132c52aec6441880e14f470113f19286bb512548`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "user_basic_information_table", "kind": "base", "block": null, "base_tables": ["user_basic_information_table"]}] | [] | [] |
| B2 | [{"alias": "ug", "kind": "derived", "block": "B1", "base_tables": ["user_basic_information_table"]}, {"alias": "b", "kind": "base", "block": null, "base_tables": ["browsing_behavior_records_table"]}, {"alias": "p", "kind": "base", "block": null, "base_tables": ["product_basic_information_table"]}] | [{"type": "INNER", "right": "browsing_behavior_records_table AS b", "on": "ug.\"User ID\" = b.\"User ID\"", "using": []}, {"type": "INNER", "right": "product_basic_information_table AS p", "on": "b.\"Product ID\" = p.\"Product ID\"", "using": []}] | ["ug.user_group"] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B2 | AVG(p."Price") | [{"table": "product_basic_information_table", "column": "Price"}] | [] | False |
| B2 | AVG(p."Sale Price") | [{"table": "product_basic_information_table", "column": "Sale Price"}] | [] | False |
| B2 | AVG(p."Original Price") | [{"table": "product_basic_information_table", "column": "Original Price"}] | [] | False |


## S33

类别 `data`；来源 `query_db`；调用 `9648d83717f241c686b3d52e2a41a546`；状态 `success`。

```sql
-- Average price of favorited products by user group
WITH user_groups AS (
  SELECT "User ID",
    CASE 
      WHEN "Membership Level" IN ('Diamond', 'Platinum') THEN 'High-Value'
      WHEN "Membership Level" = 'Regular' THEN 'Regular'
      ELSE 'Gold'
    END AS user_group
  FROM user_basic_information_table
)
SELECT ug.user_group,
  ROUND(AVG(p."Price"),2) AS avg_fav_price,
  ROUND(AVG(p."Sale Price"),2) AS avg_fav_sale_price,
  ROUND(AVG(p."Original Price"),2) AS avg_fav_original_price
FROM user_groups ug
JOIN product_favorites_table f ON ug."User ID" = f."User ID"
JOIN product_basic_information_table p ON f."Product ID" = p."Product ID"
GROUP BY ug.user_group
ORDER BY ug.user_group
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-045/attempt-01/sql/S33.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-045/attempt-01/sql/S33.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-045/attempt-01/results/S33.rows.jsonl)；完整：True；SHA256：`7c11218200b9443e42dee479321e9bce1eea1aa209d77cacff81a04f9c33d5fc`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "user_basic_information_table", "kind": "base", "block": null, "base_tables": ["user_basic_information_table"]}] | [] | [] |
| B2 | [{"alias": "ug", "kind": "derived", "block": "B1", "base_tables": ["user_basic_information_table"]}, {"alias": "f", "kind": "base", "block": null, "base_tables": ["product_favorites_table"]}, {"alias": "p", "kind": "base", "block": null, "base_tables": ["product_basic_information_table"]}] | [{"type": "INNER", "right": "product_favorites_table AS f", "on": "ug.\"User ID\" = f.\"User ID\"", "using": []}, {"type": "INNER", "right": "product_basic_information_table AS p", "on": "f.\"Product ID\" = p.\"Product ID\"", "using": []}] | ["ug.user_group"] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B2 | AVG(p."Price") | [{"table": "product_basic_information_table", "column": "Price"}] | [] | False |
| B2 | AVG(p."Sale Price") | [{"table": "product_basic_information_table", "column": "Sale Price"}] | [] | False |
| B2 | AVG(p."Original Price") | [{"table": "product_basic_information_table", "column": "Original Price"}] | [] | False |


## S34

类别 `data`；来源 `query_db`；调用 `31dacf6a7b2f429e8f5009f43877e1dc`；状态 `success`。

```sql
-- Gender distribution by user group
WITH user_groups AS (
  SELECT "User ID",
    CASE 
      WHEN "Membership Level" IN ('Diamond', 'Platinum') THEN 'High-Value'
      WHEN "Membership Level" = 'Regular' THEN 'Regular'
      ELSE 'Gold'
    END AS user_group
  FROM user_basic_information_table
)
SELECT ug.user_group, u."Gender", COUNT(*) AS cnt
FROM user_groups ug
JOIN user_basic_information_table u ON ug."User ID" = u."User ID"
GROUP BY ug.user_group, u."Gender"
ORDER BY ug.user_group, cnt DESC
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-045/attempt-01/sql/S34.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-045/attempt-01/sql/S34.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-045/attempt-01/results/S34.rows.jsonl)；完整：True；SHA256：`a0521657046d61908131fb3f66d98fe8266216e6933af50c29963d3995f294cc`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "user_basic_information_table", "kind": "base", "block": null, "base_tables": ["user_basic_information_table"]}] | [] | [] |
| B2 | [{"alias": "ug", "kind": "derived", "block": "B1", "base_tables": ["user_basic_information_table"]}, {"alias": "u", "kind": "base", "block": null, "base_tables": ["user_basic_information_table"]}] | [{"type": "INNER", "right": "user_basic_information_table AS u", "on": "ug.\"User ID\" = u.\"User ID\"", "using": []}] | ["ug.user_group", "u.\"Gender\""] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B2 | COUNT(*) | [] | [] | True |


## S35

类别 `data`；来源 `query_db`；调用 `a1cbfccd6d2943deab6bfc06d497409b`；状态 `success`。

```sql
-- Occupation distribution by user group
WITH user_groups AS (
  SELECT "User ID",
    CASE 
      WHEN "Membership Level" IN ('Diamond', 'Platinum') THEN 'High-Value'
      WHEN "Membership Level" = 'Regular' THEN 'Regular'
      ELSE 'Gold'
    END AS user_group
  FROM user_basic_information_table
)
SELECT ug.user_group, u."Occupation", COUNT(*) AS cnt
FROM user_groups ug
JOIN user_basic_information_table u ON ug."User ID" = u."User ID"
GROUP BY ug.user_group, u."Occupation"
ORDER BY ug.user_group, cnt DESC
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-045/attempt-01/sql/S35.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-045/attempt-01/sql/S35.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-045/attempt-01/results/S35.rows.jsonl)；完整：True；SHA256：`4929e3b046dc0f41a40828589fb0c0584434323294a6879b2e4fedb1c3128c1b`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "user_basic_information_table", "kind": "base", "block": null, "base_tables": ["user_basic_information_table"]}] | [] | [] |
| B2 | [{"alias": "ug", "kind": "derived", "block": "B1", "base_tables": ["user_basic_information_table"]}, {"alias": "u", "kind": "base", "block": null, "base_tables": ["user_basic_information_table"]}] | [{"type": "INNER", "right": "user_basic_information_table AS u", "on": "ug.\"User ID\" = u.\"User ID\"", "using": []}] | ["ug.user_group", "u.\"Occupation\""] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B2 | COUNT(*) | [] | [] | True |


## S36

类别 `data`；来源 `query_db`；调用 `e0720d2e0f6b468082fac1617150e657`；状态 `success`。

```sql
-- Education level distribution by user group
WITH user_groups AS (
  SELECT "User ID",
    CASE 
      WHEN "Membership Level" IN ('Diamond', 'Platinum') THEN 'High-Value'
      WHEN "Membership Level" = 'Regular' THEN 'Regular'
      ELSE 'Gold'
    END AS user_group
  FROM user_basic_information_table
)
SELECT ug.user_group, u."Education Level", COUNT(*) AS cnt
FROM user_groups ug
JOIN user_basic_information_table u ON ug."User ID" = u."User ID"
GROUP BY ug.user_group, u."Education Level"
ORDER BY ug.user_group, cnt DESC
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-045/attempt-01/sql/S36.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-045/attempt-01/sql/S36.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-045/attempt-01/results/S36.rows.jsonl)；完整：True；SHA256：`7d62677e1f11237031d643fa9468e4a99a23be7bde5ddfa72cb982d701675e4b`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "user_basic_information_table", "kind": "base", "block": null, "base_tables": ["user_basic_information_table"]}] | [] | [] |
| B2 | [{"alias": "ug", "kind": "derived", "block": "B1", "base_tables": ["user_basic_information_table"]}, {"alias": "u", "kind": "base", "block": null, "base_tables": ["user_basic_information_table"]}] | [{"type": "INNER", "right": "user_basic_information_table AS u", "on": "ug.\"User ID\" = u.\"User ID\"", "using": []}] | ["ug.user_group", "u.\"Education Level\""] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B2 | COUNT(*) | [] | [] | True |


## S37

类别 `data`；来源 `query_db`；调用 `d898df175b1f4229ac1e39c7f9857590`；状态 `success`。

```sql
-- Search keyword preferences detailed: top keywords per user group with percentages
WITH user_groups AS (
  SELECT "User ID",
    CASE 
      WHEN "Membership Level" IN ('Diamond', 'Platinum') THEN 'High-Value'
      WHEN "Membership Level" = 'Regular' THEN 'Regular'
      ELSE 'Gold'
    END AS user_group
  FROM user_basic_information_table
),
keyword_stats AS (
  SELECT ug.user_group, s."Search Keyword", COUNT(*) AS cnt,
    ROUND(COUNT(*) * 100.0 / SUM(COUNT(*)) OVER (PARTITION BY ug.user_group), 1) AS pct_in_group
  FROM user_groups ug
  JOIN search_behavior_records_table s ON ug."User ID" = s."User ID"
  GROUP BY ug.user_group, s."Search Keyword"
)
SELECT * FROM keyword_stats
WHERE user_group IN ('High-Value', 'Regular')
ORDER BY user_group, cnt DESC
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-045/attempt-01/sql/S37.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-045/attempt-01/sql/S37.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-045/attempt-01/results/S37.rows.jsonl)；完整：True；SHA256：`6c178d63d65dbccc2a134acb2719722236d851aab2bc46d9cd8de4d17c7bf33f`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "user_basic_information_table", "kind": "base", "block": null, "base_tables": ["user_basic_information_table"]}] | [] | [] |
| B2 | [{"alias": "ug", "kind": "derived", "block": "B1", "base_tables": ["user_basic_information_table"]}, {"alias": "s", "kind": "base", "block": null, "base_tables": ["search_behavior_records_table"]}] | [{"type": "INNER", "right": "search_behavior_records_table AS s", "on": "ug.\"User ID\" = s.\"User ID\"", "using": []}] | ["ug.user_group", "s.\"Search Keyword\""] |
| B3 | [{"alias": "keyword_stats", "kind": "derived", "block": "B2", "base_tables": ["search_behavior_records_table", "user_basic_information_table"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B2 | COUNT(*) | [] | [] | True |
| B2 | COUNT(*) | [] | [] | True |
| B2 | COUNT(*) | [] | [] | True |

