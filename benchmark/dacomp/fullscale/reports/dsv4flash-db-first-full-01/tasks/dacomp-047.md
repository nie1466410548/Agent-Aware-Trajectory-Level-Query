# dacomp-047

To adjust replenishment decisions, based on the interrelationships between vegetable categ…

运行：已提交。官方未评分。全部 SQL 尝试/成功 57/56；数据 SQL 55/54；Python 10 次。

完整原题：

To adjust replenishment decisions, based on the interrelationships between vegetable categories and single-item sales volumes and their seasonal characteristics, please recommend three fruit-and-vegetable combinations for replenishment in July 2023.

| 表 | 行数 | 列数 |
| --- | --- | --- |
| product_information | 251 | 4 |
| product_loss | 251 | 3 |
| purchase_price | 55982 | 3 |
| sales_records | 878503 | 7 |


实际路线（分析者依据 SQL/源码概括，不代表 Agent 自述）：SQL 连接蔬菜类别、销量与价格 → Python 再汇总季节性并合并补货指标 → 推荐七月组合。

数据库大小：135,073,792 字节。

## 数据 SQL

| SQL | 状态 | 基础表 | Join 输入/类型 | GROUP BY | 聚合表达式 | 结果行数 | 数据库 ms |
| --- | --- | --- | --- | --- | --- | --- | --- |
| [S3/Q1](#s3) | success | ["product_information"] | 0 / {} | [] | [] | 20 | 0.352 |
| [S4/Q2](#s4) | success | ["sales_records"] | 0 / {} | [] | [] | 10 | 0.339 |
| [S5/Q3](#s5) | success | ["product_information"] | 0 / {} | ["\"Category Code\"", "\"Category Name\""] | ["COUNT(DISTINCT \"Item Code\")"] | 6 | 0.527 |
| [S6/Q4](#s6) | success | ["sales_records"] | 0 / {} | [] | ["MIN(\"Sales Date\")", "MAX(\"Sales Date\")", "COUNT(*)", "COUNT(DISTINCT \"Item Code\")"] | 1 | 201.696 |
| [S7/Q5](#s7) | success | ["purchase_price"] | 0 / {} | [] | ["MIN(Date)", "MAX(Date)", "COUNT(*)", "COUNT(DISTINCT \"Item Code\")"] | 1 | 12.891 |
| [S8/Q6](#s8) | success | ["product_information", "sales_records"] | 2 / {'INNER': 1} | ["STRFTIME('%Y-%m', \"Sales Date\")", "pi.\"Category Name\""] | ["COUNT(DISTINCT s.\"Item Code\")", "SUM(s.\"Sales volume (kg)\")", "SUM(s.\"Sales volume (kg)\" * s.\"Unit price (yuan/kg)\")"] | 216 | 1503.305 |
| [S9/Q7](#s9) | success | ["product_information", "sales_records"] | 2 / {'INNER': 1} | ["pi.\"Category Name\"", "STRFTIME('%m', \"Sales Date\")"] | ["SUM(s.\"Sales volume (kg)\")"] | 72 | 1204.058 |
| [S10/Q8](#s10) | success | ["product_information", "sales_records"] | 2 / {'INNER': 1} | ["STRFTIME('%Y-%m-%d', \"Sales Date\")", "pi.\"Category Name\"", "cat", "SUBSTRING(d, 6, 2)"] | ["SUM(s.\"Sales volume (kg)\")", "AVG(vol)"] | 72 | 1296.556 |
| [S11/Q9](#s11) | success | ["sales_records"] | 0 / {} | ["STRFTIME('%Y', \"Sales Date\")", "STRFTIME('%m', \"Sales Date\")"] | ["COUNT(DISTINCT \"Sales Date\")"] | 36 | 1067.212 |
| [S12/Q10](#s12) | success | ["product_information", "sales_records"] | 2 / {'INNER': 1} | ["s.\"Item Code\"", "pi.\"Item Name\"", "pi.\"Category Name\"", "STRFTIME('%m', s.\"Sales Date\")"] | ["SUM(s.\"Sales volume (kg)\")"] | 30 | 397.505 |
| [S13/Q11](#s13) | success | ["product_information", "sales_records"] | 2 / {'INNER': 1} | ["s.\"Item Code\"", "pi.\"Item Name\"", "pi.\"Category Name\""] | ["COUNT(DISTINCT s.\"Sales Date\")", "SUM(s.\"Sales volume (kg)\")", "AVG(s.\"Unit price (yuan/kg)\")", "SUM(CASE WHEN STRFTIME('%m', s.\"Sales Date\") = '07' THEN s.\"Sales volume (kg)\" ELSE 0 END)"] | 30 | 1545.746 |
| [S14/Q12](#s14) | success | ["sales_records"] | 0 / {} | [] | ["COUNT(DISTINCT STRFTIME('%Y-%m-%d', \"Sales Date\") \|\| ' ' \|\| \"Time of sale (code scan)\")", "COUNT(*)", "COUNT(DISTINCT STRFTIME('%Y-%m-%d', \"Sales Date\") \|\| ' ' \|\| \"Time of sale (code scan)\")", "COUNT(*)"] | 1 | 898.494 |
| [S15/Q13](#s15) | success | ["sales_records"] | 0 / {} | ["STRFTIME('%Y-%m-%d', \"Sales Date\") \|\| ' ' \|\| \"Time of sale (code scan)\"", "\"Item Code\"", "basket_id", "basket_size"] | ["COUNT(*)", "COUNT(*)"] | 2 | 493.419 |
| [S16/Q14](#s16) | success | ["product_information", "sales_records"] | 2 / {'INNER': 1} | ["pi.\"Category Name\""] | ["AVG(CASE WHEN STRFTIME('%m', s.\"Sales Date\") = '07' THEN s.\"Sales volume (kg)\" END)", "AVG(s.\"Sales volume (kg)\")", "AVG(CASE WHEN STRFTIME('%m', s.\"Sales Date\") = '07' THEN s.\"Sales volume (kg)\" END)", "AVG(s.\"Sales volume (kg)\")"] | 6 | 1010.434 |
| [S17/Q15](#s17) | success | ["product_information", "sales_records"] | 2 / {'INNER': 1} | ["STRFTIME('%Y-%m-%d', s.\"Sales Date\")", "pi.\"Category Name\""] | ["SUM(s.\"Sales volume (kg)\")"] | 30 | 1047.505 |
| [S18/Q16](#s18) | success | ["product_information", "sales_records"] | 2 / {'INNER': 1} | ["s.\"Item Code\"", "pi.\"Item Name\"", "pi.\"Category Name\"", "STRFTIME('%Y', s.\"Sales Date\")", "STRFTIME('%m', s.\"Sales Date\")"] | ["SUM(s.\"Sales volume (kg)\")", "SUM(s.\"Sales volume (kg)\" * s.\"Unit price (yuan/kg)\")"] | 2514 | 2049.882 |
| [S19/Q17](#s19) | success | ["product_information", "sales_records"] | 2 / {'INNER': 1} | ["STRFTIME('%Y-%m-%d', \"Sales Date\")", "pi.\"Category Name\""] | ["SUM(\"Sales volume (kg)\")"] | 6474 | 1305.888 |
| [S20/Q18](#s20) | success | ["product_information", "sales_records"] | 2 / {'INNER': 1} | ["STRFTIME('%Y-%m-%d', \"Sales Date\")", "pi.\"Category Name\""] | ["SUM(\"Sales volume (kg)\")"] | 6474 | 1301.585 |
| [S21/Q19](#s21) | success | ["product_information", "sales_records"] | 2 / {'INNER': 1} | ["STRFTIME('%Y-%m-%d', \"Sales Date\")", "pi.\"Category Name\""] | ["SUM(\"Sales volume (kg)\")"] | 6474 | 1297.642 |
| [S22/Q20](#s22) | success | ["product_information", "sales_records"] | 2 / {'INNER': 1} | ["STRFTIME('%Y-%m-%d', \"Sales Date\")", "pi.\"Category Name\""] | ["SUM(\"Sales volume (kg)\")"] | 6474 | 1295.442 |
| [S23/Q21](#s23) | success | ["product_information", "sales_records"] | 2 / {'INNER': 1} | ["STRFTIME('%Y-%m-%d', \"Sales Date\")", "pi.\"Category Name\""] | ["SUM(\"Sales volume (kg)\")"] | 6474 | 1295.662 |
| [S24/Q22](#s24) | success | ["product_information", "sales_records"] | 2 / {'INNER': 1} | ["s.\"Item Code\"", "pi.\"Item Name\"", "pi.\"Category Name\"", "STRFTIME('%m', s.\"Sales Date\")"] | ["SUM(s.\"Sales volume (kg)\")"] | 1558 | 1577.773 |
| [S25/Q23](#s25) | success | ["product_information", "sales_records"] | 2 / {'INNER': 1} | ["s.\"Item Code\"", "pi.\"Item Name\"", "pi.\"Category Name\"", "STRFTIME('%m', s.\"Sales Date\")"] | ["COUNT(DISTINCT s.\"Sales Date\")", "SUM(s.\"Sales volume (kg)\")"] | 1558 | 1625.772 |
| [S26/Q24](#s26) | success | ["product_information", "purchase_price"] | 2 / {'INNER': 1} | ["pp.\"Item Code\"", "pi.\"Item Name\"", "pi.\"Category Name\""] | ["AVG(pp.\"Wholesale price (yuan/kg)\")", "AVG(CASE WHEN STRFTIME('%m', pp.\"Date\") = '07' THEN pp.\"Wholesale price (yuan/kg)\" END)"] | 251 | 76.22 |
| [S27/Q25](#s27) | success | ["product_information", "sales_records"] | 2 / {'INNER': 1} | ["s.\"Item Code\"", "pi.\"Item Name\"", "pi.\"Category Name\""] | ["AVG(s.\"Unit price (yuan/kg)\")", "AVG(CASE WHEN STRFTIME('%m', s.\"Sales Date\") = '07' THEN s.\"Unit price (yuan/kg)\" END)", "SUM(CASE WHEN STRFTIME('%m', s.\"Sales Date\") = '07' THEN s.\"Sales volume (kg)\" END)"] | 30 | 1714.094 |
| [S28/Q26](#s28) | success | ["product_loss"] | 0 / {} | [] | [] | 20 | 0.354 |
| [S29/Q27](#s29) | success | ["product_information", "purchase_price", "sales_records"] | 3 / {'INNER': 1, 'LEFT': 1} | ["s.\"Item Code\"", "pi.\"Item Name\"", "pi.\"Category Name\""] | ["AVG(s.\"Unit price (yuan/kg)\")", "AVG(pp.\"Wholesale price (yuan/kg)\")", "SUM(CASE WHEN STRFTIME('%m', s.\"Sales Date\") = '07' THEN s.\"Sales volume (kg)\" END)", "AVG(s.\"Unit price (yuan/kg)\")", "AVG(pp.\"Wholesale price (yuan/kg)\")"] | 30 | 164341.225 |
| [S30/Q28](#s30) | success | ["product_information", "sales_records"] | 2 / {'INNER': 1} | ["pi.\"Item Name\"", "STRFTIME('%Y', s.\"Sales Date\")"] | ["SUM(s.\"Sales volume (kg)\")"] | 52 | 332.035 |
| [S31/Q29](#s31) | success | ["product_information", "sales_records"] | 2 / {'INNER': 1} | ["pi.\"Item Name\"", "STRFTIME('%Y-%m', s.\"Sales Date\")"] | ["SUM(s.\"Sales volume (kg)\")", "COUNT(DISTINCT s.\"Sales Date\")"] | 90 | 182.198 |
| [S32/Q30](#s32) | success | ["product_information", "product_loss"] | 2 / {'INNER': 1} | [] | [] | 17 | 0.644 |
| [S33/Q31](#s33) | success | ["product_information", "sales_records"] | 2 / {'INNER': 1} | ["STRFTIME('%Y-%m-%d', s.\"Sales Date\")", "s.\"Item Code\"", "pi.\"Item Name\"", "pi.\"Category Name\""] | ["SUM(s.\"Sales volume (kg)\")"] | 11493 | 860.006 |
| [S34/Q32](#s34) | success | ["product_information", "sales_records"] | 2 / {'INNER': 1} | ["STRFTIME('%Y-%m-%d', s.\"Sales Date\")", "s.\"Item Code\"", "pi.\"Item Name\""] | ["SUM(s.\"Sales volume (kg)\")"] | 11493 | 795.25 |
| [S35/Q33](#s35) | success | ["product_information", "sales_records"] | 2 / {'INNER': 1} | ["STRFTIME('%Y-%m-%d', s.\"Sales Date\")", "s.\"Item Code\"", "pi.\"Item Name\""] | ["SUM(s.\"Sales volume (kg)\")"] | 11493 | 791.921 |
| [S36/Q34](#s36) | success | ["product_information", "sales_records"] | 2 / {'INNER': 1} | ["s.\"Item Code\"", "pi.\"Item Name\"", "STRFTIME('%m', s.\"Sales Date\")"] | ["COUNT(DISTINCT s.\"Sales Date\")", "SUM(s.\"Sales volume (kg)\")"] | 174 | 808.525 |
| [S37/Q35](#s37) | success | ["product_information", "sales_records"] | 2 / {'INNER': 1} | ["s.\"Item Code\"", "pi.\"Item Name\"", "pi.\"Category Name\""] | ["SUM(CASE WHEN STRFTIME('%m', s.\"Sales Date\") = '07' THEN s.\"Sales volume (kg)\" ELSE 0 END)", "SUM(s.\"Sales volume (kg)\")", "AVG(s.\"Unit price (yuan/kg)\")", "SUM(CASE WHEN STRFTIME('%m', s.\"Sales Date\") = '07' THEN s.\"Sales volume (kg)\" * s.\"Unit price (yuan/kg)\" ELSE 0 END)", "COUNT(DISTINCT s.\"Sales Date\")"] | 15 | 1001.838 |
| [S38/Q36](#s38) | success | ["product_loss"] | 0 / {} | [] | [] | 15 | 0.37 |
| [S39/Q37](#s39) | success | ["purchase_price", "sales_records"] | 2 / {'LEFT': 1} | ["s.\"Item Code\""] | ["AVG(s.\"Unit price (yuan/kg)\")", "AVG(pp.\"Wholesale price (yuan/kg)\")"] | 15 | 104133.862 |
| [S40/Q38](#s40) | success | ["product_information", "sales_records"] | 2 / {'INNER': 1} | ["s.\"Item Code\"", "pi.\"Item Name\"", "STRFTIME('%m', s.\"Sales Date\")"] | ["COUNT(DISTINCT s.\"Sales Date\")", "SUM(s.\"Sales volume (kg)\")"] | 174 | 806.131 |
| [S41/Q39](#s41) | success | ["product_information", "sales_records"] | 2 / {'INNER': 1} | ["pi.\"Item Name\"", "STRFTIME('%Y-%m', s.\"Sales Date\")"] | ["SUM(s.\"Sales volume (kg)\")", "SUM(s.\"Sales volume (kg)\")", "COUNT(DISTINCT s.\"Sales Date\")"] | 46 | 124.778 |
| [S42/Q40](#s42) | success | ["product_information", "sales_records"] | 2 / {'INNER': 1} | ["pi.\"Item Name\"", "STRFTIME('%Y', s.\"Sales Date\")"] | ["SUM(s.\"Sales volume (kg)\")", "COUNT(DISTINCT s.\"Sales Date\")"] | 26 | 300.822 |
| [S43/Q41](#s43) | success | ["product_information", "sales_records"] | 2 / {'INNER': 1} | ["pi.\"Item Name\""] | ["COUNT(DISTINCT STRFTIME('%Y', s.\"Sales Date\"))", "SUM(CASE WHEN s.\"Sales Date\" >= '2023-01-01' THEN s.\"Sales volume (kg)\" ELSE 0 END)", "SUM(CASE WHEN s.\"Sales Date\" >= '2022-01-01' AND s.\"Sales Date\" < '2023-01-01' THEN s.\"Sales volume (kg)\" ELSE 0 END)"] | 12 | 1302.066 |
| [S44/Q42](#s44) | success | ["product_information", "sales_records"] | 2 / {'INNER': 1} | ["pi.\"Item Name\"", "STRFTIME('%Y-%m', s.\"Sales Date\")"] | ["SUM(s.\"Sales volume (kg)\")"] | 60 | 1088.095 |
| [S45/Q43](#s45) | success | ["product_information", "sales_records"] | 2 / {'INNER': 1} | ["s.\"Item Code\"", "pi.\"Item Name\"", "pi.\"Category Name\""] | ["SUM(CASE WHEN s.\"Sales Date\" >= '2023-01-01' THEN s.\"Sales volume (kg)\" ELSE 0 END)", "SUM(CASE WHEN STRFTIME('%m', s.\"Sales Date\") = '07' AND STRFTIME('%Y', s.\"Sales Date\") = '2022' THEN s.\"Sales volume (kg)\" ELSE 0 END)", "SUM(CASE WHEN STRFTIME('%m', s.\"Sales Date\") = '07' AND STRFTIME('%Y', s.\"Sales Date\") = '2021' THEN s.\"Sales volume (kg)\" ELSE 0 END)", "SUM(CASE WHEN STRFTIME('%m', s.\"Sales Date\") = '07' AND STRFTIME('%Y', s.\"Sales Date\") = '2020' THEN s.\"Sales volume (kg)\" ELSE 0 END)"] | 40 | 368.699 |
| [S46/Q44](#s46) | success | ["product_information", "sales_records"] | 2 / {'INNER': 1} | ["pi.\"Item Name\"", "STRFTIME('%Y', s.\"Sales Date\")"] | ["SUM(s.\"Sales volume (kg)\")"] | 15 | 1047.823 |
| [S47/Q45](#s47) | success | ["product_information", "sales_records"] | 2 / {'INNER': 1} | ["pi.\"Item Name\"", "STRFTIME('%Y-%m', s.\"Sales Date\")"] | ["SUM(s.\"Sales volume (kg)\")"] | 65 | 132.376 |
| [S48/Q46](#s48) | success | ["product_information", "sales_records"] | 2 / {'INNER': 1} | ["pi.\"Item Name\"", "STRFTIME('%Y', s.\"Sales Date\")"] | ["SUM(s.\"Sales volume (kg)\")"] | 7 | 255.966 |
| [S49/Q47](#s49) | success | ["product_information", "sales_records"] | 2 / {'INNER': 1} | ["pi.\"Item Name\"", "STRFTIME('%Y-%m', s.\"Sales Date\")"] | ["SUM(s.\"Sales volume (kg)\")", "COUNT(DISTINCT s.\"Sales Date\")"] | 105 | 243.668 |
| [S50/Q48](#s50) | success | ["product_information", "sales_records"] | 2 / {'INNER': 1} | ["pi.\"Item Name\""] | ["SUM(CASE WHEN STRFTIME('%m', s.\"Sales Date\") = '07' AND STRFTIME('%Y', s.\"Sales Date\") = '2022' THEN s.\"Sales volume (kg)\" ELSE 0 END)", "SUM(CASE WHEN STRFTIME('%m', s.\"Sales Date\") = '07' AND STRFTIME('%Y', s.\"Sales Date\") = '2021' THEN s.\"Sales volume (kg)\" ELSE 0 END)", "SUM(CASE WHEN STRFTIME('%m', s.\"Sales Date\") = '07' AND STRFTIME('%Y', s.\"Sales Date\") = '2020' THEN s.\"Sales volume (kg)\" ELSE 0 END)"] | 19 | 1510.85 |
| [S51/Q49](#s51) | success | ["product_information", "sales_records"] | 2 / {'INNER': 1} | ["pi.\"Item Name\"", "STRFTIME('%Y-%m', s.\"Sales Date\")"] | ["SUM(s.\"Sales volume (kg)\")", "COUNT(DISTINCT s.\"Sales Date\")", "SUM(s.\"Sales volume (kg)\")"] | 372 | 376.662 |
| [S52/Q50](#s52) | success | ["product_information", "sales_records"] | 2 / {'INNER': 1} | ["pi.\"Item Name\"", "STRFTIME('%m', s.\"Sales Date\")"] | ["SUM(s.\"Sales volume (kg)\")", "COUNT(DISTINCT s.\"Sales Date\")"] | 93 | 195.816 |
| [S53/Q51](#s53) | success | ["product_information", "sales_records"] | 2 / {'INNER': 1} | ["pi.\"Item Name\"", "STRFTIME('%Y', s.\"Sales Date\")"] | ["SUM(s.\"Sales volume (kg)\")"] | 10 | 1051.429 |
| [S54/Q52](#s54) | failed | ["product_information", "sales_records"] | 2 / {'INNER': 1} | ["pi.\"Item Name\"", "STRFTIME('%m', s.\"Sales Date\")"] | ["AVG(CASE WHEN STRFTIME('%Y', s.\"Sales Date\") >= '2022' THEN s.\"Sales volume (kg)\" / COUNT(DISTINCT s.\"Sales Date\") END)", "COUNT(DISTINCT s.\"Sales Date\")"] | unknown | 未取得；调用总时长 0.227 ms |
| [S55/Q53](#s55) | success | ["product_information", "sales_records"] | 2 / {'INNER': 1} | ["pi.\"Item Name\"", "STRFTIME('%m', s.\"Sales Date\")"] | ["SUM(s.\"Sales volume (kg)\")", "COUNT(DISTINCT s.\"Sales Date\")"] | 90 | 196.39 |
| [S56/Q54](#s56) | success | ["product_information", "sales_records"] | 2 / {'INNER': 1} | ["pi.\"Item Name\"", "STRFTIME('%m', s.\"Sales Date\")"] | ["SUM(s.\"Sales volume (kg)\")", "COUNT(DISTINCT s.\"Sales Date\")"] | 90 | 230.291 |
| [S57/Q55](#s57) | success | ["product_information", "sales_records"] | 2 / {'INNER': 1} | ["STRFTIME('%Y-%m-%d', \"Sales Date\")", "pi.\"Category Name\""] | ["SUM(\"Sales volume (kg)\")"] | 6474 | 1356.522 |


## 元数据和设置

| SQL | 类别 | 状态 | 内容 |
| --- | --- | --- | --- |
| S1 | connection_setup | success | PRAGMA query_only=ON |
| S2 | metadata | success | SELECT name,sql FROM sqlite_master WHERE type='table' ORDER BY name |


## Python 与执行位置

人工源码审查：**database_first_violation**。Python 对单品月销量再次按商品汇总，计算七月与总体均值并合并季节性、损耗和利润结果。这些分组、连接及比率计算可在 SQL 内执行。相关分析与图表另行评价。 [证据](../reviews/dacomp-047.json)。

P1：Compute category daily sales correlation matrix and item-level July seasonality analysis. This requires statistical functions (correlation matrix, pivoting) and visualization that are better suited to Python than SQLite.

[源码](../../../runs/dsv4flash-db-first-full-01/dacomp-047/attempt-01/python/P1.py)；[输出](../../../runs/dsv4flash-db-first-full-01/dacomp-047/attempt-01/python/P1.stdout)；[错误](../../../runs/dsv4flash-db-first-full-01/dacomp-047/attempt-01/python/P1.stderr)。检出需人工核验的 SQL 可实现操作：groupby(, .merge(, .query(, sort_values(；不能仅凭理由判为合规。

P2：Check the structure of the returned data to debug column names.

[源码](../../../runs/dsv4flash-db-first-full-01/dacomp-047/attempt-01/python/P2.py)；[输出](../../../runs/dsv4flash-db-first-full-01/dacomp-047/attempt-01/python/P2.stdout)；[错误](../../../runs/dsv4flash-db-first-full-01/dacomp-047/attempt-01/python/P2.stderr)。检出需人工核验的 SQL 可实现操作：.query(；不能仅凭理由判为合规。

P3：Check the structure of db.rows output - it returns lists, not dicts. Need to understand the format.

[源码](../../../runs/dsv4flash-db-first-full-01/dacomp-047/attempt-01/python/P3.py)；[输出](../../../runs/dsv4flash-db-first-full-01/dacomp-047/attempt-01/python/P3.stdout)；[错误](../../../runs/dsv4flash-db-first-full-01/dacomp-047/attempt-01/python/P3.stderr)。检出需人工核验的 SQL 可实现操作：.query(；不能仅凭理由判为合规。

P4：Compute category daily sales correlation matrix and item-level July seasonality analysis. Rows are returned as lists, need to use column names to build DataFrame.

[源码](../../../runs/dsv4flash-db-first-full-01/dacomp-047/attempt-01/python/P4.py)；[输出](../../../runs/dsv4flash-db-first-full-01/dacomp-047/attempt-01/python/P4.stdout)；[错误](../../../runs/dsv4flash-db-first-full-01/dacomp-047/attempt-01/python/P4.stderr)。检出需人工核验的 SQL 可实现操作：groupby(, .merge(, .query(, sort_values(；不能仅凭理由判为合规。

P5：Compute item-level daily sales correlation matrix to identify interrelationships (complementary/substitute patterns) between top July items. This requires statistical correlation computation and visualization better done in Python.

[源码](../../../runs/dsv4flash-db-first-full-01/dacomp-047/attempt-01/python/P5.py)；[输出](../../../runs/dsv4flash-db-first-full-01/dacomp-047/attempt-01/python/P5.stdout)；[错误](../../../runs/dsv4flash-db-first-full-01/dacomp-047/attempt-01/python/P5.stderr)。检出需人工核验的 SQL 可实现操作：groupby(, .merge(, .query(, sort_values(；不能仅凭理由判为合规。

P6：Fix the correlation unstacking issue and complete the item-level seasonality analysis.

[源码](../../../runs/dsv4flash-db-first-full-01/dacomp-047/attempt-01/python/P6.py)；[输出](../../../runs/dsv4flash-db-first-full-01/dacomp-047/attempt-01/python/P6.stdout)；[错误](../../../runs/dsv4flash-db-first-full-01/dacomp-047/attempt-01/python/P6.stderr)。检出需人工核验的 SQL 可实现操作：groupby(, .merge(, .query(, sort_values(；不能仅凭理由判为合规。

P7：Build a comprehensive analysis for July 2023 replenishment recommendations, combining seasonality, correlations, profit margins, and loss rates to identify the best 3 combinations.

[源码](../../../runs/dsv4flash-db-first-full-01/dacomp-047/attempt-01/python/P7.py)；[输出](../../../runs/dsv4flash-db-first-full-01/dacomp-047/attempt-01/python/P7.stdout)；[错误](../../../runs/dsv4flash-db-first-full-01/dacomp-047/attempt-01/python/P7.stderr)。检出需人工核验的 SQL 可实现操作：groupby(, .merge(, .query(, sort_values(；不能仅凭理由判为合规。

P8：Analyze the full 2023 monthly trend for all candidate items to identify which items are actively selling and growing into July 2023. This requires pivoting and trend analysis beyond simple SQL aggregation.

[源码](../../../runs/dsv4flash-db-first-full-01/dacomp-047/attempt-01/python/P8.py)；[输出](../../../runs/dsv4flash-db-first-full-01/dacomp-047/attempt-01/python/P8.stdout)；[错误](../../../runs/dsv4flash-db-first-full-01/dacomp-047/attempt-01/python/P8.stderr)。检出需人工核验的 SQL 可实现操作：.query(, sort_values(；不能仅凭理由判为合规。

P9：Examine the full monthly seasonal patterns of the remaining top 2023 candidates to determine which items have July peaks suitable for replenishment.

[源码](../../../runs/dsv4flash-db-first-full-01/dacomp-047/attempt-01/python/P9.py)；[输出](../../../runs/dsv4flash-db-first-full-01/dacomp-047/attempt-01/python/P9.stdout)；[错误](../../../runs/dsv4flash-db-first-full-01/dacomp-047/attempt-01/python/P9.stderr)。检出需人工核验的 SQL 可实现操作：.query(, sort_values(；不能仅凭理由判为合规。

P10：Generate a final summary visualization combining all key findings for the report.

[源码](../../../runs/dsv4flash-db-first-full-01/dacomp-047/attempt-01/python/P10.py)；[输出](../../../runs/dsv4flash-db-first-full-01/dacomp-047/attempt-01/python/P10.stdout)；[错误](../../../runs/dsv4flash-db-first-full-01/dacomp-047/attempt-01/python/P10.stderr)。检出需人工核验的 SQL 可实现操作：.query(；不能仅凭理由判为合规。

## 优化机会

已验证候选。筛选限于精确 SQL、相同自包含 CTE、相同单表完整过滤、可分解单表聚合；未覆盖任意 Join 等价和一般谓词蕴含。全部候选都是 offline，未测在线预测。

| 候选 | 类型 | 已有结果 | 覆盖 SQL | 后续次数 | 中间行数 | 验证 | 成本 |
| --- | --- | --- | --- | --- | --- | --- | --- |
| C1 | exact-result reuse | True | ["S19", "S20", "S21", "S22", "S23", "S57"] | 5 | 6474 | verified | Not benchmarked; correctness alone does not establish net speedup. |
| C2 | exact-result reuse | True | ["S34", "S35"] | 1 | 11493 | verified | Not benchmarked; correctness alone does not establish net speedup. |
| C3 | exact-result reuse | True | ["S36", "S40"] | 1 | 174 | verified | Not benchmarked; correctness alone does not establish net speedup. |


已验证覆盖（含触发查询、候选并集去重）：10/54 条成功数据 SQL。正确性仅针对当前数据库快照；未测性能的候选不能声称已加速。

[完整 build/rewrite 与比较证据](dacomp-047.analysis.json)。

### C1：exact-result reuse

Identical normalized SQL and parameters; archive equality checked.

原查询 [S19](#s19), [S20](#s20), [S21](#s21), [S22](#s22), [S23](#s23), [S57](#s57) → 保留前序结果 S19 → 后续 5 次可复用。该构建点为事后假设，不代表 Agent 当时预知后续。

| 原 SQL | 列名一致 | 结果一致 | 比较方法 |
| --- | --- | --- | --- |
| S20 | True | True | exact_multiset |
| S21 | True | True | exact_multiset |
| S22 | True | True | exact_multiset |
| S23 | True | True | exact_multiset |
| S57 | True | True | exact_multiset |


验证状态：verified；成本结论：Not benchmarked; correctness alone does not establish net speedup.

### C2：exact-result reuse

Identical normalized SQL and parameters; archive equality checked.

原查询 [S34](#s34), [S35](#s35) → 保留前序结果 S34 → 后续 1 次可复用。该构建点为事后假设，不代表 Agent 当时预知后续。

| 原 SQL | 列名一致 | 结果一致 | 比较方法 |
| --- | --- | --- | --- |
| S35 | True | True | ordered_numeric_tolerance |


验证状态：verified；成本结论：Not benchmarked; correctness alone does not establish net speedup.

### C3：exact-result reuse

Identical normalized SQL and parameters; archive equality checked.

原查询 [S36](#s36), [S40](#s40) → 保留前序结果 S36 → 后续 1 次可复用。该构建点为事后假设，不代表 Agent 当时预知后续。

| 原 SQL | 列名一致 | 结果一致 | 比较方法 |
| --- | --- | --- | --- |
| S40 | True | True | exact_multiset |


验证状态：verified；成本结论：Not benchmarked; correctness alone does not establish net speedup.

结果依赖：自动记录 SQL→Python 的接口父调用，以及源码中引用归档文件的消费者；字面值相同不认定因果。模型方向选择需要人工读取消息，尚未做全面因果标注。

[原始报告](../../../runs/dsv4flash-db-first-full-01/dacomp-047/attempt-01/answer.md)；[统一消息](../../../runs/dsv4flash-db-first-full-01/dacomp-047/attempt-01/messages.jsonl)；[原始 OpenCode 事件](../../../runs/dsv4flash-db-first-full-01/dacomp-047/attempt-01/opencode.jsonl)；[SQL 引擎日志](../../../runs/dsv4flash-db-first-full-01/dacomp-047/attempt-01/sql_journal.jsonl)。

[可读报告（本地图片链接规范化）](../answers/dacomp-047.md)。原始回答保留，分析结论未改写。

## S1

类别 `connection_setup`；来源 `connection`；调用 `981b4270750b4bed8c1a2c2c0c209a93`；状态 `success`。

```sql
PRAGMA query_only=ON
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-047/attempt-01/sql/S1.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-047/attempt-01/sql/S1.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-047/attempt-01/results/S1.rows.jsonl)；完整：True；SHA256：`e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`。

## S2

类别 `metadata`；来源 `list_db`；调用 `981b4270750b4bed8c1a2c2c0c209a93`；状态 `success`。

```sql
SELECT name,sql FROM sqlite_master WHERE type='table' ORDER BY name
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-047/attempt-01/sql/S2.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-047/attempt-01/sql/S2.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-047/attempt-01/results/S2.rows.jsonl)；完整：True；SHA256：`fd15eee55130eb0b938130640985bd6d43ca5f5068dd98609bd01c5309634194`。

## S3

类别 `data`；来源 `query_db`；调用 `080bbfc6d131465db7087e3101fa46d2`；状态 `success`。

```sql
SELECT * FROM product_information LIMIT 20
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-047/attempt-01/sql/S3.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-047/attempt-01/sql/S3.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-047/attempt-01/results/S3.rows.jsonl)；完整：True；SHA256：`04c50b77d79a03d054d4005fd2eec45ba8ee73c52209cc011ba0716b6b0f3d2a`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "product_information", "kind": "base", "block": null, "base_tables": ["product_information"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |


## S4

类别 `data`；来源 `query_db`；调用 `63e0ef7018fa411086324e7d016647e7`；状态 `success`。

```sql
SELECT * FROM sales_records LIMIT 10
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-047/attempt-01/sql/S4.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-047/attempt-01/sql/S4.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-047/attempt-01/results/S4.rows.jsonl)；完整：True；SHA256：`09af30fb1182520f915501e337641b0267052af734d6cb11bd3a4ba87a8a0752`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "sales_records", "kind": "base", "block": null, "base_tables": ["sales_records"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |


## S5

类别 `data`；来源 `query_db`；调用 `e1a0c525ed804765bc8570617da88495`；状态 `success`。

```sql
SELECT "Category Code", "Category Name", COUNT(DISTINCT "Item Code") AS n_items FROM product_information GROUP BY "Category Code", "Category Name" ORDER BY n_items DESC
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-047/attempt-01/sql/S5.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-047/attempt-01/sql/S5.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-047/attempt-01/results/S5.rows.jsonl)；完整：True；SHA256：`5b5e0cca50cdd51479da6b0112fe44ec3de245b06e8877107a5dc405d065e776`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "product_information", "kind": "base", "block": null, "base_tables": ["product_information"]}] | [] | ["\"Category Code\"", "\"Category Name\""] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(DISTINCT "Item Code") | [{"table": "product_information", "column": "Item Code"}] | [] | False |


## S6

类别 `data`；来源 `query_db`；调用 `4d8e6b26ebd546ea9538d7552a123b2c`；状态 `success`。

```sql
SELECT MIN("Sales Date") AS min_date, MAX("Sales Date") AS max_date, COUNT(*) AS n_rows, COUNT(DISTINCT "Item Code") AS n_items FROM sales_records
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-047/attempt-01/sql/S6.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-047/attempt-01/sql/S6.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-047/attempt-01/results/S6.rows.jsonl)；完整：True；SHA256：`7d984ccf1be9429240cbe7d3a980a215d51e0ebdfbdacedd58cfdcf5058badc8`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "sales_records", "kind": "base", "block": null, "base_tables": ["sales_records"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | MIN("Sales Date") | [{"table": "sales_records", "column": "Sales Date"}] | [] | False |
| B1 | MAX("Sales Date") | [{"table": "sales_records", "column": "Sales Date"}] | [] | False |
| B1 | COUNT(*) | [] | [] | True |
| B1 | COUNT(DISTINCT "Item Code") | [{"table": "sales_records", "column": "Item Code"}] | [] | False |


## S7

类别 `data`；来源 `query_db`；调用 `160c348ffbe148529a03dec5602e85af`；状态 `success`。

```sql
SELECT MIN(Date) AS min_date, MAX(Date) AS max_date, COUNT(*) AS n_rows, COUNT(DISTINCT "Item Code") AS n_items FROM purchase_price
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-047/attempt-01/sql/S7.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-047/attempt-01/sql/S7.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-047/attempt-01/results/S7.rows.jsonl)；完整：True；SHA256：`1c0f912f12c248c0b3d014ec56176e7f1c67b57eafbf7a62dce4a768ba2a5d92`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "purchase_price", "kind": "base", "block": null, "base_tables": ["purchase_price"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | MIN(Date) | [{"table": "purchase_price", "column": "Date"}] | [] | False |
| B1 | MAX(Date) | [{"table": "purchase_price", "column": "Date"}] | [] | False |
| B1 | COUNT(*) | [] | [] | True |
| B1 | COUNT(DISTINCT "Item Code") | [{"table": "purchase_price", "column": "Item Code"}] | [] | False |


## S8

类别 `data`；来源 `query_db`；调用 `08281a23c9e04223a7917b298de7ea66`；状态 `success`。

```sql
SELECT strftime('%Y-%m', "Sales Date") AS ym, pi."Category Name",
       ROUND(SUM(s."Sales volume (kg)"),1) AS vol_kg,
       COUNT(DISTINCT s."Item Code") AS n_items,
       ROUND(SUM(s."Sales volume (kg)" * s."Unit price (yuan/kg)"),0) AS revenue
FROM sales_records s
JOIN product_information pi ON s."Item Code" = pi."Item Code"
GROUP BY ym, pi."Category Name"
ORDER BY pi."Category Name", ym
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-047/attempt-01/sql/S8.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-047/attempt-01/sql/S8.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-047/attempt-01/results/S8.rows.jsonl)；完整：True；SHA256：`cbb0c3f96ea68b62230bf07ea54a3be21aa11233d4131f6a2e7c2fb244842067`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "s", "kind": "base", "block": null, "base_tables": ["sales_records"]}, {"alias": "pi", "kind": "base", "block": null, "base_tables": ["product_information"]}] | [{"type": "INNER", "right": "product_information AS pi", "on": "s.\"Item Code\" = pi.\"Item Code\"", "using": []}] | ["STRFTIME('%Y-%m', \"Sales Date\")", "pi.\"Category Name\""] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(DISTINCT s."Item Code") | [{"table": "sales_records", "column": "Item Code"}] | [] | False |
| B1 | SUM(s."Sales volume (kg)") | [{"table": "sales_records", "column": "Sales volume (kg)"}] | [] | False |
| B1 | SUM(s."Sales volume (kg)" * s."Unit price (yuan/kg)") | [{"table": "sales_records", "column": "Sales volume (kg)"}, {"table": "sales_records", "column": "Unit price (yuan/kg)"}] | [] | False |


## S9

类别 `data`；来源 `query_db`；调用 `b7327a4e4b55490db5e63ff2ddf01b4a`；状态 `success`。

```sql
SELECT pi."Category Name", strftime('%m', "Sales Date") AS month,
       ROUND(SUM(s."Sales volume (kg)"),1) AS vol_kg
FROM sales_records s
JOIN product_information pi ON s."Item Code" = pi."Item Code"
GROUP BY pi."Category Name", month
ORDER BY pi."Category Name", month
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-047/attempt-01/sql/S9.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-047/attempt-01/sql/S9.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-047/attempt-01/results/S9.rows.jsonl)；完整：True；SHA256：`4bff5eab07a8d6dda988275c87e92614b48d3a2f36fbd55626a1d9679cb5aea3`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "s", "kind": "base", "block": null, "base_tables": ["sales_records"]}, {"alias": "pi", "kind": "base", "block": null, "base_tables": ["product_information"]}] | [{"type": "INNER", "right": "product_information AS pi", "on": "s.\"Item Code\" = pi.\"Item Code\"", "using": []}] | ["pi.\"Category Name\"", "STRFTIME('%m', \"Sales Date\")"] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | SUM(s."Sales volume (kg)") | [{"table": "sales_records", "column": "Sales volume (kg)"}] | [] | False |


## S10

类别 `data`；来源 `query_db`；调用 `6333689c18df4cb5a97e390178a7fc7b`；状态 `success`。

```sql
WITH daily AS (
  SELECT strftime('%Y-%m-%d', "Sales Date") AS d, pi."Category Name" AS cat, SUM(s."Sales volume (kg)") AS vol
  FROM sales_records s JOIN product_information pi ON s."Item Code"=pi."Item Code"
  GROUP BY d, cat
)
SELECT cat, substr(d,6,2) AS month, ROUND(AVG(vol),1) AS avg_daily_kg
FROM daily GROUP BY cat, month ORDER BY cat, month
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-047/attempt-01/sql/S10.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-047/attempt-01/sql/S10.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-047/attempt-01/results/S10.rows.jsonl)；完整：True；SHA256：`43904ae78f604ab6fcfd3a7bbc7c1080e92cdc33e30537bf1afc8a6fa982e419`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "s", "kind": "base", "block": null, "base_tables": ["sales_records"]}, {"alias": "pi", "kind": "base", "block": null, "base_tables": ["product_information"]}] | [{"type": "INNER", "right": "product_information AS pi", "on": "s.\"Item Code\" = pi.\"Item Code\"", "using": []}] | ["STRFTIME('%Y-%m-%d', \"Sales Date\")", "pi.\"Category Name\""] |
| B2 | [{"alias": "daily", "kind": "derived", "block": "B1", "base_tables": ["product_information", "sales_records"]}] | [] | ["cat", "SUBSTRING(d, 6, 2)"] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | SUM(s."Sales volume (kg)") | [{"table": "sales_records", "column": "Sales volume (kg)"}] | [] | False |
| B2 | AVG(vol) | [{"table": "sales_records", "column": "Sales volume (kg)"}] | [] | False |


## S11

类别 `data`；来源 `query_db`；调用 `1500965445574410adad032af4e8c863`；状态 `success`。

```sql
SELECT strftime('%Y', "Sales Date") AS yr, strftime('%m', "Sales Date") AS mo, COUNT(DISTINCT "Sales Date") AS days
FROM sales_records GROUP BY yr, mo ORDER BY yr, mo
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-047/attempt-01/sql/S11.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-047/attempt-01/sql/S11.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-047/attempt-01/results/S11.rows.jsonl)；完整：True；SHA256：`4077e1010c2342ff877c0c73197fe4a43853d8af4a20030b843ee00e37d1dac6`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "sales_records", "kind": "base", "block": null, "base_tables": ["sales_records"]}] | [] | ["STRFTIME('%Y', \"Sales Date\")", "STRFTIME('%m', \"Sales Date\")"] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(DISTINCT "Sales Date") | [{"table": "sales_records", "column": "Sales Date"}] | [] | False |


## S12

类别 `data`；来源 `query_db`；调用 `07ac706d934844eb9e6954d9b20f33d9`；状态 `success`。

```sql
WITH item_monthly AS (
  SELECT s."Item Code", pi."Item Name", pi."Category Name",
         strftime('%m', s."Sales Date") AS mo,
         SUM(s."Sales volume (kg)") AS vol_kg
  FROM sales_records s
  JOIN product_information pi ON s."Item Code"=pi."Item Code"
  GROUP BY s."Item Code", pi."Item Name", pi."Category Name", mo
)
SELECT * FROM item_monthly
WHERE mo = '07'
ORDER BY vol_kg DESC
LIMIT 30
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-047/attempt-01/sql/S12.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-047/attempt-01/sql/S12.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-047/attempt-01/results/S12.rows.jsonl)；完整：True；SHA256：`f120f41dc1241281dc634e0da675229350387b7264c6da722de593614164a504`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "s", "kind": "base", "block": null, "base_tables": ["sales_records"]}, {"alias": "pi", "kind": "base", "block": null, "base_tables": ["product_information"]}] | [{"type": "INNER", "right": "product_information AS pi", "on": "s.\"Item Code\" = pi.\"Item Code\"", "using": []}] | ["s.\"Item Code\"", "pi.\"Item Name\"", "pi.\"Category Name\"", "STRFTIME('%m', s.\"Sales Date\")"] |
| B2 | [{"alias": "item_monthly", "kind": "derived", "block": "B1", "base_tables": ["product_information", "sales_records"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | SUM(s."Sales volume (kg)") | [{"table": "sales_records", "column": "Sales volume (kg)"}] | [] | False |


## S13

类别 `data`；来源 `query_db`；调用 `3351f9bd79d945188f75bd5c6edf0eca`；状态 `success`。

```sql
SELECT s."Item Code", pi."Item Name", pi."Category Name",
       ROUND(SUM(s."Sales volume (kg)"),1) AS total_vol,
       ROUND(AVG(s."Unit price (yuan/kg)"),2) AS avg_price,
       COUNT(DISTINCT s."Sales Date") AS days_sold,
       ROUND(SUM(CASE WHEN strftime('%m', s."Sales Date")='07' THEN s."Sales volume (kg)" ELSE 0 END),1) AS july_vol
FROM sales_records s
JOIN product_information pi ON s."Item Code"=pi."Item Code"
GROUP BY s."Item Code", pi."Item Name", pi."Category Name"
ORDER BY july_vol DESC
LIMIT 30
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-047/attempt-01/sql/S13.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-047/attempt-01/sql/S13.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-047/attempt-01/results/S13.rows.jsonl)；完整：True；SHA256：`507f3bd50fdb9ac3c3272d05a6ffe5fa128a10d93897474c8157591b6abcbcc2`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "s", "kind": "base", "block": null, "base_tables": ["sales_records"]}, {"alias": "pi", "kind": "base", "block": null, "base_tables": ["product_information"]}] | [{"type": "INNER", "right": "product_information AS pi", "on": "s.\"Item Code\" = pi.\"Item Code\"", "using": []}] | ["s.\"Item Code\"", "pi.\"Item Name\"", "pi.\"Category Name\""] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(DISTINCT s."Sales Date") | [{"table": "sales_records", "column": "Sales Date"}] | [] | False |
| B1 | SUM(s."Sales volume (kg)") | [{"table": "sales_records", "column": "Sales volume (kg)"}] | [] | False |
| B1 | AVG(s."Unit price (yuan/kg)") | [{"table": "sales_records", "column": "Unit price (yuan/kg)"}] | [] | False |
| B1 | SUM(CASE WHEN STRFTIME('%m', s."Sales Date") = '07' THEN s."Sales volume (kg)" ELSE 0 END) | [{"table": "sales_records", "column": "Sales volume (kg)"}] | [{"table": "sales_records", "column": "Sales Date"}] | False |


## S14

类别 `data`；来源 `query_db`；调用 `12214b389baa4aefbbd6f80d4a910d14`；状态 `success`。

```sql
SELECT COUNT(DISTINCT strftime('%Y-%m-%d', "Sales Date") || ' ' || "Time of sale (code scan)") AS n_baskets,
       COUNT(*) AS n_rows,
       COUNT(*)*1.0 / COUNT(DISTINCT strftime('%Y-%m-%d', "Sales Date") || ' ' || "Time of sale (code scan)") AS avg_items_per_basket
FROM sales_records
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-047/attempt-01/sql/S14.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-047/attempt-01/sql/S14.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-047/attempt-01/results/S14.rows.jsonl)；完整：True；SHA256：`920706e5eea2e7f6dbd559c9a9fd0dbc4ddafde85bd2d222ac30aa7dcb88d8ff`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "sales_records", "kind": "base", "block": null, "base_tables": ["sales_records"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(DISTINCT STRFTIME('%Y-%m-%d', "Sales Date") \|\| ' ' \|\| "Time of sale (code scan)") | [{"table": "sales_records", "column": "Time of sale (code scan)"}, {"table": "sales_records", "column": "Sales Date"}] | [] | False |
| B1 | COUNT(*) | [] | [] | True |
| B1 | COUNT(DISTINCT STRFTIME('%Y-%m-%d', "Sales Date") \|\| ' ' \|\| "Time of sale (code scan)") | [{"table": "sales_records", "column": "Time of sale (code scan)"}, {"table": "sales_records", "column": "Sales Date"}] | [] | False |
| B1 | COUNT(*) | [] | [] | True |


## S15

类别 `data`；来源 `query_db`；调用 `2253673ed4d44ec6a7577ad0fe051ac4`；状态 `success`。

```sql
WITH baskets AS (
  SELECT strftime('%Y-%m-%d', "Sales Date") || ' ' || "Time of sale (code scan)" AS basket_id,
         "Item Code"
  FROM sales_records
  WHERE strftime('%m', "Sales Date") = '07'
  GROUP BY basket_id, "Item Code"
)
SELECT basket_size, COUNT(*) AS n_baskets
FROM (SELECT basket_id, COUNT(*) AS basket_size FROM baskets GROUP BY basket_id)
GROUP BY basket_size ORDER BY n_baskets DESC LIMIT 20
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-047/attempt-01/sql/S15.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-047/attempt-01/sql/S15.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-047/attempt-01/results/S15.rows.jsonl)；完整：True；SHA256：`af517a0a4c16288bc1bf6f07f03d6a41b46bf79ac37119cf1a60bcfbd0ed1044`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "sales_records", "kind": "base", "block": null, "base_tables": ["sales_records"]}] | [] | ["STRFTIME('%Y-%m-%d', \"Sales Date\") \|\| ' ' \|\| \"Time of sale (code scan)\"", "\"Item Code\""] |
| B2 | [{"alias": "baskets", "kind": "derived", "block": "B1", "base_tables": ["sales_records"]}] | [] | ["basket_id"] |
| B3 | [{"alias": "", "kind": "derived", "block": "B2", "base_tables": ["sales_records"]}] | [] | ["basket_size"] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B2 | COUNT(*) | [] | [] | True |
| B3 | COUNT(*) | [] | [] | True |


## S16

类别 `data`；来源 `query_db`；调用 `47f4f90980c342899a884a34ac40d138`；状态 `success`。

```sql
SELECT pi."Category Name",
       AVG(CASE WHEN strftime('%m', s."Sales Date")='07' THEN s."Sales volume (kg)" END) AS july_avg,
       AVG(s."Sales volume (kg)") AS overall_avg,
       (AVG(CASE WHEN strftime('%m', s."Sales Date")='07' THEN s."Sales volume (kg)" END) / AVG(s."Sales volume (kg)")) * 100 AS july_seasonality_idx
FROM sales_records s
JOIN product_information pi ON s."Item Code"=pi."Item Code"
GROUP BY pi."Category Name"
ORDER BY july_seasonality_idx DESC
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-047/attempt-01/sql/S16.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-047/attempt-01/sql/S16.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-047/attempt-01/results/S16.rows.jsonl)；完整：True；SHA256：`14f46e41cc67a192126178f781e4759ea7f23022ed9a6212fa03aa8916c8f8d1`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "s", "kind": "base", "block": null, "base_tables": ["sales_records"]}, {"alias": "pi", "kind": "base", "block": null, "base_tables": ["product_information"]}] | [{"type": "INNER", "right": "product_information AS pi", "on": "s.\"Item Code\" = pi.\"Item Code\"", "using": []}] | ["pi.\"Category Name\""] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | AVG(CASE WHEN STRFTIME('%m', s."Sales Date") = '07' THEN s."Sales volume (kg)" END) | [{"table": "sales_records", "column": "Sales volume (kg)"}] | [{"table": "sales_records", "column": "Sales Date"}] | False |
| B1 | AVG(s."Sales volume (kg)") | [{"table": "sales_records", "column": "Sales volume (kg)"}] | [] | False |
| B1 | AVG(CASE WHEN STRFTIME('%m', s."Sales Date") = '07' THEN s."Sales volume (kg)" END) | [{"table": "sales_records", "column": "Sales volume (kg)"}] | [{"table": "sales_records", "column": "Sales Date"}] | False |
| B1 | AVG(s."Sales volume (kg)") | [{"table": "sales_records", "column": "Sales volume (kg)"}] | [] | False |


## S17

类别 `data`；来源 `query_db`；调用 `cba8966f54464839ab5188cf7db5f96e`；状态 `success`。

```sql
-- Daily sales per category for correlation analysis
SELECT strftime('%Y-%m-%d', s."Sales Date") AS d,
       pi."Category Name" AS cat,
       SUM(s."Sales volume (kg)") AS daily_vol
FROM sales_records s
JOIN product_information pi ON s."Item Code"=pi."Item Code"
GROUP BY d, cat
ORDER BY d, cat LIMIT 30
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-047/attempt-01/sql/S17.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-047/attempt-01/sql/S17.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-047/attempt-01/results/S17.rows.jsonl)；完整：True；SHA256：`a6fd2935e7b9dec10f00b719aaf45e02bc51dbe9306e9bc4d587349d3fac943c`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "s", "kind": "base", "block": null, "base_tables": ["sales_records"]}, {"alias": "pi", "kind": "base", "block": null, "base_tables": ["product_information"]}] | [{"type": "INNER", "right": "product_information AS pi", "on": "s.\"Item Code\" = pi.\"Item Code\"", "using": []}] | ["STRFTIME('%Y-%m-%d', s.\"Sales Date\")", "pi.\"Category Name\""] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | SUM(s."Sales volume (kg)") | [{"table": "sales_records", "column": "Sales volume (kg)"}] | [] | False |


## S18

类别 `data`；来源 `query_db`；调用 `640b9961e5c14529994a69803bcfee66`；状态 `success`。

```sql
SELECT s."Item Code", pi."Item Name", pi."Category Name",
       strftime('%Y', s."Sales Date") AS yr,
       strftime('%m', s."Sales Date") AS mo,
       ROUND(SUM(s."Sales volume (kg)"),2) AS vol_kg,
       ROUND(SUM(s."Sales volume (kg)"*s."Unit price (yuan/kg)"),2) AS revenue
FROM sales_records s
JOIN product_information pi ON s."Item Code"=pi."Item Code"
GROUP BY s."Item Code", pi."Item Name", pi."Category Name", yr, mo
ORDER BY s."Item Code", yr, mo
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-047/attempt-01/sql/S18.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-047/attempt-01/sql/S18.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-047/attempt-01/results/S18.rows.jsonl)；完整：True；SHA256：`b9896f75ef28154c00bc26543cfcd6c449b5c18d1b5c7cf5de0819f93457c639`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "s", "kind": "base", "block": null, "base_tables": ["sales_records"]}, {"alias": "pi", "kind": "base", "block": null, "base_tables": ["product_information"]}] | [{"type": "INNER", "right": "product_information AS pi", "on": "s.\"Item Code\" = pi.\"Item Code\"", "using": []}] | ["s.\"Item Code\"", "pi.\"Item Name\"", "pi.\"Category Name\"", "STRFTIME('%Y', s.\"Sales Date\")", "STRFTIME('%m', s.\"Sales Date\")"] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | SUM(s."Sales volume (kg)") | [{"table": "sales_records", "column": "Sales volume (kg)"}] | [] | False |
| B1 | SUM(s."Sales volume (kg)" * s."Unit price (yuan/kg)") | [{"table": "sales_records", "column": "Sales volume (kg)"}, {"table": "sales_records", "column": "Unit price (yuan/kg)"}] | [] | False |


## S19

类别 `data`；来源 `query_db`；调用 `cee4e933e1db47609caa6f440792a5c5`；状态 `success`。

```sql
SELECT strftime('%Y-%m-%d', "Sales Date") AS d, pi."Category Name" AS cat, SUM("Sales volume (kg)") AS vol
FROM sales_records s JOIN product_information pi ON s."Item Code"=pi."Item Code"
GROUP BY d, cat
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-047/attempt-01/sql/S19.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-047/attempt-01/sql/S19.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-047/attempt-01/results/S19.rows.jsonl)；完整：True；SHA256：`3d69345160540151f3533312a2a8b809e915778d8c07d0d5ea2477fbe491463e`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "s", "kind": "base", "block": null, "base_tables": ["sales_records"]}, {"alias": "pi", "kind": "base", "block": null, "base_tables": ["product_information"]}] | [{"type": "INNER", "right": "product_information AS pi", "on": "s.\"Item Code\" = pi.\"Item Code\"", "using": []}] | ["STRFTIME('%Y-%m-%d', \"Sales Date\")", "pi.\"Category Name\""] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | SUM("Sales volume (kg)") | [{"table": "sales_records", "column": "Sales volume (kg)"}] | [] | False |


## S20

类别 `data`；来源 `python`；调用 `dfe191bb5ec94b098793713b7a087545`；状态 `success`。

```sql
SELECT strftime('%Y-%m-%d', "Sales Date") AS d, pi."Category Name" AS cat, SUM("Sales volume (kg)") AS vol FROM sales_records s JOIN product_information pi ON s."Item Code"=pi."Item Code" GROUP BY d, cat
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-047/attempt-01/sql/S20.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-047/attempt-01/sql/S20.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-047/attempt-01/results/S20.rows.jsonl)；完整：True；SHA256：`3d69345160540151f3533312a2a8b809e915778d8c07d0d5ea2477fbe491463e`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "s", "kind": "base", "block": null, "base_tables": ["sales_records"]}, {"alias": "pi", "kind": "base", "block": null, "base_tables": ["product_information"]}] | [{"type": "INNER", "right": "product_information AS pi", "on": "s.\"Item Code\" = pi.\"Item Code\"", "using": []}] | ["STRFTIME('%Y-%m-%d', \"Sales Date\")", "pi.\"Category Name\""] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | SUM("Sales volume (kg)") | [{"table": "sales_records", "column": "Sales volume (kg)"}] | [] | False |


## S21

类别 `data`；来源 `python`；调用 `61ce627a06f44d31a70379c1d4911724`；状态 `success`。

```sql
SELECT strftime('%Y-%m-%d', "Sales Date") AS d, pi."Category Name" AS cat, SUM("Sales volume (kg)") AS vol FROM sales_records s JOIN product_information pi ON s."Item Code"=pi."Item Code" GROUP BY d, cat
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-047/attempt-01/sql/S21.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-047/attempt-01/sql/S21.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-047/attempt-01/results/S21.rows.jsonl)；完整：True；SHA256：`3d69345160540151f3533312a2a8b809e915778d8c07d0d5ea2477fbe491463e`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "s", "kind": "base", "block": null, "base_tables": ["sales_records"]}, {"alias": "pi", "kind": "base", "block": null, "base_tables": ["product_information"]}] | [{"type": "INNER", "right": "product_information AS pi", "on": "s.\"Item Code\" = pi.\"Item Code\"", "using": []}] | ["STRFTIME('%Y-%m-%d', \"Sales Date\")", "pi.\"Category Name\""] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | SUM("Sales volume (kg)") | [{"table": "sales_records", "column": "Sales volume (kg)"}] | [] | False |


## S22

类别 `data`；来源 `python`；调用 `108e491ed5774973a015ba8711bc2ac5`；状态 `success`。

```sql
SELECT strftime('%Y-%m-%d', "Sales Date") AS d, pi."Category Name" AS cat, SUM("Sales volume (kg)") AS vol FROM sales_records s JOIN product_information pi ON s."Item Code"=pi."Item Code" GROUP BY d, cat
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-047/attempt-01/sql/S22.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-047/attempt-01/sql/S22.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-047/attempt-01/results/S22.rows.jsonl)；完整：True；SHA256：`3d69345160540151f3533312a2a8b809e915778d8c07d0d5ea2477fbe491463e`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "s", "kind": "base", "block": null, "base_tables": ["sales_records"]}, {"alias": "pi", "kind": "base", "block": null, "base_tables": ["product_information"]}] | [{"type": "INNER", "right": "product_information AS pi", "on": "s.\"Item Code\" = pi.\"Item Code\"", "using": []}] | ["STRFTIME('%Y-%m-%d', \"Sales Date\")", "pi.\"Category Name\""] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | SUM("Sales volume (kg)") | [{"table": "sales_records", "column": "Sales volume (kg)"}] | [] | False |


## S23

类别 `data`；来源 `python`；调用 `e75014a1664b4c179c9620b06e3d5dc3`；状态 `success`。

```sql
SELECT strftime('%Y-%m-%d', "Sales Date") AS d, pi."Category Name" AS cat, SUM("Sales volume (kg)") AS vol FROM sales_records s JOIN product_information pi ON s."Item Code"=pi."Item Code" GROUP BY d, cat
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-047/attempt-01/sql/S23.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-047/attempt-01/sql/S23.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-047/attempt-01/results/S23.rows.jsonl)；完整：True；SHA256：`3d69345160540151f3533312a2a8b809e915778d8c07d0d5ea2477fbe491463e`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "s", "kind": "base", "block": null, "base_tables": ["sales_records"]}, {"alias": "pi", "kind": "base", "block": null, "base_tables": ["product_information"]}] | [{"type": "INNER", "right": "product_information AS pi", "on": "s.\"Item Code\" = pi.\"Item Code\"", "using": []}] | ["STRFTIME('%Y-%m-%d', \"Sales Date\")", "pi.\"Category Name\""] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | SUM("Sales volume (kg)") | [{"table": "sales_records", "column": "Sales volume (kg)"}] | [] | False |


## S24

类别 `data`；来源 `python`；调用 `e75014a1664b4c179c9620b06e3d5dc3`；状态 `success`。

```sql

    SELECT s."Item Code" AS code, pi."Item Name" AS name, pi."Category Name" AS cat,
           strftime('%m', s."Sales Date") AS mo,
           SUM(s."Sales volume (kg)") AS vol
    FROM sales_records s JOIN product_information pi ON s."Item Code"=pi."Item Code"
    GROUP BY s."Item Code", pi."Item Name", pi."Category Name", mo

```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-047/attempt-01/sql/S24.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-047/attempt-01/sql/S24.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-047/attempt-01/results/S24.rows.jsonl)；完整：True；SHA256：`c93fae09e81b1582d5e712177dba88fe208e86ce60bad4d11502a865b98397db`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "s", "kind": "base", "block": null, "base_tables": ["sales_records"]}, {"alias": "pi", "kind": "base", "block": null, "base_tables": ["product_information"]}] | [{"type": "INNER", "right": "product_information AS pi", "on": "s.\"Item Code\" = pi.\"Item Code\"", "using": []}] | ["s.\"Item Code\"", "pi.\"Item Name\"", "pi.\"Category Name\"", "STRFTIME('%m', s.\"Sales Date\")"] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | SUM(s."Sales volume (kg)") | [{"table": "sales_records", "column": "Sales volume (kg)"}] | [] | False |


## S25

类别 `data`；来源 `python`；调用 `e75014a1664b4c179c9620b06e3d5dc3`；状态 `success`。

```sql

    SELECT s."Item Code" AS code, pi."Item Name" AS name, pi."Category Name" AS cat,
           strftime('%m', s."Sales Date") AS mo,
           SUM(s."Sales volume (kg)") * 1.0 / COUNT(DISTINCT s."Sales Date") AS avg_daily
    FROM sales_records s JOIN product_information pi ON s."Item Code"=pi."Item Code"
    GROUP BY s."Item Code", pi."Item Name", pi."Category Name", mo

```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-047/attempt-01/sql/S25.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-047/attempt-01/sql/S25.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-047/attempt-01/results/S25.rows.jsonl)；完整：True；SHA256：`7eaefe4350a2590ce68133e21d020e4555eac81f716e1926fb72ed425d6ff592`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "s", "kind": "base", "block": null, "base_tables": ["sales_records"]}, {"alias": "pi", "kind": "base", "block": null, "base_tables": ["product_information"]}] | [{"type": "INNER", "right": "product_information AS pi", "on": "s.\"Item Code\" = pi.\"Item Code\"", "using": []}] | ["s.\"Item Code\"", "pi.\"Item Name\"", "pi.\"Category Name\"", "STRFTIME('%m', s.\"Sales Date\")"] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(DISTINCT s."Sales Date") | [{"table": "sales_records", "column": "Sales Date"}] | [] | False |
| B1 | SUM(s."Sales volume (kg)") | [{"table": "sales_records", "column": "Sales volume (kg)"}] | [] | False |


## S26

类别 `data`；来源 `query_db`；调用 `7578f5a985914e6094ef4ad358b154a3`；状态 `success`。

```sql
-- Purchase price info for top July items
SELECT pp."Item Code", pi."Item Name", pi."Category Name",
       ROUND(AVG(pp."Wholesale price (yuan/kg)"),2) AS avg_wholesale,
       ROUND(AVG(CASE WHEN strftime('%m', pp."Date")='07' THEN pp."Wholesale price (yuan/kg)" END),2) AS july_wholesale
FROM purchase_price pp
JOIN product_information pi ON pp."Item Code"=pi."Item Code"
GROUP BY pp."Item Code", pi."Item Name", pi."Category Name"
ORDER BY pi."Item Code"
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-047/attempt-01/sql/S26.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-047/attempt-01/sql/S26.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-047/attempt-01/results/S26.rows.jsonl)；完整：True；SHA256：`6127a19bf4688ba848a8a14ade58563bfb0f96c1ad44989d365393604f7ffaea`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "pp", "kind": "base", "block": null, "base_tables": ["purchase_price"]}, {"alias": "pi", "kind": "base", "block": null, "base_tables": ["product_information"]}] | [{"type": "INNER", "right": "product_information AS pi", "on": "pp.\"Item Code\" = pi.\"Item Code\"", "using": []}] | ["pp.\"Item Code\"", "pi.\"Item Name\"", "pi.\"Category Name\""] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | AVG(pp."Wholesale price (yuan/kg)") | [{"table": "purchase_price", "column": "Wholesale price (yuan/kg)"}] | [] | False |
| B1 | AVG(CASE WHEN STRFTIME('%m', pp."Date") = '07' THEN pp."Wholesale price (yuan/kg)" END) | [{"table": "purchase_price", "column": "Wholesale price (yuan/kg)"}] | [{"table": "purchase_price", "column": "Date"}] | False |


## S27

类别 `data`；来源 `query_db`；调用 `3c68122e0b184100b458650546351567`；状态 `success`。

```sql
-- Average selling price per item in July
SELECT s."Item Code", pi."Item Name", pi."Category Name",
       ROUND(AVG(s."Unit price (yuan/kg)"),2) AS avg_retail,
       ROUND(AVG(CASE WHEN strftime('%m', s."Sales Date")='07' THEN s."Unit price (yuan/kg)" END),2) AS july_retail,
       ROUND(SUM(CASE WHEN strftime('%m', s."Sales Date")='07' THEN s."Sales volume (kg)" END),1) AS july_vol
FROM sales_records s
JOIN product_information pi ON s."Item Code"=pi."Item Code"
GROUP BY s."Item Code", pi."Item Name", pi."Category Name"
ORDER BY july_vol DESC
LIMIT 30
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-047/attempt-01/sql/S27.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-047/attempt-01/sql/S27.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-047/attempt-01/results/S27.rows.jsonl)；完整：True；SHA256：`27a0035d49c89183bd6e5904b975ffaf803e24959cc8389e5da084179a0ca7f4`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "s", "kind": "base", "block": null, "base_tables": ["sales_records"]}, {"alias": "pi", "kind": "base", "block": null, "base_tables": ["product_information"]}] | [{"type": "INNER", "right": "product_information AS pi", "on": "s.\"Item Code\" = pi.\"Item Code\"", "using": []}] | ["s.\"Item Code\"", "pi.\"Item Name\"", "pi.\"Category Name\""] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | AVG(s."Unit price (yuan/kg)") | [{"table": "sales_records", "column": "Unit price (yuan/kg)"}] | [] | False |
| B1 | AVG(CASE WHEN STRFTIME('%m', s."Sales Date") = '07' THEN s."Unit price (yuan/kg)" END) | [{"table": "sales_records", "column": "Unit price (yuan/kg)"}] | [{"table": "sales_records", "column": "Sales Date"}] | False |
| B1 | SUM(CASE WHEN STRFTIME('%m', s."Sales Date") = '07' THEN s."Sales volume (kg)" END) | [{"table": "sales_records", "column": "Sales volume (kg)"}] | [{"table": "sales_records", "column": "Sales Date"}] | False |


## S28

类别 `data`；来源 `query_db`；调用 `0321c6828a4948f59d9521be64f3c223`；状态 `success`。

```sql
SELECT * FROM product_loss LIMIT 20
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-047/attempt-01/sql/S28.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-047/attempt-01/sql/S28.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-047/attempt-01/results/S28.rows.jsonl)；完整：True；SHA256：`d8739844fa0ef795a45437cd0e877041825ca9d7fe09c5afe94d9378461f7da7`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "product_loss", "kind": "base", "block": null, "base_tables": ["product_loss"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |


## S29

类别 `data`；来源 `query_db`；调用 `afe38dea44624bc5bc55910e9622fef0`；状态 `success`。

```sql
-- Compute profit margin for top July items
SELECT s."Item Code", pi."Item Name", pi."Category Name",
       ROUND(AVG(s."Unit price (yuan/kg)"),2) AS avg_retail,
       ROUND(AVG(pp."Wholesale price (yuan/kg)"),2) AS avg_wholesale,
       ROUND(AVG(s."Unit price (yuan/kg)") - AVG(pp."Wholesale price (yuan/kg)"),2) AS margin,
       ROUND(SUM(CASE WHEN strftime('%m', s."Sales Date")='07' THEN s."Sales volume (kg)" END),1) AS july_vol
FROM sales_records s
JOIN product_information pi ON s."Item Code"=pi."Item Code"
LEFT JOIN purchase_price pp ON s."Item Code"=pp."Item Code" AND date(s."Sales Date")=date(pp."Date")
GROUP BY s."Item Code", pi."Item Name", pi."Category Name"
HAVING july_vol > 100
ORDER BY july_vol DESC
LIMIT 30
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-047/attempt-01/sql/S29.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-047/attempt-01/sql/S29.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-047/attempt-01/results/S29.rows.jsonl)；完整：True；SHA256：`b91a27f3171f7cea91e22d66d7a3176d5daf72e8de1cb9764200bfacc46fb7a5`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "s", "kind": "base", "block": null, "base_tables": ["sales_records"]}, {"alias": "pi", "kind": "base", "block": null, "base_tables": ["product_information"]}, {"alias": "pp", "kind": "base", "block": null, "base_tables": ["purchase_price"]}] | [{"type": "INNER", "right": "product_information AS pi", "on": "s.\"Item Code\" = pi.\"Item Code\"", "using": []}, {"type": "LEFT", "right": "purchase_price AS pp", "on": "s.\"Item Code\" = pp.\"Item Code\" AND DATE(s.\"Sales Date\") = DATE(pp.\"Date\")", "using": []}] | ["s.\"Item Code\"", "pi.\"Item Name\"", "pi.\"Category Name\""] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | AVG(s."Unit price (yuan/kg)") | [{"table": "sales_records", "column": "Unit price (yuan/kg)"}] | [] | False |
| B1 | AVG(pp."Wholesale price (yuan/kg)") | [{"table": "purchase_price", "column": "Wholesale price (yuan/kg)"}] | [] | False |
| B1 | SUM(CASE WHEN STRFTIME('%m', s."Sales Date") = '07' THEN s."Sales volume (kg)" END) | [{"table": "sales_records", "column": "Sales volume (kg)"}] | [{"table": "sales_records", "column": "Sales Date"}] | False |
| B1 | AVG(s."Unit price (yuan/kg)") | [{"table": "sales_records", "column": "Unit price (yuan/kg)"}] | [] | False |
| B1 | AVG(pp."Wholesale price (yuan/kg)") | [{"table": "purchase_price", "column": "Wholesale price (yuan/kg)"}] | [] | False |


## S30

类别 `data`；来源 `query_db`；调用 `75da4d9ccb574dfcaf85693e2cf2834b`；状态 `success`。

```sql
-- Yearly July volumes for top candidates
SELECT pi."Item Name", strftime('%Y', s."Sales Date") AS yr, ROUND(SUM(s."Sales volume (kg)"),1) AS july_vol
FROM sales_records s
JOIN product_information pi ON s."Item Code"=pi."Item Code"
WHERE strftime('%m', s."Sales Date")='07'
  AND s."Item Code" IN (
    102900005115779,102900005116714,102900005115984,102900011016701,
    102900005116899,102900005119975,102900005115786,102900005116257,
    102900051010455,102900011009970,102900005117056,102900005116530,
    102900005115960,102900011000328,102900005115823,102900011030059,
    102900011030097,102900011008522,102900011032787,102900011034231,
    102900011034224,102900011030141,102900011001561,102900011033234
  )
GROUP BY pi."Item Name", yr
ORDER BY pi."Item Name", yr
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-047/attempt-01/sql/S30.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-047/attempt-01/sql/S30.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-047/attempt-01/results/S30.rows.jsonl)；完整：True；SHA256：`86e7d6f4c5225138a020f0d9521529beaa4758b22392e11fd984f61db1c4d1c9`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "s", "kind": "base", "block": null, "base_tables": ["sales_records"]}, {"alias": "pi", "kind": "base", "block": null, "base_tables": ["product_information"]}] | [{"type": "INNER", "right": "product_information AS pi", "on": "s.\"Item Code\" = pi.\"Item Code\"", "using": []}] | ["pi.\"Item Name\"", "STRFTIME('%Y', s.\"Sales Date\")"] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | SUM(s."Sales volume (kg)") | [{"table": "sales_records", "column": "Sales volume (kg)"}] | [] | False |


## S31

类别 `data`；来源 `query_db`；调用 `e0af70d7e8d044dfa3aa161c1cde07f5`；状态 `success`。

```sql
-- Recent months (2023 Q1-Q2) daily avg for top candidates
SELECT pi."Item Name", strftime('%Y-%m', s."Sales Date") AS ym,
       ROUND(SUM(s."Sales volume (kg)")/COUNT(DISTINCT s."Sales Date"),2) AS avg_daily
FROM sales_records s
JOIN product_information pi ON s."Item Code"=pi."Item Code"
WHERE s."Sales Date" >= '2023-01-01'
  AND s."Item Code" IN (
    102900005115779,102900005116714,102900005115984,102900011016701,
    102900005116899,102900005119975,102900005115786,102900005116257,
    102900051010455,102900011009970,102900005117056,102900005116530,
    102900005115960,102900011000328,102900005115823,102900011030059,
    102900011030097,102900011008522,102900011032787,102900011034231,
    102900011034224,102900011030141,102900011001561,102900011033234
  )
GROUP BY pi."Item Name", ym
ORDER BY pi."Item Name", ym
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-047/attempt-01/sql/S31.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-047/attempt-01/sql/S31.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-047/attempt-01/results/S31.rows.jsonl)；完整：True；SHA256：`397e8fd01f9fa0f76c0da7fe4d258f9136611d1136946daebb09068e4a7a0771`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "s", "kind": "base", "block": null, "base_tables": ["sales_records"]}, {"alias": "pi", "kind": "base", "block": null, "base_tables": ["product_information"]}] | [{"type": "INNER", "right": "product_information AS pi", "on": "s.\"Item Code\" = pi.\"Item Code\"", "using": []}] | ["pi.\"Item Name\"", "STRFTIME('%Y-%m', s.\"Sales Date\")"] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | SUM(s."Sales volume (kg)") | [{"table": "sales_records", "column": "Sales volume (kg)"}] | [] | False |
| B1 | COUNT(DISTINCT s."Sales Date") | [{"table": "sales_records", "column": "Sales Date"}] | [] | False |


## S32

类别 `data`；来源 `query_db`；调用 `0355da01080a4351be3656dd1eac1226`；状态 `success`。

```sql
-- Loss rates for top July items
SELECT pl."Item Code", pi."Item Name", pi."Category Name", pl."Loss Rate (%)"
FROM product_loss pl
JOIN product_information pi ON pl."Item Code"=pi."Item Code"
WHERE pi."Item Name" IN (
  'Yunnan Leaf Lettuce','Broccoli','Yunnan Romaine Lettuce','Wuhu green pepper (1)',
  'Peeled Lotus Root (1)','Sweet Potato Vine Tips','Water Spinach','Purple Eggplant (2)',
  'Yellow Chinese Cabbage (2)','Green-stem Loose Cauliflower','Bubble Pepper (Premium)',
  'Xixia shiitake (1)','Napa Cabbage','Spiral chili pepper','Shanghai Bok Choy',
  'Sweet Bok Choy','Lotus seed pod (piece)'
)
ORDER BY pl."Loss Rate (%)"
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-047/attempt-01/sql/S32.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-047/attempt-01/sql/S32.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-047/attempt-01/results/S32.rows.jsonl)；完整：True；SHA256：`37e3f460be8958e402b1c000eb30ff41b78563e29118d0de95e4d051e1dec92d`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "pl", "kind": "base", "block": null, "base_tables": ["product_loss"]}, {"alias": "pi", "kind": "base", "block": null, "base_tables": ["product_information"]}] | [{"type": "INNER", "right": "product_information AS pi", "on": "pl.\"Item Code\" = pi.\"Item Code\"", "using": []}] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |


## S33

类别 `data`；来源 `query_db`；调用 `3563f1a865314c39abe1414af0414e9f`；状态 `success`。

```sql
-- Daily sales data for top items (for correlation analysis)
SELECT strftime('%Y-%m-%d', s."Sales Date") AS d, s."Item Code", pi."Item Name", pi."Category Name", SUM(s."Sales volume (kg)") AS vol
FROM sales_records s
JOIN product_information pi ON s."Item Code"=pi."Item Code"
WHERE s."Item Code" IN (
  102900005115779,102900005116714,102900005115984,102900011016701,
  102900005116899,102900005119975,102900005115786,102900005116257,
  102900051010455,102900011009970,102900005117056,102900005116530,
  102900005115960,102900011000328,102900005115823
)
GROUP BY d, s."Item Code", pi."Item Name", pi."Category Name"
ORDER BY d, pi."Item Name"
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-047/attempt-01/sql/S33.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-047/attempt-01/sql/S33.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-047/attempt-01/results/S33.rows.jsonl)；完整：True；SHA256：`2071a78159e715dacd232fb0d752e52331929cfc0906ec7486ef692fec973108`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "s", "kind": "base", "block": null, "base_tables": ["sales_records"]}, {"alias": "pi", "kind": "base", "block": null, "base_tables": ["product_information"]}] | [{"type": "INNER", "right": "product_information AS pi", "on": "s.\"Item Code\" = pi.\"Item Code\"", "using": []}] | ["STRFTIME('%Y-%m-%d', s.\"Sales Date\")", "s.\"Item Code\"", "pi.\"Item Name\"", "pi.\"Category Name\""] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | SUM(s."Sales volume (kg)") | [{"table": "sales_records", "column": "Sales volume (kg)"}] | [] | False |


## S34

类别 `data`；来源 `python`；调用 `d407a6b9da994939a176804c524ffcae`；状态 `success`。

```sql

    SELECT strftime('%Y-%m-%d', s."Sales Date") AS d, s."Item Code", pi."Item Name", SUM(s."Sales volume (kg)") AS vol
    FROM sales_records s
    JOIN product_information pi ON s."Item Code"=pi."Item Code"
    WHERE s."Item Code" IN (
      102900005115779,102900005116714,102900005115984,102900011016701,
      102900005116899,102900005119975,102900005115786,102900005116257,
      102900051010455,102900011009970,102900005117056,102900005116530,
      102900005115960,102900011000328,102900005115823
    )
    GROUP BY d, s."Item Code", pi."Item Name"
    ORDER BY d, pi."Item Name"

```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-047/attempt-01/sql/S34.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-047/attempt-01/sql/S34.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-047/attempt-01/results/S34.rows.jsonl)；完整：True；SHA256：`37b38667761aa9e2fef939a6bab62959935421fa40f7c3faed4c8cb1f7932f41`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "s", "kind": "base", "block": null, "base_tables": ["sales_records"]}, {"alias": "pi", "kind": "base", "block": null, "base_tables": ["product_information"]}] | [{"type": "INNER", "right": "product_information AS pi", "on": "s.\"Item Code\" = pi.\"Item Code\"", "using": []}] | ["STRFTIME('%Y-%m-%d', s.\"Sales Date\")", "s.\"Item Code\"", "pi.\"Item Name\""] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | SUM(s."Sales volume (kg)") | [{"table": "sales_records", "column": "Sales volume (kg)"}] | [] | False |


## S35

类别 `data`；来源 `python`；调用 `eb2a57b6cbc04905b907c7036298f0be`；状态 `success`。

```sql

    SELECT strftime('%Y-%m-%d', s."Sales Date") AS d, s."Item Code", pi."Item Name", SUM(s."Sales volume (kg)") AS vol
    FROM sales_records s
    JOIN product_information pi ON s."Item Code"=pi."Item Code"
    WHERE s."Item Code" IN (
      102900005115779,102900005116714,102900005115984,102900011016701,
      102900005116899,102900005119975,102900005115786,102900005116257,
      102900051010455,102900011009970,102900005117056,102900005116530,
      102900005115960,102900011000328,102900005115823
    )
    GROUP BY d, s."Item Code", pi."Item Name"
    ORDER BY d, pi."Item Name"

```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-047/attempt-01/sql/S35.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-047/attempt-01/sql/S35.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-047/attempt-01/results/S35.rows.jsonl)；完整：True；SHA256：`37b38667761aa9e2fef939a6bab62959935421fa40f7c3faed4c8cb1f7932f41`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "s", "kind": "base", "block": null, "base_tables": ["sales_records"]}, {"alias": "pi", "kind": "base", "block": null, "base_tables": ["product_information"]}] | [{"type": "INNER", "right": "product_information AS pi", "on": "s.\"Item Code\" = pi.\"Item Code\"", "using": []}] | ["STRFTIME('%Y-%m-%d', s.\"Sales Date\")", "s.\"Item Code\"", "pi.\"Item Name\""] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | SUM(s."Sales volume (kg)") | [{"table": "sales_records", "column": "Sales volume (kg)"}] | [] | False |


## S36

类别 `data`；来源 `python`；调用 `eb2a57b6cbc04905b907c7036298f0be`；状态 `success`。

```sql

    SELECT s."Item Code" AS code, pi."Item Name" AS name,
           strftime('%m', s."Sales Date") AS mo,
           SUM(s."Sales volume (kg)") * 1.0 / COUNT(DISTINCT s."Sales Date") AS avg_daily
    FROM sales_records s
    JOIN product_information pi ON s."Item Code"=pi."Item Code"
    WHERE s."Item Code" IN (
      102900005115779,102900005116714,102900005115984,102900011016701,
      102900005116899,102900005119975,102900005115786,102900005116257,
      102900051010455,102900011009970,102900005117056,102900005116530,
      102900005115960,102900011000328,102900005115823
    )
    GROUP BY s."Item Code", pi."Item Name", mo

```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-047/attempt-01/sql/S36.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-047/attempt-01/sql/S36.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-047/attempt-01/results/S36.rows.jsonl)；完整：True；SHA256：`7eac92e0b68359c2249b829ffbe222ccee7ac9b405af9bf82c1c96b06d6b2101`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "s", "kind": "base", "block": null, "base_tables": ["sales_records"]}, {"alias": "pi", "kind": "base", "block": null, "base_tables": ["product_information"]}] | [{"type": "INNER", "right": "product_information AS pi", "on": "s.\"Item Code\" = pi.\"Item Code\"", "using": []}] | ["s.\"Item Code\"", "pi.\"Item Name\"", "STRFTIME('%m', s.\"Sales Date\")"] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(DISTINCT s."Sales Date") | [{"table": "sales_records", "column": "Sales Date"}] | [] | False |
| B1 | SUM(s."Sales volume (kg)") | [{"table": "sales_records", "column": "Sales volume (kg)"}] | [] | False |


## S37

类别 `data`；来源 `python`；调用 `bd59210b25b3445f9d2c881abcfb0064`；状态 `success`。

```sql

    SELECT s."Item Code" AS code, pi."Item Name" AS name, pi."Category Name" AS cat,
           ROUND(SUM(CASE WHEN strftime('%m', s."Sales Date")='07' THEN s."Sales volume (kg)" ELSE 0 END),1) AS july_vol,
           ROUND(SUM(s."Sales volume (kg)"),1) AS total_vol,
           ROUND(COUNT(DISTINCT s."Sales Date")*1.0/1096,4) AS freq,
           ROUND(AVG(s."Unit price (yuan/kg)"),2) AS avg_retail,
           ROUND(SUM(CASE WHEN strftime('%m', s."Sales Date")='07' THEN s."Sales volume (kg)"*s."Unit price (yuan/kg)" ELSE 0 END),0) AS july_revenue
    FROM sales_records s
    JOIN product_information pi ON s."Item Code"=pi."Item Code"
    WHERE s."Item Code" IN (
      102900005115779,102900005116714,102900005115984,102900011016701,
      102900005116899,102900005119975,102900005115786,102900005116257,
      102900051010455,102900011009970,102900005117056,102900005116530,
      102900005115960,102900011000328,102900005115823
    )
    GROUP BY s."Item Code", pi."Item Name", pi."Category Name"

```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-047/attempt-01/sql/S37.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-047/attempt-01/sql/S37.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-047/attempt-01/results/S37.rows.jsonl)；完整：True；SHA256：`188d66166b46bbb9136ceb1aa500f9458850ea7a4de46508d4024b7e4e33920f`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "s", "kind": "base", "block": null, "base_tables": ["sales_records"]}, {"alias": "pi", "kind": "base", "block": null, "base_tables": ["product_information"]}] | [{"type": "INNER", "right": "product_information AS pi", "on": "s.\"Item Code\" = pi.\"Item Code\"", "using": []}] | ["s.\"Item Code\"", "pi.\"Item Name\"", "pi.\"Category Name\""] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | SUM(CASE WHEN STRFTIME('%m', s."Sales Date") = '07' THEN s."Sales volume (kg)" ELSE 0 END) | [{"table": "sales_records", "column": "Sales volume (kg)"}] | [{"table": "sales_records", "column": "Sales Date"}] | False |
| B1 | SUM(s."Sales volume (kg)") | [{"table": "sales_records", "column": "Sales volume (kg)"}] | [] | False |
| B1 | AVG(s."Unit price (yuan/kg)") | [{"table": "sales_records", "column": "Unit price (yuan/kg)"}] | [] | False |
| B1 | SUM(CASE WHEN STRFTIME('%m', s."Sales Date") = '07' THEN s."Sales volume (kg)" * s."Unit price (yuan/kg)" ELSE 0 END) | [{"table": "sales_records", "column": "Sales volume (kg)"}, {"table": "sales_records", "column": "Unit price (yuan/kg)"}] | [{"table": "sales_records", "column": "Sales Date"}] | False |
| B1 | COUNT(DISTINCT s."Sales Date") | [{"table": "sales_records", "column": "Sales Date"}] | [] | False |


## S38

类别 `data`；来源 `python`；调用 `bd59210b25b3445f9d2c881abcfb0064`；状态 `success`。

```sql

    SELECT pl."Item Code" AS code, pl."Loss Rate (%)" AS loss_rate
    FROM product_loss pl
    WHERE pl."Item Code" IN (
      102900005115779,102900005116714,102900005115984,102900011016701,
      102900005116899,102900005119975,102900005115786,102900005116257,
      102900051010455,102900011009970,102900005117056,102900005116530,
      102900005115960,102900011000328,102900005115823
    )

```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-047/attempt-01/sql/S38.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-047/attempt-01/sql/S38.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-047/attempt-01/results/S38.rows.jsonl)；完整：True；SHA256：`331db676d0bcffc57418a67118e41e42885dcb4bde07e7d9683b859992154ff9`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "pl", "kind": "base", "block": null, "base_tables": ["product_loss"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |


## S39

类别 `data`；来源 `python`；调用 `bd59210b25b3445f9d2c881abcfb0064`；状态 `success`。

```sql

    SELECT s."Item Code" AS code, 
           ROUND(AVG(s."Unit price (yuan/kg)") - AVG(pp."Wholesale price (yuan/kg)"),2) AS margin
    FROM sales_records s
    LEFT JOIN purchase_price pp ON s."Item Code"=pp."Item Code" AND date(s."Sales Date")=date(pp."Date")
    WHERE s."Item Code" IN (
      102900005115779,102900005116714,102900005115984,102900011016701,
      102900005116899,102900005119975,102900005115786,102900005116257,
      102900051010455,102900011009970,102900005117056,102900005116530,
      102900005115960,102900011000328,102900005115823
    )
    GROUP BY s."Item Code"

```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-047/attempt-01/sql/S39.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-047/attempt-01/sql/S39.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-047/attempt-01/results/S39.rows.jsonl)；完整：True；SHA256：`fc374177407aaa4a877a7a66340ec2ce81f7d341c6ff505410bf0246acd68936`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "s", "kind": "base", "block": null, "base_tables": ["sales_records"]}, {"alias": "pp", "kind": "base", "block": null, "base_tables": ["purchase_price"]}] | [{"type": "LEFT", "right": "purchase_price AS pp", "on": "s.\"Item Code\" = pp.\"Item Code\" AND DATE(s.\"Sales Date\") = DATE(pp.\"Date\")", "using": []}] | ["s.\"Item Code\""] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | AVG(s."Unit price (yuan/kg)") | [{"table": "sales_records", "column": "Unit price (yuan/kg)"}] | [] | False |
| B1 | AVG(pp."Wholesale price (yuan/kg)") | [{"table": "purchase_price", "column": "Wholesale price (yuan/kg)"}] | [] | False |


## S40

类别 `data`；来源 `python`；调用 `bd59210b25b3445f9d2c881abcfb0064`；状态 `success`。

```sql

    SELECT s."Item Code" AS code, pi."Item Name" AS name,
           strftime('%m', s."Sales Date") AS mo,
           SUM(s."Sales volume (kg)") * 1.0 / COUNT(DISTINCT s."Sales Date") AS avg_daily
    FROM sales_records s
    JOIN product_information pi ON s."Item Code"=pi."Item Code"
    WHERE s."Item Code" IN (
      102900005115779,102900005116714,102900005115984,102900011016701,
      102900005116899,102900005119975,102900005115786,102900005116257,
      102900051010455,102900011009970,102900005117056,102900005116530,
      102900005115960,102900011000328,102900005115823
    )
    GROUP BY s."Item Code", pi."Item Name", mo

```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-047/attempt-01/sql/S40.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-047/attempt-01/sql/S40.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-047/attempt-01/results/S40.rows.jsonl)；完整：True；SHA256：`7eac92e0b68359c2249b829ffbe222ccee7ac9b405af9bf82c1c96b06d6b2101`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "s", "kind": "base", "block": null, "base_tables": ["sales_records"]}, {"alias": "pi", "kind": "base", "block": null, "base_tables": ["product_information"]}] | [{"type": "INNER", "right": "product_information AS pi", "on": "s.\"Item Code\" = pi.\"Item Code\"", "using": []}] | ["s.\"Item Code\"", "pi.\"Item Name\"", "STRFTIME('%m', s.\"Sales Date\")"] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(DISTINCT s."Sales Date") | [{"table": "sales_records", "column": "Sales Date"}] | [] | False |
| B1 | SUM(s."Sales volume (kg)") | [{"table": "sales_records", "column": "Sales volume (kg)"}] | [] | False |


## S41

类别 `data`；来源 `query_db`；调用 `996f8866f7e04b9cb914923ad98b59f9`；状态 `success`。

```sql
-- 2023 trend for recommended items
SELECT pi."Item Name", strftime('%Y-%m', s."Sales Date") AS ym,
       ROUND(SUM(s."Sales volume (kg)")/COUNT(DISTINCT s."Sales Date"),2) AS avg_daily,
       ROUND(SUM(s."Sales volume (kg)"),1) AS month_vol
FROM sales_records s
JOIN product_information pi ON s."Item Code"=pi."Item Code"
WHERE s."Sales Date" >= '2023-01-01'
  AND pi."Item Name" IN (
    'Yunnan Leaf Lettuce','Water Spinach','Sweet Potato Vine Tips',
    'Broccoli','Purple Eggplant (2)','Spiral chili pepper',
    'Yunnan Romaine Lettuce','Shanghai Bok Choy','Green-stem Loose Cauliflower'
  )
GROUP BY pi."Item Name", ym
ORDER BY pi."Item Name", ym
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-047/attempt-01/sql/S41.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-047/attempt-01/sql/S41.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-047/attempt-01/results/S41.rows.jsonl)；完整：True；SHA256：`b8ba3be75651ec2b3614ae98bf5334ff0043e235ad08d24431d0794d02fe1a26`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "s", "kind": "base", "block": null, "base_tables": ["sales_records"]}, {"alias": "pi", "kind": "base", "block": null, "base_tables": ["product_information"]}] | [{"type": "INNER", "right": "product_information AS pi", "on": "s.\"Item Code\" = pi.\"Item Code\"", "using": []}] | ["pi.\"Item Name\"", "STRFTIME('%Y-%m', s.\"Sales Date\")"] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | SUM(s."Sales volume (kg)") | [{"table": "sales_records", "column": "Sales volume (kg)"}] | [] | False |
| B1 | SUM(s."Sales volume (kg)") | [{"table": "sales_records", "column": "Sales volume (kg)"}] | [] | False |
| B1 | COUNT(DISTINCT s."Sales Date") | [{"table": "sales_records", "column": "Sales Date"}] | [] | False |


## S42

类别 `data`；来源 `query_db`；调用 `58f66285e3ef42ceadf99019b8befe40`；状态 `success`。

```sql
-- Historical July avg daily by year for recommended items
SELECT pi."Item Name", strftime('%Y', s."Sales Date") AS yr,
       ROUND(SUM(s."Sales volume (kg)")/COUNT(DISTINCT s."Sales Date"),2) AS july_avg_daily
FROM sales_records s
JOIN product_information pi ON s."Item Code"=pi."Item Code"
WHERE strftime('%m', s."Sales Date")='07'
  AND pi."Item Name" IN (
    'Yunnan Leaf Lettuce','Water Spinach','Sweet Potato Vine Tips',
    'Broccoli','Purple Eggplant (2)','Spiral chili pepper',
    'Yunnan Romaine Lettuce','Shanghai Bok Choy','Green-stem Loose Cauliflower'
  )
GROUP BY pi."Item Name", yr
ORDER BY pi."Item Name", yr
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-047/attempt-01/sql/S42.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-047/attempt-01/sql/S42.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-047/attempt-01/results/S42.rows.jsonl)；完整：True；SHA256：`f47b761718d1a368f3165e670f307bdf9ccfe6643cec3fe991012fa881e5edeb`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "s", "kind": "base", "block": null, "base_tables": ["sales_records"]}, {"alias": "pi", "kind": "base", "block": null, "base_tables": ["product_information"]}] | [{"type": "INNER", "right": "product_information AS pi", "on": "s.\"Item Code\" = pi.\"Item Code\"", "using": []}] | ["pi.\"Item Name\"", "STRFTIME('%Y', s.\"Sales Date\")"] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | SUM(s."Sales volume (kg)") | [{"table": "sales_records", "column": "Sales volume (kg)"}] | [] | False |
| B1 | COUNT(DISTINCT s."Sales Date") | [{"table": "sales_records", "column": "Sales Date"}] | [] | False |


## S43

类别 `data`；来源 `query_db`；调用 `badb6a2d4776424ba8493faf3160fefe`；状态 `success`。

```sql
SELECT pi."Item Name", COUNT(DISTINCT strftime('%Y', s."Sales Date")) AS n_years,
       SUM(CASE WHEN s."Sales Date">='2023-01-01' THEN s."Sales volume (kg)" ELSE 0 END) AS vol_2023,
       SUM(CASE WHEN s."Sales Date">='2022-01-01' AND s."Sales Date"<'2023-01-01' THEN s."Sales volume (kg)" ELSE 0 END) AS vol_2022
FROM sales_records s
JOIN product_information pi ON s."Item Code"=pi."Item Code"
WHERE pi."Item Name" IN (
    'Yunnan Leaf Lettuce','Water Spinach','Sweet Potato Vine Tips',
    'Broccoli','Purple Eggplant (2)','Spiral chili pepper',
    'Yunnan Romaine Lettuce','Shanghai Bok Choy','Green-stem Loose Cauliflower',
    'Yellow Chinese Cabbage (2)','Napa Cabbage','Bubble Pepper (Premium)'
)
GROUP BY pi."Item Name" ORDER BY vol_2022 DESC
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-047/attempt-01/sql/S43.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-047/attempt-01/sql/S43.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-047/attempt-01/results/S43.rows.jsonl)；完整：True；SHA256：`fb269ca54bf38f79a0c7f5b5492679233556d1c911957146494d52673143f448`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "s", "kind": "base", "block": null, "base_tables": ["sales_records"]}, {"alias": "pi", "kind": "base", "block": null, "base_tables": ["product_information"]}] | [{"type": "INNER", "right": "product_information AS pi", "on": "s.\"Item Code\" = pi.\"Item Code\"", "using": []}] | ["pi.\"Item Name\""] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(DISTINCT STRFTIME('%Y', s."Sales Date")) | [{"table": "sales_records", "column": "Sales Date"}] | [] | False |
| B1 | SUM(CASE WHEN s."Sales Date" >= '2023-01-01' THEN s."Sales volume (kg)" ELSE 0 END) | [{"table": "sales_records", "column": "Sales volume (kg)"}] | [{"table": "sales_records", "column": "Sales Date"}] | False |
| B1 | SUM(CASE WHEN s."Sales Date" >= '2022-01-01' AND s."Sales Date" < '2023-01-01' THEN s."Sales volume (kg)" ELSE 0 END) | [{"table": "sales_records", "column": "Sales volume (kg)"}] | [{"table": "sales_records", "column": "Sales Date"}, {"table": "sales_records", "column": "Sales Date"}] | False |


## S44

类别 `data`；来源 `query_db`；调用 `5d20e1a6379d4db8835bb526b782e9d3`；状态 `success`。

```sql
-- When is Sweet Potato Vine Tips sold? Check its months
SELECT pi."Item Name", strftime('%Y-%m', s."Sales Date") AS ym, ROUND(SUM(s."Sales volume (kg)"),1) AS vol
FROM sales_records s
JOIN product_information pi ON s."Item Code"=pi."Item Code"
WHERE pi."Item Name" IN ('Sweet Potato Vine Tips','Water Spinach','Yunnan Leaf Lettuce','Yellow Chinese Cabbage (2)')
GROUP BY pi."Item Name", ym
ORDER BY pi."Item Name", ym DESC
LIMIT 60
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-047/attempt-01/sql/S44.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-047/attempt-01/sql/S44.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-047/attempt-01/results/S44.rows.jsonl)；完整：True；SHA256：`1d2b2b18eaa8807b036cac464b02c8fd0da9a6d4c0a5a2b6444b97d50df6e07c`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "s", "kind": "base", "block": null, "base_tables": ["sales_records"]}, {"alias": "pi", "kind": "base", "block": null, "base_tables": ["product_information"]}] | [{"type": "INNER", "right": "product_information AS pi", "on": "s.\"Item Code\" = pi.\"Item Code\"", "using": []}] | ["pi.\"Item Name\"", "STRFTIME('%Y-%m', s.\"Sales Date\")"] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | SUM(s."Sales volume (kg)") | [{"table": "sales_records", "column": "Sales volume (kg)"}] | [] | False |


## S45

类别 `data`；来源 `query_db`；调用 `daf6464fe5d74992b8cc27836e83810b`；状态 `success`。

```sql
-- All items active in 2023, with their July 2022 performance
SELECT s."Item Code", pi."Item Name", pi."Category Name",
       ROUND(SUM(CASE WHEN s."Sales Date">='2023-01-01' THEN s."Sales volume (kg)" ELSE 0 END),1) AS vol_2023,
       ROUND(SUM(CASE WHEN strftime('%m', s."Sales Date")='07' AND strftime('%Y', s."Sales Date")='2022' THEN s."Sales volume (kg)" ELSE 0 END),1) AS july22_vol,
       ROUND(SUM(CASE WHEN strftime('%m', s."Sales Date")='07' AND strftime('%Y', s."Sales Date")='2021' THEN s."Sales volume (kg)" ELSE 0 END),1) AS july21_vol,
       ROUND(SUM(CASE WHEN strftime('%m', s."Sales Date")='07' AND strftime('%Y', s."Sales Date")='2020' THEN s."Sales volume (kg)" ELSE 0 END),1) AS july20_vol
FROM sales_records s
JOIN product_information pi ON s."Item Code"=pi."Item Code"
WHERE s."Sales Date">='2023-01-01'
GROUP BY s."Item Code", pi."Item Name", pi."Category Name"
ORDER BY vol_2023 DESC
LIMIT 40
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-047/attempt-01/sql/S45.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-047/attempt-01/sql/S45.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-047/attempt-01/results/S45.rows.jsonl)；完整：True；SHA256：`f0b2b48ce4da153bdad939c3526945724710c857ca2b9b4751f19af8ebb83989`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "s", "kind": "base", "block": null, "base_tables": ["sales_records"]}, {"alias": "pi", "kind": "base", "block": null, "base_tables": ["product_information"]}] | [{"type": "INNER", "right": "product_information AS pi", "on": "s.\"Item Code\" = pi.\"Item Code\"", "using": []}] | ["s.\"Item Code\"", "pi.\"Item Name\"", "pi.\"Category Name\""] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | SUM(CASE WHEN s."Sales Date" >= '2023-01-01' THEN s."Sales volume (kg)" ELSE 0 END) | [{"table": "sales_records", "column": "Sales volume (kg)"}] | [{"table": "sales_records", "column": "Sales Date"}] | False |
| B1 | SUM(CASE WHEN STRFTIME('%m', s."Sales Date") = '07' AND STRFTIME('%Y', s."Sales Date") = '2022' THEN s."Sales volume (kg)" ELSE 0 END) | [{"table": "sales_records", "column": "Sales volume (kg)"}] | [{"table": "sales_records", "column": "Sales Date"}, {"table": "sales_records", "column": "Sales Date"}] | False |
| B1 | SUM(CASE WHEN STRFTIME('%m', s."Sales Date") = '07' AND STRFTIME('%Y', s."Sales Date") = '2021' THEN s."Sales volume (kg)" ELSE 0 END) | [{"table": "sales_records", "column": "Sales volume (kg)"}] | [{"table": "sales_records", "column": "Sales Date"}, {"table": "sales_records", "column": "Sales Date"}] | False |
| B1 | SUM(CASE WHEN STRFTIME('%m', s."Sales Date") = '07' AND STRFTIME('%Y', s."Sales Date") = '2020' THEN s."Sales volume (kg)" ELSE 0 END) | [{"table": "sales_records", "column": "Sales volume (kg)"}] | [{"table": "sales_records", "column": "Sales Date"}, {"table": "sales_records", "column": "Sales Date"}] | False |


## S46

类别 `data`；来源 `query_db`；调用 `0d866eac5901473a940ea9f85bfe8309`；状态 `success`。

```sql
-- Portion items: check their data span and July performance
SELECT pi."Item Name", strftime('%Y', s."Sales Date") AS yr, ROUND(SUM(s."Sales volume (kg)"),1) AS vol
FROM sales_records s
JOIN product_information pi ON s."Item Code"=pi."Item Code"
WHERE pi."Item Name" IN ('Yunnan Leaf Lettuce (portion)','Yunnan Romaine Lettuce (portion)',
  'Water Spinach (portion)','Shanghai Bok Choy (portion)','Sweet Potato Vine Tips (portion)',
  'Milk Bok Choy (portion)','Baby Green Bok Choy (portion)')
GROUP BY pi."Item Name", yr
ORDER BY pi."Item Name", yr
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-047/attempt-01/sql/S46.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-047/attempt-01/sql/S46.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-047/attempt-01/results/S46.rows.jsonl)；完整：True；SHA256：`82609ff6ad4e5bca6a290aa0496fccae182b8e9b2377d83894afd68343a31d7a`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "s", "kind": "base", "block": null, "base_tables": ["sales_records"]}, {"alias": "pi", "kind": "base", "block": null, "base_tables": ["product_information"]}] | [{"type": "INNER", "right": "product_information AS pi", "on": "s.\"Item Code\" = pi.\"Item Code\"", "using": []}] | ["pi.\"Item Name\"", "STRFTIME('%Y', s.\"Sales Date\")"] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | SUM(s."Sales volume (kg)") | [{"table": "sales_records", "column": "Sales volume (kg)"}] | [] | False |


## S47

类别 `data`；来源 `query_db`；调用 `14e458a4ece24c548926149d362c995b`；状态 `success`。

```sql
-- Check July 2022 for portion items correctly
SELECT pi."Item Name", strftime('%Y-%m', s."Sales Date") AS ym, ROUND(SUM(s."Sales volume (kg)"),1) AS vol
FROM sales_records s
JOIN product_information pi ON s."Item Code"=pi."Item Code"
WHERE pi."Item Name" LIKE '%(portion)%'
  AND s."Sales Date" BETWEEN '2022-06-01' AND '2022-09-01'
GROUP BY pi."Item Name", ym
ORDER BY pi."Item Name", ym
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-047/attempt-01/sql/S47.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-047/attempt-01/sql/S47.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-047/attempt-01/results/S47.rows.jsonl)；完整：True；SHA256：`3c3d464aaf161a992a89a96d267e83cc0b640ef2ff7df35e50ed16a3d7e1bb2b`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "s", "kind": "base", "block": null, "base_tables": ["sales_records"]}, {"alias": "pi", "kind": "base", "block": null, "base_tables": ["product_information"]}] | [{"type": "INNER", "right": "product_information AS pi", "on": "s.\"Item Code\" = pi.\"Item Code\"", "using": []}] | ["pi.\"Item Name\"", "STRFTIME('%Y-%m', s.\"Sales Date\")"] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | SUM(s."Sales volume (kg)") | [{"table": "sales_records", "column": "Sales volume (kg)"}] | [] | False |


## S48

类别 `data`；来源 `query_db`；调用 `c05db173ac9841a5900333bb3cfe0207`；状态 `success`。

```sql
-- Actually, check if July data exists for these items
SELECT pi."Item Name", strftime('%m', s."Sales Date") AS mo, strftime('%Y', s."Sales Date") AS yr,
       ROUND(SUM(s."Sales volume (kg)"),1) AS vol
FROM sales_records s
JOIN product_information pi ON s."Item Code"=pi."Item Code"
WHERE pi."Item Name" IN ('Yunnan Leaf Lettuce (portion)','Yunnan Romaine Lettuce (portion)',
  'Water Spinach (portion)','Shanghai Bok Choy (portion)','Sweet Potato Vine Tips (portion)',
  'Milk Bok Choy (portion)','Baby Green Bok Choy (portion)')
  AND strftime('%m', s."Sales Date") = '07'
GROUP BY pi."Item Name", yr
ORDER BY pi."Item Name", yr
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-047/attempt-01/sql/S48.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-047/attempt-01/sql/S48.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-047/attempt-01/results/S48.rows.jsonl)；完整：True；SHA256：`799dd0715c23b0077f9f59545e13866bd389c107fca2f1d056fa2e5723021283`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "s", "kind": "base", "block": null, "base_tables": ["sales_records"]}, {"alias": "pi", "kind": "base", "block": null, "base_tables": ["product_information"]}] | [{"type": "INNER", "right": "product_information AS pi", "on": "s.\"Item Code\" = pi.\"Item Code\"", "using": []}] | ["pi.\"Item Name\"", "STRFTIME('%Y', s.\"Sales Date\")"] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | SUM(s."Sales volume (kg)") | [{"table": "sales_records", "column": "Sales volume (kg)"}] | [] | False |


## S49

类别 `data`；来源 `query_db`；调用 `851c0d794c834084bb086850e18b3d33`；状态 `success`。

```sql
-- Monthly 2023 trend for top 2023 items
SELECT pi."Item Name", strftime('%Y-%m', s."Sales Date") AS ym,
       ROUND(SUM(s."Sales volume (kg)")/COUNT(DISTINCT s."Sales Date"),2) AS avg_daily
FROM sales_records s
JOIN product_information pi ON s."Item Code"=pi."Item Code"
WHERE s."Sales Date" >= '2022-10-01'
  AND s."Item Code" IN (
    106949711300259,102900011030059,102900011031100,102900011016701,
    102900011032251,102900011030097,102900005118831,102900005116714,
    102900011034231,102900011030110,102900005116257,102900011034330
  )
GROUP BY pi."Item Name", ym
ORDER BY pi."Item Name", ym
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-047/attempt-01/sql/S49.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-047/attempt-01/sql/S49.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-047/attempt-01/results/S49.rows.jsonl)；完整：True；SHA256：`d864709c2c5f176194abb18b41381d82a6b27860c876349e9dd9ab9ac742fe54`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "s", "kind": "base", "block": null, "base_tables": ["sales_records"]}, {"alias": "pi", "kind": "base", "block": null, "base_tables": ["product_information"]}] | [{"type": "INNER", "right": "product_information AS pi", "on": "s.\"Item Code\" = pi.\"Item Code\"", "using": []}] | ["pi.\"Item Name\"", "STRFTIME('%Y-%m', s.\"Sales Date\")"] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | SUM(s."Sales volume (kg)") | [{"table": "sales_records", "column": "Sales volume (kg)"}] | [] | False |
| B1 | COUNT(DISTINCT s."Sales Date") | [{"table": "sales_records", "column": "Sales Date"}] | [] | False |


## S50

类别 `data`；来源 `query_db`；调用 `6515c3e27a144fa0ae56fc754366b8f2`；状态 `success`。

```sql
-- Check the July 2022 volumes for the currently-relevant items (both full and portion versions)
SELECT pi."Item Name", 
       ROUND(SUM(CASE WHEN strftime('%m',s."Sales Date")='07' AND strftime('%Y',s."Sales Date")='2022' THEN s."Sales volume (kg)" ELSE 0 END),1) AS july22,
       ROUND(SUM(CASE WHEN strftime('%m',s."Sales Date")='07' AND strftime('%Y',s."Sales Date")='2021' THEN s."Sales volume (kg)" ELSE 0 END),1) AS july21,
       ROUND(SUM(CASE WHEN strftime('%m',s."Sales Date")='07' AND strftime('%Y',s."Sales Date")='2020' THEN s."Sales volume (kg)" ELSE 0 END),1) AS july20
FROM sales_records s
JOIN product_information pi ON s."Item Code"=pi."Item Code"
WHERE pi."Item Name" IN (
  'Yunnan Leaf Lettuce','Water Spinach','Sweet Potato Vine Tips',
  'Broccoli','Purple Eggplant (2)','Spiral chili pepper',
  'Yunnan Romaine Lettuce','Shanghai Bok Choy','Yellow Chinese Cabbage (2)',
  'Enoki Mushroom (box)','White Button Mushroom (box)','Baby Bok Choy',
  'Spinach (portion)','Milk Bok Choy (portion)','Yunnan Leaf Lettuce (portion)',
  'Yunnan Romaine Lettuce (portion)','Water Spinach (portion)','Bird''s-eye Chili (portion)',
  'Spiral chili pepper (portion)','Wuhu green pepper (1)'
)
GROUP BY pi."Item Name"
ORDER BY july22 DESC
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-047/attempt-01/sql/S50.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-047/attempt-01/sql/S50.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-047/attempt-01/results/S50.rows.jsonl)；完整：True；SHA256：`79351d8f7c24cd6dd172f9f3ff7199e26688a2efe48ad83f3913040edb9f99d4`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "s", "kind": "base", "block": null, "base_tables": ["sales_records"]}, {"alias": "pi", "kind": "base", "block": null, "base_tables": ["product_information"]}] | [{"type": "INNER", "right": "product_information AS pi", "on": "s.\"Item Code\" = pi.\"Item Code\"", "using": []}] | ["pi.\"Item Name\""] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | SUM(CASE WHEN STRFTIME('%m', s."Sales Date") = '07' AND STRFTIME('%Y', s."Sales Date") = '2022' THEN s."Sales volume (kg)" ELSE 0 END) | [{"table": "sales_records", "column": "Sales volume (kg)"}] | [{"table": "sales_records", "column": "Sales Date"}, {"table": "sales_records", "column": "Sales Date"}] | False |
| B1 | SUM(CASE WHEN STRFTIME('%m', s."Sales Date") = '07' AND STRFTIME('%Y', s."Sales Date") = '2021' THEN s."Sales volume (kg)" ELSE 0 END) | [{"table": "sales_records", "column": "Sales volume (kg)"}] | [{"table": "sales_records", "column": "Sales Date"}, {"table": "sales_records", "column": "Sales Date"}] | False |
| B1 | SUM(CASE WHEN STRFTIME('%m', s."Sales Date") = '07' AND STRFTIME('%Y', s."Sales Date") = '2020' THEN s."Sales volume (kg)" ELSE 0 END) | [{"table": "sales_records", "column": "Sales volume (kg)"}] | [{"table": "sales_records", "column": "Sales Date"}, {"table": "sales_records", "column": "Sales Date"}] | False |


## S51

类别 `data`；来源 `python`；调用 `43b45f31d7b2428b9df59bc773e895f5`；状态 `success`。

```sql

    SELECT pi."Item Name" AS name, strftime('%Y-%m', s."Sales Date") AS ym,
           SUM(s."Sales volume (kg)")/COUNT(DISTINCT s."Sales Date") AS avg_daily
    FROM sales_records s
    JOIN product_information pi ON s."Item Code"=pi."Item Code"
    WHERE s."Sales Date" >= '2022-10-01'
    GROUP BY pi."Item Name", ym
    HAVING SUM(s."Sales volume (kg)") > 50
    ORDER BY pi."Item Name", ym

```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-047/attempt-01/sql/S51.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-047/attempt-01/sql/S51.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-047/attempt-01/results/S51.rows.jsonl)；完整：True；SHA256：`c200f35f5e3272a4a1ca46fa7e57d0ba4428861af9572504cfe2b980e451f49d`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "s", "kind": "base", "block": null, "base_tables": ["sales_records"]}, {"alias": "pi", "kind": "base", "block": null, "base_tables": ["product_information"]}] | [{"type": "INNER", "right": "product_information AS pi", "on": "s.\"Item Code\" = pi.\"Item Code\"", "using": []}] | ["pi.\"Item Name\"", "STRFTIME('%Y-%m', s.\"Sales Date\")"] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | SUM(s."Sales volume (kg)") | [{"table": "sales_records", "column": "Sales volume (kg)"}] | [] | False |
| B1 | COUNT(DISTINCT s."Sales Date") | [{"table": "sales_records", "column": "Sales Date"}] | [] | False |
| B1 | SUM(s."Sales volume (kg)") | [{"table": "sales_records", "column": "Sales volume (kg)"}] | [] | False |


## S52

类别 `data`；来源 `query_db`；调用 `d3593253e0f447ccb7265d4c9f5ee258`；状态 `success`。

```sql
-- Monthly pattern for Enoki Mushroom (box) and other top 2023 items
SELECT pi."Item Name", strftime('%m', s."Sales Date") AS mo, 
       ROUND(SUM(s."Sales volume (kg)")/COUNT(DISTINCT s."Sales Date"),2) AS avg_daily
FROM sales_records s
JOIN product_information pi ON s."Item Code"=pi."Item Code"
WHERE pi."Item Name" IN ('Enoki Mushroom (box)','White Button Mushroom (box)','Bird''s-eye Chili (portion)',
  'Spinach (portion)','Baby Bok Choy','Yunnan Leaf Lettuce (portion)','Yunnan Romaine Lettuce (portion)',
  'Milk Bok Choy (portion)','Wrinkled Pepper (portion)')
  AND s."Sales Date" >= '2022-01-01'
GROUP BY pi."Item Name", mo
ORDER BY pi."Item Name", mo
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-047/attempt-01/sql/S52.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-047/attempt-01/sql/S52.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-047/attempt-01/results/S52.rows.jsonl)；完整：True；SHA256：`dc8d2dd0a16a60fa7981051e17014d73b21ea9aca990d698b180f0282f7ccf70`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "s", "kind": "base", "block": null, "base_tables": ["sales_records"]}, {"alias": "pi", "kind": "base", "block": null, "base_tables": ["product_information"]}] | [{"type": "INNER", "right": "product_information AS pi", "on": "s.\"Item Code\" = pi.\"Item Code\"", "using": []}] | ["pi.\"Item Name\"", "STRFTIME('%m', s.\"Sales Date\")"] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | SUM(s."Sales volume (kg)") | [{"table": "sales_records", "column": "Sales volume (kg)"}] | [] | False |
| B1 | COUNT(DISTINCT s."Sales Date") | [{"table": "sales_records", "column": "Sales Date"}] | [] | False |


## S53

类别 `data`；来源 `query_db`；调用 `2694437de7de41be9eddb2b91b43b194`；状态 `success`。

```sql
-- Check the correlation between Water Spinach (portion) and Water Spinach - are they the same product?
-- Also check if Water Spinach is still sold in 2023
SELECT pi."Item Name", strftime('%Y', s."Sales Date") AS yr, ROUND(SUM(s."Sales volume (kg)"),1) AS vol
FROM sales_records s
JOIN product_information pi ON s."Item Code"=pi."Item Code"
WHERE pi."Item Name" IN ('Water Spinach','Water Spinach (portion)','Sweet Potato Vine Tips','Sweet Potato Vine Tips (portion)')
GROUP BY pi."Item Name", yr
ORDER BY pi."Item Name", yr
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-047/attempt-01/sql/S53.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-047/attempt-01/sql/S53.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-047/attempt-01/results/S53.rows.jsonl)；完整：True；SHA256：`c51c548ac0ad02045be747dcd3d52381c62c5d3c3cef1d654eba1098f4756fa4`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "s", "kind": "base", "block": null, "base_tables": ["sales_records"]}, {"alias": "pi", "kind": "base", "block": null, "base_tables": ["product_information"]}] | [{"type": "INNER", "right": "product_information AS pi", "on": "s.\"Item Code\" = pi.\"Item Code\"", "using": []}] | ["pi.\"Item Name\"", "STRFTIME('%Y', s.\"Sales Date\")"] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | SUM(s."Sales volume (kg)") | [{"table": "sales_records", "column": "Sales volume (kg)"}] | [] | False |


## S54

类别 `data`；来源 `query_db`；调用 `e02f409eeb884a628f231ba595cde463`；状态 `failed`。

```sql
-- Monthly pattern for key items - focused on seasonal shape
SELECT pi."Item Name", strftime('%m', s."Sales Date") AS mo, 
       ROUND(AVG(CASE WHEN strftime('%Y', s."Sales Date")>='2022' THEN s."Sales volume (kg)"/COUNT(DISTINCT s."Sales Date") END),2) AS avg_daily
FROM sales_records s
JOIN product_information pi ON s."Item Code"=pi."Item Code"
WHERE pi."Item Name" IN ('Enoki Mushroom (box)','White Button Mushroom (box)','Bird''s-eye Chili (portion)',
  'Yunnan Leaf Lettuce (portion)','Yunnan Romaine Lettuce (portion)','Milk Bok Choy (portion)',
  'Wrinkled Pepper (portion)','Water Spinach','Sweet Potato Vine Tips')
GROUP BY pi."Item Name", mo
ORDER BY pi."Item Name", CAST(mo AS INT)
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-047/attempt-01/sql/S54.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-047/attempt-01/sql/S54.parameters.json)。

错误：`OperationalError('misuse of aggregate function COUNT()')`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "s", "kind": "base", "block": null, "base_tables": ["sales_records"]}, {"alias": "pi", "kind": "base", "block": null, "base_tables": ["product_information"]}] | [{"type": "INNER", "right": "product_information AS pi", "on": "s.\"Item Code\" = pi.\"Item Code\"", "using": []}] | ["pi.\"Item Name\"", "STRFTIME('%m', s.\"Sales Date\")"] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | AVG(CASE WHEN STRFTIME('%Y', s."Sales Date") >= '2022' THEN s."Sales volume (kg)" / COUNT(DISTINCT s."Sales Date") END) | [{"table": "sales_records", "column": "Sales volume (kg)"}, {"table": "sales_records", "column": "Sales Date"}] | [{"table": "sales_records", "column": "Sales Date"}] | False |
| B1 | COUNT(DISTINCT s."Sales Date") | [{"table": "sales_records", "column": "Sales Date"}] | [] | False |


## S55

类别 `data`；来源 `query_db`；调用 `a0104fab9c024f4b8f382a1b2cdc9501`；状态 `success`。

```sql
-- Monthly pattern for key items
SELECT pi."Item Name", strftime('%m', s."Sales Date") AS mo, 
       ROUND(SUM(s."Sales volume (kg)")/COUNT(DISTINCT s."Sales Date"),2) AS avg_daily
FROM sales_records s
JOIN product_information pi ON s."Item Code"=pi."Item Code"
WHERE pi."Item Name" IN ('Enoki Mushroom (box)','White Button Mushroom (box)','Bird''s-eye Chili (portion)',
  'Yunnan Leaf Lettuce (portion)','Yunnan Romaine Lettuce (portion)','Milk Bok Choy (portion)',
  'Wrinkled Pepper (portion)','Water Spinach','Sweet Potato Vine Tips')
  AND s."Sales Date" >= '2022-01-01'
GROUP BY pi."Item Name", mo
ORDER BY pi."Item Name", CAST(mo AS INT)
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-047/attempt-01/sql/S55.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-047/attempt-01/sql/S55.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-047/attempt-01/results/S55.rows.jsonl)；完整：True；SHA256：`658a50e23fa50e232084ac2132170706fa04468b58c19ebce6daa93660c7e5d4`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "s", "kind": "base", "block": null, "base_tables": ["sales_records"]}, {"alias": "pi", "kind": "base", "block": null, "base_tables": ["product_information"]}] | [{"type": "INNER", "right": "product_information AS pi", "on": "s.\"Item Code\" = pi.\"Item Code\"", "using": []}] | ["pi.\"Item Name\"", "STRFTIME('%m', s.\"Sales Date\")"] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | SUM(s."Sales volume (kg)") | [{"table": "sales_records", "column": "Sales volume (kg)"}] | [] | False |
| B1 | COUNT(DISTINCT s."Sales Date") | [{"table": "sales_records", "column": "Sales Date"}] | [] | False |


## S56

类别 `data`；来源 `python`；调用 `87aee1ed18d34e3ebe6539dbff1f09f1`；状态 `success`。

```sql

    SELECT pi."Item Name" AS name, strftime('%m', s."Sales Date") AS mo, 
           ROUND(SUM(s."Sales volume (kg)")/COUNT(DISTINCT s."Sales Date"),2) AS avg_daily
    FROM sales_records s
    JOIN product_information pi ON s."Item Code"=pi."Item Code"
    WHERE pi."Item Name" IN ('Enoki Mushroom (box)','White Button Mushroom (box)','Bird''s-eye Chili (portion)',
      'Yunnan Leaf Lettuce (portion)','Yunnan Romaine Lettuce (portion)','Milk Bok Choy (portion)',
      'Wrinkled Pepper (portion)','Water Spinach','Sweet Potato Vine Tips')
      AND s."Sales Date" >= '2022-01-01'
    GROUP BY pi."Item Name", mo
    ORDER BY pi."Item Name", CAST(mo AS INT)

```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-047/attempt-01/sql/S56.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-047/attempt-01/sql/S56.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-047/attempt-01/results/S56.rows.jsonl)；完整：True；SHA256：`658a50e23fa50e232084ac2132170706fa04468b58c19ebce6daa93660c7e5d4`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "s", "kind": "base", "block": null, "base_tables": ["sales_records"]}, {"alias": "pi", "kind": "base", "block": null, "base_tables": ["product_information"]}] | [{"type": "INNER", "right": "product_information AS pi", "on": "s.\"Item Code\" = pi.\"Item Code\"", "using": []}] | ["pi.\"Item Name\"", "STRFTIME('%m', s.\"Sales Date\")"] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | SUM(s."Sales volume (kg)") | [{"table": "sales_records", "column": "Sales volume (kg)"}] | [] | False |
| B1 | COUNT(DISTINCT s."Sales Date") | [{"table": "sales_records", "column": "Sales Date"}] | [] | False |


## S57

类别 `data`；来源 `python`；调用 `f3bfa39177f445019332ce323a0aff03`；状态 `success`。

```sql
SELECT strftime('%Y-%m-%d', "Sales Date") AS d, pi."Category Name" AS cat, SUM("Sales volume (kg)") AS vol FROM sales_records s JOIN product_information pi ON s."Item Code"=pi."Item Code" GROUP BY d, cat
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-047/attempt-01/sql/S57.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-047/attempt-01/sql/S57.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-047/attempt-01/results/S57.rows.jsonl)；完整：True；SHA256：`3d69345160540151f3533312a2a8b809e915778d8c07d0d5ea2477fbe491463e`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "s", "kind": "base", "block": null, "base_tables": ["sales_records"]}, {"alias": "pi", "kind": "base", "block": null, "base_tables": ["product_information"]}] | [{"type": "INNER", "right": "product_information AS pi", "on": "s.\"Item Code\" = pi.\"Item Code\"", "using": []}] | ["STRFTIME('%Y-%m-%d', \"Sales Date\")", "pi.\"Category Name\""] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | SUM("Sales volume (kg)") | [{"table": "sales_records", "column": "Sales volume (kg)"}] | [] | False |

