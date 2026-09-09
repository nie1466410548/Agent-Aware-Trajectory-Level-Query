# dacomp-025

To increase total revenue, the supermarket needs to avoid loss-making sales as much as pos…

运行：已提交。官方未评分。全部 SQL 尝试/成功 78/77；数据 SQL 76/75；Python 7 次。

完整原题：

To increase total revenue, the supermarket needs to avoid loss-making sales as much as possible. Using previous years' summer data, if procurement on 2023-07-01 follows the sales volume on 2023-06-30, which items (Item Codes) clearly need their procurement quantities reduced?

| 表 | 行数 | 列数 |
| --- | --- | --- |
| product_information | 251 | 4 |
| product_loss | 251 | 3 |
| purchase_price | 55982 | 3 |
| sales_records | 878503 | 7 |


实际路线（分析者依据 SQL/源码概括，不代表 Agent 自述）：核查 6 月 30 日销售和历年夏季价格 → SQL 关联批发价/损耗率计算单位盈利 → 按商品与月份汇总 → 深查低盈利商品并用 Python 绘制 SQL 结果。

数据库大小：135,073,792 字节。

## 数据 SQL

| SQL | 状态 | 基础表 | Join 输入/类型 | GROUP BY | 聚合表达式 | 结果行数 | 数据库 ms |
| --- | --- | --- | --- | --- | --- | --- | --- |
| [S3/Q1](#s3) | success | ["product_information"] | 0 / {} | [] | [] | 5 | 0.32 |
| [S4/Q2](#s4) | success | ["product_loss"] | 0 / {} | [] | [] | 5 | 0.304 |
| [S5/Q3](#s5) | success | ["purchase_price"] | 0 / {} | [] | [] | 5 | 0.313 |
| [S6/Q4](#s6) | success | ["sales_records"] | 0 / {} | [] | [] | 5 | 0.331 |
| [S7/Q5](#s7) | success | ["sales_records"] | 0 / {} | [] | [] | 4 | 578.334 |
| [S8/Q6](#s8) | success | ["purchase_price"] | 0 / {} | [] | [] | 4 | 32.09 |
| [S9/Q7](#s9) | success | ["sales_records"] | 0 / {} | [] | [] | 36 | 622.684 |
| [S10/Q8](#s10) | success | ["purchase_price"] | 0 / {} | [] | [] | 36 | 34.251 |
| [S11/Q9](#s11) | success | ["sales_records"] | 0 / {} | [] | [] | 2 | 82.709 |
| [S12/Q10](#s12) | success | ["sales_records"] | 0 / {} | [] | [] | 2 | 89.91 |
| [S13/Q11](#s13) | success | ["sales_records"] | 0 / {} | [] | ["COUNT(DISTINCT \"Item Code\")"] | 1 | 123.332 |
| [S14/Q12](#s14) | success | ["purchase_price"] | 0 / {} | [] | ["COUNT(DISTINCT \"Item Code\")"] | 1 | 7.711 |
| [S15/Q13](#s15) | success | ["product_information"] | 0 / {} | [] | ["COUNT(DISTINCT \"Item Code\")"] | 1 | 0.361 |
| [S16/Q14](#s16) | success | ["product_loss"] | 0 / {} | [] | ["COUNT(DISTINCT \"Item Code\")"] | 1 | 0.366 |
| [S17/Q15](#s17) | success | ["sales_records"] | 0 / {} | [] | [] | 10 | 93.537 |
| [S18/Q16](#s18) | success | ["purchase_price"] | 0 / {} | [] | [] | 0 | 5.64 |
| [S19/Q17](#s19) | success | ["product_loss"] | 0 / {} | [] | [] | 10 | 0.319 |
| [S20/Q18](#s20) | success | ["purchase_price"] | 0 / {} | ["\"Date\""] | ["COUNT(*)"] | 180 | 6.699 |
| [S21/Q19](#s21) | success | ["sales_records"] | 0 / {} | ["\"Sales Date\""] | ["COUNT(*)"] | 180 | 115.61 |
| [S22/Q20](#s22) | success | ["purchase_price"] | 0 / {} | ["\"Date\""] | [] | 30 | 6.222 |
| [S23/Q21](#s23) | success | ["sales_records"] | 0 / {} | ["\"Sales Date\""] | [] | 30 | 97.598 |
| [S24/Q22](#s24) | success | ["purchase_price"] | 0 / {} | [] | [] | 6 | 3.358 |
| [S25/Q23](#s25) | success | ["product_loss"] | 0 / {} | [] | [] | 1 | 0.493 |
| [S26/Q24](#s26) | success | ["sales_records"] | 0 / {} | ["\"Sales Date\""] | ["AVG(\"Unit price (yuan/kg)\")", "SUM(\"Sales volume (kg)\")", "COUNT(*)"] | 64 | 59.247 |
| [S27/Q25](#s27) | success | ["purchase_price"] | 0 / {} | [] | [] | 10 | 3.504 |
| [S28/Q26](#s28) | success | ["purchase_price"] | 0 / {} | ["\"Date\""] | ["AVG(\"Wholesale price (yuan/kg)\")"] | 67 | 3.487 |
| [S29/Q27](#s29) | success | ["product_information", "sales_records"] | 2 / {'LEFT': 1} | ["s.\"Item Code\""] | ["SUM(s.\"Sales volume (kg)\")"] | 0 | 93.526 |
| [S30/Q28](#s30) | success | ["sales_records"] | 0 / {} | [] | [] | 2 | 194.483 |
| [S31/Q29](#s31) | success | ["sales_records"] | 0 / {} | [] | [] | 5 | 76.715 |
| [S32/Q30](#s32) | success | ["product_information", "sales_records"] | 2 / {'LEFT': 1} | ["s.\"Item Code\""] | ["SUM(s.\"Sales volume (kg)\")"] | 39 | 149.373 |
| [S33/Q31](#s33) | success | ["sales_records"] | 0 / {} | [] | [] | 2 | 186.53 |
| [S34/Q32](#s34) | success | ["purchase_price", "sales_records"] | 2 / {'LEFT': 1} | [] | ["COUNT(*)"] | 1 | 163542.905 |
| [S35/Q33](#s35) | success | ["product_loss", "purchase_price", "sales_records"] | 3 / {'LEFT': 2} | [] | ["COUNT(*)"] | 1 | 14529.073 |
| [S36/Q34](#s36) | success | ["product_loss", "purchase_price", "sales_records"] | 3 / {'LEFT': 2} | [] | ["COUNT(*)"] | 1 | 17633.083 |
| [S37/Q35](#s37) | success | ["product_loss", "purchase_price", "sales_records"] | 3 / {'LEFT': 2} | [] | ["COUNT(*)"] | 1 | 13155.853 |
| [S38/Q36](#s38) | success | ["product_loss", "purchase_price", "sales_records"] | 4 / {'INNER': 1, 'LEFT': 2} | ["\"Item Code\""] | ["COUNT(*)", "SUM(CASE WHEN up < wp / (1.0 - lr / 100.0) THEN 1 ELSE 0 END)", "AVG(up - wp / (1.0 - lr / 100.0))", "COUNT(*)", "SUM(CASE WHEN up < wp / (1.0 - lr / 100.0) THEN 1 ELSE 0 END)"] | 34 | 23775.685 |
| [S39/Q37](#s39) | success | ["product_information", "sales_records"] | 2 / {'LEFT': 1} | [] | [] | 39 | 143.352 |
| [S40/Q38](#s40) | success | ["product_loss", "purchase_price", "sales_records"] | 4 / {'INNER': 1, 'LEFT': 2} | ["\"Item Code\""] | ["COUNT(*)", "SUM(CASE WHEN up < wp / (1.0 - lr / 100.0) THEN 1 ELSE 0 END)", "AVG(up - wp / (1.0 - lr / 100.0))", "MIN(up - wp / (1.0 - lr / 100.0))", "COUNT(*)", "SUM(CASE WHEN up < wp / (1.0 - lr / 100.0) THEN 1 ELSE 0 END)"] | 34 | 23875.305 |
| [S41/Q39](#s41) | success | ["product_loss", "purchase_price", "sales_records"] | 4 / {'INNER': 1, 'LEFT': 2} | ["\"Item Code\""] | ["COUNT(*)", "AVG(up - wp / (1.0 - lr / 100.0))", "AVG(up)", "AVG(wp / (1.0 - lr / 100.0))", "COUNT(*)", "COUNT(*)", "SUM(CASE WHEN up < wp / (1.0 - lr / 100.0) THEN 1 ELSE 0 END)", "SUM(CASE WHEN discount = 'Yes' THEN 1 ELSE 0 END)"] | 34 | 23797.802 |
| [S42/Q40](#s42) | success | ["product_loss", "purchase_price", "sales_records"] | 4 / {'INNER': 1, 'LEFT': 2} | ["\"Item Code\""] | ["COUNT(*)", "SUM(CASE WHEN up < wp / (1.0 - lr / 100.0) THEN 1 ELSE 0 END)", "COUNT(*)", "SUM(CASE WHEN up < wp / (1.0 - lr / 100.0) THEN 1 ELSE 0 END)"] | 34 | 23734.643 |
| [S43/Q41](#s43) | success | ["product_information", "product_loss"] | 2 / {'LEFT': 1} | [] | [] | 5 | 0.558 |
| [S44/Q42](#s44) | success | ["product_information", "sales_records"] | 2 / {'LEFT': 1} | ["s.\"Item Code\""] | ["SUM(s.\"Sales volume (kg)\")"] | 39 | 142.984 |
| [S45/Q43](#s45) | success | ["sales_records"] | 0 / {} | [] | [] | 2 | 56.133 |
| [S46/Q44](#s46) | success | ["purchase_price"] | 0 / {} | [] | [] | 4 | 3.331 |
| [S47/Q45](#s47) | success | ["product_loss"] | 0 / {} | [] | [] | 1 | 0.346 |
| [S48/Q46](#s48) | success | ["product_information", "product_loss", "purchase_price", "sales_records"] | 3 / {'LEFT': 3} | [] | [] | 5 | 44865.365 |
| [S49/Q47](#s49) | success | ["sales_records"] | 0 / {} | ["s.\"Item Code\""] | ["COUNT(*)"] | 0 | 96.062 |
| [S50/Q48](#s50) | success | ["purchase_price"] | 0 / {} | ["\"Item Code\""] | ["COUNT(*)"] | 5 | 6.092 |
| [S51/Q49](#s51) | success | ["product_information", "product_loss", "purchase_price", "sales_records"] | 4 / {'LEFT': 3} | [] | [] | 554 | 295.224 |
| [S52/Q50](#s52) | success | ["product_information", "product_loss", "purchase_price", "sales_records"] | 4 / {'LEFT': 3} | ["s.\"Item Code\""] | ["COUNT(*)", "SUM(s.\"Sales volume (kg)\")", "SUM(CASE WHEN s.\"Unit price (yuan/kg)\" < pp.\"Wholesale price (yuan/kg)\" / (1.0 - pl.\"Loss Rate (%)\" / 100.0) THEN 1 ELSE 0 END)", "SUM(s.\"Sales volume (kg)\" * (s.\"Unit price (yuan/kg)\" - pp.\"Wholesale price (yuan/kg)\") / (1.0 - pl.\"Loss Rate (%)\" / 100.0))", "AVG(s.\"Unit price (yuan/kg)\" - pp.\"Wholesale price (yuan/kg)\")"] | 13 | 293.751 |
| [S53/Q51](#s53) | success | ["product_loss", "purchase_price", "sales_records"] | 4 / {'INNER': 1, 'LEFT': 2} | ["\"Item Code\""] | ["COUNT(*)", "SUM(vol * profit)", "AVG(profit)", "SUM(CASE WHEN profit < 0 THEN 1 ELSE 0 END)", "COUNT(*)", "SUM(vol)", "COUNT(*)", "SUM(CASE WHEN profit < 0 THEN 1 ELSE 0 END)", "SUM(CASE WHEN profit < 0 THEN vol ELSE 0 END)", "SUM(CASE WHEN profit < 0 THEN 1 ELSE 0 END)"] | 34 | 23844.498 |
| [S54/Q52](#s54) | success | ["product_loss", "purchase_price", "sales_records"] | 4 / {'INNER': 1, 'LEFT': 2} | ["\"Item Code\"", "yr"] | ["COUNT(*)", "AVG(profit)", "COUNT(*)", "SUM(CASE WHEN profit < 0 THEN 1 ELSE 0 END)"] | 13 | 1234.435 |
| [S55/Q53](#s55) | success | ["product_loss", "purchase_price", "sales_records"] | 4 / {'INNER': 1, 'LEFT': 2} | ["\"Item Code\""] | ["COUNT(*)", "AVG(profit)", "SUM(CASE WHEN profit < 0 THEN 1 ELSE 0 END)", "SUM(vol * profit)", "COUNT(*)", "COUNT(*)", "SUM(CASE WHEN profit < 0 THEN 1 ELSE 0 END)"] | 33 | 9874.277 |
| [S56/Q54](#s56) | success | ["product_loss", "purchase_price", "sales_records"] | 4 / {'INNER': 1, 'LEFT': 2} | ["\"Item Code\""] | ["COUNT(*)", "AVG(profit)", "SUM(vol * profit)", "COUNT(*)", "SUM(CASE WHEN profit < 0 THEN 1 ELSE 0 END)"] | 34 | 9848.43 |
| [S57/Q55](#s57) | success | ["purchase_price", "sales_records"] | 3 / {'INNER': 1, 'LEFT': 1} | ["\"Item Code\""] | ["COUNT(*)", "AVG(profit_simple)", "SUM(CASE WHEN profit_simple < 0 THEN 1 ELSE 0 END)", "COUNT(*)", "SUM(CASE WHEN profit_simple < 0 THEN 1 ELSE 0 END)"] | 15 | 9967.115 |
| [S58/Q56](#s58) | success | ["purchase_price", "sales_records"] | 3 / {'INNER': 1, 'LEFT': 1} | ["\"Item Code\""] | ["COUNT(*)", "AVG(profit_simple)", "COUNT(*)", "SUM(CASE WHEN profit_simple < 0 THEN 1 ELSE 0 END)"] | 2 | 438.254 |
| [S59/Q57](#s59) | success | ["purchase_price"] | 0 / {} | [] | [] | 10 | 3.374 |
| [S60/Q58](#s60) | success | ["purchase_price"] | 0 / {} | [] | [] | 6 | 3.323 |
| [S61/Q59](#s61) | success | ["sales_records"] | 0 / {} | [] | [] | 11 | 59.59 |
| [S62/Q60](#s62) | success | ["sales_records"] | 0 / {} | [] | [] | 2 | 55.552 |
| [S63/Q61](#s63) | success | ["product_loss", "purchase_price", "sales_records"] | 3 / {'LEFT': 2} | ["\"Item Code\"", "ym"] | ["COUNT(*)", "AVG(profit)", "AVG(up)", "AVG(wp / (1.0 - lr / 100.0))", "COUNT(*)", "SUM(CASE WHEN profit < 0 THEN 1 ELSE 0 END)"] | 5 | 220.023 |
| [S64/Q62](#s64) | success | ["product_loss", "purchase_price", "sales_records"] | 4 / {'INNER': 1, 'LEFT': 2} | ["\"Item Code\"", "mo"] | ["COUNT(*)", "AVG(profit)", "COUNT(*)", "SUM(CASE WHEN profit < 0 THEN 1 ELSE 0 END)"] | 20 | 7211.102 |
| [S65/Q63](#s65) | success | ["product_information", "product_loss", "purchase_price", "sales_records"] | 5 / {'INNER': 1, 'LEFT': 6} | ["s.\"Item Code\"", "\"Item Code\"", "\"Item Code\""] | ["SUM(s.\"Sales volume (kg)\")", "COUNT(*)", "AVG(profit)", "SUM(vol * profit)", "COUNT(*)", "SUM(CASE WHEN profit < 0 THEN 1 ELSE 0 END)", "COUNT(*)", "AVG(profit)", "SUM(vol * profit)", "COUNT(*)", "SUM(CASE WHEN profit < 0 THEN 1 ELSE 0 END)"] | 39 | 33694.618 |
| [S66/Q64](#s66) | success | ["product_information", "product_loss", "purchase_price", "sales_records"] | 5 / {'INNER': 1, 'LEFT': 6} | ["s.\"Item Code\"", "\"Item Code\"", "\"Item Code\""] | ["SUM(s.\"Sales volume (kg)\")", "COUNT(*)", "AVG(profit)", "SUM(vol * profit)", "COUNT(*)", "SUM(CASE WHEN profit < 0 THEN 1 ELSE 0 END)", "COUNT(*)", "AVG(profit)", "SUM(vol * profit)", "COUNT(*)", "SUM(CASE WHEN profit < 0 THEN 1 ELSE 0 END)"] | 39 | 33625.941 |
| [S67/Q65](#s67) | success | ["product_information", "product_loss", "purchase_price", "sales_records"] | 4 / {'INNER': 1, 'LEFT': 4} | ["s.\"Item Code\"", "\"Item Code\""] | ["SUM(s.\"Sales volume (kg)\")", "COUNT(*)", "AVG(profit)", "SUM(vol * profit)", "COUNT(*)", "SUM(CASE WHEN profit < 0 THEN 1 ELSE 0 END)"] | 39 | 10108.543 |
| [S68/Q66](#s68) | success | ["product_information", "product_loss", "purchase_price", "sales_records"] | 4 / {'INNER': 1, 'LEFT': 4} | ["s.\"Item Code\"", "\"Item Code\""] | ["SUM(s.\"Sales volume (kg)\")", "COUNT(*)", "AVG(profit)", "SUM(vol * profit)", "COUNT(*)", "SUM(CASE WHEN profit < 0 THEN 1 ELSE 0 END)"] | 39 | 10107.06 |
| [S69/Q67](#s69) | failed | ["product_information", "product_loss", "purchase_price", "sales_records"] | 4 / {'LEFT': 3} | ["s.\"Item Code\""] | ["MAX(pp2.\"Date\")", "SUM(s.\"Sales volume (kg)\")", "AVG(s.\"Unit price (yuan/kg)\")"] | unknown | 未取得；调用总时长 0.302 ms |
| [S70/Q68](#s70) | success | ["product_information", "product_loss", "purchase_price", "sales_records"] | 4 / {'LEFT': 3} | ["\"Item Code\"", "s.\"Item Code\""] | ["MAX(\"Date\")", "SUM(s.\"Sales volume (kg)\")", "AVG(s.\"Unit price (yuan/kg)\")"] | 10 | 232.418 |
| [S71/Q69](#s71) | success | ["sales_records"] | 0 / {} | [] | [] | 14 | 55.169 |
| [S72/Q70](#s72) | success | ["purchase_price"] | 0 / {} | [] | [] | 10 | 3.359 |
| [S73/Q71](#s73) | success | ["product_loss", "purchase_price", "sales_records"] | 3 / {'LEFT': 2} | ["yr", "mo"] | ["COUNT(*)", "AVG(profit)", "COUNT(*)", "SUM(CASE WHEN profit < 0 THEN 1 ELSE 0 END)"] | 8 | 228.591 |
| [S74/Q72](#s74) | success | ["product_information", "product_loss", "purchase_price", "sales_records"] | 4 / {'LEFT': 3} | ["\"Item Code\"", "s.\"Item Code\""] | ["MAX(\"Date\")", "SUM(s.\"Sales volume (kg)\")", "AVG(s.\"Unit price (yuan/kg)\")"] | 39 | 230.095 |
| [S75/Q73](#s75) | success | ["product_loss", "purchase_price", "sales_records"] | 3 / {'LEFT': 2} | ["\"Item Code\"", "mo"] | ["COUNT(*)", "AVG(profit)", "AVG(up)", "AVG(wp / (1.0 - lr / 100.0))", "COUNT(*)", "SUM(CASE WHEN profit < 0 THEN 1 ELSE 0 END)"] | 5 | 226.577 |
| [S76/Q74](#s76) | success | ["product_information"] | 0 / {} | [] | [] | 2 | 0.317 |
| [S77/Q75](#s77) | success | ["product_loss", "purchase_price", "sales_records"] | 3 / {'LEFT': 2} | ["\"Item Code\"", "mo"] | ["COUNT(*)", "AVG(up)", "AVG(wp / (1.0 - lr / 100.0))"] | 5 | 221.416 |
| [S78/Q76](#s78) | success | ["product_information", "product_loss", "purchase_price", "sales_records"] | 4 / {'LEFT': 3} | ["s.\"Item Code\""] | ["COUNT(*)", "SUM(s.\"Sales volume (kg)\")", "AVG(s.\"Unit price (yuan/kg)\")", "AVG(pp.\"Wholesale price (yuan/kg)\")", "AVG(pp.\"Wholesale price (yuan/kg)\")", "COUNT(*)", "SUM(CASE WHEN s.\"Unit price (yuan/kg)\" < pp.\"Wholesale price (yuan/kg)\" / (1.0 - pl.\"Loss Rate (%)\" / 100.0) THEN 1 ELSE 0 END)"] | 2 | 199.617 |


## 元数据和设置

| SQL | 类别 | 状态 | 内容 |
| --- | --- | --- | --- |
| S1 | connection_setup | success | PRAGMA query_only=ON |
| S2 | metadata | success | SELECT name,sql FROM sqlite_master WHERE type='table' ORDER BY name |


## Python 与执行位置

人工源码审查：**reviewed_SQL_dominant_with_plot_preparation**。Core sales/price/loss joins, summer filters, profitability arithmetic and per-item/month aggregation remain in logged SQL, including SQL initiated from Python. P1/P2/P6 mainly retrieve/display results. P3/P5 filter non-null summarized items and sort them for figures, and P7 selects each item series for plotting; these limited SQL-capable presentation preparations are disclosed, without equating this trajectory to full-table pandas aggregation. [证据](../reviews/dacomp-025.json)。

P1：I need to pull the per-item summer loss statistics for all items sold on 2023-06-30 (the procurement basis) into Python to build a summary table and visualization. The SQL-side aggregation is done in the query; Python is used only for the final table formatting and plotting which SQLite cannot reasonably do.

[源码](../../../runs/dsv4flash-db-first-full-01/dacomp-025/attempt-01/python/P1.py)；[输出](../../../runs/dsv4flash-db-first-full-01/dacomp-025/attempt-01/python/P1.stdout)；[错误](../../../runs/dsv4flash-db-first-full-01/dacomp-025/attempt-01/python/P1.stderr)。检出需人工核验的 SQL 可实现操作：.query(；不能仅凭理由判为合规。

P2：Same aggregation as before; printing the full summary table so I can inspect all items sold on 2023-06-30 with their historical loss statistics before building the final visualization.

[源码](../../../runs/dsv4flash-db-first-full-01/dacomp-025/attempt-01/python/P2.py)；[输出](../../../runs/dsv4flash-db-first-full-01/dacomp-025/attempt-01/python/P2.stdout)；[错误](../../../runs/dsv4flash-db-first-full-01/dacomp-025/attempt-01/python/P2.stderr)。检出需人工核验的 SQL 可实现操作：.query(；不能仅凭理由判为合规。

P3：SQLite cannot render charts, so I use Python to produce a bar chart of 2022-summer profitability for all items that would be procured on 2023-07-01, highlighting the clearly loss-making items. The aggregation was already done in SQL.

[源码](../../../runs/dsv4flash-db-first-full-01/dacomp-025/attempt-01/python/P3.py)；[输出](../../../runs/dsv4flash-db-first-full-01/dacomp-025/attempt-01/python/P3.stdout)；[错误](../../../runs/dsv4flash-db-first-full-01/dacomp-025/attempt-01/python/P3.stderr)。检出需人工核验的 SQL 可实现操作：.query(, sort_values(；不能仅凭理由判为合规。

P4：The /work directory for saving figures does not exist yet; creating it so figures can be saved there.

[源码](../../../runs/dsv4flash-db-first-full-01/dacomp-025/attempt-01/python/P4.py)；[输出](../../../runs/dsv4flash-db-first-full-01/dacomp-025/attempt-01/python/P4.stdout)；[错误](../../../runs/dsv4flash-db-first-full-01/dacomp-025/attempt-01/python/P4.stderr)。自动源码筛查未检出预设迁出信号；这不是全面语义合规证明。

P5：Rendering the 2022-summer profitability bar chart for items to be procured on 2023-07-01; the SQL aggregation was done in the query and Python only creates the figure and prints the top rows.

[源码](../../../runs/dsv4flash-db-first-full-01/dacomp-025/attempt-01/python/P5.py)；[输出](../../../runs/dsv4flash-db-first-full-01/dacomp-025/attempt-01/python/P5.stdout)；[错误](../../../runs/dsv4flash-db-first-full-01/dacomp-025/attempt-01/python/P5.stderr)。检出需人工核验的 SQL 可实现操作：.query(, sort_values(；不能仅凭理由判为合规。

P6：Gathering monthly 2022-summer profitability details for the two candidate loss-making items to include in the final report.

[源码](../../../runs/dsv4flash-db-first-full-01/dacomp-025/attempt-01/python/P6.py)；[输出](../../../runs/dsv4flash-db-first-full-01/dacomp-025/attempt-01/python/P6.stdout)；[错误](../../../runs/dsv4flash-db-first-full-01/dacomp-025/attempt-01/python/P6.stderr)。检出需人工核验的 SQL 可实现操作：.query(；不能仅凭理由判为合规。

P7：Rendering the selling-price vs effective-cost comparison figure for the two candidate items, and pulling the 2023-06-30 direct evidence for the report. This is plotting and final summary formatting that SQLite cannot do.

[源码](../../../runs/dsv4flash-db-first-full-01/dacomp-025/attempt-01/python/P7.py)；[输出](../../../runs/dsv4flash-db-first-full-01/dacomp-025/attempt-01/python/P7.stdout)；[错误](../../../runs/dsv4flash-db-first-full-01/dacomp-025/attempt-01/python/P7.stderr)。检出需人工核验的 SQL 可实现操作：.query(, sort_values(；不能仅凭理由判为合规。

## 优化机会

已验证候选。筛选限于精确 SQL、相同自包含 CTE、相同单表完整过滤、可分解单表聚合；未覆盖任意 Join 等价和一般谓词蕴含。全部候选都是 offline，未测在线预测。

| 候选 | 类型 | 已有结果 | 覆盖 SQL | 后续次数 | 中间行数 | 验证 | 成本 |
| --- | --- | --- | --- | --- | --- | --- | --- |
| C1 | exact-result reuse | True | ["S65", "S66"] | 1 | 39 | verified | Not benchmarked; correctness alone does not establish net speedup. |
| C2 | exact-result reuse | True | ["S67", "S68"] | 1 | unknown | not_verified_cap | Not tested |
| C3 | common subexpression | False | ["S38", "S40", "S41", "S42", "S48", "S53", "S54", "S55", "S56", "S57", "S58", "S64"] | 11 | 39 | verification_limited | Not benchmarked; correctness alone does not establish net speedup. |
| C4 | common subexpression | False | ["S65", "S66", "S67", "S68"] | 3 | 39 | verified | Not benchmarked; correctness alone does not establish net speedup. |
| C5 | common subexpression | False | ["S70", "S74"] | 1 | unknown | not_verified_cap | Not tested |
| C6 | common subexpression | False | ["S70", "S74"] | 1 | unknown | not_verified_cap | Not tested |
| C7 | common filtered view | False | ["S27", "S28"] | 1 | unknown | not_verified_cap | Not tested |
| C8 | common filtered view | False | ["S45", "S62"] | 1 | unknown | not_verified_cap | Not tested |


已验证覆盖（含触发查询、候选并集去重）：4/75 条成功数据 SQL。正确性仅针对当前数据库快照；未测性能的候选不能声称已加速。

[完整 build/rewrite 与比较证据](dacomp-025.analysis.json)。

### C4：common subexpression

Identical self-contained CTE body across queries.

原查询 [S65](#s65), [S66](#s66), [S67](#s67), [S68](#s68) → 新增共享状态 C4 → 后续 3 次可复用。该构建点为事后假设，不代表 Agent 当时预知后续。

构建定义：

```sql
SELECT s."Item Code", SUM(s."Sales volume (kg)") AS vol_0630 FROM sales_records AS s WHERE DATE(s."Sales Date") = '2023-06-30' AND s."Sales type" = 'Sale' GROUP BY s."Item Code"
```

受益查询 S65 的改写示例（截取前 1600 字符，完整版本见证据 JSON）：

```sql
WITH proc_items AS (SELECT * FROM temp.reuse_candidate), summer_sales AS (SELECT s."Item Code", s."Sales volume (kg)" AS vol, s."Unit price (yuan/kg)" AS up, pp."Wholesale price (yuan/kg)" AS wp, pl."Loss Rate (%)" AS lr, STRFTIME('%Y', s."Sales Date") AS yr, s."Unit price (yuan/kg)" - pp."Wholesale price (yuan/kg)" / (1.0 - pl."Loss Rate (%)" / 100.0) AS profit FROM sales_records AS s JOIN proc_items AS pi ON s."Item Code" = pi."Item Code" LEFT JOIN purchase_price AS pp ON s."Item Code" = pp."Item Code" AND DATE(s."Sales Date") = DATE(pp."Date") LEFT JOIN product_loss AS pl ON s."Item Code" = pl."Item Code" WHERE s."Sales type" = 'Sale' AND ((s."Sales Date" >= '2020-07-01' AND s."Sales Date" < '2020-09-01') OR (s."Sales Date" >= '2021-06-01' AND s."Sales Date" < '2021-09-01') OR (s."Sales Date" >= '2022-06-01' AND s."Sales Date" < '2022-09-01')) AND NOT pp."Wholesale price (yuan/kg)" IS NULL AND NOT pl."Loss Rate (%)" IS NULL), y2022 AS (SELECT "Item Code", COUNT(*) AS n22, AVG(profit) AS avgp22, SUM(CASE WHEN profit < 0 THEN 1 ELSE 0 END) * 100.0 / COUNT(*) AS pct22, SUM(vol * profit) AS tot22 FROM summer_sales WHERE yr = '2022' GROUP BY "Item Code"), allsum AS (SELECT "Item Code", COUNT(*) AS n_all, AVG(profit) AS avgp_all, SUM(CASE WHEN profit < 0 THEN 1 ELSE 0 END) * 100.0 / COUNT(*) AS pct_all, SUM(vol * profit) AS tot_all FROM summer_sales GROUP BY "Item Code") SELECT pi."Item Code", p."Item Name", ROUND(pi.vol_0630, 2) AS vol_0630, y.n22, ROUND(y.avgp22, 3) AS avgp22, ROUND(y.pct22, 1) AS pct22, ROUND(y.tot22, 2) AS tot22, a.n_all, ROUND(a.avgp_all, 3) AS avgp_all, 
```

| 原 SQL | 列名一致 | 结果一致 | 比较方法 |
| --- | --- | --- | --- |
| S65 | True | True | ordered_numeric_tolerance |
| S66 | True | True | ordered_numeric_tolerance |
| S67 | True | True | ordered_numeric_tolerance |
| S68 | True | True | ordered_numeric_tolerance |


验证状态：verified；成本结论：Not benchmarked; correctness alone does not establish net speedup.

### C1：exact-result reuse

Identical normalized SQL and parameters; archive equality checked.

原查询 [S65](#s65), [S66](#s66) → 保留前序结果 S65 → 后续 1 次可复用。该构建点为事后假设，不代表 Agent 当时预知后续。

| 原 SQL | 列名一致 | 结果一致 | 比较方法 |
| --- | --- | --- | --- |
| S66 | True | True | ordered_numeric_tolerance |


验证状态：verified；成本结论：Not benchmarked; correctness alone does not establish net speedup.

### C3：common subexpression

Identical self-contained CTE body across queries.

原查询 [S38](#s38), [S40](#s40), [S41](#s41), [S42](#s42), [S48](#s48), [S53](#s53), [S54](#s54), [S55](#s55), [S56](#s56), [S57](#s57), [S58](#s58), [S64](#s64) → 新增共享状态 C3 → 后续 11 次可复用。该构建点为事后假设，不代表 Agent 当时预知后续。

构建定义：

```sql
SELECT DISTINCT s."Item Code" FROM sales_records AS s WHERE DATE(s."Sales Date") = '2023-06-30'
```

受益查询 S38 的改写示例：

```sql
WITH proc_items AS (SELECT * FROM temp.reuse_candidate), summer_sales AS (SELECT s."Item Code", s."Unit price (yuan/kg)" AS up, pp."Wholesale price (yuan/kg)" AS wp, pl."Loss Rate (%)" AS lr FROM sales_records AS s JOIN proc_items AS pi ON s."Item Code" = pi."Item Code" LEFT JOIN purchase_price AS pp ON s."Item Code" = pp."Item Code" AND DATE(s."Sales Date") = DATE(pp."Date") LEFT JOIN product_loss AS pl ON s."Item Code" = pl."Item Code" WHERE s."Sales type" = 'Sale' AND ((s."Sales Date" >= '2020-07-01' AND s."Sales Date" < '2020-09-01') OR (s."Sales Date" >= '2021-06-01' AND s."Sales Date" < '2021-09-01') OR (s."Sales Date" >= '2022-06-01' AND s."Sales Date" < '2022-09-01')) AND NOT pp."Wholesale price (yuan/kg)" IS NULL AND NOT pl."Loss Rate (%)" IS NULL) SELECT "Item Code", COUNT(*) AS n_sales, SUM(CASE WHEN up < wp / (1.0 - lr / 100.0) THEN 1 ELSE 0 END) AS n_loss, ROUND(100.0 * SUM(CASE WHEN up < wp / (1.0 - lr / 100.0) THEN 1 ELSE 0 END) / COUNT(*), 1) AS pct_loss, ROUND(AVG(up - wp / (1.0 - lr / 100.0)), 3) AS avg_profit_per_kg FROM summer_sales GROUP BY "Item Code" ORDER BY pct_loss DESC
```

| 原 SQL | 列名一致 | 结果一致 | 比较方法 |
| --- | --- | --- | --- |
| S38 | True | True | ordered_numeric_tolerance |
| S40 | True | True | ordered_numeric_tolerance |
| S41 | True | True | ordered_numeric_tolerance |
| S42 | True | True | ordered_numeric_tolerance |


验证状态：verification_limited；成本结论：Not benchmarked; correctness alone does not establish net speedup.

[性能证据 C4](dacomp-025.C4.performance.json)：limited_or_failed。

结果依赖：自动记录 SQL→Python 的接口父调用，以及源码中引用归档文件的消费者；字面值相同不认定因果。模型方向选择需要人工读取消息，尚未做全面因果标注。

[原始报告](../../../runs/dsv4flash-db-first-full-01/dacomp-025/attempt-01/answer.md)；[统一消息](../../../runs/dsv4flash-db-first-full-01/dacomp-025/attempt-01/messages.jsonl)；[原始 OpenCode 事件](../../../runs/dsv4flash-db-first-full-01/dacomp-025/attempt-01/opencode.jsonl)；[SQL 引擎日志](../../../runs/dsv4flash-db-first-full-01/dacomp-025/attempt-01/sql_journal.jsonl)。

[可读报告（本地图片链接规范化）](../answers/dacomp-025.md)。原始回答保留，分析结论未改写。

## S1

类别 `connection_setup`；来源 `connection`；调用 `8f9c0fdf16b347f0a0ed41ee4bc58211`；状态 `success`。

```sql
PRAGMA query_only=ON
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-025/attempt-01/sql/S1.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-025/attempt-01/sql/S1.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-025/attempt-01/results/S1.rows.jsonl)；完整：True；SHA256：`e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`。

## S2

类别 `metadata`；来源 `list_db`；调用 `8f9c0fdf16b347f0a0ed41ee4bc58211`；状态 `success`。

```sql
SELECT name,sql FROM sqlite_master WHERE type='table' ORDER BY name
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-025/attempt-01/sql/S2.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-025/attempt-01/sql/S2.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-025/attempt-01/results/S2.rows.jsonl)；完整：True；SHA256：`fd15eee55130eb0b938130640985bd6d43ca5f5068dd98609bd01c5309634194`。

## S3

类别 `data`；来源 `query_db`；调用 `aee78e9c7ea44a3a8bf6ab8094e1bbb1`；状态 `success`。

```sql
SELECT * FROM product_information LIMIT 5
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-025/attempt-01/sql/S3.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-025/attempt-01/sql/S3.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-025/attempt-01/results/S3.rows.jsonl)；完整：True；SHA256：`88fa23932db53677f583122c71aca7cec55b991cd950ce9001d4bcdebe7673e3`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "product_information", "kind": "base", "block": null, "base_tables": ["product_information"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |


## S4

类别 `data`；来源 `query_db`；调用 `4a58ee3e2278409ba28adbd8c8e48acb`；状态 `success`。

```sql
SELECT * FROM product_loss LIMIT 5
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-025/attempt-01/sql/S4.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-025/attempt-01/sql/S4.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-025/attempt-01/results/S4.rows.jsonl)；完整：True；SHA256：`ba957684e5757d78e597d829f17c6fbbd5e8a0a6567e96e9b562244100b3aa64`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "product_loss", "kind": "base", "block": null, "base_tables": ["product_loss"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |


## S5

类别 `data`；来源 `query_db`；调用 `2a3166e7627f418d9cbb43cc667bc753`；状态 `success`。

```sql
SELECT * FROM purchase_price LIMIT 5
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-025/attempt-01/sql/S5.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-025/attempt-01/sql/S5.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-025/attempt-01/results/S5.rows.jsonl)；完整：True；SHA256：`b1682198de7829ee1ac8b3cc8076e404b5185ec7294257b8a3c2fba730bc75d2`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "purchase_price", "kind": "base", "block": null, "base_tables": ["purchase_price"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |


## S6

类别 `data`；来源 `query_db`；调用 `f624d895719e46f4acf5adc44ee919ff`；状态 `success`。

```sql
SELECT * FROM sales_records LIMIT 5
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-025/attempt-01/sql/S6.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-025/attempt-01/sql/S6.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-025/attempt-01/results/S6.rows.jsonl)；完整：True；SHA256：`29c66fa72e8c5aed1a58d2f64cf38e2f2e5be680a95b41224bb5060737c7b997`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "sales_records", "kind": "base", "block": null, "base_tables": ["sales_records"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |


## S7

类别 `data`；来源 `query_db`；调用 `f2c78421cde840f69ce2d75bf88b0fc2`；状态 `success`。

```sql
SELECT DISTINCT strftime('%Y', "Sales Date") as year FROM sales_records ORDER BY year
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-025/attempt-01/sql/S7.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-025/attempt-01/sql/S7.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-025/attempt-01/results/S7.rows.jsonl)；完整：True；SHA256：`7725b98f620f1affda8ffc134f1a535f4101d457592d8b3b62e3afe7f88e6bea`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "sales_records", "kind": "base", "block": null, "base_tables": ["sales_records"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |


## S8

类别 `data`；来源 `query_db`；调用 `f7b773c7c8b240e9961c93d30d7e1fd0`；状态 `success`。

```sql
SELECT DISTINCT strftime('%Y', "Date") as year FROM purchase_price ORDER BY year
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-025/attempt-01/sql/S8.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-025/attempt-01/sql/S8.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-025/attempt-01/results/S8.rows.jsonl)；完整：True；SHA256：`7725b98f620f1affda8ffc134f1a535f4101d457592d8b3b62e3afe7f88e6bea`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "purchase_price", "kind": "base", "block": null, "base_tables": ["purchase_price"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |


## S9

类别 `data`；来源 `query_db`；调用 `ceef9c3272644ccabc6db559c1954b57`；状态 `success`。

```sql
SELECT DISTINCT strftime('%Y-%m', "Sales Date") as ym FROM sales_records ORDER BY ym
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-025/attempt-01/sql/S9.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-025/attempt-01/sql/S9.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-025/attempt-01/results/S9.rows.jsonl)；完整：True；SHA256：`d6fc71a690285c3352cf9d1a2dc3d99e7503f88750ceee8e2b9c9605c278038b`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "sales_records", "kind": "base", "block": null, "base_tables": ["sales_records"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |


## S10

类别 `data`；来源 `query_db`；调用 `9662176085d34a85ad7ae437f193cc1a`；状态 `success`。

```sql
SELECT DISTINCT strftime('%Y-%m', "Date") as ym FROM purchase_price ORDER BY ym
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-025/attempt-01/sql/S10.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-025/attempt-01/sql/S10.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-025/attempt-01/results/S10.rows.jsonl)；完整：True；SHA256：`d6fc71a690285c3352cf9d1a2dc3d99e7503f88750ceee8e2b9c9605c278038b`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "purchase_price", "kind": "base", "block": null, "base_tables": ["purchase_price"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |


## S11

类别 `data`；来源 `query_db`；调用 `5a8d99e424be41ee89f03f2ac6b6222f`；状态 `success`。

```sql
SELECT DISTINCT "Sales type" FROM sales_records
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-025/attempt-01/sql/S11.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-025/attempt-01/sql/S11.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-025/attempt-01/results/S11.rows.jsonl)；完整：True；SHA256：`4ec96fbbb48be74d8ed0f64e5df1cde93efbf2fc3732e85bf402f1881fec098f`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "sales_records", "kind": "base", "block": null, "base_tables": ["sales_records"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |


## S12

类别 `data`；来源 `query_db`；调用 `3680902cdd8f46dabc71743cd3776b1f`；状态 `success`。

```sql
SELECT DISTINCT "Whether sold at a discount" FROM sales_records
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-025/attempt-01/sql/S12.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-025/attempt-01/sql/S12.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-025/attempt-01/results/S12.rows.jsonl)；完整：True；SHA256：`5a19713cda3bf0943666a353b839ac204635994c6093a1b7bb22ac4ab428ba10`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "sales_records", "kind": "base", "block": null, "base_tables": ["sales_records"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |


## S13

类别 `data`；来源 `query_db`；调用 `28369a127eb64d6b9df8eb665b237bd7`；状态 `success`。

```sql
SELECT COUNT(DISTINCT "Item Code") FROM sales_records
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-025/attempt-01/sql/S13.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-025/attempt-01/sql/S13.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-025/attempt-01/results/S13.rows.jsonl)；完整：True；SHA256：`4d685a258045dceeaab04627f4dd7a565cb0e69d37ff111a46c45365f91b4ffc`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "sales_records", "kind": "base", "block": null, "base_tables": ["sales_records"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(DISTINCT "Item Code") | [{"table": "sales_records", "column": "Item Code"}] | [] | False |


## S14

类别 `data`；来源 `query_db`；调用 `045631804a4e47b084debafebf92660e`；状态 `success`。

```sql
SELECT COUNT(DISTINCT "Item Code") FROM purchase_price
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-025/attempt-01/sql/S14.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-025/attempt-01/sql/S14.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-025/attempt-01/results/S14.rows.jsonl)；完整：True；SHA256：`5c13566db40e1ceee2b2cd93d5040be37aaf3e371936c79d2efe79f9024d1545`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "purchase_price", "kind": "base", "block": null, "base_tables": ["purchase_price"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(DISTINCT "Item Code") | [{"table": "purchase_price", "column": "Item Code"}] | [] | False |


## S15

类别 `data`；来源 `query_db`；调用 `d8fea486ad0c40eeaf366f61b8240b3a`；状态 `success`。

```sql
SELECT COUNT(DISTINCT "Item Code") FROM product_information
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-025/attempt-01/sql/S15.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-025/attempt-01/sql/S15.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-025/attempt-01/results/S15.rows.jsonl)；完整：True；SHA256：`5c13566db40e1ceee2b2cd93d5040be37aaf3e371936c79d2efe79f9024d1545`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "product_information", "kind": "base", "block": null, "base_tables": ["product_information"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(DISTINCT "Item Code") | [{"table": "product_information", "column": "Item Code"}] | [] | False |


## S16

类别 `data`；来源 `query_db`；调用 `dde5e6ce2fae41b8a4294b644d0c0655`；状态 `success`。

```sql
SELECT COUNT(DISTINCT "Item Code") FROM product_loss
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-025/attempt-01/sql/S16.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-025/attempt-01/sql/S16.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-025/attempt-01/results/S16.rows.jsonl)；完整：True；SHA256：`5c13566db40e1ceee2b2cd93d5040be37aaf3e371936c79d2efe79f9024d1545`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "product_loss", "kind": "base", "block": null, "base_tables": ["product_loss"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(DISTINCT "Item Code") | [{"table": "product_loss", "column": "Item Code"}] | [] | False |


## S17

类别 `data`；来源 `query_db`；调用 `915138db1b464f5bb5b0a05043147179`；状态 `success`。

```sql
SELECT * FROM sales_records WHERE "Sales Date" >= '2023-06-30' AND "Sales Date" < '2023-07-01' LIMIT 10
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-025/attempt-01/sql/S17.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-025/attempt-01/sql/S17.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-025/attempt-01/results/S17.rows.jsonl)；完整：True；SHA256：`9eaff72c7a76001e5c0dab41645781cfa911bd04e6e35c49f48fc1126919c81f`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "sales_records", "kind": "base", "block": null, "base_tables": ["sales_records"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |


## S18

类别 `data`；来源 `query_db`；调用 `4c00e5435f974f8782778a2602c33eb2`；状态 `success`。

```sql
SELECT * FROM purchase_price WHERE "Date" >= '2023-07-01' AND "Date" < '2023-07-02' LIMIT 10
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-025/attempt-01/sql/S18.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-025/attempt-01/sql/S18.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-025/attempt-01/results/S18.rows.jsonl)；完整：True；SHA256：`e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "purchase_price", "kind": "base", "block": null, "base_tables": ["purchase_price"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |


## S19

类别 `data`；来源 `query_db`；调用 `5e61ea6f4c4c4b71a1202b62d19c4e98`；状态 `success`。

```sql
SELECT "Item Code", "Item Name", "Loss Rate (%)" FROM product_loss ORDER BY "Loss Rate (%)" DESC LIMIT 10
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-025/attempt-01/sql/S19.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-025/attempt-01/sql/S19.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-025/attempt-01/results/S19.rows.jsonl)；完整：True；SHA256：`6051c29fc185403d5c7142d97e364b330cbea0375e4d1ad8e707219a11dab1a7`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "product_loss", "kind": "base", "block": null, "base_tables": ["product_loss"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |


## S20

类别 `data`；来源 `query_db`；调用 `3d78c5731e6b41079b222823fcffccae`；状态 `success`。

```sql
SELECT "Date", COUNT(*) as cnt FROM purchase_price WHERE "Date" LIKE '2023-%' GROUP BY "Date" ORDER BY "Date"
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-025/attempt-01/sql/S20.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-025/attempt-01/sql/S20.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-025/attempt-01/results/S20.rows.jsonl)；完整：True；SHA256：`05db9166549d72bb172fe2731e267bfec66b03fda0844d1c8e337d131c7c1995`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "purchase_price", "kind": "base", "block": null, "base_tables": ["purchase_price"]}] | [] | ["\"Date\""] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |


## S21

类别 `data`；来源 `query_db`；调用 `05f9126dd33c45aea53076f448e65b96`；状态 `success`。

```sql
SELECT "Sales Date", COUNT(*) as cnt FROM sales_records WHERE "Sales Date" LIKE '2023-%' GROUP BY "Sales Date" ORDER BY "Sales Date"
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-025/attempt-01/sql/S21.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-025/attempt-01/sql/S21.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-025/attempt-01/results/S21.rows.jsonl)；完整：True；SHA256：`dbc44802f9df5a7623897c8172084f43c8a95596f31e95c2dc4cd090f7c4dfe6`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "sales_records", "kind": "base", "block": null, "base_tables": ["sales_records"]}] | [] | ["\"Sales Date\""] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |


## S22

类别 `data`；来源 `query_db`；调用 `eaef0a56bf9648e7ba1babab50d67288`；状态 `success`。

```sql
SELECT "Date" FROM purchase_price WHERE "Date" >= '2023-06-01' AND "Date" < '2023-08-01' GROUP BY "Date" ORDER BY "Date"
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-025/attempt-01/sql/S22.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-025/attempt-01/sql/S22.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-025/attempt-01/results/S22.rows.jsonl)；完整：True；SHA256：`a1f7df73e854c3264a395973d674728ff9adc4cba311f4ea5b9aee85bbbf3131`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "purchase_price", "kind": "base", "block": null, "base_tables": ["purchase_price"]}] | [] | ["\"Date\""] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |


## S23

类别 `data`；来源 `query_db`；调用 `68a4de8a2fcf4b309d0c7f27c1b822c5`；状态 `success`。

```sql
SELECT "Sales Date" FROM sales_records WHERE "Sales Date" >= '2023-06-01' AND "Sales Date" < '2023-08-01' GROUP BY "Sales Date" ORDER BY "Sales Date"
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-025/attempt-01/sql/S23.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-025/attempt-01/sql/S23.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-025/attempt-01/results/S23.rows.jsonl)；完整：True；SHA256：`a1f7df73e854c3264a395973d674728ff9adc4cba311f4ea5b9aee85bbbf3131`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "sales_records", "kind": "base", "block": null, "base_tables": ["sales_records"]}] | [] | ["\"Sales Date\""] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |


## S24

类别 `data`；来源 `query_db`；调用 `e768b48a419647d4b393056e2969eaea`；状态 `success`。

```sql
SELECT * FROM purchase_price WHERE "Item Code" = 102900005115823 AND "Date" >= '2023-06-25' AND "Date" < '2023-07-02'
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-025/attempt-01/sql/S24.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-025/attempt-01/sql/S24.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-025/attempt-01/results/S24.rows.jsonl)；完整：True；SHA256：`a4de4b9e57187a98c7a3479b5bdd28f6d539f8644cfc8ff10699bdfabf4ea353`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "purchase_price", "kind": "base", "block": null, "base_tables": ["purchase_price"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |


## S25

类别 `data`；来源 `query_db`；调用 `6e91d940f225480491b74d93f0e2bf2c`；状态 `success`。

```sql
SELECT * FROM product_loss WHERE "Item Code" = 102900005115823
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-025/attempt-01/sql/S25.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-025/attempt-01/sql/S25.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-025/attempt-01/results/S25.rows.jsonl)；完整：True；SHA256：`6e1a2b607b1046d61f4c47e1c1c255c5289749aa07a1ed5a78827ad8207df6c3`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "product_loss", "kind": "base", "block": null, "base_tables": ["product_loss"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |


## S26

类别 `data`；来源 `query_db`；调用 `a4063b09515346c195a76e429b85e95f`；状态 `success`。

```sql
SELECT "Sales Date", AVG("Unit price (yuan/kg)") as avg_price, SUM("Sales volume (kg)") as vol, COUNT(*) as cnt FROM sales_records WHERE "Item Code" = 102900005115823 AND "Sales Date" >= '2022-06-01' AND "Sales Date" < '2022-09-01' GROUP BY "Sales Date" ORDER BY "Sales Date"
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-025/attempt-01/sql/S26.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-025/attempt-01/sql/S26.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-025/attempt-01/results/S26.rows.jsonl)；完整：True；SHA256：`e17c3ba2ea1ea223be3d9e29e46c2aeb16aa8e5c3b280e6feb57a2b799f79919`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "sales_records", "kind": "base", "block": null, "base_tables": ["sales_records"]}] | [] | ["\"Sales Date\""] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | AVG("Unit price (yuan/kg)") | [{"table": "sales_records", "column": "Unit price (yuan/kg)"}] | [] | False |
| B1 | SUM("Sales volume (kg)") | [{"table": "sales_records", "column": "Sales volume (kg)"}] | [] | False |
| B1 | COUNT(*) | [] | [] | True |


## S27

类别 `data`；来源 `query_db`；调用 `e10aa9e8ae204aec8d01b3414630759e`；状态 `success`。

```sql
SELECT * FROM purchase_price WHERE "Item Code" = 102900005115823 AND "Date" >= '2022-06-01' AND "Date" < '2022-09-01' ORDER BY "Date" LIMIT 10
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-025/attempt-01/sql/S27.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-025/attempt-01/sql/S27.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-025/attempt-01/results/S27.rows.jsonl)；完整：True；SHA256：`9cf7bdfc9db5617199cbc5b4ea52cb82749ae34c800882958a32ee7a0751cbbe`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "purchase_price", "kind": "base", "block": null, "base_tables": ["purchase_price"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |


## S28

类别 `data`；来源 `query_db`；调用 `37af00dc5cce476988c6ec6acd7666d2`；状态 `success`。

```sql
SELECT "Date", AVG("Wholesale price (yuan/kg)") as avg_wholesale FROM purchase_price WHERE "Item Code" = 102900005115823 AND "Date" >= '2022-06-01' AND "Date" < '2022-09-01' GROUP BY "Date" ORDER BY "Date"
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-025/attempt-01/sql/S28.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-025/attempt-01/sql/S28.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-025/attempt-01/results/S28.rows.jsonl)；完整：True；SHA256：`26c470cf7fa6ee51d985234225f6838b972b5d6121c5b0b8b1c9b0d1d8870af8`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "purchase_price", "kind": "base", "block": null, "base_tables": ["purchase_price"]}] | [] | ["\"Date\""] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | AVG("Wholesale price (yuan/kg)") | [{"table": "purchase_price", "column": "Wholesale price (yuan/kg)"}] | [] | False |


## S29

类别 `data`；来源 `query_db`；调用 `5ce80ba838fa4533a061b08ccf1054eb`；状态 `success`。

```sql
SELECT DISTINCT s."Item Code", p."Item Name", SUM(s."Sales volume (kg)") as total_vol
FROM sales_records s
LEFT JOIN product_information p ON s."Item Code" = p."Item Code"
WHERE s."Sales Date" = '2023-06-30'
GROUP BY s."Item Code"
ORDER BY total_vol DESC
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-025/attempt-01/sql/S29.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-025/attempt-01/sql/S29.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-025/attempt-01/results/S29.rows.jsonl)；完整：True；SHA256：`e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "s", "kind": "base", "block": null, "base_tables": ["sales_records"]}, {"alias": "p", "kind": "base", "block": null, "base_tables": ["product_information"]}] | [{"type": "LEFT", "right": "product_information AS p", "on": "s.\"Item Code\" = p.\"Item Code\"", "using": []}] | ["s.\"Item Code\""] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | SUM(s."Sales volume (kg)") | [{"table": "sales_records", "column": "Sales volume (kg)"}] | [] | False |


## S30

类别 `data`；来源 `query_db`；调用 `bd6a10ef40f24950aea2773af81d721f`；状态 `success`。

```sql
SELECT DISTINCT "Sales Date" FROM sales_records WHERE "Sales Date" LIKE '2023-06-30%' OR "Sales Date" LIKE '2023-06-30%' OR "Sales Date" >= '2023-06-29'
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-025/attempt-01/sql/S30.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-025/attempt-01/sql/S30.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-025/attempt-01/results/S30.rows.jsonl)；完整：True；SHA256：`61cc5dc21e8aebe9136f710e3b4b36a9fa67b34159759ba97a50166543da4f34`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "sales_records", "kind": "base", "block": null, "base_tables": ["sales_records"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |


## S31

类别 `data`；来源 `query_db`；调用 `655f85d8f5d645b69259bfadb2f8e861`；状态 `success`。

```sql
SELECT DISTINCT "Sales Date" FROM sales_records ORDER BY "Sales Date" DESC LIMIT 5
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-025/attempt-01/sql/S31.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-025/attempt-01/sql/S31.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-025/attempt-01/results/S31.rows.jsonl)；完整：True；SHA256：`d5304c84d11d11118014fc13f6533d241fc926dedc5e2cc9b257ef0f38ad95ec`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "sales_records", "kind": "base", "block": null, "base_tables": ["sales_records"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |


## S32

类别 `data`；来源 `query_db`；调用 `630066aa22e84e049229cdbfe9fea490`；状态 `success`。

```sql
SELECT DISTINCT s."Item Code", p."Item Name", SUM(s."Sales volume (kg)") as total_vol
FROM sales_records s
LEFT JOIN product_information p ON s."Item Code" = p."Item Code"
WHERE date(s."Sales Date") = '2023-06-30'
GROUP BY s."Item Code"
ORDER BY total_vol DESC
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-025/attempt-01/sql/S32.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-025/attempt-01/sql/S32.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-025/attempt-01/results/S32.rows.jsonl)；完整：True；SHA256：`a0a81ef480f8b7fd3cbd2a9ace9f7c8152d033760d78b63a37d1bbdb5626d81f`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "s", "kind": "base", "block": null, "base_tables": ["sales_records"]}, {"alias": "p", "kind": "base", "block": null, "base_tables": ["product_information"]}] | [{"type": "LEFT", "right": "product_information AS p", "on": "s.\"Item Code\" = p.\"Item Code\"", "using": []}] | ["s.\"Item Code\""] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | SUM(s."Sales volume (kg)") | [{"table": "sales_records", "column": "Sales volume (kg)"}] | [] | False |


## S33

类别 `data`；来源 `query_db`；调用 `7380b5bf1b5749a188a9d40f49fca628`；状态 `success`。

```sql
SELECT DISTINCT strftime('%Y-%m', "Sales Date") as ym FROM sales_records WHERE "Sales Date" >= '2020-06-01' AND "Sales Date" < '2020-09-01' ORDER BY ym
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-025/attempt-01/sql/S33.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-025/attempt-01/sql/S33.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-025/attempt-01/results/S33.rows.jsonl)；完整：True；SHA256：`493cb8cb9765c89b2899dad9c007db27f74cfcd0d85a93c42a01ca54f0a51a64`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "sales_records", "kind": "base", "block": null, "base_tables": ["sales_records"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |


## S34

类别 `data`；来源 `query_db`；调用 `dd85a75569ca46d4a55d9534712105c3`；状态 `success`。

```sql
SELECT COUNT(*) as cnt FROM sales_records s LEFT JOIN purchase_price pp ON s."Item Code" = pp."Item Code" AND date(s."Sales Date") = date(pp."Date") WHERE s."Sales Date" >= '2020-06-01' AND s."Sales Date" < '2023-06-30' AND date(s."Sales Date") >= '2020-06-01'
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-025/attempt-01/sql/S34.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-025/attempt-01/sql/S34.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-025/attempt-01/results/S34.rows.jsonl)；完整：True；SHA256：`69103e9ceab150a5e2ec054a636561b070aaf2741682f1ea5ef3a7cbbd4dbf77`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "s", "kind": "base", "block": null, "base_tables": ["sales_records"]}, {"alias": "pp", "kind": "base", "block": null, "base_tables": ["purchase_price"]}] | [{"type": "LEFT", "right": "purchase_price AS pp", "on": "s.\"Item Code\" = pp.\"Item Code\" AND DATE(s.\"Sales Date\") = DATE(pp.\"Date\")", "using": []}] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |


## S35

类别 `data`；来源 `query_db`；调用 `b99d5971eb7d490cb7fca5857ad10db2`；状态 `success`。

```sql
SELECT COUNT(*) as cnt
FROM sales_records s
LEFT JOIN purchase_price pp ON s."Item Code" = pp."Item Code" AND date(s."Sales Date") = date(pp."Date")
LEFT JOIN product_loss pl ON s."Item Code" = pl."Item Code"
WHERE s."Sales Date" >= '2020-07-01' AND s."Sales Date" < '2020-09-01'
AND s."Sales type" = 'Sale'
AND pp."Wholesale price (yuan/kg)" IS NOT NULL
AND pl."Loss Rate (%)" IS NOT NULL
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-025/attempt-01/sql/S35.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-025/attempt-01/sql/S35.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-025/attempt-01/results/S35.rows.jsonl)；完整：True；SHA256：`c35f34a112979cd1ce38a8717f584c2eb63d18a9c2a40eae5147cc07eef97c8d`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "s", "kind": "base", "block": null, "base_tables": ["sales_records"]}, {"alias": "pp", "kind": "base", "block": null, "base_tables": ["purchase_price"]}, {"alias": "pl", "kind": "base", "block": null, "base_tables": ["product_loss"]}] | [{"type": "LEFT", "right": "purchase_price AS pp", "on": "s.\"Item Code\" = pp.\"Item Code\" AND DATE(s.\"Sales Date\") = DATE(pp.\"Date\")", "using": []}, {"type": "LEFT", "right": "product_loss AS pl", "on": "s.\"Item Code\" = pl.\"Item Code\"", "using": []}] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |


## S36

类别 `data`；来源 `query_db`；调用 `737cb3c332b74d03bd1befa3f3c030c2`；状态 `success`。

```sql
SELECT COUNT(*) as cnt
FROM sales_records s
LEFT JOIN purchase_price pp ON s."Item Code" = pp."Item Code" AND date(s."Sales Date") = date(pp."Date")
LEFT JOIN product_loss pl ON s."Item Code" = pl."Item Code"
WHERE s."Sales Date" >= '2021-06-01' AND s."Sales Date" < '2021-09-01'
AND s."Sales type" = 'Sale'
AND pp."Wholesale price (yuan/kg)" IS NOT NULL
AND pl."Loss Rate (%)" IS NOT NULL
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-025/attempt-01/sql/S36.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-025/attempt-01/sql/S36.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-025/attempt-01/results/S36.rows.jsonl)；完整：True；SHA256：`e4f35bcaae373737c74e351cc1183eb4b05e8cac1e5e0b8007029c596bf18a2b`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "s", "kind": "base", "block": null, "base_tables": ["sales_records"]}, {"alias": "pp", "kind": "base", "block": null, "base_tables": ["purchase_price"]}, {"alias": "pl", "kind": "base", "block": null, "base_tables": ["product_loss"]}] | [{"type": "LEFT", "right": "purchase_price AS pp", "on": "s.\"Item Code\" = pp.\"Item Code\" AND DATE(s.\"Sales Date\") = DATE(pp.\"Date\")", "using": []}, {"type": "LEFT", "right": "product_loss AS pl", "on": "s.\"Item Code\" = pl.\"Item Code\"", "using": []}] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |


## S37

类别 `data`；来源 `query_db`；调用 `873d77869637476eb63c413f600aca47`；状态 `success`。

```sql
SELECT COUNT(*) as cnt
FROM sales_records s
LEFT JOIN purchase_price pp ON s."Item Code" = pp."Item Code" AND date(s."Sales Date") = date(pp."Date")
LEFT JOIN product_loss pl ON s."Item Code" = pl."Item Code"
WHERE s."Sales Date" >= '2022-06-01' AND s."Sales Date" < '2022-09-01'
AND s."Sales type" = 'Sale'
AND pp."Wholesale price (yuan/kg)" IS NOT NULL
AND pl."Loss Rate (%)" IS NOT NULL
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-025/attempt-01/sql/S37.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-025/attempt-01/sql/S37.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-025/attempt-01/results/S37.rows.jsonl)；完整：True；SHA256：`4d07c03a08dc0f07c749c69c5005688583d36d7f55d5643246a0ec40c9074a00`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "s", "kind": "base", "block": null, "base_tables": ["sales_records"]}, {"alias": "pp", "kind": "base", "block": null, "base_tables": ["purchase_price"]}, {"alias": "pl", "kind": "base", "block": null, "base_tables": ["product_loss"]}] | [{"type": "LEFT", "right": "purchase_price AS pp", "on": "s.\"Item Code\" = pp.\"Item Code\" AND DATE(s.\"Sales Date\") = DATE(pp.\"Date\")", "using": []}, {"type": "LEFT", "right": "product_loss AS pl", "on": "s.\"Item Code\" = pl.\"Item Code\"", "using": []}] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |


## S38

类别 `data`；来源 `query_db`；调用 `c379c95564eb4252b17c6bf74614e15d`；状态 `success`。

```sql
WITH proc_items AS (
  SELECT DISTINCT s."Item Code"
  FROM sales_records s
  WHERE date(s."Sales Date") = '2023-06-30'
),
summer_sales AS (
  SELECT s."Item Code", s."Unit price (yuan/kg)" as up, pp."Wholesale price (yuan/kg)" as wp, pl."Loss Rate (%)" as lr
  FROM sales_records s
  JOIN proc_items pi ON s."Item Code" = pi."Item Code"
  LEFT JOIN purchase_price pp ON s."Item Code" = pp."Item Code" AND date(s."Sales Date") = date(pp."Date")
  LEFT JOIN product_loss pl ON s."Item Code" = pl."Item Code"
  WHERE s."Sales type" = 'Sale'
    AND (
      (s."Sales Date" >= '2020-07-01' AND s."Sales Date" < '2020-09-01')
      OR (s."Sales Date" >= '2021-06-01' AND s."Sales Date" < '2021-09-01')
      OR (s."Sales Date" >= '2022-06-01' AND s."Sales Date" < '2022-09-01')
    )
    AND pp."Wholesale price (yuan/kg)" IS NOT NULL
    AND pl."Loss Rate (%)" IS NOT NULL
)
SELECT "Item Code",
  COUNT(*) as n_sales,
  SUM(CASE WHEN up < wp/(1.0-lr/100.0) THEN 1 ELSE 0 END) as n_loss,
  ROUND(100.0*SUM(CASE WHEN up < wp/(1.0-lr/100.0) THEN 1 ELSE 0 END)/COUNT(*),1) as pct_loss,
  ROUND(AVG(up - wp/(1.0-lr/100.0)),3) as avg_profit_per_kg
FROM summer_sales
GROUP BY "Item Code"
ORDER BY pct_loss DESC
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-025/attempt-01/sql/S38.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-025/attempt-01/sql/S38.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-025/attempt-01/results/S38.rows.jsonl)；完整：True；SHA256：`f7e0990eb74a86e8ab811589d562818ca5a93c0c2b4312d68670c3cef8936175`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "s", "kind": "base", "block": null, "base_tables": ["sales_records"]}] | [] | [] |
| B2 | [{"alias": "s", "kind": "base", "block": null, "base_tables": ["sales_records"]}, {"alias": "pi", "kind": "derived", "block": "B1", "base_tables": ["sales_records"]}, {"alias": "pp", "kind": "base", "block": null, "base_tables": ["purchase_price"]}, {"alias": "pl", "kind": "base", "block": null, "base_tables": ["product_loss"]}] | [{"type": "INNER", "right": "proc_items AS pi", "on": "s.\"Item Code\" = pi.\"Item Code\"", "using": []}, {"type": "LEFT", "right": "purchase_price AS pp", "on": "s.\"Item Code\" = pp.\"Item Code\" AND DATE(s.\"Sales Date\") = DATE(pp.\"Date\")", "using": []}, {"type": "LEFT", "right": "product_loss AS pl", "on": "s.\"Item Code\" = pl.\"Item Code\"", "using": []}] | [] |
| B3 | [{"alias": "summer_sales", "kind": "derived", "block": "B2", "base_tables": ["product_loss", "purchase_price", "sales_records"]}] | [] | ["\"Item Code\""] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B3 | COUNT(*) | [] | [] | True |
| B3 | SUM(CASE WHEN up < wp / (1.0 - lr / 100.0) THEN 1 ELSE 0 END) | [] | [{"table": "sales_records", "column": "Unit price (yuan/kg)"}, {"table": "purchase_price", "column": "Wholesale price (yuan/kg)"}, {"table": "product_loss", "column": "Loss Rate (%)"}] | False |
| B3 | AVG(up - wp / (1.0 - lr / 100.0)) | [{"table": "sales_records", "column": "Unit price (yuan/kg)"}, {"table": "purchase_price", "column": "Wholesale price (yuan/kg)"}, {"table": "product_loss", "column": "Loss Rate (%)"}] | [] | False |
| B3 | COUNT(*) | [] | [] | True |
| B3 | SUM(CASE WHEN up < wp / (1.0 - lr / 100.0) THEN 1 ELSE 0 END) | [] | [{"table": "sales_records", "column": "Unit price (yuan/kg)"}, {"table": "purchase_price", "column": "Wholesale price (yuan/kg)"}, {"table": "product_loss", "column": "Loss Rate (%)"}] | False |


## S39

类别 `data`；来源 `query_db`；调用 `3a8df94b3b3e44fdbe018e3f613587c3`；状态 `success`。

```sql
WITH proc_items AS (
  SELECT DISTINCT s."Item Code", p."Item Name"
  FROM sales_records s
  LEFT JOIN product_information p ON s."Item Code" = p."Item Code"
  WHERE date(s."Sales Date") = '2023-06-30'
)
SELECT pi."Item Code", pi."Item Name" FROM proc_items pi
ORDER BY pi."Item Code"
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-025/attempt-01/sql/S39.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-025/attempt-01/sql/S39.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-025/attempt-01/results/S39.rows.jsonl)；完整：True；SHA256：`a6bfbdead73364636129753f830d568e7033f3120d663a2fd4a58c87f2c047a1`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "s", "kind": "base", "block": null, "base_tables": ["sales_records"]}, {"alias": "p", "kind": "base", "block": null, "base_tables": ["product_information"]}] | [{"type": "LEFT", "right": "product_information AS p", "on": "s.\"Item Code\" = p.\"Item Code\"", "using": []}] | [] |
| B2 | [{"alias": "pi", "kind": "derived", "block": "B1", "base_tables": ["product_information", "sales_records"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |


## S40

类别 `data`；来源 `query_db`；调用 `312fbe179c924373802c34517d280dc6`；状态 `success`。

```sql
WITH proc_items AS (
  SELECT DISTINCT s."Item Code"
  FROM sales_records s
  WHERE date(s."Sales Date") = '2023-06-30'
),
summer_sales AS (
  SELECT s."Item Code", s."Unit price (yuan/kg)" as up, pp."Wholesale price (yuan/kg)" as wp, pl."Loss Rate (%)" as lr
  FROM sales_records s
  JOIN proc_items pi ON s."Item Code" = pi."Item Code"
  LEFT JOIN purchase_price pp ON s."Item Code" = pp."Item Code" AND date(s."Sales Date") = date(pp."Date")
  LEFT JOIN product_loss pl ON s."Item Code" = pl."Item Code"
  WHERE s."Sales type" = 'Sale'
    AND (
      (s."Sales Date" >= '2020-07-01' AND s."Sales Date" < '2020-09-01')
      OR (s."Sales Date" >= '2021-06-01' AND s."Sales Date" < '2021-09-01')
      OR (s."Sales Date" >= '2022-06-01' AND s."Sales Date" < '2022-09-01')
    )
    AND pp."Wholesale price (yuan/kg)" IS NOT NULL
    AND pl."Loss Rate (%)" IS NOT NULL
)
SELECT "Item Code",
  COUNT(*) as n_sales,
  SUM(CASE WHEN up < wp/(1.0-lr/100.0) THEN 1 ELSE 0 END) as n_loss,
  ROUND(100.0*SUM(CASE WHEN up < wp/(1.0-lr/100.0) THEN 1 ELSE 0 END)/COUNT(*),1) as pct_loss,
  ROUND(AVG(up - wp/(1.0-lr/100.0)),3) as avg_profit_per_kg,
  ROUND(MIN(up - wp/(1.0-lr/100.0)),3) as min_profit
FROM summer_sales
GROUP BY "Item Code"
ORDER BY pct_loss DESC, n_sales DESC
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-025/attempt-01/sql/S40.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-025/attempt-01/sql/S40.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-025/attempt-01/results/S40.rows.jsonl)；完整：True；SHA256：`c6b4fc1b02ce5d1d3a421eb2ff07b8ab0c4311185c995efb829e77b2286a23f7`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "s", "kind": "base", "block": null, "base_tables": ["sales_records"]}] | [] | [] |
| B2 | [{"alias": "s", "kind": "base", "block": null, "base_tables": ["sales_records"]}, {"alias": "pi", "kind": "derived", "block": "B1", "base_tables": ["sales_records"]}, {"alias": "pp", "kind": "base", "block": null, "base_tables": ["purchase_price"]}, {"alias": "pl", "kind": "base", "block": null, "base_tables": ["product_loss"]}] | [{"type": "INNER", "right": "proc_items AS pi", "on": "s.\"Item Code\" = pi.\"Item Code\"", "using": []}, {"type": "LEFT", "right": "purchase_price AS pp", "on": "s.\"Item Code\" = pp.\"Item Code\" AND DATE(s.\"Sales Date\") = DATE(pp.\"Date\")", "using": []}, {"type": "LEFT", "right": "product_loss AS pl", "on": "s.\"Item Code\" = pl.\"Item Code\"", "using": []}] | [] |
| B3 | [{"alias": "summer_sales", "kind": "derived", "block": "B2", "base_tables": ["product_loss", "purchase_price", "sales_records"]}] | [] | ["\"Item Code\""] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B3 | COUNT(*) | [] | [] | True |
| B3 | SUM(CASE WHEN up < wp / (1.0 - lr / 100.0) THEN 1 ELSE 0 END) | [] | [{"table": "sales_records", "column": "Unit price (yuan/kg)"}, {"table": "purchase_price", "column": "Wholesale price (yuan/kg)"}, {"table": "product_loss", "column": "Loss Rate (%)"}] | False |
| B3 | AVG(up - wp / (1.0 - lr / 100.0)) | [{"table": "sales_records", "column": "Unit price (yuan/kg)"}, {"table": "purchase_price", "column": "Wholesale price (yuan/kg)"}, {"table": "product_loss", "column": "Loss Rate (%)"}] | [] | False |
| B3 | MIN(up - wp / (1.0 - lr / 100.0)) | [{"table": "sales_records", "column": "Unit price (yuan/kg)"}, {"table": "purchase_price", "column": "Wholesale price (yuan/kg)"}, {"table": "product_loss", "column": "Loss Rate (%)"}] | [] | False |
| B3 | COUNT(*) | [] | [] | True |
| B3 | SUM(CASE WHEN up < wp / (1.0 - lr / 100.0) THEN 1 ELSE 0 END) | [] | [{"table": "sales_records", "column": "Unit price (yuan/kg)"}, {"table": "purchase_price", "column": "Wholesale price (yuan/kg)"}, {"table": "product_loss", "column": "Loss Rate (%)"}] | False |


## S41

类别 `data`；来源 `query_db`；调用 `c11be4160c3c498ca0b33802daac468d`；状态 `success`。

```sql
WITH proc_items AS (
  SELECT DISTINCT s."Item Code"
  FROM sales_records s
  WHERE date(s."Sales Date") = '2023-06-30'
),
summer_sales AS (
  SELECT s."Item Code", s."Unit price (yuan/kg)" as up, pp."Wholesale price (yuan/kg)" as wp, pl."Loss Rate (%)" as lr, s."Whether sold at a discount" as discount
  FROM sales_records s
  JOIN proc_items pi ON s."Item Code" = pi."Item Code"
  LEFT JOIN purchase_price pp ON s."Item Code" = pp."Item Code" AND date(s."Sales Date") = date(pp."Date")
  LEFT JOIN product_loss pl ON s."Item Code" = pl."Item Code"
  WHERE s."Sales type" = 'Sale'
    AND (
      (s."Sales Date" >= '2020-07-01' AND s."Sales Date" < '2020-09-01')
      OR (s."Sales Date" >= '2021-06-01' AND s."Sales Date" < '2021-09-01')
      OR (s."Sales Date" >= '2022-06-01' AND s."Sales Date" < '2022-09-01')
    )
    AND pp."Wholesale price (yuan/kg)" IS NOT NULL
    AND pl."Loss Rate (%)" IS NOT NULL
)
SELECT "Item Code",
  COUNT(*) as n_sales,
  ROUND(100.0*SUM(CASE WHEN up < wp/(1.0-lr/100.0) THEN 1 ELSE 0 END)/COUNT(*),1) as pct_loss,
  ROUND(AVG(up - wp/(1.0-lr/100.0)),3) as avg_profit,
  ROUND(AVG(up),2) as avg_up,
  ROUND(AVG(wp/(1.0-lr/100.0)),2) as avg_cost,
  ROUND(SUM(CASE WHEN discount='Yes' THEN 1 ELSE 0 END)*100.0/COUNT(*),1) as pct_discount
FROM summer_sales
GROUP BY "Item Code"
ORDER BY pct_loss DESC
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-025/attempt-01/sql/S41.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-025/attempt-01/sql/S41.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-025/attempt-01/results/S41.rows.jsonl)；完整：True；SHA256：`c98f0b535bd7c02f68c9ac003931af20737305bcf22c39a0f43910f88336c2b9`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "s", "kind": "base", "block": null, "base_tables": ["sales_records"]}] | [] | [] |
| B2 | [{"alias": "s", "kind": "base", "block": null, "base_tables": ["sales_records"]}, {"alias": "pi", "kind": "derived", "block": "B1", "base_tables": ["sales_records"]}, {"alias": "pp", "kind": "base", "block": null, "base_tables": ["purchase_price"]}, {"alias": "pl", "kind": "base", "block": null, "base_tables": ["product_loss"]}] | [{"type": "INNER", "right": "proc_items AS pi", "on": "s.\"Item Code\" = pi.\"Item Code\"", "using": []}, {"type": "LEFT", "right": "purchase_price AS pp", "on": "s.\"Item Code\" = pp.\"Item Code\" AND DATE(s.\"Sales Date\") = DATE(pp.\"Date\")", "using": []}, {"type": "LEFT", "right": "product_loss AS pl", "on": "s.\"Item Code\" = pl.\"Item Code\"", "using": []}] | [] |
| B3 | [{"alias": "summer_sales", "kind": "derived", "block": "B2", "base_tables": ["product_loss", "purchase_price", "sales_records"]}] | [] | ["\"Item Code\""] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B3 | COUNT(*) | [] | [] | True |
| B3 | AVG(up - wp / (1.0 - lr / 100.0)) | [{"table": "sales_records", "column": "Unit price (yuan/kg)"}, {"table": "purchase_price", "column": "Wholesale price (yuan/kg)"}, {"table": "product_loss", "column": "Loss Rate (%)"}] | [] | False |
| B3 | AVG(up) | [{"table": "sales_records", "column": "Unit price (yuan/kg)"}] | [] | False |
| B3 | AVG(wp / (1.0 - lr / 100.0)) | [{"table": "purchase_price", "column": "Wholesale price (yuan/kg)"}, {"table": "product_loss", "column": "Loss Rate (%)"}] | [] | False |
| B3 | COUNT(*) | [] | [] | True |
| B3 | COUNT(*) | [] | [] | True |
| B3 | SUM(CASE WHEN up < wp / (1.0 - lr / 100.0) THEN 1 ELSE 0 END) | [] | [{"table": "sales_records", "column": "Unit price (yuan/kg)"}, {"table": "purchase_price", "column": "Wholesale price (yuan/kg)"}, {"table": "product_loss", "column": "Loss Rate (%)"}] | False |
| B3 | SUM(CASE WHEN discount = 'Yes' THEN 1 ELSE 0 END) | [] | [{"table": "sales_records", "column": "Whether sold at a discount"}] | False |


## S42

类别 `data`；来源 `query_db`；调用 `2e9c31bac0c94c98b726d782908ed5a1`；状态 `success`。

```sql
WITH proc_items AS (
  SELECT DISTINCT s."Item Code"
  FROM sales_records s
  WHERE date(s."Sales Date") = '2023-06-30'
),
summer_sales AS (
  SELECT s."Item Code", s."Unit price (yuan/kg)" as up, pp."Wholesale price (yuan/kg)" as wp, pl."Loss Rate (%)" as lr
  FROM sales_records s
  JOIN proc_items pi ON s."Item Code" = pi."Item Code"
  LEFT JOIN purchase_price pp ON s."Item Code" = pp."Item Code" AND date(s."Sales Date") = date(pp."Date")
  LEFT JOIN product_loss pl ON s."Item Code" = pl."Item Code"
  WHERE s."Sales type" = 'Sale'
    AND (
      (s."Sales Date" >= '2020-07-01' AND s."Sales Date" < '2020-09-01')
      OR (s."Sales Date" >= '2021-06-01' AND s."Sales Date" < '2021-09-01')
      OR (s."Sales Date" >= '2022-06-01' AND s."Sales Date" < '2022-09-01')
    )
    AND pp."Wholesale price (yuan/kg)" IS NOT NULL
    AND pl."Loss Rate (%)" IS NOT NULL
)
SELECT "Item Code",
  COUNT(*) as n_sales,
  SUM(CASE WHEN up < wp/(1.0-lr/100.0) THEN 1 ELSE 0 END) as n_loss,
  ROUND(100.0*SUM(CASE WHEN up < wp/(1.0-lr/100.0) THEN 1 ELSE 0 END)/COUNT(*),1) as pct_loss
FROM summer_sales
GROUP BY "Item Code"
ORDER BY pct_loss DESC
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-025/attempt-01/sql/S42.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-025/attempt-01/sql/S42.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-025/attempt-01/results/S42.rows.jsonl)；完整：True；SHA256：`6b236b98070bbc48b0598d308a4683b20cd1f5f76bcf7a0d2d79d324be741207`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "s", "kind": "base", "block": null, "base_tables": ["sales_records"]}] | [] | [] |
| B2 | [{"alias": "s", "kind": "base", "block": null, "base_tables": ["sales_records"]}, {"alias": "pi", "kind": "derived", "block": "B1", "base_tables": ["sales_records"]}, {"alias": "pp", "kind": "base", "block": null, "base_tables": ["purchase_price"]}, {"alias": "pl", "kind": "base", "block": null, "base_tables": ["product_loss"]}] | [{"type": "INNER", "right": "proc_items AS pi", "on": "s.\"Item Code\" = pi.\"Item Code\"", "using": []}, {"type": "LEFT", "right": "purchase_price AS pp", "on": "s.\"Item Code\" = pp.\"Item Code\" AND DATE(s.\"Sales Date\") = DATE(pp.\"Date\")", "using": []}, {"type": "LEFT", "right": "product_loss AS pl", "on": "s.\"Item Code\" = pl.\"Item Code\"", "using": []}] | [] |
| B3 | [{"alias": "summer_sales", "kind": "derived", "block": "B2", "base_tables": ["product_loss", "purchase_price", "sales_records"]}] | [] | ["\"Item Code\""] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B3 | COUNT(*) | [] | [] | True |
| B3 | SUM(CASE WHEN up < wp / (1.0 - lr / 100.0) THEN 1 ELSE 0 END) | [] | [{"table": "sales_records", "column": "Unit price (yuan/kg)"}, {"table": "purchase_price", "column": "Wholesale price (yuan/kg)"}, {"table": "product_loss", "column": "Loss Rate (%)"}] | False |
| B3 | COUNT(*) | [] | [] | True |
| B3 | SUM(CASE WHEN up < wp / (1.0 - lr / 100.0) THEN 1 ELSE 0 END) | [] | [{"table": "sales_records", "column": "Unit price (yuan/kg)"}, {"table": "purchase_price", "column": "Wholesale price (yuan/kg)"}, {"table": "product_loss", "column": "Loss Rate (%)"}] | False |


## S43

类别 `data`；来源 `query_db`；调用 `29eb10d8fdf74e23927aeb3517632f85`；状态 `success`。

```sql
SELECT pi."Item Code", pi."Item Name", pi."Category Name", pl."Loss Rate (%)"
FROM product_information pi
LEFT JOIN product_loss pl ON pi."Item Code" = pl."Item Code"
WHERE pi."Item Code" IN (102900011032732, 102900011034439, 102900005118824, 102900011034330, 102900011001691)
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-025/attempt-01/sql/S43.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-025/attempt-01/sql/S43.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-025/attempt-01/results/S43.rows.jsonl)；完整：True；SHA256：`f978cce621099944ed47ecb7c098a3c6ff9a86fa353b6f905e82a30a571319ea`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "pi", "kind": "base", "block": null, "base_tables": ["product_information"]}, {"alias": "pl", "kind": "base", "block": null, "base_tables": ["product_loss"]}] | [{"type": "LEFT", "right": "product_loss AS pl", "on": "pi.\"Item Code\" = pl.\"Item Code\"", "using": []}] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |


## S44

类别 `data`；来源 `query_db`；调用 `db2b92d8c9654f72be7410417a5b2d28`；状态 `success`。

```sql
SELECT s."Item Code", p."Item Name",
  ROUND(SUM(s."Sales volume (kg)"),2) as vol_0630
FROM sales_records s
LEFT JOIN product_information p ON s."Item Code" = p."Item Code"
WHERE date(s."Sales Date") = '2023-06-30'
GROUP BY s."Item Code"
ORDER BY vol_0630 DESC
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-025/attempt-01/sql/S44.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-025/attempt-01/sql/S44.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-025/attempt-01/results/S44.rows.jsonl)；完整：True；SHA256：`d7d508dea84546540b6937267a1ed0348ac96e9063ea4c4ad36ed789c6cf7bbe`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "s", "kind": "base", "block": null, "base_tables": ["sales_records"]}, {"alias": "p", "kind": "base", "block": null, "base_tables": ["product_information"]}] | [{"type": "LEFT", "right": "product_information AS p", "on": "s.\"Item Code\" = p.\"Item Code\"", "using": []}] | ["s.\"Item Code\""] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | SUM(s."Sales volume (kg)") | [{"table": "sales_records", "column": "Sales volume (kg)"}] | [] | False |


## S45

类别 `data`；来源 `query_db`；调用 `c462b0c082c54e60abd40ce98a70cde2`；状态 `success`。

```sql
SELECT * FROM sales_records WHERE "Item Code" = 102900011032732 AND date("Sales Date") = '2023-06-30'
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-025/attempt-01/sql/S45.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-025/attempt-01/sql/S45.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-025/attempt-01/results/S45.rows.jsonl)；完整：True；SHA256：`5c2ff03edbd1e046b220875c35d86ae3e65b175bd9da34a38e8946611e9efd9c`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "sales_records", "kind": "base", "block": null, "base_tables": ["sales_records"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |


## S46

类别 `data`；来源 `query_db`；调用 `c1de7cf622e547fd88bfd3a49d5cdbc7`；状态 `success`。

```sql
SELECT * FROM purchase_price WHERE "Item Code" = 102900011032732 AND "Date" >= '2023-06-25' AND "Date" <= '2023-06-30'
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-025/attempt-01/sql/S46.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-025/attempt-01/sql/S46.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-025/attempt-01/results/S46.rows.jsonl)；完整：True；SHA256：`b0e967b55b5674961547ffd497b7833856d8cc5843aeb5582a88b02ddb5fa087`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "purchase_price", "kind": "base", "block": null, "base_tables": ["purchase_price"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |


## S47

类别 `data`；来源 `query_db`；调用 `9cdc72d1e31f4b2fb937cbd283447c40`；状态 `success`。

```sql
SELECT * FROM product_loss WHERE "Item Code" = 102900011032732
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-025/attempt-01/sql/S47.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-025/attempt-01/sql/S47.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-025/attempt-01/results/S47.rows.jsonl)；完整：True；SHA256：`81ac8420ffc1b6b1b8bd8392715cedeea5db663138346b03aeb5933be4b1853b`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "product_loss", "kind": "base", "block": null, "base_tables": ["product_loss"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |


## S48

类别 `data`；来源 `query_db`；调用 `be438bb0bf03440f8601e1e6912a3bd3`；状态 `success`。

```sql
WITH proc_items AS (
  SELECT DISTINCT s."Item Code"
  FROM sales_records s
  WHERE date(s."Sales Date") = '2023-06-30'
),
summer_items AS (
  SELECT DISTINCT s."Item Code"
  FROM sales_records s
  LEFT JOIN purchase_price pp ON s."Item Code" = pp."Item Code" AND date(s."Sales Date") = date(pp."Date")
  LEFT JOIN product_loss pl ON s."Item Code" = pl."Item Code"
  WHERE s."Sales type" = 'Sale'
    AND (
      (s."Sales Date" >= '2020-07-01' AND s."Sales Date" < '2020-09-01')
      OR (s."Sales Date" >= '2021-06-01' AND s."Sales Date" < '2021-09-01')
      OR (s."Sales Date" >= '2022-06-01' AND s."Sales Date" < '2022-09-01')
    )
    AND pp."Wholesale price (yuan/kg)" IS NOT NULL
    AND pl."Loss Rate (%)" IS NOT NULL
)
SELECT pi."Item Code", p."Item Name"
FROM proc_items pi
LEFT JOIN product_information p ON pi."Item Code" = p."Item Code"
WHERE pi."Item Code" NOT IN (SELECT "Item Code" FROM summer_items)
ORDER BY pi."Item Code"
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-025/attempt-01/sql/S48.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-025/attempt-01/sql/S48.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-025/attempt-01/results/S48.rows.jsonl)；完整：True；SHA256：`fc99752c343fe7cb69ffe483319231cc10cb0dfc3013fe052f281b5ec2451323`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "s", "kind": "base", "block": null, "base_tables": ["sales_records"]}] | [] | [] |
| B2 | [{"alias": "s", "kind": "base", "block": null, "base_tables": ["sales_records"]}, {"alias": "pp", "kind": "base", "block": null, "base_tables": ["purchase_price"]}, {"alias": "pl", "kind": "base", "block": null, "base_tables": ["product_loss"]}] | [{"type": "LEFT", "right": "purchase_price AS pp", "on": "s.\"Item Code\" = pp.\"Item Code\" AND DATE(s.\"Sales Date\") = DATE(pp.\"Date\")", "using": []}, {"type": "LEFT", "right": "product_loss AS pl", "on": "s.\"Item Code\" = pl.\"Item Code\"", "using": []}] | [] |
| B3 | [{"alias": "summer_items", "kind": "derived", "block": "B2", "base_tables": ["product_loss", "purchase_price", "sales_records"]}] | [] | [] |
| B4 | [{"alias": "pi", "kind": "derived", "block": "B1", "base_tables": ["sales_records"]}, {"alias": "p", "kind": "base", "block": null, "base_tables": ["product_information"]}] | [{"type": "LEFT", "right": "product_information AS p", "on": "pi.\"Item Code\" = p.\"Item Code\"", "using": []}] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |


未解析列血缘：[{"block": "B4", "column": "\"Item Code\"", "reason": "ambiguous_or_missing_source"}]

## S49

类别 `data`；来源 `query_db`；调用 `e59fb2d7849445eb8b27d159eb5495fa`；状态 `success`。

```sql
SELECT s."Item Code", COUNT(*) as n_sales
FROM sales_records s
WHERE s."Item Code" IN (102900011018132, 102900011031926, 102900011035740, 102900011036686, 106971533450003)
  AND s."Sales type" = 'Sale'
  AND (
    (s."Sales Date" >= '2020-07-01' AND s."Sales Date" < '2020-09-01')
    OR (s."Sales Date" >= '2021-06-01' AND s."Sales Date" < '2021-09-01')
    OR (s."Sales Date" >= '2022-06-01' AND s."Sales Date" < '2022-09-01')
  )
GROUP BY s."Item Code"
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-025/attempt-01/sql/S49.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-025/attempt-01/sql/S49.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-025/attempt-01/results/S49.rows.jsonl)；完整：True；SHA256：`e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "s", "kind": "base", "block": null, "base_tables": ["sales_records"]}] | [] | ["s.\"Item Code\""] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |


## S50

类别 `data`；来源 `query_db`；调用 `4ab9bde690524095898d9735d419c105`；状态 `success`。

```sql
SELECT "Item Code", COUNT(*) as n_prices
FROM purchase_price
WHERE "Item Code" IN (102900011018132, 102900011031926, 102900011035740, 102900011036686, 106971533450003)
GROUP BY "Item Code"
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-025/attempt-01/sql/S50.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-025/attempt-01/sql/S50.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-025/attempt-01/results/S50.rows.jsonl)；完整：True；SHA256：`f0a2387046fcc0e8c1800a72b6f99f12a01c51ce2144e79c31393cb18c9effef`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "purchase_price", "kind": "base", "block": null, "base_tables": ["purchase_price"]}] | [] | ["\"Item Code\""] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |


## S51

类别 `data`；来源 `query_db`；调用 `98b3f75edf034b45bf6c68ba7e5bafc4`；状态 `success`。

```sql
SELECT s."Item Code", p."Item Name",
  s."Unit price (yuan/kg)" as unit_price,
  pp."Wholesale price (yuan/kg)" as wholesale,
  pl."Loss Rate (%)" as loss_rate,
  ROUND(pp."Wholesale price (yuan/kg)"/(1.0-pl."Loss Rate (%)"/100.0),3) as eff_cost,
  ROUND(s."Unit price (yuan/kg)" - pp."Wholesale price (yuan/kg)"/(1.0-pl."Loss Rate (%)"/100.0),3) as profit_per_kg,
  s."Sales volume (kg)" as vol,
  s."Whether sold at a discount" as discount
FROM sales_records s
LEFT JOIN product_information p ON s."Item Code" = p."Item Code"
LEFT JOIN purchase_price pp ON s."Item Code" = pp."Item Code" AND date(s."Sales Date") = date(pp."Date")
LEFT JOIN product_loss pl ON s."Item Code" = pl."Item Code"
WHERE date(s."Sales Date") = '2023-06-30'
  AND s."Sales type" = 'Sale'
  AND pp."Wholesale price (yuan/kg)" IS NOT NULL
  AND pl."Loss Rate (%)" IS NOT NULL
ORDER BY profit_per_kg ASC
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-025/attempt-01/sql/S51.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-025/attempt-01/sql/S51.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-025/attempt-01/results/S51.rows.jsonl)；完整：True；SHA256：`25999de4ac83102aea8ec93e9b94b723870b6c0f283f59800ca0e429ae4caf05`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "s", "kind": "base", "block": null, "base_tables": ["sales_records"]}, {"alias": "p", "kind": "base", "block": null, "base_tables": ["product_information"]}, {"alias": "pp", "kind": "base", "block": null, "base_tables": ["purchase_price"]}, {"alias": "pl", "kind": "base", "block": null, "base_tables": ["product_loss"]}] | [{"type": "LEFT", "right": "product_information AS p", "on": "s.\"Item Code\" = p.\"Item Code\"", "using": []}, {"type": "LEFT", "right": "purchase_price AS pp", "on": "s.\"Item Code\" = pp.\"Item Code\" AND DATE(s.\"Sales Date\") = DATE(pp.\"Date\")", "using": []}, {"type": "LEFT", "right": "product_loss AS pl", "on": "s.\"Item Code\" = pl.\"Item Code\"", "using": []}] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |


## S52

类别 `data`；来源 `query_db`；调用 `c8c57e7013c642a4a3df8589d0fa2bb2`；状态 `success`。

```sql
SELECT s."Item Code", p."Item Name",
  COUNT(*) as n_sales,
  SUM(s."Sales volume (kg)") as total_vol,
  ROUND(SUM(s."Sales volume (kg)" * (s."Unit price (yuan/kg)" - pp."Wholesale price (yuan/kg)")/(1.0-pl."Loss Rate (%)"/100.0)),2) as total_profit_loss,
  ROUND(AVG(s."Unit price (yuan/kg)" - pp."Wholesale price (yuan/kg)")/(1.0-pl."Loss Rate (%)"/100.0),3) as avg_profit_per_kg,
  SUM(CASE WHEN s."Unit price (yuan/kg)" < pp."Wholesale price (yuan/kg)"/(1.0-pl."Loss Rate (%)"/100.0) THEN 1 ELSE 0 END) as n_loss_sales
FROM sales_records s
LEFT JOIN product_information p ON s."Item Code" = p."Item Code"
LEFT JOIN purchase_price pp ON s."Item Code" = pp."Item Code" AND date(s."Sales Date") = date(pp."Date")
LEFT JOIN product_loss pl ON s."Item Code" = pl."Item Code"
WHERE date(s."Sales Date") = '2023-06-30'
  AND s."Sales type" = 'Sale'
  AND pp."Wholesale price (yuan/kg)" IS NOT NULL
  AND pl."Loss Rate (%)" IS NOT NULL
GROUP BY s."Item Code"
HAVING total_profit_loss < 0 OR n_loss_sales > 0
ORDER BY total_profit_loss ASC
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-025/attempt-01/sql/S52.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-025/attempt-01/sql/S52.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-025/attempt-01/results/S52.rows.jsonl)；完整：True；SHA256：`34b21456d893c1a9e904a537e4afddc91e7752064e8f27d75fe022e853b60e27`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "s", "kind": "base", "block": null, "base_tables": ["sales_records"]}, {"alias": "p", "kind": "base", "block": null, "base_tables": ["product_information"]}, {"alias": "pp", "kind": "base", "block": null, "base_tables": ["purchase_price"]}, {"alias": "pl", "kind": "base", "block": null, "base_tables": ["product_loss"]}] | [{"type": "LEFT", "right": "product_information AS p", "on": "s.\"Item Code\" = p.\"Item Code\"", "using": []}, {"type": "LEFT", "right": "purchase_price AS pp", "on": "s.\"Item Code\" = pp.\"Item Code\" AND DATE(s.\"Sales Date\") = DATE(pp.\"Date\")", "using": []}, {"type": "LEFT", "right": "product_loss AS pl", "on": "s.\"Item Code\" = pl.\"Item Code\"", "using": []}] | ["s.\"Item Code\""] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |
| B1 | SUM(s."Sales volume (kg)") | [{"table": "sales_records", "column": "Sales volume (kg)"}] | [] | False |
| B1 | SUM(CASE WHEN s."Unit price (yuan/kg)" < pp."Wholesale price (yuan/kg)" / (1.0 - pl."Loss Rate (%)" / 100.0) THEN 1 ELSE 0 END) | [] | [{"table": "sales_records", "column": "Unit price (yuan/kg)"}, {"table": "purchase_price", "column": "Wholesale price (yuan/kg)"}, {"table": "product_loss", "column": "Loss Rate (%)"}] | False |
| B1 | SUM(s."Sales volume (kg)" * (s."Unit price (yuan/kg)" - pp."Wholesale price (yuan/kg)") / (1.0 - pl."Loss Rate (%)" / 100.0)) | [{"table": "sales_records", "column": "Sales volume (kg)"}, {"table": "sales_records", "column": "Unit price (yuan/kg)"}, {"table": "purchase_price", "column": "Wholesale price (yuan/kg)"}, {"table": "product_loss", "column": "Loss Rate (%)"}] | [] | False |
| B1 | AVG(s."Unit price (yuan/kg)" - pp."Wholesale price (yuan/kg)") | [{"table": "sales_records", "column": "Unit price (yuan/kg)"}, {"table": "purchase_price", "column": "Wholesale price (yuan/kg)"}] | [] | False |


## S53

类别 `data`；来源 `query_db`；调用 `22b6b14c756c4525a91e922c0974f085`；状态 `success`。

```sql
WITH proc_items AS (
  SELECT DISTINCT s."Item Code"
  FROM sales_records s
  WHERE date(s."Sales Date") = '2023-06-30'
),
summer_analysis AS (
  SELECT s."Item Code",
    s."Sales volume (kg)" as vol,
    s."Unit price (yuan/kg)" as up,
    pp."Wholesale price (yuan/kg)" as wp,
    pl."Loss Rate (%)" as lr,
    s."Whether sold at a discount" as discount,
    s."Unit price (yuan/kg)" - pp."Wholesale price (yuan/kg)"/(1.0-pl."Loss Rate (%)"/100.0) as profit
  FROM sales_records s
  JOIN proc_items pi ON s."Item Code" = pi."Item Code"
  LEFT JOIN purchase_price pp ON s."Item Code" = pp."Item Code" AND date(s."Sales Date") = date(pp."Date")
  LEFT JOIN product_loss pl ON s."Item Code" = pl."Item Code"
  WHERE s."Sales type" = 'Sale'
    AND (
      (s."Sales Date" >= '2020-07-01' AND s."Sales Date" < '2020-09-01')
      OR (s."Sales Date" >= '2021-06-01' AND s."Sales Date" < '2021-09-01')
      OR (s."Sales Date" >= '2022-06-01' AND s."Sales Date" < '2022-09-01')
    )
    AND pp."Wholesale price (yuan/kg)" IS NOT NULL
    AND pl."Loss Rate (%)" IS NOT NULL
)
SELECT "Item Code",
  COUNT(*) as n_sales,
  ROUND(SUM(vol*profit),2) as total_profit,
  ROUND(AVG(profit),3) as avg_profit_per_kg,
  ROUND(SUM(CASE WHEN profit < 0 THEN 1 ELSE 0 END)*100.0/COUNT(*),1) as pct_loss,
  ROUND(SUM(CASE WHEN profit < 0 THEN vol ELSE 0 END)*100.0/SUM(vol),1) as vol_weighted_pct_loss,
  ROUND(SUM(CASE WHEN profit < 0 THEN 1 ELSE 0 END),0) as n_loss,
  ROUND(SUM(CASE WHEN profit < 0 THEN 1 ELSE 0 END)*100.0/COUNT(*),1) as pct_loss
FROM summer_analysis
GROUP BY "Item Code"
ORDER BY pct_loss DESC, avg_profit_per_kg ASC
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-025/attempt-01/sql/S53.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-025/attempt-01/sql/S53.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-025/attempt-01/results/S53.rows.jsonl)；完整：True；SHA256：`eba19e5a85704fbe75239b4c6072b7162d5904de62aa31ce1522dd9b9da1dc31`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "s", "kind": "base", "block": null, "base_tables": ["sales_records"]}] | [] | [] |
| B2 | [{"alias": "s", "kind": "base", "block": null, "base_tables": ["sales_records"]}, {"alias": "pi", "kind": "derived", "block": "B1", "base_tables": ["sales_records"]}, {"alias": "pp", "kind": "base", "block": null, "base_tables": ["purchase_price"]}, {"alias": "pl", "kind": "base", "block": null, "base_tables": ["product_loss"]}] | [{"type": "INNER", "right": "proc_items AS pi", "on": "s.\"Item Code\" = pi.\"Item Code\"", "using": []}, {"type": "LEFT", "right": "purchase_price AS pp", "on": "s.\"Item Code\" = pp.\"Item Code\" AND DATE(s.\"Sales Date\") = DATE(pp.\"Date\")", "using": []}, {"type": "LEFT", "right": "product_loss AS pl", "on": "s.\"Item Code\" = pl.\"Item Code\"", "using": []}] | [] |
| B3 | [{"alias": "summer_analysis", "kind": "derived", "block": "B2", "base_tables": ["product_loss", "purchase_price", "sales_records"]}] | [] | ["\"Item Code\""] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B3 | COUNT(*) | [] | [] | True |
| B3 | SUM(vol * profit) | [{"table": "sales_records", "column": "Sales volume (kg)"}, {"table": "sales_records", "column": "Unit price (yuan/kg)"}, {"table": "purchase_price", "column": "Wholesale price (yuan/kg)"}, {"table": "product_loss", "column": "Loss Rate (%)"}] | [] | False |
| B3 | AVG(profit) | [{"table": "sales_records", "column": "Unit price (yuan/kg)"}, {"table": "purchase_price", "column": "Wholesale price (yuan/kg)"}, {"table": "product_loss", "column": "Loss Rate (%)"}] | [] | False |
| B3 | SUM(CASE WHEN profit < 0 THEN 1 ELSE 0 END) | [] | [{"table": "sales_records", "column": "Unit price (yuan/kg)"}, {"table": "purchase_price", "column": "Wholesale price (yuan/kg)"}, {"table": "product_loss", "column": "Loss Rate (%)"}] | False |
| B3 | COUNT(*) | [] | [] | True |
| B3 | SUM(vol) | [{"table": "sales_records", "column": "Sales volume (kg)"}] | [] | False |
| B3 | COUNT(*) | [] | [] | True |
| B3 | SUM(CASE WHEN profit < 0 THEN 1 ELSE 0 END) | [] | [{"table": "sales_records", "column": "Unit price (yuan/kg)"}, {"table": "purchase_price", "column": "Wholesale price (yuan/kg)"}, {"table": "product_loss", "column": "Loss Rate (%)"}] | False |
| B3 | SUM(CASE WHEN profit < 0 THEN vol ELSE 0 END) | [{"table": "sales_records", "column": "Sales volume (kg)"}] | [{"table": "sales_records", "column": "Unit price (yuan/kg)"}, {"table": "purchase_price", "column": "Wholesale price (yuan/kg)"}, {"table": "product_loss", "column": "Loss Rate (%)"}] | False |
| B3 | SUM(CASE WHEN profit < 0 THEN 1 ELSE 0 END) | [] | [{"table": "sales_records", "column": "Unit price (yuan/kg)"}, {"table": "purchase_price", "column": "Wholesale price (yuan/kg)"}, {"table": "product_loss", "column": "Loss Rate (%)"}] | False |


## S54

类别 `data`；来源 `query_db`；调用 `ada75e58e1b443e9afa42845f5e9f9e9`；状态 `success`。

```sql
WITH proc_items AS (
  SELECT DISTINCT s."Item Code"
  FROM sales_records s
  WHERE date(s."Sales Date") = '2023-06-30'
),
summer_analysis AS (
  SELECT s."Item Code",
    strftime('%Y', s."Sales Date") as yr,
    s."Unit price (yuan/kg)" as up,
    pp."Wholesale price (yuan/kg)" as wp,
    pl."Loss Rate (%)" as lr,
    s."Unit price (yuan/kg)" - pp."Wholesale price (yuan/kg)"/(1.0-pl."Loss Rate (%)"/100.0) as profit
  FROM sales_records s
  JOIN proc_items pi ON s."Item Code" = pi."Item Code"
  LEFT JOIN purchase_price pp ON s."Item Code" = pp."Item Code" AND date(s."Sales Date") = date(pp."Date")
  LEFT JOIN product_loss pl ON s."Item Code" = pl."Item Code"
  WHERE s."Sales type" = 'Sale'
    AND (
      (s."Sales Date" >= '2020-07-01' AND s."Sales Date" < '2020-09-01')
      OR (s."Sales Date" >= '2021-06-01' AND s."Sales Date" < '2021-09-01')
      OR (s."Sales Date" >= '2022-06-01' AND s."Sales Date" < '2022-09-01')
    )
    AND pp."Wholesale price (yuan/kg)" IS NOT NULL
    AND pl."Loss Rate (%)" IS NOT NULL
)
SELECT "Item Code", yr, COUNT(*) as n, ROUND(AVG(profit),3) as avg_profit,
  ROUND(SUM(CASE WHEN profit<0 THEN 1 ELSE 0 END)*100.0/COUNT(*),1) as pct_loss
FROM summer_analysis
WHERE "Item Code" IN (102900011032732, 102900005118824, 102900011034439, 102900011034330, 102900011001691, 102900011030110, 102900051000944)
GROUP BY "Item Code", yr
ORDER BY "Item Code", yr
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-025/attempt-01/sql/S54.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-025/attempt-01/sql/S54.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-025/attempt-01/results/S54.rows.jsonl)；完整：True；SHA256：`37d3a8c1a2fb7c5fa9dc7f7cccda2513ee9b342a4830661c4a50ea53efc1ace8`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "s", "kind": "base", "block": null, "base_tables": ["sales_records"]}] | [] | [] |
| B2 | [{"alias": "s", "kind": "base", "block": null, "base_tables": ["sales_records"]}, {"alias": "pi", "kind": "derived", "block": "B1", "base_tables": ["sales_records"]}, {"alias": "pp", "kind": "base", "block": null, "base_tables": ["purchase_price"]}, {"alias": "pl", "kind": "base", "block": null, "base_tables": ["product_loss"]}] | [{"type": "INNER", "right": "proc_items AS pi", "on": "s.\"Item Code\" = pi.\"Item Code\"", "using": []}, {"type": "LEFT", "right": "purchase_price AS pp", "on": "s.\"Item Code\" = pp.\"Item Code\" AND DATE(s.\"Sales Date\") = DATE(pp.\"Date\")", "using": []}, {"type": "LEFT", "right": "product_loss AS pl", "on": "s.\"Item Code\" = pl.\"Item Code\"", "using": []}] | [] |
| B3 | [{"alias": "summer_analysis", "kind": "derived", "block": "B2", "base_tables": ["product_loss", "purchase_price", "sales_records"]}] | [] | ["\"Item Code\"", "yr"] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B3 | COUNT(*) | [] | [] | True |
| B3 | AVG(profit) | [{"table": "sales_records", "column": "Unit price (yuan/kg)"}, {"table": "purchase_price", "column": "Wholesale price (yuan/kg)"}, {"table": "product_loss", "column": "Loss Rate (%)"}] | [] | False |
| B3 | COUNT(*) | [] | [] | True |
| B3 | SUM(CASE WHEN profit < 0 THEN 1 ELSE 0 END) | [] | [{"table": "sales_records", "column": "Unit price (yuan/kg)"}, {"table": "purchase_price", "column": "Wholesale price (yuan/kg)"}, {"table": "product_loss", "column": "Loss Rate (%)"}] | False |


## S55

类别 `data`；来源 `query_db`；调用 `7f4e8220dffa4200a2cca5ebdf02a0e6`；状态 `success`。

```sql
WITH proc_items AS (
  SELECT DISTINCT s."Item Code"
  FROM sales_records s
  WHERE date(s."Sales Date") = '2023-06-30'
),
summer_analysis AS (
  SELECT s."Item Code",
    s."Sales volume (kg)" as vol,
    s."Unit price (yuan/kg)" as up,
    pp."Wholesale price (yuan/kg)" as wp,
    pl."Loss Rate (%)" as lr,
    s."Unit price (yuan/kg)" - pp."Wholesale price (yuan/kg)"/(1.0-pl."Loss Rate (%)"/100.0) as profit
  FROM sales_records s
  JOIN proc_items pi ON s."Item Code" = pi."Item Code"
  LEFT JOIN purchase_price pp ON s."Item Code" = pp."Item Code" AND date(s."Sales Date") = date(pp."Date")
  LEFT JOIN product_loss pl ON s."Item Code" = pl."Item Code"
  WHERE s."Sales type" = 'Sale'
    AND s."Sales Date" >= '2022-06-01' AND s."Sales Date" < '2022-09-01'
    AND pp."Wholesale price (yuan/kg)" IS NOT NULL
    AND pl."Loss Rate (%)" IS NOT NULL
)
SELECT "Item Code",
  COUNT(*) as n_sales,
  ROUND(AVG(profit),3) as avg_profit_per_kg,
  ROUND(SUM(CASE WHEN profit<0 THEN 1 ELSE 0 END)*100.0/COUNT(*),1) as pct_loss,
  ROUND(SUM(CASE WHEN profit<0 THEN 1 ELSE 0 END),0) as n_loss,
  ROUND(SUM(vol*profit),2) as total_profit
FROM summer_analysis
GROUP BY "Item Code"
HAVING COUNT(*) >= 10
ORDER BY avg_profit_per_kg ASC
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-025/attempt-01/sql/S55.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-025/attempt-01/sql/S55.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-025/attempt-01/results/S55.rows.jsonl)；完整：True；SHA256：`84ae59279e5388bdd74406074f8dc90173da1ee89b19c6544279a7b44e6e0ec8`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "s", "kind": "base", "block": null, "base_tables": ["sales_records"]}] | [] | [] |
| B2 | [{"alias": "s", "kind": "base", "block": null, "base_tables": ["sales_records"]}, {"alias": "pi", "kind": "derived", "block": "B1", "base_tables": ["sales_records"]}, {"alias": "pp", "kind": "base", "block": null, "base_tables": ["purchase_price"]}, {"alias": "pl", "kind": "base", "block": null, "base_tables": ["product_loss"]}] | [{"type": "INNER", "right": "proc_items AS pi", "on": "s.\"Item Code\" = pi.\"Item Code\"", "using": []}, {"type": "LEFT", "right": "purchase_price AS pp", "on": "s.\"Item Code\" = pp.\"Item Code\" AND DATE(s.\"Sales Date\") = DATE(pp.\"Date\")", "using": []}, {"type": "LEFT", "right": "product_loss AS pl", "on": "s.\"Item Code\" = pl.\"Item Code\"", "using": []}] | [] |
| B3 | [{"alias": "summer_analysis", "kind": "derived", "block": "B2", "base_tables": ["product_loss", "purchase_price", "sales_records"]}] | [] | ["\"Item Code\""] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B3 | COUNT(*) | [] | [] | True |
| B3 | AVG(profit) | [{"table": "sales_records", "column": "Unit price (yuan/kg)"}, {"table": "purchase_price", "column": "Wholesale price (yuan/kg)"}, {"table": "product_loss", "column": "Loss Rate (%)"}] | [] | False |
| B3 | SUM(CASE WHEN profit < 0 THEN 1 ELSE 0 END) | [] | [{"table": "sales_records", "column": "Unit price (yuan/kg)"}, {"table": "purchase_price", "column": "Wholesale price (yuan/kg)"}, {"table": "product_loss", "column": "Loss Rate (%)"}] | False |
| B3 | SUM(vol * profit) | [{"table": "sales_records", "column": "Sales volume (kg)"}, {"table": "sales_records", "column": "Unit price (yuan/kg)"}, {"table": "purchase_price", "column": "Wholesale price (yuan/kg)"}, {"table": "product_loss", "column": "Loss Rate (%)"}] | [] | False |
| B3 | COUNT(*) | [] | [] | True |
| B3 | COUNT(*) | [] | [] | True |
| B3 | SUM(CASE WHEN profit < 0 THEN 1 ELSE 0 END) | [] | [{"table": "sales_records", "column": "Unit price (yuan/kg)"}, {"table": "purchase_price", "column": "Wholesale price (yuan/kg)"}, {"table": "product_loss", "column": "Loss Rate (%)"}] | False |


## S56

类别 `data`；来源 `query_db`；调用 `a8e5ac6559974f09bbadcbbc104ce7a9`；状态 `success`。

```sql
WITH proc_items AS (
  SELECT DISTINCT s."Item Code"
  FROM sales_records s
  WHERE date(s."Sales Date") = '2023-06-30'
),
summer_analysis AS (
  SELECT s."Item Code",
    s."Sales volume (kg)" as vol,
    s."Unit price (yuan/kg)" as up,
    pp."Wholesale price (yuan/kg)" as wp,
    pl."Loss Rate (%)" as lr,
    s."Unit price (yuan/kg)" - pp."Wholesale price (yuan/kg)"/(1.0-pl."Loss Rate (%)"/100.0) as profit
  FROM sales_records s
  JOIN proc_items pi ON s."Item Code" = pi."Item Code"
  LEFT JOIN purchase_price pp ON s."Item Code" = pp."Item Code" AND date(s."Sales Date") = date(pp."Date")
  LEFT JOIN product_loss pl ON s."Item Code" = pl."Item Code"
  WHERE s."Sales type" = 'Sale'
    AND s."Sales Date" >= '2022-06-01' AND s."Sales Date" < '2022-09-01'
    AND pp."Wholesale price (yuan/kg)" IS NOT NULL
    AND pl."Loss Rate (%)" IS NOT NULL
)
SELECT "Item Code",
  COUNT(*) as n_sales,
  ROUND(SUM(CASE WHEN profit<0 THEN 1 ELSE 0 END)*100.0/COUNT(*),1) as pct_loss,
  ROUND(AVG(profit),3) as avg_profit_per_kg,
  ROUND(SUM(vol*profit),2) as total_profit
FROM summer_analysis
GROUP BY "Item Code"
ORDER BY avg_profit_per_kg ASC
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-025/attempt-01/sql/S56.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-025/attempt-01/sql/S56.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-025/attempt-01/results/S56.rows.jsonl)；完整：True；SHA256：`a066ef0407b7a72be2b66f0b1fae5cece62fae10ba62c419f57c6e697ca20bbc`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "s", "kind": "base", "block": null, "base_tables": ["sales_records"]}] | [] | [] |
| B2 | [{"alias": "s", "kind": "base", "block": null, "base_tables": ["sales_records"]}, {"alias": "pi", "kind": "derived", "block": "B1", "base_tables": ["sales_records"]}, {"alias": "pp", "kind": "base", "block": null, "base_tables": ["purchase_price"]}, {"alias": "pl", "kind": "base", "block": null, "base_tables": ["product_loss"]}] | [{"type": "INNER", "right": "proc_items AS pi", "on": "s.\"Item Code\" = pi.\"Item Code\"", "using": []}, {"type": "LEFT", "right": "purchase_price AS pp", "on": "s.\"Item Code\" = pp.\"Item Code\" AND DATE(s.\"Sales Date\") = DATE(pp.\"Date\")", "using": []}, {"type": "LEFT", "right": "product_loss AS pl", "on": "s.\"Item Code\" = pl.\"Item Code\"", "using": []}] | [] |
| B3 | [{"alias": "summer_analysis", "kind": "derived", "block": "B2", "base_tables": ["product_loss", "purchase_price", "sales_records"]}] | [] | ["\"Item Code\""] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B3 | COUNT(*) | [] | [] | True |
| B3 | AVG(profit) | [{"table": "sales_records", "column": "Unit price (yuan/kg)"}, {"table": "purchase_price", "column": "Wholesale price (yuan/kg)"}, {"table": "product_loss", "column": "Loss Rate (%)"}] | [] | False |
| B3 | SUM(vol * profit) | [{"table": "sales_records", "column": "Sales volume (kg)"}, {"table": "sales_records", "column": "Unit price (yuan/kg)"}, {"table": "purchase_price", "column": "Wholesale price (yuan/kg)"}, {"table": "product_loss", "column": "Loss Rate (%)"}] | [] | False |
| B3 | COUNT(*) | [] | [] | True |
| B3 | SUM(CASE WHEN profit < 0 THEN 1 ELSE 0 END) | [] | [{"table": "sales_records", "column": "Unit price (yuan/kg)"}, {"table": "purchase_price", "column": "Wholesale price (yuan/kg)"}, {"table": "product_loss", "column": "Loss Rate (%)"}] | False |


## S57

类别 `data`；来源 `query_db`；调用 `aa2d556e676a468e9d2ac208abbf2cdd`；状态 `success`。

```sql
WITH proc_items AS (
  SELECT DISTINCT s."Item Code"
  FROM sales_records s
  WHERE date(s."Sales Date") = '2023-06-30'
),
summer_analysis AS (
  SELECT s."Item Code",
    s."Unit price (yuan/kg)" as up,
    pp."Wholesale price (yuan/kg)" as wp,
    s."Unit price (yuan/kg)" - pp."Wholesale price (yuan/kg)" as profit_simple
  FROM sales_records s
  JOIN proc_items pi ON s."Item Code" = pi."Item Code"
  LEFT JOIN purchase_price pp ON s."Item Code" = pp."Item Code" AND date(s."Sales Date") = date(pp."Date")
  WHERE s."Sales type" = 'Sale'
    AND s."Sales Date" >= '2022-06-01' AND s."Sales Date" < '2022-09-01'
    AND pp."Wholesale price (yuan/kg)" IS NOT NULL
)
SELECT "Item Code",
  COUNT(*) as n_sales,
  ROUND(AVG(profit_simple),3) as avg_profit_simple,
  ROUND(SUM(CASE WHEN profit_simple<0 THEN 1 ELSE 0 END)*100.0/COUNT(*),1) as pct_loss_simple,
  ROUND(SUM(CASE WHEN profit_simple<0 THEN 1 ELSE 0 END),0) as n_loss_simple
FROM summer_analysis
GROUP BY "Item Code"
ORDER BY avg_profit_simple ASC
LIMIT 15
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-025/attempt-01/sql/S57.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-025/attempt-01/sql/S57.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-025/attempt-01/results/S57.rows.jsonl)；完整：True；SHA256：`ed5a86496397b1ed4261c7e6a4ebc79583d1cc84a559a635a0e25ed617eda9c1`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "s", "kind": "base", "block": null, "base_tables": ["sales_records"]}] | [] | [] |
| B2 | [{"alias": "s", "kind": "base", "block": null, "base_tables": ["sales_records"]}, {"alias": "pi", "kind": "derived", "block": "B1", "base_tables": ["sales_records"]}, {"alias": "pp", "kind": "base", "block": null, "base_tables": ["purchase_price"]}] | [{"type": "INNER", "right": "proc_items AS pi", "on": "s.\"Item Code\" = pi.\"Item Code\"", "using": []}, {"type": "LEFT", "right": "purchase_price AS pp", "on": "s.\"Item Code\" = pp.\"Item Code\" AND DATE(s.\"Sales Date\") = DATE(pp.\"Date\")", "using": []}] | [] |
| B3 | [{"alias": "summer_analysis", "kind": "derived", "block": "B2", "base_tables": ["purchase_price", "sales_records"]}] | [] | ["\"Item Code\""] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B3 | COUNT(*) | [] | [] | True |
| B3 | AVG(profit_simple) | [{"table": "sales_records", "column": "Unit price (yuan/kg)"}, {"table": "purchase_price", "column": "Wholesale price (yuan/kg)"}] | [] | False |
| B3 | SUM(CASE WHEN profit_simple < 0 THEN 1 ELSE 0 END) | [] | [{"table": "sales_records", "column": "Unit price (yuan/kg)"}, {"table": "purchase_price", "column": "Wholesale price (yuan/kg)"}] | False |
| B3 | COUNT(*) | [] | [] | True |
| B3 | SUM(CASE WHEN profit_simple < 0 THEN 1 ELSE 0 END) | [] | [{"table": "sales_records", "column": "Unit price (yuan/kg)"}, {"table": "purchase_price", "column": "Wholesale price (yuan/kg)"}] | False |


## S58

类别 `data`；来源 `query_db`；调用 `e06e27558e6b4d7992be4e915e859c54`；状态 `success`。

```sql
WITH proc_items AS (
  SELECT DISTINCT s."Item Code"
  FROM sales_records s
  WHERE date(s."Sales Date") = '2023-06-30'
),
summer_analysis AS (
  SELECT s."Item Code",
    s."Unit price (yuan/kg)" as up,
    pp."Wholesale price (yuan/kg)" as wp,
    s."Unit price (yuan/kg)" - pp."Wholesale price (yuan/kg)" as profit_simple
  FROM sales_records s
  JOIN proc_items pi ON s."Item Code" = pi."Item Code"
  LEFT JOIN purchase_price pp ON s."Item Code" = pp."Item Code" AND date(s."Sales Date") = date(pp."Date")
  WHERE s."Sales type" = 'Sale'
    AND s."Sales Date" >= '2022-06-01' AND s."Sales Date" < '2022-09-01'
    AND pp."Wholesale price (yuan/kg)" IS NOT NULL
)
SELECT "Item Code", COUNT(*) as n, ROUND(AVG(profit_simple),3) as avg_profit_simple,
  ROUND(SUM(CASE WHEN profit_simple<0 THEN 1 ELSE 0 END)*100.0/COUNT(*),1) as pct_loss_simple
FROM summer_analysis
GROUP BY "Item Code"
HAVING "Item Code" IN (102900005118824, 102900011032732)
ORDER BY avg_profit_simple
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-025/attempt-01/sql/S58.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-025/attempt-01/sql/S58.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-025/attempt-01/results/S58.rows.jsonl)；完整：True；SHA256：`06e5b3637909d2e948c7e265e86cdbed181f850e96530bd513e51d3dfed8c158`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "s", "kind": "base", "block": null, "base_tables": ["sales_records"]}] | [] | [] |
| B2 | [{"alias": "s", "kind": "base", "block": null, "base_tables": ["sales_records"]}, {"alias": "pi", "kind": "derived", "block": "B1", "base_tables": ["sales_records"]}, {"alias": "pp", "kind": "base", "block": null, "base_tables": ["purchase_price"]}] | [{"type": "INNER", "right": "proc_items AS pi", "on": "s.\"Item Code\" = pi.\"Item Code\"", "using": []}, {"type": "LEFT", "right": "purchase_price AS pp", "on": "s.\"Item Code\" = pp.\"Item Code\" AND DATE(s.\"Sales Date\") = DATE(pp.\"Date\")", "using": []}] | [] |
| B3 | [{"alias": "summer_analysis", "kind": "derived", "block": "B2", "base_tables": ["purchase_price", "sales_records"]}] | [] | ["\"Item Code\""] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B3 | COUNT(*) | [] | [] | True |
| B3 | AVG(profit_simple) | [{"table": "sales_records", "column": "Unit price (yuan/kg)"}, {"table": "purchase_price", "column": "Wholesale price (yuan/kg)"}] | [] | False |
| B3 | COUNT(*) | [] | [] | True |
| B3 | SUM(CASE WHEN profit_simple < 0 THEN 1 ELSE 0 END) | [] | [{"table": "sales_records", "column": "Unit price (yuan/kg)"}, {"table": "purchase_price", "column": "Wholesale price (yuan/kg)"}] | False |


## S59

类别 `data`；来源 `query_db`；调用 `767aa61f52ce46efbf17a364a7e1738b`；状态 `success`。

```sql
SELECT "Date", "Wholesale price (yuan/kg)" FROM purchase_price
WHERE "Item Code" = 102900005118824 AND "Date" >= '2023-06-20' AND "Date" <= '2023-06-30'
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-025/attempt-01/sql/S59.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-025/attempt-01/sql/S59.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-025/attempt-01/results/S59.rows.jsonl)；完整：True；SHA256：`bd59ed33232e12efb6d324d10caddbcedcd427900ccf1c96f379850abef83f93`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "purchase_price", "kind": "base", "block": null, "base_tables": ["purchase_price"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |


## S60

类别 `data`；来源 `query_db`；调用 `df135b657eb342b6bcececbf621c1492`；状态 `success`。

```sql
SELECT "Date", "Wholesale price (yuan/kg)" FROM purchase_price
WHERE "Item Code" = 102900011032732 AND "Date" >= '2023-06-20' AND "Date" <= '2023-06-30'
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-025/attempt-01/sql/S60.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-025/attempt-01/sql/S60.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-025/attempt-01/results/S60.rows.jsonl)；完整：True；SHA256：`890670490d53a249691529c19f8d5b073ba6043ab7506e022e5659d269915372`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "purchase_price", "kind": "base", "block": null, "base_tables": ["purchase_price"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |


## S61

类别 `data`；来源 `query_db`；调用 `f15e324133d340f397d2498f52da2e7f`；状态 `success`。

```sql
SELECT date("Sales Date") as d, "Unit price (yuan/kg)", "Sales volume (kg)", "Whether sold at a discount"
FROM sales_records WHERE "Item Code" = 102900005118824 AND date("Sales Date") = '2023-06-30'
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-025/attempt-01/sql/S61.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-025/attempt-01/sql/S61.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-025/attempt-01/results/S61.rows.jsonl)；完整：True；SHA256：`24933657c51f97bcfb5aa35db7062801ae714268c4d727065b73cf1e3dd5a1d7`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "sales_records", "kind": "base", "block": null, "base_tables": ["sales_records"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |


## S62

类别 `data`；来源 `query_db`；调用 `24fd9df6fc15485fafb806b4ca2c91dc`；状态 `success`。

```sql
SELECT date("Sales Date") as d, "Unit price (yuan/kg)", "Sales volume (kg)", "Whether sold at a discount"
FROM sales_records WHERE "Item Code" = 102900011032732 AND date("Sales Date") = '2023-06-30'
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-025/attempt-01/sql/S62.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-025/attempt-01/sql/S62.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-025/attempt-01/results/S62.rows.jsonl)；完整：True；SHA256：`2a688028ec0f8efc3921b1a03cee689f6988d7706922ad7cb8cf69f5b1794433`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "sales_records", "kind": "base", "block": null, "base_tables": ["sales_records"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |


## S63

类别 `data`；来源 `query_db`；调用 `186a06d721b54dc4af51f555df7f5c0b`；状态 `success`。

```sql
WITH summer_analysis AS (
  SELECT s."Item Code",
    strftime('%Y-%m', s."Sales Date") as ym,
    s."Sales volume (kg)" as vol,
    s."Unit price (yuan/kg)" as up,
    pp."Wholesale price (yuan/kg)" as wp,
    pl."Loss Rate (%)" as lr,
    s."Unit price (yuan/kg)" - pp."Wholesale price (yuan/kg)"/(1.0-pl."Loss Rate (%)"/100.0) as profit
  FROM sales_records s
  LEFT JOIN purchase_price pp ON s."Item Code" = pp."Item Code" AND date(s."Sales Date") = date(pp."Date")
  LEFT JOIN product_loss pl ON s."Item Code" = pl."Item Code"
  WHERE s."Item Code" IN (102900005118824, 102900011032732)
    AND s."Sales type" = 'Sale'
    AND s."Sales Date" >= '2022-06-01' AND s."Sales Date" < '2022-09-01'
    AND pp."Wholesale price (yuan/kg)" IS NOT NULL
    AND pl."Loss Rate (%)" IS NOT NULL
)
SELECT "Item Code", ym, COUNT(*) as n, ROUND(AVG(profit),3) as avg_profit,
  ROUND(AVG(up),2) as avg_up, ROUND(AVG(wp/(1.0-lr/100.0)),2) as avg_cost,
  ROUND(SUM(CASE WHEN profit<0 THEN 1 ELSE 0 END)*100.0/COUNT(*),1) as pct_loss
FROM summer_analysis
GROUP BY "Item Code", ym
ORDER BY "Item Code", ym
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-025/attempt-01/sql/S63.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-025/attempt-01/sql/S63.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-025/attempt-01/results/S63.rows.jsonl)；完整：True；SHA256：`f9efe4a09ba21529b9da2824f6e68de6d5bacc2795eea7bce477735431698430`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "s", "kind": "base", "block": null, "base_tables": ["sales_records"]}, {"alias": "pp", "kind": "base", "block": null, "base_tables": ["purchase_price"]}, {"alias": "pl", "kind": "base", "block": null, "base_tables": ["product_loss"]}] | [{"type": "LEFT", "right": "purchase_price AS pp", "on": "s.\"Item Code\" = pp.\"Item Code\" AND DATE(s.\"Sales Date\") = DATE(pp.\"Date\")", "using": []}, {"type": "LEFT", "right": "product_loss AS pl", "on": "s.\"Item Code\" = pl.\"Item Code\"", "using": []}] | [] |
| B2 | [{"alias": "summer_analysis", "kind": "derived", "block": "B1", "base_tables": ["product_loss", "purchase_price", "sales_records"]}] | [] | ["\"Item Code\"", "ym"] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B2 | COUNT(*) | [] | [] | True |
| B2 | AVG(profit) | [{"table": "sales_records", "column": "Unit price (yuan/kg)"}, {"table": "purchase_price", "column": "Wholesale price (yuan/kg)"}, {"table": "product_loss", "column": "Loss Rate (%)"}] | [] | False |
| B2 | AVG(up) | [{"table": "sales_records", "column": "Unit price (yuan/kg)"}] | [] | False |
| B2 | AVG(wp / (1.0 - lr / 100.0)) | [{"table": "purchase_price", "column": "Wholesale price (yuan/kg)"}, {"table": "product_loss", "column": "Loss Rate (%)"}] | [] | False |
| B2 | COUNT(*) | [] | [] | True |
| B2 | SUM(CASE WHEN profit < 0 THEN 1 ELSE 0 END) | [] | [{"table": "sales_records", "column": "Unit price (yuan/kg)"}, {"table": "purchase_price", "column": "Wholesale price (yuan/kg)"}, {"table": "product_loss", "column": "Loss Rate (%)"}] | False |


## S64

类别 `data`；来源 `query_db`；调用 `4ae92327301a4fa2840804f0ed9e9259`；状态 `success`。

```sql
WITH proc_items AS (
  SELECT DISTINCT s."Item Code"
  FROM sales_records s
  WHERE date(s."Sales Date") = '2023-06-30'
),
summer_analysis AS (
  SELECT s."Item Code",
    strftime('%m', s."Sales Date") as mo,
    s."Sales volume (kg)" as vol,
    s."Unit price (yuan/kg)" as up,
    pp."Wholesale price (yuan/kg)" as wp,
    pl."Loss Rate (%)" as lr,
    s."Unit price (yuan/kg)" - pp."Wholesale price (yuan/kg)"/(1.0-pl."Loss Rate (%)"/100.0) as profit
  FROM sales_records s
  JOIN proc_items pi ON s."Item Code" = pi."Item Code"
  LEFT JOIN purchase_price pp ON s."Item Code" = pp."Item Code" AND date(s."Sales Date") = date(pp."Date")
  LEFT JOIN product_loss pl ON s."Item Code" = pl."Item Code"
  WHERE s."Sales type" = 'Sale'
    AND s."Sales Date" >= '2022-07-01' AND s."Sales Date" < '2022-09-01'
    AND pp."Wholesale price (yuan/kg)" IS NOT NULL
    AND pl."Loss Rate (%)" IS NOT NULL
)
SELECT "Item Code", mo, COUNT(*) as n,
  ROUND(AVG(profit),3) as avg_profit,
  ROUND(SUM(CASE WHEN profit<0 THEN 1 ELSE 0 END)*100.0/COUNT(*),1) as pct_loss
FROM summer_analysis
GROUP BY "Item Code", mo
HAVING n >= 20
ORDER BY avg_profit ASC
LIMIT 20
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-025/attempt-01/sql/S64.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-025/attempt-01/sql/S64.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-025/attempt-01/results/S64.rows.jsonl)；完整：True；SHA256：`7643ecd633ed82aff52f4a7362e0ffc6de5aa1c839c25ddb4aada3e10dff4516`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "s", "kind": "base", "block": null, "base_tables": ["sales_records"]}] | [] | [] |
| B2 | [{"alias": "s", "kind": "base", "block": null, "base_tables": ["sales_records"]}, {"alias": "pi", "kind": "derived", "block": "B1", "base_tables": ["sales_records"]}, {"alias": "pp", "kind": "base", "block": null, "base_tables": ["purchase_price"]}, {"alias": "pl", "kind": "base", "block": null, "base_tables": ["product_loss"]}] | [{"type": "INNER", "right": "proc_items AS pi", "on": "s.\"Item Code\" = pi.\"Item Code\"", "using": []}, {"type": "LEFT", "right": "purchase_price AS pp", "on": "s.\"Item Code\" = pp.\"Item Code\" AND DATE(s.\"Sales Date\") = DATE(pp.\"Date\")", "using": []}, {"type": "LEFT", "right": "product_loss AS pl", "on": "s.\"Item Code\" = pl.\"Item Code\"", "using": []}] | [] |
| B3 | [{"alias": "summer_analysis", "kind": "derived", "block": "B2", "base_tables": ["product_loss", "purchase_price", "sales_records"]}] | [] | ["\"Item Code\"", "mo"] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B3 | COUNT(*) | [] | [] | True |
| B3 | AVG(profit) | [{"table": "sales_records", "column": "Unit price (yuan/kg)"}, {"table": "purchase_price", "column": "Wholesale price (yuan/kg)"}, {"table": "product_loss", "column": "Loss Rate (%)"}] | [] | False |
| B3 | COUNT(*) | [] | [] | True |
| B3 | SUM(CASE WHEN profit < 0 THEN 1 ELSE 0 END) | [] | [{"table": "sales_records", "column": "Unit price (yuan/kg)"}, {"table": "purchase_price", "column": "Wholesale price (yuan/kg)"}, {"table": "product_loss", "column": "Loss Rate (%)"}] | False |


## S65

类别 `data`；来源 `python`；调用 `1da3017914574a2f86fc9272623e52e3`；状态 `success`。

```sql

WITH proc_items AS (
  SELECT s."Item Code", SUM(s."Sales volume (kg)") as vol_0630
  FROM sales_records s
  WHERE date(s."Sales Date") = '2023-06-30' AND s."Sales type" = 'Sale'
  GROUP BY s."Item Code"
),
summer_sales AS (
  SELECT s."Item Code",
    s."Sales volume (kg)" as vol,
    s."Unit price (yuan/kg)" as up,
    pp."Wholesale price (yuan/kg)" as wp,
    pl."Loss Rate (%)" as lr,
    strftime('%Y', s."Sales Date") as yr,
    s."Unit price (yuan/kg)" - pp."Wholesale price (yuan/kg)"/(1.0-pl."Loss Rate (%)"/100.0) as profit
  FROM sales_records s
  JOIN proc_items pi ON s."Item Code" = pi."Item Code"
  LEFT JOIN purchase_price pp ON s."Item Code" = pp."Item Code" AND date(s."Sales Date") = date(pp."Date")
  LEFT JOIN product_loss pl ON s."Item Code" = pl."Item Code"
  WHERE s."Sales type" = 'Sale'
    AND (
      (s."Sales Date" >= '2020-07-01' AND s."Sales Date" < '2020-09-01')
      OR (s."Sales Date" >= '2021-06-01' AND s."Sales Date" < '2021-09-01')
      OR (s."Sales Date" >= '2022-06-01' AND s."Sales Date" < '2022-09-01')
    )
    AND pp."Wholesale price (yuan/kg)" IS NOT NULL
    AND pl."Loss Rate (%)" IS NOT NULL
),
y2022 AS (
  SELECT "Item Code", COUNT(*) n22, AVG(profit) avgp22,
    SUM(CASE WHEN profit<0 THEN 1 ELSE 0 END)*100.0/COUNT(*) pct22,
    SUM(vol*profit) tot22
  FROM summer_sales WHERE yr='2022' GROUP BY "Item Code"
),
allsum AS (
  SELECT "Item Code", COUNT(*) n_all, AVG(profit) avgp_all,
    SUM(CASE WHEN profit<0 THEN 1 ELSE 0 END)*100.0/COUNT(*) pct_all,
    SUM(vol*profit) tot_all
  FROM summer_sales GROUP BY "Item Code"
)
SELECT pi."Item Code", p."Item Name", ROUND(pi.vol_0630,2) vol_0630,
  y.n22, ROUND(y.avgp22,3) avgp22, ROUND(y.pct22,1) pct22, ROUND(y.tot22,2) tot22,
  a.n_all, ROUND(a.avgp_all,3) avgp_all, ROUND(a.pct_all,1) pct_all, ROUND(a.tot_all,2) tot_all,
  ROUND(pl."Loss Rate (%)",2) loss_rate
FROM proc_items pi
LEFT JOIN product_information p ON pi."Item Code" = p."Item Code"
LEFT JOIN y2022 y ON pi."Item Code" = y."Item Code"
LEFT JOIN allsum a ON pi."Item Code" = a."Item Code"
LEFT JOIN product_loss pl ON pi."Item Code" = pl."Item Code"
ORDER BY COALESCE(y.avgp22, 999) ASC, COALESCE(a.avgp_all, 999) ASC

```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-025/attempt-01/sql/S65.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-025/attempt-01/sql/S65.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-025/attempt-01/results/S65.rows.jsonl)；完整：True；SHA256：`29725e190ddfb9441575b9eeb95ad6b3dffbe7ed96cb990c0bf4e10d7cafee39`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "s", "kind": "base", "block": null, "base_tables": ["sales_records"]}] | [] | ["s.\"Item Code\""] |
| B2 | [{"alias": "s", "kind": "base", "block": null, "base_tables": ["sales_records"]}, {"alias": "pi", "kind": "derived", "block": "B1", "base_tables": ["sales_records"]}, {"alias": "pp", "kind": "base", "block": null, "base_tables": ["purchase_price"]}, {"alias": "pl", "kind": "base", "block": null, "base_tables": ["product_loss"]}] | [{"type": "INNER", "right": "proc_items AS pi", "on": "s.\"Item Code\" = pi.\"Item Code\"", "using": []}, {"type": "LEFT", "right": "purchase_price AS pp", "on": "s.\"Item Code\" = pp.\"Item Code\" AND DATE(s.\"Sales Date\") = DATE(pp.\"Date\")", "using": []}, {"type": "LEFT", "right": "product_loss AS pl", "on": "s.\"Item Code\" = pl.\"Item Code\"", "using": []}] | [] |
| B3 | [{"alias": "summer_sales", "kind": "derived", "block": "B2", "base_tables": ["product_loss", "purchase_price", "sales_records"]}] | [] | ["\"Item Code\""] |
| B4 | [{"alias": "summer_sales", "kind": "derived", "block": "B2", "base_tables": ["product_loss", "purchase_price", "sales_records"]}] | [] | ["\"Item Code\""] |
| B5 | [{"alias": "pi", "kind": "derived", "block": "B1", "base_tables": ["sales_records"]}, {"alias": "p", "kind": "base", "block": null, "base_tables": ["product_information"]}, {"alias": "y", "kind": "derived", "block": "B3", "base_tables": ["product_loss", "purchase_price", "sales_records"]}, {"alias": "a", "kind": "derived", "block": "B4", "base_tables": ["product_loss", "purchase_price", "sales_records"]}, {"alias": "pl", "kind": "base", "block": null, "base_tables": ["product_loss"]}] | [{"type": "LEFT", "right": "product_information AS p", "on": "pi.\"Item Code\" = p.\"Item Code\"", "using": []}, {"type": "LEFT", "right": "y2022 AS y", "on": "pi.\"Item Code\" = y.\"Item Code\"", "using": []}, {"type": "LEFT", "right": "allsum AS a", "on": "pi.\"Item Code\" = a.\"Item Code\"", "using": []}, {"type": "LEFT", "right": "product_loss AS pl", "on": "pi.\"Item Code\" = pl.\"Item Code\"", "using": []}] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | SUM(s."Sales volume (kg)") | [{"table": "sales_records", "column": "Sales volume (kg)"}] | [] | False |
| B3 | COUNT(*) | [] | [] | True |
| B3 | AVG(profit) | [{"table": "sales_records", "column": "Unit price (yuan/kg)"}, {"table": "purchase_price", "column": "Wholesale price (yuan/kg)"}, {"table": "product_loss", "column": "Loss Rate (%)"}] | [] | False |
| B3 | SUM(vol * profit) | [{"table": "sales_records", "column": "Sales volume (kg)"}, {"table": "sales_records", "column": "Unit price (yuan/kg)"}, {"table": "purchase_price", "column": "Wholesale price (yuan/kg)"}, {"table": "product_loss", "column": "Loss Rate (%)"}] | [] | False |
| B3 | COUNT(*) | [] | [] | True |
| B3 | SUM(CASE WHEN profit < 0 THEN 1 ELSE 0 END) | [] | [{"table": "sales_records", "column": "Unit price (yuan/kg)"}, {"table": "purchase_price", "column": "Wholesale price (yuan/kg)"}, {"table": "product_loss", "column": "Loss Rate (%)"}] | False |
| B4 | COUNT(*) | [] | [] | True |
| B4 | AVG(profit) | [{"table": "sales_records", "column": "Unit price (yuan/kg)"}, {"table": "purchase_price", "column": "Wholesale price (yuan/kg)"}, {"table": "product_loss", "column": "Loss Rate (%)"}] | [] | False |
| B4 | SUM(vol * profit) | [{"table": "sales_records", "column": "Sales volume (kg)"}, {"table": "sales_records", "column": "Unit price (yuan/kg)"}, {"table": "purchase_price", "column": "Wholesale price (yuan/kg)"}, {"table": "product_loss", "column": "Loss Rate (%)"}] | [] | False |
| B4 | COUNT(*) | [] | [] | True |
| B4 | SUM(CASE WHEN profit < 0 THEN 1 ELSE 0 END) | [] | [{"table": "sales_records", "column": "Unit price (yuan/kg)"}, {"table": "purchase_price", "column": "Wholesale price (yuan/kg)"}, {"table": "product_loss", "column": "Loss Rate (%)"}] | False |


## S66

类别 `data`；来源 `python`；调用 `946940d3071c49aeacc93393309552d5`；状态 `success`。

```sql

WITH proc_items AS (
  SELECT s."Item Code", SUM(s."Sales volume (kg)") as vol_0630
  FROM sales_records s
  WHERE date(s."Sales Date") = '2023-06-30' AND s."Sales type" = 'Sale'
  GROUP BY s."Item Code"
),
summer_sales AS (
  SELECT s."Item Code",
    s."Sales volume (kg)" as vol,
    s."Unit price (yuan/kg)" as up,
    pp."Wholesale price (yuan/kg)" as wp,
    pl."Loss Rate (%)" as lr,
    strftime('%Y', s."Sales Date") as yr,
    s."Unit price (yuan/kg)" - pp."Wholesale price (yuan/kg)"/(1.0-pl."Loss Rate (%)"/100.0) as profit
  FROM sales_records s
  JOIN proc_items pi ON s."Item Code" = pi."Item Code"
  LEFT JOIN purchase_price pp ON s."Item Code" = pp."Item Code" AND date(s."Sales Date") = date(pp."Date")
  LEFT JOIN product_loss pl ON s."Item Code" = pl."Item Code"
  WHERE s."Sales type" = 'Sale'
    AND (
      (s."Sales Date" >= '2020-07-01' AND s."Sales Date" < '2020-09-01')
      OR (s."Sales Date" >= '2021-06-01' AND s."Sales Date" < '2021-09-01')
      OR (s."Sales Date" >= '2022-06-01' AND s."Sales Date" < '2022-09-01')
    )
    AND pp."Wholesale price (yuan/kg)" IS NOT NULL
    AND pl."Loss Rate (%)" IS NOT NULL
),
y2022 AS (
  SELECT "Item Code", COUNT(*) n22, AVG(profit) avgp22,
    SUM(CASE WHEN profit<0 THEN 1 ELSE 0 END)*100.0/COUNT(*) pct22,
    SUM(vol*profit) tot22
  FROM summer_sales WHERE yr='2022' GROUP BY "Item Code"
),
allsum AS (
  SELECT "Item Code", COUNT(*) n_all, AVG(profit) avgp_all,
    SUM(CASE WHEN profit<0 THEN 1 ELSE 0 END)*100.0/COUNT(*) pct_all,
    SUM(vol*profit) tot_all
  FROM summer_sales GROUP BY "Item Code"
)
SELECT pi."Item Code", p."Item Name", ROUND(pi.vol_0630,2) vol_0630,
  y.n22, ROUND(y.avgp22,3) avgp22, ROUND(y.pct22,1) pct22, ROUND(y.tot22,2) tot22,
  a.n_all, ROUND(a.avgp_all,3) avgp_all, ROUND(a.pct_all,1) pct_all, ROUND(a.tot_all,2) tot_all,
  ROUND(pl."Loss Rate (%)",2) loss_rate
FROM proc_items pi
LEFT JOIN product_information p ON pi."Item Code" = p."Item Code"
LEFT JOIN y2022 y ON pi."Item Code" = y."Item Code"
LEFT JOIN allsum a ON pi."Item Code" = a."Item Code"
LEFT JOIN product_loss pl ON pi."Item Code" = pl."Item Code"
ORDER BY COALESCE(y.avgp22, 999) ASC, COALESCE(a.avgp_all, 999) ASC

```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-025/attempt-01/sql/S66.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-025/attempt-01/sql/S66.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-025/attempt-01/results/S66.rows.jsonl)；完整：True；SHA256：`29725e190ddfb9441575b9eeb95ad6b3dffbe7ed96cb990c0bf4e10d7cafee39`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "s", "kind": "base", "block": null, "base_tables": ["sales_records"]}] | [] | ["s.\"Item Code\""] |
| B2 | [{"alias": "s", "kind": "base", "block": null, "base_tables": ["sales_records"]}, {"alias": "pi", "kind": "derived", "block": "B1", "base_tables": ["sales_records"]}, {"alias": "pp", "kind": "base", "block": null, "base_tables": ["purchase_price"]}, {"alias": "pl", "kind": "base", "block": null, "base_tables": ["product_loss"]}] | [{"type": "INNER", "right": "proc_items AS pi", "on": "s.\"Item Code\" = pi.\"Item Code\"", "using": []}, {"type": "LEFT", "right": "purchase_price AS pp", "on": "s.\"Item Code\" = pp.\"Item Code\" AND DATE(s.\"Sales Date\") = DATE(pp.\"Date\")", "using": []}, {"type": "LEFT", "right": "product_loss AS pl", "on": "s.\"Item Code\" = pl.\"Item Code\"", "using": []}] | [] |
| B3 | [{"alias": "summer_sales", "kind": "derived", "block": "B2", "base_tables": ["product_loss", "purchase_price", "sales_records"]}] | [] | ["\"Item Code\""] |
| B4 | [{"alias": "summer_sales", "kind": "derived", "block": "B2", "base_tables": ["product_loss", "purchase_price", "sales_records"]}] | [] | ["\"Item Code\""] |
| B5 | [{"alias": "pi", "kind": "derived", "block": "B1", "base_tables": ["sales_records"]}, {"alias": "p", "kind": "base", "block": null, "base_tables": ["product_information"]}, {"alias": "y", "kind": "derived", "block": "B3", "base_tables": ["product_loss", "purchase_price", "sales_records"]}, {"alias": "a", "kind": "derived", "block": "B4", "base_tables": ["product_loss", "purchase_price", "sales_records"]}, {"alias": "pl", "kind": "base", "block": null, "base_tables": ["product_loss"]}] | [{"type": "LEFT", "right": "product_information AS p", "on": "pi.\"Item Code\" = p.\"Item Code\"", "using": []}, {"type": "LEFT", "right": "y2022 AS y", "on": "pi.\"Item Code\" = y.\"Item Code\"", "using": []}, {"type": "LEFT", "right": "allsum AS a", "on": "pi.\"Item Code\" = a.\"Item Code\"", "using": []}, {"type": "LEFT", "right": "product_loss AS pl", "on": "pi.\"Item Code\" = pl.\"Item Code\"", "using": []}] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | SUM(s."Sales volume (kg)") | [{"table": "sales_records", "column": "Sales volume (kg)"}] | [] | False |
| B3 | COUNT(*) | [] | [] | True |
| B3 | AVG(profit) | [{"table": "sales_records", "column": "Unit price (yuan/kg)"}, {"table": "purchase_price", "column": "Wholesale price (yuan/kg)"}, {"table": "product_loss", "column": "Loss Rate (%)"}] | [] | False |
| B3 | SUM(vol * profit) | [{"table": "sales_records", "column": "Sales volume (kg)"}, {"table": "sales_records", "column": "Unit price (yuan/kg)"}, {"table": "purchase_price", "column": "Wholesale price (yuan/kg)"}, {"table": "product_loss", "column": "Loss Rate (%)"}] | [] | False |
| B3 | COUNT(*) | [] | [] | True |
| B3 | SUM(CASE WHEN profit < 0 THEN 1 ELSE 0 END) | [] | [{"table": "sales_records", "column": "Unit price (yuan/kg)"}, {"table": "purchase_price", "column": "Wholesale price (yuan/kg)"}, {"table": "product_loss", "column": "Loss Rate (%)"}] | False |
| B4 | COUNT(*) | [] | [] | True |
| B4 | AVG(profit) | [{"table": "sales_records", "column": "Unit price (yuan/kg)"}, {"table": "purchase_price", "column": "Wholesale price (yuan/kg)"}, {"table": "product_loss", "column": "Loss Rate (%)"}] | [] | False |
| B4 | SUM(vol * profit) | [{"table": "sales_records", "column": "Sales volume (kg)"}, {"table": "sales_records", "column": "Unit price (yuan/kg)"}, {"table": "purchase_price", "column": "Wholesale price (yuan/kg)"}, {"table": "product_loss", "column": "Loss Rate (%)"}] | [] | False |
| B4 | COUNT(*) | [] | [] | True |
| B4 | SUM(CASE WHEN profit < 0 THEN 1 ELSE 0 END) | [] | [{"table": "sales_records", "column": "Unit price (yuan/kg)"}, {"table": "purchase_price", "column": "Wholesale price (yuan/kg)"}, {"table": "product_loss", "column": "Loss Rate (%)"}] | False |


## S67

类别 `data`；来源 `python`；调用 `7821fb4113bc4172b102c636e4a5ffa3`；状态 `success`。

```sql

WITH proc_items AS (
  SELECT s."Item Code", SUM(s."Sales volume (kg)") as vol_0630
  FROM sales_records s
  WHERE date(s."Sales Date") = '2023-06-30' AND s."Sales type" = 'Sale'
  GROUP BY s."Item Code"
),
summer_sales AS (
  SELECT s."Item Code",
    s."Sales volume (kg)" as vol,
    s."Unit price (yuan/kg)" as up,
    pp."Wholesale price (yuan/kg)" as wp,
    pl."Loss Rate (%)" as lr,
    strftime('%Y', s."Sales Date") as yr,
    s."Unit price (yuan/kg)" - pp."Wholesale price (yuan/kg)"/(1.0-pl."Loss Rate (%)"/100.0) as profit
  FROM sales_records s
  JOIN proc_items pi ON s."Item Code" = pi."Item Code"
  LEFT JOIN purchase_price pp ON s."Item Code" = pp."Item Code" AND date(s."Sales Date") = date(pp."Date")
  LEFT JOIN product_loss pl ON s."Item Code" = pl."Item Code"
  WHERE s."Sales type" = 'Sale'
    AND (
      (s."Sales Date" >= '2020-07-01' AND s."Sales Date" < '2020-09-01')
      OR (s."Sales Date" >= '2021-06-01' AND s."Sales Date" < '2021-09-01')
      OR (s."Sales Date" >= '2022-06-01' AND s."Sales Date" < '2022-09-01')
    )
    AND pp."Wholesale price (yuan/kg)" IS NOT NULL
    AND pl."Loss Rate (%)" IS NOT NULL
),
y2022 AS (
  SELECT "Item Code", COUNT(*) n22, AVG(profit) avgp22,
    SUM(CASE WHEN profit<0 THEN 1 ELSE 0 END)*100.0/COUNT(*) pct22,
    SUM(vol*profit) tot22
  FROM summer_sales WHERE yr='2022' GROUP BY "Item Code"
)
SELECT pi."Item Code", p."Item Name", ROUND(pi.vol_0630,2) vol_0630,
  y.n22, ROUND(y.avgp22,3) avgp22, ROUND(y.pct22,1) pct22, ROUND(y.tot22,2) tot22
FROM proc_items pi
LEFT JOIN product_information p ON pi."Item Code" = p."Item Code"
LEFT JOIN y2022 y ON pi."Item Code" = y."Item Code"
ORDER BY COALESCE(y.avgp22, 999) ASC

```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-025/attempt-01/sql/S67.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-025/attempt-01/sql/S67.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-025/attempt-01/results/S67.rows.jsonl)；完整：True；SHA256：`1e3e5022cac77544ff79fe7e09139f3f9f4e2e5abe0999d35956b048c22e353e`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "s", "kind": "base", "block": null, "base_tables": ["sales_records"]}] | [] | ["s.\"Item Code\""] |
| B2 | [{"alias": "s", "kind": "base", "block": null, "base_tables": ["sales_records"]}, {"alias": "pi", "kind": "derived", "block": "B1", "base_tables": ["sales_records"]}, {"alias": "pp", "kind": "base", "block": null, "base_tables": ["purchase_price"]}, {"alias": "pl", "kind": "base", "block": null, "base_tables": ["product_loss"]}] | [{"type": "INNER", "right": "proc_items AS pi", "on": "s.\"Item Code\" = pi.\"Item Code\"", "using": []}, {"type": "LEFT", "right": "purchase_price AS pp", "on": "s.\"Item Code\" = pp.\"Item Code\" AND DATE(s.\"Sales Date\") = DATE(pp.\"Date\")", "using": []}, {"type": "LEFT", "right": "product_loss AS pl", "on": "s.\"Item Code\" = pl.\"Item Code\"", "using": []}] | [] |
| B3 | [{"alias": "summer_sales", "kind": "derived", "block": "B2", "base_tables": ["product_loss", "purchase_price", "sales_records"]}] | [] | ["\"Item Code\""] |
| B4 | [{"alias": "pi", "kind": "derived", "block": "B1", "base_tables": ["sales_records"]}, {"alias": "p", "kind": "base", "block": null, "base_tables": ["product_information"]}, {"alias": "y", "kind": "derived", "block": "B3", "base_tables": ["product_loss", "purchase_price", "sales_records"]}] | [{"type": "LEFT", "right": "product_information AS p", "on": "pi.\"Item Code\" = p.\"Item Code\"", "using": []}, {"type": "LEFT", "right": "y2022 AS y", "on": "pi.\"Item Code\" = y.\"Item Code\"", "using": []}] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | SUM(s."Sales volume (kg)") | [{"table": "sales_records", "column": "Sales volume (kg)"}] | [] | False |
| B3 | COUNT(*) | [] | [] | True |
| B3 | AVG(profit) | [{"table": "sales_records", "column": "Unit price (yuan/kg)"}, {"table": "purchase_price", "column": "Wholesale price (yuan/kg)"}, {"table": "product_loss", "column": "Loss Rate (%)"}] | [] | False |
| B3 | SUM(vol * profit) | [{"table": "sales_records", "column": "Sales volume (kg)"}, {"table": "sales_records", "column": "Unit price (yuan/kg)"}, {"table": "purchase_price", "column": "Wholesale price (yuan/kg)"}, {"table": "product_loss", "column": "Loss Rate (%)"}] | [] | False |
| B3 | COUNT(*) | [] | [] | True |
| B3 | SUM(CASE WHEN profit < 0 THEN 1 ELSE 0 END) | [] | [{"table": "sales_records", "column": "Unit price (yuan/kg)"}, {"table": "purchase_price", "column": "Wholesale price (yuan/kg)"}, {"table": "product_loss", "column": "Loss Rate (%)"}] | False |


## S68

类别 `data`；来源 `python`；调用 `e299a84d3dcb4cc392b6593eab42a423`；状态 `success`。

```sql

WITH proc_items AS (
  SELECT s."Item Code", SUM(s."Sales volume (kg)") as vol_0630
  FROM sales_records s
  WHERE date(s."Sales Date") = '2023-06-30' AND s."Sales type" = 'Sale'
  GROUP BY s."Item Code"
),
summer_sales AS (
  SELECT s."Item Code",
    s."Sales volume (kg)" as vol,
    s."Unit price (yuan/kg)" as up,
    pp."Wholesale price (yuan/kg)" as wp,
    pl."Loss Rate (%)" as lr,
    strftime('%Y', s."Sales Date") as yr,
    s."Unit price (yuan/kg)" - pp."Wholesale price (yuan/kg)"/(1.0-pl."Loss Rate (%)"/100.0) as profit
  FROM sales_records s
  JOIN proc_items pi ON s."Item Code" = pi."Item Code"
  LEFT JOIN purchase_price pp ON s."Item Code" = pp."Item Code" AND date(s."Sales Date") = date(pp."Date")
  LEFT JOIN product_loss pl ON s."Item Code" = pl."Item Code"
  WHERE s."Sales type" = 'Sale'
    AND (
      (s."Sales Date" >= '2020-07-01' AND s."Sales Date" < '2020-09-01')
      OR (s."Sales Date" >= '2021-06-01' AND s."Sales Date" < '2021-09-01')
      OR (s."Sales Date" >= '2022-06-01' AND s."Sales Date" < '2022-09-01')
    )
    AND pp."Wholesale price (yuan/kg)" IS NOT NULL
    AND pl."Loss Rate (%)" IS NOT NULL
),
y2022 AS (
  SELECT "Item Code", COUNT(*) n22, AVG(profit) avgp22,
    SUM(CASE WHEN profit<0 THEN 1 ELSE 0 END)*100.0/COUNT(*) pct22,
    SUM(vol*profit) tot22
  FROM summer_sales WHERE yr='2022' GROUP BY "Item Code"
)
SELECT pi."Item Code", p."Item Name", ROUND(pi.vol_0630,2) vol_0630,
  y.n22, ROUND(y.avgp22,3) avgp22, ROUND(y.pct22,1) pct22, ROUND(y.tot22,2) tot22
FROM proc_items pi
LEFT JOIN product_information p ON pi."Item Code" = p."Item Code"
LEFT JOIN y2022 y ON pi."Item Code" = y."Item Code"
ORDER BY COALESCE(y.avgp22, 999) ASC

```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-025/attempt-01/sql/S68.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-025/attempt-01/sql/S68.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-025/attempt-01/results/S68.rows.jsonl)；完整：True；SHA256：`1e3e5022cac77544ff79fe7e09139f3f9f4e2e5abe0999d35956b048c22e353e`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "s", "kind": "base", "block": null, "base_tables": ["sales_records"]}] | [] | ["s.\"Item Code\""] |
| B2 | [{"alias": "s", "kind": "base", "block": null, "base_tables": ["sales_records"]}, {"alias": "pi", "kind": "derived", "block": "B1", "base_tables": ["sales_records"]}, {"alias": "pp", "kind": "base", "block": null, "base_tables": ["purchase_price"]}, {"alias": "pl", "kind": "base", "block": null, "base_tables": ["product_loss"]}] | [{"type": "INNER", "right": "proc_items AS pi", "on": "s.\"Item Code\" = pi.\"Item Code\"", "using": []}, {"type": "LEFT", "right": "purchase_price AS pp", "on": "s.\"Item Code\" = pp.\"Item Code\" AND DATE(s.\"Sales Date\") = DATE(pp.\"Date\")", "using": []}, {"type": "LEFT", "right": "product_loss AS pl", "on": "s.\"Item Code\" = pl.\"Item Code\"", "using": []}] | [] |
| B3 | [{"alias": "summer_sales", "kind": "derived", "block": "B2", "base_tables": ["product_loss", "purchase_price", "sales_records"]}] | [] | ["\"Item Code\""] |
| B4 | [{"alias": "pi", "kind": "derived", "block": "B1", "base_tables": ["sales_records"]}, {"alias": "p", "kind": "base", "block": null, "base_tables": ["product_information"]}, {"alias": "y", "kind": "derived", "block": "B3", "base_tables": ["product_loss", "purchase_price", "sales_records"]}] | [{"type": "LEFT", "right": "product_information AS p", "on": "pi.\"Item Code\" = p.\"Item Code\"", "using": []}, {"type": "LEFT", "right": "y2022 AS y", "on": "pi.\"Item Code\" = y.\"Item Code\"", "using": []}] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | SUM(s."Sales volume (kg)") | [{"table": "sales_records", "column": "Sales volume (kg)"}] | [] | False |
| B3 | COUNT(*) | [] | [] | True |
| B3 | AVG(profit) | [{"table": "sales_records", "column": "Unit price (yuan/kg)"}, {"table": "purchase_price", "column": "Wholesale price (yuan/kg)"}, {"table": "product_loss", "column": "Loss Rate (%)"}] | [] | False |
| B3 | SUM(vol * profit) | [{"table": "sales_records", "column": "Sales volume (kg)"}, {"table": "sales_records", "column": "Unit price (yuan/kg)"}, {"table": "purchase_price", "column": "Wholesale price (yuan/kg)"}, {"table": "product_loss", "column": "Loss Rate (%)"}] | [] | False |
| B3 | COUNT(*) | [] | [] | True |
| B3 | SUM(CASE WHEN profit < 0 THEN 1 ELSE 0 END) | [] | [{"table": "sales_records", "column": "Unit price (yuan/kg)"}, {"table": "purchase_price", "column": "Wholesale price (yuan/kg)"}, {"table": "product_loss", "column": "Loss Rate (%)"}] | False |


## S69

类别 `data`；来源 `query_db`；调用 `dd3f4377a37a4ddc93247f2a819cd01f`；状态 `failed`。

```sql
WITH last_price AS (
  SELECT pp."Item Code", pp."Wholesale price (yuan/kg)" as wp
  FROM purchase_price pp
  WHERE pp."Date" = (SELECT MAX(pp2."Date") FROM purchase_price pp2 WHERE pp2."Item Code" = pp."Item Code")
),
day_sales AS (
  SELECT s."Item Code",
    SUM(s."Sales volume (kg)") as vol,
    AVG(s."Unit price (yuan/kg)") as avg_up
  FROM sales_records s
  WHERE date(s."Sales Date") = '2023-06-30' AND s."Sales type" = 'Sale'
  GROUP BY s."Item Code"
)
SELECT ds."Item Code", p."Item Name",
  ROUND(ds.vol,2) as proc_vol_kg,
  ROUND(lp.wp,2) as last_wholesale,
  ROUND(pl."Loss Rate (%)",2) as loss_rate,
  ROUND(lp.wp/(1.0-pl."Loss Rate (%)"/100.0),2) as eff_cost,
  ROUND(ds.avg_up,2) as avg_sell_price,
  ROUND(ds.vol * (ds.avg_up - lp.wp/(1.0-pl."Loss Rate (%)"/100.0)),2) as expected_pnl_0701
FROM day_sales ds
LEFT JOIN purchase_price lp ON ds."Item Code" = lp."Item Code"
LEFT JOIN product_information p ON ds."Item Code" = p."Item Code"
LEFT JOIN product_loss pl ON ds."Item Code" = pl."Item Code"
WHERE lp.wp IS NOT NULL
ORDER BY expected_pnl_0701 ASC
LIMIT 10
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-025/attempt-01/sql/S69.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-025/attempt-01/sql/S69.parameters.json)。

错误：`OperationalError('no such column: lp.wp')`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "pp2", "kind": "base", "block": null, "base_tables": ["purchase_price"]}] | [] | [] |
| B2 | [{"alias": "pp", "kind": "base", "block": null, "base_tables": ["purchase_price"]}] | [] | [] |
| B3 | [{"alias": "s", "kind": "base", "block": null, "base_tables": ["sales_records"]}] | [] | ["s.\"Item Code\""] |
| B4 | [{"alias": "ds", "kind": "derived", "block": "B3", "base_tables": ["sales_records"]}, {"alias": "lp", "kind": "base", "block": null, "base_tables": ["purchase_price"]}, {"alias": "p", "kind": "base", "block": null, "base_tables": ["product_information"]}, {"alias": "pl", "kind": "base", "block": null, "base_tables": ["product_loss"]}] | [{"type": "LEFT", "right": "purchase_price AS lp", "on": "ds.\"Item Code\" = lp.\"Item Code\"", "using": []}, {"type": "LEFT", "right": "product_information AS p", "on": "ds.\"Item Code\" = p.\"Item Code\"", "using": []}, {"type": "LEFT", "right": "product_loss AS pl", "on": "ds.\"Item Code\" = pl.\"Item Code\"", "using": []}] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | MAX(pp2."Date") | [{"table": "purchase_price", "column": "Date"}] | [] | False |
| B3 | SUM(s."Sales volume (kg)") | [{"table": "sales_records", "column": "Sales volume (kg)"}] | [] | False |
| B3 | AVG(s."Unit price (yuan/kg)") | [{"table": "sales_records", "column": "Unit price (yuan/kg)"}] | [] | False |


## S70

类别 `data`；来源 `query_db`；调用 `9a1992224320489a928da5b1a1415201`；状态 `success`。

```sql
WITH last_price AS (
  SELECT "Item Code", "Wholesale price (yuan/kg)" as wp
  FROM purchase_price
  WHERE ("Item Code", "Date") IN (
    SELECT "Item Code", MAX("Date")
    FROM purchase_price
    GROUP BY "Item Code"
  )
),
day_sales AS (
  SELECT s."Item Code",
    SUM(s."Sales volume (kg)") as vol,
    AVG(s."Unit price (yuan/kg)") as avg_up
  FROM sales_records s
  WHERE date(s."Sales Date") = '2023-06-30' AND s."Sales type" = 'Sale'
  GROUP BY s."Item Code"
)
SELECT ds."Item Code", p."Item Name",
  ROUND(ds.vol,2) as proc_vol_kg,
  ROUND(lp.wp,2) as last_wholesale,
  ROUND(pl."Loss Rate (%)",2) as loss_rate,
  ROUND(lp.wp/(1.0-pl."Loss Rate (%)"/100.0),2) as eff_cost,
  ROUND(ds.avg_up,2) as avg_sell_price,
  ROUND(ds.vol * (ds.avg_up - lp.wp/(1.0-pl."Loss Rate (%)"/100.0)),2) as expected_pnl_0701
FROM day_sales ds
LEFT JOIN last_price lp ON ds."Item Code" = lp."Item Code"
LEFT JOIN product_information p ON ds."Item Code" = p."Item Code"
LEFT JOIN product_loss pl ON ds."Item Code" = pl."Item Code"
WHERE lp.wp IS NOT NULL
ORDER BY expected_pnl_0701 ASC
LIMIT 10
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-025/attempt-01/sql/S70.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-025/attempt-01/sql/S70.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-025/attempt-01/results/S70.rows.jsonl)；完整：True；SHA256：`3faba8cc44df7cd40db3516712df430c0e52761b570dfe289076e98441c8790f`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "purchase_price", "kind": "base", "block": null, "base_tables": ["purchase_price"]}] | [] | ["\"Item Code\""] |
| B2 | [{"alias": "purchase_price", "kind": "base", "block": null, "base_tables": ["purchase_price"]}] | [] | [] |
| B3 | [{"alias": "s", "kind": "base", "block": null, "base_tables": ["sales_records"]}] | [] | ["s.\"Item Code\""] |
| B4 | [{"alias": "ds", "kind": "derived", "block": "B3", "base_tables": ["sales_records"]}, {"alias": "lp", "kind": "derived", "block": "B2", "base_tables": ["purchase_price"]}, {"alias": "p", "kind": "base", "block": null, "base_tables": ["product_information"]}, {"alias": "pl", "kind": "base", "block": null, "base_tables": ["product_loss"]}] | [{"type": "LEFT", "right": "last_price AS lp", "on": "ds.\"Item Code\" = lp.\"Item Code\"", "using": []}, {"type": "LEFT", "right": "product_information AS p", "on": "ds.\"Item Code\" = p.\"Item Code\"", "using": []}, {"type": "LEFT", "right": "product_loss AS pl", "on": "ds.\"Item Code\" = pl.\"Item Code\"", "using": []}] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | MAX("Date") | [{"table": "purchase_price", "column": "Date"}] | [] | False |
| B3 | SUM(s."Sales volume (kg)") | [{"table": "sales_records", "column": "Sales volume (kg)"}] | [] | False |
| B3 | AVG(s."Unit price (yuan/kg)") | [{"table": "sales_records", "column": "Unit price (yuan/kg)"}] | [] | False |


## S71

类别 `data`；来源 `query_db`；调用 `4b406bef875c4e74a380a7542b44e679`；状态 `success`。

```sql
SELECT "Unit price (yuan/kg)", "Sales volume (kg)", "Whether sold at a discount", "Time of sale (code scan)"
FROM sales_records WHERE "Item Code" = 102900051000944 AND date("Sales Date") = '2023-06-30'
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-025/attempt-01/sql/S71.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-025/attempt-01/sql/S71.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-025/attempt-01/results/S71.rows.jsonl)；完整：True；SHA256：`d270603124f70895929685831aace350427a1a49554d1bfcb1f4d0c7b6cacfa5`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "sales_records", "kind": "base", "block": null, "base_tables": ["sales_records"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |


## S72

类别 `data`；来源 `query_db`；调用 `3da20afb6933486e973b2971e1d39209`；状态 `success`。

```sql
SELECT "Date", "Wholesale price (yuan/kg)" FROM purchase_price
WHERE "Item Code" = 102900051000944 AND "Date" >= '2023-06-20' AND "Date" <= '2023-06-30'
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-025/attempt-01/sql/S72.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-025/attempt-01/sql/S72.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-025/attempt-01/results/S72.rows.jsonl)；完整：True；SHA256：`2f879b93a3108c9bd48556399afa314e43257d7060096064481610a9b7d3f183`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "purchase_price", "kind": "base", "block": null, "base_tables": ["purchase_price"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |


## S73

类别 `data`；来源 `query_db`；调用 `5f29c5f413b9472f96f34901ea9a9304`；状态 `success`。

```sql
WITH summer_analysis AS (
  SELECT s."Item Code",
    strftime('%Y', s."Sales Date") as yr,
    strftime('%m', s."Sales Date") as mo,
    s."Unit price (yuan/kg)" as up,
    pp."Wholesale price (yuan/kg)" as wp,
    pl."Loss Rate (%)" as lr,
    s."Unit price (yuan/kg)" - pp."Wholesale price (yuan/kg)"/(1.0-pl."Loss Rate (%)"/100.0) as profit
  FROM sales_records s
  LEFT JOIN purchase_price pp ON s."Item Code" = pp."Item Code" AND date(s."Sales Date") = date(pp."Date")
  LEFT JOIN product_loss pl ON s."Item Code" = pl."Item Code"
  WHERE s."Item Code" = 102900051000944
    AND s."Sales type" = 'Sale'
    AND (
      (s."Sales Date" >= '2020-07-01' AND s."Sales Date" < '2020-09-01')
      OR (s."Sales Date" >= '2021-06-01' AND s."Sales Date" < '2021-09-01')
      OR (s."Sales Date" >= '2022-06-01' AND s."Sales Date" < '2022-09-01')
    )
    AND pp."Wholesale price (yuan/kg)" IS NOT NULL
    AND pl."Loss Rate (%)" IS NOT NULL
)
SELECT yr, mo, COUNT(*) n, ROUND(AVG(profit),3) avg_profit,
  ROUND(SUM(CASE WHEN profit<0 THEN 1 ELSE 0 END)*100.0/COUNT(*),1) pct_loss
FROM summer_analysis GROUP BY yr, mo ORDER BY yr, mo
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-025/attempt-01/sql/S73.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-025/attempt-01/sql/S73.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-025/attempt-01/results/S73.rows.jsonl)；完整：True；SHA256：`9afdfa2b9a8b7a32e3c1f84358265dacda16b4062f4fc16da2c10377576686f6`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "s", "kind": "base", "block": null, "base_tables": ["sales_records"]}, {"alias": "pp", "kind": "base", "block": null, "base_tables": ["purchase_price"]}, {"alias": "pl", "kind": "base", "block": null, "base_tables": ["product_loss"]}] | [{"type": "LEFT", "right": "purchase_price AS pp", "on": "s.\"Item Code\" = pp.\"Item Code\" AND DATE(s.\"Sales Date\") = DATE(pp.\"Date\")", "using": []}, {"type": "LEFT", "right": "product_loss AS pl", "on": "s.\"Item Code\" = pl.\"Item Code\"", "using": []}] | [] |
| B2 | [{"alias": "summer_analysis", "kind": "derived", "block": "B1", "base_tables": ["product_loss", "purchase_price", "sales_records"]}] | [] | ["yr", "mo"] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B2 | COUNT(*) | [] | [] | True |
| B2 | AVG(profit) | [{"table": "sales_records", "column": "Unit price (yuan/kg)"}, {"table": "purchase_price", "column": "Wholesale price (yuan/kg)"}, {"table": "product_loss", "column": "Loss Rate (%)"}] | [] | False |
| B2 | COUNT(*) | [] | [] | True |
| B2 | SUM(CASE WHEN profit < 0 THEN 1 ELSE 0 END) | [] | [{"table": "sales_records", "column": "Unit price (yuan/kg)"}, {"table": "purchase_price", "column": "Wholesale price (yuan/kg)"}, {"table": "product_loss", "column": "Loss Rate (%)"}] | False |


## S74

类别 `data`；来源 `query_db`；调用 `5165892c88324b83b3f359e36f2b4707`；状态 `success`。

```sql
WITH last_price AS (
  SELECT "Item Code", "Wholesale price (yuan/kg)" as wp
  FROM purchase_price
  WHERE ("Item Code", "Date") IN (
    SELECT "Item Code", MAX("Date")
    FROM purchase_price
    GROUP BY "Item Code"
  )
),
day_sales AS (
  SELECT s."Item Code",
    SUM(s."Sales volume (kg)") as vol,
    AVG(s."Unit price (yuan/kg)") as avg_up
  FROM sales_records s
  WHERE date(s."Sales Date") = '2023-06-30' AND s."Sales type" = 'Sale'
  GROUP BY s."Item Code"
)
SELECT ds."Item Code", p."Item Name",
  ROUND(ds.vol,2) as proc_vol_kg,
  ROUND(ds.avg_up,2) as avg_sell_price,
  ROUND(lp.wp/(1.0-pl."Loss Rate (%)"/100.0),2) as eff_cost,
  ROUND(ds.vol * (ds.avg_up - lp.wp/(1.0-pl."Loss Rate (%)"/100.0)),2) as expected_pnl_0701
FROM day_sales ds
LEFT JOIN last_price lp ON ds."Item Code" = lp."Item Code"
LEFT JOIN product_information p ON ds."Item Code" = p."Item Code"
LEFT JOIN product_loss pl ON ds."Item Code" = pl."Item Code"
WHERE lp.wp IS NOT NULL
ORDER BY expected_pnl_0701 ASC
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-025/attempt-01/sql/S74.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-025/attempt-01/sql/S74.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-025/attempt-01/results/S74.rows.jsonl)；完整：True；SHA256：`11fab331c555922f52c2c582c230c166abc175ed07dd2789ed9aa6710e3644fe`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "purchase_price", "kind": "base", "block": null, "base_tables": ["purchase_price"]}] | [] | ["\"Item Code\""] |
| B2 | [{"alias": "purchase_price", "kind": "base", "block": null, "base_tables": ["purchase_price"]}] | [] | [] |
| B3 | [{"alias": "s", "kind": "base", "block": null, "base_tables": ["sales_records"]}] | [] | ["s.\"Item Code\""] |
| B4 | [{"alias": "ds", "kind": "derived", "block": "B3", "base_tables": ["sales_records"]}, {"alias": "lp", "kind": "derived", "block": "B2", "base_tables": ["purchase_price"]}, {"alias": "p", "kind": "base", "block": null, "base_tables": ["product_information"]}, {"alias": "pl", "kind": "base", "block": null, "base_tables": ["product_loss"]}] | [{"type": "LEFT", "right": "last_price AS lp", "on": "ds.\"Item Code\" = lp.\"Item Code\"", "using": []}, {"type": "LEFT", "right": "product_information AS p", "on": "ds.\"Item Code\" = p.\"Item Code\"", "using": []}, {"type": "LEFT", "right": "product_loss AS pl", "on": "ds.\"Item Code\" = pl.\"Item Code\"", "using": []}] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | MAX("Date") | [{"table": "purchase_price", "column": "Date"}] | [] | False |
| B3 | SUM(s."Sales volume (kg)") | [{"table": "sales_records", "column": "Sales volume (kg)"}] | [] | False |
| B3 | AVG(s."Unit price (yuan/kg)") | [{"table": "sales_records", "column": "Unit price (yuan/kg)"}] | [] | False |


## S75

类别 `data`；来源 `python`；调用 `4ab92ea8f56d4589aa436d2c66edf27b`；状态 `success`。

```sql

WITH summer_analysis AS (
  SELECT s."Item Code",
    strftime('%Y-%m', s."Sales Date") as ym,
    strftime('%m', s."Sales Date") as mo,
    s."Unit price (yuan/kg)" as up,
    pp."Wholesale price (yuan/kg)" as wp,
    pl."Loss Rate (%)" as lr,
    s."Unit price (yuan/kg)" - pp."Wholesale price (yuan/kg)"/(1.0-pl."Loss Rate (%)"/100.0) as profit
  FROM sales_records s
  LEFT JOIN purchase_price pp ON s."Item Code" = pp."Item Code" AND date(s."Sales Date") = date(pp."Date")
  LEFT JOIN product_loss pl ON s."Item Code" = pl."Item Code"
  WHERE s."Item Code" IN (102900005118824, 102900011032732)
    AND s."Sales type" = 'Sale'
    AND s."Sales Date" >= '2022-06-01' AND s."Sales Date" < '2022-09-01'
    AND pp."Wholesale price (yuan/kg)" IS NOT NULL
    AND pl."Loss Rate (%)" IS NOT NULL
)
SELECT "Item Code", mo, COUNT(*) n, ROUND(AVG(profit),3) avg_profit,
  ROUND(AVG(up),2) avg_up, ROUND(AVG(wp/(1.0-lr/100.0)),2) avg_cost,
  ROUND(SUM(CASE WHEN profit<0 THEN 1 ELSE 0 END)*100.0/COUNT(*),1) pct_loss
FROM summer_analysis
GROUP BY "Item Code", mo
ORDER BY "Item Code", mo

```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-025/attempt-01/sql/S75.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-025/attempt-01/sql/S75.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-025/attempt-01/results/S75.rows.jsonl)；完整：True；SHA256：`5c05140b1d01d26a38502afc279974271c7a364f88240b98944c38181532a9a1`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "s", "kind": "base", "block": null, "base_tables": ["sales_records"]}, {"alias": "pp", "kind": "base", "block": null, "base_tables": ["purchase_price"]}, {"alias": "pl", "kind": "base", "block": null, "base_tables": ["product_loss"]}] | [{"type": "LEFT", "right": "purchase_price AS pp", "on": "s.\"Item Code\" = pp.\"Item Code\" AND DATE(s.\"Sales Date\") = DATE(pp.\"Date\")", "using": []}, {"type": "LEFT", "right": "product_loss AS pl", "on": "s.\"Item Code\" = pl.\"Item Code\"", "using": []}] | [] |
| B2 | [{"alias": "summer_analysis", "kind": "derived", "block": "B1", "base_tables": ["product_loss", "purchase_price", "sales_records"]}] | [] | ["\"Item Code\"", "mo"] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B2 | COUNT(*) | [] | [] | True |
| B2 | AVG(profit) | [{"table": "sales_records", "column": "Unit price (yuan/kg)"}, {"table": "purchase_price", "column": "Wholesale price (yuan/kg)"}, {"table": "product_loss", "column": "Loss Rate (%)"}] | [] | False |
| B2 | AVG(up) | [{"table": "sales_records", "column": "Unit price (yuan/kg)"}] | [] | False |
| B2 | AVG(wp / (1.0 - lr / 100.0)) | [{"table": "purchase_price", "column": "Wholesale price (yuan/kg)"}, {"table": "product_loss", "column": "Loss Rate (%)"}] | [] | False |
| B2 | COUNT(*) | [] | [] | True |
| B2 | SUM(CASE WHEN profit < 0 THEN 1 ELSE 0 END) | [] | [{"table": "sales_records", "column": "Unit price (yuan/kg)"}, {"table": "purchase_price", "column": "Wholesale price (yuan/kg)"}, {"table": "product_loss", "column": "Loss Rate (%)"}] | False |


## S76

类别 `data`；来源 `python`；调用 `4ab92ea8f56d4589aa436d2c66edf27b`；状态 `success`。

```sql
SELECT "Item Code", "Item Name" FROM product_information WHERE "Item Code" IN (102900005118824, 102900011032732)
```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-025/attempt-01/sql/S76.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-025/attempt-01/sql/S76.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-025/attempt-01/results/S76.rows.jsonl)；完整：True；SHA256：`ebb7bb54b754ee1ca4b0ee9713a0fcd2d9bef5264690ac4ec998bfc4f073fef2`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "product_information", "kind": "base", "block": null, "base_tables": ["product_information"]}] | [] | [] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |


## S77

类别 `data`；来源 `python`；调用 `2aefa419bad144cfa3d927a9d00eb612`；状态 `success`。

```sql

WITH summer_analysis AS (
  SELECT s."Item Code",
    strftime('%m', s."Sales Date") as mo,
    s."Unit price (yuan/kg)" as up,
    pp."Wholesale price (yuan/kg)" as wp,
    pl."Loss Rate (%)" as lr,
    s."Unit price (yuan/kg)" - pp."Wholesale price (yuan/kg)"/(1.0-pl."Loss Rate (%)"/100.0) as profit
  FROM sales_records s
  LEFT JOIN purchase_price pp ON s."Item Code" = pp."Item Code" AND date(s."Sales Date") = date(pp."Date")
  LEFT JOIN product_loss pl ON s."Item Code" = pl."Item Code"
  WHERE s."Item Code" IN (102900005118824, 102900011032732)
    AND s."Sales type" = 'Sale'
    AND s."Sales Date" >= '2022-06-01' AND s."Sales Date" < '2022-09-01'
    AND pp."Wholesale price (yuan/kg)" IS NOT NULL
    AND pl."Loss Rate (%)" IS NOT NULL
)
SELECT "Item Code", mo, COUNT(*) n, AVG(up) avg_up, AVG(wp/(1.0-lr/100.0)) avg_cost
FROM summer_analysis GROUP BY "Item Code", mo

```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-025/attempt-01/sql/S77.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-025/attempt-01/sql/S77.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-025/attempt-01/results/S77.rows.jsonl)；完整：True；SHA256：`3a4824df3e200793d70838154f1c1629ed93ef28b4b675f4d2d206be1f059654`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "s", "kind": "base", "block": null, "base_tables": ["sales_records"]}, {"alias": "pp", "kind": "base", "block": null, "base_tables": ["purchase_price"]}, {"alias": "pl", "kind": "base", "block": null, "base_tables": ["product_loss"]}] | [{"type": "LEFT", "right": "purchase_price AS pp", "on": "s.\"Item Code\" = pp.\"Item Code\" AND DATE(s.\"Sales Date\") = DATE(pp.\"Date\")", "using": []}, {"type": "LEFT", "right": "product_loss AS pl", "on": "s.\"Item Code\" = pl.\"Item Code\"", "using": []}] | [] |
| B2 | [{"alias": "summer_analysis", "kind": "derived", "block": "B1", "base_tables": ["product_loss", "purchase_price", "sales_records"]}] | [] | ["\"Item Code\"", "mo"] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B2 | COUNT(*) | [] | [] | True |
| B2 | AVG(up) | [{"table": "sales_records", "column": "Unit price (yuan/kg)"}] | [] | False |
| B2 | AVG(wp / (1.0 - lr / 100.0)) | [{"table": "purchase_price", "column": "Wholesale price (yuan/kg)"}, {"table": "product_loss", "column": "Loss Rate (%)"}] | [] | False |


## S78

类别 `data`；来源 `python`；调用 `2aefa419bad144cfa3d927a9d00eb612`；状态 `success`。

```sql

SELECT s."Item Code", p."Item Name",
  COUNT(*) n_sales,
  ROUND(SUM(s."Sales volume (kg)"),2) vol,
  ROUND(AVG(s."Unit price (yuan/kg)"),2) avg_up,
  ROUND(AVG(pp."Wholesale price (yuan/kg)"),2) avg_wp,
  ROUND(AVG(pp."Wholesale price (yuan/kg)")/(1.0-pl."Loss Rate (%)"/100.0),2) avg_cost,
  ROUND(SUM(CASE WHEN s."Unit price (yuan/kg)" < pp."Wholesale price (yuan/kg)"/(1.0-pl."Loss Rate (%)"/100.0) THEN 1 ELSE 0 END)*100.0/COUNT(*),1) pct_loss_sales
FROM sales_records s
LEFT JOIN product_information p ON s."Item Code" = p."Item Code"
LEFT JOIN purchase_price pp ON s."Item Code" = pp."Item Code" AND date(s."Sales Date") = date(pp."Date")
LEFT JOIN product_loss pl ON s."Item Code" = pl."Item Code"
WHERE date(s."Sales Date") = '2023-06-30' AND s."Sales type" = 'Sale'
  AND s."Item Code" IN (102900005118824, 102900011032732)
  AND pp."Wholesale price (yuan/kg)" IS NOT NULL
GROUP BY s."Item Code"

```

[SQL](../../../runs/dsv4flash-db-first-full-01/dacomp-025/attempt-01/sql/S78.sql)；[绑定参数](../../../runs/dsv4flash-db-first-full-01/dacomp-025/attempt-01/sql/S78.parameters.json)。

[原始行数组](../../../runs/dsv4flash-db-first-full-01/dacomp-025/attempt-01/results/S78.rows.jsonl)；完整：True；SHA256：`02d0d9ca6e092420f1f5b806a772528add07596c78c5e2a95923b70d72f94cb2`。

| 查询块 | 来源实例与基础表 | Join 条件 | 分组维度 |
| --- | --- | --- | --- |
| B1 | [{"alias": "s", "kind": "base", "block": null, "base_tables": ["sales_records"]}, {"alias": "p", "kind": "base", "block": null, "base_tables": ["product_information"]}, {"alias": "pp", "kind": "base", "block": null, "base_tables": ["purchase_price"]}, {"alias": "pl", "kind": "base", "block": null, "base_tables": ["product_loss"]}] | [{"type": "LEFT", "right": "product_information AS p", "on": "s.\"Item Code\" = p.\"Item Code\"", "using": []}, {"type": "LEFT", "right": "purchase_price AS pp", "on": "s.\"Item Code\" = pp.\"Item Code\" AND DATE(s.\"Sales Date\") = DATE(pp.\"Date\")", "using": []}, {"type": "LEFT", "right": "product_loss AS pl", "on": "s.\"Item Code\" = pl.\"Item Code\"", "using": []}] | ["s.\"Item Code\""] |


| 块 | 聚合表达式 | 指标列血缘 | 条件列血缘 | 行计数 |
| --- | --- | --- | --- | --- |
| B1 | COUNT(*) | [] | [] | True |
| B1 | SUM(s."Sales volume (kg)") | [{"table": "sales_records", "column": "Sales volume (kg)"}] | [] | False |
| B1 | AVG(s."Unit price (yuan/kg)") | [{"table": "sales_records", "column": "Unit price (yuan/kg)"}] | [] | False |
| B1 | AVG(pp."Wholesale price (yuan/kg)") | [{"table": "purchase_price", "column": "Wholesale price (yuan/kg)"}] | [] | False |
| B1 | AVG(pp."Wholesale price (yuan/kg)") | [{"table": "purchase_price", "column": "Wholesale price (yuan/kg)"}] | [] | False |
| B1 | COUNT(*) | [] | [] | True |
| B1 | SUM(CASE WHEN s."Unit price (yuan/kg)" < pp."Wholesale price (yuan/kg)" / (1.0 - pl."Loss Rate (%)" / 100.0) THEN 1 ELSE 0 END) | [] | [{"table": "sales_records", "column": "Unit price (yuan/kg)"}, {"table": "purchase_price", "column": "Wholesale price (yuan/kg)"}, {"table": "product_loss", "column": "Loss Rate (%)"}] | False |

